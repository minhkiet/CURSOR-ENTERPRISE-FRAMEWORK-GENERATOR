---
title: "Application Patterns"
description: "Hướng dẫn về các application patterns với vector search: recommendation systems, semantic search, anomaly detection, deduplication, classification"
tags: ["application", "patterns", "recommendation", "semantic-search", "anomaly-detection", "deduplication", "classification"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Application Patterns

## Tổng Quan

Vector search không chỉ là một công cụ tìm kiếm đơn thuần, mà còn là nền tảng cho nhiều application patterns phức tạp trong các hệ thống hiện đại. Từ recommendation engines đến semantic search, từ anomaly detection đến classification, vector representations cho phép chúng ta giải quyết các bài toán business phức tạp một cách hiệu quả.

Key application areas bao gồm:

- **Recommendation Systems**: Đề xuất sản phẩm, nội dung, hoặc user interactions dựa trên similarity
- **Semantic Search**: Tìm kiếm theo ngữ nghĩa thay vì keyword matching
- **Anomaly Detection**: Phát hiện các mẫu bất thường trong dữ liệu
- **Deduplication**: Loại bỏ các bản ghi trùng lặp
- **Classification**: Phân loại items dựa trên vector similarity

Mỗi pattern có những đặc điểm riêng về data model, indexing strategy, và query patterns.

## Mục Đích

Tài liệu này nhằm cung cấp:

Đầu tiên, chúng ta sẽ tìm hiểu về cách thiết kế và implement các application patterns phổ biến.

Thứ hai, tài liệu cung cấp các best practices cho từng pattern cụ thể.

Thứ ba, chúng ta sẽ xem xét các trade-offs và optimization strategies.

Cuối cùng, tài liệu đề cập đến các troubleshooting strategies cho từng pattern.

## Key Concepts

### 1. Application Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    VECTOR APPLICATION PATTERNS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐     ┌──────────────────┐                 │
│  │  RECOMMENDATION  │     │   SEMANTIC       │                 │
│  │  SYSTEMS         │     │   SEARCH         │                 │
│  ├──────────────────┤     ├──────────────────┤                 │
│  │ - User vectors   │     │ - Document vec   │                 │
│  │ - Item vectors   │     │ - Query vec       │                 │
│  │ - Collaborative   │     │ - BM25 hybrid    │                 │
│  │ - Content-based   │     │ - Reranking      │                 │
│  └──────────────────┘     └──────────────────┘                 │
│                                                                  │
│  ┌──────────────────┐     ┌──────────────────┐                 │
│  │  ANOMALY         │     │   DEDUPLICATION  │                 │
│  │  DETECTION       │     ├──────────────────┤                 │
│  ├──────────────────┤     │ - Similarity     │                 │
│  │ - Distance-based │     │ - Clustering     │                 │
│  │ - Density-based  │     │ - Blocking       │                 │
│  │ - Isolation      │     │ - Graph-based    │                 │
│  └──────────────────┘     └──────────────────┘                 │
│                                                                  │
│  ┌──────────────────┐                                          │
│  │  CLASSIFICATION  │                                          │
│  ├──────────────────┤                                          │
│  │ - KNN classifier │                                          │
│  │ - Prototype-based │                                          │
│  │ - Ensemble        │                                          │
│  └──────────────────┘                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Pattern Selection Guide

```python
"""
Pattern selection guide based on use case requirements.
"""

PATTERN_SELECTION = {
    "recommendation": {
        "use_cases": [
            "Product recommendations",
            "Content personalization",
            "Friend suggestions",
            "Next-item prediction"
        ],
        "key_vectors": ["user", "item", "interaction"],
        "index_types": ["hnsw", "ivf"],
        "typical_latency": "< 50ms",
        "scale": "1M - 100M items"
    },
    
    "semantic_search": {
        "use_cases": [
            "Document search",
            "Question answering",
            "Code search",
            "Knowledge base queries"
        ],
        "key_vectors": ["document", "query", "passage"],
        "index_types": ["hnsw"],
        "typical_latency": "< 100ms",
        "scale": "100K - 10M documents"
    },
    
    "anomaly_detection": {
        "use_cases": [
            "Fraud detection",
            "Network intrusion",
            "System monitoring",
            "Quality control"
        ],
        "key_vectors": ["event", "behavior", "transaction"],
        "index_types": ["l2", "cosine"],
        "typical_latency": "< 10ms",
        "scale": "Real-time streaming"
    },
    
    "deduplication": {
        "use_cases": [
            "Record linkage",
            "Plagiarism detection",
            "Image dedup",
            "Content dedup"
        ],
        "key_vectors": ["record", "content", "signature"],
        "index_types": ["lsh", "hnsw"],
        "typical_latency": "Batch or near-real-time",
        "scale": "10K - 10M records"
    },
    
    "classification": {
        "use_cases": [
            "Text classification",
            "Image classification",
            "Fraud categories",
            "Content moderation"
        ],
        "key_vectors": ["sample", "class_centroid", "prototype"],
        "index_types": ["hnsw", "flat"],
        "typical_latency": "< 20ms",
        "scale": "Online or batch"
    }
}
```

## Recommendation Systems

### 1. User-Item Embedding

```python
class RecommendationSystem:
    """
    Vector-based recommendation system.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.user_vectors = VectorStore("user_vectors")
        self.item_vectors = VectorStore("item_vectors")
        self.user_item_matrix = {}  # user_id -> {item_id: rating}
    
    def add_user(self, user_id: str, features: dict):
        """Add or update user vector."""
        # Generate user embedding from features
        features_text = self._features_to_text(features)
        user_vector = self.embedding_model.encode(features_text)
        
        self.user_vectors.upsert(user_id, user_vector)
    
    def add_item(self, item_id: str, features: dict, category: str = None):
        """Add or update item vector."""
        features_text = self._features_to_text(features)
        item_vector = self.embedding_model.encode(features_text)
        
        metadata = {"category": category} if category else {}
        self.item_vectors.upsert(item_id, item_vector, metadata)
    
    def _features_to_text(self, features: dict) -> str:
        """Convert feature dict to text for embedding."""
        parts = []
        for key, value in features.items():
            if isinstance(value, list):
                parts.append(f"{key}: {', '.join(str(v) for v in value)}")
            else:
                parts.append(f"{key}: {value}")
        return " ".join(parts)
```

### 2. Collaborative Filtering

```python
class CollaborativeFiltering:
    """
    Collaborative filtering using vector similarity.
    """
    
    def __init__(self, interaction_store):
        self.interactions = interaction_store
        self.user_vectors = {}
        self.item_vectors = {}
    
    def build_user_vectors(self, min_interactions: int = 5):
        """Build user vectors from interaction history."""
        # Aggregate item interactions per user
        user_item_matrix = self.interactions.get_user_item_matrix()
        
        for user_id, items in user_item_matrix.items():
            if len(items) < min_interactions:
                continue
            
            # Weighted average of item vectors
            weighted_sum = np.zeros(self.vector_dim)
            weight_sum = 0
            
            for item_id, rating in items.items():
                if item_id in self.item_vectors:
                    # Weight by rating
                    weight = rating  # or use log(rating), etc.
                    weighted_sum += self.item_vectors[item_id] * weight
                    weight_sum += weight
            
            if weight_sum > 0:
                self.user_vectors[user_id] = weighted_sum / weight_sum
    
    def recommend_for_user(
        self,
        user_id: str,
        k: int = 10,
        exclude_seen: bool = True
    ) -> List[dict]:
        """Get recommendations for a user."""
        if user_id not in self.user_vectors:
            return self._cold_start_recommendations(k)
        
        query_vector = self.user_vectors[user_id]
        
        # Search for similar items
        results = self.item_index.search(query_vector, k * 2)
        
        # Filter and format results
        recommendations = []
        seen_items = self.interactions.get_user_items(user_id) if exclude_seen else set()
        
        for item_id, score in results:
            if item_id not in seen_items:
                recommendations.append({
                    "item_id": item_id,
                    "score": float(score),
                    "reason": "collaborative"
                })
                
                if len(recommendations) >= k:
                    break
        
        return recommendations
    
    def _cold_start_recommendations(self, k: int) -> List[dict]:
        """Handle cold start with popularity-based recommendations."""
        popular_items = self.interactions.get_most_popular(k)
        
        return [
            {"item_id": item_id, "score": 1.0, "reason": "popular"}
            for item_id in popular_items
        ]
```

### 3. Content-Based Recommendations

```python
class ContentBasedRecommender:
    """
    Content-based recommendation using item similarity.
    """
    
    def __init__(self, item_index, item_metadata):
        self.item_index = item_index
        self.item_metadata = item_metadata
    
    def recommend_similar_to(
        self,
        seed_item_id: str,
        k: int = 10,
        category_filter: str = None
    ) -> List[dict]:
        """Recommend items similar to a seed item."""
        seed_vector = self.item_index.get_vector(seed_item_id)
        
        # Search with category filter if specified
        if category_filter:
            results = self.item_index.search(
                seed_vector,
                k=k * 3,
                filter={"category": category_filter}
            )
        else:
            results = self.item_index.search(seed_vector, k * 3)
        
        return [
            {
                "item_id": item_id,
                "score": float(score),
                "metadata": self.item_metadata.get(item_id, {})
            }
            for item_id, score in results
            if item_id != seed_item_id
        ][:k]
    
    def recommend_for_user_profile(
        self,
        liked_item_ids: List[str],
        disliked_item_ids: List[str] = None,
        k: int = 10
    ) -> List[dict]:
        """Recommend based on user preference profile."""
        # Aggregate liked items (positive signal)
        positive_vectors = [
            self.item_index.get_vector(item_id)
            for item_id in liked_item_ids
            if item_id in self.item_index
        ]
        
        if not positive_vectors:
            return []
        
        # Average positive vectors
        profile_vector = np.mean(positive_vectors, axis=0)
        
        # Subtract disliked items (negative signal) if available
        if disliked_item_ids:
            negative_vectors = [
                self.item_index.get_vector(item_id)
                for item_id in disliked_item_ids
                if item_id in self.item_index
            ]
            
            if negative_vectors:
                profile_vector -= np.mean(negative_vectors, axis=0) * 0.5
        
        # Normalize profile vector
        profile_vector = profile_vector / np.linalg.norm(profile_vector)
        
        # Search with profile vector
        results = self.item_index.search(profile_vector, k * 2)
        
        # Filter out items user already rated
        all_rated = set(liked_item_ids) | (set(disliked_item_ids) if disliked_item_ids else set())
        
        return [
            {
                "item_id": item_id,
                "score": float(score)
            }
            for item_id, score in results
            if item_id not in all_rated
        ][:k]
```

### 4. Hybrid Recommendations

```python
class HybridRecommender:
    """
    Hybrid recommendation combining multiple strategies.
    """
    
    def __init__(self, config: dict):
        self.collaborative = CollaborativeFiltering(config["collab"])
        self.content_based = ContentBasedRecommender(config["content"])
        self.popular = PopularityBasedRecommender(config["popular"])
        
        # Weights for each strategy
        self.weights = config.get("weights", {
            "collaborative": 0.4,
            "content": 0.4,
            "popular": 0.2
        })
    
    def recommend(
        self,
        user_id: str,
        context: dict = None,
        k: int = 10
    ) -> List[dict]:
        """Generate hybrid recommendations."""
        candidates = []
        
        # Get candidates from each strategy
        if self._user_has_history(user_id):
            collab_results = self.collaborative.recommend_for_user(user_id, k * 3)
            candidates.extend(collab_results)
        
        # Content-based on recent interactions
        recent_items = self._get_recent_items(user_id, limit=5)
        for item_id in recent_items:
            content_results = self.content_based.recommend_similar_to(item_id, k)
            candidates.extend(content_results)
        
        # Popular items as fallback
        popular_results = self.popular.get_popular(k * 2)
        candidates.extend(popular_results)
        
        # Combine scores with Reciprocal Rank Fusion
        combined = self._reciprocal_rank_fusion(candidates)
        
        # Apply diversity bonus
        diversified = self._diversify_results(combined, k)
        
        return diversified
    
    def _reciprocal_rank_fusion(
        self,
        results: List[dict],
        k: int = 60
    ) -> List[dict]:
        """Combine results using RRF."""
        from collections import defaultdict
        
        ranks = defaultdict(list)
        
        # Assign ranks within each result list
        for i, result in enumerate(results):
            ranks[result["item_id"]].append(i + 1)
        
        # Calculate RRF score
        fused_scores = {}
        for item_id, rank_list in ranks.items():
            rrf_score = sum(1 / (k + rank) for rank in rank_list)
            fused_scores[item_id] = rrf_score
        
        # Sort by fused score
        sorted_items = sorted(
            fused_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {"item_id": item_id, "score": score}
            for item_id, score in sorted_items[:50]
        ]
    
    def _diversify_results(
        self,
        results: List[dict],
        k: int = 10,
        diversity_threshold: float = 0.7
    ) -> List[dict]:
        """Add diversity to results."""
        if len(results) <= k:
            return results
        
        selected = []
        selected_ids = set()
        
        for result in results:
            if len(selected) >= k:
                break
            
            item_id = result["item_id"]
            
            # Check diversity against selected items
            item_vector = self.content_based.item_index.get_vector(item_id)
            
            is_diverse = True
            for selected_id in selected_ids:
                selected_vector = self.content_based.item_index.get_vector(selected_id)
                
                similarity = np.dot(item_vector, selected_vector)
                if similarity > diversity_threshold:
                    is_diverse = False
                    break
            
            if is_diverse:
                selected.append(result)
                selected_ids.add(item_id)
        
        # Fill remaining slots if needed
        for result in results:
            if len(selected) >= k:
                break
            if result["item_id"] not in selected_ids:
                selected.append(result)
                selected_ids.add(result["item_id"])
        
        return selected
```

## Semantic Search

### 1. Document Indexing Pipeline

```python
class SemanticSearchIndex:
    """
    Semantic search index for documents.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.vector_store = VectorStore(config["vector_store"])
        self.chunker = self._create_chunker(config["chunking"])
        self.embedding_model = self._load_embedding_model(config["embedding"])
    
    def _create_chunker(self, config: dict) -> Chunker:
        """Create document chunker based on config."""
        chunking_type = config.get("type", "recursive")
        
        if chunking_type == "recursive":
            return RecursiveChunker(
                chunk_size=config.get("chunk_size", 512),
                overlap=config.get("overlap", 50)
            )
        elif chunking_type == "semantic":
            return SemanticChunker(
                embedding_model=self.embedding_model,
                threshold=config.get("similarity_threshold", 0.8)
            )
        else:
            return FixedSizeChunker(
                chunk_size=config.get("chunk_size", 512)
            )
    
    def index_document(
        self,
        doc_id: str,
        content: str,
        metadata: dict = None
    ):
        """Index a document."""
        # Chunk document
        chunks = self.chunker.chunk(content)
        
        # Embed chunks
        chunk_vectors = self.embedding_model.encode(chunks)
        
        # Store in vector store
        for i, (chunk, vector) in enumerate(zip(chunks, chunk_vectors)):
            chunk_id = f"{doc_id}:{i}"
            
            chunk_metadata = {
                "doc_id": doc_id,
                "chunk_index": i,
                "total_chunks": len(chunks),
                **(metadata or {})
            }
            
            self.vector_store.upsert(
                chunk_id,
                vector,
                metadata=chunk_metadata
            )
    
    def search(
        self,
        query: str,
        k: int = 10,
        filters: dict = None
    ) -> List[dict]:
        """Search for relevant chunks."""
        # Embed query
        query_vector = self.embedding_model.encode(query)
        
        # Search vector index
        results = self.vector_store.search(
            query_vector,
            k=k * 2,
            filter=filters
        )
        
        # Re-rank with cross-encoder if configured
        if self.config.get("rerank"):
            results = self._rerank_results(query, results, k)
        else:
            results = results[:k]
        
        return results
    
    def _rerank_results(
        self,
        query: str,
        results: List[dict],
        k: int
    ) -> List[dict]:
        """Re-rank results using cross-encoder."""
        cross_encoder = CrossEncoderReranker(self.config["rerank_model"])
        
        # Prepare query-document pairs
        pairs = [
            (query, result["text"])
            for result in results
        ]
        
        # Get reranking scores
        scores = cross_encoder.predict(pairs)
        
        # Sort by reranking score
        for result, score in zip(results, scores):
            result["rerank_score"] = float(score)
        
        results.sort(key=lambda x: x["rerank_score"], reverse=True)
        
        return results[:k]
```

### 2. Query Understanding

```python
class SemanticQueryProcessor:
    """
    Process and expand queries for semantic search.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.query_analyzer = QueryAnalyzer()
        self.expander = self._create_expander(config.get("expansion"))
        self.spell_checker = SpellChecker() if config.get("spell_check") else None
    
    def process_query(self, query: str) -> dict:
        """Process and expand a search query."""
        processed = {
            "original": query,
            "intent": None,
            "entities": [],
            "expanded_queries": [],
            "filters": {}
        }
        
        # Analyze query intent
        intent_result = self.query_analyzer.analyze(query)
        processed["intent"] = intent_result["intent"]
        processed["entities"] = intent_result.get("entities", [])
        
        # Apply spell correction
        if self.spell_checker:
            query = self.spell_checker.correct(query)
            processed["corrected"] = query
        
        # Expand query
        if self.expander:
            processed["expanded_queries"] = self.expander.expand(query)
        
        # Extract filters from query
        processed["filters"] = self._extract_filters(query)
        
        return processed
    
    def _create_expander(self, config: dict):
        """Create query expander based on config."""
        if not config:
            return None
        
        expansion_type = config.get("type", "embedding")
        
        if expansion_type == "embedding":
            return EmbeddingExpander(config["embedding_model"])
        elif expansion_type == "llm":
            return LLMExpander(config["llm"])
        elif expansion_type == "hyde":
            return HyDEExpander(config["hyde_model"])
        else:
            return None
    
    def _extract_filters(self, query: str) -> dict:
        """Extract structured filters from query."""
        filters = {}
        
        # Extract date ranges
        date_pattern = r'(?:from|since|between)\s+(\d{4}-\d{2}-\d{2})'
        date_match = re.search(date_pattern, query, re.IGNORECASE)
        if date_match:
            filters["date_from"] = date_match.group(1)
        
        # Extract category filters
        category_pattern = r'category:(\w+)'
        category_match = re.search(category_pattern, query, re.IGNORECASE)
        if category_match:
            filters["category"] = category_match.group(1)
        
        return filters
```

### 3. Search Result Enhancement

```python
class SearchResultEnhancer:
    """
    Enhance search results with additional context.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.summary_model = config.get("summary_model")
        self.qa_model = config.get("qa_model")
    
    def enhance_results(
        self,
        query: str,
        results: List[dict]
    ) -> List[dict]:
        """Enhance search results with summaries and QA."""
        enhanced = []
        
        for result in results:
            enhanced_result = result.copy()
            
            # Add snippet/summary if text is long
            if len(result.get("text", "")) > 300:
                enhanced_result["snippet"] = self._generate_snippet(
                    result["text"],
                    query
                )
            
            # Answer question from context if applicable
            if self.qa_model:
                answer = self._answer_from_context(
                    query,
                    result["text"]
                )
                if answer:
                    enhanced_result["answer"] = answer
            
            # Add related terms
            enhanced_result["related_terms"] = self._extract_related_terms(
                result["text"]
            )
            
            enhanced.append(enhanced_result)
        
        return enhanced
    
    def _generate_snippet(
        self,
        text: str,
        query: str,
        max_length: int = 200
    ) -> str:
        """Generate query-focused snippet."""
        # Find query terms in text
        query_terms = query.lower().split()
        
        sentences = text.split(".")
        best_sentence = sentences[0]
        best_score = 0
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            score = sum(
                1 for term in query_terms
                if term in sentence_lower
            )
            
            if score > best_score:
                best_score = score
                best_sentence = sentence
        
        # Truncate if needed
        if len(best_sentence) > max_length:
            best_sentence = best_sentence[:max_length] + "..."
        
        return best_sentence.strip()
    
    def _answer_from_context(
        self,
        question: str,
        context: str
    ) -> Optional[str]:
        """Extract answer from context for question."""
        if not self.qa_model:
            return None
        
        try:
            answer = self.qa_model.predict(
                question=question,
                context=context
            )
            return answer
        except:
            return None
    
    def _extract_related_terms(self, text: str, max_terms: int = 5) -> List[str]:
        """Extract related terms from text."""
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter stopwords
        stopwords = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "being"}
        words = [w for w in words if w not in stopwords and len(w) > 3]
        
        # Count frequency
        from collections import Counter
        word_freq = Counter(words)
        
        return [term for term, _ in word_freq.most_common(max_terms)]
```

## Anomaly Detection

### 1. Distance-Based Anomaly Detection

```python
class DistanceBasedAnomalyDetector:
    """
    Detect anomalies based on distance to nearest neighbors.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.reference_vectors = []
        self.threshold = config.get("threshold", 0.1)
        self.k = config.get("k", 5)
    
    def fit(self, normal_data: np.ndarray):
        """Fit detector on normal data."""
        self.reference_vectors = normal_data
    
    def detect(self, vector: np.ndarray) -> dict:
        """Detect if vector is anomalous."""
        # Calculate distances to k nearest neighbors in reference set
        distances = np.linalg.norm(
            self.reference_vectors - vector,
            axis=1
        )
        
        # Get k nearest distances
        k_nearest = np.sort(distances)[:self.k]
        
        # Anomaly score = mean distance to k nearest
        score = float(np.mean(k_nearest))
        
        return {
            "is_anomaly": score > self.threshold,
            "score": score,
            "threshold": self.threshold,
            "k_distances": k_nearest.tolist()
        }
    
    def detect_batch(self, vectors: np.ndarray) -> List[dict]:
        """Detect anomalies in batch."""
        results = []
        
        for vector in vectors:
            results.append(self.detect(vector))
        
        return results
```

### 2. Isolation Forest Style Detection

```python
class IsolationScoreDetector:
    """
    Isolation-style anomaly detection using vector search.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.tree_depth = config.get("tree_depth", 10)
        self.num_trees = config.get("num_trees", 100)
        self.trees = []
    
    def fit(self, vectors: np.ndarray):
        """Build isolation trees."""
        import random
        
        self.reference_vectors = vectors
        
        for _ in range(self.num_trees):
            # Random subsample
            sample_size = min(len(vectors), 256)
            indices = random.sample(range(len(vectors)), sample_size)
            sample = vectors[indices]
            
            # Build tree
            tree = self._build_tree(sample, depth=0)
            self.trees.append(tree)
    
    def _build_tree(self, vectors: np.ndarray, depth: int):
        """Recursively build isolation tree."""
        if depth >= self.tree_depth or len(vectors) <= 1:
            return {"leaf": len(vectors)}
        
        # Random hyperplane split
        dim = vectors.shape[1]
        split_dim = random.randint(0, dim - 1)
        
        min_val = vectors[:, split_dim].min()
        max_val = vectors[:, split_dim].max()
        
        if min_val == max_val:
            return {"leaf": len(vectors)}
        
        split_val = random.uniform(min_val, max_val)
        
        left_mask = vectors[:, split_dim] < split_val
        right_mask = ~left_mask
        
        return {
            "split_dim": split_dim,
            "split_val": split_val,
            "left": self._build_tree(vectors[left_mask], depth + 1),
            "right": self._build_tree(vectors[right_mask], depth + 1)
        }
    
    def _path_length(self, vector: np.ndarray, tree: dict, depth: int = 0) -> float:
        """Calculate path length in tree."""
        if "leaf" in tree:
            # Adjustment for small sample sizes
            c = 2 * (np.log(tree["leaf"] - 1) + 0.5772156649) if tree["leaf"] > 1 else 0
            return depth + c
        
        split_dim = tree["split_dim"]
        split_val = tree["split_val"]
        
        if vector[split_dim] < split_val:
            return self._path_length(vector, tree["left"], depth + 1)
        else:
            return self._path_length(vector, tree["right"], depth + 1)
    
    def score(self, vector: np.ndarray) -> float:
        """Calculate anomaly score."""
        path_lengths = []
        
        for tree in self.trees:
            path_len = self._path_length(vector, tree)
            path_lengths.append(path_len)
        
        # Average path length
        avg_path_len = np.mean(path_lengths)
        
        # Normalize using expected path length
        c = 2 * (np.log(len(self.reference_vectors) - 1) + 0.5772156649)
        
        # Anomaly score (shorter path = more anomalous)
        score = 2 ** (-avg_path_len / c)
        
        return float(score)
```

### 3. Streaming Anomaly Detection

```python
class StreamingAnomalyDetector:
    """
    Real-time anomaly detection for streaming data.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.window_size = config.get("window_size", 1000)
        self.recent_vectors = deque(maxlen=self.window_size)
        self.threshold_percentile = config.get("threshold_percentile", 95)
        self.baseline_stats = []
    
    def add_point(self, vector: np.ndarray, timestamp: datetime = None) -> dict:
        """Add point and check for anomaly."""
        self.recent_vectors.append(vector)
        
        # Need minimum points for comparison
        if len(self.recent_vectors) < 50:
            return {
                "is_anomaly": False,
                "score": 0.0,
                "reason": "insufficient_data"
            }
        
        # Calculate distance to recent points
        recent_array = np.array(self.recent_vectors)
        
        # Sample for efficiency
        if len(recent_array) > 500:
            sample_indices = np.random.choice(len(recent_array), 500, replace=False)
            recent_sample = recent_array[sample_indices]
        else:
            recent_sample = recent_array
        
        # Find nearest neighbor distance
        distances = np.linalg.norm(recent_sample - vector, axis=1)
        min_distance = float(np.min(distances))
        avg_distance = float(np.mean(np.sort(distances)[:10]))
        
        # Calculate threshold from historical data
        threshold = self._calculate_threshold()
        
        return {
            "is_anomaly": avg_distance > threshold,
            "score": avg_distance,
            "threshold": threshold,
            "min_distance": min_distance,
            "timestamp": timestamp.isoformat() if timestamp else None
        }
    
    def _calculate_threshold(self) -> float:
        """Calculate threshold from historical scores."""
        if len(self.baseline_stats) < 100:
            return float('inf')
        
        # Use percentile of recent scores
        scores = sorted(self.baseline_stats[-1000:])
        percentile = self.threshold_percentile
        
        index = int(len(scores) * percentile / 100)
        
        return scores[index]
    
    def update_baseline(self, score: float):
        """Update baseline statistics."""
        self.baseline_stats.append(score)
        
        # Keep only recent history
        if len(self.baseline_stats) > 10000:
            self.baseline_stats = self.baseline_stats[-5000:]
```

## Deduplication

### 1. Similarity-Based Deduplication

```python
class SimilarityDeduplicator:
    """
    Find and remove duplicate records using vector similarity.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.similarity_threshold = config.get("threshold", 0.95)
        self.vector_store = VectorStore("dedup_vectors")
    
    def find_duplicates(
        self,
        records: List[dict],
        id_field: str = "id",
        content_field: str = "content"
    ) -> List[dict]:
        """Find duplicate record pairs."""
        # Index records
        record_vectors = {}
        
        for record in records:
            record_id = record[id_field]
            content = record[content_field]
            
            vector = self.embedding_model.encode(content)
            record_vectors[record_id] = vector
            
            self.vector_store.upsert(record_id, vector)
        
        # Find similar pairs
        duplicate_pairs = []
        processed = set()
        
        for record_id, vector in record_vectors.items():
            # Search for similar records
            results = self.vector_store.search(
                vector,
                k=20,
                filter=None
            )
            
            for similar_id, similarity in results:
                if similar_id == record_id:
                    continue
                
                pair_key = tuple(sorted([record_id, similar_id]))
                
                if pair_key in processed:
                    continue
                
                if similarity >= self.similarity_threshold:
                    duplicate_pairs.append({
                        "record_1": record_id,
                        "record_2": similar_id,
                        "similarity": float(similarity)
                    })
                    processed.add(pair_key)
        
        return duplicate_pairs
    
    def merge_duplicates(
        self,
        records: List[dict],
        duplicate_pairs: List[dict],
        id_field: str = "id"
    ) -> List[dict]:
        """Merge duplicate records."""
        # Build union-find structure
        uf = UnionFind(len(records))
        
        record_map = {r[id_field]: i for i, r in enumerate(records)}
        
        for pair in duplicate_pairs:
            idx1 = record_map[pair["record_1"]]
            idx2 = record_map[pair["record_2"]]
            uf.union(idx1, idx2)
        
        # Group by cluster
        clusters = defaultdict(list)
        
        for i in range(len(records)):
            cluster_id = uf.find(i)
            clusters[cluster_id].append(records[i])
        
        # Merge each cluster
        merged = []
        
        for cluster in clusters.values():
            if len(cluster) == 1:
                merged.append(cluster[0])
            else:
                merged.append(self._merge_cluster(cluster))
        
        return merged
    
    def _merge_cluster(self, cluster: List[dict]) -> dict:
        """Merge a cluster of duplicate records."""
        # Keep record with most fields filled
        best = max(cluster, key=lambda r: sum(1 for v in r.values() if v))
        
        # Merge metadata about duplicates
        merged = best.copy()
        merged["duplicate_count"] = len(cluster)
        merged["duplicate_ids"] = [r.get("id") for r in cluster]
        
        return merged


class UnionFind:
    """Union-Find data structure for clustering."""
    
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: int, y: int):
        px = self.find(x)
        py = self.find(y)
        
        if px == py:
            return
        
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        
        self.parent[py] = px
        
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
```

### 2. Locality-Sensitive Hashing for Dedup

```python
class LSHDedup:
    """
    Locality-Sensitive Hashing for efficient deduplication.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.num_bands = config.get("num_bands", 20)
        self.rows_per_band = config.get("rows_per_band", 5)
        self.hash_tables = [defaultdict(list) for _ in range(self.num_bands)]
        self.signatures = {}  # record_id -> signature
    
    def _minhash_signature(self, vector: np.ndarray, num_hashes: int = 100) -> List[int]:
        """Generate MinHash signature for vector."""
        import random
        
        signature = []
        dim = len(vector)
        
        # Create random projection matrices
        for _ in range(num_hashes):
            # Random line direction
            line = np.random.randn(dim)
            line = line / np.linalg.norm(line)
            
            # Project
            projection = np.dot(vector, line)
            signature.append(int(projection * 1000))
        
        return signature
    
    def add_record(self, record_id: str, vector: np.ndarray):
        """Add record to LSH index."""
        # Generate MinHash signature
        signature = self._minhash_signature(vector)
        self.signatures[record_id] = signature
        
        # Add to hash tables
        for band_idx in range(self.num_bands):
            start = band_idx * self.rows_per_band
            end = start + self.rows_per_band
            
            band_signature = tuple(signature[start:end])
            band_hash = hash(band_signature)
            
            self.hash_tables[band_idx][band_hash].append(record_id)
    
    def find_candidates(self, record_id: str) -> Set[str]:
        """Find candidate duplicate records."""
        if record_id not in self.signatures:
            return set()
        
        signature = self.signatures[record_id]
        candidates = set()
        
        for band_idx in range(self.num_bands):
            start = band_idx * self.rows_per_band
            end = start + self.rows_per_band
            
            band_signature = tuple(signature[start:end])
            band_hash = hash(band_signature)
            
            # Add all records in same bucket
            candidates.update(self.hash_tables[band_idx][band_hash])
        
        # Remove self
        candidates.discard(record_id)
        
        return candidates
```

## Classification

### 1. KNN Classification

```python
class KNNClassifier:
    """
    K-Nearest Neighbors classifier using vector search.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.k = config.get("k", 5)
        self.class_vectors = {}  # class_name -> list of vectors
        self.class_centroids = {}  # class_name -> centroid vector
        self.vector_store = VectorStore("class_vectors")
    
    def fit(self, labeled_data: List[dict]):
        """Train classifier with labeled data."""
        # Group vectors by class
        for item in labeled_data:
            class_name = item["label"]
            vector = item["vector"]
            
            if class_name not in self.class_vectors:
                self.class_vectors[class_name] = []
            
            self.class_vectors[class_name].append(vector)
            
            # Index in vector store
            sample_id = f"{class_name}:{len(self.class_vectors[class_name])}"
            self.vector_store.upsert(sample_id, vector, {"class": class_name})
        
        # Compute class centroids
        for class_name, vectors in self.class_vectors.items():
            centroid = np.mean(vectors, axis=0)
            self.class_centroids[class_name] = centroid
        
        print(f"Trained on {len(labeled_data)} samples across {len(self.class_vectors)} classes")
    
    def predict(self, vector: np.ndarray) -> dict:
        """Predict class for a vector."""
        # Search for nearest neighbors
        results = self.vector_store.search(vector, k=self.k)
        
        # Count class votes
        class_votes = defaultdict(int)
        class_distances = defaultdict(list)
        
        for sample_id, distance in results:
            class_name = results[0].get("metadata", {}).get("class", "unknown")
            class_votes[class_name] += 1
            class_distances[class_name].append(distance)
        
        # Get top classes
        top_classes = sorted(
            class_votes.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        # Calculate weighted scores
        predictions = []
        
        for class_name, votes in top_classes:
            # Weighted by inverse distance
            distances = class_distances[class_name]
            weight = sum(1 / (d + 1e-10) for d in distances)
            
            predictions.append({
                "class": class_name,
                "votes": votes,
                "confidence": float(weight / sum(p[1] for p in top_classes))
            })
        
        return predictions[0] if predictions else None
    
    def predict_with_centroid(
        self,
        vector: np.ndarray,
        metric: str = "cosine"
    ) -> dict:
        """Predict using centroid distance."""
        scores = {}
        
        for class_name, centroid in self.class_centroids.items():
            if metric == "cosine":
                similarity = np.dot(vector, centroid) / (
                    np.linalg.norm(vector) * np.linalg.norm(centroid)
                )
                scores[class_name] = float(similarity)
            else:  # euclidean
                distance = np.linalg.norm(vector - centroid)
                scores[class_name] = float(-distance)  # Negative for sorting
        
        # Sort by score
        sorted_classes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "class": sorted_classes[0][0],
            "confidence": sorted_classes[0][1],
            "all_scores": scores
        }
```

### 2. Prototype-Based Classification

```python
class PrototypeClassifier:
    """
    Classification using class prototypes (medoids/centroids).
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.num_prototypes = config.get("num_prototypes", 5)
        self.class_prototypes = {}
        self.prototype_vectors = []
        self.prototype_labels = []
    
    def fit(self, labeled_data: List[dict]):
        """Learn prototypes for each class."""
        from sklearn.cluster import KMeans
        
        # Group by class
        class_data = defaultdict(list)
        
        for item in labeled_data:
            class_data[item["label"]].append(item["vector"])
        
        # Learn prototypes per class
        for class_name, vectors in class_data.items():
            vectors = np.array(vectors)
            
            num_prototypes = min(self.num_prototypes, len(vectors))
            
            if num_prototypes == 1:
                # Single prototype = centroid
                prototype = np.mean(vectors, axis=0)
                self.class_prototypes[class_name] = [prototype]
            else:
                # K-means to find prototypes
                kmeans = KMeans(n_clusters=num_prototypes, random_state=42)
                kmeans.fit(vectors)
                
                # Use cluster centers as prototypes
                self.class_prototypes[class_name] = kmeans.cluster_centers_
            
            # Add to searchable index
            for i, prototype in enumerate(self.class_prototypes[class_name]):
                prototype_id = f"{class_name}:{i}"
                self.prototype_vectors.append(prototype)
                self.prototype_labels.append(class_name)
        
        # Build vector index
        self.prototype_index = self._build_index(np.array(self.prototype_vectors))
        
        print(f"Learned {len(self.prototype_vectors)} prototypes across {len(self.class_prototypes)} classes")
    
    def _build_index(self, vectors: np.ndarray):
        """Build vector search index."""
        # Use HNSW for fast prototyping
        return HNSWIndex(m=16, ef=100).build(vectors)
    
    def predict(self, vector: np.ndarray, return_scores: bool = False) -> dict:
        """Classify vector using prototype matching."""
        # Search for nearest prototypes
        distances, indices = self.prototype_index.search(vector.reshape(1, -1), k=10)
        
        # Aggregate scores by class
        class_scores = defaultdict(lambda: {"score": 0, "count": 0})
        
        for dist, idx in zip(distances[0], indices[0]):
            class_name = self.prototype_labels[idx]
            
            # Score = inverse distance
            score = 1 / (dist + 1e-10)
            class_scores[class_name]["score"] += score
            class_scores[class_name]["count"] += 1
        
        # Normalize by prototype count
        for class_name in class_scores:
            num_prototypes = len(self.class_prototypes[class_name])
            class_scores[class_name]["score"] /= num_prototypes
        
        # Sort by score
        sorted_classes = sorted(
            class_scores.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        top_class = sorted_classes[0]
        
        result = {
            "class": top_class[0],
            "confidence": top_class[1]["score"],
            "matching_prototypes": top_class[1]["count"]
        }
        
        if return_scores:
            result["all_scores"] = {
                c: s["score"] for c, s in sorted_classes
            }
        
        return result
```

### 3. Ensemble Classification

```python
class EnsembleVectorClassifier:
    """
    Ensemble of vector-based classifiers.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.classifiers = []
        self.weights = config.get("weights", None)
    
    def add_classifier(self, classifier, weight: float = 1.0):
        """Add classifier to ensemble."""
        self.classifiers.append(classifier)
        
        if self.weights is None:
            self.weights = []
        self.weights.append(weight)
    
    def fit(self, labeled_data: List[dict]):
        """Train all classifiers in ensemble."""
        for classifier in self.classifiers:
            classifier.fit(labeled_data)
    
    def predict(self, vector: np.ndarray) -> dict:
        """Ensemble prediction with weighted voting."""
        all_predictions = []
        
        # Get predictions from each classifier
        for classifier in self.classifiers:
            pred = classifier.predict(vector)
            all_predictions.append(pred)
        
        # Aggregate predictions
        class_scores = defaultdict(float)
        total_weight = sum(self.weights)
        
        for pred, weight in zip(all_predictions, self.weights):
            class_name = pred["class"]
            confidence = pred.get("confidence", 1.0)
            
            # Weighted score
            class_scores[class_name] += weight * confidence
        
        # Normalize
        for class_name in class_scores:
            class_scores[class_name] /= total_weight
        
        # Sort by score
        sorted_classes = sorted(
            class_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "class": sorted_classes[0][0],
            "confidence": sorted_classes[0][1],
            "ensemble_votes": dict(sorted_classes[:5]),
            "individual_predictions": all_predictions
        }
```

## Best Practices

### 1. Pattern Selection Matrix

```python
PATTERN_BEST_PRACTICES = {
    "recommendation": {
        "indexing": {
            "user_vectors": "Rebuild weekly or on significant interaction changes",
            "item_vectors": "Daily or on catalog updates"
        },
        "query_optimization": {
            "召回率": "Use HNSW with high recall (ef=200+) for candidate generation",
            "排序": "Use lightweight scoring for re-ranking"
        },
        "冷启动": [
            "Use popularity-based recommendations for new users",
            "Use content-based features for new items",
            "Consider exploration/exploitation balance"
        ]
    },
    
    "semantic_search": {
        "indexing": {
            "chunking": "512 tokens with 50 token overlap for general text",
            "metadata": "Index metadata fields for filtering"
        },
        "query_optimization": {
            "embedding": "Use domain-specific embeddings when available",
            "reranking": "Apply cross-encoder reranking for top results"
        },
        "quality": [
            "Monitor retrieval precision on sample queries",
            "Update embeddings when domain vocabulary changes",
            "Use hybrid search for keyword-sensitive queries"
        ]
    },
    
    "anomaly_detection": {
        "indexing": {
            "baseline": "Regular refresh of normal behavior baseline",
            "window": "Sliding window for streaming scenarios"
        },
        "threshold": {
            "calibration": "Use percentile-based threshold from recent history",
            "adjustment": "Adjust based on false positive rate"
        },
        "accuracy": [
            "Combine multiple detection methods for robustness",
            "Use labeled anomalies when available for calibration",
            "Monitor detection rate drift over time"
        ]
    },
    
    "deduplication": {
        "indexing": {
            "blocking": "Use blocking keys to reduce comparison space",
            "signature": "Use MinHash/LSH for scalable similarity search"
        },
        "threshold": {
            "tuning": "Adjust threshold based on precision/recall trade-off",
            "domain": "Different thresholds for different entity types"
        },
        "quality": [
            "Review edge cases manually for threshold calibration",
            "Consider transitive closure of duplicate relationships",
            "Track false positive and negative rates"
        ]
    },
    
    "classification": {
        "indexing": {
            "prototypes": "Use class centroids or medoids",
            "sampling": "Balance training data across classes"
        },
        "query_optimization": {
            "k": "Use odd k to avoid ties in voting",
            "distance": "Consider distance weighting for votes"
        },
        "accuracy": [
            "Monitor per-class precision and recall",
            "Use class-specific thresholds when needed",
            "Consider class hierarchy in prediction"
        ]
    }
}
```

### 2. Performance Optimization

```python
class PerformanceOptimizer:
    """
    Optimize performance for vector application patterns.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.cache = ResultCache()
        self.batching = BatchProcessor()
    
    def optimize_recommendation(self, system: RecommendationSystem):
        """Optimize recommendation system performance."""
        optimizations = []
        
        # Cache popular recommendations
        optimizations.append({
            "strategy": "popular_recommendation_cache",
            "impact": "Reduce latency by 90% for 80% of requests"
        })
        
        # Batch embedding updates
        optimizations.append({
            "strategy": "async_embedding_updates",
            "impact": "Reduce write latency by 10x"
        })
        
        # Use approximate search for initial recall
        optimizations.append({
            "strategy": "two_stage_recall",
            "initial": "HNSW ef=100 (fast)",
            "rerank": "Exact k-NN on candidates"
        })
        
        return optimizations
    
    def optimize_semantic_search(self, search: SemanticSearchIndex):
        """Optimize semantic search performance."""
        optimizations = []
        
        # Cache query results
        optimizations.append({
            "strategy": "query_result_cache",
            "ttl": "5 minutes for frequently updated corpora",
            "invalidation": "On document update"
        })
        
        # Optimize chunk size
        optimizations.append({
            "strategy": "adaptive_chunking",
            "small_docs": "No chunking for docs < 500 tokens",
            "large_docs": "Larger overlap for better recall"
        })
        
        return optimizations
```

## Troubleshooting

### Common Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Recommendation cold start | New users get random recommendations | Use popularity/content-based fallback |
| Semantic search quality | Low relevance scores | Check embedding model, adjust chunking |
| Anomaly detection false positives | Too many alerts | Adjust threshold, use ensemble methods |
| Dedup performance | Slow processing | Use blocking/LSH to reduce search space |
| Classification imbalanced | Some classes always predicted | Use class weights or oversampling |

### Debugging Strategies

```python
def debug_vector_application(application: str, data: dict):
    """Debug vector application issues."""
    debug_strategies = {
        "recommendation": debug_recommendation,
        "semantic_search": debug_semantic_search,
        "anomaly_detection": debug_anomaly_detection,
        "deduplication": debug_deduplication,
        "classification": debug_classification
    }
    
    if application in debug_strategies:
        return debug_strategies[application](data)
    else:
        return {"error": "Unknown application type"}


def debug_recommendation(data: dict) -> dict:
    """Debug recommendation system."""
    return {
        "user_vector_quality": check_vector_quality(data.get("user_vector")),
        "item_vector_distribution": analyze_distribution(data.get("item_vectors")),
        "coverage_metrics": calculate_coverage(data),
        "recommendations_sample": sample_recommendations(data, n=10)
    }


def debug_semantic_search(data: dict) -> dict:
    """Debug semantic search."""
    return {
        "query_expansion": data.get("expanded_queries", []),
        "retrieval_precision": calculate_retrieval_precision(data),
        "reranking_impact": compare_before_after_reranking(data),
        "index_health": check_index_health(data.get("index"))
    }
```

## Examples

### Example 1: Complete Recommendation Pipeline

```python
class ProductionRecommendationSystem:
    """
    Production-ready recommendation system.
    """
    
    def __init__(self, config: dict):
        self.config = config
        
        # Initialize components
        self.embedding_service = EmbeddingService(config["embedding"])
        self.vector_store = VectorStore(config["vector_store"])
        
        # Recommendation strategies
        self.collaborative = CollaborativeFiltering(config["collab"])
        self.content_based = ContentBasedRecommender(config["content"])
        self.hybrid = HybridRecommender(config["hybrid"])
        
        # Caching
        self.cache = MultiLevelCache(config["cache"])
        
        # Monitoring
        self.metrics = MetricsCollector()
    
    def recommend(
        self,
        user_id: str,
        context: dict = None,
        k: int = 10,
        strategy: str = "hybrid"
    ) -> List[dict]:
        """Generate recommendations."""
        start_time = time.time()
        
        # Check cache
        cache_key = f"rec:{user_id}:{strategy}:{k}"
        cached = self.cache.get(cache_key)
        
        if cached:
            self.metrics.increment("recommendations_cache_hit")
            return cached
        
        # Generate recommendations based on strategy
        if strategy == "collaborative":
            results = self.collaborative.recommend_for_user(user_id, k)
        elif strategy == "content":
            results = self.content_based.recommend_for_user_profile(
                self._get_user_liked_items(user_id),
                k=k
            )
        else:
            results = self.hybrid.recommend(user_id, context, k)
        
        # Cache results
        self.cache.set(cache_key, results, ttl=300)
        
        # Record metrics
        latency = (time.time() - start_time) * 1000
        self.metrics.record("recommendation_latency_ms", latency)
        
        return results
```

### Example 2: Production Semantic Search

```python
class ProductionSemanticSearch:
    """
    Production semantic search with monitoring.
    """
    
    def __init__(self, config: dict):
        self.config = config
        
        # Indexing pipeline
        self.indexer = DocumentIndexer(config["indexing"])
        
        # Search components
        self.searcher = SemanticQueryProcessor(config["query"])
        self.index = self.indexer.load_index()
        
        # Result enhancement
        self.enhancer = SearchResultEnhancer(config.get("enhancement", {}))
        
        # Monitoring
        self.metrics = MetricsCollector()
    
    def search(
        self,
        query: str,
        k: int = 10,
        filters: dict = None,
        user_id: str = None
    ) -> dict:
        """Execute semantic search."""
        start_time = time.time()
        
        # Process query
        processed = self.searcher.process_query(query)
        
        # Merge filters
        combined_filters = {**(processed.get("filters", {})), **(filters or {})}
        
        # Execute search
        results = self.index.search(
            processed["expanded_queries"][0] if processed["expanded_queries"] else query,
            k=k * 2,
            filters=combined_filters
        )
        
        # Enhance results
        enhanced = self.enhancer.enhance_results(query, results)
        
        # Record metrics
        latency = (time.time() - start_time) * 1000
        self.metrics.record("search_latency_ms", latency)
        self.metrics.increment("search_requests_total")
        
        if user_id:
            self._log_search(user_id, query, results)
        
        return {
            "query": query,
            "processed_query": processed,
            "results": enhanced[:k],
            "total_candidates": len(results),
            "latency_ms": latency
        }
```

## References

1. **Recommendation Systems**: https://developers.google.com/machine-learning/recommendation
2. **Vector Search Applications**: https://github.com/facebookresearch/faiss/wiki/Application-examples
3. **Anomaly Detection**: https://scikit-learn.org/stable/modules/outlier_detection.html
4. **Cursor Enterprise Framework - Vector Search Rules**: `.cursor/rules/vector-search.mdc`
