# SQL Server FAQ - Câu Hỏi Thường Gặp

## Giới thiệu

Tài liệu này trả lời các câu hỏi thường gặp về Microsoft SQL Server, được đặt ra bởi developers và administrators trong quá trình làm việc với Cursor Enterprise Framework.

---

## 1. Performance Tuning Questions

### Q1: Làm thế nào để tối ưu hóa câu truy vấn chậm?

**A:** Có nhiều bước để tối ưu hóa câu truy vấn chậm:

```sql
-- Bước 1: Xem execution plan
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

-- Chạy query và xem actual execution plan trong SSMS
SELECT * FROM Orders o
INNER JOIN Customers c ON o.CustomerID = c.CustomerID
WHERE o.OrderDate >= '2024-01-01';

-- Bước 2: Kiểm tra missing indexes từ plan
SELECT 
    d.statement AS TableName,
    d.equality_columns,
    d.inequality_columns,
    d.included_columns,
    s.avg_user_impact,
    s.avg_total_user_cost
FROM sys.dm_db_missing_index_groups g
JOIN sys.dm_db_missing_index_details d ON g.index_handle = d.index_handle
JOIN sys.dm_db_missing_index_group_stats s ON g.index_group_handle = s.group_handle
WHERE d.database_id = DB_ID()
ORDER BY s.avg_total_user_cost DESC;

-- Bước 3: Tạo index được đề xuất
CREATE INDEX IX_Orders_CustomerID_Date_Covering
ON Orders(CustomerID, OrderDate)
INCLUDE (TotalAmount, Status);

-- Bước 4: Kiểm tra statistics
DBCC SHOW_STATISTICS('Orders', 'IX_Orders_CustomerID');

-- Nếu statistics stale, update
UPDATE STATISTICS Orders WITH FULLSCAN;

-- Bước 5: Xem Query Store để so sánh performance
SELECT 
    q.query_id,
    rs.avg_duration,
    rs.count_executions,
    p.plan_id
FROM sys.query_store_query q
JOIN sys.query_store_plan p ON q.query_id = p.query_id
JOIN sys.query_store_runtime_stats rs ON p.plan_id = rs.plan_id
ORDER BY rs.avg_duration DESC;
```

---

### Q2: Sự khác biệt giữa REBUILD và REORGANIZE index là gì?

**A:** REBUILD và REORGANIZE đều là index maintenance operations nhưng có đặc điểm khác nhau:

```sql
-- REORGANIZE: Sắp xếp lại leaf pages in-place
-- - Ít tốn tài nguyên
-- - Không lock table (brief schema lock)
-- - Chỉ hiệu quả khi fragmentation < 30%
ALTER INDEX IX_Orders_CustomerID ON Orders REORGANIZE;

-- REBUILD: Drop và tạo lại index hoàn toàn
-- - Tốn nhiều tài nguyên hơn
-- - Chiếm không gian disk tạm thời
-- - Hiệu quả cho fragmentation > 30%
ALTER INDEX IX_Orders_CustomerID ON Orders REBUILD;

-- Decision logic:
-- Fragmentation < 10%: Không cần làm gì
-- Fragmentation 10-30%: REORGANIZE
-- Fragmentation > 30%: REBUILD

-- Kiểm tra fragmentation:
SELECT 
    OBJECT_NAME(i.object_id) AS TableName,
    i.name AS IndexName,
    ips.avg_fragmentation_in_percent,
    ips.page_count,
    CASE 
        WHEN ips.avg_fragmentation_in_percent < 10 THEN 'No action needed'
        WHEN ips.avg_fragmentation_in_percent < 30 THEN 'REORGANIZE'
        ELSE 'REBUILD'
    END AS RecommendedAction
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'DETAILED') ips
JOIN sys.indexes i ON ips.object_id = i.object_id AND ips.index_id = i.index_id
WHERE ips.page_count > 100;
```

---

### Q3: TempDB nên được cấu hình như thế nào?

**A:** TempDB là system database rất quan trọng cho performance:

```sql
-- 1. Số lượng data files = số CPU cores (tối đa 8)
-- 2. Kích thước equal cho tất cả files
-- 3. Same initial size và growth rate

-- Xem cấu hình hiện tại
SELECT 
    name,
    type_desc,
    size * 8.0 / 1024 AS size_mb,
    max_size,
    growth,
    physical_name
FROM sys.master_files
WHERE database_id = DB_ID('tempdb');

-- Cấu hình mới cho server 8 cores:
ALTER DATABASE tempdb MODIFY FILE (
    NAME = tempdev, 
    SIZE = 1GB, 
    FILEGROWTH = 256MB
);

-- Thêm data files (tổng cộng 8)
ALTER DATABASE tempdb ADD FILE (
    NAME = tempdev2, 
    FILENAME = 'E:\SQLData\tempdev2.ndf',
    SIZE = 1GB, 
    FILEGROWTH = 256MB
);

ALTER DATABASE tempdb ADD FILE (
    NAME = tempdev3, 
    FILENAME = 'E:\SQLData\tempdev3.ndf',
    SIZE = 1GB, 
    FILEGROWTH = 256MB
);

-- ... tiếp tục đến tempdev8

-- Restart SQL Server để áp dụng

-- Monitor tempdb usage:
SELECT 
    SU.session_id,
    S.login_name,
    SU.task_allocated_kb / 1024.0 AS allocated_mb,
    SU.task_deallocated_kb / 1024.0 AS deallocated_mb,
    SUBSTRING(T.text, 1, 100) AS query_text
FROM sys.dm_db_session_space_usage SU
JOIN sys.dm_exec_sessions S ON SU.session_id = S.session_id
CROSS APPLY sys.dm_exec_sql_text(S.sql_handle) T
WHERE SU.user_objects_alloc_page_count > 0
    OR SU.internal_objects_alloc_page_count > 0
ORDER BY SU.user_objects_alloc_page_count DESC;
```

