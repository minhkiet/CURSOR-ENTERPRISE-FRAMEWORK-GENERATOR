---
title: "Vector Indexing - ivfflat vs HNSW"
description: "Hướng dẫn chi tiết về các phương pháp indexing vector trong pgvector: ivfflat và HNSW, build parameters, PQ compression và index selection guide"
tags: ["pgvector", "indexing", "hnsw", "ivfflat", "postgresql", "vector-search"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Vector Indexing - ivfflat vs HNSW

## Tổng Quan

Việc lựa chọn đúng thuật toán indexing vector là yếu tố then chốt quyết định hiệu suất của hệ thống vector search. Trong pgvector, chúng ta có hai phương pháp indexing chính: **IVFFlat** và **HNSW** (Hierarchical Navigable Small World). Mỗi phương pháp có những đặc điểm riêng biệt về hiệu suất, độ chính xác và resource requirements.

IVFFlat (Inverted File Flat) là phương pháp clustering-based indexing, phù hợp với những bộ dữ liệu lớn và khi cần balance giữa tốc độ và độ chính xác. HNSW là phương pháp graph-based indexing, mang lại hiệu suất tìm kiếm vượt trội nhưng đòi hỏi nhiều bộ nhớ hơn.

Việc hiểu rõ cơ chế hoạt động, các tham số build và trường hợp sử dụng của từng phương pháp sẽ giúp kiến trúc sư và developer đưa ra quyết định tối ưu cho từng use case cụ thể trong hệ thống enterprise.

## Mục Đích

Tài liệu này nhằm mục đích cung cấp kiến thức chuyên sâu về các phương pháp vector indexing trong pgvector, bao gồm:

Thứ nhất, giúp người đọc hiểu rõ cơ chế hoạt động của IVFFlat và HNSW ở mức algorithmic. Việc nắm vững cách các thuật toán này tổ chức và tìm kiếm vector sẽ giúp developer hiểu được trade-offs giữa các phương pháp.

Thứ hai, tài liệu hướng dẫn cách tối ưu các build parameters cho từng loại index. Việc tuning đúng parameters có thể cải thiện đáng kể cả hiệu suất lẫn độ chính xác của vector search.

Thứ ba, chúng ta sẽ đề cập đến PQ compression (Product Quantization) như một phương pháp giảm kích thước index và tăng tốc độ tìm kiếm, đồng thời cũng có những đánh đổi về độ chính xác.

Cuối cùng, tài liệu cung cấp index selection guide dựa trên các tiêu chí cụ thể như dataset size, latency requirements, memory constraints và accuracy requirements.

## Key Concepts

### 1. IVFFlat Index

IVFFlat là thuật toán clustering-based indexing hoạt động theo nguyên tắc phân cụm các vectors vào các clusters và chỉ tìm kiếm trong các clusters gần nhất với query vector.

#### Cơ Chế Hoạt Động

IVFFlat sử dụng k-means clustering để phân chia tập vectors thành N clusters. Mỗi vector được gán vào cluster có centroid gần nhất. Khi tìm kiếm, thuật toán chỉ kiểm tra các clusters có khả năng chứa kết quả cao nhất thay vì duyệt toàn bộ dataset.

Điều này giúp giảm đáng kể số lượng so sánh cần thiết, từ O(N) xuống còn O(N/K + K) trong đó K là số lượng clusters được khảo sát.

```sql
-- Tạo IVFFlat index với số lists = 100
CREATE INDEX ON items 
USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 100);
```

#### Build Parameters

Việc lựa chọn số lượng lists (clusters) là quan trọng nhất trong IVFFlat. Công thức thực nghiệm:

- Small datasets (<100K vectors): lists = sqrt(N) * 4
- Medium datasets (100K - 1M vectors): lists = sqrt(N)
- Large datasets (>1M vectors): lists = sqrt(N) / 2

```sql
-- Dataset có 1 triệu vectors
CREATE INDEX idx_embedding_ivf 
ON items USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 1000);
```

#### Probes Parameter

Tham số `probes` kiểm soát số lượng clusters được khảo sát khi tìm kiếm. Giá trị mặc định là 1, nhưng có thể tăng để cải thiện recall:

```sql
-- Tăng probes để cải thiện recall
SET hnsw.nprobe = 10;
SET ivfflat.probes = 10;

SELECT id, name, 1 - (embedding <=> $query_embedding) AS similarity
FROM items
ORDER BY embedding <=> $query_embedding
LIMIT 10;
```

### 2. HNSW Index

HNSW (Hierarchical Navigable Small World) là thuật toán graph-based indexing sử dụng cấu trúc multi-layer graph để tìm kiếm nearest neighbors nhanh chóng.

#### Cơ Chế Hoạt Động

HNSW xây dựng một cấu trúc hierarchical gồm nhiều layers, mỗi layer là một navigable small world graph. Layer trên cùng có ít nodes hơn nhưng kết nối xa hơn, layer dưới cùng chứa tất cả các vectors với kết nối cục bộ.

```sql
-- Tạo HNSW index
CREATE INDEX idx_embedding_hnsw 
ON items USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 200);
```

#### Build Parameters

| Parameter | Mô Tả | Giá Trị Đề Xuất | Ảnh Hưởng |
|-----------|--------|-----------------|-----------|
| `m` | Số lượng connections tối đa mỗi node | 8-64 | Cao hơn = chính xác hơn, chậm hơn |
| `ef_construction` | Kích thước dynamic list khi build | 64-400 | Cao hơn = chính xác hơn, build chậm hơn |

```sql
-- HNSW với parameters tối ưu cho high recall
CREATE INDEX idx_embedding_hnsw_high_recall 
ON items USING hnsw (embedding vector_cosine_ops) 
WITH (m = 32, ef_construction = 400);

-- HNSW với parameters cho high throughput
CREATE INDEX idx_embedding_hnsw_high_throughput 
ON items USING hnsw (embedding vector_cosine_ops) 
WITH (m = 12, ef_construction = 128);
```

#### Search Parameters

```sql
-- Tăng ef_search để cải thiện recall
SET hnsw.ef_search = 100;

SELECT id, name, 1 - (embedding <=> $query_embedding) AS similarity
FROM items
ORDER BY embedding <=> $query_embedding
LIMIT 10;
```

### 3. Product Quantization (PQ) Compression

PQ là kỹ thuật nén vector bằng cách chia vector thành các subvectors và lượng tử hóa mỗi phần riêng biệt.

```sql
-- pgvector hỗ trợ PQ với số bytes thấp hơn
CREATE INDEX idx_embedding_pq 
ON items USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 200, pq_dim = 32);
```

PQ compression giảm kích thước index đáng kể (ví dụ: 1536 dimensions float32 -> 64 bytes với pq_dim = 64) nhưng cũng giảm độ chính xác của kết quả tìm kiếm.

## So Sánh IVFFlat vs HNSW

| Tiêu Chí | IVFFlat | HNSW |
|----------|---------|------|
| Build Time | Nhanh | Chậm |
| Search Speed | Trung bình | Rất nhanh |
| Memory Usage | Thấp | Cao |
| Recall | Phụ thuộc vào probes | Cao ngay cả với ef_search mặc định |
| Update Performance | Tốt hơn | Kém hơn |
| Scalability | Tốt cho dataset lớn | Memory-bound |

```sql
-- So sánh hiệu suất
EXPLAIN ANALYZE
SELECT id FROM items 
ORDER BY embedding <=> $query_embedding 
LIMIT 100;
```

## Best Practices

### 1. Lựa Chọn Index Theo Use Case

```sql
-- Use case: Real-time search với latency thấp
-- Recommendation: HNSW với ef_search = 100-200
CREATE INDEX idx_realtime ON items 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 200);

-- Use case: Batch processing với dataset lớn
-- Recommendation: IVFFlat với số lists phù hợp
CREATE INDEX idx_batch ON items 
USING ivfflat (embedding vector_cosine_ops) 
WITH (lists = 10000);

-- Use case: Memory-constrained environment
-- Recommendation: IVFFlat hoặc HNSW với PQ
CREATE INDEX idx_memory ON items 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 8, ef_construction = 64, pq_dim = 32);
```

### 2. Tối Ưu Build Parameters

```sql
-- Dataset analysis trước khi build index
SELECT 
    COUNT(*) as total_vectors,
    COUNT(DISTINCT LEFT(embedding::text, 100)) as unique_batches
FROM items;

-- Batch insert để improve index quality
INSERT INTO items (embedding, name)
SELECT embedding, name FROM staging_table;

-- Sau khi insert xong, trigger index rebuild nếu cần
REINDEX INDEX idx_embedding_hnsw;
```

### 3. Kết Hợp Vector Index với SQL Filters

```sql
-- Sử dụng index cho vector search, sau đó filter
CREATE INDEX idx_embedding_hnsw ON items 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 200);

CREATE INDEX idx_category ON items (category_id);

-- Query: tìm similar products trong category cụ thể
SELECT id, name, 1 - (embedding <=> $query_embedding) AS similarity
FROM items
WHERE category_id = $category_id
ORDER BY embedding <=> $query_embedding
LIMIT 20;
```

## Common Patterns

### Pattern 1: Hybrid Search với Pre-filtering

```sql
-- Pre-filter sử dụng index scan
SET enable_seqscan = off;

SELECT id, name, 
       1 - (embedding <=> $query_embedding) AS similarity
FROM items
WHERE status = 'active' 
  AND category_id = ANY($allowed_categories)
ORDER BY embedding <=> $query_embedding
LIMIT 50;
```

### Pattern 2: ANN Search với Fallback

```sql
-- Sử dụng ANN index nhưng fallback sang exact search nếu cần
SET hnsw.ef_search = 100;

WITH ann_results AS (
    SELECT id, name, 
           1 - (embedding <=> $query_embedding) AS similarity
    FROM items
    WHERE is_deleted = false
    ORDER BY embedding <=> $query_embedding
    LIMIT 100
)
SELECT * FROM ann_results
UNION ALL
SELECT id, name, 
       1 - (embedding <=> $query_embedding) AS similarity
FROM items
WHERE is_deleted = false
  AND id NOT IN (SELECT id FROM ann_results)
ORDER BY similarity DESC
LIMIT 100;
```

### Pattern 3: Approximate k-NN với Confidence Score

```sql
-- Tính confidence dựa trên similarity gap
WITH ranked_results AS (
    SELECT id, name,
           1 - (embedding <=> $query_embedding) AS similarity,
           ROW_NUMBER() OVER (ORDER BY embedding <=> $query_embedding) as rank
    FROM items
    WHERE category_id = $category_id
)
SELECT id, name, similarity,
       CASE 
           WHEN rank = 1 THEN 'HIGH'
           WHEN similarity > (SELECT similarity FROM ranked_results WHERE rank = 1) - 0.1 
           THEN 'MEDIUM'
           ELSE 'LOW'
       END as confidence
FROM ranked_results
WHERE rank <= 20;
```

## Troubleshooting

### Vấn Đề 1: Index Không Được Sử Dụng

```sql
-- Kiểm tra xem index có tồn tại không
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'items';

-- Kiểm tra xem planner có sử dụng index không
EXPLAIN SELECT id FROM items 
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector;

-- Force sử dụng index
SET enable_seqscan = off;
```

### Vấn Đề 2: Recall Thấp

```sql
-- Tăng ef_search cho HNSW
SET hnsw.ef_search = 500;

-- Hoặc tăng probes cho IVFFlat
SET ivfflat.probes = 50;

-- Kiểm tra recall bằng cách so sánh với exact search
WITH exact AS (
    SELECT id FROM items
    ORDER BY embedding <=> $query_embedding
    LIMIT 100
),
approx AS (
    SELECT id FROM items
    ORDER BY embedding <=> $query_embedding
    LIMIT 100
)
SELECT 
    COUNT(DISTINCT e.id) as recall_count,
    COUNT(DISTINCT e.id) * 100.0 / 100 as recall_percentage
FROM exact e
JOIN approx a ON e.id = a.id;
```

### Vấn Đề 3: Memory Usage Cao

```sql
-- Giảm m cho HNSW
ALTER INDEX idx_embedding_hnsw SET (m = 8);

-- Hoặc rebuild với PQ compression
REINDEX INDEX idx_embedding_hnsw SET (pq_dim = 64);

-- Monitor memory usage
SELECT pg_size_pretty(pg_relation_size('idx_embedding_hnsw'));
```

## Examples

### Example 1: Build Production-Ready HNSW Index

```sql
-- Step 1: Create table với vector column
CREATE TABLE document_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1536) NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT unique_doc_chunk UNIQUE (document_id, chunk_index)
);

-- Step 2: Create HNSW index optimized cho production
CREATE INDEX idx_embeddings_hnsw ON document_embeddings 
USING hnsw (embedding vector_cosine_ops) 
WITH (
    m = 16,
    ef_construction = 200,
    maintenance_work_mem = '4GB'
);

-- Step 3: Create additional indexes for filtering
CREATE INDEX idx_documents_category ON document_embeddings 
USING gin ((metadata->>'category_id') jsonb_path_ops);

CREATE INDEX idx_documents_created ON document_embeddings (created_at DESC);

-- Step 4: Analyze table sau khi data loaded
ANALYZE document_embeddings;
```

### Example 2: Incremental Index Maintenance

```sql
-- Function để thêm vectors mà không rebuild index
CREATE OR REPLACE FUNCTION add_embedding(
    p_document_id UUID,
    p_chunk_index INTEGER,
    p_content TEXT,
    p_embedding VECTOR(1536),
    p_metadata JSONB DEFAULT '{}'
) RETURNS VOID AS $$
BEGIN
    INSERT INTO document_embeddings 
        (document_id, chunk_index, content, embedding, metadata)
    VALUES 
        (p_document_id, p_chunk_index, p_content, p_embedding, p_metadata)
    ON CONFLICT (document_id, chunk_index) 
    DO UPDATE SET
        content = EXCLUDED.content,
        embedding = EXCLUDED.embedding,
        metadata = EXCLUDED.metadata,
        created_at = NOW();
END;
$$ LANGUAGE plpgsql;

-- Periodic maintenance để optimize index
CREATE OR REPLACE FUNCTION maintain_vector_index()
RETURNS void AS $$
BEGIN
    -- Vacuum để reclaim space
    VACUUM document_embeddings;
    
    -- Analyze để update statistics
    ANALYZE document_embeddings;
    
    -- Rebuild index nếu fragmentation cao
    IF pg_relation_size('idx_embeddings_hnsw') > 
       pg_relation_size('document_embeddings') * 2 THEN
        REINDEX INDEX idx_embeddings_hnsw;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

### Example 3: A/B Testing Giữa Index Types

```sql
-- Tạo cả hai loại index
CREATE INDEX idx_ivfflat ON items USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX idx_hnsw ON items USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 200);

