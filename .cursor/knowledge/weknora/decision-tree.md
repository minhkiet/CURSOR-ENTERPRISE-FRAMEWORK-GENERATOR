# WeKnora Decision Tree

## 1. Document Type Decision

```
What type of documents are you processing?
│
├─► PDF / Scanned Documents
│   └─► Need OCR?
│       ├─► Yes → Use PaddleOCR parser
│       └─► No → Use Built-in parser
│
├─► Word / Office Documents
│   └─► Preserve formatting?
│       ├─► Yes → Built-in parser with structure preservation
│       └─► No → Built-in plain text parser
│
├─► Markdown / HTML
│   └─► Built-in parser (native support)
│
├─► Images
│   └─► Use PaddleOCR-VL for multimodal understanding
│
└─► Structured Data (JSON, CSV, Excel)
    └─► Built-in structured parser
```

## 2. Knowledge Base Type Decision

```
What is your primary use case?
│
├─► Q&A System (FAQ-style)
│   └─► FAQ Knowledge Base
│       Features: Structured Q&A, intent routing, high precision
│
├─► General Information Retrieval
│   └─► Document Knowledge Base
│       Features: Full-text + semantic search, citations
│
└─► Self-Maintaining Wiki
    └─► Wiki Knowledge Base
        Features: Auto-generation, entity extraction, knowledge graph
```

## 3. Retrieval Strategy Decision

```
What retrieval quality do you need?
│
├─► Maximum Quality (slower)
│   └─► Hybrid Search + Reranking
│       Vector (0.4) + BM25 (0.3) + GraphRAG (0.2) + KG (0.1)
│       + Cross-encoder reranking
│
├─► Balanced (recommended)
│   └─► Hybrid Search (no reranking)
│       Vector (0.5) + BM25 (0.3) + GraphRAG (0.2)
│
└─► Fast Response (lower quality)
    └─► Vector Search Only
        Use HNSW indexing for speed
```

## 4. Chunking Strategy Decision

```
What is the nature of your documents?
│
├─► Short content (Q&A, FAQs)
│   └─► Tier 1: chunk_size=256, overlap=50
│
├─► Technical documents (manuals, reports)
│   └─► Tier 2: chunk_size=512, overlap=100
│       Consider parent-child chunking
│
├─► Long-form content (books, articles)
│   └─► Tier 3: chunk_size=1024, overlap=200
│
└─► Mixed content
    └─► Adaptive chunking based on document structure
```

## 5. LLM Provider Decision

```
What are your priorities?
│
├─► Best Quality
│   └─► Claude 3 Opus / GPT-4
│       Trade-off: Higher cost
│
├─► Best Value
│   └─► DeepSeek / GPT-3.5-Turbo
│       Trade-off: Slightly lower quality
│
├─► Privacy / Self-hosted
│   └─► Ollama with Llama/Mistral
│       Trade-off: Requires local GPU
│
└─► Chinese Language
    └─► Qwen / Zhipu / DeepSeek
        Trade-off: Best for Chinese content
```

## 6. Vector Store Decision

```
What is your scale and infrastructure?
│
├─► Development / Small Scale
│   └─► pgvector (PostgreSQL)
│       Pros: Built-in, simple setup
│       Cons: Limited scaling
│
├─► Medium Scale
│   ├─► Elasticsearch
│   │   Pros: Full-text + vector
│   └─► Qdrant
│       Pros: Fast, easy to use
│
├─► Large Scale / Production
│   ├─► Milvus
│   │   Pros: Highly scalable
│   ├─► Weaviate
│   │   Pros: Graph features
│   └─► Elasticsearch / OpenSearch
│       Pros: Enterprise support
│
└─► AWS Environment
    └─► OpenSearch / Amazon Aurora
        Pros: Native AWS integration
```

## 7. Agent Mode Decision

```
Do you need complex reasoning?
│
├─► Simple Q&A (fast, accurate)
│   └─► QA Mode
│       Direct RAG retrieval + generation
│
├─► Complex Tasks (multi-step)
│   └─► Agent Mode (ReAct)
│       Autonomous reasoning, tool use
│
└─► Research / Analysis
    └─► Agent Mode with:
│       - Web search enabled
│       - Extended max_steps
│       - Thinking mode enabled
```

## 8. Embedding Model Decision

```
What embedding requirements?
│
├─► General Purpose
│   └─► text-embedding-3-small (OpenAI)
│       1536 dims, fast, affordable
│
├─► High Quality
│   └─► text-embedding-3-large / BGE
│       3072 dims, better quality
│
├─► Multilingual
│   └─► BGE-m3 / Multilingual-E5
│       100+ languages support
│
└─► Self-hosted
    └─► Ollama embeddings
        Privacy, no API costs
```

## 9. Deployment Decision

```
What is your deployment environment?
│
├─► Local Development
│   └─► Docker Compose (single-node)
│       Quick start, limited resources
│
├─► Team / Small Org
│   └─► Docker Compose with profiles
│       Neo4j + Langfuse optional
│
├─► Production / Enterprise
│   └─► Kubernetes (Helm)
│       Scalability, high availability
│
└─► Managed Service
    └─► WeKnora Cloud
│       Zero infrastructure management
```

## 10. Security Configuration Decision

```
What security level is required?
│
├─► Internal Network Only
│   └─► Basic security
│       - Internal authentication
│       - Network isolation
│
├─► Internet-facing (standard)
│   └─► Standard security
│       - TLS enabled
│       - API key authentication
│       - Rate limiting
│
└─► Enterprise / Regulated
    └─► Enhanced security
        - AES-256-GCM encryption
        - gRPC TLS
        - Full audit logging
        - RBAC enforcement
        - SSRF protection
```
