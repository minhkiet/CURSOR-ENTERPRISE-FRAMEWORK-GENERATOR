# Redis Architecture - Kiến Trúc Chi Tiết

## Mục lục
1. [Tổng quan Kiến trúc](#1-tổng-quan-kiến-trúc)
2. [Data Structures](#2-data-structures)
3. [Memory Management](#3-memory-management)
4. [Persistence](#4-persistence)
5. [Replication & Clustering](#5-replication--clustering)

---

## 1. Tổng quan Kiến trúc

### 1.1 Redis Overview

Redis là in-memory data structure store được sử dụng như database, cache, message broker, và streaming engine. Nó cung cấp sub-millisecond latency với high throughput.

Core features:
- **In-Memory Storage**: Data được lưu trong RAM
- **Rich Data Structures**: String, Hash, List, Set, Sorted Set, Bitmap, HyperLogLog, Geospatial, Stream
- **Persistence**: Optional disk storage với RDB và AOF
- **Replication**: Master-slave replication
- **Clustering**: Horizontal scaling với automatic sharding
- **High Availability**: Sentinel cho failover
- **Lua Scripting**: Atomic script execution

### 1.2 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                      REDIS ARCHITECTURE                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      CLIENT LAYER                             │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │   │
│  │  │ Python  │  │   Node  │  │   Go    │  │  Java  │       │   │
│  │  │redis-py│  │  ioredis │  │ go-redis│  │ Lettuce│       │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │   │
│  └────────┼──────────┼──────────┼──────────┼──────────────┘   │
│           │          │          │          │                     │
│           └──────────┴──────────┴──────────┘                     │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   NETWORK LAYER                               │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │              Event Loop (ae_evloop)                   │  │   │
│  │  │  - I/O multiplexing (epoll/select/kqueue)         │  │   │
│  │  │  - Non-blocking I/O                               │  │   │
│  │  │  - Connection handling                             │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      CORE LAYER                               │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │              Command Parser & Dispatcher             │  │   │
│  │  │  - Parse Redis protocol                            │  │   │
│  │  │  - Route to command handlers                       │  │   │
│  │  │  - Command validation                              │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                           │                                │   │
│  │                           ▼                                │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │              Data Structure Layer                    │  │   │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │  │   │
│  │  │  │  String │ │   Hash  │ │   List  │ │   Set   │  │  │   │
│  │  │  │  Object │ │  Object │ │  Object │ │  Object │  │  │   │
│  │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │  │   │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │  │   │
│  │  │  │  ZSet   │ │  Stream │ │  Geo    │ │HyperLog │  │  │   │
│  │  │  │  Object │ │  Object │ │  Object │ │   Log   │  │  │   │
│  │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                           │                                │   │
│  │                           ▼                                │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │              Memory Management Layer                  │  │   │
│  │  │  - Memory allocation (jemalloc/tcmalloc)           │  │   │
│  │  │  - Eviction policies                                │  │   │
│  │  │  - Memory profiling                                 │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    PERSISTENCE LAYER                         │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │                    RDB Snapshot                       │  │   │
│  │  │  - Point-in-time snapshots                          │  │   │
│  │  │  - Background save (fork)                          │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                           │                                │   │
│  │                           ▼                                │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │                    AOF (Append Only File)              │  │   │
│  │  │  - Command log                                     │  │   │
│  │  │  - fsync policies                                  │  │   │
│  │  │  - Rewrite/compaction                              │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Structures

### 2.1 Internal Object Encoding

```
┌─────────────────────────────────────────────────────────────────────┐
│                    REDIS OBJECT ENCODING                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    STRING Object                              │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │  embstr (<= 44 bytes)                               │  │   │
│  │  │  - Embedded string in redisObject                   │  │   │
│  │  │  - Single allocation                                │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                           │                                │   │
│  │                           ▼                                │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │  raw (> 44 bytes)                                   │  │   │
│  │  │  - Simple dynamic string (sds)                      │  │   │
│  │  │  - Separate allocation                             │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                           │                                │   │
│  │                           ▼                                │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │  int                                                 │  │   │
│  │  │  - Integer stored directly                          │  │   │
│  │  │  - For numeric strings                              │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    COLLECTION Objects                        │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │  LIST: quicklist                                     │  │   │
│  │  │  - Linked list of ziplists                          │  │   │
│  │  │  - O(1) push/pop at both ends                       │  │   │
│  │  │  - Memory efficient for small lists                 │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                           │                                │   │
│  │                           ▼                                │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │  HASH: ziplist (< 512 items, each < 64 bytes)       │  │   │
│  │  │  HASH: hashtable (otherwise)                        │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                           │                                │   │
│  │                           ▼                                │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │  SET: intset (all integers)                        │  │   │
│  │  │  SET: hashtable (otherwise)                        │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                           │                                │   │
│  │                           ▼                                │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │  ZSET: ziplist (< 128 items)                       │  │   │
│  │  │  ZSET: skiplist + hashtable (otherwise)             │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Memory Management

### 3.1 Memory Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    REDIS MEMORY MANAGEMENT                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   PROCESS MEMORY                            │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │              Redis Resident Set                       │  │   │
│  │  │  ┌───────────────────────────────────────────────┐ │  │   │
│  │  │  │              Data Base                        │ │  │   │
│  │  │  │  ┌─────────────────────────────────────────┐ │ │  │   │
│  │  │  │  │  Keys (hashtable)                      │ │ │  │   │
│  │  │  │  │  - Key pointers                        │ │ │  │   │
│  │  │  │  │  - Key names                           │ │ │  │   │
│  │  │  │  └─────────────────────────────────────────┘ │ │  │   │
│  │  │  │  ┌─────────────────────────────────────────┐ │ │  │   │
│  │  │  │  │  Values (data structures)               │ │ │  │   │
│  │  │  │  │  - Strings                             │ │ │  │   │
│  │  │  │  │  - Collections                         │ │ │  │   │
│  │  │  │  └─────────────────────────────────────────┘ │ │  │   │
│  │  │  └───────────────────────────────────────────────┘ │  │   │
│  │  │                                                      │  │   │
│  │  │  ┌───────────────────────────────────────────────┐ │  │   │
│  │  │  │              Overhead                           │ │  │   │
│  │  │  │  - Object metadata (16 bytes)                 │ │  │   │
│  │  │  │  - Hashtable entries                         │ │  │   │
│  │  │  │  - Redis Cluster slots                       │ │  │   │
│  │  │  └───────────────────────────────────────────────┘ │  │   │
│  │  │                                                      │  │   │
│  │  │  ┌───────────────────────────────────────────────┐ │  │   │
│  │  │  │              Fragmentation                     │ │  │   │
│  │  │  │  - Memory fragmentation                      │ │  │   │
│  │  │  │  - Can be reclaimed with MEMORY PURGE        │ │  │   │
│  │  │  └───────────────────────────────────────────────┘ │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   EVICTION POLICIES                         │   │
│  │                                                             │   │
│  │  noeviction       → Return error on write                   │   │
│  │  allkeys-lru      → Evict LRU keys globally                 │   │
│  │  allkeys-lfu      → Evict LFU keys globally                 │   │
│  │  allkeys-random   → Evict random keys globally             │   │
│  │  volatile-lru     → Evict LRU among TTL keys               │   │
│  │  volatile-lfu     → Evict LFU among TTL keys               │   │
│  │  volatile-random  → Evict random among TTL keys            │   │
│  │  volatile-ttl     → Evict shortest TTL keys                │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 4. Persistence

### 4.1 RDB Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RDB PERSISTENCE                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   BGSAVE Process                             │   │
│  │                                                             │   │
│  │  Parent Process ───fork()──→ Child Process                 │   │
│  │                                                             │   │
│  │  Parent:                    Child:                          │   │
│  │  - Continue serving        - Create RDB file                │   │
│  │    requests               - Iterate all keys               │   │
│  │  - Monitor child          - Write to temp file             │   │
│  │                          - Rename temp file                │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   RDB File Format                            │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │  MAGIC: "REDIS0009"                                  │  │   │
│  │  │  Version: 4 bytes                                   │  │   │
│  │  │  Auxiliary fields (version, etc.)                   │  │   │
│  │  │  Database 0:                                        │  │   │
│  │  │    SELECTDB                                         │  │   │
│  │  │    Key-Value pairs...                               │  │   │
│  │  │  Database 1:                                        │  │   │
│  │  │    ...                                              │  │   │
│  │  │  EOF: 0xFF                                         │  │   │
│  │  │  CRC64 checksum                                    │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  Configuration:                                                       │
│  - save 900 1     (after 1 write in 900s)                          │
│  - save 300 10    (after 10 writes in 300s)                        │
│  - save 60 10000  (after 10000 writes in 60s)                      │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 4.2 AOF Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AOF PERSISTENCE                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   Write Operations                           │   │
│  │                                                             │   │
│  │  Client ──→ Command ──→ AOF Buffer ──→ AOF File            │   │
│  │                                │                             │   │
│  │                                ▼                             │   │
│  │                    fsync to disk                            │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  fsync policies:                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  appendfsync always                                          │   │
│  │  - fsync after every write                                  │   │
│  │  - Safest, slowest                                          │   │
│  │                                                             │   │
│  │  appendfsync everysec (default)                             │   │
│  │  - fsync once per second                                   │   │
│  │  - Good balance of safety and performance                  │   │
│  │                                                             │   │
│  │  appendfsync no                                             │   │
│  │  - Let OS handle fsync                                     │   │
│  │  - Fastest, least safe                                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   AOF Rewrite                                │   │
│  │                                                             │   │
│  │  BGREWRITEAOF:                                             │   │
│  │  - Creates new AOF with minimal operations                 │   │
│  │  - Compacts redundant operations                           │   │
│  │  - SET a 1, SET a 2, SET a 3 → SET a 3                   │   │
│  │                                                             │   │
│  │  Example:                                                   │   │
│  │  Before:         After:                                     │   │
│  │  SET key v1      SET key v3                                 │   │
│  │  SET key v2                                               │   │
│  │  SET key v3                                               │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 5. Replication & Clustering

### 5.1 Replication Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MASTER-SLAVE REPLICATION                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌───────────────────┐                                            │
│  │      MASTER       │                                            │
│  │                   │                                            │
│  │  ┌─────────────┐  │                                            │
│  │  │   Master    │  │                                            │
│  │  │   Repl Buf  │  │◄── Replication buffer                     │
│  │  └─────────────┘  │                                            │
│  │         │         │                                            │
│  │         ▼         │                                            │
│  │  ┌─────────────┐  │                                            │
│  │  │   Commands  │──┼──────────────────────────────────────┐   │
│  │  └─────────────┘  │                                      │   │
│  │                   │                                      │   │
│  └───────────────────┘                                      │   │
│                                                              │   │
│                          ┌──────────────────────────────────┘   │
│                          │                                       │
│                          ▼                                       │
│  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐
│  │      SLAVE 1      │  │      SLAVE 2      │  │      SLAVE N      │
│  │                   │  │                   │  │                   │
│  │  ┌─────────────┐  │  │  ┌─────────────┐  │  │  ┌─────────────┐  │
│  │  │  Repl Backlog│  │  │  │  Repl Backlog│  │  │  │  Repl Backlog│  │
│  │  └─────────────┘  │  │  └─────────────┘  │  │  └─────────────┘  │
│  │         │         │  │         │         │  │         │         │
│  │         ▼         │  │         ▼         │  │         ▼         │
│  │  ┌─────────────┐  │  │  ┌─────────────┐  │  │  ┌─────────────┐  │
│  │  │ PSYNC/RDB   │  │  │  │ PSYNC/RDB   │  │  │  │ PSYNC/RDB   │  │
│  │  │   Buffer    │  │  │  │   Buffer    │  │  │  │   Buffer    │  │
│  │  └─────────────┘  │  │  └─────────────┘  │  │  └─────────────┘  │
│  │                   │  │                   │  │                   │
│  └───────────────────┘  └───────────────────┘  └───────────────────┘
│                                                                      │
│  Replication Flow:                                                   │
│  1. Slave connects to master (REPLCONF)                             │
│  2. Master starts BGSAVE with REPLICAOF or REPLICATIONID offset     │
│  3. Master sends RDB file to slave                                  │
│  4. Master streams incremental commands via PING/PUBLISH            │
│  5. Slave applies commands locally                                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 5.2 Redis Cluster Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    REDIS CLUSTER                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   CLUSTER OVERVIEW                           │   │
│  │                                                             │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │   │
│  │  │ Node 1  │ │ Node 2  │ │ Node 3  │ │ Node 4  │         │   │
│  │  │Master A │ │Master B │ │Master C │ │Master A │         │   │
│  │  │(Slots   │ │(Slots   │ │(Slots   │ │(Replica)│         │   │
│  │  │0-5460) │ │5461-    │ │10923-   │ │         │         │   │
│  │  │         │ │10922)  │ │16383)  │ │         │         │   │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘         │   │
│  │       │           │           │           │               │   │
│  │       └───────────┴───────────┴───────────┘               │   │
│  │                        │                                   │   │
│  │              Cluster Bus (Gossip Protocol)                 │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   SLOT DISTRIBUTION                         │   │
│  │                                                             │   │
│  │  Total: 16384 slots (0-16383)                              │   │
│  │                                                             │   │
│  │  Slot calculation:                                          │   │
│  │  HASH_SLOT = CRC16(key) mod 16384                          │   │
│  │                                                             │   │
│  │  Example:                                                   │   │
│  │  Key "user:1001" → CRC16 = 4432 → Slot = 4432 mod 16384   │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   FAILOVER PROCESS                           │   │
│  │                                                             │   │
│  │  1. Master fails (detected via gossip)                      │   │
│  │  2. Replica promotes itself (slave of failed master)       │   │
│  │  3. Cluster updates slot mapping                            │   │
│  │  4. Other nodes redirect clients                           │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Liên kết liên quan
- [Redis Glossary](./glossary.md)
- [Redis Best Practices](./best-practice.md)
- [Redis Anti-Patterns](./anti-pattern.md)
- [Redis Checklist](./checklist.md)
- [Redis FAQ](./faq.md)
- [Redis Decision Tree](./decision-tree.md)
