---
title: "Vector Database Comparison"
description: "So sánh chi tiết các vector databases: Pinecone, Weaviate, Qdrant, Chroma, pgvector về features, cost và use case fit"
tags: ["vector-db", "pinecone", "weaviate", "qdrant", "chroma", "pgvector", "comparison"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Vector Database Comparison

## Tổng Quan

Việc lựa chọn đúng vector database là quyết định kiến trúc quan trọng, ảnh hưởng đến performance, scalability, và total cost of ownership của hệ thống. Mỗi vector database có những strengths và weaknesses khác nhau, phù hợp với các use cases khác nhau.

Trong thị trường hiện tại, có nhiều options từ fully-managed cloud services (Pinecone) đến self-hosted solutions (Qdrant, Weaviate) và extensions cho existing databases (pgvector, Chroma).

Việc hiểu rõ differences giữa các solutions sẽ giúp architect đưa ra quyết định phù hợp với requirements cụ thể của dự án.

## Mục Đích

Tài liệu này nhằm cung cấp comprehensive comparison giữa các vector databases phổ biến:

Đầu tiên, chúng ta sẽ so sánh feature sets của từng database.

Thứ hai, tài liệu phân tích chi phí và pricing models.

Thứ ba, chúng ta sẽ đề cập đến use case recommendations.

Cuối cùng, tài liệu cung cấp migration considerations và best practices.

## Feature Comparison

### 1. Feature Matrix

| Feature | Pinecone | Weaviate | Qdrant | Chroma | pgvector |
|---------|----------|----------|--------|--------|----------|
| **Deployment** | | | | | |
| Cloud-native | ✓ | ✓ | ✓ | ✓ | ✓ |
| Self-hosted | ✓ | ✓ | ✓ | ✓ | ✓ |
| Hybrid Search | ✓ | ✓ | ✓ | Limited | ✓ |
| Metadata Filtering | ✓ | ✓ | ✓ | ✓ | ✓ |
| Multi-tenancy | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Indexing** | | | | | |
| HNSW | ✓ | ✓ | ✓ | ✓ | ✓ |
| IVF/IVFFlat | ✓ | ✓ | ✓ | ✓ | ✓ |
| PQ/SQ | ✓ | ✓ | ✓ | Limited | ✓ |
| **Data Types** | | | | | |
| Text | ✓ | ✓ | ✓ | ✓ | ✓ |
| Images | ✓ | ✓ | ✓ | ✓ | ✓ |
| Multimodal | ✓ | ✓ | Limited | ✓ | ✓ |
| **Operations** | | | | | |
| ACID Transactions | Limited | ✓ | ✓ | Limited | ✓ |
| Backup/Restore | ✓ | ✓ | ✓ | Limited | ✓ |
| API | REST, gRPC | REST, GraphQL | REST, gRPC | REST | SQL |

### 2. Detailed Feature Analysis

#### Pinecone

```python
# Pinecone Python Client
import pinecone

# Initialize
pinecone.init(api_key="your-api-key", environment="us-west1")

# Create index
pinecone.create_index(
    name="production-index",
    dimension=1536,
    metric="cosine",
    shards=1,
    pods=1
)

# Connect to index
index = pinecone.Index("production-index")

# Upsert vectors
index.upsert([
    ("vec1", [0.1] * 1536, {"category": "tech", "id": "123"}),
    ("vec2", [0.2] * 1536, {"category": "science", "id": "456"})
])

# Query
results = index.query(
    vector=[0.1] * 1536,
    top_k=10,
    filter={"category": {"$eq": "tech"}},
    include_metadata=True
)
```

#### Weaviate

```python
# Weaviate Python Client
import weaviate

# Initialize
client = weaviate.Client("http://localhost:8080")

# Create schema
schema = {
    "class": "Document",
    "vectorizer": "text2vec-transformers",
    "vectorIndexType": "hnsw",
    "vectorIndexConfig": {
        "efConstruction": 128,
        "ef": -1,
        "maxConnections": 64
    },
    "properties": [
        {"name": "title", "dataType": ["text"]},
        {"name": "content", "dataType": ["text"]},
        {"name": "category", "dataType": ["text"]}
    ]
}

client.schema.create_class(schema)

# Add objects
client.data_object.create(
    class_name="Document",
    data_object={
        "title": "Introduction to AI",
        "content": "...",
        "category": "technology"
    },
    vector=[0.1] * 1536
)

# Query with near text
result = client.query.get(
    "Document",
    ["title", "content", "category"]
).with_near_text({
    "concepts": ["artificial intelligence"]
}).with_limit(10).do()
```

#### Qdrant

```python
# Qdrant Python Client
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter

# Initialize
client = QdrantClient("localhost", port=6333)

# Create collection
client.recreate_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

# Upsert points
client.upsert(
    collection_name="documents",
    points=[
        PointStruct(
            id=1,
            vector=[0.1] * 1536,
            payload={"title": "Doc 1", "category": "tech"}
        )
    ]
)

# Search with filter
results = client.search(
    collection_name="documents",
    query_vector=[0.1] * 1536,
    query_filter=Filter(
        must=[
            {"key": "category", "match": {"value": "tech"}}
        ]
    ),
    limit=10
)
```

#### Chroma

```python
# Chroma Python Client
import chromadb
from chromadb.config import Settings

# Initialize
client = chromadb.Client(Settings(
    chroma_api_impl="rest",
    persist_directory="./chroma_db"
))

# Create collection
collection = client.create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)

# Add embeddings
collection.add(
    ids=["1", "2", "3"],
    embeddings=[[0.1] * 1536, [0.2] * 1536, [0.3] * 1536],
    metadatas=[{"category": "tech"}, {"category": "science"}, {"category": "tech"}],
    documents=["Doc 1 content", "Doc 2 content", "Doc 3 content"]
)

# Query
results = collection.query(
    query_embeddings=[[0.1] * 1536],
    n_results=10,
    where={"category": {"$eq": "tech"}}
)
```

#### pgvector

```sql
-- Enable extension
CREATE EXTENSION vector;

-- Create table with vector column
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500),
    content TEXT,
    embedding VECTOR(1536),
    category VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create HNSW index
CREATE INDEX ON documents 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 200);

-- Insert data
INSERT INTO documents (title, content, embedding, category)
VALUES (
    'Introduction to AI',
    'Content here...',
    '[0.1, 0.2, ...]::vector',
    'technology'
);

-- Query with filtering
SELECT 
    id, title,
    1 - (embedding <=> '[0.1, 0.2, ...]::vector') AS similarity
FROM documents
WHERE category = 'technology'
ORDER BY embedding <=> '[0.1, 0.2, ...]::vector'
LIMIT 10;
```

## Cost Analysis

### 1. Pricing Models Comparison

| Provider | Free Tier | Starter | Enterprise |
|----------|-----------|---------|------------|
| **Pinecone** | - | $70/1M vectors | Custom |
| **Weaviate** | Local only | $0.025/hour (cloud) | Custom |
| **Qdrant** | Local only | $0.025/hour | Custom |
| **Chroma** | Unlimited (self-hosted) | - | - |
| **pgvector** | Unlimited (self-hosted) | DB hosting ~$20/month | Custom |

### 2. Cost Breakdown by Scale

```
Cost Analysis (Monthly Estimates)
================================

Small Scale (100K vectors)
├── Pinecone Serverless: ~$25/month
├── Weaviate Cloud: ~$50/month
├── Qdrant Cloud: ~$50/month
├── Self-hosted (pgvector): ~$20-50/month (VPS)
└── Chroma (local): Free

Medium Scale (1M vectors)
├── Pinecone: ~$200/month
├── Weaviate Cloud: ~$300/month
├── Qdrant Cloud: ~$300/month
├── Self-hosted (pgvector): ~$50-100/month
└── Chroma (local): Free (but limited features)

Large Scale (10M vectors)
├── Pinecone: ~$1,000+/month
├── Weaviate Cloud: ~$1,500+/month
├── Qdrant Cloud: ~$1,500+/month
├── Self-hosted (pgvector): ~$200-500/month
└── Chroma: Not recommended at this scale
```

### 3. TCO (Total Cost of Ownership)

```python
def calculate_tco(
    vector_db: str,
    num_vectors: int,
    monthly_queries: int,
    team_size: int = 1
) -> dict:
    """
    Calculate TCO for different vector databases.
    """
    
    costs = {
        "pinecone": {
            "cloud": {
                "infrastructure": 0.40 * num_vectors / 1_000_000,  # Per million vectors
                "queries": 0.10 * monthly_queries / 1_000_000,
            },
            "ops_cost_per_month": team_size * 1000  # DevOps overhead
        },
        "qdrant": {
            "self_hosted": {
                "vm_cost": 100 + (num_vectors / 1_000_000) * 50,
                "backup": 20,
            },
            "ops_cost_per_month": team_size * 1500
        },
        "pgvector": {
            "self_hosted": {
                "db_cost": 50 + (num_vectors / 1_000_000) * 30,
                "backup": 10,
            },
            "ops_cost_per_month": team_size * 2000
        }
    }
    
    return costs.get(vector_db, {})
```

## Use Case Recommendations

### 1. Decision Matrix

```
Use Case Decision Guide
======================

┌─────────────────────────────────────────────────────────────┐
│                    NEED TO DECIDE?                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Do you need enterprise support?                              │
│  ├── Yes → Pinecone, Weaviate Enterprise                     │
│  └── No ↓                                                  │
│                                                              │
│  Do you have existing PostgreSQL?                           │
│  ├── Yes → pgvector                                         │
│  └── No ↓                                                   │
│                                                              │
│  What's your scale?                                          │
│  ├── <100K vectors → Chroma, pgvector                       │
│  ├── 100K - 10M → Qdrant, Weaviate, pgvector              │
│  └── >10M → Pinecone, Qdrant Cloud                          │
│                                                              │
│  Do you need hybrid search?                                  │
│  ├── Yes → Weaviate, Qdrant                                 │
│  └── No ↓                                                   │
│                                                              │
│  Self-hosted or Cloud?                                       │
│  ├── Self-hosted → Qdrant, pgvector, Weaviate               │
│  └── Cloud → Pinecone, Qdrant Cloud, Weaviate Cloud         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2. Specific Use Case Recommendations

#### RAG (Retrieval Augmented Generation)

```python
# RAG Use Case Recommendations

USE_CASE_RAG = {
    "small_scale": {
        "recommended": ["chroma", "pgvector"],
        "reason": "Simple setup, cost-effective for <100K docs",
        "example": "Prototypes, small applications"
    },
    "medium_scale": {
        "recommended": ["qdrant", "weaviate", "pgvector"],
        "reason": "Good balance of features and performance",
        "example": "Production RAG for startups"
    },
    "large_scale": {
        "recommended": ["pinecone", "qdrant_cloud"],
        "reason": "Managed service, high performance at scale",
        "example": "Enterprise RAG platforms"
    }
}
```

#### Semantic Search

```python
# Semantic Search Recommendations

USE_CASE_SEMANTIC_SEARCH = {
    "e-commerce": {
        "recommended": ["qdrant", "weaviate"],
        "features_needed": ["hybrid_search", "filters", "realtime"],
        "reason": "Good hybrid search for product discovery"
    },
    "document_search": {
        "recommended": ["weaviate", "pgvector"],
        "features_needed": ["text_processing", "hybrid_search"],
        "reason": "Strong text embedding support"
    },
    "image_search": {
        "recommended": ["weaviate", "qdrant"],
        "features_needed": ["multimodal", "filters"],
        "reason": "Built-in multimodal support"
    }
}
```

#### Recommendation Systems

```python
# Recommendation System Recommendations

USE_CASE_RECOMMENDATIONS = {
    "collaborative_filtering": {
        "recommended": ["pgvector", "qdrant"],
        "reason": "Efficient for user/item embeddings",
        "scale": "Any scale with proper indexing"
    },
    "content_based": {
        "recommended": ["pinecone", "qdrant"],
        "reason": "High throughput for real-time recommendations",
        "scale": "Medium to large"
    },
    "hybrid_recommendations": {
        "recommended": ["weaviate", "qdrant"],
        "reason": "Support for multiple embedding types",
        "scale": "Medium to large"
    }
}
```

## Performance Comparison

### 1. Benchmark Results (Typical)

```
Performance Benchmarks (10M vectors, 1536 dimensions)
====================================================

Metric              Pinecone    Qdrant    Weaviate    pgvector
------------------------------------------------------------------------
Query Latency (P99)   25ms       30ms       45ms        40ms
Index Build Time      45min      60min      90min       75min
Memory Usage         40GB        35GB       55GB        30GB
QPS (with filters)   2000       1800       1200        1500
Recall @ 10           0.95       0.94       0.93        0.93
```

### 2. Latency by Scale

```python
# Latency estimates by scale

LATENCY_ESTIMATES = {
    "100k_vectors": {
        "pinecone": {"p50": "5ms", "p99": "15ms"},
        "qdrant": {"p50": "8ms", "p99": "20ms"},
        "weaviate": {"p50": "10ms", "p99": "25ms"},
        "pgvector": {"p50": "10ms", "p99": "30ms"}
    },
    "1m_vectors": {
        "pinecone": {"p50": "15ms", "p99": "40ms"},
        "qdrant": {"p50": "20ms", "p99": "50ms"},
        "weaviate": {"p50": "25ms", "p99": "60ms"},
        "pgvector": {"p50": "25ms", "p99": "70ms"}
    },
    "10m_vectors": {
        "pinecone": {"p50": "30ms", "p99": "80ms"},
        "qdrant": {"p50": "40ms", "p99": "100ms"},
        "weaviate": {"p50": "50ms", "p99": "120ms"},
        "pgvector": {"p50": "50ms", "p99": "150ms"}
    }
}
```

## Migration Considerations

### 1. Migration Path

```python
# Migration considerations between databases

MIGRATION_PATHS = {
    "chroma_to_qdrant": {
        "difficulty": "medium",
        "steps": [
            "1. Export Chroma collection to JSON",
            "2. Transform to Qdrant format",
            "3. Create Qdrant collection",
            "4. Import vectors with payload",
            "5. Verify index and rebuild if needed"
        ]
    },
    "pgvector_to_qdrant": {
        "difficulty": "medium",
        "steps": [
            "1. Export from PostgreSQL to CSV",
            "2. Parse and transform vectors",
            "3. Create Qdrant collection",
            "4. Bulk import vectors",
            "5. Set up PostgreSQL sync if needed"
        ]
    },
    "pinecone_to_qdrant": {
        "difficulty": "easy",
        "steps": [
            "1. Export Pinecone data via API",
            "2. Use Qdrant migration tool",
            "3. Verify data integrity"
        ]
    }
}
```

### 2. Export/Import Scripts

```python
# Example: Export from Chroma, Import to Qdrant

def migrate_chroma_to_qdrant(
    chroma_client,
    qdrant_client,
    collection_name: str,
    qdrant_collection: str
):
    """
    Migrate from Chroma to Qdrant.
    """
    # Get Chroma collection
    collection = chroma_client.get_collection(collection_name)
    
    # Get all data
    data = collection.get(include=["embeddings", "metadatas", "documents"])
    
    # Create Qdrant collection
    qdrant_client.recreate_collection(
        collection_name=qdrant_collection,
        vectors_config=VectorParams(
            size=len(data["embeddings"][0]),
            distance=Distance.COSINE
        )
    )
    
    # Transform and import
    points = []
    for i, (embedding, metadata, doc) in enumerate(zip(
        data["embeddings"],
        data["metadatas"],
        data["documents"]
    )):
        points.append(PointStruct(
            id=i,
            vector=embedding,
            payload={
                "document": doc,
                **metadata
            }
        ))
        
        # Batch import
        if len(points) >= 1000:
            qdrant_client.upsert(
                collection_name=qdrant_collection,
                points=points
            )
            points = []
    
    # Import remaining
    if points:
        qdrant_client.upsert(
            collection_name=qdrant_collection,
            points=points
        )
    
    print(f"Migrated {len(data['ids'])} vectors")
```

## Best Practices

### 1. Selection Criteria

```python
def evaluate_vector_db(options: dict) -> dict:
    """
    Evaluate vector database options against criteria.
    """
    criteria = {
        "scalability": {"weight": 0.2, "options": {}},
        "performance": {"weight": 0.25, "options": {}},
        "ease_of_use": {"weight": 0.15, "options": {}},
        "cost": {"weight": 0.2, "options": {}},
        "support": {"weight": 0.1, "options": {}},
        "features": {"weight": 0.1, "options": {}}
    }
    
    scores = {}
    
    for db, weights in criteria.items():
        scores[db] = sum(
            weights["options"].get(criterion, 0) * criteria[criterion]["weight"]
            for criterion in criteria
        )
    
    return scores
```

### 2. Hybrid Approach

```python
# Using multiple vector databases strategically

class HybridVectorStrategy:
    """
    Use different vector databases for different purposes.
    """
    
    def __init__(self):
        # Fast semantic search
        self.pinecone = PineconeClient()
        
        # Complex queries with PostgreSQL
        self.pgvector = PGVectorClient()
        
        # Local development
        self.chroma = ChromaClient()
    
    def get_client(self, environment: str):
        """Get appropriate client based on environment."""
        if environment == "production":
            return self.pinecone
        elif environment == "staging":
            return self.pgvector
        else:
            return self.chroma
```

## Examples

### Example 1: Multi-Database Architecture

```python
class MultiDatabaseVectorStore:
    """
    Architecture using multiple vector databases for different needs.
    """
    
    def __init__(self, config: dict):
        # Primary: Pinecone for user-facing search
        self.primary = PineconeClient(config["pinecone"])
        
        # Secondary: pgvector for complex analytics
        self.analytics = PGVectorClient(config["pgvector"])
        
        # Cache: Qdrant for recent/frequent queries
        self.cache = QdrantClient(config["qdrant"])
        
        self.sync_enabled = config.get("sync_enabled", True)
    
    async def search(
        self,
        query_vector: List[float],
        use_cache: bool = True
    ) -> List[dict]:
        """
        Search with caching layer.
        """
        # Check cache first
        if use_cache:
            cached = await self.cache.search(query_vector, limit=20)
            if cached:
                return cached
        
        # Search primary
        results = await self.primary.search(query_vector, limit=100)
        
        # Update cache
        if use_cache:
            await self.cache.upsert(results[:20])
        
        return results
    
    async def sync_analytics(self):
        """
        Sync data to analytics database.
        """
        if not self.sync_enabled:
            return
        
        # Periodic sync from primary to analytics
        recent_data = await self.primary.get_recent(limit=10000)
        await self.analytics.upsert(recent_data)
```

### Example 2: Feature Comparison Dashboard

```python
def generate_comparison_dashboard() -> dict:
    """
    Generate feature comparison dashboard data.
    """
    
    features = {
        "Core Features": [
            "HNSW Indexing",
            "IVF Indexing",
            "Product Quantization",
            "Hybrid Search",
            "Metadata Filtering",
            "Multi-tenancy"
        ],
        "Deployment": [
            "Self-hosted",
            "Cloud Native",
            "Kubernetes Support",
            "Docker Support"
        ],
        "Data Management": [
            "ACID Transactions",
            "Point-in-time Recovery",
            "Change Data Capture",
            "Bulk Import/Export"
        ],
        "API & Integrations": [
            "REST API",
            "gRPC API",
            "Python SDK",
            "JavaScript SDK",
            "OpenAPI Spec"
        ]
    }
    
    matrix = {}
    databases = ["pinecone", "weaviate", "qdrant", "chroma", "pgvector"]
    
    feature_support = {
        "pinecone": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        "weaviate": [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "qdrant": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "chroma": [1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0],
        "pgvector": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }
    
    return {
        "features": features,
        "databases": databases,
        "support_matrix": feature_support
    }
```

### Example 3: Cost Optimization Strategy

```python
class VectorDBCostOptimizer:
    """
    Optimize vector database costs.
    """
    
    def __init__(self, primary_db, analytics_db):
        self.primary = primary_db
        self.analytics = analytics_db
    
    async def optimize_storage(
        self,
        data: List[dict],
        access_pattern: str
    ) -> dict:
        """
        Optimize storage based on access patterns.
        """
        hot_data = []  # Frequently accessed
        warm_data = []  # Sometimes accessed
        cold_data = []  # Rarely accessed
        
        # Analyze access patterns
        for item in data:
            access_count = item.get("access_count", 0)
            
            if access_count > 1000:
                hot_data.append(item)
            elif access_count > 100:
                warm_data.append(item)
            else:
                cold_data.append(item)
        
        # Store hot data in premium tier
        if hot_data:
            await self.primary.upsert(hot_data)
        
        # Store warm data in standard tier
        if warm_data:
            await self.analytics.upsert(warm_data)
        
        # Archive cold data
        # (Implementation depends on specific DB)
        
        return {
            "hot_vectors": len(hot_data),
            "warm_vectors": len(warm_data),
            "cold_vectors": len(cold_data),
            "estimated_savings": self._calculate_savings(hot_data, warm_data, cold_data)
        }
    
    def _calculate_savings(self, hot, warm, cold) -> float:
        """Calculate cost savings from tiering."""
        # Simplified calculation
        hot_cost = len(hot) * 0.40  # Per million
        warm_cost = len(warm) * 0.20
        cold_cost = len(cold) * 0.05
        
        all_hot_cost = (len(hot) + len(warm) + len(cold)) * 0.40
        
        return all_hot_cost - (hot_cost + warm_cost + cold_cost)
```

## References

1. **Pinecone Documentation**: https://docs.pinecone.io/
2. **Weaviate Documentation**: https://weaviate.io/developers/weaviate/
3. **Qdrant Documentation**: https://qdrant.tech/documentation/
4. **Chroma Documentation**: https://docs.trychroma.com/
5. **pgvector**: https://github.com/pgvector/pgvector
6. **Vector DB Benchmarks**: https://ann-benchmarks.com/
7. **Cursor Enterprise Framework - RAG Rules**: `.cursor/rules/vector-search.mdc`
