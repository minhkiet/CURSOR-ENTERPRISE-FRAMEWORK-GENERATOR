---
title: "Redis Caching Patterns"
description: "Hướng dẫn toàn diện về các patterns caching với Redis bao gồm cache-aside, write-through, write-behind, distributed locking và cache stampede prevention trong enterprise applications"
tags: ["redis", "caching", "cache-aside", "write-through", "write-behind", "redlock", "distributed-lock", "cache-stampede"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Redis Caching Patterns

## 1. Tổng Quan (Overview)

Trong các hệ thống enterprise, Redis được sử dụng chủ yếu như một caching layer để giảm tải cho database và cải thiện đáng kể performance của ứng dụng. Việc implement caching đúng cách là yếu tố then chốt quyết định sự thành công của hệ thống. Bài viết này sẽ đi sâu vào các caching patterns phổ biến, từ những pattern cơ bản đến những kỹ thuật nâng cao phù hợp cho môi trường production.

Caching không chỉ đơn giản là lưu trữ dữ liệu tạm thời. Trong thực tế enterprise, chúng ta cần xem xét nhiều yếu tố như data consistency (tính nhất quán dữ liệu), cache invalidation (xóa cache hợp lý), fault tolerance (khả năng chịu lỗi), và horizontal scalability (mở rộng ngang). Mỗi pattern có ưu nhược điểm riêng và phù hợp với các use case khác nhau.

Redis cung cấp nhiều features hỗ trợ caching như TTL (Time-To-Live), eviction policies, pub/sub cho cache invalidation messages, và Lua scripting cho các operations phức tạp. Hiểu rõ cách kết hợp các features này sẽ giúp bạn xây dựng caching layer hiệu quả và đáng tin cậy.

## 2. Mục Đích (Purpose)

Mục tiêu chính của caching layer trong hệ thống enterprise bao gồm:

**Performance Optimization**: Giảm latency từ hàng trăm milliseconds (database query) xuống còn microseconds (cache hit). Điều này đặc biệt quan trọng với các ứng dụng real-time và high-traffic như e-commerce, gaming, hay financial services.

**Database Load Reduction**: Giảm số lượng queries đến database chính, từ đó giảm CPU usage, I/O operations, và connection pool pressure. Một cache hit rate 95% có thể giảm database load đến 20 lần.

**Cost Efficiency**: Database engines enterprise-grade (PostgreSQL, MySQL, MongoDB) có chi phí licensing và operation cao. Việc sử dụng cache hiệu quả giúp giảm đáng kể chi phí infrastructure.

**Availability Improvement**: Trong trường hợp database có vấn đề, cache có thể serve read requests, giúp hệ thống vẫn hoạt động ở chế độ degraded.

## 3. Các Khái Niệm Quan Trọng (Key Concepts)

### 3.1 Cache Hit vs Cache Miss

```typescript
interface CacheMetrics {
  hits: number;
  misses: number;
  hitRate: number;
  latencyMs: number;
}

function calculateHitRate(metrics: CacheMetrics): number {
  const total = metrics.hits + metrics.misses;
  return total > 0 ? (metrics.hits / total) * 100 : 0;
}

// Cache hit - dữ liệu có sẵn trong cache
// Cache miss - cần fetch từ database và populate cache
```

### 3.2 TTL (Time-To-Live)

TTL là thời gian tồn tại của một key trong cache trước khi tự động bị xóa. Việc set TTL phù hợp là cân bằng giữa data freshness và cache efficiency.

```redis
# Set TTL 5 phút cho user session
SET user:session:12345 "session_data" EX 300

# Set TTL 1 giờ cho product catalog
SET product:cache:SKU001 "product_data" EX 3600

# Set TTL 24 giờ cho configuration
SET app:config:feature_flags "flags_data" EX 86400

# Kiểm tra TTL còn lại
TTL user:session:12345
```

### 3.3 Eviction Policies

Khi Redis memory đầy, nó sẽ trigger eviction policy để freeing space.

```redis
# Cấu hình eviction policy trong redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru

# Các eviction policies phổ biến:
# - noeviction: Không xóa any key (default)
# - allkeys-lru: Xóa least recently used keys
# - allkeys-random: Xóa random keys
# - volatile-lru: Xóa LRU keys trong keys có TTL
# - volatile-ttl: Xóa keys có TTL ngắn nhất
# - volatile-random: Xóa random keys có TTL
# - allkeys-lfu: Xóa least frequently used keys
# - volatile-lfu: Xóa LFU keys có TTL
```

### 3.4 Cache Invalidation Strategies

```typescript
// Invalidation on write - xóa cache khi data thay đổi
async function updateUser(userId: string, data: UserData): Promise<void> {
  await db.updateUser(userId, data);
  await redis.del(`user:${userId}`); // Invalidate cache
}

// Invalidation on delete
async function deleteUser(userId: string): Promise<void> {
  await db.deleteUser(userId);
  await redis.del(`user:${userId}`);
}

// Pattern: Delete而非Update - luôn xóa cache thay vì update
// Lý do: Tránh race condition giữa update và read
```

## 4. Cache-Aside Pattern (Read-Through Cache)

### 4.1 Giới Thiệu

Cache-aside là pattern phổ biến nhất và đơn giản nhất. Application code kiểm soát hoàn toàn việc đọc và ghi cache. Khi cần data, trước tiên check cache, nếu miss thì fetch từ database và populate cache.

### 4.2 Flow Diagram

```
┌─────────┐    1. GET    ┌─────────┐    2. MISS    ┌─────────┐
│   App   │ ──────────>  │  Redis  │ ───────────> │   DB    │
│         │              │  Cache  │              │         │
│         │ <──────────  │          │ <──────────  │         │
└─────────┘   4. Return  └─────────┘   3. Fetch   └─────────┘
              (no data)
```

### 4.3 Implementation

```typescript
// TypeScript implementation cho cache-aside pattern
import Redis from 'ioredis';

interface CachedUser {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}

class UserService {
  private redis: Redis;
  private readonly CACHE_TTL = 3600; // 1 hour
  private readonly CACHE_PREFIX = 'user:';

  constructor(redisClient: Redis) {
    this.redis = redisClient;
  }

  async getUserById(userId: string): Promise<CachedUser | null> {
    const cacheKey = `${this.CACHE_PREFIX}${userId}`;

    // Bước 1: Check cache
    const cached = await this.redis.get(cacheKey);
    
    if (cached) {
      console.log(`Cache HIT for user:${userId}`);
      return JSON.parse(cached) as CachedUser;
    }

    // Bước 2: Cache miss - fetch từ database
    console.log(`Cache MISS for user:${userId}`);
    const user = await this.fetchUserFromDatabase(userId);

    if (user) {
      // Bước 3: Populate cache với TTL
      await this.redis.setex(
        cacheKey,
        this.CACHE_TTL,
        JSON.stringify(user)
      );
    }

    return user;
  }

  async updateUser(userId: string, data: Partial<CachedUser>): Promise<void> {
    // Update database trước
    await this.saveUserToDatabase(userId, data);
    
    // Invalidate cache
    const cacheKey = `${this.CACHE_PREFIX}${userId}`;
    await this.redis.del(cacheKey);
    
    console.log(`Cache invalidated for user:${userId}`);
  }

  private async fetchUserFromDatabase(userId: string): Promise<CachedUser | null> {
    // Giả lập database query
    return {
      id: userId,
      email: `user${userId}@example.com`,
      name: `User ${userId}`,
      createdAt: new Date(),
    };
  }

  private async saveUserToDatabase(
    userId: string, 
    data: Partial<CachedUser>
  ): Promise<void> {
    // Giả lập database write
    console.log(`Saving user ${userId} to database`);
  }
}

// Sử dụng
const redis = new Redis({ host: '10.112.2.4', port: 6379 });
const userService = new UserService(redis);
```

### 4.4 Python Implementation

```python
import json
import redis
from typing import Optional, Dict, Any
from datetime import datetime

class CacheAsidePattern:
    def __init__(self, redis_host: str, redis_port: int, ttl: int = 3600):
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        self.ttl = ttl

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Cache-Aside: Read pattern
        1. Check cache first
        2. If miss, fetch from DB and populate cache
        """
        cache_key = f"user:{user_id}"
        
        # Step 1: Try cache
        cached_data = self.redis_client.get(cache_key)
        
        if cached_data:
            print(f"Cache HIT for user:{user_id}")
            return json.loads(cached_data)
        
        # Step 2: Cache miss - fetch from DB
        print(f"Cache MISS for user:{user_id}")
        user_data = self._fetch_from_database(user_id)
        
        if user_data:
            # Step 3: Populate cache with TTL
            self.redis_client.setex(
                cache_key,
                self.ttl,
                json.dumps(user_data)
            )
        
        return user_data

    def update_user(self, user_id: str, data: Dict[str, Any]) -> None:
        """
        Write pattern: Update DB first, then invalidate cache
        """
        # Step 1: Update database
        self._save_to_database(user_id, data)
        
        # Step 2: Invalidate cache
        cache_key = f"user:{user_id}"
        self.redis_client.delete(cache_key)
        print(f"Cache invalidated for user:{user_id}")

    def delete_user(self, user_id: str) -> None:
        """Delete pattern: Delete from DB, then invalidate cache"""
        self._delete_from_database(user_id)
        cache_key = f"user:{user_id}"
        self.redis_client.delete(cache_key)

    def _fetch_from_database(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Simulate database fetch"""
        return {
            "id": user_id,
            "email": f"user{user_id}@example.com",
            "name": f"User {user_id}",
            "updated_at": datetime.now().isoformat()
        }

    def _save_to_database(self, user_id: str, data: Dict[str, Any]) -> None:
        """Simulate database save"""
        print(f"Saving user {user_id} to database: {data}")

    def _delete_from_database(self, user_id: str) -> None:
        """Simulate database delete"""
        print(f"Deleting user {user_id} from database")


# Usage example
if __name__ == "__main__":
    cache = CacheAsidePattern("localhost", 6379, ttl=3600)
    
    # First call - cache miss
    user = cache.get_user("123")
    print(f"User: {user}")
    
    # Second call - cache hit
    user = cache.get_user("123")
    print(f"User: {user}")
    
    # Update user - invalidates cache
    cache.update_user("123", {"name": "Updated Name"})
    
    # Next read will be cache miss again
    user = cache.get_user("123")
```

## 5. Write-Through Pattern

### 5.1 Giới Thiệu

Write-through đảm bảo data trong cache luôn đồng nhất với database. Mỗi khi ghi data, cả cache và database đều được update đồng thời.

### 5.2 Flow Diagram

```
┌─────────┐    1. WRITE    ┌─────────┐    2. WRITE    ┌─────────┐
│   App   │ ────────────>  │  Redis  │ ────────────> │   DB    │
│         │ <────────────  │  Cache  │ <────────────  │         │
└─────────┘   4. Return    └─────────┘   3. Confirm   └─────────┘
              (success)
```

### 5.3 Implementation

```typescript
interface WriteThroughCache<T> {
  get(key: string): Promise<T | null>;
  set(key: string, value: T): Promise<void>;
  delete(key: string): Promise<void>;
}

class WriteThroughUserCache implements WriteThroughCache<CachedUser> {
  private redis: Redis;
  private db: DatabaseConnection;
  private ttl: number;

  constructor(redis: Redis, db: DatabaseConnection, ttl: number = 3600) {
    this.redis = redis;
    this.db = db;
    this.ttl = ttl;
  }

  async get(key: string): Promise<CachedUser | null> {
    // Always try cache first
    const cached = await this.redis.get(key);
    if (cached) {
      return JSON.parse(cached);
    }

    // Fallback to database
    const user = await this.db.findUserById(key);
    if (user) {
      // Populate cache
      await this.redis.setex(key, this.ttl, JSON.stringify(user));
    }
    return user;
  }

  async set(key: string, value: CachedUser): Promise<void> {
    // Write to cache first
    await this.redis.setex(key, this.ttl, JSON.stringify(value));
    
    // Then write to database (atomic operation)
    await this.db.upsertUser(value);
  }

  async delete(key: string): Promise<void> {
    // Delete from both cache and database
    await this.redis.del(key);
    await this.db.deleteUserById(key);
  }
}
```

### 5.4 Python Implementation

```python
from typing import TypeVar, Generic, Optional
import redis
import json
from contextlib import asynccontextmanager

T = TypeVar('T')

class WriteThroughCache(Generic[T]):
    """
    Write-Through Cache Pattern
    - Writes go to both cache and database synchronously
    - Guarantees strong consistency
    - Higher write latency but ensures no stale data
    """
    
    def __init__(self, redis_client: redis.Redis, ttl: int = 3600):
        self.redis = redis_client
        self.ttl = ttl

    def get(self, key: str) -> Optional[T]:
        """Read from cache first, fallback to source"""
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        return None

    def set(self, key: str, value: T) -> None:
        """
        Write-Through: Write to both cache and database
        This ensures cache is always up-to-date with source
        """
        # Serialize value
        serialized = json.dumps(value)
        
        # Write to cache with TTL
        self.redis.setex(key, self.ttl, serialized)
        
        # Write to database (implement in subclass)
        self._write_to_source(key, value)

    def delete(self, key: str) -> None:
        """Delete from both cache and database"""
        self.redis.delete(key)
        self._delete_from_source(key)

    def _write_to_source(self, key: str, value: T) -> None:
        """Override this method to implement actual source write"""
        raise NotImplementedError

    def _delete_from_source(self, key: str) -> None:
        """Override this method to implement actual source delete"""
        raise NotImplementedError


class WriteThroughUserCache(WriteThroughCache[dict]):
    """User cache with write-through pattern"""

    def __init__(self, redis_client: redis.Redis, db_pool, ttl: int = 3600):
        super().__init__(redis_client, ttl)
        self.db_pool = db_pool

    def _write_to_source(self, key: str, value: dict) -> None:
        """Write user to database"""
        with self.db_pool.connection() as conn:
            conn.execute("""
                INSERT INTO users (id, email, name, updated_at)
                VALUES (%s, %s, %s, NOW())
                ON CONFLICT (id) DO UPDATE
                SET email = EXCLUDED.email,
                    name = EXCLUDED.name,
                    updated_at = NOW()
            """, (key, value.get('email'), value.get('name')))

    def _delete_from_source(self, key: str) -> None:
        """Delete user from database"""
        with self.db_pool.connection() as conn:
            conn.execute("DELETE FROM users WHERE id = %s", (key,))
```

## 6. Write-Behind Pattern (Write-Around)

### 6.1 Giới Thiệu

Write-behind ghi data vào cache trước và đợi một khoảng thời gian hoặc điều kiện nhất định trước khi đồng bộ xuống database. Pattern này cải thiện write performance nhưng có risk về data loss nếu cache fail trước khi persist.

### 6.2 Flow Diagram

```
┌─────────┐    1. WRITE    ┌─────────┐              ┌─────────┐
│   App   │ ────────────>  │  Redis  │   (async)    │   DB    │
│         │ <────────────  │  Cache  │ ──────────>  │         │
└─────────┘   2. Return    └─────────┘   3. Later    └─────────┘
              (immediate)      │                         ▲
                              │      4. Batch/Sync       │
                              └───────────────────────────┘
```

### 6.3 Implementation

```typescript
interface WriteBehindOptions {
  flushInterval: number; // ms
  maxBatchSize: number;
  retryAttempts: number;
}

class WriteBehindCache<T> {
  private redis: Redis;
  private pendingWrites: Map<string, T> = new Map();
  private flushInterval: NodeJS.Timeout;
  
  constructor(
    private readonly redis: Redis,
    private readonly sourceWriter: SourceWriter<T>,
    options: WriteBehindOptions
  ) {
    this.flushInterval = setInterval(
      () => this.flush(),
      options.flushInterval
    );
  }

  async set(key: string, value: T): Promise<void> {
    // Write to cache immediately
    await this.redis.setex(key, this.getTTL(), JSON.stringify(value));
    
    // Queue for async database write
    this.pendingWrites.set(key, value);
  }

  async flush(): Promise<void> {
    if (this.pendingWrites.size === 0) return;

    const writes = new Map(this.pendingWrites);
    this.pendingWrites.clear();

    try {
      // Batch write to database
      await this.sourceWriter.batchWrite(Array.from(writes.entries()));
      console.log(`Flushed ${writes.size} writes to database`);
    } catch (error) {
      // Re-queue failed writes
      console.error('Flush failed, re-queuing:', error);
      writes.forEach((value, key) => {
        this.pendingWrites.set(key, value);
      });
    }
  }

  private getTTL(): number {
    return 86400; // 24 hours
  }

  async shutdown(): Promise<void> {
    clearInterval(this.flushInterval);
    await this.flush(); // Final flush
  }
}

interface SourceWriter<T> {
  batchWrite(entries: [string, T][]): Promise<void>;
}
```

## 7. Cache Stampede Prevention

### 7.1 Vấn Đề

Cache stampede (hay còn gọi là thundering herd) xảy ra khi cache expires đồng thời cho nhiều requests, dẫn đến hàng loạt requests đổ vào database cùng lúc.

### 7.2 Giải Pháp 1: Probabilistic Early Expiration

```typescript
class ProbabilisticEarlyExpiration {
  private redis: Redis;
  private beta: number = 1.0; // Tuning factor

  async getWithProbabilisticRefresh(
    key: string, 
    fetchFn: () => Promise<any>
  ): Promise<any> {
    // Lấy giá trị và TTL hiện tại
    const [value, ttl] = await Promise.all([
      this.redis.get(key),
      this.redis.ttl(key)
    ]);

    if (value && ttl > 0) {
      // Tính probability của việc refresh sớm
      const refreshProbability = this.calculateRefreshProbability(ttl);
      
      if (Math.random() < refreshProbability) {
        // Refresh asynchronously
        this.refreshAsync(key, fetchFn);
        return JSON.parse(value);
      }
      return JSON.parse(value);
    }

    // Cache miss hoặc expired - fetch synchronously
    const freshValue = await fetchFn();
    await this.redis.setex(key, 3600, JSON.stringify(freshValue));
    return freshValue;
  }

  private calculateRefreshProbability(ttl: number): number {
    const standardDeviation = this.beta * Math.sqrt(ttl);
    return Math.exp(-ttl / standardDeviation);
  }

  private refreshAsync(key: string, fetchFn: () => Promise<any>): void {
    fetchFn()
      .then(value => this.redis.setex(key, 3600, JSON.stringify(value)))
      .catch(err => console.error('Background refresh failed:', err));
  }
}
```

### 7.3 Giải Pháp 2: Distributed Locking

```typescript
class CacheStampedeProtection {
  private redis: Redis;
  private readonly LOCK_TTL = 10; // seconds
  private readonly LOCK_KEY_PREFIX = 'lock:';

  async getWithLock(
    key: string,
    fetchFn: () => Promise<any>,
    ttl: number = 3600
  ): Promise<any> {
    // Thử lấy từ cache trước
    const cached = await this.redis.get(key);
    if (cached) {
      return JSON.parse(cached);
    }

    // Cache miss - thử acquire lock
    const lockKey = `${this.LOCK_KEY_PREFIX}${key}`;
    const lockAcquired = await this.acquireLock(lockKey);

    if (lockAcquired) {
      try {
        // Double-check cache sau khi acquire lock
        const doubleCheck = await this.redis.get(key);
        if (doubleCheck) {
          return JSON.parse(doubleCheck);
        }

        // Fetch và cache
        const value = await fetchFn();
        await this.redis.setex(key, ttl, JSON.stringify(value));
        return value;
      } finally {
        await this.releaseLock(lockKey);
      }
    } else {
      // Không acquire được lock - đợi và retry cache
      await this.delay(100);
      return this.getWithLock(key, fetchFn, ttl);
    }
  }

  private async acquireLock(lockKey: string): Promise<boolean> {
    const result = await this.redis.set(
      lockKey, 
      '1', 
      'EX', 
      this.LOCK_TTL, 
      'NX' // Only set if not exists
    );
    return result === 'OK';
  }

  private async releaseLock(lockKey: string): Promise<void> {
    await this.redis.del(lockKey);
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

### 7.4 Giải Pháp 3: Lua Script cho Atomic Operations

```lua
-- cache_stampede_prevention.lua
-- Prevents cache stampede using probabilistic early refresh

local key = KEYS[1]
local lock_key = KEYS[2]
local ttl = tonumber(ARGV[1])
local beta = tonumber(ARGV[2]) or 1.0

-- Get current value and TTL
local value = redis.call('GET', key)
local current_ttl = redis.call('TTL', key)

if value then
    -- Calculate refresh probability using negative exponential
    -- P(refresh) = exp(-ttl / (beta * sqrt(ttl)))
    if current_ttl > 0 then
        local stddev = beta * math.sqrt(current_ttl)
        local prob = math.exp(-current_ttl / stddev)
        
        -- Use local random (not available in Redis, using deterministic check)
        -- In production, use probabilistic based on key name
        local should_refresh = 0
        
        -- For demo: refresh if TTL < 10% of original
        if current_ttl < (ttl * 0.1) then
            should_refresh = 1
        end
        
        if should_refresh == 1 then
            -- Try to acquire lock for refresh
            local lock_acquired = redis.call('SET', lock_key, '1', 'NX', 'EX', 10)
            if lock_acquired then
                return {value, 1} -- Return value with refresh flag
            end
        end
        
        return {value, 0} -- Return value without refresh flag
    end
end

-- Cache miss
local lock_acquired = redis.call('SET', lock_key, '1', 'NX', 'EX', 10)
if lock_acquired then
    return {nil, 1} -- Signal to fetch and cache
end

-- Another process is fetching, wait and retry
return {nil, 0}
```

## 8. Distributed Locking với Redlock

### 8.1 Giới Thiệu về Redlock

Redlock là algorithm được recommend bởi Salvatore Sanfilippo (tác giả Redis) để implement distributed lock một cách an toàn trong môi trường distributed system.

### 8.2 Redlock Algorithm

```
1. Get current time in milliseconds
2. Try to acquire lock on N Redis instances sequentially
   - Use SET with NX and PX (expiration) options
   - Use a unique value (UUID) as lock token
3. Calculate elapsed time for acquiring lock
4. If lock acquired on majority of instances (N/2 + 1)
   and elapsed time < lock timeout, lock is valid
5. If lock acquired but not majority, release all locks
6. If lock not acquired, retry after random delay
```

### 8.3 Implementation

```typescript
import Redis from 'ioredis';
import { v4 as uuidv4 } from 'uuid';

interface RedlockOptions {
  driftFactor: number; // Thời gian drift cho phép
  retryCount: number;
  retryDelay: number;
  retryJitter: number;
}

class Redlock {
  private redisClients: Redis[];
  private options: RedlockOptions;

  constructor(redisClients: Redis[], options: Partial<RedlockOptions> = {}) {
    this.redisClients = redisClients;
    this.options = {
      driftFactor: 0.01,
      retryCount: 3,
      retryDelay: 200,
      retryJitter: 200,
      ...options
    };
  }

  async lock(
    resource: string, 
    ttl: number
  ): Promise<{ value: string; validUntil: number } | null> {
    const token = uuidv4();
    const drift = this.options.driftFactor * ttl + 2;
    
    for (let attempt = 0; attempt < this.options.retryCount; attempt++) {
      const startTime = Date.now();
      const results = await Promise.all(
        this.redisClients.map(client => 
          this.acquireOnInstance(client, resource, token, ttl)
        )
      );

      const successes = results.filter(r => r === true).length;
      const elapsed = Date.now() - startTime;
      const validityTime = ttl - elapsed - drift;

      if (successes >= Math.floor(this.redisClients.length / 2) + 1) {
        if (validityTime > 0) {
          return { value: token, validUntil: Date.now() + validityTime };
        }
      }

      // Release all locks if acquired
      await this.releaseAll(resource, token);
      
      // Wait with jitter before retry
      const jitter = Math.random() * this.options.retryJitter;
      await this.delay(this.options.retryDelay + jitter);
    }

    return null;
  }

  async unlock(
    resource: string, 
    lock: { value: string; validUntil: number }
  ): Promise<void> {
    // Verify lock is still valid
    if (lock.validUntil < Date.now()) {
      console.warn('Lock expired, cannot unlock');
      return;
    }

    await this.releaseAll(resource, lock.value);
  }

  private async acquireOnInstance(
    client: Redis, 
    resource: string, 
    token: string, 
    ttl: number
  ): Promise<boolean> {
    try {
      const result = await client.set(
        resource, 
        token, 
        'PX', 
        ttl, 
        'NX'
      );
      return result === 'OK';
    } catch (error) {
      console.error('Failed to acquire lock on instance:', error);
      return false;
    }
  }

  private async releaseAll(resource: string, token: string): Promise<void> {
    // Lua script để ensure chỉ release nếu token match
    const script = `
      if redis.call("GET", KEYS[1]) == ARGV[1] then
        return redis.call("DEL", KEYS[1])
      else
        return 0
      end
    `;

    await Promise.all(
      this.redisClients.map(client => 
        client.eval(script, 1, resource, token)
      )
    );
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Sử dụng
const redis1 = new Redis({ host: 'redis-1.example.com', port: 6379 });
const redis2 = new Redis({ host: 'redis-2.example.com', port: 6379 });
const redis3 = new Redis({ host: 'redis-3.example.com', port: 6379 });

const redlock = new Redlock([redis1, redis2, redis3]);

async function processPayment(orderId: string) {
  const lockKey = `lock:payment:${orderId}`;
  
  const lock = await redlock.lock(lockKey, 30000); // 30 seconds TTL
  if (!lock) {
    throw new Error('Could not acquire lock for payment processing');
  }

  try {
    // Process payment
    await doProcessPayment(orderId);
  } finally {
    await redlock.unlock(lockKey, lock);
  }
}
```

### 8.4 Python Redlock Implementation

```python
import redis
import time
import uuid
from typing import Optional, Tuple
from contextlib import contextmanager

class Redlock:
    """
    Redlock implementation for distributed locking
    """
    
    def __init__(self, redis_servers: list, retry_count: int = 3, 
                 retry_delay: float = 0.2, clock_drift_factor: float = 0.01):
        self.redis_clients = [redis.Redis.from_url(s) for s in redis_servers]
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.clock_drift_factor = clock_drift_factor
    
    def lock(self, resource: str, ttl_ms: int) -> Optional[dict]:
        """
        Acquire a distributed lock
        
        Args:
            resource: Lock resource name
            ttl_ms: Lock TTL in milliseconds
            
        Returns:
            Lock object if acquired, None otherwise
        """
        token = str(uuid.uuid4())
        drift = int((ttl_ms * self.clock_drift_factor) + 2)
        
        for attempt in range(self.retry_count):
            start_time = int((time.time() * 1000))
            acquired_count = 0
            
            # Try to acquire on all instances
            for client in self.redis_clients:
                if self._acquire_on_instance(client, resource, token, ttl_ms):
                    acquired_count += 1
            
            elapsed = int((time.time() * 1000)) - start_time
            validity_time = ttl_ms - elapsed - drift
            
            # Check if majority acquired and still valid
            if acquired_count >= (len(self.redis_clients) // 2) + 1:
                if validity_time > 0:
                    return {
                        'resource': resource,
                        'token': token,
                        'validity_ms': validity_time
                    }
            
            # Release any acquired locks
            self._release_all(resource, token)
            
            # Wait before retry
            time.sleep(self.retry_delay)
        
        return None
    
    def unlock(self, lock: dict) -> None:
        """
        Release a distributed lock
        """
        if lock['validity_ms'] > 0:
            self._release_all(lock['resource'], lock['token'])
    
    def _acquire_on_instance(self, client: redis.Redis, 
                            resource: str, token: str, 
                            ttl_ms: int) -> bool:
        """Try to acquire lock on single instance"""
        try:
            return client.set(
                resource,
                token,
                nx=True,  # Only set if not exists
                px=ttl_ms  # TTL in milliseconds
            ) is True
        except redis.RedisError:
            return False
    
    def _release_all(self, resource: str, token: str) -> None:
        """Release lock on all instances using Lua script"""
        release_script = """
        if redis.call("GET", KEYS[1]) == ARGV[1] then
            return redis.call("DEL", KEYS[1])
        else
            return 0
        end
        """
        
        for client in self.redis_clients:
            try:
                client.eval(release_script, 1, resource, token)
            except redis.RedisError:
                pass
    
    @contextmanager
    def locking(self, resource: str, ttl_ms: int = 30000):
        """
        Context manager for lock acquisition
        """
        lock = self.lock(resource, ttl_ms)
        if not lock:
            raise RuntimeError(f"Could not acquire lock for {resource}")
        
        try:
            yield lock
        finally:
            self.unlock(lock)


# Usage
if __name__ == "__main__":
    redlock = Redlock([
        "redis://redis-1:6379",
        "redis://redis-2:6379", 
        "redis://redis-3:6379"
    ])
    
    try:
        with redlock.locking("payment:order-123", 30000):
            print("Processing payment...")
            # Do payment processing
            print("Payment processed")
    except RuntimeError as e:
        print(f"Lock acquisition failed: {e}")
```

## 9. Best Practices

### 9.1 Cache Key Design

```typescript
// Good: Hierarchical, descriptive key naming
const GOOD_KEYS = [
  'user:12345:profile',
  'user:12345:sessions:active',
  'product:catalog:featured:2026',
  'order:processing:queue:pending',
  'cache:region:us-east:config',
];

// Bad: Flat, non-descriptive keys
const BAD_KEYS = [
  'u12345',
  'data1',
  'cache2',
  'tmp3',
];
```

### 9.2 TTL Strategy

```typescript
// TTL recommendations by data type
const TTL_STRATEGY = {
  // Real-time data: Short TTL
  userSessions: 900,        // 15 minutes
  onlineStatus: 60,          // 1 minute
  stockPrices: 5,           // 5 seconds
  
  // Near real-time: Medium TTL
  userProfiles: 3600,       // 1 hour
  productCatalog: 1800,     // 30 minutes
  categoryLists: 900,       // 15 minutes
  
  // Static/Reference data: Long TTL
  appConfig: 86400,         // 24 hours
  featureFlags: 3600,       // 1 hour
  geoipData: 604800,        // 1 week
  countryCodes: 2592000,    // 30 days
};
```

### 9.3 Memory Management

```redis
# redis.conf - Production memory settings

# Set maxmemory
maxmemory 4gb
maxmemory-policy allkeys-lru

# Enable memory efficient data structures
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64

# Active defragmentation
activedefrag yes
active-defrag-ignore-bytes 100mb
active-defrag-threshold-lower 10
active-defrag-threshold-upper 100
```

### 9.4 Monitoring

```typescript
async function getCacheMetrics(redis: Redis): Promise<CacheMetrics> {
  const info = await redis.info('memory');
  const keys = await redis.dbsize();
  
  // Parse memory info
  const memoryUsed = parseInt(info.match(/used_memory:(\d+)/)?.[1] || '0');
  const memoryPeak = parseInt(info.match(/used_memory_peak:(\d+)/)?.[1] || '0');
  
  return {
    keys,
    memoryUsedBytes: memoryUsed,
    memoryUsedMB: Math.round(memoryUsed / 1024 / 1024),
    memoryPeakMB: Math.round(memoryPeak / 1024 / 1024),
    hitRate: await calculateHitRate(redis),
  };
}

async function calculateHitRate(redis: Redis): Promise<number> {
  const info = await redis.info('stats');
  const hits = parseInt(info.match(/keyspace_hits:(\d+)/)?.[1] || '0');
  const misses = parseInt(info.match(/keyspace_misses:(\d+)/)?.[1] || '0');
  const total = hits + misses;
  return total > 0 ? Math.round((hits / total) * 100 * 100) / 100 : 0;
}
```

## 10. Common Patterns và Use Cases

### 10.1 Session Store

```typescript
class SessionStore {
  private redis: Redis;
  private readonly SESSION_TTL = 86400; // 24 hours

  async createSession(userId: string, data: SessionData): Promise<string> {
    const sessionId = `sess:${uuidv4()}`;
    const key = `session:${sessionId}`;
    
    await this.redis.setex(
      key,
      this.SESSION_TTL,
      JSON.stringify({ userId, ...data, createdAt: Date.now() })
    );
    
    // Add to user's session set
    await this.redis.sadd(`user:${userId}:sessions`, sessionId);
    
    return sessionId;
  }

  async getSession(sessionId: string): Promise<SessionData | null> {
    const data = await this.redis.get(`session:${sessionId}`);
    return data ? JSON.parse(data) : null;
  }

  async refreshSession(sessionId: string): Promise<void> {
    const key = `session:${sessionId}`;
    const ttl = await this.redis.ttl(key);
    if (ttl > 0) {
      await this.redis.expire(key, this.SESSION_TTL);
    }
  }

  async deleteSession(sessionId: string): Promise<void> {
    const data = await this.redis.get(`session:${sessionId}`);
    if (data) {
      const session = JSON.parse(data);
      await this.redis.del(`session:${sessionId}`);
      await this.redis.srem(`user:${session.userId}:sessions`, sessionId);
    }
  }
}
```

### 10.2 Rate Limiting

```typescript
class RateLimiter {
  private redis: Redis;
  private readonly WINDOW_SIZE = 60; // seconds
  private readonly MAX_REQUESTS = 100;

  async isAllowed(clientId: string): Promise<{ allowed: boolean; remaining: number }> {
    const key = `ratelimit:${clientId}`;
    const now = Math.floor(Date.now() / 1000);
    const windowStart = now - this.WINDOW_SIZE;

    const pipeline = this.redis.pipeline();
    
    // Remove old entries
    pipeline.zremrangebyscore(key, 0, windowStart);
    // Add current request
    pipeline.zadd(key, now, `${now}-${Math.random()}`);
    // Count requests in window
    pipeline.zcard(key);
    // Set TTL
    pipeline.expire(key, this.WINDOW_SIZE);

    const results = await pipeline.exec();
    const requestCount = results?.[2]?.[1] as number;

    return {
      allowed: requestCount <= this.MAX_REQUESTS,
      remaining: Math.max(0, this.MAX_REQUESTS - requestCount)
    };
  }
}
```

## 11. Troubleshooting

### 11.1 Common Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Cache bị evict quá nhiều | Memory used gần max, eviction count cao | Tăng maxmemory, điều chỉnh eviction policy |
| Cache stampede | Database CPU spike, latency spike khi cache miss | Implement lock hoặc probabilistic refresh |
| Stale data | Data không update sau khi source change | Kiểm tra invalidation logic, giảm TTL |
| Memory fragmentation | used_memory_rss > used_memory | Enable activedefrag, restart Redis |
| Connection exhaustion | "Too many open connections" errors | Tăng max clients, sử dụng connection pool |

### 11.2 Debug Commands

```redis
# Kiểm tra memory usage
INFO memory

# Kiểm tra eviction count
INFO stats | grep evicted

# Kiểm tra key count
DBSIZE

# Kiểm tra big keys
--bigkeys

# Kiểm tra memory của một key
DEBUG OBJECTF key_name

# Kiểm tra keys matching pattern
KEYS user:*
SCAN 0 MATCH user:* COUNT 100
```

## 12. References

- [Redis Documentation](https://redis.io/docs/)
- [Redis Caching Patterns - Martin Fowler](https://martinfowler.com/articles/patterns-of-distributed-systems/)
- [Redlock by Salvatore Sanfilippo](https://redis.io/docs/manual/patterns/distributed-locks/)
- [Cache Stampede Prevention - Google Paper](https://research.google.com/pubs/archive/45406.pdf)
- [Redis Best Practices - AWS](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/RedisBestPractices.html)
