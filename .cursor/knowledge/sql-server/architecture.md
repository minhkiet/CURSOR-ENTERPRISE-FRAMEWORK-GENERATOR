# SQL Server Architecture - Kiến Trúc SQL Server

## Giới thiệu

Tài liệu này mô tả kiến trúc chi tiết của Microsoft SQL Server, các thành phần, cách chúng tương tác, và các best practices để thiết kế hệ thống database enterprise.

---

## 1. Tổng Quan Kiến Trúc

### 1.1. Các Layer Chính

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                              │
│  (ADO.NET, ODBC, JDBC, Entity Framework, Dapper)          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    PROTOCOL LAYER                           │
│  TDS (Tabular Data Stream) Protocol                         │
│  - TCP/IP (Default Port 1433)                               │
│  - Named Pipes (\\servername\pipe\sql\query)                │
│  - Shared Memory (Local connections)                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    RELATIONAL ENGINE                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Parser     │→ │  Optimizer  │→ │  Query Executor     │  │
│  │  (Parse SQL)│  │  (Find best │  │  (Execute plan)     │  │
│  │             │  │  plan)      │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    STORAGE ENGINE                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Access     │  │  Buffer     │  │  Transaction        │  │
│  │  Methods    │  │  Manager    │  │  Manager            │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Lock       │  │  Log        │  │  Row versioning     │  │
│  │  Manager    │  │  Manager    │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    OS (Windows / Linux)                      │
│  Memory Management, File System, Network Stack              │
└─────────────────────────────────────────────────────────────┘
```

### 1.2. Data Flow trong SQL Server

```
Client Request (TDS Packet)
        │
        ▼
Protocol Layer (Decodes TDS)
        │
        ▼
Command Text
        │
        ▼
Parser (Syntax Check) → Optimizer → Execution Plan Cache
        │                    │
        │                    ▼
        │            Plan Hash / Text Hash
        │                    │
        ▼                    ▼
       ┌────────────────────────────┐
       │     Execution Plan          │
       │  ┌────────────────────────┐ │
       │  │ Iterator Tree:        │ │
       │  │ - Table/Index Scans   │ │
       │  │ - Joins (Hash/Merge/  │ │
       │  │   Nested Loop)        │ │
       │  │ - Aggregations        │ │
       │  │ - Sorts                │ │
       │  └────────────────────────┘ │
       └────────────────────────────┘
        │
        ▼
Storage Engine (Access Methods)
        │
        ├──→ Buffer Pool (Data Pages)
        ├──→ Lock Manager (Concurrency)
        └──→ Transaction Log (Write-Ahead Logging)
```

---

## 2. Buffer Pool và Memory Architecture

### 2.1. Buffer Manager

```
┌─────────────────────────────────────────────────────────────┐
│                      BUFFER POOL                             │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │ Page 1  │ │ Page 2  │ │ Page 3  │ │ Page N  │          │
│  │ (Data)  │ │ (Data)  │ │ (Data)  │ │ (Data)  │          │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ BUFFER POOL MANAGER                                 │   │
│  │ - Free Page List                                    │   │
│  │ - Lazy Writer                                      │   │
│  │ - Checkpoint                                       │   │
│  │ - AWE (Address Windowing Extensions)              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 2.2. Page và Extent Structure

```
┌────────────────────────────────────┐
│ PAGE STRUCTURE (8KB)               │
├────────────────────────────────────┤
│ Page Header (96 bytes)             │
│ - Page ID                          │
│ - Object ID                        │
│ - Previous/Next Page              │
│ - Free Space Offset                │
├────────────────────────────────────┤
│                                    │
│ Row Data (Variable)                │
│ - Row 1: [Status][Data...]        │
│ - Row 2: [Status][Data...]        │
│ - Row 3: [Status][Data...]        │
│                                    │
├────────────────────────────────────┤
│ Slot Array (Pointers to rows)      │
│ [Offset Row 1][Offset Row 2]...    │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ EXTENT STRUCTURE (64KB = 8 Pages)  │
├────────────────────────────────────┤
│ ┌──────┐┌──────┐┌──────┐┌──────┐ │
│ │Page 1││Page 2││Page 3││Page 4│ │
│ └──────┘└──────┘└──────┘└──────┘ │
│ ┌──────┐┌──────┐┌──────┐┌──────┐ │
│ │Page 5││Page 6││Page 7││Page 8│ │
│ └──────┘└──────┘└──────┘└──────┘ │
└────────────────────────────────────┘
```