---

## 2. Concurrency và Locking Questions

### Q4: Làm thế nào để tránh deadlock?

**A:** Deadlock xảy ra khi hai transactions chờ nhau giải phóng locks:

```sql
-- Chiến lược 1: Access tables theo cùng thứ tự
-- Bad: Session 1 locks A then B, Session 2 locks B then A
BEGIN TRANSACTION;
    UPDATE Products SET Price = 100 WHERE ProductID = 1;  -- A
    UPDATE Products SET Price = 200 WHERE ProductID = 2;  -- B (Deadlock với Session 2!)
COMMIT;

-- Good: Luôn lock theo cùng thứ tự
BEGIN TRANSACTION;
    UPDATE Products SET Price = 100 WHERE ProductID = 1;  -- Lock A trước
    UPDATE Products SET Price = 200 WHERE ProductID = 2;  -- Lock B sau
COMMIT;

-- Chiến lược 2: Giữ transactions ngắn
BEGIN TRANSACTION;
    -- Chỉ database operations trong transaction
    UPDATE Orders SET Status = 'Shipped' WHERE OrderID = @OrderID;
COMMIT;
-- External calls (email, API) bên ngoài transaction

-- Chiến lược 3: Sử dụng appropriate isolation level
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Chiến lược 4: Sử dụng NOLOCK hint cho reads không critical
SELECT * FROM Products WITH (NOLOCK)
WHERE CategoryID = 1;

-- Chiến lược 5: Retry logic trong application
```csharp
public void ExecuteWithRetry(int maxRetries = 3)
{
    for (int i = 0; i < maxRetries; i++)
    {
        try
        {
            using (var conn = new SqlConnection(connectionString))
            {
                conn.Open();
                // Execute command
            }
            break; // Success
        }
        catch (SqlException ex) when (ex.Number == 1205) // Deadlock
        {
            if (i == maxRetries - 1) throw;
            Thread.Sleep(100 * (i + 1)); // Exponential backoff
        }
    }
}
```

---

### Q5: Sự khác biệt giữa các Isolation Levels là gì?

**A:** SQL Server cung cấp nhiều isolation levels để kiểm soát concurrency:

```sql
-- 1. READ UNCOMMITTED (Dirty Read)
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
-- - Đọc uncommitted changes
-- - Không lock gì cả
-- - Có thể đọc dirty data
-- - Ví dụ:
SELECT * FROM Orders WHERE CustomerID = 1; -- Có thể đọc data chưa commit

-- 2. READ COMMITTED (Default)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- - Chỉ đọc committed data
-- - Giữ shared lock khi đọc
-- - Shared lock được release sau khi read xong
-- - Có thể đọc inconsistent data nếu transaction khác update giữa chừng

-- 3. READ COMMITTED SNAPSHOT (RCSI)
ALTER DATABASE MyDB SET READ_COMMITTED_SNAPSHOT ON;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- - Sử dụng row versioning
-- - Không blocking writers
-- - Đọc last committed version

-- 4. REPEATABLE READ
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- - Giữ shared locks cho đến khi transaction kết thúc
-- - Ngăn other transactions update/delete rows đã đọc
-- - Có thể có phantom reads

-- 5. SNAPSHOT
ALTER DATABASE MyDB SET ALLOW_SNAPSHOT_ISOLATION ON;
SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
-- - Mỗi transaction đọc version tại thời điểm bắt đầu
-- - Update conflicts có thể xảy ra (throw error)
-- - Không blocking

-- 6. SERIALIZABLE
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- - Lock toàn bộ range (như WHERE clause)
-- - Ngăn phantom reads hoàn toàn
-- - Có thể gây deadlock và performance issues

-- Performance impact: READ UNCOMMITTED > RCSI > READ COMMITTED > REPEATABLE READ > SNAPSHOT > SERIALIZABLE
-- Blocking: SERIALIZABLE > REPEATABLE READ > READ COMMITTED > RCSI > READ UNCOMMITTED
```

---

## 3. Backup và Recovery Questions

### Q6: Nên chọn Recovery Model nào?

**A:** Chọn recovery model dựa trên business requirements:

```sql
-- Xem recovery model hiện tại
SELECT 
    name,
    recovery_model_desc,
    log_reuse_wait_desc
FROM sys.databases;

-- FULL Recovery Model
ALTER DATABASE MyDB SET RECOVERY FULL;
-- - Full logging (tất cả operations được log)
-- - Hỗ trợ point-in-time recovery
-- - Cần regular log backups
-- - Dùng cho: Production databases, critical data

-- BULK_LOGGED Recovery Model
ALTER DATABASE MyDB SET RECOVERY BULK_LOGGED;
-- - Minimal logging cho bulk operations (SELECT INTO, BULK INSERT, etc.)
-- - Giảm log space cho bulk imports
-- - Vẫn hỗ trợ point-in-time (ngoại trừ bulk operations)
-- - Dùng cho: Databases với periodic bulk loads

-- SIMPLE Recovery Model
ALTER DATABASE MyDB SET RECOVERY SIMPLE;
-- - Minimal logging
-- - Log space được reuse sau checkpoint
-- - Chỉ recover được đến last full/differential backup
-- - Dùng cho: Development databases, read-only databases, small databases

