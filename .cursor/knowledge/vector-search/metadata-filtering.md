---
title: "Metadata Filtering"
description: "Hướng dẫn về metadata filtering: pre-filtering vs post-filtering, hybrid filtering, sparse metadata indices và filter accuracy impact"
tags: ["metadata-filtering", "pre-filtering", "post-filtering", "hybrid-filtering", "vector-search"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Metadata Filtering

## Tổng Quan

Metadata filtering là kỹ thuật quan trọng trong vector search, cho phép giới hạn kết quả dựa trên structured attributes thay vì chỉ dựa vào vector similarity. Trong thực tế, hầu hết applications đều cần kết hợp cả vector search và structured filtering để đạt được relevant results.

Ví dụ, trong e-commerce search, user có thể muốn tìm "similar products in category 'electronics' with price under $500". Điều này đòi hỏi filtering trên metadata (category, price) kết hợp với similarity search trên product embeddings.

Việc implement filtering efficiently là challenge vì nó phải được làm đúng cách để không compromise search performance hoặc recall.

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức toàn diện về metadata filtering:

Đầu tiên, chúng ta sẽ tìm hiểu pre-filtering vs post-filtering approaches.

Thứ hai, tài liệu hướng dẫn hybrid filtering strategies.

Thứ ba, chúng ta sẽ đề cập đến sparse metadata indices và optimization techniques.

Cuối cùng, tài liệu phân tích impact của filtering trên search accuracy.

## Key Concepts

### 1. Filtering Approaches Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   FILTERING STRATEGIES                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Pre-filtering              Post-filtering                       │
│  ┌──────────────┐          ┌──────────────┐                    │
│  │ Filter first │          │ Search first │                    │
│  │ Then search  │          │ Then filter │                    │
│  └──────┬───────┘          └──────┬───────┘                    │
│         │                         │                              │
│  ┌──────▼───────┐          ┌──────▼───────┐                    │
│  │ Smaller      │          │ Larger      │                    │
│  │ search space │          │ search space │                    │
│  └──────────────┘          └──────────────┘                    │
│                                                                  │
│  ┌──────────────────────────────────────────┐                   │
│  │            Hybrid Filtering               │                   │
│  │  ┌────────────────────────────────────┐ │                   │
│  │  │ 1. Approximate pre-filter         │ │                   │
│  │  │ 2. Vector search in filtered space │ │                   │
│  │  │ 3. Post-filter refinement         │ │                   │
│  │  └────────────────────────────────────┘ │                   │
│  └──────────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Filter Types

```python
# Common filter types

FILTER_TYPES = {
    "equality": {
        "operator": "==",
        "example": {"category": "electronics"},
        "sql": "category = 'electronics'"
    },
    "range": {
        "operator": "> < >= <=",
        "example": {"price": {"gte": 100, "lte": 500}},
        "sql": "price BETWEEN 100 AND 500"
    },
    "in": {
        "operator": "IN",
        "example": {"tags": {"$in": ["ai", "ml", "data"]}},
        "sql": "tags IN ('ai', 'ml', 'data')"
    },
    "not_in": {
        "operator": "NOT IN",
        "example": {"status": {"$nin": ["deleted", "archived"]}},
        "sql": "status NOT IN ('deleted', 'archived')"
    },
    "exists": {
        "operator": "EXISTS",
        "example": {"author": {"$exists": True}},
        "sql": "author IS NOT NULL"
    },
    "text_match": {
        "operator": "LIKE/ILIKE",
        "example": {"title": {"$contains": "machine"}},
        "sql": "title ILIKE '%machine%'"
    },
    "geo": {
        "operator": "GEO_WITHIN",
        "example": {"location": {"$near": {"lat": 40.7, "lng": -74.0, "radius": 10}}},
        "sql": "ST_DWithin(location, point, radius)"
    }
}
```

## Pre-filtering

### 1. Implementation

```python
# Pre-filtering: Apply filter before vector search

class PreFilterVectorStore:
    """
    Pre-filtering implementation.
    """
    
    def __init__(self, vector_index, metadata_index):
        self.vector_index = vector_index
        self.metadata_index = metadata_index  # PostgreSQL, Elasticsearch, etc.
    
    async def search(
        self,
        query_vector: List[float],
        filter: dict,
        limit: int = 10
    ):
        """
        Pre-filtering approach.
        
        Steps:
        1. Apply metadata filter first
        2. Search only within filtered results
        """
        # Step 1: Get filtered document IDs
        filtered_ids = await self.metadata_index.query(filter)
        
        if not filtered_ids:
            return []
        
        # Step 2: Search only in filtered space
        # This may require scanning filtered vectors
        results = await self.vector_index.search_in_ids(
            query_vector=query_vector,
            ids=filtered_ids,
            limit=limit
        )
        
        return results
```

### 2. PostgreSQL Pre-filtering

```sql
-- Pre-filtering in PostgreSQL

-- Create table with metadata and vector
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name VARCHAR(500),
    category VARCHAR(100),
    price DECIMAL(10,2),
    rating DECIMAL(2,1),
    embedding VECTOR(1536)
);

-- Create indexes
CREATE INDEX idx_products_category ON products (category);
CREATE INDEX idx_products_price ON products (price);
CREATE INDEX idx_products_embedding ON products USING hnsw (embedding vector_cosine_ops);

-- Pre-filter query
EXPLAIN ANALYZE
SELECT 
    id, name,
    1 - (embedding <=> $query_vector) AS similarity
FROM products
WHERE 
    category = 'electronics'
    AND price BETWEEN 100 AND 500
    AND rating >= 4.0
ORDER BY embedding <=> $query_vector
LIMIT 10;
```

### 3. Performance Considerations

```python
# Pre-filtering performance tips

PRE_FILTER_OPTIMIZATION = {
    # Use selective filters first
    "selective_first": """
        Apply the most selective filter first.
        Example: 'deleted = false' eliminates most documents.
    """,
    
    # Composite indexes
    "composite_indexes": """
        Create indexes on common filter combinations.
        Example: (category, status, created_at)
    """,
    
    # Partial indexes
    "partial_indexes": """
        Use partial indexes for common filter values.
        Example: WHERE status = 'active'
    """,
    
    # Filter order matters
    "filter_order": """
        Order filters by selectivity.
        Most selective (fewest matches) first.
    """
}
```

## Post-filtering

### 1. Implementation

```python
# Post-filtering: Search first, then filter

class PostFilterVectorStore:
    """
    Post-filtering implementation.
    """
    
    def __init__(self, vector_index):
        self.vector_index = vector_index
    
    async def search(
        self,
        query_vector: List[float],
        filter: dict,
        limit: int = 10,
        oversample: int = 5
    ):
        """
        Post-filtering approach.
        
        Steps:
        1. Search to get more results than needed
        2. Apply filter to results
        3. Return top-k after filtering
        """
        # Step 1: Oversearch to account for filtering
        initial_limit = limit * oversample
        
        results = await self.vector_index.search(
            query_vector=query_vector,
            limit=initial_limit
        )
        
        # Step 2: Apply filter
        filtered_results = [
            result for result in results
            if self._matches_filter(result, filter)
        ]
        
        # Step 3: Return top-k
        return filtered_results[:limit]
    
    def _matches_filter(self, result: dict, filter: dict) -> bool:
        """Check if result matches filter."""
        for field, condition in filter.items():
            value = result.get("metadata", {}).get(field)
            
            if isinstance(condition, dict):
                # Complex condition
                if "$eq" in condition and value != condition["$eq"]:
                    return False
                if "$in" in condition and value not in condition["$in"]:
                    return False
                if "$gte" in condition and (value is None or value < condition["$gte"]):
                    return False
                if "$lte" in condition and (value is None or value > condition["$lte"]):
                    return False
            else:
                # Simple equality
                if value != condition:
                    return False
        
        return True
```

### 2. Oversampling Calculation

```python
def calculate_oversample_factor(
    filter_selectivity: float,
    target_k: int,
    desired_recall: float = 0.95
) -> int:
    """
    Calculate oversample factor based on filter selectivity.
    
    Args:
        filter_selectivity: Expected fraction that passes filter (0-1)
        target_k: Desired number of final results
        desired_recall: How many filtered results to capture
    """
    # Calculate how many to retrieve before filtering
    # to get target_k after filtering
    
    base = target_k / filter_selectivity
    
    # Adjust for desired recall
    # Higher recall needs more oversampling
    oversample = base / desired_recall
    
    return int(math.ceil(oversample))

# Example calculations
EXAMPLES = {
    "low_selectivity": {  # 10% pass filter
        "filter_selectivity": 0.1,
        "target_k": 10,
        "desired_recall": 0.95,
        "oversample_factor": calculate_oversample_factor(0.1, 10, 0.95)
        # Result: ~105
    },
    "high_selectivity": {  # 80% pass filter
        "filter_selectivity": 0.8,
        "target_k": 10,
        "desired_recall": 0.95,
        "oversample_factor": calculate_oversample_factor(0.8, 10, 0.95)
        # Result: ~13
    }
}
```

## Hybrid Filtering

### 1. Multi-stage Approach

```python
class HybridFilterVectorStore:
    """
    Hybrid filtering with multiple stages.
    """
    
    def __init__(self, config):
        self.vector_index = config["vector_index"]
        self.filter_index = config["filter_index"]  # e.g., PostgreSQL
        self.cache = config.get("cache")
    
    async def search(
        self,
        query_vector: List[float],
        filter: dict,
        limit: int = 10
    ):
        """
        Hybrid filtering approach.
        
        Stages:
        1. Light pre-filter using index scan
        2. Vector search on filtered space
        3. Post-filter refinement
        """
        # Stage 1: Fast pre-filter
        candidate_ids = await self._fast_prefilter(filter)
        
        if not candidate_ids:
            return []
        
        # Stage 2: Vector search on candidates
        if len(candidate_ids) > 10000:
            # Too many candidates, use post-filtering instead
            return await self._postfilter_search(
                query_vector, filter, limit
            )
        
        results = await self.vector_index.search_in_ids(
            query_vector=query_vector,
            ids=candidate_ids,
            limit=limit * 2  # Small oversample
        )
        
        # Stage 3: Post-filter refinement
        final_results = self._apply_filter(results, filter)
        
        return final_results[:limit]
    
    async def _fast_prefilter(self, filter: dict) -> List[str]:
        """Fast pre-filtering using metadata index."""
        # Use cache if available
        cache_key = self._cache_key(filter)
        
        if self.cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return cached
        
        # Query filter index
        ids = await self.filter_index.query(filter)
        
        # Cache result
        if self.cache and len(ids) < 10000:
            await self.cache.set(cache_key, ids, ttl=300)
        
        return ids
    
    def _apply_filter(self, results: List[dict], filter: dict) -> List[dict]:
        """Apply post-filter to results."""
        return [
            r for r in results
            if self._matches_filter(r, filter)
        ]
```

### 2. Adaptive Strategy Selection

```python
class AdaptiveFilterStrategy:
    """
    Select filtering strategy based on query characteristics.
    """
    
    def __init__(self, index):
        self.index = index
        self.filter_stats = FilterStatistics()
    
    async def search(
        self,
        query_vector: List[float],
        filter: dict,
        limit: int = 10
    ):
        """Choose best filtering strategy dynamically."""
        
        # Analyze filter
        selectivity = await self.filter_stats.estimate_selectivity(filter)
        
        # Get index statistics
        total_docs = await self.index.get_doc_count()
        filtered_count = int(total_docs * selectivity)
        
        # Decision logic
        if selectivity < 0.01:
            # Very selective filter (< 1%)
            # Pre-filtering is best
            return await self._prefilter_search(
                query_vector, filter, limit
            )
        
        elif selectivity > 0.5:
            # Low selectivity (> 50%)
            # Post-filtering is fine
            return await self._postfilter_search(
                query_vector, filter, limit
            )
        
        else:
            # Medium selectivity
            # Use hybrid approach
            return await self._hybrid_search(
                query_vector, filter, limit
            )


class FilterStatistics:
    """
    Track filter selectivity statistics.
    """
    
    def __init__(self):
        self.selectivity_cache = {}
    
    async def estimate_selectivity(self, filter: dict) -> float:
        """Estimate filter selectivity based on historical data."""
        # This would use historical query data
        # to estimate how many documents pass the filter
        
        # Simplified: assume uniform distribution
        return 0.1  # 10% pass rate estimate
```

## Sparse Metadata Indices

### 1. Sparse Index Implementation

```python
class SparseMetadataIndex:
    """
    Efficient sparse metadata index for fast filtering.
    """
    
    def __init__(self):
        # Inverted index for term-based filters
        self.inverted_index = {}  # term -> set(doc_ids)
        
        # B-tree for range filters
        self.range_indexes = {}  # field -> sorted list of (value, doc_id)
        
        # Bloom filter for existence checks
        self.bloom_filters = {}  # field -> BloomFilter
    
    def add(self, doc_id: str, metadata: dict):
        """Add document metadata."""
        for field, value in metadata.items():
            # Update inverted index
            if field not in self.inverted_index:
                self.inverted_index[field] = defaultdict(set)
            
            if isinstance(value, (str, int, bool)):
                self.inverted_index[field][value].add(doc_id)
            
            elif isinstance(value, list):
                for item in value:
                    self.inverted_index[field][item].add(doc_id)
            
            # Update range index
            if isinstance(value, (int, float)):
                if field not in self.range_indexes:
                    self.range_indexes[field] = []
                self.range_indexes[field].append((value, doc_id))
    
    def query_equality(self, field: str, value) -> Set[str]:
        """Query by equality."""
        if field in self.inverted_index:
            return self.inverted_index[field].get(value, set())
        return set()
    
    def query_range(
        self,
        field: str,
        gte=None,
        lte=None,
        gt=None,
        lt=None
    ) -> Set[str]:
        """Query by range."""
        if field not in self.range_indexes:
            return set()
        
        results = set()
        sorted_values = self.range_indexes[field]
        
        # Binary search for bounds
        for value, doc_id in sorted_values:
            if gte is not None and value < gte:
                continue
            if lte is not None and value > lte:
                break  # Sorted, so can stop
            if gt is not None and value <= gt:
                continue
            if lt is not None and value >= lt:
                continue
            
            results.add(doc_id)
        
        return results
    
    def query_and(self, *queries) -> Set[str]:
        """AND multiple queries."""
        if not queries:
            return set()
        
        result = queries[0]
        for query in queries[1:]:
            result = result & query
        
        return result
    
    def query_or(self, *queries) -> Set[str]:
        """OR multiple queries."""
        result = set()
        for query in queries:
            result = result | query
        
        return result
```

### 2. Composite Filter Optimization

```python
class CompositeFilterOptimizer:
    """
    Optimize composite filters for better performance.
    """
    
    def __init__(self, metadata_index):
        self.index = metadata_index
    
    def optimize(self, filter: dict) -> dict:
        """
        Reorder and optimize filter conditions.
        """
        conditions = self._extract_conditions(filter)
        
        # Sort by selectivity (estimated)
        sorted_conditions = sorted(
            conditions,
            key=lambda c: self._estimate_selectivity(c),
            reverse=True  # Most selective first
        )
        
        return self._reconstruct_filter(sorted_conditions)
    
    def _extract_conditions(self, filter: dict) -> List[dict]:
        """Extract flat list of conditions."""
        conditions = []
        
        for field, condition in filter.items():
            if isinstance(condition, dict):
                for op, value in condition.items():
                    conditions.append({
                        "field": field,
                        "operator": op,
                        "value": value
                    })
            else:
                conditions.append({
                    "field": field,
                    "operator": "eq",
                    "value": condition
                })
        
        return conditions
    
    def _estimate_selectivity(self, condition: dict) -> float:
        """
        Estimate selectivity of a condition.
        Returns 0-1 where lower = more selective.
        """
        field = condition["field"]
        op = condition["operator"]
        value = condition["value"]
        
        # These would come from statistics
        field_cardinality = self._get_cardinality(field)
        
        if op == "eq":
            return 1.0 / field_cardinality
        elif op in ("gte", "gt"):
            return 0.5  # Rough estimate
        elif op in ("lte", "lt"):
            return 0.5
        elif op == "$in":
            return len(value) / field_cardinality
        else:
            return 0.1
    
    def _get_cardinality(self, field: str) -> float:
        """Get cardinality estimate for field."""
        # Would be calculated from index statistics
        cardinalities = {
            "category": 100,
            "status": 5,
            "price": 10000,
            "created_at": 1000000
        }
        return cardinalities.get(field, 1000)
```

## Filter Accuracy Impact

### 1. Recall Degradation Analysis

```python
def analyze_filter_impact(
    total_documents: int,
    filtered_documents: int,
    vector_search_recall: float,
    filter_selectivity: float
) -> dict:
    """
    Analyze how filtering affects overall recall.
    """
    
    # Expected documents after filter
    expected_filtered = total_documents * filter_selectivity
    
    # Effective search space reduction
    space_reduction = 1 - filter_selectivity
    
    # For pre-filtering: same recall as no-filter search
    # (searches all filtered documents)
    prefilter_recall = vector_search_recall
    
    # For post-filtering: recall degrades with oversampling
    # Assuming we oversample by factor K
    oversample_factor = 10
    effective_searches = min(
        total_documents * oversample_factor,
        total_documents
    )
    
    postfilter_recall = (
        min(expected_filtered, effective_searches) / expected_filtered
    ) * vector_search_recall
    
    return {
        "total_documents": total_documents,
        "expected_filtered": expected_filtered,
        "filter_selectivity": filter_selectivity,
        "prefilter_recall": prefilter_recall,
        "postfilter_recall": postfilter_recall,
        "recall_degradation": prefilter_recall - postfilter_recall
    }
```

### 2. Performance vs Recall Trade-off

```python
def compute_filter_tradeoff(
    filter_selectivity: float,
    vector_search_params: dict
) -> dict:
    """
    Compute performance vs recall trade-off for different strategies.
    """
    
    results = {
        "prefilter": {},
        "postfilter": {},
        "hybrid": {}
    }
    
    # Pre-filtering
    results["prefilter"] = {
        "recall": vector_search_params["base_recall"],
        "latency_ms": 100 / filter_selectivity,  # Increases as filter gets more selective
        "strategy": "filter_first"
    }
    
    # Post-filtering
    oversample = 1 / filter_selectivity if filter_selectivity > 0 else float("inf")
    results["postfilter"] = {
        "recall": vector_search_params["base_recall"] * min(1, 1/oversample),
        "latency_ms": vector_search_params["base_latency"] * min(1, oversample),
        "oversample_factor": oversample,
        "strategy": "search_first"
    }
    
    # Hybrid
    results["hybrid"] = {
        "recall": vector_search_params["base_recall"] * 0.98,  # Slight degradation
        "latency_ms": vector_search_params["base_latency"] * 1.2,
        "strategy": "adaptive"
    }
    
    return results
```

## Best Practices

### 1. Index Design

```sql
-- Recommended indexes for filtering

-- 1. B-tree indexes for equality and range queries
CREATE INDEX idx_products_category ON products (category);
CREATE INDEX idx_products_price ON products (price);
CREATE INDEX idx_products_rating ON products (rating DESC);
CREATE INDEX idx_products_created ON products (created_at DESC);

-- 2. Composite indexes for common filter combinations
CREATE INDEX idx_products_cat_price ON products (category, price);
CREATE INDEX idx_products_cat_status ON products (category, status);

-- 3. Partial indexes for active records
CREATE INDEX idx_products_active 
ON products (embedding vector_cosine_ops) 
WHERE status = 'active';

-- 4. GIN indexes for JSONB metadata
CREATE INDEX idx_products_metadata 
ON products USING gin (metadata jsonb_path_ops);

-- 5. Covering indexes to avoid table lookups
CREATE INDEX idx_products_covering 
ON products (category, price) 
INCLUDE (name, embedding);
```

### 2. Query Optimization

```python
# Query optimization tips

QUERY_OPTIMIZATION = {
    "avoid_or_in_filter": """
        OR conditions in filters can be slow.
        Use IN instead when possible.
        
        Bad: WHERE category = 'a' OR category = 'b'
        Good: WHERE category IN ('a', 'b')
    """,
    
    "use_range_over_multiple_eq": """
        Multiple equality checks = ORs.
        Range queries are more efficient.
        
        Bad: WHERE price = 100 OR price = 200 OR price = 300
        Good: WHERE price IN (100, 200, 300)
        Best: Use application-side lookup
    """,
    
    "combine_filters_early": """
        Combine multiple filters before querying vector index.
        Reduces the search space early.
    """,
    
    "cache_filter_results": """
        Cache filter results for frequently used filters.
        Example: 'active products', 'published posts'
    """,
    
    "monitor_selectivity": """
        Track filter selectivity over time.
        Adjust index strategy based on actual usage.
    """
}
```

### 3. Error Handling

```python
class FilterErrorHandler:
    """
    Handle filter-related errors gracefully.
    """
    
    async def search_safe(
        self,
        query_vector: List[float],
        filter: dict,
        limit: int = 10
    ):
        """Search with graceful degradation."""
        try:
            return await self.search(query_vector, filter, limit)
        
        except FilterTimeoutError:
            # Filter took too long, fall back to post-filtering
            logger.warning("Filter timeout, falling back to post-filtering")
            return await self._postfilter_search(
                query_vector, filter, limit
            )
        
        except EmptyResultError:
            # Filter returned no results
            logger.info("Filter returned empty results")
            return []
        
        except IndexNotFoundError:
            # Index doesn't exist, skip filter
            logger.warning("Filter index not found, skipping filter")
            return await self.vector_index.search(
                query_vector, limit
            )
```

## Examples

### Example 1: Complete Filtered Search Implementation

```python
class CompleteFilteredSearch:
    """
    Production-ready filtered vector search.
    """
    
    def __init__(self, config: dict):
        self.pg_client = config["pg_client"]
        self.vector_client = config["vector_client"]
        self.cache = config.get("cache")
        
        # Prepared statements
        self._prepare_statements()
    
    def _prepare_statements(self):
        """Prepare optimized SQL statements."""
        # Statement for simple equality filter
        self.filter_eq = """
            SELECT id FROM products WHERE {field} = $1
        """
        
        # Statement for range filter
        self.filter_range = """
            SELECT id FROM products 
            WHERE {field} >= $1 AND {field} <= $2
        """
        
        # Statement for composite filter
        self.filter_composite = """
            SELECT id FROM products
            WHERE category = $1
              AND price >= $2
              AND price <= $3
              AND status = $4
        """
    
    async def search(
        self,
        query_vector: List[float],
        filters: dict = None,
        limit: int = 10
    ) -> List[dict]:
        """
        Complete search with metadata filtering.
        """
        filters = filters or {}
        
        # Step 1: Build and execute filter query
        filtered_ids = await self._execute_filter(filters)
        
        if not filtered_ids:
            return []
        
        # Step 2: Vector search on filtered IDs
        results = await self._search_vectors(
            query_vector=query_vector,
            ids=filtered_ids,
            limit=limit
        )
        
        # Step 3: Apply post-filter (belt and suspenders)
        final_results = [
            r for r in results
            if self._verify_filter(r, filters)
        ]
        
        return final_results[:limit]
    
    async def _execute_filter(self, filters: dict) -> List[str]:
        """Execute filter and return matching IDs."""
        if not filters:
            # No filter, return all
            query = "SELECT id FROM products WHERE status = 'active'"
            return await self.pg_client.fetch(query)
        
        # Build filter query based on filter structure
        if len(filters) == 1:
            field, value = list(filters.items())[0]
            return await self._simple_filter(field, value)
        
        elif len(filters) <= 4:
            return await self._composite_filter(filters)
        
        else:
            return await self._dynamic_filter(filters)
    
    async def _simple_filter(self, field: str, value) -> List[str]:
        """Simple single-field filter."""
        # Use prepared statement
        query = self.filter_eq.format(field=field)
        rows = await self.pg_client.fetch(query, value)
        return [row["id"] for row in rows]
    
    async def _composite_filter(self, filters: dict) -> List[str]:
        """Composite filter with multiple fields."""
        # Build parameterized query
        conditions = []
        params = []
        
        for field, value in filters.items():
            if isinstance(value, dict):
                # Range condition
                if "$gte" in value:
                    conditions.append(f"{field} >= ${len(params) + 1}")
                    params.append(value["$gte"])
                if "$lte" in value:
                    conditions.append(f"{field} <= ${len(params) + 1}")
                    params.append(value["$lte"])
            else:
                conditions.append(f"{field} = ${len(params) + 1}")
                params.append(value)
        
        query = f"SELECT id FROM products WHERE {' AND '.join(conditions)}"
        rows = await self.pg_client.fetch(query, *params)
        return [row["id"] for row in rows]
    
    async def _search_vectors(
        self,
        query_vector: List[float],
        ids: List[str],
        limit: int
    ) -> List[dict]:
        """Search vectors within given IDs."""
        # In practice, this would use the vector DB's filter capability
        # Example with Pinecone:
        results = self.vector_client.query(
            vector=query_vector,
            filter={"id": {"$in": ids}},
            top_k=limit,
            include_metadata=True
        )
        return results["matches"]
    
    def _verify_filter(self, result: dict, filters: dict) -> bool:
        """Verify result matches filter (post-filter)."""
        metadata = result.get("metadata", {})
        
        for field, value in filters.items():
            result_value = metadata.get(field)
            
            if isinstance(value, dict):
                if "$eq" in value and result_value != value["$eq"]:
                    return False
                if "$gte" in value and (result_value is None or result_value < value["$gte"]):
                    return False
                if "$lte" in value and (result_value is None or result_value > value["$lte"]):
                    return False
            else:
                if result_value != value:
                    return False
        
        return True
```

### Example 2: Filter Metrics Dashboard

```python
class FilterMetricsDashboard:
    """
    Dashboard for monitoring filter performance.
    """
    
    def __init__(self, metrics_client):
        self.metrics = metrics_client
    
    async def record_search(
        self,
        filter: dict,
        filter_time_ms: float,
        result_count: int,
        recall_estimated: float
    ):
        """Record metrics for a filtered search."""
        # Record filter-specific metrics
        self.metrics.gauge(
            "filter.time_ms",
            filter_time_ms,
            tags={"filter_type": self._classify_filter(filter)}
        )
        
        self.metrics.gauge(
            "filter.result_count",
            result_count
        )
        
        self.metrics.gauge(
            "filter.estimated_recall",
            recall_estimated
        )
    
    def _classify_filter(self, filter: dict) -> str:
        """Classify filter type."""
        if not filter:
            return "none"
        
        if len(filter) == 1:
            return "simple"
        
        if len(filter) <= 4:
            return "composite"
        
        return "complex"
    
    async def get_filter_stats(self) -> dict:
        """Get filter statistics."""
        return {
            "avg_filter_time_ms": await self.metrics.get_average("filter.time_ms"),
            "p95_filter_time_ms": await self.metrics.get_percentile("filter.time_ms", 95),
            "avg_result_count": await self.metrics.get_average("filter.result_count"),
            "avg_recall": await self.metrics.get_average("filter.estimated_recall"),
            "filter_type_distribution": await self.metrics.get_distribution("filter_type")
        }
```

### Example 3: A/B Testing Filters

```python
class FilterABTester:
    """
    A/B test different filter strategies.
    """
    
    def __init__(self, experiment_tracker):
        self.tracker = experiment_tracker
    
    async def test_filter_strategy(
        self,
        query_vector: List[float],
        filter: dict,
        strategy_a: str,
        strategy_b: str
    ) -> dict:
        """
        Compare two filtering strategies.
        """
        # Test Strategy A
        results_a = await self._search_with_strategy(
            query_vector, filter, strategy_a
        )
        
        # Test Strategy B
        results_b = await self._search_with_strategy(
            query_vector, filter, strategy_b
        )
        
        # Record experiment
        self.tracker.record(
            experiment="filter_strategy",
            variant_a={"strategy": strategy_a, "results": results_a},
            variant_b={"strategy": strategy_b, "results": results_b}
        )
        
        return {
            "strategy_a": {
                "results": results_a,
                "latency_ms": results_a.get("latency", 0)
            },
            "strategy_b": {
                "results": results_b,
                "latency_ms": results_b.get("latency", 0)
            }
        }
    
    async def _search_with_strategy(
        self,
        query_vector: List[float],
        filter: dict,
        strategy: str
    ) -> dict:
        """Search using specific strategy."""
        start = time.time()
        
        if strategy == "prefilter":
            results = await self.prefilter_search(query_vector, filter)
        elif strategy == "postfilter":
            results = await self.postfilter_search(query_vector, filter)
        else:
            results = await self.hybrid_search(query_vector, filter)
        
        latency = (time.time() - start) * 1000
        
        return {
            "results": results,
            "latency": latency
        }
```

## References

1. **PostgreSQL Indexes**: https://www.postgresql.org/docs/current/indexes.html
2. **Vector Filtering**: https://docs.pinecone.io/docs/metadata-filtering
3. **Qdrant Filtering**: https://qdrant.tech/documentation/concepts/filtering/
4. **Cursor Enterprise Framework - Vector Search Rules**: `.cursor/rules/vector-search.mdc`