### 2.3. Memory Configuration

```sql
-- Xem memory usage
SELECT 
    object_name,
    counter_name,
    cntr_value / 1024.0 AS value_mb
FROM sys.dm_os_performance_counters
WHERE counter_name IN ('Total Server Memory (KB)', 'Target Server Memory (KB)');

-- Cấu hình max server memory (MB)
EXEC sp_configure 'max server memory', 32768; -- 32GB
RECONFIGURE;

-- Cấu hình min server memory (MB)
EXEC sp_configure 'min server memory', 8192; -- 8GB
RECONFIGURE;

-- Buffer pool extension (SSD cache)
ALTER SERVER CONFIGURATION 
SET BUFFER POOL EXTENSION ON 
(FILENAME = 'F:\SQLBuffer\BufferPoolExtension.bpe', SIZE = 32 GB);
```

---

## 3. Query Processing Architecture

### 3.1. Query Optimizer Pipeline

```
SQL Text
    │
    ▼
┌─────────────────┐
│     PARSER      │ Parse SQL → Parse Tree
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    ALGEBRIZER   │ Name Resolution, Type Checking
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  OPTIMIZER     │ Generate & Evaluate Plans
│  (Cost-based)  │ Choose Cheapest Plan
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   EXECUTOR     │ Execute Selected Plan
└─────────────────┘
```

### 3.2. Query Plan Types

#### 3.2.1. Table Scan
```sql
-- Full table scan (khi không có index hoặc index không hữu ích)
SELECT * FROM LargeTable WHERE Status = 'Active';
-- Plan: Table Scan → Filter(Status='Active')
```

#### 3.2.2. Index Scan vs Index Seek
```sql
-- Index Scan: Đọc toàn bộ index
SELECT ProductName FROM Products; -- Covering index scan

-- Index Seek: Tìm kiếm có chỉ mục hiệu quả
SELECT * FROM Orders WHERE OrderDate = '2024-01-15';
-- Plan: Index Seek on OrderDate
```

#### 3.2.3. Join Strategies

```sql
-- Nested Loop Join (tốt cho small outer table)
SELECT o.*, c.CustomerName
FROM Orders o
INNER JOIN Customers c ON o.CustomerID = c.CustomerID
-- Với Index trên CustomerID

-- Hash Join (tốt cho large tables, no index)
SELECT p.ProductName, SUM(oi.Quantity) AS TotalQty
FROM Products p
INNER JOIN OrderItems oi ON p.ProductID = oi.ProductID
-- Không có index, hash join hiệu quả

-- Merge Join (tốt cho pre-sorted data)
SELECT * FROM Orders o
INNER JOIN OrderItems oi ON o.OrderID = oi.OrderID
WHERE o.OrderDate >= '2024-01-01'
-- Cả hai đã sorted trên OrderID
```

### 3.3. Plan Caching

```sql
-- Xem cached plans
SELECT 
    cp.usecounts,
    cp.size_in_bytes / 1024.0 AS size_kb,
    qt.text,
    qp.query_plan
FROM sys.dm_exec_cached_plans cp
CROSS APPLY sys.dm_exec_sql_text(cp.plan_handle) qt
CROSS APPLY sys.dm_exec_query_plan(cp.plan_handle) qp
WHERE cp.objtype = 'Proc' -- Hoặc 'Adhoc', 'Prepared'
ORDER BY cp.usecounts DESC;

-- Xóa specific plan
DBCC FREEPROCCACHE (0x1234567890ABCDEF); -- plan_handle

-- Xóa all plans cho một database
ALTER DATABASE MyDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
ALTER DATABASE MyDB SET MULTI_USER;
```

