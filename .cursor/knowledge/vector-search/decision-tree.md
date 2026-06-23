# Vector Search Decision Tree - Cây Quyết Định

## Quyết định về Index

### Câu hỏi: Index type nào?

- **HNSW**: High recall, slow build
- **IVF**: Fast build, good recall
- **FLAT**: Exact search

## Quyết định về Distance

### Câu hỏi: Distance metric nào?

- **Cosine**: Angle similarity
- **Euclidean**: Straight-line distance
- **Dot Product**: Projection

## Summary

HNSW + Cosine là common approach.
