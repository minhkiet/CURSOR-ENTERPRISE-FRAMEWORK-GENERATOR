# WeKnora Best Practices

## 1. Document Ingestion

### Supported Formats

| Format | Parser | Notes |
|--------|--------|-------|
| PDF | Built-in / PaddleOCR | Best for scanned docs |
| Word (.docx) | Built-in | Preserves formatting |
| Markdown | Built-in | Direct processing |
| HTML | Built-in | Web scraping |
| Images | PaddleOCR-VL | OCR for scanned |
| CSV | Built-in | Tabular data |
| Excel | Built-in | Multi-sheet support |
| PowerPoint | Built-in | Slides as pages |
| JSON | Built-in | Structured data |
| Text | Built-in | Plain text |

### Chunking Strategies

```yaml
# Adaptive 3-tier chunking
chunking:
  tier_1_small:
    chunk_size: 256
    overlap: 50
    for: "Q&A, FAQ"
  
  tier_2_medium:
    chunk_size: 512
    overlap: 100
    for: "General documents"
  
  tier_3_large:
    chunk_size: 1024
    overlap: 200
    for: "Long-form content"
  
  # Parent-child chunking
  parent_child:
    parent_size: 2048
    child_size: 512
    for: "Detailed retrieval"
```

### Per-Upload Process Config

```json
{
  "upload_id": "batch-001",
  "parser": "paddleocr",  // or "builtin", "opendata"
  "chunking": {
    "strategy": "adaptive",
    "tier": "tier_2_medium"
  },
  "multimodal": {
    "enabled": true,
    "vlm": "gpt-4-vision",  // for image understanding
    "ocr": "paddleocr"      // for text extraction
  },
  "graph": {
    "extract_entities": true,
    "extract_relationships": true
  },
  "qa_generation": {
    "enabled": true,
    "count": 5  // Generate Q&A pairs
  }
}
```

## 2. Knowledge Base Configuration

### FAQ KB

```yaml
kb_config:
  type: faq
  features:
    - structured_qa
    - intent_routing
    - confidence_scoring
  retrieval:
    top_k: 3  # Return top 3 matches
    threshold: 0.7
```

### Document KB

```yaml
kb_config:
  type: document
  features:
    - full_text_search
    - semantic_search
    - citation_generation
  retrieval:
    top_k: 10
    include_citations: true
```

### Wiki KB

```yaml
kb_config:
  type: wiki
  features:
    - auto_generation
    - entity_extraction
    - relationship_mapping
    - knowledge_graph
  generation:
    style: "technical"  # or "casual", "academic"
    structure: "hierarchical"
    linking: true  # Auto-link related pages
```

## 3. Retrieval Optimization

### Hybrid Search Weights

```python
# Default weights
WEIGHTS = {
    "vector": 0.4,      # Semantic similarity
    "bm25": 0.3,       # Keyword matching
    "graphrag": 0.2,   # Graph traversal
    "knowledge_graph": 0.1  # Entity query
}

# Tuning for different use cases
FAQ_WEIGHTS = {
    "vector": 0.3,
    "bm25": 0.5,      # FAQ needs exact keywords
    "graphrag": 0.1,
    "knowledge_graph": 0.1
}

TECHNICAL_WEIGHTS = {
    "vector": 0.5,     # Technical docs need semantic
    "bm25": 0.2,
    "graphrag": 0.2,
    "knowledge_graph": 0.1
}
```

### Reranking Configuration

```yaml
rerank:
  enabled: true
  model: "cross-encoder/ms-marco"  # or proprietary
  top_k_initial: 50  # Retrieve 50, rerank top 10
  top_k_final: 10
  weights:
    relevance: 0.7
    novelty: 0.2
    coverage: 0.1
```

## 4. Agent Configuration

### ReAct Settings

```yaml
agent:
  model: "gpt-4-turbo"
  temperature: 0.3  # Lower for factual
  max_steps: 10     # Prevent infinite loops
  thinking_mode: "chain"  # or "tree"
  
  tools:
    - name: "knowledge_search"
      max_results: 5
      fallback_to_web: true
    
    - name: "web_search"
      provider: "duckduckgo"
      max_results: 3
    
    - name: "final_answer"
      requires_confirmation: false
  
  safety:
    human_in_the_loop: true  # Approve sensitive actions
    max_tool_calls: 20
```

### Tool Calling Patterns

```python
# Parallel tool calling
async def execute_tools_parallel(tools: List[str], params: dict):
    tasks = [call_tool(t, params) for t in tools]
    results = await asyncio.gather(*tasks)
    return results

# Sequential with dependency
async def execute_tools_sequential(tools: List[dict]):
    results = {}
    for tool in tools:
        if tool.get("depends_on"):
            tool["params"]["context"] = results[tool["depends_on"]]
        result = await call_tool(tool["name"], tool["params"])
        results[tool["name"]] = result
    return results
```

## 5. LLM Provider Selection

### Decision Matrix