-- Benchmark function
CREATE OR REPLACE FUNCTION benchmark_vector_search(
    p_query_embedding VECTOR(1536),
    p_limit INTEGER DEFAULT 100
) RETURNS TABLE(
    method TEXT,
    execution_time_ms DOUBLE PRECISION,
    result_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    -- Test IVFFlat
    WITH t1 AS (
        SELECT clock_timestamp() as start_time
    ),
    ivfflat_results AS (
        SELECT id FROM items
        ORDER BY embedding <=> p_query_embedding
        LIMIT p_limit
    )
    SELECT 
        'IVFFlat' as method,
        EXTRACT(MILLISECONDS FROM clock_timestamp() - t1.start_time)::double precision as execution_time_ms,
        COUNT(*)::bigint as result_count
    FROM ivfflat_results, t1
    GROUP BY t1.start_time
    
    UNION ALL
    
    -- Test HNSW
    WITH t2 AS (
        SELECT clock_timestamp() as start_time
    ),
    hnsw_results AS (
        SELECT id FROM items
        ORDER BY embedding <=> p_query_embedding
        LIMIT p_limit
    )
    SELECT 
        'HNSW' as method,
        EXTRACT(MILLISECONDS FROM clock_timestamp() - t2.start_time)::double precision as execution_time_ms,
        COUNT(*)::bigint as result_count
    FROM hnsw_results, t2
    GROUP BY t2.start_time;
END;
$$ LANGUAGE plpgsql;
```

## Performance Benchmarks

### Benchmark Methodology

```sql
-- Tạo benchmark dataset
CREATE TABLE benchmark_vectors (
    id SERIAL PRIMARY KEY,
    embedding VECTOR(768) NOT NULL,
    category_id INTEGER NOT NULL
);

-- Generate random vectors cho testing
INSERT INTO benchmark_vectors (embedding, category_id)
SELECT 
    array_to_vector(array(
        SELECT random() FROM generate_series(1, 768)
    )) as embedding,
    (random() * 9)::integer as category_id
FROM generate_series(1, 100000);

-- Run benchmark với multiple queries
DO $$
DECLARE
    query_embedding VECTOR(768);
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    total_duration INTERVAL;
BEGIN
    -- Warm up cache
    PERFORM 1 FROM benchmark_vectors 
    ORDER BY embedding <=> 
        (SELECT embedding FROM benchmark_vectors LIMIT 1);
    
    -- Benchmark
    total_duration := '0'::interval;
    
    FOR i IN 1..100 LOOP
        query_embedding := (SELECT embedding FROM benchmark_vectors OFFSET i LIMIT 1);
        
        start_time := clock_timestamp();
        PERFORM id FROM benchmark_vectors 
        ORDER BY embedding <=> query_embedding 
        LIMIT 100;
        end_time := clock_timestamp();
        
        total_duration := total_duration + (end_time - start_time);
    END LOOP;
    
    RAISE NOTICE 'Average query time: % ms', 
        EXTRACT(MILLISECONDS FROM total_duration) / 100;
END $$;
```

### Expected Performance Ranges

| Dataset Size | Index Type | Build Time | Query Time (p95) | Memory |
|--------------|------------|------------|------------------|--------|
| 100K vectors | IVFFlat | 30s | 50ms | 200MB |
| 100K vectors | HNSW | 2min | 5ms | 500MB |
| 1M vectors | IVFFlat | 5min | 200ms | 2GB |
| 1M vectors | HNSW | 30min | 15ms | 5GB |

## References

1. **pgvector Documentation**: https://github.com/pgvector/pgvector
2. **HNSW Paper**: "Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs" - Yu A. Malkov, D A. Yashunin
3. **IVFFlat Implementation**: PostgreSQL Documentation - GIN Indexes
4. **Product Quantization**: "Product Quantization for Nearest Neighbor Search" - Jegou et al.
5. **Cursor Enterprise Framework - Database Rules**: `.cursor/rules/pgvector.mdc`
