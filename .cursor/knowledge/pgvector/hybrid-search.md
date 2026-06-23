---
title: "Hybrid Search - Vector + SQL Filters"
description: "Hướng dẫn về hybrid search kết hợp vector similarity search với SQL filters, weighted scoring và RRF fusion"
tags: ["hybrid-search", "pgvector", "vector-search", "rrf", "reciprocal-rank-fusion"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Hybrid Search - Vector + SQL Filters

## Tổng Quan

Hybrid search là kỹ thuật kết hợp khả năng tìm kiếm semantic của vector search với khả năng lọc chính xác của traditional SQL queries. Trong thực tế, hầu hết các ứng dụng RAG (Retrieval Augmented Generation) và recommendation systems đều cần kết hợp cả hai phương pháp này để đạt được kết quả tối ưu.

pgvector cung cấp các toán tử vector similarity (`<=>`, `<+>`, `<->`, `<#>`) có thể được sử dụng trực tiếp trong WHERE clauses, cho phép developers dễ dàng kết hợp vector search với các điều kiện lọc SQL truyền thống.

Tuy nhiên, việc kết hợp này đòi hỏi hiểu biết sâu về cách PostgreSQL planner xử lý các queries dạng hybrid, cũng như các kỹ thuật tối ưu như pre-filtering, post-filtering và weighted scoring.

## Mục Đích

Tài liệu này nhằm mục đích cung cấp kiến thức toàn diện về hybrid search trong pgvector, bao gồm:

Đầu tiên, chúng ta sẽ tìm hiểu các phương pháp kết hợp vector search với SQL filters, từ basic pre-filtering đến advanced weighted scoring.

Thứ hai, tài liệu giới thiệu Reciprocal Rank Fusion (RRF) như một phương pháp hiệu quả để merge kết quả từ multiple retrieval methods.

Thứ ba, chúng ta sẽ đề cập đến các best practices để đạt được hiệu suất tối ưu khi thực hiện hybrid retrieval.

Cuối cùng, tài liệu cung cấp các code examples thực tế cho việc implement hybrid search trong production systems.

## Key Concepts

### 1. Basic Hybrid Search Patterns

#### Pre-filtering (Filter-first)

Trong pre-filtering, chúng ta áp dụng SQL filters trước khi thực hiện vector search. Điều này đảm bảo rằng chỉ có các documents thỏa mãn điều kiện lọc mới được tìm kiếm.

```sql
-- Pre-filtering: filter trước, search sau
SELECT 
    id,
    title,
    content,
    1 - (embedding <=> $query_embedding) AS similarity
FROM documents
WHERE 
    status = 'published'
    AND category_id = $category_id
    AND created_at > NOW() - INTERVAL '30 days'
ORDER BY embedding <=> $query_embedding
LIMIT 20;
```

Pre-filtering hoạt động tốt khi filter conditions có selectivity cao (loại bỏ được nhiều documents không liên quan) và khi filtered result set vẫn đủ lớn để vector search có ý nghĩa.

#### Post-filtering (Search-first)

Trong post-filtering, chúng ta thực hiện vector search trước, sau đó lọc kết quả bằng SQL conditions.

```sql
-- Post-filtering: search trước, filter sau
SELECT *
FROM (
    SELECT 
        id,
        title,
        content,
        1 - (embedding <=> $query_embedding) AS similarity
    FROM documents
    ORDER BY embedding <=> $query_embedding
    LIMIT 200
) AS ranked
WHERE 
    status = 'published'
    AND category_id = $category_id
    AND created_at > NOW() - INTERVAL '30 days'
LIMIT 20;
```

Post-filtering đảm bảo recall cao hơn vì không có documents nào bị loại trừ trước khi tìm kiếm, nhưng có thể trả về ít kết quả hơn nếu filter conditions quá restrictive.

### 2. Weighted Scoring

Weighted scoring cho phép chúng ta kết hợp multiple scoring signals (vector similarity, BM25, recency, popularity) vào một điểm số duy nhất.

```sql
-- Weighted scoring với multiple signals
SELECT 
    id,
    title,
    content,
    -- Vector similarity (0-1, cao hơn = tốt hơn)
    (1 - (embedding <=> $query_embedding)) AS vector_score,
    
    -- Recency score (0-1, gần đây = cao hơn)
    GREATEST(0, LEAST(1, 
        EXTRACT(EPOCH FROM (NOW() - created_at)) / (30 * 24 * 60 * 60)
    )) AS recency_score,
    
    -- Popularity score (0-1, phổ biến = cao hơn)
    LEAST(1, log(view_count + 1) / 10) AS popularity_score,
    
    -- Combined weighted score
    (
        0.6 * (1 - (embedding <=> $query_embedding)) +
        0.2 * GREATEST(0, LEAST(1, 
            EXTRACT(EPOCH FROM (NOW() - created_at)) / (30 * 24 * 60 * 60)
        )) +
        0.2 * LEAST(1, log(view_count + 1) / 10)
    ) AS combined_score
FROM documents
WHERE status = 'published'
ORDER BY combined_score DESC
LIMIT 20;
```

### 3. Reciprocal Rank Fusion (RRF)

RRF là thuật toán đơn giản nhưng hiệu quả để kết hợp kết quả từ multiple retrieval methods. Công thức:

```
RRF_score(d) = Σ 1 / (k + rank_i(d))
```

Trong đó:
- `d` là document
- `rank_i(d)` là rank của document trong result set thứ i
- `k` là constant (thường là 60)

```sql
-- RRF fusion giữa vector search và full-text search
WITH vector_results AS (
    SELECT 
        id,
        title,
        content,
        ROW_NUMBER() OVER (ORDER BY embedding <=> $query_embedding) as rank,
        1 - (embedding <=> $query_embedding) as score
    FROM documents
    WHERE status = 'published'
),
text_results AS (
    SELECT 
        id,
        title,
        content,
        ROW_NUMBER() OVER (ORDER BY ts_rank(to_tsvector('english', content), plainto_tsquery('english', $query_text))) DESC) as rank,
        ts_rank(to_tsvector('english', content), plainto_tsquery('english', $query_text)) as score
    FROM documents
    WHERE status = 'published'
      AND content ILIKE '%' || $query_text || '%'
),
fused AS (
    SELECT 
        COALESCE(v.id, t.id) as id,
        COALESCE(v.title, t.title) as title,
        COALESCE(v.content, t.content) as content,
        COALESCE(v.score, 0) as vector_score,
        COALESCE(t.score, 0) as text_score,
        -- RRF formula với k = 60
        COALESCE(1.0 / (60 + v.rank), 0) + 
        COALESCE(1.0 / (60 + t.rank), 0) as rrf_score
    FROM vector_results v
    FULL OUTER JOIN text_results t ON v.id = t.id
)
SELECT 
    id,
    title,
    LEFT(content, 200) as content_preview,
    vector_score,
    text_score,
    rrf_score
FROM fused
ORDER BY rrf_score DESC
LIMIT 20;
```

## Best Practices

### 1. Indexing Strategy for Hybrid Queries

```sql
-- Tạo cả vector index và filter indexes
-- Vector index cho semantic search
CREATE INDEX idx_embeddings_hnsw ON document_chunks 
    USING hnsw (embedding vector_cosine_ops) 
    WITH (m = 16, ef_construction = 200);

-- B-tree indexes cho filters phổ biến
CREATE INDEX idx_documents_category ON documents (category_id);
CREATE INDEX idx_documents_status ON documents (status);
CREATE INDEX idx_documents_created ON documents (created_at DESC);

-- Composite index cho common filter combinations
CREATE INDEX idx_documents_category_status 
    ON documents (category_id, status);

-- Partial index cho active documents
CREATE INDEX idx_documents_active 
    ON documents (created_at DESC) 
    WHERE status = 'published';
```

### 2. Query Optimization

```sql
-- Sử dụng prepared statements để tránh parse overhead
PREPARE hybrid_search(UUID, VECTOR(1536), INTEGER, TIMESTAMPTZ) AS
SELECT 
    id,
    title,
    1 - (embedding <=> $2) AS similarity
FROM documents
WHERE 
    status = 'published'
    AND category_id = $3
    AND created_at > $4
ORDER BY embedding <=> $2
LIMIT 20;

-- Execute prepared statement
EXECUTE hybrid_search(
    NULL,
    '[0.1, 0.2, ...]::vector',
    5,
    NOW() - INTERVAL '30 days'
);

-- Deallocate khi không cần
DEALLOCATE hybrid_search;
```

### 3. Handling Empty Results

```sql
-- Fallback strategy khi hybrid search trả về ít kết quả
CREATE OR REPLACE FUNCTION hybrid_search_with_fallback(
    p_query_embedding REAL[],
    p_category_id INTEGER,
    p_limit INTEGER DEFAULT 20
) RETURNS TABLE(
    id UUID,
    title TEXT,
    content TEXT,
    similarity FLOAT,
    search_method TEXT
) AS $$
DECLARE
    v_hybrid_count INTEGER;
    v_fallback_count INTEGER;
BEGIN
    -- Thử hybrid search trước
    RETURN QUERY
    WITH hybrid AS (
        SELECT 
            d.id,
            d.title,
            d.content,
            1 - (d.embedding <=> p_query_embedding::vector) AS similarity,
            'hybrid' as search_method,
            ROW_NUMBER() OVER (ORDER BY d.embedding <=> p_query_embedding::vector) as rn
        FROM documents d
        WHERE d.status = 'published'
          AND d.category_id = p_category_id
    )
    SELECT h.id, h.title, h.content, h.similarity, h.search_method
    FROM hybrid h
    WHERE h.rn <= p_limit;
    
    GET DIAGNOSTICS v_hybrid_count = ROW_COUNT;
    
    -- Nếu hybrid search trả về ít hơn limit, bổ sung với broader search
    IF v_hybrid_count < p_limit THEN
        RETURN QUERY
        WITH existing AS (
            SELECT id FROM hybrid_search_with_fallback(p_query_embedding, p_category_id, p_limit)
        ),
        fallback AS (
            SELECT 
                d.id,
                d.title,
                d.content,
                1 - (d.embedding <=> p_query_embedding::vector) AS similarity,
                'fallback' as search_method,
                ROW_NUMBER() OVER (ORDER BY d.embedding <=> p_query_embedding::vector) as rn
            FROM documents d
            WHERE d.status = 'published'
              AND d.id NOT IN (SELECT id FROM existing)
        )
        SELECT f.id, f.title, f.content, f.similarity, f.search_method
        FROM fallback f
        WHERE f.rn <= p_limit - v_hybrid_count;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

## Common Patterns

### Pattern 1: Multi-dimensional Filtering

```sql
-- Filter với nhiều dimensions
CREATE OR REPLACE FUNCTION advanced_search(
    p_query_embedding REAL[],
    p_filters JSONB DEFAULT '{}'
) RETURNS TABLE(
    id UUID,
    title TEXT,
    content TEXT,
    similarity FLOAT
) AS $$
DECLARE
    v_min_similarity FLOAT := COALESCE((p_filters->>'min_similarity')::float, 0.5);
    v_category_id INTEGER := (p_filters->>'category_id')::integer;
    v_tags TEXT[] := ARRAY(SELECT jsonb_array_elements_text(p_filters->'tags'));
    v_date_from TIMESTAMPTZ := (p_filters->>'date_from')::timestamptz;
    v_date_to TIMESTAMPTZ := (p_filters->>'date_to')::timestamptz;
    v_limit INTEGER := COALESCE((p_filters->>'limit')::integer, 20);
BEGIN
    RETURN QUERY
    SELECT 
        d.id,
        d.title,
        d.content,
        1 - (d.embedding <=> p_query_embedding::vector) AS similarity
    FROM documents d
    WHERE 
        -- Similarity threshold
        1 - (d.embedding <=> p_query_embedding::vector) >= v_min_similarity
        -- Category filter
        AND (v_category_id IS NULL OR d.category_id = v_category_id)
        -- Date range filter
        AND (v_date_from IS NULL OR d.created_at >= v_date_from)
        AND (v_date_to IS NULL OR d.created_at <= v_date_to)
        -- Tags filter (AND logic)
        AND (
            v_tags IS NULL OR v_tags = '{}'::text[]
            OR metadata->'tags' ?| v_tags
        )
    ORDER BY d.embedding <=> p_query_embedding::vector
    LIMIT v_limit;
END;
$$ LANGUAGE plpgsql;

-- Usage
SELECT * FROM advanced_search(
    '[0.1, 0.2, ...]::real[]',
    '{
        "min_similarity": 0.7,
        "category_id": 5,
        "tags": ["ai", "ml"],
        "date_from": "2024-01-01",
        "limit": 20
    }'::jsonb
);
```

### Pattern 2: Geographic + Vector Hybrid Search

```sql
-- Kết hợp vector search với geospatial filtering
CREATE TABLE businesses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    embedding VECTOR(1536) NOT NULL,
    location GEOGRAPHY(POINT, 4326),
    category VARCHAR(100),
    rating FLOAT DEFAULT 0
);

