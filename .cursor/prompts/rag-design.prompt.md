---
description: Prompt chuan de thiet ke RAG - chunking, embedding, retrieval
trigger: rag, vector search, retrieval
category: AI
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Prompt: RAG Design - Thiết kế RAG

```markdown
# RAG Design Workflow

## 1. RAG ARCHITECTURE
- **Use Case**: [Chatbot / Search / Recommendation / Analysis]
- **Data Source**: [Documents / Database / Web / API]
- **Model**: [GPT-4o / Gemini / Claude]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/rag/*
- knowledge/vector-search/*
- knowledge/pgvector/*
- knowledge/[ai-provider]/*
Load rules: rag.mdc, vector-search.mdc, pgvector.mdc
```

## 3. RAG PIPELINE

### Ingestion
- [ ] Document loading
- [ ] Text extraction
- [ ] Chunking strategy (512-1024 tokens)
- [ ] Chunk overlap (10-20%)
- [ ] Metadata extraction

### Embedding
- [ ] Model selection
- [ ] Batch processing
- [ ] Quality filtering
- [ ] Deduplication

### Storage
- [ ] Vector DB: PGVector / ChromaDB / Qdrant
- [ ] Index strategy
- [ ] Metadata indexing
- [ ] Hybrid search setup

### Retrieval
- [ ] Query processing
- [ ] Vector search
- [ ] Keyword search
- [ ] Hybrid retrieval
- [ ] Reranking

### Generation
- [ ] Prompt template
- [ ] Context window management
- [ ] Citation generation
- [ ] Response formatting

## 4. EVALUATION METRICS
- [ ] Precision@K
- [ ] Recall@K
- [ ] NDCG@K
- [ ] MRR
- [ ] RAGAS metrics

## 5. LIÊN KẾT
- [[../skills/rag-builder]] - RAG Builder
- [[../skills/vector-search-review]] - Vector Search Review
- [[../rules/rag]] - RAG Rules
- [[../rules/pgvector]] - PGVector Rules
```