-- Best practice: FULL + Log backups
BACKUP DATABASE MyDB TO DISK = 'C:\Backups\MyDB_Full.bak';
BACKUP LOG MyDB TO DISK = 'C:\Backups\MyDB_Log.trn';

-- Point-in-time recovery
RESTORE DATABASE MyDB 
FROM DISK = 'C:\Backups\MyDB_Full.bak'
WITH NORECOVERY;

RESTORE DATABASE MyDB 
FROM DISK = 'C:\Backups\MyDB_Diff.bak'
WITH NORECOVERY;

RESTORE LOG MyDB 
FROM DISK = 'C:\Backups\MyDB_Log.trn'
WITH NORECOVERY,
     STOPAT = '2024-01-15 14:30:00';
```

---

### Q7: Làm thế nào để restore database đến point-in-time?

**A:** Point-in-time recovery yêu cầu FULL hoặc BULK_LOGGED recovery model:

```sql
-- Giả sử:
-- - Full backup: 2024-01-01 00:00
-- - Diff backup: 2024-01-15 00:00
-- - Log backups: Every 15 minutes

-- Muốn restore đến: 2024-01-15 14:30:00

-- Bước 1: Restore full backup
RESTORE DATABASE MyDB
FROM DISK = 'C:\Backups\MyDB_Full_20240101.bak'
WITH NORECOVERY,
      MOVE 'MyDB_Data' TO 'E:\Data\MyDB.mdf',
      MOVE 'MyDB_Log' TO 'F:\Logs\MyDB.ldf';

-- Bước 2: Restore differential backup (nếu có)
RESTORE DATABASE MyDB
FROM DISK = 'C:\Backups\MyDB_Diff_20240115.bak'
WITH NORECOVERY;

-- Bước 3: Restore log backups đến target time
RESTORE LOG MyDB
FROM DISK = 'C:\Backups\MyDB_Log_20240115_1400.trn'
WITH NORECOVERY;

RESTORE LOG MyDB
FROM DISK = 'C:\Backups\MyDB_Log_20240115_1415.trn'
WITH NORECOVERY;

RESTORE LOG MyDB
FROM DISK = 'C:\Backups\MyDB_Log_20240115_1430.trn'
WITH STOPAT = '2024-01-15 14:30:00',
      RECOVERY;

-- Verify
SELECT 
    name,
    state_desc,
    user_access_desc,
    recovery_model_desc
FROM sys.databases WHERE name = 'MyDB';
```

---

## 4. Index Questions

### Q8: Khi nào nên sử dụng Clustered vs Non-Clustered index?

**A:** Chọn loại index dựa trên usage pattern:

```sql
-- CLUSTERED INDEX
-- - Sắp xếp dữ liệu vật lý theo key
-- - Chỉ một clustered index per table
-- - Leaf level = actual data
-- - Tốt khi:
--   * Truy vấn range (BETWEEN, >, <)
--   * ORDER BY theo column đó
--   * Cột có tính uniqueness
--   * PRIMARY KEY columns

CREATE TABLE Orders (
    OrderID INT IDENTITY(1,1) PRIMARY KEY, -- Clustered by default
    OrderDate DATETIME NOT NULL,
    CustomerID INT NOT NULL
);

-- Tạo clustered index cho range queries
CREATE CLUSTERED INDEX IX_Orders_Date ON Orders(OrderDate);

-- NON-CLUSTERED INDEX
-- - Separate structure từ data
-- - Nhiều non-clustered indexes per table
-- - Leaf level chứa index key + bookmark
-- - Tốt khi:
--   * Covering index cho specific queries
--   * Columns thường được filter
--   * JOIN columns
--   * Columns trong ORDER BY

CREATE NONCLUSTERED INDEX IX_Orders_CustomerID
ON Orders(CustomerID)
INCLUDE (OrderDate, TotalAmount);

-- Query được cover hoàn toàn bởi index:
SELECT OrderID, OrderDate, TotalAmount
FROM Orders
WHERE CustomerID = 100;
-- Sử dụng IX_Orders_CustomerID mà không cần lookup

-- COMPOSITE INDEX Column Order
-- Quy tắc: Equality columns -> Range columns -> Sort columns

-- Tốt: Equality trước
CREATE INDEX IX_Orders_Customer_Status_Date 
ON Orders(CustomerID, Status, OrderDate);

-- Query này sẽ sử dụng index hiệu quả:
SELECT * FROM Orders
WHERE CustomerID = 100       -- Equality: sử dụng first column
  AND Status = 'Shipped'    -- Equality: sử dụng second column
  AND OrderDate >= '2024-01-01';  -- Range: sử dụng third column
```

---

### Q9: Filtered Index vs Regular Index - Khi nào nên dùng?

**A:** Filtered index tốt cho queries trên subset của data:

```sql
-- REGULAR INDEX: Index tất cả rows
CREATE INDEX IX_Orders_Status ON Orders(Status);
-- Kích thước: Lớn, index tất cả orders (có thể millions)

-- FILTERED INDEX: Chỉ index rows thỏa điều kiện
CREATE INDEX IX_Orders_Pending ON Orders(OrderDate)
WHERE Status = 'Pending';
-- Kích thước: Nhỏ hơn, chỉ index pending orders

-- FILTERED INDEX tốt khi:
-- 1. Query thường filter trên specific value
SELECT * FROM Orders WHERE Status = 'Pending';

-- 2. NULL values chiếm majority
CREATE INDEX IX_Customers_Phone 
ON Customers(PhoneNumber)
WHERE PhoneNumber IS NOT NULL;

-- 3. Computed conditions
CREATE INDEX IX_Products_ActiveCategory 
ON Products(CategoryID)
WHERE IsActive = 1 AND IsDeleted = 0;

