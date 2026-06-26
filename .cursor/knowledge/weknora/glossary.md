# WeKnora Glossary

## Core Concepts

### RAG (Retrieval-Augmented Generation)
A technique that combines information retrieval with LLM generation. The system retrieves relevant documents from a knowledge base and uses them as context for the LLM to generate accurate, grounded responses.

### ReAct Agent
An autonomous agent that uses a Reasoning + Acting loop to solve complex tasks. It thinks about what action to take, executes it, observes the result, and repeats until the task is complete.

### Knowledge Base (KB)
A collection of documents and associated metadata that the system can search and use for answering questions. WeKnora supports three types: FAQ, Document, and Wiki.

### Wiki Mode
A WeKnora feature that automatically generates interlinked Markdown wiki pages from raw documents, with a visual knowledge graph.

## Document Processing

### Chunking
The process of splitting large documents into smaller, manageable pieces (chunks) for embedding and retrieval.

### Embedding
A numerical representation of text that captures semantic meaning. Used for vector similarity search.

### Parser
A component that extracts text and structure from various document formats (PDF, Word, etc.).

### OCR (Optical Character Recognition)
Technology that converts images of text into machine-readable text. Used for scanned documents and images.

### Parent-Child Chunking
A chunking strategy where larger "parent" chunks contain smaller "child" chunks, enabling both broad and detailed retrieval.

## Retrieval Strategies

### Vector Search
Similarity search using vector embeddings. Finds semantically similar content based on mathematical distance in embedding space.

### BM25
A keyword-based ranking function used for full-text search. Based on probabilistic relevance model.

### GraphRAG
A retrieval strategy that traverses a knowledge graph to find related entities and concepts, improving contextual understanding.

### Knowledge Graph
A graph structure of entities and relationships extracted from documents. Enables relationship-based retrieval.

### Hybrid Search
Combining multiple retrieval strategies (vector + BM25 + GraphRAG) for comprehensive results.

### Reranking
Using a more sophisticated model to reorder initial retrieval results for better relevance.

### RRF (Reciprocal Rank Fusion)
A fusion algorithm that combines rankings from multiple retrieval methods based on their reciprocal ranks.

## Agent Concepts

### Tool Calling
The ability for the agent to invoke external tools or functions to accomplish tasks.

### Web Search
Searching the internet for current information that may not be in the knowledge base.

### MCP (Model Context Protocol)
A protocol that allows LLM applications to connect with external tools and data sources.

### Human-in-the-Loop
A safety mechanism where certain agent actions require human approval before execution.

### Final Answer
A special tool that signals the agent has completed its reasoning and is ready to provide a response.

## Vector Stores

### pgvector
PostgreSQL extension for vector storage and similarity search. Built-in option for WeKnora.

### HNSW (Hierarchical Navigable Small World)
An indexing algorithm for approximate nearest neighbor search. Provides fast, high-quality similarity search.

### ANN (Approximate Nearest Neighbor)
Search algorithms that find approximately similar vectors much faster than exact search, with acceptable accuracy trade-offs.

## LLM Concepts

### Temperature
A parameter controlling randomness in LLM output. Lower values = more deterministic, higher = more creative.

### Context Window
The maximum amount of text (measured in tokens) that an LLM can process in a single request.

### Token
The basic unit of text that LLMs process. Roughly 1 token = 4 characters in English.

### Embedding Model
A specialized LLM designed to convert text into vector embeddings for similarity search.

### Thinking Mode
A feature in some LLMs (like Claude) that shows the model's reasoning process before giving the final answer.

## Multi-Tenant

### RBAC (Role-Based Access Control)
A security model where access is determined by user roles (Owner, Admin, Contributor, Viewer).

### Tenant
A self-contained environment for an organization, with isolated data and settings.

### Audit Log
A record of all actions taken within the system, important for compliance and security.

## API & Integration

### CLI (Command-Line Interface)
The `weknora` command-line tool for interacting with the system programmatically.

### REST API
HTTP-based API for programmatic access to WeKnora functionality.

### WebSocket
A bidirectional communication channel for real-time features like streaming responses.

### Streaming
Sending responses incrementally as they are generated, rather than waiting for the complete response.

## Security

### AES-256-GCM
A strong encryption algorithm used for securing API keys and credentials at rest.

### TLS (Transport Layer Security)
Encryption for data in transit. Protects against eavesdropping and tampering.

### SSRF (Server-Side Request Forgery)
A security vulnerability where an attacker can make the server perform unintended requests.

### gRPC
A high-performance RPC framework used internally for communication between services.

## Evaluation

### Recall
The fraction of relevant documents that were retrieved. Measures completeness of retrieval.

### Precision
The fraction of retrieved documents that are relevant. Measures accuracy of retrieval.

### MRR (Mean Reciprocal Rank)
The average of the reciprocal ranks of the first relevant result in the retrieved list.

### NDCG (Normalized Discounted Cumulative Gain)
A metric that measures the quality of ranking, considering both relevance and position.

### BLEU/ROUGE
Metrics for comparing generated text against reference text, commonly used in summarization evaluation.

## Deployment

### Docker Compose
A tool for defining and running multi-container Docker applications.

### Helm
A package manager for Kubernetes that simplifies deploying complex applications.

### Profile
Docker Compose profiles for enabling optional services (neo4j, minio, langfuse).

### Fast Development Mode
A development workflow where code changes are applied without rebuilding Docker images.
