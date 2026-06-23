# OpenAI FAQ - Câu Hỏi Thường Gặp

## Câu Hỏi Cơ Bản

### 1. GPT-4 vs GPT-3.5?

GPT-4 là advanced model với better reasoning, larger context window. GPT-3.5 cheaper, faster, adequate for simple tasks.

### 2. Token là gì?

Token là units of text processed by models. ~4 characters = 1 token. Input + Output must stay within model's limit.

### 3. Temperature nào nên dùng?

0 = deterministic, good for factual. 0.7 = balanced. 1 = creative, good for brainstorming.

## Câu Hỏi Kỹ Thuật

### 4. Embeddings là gì?

Embeddings là numerical vectors representing text. Used for similarity search. OpenAI ada-002 là popular embedding model.

### 5. Function calling là gì?

Function calling cho phép model generate structured JSON output. Define functions, model calls appropriate one.

### 6. Làm thế nào để reduce costs?

Optimize prompts, use caching, use appropriate model (GPT-3.5 for simple tasks).
