---
title: "Claude API Integration"
description: "Hướng dẫn tích hợp Anthropic Claude API trong enterprise applications - API key management, SDK setup, error handling, rate limits"
tags: ["claude", "api", "integration", "sdk", "enterprise", "authentication"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Claude API Integration

## Tổng quan (Overview)

Anthropic Claude API là một trong những Large Language Model (LLM) API mạnh mẽ nhất hiện nay, được sử dụng rộng rãi trong các ứng dụng enterprise từ chatbot thông minh đến automation workflows phức tạp. Việc tích hợp Claude API một cách hiệu quả và an toàn là yếu tố then chốt cho bất kỳ enterprise application nào muốn tận dụng sức mạnh của generative AI.

Tài liệu này cung cấp hướng dẫn toàn diện về cách thiết lập, cấu hình và vận hành Claude API trong môi trường production, bao gồm các best practices về security, scalability và reliability.

## Mục đích (Purpose)

Mục tiêu của tài liệu này bao gồm:

1. **Thiết lập môi trường phát triển** - Cấu hình API credentials, SDK và development environment một cách an toàn
2. **Quản lý API Keys** - Best practices cho việc lưu trữ, rotation và bảo mật API keys trong production
3. **SDK Implementation** - Hướng dẫn sử dụng official SDKs cho Python và TypeScript/JavaScript
4. **Error Handling** - Chiến lược xử lý lỗi, retry logic và fallback mechanisms
5. **Rate Limits & Quotas** - Quản lý và tối ưu hóa việc sử dụng API để tránh hitting rate limits
6. **Production Deployment** - Cấu hình cho môi trường production với high availability và monitoring

## Khái niệm cốt lõi (Key Concepts)

### 1. API Key Management

API key là credentials quan trọng nhất khi làm việc với Claude API. Trong môi trường enterprise, việc quản lý API key cần tuân thủ các nguyên tắc sau:

- **Không hardcode API keys** trong source code
- **Sử dụng environment variables** hoặc secret management services
- **Implement key rotation** định kỳ
- **Theo dõi usage** per API key để phát hiện bất thường

### 2. API Endpoints

Claude API cung cấp các endpoints chính sau:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/messages` | POST | Gửi messages và nhận responses |
| `/v1/messages/stream` | POST | Streaming responses |
| `/v1/models` | GET | Liệt kê available models |
| `/v1/complete` | POST | Completion API (legacy) |

### 3. Request Structure

Một Claude API request cơ bản bao gồm:

```json
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": "Your message here"
    }
  ]
}
```

### 4. Response Structure

```json
{
  "id": "msg_abc123",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Response content"
    }
  ],
  "model": "claude-3-5-sonnet-20241022",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 10,
    "output_tokens": 25
  }
}
```

## SDK Setup và Configuration

### Python SDK (Anthropic Python SDK)

#### Installation

```bash
pip install anthropic
```

#### Basic Configuration

```python
import os
from anthropic import Anthropic

# Method 1: Using environment variable (RECOMMENDED)
client = Anthropic()

# Method 2: Explicit API key
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Method 3: Configuration with custom settings
client = Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
    timeout=60.0,  # Request timeout in seconds
    max_retries=3,  # Number of retries for failed requests
)
```

#### Production Configuration với tenacity

```python
import os
from anthropic import Anthropic
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

class ClaudeAPIClient:
    """Production-grade Claude API client với retry logic."""
    
    def __init__(
        self,
        api_key: str | None = None,
        max_retries: int = 3,
        timeout: float = 60.0,
    ):
        self.client = Anthropic(
            api_key=api_key or os.environ["ANTHROPIC_API_KEY"],
            timeout=timeout,
            max_retries=0,  # We handle retries ourselves
        )
        self._configure_retries(max_retries)
    
    def _configure_retries(self, max_retries: int):
        """Configure retry behavior với exponential backoff."""
        retry_config = {
            "stop": stop_after_attempt(max_retries),
            "wait": wait_exponential(multiplier=1, min=2, max=30),
            "retry": retry_if_exception_type((RateLimitError, APIError)),
            "reraise": True,
        }
        # Apply retry decorator to methods
    
    def create_message(
        self,
        model: str = "claude-3-5-sonnet-20241022",
        messages: list[dict],
        system: str | None = None,
        max_tokens: int = 1024,
        temperature: float = 1.0,
        **kwargs,
    ) -> Anthropic.types.Message:
        """Create a message với Claude."""
        return self.client.messages.create(
            model=model,
            system=system,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs,
        )
