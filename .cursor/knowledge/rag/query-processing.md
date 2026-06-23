---
title: "Query Processing"
description: "Hướng dẫn về query processing: query rewriting, query expansion, HyDE và multi-query retrieval"
tags: ["query-processing", "hyde", "query-expansion", "query-rewriting", "retrieval"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Query Processing

## Tổng Quan

Query processing là bước quan trọng trong RAG pipeline, biến đổi user query thành dạng tối ưu để retrieval. User queries thường ngắn, ambiguous, hoặc thiếu context, trong khi retrieval systems cần precise representations để tìm relevant documents.

Các techniques như query rewriting, query expansion, và HyDE (Hypothetical Document Embeddings) giúp bridge gap giữa user intent và retrieval system capabilities.

Việc xử lý query tốt có thể cải thiện đáng kể retrieval quality mà không cần thay đổi underlying retrieval system.

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức toàn diện về query processing:

Đầu tiên, chúng ta sẽ tìm hiểu query rewriting - biến đổi query thành dạng tốt hơn.

Thứ hai, tài liệu hướng dẫn query expansion - mở rộng query với related terms.

Thứ ba, chúng ta sẽ đề cập đến HyDE - sử dụng hypothetical documents cho retrieval.

Cuối cùng, tài liệu cung cấp multi-query retrieval và các best practices.

## Key Concepts

### 1. Query Analysis

```python
from dataclasses import dataclass
from typing import List, Optional
import re

@dataclass
class QueryAnalysis:
    """Analysis of a user query."""
    original_query: str
    query_type: str  # factual, conversational, complex
    key_entities: List[str]
    intent: str  # lookup, comparison, explanation, etc.
    complexity_score: float
    is_ambiguous: bool
    suggested_expansions: List[str]

class QueryAnalyzer:
    """
    Analyze query characteristics to guide processing.
    """
    
    def __init__(self, nlp_model=None):
        self.nlp = nlp_model
    
    def analyze(self, query: str) -> QueryAnalysis:
        """Analyze a query."""
        return QueryAnalysis(
            original_query=query,
            query_type=self._classify_query_type(query),
            key_entities=self._extract_entities(query),
            intent=self._classify_intent(query),
            complexity_score=self._estimate_complexity(query),
            is_ambiguous=self._check_ambiguity(query),
            suggested_expansions=self._suggest_expansions(query)
        )
    
    def _classify_query_type(self, query: str) -> str:
        """Classify query type."""
        query_lower = query.lower()
        
        # Question patterns
        if query_lower.startswith(("who", "what", "when", "where", "why", "how")):
            if any(word in query_lower for word in ["define", "meaning", "explain"]):
                return "explanation"
            elif any(word in query_lower for word in ["compare", "difference"]):
                return "comparison"
            elif any(word in query_lower for word in ["history", "origin", "invented"]):
                return "factual"
            else:
                return "lookup"
        
        # Command patterns
        if query_lower.startswith(("find", "search", "show", "get", "list")):
            return "search"
        
        # Topic patterns
        if "?" not in query:
            return "topic"
        
        return "general"
    
    def _extract_entities(self, query: str) -> List[str]:
        """Extract named entities from query."""
        entities = []
        
        # Simple regex-based extraction
        # In production, use spaCy or similar
        patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Proper nouns
            r'\b\w+\s+\d{4}\b',  # Year references
            r'\b\d+(?:\.\d+)?\s*(?:percent|%)?\b',  # Numbers
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, query)
            entities.extend(matches)
        
        return list(set(entities))
    
    def _classify_intent(self, query: str) -> str:
        """Classify user intent."""
        query_lower = query.lower()
        
        intents = {
            "lookup": ["what is", "who is", "where is", "find", "search"],
            "comparison": ["compare", "difference", "versus", "vs", "better"],
            "explanation": ["how does", "why does", "explain", "describe"],
            "instructions": ["how to", "steps to", "guide to"],
            "list": ["list", "show all", "what are", "names of"]
        }
        
        for intent, keywords in intents.items():
            if any(kw in query_lower for kw in keywords):
                return intent
        
        return "general"
    
    def _estimate_complexity(self, query: str) -> float:
        """Estimate query complexity (0-1)."""
        score = 0.0
        
        # Length factor
        words = len(query.split())
        score += min(words / 20, 0.3)
        
        # Multiple clauses
        if any(c in query for c in [",", " and ", " but ", " or "]):
            score += 0.2
        
        # Question complexity
        if query.count("?") > 1 or " and " in query.lower():
            score += 0.2
        
        # Technical terms
        technical_terms = ["implement", "optimize", "configure", "architecture"]
        if any(term in query.lower() for term in technical_terms):
            score += 0.3
        
        return min(score, 1.0)
    
    def _check_ambiguity(self, query: str) -> bool:
        """Check if query is ambiguous."""
        # Short queries are often ambiguous
        if len(query.split()) < 3:
            return True
        
        # Pronouns without context
        if any(word in query.lower() for word in ["it", "they", "this", "that"]):
            return True
        
        # Vague terms
        vague_terms = ["stuff", "things", "something", "anything"]
        if any(term in query.lower() for term in vague_terms):
            return True
        
        return False
    
    def _suggest_expansions(self, query: str) -> List[str]:
        """Suggest query expansions."""
        expansions = []
        
        # Technical expansions
        if any(term in query.lower() for term in ["ai", "ml", "ml"]):
            expansions.extend(["machine learning", "artificial intelligence"])
        
        # Domain expansions
        if any(term in query.lower() for term in ["python", "javascript"]):
            expansions.append("programming")
        
        return expansions
```

## Query Rewriting

### 1. LLM-based Rewriting

```python
class LLMQueryRewriter:
    """
    Rewrite queries using LLM for better retrieval.
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
        
        self.rewrite_prompt = """
Rewrite the following query to be more effective for semantic search.
The rewritten query should:
1. Be clear and specific
2. Include relevant context
3. Use technical terms if appropriate
4. Be self-contained (don't rely on external context)

Original Query: {query}

Rewritten Query:"""
    
    async def rewrite(self, query: str) -> str:
        """Rewrite query using LLM."""
        prompt = self.rewrite_prompt.format(query=query)
        response = await self.llm.complete(prompt)
        
        # Extract rewritten query
        rewritten = response.strip()
        
        return rewritten
    
    async def rewrite_for_context(
        self,
        query: str,
        conversation_history: List[dict] = None
    ) -> str:
        """Rewrite query with conversation context."""
        if not conversation_history:
            return await self.rewrite(query)
        
        # Build context from history
        context = "\n".join([
            f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
            for m in conversation_history[-3:]
        ])
        
        prompt = f"""
Given the following conversation context, rewrite the current query 
to be clear and self-contained for semantic search.

Conversation:
{context}

Current Query: {query}

Rewritten Query:"""
        
        response = await self.llm.complete(prompt)
        return response.strip()
```

### 2. Subquery Decomposition

```python
class SubqueryDecomposer:
    """
    Decompose complex queries into simpler subqueries.
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def decompose(self, query: str) -> List[str]:
        """Decompose query into subqueries."""
        prompt = f"""
Decompose the following complex query into simpler subqueries that can be 
answered independently. Each subquery should focus on one aspect.

Original Query: {query}

Subqueries:"""
        
        response = await self.llm.complete(prompt)
        
        # Parse subqueries from response
        subqueries = [
            line.strip().lstrip("0123456789.-) ")
            for line in response.split("\n")
            if line.strip() and (line[0].isdigit() or line[0] == "-")
        ]
        
        return subqueries if subqueries else [query]
    
    async def decompose_and_expand(
        self,
        query: str
    ) -> List[dict]:
        """Decompose and expand each subquery."""
        subqueries = await self.decompose(query)
        
        expanded = []
        for sq in subqueries:
            expanded.append({
                "subquery": sq,
                "expanded_queries": await self._expand_subquery(sq)
            })
        
        return expanded
    
    async def _expand_subquery(self, subquery: str) -> List[str]:
        """Expand a single subquery."""
        prompt = f"""
Generate 3 alternative phrasings for the following query that capture 
the same meaning but use different words.

Query: {subquery}

Alternatives:"""
        
        response = await self.llm.complete(prompt)
        
        alternatives = [
            line.strip().lstrip("0123456789.-) ")
            for line in response.split("\n")
            if line.strip()
        ]
        
        return alternatives if alternatives else [subquery]
```

### 3. Query Type-specific Rewriting

```python
class TypedQueryRewriter:
    """
    Rewrite queries based on their type.
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
        self.analyzer = QueryAnalyzer()
    
    async def rewrite(self, query: str) -> str:
        """Rewrite query based on its type."""
        analysis = self.analyzer.analyze(query)
        
        if analysis.query_type == "comparison":
            return await self._rewrite_comparison(query)
        elif analysis.query_type == "explanation":
            return await self._rewrite_explanation(query)
        elif analysis.query_type == "lookup":
            return await self._rewrite_lookup(query)
        else:
            return await self._rewrite_general(query)
    
    async def _rewrite_comparison(self, query: str) -> str:
        """Rewrite comparison queries."""
        prompt = f"""
Rewrite this comparison query to include both items being compared 
and the aspect of comparison.

Query: {query}

Rewritten:"""
        return (await self.llm.complete(prompt)).strip()
    
    async def _rewrite_explanation(self, query: str) -> str:
        """Rewrite explanation queries."""
        prompt = f"""
Rewrite this explanation query to be more specific about what 
aspect needs to be explained.

Query: {query}

Rewritten:"""
        return (await self.llm.complete(prompt)).strip()
    
    async def _rewrite_lookup(self, query: str) -> str:
        """Rewrite lookup queries."""
        prompt = f"""
Rewrite this lookup query to include specific details that would 
help find the exact answer.

Query: {query}

Rewritten:"""
        return (await self.llm.complete(prompt)).strip()
    
    async def _rewrite_general(self, query: str) -> str:
        """General query rewriting."""
        rewriter = LLMQueryRewriter(self.llm)
        return await rewriter.rewrite(query)
```

## Query Expansion

### 1. Thesaurus-based Expansion

```python
class ThesaurusExpander:
    """
    Expand queries using synonyms and related terms.
    """
    
    def __init__(self, thesaurus_path: str = None):
        # Simple built-in thesaurus
        self.thesaurus = {
            "learn": ["understand", "comprehend", "grasp", "study"],
            "fast": ["quick", "rapid", "swift", "speedy"],
            "good": ["high quality", "excellent", "effective", "beneficial"],
            "bad": ["poor", "ineffective", "negative", "harmful"],
            "build": ["create", "develop", "construct", "design"],
            "find": ["discover", "locate", "identify", "search for"],
            "explain": ["describe", "clarify", "illustrate", "elaborate"],
            "important": ["significant", "crucial", "essential", "vital"],
        }
    
    def expand(self, query: str, max_terms: int = 5) -> List[str]:
        """Expand query with synonyms."""
        words = query.lower().split()
        expanded = []
        
        for word in words:
            if word in self.thesaurus:
                synonyms = self.thesaurus[word][:max_terms]
                expanded.extend(synonyms)
        
        # Add original words
        expanded.extend(words)
        
        # Create expanded query strings
        queries = [
            query,
            " ".join(expanded[:len(words) * 2])
        ]
        
        return queries


class WordNetExpander:
    """
    Expand queries using WordNet synonyms.
    """
    
    def __init__(self):
        try:
            import nltk
            from nltk.corpus import wordnet
            nltk.download('wordnet', quiet=True)
            nltk.download('punkt', quiet=True)
            self.wordnet = wordnet
        except ImportError:
            self.wordnet = None
    
    def expand(self, query: str, max_synsets: int = 3) -> List[str]:
        """Expand query with WordNet synonyms."""
        if not self.wordnet:
            return [query]
        
        words = query.split()
        expansions = []
        
        for word in words:
            synsets = self.wordnet.synsets(word)
            
            for synset in synsets[:max_synsets]:
                for lemma in synset.lemmas()[:2]:
                    expansions.append(lemma.name().replace("_", " "))
        
        # Create expanded queries
        if expansions:
            return [
                query,
                query + " " + " ".join(expanded[:10])
            ]
        
        return [query]
```

### 2. Embedding-based Expansion

```python
class EmbeddingExpander:
    """
    Expand queries using similar terms from embedding space.
    """
    
    def __init__(self, embeddings_model, top_k: int = 5):
        self.model = embeddings_model
        self.top_k = top_k
    
    async def expand(self, query: str) -> List[str]:
        """Find similar terms and expand query."""
        # Get query embedding
        query_embedding = await self.model.embed(query)
        
        # This would typically search against a term index
        # For now, return original query
        return [query]
    
    async def expand_with_context(
        self,
        query: str,
        context_docs: List[str] = None
    ) -> List[str]:
        """Expand query using context documents."""
        if not context_docs:
            return [query]
        
        # Get query embedding
        query_emb = await self.model.embed(query)
        
        # Get document embeddings
        doc_embs = await self.model.embed_batch(context_docs)
        
        # Find most relevant terms from documents
        # (simplified - actual implementation would extract key terms)
        expanded_terms = []
        
        for doc in context_docs[:5]:
            # Extract important terms (simplified)
            words = doc.split()[:20]
            expanded_terms.extend(words)
        
        # Create expanded query
        expanded_query = query + " " + " ".join(list(set(expanded_terms))[:10])
        
        return [query, expanded_query]
```

### 3. Generated Expansion

```python
class LLMExpander:
    """
    Expand queries using LLM to generate related terms.
    """
    
    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def expand(self, query: str) -> List[str]:
        """Generate expanded versions of query."""
        prompt = f"""
Generate alternative versions of this search query that cover the same 
topic from different angles. Include technical terms, related concepts, 
and alternative phrasings.

Query: {query}

Alternative Queries:"""
        
        response = await self.llm.complete(prompt)
        
        # Parse alternatives
        alternatives = [
            line.strip().lstrip("0123456789.-) ")
            for line in response.split("\n")
            if line.strip()
        ]
        
        return [query] + alternatives[:5]
    
    async def expand_with_hyponyms(
        self,
        query: str
    ) -> List[str]:
        """Expand with hyponyms (specific terms)."""
        prompt = f"""
For this query, list specific examples, types, and instances that 
are related to the main concepts.

Query: {query}

Specific Examples:"""
        
        response = await self.llm.complete(prompt)
        
        # Parse and create expanded query
        specific = [
            line.strip().lstrip("-* ")
            for line in response.split("\n")
            if line.strip()
        ]
        
        if specific:
            expanded = query + " " + " ".join(specific[:10])
            return [query, expanded]
        
        return [query]
```

## HyDE (Hypothetical Document Embeddings)

### 1. Basic HyDE Implementation

```python
class HyDERetriever:
    """
    HyDE: Hypothetical Document Embeddings.
    
    1. Generate hypothetical document(s) that would answer the query
    2. Embed the hypothetical document(s)
    3. Use those embeddings to retrieve real documents
    """
    
    def __init__(
        self,
        llm_client,
        embedding_model,
        vector_store
    ):
        self.llm = llm_client
        self.embedding = embedding_model
        self.vector_store = vector_store
    
    async def retrieve(
        self,
        query: str,
        num_hypothetical: int = 3,
        k_per_hypothetical: int = 20,
        final_k: int = 10
    ) -> List[dict]:
        """
        Retrieve using HyDE approach.
        """
        # Step 1: Generate hypothetical documents
        hypothetical_docs = await self._generate_hypothetical_docs(
            query,
            n=num_hypothetical
        )
        
        # Step 2: Embed hypothetical documents
        hypothetical_embeddings = await self.embedding.embed_batch(
            hypothetical_docs
        )
        
        # Step 3: Retrieve using each hypothetical embedding
        all_results = []
        
        for i, (doc, embedding) in enumerate(
            zip(hypothetical_docs, hypothetical_embeddings)
        ):
            results = await self.vector_store.search_by_embedding(
                embedding=embedding,
                k=k_per_hypothetical
            )
            
            for result in results:
                result["hypothetical_doc_index"] = i
                result["hypothetical_doc"] = doc
            
            all_results.extend(results)
        
        # Step 4: Deduplicate and rank
        seen = set()
        unique_results = []
        
        for result in sorted(
            all_results,
            key=lambda x: x["score"],
            reverse=True
        ):
            doc_id = result.get("id", result["document"])
            
            if doc_id not in seen:
                seen.add(doc_id)
                unique_results.append(result)
                
                if len(unique_results) >= final_k:
                    break
        
        return unique_results
    
    async def _generate_hypothetical_docs(
        self,
        query: str,
        n: int = 3
    ) -> List[str]:
        """Generate n hypothetical documents that answer the query."""
        prompt = f"""
Generate {n} hypothetical document excerpts that would provide a good 
answer to the following query. Each document should be 2-3 paragraphs 
and explain the concept thoroughly.

Query: {query}

Hypothetical Documents:"""
        
        response = await self.llm.complete(prompt)
        
        # Parse documents (split by common delimiters)
        docs = []
        
        # Try to split by numbered sections
        for i in range(1, n + 1):
            # Look for section headers
            patterns = [
                f"Document {i}:",
                f"Document {i}\n",
                f"{i}. ",
            ]
            
            for pattern in patterns:
                if pattern in response:
                    parts = response.split(pattern)
                    if len(parts) > i:
                        docs.append(parts[i].strip())
                        break
        
        # If parsing failed, split roughly
        if len(docs) < n:
            sections = response.split("\n\n")
            docs = [s.strip() for s in sections if len(s.strip()) > 100][:n]
        
        # Ensure we have n documents
        while len(docs) < n:
            docs.append(response)
        
        return docs[:n]
```

### 2. HyDE with Diverse Hypotheses

```python
class DiverseHyDE:
    """
    HyDE with diverse hypothetical documents from different perspectives.
    """
    
    def __init__(self, llm_client, embedding_model, vector_store):
        self.llm = llm_client
        self.embedding = embedding_model
        self.vector_store = vector_store
    
    async def retrieve(
        self,
        query: str,
        perspectives: List[str] = None,
        k_per_perspective: int = 10,
        final_k: int = 10
    ) -> List[dict]:
        """
        Retrieve using diverse perspectives.
        """
        if perspectives is None:
            perspectives = [
                "technical explanation",
                "practical implementation",
                "beginner's guide",
                "expert analysis"
            ]
        
        # Generate hypothetical docs from each perspective
        all_results = []
        
        for perspective in perspectives:
            docs = await self._generate_perspective_doc(query, perspective)
            
            # Embed and retrieve
            embedding = await self.embedding.embed(docs)
            
            results = await self.vector_store.search_by_embedding(
                embedding=embedding,
                k=k_per_perspective
            )
            
            for result in results:
                result["perspective"] = perspective
            
            all_results.extend(results)
        
        # Fuse and deduplicate
        return self._fuse_results(all_results, final_k)
    
    async def _generate_perspective_doc(
        self,
        query: str,
        perspective: str
    ) -> str:
        """Generate hypothetical document from a specific perspective."""
        prompt = f"""
Write a hypothetical document excerpt about the following topic 
from the perspective of a {perspective}. The document should be 
2 paragraphs and explain the concept thoroughly from this viewpoint.

Topic: {query}

Document:"""
        
        return (await self.llm.complete(prompt)).strip()
    
    def _fuse_results(
        self,
        results: List[dict],
        k: int
    ) -> List[dict]:
        """Fuse results from multiple perspectives."""
        # Group by document
        doc_scores = {}
        
        for result in results:
            doc_id = result.get("id", result["document"])
            
            if doc_id not in doc_scores:
                doc_scores[doc_id] = {
                    "document": result["document"],
                    "content": result.get("content", ""),
                    "metadata": result.get("metadata", {}),
                    "perspectives": [],
                    "max_score": 0,
                    "avg_score": 0,
                    "scores": []
                }
            
            doc_scores[doc_id]["scores"].append(result["score"])
            doc_scores[doc_id]["perspectives"].append(
                result.get("perspective", "default")
            )
            doc_scores[doc_id]["max_score"] = max(
                doc_scores[doc_id]["max_score"],
                result["score"]
            )
        
        # Calculate aggregate scores
        fused = []
        for doc_id, data in doc_scores.items():
            data["avg_score"] = sum(data["scores"]) / len(data["scores"])
            
            # Combined score: max + average (rewards documents from multiple perspectives)
            data["fused_score"] = data["max_score"] + 0.5 * data["avg_score"]
            
            fused.append(data)
        
        # Sort and return top-k
        fused.sort(key=lambda x: x["fused_score"], reverse=True)
        
        return [
            {
                "document": d["document"],
                "content": d["content"],
                "metadata": d["metadata"],
                "perspectives": d["perspectives"],
                "max_score": d["max_score"],
                "avg_score": d["avg_score"],
                "fused_score": d["fused_score"]
            }
            for d in fused[:k]
        ]
```

## Multi-Query Retrieval

### 1. Parallel Query Execution

```python
class MultiQueryRetriever:
    """
    Execute multiple query variations and fuse results.
    """
    
    def __init__(
        self,
        vector_store,
        query_rewriter,
        fusion_method: str = "rrf"
    ):
        self.vector_store = vector_store
        self.rewriter = query_rewriter
        self.fusion_method = fusion_method
    
    async def retrieve(
        self,
        query: str,
        num_variations: int = 5,
        k_per_variation: int = 20,
        final_k: int = 10
    ) -> List[dict]:
        """
        Retrieve using multiple query variations.
        """
        # Generate query variations
        variations = await self._generate_variations(
            query,
            num_variations
        )
        
        # Execute all variations in parallel
        tasks = [
            self.vector_store.search(query=q, k=k_per_variation)
            for q in variations
        ]
        
        results_per_query = await asyncio.gather(*tasks)
        
        # Convert to rankings for fusion
        rankings = []
        for results in results_per_query:
            ranking = [
                {
                    "id": r.get("id", i),
                    "document": r["document"],
                    "score": r.get("score", 1.0 / (i + 1))
                }
                for i, r in enumerate(results)
            ]
            rankings.append(ranking)
        
        # Fuse results
        if self.fusion_method == "rrf":
            fused = self._reciprocal_rank_fusion(rankings)
        elif self.fusion_method == "diverse":
            fused = self._diverse_fusion(rankings)
        else:
            fused = self._reciprocal_rank_fusion(rankings)
        
        return fused[:final_k]
    
    async def _generate_variations(
        self,
        query: str,
        num: int
    ) -> List[str]:
        """Generate query variations."""
        variations = [query]
        
        # Use rewriter
        expanded = await self.rewriter.expand(query)
        variations.extend(expanded[1:num])
        
        # Ensure we have enough variations
        while len(variations) < num:
            variations.append(query)
        
        return variations[:num]
    
    def _reciprocal_rank_fusion(
        self,
        rankings: List[List[dict]],
        k: int = 60
    ) -> List[dict]:
        """RRF fusion."""
        scores = {}
        
        for ranking in rankings:
            for rank, item in enumerate(ranking, 1):
                item_id = item["id"]
                
                if item_id not in scores:
                    scores[item_id] = {
                        **item,
                        "rrf_score": 0
                    }
                
                scores[item_id]["rrf_score"] += 1.0 / (k + rank)
        
        return sorted(
            scores.values(),
            key=lambda x: x["rrf_score"],
            reverse=True
        )
    
    def _diverse_fusion(
        self,
        rankings: List[List[dict]],
        k: int = 10
    ) -> List[dict]:
        """Diversified fusion using MMR-like approach."""
        selected = []
        remaining = {}
        
        # Collect all items with their max scores
        for ranking in rankings:
            for rank, item in enumerate(ranking, 1):
                item_id = item["id"]
                
                if item_id not in remaining:
                    remaining[item_id] = {
                        **item,
                        "max_score": 0,
                        "scores": []
                    }
                
                remaining[item_id]["scores"].append(1.0 / (rank + 1))
                remaining[item_id]["max_score"] = max(
                    remaining[item_id]["max_score"],
                    item["score"]
                )
        
        # Select diverse items
        while selected and len(selected) < k:
            best_item = None
            best_combined = -float("inf")
            
            for item_id, item in remaining.items():
                # Relevance score
                relevance = item["max_score"]
                
                # Diversity bonus (based on similarity to selected)
                diversity = 0
                for sel in selected:
                    sim = self._calculate_similarity(
                        item.get("embedding", []),
                        sel.get("embedding", [])
                    )
                    diversity += (1 - sim)
                
                # Combined score
                combined = relevance + 0.5 * diversity
                
                if combined > best_combined:
                    best_combined = combined
                    best_item = item_id
            
            if best_item:
                selected.append(remaining.pop(best_item))
            else:
                break
        
        return selected
    
    def _calculate_similarity(
        self,
        emb1: List[float],
        emb2: List[float]
    ) -> float:
        """Calculate cosine similarity."""
        import numpy as np
        
        if not emb1 or not emb2:
            return 0
        
        a = np.array(emb1)
        b = np.array(emb2)
        
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

### 2. Query Routing

```python
class QueryRouter:
    """
    Route queries to specialized retrievers.
    """
    
    def __init__(self):
        self.routes = {
            "code": {
                "keywords": ["code", "function", "class", "api", "implement"],
                "retriever": None  # Set at runtime
            },
            "technical": {
                "keywords": ["architecture", "system", "database", "server"],
                "retriever": None
            },
            "factual": {
                "keywords": ["who", "what", "when", "where", "number"],
                "retriever": None
            },
            "general": {
                "keywords": [],
                "retriever": None  # Default retriever
            }
        }
    
    def route(self, query: str) -> str:
        """Determine which retriever to use."""
        query_lower = query.lower()
        
        for category, config in self.routes.items():
            if category == "general":
                continue
            
            keywords = config["keywords"]
            
            if any(kw in query_lower for kw in keywords):
                return category
        
        return "general"
    
    async def retrieve(
        self,
        query: str,
        retrievers: Dict[str, object],
        k: int = 10
    ) -> List[dict]:
        """Route and retrieve."""
        # Determine route
        category = self.route(query)
        
        # Get appropriate retriever
        retriever = retrievers.get(category, retrievers.get("general"))
        
        if retriever:
            return await retriever.search(query=query, k=k)
        
        return []
```

## Best Practices

### 1. Query Processing Pipeline

```python
class CompleteQueryProcessingPipeline:
    """
    Full query processing pipeline.
    """
    
    def __init__(
        self,
        analyzer: QueryAnalyzer,
        rewriter: TypedQueryRewriter,
        expander: LLMExpander,
        retriever: MultiQueryRetriever,
        reranker: object = None
    ):
        self.analyzer = analyzer
        self.rewriter = rewriter
        self.expander = expander
        self.retriever = retriever
        self.reranker = reranker
    
    async def process(
        self,
        query: str,
        conversation_history: List[dict] = None,
        k_initial: int = 50,
        k_rerank: int = 20,
        k_final: int = 10
    ) -> dict:
        """
        Complete query processing pipeline.
        """
        # Step 1: Analyze query
        analysis = self.analyzer.analyze(query)
        
        # Step 2: Rewrite query (if needed)
        rewritten = query
        if analysis.is_ambiguous or analysis.complexity_score > 0.5:
            rewritten = await self.rewriter.rewrite(query)
        
        # Step 3: Expand query
        expanded = await self.expander.expand(rewritten)
        
        # Step 4: Multi-query retrieval
        if len(expanded) > 1:
            results = await self.retriever.retrieve(
                query=rewritten,
                num_variations=len(expanded),
                k_per_variation=k_initial // len(expanded),
                final_k=k_initial
            )
        else:
            results = await self.retriever.retrieve(
                query=rewritten,
                k_initial=k_initial,
                final_k=k_initial
            )
        
        # Step 5: Rerank (if available)
        if self.reranker and results:
            reranked = self.reranker.rerank(
                query=rewritten,
                documents=[r["document"] for r in results],
                top_k=k_rerank
            )
            
            # Merge reranked scores
            doc_lookup = {r["document"]: r for r in results}
            
            final_results = []
            for i, item in enumerate(reranked, 1):
                original = doc_lookup[item["document"]]
                final_results.append({
                    **original,
                    "rerank_score": item["score"],
                    "rank": i
                })
            
            results = final_results
        
        return {
            "original_query": query,
            "rewritten_query": rewritten,
            "expanded_queries": expanded,
            "analysis": analysis,
            "results": results[:k_final]
        }
```

### 2. Caching Rewritten Queries

```python
class CachedQueryProcessor:
    """
    Cache processed queries for efficiency.
    """
    
    def __init__(self, base_processor, cache_storage):
        self.processor = base_processor
        self.cache = cache_storage
    
    async def process(self, query: str, **kwargs) -> dict:
        """Process query with caching."""
        # Check cache
        cache_key = self._generate_cache_key(query)
        cached = await self.cache.get(cache_key)
        
        if cached:
            return cached
        
        # Process query
        result = await self.processor.process(query, **kwargs)
        
        # Cache result
        await self.cache.set(cache_key, result, ttl=3600)
        
        return result
    
    def _generate_cache_key(self, query: str) -> str:
        """Generate cache key for query."""
        import hashlib
        return hashlib.md5(query.lower().encode()).hexdigest()
```

### 3. Fallback Strategy

```python
class RobustQueryProcessor:
    """
    Query processor with fallback strategies.
    """
    
    def __init__(self, primary_retriever, fallback_retriever):
        self.primary = primary_retriever
        self.fallback = fallback_retriever
    
    async def process(
        self,
        query: str,
        k: int = 10
    ) -> dict:
        """
        Process with automatic fallback.
        """
        try:
            # Try primary retriever
            results = await self.primary.search(query=query, k=k)
            
            if len(results) >= k // 2:
                return {
                    "results": results,
                    "source": "primary"
                }
            
            # Fallback if primary returns too few results
            results = await self.fallback.search(query=query, k=k)
            
            return {
                "results": results,
                "source": "fallback"
            }
        
        except Exception as e:
            # Ultimate fallback: use simple embedding search
            results = await self._simple_search(query, k)
            
            return {
                "results": results,
                "source": "emergency_fallback",
                "error": str(e)
            }
```

## Examples

### Example 1: Production Query Processing Service

```python
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    conversation_id: str = None
    k: int = 10
    use_reranking: bool = True

class QueryResponse(BaseModel):
    results: List[dict]
    metadata: dict

# Initialize components
query_processor = CompleteQueryProcessingPipeline(...)
cache = RedisCache(...)
metrics = MetricsCollector(...)

@app.post("/search", response_model=QueryResponse)
async def search(request: QueryRequest):
    """Search endpoint."""
    start_time = time.time()
    
    try:
        # Get conversation history if provided
        history = []
        if request.conversation_id:
            history = await cache.get_conversation(request.conversation_id)
        
        # Process query
        result = await query_processor.process(
            query=request.query,
            conversation_history=history,
            k_final=request.k
        )
        
        # Record metrics
        metrics.record(
            "query_processing_time",
            time.time() - start_time,
            tags={"status": "success"}
        )
        
        return QueryResponse(
            results=result["results"],
            metadata={
                "original_query": result["original_query"],
                "rewritten_query": result["rewritten_query"],
                "analysis": {
                    "query_type": result["analysis"].query_type,
                    "complexity": result["analysis"].complexity_score
                }
            }
        )
    
    except Exception as e:
        metrics.record(
            "query_processing_time",
            time.time() - start_time,
            tags={"status": "error"}
        )
        raise HTTPException(status_code=500, detail=str(e))
```

### Example 2: Batch Query Processing

```python
class BatchQueryProcessor:
    """
    Process multiple queries efficiently.
    """
    
    def __init__(self, processor):
        self.processor = processor
    
    async def process_batch(
        self,
        queries: List[str],
        max_concurrent: int = 5
    ) -> List[dict]:
        """
        Process multiple queries with concurrency limit.
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_with_limit(query):
            async with semaphore:
                return await self.processor.process(query)
        
        tasks = [process_with_limit(q) for q in queries]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed = []
        for query, result in zip(queries, results):
            if isinstance(result, Exception):
                processed.append({
                    "query": query,
                    "error": str(result),
                    "results": []
                })
            else:
                processed.append(result)
        
        return processed
```

### Example 3: Query Processing Monitoring

```python
class QueryProcessingMonitor:
    """
    Monitor query processing performance.
    """
    
    def __init__(self):
        self.metrics = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "rewrite_rate": 0,
            "avg_processing_time": 0,
            "expansion_rate": 0
        }
    
    def record(self, query: str, result: dict, processing_time: float):
        """Record query processing metrics."""
        self.metrics["total_queries"] += 1
        self.metrics["successful_queries"] += 1
        
        # Track rewrite rate
        if result.get("rewritten_query") != query:
            self.metrics["rewrite_rate"] += 1
        
        # Track expansion rate
        if len(result.get("expanded_queries", [])) > 1:
            self.metrics["expansion_rate"] += 1
        
        # Update average processing time
        n = self.metrics["total_queries"]
        current_avg = self.metrics["avg_processing_time"]
        self.metrics["avg_processing_time"] = (
            (current_avg * (n - 1) + processing_time) / n
        )
    
    def get_metrics(self) -> dict:
        """Get current metrics."""
        return {
            **self.metrics,
            "rewrite_rate": (
                self.metrics["rewrite_rate"] / max(1, self.metrics["total_queries"])
            ),
            "expansion_rate": (
                self.metrics["expansion_rate"] / max(1, self.metrics["total_queries"])
            ),
            "success_rate": (
                self.metrics["successful_queries"] / max(1, self.metrics["total_queries"])
            )
        }
```

## References

1. **HyDE Paper**: https://arxiv.org/abs/2212.10496
2. **Query Expansion**: https://en.wikipedia.org/wiki/Query_expansion
3. **RRF Fusion**: https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
4. **Query Rewriting**: https://blog.research.google/2022/10/using-large-language-models-to.html
5. **Cursor Enterprise Framework - RAG Rules**: `.cursor/rules/rag.mdc`
