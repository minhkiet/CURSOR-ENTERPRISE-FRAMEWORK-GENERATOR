# PGVector FAQ - Câu Hỏi Thường Gặp

## Câu Hỏi Cơ Bản

### 1. PGVector là gì?

PGVector là PostgreSQL extension cho vector similarity search. Cung cấp data type, operators, indexes.

### 2. HNSW vs IVFFlat?

HNSW: Higher recall, slower build. IVFFlat: Faster build, good recall.

## Câu Hỏi Kỹ Thuật

### 3. Dimensions nào?

Typically 384-3072 for text embeddings. Match your embedding model.

### 4. Distance nào?

Cosine distance recommended for text. Euclidean for images.
