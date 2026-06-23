---
title: "Embedding Storage in PostgreSQL"
description: "Hướng dẫn chi tiết về cách lưu trữ vectors trong PostgreSQL, dimension management, schema design và so sánh pgvector với pg_embedding"
tags: ["pgvector", "storage", "schema", "dimensions", "postgresql", "vector-embedding"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Embedding Storage in PostgreSQL

## Tổng Quan

Việc lưu trữ embeddings một cách hiệu quả trong PostgreSQL là nền tảng quan trọng cho bất kỳ hệ thống vector search nào. Không chỉ đơn thuần là lưu trữ các mảng số float, việc thiết kế schema đúng cách còn ảnh hưởng trực tiếp đến hiệu suất tìm kiếm, khả năng mở rộng và chi phí vận hành của toàn bộ hệ thống.

pgvector cung cấp kiểu dữ liệu `VECTOR` native trong PostgreSQL, cho phép lưu trữ vectors với độ chính xác float32 hoặc float64. Kiểu dữ liệu này được tích hợp sâu vào PostgreSQL, tận dụng được các tính năng như indexing, partitioning, và replication.

Ngoài ra, còn có các extensions khác như `pg_embedding` cũng cung cấp khả năng lưu trữ vector, mỗi loại có những ưu nhược điểm riêng biệt. Việc hiểu rõ các option này sẽ giúp architect đưa ra quyết định phù hợp với yêu cầu của hệ thống.

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức toàn diện về các khía cạnh sau:

Đầu tiên, chúng ta sẽ tìm hiểu cách định nghĩa và sử dụng kiểu dữ liệu VECTOR trong PostgreSQL, bao gồm casting giữa các định dạng khác nhau và quản lý dimension.

Thứ hai, tài liệu hướng dẫn thiết kế schema tối ưu cho vector storage, bao gồm partitioning strategies, indexing considerations và data modeling patterns.

Thứ ba, chúng ta sẽ so sánh chi tiết giữa pgvector và pg_embedding, phân tích use cases phù hợp cho từng solution.

Cuối cùng, tài liệu cung cấp các best practices về performance optimization, backup strategies và monitoring cho vector storage.

## Key Concepts

### 1. Kiểu Dữ Liệu VECTOR trong pgvector

pgvector cung cấp kiểu dữ liệu `VECTOR(d)` trong đó `d` là số chiều của vector. Các chiều phổ biến phụ thuộc vào embedding model được sử dụng:

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Các dimension phổ biến theo model
-- OpenAI ada-002: 1536 dimensions
-- OpenAI text-embedding-3-small: 1536 dimensions
-- OpenAI text-embedding-3-large: 3072 dimensions
-- Cohere embed-english-v3: 1024 dimensions
-- sentence-transformers/all-MiniLM-L6-v2: 384 dimensions

-- Tạo table với vector column
CREATE TABLE document_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding VECTOR(1536) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Vector có thể được cast từ various formats
INSERT INTO document_embeddings (document_id, chunk_text, embedding)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'Nội dung của đoạn văn bản',
    '[0.123, -0.456, 0.789, ...]::vector'  -- Cast từ text
);
```

### 2. Dimension Management

Việc quản lý dimension là quan trọng vì pgvector yêu cầu tất cả vectors trong một column phải có cùng số chiều. Nếu dimension không khớp, sẽ có lỗi xảy ra.

```sql
-- Kiểm tra dimension của một vector
SELECT embedding::text, 
       array_length(embedding::real[], 1) as dimensions
FROM document_embeddings
LIMIT 1;