-- 4. Rare values
CREATE INDEX IX_Orders_Exception 
ON Orders(ExceptionCode)
WHERE ExceptionCode IS NOT NULL;

-- Khi nào KHÔNG nên dùng:
-- - Filter condition không stable (thay đổi frequently)
-- - Subset quá lớn (hơn 50% total rows)
-- - Queries không sử dụng filter trong WHERE clause

-- Kiểm tra filtered index usage:
SELECT 
    OBJECT_NAME(i.object_id) AS TableName,
    i.name AS IndexName,
    i.filter_definition,
    us.user_seeks,
    us.user_scans
FROM sys.indexes i
JOIN sys.dm_db_index_usage_stats us 
    ON i.object_id = us.object_id AND i.index_id = us.index_id
WHERE i.has_filter = 1;
```

---

## 5. Security Questions

### Q10: Làm thế nào để implement column-level security?

**A:** SQL Server cung cấp multiple approaches cho column-level security:

```sql
-- Phương pháp 1: GRANT/REVOKE permissions
-- Tạo role cho users được phép xem sensitive data
CREATE ROLE HRManager;

GRANT SELECT ON Employees TO HRManager;
-- Không grant on Salary column - HRManager không thể SELECT Salary

-- Normal users chỉ có thể SELECT columns được grant
-- SELECT Salary sẽ fail cho non-HR users

-- Phương pháp 2: View với security
CREATE VIEW vw_Employees_Public AS
SELECT 
    EmployeeID,
    FirstName,
    LastName,
    Department,
    HireDate,
    -- Salary bị exclude
    NULL AS SalaryMasked
FROM Employees;

GRANT SELECT ON vw_Employees_Public TO Public;

-- Phương pháp 3: Dynamic Data Masking (SQL Server 2016+)
CREATE TABLE SensitiveData (
    ID INT IDENTITY PRIMARY KEY,
    Name NVARCHAR(100),
    SSN VARCHAR(11) MASKED WITH (FUNCTION = 'partial(0,"XXX-XX-",4)'),
    Email VARCHAR(100) MASKED WITH (FUNCTION = 'email()'),
    Phone VARCHAR(20) MASKED WITH (FUNCTION = 'default()'),
    Salary DECIMAL(10,2) MASKED WITH (FUNCTION = 'random(10000,50000)')
);

-- Grant unmasked access
GRANT UNMASK TO HRManager;

-- Phương pháp 4: Column-level ENCRYPTION
CREATE TABLE EncryptedData (
    ID INT PRIMARY KEY,
    SSN CHAR(11) COLLATE Latin1_General_BIN2 
        ENCRYPTED WITH (
            ENCRYPTION_TYPE = DETERMINISTIC,
            ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256',
            COLUMN_ENCRYPTION_KEY = MyCEK
        ) NOT NULL
);

-- Phương pháp 5: Application role (với connection string đặc biệt)
-- Trong application, kích hoạt application role
EXEC sp_setapprole 'SensitiveDataRole', 'RolePassword';

-- Bây giờ application có quyền xem sensitive columns
-- Users trực tiếp kết nối không có quyền
```

---

### Q11: Sự khác biệt giữa TDE và Always Encrypted là gì?

**A:** Hai cơ chế mã hóa phục vụ mục đích khác nhau:

```sql
-- TDE (Transparent Data Encryption)
-- - Mã hóa toàn bộ database files (data + log)
-- - Database Engine decrypts automatically khi đọc
-- - Transparent với applications
-- - Bảo vệ against physical theft (stolen backups, drives)
-- - Không bảo vệ against SQL Server access

-- Enable TDE:
USE master;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'StrongPassword123!';
CREATE CERTIFICATE MyCert WITH SUBJECT = 'TDE Certificate';
BACKUP CERTIFICATE MyCert TO FILE = 'C:\Backups\MyCert.cer'
PRIVATE KEY (FILE = 'C:\Backups\MyCert.key', 
             ENCRYPTION BY PASSWORD = 'KeyPassword!');

USE MyDB;
CREATE DATABASE ENCRYPTION KEY
BY ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE MyCert;
ALTER DATABASE MyDB SET ENCRYPTION ON;

-- Always Encrypted
-- - Mã hóa sensitive columns trong application layer
-- - SQL Server chỉ thấy encrypted values
-- - Encryption key được lưu trong external store (Azure Key Vault, Windows Certificate Store)
-- - Bảo vệ against SQL Server DBA access
-- - Applications cần driver hỗ trợ AE

-- Create table với Always Encrypted:
CREATE TABLE SensitiveData (
    ID INT IDENTITY PRIMARY KEY,
    SSN CHAR(11) COLLATE Latin1_General_BIN2 
        ENCRYPTED WITH (
            ENGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256',
            COLUMN_ENCRYPTION_KEY = MyCEK
        ) NOT NULL,
    Salary DECIMAL(10,2) 
        ENCRYPTED WITH (
            ENCRYPTION_TYPE = DETERMINISTIC,
            ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256',
            COLUMN_ENCRYPTION_KEY = MyCEK
        ) NOT NULL
);

-- Connection string phải có Column Encryption Setting:
-- "Server=MyServer;Database=MyDB;Column Encryption Setting=Enabled;"

-- So sánh:
-- TDE: Bảo vệ physical media, DBA vẫn thấy data
-- Always Encrypted: Bảo vệ data khỏi DBA và SQL Server engine

