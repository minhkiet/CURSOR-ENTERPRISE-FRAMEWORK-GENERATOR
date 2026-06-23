# RAG Decision Tree - Cây Quyết Định RAG

## Quyết định về Chunking

### Câu hỏi: Chunk size nào?

- **Small (256-512)**: High granularity
- **Medium (512-1024)**: Balanced
- **Large (1024+)**: More context

## Quyết định về Vector DB

### Câu hỏi: Vector DB nào?

- **Pinecone**: Managed, scalable
- **pgvector**: PostgreSQL-based
- **Weaviate**: Open-source

## Summary

Medium chunks + Pinecone là common approach.
