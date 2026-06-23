---
title: OpenAI API Integration
description: Hướng dẫn toàn diện về tích hợp OpenAI API, quản lý API keys, rate limits, error handling và retry patterns
tags: [openai, api, integration, typescript, python, enterprise]
created: 2026-06-23
version: 1.0.0
framework: cursor-enterprise
---

# OpenAI API Integration

## Tổng quan

Tài liệu này cung cấp hướng dẫn toàn diện về cách tích hợp OpenAI API vào các ứng dụng enterprise. Việc tích hợp OpenAI API đòi hỏi sự hiểu biết sâu về cách quản lý credentials, xử lý rate limits, và implement các chiến lược retry hiệu quả để đảm bảo ứng dụng hoạt động ổn định trong môi trường production.

OpenAI cung cấp nhiều loại API khác nhau bao gồm Chat Completions, Completions, Embeddings, Fine-tuning, Assistants, và các API multimedia. Mỗi loại API có các đặc điểm riêng về authentication, rate limits, và cách sử dụng. Trong tài liệu này, chúng ta sẽ tập trung vào các pattern chung áp dụng cho tất cả các loại API của OpenAI.

Việc tích hợp API không chỉ đơn thuần là gọi endpoint. Trong thực tế enterprise, bạn cần consider đến security (quản lý API keys an toàn), reliability (xử lý lỗi và retry), scalability (quản lý rate limits), observability (logging và monitoring), và cost optimization (giảm thiểu chi phí). Tất cả những yếu tố này sẽ được covered trong tài liệu.

## Mục đích và Phạm vi

Tài liệu này được thiết kế để giúp các development teams hiểu và implement các best practices cho việc tích hợp OpenAI API. Phạm vi bao gồm từ việc setup ban đầu, cấu hình client, cho đến các kỹ thuật xử lý lỗi nâng cao và tối ưu hóa chi phí. Chúng tôi sẽ cung cấp code examples cho cả TypeScript và Python để phù hợp với different tech stacks.

Đối tượng mục tiêu bao gồm backend developers, full-stack developers, DevOps engineers, và technical architects đang làm việc với các ứng dụng cần tích hợp AI capabilities. Kiến thức cơ bản về REST APIs và asynchronous programming là yêu cầu tiên quyết.

## Các Khái niệm Chính

### OpenAI API Architecture

OpenAI API được thiết kế theo kiến trúc RESTful với JSON-based requests và responses. Tất cả các API calls đều phải được authenticated thông qua API keys và phải tuân thủ các rate limits được quy định. Hiểu rõ architecture này giúp bạn design solution tốt hơn.

API endpoint chính của OpenAI là `https://api.openai.com/v1`. Tất cả các API calls đều phải được thực hiện qua HTTPS với TLS 1.2 trở lên. Response format nhất quán across all endpoints với các trường như `id`, `object`, `created`, `model`, và `usage` cho metadata.

OpenAI sử dụng token-based pricing model. Mỗi request tiêu tốn tokens cho cả input và output. Việc đếm và tối ưu hóa token usage là critical cho cost management. Bạn nên implement token tracking từ đầu để tránh surprise bills.

### Authentication và Security

Authentication trong OpenAI API được thực hiện thông qua Bearer token scheme. API key được passed trong Authorization header của mỗi request. Đây là phương thức authentication đơn giản nhưng đòi hỏi việc bảo mật chặt chẽ API keys.

API keys của OpenAI có các cấp độ khác nhau tùy thuộc vào loại key. Organization keys cho phép quản lý permissions và billing ở cấp organization, trong khi User keys được sử dụng cho các use cases cá nhân. Trong môi trường enterprise, bạn nên sử dụng organization keys với proper IAM controls.

Việc rotation API keys định kỳ là best practice bảo mật. OpenAI hỗ trợ multiple active keys cho phép rotation không downtime. Bạn nên implement key rotation mechanism trong configuration management system.

### Rate Limits và Quotas

OpenAI áp dụng rate limits khác nhau cho different subscription tiers và API endpoints. Rate limits được measured bằng requests per minute (RPM) và tokens per minute (TPM). Understanding these limits là essential để design systems that won't hit throttling.

Default rate limits cho Chat Completions API trên Pay-as-you-go tier là 3 RPM và 150,000 TPM cho gpt-4o model. Tuy nhiên, bạn có thể request increase rate limits thông qua dashboard hoặc support. Enterprise customers có higher limits by default.

Rate limit headers được trả về trong mỗi response: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, và `Retry-After`. Bạn nên parse these headers để implement adaptive throttling logic trong application.

### Error Types và Handling

OpenAI API trả về different error types với specific HTTP status codes. Understanding these errors giúp bạn implement appropriate handling logic. Các error types chính bao gồm 4xx client errors và 5xx server errors.

Authentication errors (401) xảy ra khi API key không hợp lệ hoặc không có permission. Rate limit errors (429) indicate rằng bạn đã vượt quá rate limit. Server errors (500, 502, 503) là temporary issues có thể được resolve với retries.

Error response format nhất quán với `error` object chứa `message`, `type`, `code`, và `param` fields. Code field đặc biệt hữu ích cho programmatic error handling vì nó cung cấp machine-readable error codes như `invalid_api_key`, `rate_limit_exceeded`, hoặc `server_error`.

## Cấu hình Client và Setup

### TypeScript Client Setup

```typescript
import OpenAI from 'openai';

// Basic client configuration
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  organization: process.env.OPENAI_ORG_ID,
});

// Client with custom timeout and retry configuration
const openaiConfigured = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  organization: process.env.OPENAI_ORG_ID,
  timeout: 60000, // 60 seconds
  maxRetries: 3,
  defaultHeaders: {
    'X-App-Name': 'my-enterprise-app',
    'X-App-Version': process.env.APP_VERSION,
  },
});

// Client with custom base URL (for proxies or testing)
const openaiProxy = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: 'https://api.openai.com/v1', // or custom proxy URL
});
```

### Python Client Setup

```python
from openai import OpenAI
from openai._client import OpenAI as SyncClient
import os

# Basic client configuration
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    organization=os.environ.get("OPENAI_ORG_ID"),
)

# Client with custom timeout configuration
client_configured = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    organization=os.environ.get("OPENAI_ORG_ID"),
    timeout=60.0,  # 60 seconds
    max_retries=3,
    default_headers={
        "X-App-Name": "my-enterprise-app",
        "X-App-Version": os.environ.get("APP_VERSION", "1.0.0"),
    },
)

# Async client for high-performance applications
from openai import AsyncOpenAI

async_client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    max_retries=3,
)
```

### Environment Configuration