---

## 4. Concurrency Control Architecture

### 4.1. Lock Manager

```
┌─────────────────────────────────────────────────────────────┐
│                    LOCK MANAGER                              │
│                                                             │
│  Lock Hash Table                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ [Object:Table1] → [HASH] → Lock Chain               │   │
│  │ [Object:Page123] → [HASH] → Lock Chain               │   │
│  │ [Object:Row456]  → [HASH] → Lock Chain               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Lock Types:                                                │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐ │
│  │ SHARED  │ │EXCLUSIVE│ │ UPDATE  │ │ INTENTION locks │ │
│  │   (S)   │ │   (X)   │ │   (U)   │ │ (IS, IX, IU)   │ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────────────┘ │
│                                                             │
│  Compatibility Matrix:                                      │
│  │     S    X    U    IS   IX   IU                       │
│  │ S  ✓    ✗    ✗    ✓    ✗    ✗                        │
│  │ X  ✗    ✗    ✗    ✗    ✗    ✗                        │
│  │ U  ✗    ✗    ✓    ?    ?    ?                        │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 4.2. Lock Escalation

```sql
-- Xem lock escalation events
SELECT * FROM sys.dm_db_index_operational_stats(NULL, NULL, NULL, NULL)
WHERE lock_escalation_desc IS NOT NULL;

-- Ngăn chặn lock escalation
ALTER TABLE Orders SET (LOCK_ESCALATION = DISABLE);

-- Hoặc cho specific index
CREATE INDEX IX_Orders_CustomerID ON Orders(CustomerID)
WITH (LOCK_ESCALATION = DISABLE);

-- Kiểm tra escalation threshold
-- Default: 5000 row locks hoặc 40% of table locks
```

### 4.3. Deadlock Detection

```
┌─────────────────────────────────────────────────────────────┐
│              DEADLOCK DETECTION                             │
│                                                             │
│  Wait-For Graph                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │    Session A ──── waits for ──── Resource 2        │   │
│  │       │                        ▲                   │   │
│  │       │                        │                   │   │
│  │       │                        │                   │   │
│  │       └─── holds ──── Resource 1 ──┘              │   │
│  │                                                     │   │
│  │    Session B ──── waits for ──── Resource 1       │   │
│  │       │                        ▲                   │   │
│  │       │                        │                   │   │
│  │       └─── holds ──── Resource 2 ──┘              │   │
│  │                                                     │   │
│  │    CYCLE DETECTED! → Victim selected → Rollback   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

```sql
-- Extended event for deadlock monitoring
CREATE EVENT SESSION DeadlockMon ON SERVER
ADD EVENT sqlserver.xml_deadlock_report
ADD TARGET package0.event_file(SET filename='deadlocks.xel')
WITH (STARTUP_STATE=ON);

-- Xem deadlock graph
SELECT 
    event_data.value('(/event/@timestamp)[1]', 'datetime2') AS EventTime,
    event_data.value('(/event/data/value)[1]', 'nvarchar(max)') AS DeadlockGraph
FROM sys.fn_xe_file_target_read_file('deadlocks*.xel', NULL, NULL, NULL)
WITH (event_data XML);
```

---

## 5. Transaction Log Architecture

### 5.1. Write-Ahead Logging (WAL)