-- Best practice: Sử dụng cả hai
ALTER DATABASE MyDB SET ENCRYPTION ON;  -- TDE
-- Plus Always Encrypted columns cho sensitive data
```

---

## 6. Query Optimization Questions

### Q12: Làm thế nào để phân tích execution plan?

**A:** Execution plan cho biết cách SQL Server thực thi query:

```sql
-- Bật actual execution plan (SSMS: Ctrl+M)
-- Hoặc dùng query:

SET STATISTICS IO ON;
SET STATISTICS TIME ON;

-- Chạy query để get actual plan
SELECT * FROM Orders o
INNER JOIN Customers c ON o.CustomerID = c.CustomerID
WHERE o.OrderDate >= '2024-01-01';

-- Xem plan từ cache:
SELECT 
    q.query_text,
    p.query_plan,
    qs.execution_count,
    qs.total_elapsed_time / 1000.0 AS total_ms,
    qs.total_logical_reads,
    qs.total_cpu_time / 1000.0 AS cpu_ms
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) q
CROSS APPLY sys.dm_exec_query_plan(qs.plan_handle) p
WHERE q.text LIKE '%Orders%'
ORDER BY qs.total_elapsed_time DESC;

-- Các operators cần chú ý:
-- Good:
-- - Index Seek: Hiệu quả, seeks trực tiếp
-- - Nested Loop (small outer): Tốt cho small joins
-- - Hash Match (large tables): Hiệu quả cho large data

-- Bad:
-- - Table Scan: Đọc toàn bộ bảng
-- - Clustered Index Scan: Đọc toàn bộ clustered index
-- - Sort (no index): Phải sort trong memory
-- - Hash Match Warning: Hash spill to tempdb

-- Estimated vs Actual plan:
-- - Estimated: Dựa trên statistics
-- - Actual: Sau khi thực thi
-- So sánh để tìm row estimate errors

-- Cost comparison:
-- - Relative cost trong plan (tổng = 100%)
-- - Query cost = Batch cost của tất cả statements
-- - Index cost vs Scan cost
```

---

### Q13: Parameter Sniffing là gì và cách xử lý?

**A:** Parameter sniffing là hiện tượng khi SQL Server reuse plan compiled với giá trị parameter đầu tiên:

```sql
-- Stored procedure bị parameter sniffing:
CREATE PROCEDURE usp_GetOrdersByStatus
    @Status NVARCHAR(50)
AS
BEGIN
    SELECT * FROM Orders WHERE Status = @Status;
END;

-- Lần 1: Gọi với @Status = 'Pending' (100 rows)
EXEC usp_GetOrdersByStatus @Status = 'Pending';
-- Plan compiled: Table Scan + Filter (tốt cho 100 rows)

-- Lần 2: Gọi với @Status = 'All' (1,000,000 rows)
EXEC usp_GetOrdersByStatus @Status = 'All';
-- Plan vẫn dùng Table Scan + Filter (không tối ưu cho 1M rows!)

-- Solution 1: OPTION (RECOMPILE)
CREATE PROCEDURE usp_GetOrdersByStatus_Recompile
    @Status NVARCHAR(50)
AS
BEGIN
    SELECT * FROM Orders WHERE Status = @Status
    OPTION (RECOMPILE);  -- Compile mới mỗi lần
END;

-- Solution 2: OPTIMIZE FOR UNKNOWN
CREATE PROCEDURE usp_GetOrdersByStatus_Optimize
    @Status NVARCHAR(50)
AS
BEGIN
    SELECT * FROM Orders WHERE Status = @Status
    OPTION (OPTIMIZE FOR UNKNOWN);  -- Sử dụng average statistics
END;

-- Solution 3: Local variable
CREATE PROCEDURE usp_GetOrdersByStatus_LocalVar
    @Status NVARCHAR(50)
AS
BEGIN
    DECLARE @LocalStatus NVARCHAR(50) = @Status;
    SELECT * FROM Orders WHERE Status = @LocalStatus;
    -- Parameter sniffing không xảy ra với local variable
END;

-- Solution 4: Sử dụng plan guide
EXEC sp_create_plan_guide 
    @name = 'Guide_OrdersByStatus',
    @stmt = 'SELECT * FROM Orders WHERE Status = @Status',
    @type = 'SQL_STMT',
    @params = '@Status NVARCHAR(50)',
    @hints = 'OPTION (OPTIMIZE FOR (@Status = ''Active''))';

-- Monitor parameter sniffing:
SELECT 
    qs.execution_count,
    qs.total_elapsed_time / 1000.0 AS total_ms,
    qs.min_elapsed_time / 1000.0 AS min_ms,
    qs.max_elapsed_time / 1000.0 AS max_ms,
    SUBSTRING(qt.text, 1, 200) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
WHERE qt.text LIKE '%usp_GetOrders%'
ORDER BY qs.execution_count DESC;
-- Nếu max_ms >> min_ms, có thể có parameter sniffing
```

---

## 7. High Availability Questions

### Q14: Always On Availability Groups vs Database Mirroring - Chọn cái nào?

**A:** So sánh chi tiết để đưa ra quyết định:

```sql
-- ALWAYS ON AVAILABILITY GROUPS (AG)
-- SQL Server 2012+
-- - Enterprise edition trở lên
-- - Multiple databases trong một group
-- - Multiple secondaries (up to 8)
-- - Automatic failback
-- - Read-only routing
-- - Backup on secondary
-- - Requires Windows Server Failover Cluster (WSFC)
-- - Combined with failover clustering

