# RAG Architecture - Kiến Trúc RAG Systems

## Tổng quan

RAG (Retrieval-Augmented Generation) kết hợp vector search với LLM để generate responses từ knowledge base.

## Kiến trúc chi tiết

### 1. Components

- **Document Loader**: Load documents
- **Text Splitter**: Chunk documents
- **Embedding Model**: Generate vectors
- **Vector Store**: Store & search vectors
- **LLM**: Generate responses

### 2. Flow

1. Ingest documents
2. Chunk into pieces
3. Generate embeddings
4. Store in vector DB
5. Query relevant chunks
6. Feed to LLM

### 3. Implementation

```typescript
// Document ingestion
const docs = await loader.load();
const chunks = splitter.splitDocuments(docs);

// Embedding
const embeddings = await embedModel.embedDocuments(chunks);

// Store
await vectorStore.addVectors(embeddings, chunks);

// Query
const results = await vectorStore.similaritySearch(query);
const response = await llm.generate(results);
```

## Kết luận

RAG architecture enables accurate AI responses from private knowledge.
