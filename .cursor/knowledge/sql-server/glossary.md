# SQL Server Glossary - Từ Điển Thuật Ngữ

## Giới thiệu

Tài liệu này cung cấp định nghĩa chi tiết cho các thuật ngữ quan trọng liên quan đến Microsoft SQL Server, được sử dụng trong Cursor Enterprise Framework.

---

## Danh Sách Thuật Ngữ

### 1. ACID (Atomicity, Consistency, Isolation, Durability)

**Định nghĩa:** Bộ bốn tính chất đảm bảo tính tin cậy của transaction trong database:
- **Atomicity (Tính nguyên tử):** Mọi thao tác trong transaction phải hoàn thành hoặc không có gì xảy ra
- **Consistency (Tính nhất quán):** Database phải chuyển từ trạng thái hợp lệ này sang trạng thái hợp lệ khác
- **Isolation (Tính cô lập):** Các transaction đồng thời không ảnh hưởng lẫn nhau
- **Durability (Tính bền vững):** Kết quả transaction được lưu vĩnh viễn sau khi hoàn thành

** Ví dụ:**
```sql
BEGIN TRANSACTION;
    UPDATE Accounts SET Balance = Balance - 1000 WHERE AccountID = 1;
    UPDATE Accounts SET Balance = Balance + 1000 WHERE AccountID = 2;
COMMIT TRANSACTION;
-- Nếu câu lệnh thứ 2 thất bại, cả hai đều rollback
```

---

### 2. Clustered Index

**Định nghĩa:** Index sắp xếp dữ liệu vật lý trong bảng theo thứ tự của key. Mỗi bảng chỉ có thể có một clustered index vì dữ liệu chỉ có thể được sắp xếp một cách vật lý theo một cách.

**Đặc điểm:**
- Thường được tạo trên PRIMARY KEY
- Tăng tốc độ truy vấn range (BETWEEN, >, <)
- Phù hợp cho các cột có tính uniqueness cao
- Table Heap chuyển thành clustered table

** Ví dụ:**
```sql
CREATE CLUSTERED INDEX IX_Orders_OrderDate 
ON Orders(OrderDate, OrderID);

-- Hoặc khi tạo bảng
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY CLUSTERED,
    OrderDate DATETIME,
    CustomerID INT
);
```

---

### 3. Deadlock

**Định nghĩa:** Tình trạng hai hoặc nhiều process giữ tài nguyên và chờ nhau giải phóng, tạo thành vòng chờ vô hạn. SQL Server tự động phát hiện và hủy một trong các transaction để phá vòng deadlock.

**Cơ chế hoạt động:**
- SQL Server sử dụng Wait-For Graph để phát hiện deadlock
- Deadlock victim bị rollback tự động
- Error 1205 được trả về cho transaction bị hủy

** Ví dụ:**
```sql
-- Session 1
BEGIN TRANSACTION;
    UPDATE Products SET Price = 99 WHERE ProductID = 1; -- Giữ IX lock
    -- Chờ Session 2 release lock trên ProductID = 2

-- Session 2  
BEGIN TRANSACTION;
    UPDATE Products SET Price = 149 WHERE ProductID = 2; -- Giữ IX lock
    -- Chờ Session 1 release lock trên ProductID = 1
    -- => DEADLOCK
```

**Xử lý:**
```sql
-- Thiết lập timeout cho deadlock
SET DEADLOCK_PRIORITY NORMAL; -- Hoặc LOW, HIGH, numeric value

-- Bắt và xử lý deadlock
BEGIN TRY
    -- Các câu lệnh SQL
END TRY
BEGIN CATCH
    IF ERROR_NUMBER() = 1205
        -- Retry logic
END CATCH;
```

---

### 4. Execution Plan

**Định nghĩa:** Kế hoạch thực thi mà SQL Server Query Optimizer tạo ra để thực thi một câu truy vấn. Chứa thông tin về cách SQL Server sẽ truy cập, join, filter và aggregate dữ liệu.