-- Validate dimension consistency
CREATE OR REPLACE FUNCTION validate_vector_dimension()
RETURNS TABLE(
    table_name TEXT,
    column_name TEXT,
    dimension INTEGER,
    min_dim INTEGER,
    max_dim INTEGER,
    vector_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'document_embeddings'::text,
        'embedding'::text,
        1536::integer,
        MIN(array_length(embedding::real[], 1))::integer,
        MAX(array_length(embedding::real[], 1))::integer,
        COUNT(*)::bigint
    FROM document_embeddings;
END;
$$ LANGUAGE plpgsql;
```

### 3. Casting và Type Conversion

pgvector hỗ trợ nhiều cách casting khác nhau:

```sql
-- Cast từ array
INSERT INTO document_embeddings (embedding)
VALUES (ARRAY[0.1::real, 0.2::real, 0.3::real, ...]::vector);

-- Cast từ JSONB array
INSERT INTO document_embeddings (embedding)
VALUES ('[0.1, 0.2, 0.3, ...]'::jsonb::vector);

-- Cast từ string
INSERT INTO document_embeddings (embedding)
VALUES ('[0.1,0.2,0.3]'::vector);

-- Cast vector thành array để sử dụng trong calculations
SELECT embedding::real[] as embedding_array
FROM document_embeddings;

-- Serialize vector ra JSON
SELECT jsonb_build_object(
    'vector', embedding::text,
    'dimensions', array_length(embedding::real[], 1)
) as vector_json
FROM document_embeddings;
```

### 4. Schema Design Patterns

#### Pattern 1: Document Embedding Storage

```sql
-- Table cho document chunks với metadata
CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Document reference
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    
    -- Content
    chunk_text TEXT NOT NULL,
    chunk_hash VARCHAR(64) NOT NULL,  -- SHA-256 hash for deduplication
    
    -- Embedding với dimension cố định
    embedding VECTOR(1536) NOT NULL,
    
    -- Metadata cho filtering
    metadata JSONB DEFAULT '{}',
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT unique_document_chunk UNIQUE (document_id, chunk_index),
    CONSTRAINT valid_chunk_index CHECK (chunk_index >= 0)
);

-- Indexes
CREATE INDEX idx_chunks_document ON document_chunks (document_id);
CREATE INDEX idx_chunks_hash ON document_chunks (chunk_hash);
CREATE INDEX idx_chunks_embedding ON document_chunks 
    USING hnsw (embedding vector_cosine_ops) 
    WITH (m = 16, ef_construction = 200);

-- GIN index for JSONB metadata
CREATE INDEX idx_chunks_metadata ON document_chunks 
    USING gin (metadata jsonb_path_ops);
```

#### Pattern 2: Multi-tenant Vector Storage

```sql
-- Partitioned table cho multi-tenant
CREATE TABLE tenant_embeddings (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID NOT NULL,
    embedding VECTOR(1536) NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    PRIMARY KEY (tenant_id, id)
) PARTITION BY LIST (tenant_id);

-- Tạo partitions cho từng tenant
CREATE TABLE tenant_embeddings_tenant_a 
    PARTITION OF tenant_embeddings
    FOR VALUES IN ('tenant-a-uuid');

CREATE TABLE tenant_embeddings_tenant_b 
    PARTITION OF tenant_embeddings
    FOR VALUES IN ('tenant-b-uuid');

-- Index per partition
CREATE INDEX ON tenant_embeddings_tenant_a 
    USING hnsw (embedding vector_cosine_ops);

CREATE INDEX ON tenant_embeddings_tenant_b 
    USING hnsw (embedding vector_cosine_ops);
```

#### Pattern 3: Time-series Vector Storage

```sql
-- Table cho time-series embeddings (e.g., user behavior)
CREATE TABLE user_behavior_embeddings (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    embedding VECTOR(128) NOT NULL,
    event_timestamp TIMESTAMPTZ DEFAULT NOW(),
    
    -- Partition by month
    PARTITION BY RANGE (event_timestamp)
);

CREATE TABLE user_behavior_embeddings_2024_01 
    PARTITION OF user_behavior_embeddings
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE user_behavior_embeddings_2024_02 
    PARTITION OF user_behavior_embeddings
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Index trên mỗi partition
CREATE INDEX ON user_behavior_embeddings_2024_01 
    USING hnsw (embedding vector_cosine_ops);

CREATE INDEX ON user_behavior_embeddings_2024_02 
    USING hnsw (embedding vector_cosine_ops);