```
┌─────────────────────────────────────────────────────────────┐
│               WRITE-AHEAD LOGGING                           │
│                                                             │
│  Transaction T1: UPDATE Balance = 100 WHERE ID = 1         │
│                                                             │
│  Step 1: Log Manager writes to Log Buffer                  │
│  ┌─────────────────────────────────────┐                   │
│  │ LSN 1001: BEGIN T1                  │                   │
│  │ LSN 1002: MODIFY Page X (ID=1)      │                   │
│  │ LSN 1003: OldValue=50, NewValue=100 │                   │
│  └─────────────────────────────────────┘                   │
│                    │                                        │
│                    ▼ (Log Flush)                           │
│  ┌─────────────────────────────────────┐                   │
│  │        Transaction Log File         │                   │
│  │   [LSN 1001][LSN 1002][LSN 1003]   │                   │
│  └─────────────────────────────────────┘                   │
│                    │                                        │
│                    ▼                                        │
│  Step 2: Buffer Manager modifies data page                 │
│  ┌─────────────────────────────────────┐                   │
│  │         Data Page X                 │                   │
│  │   [ID=1, Balance=100]               │                   │
│  └─────────────────────────────────────┘                   │
│                    │                                        │
│                    ▼                                        │
│  Step 3: COMMIT T1                                          │
│  ┌─────────────────────────────────────┐                   │
│  │ LSN 1004: COMMIT T1                 │                   │
│  └─────────────────────────────────────┘                   │
│                                                             │
│  Key: Log must be flushed BEFORE data page is written      │
└─────────────────────────────────────────────────────────────┘
```

### 5.2. Log File Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    TRANSACTION LOG                          │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ VLF 1 (Virtual Log File)                              │  │
│  │ ┌─────────────────────────────────────────────────┐  │  │
│  │ │ LSN:0001 - LSN:0100 (Active)                    │  │  │
│  │ │ [BEGIN TX1][UPDATE][COMMIT TX1][BEGIN TX2]...  │  │  │
│  │ └─────────────────────────────────────────────────┘  │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ VLF 2                                               │  │
│  │ ┌─────────────────────────────────────────────────┐  │  │
│  │ │ LSN:0101 - LSN:0200 (Reusable)                  │  │  │
│  │ │ [Log records...]                                │  │  │
│  │ └─────────────────────────────────────────────────┘  │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ VLF 3                                               │  │
│  │ ┌─────────────────────────────────────────────────┐  │  │
│  │ │ LSN:0201 - LSN:0300 (Reusable)                  │  │  │
│  │ │ [Log records...]                                │  │  │
│  │ └─────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  MinLSN (Oldest Active Log Sequence Number)                │
│  - Oldest active transaction's first log record            │
│  - Truncation cannot occur before this point                │
└─────────────────────────────────────────────────────────────┘
```

### 5.3. Checkpoint Process

```sql
-- Force checkpoint
CHECKPOINT;

-- Xem checkpoint info
SELECT 
    database_name,
    last_checkpoint_recovery_tsn,
    last_full_backup_tsn,
    log_backup_lsn
FROM sys.database_recovery_status;

-- Automatic checkpoint interval
EXEC sp_configure 'recovery interval', 60; -- minutes
RECONFIGURE;

-- Indirect checkpoint (SQL 2016+)
ALTER DATABASE MyDB SET TARGET_RECOVERY_TIME = 60 SECONDS;
```

---

## 6. Index Architecture

### 6.1. B-Tree Structure

```
┌─────────────────────────────────────────────────────────────┐
│                   CLUSTERED INDEX B-TREE                    │
│                                                             │
│                         [Root Page]                         │
│                        /     |     \                        │
│           [Intermediate] [Intermediate] [Intermediate]      │
│              /    \        /    \        /    \            │
│          [Leaf] [Leaf]  [Leaf] [Leaf]  [Leaf] [Leaf]      │
│           │                           │                    │
│           ▼                           ▼                    │
│  ┌─────────────────┐        ┌─────────────────┐            │
│  │ Row Data Pages  │        │ Row Data Pages  │            │
│  │ (Actual Data)   │        │ (Actual Data)   │            │
│  └─────────────────┘        └─────────────────┘            │
│                                                             │
│  Note: Leaf level = Actual Data (in clustered index)       │
└─────────────────────────────────────────────────────────────┘
```

### 6.2. Non-Clustered Index Structure

```
┌─────────────────────────────────────────────────────────────┐
│               NON-CLUSTERED INDEX B-TREE                   │
│                                                             │
│                         [Root Page]                         │
│                        /     |     \                        │
│           [Intermediate] [Intermediate] [Intermediate]      │
│              /    \        /    \        /    \            │
│          [Leaf] [Leaf]  [Leaf] [Leaf]  [Leaf] [Leaf]      │
│           │                                         │       │
│           ▼                                         ▼       │
│  ┌─────────────────┐                      ┌─────────────────┐│
│  │ Index Key Data  │  ────────────────→  │ Bookmark        ││
│  │ + Included Cols │                      │ (RID or PK)     ││
│  └─────────────────┘                      └─────────────────┘│
│                                                     │        │
│                                                     ▼        │
│                                            ┌─────────────────┐│
│                                            │ Actual Row Data ││
│                                            └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### 6.3. Columnstore Index Architecture