**Các loại Operator phổ biến:**
- **Table Scan:** Đọc toàn bộ bảng
- **Index Scan:** Đọc toàn bộ index
- **Index Seek:** Tìm kiếm có chỉ mục
- **Nested Loop Join:** Join bằng nested loops
- **Hash Join:** Join bằng hash table
- **Merge Join:** Join bằng sorted merge

**Xem Execution Plan:**
```sql
-- Actual Execution Plan
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

SELECT * FROM Orders WHERE OrderDate > '2024-01-01';

-- Xem qua SSMS hoặc sử dụng query
SELECT * FROM sys.dm_exec_query_plan(@plan_handle);
```

---

### 5. Locking Mechanism

**Định nghĩa:** Cơ chế đồng bộ hóa của SQL Server để đảm bảo tính nhất quán của dữ liệu khi nhiều users truy cập đồng thời.

**Các loại Lock:**
| Loại Lock | Mô tả |
|-----------|-------|
| SHARED (S) | Cho phép đọc, không cho sửa |
| EXCLUSIVE (X) | Không cho phép đọc hoặc sửa |
| UPDATE (U) | Lock trung gian khi cập nhật |
| INTENT | Lock trên parent resource |

**Isolation Levels và Locking:**
```sql
-- Read Uncommitted - Không lock, đọc dirty data
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

-- Read Committed (default) - Lock khi đọc
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Repeatable Read - Lock các row đã đọc
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- Serializable - Lock toàn bộ range
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Snapshot - Sử dụng row versioning
ALTER DATABASE MyDB SET ALLOW_SNAPSHOT_ISOLATION ON;
SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
```

---

### 6. Normalization vs Denormalization

**Định nghĩa:**
- **Normalization:** Quá trình tổ chức dữ liệu để giảm redundancy và cải thiện integrity. Các dạng chuẩn từ 1NF đến 3NF, BCNF.
- **Denormalization:** Thêm redundant data để tăng performance đọc, thường dùng trong reporting databases.

**Các dạng chuẩn:**
```
1NF: Atomic values, no repeating groups
2NF: 1NF + No partial dependencies (composite keys)
3NF: 2NF + No transitive dependencies
BCNF: 3NF + Every determinant must be a candidate key
```

** Ví dụ Normalization:**
```sql
-- 1NF: Tách repeating group
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName NVARCHAR(100),
    -- Thay vì Phone1, Phone2, Phone3 => Tạo bảng riêng
);

CREATE TABLE CustomerPhones (
    CustomerID INT FOREIGN KEY,
    PhoneNumber NVARCHAR(20),
    PhoneType NVARCHAR(20)
);

-- 3NF: Tách transitive dependency
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    ProductID INT,
    OrderDate DATE
    -- Không lưu CustomerName, ProductName ở đây
    -- Chỉ lưu foreign keys
);
```

---

### 7. Primary Key vs Foreign Key

**Primary Key:**
- Identifies duy nhất mỗi row trong bảng
- Không chứa giá trị NULL
- Chỉ có một Primary Key trên mỗi bảng
- Tự động tạo clustered index (trừ khi chỉ định khác)
- Tính uniqueness được enforce

```sql
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY,
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50)
);
```

**Foreign Key:**
- Tạo mối quan hệ referential integrity giữa hai bảng
- Giá trị phải tồn tại trong bảng cha hoặc NULL
- Có thể có nhiều Foreign Keys trên bảng
- Hỗ trợ ON DELETE/UPDATE actions

```sql
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    EmployeeID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
        ON DELETE NO ACTION
        ON UPDATE CASCADE
);
```

---

### 8. Query Optimizer

**Định nghĩa:** Thành phần của SQL Server Database Engine phân tích và chọn kế hoạch thực thi tối ưu nhất cho câu truy vấn dựa trên statistics và available indexes.

**Các hoạt động chính:**
1. Parsing: Chuyển SQL thành parse tree
2. Binding: Kiểm tra semantic và resolution names
3. Optimization: Tìm kế hoạch thực thi tối ưu
4. Execution: Thực thi theo kế hoạch đã chọn

