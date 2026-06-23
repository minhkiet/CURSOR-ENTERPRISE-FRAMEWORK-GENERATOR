# Redis Glossary - Thuật Ngữ Chuyên Ngành

## Mục lục
1. [Data Structures](#1-data-structures)
2. [Operations](#2-operations)
3. [Cluster & HA](#3-cluster--ha)
4. [Persistence & Storage](#4-persistence--storage)
5. [Performance](#5-performance)

---

## String

**Định nghĩa**: String là basic data type trong Redis, có thể chứa any data như text, numbers, hoặc serialized objects. Đây là most versatile và widely used data type.

**Ví dụ**:
```redis
-- Basic string operations
SET user:1001:username "john_doe"
GET user:1001:username

-- Set with expiration (cache pattern)
SET session:abc123 "user_data" EX 3600

-- Multiple values
MSET user:1001:name "John" user:1001:email "john@example.com"
MGET user:1001:name user:1001:email

-- Atomic increment
SET counter 0
INCR counter      -- 1
INCR counter      -- 2
INCRBY counter 10 -- 12
```

---

## Hash

**Định nghĩa**: Hash là field-value pairs collection, tương tự như JSON object hoặc associative array. Perfect cho việc lưu trữ structured objects.

**Ví dụ**:
```redis
-- Store user object
HSET user:1001 name "John Doe" email "john@example.com" age "30"

-- Get single field
HGET user:1001 name

-- Get all fields
HGETALL user:1001

-- Get multiple fields
HMGET user:1001 name email

-- Increment field
HINCRBY user:1001 age 1

-- Check field exists
HEXISTS user:1001 email

-- Delete field
HDEL user:1001 age
```

---

## List

**Định nghĩa**: List là ordered collection of strings, implemented as linked list. Supports push/pop operations ở both ends. Perfect cho message queues và activity logs.

**Ví dụ**:
```redis
-- Add items to list
LPUSH notifications:user:1001 "New order received"
LPUSH notifications:user:1001 "Order shipped"
LPUSH notifications:user:1001 "Order delivered"

-- Get items
LRANGE notifications:user:1001 0 -1  -- All items
LRANGE notifications:user:1001 0 9   -- First 10

-- Pop items
RPOP notifications:user:1001  -- Remove from right
LPOP notifications:user:1001   -- Remove from left

-- List length
LLEN notifications:user:1001

-- Blocking pop (for queues)
BLPOP notifications:queue 0  -- Wait indefinitely
BRPOP notifications:queue 30 -- Wait 30 seconds
```

---

## Set

**Định nghĩa**: Set là unordered collection of unique strings. Operations như intersection, union, và difference được support. Perfect cho tags và unique items.

**Ví dụ**:
```redis
-- Add items to set
SADD product:tags:1001 "electronics" "sale" "new"

-- Get all members
SMEMBERS product:tags:1001

-- Check membership
SISMEMBER product:tags:1001 "electronics"  -- 1

-- Remove item
SREM product:tags:1001 "sale"

-- Set operations
SADD set:a 1 2 3 4
SADD set:b 3 4 5 6
SUNION set:a set:b        -- 1 2 3 4 5 6
SINTER set:a set:b        -- 3 4
SDIFF set:a set:b         -- 1 2

-- Random member
SRANDMEMBER product:tags:1001 2  -- Get 2 random members
```

---

## Sorted Set (ZSET)

**Định nghĩa**: Sorted Set là ordered collection of unique strings với scores. Items được sorted by score. Perfect cho leaderboards, priority queues, và time-series data.

**Ví dụ**:
```redis
-- Add leaderboard entries
ZADD leaderboard:global 1000 "player1" 2000 "player2" 1500 "player3"

-- Get rank (0-indexed)
ZRANK leaderboard:global "player1"   -- 0
ZREVRANK leaderboard:global "player1" -- 2 (highest first)

-- Get score
ZSCORE leaderboard:global "player1"   -- "1000"

-- Get range
ZRANGE leaderboard:global 0 9        -- Top 10 (lowest scores)
ZREVRANGE leaderboard:global 0 9     -- Top 10 (highest scores)

-- Get rank with scores
ZRANGE leaderboard:global 0 9 WITHSCORES

-- Increment score
ZINCRBY leaderboard:global 500 "player1"

-- Count in range
ZCOUNT leaderboard:global 1000 2000
```

---

## Key

**Định nghĩa**: Key là identifier cho любой value trong Redis. Keys được organized bằng namespace pattern (ví dụ: `user:1001:profile`). Supports patterns và expiration.

**Ví dụ**:
```redis
-- Basic key operations
SET mykey "value"
GET mykey
DEL mykey

-- Key patterns
KEYS user:*           -- Find all user keys
SCAN 0 MATCH user:*   -- Safer alternative to KEYS

-- Key metadata
EXISTS mykey          -- Check existence (1 or 0)
TYPE mykey            -- Get value type
TTL mykey             -- Time to live (-1 = no expire, -2 = not exists)

-- Expiration
EXPIRE mykey 3600     -- Set 1 hour TTL
SETEX mykey 3600 "v"  -- Set value with TTL
EXPIREAT mykey 1699900800  -- Set expire at timestamp
PERSIST mykey         -- Remove expiration

-- Rename
RENAME oldkey newkey
RENAMENX oldkey newkey  -- Only if newkey doesn't exist
```

---

## Pub/Sub

**Định nghĩa**: Publish/Subscribe là messaging pattern cho real-time notifications. Publishers gửi messages đến channels, subscribers nhận messages từ channels.

**Ví dụ**:
```redis
-- Subscribe to channel (in redis-cli)
SUBSCRIBE notifications
PSUBSCRIBE notifications:*  -- Pattern subscription

-- Publish message
PUBLISH notifications:user:1001 "You have a new message"
PUBLISH notifications:system "System maintenance scheduled"

-- Check subscriptions
PUBSUB NUMSUB notifications:user:1001

-- Pattern subscriptions
PSUBSCRIBE news.* sports.*
UNSUBSCRIBE notifications
PUNSUBSCRIBE news.*
```

---

## Transaction

**Định nghĩa**: Redis transactions cho phép grouping commands được executed atomically sử dụng MULTI/EXEC. Commands được queued và executed together.

**Ví dụ**:
```redis
-- Start transaction
MULTI

-- Queue commands
SET key1 "value1"
SET key2 "value2"
INCR counter
HSET user:1 name "John"

-- Execute all commands
EXEC

-- Discard queued commands
DISCARD

-- Atomic operations
WATCH user:1  -- Optimistic locking
GET user:1
MULTI
SET user:1:name "Jane"
EXEC  -- Fails if user:1 was modified by another client
```

---

## Pipeline

**Định nghĩa**: Pipeline cho phép batch multiple commands được sent và executed như một network round-trip. Cải thiện performance khi cần execute nhiều commands.

**Ví dụ**:
```redis
-- Multiple commands in pipeline
PIPELINE
GET user:1:name
GET user:1:email
GET user:1:age
INCR page_views
HGETALL user:1:stats
EXEC

-- Pipeline with many commands (client-side)
-- In Python:
pipe = r.pipeline()
pipe.get('key1')
pipe.get('key2')
pipe.get('key3')
results = pipe.execute()
```

---

## Lua Script

**Định nghĩa**: Lua scripts cho phép execute complex operations atomically. Scripts được executed in a single step, perfect cho operations cần atomicity beyond transactions.

**Ví dụ**:
```redis
-- Simple Lua script
EVAL "return redis.call('GET', KEYS[1])" 1 mykey

-- Script with arguments
EVAL "
  local current = redis.call('GET', KEYS[1])
  current = tonumber(current) or 0
  redis.call('SET', KEYS[1], current + tonumber(ARGV[1]))
  return redis.call('GET', KEYS[1])
" 1 counter 10

-- Script for distributed lock
EVAL "
  if redis.call('SET', KEYS[1], ARGV[1], 'NX', 'EX', ARGV[2]) then
    return 1
  else
    return 0
  end
" 1 lock:resource1 "unique_id" 30

-- Cache compiled script
SCRIPT LOAD "return redis.call('GET', KEYS[1])"
-- Returns script SHA
-- Then use EVALSHA with SHA
```

---

## Persistence

**Định nghĩa**: Redis hỗ trợ multiple persistence options: RDB (point-in-time snapshots) và AOF (append-only file). Có thể sử dụng cả hai hoặc không có persistence (pure cache).

**Ví dụ**:
```redis
-- Configuration in redis.conf:
-- save 900 1    -- RDB: after 1 change in 900 seconds
-- save 300 10   -- RDB: after 10 changes in 300 seconds
-- save 60 10000 -- RDB: after 10000 changes in 60 seconds

-- Manual operations
BGSAVE       -- Background save
SAVE         -- Synchronous save (blocks)

-- AOF configuration
-- appendonly yes
-- appendfsync everysec  -- (always, everysec, no)

-- Rewrite AOF
BGREWRITEAOF

-- Check last save info
LASTSAVE
```

---

## Cluster

**Định nghĩa**: Redis Cluster cung cấp automatic sharding và high availability. Data được partitioned across multiple nodes với replication.

**Ví dụ**:
```redis
-- Cluster info (redis-cli --cluster)
CLUSTER INFO

-- Node operations
CLUSTER NODES
CLUSTER MEET 192.168.1.2 6379
CLUSTER FORGET node_id
CLUSTER REPLICATE node_id

-- Slot assignment
CLUSTER ADDSLOTS 0 1 2 3
CLUSTER DELSLOTS 0 1 2 3
CLUSTER SETSLOT 0 IMPORTING source_node_id
CLUSTER SETSLOT 0 MIGRATING target_node_id
CLUSTER SETSLOT 0 NODE node_id

-- Key slot
CLUSTER KEYSLOT mykey

-- Failover
CLUSTER FAILOVER
CLUSTER FAILOVER FORCE
```

---

## Sentinel

**Định nghĩa**: Redis Sentinel provides high availability monitoring và automatic failover cho standalone Redis hoặc master-slave setups.

**Ví dụ**:
```redis
-- Sentinel commands
INFO SENTINEL
SENTINEL masters
SENTINEL master mymaster
SENTINEL slaves mymaster
SENTINEL get-master-addr-by-name mymaster

-- Failover
SENTINEL failover mymaster

-- Configuration
-- sentinel.conf:
-- sentinel monitor mymaster 127.0.0.1 6379 2
-- sentinel down-after-milliseconds mymaster 30000
-- sentinel failover-timeout mymaster 180000
```

---

## Memory

**Định nghĩa**: Redis lưu trữ data in-memory nhưng có thể evict data khi memory limit reached. Multiple eviction policies available.

**Ví dụ**:
```redis
-- Memory info
INFO memory
MEMORY STATS
MEMORY USAGE mykey

-- Set memory limit
CONFIG SET maxmemory 2gb
CONFIG SET maxmemory-policy allkeys-lru

-- Eviction policies:
-- noeviction: Return error when memory limit reached
-- allkeys-lru: Evict least recently used keys
-- allkeys-lfu: Evict least frequently used keys
-- volatile-lru: Evict LRU among keys with TTL
-- volatile-lfu: Evict LFU among keys with TTL
-- allkeys-random: Evict random keys
-- volatile-random: Evict random among keys with TTL
-- volatile-ttl: Evict keys with shortest TTL

-- Lazy freeing
UNLINK key1 key2  -- Async deletion
```

---

## Scan

**Định nghĩa**: SCAN là cursor-based iterator cho việc iterate through keys một cách non-blocking. An toàn hơn KEYS command cho production.

**Ví dụ**:
```redis
-- Iterate all keys
SCAN 0              -- Returns cursor and keys
SCAN 0 COUNT 100    -- Hint to return 100 keys per iteration
SCAN 0 MATCH user:* -- Pattern match

-- Cursor-based iteration
-- In Python:
cursor = 0
while True:
    cursor, keys = r.scan(cursor, match='user:*', count=100)
    process_keys(keys)
    if cursor == 0:
        break

-- SSCAN, HSCAN, ZSCAN for specific data types
SSCAN myset 0 COUNT 100
HSCAN myhash 0 MATCH field:*
ZSCAN myzset 0
```

---

## Bitmap

**Định nghĩa**: Bitmap là string treated as array of bits. Efficient cho tracking binary states như user activity, daily logins, hoặc flags.

**Ví dụ**:
```redis
-- Set bit at position
SETBIT user:login:2024:01:15 1001 1

-- Get bit at position
GETBIT user:login:2024:01:15 1001

-- Count set bits (daily active users)
BITCOUNT user:login:2024:01:15

-- Bitwise operations
SETBIT activity:a 0 1
SETBIT activity:a 1 0
SETBIT activity:b 0 1
SETBIT activity:b 2 1
BITOP AND activity:ab activity:a activity:b

-- Find first set bit
BITPOS activity:a 1
```

---

## HyperLogLog

**Định nghĩa**: HyperLogLog là probabilistic data structure cho cardinality estimation. Sử dụng minimal memory để estimate unique count của large datasets.

**Ví dụ**:
```redis
-- Add items to HyperLogLog
PFADD unique_visitors:daily "user1" "user2" "user3"
PFADD unique_visitors:daily "user4"

-- Get estimated count
PFCOUNT unique_visitors:daily

-- Merge multiple HyperLogLogs
PFADD campaign:week:1 "user1" "user2"
PFADD campaign:week:2 "user2" "user3"
PFADD campaign:week:3 "user3" "user4"
PFMERGE campaign:total campaign:week:1 campaign:week:2 campaign:week:3
PFCOUNT campaign:total
```

---

## Geospatial

**Định nghĩa**: Geospatial indexes store geographic coordinates và support location-based queries như finding nearby places hoặc distance between locations.

**Ví dụ**:
```redis
-- Add locations
GEOADD stores:us -122.4194 37.7749 "store:sanfrancisco"
GEOADD stores:us -118.2437 34.0522 "store:losangeles"
GEOADD stores:us -74.0060 40.7128 "store:newyork"

-- Get coordinates
GEOPOS stores:us store:sanfrancisco

-- Distance between locations
GEODIST stores:us store:sanfrancisco store:losangeles km

-- Find nearby places
GEORADIUS stores:us -122.4194 37.7749 100 km WITHDIST ASC COUNT 10
GEOSEARCH stores:us FROMLONLAT -122.4194 37.7749 BYRADIUS 100 km ASC

-- Store members in geo
GEOADD users:location -122.4194 37.7749 "user:1001"
```

---

## Stream

**Định nghĩa**: Stream là log-structured data structure hỗ trợ multiple consumers và consumer groups. Perfect cho event sourcing, messaging, và activity logs.

**Ví dụ**:
```redis
-- Add to stream
XADD events:orders "*" user_id "1001" total "150.00"
XADD events:orders "*" user_id "1002" total "200.00"

-- Read from stream
XRANGE events:orders - + COUNT 10
XREAD STREAMS events:orders $

-- Consumer groups
XGROUP CREATE events:orders:processors group1 0
XREADGROUP GROUP group1 consumer1 STREAMS events:orders ">"

-- Acknowledge processing
XACK events:orders:processors group1 message_id

-- Pending entries
XPENDING events:orders:processors group1

-- Consumer info
XINFO GROUPS events:orders
```

---

## Liên kết liên quan
- [Redis Architecture](./architecture.md)
- [Redis Best Practices](./best-practice.md)
- [Redis Anti-Patterns](./anti-pattern.md)
- [Redis Checklist](./checklist.md)
- [Redis FAQ](./faq.md)
- [Redis Decision Tree](./decision-tree.md)
