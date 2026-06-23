---
title: "SQL Server Decision Tree - Cây Quyết Định SQL Server"
description: "Decision trees for SQL Server covering index strategy selection, HA/DR options, backup strategy, query optimization approach, and isolation level selection with practical scenarios."
tags: ["sql-server", "decision-tree", "indexing", "ha-dr", "backup", "performance", "query-optimization"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# SQL Server Decision Tree - Cây Quyết Định SQL Server

## Tổng Quan (Overview)

Tài liệu này cung cấp các decision trees để guide developers và DBAs through common technical decisions trong SQL Server. Mỗi decision tree bao gồm các scenarios cụ thể với recommended approaches và rationale.

Các quyết định về database design và configuration thường có cascading effects trên performance, maintainability, và reliability. Sử dụng systematic approach giúp đảm bảo rằng decisions được made consistently và based on solid reasoning, không phải gut feeling hoặc convention.

## Mục Đích (Purpose)

Decision trees này được thiết kế để:

**Accelerate Decision-Making**: Cung cấp structured framework cho các common decisions, reducing time spent on routine choices.

**Ensure Consistency**: Giúp ensure rằng similar decisions được made consistently across projects và teams.

**Capture Best Practices**: Encode best practices từ industry experience và Microsoft recommendations vào actionable guidance.

**Reduce Errors**: Minimize risk của suboptimal decisions bằng cách highlighting common pitfalls và trade-offs.

## Index Strategy Decision Tree

### Primary Key Decision

```
Does the table require a natural composite key?
├── YES ──────────────────────────────────→ Use composite primary key
│   Considerations:
│   • Keys should be as narrow as possible
│   • Order matters for query patterns
│   • Use for many-to-many junction tables
│
└── NO
    │
    ├── Is the table primarily for OLTP?
    │   └── YES ──────────────────────────→ Use BIGINT IDENTITY as PK
    │       Rationale:
    │       • Sequential values minimize page splits
    │       • Narrow key (8 bytes)
    │       • Works well with auto-increment patterns
    │
    ├── Is the table primarily for analytics?
    │   └── YES ──────────────────────────→ Consider BIGINT IDENTITY or
    │       Rationale:                      composite business key
    │       • May benefit from clustering
    │       • Consider columnstore later
    │       • Business keys may improve joins
    │
    └── Is the table very small (<1000 rows)?
        └── YES ──────────────────────────→ Consider heap (no PK)
            Rationale:
            • Minimal benefit from clustering
            • Simpler INSERT operations
            • May use less space
```

### Clustered Index Decision

```
What is the PRIMARY access pattern for this table?

├── Range queries on a sequential key?
│   └── YES ──────────────────────────────→ Cluster on that column
│       Examples:
│       • Orders by OrderDate
│       • Transactions by TransactionDate
│       Benefits:
│       • Efficient range scans
│       • Physical data ordering matches query
│
├── Primary key is frequently used in JOINs?
│   └── YES ──────────────────────────────→ Cluster on primary key
│       Rationale:
│       • JOINs often reference PK
│       • Bookmark lookups use clustered index
│
├── Table is a many-to-many junction?
│   └── YES ──────────────────────────────→ Cluster on composite key
│       Example: OrderDetails (OrderID, ProductID)
│       Benefits:
│       • Both FKs benefit from clustering
│       • Efficient for typical junction queries
│
├── High INSERT volume, no range queries?
│   └── YES ──────────────────────────────→ Cluster on IDENTITY or
│       Rationale:                         NEWSEQUENTIALID()
│       • Sequential inserts minimize fragmentation
│       • No page split overhead
│
└── None of above?
    └── ─────────────────────────────────→ Evaluate carefully
        Considerations:
        • Cluster on column with high selectivity
        • Consider narrow keys
        • Avoid wide keys (multiple columns, strings)
```

### Non-Clustered Index Decision

```
Is the column frequently used in WHERE, JOIN, or ORDER BY?

├── NO ───────────────────────────────────→ Skip the index
│   Justification:
│   • Index overhead on writes
│   • Not used for data access
│
└── YES
    │
    ├── Are all columns needed by the query in this index?
    │   ├── (Including them as key or included columns)
    │   │
    │   ├── YES ──────────────────────────→ Index already covering
    │   │   Verify:
    │   │   • Columns in correct order
    │   │   • Included columns appropriate
    │   │
    │   └── NO ───────────────────────────→ Create covering index
    │       Design:
    │       • Key columns: WHERE/JOIN/ORDER BY columns
    │       • Included columns: SELECT columns
    │       • Example:
    │       CREATE INDEX IX_Table_Covering
    │       ON Table(Col1, Col2)
    │       INCLUDE (Col3, Col4, Col5);
    │
    └── Is the column highly selective?
        │
        ├── YES (>10% unique values) ─────→ Good index candidate
        │   Use as leading column of composite index
        │
        └── NO ───────────────────────────→ Consider including
            (Low selectivity)                with other high-selective
            Examples:                        columns
            • Status columns
            • Gender columns
            • Boolean flags

Additional Considerations:
├── Will the index be filtered?
│   └── YES ────────────────────────────→ Consider filtered index
│       Example:
│       CREATE INDEX IX_Orders_Pending
│       ON Orders(OrderDate)
│       WHERE Status = 'Pending';
│
└── Is the table large and analytical?
    └── YES ────────────────────────────→ Consider columnstore index
        Example:
        CREATE NONCLUSTERED COLUMNSTORE INDEX IX_Fact_ColumnStore
        ON FactSales(DateKey, ProductKey, CustomerKey, Amount);
```

## Query Optimization Decision Tree

### Performance Problem Investigation

```
Query is performing poorly. Investigation path:

STEP 1: Check Execution Plan
│
├── Are there table scans?
│   └── YES ─────────────────────────────→ Missing index needed
│       Action:
│       • Review WHERE clause columns
│       • Review JOIN columns
│       • Create appropriate index
│
├── Are there bookmark lookups?
│   └── YES ─────────────────────────────→ Add covering index
│       Action:
│       • Identify missing columns
│       • Add as INCLUDE columns
│
├── Large gap between estimated and actual rows?
│   └── YES ─────────────────────────────→ Statistics issue
│       Actions:
│       • UPDATE STATISTICS on affected tables
│       • Consider FULLSCAN for accuracy
│       • Check for parameter sniffing
│
└── Are there expensive sort operations?
    └── YES ─────────────────────────────→ Check if sort can be avoided
        Actions:
        • Add index on ORDER BY columns
        • Remove unnecessary columns from SELECT
        • Consider query rewrite

STEP 2: Check Wait Statistics
│
├── High CXPACKET waits?
│   └── YES ─────────────────────────────→ Parallelism issue
│       Actions:
│       • Review MAXDOP setting
│       • Check for uneven distribution
│
├── High PAGEIOLATCH waits?
│   └── YES ─────────────────────────────→ I/O bottleneck
│       Actions:
│       • Check disk latency
│       • Consider adding indexes
│       • Review buffer pool size
│
├── High LCK_M_ waits?
│   └── YES ─────────────────────────────→ Blocking issue
│       Actions:
│       • Review transaction isolation level
│       • Optimize query to hold locks shorter
│       • Consider optimistic locking
│
└── High ASYNC_NETWORK_IO waits?
    └── YES ─────────────────────────────→ Client processing lag
        Actions:
        • Review client application
        • Consider smaller result sets
        • Check network latency

STEP 3: Check System Resources
│
├── High CPU?
│   └── YES ─────────────────────────────→ CPU-bound workload
│       Actions:
│       • Review query compilation
│       • Check for unnecessary computations
│       • Consider query optimization
│
└── Memory pressure?
    └── YES ─────────────────────────────→ Memory-bound workload
        Actions:
        • Review buffer pool size
        • Check for memory leaks
        • Optimize memory-intensive queries
```

### Query Rewrite Decision Tree

```
How can this query be improved?

├── Query uses SELECT *?
│   └── YES ─────────────────────────────→ Replace with column list
│       Change:
│       SELECT * FROM Orders
│       ↓
│       SELECT OrderID, CustomerID, OrderDate, TotalAmount
│       FROM Orders;
│
├── Query has functions in WHERE clause?
│   └── YES ─────────────────────────────→ Restructure predicate
│       Before:
│       WHERE YEAR(OrderDate) = 2024
│       ↓
│       After:
│       WHERE OrderDate >= '2024-01-01'
│         AND OrderDate < '2025-01-01';
│
├── Query uses NOT IN with subquery?
│   └── YES ─────────────────────────────→ Use NOT EXISTS or LEFT JOIN
│       Before:
│       WHERE CustomerID NOT IN (SELECT...)
│       ↓
│       After:
│       WHERE NOT EXISTS (SELECT 1 FROM...);
│
├── Query uses DISTINCT unnecessarily?
│   └── YES ─────────────────────────────→ Investigate root cause
│       Actions:
│       • Check for proper JOIN conditions
│       • Use EXISTS if only checking existence
│       • Verify data model normalization
│
├── Query uses OR in WHERE clause?
│   └── YES ─────────────────────────────→ Consider UNION or IN
│       Before:
│       WHERE CustomerID = 1 OR CustomerID = 2
│       ↓
│       After:
│       WHERE CustomerID IN (1, 2);
│
└── Query has multiple JOINs?
    └── YES ─────────────────────────────→ Review JOIN order and types
        Considerations:
        • Put smaller tables first
        • Filter early on small tables
        • Use appropriate JOIN types
        • Consider denormalization if excessive JOINs
```

## High Availability Decision Tree

### HA/DR Solution Selection

```
What is your PRIMARY requirement?

├── Maximum protection with zero data loss?
│   └── YES ─────────────────────────────→ Always On AG with
│       Configuration:                     Synchronous Commit
│       • All replicas synchronous
│       • Automatic failover enabled
│       • Automatic backups on secondary
│       RTO: Minutes
│       RPO: Zero
│
├── Balanced protection and performance?
│   └── YES ─────────────────────────────→ Always On AG with
│       Configuration:                     Mixed Commit Mode
│       • Primary site: Synchronous
│       • DR site: Asynchronous
│       • Manual failover to DR
│       RTO: Minutes
│       RPO: Minutes (depending on distance)
│
├── Simple disaster recovery?
│   └── YES ─────────────────────────────→ Log Shipping
│       Characteristics:
│       • Lower cost than AGs
│       • Simple to configure
│       • Manual failover
│       RTO: Hours (depending on backup frequency)
│       RPO: Hours (depending on backup frequency)
│
├── Instance-level protection?
│   └── YES ─────────────────────────────→ Failover Cluster Instance
│       Characteristics:
│       • Protects entire SQL instance
│       • Requires shared storage
│       • Automatic failover
│
└── Data distribution/scale-out?
    └── ─────────────────────────────────→ Consider Replication
        Options:
        • Transactional: Real-time distribution
        • Peer-to-Peer: Multi-master
        • Merge: Bidirectional with conflicts
```

### Always On AG Topology Decision

```
How many replicas do you need?

├── Business-critical, cannot afford downtime?
│   └── YES ─────────────────────────────→ 3 replicas minimum
│       Topology:
│       • Primary (sync)
│       • Secondary 1 (sync, automatic failover)
│       • Secondary 2 (async, backup/DR)
│
├── Standard business continuity?
│   └── YES ─────────────────────────────→ 2 replicas
│       Topology:
│       • Primary (sync)
│       • Secondary (sync, automatic failover)
│       Note: No automatic failover to third site
│
└── Development/Non-critical?
    └── YES ─────────────────────────────→ 1 replica (primary only)
        Or:
        • Basic Availability Groups (SQL 2016+)
        • Database mirroring (legacy)
```

### Backup Location Decision

```
Where should backups run?

├── Want to minimize impact on primary?
│   └── YES ─────────────────────────────→ Backup on secondary replicas
│       Benefits:
│       • Reduces primary workload
│       • Offloads I/O to replica
│       • Same reliability as primary backups
│
├── Need point-in-time recovery guarantee?
│   └── YES ─────────────────────────────→ Must backup transaction log
│       Requirements:
│       • Log backups every 15-30 minutes
│       • Continuous log chain
│       • Monitor backup job success
│
└── Can accept some data loss?
    └── YES ─────────────────────────────→ Consider differential backups
        Strategy:
        • Weekly full backups
        • Daily differential backups
        • Hourly log backups
```

## Backup Strategy Decision Tree

### Recovery Model Selection

```
What is your RPO requirement?

├── Zero data loss required?
│   └── YES ─────────────────────────────→ FULL recovery model
│       Requirements:
│       • Regular log backups (every 15-30 min)
│       • Continuous log chain
│       • Point-in-time recovery capability
│       Cost: Higher log storage, backup overhead
│
├── Can tolerate some data loss?
│   └── YES ─────────────────────────────→ BULK_LOGGED recovery model
│       Benefits:
│       • Minimal logging for bulk operations
│       • Better performance for bulk inserts
│       • Still supports log backups
│       Caveat: Some operations require full backup
│
└── Simple backup acceptable?
    └── YES ─────────────────────────────→ SIMPLE recovery model
        Characteristics:
        • No log backups needed
        • Auto-truncates log after checkpoint
        • Maximum data loss = since last full backup
        Use for: Development, non-critical data
```

### Backup Schedule Decision

```
What backup schedule meets your RTO/RPO?

For CRITICAL databases (RPO = 15 minutes):
├── Full backup: Daily (or more frequently)
├── Differential: Every 4-6 hours
└── Log backup: Every 15 minutes

For IMPORTANT databases (RPO = 1 hour):
├── Full backup: Daily
├── Differential: Every 6 hours
└── Log backup: Every 30-60 minutes

For STANDARD databases (RPO = 24 hours):
├── Full backup: Daily
└── Differential: Every 12-24 hours

For NON-CRITICAL databases (RPO = weekly):
└── Full backup: Weekly
```

### Backup Retention Decision

```
How long should backups be retained?

Based on compliance requirements:
├── General business: 30-90 days
├── Financial/SOX: 7 years
├── Healthcare/HIPAA: 6 years
├── GDPR considerations: As needed for data subject requests
│
Based on recovery needs:
├── Can restore to any point in last 30 days?
│   └── Keep 30+ days of backups
│
└── Need historical analysis?
    └── YES ─────────────────────────────→ Keep backups longer
        Consider:
        • Archive older backups to cheaper storage
        • Document retention policy
        • Test restores from archived backups
```

## Isolation Level Decision Tree

```
What are your requirements?

├── Need to read uncommitted changes?
│   └── YES ─────────────────────────────→ READ UNCOMMITTED
│       Use cases:
│       • Very low priority reporting
│       • Debugging scenarios
│       Risk: Dirty reads possible
│
├── Need to avoid blocking?
│   └── YES ─────────────────────────────→ READ COMMITTED SNAPSHOT
│       (Enable at database level)
│       Benefits:
│       • Readers don't block writers
│       • Writers don't block readers
│       • No dirty reads
│
├── Need consistent reads within transaction?
│   └── YES ─────────────────────────────→ REPEATABLE READ
│       Use cases:
│       • Financial calculations
│       • Audit reports
│       Risk: Higher blocking potential
│
├── Need snapshot of data as of transaction start?
│   └── YES ─────────────────────────────→ SNAPSHOT isolation
│       Benefits:
│       • Consistent view without blocking
│       • Uses row versioning
│       Consideration: Tempdb usage increases
│
└── Need to prevent phantom reads entirely?
    └── YES ─────────────────────────────→ SERIALIZABLE
        Use cases:
        • Critical financial transactions
        • When absolute consistency required
        Risk: Highest blocking potential
```

## Data Type Decision Tree

### Numeric Data Type Selection

```
What type of number do you need?

├── Integer values?
│   │
│   ├── Range: -2,147,483,648 to 2,147,483,647?
│   │   └── YES ─────────────────────────→ INT (4 bytes)
│   │
│   ├── Range: -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807?
│   │   └── YES ─────────────────────────→ BIGINT (8 bytes)
│   │
│   ├── Range: 0 to 255?
│   │   └── YES ─────────────────────────→ TINYINT (1 byte)
│   │
│   └── Range: -32,768 to 32,767?
│       └── YES ─────────────────────────→ SMALLINT (2 bytes)
│
├── Decimal values (exact precision)?
│   └── ────────────────────────────────→ DECIMAL(p,s) or NUMERIC(p,s)
│       Parameters:
│       • p = total digits (precision)
│       • s = digits after decimal (scale)
│       Examples:
│       • DECIMAL(10,2): 12345678.90
│       • DECIMAL(18,4): For currency calculations
│
├── Approximate numbers (floating point)?
│   └── ────────────────────────────────→ FLOAT or REAL
│       Use for:
│       • Scientific calculations
│       • When precision not critical
│       Caveat: Not for financial calculations
│
└── Monetary values?
    └── ─────────────────────────────────→ DECIMAL(p,s)
        Best practice:
        • DECIMAL(19,4) for general currency
        • DECIMAL(19,2) if no sub-unit needed
        • Avoid FLOAT/MONEY for accuracy
```

### Date/Time Data Type Selection

```
What type of date/time do you need?

├── Need both date and time?
│   │
│   ├── Need precision better than milliseconds?
│   │   └── YES ─────────────────────────→ DATETIME2(7)
│   │       Range: 0001-01-01 to 9999-12-31
│   │       Precision: 100 nanoseconds
│   │
│   └── Millisecond precision acceptable?
│       └── YES ─────────────────────────→ DATETIME2(3)
│           Precision: 1 millisecond
│
├── Need date only (no time)?
│   └── ─────────────────────────────────→ DATE
│       Storage: 3 bytes
│       Range: 0001-01-01 to 9999-12-31
│
├── Need time only (no date)?
│   └── ─────────────────────────────────→ TIME(p)
│       Parameters:
│       • p = precision (0-7)
│       • Default: TIME(7)
│
├── Legacy applications only?
│   └── ─────────────────────────────────→ DATETIME (deprecated)
│       Issues:
│       • Less precision (3.33ms)
│       • Limited range
│       • Accuracy issues
│       Recommendation: Migrate to DATETIME2
│
└── Need date and time with timezone?
    └── ─────────────────────────────────→ DATETIMEOFFSET
        Use when:
        • Multi-timezone applications
        • Need to preserve original timezone
```

### String Data Type Selection

```
What type of string do you need?

├── Need variable-length ASCII data?
│   │
│   ├── Fixed maximum length < 8,000?
│   │   └── YES ─────────────────────────→ VARCHAR(n)
│   │       Example: VARCHAR(50) for names
│   │
│   └── Variable length, > 8,000 chars?
│       └── YES ─────────────────────────→ VARCHAR(MAX)
│           Use for:
│           • Large text fields
│           • JSON/XML storage
│           • File contents
│
├── Need fixed-length data?
│   └── YES ─────────────────────────────→ CHAR(n)
│       Use for:
│       • Codes, IDs with fixed format
│       • When padding is acceptable
│
├── Need Unicode data (multi-language)?
│   │
│   ├── Fixed maximum length < 4,000?
│   │   └── YES ─────────────────────────→ NVARCHAR(n)
│   │
│   └── Variable length, > 4,000 chars?
│       └── YES ─────────────────────────→ NVARCHAR(MAX)
│
└── Deprecated types - AVOID:
    ├── TEXT, NTEXT (use VARCHAR/NAVARCHAR)
    ├── IMAGE (use VARBINARY)
    └── VARCHAR without size (use VARCHAR(n))
```

## Index Type Selection Decision Tree

```
What index type is appropriate?

├── General OLTP workload?
│   └── YES ─────────────────────────────→ Traditional row-store indexes
│       Types:
│       • Clustered: For primary access pattern
│       • Non-clustered: For additional access paths
│
├── Analytical/warehouse workload?
│   └── YES ─────────────────────────────→ Columnstore indexes
│       Options:
│       • Non-clustered columnstore
│       • Clustered columnstore (for data warehouse)
│
├── Need to filter index to subset of rows?
│   └── YES ─────────────────────────────→ Filtered index
│       Example:
│       CREATE INDEX IX_Orders_Pending
│       ON Orders(OrderDate)
│       WHERE Status = 'Pending';
│
├── Need full-text search capability?
│   └── YES ─────────────────────────────→ Full-text index
│       Note: Also need standard B-tree index
│
└── Need spatial/geographic data?
    └── YES ─────────────────────────────→ Spatial index
        For geometry/geography data types
```

## Common Scenarios

### Scenario 1: New Transactional Table

```
Requirements:
• High INSERT volume
• Frequent queries by customer
• Rarely queried by order date
• No range queries expected

Decision Process:

1. Primary Key
└── INT IDENTITY ──────────────────────→ Best for auto-increment inserts

2. Clustered Index
└── PK on OrderID ─────────────────────→ Good for sequential inserts

3. Non-clustered Indexes
└── CustomerID ────────────────────────→ For customer lookups
└── Consider: Covering index with
    INCLUDE (CustomerID, OrderDate, TotalAmount)

4. Table Design
└── Heap NOT recommended ──────────────→ PK clustering is fine
```

### Scenario 2: Reporting Table with Aggregations

```
Requirements:
• Primarily read-only (refreshed nightly)
• Complex aggregations by date
• Sum by product category
• Average by customer region

Decision Process:

1. Clustered Index
└── DateKey ───────────────────────────→ For time-based aggregation

2. Indexes for Common Aggregations
└── Composite (DateKey, CategoryKey) ──→ For category rollups
└── Composite (DateKey, RegionKey) ───→ For region rollups

3. Index Type
└── Consider columnstore ───────────────→ For large fact tables
└── Combined row + columnstore ────────→ For mixed workloads

4. Materialized Aggregations
└── Consider: Indexed views for pre-computed aggregations
```

### Scenario 3: High-Concurrency Table

```
Requirements:
• Many concurrent transactions
• Short transactions
• Minimal blocking tolerance
• Point lookups by ID

Decision Process:

1. Isolation Level
└── Enable RCSI ────────────────────────→ READ COMMITTED SNAPSHOT

2. Index Design
└── Narrow indexes ────────────────────→ Reduce lock footprint
└── Avoid covering indexes with many ──→ Keep writes efficient
    included columns

3. Application Design
└── Keep transactions short ─────────────→ Hold locks briefly
└── Process in batches if possible ─────→ Better concurrency

4. Monitoring
└── Track lock waits ───────────────────→ Alert on blocking
```

## Quick Reference Tables

### Index Selection Quick Guide

| Query Pattern | Recommended Index |
|--------------|-------------------|
| Equality: WHERE col = value | Non-clustered on col |
| Range: WHERE col > value | Non-clustered on col |
| Multiple filters | Composite index |
| JOIN on foreign key | Index on FK |
| ORDER BY col | Index on col (same order) |
| GROUP BY col | Index on col |
| SELECT + WHERE + ORDER | Covering index |

### HA Solution Comparison

| Solution | RPO | RTO | Cost | Complexity |
|---------|-----|-----|------|------------|
| Always On AG (Sync) | Zero | Minutes | High | High |
| Always On AG (Async) | Minutes | Minutes | High | High |
| FCI | Zero | Minutes | Medium | Medium |
| Log Shipping | Hours | Hours | Low | Low |
| Backup/Restore | Hours | Hours | Low | Low |

### Isolation Level Comparison

| Level | Dirty Read | Non-Repeatable | Phantom | Blocking |
|-------|-----------|----------------|---------|----------|
| READ UNCOMMITTED | Yes | Yes | Yes | Minimal |
| READ COMMITTED | No | Yes | Yes | Moderate |
| RCSI | No | Yes | Yes | Low |
| REPEATABLE READ | No | No | Yes | High |
| SNAPSHOT | No | No | No | Low |
| SERIALIZABLE | No | No | No | Very High |

## References

- SQL Server Index Design: https://docs.microsoft.com/en-us/sql/relational-databases/sql-server-index-design-guide
- High Availability: https://docs.microsoft.com/en-us/sql/sql-server/high-availability-solutions-sql-server
- Backup and Restore: https://docs.microsoft.com/en-us/sql/relational-databases/backup-restore/back-up-and-restore-of-sql-server-databases
- Isolation Levels: https://docs.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-locking-and-row-versioning-guide