```typescript
// config/openai.ts - TypeScript configuration module
import OpenAI from 'openai';

interface OpenAIConfig {
  apiKey: string;
  organizationId: string | undefined;
  baseURL: string;
  timeout: number;
  maxRetries: number;
  defaultModel: string;
  maxTokensPerMinute: number;
  requestsPerMinute: number;
}

function getOpenAIConfig(): OpenAIConfig {
  // Validate required environment variables
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    throw new Error('OPENAI_API_KEY environment variable is required');
  }

  return {
    apiKey,
    organizationId: process.env.OPENAI_ORG_ID,
    baseURL: process.env.OPENAI_BASE_URL || 'https://api.openai.com/v1',
    timeout: parseInt(process.env.OPENAI_TIMEOUT || '60000', 10),
    maxRetries: parseInt(process.env.OPENAI_MAX_RETRIES || '3', 10),
    defaultModel: process.env.OPENAI_DEFAULT_MODEL || 'gpt-4o',
    maxTokensPerMinute: parseInt(process.env.OPENAI_TPM_LIMIT || '150000', 10),
    requestsPerMinute: parseInt(process.env.OPENAI_RPM_LIMIT || '500', 10),
  };
}

export function createOpenAIClient(): OpenAI {
  const config = getOpenAIConfig();
  
  return new OpenAI({
    apiKey: config.apiKey,
    organization: config.organizationId,
    baseURL: config.baseURL,
    timeout: config.timeout,
    maxRetries: config.maxRetries,
  });
}

export const openaiConfig = getOpenAIConfig();
```

```python
# config/openai_config.py - Python configuration module
import os
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class OpenAIConfig:
    api_key: str
    organization_id: Optional[str] = None
    base_url: str = 'https://api.openai.com/v1'
    timeout: float = 60.0
    max_retries: int = 3
    default_model: str = 'gpt-4o'
    max_tokens_per_minute: int = 150000
    requests_per_minute: int = 500

def get_openai_config() -> OpenAIConfig:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    return OpenAIConfig(
        api_key=api_key,
        organization_id=os.environ.get("OPENAI_ORG_ID"),
        base_url=os.environ.get("OPENAI_BASE_URL", 'https://api.openai.com/v1'),
        timeout=float(os.environ.get("OPENAI_TIMEOUT", "60.0")),
        max_retries=int(os.environ.get("OPENAI_MAX_RETRIES", "3")),
        default_model=os.environ.get("OPENAI_DEFAULT_MODEL", "gpt-4o"),
        max_tokens_per_minute=int(os.environ.get("OPENAI_TPM_LIMIT", "150000")),
        requests_per_minute=int(os.environ.get("OPENAI_RPM_LIMIT", "500")),
    )

def create_openai_client() -> OpenAI:
    from openai import OpenAI
    config = get_openai_config()
    
    return OpenAI(
        api_key=config.api_key,
        organization=config.organization_id,
        base_url=config.base_url,
        timeout=config.timeout,
        max_retries=config.max_retries,
    )
```

## Token Counting và Cost Management

### Token Counting Utilities

```typescript
// utils/tokenCounter.ts - Token counting utilities
import { encoding_for_model, type TiktokenEncoding } from 'tiktoken';

const MODEL_TOKEN_LIMITS: Record<string, number> = {
  'gpt-4o': 128000,
  'gpt-4-turbo': 128000,
  'gpt-4': 8192,
  'gpt-3.5-turbo': 16385,
  'o1-preview': 128000,
  'o1-mini': 65536,
};

interface TokenCount {
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
}

export function countTokens(
  text: string,
  model: string = 'gpt-4o'
): number {
  try {
    const encoding = encoding_for_model('gpt-4o' as TiktokenEncoding);
    const tokens = encoding.encode(text);
    encoding.free();
    return tokens.length;
  } catch {
    // Fallback: rough estimation (1 token ≈ 4 characters)
    return Math.ceil(text.length / 4);
  }
}

export function countMessagesTokens(
  messages: Array<{
    role: 'system' | 'user' | 'assistant';
    content: string;
  }>,
  model: string = 'gpt-4o'
): TokenCount {
  let promptTokens = 0;
  
  // Base tokens per message
  const tokensPerMessage = 3;
  const tokensPerName = 1;
  
  for (const message of messages) {
    promptTokens += tokensPerMessage;
    promptTokens += countTokens(message.role);
    promptTokens += countTokens(message.content);
    if (message.role === 'system') {
      // System messages have additional overhead
      promptTokens += 3;
    }
  }
  
  // Add overhead for message format
  promptTokens += 3;
  
  return {
    promptTokens,
    completionTokens: 0,
    totalTokens: promptTokens,
  };
}

export function estimateCost(
  tokens: TokenCount,
  model: string,
  pricing: { inputPer1M: number; outputPer1M: number } = {
    inputPer1M: 2.5, // gpt-4o pricing
    outputPer1M: 10.0,
  }
): number {
  const inputCost = (tokens.promptTokens / 1_000_000) * pricing.inputPer1M;
  const outputCost = (tokens.completionTokens / 1_000_000) * pricing.outputPer1M;
  return inputCost + outputCost;
}

export function getModelContextLimit(model: string): number {
  return MODEL_TOKEN_LIMITS[model] || 4096;
}

export function truncateToContextLimit(
  text: string,
  model: string = 'gpt-4o'
): string {
  const maxTokens = getModelContextLimit(model) - 1000; // Reserve for response
  let tokenCount = countTokens(text, model);
  
  if (tokenCount <= maxTokens) {
    return text;
  }
  
  // Binary search for truncation point
  let low = 0;
  let high = text.length;
  
  while (low < high) {
    const mid = Math.floor((low + high + 1) / 2);
    const truncated = text.substring(0, mid);
    tokenCount = countTokens(truncated, model);
    
    if (tokenCount <= maxTokens) {
      low = mid;
    } else {
      high = mid - 1;
    }
  }
  
  return text.substring(0, low);
}
```

