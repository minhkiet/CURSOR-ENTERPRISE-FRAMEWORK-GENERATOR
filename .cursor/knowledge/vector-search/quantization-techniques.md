---
title: "Quantization Techniques"
description: "Hướng dẫn về quantization: scalar quantization, product quantization, binary quantization, quality degradation và speed gains"
tags: ["quantization", "compression", "product-quantization", "binary-quantization", "vector-search"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Quantization Techniques

## Tổng Quan

Quantization là kỹ thuật nén vectors bằng cách reduce precision của các giá trị, cho phép lưu trữ nhiều vectors hơn trong cùng bộ nhớ và tăng tốc độ similarity computation. Thay vì lưu trữ float32 (4 bytes per value), quantization có thể reduce xuống int8 (1 byte) hoặc thậm chí binary (1 bit).

Trade-off chính là quantization introduces approximation error, có thể dẫn đến giảm recall nếu không được implement đúng cách. Tuy nhiên, với proper techniques, có thể achieve good balance giữa compression, speed, và accuracy.

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức toàn diện về quantization techniques:

Đầu tiên, chúng ta sẽ tìm hiểu scalar quantization (SQ) - đơn giản nhất.

Thứ hai, tài liệu hướng dẫn product quantization (PQ) - phổ biến nhất cho vector search.

Thứ ba, chúng ta sẽ đề cập đến binary quantization và optimizations.

Cuối cùng, tài liệu phân tích quality vs speed trade-offs và implementation strategies.

## Key Concepts

### 1. Quantization Overview

```
Quantization Spectrum
====================

┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  Float32 (4 bytes) ──────► Int8 (1 byte) ──────► Binary (1 bit) │
│                                                              │
│  ┌─────────┐        ┌─────────┐        ┌─────────┐         │
│  │ Original │        │ Quantized│        │ Compressed│        │
│  │ 0.1234   │   ──►  │    12   │   ──►  │     1   │        │
│  │ 0.5678   │        │    57   │        │     0   │        │
│  │ 0.9012   │        │    90   │        │     1   │        │
│  └─────────┘        └─────────┘        └─────────┘         │
│                                                              │
│  Compression: 1x            4x              32x            │
│  Speed:       1x            4x              32x+            │
│  Accuracy:    100%          95-99%         85-95%           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2. Quantization Error

```python
def quantization_error(original: np.ndarray, quantized: np.ndarray) -> float:
    """
    Calculate quantization error.
    
    Metrics:
    - MSE: Mean Squared Error
    - RMSE: Root Mean Squared Error
    - Relative Error: ||q - x|| / ||x||
    """
    mse = np.mean((original - quantized) ** 2)
    rmse = np.sqrt(mse)
    relative_error = np.linalg.norm(original - quantized) / np.linalg.norm(original)
    
    return {
        "mse": mse,
        "rmse": rmse,
        "relative_error": relative_error
    }
```

## Scalar Quantization (SQ)

### 1. Theory

```python
"""
Scalar Quantization (SQ) / Uniform Quantization

原理: 
1. Tìm min và max values trong vector set
2. Chia range thành 2^b bins (b = bits per value)
3. Map mỗi value vào bin index

Ví dụ: Float32 → Int8 (b = 8, 256 bins)
- Range: [-1.0, 1.0]
- Bin size: 2.0 / 256 ≈ 0.0078
- Value 0.5 → bin 96 → store as int8(96)
"""
```

### 2. Implementation

```python
class ScalarQuantizer:
    """
    Scalar quantization for vectors.
    """
    
    def __init__(self, bits=8):
        self.bits = bits
        self.levels = 2 ** bits  # 256 for int8
        self.scale = None  # bin size
        self.offset = None  # for non-zero centered data
    
    def fit(self, vectors: np.ndarray):
        """
        Fit quantizer on training data.
        
        Computes min, max, scale for quantization.
        """
        # Find min and max
        vmin = vectors.min()
        vmax = vectors.max()
        
        # Compute scale and offset
        self.scale = (vmax - vmin) / self.levels
        self.offset = vmin
        
        return self
    
    def quantize(self, vectors: np.ndarray) -> np.ndarray:
        """
        Quantize vectors to integer values.
        """
        # Shift and scale
        shifted = vectors - self.offset
        quantized = shifted / self.scale
        
        # Round to nearest integer
        quantized = np.round(quantized).astype(np.int32)
        
        # Clip to valid range
        quantized = np.clip(quantized, 0, self.levels - 1)
        
        return quantized
    
    def dequantize(self, quantized: np.ndarray) -> np.ndarray:
        """
        Convert quantized values back to floats.
        """
        # Scale back
        return quantized.astype(np.float32) * self.scale + self.offset
    
    def fit_quantize(self, vectors: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fit and quantize in one step.
        """
        self.fit(vectors)
        return self.quantize(vectors), self.scale


class LearnedScalarQuantizer:
    """
    Scalar quantization with learned boundaries.
    Uses k-means to find optimal bin boundaries.
    """
    
    def __init__(self, bits=8):
        self.bits = bits
        self.codebook = None  # bin centers
    
    def fit(self, vectors: np.ndarray):
        """
        Fit using k-means clustering.
        """
        from sklearn.cluster import KMeans
        
        n_clusters = 2 ** self.bits
        
        # Flatten for clustering
        flat_vectors = vectors.flatten().reshape(-1, 1)
        
        # K-means to find centers
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        kmeans.fit(flat_vectors)
        
        # Sort centers for faster lookup
        self.codebook = np.sort(kmeans.cluster_centers_.flatten())
        
        return self
    
    def quantize(self, vectors: np.ndarray) -> np.ndarray:
        """
        Quantize using nearest center lookup.
        """
        flat = vectors.flatten()
        
        # Find nearest center for each value
        indices = np.searchsorted(self.codebook, flat)
        
        # Handle edge cases
        indices = np.clip(indices, 0, len(self.codebook) - 1)
        
        # Adjust for exact match
        for i, val in enumerate(flat):
            if indices[i] > 0 and (indices[i] >= len(self.codebook) or 
                abs(self.codebook[indices[i]] - val) > abs(self.codebook[indices[i] - 1] - val)):
                indices[i] -= 1
        
        return indices.astype(np.int32)
    
    def dequantize(self, indices: np.ndarray) -> np.ndarray:
        """Convert indices back to values."""
        original_shape = indices.shape
        flat_indices = indices.flatten()
        
        values = self.codebook[flat_indices]
        
        return values.reshape(original_shape)
```

## Product Quantization (PQ)

### 1. Theory

```python
"""
Product Quantization (PQ)

原理:
1. Chia vector thành M subvectors
2. Mỗi subvector được quantize độc lập bằng k-means
3. Store centroid index thay vì original values

Ví dụ: 128-dim float32 → M=16 subvectors, each 8-dim
- Each subvector: 8 floats * 4 bytes = 32 bytes
- After PQ: 16 * 1 byte = 16 bytes
- Compression: 50%

Benefits:
- High compression ratio
- Fast distance computation via lookup tables
- Works well for high-dimensional vectors
"""
```

### 2. Implementation

```python
class ProductQuantizer:
    """
    Product Quantization implementation.
    """
    
    def __init__(
        self,
        dim: int = 128,
        M: int = 8,  # Number of subvectors
        n_bits: int = 8  # Bits per subvector
    ):
        self.dim = dim
        self.M = M
        self.n_bits = n_bits
        self.K = 2 ** n_bits  # 256 centroids per subvector
        
        self.sub_dim = dim // M
        self.codebooks = []  # M arrays of K centroids each
        
        # Statistics
        self.training_vectors = None
    
    def fit(self, vectors: np.ndarray, max_iter: int = 20):
        """
        Train PQ codebooks using k-means on each subvector.
        """
        import numpy as np
        
        self.training_vectors = vectors
        n_vectors = len(vectors)
        
        # Split vectors into subvectors
        # subvectors[m] has shape (n_vectors, sub_dim)
        subvectors = np.array_split(vectors, self.M, axis=1)
        
        self.codebooks = []
        
        for m in range(self.M):
            print(f"Training subvector {m+1}/{self.M}...")
            
            # Get subvectors for this segment
            subvec = subvectors[m]
            
            # K-means clustering
            centroids = self._kmeans(
                subvec, 
                n_clusters=self.K, 
                max_iter=max_iter
            )
            
            self.codebooks.append(centroids)
        
        return self
    
    def _kmeans(
        self,
        vectors: np.ndarray,
        n_clusters: int,
        max_iter: int
    ) -> np.ndarray:
        """K-means clustering for one subvector."""
        import numpy as np
        from sklearn.cluster import MiniBatchKMeans
        
        # Use MiniBatchKMeans for speed
        kmeans = MiniBatchKMeans(
            n_clusters=n_clusters,
            max_iter=max_iter,
            random_state=42,
            batch_size=1000,
            n_init=3
        )
        
        kmeans.fit(vectors)
        
        return kmeans.cluster_centers_
    
    def encode(self, vectors: np.ndarray) -> np.ndarray:
        """
        Encode vectors to compressed codes.
        
        Returns:
            codes: shape (n_vectors, M), dtype uint8
        """
        import numpy as np
        
        n_vectors = len(vectors)
        codes = np.zeros((n_vectors, self.M), dtype=np.uint8)
        
        # Split into subvectors
        subvectors = np.array_split(vectors, self.M, axis=1)
        
        for m in range(self.M):
            subvec = subvectors[m]
            
            # Find nearest centroid for each subvector
            # Using efficient vectorized distance computation
            centroids = self.codebooks[m]  # (K, sub_dim)
            
            # Compute distances: (n, sub_dim) - (K, sub_dim) -> (n, K)
            distances = np.linalg.norm(
                subvec[:, np.newaxis, :] - centroids[np.newaxis, :, :],
                axis=2
            )
            
            # Assign to nearest centroid
            codes[:, m] = np.argmin(distances, axis=1).astype(np.uint8)
        
        return codes
    
    def decode(self, codes: np.ndarray) -> np.ndarray:
        """
        Decode compressed codes back to approximate vectors.
        
        Args:
            codes: shape (n_vectors, M), dtype uint8
        
        Returns:
            vectors: shape (n_vectors, dim)
        """
        import numpy as np
        
        n_vectors = len(codes)
        vectors = np.zeros((n_vectors, self.dim), dtype=np.float32)
        
        for m in range(self.M):
            start = m * self.sub_dim
            end = start + self.sub_dim
            
            # Look up centroids
            centroids = self.codebooks[m]  # (K, sub_dim)
            selected = centroids[codes[:, m]]  # (n_vectors, sub_dim)
            
            vectors[:, start:end] = selected
        
        return vectors
    
    def compressed_distance(
        self,
        query: np.ndarray,
        codes: np.ndarray
    ) -> np.ndarray:
        """
        Compute approximate distances efficiently.
        
        Uses Asymmetric Distance Computation (ADC):
        d(q, c) ≈ Σ d(q_m, C_m[q_m])
        
        Args:
            query: shape (dim,) or (n_queries, dim)
            codes: shape (n_codes, M)
        
        Returns:
            distances: shape (n_queries, n_codes)
        """
        import numpy as np
        
        if query.ndim == 1:
            query = query[np.newaxis, :]
        
        n_queries = len(query)
        n_codes = len(codes)
        
        # Split query into subvectors
        query_subvecs = np.array_split(query, self.M, axis=1)
        
        # Build distance lookup table for each query subvector
        # lookup[m][k] = distance from query_subvec[m] to centroid k
        distances = np.zeros((self.M, self.K))
        
        for m in range(self.M):
            q_m = query_subvecs[m][:, np.newaxis, :]  # (n_queries, 1, sub_dim)
            c_m = self.codebooks[m][np.newaxis, :, :]  # (1, K, sub_dim)
            
            # Distances: (n_queries, K)
            d = np.linalg.norm(q_m - c_m, axis=2)
            distances[m] = d.mean(axis=0)  # Average across query vectors if batch
        
        # Accumulate distances using codes
        result = np.zeros((n_queries, n_codes))
        
        for m in range(self.M):
            # codes[:, m] selects centroid index for subvector m
            result += distances[m][codes[:, m]].T
        
        return result
```

## Binary Quantization

### 1. Theory

```python
"""
Binary Quantization (BQ)

原理:
1. Map each value to 0 or 1 based on threshold (usually 0 or mean)
2. Store as bits instead of bytes
3. Distance = Hamming distance (fast XOR + POPCOUNT)

Ví dụ: 128-dim float32 → 128 bits = 16 bytes
Compression: 32x (128 * 4 bytes → 16 bytes)

Distance computation:
- Original: 128 multiplications + 127 additions (float32)
- Binary: 128 XOR + POPCOUNT (very fast, often hardware-accelerated)

Trade-off:
- Severe information loss
- Good for very high dimensions
- Fast but lower accuracy
"""
```

### 2. Implementation

```python
class BinaryQuantizer:
    """
    Binary quantization for vectors.
    """
    
    def __init__(self, threshold_type="sign"):
        """
        Args:
            threshold_type: 'sign', 'mean', 'median', or 'random'
        """
        self.threshold_type = threshold_type
        self.thresholds = None
    
    def fit(self, vectors: np.ndarray):
        """
        Compute thresholds for binarization.
        """
        if self.threshold_type == "sign":
            self.thresholds = np.zeros(vectors.shape[1])
        elif self.threshold_type == "mean":
            self.thresholds = vectors.mean(axis=0)
        elif self.threshold_type == "median":
            self.thresholds = np.median(vectors, axis=0)
        elif self.threshold_type == "random":
            # For LSH-like behavior
            self.thresholds = np.random.randn(vectors.shape[1])
        
        return self
    
    def binarize(self, vectors: np.ndarray) -> np.ndarray:
        """
        Convert vectors to binary codes.
        
        Returns:
            bits: shape (n_vectors, dim), dtype uint8 (0 or 1)
        """
        return (vectors > self.thresholds).astype(np.uint8)
    
    def debinarize(self, bits: np.ndarray) -> np.ndarray:
        """
        Convert binary codes back to vectors (approximate).
        
        Returns centroids for each binary vector.
        """
        # For sign quantization, this returns the threshold as centroid
        # This is a crude approximation
        return bits.astype(np.float32) + self.thresholds
    
    def pack_bits(self, bits: np.ndarray) -> np.ndarray:
        """
        Pack bits into bytes for efficient storage.
        
        Input: (n_vectors, dim) uint8
        Output: (n_vectors, dim//8) uint8
        """
        import numpy as np
        
        n_vectors, dim = bits.shape
        packed_dim = (dim + 7) // 8
        
        # Pad to byte boundary
        if dim % 8 != 0:
            pad_width = 8 - (dim % 8)
            bits = np.pad(bits, ((0, 0), (0, pad_width)))
        
        # Pack
        packed = bits.reshape(n_vectors, packed_dim, 8)
        result = np.zeros((n_vectors, packed_dim), dtype=np.uint8)
        
        for i in range(8):
            result |= (packed[:, :, i] << i)
        
        return result
    
    def unpack_bits(self, packed: np.ndarray, dim: int) -> np.ndarray:
        """
        Unpack bytes back to bits.
        """
        import numpy as np
        
        n_vectors, packed_dim = packed.shape
        unpacked = np.zeros((n_vectors, dim), dtype=np.uint8)
        
        for i in range(8):
            unpacked |= ((packed >> i) & 1)
        
        return unpacked[:, :dim]
    
    def hamming_distance(self, a: np.ndarray, b: np.ndarray) -> int:
        """
        Compute Hamming distance between two binary vectors.
        """
        xor = np.bitwise_xor(a, b)
        return bin(xor).count('1')


class OptimizedBinaryIndex:
    """
    Fast vector index using binary quantization.
    """
    
    def __init__(self, quantizer: BinaryQuantizer):
        self.quantizer = quantizer
        self.vectors = {}
        self.binary_codes = {}
        self.packed_codes = {}
    
    def add(self, ids: List[str], vectors: np.ndarray):
        """
        Add vectors to index.
        """
        bits = self.quantizer.binarize(vectors)
        
        for vec_id, bit_vector, packed in zip(ids, bits, self.quantizer.pack_bits(bits)):
            self.vectors[vec_id] = vectors
            self.binary_codes[vec_id] = bit_vector
            self.packed_codes[vec_id] = packed
    
    def search(
        self,
        query: np.ndarray,
        k: int = 10,
        max_hamming: int = None
    ) -> List[Tuple[str, int]]:
        """
        Search using Hamming distance.
        """
        query_bits = self.quantizer.binarize(query.reshape(1, -1))[0]
        query_packed = self.quantizer.pack_bits(
            query_bits.reshape(1, -1)
        )[0]
        
        results = []
        
        for vec_id, packed in self.packed_codes.items():
            dist = self._hamming_distance(query_packed, packed)
            
            if max_hamming is None or dist <= max_hamming:
                results.append((vec_id, dist))
        
        results.sort(key=lambda x: x[1])
        return results[:k]
    
    def _hamming_distance(self, a: np.ndarray, b: np.ndarray) -> int:
        """
        Fast Hamming distance using numpy.
        """
        xor = np.bitwise_xor(a, b)
        return int(np.unpackbits(xor).sum())
```

## Quality vs Speed Trade-offs

### 1. Benchmark Framework

```python
def benchmark_quantization_methods(
    vectors: np.ndarray,
    queries: np.ndarray,
    ground_truth: np.ndarray
) -> dict:
    """
    Benchmark different quantization methods.
    """
    import numpy as np
    import time
    
    results = {}
    k = 10
    
    # Original (baseline)
    print("Benchmarking Original vectors...")
    start = time.time()
    orig_distances = compute_distances(queries, vectors)
    orig_time = time.time() - start
    orig_recall = compute_recall(orig_distances, ground_truth, k)
    
    results["original"] = {
        "memory_bytes": vectors.nbytes,
        "time_ms": orig_time * 1000,
        "recall": orig_recall
    }
    
    # Scalar Quantization Int8
    print("Benchmarking SQ Int8...")
    sq = ScalarQuantizer(bits=8)
    sq.fit(vectors)
    sq_codes = sq.quantize(vectors)
    sq_vectors = sq.dequantize(sq_codes)
    
    start = time.time()
    sq_distances = compute_distances(queries, sq_vectors)
    sq_time = time.time() - start
    sq_recall = compute_recall(sq_distances, ground_truth, k)
    
    results["sq_int8"] = {
        "memory_bytes": sq_codes.nbytes,
        "compression": vectors.nbytes / sq_codes.nbytes,
        "time_ms": sq_time * 1000,
        "recall": sq_recall
    }
    
    # Product Quantization
    print("Benchmarking PQ...")
    pq = ProductQuantizer(dim=vectors.shape[1], M=8, n_bits=8)
    pq.fit(vectors)
    pq_codes = pq.encode(vectors)
    
    start = time.time()
    pq_distances = np.array([
        pq.compressed_distance(q, pq_codes).flatten()
        for q in queries
    ])
    pq_time = time.time() - start
    pq_recall = compute_recall(pq_distances, ground_truth, k)
    
    results["pq_8_8"] = {
        "memory_bytes": pq_codes.nbytes,
        "compression": vectors.nbytes / pq_codes.nbytes,
        "time_ms": pq_time * 1000,
        "recall": pq_recall
    }
    
    # Binary Quantization
    print("Benchmarking Binary...")
    bq = BinaryQuantizer(threshold_type="mean")
    bq.fit(vectors)
    bq_bits = bq.binarize(vectors)
    
    start = time.time()
    bq_distances = np.array([
        compute_hamming_distances(q.reshape(1, -1), bq_bits)
        for q in queries
    ])
    bq_time = time.time() - start
    bq_recall = compute_recall(bq_distances, ground_truth, k)
    
    packed_bits = bq.pack_bits(bq_bits)
    results["binary"] = {
        "memory_bytes": packed_bits.nbytes,
        "compression": vectors.nbytes / packed_bits.nbytes,
        "time_ms": bq_time * 1000,
        "recall": bq_recall
    }
    
    return results


def compute_distances(queries: np.ndarray, vectors: np.ndarray) -> np.ndarray:
    """Compute cosine distances."""
    import numpy as np
    
    # Normalize
    q_norm = queries / (np.linalg.norm(queries, axis=1, keepdims=True) + 1e-10)
    v_norm = vectors / (np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-10)
    
    return 1 - np.dot(q_norm, v_norm.T)


def compute_hamming_distances(query: np.ndarray, codes: np.ndarray) -> np.ndarray:
    """Compute Hamming distances."""
    import numpy as np
    
    query_bits = (query > 0).astype(np.uint8)
    distances = np.sum(query_bits != codes, axis=1)
    
    return distances


def compute_recall(
    distances: np.ndarray,
    ground_truth: np.ndarray,
    k: int
) -> float:
    """Compute recall@k."""
    import numpy as np
    
    # Get top-k indices from distances
    if distances.ndim == 1:
        top_k_indices = np.argsort(distances)[:k]
    else:
        top_k_indices = np.argsort(distances, axis=1)[:, :k]
    
    # Get ground truth top-k
    if ground_truth.ndim == 1:
        gt_top_k = ground_truth[:k]
    else:
        gt_top_k = ground_truth[:, :k]
    
    # Calculate recall
    if ground_truth.ndim == 1:
        hits = len(set(top_k_indices) & set(gt_top_k))
    else:
        hits = 0
        for pred, truth in zip(top_k_indices, gt_top_k):
            hits += len(set(pred) & set(truth))
    
    return hits / (len(ground_truth) * k)
```

### 2. Quality Degradation Analysis

```python
def analyze_quality_degradation(
    vectors: np.ndarray,
    methods: List[str] = ["sq_int8", "pq_8_8", "binary"]
) -> dict:
    """
    Analyze how quantization affects vector quality.
    """
    import numpy as np
    
    results = {}
    
    # Original distances (baseline)
    orig_norms = np.linalg.norm(vectors, axis=1)
    
    for method in methods:
        if method == "sq_int8":
            quantizer = ScalarQuantizer(bits=8)
            quantizer.fit(vectors)
            codes = quantizer.quantize(vectors)
            reconstructed = quantizer.dequantize(codes)
        
        elif method == "pq_8_8":
            quantizer = ProductQuantizer(dim=vectors.shape[1], M=8, n_bits=8)
            quantizer.fit(vectors)
            codes = quantizer.encode(vectors)
            reconstructed = quantizer.decode(codes)
        
        elif method == "binary":
            quantizer = BinaryQuantizer(threshold_type="mean")
            quantizer.fit(vectors)
            codes = quantizer.binarize(vectors)
            reconstructed = quantizer.dequantize(codes)
        
        # Calculate reconstruction error
        mse = np.mean((vectors - reconstructed) ** 2)
        
        # Calculate per-vector error
        vector_errors = np.mean((vectors - reconstructed) ** 2, axis=1)
        
        results[method] = {
            "mse": mse,
            "rmse": np.sqrt(mse),
            "mean_vector_error": np.mean(vector_errors),
            "p95_vector_error": np.percentile(vector_errors, 95),
            "worst_case_error": np.max(vector_errors)
        }
    
    return results
```

## Best Practices

### 1. Method Selection Guide

```python
# Quantization method selection guide

METHOD_SELECTION = {
    "scalar_quantization": {
        "best_for": [
            "Low-dimensional vectors (< 128 dim)",
            "When you need exact reconstruction",
            "Simple implementation"
        ],
        "compression": "2-4x",
        "accuracy_loss": "1-5%",
        "speed_gain": "2-4x"
    },
    "product_quantization": {
        "best_for": [
            "High-dimensional vectors (128-2048 dim)",
            "Balanced accuracy and compression",
            "Production vector search"
        ],
        "compression": "4-32x",
        "accuracy_loss": "2-10%",
        "speed_gain": "4-16x"
    },
    "binary_quantization": {
        "best_for": [
            "Very high dimensions (> 1000)",
            "Maximum compression",
            "Fast approximate search"
        ],
        "compression": "32x+",
        "accuracy_loss": "10-30%",
        "speed_gain": "16-64x"
    }
}
```

### 2. Optimization Tips

```python
OPTIMIZATION_TIPS = {
    "training_data": """
        Use representative data for training quantizers.
        At least 10x more training vectors than centroids.
    """,
    
    "normalization": """
        Normalize vectors before quantization for better results.
        Especially important for binary quantization.
    """,
    
    "codebook_size": """
        Larger codebooks = better accuracy but more memory.
        Trade-off: K=256 usually good balance for int8.
    """,
    
    "subvector_count": """
        More subvectors = better accuracy but slower.
        Rule of thumb: dim / M ≈ 32-64.
    """,
    
    "residual_quantization": """
        For PQ, quantize residuals after first pass.
        Can improve accuracy significantly.
    """
}
```

## Examples

### Example 1: Production Quantized Index

```python
class QuantizedVectorIndex:
    """
    Production-ready quantized vector index.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.method = config.get("method", "pq")
        
        if self.method == "pq":
            self.quantizer = ProductQuantizer(
                dim=config["dim"],
                M=config.get("M", 8),
                n_bits=config.get("n_bits", 8)
            )
        elif self.method == "sq":
            self.quantizer = ScalarQuantizer(bits=config.get("bits", 8))
        elif self.method == "binary":
            self.quantizer = BinaryQuantizer(
                threshold_type=config.get("threshold", "mean")
            )
        
        self.codes = None
        self.vectors = {}  # Optional: store originals for refinement
    
    def build(
        self,
        vectors: np.ndarray,
        ids: List[str],
        train_vectors: np.ndarray = None
    ):
        """
        Build quantized index.
        """
        # Train quantizer
        training_data = train_vectors if train_vectors is not None else vectors
        print(f"Training {self.method} on {len(training_data)} vectors...")
        self.quantizer.fit(training_data)
        
        # Encode all vectors
        print("Encoding vectors...")
        self.codes = self.quantizer.encode(vectors)
        
        # Store ID mapping
        self.id_to_idx = {id_: i for i, id_ in enumerate(ids)}
        self.idx_to_id = {i: id_ for i, id_ in enumerate(ids)}
        
        return self
    
    def search(
        self,
        query: np.ndarray,
        k: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Search for nearest neighbors.
        """
        if self.method == "pq":
            distances = self.quantizer.compressed_distance(query, self.codes)
            top_k = np.argsort(distances.flatten())[:k]
            top_k_distances = distances.flatten()[top_k]
        
        else:
            # Reconstruct and compute exact distances
            reconstructed = self.quantizer.decode(self.codes)
            
            # Compute distances
            similarities = np.dot(query, reconstructed.T).flatten()
            top_k = np.argsort(similarities)[::-1][:k]
            top_k_distances = similarities[top_k]
        
        # Map to IDs
        results = [
            (self.idx_to_id[idx], float(dist))
            for idx, dist in zip(top_k, top_k_distances)
        ]
        
        return results
    
    def add(self, vector: np.ndarray, id_: str):
        """Add new vector to index."""
        code = self.quantizer.encode(vector.reshape(1, -1))[0]
        
        if self.codes is None:
            self.codes = code.reshape(1, -1)
            idx = 0
        else:
            self.codes = np.vstack([self.codes, code])
            idx = len(self.codes) - 1
        
        self.id_to_idx[id_] = idx
        self.idx_to_id[idx] = id_
        
        return self
    
    def save(self, path: str):
        """Save quantized index."""
        import pickle
        import numpy as np
        
        with open(path, 'wb') as f:
            pickle.dump({
                "config": self.config,
                "codes": self.codes,
                "id_to_idx": self.id_to_idx,
                "idx_to_id": self.idx_to_id,
                "quantizer": self.quantizer
            }, f)
        
        return self
    
    @classmethod
    def load(cls, path: str) -> "QuantizedVectorIndex":
        """Load quantized index."""
        import pickle
        
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        index = cls(data["config"])
        index.codes = data["codes"]
        index.id_to_idx = data["id_to_idx"]
        index.idx_to_id = data["idx_to_id"]
        index.quantizer = data["quantizer"]
        
        return index
```

### Example 2: Tiered Quantization

```python
class TieredQuantizedIndex:
    """
    Tiered storage: hot (binary) + warm (PQ) + cold (compressed).
    """
    
    def __init__(self):
        self.binary_index = None  # Fast, low accuracy
        self.pq_index = None       # Medium speed/accuracy
        self.full_index = None     # Slow, exact
    
    def build(
        self,
        vectors: np.ndarray,
        ids: List[str],
        binary_thresh: int = 100,  # Top 100 candidates
        pq_thresh: int = 1000      # Top 1000 candidates
    ):
        """
        Build tiered index.
        """
        # Full precision for all
        self.full_index = vectors
        
        # PQ for medium recall
        self.pq_index = ProductQuantizer(dim=vectors.shape[1], M=8)
        self.pq_index.fit(vectors)
        self.pq_codes = self.pq_index.encode(vectors)
        
        # Binary for fast filtering
        self.binary_index = BinaryQuantizer(threshold_type="mean")
        self.binary_index.fit(vectors)
        self.binary_codes = self.binary_index.binarize(vectors)
    
    def search(
        self,
        query: np.ndarray,
        recall_target: float = 0.95,
        max_results: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Search with tiered approach.
        """
        import numpy as np
        
        if recall_target >= 0.99:
            # Use exact search
            return self._exact_search(query, max_results)
        
        elif recall_target >= 0.95:
            # Use PQ
            return self._pq_search(query, max_results)
        
        else:
            # Use binary for initial filtering
            return self._binary_search(query, max_results)
    
    def _exact_search(self, query, k):
        """Exact search on full precision."""
        import numpy as np
        
        similarities = np.dot(query, self.full_index.T)
        top_k = np.argsort(similarities)[::-1][:k]
        
        return [(f"vec_{i}", float(similarities[i])) for i in top_k]
    
    def _pq_search(self, query, k):
        """PQ-based search."""
        distances = self.pq_index.compressed_distance(query, self.pq_codes)
        top_k = np.argsort(distances.flatten())[:k]
        
        return [(f"vec_{i}", float(1 / (1 + distances.flatten()[i]))) for i in top_k]
    
    def _binary_search(self, query, k):
        """Binary search for fast results."""
        query_bits = self.binary_index.binarize(query.reshape(1, -1))[0]
        distances = np.sum(query_bits != self.binary_codes, axis=1)
        top_k = np.argsort(distances)[:k]
        
        return [(f"vec_{i}", float(1 / (1 + distances[i]))) for i in top_k]
```

## References

1. **Product Quantization Paper**: https://arxiv.org/abs/1510.00149
2. **Optimized Product Quantization**: https://arxiv.org/abs/1310.1534
3. **Cursor Enterprise Framework - Vector Search Rules**: `.cursor/rules/vector-search.mdc`