-- Setup:
CREATE AVAILABILITY GROUP MyAG
FOR DATABASE MyDB
WITH (
    AUTOMATED_BACKUP_PREFERENCE = SECONDARY,
    FAILURE_CONDITION_LEVEL = 3,
    HEALTH_CHECK_TIMEOUT = 30000
)
REPLICA ON 
    'PrimaryServer' WITH (
        ENDPOINT_URL = 'TCP://PrimaryServer:5022',
        AVAILABILITY_MODE = SYNCHRONOUS_COMMIT,
        FAILOVER_MODE = AUTOMATIC,
        BACKUP_PRIORITY = 50,
        SECONDARY_ROLE (ALLOW_CONNECTIONS = READ_ONLY)
    ),
    'SecondaryServer1' WITH (
        ENDPOINT_URL = 'TCP://SecondaryServer1:5022',
        AVAILABILITY_MODE = SYNCHRONOUS_COMMIT,
        FAILOVER_MODE = AUTOMATIC,
        BACKUP_PRIORITY = 30,
        SECONDARY_ROLE (ALLOW_CONNECTIONS = READ_ONLY)
    );

-- DATABASE MIRRORING (Deprecated in SQL 2012+)
-- - Single database
-- - One mirror only
-- - Automatic failover requires witness
-- - No read-only access on mirror
-- - No backup on mirror
-- - Does not require WSFC

-- Migration từ Mirroring sang AG:
-- 1. Remove mirroring
ALTER DATABASE MyDB SET PARTNER OFF;

-- 2. Add to AG
ALTER AVAILABILITY GROUP MyAG ADD DATABASE MyDB;

-- RECOMMENDATION:
-- - Use Always On AG for new implementations
-- - Database Mirroring only for legacy systems
-- - AG provides more features và flexibility
```

---

### Q15: Làm thế nào để implement read-scaleout với secondary replicas?

**A:** AG cho phép scale-out reads sang secondary replicas:

```sql
-- Bật read-only routing
ALTER AVAILABILITY GROUP MyAG
MODIFY REPLICA ON 'SecondaryServer1'
WITH (SECONDARY_ROLE (ALLOW_CONNECTIONS = READ_ONLY));

ALTER AVAILABILITY GROUP MyAG
MODIFY REPLICA ON 'SecondaryServer2'
WITH (SECONDARY_ROLE (ALLOW_CONNECTIONS = READ_ONLY));

-- Cấu hình read-only routing list
ALTER AVAILABILITY GROUP MyAG
MODIFY REPLICA ON 'PrimaryServer'
WITH (PRIMARY_ROLE (
    READ_ONLY_ROUTING_LIST = ('SecondaryServer1', 'SecondaryServer2')
));

-- Cấu hình routing URL cho mỗi replica
ALTER AVAILABILITY GROUP MyAG
MODIFY REPLICA ON 'SecondaryServer1'
WITH (PRIMARY_ROLE (READ_ONLY_ROUTING_URL = 'TCP://SecondaryServer1:1433'));

ALTER AVAILABILITY AG MyAG
MODIFY REPLICA ON 'SecondaryServer2'
WITH (PRIMARY_ROLE (READ_ONLY_ROUTING_URL = 'TCP://SecondaryServer2:1433'));

-- Connection string cho read-only workloads:
"Server=MyAGListener;Database=MyDB;ApplicationIntent=ReadOnly;"

-- Application code:
```csharp
// Read-only connection
var readOnlyConnString = 
    "Server=MyAGListener;Database=MyDB;ApplicationIntent=ReadOnly;";
    
// Read-write connection  
var readWriteConnString = 
    "Server=MyAGListener;Database=MyDB;ApplicationIntent=ReadWrite;";

// Using with connection pooling
public async Task<List<Product>> GetProductsAsync()
{
    // Automatically routes to secondary
    using (var conn = new SqlConnection(readOnlyConnString))
    {
        await conn.OpenAsync();
        return await conn.QueryAsync<Product>("SELECT * FROM Products");
    }
}
```

-- Monitor routing:
SELECT 
    ar.replica_server_name,
    rcs.is_local,
    rcs.role_desc,
    rcs.connected_state_desc,
    rrs.is_routeable,
    rrs.router_direction
FROM sys.dm_hadr_availability_replica_states rcs
JOIN sys.availability_replicas ar ON rcs.replica_id = ar.replica_id
LEFT JOIN sys.dm_hadr_availability_replica_route_scores rrs 
    ON ar.replica_id = rrs.replica_id;
```

---

## 8. Troubleshooting Questions

### Q16: Làm thế nào để xử lý blocking issues?

**A:** Blocking xảy ra khi một session giữ locks mà session khác cần:

```sql
-- Bước 1: Xác định blocking
SELECT 
    blocked.session_id AS blocked_session,
    blocker.session_id AS blocking_session,
    blocker.status AS blocker_status,
    blocker.login_name AS blocker_login,
    blocker.open_transaction_count AS blocker_open_trans,
    blocked.wait_time / 1000.0 AS wait_seconds,
    blocked.wait_type AS wait_type,
    blocked.last_wait_type,
    blocked_txt.text AS blocked_sql,
    blocker_txt.text AS blocker_sql,
    blocker_plan.query_plan AS blocker_plan
FROM sys.dm_exec_requests blocked
JOIN sys.dm_exec_requests blocker ON blocked.blocking_session_id = blocker.session_id
CROSS APPLY sys.dm_exec_sql_text(blocked.sql_handle) blocked_txt
CROSS APPLY sys.dm_exec_sql_text(blocker.sql_handle) blocker_txt
OUTER APPLY sys.dm_exec_query_plan(blocker.plan_handle) blocker_plan
WHERE blocked.session_id > 50;

