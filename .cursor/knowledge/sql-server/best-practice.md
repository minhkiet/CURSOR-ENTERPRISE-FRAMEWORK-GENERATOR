---
title: "SQL Server Best Practices - Thực Hành Tốt Nhất"
description: "Comprehensive guide to SQL Server best practices covering index design, query optimization, parameter sniffing, statistics maintenance, isolation levels, and security configurations for enterprise deployments."
tags: ["sql-server", "best-practices", "performance", "indexing", "query-optimization", "database", "tuning"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# SQL Server Best Practices - Thực Hành Tốt Nhất

## Tổng Quan (Overview)

SQL Server là một nền tảng cơ sở dữ liệu doanh nghiệp (enterprise database platform) được thiết kế để xử lý các workload từ small business applications đến mission-critical enterprise systems. Để tận dụng tối đa khả năng của SQL Server, developers và DBAs cần áp dụng các best practices đã được kiểm chứng qua nhiều năm.

Tài liệu này tổng hợp các best practices thiết yếu cho SQL Server, được phân loại theo các lĩnh vực quan trọng nhất: index design, query optimization, parameter sniffing, statistics maintenance, và isolation levels. Mỗi best practice đều đi kèm với giải thích chi tiết về lý do và cách triển khai, giúp người đọc không chỉ áp dụng một cách máy móc mà còn hiểu được nguyên lý đằng sau.

Trong môi trường enterprise, nơi mà database thường là heart của toàn bộ hệ thống, việc áp dụng best practices có thể tạo ra sự khác biệt lớn giữa một ứng dụng hoạt động trơn tru và một ứng dụng gặp phải các vấn đề về performance, scalability, và reliability. Một single misconfigured option hoặc một query không tối ưu có thể gây ra cascading failures ảnh hưởng đến toàn bộ hệ thống.

## Mục Đích (Purpose)

Mục đích của tài liệu này là cung cấp một framework tham khảo toàn diện giúp developers, database administrators (DBAs), và system architects hiểu và áp dụng các best practices của SQL Server một cách nhất quán. Tài liệu được thiết kế để phục vụ nhiều đối tượng:

**Developers** sẽ tìm thấy các best practices cho việc viết queries, thiết kế schemas, và xử lý dữ liệu hiệu quả. Các ví dụ code cụ thể giúp developers áp dụng ngay vào công việc hàng ngày.

**DBAs** sẽ được hướng dẫn về các configurations và maintenance tasks cần thiết để giữ hệ thống hoạt động ở peak performance. Bao gồm các scripts cho monitoring, alerting, và automated maintenance.

**System Architects** sẽ có được cái nhìn tổng quan về các design patterns và architectural decisions tốt nhất cho SQL Server, từ đó đưa ra các quyết định thiết kế phù hợp với requirements của hệ thống.

## Key Concepts

### 1. Index Design Principles

Index design là một trong những yếu tố quan trọng nhất ảnh hưởng đến query performance. Một index được thiết kế tốt có thể giảm thời gian execution của query từ hàng phút xuống còn mili giây, trong khi một index không phù hợp có thể gây lãng phí tài nguyên và thậm chí làm chậm performance.

**Clustered vs Non-Clustered Indexes**: Hiểu rõ sự khác biệt và khi nào nên sử dụng mỗi loại là fundamental:

Clustered indexes sắp xếp vật lý dữ liệu trong table theo thứ tự của index key. Mỗi table chỉ có thể có một clustered index vì dữ liệu chỉ có thể được sắp xếp theo một thứ tự vật lý duy nhất. Clustered index phù hợp nhất cho các columns thường được truy cập theo ranges (ví dụ: OrderDate BETWEEN '2024-01-01' AND '2024-01-31') hoặc các columns có high selectivity được sử dụng trong ORDER BY clauses.

Non-clustered indexes là các cấu trúc riêng biệt chứa các index key values cùng với pointers đến vị trí của dữ liệu trong clustered index. Một table có thể có nhiều non-clustered indexes, và chúng đặc biệt hữu ích cho các columns thường được sử dụng trong WHERE clauses nhưng không phù hợp làm clustered index.

```sql
-- Example: E-commerce database with Orders and OrderDetails tables

-- Create clustered index on OrderID (primary key, natural ordering)
-- This is optimal because:
-- 1. Primary keys should typically be clustered
-- 2. OrderDetails references Orders by OrderID, so ordering by OrderID
--    makes JOIN operations efficient
CREATE CLUSTERED INDEX IX_Orders_OrderID ON Orders(OrderID);

-- Create clustered index on composite primary key
CREATE CLUSTERED INDEX IX_OrderDetails_Composite 
ON OrderDetails(OrderID, LineNumber);

-- Create non-clustered indexes for common query patterns
-- Covering index for customer lookup by email
CREATE NONCLUSTERED INDEX IX_Customers_Email 
ON Customers(Email) 
INCLUDE (FirstName, LastName, Phone);

-- Covering index for order search by customer and date
CREATE NONCLUSTERED INDEX IX_Orders_Customer_Date 
ON Orders(CustomerID, OrderDate) 
INCLUDE (TotalAmount, Status);

-- Columnstore index for analytical queries
CREATE NONCLUSTERED COLUMNSTORE INDEX IX_Orders_Analytics 
ON Orders(OrderDate, CustomerID, TotalAmount, Status);
```

**Index Selectivity**: Selectivity là tỷ lệ unique values trong một column. Columns có high selectivity (nhiều unique values) là candidates tốt cho indexes, trong khi columns có low selectivity (ít unique values) thường không benefit từ indexing:

```sql
-- High selectivity: Almost every row is unique
-- Good candidate for index
CREATE INDEX IX_Orders_OrderID ON Orders(OrderID);  -- ~100% selectivity

-- Low selectivity: Only a few distinct values
-- Index may not be beneficial unless using included columns
CREATE INDEX IX_Orders_Status ON Orders(Status);  -- ~4 values (Pending, Shipped, etc.)
-- Consider: Only useful if filtered with other high-selective conditions
```

**Fill Factor**: Fill factor xác định mức độ filled of pages khi index được created hoặc rebuilt. Giá trị mặc định là 0 (tương đương 100%), có nghĩa là pages được fill đầy. Giảm fill factor tạo ra more empty space trên mỗi page, cho phép more updates trước khi page split xảy ra:

```sql
-- For tables with frequent inserts, use lower fill factor
-- This example: 80% fill factor, 20% free space for inserts
CREATE INDEX IX_Orders_OrderDate 
ON Orders(OrderDate) 
WITH (FILLFACTOR = 80);

-- Monitor page splits to determine appropriate fill factor
SELECT 
    object_name(ps.object_id) AS table_name,
    ps.page_type,
    ps.page_type_desc,
    ps.number_of_pages,
    ps.avg_page_space_used_in_percent
FROM sys.dm_db_index_physical_stats(
    DB_ID(), 
    OBJECT_ID('Orders'), 
    NULL, 
    NULL, 
    'DETAILED') ps
WHERE ps.alloc_unit_type_desc = 'IN_ROW_DATA';
```

### 2. Query Optimization Strategies

Query optimization là quá trình cải thiện performance của các câu queries thông qua việc viết lại queries, thêm indexes, hoặc thay đổi execution plans. SQL Server query optimizer là một component phức tạp tự động chọn execution plan tốt nhất cho mỗi query, nhưng đôi khi nó cần assistance từ developers.

**Understanding Execution Plans**: Execution plan mô tả cách SQL Server sẽ thực thi một query. Analyzing plans là kỹ năng essential cho việc tối ưu hóa:

```sql
-- Enable actual execution plan in SSMS or use these SET options
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

-- Run your query here
SELECT 
    o.OrderID,
    c.CustomerName,
    o.OrderDate,
    od.ProductID,
    p.ProductName,
    od.Quantity,
    od.Price
FROM Orders o
INNER JOIN Customers c ON o.CustomerID = c.CustomerID
INNER JOIN OrderDetails od ON o.OrderID = od.OrderID
INNER JOIN Products p ON od.ProductID = p.ProductID
WHERE o.OrderDate >= '2024-01-01'
    AND c.Region = 'North'
ORDER BY o.OrderDate DESC;

-- Key operators to look for:
-- Table Scan: Bad - reading entire table
-- Index Scan: Acceptable - reading entire index
-- Index Seek: Good - using index efficiently
-- Bookmark Lookup: Warning - may need covering index
-- Nested Loop Join: Good for small tables
-- Hash Match Join: Good for large tables
-- Merge Join: Good when inputs are sorted
```

**Join Optimization**: Thứ tự JOIN và loại JOIN operator có thể ảnh hưởng lớn đến performance:

```sql
-- Principle: Start with smallest tables and filter early
-- BAD: Large tables joined without filtering
SELECT * 
FROM LargeTransactions t
INNER JOIN Customers c ON t.CustomerID = c.CustomerID;

-- GOOD: Apply filters early, join smaller filtered sets
SELECT t.TransactionID, c.CustomerName, t.Amount
FROM (
    SELECT * FROM Transactions 
    WHERE TransactionDate >= '2024-01-01'
) t
INNER JOIN (
    SELECT CustomerID, CustomerName 
    FROM Customers 
    WHERE Region = 'North'
) c ON t.CustomerID = c.CustomerID;

-- Use EXISTS instead of IN for better performance with subqueries
-- GOOD: EXISTS can short-circuit once match is found
SELECT c.CustomerID, c.CustomerName
FROM Customers c
WHERE EXISTS (
    SELECT 1 
    FROM Orders o 
    WHERE o.CustomerID = c.CustomerID 
    AND o.OrderDate >= '2024-01-01'
);

-- BAD: IN must evaluate all subquery results first
SELECT c.CustomerID, c.CustomerName
FROM Customers c
WHERE c.CustomerID IN (
    SELECT o.CustomerID 
    FROM Orders o 
    WHERE o.OrderDate >= '2024-01-01'
);
```

### 3. Parameter Sniffing

Parameter sniffing là quá trình SQL Server optimizer "sniffs" giá trị parameters khi một stored procedure được compiled và sử dụng giá trị đó để tạo execution plan. Plan được tạo dựa trên parameter value cụ thể có thể không optimal cho các parameter values khác.

Vấn đề xảy ra khi cached plan được reuse cho các calls với different parameter values có different data distribution:

```sql
-- Stored procedure with parameter sniffing issue
CREATE PROCEDURE GetOrdersByCustomer
    @CustomerID INT
AS
BEGIN
    SELECT OrderID, OrderDate, TotalAmount
    FROM Orders
    WHERE CustomerID = @CustomerID
    ORDER BY OrderDate DESC;
END;

-- Scenario: 
-- Call 1: @CustomerID = 1 (has 5 orders) - fast, uses index seek
-- Call 2: @CustomerID = 2 (has 500,000 orders) - slow, same plan used

-- Solutions:

-- Solution 1: OPTIMIZE FOR UNKNOWN
CREATE PROCEDURE GetOrdersByCustomer_Optimized
    @CustomerID INT
AS
BEGIN
    SELECT OrderID, OrderDate, TotalAmount
    FROM Orders
    WHERE CustomerID = @CustomerID
    ORDER BY OrderDate DESC
    OPTION (OPTIMIZE FOR UNKNOWN);
END;

-- Solution 2: OPTIMIZE FOR specific value
CREATE PROCEDURE GetOrdersByCustomer_Average
    @CustomerID INT
AS
BEGIN
    SELECT OrderID, OrderDate, TotalAmount
    FROM Orders
    WHERE CustomerID = @CustomerID
    ORDER BY OrderDate DESC
    OPTION (OPTIMIZE FOR (@CustomerID = 0));
END;

-- Solution 3: Use OPTION (RECOMPILE) when parameters vary widely
CREATE PROCEDURE GetOrdersByCustomer_Recompile
    @CustomerID INT
AS
BEGIN
    SELECT OrderID, OrderDate, TotalAmount
    FROM Orders
    WHERE CustomerID = @CustomerID
    ORDER BY OrderDate DESC
    OPTION (RECOMPILE);
END;

-- Solution 4: Use plan guide for specific parameter values
-- (Advanced, rarely needed in modern SQL Server)
```

**Detecting Parameter Sniffing Issues**:

```sql
-- Compare statistics for different parameter values
-- Look for large variance in row estimates vs actual rows
SELECT 
    qs.execution_count,
    qs.total_elapsed_time / qs.execution_count AS avg_elapsed_time_ms,
    qs.total_logical_reads / qs.execution_count AS avg_logical_reads,
    SUBSTRING(qt.text, qs.statement_start_offset / 2 + 1,
        (CASE qs.statement_end_offset
          WHEN -1 THEN DATALENGTH(qt.text)
          ELSE qs.statement_end_offset
         END - qs.statement_start_offset) / 2 + 1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
WHERE qt.text LIKE '%GetOrdersByCustomer%'
ORDER BY qs.total_elapsed_time DESC;
```

### 4. Statistics Maintenance

Statistics là metadata về distribution of data trong indexes và columns. SQL Server query optimizer sử dụng statistics để estimate row counts và chọn optimal execution plans. Out-of-date statistics có thể dẫn đến suboptimal plans.

```sql
-- Check when statistics were last updated
SELECT 
    object_name(s.object_id) AS table_name,
    s.name AS statistics_name,
    STATS_DATE(s.object_id, s.stats_id) AS last_updated,
    s.auto_created,
    s.user_created,
    s.no_recompute
FROM sys.stats s
WHERE objectproperty(s.object_id, 'IsUserTable') = 1
ORDER BY STATS_DATE(s.object_id, s.stats_id);

-- Update statistics manually
UPDATE STATISTICS Orders IX_Orders_Customer_Date;

-- Update all statistics for a table
UPDATE STATISTICS Orders WITH ALL;

-- Update statistics with FULLSCAN for better accuracy
UPDATE STATISTICS Orders IX_Orders_Customer_Date WITH FULLSCAN;

-- Automated statistics maintenance
-- SQL Server automatically updates statistics when:
-- 1. Table size changes from 0 to non-zero rows
-- 2. 20% of rows change (small tables) or
-- 3. 20% + 500 rows change (large tables)
-- Configure auto-update behavior:
ALTER DATABASE YourDatabase SET AUTO_UPDATE_STATISTICS ON;
ALTER DATABASE YourDatabase SET AUTO_UPDATE_STATISTICS_ASYNC ON;
```

### 5. Isolation Levels

Isolation levels xác định mức độ visibility của uncommitted changes giữa các concurrent transactions. Higher isolation levels cung cấp better consistency nhưng có thể gây ra blocking và concurrency issues.

```sql
-- Default isolation level: READ COMMITTED
-- Allows dirty reads prevention but may have non-repeatable reads

-- READ UNCOMMITTED: Allows dirty reads, minimal locking
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SELECT * FROM Orders WHERE CustomerID = 1;  -- May read uncommitted data

-- READ COMMITTED (default): Prevents dirty reads
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT * FROM Orders WHERE CustomerID = 1;  -- Only reads committed data

-- READ COMMITTED SNAPSHOT (RCSI): Read-committed without blocking
-- Requires database-level setting
ALTER DATABASE YourDatabase SET READ_COMMITTED_SNAPSHOT ON;
-- Now reads don't block writers, writers don't block readers

-- REPEATABLE READ: Prevents non-repeatable reads
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- Holds shared locks until transaction ends
-- May cause more blocking than READ COMMITTED

-- SNAPSHOT: Provides consistent view as of transaction start
SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
BEGIN TRANSACTION;
    -- All reads in this transaction see data as of transaction start
    SELECT * FROM Orders WHERE CustomerID = 1;
COMMIT TRANSACTION;

-- SERIALIZABLE: Highest isolation, prevents phantom reads
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Places range locks on queried ranges
-- Can cause severe blocking issues
```

**Choosing the Right Isolation Level**:

| Isolation Level | Dirty Reads | Non-Repeatable Reads | Phantom Reads | Blocking |
|----------------|-------------|---------------------|---------------|----------|
| READ UNCOMMITTED | Yes | Yes | Yes | Minimal |
| READ COMMITTED | No | Yes | Yes | Moderate |
| READ COMMITTED SNAPSHOT | No | Yes | Yes | Low |
| REPEATABLE READ | No | No | Yes | High |
| SNAPSHOT | No | No | No | Low |
| SERIALIZABLE | No | No | No | Very High |

## Best Practices Summary

### Index Design

- **Primary Keys**: Thường nên là clustered index, sử dụng sequential keys (IDENTITY) để tránh page splits
- **Foreign Keys**: Index trên foreign key columns để cải thiện JOIN performance
- **Covering Indexes**: Include all columns needed by frequently executed queries
- **Column Order**: Đặt high-selective columns first trong composite indexes
- **Monitor and Maintain**: Regular index rebuilds/reorganizes based on fragmentation

### Query Writing

- **Avoid SELECT ***: Chỉ select columns actually needed
- **Use SET-based operations**: Tránh cursors và row-by-row processing
- **Parameterize queries**: Use stored procedures hoặc parameterized queries
- **Test with actual data volumes**: Execution plans may differ with data size

### Security Configuration

```sql
-- Use contained database authentication
ALTER DATABASE YourDatabase SET containment = partial;
CREATE USER YourUser WITH PASSWORD = 'StrongPassword123!';

-- Implement principle of least privilege
-- Create application roles with specific permissions
CREATE APPLICATION ROLE AppRole_Documents 
WITH PASSWORD = 'AppRolePassword123!';
GRANT SELECT, INSERT, UPDATE ON SCHEMA::Documents TO AppRole_Documents;
DENY DELETE ON SCHEMA::Documents TO AppRole_Documents;

-- Enable encrypted connections
-- Configure in SQL Server Configuration Manager:
-- 1. Enable Force Encryption = Yes
-- 2. Specify certificate
-- 3. Restart SQL Server

-- Use Always Encrypted for sensitive data
CREATE TABLE Customers (
    CustomerID INT IDENTITY PRIMARY KEY,
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    SSN CHAR(11) COLLATE Latin1_General_BIN2 
        ENCRYPTED WITH (COLUMN_ENCRYPTION_KEY = SSN_CEK,
                       ENCRYPTION_TYPE = Deterministic,
                       ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256')
);
```

### Backup Strategy

```sql
-- Full backup (daily at minimum)
BACKUP DATABASE YourDatabase 
TO DISK = 'D:\Backups\YourDatabase_Full.bak'
WITH COMPRESSION, CHECKSUM, STATS = 10;

-- Transaction log backup (every 15-30 minutes for RPO)
BACKUP LOG YourDatabase 
TO DISK = 'D:\Backups\YourDatabase_Log.trn'
WITH COMPRESSION, CHECKSUM, STATS = 10;

-- Differential backup (every 4-6 hours between full backups)
BACKUP DATABASE YourDatabase 
TO DISK = 'D:\Backups\YourDatabase_Diff.bak'
WITH DIFFERENTIAL, COMPRESSION, CHECKSUM, STATS = 10;

-- Test restore regularly
RESTORE VERIFYONLY FROM DISK = 'D:\Backups\YourDatabase_Full.bak';
```

## Troubleshooting

### Performance Troubleshooting Query

```sql
-- Find top 50 queries by total execution time
SELECT TOP 50
    qs.execution_count AS exec_count,
    qs.total_elapsed_time / 1000 AS total_elapsed_ms,
    qs.total_elapsed_time / (qs.execution_count * 1000) AS avg_elapsed_ms,
    qs.total_logical_reads / qs.execution_count AS avg_logical_reads,
    qs.total_physical_reads / qs.execution_count AS avg_physical_reads,
    qs.total_worker_time / 1000 AS total_cpu_ms,
    qp.query_plan,
    SUBSTRING(st.text, 1, 500) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) st
CROSS APPLY sys.dm_exec_query_plan(qs.plan_handle) qp
WHERE qs.execution_count > 10
ORDER BY qs.total_elapsed_time DESC;

-- Find queries with missing indexes
SELECT 
    migs.avg_user_impact AS impact_pct,
    migs.user_seeks,
    migs.user_scans,
    mid.statement AS table_name,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns,
    migs.avg_total_user_cost AS avg_cost
FROM sys.dm_db_missing_index_details mid
JOIN sys.dm_db_missing_index_groups mig ON mid.index_handle = mig.index_handle
JOIN sys.dm_db_missing_index_group_stats migs 
    ON mig.index_group_handle = migs.group_handle
WHERE migs.avg_user_impact > 30
ORDER BY migs.avg_user_impact DESC;

-- Check for blocking chains
SELECT 
    blocked.session_id AS blocked_session,
    blocked_wait_type,
    blocked_text.text AS blocked_query,
    blocker.session_id AS blocker_session,
    blocker_wait_type AS blocker_wait_type,
    blocker_text.text AS blocker_query,
    blocked_req.wait_resource
FROM sys.dm_exec_requests blocked
CROSS APPLY sys.dm_exec_sql_text(blocked.sql_handle) blocked_text
JOIN sys.dm_exec_sessions blocker ON blocked.blocking_session_id = blocker.session_id
OUTER APPLY sys.dm_exec_sql_text(blocker.sql_handle) blocker_text
LEFT JOIN sys.dm_exec_requests blocked_req 
    ON blocked.session_id = blocked_req.session_id
WHERE blocked.blocking_session_id > 0;
```

## Examples

### Example 1: Comprehensive Index Strategy for OLTP

```sql
-- Create tables for e-commerce workload
CREATE TABLE Products (
    ProductID INT IDENTITY(1,1) PRIMARY KEY,
    ProductName NVARCHAR(200) NOT NULL,
    CategoryID INT NOT NULL,
    SupplierID INT NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,
    UnitsInStock INT NOT NULL,
    UnitsOnOrder INT NOT NULL,
    Discontinued BIT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    ModifiedDate DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    CONSTRAINT FK_Products_Categories FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID),
    CONSTRAINT FK_Products_Suppliers FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);

CREATE NONCLUSTERED INDEX IX_Products_Category 
ON Products(CategoryID);

CREATE NONCLUSTERED INDEX IX_Products_Supplier 
ON Products(SupplierID);

-- Covering index for category browsing
CREATE NONCLUSTERED INDEX IX_Products_Category_Covering 
ON Products(CategoryID, Discontinued) 
INCLUDE (ProductName, UnitPrice, UnitsInStock);

-- Columnstore for analytics
CREATE NONCLUSTERED COLUMNSTORE INDEX IX_Products_Analytics 
ON Products(CategoryID, SupplierID, UnitPrice, UnitsInStock, UnitsOnOrder);

-- For products by name search (e-commerce often needs this)
CREATE NONCLUSTERED INDEX IX_Products_Name 
ON Products(ProductName) 
INCLUDE (ProductID, UnitPrice, UnitsInStock)
WHERE Discontinued = 0;

-- Full-text index for product search
CREATE FULLTEXT CATALOG ProductSearch AS DEFAULT;
CREATE FULLTEXT INDEX ON Products(ProductName) 
KEY INDEX PK_Products_ProductID 
ON ProductSearch;
```

### Example 2: Optimizing a Complex Report Query

```sql
-- BEFORE: Unoptimized report query
CREATE PROCEDURE rpt_SalesSummary_Unoptimized
    @StartDate DATETIME,
    @EndDate DATETIME,
    @Region VARCHAR(50)
AS
BEGIN
    SELECT 
        YEAR(o.OrderDate) AS Year,
        MONTH(o.OrderDate) AS Month,
        c.Region,
        c.CustomerName,
        p.ProductName,
        SUM(od.Quantity) AS TotalQuantity,
        SUM(od.Quantity * od.Price) AS TotalSales
    FROM Orders o
    INNER JOIN Customers c ON o.CustomerID = c.CustomerID
    INNER JOIN OrderDetails od ON o.OrderID = od.OrderID
    INNER JOIN Products p ON od.ProductID = p.ProductID
    WHERE o.OrderDate BETWEEN @StartDate AND @EndDate
        AND c.Region = @Region
    GROUP BY 
        YEAR(o.OrderDate),
        MONTH(o.OrderDate),
        c.Region,
        c.CustomerName,
        p.ProductName
    ORDER BY Year, Month, TotalSales DESC;
END;

-- AFTER: Optimized with proper indexes and query structure
CREATE PROCEDURE rpt_SalesSummary_Optimized
    @StartDate DATETIME,
    @EndDate DATETIME,
    @Region VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Use table variables to stage filtered data
    DECLARE @StartDateInternal DATETIME = @StartDate;
    DECLARE @EndDateInternal DATETIME = @EndDate;
    
    -- Use OPTION (RECOMPILE) if parameters vary significantly
    SELECT 
        YEAR(o.OrderDate) AS Year,
        MONTH(o.OrderDate) AS Month,
        c.Region,
        c.CustomerName,
        p.ProductName,
        SUM(od.Quantity) AS TotalQuantity,
        SUM(od.Quantity * od.Price) AS TotalSales
    FROM Orders o
    INNER JOIN Customers c ON o.CustomerID = c.CustomerID
    INNER JOIN OrderDetails od ON o.OrderID = od.OrderID
    INNER JOIN Products p ON od.ProductID = p.ProductID
    WHERE o.OrderDate >= @StartDateInternal
        AND o.OrderDate < DATEADD(DAY, 1, @EndDateInternal)
        AND c.Region = @Region
    GROUP BY 
        YEAR(o.OrderDate),
        MONTH(o.OrderDate),
        c.Region,
        c.CustomerName,
        p.ProductName
    ORDER BY Year, Month, TotalSales DESC
    OPTION (HASH GROUP, RECOMPILE);  -- Hint for better aggregation
END;

-- Recommended indexes for this report
CREATE NONCLUSTERED INDEX IX_Orders_Date_Customer 
ON Orders(OrderDate, CustomerID) 
INCLUDE (OrderID);

CREATE NONCLUSTERED INDEX IX_Customers_Region 
ON Customers(Region) 
INCLUDE (CustomerID, CustomerName);
```

## References

- SQL Server Documentation: https://docs.microsoft.com/en-us/sql/sql-server/
- Index Design Guide: https://docs.microsoft.com/en-us/sql/relational-databases/sql-server-index-design-guide
- Query Processing Architecture: https://docs.microsoft.com/en-us/sql/relational-databases/query-processing-architecture-guide
- Transaction Locking and Row Versioning: https://docs.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-locking-and-row-versioning-guide
- Statistics: https://docs.microsoft.com/en-us/sql/relational-databases/statistics/statistics