```python
# utils/token_counter.py - Token counting utilities
import tiktoken
from typing import Dict, List, Optional, TypedDict
from dataclasses import dataclass

MODEL_TOKEN_LIMITS = {
    'gpt-4o': 128000,
    'gpt-4-turbo': 128000,
    'gpt-4': 8192,
    'gpt-3.5-turbo': 16385,
    'o1-preview': 128000,
    'o1-mini': 65536,
}

@dataclass
class TokenCount:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

def count_tokens(text: str, model: str = 'gpt-4o') -> int:
    """Count tokens for a given text using tiktoken."""
    try:
        encoding = tiktoken.encoding_for_model('gpt-4o')
        tokens = encoding.encode(text)
        return len(tokens)
    except KeyError:
        # Fallback for models without specific encoding
        encoding = tiktoken.get_encoding('cl100k_base')
        tokens = encoding.encode(text)
        return len(tokens)

def count_messages_tokens(
    messages: List[Dict[str, str]],
    model: str = 'gpt-4o'
) -> TokenCount:
    """Count tokens for a list of messages."""
    prompt_tokens = 0
    tokens_per_message = 3  # Base tokens per message
    tokens_per_name = 1
    
    for message in messages:
        prompt_tokens += tokens_per_message
        prompt_tokens += count_tokens(message.get('role', ''))
        prompt_tokens += count_tokens(message.get('content', ''))
        if 'name' in message:
            prompt_tokens += tokens_per_name
        if message.get('role') == 'system':
            prompt_tokens += 3  # Additional overhead for system messages
    
    # Overhead for message format
    prompt_tokens += 3
    
    return TokenCount(
        prompt_tokens=prompt_tokens,
        completion_tokens=0,
        total_tokens=prompt_tokens
    )

def estimate_cost(
    tokens: TokenCount,
    model: str = 'gpt-4o',
    pricing: Optional[Dict[str, float]] = None
) -> float:
    """Estimate cost for token usage."""
    if pricing is None:
        pricing = {
            'gpt-4o': {'input_per_1m': 2.5, 'output_per_1m': 10.0},
            'gpt-4o-mini': {'input_per_1m': 0.15, 'output_per_1m': 0.6},
            'gpt-4-turbo': {'input_per_1m': 10.0, 'output_per_1m': 30.0},
        }
    
    model_pricing = pricing.get(model, {'input_per_1m': 2.5, 'output_per_1m': 10.0})
    
    input_cost = (tokens.prompt_tokens / 1_000_000) * model_pricing['input_per_1m']
    output_cost = (tokens.completion_tokens / 1_000_000) * model_pricing['output_per_1m']
    
    return input_cost + output_cost

def get_model_context_limit(model: str) -> int:
    """Get the context window limit for a model."""
    return MODEL_TOKEN_LIMITS.get(model, 4096)

def truncate_to_context_limit(text: str, model: str = 'gpt-4o') -> str:
    """Truncate text to fit within model's context limit."""
    max_tokens = get_model_context_limit(model) - 1000  # Reserve for response
    
    if count_tokens(text, model) <= max_tokens:
        return text
    
    # Binary search for truncation point
    low, high = 0, len(text)
    
    while low < high:
        mid = (low + high + 1) // 2
        truncated = text[:mid]
        
        if count_tokens(truncated, model) <= max_tokens:
            low = mid
        else:
            high = mid - 1
    
    return text[:low]
```

## Error Handling và Retry Patterns

### Comprehensive Error Handling

```typescript
// errors/openaiError.ts - Custom error types
export class OpenAIAPIError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number,
    public readonly code: string,
    public readonly param: string | null,
    public readonly type: string
  ) {
    super(message);
    this.name = 'OpenAIAPIError';
  }
}

export class RateLimitError extends OpenAIAPIError {
  constructor(
    message: string,
    public readonly retryAfter: number,
    public readonly limit: number,
    public readonly remaining: number,
    public readonly resetAt: Date
  ) {
    super(message, 429, 'rate_limit_exceeded', null, 'rate_limit');
    this.name = 'RateLimitError';
  }
}

export class AuthenticationError extends OpenAIAPIError {
  constructor(message: string) {
    super(message, 401, 'invalid_api_key', null, 'authentication');
    this.name = 'AuthenticationError';
  }
}

export class InsufficientQuotaError extends OpenAIAPIError {
  constructor(message: string, public readonly maxTokens: number) {
    super(message, 429, 'insufficient_quota', null, 'quota');
    this.name = 'InsufficientQuotaError';
  }
}

export class ContextLengthExceededError extends OpenAIAPIError {
  constructor(
    message: string,
    public readonly maxTokens: number,
    public readonly requestedTokens: number
  ) {
    super(message, 400, 'context_length_exceeded', null, 'invalid_request');
    this.name = 'ContextLengthExceededError';
  }
}

export class ModelNotFoundError extends OpenAIAPIError {
  constructor(message: string, public readonly model: string) {
    super(message, 404, 'model_not_found', null, 'invalid_request');
    this.name = 'ModelNotFoundError';
  }
}
```

```python
# errors/openai_errors.py - Custom error types
from typing import Optional, Dict, Any
from datetime import datetime

class OpenAIAPIError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int,
        code: str,
        param: Optional[str] = None,
        error_type: str = 'api_error'
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.param = param
        self.type = error_type

    def to_dict(self) -> Dict[str, Any]:
        return {
            'message': self.message,
            'status_code': self.status_code,
            'code': self.code,
            'param': self.param,
            'type': self.type,
        }

class RateLimitError(OpenAIAPIError):
    def __init__(
        self,
        message: str,
        retry_after: int,
        limit: int,
        remaining: int,
        reset_at: datetime
    ):
        super__(
            message,
            429,
            'rate_limit_exceeded',
            error_type='rate_limit'
        )
        self.retry_after = retry_after
        self.limit = limit
        self.remaining = remaining
        self.reset_at = reset_at

class AuthenticationError(OpenAIAPIError):
    def __init__(self, message: str):
        super__(message, 401, 'invalid_api_key', error_type='authentication')

class InsufficientQuotaError(OpenAIAPIError):
    def __init__(self, message: str, max_tokens: int):
        super__(message, 429, 'insufficient_quota', error_type='quota')
        self.max_tokens = max_tokens

class ContextLengthExceededError(OpenAIAPIError):
    def __init__(
        self,
        message: str,
        max_tokens: int,
        requested_tokens: int
    ):
        super__(message, 400, 'context_length_exceeded', error_type='invalid_request')
        self.max_tokens = max_tokens
        self.requested_tokens = requested_tokens

class ModelNotFoundError(OpenAIAPIError):
    def __init__(self, message: str, model: str):
        super__(message, 404, 'model_not_found', error_type='invalid_request')
        self.model = model
```

### Retry Logic với Exponential Backoff

