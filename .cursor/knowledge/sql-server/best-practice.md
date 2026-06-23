# SQL Server Best Practices - Thực Hành Tốt Nhất

## Giới thiệu

Tài liệu này tổng hợp các best practices đã được kiểm chứng cho Microsoft SQL Server trong môi trường enterprise, giúp tối ưu hóa performance, reliability và security.

---

## 1. Chỉ Mục (Indexes)

### 1.1. Tạo Chỉ Mục Covering cho Queries Thường Xuyên

**Nguyên tắc:** Đưa tất cả columns cần thiết vào index để tránh bookmark lookup hoặc table scan.

```sql
-- Bad: Non-covering index
CREATE INDEX IX_Orders_CustomerID ON Orders(CustomerID);
-- Khi query này chạy, SQL phải lookup vào data page
SELECT OrderID, OrderDate, TotalAmount 
FROM Orders 
WHERE CustomerID = 100; -- Bookmark lookup

-- Good: Covering index với INCLUDE
CREATE INDEX IX_Orders_CustomerID_Covering 
ON Orders(CustomerID) 
INCLUDE (OrderDate, TotalAmount);
-- Query có thể satisfied hoàn toàn từ index
SELECT OrderID, OrderDate, TotalAmount 
FROM Orders 
WHERE CustomerID = 100; -- Index seek + key lookup = covering
```

### 1.2. Filtered Index cho Sparse Data

```sql
-- Bad: Index trên tất cả rows (bao gồm NULL và inactive)
CREATE INDEX IX_Orders_Status ON Orders(Status);

-- Good: Filtered index cho điều kiện phổ biến
CREATE INDEX IX_Orders_ActiveCustomer 
ON Orders(CustomerID, OrderDate) 
WHERE Status = 'Active';

-- Sử dụng trong query
SELECT OrderID, OrderDate 
FROM Orders 
WHERE CustomerID = 100 AND Status = 'Active';
-- SQL Server sử dụng filtered index một cách thông minh

-- Thêm ví dụ cho is_deleted flag
CREATE INDEX IX_Products_Active 
ON Products(CategoryID) 
WHERE IsDeleted = 0;
```

### 1.3. Tránh Index trên Columns Thường Xuyên Cập Nhật

```sql
-- Bad: Index trên cột được UPDATE thường xuyên
CREATE INDEX IX_Transactions_Balance ON Transactions(AccountBalance);
-- Mỗi khi Balance thay đổi, index phải cập nhật

-- Good: Chỉ tạo index khi SELECT outweighs INSERT/UPDATE
-- Hoặc đặt index trên cột ít thay đổi
CREATE INDEX IX_Transactions_Date ON Transactions(TransactionDate);
-- TransactionDate thường chỉ set khi INSERT
```

### 1.4. Column Order trong Composite Index

```sql
-- Quy tắc: Equality columns trước, Range/Sort columns sau
-- Bad: Range column đầu tiên
CREATE INDEX IX_Bad ON Orders(OrderDate, CustomerID, Status);

-- Good: Equality columns trước
CREATE INDEX IX_Good ON Orders(CustomerID, Status, OrderDate);

-- Khi query này chạy:
SELECT * FROM Orders 
WHERE CustomerID = 100        -- Equality: first
  AND Status = 'Shipped'      -- Equality: second
  AND OrderDate >= '2024-01-01'; -- Range: last
-- Composite index IX_Good được sử dụng hiệu quả
```

---

## 2. Viết Truy Vấn (Query Writing)

### 2.1. Tránh SELECT *

```sql
-- Bad: Lấy tất cả columns
SELECT * FROM Orders o
JOIN OrderItems oi ON o.OrderID = oi.OrderID
-- Tốn bandwidth, không tận dụng covering index

-- Good: Chỉ lấy columns cần thiết
SELECT 
    o.OrderID,
    o.OrderDate,
    oi.Quantity,
    oi.UnitPrice
FROM Orders o
INNER JOIN OrderItems oi ON o.OrderID = oi.OrderID
WHERE o.CustomerID = @CustomerID;
```

### 2.2. Sử Dụng INNER JOIN Thay vì Subquery Khi Có Thể

