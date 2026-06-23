---
title: "Serving Architecture"
description: "Hướng dẫn về vector database deployment: index serving, cold start, caching strategies và horizontal scaling"
tags: ["serving", "deployment", "architecture", "scaling", "caching", "horizontal-scaling"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Serving Architecture

## Tổng Quan

Serving architecture cho vector search systems phải balance giữa latency, throughput, và resource utilization. Khác với traditional databases, vector indexes có những đặc điểm riêng về memory access patterns và computational requirements đòi hỏi specialized architectures.

Key considerations bao gồm:
- Index loading và warm-up strategies
- Caching để reduce latency
- Horizontal scaling để handle increased load
- Resource management và capacity planning

Việc design đúng architecture sẽ quyết định performance và cost-effectiveness của hệ thống.

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức toàn diện về vector serving architecture:

Đầu tiên, chúng ta sẽ tìm hiểu về index serving và memory management.

Thứ hai, tài liệu hướng dẫn các chiến lược để handle cold start.

Thứ ba, chúng ta sẽ đề cập đến caching strategies.

Cuối cùng, tài liệu cung cấp patterns cho horizontal scaling.

## Key Concepts

### 1. Architecture Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│                    SERVING ARCHITECTURE PATTERNS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Pattern 1: Single Node                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  API Server + Vector Index (In-Memory)                    │   │
│  │  - Simple setup                                          │   │
│  │  - Limited by single machine resources                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Pattern 2: Separate Compute/Storage                              │
│  ┌──────────────┐     ┌──────────────┐                        │
│  │  API Servers │────►│  Index Store │                         │
│  │  (Stateless) │     │  (S3 + RAM) │                         │
│  └──────────────┘     └──────────────┘                        │
│                                                                  │
│  Pattern 3: Distributed Search                                    │
│  ┌──────────────┐     ┌──────────────┐                        │
│  │   Router    │────►│  Shard 1    │                        │
│  │  (Fan-out)  │────►│  Shard 2    │                        │
│  │             │────►│  Shard N    │                         │
│  └──────────────┘     └──────────────┘                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Latency Budget

```python
"""
Target latency breakdown for vector search requests.

Goal: < 50ms P99 for most applications

Breakdown:
- Network: 5ms (request/response)
- Query parsing: 1ms
- Vector search: 30ms (HNSW with ef=100)
- Post-processing: 5ms
- Serialization: 5ms
- Buffer: 4ms

Total: ~50ms
"""

LATENCY_BUDGET = {
    "network_overhead": 5,  # Network RTT
    "request_parsing": 1,   # JSON parse
    "vector_search": 30,    # Core search
    "post_processing": 5,    # Ranking, filtering
    "serialization": 5,      # Response encoding
    "buffer": 4,            # GC, scheduling
    
    "target_p99_ms": 50
}
```

## Index Serving

### 1. In-Memory Index

```python
class InMemoryVectorIndex:
    """
    In-memory vector index server.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.index = None
        self.vectors = {}
        self.metadata = {}
    
    def load(self, path: str):
        """Load index from disk."""
        import numpy as np
        import pickle
        
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        self.vectors = data['vectors']
        self.metadata = data.get('metadata', {})
        
        # Rebuild index structure
        self._build_index()
    
    def _build_index(self):
        """Build search index from vectors."""
        # Choose index type based on config
        if self.config.get("index_type") == "hnsw":
            self.index = HNSWIndex(
                m=self.config.get("m", 16),
                ef_construction=self.config.get("ef_construction", 200)
            )
            self.index.build(self.vectors)
        elif self.config.get("index_type") == "ivf":
            self.index = IVFIndex(
                nlist=self.config.get("nlist", 100)
            )
            self.index.build(self.vectors)
    
    def search(
        self,
        query_vector: np.ndarray,
        k: int = 10
    ) -> List[Tuple[str, float]]:
        """Search for nearest neighbors."""
        return self.index.search(query_vector, k)
    
    def add(
        self,
        id: str,
        vector: np.ndarray,
        metadata: dict = None
    ):
        """Add vector to index."""
        self.vectors[id] = vector
        if metadata:
            self.metadata[id] = metadata
        
        # Update index
        self.index.add(id, vector)
    
    def save(self, path: str):
        """Save index to disk."""
        import pickle
        
        data = {
            'vectors': self.vectors,
            'metadata': self.metadata,
            'config': self.config
        }
        
        with open(path, 'wb') as f:
            pickle.dump(data, f)
```

### 2. Memory-Mapped Index

```python
class MemoryMappedIndex:
    """
    Memory-mapped vector index for large datasets.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.mmap_file = None
        self.vectors = None
        self.vectors_shape = None
    
    def load(self, path: str):
        """Load vectors using memory mapping."""
        import numpy as np
        import mmap
        import os
        
        # Open file for memory mapping
        self.mmap_file = open(path, 'rb+')
        file_size = os.path.getsize(path)
        
        # Memory map the file
        self.mmapped = mmap.mmap(
            self.mmap_file.fileno(),
            length=file_size,
            access=mmap.ACCESS_READ
        )
    
    def get_vector(self, idx: int) -> np.ndarray:
        """Get single vector from memory-mapped file."""
        import numpy as np
        
        offset = idx * self.vectors_shape[1] * 4  # float32 = 4 bytes
        
        # Read vector directly from memory
        vector = np.frombuffer(
            self.mmapped,
            dtype=np.float32,
            count=self.vectors_shape[1],
            offset=offset
        ).copy()
        
        return vector
    
    def search(
        self,
        query: np.ndarray,
        k: int = 10
    ) -> List[Tuple[int, float]]:
        """Search using memory-mapped vectors."""
        import numpy as np
        
        # Read vectors in batches to avoid memory pressure
        batch_size = 10000
        results = []
        
        for start in range(0, self.vectors_shape[0], batch_size):
            end = min(start + batch_size, self.vectors_shape[0])
            
            # Read batch
            batch_vectors = np.frombuffer(
                self.mmapped,
                dtype=np.float32,
                count=(end - start) * self.vectors_shape[1],
                offset=start * self.vectors_shape[1] * 4
            ).reshape(-1, self.vectors_shape[1])
            
            # Compute distances
            distances = np.linalg.norm(batch_vectors - query, axis=1)
            
            # Track top-k
            for i, dist in enumerate(distances):
                results.append((start + i, dist))
        
        # Sort and return top-k
        results.sort(key=lambda x: x[1])
        return results[:k]
```

### 3. Streaming Index Updates

```python
class StreamingIndex:
    """
    Vector index with streaming updates.
    """
    
    def __init__(self, base_index, write_ahead_log: str):
        self.base_index = base_index
        self.wal = write_ahead_log
        self.pending_updates = []
        self.flush_interval = 100  # Flush every N updates
    
    def add(self, id: str, vector: np.ndarray):
        """Add vector (immediate write)."""
        import json
        
        # Write to WAL first
        with open(self.wal, 'a') as f:
            f.write(json.dumps({
                'op': 'add',
                'id': id,
                'vector': vector.tolist()
            }) + '\n')
        
        # Apply to base index
        self.base_index.add(id, vector)
        
        # Track for batch flush
        self.pending_updates.append(('add', id, vector))
        
        if len(self.pending_updates) >= self.flush_interval:
            self._flush()
    
    def _flush(self):
        """Flush pending updates to persistent storage."""
        # Implementation depends on storage backend
        self.pending_updates = []
    
    def recovery(self):
        """Recover from WAL after crash."""
        import json
        
        if not os.path.exists(self.wal):
            return
        
        with open(self.wal, 'r') as f:
            for line in f:
                op = json.loads(line)
                
                if op['op'] == 'add':
                    self.base_index.add(
                        op['id'],
                        np.array(op['vector'])
                    )
        
        # Clear WAL after recovery
        os.remove(self.wal)
```

## Cold Start Handling

### 1. Lazy Loading

```python
class LazyLoadingIndex:
    """
    Index that loads data on-demand.
    """
    
    def __init__(self, storage_client):
        self.storage = storage_client
        self.loaded_segments = {}
        self.segment_size = 1000000  # 1M vectors per segment
    
    def _get_segment_path(self, vector_id: int) -> str:
        """Get storage path for segment."""
        segment_id = vector_id // self.segment_size
        return f"index/segment_{segment_id}.bin"
    
    def get_vector(self, id: int) -> np.ndarray:
        """Get vector, loading segment if needed."""
        segment_path = self._get_segment_path(id)
        
        if segment_path not in self.loaded_segments:
            # Lazy load segment
            print(f"Loading segment: {segment_path}")
            self.loaded_segments[segment_path] = self._load_segment(segment_path)
        
        # Get from loaded segment
        offset = id % self.segment_size
        return self.loaded_segments[segment_path][offset]
    
    def _load_segment(self, path: str) -> np.ndarray:
        """Load segment from storage."""
        import numpy as np
        
        # Download from S3 or load from disk
        data = self.storage.download(path)
        
        return np.frombuffer(data, dtype=np.float32).reshape(-1, self.dimensions)
```

### 2. Warm-up Strategy

```python
class WarmUpStrategy:
    """
    Strategies to warm up vector index after cold start.
    """
    
    def __init__(self, index):
        self.index = index
    
    def warm_up(self, strategy: str = "priority"):
        """
        Warm up index using specified strategy.
        """
        if strategy == "priority":
            return self._warm_up_priority()
        elif strategy == "sampling":
            return self._warm_up_sampling()
        elif strategy == "recent":
            return self._warm_up_recent()
    
    def _warm_up_priority(self):
        """Load high-priority segments first."""
        # Define priority based on access patterns
        priority_segments = [
            "active_users",
            "recent_products",
            "featured_content"
        ]
        
        for segment in priority_segments:
            print(f"Warming: {segment}")
            self.index.load_segment(segment)
    
    def _warm_up_sampling(self):
        """Load representative sample of all segments."""
        import random
        
        # Load 10% of each segment
        for segment in self.index.segments:
            sample_ids = random.sample(
                range(len(segment)),
                len(segment) // 10
            )
            
            for idx in sample_ids:
                _ = segment[idx]  # Trigger load
    
    def _warm_up_recent(self):
        """Load recent data first."""
        import datetime
        
        # Load segments with recent timestamps
        recent_cutoff = datetime.datetime.now() - datetime.timedelta(days=7)
        
        for segment in self.index.segments:
            if segment.last_updated > recent_cutoff:
                print(f"Warming recent: {segment.id}")
                self.index.load_segment(segment.id)
```

### 3. Background Loading

```python
class BackgroundLoader:
    """
    Background thread for loading segments.
    """
    
    def __init__(self, index, max_concurrent=3):
        self.index = index
        self.max_concurrent = max_concurrent
        self.loading_queue = queue.PriorityQueue()
        self.loading_thread = None
        self.active_loads = {}
    
    def start(self):
        """Start background loading thread."""
        self.loading_thread = threading.Thread(
            target=self._loading_loop,
            daemon=True
        )
        self.loading_thread.start()
    
    def request_load(self, segment_id: str, priority: int = 5):
        """Request segment loading."""
        self.loading_queue.put((priority, segment_id))
    
    def _loading_loop(self):
        """Background loading loop."""
        import queue
        
        while True:
            try:
                # Get next segment to load
                priority, segment_id = self.loading_queue.get(timeout=1)
                
                if segment_id in self.active_loads:
                    continue
                
                # Check concurrent limit
                while len(self.active_loads) >= self.max_concurrent:
                    time.sleep(0.1)
                
                # Start loading
                self.active_loads[segment_id] = True
                threading.Thread(
                    target=self._load_segment,
                    args=(segment_id,),
                    daemon=True
                ).start()
            
            except queue.Empty:
                time.sleep(0.1)
    
    def _load_segment(self, segment_id: str):
        """Load segment in background."""
        print(f"Loading: {segment_id}")
        
        try:
            self.index.load_segment(segment_id)
        finally:
            del self.active_loads[segment_id]
```

## Caching Strategies

### 1. Multi-level Cache

```python
class MultiLevelCache:
    """
    L1 (hot) + L2 (warm) + L3 (cold) cache hierarchy.
    """
    
    def __init__(self, config: dict):
        # L1: In-memory cache (hot queries)
        self.l1_cache = LRUCache(
            max_size=config.get("l1_size", 10000)
        )
        
        # L2: Redis cache (warm data)
        self.l2_cache = RedisCache(
            host=config.get("redis_host", "localhost"),
            port=config.get("redis_port", 6379),
            ttl=config.get("l2_ttl", 3600)
        )
        
        # L3: Query result cache
        self.result_cache = ResultCache(
            max_size=config.get("result_cache_size", 50000)
        )
    
    def get(self, key: str) -> Optional[any]:
        """Get value from cache hierarchy."""
        # Check L1 first
        value = self.l1_cache.get(key)
        if value is not None:
            return value
        
        # Check L2
        value = self.l2_cache.get(key)
        if value is not None:
            # Promote to L1
            self.l1_cache.set(key, value)
            return value
        
        return None
    
    def set(self, key: str, value: any):
        """Set value in cache hierarchy."""
        self.l1_cache.set(key, value)
        self.l2_cache.set(key, value)
    
    def get_search_result(
        self,
        query_hash: str,
        filters: str = None
    ) -> Optional[List[dict]]:
        """Get cached search result."""
        cache_key = f"search:{query_hash}:{filters}"
        
        return self.get(cache_key)
    
    def set_search_result(
        self,
        query_hash: str,
        filters: str,
        results: List[dict]
    ):
        """Cache search result."""
        cache_key = f"search:{query_hash}:{filters}"
        
        self.result_cache.set(cache_key, results)


class LRUCache:
    """Simple LRU cache implementation."""
    
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.cache = OrderedDict()
    
    def get(self, key: str) -> Optional[any]:
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def set(self, key: str, value: any):
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.max_size:
                # Remove least recently used
                self.cache.popitem(last=False)
        
        self.cache[key] = value
```

### 2. Query Result Caching

```python
class QueryResultCache:
    """
    Cache for vector search results.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.cache = {}
        self.query_history = []
        self.max_size = config.get("max_size", 50000)
        self.hit_count = 0
        self.miss_count = 0
    
    def get_cache_key(
        self,
        query_vector: np.ndarray,
        filters: dict = None,
        k: int = 10
    ) -> str:
        """Generate cache key from query parameters."""
        import hashlib
        
        # Quantize query for cache key
        # This allows similar queries to hit the same cache
        quantized = (query_vector * 100).astype(np.int8).tobytes()
        
        key_hash = hashlib.sha256(quantized).hexdigest()[:16]
        
        filter_hash = hashlib.md5(
            str(sorted(filters.items())).encode()
        ).hexdigest()[:8] if filters else "nofilter"
        
        return f"{key_hash}:{filter_hash}:{k}"
    
    def get(self, cache_key: str) -> Optional[List[dict]]:
        """Get cached results."""
        if cache_key in self.cache:
            self.hit_count += 1
            return self.cache[cache_key]
        
        self.miss_count += 1
        return None
    
    def set(self, cache_key: str, results: List[dict]):
        """Cache search results."""
        if len(self.cache) >= self.max_size:
            # Evict oldest entry
            oldest_key = self.query_history.pop(0)
            del self.cache[oldest_key]
        
        self.cache[cache_key] = results
        self.query_history.append(cache_key)
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        total = self.hit_count + self.miss_count
        hit_rate = self.hit_count / total if total > 0 else 0
        
        return {
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": hit_rate,
            "cache_size": len(self.cache),
            "max_size": self.max_size
        }
```

### 3. Embedding Cache

```python
class EmbeddingCache:
    """
    Cache for embedding computations.
    """
    
    def __init__(self, storage, ttl: int = 86400 * 30):
        self.storage = storage  # Redis, S3, etc.
        self.ttl = ttl
        self.local_cache = {}  # L1 in-process cache
        self.local_cache_size = 10000
    
    def get_embedding(self, text: str) -> Optional[np.ndarray]:
        """Get cached embedding."""
        import hashlib
        
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        
        # Check local cache
        if text_hash in self.local_cache:
            return self.local_cache[text_hash]
        
        # Check persistent storage
        embedding = self.storage.get(f"embedding:{text_hash}")
        
        if embedding is not None:
            vector = np.frombuffer(embedding, dtype=np.float32)
            
            # Promote to local cache
            self._add_local_cache(text_hash, vector)
            
            return vector
        
        return None
    
    def set_embedding(self, text: str, embedding: np.ndarray):
        """Cache embedding."""
        import hashlib
        
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        
        # Store in both caches
        self._add_local_cache(text_hash, embedding)
        
        self.storage.set(
            f"embedding:{text_hash}",
            embedding.tobytes(),
            ttl=self.ttl
        )
    
    def _add_local_cache(self, key: str, value: np.ndarray):
        """Add to local LRU cache."""
        if len(self.local_cache) >= self.local_cache_size:
            # Simple eviction: remove first item
            first_key = next(iter(self.local_cache))
            del self.local_cache[first_key]
        
        self.local_cache[key] = value
```

## Horizontal Scaling

### 1. Sharding Strategies

```python
class ShardedVectorIndex:
    """
    Horizontally scaled vector index.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.shards = {}
        self.shard_strategy = config.get("shard_strategy", "hash")
    
    def create_shards(self, num_shards: int):
        """Create shard instances."""
        for i in range(num_shards):
            self.shards[i] = VectorIndex(
                config=self.config
            )
    
    def _get_shard(self, vector_id: str) -> int:
        """Determine which shard owns a vector."""
        if self.shard_strategy == "hash":
            return hash(vector_id) % len(self.shards)
        elif self.shard_strategy == "range":
            # Range-based sharding
            return self._range_shard(vector_id)
        elif self.shard_strategy == "categorical":
            # Shard by category
            return self._categorical_shard(vector_id)
    
    def add(self, vector_id: str, vector: np.ndarray):
        """Add vector to appropriate shard."""
        shard_id = self._get_shard(vector_id)
        self.shards[shard_id].add(vector_id, vector)
    
    def search(
        self,
        query: np.ndarray,
        k: int = 10
    ) -> List[Tuple[str, float]]:
        """Search across all shards."""
        import concurrent.futures
        
        # Search all shards in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(shard.search, query, k * 2): shard_id
                for shard_id, shard in self.shards.items()
            }
            
            # Collect results
            all_results = []
            for future in concurrent.futures.as_completed(futures):
                shard_results = future.result()
                all_results.extend(shard_results)
        
        # Merge and dedupe
        seen = set()
        merged = []
        
        for result in sorted(all_results, key=lambda x: x[1]):
            if result[0] not in seen:
                seen.add(result[0])
                merged.append(result)
                if len(merged) >= k:
                    break
        
        return merged


class ConsistentHashSharding:
    """
    Consistent hashing for vector sharding.
    """
    
    def __init__(self, num_virtual_nodes: int = 100):
        self.num_virtual_nodes = num_virtual_nodes
        self.ring = {}  # hash -> node
        self.sorted_keys = []
    
    def add_node(self, node_id: str):
        """Add node to hash ring."""
        import hashlib
        
        for i in range(self.num_virtual_nodes):
            key = hashlib.sha256(
                f"{node_id}:{i}".encode()
            ).digest()
            
            self.ring[key] = node_id
        
        self.sorted_keys = sorted(self.ring.keys())
    
    def get_node(self, key: str) -> str:
        """Get responsible node for a key."""
        import hashlib
        
        key_hash = hashlib.sha256(key.encode()).digest()
        
        # Binary search for first node >= key_hash
        for ring_key in self.sorted_keys:
            if ring_key >= key_hash:
                return self.ring[ring_key]
        
        # Wrap around to first node
        return self.ring[self.sorted_keys[0]]
```

### 2. Replica Management

```python
class ReplicatedIndex:
    """
    Vector index with read replicas.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.primary = VectorIndex(config)
        self.replicas = []
        self.replication_factor = config.get("replication_factor", 3)
    
    def add_replica(self, replica: VectorIndex):
        """Add read replica."""
        self.replicas.append(replica)
    
    def write(self, vector_id: str, vector: np.ndarray):
        """Write to primary and all replicas."""
        # Write to primary
        self.primary.add(vector_id, vector)
        
        # Write to all replicas
        for replica in self.replicas:
            replica.add(vector_id, vector)
    
    def read(self, query: np.ndarray, k: int = 10) -> List[Tuple[str, float]]:
        """Read from random replica (load balancing)."""
        import random
        
        # Random replica selection
        replica = random.choice(self.replicas) if self.replicas else self.primary
        
        return replica.search(query, k)
    
    def read_with_fallback(
        self,
        query: np.ndarray,
        k: int = 10
    ) -> List[Tuple[str, float]]:
        """Read with automatic fallback to primary."""
        import random
        
        # Try replicas first
        if self.replicas:
            replica = random.choice(self.replicas)
            
            try:
                return replica.search(query, k)
            except Exception as e:
                print(f"Replica failed: {e}, falling back to primary")
        
        return self.primary.search(query, k)
```

### 3. Load Balancer

```python
class VectorSearchLoadBalancer:
    """
    Load balancer for vector search requests.
    """
    
    def __init__(self, backends: List[str]):
        self.backends = backends
        self.current_index = 0
        self.request_counts = {b: 0 for b in backends}
        self.latencies = {b: [] for b in backends}
    
    def get_backend(self) -> str:
        """Get next backend using least connections strategy."""
        # Find backend with least requests
        min_count = min(self.request_counts.values())
        
        candidates = [
            b for b, count in self.request_counts.items()
            if count == min_count
        ]
        
        # Round-robin among candidates
        for backend in candidates:
            if backend == candidates[self.current_index % len(candidates)]:
                self.request_counts[backend] += 1
                return backend
        
        # Fallback
        backend = candidates[0]
        self.request_counts[backend] += 1
        return backend
    
    def release_backend(self, backend: str, latency_ms: float):
        """Release backend after request completes."""
        self.request_counts[backend] -= 1
        self.latencies[backend].append(latency_ms)
        
        # Keep only recent latencies
        if len(self.latencies[backend]) > 100:
            self.latencies[backend] = self.latencies[backend][-100:]
    
    def get_stats(self) -> dict:
        """Get load balancer statistics."""
        return {
            backend: {
                "active_requests": self.request_counts[backend],
                "avg_latency_ms": sum(self.latencies[backend]) / 
                                  len(self.latencies[backend]) if self.latencies[backend] else 0,
                "recent_latencies": self.latencies[backend][-10:]
            }
            for backend in self.backends
        }
```

## Resource Management

### 1. Memory Management

```python
class MemoryManagedIndex:
    """
    Vector index with memory management.
    """
    
    def __init__(self, max_memory_gb: float = 8.0):
        self.max_memory_bytes = int(max_memory_gb * 1024 * 1024 * 1024)
        self.current_memory = 0
        self.segments = {}  # id -> (data, memory_size)
        self.access_times = {}  # id -> last_access_time
    
    def can_add_segment(self, segment_size_bytes: int) -> bool:
        """Check if we can add a new segment."""
        return (self.current_memory + segment_size_bytes) <= self.max_memory_bytes
    
    def add_segment(self, segment_id: str, data: np.ndarray):
        """Add segment with memory tracking."""
        import time
        
        segment_size = data.nbytes
        
        if not self.can_add_segment(segment_size):
            # Evict oldest segment
            self._evict_oldest()
        
        self.segments[segment_id] = data
        self.access_times[segment_id] = time.time()
        self.current_memory += segment_size
    
    def get_segment(self, segment_id: str) -> np.ndarray:
        """Get segment, updating access time."""
        import time
        
        if segment_id in self.segments:
            self.access_times[segment_id] = time.time()
            return self.segments[segment_id]
        
        return None
    
    def _evict_oldest(self):
        """Evict least recently used segment."""
        if not self.access_times:
            return
        
        oldest_id = min(self.access_times, key=self.access_times.get)
        
        # Free memory
        segment_size = self.segments[oldest_id].nbytes
        del self.segments[oldest_id]
        del self.access_times[oldest_id]
        self.current_memory -= segment_size
        
        print(f"Evicted segment {oldest_id}, freed {segment_size / 1024**2:.1f}MB")
    
    def get_memory_usage(self) -> dict:
        """Get current memory usage."""
        return {
            "current_mb": self.current_memory / 1024**2,
            "max_mb": self.max_memory_bytes / 1024**2,
            "usage_percent": (self.current_memory / self.max_memory_bytes) * 100,
            "num_segments": len(self.segments)
        }
```

### 2. Capacity Planning

```python
class CapacityPlanner:
    """
    Capacity planning for vector search infrastructure.
    """
    
    def __init__(self):
        self.models = {}
    
    def estimate_index_size(
        self,
        num_vectors: int,
        dimensions: int,
        index_type: str = "hnsw"
    ) -> dict:
        """
        Estimate index size for given parameters.
        """
        vector_size_bytes = dimensions * 4  # float32
        
        # Index overhead estimates
        index_overheads = {
            "hnsw": {
                "base": 3.0,  # 3x vector size for HNSW graph
                "m_16": 1.0,
                "m_32": 1.5
            },
            "ivf": {
                "base": 1.2,  # 1.2x for IVF
                "centroids": dimensions * 4 * 100  # 100 centroids
            },
            "pq": {
                "base": 0.1,  # 10% for PQ codes
                "codebook": dimensions * 256 * 4  # 256 centroids
            }
        }
        
        base_size = num_vectors * vector_size_bytes
        overhead = index_overheads[index_type]["base"]
        
        total_size = base_size * overhead
        
        return {
            "vectors_size_mb": base_size / 1024**2,
            "total_index_size_mb": total_size / 1024**2,
            "total_index_size_gb": total_size / 1024**3,
            "memory_recommendation_gb": (total_size / 1024**3) * 1.2  # 20% buffer
        }
    
    def estimate_query_throughput(
        self,
        num_vectors: int,
        hardware: str = "standard"
    ) -> dict:
        """
        Estimate query throughput based on hardware.
        """
        hardware_specs = {
            "standard": {
                "cores": 8,
                "memory_gb": 32,
                "qps_per_core": 50
            },
            "high_performance": {
                "cores": 32,
                "memory_gb": 128,
                "qps_per_core": 100
            },
            "memory_optimized": {
                "cores": 16,
                "memory_gb": 256,
                "qps_per_core": 30
            }
        }
        
        specs = hardware_specs.get(hardware, hardware_specs["standard"])
        
        # Scale factor based on dataset size
        if num_vectors < 1_000_000:
            scale_factor = 1.0
        elif num_vectors < 10_000_000:
            scale_factor = 0.7
        else:
            scale_factor = 0.5
        
        qps = specs["cores"] * specs["qps_per_core"] * scale_factor
        
        return {
            "estimated_qps": int(qps),
            "p99_latency_ms": 100 / (qps / specs["cores"]),
            "hardware": specs
        }
    
    def recommend_configuration(
        self,
        num_vectors: int,
        dimensions: int,
        target_qps: int,
        budget_tier: str = "standard"
    ) -> dict:
        """
        Recommend infrastructure configuration.
        """
        index_size = self.estimate_index_size(num_vectors, dimensions)
        
        # Memory = index size + overhead
        required_memory = index_size["memory_recommendation_gb"]
        
        # CPU cores based on QPS requirements
        if target_qps < 100:
            cores = 4
        elif target_qps < 1000:
            cores = 16
        else:
            cores = 32
        
        # Instance recommendations by tier
        recommendations = {
            "budget": {
                "instance_type": "t3.large",
                "memory_gb": required_memory + 8,
                "cores": cores,
                "estimated_cost_monthly": cores * 10
            },
            "standard": {
                "instance_type": "m6i.xlarge",
                "memory_gb": required_memory + 16,
                "cores": cores,
                "estimated_cost_monthly": cores * 25
            },
            "performance": {
                "instance_type": "m6i.4xlarge",
                "memory_gb": required_memory + 32,
                "cores": cores * 2,
                "estimated_cost_monthly": cores * 50
            }
        }
        
        return {
            "index_size": index_size,
            "required_memory_gb": required_memory,
            "recommended_config": recommendations.get(budget_tier, recommendations["standard"])
        }
```

## Examples

### Example 1: Production Deployment

```python
class ProductionVectorService:
    """
    Production-ready vector search service.
    """
    
    def __init__(self, config: dict):
        self.config = config
        
        # Initialize components
        self.cache = MultiLevelCache(config["cache"])
        self.index = ShardedVectorIndex(config["index"])
        
        # Load balancing
        self.load_balancer = VectorSearchLoadBalancer(
            config["backends"]
        )
        
        # Monitoring
        self.metrics = MetricsCollector()
        
        # Background tasks
        self.warm_up = WarmUpStrategy(self.index)
    
    async def search(
        self,
        query_vector: np.ndarray,
        filters: dict = None,
        k: int = 10,
        include_metadata: bool = True
    ) -> dict:
        """Handle search request."""
        import time
        
        start_time = time.time()
        
        # Check cache
        cache_key = self.cache.get_cache_key(query_vector, filters, k)
        cached = self.cache.get_search_result(cache_key)
        
        if cached is not None:
            return cached
        
        # Route to backend
        backend = self.load_balancer.get_backend()
        
        try:
            # Execute search
            results = await self._search_backend(
                backend,
                query_vector,
                k
            )
            
            # Cache results
            self.cache.set_search_result(cache_key, results)
            
            # Record metrics
            latency = (time.time() - start_time) * 1000
            self.metrics.record("search_latency_ms", latency)
            self.load_balancer.release_backend(backend, latency)
            
            return results
        
        except Exception as e:
            # Fallback to primary
            self.metrics.increment("search_fallback")
            return await self._search_primary(query_vector, k)
    
    async def _search_backend(
        self,
        backend: str,
        query: np.ndarray,
        k: int
    ) -> List[dict]:
        """Search specific backend."""
        # Implementation depends on backend type
        pass
    
    def health_check(self) -> dict:
        """Health check endpoint."""
        return {
            "status": "healthy",
            "index_loaded": len(self.index.shards) > 0,
            "cache_stats": self.cache.get_stats(),
            "load_balancer": self.load_balancer.get_stats()
        }
```

### Example 2: Kubernetes Deployment

```yaml
# kubernetes/vector-search-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vector-search
  labels:
    app: vector-search
spec:
  replicas: 3
  selector:
    matchLabels:
      app: vector-search
  template:
    metadata:
      labels:
        app: vector-search
    spec:
      containers:
      - name: vector-search
        image: vector-search:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "16Gi"
            cpu: "2"
          limits:
            memory: "32Gi"
            cpu: "4"
        env:
        - name: INDEX_PATH
          value: "/data/index"
        - name: REDIS_HOST
          value: "redis-service"
        volumeMounts:
        - name: index-data
          mountPath: /data
      volumes:
      - name: index-data
        persistentVolumeClaim:
          claimName: vector-index-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: vector-search-service
spec:
  selector:
    app: vector-search
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vector-search-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vector-search
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Example 3: Monitoring Dashboard

```python
class VectorSearchMonitoring:
    """
    Monitoring for vector search service.
    """
    
    def __init__(self, metrics_client):
        self.metrics = metrics_client
    
    def record_search(
        self,
        latency_ms: float,
        cache_hit: bool,
        num_results: int,
        shard: str
    ):
        """Record search metrics."""
        self.metrics.increment("search_requests_total", tags={
            "cache": "hit" if cache_hit else "miss",
            "shard": shard
        })
        
        self.metrics.gauge("search_latency_ms", latency_ms, tags={
            "shard": shard
        })
        
        self.metrics.histogram("search_results_count", num_results)
    
    def record_index_operation(
        self,
        operation: str,  # add, delete, rebuild
        duration_ms: float,
        vector_count: int
    ):
        """Record index operation metrics."""
        self.metrics.increment(f"index_{operation}_total")
        self.metrics.gauge(f"index_vector_count", vector_count)
        self.metrics.gauge(f"index_{operation}_duration_ms", duration_ms)
    
    def get_dashboard_data(self) -> dict:
        """Generate dashboard data."""
        return {
            "requests": {
                "total": self.metrics.get_counter("search_requests_total"),
                "cache_hit_rate": self._calculate_cache_hit_rate(),
                "p50_latency": self.metrics.get_percentile("search_latency_ms", 50),
                "p99_latency": self.metrics.get_percentile("search_latency_ms", 99)
            },
            "index": {
                "total_vectors": self.metrics.get_gauge("index_vector_count"),
                "size_mb": self.metrics.get_gauge("index_size_mb"),
                "shard_distribution": self._get_shard_distribution()
            },
            "system": {
                "cpu_usage": self.metrics.get_gauge("system_cpu_percent"),
                "memory_usage": self.metrics.get_gauge("system_memory_percent"),
                "cache_stats": self.metrics.get_all("cache_*")
            }
        }
```

## References

1. **Vector Database Architecture**: https://docs.pinecone.io/docs/architecture
2. **Kubernetes Vector Search**: https://kubernetes.io/docs/tutorials/
3. **Monitoring Best Practices**: https://prometheus.io/docs/practices/
4. **Cursor Enterprise Framework - Vector Search Rules**: `.cursor/rules/vector-search.mdc`
