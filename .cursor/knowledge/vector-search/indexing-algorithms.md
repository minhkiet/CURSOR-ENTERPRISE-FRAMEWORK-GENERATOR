---
title: "Indexing Algorithms"
description: "Hướng dẫn về các thuật toán indexing: HNSW, IVF, PQ, ScaNN, DiskANN, graph-based vs inverted index"
tags: ["indexing", "algorithms", "hnsw", "ivf", "pq", "scaNN", "diskann", "ann"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Indexing Algorithms

## Tổng Quan

Vector indexing algorithms là heart của bất kỳ vector database nào, quyết định trade-off giữa search speed, accuracy, và memory usage. Các thuật toán ANN (Approximate Nearest Neighbor) được thiết kế để find near neighbors nhanh chóng mà không cần exhaustive search qua toàn bộ dataset.

Có nhiều families of algorithms, mỗi loại có cơ chế và trade-offs khác nhau:

- **Graph-based**: HNSW, DiskANN - Xây dựng graph để navigate đến neighbors
- **Clustering-based**: IVF - Phân chia space thành clusters
- **Quantization-based**: PQ, SQ - Nén vectors để reduce memory và speed up comparison
- **Hybrid**: Kết hợp nhiều techniques

Việc hiểu rõ cách các thuật toán này work sẽ giúp bạn tune parameters hiệu quả và choose right algorithm cho use case.

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức chuyên sâu về vector indexing algorithms:

Đầu tiên, chúng ta sẽ tìm hiểu HNSW - thuật toán phổ biến nhất cho vector search.

Thứ hai, tài liệu hướng dẫn IVF và các clustering-based methods.

Thứ ba, chúng ta sẽ đề cập đến quantization methods (PQ, SQ).

Cuối cùng, tài liệu so sánh các algorithms và cung cấp selection guide.

## Key Concepts

### 1. Trade-off Space

```
                    Vector Indexing Trade-offs
    ==========================================
    
                         Fast Search
                              ↑
                              │
                              │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         │   HNSW           IVF+PQ        IVF   │
         │   - Best recall  - Memory eff   - Fast│
         │   - High memory  - Good recall       │
         │   - Slow build   - Medium build       │
         │                                       │
────────┼───────────────────────────────────────────┼────────
        │                                       │
   High │     Brute Force          Random Proj   │  Low
 Memory│     - Perfect recall     - Fast          │ Memory
 Usage │     - Slow for large    - Low recall    │ Usage
        │                                       │
────────┼───────────────────────────────────────────┼────────
         │                                       │
         └───────────────────┬───────────────────┘
                              │
                              │
                         Slow Search
```

### 2. Key Metrics

```python
# Key performance metrics for ANN algorithms

METRICS = {
    "recall": {
        "definition": "Percentage of true nearest neighbors found",
        "formula": "TP / (TP + FN)",
        "target": "0.95-0.99 for most applications"
    },
    "qps": {
        "definition": "Queries per second throughput",
        "factors": ["index size", "hardware", "ef_search parameter"]
    },
    "latency": {
        "definition": "Time per query (P50, P95, P99)",
        "target": "<100ms for real-time applications"
    },
    "memory": {
        "definition": "Index size in memory",
        "factors": ["vector dimensions", "index type", "compression"]
    },
    "build_time": {
        "definition": "Time to build index",
        "factors": ["dataset size", "index parameters"]
    }
}
```

## HNSW (Hierarchical Navigable Small World)

### 1. Algorithm Overview

```
HNSW Structure
==============

Layer 2:    ○────────○           (Long-range connections)
            │                   (Skip list)
Layer 1: ○─○─○─○─○─○─○─○       (Medium-range)
            │                   
Layer 0: ○─○─○─○─○─○─○─○─○─○   (All points, short-range)

Search: Start from Layer 2, greedily traverse down
        to find nearest neighbors
```

```python
# HNSW Parameters Explained

PARAMETERS = {
    "m": {
        "name": "Max connections per node",
        "range": "4-64",
        "default": 16,
        "effect": {
            "higher": "Better recall, more memory, slower build",
            "lower": "Less memory, faster build, lower recall"
        },
        "recommendation": {
            "high_recall": 32,
            "balanced": 16,
            "memory_constrained": 8
        }
    },
    "ef_construction": {
        "name": "Construction parameter",
        "range": "64-512",
        "default": 200,
        "effect": {
            "higher": "Better recall, slower build",
            "lower": "Faster build, lower recall"
        },
        "recommendation": {
            "high_recall": 400,
            "balanced": 200,
            "fast_build": 64
        }
    },
    "ef_search": {
        "name": "Search parameter",
        "range": "16-1000+",
        "default": 40,
        "effect": {
            "higher": "Better recall, slower search",
            "lower": "Faster search, lower recall"
        }
    }
}
```

### 2. Implementation Details

```python
class HNSWIndex:
    """
    HNSW index implementation (simplified conceptual view).
    """
    
    def __init__(self, m=16, ef_construction=200, max_l=0):
        self.m = m
        self.ef_construction = ef_construction
        self.max_l = max_l  # Number of layers
        
        self.layers = [[] for _ in range(max_l + 1)]
        self.graph = {}  # adjacency list
        self.vectors = {}
        
        # Statistics
        self.inserted = 0
    
    def build_index(self, vectors, ids):
        """
        Build HNSW index from vectors.
        """
        import random
        
        # Determine number of layers (probabilistic)
        # L = floor(-ln(random) * (1 / ln(1/p)))
        # where p = 1 / e for layer 0
        
        for i, (vec_id, vector) in enumerate(zip(ids, vectors)):
            self.vectors[vec_id] = vector
            
            # Calculate entry point
            ep = self._get_entry_point()
            
            # Determine max layer for this point
            max_l = self._select_layer()
            
            # Insert into each layer
            for l in range(max_l, -1, -1):
                if l == max_l and max_l > 0:
                    # For top layers, start from current ep
                    entry = ep
                else:
                    entry = self._search_layer(
                        vector, self.ef_construction, entry, l
                    )
                
                # Insert into layer
                self._insert_into_layer(vec_id, entry, l)
    
    def _select_layer(self) -> int:
        """Select layer for new point (geometric distribution)."""
        import random
        import math
        
        # p = 1 / e ≈ 0.367
        # L ≈ -ln(random) / p
        
        p = 1.0 / math.e
        r = random.random()
        l = int(-math.log(r) * p)
        
        return min(l, self.max_l)
    
    def _search_layer(self, query, ef, entry, layer):
        """
        Search within a layer using greedy algorithm.
        """
        visited = {entry}
        candidates = [(entry, self._distance(query, self.vectors[entry]))]
        results = [(entry, self._distance(query, self.vectors[entry]))]
        
        while candidates:
            # Get best candidate
            candidates.sort(key=lambda x: x[1])
            current, dist = candidates.pop(0)
            
            # Check termination
            results.sort(key=lambda x: x[1])
            if len(results) >= ef:
                break
            
            # Explore neighbors
            for neighbor in self.graph.get(current, {}).get(layer, []):
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                
                neighbor_dist = self._distance(query, self.vectors[neighbor])
                
                # Add to candidates if promising
                if len(results) < ef or neighbor_dist < results[-1][1]:
                    candidates.append((neighbor, neighbor_dist))
                    results.append((neighbor, neighbor_dist))
                    results.sort(key=lambda x: x[1])
                    if len(results) > ef:
                        results.pop()
        
        return results[0][0] if results else entry
    
    def _insert_into_layer(self, vec_id, entry, layer):
        """Insert vector into specific layer."""
        if layer not in self.graph:
            self.graph[layer] = {}
        
        if vec_id not in self.graph[layer]:
            self.graph[layer][vec_id] = []
        
        # Find neighbors
        neighbors = self._select_neighbors(entry, vec_id, layer)
        
        # Add bidirectional edges
        self.graph[layer][vec_id].extend(neighbors)
        for neighbor in neighbors:
            if neighbor not in self.graph[layer]:
                self.graph[layer][neighbor] = []
            if vec_id not in self.graph[layer][neighbor]:
                self.graph[layer][neighbor].append(vec_id)
    
    def _select_neighbors(self, entry, vec_id, layer):
        """Select M nearest neighbors from candidates."""
        candidates = [entry]
        # Add some random candidates for diversity
        # (Simplified - actual HNSW uses more complex selection)
        
        # Sort by distance
        candidates.sort(
            key=lambda x: self._distance(
                self.vectors[vec_id],
                self.vectors[x]
            )
        )
        
        return candidates[:self.m]
    
    def _distance(self, a, b):
        """Calculate cosine distance."""
        import numpy as np
        a = np.array(a)
        b = np.array(b)
        return 1 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def _get_entry_point(self):
        """Get entry point (first inserted element)."""
        if self.inserted == 0:
            return None
        return list(self.vectors.keys())[0]
    
    def search(self, query, k=10, ef=None):
        """
        Search for k nearest neighbors.
        """
        ef = ef or self.ef_search
        
        # Start from top layer
        entry = self._get_entry_point()
        
        # Descend to layer 0
        for layer in range(self.max_l, 0, -1):
            entry = self._search_layer(query, ef, entry, layer)
        
        # Final search on layer 0
        results = self._search_layer(query, ef, entry, 0)
        
        # Return top k
        results.sort(key=lambda x: x[1])
        return results[:k]
```

## IVF (Inverted File Index)

### 1. Algorithm Overview

```
IVF Index Structure
====================

Centroid 0:  [vec1, vec5, vec9, ...]
Centroid 1:  [vec2, vec6, vec10, ...]
Centroid 2:  [vec3, vec7, vec11, ...]
Centroid 3:  [vec4, vec8, vec12, ...]

Query:
1. Find nearest centroids
2. Search only those partitions
3. Merge and rank results
```

```python
# IVF Parameters

PARAMETERS = {
    "nlist": {
        "name": "Number of clusters",
        "range": "100-10000+",
        "default": 100,
        "effect": {
            "higher": "Less points per cluster, faster search, less accurate",
            "lower": "More points per cluster, slower search, more accurate"
        },
        "recommendation": {
            "small_dataset": "sqrt(N) * 4",
            "large_dataset": "sqrt(N)"
        }
    },
    "nprobe": {
        "name": "Clusters to search",
        "range": "1-nlist",
        "default": 1,
        "effect": {
            "higher": "Better recall, slower search",
            "lower": "Faster search, lower recall"
        }
    }
}
```

### 2. k-means Clustering

```python
class IVFIndex:
    """
    IVF index implementation with k-means clustering.
    """
    
    def __init__(self, nlist=100, nprobe=10, metric="cosine"):
        self.nlist = nlist
        self.nprobe = nprobe
        self.metric = metric
        
        self.centroids = []
        self.inverted_lists = [[] for _ in range(nlist)]
        self.vectors = {}
    
    def build_index(self, vectors, ids):
        """
        Build IVF index.
        """
        import numpy as np
        
        # Step 1: k-means clustering
        print("Running k-means clustering...")
        self.centroids = self._kmeans(vectors, self.nlist)
        
        # Step 2: Assign vectors to clusters
        print("Assigning vectors to clusters...")
        for vec_id, vector in zip(ids, vectors):
            self.vectors[vec_id] = vector
            
            # Find nearest centroid
            cluster_id = self._find_nearest_centroid(vector)
            self.inverted_lists[cluster_id].append(vec_id)
    
    def _kmeans(self, vectors, k, max_iter=20):
        """
        k-means clustering implementation.
        """
        import numpy as np
        
        n = len(vectors)
        
        # Initialize centroids randomly
        indices = np.random.choice(n, k, replace=False)
        centroids = [vectors[i] for i in indices]
        
        for _ in range(max_iter):
            # Assign points to nearest centroid
            clusters = [[] for _ in range(k)]
            
            for i, vector in enumerate(vectors):
                distances = [
                    self._distance(vector, c)
                    for c in centroids
                ]
                nearest = np.argmin(distances)
                clusters[nearest].append(i)
            
            # Update centroids
            new_centroids = []
            for cluster in clusters:
                if cluster:
                    cluster_vectors = [vectors[i] for i in cluster]
                    new_centroid = np.mean(cluster_vectors, axis=0)
                    new_centroids.append(new_centroid)
                else:
                    # Keep old centroid if empty
                    new_centroids.append(centroids[len(new_centroids)])
            
            centroids = new_centroids
        
        return centroids
    
    def _find_nearest_centroid(self, vector):
        """Find nearest centroid for a vector."""
        import numpy as np
        
        distances = [
            self._distance(vector, c)
            for c in self.centroids
        ]
        return np.argmin(distances)
    
    def search(self, query, k=10, nprobe=None):
        """
        Search for k nearest neighbors.
        """
        nprobe = nprobe or self.nprobe
        
        # Step 1: Find nearest centroids
        centroid_distances = [
            (i, self._distance(query, c))
            for i, c in enumerate(self.centroids)
        ]
        centroid_distances.sort(key=lambda x: x[1])
        nearest_centroids = [c[0] for c in centroid_distances[:nprobe]]
        
        # Step 2: Search in selected clusters
        candidates = []
        for cluster_id in nearest_centroids:
            for vec_id in self.inverted_lists[cluster_id]:
                dist = self._distance(query, self.vectors[vec_id])
                candidates.append((vec_id, dist))
        
        # Step 3: Sort and return top k
        candidates.sort(key=lambda x: x[1])
        return candidates[:k]
    
    def _distance(self, a, b):
        """Calculate distance."""
        import numpy as np
        a = np.array(a)
        b = np.array(b)
        
        if self.metric == "cosine":
            return 1 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        elif self.metric == "l2":
            return np.linalg.norm(a - b)
        return np.linalg.norm(a - b)
```

## Product Quantization (PQ)

### 1. Algorithm Overview

```
Product Quantization Process
===========================

Original Vector (1536 dim):
[0.1, 0.2, 0.3, 0.4, ...]

Split into M=8 subvectors (192 dim each):
Subvec 0: [0.1, 0.2, ... 192 values]
Subvec 1: [0.3, 0.4, ... 192 values]
...
Subvec 7: [... 192 values]

Each subvector quantized separately:
- k* centers per subvector
- Store centroid ID instead of values

Memory savings: 
- Original: 1536 * 4 bytes = 6KB
- PQ: 8 * 1 byte + 8 * 256 * 192 * 4 bytes ≈ 1.5KB
```

```python
class ProductQuantizer:
    """
    Product Quantization implementation.
    """
    
    def __init__(self, dim=1536, M=8, bits=8):
        self.dim = dim
        self.M = M  # Number of subvectors
        self.bits = bits  # Bits per subvector
        self.K = 2 ** bits  # Codebook size (256)
        
        self.sub_dim = dim // M
        self.codebooks = []
        self.codes = {}
    
    def train(self, vectors, max_iter=20):
        """
        Train PQ codebooks using k-means on subvectors.
        """
        import numpy as np
        
        vectors = np.array(vectors)
        n = len(vectors)
        
        # Split vectors into subvectors
        subvectors = []
        for m in range(self.M):
            start = m * self.sub_dim
            end = start + self.sub_dim
            subvectors.append(vectors[:, start:end])
        
        # Train codebook for each subvector
        self.codebooks = []
        for m, subvecs in enumerate(subvectors):
            print(f"Training codebook {m+1}/{self.M}...")
            
            # k-means on this subvector
            centroids = self._kmeans(
                subvecs, 
                self.K, 
                max_iter
            )
            self.codebooks.append(centroids)
    
    def _kmeans(self, vectors, k, max_iter=20):
        """k-means for codebook training."""
        import numpy as np
        
        n, dim = vectors.shape
        
        # Initialize centroids
        indices = np.random.choice(n, k, replace=False)
        centroids = vectors[indices]
        
        for _ in range(max_iter):
            # Assign to nearest centroid
            distances = np.zeros((n, k))
            for i in range(k):
                distances[:, i] = np.linalg.norm(
                    vectors - centroids[i], axis=1
                )
            assignments = np.argmin(distances, axis=1)
            
            # Update centroids
            new_centroids = []
            for i in range(k):
                mask = assignments == i
                if np.sum(mask) > 0:
                    new_centroids.append(vectors[mask].mean(axis=0))
                else:
                    new_centroids.append(centroids[i])
            centroids = np.array(new_centroids)
        
        return centroids
    
    def encode(self, vectors):
        """
        Encode vectors to compressed codes.
        """
        import numpy as np
        
        vectors = np.array(vectors)
        n = len(vectors)
        codes = np.zeros((n, self.M), dtype=np.uint8)
        
        for m in range(self.M):
            start = m * self.sub_dim
            end = start + self.sub_dim
            subvecs = vectors[:, start:end]
            
            # Find nearest centroid for each subvector
            distances = np.zeros((n, self.K))
            for i in range(self.K):
                distances[:, i] = np.linalg.norm(
                    subvecs - self.codebooks[m][i], axis=1
                )
            codes[:, m] = np.argmin(distances, axis=1)
        
        return codes
    
    def decode(self, codes):
        """
        Decode codes back to approximate vectors.
        """
        import numpy as np
        
        n = len(codes)
        vectors = np.zeros((n, self.dim))
        
        for m in range(self.M):
            start = m * self.sub_dim
            end = start + self.sub_dim
            vectors[:, start:end] = self.codebooks[m][codes[:, m]]
        
        return vectors
    
    def compressed_distance(self, query, codes):
        """
        Calculate approximate distances using SDC (Symmetric Distance Computation).
        """
        import numpy as np
        
        n = len(codes)
        distances = np.zeros(n)
        
        for m in range(self.M):
            # Split query
            start = m * self.sub_dim
            end = start + self.sub_dim
            query_sub = query[start:end]
            
            # Precompute distances from query to centroids
            query_distances = np.array([
                np.linalg.norm(query_sub - c)
                for c in self.codebooks[m]
            ])
            
            # Look up distances using codes
            distances += query_distances[codes[:, m]]
        
        return distances
```

## ScaNN (Scalable Nearest Neighbors)

### 1. Algorithm Overview

ScaNN combines multiple techniques for optimal performance:

```python
class ScaNNIndex:
    """
    ScaNN implementation combining PQ with asymmetric distance computation.
    """
    
    def __init__(
        self,
        dim=1536,
        M=8,
        Ks=256,  # Number of leaves in tree
        K=256,   # PQ codebook size
    ):
        self.dim = dim
        self.M = M
        self.Ks = Ks
        self.K = K
        
        self.pq = ProductQuantizer(dim, M, bits=8)
        self.tree = None
        self.leaf_centroids = []
    
    def build(self, vectors, ids):
        """Build ScaNN index."""
        # Step 1: Quantize vectors with PQ
        print("Training PQ...")
        self.pq.train(vectors)
        codes = self.pq.encode(vectors)
        
        # Step 2: Build tree over compressed representations
        print("Building tree...")
        self._build_tree(vectors, codes, ids)
    
    def search(self, query, k=10):
        """Search using tree traversal + PQ."""
        # Step 1: Find promising leaves using tree
        promising_leaves = self._search_tree(query, limit=100)
        
        # Step 2: Refine with full vectors from promising leaves
        candidates = []
        for leaf_id in promising_leaves:
            for vec_id in self.tree[leaf_id]:
                dist = self._full_distance(query, vec_id)
                candidates.append((vec_id, dist))
        
        candidates.sort(key=lambda x: x[1])
        return candidates[:k]
```

## DiskANN (Disk-based ANN)

### 1. Algorithm Overview

DiskANN is designed for billion-scale datasets that don't fit in memory:

```
DiskANN Architecture
====================

┌─────────────────────────────────────────────────────────────┐
│                        RAM                                 │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  PQ Compressed Vectors (10% of original)            │  │
│  └─────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Vamana Graph (Navigation Structure)                │  │
│  └─────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Beam Search State                                   │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                       SSD                                  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Full Vectors (stored on disk)                      │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

```python
class DiskANNIndex:
    """
    DiskANN implementation for large-scale search.
    """
    
    def __init__(self, alpha=1.2, L=100, R=32):
        self.alpha = alpha  # Search parameter
        self.L = L          # Search list size
        self.R = R          # Graph degree
        
        self.pq = None
        self.graph = {}
        self.centroid = None
    
    def build(self, vectors, ids):
        """Build DiskANN index."""
        # Step 1: Build Vamana graph
        self._build_vamana(vectors, ids)
        
        # Step 2: Compute PQ compression
        self.pq = ProductQuantizer(dim=len(vectors[0]))
        self.pq.train(vectors)
    
    def _build_vamana(self, vectors, ids):
        """Build Vamana graph (robust version of HNSW)."""
        import numpy as np
        
        n = len(vectors)
        
        # Start with random graph
        self.graph = {i: [] for i in range(n)}
        
        # Greedy graph construction with alpha parameter
        for i in range(n):
            candidates = self._鲁棒邻居(vectors[i], vectors, self.R, self.alpha)
            self.graph[i] = candidates[:self.R]
    
    def _鲁棒邻居(self, query, vectors, R, alpha):
        """Find R nearest neighbors with alpha robustness."""
        import numpy as np
        
        n = len(vectors)
        
        # Start with random candidates
        candidates = list(range(min(100, n)))
        
        # Iterative refinement
        for _ in range(3):
            # Sort candidates by distance
            distances = [np.linalg.norm(query - vectors[c]) for c in candidates]
            sorted_indices = np.argsort(distances)
            
            # Keep top R*alpha
            candidates = [candidates[i] for i in sorted_indices[:int(R * alpha)]]
            
            # Add neighbors of candidates
            for c in candidates[:10]:
                for neighbor in self.graph.get(c, []):
                    if neighbor not in candidates:
                        candidates.append(neighbor)
            
            candidates = list(set(candidates))[:200]
        
        # Return top R
        distances = [np.linalg.norm(query - vectors[c]) for c in candidates]
        sorted_indices = np.argsort(distances)
        return [candidates[i] for i in sorted_indices[:R]]
```

## Algorithm Selection Guide

### 1. Comparison Matrix

| Algorithm | Recall | Speed | Memory | Build Time | Best For |
|-----------|--------|-------|--------|-----------|----------|
| **HNSW** | Very High | Very Fast | High | Slow | Real-time search |
| **IVF** | High | Medium | Medium | Medium | Balanced |
| **IVF+PQ** | Medium-High | Fast | Low | Medium | Memory-constrained |
| **PQ-only** | Low-Medium | Very Fast | Very Low | Fast | Large-scale, low accuracy ok |
| **ScaNN** | High | Fast | Low | Medium | Production at scale |
| **DiskANN** | High | Fast | Very Low | Slow | Billion-scale |

### 2. Selection Decision Tree

```
Algorithm Selection
==================

Is memory a constraint?
├── Yes → PQ-based methods
│   ├── Very constrained → PQ-only
│   └── Some memory → IVF+PQ or ScaNN
└── No → HNSW or IVF

What's your dataset size?
├── <1M vectors → HNSW (recommended)
├── 1M - 10M → IVF+PQ or ScaNN
└── >10M → DiskANN or Qdrant/Pinecone cloud

What's your recall requirement?
├── >0.95 → HNSW with high ef
├── 0.90-0.95 → ScaNN or IVF+PQ
└── <0.90 → PQ-only or IVF

What's your build time budget?
├── Fast builds → PQ or IVF
└── Slow builds ok → HNSW
```

### 3. Parameter Tuning Guide

```python
# Parameter tuning for different scenarios

TUNING_GUIDE = {
    "hnsw": {
        "high_recall": {
            "m": 32,
            "ef_construction": 400,
            "ef_search": 200
        },
        "balanced": {
            "m": 16,
            "ef_construction": 200,
            "ef_search": 100
        },
        "fast_search": {
            "m": 12,
            "ef_construction": 128,
            "ef_search": 50
        },
        "low_memory": {
            "m": 8,
            "ef_construction": 64,
            "ef_search": 40
        }
    },
    "ivf": {
        "high_recall": {
            "nlist": 1024,
            "nprobe": 64
        },
        "balanced": {
            "nlist": 256,
            "nprobe": 20
        },
        "fast": {
            "nlist": 128,
            "nprobe": 5
        }
    },
    "pq": {
        "high_accuracy": {
            "M": 8,   # Fewer subvectors
            "bits": 12  # More bits per subvector
        },
        "balanced": {
            "M": 16,
            "bits": 8
        },
        "high_compression": {
            "M": 32,
            "bits": 4
        }
    }
}
```

## Examples

### Example 1: Benchmark Different Algorithms

```python
import time
import numpy as np

def benchmark_algorithms(
    vectors,
    queries,
    ground_truth,
    k=10
):
    """
    Benchmark different indexing algorithms.
    """
    results = {}
    
    # Brute Force (baseline)
    print("Benchmarking Brute Force...")
    start = time.time()
    bf_results = brute_force_search(vectors, queries, k)
    bf_time = time.time() - start
    bf_recall = calculate_recall(bf_results, ground_truth, k)
    
    results["brute_force"] = {
        "latency_ms": bf_time * 1000 / len(queries),
        "recall": bf_recall
    }
    
    # HNSW
    print("Building HNSW...")
    hnsw = HNSWIndex(m=16, ef_construction=200)
    hnsw.build_index(vectors, range(len(vectors)))
    
    print("Benchmarking HNSW...")
    start = time.time()
    hnsw_results = [hnsw.search(q, k=k) for q in queries]
    hnsw_time = time.time() - start
    hnsw_recall = calculate_recall(hnsw_results, ground_truth, k)
    
    results["hnsw"] = {
        "latency_ms": hnsw_time * 1000 / len(queries),
        "recall": hnsw_recall
    }
    
    # IVF
    print("Building IVF...")
    ivf = IVFIndex(nlist=100, nprobe=10)
    ivf.build_index(vectors, range(len(vectors)))
    
    print("Benchmarking IVF...")
    start = time.time()
    ivf_results = [ivf.search(q, k=k) for q in queries]
    ivf_time = time.time() - start
    ivf_recall = calculate_recall(ivf_results, ground_truth, k)
    
    results["ivf"] = {
        "latency_ms": ivf_time * 1000 / len(queries),
        "recall": ivf_recall
    }
    
    return results

def brute_force_search(vectors, queries, k):
    """Brute force search for ground truth."""
    results = []
    
    for query in queries:
        distances = np.linalg.norm(vectors - query, axis=1)
        top_k = np.argsort(distances)[:k]
        results.append([(i, distances[i]) for i in top_k])
    
    return results

def calculate_recall(results, ground_truth, k):
    """Calculate recall."""
    total_hits = 0
    
    for result, truth in zip(results, ground_truth):
        result_ids = set(r[0] for r in result)
        truth_ids = set(truth[:k])
        hits = len(result_ids & truth_ids)
        total_hits += hits
    
    return total_hits / (len(results) * k)
```

### Example 2: Hybrid Indexing

```python
class HybridIVFHNSWIndex:
    """
    Combine IVF for partitioning + HNSW within partitions.
    """
    
    def __init__(self, nlist=100, m=16, ef_construction=100):
        self.nlist = nlist
        self.m = m
        self.ef_construction = ef_construction
        
        self.centroids = []
        self.partitions = {}  # partition_id -> HNSW index
        self.vectors = {}
    
    def build(self, vectors, ids):
        """Build hybrid index."""
        import numpy as np
        
        # k-means clustering
        self.centroids = self._kmeans(vectors, self.nlist)
        
        # Build HNSW for each partition
        for i, (vec_id, vector) in enumerate(zip(ids, vectors)):
            self.vectors[vec_id] = vector
            cluster_id = self._find_nearest_centroid(vector)
            
            if cluster_id not in self.partitions:
                self.partitions[cluster_id] = HNSWIndex(
                    m=self.m,
                    ef_construction=self.ef_construction
                )
            
            self.partitions[cluster_id].vectors[vec_id] = vector
    
    def search(self, query, k=10, search_clusters=3):
        """Search with hybrid approach."""
        # Find nearest clusters
        distances = [
            (i, self._distance(query, c))
            for i, c in enumerate(self.centroids)
        ]
        distances.sort(key=lambda x: x[1])
        nearest_clusters = [d[0] for d in distances[:search_clusters]]
        
        # Search in each cluster
        all_results = []
        for cluster_id in nearest_clusters:
            if cluster_id in self.partitions:
                cluster_results = self.partitions[cluster_id].search(
                    query, k=k
                )
                all_results.extend(cluster_results)
        
        # Sort and return top k
        all_results.sort(key=lambda x: x[1])
        return all_results[:k]
```

## References

1. **HNSW Paper**: https://arxiv.org/abs/1603.09320
2. **IVF Paper**: https://www.cs.jhu.edu/~misha/MyPapers/PAMI14.pdf
3. **PQ Paper**: https://arxiv.org/abs/1510.00149
4. **ScaNN Paper**: https://arxiv.org/abs/1908.10396
5. **DiskANN Paper**: https://arxiv.org/abs/1907.06147
6. **ANN Benchmarks**: https://ann-benchmarks.com/
7. **Cursor Enterprise Framework - Vector Search Rules**: `.cursor/rules/vector-search.mdc`