```sql
-- Bad: Subquery trong WHERE
SELECT ProductName, Price 
FROM Products p
WHERE CategoryID IN (
    SELECT CategoryID 
    FROM Categories 
    WHERE CategoryName = 'Electronics'
);

-- Good: INNER JOIN
SELECT p.ProductName, p.Price 
FROM Products p
INNER JOIN Categories c ON p.CategoryID = c.CategoryID
WHERE c.CategoryName = 'Electronics';

-- Exception: EXISTS với NULL checks
SELECT CustomerName 
FROM Customers c
WHERE EXISTS (
    SELECT 1 FROM Orders o 
    WHERE o.CustomerID = c.CustomerID 
    AND o.OrderDate >= '2024-01-01'
);
```

### 2.3. Tránh Functions trên Indexed Columns trong WHERE

```sql
-- Bad: Function làm mất index usage
SELECT * FROM Orders 
WHERE YEAR(OrderDate) = 2024
  AND MONTH(OrderDate) = 1;

-- Good: Range predicate giữ index usage
SELECT * FROM Orders 
WHERE OrderDate >= '2024-01-01' 
  AND OrderDate < '2024-02-01';

-- Bad: String manipulation
SELECT * FROM Customers 
WHERE LOWER(Email) = 'test@example.com';

-- Good: Case-insensitive collation hoặc computed column
-- Thiết lập collation case-insensitive khi tạo bảng
-- Hoặc tạo computed column:
ALTER TABLE Customers
ADD EmailNormalized AS LOWER(Email);

CREATE INDEX IX_Customers_EmailNormalized 
ON Customers(EmailNormalized);
```

### 2.4. Sử Dụng Table Hints Một Cách Cẩn Thận

```sql
-- Bad: Hard-code hints không cần thiết
SELECT * FROM Orders WITH (INDEX(IX_Orders_CustomerID))
WHERE CustomerID = 100;
-- Optimizer thường chọn đúng plan

-- Good: Sử dụng hints khi có lý do rõ ràng
-- Ví dụ: Force hash join cho large fact table
SELECT 
    f.SalesDate,
    d.DimensionValue,
    SUM(f.MetricValue) AS TotalSales
FROM FactSales f
HASH JOIN DimProducts d ON f.ProductKey = d.ProductKey
WHERE f.SalesDate >= '2024-01-01'
OPTION (HASH JOIN);
-- Sử dụng khi stats stale hoặc query pattern đặc biệt
```

---

## 3. Transaction Management

### 3.1. Giữ Transactions Ngắn

```sql
-- Bad: Transaction dài với nhiều operations
BEGIN TRANSACTION;
    -- Operation 1: Get customer info
    SELECT @Name = CustomerName FROM Customers WHERE CustomerID = @ID;
    
    -- Network call hoặc business logic ở đây (LONG WAIT)
    EXEC usp_ExternalAPICall; -- Có thể mất vài giây
    
    -- Operation 2: Update
    UPDATE Customers SET LastActivity = GETDATE() WHERE CustomerID = @ID;
COMMIT;
-- Lock giữ quá lâu, blocking other transactions

-- Good: Giữ transaction ngắn
BEGIN TRANSACTION;
    UPDATE Customers SET LastActivity = GETDATE() WHERE CustomerID = @ID;
COMMIT TRANSACTION;

-- Sau đó gọi external API riêng (không trong transaction)
EXEC usp_ExternalAPICall;
```

### 3.2. Xử Lý Error Với Try-Catch

```sql
CREATE PROCEDURE usp_TransferFunds
    @FromAccount INT,
    @ToAccount INT,
    @Amount DECIMAL(18,2)
AS
BEGIN
    SET XACT_ABORT ON; -- Tự động rollback khi error
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Trừ tiền tài khoản nguồn
        UPDATE Accounts 
        SET Balance = Balance - @Amount 
        WHERE AccountID = @FromAccount;
        
        IF @@ROWCOUNT = 0 
            RAISERROR('Source account not found', 16, 1);
        
        -- Kiểm tra số dư (prevent negative balance)
        IF (SELECT Balance FROM Accounts WHERE AccountID = @FromAccount) < 0
            RAISERROR('Insufficient funds', 16, 1);
        
        -- Cộng tiền tài khoản đích
        UPDATE Accounts 
        SET Balance = Balance + @Amount 
        WHERE AccountID = @ToAccount;
        
        IF @@ROWCOUNT = 0
            RAISERROR('Destination account not found', 16, 1);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        -- Kiểm tra nếu transaction còn active
        IF XACT_STATE() <> 0
            ROLLBACK TRANSACTION;
        
        -- Log error hoặc re-throw
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();
        
        -- Log vào bảng
        INSERT INTO ErrorLog (ErrorMessage, ErrorSeverity, ErrorState, ErrorTime)
        VALUES (@ErrorMessage, @ErrorSeverity, @ErrorState, GETDATE());
        
        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END;
```

