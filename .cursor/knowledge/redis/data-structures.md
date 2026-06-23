---
title: "Redis Data Structures"
description: "Hướng dẫn toàn diện về tất cả Redis data structures bao gồm Strings, Lists, Sets, Sorted Sets, Hashes, Bitmaps, HyperLogLog và Geospatial indexes với use cases và performance considerations"
tags: ["redis", "data-structures", "strings", "lists", "sets", "sorted-sets", "hashes", "bitmaps", "hyperloglog", "geospatial", "geoadd", "georadius"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Redis Data Structures

## 1. Tổng Quan (Overview)

Redis không chỉ là một key-value store đơn giản. Nó cung cấp một tập hợp phong phú các data structures với performance cao và memory efficiency đáng kinh ngạc. Mỗi data structure có những use cases riêng và được tối ưu hóa cho các operations cụ thể.

Việc hiểu rõ về các data structures của Redis và cách sử dụng chúng đúng cách là yếu tố then chốt để xây dựng các ứng dụng hiệu quả. Trong bài viết này, chúng ta sẽ đi sâu vào từng loại data structure, từ những cái cơ bản nhất đến những cái chuyên biệt như HyperLogLog và Geospatial indexes.

## 2. Strings

### 2.1 Giới Thiệu

String là data structure cơ bản nhất trong Redis. Nó có thể chứa bất kỳ loại dữ liệu nào: plain text, JSON, serialized objects, numbers, binary data. Redis Strings có thể lưu trữ tối đa 512MB data.

### 2.2 Basic String Operations

```redis
# Basic operations
SET key "value"
GET key
DEL key

# With expiration
SET key "value" EX 3600      # Set with 1 hour TTL
SET key "value" PX 300000     # Set with 300 seconds in milliseconds
SETEX key 3600 "value"        # Set and expire in one command
SETNX key "value"             # Set if not exists (atomic)
SETXX key "value"             # Set only if exists

# Multiple values
MSET key1 "value1" key2 "value2" key3 "value3"
MGET key1 key2 key3
MSETNX key1 "value1" key2 "value2"  # MSETNX is atomic

# Partial updates
APPEND key "suffix"           # Append to existing value
SETRANGE key 0 "prefix"       # Replace from offset
GETRANGE key 0 -1             # Get substring
STRLEN key                    # Get string length

# Numeric operations
SET count 10
INCR count                    # Increment by 1 (returns new value)
INCRBY count 5                # Increment by 5
DECR count                    # Decrement by 1
DECRBY count 3                # Decrement by 3
INCRBYFLOAT count 2.5         # Increment by float
```

### 2.3 String Use Cases

```typescript
// 1. Simple caching
async function cacheGet<T>(key: string): Promise<T | null> {
  const value = await redis.get(`cache:${key}`);
  return value ? JSON.parse(value) : null;
}

async function cacheSet<T>(key: string, value: T, ttl = 3600): Promise<void> {
  await redis.setex(`cache:${key}`, ttl, JSON.stringify(value));
}

// 2. Counter and statistics
async function incrementCounter(counterName: string): Promise<number> {
  return redis.incr(`stats:${counterName}`);
}

async function getCounter(counterName: string): Promise<number> {
  const value = await redis.get(`stats:${counterName}`);
  return parseInt(value || '0');
}

// 3. Distributed locking
async function acquireLock(lockKey: string, ttl = 10000): Promise<boolean> {
  const result = await redis.set(lockKey, '1', 'PX', ttl, 'NX');
  return result === 'OK';
}

async function releaseLock(lockKey: string): Promise<void> {
  await redis.del(lockKey);
}

// 4. Session management
async function createSession(userId: string): Promise<string> {
  const sessionId = generateUUID();
  const sessionData = {
    userId,
    createdAt: Date.now(),
    lastActive: Date.now(),
  };
  await redis.setex(
    `session:${sessionId}`,
    86400, // 24 hours
    JSON.stringify(sessionData)
  );
  return sessionId;
}

// 5. Rate limiting
async function checkRateLimit(
  identifier: string,
  maxRequests: number,
  windowSeconds: number
): Promise<{ allowed: boolean; remaining: number }> {
  const key = `ratelimit:${identifier}:${Math.floor(Date.now() / (windowSeconds * 1000))}`;
  
  const current = await redis.incr(key);
  if (current === 1) {
    await redis.expire(key, windowSeconds);
  }
  
  return {
    allowed: current <= maxRequests,
    remaining: Math.max(0, maxRequests - current),
  };
}
```

### 2.4 TypeScript Implementation

```typescript
import Redis from 'ioredis';

class RedisStringOperations {
  private redis: Redis;

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async setObject<T>(
    key: string,
    value: T,
    ttlSeconds?: number
  ): Promise<void> {
    const serialized = JSON.stringify(value);
    if (ttlSeconds) {
      await this.redis.setex(key, ttlSeconds, serialized);
    } else {
      await this.redis.set(key, serialized);
    }
  }

  async getObject<T>(key: string): Promise<T | null> {
    const value = await this.redis.get(key);
    if (!value) return null;
    return JSON.parse(value) as T;
  }

  async setNX<T>(key: string, value: T, ttlSeconds?: number): Promise<boolean> {
    const serialized = JSON.stringify(value);
    const result = ttlSeconds
      ? await this.redis.set(key, serialized, 'EX', ttlSeconds, 'NX')
      : await this.redis.setnx(key, serialized);
    return result === 1 || result === 'OK';
  }

  async increment(key: string, amount = 1): Promise<number> {
    if (amount === 1) {
      return this.redis.incr(key);
    }
    return this.redis.incrby(key, amount);
  }

  async decrement(key: string, amount = 1): Promise<number> {
    if (amount === 1) {
      return this.redis.decr(key);
    }
    return this.redis.decrby(key, amount);
  }

  async batchSet(pairs: Record<string, any>): Promise<void> {
    const args: string[] = [];
    for (const [key, value] of Object.entries(pairs)) {
      args.push(key, typeof value === 'string' ? value : JSON.stringify(value));
    }
    await this.redis.mset(...args);
  }

  async batchGet(keys: string[]): Promise<(string | null)[]> {
    return this.redis.mget(...keys);
  }

  async batchGetObjects<T>(keys: string[]): Promise<(T | null)[]> {
    const values = await this.batchGet(keys);
    return values.map(v => {
      if (!v) return null;
      try {
        return JSON.parse(v) as T;
      } catch {
        return v as unknown as T;
      }
    });
  }
}
```

## 3. Lists

### 3.1 Giới Thiệu

Redis Lists là ordered collections of strings, được implement như doubly linked lists. Điều này có nghĩa là thêm/xóa elements ở cả hai đầu (head/tail) có độ phức tạp O(1). Tuy nhiên, truy cập elements ở giữa list có độ phức tạp O(n).

### 3.2 List Operations

```redis
# Push operations
LPUSH mylist "element1"           # Push to head
RPUSH mylist "element2"           # Push to tail
LPUSHX mylist "element0"         # Push only if list exists
RPUSHX mylist "element3"         # Push to tail only if list exists

# Pop operations
LPOP mylist                       # Pop from head
RPOP mylist                       # Pop from tail
BLPOP mylist timeout              # Blocking pop from head
BRPOP mylist timeout              # Blocking pop from tail

# Range operations
LRANGE mylist 0 -1               # Get all elements
LRANGE mylist 0 9                # Get first 10 elements
LINDEX mylist 0                   # Get element at index
LINSERT mylist BEFORE "pivot" "new"   # Insert before pivot
LINSERT mylist AFTER "pivot" "new"    # Insert after pivot

# Modification
LSET mylist 0 "new_value"        # Set element at index
LTRIM mylist 0 99                # Trim to keep indices 0-99
LREM mylist 2 "value"            # Remove 2 occurrences of "value"
LREM mylist 0 "value"            # Remove all occurrences

# Utility
LLEN mylist                       # Get list length
SORT mylist ALPHA DESC            # Sort list
```

### 3.3 List Use Cases

```typescript
// 1. Recent activity / Timeline
async function addToTimeline(
  userId: string,
  activity: Activity,
  maxItems = 100
): Promise<void> {
  const key = `timeline:${userId}`;
  const data = JSON.stringify(activity);
  
  await this.redis.lpush(key, data);
  await this.redis.ltrim(key, 0, maxItems - 1);
}

async function getTimeline(
  userId: string,
  page = 0,
  pageSize = 20
): Promise<Activity[]> {
  const key = `timeline:${userId}`;
  const start = page * pageSize;
  const end = start + pageSize - 1;
  
  const items = await this.redis.lrange(key, start, end);
  return items.map(item => JSON.parse(item));
}

// 2. Message Queue (FIFO)
async function enqueueMessage(queueName: string, message: any): Promise<void> {
  await this.redis.rpush(`queue:${queueName}`, JSON.stringify(message));
}

async function dequeueMessage(
  queueName: string,
  timeoutSeconds = 0
): Promise<any | null> {
  const result = timeoutSeconds > 0
    ? await this.redis.brpop(`queue:${queueName}`, timeoutSeconds)
    : await this.redis.rpop(`queue:${queueName}`);
  
  if (!result) return null;
  const [, data] = result; // brpop returns [key, value]
  return JSON.parse(data);
}

// 3. Latest items / Recent logs
async function addLogEntry(service: string, level: string, message: string): Promise<void> {
  const entry = JSON.stringify({
    timestamp: Date.now(),
    level,
    message,
  });
  
  await this.redis.lpush(`logs:${service}`, entry);
  await this.redis.ltrim(`logs:${service}`, 0, 999); // Keep last 1000
}

async function getRecentLogs(service: string, count = 50): Promise<LogEntry[]> {
  const entries = await this.redis.lrange(`logs:${service}`, 0, count - 1);
  return entries.map(e => JSON.parse(e));
}

// 4. Task Queue with Priority
async function enqueueTask(
  queueName: string,
  task: Task,
  priority = 0
): Promise<void> {
  const data = JSON.stringify({ ...task, priority, queuedAt: Date.now() });
  
  if (priority > 0) {
    // High priority - add to head
    await this.redis.lpush(`tasks:${queueName}`, data);
  } else {
    // Normal priority - add to tail
    await this.redis.rpush(`tasks:${queueName}`, data);
  }
}

// 5. Rate Limiter with Sliding Window
async function slidingWindowRateLimit(
  key: string,
  maxRequests: number,
  windowSeconds: number
): Promise<boolean> {
  const now = Date.now();
  const windowStart = now - windowSeconds * 1000;
  
  const pipe = this.redis.pipeline();
  
  // Remove old entries
  pipe.zremrangebyscore(key, 0, windowStart);
  
  // Add current request
  pipe.zadd(key, now, `${now}-${Math.random()}`);
  
  // Count requests in window
  pipe.zcard(key);
  
  // Set TTL
  pipe.expire(key, windowSeconds);
  
  const results = await pipe.exec();
  const requestCount = results?.[2]?.[1] as number;
  
  return requestCount <= maxRequests;
}
```

### 3.4 Python Implementation

```python
import redis
import json
from typing import Any, List, Optional, Callable
from dataclasses import dataclass

class RedisListOperations:
    """
    Wrapper cho Redis List operations
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def lpush(self, key: str, *values: Any) -> int:
        """Push values to the head of list"""
        serialized = [self._serialize(v) for v in values]
        return self.redis.lpush(key, *serialized)
    
    def rpush(self, key: str, *values: Any) -> int:
        """Push values to the tail of list"""
        serialized = [self._serialize(v) for v in values]
        return self.redis.rpush(key, *serialized)
    
    def lpop(self, key: str) -> Optional[Any]:
        """Pop value from head"""
        value = self.redis.lpop(key)
        return self._deserialize(value)
    
    def rpop(self, key: str) -> Optional[Any]:
        """Pop value from tail"""
        value = self.redis.rpop(key)
        return self._deserialize(value)
    
    def brpop(self, key: str, timeout: int = 0) -> Optional[Any]:
        """Blocking pop from tail"""
        result = self.redis.brpop(key, timeout)
        if result:
            return self._deserialize(result[1])
        return None
    
    def lrange(self, key: str, start: int = 0, end: int = -1) -> List[Any]:
        """Get range of elements"""
        values = self.redis.lrange(key, start, end)
        return [self._deserialize(v) for v in values]
    
    def ltrim(self, key: str, start: int, end: int) -> bool:
        """Trim list to keep specified range"""
        return self.redis.ltrim(key, start, end)
    
    def llen(self, key: str) -> int:
        """Get list length"""
        return self.redis.llen(key)
    
    def lindex(self, key: str, index: int) -> Optional[Any]:
        """Get element at index"""
        value = self.redis.lindex(key, index)
        return self._deserialize(value)
    
    def _serialize(self, value: Any) -> str:
        """Serialize value for storage"""
        if isinstance(value, str):
            return value
        return json.dumps(value)
    
    def _deserialize(self, value: Optional[str]) -> Optional[Any]:
        """Deserialize value from storage"""
        if value is None:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value


class MessageQueue:
    """
    Simple message queue using Redis Lists
    """
    
    def __init__(self, redis_client: redis.Redis, queue_name: str):
        self.redis = redis_client
        self.queue_name = queue_name
        self.key = f"queue:{queue_name}"
    
    def enqueue(self, message: Any) -> int:
        """Add message to queue (FIFO)"""
        serialized = json.dumps(message)
        return self.redis.rpush(self.key, serialized)
    
    def dequeue(self, timeout: int = 0) -> Optional[Any]:
        """Remove and return message from queue"""
        if timeout > 0:
            result = self.redis.brpop(self.key, timeout)
            if result:
                return json.loads(result[1])
        else:
            result = self.redis.rpop(self.key)
            if result:
                return json.loads(result)
        return None
    
    def peek(self, count: int = 1) -> List[Any]:
        """Look at messages without removing"""
        values = self.redis.lrange(self.key, -count, -1)
        return [json.loads(v) for v in reversed(values)]
    
    def size(self) -> int:
        """Get queue size"""
        return self.redis.llen(self.key)


class Timeline:
    """
    User timeline using Redis Lists
    """
    
    def __init__(self, redis_client: redis.Redis, max_items: int = 1000):
        self.redis = redis_client
        self.max_items = max_items
    
    def add(self, user_id: str, item: Any) -> int:
        """Add item to user's timeline"""
        key = f"timeline:{user_id}"
        serialized = json.dumps(item)
        
        pipe = self.redis.pipeline()
        pipe.lpush(key, serialized)
        pipe.ltrim(key, 0, self.max_items - 1)
        results = pipe.execute()
        return results[0]
    
    def get(self, user_id: str, page: int = 0, size: int = 20) -> List[Any]:
        """Get timeline items with pagination"""
        key = f"timeline:{user_id}"
        start = page * size
        end = start + size - 1
        
        items = self.redis.lrange(key, start, end)
        return [json.loads(item) for item in items]
    
    def clear(self, user_id: str) -> bool:
        """Clear user's timeline"""
        key = f"timeline:{user_id}"
        return self.redis.delete(key) > 0
```

## 4. Sets

### 4.1 Giới Thiệu

Redis Sets là unordered collections của unique strings. Các operations như add, remove, và membership check có độ phức tạp O(1). Sets đặc biệt hữu ích cho các use cases liên quan đến unique items và set operations.

### 4.2 Set Operations

```redis
# Basic operations
SADD myset "member1" "member2" "member3"
SREM myset "member1"
SISMEMBER myset "member1"           # Check membership (1 or 0)
SMEMBERS myset                     # Get all members
SCARD myset                        # Get set cardinality (size)
SRANDMEMBER myset count            # Get random members
SPOP myset count                   # Remove and return random members

# Set operations
SINTER set1 set2 set3              # Intersection
SINTERSTORE destination set1 set2   # Intersection and store
SUNION set1 set2 set3              # Union
SUNIONSTORE destination set1 set2   # Union and store
SDIFF set1 set2                    # Difference (set1 - set2)
SDIFFSTORE destination set1 set2    # Difference and store

# Advanced
SMISMEMBER key member1 member2      # Check multiple membership
SSCAN key cursor [MATCH pattern] [COUNT count]  # Iterate with cursor
```

### 4.3 Set Use Cases

```typescript
// 1. Tags / Categories
async function addTags(resourceId: string, tags: string[]): Promise<void> {
  const key = `tags:${resourceId}`;
  await this.redis.sadd(key, ...tags);
}

async function removeTags(resourceId: string, tags: string[]): Promise<void> {
  const key = `tags:${resourceId}`;
  await this.redis.srem(key, ...tags);
}

async function getTags(resourceId: string): Promise<string[]> {
  return this.redis.smembers(`tags:${resourceId}`);
}

async function getResourcesWithAllTags(tagKeys: string[]): Promise<string[]> {
  if (tagKeys.length === 0) return [];
  return this.redis.sinter(...tagKeys);
}

async function getResourcesWithAnyTag(tagKeys: string[]): Promise<string[]> {
  if (tagKeys.length === 0) return [];
  return this.redis.sunion(...tagKeys);
}

// 2. User permissions
async function addUserPermissions(userId: string, permissions: string[]): Promise<void> {
  await this.redis.sadd(`permissions:${userId}`, ...permissions);
}

async function hasPermission(userId: string, permission: string): Promise<boolean> {
  const result = await this.redis.sismember(`permissions:${userId}`, permission);
  return result === 1;
}

async function removePermission(userId: string, permission: string): Promise<void> {
  await this.redis.srem(`permissions:${userId}`, permission);
}

// 3. Unique visitors / Daily active users
async function trackUniqueVisitor(date: string, visitorId: string): Promise<boolean> {
  const key = `visitors:daily:${date}`;
  const added = await this.redis.sadd(key, visitorId);
  return added === 1; // Returns 1 if added, 0 if already existed
}

async function getDailyUniqueVisitors(date: string): Promise<number> {
  return this.redis.scard(`visitors:daily:${date}`);
}

async function getWeeklyUniqueVisitors(startDate: string): Promise<number> {
  const dates = getDateRange(startDate, 7);
  const keys = dates.map(d => `visitors:daily:${d}`);
  return this.redis.sunion(...keys).then(ids => ids.length);
}

// 4. Product recommendations
async function trackProductView(userId: string, productId: string): Promise<void> {
  const viewedKey = `viewed:${userId}`;
  await this.redis.sadd(viewedKey, productId);
  await this.redis.expire(viewedKey, 30 * 86400); // 30 days
}

async function getProductRecommendations(
  userId: string,
  categoryKey: string,
  limit = 10
): Promise<string[]> {
  const viewedKey = `viewed:${userId}`;
  
  // Get products in category user hasn't viewed
  const recommendations = await this.redis.sdiff(categoryKey, viewedKey);
  
  // Return random subset
  return this.shuffleArray(recommendations).slice(0, limit);
}

// 5. Anti-spam / IP blocking
async function blockIP(ip: string): Promise<void> {
  await this.redis.sadd('blocked:ips', ip);
}

async function isIPBlocked(ip: string): Promise<boolean> {
  return this.redis.sismember('blocked:ips', ip) === 1;
}

async function getBlockedIPs(): Promise<string[]> {
  return this.redis.smembers('blocked:ips');
}

async function unblockIP(ip: string): Promise<void> {
  await this.redis.srem('blocked:ips', ip);
}
```

## 5. Sorted Sets (ZSets)

### 5.1 Giới Thiệu

Sorted Sets là collections của unique strings được sắp xếp theo score. Mỗi element có một score associated với nó, và elements được sorted theo score. Đây là một trong những data structures mạnh mẽ nhất của Redis, hỗ trợ range queries và rank-based operations với O(log N) complexity.

### 5.2 Sorted Set Operations

```redis
# Basic operations
ZADD myzset 1 "one" 2 "two" 3 "three"
ZSCORE myzset "one"                  # Get score of member
ZRANK myzset "one"                   # Get rank (0-indexed, ascending)
ZREVRANK myzset "one"                # Get rank (descending)

# Range operations
ZRANGE myzset 0 -1                   # Get all (with scores)
ZREVRANGE myzset 0 -1                # Get all (descending)
ZRANGEBYSCORE myzset 1 3             # Get by score range
ZRANGEBYSCORE myzset -inf +inf       # Get all by score
ZRANGEBYSCORE myzset 0 10 WITHSCORES # With scores

# Count operations
ZCARD myzset                         # Get set size
ZCOUNT myzset 1 3                    # Count by score range
ZLEXCOUNT myzset [a [c               # Count by lex range

# Modification
ZINCRBY myzset 2 "one"               # Increment score
ZREM myzset "two"                   # Remove member
ZREMRANGEBYRANK myzset 0 1          # Remove by rank
ZREMRANGEBYSCORE myzset 0 1         # Remove by score
ZREMRANGEBYLEX myzset [a [c          # Remove by lex

# Set operations
ZUNIONSTORE dest numkeys key1 key2 [WEIGHTS w1 w2] [AGGREGATE SUM|MIN|MAX]
ZINTERSTORE dest numkeys key1 key2 [WEIGHTS w1 w2] [AGGREGATE SUM|MIN|MAX]

# Pagination
ZRANGE myzset 0 9 WITHSCORES
ZREVRANGE myzset 0 9 WITHSCORES
```

### 5.3 Sorted Set Use Cases

```typescript
// 1. Leaderboard / Rankings
class Leaderboard {
  async addScore(userId: string, gameId: string, score: number): Promise<void> {
    const key = `leaderboard:${gameId}`;
    await this.redis.zadd(key, score, userId);
  }

  async getRank(userId: string, gameId: string): Promise<number | null> {
    const key = `leaderboard:${gameId}`;
    const rank = await this.redis.zrevrank(key, userId);
    return rank !== null ? rank + 1 : null; // Convert to 1-indexed
  }

  async getScore(userId: string, gameId: string): Promise<number | null> {
    const key = `leaderboard:${gameId}`;
    const score = await this.redis.zscore(key, userId);
    return score !== null ? parseFloat(score) : null;
  }

  async getTopPlayers(gameId: string, count = 10): Promise<PlayerScore[]> {
    const key = `leaderboard:${gameId}`;
    const results = await this.redis.zrevrange(key, 0, count - 1, 'WITHSCORES');
    
    const players: PlayerScore[] = [];
    for (let i = 0; i < results.length; i += 2) {
      players.push({
        userId: results[i],
        score: parseFloat(results[i + 1]),
        rank: Math.floor(i / 2) + 1,
      });
    }
    return players;
  }

  async getPlayersAround(
    gameId: string,
    userId: string,
    range = 5
  ): Promise<PlayerScore[]> {
    const key = `leaderboard:${gameId}`;
    const rank = await this.redis.zrevrank(key, userId);
    
    if (rank === null) return [];
    
    const start = Math.max(0, rank - range);
    const end = rank + range;
    
    const results = await this.redis.zrevrange(key, start, end, 'WITHSCORES');
    
    const players: PlayerScore[] = [];
    for (let i = 0; i < results.length; i += 2) {
      players.push({
        userId: results[i],
        score: parseFloat(results[i + 1]),
        rank: start + Math.floor(i / 2) + 1,
      });
    }
    return players;
  }

  async incrementScore(
    userId: string,
    gameId: string,
    increment: number
  ): Promise<number> {
    const key = `leaderboard:${gameId}`;
    return this.redis.zincrby(key, increment, userId);
  }
}

// 2. Time-series data
async function addEvent(
  eventType: string,
  timestamp: number,
  data: object
): Promise<void> {
  const key = `events:${eventType}`;
  await this.redis.zadd(key, timestamp, JSON.stringify({ timestamp, ...data }));
}

async function getEventsInRange(
  eventType: string,
  startTime: number,
  endTime: number
): Promise<Event[]> {
  const key = `events:${eventType}`;
  const results = await this.redis.zrangebyscore(key, startTime, endTime);
  return results.map(r => JSON.parse(r));
}

async function getLatestEvents(
  eventType: string,
  count = 100
): Promise<Event[]> {
  const key = `events:${eventType}`;
  const results = await this.redis.zrevrange(key, 0, count - 1);
  return results.map(r => JSON.parse(r));
}

async function pruneOldEvents(eventType: string, maxAge: number): Promise<void> {
  const key = `events:${eventType}`;
  const cutoff = Date.now() - maxAge;
  await this.redis.zremrangebyscore(key, 0, cutoff);
}

// 3. Priority queue / Task scheduling
async function scheduleTask(
  taskId: string,
  priority: number,
  taskData: object
): Promise<void> {
  const key = 'tasks:scheduled';
  const member = JSON.stringify({ id: taskId, data: taskData });
  await this.redis.zadd(key, priority, member);
}

async function getNextTask(): Promise<Task | null> {
  const key = 'tasks:scheduled';
  const now = Date.now();
  
  // Get task with score <= now
  const results = await this.redis.zrangebyscore(key, '-inf', now, 'LIMIT', 0, 1);
  
  if (results.length === 0) return null;
  
  const task = JSON.parse(results[0]);
  
  // Remove from queue
  await this.redis.zrem(key, results[0]);
  
  return task;
}

// 4. Rate limiting with sliding window
async function slidingWindowRateLimit(
  identifier: string,
  maxRequests: number,
  windowSeconds: number
): Promise<{ allowed: boolean; remaining: number; resetAt: number }> {
  const key = `ratelimit:sliding:${identifier}`;
  const now = Date.now();
  const windowStart = now - windowSeconds * 1000;
  
  const pipe = this.redis.pipeline();
  
  // Remove old entries
  pipe.zremrangebyscore(key, 0, windowStart);
  
  // Count current entries
  pipe.zcard(key);
  
  const results = await pipe.exec();
  const currentCount = results?.[1]?.[1] as number;
  
  if (currentCount >= maxRequests) {
    // Get oldest entry to calculate reset time
    const oldest = await this.redis.zrange(key, 0, 0, 'WITHSCORES');
    const resetAt = oldest.length >= 2 
      ? parseInt(oldest[1]) + windowSeconds * 1000 
      : now + windowSeconds * 1000;
    
    return { allowed: false, remaining: 0, resetAt };
  }
  
  // Add new request
  await this.redis.zadd(key, now, `${now}-${Math.random()}`);
  await this.redis.expire(key, windowSeconds);
  
  return {
    allowed: true,
    remaining: maxRequests - currentCount - 1,
    resetAt: now + windowSeconds * 1000,
  };
}
```

## 6. Hashes

### 6.1 Giới Thiệu

Redis Hashes là field-value pairs giữa một single key, tương tự như JSON objects hoặc database rows. Chúng rất hiệu quả về memory khi lưu trữ objects với nhiều fields, và các operations như HGET, HSET có độ phức tạp O(1).

### 6.2 Hash Operations

```redis
# Basic operations
HSET user:123 name "John" email "john@example.com" age "30"
HGET user:123 name
HGETALL user:123
HDEL user:123 age
HEXISTS user:123 email              # Check if field exists (1 or 0)

# Multiple fields
HMSET user:123 name "John" email "john@example.com"  # Legacy
HSET user:123 name "John" email "john@example.com"     # Modern
HMGET user:123 name email
HMLEN user:123

# Field operations
HINCRBY user:123 login_count 1
HINCRBYFLOAT user:123 balance 10.50

# Get operations
HLEN user:123
HSTRLEN user:123 name

# Field operations
HKEYS user:123                      # Get all field names
HVALS user:123                      # Get all values
HSCAN user:123 cursor [MATCH pattern] [COUNT count]  # Iterate
```

### 6.3 Hash Use Cases

```typescript
// 1. User profiles
async function setUserProfile(userId: string, profile: UserProfile): Promise<void> {
  const key = `user:${userId}:profile`;
  await this.redis.hmset(key, {
    name: profile.name,
    email: profile.email,
    avatar: profile.avatar || '',
    bio: profile.bio || '',
    createdAt: profile.createdAt.toISOString(),
    updatedAt: new Date().toISOString(),
  });
}

async function getUserProfile(userId: string): Promise<UserProfile | null> {
  const key = `user:${userId}:profile`;
  const data = await this.redis.hgetall(key);
  
  if (!data || Object.keys(data).length === 0) return null;
  
  return {
    name: data.name,
    email: data.email,
    avatar: data.avatar,
    bio: data.bio,
    createdAt: new Date(data.createdAt),
    updatedAt: new Date(data.updatedAt),
  };
}

async function updateUserProfile(
  userId: string,
  updates: Partial<UserProfile>
): Promise<void> {
  const key = `user:${userId}:profile`;
  const hash: Record<string, string> = {};
  
  if (updates.name !== undefined) hash.name = updates.name;
  if (updates.email !== undefined) hash.email = updates.email;
  if (updates.avatar !== undefined) hash.avatar = updates.avatar;
  if (updates.bio !== undefined) hash.bio = updates.bio;
  hash.updatedAt = new Date().toISOString();
  
  if (Object.keys(hash).length > 0) {
    await this.redis.hmset(key, hash);
  }
}

// 2. Product catalog
async function setProduct(product: Product): Promise<void> {
  const key = `product:${product.id}`;
  await this.redis.hmset(key, {
    id: product.id,
    name: product.name,
    description: product.description,
    price: product.price.toString(),
    category: product.category,
    stock: product.stock.toString(),
    updatedAt: new Date().toISOString(),
  });
}

async function getProduct(productId: string): Promise<Product | null> {
  const key = `product:${productId}`;
  const data = await this.redis.hgetall(key);
  
  if (!data || Object.keys(data).length === 0) return null;
  
  return {
    id: data.id,
    name: data.name,
    description: data.description,
    price: parseFloat(data.price),
    category: data.category,
    stock: parseInt(data.stock),
    updatedAt: new Date(data.updatedAt),
  };
}

async function updateProductStock(productId: string, delta: number): Promise<number> {
  const key = `product:${productId}`;
  return this.redis.hincrby(key, 'stock', delta);
}

// 3. Session storage
async function setSession(sessionId: string, sessionData: SessionData): Promise<void> {
  const key = `session:${sessionId}`;
  await this.redis.hmset(key, {
    userId: sessionData.userId,
    data: JSON.stringify(sessionData.data),
    createdAt: sessionData.createdAt.toISOString(),
    lastActive: sessionData.lastActive.toISOString(),
  });
  await this.redis.expire(key, sessionData.ttlSeconds);
}

async function updateSessionActivity(sessionId: string): Promise<void> {
  const key = `session:${sessionId}`;
  await this.redis.hset(key, 'lastActive', new Date().toISOString());
}

// 4. Caching with hash
async function cacheApiResponse(
  endpoint: string,
  params: Record<string, string>,
  response: any,
  ttlSeconds = 300
): Promise<void> {
  const hashKey = this.hashParams(params);
  const key = `cache:${endpoint}:${hashKey}`;
  
  await this.redis.hmset(key, {
    response: JSON.stringify(response),
    cachedAt: Date.now().toString(),
  });
  await this.redis.expire(key, ttlSeconds);
}

async function getCachedApiResponse(
  endpoint: string,
  params: Record<string, string>
): Promise<any | null> {
  const hashKey = this.hashParams(params);
  const key = `cache:${endpoint}:${hashKey}`;
  
  const data = await this.redis.hgetall(key);
  if (!data || !data.response) return null;
  
  return JSON.parse(data.response);
}

private hashParams(params: Record<string, string>): string {
  const sorted = Object.entries(params)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([k, v]) => `${k}=${v}`)
    .join('&');
  return crypto.createHash('md5').update(sorted).digest('hex');
}
```

## 7. Bitmaps

### 7.1 Giới Thiệu

Bitmaps không phải là một data type riêng biệt - chúng là một view của String data type, cho phép bạn treat strings như bit arrays. Đây là một cách cực kỳ memory-efficient để store boolean flags hoặc sets, đặc biệt khi dealing với large-scale boolean data.

### 7.2 Bitmap Operations

```redis
# Set/Get bits
SETBIT bitmap 10 1                    # Set bit at offset 10 to 1
GETBIT bitmap 10                      # Get bit at offset 10
SETBIT bitmap 0 1                     # Set bit 0
GETBIT bitmap 0                       # Returns 1

# Bitwise operations
BITOP AND result key1 key2            # AND operation
BITOP OR result key1 key2             # OR operation
BITOP XOR result key1 key2             # XOR operation
BITOP NOT result key1                  # NOT operation

# Count/Analysis
BITCOUNT bitmap [start end]           # Count set bits
BITPOS bitmap 0 [start end]           # Find first bit with value 0
BITPOS bitmap 1 [start end]           # Find first bit with value 1

# Get range as string
GET bitmap
```

### 7.3 Bitmap Use Cases

```typescript
// 1. Daily active users tracking
class DailyActiveUsers {
  private redis: Redis;

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async markActive(date: string, userId: string): Promise<void> {
    // Use userId as bit offset
    const key = `dau:${date}`;
    const offset = this.userIdToOffset(userId);
    await this.redis.setbit(key, offset, 1);
  }

  async isActive(date: string, userId: string): Promise<boolean> {
    const key = `dau:${date}`;
    const offset = this.userIdToOffset(userId);
    const result = await this.redis.getbit(key, offset);
    return result === 1;
  }

  async getActiveCount(date: string): Promise<number> {
    const key = `dau:${date}`;
    return this.redis.bitcount(key);
  }

  async getActiveUsers(date: string): Promise<string[]> {
    const key = `dau:${date}`;
    const bitmap = await this.redis.get(key);
    return this.parseBitmapUsers(bitmap);
  }

  // For date ranges
  async getDailyActiveUsersRange(
    startDate: string,
    endDate: string
  ): Promise<Map<string, number>> {
    const dates = this.getDateRange(startDate, endDate);
    const keys = dates.map(d => `dau:${d}`);
    
    const results = new Map<string, number>();
    
    for (const date of dates) {
      const count = await this.redis.bitcount(`dau:${date}`);
      results.set(date, count);
    }
    
    return results;
  }

  // User overlap between days
  async getOverlapUsers(date1: string, date2: string): Promise<number> {
    const key1 = `dau:${date1}`;
    const key2 = `dau:${date2}`;
    const tempKey = `temp:overlap:${Date.now()}`;
    
    await this.redis.bitop('AND', tempKey, key1, key2);
    const overlap = await this.redis.bitcount(tempKey);
    await this.redis.del(tempKey);
    
    return overlap;
  }

  private userIdToOffset(userId: string): number {
    // Convert userId to numeric offset
    // In production, use consistent hashing or mapping
    return parseInt(userId.replace(/\D/g, '')) || this.hashString(userId);
  }

  private hashString(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash |= 0;
    }
    return Math.abs(hash);
  }

  private parseBitmapUsers(bitmap: string | null): string[] {
    if (!bitmap) return [];
    // This is simplified - in production, track offset -> userId mapping
    return [];
  }

  private getDateRange(startDate: string, days: number): string[] {
    const dates: string[] = [];
    const start = new Date(startDate);
    for (let i = 0; i < days; i++) {
      const d = new Date(start);
      d.setDate(d.getDate() + i);
      dates.push(d.toISOString().split('T')[0]);
    }
    return dates;
  }
}

// 2. Online status tracking
class OnlineStatus {
  async setUserOnline(userId: string): Promise<void> {
    const key = 'online:users';
    const offset = this.hashUserId(userId);
    await this.redis.setbit(key, offset, 1);
  }

  async setUserOffline(userId: string): Promise<void> {
    const key = 'online:users';
    const offset = this.hashUserId(userId);
    await this.redis.setbit(key, offset, 0);
  }

  async isUserOnline(userId: string): Promise<boolean> {
    const key = 'online:users';
    const offset = this.hashUserId(userId);
    return (await this.redis.getbit(key, offset)) === 1;
  }

  async getOnlineCount(): Promise<number> {
    return this.redis.bitcount('online:users');
  }

  private hashUserId(userId: string): number {
    // Simple hash for demo - use consistent hashing in production
    let hash = 0;
    for (let i = 0; i < userId.length; i++) {
      hash = ((hash << 5) - hash) + userId.charCodeAt(i);
      hash |= 0;
    }
    return Math.abs(hash) % 10000000; // Limit to 10 million bits
  }
}

// 3. Feature flags
class FeatureFlags {
  async enableFeature(userId: string, feature: string): Promise<void> {
    const key = `features:${feature}`;
    const offset = this.userIdToOffset(userId);
    await this.redis.setbit(key, offset, 1);
  }

  async disableFeature(userId: string, feature: string): Promise<void> {
    const key = `features:${feature}`;
    const offset = this.userIdToOffset(userId);
    await this.redis.setbit(key, offset, 0);
  }

  async isFeatureEnabled(userId: string, feature: string): Promise<boolean> {
    const key = `features:${feature}`;
    const offset = this.userIdToOffset(userId);
    return (await this.redis.getbit(key, offset)) === 1;
  }

  async getFeatureUserCount(feature: string): Promise<number> {
    const key = `features:${feature}`;
    return this.redis.bitcount(key);
  }
}
```

## 8. HyperLogLog

### 8.1 Giới Thiệu

HyperLogLog (HLL) là một probabilistic data structure dùng để estimate the cardinality (số lượng unique elements) của một set với memory rất thấp (~12KB per counter). Error rate vào khoảng 0.81%, là sự đánh đổi chấp nhận được cho hầu hết use cases cần cardinality estimation.

### 8.2 HyperLogLog Operations

```redis
# Add elements
PFADD hll key element1 element2 element3
PFADD hll element1
PFADD hll element2

# Get estimate
PFCOUNT hll                           # Get cardinality estimate
PFCOUNT hll1 hll2 hll3                # Merge and count multiple

# Merge
PFMERGE dest hll1 hll2 hll3           # Merge multiple HLLs into dest
```

### 8.3 HyperLogLog Use Cases

```typescript
class HyperLogLogAnalytics {
  private redis: Redis;

  constructor(redis: Redis) {
    this.redis = redis;
  }

  // 1. Daily unique visitors
  async addVisitor(date: string, visitorId: string): Promise<void> {
    const key = `hll:visitors:daily:${date}`;
    await this.redis.pfadd(key, visitorId);
  }

  async getDailyUniqueVisitors(date: string): Promise<number> {
    const key = `hll:visitors:daily:${date}`;
    return this.redis.pfcount(key);
  }

  async getWeeklyUniqueVisitors(startDate: string): Promise<number> {
    const dates = this.getWeekDates(startDate);
    const keys = dates.map(d => `hll:visitors:daily:${d}`);
    return this.redis.pfcount(...keys);
  }

  // 2. Product unique views
  async recordProductView(productId: string, visitorId: string): Promise<void> {
    const key = `hll:product:${productId}:views`;
    await this.redis.pfadd(key, visitorId);
  }

  async getUniqueProductViews(productId: string): Promise<number> {
    const key = `hll:product:${productId}:views`;
    return this.redis.pfcount(key);
  }

  // 3. Search unique queries
  async recordSearchQuery(userId: string, query: string): Promise<void> {
    const today = new Date().toISOString().split('T')[0];
    const key = `hll:searches:daily:${today}`;
    const uniqueQuery = `${userId}:${query.toLowerCase().trim()}`;
    await this.redis.pfadd(key, uniqueQuery);
  }

  async getDailySearchQueries(date: string): Promise<number> {
    const key = `hll:searches:daily:${date}`;
    return this.redis.pfcount(key);
  }

  // 4. Cross-platform unique users
  async mergeUniqueUsers(
    platform1Key: string,
    platform2Key: string
  ): Promise<number> {
    const destKey = `hll:merged:${Date.now()}`;
    await this.redis.pfmerge(destKey, platform1Key, platform2Key);
    const count = await this.redis.pfcount(destKey);
    await this.redis.del(destKey);
    return count;
  }

  // 5. Retention analysis
  async recordUserActivity(userId: string, date: string): Promise<void> {
    const key = `hll:active:daily:${date}`;
    await this.redis.pfadd(key, userId);
  }

  async calculateRetention(
    cohortDate: string,
    targetDate: string
  ): Promise<number> {
    const cohortKey = `hll:active:daily:${cohortDate}`;
    const targetKey = `hll:active:daily:${targetDate}`;
    
    // Merge to temp key and count
    const tempKey = `hll:temp:${Date.now()}`;
    await this.redis.pfmerge(tempKey, cohortKey, targetKey);
    const mergedCount = await this.redis.pfcount(tempKey);
    
    // We need intersection, not union
    // For proper retention, use sets instead
    await this.redis.del(tempKey);
    
    return 0; // Placeholder - use Sets for proper retention
  }

  private getWeekDates(startDate: string): string[] {
    const dates: string[] = [];
    const start = new Date(startDate);
    for (let i = 0; i < 7; i++) {
      const d = new Date(start);
      d.setDate(d.getDate() + i);
      dates.push(d.toISOString().split('T')[0]);
    }
    return dates;
  }
}
```

## 9. Geospatial Indexes (GEO)

### 9.1 Giới Thiệu

Redis GEO commands cho phép bạn lưu trữ coordinates (latitude, longitude) và thực hiện các queries như tìm các điểm gần nhất, tính khoảng cách giữa các điểm. Đây là một tính năng mạnh mẽ cho các ứng dụng location-based services.

### 9.2 Geospatial Operations

```redis
# Add locations
GEOADD locations 13.361389 38.115556 "Palermo" 15.087269 37.502669 "Catania"
GEOADD users:locations -122.4194 37.7749 "user1"

# Get coordinates
GEOPOS locations "Palermo"                    # Get position of member
GEOPOS locations "Palermo" "Catania"

# Calculate distance
GEODIST locations "Palermo" "Catania" km      # Distance in km
GEODIST locations "Palermo" "Catania" mi     # Distance in miles
GEODIST locations "Palermo" "Catania" m      # Distance in meters

# Find nearby locations
GEORADIUS locations 15 37 100 km              # Points within 100km of (15, 37)
GEORADIUS locations 15 37 100 km WITHDIST      # Include distance
GEORADIUS locations 15 37 100 km WITHCOORD    # Include coordinates
GEORADIUS locations 15 37 100 km COUNT 10     # Limit results
GEORADIUS locations 15 37 100 km ASC           # Sort ascending
GEORADIUS locations 15 37 100 km DESC          # Sort descending

# Find nearby for stored member
GEORADIUSBYMEMBER locations "Palermo" 100 km

# Get hash (geohash)
GEOHASH locations "Palermo"
GEOHASH locations "Palermo" "Catania"
```

### 9.3 Geospatial Use Cases

```typescript
class GeoOperations {
  private redis: Redis;

  constructor(redis: Redis) {
    this.redis = redis;
  }

  // 1. Store user locations
  async updateUserLocation(
    userId: string,
    longitude: number,
    latitude: number
  ): Promise<void> {
    const key = 'geo:users';
    await this.redis.geoadd(key, longitude, latitude, userId);
  }

  async getUserLocation(userId: string): Promise<Location | null> {
    const key = 'geo:users';
    const positions = await this.redis.geopos(key, userId);
    
    if (!positions || !positions[0]) return null;
    
    const [longitude, latitude] = positions[0];
    return { longitude, latitude };
  }

  // 2. Find nearby users
  async findNearbyUsers(
    longitude: number,
    latitude: number,
    radiusKm: number,
    limit = 50
  ): Promise<NearbyUser[]> {
    const key = 'geo:users';
    
    const results = await this.redis.georadius(
      key,
      longitude,
      latitude,
      radiusKm,
      'km',
      'WITHCOORD',
      'WITHDIST',
      'ASC',
      'COUNT',
      limit
    );
    
    return results.map((result: any) => ({
      userId: result[0],
      distance: parseFloat(result[1]),
      longitude: result[2][0],
      latitude: result[2][1],
    }));
  }

  // 3. Find nearby stores
  async findNearbyStores(
    longitude: number,
    latitude: number,
    radiusKm: number,
    limit = 20
  ): Promise<Store[]> {
    const key = 'geo:stores';
    
    const results = await this.redis.georadius(
      key,
      longitude,
      latitude,
      radiusKm,
      'km',
      'WITHCOORD',
      'WITHDIST',
      'ASC',
      'COUNT',
      limit
    );
    
    // Fetch store details from hash
    const storeIds = results.map((r: any) => r[0]);
    const storeDetails = await this.getStoreDetails(storeIds);
    
    return results.map((result: any, index: number) => ({
      ...storeDetails[index],
      distance: parseFloat(result[1]),
      location: {
        longitude: result[2][0],
        latitude: result[2][1],
      },
    }));
  }

  // 4. Store with additional details
  async addStore(store: Store): Promise<void> {
    const geoKey = 'geo:stores';
    const hashKey = `store:${store.id}`;
    
    // Add to geo index
    await this.redis.geoadd(
      geoKey,
      store.location.longitude,
      store.location.latitude,
      store.id
    );
    
    // Store details in hash
    await this.redis.hmset(hashKey, {
      id: store.id,
      name: store.name,
      address: store.address,
      category: store.category,
      rating: store.rating.toString(),
    });
  }

  async getStoreDetails(storeIds: string[]): Promise<Store[]> {
    const pipeline = this.redis.pipeline();
    for (const id of storeIds) {
      pipeline.hgetall(`store:${id}`);
    }
    
    const results = await pipeline.exec();
    return results?.map(([, data]) => data as Store) || [];
  }

  // 5. Calculate distance between users
  async getDistanceBetweenUsers(
    userId1: string,
    userId2: string
  ): Promise<number | null> {
    const key = 'geo:users';
    const distance = await this.redis.geodist(key, userId1, userId2, 'km');
    return distance ? parseFloat(distance) : null;
  }

  // 6. Delivery zone checking
  async isWithinDeliveryZone(
    userLat: number,
    userLng: number,
    zoneRadiusKm: number
  ): Promise<boolean> {
    const centerLat = 40.7128; // NYC as example
    const centerLng = -74.0060;
    
    const distance = await this.redis.geodist(
      'geo:delivery:zones:nyc',
      `${centerLat},${centerLng}`,
      `${userLat},${userLng}`,
      'km'
    );
    
    return distance !== null && parseFloat(distance) <= zoneRadiusKm;
  }

  // 7. Geofencing alerts
  async getUsersInGeofence(
    geofenceId: string,
    centerLat: number,
    centerLng: number,
    radiusKm: number
  ): Promise<string[]> {
    const usersKey = 'geo:users';
    const geofenceKey = `geo:geofence:${geofenceId}`;
    
    // Store geofence center temporarily
    await this.redis.geoadd(
      geofenceKey,
      centerLng,
      centerLat,
      'center'
    );
    
    // Find users within geofence
    const nearby = await this.redis.georadius(
      usersKey,
      centerLng,
      centerLat,
      radiusKm,
      'km'
    );
    
    // Cleanup
    await this.redis.del(geofenceKey);
    
    return nearby;
  }
}
```

### 9.4 Python Geospatial Implementation

```python
import redis
from typing import List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Location:
    longitude: float
    latitude: float

@dataclass
class GeoResult:
    member: str
    distance: Optional[float] = None
    coordinates: Optional[Location] = None
    hash: Optional[str] = None

class RedisGeoOperations:
    """
    Geospatial operations wrapper
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def geoadd(
        self, 
        key: str, 
        longitude: float, 
        latitude: float, 
        member: str
    ) -> int:
        """Add a member to a geo set"""
        return self.redis.geoadd(key, (longitude, latitude, member))
    
    def geopos(self, key: str, *members: str) -> List[Optional[Tuple[float, float]]]:
        """Get positions of members"""
        return self.redis.geopos(key, *members)
    
    def geodist(
        self, 
        key: str, 
        member1: str, 
        member2: str, 
        unit: str = 'm'
    ) -> Optional[float]:
        """Calculate distance between two members"""
        return self.redis.geodist(key, member1, member2, unit)
    
    def georadius(
        self,
        key: str,
        longitude: float,
        latitude: float,
        radius: float,
        unit: str = 'km',
        withdist: bool = False,
        withcoord: bool = False,
        withhash: bool = False,
        count: Optional[int] = None,
        sort: Optional[str] = None
    ) -> List:
        """Find members within radius of a point"""
        return self.redis.georadius(
            key,
            longitude,
            latitude,
            radius,
            unit,
            withdist=withdist,
            withcoord=withcoord,
            withhash=withhash,
            count=count,
            sort=sort
        )
    
    def georadiusbymember(
        self,
        key: str,
        member: str,
        radius: float,
        unit: str = 'km',
        **kwargs
    ) -> List:
        """Find members within radius of a member"""
        return self.redis.georadiusbymember(
            key,
            member,
            radius,
            unit,
            **kwargs
        )
    
    def geohash(self, key: str, *members: str) -> List[str]:
        """Get geohash of members"""
        return self.redis.geohash(key, *members)


class LocationService:
    """
    Location-based service using Redis Geo
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.geo = RedisGeoOperations(redis_client)
        self.redis = redis_client
    
    def add_location(self, key: str, member: str, lat: float, lng: float) -> None:
        """Add a location to geo index"""
        self.geo.geoadd(key, lng, lat, member)
    
    def nearby(
        self, 
        key: str, 
        lat: float, 
        lng: float, 
        radius_km: float,
        limit: int = 20
    ) -> List[GeoResult]:
        """Find nearby locations"""
        results = self.geo.georadius(
            key, lng, lat, radius_km,
            withdist=True,
            withcoord=True,
            sort='ASC',
            count=limit
        )
        
        return [
            GeoResult(
                member=r[0],
                distance=r[1],
                coordinates=Location(longitude=r[2][0], latitude=r[2][1])
            )
            for r in results
        ]
    
    def distance(self, key: str, member1: str, member2: str) -> float:
        """Get distance between two members in km"""
        dist = self.geo.geodist(key, member1, member2, 'km')
        return float(dist) if dist else 0.0
```

## 10. Best Practices và Performance Considerations

### 10.1 Memory Efficiency

```typescript
// Choose appropriate data structures
const DATA_STRUCTURE_CHOICES = {
  // For simple key-value (string)
  useCase: 'Config, session data, simple cache',
  recommended: 'String (or Hash for multiple fields)',
  
  // For unique collections
  useCase: 'Tags, unique IDs, permissions',
  recommended: 'Set',
  
  // For sorted unique collections
  useCase: 'Leaderboards, priorities, time-series',
  recommended: 'Sorted Set',
  
  // For ordered collections
  useCase: 'Queues, histories, feeds',
  recommended: 'List',
  
  // For objects
  useCase: 'User profiles, product info',
  recommended: 'Hash',
  
  // For boolean flags at scale
  useCase: 'Tracking, feature flags, active status',
  recommended: 'Bitmap',
  
  // For unique counts
  useCase: 'UV tracking, analytics',
  recommended: 'HyperLogLog',
  
  // For locations
  useCase: 'Store finder, user locations',
  recommended: 'Geo',
};
```

### 10.2 Encoding Optimization

```redis
# Memory-efficient encodings
# Redis automatically uses efficient encodings:

# Hashes with few fields useziplist encoding
# Lists with few items use ziplist encoding
# Sets with few members use intset encoding
# Sorted sets with few elements use ziplist encoding

# For large datasets, Redis automatically switches to
#hashtable/linkedlist/skiplist encodings

# Monitor encoding types
DEBUG OBJECT ENCODING mykey

# Encoding types:
# - raw: Regular string
# - int: Integer (for numeric strings)
# - ziplist: Memory-efficient list/hash
# - intset: Memory-efficient integer set
# - skiplist: Sorted set with skip list
# - hashtable: Regular hash/set
```

### 10.3 Key Naming Conventions

```typescript
const NAMING_CONVENTIONS = {
  // Hierarchical naming
  userProfile: 'user:{userId}:profile',
  userSession: 'session:{sessionId}',
  userPermissions: 'user:{userId}:permissions',
  
  // Namespaced by data type
  cachePrefix: 'cache:',
  rateLimitPrefix: 'ratelimit:',
  lockPrefix: 'lock:',
  
  // Namespaced by feature
  leaderboardKey: 'leaderboard:{gameId}',
  timelineKey: 'timeline:{userId}',
  
  // Time-series
  dailyMetric: 'metrics:{metric}:{YYYY-MM-DD}',
  hourlyMetric: 'metrics:{metric}:{YYYY-MM-DD-HH}',
  
  // Examples:
  // Good: user:12345:profile, cache:product:SKU001
  // Bad: profile_12345, product_data
};
```

## 11. References

- [Redis Data Types Documentation](https://redis.io/docs/data-types/)
- [Redis Strings](https://redis.io/docs/data-types/strings/)
- [Redis Lists](https://redis.io/docs/data-types/lists/)
- [Redis Sets](https://redis.io/docs/data-types/sets/)
- [Redis Sorted Sets](https://redis.io/docs/data-types/sorted-sets/)
- [Redis Hashes](https://redis.io/docs/data-types/hashes/)
- [Redis Bitmaps](https://redis.io/docs/data-types/bitmaps/)
- [Redis Geospatial](https://redis.io/docs/data-types/geospatial/)
- [Redis HyperLogLog](https://redis.io/docs/data-types/hyperloglogs/)