```typescript
// utils/retry.ts - Retry utilities with exponential backoff
import { OpenAI } from 'openai';
import {
  RateLimitError,
  AuthenticationError,
  ContextLengthExceededError,
} from '../errors/openaiError';

interface RetryConfig {
  maxRetries: number;
  initialDelayMs: number;
  maxDelayMs: number;
  backoffMultiplier: number;
  retryableStatusCodes: number[];
  retryableErrorCodes: string[];
}

const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxRetries: 3,
  initialDelayMs: 1000,
  maxDelayMs: 30000,
  backoffMultiplier: 2,
  retryableStatusCodes: [408, 429, 500, 502, 503, 504],
  retryableErrorCodes: [
    'rate_limit_exceeded',
    'server_error',
    'timeout',
    'connection_error',
  ],
};

function isRetryable(error: any): boolean {
  if (error.status) {
    return DEFAULT_RETRY_CONFIG.retryableStatusCodes.includes(error.status);
  }
  if (error.code) {
    return DEFAULT_RETRY_CONFIG.retryableErrorCodes.includes(error.code);
  }
  return false;
}

function calculateDelay(
  attempt: number,
  config: RetryConfig,
  retryAfter?: number
): number {
  if (retryAfter) {
    return Math.min(retryAfter * 1000, config.maxDelayMs);
  }
  
  const exponentialDelay = config.initialDelayMs * Math.pow(config.backoffMultiplier, attempt);
  const jitter = Math.random() * 0.3 * exponentialDelay; // 0-30% jitter
  return Math.min(exponentialDelay + jitter, config.maxDelayMs);
}

export async function withRetry<T>(
  operation: () => Promise<T>,
  config: Partial<RetryConfig> = {},
  onRetry?: (attempt: number, error: any, delay: number) => void
): Promise<T> {
  const mergedConfig = { ...DEFAULT_RETRY_CONFIG, ...config };
  let lastError: any;
  
  for (let attempt = 0; attempt <= mergedConfig.maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error: any) {
      lastError = error;
      
      // Don't retry on non-retryable errors
      if (!isRetryable(error)) {
        throw error;
      }
      
      // Don't retry on final attempt
      if (attempt === mergedConfig.maxRetries) {
        break;
      }
      
      const retryAfter = error.headers?.['retry-after'];
      const delay = calculateDelay(attempt, mergedConfig, retryAfter);
      
      if (onRetry) {
        onRetry(attempt + 1, error, delay);
      }
      
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw lastError;
}

export function createRetryableOpenAI(client: OpenAI) {
  return {
    async chat.completions.create(
      params: Parameters<typeof client.chat.completions.create>[0],
      options?: { retries?: number }
    ) {
      return withRetry(
        () => client.chat.completions.create(params),
        { maxRetries: options?.retries ?? DEFAULT_RETRY_CONFIG.maxRetries }
      );
    },
    
    async embeddings.create(
      params: Parameters<typeof client.embeddings.create>[0]
    ) {
      return withRetry(
        () => client.embeddings.create(params)
      );
    },
  };
}
```

```python
# utils/retry.py - Retry utilities with exponential backoff
import time
import random
from typing import Callable, TypeVar, Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

T = TypeVar('T')

@dataclass
class RetryConfig:
    max_retries: int = 3
    initial_delay_ms: float = 1000.0
    max_delay_ms: float = 30000.0
    backoff_multiplier: float = 2.0
    retryable_status_codes: List[int] = field(default_factory=lambda: [408, 429, 500, 502, 503, 504])
    retryable_error_codes: List[str] = field(default_factory=lambda: [
        'rate_limit_exceeded', 'server_error', 'timeout', 'connection_error'
    ])

def is_retryable(error: Exception) -> bool:
    """Determine if an error is retryable."""
    if hasattr(error, 'status_code'):
        return error.status_code in [429, 500, 502, 503, 504]
    if hasattr(error, 'code'):
        return error.code in ['rate_limit_exceeded', 'server_error', 'timeout']
    return False

def calculate_delay(
    attempt: int,
    config: RetryConfig,
    retry_after: Optional[float] = None
) -> float:
    """Calculate delay for the next retry with exponential backoff and jitter."""
    if retry_after:
        return min(retry_after, config.max_delay_ms / 1000)
    
    exponential_delay = config.initial_delay_ms * (config.backoff_multiplier ** attempt)
    jitter = random.uniform(0, 0.3) * exponential_delay
    delay_ms = min(exponential_delay + jitter, config.max_delay_ms)
    
    return delay_ms / 1000

def with_retry(
    operation: Callable[[], T],
    config: Optional[RetryConfig] = None,
    on_retry: Optional[Callable[[int, Exception, float], None]] = None
) -> T:
    """Execute an operation with retry logic and exponential backoff."""
    if config is None:
        config = RetryConfig()
    
    last_error: Optional[Exception] = None
    
    for attempt in range(config.max_retries + 1):
        try:
            return operation()
        except Exception as error:
            last_error = error
            
            if not is_retryable(error):
                raise
            
            if attempt == config.max_retries:
                break
            
            retry_after = getattr(error, 'retry_after', None)
            delay = calculate_delay(attempt, config, retry_after)
            
            if on_retry:
                on_retry(attempt + 1, error, delay)
            
            time.sleep(delay)
    
    raise last_error

class RetryableOpenAIClient:
    """Wrapper for OpenAI client with automatic retry logic."""
    
    def __init__(self, client, max_retries: int = 3):
        self.client = client
        self.max_retries = max_retries
    
    def chat_completions_create(self, **params):
        """Create chat completion with retry logic."""
        return with_retry(
            lambda: self.client.chat.completions.create(**params),
            RetryConfig(max_retries=self.max_retries)
        )
    
    def embeddings_create(self, **params):
        """Create embeddings with retry logic."""
        return with_retry(
            lambda: self.client.embeddings.create(**params),
            RetryConfig(max_retries=self.max_retries)
        )
```

## Best Practices cho Production

### Rate Limit Management

```typescript
// services/rateLimiter.ts - Token bucket rate limiter
import { EventEmitter } from 'events';

interface RateLimitState {
  tokens: number;
  lastRefill: number;
  requestsInFlight: number;
}

export class TokenBucketRateLimiter extends EventEmitter {
  private state: RateLimitState;
  private readonly maxTokens: number;
  private readonly refillRate: number; // tokens per second
  private readonly maxConcurrent: number;
  
  constructor(
    maxTokensPerMinute: number,
    requestsPerMinute: number,
    maxConcurrent: number = 10
  ) {
    super();
    this.maxTokens = maxTokensPerMinute;
    this.refillRate = maxTokensPerMinute / 60;
    this.maxConcurrent = maxConcurrent;
    this.state = {
      tokens: maxTokensPerMinute,
      lastRefill: Date.now(),
      requestsInFlight: 0,
    };
  }
  
  private refill(): void {
    const now = Date.now();
    const elapsed = (now - this.state.lastRefill) / 1000;
    const tokensToAdd = elapsed * this.refillRate;
    
    this.state.tokens = Math.min(this.maxTokens, this.state.tokens + tokensToAdd);
    this.state.lastRefill = now;
  }
  
  async acquire(estimatedTokens: number): Promise<void> {
    while (true) {
      this.refill();
      
      if (
        this.state.tokens >= estimatedTokens &&
        this.state.requestsInFlight < this.maxConcurrent
      ) {
        this.state.tokens -= estimatedTokens;
        this.state.requestsInFlight++;
        return;
      }
      
      const waitTime = Math.max(
        (estimatedTokens - this.state.tokens) / this.refillRate * 1000,
        100
      );
      
      await new Promise(resolve => setTimeout(resolve, waitTime));
      this.refill();
    }
  }
  
  release(tokensUsed: number): void {
    this.state.requestsInFlight--;
    this.state.tokens = Math.min(
      this.maxTokens,
      this.state.tokens + tokensUsed
    );
    this.emit('release', { tokensUsed, remaining: this.state.tokens });
  }
  
  getStatus(): { tokens: number; inFlight: number } {
    this.refill();
    return {
      tokens: Math.floor(this.state.tokens),
      inFlight: this.state.requestsInFlight,
    };
  }
}

// Global rate limiter instance
export const rateLimiter = new TokenBucketRateLimiter(
  parseInt(process.env.OPENAI_TPM_LIMIT || '150000', 10),
  parseInt(process.env.OPENAI_RPM_LIMIT || '500', 10),
  10
);
```