### 3.3. Sử Dụng Savepoint Cho Partial Rollback

```sql
BEGIN TRANSACTION;
    
    -- Operation A: Phải commit dù có lỗi
    INSERT INTO AuditLog (Action, Timestamp) VALUES ('ProcessStarted', GETDATE());
    SAVE TRANSACTION SavepointA;
    
    BEGIN TRY
        -- Operation B: Có thể rollback
        INSERT INTO TempData (Value) VALUES ('Data1');
        INSERT INTO TempData (Value) VALUES ('Data2');
        
        -- Giả sử có lỗi ở đây
        DECLARE @Value INT = NULL;
        SET @Value = 1 / 0; -- Lỗi!
        
        -- Nếu đến đây, commit
        COMMIT;
    END TRY
    BEGIN CATCH
        -- Rollback chỉ phần B, giữ lại phần A
        ROLLBACK TRANSACTION SavepointA;
        
        -- Log lỗi nhưng vẫn tiếp tục
        INSERT INTO AuditLog (Action, Timestamp) VALUES ('PartialError', GETDATE());
    END CATCH;
    
    -- Phần C: Tiếp tục bình thường
    INSERT INTO AuditLog (Action, Timestamp) VALUES ('ProcessCompleted', GETDATE());
    
COMMIT;
```

---

## 4. Table Design

### 4.1. Sử Dụng Appropriate Data Types

```sql
-- Bad: Over-sized data types
CREATE TABLE BadExample (
    ID INT,                    -- INT cho ID nhỏ là overkill
    Price DECIMAL(18,4),       -- Quá nhiều precision
    Name NVARCHAR(1000),       -- Quá dài
    IsActive BIT,              -- OK
    CreatedDate DATETIME2(7)   -- 7 digits cho seconds là overkill
);

-- Good: Appropriately-sized data types
CREATE TABLE GoodExample (
    ID SMALLINT,               -- Đủ cho IDs < 32767
    Price DECIMAL(10,2),       -- 99999999.99 là đủ
    Name NVARCHAR(100),        -- Tên thường không quá 100 ký tự
    IsActive BIT,              -- OK
    CreatedDate DATETIME2(0)   -- Chỉ cần precision = 0 (1 giây)
);

-- Ngoại lệ: Khi cần lưu trữ ngày tháng với timezone
CREATE TABLE Events (
    EventTime DATETIMEOFFSET(7) -- Cần timezone info
);
```

### 4.2. Sử Dụng VARCHAR Thay vì TEXT/IMAGE

```sql
-- Bad: Legacy large object types
CREATE TABLE BadDocuments (
    DocumentID INT PRIMARY KEY,
    DocumentText TEXT,     -- Deprecated
    DocumentImage IMAGE,   -- Deprecated
    DocumentData VARBINARY(MAX) -- OK nhưng legacy
);

-- Good: Modern MAX types
CREATE TABLE GoodDocuments (
    DocumentID INT PRIMARY KEY,
    DocumentText NVARCHAR(MAX),     -- Thay thế TEXT
    DocumentImage VARBINARY(MAX),   -- Thay thế IMAGE
    FileHash NVARCHAR(64)          -- For deduplication
);

-- Full-Text Search
CREATE FULLTEXT CATALOG ft_catalog;
CREATE FULLTEXT INDEX ON GoodDocuments(DocumentText)
KEY INDEX PK_GoodDocuments
ON ft_catalog;
```

### 4.3. Tránh Nullable Columns Không Cần Thiết