| Use Case | Primary | Fallback |
|----------|---------|----------|
| General Q&A | OpenAI GPT-4 | DeepSeek |
| Code Review | Claude 3 | GPT-4 |
| Chinese Content | Qwen / Zhipu | GPT-4 |
| Self-hosted | Ollama (Llama) | - |
| Cost-sensitive | DeepSeek | Ollama |
| Long Context | Claude 3 | GPT-4-128k |

### Multi-Provider Config

```yaml
llm:
  primary: "openai"
  fallback:
    - "deepseek"
    - "ollama"
  
  per_model_settings:
    "gpt-4-turbo":
      temperature: 0.3
      max_tokens: 4096
      thinking_mode: true
    
    "claude-3-opus":
      temperature: 0.3
      max_tokens: 4096
      thinking_mode: true
  
  timeout: 60  # seconds
  retry: 3
```

## 6. Performance Optimization

### Caching Strategy

```python
CACHE_CONFIG = {
    "embedding_cache": {
        "type": "redis",
        "ttl": 3600,  # 1 hour
        "max_size": "10GB"
    },
    "retrieval_cache": {
        "type": "redis",
        "ttl": 300,  # 5 minutes
        "invalidate_on_update": True
    },
    "llm_response_cache": {
        "type": "redis",
        "ttl": 1800,  # 30 minutes
        "key_template": "llm:{hash(query)}:{kb_id}"
    }
}
```

### Batch Processing

```python
# Batch document processing
BATCH_CONFIG = {
    "upload_batch_size": 100,  # Documents per batch
    "embedding_batch_size": 32,  # Texts per API call
    "indexing_workers": 4,
    "queue_processing": True
}

async def process_documents_batch(docs: List[Document]):
    # 1. Parse all documents
    parsed = await parse_all(docs)
    
    # 2. Chunk in parallel
    chunks = await chunk_all_parallel(parsed, workers=4)
    
    # 3. Generate embeddings batch
    embeddings = await embed_batch(chunks, batch_size=32)
    
    # 4. Index to vector store
    await index_batch(chunks, embeddings)
    
    return {"chunks": len(chunks), "status": "complete"}
```

## 7. Multi-Tenant Configuration

### RBAC Matrix

| Role | Permissions |
|------|-------------|
| Owner | Full access, manage billing, delete tenant |
| Admin | Manage users, KB, settings |
| Contributor | Upload docs, create KB, chat |
| Viewer | Read-only KB access, chat |

### Tenant Isolation

```yaml
tenant:
  isolation: "strict"
  
  shared_resources:
    - "LLM models"
    - "Embedding services"
  
  dedicated_resources:
    - "Knowledge bases"
    - "Chat sessions"
    - "Documents"
    - "Vector indices"
  
  cross_tenant: false  # No shared KBs
```

## 8. Monitoring & Observability

### Langfuse Integration

```yaml
langfuse:
  enabled: true
  public_key: "${LANGFUSE_PUBLIC_KEY}"
  secret_key: "${LANGFUSE_SECRET_KEY}"
  host: "http://localhost:3000"
  
  trace:
    - "agent_reasoning"
    - "tool_calls"
    - "retrieval_latency"
    - "llm_token_usage"
    - "document_parsing"
```

### Key Metrics

| Metric | Target | Alert |
|--------|--------|-------|
| Retrieval Latency (p95) | < 200ms | > 500ms |
| LLM Response Time | < 3s | > 10s |
| Indexing Throughput | > 100 docs/min | < 50 docs/min |
| Cache Hit Rate | > 80% | < 60% |
| Error Rate | < 0.1% | > 1% |

## 9. Security Best Practices

### API Key Management

```python
# Use AES-256-GCM encryption for stored keys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class SecureKeyStore:
    def __init__(self, key: bytes):
        self.aesgcm = AESGCM(key)
    
    def store(self, key_id: str, api_key: str) -> None:
        encrypted = self.aesgcm.encrypt(
            nonce=os.urandom(12),
            data=api_key.encode()
        )
        # Store encrypted key in DB
        db.set(f"key:{key_id}", encrypted)
    
    def retrieve(self, key_id: str) -> str:
        encrypted = db.get(f"key:{key_id}")
        return self.aesgcm.decrypt(encrypted).decode()
```

### Network Security

```yaml
security:
  tls:
    min_version: "1.2"
    cert_path: "/path/to/cert"
    key_path: "/path/to/key"
  
  grpc_tls:
    enabled: true
    between_app_and_docreader: true
  
  ssrf_protection:
    enabled: true
    allowed_domains: ["trusted-sources.com"]
```

## 10. Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Slow indexing | Large docs | Enable batch mode |
| Poor retrieval | Wrong weights | Tune hybrid weights |
| Hallucinations | Weak context | Increase top_k |
| Rate limits | LLM throttling | Add retry + backoff |
| OOM errors | Large embeddings | Reduce batch size |

### Debug Commands

```bash
# Check service health
docker compose ps

# View logs
docker compose logs -f weknora

# Test MCP connection
weknora mcp status

# Rebuild index
weknora kb rebuild --kb "my-kb"

# Clear cache
weknora cache clear
```