```python
# services/rate_limiter.py - Token bucket rate limiter
import time
import threading
from typing import Optional
from dataclasses import dataclass
from threading import Lock

@dataclass
class RateLimitState:
    tokens: float
    last_refill: float
    requests_in_flight: int

class TokenBucketRateLimiter:
    """Token bucket rate limiter for OpenAI API calls."""
    
    def __init__(
        self,
        max_tokens_per_minute: int,
        requests_per_minute: int,
        max_concurrent: int = 10
    ):
        self.max_tokens = max_tokens_per_minute
        self.refill_rate = max_tokens_per_minute / 60.0
        self.max_concurrent = max_concurrent
        self.state = RateLimitState(
            tokens=max_tokens_per_minute,
            last_refill=time.time(),
            requests_in_flight=0
        )
        self.lock = Lock()
        self.callbacks = []
    
    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.state.last_refill
        tokens_to_add = elapsed * self.refill_rate
        
        self.state.tokens = min(self.max_tokens, self.state.tokens + tokens_to_add)
        self.state.last_refill = now
    
    def acquire(self, estimated_tokens: int, timeout: Optional[float] = 60.0) -> None:
        """Acquire tokens for a request."""
        start_time = time.time()
        
        while True:
            with self.lock:
                self._refill()
                
                if (
                    self.state.tokens >= estimated_tokens and
                    self.state.requests_in_flight < self.max_concurrent
                ):
                    self.state.tokens -= estimated_tokens
                    self.state.requests_in_flight += 1
                    return
                
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    raise TimeoutError(f"Rate limiter timeout after {elapsed:.2f}s")
            
                wait_time = max(
                    (estimated_tokens - self.state.tokens) / self.refill_rate * 1000,
                    100
                ) / 1000
            
            time.sleep(min(wait_time, 1.0))
    
    def release(self, tokens_used: int) -> None:
        """Release resources after request completes."""
        with self.lock:
            self.state.requests_in_flight -= 1
            self.state.tokens = min(
                self.max_tokens,
                self.state.tokens + tokens_used
            )
        
        for callback in self.callbacks:
            callback(tokens_used, self.state.tokens)
    
    def get_status(self) -> dict:
        """Get current rate limiter status."""
        with self.lock:
            self._refill()
            return {
                'tokens': int(self.state.tokens),
                'in_flight': self.state.requests_in_flight,
            }
    
    def on_release(self, callback) -> None:
        """Register a callback for release events."""
        self.callbacks.append(callback)
```

### Comprehensive API Service Class

```typescript
// services/openaiService.ts - Complete OpenAI service
import OpenAI from 'openai';
import { rateLimiter } from './rateLimiter';
import { withRetry } from '../utils/retry';
import { countMessagesTokens, estimateCost } from '../utils/tokenCounter';
import {
  OpenAIAPIError,
  RateLimitError,
  AuthenticationError,
  ContextLengthExceededError,
} from '../errors/openaiError';

interface CompletionOptions {
  model?: string;
  temperature?: number;
  maxTokens?: number;
  topP?: number;
  stop?: string[];
  stream?: boolean;
}

interface CompletionResponse {
  content: string;
  usage: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  cost: number;
  model: string;
  finishReason: string;
  id: string;
}

export class OpenAIService {
  private client: OpenAI;
  private defaultModel: string;
  
  constructor(apiKey?: string, defaultModel: string = 'gpt-4o') {
    this.client = new OpenAI({ apiKey: apiKey || process.env.OPENAI_API_KEY });
    this.defaultModel = defaultModel;
  }
  
  async chatCompletion(
    messages: Array<{
      role: 'system' | 'user' | 'assistant';
      content: string;
    }>,
    options: CompletionOptions = {}
  ): Promise<CompletionResponse> {
    const model = options.model || this.defaultModel;
    const estimatedTokens = countMessagesTokens(messages, model).promptTokens;
    
    await rateLimiter.acquire(estimatedTokens);
    
    try {
      const response = await withRetry(
        () => this.client.chat.completions.create({
          model,
          messages,
          temperature: options.temperature,
          max_tokens: options.maxTokens,
          top_p: options.topP,
          stop: options.stop,
          stream: false,
        }),
        { maxRetries: 3 }
      );
      
      const usage = response.usage;
      const content = response.choices[0]?.message?.content || '';
      const cost = estimateCost(
        { ...usage, totalTokens: usage?.total_tokens || 0 },
        model
      );
      
      rateLimiter.release(estimatedTokens);
      
      return {
        content,
        usage: {
          promptTokens: usage?.prompt_tokens || 0,
          completionTokens: usage?.completion_tokens || 0,
          totalTokens: usage?.total_tokens || 0,
        },
        cost,
        model,
        finishReason: response.choices[0]?.finish_reason || 'stop',
        id: response.id,
      };
    } catch (error: any) {
      rateLimiter.release(estimatedTokens);
      this.handleError(error);
      throw error;
    }
  }
  
  async chatCompletionStream(
    messages: Array<{
      role: 'system' | 'user' | 'assistant';
      content: string;
    }>,
    options: CompletionOptions = {}
  ): Promise<AsyncIterable<string>> {
    const model = options.model || this.defaultModel;
    
    const stream = await withRetry(
      () => this.client.chat.completions.create({
        model,
        messages,
        temperature: options.temperature,
        max_tokens: options.maxTokens,
        top_p: options.topP,
        stream: true,
      })
    );
    
    return stream;
  }
  
  async createEmbedding(
    text: string,
    model: string = 'text-embedding-3-large'
  ): Promise<number[]> {
    await rateLimiter.acquire(1000); // Approximate tokens
    
    try {
      const response = await withRetry(
        () => this.client.embeddings.create({
          model,
          input: text,
        })
      );
      
      rateLimiter.release(1000);
      return response.data[0].embedding;
    } catch (error) {
      rateLimiter.release(1000);
      this.handleError(error);
      throw error;
    }
  }
  
  private handleError(error: any): never {
    if (error.status === 401) {
      throw new AuthenticationError(error.message);
    }
    if (error.status === 429) {
      const retryAfter = parseInt(error.headers?.['retry-after'] || '1', 10);
      throw new RateLimitError(
        error.message,
        retryAfter,
        parseInt(error.headers?.['x-ratelimit-limit'] || '0', 10),
        parseInt(error.headers?.['x-ratelimit-remaining'] || '0', 10),
        new Date(parseInt(error.headers?.['x-ratelimit-reset'] || '0', 10) * 1000)
      );
    }
    if (error.code === 'context_length_exceeded') {
      throw new ContextLengthExceededError(
        error.message,
        parseInt(error.param || '0', 10),
        parseInt(error.message.match(/\d+/)?.[0] || '0', 10)
      );
    }
    throw new OpenAIAPIError(
      error.message,
      error.status || 500,
      error.code || 'unknown_error',
      error.param,
      error.type || 'server_error'
    );
  }
}

// Factory function for dependency injection
export function createOpenAIService(): OpenAIService {
  return new OpenAIService();
}
```