```sql
-- Bad: Many NULLable columns
CREATE TABLE BadOrders (
    OrderID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    ShippingAddress NVARCHAR(500) NULL,     -- Thường có giá trị
    BillingAddress NVARCHAR(500) NULL,      -- Thường có giá trị
    DiscountCode NVARCHAR(50) NULL,         -- Nullable nhưng 90% có giá trị
    Notes NVARCHAR(MAX) NULL,               -- Nullable nhưng 70% có giá trị
    GiftWrap BIT NULL                       -- BIT nên NOT NULL
);

-- Good: NOT NULL với default values
CREATE TABLE GoodOrders (
    OrderID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    ShippingAddress NVARCHAR(500) NOT NULL,
    BillingAddress NVARCHAR(500) NOT NULL,
    DiscountCode NVARCHAR(50) NULL,         -- Chỉ NULL khi không có discount
    Notes NVARCHAR(MAX) NULL,
    GiftWrap BIT NOT NULL DEFAULT 0
);
```

---

## 5. Performance Tuning

### 5.1. Sử Dụng Parameterized Queries

```sql
-- Bad: Ad-hoc queries với string concatenation
-- (Tạo nhiều cached plans, dễ bị SQL injection)
string query = "SELECT * FROM Products WHERE CategoryID = " + categoryId;
SqlCommand cmd = new SqlCommand(query, connection);

-- Good: Parameterized queries
string query = "SELECT * FROM Products WHERE CategoryID = @CategoryID";
SqlCommand cmd = new SqlCommand(query, connection);
cmd.Parameters.AddWithValue("@CategoryID", categoryId);

-- In SQL: Stored procedures tự động parameterized
CREATE PROCEDURE usp_GetProductsByCategory
    @CategoryID INT
AS
BEGIN
    SELECT ProductID, ProductName, Price
    FROM Products
    WHERE CategoryID = @CategoryID;
END;
```

### 5.2. Batch Operations Cho Large Data

```sql
-- Bad: Insert từng row (rất chậm)
WHILE @Counter <= @TotalRows
BEGIN
    INSERT INTO BigTable (Column1, Column2)
    VALUES (@Value1, @Value2);
    SET @Counter = @Counter + 1;
END;

-- Good: Batch insert
INSERT INTO BigTable (Column1, Column2)
SELECT Column1, Column2 FROM SourceTable;

-- Good: Bulk Insert
BULK INSERT StagingTable
FROM 'C:\DataFiles\source.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);

-- Good: Table-valued parameters
CREATE TYPE IntList AS TABLE (Value INT);
CREATE PROCEDURE usp_InsertMultipleProducts
    @ProductIDs IntList READONLY
AS
BEGIN
    INSERT INTO Products (ProductName, CategoryID)
    SELECT p.ProductName, @CategoryID
    FROM SourceProducts p
    JOIN @ProductIDs pid ON p.SourceID = pid.Value;
END;

-- Gọi stored procedure
DECLARE @IDs IntList;
INSERT INTO @IDs VALUES (1), (2), (3), (4), (5);
EXEC usp_InsertMultipleProducts @ProductIDs = @IDs;
```

### 5.3. Sử Dụng Window Functions Thay vì Self-Join

```sql
-- Bad: Self-join cho running total
SELECT 
    o1.OrderDate,
    o1.Amount,
    SUM(o2.Amount) AS RunningTotal
FROM Orders o1
INNER JOIN Orders o2 ON o1.OrderDate >= o2.OrderDate
GROUP BY o1.OrderDate, o1.Amount
ORDER BY o1.OrderDate;
-- O(n²) complexity, rất chậm cho large tables

-- Good: Window function
SELECT 
    OrderDate,
    Amount,
    SUM(Amount) OVER (ORDER BY OrderDate) AS RunningTotal
FROM Orders
ORDER BY OrderDate;

-- Bad: Self-join cho ranking
SELECT 
    e1.EmployeeName,
    e1.Department,
    e1.Salary,
    (SELECT COUNT(*) FROM Employees e2 
     WHERE e2.Department = e1.Department 
     AND e2.Salary > e1.Salary) + 1 AS RankInDept
FROM Employees e1;

-- Good: Window function
SELECT 
    EmployeeName,
    Department,
    Salary,
    RANK() OVER (PARTITION BY Department ORDER BY Salary DESC) AS RankInDept
FROM Employees;
```

### 5.4. Tránh OR Trong WHERE Clause

