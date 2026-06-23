---
title: "SQL Server Glossary - Từ Điển Thuật Ngữ SQL Server"
description: "Comprehensive glossary of SQL Server terminology covering database objects, T-SQL language elements, performance tuning terms, high availability concepts, and administration terminology."
tags: ["sql-server", "glossary", "terminology", "t-sql", "database", "definitions"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# SQL Server Glossary - Từ Điển Thuật Ngữ SQL Server

## Tổng Quan (Overview)

Từ điển thuật ngữ này cung cấp giải thích chi tiết về các thuật ngữ chuyên ngành được sử dụng trong SQL Server. Mỗi entry bao gồm định nghĩa, ngữ cảnh sử dụng, và các thuật ngữ liên quan để giúp người đọc hiểu sâu hơn về cách các khái niệm kết nối với nhau.

SQL Server có một hệ sinh thái phong phú với hàng trăm thuật ngữ chuyên ngành, từ basic database concepts đến advanced high availability features. Đối với những người mới bắt đầu, việc tiếp cận với tất cả các thuật ngữ này có thể gây choáng ngợp. Tài liệu này được tổ chức theo categories logic, giúp người đọc dễ dàng tìm kiếm và hiểu các thuật ngữ liên quan.

## Mục Đích (Purpose)

Từ điển này phục vụ như một tài liệu tham khảo chuẩn cho:

**Developers và DBAs**: Tra cứu nhanh các thuật ngữ khi gặp phải trong documentation, error messages, hoặc technical discussions.

**Technical Writers**: Đảm bảo sử dụng thuật ngữ nhất quán và chính xác trong technical documentation.

**Project Managers và Stakeholders**: Hiểu các thuật ngữ kỹ thuật được sử dụng trong các cuộc họp và tài liệu dự án.

## Database Objects

### ACID

**ACID** là acronym cho Atomicity, Consistency, Isolation, và Durability - bốn properties quan trọng nhất của database transactions. Atomicity đảm bảo rằng một transaction được thực thi hoàn toàn hoặc không thực thi gì cả (all-or-nothing). Consistency đảm bảo rằng database chuyển từ một valid state sang another valid state. Isolation đảm bảo rằng concurrent transactions không interfere với nhau. Durability đảm bảo rằng once a transaction commits, các changes của nó persist ngay cả khi system fails.

### Aggregate Function

**Aggregate Function** là các functions tính toán một single value từ một tập hợp values. Các aggregate functions phổ biến bao gồm COUNT, SUM, AVG, MIN, MAX, và GROUP_CONCAT. SQL Server cũng hỗ trợ window aggregate functions cho phép calculations across sets of rows related to the current row.

```sql
-- Aggregate functions example
SELECT 
    COUNT(*) AS total_orders,
    SUM(TotalAmount) AS total_revenue,
    AVG(TotalAmount) AS average_order_value,
    MIN(OrderDate) AS first_order_date,
    MAX(OrderDate) AS last_order_date
FROM Orders
WHERE OrderDate >= '2024-01-01';
```

### B-Tree

**B-Tree (Balanced Tree)** là cấu trúc dữ liệu được sử dụng bởi default row-store indexes trong SQL Server. B-Tree cung cấp efficient data retrieval với time complexity O(log n) cho search, insert, và delete operations. Tree được maintain balanced để đảm bảo performance consistent regardless of data distribution.

### Bookmark Lookup

**Bookmark Lookup** là operation xảy ra khi optimizer cần retrieve additional columns không có trong non-clustered index đã được used to locate rows. Bookmark (pointer) trong index chỉ đến vị trí của row trong clustered index hoặc heap, và lookup operation fetches row data từ vị trí đó. Bookmark lookups có thể trở thành bottleneck cho queries returning many rows.

### Cast và Convert

**CAST** và **CONVERT** là functions để convert expressions từ một data type sang another. CAST là ANSI SQL standard syntax, trong khi CONVERT là T-SQL specific với additional functionality như formatting options for dates và numbers.

```sql
-- CAST example
SELECT CAST(Price AS VARCHAR(10)) FROM Products;

-- CONVERT example with style
SELECT CONVERT(VARCHAR(10), OrderDate, 103) AS FormattedDate  -- dd/mm/yyyy
FROM Orders;
```

### Clustered Index

**Clustered Index** sắp xếp vật lý data rows trong table theo thứ tự của index key. Mỗi table chỉ có thể có một clustered index vì data rows chỉ có thể be stored in one physical order. Thông thường, primary key được sử dụng làm clustered index, nhưng không phải lúc nào cũng vậy - sometimes a different column provides better clustering for the workload.

### CTE (Common Table Expression)

**CTE (Common Table Expression)** là một temporary named result set derived từ một simple query và có thể be referenced trong subsequent queries. CTEs improve readability của complex queries và support recursive queries.

```sql
-- Non-recursive CTE
WITH HighValueOrders AS (
    SELECT CustomerID, SUM(TotalAmount) AS TotalSpent
    FROM Orders
    GROUP BY CustomerID
    HAVING SUM(TotalAmount) > 10000
)
SELECT c.CustomerName, hvo.TotalSpent
FROM HighValueOrders hvo
INNER JOIN Customers c ON hvo.CustomerID = c.CustomerID;

-- Recursive CTE for hierarchical data
WITH EmployeeHierarchy AS (
    SELECT EmployeeID, ManagerID, FirstName, 1 AS Level
    FROM Employees
    WHERE ManagerID IS NULL
    UNION ALL
    SELECT e.EmployeeID, e.ManagerID, e.FirstName, eh.Level + 1
    FROM Employees e
    INNER JOIN EmployeeHierarchy eh ON e.ManagerID = eh.EmployeeID
)
SELECT * FROM EmployeeHierarchy;
```

### Cursor

**Cursor** là database object cho phép developers process rows one at a time thay vì operating on entire result sets. SQL Server supports multiple cursor types: static, dynamic, forward-only, và keyset-driven. While cursors provide row-level control, they are generally slower than set-based operations và should be avoided unless absolutely necessary.

```sql
DECLARE @CustomerID INT;
DECLARE customer_cursor CURSOR FOR
    SELECT CustomerID FROM Customers WHERE Region = 'North';

OPEN customer_cursor;
FETCH NEXT FROM customer_cursor INTO @CustomerID;

WHILE @@FETCH_STATUS = 0
BEGIN
    -- Process each customer
    EXEC ProcessCustomerOrders @CustomerID;
    FETCH NEXT FROM customer_cursor INTO @CustomerID;
END;

CLOSE customer_cursor;
DEALLOCATE cursor_name;
```

### Data File

**Data File** là physical file trên disk chứa database data. Primary data file có extension .mdf và chứa system tables và startup information. Secondary data files có extension .ndf và are optional, used for distributing data across multiple disks.

### Database Snapshot

**Database Snapshot** là một read-only, static view của database tại một point in time. Snapshots are useful for reporting scenarios và providing a consistent view for queries without impacting source database.

```sql
-- Create database snapshot
CREATE DATABASE SalesSnapshot ON (
    NAME = SalesData,
    FILENAME = 'D:\Snapshots\SalesSnapshot.ss'
) AS SNAPSHOT OF SalesDB;

-- Query from snapshot
SELECT * FROM SalesSnapshot.dbo.Orders WHERE OrderDate > '2024-01-01';
```

### Deadlock

**Deadlock** xảy ra khi two hoặc more processes each hold a lock on a resource và wait for the other process to release its lock. SQL Server automatically detects deadlocks và terminates one of the transactions (deadlock victim) to break the cycle. Deadlocks có thể được minimize bằng cách accessing tables in consistent order across transactions.

### Dirty Read

**Dirty Read** là tình trạng đọc được data đã được modified bởi một transaction chưa commit. Điều này có thể xảy ra khi using READ UNCOMMITTED isolation level. Dirty reads có thể lead to incorrect business decisions nếu the modifying transaction rolls back.

### Execution Plan

**Execution Plan** là roadmap mô tả cách SQL Server sẽ execute một query. Plans show sequence of operations (operators) như scans, seeks, joins, sorts, và aggregations, cùng với estimated row counts và costs. Actual execution plans include runtime statistics như actual row counts và execution times.

```sql
-- View estimated execution plan
SET SHOWPLAN_TEXT ON;
SELECT * FROM Orders WHERE CustomerID = 100;
SET SHOWPLAN_TEXT OFF;

-- View actual execution plan with runtime info
SET STATISTICS PROFILE ON;
SELECT * FROM Orders WHERE CustomerID = 100;
SET STATISTICS PROFILE OFF;
```

### Fill Factor

**Fill Factor** là configuration xác định mức độ filled of index pages khi index được created hoặc rebuilt. Default là 0 (100%), có nghĩa pages được filled đầy. Lower fill factors create pages với more free space, reducing page splits during inserts nhưng using more storage.

```sql
-- Create index with fill factor
CREATE NONCLUSTERED INDEX IX_Orders_Customer_Date
ON Orders(CustomerID, OrderDate)
WITH (FILLFACTOR = 80);
```

### Foreign Key

**Foreign Key** là constraint establishes referential integrity giữa two tables. A foreign key in child table references primary key (hoặc unique key) của parent table, ensuring that values in child table must match existing values in parent table.

### Full-Text Search

**Full-Text Search** là capability cho phép searching text columns based on meaning và word matching, không chỉ exact phrase matches. Full-text search supports features như word stemming, thesaurus lookups, và proximity searches.

```sql
-- Create full-text index
CREATE FULLTEXT CATALOG ftCatalog AS DEFAULT;
CREATE FULLTEXT INDEX ON Products(ProductName, Description)
KEY INDEX PK_Products_ProductID;

-- Search using full-text predicates
SELECT ProductName, Description
FROM Products
WHERE CONTAINS((ProductName, Description), 'laptop OR notebook');
```

### Heap

**Heap** là table không có clustered index. Data rows được stored không có specific order, và SQL Server uses IAM pages để locate data within heap. Heaps are generally less efficient for retrieval operations nhưng can be faster for pure INSERT workloads without range queries.

### Index

**Index** là cấu trúc database giúp speed up data retrieval. Indexes được tạo trên columns thường được used in WHERE clauses, JOIN conditions, và ORDER BY clauses. SQL Server supports multiple index types: clustered, non-clustered, filtered, covering, columnstore, và full-text indexes.

### Isolation Level

**Isolation Level** xác định visibility của uncommitted changes giữa concurrent transactions. SQL Server supports: READ UNCOMMITTED, READ COMMITTED (default), READ COMMITTED SNAPSHOT, REPEATABLE READ, SNAPSHOT, và SERIALIZABLE.

### JOIN

**JOIN** là operation kết hợp rows từ two hoặc more tables dựa trên related columns. Các loại JOINs bao gồm: INNER JOIN (only matching rows), LEFT JOIN (all rows from left table), RIGHT JOIN (all rows from right table), FULL JOIN (all rows from both tables), và CROSS JOIN (cartesian product).

```sql
-- Various JOIN types
SELECT o.OrderID, c.CustomerName
FROM Orders o
INNER JOIN Customers c ON o.CustomerID = c.CustomerID;

SELECT c.CustomerName, o.OrderID
FROM Customers c
LEFT JOIN Orders o ON c.CustomerID = o.CustomerID;

SELECT c1.CustomerName AS Customer1, c2.CustomerName AS Customer2
FROM Customers c1
CROSS JOIN Customers c2
WHERE c1.CustomerID < c2.CustomerID;
```

### Keyset Cursor

**Keyset Cursor** là cursor type trong đó visibility of rows được determined tại thời điểm cursor được opened. Rows added after opening không visible, nhưng rows deleted become visible as empty. Keyset cursors are useful when you need to see changes made by other users but don't need real-time updates.

### Log File

**Log File** (.ldf) chứa transaction log records. Every database change được recorded trong log file trước khi applied to data files (write-ahead logging). Log file là critical cho crash recovery và point-in-time recovery.

### Lock

**Lock** là mechanism used by SQL Server's concurrency control để prevent conflicting operations between transactions. Locks được acquired on resources như rows, pages, tables, và databases. SQL Server automatically determines appropriate lock granularity based on operation type.

### Materialized View

Trong SQL Server, **Materialized Views** được implement thông qua indexed views (views với clustered index). Data được physically stored và maintained, providing fast access for complex aggregations.

### MERGE Statement

**MERGE** statement combines INSERT, UPDATE, và DELETE operations into a single statement, allowing you to synchronize two tables based on a condition.

```sql
MERGE TargetTable AS t
USING SourceTable AS s
ON t.ID = s.ID
WHEN MATCHED THEN
    UPDATE SET t.Value = s.Value
WHEN NOT MATCHED BY TARGET THEN
    INSERT (ID, Value) VALUES (s.ID, s.Value)
WHEN NOT MATCHED BY SOURCE THEN
    DELETE;
```

### NOLOCK

**NOLOCK** (READ UNCOMMITTED) là table hint cho phép query read rows đang được modified bởi other transactions without waiting for locks. While this reduces blocking, it can result in dirty reads và should be used judiciously.

### Normalization

**Normalization** là process of organizing data into tables according to rules (normal forms) để eliminate redundancy và improve data integrity. Các normal forms: 1NF (atomic values), 2NF (no partial dependencies), 3NF (no transitive dependencies), BCNF, 4NF, và 5NF.

### NULL

**NULL** represents missing or unknown data. NULL is not zero, empty string, hoặc any other value - it literally means "unknown". Operations involving NULLs typically return NULL, which is important to consider in WHERE clauses và aggregations.

```sql
-- NULL handling
SELECT 
    ISNULL(ColumnName, 'N/A') AS SafeColumn,  -- Replace NULL
    NULLIF(Value, 0) AS SafeValue,  -- Return NULL if equals second param
    COALESCE(A, B, C) AS FirstNonNull  -- Return first non-NULL value
FROM TableName;
```

### PIVOT và UNPIVOT

**PIVOT** transforms rows into columns (aggregation across categories), trong khi **UNPIVOT** transforms columns into rows (normalization).

```sql
-- PIVOT example
SELECT CustomerID, [2022], [2023], [2024]
FROM (
    SELECT CustomerID, Year, TotalAmount
    FROM Orders
) AS SourceTable
PIVOT (
    SUM(TotalAmount)
    FOR Year IN ([2022], [2023], [2024])
) AS PivotTable;
```

### Query Store

**Query Store** là feature captures query execution plans và performance metrics over time, allowing you to analyze query performance trends và force specific plans.

```sql
-- Enable Query Store
ALTER DATABASE YourDatabase SET QUERY_STORE = ON;
ALTER DATABASE YourDatabase SET QUERY_STORE (OPERATION_MODE = READ_WRITE);

-- Find expensive queries
SELECT 
    qsq.query_id,
    qsq.query_text_id,
    qrs.count_executions,
    qrs.avg_duration,
    qrs.avg_cpu_time,
    qsq.query_sql_text
FROM sys.query_store_query qsq
JOIN sys.query_store_query_stats qrs ON qsq.query_id = qrs.query_id
ORDER BY qrs.avg_duration DESC;
```

### RANK, DENSE_RANK, ROW_NUMBER

**Ranking Functions** assign ordinal values to rows based on ORDER BY clause. ROW_NUMBER assigns unique sequential numbers, RANK assigns same rank for ties with gaps, và DENSE_RANK assigns same rank for ties without gaps.

```sql
SELECT 
    CustomerName,
    TotalSpent,
    ROW_NUMBER() OVER (ORDER BY TotalSpent DESC) AS RowNum,
    RANK() OVER (ORDER BY TotalSpent DESC) AS Rank,
    DENSE_RANK() OVER (ORDER BY TotalSpent DESC) AS DenseRank,
    NTILE(4) OVER (ORDER BY TotalSpent DESC) AS Quartile
FROM (
    SELECT c.CustomerName, SUM(o.TotalAmount) AS TotalSpent
    FROM Customers c
    JOIN Orders o ON c.CustomerID = o.CustomerID
    GROUP BY c.CustomerName
) AS CustomerSales;
```

### Recovery Model

**Recovery Model** determines how transaction log records are maintained và whether point-in-time recovery is possible. Three models: FULL (complete logging, supports point-in-time), BULK_LOGGED (minimal logging for bulk operations), và SIMPLE (no log backups, minimal logging).

### Replication

**Replication** là set of technologies for copying và distributing data và database objects from one database to another, synchronizing consistency between databases. Types: Snapshot, Transactional, Merge, và Peer-to-Peer replication.

### Scalar Function

**Scalar Function** là user-defined function trả về single value. Scalar functions có thể be used in SELECT, WHERE, và other expressions. Important: scalar functions are executed once per row, which can cause performance issues.

### SARGable

**SARGable** (Search ARGument ABLE) mô tả predicates có thể utilize indexes for efficient searching. Non-sargable predicates include functions on indexed columns, leading wildcards, và type mismatches.

### Schema

**Schema** là container for database objects, providing namespace organization. Default schema là dbo. Schemas help with security (permissions at schema level) và logical organization of objects.

### Snapshot Isolation

**Snapshot Isolation** là isolation level cung cấp consistent view of data as of transaction start time, without taking locks on reads. Uses row versioning để maintain consistent view.

### SQL Server Agent

**SQL Server Agent** là Windows service for scheduling và executing administrative tasks (jobs). Supports job scheduling, alerting, và automation of maintenance tasks.

### Statistics

**Statistics** là objects chứa metadata về data distribution in columns và indexes. Optimizer uses statistics to estimate row counts và choose efficient execution plans.

### Stored Procedure

**Stored Procedure** là precompiled collection of T-SQL statements stored under a name và processed as a unit. Benefits include network traffic reduction, plan caching, và security (permissions on procedure instead of underlying tables).

### Table Variable

**Table Variable** là variable type holding a temporary table, similar to temp table nhưng with some differences in scope và behavior. Table variables are useful for small datasets và in stored procedures.

```sql
DECLARE @OrderSummary TABLE (
    OrderID INT PRIMARY KEY,
    CustomerName NVARCHAR(100),
    TotalAmount DECIMAL(10,2)
);

INSERT INTO @OrderSummary
SELECT o.OrderID, c.CustomerName, o.TotalAmount
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID;

SELECT * FROM @OrderSummary;
```

### Temp Table

**Temp Table** là temporary table stored in tempdb. Supports indexes và statistics, unlike table variables. Two types: local (#TableName) visible only in current session, và global (##TableName) visible across sessions.

```sql
CREATE TABLE #TempResults (
    ID INT PRIMARY KEY,
    Value VARCHAR(50)
);

INSERT INTO #TempResults VALUES (1, 'First');
INSERT INTO #TempResults VALUES (2, 'Second');

SELECT * FROM #TempResults;

DROP TABLE #TempResults;
```

### Transaction

**Transaction** là unit of work包含 một or more database operations that must be processed together. Transactions follow ACID properties và are controlled with BEGIN TRANSACTION, COMMIT, và ROLLBACK statements.

```sql
BEGIN TRY
    BEGIN TRANSACTION;
    
    INSERT INTO Orders (CustomerID, OrderDate, TotalAmount)
    VALUES (1, GETDATE(), 100.00);
    
    INSERT INTO OrderDetails (OrderID, ProductID, Quantity)
    VALUES (@@IDENTITY, 1, 5);
    
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
    THROW;
END CATCH;
```

### Trigger

**Trigger** là special type of stored procedure automatically executed in response to DML events (INSERT, UPDATE, DELETE) hoặc DDL events. Triggers are useful for enforcing business rules và maintaining audit trails.

```sql
CREATE TRIGGER TR_Orders_AfterInsert
ON Orders
AFTER INSERT
AS
BEGIN
    INSERT INTO AuditLog (Action, TableName, RecordID, ChangedBy, ChangeDate)
    SELECT 'INSERT', 'Orders', OrderID, SYSTEM_USER, GETDATE()
    FROM inserted;
END;
```

### UDT (User-Defined Type)

**User-Defined Type** là custom data type created from existing SQL Server data types. Can include validation rules. CLR types can be created using .NET assemblies.

### View

**View** là virtual table based on the result of a stored query. Views can simplify complex queries, restrict data access, và provide security layer.

```sql
CREATE VIEW vw_CustomerOrders AS
SELECT 
    c.CustomerID,
    c.CustomerName,
    c.Email,
    COUNT(o.OrderID) AS OrderCount,
    ISNULL(SUM(o.TotalAmount), 0) AS TotalSpent
FROM Customers c
LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID, c.CustomerName, c.Email;
```

### Window Function

**Window Functions** perform calculations across sets of rows related to the current row, without collapsing groups like GROUP BY. Include RANK, LEAD, LAG, SUM OVER, AVG OVER, và nhiều functions khác.

```sql
-- Compare each order to customer's average
SELECT 
    o.OrderID,
    o.CustomerID,
    o.TotalAmount,
    AVG(o.TotalAmount) OVER (PARTITION BY o.CustomerID) AS CustomerAvg,
    o.TotalAmount - AVG(o.TotalAmount) OVER (PARTITION BY o.CustomerID) AS DiffFromAvg
FROM Orders o;

-- Running total
SELECT 
    OrderDate,
    TotalAmount,
    SUM(TotalAmount) OVER (ORDER BY OrderDate ROWS UNBOUNDED PRECEDING) AS RunningTotal
FROM Orders;
```

## Performance Terms

### Actual Execution Plan

**Actual Execution Plan** là execution plan collected during query execution, containing runtime statistics như actual row counts, execution times, và memory grants. More accurate than estimated plan but requires executing the query.

### Estimated Execution Plan

**Estimated Execution Plan** là plan generated by optimizer without executing query. Provides estimated costs và row counts based on statistics, useful for troubleshooting without running potentially expensive queries.

### Index Seek

**Index Seek** là efficient operation using index navigation to find specific rows. Preferred over scans for selective queries.

### Index Scan

**Index Scan** là operation reading entire index sequentially. May be appropriate when large percentage of rows are needed.

### Logical Read

**Logical Read** là access to a page in buffer pool. Logical reads don't necessarily require physical I/O if page is cached.

### Physical Read

**Physical Read** là access to pages from disk. Indicates cache miss và contributes to I/O latency.

### Table Scan

**Table Scan** là operation reading entire table sequentially. Usually indicates missing index hoặc inefficient query design.

### Wait Statistics

**Wait Statistics** show what resources SQL Server is waiting on during execution. Useful for identifying bottlenecks.

```sql
-- Top wait types
SELECT TOP 10
    wait_type,
    waiting_tasks_count,
    wait_time_ms,
    signal_wait_time_ms
FROM sys.dm_os_wait_stats
WHERE wait_time_ms > 0
ORDER BY wait_time_ms DESC;
```

## High Availability Terms

### AG (Availability Group)

**Availability Group** là feature cung cấp HA/DR protection bằng cách replicating databases across multiple SQL Server instances with automatic failover.

### Automatic Failover

**Automatic Failover** là process where secondary replica automatically becomes primary without manual intervention when primary fails.

### Failover Cluster Instance

**FCI** là HA solution protecting entire SQL Server instance, requiring shared storage between cluster nodes.

### Listener

**Availability Group Listener** là virtual network name (VNN) allowing clients to connect to availability group without knowing which replica is primary.

### Log Shipping

**Log Shipping** là DR solution using transaction log backups to keep secondary database synchronized.

### Manual Failover

**Manual Failover** là planned failover initiated by administrator, allowing maintenance without downtime.

### Primary Replica

**Primary Replica** là replica that hosts read-write copy of databases in an availability group.

### RPO (Recovery Point Objective)

**RPO** là maximum acceptable data loss measured in time. Determines backup frequency requirements.

### RTO (Recovery Time Objective)

**RTO** là maximum acceptable downtime. Determines acceptable failover and recovery time.

### Secondary Replica

**Secondary Replica** là replica hosting read-only copy of databases. Can also accept backups.

### Synchronous Commit

**Synchronous Commit** là availability mode requiring log records to be hardened on secondary before commit completes on primary. Guarantees zero data loss.

### Asynchronous Commit

**Asynchronous Commit** là availability mode allowing commit before log is hardened on secondary. Lower latency but potential data loss.

## Administration Terms

### Database Engine

**Database Engine** là core service responsible for storing, processing, và securing data.

### Dedicated Administrator Connection (DAC)

**DAC** là special connection allowing administrative access when all regular connections are blocked.

### Dynamic Management View (DMV)

**DMV** là view exposing server state information for monitoring và troubleshooting.

### Instance

**Instance** là installation of SQL Server database engine. Multiple instances can run on same server, each with its own databases và configuration.

### Max Degree of Parallelism (MAXDOP)

**MAXDOP** là configuration controlling maximum number of processors used for parallel query execution.

### Query Store

**Query Store** là feature capturing query plans và runtime statistics for analysis và troubleshooting.

### Resource Governor

**Resource Governor** là feature allowing you to manage workloads và resource allocation.

### Service Broker

**Service Broker** là native messaging và queuing technology within SQL Server.

### SQL Server Configuration Manager

**SQL Server Configuration Manager** là tool for managing SQL Server services, network protocols, và configuration settings.

## References

- SQL Server Documentation: https://docs.microsoft.com/en-us/sql/sql-server/
- T-SQL Reference: https://docs.microsoft.com/en-us/sql/t-sql/language-reference
- Database Engine: https://docs.microsoft.com/en-us/sql/relational-databases/