## Common Patterns và Use Cases

### Batch Processing Pattern

```typescript
// services/batchProcessor.ts - Batch processing with progress tracking
import { OpenAIService } from './openaiService';

interface BatchItem<T> {
  id: string;
  data: T;
  result?: string;
  error?: string;
  tokens?: number;
}

interface BatchProgress {
  total: number;
  completed: number;
  failed: number;
  totalTokens: number;
  estimatedCost: number;
}

export class BatchProcessor<T> {
  private service: OpenAIService;
  private concurrency: number;
  private results: BatchItem<T>[] = [];
  
  constructor(
    openaiService: OpenAIService,
    concurrency: number = 5
  ) {
    this.service = openaiService;
    this.concurrency = concurrency;
  }
  
  async process(
    items: T[],
    processor: (item: T) => Promise<string>,
    onProgress?: (progress: BatchProgress) => void
  ): Promise<BatchItem<T>[]> {
    this.results = items.map((data, index) => ({
      id: `batch-${index}`,
      data,
    }));
    
    const chunks = this.chunkArray(this.results, this.concurrency);
    
    for (const chunk of chunks) {
      const promises = chunk.map(async (item) => {
        try {
          const result = await processor(item.data);
          item.result = result;
        } catch (error: any) {
          item.error = error.message;
        }
        item.tokens = this.estimateTokens(item);
        
        if (onProgress) {
          onProgress(this.getProgress());
        }
      });
      
      await Promise.all(promises);
    }
    
    return this.results;
  }
  
  private chunkArray<T>(array: T[], size: number): T[][] {
    const chunks: T[][] = [];
    for (let i = 0; i < array.length; i += size) {
      chunks.push(array.slice(i, i + size));
    }
    return chunks;
  }
  
  private getProgress(): BatchProgress {
    const completed = this.results.filter(r => r.result !== undefined).length;
    const failed = this.results.filter(r => r.error !== undefined).length;
    const totalTokens = this.results.reduce((sum, r) => sum + (r.tokens || 0), 0);
    
    return {
      total: this.results.length,
      completed,
      failed,
      totalTokens,
      estimatedCost: totalTokens * 0.00001, // Rough estimate
    };
  }
  
  private estimateTokens(item: BatchItem<T>): number {
    return JSON.stringify(item.data).length / 4; // Rough estimate
  }
}

// Usage example
async function processDocuments() {
  const service = createOpenAIService();
  const processor = new BatchProcessor(service, 3);
  
  const documents = await loadDocuments();
  
  const results = await processor.process(
    documents,
    async (doc) => {
      const response = await service.chatCompletion([
        { role: 'user', content: `Summarize: ${doc.content}` }
      ]);
      return response.content;
    },
    (progress) => {
      console.log(`Progress: ${progress.completed}/${progress.total} completed`);
    }
  );
  
  return results;
}
```

### Fallback Model Pattern

```typescript
// services/fallbackService.ts - Fallback model handling
import { OpenAIService } from './openaiService';
import { RateLimitError, ContextLengthExceededError } from '../errors/openaiError';

interface ModelConfig {
  primary: string;
  fallback?: string;
  emergency?: string;
}

export class FallbackService {
  private service: OpenAIService;
  private modelConfig: ModelConfig;
  
  constructor(
    service: OpenAIService,
    modelConfig: ModelConfig = {
      primary: 'gpt-4o',
      fallback: 'gpt-4o-mini',
      emergency: 'gpt-3.5-turbo',
    }
  ) {
    this.service = service;
    this.modelConfig = modelConfig;
  }
  
  async chatWithFallback(
    messages: Array<{ role: string; content: string }>,
    options: any = {}
  ): Promise<any> {
    const models = [
      this.modelConfig.primary,
      this.modelConfig.fallback,
      this.modelConfig.emergency,
    ].filter(Boolean);
    
    let lastError: Error | null = null;
    
    for (const model of models) {
      try {
        const response = await this.service.chatCompletion(messages, {
          ...options,
          model,
        });
        
        return {
          ...response,
          modelUsed: model,
          fallbackAttempted: model !== this.modelConfig.primary,
        };
      } catch (error: any) {
        lastError = error;
        
        // Don't fallback for certain errors
        if (error instanceof AuthenticationError) {
          throw error;
        }
        
        // Context length errors need different handling
        if (error instanceof ContextLengthExceededError) {
          // Try to truncate and retry
          messages = this.truncateMessages(messages);
          continue;
        }
        
        // Rate limit errors should trigger fallback
        if (error instanceof RateLimitError) {
          await new Promise(resolve => setTimeout(resolve, error.retryAfter * 1000));
          continue;
        }
        
        // Other errors also trigger fallback
        continue;
      }
    }
    
    throw lastError || new Error('All models failed');
  }
  
  private truncateMessages(
    messages: Array<{ role: string; content: string }>
  ): Array<{ role: string; content: string }> {
    // Keep system message and last user message
    const systemMessage = messages.find(m => m.role === 'system');
    const userMessages = messages.filter(m => m.role === 'user');
    const lastUserMessage = userMessages[userMessages.length - 1];
    
    const truncatedContent = lastUserMessage.content.substring(0, 8000);
    
    return [
      ...(systemMessage ? [systemMessage] : []),
      { ...lastUserMessage, content: truncatedContent },
    ];
  }
}
```

## Troubleshooting Common Issues

### Diagnostic Utilities

