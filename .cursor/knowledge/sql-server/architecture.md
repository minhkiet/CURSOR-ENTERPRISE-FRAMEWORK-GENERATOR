---
title: "SQL Server Architecture - Kiến Trúc SQL Server"
description: "Comprehensive guide to SQL Server architecture covering storage engine, query optimizer, execution plans, Always On availability groups, replication topologies, and memory management."
tags: ["sql-server", "architecture", "storage-engine", "query-optimizer", "execution-plan", "always-on", "replication", "database"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# SQL Server Architecture - Kiến Trúc SQL Server

## Tổng Quan (Overview)

SQL Server là một Relational Database Management System (RDBMS) enterprise-class được phát triển bởi Microsoft, được thiết kế để xử lý các workload từ small single-application databases đến large enterprise systems với hàng terabytes dữ liệu và thousands concurrent users. Hiểu biết sâu về kiến trúc nội bộ của SQL Server là essential cho việc thiết kế, implementing, và operating các hệ thống database hiệu quả.

Kiến trúc SQL Server được chia thành nhiều layers và components, mỗi component đảm nhận một responsibility cụ thể. Từ cách data được stored trên disk, qua cách nó được cached trong memory, đến cách queries được parsed và executed, mỗi bước đều có những optimizations và configurations mà developers và DBAs cần hiểu để tận dụng tối đa platform.

Tài liệu này cung cấp một cái nhìn toàn diện về kiến trúc SQL Server, từ low-level storage mechanisms đến high-level availability solutions. Mỗi section bao gồm both conceptual explanations và practical implications, giúp người đọc không chỉ hiểu "cái gì" mà còn hiểu "tại sao" và "như thế nào" của mỗi component.

## Mục Đích (Purpose)

Mục đích của tài liệu này là cung cấp nền tảng kiến thức vững chắc về kiến trúc SQL Server cho các đối tượng:

**Database Administrators (DBAs)**: Hiểu rõ kiến trúc giúp DBAs make informed decisions về configuration, performance tuning, và troubleshooting. Nhiều issues trong production environment có root cause liên quan đến architectural decisions hoặc misconfigurations.

**Software Developers**: Developers với kiến thức về kiến trúc database có thể viết code hiệu quả hơn, design schemas tối ưu hơn, và troubleshoot performance issues một cách systematic. Hiểu cách query optimizer hoạt động giúp developers viết queries thân thiện với optimizer.

**System Architects**: Kiến thức về kiến trúc SQL Server là essential cho việc design các giải pháp enterprise-scale, bao gồm high availability, disaster recovery, và data tier architecture.

## Kiến Trúc Storage Engine

### Data Files and Pages

SQL Server lưu trữ data trong các files với cấu trúc page-based. Mỗi page có kích thước cố định là 8KB và là unit cơ bản nhất của I/O operations. Hiểu cách SQL Server organiz dữ liệu trong pages là fundamental cho việc hiểu performance characteristics của queries và index operations.

**Page Types**: SQL Server sử dụng nhiều loại pages cho các mục đích khác nhau. Data pages chứa actual row data, index pages chứa index entries, và IAM (Index Allocation Map) pages track which pages belong to which objects. Mỗi page có một 96-byte header chứa metadata như page type, object ID, và free space information.

**Extents**: Pages được grouped vào units gọi là extents, mỗi extent chứa 8 contiguous pages (64KB). SQL Server sử dụng two types of extents: mixed extents (có thể contain pages từ multiple objects) và uniform extents (owned hoàn toàn by một single object). Khi một object mới được tạo, SQL Server allocate pages từ mixed extents cho đến khi object đủ lớn để merit a uniform extent.

```sql
-- Check page count and size for a table
SELECT 
    OBJECT_NAME(p.object_id) AS table_name,
    p.index_id,
    i.name AS index_name,
    SUM(p.page_count) AS total_pages,
    SUM(p.page_count) * 8 / 1024 AS size_mb,
    SUM(p.avg_page_space_used_in_percent) / NULLIF(COUNT(*), 0) AS avg_space_used_pct
FROM sys.dm_db_index_physical_stats(
    DB_ID(), 
    OBJECT_ID('Orders'), 
    NULL, 
    NULL, 
    'DETAILED') p
JOIN sys.indexes i ON p.object_id = i.object_id AND p.index_id = i.index_id
WHERE p.page_count > 0
GROUP BY p.object_id, p.index_id, i.name
ORDER BY total_pages DESC;
```

### Buffer Pool

Buffer Pool là phần quan trọng nhất của SQL Server memory architecture, đóng vai trò như một in-memory cache cho data pages. Khi một query cần đọc data từ disk, SQL Server first checks buffer pool. Nếu page đã có trong buffer pool (buffer hit), I/O operation được avoided hoàn toàn. Nếu page không có trong buffer pool (buffer miss), page được read từ disk vào buffer pool trước khi query có thể proceed.

Buffer pool management là một balancing act giữa maximizing cache hit rate và leaving enough memory cho other SQL Server components. SQL Server sử dụng sophisticated algorithms để determine which pages to keep in cache và which to evict, dựa trên factors như page access frequency, how recently accessed, và whether page has been modified.

```sql
-- Check buffer pool usage
SELECT 
    COUNT(*) * 8 / 1024 AS total_buffer_size_mb,
    SUM(CASE WHEN database_id = DB_ID() THEN 1 ELSE 0 END) * 8 / 1024 AS current_db_size_mb,
    SUM(CASE WHEN database_id <> DB_ID() THEN 1 ELSE 0 END) * 8 / 1024 AS other_db_size_mb,
    SUM(CONVERT(BIGINT, free_space_in_bytes)) / 1024 / 1024 AS free_space_mb
FROM sys.dm_os_buffer_descriptors;

-- Check which tables use most buffer pool
SELECT 
    OBJECT_NAME(p.object_id) AS table_name,
    COUNT(*) AS cached_pages,
    COUNT(*) * 8 / 1024 AS size_mb
FROM sys.dm_os_buffer_descriptors bd
JOIN sys.allocation_units au ON bd.allocation_unit_id = au.allocation_unit_id
JOIN sys.partitions p ON au.container_id = p.hobt_id
WHERE bd.database_id = DB_ID()
    AND p.object_id > 100
GROUP BY p.object_id
ORDER BY size_mb DESC;
```

### Transaction Log

Transaction log là một append-only file hoặc series of files record tất cả changes made to the database. Mỗi change được written to log trước khi nó được applied to data files (write-ahead logging), đảm bảo durability và enabling point-in-time recovery.

Log records được written sequentially và rarely accessed randomly, making log files ideal candidate cho sequential I/O và đặc biệt suitable cho fast storage (như SSDs). Khi transaction commits, log records for that transaction remain in log file until a checkpoint process marks them as no longer needed for recovery.

```sql
-- Check transaction log usage
SELECT 
    DB_NAME(database_id) AS database_name,
    total_log_size_in_bytes / 1024 / 1024 AS total_log_mb,
    used_log_space_in_bytes / 1024 / 1024 AS used_log_mb,
    used_log_space_in_percent AS used_log_pct,
    log_space_in_bytes_since_last_backup / 1024 / 1024 AS log_since_backup_mb,
    (total_log_size_in_bytes - used_log_space_in_bytes) / 1024 / 1024 AS available_log_mb
FROM sys.dm_db_log_space_usage;

-- Check virtual log files
SELECT 
    DB_NAME(database_id) AS database_name,
    COUNT(*) AS total_vlfs,
    SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END) AS inactive_vlfs,
    SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) AS active_vlfs,
    SUM(CASE WHEN status = 2 THEN 1 ELSE 0 END) AS reusable_vlfs,
    MIN(size_in_bytes / 1024) AS min_vlf_size_kb,
    MAX(size_in_bytes / 1024) AS max_vlf_size_kb,
    AVG(size_in_bytes / 1024) AS avg_vlf_size_kb
FROM sys.dm_db_log_info(DB_ID())
GROUP BY database_id;
```

## Query Optimizer

### Query Processing Pipeline

Query optimizer là "brain" của SQL Server's query processing, responsible cho việc tạo efficient execution plans cho mỗi query. Optimizer takes a query (expressed in T-SQL), analyzes it, và produces a plan that specifies exactly how to execute the query. Quá trình này bao gồm nhiều stages, mỗi stage transforms query representation để cuối cùng produce an executable plan.

**Parsing**: Đầu tiên, query text được parsed thành a parse tree, xác nhận syntax correctness và identifying query components (SELECT, FROM, WHERE, etc.). Parse tree không check semantic validity (ví dụ: whether referenced tables actually exist).

**Binding**: Parse tree được bound against database metadata, resolving object names to actual objects và validating semantic correctness. Binding produces a logical tree representation của query.

**Optimization**: Query optimizer analyzes the bound tree và generates multiple candidate execution plans, estimate cost của mỗi plan dựa trên statistics về underlying data. Optimizer chọn plan với estimated lowest cost.

### Cost-Based Optimizer

SQL Server's optimizer là cost-based, meaning nó sử dụng cost estimates (based on I/O, CPU, và memory considerations) để select execution plan. Cost estimates được derived từ statistics về data distribution trong tables và indexes.

**Statistics**: Statistics objects chứa histogram và density information mô tả distribution of values trong indexed or computed columns. SQL Server automatically maintains statistics when data changes exceed thresholds. Statistics quality directly impacts optimizer's ability to generate good plans.

```sql
-- Check statistics for an index
DBCC SHOW_STATISTICS ('Orders', 'IX_Orders_Customer_Date');

-- List all statistics for a table with update dates
SELECT 
    s.name AS statistics_name,
    STATS_DATE(s.object_id, s.stats_id) AS last_updated,
    s.auto_created,
    s.user_created,
    s.no_recompute,
    sc.name AS leading_column,
    (SELECT COUNT(*) FROM sys.stats_columns WHERE object_id = s.object_id AND stats_id = s.stats_id) AS column_count
FROM sys.stats s
JOIN sys.stats_columns sc ON s.object_id = sc.object_id AND s.stats_id = sc.stats_id AND sc.stats_column_id = 1
WHERE s.object_id = OBJECT_ID('Orders')
ORDER BY STATS_DATE(s.object_id, s.stats_id);
```

**Cardinality Estimation**: Optimizer estimates number of rows một operator sẽ process dựa trên statistics và algebraic rules. Modern SQL Server versions (2014+) có multiple cardinality estimation (CE) models cho backward compatibility và testing purposes.

### Execution Plan Types

**Trivial Plan**: For simple queries, optimizer recognizes that only one reasonable plan exists và uses it directly without full optimization overhead.

**Forced Plan**: Administrators có thể force a specific plan using plan guides hoặc OPTION (USE PLAN), bypass optimizer's cost-based selection. This nên được sử dụng judiciously vì data distribution có thể change over time.

```sql
-- View estimated vs actual plan
SET SHOWPLAN_TEXT ON;
GO
SELECT * FROM Orders WHERE CustomerID = 100;
GO
SET SHOWPLAN_TEXT OFF;

-- View actual plan with runtime info
SET STATISTICS PROFILE ON;
GO
SELECT * FROM Orders WHERE CustomerID = 100;
GO
SET STATISTICS PROFILE OFF;

-- Use query store to force a plan
ALTER DATABASE YourDatabase SET QUERY_STORE = ON;
ALTER DATABASE YourDatabase SET QUERY_STORE (OPERATION_MODE = READ_WRITE);

-- Find a query in query store
SELECT 
    qsq.query_id,
    qsq.query_text_id,
    qrs.plan_id,
    qrs.runtime_stats_id,
    qrs.count_executions,
    qrs.avg_duration,
    qrs.avg_cpu_time,
    qsq.query_sql_text
FROM sys.query_store_query qsq
JOIN sys.query_store_query_stats qrs ON qsq.query_id = qrs.query_id
WHERE qsq.query_text_id = @query_text_id;

-- Force a specific plan
EXEC sp_query_store_force_plan @query_id = @query_id, @plan_id = @plan_id;
```

## High Availability Architecture

### Always On Availability Groups

Always On Availability Groups (AGs) là SQL Server's flagship high availability và disaster recovery solution, cung cấp enterprise-grade protection cho mission-critical databases. AGs allow một set of user databases (availability databases) được replicated across multiple SQL Server instances (replicas), với automatic failover capability và support for readable secondary replicas.

**Primary Replica**: Holds the read-write copy của availability databases. Tất cả write operations happen trên primary replica và được replicated asynchronously hoặc synchronously đến secondary replicas tùy thuộc vào availability mode.

**Secondary Replicas**: Hold read-only copies của databases (nếu configured for readable secondary) và serve as potential failover targets. Secondary replicas có thể be configured cho automatic backups.

**Availability Modes**:
- **Synchronous-Commit**: Changes phải be written to log on secondary replica trước khi transaction commits trên primary. Guarantees zero data loss nhưng tăng commit latency.
- **Asynchronous-Commit**: Transaction commits trên primary trước khi log được hardened trên secondary. Lower latency nhưng potential for data loss during failover.

```sql
-- Create an availability group
CREATE AVAILABILITY GROUP [ProductionAG]
WITH (AUTOMATED_BACKUP_PREFERENCE = SECONDARY)
FOR DATABASE [YourDatabase]
REPLICA ON 
    'SQLServer1' WITH (
        ENDPOINT_URL = 'TCP://SQLServer1.domain.com:5022',
        AVAILABILITY_MODE = SYNCHRONOUS_COMMIT,
        FAILOVER_MODE = AUTOMATIC,
        BACKUP_PRIORITY = 50,
        SECONDARY_ROLE(ALLOW_CONNECTIONS = READ_ONLY)
    ),
    'SQLServer2' WITH (
        ENDPOINT_URL = 'TCP://SQLServer2.domain.com:5022',
        AVAILABILITY_MODE = SYNCHRONOUS_COMMIT,
        FAILOVER_MODE = AUTOMATIC,
        BACKUP_PRIORITY = 50,
        SECONDARY_ROLE(ALLOW_CONNECTIONS = READ_ONLY)
    )
LISTENER 'ProductionAGListener' (
    WITH IP ((N'10.0.0.1', N'255.255.255.0'), (N'10.0.0.2', N'255.255.255.0')),
    PORT = 1433
);
```

### Failover Cluster Instances

Failover Cluster Instances (FCIs) provide high availability at the SQL Server instance level, protecting against both software failures và hardware failures. Unlike AGs which replicate databases, FCIs provide redundancy by having multiple nodes in a Windows Server Failover Cluster (WSFC), with SQL Server installed on all nodes but active on only one at a time.

**Shared Storage**: FCIs require shared storage (SAN) accessible from all cluster nodes. When failover occurs, storage remains accessible from the new primary node.

**Failover Process**: When primary node fails, WSFC triggers failover, SQL Server service starts on secondary node, và databases come online using storage attached to new node.

### Log Shipping

Log Shipping là một simpler HA/DR solution dựa trên periodic transaction log backups. Unlike AGs và FCIs, log shipping is database-level và does not provide automatic failover.

```sql
-- Configure log shipping on primary
BACKUP DATABASE [YourDatabase] 
TO DISK = '\\Share\LogShipping\YourDatabase_Full.bak' 
WITH COMPRESSION, CHECKSUM;

-- Restore with NORECOVERY on secondary
RESTORE DATABASE [YourDatabase]
FROM DISK = '\\Share\LogShipping\YourDatabase_Full.bak'
WITH NORECOVERY;

-- Configure log backup job on primary
EXEC sp_add_log_shipping_primary_database
    @database = 'YourDatabase',
    @backup_directory = '\\Share\LogShipping',
    @backup_share = '\\Share\LogShipping',
    @backup_job_name = 'LSBackup_YourDatabase',
    @retention_period = 4320,
    @backup_job_id = @backup_job_id OUTPUT,
    @backup_alert_job_id = @backup_alert_job_id OUTPUT;

-- Configure copy and restore jobs on secondary
EXEC sp_add_log_shipping_secondary_primary
    @primary_server = 'PrimaryServer',
    @primary_database = 'YourDatabase',
    @backup_source_directory = '\\Share\LogShipping',
    @backup_destination_directory = '\\Share\LogShipping\Restored',
    @copy_job_name = 'LSCopy_YourDatabase',
    @restore_job_name = 'LSRestore_YourDatabase',
    @file_retention_period = 4320;
```

## Replication Architecture

### Replication Types

SQL Server Replication cung cấp các solutions cho data distribution và data movement scenarios, khác với HA/DR solutions tập trung vào protection.

**Snapshot Replication**: Copies entire dataset at scheduled intervals. Appropriate for small databases, read-only data, hoặc when data changes are large relative to overall data size.

**Transactional Replication**: Replicates individual transactions as they occur on publisher. Provides near real-time data movement với minimal latency. Appropriate for scale-out scenarios và read-heavy workloads.

**Merge Replication**: Allows bidirectional changes, with conflict resolution when same data is modified on multiple sites. Appropriate for scenarios where remote sites need to modify data independently.

### Replication Components

**Publisher**: Database instance that makes data available for replication.

**Distributor**: Instance that receives transactions from publishers và stores them in distribution database before pushing to subscribers.

**Subscriber**: Instance that receives replicated data from publisher through distributor.

**Articles**: Individual database objects (tables, stored procedures, views) configured for replication.

```sql
-- Configure transactional replication
-- 1. Configure distributor
EXEC sp_adddistributor 
    @distributor = 'DistributorServer',
    @working_directory = 'C:\ReplData';

-- 2. Create publication
EXEC sp_addpublication
    @publication = 'OrdersPublication',
    @status = 'active',
    @allow_push = N'true',
    @allow_pull = N'true',
    @repl_freq = N'continuous';

-- 3. Add articles
EXEC sp_addarticle
    @publication = 'OrdersPublication',
    @article = 'Orders',
    @source_object = 'Orders',
    @destination_table = 'Orders',
    @type = N'logbased';

-- 4. Create subscription
EXEC sp_addsubscription
    @publication = 'OrdersPublication',
    @subscriber = 'SubscriberServer',
    @destination_db = 'OrdersReplica',
    @subscription_type = N'Push',
    @sync_type = N'automatic';
```

## Memory Architecture

### Memory Components

SQL Server's memory architecture consists of multiple components, each responsible for different aspects of data and query processing.

**Buffer Pool**: Lớn nhất component, cache data pages. Buffer pool size được controlled bởi max server memory setting và grows/shrinks dynamically based on workload.

**Plan Cache**: Stores compiled execution plans cho reuse. Plan cache reduces compilation overhead cho frequently executed queries nhưng excessive size có thể indicate plan reuse issues.

**Columnstore Segment Cache**: For databases using columnstore indexes, this component caches decompressed column segments for analytical query performance.

```sql
-- Check memory clerk breakdown
SELECT 
    mc.type AS memory_clerk_type,
    mc.name AS memory_clerk_name,
    mc.memory_node_id,
    mc.pages_kb / 1024 AS pages_mb,
    mc.virtual_memory_reserved_kb / 1024 AS vm_reserved_mb,
    mc.virtual_memory_committed_kb / 1024 AS vm_committed_mb,
    mc.awe_allocated_kb / 1024 AS awe_mb
FROM sys.dm_os_memory_clerks mc
WHERE mc.pages_kb > 0
ORDER BY pages_kb DESC;

-- Check plan cache
SELECT 
    cp.objtype AS plan_type,
    cp.usecounts AS reuse_count,
    COUNT(*) AS plan_count,
    SUM(cp.size_in_bytes) / 1024 / 1024 AS size_mb
FROM sys.dm_exec_cached_plans cp
GROUP BY cp.objtype
ORDER BY size_mb DESC;

-- Find expensive cached plans
SELECT 
    cp.objtype AS plan_type,
    cp.usecounts AS execution_count,
    cp.size_in_bytes / 1024 / 1024 AS plan_size_mb,
    qs.total_elapsed_time / qs.execution_count AS avg_elapsed_ms,
    qs.total_logical_reads / qs.execution_count AS avg_logical_reads,
    SUBSTRING(st.text, 1, 200) AS query_preview
FROM sys.dm_exec_cached_plans cp
JOIN sys.dm_exec_query_stats qs ON cp.plan_handle = qs.plan_handle
CROSS APPLY sys.dm_exec_sql_text(cp.plan_handle) st
WHERE cp.objtype IN ('Proc', 'Prepared')
ORDER BY qs.total_elapsed_time DESC;
```

### Memory Configuration

**max server memory**: Controls maximum amount of memory buffer pool can use. Should be set to leave adequate memory cho OS và other SQL Server components.

**min server memory**: Sets minimum memory cho buffer pool. SQL Server will not release memory below this threshold even under memory pressure.

```sql
-- Check current memory configuration
SELECT 
    name AS config_name,
    value AS config_value,
    value_in_use AS in_use_value,
    description
FROM sys.configurations
WHERE name LIKE '%memory%'
ORDER BY name;

-- Recommended max server memory calculation
-- Leave 4GB or 10% (whichever is larger) for OS, plus memory for other SQL components
-- For dedicated SQL Server with 128GB RAM:
-- max server memory = 128GB - 4GB = 124GB (approximately)
EXEC sp_configure 'max server memory', 130048;  -- In MB, 124GB
RECONFIGURE;
```

## Thread and Task Architecture

### SQL Server Scheduling

SQL Server uses a non-preemptive scheduling model where SQL Server worker threads voluntarily yield the CPU, allowing better control over resource distribution và reducing context switching overhead compared to preemptive scheduling.

**Scheduler**: Mỗi scheduler corresponds to a CPU core. Schedulers manage work items (tasks) và schedule them for execution on their associated CPU.

**Worker**: Worker threads execute tasks. Each worker is associated with exactly one scheduler. Number of workers được controlled bởi max worker threads setting.

**Task**: Represents a unit of work (ví dụ: a query batch). Tasks are assigned to workers for execution.

```sql
-- Check scheduler health
SELECT 
    scheduler_id,
    cpu_id,
    status,
    current_tasks_count,
    runnable_tasks_count,
    current_workers_count,
    active_workers_count,
    work_queue_count,
    pending_disk_io_count
FROM sys.dm_os_schedulers
WHERE status = 'VISIBLE ONLINE'
ORDER BY scheduler_id;

-- Check wait statistics
SELECT TOP 20
    wait_type,
    waiting_tasks_count,
    wait_time_ms,
    signal_wait_time_ms,
    wait_time_ms - signal_wait_time_ms AS resource_wait_ms,
    signal_wait_time_ms * 100.0 / NULLIF(wait_time_ms, 0) AS signal_wait_pct
FROM sys.dm_os_wait_stats
WHERE wait_time_ms > 0
    AND wait_type NOT IN (
        SELECT wait_type FROM sys.dm_os_wait_stats 
        WHERE wait_type LIKE 'XE%' OR wait_type LIKE 'SLEEP%'
    )
ORDER BY wait_time_ms DESC;
```

## Data Storage Architecture

### Columnstore Indexes

Columnstore indexes là một storage format optimized cho analytical workloads, store data column-by-column instead of row-by-row. This orientation provides significant compression benefits và allows efficient analytical queries that aggregate over specific columns without reading entire rows.

**Columnstore Format**: Data được compressed và stored in column segments, each containing values from one column for a range of rows (row groups). Segment elimination allows query processor to skip irrelevant segments without decompressing them.

**Batch Mode Execution**: Columnstore queries execute in "batch mode" where processing happens on batches of rows (typically 900 rows at a time), significantly reducing CPU overhead for analytical queries.

```sql
-- Create a columnstore index
CREATE NONCLUSTERED COLUMNSTORE INDEX IX_Orders_ColumnStore
ON Orders(OrderDate, CustomerID, TotalAmount, Status)
WHERE Status = 'Completed';  -- Filtered columnstore

-- Check columnstore segment information
SELECT 
    OBJECT_NAME(p.object_id) AS table_name,
    i.name AS index_name,
    ps.segment_id,
    ps.row_count,
    ps.used_in_row_store_count,
    ps.avg_compression_ratio,
    ps.min_data_id,
    ps.max_data_id
FROM sys.column_store_segments ps
JOIN sys.indexes i ON ps.object_id = i.object_id AND ps.index_id = i.index_id
JOIN sys.dm_db_partition_stats p ON ps.object_id = p.object_id AND ps.index_id = p.index_id
WHERE i.type IN (5, 6)  -- Columnstore indexes
ORDER BY OBJECT_NAME(ps.object_id), ps.segment_id;
```

## Troubleshooting Architecture Issues

### DMVs for Architecture Analysis

```sql
-- Check for missing indexes with high impact
SELECT 
    migs.avg_user_impact,
    migs.user_seeks,
    migs.user_scans,
    migs.avg_total_user_cost,
    mid.statement AS table_name,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns
FROM sys.dm_db_missing_index_details mid
JOIN sys.dm_db_missing_index_groups mig ON mid.index_handle = mig.index_handle
JOIN sys.dm_db_missing_index_group_stats migs ON mig.index_group_handle = migs.group_handle
WHERE migs.avg_user_impact > 50
    AND migs.user_seeks > 100
ORDER BY migs.avg_user_impact DESC;

-- Check for expensive operators in recent queries
SELECT 
    SUBSTRING(st.text, 1, 200) AS query_preview,
    qs.execution_count,
    qs.total_elapsed_time / 1000 AS total_elapsed_ms,
    qp.query_plan
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) st
CROSS APPLY sys.dm_exec_query_plan(qs.plan_handle) qp
WHERE qs.total_elapsed_time > 10000  -- Queries taking more than 10 seconds
ORDER BY qs.total_elapsed_time DESC;
```

## References

- SQL Server Documentation: https://docs.microsoft.com/en-us/sql/sql-server/
- Storage Engine: https://docs.microsoft.com/en-us/sql/relational-databases/pages-and-extents-architecture-guide
- Query Processing: https://docs.microsoft.com/en-us/sql/relational-databases/query-processing-architecture-guide
- Memory Architecture: https://docs.microsoft.com/en-us/sql/relational-databases/memory-management-architecture-guide
- Always On Architecture: https://docs.microsoft.com/en-us/sql/database-engine/availability-groups/windows/overview-of-always-on-availability-groups
- Columnstore Architecture: https://docs.microsoft.com/en-us/sql/relational-databases/backup-restore/back-up-and-restore-of-sql-server-databases