```

### 5. So Sánh pgvector vs pg_embedding

| Tiêu Chí | pgvector | pg_embedding |
|----------|----------|--------------|
| **Kiểu dữ liệu** | VECTOR(d) | embedding |
| **Max dimensions** | 16,000 | 65,535 |
| **Precision** | float32, float64 | float16, float32 |
| **Indexing** | HNSW, IVFFlat | HNSW only |
| **Operators** | <=>, <+>, <->, <#> | <=>, <+>, L2, IP |
| **Maintenance** | Mature, well-tested | Newer, less battle-tested |
| **Community** | Large, active | Smaller |
| **Compatibility** | PostgreSQL 12+ | PostgreSQL 14+ |

```sql
-- pgvector example
CREATE EXTENSION vector;
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    embedding VECTOR(1536)
);
INSERT INTO items (embedding) VALUES ('[0.1, 0.2, ...]'::vector);
SELECT * FROM items ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector LIMIT 5;
```

```sql
-- pg_embedding example
CREATE EXTENSION embedding;
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    embedding embedding(1536)
);
INSERT INTO items (embedding) VALUES ('[0.1, 0.2, ...]');
SELECT * FROM items ORDER BY embedding <=> '[0.1, 0.2, ...]' LIMIT 5;
```

## Best Practices

### 1. Optimal Data Types

```sql
-- Sử dụng float32 thay vì float64 để tiết kiệm space
-- pgvector mặc định sử dụng float32

CREATE TABLE optimized_embeddings (
    -- Dùng float32 vector (4 bytes per dimension)
    embedding VECTOR(1536) NOT NULL,
    
    -- Store normalized vectors để use cosine similarity
    -- giúp comparison nhanh hơn
    embedding_cosine VECTOR(1536) GENERATED ALWAYS AS (
        embedding / (SELECT sqrt(sum(v * v))::real 
                    FROM unnest(embedding::real[]) AS v)
    ) STORED
);

-- Nếu cần float64 cho precision
CREATE TABLE high_precision_embeddings (
    embedding VECTOR(1536) NOT NULL  -- vẫn là float32 internally
);
-- Hoặc cast khi cần:
SELECT embedding::double precision[] FROM high_precision_embeddings;
```

### 2. Storage Optimization

```sql
-- Sử dụng TOAST compression cho text columns
CREATE TABLE chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chunk_text TEXT COMPRESSIBLE,
    embedding VECTOR(1536) NOT NULL
) WITH (
    toast_tuple_target = 8160
);

-- Monitor storage
SELECT 
    pg_size_pretty(pg_total_relation_size('document_chunks')) as total_size,
    pg_size_pretty(pg_relation_size('document_chunks')) as table_size,
    pg_size_pretty(pg_indexes_size('document_chunks')) as index_size;
```

### 3. Batch Operations

```sql
-- Batch insert để improve performance
PREPARE insert_embedding(UUID, UUID, TEXT, REAL[]) AS
INSERT INTO document_embeddings (document_id, chunk_index, chunk_text, embedding)
VALUES ($1, $2, $3, $4::vector)
ON CONFLICT (document_id, chunk_index) 
DO UPDATE SET 
    chunk_text = EXCLUDED.chunk_text,
    embedding = EXCLUDED.embedding;

-- Execute batch
DO $$
DECLARE
    batch_size := 1000;
    offset_val := 0;
BEGIN
    FOR i IN 0..999 LOOP
        EXECUTE format(
            'PREPARE batch_insert_%s AS INSERT INTO document_embeddings 
             (document_id, chunk_index, chunk_text, embedding) VALUES ($1, $2, $3, $4::vector)',
            i
        );
    END LOOP;
END $$;

-- Sử dụng COPY cho bulk insert
\copy document_embeddings(id, document_id, chunk_index, chunk_text, embedding) 
FROM 'embeddings.csv' WITH (FORMAT csv, NULL 'NULL');
```

## Common Patterns

### Pattern 1: Upsert với Deduplication

```sql
CREATE OR REPLACE FUNCTION upsert_embedding(
    p_document_id UUID,
    p_chunk_index INTEGER,
    p_chunk_text TEXT,
    p_embedding REAL[]
) RETURNS UUID AS $$
DECLARE
    v_id UUID;
    v_hash VARCHAR(64);
