# WeKnora Checklist

## Pre-Deployment

### Environment Setup
- [ ] Docker and Docker Compose installed
- [ ] Git installed
- [ ] Minimum 4GB RAM available
- [ ] 20GB disk space available
- [ ] Network ports available (80, 8080, 3000 for Langfuse)

### Configuration
- [ ] Copied `.env.example` to `.env`
- [ ] Set `SECRET_KEY` for session encryption
- [ ] Configured `WEKNORA_HOST`
- [ ] Set up LLM provider API keys
- [ ] Configured vector database settings
- [ ] Set up storage (local/S3/MinIO)

## Knowledge Base Setup

### KB Creation
- [ ] Created new Knowledge Base
- [ ] Selected KB type (FAQ/Document/Wiki)
- [ ] Configured KB name and description
- [ ] Set up KB permissions

### LLM Configuration
- [ ] Selected primary LLM provider
- [ ] Configured API key/credentials
- [ ] Set fallback LLM provider
- [ ] Tested LLM connectivity

### Vector Store Setup
- [ ] Selected vector database
- [ ] Configured connection settings
- [ ] Set embedding model
- [ ] Configured indexing parameters

## Document Ingestion

### Upload
- [ ] Uploaded sample documents
- [ ] Verified file format compatibility
- [ ] Set upload batch size

### Processing
- [ ] Selected parser (builtin/paddleocr/opendata)
- [ ] Configured chunking strategy
- [ ] Set chunk size and overlap
- [ ] Enabled metadata extraction
- [ ] Configured OCR for images

### Indexing
- [ ] Verified embedding generation
- [ ] Checked vector storage
- [ ] Validated index health
- [ ] Confirmed search functionality

## Retrieval Configuration

### Hybrid Search
- [ ] Enabled vector search
- [ ] Enabled BM25 search
- [ ] Configured GraphRAG (if using)
- [ ] Set Knowledge Graph integration
- [ ] Configured fusion weights

### Reranking
- [ ] Enabled reranking
- [ ] Selected rerank model
- [ ] Set initial retrieval count
- [ ] Configured final result count

## Agent Configuration

### Basic Setup
- [ ] Selected agent mode
- [ ] Configured LLM settings
- [ ] Set max steps (loop prevention)
- [ ] Configured temperature

### Tools
- [ ] Enabled knowledge search
- [ ] Configured web search provider
- [ ] Added MCP tools (if needed)
- [ ] Set up tool permissions

### Safety
- [ ] Enabled human-in-the-loop (if required)
- [ ] Set max tool calls per session
- [ ] Configured content filtering

## MCP Integration

### Server Setup
- [ ] Installed WeKnora CLI
- [ ] Configured MCP transport (stdio/SSE/HTTP)
- [ ] Set authentication
- [ ] Tested MCP connection

### Cursor Integration
- [ ] Added WeKnora to Cursor MCP config
- [ ] Verified tool availability
- [ ] Tested tool execution

## Multi-Tenant (Enterprise)

### Tenant Management
- [ ] Created tenant
- [ ] Configured tenant settings
- [ ] Set up RBAC roles
- [ ] Assigned user permissions

### Security
- [ ] Enabled API key encryption
- [ ] Configured TLS settings
- [ ] Set up audit logging
- [ ] Enabled SSRF protection

## Testing

### Unit Tests
- [ ] Document parsing tested
- [ ] Chunking logic tested
- [ ] Embedding generation tested
- [ ] Retrieval tested

### Integration Tests
- [ ] End-to-end Q&A flow tested
- [ ] Agent mode tested
- [ ] Web search tested
- [ ] MCP tools tested

### Performance Tests
- [ ] Retrieval latency measured
- [ ] Throughput tested
- [ ] Memory usage checked
- [ ] Cache efficiency verified

## Monitoring

### Observability
- [ ] Langfuse configured (optional)
- [ ] Logging configured
- [ ] Metrics collection enabled
- [ ] Alerting set up

### Health Checks
- [ ] API health endpoint tested
- [ ] Vector store connection tested
- [ ] LLM connectivity tested
- [ ] Storage available

## Deployment

### Docker Deployment
- [ ] Docker images pulled
- [ ] Services started
- [ ] Health checks passing
- [ ] Web UI accessible

### Optional Services
- [ ] Neo4j deployed (Knowledge Graph)
- [ ] MinIO deployed (Object Storage)
- [ ] Langfuse deployed (Tracing)

## Production Checklist

### Security
- [ ] Changed default passwords
- [ ] Enabled HTTPS/TLS
- [ ] Configured firewall rules
- [ ] Set up backup strategy
- [ ] API rate limiting enabled

### Scalability
- [ ] Load balancer configured (if needed)
- [ ] Database scaling planned
- [ ] Vector store scaling configured
- [ ] CDN configured (if needed)

### Maintenance
- [ ] Documented deployment
- [ ] Set up monitoring dashboards
- [ ] Created runbooks
- [ ] Planned update schedule
