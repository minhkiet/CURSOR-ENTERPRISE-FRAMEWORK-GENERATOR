# PGVector Anti-Patterns - Các Mẫu Cần Tránh

## Anti-Patterns

### 1. No Index

**Mô tả**: Search without index on large table.

**Giải pháp**: Create HNSW/IVFFlat index.

## Kết luận

Tránh các anti-patterns này giúp PGVector performance tốt hơn.
