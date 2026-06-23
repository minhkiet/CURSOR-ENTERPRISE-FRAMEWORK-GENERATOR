# Redis Checklist - Danh Sách Kiểm Tra

## Mục lục
1. [Project Setup](#1-project-setup)
2. [Key Design](#2-key-design)
3. [Data Types](#3-data-types)
4. [Caching Patterns](#4-caching-patterns)
5. [Performance](#5-performance)
6. [Security](#6-security)
7. [Monitoring](#7-monitoring)

---

## 1. Project Setup

### Basic Configuration

- [ ] Redis version is recent (7.0+)
- [ ] `redis.conf` configured appropriately:
  - `maxmemory` set appropriately
  - `maxmemory-policy` configured
  - `maxclients` set for expected load
  - `tcp-backlog` increased for high concurrency
  - `timeout` set to disconnect idle clients
- [ ] Memory allocation tuned
  - `maxmemory` = 50-70% of available RAM
  - `maxmemory-policy` = appropriate eviction policy
- [ ] Logging configured
  - `loglevel` set appropriately
  - `logfile` specified

### Installation

- [ ] Installed from official packages
- [ ] Configuration file backed up
- [ ] Service configured for auto-start
- [ ] Firewall configured
- [ ] Backup strategy defined

---

## 2. Key Design

### Naming Conventions

- [ ] Keys follow consistent naming pattern
- [ ] Namespaces used (e.g., `user:`, `cache:`, `session:`)
- [ ] Key names are descriptive
- [ ] Hierarchy reflects data relationships
- [ ] Abbreviations documented if used

### Expiration Strategy

- [ ] All cache keys have TTL set
- [ ] Session keys have appropriate expiration
- [ ] TTL values are appropriate for data freshness
- [ ] Permanent data doesn't have keys without TTL

### Key Patterns

- [ ] Pattern used for related keys
- [ ] Index keys maintained for search patterns
- [ ] Lock keys use proper TTL
- [ ] Temporary keys cleaned up properly

---

## 3. Data Types

### String Usage

- [ ] Used for simple key-value pairs
- [ ] Not used for complex objects (use Hash)
- [ ] Serialization format documented
- [ ] Large values compressed if needed

### Hash Usage

- [ ] Used for structured objects
- [ ] Field count reasonable (< 100)
- [ ] Individual field access needed
- [ ] Hash encoding optimized (ziplist vs hashtable)

### List Usage

- [ ] Used for queues and ordered data
- [ ] Not used when random access needed
- [ ] Maximum length controlled with LTRIM
- [ ] Blocking operations use BLPOP/BRPOP

### Set Usage

- [ ] Used for unique collections
- [ ] Set operations needed (SINTER, SUNION)
- [ ] Membership checking required
- [ ] Cardinality reasonable

### Sorted Set Usage

- [ ] Used for rankings/leaderboards
- [ ] Used for time-series data
- [ ] Score updates needed
- [ ] Range queries required

---

## 4. Caching Patterns

### Cache-Aside

- [ ] Application checks cache first
- [ ] Falls back to database on miss
- [ ] Populates cache after database read
- [ ] Invalidates cache on writes

### Write Patterns

- [ ] Write-through used where consistency critical
- [ ] Write-behind used where performance prioritized
- [ ] Cache invalidation strategy defined
- [ ] Dual-writes handled properly

### Cache Stampede

- [ ] Lock mechanism in place for cache rebuilds
- [ ] Probabilistic early expiration considered
- [ ] Background refresh for critical caches

### TTL Management

- [ ] Cache keys have appropriate TTL
- [ ] TTL varies by data freshness requirements
- [ ] TTL documented in code
- [ ] Default TTL defined centrally

---

## 5. Performance

### Connection Management

- [ ] Connection pooling configured
- [ ] Connection pool size appropriate
- [ ] Pool exhaustion handled
- [ ] Long connections reused

### Batch Operations

- [ ] Pipelines used for multiple commands
- [ ] Lua scripts for atomic operations
- [ ] MULTI/EXEC for transactions
- [ ] Number of commands per pipeline reasonable

### Query Patterns

- [ ] SCAN used instead of KEYS
- [ ] Wildcards don't match too many keys
- [ ] Hot keys identified and optimized
- [ ] Big keys identified and split

### Memory Optimization

- [ ] Memory usage monitored
- [ ] Memory fragmentation controlled
- [ ] Eviction policy appropriate
- [ ] Large values compressed

### Operations

- [ ] Pipelining for batch operations
- [ ] Lua scripts for atomic operations
- [ ] Pipeline size reasonable
- [ ] Connection timeout configured

---

## 6. Security

### Authentication

- [ ] Password authentication enabled
- [ ] Strong password used
- [ ] AUTH required for all connections
- [ ] Password rotation policy in place

### Network Security

- [ ] Redis bound to internal IPs only
- [ ] Firewall rules configured
- [ ] Protected mode enabled
- [ ] TLS configured for external access

### Command Security

- [ ] Dangerous commands renamed
- [ ] FLUSHDB/FLUSHALL protected
- [ ] CONFIG protected
- [ ] DEBUG disabled in production

### Data Security

- [ ] Sensitive data encrypted
- [ ] Passwords hashed if stored
- [ ] API keys not stored in plain text
- [ ] PII handling compliant

### Access Control

- [ ] Separate read/write access if needed
- [ ] ACL configured for Redis 6+
- [ ] Minimal privileges for applications
- [ ] Monitoring role separate from data access

---

## 7. Monitoring

### Key Metrics

- [ ] Memory usage monitored
- [ ] Connected clients monitored
- [ ] Commands per second monitored
- [ ] Key count monitored
- [ ] Hit/miss ratio tracked

### Performance Metrics

- [ ] Latency P50, P95, P99 tracked
- [ ] Slow queries logged
- [ ] Blocked clients monitored
- [ ] Eviction count tracked

### Replication Metrics

- [ ] Replication lag monitored
- [ ] Master/slave sync status
- [ ] Connected replicas tracked
- [ ] Failover tested

### Cluster Metrics (if applicable)

- [ ] Slot distribution balanced
- [ ] Node health monitored
- [ ] Cluster state healthy
- [ ] Failover tested

### Alerts

- [ ] Memory threshold alerts configured
- [ ] Connection limit alerts configured
- [ ] Replication lag alerts configured
- [ ] Error rate alerts configured

---

## Summary Checklist

### Pre-Deployment

- [ ] Configuration optimized
- [ ] Security hardening completed
- [ ] Monitoring configured
- [ ] Backup tested
- [ ] Performance baseline established

### Post-Deployment

- [ ] All tests passing
- [ ] Monitoring active
- [ ] Alerts configured
- [ ] Documentation complete
- [ ] Runbook created

---

## Liên kết liên quan
- [Redis Glossary](./glossary.md)
- [Redis Architecture](./architecture.md)
- [Redis Best Practices](./best-practice.md)
- [Redis Anti-Patterns](./anti-pattern.md)
- [Redis FAQ](./faq.md)
- [Redis Decision Tree](./decision-tree.md)