-- Bước 2: Xem locks đang giữ
SELECT 
    t.request_session_id AS session_id,
    t.request_owner_type,
    t.request_mode AS lock_mode,
    t.request_status AS lock_status,
    OBJECT_NAME(t.resource_associated_entity_id) AS table_name,
    CASE t.resource_type
        WHEN 'OBJECT' THEN OBJECT_NAME(t.resource_associated_entity_id)
        WHEN 'PAGE' THEN OBJECT_NAME(part.object_id) + ': Page ' + CAST(t.resource_associated_entity_id AS VARCHAR(10))
        WHEN 'RID' THEN OBJECT_NAME(part.object_id) + ': Row ' + CAST(t.resource_associated_entity_id AS VARCHAR(10))
        WHEN 'KEY' THEN OBJECT_NAME(part.object_id) + ': Key'
        ELSE t.resource_description
    END AS resource_detail,
    s.login_name,
    s.host_name,
    s.program_name,
    s.status AS session_status,
    s.cpu_time,
    s.memory_usage,
    s.total_elapsed_time / 1000.0 AS elapsed_seconds,
    s.reads, s.writes,
    s.open_transaction_count
FROM sys.dm_tran_locks t
JOIN sys.dm_exec_sessions s ON t.request_session_id = s.session_id
LEFT JOIN sys.partitions part ON t.resource_associated_entity_id = part.hobt_id
WHERE t.request_session_id > 50
    AND t.resource_database_id = DB_ID()
ORDER BY s.open_transaction_count DESC;

-- Bước 3: Kill blocking session (nếu cần)
-- 13 = blocked session
KILL 13;  -- Chỉ kill nếu chắc chắn an toàn

-- Hoặc kill với rollback
KILL 13 WITH STATUSONLY;  -- Xem progress

-- Bước 4: Long-term solutions
-- - Tối ưu queries để giảm thời gian giữ lock
-- - Giảm transaction length
-- - Sử dụng optimistic locking
-- - Điều chỉnh isolation level
-- - Cấu hình lock escalation
ALTER TABLE Orders SET (LOCK_ESCALATION = AUTO);
```

---

### Q17: Wait Statistics cho biết điều gì về performance?

**A:** Wait statistics tổng hợp thời gian threads phải chờ resources:

```sql
-- Xem top waits
SELECT TOP 20
    wait_type,
    waiting_tasks_count,
    wait_time_ms / 1000.0 AS total_wait_sec,
    signal_wait_time_ms / 1000.0 AS signal_wait_sec,
    (wait_time_ms - signal_wait_time_ms) / 1000.0 AS resource_wait_sec,
    CASE 
        WHEN wait_type LIKE 'CXPACKET%' THEN 'Parallelism'
        WHEN wait_type LIKE 'PAGEIOLATCH%' THEN 'IO'
        WHEN wait_type LIKE 'PAGELATCH%' THEN 'Latching'
        WHEN wait_type LIKE 'LCK_M%' THEN 'Locking'
        WHEN wait_type LIKE 'SOS%' THEN 'Memory'
        WHEN wait_type LIKE 'ASYNC%' THEN 'Network'
        WHEN wait_type LIKE 'BACKUP%' THEN 'Backup'
        WHEN wait_type LIKE 'HADR%' THEN 'Always On'
        ELSE 'Other'
    END AS category
FROM sys.dm_os_wait_stats
WHERE wait_time_ms > 1000
    AND wait_type NOT IN (
        'XE_TIMER_EVENT', 'XE_DISPATCHER_SESSION', 
        'REQUEST_FOR_DEADLOCK_SEARCH', 'SLEEP_TASK',
        'SQLTRACE_INCREMENTAL_FLUSH_SLEEP'
    )
ORDER BY wait_time_ms DESC;

-- Giải thích các waits phổ biến:

-- CXPACKET: Threads waiting for parallel query partner
-- Solution: Adjust MAXDOP hoặc tune queries
EXEC sp_configure 'max degree of parallelism', 4;

-- PAGEIOLATCH_*: Waiting for disk IO
-- Solution: Add indexes, optimize queries, add memory

-- PAGELATCH_*: Latches in memory (không phải disk IO)
-- PAGELATCH_UP: Allocation page contention
-- Solution: Increase file count, use TF 1118

-- LCK_M_IX, LCK_M_X: Lock waits
-- Solution: Reduce transaction length, optimize queries

-- ASYNC_NETWORK_IO: Waiting for client to consume data
-- Solution: Fix client application, use more selective queries

-- HADR_SYNC_COMMIT: Waiting for AG sync
-- Solution: Optimize transaction, use async if acceptable

-- SOS_SCHEDULER_YIELD: CPU contention
-- Solution: More CPU, optimize queries

-- OLEDB: Waiting for linked server
-- Solution: Optimize remote queries, increase timeout
```

---

## 9. Best Practices Questions

### Q18: Nên sử dụng GUID hay INT cho Primary Key?

**A:** Mỗi loại có ưu và nhược điểm:

```sql
-- INT Identity (Recommend cho hầu hết cases)
CREATE TABLE Orders (
    OrderID INT IDENTITY(1,1) PRIMARY KEY CLUSTERED,
    -- ...
);
-- Pros:
-- - Nhỏ (4 bytes)
-- - Sequential, no page splits
-- - Index efficient
-- - Predictable
-- - Auto-increment
-- Cons:
-- - Giới hạn ~2 billion rows
-- - Không merge-able across systems

-- BIGINT Identity (cho very large tables)
CREATE TABLE Transactions (
    TransactionID BIGINT IDENTITY(1,1) PRIMARY KEY CLUSTERED,
    -- ...
);
-- Nếu cần hơn 2 billion rows