```sql
-- Rowstore vs Columnstore
┌─────────────────────────────────────────────────────────────┐
│ ROWSTORE (Traditional)         COLUMNSTORE                 │
│ ┌─────┬─────┬─────┐           ┌─────────────────────────┐  │
│ │ R1  │ R2  │ R3  │           │ Column A: [A1,A2,A3...] │  │
│ │     │     │     │           │ Column B: [B1,B2,B3...] │  │
│ │     │     │     │           │ Column C: [C1,C2,C3...] │  │
│ └─────┴─────┴─────┘           └─────────────────────────┘  │
│ Each row together              Each column together         │
│ Good for OLTP                  Good for Data Warehouse      │
└─────────────────────────────────────────────────────────────┘

-- Create columnstore index
CREATE NONCLUSTERED COLUMNSTORE INDEX NCCI_Orders
ON Orders (
    OrderDate, CustomerID, ProductID, Quantity, Amount
);

-- Batch mode execution
-- Automatically used for large scans with columnstore
```

---

## 7. Always On Availability Architecture

### 7.1. AG/Listener Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              ALWAYS ON AVAILABILITY GROUP                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Primary Replica (Read/Write)                         │   │
│  │ ┌─────────┐ ┌─────────┐ ┌─────────┐               │   │
│  │ │ DB1     │ │ DB2     │ │ DB3     │               │   │
│  │ └─────────┘ └─────────┘ └─────────┘               │   │
│  │              │                                     │   │
│  │              ▼ (Sync/Async Log Send)               │   │
│  └──────────────┼─────────────────────────────────────┘   │
│                 │                                          │
│        ┌────────┴────────┐                                │
│        ▼                 ▼                                │
│  ┌──────────┐     ┌──────────┐                           │
│  │Secondary │     │Secondary │                          │
│  │Replica 1 │     │Replica 2 │                          │
│  │(Sync)    │     │(Async)   │                           │
│  └──────────┘     └──────────┘                           │
│        │                 │                                │
│        └────────┬────────┘                                │
│                 ▼                                          │
│  ┌─────────────────────────────────────────────────────┐  │
│  │           AG LISTENER (Virtual Network Name)        │  │
│  │              10.0.0.100:1433                         │  │
│  │         Routes connections to primary                │  │
│  └─────────────────────────────────────────────────────┘  │
│                 │                                          │
│        ┌────────┴────────┐                                │
│        ▼                 ▼                                │
│  ┌──────────┐     ┌──────────┐                           │
│  │App Conn 1 │     │App Conn 2│                           │
│  │(Primary)  │     │(Read-    │                           │
│  │           │     │Only Replica)│                        │
│  └──────────┘     └──────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

### 7.2. Failover Process

