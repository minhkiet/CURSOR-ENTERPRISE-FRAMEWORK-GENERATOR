# WeKnora Anti-Patterns

## 1. Document Processing Anti-Patterns

### ❌ Wrong: Ignoring Document Structure

```python
# Bad: Flatten everything
def bad_chunking(text):
    return [text[i:i+1000] for i in range(0, len(text), 1000)]

# Problems:
# - Breaks semantic units (paragraphs, sections)
# - No metadata preservation
# - Loses context relationships
```

### ✅ Right: Preserve Structure

```python
# Good: Structure-aware chunking
def smart_chunking(document):
    chunks = []
    for section in document.sections:
        if len(section.text) < 500:
            chunks.append(Chunk(
                content=section.text,
                metadata={
                    "heading": section.heading,
                    "level": section.level,
                    "page": section.page
                }
            ))
        else:
            # Split by paragraphs within section
            for para in section.paragraphs:
                chunks.append(Chunk(
                    content=para.text,
                    metadata={
                        "heading": section.heading,
                        "paragraph_index": para.index
                    }
                ))
    return chunks
```

## 2. Retrieval Anti-Patterns

### ❌ Wrong: Single Retrieval Strategy

```python
# Bad: Only vector search
def bad_retrieval(query):
    embedding = get_embedding(query)
    return vector_db.search(embedding, top_k=10)
```

### ✅ Right: Hybrid Retrieval

```python
# Good: Combine multiple strategies
def hybrid_retrieval(query, weights=None):
    weights = weights or DEFAULT_WEIGHTS
    
    # 1. Vector search (semantic)
    vector_results = vector_search(query, top_k=20)
    
    # 2. BM25 search (keyword)
    bm25_results = bm25_search(query, top_k=20)
    
    # 3. GraphRAG (relationships)
    graphrag_results = graphrag_search(query, depth=3)
    
    # 4. Knowledge Graph (entities)
    kg_results = kg_search(query)
    
    # 5. RRF Fusion
    return reciprocal_rank_fusion(
        vector_results,
        bm25_results,
        graphrag_results,
        kg_results,
        weights=weights
    )
```

### ❌ Wrong: No Reranking

```python
# Bad: Trust initial retrieval
results = vector_search(query, top_k=10)
return results  # May include irrelevant results
```

### ✅ Right: Rerank Results

```python
# Good: Cross-encoder reranking
def smart_retrieval(query, initial_k=50, final_k=10):
    # Get more candidates
    candidates = vector_search(query, top_k=initial_k)
    
    # Rerank with cross-encoder
    reranked = cross_encoder.rerank(
        query=query,
        documents=[c.content for c in candidates],
        top_k=final_k
    )
    
    # Map back scores
    return [candidates[r.index] for r in reranked]
```

## 3. Agent Anti-Patterns

### ❌ Wrong: No Loop Prevention

```python
# Bad: Infinite loop risk
async def bad_agent(user_input):
    while True:
        thought = await llm.think(...)
        if thought.action == "final_answer":
            return thought.result
        await execute_tool(thought.tool, thought.params)
```

### ✅ Right: Bounded Loop

```python
# Good: Controlled iteration
async def bounded_agent(user_input, max_steps=10):
    for step in range(max_steps):
        thought = await llm.think(context)
        
        if thought.action == "final_answer":
            return thought.result
        
        if step == max_steps - 1:
            # Max steps reached
            return await generate_fallback_response(context)
        
        result = await execute_tool(thought.tool, thought.params)
        context.add_result(result)
```

### ❌ Wrong: No Error Handling

```python
# Bad: Silent failures
async def no_error_handling(query):
    results = await vector_search(query)  # What if this fails?
    return await llm.respond(query, results)  # What if LLM fails?
```

### ✅ Right: Graceful Degradation

```python
# Good: Robust error handling
async def robust_agent(query):
    try:
        results = await vector_search(query)
    except VectorDBError:
        logger.error("Vector search failed, using fallback")
        results = await fallback_search(query)
    
    try:
        return await llm.respond(query, results)
    except RateLimitError:
        # Wait and retry
        await asyncio.sleep(60)
        return await llm.respond(query, results)
    except LLMError as e:
        logger.error(f"LLM error: {e}")
        return generate_simple_response(query)
```

## 4. Chunking Anti-Patterns

### ❌ Wrong: Fixed-Size Chunks

```python
# Bad: One size fits all
def fixed_chunking(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
```

### ✅ Right: Adaptive Chunking

```python
# Good: Content-aware chunking
def adaptive_chunking(document):
    chunks = []
    
    # Determine chunk size based on content type
    if document.type == "faq":
        chunk_size = 256  # Small chunks for Q&A
    elif document.type == "technical":
        chunk_size = 512  # Medium for technical docs
    else:
        chunk_size = 1024  # Large for long-form
    
    for section in document.sections:
        # Respect semantic boundaries
        if len(section.text) <= chunk_size * 1.5:
            chunks.append(section)
        else:
            # Split by paragraphs
            chunks.extend(split_by_paragraph(section, chunk_size))
    
    return chunks
```

## 5. Embedding Anti-Patterns

### ❌ Wrong: Single Embedding Model

```python
# Bad: No fallback
embedder = OpenAIEmbedder(model="text-embedding-3-small")
# If OpenAI is down, everything fails
```

### ✅ Right: Multi-Provider Strategy

