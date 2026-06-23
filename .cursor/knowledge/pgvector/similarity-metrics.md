---
title: "Similarity Metrics in pgvector"
description: "Hướng dẫn về các metrics đo lường similarity trong pgvector: cosine similarity, L2 distance, inner product, và strategies cho việc lựa chọn metric phù hợp"
tags: ["similarity", "cosine", "l2", "inner-product", "pgvector", "distance-metrics"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Similarity Metrics in pgvector

## Tổng Quan

Việc lựa chọn đúng similarity metric là yếu tố then chốt quyết định chất lượng của vector search results. pgvector hỗ trợ bốn distance operators chính, mỗi loại phù hợp với các loại dữ liệu và use cases khác nhau.

Understanding khi nào nên sử dụng cosine similarity thay vì L2 distance, hoặc inner product thay vì negative inner product, sẽ giúp developers tối ưu hóa search quality và performance cho ứng dụng cụ thể của mình.

Ngoài ra, việc hiểu rõ cách normalize vectors và các trade-offs giữa different metrics sẽ giúp architect đưa ra quyết định thiết kế đúng đắn ngay từ đầu, tránh phải re-index dữ liệu sau này.

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức toàn diện về các similarity metrics trong pgvector:

Đầu tiên, chúng ta sẽ tìm hiểu chi tiết về từng metric: cosine similarity, L2 distance (Euclidean), và inner product. Mỗi metric sẽ được phân tích về công thức toán học, ý nghĩa, và trường hợp sử dụng.

Thứ hai, tài liệu hướng dẫn cách lựa chọn metric phù hợp dựa trên loại dữ liệu và embedding model đang sử dụng.

Thứ ba, chúng ta sẽ đề cập đến các chiến lược normalization để đảm bảo vectors được so sánh một cách chính xác và nhất quán.

Cuối cùng, tài liệu cung cấp các best practices và code examples để implement đúng các similarity computations trong production systems.

## Key Concepts

### 1. Cosine Similarity

Cosine similarity đo lường góc giữa hai vectors, bất kể độ dài của chúng. Giá trị range từ -1 (ngược hướng hoàn toàn) đến 1 (cùng hướng hoàn toàn).

```
cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)
```

#### Công Thức pgvector

pgvector sử dụng `<=>` operator cho cosine distance (không phải similarity):

```sql
-- Cosine distance operator: <=>
-- Cosine similarity = 1 - cosine_distance

SELECT 
    id,
    embedding,
    embedding <=> $query_embedding AS cosine_distance,
    1 - (embedding <=> $query_embedding) AS cosine_similarity
FROM items
ORDER BY embedding <=> $query_embedding
LIMIT 10;
```

#### Khi Nào Sử Dụng Cosine Similarity

```sql
-- Phù hợp khi:
-- 1. Documents có độ dài khác nhau (text embeddings)
-- 2. Cần semantic similarity thay vì magnitude
-- 3. Sử dụng models như OpenAI, sentence-transformers

-- Example: Text search với varying document lengths
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1536) NOT NULL
);

-- Search không cần normalize vì cosine similarity tự handle
SELECT 
    id,
    title,
    1 - (embedding <=> $query_embedding) AS similarity
FROM documents
WHERE title ILIKE '%' || $keyword || '%'
ORDER BY embedding <=> $query_embedding
LIMIT 10;
```

### 2. L2 Distance (Euclidean Distance)

L2 distance đo lường khoảng cách Euclidean giữa hai điểm trong không gian vector. Đây là khoảng cách "thẳng" giữa hai vectors.

```
L2(A, B) = sqrt(Σ(Ai - Bi)²)
```

#### Công Thức pgvector

pgvector sử dụng `<->` operator cho L2 distance:

```sql
-- L2 distance operator: <->
SELECT 
    id,
    embedding,
    embedding <-> $query_embedding AS l2_distance
FROM items
ORDER BY embedding <-> $query_embedding
LIMIT 10;
```

#### Khi Nào Sử Dụng L2 Distance

```sql
-- Phù hợp khi:
-- 1. Cần đo "độ gần" tuyệt đối trong không gian
-- 2. Image embeddings (CNN-based)
-- 3. Audio embeddings
-- 4. Khi vectors đã được normalized

-- Example: Image similarity search
CREATE TABLE images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    image_url VARCHAR(1000),
    embedding VECTOR(2048) NOT NULL,  -- ResNet, VGG embeddings
    category VARCHAR(100)
);

-- Tìm ảnh tương tự
SELECT 
    id,
    image_url,
    embedding <-> $query_embedding AS l2_distance
FROM images
WHERE category = $category
ORDER BY embedding <-> $query_embedding
LIMIT 10;
```

### 3. Inner Product

Inner product (dot product) là tổng của các phép nhân element-wise. Khi vectors được normalized, inner product tương đương với cosine similarity.

```
IP(A, B) = Σ(Ai × Bi)
```

#### Công Thức pgvector

pgvector sử dụng `<#>` operator cho inner product distance (negative inner product):

```sql
-- Inner product distance operator: <#>
-- Inner product similarity = -1 * inner_product_distance

SELECT 
    id,
    embedding,
    embedding <#> $query_embedding AS neg_inner_product,
    -1 * (embedding <#> $query_embedding) AS inner_product
FROM items
ORDER BY embedding <#> $query_embedding
LIMIT 10;
```

#### Khi Nào Sử Dụng Inner Product

```sql
-- Phù hợp khi:
-- 1. Unnormalized embeddings từ neural networks
-- 2. Collaborative filtering
-- 3. Khi muốn penalize vectors có magnitude lớn
-- 4. Sử dụng với <+> operator cho positive inner product

-- Example: Recommendation system với unnormalized embeddings
CREATE TABLE user_item_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type VARCHAR(20) NOT NULL,  -- 'user' hoặc 'item'
    entity_id UUID NOT NULL,
    embedding VECTOR(128) NOT NULL
);

-- Tính recommendation score
SELECT 
    u.entity_id as user_id,
    i.entity_id as item_id,
    -1 * (u.embedding <#> i.embedding) AS recommendation_score
FROM user_embeddings u
CROSS JOIN LATERAL (
    SELECT entity_id, embedding
    FROM user_item_embeddings
    WHERE entity_type = 'item'
) i
WHERE u.entity_id = $user_id
ORDER BY u.embedding <#> i.embedding
LIMIT 20;
```

### 4. Negative Inner Product (<+>)

pgvector cũng hỗ trợ `<+>` operator cho positive inner product, tiện lợi khi muốn ORDER BY inner product mà không cần negate.

```sql
-- <+> là positive inner product (không cần negate)
SELECT 
    id,
    embedding,
    embedding <+> $query_embedding AS positive_inner_product
FROM items
ORDER BY embedding <+> $query_embedding
LIMIT 10;

-- Kết quả tương đương với:
-- ORDER BY -1 * (embedding <#> $query_embedding)
```

## Metric Selection Guide

### So Sánh Các Metrics

| Metric | Operator | Range | Best For | Characteristics |
|--------|----------|-------|----------|------------------|
| Cosine Distance | `<=>` | [0, 2] | Text, semantic | Orientation-focused |
| L2 Distance | `<->` | [0, ∞) | Images, audio | Magnitude-sensitive |
| Negative IP | `<#>` | [-∞, ∞) | Unnormalized NN | Magnitude-weighted |
| Positive IP | `<+>` | [-∞, ∞) | Same as above | Convenience syntax |

### Decision Tree cho Metric Selection

```
Is your embedding model already normalized?
├── Yes: Cosine = L2 = IP (any works)
└── No: 
    ├── Text/Semantic Search?
    │   └── Yes: Cosine Similarity
    ├── Image/Audio Embeddings?
    │   └── Yes: L2 Distance
    └── Collaborative Filtering?
        └── Yes: Inner Product
```

### Model-specific Recommendations

```sql
-- OpenAI text-embedding-3 models: normalized by default
-- Cosine similarity recommended

-- OpenAI ada-002: NOT normalized
-- Cosine similarity recommended OR normalize before storage

-- Sentence-transformers: normalized by default
-- Cosine similarity recommended

-- ResNet/VGG image embeddings: NOT normalized
-- L2 distance recommended

-- CLIP image-text embeddings: normalized
-- Cosine similarity recommended

-- word2vec/GloVe: NOT normalized
-- Cosine similarity recommended
```

## Normalization Strategies

### 1. Pre-normalization (Storage-time)

Normalize vectors trước khi lưu vào database để đảm bảo consistency và có thể sử dụng bất kỳ metric nào.

```sql
-- Function để normalize vector
CREATE OR REPLACE FUNCTION normalize_vector(v REAL[])
RETURNS REAL[] AS $$
DECLARE
    norm REAL;
BEGIN
    norm := sqrt((SELECT sum(x * x) FROM unnest(v) AS x));
    IF norm = 0 THEN
        RETURN v;  -- Return as-is if zero vector
    END IF;
    RETURN (SELECT array_agg(x / norm) FROM unnest(v) AS x);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Tạo table với pre-normalized vectors
CREATE TABLE normalized_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    original_embedding VECTOR(1536) NOT NULL,
    normalized_embedding VECTOR(1536) GENERATED ALWAYS AS (
        (SELECT normalize_vector(original_embedding::real[]))::vector
    ) STORED
);

-- Index on normalized embedding
CREATE INDEX idx_normalized_hnsw ON normalized_embeddings 
    USING hnsw (normalized_embedding vector_cosine_ops);
```

### 2. Post-normalization (Query-time)

Normalize vectors tại query time khi retrieval.

```sql
-- Normalize tại query time
SELECT 
    id,
    embedding,
    -- Normalize query vector
    (embedding <=> (
        SELECT normalize_vector($1::real[])::vector
    )) AS cosine_distance
FROM items
ORDER BY embedding <=> (
    SELECT normalize_vector($1::real[])::vector
)
LIMIT 10;

-- Performance note: Query-time normalization có thể chậm hơn
-- vì không thể tận dụng pre-computed values
```

### 3. Batch Normalization

```sql
-- Normalize all vectors in table
UPDATE embeddings
SET embedding = normalize_vector(embedding::real[])::vector;

-- Verify normalization
SELECT 
    MIN((SELECT sqrt(sum(x*x)) FROM unnest(embedding::real[]) AS x)) as min_norm,
    MAX((SELECT sqrt(sum(x*x)) FROM unnest(embedding::real[]) AS x)) as max_norm
FROM embeddings;

-- Norm should be 1.0 for all vectors after normalization
```

## Best Practices

### 1. Consistent Metric Usage

```sql
-- LUÔN sử dụng cùng một metric cho cả storage và retrieval
-- Bad practice: Store with L2, search with Cosine

-- Good practice: Consistent metric throughout

-- Table definition
CREATE TABLE items (
    id UUID PRIMARY KEY,
    embedding VECTOR(1536) NOT NULL
);

-- Index sử dụng cosine operator class
CREATE INDEX idx_items_cosine ON items 
    USING hnsw (embedding vector_cosine_ops);

-- Search sử dụng cosine distance
SELECT * FROM items 
ORDER BY embedding <=> $query_embedding 
LIMIT 10;

-- Hoặc nếu dùng L2:
CREATE INDEX idx_items_l2 ON items 
    USING hnsw (embedding vector_l2_ops);

SELECT * FROM items 
ORDER BY embedding <-> $query_embedding 
LIMIT 10;
```

### 2. Handling Edge Cases

```sql
-- Check for zero vectors
SELECT COUNT(*) FROM items 
WHERE (SELECT sum(x*x) FROM unnest(embedding::real[]) AS x) = 0;

-- Handle zero vectors
DELETE FROM items 
WHERE (SELECT sum(x*x) FROM unnest(embedding::real[]) AS x) = 0;

-- Check for NaN or Inf values
SELECT COUNT(*) FROM items 
WHERE embedding::text LIKE '%NaN%' 
   OR embedding::text LIKE '%Inf%';

-- Fix NaN/Inf by replacing with zero vector
UPDATE items
SET embedding = array_to_vector(
    array_fill(0::real, ARRAY[1536])
)::vector
WHERE embedding::text LIKE '%NaN%' 
   OR embedding::text LIKE '%Inf%';
```

### 3. Combining Multiple Metrics

```sql
-- Weighted combination của nhiều metrics
CREATE OR REPLACE FUNCTION multi_metric_search(
    p_query_embedding REAL[],
    p_weights JSONB DEFAULT '{"cosine": 0.5, "l2": 0.3, "ip": 0.2}'::jsonb
) RETURNS TABLE(
    id UUID,
    combined_score FLOAT,
    metrics JSONB
) AS $$
DECLARE
    v_cosine_weight FLOAT := (p_weights->>'cosine')::float;
    v_l2_weight FLOAT := (p_weights->>'l2')::float;
    v_ip_weight FLOAT := (p_weights->>'ip')::float;
BEGIN
    RETURN QUERY
    SELECT 
        id,
        -- Normalize each metric và combine
        (
            v_cosine_weight * (1 - (embedding <=> p_query_embedding::vector)) +
            v_l2_weight * (1 - LEAST(1, (embedding <-> p_query_embedding::vector) / 100)) +
            v_ip_weight * (-1 * (embedding <#> p_query_embedding::vector))
        ) as combined_score,
        jsonb_build_object(
            'cosine', 1 - (embedding <=> p_query_embedding::vector),
            'l2', embedding <-> p_query_embedding::vector,
            'inner_product', -1 * (embedding <#> p_query_embedding::vector)
        ) as metrics
    FROM items
    ORDER BY combined_score DESC
    LIMIT 20;
END;
$$ LANGUAGE plpgsql;
```

## Common Patterns

### Pattern 1: Similarity-based Filtering

```sql
-- Filter results dựa trên minimum similarity threshold
CREATE OR REPLACE FUNCTION similar_items_filtered(
    p_query_embedding REAL[],
    p_min_similarity FLOAT DEFAULT 0.7,
    p_category VARCHAR DEFAULT NULL
) RETURNS TABLE(
    id UUID,
    title TEXT,
    similarity FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.id,
        i.title,
        1 - (i.embedding <=> p_query_embedding::vector) AS similarity
    FROM items i
    WHERE 
        -- Similarity threshold
        1 - (i.embedding <=> p_query_embedding::vector) >= p_min_similarity
        -- Optional category filter
        AND (p_category IS NULL OR i.category = p_category)
    ORDER BY i.embedding <=> p_query_embedding::vector;
END;
$$ LANGUAGE plpgsql;
```

### Pattern 2: k-NN with Distance Cutoff

```sql
-- Find k nearest neighbors với maximum distance threshold
CREATE OR REPLACE FUNCTION knn_with_cutoff(
    p_query_embedding REAL[],
    p_k INTEGER DEFAULT 10,
    p_max_distance FLOAT DEFAULT 0.5
) RETURNS TABLE(
    id UUID,
    title TEXT,
    distance FLOAT,
    rank BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        id,
        title,
        embedding <=> p_query_embedding::vector AS distance,
        ROW_NUMBER() OVER (ORDER BY embedding <=> p_query_embedding::vector) AS rank
    FROM items
    WHERE embedding <=> p_query_embedding::vector <= p_max_distance
    ORDER BY embedding <=> p_query_embedding::vector
    LIMIT p_k;
END;
$$ LANGUAGE plpgsql;
```

### Pattern 3: Diversity Search

```sql
-- Tìm diverse set of results (MMR - Maximal Marginal Relevance)
CREATE OR REPLACE FUNCTION diverse_search(
    p_query_embedding REAL[],
    p_lambda FLOAT DEFAULT 0.5,  -- Trade-off between relevance và diversity
    p_limit INTEGER DEFAULT 10
) RETURNS TABLE(
    id UUID,
    title TEXT,
    relevance FLOAT,
    diversity_bonus FLOAT,
    mmr_score FLOAT
) AS $$
DECLARE
    v_selected_ids UUID[] := '{}';
    v_candidate_id UUID;
    v_min_distance FLOAT;
BEGIN
    -- Iteratively select diverse items
    FOR v_candidate_id IN (
        SELECT id FROM items
        WHERE id != ALL(v_selected_ids)
        ORDER BY embedding <=> p_query_embedding::vector
        LIMIT 100  -- Consider top 100 candidates
    )
    LOOP
        IF array_length(v_selected_ids, 1) >= p_limit THEN
            EXIT;
        END IF;
        
        -- Calculate minimum distance to selected items
        SELECT MIN(embedding <=> e.embedding)
        INTO v_min_distance
        FROM items e
        WHERE e.id = ANY(v_selected_ids);
        
        -- MMR score = relevance + lambda * diversity
        INSERT INTO selected_results (id, title, relevance, diversity_bonus, mmr_score)
        SELECT 
            c.id,
            c.title,
            1 - (c.embedding <=> p_query_embedding::vector) AS relevance,
            COALESCE(v_min_distance, 1) AS diversity_bonus,
            (
                (1 - p_lambda) * (1 - (c.embedding <=> p_query_embedding::vector)) +
                p_lambda * COALESCE(v_min_distance, 1)
            ) AS mmr_score
        FROM items c
        WHERE c.id = v_candidate_id
        ORDER BY mmr_score DESC
        LIMIT 1;
        
        v_selected_ids := array_append(v_selected_ids, v_candidate_id);
    END LOOP;
    
    RETURN QUERY SELECT * FROM selected_results ORDER BY mmr_score DESC;
END;
$$ LANGUAGE plpgsql;
```

## Troubleshooting

### Vấn Đề 1: Unexpected Ranking Results

```sql
-- Debug: Kiểm tra distribution của distances
SELECT 
    AVG(embedding <=> $1::vector) as avg_distance,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY embedding <=> $1::vector) as median_distance,
    MIN(embedding <=> $1::vector) as min_distance,
    MAX(embedding <=> $1::vector) as max_distance
FROM items;

-- Kiểm tra xem query vector có được normalize đúng không
SELECT 
    (SELECT sqrt(sum(x*x)) FROM unnest($1::real[]) AS x) as query_norm,
    (SELECT sqrt(sum(x*x)) FROM unnest(embedding::real[]) AS x) as avg_embedding_norm
FROM items
LIMIT 1;
```

### Vấn Đề 2: Inconsistent Results Across Models

```sql
-- Verify embedding dimension consistency
SELECT 
    array_length(embedding::real[], 1) as dim,
    COUNT(*) as count
FROM items
GROUP BY array_length(embedding::real[], 1);

-- Check embedding value ranges
SELECT 
    MIN(unnest) as min_val,
    MAX(unnest) as max_val,
    AVG(unnest) as avg_val
FROM (
    SELECT embedding::real[] as arr FROM items
) t,
unnest(t.arr);
```

### Vấn Đề 3: Performance với Large Dimensions

```sql
-- For very high dimensions (>2048), consider dimensionality reduction
-- sử dụng PCA hoặc truncation

-- Option 1: Truncate dimensions
UPDATE embeddings
SET embedding = (
    SELECT array_to_vector(array[:target_dimensions])
)::vector
WHERE array_length(embedding::real[], 1) > :target_dimensions;

-- Option 2: Use approximate L2 for high-dimensional data
SET enable_seqscan = off;  -- Force index usage

-- Option 3: Quantization for faster computation
ALTER INDEX idx_items_hnsw SET (pq_dim = 64);
```

## Examples

### Example 1: Complete Similarity Search System

```sql
-- Setup complete similarity search system
CREATE EXTENSION IF NOT EXISTS vector;

-- Create embeddings table
CREATE TABLE product_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id),
    product_name VARCHAR(500) NOT NULL,
    description TEXT,
    embedding VECTOR(1536) NOT NULL,
    model_name VARCHAR(100) NOT NULL,  -- Track which model generated this
    embedding_version INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE (product_id, embedding_version)
);

-- Indexes for different metrics
CREATE INDEX idx_product_cosine ON product_embeddings 
    USING hnsw (embedding vector_cosine_ops);

-- Verify embeddings are normalized
CREATE OR REPLACE FUNCTION verify_normalization()
RETURNS TABLE(
    is_normalized BOOLEAN,
    min_norm REAL,
    max_norm REAL,
    count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*) FILTER (
            WHERE ABS(1 - (SELECT sqrt(sum(x*x)) 
                          FROM unnest(embedding::real[]) AS x))
        ) = 0 as is_normalized,
        MIN((SELECT sqrt(sum(x*x)) FROM unnest(embedding::real[]) AS x)) as min_norm,
        MAX((SELECT sqrt(sum(x*x)) FROM unnest(embedding::real[]) AS x)) as max_norm,
        COUNT(*) as total_count
    FROM product_embeddings;
END;
$$ LANGUAGE plpgsql;

-- Unified search function
CREATE OR REPLACE FUNCTION search_products(
    p_query_embedding REAL[],
    p_metric VARCHAR DEFAULT 'cosine',  -- 'cosine', 'l2', 'ip'
    p_min_similarity FLOAT DEFAULT 0.5,
    p_limit INTEGER DEFAULT 20
) RETURNS TABLE(
    product_id UUID,
    product_name TEXT,
    description TEXT,
    score FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        pe.product_id,
        pe.product_name,
        LEFT(pe.description, 200) as description,
        CASE p_metric
            WHEN 'cosine' THEN 1 - (pe.embedding <=> p_query_embedding::vector)
            WHEN 'l2' THEN 1 / (1 + (pe.embedding <-> p_query_embedding::vector))
            WHEN 'ip' THEN -1 * (pe.embedding <#> p_query_embedding::vector)
            ELSE 1 - (pe.embedding <=> p_query_embedding::vector)
        END as score
    FROM product_embeddings pe
    WHERE 
        -- Apply threshold
        CASE p_metric
            WHEN 'cosine' THEN 1 - (pe.embedding <=> p_query_embedding::vector) >= p_min_similarity
            WHEN 'l2' THEN 1 / (1 + (pe.embedding <-> p_query_embedding::vector)) >= p_min_similarity
            WHEN 'ip' THEN -1 * (pe.embedding <#> p_query_embedding::vector) >= p_min_similarity
            ELSE TRUE
        END
    ORDER BY 
        CASE p_metric
            WHEN 'cosine' THEN pe.embedding <=> p_query_embedding::vector
            WHEN 'l2' THEN pe.embedding <-> p_query_embedding::vector
            WHEN 'ip' THEN pe.embedding <#> p_query_embedding::vector
        END
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;
```

### Example 2: Cross-model Embedding Comparison

```sql
-- Store embeddings from multiple models
CREATE TABLE multi_model_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id UUID NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    embedding VECTOR(1536) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE (entity_id, entity_type, model_name)
);

-- Compare similarity across models
CREATE OR REPLACE FUNCTION cross_model_similarity(
    p_entity_id UUID,
    p_entity_type VARCHAR,
    p_query_embedding REAL[]
) RETURNS TABLE(
    model_name VARCHAR(100),
    cosine_similarity FLOAT,
    rank INTEGER
) AS $$
BEGIN
    RETURN QUERY
    WITH similarities AS (
        SELECT 
            model_name,
            1 - (embedding <=> p_query_embedding::vector) as cosine_similarity
        FROM multi_model_embeddings
        WHERE entity_id = p_entity_id
          AND entity_type = p_entity_type
    )
    SELECT 
        s.model_name,
        s.cosine_similarity,
        ROW_NUMBER() OVER (ORDER BY s.cosine_similarity DESC)::integer as rank
    FROM similarities s;
END;
$$ LANGUAGE plpgsql;

-- Aggregate similarity across models (ensemble)
CREATE OR REPLACE FUNCTION ensemble_similarity(
    p_query_embedding REAL[],
    p_entity_id UUID,
    p_entity_type VARCHAR
) RETURNS FLOAT AS $$
DECLARE
    v_avg_similarity FLOAT;
BEGIN
    SELECT AVG(1 - (embedding <=> p_query_embedding::vector))
    INTO v_avg_similarity
    FROM multi_model_embeddings
    WHERE entity_id = p_entity_id
      AND entity_type = p_entity_type;
    
    RETURN v_avg_similarity;
END;
$$ LANGUAGE plpgsql;
```

### Example 3: Recommendation with Implicit Feedback

```sql
-- Collaborative filtering với implicit feedback
CREATE TABLE user_item_interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    item_id UUID NOT NULL,
    interaction_type VARCHAR(50) NOT NULL,  -- 'view', 'click', 'purchase'
    weight FLOAT DEFAULT 1.0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE (user_id, item_id, interaction_type)
);

CREATE TABLE collaborative_embeddings (
    user_id UUID PRIMARY KEY,
    embedding VECTOR(64) NOT NULL,  -- Learned embeddings
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Predict user preference
CREATE OR REPLACE FUNCTION predict_preference(
    p_user_id UUID,
    p_item_id UUID
) RETURNS FLOAT AS $$
DECLARE
    v_user_embedding VECTOR(64);
    v_item_embedding VECTOR(64);
BEGIN
    SELECT embedding INTO v_user_embedding
    FROM collaborative_embeddings
    WHERE user_id = p_user_id;
    
    -- Item embeddings stored separately
    SELECT embedding INTO v_item_embedding
    FROM item_embeddings
    WHERE item_id = p_item_id;
    
    IF v_user_embedding IS NULL OR v_item_embedding IS NULL THEN
        RETURN 0;
    END IF;
    
    -- Inner product as prediction score
    RETURN -1 * (v_user_embedding <#> v_item_embedding);
END;
$$ LANGUAGE plpgsql;

-- Find items for user (recommendation)
CREATE OR REPLACE FUNCTION recommend_for_user(
    p_user_id UUID,
    p_exclude_viewed BOOLEAN DEFAULT TRUE,
    p_limit INTEGER DEFAULT 20
) RETURNS TABLE(
    item_id UUID,
    predicted_score FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ie.item_id,
        predict_preference(p_user_id, ie.item_id) as predicted_score
    FROM item_embeddings ie
    WHERE 
        -- Exclude items user has already interacted with
        (NOT p_exclude_viewed OR ie.item_id NOT IN (
            SELECT item_id FROM user_item_interactions
            WHERE user_id = p_user_id
        ))
    ORDER BY predict_preference(p_user_id, ie.item_id) DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;
```

## References

1. **pgvector Documentation**: https://github.com/pgvector/pgvector
2. **Cosine Similarity**: https://en.wikipedia.org/wiki/Cosine_similarity
3. **Euclidean Distance**: https://en.wikipedia.org/wiki/Euclidean_distance
4. **Inner Product**: https://en.wikipedia.org/wiki/Inner_product_space
5. **Embedding Normalization**: https://txt.cohere.com/sentence-embeddings/
6. **Cursor Enterprise Framework - Database Rules**: `.cursor/rules/pgvector.mdc`