**Statistics:**
```sql
-- Cập nhật statistics
UPDATE STATISTICS Orders;

-- Xem statistics
DBCC SHOW_STATISTICS('Orders', 'IX_Orders_CustomerID');

-- Auto-update statistics
ALTER DATABASE MyDB SET AUTO_UPDATE_STATISTICS ON;
```

---

### 9. Recovery Model

**Định nghĩa:** Thiết lập cấp độ logging và khả năng phục hồi của database. Ảnh hưởng đến kích thước transaction log và khả năng recovery.

**Các Recovery Models:**

| Model | Logging | Recovery Point | Use Case |
|-------|---------|----------------|----------|
| Full | Full | Point-in-time | Production, critical data |
| Bulk-Logged | Minimal + Bulk | Last backup | Large data import |
| Simple | Minimal | Last checkpoint | Development, small DB |

**Cấu hình:**
```sql
-- Xem recovery model
SELECT name, recovery_model_desc 
FROM sys.databases 
WHERE name = 'MyDB';

-- Thay đổi recovery model
ALTER DATABASE MyDB SET RECOVERY FULL;
ALTER DATABASE MyDB SET RECOVERY BULK_LOGGED;
ALTER DATABASE MyDB SET RECOVERY SIMPLE;
```

---

### 10. Row Versioning

**Định nghĩa:** Cơ chế lưu trữ các phiên bản cũ của rows trong tempdb, cho phép đọc dữ liệu mà không cần blocking writers (Read Committed Snapshot Isolation - RCSI).

**Các loại:**
- **RCSI (Read Committed Snapshot Isolation):** Mỗi statement đọc phiên bản committed mới nhất
- **Snapshot Isolation:** Mỗi transaction đọc phiên bản tại thời điểm bắt đầu transaction

```sql
-- Kích hoạt RCSI
ALTER DATABASE MyDB SET READ_COMMITTED_SNAPSHOT ON;

-- Sử dụng Snapshot Isolation
SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
BEGIN TRANSACTION;
    SELECT * FROM Products;
COMMIT;
```

---

### 11. Stored Procedure

**Định nghĩa:** Nhóm các câu lệnh SQL đã được biên dịch và lưu trữ trong database. Có thể nhận parameters, trả về values, và được gọi bởi ứng dụng.

**Ưu điểm:**
- Performance tốt hơn (compiled và cached)
- Giảm network traffic
- Bảo mật tốt hơn (grants on procedures)
- Tái sử dụng code
- Centralized business logic

** Ví dụ:**
```sql
CREATE PROCEDURE usp_GetOrdersByCustomer
    @CustomerID INT,
    @StartDate DATE = NULL,
    @EndDate DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        o.OrderID,
        o.OrderDate,
        o.TotalAmount,
        COUNT(oi.OrderItemID) AS ItemCount
    FROM Orders o
    LEFT JOIN OrderItems oi ON o.OrderID = oi.OrderID
    WHERE o.CustomerID = @CustomerID
        AND (@StartDate IS NULL OR o.OrderDate >= @StartDate)
        AND (@EndDate IS NULL OR o.OrderDate <= @EndDate)
    GROUP BY o.OrderID, o.OrderDate, o.TotalAmount
    ORDER BY o.OrderDate DESC;
END;

-- Gọi stored procedure
EXEC usp_GetOrdersByCustomer 
    @CustomerID = 100,
    @StartDate = '2024-01-01';
```

---

### 12. Transaction Log

**Định nghĩa:** File log ghi lại tất cả thay đổi trong database, phục vụ cho:
- Crash recovery
- Point-in-time recovery
- Replication
- Auditing

**Kiến trúc Log:**
```
Virtual Log Files (VLFs) -> Log Sequence Number (LSN)
[log records: BEGIN, MODIFY, COMMIT, etc.]
```

**Quản lý Log:**
```sql
-- Xem log usage
DBCC SQLPERF(LOGSPACE);

-- Xem log records
SELECT * FROM sys.dm_db_log_info(DB_ID());

-- Shrink log file
USE MyDB;
CHECKPOINT;
BACKUP LOG MyDB TO DISK = 'NUL';
DBCC SHRINKFILE(MyDB_log, 1000); -- Target size in MB

-- Tăng kích thước log
ALTER DATABASE MyDB MODIFY FILE (
    NAME = MyDB_log,
    SIZE = 100MB
);
```