```sql
-- Bad: OR làm chậm query
SELECT * FROM Orders
WHERE CustomerID = 100 OR CustomerID = 200 OR CustomerID = 300;

-- Good: IN
SELECT * FROM Orders
WHERE CustomerID IN (100, 200, 300);

-- Bad: OR với different columns
SELECT * FROM Orders
WHERE OrderDate = '2024-01-01' OR ShippingDate = '2024-01-01';

-- Good: UNION ALL (hoặc UNION nếu cần loại bỏ duplicates)
SELECT * FROM Orders WHERE OrderDate = '2024-01-01'
UNION ALL
SELECT * FROM Orders WHERE ShippingDate = '2024-01-01' 
    AND OrderDate <> '2024-01-01';
```

---

## 6. Security

### 6.1. Sử Dụng Stored Procedures Thay vì Dynamic SQL

```sql
-- Bad: Dynamic SQL với string concatenation
CREATE PROCEDURE usp_GetCustomerBad
    @CustomerID INT
AS
BEGIN
    DECLARE @SQL NVARCHAR(500);
    SET @SQL = N'SELECT * FROM Customers WHERE CustomerID = ' + CAST(@CustomerID AS NVARCHAR(10));
    EXEC sp_executesql @SQL;
    -- SQL Injection risk, không dùng được parameterization tốt
END;

-- Good: Stored procedure với parameters
CREATE PROCEDURE usp_GetCustomerGood
    @CustomerID INT
AS
BEGIN
    SELECT * FROM Customers WHERE CustomerID = @CustomerID;
    -- An toàn, parameterized
END;

-- Good: sp_executesql với parameters
CREATE PROCEDURE usp_GetCustomerBetter
    @CustomerID INT
AS
BEGIN
    DECLARE @SQL NVARCHAR(500);
    SET @SQL = N'SELECT * FROM Customers WHERE CustomerID = @ID';
    EXEC sp_executesql @SQL, N'@ID INT', @ID = @CustomerID;
    -- Parameterized, an toàn
END;
```

### 6.2. Principle of Least Privilege

```sql
-- Bad: Dùng db_owner hoặc sa cho application
-- Connection string của app dùng 'sa' account

-- Good: Tạo application role với minimal permissions
USE MyDB;
GO

-- Tạo role cho application
CREATE APPLICATION ROLE AppReaderRole 
WITH PASSWORD = 'ComplexPassword123!';

-- Grant chỉ những permissions cần thiết
GRANT SELECT ON SCHEMA::dbo TO AppReaderRole;
GRANT EXECUTE ON SCHEMA::dbo TO AppReaderRole;

-- Tạo user cho app
CREATE USER AppUser FOR LOGIN AppLogin;
ALTER ROLE AppReaderRole ADD MEMBER AppUser;

-- Khi application kết nối, activate role
EXEC sp_setapprole 'AppReaderRole', 'ComplexPassword123!';
```

### 6.3. Mã Hóa Sensitive Data

```sql
-- TDE cho database encryption
USE master;
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'MasterKeyPassword123!';
CREATE CERTIFICATE MyDBCert WITH SUBJECT = 'My Database Certificate';
BACKUP CERTIFICATE MyDBCert TO FILE = 'C:\Backups\MyCert.cer'
    PRIVATE KEY (FILE = 'C:\Backups\MyCertKey.key',
                 ENCRYPTION BY PASSWORD = 'PrivateKeyPassword123!');

USE MyDB;
CREATE DATABASE ENCRYPTION KEY
BY ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE MyDBCert;
ALTER DATABASE MyDB SET ENCRYPTION ON;

-- Always Encrypted cho sensitive columns
CREATE TABLE SensitiveData (
    ID INT PRIMARY KEY,
    SSN CHAR(11) COLLATE Latin1_General_BIN2 
        ENCRYPTED WITH (ENCRYPTION_TYPE = DETERMINISTIC,
                       ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256',
                       COLUMN_ENCRYPTION_KEY = MyCEK) NOT NULL,
    Salary DECIMAL(10,2) ENCRYPTED WITH (
        ENCRYPTION_TYPE = DETERMINISTIC,
        ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256',
        COLUMN_ENCRYPTION_KEY = MyCEK
    ) NOT NULL
);
```

---

## 7. Maintenance

### 7.1. Regular Index Maintenance