BEGIN
    -- Calculate hash cho deduplication
    v_hash := encode(sha256(p_chunk_text::bytea), 'hex');
    
    INSERT INTO document_chunks (
        id, document_id, chunk_index, chunk_text, embedding, chunk_hash
    )
    VALUES (
        gen_random_uuid(),
        p_document_id, p_chunk_index, p_chunk_text, 
        p_embedding::vector, v_hash
    )
    ON CONFLICT (document_id, chunk_index)
    DO UPDATE SET
        chunk_text = EXCLUDED.chunk_text,
        embedding = EXCLUDED.embedding,
        chunk_hash = EXCLUDED.chunk_hash,
        updated_at = NOW()
    RETURNING id INTO v_id;
    
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;
```

### Pattern 2: Incremental Similarity Search

```sql
-- Tìm similar items với pagination
CREATE OR REPLACE FUNCTION search_similar_embeddings(
    p_query_embedding REAL[],
    p_limit INTEGER DEFAULT 20,
    p_offset INTEGER DEFAULT 0,
    p_min_similarity FLOAT DEFAULT 0.7
) RETURNS TABLE(
    id UUID,
    chunk_text TEXT,
    similarity FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        dc.id,
        dc.chunk_text,
        1 - (dc.embedding <=> p_embedding::vector) as similarity
    FROM document_chunks dc
    WHERE 1 - (dc.embedding <=> p_embedding::vector) >= p_min_similarity
    ORDER BY dc.embedding <=> p_embedding::vector
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
```

### Pattern 3: Cross-reference Embeddings

```sql
-- Tìm documents có similar embeddings
WITH similar_chunks AS (
    SELECT 
        document_id,
        array_agg(id) as chunk_ids,
        array_agg(1 - (embedding <=> $1::vector)) as similarities
    FROM document_chunks
    GROUP BY document_id
)
SELECT 
    dc.document_id,
    COUNT(*) as matching_chunks,
    AVG(1 - (dc.embedding <=> $1::vector)) as avg_similarity,
    MAX(1 - (dc.embedding <=> $1::vector)) as max_similarity
FROM document_chunks dc
JOIN similar_chunks sc ON dc.document_id = sc.document_id
GROUP BY dc.document_id
ORDER BY avg_similarity DESC
LIMIT 20;
```

## Troubleshooting

### Vấn Đề 1: Dimension Mismatch

```sql
-- Lỗi: dimension mismatch
-- ERROR: vector dimension must be 1536

-- Kiểm tra embeddings có dimension không đồng nhất
SELECT 
    array_length(embedding::real[], 1) as dim,
    COUNT(*) as count
FROM document_embeddings
GROUP BY array_length(embedding::real[], 1);

-- Fix: Resize vectors
UPDATE document_embeddings
SET embedding = (
    SELECT array_to_vector(
        array_fill(0::real, ARRAY[1536]) || 
        embedding::real[]
    )[1:1536]
)
WHERE array_length(embedding::real[], 1) != 1536;
```

### Vấn Đề 2: NULL Vectors

```sql
-- Kiểm tra NULL embeddings
SELECT COUNT(*) FROM document_embeddings WHERE embedding IS NULL;

-- Fix: Xóa hoặc update NULL vectors
DELETE FROM document_embeddings WHERE embedding IS NULL;

-- Hoặc fill với zero vector
UPDATE document_embeddings
SET embedding = array_to_vector(
    array_fill(0::real, ARRAY[1536])
)::vector
WHERE embedding IS NULL;
```

### Vấn Đề 3: Out-of-Range Values

```sql
-- Kiểm tra values có trong range [-1, 1] (common for cosine similarity)
SELECT 
    MIN(unnest) as min_val,
    MAX(unnest) as max_val
FROM (
    SELECT embedding::real[] as arr
    FROM document_embeddings
) t,
unnest(t.arr);

-- Normalize out-of-range vectors
UPDATE document_embeddings
SET embedding = (
    embedding / sqrt(
        (SELECT sum(v * v)::real 
         FROM unnest(embedding::real[]) AS v)
    )
)::vector
WHERE embedding IS NOT NULL;
```

## Examples

### Example 1: Complete Document Embedding System

```sql
-- Step 1: Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Step 2: Create documents table
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    source_url TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Step 3: Create chunks table
CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_hash VARCHAR(64) NOT NULL,
    embedding VECTOR(1536) NOT NULL,
    token_count INTEGER,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE (document_id, chunk_index)
);

-- Step 4: Create indexes
CREATE INDEX idx_chunks_document ON document_chunks (document_id);
CREATE INDEX idx_chunks_hash ON document_chunks (chunk_hash);
CREATE INDEX idx_chunks_embedding ON document_chunks 
    USING hnsw (embedding vector_cosine_ops) 
    WITH (m = 16, ef_construction = 200);

-- Step 5: Create trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER documents_updated_at
    BEFORE UPDATE ON documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- Step 6: Create search function