CREATE INDEX idx_businesses_location ON businesses USING GIST (location);
CREATE INDEX idx_businesses_embedding ON businesses USING hnsw (embedding vector_cosine_ops);

-- Search nearby businesses với similar description
CREATE OR REPLACE FUNCTION nearby_similar_search(
    p_query_embedding REAL[],
    p_longitude FLOAT,
    p_latitude FLOAT,
    p_radius_meters INTEGER DEFAULT 5000
) RETURNS TABLE(
    id UUID,
    name TEXT,
    description TEXT,
    distance_meters FLOAT,
    similarity FLOAT,
    score FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        b.id,
        b.name,
        b.description,
        ST_Distance(
            b.location,
            ST_SetSRID(ST_MakePoint(p_longitude, p_latitude), 4326)::geography
        ) AS distance_meters,
        1 - (b.embedding <=> p_query_embedding::vector) AS similarity,
        -- Combined score: 70% similarity, 30% proximity
        (
            0.7 * (1 - (b.embedding <=> p_query_embedding::vector)) +
            0.3 * (1 - LEAST(1, 
                ST_Distance(
                    b.location,
                    ST_SetSRID(ST_MakePoint(p_longitude, p_latitude), 4326)::geography
                ) / p_radius_meters
            ))
        ) AS score
    FROM businesses b
    WHERE ST_DWithin(
        b.location,
        ST_SetSRID(ST_MakePoint(p_longitude, p_latitude), 4326)::geography,
        p_radius_meters
    )
    ORDER BY score DESC
    LIMIT 20;
END;
$$ LANGUAGE plpgsql;
```

### Pattern 3: User Personalization with Hybrid Search

```sql
-- Sử dụng user embedding cho personalized search
CREATE TABLE user_preferences (
    user_id UUID PRIMARY KEY REFERENCES users(id),
    interest_embedding VECTOR(1536) NOT NULL,
    favorite_categories INTEGER[],
    excluded_categories INTEGER[],
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_user_prefs_embedding ON user_preferences 
    USING hnsw (interest_embedding vector_cosine_ops);

-- Personalized hybrid search
CREATE OR REPLACE FUNCTION personalized_search(
    p_user_id UUID,
    p_query_embedding REAL[],
    p_limit INTEGER DEFAULT 20
) RETURNS TABLE(
    id UUID,
    title TEXT,
    content TEXT,
    similarity FLOAT,
    personalization_score FLOAT
) AS $$
DECLARE
    v_user_embedding VECTOR(1536);
    v_favorite_categories INTEGER[];
    v_excluded_categories INTEGER[];
BEGIN
    -- Get user preferences
    SELECT 
        interest_embedding,
        favorite_categories,
        excluded_categories
    INTO v_user_embedding, v_favorite_categories, v_excluded_categories
    FROM user_preferences
    WHERE user_id = p_user_id;
    
    -- Default embedding if user has no preferences
    v_user_embedding := COALESCE(v_user_embedding, p_query_embedding::vector);
    
    RETURN QUERY
    SELECT 
        d.id,
        d.title,
        d.content,
        1 - (d.embedding <=> p_query_embedding::vector) AS similarity,
        -- Personalization boost
        (
            0.6 * (1 - (d.embedding <=> p_query_embedding::vector)) +
            0.4 * (1 - (d.embedding <=> v_user_embedding))
        ) AS personalization_score
    FROM documents d
    WHERE 
        d.status = 'published'
        -- Boost favorites
        AND (v_favorite_categories IS NULL OR v_favorite_categories = '{}' 
             OR d.category_id = ANY(v_favorite_categories))
        -- Exclude non-favorites
        AND (v_excluded_categories IS NULL OR v_excluded_categories = '{}'
             OR d.category_id != ALL(v_excluded_categories))
    ORDER BY personalization_score DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;
```

## Troubleshooting

### Vấn Đề 1: Slow Hybrid Queries

```sql
-- Analyze query plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT id, title
FROM documents
WHERE status = 'published'
  AND category_id = 5
ORDER BY embedding <=> $1::vector
LIMIT 20;

-- Nếu không sử dụng index, force index usage
SET enable_seqscan = off;

-- Hoặc sử dụng sequential scan nhưng với filter nhỏ
SET enable_seqscan = on;

-- Kiểm tra index stats
SELECT 
    indexrelname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan;
```

### Vấn Đề 2: Poor Recall với Strict Filters

```sql
-- Debug: count documents match filter
SELECT 
    category_id,
    status,
    COUNT(*) as doc_count
FROM documents
GROUP BY category_id, status
ORDER BY doc_count DESC;

-- Adjust filter nếu quá restrictive
-- Thay vì exact match, sử dụng range
SELECT * FROM documents
WHERE 
    status = 'published'
    AND (category_id = 5 OR category_id IS NULL)  -- Include NULL
    AND embedding <=> $1::vector < 0.5  -- similarity threshold
ORDER BY embedding <=> $1::vector;
```

### Vấn Đề 3: Inconsistent Results với RRF

```sql
-- Debug RRF calculation
WITH sample_data AS (
    SELECT 1 as doc_id, 1 as vector_rank, 2 as text_rank
    UNION ALL
    SELECT 2, 2, 1
    UNION ALL
    SELECT 3, 3, 3
)
SELECT 
    doc_id,
    1.0 / (60 + vector_rank) as vector_rrf,
    1.0 / (60 + text_rank) as text_rrf,
    1.0 / (60 + vector_rank) + 1.0 / (60 + text_rank) as total_rrf
FROM sample_data
ORDER BY total_rrf DESC;

-- Test different k values
SELECT 
    doc_id,
    1.0 / (60 + vector_rank) + 1.0 / (60 + text_rank) as rrf_k60,
    1.0 / (30 + vector_rank) + 1.0 / (30 + text_rank) as rrf_k30,
    1.0 / (100 + vector_rank) + 1.0 / (100 + text_rank) as rrf_k100
FROM sample_data
ORDER BY rrf_k60 DESC;
```

## Examples

### Example 1: Production RAG Hybrid Search

```sql
-- Complete RAG search implementation
CREATE TABLE rag_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type VARCHAR(50) NOT NULL,  -- 'pdf', 'web', 'api'
    source_id VARCHAR(255),
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1536) NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE (source_type, source_id)
);