---

### 13. Trigger

**Định nghĩa:** Đối tượng database tự động thực thi khi xảy ra certain events (INSERT, UPDATE, DELETE) trên một bảng hoặc view.

**Các loại Trigger:**
- **DML Trigger:** Kích hoạt khi có DML events (INSERT, UPDATE, DELETE)
- **DDL Trigger:** Kích hoạt khi có DDL events (CREATE, ALTER, DROP)
- **Logon Trigger:** Kích hoạt khi có logon events

** Ví dụ:**
```sql
-- Trigger audit log
CREATE TRIGGER trg_AuditOrderChanges
ON Orders
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Log inserted rows
    INSERT INTO AuditLog (TableName, Action, OldData, NewData, ModifiedBy)
    SELECT 
        'Orders',
        'INSERT',
        NULL,
        (SELECT i.* FOR JSON PATH),
        SUSER_SNAME()
    FROM inserted i;
    
    -- Log deleted rows
    INSERT INTO AuditLog (TableName, Action, OldData, NewData, ModifiedBy)
    SELECT 
        'Orders',
        'DELETE',
        (SELECT d.* FOR JSON PATH),
        NULL,
        SUSER_SNAME()
    FROM deleted d;
END;
```

---

### 14. Window Functions

**Định nghĩa:** Functions thực hiện tính toán trên một tập rows liên quan đến current row mà không cần GROUP BY. Sử dụng OVER() clause để định nghĩa window.

**Các loại Window Functions:**
- **Aggregate:** SUM(), AVG(), COUNT(), MIN(), MAX()
- **Ranking:** ROW_NUMBER(), RANK(), DENSE_RANK(), NTILE()
- **Value:** LAG(), LEAD(), FIRST_VALUE(), LAST_VALUE()

** Ví dụ:**
```sql
-- Ranking với Window Functions
SELECT 
    EmployeeName,
    Department,
    Salary,
    ROW_NUMBER() OVER (PARTITION BY Department ORDER BY Salary DESC) AS RowNum,
    RANK() OVER (ORDER BY Salary DESC) AS Rank,
    DENSE_RANK() OVER (ORDER BY Salary DESC) AS DenseRank
FROM Employees;

-- Running total
SELECT 
    OrderDate,
    DailySales,
    SUM(DailySales) OVER (ORDER BY OrderDate) AS RunningTotal,
    AVG(DailySales) OVER (ORDER BY OrderDate 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS MovingAvg7Day
FROM DailySalesSummary;

-- LAG và LEAD
SELECT 
    ProductName,
    Price,
    LAG(Price, 1) OVER (ORDER BY ProductID) AS PreviousPrice,
    LEAD(Price, 1) OVER (ORDER BY ProductID) AS NextPrice,
    Price - LAG(Price, 1) OVER (ORDER BY ProductID) AS PriceChange
FROM Products;
```

---

### 15. CTE (Common Table Expression)

**Định nghĩa:** Tạo view tạm thời có thể tham chiếu trong câu truy vấn, giúp code dễ đọc và maintain hơn. Có hai loại: Non-recursive và Recursive CTE.

** Ví dụ Non-recursive:**
```sql
WITH SalesByRegion AS (
    SELECT 
        r.RegionName,
        SUM(s.SaleAmount) AS TotalSales
    FROM Sales s
    JOIN Regions r ON s.RegionID = r.RegionID
    WHERE s.SaleDate >= '2024-01-01'
    GROUP BY r.RegionName
)
SELECT 
    RegionName,
    TotalSales,
    TotalSales * 100.0 / (SELECT SUM(TotalSales) FROM SalesByRegion) AS Percentage
FROM SalesByRegion
ORDER BY TotalSales DESC;
```