```sql
-- Manual failover (synchronous commit)
ALTER AVAILABILITY GROUP MyAG FAILOVER;
ALTER AVAILABILITY GROUP MyAG FAILOVER WITH DATA_LOSS;

-- Automatic failover requirements
-- 1. Synchronous commit mode
-- 2. At least 2 synchronous replicas
-- 3. Windows Server Failover Cluster (WSFC)

-- Configure automatic failover
ALTER AVAILABILITY GROUP MyAG
MODIFY REPLICA ON 'SecondaryReplica1'
WITH (AVAILABILITY_MODE = SYNCHRONOUS_COMMIT, FAILOVER_MODE = AUTOMATIC);
```

---

## 8. High Availability Options Comparison

| Feature | Always On AG | Database Mirroring | Log Shipping | Replication |
|---------|--------------|-------------------|--------------|-------------|
| Automatic Failover | Yes (with WSFC) | Yes (with witness) | No | No |
| Read Scale-out | Yes (readable secondary) | No | No | Yes (subscribers) |
| Data Loss | Zero (sync) | Zero (sync) | Some (by design) | Minimal |
| Failover Time | Seconds | Seconds | Minutes | Minutes |
| Database Count | Multiple | Single | Multiple | Multiple |
| Enterprise Required | Yes | No | No | No |
| Automatic Page Repair | Yes | No | No | No |

---

## 9. Resource Governor

### 9.1. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              RESOURCE GOVERNOR                              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Workload Groups                                      │   │
│  │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐    │   │
│  │ │ Executive   │ │ Standard    │ │ Reporting   │    │   │
│  │ │ (High Pri)  │ │ (Normal)    │ │ (Low Pri)   │    │   │
│  │ └─────────────┘ └─────────────┘ └─────────────┘    │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Resource Pools                                      │   │
│  │ ┌─────────────┐ ┌─────────────┐                     │   │
│  │ │ Pool 1      │ │ Pool 2      │                     │   │
│  │ │ MIN=50%     │ │ MIN=25%     │                     │   │
│  │ │ MAX=100%    │ │ MAX=50%     │                     │   │
│  │ └─────────────┘ └─────────────┘                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Classifier Function                                  │   │
│  │ - Routes sessions to workload groups                │   │
│  │ - Based on: username, app name, host, etc.           │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 9.2. Implementation

```sql
-- Tạo resource pool
CREATE RESOURCE POOL ExecutivePool
WITH (
    MIN_CPU_PERCENT = 40,
    MAX_CPU_PERCENT = 100,
    MIN_MEMORY_PERCENT = 30,
    MAX_MEMORY_PERCENT = 100
);

CREATE RESOURCE POOL ReportingPool
WITH (
    MIN_CPU_PERCENT = 0,
    MAX_CPU_PERCENT = 20,
    MIN_MEMORY_PERCENT = 10,
    MAX_MEMORY_PERCENT = 30
);

-- Tạo workload group
CREATE WORKLOAD GROUP ExecutiveGroup
USING ExecutivePool;

CREATE WORKLOAD GROUP ReportingGroup
USING ReportingPool;

-- Tạo classifier function
CREATE FUNCTION dbo.ResourceClassifier()
RETURNS SYSNAME
WITH SCHEMABINDING
AS
BEGIN
    DECLARE @group SYSNAME;
    
    IF SUSER_NAME() LIKE 'exec\%'
        SET @group = 'ExecutiveGroup';
    ELSE IF PROGRAM_NAME() LIKE '%Reporting%'
        SET @group = 'ReportingGroup';
    ELSE
        SET @group = 'default';
    
    RETURN @group;
END;

-- Register classifier
ALTER RESOURCE GOVERNOR WITH (CLASSIFIER_FUNCTION = dbo.ResourceClassifier);
ALTER RESOURCE GOVERNOR RECONFIGURE;
```

---

## 10. Security Architecture

### 10.1. Authentication Modes

