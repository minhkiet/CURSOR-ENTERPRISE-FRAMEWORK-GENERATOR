# Redis Decision Tree - Cây Quyết Định

## Mục lục
1. [Data Type Selection](#1-data-type-selection)
2. [Key Design](#2-key-design)
3. [Performance Optimization](#3-performance-optimization)
4. [Caching Strategy](#4-caching-strategy)
5. [High Availability](#5-high-availability)

---

## 1. Data Type Selection

```
BẮT ĐẦU: Chọn data type cho use case
              │
              ▼
┌─────────────────────────────────────────┐
│  Cần lưu trữ simple value?             │
│  (string, number, serialized object)    │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│   STRING      │
│               │
│ Get/Set simple│
│ values        │
└───────────────┘
        │
        ▼
    KẾT THÚC
```

```
TIẾP TỤC: Chọn data type
              │
              ▼
┌─────────────────────────────────────────┐
│  Data có multiple fields?               │
│  (object với properties)               │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│    HASH      │
│               │
│ Store object │
│ with fields   │
└───────────────┘
        │
        ▼
    KẾT THÚC
```

```
TIẾP TỤC: Chọn data type
              │
              ▼
┌─────────────────────────────────────────┐
│  Cần uniqueness?                       │
│  (mỗi value chỉ xuất hiện 1 lần)       │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│   Cần order  │
│   hoặc score?│
└───────────────┘
        │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐┌───────────────┐
│  SORTED SET  ││     SET       │
│              ││               │
│ Leaderboard, ││ Unique items  │
│ rankings,    ││ Tags, likes   │
│ time-series  ││               │
└───────────────┘└───────────────┘
        │            │
        └──────┬─────┘
               ▼
           KẾT THÚC
```

```
TIẾP TỤC: Chọn data type
              │
              ▼
┌─────────────────────────────────────────┐
│  Cần ordered collection?               │
│  (FIFO queue, activity feed)           │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  Cần multi-  │
│  consumer     │
│  support?     │
└───────────────┘
        │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐┌───────────────┐
│    STREAM     ││     LIST      │
│               ││               │
│ Event         ││ Queue, feed   │
│ sourcing,     ││ FIFO order    │
│ multi-        ││ LPUSH/RPOP   │
│ consumer      ││ or RPUSH/LPOP │
└───────────────┘└───────────────┘
        │            │
        └──────┬─────┘
               ▼
           KẾT THÚC
```

---

## 2. Key Design

```
BẮT ĐẦU: Thiết kế key name
              │
              ▼
┌─────────────────────────────────────────┐
│  Key có relationship?                  │
│  (e.g., user:1001:profile)             │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  Sử dụng    │
│  hierarchical │
│  naming      │
│               │
│ namespace:   │
│ entity:id:   │
│ field        │
└───────────────┘
```

```
TIẾP TỤC: Thiết kế key name
              │
              ▼
┌─────────────────────────────────────────┐
│  Key có expiration?                    │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  Cache key   │
│  → SETEX     │
│  hoặc EXPIRE │
│               │
│ TTL patterns:│
│ • Session    │
│   24h       │
│ • Cache     │
│   5-15min  │
│ • Token     │
│   1-24h    │
└───────────────┘
```

```
TIẾP TỤC: Thiết kế key name
              │
              ▼
┌─────────────────────────────────────────┐
│  Key name length?                      │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
      LONG        SHORT
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  Cân nhắc     │
│  abbreviation │
│               │
│ Balance:     │
│ • Readability│
│ • Memory     │
│ • Frequency  │
└───────────────┘
```

---

## 3. Performance Optimization

```
BẮT ĐẦU: Tối ưu performance
              │
              ▼
┌─────────────────────────────────────────┐
│  Multiple commands?                      │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  Sử dụng     │
│  PIPELINE    │
│               │
│ batch multiple│
│ commands in   │
│ single RTT    │
└───────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Commands cần atomicity?                │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐  Tiếp tục ↓
│  Sử dụng    │
│  LUA SCRIPT  │
│               │
│ Atomic multi- │
│ command ops   │
└───────────────┘
```

```
TIẾP TỤC: Performance optimization
              │
              ▼
┌─────────────────────────────────────────┐
│  Connection pattern?                    │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       NEW        REUSE
        │            │
        ▼            ▼
┌───────────────┐┌───────────────┐
│  Sử dụng     ││  Connection   │
│  connection   ││  POOL        │
│  pool!        ││               │
│               ││ Configure:   │
│ Single        ││ • max_conns  │
│ connection    ││ • timeout    │
│ per request  ││ • keepalive  │
│ = BAD!        ││ • reuse      │
└───────────────┘└───────────────┘
        │
        └──────┬─────┘
               ▼
           KẾT THÚC
```

```
PERFORMANCE ISSUE RESOLUTION:
              │
              ▼
┌─────────────────────────────────────────┐
│  Issue type?                            │
└─────────────────────────────────────────┘
              │
    ┌────┬────┬────┬────┐
    ▼    ▼    ▼    ▼    ▼
 HIGH   LAT  MEM  KEYS  CONNECT
 LAT   ENCY ORY  BLOCK
    │    │    │    │    │
    ▼    ▼    ▼    ▼    ▼
┌──────┐┌───┐┌────┐┌────┐┌─────────┐
│Reduce││Pipe││Evic││SCAN││Increase │
│calls ││line││tion││not││pool size│
│cache ││batch││policy││KEYS ││         │
│local ││    ││monitor││  ││tune     │
└──────┘└───┘└────┘└────┘└─────────┘
```

---

## 4. Caching Strategy

```
BẮT ĐẦU: Chọn caching pattern
              │
              ▼
┌─────────────────────────────────────────┐
│  Consistency requirement?               │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
      HIGH         LOW
        │            │
        ▼            ▼
┌───────────────┐┌───────────────┐
│ WRITE-THROUGH ││  CACHE-ASIDE │
│               ││               │
│ Write to DB  ││ Read: cache   │
│ + cache      ││ miss → DB →   │
│ simultaneously││ cache        │
│               ││               │
│ Strong       ││ Write: DB →   │
│ consistency  ││ invalidate    │
│ Slower writes││ cache         │
└───────────────┘└───────────────┘
        │            │
        └──────┬─────┘
               ▼
┌─────────────────────────────────────────┐
│  Need cache stampede protection?        │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐┌───────────────┐
│   ADD LOCK    ││    DONE       │
│               ││               │
│ Distributed   ││               │
│ lock when     ││               │
│ rebuilding    ││               │
│ cache         ││               │
│               ││               │
│ Or: Prob.     ││               │
│ early exp.    ││               │
└───────────────┘└───────────────┘
```

---

## 5. High Availability

```
BẮT ĐẦU: Chọn HA solution
              │
              ▼
┌─────────────────────────────────────────┐
│  Cần scale writes horizontally?         │
│  (data > single instance)              │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
       YES          NO
        │            │
        ▼            ▼
┌───────────────┐┌───────────────┐
│REDIS CLUSTER  ││REDIS SENTINEL │
│               ││               │
│• Auto shard   ││• Failover     │
│• 16384 slots ││• Monitoring   │
│• Multi-node  ││• 1 master     │
│• Built-in    ││  + replicas   │
│  replication ││               │
│               ││Simpler       │
│Complex setup ││setup          │
└───────────────┘└───────────────┘
        │            │
        └──────┬─────┘
               ▼
┌─────────────────────────────────────────┐
│  Persistence requirement?               │
└─────────────────────────────────────────┘
              │
        ┌─────┴─────┐
      HIGH         LOW
        │            │
        ▼            ▼
┌───────────────┐┌───────────────┐
│   AOF only    ││   RDB only    │
│               ││               │
│ appendfsync   ││ Periodic      │
│ everysec     ││ snapshots     │
│               ││               │
│ + Periodic    ││Less durable   │
│ RDB backups  ││Faster writes │
└───────────────┘└───────────────┘
        │
        └──────┬─────┘
               ▼
           KẾT THÚC
```

---

## Summary Decision Tree

```
REDIS DECISION FLOW:
              │
              ▼
┌─────────────────────────────────────────┐
│           START HERE                     │
└─────────────────────────────────────────┘
              │
              ▼
    ┌─────────────────┐
    │  Data Type?     │
    │  String/Hash/   │
    │  List/Set/ZSet/ │
    │  Stream         │
    └────────┬────────┘
              │
              ▼
    ┌─────────────────┐
    │  Key Design?    │
    │  Namespaces/    │
    │  TTL/Patterns   │
    └────────┬────────┘
              │
              ▼
    ┌─────────────────┐
    │  Performance?   │
    │  Pipeline/Lua/  │
    │  Connection Pool│
    └────────┬────────┘
              │
              ▼
    ┌─────────────────┐
    │  Caching?       │
    │  Cache-aside/   │
    │  Write-through  │
    └────────┬────────┘
              │
              ▼
    ┌─────────────────┐
    │  HA?            │
    │  Sentinel/      │
    │  Cluster        │
    └─────────────────┘
```

---

## Data Type Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA TYPE SELECTION                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  STRING → Simple values, counters, serialized data          │
│  HASH   → Objects with multiple fields                      │
│  LIST   → Queues, ordered collections (FIFO)                │
│  SET    → Unique items, membership, set operations          │
│  ZSET   → Rankings, leaderboards, time-series               │
│  STREAM → Event sourcing, multi-consumer messaging          │
│  GEO    → Location-based queries                            │
│  BITMAP → Activity tracking, flags, counters               │
│  HYPERLOGLOG → Unique visitor counting                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Liên kết liên quan
- [Redis Glossary](./glossary.md)
- [Redis Architecture](./architecture.md)
- [Redis Best Practices](./best-practice.md)
- [Redis Anti-Patterns](./anti-pattern.md)
- [Redis Checklist](./checklist.md)
- [Redis FAQ](./faq.md)