** Ví dụ Recursive:**
```sql
-- Hierarchical organization structure
WITH EmployeeHierarchy AS (
    -- Anchor: CEO (no manager)
    SELECT 
        EmployeeID,
        EmployeeName,
        ManagerID,
        1 AS Level,
        CAST(EmployeeName AS NVARCHAR(MAX)) AS Path
    FROM Employees
    WHERE ManagerID IS NULL
    
    UNION ALL
    
    -- Recursive: Employees with managers
    SELECT 
        e.EmployeeID,
        e.EmployeeName,
        e.ManagerID,
        eh.Level + 1,
        eh.Path + ' -> ' + e.EmployeeName
    FROM Employees e
    JOIN EmployeeHierarchy eh ON e.ManagerID = eh.EmployeeID
)
SELECT * FROM EmployeeHierarchy ORDER BY Level, Path;
```

---

### 16. Index Rebuild vs Reorganize

**Định nghĩa:**
- **Rebuild:** Drop và tạo lại index hoàn toàn, loại bỏ fragmentation, cập nhật statistics
- **Reorganize:** Sắp xếp lại leaf-level pages in-place, ít tốn tài nguyên hơn

**So sánh:**
| Tiêu chí | Rebuild | Reorganize |
|----------|---------|------------|
| Fragmentation > 30% | Cần thiết | Không đủ |
| Resource usage | Cao | Thấp |
| Lock table | Ngắn (brief) | Không |
| Online option | Có (Enterprise) | Mặc định |
| Statistics update | Tự động | Không |

** Ví dụ:**
```sql
-- Rebuild index
ALTER INDEX IX_Orders_CustomerID ON Orders REBUILD;
ALTER INDEX ALL ON Orders REBUILD;

-- Reorganize index
ALTER INDEX IX_Orders_CustomerID ON Orders REORGANIZE;

-- Check fragmentation
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
ORDER BY ips.avg_fragmentation_in_percent DESC;
```

---

### 17. Parameter Sniffing

**Định nghĩa:** Hiện tượng khi SQL Server sử dụng execution plan đã compiled với giá trị parameter đầu tiên cho tất cả các lần gọi sau, dẫn đến performance kém với các giá trị parameter khác nhau.

** Ví dụ:**
```sql
CREATE PROCEDURE usp_GetOrdersByStatus
    @Status NVARCHAR(50)
AS
BEGIN
    -- Nếu lần đầu gọi với @Status = 'Pending' (ít rows)
    -- Plan được optimized cho ít rows
    -- Nếu gọi sau với @Status = 'All' (nhiều rows)
    -- Plan không phù hợp => Performance kém
    SELECT * FROM Orders WHERE Status = @Status;
END;
```

**Giải pháp:**
```sql
-- Solution 1: OPTION (RECOMPILE)
CREATE PROCEDURE usp_GetOrdersByStatus
    @Status NVARCHAR(50)
AS
BEGIN
    SELECT * FROM Orders WHERE Status = @Status
    OPTION (RECOMPILE); -- Luôn compile mới
END;

-- Solution 2: OPTIMIZE FOR UNKNOWN
CREATE PROCEDURE usp_GetOrdersByStatus
    @Status NVARCHAR(50)
AS
BEGIN
    SELECT * FROM Orders WHERE Status = @Status
    OPTION (OPTIMIZE FOR UNKNOWN); -- Sử dụng average statistics
END;

-- Solution 3: Local variable
CREATE PROCEDURE usp_GetOrdersByStatus
    @Status NVARCHAR(50)
AS
BEGIN
    DECLARE @LocalStatus NVARCHAR(50) = @Status;
    SELECT * FROM Orders WHERE Status = @LocalStatus;
    -- Parameter sniffing không xảy ra với local variable
END;
```

---

### 18. Query Store

**Định nghĩa:** Tính năng SQL Server 2016+ lưu trữ lịch sử execution plans và performance metrics, cho phép phân tích và khắc phục performance issues.

