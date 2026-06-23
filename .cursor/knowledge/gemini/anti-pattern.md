---
title: "Gemini Anti-Patterns - Các Mẫu Cần Tránh"
description: "Comprehensive guide on common anti-patterns when working with Google Gemini API, including safety filtering, multimodal misuse, rate limiting, and token counting issues"
tags: ["gemini", "google-ai", "anti-patterns", "best-practices", "llm", "vertex-ai"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Gemini Anti-Patterns - Các Mẫu Cần Tránh

## Tổng Quan (Overview)

Google Gemini API là một công cụ mạnh mẽ cho việc xây dựng các ứng dụng AI đa phương thức (multimodal). Tuy nhiên, nhiều developers mắc phải những anti-patterns phổ biến dẫn đến hiệu suất kém, chi phí cao, và trải nghiệm người dùng không tốt. Tài liệu này tổng hợp các anti-patterns phổ biến nhất và cách tránh chúng.

Trong quá trình tích hợp Gemini vào Cursor Enterprise Framework, chúng tôi đã quan sát được nhiều patterns không hiệu quả từ các dự án thực tế. Những anti-patterns này không chỉ ảnh hưởng đến hiệu suất mà còn có thể gây ra các vấn đề về bảo mật, chi phí, và khả năng mở rộng.

Việc hiểu rõ các anti-patterns này là bước đầu tiên để xây dựng một hệ thống Gemini production-ready. Mỗi anti-pattern được phân tích theo cấu trúc: Mô tả vấn đề, Tại sao nó xảy ra, Hậu quả tiềm tàng, và Cách khắc phục.

## Mục Đích (Purpose)

Tài liệu này phục vụ các mục đích chính sau:

1. **Giáo dục đội ngũ phát triển** về các practices không nên làm khi làm việc với Gemini API
2. **Cung cấp giải pháp thay thế** đã được kiểm chứng cho từng anti-pattern
3. **Hỗ trợ code review** bằng cách cung cấp checklist các vấn đề cần tìm
4. **Tối ưu hóa chi phí** bằng cách tránh các patterns gây lãng phí

## Khái Niệm Chính (Key Concepts)

### 1. Safety Filtering và Blocked Content

Google Gemini có built-in safety filtering system để ngăn chặn nội dung có hại. Tuy nhiên, nhiều developers không hiểu cách hệ thống này hoạt động và không xử lý các trường hợp bị block một cách graceful. Safety settings có nhiều mức độ từ BLOCK_NONE đến BLOCK_ONLY_HIGH, và việc chọn sai mức có thể dẫn đến trải nghiệm người dùng kém hoặc bỏ sót nội dung cần thiết.

Safety categories bao gồm: HARM_CATEGORY_HATE_SPEECH, HARM_CATEGORY_DANGEROUS_CONTENT, HARM_CATEGORY_SEXUAL_EXPLICIT, và HARM_CATEGORY_HARASSMENT. Mỗi category có 4 mức threshold: BLOCK_NONE, BLOCK_ONLY_HIGH, BLOCK_MEDIUM_AND_ABOVE, và BLOCK_LOW_AND_ABOVE.

### 2. Rate Limiting và Quota Management

Gemini API có rate limits và quotas khác nhau tùy thuộc vào tier (Free tier vs Pay-as-you-go vs Enterprise). Việc không hiểu và quản lý these limits dẫn đến 429 errors và service disruptions. Rate limits được tính theo requests per minute (RPM), tokens per minute (TPM), và requests per day (RPD).

### 3. Token Counting và Context Management

Việc không đếm token chính xác có thể dẫn đến context overflow errors hoặc chi phí cao hơn cần thiết. Gemini models có context windows khác nhau: Gemini Nano có 32K tokens, Gemini Pro có 128K tokens, và Gemini Ultra có 1M tokens trong phiên bản experimental.

### 4. Multimodal Input Handling

Gemini's strength là multimodal capabilities, nhưng nhiều developers không tận dụng đúng cách hoặc sử dụng không hiệu quả. Điều này bao gồm việc gửi images với resolution quá cao, sử dụng sai format cho audio/video, và không tối ưu hóa input data.

## Anti-Patterns Chi Tiết

### Anti-Pattern #1: Ignoring Safety Blocks

#### Mô Tả Vấn Đề

Đây là một trong những anti-pattern phổ biến và nguy hiểm nhất. Developers thường giả định rằng safety blocks sẽ không xảy ra hoặc không implement proper error handling cho các trường hợp này. Khi user input trigger safety filter, application crash hoặc trả về unhandled exception.

#### Tại Sao Nó Xảy Ra

Nhiều developers test với benign inputs và không test với edge cases có thể trigger safety filters. Thêm vào đó, document của Google về safety settings có thể khó hiểu và developers không realize rằng default settings có thể block legitimate content.

#### Hậu Quả Tiềm Tàng

User experience kém khi application crash hoặc hiển thị generic error message. Brand reputation risk nếu application expose internal errors hoặc behave unexpectedly. Security risk nếu developers disable safety settings hoàn toàn để "fix" vấn đề. Potential legal liability nếu harmful content được generated mà không có guardrails.

#### Cách Khắc Phục

```typescript
// ❌ ANTI-PATTERN: Không handle safety blocks
async function generateContent(prompt: string): Promise<string> {
  const result = await model.generateContent(prompt);
  return result.response.text(); // Có thể throw nếu blocked
}

// ✅ BEST PRACTICE: Handle safety blocks gracefully
interface SafetyBlockResult {
  blocked: boolean;
  categories?: HarmCategory[];
  feedbackMessage?: string;
}

async function generateContentSafe(
  prompt: string
): Promise<{ text: string; safety: SafetyBlockResult }> {
  try {
    const result = await model.generateContent(prompt);
    const candidate = result.response.candidates?.[0];
    
    if (!candidate) {
      return {
        text: '',
        safety: { 
          blocked: true, 
          feedbackMessage: result.response.promptFeedback?.blockReason 
        }
      };
    }
    
    return {
      text: candidate.content.parts[0].text || '',
      safety: { blocked: false }
    };
  } catch (error) {
    if (error instanceof SafetyBlockError) {
      return {
        text: '',
        safety: {
          blocked: true,
          categories: error.blockedCategories,
          feedbackMessage: 'Content blocked due to safety concerns. Please modify your input.'
        }
      };
    }
    throw error;
  }
}
```

```python
# Python implementation
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class SafetyResult:
    blocked: bool
    categories: Optional[List[str]] = None
    message: Optional[str] = None

async def generate_content_safe(prompt: str) -> tuple[str, SafetyResult]:
    try:
        response = await model.generate_content_async(prompt)
        candidate = response.candidates[0] if response.candidates else None
        
        if not candidate:
            return "", SafetyResult(
                blocked=True,
                message=f"Blocked: {response.prompt_feedback.block_reason}"
            )
        
        return candidate.content.parts[0].text, SafetyResult(blocked=False)
    
    except Exception as e:
        if "SAFETY" in str(e).upper():
            return "", SafetyResult(
                blocked=True,
                categories=extract_blocked_categories(e),
                message="Content filtered for safety. Please revise your request."
            )
        raise
```

#### Testing Strategy

Implement comprehensive safety testing:

```typescript
const dangerousPrompts = [
  "Instructions for making weapons",
  "Self-harm instructions",
  "Promoting hate speech",
  "Explicit content generation",
];

for (const prompt of dangerousPrompts) {
  const result = await generateContentSafe(prompt);
  expect(result.safety.blocked).toBe(true);
}
```

### Anti-Pattern #2: No Token Budget or Limit

#### Mô Tả Vấn Đề

Developers không set maxOutputTokens hoặc đặt giá trị quá cao, dẫn đến:
- Unexpectedly high API costs
- Very long response times
- Application logic assumptions broken by variable-length responses

#### Tại Sao Nó Xảy Ra

Developers muốn "get complete answers" và không realize rằng unlimited outputs có cost implications. Default settings có thể allow outputs lên đến 8192 tokens cho some models.

#### Hậu Quả Tiềm Tàng

Cost overruns có thể significant. User phải chờ lâu cho responses. UI layouts break khi content quá dài. Potential for abuse nếu application allow user-provided prompts.

#### Cách Khắc Phục

```typescript
interface GenerationConfig {
  maxOutputTokens: number;
  expectedResponseLength?: 'short' | 'medium' | 'long';
}

// Context-aware token limits
const TOKEN_LIMITS = {
  short: 256,    // Quick answers, confirmations
  medium: 1024,  // Standard responses
  long: 2048,    // Detailed explanations
  code: 4096,    // Code generation
} as const;

async function generateWithBudget(
  prompt: string,
  responseType: keyof typeof TOKEN_LIMITS = 'medium'
): Promise<string> {
  const result = await model.generateContent({
    prompt,
    generationConfig: {
      maxOutputTokens: TOKEN_LIMITS[responseType],
      // Thêm stop sequences để truncate nếu cần
      stopSequences: ['\n\n---', 'END OF RESPONSE'],
    }
  });
  
  return result.response.text();
}
```

```python
# Python với token budget
from enum import Enum
from dataclasses import dataclass

class ResponseType(Enum):
    SHORT = 256
    MEDIUM = 1024
    LONG = 2048
    CODE = 4096

@dataclass
class GenerationConfig:
    max_output_tokens: int
    temperature: float = 0.7
    top_p: float = 0.95
    stop_sequences: list[str] = None

async def generate_with_budget(
    prompt: str,
    response_type: ResponseType = ResponseType.MEDIUM
) -> str:
    config = GenerationConfig(
        max_output_tokens=response_type.value,
        stop_sequences=["\n\n---", "TERMINATE"]
    )
    
    response = await model.generate_content_async(
        prompt,
        generation_config=config
    )
    
    return response.text
```

### Anti-Pattern #3: Wrong Model Selection

#### Mô Tả Vấn Đề

Using Gemini Ultra cho simple tasks (wasting cost) hoặc using Gemini Flash cho complex reasoning (poor results). Model selection không aligned với task requirements.

#### Model Comparison

| Model | Use Case | Cost | Speed | Capabilities |
|-------|----------|------|-------|-------------|
| Gemini Ultra | Complex reasoning, research | Highest | Slowest | Best quality |
| Gemini Pro | General purpose | Medium | Medium | Balanced |
| Gemini Flash | High volume, simple tasks | Lowest | Fastest | Good for simple tasks |
| Gemini Nano | On-device, mobile | Free | Instant | Limited |

#### Cách Khắc Phục

```typescript
type TaskComplexity = 'simple' | 'moderate' | 'complex' | 'research';

const MODEL_SELECTION = {
  // Simple: Classification, sentiment, extraction
  simple: 'gemini-1.5-flash',
  
  // Moderate: Summarization, translation, Q&A
  moderate: 'gemini-1.5-flash',
  
  // Complex: Analysis, multi-step reasoning
  complex: 'gemini-1.5-pro',
  
  // Research: Deep analysis, long documents
  research: 'gemini-1.5-pro-002',
} as const;

function selectModel(task: TaskComplexity): string {
  return MODEL_SELECTION[task];
}

// Cost-aware model selection
interface ModelCost {
  inputCostPer1K: number;
  outputCostPer1K: number;
  contextCacheCostPer1K: number;
}

const MODEL_COSTS: Record<string, ModelCost> = {
  'gemini-1.5-pro': {
    inputCostPer1K: 0.00125,  // $0.125/1M tokens
    outputCostPer1K: 0.005,
    contextCacheCostPer1K: 0.000088,
  },
  'gemini-1.5-flash': {
    inputCostPer1K: 0.000035,  // $0.035/1M tokens
    outputCostPer1K: 0.00014,
    contextCacheCostPer1K: 0.0000175,
  },
};

function estimateCost(
  model: string,
  inputTokens: number,
  outputTokens: number,
  useCache: boolean = false
): number {
  const costs = MODEL_COSTS[model];
  if (!costs) return 0;
  
  const inputCost = (inputTokens / 1000) * costs.inputCostPer1K;
  const outputCost = (outputTokens / 1000) * costs.outputCostPer1K;
  const cacheCost = useCache 
    ? (inputTokens / 1000) * costs.contextCacheCostPer1K 
    : 0;
  
  return inputCost + outputCost - cacheCost;
}
```

### Anti-Pattern #4: Not Handling Rate Limits

#### Mô Tả Vấn Đề

Application gửi too many requests và nhận 429 Too Many Requests errors mà không có retry logic hoặc exponential backoff. Hoặc không monitor usage và exceed quotas.

#### Rate Limits Overview

| Tier | RPM | TPM | RPD | Concurrent |
|------|-----|-----|-----|-------------|
| Free | 15 | 1M | 1500 | 3 |
| Pay-as-you-go | 60 | 1M | - | 10 |
| Vertex AI | Configurable | Configurable | - | Configurable |

#### Cách Khắc Phục

```typescript
interface RateLimitConfig {
  maxRetries: number;
  baseDelayMs: number;
  maxDelayMs: number;
  jitterFactor: number;
}

const DEFAULT_RATE_LIMIT_CONFIG: RateLimitConfig = {
  maxRetries: 5,
  baseDelayMs: 1000,
  maxDelayMs: 60000,
  jitterFactor: 0.2,
};

class RateLimitedClient {
  private requestQueue: Promise<unknown>[] = [];
  private tokens: number;
  private lastRefill: number;
  
  constructor(
    private readonly model: GenerativeModel,
    private readonly config: RateLimitConfig = DEFAULT_RATE_LIMIT_CONFIG,
    private readonly rpm: number = 60
  ) {
    this.tokens = rpm;
    this.lastRefill = Date.now();
  }
  
  private async acquireToken(): Promise<void> {
    while (this.tokens <= 0) {
      const waitTime = this.calculateRefillTime();
      if (waitTime > 0) {
        await this.delay(waitTime);
      }
      this.refillTokens();
    }
    this.tokens--;
  }
  
  private refillTokens(): void {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    const refillAmount = Math.floor(elapsed * (this.rpm / 60));
    
    if (refillAmount > 0) {
      this.tokens = Math.min(this.rpm, this.tokens + refillAmount);
      this.lastRefill = now;
    }
  }
  
  private calculateRefillTime(): number {
    if (this.tokens > 0) return 0;
    const secondsUntilRefill = Math.ceil((1 - this.tokens) / (this.rpm / 60));
    return secondsUntilRefill * 1000;
  }
  
  async withRetry<T>(
    operation: () => Promise<T>,
    context: string = ''
  ): Promise<T> {
    let lastError: Error | null = null;
    
    for (let attempt = 0; attempt <= this.config.maxRetries; attempt++) {
      try {
        await this.acquireToken();
        return await operation();
      } catch (error) {
        lastError = error as Error;
        
        if (this.isRateLimitError(error)) {
          const delay = this.calculateBackoffDelay(attempt);
          console.warn(`Rate limit hit (attempt ${attempt + 1}/${this.config.maxRetries + 1}). Retrying in ${delay}ms. ${context}`);
          await this.delay(delay);
          continue;
        }
        
        if (!this.isRetryableError(error)) {
          throw error;
        }
      }
    }
    
    throw lastError;
  }
  
  private calculateBackoffDelay(attempt: number): number {
    const exponentialDelay = this.config.baseDelayMs * Math.pow(2, attempt);
    const jitter = exponentialDelay * this.config.jitterFactor * Math.random();
    return Math.min(exponentialDelay + jitter, this.config.maxDelayMs);
  }
  
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  private isRateLimitError(error: Error): boolean {
    return error.message.includes('429') || 
           error.message.includes('RESOURCE_EXHAUSTED') ||
           error.message.includes('quota');
  }
  
  private isRetryableError(error: Error): boolean {
    return this.isRateLimitError(error) ||
           error.message.includes('500') ||
           error.message.includes('503') ||
           error.message.includes('timeout');
  }
}
```

```python
# Python implementation
import asyncio
import random
import time
from dataclasses import dataclass
from typing import Callable, TypeVar, Any

@dataclass
class RateLimitConfig:
    max_retries: int = 5
    base_delay: float = 1.0
    max_delay: float = 60.0
    jitter_factor: float = 0.2

T = TypeVar('T')

class RateLimitedClient:
    def __init__(
        self,
        model: Any,
        config: RateLimitConfig = None,
        rpm: int = 60
    ):
        self.model = model
        self.config = config or RateLimitConfig()
        self.rpm = rpm
        self.tokens = rpm
        self.last_refill = time.time()
        self._lock = asyncio.Lock()
    
    def _refill_tokens(self):
        now = time.time()
        elapsed = now - self.last_refill
        refill_amount = int(elapsed * (self.rpm / 60))
        
        if refill_amount > 0:
            self.tokens = min(self.rpm, self.tokens + refill_amount)
            self.last_refill = now
    
    async def _acquire_token(self):
        while self.tokens <= 0:
            self._refill_tokens()
            if self.tokens <= 0:
                await asyncio.sleep(1)
        
        self.tokens -= 1
    
    def _calculate_backoff(self, attempt: int) -> float:
        delay = self.config.base_delay * (2 ** attempt)
        jitter = delay * self.config.jitter_factor * random.random()
        return min(delay + jitter, self.config.max_delay)
    
    def _is_rate_limit_error(self, error: Exception) -> bool:
        return any(code in str(error) for code in ['429', 'RESOURCE_EXHAUSTED', 'quota'])
    
    async def with_retry(
        self,
        operation: Callable[..., T],
        *args,
        **kwargs
    ) -> T:
        last_error = None
        
        for attempt in range(self.config.max_retries + 1):
            try:
                await self._acquire_token()
                return await operation(*args, **kwargs)
            except Exception as e:
                last_error = e
                
                if self._is_rate_limit_error(e):
                    delay = self._calculate_backoff(attempt)
                    print(f"Rate limit hit, retrying in {delay:.2f}s...")
                    await asyncio.sleep(delay)
                    continue
                
                raise
        
        raise last_error
```

### Anti-Pattern #5: Poor Multimodal Input Handling

#### Mô Tả Vấn Đề

Sending images/audio/video với quality hoặc format không optimized. Not properly handling different modalities or mixing them incorrectly.

#### Common Mistakes

1. **Sending images at full camera resolution** - Unnecessarily increases token count và latency
2. **Using wrong mime types** - Causing parsing errors
3. **Not specifying what to extract** - Getting incomplete or irrelevant information
4. **Mixing modalities incorrectly** - Breaking the model's input format expectations

#### Cách Khắc Phục

```typescript
interface ImageOptimizationConfig {
  maxWidth: number;
  maxHeight: number;
  quality: number;
  format: 'jpeg' | 'png' | 'webp';
}

const IMAGE_OPTIMIZATION: Record<string, ImageOptimizationConfig> = {
  thumbnail: { maxWidth: 224, maxHeight: 224, quality: 70, format: 'jpeg' },
  standard: { maxWidth: 768, maxHeight: 768, quality: 85, format: 'jpeg' },
  high: { maxWidth: 1536, maxHeight: 1536, quality: 90, format: 'png' },
};

interface MultimodalInput {
  text?: string;
  image?: {
    data: Buffer;
    mimeType: string;
    optimization?: keyof typeof IMAGE_OPTIMIZATION;
  };
  audio?: {
    data: Buffer;
    sampleRate?: number;
  };
}

async function buildMultimodalContent(
  inputs: MultimodalInput[]
): Promise<Array<{ text?: string; inlineData?: { mimeType: string; data: string } }>> {
  const contents: Array<{ text?: string; inlineData?: { mimeType: string; data: string } }> = [];
  
  for (const input of inputs) {
    if (input.text) {
      contents.push({ text: input.text });
    }
    
    if (input.image) {
      const optimized = await optimizeImage(
        input.image.data,
        input.image.optimization || 'standard'
      );
      contents.push({
        inlineData: {
          mimeType: optimized.mimeType,
          data: optimized.data.toString('base64'),
        },
      });
    }
    
    if (input.audio) {
      contents.push({
        inlineData: {
          mimeType: 'audio/wav',
          data: input.audio.data.toString('base64'),
        },
      });
    }
  }
  
  return contents;
}

async function optimizeImage(
  imageData: Buffer,
  preset: keyof typeof IMAGE_OPTIMIZATION
): Promise<{ data: Buffer; mimeType: string }> {
  const config = IMAGE_OPTIMIZATION[preset];
  
  // Sử dụng Sharp để resize và optimize
  // const sharp = require('sharp');
  // const optimized = await sharp(imageData)
  //   .resize(config.maxWidth, config.maxHeight, { fit: 'inside' })
  //   .toFormat(config.format, { quality: config.quality })
  //   .toBuffer();
  
  // Placeholder - implement với actual image processing
  return {
    data: imageData,
    mimeType: `image/${config.format}`,
  };
}

// Multimodal analysis với clear instructions
interface MultimodalAnalysisResult {
  description?: string;
  extractedText?: string;
  structuredData?: Record<string, unknown>;
  analysis?: string;
}

async function analyzeMultimodal(
  inputs: MultimodalInput[],
  analysisType: 'describe' | 'extract' | 'analyze' | 'compare'
): Promise<MultimodalAnalysisResult> {
  const promptTemplate = {
    describe: 'Provide a detailed description of the content in this image.',
    extract: 'Extract all text visible in this image. Return ONLY the text, nothing else.',
    analyze: 'Analyze this image thoroughly and provide insights about its content, structure, and any notable features.',
    compare: 'Compare these images. Highlight similarities and differences.',
  };
  
  const contents = await buildMultimodalContent(inputs);
  
  const result = await model.generateContent({
    contents: [{ role: 'user', parts: contents }],
    generationConfig: {
      maxOutputTokens: analysisType === 'extract' ? 2048 : 4096,
    },
  });
  
  return {
    description: result.response.text(),
  };
}
```

```python
# Python multimodal handling
from dataclasses import dataclass
from typing import Optional, Literal
from io import BytesIO
from PIL import Image

@dataclass
class ImageConfig:
    max_width: int = 768
    max_height: int = 768
    quality: int = 85
    format: str = "JPEG"

@dataclass
class MultimodalInput:
    text: Optional[str] = None
    image_path: Optional[str] = None
    image_bytes: Optional[bytes] = None
    mime_type: Optional[str] = None

def optimize_image(
    image_source: bytes | Image.Image,
    config: ImageConfig = None
) -> tuple[bytes, str]:
    config = config or ImageConfig()
    
    if isinstance(image_source, bytes):
        image = Image.open(BytesIO(image_source))
    else:
        image = image_source
    
    # Resize if needed
    if image.width > config.max_width or image.height > config.max_height:
        image.thumbnail((config.max_width, config.max_height), Image.Resampling.LANCZOS)
    
    # Convert to RGB if necessary
    if image.mode in ('RGBA', 'P'):
        image = image.convert('RGB')
    
    # Save with compression
    output = BytesIO()
    save_format = 'JPEG' if config.format == 'JPEG' else 'PNG'
    image.save(output, format=save_format, quality=config.quality)
    
    mime_type = f'image/{config.format.lower()}'
    return output.getvalue(), mime_type

async def analyze_multimodal(
    inputs: list[MultimodalInput],
    analysis_type: Literal["describe", "extract", "analyze"] = "analyze"
) -> str:
    contents = []
    
    for inp in inputs:
        if inp.text:
            contents.append({"text": inp.text})
        
        if inp.image_bytes:
            optimized_bytes, mime_type = optimize_image(inp.image_bytes)
            contents.append({
                "inline_data": {
                    "mime_type": mime_type,
                    "data": base64.b64encode(optimized_bytes).decode()
                }
            })
    
    prompts = {
        "describe": "Describe this image in detail.",
        "extract": "Extract all visible text from this image.",
        "analyze": "Analyze this image thoroughly and provide detailed insights."
    }
    
    contents.append({"text": prompts[analysis_type]})
    
    response = await model.generate_content_async({
        "contents": [{"parts": contents}]
    })
    
    return response.text
```

### Anti-Pattern #6: Not Using Context Caching

#### Mô Tả Vấn Đề

Repeating same context across multiple API calls. For example, when processing multiple queries about the same document, developers send the entire document with each query instead of caching it once.

#### Hậu Quả

Cost cao hơn đáng kể. Higher latency vì same context được transmitted mỗi lần. Wasted API quota.

#### Giải Pháp

```typescript
class ContextCacheService {
  private cache: Map<string, { cachedContent: string; tokenCount: number }> = new Map();
  
  async cacheContext(
    contextId: string,
    content: string,
    ttlSeconds: number = 3600
  ): Promise<number> {
    const tokenCount = await this.countTokens(content);
    
    // Store in application cache
    this.cache.set(contextId, { cachedContent: content, tokenCount });
    
    // Also cache on API level if using Vertex AI
    if (this.useAPICaching) {
      await this.createAPICache(contextId, content, ttlSeconds);
    }
    
    return tokenCount;
  }
  
  async getCachedResponse(
    contextId: string,
    query: string
  ): Promise<string> {
    const cached = this.cache.get(contextId);
    if (!cached) {
      throw new Error(`Context ${contextId} not found in cache`);
    }
    
    // Calculate cache benefit
    const queryTokens = await this.countTokens(query);
    const totalWithoutCache = cached.tokenCount + queryTokens;
    const totalWithCache = queryTokens;
    
    console.log(`Cache benefit: ${totalWithoutCache - totalWithCache} tokens saved`);
    
    // Use cached context for response
    const result = await model.generateContent({
      contents: [{ role: 'user', parts: [{ text: cached.cachedContent }] }],
    });
    
    return result.response.text();
  }
  
  private async countTokens(text: string): Promise<number> {
    // Approximation: ~4 characters per token for English
    // For accurate count, use tiktoken or Gemini's token counting API
    return Math.ceil(text.length / 4);
  }
}
```

### Anti-Pattern #7: Improper Error Handling

#### Mô Tả Vấn Đề

Generic try-catch blocks that swallow errors or don't differentiate between different error types. Not handling specific Gemini API errors like safety blocks, quota exceeded, or invalid requests.

#### Common Mistakes

```typescript
// ❌ ANTI-PATTERN: Generic error handling
async function generate(prompt: string) {
  try {
    return await model.generateContent(prompt);
  } catch (error) {
    console.error(error);
    return null; // Silent failure
  }
}

// ✅ BEST PRACTICE: Specific error handling
interface GeminiAPIError extends Error {
  code: string;
  status: number;
  details?: Record<string, unknown>;
}

type GeminiErrorType = 
  | 'authentication' 
  | 'quota_exceeded' 
  | 'rate_limited' 
  | 'safety_blocked'
  | 'invalid_request'
  | 'timeout'
  | 'internal_error';

async function generateWithErrorHandling(prompt: string): Promise<Result<string, GeminiError>> {
  try {
    const result = await model.generateContent(prompt);
    return { success: true, data: result.response.text() };
  } catch (error) {
    const geminiError = parseGeminiError(error as Error);
    
    return { 
      success: false, 
      error: geminiError,
      userMessage: getUserFriendlyMessage(geminiError.type)
    };
  }
}

function parseGeminiError(error: Error): GeminiAPIError {
  const message = error.message.toLowerCase();
  
  if (message.includes('api_key') || message.includes('auth')) {
    return { ...error, code: 'AUTH_ERROR', status: 401, type: 'authentication' } as GeminiAPIError;
  }
  
  if (message.includes('quota') || message.includes('limit')) {
    return { ...error, code: 'QUOTA_EXCEEDED', status: 429, type: 'quota_exceeded' } as GeminiAPIError;
  }
  
  if (message.includes('rate') || message.includes('429')) {
    return { ...error, code: 'RATE_LIMITED', status: 429, type: 'rate_limited' } as GeminiAPIError;
  }
  
  if (message.includes('safety') || message.includes('blocked')) {
    return { ...error, code: 'SAFETY_BLOCK', status: 400, type: 'safety_blocked' } as GeminiAPIError;
  }
  
  if (message.includes('invalid') || message.includes('malformed')) {
    return { ...error, code: 'INVALID_REQUEST', status: 400, type: 'invalid_request' } as GeminiAPIError;
  }
  
  return { ...error, code: 'UNKNOWN', status: 500, type: 'internal_error' } as GeminiAPIError;
}

function getUserFriendlyMessage(type: GeminiErrorType): string {
  const messages: Record<GeminiErrorType, string> = {
    authentication: 'API authentication failed. Please check your credentials.',
    quota_exceeded: 'Monthly quota exceeded. Please upgrade your plan.',
    rate_limited: 'Too many requests. Please wait a moment and try again.',
    safety_blocked: 'Your request was blocked for safety. Please modify and try again.',
    invalid_request: 'Invalid request format. Please check your input.',
    timeout: 'Request timed out. Please try again.',
    internal_error: 'An internal error occurred. Please try again later.',
  };
  
  return messages[type];
}
```

### Anti-Pattern #8: Not Implementing Streaming Properly

#### Mô Tả Vấn Đề

Not using streaming when UX benefits from it, or implementing streaming incorrectly causing memory issues or incomplete responses.

#### Khi Nào Nên Dùng Streaming

- Long-form content generation
- Real-time user interfaces
- Chat applications
- Content preview before completion

#### Khi Nào Không Nên Dùng Streaming

- Short, quick responses
- Batch processing
- When response must be complete before display
- When streaming overhead > time savings

```typescript
interface StreamingConfig {
  chunkSize: number;
  includeMetadata: boolean;
  bufferSize: number;
}

class StreamingGenerator {
  async *generateStream(
    prompt: string,
    config: StreamingConfig = { chunkSize: 1, includeMetadata: true, bufferSize: 10 }
  ): AsyncGenerator<StreamChunk> {
    const buffer: string[] = [];
    
    const stream = await model.generateContentStream(prompt);
    
    for await (const chunk of stream.stream) {
      const text = chunk.text();
      if (!text) continue;
      
      buffer.push(text);
      
      if (buffer.length >= config.bufferSize) {
        yield {
          text: buffer.join(''),
          complete: false,
          tokensGenerated: buffer.join('').length / 4,
        };
        buffer.length = 0;
      }
    }
    
    // Yield remaining
    if (buffer.length > 0) {
      yield {
        text: buffer.join(''),
        complete: true,
        tokensGenerated: buffer.join('').length / 4,
      };
    }
  }
}

interface StreamChunk {
  text: string;
  complete: boolean;
  tokensGenerated: number;
}
```

## Common Patterns Để Tránh

### Pattern 1: Prompt Injection Vulnerabilities

```typescript
// ❌ Vulnerable: User input directly concatenated
const prompt = `Translate to French: ${userInput}`;

// ✅ Safe: Input properly structured and validated
function buildSafePrompt(userInput: string, task: string): string {
  // Sanitize and escape special characters
  const sanitized = sanitizeUserInput(userInput);
  
  // Use structured prompts
  return JSON.stringify({
    task,
    input: sanitized,
    constraints: ['No code execution', 'No system override attempts']
  });
}
```

### Pattern 2: Not Validating Outputs

```typescript
// ❌ No output validation
const response = await model.generateContent(prompt);
processOutput(response.text()); // Trusting output blindly

// ✅ Output validation
interface ValidatedOutput<T> {
  valid: boolean;
  data?: T;
  errors?: string[];
}

function validateOutput<T>(
  response: string,
  schema: z.ZodSchema<T>
): ValidatedOutput<T> {
  try {
    const parsed = schema.parse(JSON.parse(response));
    return { valid: true, data: parsed };
  } catch (error) {
    return { 
      valid: false, 
      errors: [(error as Error).message],
      // Fallback: try to extract partial data
      data: extractPartialData(response, schema)
    };
  }
}
```

## Troubleshooting Guide

### Issue: Unexpected Safety Blocks

**Symptoms**: Legitimate content getting blocked

**Diagnosis Steps**:
1. Check which category is being triggered
2. Review user input for potential triggers
3. Consider adjusting threshold if content is safe

**Solutions**:
- Lower safety threshold (but evaluate risks)
- Rephrase input to avoid triggers
- Use content moderation pre-filter

### Issue: High Latency

**Symptoms**: Responses taking > 10 seconds

**Diagnosis Steps**:
1. Check input token count
2. Verify model tier
3. Check if using streaming appropriately

**Solutions**:
- Optimize prompt length
- Use faster model (Flash vs Pro)
- Implement caching
- Consider async processing

### Issue: Cost Overruns

**Symptoms**: Unexpectedly high API bills

**Diagnosis Steps**:
1. Check token usage in logs
2. Review model selection per endpoint
3. Verify caching is working

**Solutions**:
- Implement token budgets
- Use context caching
- Select appropriate model tier
- Add usage monitoring

## Examples

### Example 1: Complete Error-Safe Implementation

```typescript
class GeminiService {
  constructor(
    private readonly model: GenerativeModel,
    private readonly config: ServiceConfig
  ) {}
  
  async generate(prompt: string): Promise<GenerationResult> {
    // Validate input
    if (!prompt.trim()) {
      return { success: false, error: 'Empty prompt' };
    }
    
    // Check token budget
    const estimatedTokens = this.estimateTokens(prompt);
    if (estimatedTokens > this.config.maxInputTokens) {
      return { success: false, error: 'Input too long' };
    }
    
    try {
      const result = await this.rateLimitedClient.withRetry(
        () => this.model.generateContent(prompt)
      );
      
      const text = result.response.text();
      
      // Validate output
      if (!text || text.trim().length === 0) {
        return { success: false, error: 'Empty response' };
      }
      
      return { success: true, data: text };
      
    } catch (error) {
      return this.handleError(error);
    }
  }
  
  private handleError(error: unknown): GenerationResult {
    const err = error as Error;
    
    if (err.message.includes('SAFETY')) {
      return { 
        success: false, 
        error: 'Content blocked',
        retryable: false 
      };
    }
    
    if (err.message.includes('quota') || err.message.includes('429')) {
      return { 
        success: false, 
        error: 'Quota exceeded',
        retryable: true,
        retryAfter: 60000
      };
    }
    
    return { 
      success: false, 
      error: 'Unknown error',
      retryable: true 
    };
  }
}
```

### Example 2: Production Multimodal Pipeline

```typescript
interface MultimodalPipelineConfig {
  imagePreset: 'thumbnail' | 'standard' | 'high';
  maxRetries: number;
  enableCaching: boolean;
}

class MultimodalPipeline {
  constructor(
    private readonly visionModel: GenerativeModel,
    private readonly textModel: GenerativeModel,
    private readonly cache: ContextCacheService,
    private readonly config: MultimodalPipelineConfig
  ) {}
  
  async processDocument(
    documentId: string,
    image: Buffer,
    query: string
  ): Promise<PipelineResult> {
    // 1. Check cache
    const cachedAnalysis = await this.cache.get(documentId);
    if (cachedAnalysis && this.config.enableCaching) {
      return this.queryCachedAnalysis(cachedAnalysis, query);
    }
    
    // 2. Optimize image
    const optimized = await this.optimizeImage(image, this.config.imagePreset);
    
    // 3. Extract content from image
    const extraction = await this.extractWithRetry({
      image: optimized,
      prompt: 'Extract all text and structure from this document.'
    });
    
    // 4. Cache if enabled
    if (this.config.enableCaching) {
      await this.cache.set(documentId, extraction);
    }
    
    // 5. Answer query
    const answer = await this.answerWithRetry({
      context: extraction,
      question: query
    });
    
    return { extraction, answer, cached: false };
  }
  
  private async extractWithRetry(input: { image: Buffer; prompt: string }): Promise<string> {
    for (let attempt = 0; attempt < this.config.maxRetries; attempt++) {
      try {
        const result = await this.visionModel.generateContent({
          contents: [{ 
            role: 'user', 
            parts: [
              { inlineData: { mimeType: 'image/jpeg', data: input.image.toString('base64') } },
              { text: input.prompt }
            ]
          }]
        });
        return result.response.text();
      } catch (error) {
        if (attempt === this.config.maxRetries - 1) throw error;
        await this.delay(1000 * Math.pow(2, attempt));
      }
    }
    throw new Error('Max retries exceeded');
  }
  
  private async answerWithRetry(input: { context: string; question: string }): Promise<string> {
    const prompt = `Based on the following document:\n\n${input.context}\n\nAnswer: ${input.question}`;
    
    for (let attempt = 0; attempt < this.config.maxRetries; attempt++) {
      try {
        const result = await this.textModel.generateContent(prompt);
        return result.response.text();
      } catch (error) {
        if (attempt === this.config.maxRetries - 1) throw error;
        await this.delay(1000 * Math.pow(2, attempt));
      }
    }
    throw new Error('Max retries exceeded');
  }
  
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

## References

- [Google Gemini API Documentation](https://ai.google.dev/docs/gemini_api)
- [Vertex AI Gemini Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/overview)
- [Safety Settings Guide](https://ai.google.dev/docs/safety_guidance)
- [Gemini API Pricing](https://ai.google.dev/pricing)
- [Token Counting](https://ai.google.dev/docs/token_counting)
- [Context Caching](https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache)
- [Rate Limits](https://cloud.google.com/vertex-ai/quotas)
