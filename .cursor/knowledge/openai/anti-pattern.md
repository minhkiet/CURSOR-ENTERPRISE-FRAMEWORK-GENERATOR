# OpenAI Anti-Patterns - Các Mẫu Cần Tránh

## Anti-Patterns

### 1. API Key Exposure

**Mô tả**: Expose API key in frontend.

**Giải pháp**: Use backend proxy.

### 2. No Retry Logic

**Mô tả**: Ignore rate limit errors.

**Giải pháp**: Implement retry với backoff.

### 3. Large Prompts

**Mô tả**: Send too much context.

**Giải pháp**: Optimize, summarize.

## Kết luận

Tránh các anti-patterns này giúp OpenAI usage tốt hơn.
