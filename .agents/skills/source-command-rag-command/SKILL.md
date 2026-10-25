---
name: "source-command-rag-command"
description: "RAG - Xây dựng RAG system với embedding và retrieval"
---

# source-command-rag-command

Use this skill when the user asks to run the migrated source command `rag-command`.

## Command Template

# Command: /rag

## Mục tiêu
Xây dựng RAG system từ document processing đến retrieval.

## Trigger Keywords
- rag
- rag system
- xây dựng rag
- build rag
- retrieval augmented generation
- vector search
- embedding
- knowledge base
- document search

## Workflow

### Bước 1: Memory First
- [ ] Check `memory/decisions.sqlite` cho existing RAG decisions
- [ ] Check `technology-stack.json` cho AI stack
- [ ] Load rag rules và skills

### Bước 2: Architecture Design
- [ ] Identify document sources
- [ ] Define chunking strategy
- [ ] Select embedding model
- [ ] Select vector store (PGVector/ChromaDB/Qdrant)
- [ ] Design retrieval strategy
- [ ] Design reranking strategy
- [ ] Create ADR

### Bước 3: Implementation
- [ ] Setup embedding pipeline
- [ ] Implement document processing
- [ ] Implement chunking logic
- [ ] Implement vector storage
- [ ] Implement retrieval
- [ ] Implement reranking
- [ ] Implement generation prompt

### Bước 4: Evaluation
- [ ] Design evaluation metrics
- [ ] Test retrieval accuracy
- [ ] Test generation quality
- [ ] Optimize chunking/retrieval

## Liên kết
- [[../workflows/build-rag]] - Build RAG Workflow
- [[../prompts/rag-design]] - RAG Design Prompt
- [[../skills/rag-builder]] - RAG Builder Skill
- [[../rules/rag]] - RAG Rules
- [[../rules/pgvector]] - PGVector Rules
- [[../rules/vector-search]] - Vector Search Rules