```

### TypeScript/JavaScript SDK

#### Installation

```bash
npm install @anthropic-ai/sdk
# hoặc
yarn add @anthropic-ai/sdk
# hoặc
pnpm add @anthropic-ai/sdk
```

#### Basic Configuration

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// With custom configuration
const clientConfigured = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
  timeout: 60000, // 60 seconds
  maxRetries: 3,
  baseURL: 'https://api.anthropic.com/v1', // Custom base URL if needed
});
```

#### Production Configuration với TypeScript

```typescript
import Anthropic, { APIError, RateLimitError } from '@anthropic-ai/sdk';

interface ClaudeClientConfig {
  apiKey: string;
  maxRetries?: number;
  timeout?: number;
  baseDelay?: number;
  maxDelay?: number;
}

interface MessageRequest {
  model: string;
  messages: Array<{
    role: 'user' | 'assistant';
    content: string;
  }>;
  system?: string;
  maxTokens?: number;
  temperature?: number;
  [key: string]: unknown;
}

export class ClaudeAPIService {
  private client: Anthropic;
  private readonly maxRetries: number;
  private readonly baseDelay: number;
  private readonly maxDelay: number;

  constructor(config: ClaudeClientConfig) {
    this.client = new Anthropic({
      apiKey: config.apiKey,
      timeout: config.timeout ?? 60000,
      maxRetries: 0, // We handle retries manually
    });
    
    this.maxRetries = config.maxRetries ?? 3;
    this.baseDelay = config.baseDelay ?? 1000;
    this.maxDelay = config.maxDelay ?? 30000;
  }

  async createMessage(request: MessageRequest): Promise<string> {
    let lastError: Error | null = null;
    
    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      try {
        const response = await this.client.messages.create({
          model: request.model,
          messages: request.messages,
          system: request.system,
          max_tokens: request.maxTokens ?? 1024,
          temperature: request.temperature ?? 1.0,
        });
        
        return response.content[0].type === 'text' 
          ? response.content[0].text 
          : '';
      } catch (error) {
        lastError = error as Error;
        
        if (error instanceof RateLimitError) {
          const delay = this.calculateBackoff(attempt);
          await this.sleep(delay);
          continue;
        }
        
        if (error instanceof APIError && error.status === 429) {
          const delay = this.calculateBackoff(attempt);
          await this.sleep(delay);
          continue;
        }
        
        // Don't retry for non-retryable errors
        throw error;
      }
    }
    
    throw lastError;
  }

  private calculateBackoff(attempt: number): number {
    // Exponential backoff với jitter
    const exponentialDelay = this.baseDelay * Math.pow(2, attempt);
    const jitter = Math.random() * 1000;
    return Math.min(exponentialDelay + jitter, this.maxDelay);
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

## Error Handling

### Error Types

Claude API có thể trả về các loại lỗi sau:

1. **APIError** - Lỗi chung từ API (4xx, 5xx responses)
2. **RateLimitError** - Khi exceeds rate limits
3. **AuthenticationError** - Invalid hoặc missing API key
4. **InvalidRequestError** - Invalid request parameters
5. **TimeoutError** - Request timeout

### Error Handling Pattern

```python
from anthropic import (
    Anthropic,
    APIError,
    RateLimitError,
    AuthenticationError,
    InvalidRequestError,
)
from typing import Union

