---
title: "Embedding Pipeline"
description: "Hướng dẫn xây dựng embedding pipeline: model selection, batch processing, async embedding và quality vs speed tradeoffs"
tags: ["embedding", "pipeline", "batch-processing", "async", "llm", "model-selection"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Embedding Pipeline

## Tổng Quan

Embedding pipeline là thành phần cốt lõi trong bất kỳ RAG system nào, chịu trách nhiệm chuyển đổi documents thành numerical vectors mà các vector search engines có thể sử dụng. Quality của embeddings ảnh hưởng trực tiếp đến retrieval quality và cuối cùng là answer quality của LLM.

Việc xây dựng một embedding pipeline hiệu quả đòi hỏi hiểu biết về:
- Các embedding models khác nhau và use cases phù hợp
- Batch processing để optimize throughput
- Async operations để handle large volumes
- Quality vs speed tradeoffs trong production

Một embedding pipeline tốt không chỉ generate embeddings nhanh mà còn đảm bảo consistency, reliability, và easy maintenance trong production environment.

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức toàn diện về embedding pipeline:

Đầu tiên, chúng ta sẽ tìm hiểu cách lựa chọn embedding model phù hợp với use case và budget.

Thứ hai, tài liệu hướng dẫn các kỹ thuật batch processing để maximize throughput.

Thứ ba, chúng ta sẽ đề cập đến async embedding cho production workloads.

Cuối cùng, tài liệu cung cấp strategies để balance giữa quality và speed.

## Key Concepts

### 1. Embedding Model Overview

Embedding models convert text (hoặc other modalities) thành dense vectors trong high-dimensional space. Các models phổ biến:

```python
# Popular embedding models (2024)
EMBEDDING_MODELS = {
    # OpenAI
    "text-embedding-3-large": {
        "dimensions": 3072,
        "max_tokens": 8192,
        "price_per_1k": 0.00013,
        "use_case": "High-quality semantic search"
    },
    "text-embedding-3-small": {
        "dimensions": 1536,
        "max_tokens": 8192,
        "price_per_1k": 0.00002,
        "use_case": "Cost-effective general purpose"
    },
    "text-embedding-ada-002": {
        "dimensions": 1536,
        "max_tokens": 8191,
        "price_per_1k": 0.0001,
        "use_case": "Legacy, use 3-small instead"
    },
    
    # Cohere
    "embed-english-v3.0": {
        "dimensions": 1024,
        "max_tokens": 512,
        "price_per_1k": 0.0001,
        "use_case": "English semantic search"
    },
    "embed-multilingual-v3.0": {
        "dimensions": 1024,
        "max_tokens": 512,
        "price_per_1k": 0.0001,
        "use_case": "Multi-language support"
    },
    
    # Open Source
    "sentence-transformers/all-MiniLM-L6-v2": {
        "dimensions": 384,
        "max_tokens": 256,
        "price_per_1k": 0,  # Local inference
        "use_case": "Fast, local deployment"
    },
    "sentence-transformers/all-mpnet-base-v2": {
        "dimensions": 768,
        "max_tokens": 384,
        "price_per_1k": 0,
        "use_case": "High quality local"
    }
}
```

### 2. Model Selection Criteria

```python
def select_embedding_model(
    use_case: str,
    budget: str,
    latency_requirement: str,
    language: str = "english"
) -> dict:
    """
    Select appropriate embedding model based on requirements.
    """
    
    # Define requirements mapping
    if use_case == "code_search":
        return {
            "model": "cursor/fast-embed-code",
            "dimensions": 768,
            "reason": "Specialized for code"
        }
    
    if language != "english":
        return {
            "model": "Cohere/embed-multilingual-v3.0",
            "dimensions": 1024,
            "reason": "Best multilingual support"
        }
    
    if budget == "low" or budget == "minimal":
        return {
            "model": "sentence-transformers/all-MiniLM-L6-v2",
            "dimensions": 384,
            "reason": "Free, fast local inference"
        }
    
    if latency_requirement == "ultra_low":
        return {
            "model": "sentence-transformers/all-MiniLM-L6-v2",
            "dimensions": 384,
            "reason": "Fast local inference"
        }
    
    if quality_requirement == "maximum":
        return {
            "model": "text-embedding-3-large",
            "dimensions": 3072,
            "reason": "Highest quality proprietary"
        }
    
    # Default: balanced option
    return {
        "model": "text-embedding-3-small",
        "dimensions": 1536,
        "reason": "Good balance of quality and cost"
    }
```

## Batch Processing

### 1. Basic Batch Embedding

```python
import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass
import time

@dataclass
class EmbeddingRequest:
    """Single embedding request."""
    id: str
    text: str
    metadata: Optional[dict] = None

@dataclass
class EmbeddingResult:
    """Embedding result."""
    id: str
    embedding: List[float]
    metadata: Optional[dict] = None
    latency_ms: float = 0

class BatchEmbeddingProcessor:
    """
    Process embeddings in batches for efficiency.
    """
    
    def __init__(
        self,
        model_client,
        batch_size: int = 100,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        self.client = model_client
        self.batch_size = batch_size
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    async def embed_batch(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Embed a batch of texts.
        """
        if not texts:
            return []
        
        # API-specific batch call
        response = await self.client.embed(
            texts=texts,
            model="text-embedding-3-small"
        )
        
        return response["embeddings"]
    
    async def process_items(
        self,
        items: List[EmbeddingRequest]
    ) -> List[EmbeddingResult]:
        """
        Process multiple embedding requests in batches.
        """
        results = []
        
        # Process in batches
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            
            try:
                batch_embeddings = await self._embed_with_retry(
                    [item.text for item in batch]
                )
                
                for item, embedding in zip(batch, batch_embeddings):
                    results.append(EmbeddingResult(
                        id=item.id,
                        embedding=embedding,
                        metadata=item.metadata
                    ))
            
            except Exception as e:
                # Handle batch failure
                print(f"Batch failed: {e}")
                # Could implement fallback strategy here
        
        return results
    
    async def _embed_with_retry(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """Embed with retry logic."""
        for attempt in range(self.max_retries):
            try:
                return await self.embed_batch(texts)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(self.retry_delay * (attempt + 1))
        
        return []
```

### 2. Optimized Batch Processing

```python
import numpy as np
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os

class OptimizedBatchProcessor:
    """
    Highly optimized batch embedding processor.
    """
    
    def __init__(
        self,
        embedding_function,
        batch_size: int = 100,
        num_workers: int = None,
        use_multiprocessing: bool = False
    ):
        self.embedding_function = embedding_function
        self.batch_size = batch_size
        self.num_workers = num_workers or os.cpu_count()
        self.use_multiprocessing = use_multiprocessing
        
        # Choose executor
        if use_multiprocessing:
            self.executor = ProcessPoolExecutor(max_workers=self.num_workers)
        else:
            self.executor = ThreadPoolExecutor(max_workers=self.num_workers)
    
    def create_batches(
        self,
        items: List[dict],
        batch_size: int = None
    ) -> List[List[dict]]:
        """
        Create batches from items, respecting max token limits.
        """
        batch_size = batch_size or self.batch_size
        batches = []
        current_batch = []
        current_tokens = 0
        max_tokens_per_batch = 8000  # Approximate for most APIs
        
        for item in items:
            item_tokens = item.get("token_count", len(item["text"]) // 4)
            
            if current_tokens + item_tokens > max_tokens_per_batch:
                if current_batch:
                    batches.append(current_batch)
                current_batch = [item]
                current_tokens = item_tokens
            else:
                current_batch.append(item)
                current_tokens += item_tokens
        
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    async def process_large_dataset(
        self,
        items: List[dict],
        progress_callback=None
    ) -> List[dict]:
        """
        Process large dataset with progress tracking.
        """
        batches = self.create_batches(items)
        all_results = []
        total_batches = len(batches)
        
        for i, batch in enumerate(batches):
            # Process batch
            embeddings = await self._process_single_batch(batch)
            all_results.extend(embeddings)
            
            # Progress callback
            if progress_callback:
                progress_callback(
                    processed=i + 1,
                    total=total_batches,
                    percentage=((i + 1) / total_batches) * 100
                )
        
        return all_results
    
    async def _process_single_batch(
        self,
        batch: List[dict]
    ) -> List[dict]:
        """Process a single batch."""
        texts = [item["text"] for item in batch]
        embeddings = await self.embedding_function(texts)
        
        results = []
        for item, embedding in zip(batch, embeddings):
            results.append({
                "id": item.get("id"),
                "text": item["text"],
                "embedding": embedding,
                "metadata": item.get("metadata", {})
            })
        
        return results
    
    def shutdown(self):
        """Cleanup executor."""
        self.executor.shutdown(wait=True)
```

### 3. Token-aware Batching

```python
class TokenAwareBatcher:
    """
    Batch items based on token count for optimal API utilization.
    """
    
    def __init__(
        self,
        max_tokens_per_batch: int = 100000,
        max_items_per_batch: int = 1000,
        model: str = "text-embedding-3-small"
    ):
        self.max_tokens_per_batch = max_tokens_per_batch
        self.max_items_per_batch = max_items_per_batch
        self.model = model
        
        # Token limits by model
        self.model_limits = {
            "text-embedding-3-large": {"max": 8000, "dim": 3072},
            "text-embedding-3-small": {"max": 8000, "dim": 1536},
            "text-embedding-ada-002": {"max": 8000, "dim": 1536},
        }
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        # Rough estimate: 4 chars per token
        return len(text) // 4
    
    def create_token_bounded_batches(
        self,
        items: List[dict]
    ) -> List[List[dict]]:
        """
        Create batches bounded by token count.
        """
        batches = []
        current_batch = []
        current_tokens = 0
        
        for item in items:
            item_tokens = item.get("token_count", self.estimate_tokens(item["text"]))
            
            # Check if adding this item exceeds limits
            exceeds_token_limit = current_tokens + item_tokens > self.max_tokens_per_batch
            exceeds_item_limit = len(current_batch) >= self.max_items_per_batch
            
            if exceeds_token_limit or exceeds_item_limit:
                if current_batch:
                    batches.append(current_batch)
                current_batch = [item]
                current_tokens = item_tokens
            else:
                current_batch.append(item)
                current_tokens += item_tokens
        
        # Don't forget the last batch
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    def optimize_batch_sizes(self, items: List[dict]) -> List[List[dict]]:
        """
        Optimize batch sizes for specific API.
        """
        model_limit = self.model_limits.get(
            self.model, 
            {"max": 8000}
        )["max"]
        
        # Adjust max tokens per batch to be safe
        effective_limit = int(model_limit * 0.9)  # 90% safety margin
        
        return self.create_token_bounded_batches(items)
```

## Async Embedding

### 1. Async Embedding Service

```python
import asyncio
import aiohttp
from typing import List, Optional
from dataclasses import dataclass
import json

@dataclass
class AsyncEmbeddingConfig:
    """Configuration for async embedding service."""
    api_key: str
    api_url: str = "https://api.openai.com/v1/embeddings"
    model: str = "text-embedding-3-small"
    max_concurrent_requests: int = 10
    timeout: int = 60

class AsyncEmbeddingService:
    """
    Async embedding service with rate limiting and retry logic.
    """
    
    def __init__(self, config: AsyncEmbeddingConfig):
        self.config = config
        self.semaphore = asyncio.Semaphore(config.max_concurrent_requests)
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json"
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def embed_single(self, text: str) -> List[float]:
        """Embed a single text."""
        async with self.semaphore:
            payload = {
                "input": text,
                "model": self.config.model
            }
            
            async with self.session.post(
                self.config.api_url,
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["data"][0]["embedding"]
                else:
                    raise Exception(f"API error: {response.status}")
    
    async def embed_batch(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """Embed multiple texts in a single API call."""
        async with self.semaphore:
            payload = {
                "input": texts,
                "model": self.config.model
            }
            
            async with self.session.post(
                self.config.api_url,
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    # Sort by index to maintain order
                    sorted_embeddings = sorted(
                        data["data"],
                        key=lambda x: x["index"]
                    )
                    return [item["embedding"] for item in sorted_embeddings]
                else:
                    error = await response.text()
                    raise Exception(f"API error: {response.status} - {error}")
    
    async def embed_with_retry(
        self,
        texts: List[str],
        max_retries: int = 3
    ) -> List[List[float]]:
        """Embed with automatic retry."""
        for attempt in range(max_retries):
            try:
                return await self.embed_batch(texts)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        return []


# Usage
async def main():
    config = AsyncEmbeddingConfig(
        api_key="your-api-key",
        max_concurrent_requests=10
    )
    
    async with AsyncEmbeddingService(config) as service:
        # Single embedding
        embedding = await service.embed_single("Hello, world!")
        
        # Batch embedding
        embeddings = await service.embed_batch([
            "Text 1",
            "Text 2",
            "Text 3"
        ])
        
        # Concurrent batch processing
        tasks = [
            service.embed_batch(batch_texts)
            for batch_texts in chunked_texts
        ]
        results = await asyncio.gather(*tasks)
```

### 2. Background Embedding Worker

```python
import asyncio
from queue import Queue, Empty
from threading import Thread
from typing import List, Callable
import time

class BackgroundEmbeddingWorker:
    """
    Background worker for continuous embedding processing.
    """
    
    def __init__(
        self,
        embedding_service,
        queue_size: int = 10000,
        batch_size: int = 100,
        flush_interval: float = 5.0
    ):
        self.service = embedding_service
        self.queue = Queue(maxsize=queue_size)
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.running = False
        self.worker_thread = None
        
        # Callbacks
        self.on_result: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
    
    def start(self):
        """Start the background worker."""
        self.running = True
        self.worker_thread = Thread(target=self._run_worker, daemon=True)
        self.worker_thread.start()
    
    def stop(self):
        """Stop the background worker."""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=10)
    
    def submit(self, item: dict) -> str:
        """
        Submit an item for embedding.
        Returns the item ID for tracking.
        """
        self.queue.put(item)
        return item.get("id", str(time.time()))
    
    def _run_worker(self):
        """Main worker loop."""
        buffer = []
        last_flush = time.time()
        
        while self.running:
            try:
                # Try to get item from queue with timeout
                try:
                    item = self.queue.get(timeout=0.1)
                    buffer.append(item)
                except Empty:
                    pass
                
                # Check if we should flush
                should_flush = (
                    len(buffer) >= self.batch_size or
                    (time.time() - last_flush) >= self.flush_interval
                )
                
                if buffer and should_flush:
                    asyncio.run(self._process_buffer(buffer))
                    buffer = []
                    last_flush = time.time()
            
            except Exception as e:
                if self.on_error:
                    self.on_error(e)
        
        # Process remaining items
        if buffer:
            asyncio.run(self._process_buffer(buffer))
    
    async def _process_buffer(self, buffer: List[dict]):
        """Process buffered items."""
        try:
            texts = [item["text"] for item in buffer]
            embeddings = await self.service.embed_batch(texts)
            
            for item, embedding in zip(buffer, embeddings):
                result = {
                    **item,
                    "embedding": embedding,
                    "processed_at": time.time()
                }
                
                if self.on_result:
                    self.on_result(result)
        
        except Exception as e:
            for item in buffer:
                if self.on_error:
                    self.on_error(item, e)


# Usage
def handle_result(result):
    print(f"Embedded: {result['id']}")

worker = BackgroundEmbeddingWorker(
    embedding_service=service,
    batch_size=100,
    flush_interval=5.0
)
worker.on_result = handle_result
worker.start()

# Submit items
worker.submit({"id": "doc_1", "text": "Some text to embed"})
worker.submit({"id": "doc_2", "text": "Another text"})
```

## Quality vs Speed Tradeoffs

### 1. Quality Optimization

```python
class QualityOptimizedEmbedder:
    """
    Embedder optimized for maximum quality.
    """
    
    def __init__(
        self,
        model: str = "text-embedding-3-large",
        normalize: bool = True
    ):
        self.model = model
        self.normalize = normalize
    
    async def embed_with_quality_checks(
        self,
        text: str
    ) -> dict:
        """
        Embed with quality validation.
        """
        # Pre-processing for quality
        cleaned_text = self._preprocess_text(text)
        
        # Embed
        embedding = await self._embed(cleaned_text)
        
        # Post-processing
        if self.normalize:
            embedding = self._normalize(embedding)
        
        # Quality check
        quality = self._assess_quality(embedding)
        
        return {
            "embedding": embedding,
            "quality_score": quality,
            "original_length": len(text),
            "cleaned_length": len(cleaned_text)
        }
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for better embeddings.
        """
        import re
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Normalize unicode
        text = text.encode('utf-8').decode('utf-8')
        
        # Preserve important punctuation
        # Don't strip out periods, question marks, etc.
        
        return text.strip()
    
    def _normalize(self, embedding: List[float]) -> List[float]:
        """L2 normalize embedding."""
        import numpy as np
        vec = np.array(embedding)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist() if norm > 0 else embedding
    
    def _assess_quality(self, embedding: List[float]) -> float:
        """
        Assess embedding quality.
        Returns a score between 0 and 1.
        """
        import numpy as np
        
        vec = np.array(embedding)
        
        # Check for NaN or Inf
        if not np.isfinite(vec).all():
            return 0.0
        
        # Check variance (too uniform = low quality)
        variance = np.var(vec)
        if variance < 0.01:
            return 0.5
        
        # Check magnitude (should be around 1 for normalized)
        magnitude = np.linalg.norm(vec)
        magnitude_score = 1.0 - abs(1.0 - magnitude)
        
        return min(magnitude_score, 1.0)
```

### 2. Speed Optimization

```python
class SpeedOptimizedEmbedder:
    """
    Embedder optimized for speed.
    """
    
    def __init__(
        self,
        model: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: str = "cuda"  # or "cpu"
    ):
        from sentence_transformers import SentenceTransformer
        
        self.model_name = model
        self.model = SentenceTransformer(model, device=device)
        self.encode_kwargs = {
            "batch_size": 256,
            "show_progress_bar": False,
            "normalize_embeddings": True
        }
    
    def embed_batch_fast(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Fast batch embedding using local model.
        """
        embeddings = self.model.encode(
            texts,
            **self.encode_kwargs
        )
        
        return embeddings.tolist()
    
    def embed_single_fast(
        self,
        text: str
    ) -> List[float]:
        """Fast single embedding."""
        return self.embed_batch_fast([text])[0]


# Local GPU embedding for speed
embedder = SpeedOptimizedEmbedder(
    model="sentence-transformers/all-mpnet-base-v2",
    device="cuda"  # Use GPU
)
```

### 3. Adaptive Embedding Strategy

```python
class AdaptiveEmbeddingStrategy:
    """
    Adapt strategy based on content and requirements.
    """
    
    def __init__(
        self,
        fast_embedder,
        quality_embedder
    ):
        self.fast = fast_embedder
        self.quality = quality_embedder
        
        # Thresholds
        self.length_threshold = 500
        self.importance_threshold = 0.7
    
    def embed(
        self,
        text: str,
        importance: float = 1.0,
        prefer_speed: bool = False
    ) -> List[float]:
        """
        Choose embedding strategy adaptively.
        """
        # Very important content -> use quality model
        if importance >= self.importance_threshold:
            return self.quality.embed_with_quality_checks(text)
        
        # Short, fast content -> use fast model
        if len(text) < self.length_threshold or prefer_speed:
            return self.fast.embed_single_fast(text)
        
        # Long content -> use batch processing with fast model
        return self.fast.embed_single_fast(text)
    
    async def embed_batch_adaptive(
        self,
        items: List[dict]
    ) -> List[dict]:
        """
        Adaptive batch processing.
        """
        # Separate into fast and quality items
        fast_items = []
        quality_items = []
        
        for item in items:
            importance = item.get("importance", 1.0)
            
            if importance >= self.importance_threshold:
                quality_items.append(item)
            else:
                fast_items.append(item)
        
        results = []
        
        # Process fast items in batch
        if fast_items:
            texts = [item["text"] for item in fast_items]
            embeddings = self.fast.embed_batch_fast(texts)
            
            for item, embedding in zip(fast_items, embeddings):
                results.append({**item, "embedding": embedding})
        
        # Process quality items
        for item in quality_items:
            embedding = self.quality.embed_with_quality_checks(item["text"])
            results.append({**item, "embedding": embedding})
        
        return results
```

## Best Practices

### 1. Error Handling

```python
class ResilientEmbeddingPipeline:
    """
    Embedding pipeline with comprehensive error handling.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.failed_items = []
        self.stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "retried": 0
        }
    
    async def embed_with_error_handling(
        self,
        items: List[dict]
    ) -> List[dict]:
        """
        Embed items with comprehensive error handling.
        """
        self.stats["total"] = len(items)
        results = []
        
        for item in items:
            try:
                result = await self._embed_single(item)
                results.append(result)
                self.stats["success"] += 1
            
            except RateLimitError:
                # Wait and retry
                await asyncio.sleep(60)  # Wait 1 minute
                try:
                    result = await self._embed_single(item)
                    results.append(result)
                    self.stats["success"] += 1
                    self.stats["retried"] += 1
                except Exception as e:
                    self._handle_failure(item, e)
            
            except ValidationError as e:
                # Invalid input - don't retry
                self._handle_failure(item, e)
            
            except Exception as e:
                # Unknown error - retry once
                await asyncio.sleep(5)
                try:
                    result = await self._embed_single(item)
                    results.append(result)
                    self.stats["success"] += 1
                    self.stats["retried"] += 1
                except Exception as e2:
                    self._handle_failure(item, e2)
        
        return results
    
    def _handle_failure(self, item: dict, error: Exception):
        """Handle failed embedding."""
        self.stats["failed"] += 1
        self.failed_items.append({
            "item": item,
            "error": str(error),
            "timestamp": time.time()
        })
    
    def get_failed_items(self) -> List[dict]:
        """Get items that failed to embed."""
        return self.failed_items
    
    def retry_failed_items(self) -> List[dict]:
        """Retry items that previously failed."""
        items = [f["item"] for f in self.failed_items]
        self.failed_items = []
        return asyncio.run(self.embed_with_error_handling(items))
```

### 2. Caching Strategy

```python
import hashlib
from typing import Optional

class EmbeddingCache:
    """
    Cache embeddings to avoid redundant API calls.
    """
    
    def __init__(
        self,
        storage,
        ttl_seconds: int = 86400 * 30  # 30 days
    ):
        self.storage = storage  # Redis, disk, etc.
        self.ttl = ttl_seconds
    
    def _get_cache_key(self, text: str, model: str) -> str:
        """Generate cache key."""
        content = f"{model}:{text}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    async def get(
        self,
        text: str,
        model: str
    ) -> Optional[List[float]]:
        """Get cached embedding."""
        key = self._get_cache_key(text, model)
        
        cached = await self.storage.get(key)
        if cached:
            return json.loads(cached)
        
        return None
    
    async def set(
        self,
        text: str,
        model: str,
        embedding: List[float]
    ):
        """Cache embedding."""
        key = self._get_cache_key(text, model)
        await self.storage.setex(
            key,
            self.ttl,
            json.dumps(embedding)
        )


class CachedEmbeddingPipeline:
    """
    Embedding pipeline with caching.
    """
    
    def __init__(self, cache: EmbeddingCache, service):
        self.cache = cache
        self.service = service
    
    async def embed(self, text: str, model: str) -> List[float]:
        """Embed with cache lookup."""
        # Check cache first
        cached = await self.cache.get(text, model)
        if cached:
            return cached
        
        # Generate embedding
        embedding = await self.service.embed_single(text, model)
        
        # Cache result
        await self.cache.set(text, model, embedding)
        
        return embedding
```

### 3. Monitoring và Metrics

```python
import time
from dataclasses import dataclass, field

@dataclass
class EmbeddingMetrics:
    """Metrics for embedding operations."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_tokens: int = 0
    total_latency_ms: float = 0
    batch_sizes: list = field(default_factory=list)
    
    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0
        return self.successful_requests / self.total_requests
    
    @property
    def avg_latency_ms(self) -> float:
        if self.total_requests == 0:
            return 0
        return self.total_latency_ms / self.total_requests


class MonitoredEmbeddingPipeline:
    """
    Embedding pipeline with metrics collection.
    """
    
    def __init__(self, service):
        self.service = service
        self.metrics = EmbeddingMetrics()
    
    async def embed(self, text: str) -> List[float]:
        """Embed with metrics."""
        start = time.time()
        self.metrics.total_requests += 1
        
        try:
            result = await self.service.embed_single(text)
            self.metrics.successful_requests += 1
            return result
        
        except Exception:
            self.metrics.failed_requests += 1
            raise
        
        finally:
            latency = (time.time() - start) * 1000
            self.metrics.total_latency_ms += latency
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed batch with metrics."""
        start = time.time()
        self.metrics.total_requests += 1
        self.metrics.batch_sizes.append(len(texts))
        
        try:
            results = await self.service.embed_batch(texts)
            self.metrics.successful_requests += len(texts)
            self.metrics.total_tokens += sum(len(t) // 4 for t in texts)
            return results
        
        except Exception:
            self.metrics.failed_requests += len(texts)
            raise
        
        finally:
            latency = (time.time() - start) * 1000
            self.metrics.total_latency_ms += latency
    
    def get_metrics(self) -> dict:
        """Get current metrics."""
        return {
            "total_requests": self.metrics.total_requests,
            "successful_requests": self.metrics.successful_requests,
            "failed_requests": self.metrics.failed_requests,
            "success_rate": self.metrics.success_rate,
            "avg_latency_ms": self.metrics.avg_latency_ms,
            "total_tokens": self.metrics.total_tokens,
            "avg_batch_size": sum(self.metrics.batch_sizes) / len(self.metrics.batch_sizes) if self.metrics.batch_sizes else 0
        }
```

## Examples

### Example 1: Complete Production Embedding Pipeline

```python
import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class EmbeddingPipelineConfig:
    """Configuration for embedding pipeline."""
    # API settings
    api_key: str
    api_url: str = "https://api.openai.com/v1/embeddings"
    model: str = "text-embedding-3-small"
    
    # Batch settings
    batch_size: int = 100
    max_concurrent_batches: int = 5
    
    # Retry settings
    max_retries: int = 3
    retry_base_delay: float = 1.0
    
    # Cache settings
    use_cache: bool = True
    cache_ttl_days: int = 30
    
    # Monitoring
    enable_metrics: bool = True

class ProductionEmbeddingPipeline:
    """
    Complete production-ready embedding pipeline.
    """
    
    def __init__(self, config: EmbeddingPipelineConfig):
        self.config = config
        
        # Initialize components
        self.cache = EmbeddingCache() if config.use_cache else None
        self.service = AsyncEmbeddingService(config)
        self.metrics = MonitoredEmbeddingPipeline(self.service)
        
        # Queue for background processing
        self.queue: asyncio.Queue = None
        self.worker_task: Optional[asyncio.Task] = None
    
    async def __aenter__(self):
        """Start the pipeline."""
        self.queue = asyncio.Queue()
        self.worker_task = asyncio.create_task(self._background_worker())
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Stop the pipeline."""
        if self.worker_task:
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                pass
    
    async def embed_single(
        self,
        text: str,
        use_cache: bool = True
    ) -> List[float]:
        """Embed a single text."""
        # Check cache
        if self.cache and use_cache:
            cached = await self.cache.get(text, self.config.model)
            if cached:
                return cached
        
        # Embed
        embedding = await self.metrics.embed(text)
        
        # Cache result
        if self.cache and use_cache:
            await self.cache.set(text, self.config.model, embedding)
        
        return embedding
    
    async def embed_batch(
        self,
        texts: List[str],
        show_progress: bool = False
    ) -> List[List[float]]:
        """Embed a batch of texts."""
        results = []
        
        # Process in smaller batches to respect rate limits
        for i in range(0, len(texts), self.config.batch_size):
            batch = texts[i:i + self.config.batch_size]
            
            # Check cache for each item
            uncached = []
            cached_results = []
            
            if self.cache:
                for text in batch:
                    cached = await self.cache.get(text, self.config.model)
                    if cached:
                        cached_results.append(cached)
                    else:
                        uncached.append(text)
            else:
                uncached = batch
            
            # Embed uncached items
            if uncached:
                embeddings = await self.metrics.embed_batch(uncached)
                
                # Cache results
                if self.cache:
                    for text, embedding in zip(uncached, embeddings):
                        await self.cache.set(text, self.config.model, embedding)
                
                results.extend(embeddings)
            
            results.extend(cached_results)
            
            if show_progress:
                logger.info(f"Processed {min(i + self.config.batch_size, len(texts))}/{len(texts)}")
        
        return results
    
    async def _background_worker(self):
        """Background worker for continuous processing."""
        while True:
            try:
                # Get items from queue
                items = []
                while len(items) < self.config.batch_size:
                    try:
                        item = await asyncio.wait_for(
                            self.queue.get(),
                            timeout=1.0
                        )
                        items.append(item)
                    except asyncio.TimeoutError:
                        break
                
                if items:
                    texts = [item["text"] for item in items]
                    embeddings = await self.embed_batch(texts)
                    
                    # Call callbacks
                    for item, embedding in zip(items, embeddings):
                        if "callback" in item:
                            item["callback"]({
                                **item,
                                "embedding": embedding
                            })
            
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Background worker error: {e}")
    
    def get_metrics(self) -> dict:
        """Get pipeline metrics."""
        return self.metrics.get_metrics()


# Usage
async def main():
    config = EmbeddingPipelineConfig(
        api_key="your-api-key",
        batch_size=100,
        max_concurrent_batches=5,
        use_cache=True
    )
    
    async with ProductionEmbeddingPipeline(config) as pipeline:
        # Single embedding
        embedding = await pipeline.embed_single("Hello, world!")
        
        # Batch embedding
        embeddings = await pipeline.embed_batch([
            "Text 1",
            "Text 2",
            "Text 3"
        ])
        
        # Get metrics
        metrics = pipeline.get_metrics()
        print(f"Success rate: {metrics['success_rate']}")
        print(f"Avg latency: {metrics['avg_latency_ms']}ms")
```

### Example 2: Incremental Embedding for Updates

```python
class IncrementalEmbeddingHandler:
    """
    Handle incremental updates to embedding index.
    """
    
    def __init__(self, pipeline, storage):
        self.pipeline = pipeline
        self.storage = storage  # Database or vector store
    
    async def process_updates(
        self,
        updates: List[dict]
    ) -> dict:
        """
        Process incremental updates.
        
        updates: List of {
            "action": "upsert" | "delete",
            "id": str,
            "text": str (for upsert)
        }
        """
        results = {
            "upserted": 0,
            "deleted": 0,
            "failed": 0,
            "errors": []
        }
        
        # Separate upserts and deletes
        upserts = [u for u in updates if u["action"] == "upsert"]
        deletes = [u for u in updates if u["action"] == "delete"]
        
        # Process deletes
        for delete in deletes:
            try:
                await self.storage.delete(delete["id"])
                results["deleted"] += 1
            except Exception as e:
                results["failed"] += 1
                results["errors"].append({
                    "id": delete["id"],
                    "error": str(e)
                })
        
        # Process upserts
        if upserts:
            texts = [u["text"] for u in upserts]
            
            try:
                embeddings = await self.pipeline.embed_batch(texts)
                
                for update, embedding in zip(upserts, embeddings):
                    try:
                        await self.storage.upsert({
                            "id": update["id"],
                            "text": update["text"],
                            "embedding": embedding,
                            "updated_at": time.time()
                        })
                        results["upserted"] += 1
                    except Exception as e:
                        results["failed"] += 1
                        results["errors"].append({
                            "id": update["id"],
                            "error": str(e)
                        })
            
            except Exception as e:
                results["failed"] += len(upserts)
                results["errors"].append({
                    "error": f"Batch embedding failed: {str(e)}"
                })
        
        return results
    
    async def sync_checkpointer(
        self,
        checkpoint_interval: int = 100
    ) -> dict:
        """
        Checkpoint for resumable processing.
        """
        last_processed = await self.storage.get_checkpoint()
        
        # Get items since checkpoint
        pending = await self.storage.get_pending_items(
            after=last_processed,
            limit=checkpoint_interval
        )
        
        if not pending:
            return {"status": "up_to_date"}
        
        # Process batch
        results = await self.process_updates(pending)
        
        # Update checkpoint
        if results["failed"] == 0:
            await self.storage.set_checkpoint(pending[-1]["id"])
        
        return {
            "status": "processed",
            "processed": len(pending),
            "results": results
        }
```

### Example 3: Multi-modal Embedding

```python
class MultiModalEmbeddingPipeline:
    """
    Pipeline for embedding multiple modalities.
    """
    
    def __init__(self, text_pipeline, image_pipeline):
        self.text = text_pipeline
        self.image = image_pipeline
    
    async def embed_text(self, text: str) -> List[float]:
        """Embed text."""
        return await self.text.embed_single(text)
    
    async def embed_image(self, image_path: str) -> List[float]:
        """Embed image."""
        return await self.image.embed_single(image_path)
    
    async def embed_document(
        self,
        text: str,
        images: List[str] = None
    ) -> dict:
        """
        Embed document with both text and images.
        """
        result = {
            "text_embedding": None,
            "image_embeddings": [],
            "combined_embedding": None
        }
        
        # Embed text
        result["text_embedding"] = await self.embed_text(text)
        
        # Embed images if present
        if images:
            result["image_embeddings"] = await self.image.embed_batch(images)
            
            # Combine embeddings (average pooling)
            all_embeddings = [result["text_embedding"]] + result["image_embeddings"]
            result["combined_embedding"] = self._average_pool(all_embeddings)
        else:
            result["combined_embedding"] = result["text_embedding"]
        
        return result
    
    def _average_pool(self, embeddings: List[List[float]]) -> List[float]:
        """Average pool multiple embeddings."""
        import numpy as np
        
        if not embeddings:
            return []
        
        arr = np.array(embeddings)
        return np.mean(arr, axis=0).tolist()
```

## References

1. **OpenAI Embeddings**: https://platform.openai.com/docs/guides/embeddings
2. **Cohere Embeddings**: https://docs.cohere.com/docsembeddings
3. **Sentence Transformers**: https://www.sbert.net/
4. **Batch Processing Best Practices**: https://docs.python.org/3/library/asyncio.html
5. **Cursor Enterprise Framework - RAG Rules**: `.cursor/rules/rag.mdc`
