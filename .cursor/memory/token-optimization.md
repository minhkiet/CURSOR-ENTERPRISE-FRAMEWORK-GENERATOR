# Token Optimization Strategy Guide

```markdown
# Token Optimization - Hướng dẫn chi tiết

## Tổng quan
Framework này được thiết kế để tối ưu token tiêu thụ tối đa cho AI coding agents.

## 10 Chiến lược Token Optimization

### 1. Context Router

**Mô tả**: Chỉ load domain knowledge cần thiết cho task hiện tại.

**Cách hoạt động**:
```
Request: "Tối ưu Entity Framework"
→ Chỉ load: aspnet-core, sql-server, postgres
→ Skip: bazi, pdf, crm, marketing, nextjs, vue, nuxt
→ Tiết kiệm: ~70% token
```

**Cài đặt**:
```json
{
  "context-router": {
    "aspnet-core": ["sql-server", "postgres", "redis"],
    "bazi": ["pdf"],
    "rag": ["vector-search", "pgvector", "openai"]
  }
}
```

**Best Practice**:
- Luôn xác định domain chính trước
- Chỉ load dependencies trực tiếp
- Không load toàn bộ knowledge base

### 2. Knowledge Compiler

**Mô tả**: Gộp và summarize knowledge documents thành một file nhỏ hơn.

**Cách hoạt động**:
```
Input: 10 knowledge files (100KB)
→ Compile: 1 compiled file (10KB)
→ Tiết kiệm: ~90% token
```

**Script**:
```powershell
. .cursor/scripts/knowledge-compiler/compile-knowledge.ps1 -Domain aspnet-core
```

### 3. Prompt Cache

**Mô tả**: Cache prompt templates và responses để reuse.

**Lưu trữ**:
- Prompt hash
- Prompt summary
- Response summary
- Last used timestamp
- Use count

**Cache hit rate target**: > 80%

### 4. Session Summary

**Mô tả**: Compress session context sau mỗi task.

**Trước khi compress**:
```
- 50 messages
- 5000 tokens context
```

**Sau khi compress**:
```
- 1 summary message
- 200 tokens context
→ Tiết kiệm: ~96% token
```

### 5. Decision Memory

**Mô tả**: Lưu trữ ADRs và reuse trong các task tương tự.

**Khi nào reuse**:
- Check decisions.sqlite trước khi tạo ADR mới
- Check tittle ADRs cho similar decisions
- Reference existing ADRs thay vì re-explain

**Tiết kiệm**: ~30% token cho architecture decisions

### 6. Bug Memory

**Mô tả**: Lưu trữ bug patterns và solutions để tránh repeat.

**Khi nào reuse**:
- Check bugs.sqlite trước khi fix bug
- Check bug_patterns cho known patterns
- Reference existing solutions

**Tiết kiệm**: ~50% token cho bug fixing

### 7. Incremental Scan

**Mô tả**: Chỉ scan changed files thay vì toàn bộ codebase.

**Trước**:
```
Scan entire codebase: 10,000 files → 500,000 tokens
```

**Sau**:
```
Scan only changed: 10 files → 500 tokens
→ Tiết kiệm: ~99% token
```

**Implementation**:
```powershell
git diff --name-only HEAD~1
```

### 8. Lazy Loading

**Mô tả**: Load knowledge on-demand, không load tất cả cùng lúc.

**Trước**:
```
Load all knowledge: 200 files → 1,000,000 tokens
```

**Sau**:
```
Load on-demand: 5 files → 25,000 tokens per request
→ Tiết kiệm: ~97.5% token per request
```

### 9. Semantic Retrieval

**Mô tả**: Sử dụng vector search thay vì full-text search.

**Trước**:
```
Grep full-text: scan 10,000 files → 100,000 tokens
```

**Sau**:
```
Vector search: search 1000 vectors → 100 tokens
→ Tiết kiệm: ~99% token cho search
```

### 10. Auto Compression

**Mô tả**: Tự động compress long contexts.

**Trigger**: Khi context > 80% của context window

**Method**:
- Remove redundant whitespace
- Shorten variable names
- Collapse repeated patterns
- Replace long code with summaries

## Token Budget

| Context Type | Budget | Optimization |
|---|---|---|
| System prompt | 2000 | Cache common parts |
| Knowledge | 5000 | Context Router |
| Session | 3000 | Session Summary |
| Output | 4000 | Concise responses |

## Benchmark

| Task Type | Before | After | Savings |
|---|---|---|---|
| Bug Fix | 50,000 | 15,000 | 70% |
| Feature Build | 100,000 | 25,000 | 75% |
| Code Review | 30,000 | 10,000 | 67% |
| Security Audit | 80,000 | 20,000 | 75% |
| Architecture | 60,000 | 18,000 | 70% |

## Best Practices

1. **Luôn check memory trước**: Trước khi implement, check memory
2. **Sử dụng Context Router**: Không load toàn bộ knowledge
3. **Cache prompt responses**: Reuse responses cho similar prompts
4. **Compress session**: Sau mỗi task, compress session
5. **Incremental scan**: Chỉ scan changed files
6. **Semantic search**: Use vector search thay vì grep
7. **Lazy load**: Load knowledge on-demand
8. **Reuse decisions**: Không tạo lại existing ADRs
9. **Reuse bugs**: Không fix lại known bugs
10. **Auto compress**: Compress long contexts

## Liên kết
- [[memory/context-router]] - Context Router
- [[memory/prompt-index]] - Prompt Index
- [[scripts/knowledge-compiler]] - Knowledge Compiler
- [[scripts/embedding-builder]] - Embedding Builder
```
