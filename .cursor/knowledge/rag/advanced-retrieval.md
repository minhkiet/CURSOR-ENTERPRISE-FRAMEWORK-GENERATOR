---
title: "Advanced Retrieval"
description: "Hướng dẫn về advanced retrieval patterns: parent document retrieval, sentence window, auto-merging và knowledge graph RAG"
tags: ["advanced-retrieval", "parent-document", "sentence-window", "auto-merging", "knowledge-graph"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Advanced Retrieval

## Tổng Quan

Advanced retrieval techniques vượt ra ngoài simple top-k similarity search, address những limitations phổ biến như: missing context khi chunks quá nhỏ, lack of document-level coherence, và poor handling of complex queries.

Các techniques như parent document retrieval, sentence window retrieval, và auto-merging retrieval giúp balance giữa granularity của retrieval và richness của context được cung cấp cho LLM.

Knowledge graph RAG represents another frontier, structured hierarchical information để enable more precise retrieval và reasoning.

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức toàn diện về advanced retrieval techniques:

Đầu tiên, chúng ta sẽ tìm hiểu parent document retrieval - retrieve small chunks nhưng use larger parent documents as context.

Thứ hai, tài liệu hướng dẫn sentence window retrieval - focus retrieval on sentences nhưng expand với surrounding context.

Thứ ba, chúng ta sẽ đề cập đến auto-merging retrieval - hierarchical organization cho dynamic granularity.

Cuối cùng, tài liệu cung cấp knowledge graph RAG và implementation examples.

## Key Concepts

### 1. The Chunking Paradox

```
┌─────────────────────────────────────────────────────────────┐
│                    CHUNKING PARADOX                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Small Chunks          Large Chunks                        │
│   ┌─────────┐          ┌───────────────────┐               │
│   │ Sentence │          │ Paragraph/Doc     │               │
│   └─────────┘          └───────────────────┘               │
│        ↓                       ↓                              │
│   + Precise              + Rich context                     │
│   - Missing context      - Noisy, diluted                    │
│   - Lost relationships   - Lower relevance                    │
│                                                              │
│   Solution: Advanced Retrieval Patterns                       │
│   ┌─────────────────────────────────────────┐               │
│   │  Retrieve small chunks, use large context │             │
│   └─────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

## Parent Document Retrieval

### 1. Basic Implementation

```python
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Chunk:
    """Small chunk for retrieval."""
    id: str
    text: str
    parent_id: str  # Reference to parent document
    metadata: Dict

@dataclass
class ParentDocument:
    """Parent document containing chunk."""
    id: str
    text: str
    metadata: Dict

class ParentDocumentRetriever:
    """
    Parent Document Retrieval.
    
    1. Index small chunks (sentences, paragraphs)
    2. Retrieve top-k chunks
    3. Return parent documents with chunk context
    """
    
    def __init__(
        self,
        vector_store,
        chunk_size: int = 256,
        parent_size: int = 2048
    ):
        self.vector_store = vector_store
        self.chunk_size = chunk_size
        self.parent_size = parent_size
        self.chunks = []
        self.parents = {}
    
    def index_document(
        self,
        doc_id: str,
        document: str,
        metadata: Dict = None
    ):
        """
        Index a document, creating chunks and parent.
        """
        metadata = metadata or {}
        
        # Create parent document
        parent = ParentDocument(
            id=f"{doc_id}_parent",
            text=document[:self.parent_size],
            metadata=metadata
        )
        self.parents[parent.id] = parent
        
        # Create child chunks
        chunks = self._create_chunks(document, doc_id, metadata)
        self.chunks.extend(chunks)
        
        # Index chunks
        self.vector_store.index(
            ids=[c.id for c in chunks],
            texts=[c.text for c in chunks]
        )
    
    def _create_chunks(
        self,
        text: str,
        doc_id: str,
        metadata: Dict
    ) -> List[Chunk]:
        """Create chunks from document."""
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), self.chunk_size):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunk = Chunk(
                id=f"{doc_id}_chunk_{i}",
                text=chunk_text,
                parent_id=f"{doc_id}_parent",
                metadata={
                    **metadata,
                    "chunk_index": i // self.chunk_size
                }
            )
            chunks.append(chunk)
        
        return chunks
    
    async def retrieve(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Retrieve relevant documents.
        
        Returns:
            List of dicts with parent document and matched chunks
        """
        # Step 1: Retrieve top-k chunks
        chunk_results = await self.vector_store.search(
            query=query,
            k=top_k * 2  # Retrieve more chunks to group by parent
        )
        
        # Step 2: Group by parent
        parent_chunks = {}
        for result in chunk_results:
            chunk = self._get_chunk(result["id"])
            parent_id = chunk.parent_id
            
            if parent_id not in parent_chunks:
                parent_chunks[parent_id] = {
                    "parent": self.parents[parent_id],
                    "matched_chunks": []
                }
            
            parent_chunks[parent_id]["matched_chunks"].append(chunk)
        
        # Step 3: Create results
        results = []
        for parent_id, data in parent_chunks.items():
            # Find best matching chunk for ranking
            best_chunk = max(
                data["matched_chunks"],
                key=lambda c: self._get_chunk_score(c.id, query)
            )
            
            results.append({
                "parent_doc": data["parent"].text,
                "parent_id": parent_id,
                "matched_chunks": [c.text for c in data["matched_chunks"]],
                "best_chunk": best_chunk.text,
                "chunk_indices": [c.metadata.get("chunk_index") for c in data["matched_chunks"]],
                "score": self._get_chunk_score(best_chunk.id, query)
            })
        
        # Sort by score and return top-k parents
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
    
    def _get_chunk(self, chunk_id: str) -> Chunk:
        """Get chunk by ID."""
        for chunk in self.chunks:
            if chunk.id == chunk_id:
                return chunk
        return None
    
    def _get_chunk_score(self, chunk_id: str, query: str) -> float:
        """Get retrieval score for chunk."""
        # In real implementation, get from vector store
        return 1.0
```

### 2. Hierarchical Parent Retrieval

```python
class HierarchicalParentRetriever:
    """
    Multi-level parent document retrieval.
    
    Levels:
    1. Sentence (for precise matching)
    2. Paragraph (for context)
    3. Section (for document structure)
    4. Document (for full context)
    """
    
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.hierarchy = {
            "sentence": [],
            "paragraph": [],
            "section": [],
            "document": {}
        }
    
    def index_document(
        self,
        doc_id: str,
        document: str,
        metadata: Dict = None
    ):
        """Index with hierarchical structure."""
        metadata = metadata or {}
        
        # Level 4: Document
        self.hierarchy["document"][doc_id] = {
            "text": document,
            "metadata": metadata
        }
        
        # Level 3: Sections
        sections = self._split_sections(document)
        for i, section in enumerate(sections):
            section_id = f"{doc_id}_section_{i}"
            self.hierarchy["section"].append({
                "id": section_id,
                "doc_id": doc_id,
                "text": section,
                "metadata": {**metadata, "section_index": i}
            })
        
        # Level 2: Paragraphs
        paragraphs = self._split_paragraphs(document)
        for i, para in enumerate(paragraphs):
            para_id = f"{doc_id}_para_{i}"
            section_idx = i // 3  # Approximate section assignment
            self.hierarchy["paragraph"].append({
                "id": para_id,
                "doc_id": doc_id,
                "section_id": f"{doc_id}_section_{section_idx}",
                "text": para,
                "metadata": {**metadata, "paragraph_index": i}
            })
        
        # Level 1: Sentences
        sentences = self._split_sentences(document)
        for i, sent in enumerate(sentences):
            sent_id = f"{doc_id}_sent_{i}"
            para_idx = i // 5  # Approximate paragraph assignment
            self.hierarchy["sentence"].append({
                "id": sent_id,
                "doc_id": doc_id,
                "para_id": f"{doc_id}_para_{para_idx}",
                "text": sent,
                "metadata": {**metadata, "sentence_index": i}
            })
    
    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        retrieval_level: str = "sentence"
    ) -> List[Dict]:
        """
        Retrieve with hierarchical context expansion.
        """
        # Step 1: Retrieve at specified level
        primary_results = await self.vector_store.search(
            query=query,
            k=top_k * 3,
            index_name=f"{retrieval_level}_index"
        )
        
        results = []
        
        for result in primary_results[:top_k]:
            # Step 2: Expand context based on hierarchy
            expanded = await self._expand_hierarchy(result)
            results.append(expanded)
        
        return results
    
    async def _expand_hierarchy(
        self,
        primary_result: Dict
    ) -> Dict:
        """Expand context through hierarchy levels."""
        result_id = primary_result["id"]
        parts = result_id.split("_")
        doc_id = parts[0]
        
        # Build hierarchical context
        context = {
            "primary": primary_result["text"],
            "paragraph": "",
            "section": "",
            "document": self.hierarchy["document"].get(doc_id, {}).get("text", "")
        }
        
        # Expand paragraph
        if "para" in result_id:
            para_id = result_id
            context["paragraph"] = self._get_paragraph(para_id)
        elif "sent" in result_id:
            sent_id = result_id
            para_id = self._get_para_for_sent(sent_id)
            context["paragraph"] = self._get_paragraph(para_id)
        
        # Expand section
        if "section" in result_id:
            context["section"] = self._get_section(result_id)
        else:
            section_id = self._get_section_for_para(
                result_id.replace("_para_", "_section_").rsplit("_", 1)[0]
            )
            context["section"] = self._get_section(section_id)
        
        return {
            "query": primary_result.get("query", ""),
            "primary_match": context["primary"],
            "context": "\n\n".join(filter(None, [
                context["paragraph"],
                context["section"]
            ])),
            "full_document": context["document"],
            "metadata": primary_result.get("metadata", {})
        }
```

## Sentence Window Retrieval

### 1. Sentence Window Implementation

```python
class SentenceWindowRetriever:
    """
    Sentence Window Retrieval.
    
    - Retrieve focused on sentences
    - Expand window to include surrounding sentences
    - Balance precision with context
    """
    
    def __init__(
        self,
        vector_store,
        window_size: int = 3  # Number of sentences before/after
    ):
        self.vector_store = vector_store
        self.window_size = window_size
        self.sentences = []
        self.sentence_map = {}  # id -> sentence data
    
    def index_document(
        self,
        doc_id: str,
        document: str,
        metadata: Dict = None
    ):
        """Index document with sentence-level granularity."""
        import re
        
        # Split into sentences
        sentence_pattern = r'[.!?]+["\'"]?\s+'
        raw_sentences = re.split(sentence_pattern, document)
        raw_sentences = [s.strip() for s in raw_sentences if s.strip()]
        
        metadata = metadata or {}
        sentence_data = []
        
        for i, sentence in enumerate(raw_sentences):
            sent_id = f"{doc_id}_sent_{i}"
            
            sentence_data.append({
                "id": sent_id,
                "doc_id": doc_id,
                "text": sentence,
                "index": i,
                "metadata": {
                    **metadata,
                    "sentence_index": i,
                    "total_sentences": len(raw_sentences)
                }
            })
            
            self.sentence_map[sent_id] = sentence_data[-1]
        
        self.sentences.extend(sentence_data)
        
        # Index sentences
        self.vector_store.index(
            ids=[s["id"] for s in sentence_data],
            texts=[s["text"] for s in sentence_data]
        )
    
    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        expand_window: bool = True
    ) -> List[Dict]:
        """
        Retrieve sentences with expanded context.
        """
        # Step 1: Retrieve relevant sentences
        sent_results = await self.vector_store.search(
            query=query,
            k=top_k * 2
        )
        
        # Step 2: Expand windows
        expanded_results = []
        
        for result in sent_results:
            sent_data = self.sentence_map.get(result["id"], {})
            
            if expand_window:
                window_context = self._get_window_context(
                    sent_data,
                    self.window_size
                )
            else:
                window_context = {
                    "window_text": sent_data.get("text", ""),
                    "window_start": sent_data.get("index", 0),
                    "window_end": sent_data.get("index", 0),
                    "window_sentences": [sent_data.get("text", "")]
                }
            
            expanded_results.append({
                "query": query,
                "matched_sentence": sent_data.get("text", ""),
                "window": window_context["window_text"],
                "window_start": window_context["window_start"],
                "window_end": window_context["window_end"],
                "all_sentences_in_window": window_context["window_sentences"],
                "score": result.get("score", 0),
                "metadata": sent_data.get("metadata", {})
            })
        
        # Step 3: Sort by score and deduplicate
        expanded_results.sort(key=lambda x: x["score"], reverse=True)
        
        # Remove overlapping windows
        final_results = self._deduplicate_windows(
            expanded_results,
            min_gap=2  # Minimum gap between windows
        )
        
        return final_results[:top_k]
    
    def _get_window_context(
        self,
        sent_data: Dict,
        window_size: int
    ) -> Dict:
        """Get surrounding sentences within window."""
        doc_id = sent_data.get("doc_id")
        sent_index = sent_data.get("index", 0)
        
        # Find all sentences in document
        doc_sentences = [
            s for s in self.sentences
            if s.get("doc_id") == doc_id
        ]
        
        # Get window indices
        start_idx = max(0, sent_index - window_size)
        end_idx = min(
            len(doc_sentences),
            sent_index + window_size + 1
        )
        
        window_sentences = doc_sentences[start_idx:end_idx]
        
        return {
            "window_text": " ".join(s.get("text", "") for s in window_sentences),
            "window_start": start_idx,
            "window_end": end_idx - 1,
            "window_sentences": [s.get("text", "") for s in window_sentences]
        }
    
    def _deduplicate_windows(
        self,
        results: List[Dict],
        min_gap: int
    ) -> List[Dict]:
        """Remove overlapping windows."""
        if not results:
            return []
        
        filtered = [results[0]]
        last_end = results[0]["window_end"]
        
        for result in results[1:]:
            if result["window_start"] > last_end + min_gap:
                filtered.append(result)
                last_end = result["window_end"]
        
        return filtered
```

### 2. Dynamic Window Sizing

```python
class DynamicWindowRetriever(SentenceWindowRetriever):
    """
    Dynamic window sizing based on query and results.
    """
    
    def __init__(self, vector_store, llm_client):
        super().__init__(vector_store)
        self.llm = llm_client
    
    async def retrieve(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Retrieve with dynamic window expansion.
        """
        # Analyze query
        query_type = await self._analyze_query_type(query)
        
        # Set window size based on query type
        if query_type == "factual":
            window_size = 1  # Small window for precise facts
        elif query_type == "explanatory":
            window_size = 3  # Medium window for explanations
        else:
            window_size = 5  # Larger window for complex queries
        
        self.window_size = window_size
        
        # Perform retrieval with determined window
        return await super().retrieve(
            query=query,
            top_k=top_k,
            expand_window=True
        )
    
    async def _analyze_query_type(self, query: str) -> str:
        """Analyze query to determine type."""
        prompt = f"""
Analyze this query and determine its type:
- "factual": Simple who/what/when/where questions
- "explanatory": How/why questions requiring explanation
- "comprehensive": Complex questions requiring detailed context

Query: {query}

Type:"""
        
        response = await self.llm.complete(prompt)
        
        response_lower = response.lower().strip()
        
        if "factual" in response_lower:
            return "factual"
        elif "explanatory" in response_lower:
            return "explanatory"
        else:
            return "comprehensive"
```

## Auto-Merging Retrieval

### 1. Hierarchical Auto-Merge

```python
class AutoMergingRetriever:
    """
    Auto-Merging Retrieval.
    
    Builds a hierarchical tree of chunks and automatically 
    merges branches that consistently get retrieved together.
    """
    
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.tree = {}  # node_id -> node_data
        self.children_map = {}  # parent_id -> [child_ids]
        self.retrieval_counts = {}  # node_id -> count
    
    def build_tree(
        self,
        doc_id: str,
        document: str,
        metadata: Dict = None
    ):
        """Build hierarchical chunk tree from document."""
        metadata = metadata or {}
        
        # Level 1: Leaf nodes (smallest chunks)
        leaf_chunks = self._create_leaf_chunks(document)
        
        for i, chunk in enumerate(leaf_chunks):
            node_id = f"{doc_id}_leaf_{i}"
            self.tree[node_id] = {
                "text": chunk,
                "level": 1,
                "doc_id": doc_id,
                "children": []
            }
        
        # Level 2: Merge leaves into small groups
        group_size = 4
        for i in range(0, len(leaf_chunks), group_size):
            group_chunks = leaf_chunks[i:i + group_size]
            node_id = f"{doc_id}_group_{i // group_size}"
            child_ids = [
                f"{doc_id}_leaf_{j}"
                for j in range(i, min(i + group_size, len(leaf_chunks)))
            ]
            
            self.tree[node_id] = {
                "text": " ".join(group_chunks),
                "level": 2,
                "doc_id": doc_id,
                "children": child_ids
            }
            
            for child_id in child_ids:
                if child_id not in self.children_map:
                    self.children_map[child_id] = []
                self.children_map[child_id].append(node_id)
        
        # Level 3: Merge groups into larger sections
        section_size = 4
        num_groups = (len(leaf_chunks) + group_size - 1) // group_size
        
        for i in range(0, num_groups, section_size):
            group_ids = [
                f"{doc_id}_group_{j}"
                for j in range(i, min(i + section_size, num_groups))
            ]
            
            node_id = f"{doc_id}_section_{i // section_size}"
            section_text = " ".join(
                self.tree[g]["text"]
                for g in group_ids if g in self.tree
            )
            
            self.tree[node_id] = {
                "text": section_text,
                "level": 3,
                "doc_id": doc_id,
                "children": group_ids
            }
            
            for child_id in group_ids:
                if child_id not in self.children_map:
                    self.children_map[child_id] = []
                self.children_map[child_id].append(node_id)
        
        # Level 4: Document root
        root_id = f"{doc_id}_root"
        section_ids = [
            f"{doc_id}_section_{i}"
            for i in range((num_groups + section_size - 1) // section_size)
        ]
        
        self.tree[root_id] = {
            "text": document,
            "level": 4,
            "doc_id": doc_id,
            "children": section_ids
        }
        
        for child_id in section_ids:
            if child_id not in self.children_map:
                self.children_map[child_id] = []
            self.children_map[child_id].append(root_id)
        
        # Index leaf nodes
        leaf_nodes = [
            (node_id, node["text"])
            for node_id, node in self.tree.items()
            if node["level"] == 1
        ]
        
        self.vector_store.index(
            ids=[n[0] for n in leaf_nodes],
            texts=[n[1] for n in leaf_nodes]
        )
    
    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        merge_threshold: int = 2  # Merge if retrieved >= threshold times
    ) -> List[Dict]:
        """
        Retrieve and auto-merge results.
        """
        # Step 1: Retrieve leaf nodes
        leaf_results = await self.vector_store.search(
            query=query,
            k=top_k * 5
        )
        
        # Step 2: Track retrieval counts
        for result in leaf_results:
            node_id = result["id"]
            self.retrieval_counts[node_id] = (
                self.retrieval_counts.get(node_id, 0) + 1
            )
        
        # Step 3: Propagate counts up the tree
        self._propagate_counts(leaf_results)
        
        # Step 4: Merge nodes based on threshold
        merged_results = self._merge_nodes(
            leaf_results,
            merge_threshold
        )
        
        # Step 5: Return merged chunks
        results = []
        for node_id in merged_results:
            node = self.tree.get(node_id)
            if node:
                results.append({
                    "text": node["text"],
                    "level": node["level"],
                    "node_id": node_id,
                    "retrieval_count": self.retrieval_counts.get(node_id, 1)
                })
        
        results.sort(
            key=lambda x: x["retrieval_count"],
            reverse=True
        )
        
        return results[:top_k]
    
    def _propagate_counts(self, leaf_results: List[Dict]):
        """Propagate retrieval counts up the tree."""
        for result in leaf_results:
            node_id = result["id"]
            count = self.retrieval_counts.get(node_id, 1)
            
            # Propagate to parents
            parents = self.children_map.get(node_id, [])
            for parent_id in parents:
                self.retrieval_counts[parent_id] = (
                    self.retrieval_counts.get(parent_id, 0) + count
                )
                
                # Propagate to grandparents
                grandparents = self.children_map.get(parent_id, [])
                for gp_id in grandparents:
                    self.retrieval_counts[gp_id] = (
                        self.retrieval_counts.get(gp_id, 0) + count // 2
                    )
    
    def _merge_nodes(
        self,
        leaf_results: List[Dict],
        threshold: int
    ) -> List[str]:
        """Merge nodes that meet threshold."""
        # Start with retrieved leaf nodes
        selected = set(r["id"] for r in leaf_results)
        
        # Try to merge by climbing tree
        merged = set()
        
        for node_id in list(selected):
            if self.retrieval_counts.get(node_id, 0) >= threshold:
                # Include this node and exclude its children
                children = self.tree.get(node_id, {}).get("children", [])
                
                for child_id in children:
                    if child_id in selected:
                        selected.remove(child_id)
                        merged.add(child_id)
                
                merged.add(node_id)
        
        return list(selected | merged)
```

## Knowledge Graph RAG

### 1. Knowledge Graph Structure

```python
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Entity:
    """Knowledge graph entity."""
    id: str
    name: str
    type: str  # person, org, concept, location, etc.
    description: str
    properties: Dict
    embedding: List[float] = None

@dataclass
class Relationship:
    """Knowledge graph relationship."""
    source_id: str
    target_id: str
    relation_type: str  # works_for, located_in, part_of, etc.
    properties: Dict
    weight: float = 1.0

class KnowledgeGraphRAG:
    """
    Knowledge Graph RAG.
    
    Uses structured knowledge graph for retrieval
    instead of pure vector search.
    """
    
    def __init__(
        self,
        vector_store,
        kg_storage
    ):
        self.vector_store = vector_store
        self.kg = kg_storage
        self.entities = {}
        self.relations = []
    
    def build_graph(
        self,
        documents: List[dict]
    ):
        """
        Build knowledge graph from documents.
        """
        for doc in documents:
            # Extract entities and relationships
            entities, relations = self._extract_from_document(doc)
            
            # Add to graph
            for entity in entities:
                self.entities[entity.id] = entity
            
            self.relations.extend(relations)
        
        # Index entities for retrieval
        self._index_entities()
    
    def _extract_from_document(
        self,
        doc: dict
    ) -> tuple:
        """
        Extract entities and relationships from document.
        In production, use NER and RE models.
        """
        # Placeholder - in production use spaCy, LlamaIndex, etc.
        entities = []
        relations = []
        
        # This would call NER model
        # Example output:
        # entities = [
        #     Entity(id="e1", name="GPT-4", type="model", ...),
        #     Entity(id="e2", name="OpenAI", type="organization", ...),
        # ]
        # relations = [
        #     Relationship(source_id="e1", target_id="e2", type="developed_by", ...),
        # ]
        
        return entities, relations
    
    def _index_entities(self):
        """Index entities for vector search."""
        entity_ids = [e.id for e in self.entities.values()]
        entity_texts = [
            f"{e.name}: {e.description}"
            for e in self.entities.values()
        ]
        
        self.vector_store.index(
            ids=entity_ids,
            texts=entity_texts
        )
    
    async def retrieve(
        self,
        query: str,
        top_k: int = 10,
        max_hops: int = 2
    ) -> List[Dict]:
        """
        Retrieve from knowledge graph with multi-hop reasoning.
        """
        # Step 1: Find seed entities via vector search
        seed_results = await self.vector_store.search(
            query=query,
            k=top_k
        )
        
        seed_entity_ids = [r["id"] for r in seed_results]
        
        # Step 2: Expand via relationships (multi-hop)
        expanded_entities = self._expand_graph(
            seed_entity_ids,
            max_hops
        )
        
        # Step 3: Build subgraph context
        subgraph_context = self._build_subgraph_context(
            expanded_entities
        )
        
        return subgraph_context
    
    def _expand_graph(
        self,
        seed_ids: List[str],
        max_hops: int
    ) -> Set[str]:
        """Expand from seed entities through relationships."""
        expanded = set(seed_ids)
        current = set(seed_ids)
        
        for hop in range(max_hops):
            next_layer = set()
            
            for entity_id in current:
                # Find related entities
                for rel in self.relations:
                    if rel.source_id == entity_id:
                        next_layer.add(rel.target_id)
                    elif rel.target_id == entity_id:
                        next_layer.add(rel.source_id)
            
            expanded |= next_layer
            current = next_layer
        
        return expanded
    
    def _build_subgraph_context(
        self,
        entity_ids: Set[str]
    ) -> List[Dict]:
        """Build context from subgraph."""
        context = []
        
        for entity_id in entity_ids:
            entity = self.entities.get(entity_id)
            if not entity:
                continue
            
            # Get related entities
            related = []
            for rel in self.relations:
                if rel.source_id == entity_id:
                    target = self.entities.get(rel.target_id)
                    if target:
                        related.append({
                            "entity": target.name,
                            "relation": rel.relation_type,
                            "target_description": target.description
                        })
                elif rel.target_id == entity_id:
                    source = self.entities.get(rel.source_id)
                    if source:
                        related.append({
                            "entity": source.name,
                            "relation": rel.relation_type,
                            "target_description": entity.description
                        })
            
            context.append({
                "entity_id": entity.id,
                "entity_name": entity.name,
                "entity_type": entity.type,
                "description": entity.description,
                "related_entities": related,
                "properties": entity.properties
            })
        
        return context
    
    async def retrieve_with_reasoning(
        self,
        query: str,
        question_type: str = "direct"
    ) -> Dict:
        """
        Retrieve with explicit reasoning steps.
        """
        if question_type == "direct":
            # Simple retrieval
            return await self.retrieve(query)
        
        elif question_type == "comparative":
            # Need to compare two entities
            entities = await self._identify_comparison_entities(query)
            
            entity_a, entity_b = entities
            
            # Get context for both
            context_a = self._get_entity_context(entity_a)
            context_b = self._get_entity_context(entity_b)
            
            return {
                "entity_a": context_a,
                "entity_b": context_b,
                "comparison_needed": True
            }
        
        elif question_type == "path":
            # Need to find path between entities
            source, target = await self._identify_path_entities(query)
            
            path = self._find_shortest_path(source, target)
            
            return {
                "path": path,
                "path_description": self._describe_path(path)
            }
        
        return await self.retrieve(query)
    
    def _get_entity_context(self, entity_id: str) -> Dict:
        """Get full context for an entity."""
        entity = self.entities.get(entity_id, {})
        
        # Get all relations
        relations = [
            r for r in self.relations
            if r.source_id == entity_id or r.target_id == entity_id
        ]
        
        return {
            "entity": entity,
            "relations": relations
        }
    
    def _find_shortest_path(
        self,
        source_id: str,
        target_id: str
    ) -> List[str]:
        """Find shortest path between two entities."""
        from collections import deque
        
        queue = deque([(source_id, [source_id])])
        visited = {source_id}
        
        while queue:
            current, path = queue.popleft()
            
            if current == target_id:
                return path
            
            for rel in self.relations:
                next_id = None
                
                if rel.source_id == current and rel.target_id not in visited:
                    next_id = rel.target_id
                elif rel.target_id == current and rel.source_id not in visited:
                    next_id = rel.source_id
                
                if next_id:
                    visited.add(next_id)
                    queue.append((next_id, path + [next_id]))
        
        return []  # No path found
    
    def _describe_path(self, path: List[str]) -> str:
        """Generate natural language description of path."""
        if len(path) < 2:
            return ""
        
        descriptions = []
        
        for i in range(len(path) - 1):
            source_id = path[i]
            target_id = path[i + 1]
            
            source = self.entities.get(source_id, {})
            target = self.entities.get(target_id, {})
            
            # Find relation
            relation = None
            for rel in self.relations:
                if (rel.source_id == source_id and rel.target_id == target_id) or \
                   (rel.source_id == target_id and rel.target_id == source_id):
                    relation = rel
                    break
            
            if relation:
                desc = f"{source.name} {relation.relation_type} {target.name}"
                descriptions.append(desc)
            else:
                descriptions.append(f"{source.name} to {target.name}")
        
        return " → ".join(descriptions)
```

## Best Practices

### 1. Choosing the Right Pattern

```python
def select_retrieval_pattern(
    query: str,
    document_structure: str,
    complexity: str
) -> str:
    """
    Select appropriate retrieval pattern.
    """
    # Decision tree
    if complexity == "high":
        if document_structure == "structured":
            return "knowledge_graph"
        else:
            return "auto_merging"
    
    if document_structure == "hierarchical":
        if "compare" in query.lower():
            return "parent_document"
        else:
            return "auto_merging"
    
    if complexity == "low" and document_structure == "flat":
        return "sentence_window"
    
    # Default
    return "parent_document"


RETRIEVAL_PATTERN_GUIDE = {
    "parent_document": {
        "best_for": [
            "Documents with clear parent-child structure",
            "When you need full document context",
            "Comparison queries"
        ],
        "pros": [
            "Rich context",
            "Maintains document structure",
            "Good for comparisons"
        ],
        "cons": [
            "May include irrelevant content",
            "Larger context window"
        ]
    },
    "sentence_window": {
        "best_for": [
            "Precise factual queries",
            "When local context matters",
            "Short answer questions"
        ],
        "pros": [
            "Very focused retrieval",
            "Fast indexing",
            "Good for precise facts"
        ],
        "cons": [
            "May miss broader context",
            "Requires careful window sizing"
        ]
    },
    "auto_merging": {
        "best_for": [
            "Complex analytical queries",
            "When retrieval granularity varies",
            "Long documents with varying density"
        ],
        "pros": [
            "Adaptive granularity",
            "Handles complexity variation",
            "Good for multi-faceted queries"
        ],
        "cons": [
            "More complex implementation",
            "Tuning required"
        ]
    },
    "knowledge_graph": {
        "best_for": [
            "Structured domains",
            "Multi-hop reasoning",
            "When relationships matter"
        ],
        "pros": [
            "Explicit reasoning",
            "Handles complex queries",
            "Explainable"
        ],
        "cons": [
            "Requires KG construction",
            "May miss unstructured info"
        ]
    }
}
```

### 2. Hybrid Approaches

```python
class HybridRetrievalSystem:
    """
    Combine multiple retrieval patterns.
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
        pattern: str = "auto",
        **kwargs
    ) -> List[Dict]:
        """
        Retrieve using appropriate pattern or hybrid.
        """
        if pattern == "auto":
            pattern = self._select_pattern(query)
        
        if pattern == "hybrid":
            return await self._hybrid_retrieve(query, **kwargs)
        
        # Single pattern retrieval
        retriever = self.retrievers.get(pattern)
        
        if not retriever:
            raise ValueError(f"Unknown pattern: {pattern}")
        
        return await retriever.retrieve(query, **kwargs)
    
    async def _hybrid_retrieve(
        self,
        query: str,
        top_k: int = 10
    ) -> List[Dict]:
        """Combine multiple retrieval patterns."""
        # Retrieve from all patterns
        results = {}
        
        for pattern_name, retriever in self.retrievers.items():
            try:
                pattern_results = await retriever.retrieve(
                    query=query,
                    top_k=top_k
                )
                results[pattern_name] = pattern_results
            except Exception as e:
                print(f"Error with {pattern_name}: {e}")
        
        # Fuse results
        if self.fusion_method == "rrf":
            return self._rrf_fusion(results, top_k)
        else:
            return self._score_weighted_fusion(results, top_k)
    
    def _rrf_fusion(
        self,
        results: Dict,
        k: int = 60
    ) -> List[Dict]:
        """Reciprocal Rank Fusion."""
        scores = {}
        
        for pattern_name, pattern_results in results.items():
            for rank, result in enumerate(pattern_results, 1):
                result_id = result.get("id", result.get("node_id", rank))
                
                if result_id not in scores:
                    scores[result_id] = {
                        **result,
                        "rrf_score": 0,
                        "sources": []
                    }
                
                scores[result_id]["rrf_score"] += 1.0 / (k + rank)
                scores[result_id]["sources"].append(pattern_name)
        
        # Sort and return
        fused = sorted(
            scores.values(),
            key=lambda x: x["rrf_score"],
            reverse=True
        )
        
        return fused
    
    def _score_weighted_fusion(
        self,
        results: Dict,
        top_k: int
    ) -> List[Dict]:
        """Score-weighted fusion."""
        weights = {
            "parent_document": 0.3,
            "sentence_window": 0.2,
            "auto_merging": 0.3,
            "knowledge_graph": 0.2
        }
        
        scores = {}
        
        for pattern_name, pattern_results in results.items():
            weight = weights.get(pattern_name, 0.25)
            
            for result in pattern_results:
                result_id = result.get("id", result.get("node_id"))
                
                if result_id not in scores:
                    scores[result_id] = {
                        **result,
                        "weighted_score": 0,
                        "sources": []
                    }
                
                base_score = result.get("score", 0)
                scores[result_id]["weighted_score"] += weight * base_score
                scores[result_id]["sources"].append(pattern_name)
        
        # Sort and return
        fused = sorted(
            scores.values(),
            key=lambda x: x["weighted_score"],
            reverse=True
        )
        
        return fused[:top_k]
```

## Examples

### Example 1: Production RAG System

```python
class ProductionAdvancedRAG:
    """
    Production-ready advanced RAG system.
    """
    
    def __init__(self, config: dict):
        self.config = config
        
        # Initialize vector store
        self.vector_store = VectorStore(config["vector_store"])
        
        # Initialize retrievers
        self.retrievers = {
            "parent_document": ParentDocumentRetriever(
                self.vector_store,
                chunk_size=config.get("chunk_size", 256),
                parent_size=config.get("parent_size", 2048)
            ),
            "sentence_window": SentenceWindowRetriever(
                self.vector_store,
                window_size=config.get("window_size", 3)
            ),
            "auto_merging": AutoMergingRetriever(self.vector_store)
        }
        
        # Initialize hybrid system
        self.hybrid = HybridRetrievalSystem(self.retrievers)
    
    async def index_documents(
        self,
        documents: List[dict]
    ):
        """Index documents with all patterns."""
        for doc in documents:
            doc_id = doc["id"]
            content = doc["content"]
            metadata = doc.get("metadata", {})
            
            # Index with each retriever
            for retriever in self.retrievers.values():
                try:
                    retriever.index_document(
                        doc_id=doc_id,
                        document=content,
                        metadata=metadata
                    )
                except Exception as e:
                    print(f"Error indexing with {type(retriever)}: {e}")
    
    async def retrieve(
        self,
        query: str,
        pattern: str = "hybrid",
        top_k: int = 10,
        **kwargs
    ) -> List[Dict]:
        """
        Retrieve with specified or auto-selected pattern.
        """
        return await self.hybrid.retrieve(
            query=query,
            pattern=pattern,
            top_k=top_k,
            **kwargs
        )
```

### Example 2: Evaluation Framework

```python
class AdvancedRetrievalEvaluator:
    """
    Evaluate advanced retrieval patterns.
    """
    
    def __init__(self, evaluator: RAGEvaluationPipeline):
        self.rag_evaluator = evaluator
    
    async def evaluate_patterns(
        self,
        test_cases: List[dict],
        patterns: List[str]
    ) -> Dict:
        """
        Compare different retrieval patterns.
        """
        results = {}
        
        for pattern in patterns:
            print(f"Evaluating pattern: {pattern}")
            
            pattern_results = []
            
            for test_case in test_cases:
                # Get results from this pattern
                # (Simplified - actual implementation would call RAG)
                result = {
                    "question": test_case["question"],
                    "answer": test_case["answer"],
                    "contexts": test_case.get("contexts", []),
                    "reference": test_case.get("reference")
                }
                
                pattern_results.append(result)
            
            # Evaluate this pattern
            eval_results = await self.rag_evaluator.evaluate(pattern_results)
            results[pattern] = eval_results
        
        return self._generate_comparison_report(results)
    
    def _generate_comparison_report(
        self,
        results: Dict
    ) -> Dict:
        """Generate comparison report."""
        report = {
            "patterns_compared": list(results.keys()),
            "metrics": {}
        }
        
        # Compare each metric
        for metric_name in ["faithfulness", "answer_relevance", "context_precision"]:
            metric_results = {}
            
            for pattern, pattern_results in results.items():
                mean_score = pattern_results.get("metrics", {}).get(metric_name, {}).get("mean", 0)
                metric_results[pattern] = mean_score
            
            best_pattern = max(metric_results.items(), key=lambda x: x[1])
            
            report["metrics"][metric_name] = {
                "scores": metric_results,
                "best_pattern": best_pattern[0],
                "best_score": best_pattern[1]
            }
        
        return report
```

## References

1. **Parent Document Retriever**: https://python.langchain.com/docs/modules/data_connection/retrievers/parent_document_retriever
2. **Sentence Window Retrieval**: https://python.langchain.com/docs/modules/data_connection/retrievers/sentence_window
3. **Auto-Merging Retriever**: https://python.langchain.com/docs/modules/data_connection/retrievers/auto_merging_retriever
4. **Knowledge Graph RAG**: https://python.langchain.com/docs/modules/data_connection/retrievers/kg_retriever
5. **Cursor Enterprise Framework - RAG Rules**: `.cursor/rules/rag.mdc`
