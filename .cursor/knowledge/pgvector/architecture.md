# PGVector Architecture - Kiến Trúc PGVector

## Tổng quan

PGVector là PostgreSQL extension cho vector similarity search. Hỗ trợ embeddings storage và similarity queries.

## Kiến trúc chi tiết

### 1. Data Types

```sql
-- Create table with vector column
CREATE TABLE items (
  id bigserial PRIMARY KEY,
  embedding vector(1536)
);
```

### 2. Indexes

```sql
-- HNSW index
CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops);

-- IVFFlat index
CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops);
```

### 3. Similarity Queries

```sql
-- Find similar items
SELECT * FROM items ORDER BY embedding <=> '[0.1, 0.2, ...]' LIMIT 5;
```

## Kết luận

PGVector enables semantic search in PostgreSQL.