```typescript
// utils/diagnostics.ts - Diagnostic utilities for troubleshooting
import { OpenAI } from 'openai';

interface DiagnosticResult {
  apiKeyValid: boolean;
  organizationValid: boolean;
  rateLimitStatus: {
    limit: number;
    remaining: number;
    resetAt: Date;
  };
  accountStatus: {
    hasActiveSubscription: boolean;
    totalUsage: number;
    hardLimit: number | null;
  };
  recommendedModels: string[];
}

export async function runDiagnostics(apiKey: string): Promise<DiagnosticResult> {
  const client = new OpenAI({ apiKey });
  
  const result: DiagnosticResult = {
    apiKeyValid: false,
    organizationValid: false,
    rateLimitStatus: { limit: 0, remaining: 0, resetAt: new Date() },
    accountStatus: { hasActiveSubscription: false, totalUsage: 0, hardLimit: null },
    recommendedModels: [],
  };
  
  try {
    // Test API key with a minimal request
    const testResponse = await client.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [{ role: 'user', content: 'test' }],
      max_tokens: 5,
    });
    
    result.apiKeyValid = true;
    
    // Check rate limit headers
    result.rateLimitStatus = {
      limit: parseInt(testResponse.headers?.['x-ratelimit-limit'] || '0', 10),
      remaining: parseInt(testResponse.headers?.['x-ratelimit-remaining'] || '0', 10),
      resetAt: new Date(
        parseInt(testResponse.headers?.['x-ratelimit-reset'] || '0', 10) * 1000
      ),
    };
    
    result.recommendedModels = ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo'];
    
  } catch (error: any) {
    if (error.status === 401) {
      result.apiKeyValid = false;
    }
  }
  
  return result;
}

export function formatDiagnosticReport(result: DiagnosticResult): string {
  return `
=== OpenAI API Diagnostic Report ===
Generated: ${new Date().toISOString()}

API Key Status: ${result.apiKeyValid ? '✓ Valid' : '✗ Invalid'}
Organization: ${result.organizationValid ? '✓ Valid' : '✗ Not Set'}

Rate Limits:
  Limit: ${result.rateLimitStatus.limit} requests
  Remaining: ${result.rateLimitStatus.remaining} requests
  Resets: ${result.rateLimitStatus.resetAt.toISOString()}

Account Status:
  Subscription: ${result.accountStatus.hasActiveSubscription ? 'Active' : 'Inactive'}
  Total Usage: $${result.accountStatus.totalUsage.toFixed(2)}
  Hard Limit: ${result.accountStatus.hardLimit ? `$${result.accountStatus.hardLimit}` : 'None'}

Recommended Models:
${result.recommendedModels.map(m => `  - ${m}`).join('\n')}
`;
}
```

### Common Error Solutions

```typescript
// troubleshooting/solutions.ts - Common issue solutions

interface TroubleshootingGuide {
  issue: string;
  symptoms: string[];
  causes: string[];
  solutions: string[];
  prevention: string[];
}

export const troubleshootingGuides: TroubleshootingGuide[] = [
  {
    issue: 'Rate Limit Exceeded (429)',
    symptoms: [
      'Requests fail with 429 status code',
      'Error message: "Rate limit reached"',
      'Intermittent failures under high load',
    ],
    causes: [
      'Too many requests per minute',
      'Too many tokens per minute',
      'Burst of requests exceeding limits',
      'Multiple concurrent applications using same key',
    ],
    solutions: [
      'Implement exponential backoff with jitter',
      'Add request queuing with rate limiter',
      'Distribute load across multiple API keys',
      'Use batch processing for high-volume operations',
      'Implement caching to reduce redundant requests',
    ],
    prevention: [
      'Monitor rate limit headers in responses',
      'Implement proactive throttling before limits hit',
      'Use token bucket algorithm for smooth request distribution',
      'Set up alerts for rate limit usage > 80%',
    ],
  },
  {
    issue: 'Invalid API Key (401)',
    symptoms: [
      'Authentication failures on all requests',
      'Error message: "Invalid API key"',
      'Sudden authentication failures after working normally',
    ],
    causes: [
      'Incorrect or mistyped API key',
      'API key deleted or revoked',
      'Using wrong key for organization',
      'Environment variable not loaded correctly',
    ],
    solutions: [
      'Verify API key in OpenAI dashboard',
      'Check environment variable configuration',
      'Regenerate API key if compromised',
      'Verify key matches expected format (sk-...)',
    ],
    prevention: [
      'Store API keys in secure secrets manager',
      'Use environment-specific key configurations',
      'Implement key validation on startup',
      'Regular audit of active API keys',
    ],
  },
  {
    issue: 'Context Length Exceeded (400)',
    symptoms: [
      'Errors when processing long documents',
      'Failure on conversations with many messages',
      'Model-specific limitations hit unexpectedly',
    ],
    causes: [
      'Input exceeds model context window',
      'Accumulated conversation history too long',
      'System prompt too verbose',
      'Using smaller context model than needed',
    ],
    solutions: [
      'Implement message summarization for long conversations',
      'Truncate oldest messages when context exceeds limit',
      'Use models with larger context windows (128k)',
      'Optimize system prompts for efficiency',
      'Split large documents into chunks',
    ],
    prevention: [
      'Track token usage in all requests',
      'Implement pre-flight token counting',
      'Set up automated truncation for edge cases',
      'Choose appropriate model based on input size',
    ],
  },
  {
    issue: 'Timeout Errors',
    symptoms: [
      'Requests hang and never complete',
      'Timeout errors after 60+ seconds',
      'Inconsistent response times',
    ],
    causes: [
      'Request payload too large',
      'Network latency or connectivity issues',
      'Server-side processing taking too long',
      'Proxy or firewall interference',
    ],
    solutions: [
      'Increase client timeout configuration',
      'Reduce input size to speed up processing',
      'Implement proper timeout handling with retries',
      'Check network routes and proxy settings',
    ],
    prevention: [
      'Set reasonable timeout values (60-120s)',
      'Monitor request duration metrics',
      'Implement circuit breaker pattern',
      'Use async processing for long operations',
    ],
  },
];
```

## Code Examples hoàn chỉnh

### TypeScript Complete Example

