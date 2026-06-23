# Claude Architecture - Kiến Trúc Claude Integration

## Tổng quan

Claude là Anthropic AI assistant. Integration bao gồm API client, tool use, message history.

## Kiến trúc chi tiết

### 1. API Integration

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const message = await client.messages.create({
  model: 'claude-3-5-sonnet-20240620',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Hello!' }]
});
```

## Kết luận

Claude integration requires proper error handling.
