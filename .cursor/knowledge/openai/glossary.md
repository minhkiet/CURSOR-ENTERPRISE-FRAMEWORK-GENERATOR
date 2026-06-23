# OpenAI Glossary - Từ Điển Thuật Ngữ OpenAI

## Giới thiệu

Tài liệu này cung cấp các thuật ngữ chuyên ngành OpenAI API và services.

## Các thuật ngữ cơ bản

### 1. GPT Models

GPT (Generative Pre-trained Transformer) là LLM từ OpenAI. GPT-4 là latest version. Token limit, reasoning capabilities.

### 2. API Key

API Key là unique identifier cho authenticate requests. Store securely, never expose in frontend.

### 3. Tokens

Tokens là units of text processed by models. Roughly 4 characters = 1 token. Input + Output must stay within limit.

### 4. Temperature

Temperature controls randomness of output. 0 = deterministic, 1 = creative. Affects creativity vs consistency.

### 5. Top P

Top P là nucleus sampling parameter. Controls diversity of output. Lower = focused, Higher = diverse.

### 6. System Prompt

System prompt sets behavior/instructions for model. Defines role, rules, context. Critical for getting desired outputs.

### 7. Few-Shot Learning

Providing examples in prompt for model to learn pattern. Improves accuracy without fine-tuning.

### 8. Fine-Tuning

Fine-tuning là training model on custom data. Creates specialized version. Higher cost, better performance.

### 9. Embeddings

Embeddings là numerical representations of text. Used for similarity search. OpenAI provides embedding models.

### 10. Chat Completions

Chat Completions API for conversational interactions. Messages array with roles: system, user, assistant.

### 11. Completions API

Legacy API for text generation. Given prompt, model generates completion. Less structured than chat.

### 12. Function Calling

Function calling là capability to generate structured JSON output. Define functions, model calls appropriate one.

### 13. Streaming

Streaming returns tokens as they're generated. Faster perceived response. Event-based processing.

## Kết luận

OpenAI Glossary cung cấp nền tảng về OpenAI concepts.
