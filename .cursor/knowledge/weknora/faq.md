# WeKnora FAQ

## General Questions

### What is WeKnora?
WeKnora is an open-source LLM knowledge platform developed by Tencent that enables organizations to turn raw documents into queryable knowledge bases, autonomous reasoning agents, and self-maintaining wikis. It supports RAG-based Q&A, ReAct agents, and automatic wiki generation.

### How does WeKnora compare to other RAG solutions?
| Feature | WeKnora | Generic RAG | Commercial Solutions |
|---------|----------|------------|---------------------|
| Document Formats | 10+ built-in | Limited | Variable |
| Hybrid Search | Vector + BM25 + GraphRAG | Vector only | Often extra cost |
| Agent Mode | Native ReAct | Requires custom | Often extra cost |
| Wiki Mode | Auto-generated | Not supported | Not supported |
| MCP Tools | Built-in | Not supported | Variable |
| Multi-tenant | Built-in RBAC | Custom | Usually extra |
| Self-hosted | Full | Full | Often cloud-only |

### What are the system requirements?
- **Minimum**: 4GB RAM, 20GB disk
- **Recommended**: 8GB+ RAM, 100GB+ SSD
- **GPU**: Optional (for local embedding models)

### Is WeKnora free to use?
Yes, WeKnora is MIT licensed. You can self-host for free.

## Deployment Questions

### What's the difference between Docker profiles?
| Profile | Services | Use Case |
|---------|----------|----------|
| (default) | Core services only | Basic usage |
| full | All services | Complete setup |
| neo4j | + Neo4j | Knowledge Graph |
| minio | + MinIO | Object Storage |
| langfuse | + Langfuse | Tracing |

### Can I run WeKnora without Docker?
Yes, but Docker is recommended. You can run the Go backend directly with:
```bash
# Build from source
go build -o weknora ./cmd/server

# Run
./weknora serve
```

### How do I update WeKnora?
```bash
# Pull latest
git pull

# Rebuild
docker compose build

# Restart
docker compose up -d
```

## Knowledge Base Questions

### What's the difference between KB types?
- **FAQ**: Optimized for Q&A pairs with intent routing
- **Document**: General purpose full-text + semantic search
- **Wiki**: Auto-generates interlinked Markdown pages with knowledge graph

### How do I choose chunk size?
| Content Type | Recommended Size |
|--------------|------------------|
| Q&A / FAQ | 256 tokens |
| Technical docs | 512 tokens |
| Long articles | 1024 tokens |

### Can I upload scanned PDFs?
Yes, WeKnora supports OCR via:
- Built-in parser (basic)
- PaddleOCR (better quality)
- PaddleOCR-VL (multimodal)

## LLM Provider Questions

### Which LLM should I use?
| Use Case | Recommended |
|----------|-------------|
| Best quality | Claude 3 / GPT-4 |
| Cost-effective | DeepSeek |
| Self-hosted | Ollama (Llama/Mistral) |
| Chinese content | Qwen / Zhipu |

### Can I use local models?
Yes, via Ollama integration:
```yaml
llm:
  provider: "ollama"
  model: "llama3"
  base_url: "http://localhost:11434"
```

### How do I handle rate limits?
WeKnora handles retries automatically with exponential backoff. For high-volume usage, consider:
1. Multiple LLM providers with fallback
2. Caching frequent queries
3. Rate limit configuration

## Retrieval Questions

### Why use hybrid search?
Vector search finds semantically similar content but misses exact keyword matches. BM25 handles exact matches. Combining both gives best results.

### What is GraphRAG?
GraphRAG traverses a knowledge graph to find related entities. It improves contextual understanding for complex queries involving relationships.

### How do I improve retrieval quality?
1. Tune hybrid weights
2. Enable reranking
3. Use parent-child chunking
4. Improve document structure
5. Add metadata filters

## Agent Questions

### What's the difference between QA and Agent mode?
| Feature | QA Mode | Agent Mode |
|---------|---------|------------|
| Response time | Fast | Slower |
| Multi-step reasoning | No | Yes |
| Web search | No | Yes |
| MCP tools | No | Yes |
| Use case | Simple Q&A | Complex tasks |

### How does ReAct work?
```
1. Think: Reason about current state
2. Act: Choose and execute tool
3. Observe: Get result
4. Repeat until task complete
```

### Can I add custom tools?
Yes, via MCP (Model Context Protocol):
```bash
# Add MCP server
weknora mcp add --name my-tool --command "npx my-mcp-server"
```

## MCP Integration Questions

### How do I connect WeKnora to Cursor?
1. Install CLI: `brew install weknora` or download binary
2. Start MCP server: `weknora mcp serve`
3. Configure Cursor MCP in settings
4. Authenticate: `weknora auth login`

### What MCP transports are supported?
- **stdio**: Local CLI (recommended for Cursor)
- **SSE**: Server-Sent Events
- **HTTP**: REST API

## Security Questions

### How are API keys secured?
All API keys are encrypted with AES-256-GCM before storage. Keys are decrypted only when needed and never logged.

### Is multi-tenant data isolated?
Yes. Each tenant has:
- Isolated vector store namespace
- Separate RBAC policies
- Independent audit logs

### Can I use WeKnora offline?
Yes, WeKnora is designed for self-hosting with full offline capability.

## Troubleshooting

### Documents not indexing?
1. Check file format is supported
2. Verify file isn't corrupted
3. Check disk space
4. Review logs: `docker compose logs | grep index`

### Slow retrieval?
1. Enable caching
2. Reduce top_k
3. Optimize vector index (HNSW parameters)
4. Scale vector store

### LLM errors?
1. Verify API key
2. Check rate limits
3. Review network connectivity
4. Enable fallback provider

## Performance Questions

### How many documents can WeKnora handle?
| Deployment | Document Limit |
|------------|----------------|
| Docker (local) | ~10,000 |
| Docker (optimized) | ~100,000 |
| Kubernetes | 1M+ |

### What's the typical latency?
| Operation | Latency (p95) |
|-----------|---------------|
| Simple retrieval | < 100ms |
| Hybrid search | < 200ms |
| Agent reasoning | 2-5s |
| Document parsing | 1-10s |

### How do I scale WeKnora?
1. Scale vector store horizontally
2. Add caching layer (Redis)
3. Use CDN for static assets
4. Scale Kubernetes pods
5. Use managed LLM services
