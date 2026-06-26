# WeKnora Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         WeKnora Architecture                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌────────────┐ │
│  │   Web UI    │   │  REST API   │   │    CLI      │   │   MCP      │ │
│  │  (Vue.js)   │   │  (Go)       │   │  (weknora) │   │  Server    │ │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘   └─────┬──────┘ │
│         │                 │                 │                  │        │
│         └─────────────────┼─────────────────┼──────────────────┘        │
│                           │                 │                            │
│                    ┌──────▼─────────────────▼──────┐                    │
│                    │         API Gateway            │                    │
│                    │      (Go HTTP Server)          │                    │
│                    └──────┬─────────────────────────┘                    │
│                           │                                               │
│         ┌─────────────────┼─────────────────┐                           │
│         │                 │                 │                           │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐                     │
│  │   Session   │  │   Document  │  │   Agent     │                     │
│  │   Service   │  │   Service   │  │   Service   │                     │
│  │             │  │             │  │   (ReAct)   │                     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                     │
│         │                 │                 │                            │
│  ┌──────▼─────────────────▼─────────────────▼──────┐                   │
│  │              Retrieval Engine                      │                   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────┐│                   │
│  │  │  Vector  │ │   BM25   │ │ GraphRAG │ │  KG  ││                   │
│  │  │  Search  │ │  Search  │ │  Search  │ │Search││                   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────┘│                   │
│  └──────────────────────┬───────────────────────────┘                   │
│                         │                                              │
│  ┌──────────────────────▼───────────────────────────┐                  │
│  │              LLM Provider Layer                  │                  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐     │                  │
│  │  │ OpenAI │ │DeepSeek│ │ Qwen   │ │Ollama │     │                  │
│  │  └────────┘ └────────┘ └────────┘ └────────┘     │                  │
│  └──────────────────────────────────────────────────┘                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend (Vue.js + TypeScript)

- **Web UI**: React-style interface với real-time chat
- **Responsive Design**: Desktop và mobile compatible
- **Features**: Knowledge browser, chat interface, admin panel

### 2. Backend (Go)

#### API Server
- RESTful API với JWT authentication
- Multi-tenant support với RBAC
- WebSocket support cho real-time streaming

#### Core Services

| Service | Responsibility |
|---------|----------------|
| Session Service | Chat sessions, conversation history |
| Document Service | Upload, parsing, chunking, indexing |
| Agent Service | ReAct loop, tool orchestration |
| Retrieval Service | Hybrid search engine |

### 3. Document Processing Pipeline

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Upload  │───▶│  Parser  │───▶│ Chunking │───▶│Embedding│
│  (multi) │    │ (10+ fmt)│    │ (adaptive)   │ (batch) │
└──────────┘    └──────────┘    └──────────┘    └────┬─────┘
                                                      │
                                                      ▼
                          ┌──────────┐    ┌──────────────────┐
                          │ Knowledge │◀───│   Vector Store   │
                          │  Graph   │    │ (pgvector/etc.)  │
                          └──────────┘    └──────────────────┘
```

### 4. Retrieval Engine

#### Hybrid Search Architecture

```python
def hybrid_search(query: str, kb_id: str, options: dict):
    # 1. Vector Search (semantic)
    vector_results = vector_search(query_embedding, top_k=20)
    
    # 2. BM25 Search (keyword)
    bm25_results = bm25_search(query, top_k=20)
    
    # 3. GraphRAG Search (relationships)
    graphrag_results = graphrag_search(query, depth=3)
    
    # 4. Knowledge Graph Query
    kg_results = kg_query(query)
    
    # 5. Fusion (RRF)
    fused = reciprocal_rank_fusion(
        vector_results, 
        bm25_results,
        graphrag_results,
        kg_results
    )
    
    # 6. Reranking
    reranked = rerank(fused, query)
    
    return reranked[:top_k]
```

### 5. ReAct Agent Loop

```
┌─────────────────────────────────────────────────────────┐
│                   ReAct Agent Loop                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐           │
│  │Think│───▶│ Act │───▶│Obser│───▶│Decid│           │
│  │     │    │     │    │     │    │     │           │
│  └─────┘    └─────┘    └─────┘    └─────┘           │
│     ▲                                    │            │
│     └────────────────────────────────────┘            │
│                                                         │
│  Tools:                                                 │
│  - knowledge_search: Vector + BM25 + GraphRAG          │
│  - web_search: DuckDuckGo, Bing, Google, Tavily       │
│  - mcp_call: External MCP tools                       │
│  - final_answer: Complete task                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 6. Vector Stores Supported

| Provider | Type | Use Case |
|----------|------|----------|
| PostgreSQL + pgvector | Built-in | Small-Medium |
| Elasticsearch | External | Large scale |
| OpenSearch | External | AWS environment |
| Milvus | External | High performance |
| Weaviate | External | Graph features |
| Qdrant | External | Fast ANN |
| Apache Doris | External | Analytics |
| Tencent VectorDB | External | Enterprise |

### 7. LLM Providers

| Provider | Models | Notes |
|----------|--------|-------|
| OpenAI | GPT-4, GPT-3.5 | Cloud |
| Azure OpenAI | GPT-4, GPT-3.5 | Enterprise |
| Anthropic | Claude 3 | Cloud |
| DeepSeek | DeepSeek Chat | Cloud |
| Qwen | Qwen-Turbo, Plus | Alibaba Cloud |
| Zhipu | GLM-4 | China |
| Gemini | Gemini Pro | Google |
| Ollama | Local models | Self-hosted |

## Data Flow

### Chat Request Flow

```
User Input
    │
    ▼
┌──────────────┐
│ Input Parser │
└──────┬───────┘
       │
       ▼
┌──────────────┐    ┌─────────────┐
│ Mode Detect  │───▶│ QA Mode     │ (Simple RAG)
└──────────────┘    └─────────────┘
       │                    │
       ▼                    ▼
┌──────────────┐    ┌─────────────┐
│ Agent Mode   │───▶│ ReAct Loop  │
└──────────────┘    └─────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ Retrieve │    │ Web      │    │ MCP      │
    │ Knowledge│    │ Search   │    │ Tools    │
    └──────────┘    └──────────┘    └──────────┘
          │                │                │
          └────────────────┴────────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ LLM Generate│
                    └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Response   │
                    └─────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layer                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  Tenant     │  │    RBAC    │  │   Audit     │    │
│  │  Isolation  │  │   (4-tier) │  │    Log      │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │  AES-256-GCM Encryption                         │  │
│  │  - API keys at rest                            │  │
│  │  - MCP credentials                             │  │
│  │  - Data source credentials                     │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │  TLS + Token (gRPC between app and docreader)  │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Deployment Modes

| Mode | Components | Scalability |
|------|------------|-------------|
| Lite | Docker (all-in-one) | Development |
| Standard | Docker Compose | Small-Medium |
| Full | K8s + Helm | Enterprise |
| Cloud | WeKnora Cloud | Managed |