```sql
-- Tạo stored procedure cho index maintenance
CREATE PROCEDURE usp_IndexMaintenance
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @TableName NVARCHAR(128);
    DECLARE @IndexName NVARCHAR(128);
    DECLARE @Fragmentation FLOAT;
    DECLARE @PageCount INT;
    
    -- Cursor để duyệt qua các indexes
    DECLARE index_cursor CURSOR FOR
    SELECT 
        OBJECT_NAME(i.object_id) AS TableName,
        i.name AS IndexName,
        ips.avg_fragmentation_in_percent,
        ips.page_count
    FROM sys.dm_db_index_physical_stats(
        DB_ID(), NULL, NULL, NULL, 'DETAILED'
    ) ips
    JOIN sys.indexes i ON ips.object_id = i.object_id 
        AND ips.index_id = i.index_id
    WHERE ips.avg_fragmentation_in_percent > 5
        AND ips.page_count > 100  -- Ignore small indexes
        AND i.is_disabled = 0
    ORDER BY ips.avg_fragmentation_in_percent DESC;
    
    OPEN index_cursor;
    FETCH NEXT FROM index_cursor INTO @TableName, @IndexName, @Fragmentation, @PageCount;
    
    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Reorganize nếu fragmentation < 30%
        IF @Fragmentation < 30
        BEGIN
            PRINT 'Reorganizing ' + @TableName + '.' + @IndexName + 
                  ' (Fragmentation: ' + CAST(@Fragmentation AS VARCHAR(10)) + '%)';
            EXEC('ALTER INDEX ' + @IndexName + ' ON ' + @TableName + ' REORGANIZE');
        END
        -- Rebuild nếu fragmentation >= 30%
        ELSE
        BEGIN
            PRINT 'Rebuilding ' + @TableName + '.' + @IndexName + 
                  ' (Fragmentation: ' + CAST(@Fragmentation AS VARCHAR(10)) + '%)';
            EXEC('ALTER INDEX ' + @IndexName + ' ON ' + @TableName + ' REBUILD');
        END
        
        FETCH NEXT FROM index_cursor INTO @TableName, @IndexName, @Fragmentation, @PageCount;
    END
    
    CLOSE index_cursor;
    DEALLOCATE index_cursor;
END;

-- Chạy maintenance job
EXEC usp_IndexMaintenance;
```

### 7.2. Statistics Maintenance

```sql
-- Cập nhật statistics định kỳ
CREATE PROCEDURE usp_UpdateStatistics
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Update all statistics với FULLSCAN cho accuracy
    EXEC sp_MSforeachtable 'UPDATE STATISTICS ? WITH FULLSCAN';
    
    -- Hoặc chỉ update stale statistics
    DECLARE @TableName NVARCHAR(128);
    
    DECLARE stats_cursor CURSOR FOR
    SELECT DISTINCT 
        OBJECT_NAME(s.object_id)
    FROM sys.dm_db_stats_properties(NULL, NULL) s
    JOIN sys.tables t ON s.object_id = t.object_id
    WHERE AUTO_UPDATEStatistics = 1;
    
    OPEN stats_cursor;
    FETCH NEXT FROM stats_cursor INTO @TableName;
    
    WHILE @@FETCH_STATUS = 0
    BEGIN
        EXEC('UPDATE STATISTICS ' + @TableName);
        FETCH NEXT FROM stats_cursor INTO @TableName;
    END
    
    CLOSE stats_cursor;
    DEALLOCATE stats_cursor;
END;
```

### 7.3. Backup Strategy

```sql
-- Full backup (daily)
BACKUP DATABASE MyDB 
TO DISK = 'C:\Backups\MyDB_Full_20240115.bak'
WITH COMPRESSION, CHECKSUM, STATS = 10;

-- Differential backup (every 4 hours)
BACKUP DATABASE MyDB 
TO DISK = 'C:\Backups\MyDB_Diff_20240115_1200.bak'
WITH COMPRESSION, CHECKSUM, DIFFERENTIAL, STATS = 10;

-- Transaction log backup (every 15 minutes)
BACKUP LOG MyDB 
TO DISK = 'C:\Backups\MyDB_Log_20240115_1215.trn'
WITH COMPRESSION, CHECKSUM, STATS = 10;

-- Verify backup integrity
RESTORE VERIFYONLY 
FROM DISK = 'C:\Backups\MyDB_Full_20240115.bak'
WITH CHECKSUM;

-- Test restore
RESTORE DATABASE MyDB_TestRestore
FROM DISK = 'C:\Backups\MyDB_Full_20240115.bak'
WITH MOVE 'MyDB_Data' TO 'C:\Data\MyDB_TestRestore.mdf',
     MOVE 'MyDB_Log' TO 'C:\Logs\MyDB_TestRestore.ldf';
```

