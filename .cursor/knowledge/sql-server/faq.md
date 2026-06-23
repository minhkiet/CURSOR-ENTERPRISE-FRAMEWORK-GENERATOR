---
title: "SQL Server FAQ - Câu Hỏi Thường Gặp"
description: "Frequently asked questions about SQL Server with expert answers covering performance tuning, high availability, security, backup, indexing, and query optimization."
tags: ["sql-server", "faq", "performance", "database", "troubleshooting", "best-practices", "questions"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# SQL Server FAQ - Câu Hỏi Thường Gặp

## Tổng Quan (Overview)

Tài liệu này tổng hợp các câu hỏi thường gặp về SQL Server từ beginners đến advanced topics. Mỗi câu hỏi được trả lời chi tiết với giải thích về underlying concepts và practical solutions.

Các câu hỏi được phân loại theo chủ đề để dễ dàng tra cứu. Mỗi câu trả lời bao gồm không chỉ solution mà còn giải thích về lý do tại sao solution đó hoạt động và các alternatives có thể có.

## Performance và Query Optimization

### Q1: Làm thế nào để cải thiện performance của câu query chậm?

**Câu hỏi**: Tôi có một stored procedure chạy rất chậm, mất khoảng 30 giây. Làm thế nào để tìm và fix vấn đề?

**Trả lời**: Việc troubleshooting một câu query chậm nên được thực hiện theo systematic approach:

**Bước 1: Thu thập Execution Plan**

Đầu tiên, bạn cần hiểu SQL Server đang thực thi query như thế nào. Enable actual execution plan và chạy stored procedure:

```sql
-- Enable actual execution plan
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

-- Run the stored procedure
EXEC YourSlowStoredProcedure @Parameter1 = 'value1';

-- Review the plan for:
-- 1. Table scans (bad for large tables)
-- 2. Index scans (may be acceptable for small tables)
-- 3. Bookmark lookups (indicates missing covering index)
-- 4. Large row estimate differences (indicates statistics issues)
```

**Bước 2: Kiểm tra Missing Indexes**

SQL Server tự động tracking các indexes mà nó "wishes" có khi executing queries:

```sql
-- Find missing indexes with high impact
SELECT 
    migs.avg_user_impact AS improvement_pct,
    migs.user_seeks AS times_used,
    mid.statement AS table_name,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns,
    'CREATE INDEX IX_' + OBJECT_NAME(mid.object_id) + '_' +
    REPLACE(REPLACE(mid.equality_columns, '[', ''), ']', '') + 
    ' ON ' + OBJECT_NAME(mid.object_id) + 
    '(' + ISNULL(mid.equality_columns + ', ' + mid.inequality_columns, mid.inequality_columns) + ')' +
    CASE WHEN mid.included_columns IS NOT NULL 
         THEN ' INCLUDE (' + mid.included_columns + ')' 
         ELSE '' END AS suggested_index
FROM sys.dm_db_missing_index_details mid
JOIN sys.dm_db_missing_index_groups mig ON mid.index_handle = mig.index_handle
JOIN sys.dm_db_missing_index_group_stats migs ON mig.index_group_handle = migs.group_handle
WHERE migs.avg_user_impact > 30
ORDER BY migs.avg_user_impact DESC;
```

**Bước 3: Kiểm tra Statistics**

Out-of-date statistics có thể khiến optimizer tạo ra suboptimal plans:

```sql
-- Check statistics update dates
SELECT 
    OBJECT_NAME(s.object_id) AS table_name,
    s.name AS statistics_name,
    STATS_DATE(s.object_id, s.stats_id) AS last_updated,
    s.auto_created
FROM sys.stats s
WHERE OBJECTPROPERTY(s.object_id, 'IsUserTable') = 1
    AND STATS_DATE(s.object_id, s.stats_id) < DATEADD(DAY, -7, GETDATE())
ORDER BY STATS_DATE(s.object_id, s.stats_id);

-- Update statistics with FULLSCAN for better accuracy
UPDATE STATISTICS YourTable WITH FULLSCAN;
```

**Bước 4: Xem xét Query Rewrite**

Đôi khi query structure cần được cải thiện:

```sql
-- BAD: Using functions on columns prevents index usage
SELECT * FROM Orders WHERE YEAR(OrderDate) = 2024;

-- GOOD: Range query allows index usage
SELECT * FROM Orders 
WHERE OrderDate >= '2024-01-01' AND OrderDate < '2025-01-01';

-- BAD: Using OR can prevent index usage
SELECT * FROM Orders WHERE CustomerID = 1 OR CustomerID = 2;

-- GOOD: IN is often better
SELECT * FROM Orders WHERE CustomerID IN (1, 2);
```

### Q2: Sự khác biệt giữa clustered và non-clustered index là gì?

**Câu hỏi**: Tôi mới bắt đầu với SQL Server và không hiểu rõ sự khác biệt giữa clustered và non-clustered indexes. Khi nào nên sử dụng loại nào?

**Trả lời**: Đây là một trong những khái niệm fundamental nhất trong SQL Server indexing.

**Clustered Index:**

- **Cách hoạt động**: Data rows được sắp xếp và lưu trữ vật lý theo thứ tự của index key. Giống như sắp xếp một cuốn sách theo thứ tự alphabet - mỗi trang được đặt đúng vị trí.
- **Số lượng**: Mỗi table chỉ có thể có một clustered index vì data chỉ có thể được sắp xếp theo một thứ tự vật lý duy nhất.
- **Hiệu suất đọc**: Cực kỳ nhanh cho các truy vấn lấy rows bằng clustered key hoặc range queries trên clustered key.
- **Hiệu suất ghi**: INSERT, UPDATE, DELETE có thể chậm hơn vì data cần được chèn vào đúng vị trí, có thể gây page splits.

```sql
-- Clustered index on primary key (common pattern)
CREATE TABLE Orders (
    OrderID INT IDENTITY(1,1) PRIMARY KEY,  -- This becomes clustered
    CustomerID INT NOT NULL,
    OrderDate DATETIME NOT NULL,
    TotalAmount DECIMAL(10,2) NOT NULL
);

-- Explicitly create clustered index on different column
CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,  -- Non-clustered PK by default
    CustomerID INT NOT NULL,
    TransactionDate DATETIME NOT NULL
);

CREATE CLUSTERED INDEX IX_Transactions_Date 
ON Transactions(TransactionDate);
```

**Non-Clustered Index:**

- **Cách hoạt động**: Là một cấu trúc riêng biệt chứa index key values và pointers (bookmarks) chỉ đến vị trí của data row trong clustered index hoặc heap.
- **Số lượng**: Một table có thể có nhiều non-clustered indexes (tối đa 999 non-clustered indexes).
- **Hiệu suất đọc**: Tốt cho các truy vấn tìm kiếm trên indexed columns. Nếu query chỉ cần columns có trong index, có thể served hoàn toàn từ index (index-only scan).
- **Hiệu suất ghi**: INSERT, UPDATE, DELETE cần cập nhật tất cả indexes, có thể làm chậm write operations.

```sql
-- Non-clustered index on foreign key
CREATE NONCLUSTERED INDEX IX_Orders_CustomerID 
ON Orders(CustomerID);

-- Covering non-clustered index (includes all needed columns)
CREATE NONCLUSTERED INDEX IX_Orders_Customer_Covering
ON Orders(CustomerID, OrderDate)
INCLUDE (TotalAmount);

-- Now this query can be served entirely from the index:
SELECT OrderDate, TotalAmount 
FROM Orders 
WHERE CustomerID = @CustomerID;
```

**Khi nào sử dụng loại nào?**

| Scenario | Recommended Index Type |
|----------|----------------------|
| Primary key lookup | Clustered (usually) |
| Range queries (dates, sequential) | Clustered |
| JOINs on primary key | Clustered |
| Foreign key lookups | Non-clustered |
| Covering specific queries | Non-clustered with INCLUDE |
| Highly selective queries | Non-clustered |

### Q3: Parameter Sniffing là gì và làm thế nào để xử lý nó?

**Câu hỏi**: Tôi có một stored procedure chạy nhanh khi tôi test với một giá trị nhưng chạy rất chậm với giá trị khác. Đây có phải là parameter sniffing không?

**Trả lời**: Đúng vậy, đây là classic parameter sniffing problem.

**Giải thích**: Khi stored procedure được compiled lần đầu tiên, SQL Server optimizer "sniffs" giá trị parameters và sử dụng nó để tạo execution plan. Plan này sau đó được cached và reused cho tất cả subsequent executions, bất kể parameter values khác nhau.

Ví dụ, nếu bạn có stored procedure tìm orders theo CustomerID:

```sql
CREATE PROCEDURE GetCustomerOrders
    @CustomerID INT
AS
BEGIN
    SELECT OrderID, OrderDate, TotalAmount
    FROM Orders
    WHERE CustomerID = @CustomerID
    ORDER BY OrderDate DESC;
END;
```

- Khi @CustomerID = 1 (có 5 orders): Plan sử dụng index seek vì optimizer expect chỉ few rows.
- Khi @CustomerID = 2 (có 500,000 orders): Same plan được reuse, nhưng giờ nó rất inefficient.

**Solutions:**

**Solution 1: OPTIMIZE FOR UNKNOWN**
Khuyến khích optimizer tạo plan dựa trên average statistics:

```sql
CREATE PROCEDURE GetCustomerOrders_Optimized
    @CustomerID INT
AS
BEGIN
    SELECT OrderID, OrderDate, TotalAmount
    FROM Orders
    WHERE CustomerID = @CustomerID
    ORDER BY OrderDate DESC
    OPTION (OPTIMIZE FOR UNKNOWN);
END;
```

**Solution 2: OPTIMIZE FOR specific value**
Nếu bạn biết có một giá trị phổ biến hơn:

```sql
CREATE PROCEDURE GetCustomerOrders
    @CustomerID INT
AS
BEGIN
    SELECT OrderID, OrderDate, TotalAmount
    FROM Orders
    WHERE CustomerID = @CustomerID
    ORDER BY OrderDate DESC
    OPTION (OPTIMIZE FOR (@CustomerID = 1));  -- Optimize for typical customer
END;
```

**Solution 3: RECOMPILE**
Tạo mới plan mỗi lần execution:

```sql
CREATE PROCEDURE GetCustomerOrders
    @CustomerID INT
AS
BEGIN
    SELECT OrderID, OrderDate, TotalAmount
    FROM Orders
    WHERE CustomerID = @CustomerID
    ORDER BY OrderDate DESC
    OPTION (RECOMPILE);  -- New plan each execution
END;
```

**Solution 4: Query Store**
Force specific plan cho problematic queries:

```sql
-- Enable Query Store
ALTER DATABASE YourDB SET QUERY_STORE = ON;

-- Force a better plan
EXEC sp_query_store_force_plan 
    @query_id = 123,  -- The query_id
    @plan_id = 456;  -- The plan_id to force
```

### Q4: Làm thế nào để giảm blocking và deadlock?

**Câu hỏi**: Ứng dụng của tôi gặp tình trạng blocking nghiêm trọng và đôi khi có deadlocks. Làm thế nào để giải quyết?

**Trả lời**: Blocking và deadlocks có causes khác nhau và cần approaches khác nhau.

**Understanding Blocking:**

Blocking xảy ra khi một transaction hold locks mà transaction khác cần. Đây là hành vi bình thường của locking mechanism, nhưng trở thành vấn đề khi nó kéo dài quá lâu.

```sql
-- Find blocking chains
SELECT 
    blocked.session_id AS blocked_session_id,
    blocker.session_id AS blocking_session_id,
    blocker.login_name AS blocking_login,
    blocked.status AS blocked_status,
    blocker.status AS blocker_status,
    blocked.wait_type AS blocked_wait,
    blocker.wait_type AS blocker_wait,
    blocked.wait_time AS blocked_wait_ms,
    SUBSTRING(blocked_text.text, 1, 200) AS blocked_query,
    SUBSTRING(blocker_text.text, 1, 200) AS blocker_query
FROM sys.dm_exec_requests blocked
CROSS APPLY sys.dm_exec_sql_text(blocked.sql_handle) blocked_text
JOIN sys.dm_exec_sessions blocker ON blocked.blocking_session_id = blocker.session_id
OUTER APPLY sys.dm_exec_sql_text(blocker.sql_handle) blocker_text
WHERE blocked.blocking_session_id > 0;
```

**Reducing Blocking:**

1. **Use appropriate isolation level:**
   ```sql
   -- Enable Read Committed Snapshot (RCSI)
   ALTER DATABASE YourDatabase SET READ_COMMITTED_SNAPSHOT ON;
   ```
   RCSI uses row versioning thay vì blocking readers với writers.

2. **Keep transactions short:**
   ```sql
   -- BAD: Long-running transaction
   BEGIN TRANSACTION;
   SELECT * FROM LargeTable;  -- Acquires shared locks
   -- Application processing here
   UPDATE LargeTable SET Column = 'value';  -- Waits for previous locks
   COMMIT;
   
   -- GOOD: Short transactions
   BEGIN TRANSACTION;
   UPDATE LargeTable SET Column = 'value';
   COMMIT;
   ```

3. **Access tables in consistent order:**
   ```sql
   -- Always access tables in same order to prevent deadlocks
   -- Transaction 1: TableA then TableB
   -- Transaction 2: TableA then TableB (consistent order prevents deadlock)
   ```

4. **Use appropriate indexes:**
   Missing indexes cause more rows to be locked than necessary.

**Handling Deadlocks:**

```sql
-- Log deadlock information
-- Deadlocks are automatically logged to ERRORLOG
EXEC sp_readerrorlog;

-- Enable deadlock trace
DBCC TRACEON (1222, -1);  -- Returns deadlock graph in XML format

-- Or use extended events
CREATE EVENT SESSION DeadlockMonitor ON SERVER
ADD EVENT sqlserver.xml_deadlock_report
ADD TARGET package0.event_file(SET filename='deadlock.xel');
```

### Q5: Khi nào nên sử dụng table variable vs temp table?

**Câu hỏi**: Tôi thấy có table variable (@TableName) và temp table (#TableName). Khi nào nên sử dụng cái nào?

**Trả lời**: Đây là một câu hỏi phổ biến với một số khác biệt quan trọng:

**Table Variables (@TableName):**

```sql
DECLARE @Products TABLE (
    ProductID INT PRIMARY KEY,
    ProductName NVARCHAR(100),
    Price DECIMAL(10,2)
);

INSERT INTO @Products VALUES (1, 'Product A', 10.00);
```

**Characteristics:**
- Scope: Chỉ visible trong batch/procedure hiện tại
- Statistics: Không có statistics, optimizer assumes 1 row
- Indexes: Chỉ có thể có PRIMARY KEY và UNIQUE constraints tại declaration time
- Logging: Minimal logging (nhưng transaction log vẫn được sử dụng)
- Parallelism: Queries using table variables không parallelized

**Temp Tables (#TableName):**

```sql
CREATE TABLE #Products (
    ProductID INT PRIMARY KEY,
    ProductName NVARCHAR(100),
    Price DECIMAL(10,2)
);

INSERT INTO #Products VALUES (1, 'Product A', 10.00);
```

**Characteristics:**
- Scope: Visible trong session (local) hoặc across sessions (global)
- Statistics: Có statistics, auto-created as rows are inserted
- Indexes: Có thể tạo indexes bất kỳ lúc nào
- Logging: Full logging trong tempdb
- Parallelism: Full support cho parallel query plans

**When to use Table Variables:**

- Khi dataset nhỏ và stable (thường < 1000 rows)
- Khi không cần indexes đặc biệt
- Khi muốn hạn chế scope (tránh accidentally access từ nơi khác)
- Trong functions (table variables được phép, temp tables không)

**When to use Temp Tables:**

- Khi dataset lớn hoặc có thể grow significantly
- Khi cần complex indexes hoặc statistics cho query optimization
- Khi cần reference table multiple times trong procedure
- Khi cần use in dynamic SQL hoặc pass between procedures
- Khi cần parallel query execution

**Performance Considerations:**

```sql
-- For small tables (< 100 rows), table variables often faster
-- due to reduced overhead

-- For larger tables, temp tables usually perform better
-- due to proper statistics

-- Hybrid approach: Start with table variable, convert if needed
DECLARE @Results TABLE (ID INT, Value NVARCHAR(50));
INSERT INTO @Results SELECT ID, Value FROM SourceTable;

-- If table grows large, switch to temp table
CREATE TABLE #Results (ID INT PRIMARY KEY, Value NVARCHAR(50));
INSERT INTO #Results SELECT ID, Value FROM SourceTable;
```

## High Availability và Disaster Recovery

### Q6: Sự khác biệt giữa Always On AG và Failover Cluster Instance là gì?

**Câu hỏi**: Tôi đang lên kế hoạch cho HA solution. Nên chọn Always On Availability Groups hay Failover Cluster Instances?

**Trả lời**: Đây là hai solutions khác nhau cho các use cases khác nhau:

**Failover Cluster Instance (FCI):**

- **Protection level**: Instance-level
- **Storage**: Requires shared storage (SAN) accessible từ tất cả nodes
- **Failover time**: Minutes
- **Data loss on failover**: Zero (same databases)
- **Readable secondaries**: Không (primary node only)

```sql
-- FCI is configured at Windows/cluster level, not T-SQL
-- Example: Creating a database on FCI
USE [master];
GO
CREATE DATABASE [MyDatabase] ON PRIMARY
( NAME = N'MyDatabase', FILENAME = N'S:\Data\MyDatabase.mdf')
LOG ON
( NAME = N'MyDatabase_log', FILENAME = N'S:\Logs\MyDatabase_log.ldf');
```

**Always On Availability Groups (AG):**

- **Protection level**: Database-level
- **Storage**: Each replica có its own storage (no shared storage required)
- **Failover time**: Seconds to minutes (automatic)
- **Data loss on failover**: Varies (zero for sync, potential for async)
- **Readable secondaries**: Yes (if configured)

```sql
-- Create Availability Group (PowerShell/config wizard primarily)
-- Example of connecting to AG listener
-- Connection string should use listener name, not physical server

-- Test connection to AG
SELECT @@SERVERNAME;  -- Returns current replica
SELECT 
    @@SERVERNAME AS CurrentReplica,
    SERVERPROPERTY('ServerName') AS PhysicalServer;
```

**So sánh chi tiết:**

| Feature | FCI | Always On AG |
|---------|-----|-------------|
| Protects | Entire instance | Specific databases |
| Storage | Shared (SAN) | Independent per replica |
| Setup complexity | Medium | High |
| Automatic failover | Yes | Yes (with sync mode) |
| Read-scale out | No | Yes |
| Cross-subnet DR | No | Yes |
| Backup on secondary | No | Yes |
| Multiple AGs | No | Yes |

**Recommendation:**

- **Use FCI** khi:
  - Cần protect entire instance
  - Đã có shared storage infrastructure
  - Đơn giản hóa management (single database set)
  - Cần protect system databases

- **Use AG** khi:
  - Cần database-level protection
  - Cần read-scale out
  - Cần geographic distribution
  - Muốn mix sync và async replicas
  - Cần selective database protection

### Q7: Làm thế nào để chọn recovery model phù hợp?

**Câu hỏi**: Tôi nên sử dụng FULL, SIMPLE hay BULK_LOGGED recovery model?

**Trả lời**: Việc chọn recovery model phụ thuộc vào RPO requirements và workload characteristics:

**SIMPLE Recovery Model:**

```sql
-- Set to SIMPLE
ALTER DATABASE YourDatabase SET RECOVERY SIMPLE;
```

- **Log backups**: Không cần
- **Point-in-time recovery**: Không hỗ trợ
- **Log truncation**: Tự động sau mỗi checkpoint
- **Use cases**: Development databases, non-critical data, small databases where backups are impractical

**FULL Recovery Model:**

```sql
ALTER DATABASE YourDatabase SET RECOVERY FULL;
```

- **Log backups**: Required để truncate log
- **Point-in-time recovery**: Hỗ trợ đầy đủ
- **Log truncation**: Chỉ sau log backup
- **Use cases**: Production databases requiring no data loss, databases with critical transactions

```sql
-- Full backup
BACKUP DATABASE YourDatabase TO DISK = 'D:\Backups\Full.bak';

-- Log backup
BACKUP LOG YourDatabase TO DISK = 'D:\Backups\Log.trn';

-- Point-in-time restore
RESTORE DATABASE YourDatabase 
FROM DISK = 'D:\Backups\Full.bak'
WITH NORECOVERY;

RESTORE LOG YourDatabase 
FROM DISK = 'D:\Backups\Log1.trn'
WITH NORECOVERY;

RESTORE LOG YourDatabase 
FROM DISK = 'D:\Backups\Log2.trn'
WITH STOPAT = '2024-06-20 14:30:00';
```

**BULK_LOGGED Recovery Model:**

```sql
ALTER DATABASE YourDatabase SET RECOVERY BULK_LOGGED;
```

- **Log backups**: Required
- **Point-in-time recovery**: Limited (không thể point-in-time trong bulk operations)
- **Logging**: Minimal logging cho SELECT INTO, BULK INSERT, CREATE INDEX, etc.
- **Use cases**: Databases with periodic bulk operations (ETL, data imports)

**Decision Matrix:**

| Factor | SIMPLE | FULL | BULK_LOGGED |
|--------|--------|------|-------------|
| Data loss tolerance | Hours | Zero | Minutes to hours |
| Point-in-time recovery | No | Yes | Limited |
| Bulk operation performance | Normal | Normal | Better |
| Log backup overhead | None | High | Medium |
| Compliance requirements | Low | High | Medium |

### Q8: Làm thế nào để test backup và restore?

**Câu hỏi**: Tôi có backup schedule đầy đủ nhưng chưa bao giờ test restore. Làm thế nào để verify backups có thể restore được?

**Trả lời**: Testing backups là một trong những critical maintenance tasks nhưng thường bị neglect:

**Step 1: Verify Backup Integrity**

```sql
-- Verify backup file before relying on it
RESTORE VERIFYONLY 
FROM DISK = 'D:\Backups\YourDatabase_Full.bak'
WITH CHECKSUM;

-- Check backup history
SELECT 
    bs.backup_set_id,
    bs.database_name,
    bs.backup_start_date,
    bs.backup_finish_date,
    CASE bs.type
        WHEN 'D' THEN 'Full'
        WHEN 'I' THEN 'Differential'
        WHEN 'L' THEN 'Log'
    END AS backup_type,
    bs.is_damaged,
    bs.has_backup_checksums,
    bm.physical_device_name
FROM msdb.dbo.backupset bs
JOIN msdb.dbo.backupmediafamily bm ON bs.media_set_id = bm.media_set_id
WHERE bs.database_name = 'YourDatabase'
ORDER BY bs.backup_start_date DESC;
```

**Step 2: Perform Test Restore**

```sql
-- Test restore to alternate location
RESTORE DATABASE YourDatabase_TestRestore
FROM DISK = 'D:\Backups\YourDatabase_Full.bak'
WITH MOVE 'YourDatabase_Data' TO 'D:\TestRestore\YourDatabase.mdf',
     MOVE 'YourDatabase_Log' TO 'D:\TestRestore\YourDatabase_log.ldf',
     NORECOVERY;

-- If you have differential backups
RESTORE DATABASE YourDatabase_TestRestore
FROM DISK = 'D:\Backups\YourDatabase_Diff.bak'
WITH NORECOVERY;

-- Restore log backups in sequence
RESTORE LOG YourDatabase_TestRestore
FROM DISK = 'D:\Backups\YourDatabase_Log1.trn'
WITH NORECOVERY;

RESTORE LOG YourDatabase_TestRestore
FROM DISK = 'D:\Backups\YourDatabase_Log2.trn'
WITH RECOVERY;

-- Verify database is accessible
USE YourDatabase_TestRestore;
SELECT COUNT(*) FROM sys.tables;
```

**Step 3: Document Test Results**

Tạo documentation bao gồm:
- Date of test
- Backup files used
- Time taken to restore
- Any issues encountered
- RTO achieved

**Step 4: Automate Regular Testing**

```sql
-- Create a SQL Agent job to automate restore testing
-- Schedule: Weekly or after major deployments

USE msdb;
GO

EXEC dbo.sp_add_job
    @job_name = N'Database Restore Test',
    @enabled = 1,
    @description = N'Test restore of critical databases';

EXEC sp_add_jobstep
    @job_name = N'Database Restore Test',
    @step_name = N'Restore Test',
    @subsystem = N'TSQL',
    @command = N'EXEC dbo.usp_TestDatabaseRestore',
    @database_name = N'msdb';
```

## Security

### Q9: Làm thế nào để implement principle of least privilege?

**Câu hỏi**: Tôi muốn implement principle of least privilege cho SQL Server applications. Làm thế nào để bắt đầu?

**Trả lời**: Principle of least privilege yêu cầu mỗi user và application chỉ có đủ permissions để thực hiện công việc của nó, không hơn không kém.

**Step 1: Audit Current Permissions**

```sql
-- List all server logins và their roles
SELECT 
    sp.name AS login_name,
    sp.type_desc,
    sp.is_disabled,
    STUFF((
        SELECT ', ' + spr.name
        FROM sys.server_role_members srm
        JOIN sys.server_principals spr ON srm.role_principal_id = spr.principal_id
        WHERE srm.member_principal_id = sp.principal_id
        FOR XML PATH('')
    ), 1, 2, '') AS server_roles
FROM sys.server_principals sp
WHERE sp.type IN ('S', 'U')
ORDER BY sp.name;

-- List all database users và their permissions
SELECT 
    dp.name AS user_name,
    dp.type_desc,
    STUFF((
        SELECT ', ' + dpr.name
        FROM sys.db_role_members drm
        JOIN sys.database_principals dpr ON drm.role_principal_id = dpr.principal_id
        WHERE drm.member_principal_id = dp.principal_id
        FOR XML PATH('')
    ), 1, 2, '') AS db_roles
FROM sys.database_principals dp
WHERE dp.type IN ('S', 'U', 'G')
ORDER BY dp.name;

-- List explicit permissions
SELECT 
    dp.name AS principal_name,
    dp.type_desc,
    o.name AS object_name,
    pm.permission_name,
    pm.state_desc
FROM sys.database_permissions pm
JOIN sys.database_principals dp ON pm.grantee_principal_id = dp.principal_id
LEFT JOIN sys.objects o ON pm.major_id = o.object_id
WHERE dp.type IN ('S', 'U', 'G')
ORDER BY dp.name, o.name;
```

**Step 2: Create Application Roles**

```sql
-- Create role for each application/function
CREATE APPLICATION ROLE AppRole_OrderEntry
    WITH PASSWORD = 'StrongPassword123!';

-- Grant only necessary permissions
GRANT SELECT, INSERT, UPDATE ON SCHEMA::Sales TO AppRole_OrderEntry;
GRANT EXECUTE ON SCHEMA::Sales TO AppRole_OrderEntry;

-- Deny permissions not needed
DENY DELETE ON SCHEMA::Sales TO AppRole_OrderEntry;
DENY ALTER ON SCHEMA::Sales TO AppRole_OrderEntry;

-- Application connects using application role
EXEC sp_setapprole 'AppRole_OrderEntry', 'StrongPassword123!';
```

**Step 3: Use Stored Procedures for Data Access**

```sql
-- Instead of granting table access directly,
-- grant EXECUTE on stored procedures

CREATE PROCEDURE Sales.GetCustomerOrders
    @CustomerID INT
AS
BEGIN
    SELECT OrderID, OrderDate, TotalAmount
    FROM Sales.Orders
    WHERE CustomerID = @CustomerID;
END;

GRANT EXECUTE ON Sales.GetCustomerOrders TO AppRole_OrderEntry;

-- Application only needs:
-- GRANT EXECUTE ON SCHEMA::Sales TO AppRole_OrderEntry;
```

**Step 4: Implement Contained Database Authentication**

```sql
-- Enable contained database for easier user management
ALTER DATABASE YourDatabase SET containment = partial;

-- Create user without server login
CREATE USER AppUser WITH PASSWORD = 'ComplexPassword123!';

-- Assign to role
ALTER ROLE AppRole_OrderEntry ADD MEMBER AppUser;

-- Now user authentication is at database level, not server level
```

### Q10: Làm thế nào để protect sensitive data?

**Câu hỏi**: Tôi cần protect sensitive columns như credit card numbers và SSN. SQL Server có features nào để hỗ trợ?

**Trả lời**: SQL Server cung cấp nhiều layers của data protection:

**Layer 1: Transparent Data Encryption (TDE)**

Encrypts entire database at rest:

```sql
-- Create master key
USE master;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'ComplexMasterKey123!';

-- Create certificate
CREATE CERTIFICATE MyServerCert 
WITH SUBJECT = 'Database Encryption Certificate';

-- Create encryption key
USE YourDatabase;
CREATE DATABASE ENCRYPTION KEY
WITH ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE MyServerCert;

-- Enable TDE
ALTER DATABASE YourDatabase SET ENCRYPTION ON;

-- Monitor encryption status
SELECT 
    database_name = DB_NAME(database_id),
    encryption_state_desc,
    percent_complete,
    key_algorithm,
    encryption_type_desc
FROM sys.dm_database_encryption_keys;
```

**Layer 2: Always Encrypted**

Encrypts data at column level, keys never exposed to SQL Server:

```sql
-- Create column master key
CREATE COLUMN MASTER KEY CMK_PaymentInfo
WITH (
    KEY_STORE_PROVIDER_NAME = 'MSSQL_CERTIFICATE_STORE',
    KEY_PATH = 'CurrentUser/My/CustomerPaymentKey'
);

-- Create column encryption key
CREATE COLUMN ENCRYPTION KEY CEK_PaymentInfo
WITH VALUES (
    COLUMN_MASTER_KEY = CMK_PaymentInfo,
    ALGORITHM = 'RSA_OAEP',
    ENCRYPTED_VALUE = 0x...  -- Encrypted by column master key
);

-- Create table with encrypted columns
CREATE TABLE Payments (
    PaymentID INT IDENTITY PRIMARY KEY,
    CustomerID INT,
    CardNumberEncrypted CHAR(8000) COLLATE Latin1_General_BIN2 
        ENCRYPTED WITH (
            COLUMN_ENCRYPTION_KEY = CEK_PaymentInfo,
            ENCRYPTION_TYPE = DETERMINISTIC,
            ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256'
        ),
    CardLast4 CHAR(4),
    ExpiryDate CHAR(4)
);

-- Application must use parameterized queries with Always Encrypted
-- Connection string: Column Encryption Setting=enabled
```

**Layer 3: Row-Level Security (RLS)**

Limit rows visible to different users:

```sql
-- Create function to filter rows based on user
CREATE FUNCTION dbo.fn_security predicate(@SalesRepID INT)
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN SELECT 1 AS fn_security_predicate
WHERE @SalesRepID = CAST(SESSION_CONTEXT(N'SalesRepID') AS INT)
    OR IS_ROLEMEMBER('SalesManager') = 1;

-- Apply security policy to table
CREATE SECURITY POLICY Sales.SalesQuotaPolicy
ADD FILTER PREDICATE dbo.fn_security_predicate(SalesRepID)
ON Sales.SalesQuota
WITH (STATE = ON);

-- Application sets user context
EXEC sp_set_session_context @key = N'SalesRepID', @value = @CurrentUserID;
```

## Administration

### Q11: Làm thế nào để monitor SQL Server performance?

**Câu hỏi**: Tôi cần monitor SQL Server production environment. Nên theo dõi những metrics nào?

**Trả lời**: Comprehensive monitoring bao gồm nhiều layers:

**Resource Utilization:**

```sql
-- CPU and Memory usage
SELECT 
    @@SERVERNAME AS ServerName,
    (SELECT COUNT(*) FROM sys.dm_exec_requests) AS ActiveRequests,
    (SELECT COUNT(*) FROM sys.dm_exec_sessions WHERE status = 'runnable') AS RunnableTasks,
    (SELECT COUNT(*) FROM sys.dm_exec_sessions WHERE status = 'suspended') AS SuspendedTasks,
    (SELECT COUNT(*) FROM sys.dm_exec_requests WHERE blocking_session_id > 0) AS BlockedRequests;

-- Buffer pool usage
SELECT 
    COUNT(*) * 8 / 1024 AS BufferPoolSize_GB,
    SUM(CONVERT(BIGINT, free_space_in_bytes)) / 1024 / 1024 / 1024 AS FreeSpace_GB
FROM sys.dm_os_buffer_descriptors
WHERE database_id = DB_ID();
```

**Wait Statistics:**

```sql
-- Top wait types
SELECT TOP 15
    wait_type,
    waiting_tasks_count,
    wait_time_ms,
    signal_wait_time_ms,
    wait_time_ms - signal_wait_time_ms AS resource_wait_ms,
    CAST(100.0 * wait_time_ms / SUM(wait_time_ms) OVER() AS DECIMAL(5,2)) AS wait_pct
FROM sys.dm_os_wait_stats
WHERE wait_time_ms > 0
    AND wait_type NOT LIKE 'XE%'
ORDER BY wait_time_ms DESC;
```

**Top Queries:**

```sql
-- Most expensive queries by total time
SELECT TOP 20
    qs.execution_count,
    qs.total_elapsed_time / 1000 AS total_elapsed_ms,
    qs.total_elapsed_time / (qs.execution_count * 1000) AS avg_elapsed_ms,
    qs.total_logical_reads / qs.execution_count AS avg_logical_reads,
    qs.total_physical_reads / qs.execution_count AS avg_physical_reads,
    SUBSTRING(st.text, 1, 300) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) st
WHERE qs.execution_count > 10
ORDER BY qs.total_elapsed_time DESC;
```

**Key Metrics to Monitor:**

| Category | Metrics | Warning Threshold |
|----------|---------|------------------|
| CPU | Processor Queue Length, % Processor Time | >80% sustained |
| Memory | Buffer Cache Hit Ratio, Page Life Expectancy | <300 seconds |
| Disk | Avg Disk sec/Read, Avg Disk sec/Write | >20ms for OLTP |
| Blocking | Blocked processes, Lock waits | Any sustained blocking |
| Availability | Database online status, Job success | Any failures |
| Capacity | Data file growth, Log file growth | >80% space used |

### Q12: Tempdb có nên được configure đặc biệt không?

**Câu hỏi**: Tôi nghe nói tempdb cần special configuration. Điều gì cần lưu ý?

**Trả lời**: Tempdb thường là bottleneck trong busy SQL Server environments vì nó được sử dụng bởi tất cả databases cho temporary objects, sorting, versioning, và các operations khác.

**Configuration Recommendations:**

1. **Multiple data files**: Một data file per CPU core (up to 8):

```sql
-- Check current tempdb files
SELECT 
    name AS file_name,
    physical_name,
    size * 8 / 1024 AS size_mb,
    growth * 8 / 1024 AS growth_mb
FROM sys.master_files
WHERE database_id = DB_ID('tempdb');

-- Add additional tempdb data files (run during maintenance window)
ALTER DATABASE tempdb ADD FILE (
    NAME = tempdev2,
    FILENAME = 'S:\Data\tempdb2.ndf',
    SIZE = 8192MB,
    FILEGROWTH = 64MB
);

ALTER DATABASE tempdb ADD FILE (
    NAME = tempdev3,
    FILENAME = 'S:\Data\tempdb3.ndf',
    SIZE = 8192MB,
    FILEGROWTH = 64MB
);
```

2. **Size appropriately**: Pre-size tempdb để tránh autogrowth:

```sql
-- Set initial size large enough for typical workload
ALTER DATABASE tempdb MODIFY FILE (
    NAME = tempdev,
    SIZE = 10240MB  -- 10GB, adjust based on workload
);

ALTER DATABASE tempdb MODIFY FILE (
    NAME = templog,
    SIZE = 5120MB  -- 5GB
);
```

3. **Trace flags**: Enable trace flags for tempdb optimization:

```sql
-- Recommended trace flags for tempdb
DBCC TRACEON (1118, -1);  -- Uniform extent allocation (SQL 2014 and earlier)
DBCC TRACEON (1117, -1);  -- Auto-grow all files together (SQL 2014 and earlier)

-- For SQL 2016+, these are enabled by default
```

4. **Remove from resource governor** if using:

```sql
-- Ensure tempdb not affected by resource governor
ALTER RESOURCE GOVERNOR RESET STATISTICS;
```

5. **Monitor tempdb usage:**

```sql
-- Check space used by temporary objects
SELECT 
    SUM(user_object_reserved_page_count) * 8 / 1024 AS user_objects_mb,
    SUM(internal_object_reserved_page_count) * 8 / 1024 AS internal_objects_mb,
    SUM(version_store_reserved_page_count) * 8 / 1024 AS version_store_mb,
    SUM(unallocated_extent_page_count) * 8 / 1024 AS free_space_mb
FROM sys.dm_db_file_space_usage
WHERE database_id = 2;

-- Check for active tempdb objects
SELECT 
    s.session_id,
    s.host_name,
    s.login_name,
    t.text AS query_text,
    te.total_elapsed_time / 1000 AS elapsed_seconds
FROM sys.dm_exec_sessions s
JOIN sys.dm_exec_requests r ON s.session_id = r.session_id
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
JOIN sys.dm_db_task_space_usage te ON s.session_id = te.session_id
WHERE te.database_id = 2
ORDER BY te.total_allocated_extent_page_count DESC;
```

## Best Practices

### Q13: Best practices cho stored procedure development là gì?

**Câu hỏi**: Tôi muốn viết stored procedures tốt. Có checklist nào để follow không?

**Trả lời**: Đây là comprehensive best practices:

**1. Include proper headers:**

```sql
CREATE OR ALTER PROCEDURE Sales.usp_GetCustomerOrders
    @CustomerID INT,
    @StartDate DATE = NULL,
    @EndDate DATE = NULL,
    @MaxRows INT = 1000
/*
    =================================================================
    Procedure: Sales.usp_GetCustomerOrders
    Created:   2024-06-20
    Author:    John Smith
    Purpose:   Retrieve orders for a specific customer
    
    Parameters:
        @CustomerID  - Customer identifier (required)
        @StartDate   - Filter orders from this date (optional)
        @EndDate     - Filter orders until this date (optional)
        @MaxRows     - Maximum rows to return (default 1000)
    
    Returns:    Result set of orders
    
    Usage Example:
        EXEC Sales.usp_GetCustomerOrders 
            @CustomerID = 123,
            @StartDate = '2024-01-01',
            @MaxRows = 50;
    
    History:
        2024-06-20  JS  Created
        2024-06-25  JS  Added date range filtering
    =================================================================
    */
AS
BEGIN
    SET NOCOUNT ON;
    -- ... procedure body
END;
```

**2. Use SET NOCOUNT ON:**

```sql
SET NOCOUNT ON;  -- Reduces network traffic
```

**3. Handle errors properly:**

```sql
CREATE PROCEDURE dbo.usp_SafeUpdate
    @ID INT,
    @Value NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        UPDATE dbo.MyTable
        SET Value = @Value,
            ModifiedDate = GETDATE()
        WHERE ID = @ID;
        
        IF @@ROWCOUNT = 0
        BEGIN
            RAISERROR('Record not found', 16, 1);
            RETURN;
        END
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        
        THROW;  -- Re-throw the error
    END CATCH
END;
```

**4. Use OUTPUT parameters appropriately:**

```sql
CREATE PROCEDURE dbo.usp_InsertOrder
    @CustomerID INT,
    @OrderDate DATETIME,
    @OrderID INT OUTPUT,
    @RowCount INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    INSERT INTO Orders (CustomerID, OrderDate, Status)
    VALUES (@CustomerID, @OrderDate, 'Pending');
    
    SET @OrderID = SCOPE_IDENTITY();
    SET @RowCount = @@ROWCOUNT;
END;
```

**5. Validate parameters:**

```sql
CREATE PROCEDURE dbo.usp_GetOrdersByDate
    @StartDate DATE,
    @EndDate DATE
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Validate parameters
    IF @StartDate IS NULL
    BEGIN
        RAISERROR('@StartDate is required', 16, 1);
        RETURN 1;
    END
    
    IF @EndDate IS NOT NULL AND @EndDate < @StartDate
    BEGIN
        RAISERROR('@EndDate must be >= @StartDate', 16, 1);
        RETURN 1;
    END
    
    -- Proceed with query
END;
```

### Q14: Index maintenance nên được thực hiện như thế nào?

**Câu hỏi**: Tôi nên schedule index maintenance như thế nào và làm sao biết khi nào cần rebuild hay reorganize?

**Trả lời**: Index maintenance là critical cho performance nhưng cần được thực hiện đúng cách:

**Determine fragmentation level:**

```sql
-- Check fragmentation for all indexes
SELECT 
    OBJECT_SCHEMA_NAME(ips.object_id) AS SchemaName,
    OBJECT_NAME(ips.object_id) AS TableName,
    i.name AS IndexName,
    ips.avg_fragmentation_in_percent AS FragmentationPct,
    ips.page_count AS PageCount,
    ips.avg_page_space_used_in_percent AS PageFillPct,
    CASE 
        WHEN ips.avg_fragmentation_in_percent > 40 THEN 'REBUILD'
        WHEN ips.avg_fragmentation_in_percent > 10 THEN 'REORGANIZE'
        ELSE 'NO ACTION'
    END AS RecommendedAction
FROM sys.dm_db_index_physical_stats(
    DB_ID(), NULL, NULL, NULL, 'DETAILED') ips
JOIN sys.indexes i ON ips.object_id = i.object_id AND ips.index_id = i.index_id
WHERE ips.alloc_unit_type_desc = 'IN_ROW_DATA'
    AND ips.page_count > 1000  -- Only large indexes
    AND OBJECTPROPERTY(ips.object_id, 'IsUserTable') = 1
ORDER BY ips.avg_fragmentation_in_percent DESC;
```

**Maintenance Strategy:**

```sql
-- Automated maintenance script
DECLARE @FragmentationThreshold INT = 30;
DECLARE @MinPageCount INT = 1000;

-- Rebuild highly fragmented indexes
EXEC sp_MSforeachtable @command1 = '
    IF OBJECTPROPERTY(''?'', ''TableHasClusteredIndex'') = 1
    BEGIN
        DECLARE @Frag FLOAT;
        SELECT @Frag = ips.avg_fragmentation_in_percent
        FROM sys.dm_db_index_physical_stats(DB_ID(), OBJECT_ID(''?''), NULL, NULL, ''LIMITED'') ips
        WHERE ips.avg_fragmentation_in_percent > 30
        AND ips.page_count > 1000;
        
        IF @Frag > 30
            ALTER INDEX ALL ON ? REBUILD;
        ELSE IF @Frag > 10
            ALTER INDEX ALL ON ? REORGANIZE;
    END';
```

**Considerations:**

| Factor | REBUILD | REORGANIZE |
|--------|---------|------------|
| Fragmentation | >30% | 10-30% |
| Lock behavior | Table lock (blocks users) | Page-level lock |
| Time | Longer | Shorter |
| Resources | More CPU, log space | Less resource intensive |
| Online option | Enterprise only | Always online |

### Q15: Làm thế nào để migrate sang SQL Server version mới?

**Câu hỏi**: Tôi cần migrate từ SQL Server 2012 lên SQL Server 2022. Có best practices nào không?

**Trả lời**: Migration là một quá trình cần được lên kế hoạch cẩn thận:

**Phase 1: Assessment**

```sql
-- Check for deprecated features in use
SELECT 
    OBJECT_NAME(object_id) AS ObjectName,
    type_desc,
    property_desc,
    value AS DeprecatedSetting
FROM sys.dm_db_inconsistent_state;

-- Find queries using deprecated syntax
SELECT 
    OBJECT_NAME(object_id) AS ObjectName,
    definition
FROM sys.sql_modules
WHERE definition LIKE '%SET ROWCOUNT%'  -- Deprecated, use TOP instead
    OR definition LIKE '%RAISERROR%''%''%'''  -- Old RAISERROR syntax
ORDER BY ObjectName;
```

**Phase 2: Test Environment**

1. Restore production database(s) to test environment running new version
2. Run DBCC CHECKDB to verify integrity
3. Run application tests
4. Capture and resolve deprecation warnings

```sql
-- Enable legacy cardinality estimation for testing
ALTER DATABASE SCOPED CONFIGURATION SET LEGACY_CARDINALITY_ESTIMATION = ON;

-- Or use query-level hint
SELECT * FROM Orders 
WHERE CustomerID = 123
OPTION (USE HINT ('FORCE_LEGACY_CARDINALITY_ESTIMATION'));
```

**Phase 3: Migration Execution**

```sql
-- Backup databases on source server
BACKUP DATABASE [YourDatabase] 
TO DISK = '\\Share\YourDatabase_Full.bak' 
WITH COMPRESSION, CHECKSUM;

-- On target server, restore
RESTORE DATABASE [YourDatabase]
FROM DISK = '\\Share\YourDatabase_Full.bak'
WITH MOVE 'YourDatabase_Data' TO 'D:\Data\YourDatabase.mdf',
     MOVE 'YourDatabase_Log' TO 'E:\Logs\YourDatabase_log.ldf',
     RECOVERY;

-- Update compatibility level
ALTER DATABASE YourDatabase SET COMPATIBILITY_LEVEL = 160;  -- SQL Server 2022
```

**Phase 4: Post-Migration**

```sql
-- Monitor for performance regressions using Query Store
SELECT 
    qsq.query_id,
    qsq.query_text_id,
    qrs.count_executions,
    qrs.avg_duration AS new_avg_duration,
    qsq.query_sql_text
FROM sys.query_store_query qsq
JOIN sys.query_store_query_stats qrs ON qsq.query_id = qrs.query_id
WHERE qrs.avg_duration > 1000  -- Queries over 1 second
ORDER BY qrs.avg_duration DESC;

-- Update statistics
EXEC sp_MSforeachtable 'UPDATE STATISTICS ? WITH FULLSCAN';

-- Clear procedure cache after major changes
ALTER DATABASE SCOPED CONFIGURATION CLEAR PROCEDURE_CACHE;
```

## References

- SQL Server Documentation: https://docs.microsoft.com/en-us/sql/sql-server/
- Performance Tuning: https://docs.microsoft.com/en-us/sql/relational-databases/performance/
- Security: https://docs.microsoft.com/en-us/sql/relational-databases/security/
- High Availability: https://docs.microsoft.com/en-us/sql/sql-server/high-availability-solutions-sql-server
