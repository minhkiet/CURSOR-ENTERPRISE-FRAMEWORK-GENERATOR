---
title: "Reranking Strategies"
description: "Hướng dẫn về các chiến lược reranking: cross-encoder, bi-encoder, late interaction models và RRF fusion"
tags: ["reranking", "cross-encoder", "bi-encoder", "llm", "search", "rank-fusion"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Reranking Strategies

## Tổng Quan

Reranking là kỹ thuật quan trọng trong RAG systems, giúp cải thiện đáng kể quality của retrieval results bằng cách sử dụng more expensive nhưng accurate reranking models sau khi đã có candidate set từ initial retrieval.

Trong typical RAG pipeline, chúng ta thường:
1. **Retrieval (Bi-encoder)**: Nhanh nhưng approximate - sử dụng embedding similarity để get top-K candidates
2. **Reranking (Cross-encoder)**: Chậm hơn nhưng chính xác hơn - đánh giá lại candidates với full cross-attention

Việc kết hợp cả hai approaches mang lại best of both worlds: speed của bi-encoder retrieval và accuracy của cross-encoder reranking.

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức toàn diện về reranking strategies:

Đầu tiên, chúng ta sẽ tìm hiểu cross-encoder reranking - phương pháp chính xác nhất.

Thứ hai, tài liệu hướng dẫn bi-encoder reranking cho cases cần speed.

Thứ ba, chúng ta sẽ đề cập đến late interaction models như ColBERT.

Cuối cùng, tài liệu cung cấp RRF fusion và các best practices.

## Key Concepts

### 1. Cross-encoder Architecture

Cross-encoder process query và document cùng nhau trong một forward pass, cho phép full attention giữa query và document tokens.

```
Query: "What is machine learning?"
Document: "Machine learning is a subset of artificial intelligence..."

Cross-Encoder Architecture:
┌─────────────────────────────────────────────────────────────┐
│  Input: [CLS] Query [SEP] Document [SEP]                   │
│           ↓           ↓           ↓                        │
│        Token Embeddings + Position Embeddings                │
│                    ↓                                        │
│              Transformer Layer                              │
│         (Full Cross-Attention)                              │
│                    ↓                                        │
│              [CLS] Output                                   │
│                    ↓                                        │
│            Relevance Score                                   │
└─────────────────────────────────────────────────────────────┘
```

```python
from sentence_transformers import CrossEncoder

class CrossEncoderReranker:
    """
    Reranker using Cross-Encoder model.
    """
    
    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-12-v2",
        max_length: int = 512
    ):
        self.model = CrossEncoder(
            model_name,
            max_length=max_length
        )
    
    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 10
    ) -> List[dict]:
        """
        Rerank documents for a query.
        
        Returns:
            List of dicts with document, score, and rank
        """
        # Create query-document pairs
        pairs = [(query, doc) for doc in documents]
        
        # Get relevance scores
        scores = self.model.predict(pairs)
        
        # Sort by score and return top-k
        results = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {
                "document": doc,
                "score": float(score),
                "rank": i + 1
            }
            for i, (doc, score) in enumerate(results[:top_k])
        ]
```

### 2. Bi-encoder Reranking

Bi-encoder reranking sử dụng pre-computed embeddings, faster nhưng less accurate.

```python
class BiEncoderReranker:
    """
    Reranker using Bi-Encoder model.
    Faster than cross-encoder but less accurate.
    """
    
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
    
    def rerank(
        self,
        query: str,
        documents: List[str],
        query_embedding: List[float] = None,
        top_k: int = 10
    ) -> List[dict]:
        """
        Rerank documents using bi-encoder.
        """
        # Encode query (or use provided embedding)
        if query_embedding is None:
            query_embedding = self.model.encode(query)
        
        # Encode documents
        doc_embeddings = self.model.encode(documents)
        
        # Calculate similarities
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity(
            [query_embedding],
            doc_embeddings
        )[0]
        
        # Sort and return
        results = sorted(
            zip(documents, similarities),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {
                "document": doc,
                "score": float(score),
                "rank": i + 1
            }
            for i, (doc, score) in enumerate(results[:top_k])
        ]
```

### 3. Late Interaction Models (ColBERT)

Late interaction models như ColBERT cho phép fine-grained matching mà vẫn giữ được speed.

```python
class ColBERTReranker:
    """
    ColBERT-style late interaction reranking.
    
    ColBERT encodes query and document separately,
    then uses MaxSim operator for late interaction.
    """
    
    def __init__(
        self,
        model_name: str = "colbert-ir/colbertv2.0"
    ):
        from transformers import AutoTokenizer, AutoModel
        import torch
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
    
    def _encode(self, text: str, mask: bool = True) -> torch.Tensor:
        """Encode text to token embeddings."""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Get token embeddings (late interaction)
        embeddings = outputs.last_hidden_state
        
        # Apply mask if needed
        if mask:
            mask = inputs["attention_mask"].unsqueeze(-1).float()
            embeddings = embeddings * mask
        
        return embeddings
    
    def score(self, query: str, document: str) -> float:
        """
        Calculate relevance score using MaxSim.
        """
        import torch.nn.functional as F
        
        # Encode query and document
        Q = self._encode(query)  # [query_len, dim]
        D = self._encode(document)  # [doc_len, dim]
        
        # MaxSim: for each query token, find max similarity with doc tokens
        # Q: [query_len, dim] -> [1, query_len, dim]
        # D: [doc_len, dim] -> [1, dim, doc_len]
        # Similarity: [1, query_len, doc_len]
        similarity = torch.matmul(
            Q.unsqueeze(0),
            D.unsqueeze(0).transpose(1, 2)
        ).squeeze(0)
        
        # Max over document tokens for each query token
        max_sim = similarity.max(dim=1).values  # [query_len]
        
        # Mean over query tokens
        score = max_sim.mean().item()
        
        return score
    
    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 10
    ) -> List[dict]:
        """Rerank documents using ColBERT."""
        scores = []
        
        for doc in documents:
            score = self.score(query, doc)
            scores.append(score)
        
        # Sort by score
        results = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {
                "document": doc,
                "score": float(score),
                "rank": i + 1
            }
            for i, (doc, score) in enumerate(results[:top_k])
        ]
```

## RRF Fusion

### 1. Reciprocal Rank Fusion

RRF là phương pháp đơn giản và hiệu quả để combine multiple rankings.

```python
def reciprocal_rank_fusion(
    rankings: List[List[dict]],
    k: int = 60
) -> List[dict]:
    """
    Combine multiple rankings using RRF.
    
    Args:
        rankings: List of rankings, each is list of dicts with 'id' and 'document'
        k: RRF constant (default 60)
    
    Returns:
        Fused ranking
    """
    scores = {}
    
    for ranking in rankings:
        for rank, item in enumerate(ranking, 1):
            item_id = item.get("id", item.get("document"))
            
            if item_id not in scores:
                scores[item_id] = {
                    "document": item.get("document", item_id),
                    "metadata": item.get("metadata", {}),
                    "rrf_score": 0
                }
            
            # RRF formula: 1 / (k + rank)
            scores[item_id]["rrf_score"] += 1.0 / (k + rank)
    
    # Sort by RRF score
    fused = sorted(
        scores.values(),
        key=lambda x: x["rrf_score"],
        reverse=True
    )
    
    return fused


def rrf_with_scores(
    rankings: List[List[dict]],
    weights: List[float] = None,
    k: int = 60
) -> List[dict]:
    """
    RRF với weighted combination of scores.
    """
    if weights is None:
        weights = [1.0] * len(rankings)
    
    # Normalize weights
    total_weight = sum(weights)
    weights = [w / total_weight for w in weights]
    
    scores = {}
    
    for ranking, weight in zip(rankings, weights):
        for rank, item in enumerate(ranking, 1):
            item_id = item.get("id", item.get("document"))
            
            if item_id not in scores:
                scores[item_id] = {
                    "document": item.get("document", item_id),
                    "metadata": item.get("metadata", {}),
                    "weighted_rrf_score": 0,
                    "original_scores": {}
                }
            
            # Weighted RRF
            rrf_contribution = weight * (1.0 / (k + rank))
            scores[item_id]["weighted_rrf_score"] += rrf_contribution
            scores[item_id]["original_scores"][str(rank)] = item.get("score", 1.0 / (k + rank))
    
    # Sort by weighted RRF score
    fused = sorted(
        scores.values(),
        key=lambda x: x["weighted_rrf_score"],
        reverse=True
    )
    
    return fused
```

### 2. Score-based Fusion

```python
def score_normalize(scores: List[float], method: str = "min-max") -> List[float]:
    """
    Normalize scores to [0, 1] range.
    """
    if not scores:
        return []
    
    if method == "min-max":
        min_s = min(scores)
        max_s = max(scores)
        
        if max_s == min_s:
            return [1.0] * len(scores)
        
        return [(s - min_s) / (max_s - min_s) for s in scores]
    
    elif method == "z-score":
        import numpy as np
        mean = np.mean(scores)
        std = np.std(scores)
        
        if std == 0:
            return [1.0] * len(scores)
        
        return [(s - mean) / std for s in scores]
    
    elif method == "rank":
        # Convert to rank-based scores
        sorted_scores = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        ranks = [0] * len(scores)
        
        for rank, (idx, _) in enumerate(sorted_scores, 1):
            ranks[idx] = 1.0 / rank
        
        return ranks
    
    return scores


def linear_score_fusion(
    rankings: List[List[dict]],
    weights: List[float] = None,
    score_key: str = "score"
) -> List[dict]:
    """
    Linear combination of normalized scores.
    """
    if weights is None:
        weights = [1.0] * len(rankings)
    
    # Normalize weights
    total_weight = sum(weights)
    weights = [w / total_weight for w in weights]
    
    scores = {}
    
    for ranking, weight in zip(rankings, weights):
        # Normalize scores
        raw_scores = [item.get(score_key, 0) for item in ranking]
        norm_scores = score_normalize(raw_scores)
        
        for item, norm_score in zip(ranking, norm_scores):
            item_id = item.get("id", item.get("document"))
            
            if item_id not in scores:
                scores[item_id] = {
                    "document": item.get("document", item_id),
                    "metadata": item.get("metadata", {}),
                    "fused_score": 0
                }
            
            scores[item_id]["fused_score"] += weight * norm_score
    
    # Sort by fused score
    fused = sorted(
        scores.values(),
        key=lambda x: x["fused_score"],
        reverse=True
    )
    
    return fused
```

### 3. Advanced Fusion Methods

```python
def borda_count_fusion(rankings: List[List[dict]]) -> List[dict]:
    """
    Borda Count fusion - each rank gets points based on position.
    """
    if not rankings:
        return []
    
    n_rankings = len(rankings)
    n_candidates = max(len(r) for r in rankings)
    
    scores = {}
    
    for ranking in rankings:
        for rank, item in enumerate(ranking, 1):
            item_id = item.get("id", item.get("document"))
            
            if item_id not in scores:
                scores[item_id] = {
                    "document": item.get("document", item_id),
                    "borda_score": 0
                }
            
            # Borda count: n - rank points
            scores[item_id]["borda_score"] += n_candidates - rank
    
    # Sort by borda score
    fused = sorted(
        scores.values(),
        key=lambda x: x["borda_score"],
        reverse=True
    )
    
    return fused


def combMNZ_fusion(
    rankings: List[List[dict]],
    score_key: str = "score"
) -> List[dict]:
    """
    CombMNZ (Combination with Multiplicative Z) fusion.
    Multiplies sum of normalized scores by number of systems that retrieved the item.
    """
    scores = {}
    retrieval_count = {}
    
    for ranking in rankings:
        # Normalize scores
        raw_scores = [item.get(score_key, 0) for item in ranking]
        norm_scores = score_normalize(raw_scores, "min-max")
        
        for item, norm_score in zip(ranking, norm_scores):
            item_id = item.get("id", item.get("document"))
            
            if item_id not in scores:
                scores[item_id] = {
                    "document": item.get("document", item_id),
                    "sum_scores": 0
                }
                retrieval_count[item_id] = 0
            
            scores[item_id]["sum_scores"] += norm_score
            retrieval_count[item_id] += 1
    
    # Multiply by retrieval count
    for item_id in scores:
        scores[item_id]["combMNZ_score"] = (
            scores[item_id]["sum_scores"] * retrieval_count[item_id]
        )
    
    # Sort
    fused = sorted(
        scores.values(),
        key=lambda x: x["combMNZ_score"],
        reverse=True
    )
    
    return fused
```

## Best Practices

### 1. Cascade Retrieval Pipeline

```python
class CascadeRetrievalPipeline:
    """
    Multi-stage retrieval với progressive reranking.
    """
    
    def __init__(
        self,
        vector_store,
        rerankers: List[object] = None,
        retrieval_k: int = 100,
        final_k: int = 10
    ):
        self.vector_store = vector_store
        self.rerankers = rerankers or []
        self.retrieval_k = retrieval_k
        self.final_k = final_k
    
    async def retrieve_and_rerank(
        self,
        query: str,
        filters: dict = None
    ) -> List[dict]:
        """
        Retrieve and progressively rerank.
        """
        # Stage 1: Initial vector retrieval
        initial_results = await self.vector_store.search(
            query=query,
            k=self.retrieval_k,
            filters=filters
        )
        
        if not initial_results:
            return []
        
        # Apply rerankers in cascade
        current_results = initial_results
        
        for reranker in self.rerankers:
            reranked = reranker.rerank(
                query=query,
                documents=[r["document"] for r in current_results],
                top_k=self.final_k * 2  # Keep more for next stage
            )
            
            # Merge reranked scores with original retrieval scores
            current_results = self._merge_scores(
                current_results,
                reranked
            )
        
        # Final selection
        current_results.sort(key=lambda x: x["combined_score"], reverse=True)
        
        return current_results[:self.final_k]
    
    def _merge_scores(
        self,
        initial: List[dict],
        reranked: List[dict]
    ) -> List[dict]:
        """Merge initial and reranked scores."""
        # Create lookup for reranked results
        reranked_dict = {
            r["document"]: r["score"]
            for r in reranked
        }
        
        # Merge
        merged = []
        for item in initial:
            rerank_score = reranked_dict.get(item["document"], 0)
            
            # Combine scores (can be weighted)
            combined_score = (
                0.3 * item.get("score", 0) +
                0.7 * rerank_score
            )
            
            merged.append({
                **item,
                "rerank_score": rerank_score,
                "combined_score": combined_score
            })
        
        return merged
```

### 2. Dynamic Reranking Strategy

```python
class DynamicReranker:
    """
    Choose reranking strategy based on query characteristics.
    """
    
    def __init__(
        self,
        fast_reranker,
        accurate_reranker,
        llm_reranker=None
    ):
        self.fast = fast_reranker
        self.accurate = accurate_reranker
        self.llm = llm_reranker
    
    def _analyze_query(self, query: str) -> dict:
        """Analyze query characteristics."""
        return {
            "length": len(query.split()),
            "complexity": self._estimate_complexity(query),
            "is_factual": self._is_factual_query(query),
            "requires_reasoning": self._requires_reasoning(query)
        }
    
    def _estimate_complexity(self, query: str) -> str:
        """Estimate query complexity."""
        words = len(query.split())
        
        if words < 5:
            return "simple"
        elif words < 15:
            return "moderate"
        else:
            return "complex"
    
    def _is_factual_query(self, query: str) -> bool:
        """Check if query is factual (who, what, when, where)."""
        factual_patterns = [
            r"^(who|what|when|where|how many|how much)",
            r"(definition|meaning|explain)",
            r"(date|year|number|count)"
        ]
        
        import re
        return any(
            re.search(p, query.lower())
            for p in factual_patterns
        )
    
    def _requires_reasoning(self, query: str) -> bool:
        """Check if query requires multi-step reasoning."""
        reasoning_patterns = [
            r"(compare|contrast|difference)",
            r"(why|because|reason)",
            r"(if|then|unless)",
            r"(therefore|consequently|as a result)"
        ]
        
        import re
        return any(
            re.search(p, query.lower())
            for p in reasoning_patterns
        )
    
    async def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 10
    ) -> List[dict]:
        """Choose reranking strategy dynamically."""
        analysis = self._analyze_query(query)
        
        # Simple factual query -> fast reranker
        if analysis["complexity"] == "simple" and analysis["is_factual"]:
            return await self.fast.rerank(query, documents, top_k)
        
        # Complex query -> accurate reranker
        if analysis["complexity"] == "complex" or analysis["requires_reasoning"]:
            return await self.accurate.rerank(query, documents, top_k)
        
        # Default: use fast reranker
        return await self.fast.rerank(query, documents, top_k)
```

### 3. LLM-based Reranking

```python
class LLMReranker:
    """
    Rerank using LLM to evaluate relevance.
    """
    
    def __init__(
        self,
        llm_client,
        prompt_template: str = None
    ):
        self.llm = llm_client
        
        self.default_prompt = """
You are an expert at evaluating how relevant a document is to a user query.

Query: {query}

Document: {document}

Your task: Rate the relevance of this document to the query on a scale of 0 to 10.
- 0: Completely irrelevant
- 5: Somewhat relevant but missing key information
- 10: Perfectly relevant, directly answers the query

Provide your rating and a brief explanation.

Rating: """
    
    async def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 10
    ) -> List[dict]:
        """Rerank documents using LLM."""
        results = []
        
        for doc in documents:
            prompt = self.default_prompt.format(
                query=query,
                document=doc[:2000]  # Truncate for token limits
            )
            
            response = await self.llm.complete(prompt)
            
            # Parse rating from response
            rating = self._parse_rating(response)
            
            results.append({
                "document": doc,
                "score": rating,
                "llm_reasoning": response
            })
        
        # Sort by rating
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:top_k]
    
    def _parse_rating(self, response: str) -> float:
        """Parse rating from LLM response."""
        import re
        
        # Look for number in response
        match = re.search(r'[Rr]ating:\s*(\d+(?:\.\d+)?)', response)
        
        if match:
            rating = float(match.group(1))
            return min(max(rating / 10, 0), 1)  # Normalize to [0, 1]
        
        return 0.5  # Default if can't parse
```

## Common Patterns

### Pattern 1: Two-Stage Retrieval + Rerank

```python
class TwoStageRAG:
    """
    Standard two-stage retrieval với reranking.
    """
    
    def __init__(
        self,
        vector_store,
        reranker
    ):
        self.vector_store = vector_store
        self.reranker = reranker
    
    async def retrieve(
        self,
        query: str,
        k_initial: int = 100,
        k_final: int = 10
    ) -> List[dict]:
        """
        Two-stage retrieval:
        1. Fast vector search to get candidates
        2. Rerank to get final results
        """
        # Stage 1: Initial retrieval
        candidates = await self.vector_store.search(
            query=query,
            k=k_initial
        )
        
        if not candidates:
            return []
        
        # Stage 2: Rerank
        reranked = self.reranker.rerank(
            query=query,
            documents=[c["document"] for c in candidates],
            top_k=k_final
        )
        
        # Merge metadata
        doc_lookup = {c["document"]: c for c in candidates}
        
        final_results = []
        for rank, item in enumerate(reranked, 1):
            original = doc_lookup[item["document"]]
            final_results.append({
                **original,
                "rerank_score": item["score"],
                "final_rank": rank
            })
        
        return final_results
```

### Pattern 2: Multi-retriever Fusion

```python
class MultiRetrieverFusion:
    """
    Fuse results from multiple retrievers.
    """
    
    def __init__(
        self,
        retrievers: Dict[str, object],
        fusion_method: str = "rrf"
    ):
        self.retrievers = retrievers
        self.fusion_method = fusion_method
    
    async def retrieve(
        self,
        query: str,
        k_per_retriever: int = 50,
        k_final: int = 10
    ) -> List[dict]:
        """Retrieve from all retrievers and fuse."""
        # Parallel retrieval from all retrievers
        tasks = [
            retriever.search(query=query, k=k_per_retriever)
            for retriever in self.retrievers.values()
        ]
        
        results_per_retriever = await asyncio.gather(*tasks)
        
        # Convert to rankings
        rankings = [
            [{"id": r.get("id", i), "document": r["document"], "score": r.get("score", 0)}
             for i, r in enumerate(results)]
            for results in results_per_retriever
        ]
        
        # Apply fusion
        if self.fusion_method == "rrf":
            fused = reciprocal_rank_fusion(rankings)
        elif self.fusion_method == "linear":
            fused = linear_score_fusion(rankings)
        elif self.fusion_method == "borda":
            fused = borda_count_fusion(rankings)
        else:
            fused = reciprocal_rank_fusion(rankings)
        
        return fused[:k_final]
```

### Pattern 3: Learned Reranking (Learning to Rank)

```python
class LearnedReranker:
    """
    ML-based reranker using LightGBM or XGBoost.
    """
    
    def __init__(self, model_path: str = None):
        self.model = None
        if model_path:
            import lightgbm as lgb
            self.model = lgb.Booster(model_file=model_path)
    
    def _extract_features(
        self,
        query: str,
        document: str,
        query_embedding: List[float],
        doc_embedding: List[float]
    ) -> List[float]:
        """Extract features for learning-to-rank."""
        features = []
        
        # Text features
        features.append(len(document) / 1000)  # Document length
        features.append(len(query) / 100)  # Query length
        
        # Overlap features
        query_words = set(query.lower().split())
        doc_words = set(document.lower().split())
        
        features.append(len(query_words & doc_words) / max(1, len(query_words)))  # Query term overlap
        features.append(len(query_words & doc_words) / max(1, len(doc_words)))  # Doc coverage
        
        # Semantic similarity
        import numpy as np
        q_emb = np.array(query_embedding)
        d_emb = np.array(doc_embedding)
        
        features.append(np.dot(q_emb, d_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(d_emb)))  # Cosine
        features.append(np.linalg.norm(q_emb - d_emb))  # L2 distance
        
        return features
    
    def rerank(
        self,
        query: str,
        documents: List[dict],
        query_embedding: List[float],
        top_k: int = 10
    ) -> List[dict]:
        """Rerank using learned model."""
        if not self.model:
            return documents[:top_k]
        
        # Extract features for all documents
        features_list = []
        for doc in documents:
            features = self._extract_features(
                query=query,
                document=doc["document"],
                query_embedding=query_embedding,
                doc_embedding=doc.get("embedding", [0] * 768)
            )
            features_list.append(features)
        
        # Predict scores
        scores = self.model.predict(features_list)
        
        # Sort by predicted score
        results = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {**doc, "learned_score": float(score), "rank": i + 1}
            for i, (doc, score) in enumerate(results[:top_k])
        ]
```

## Examples

### Example 1: Complete Reranking Pipeline

```python
class CompleteRerankingPipeline:
    """
    Full reranking pipeline với multiple strategies.
    """
    
    def __init__(self, config: dict):
        # Initialize retrievers
        self.vector_retriever = VectorRetriever(config["vector_store"])
        self.bm25_retriever = BM25Retriever(config["bm25_index"])
        
        # Initialize rerankers
        self.fast_reranker = CrossEncoderReranker(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )
        self.accurate_reranker = CrossEncoderReranker(
            "cross-encoder/ms-marcoELECTRA-base"
        )
        
        self.config = config
    
    async def retrieve(
        self,
        query: str,
        k_initial: int = 100,
        k_rerank: int = 20,
        k_final: int = 5
    ) -> List[dict]:
        """
        Complete retrieval pipeline.
        """
        # Parallel initial retrieval
        vector_results, bm25_results = await asyncio.gather(
            self.vector_retriever.search(query, k=k_initial),
            self.bm25_retriever.search(query, k=k_initial)
        )
        
        # Convert to rankings
        rankings = [
            [{"id": f"v_{i}", "document": r["document"], "score": r["score"]}
             for i, r in enumerate(vector_results)],
            [{"id": f"b_{i}", "document": r["document"], "score": r["score"]}
             for i, r in enumerate(bm25_results)]
        ]
        
        # Fuse using RRF
        fused = reciprocal_rank_fusion(rankings, k=60)
        
        # Get top candidates for reranking
        candidates = fused[:k_rerank]
        
        # Rerank with cross-encoder
        reranked = self.fast_reranker.rerank(
            query=query,
            documents=[c["document"] for c in candidates],
            top_k=k_final
        )
        
        # Merge results
        doc_lookup = {c["document"]: c for c in candidates}
        
        final_results = []
        for rank, item in enumerate(reranked, 1):
            original = doc_lookup[item["document"]]
            final_results.append({
                "document": item["document"],
                "content": item.get("content", item["document"][:200]),
                "rerank_score": item["score"],
                "original_score": original.get("score", 0),
                "rank": rank,
                "metadata": original.get("metadata", {})
            })
        
        return final_results
    
    async def retrieve_with_fallback(
        self,
        query: str,
        fallback_threshold: float = 0.3
    ) -> List[dict]:
        """
        Retrieve với fallback to accurate reranker if needed.
        """
        results = await self.retrieve(query)
        
        # If top result has low score, use accurate reranker
        if results and results[0]["rerank_score"] < fallback_threshold:
            # Re-rerank with more accurate model
            candidates = results[:20]
            
            reranked = self.accurate_reranker.rerank(
                query=query,
                documents=[c["document"] for c in candidates],
                top_k=10
            )
            
            # Update results
            for i, item in enumerate(reranked):
                for result in results:
                    if result["document"] == item["document"]:
                        result["rerank_score"] = item["score"]
                        result["rank"] = i + 1
                        break
            
            # Re-sort
            results.sort(key=lambda x: x["rerank_score"], reverse=True)
        
        return results
```

### Example 2: Adaptive Batch Reranking

```python
class AdaptiveBatchReranker:
    """
    Batch reranking với adaptive batching.
    """
    
    def __init__(self, reranker):
        self.reranker = reranker
    
    async def rerank_batch(
        self,
        queries: List[str],
        documents: List[List[str]],
        top_k: int = 10
    ) -> List[List[dict]]:
        """
        Rerank multiple query-result pairs.
        
        Args:
            queries: List of queries
            documents: List of document lists (one per query)
            top_k: Number of results to return per query
        """
        results = []
        
        for query, docs in zip(queries, documents):
            if not docs:
                results.append([])
                continue
            
            # Batch similar queries together
            reranked = self.reranker.rerank(
                query=query,
                documents=docs,
                top_k=top_k
            )
            
            results.append(reranked)
        
        return results
    
    async def rerank_streaming(
        self,
        query: str,
        document_stream,
        batch_size: int = 50,
        top_k: int = 10
    ) -> List[dict]:
        """
        Rerank from a streaming document source.
        """
        batch = []
        results = []
        
        async for doc in document_stream:
            batch.append(doc)
            
            if len(batch) >= batch_size:
                reranked = self.reranker.rerank(
                    query=query,
                    documents=batch,
                    top_k=top_k
                )
                results.extend(reranked)
                batch = []
        
        # Process remaining batch
        if batch:
            reranked = self.reranker.rerank(
                query=query,
                documents=batch,
                top_k=top_k
            )
            results.extend(reranked)
        
        # Sort and return top-k
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
```

### Example 3: Evaluation of Reranking

```python
class RerankingEvaluator:
    """
    Evaluate reranking performance.
    """
    
    def __init__(self):
        self.metrics = []
    
    def evaluate(
        self,
        predictions: List[dict],
        ground_truth: List[dict]
    ) -> dict:
        """
        Evaluate reranking results.
        
        Args:
            predictions: List of predicted rankings
            ground_truth: List of ground truth rankings
        """
        metrics = {}
        
        # NDCG@K
        for k in [1, 3, 5, 10]:
            ndcg = self._ndcg_at_k(predictions, ground_truth, k)
            metrics[f"ndcg@{k}"] = ndcg
        
        # MRR (Mean Reciprocal Rank)
        metrics["mrr"] = self._mrr(predictions, ground_truth)
        
        # Precision@K
        for k in [1, 3, 5, 10]:
            precision = self._precision_at_k(predictions, ground_truth, k)
            metrics[f"precision@{k}"] = precision
        
        # Recall@K
        for k in [1, 3, 5, 10]:
            recall = self._recall_at_k(predictions, ground_truth, k)
            metrics[f"recall@{k}"] = recall
        
        return metrics
    
    def _ndcg_at_k(
        self,
        predictions: List[dict],
        ground_truth: List[dict],
        k: int
    ) -> float:
        """Calculate NDCG@K."""
        # Create relevance mapping from ground truth
        relevance = {gt["id"]: gt.get("relevance", 1) for gt in ground_truth}
        
        # Calculate DCG
        dcg = 0
        for i, pred in enumerate(predictions[:k], 1):
            rel = relevance.get(pred.get("id", pred["document"]), 0)
            dcg += rel / np.log2(i + 1)
        
        # Calculate IDCG
        ideal_relevance = sorted(
            [r.get("relevance", 1) for r in ground_truth],
            reverse=True
        )
        idcg = sum(
            rel / np.log2(i + 1)
            for i, rel in enumerate(ideal_relevance[:k], 1)
        )
        
        return dcg / idcg if idcg > 0 else 0
    
    def _mrr(
        self,
        predictions: List[dict],
        ground_truth: List[dict]
    ) -> float:
        """Calculate Mean Reciprocal Rank."""
        relevant_ids = {gt["id"] for gt in ground_truth if gt.get("relevance", 1) > 0}
        
        for i, pred in enumerate(predictions, 1):
            pred_id = pred.get("id", pred.get("document"))
            if pred_id in relevant_ids:
                return 1.0 / i
        
        return 0
    
    def _precision_at_k(
        self,
        predictions: List[dict],
        ground_truth: List[dict],
        k: int
    ) -> float:
        """Calculate Precision@K."""
        relevant_ids = {gt["id"] for gt in ground_truth if gt.get("relevance", 1) > 0}
        
        predicted_relevant = sum(
            1 for p in predictions[:k]
            if p.get("id", p.get("document")) in relevant_ids
        )
        
        return predicted_relevant / k if k > 0 else 0
    
    def _recall_at_k(
        self,
        predictions: List[dict],
        ground_truth: List[dict],
        k: int
    ) -> float:
        """Calculate Recall@K."""
        relevant_ids = {gt["id"] for gt in ground_truth if gt.get("relevance", 1) > 0}
        total_relevant = len(relevant_ids)
        
        if total_relevant == 0:
            return 0
        
        predicted_relevant = sum(
            1 for p in predictions[:k]
            if p.get("id", p.get("document")) in relevant_ids
        )
        
        return predicted_relevant / total_relevant
```

## References

1. **Cross-Encoders**: https://www.sbert.net/docs/training/overview.html
2. **ColBERT**: https://arxiv.org/abs/2004.12832
3. **RRF**: https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
4. **NDCG**: https://en.wikipedia.org/wiki/Discounted_cumulative_gain
5. **Cursor Enterprise Framework - RAG Rules**: `.cursor/rules/rag.mdc`