---

## 8. Error Handling và Logging

### 8.1. Centralized Error Logging

```sql
CREATE TABLE ErrorLog (
    ErrorID INT IDENTITY(1,1) PRIMARY KEY,
    ErrorNumber INT,
    ErrorSeverity INT,
    ErrorState INT,
    ErrorProcedure NVARCHAR(128),
    ErrorLine INT,
    ErrorMessage NVARCHAR(4000),
    UserName NVARCHAR(128),
    HostName NVARCHAR(128),
    ProgramName NVARCHAR(128),
    ErrorTime DATETIME2 DEFAULT SYSDATETIME(),
    AdditionalData XML
);

CREATE NONCLUSTERED INDEX IX_ErrorLog_Time 
ON ErrorLog(ErrorTime DESC);

GO

CREATE PROCEDURE usp_LogError
AS
BEGIN
    -- Get error information
    DECLARE @ErrorNumber INT = ERROR_NUMBER();
    DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
    DECLARE @ErrorState INT = ERROR_STATE();
    DECLARE @ErrorProcedure NVARCHAR(128) = ERROR_PROCEDURE();
    DECLARE @ErrorLine INT = ERROR_LINE();
    DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
    
    -- Log to table
    INSERT INTO ErrorLog (
        ErrorNumber, ErrorSeverity, ErrorState, ErrorProcedure,
        ErrorLine, ErrorMessage, UserName, HostName, ProgramName, AdditionalData
    )
    SELECT 
        @ErrorNumber, @ErrorSeverity, @ErrorState, @ErrorProcedure,
        @ErrorLine, @ErrorMessage, 
        SUSER_SNAME(), HOST_NAME(), APP_NAME(),
        (SELECT * FROM OPENJSON((SELECT 1)) FOR JSON PATH));
    
    -- Return error ID for reference
    RETURN SCOPE_IDENTITY();
END;

GO

CREATE TRIGGER trg_CatchErrors
ON DATABASE
FOR SP_SQL_ERROR
AS
BEGIN
    EXEC usp_LogError;
END;
```

---

## 9. High Availability và Disaster Recovery

### 9.1. Implement Always On Availability Groups

```sql
-- Primary Replica: Tạo backup để restore lên secondary
BACKUP DATABASE MyDB 
TO DISK = '\\BackupShare\MyDB_Full.bak'
WITH COMPRESSION, CHECKSUM;

BACKUP LOG MyDB
TO DISK = '\\BackupShare\MyDB_Log.trn'
WITH COMPRESSION, CHECKSUM;

-- Secondary Replica: Restore với NORECOVERY
RESTORE DATABASE MyDB
FROM DISK = '\\BackupShare\MyDB_Full.bak'
WITH MOVE 'MyDB_Data' TO 'E:\Data\MyDB.mdf',
     MOVE 'MyDB_Log' TO 'F:\Logs\MyDB.ldf',
     NORECOVERY, REPLACE;

RESTORE LOG MyDB
FROM DISK = '\\BackupShare\MyDB_Log.trn'
WITH NORECOVERY;

-- Join vào Availability Group
ALTER DATABASE MyDB SET HADR AVAILABILITY GROUP = MyAG;

-- Kiểm tra sync status
SELECT 
    ar.replica_server_name,
    ar.availability_mode_desc,
    rcs.synchronization_state_desc,
    rcs.log_send_queue_size / 1024.0 AS log_send_mb,
    rcs.redo_queue_size / 1024.0 AS redo_queue_mb
FROM sys.availability_replicas ar
JOIN sys.dm_hadr_database_replica_states rcs 
    ON ar.replica_id = rcs.replica_id
JOIN sys.databases d ON rcs.database_id = d.database_id
WHERE d.name = 'MyDB';
```

### 9.2. Read-Only Routing Configuration