class ClaudeErrorHandler:
    """Centralized error handler cho Claude API operations."""
    
    @staticmethod
    def handle_error(error: Exception) -> dict:
        """Handle và categorize Claude API errors."""
        
        if isinstance(error, RateLimitError):
            return {
                "error_type": "rate_limit",
                "message": str(error),
                "retry_after": getattr(error, 'retry_after', None),
                "action": "retry_with_backoff"
            }
        
        if isinstance(error, AuthenticationError):
            return {
                "error_type": "authentication",
                "message": "Invalid API key or authentication failed",
                "action": "check_credentials"
            }
        
        if isinstance(error, InvalidRequestError):
            return {
                "error_type": "invalid_request",
                "message": str(error),
                "action": "fix_request_parameters"
            }
        
        if isinstance(error, APIError):
            return {
                "error_type": "api_error",
                "message": str(error),
                "status_code": error.status_code if hasattr(error, 'status_code') else None,
                "action": "log_and_notify"
            }
        
        # Unknown error
        return {
            "error_type": "unknown",
            "message": str(error),
            "action": "escalate"
        }
    
    @staticmethod
    def should_retry(error: Exception) -> bool:
        """Determine if an error is retryable."""
        retryable_errors = (
            RateLimitError,
            APIError,
        )
        
        if isinstance(error, APIError):
            # Only retry 5xx errors, not 4xx
            if hasattr(error, 'status_code'):
                return 500 <= error.status_code < 600
        
        return isinstance(error, retryable_errors)
```

### Retry Logic Implementation

```python
import asyncio
import random
from functools import wraps
from typing import Callable, TypeVar, ParamSpec
from anthropic import RateLimitError, APIError

P = ParamSpec('P')
T = TypeVar('T')

def async_retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exponential_base: float = 2.0,
):
    """Decorator cho async functions với exponential backoff retry logic."""
    
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except (RateLimitError, APIError) as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        break
                    
                    # Check if retryable
                    if isinstance(e, APIError):
                        if not (500 <= getattr(e, 'status_code', 0) < 600):
                            raise  # Don't retry 4xx except 429
                    
                    # Calculate delay với exponential backoff và jitter
                    delay = min(
                        base_delay * (exponential_base ** attempt),
                        max_delay
                    )
                    jitter = random.uniform(0, 1000) / 1000
                    delay = delay + jitter
                    
                    print(f"Retry attempt {attempt + 1}/{max_retries} "
                          f"after {delay:.2f}s delay. Error: {e}")
                    await asyncio.sleep(delay)
            
            raise last_exception
        
        return wrapper
    return decorator


# Usage
class ClaudeAsyncService:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
    
    @async_retry_with_backoff(max_retries=3, base_delay=2.0)
    async def generate_response(self, prompt: str) -> str:
        message = await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
```

## Rate Limits và Quota Management

### Understanding Rate Limits

Claude API có các rate limits khác nhau tùy thuộc vào subscription tier:

| Tier | Requests/min | Tokens/min | Concurrent |
|------|-------------|------------|------------|
| Free | 5 | 10,000 | 1 |
| Pro | 50 | 80,000 | 5 |
| Team | 100 | 200,000 | 10 |
| Enterprise | Custom | Custom | Custom |

### Rate Limit Handling

```typescript
interface RateLimitConfig {
  requestsPerMinute: number;
  tokensPerMinute: number;
  maxConcurrent: number;
}

class RateLimitedClient {
  private requestQueue: Promise<void>[] = [];
  private tokensUsed: number = 0;
  private lastReset: number = Date.now();
  
  constructor(
    private client: Anthropic,
    private config: RateLimitConfig
  ) {
    // Start token reset interval
    setInterval(() => this.resetTokens(), 60000);
  }
  
  private async acquireSlot(): Promise<void> {
    // Wait if at concurrent limit
    while (this.requestQueue.length >= this.config.maxConcurrent) {
      await this.requestQueue.shift();
    }
    
    // Check token limit
    while (this.tokensUsed >= this.config.tokensPerMinute) {
      const waitTime = 60000 - (Date.now() - this.lastReset);
      if (waitTime > 0) {
        await new Promise(resolve => setTimeout(resolve, waitTime));
        this.resetTokens();
      }
    }
  }
  
  private resetTokens(): void {
    this.tokensUsed = 0;
    this.lastReset = Date.now();
  }
  