CREATE INDEX idx_rag_embedding ON rag_documents 
    USING hnsw (embedding vector_cosine_ops) 
    WITH (m = 16, ef_construction = 200);

CREATE INDEX idx_rag_source ON rag_documents (source_type, source_id);
CREATE INDEX idx_rag_created ON rag_documents (created_at DESC);

-- Main RAG search function
CREATE OR REPLACE FUNCTION rag_hybrid_search(
    p_query_embedding REAL[],
    p_query_text TEXT DEFAULT NULL,
    p_source_types TEXT[] DEFAULT NULL,
    p_date_from TIMESTAMPTZ DEFAULT NULL,
    p_date_to TIMESTAMPTZ DEFAULT NULL,
    p_min_similarity FLOAT DEFAULT 0.5,
    p_limit INTEGER DEFAULT 10,
    p_include_text_search BOOLEAN DEFAULT TRUE
) RETURNS TABLE(
    id UUID,
    source_type VARCHAR(50),
    title TEXT,
    content TEXT,
    metadata JSONB,
    vector_score FLOAT,
    text_score FLOAT,
    rrf_score FLOAT
) AS $$
BEGIN
    IF p_include_text_search AND p_query_text IS NOT NULL THEN
        -- RRF fusion với cả vector và text search
        RETURN QUERY
        WITH vector_search AS (
            SELECT 
                id,
                source_type,
                title,
                LEFT(content, 500) as content,
                metadata,
                1 - (embedding <=> p_query_embedding::vector) as vector_score,
                0.0 as text_score,
                ROW_NUMBER() OVER (ORDER BY embedding <=> p_query_embedding::vector) as vector_rank
            FROM rag_documents
            WHERE 
                (p_source_types IS NULL OR source_type = ANY(p_source_types))
                AND (p_date_from IS NULL OR created_at >= p_date_from)
                AND (p_date_to IS NULL OR created_at <= p_date_to)
                AND 1 - (embedding <=> p_query_embedding::vector) >= p_min_similarity
        ),
        text_search AS (
            SELECT 
                id,
                ts_rank(
                    setweight(to_tsvector('english', title), 'A') ||
                    setweight(to_tsvector('english', content), 'B'),
                    plainto_tsquery('english', p_query_text)
                ) as text_score,
                ROW_NUMBER() OVER (ORDER BY 
                    ts_rank(
                        setweight(to_tsvector('english', title), 'A') ||
                        setweight(to_tsvector('english', content), 'B'),
                        plainto_tsquery('english', p_query_text)
                    ) DESC
                ) as text_rank
            FROM rag_documents
            WHERE 
                (p_source_types IS NULL OR source_type = ANY(p_source_types))
                AND (p_date_from IS NULL OR created_at >= p_date_from)
                AND (p_date_to IS NULL OR created_at <= p_date_to)
                AND to_tsvector('english', title || ' ' || content) 
                    @@ plainto_tsquery('english', p_query_text)
        ),
        fused AS (
            SELECT 
                COALESCE(v.id, t.id) as id,
                COALESCE(v.source_type, r.source_type) as source_type,
                COALESCE(v.title, r.title) as title,
                COALESCE(v.content, r.content) as content,
                COALESCE(v.metadata, r.metadata) as metadata,
                COALESCE(v.vector_score, 0) as vector_score,
                COALESCE(t.text_score, 0) as text_score,
                COALESCE(1.0 / (60 + v.vector_rank), 0) + 
                COALESCE(1.0 / (60 + t.text_rank), 0) as rrf_score
            FROM vector_search v
            FULL OUTER JOIN text_search t ON v.id = t.id
            JOIN rag_documents r ON COALESCE(v.id, t.id) = r.id
        )
        SELECT 
            f.id,
            f.source_type,
            f.title,
            f.content,
            f.metadata,
            f.vector_score,
            f.text_score,
            f.rrf_score
        FROM fused f
        ORDER BY f.rrf_score DESC
        LIMIT p_limit;
    ELSE
        -- Chỉ vector search
        RETURN QUERY
        SELECT 
            id,
            source_type,
            title,
            content,
            metadata,
            1 - (embedding <=> p_query_embedding::vector) as vector_score,
            0.0 as text_score,
            1 - (embedding <=> p_query_embedding::vector) as rrf_score
        FROM rag_documents
        WHERE 
            (p_source_types IS NULL OR source_type = ANY(p_source_types))
            AND (p_date_from IS NULL OR created_at >= p_date_from)
            AND (p_date_to IS NULL OR created_at <= p_date_to)
            AND 1 - (embedding <=> p_query_embedding::vector) >= p_min_similarity
        ORDER BY embedding <=> p_query_embedding::vector
        LIMIT p_limit;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Create full-text search index
