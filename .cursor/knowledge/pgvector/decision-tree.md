# PGVector Decision Tree - Cây Quyết Định PGVector

## Quyết định về Index

### Câu hỏi: Index type nào?

- **HNSW**: High recall, slow build
- **IVFFlat**: Fast build, good recall
- **No Index**: Small datasets

## Quyết định về Distance

### Câu hỏi: Distance metric nào?

- **Cosine**: Text embeddings
- **Euclidean**: Images
- **Negative Dot Product**: Recommendations

## Summary

HNSW + Cosine là common approach.