  async createMessage(params: {
    model: string;
    messages: Array<{ role: string; content: string }>;
    maxTokens: number;
  }): Promise<string> {
    await this.acquireSlot();
    
    const response = await this.client.messages.create({
      ...params,
      extraHeaders: {
        'anthropic-dangerous-direct-browser-access': 'true',
      },
    });
    
    this.tokensUsed += response.usage.input_tokens + 
                      response.usage.output_tokens;
    
    return response.content[0].text;
  }
}
```

### Token Budgeting

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class TokenBudget:
    """Token budget tracker cho Claude API usage."""
    
    daily_limit: int
    monthly_limit: int
    warning_threshold: float = 0.8
    
    _daily_used: int = 0
    _monthly_used: int = 0
    _last_reset: str = ""  # date string
    
    def check_budget(self, required_tokens: int) -> tuple[bool, Optional[str]]:
        """Check if request fits within budget."""
        import datetime
        
        today = datetime.date.today().isoformat()
        
        # Reset daily if new day
        if self._last_reset != today:
            self._daily_used = 0
            self._last_reset = today
        
        # Check daily limit
        if self._daily_used + required_tokens > self.daily_limit:
            return False, "Daily token limit exceeded"
        
        # Check monthly limit
        if self._monthly_used + required_tokens > self.monthly_limit:
            return False, "Monthly token limit exceeded"
        
        # Check warning threshold
        daily_pct = (self._daily_used + required_tokens) / self.daily_limit
        monthly_pct = (self._monthly_used + required_tokens) / self.monthly_limit
        
        if daily_pct >= self.warning_threshold:
            return True, f"Warning: Daily usage at {daily_pct:.0%}"
        
        return True, None
    
    def record_usage(self, tokens: int):
        """Record token usage after API call."""
        self._daily_used += tokens
        self._monthly_used += tokens
    
    @property
    def remaining_daily(self) -> int:
        return max(0, self.daily_limit - self._daily_used)
    
    @property
    def remaining_monthly(self) -> int:
        return max(0, self.monthly_limit - self._monthly_used)
```

## Common Patterns

### Pattern 1: Singleton Client

```python
# config.py
import os
from functools import lru_cache
from anthropic import Anthropic

@lru_cache(maxsize=1)
def get_claude_client() -> Anthropic:
    """Get singleton Claude client instance."""
    return Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        timeout=60.0,
        max_retries=3,
    )

# usage.py
from config import get_claude_client

def some_function():
    client = get_claude_client()
    response = client.messages.create(...)
```

### Pattern 2: Factory Pattern cho Different Models

```python
from anthropic import Anthropic
from typing import Literal
from dataclasses import dataclass

@dataclass
class ModelConfig:
    name: str
    max_tokens: int
    temperature: float
    description: str

class ClaudeModelFactory:
    """Factory for creating configured Claude API clients."""
    
    MODELS = {
        "fast": ModelConfig(
            name="claude-3-5-haiku-20241022",
            max_tokens=1024,
            temperature=0.7,
            description="Fast, cost-effective for simple tasks"
        ),
        "balanced": ModelConfig(
            name="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            temperature=1.0,
            description="Balanced performance and cost"
        ),
        "powerful": ModelConfig(
            name="claude-3-opus-20240229",
            max_tokens=4096,
            temperature=1.0,
            description="Most capable, higher cost"
        ),
    }
    
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
    
    def get_model(self, use_case: Literal["fast", "balanced", "powerful"]):
        return self.MODELS[use_case]
    
    async def generate(
        self,
        prompt: str,
        use_case: Literal["fast", "balanced", "powerful"] = "balanced",
        system: str | None = None,
    ) -> str:
        config = self.get_model(use_case)
        
        response = await self.client.messages.create(
            model=config.name,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=config.max_tokens,
            temperature=config.temperature,
        )
        
        return response.content[0].text
```

### Pattern 3: Circuit Breaker Pattern