CREATE INDEX idx_rag_fts ON rag_documents 
    USING GIN (to_tsvector('english', title || ' ' || content));
```

### Example 2: A/B Testing Hybrid Search Strategies

```sql
-- System để test different hybrid strategies
CREATE TABLE search_experiments (
    id SERIAL PRIMARY KEY,
    experiment_name VARCHAR(100) NOT NULL,
    strategy JSONB NOT NULL,  -- strategy configuration
    traffic_percentage INTEGER DEFAULT 10,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE experiment_results (
    id BIGSERIAL PRIMARY KEY,
    experiment_id INTEGER REFERENCES search_experiments(id),
    strategy_name VARCHAR(100),
    query_id UUID DEFAULT gen_random_uuid(),
    user_id UUID,
    result_count INTEGER,
    click_position INTEGER,
    conversion_flag BOOLEAN,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Track search performance
CREATE OR REPLACE FUNCTION track_search_result(
    p_experiment_id INTEGER,
    p_strategy_name VARCHAR(100),
    p_user_id UUID,
    p_result_count INTEGER
) RETURNS UUID AS $$
DECLARE
    v_query_id UUID;
BEGIN
    v_query_id := gen_random_uuid();
    
    INSERT INTO experiment_results (
        experiment_id, strategy_name, query_id, user_id, result_count
    ) VALUES (
        p_experiment_id, p_strategy_name, v_query_id, p_user_id, p_result_count
    );
    
    RETURN v_query_id;
END;
$$ LANGUAGE plpgsql;

-- Record click
CREATE OR REPLACE FUNCTION record_click(
    p_query_id UUID,
    p_click_position INTEGER
) RETURNS VOID AS $$
BEGIN
    UPDATE experiment_results
    SET click_position = p_click_position
    WHERE query_id = p_query_id;
END;
$$ LANGUAGE plpgsql;

-- Analyze experiment results
CREATE OR REPLACE FUNCTION analyze_experiment(
    p_experiment_id INTEGER
) RETURNS TABLE(
    strategy_name VARCHAR(100),
    total_queries BIGINT,
    avg_results_per_query FLOAT,
    avg_click_position FLOAT,
    click_rate FLOAT,
    conversion_rate FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        er.strategy_name,
        COUNT(*)::bigint as total_queries,
        AVG(er.result_count)::float as avg_results,
        AVG(er.click_position)::float as avg_click_position,
        COUNT(er.click_position) * 100.0 / COUNT(*) as click_rate,
        COUNT(er.conversion_flag) * 100.0 / COUNT(*) as conversion_rate
    FROM experiment_results er
    WHERE er.experiment_id = p_experiment_id
    GROUP BY er.strategy_name
    ORDER BY conversion_rate DESC;
END;
$$ LANGUAGE plpgsql;
```

### Example 3: Real-time Search Ranking

```sql
-- Live search với multiple scoring factors
CREATE OR REPLACE FUNCTION live_hybrid_search(
    p_query_embedding REAL[],
    p_query_text TEXT,
    p_user_id UUID DEFAULT NULL,
    p_limit INTEGER DEFAULT 20
) RETURNS TABLE(
    id UUID,
    title TEXT,
    content_preview TEXT,
    combined_score FLOAT,
    score_breakdown JSONB
) AS $$
DECLARE
    v_user_preference_score FLOAT := 0;
    v_user_favorites INTEGER[] := '{}';
BEGIN
    -- Get user preferences if logged in
    IF p_user_id IS NOT NULL THEN
        SELECT favorite_categories INTO v_user_favorites
        FROM user_preferences
        WHERE user_id = p_user_id;
    END IF;
    
    RETURN QUERY
    WITH scored AS (
        SELECT 
            d.id,
            d.title,
            LEFT(d.content, 300) as content_preview,
            
            -- Vector similarity (0-1)
            (1 - (d.embedding <=> p_query_embedding::vector)) as vector_score,
            
            -- Text relevance (0-1)
            COALESCE(ts_rank(
                setweight(to_tsvector('english', d.title), 'A') ||
                setweight(to_tsvector('english', d.content), 'B'),
                plainto_tsquery('english', COALESCE(p_query_text, ''))
            ) / NULLIF(ts_rank(
                setweight(to_tsvector('english', d.title), 'A') ||
                setweight(to_tsvector('english', d.content), 'B'),
                plainto_tsquery('english', COALESCE(p_query_text, ''))
            ), 0), 0) as text_score,
            
            -- Recency (0-1, last 30 days)
            GREATEST(0, LEAST(1, 
                1 - EXTRACT(EPOCH FROM (NOW() - d.created_at)) / (30 * 24 * 60 * 60)
            )) as recency_score,
            
            -- Category preference (0-1)
            CASE 
                WHEN v_user_favorites = '{}' OR v_user_favorites IS NULL THEN 0.5
                WHEN d.category_id = ANY(v_user_favorites) THEN 1.0
                ELSE 0.0
            END as preference_score
    )
    SELECT 
        s.id,
        s.title,
        s.content_preview,
        -- Weighted combination
        (
            0.40 * s.vector_score +
            0.25 * LEAST(1, s.text_score * 10) +  -- Normalize text score
            0.20 * s.recency_score +
            0.15 * s.preference_score
        ) as combined_score,
        -- Score breakdown for debugging
        jsonb_build_object(
            'vector', ROUND(s.vector_score::numeric, 3),
            'text', ROUND(s.text_score::numeric, 3),
            'recency', ROUND(s.recency_score::numeric, 3),
            'preference', ROUND(s.preference_score::numeric, 3)
        ) as score_breakdown
    FROM scored s
    WHERE s.vector_score > 0.3  -- Minimum threshold
    ORDER BY combined_score DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;
```

## References

1. **pgvector Documentation**: https://github.com/pgvector/pgvector
2. **Reciprocal Rank Fusion**: https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
3. **Hybrid Search Patterns**: https://www.pg屋子里.com/blog/hybrid-search-with-pgvector
4. **PostgreSQL JSONB**: https://www.postgresql.org/docs/current/functions-json.html
5. **Cursor Enterprise Framework - Database Rules**: `.cursor/rules/pgvector.mdc`