**Cấu hình:**
```sql
-- Kích hoạt Query Store
ALTER DATABASE MyDB SET QUERY_STORE = ON;
ALTER DATABASE MyDB SET QUERY_STORE (
    OPERATION_MODE = READ_WRITE,
    MAX_STORAGE_SIZE_MB = 1000,
    QUERY_CAPTURE_MODE = AUTO,
    WAIT_STATS_CAPTURE_MODE = ON
);

-- Các views phổ biến
-- Xem top queries by execution time
SELECT 
    q.query_id,
    qt.query_text_id,
    ROUND(rs.avg_duration / 1000.0, 2) AS avg_duration_ms,
    rs.count_executions,
    qs.query_sql_text
FROM sys.query_store_query q
JOIN sys.query_store_query_text qt ON q.query_id = qt.query_id
JOIN sys.query_store_plan p ON q.query_id = p.query_id
JOIN sys.query_store_runtime_stats rs ON p.plan_id = rs.plan_id
JOIN sys.query_store_query_text qs ON qt.query_text_id = qs.query_text_id
ORDER BY rs.avg_duration DESC;

-- Force good plan
DECLARE @plan_id BIGINT = 123; -- plan_id cần force
EXEC sp_query_store_force_plan @plan_id;
```

---

### 19. Table Variable vs Temp Table

**Định nghĩa:**
- **Table Variable:** Khai báo với @table_name, lưu trong RAM (thường), scope trong batch/procedure
- **Temp Table:** Tạo với #table_name, lưu trong tempdb, có statistics

**So sánh:**
| Tiêu chí | Table Variable | Temp Table |
|----------|----------------|------------|
| Storage | Memory (then tempdb) | tempdb |
| Statistics | Không | Có |
| Indexes | Chỉ khi PRIMARY/UNIQUE | Có thể tạo thêm |
| Size | Nhỏ (< 100 rows) | Lớn |
| Transaction | Không logged | Logged |
| Scope | Batch/Procedure | Session/Global |
| Re-compilation | Ít hơn | Có thể control |

** Ví dụ:**
```sql
-- Table Variable
DECLARE @OrderItems TABLE (
    ItemID INT PRIMARY KEY,
    ProductName NVARCHAR(100),
    Quantity INT,
    Price DECIMAL(10,2)
);

INSERT INTO @OrderItems SELECT * FROM Products;

-- Temp Table
CREATE TABLE #TempOrders (
    OrderID INT PRIMARY KEY,
    CustomerName NVARCHAR(100),
    OrderDate DATETIME
);

INSERT INTO #TempOrders SELECT OrderID, CustomerName, OrderDate 
FROM Orders WHERE OrderDate > '2024-01-01';

CREATE INDEX IX_TempOrders_Date ON #TempOrders(OrderDate);

-- Global Temp Table
CREATE TABLE ##GlobalConfig (
    ConfigKey NVARCHAR(50),
    ConfigValue NVARCHAR(MAX)
);
```

---

### 20. XEvents (Extended Events)

**Định nghĩa:** Hệ thống event handling nhẹ, scalable của SQL Server để monitor và troubleshoot performance issues, thay thế cho SQL Trace/Profiler.

** Ví dụ:**
```sql
-- Tạo session để track deadlocks
CREATE EVENT SESSION DeadlockMonitor ON SERVER
ADD EVENT sqlserver.xml_deadlock_report (
    ACTION (
        sqlserver.session_id,
        sqlserver.sql_text,
        sqlserver.database_id
    )
)
ADD TARGET package0.event_file (
    SET filename = 'C:\Temp\DeadlockTrace.xel',
        max_file_size = 10,
        max_rollover_files = 5
)
WITH (
    MAX_DISPATCH_LATENCY = 5 SECONDS,
    STARTUP_STATE = ON
);

-- Start session
ALTER EVENT SESSION DeadlockMonitor ON SERVER STATE = START;

-- Xem deadlock events
SELECT 
    event_data.value('(event/@timestamp)[1]', 'DATETIME2') AS Timestamp,
    event_data.value('(event/data/value)[1]', 'NVARCHAR(MAX)') AS DeadlockGraph
FROM sys.fn_xe_file_target_read_file(
    'C:\Temp\DeadlockTrace*.xel', 
    NULL, NULL, NULL
) WITH (event_data XML);
```
