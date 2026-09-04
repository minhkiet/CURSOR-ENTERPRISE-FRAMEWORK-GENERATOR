---
description: WeKnora Knowledge Base Skill - RAG implementation, document Q&A, FAQ system, enterprise wiki, hybrid search với Vector + BM25 + GraphRAG + Knowledge Graph
created: 2026-06-26
version: 1.0.0
tags: [weknora, rag, knowledge-base, hybrid-search, vector-search, bm25, graphrag, knowledge-graph, document-qa, faq, wiki]
---

# WeKnora KB Skill

## Mục tiêu

Tích hợp WeKnora knowledge platform vào Codex workflow để:
- Xây dựng Knowledge Base từ PDF, Word, Markdown, hình ảnh OCR
- Triển khai RAG-based Q&A system
- Tạo FAQ Knowledge Base
- Xây dựng Enterprise Wiki
- Sử dụng Hybrid Retrieval (Vector + BM25 + GraphRAG + Knowledge Graph)

## Pre-Review Gate

### W.1 Requirements Analysis

**1. Identify KB Type:**
- [ ] FAQ Knowledge Base - Structured Q&A pairs, intent routing
- [ ] Document Knowledge Base - General docs, full-text + semantic search
- [ ] Wiki Knowledge Base - Auto-generated interlinked pages

**2. Document Assessment:**
- [ ] Document formats identified (PDF/Word/Markdown/Images)
- [ ] Total document volume estimated
- [ ] Document structure complexity evaluated
- [ ] OCR requirements assessed (for scanned docs)

**3. Retrieval Requirements:**
- [ ] Search quality requirements defined
- [ ] Latency requirements defined
- [ ] Hybrid search weights considered
- [ ] Reranking requirements assessed

### W.2 Infrastructure Planning

**1. WeKnora Deployment:**
- [ ] Deployment type selected (Docker/Kubernetes/Cloud)
- [ ] Vector store selected (pgvector/Elasticsearch/Milvus)
- [ ] LLM provider configured (OpenAI/DeepSeek/Ollama)

**2. MCP Integration:**
- [ ] WeKnora CLI installed
- [ ] MCP server configured
- [ ] Codex MCP connection planned

### W.3 Knowledge Architecture

**1. KB Structure:**
- [ ] KB name and type defined
- [ ] Chunking strategy selected
- [ ] Metadata schema designed
- [ ] Index structure planned

**2. Document Processing:**
- [ ] Parser selected (builtin/paddleocr/opendata)
- [ ] Chunking strategy defined (tier 1/2/3 or adaptive)
- [ ] OCR configuration planned (if needed)
- [ ] Q&A generation considered (for FAQ KB)

---

## Implementation

### Phase 1: WeKnora Setup

```bash
# 1. Clone and configure WeKnora
git clone https://github.com/Tencent/WeKnora.git
cd WeKnora
cp .env.example .env

# 2. Configure environment
# Set LLM provider, vector store, storage

# 3. Start services
docker compose up -d

# 4. Install CLI for MCP
brew install weknora  # or download binary

# 5. Configure MCP in Codex
weknora auth login --host http://localhost:8080
```

### Phase 2: Knowledge Base Creation

```bash
# Create KB via CLI
weknora kb create \
  --name "My Knowledge Base" \
  --type document  # or faq, wiki

# Configure retrieval settings
weknora kb config --kb "My Knowledge Base" \
  --retrieval hybrid \
  --weights vector=0.4,bm25=0.3,graphrag=0.2
```

### Phase 3: Document Ingestion

```bash
# Upload documents
weknora doc upload ./docs/ --kb "My Knowledge Base"

# With options
weknora doc upload manual.pdf \
  --kb "My Knowledge Base" \
  --parser paddleocr \
  --chunk-size 512

# Generate Q&A pairs (for FAQ)
weknora doc upload faq.md \
  --kb "FAQ KB" \
  --generate-qa \
  --qa-count 10
```

### Phase 4: Query Integration

```typescript
// Integration example
import { WeKnoraClient } from '@weknora/client';

const client = new WeKnoraClient({
  host: process.env.WEKNORA_HOST,
  apiKey: process.env.WEKNORA_API_KEY
});

// Simple Q&A
async function askQuestion(query: string) {
  const results = await client.search({
    kbId: 'my-kb',
    query,
    mode: 'qa',
    topK: 10
  });
  return results;
}

// Agent mode for complex tasks
async function agentQuery(query: string) {
  const response = await client.chat({
    kbId: 'my-kb',
    query,
    mode: 'agent'
  });
  return response;
}
```

---

## Post-Review Gate

### W.4 Quality Verification

**1. Retrieval Quality:**
- [ ] Sample queries tested
- [ ] Precision/Recall metrics checked
- [ ] Hybrid search weights validated
- [ ] Reranking quality verified

**2. Document Processing:**
- [ ] Chunk boundaries appropriate
- [ ] Metadata preserved correctly
- [ ] OCR accuracy acceptable
- [ ] Index health verified

**3. Integration:**
- [ ] MCP tools working in Codex
- [ ] CLI commands functional
- [ ] API responses correct
- [ ] Error handling verified

### W.5 Performance Check

**1. Latency:**
- [ ] Retrieval latency < 200ms (p95)
- [ ] Agent reasoning time acceptable
- [ ] Document processing throughput adequate

**2. Scalability:**
- [ ] Index size within limits
- [ ] Chunk count optimized
- [ ] Cache configured if needed

### W.6 Documentation

**1. Setup Documentation:**
- [ ] Deployment documented
- [ ] Configuration documented
- [ ] Troubleshooting guide prepared

**2. Usage Documentation:**
- [ ] KB usage documented
- [ ] Query examples provided
- [ ] API reference documented

---

## Quick Reference

### KB Types

| Type | Use Case | Key Features |
|------|----------|--------------|
| FAQ | Q&A systems | Intent routing, high precision |
| Document | General KB | Full search, citations |
| Wiki | Self-maintaining | Auto-generation, knowledge graph |

### Chunking Tiers

| Tier | Size | Use Case |
|------|------|----------|
| Tier 1 | 256 tokens | Q&A, FAQ |
| Tier 2 | 512 tokens | Technical docs |
| Tier 3 | 1024 tokens | Long-form content |

### Hybrid Search Weights

```yaml
# Default
vector: 0.4
bm25: 0.3
graphrag: 0.2
knowledge_graph: 0.1

# For FAQ (keyword-heavy)
vector: 0.3
bm25: 0.5
graphrag: 0.1
knowledge_graph: 0.1

# For technical (semantic-heavy)
vector: 0.5
bm25: 0.2
graphrag: 0.2
knowledge_graph: 0.1
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Slow indexing | Enable batch mode, reduce chunk size |
| Poor retrieval | Tune hybrid weights, enable reranking |
| OCR failures | Use PaddleOCR parser |
| LLM errors | Check API key, enable fallback provider |

---

## Liên kết

- [[weknora]] - WeKnora Rule
- [[rag]] - RAG Guidelines
- [[vector-search]] - Vector Search
- [[weknora-knowledge/architecture]] - Architecture Details
- [[weknora-knowledge/mcp-integration]] - MCP Setup