```typescript
// example/completeOpenAIExample.ts - Full production-ready example
import OpenAI from 'openai';
import { EventEmitter } from 'events';
import { TokenBucketRateLimiter } from '../services/rateLimiter';
import { withRetry } from '../utils/retry';
import {
  countMessagesTokens,
  estimateCost,
  truncateToContextLimit,
} from '../utils/tokenCounter';
import {
  OpenAIAPIError,
  RateLimitError,
  AuthenticationError,
  ContextLengthExceededError,
} from '../errors/openaiError';

// Configuration
const config = {
  apiKey: process.env.OPENAI_API_KEY!,
  organizationId: process.env.OPENAI_ORG_ID,
  defaultModel: 'gpt-4o',
  maxTokensPerMinute: 150000,
  requestsPerMinute: 500,
  maxConcurrent: 10,
  maxRetries: 3,
  timeout: 60000,
};

// Events for observability
const events = new EventEmitter();

// Metrics tracking
interface Metrics {
  totalRequests: number;
  successfulRequests: number;
  failedRequests: number;
  totalTokens: number;
  totalCost: number;
  averageLatency: number;
}

const metrics: Metrics = {
  totalRequests: 0,
  successfulRequests: 0,
  failedRequests: 0,
  totalTokens: 0,
  totalCost: 0,
  averageLatency: 0,
};

// Initialize rate limiter
const rateLimiter = new TokenBucketRateLimiter(
  config.maxTokensPerMinute,
  config.requestsPerMinute,
  config.maxConcurrent
);

// Initialize OpenAI client
const client = new OpenAI({
  apiKey: config.apiKey,
  organization: config.organizationId,
  timeout: config.timeout,
  maxRetries: config.maxRetries,
});

interface ChatRequest {
  messages: Array<{ role: string; content: string }>;
  model?: string;
  temperature?: number;
  maxTokens?: number;
  userId?: string;
  requestId?: string;
}

interface ChatResponse {
  content: string;
  usage: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  cost: number;
  model: string;
  finishReason: string;
  requestId: string;
  latencyMs: number;
}

async function chat(request: ChatRequest): Promise<ChatResponse> {
  const requestId = request.requestId || `req-${Date.now()}`;
  const model = request.model || config.defaultModel;
  const startTime = Date.now();
  
  metrics.totalRequests++;
  events.emit('request:start', { requestId, model });
  
  try {
    // Estimate tokens and acquire rate limit
    const tokenCount = countMessagesTokens(request.messages, model);
    await rateLimiter.acquire(tokenCount.totalTokens);
    
    // Execute with retry
    const response = await withRetry(
      () => client.chat.completions.create({
        model,
        messages: request.messages,
        temperature: request.temperature,
        max_tokens: request.maxTokens,
        user: request.userId,
      }),
      { maxRetries: config.maxRetries },
      (attempt, error, delay) => {
        events.emit('request:retry', { requestId, attempt, error, delay });
      }
    );
    
    // Calculate cost and metrics
    const usage = response.usage!;
    const cost = estimateCost(
      {
        promptTokens: usage.prompt_tokens,
        completionTokens: usage.completion_tokens,
        totalTokens: usage.total_tokens,
      },
      model
    );
    
    const latencyMs = Date.now() - startTime;
    
    // Update metrics
    metrics.successfulRequests++;
    metrics.totalTokens += usage.total_tokens;
    metrics.totalCost += cost;
    metrics.averageLatency = 
      (metrics.averageLatency * (metrics.successfulRequests - 1) + latencyMs) /
      metrics.successfulRequests;
    
    // Release rate limit
    rateLimiter.release(tokenCount.totalTokens);
    
    const result: ChatResponse = {
      content: response.choices[0].message.content || '',
      usage: {
        promptTokens: usage.prompt_tokens,
        completionTokens: usage.completion_tokens,
        totalTokens: usage.total_tokens,
      },
      cost,
      model,
      finishReason: response.choices[0].finish_reason || 'stop',
      requestId,
      latencyMs,
    };
    
    events.emit('request:success', result);
    return result;
    
  } catch (error: any) {
    metrics.failedRequests++;
    events.emit('request:error', { requestId, error });
    
    // Handle specific errors
    if (error instanceof AuthenticationError) {
      throw new Error('OpenAI API authentication failed. Please check your API key.');
    }
    
    if (error instanceof RateLimitError) {
      throw new Error(`Rate limit exceeded. Retry after ${error.retryAfter} seconds.`);
    }
    
    if (error instanceof ContextLengthExceededError) {
      // Attempt automatic truncation and retry
      const truncatedMessages = request.messages.map(msg => ({
        ...msg,
        content: truncateToContextLimit(msg.content, model),
      }));
      
      return chat({ ...request, messages: truncatedMessages });
    }
    
    throw error;
  }
}

// Streaming support
async function* chatStream(
  request: ChatRequest
): AsyncGenerator<string, void, unknown> {
  const model = request.model || config.defaultModel;
  
  const stream = await withRetry(
    () => client.chat.completions.create({
      model,
      messages: request.messages,
      temperature: request.temperature,
      max_tokens: request.maxTokens,
      stream: true,
    })
  );
  
  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content;
    if (content) {
      yield content;
    }
  }
}

// Event listeners for monitoring
events.on('request:start', (data) => {
  console.log(`[${data.requestId}] Starting request to ${data.model}`);
});

events.on('request:retry', (data) => {
  console.log(`[${data.requestId}] Retrying attempt ${data.attempt} after ${data.delay}ms`);
});

events.on('request:success', (data) => {
  console.log(
    `[${data.requestId}] Success: ${data.cost.toFixed(4)} USD, ` +
    `${data.latencyMs}ms, ${data.usage.totalTokens} tokens`
  );
});

events.on('request:error', (data) => {
  console.error(`[${data.requestId}] Error: ${data.error.message}`);
});

// Usage example
async function main() {
  try {
    const response = await chat({
      messages: [
        { role: 'system', content: 'You are a helpful assistant.' },
        { role: 'user', content: 'Explain quantum computing in simple terms.' },
      ],
      temperature: 0.7,
      maxTokens: 500,
    });
    
    console.log('Response:', response.content);
    console.log('Metrics:', metrics);
    
  } catch (error) {
    console.error('Chat failed:', error);
  }
}
```

## References và Resources

### Official Documentation

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [API Rate Limits](https://platform.openai.com/account/rate-limits)
- [Token Usage Calculator](https://platform.openai.com/tokenizer)
- [Pricing Page](https://openai.com/pricing)
- [Status Page](https://status.openai.com)

### SDK Documentation

- [OpenAI Node.js SDK](https://github.com/openai/openai-node)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [SDK Changelog](https://github.com/openai/openai-node/blob/main/CHANGELOG.md)

### Best Practices Guides

- [Production Best Practices](https://help.openai.com/en/articles/8474698-using-the-openai-api-in-production)
- [Safety Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [Rate Limit Management](https://platform.openai.com/docs/guides/rate-limits)

### Community Resources

- [OpenAI Community Forum](https://community.openai.com)
- [API Examples Repository](https://github.com/openai/openai-cookbook)
- [API Guides and Tutorials](https://platform.openai.com/docs/guides)

---

**Tài liệu này là một phần của Cursor Enterprise Framework Generator. Để cập nhật mới nhất, vui lòng truy cập repository hoặc liên hệ team development.**