-- GUID (chỉ khi cần)
CREATE TABLE DistributedOrders (
    OrderID UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY,
    -- ...
);
-- Pros:
-- - Unique across systems
-- - Merge data từ multiple sources
-- - Không guessable IDs
-- Cons:
-- - Lớn (16 bytes)
-- - Random, gây page splits
-- - Index fragmentation
-- - Không sequential

-- GUID với NEWSEQUENTIALID (tốt hơn nhưng không hoàn hảo)
CREATE TABLE BetterGUIDOrders (
    OrderID UNIQUEIDENTIFIER DEFAULT NEWSEQUENTIALID() PRIMARY KEY,
    -- ...
);
-- Tạo sequential GUIDs (trong một số trường hợp)
-- Vẫn có thể có fragmentation

-- RECOMMENDATION:
-- 1. Sử dụng INT/BIGINT Identity cho hầu hết cases
-- 2. Sử dụng GUID khi:
--    - Data được merge từ multiple sources
--    - Need to generate IDs before insert
--    - IDs exposed to public (harder to guess)
-- 3. Nếu dùng GUID, đặt làm NONCLUSTERED index
CREATE TABLE Orders (
    OrderID INT IDENTITY(1,1) PRIMARY KEY NONCLUSTERED,
    OrderSeq UNIQUEIDENTIFIER DEFAULT NEWID(),
    ...
);
CREATE CLUSTERED INDEX IX_Orders_Date ON Orders(OrderDate);
```

---

### Q19: Làm thế nào để implement soft delete?

**A:** Soft delete lưu trữ trạng thái deleted trong column thay vì xóa row:

```sql
-- Phương pháp 1: IsDeleted flag
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName NVARCHAR(100),
    Price DECIMAL(10,2),
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy NVARCHAR(100) NULL
);

-- Tạo filtered index cho active records
CREATE INDEX IX_Products_Active 
ON Products(ProductName)
WHERE IsDeleted = 0;

-- View cho active records
CREATE VIEW vw_ActiveProducts AS
SELECT ProductID, ProductName, Price
FROM Products
WHERE IsDeleted = 0;

-- Delete operation trở thành update
CREATE PROCEDURE usp_DeleteProduct
    @ProductID INT,
    @DeletedBy NVARCHAR(100)
AS
BEGIN
    UPDATE Products
    SET IsDeleted = 1,
        DeletedDate = GETDATE(),
        DeletedBy = @DeletedBy
    WHERE ProductID = @ProductID;
END;

-- Query luôn filter IsDeleted = 0
CREATE FUNCTION fn_ActiveProducts()
RETURNS TABLE
AS
RETURN (
    SELECT ProductID, ProductName, Price
    FROM Products
    WHERE IsDeleted = 0
);

-- Phương pháp 2: IsActive (ngược lại)
CREATE TABLE StatusProducts (
    ProductID INT PRIMARY KEY,
    ProductName NVARCHAR(100),
    IsActive BIT NOT NULL DEFAULT 1
);

CREATE INDEX IX_Products_IsActive 
ON StatusProducts(IsActive)
WHERE IsActive = 1;

-- Phương pháp 3: Row Version (timestamp)
CREATE TABLE VersionProducts (
    ProductID INT PRIMARY KEY,
    ProductName NVARCHAR(100),
    ValidFrom DATETIME2 GENERATED ALWAYS AS ROW START HIDDEN,
    ValidTo DATETIME2 GENERATED ALWAYS AS ROW END HIDDEN,
    PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo)
);

-- Enable temporal table
ALTER TABLE VersionProducts
SET (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.ProductHistory));
```

---

### Q20: Transaction Isolation nào nên sử dụng trong ứng dụng?

**A:** Chọn isolation level dựa trên requirements của business:

```sql
-- DEFAULT (READ COMMITTED)
-- Phù hợp cho: Most OLTP applications
-- Balance giữa consistency và performance

SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- READ COMMITTED SNAPSHOT (RCSI)
-- Phù hợp cho: Applications cần consistent reads without blocking
-- Cần enable database:
ALTER DATABASE MyDB SET READ_COMMITTED_SNAPSHOT ON;

-- REPEATABLE READ
-- Phù hợp cho: Financial transactions cần consistent reads
-- Đảm bảo rows không thay đổi trong transaction

SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN TRANSACTION;
    SELECT @Balance = Balance FROM Accounts WHERE AccountID = @ID;
    -- @Balance guaranteed not changed until COMMIT
    UPDATE Accounts SET Balance = @Balance - @Amount WHERE AccountID = @ID;
COMMIT;

-- SNAPSHOT
-- Phù hợp cho: Long-running reports cần point-in-time consistency
-- Không blocking writers
ALTER DATABASE MyDB SET ALLOW_SNAPSHOT_ISOLATION ON;

SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
BEGIN TRANSACTION;
    SELECT * FROM Orders WHERE OrderDate = '2024-01-01';
    -- Đọc version tại thời điểm transaction bắt đầu
    -- Writers khác không bị blocking
COMMIT;

-- SERIALIZABLE
-- Phù hợp cho: Critical data integrity requirements
-- Ngăn phantom reads hoàn toàn
-- Có thể gây deadlock và performance issues

SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN TRANSACTION;
    SELECT * FROM Inventory WHERE ProductID BETWEEN 1 AND 100;
    -- No inserts/updates/deletes possible in this range
COMMIT;

-- Recommendation:
-- 1. Default (READ COMMITTED) cho hầu hết OLTP
-- 2. RCSI cho applications với nhiều reads và writes
-- 3. SNAPSHOT cho long-running queries/reports
-- 4. REPEATABLE READ cho financial/critical operations
-- 5. SERIALIZABLE chỉ khi cần thiết (performance impact cao)
```
