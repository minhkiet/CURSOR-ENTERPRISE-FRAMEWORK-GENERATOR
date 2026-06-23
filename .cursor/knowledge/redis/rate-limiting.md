---
title: "Redis Rate Limiting"
description: "Hướng dẫn toàn diện về các rate limiting patterns với Redis bao gồm sliding window, token bucket, fixed window, leaky bucket, Redis Lua scripts cho atomic operations và IP whitelist/blacklist patterns"
tags: ["redis", "rate-limiting", "throttling", "token-bucket", "sliding-window", "fixed-window", "leaky-bucket", "lua-script", "redis-lua"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Redis Rate Limiting

## 1. Tổng Quan (Overview)

Rate limiting là một kỹ thuật quan trọng trong việc bảo vệ hệ thống khỏi quá tải, abuse, và DDoS attacks. Nó kiểm soát số lượng requests mà một client có thể thực hiện trong một khoảng thời gian nhất định.

Redis là lựa chọn lý tưởng cho rate limiting vì:
- **Performance cao**: In-memory operations với sub-millisecond latency
- **Atomic operations**: Đảm bảo thread-safety và consistency
- **Scalability**: Hỗ trợ cluster mode cho distributed systems
- **Flexibility**: Nhiều data structures phù hợp với various algorithms

Bài viết này sẽ đi sâu vào các rate limiting algorithms phổ biến, cách implement chúng với Redis, và best practices cho production deployments.

## 2. Fixed Window Rate Limiting

### 2.1 Giới Thiệu

Fixed window là algorithm đơn giản nhất. Nó chia thời gian thành các windows cố định (ví dụ: mỗi phút) và đếm số requests trong mỗi window. Khi một window kết thúc, counter reset về 0.

### 2.2 Algorithm

```
┌─────────────┬─────────────┬─────────────┐
│ Window 1    │ Window 2    │ Window 3    │
│ 00:00-01:00│ 01:00-02:00│ 02:00-03:00│
├─────────────┼─────────────┼─────────────┤
│ ████████    │ ██████      │ ████        │
│ 100/100 req │ 60/100 req  │ 40/100 req  │
└─────────────┴─────────────┴─────────────┘

Problems:
- Burst at window boundaries (100 requests in last second of window 1
  + 100 requests in first second of window 2 = 200 requests in 2 seconds)
```

### 2.3 Implementation

```typescript
import Redis from 'ioredis';

interface RateLimitResult {
  allowed: boolean;
  remaining: number;
  limit: number;
  resetAt: number;
  resetIn: number;
}

class FixedWindowRateLimiter {
  private redis: Redis;
  private windowSeconds: number;
  private maxRequests: number;
  private keyPrefix: string;

  constructor(
    redis: Redis,
    options: {
      windowSeconds: number;
      maxRequests: number;
      keyPrefix?: string;
    }
  ) {
    this.redis = redis;
    this.windowSeconds = options.windowSeconds;
    this.maxRequests = options.maxRequests;
    this.keyPrefix = options.keyPrefix || 'ratelimit:fixed';
  }

  private getKey(identifier: string): string {
    const windowId = Math.floor(Date.now() / (this.windowSeconds * 1000));
    return `${this.keyPrefix}:${identifier}:${windowId}`;
  }

  async checkLimit(identifier: string): Promise<RateLimitResult> {
    const key = this.getKey(identifier);
    const now = Date.now();
    const windowStart = Math.floor(now / (this.windowSeconds * 1000)) * (this.windowSeconds * 1000);
    const resetAt = windowStart + this.windowSeconds * 1000;
    const resetIn = Math.max(0, Math.ceil((resetAt - now) / 1000));

    const pipeline = this.redis.pipeline();

    // Get current count
    pipeline.incr(key);

    // Set expiry to window duration (add buffer for safety)
    pipeline.expire(key, this.windowSeconds + 60);

    const results = await pipeline.exec();

    if (!results) {
      throw new Error('Redis pipeline failed');
    }

    const count = results[0][1] as number;

    return {
      allowed: count <= this.maxRequests,
      remaining: Math.max(0, this.maxRequests - count),
      limit: this.maxRequests,
      resetAt,
      resetIn,
    };
  }

  async resetLimit(identifier: string): Promise<void> {
    const key = this.getKey(identifier);
    await this.redis.del(key);
  }

  async getCurrentCount(identifier: string): Promise<number> {
    const key = this.getKey(identifier);
    const count = await this.redis.get(key);
    return count ? parseInt(count) : 0;
  }
}

// Usage
const limiter = new FixedWindowRateLimiter(redis, {
  windowSeconds: 60,    // 1 minute window
  maxRequests: 100,    // 100 requests per minute
  keyPrefix: 'api:ratelimit',
});

async function handleRequest(req: Request, res: Response) {
  const clientId = req.headers['x-client-id'] as string || req.ip;

  const result = await limiter.checkLimit(clientId);

  res.set({
    'X-RateLimit-Limit': result.limit.toString(),
    'X-RateLimit-Remaining': result.remaining.toString(),
    'X-RateLimit-Reset': result.resetAt.toString(),
  });

  if (!result.allowed) {
    return res.status(429).json({
      error: 'Too Many Requests',
      retryAfter: result.resetIn,
    });
  }

  // Process request...
}
```

### 2.4 Python Implementation

```python
import redis
import time
from typing import Optional, Dict

class FixedWindowRateLimiter:
    """
    Fixed Window Rate Limiter implementation
    
    Pros:
    - Simple to implement
    - Memory efficient
    - Good for simple use cases
    
    Cons:
    - Allows burst at window boundaries (2x the limit)
    - May not be fair across window boundaries
    """
    
    def __init__(
        self,
        redis_client: redis.Redis,
        max_requests: int,
        window_seconds: int,
        key_prefix: str = "ratelimit:fixed"
    ):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.key_prefix = key_prefix
    
    def _get_key(self, identifier: str) -> str:
        """Generate key based on current window"""
        window_id = int(time.time()) // self.window_seconds
        return f"{self.key_prefix}:{identifier}:{window_id}"
    
    def check_limit(self, identifier: str) -> Dict:
        """
        Check if request is within rate limit
        
        Returns dict with:
        - allowed: bool
        - remaining: int
        - limit: int
        - reset_at: int (timestamp)
        - reset_in: int (seconds)
        """
        key = self._get_key(identifier)
        now = time.time()
        
        # Calculate window boundaries
        current_window = int(now // self.window_seconds)
        window_start = current_window * self.window_seconds
        reset_at = (current_window + 1) * self.window_seconds
        reset_in = int(reset_at - now)
        
        # Atomic increment and expire
        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, self.window_seconds + 60)  # Add buffer
        results = pipe.execute()
        
        count = results[0]
        
        return {
            'allowed': count <= self.max_requests,
            'remaining': max(0, self.max_requests - count),
            'limit': self.max_requests,
            'reset_at': int(reset_at),
            'reset_in': max(0, reset_in),
            'current': count,
        }
    
    def is_allowed(self, identifier: str) -> bool:
        """Simple boolean check"""
        return self.check_limit(identifier)['allowed']
    
    def reset(self, identifier: str) -> bool:
        """Reset rate limit for identifier"""
        key = self._get_key(identifier)
        return self.redis.delete(key) > 0
    
    def get_usage(self, identifier: str) -> int:
        """Get current usage count"""
        key = self._get_key(identifier)
        count = self.redis.get(key)
        return int(count) if count else 0


# Usage example
if __name__ == "__main__":
    client = redis.Redis(host='localhost', port=6379)
    limiter = FixedWindowRateLimiter(
        redis_client=client,
        max_requests=100,
        window_seconds=60,  # 1 minute
        key_prefix="api:v1"
    )
    
    # Check rate limit
    result = limiter.check_limit("user:123")
    
    print(f"Allowed: {result['allowed']}")
    print(f"Remaining: {result['remaining']}")
    print(f"Reset in: {result['reset_in']}s")
    
    # Add headers to response
    def add_rate_limit_headers(response, result):
        response.headers['X-RateLimit-Limit'] = str(result['limit'])
        response.headers['X-RateLimit-Remaining'] = str(result['remaining'])
        response.headers['X-RateLimit-Reset'] = str(result['reset_at'])
        return response
```

## 3. Sliding Window Rate Limiting

### 3.1 Giới Thiệu

Sliding window algorithm khắc phục nhược điểm của fixed window bằng cách xem xét requests trong một window trượt theo thời gian thực. Mỗi request được evaluate dựa trên thời gian của nó và các requests trước đó.

### 3.2 Algorithm

```
Sliding Window (1 minute, 100 requests):

Time: 00:00 ────────────────────────────────────────────► 01:00

Requests at:
  t=10s: █ (10 seconds ago)
  t=20s: █ (20 seconds ago)
  t=30s: █ (30 seconds ago)
  t=40s: █ (40 seconds ago)
  t=50s: █ (50 seconds ago)
  
Current window: last 60 seconds
At t=55s, requests in window: 5
At t=61s, requests in window: 4 (t=10s request expires)

┌──────────────────────────────────────────────────────┐
│ Window from t=0 to t=60s                    [ACTIVE] │
│ Requests: 5                              [EXPIRED→] │
└──────────────────────────────────────────────────────┘
```

### 3.3 Implementation

```typescript
import Redis from 'ioredis';

class SlidingWindowRateLimiter {
  private redis: Redis;
  private windowMs: number;
  private maxRequests: number;
  private keyPrefix: string;

  constructor(
    redis: Redis,
    options: {
      windowSeconds: number;
      maxRequests: number;
      keyPrefix?: string;
    }
  ) {
    this.redis = redis;
    this.windowMs = options.windowSeconds * 1000;
    this.maxRequests = options.maxRequests;
    this.keyPrefix = options.keyPrefix || 'ratelimit:sliding';
  }

  async checkLimit(identifier: string): Promise<RateLimitResult> {
    const key = `${this.keyPrefix}:${identifier}`;
    const now = Date.now();
    const windowStart = now - this.windowMs;

    // Use Lua script for atomic operations
    const script = `
      local key = KEYS[1]
      local now = tonumber(ARGV[1])
      local window_start = tonumber(ARGV[2])
      local max_requests = tonumber(ARGV[3])
      local window_ms = tonumber(ARGV[4])

      -- Remove old entries outside the window
      redis.call('ZREMRANGEBYSCORE', key, 0, window_start)

      -- Count current requests in window
      local current = redis.call('ZCARD', key)

      -- Check if limit exceeded
      if current >= max_requests then
        -- Get oldest request timestamp
        local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
        local reset_at = oldest and oldest[2] and 
          (tonumber(oldest[2]) + window_ms) or now + window_ms
        return {0, current, reset_at}
      end

      -- Add new request
      redis.call('ZADD', key, now, now .. ':' .. math.random())

      -- Set expiry on the key
      redis.call('PEXPIRE', key, window_ms)

      return {1, current + 1, now + window_ms}
    `;

    const result = await this.redis.eval(
      script,
      1,
      key,
      now.toString(),
      windowStart.toString(),
      this.maxRequests.toString(),
      this.windowMs.toString()
    ) as [number, number, number];

    const [allowed, count, resetAt] = result;

    return {
      allowed: allowed === 1,
      remaining: Math.max(0, this.maxRequests - count),
      limit: this.maxRequests,
      resetAt: resetAt,
      resetIn: Math.max(0, Math.ceil((resetAt - now) / 1000)),
    };
  }

  async checkLimitWithPipeline(identifier: string): Promise<RateLimitResult> {
    const key = `${this.keyPrefix}:${identifier}`;
    const now = Date.now();
    const windowStart = now - this.windowMs;

    // Alternative: Use pipeline for slightly better performance
    // (Note: Not fully atomic, but good enough for most cases)
    const pipeline = this.redis.pipeline();

    // Remove old entries
    pipeline.zremrangebyscore(key, 0, windowStart);

    // Get current count
    pipeline.zcard(key);

    // Execute pipeline
    const results = await pipeline.exec();

    if (!results) {
      throw new Error('Pipeline failed');
    }

    const count = results[1]?.[1] as number || 0;

    if (count >= this.maxRequests) {
      return {
        allowed: false,
        remaining: 0,
        limit: this.maxRequests,
        resetAt: now + this.windowMs,
        resetIn: this.windowSeconds,
      };
    }

    // Add new request
    const addPipeline = this.redis.pipeline();
    addPipeline.zadd(key, now, `${now}:${Math.random()}`);
    addPipeline.pexpire(key, this.windowMs);
    addPipeline.zcard(key);
    await addPipeline.exec();

    return {
      allowed: true,
      remaining: this.maxRequests - count - 1,
      limit: this.maxRequests,
      resetAt: now + this.windowMs,
      resetIn: this.windowSeconds,
    };
  }

  async getUsage(identifier: string): Promise<{ count: number; oldest: number | null }> {
    const key = `${this.keyPrefix}:${identifier}`;
    const now = Date.now();
    const windowStart = now - this.windowMs;

    // Remove old entries first
    await this.redis.zremrangebyscore(key, 0, windowStart);

    // Get count and oldest
    const [count, oldestResult] = await Promise.all([
      this.redis.zcard(key),
      this.redis.zrange(key, 0, 0, 'WITHSCORES'),
    ]);

    return {
      count,
      oldest: oldestResult.length >= 2 ? parseInt(oldestResult[1]) : null,
    };
  }

  async reset(identifier: string): Promise<void> {
    const key = `${this.keyPrefix}:${identifier}`;
    await this.redis.del(key);
  }

  private get windowSeconds(): number {
    return this.windowMs / 1000;
  }
}
```

### 3.4 Python Implementation

```python
import redis
import time
import random
from typing import Dict, Optional

class SlidingWindowRateLimiter:
    """
    Sliding Window Rate Limiter using Redis Sorted Sets
    
    Uses timestamps as scores for precise window calculation.
    More accurate than fixed window but uses more memory.
    """
    
    def __init__(
        self,
        redis_client: redis.Redis,
        max_requests: int,
        window_seconds: int,
        key_prefix: str = "ratelimit:sliding"
    ):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.window_ms = window_seconds * 1000
        self.key_prefix = key_prefix
    
    def _get_key(self, identifier: str) -> str:
        return f"{self.key_prefix}:{identifier}"
    
    def check_limit(self, identifier: str) -> Dict:
        """
        Check rate limit using sliding window algorithm
        """
        key = self._get_key(identifier)
        now_ms = int(time.time() * 1000)
        window_start = now_ms - self.window_ms
        
        # Lua script for atomic operations
        lua_script = """
        local key = KEYS[1]
        local now = tonumber(ARGV[1])
        local window_start = tonumber(ARGV[2])
        local max_requests = tonumber(ARGV[3])
        local window_ms = tonumber(ARGV[4])
        
        -- Remove expired entries
        redis.call('ZREMRANGEBYSCORE', key, 0, window_start)
        
        -- Count current entries
        local current = redis.call('ZCARD', key)
        
        -- Check limit
        if current >= max_requests then
            -- Get oldest entry to calculate reset time
            local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
            local reset_at = now + window_ms
            if oldest and #oldest >= 2 then
                reset_at = tonumber(oldest[2]) + window_ms
            end
            return {0, current, reset_at}
        end
        
        -- Add new request with unique member
        local member = now .. ':' .. math.random(1000000)
        redis.call('ZADD', key, now, member)
        
        -- Set expiry
        redis.call('PEXPIRE', key, window_ms)
        
        return {1, current + 1, now + window_ms}
        """
        
        result = self.redis.eval(
            lua_script,
            1,
            key,
            now_ms,
            window_start,
            self.max_requests,
            self.window_ms
        )
        
        allowed, count, reset_at = result
        reset_in = max(0, (reset_at - now_ms) / 1000)
        
        return {
            'allowed': bool(allowed),
            'remaining': max(0, self.max_requests - count),
            'limit': self.max_requests,
            'reset_at': int(reset_at / 1000),  # Convert to seconds
            'reset_in': int(reset_in),
            'current': count,
        }
    
    def is_allowed(self, identifier: str) -> bool:
        """Quick boolean check"""
        return self.check_limit(identifier)['allowed']
    
    def get_current_count(self, identifier: str) -> int:
        """Get current request count in window"""
        key = self._get_key(identifier)
        now_ms = int(time.time() * 1000)
        window_start = now_ms - self.window_ms
        
        # Remove expired and count
        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, window_start)
        pipe.zcard(key)
        results = pipe.execute()
        
        return results[1]
    
    def reset(self, identifier: str) -> bool:
        """Reset rate limit for identifier"""
        key = self._get_key(identifier)
        return self.redis.delete(key) > 0
    
    def get_window_info(self, identifier: str) -> Dict:
        """Get detailed window information"""
        key = self._get_key(identifier)
        now_ms = int(time.time() * 1000)
        window_start = now_ms - self.window_ms
        
        # Get all entries in window
        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, window_start)
        pipe.zrange(key, 0, -1, 'WITHSCORES')
        results = pipe.execute()
        
        entries = results[1]
        entries_info = []
        for i in range(0, len(entries), 2):
            timestamp = int(entries[i])
            entries_info.append({
                'timestamp': timestamp,
                'age_ms': now_ms - timestamp,
            })
        
        return {
            'identifier': identifier,
            'window_start': window_start,
            'window_end': now_ms,
            'total_requests': len(entries_info),
            'entries': entries_info,
        }


# Usage example
if __name__ == "__main__":
    client = redis.Redis(host='localhost', port=6379, decode_responses=False)
    limiter = SlidingWindowRateLimiter(
        redis_client=client,
        max_requests=100,
        window_seconds=60,
        key_prefix="api:v2"
    )
    
    # Test rate limiting
    for i in range(105):
        result = limiter.check_limit("user:456")
        status = "✓" if result['allowed'] else "✗"
        if i < 5 or not result['allowed']:
            print(f"{status} Request {i+1}: allowed={result['allowed']}, "
                  f"remaining={result['remaining']}, "
                  f"reset_in={result['reset_in']}s")
        
        if not result['allowed']:
            break
```

## 4. Token Bucket Rate Limiting

### 4.1 Giới Thiệu

Token bucket algorithm hoạt động giống như một cái bình chứa tokens. Mỗi request tiêu tốn một token, và tokens được refill với một rate nhất định. Algorithm này cho phép burst traffic trong khi vẫn duy trì average rate limit.

### 4.2 Algorithm

```
Token Bucket:
- Bucket capacity: 100 tokens (max)
- Refill rate: 10 tokens/second
- Token consumption: 1 token/request

Timeline:
Time: 0s ────────────────────────────────────────────►

Bucket:  [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]
         100/100 tokens (full at start)

After 5s of no requests:
Bucket:  [████████████████████░░░░░░░░░░░░░░░░░░░░░░]
         150/100 tokens (capped at capacity)

After 10 burst requests:
Bucket:  [████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]
         90/100 tokens

After 1s of refill (10 tokens added):
Bucket:  [████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░]
         100/100 tokens (capped)
```

### 4.3 Implementation

```typescript
import Redis from 'ioredis';

interface TokenBucketResult extends RateLimitResult {
  tokensRemaining: number;
}

class TokenBucketRateLimiter {
  private redis: Redis;
  private bucketCapacity: number;
  private refillRate: number; // tokens per second
  private keyPrefix: string;

  constructor(
    redis: Redis,
    options: {
      bucketCapacity: number;
      refillRate: number; // tokens per second
      keyPrefix?: string;
    }
  ) {
    this.redis = redis;
    this.bucketCapacity = options.bucketCapacity;
    this.refillRate = options.refillRate;
    this.keyPrefix = options.keyPrefix || 'ratelimit:tokenbucket';
  }

  async consume(
    identifier: string,
    tokens = 1
  ): Promise<TokenBucketResult> {
    const key = `${this.keyPrefix}:${identifier}`;

    const script = `
      local key = KEYS[1]
      local capacity = tonumber(ARGV[1])
      local refill_rate = tonumber(ARGV[2])
      local tokens_requested = tonumber(ARGV[3])
      local now = tonumber(ARGV[4])

      -- Get current bucket state
      local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
      local tokens = tonumber(bucket[1])
      local last_refill = tonumber(bucket[2])

      -- Initialize if new bucket
      if not tokens then
        tokens = capacity
        last_refill = now
      end

      -- Calculate tokens to add based on time elapsed
      local elapsed = now - last_refill
      local tokens_to_add = elapsed * refill_rate / 1000
      tokens = math.min(capacity, tokens + tokens_to_add)
      last_refill = now

      -- Check if we have enough tokens
      local allowed = 0
      if tokens >= tokens_requested then
        tokens = tokens - tokens_requested
        allowed = 1
      end

      -- Update bucket state
      redis.call('HMSET', key, 'tokens', tokens, 'last_refill', last_refill)
      redis.call('EXPIRE', key, 3600)

      local reset_in = math.ceil((capacity - tokens) / refill_rate)

      return {allowed, tokens, now + reset_in * 1000}
    `;

    const result = await this.redis.eval(
      script,
      1,
      key,
      this.bucketCapacity.toString(),
      this.refillRate.toString(),
      tokens.toString(),
      Date.now().toString()
    ) as [number, number, number];

    const [allowed, tokensRemaining, resetAt] = result;

    return {
      allowed: allowed === 1,
      tokensRemaining: tokensRemaining,
      remaining: Math.floor(tokensRemaining),
      limit: this.bucketCapacity,
      resetAt,
      resetIn: Math.ceil((resetAt - Date.now()) / 1000),
    };
  }

  async getBucketState(identifier: string): Promise<{
    tokens: number;
    capacity: number;
    refillRate: number;
    lastRefill: number;
  } | null> {
    const key = `${this.keyPrefix}:${identifier}`;
    const state = await this.redis.hgetall(key);

    if (!state || Object.keys(state).length === 0) {
      return null;
    }

    return {
      tokens: parseFloat(state.tokens),
      capacity: this.bucketCapacity,
      refillRate: this.refillRate,
      lastRefill: parseInt(state.last_refill),
    };
  }

  async reset(identifier: string): Promise<void> {
    const key = `${this.keyPrefix}:${identifier}`;
    await this.redis.del(key);
  }

  async refill(identifier: string): Promise<void> {
    const key = `${this.keyPrefix}:${identifier}`;
    await this.redis.hset(key, 'tokens', this.bucketCapacity.toString());
  }
}

// Usage
const tokenBucket = new TokenBucketRateLimiter(redis, {
  bucketCapacity: 100,  // Max burst size
  refillRate: 10,      // 10 tokens per second
});

async function handleRequest(req: Request, res: Response) {
  const clientId = req.headers['x-client-id'] as string;

  const result = await tokenBucket.consume(clientId);

  res.set({
    'X-RateLimit-Limit': result.limit.toString(),
    'X-RateLimit-Remaining': result.remaining.toString(),
    'X-RateLimit-Reset': result.resetAt.toString(),
    'X-RateLimit-Bucket-Capacity': result.tokensRemaining.toString(),
  });

  if (!result.allowed) {
    return res.status(429).json({
      error: 'Rate limit exceeded',
      retryAfter: result.resetIn,
      bucketState: {
        tokensRemaining: result.tokensRemaining,
        refillRate: '10 tokens/second',
      },
    });
  }

  // Process request...
}
```

### 4.4 Python Implementation

```python
import redis
import time
from typing import Dict, Optional

class TokenBucketRateLimiter:
    """
    Token Bucket Rate Limiter implementation
    
    Pros:
    - Allows burst traffic while maintaining average rate
    - Smooth rate limiting
    - Good for API rate limiting with burst tolerance
    
    Cons:
    - More complex implementation
    - Requires atomic operations for accuracy
    """
    
    def __init__(
        self,
        redis_client: redis.Redis,
        bucket_capacity: int,
        refill_rate: float,  # tokens per second
        key_prefix: str = "ratelimit:tokenbucket"
    ):
        self.redis = redis_client
        self.bucket_capacity = bucket_capacity
        self.refill_rate = refill_rate
        self.key_prefix = key_prefix
    
    def _get_key(self, identifier: str) -> str:
        return f"{self.key_prefix}:{identifier}"
    
    def consume(self, identifier: str, tokens: int = 1) -> Dict:
        """
        Consume tokens from bucket
        
        Returns:
        - allowed: bool
        - tokens_remaining: float
        - limit: int
        - reset_at: int
        - reset_in: int
        """
        key = self._get_key(identifier)
        now_ms = int(time.time() * 1000)
        
        lua_script = """
        local key = KEYS[1]
        local capacity = tonumber(ARGV[1])
        local refill_rate = tonumber(ARGV[2])
        local tokens_requested = tonumber(ARGV[3])
        local now = tonumber(ARGV[4])
        
        -- Get current bucket state
        local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
        local current_tokens = tonumber(bucket[1])
        local last_refill = tonumber(bucket[2])
        
        -- Initialize new bucket
        if not current_tokens then
            current_tokens = capacity
            last_refill = now
        end
        
        -- Calculate tokens to add based on elapsed time
        local elapsed_ms = now - last_refill
        local elapsed_seconds = elapsed_ms / 1000.0
        local tokens_to_add = elapsed_seconds * refill_rate
        current_tokens = math.min(capacity, current_tokens + tokens_to_add)
        
        -- Update last refill time
        last_refill = now
        
        -- Check if we have enough tokens
        local allowed = 0
        if current_tokens >= tokens_requested then
            current_tokens = current_tokens - tokens_requested
            allowed = 1
        end
        
        -- Save bucket state
        redis.call('HMSET', key, 
                   'tokens', tostring(current_tokens), 
                   'last_refill', tostring(last_refill))
        redis.call('EXPIRE', key, 3600)  -- 1 hour TTL
        
        -- Calculate reset time (time to get 1 token back)
        local reset_in = 0
        if allowed == 0 then
            local tokens_needed = tokens_requested - current_tokens
            reset_in = math.ceil(tokens_needed / refill_rate)
        end
        
        return {
            allowed,
            current_tokens,
            now + (reset_in * 1000),
            reset_in
        }
        """
        
        result = self.redis.eval(
            lua_script,
            1,
            key,
            self.bucket_capacity,
            self.refill_rate,
            tokens,
            now_ms
        )
        
        allowed, tokens_remaining, reset_at_ms, reset_in = result
        
        return {
            'allowed': bool(allowed),
            'tokens_remaining': float(tokens_remaining),
            'remaining': int(float(tokens_remaining)),
            'limit': self.bucket_capacity,
            'reset_at': int(reset_at_ms / 1000),
            'reset_in': int(reset_in),
        }
    
    def is_allowed(self, identifier: str, tokens: int = 1) -> bool:
        """Quick boolean check"""
        return self.consume(identifier, tokens)['allowed']
    
    def get_bucket_state(self, identifier: str) -> Optional[Dict]:
        """Get current bucket state"""
        key = self._get_key(identifier)
        state = self.redis.hgetall(key)
        
        if not state:
            return None
        
        return {
            'tokens': float(state.get('tokens', self.bucket_capacity)),
            'capacity': self.bucket_capacity,
            'refill_rate': self.refill_rate,
            'last_refill': int(float(state.get('last_refill', 0))),
        }
    
    def reset(self, identifier: str) -> bool:
        """Reset bucket for identifier"""
        key = self._get_key(identifier)
        return self.redis.delete(key) > 0


# Usage example
if __name__ == "__main__":
    client = redis.Redis(host='localhost', port=6379)
    limiter = TokenBucketRateLimiter(
        redis_client=client,
        bucket_capacity=100,
        refill_rate=10.0  # 10 tokens per second
    )
    
    # Simulate burst traffic
    print("Simulating burst traffic...")
    for i in range(15):
        result = limiter.consume("burst-user", tokens=1)
        print(f"Request {i+1}: allowed={result['allowed']}, "
              f"tokens={result['tokens_remaining']:.2f}")
        if not result['allowed']:
            print(f"Rate limited! Retry in {result['reset_in']}s")
            break
    
    # Check bucket state
    state = limiter.get_bucket_state("burst-user")
    if state:
        print(f"\nBucket state: {state['tokens']:.2f}/{state['capacity']} tokens, "
              f"refill rate: {state['refill_rate']}/s")
```

## 5. Leaky Bucket Rate Limiting

### 5.1 Giới Thiệu

Leaky bucket algorithm hoạt động như một cái xô có lỗ rỉ ở đáy. Requests được thêm vào bucket và xử lý với một rate cố định. Nếu bucket đầy, requests mới bị reject. Algorithm này đảm bảo requests được xử lý với rate đều đặn.

### 5.2 Algorithm

```
Leaky Bucket:

        ┌─────────────────────────────────┐
        │  Incoming Requests               │
        │    ↓ ↓ ↓ ↓ ↓ ↓                  │
Requests │    █ █ █ █ █                  │
  Enter  │    █ █ █ █ █                  │
        │    █ █ █ █ █  (bucket fills)   │
        │    █ █ █ █ █ █ █              │
        └────┼────────────────────────────┘
             │ Leak Rate: 5 requests/sec
             ▼
        ┌────────────────────────────┐
        │ Processed at steady rate  │
        └────────────────────────────┘
```

### 5.3 Implementation

```typescript
import Redis from 'ioredis';

class LeakyBucketRateLimiter {
  private redis: Redis;
  private bucketSize: number;
  private leakRate: number; // requests per second
  private keyPrefix: string;

  constructor(
    redis: Redis,
    options: {
      bucketSize: number;
      leakRate: number; // requests per second
      keyPrefix?: string;
    }
  ) {
    this.redis = redis;
    this.bucketSize = options.bucketSize;
    this.leakRate = options.leakRate;
    this.keyPrefix = options.keyPrefix || 'ratelimit:leaky';
  }

  async checkLimit(identifier: string): Promise<RateLimitResult> {
    const key = `${this.keyPrefix}:${identifier}`;
    const now = Date.now();

    const script = `
      local key = KEYS[1]
      local bucket_size = tonumber(ARGV[1])
      local leak_rate = tonumber(ARGV[2])
      local now = tonumber(ARGV[3])

      -- Get current bucket state
      local bucket = redis.call('HMGET', key, 'level', 'last_update')
      local level = tonumber(bucket[1]) or 0
      local last_update = tonumber(bucket[2]) or now

      -- Calculate how much has leaked since last update
      local elapsed = (now - last_update) / 1000.0  -- seconds
      local leaked = elapsed * leak_rate
      level = math.max(0, level - leaked)

      -- Check if bucket can accept new request
      local allowed = 0
      if level < bucket_size then
        level = level + 1
        allowed = 1
      end

      -- Update state
      redis.call('HMSET', key, 'level', level, 'last_update', now)
      redis.call('EXPIRE', key, 3600)

      -- Calculate time until bucket is empty
      local reset_in = math.ceil(level / leak_rate)
      local reset_at = now + (reset_in * 1000)

      return {allowed, level, reset_at, reset_in}
    `;

    const result = await this.redis.eval(
      script,
      1,
      key,
      this.bucketSize.toString(),
      this.leakRate.toString(),
      now.toString()
    ) as [number, number, number, number];

    const [allowed, level, resetAt, resetIn] = result;

    return {
      allowed: allowed === 1,
      remaining: Math.max(0, Math.floor(this.bucketSize - level)),
      limit: this.bucketSize,
      resetAt,
      resetIn,
    };
  }

  async getBucketLevel(identifier: string): Promise<number> {
    const key = `${this.keyPrefix}:${identifier}`;
    const level = await this.redis.hget(key, 'level');
    return level ? parseFloat(level) : 0;
  }

  async reset(identifier: string): Promise<void> {
    const key = `${this.keyPrefix}:${identifier}`;
    await this.redis.del(key);
  }
}
```

## 6. Redis Lua Scripts cho Atomic Operations

### 6.1 Giới Thiệu

Lua scripts đảm bảo atomicity cho các operations phức tạp. Tất cả commands trong một script được execute như một atomic unit, không có race conditions.

### 6.2 Common Lua Patterns

```lua
-- Pattern 1: Sliding Window với Timestamp
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window_ms = tonumber(ARGV[2])
local max_requests = tonumber(ARGV[3])

-- Remove expired requests
redis.call('ZREMRANGEBYSCORE', key, 0, now - window_ms)

-- Count current requests
local count = redis.call('ZCARD', key)

if count >= max_requests then
    return {0, count, now + window_ms}
end

-- Add new request
redis.call('ZADD', key, now, now .. ':' .. math.random())
redis.call('PEXPIRE', key, window_ms)

return {1, count + 1, now + window_ms}
```

```lua
-- Pattern 2: Token Bucket với Precise Calculation
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local requested = tonumber(ARGV[3])
local now = tonumber(ARGV[4])

-- Get state
local state = redis.call('HMGET', key, 'tokens', 'last_refill')
local tokens = tonumber(state[1]) or capacity
local last_refill = tonumber(state[2]) or now

-- Calculate refill
local elapsed = (now - last_refill) / 1000.0
tokens = math.min(capacity, tokens + (elapsed * refill_rate))

-- Check and consume
local allowed = 0
if tokens >= requested then
    tokens = tokens - requested
    allowed = 1
end

-- Update state
redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
redis.call('EXPIRE', key, 3600)

return {allowed, tokens, now}
```

```lua
-- Pattern 3: Multi-tier Rate Limit (User + IP + Global)
local user_key = KEYS[1]
local ip_key = KEYS[2]
local global_key = KEYS[3]
local user_limit = tonumber(ARGV[1])
local ip_limit = tonumber(ARGV[2])
local global_limit = tonumber(ARGV[3])
local now = tonumber(ARGV[4])
local window = tonumber(ARGV[5])

-- Check all tiers
local user_count = redis.call('ZCOUNT', user_key, now - window, '+inf')
local ip_count = redis.call('ZCOUNT', ip_key, now - window, '+inf')
local global_count = redis.call('ZCOUNT', global_key, now - window, '+inf')

if user_count >= user_limit then
    return {0, 'user', user_count, user_limit}
end

if ip_count >= ip_limit then
    return {0, 'ip', ip_count, ip_limit}
end

if global_count >= global_limit then
    return {0, 'global', global_count, global_limit}
end

-- Add to all tiers
redis.call('ZADD', user_key, now, now)
redis.call('ZADD', ip_key, now, now)
redis.call('ZADD', global_key, now, now)

-- Set expiry
redis.call('PEXPIRE', user_key, window)
redis.call('PEXPIRE', ip_key, window)
redis.call('PEXPIRE', global_key, window)

return {1, 'ok', user_count + 1, user_limit}
```

### 6.3 Multi-tier Rate Limiter

```typescript
import Redis from 'ioredis';

interface MultiTierLimit {
  allowed: boolean;
  tier: string | null;
  current: number;
  limit: number;
  resetIn: number;
}

class MultiTierRateLimiter {
  private redis: Redis;
  private tiers: Map<string, { key: string; limit: number; window: number }>;
  private globalLimit: number;

  constructor(
    redis: Redis,
    config: {
      tiers: Array<{
        name: string;
        keyPrefix: string;
        limit: number;
        windowSeconds: number;
      }>;
      globalLimit: number;
      globalWindowSeconds: number;
    }
  ) {
    this.redis = redis;
    this.tiers = new Map();
    this.globalLimit = config.globalLimit;

    for (const tier of config.tiers) {
      this.tiers.set(tier.name, {
        key: tier.keyPrefix,
        limit: tier.limit,
        window: tier.windowSeconds * 1000,
      });
    }
  }

  async checkLimit(
    identifier: string,
    userId: string,
    ip: string
  ): Promise<MultiTierLimit> {
    const keys: string[] = [];
    const args: (string | number)[] = [];
    let argIndex = 1;

    // Build keys for each tier
    for (const [name, config] of this.tiers) {
      const identifierKey = name === 'user' ? userId : ip;
      keys.push(`${config.key}:${identifierKey}`);
      args.push(config.limit);
      args.push(config.window);
    }

    // Global key
    keys.push(`ratelimit:global`);
    args.push(this.globalLimit);
    args.push(24 * 60 * 60 * 1000); // 24 hours

    const now = Date.now();

    const script = `
      local now = tonumber(ARGV[${argIndex++}])
      local results = {}

      -- Check each tier
      for i = 1, #KEYS do
        local key = KEYS[i]
        local limit = tonumber(ARGV[${argIndex++}])
        local window = tonumber(ARGV[${argIndex++}])
        
        -- Remove expired
        redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
        
        -- Count
        local count = redis.call('ZCARD', key)
        
        if count >= limit then
          return {0, i, count, limit}
        end
        
        -- Add request
        redis.call('ZADD', key, now, now .. ':' .. math.random())
        redis.call('PEXPIRE', key, window)
        
        table.insert(results, count + 1)
      end

      return {1, 0, results[1], ARGV[${--argIndex}]}
    `;

    const result = await this.redis.eval(
      script,
      keys.length,
      ...keys,
      now,
      ...args
    ) as [number, number, number, number];

    const [allowed, tierIndex, current, limit] = result;

    if (allowed === 0) {
      const tierName = Array.from(this.tiers.keys())[tierIndex - 1] || 'global';
      const window = tierIndex <= this.tiers.size
        ? Array.from(this.tiers.values())[tierIndex - 1]!.window
        : 24 * 60 * 60 * 1000;

      return {
        allowed: false,
        tier: tierName,
        current,
        limit,
        resetIn: Math.ceil(window / 1000),
      };
    }

    return {
      allowed: true,
      tier: null,
      current,
      limit,
      resetIn: 60,
    };
  }
}

// Usage with Express middleware
class RateLimitMiddleware {
  private limiter: MultiTierRateLimiter;

  constructor(redis: Redis) {
    this.limiter = new MultiTierRateLimiter(redis, {
      tiers: [
        { name: 'user', keyPrefix: 'rl:user', limit: 100, windowSeconds: 60 },
        { name: 'ip', keyPrefix: 'rl:ip', limit: 500, windowSeconds: 60 },
      ],
      globalLimit: 10000,
      globalWindowSeconds: 86400,
    });
  }

  async handle(req: Request, res: Response, next: NextFunction): Promise<void> {
    const userId = (req.user as any)?.id || 'anonymous';
    const ip = req.ip || req.socket.remoteAddress || 'unknown';

    const result = await this.limiter.checkLimit(req.path, userId, ip);

    res.set({
      'X-RateLimit-Limit': result.limit.toString(),
      'X-RateLimit-Remaining': String(result.limit - result.current),
      'X-RateLimit-Reset': String(Math.floor(Date.now() / 1000) + result.resetIn),
      'X-RateLimit-Tier': result.tier || 'ok',
    });

    if (!result.allowed) {
      res.status(429).json({
        error: 'Rate limit exceeded',
        message: `Too many requests. Please try again in ${result.resetIn} seconds.`,
        tier: result.tier,
      });
      return;
    }

    next();
  }
}
```

## 7. IP Whitelist/Blacklist

### 7.1 IP Management Patterns

```typescript
import Redis from 'ioredis';

class IPLimiter {
  private redis: Redis;
  private blacklistKey = 'ip:blacklist';
  private whitelistKey = 'ip:whitelist';

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async addToBlacklist(ip: string, ttlSeconds?: number): Promise<void> {
    const key = `${this.blacklistKey}:${ip}`;
    await this.redis.set(key, Date.now().toString());
    
    if (ttlSeconds) {
      await this.redis.expire(key, ttlSeconds);
    }
  }

  async removeFromBlacklist(ip: string): Promise<void> {
    const key = `${this.blacklistKey}:${ip}`;
    await this.redis.del(key);
  }

  async isBlacklisted(ip: string): Promise<boolean> {
    const key = `${this.blacklistKey}:${ip}`;
    const exists = await this.redis.exists(key);
    return exists === 1;
  }

  async addToWhitelist(ip: string): Promise<void> {
    const key = `${this.whitelistKey}:${ip}`;
    await this.redis.set(key, '1');
  }

  async removeFromWhitelist(ip: string): Promise<void> {
    const key = `${this.whitelistKey}:${ip}`;
    await this.redis.del(key);
  }

  async isWhitelisted(ip: string): Promise<boolean> {
    const key = `${this.whitelistKey}:${ip}`;
    const exists = await this.redis.exists(key);
    return exists === 1;
  }

  async getBlacklistedIPs(pattern = '*'): Promise<string[]> {
    const keys = await this.redis.keys(`${this.blacklistKey}:${pattern}`);
    return keys.map(k => k.split(':').pop()!);
  }

  async getBlacklistCount(): Promise<number> {
    const keys = await this.redis.keys(`${this.blacklistKey}:*`);
    return keys.length;
  }
}

// Combined with Rate Limiting
class IntelligentRateLimiter {
  private ipLimiter: IPLimiter;
  private rateLimiter: SlidingWindowRateLimiter;
  private redis: Redis;

  constructor(redis: Redis) {
    this.redis = redis;
    this.ipLimiter = new IPLimiter(redis);
    this.rateLimiter = new SlidingWindowRateLimiter(redis, {
      windowSeconds: 60,
      maxRequests: 100,
    });
  }

  async checkRequest(ip: string, identifier: string): Promise<{
    allowed: boolean;
    reason?: string;
    whitelist?: boolean;
    blacklist?: boolean;
    rateLimit?: RateLimitResult;
  }> {
    // 1. Check whitelist first
    if (await this.ipLimiter.isWhitelisted(ip)) {
      return { allowed: true, whitelist: true };
    }

    // 2. Check blacklist
    if (await this.ipLimiter.isBlacklisted(ip)) {
      return {
        allowed: false,
        reason: 'IP is blacklisted',
        blacklist: true,
      };
    }

    // 3. Check rate limit
    const rateLimitResult = await this.rateLimiter.checkLimit(identifier);

    if (!rateLimitResult.allowed) {
      // Auto-blacklist after repeated violations
      await this.handleViolation(ip);
      
      return {
        allowed: false,
        reason: 'Rate limit exceeded',
        rateLimit: rateLimitResult,
      };
    }

    return {
      allowed: true,
      rateLimit: rateLimitResult,
    };
  }

  private async handleViolation(ip: string): Promise<void> {
    const violationKey = `ip:violations:${ip}`;
    
    const violations = await this.redis.incr(violationKey);
    await this.redis.expire(violationKey, 3600); // 1 hour window

    // Auto-blacklist after 5 violations
    if (violations >= 5) {
      await this.ipLimiter.addToBlacklist(ip, 3600); // 1 hour ban
      console.log(`IP ${ip} auto-blacklisted after ${violations} violations`);
    }
  }
}
```

### 7.2 Python IP Management

```python
import redis
import time
from typing import List, Optional, Dict
from dataclasses import dataclass

@dataclass
class IPRule:
    ip: str
    added_at: int
    expires_at: Optional[int] = None

class IPManagement:
    """
    IP whitelist/blacklist management with Redis
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.blacklist_prefix = "ip:blacklist:"
        self.whitelist_prefix = "ip:whitelist:"
    
    def add_to_blacklist(
        self, 
        ip: str, 
        duration_seconds: Optional[int] = None
    ) -> bool:
        """Add IP to blacklist"""
        key = f"{self.blacklist_prefix}{ip}"
        
        pipe = self.redis.pipeline()
        pipe.set(key, str(int(time.time())))
        if duration_seconds:
            pipe.expire(key, duration_seconds)
        results = pipe.execute()
        
        return results[0]
    
    def remove_from_blacklist(self, ip: str) -> bool:
        """Remove IP from blacklist"""
        key = f"{self.blacklist_prefix}{ip}"
        return self.redis.delete(key) > 0
    
    def is_blacklisted(self, ip: str) -> bool:
        """Check if IP is blacklisted"""
        key = f"{self.blacklist_prefix}{ip}"
        return self.redis.exists(key) > 0
    
    def add_to_whitelist(self, ip: str) -> bool:
        """Add IP to whitelist (no expiry)"""
        key = f"{self.whitelist_prefix}{ip}"
        return self.redis.set(key, '1')
    
    def remove_from_whitelist(self, ip: str) -> bool:
        """Remove IP from whitelist"""
        key = f"{self.whitelist_prefix}{ip}"
        return self.redis.delete(key) > 0
    
    def is_whitelisted(self, ip: str) -> bool:
        """Check if IP is whitelisted"""
        key = f"{self.whitelist_prefix}{ip}"
        return self.redis.exists(key) > 0
    
    def get_blacklist_stats(self) -> Dict:
        """Get blacklist statistics"""
        keys = list(self.redis.scan_iter(f"{self.blacklist_prefix}*", count=1000))
        
        count = len(keys)
        ips = [k.replace(self.blacklist_prefix, '') for k in keys[:10]]
        
        return {
            'total_blacklisted': count,
            'sample_ips': ips,
        }
    
    def clear_expired_blacklist(self) -> int:
        """Remove expired blacklist entries (not needed with TTL)"""
        # This is handled automatically by Redis TTL
        return 0


class SmartRateLimiter:
    """
    Rate limiter with IP whitelist/blacklist support
    """
    
    def __init__(
        self,
        redis_client: redis.Redis,
        max_requests: int = 100,
        window_seconds: int = 60
    ):
        self.redis = redis_client
        self.ip_manager = IPManagement(redis_client)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
    
    def check_request(self, ip: str, identifier: str) -> Dict:
        """
        Check request with whitelist/blacklist/rate limiting
        """
        result = {
            'allowed': True,
            'whitelisted': False,
            'blacklisted': False,
            'rate_limited': False,
            'remaining': self.max_requests,
        }
        
        # 1. Check whitelist
        if self.ip_manager.is_whitelisted(ip):
            result['whitelisted'] = True
            return result
        
        # 2. Check blacklist
        if self.ip_manager.is_blacklisted(ip):
            result['allowed'] = False
            result['blacklisted'] = True
            return result
        
        # 3. Check rate limit
        key = f"ratelimit:{identifier}"
        now = int(time.time() * 1000)
        window_start = now - (self.window_seconds * 1000)
        
        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, window_start)
        pipe.zcard(key)
        pipe.execute()
        
        # Count again after cleanup
        current = self.redis.zcard(key)
        
        if current >= self.max_requests:
            result['allowed'] = False
            result['rate_limited'] = True
            result['remaining'] = 0
            return result
        
        # Add new request
        pipe = self.redis.pipeline()
        pipe.zadd(key, now, f"{now}:{id(ip)}")
        pipe.expire(key, self.window_seconds)
        pipe.execute()
        
        result['remaining'] = self.max_requests - current - 1
        return result
    
    def record_violation(self, ip: str) -> int:
        """Record a rate limit violation"""
        key = f"violations:{ip}"
        violations = self.redis.incr(key)
        self.redis.expire(key, 3600)  # 1 hour window
        
        # Auto-blacklist after 5 violations
        if violations >= 5:
            self.ip_manager.add_to_blacklist(ip, duration_seconds=3600)
            return -1  # Indicates IP was blacklisted
        
        return violations
```

## 8. Distributed Rate Limiting

### 8.1 Cluster-aware Rate Limiter

```typescript
import Redis from 'ioredis';

class DistributedRateLimiter {
  private clusters: Redis[];
  private algorithm: 'sliding' | 'fixed' | 'tokenbucket';
  private maxRequests: number;
  private windowSeconds: number;

  constructor(
    clusterNodes: Array<{ host: string; port: number }>,
    options: {
      algorithm: 'sliding' | 'fixed' | 'tokenbucket';
      maxRequests: number;
      windowSeconds: number;
    }
  ) {
    this.clusters = clusterNodes.map(
      (node) =>
        new Redis({
          host: node.host,
          port: node.port,
        })
    );
    this.algorithm = options.algorithm;
    this.maxRequests = options.maxRequests;
    this.windowSeconds = options.windowSeconds;
  }

  private getNode(identifier: string): Redis {
    // Consistent hashing to select node
    const hash = this.hashString(identifier);
    const nodeIndex = hash % this.clusters.length;
    return this.clusters[nodeIndex];
  }

  private hashString(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = (hash << 5) - hash + str.charCodeAt(i);
      hash |= 0;
    }
    return Math.abs(hash);
  }

  async checkLimit(identifier: string): Promise<RateLimitResult> {
    const redis = this.getNode(identifier);
    
    if (this.algorithm === 'sliding') {
      return this.slidingWindowCheck(redis, identifier);
    } else if (this.algorithm === 'tokenbucket') {
      return this.tokenBucketCheck(redis, identifier);
    } else {
      return this.fixedWindowCheck(redis, identifier);
    }
  }

  private async slidingWindowCheck(
    redis: Redis,
    identifier: string
  ): Promise<RateLimitResult> {
    const key = `rl:sliding:${identifier}`;
    const now = Date.now();
    const windowMs = this.windowSeconds * 1000;
    const windowStart = now - windowMs;

    const script = `
      local key = KEYS[1]
      local now = tonumber(ARGV[1])
      local window_start = tonumber(ARGV[2])
      local max = tonumber(ARGV[3])
      
      redis.call('ZREMRANGEBYSCORE', key, 0, window_start)
      local count = redis.call('ZCARD', key)
      
      if count >= max then
        return {0, count, now + windowMs}
      end
      
      redis.call('ZADD', key, now, now)
      redis.call('PEXPIRE', key, ${windowMs})
      
      return {1, count + 1, now + windowMs}
    `;

    const result = await redis.eval(
      script,
      1,
      key,
      now,
      windowStart,
      this.maxRequests
    ) as [number, number, number];

    return {
      allowed: result[0] === 1,
      remaining: Math.max(0, this.maxRequests - result[1]),
      limit: this.maxRequests,
      resetAt: result[2],
      resetIn: this.windowSeconds,
    };
  }

  private async tokenBucketCheck(
    redis: Redis,
    identifier: string
  ): Promise<RateLimitResult> {
    const key = `rl:tokenbucket:${identifier}`;
    // Implementation similar to single-node version
    // Using the selected redis node
    return this.slidingWindowCheck(redis, identifier); // Simplified
  }

  private async fixedWindowCheck(
    redis: Redis,
    identifier: string
  ): Promise<RateLimitResult> {
    const key = `rl:fixed:${identifier}:${Math.floor(Date.now() / (this.windowSeconds * 1000))}`;
    const now = Date.now();

    const count = await redis.incr(key);
    await redis.expire(key, this.windowSeconds + 60);

    return {
      allowed: count <= this.maxRequests,
      remaining: Math.max(0, this.maxRequests - count),
      limit: this.maxRequests,
      resetAt: Math.floor(now / (this.windowSeconds * 1000)) * (this.windowSeconds * 1000) + this.windowSeconds * 1000,
      resetIn: this.windowSeconds,
    };
  }

  async close(): Promise<void> {
    await Promise.all(this.clusters.map((r) => r.quit()));
  }
}
```

## 9. Best Practices

### 9.1 Configuration Guidelines

```typescript
// Recommended rate limit configurations
const RATE_LIMIT_CONFIGS = {
  // API endpoints
  'api:public': {
    algorithm: 'sliding',
    maxRequests: 100,
    windowSeconds: 60,
    description: 'Public API - moderate rate limit',
  },
  'api:authenticated': {
    algorithm: 'sliding',
    maxRequests: 1000,
    windowSeconds: 60,
    description: 'Authenticated users - higher limit',
  },
  'api:premium': {
    algorithm: 'tokenbucket',
    bucketCapacity: 500,
    refillRate: 50,
    description: 'Premium users - allows bursts',
  },
  'api:write': {
    algorithm: 'sliding',
    maxRequests: 10,
    windowSeconds: 60,
    description: 'Write operations - strict limit',
  },
  'auth:login': {
    algorithm: 'fixed',
    maxRequests: 5,
    windowSeconds: 300,
    description: 'Login attempts - prevent brute force',
  },
  'upload:files': {
    algorithm: 'fixed',
    maxRequests: 10,
    windowSeconds: 3600,
    description: 'File uploads - hourly limit',
  },
};
```

### 9.2 Error Handling

```typescript
class RateLimiterError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number,
    public readonly tier?: string
  ) {
    super(message);
    this.name = 'RateLimiterError';
  }
}

async function safeRateLimitCheck(
  limiter: SlidingWindowRateLimiter,
  identifier: string,
  fallback: () => Promise<RateLimitResult>
): Promise<RateLimitResult> {
  try {
    return await limiter.checkLimit(identifier);
  } catch (error) {
    console.error('Rate limiter error, allowing request:', error);
    // Fallback: Allow request but log for monitoring
    return fallback();
  }
}

function createRateLimitError(result: RateLimitResult): RateLimiterError {
  return new RateLimiterError(
    `Rate limit exceeded. Retry in ${result.resetIn} seconds.`,
    429,
    'rate_limit'
  );
}
```

### 9.3 Monitoring và Alerts

```typescript
interface RateLimitMetrics {
  totalRequests: number;
  allowedRequests: number;
  blockedRequests: number;
  blockedByTier: Record<string, number>;
}

class RateLimitMonitor {
  private redis: Redis;

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async recordRequest(
    identifier: string,
    allowed: boolean,
    tier?: string
  ): Promise<void> {
    const now = Date.now();
    const hourKey = `metrics:ratelimit:${Math.floor(now / 3600000)}`;

    const pipeline = this.redis.pipeline();

    pipeline.incr(`${hourKey}:total`);
    if (allowed) {
      pipeline.incr(`${hourKey}:allowed`);
    } else {
      pipeline.incr(`${hourKey}:blocked`);
      if (tier) {
        pipeline.hincrby(`${hourKey}:by_tier`, tier, 1);
      }
    }

    await pipeline.exec();
  }

  async getMetrics(hours = 24): Promise<RateLimitMetrics> {
    const metrics: RateLimitMetrics = {
      totalRequests: 0,
      allowedRequests: 0,
      blockedRequests: 0,
      blockedByTier: {},
    };

    const now = Date.now();
    const pipeline = this.redis.pipeline();

    for (let i = 0; i < hours; i++) {
      const hourKey = `metrics:ratelimit:${Math.floor(now / 3600000) - i}`;
      pipeline.get(`${hourKey}:total`);
      pipeline.get(`${hourKey}:allowed`);
      pipeline.get(`${hourKey}:blocked`);
      pipeline.hgetall(`${hourKey}:by_tier`);
    }

    const results = await pipeline.exec();

    for (let i = 0; i < hours; i++) {
      const baseIndex = i * 4;
      const total = parseInt(results[baseIndex]?.[1] as string || '0');
      const allowed = parseInt(results[baseIndex + 1]?.[1] as string || '0');
      const blocked = parseInt(results[baseIndex + 2]?.[1] as string || '0');
      const byTier = results[baseIndex + 3]?.[1] as Record<string, string> || {};

      metrics.totalRequests += total;
      metrics.allowedRequests += allowed;
      metrics.blockedRequests += blocked;

      for (const [tier, count] of Object.entries(byTier)) {
        metrics.blockedByTier[tier] = (metrics.blockedByTier[tier] || 0) + parseInt(count);
      }
    }

    return metrics;
  }
}
```

## 10. Express.js Middleware Example

```typescript
import { Request, Response, NextFunction } from 'express';
import Redis from 'ioredis';

interface RateLimitConfig {
  algorithm: 'sliding' | 'fixed' | 'tokenbucket';
  maxRequests: number;
  windowSeconds: number;
  keyGenerator?: (req: Request) => string;
  skipSuccessfulRequests?: boolean;
  skipFailedRequests?: boolean;
}

function createRateLimitMiddleware(
  redis: Redis,
  config: RateLimitConfig
) {
  const {
    algorithm,
    maxRequests,
    windowSeconds,
    keyGenerator = (req) => req.ip || 'unknown',
    skipSuccessfulRequests = false,
    skipFailedRequests = false,
  } = config;

  let limiter: SlidingWindowRateLimiter | FixedWindowRateLimiter;

  if (algorithm === 'fixed') {
    limiter = new FixedWindowRateLimiter(redis, {
      windowSeconds,
      maxRequests,
    });
  } else {
    limiter = new SlidingWindowRateLimiter(redis, {
      windowSeconds,
      maxRequests,
    });
  }

  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const identifier = keyGenerator(req);
      const result = await limiter.checkLimit(identifier);

      // Set rate limit headers
      res.set({
        'X-RateLimit-Limit': result.limit.toString(),
        'X-RateLimit-Remaining': result.remaining.toString(),
        'X-RateLimit-Reset': Math.floor(result.resetAt / 1000).toString(),
      });

      if (!result.allowed) {
        res.status(429).json({
          error: 'Too Many Requests',
          message: `Rate limit exceeded. Please retry in ${result.resetIn} seconds.`,
          retryAfter: result.resetIn,
        });
        return;
      }

      // Hooks for logging
      res.on('finish', () => {
        const shouldSkip = 
          (skipSuccessfulRequests && res.statusCode < 400) ||
          (skipFailedRequests && res.statusCode >= 400);
        
        if (!shouldSkip) {
          // Record for metrics
          console.log(`Rate limit check: ${identifier} - ${result.remaining} remaining`);
        }
      });

      next();
    } catch (error) {
      console.error('Rate limiter error:', error);
      // Fail open - allow request if rate limiter fails
      next();
    }
  };
}

// Usage in Express
const app = express();

// Apply rate limiting to all routes
app.use(createRateLimitMiddleware(redis, {
  algorithm: 'sliding',
  maxRequests: 100,
  windowSeconds: 60,
}));

// Apply stricter rate limiting to auth routes
app.post('/login', createRateLimitMiddleware(redis, {
  algorithm: 'fixed',
  maxRequests: 5,
  windowSeconds: 300,
  keyGenerator: (req) => req.ip + ':login',
}));

// Apply to specific route
app.use('/api/secure', createRateLimitMiddleware(redis, {
  algorithm: 'sliding',
  maxRequests: 50,
  windowSeconds: 60,
  keyGenerator: (req) => (req.user as any)?.id || req.ip,
}));
```

## 11. References

- [Redis Rate Limiting Patterns](https://redis.io/docs/manual/redis-clients/)
- [Rate Limiting Algorithms](https://en.wikipedia.org/wiki/Rate_limiting)
- [Token Bucket Algorithm](https://en.wikipedia.org/wiki/Token_bucket)
- [Sliding Window Log Algorithm](https://aws.amazon.com/blogs/architecture/token-bucket-and-leaky-bucket-algorithms/)
- [Redis Lua Scripting](https://redis.io/docs/manual/programmability/intro-to-redis-scripting/)
- [Express Rate Limit](https://github.com/express-rate-limit/express-rate-limit)
