---
title: "Approximate Nearest Neighbor"
description: "Hướng dẫn về lý thuyết ANN search: recall@k, precision@k, Hamming distance, sparse vectors và binary embeddings"
tags: ["ann", "approximate-nearest-neighbor", "recall", "precision", "hamming", "binary-embedding"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Approximate Nearest Neighbor

## Tổng Quan

Approximate Nearest Neighbor (ANN) search là nền tảng của vector search, giải quyết bài toán tìm các điểm gần nhất trong không gian nhiều chiều với độ phức tạp thấp hơn đáng kể so với tìm kiếm chính xác (brute force).

Trong khi exact nearest neighbor search có độ phức tạp O(N) cho mỗi query, ANN algorithms đạt được sub-linear complexity thông qua các cấu trúc dữ liệu và thuật toán clever, chấp nhận một lượng nhỏ approximation error để đổi lấy performance gains.

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức lý thuyết và thực tiễn về ANN:

Đầu tiên, chúng ta sẽ tìm hiểu mathematical foundations của ANN search.

Thứ hai, tài liệu giải thích các metrics để đo lường ANN quality.

Thứ ba, chúng ta sẽ đề cập đến specialized variants như binary embeddings và sparse vectors.

Cuối cùng, tài liệu cung cấp practical guidance cho implementation.

## Key Concepts

### 1. The Curse of Dimensionality

```
Curse of Dimensionality
======================

As dimensionality increases:

┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  Brute Force: O(N)    ← Still requires O(N) distance calc │
│                                                              │
│  All points become nearly equidistant → Hard to distinguish │
│                                                              │
│  Random projection can help: Johnson-Lindenstrauss Lemma     │
│                                                              │
│  PR(N) ≈ 1 - (1 - 1/k)^d  (probability of finding true NN) │
│                                                              │
└─────────────────────────────────────────────────────────────┘

At d=1000, with k=10 neighbors:
- Random search finds true NN with probability ≈ 1%
- Need structured indexing to do better
```

### 2. Johnson-Lindenstrauss Lemma

```python
"""
Johnson-Lindenstrauss Lemma:
A set of N points in high-dimensional space can be projected 
to O(log N / ε²) dimensions while preserving pairwise distances 
within factor (1 ± ε).
"""

import numpy as np

def generate_projection_matrix(
    original_dim: int,
    target_dim: int
) -> np.ndarray:
    """
    Generate random projection matrix.
    
    For JL guarantee with ε = 0.1:
    target_dim ≈ 10 * log(N) / ε²
    """
    # Gaussian projection (works but slow)
    return np.random.randn(target_dim, original_dim) / np.sqrt(target_dim)

def project_with_jl(
    vectors: np.ndarray,
    target_dim: int
) -> np.ndarray:
    """
    Project vectors to lower dimension using JL.
    """
    n = len(vectors)
    
    # Generate projection matrix
    P = generate_projection_matrix(vectors.shape[1], target_dim)
    
    # Project
    projected = vectors @ P.T
    
    # Normalize
    norms = np.linalg.norm(projected, axis=1, keepdims=True)
    projected = projected / (norms + 1e-10)
    
    return projected
```

## Metrics

### 1. Recall@k

```python
def recall_at_k(
    ann_results: List[List[int]],
    ground_truth: List[List[int]],
    k: int
) -> float:
    """
    Calculate Recall@K.
    
    Recall@K = (1/N) * Σ |Ann_k ∩ True_k| / K
    
    Where:
    - Ann_k = Top K results from ANN algorithm
    - True_k = True K nearest neighbors
    - N = Number of queries
    """
    total_hits = 0
    total_possible = 0
    
    for ann, truth in zip(ann_results, ground_truth):
        ann_set = set(ann[:k])
        truth_set = set(truth[:k])
        
        hits = len(ann_set & truth_set)
        total_hits += hits
        total_possible += k
    
    return total_hits / total_possible if total_possible > 0 else 0.0

# Example
ann_results = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
ground_truth = [[1, 2, 6, 7, 8], [6, 7, 9, 10, 11]]
k = 5

recall = recall_at_k(ann_results, ground_truth, k)
print(f"Recall@{k}: {recall:.4f}")  # Output: 0.6 (60%)
```

### 2. Precision@k

```python
def precision_at_k(
    ann_results: List[List[int]],
    ground_truth: List[List[int]],
    k: int
) -> float:
    """
    Calculate Precision@K.
    
    Precision@K = (1/N) * Σ |Ann_k ∩ True_k| / K
    """
    total_hits = 0
    total_returned = 0
    
    for ann, truth in zip(ann_results, ground_truth):
        ann_set = set(ann[:k])
        truth_set = set(truth[:k])
        
        hits = len(ann_set & truth_set)
        total_hits += hits
        total_returned += k
    
    return total_hits / total_returned if total_returned > 0 else 0.0
```

### 3. R-precision

```python
def r_precision(
    ann_results: List[List[int]],
    ground_truth: List[List[int]]
) -> float:
    """
    R-precision: Precision@R where R = number of relevant items.
    """
    total_score = 0
    
    for ann, truth in zip(ann_results, ground_truth):
        r = len(truth)  # Number of relevant items
        ann_set = set(ann[:r])
        truth_set = set(truth)
        
        hits = len(ann_set & truth_set)
        total_score += hits / r if r > 0 else 0.0
    
    return total_score / len(ann_results) if ann_results else 0.0
```

### 4. Average Precision (AP) và MAP

```python
def average_precision(
    ann_results: List[int],
    relevant: Set[int]
) -> float:
    """
    Calculate Average Precision for a single query.
    
    AP = (1/|relevant|) * Σ Precision@i * rel_i
    
    Where rel_i = 1 if i-th result is relevant, 0 otherwise
    """
    if not relevant:
        return 0.0
    
    hits = 0
    sum_precision = 0.0
    
    for i, result_id in enumerate(ann_results, 1):
        if result_id in relevant:
            hits += 1
            precision_at_i = hits / i
            sum_precision += precision_at_i
    
    return sum_precision / len(relevant)

def mean_average_precision(
    ann_results: List[List[int]],
    relevant_lists: List[Set[int]]
) -> float:
    """
    Calculate Mean Average Precision (MAP).
    """
    aps = [
        average_precision(ann, relevant)
        for ann, relevant in zip(ann_results, relevant_lists)
    ]
    
    return sum(aps) / len(aps) if aps else 0.0
```

### 5. NDCG (Normalized Discounted Cumulative Gain)

```python
def ndcg_at_k(
    ann_results: List[List[int]],
    relevance_scores: List[List[float]],
    k: int
) -> float:
    """
    Calculate NDCG@K.
    
    NDCG = DCG / IDCG
    
    DCG@K = Σ (rel_i / log2(i+1))
    IDCG@K = DCG@K for ideal ordering
    """
    def dcg_at_k(results, relevance, k):
        dcg = 0.0
        for i, result_id in enumerate(results[:k], 1):
            rel = relevance[result_id] if result_id < len(relevance) else 0
            dcg += rel / np.log2(i + 1)
        return dcg
    
    ndcgs = []
    for results, relevance in zip(ann_results, relevance_scores):
        # Create ideal ordering
        ideal_order = sorted(
            range(len(relevance)),
            key=lambda i: relevance[i],
            reverse=True
        )
        
        dcg = dcg_at_k(results, relevance, k)
        idcg = dcg_at_k(ideal_order, relevance, k)
        
        ndcg = dcg / idcg if idcg > 0 else 0.0
        ndcgs.append(ndcg)
    
    return sum(ndcgs) / len(ndcgs) if ndcgs else 0.0
```

## Hamming Distance

### 1. Binary Vectors và Hamming Distance

```python
"""
Hamming Distance: Number of positions where bits differ.

Example:
  a = 1 0 1 1 0 1 0
  b = 1 1 1 0 0 1 0
  ───────────────────
  d = 0 1 0 1 0 0 0  → Hamming distance = 2
"""

def hamming_distance(a: np.ndarray, b: np.ndarray) -> int:
    """Calculate Hamming distance between two binary vectors."""
    return np.sum(a != b)

def hamming_distance_fast(a: int, b: int) -> int:
    """Fast Hamming distance for bit-packed integers."""
    # XOR gives 1s where bits differ
    xor = a ^ b
    # Count 1s using Brian Kernighan's algorithm
    count = 0
    while xor:
        xor &= (xor - 1)
        count += 1
    return count

# For 128-bit vectors, pack into 2 integers
def hamming_distance_128bit(a: np.ndarray, b: np.ndarray) -> int:
    """Hamming distance for 128-bit vectors packed into 2 integers."""
    a_packed = np.packbits(a).view(np.uint64)
    b_packed = np.packbits(b).view(np.uint64)
    
    return hamming_distance_fast(a_packed[0], b_packed[0]) + \
           hamming_distance_fast(a_packed[1], b_packed[1])
```

### 2. Binary Embedding Generation

```python
class BinaryEmbeddingGenerator:
    """
    Generate binary embeddings from real-valued vectors.
    """
    
    def __init__(self, method="sign"):
        self.method = method
        self.thresholds = None
    
    def fit(self, vectors: np.ndarray):
        """
        Fit the binarizer on training data.
        """
        if self.method == "sign":
            # Simple sign function
            self.thresholds = np.zeros(vectors.shape[1])
        elif self.method == "mean":
            # Use mean as threshold
            self.thresholds = vectors.mean(axis=0)
        elif self.method == "median":
            # Use median as threshold
            self.thresholds = np.median(vectors, axis=0)
        elif self.method == "lsh":
            # Random projection thresholds (for LSH)
            self.thresholds = np.random.randn(vectors.shape[1])
    
    def transform(self, vectors: np.ndarray) -> np.ndarray:
        """
        Transform vectors to binary.
        """
        return (vectors > self.thresholds).astype(np.uint8)
    
    def fit_transform(self, vectors: np.ndarray) -> np.ndarray:
        """
        Fit and transform in one step.
        """
        self.fit(vectors)
        return self.transform(vectors)
```

### 3. Fast Search với Binary Vectors

```python
class BinaryIndex:
    """
    Fast vector index using binary embeddings and Hamming distance.
    """
    
    def __init__(self, bits=128):
        self.bits = bits
        self.vectors = {}
        self.packed_vectors = []
    
    def add(self, ids, vectors):
        """
        Add vectors to index.
        """
        for vec_id, vector in zip(ids, vectors):
            self.vectors[vec_id] = vector
        
        # Pack to bit arrays
        self.packed_vectors = [
            self._pack_vector(v)
            for v in vectors
        ]
    
    def _pack_vector(self, vector):
        """Pack float vector to bit array."""
        binary = (vector > 0).astype(np.uint8)
        return np.packbits(binary)
    
    def search(self, query, k=10, max_hamming=None):
        """
        Search for nearest neighbors using Hamming distance.
        """
        query_packed = self._pack_vector(query)
        
        distances = []
        for i, packed in enumerate(self.packed_vectors):
            dist = self._hamming_packed(query_packed, packed)
            
            if max_hamming is None or dist <= max_hamming:
                distances.append((i, dist))
        
        # Sort by distance
        distances.sort(key=lambda x: x[1])
        
        return distances[:k]
    
    def _hamming_packed(self, a, b):
        """Calculate Hamming distance between packed bit arrays."""
        xor = np.bitwise_xor(a, b)
        return sum(bin(x).count('1') for x in xor)
    
    def search_range(self, query, min_hamming, max_hamming):
        """
        Search for vectors within Hamming distance range.
        """
        query_packed = self._pack_vector(query)
        
        results = []
        for i, packed in enumerate(self.packed_vectors):
            dist = self._hamming_packed(query_packed, packed)
            
            if min_hamming <= dist <= max_hamming:
                results.append((i, dist))
        
        return sorted(results, key=lambda x: x[1])
```

## Sparse Vectors

### 1. Sparse Representation

```python
from scipy.sparse import csr_matrix, csc_matrix
from typing import List, Tuple

class SparseVectorIndex:
    """
    Index for sparse vectors (e.g., BM25, TF-IDF).
    """
    
    def __init__(self):
        self.vectors = {}  # id -> sparse vector
        self.indices = []  # Ordered list of ids
        self.dimensions = set()
    
    def add(self, ids: List[str], vectors: List[dict]):
        """
        Add sparse vectors.
        
        vectors: List of dicts mapping index -> value
        """
        for vec_id, vector_dict in zip(ids, vectors):
            self.vectors[vec_id] = vector_dict
            self.indices.append(vec_id)
            self.dimensions.update(vector_dict.keys())
    
    def search_dense(
        self,
        query: dict,
        k: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Search using dense representation.
        """
        results = []
        
        for vec_id, sparse_vec in self.vectors.items():
            score = self._sparse_dot(query, sparse_vec)
            results.append((vec_id, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]
    
    def _sparse_dot(self, a: dict, b: dict) -> float:
        """Sparse dot product."""
        score = 0.0
        
        for idx, val in a.items():
            if idx in b:
                score += val * b[idx]
        
        return score
    
    def search_inverted_index(
        self,
        query: dict,
        k: int = 10,
        limit_postings: int = 100
    ) -> List[Tuple[str, float]]:
        """
        Search using inverted index (more efficient for sparse).
        """
        # Build inverted index
        posting_lists = {}
        for vec_id, sparse_vec in self.vectors.items():
            for idx, val in sparse_vec.items():
                if idx not in posting_lists:
                    posting_lists[idx] = []
                posting_lists[idx].append((vec_id, val))
        
        # Score documents
        doc_scores = {}
        for idx, query_val in query.items():
            if idx in posting_lists:
                for vec_id, vec_val in posting_lists[idx][:limit_postings]:
                    if vec_id not in doc_scores:
                        doc_scores[vec_id] = 0.0
                    doc_scores[vec_id] += query_val * vec_val
        
        # Sort and return
        results = [(vec_id, score) for vec_id, score in doc_scores.items()]
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]
```

### 2. Sparse Matrix Operations

```python
def create_sparse_matrix(
    vectors: List[dict],
    vocab_size: int
) -> csr_matrix:
    """
    Create sparse matrix from list of sparse vectors.
    """
    import numpy as np
    from scipy.sparse import csr_matrix
    
    n = len(vectors)
    
    # Collect all indices and values
    rows, cols, data = [], [], []
    
    for i, vec in enumerate(vectors):
        for idx, val in vec.items():
            if idx < vocab_size:
                rows.append(i)
                cols.append(idx)
                data.append(val)
    
    return csr_matrix(
        (data, (rows, cols)),
        shape=(n, vocab_size)
    )

def sparse_to_dense(sparse_matrix: csr_matrix) -> np.ndarray:
    """Convert sparse matrix to dense."""
    return sparse_matrix.toarray()

def dense_to_sparse(dense_matrix: np.ndarray) -> csr_matrix:
    """Convert dense matrix to sparse."""
    return csr_matrix(dense_matrix)
```

## Binary Quantization (BQ)

### 1. Binary Quantization Overview

```python
class BinaryQuantizer:
    """
    Binary Quantization for efficient similarity search.
    
    Benefits:
    - Storage: 32x reduction (float32 → 1 bit)
    - Distance: XOR + POPCOUNT (very fast)
    - Memory: Fits in CPU cache
    """
    
    def __init__(self, n_bits=128):
        self.n_bits = n_bits
        self.codebooks = []
        self.binary_codes = []
    
    def train(self, vectors: np.ndarray, n_clusters=256):
        """
        Train binary quantizer using k-means.
        """
        from sklearn.cluster import MiniBatchKMeans
        
        # Store original vectors
        self.original_dim = vectors.shape[1]
        
        # Split into subvectors
        n_subvecs = self.n_bits // 8
        subvec_dim = self.original_dim // n_subvecs
        
        self.codebooks = []
        
        for i in range(n_subvecs):
            start = i * subvec_dim
            end = start + subvec_dim
            subvecs = vectors[:, start:end]
            
            # k-means to find centroids
            kmeans = MiniBatchKMeans(
                n_clusters=n_clusters,
                random_state=42
            )
            kmeans.fit(subvecs)
            
            # Binarize centroids
            binary_centroids = (kmeans.cluster_centers_ > 0).astype(np.uint8)
            self.codebooks.append(binary_centroids)
    
    def encode(self, vectors: np.ndarray) -> np.ndarray:
        """
        Encode vectors to binary codes.
        """
        n_samples = len(vectors)
        n_subvecs = self.n_bits // 8
        subvec_dim = self.original_dim // n_subvecs
        
        codes = np.zeros((n_samples, n_subvecs), dtype=np.uint8)
        
        for i in range(n_subvecs):
            start = i * subvec_dim
            end = start + subvec_dim
            subvecs = vectors[:, start:end]
            
            # Find nearest centroid for each subvector
            for j, subvec in enumerate(subvecs):
                distances = np.linalg.norm(
                    self.codebooks[i] - subvec,
                    axis=1
                )
                nearest = np.argmin(distances)
                codes[j, i] = nearest
        
        return codes
    
    def decode(self, codes: np.ndarray) -> np.ndarray:
        """
        Decode binary codes back to vectors.
        """
        n_samples = len(codes)
        n_subvecs = self.n_bits // 8
        subvec_dim = self.original_dim // n_subvecs
        
        vectors = np.zeros((n_samples, self.original_dim))
        
        for i in range(n_subvecs):
            start = i * subvec_dim
            end = start + subvec_dim
            vectors[:, start:end] = self.codebooks[i][codes[:, i]]
        
        return vectors
    
    def compressed_distance(
        self,
        query: np.ndarray,
        codes: np.ndarray
    ) -> np.ndarray:
        """
        Calculate approximate distances using asymmetric distance computation.
        """
        n_samples = len(codes)
        n_subvecs = self.n_bits // 8
        subvec_dim = self.original_dim // n_subvecs
        
        distances = np.zeros(n_samples)
        
        for i in range(n_subvecs):
            start = i * subvec_dim
            end = start + subvec_dim
            query_sub = query[start:end]
            
            # Quantize query subvector
            query_binary = (query_sub > 0).astype(np.uint8)
            
            # Calculate distance to each code
            for j, code in enumerate(codes[:, i]):
                centroid = self.codebooks[i][code]
                dist = np.sum(query_binary != centroid)
                distances[j] += dist
        
        return distances
```

## Locality-Sensitive Hashing (LSH)

### 1. LSH Overview

```python
class LSHIndex:
    """
    Locality-Sensitive Hashing for approximate nearest neighbor search.
    """
    
    def __init__(self, n_hashes=10, n_bits=128):
        self.n_hashes = n_hashes
        self.n_bits = n_bits
        self.hash_tables = [{} for _ in range(n_hashes)]
        self.hash_functions = []
    
    def fit(self, vectors: np.ndarray):
        """
        Generate random projection hash functions.
        """
        import numpy as np
        
        self.hash_functions = [
            np.random.randn(len(vectors[0]))
            for _ in range(self.n_hashes)
        ]
    
    def _hash(self, vector: np.ndarray, hash_fn: np.ndarray) -> int:
        """Hash a single vector with one hash function."""
        import numpy as np
        
        projection = np.dot(vector, hash_fn)
        return 1 if projection > 0 else 0
    
    def _hash_to_int(self, vector: np.ndarray) -> int:
        """Convert binary hash to integer."""
        import numpy as np
        
        bits = [
            self._hash(vector, h)
            for h in self.hash_functions
        ]
        return int(''.join(map(str, bits)), 2)
    
    def add(self, ids: List[str], vectors: np.ndarray):
        """
        Add vectors to LSH index.
        """
        for vec_id, vector in zip(ids, vectors):
            hash_val = self._hash_to_int(vector)
            
            for i, h in enumerate(self.hash_functions):
                bucket_key = self._hash(vector, h)
                
                if bucket_key not in self.hash_tables[i]:
                    self.hash_tables[i][bucket_key] = []
                self.hash_tables[i][bucket_key].append(vec_id)
    
    def search(
        self,
        query: np.ndarray,
        k: int = 10,
        candidates_multiplier: int = 5
    ) -> List[Tuple[str, int]]:
        """
        Search for nearest neighbors.
        """
        candidates = set()
        
        # Get candidates from each hash table
        for i, h in enumerate(self.hash_functions):
            bucket_key = self._hash(query, h)
            
            if bucket_key in self.hash_tables[i]:
                candidates.update(self.hash_tables[i][bucket_key])
        
        # Calculate exact distances
        results = []
        for vec_id in candidates:
            # Store distance calculation here
            # (Would need to look up vector and compute distance)
            results.append((vec_id, 0))  # Placeholder
        
        results.sort(key=lambda x: x[1])
        return results[:k]
```

## Best Practices

### 1. Metric Selection

```python
# When to use which metric

METRIC_GUIDE = {
    "cosine_similarity": {
        "use_when": [
            "Text embeddings (usually normalized)",
            "When angle matters more than magnitude",
            "Document similarity"
        ],
        "pros": ["Scale-invariant", "Works well with text"],
        "cons": ["Not optimal for very high dimensions"]
    },
    "euclidean_distance": {
        "use_when": [
            "Image embeddings",
            "When absolute distance matters",
            "Coordinates/positions"
        ],
        "pros": ["Intuitive for spatial data"],
        "cons": ["Sensitive to scale"]
    },
    "dot_product": {
        "use_when": [
            "Unnormalized neural embeddings",
            "Recommendation systems",
            "When magnitude matters"
        ],
        "pros": ["Works well with raw NN outputs"],
        "cons": ["Not normalized"]
    },
    "hamming_distance": {
        "use_when": [
            "Binary embeddings",
            "Memory-constrained environments",
            "Very high dimensions"
        ],
        "pros": ["Fast computation", "Low memory"],
        "cons": ["Information loss"]
    }
}
```

### 2. Quality vs Speed Trade-off

```python
def tune_recall_vs_speed(
    target_recall: float,
    current_latency_ms: float
) -> dict:
    """
    Suggest parameter adjustments based on recall/speed requirements.
    """
    
    if target_recall >= 0.99:
        return {
            "hnsw_ef_search": 500,
            "hnsw_ef_construction": 400,
            "expected_latency_increase": "3-5x"
        }
    elif target_recall >= 0.95:
        return {
            "hnsw_ef_search": 200,
            "hnsw_ef_construction": 200,
            "expected_latency_increase": "1.5-2x"
        }
    elif target_recall >= 0.90:
        return {
            "hnsw_ef_search": 100,
            "hnsw_ef_construction": 128,
            "expected_latency_increase": "baseline"
        }
    else:
        return {
            "hnsw_ef_search": 50,
            "hnsw_ef_construction": 64,
            "expected_latency_increase": "0.5x"
        }
```

## Examples

### Example 1: Comprehensive ANN Evaluation

```python
import numpy as np
from typing import List, Dict

class ANNEvaluator:
    """
    Comprehensive evaluation framework for ANN algorithms.
    """
    
    def __init__(self, k_values=[1, 5, 10, 50, 100]):
        self.k_values = k_values
        self.results = {}
    
    def evaluate(
        self,
        ann_results: Dict[str, List[List[int]]],
        ground_truth: List[List[int]],
        query_latencies: Dict[str, List[float]]
    ) -> Dict:
        """
        Comprehensive evaluation of ANN results.
        """
        evaluation = {
            "recall": {},
            "precision": {},
            "latency": {},
            "qps": {}
        }
        
        # Calculate metrics for each algorithm
        for algo, results in ann_results.items():
            # Recall metrics
            evaluation["recall"][algo] = {
                f"recall@{k}": recall_at_k(results, ground_truth, k)
                for k in self.k_values
            }
            
            # Precision metrics
            evaluation["precision"][algo] = {
                f"precision@{k}": precision_at_k(results, ground_truth, k)
                for k in self.k_values
            }
            
            # Latency metrics
            latencies = query_latencies.get(algo, [])
            if latencies:
                evaluation["latency"][algo] = {
                    "mean_ms": np.mean(latencies),
                    "p50_ms": np.percentile(latencies, 50),
                    "p95_ms": np.percentile(latencies, 95),
                    "p99_ms": np.percentile(latencies, 99)
                }
        
        return evaluation
    
    def generate_report(self, evaluation: Dict) -> str:
        """Generate human-readable report."""
        report = []
        report.append("=" * 60)
        report.append("ANN EVALUATION REPORT")
        report.append("=" * 60)
        
        # Recall section
        report.append("\nRECALL METRICS")
        report.append("-" * 40)
        for algo, metrics in evaluation["recall"].items():
            report.append(f"\n{algo}:")
            for metric, value in metrics.items():
                report.append(f"  {metric}: {value:.4f}")
        
        # Latency section
        report.append("\n\nLATENCY METRICS (ms)")
        report.append("-" * 40)
        for algo, metrics in evaluation["latency"].items():
            report.append(f"\n{algo}:")
            for metric, value in metrics.items():
                report.append(f"  {metric}: {value:.2f}")
        
        return "\n".join(report)
```

### Example 2: Adaptive Search Strategy

```python
class AdaptiveSearch:
    """
    Adaptive search that adjusts parameters based on query characteristics.
    """
    
    def __init__(self, base_index):
        self.index = base_index
    
    def search(
        self,
        query: np.ndarray,
        recall_target: float = 0.95,
        time_budget_ms: float = 100.0
    ):
        """
        Search with adaptive parameter tuning.
        """
        import time
        
        # Start with fast parameters
        ef_search = 40
        start_time = time.time()
        
        while True:
            # Search with current ef
            results = self.index.search(query, ef=ef_search)
            
            elapsed = (time.time() - start_time) * 1000
            
            # Estimate if we can afford more time
            if elapsed >= time_budget_ms:
                break
            
            # Estimate recall improvement
            estimated_recall = self._estimate_recall(ef_search)
            
            if estimated_recall >= recall_target:
                break
            
            # Increase ef for better recall
            ef_search = min(ef_search * 2, 1000)
        
        return results
    
    def _estimate_recall(self, ef_search: int) -> float:
        """
        Estimate recall based on ef_search.
        (Would use historical data in production)
        """
        # Simplified estimation
        return min(1.0, ef_search / 200)
```

## References

1. **ANN Survey**: https://arxiv.org/abs/1906.10736
2. **Hamming Distance**: https://en.wikipedia.org/wiki/Hamming_distance
3. **LSH**: https://en.wikipedia.org/wiki/Locality-sensitive_hashing
4. **Binary Quantization**: https://arxiv.org/abs/1709.09118
5. **Cursor Enterprise Framework - Vector Search Rules**: `.cursor/rules/vector-search.mdc`
