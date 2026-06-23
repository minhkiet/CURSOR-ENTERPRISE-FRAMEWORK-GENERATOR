# Redis FAQ - Câu Hỏi Thường Gặp

## Mục lục
1. [General Questions](#1-general-questions)
2. [Data Types](#2-data-types)
3. [Performance](#3-performance)
4. [Persistence](#4-persistence)
5. [Clustering](#5-clustering)

---

## 1. General Questions

### Q1: Redis vs Memcached - Nên dùng cái nào?

**Trả lời**: Redis cung cấp richer data structures và persistence options, trong khi Memcached đơn giản hơn và scale horizontally easier.

**Khi nào dùng Redis**:
- Cần complex data types (Hash, List, Set, Sorted Set)
- Cần persistence (RDB, AOF)
- Cần atomic operations
- Cần pub/sub hoặc streams
- Cần built-in clustering

**Khi nào dùng Memcached**:
- Simple key-value caching
- Pure session storage
- Scale horizontally across multiple instances
- Maximum simplicity needed
- No persistence needed

**Ví dụ**:
```redis
# Redis: Rich data structures
HSET user:1001 name "John" email "john@example.com"
ZADD leaderboard 1000 "player1" 2000 "player2"
LPUSH queue:tasks "task1" "task2"

# Memcached: Simple key-value only
set user:1001 "John" 3600
get user:1001
```

### Q2: Eviction policies khác nhau gì?

**Trả lời**: Redis cung cấp 8 eviction policies, chọn dựa trên use case.

**Chi tiết eviction policies**:

```redis
# noeviction: Return error when memory limit reached
# Best for: Persistent data storage
SET maxmemory-policy noeviction

# allkeys-lru: Evict least recently used keys globally
# Best for: Cache - keep hot data
SET maxmemory-policy allkeys-lru

# allkeys-lfu: Evict least frequently used keys globally
# Best for: Cache - keep frequently accessed data
SET maxmemory-policy allkeys-lfu

# allkeys-random: Evict random keys globally
# Best for: Cache - simple rotation
SET maxmemory-policy allkeys-random

# volatile-lru: Evict LRU among keys with TTL only
# Best for: Mix of persistent and cache data
SET maxmemory-policy volatile-lru

# volatile-lfu: Evict LFU among keys with TTL only
# Best for: Mix with frequency-based eviction
SET maxmemory-policy volatile-lfu

# volatile-random: Evict random among keys with TTL only
# Best for: TTL-based rotation
SET maxmemory-policy volatile-random

# volatile-ttl: Evict keys with shortest TTL
# Best for: Automatic cleanup of expired data
SET maxmemory-policy volatile-ttl
```

**Recommendation**:
- Cache: `allkeys-lru` hoặc `allkeys-lfu`
- Session store: `volatile-lru` hoặc `volatile-ttl`
- Rate limiting: `noeviction` với monitoring

### Q3: Redis có durable như database không?

**Trả lời**: Redis là in-memory store nhưng cung cấp persistence options. Data có thể được lost nếu không configure properly.

**Persistence options**:
```bash
# RDB: Point-in-time snapshots
# Pros: Fast, compact, good for backups
# Cons: Some data loss possible between snapshots

# AOF: Append-only file
# Pros: Better durability, fsync options
# Cons: Larger files, slightly slower

# Both (recommended for critical data)
# Best of both worlds - combine safety
```

**Best practice for durability**:
```redis
# Configuration for critical data
# redis.conf:

# Enable AOF
appendonly yes

# fsync every second (balance of safety and performance)
appendfsync everysec

# Rewrite when AOF gets too large
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# RDB as backup
save 900 1
save 300 10
save 60 10000
```

---

## 2. Data Types

### Q4: String vs Hash - Khi nào dùng cái nào?

**Trả lời**: Sử dụng Hash cho structured objects với multiple fields, String cho simple values hoặc serialized data.

**Ví dụ**:
```redis
# String: Simple values
SET user:1001:token "jwt_token_here"
SET cache:page:home "<html>..."
SET counter:page_views 100

# Hash: Structured objects
HSET user:1001 name "John" email "john@example.com" age 30

# When to use String:
# - Simple scalar values
# - Serialized objects you rarely update partially
# - Binary data (images, files)
# - Values under 100KB

# When to use Hash:
# - Objects with multiple fields
# - Need to update individual fields
# - Need to query by field existence
# - Field count reasonable (< 100)
```

### Q5: Set vs Sorted Set - Khi nào dùng cái nào?

**Trả lời**: Set cho unique collections không cần order, Sorted Set khi cần order hoặc ranking.

**Ví dụ**:
```redis
# Set: Unique items, no order needed
SADD user:1001:liked_posts "post1" "post2" "post3"
SISMEMBER user:1001:liked_posts "post1"  -- Fast O(1) check
SINTER user:1001:liked_posts user:1002:liked_posts  -- Intersection

# Sorted Set: When order matters
ZADD leaderboard 1000 "player1" 2000 "player2" 1500 "player3"

-- Get rankings
ZREVRANGE leaderboard 0 9 WITHSCORES  -- Top 10

-- Get specific player rank
ZREVRANK leaderboard "player1"  -- 2 (0-indexed)

-- Range queries
ZRANGEBYSCORE leaderboard 1000 2000  -- Scores between 1000-2000
```

### Q6: List vs Stream - Khi nào dùng cái nào?

**Trả lời**: List cho simple queues, Stream cho complex event sourcing với multiple consumers.

**Ví dụ**:
```redis
# List: Simple FIFO queue
LPUSH queue:tasks "task1" "task2"
BRPOP queue:tasks 0  -- Blocking pop

# List is good for:
# - Simple job queues
# - Activity feeds (append-only)
# - Known number of producers/consumers

# Stream: Event sourcing, multiple consumers
XADD events:orders "*" user_id "1001" total "150.00"

# Consumer groups for multiple consumers
XGROUP CREATE events:orders:processors group1 0

# Each consumer gets different messages
XREADGROUP GROUP group1 consumer1 STREAMS events:orders ">"

# Acknowledge processing
XACK events:orders:processors group1 message_id

# Stream is good for:
# - Event sourcing
# - Multiple consumers need to process same events
# - Need message acknowledgment
# - Need to track pending messages
```

---

## 3. Performance

### Q7: Làm sao tối ưu performance?

**Trả lời**: Sử dụng pipelines, Lua scripts, và connection pooling.

**Best practices**:

```python
# ✅ Use Pipeline for batch operations
pipe = redis.pipeline()
for key in keys:
    pipe.get(f"user:{key}:profile")
results = pipe.execute()  # Single round trip!

# ✅ Use Lua scripts for atomic operations
SCRIPT = """
local current = redis.call('GET', KEYS[1])
current = tonumber(current) or 0
redis.call('SET', KEYS[1], current + tonumber(ARGV[1]))
return current + tonumber(ARGV[1])
"""
redis.eval(SCRIPT, 1, "counter", 10)

# ✅ Connection pooling
pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50,
    socket_keepalive=True,
    socket_connect_timeout=5
)

# ✅ Use scan instead of keys
cursor = 0
while True:
    cursor, keys = redis.scan(cursor, match='user:*', count=100)
    process_keys(keys)
    if cursor == 0:
        break
```

### Q8: Làm sao handle hot keys?

**Trả lời**: Hot keys có thể become bottleneck. Solutions bao gồm sharding, local caching, và replicas.

**Solutions**:

```python
# Solution 1: Key sharding (client-side)
# Split hot key into multiple keys
hot_key = "popular_item:1001"
shards = ["popular_item:1001:a", "popular_item:1001:b", "popular_item:1001:c"]
shard = hash(user_id) % len(shards)

# Solution 2: Local cache + Redis
local_cache = {}

def get_popular_item():
    item_id = "popular_item:1001"
    
    # Check local cache first
    if item_id in local_cache:
        return local_cache[item_id]
    
    # Get from Redis
    item = redis.get(item_id)
    local_cache[item_id] = item
    
    return item

# Solution 3: Read from replicas
# Direct read traffic to replicas
replica = redis.Replica(host='replica-host')

# Solution 4: Redis Cluster with replicas
# Automatic load distribution
```

### Q9: Memory fragmentation cao thì làm sao?

**Trả lời**: Memory fragmentation xảy ra khi Redis allocate/deallocate memory. Có thể fix bằng MEMORY PURGE hoặc restart.

**Diagnosis và fix**:

```redis
# Check fragmentation ratio
INFO memory
# mem_fragmentation_ratio: 1.45

# Ratio > 1.5 is concerning
# Ratio > 2.0 needs immediate action

# Fix 1: Memory purge (Redis 4.0+)
MEMORY PURGE

# Fix 2: Restart Redis
# This defragments memory completely

# Fix 3: Configure memory allocator
# redis.conf
# memory allocator: jemalloc (default, generally good)
# active-defrag: enable automatic defragmentation
activedefrag yes
active-defrag-ignore-bytes 100mb
active-defrag-threshold-lower 10
active-defrag-threshold-upper 100
```

---

## 4. Persistence

### Q10: RDB vs AOF - Nên dùng cái nào?

**Trả lời**: Recommend dùng cả hai (AOF + RDB) để combine safety và performance.

**So sánh**:

```bash
# redis.conf

# RDB Configuration
save 900 1      # After 1 change in 900 seconds
save 300 10     # After 10 changes in 300 seconds
save 60 10000   # After 10000 changes in 60 seconds

# AOF Configuration
appendonly yes
appendfsync everysec  # Recommended: balance of safety and performance
# appendfsync always   # Safest but slowest
# appendfsync no       # Fastest but risky

# AOF rewrite
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

**Recovery scenarios**:

```bash
# RDB only - up to 5 minutes data loss possible
# AOF only - typically < 1 second data loss with everysec

# Best practice: Both
# - AOF for point-in-time recovery
# - RDB for fast full snapshot backups

# Recovery from AOF
redis-server --appendonly yes
# Redis automatically loads AOF on startup

# Recovery from RDB backup
cp backup-dump.rdb /var/lib/redis/dump.rdb
redis-server
```

### Q11: Backup và restore như thế nào?

**Trả lời**: Sử dụng `BGSAVE` để create backup và `redis-cli` để restore.

**Backup process**:

```bash
# Create background save
redis-cli BGSAVE
# Returns "Background saving started"

# Check save status
redis-cli LASTSAVE
# Returns timestamp of last successful save

# Wait for save to complete
while [ $(redis-cli LASTSAVE) -eq $(redis-cli LASTSAVE) ]; do
    sleep 1
done

# Copy RDB file
cp /var/lib/redis/dump.rdb /backup/dump-$(date +%Y%m%d).rdb

# Or use redis-cli
redis-cli SAVE  # Synchronous save
```

**Restore process**:

```bash
# Stop Redis
redis-cli SHUTDOWN

# Copy backup file
cp /backup/dump-20240115.rdb /var/lib/redis/dump.rdb

# Start Redis
redis-server

# Verify data
redis-cli KEYS "*"
```

---

## 5. Clustering

### Q12: Redis Cluster vs Sentinel - Khi nào dùng cái nào?

**Trả lời**: Cluster cho horizontal scaling và sharding, Sentinel cho high availability với single shard.

**Redis Sentinel - Use when**:
- Need automatic failover
- Single primary + replicas
- Don't need to scale writes horizontally
- Simple setup and management

**Redis Cluster - Use when**:
- Need to scale writes horizontally
- Data larger than single instance
- Multiple shards needed
- Automatic sharding required

**Sentinel setup**:
```bash
# sentinel.conf
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel down-after-milliseconds mymaster 30000
sentinel failover-timeout mymaster 180000
sentinel parallel-syncs mymaster 1

# Start sentinel
redis-sentinel /path/to/sentinel.conf
```

**Cluster setup**:
```bash
# Create cluster
redis-cli --cluster create 127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 \
    --cluster-replicas 1

# Check cluster
redis-cli -p 7000 cluster info

# Assign slots
redis-cli --cluster rebalance 127.0.0.1:7000
```

### Q13: Sharding trong Redis Cluster như thế nào?

**Trả lời**: Redis Cluster tự động shard data sử dụng 16384 slots và CRC16 hash.

**Cách hoạt động**:

```bash
# Key slot calculation
# HASH_SLOT = CRC16(key) mod 16384

# Example in Python:
import crc16

def key_slot(key):
    # CRC16 returns value 0-65535
    crc = crc16.crc16xmodem(key.encode())
    return crc % 16384

# Key "user:1001" → CRC16 = 4432 → Slot = 4432
# Key "user:1002" → CRC16 = 12050 → Slot = 12050
```

**Client handling**:

```python
# Most Redis clients handle MOVED redirects automatically
import redis

# Cluster client handles redirects
r = redis.RedisCluster(
    host='localhost',
    port=7000,
    skip_full_coverage_check=True
)

# This works automatically
r.set("user:1001", "John")
r.get("user:1001")

# MOVED redirect is handled by client
# 127.0.0.1:7002 MOVED 1234 127.0.0.1:7003
```

### Q14: Multi-key operations trong Cluster có được không?

**Trả lời**: Commands operating on multiple keys chỉ được support nếu all keys nằm trong same slot hoặc same node.

**Hạn chế**:

```redis
# ❌ Not supported across slots
SUNION key1 key2  -- Error if different slots
SINTER key1 key2  -- Error if different slots
MGET key1 key2    -- Error if different slots

# ✅ Supported if same slot
# Use hash tags to force same slot
MGET user:1001:profile user:1001:settings  -- Works if tagged
# user:{1001}:profile and user:{1001}:settings
# Both have "1001" as hash tag → same slot

# ✅ Supported if same node (via hash tags)
# {user:1001}:profile {user:1001}:settings

# ✅ Scripts work with same slot keys
EVAL "return redis.call('MGET', KEYS[1], KEYS[2])" 2 \
    user:1001:profile user:1001:settings
```

---

## Liên kết liên quan
- [Redis Glossary](./glossary.md)
- [Redis Architecture](./architecture.md)
- [Redis Best Practices](./best-practice.md)
- [Redis Anti-Patterns](./anti-pattern.md)
- [Redis Checklist](./checklist.md)
- [Redis Decision Tree](./decision-tree.md)