```
┌─────────────────────────────────────────────────────────────┐
│              SQL SERVER AUTHENTICATION                      │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Windows Authentication (Integrated Security)        │   │
│  │ - Uses Windows AD/Kerberos                          │   │
│  │ - Single sign-on                                    │   │
│  │ - NTLM fallback                                    │   │
│  │ - More secure                                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ SQL Server Authentication (Mixed Mode)               │   │
│  │ - Username/password stored in SQL Server            │   │
│  │ - Password hash stored (no plaintext)              │   │
│  │ - Policy enforcement (complexity, expiration)       │   │
│  │ - Must explicitly specify in connection string      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Connection String Examples:                                │
│  Integrated: "Server=MyServer;Database=MyDB;Integrated       │
│               Security=true;"                              │
│  SQL Auth:   "Server=MyServer;Database=MyDB;User            │
│               ID=MyUser;Password=MyPass;"                  │
└─────────────────────────────────────────────────────────────┘
```

### 10.2. Encryption Architecture

```sql
-- Transparent Data Encryption (TDE)
USE master;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'ComplexPassword123!';
CREATE CERTIFICATE MyServerCert WITH SUBJECT = 'My TDE Certificate';
BACKUP CERTIFICATE MyServerCert TO FILE = 'C:\Backups\MyCert.cer'
    PRIVATE KEY (FILE = 'C:\Backups\MyCertKey.key',
                 ENCRYPTION BY PASSWORD = 'CertPassword123!');

USE MyDB;
CREATE DATABASE ENCRYPTION KEY
BY ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE MyServerCert;
ALTER DATABASE MyDB SET ENCRYPTION ON;

-- Always Encrypted
-- Column-level encryption with keys stored in Windows Certificate Store
CREATE TABLE Customers (
    SSN CHAR(11) COLLATE Latin1_General_BIN2 
        ENCRYPTED WITH (ENCRYPTION_TYPE = DETERMINISTIC,
                       ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256',
                       COLUMN_ENCRYPTION_KEY = MyCEK) NOT NULL,
    Name NVARCHAR(100)
);

-- Connection string with Column Encryption Setting
"Server=MyServer;Database=MyDB;Column Encryption Setting=Enabled;"
```

---

## 11. Monitoring Architecture

### 11.1. Dynamic Management Views (DMVs)

```sql
-- System Health Monitoring
-- CPU Pressure
SELECT 
    r.session_id,
    r.status,
    r.cpu_time,
    r.total_elapsed_time,
    t.text AS query_text
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE r.cpu_time > 1000;

-- Memory Pressure
SELECT 
    counter_name,
    cntr_value / 1024.0 AS value_mb
FROM sys.dm_os_performance_counters
WHERE counter_name LIKE '%Memory%';

-- Blocking
SELECT 
    blocked.session_id AS blocked_session,
    blocker.session_id AS blocking_session,
    blocked_txt.text AS blocked_sql,
    blocker_txt.text AS blocker_sql
FROM sys.dm_exec_requests blocked
JOIN sys.dm_exec_requests blocker ON blocked.blocking_session_id = blocker.session_id
CROSS APPLY sys.dm_exec_sql_text(blocked.sql_handle) blocked_txt
CROSS APPLY sys.dm_exec_sql_text(blocker.sql_handle) blocker_txt;

-- Wait Statistics
SELECT TOP 20
    wait_type,
    waiting_tasks_count,
    wait_time_ms,
    signal_wait_time_ms,
    wait_time_ms - signal_wait_time_ms AS resource_wait_time_ms
FROM sys.dm_os_wait_stats
WHERE wait_time_ms > 0
ORDER BY wait_time_ms DESC;
```

### 11.2. SQL Server Error Log

```sql
-- Đọc error log qua sp
EXEC sp_readerrorlog;

-- Lọc error log
EXEC sp_readerrorlog 0, 1, 'error'; -- 0=current, 1=ERRORLOG, 'error'=filter
EXEC sp_readerrorlog 0, 1, NULL, '2024-01-01'; -- entries after date

-- Xem configuration
EXEC sp_configure;

-- Error log path
SELECT SERVERPROPERTY('ErrorLogFileName');
```