```typescript
enum CircuitState {
  CLOSED = 'CLOSED',
  OPEN = 'OPEN',
  HALF_OPEN = 'HALF_OPEN',
}

interface CircuitBreakerConfig {
  failureThreshold: number;
  successThreshold: number;
  timeout: number; // ms
}

class CircuitBreaker {
  private state: CircuitState = CircuitState.CLOSED;
  private failures: number = 0;
  private successes: number = 0;
  private nextAttempt: number = Date.now();
  
  constructor(private config: CircuitBreakerConfig) {}
  
  async execute<T>(operation: () => Promise<T>): Promise<T> {
    if (this.state === CircuitState.OPEN) {
      if (Date.now() < this.nextAttempt) {
        throw new Error('Circuit breaker is OPEN');
      }
      this.state = CircuitState.HALF_OPEN;
    }
    
    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  private onSuccess(): void {
    this.failures = 0;
    this.successes++;
    
    if (this.state === CircuitState.HALF_OPEN) {
      if (this.successes >= this.config.successThreshold) {
        this.state = CircuitState.CLOSED;
        this.successes = 0;
      }
    }
  }
  
  private onFailure(): void {
    this.failures++;
    this.successes = 0;
    
    if (this.failures >= this.config.failureThreshold) {
      this.state = CircuitState.OPEN;
      this.nextAttempt = Date.now() + this.config.timeout;
    }
  }
}
```

## Best Practices

### 1. Security Best Practices

- **Luôn sử dụng environment variables** cho API keys, không hardcode
- **Implement key rotation** định kỳ (recommend: 90 ngày)
- **Sử dụng secret management** như AWS Secrets Manager, HashiCorp Vault
- **Enable API access logs** và monitoring
- **Implement IP whitelisting** nếu có thể

### 2. Performance Best Practices

- **Use connection pooling** để reuse HTTP connections
- **Implement caching** cho repeated queries
- **Batch requests** khi có thể
- **Use streaming** cho long responses để improve perceived latency
- **Monitor token usage** để optimize costs

### 3. Reliability Best Practices

- **Implement retry logic** với exponential backoff
- **Use circuit breakers** để prevent cascade failures
- **Set appropriate timeouts** cho different operations
- **Implement fallback mechanisms** (fallback to cache, alternative model)
- **Log all API interactions** cho debugging và auditing

### 4. Cost Optimization

- **Use appropriate model** cho từng use case (không dùng Opus cho simple tasks)
- **Implement token budgeting** và monitoring
- **Cache responses** cho identical queries
- **Use streaming** để allow early termination if needed

## Troubleshooting

### Common Issues và Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `AuthenticationError` | Invalid API key | Verify key in environment |
| `RateLimitError` | Too many requests | Implement backoff, check quotas |
| `InvalidRequestError` | Invalid parameters | Check request format, model name |
| `TimeoutError` | Network/server issue | Increase timeout, check network |
| `ContextLengthExceeded` | Prompt too long | Implement truncation, chunking |

### Debugging Tips

```python
import logging
from anthropic import Anthropic

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('anthropic').setLevel(logging.DEBUG)

# Log all requests
client = Anthropic()

# Custom logging middleware
class LoggingMiddleware:
    def __init__(self, client: Anthropic):
        self.client = client
    
    def create_message(self, *args, **kwargs):
        print(f"Request: model={kwargs.get('model')}, "
              f"max_tokens={kwargs.get('max_tokens')}")
        
        response = self.client.messages.create(*args, **kwargs)
        
        print(f"Response: usage={response.usage}")
        return response
```

### Health Check Implementation

```python
from anthropic import Anthropic, APIError
import time

class ClaudeHealthCheck:
    """Health check cho Claude API integration."""
    
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
    
    async def check(self) -> dict:
        """Perform health check."""
        start = time.time()
        
        try:
            response = await self.client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}],
            )
            
            return {
                "status": "healthy",
                "latency_ms": int((time.time() - start) * 1000),
                "model": response.model,
            }
        except APIError as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "latency_ms": int((time.time() - start) * 1000),
            }
```

## References

- [Anthropic Documentation](https://docs.anthropic.com/)
- [Claude API Reference](https://docs.anthropic.com/claude/reference)
- [Python SDK GitHub](https://github.com/anthropics/anthropic-sdk-python)
- [TypeScript SDK GitHub](https://github.com/anthropics/anthropic-sdk-typescript)
- [Rate Limits Documentation](https://docs.anthropic.com/claude/reference/rate-limits)