```sql
-- Bật read-only routing
ALTER AVAILABILITY GROUP MyAG
MODIFY REPLICA ON 'PrimaryServer' 
WITH (SECONDARY_ROLE(ALLOW_CONNECTIONS = READ_ONLY));

ALTER AVAILABILITY GROUP MyAG
MODIFY REPLICA ON 'SecondaryServer1'
WITH (SECONDARY_ROLE(ALLOW_CONNECTIONS = READ_ONLY));

ALTER AVAILABILITY GROUP MyAG
MODIFY REPLICA ON 'PrimaryServer'
WITH (PRIMARY_ROLE(READ_ONLY_ROUTING_LIST = ('SecondaryServer1', 'SecondaryServer2')));

ALTER AVAILABILITY GROUP MyAG
MODIFY REPLICA ON 'SecondaryServer1'
WITH (PRIMARY_ROLE(READ_ONLY_ROUTING_URL = 'TCP://SecondaryServer1:1433'));

ALTER AVAILABILITY GROUP MyAG
MODIFY REPLICA ON 'SecondaryServer2'
WITH (PRIMARY_ROLE(READ_ONLY_ROUTING_URL = 'TCP://SecondaryServer2:1433'));

-- Connection string cho read-only workloads
"Server=MyAGListener;Database=MyDB;ApplicationIntent=ReadOnly;Integrated Security=true;"
```

---

## 10. Monitoring và Alerting

### 10.1. Performance Baseline

```sql
-- Tạo bảng lưu baseline metrics
CREATE TABLE PerformanceBaseline (
    BaselineID INT IDENTITY(1,1) PRIMARY KEY,
    CaptureTime DATETIME2,
    MetricName NVARCHAR(128),
    MetricValue FLOAT,
    MetricUnit NVARCHAR(20)
);

-- Stored procedure để capture baseline
CREATE PROCEDURE usp_CapturePerformanceBaseline
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Batch Performance
    INSERT INTO PerformanceBaseline (CaptureTime, MetricName, MetricValue, MetricUnit)
    SELECT 
        SYSDATETIME(),
        counter_name,
        cntr_value,
        'Count'
    FROM sys.dm_os_performance_counters
    WHERE object_name LIKE '%Batch Resp%';
    
    -- Wait Statistics
    INSERT INTO PerformanceBaseline (CaptureTime, MetricName, MetricValue, MetricUnit)
    SELECT 
        SYSDATETIME(),
        wait_type,
        wait_time_ms / 1000.0,  -- Convert to seconds
        'Seconds'
    FROM sys.dm_os_wait_stats
    WHERE wait_time_ms > 1000;
    
    -- Active Sessions
    INSERT INTO PerformanceBaseline (CaptureTime, MetricName, MetricValue, MetricUnit)
    SELECT 
        SYSDATETIME(),
        'ActiveRequests',
        COUNT(*),
        'Count'
    FROM sys.dm_exec_requests
    WHERE session_id > 50;  -- Exclude system sessions
END;
```

### 10.2. Query Performance Monitoring

```sql
-- Kích hoạt Query Store
ALTER DATABASE MyDB SET QUERY_STORE = ON;
ALTER DATABASE MyDB SET QUERY_STORE (
    OPERATION_MODE = READ_WRITE,
    MAX_STORAGE_SIZE_MB = 1024,
    QUERY_CAPTURE_MODE = AUTO,
    WAIT_STATS_CAPTURE_MODE = ON,
    MAX_PLANS_PER_QUERY = 20
);

-- Xem top resource-consuming queries
SELECT TOP 25 
    qs.query_id,
    qt.query_text_id,
    CAST(qs.query_plan AS XML) AS query_plan,
    rs.execution_count,
    rs.avg_duration / 1000.0 AS avg_duration_ms,
    rs.avg_cpu_time / 1000.0 AS avg_cpu_ms,
    rs.avg_logical_io_reads / 128.0 AS avg_logical_read_mb,
    rs.avg_physical_io_reads / 128.0 AS avg_physical_read_mb,
    SUBSTRING(qt.query_sql_text, 1, 500) AS query_text
FROM sys.query_store_query q
JOIN sys.query_store_query_text qt ON q.query_id = qt.query_text_id
JOIN sys.query_store_plan p ON q.query_id = p.query_id
JOIN sys.query_store_runtime_stats rs ON p.plan_id = rs.plan_id
ORDER BY rs.avg_duration DESC;

-- Force plan tốt
DECLARE @good_plan_id BIGINT = (SELECT plan_id 
    FROM sys.query_store_plan 
    WHERE query_id = @query_id 
    AND avg_duration < @target_duration);
    
EXEC sp_query_store_force_plan @query_id, @good_plan_id;
```