```python
# Good: Fallback chain
class ResilientEmbedder:
    def __init__(self):
        self.providers = [
            OpenAIEmbedder(),
            OllamaEmbedder(),  # Local fallback
        ]
    
    async def embed(self, text):
        for provider in self.providers:
            try:
                return await provider.embed(text)
            except ProviderError:
                continue
        raise AllProvidersFailedError()
```

## 6. LLM Integration Anti-Patterns

### ❌ Wrong: Hardcoded Model

```python
# Bad: No flexibility
async def respond(query, context):
    return await openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
        ]
    )
```

### ✅ Right: Configurable LLM

```python
# Good: Provider abstraction
class LLMManager:
    def __init__(self, config: LLMConfig):
        self.providers = {
            "openai": OpenAIProvider(config.openai),
            "deepseek": DeepSeekProvider(config.deepseek),
            "ollama": OllamaProvider(config.ollama),
        }
        self.primary = config.primary
        self.fallbacks = config.fallbacks
    
    async def complete(self, prompt, **kwargs):
        for provider_name in [self.primary] + self.fallbacks:
            try:
                return await self.providers[provider_name].complete(prompt, **kwargs)
            except ProviderError:
                continue
        raise NoProviderAvailableError()
```

## 7. Caching Anti-Patterns

### ❌ Wrong: No Cache

```python
# Bad: Recompute everything
async def slow_search(query):
    embedding = await get_embedding(query)  # Same query = new embedding
    return await vector_search(embedding)
```

### ✅ Right: Smart Caching

```python
# Good: Multi-layer cache
class CachedSearch:
    def __init__(self):
        self.embedding_cache = RedisCache(ttl=3600)
        self.retrieval_cache = RedisCache(ttl=300)
    
    async def search(self, query):
        # Cache embedding
        query_hash = hash(query)
        embedding = self.embedding_cache.get(query_hash)
        
        if not embedding:
            embedding = await get_embedding(query)
            self.embedding_cache.set(query_hash, embedding)
        
        # Cache retrieval results
        cache_key = f"{query_hash}:{get_kb_version()}"
        results = self.retrieval_cache.get(cache_key)
        
        if not results:
            results = await vector_search(embedding)
            self.retrieval_cache.set(cache_key, results)
        
        return results
```

## 8. Evaluation Anti-Patterns

### ❌ Wrong: No Metrics

```python
# Bad: Hope for the best
async def deploy_rag():
    # No evaluation
    # Hope users don't complain
    pass
```

### ✅ Right: Comprehensive Metrics

```python
# Good: Measure everything
class RAGEvaluator:
    async def evaluate(self, test_set):
        results = []
        
        for query, expected in test_set:
            # Retrieval metrics
            retrieved = await self.retrieval.search(query)
            retrieval_metrics = self.compute_retrieval_metrics(
                retrieved, expected["relevant_docs"]
            )
            
            # Generation metrics
            response = await self.generate(query, retrieved)
            generation_metrics = self.compute_generation_metrics(
                response, expected["answer"]
            )
            
            results.append({
                "query": query,
                "retrieval": retrieval_metrics,
                "generation": generation_metrics,
                "latency": measure_time(),
            })
        
        return self.aggregate_metrics(results)
    
    def compute_retrieval_metrics(self, retrieved, relevant):
        return {
            "precision": len(set(retrieved) & set(relevant)) / len(retrieved),
            "recall": len(set(retrieved) & set(relevant)) / len(relevant),
            "mrr": self.mean_reciprocal_rank(retrieved, relevant),
            "ndcg": self.ndcg(retrieved, relevant),
        }
```

## 9. Multi-Tenant Anti-Patterns

### ❌ Wrong: Shared Everything

```python
# Bad: No isolation
class SharedVectorStore:
    async def insert(self, tenant_id, doc):
        # tenant_id ignored!
        await self.db.insert(doc)
```

### ✅ Right: Tenant Isolation

```python
# Good: Namespace per tenant
class IsolatedVectorStore:
    async def insert(self, tenant_id, doc):
        # Add tenant prefix to namespace
        namespace = f"tenant_{tenant_id}"
        await self.vector_db.upsert(
            namespace=namespace,
            vectors=[doc.vector],
            metadata={"doc_id": doc.id, "tenant": tenant_id}
        )
    
    async def search(self, tenant_id, query):
        # Only search within tenant namespace
        return await self.vector_db.search(
            namespace=f"tenant_{tenant_id}",
            vector=query.vector,
            filter={"tenant": tenant_id}  # Double-check
        )
```

## 10. Security Anti-Patterns

### ❌ Wrong: Plaintext API Keys

```python
# Bad: Exposed secrets
API_KEY = "sk-1234567890abcdef"
# Stored in source code!
```

### ✅ Right: Secure Key Management

```python
# Good: Encrypted storage
class SecureKeyManager:
    def __init__(self, encryption_key):
        self.cipher = AESGCM(encryption_key)
    
    def store_key(self, user_id, provider, encrypted_key):
        # Store only encrypted keys in DB
        db.keys.insert({
            "user_id": user_id,
            "provider": provider,
            "encrypted_key": encrypted_key
        })
    
    def get_key(self, user_id, provider):
        record = db.keys.get(user_id=user_id, provider=provider)
        # Decrypt on retrieval
        return self.cipher.decrypt(record.encrypted_key)
```