CREATE OR REPLACE FUNCTION search_documents(
    p_query_embedding REAL[],
    p_limit INTEGER DEFAULT 10,
    p_min_similarity FLOAT DEFAULT 0.7
) RETURNS TABLE(
    document_id UUID,
    title TEXT,
    chunk_text TEXT,
    similarity FLOAT,
    rank BIGINT
) AS $$
BEGIN
    RETURN QUERY
    WITH results AS (
        SELECT 
            dc.document_id,
            d.title,
            dc.chunk_text,
            1 - (dc.embedding <=> p_query_embedding::vector) as similarity,
            ROW_NUMBER() OVER (PARTITION BY dc.document_id ORDER BY 
                dc.embedding <=> p_query_embedding::vector) as rn
        FROM document_chunks dc
        JOIN documents d ON dc.document_id = d.id
        WHERE 1 - (dc.embedding <=> p_query_embedding::vector) >= p_min_similarity
    )
    SELECT 
        r.document_id,
        r.title,
        r.chunk_text,
        r.similarity,
        ROW_NUMBER() OVER (ORDER BY r.similarity DESC)::bigint as rank
    FROM results r
    WHERE r.rn = 1
    ORDER BY r.similarity DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;
```

### Example 2: Embedding Versioning System

```sql
-- System để track embedding versions (useful khi upgrade model)
CREATE TABLE embedding_versions (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    dimension INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE (model_name, model_version)
);

CREATE TABLE versioned_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id UUID NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    version_id INTEGER NOT NULL REFERENCES embedding_versions(id),
    embedding VECTOR(1536) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE (entity_id, entity_type, version_id)
);

-- Index per version
CREATE INDEX idx_v1_embeddings ON versioned_embeddings 
    USING hnsw (embedding vector_cosine_ops)
    WHERE version_id = 1;

CREATE INDEX idx_v2_embeddings ON versioned_embeddings 
    USING hnsw (embedding vector_cosine_ops)
    WHERE version_id = 2;

-- Search across specific version
CREATE OR REPLACE FUNCTION search_version(
    p_entity_id UUID,
    p_query_embedding REAL[],
    p_version_id INTEGER
) RETURNS FLOAT AS $$
DECLARE
    v_similarity FLOAT;
BEGIN
    SELECT 1 - (embedding <=> p_query_embedding::vector)
    INTO v_similarity
    FROM versioned_embeddings
    WHERE entity_id = p_entity_id
      AND entity_type = 'document'
      AND version_id = p_version_id
    LIMIT 1;
    
    RETURN COALESCE(v_similarity, 0);
END;
$$ LANGUAGE plpgsql;
```

### Example 3: Backup và Restore Strategy

```sql
-- Export embeddings to file
COPY (
    SELECT 
        id::text,
        document_id::text,
        chunk_index,
        chunk_text,
        embedding::text
    FROM document_chunks
) TO '/backup/embeddings.csv';

-- Import từ backup
COPY document_chunks (id, document_id, chunk_index, chunk_text, embedding)
FROM '/backup/embeddings.csv'
WITH (FORMAT csv);

-- Hoặc sử dụng pg_dump với data-only
-- pg_dump -h localhost -U postgres -d mydb --data-only -t document_chunks > embeddings.sql

-- Incremental backup using COPY
CREATE OR REPLACE FUNCTION backup_embeddings_since(
    p_timestamp TIMESTAMPTZ
) RETURNS void AS $$
BEGIN
    COPY (
        SELECT 
            id::text,
            document_id::text,
            chunk_index,
            chunk_text,
            embedding::text,
            created_at::text
        FROM document_chunks
        WHERE created_at > p_timestamp
    ) TO '/backup/incremental_' || to_char(p_timestamp, 'YYYYMMDDHH24MI') || '.csv';
END;
$$ LANGUAGE plpgsql;
```

## References

1. **pgvector GitHub**: https://github.com/pgvector/pgvector
2. **PostgreSQL TOAST**: https://www.postgresql.org/docs/current/storage-toast.html
3. **pg_embedding GitHub**: https://github.com/embulk/pg_embedding
4. **Embedding Model Documentation**: OpenAI, Cohere, HuggingFace
5. **Cursor Enterprise Framework - Database Rules**: `.cursor/rules/database.mdc`
