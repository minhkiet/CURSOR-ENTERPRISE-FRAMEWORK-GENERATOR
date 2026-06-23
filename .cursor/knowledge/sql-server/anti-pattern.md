---
title: "SQL Server Anti-Patterns - Các Mẫu Cần Tránh"
description: "Comprehensive guide to common SQL Server anti-patterns that degrade performance, scalability, and reliability. Covers missing indexes, SELECT *, NOLOCK abuse, cursor overuse, implicit conversions, and more."
tags: ["sql-server", "anti-patterns", "performance", "database", "t-sql", "query-optimization", "indexing"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# SQL Server Anti-Patterns - Các Mẫu Thiết Kế Cần Tránh

## Tổng Quan (Overview)

Trong quá trình phát triển và vận hành SQL Server, có nhiều anti-pattern (mẫu thiết kế phản tác dụng) phổ biến mà developers và DBA thường gặp phải. Những anti-pattern này không chỉ làm giảm performance đáng kể mà còn gây ra các vấn đề về scalability, maintainability, và reliability của hệ thống. Tài liệu này sẽ đi sâu vào từng loại anti-pattern, giải thích tại sao chúng gây hại, cách nhận diện chúng trong codebase hiện tại, và đưa ra giải pháp thay thế tối ưu.

SQL Server là một relational database management system (RDBMS) mạnh mẽ từ Microsoft, được thiết kế để xử lý khối lượng công việc lớn với hiệu suất cao. Tuy nhiên, ngay cả những hệ thống mạnh mẽ nhất cũng có thể bị suy giảm nghiêm trọng khi áp dụng các mẫu thiết kế không tối ưu. Một câu query đơn giản viết sai cách có thể gây ra full table scan trên một bảng có hàng triệu rows, dẫn đến thời gian phản hồi lên đến hàng phút thay vì mili giây.

Việc hiểu và tránh các anti-pattern không chỉ là kỹ năng cần thiết cho developers mà còn là nền tảng để xây dựng các ứng dụng enterprise-grade. Trong môi trường production, nơi mà database thường là bottleneck của cả hệ thống, việc loại bỏ các anti-pattern có thể mang lại cải thiện hiệu suất gấp nhiều lần mà không cần thay đổi phần cứng hay kiến trúc hệ thống.

## Mục Đích (Purpose)

Mục đích chính của tài liệu này là cung cấp một bộ tài liệu tham khảo toàn diện giúp developers, DBAs, và system architects nhận diện và loại bỏ các anti-pattern phổ biến trong SQL Server. Thay vì chỉ liệt kê các anti-pattern một cách khô khan, tài liệu sẽ đi sâu vào cơ chế bên trong của từng vấn đề, giúp người đọc hiểu được bản chất và lý do tại sao một mẫu thiết kế cụ thể lại gây hại cho hệ thống.

Tài liệu cũng hướng đến việc trở thành một phần của kiến thức nền tảng trong framework phát triển enterprise, giúp đảm bảo rằng tất cả các thành viên trong team đều hiểu và áp dụng các best practices nhất quán. Điều này đặc biệt quan trọng trong các dự án lớn, nơi mà nhiều developers có thể làm việc trên cùng một database schema và viết các câu queries độc lập.

Ngoài ra, tài liệu cung cấp các giải pháp thay thế cụ thể với T-SQL code examples, cho phép người đọc áp dụng ngay vào dự án của mình. Mỗi giải pháp đều đi kèm với giải thích về performance benefits và trade-offs, giúp người đọc đưa ra quyết định phù hợp với yêu cầu cụ thể của hệ thống.

## Các Khái Niệm Chính (Key Concepts)

### 1. Missing Indexes - Thiếu Index

Missing index là một trong những anti-pattern phổ biến và nguy hại nhất. Khi một table không có appropriate indexes cho các câu queries thường được thực thi, SQL Server buộc phải thực hiện table scan hoặc clustered index scan, đọc toàn bộ dữ liệu để tìm kiếm kết quả mong muốn. Điều này đặc biệt tệ hại với các bảng có hàng triệu rows.

SQL Server cung cấp Dynamic Management Views (DMVs) để phát hiện missing indexes. Query sau đây liệt kê các missing indexes được SQL Server gợi ý:

```sql
SELECT 
    migs.avg_user_impact AS avg_improvement_pct,
    migs.avg_total_user_cost AS avg_cost_reduction,
    migs.user_seeks AS num_user_seeks,
    mid.statement AS table_name,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns
FROM sys.dm_db_missing_index_details mid
CROSS APPLY sys.dm_db_missing_index_groups mig
INNER JOIN sys.dm_db_missing_index_group_stats migs 
    ON mig.index_group_handle = migs.group_handle
WHERE migs.avg_user_impact > 30 
    AND migs.user_seeks > 100
ORDER BY migs.avg_user_impact DESC;
```

Tuy nhiên, không phải lúc nào cũng nên tạo index cho mọi missing index suggestion. Việc tạo quá nhiều indexes sẽ làm chậm INSERT, UPDATE, và DELETE operations vì SQL Server phải cập nhật tất cả các indexes. Thay vào đó, hãy tập trung vào các indexes có high impact (avg_user_impact cao) và được sử dụng frequently (user_seeks nhiều).

### 2. SELECT * Anti-Pattern

Sử dụng SELECT * là một trong những anti-pattern được cảnh báo nhiều nhất nhưng vẫn rất phổ biến. Có nhiều lý do khiến SELECT * gây hại:

**Network overhead**: Khi SELECT *, bạn trả về tất cả các columns bao gồm cả những columns không cần thiết. Với các bảng có nhiều large data types như VARCHAR(MAX), TEXT, hoặc BLOB, điều này có thể tăng network traffic lên gấp nhiều lần. Trong một ứng dụng web được truy cập hàng ngàn lần mỗi phút, điều này tạo ra sự khác biệt lớn về bandwidth consumption.

**Index coverage issues**: SELECT * ngăn cản việc tạo covering indexes hiệu quả. Khi bạn chỉ cần một vài columns cụ thể, bạn có thể tạo một non-clustered index bao gồm (included columns) các columns đó, cho phép SQL Server phục vụ query hoàn toàn từ index mà không cần bookmark lookup vào clustered index. Nhưng khi dùng SELECT *, covering index không còn hiệu quả.

**Application coupling**: SELECT * tạo ra sự phụ thuộc chặt chẽ giữa database schema và application code. Khi bạn thêm column mới, thay đổi thứ tự columns, hoặc đổi tên column, application code sử dụng SELECT * có thể bị break hoặc hoạt động không đúng.

```sql
-- BAD: SELECT * returns all columns including large ones
SELECT * FROM Orders;

-- GOOD: Only select needed columns
SELECT 
    OrderID, 
    CustomerID, 
    OrderDate, 
    TotalAmount 
FROM Orders;

-- GOOD: For specific use case, select only what's needed
SELECT 
    o.OrderID,
    c.CustomerName,
    o.OrderDate
FROM Orders o
INNER JOIN Customers c ON o.CustomerID = c.CustomerID;
```

### 3. NOLOCK Hint Abuse

NOLOCK (hay READ UNCOMMITTED) là một table hint cho phép query đọc dữ liệu mà không yêu cầu shared locks, từ đó giảm blocking và tăng concurrency. Tuy nhiên, việc lạm dụng NOLOCK mang lại nhiều rủi ro nghiêm trọng:

**Dirty reads**: Query với NOLOCK có thể đọc các rows đang được modified bởi các transactions khác nhưng chưa được commit. Nếu transaction kia rollback, dữ liệu bạn đọc được là không tồn tại hoặc sai lệch.

**Phantom reads**: Khi sử dụng NOLOCK, bạn có thể đọc cùng một row nhiều lần hoặc bỏ sót rows do các pages đang được reorganized bởi concurrent operations.

**Incorrect aggregation**: Khi thực hiện COUNT, SUM, AVG trên dữ liệu đang thay đổi, kết quả có thể sai lệch đáng kể.

```sql
-- BAD: NOLOCK on every table is dangerous
SELECT * 
FROM Orders WITH (NOLOCK)
INNER JOIN Customers WITH (NOLOCK) ON Orders.CustomerID = Customers.CustomerID;

-- GOOD: Let SQL Server handle locking with default isolation level
SELECT 
    o.OrderID,
    c.CustomerName,
    o.OrderDate
FROM Orders o
INNER JOIN Customers c ON o.CustomerID = c.CustomerID;
```

Nếu bạn gặp blocking issues nghiêm trọng, thay vì dùng NOLOCK, hãy xem xét:

```sql
-- Consider using READ COMMITTED SNAPSHOT (RCSI) at database level
ALTER DATABASE YourDatabase SET READ_COMMITTED_SNAPSHOT ON;

-- Or use SNAPSHOT isolation level explicitly for read-only operations
SET TRANSACTION ISOLATION LEVEL SNAPSHOT;
BEGIN TRANSACTION;
    SELECT * FROM Orders WHERE OrderDate > '2024-01-01';
COMMIT TRANSACTION;
```

### 4. Cursor Overuse

Cursors là constructs cho phép xử lý row-by-row thay vì set-based operations. Mặc dù đôi khi cần thiết, cursor overuse là một trong những nguyên nhân phổ biến nhất của performance problems trong SQL Server.

Vấn đề cốt lõi của cursors là chúng hoạt động ngược với design philosophy của relational databases. SQL Server và T-SQL được tối ưu hóa cho set-based operations, nơi mà toàn bộ operation được thực hiện trong một statement duy nhất, tận dụng parallel processing và batch operations. Khi sử dụng cursor, bạn yêu cầu SQL Server xử lý từng row một, loại bỏ hầu hết các optimizations.

```sql
-- BAD: Using cursor to update rows one by one
DECLARE @OrderID INT;
DECLARE order_cursor CURSOR FOR
    SELECT OrderID FROM Orders WHERE Status = 'Pending';

OPEN order_cursor;
FETCH NEXT FROM order_cursor INTO @OrderID;

WHILE @@FETCH_STATUS = 0
BEGIN
    UPDATE Orders 
    SET Status = 'Processed', 
        ProcessedDate = GETDATE() 
    WHERE OrderID = @OrderID;
    
    FETCH NEXT FROM order_cursor INTO @OrderID;
END;

CLOSE order_cursor;
DEALLOCATE order_cursor;

-- GOOD: Set-based update in single statement
UPDATE Orders 
SET Status = 'Processed', 
    ProcessedDate = GETDATE() 
WHERE Status = 'Pending';
```

Set-based approach có thể nhanh hơn cursor implementation gấp 100 lần hoặc hơn, đặc biệt với các bảng lớn. Lý do là cursor phải:
- Fetch mỗi row riêng lẻ (network round-trips)
- Thực hiện separate UPDATE cho mỗi row (multiple writes)
- Hold locks lâu hơn (longer transaction duration)
- Không thể parallelize (single-threaded execution)

### 5. Implicit Conversions

Implicit conversion xảy ra khi SQL Server tự động chuyển đổi data types của operands để so sánh hoặc tính toán. Điều này thường xảy ra khi bạn so sánh columns có data type này với constants hoặc parameters có data type khác.

Khi implicit conversion xảy ra, SQL Server không thể sử dụng indexes efficiently trên column bị converted. Thay vì index seek, SQL Server phải thực hiện index scan hoặc table scan để áp dụng conversion cho mỗi row.

```sql
-- BAD: Implicit conversion - CustomerID is INT but being compared to VARCHAR
DECLARE @CustomerID VARCHAR(10) = '12345';
SELECT * FROM Orders WHERE CustomerID = @CustomerID;

-- BAD: Mixing data types in comparison
SELECT * FROM Products 
WHERE Price = '19.99';  -- Price is DECIMAL but literal is string

-- GOOD: Match data types explicitly
DECLARE @CustomerID INT = 12345;
SELECT * FROM Orders WHERE CustomerID = @CustomerID;

-- GOOD: Explicit CAST/CONVERT
SELECT * FROM Products 
WHERE Price = CAST('19.99' AS DECIMAL(10,2));
```

Để phát hiện implicit conversions trong execution plans, hãy tìm kiếm "Convert" operator trong graphical plan hoặc warnings trong text plan. Query sau giúp identify implicit conversions trong cached plans:

```sql
SELECT 
    qp.query_text,
    cp.usecounts AS execution_count,
    cp.size_in_bytes / 1024 AS plan_size_kb,
    qp.query_plan
FROM sys.dm_exec_cached_plans cp
CROSS APPLY sys.dm_exec_query_plan(cp.plan_handle) qp
CROSS APPLY sys.dm_exec_sql_text(cp.plan_handle) qs
WHERE qp.query_plan.exist('declare namespace p="http://schemas.microsoft.com/sqlserver/2004/07/showplan";
                        //p:RelOp/p:Convert') = 1
ORDER BY cp.usecounts DESC;
```

### 6. Scalar Function in WHERE Clause

Đặt scalar functions trong WHERE clause là một anti-pattern subtle nhưng gây hại nghiêm trọng. Khi bạn wrap một column trong scalar function, SQL Server phải áp dụng function đó cho mỗi row trước khi có thể evaluate WHERE condition, ngăn cản index usage.

```sql
-- BAD: Function on column prevents index usage
SELECT CustomerID, OrderDate, TotalAmount
FROM Orders
WHERE YEAR(OrderDate) = 2024 AND MONTH(OrderDate) = 6;

-- GOOD: Range query can use index
SELECT CustomerID, OrderDate, TotalAmount
FROM Orders
WHERE OrderDate >= '2024-06-01' AND OrderDate < '2024-07-01';

-- BAD: String function prevents index seek
SELECT * FROM Customers WHERE LOWER(Email) = 'test@example.com';

-- GOOD: Use COLLATE or proper comparison
SELECT * FROM Customers 
WHERE Email = 'test@example.com' COLLATE Latin1_General_CI_AS;

-- If case-insensitive comparison needed, use appropriate collation
-- or create computed column with desired collation
```

### 7. Non-Sargable Patterns

SARGable (Search Argument Able) là thuật ngữ mô tả các conditions mà SQL Server có thể sử dụng index seeks. Các patterns sau là non-sargable và nên tránh:

```sql
-- BAD: Function on indexed column
SELECT * FROM Orders WHERE ABS(OrderID) = 12345;
SELECT * FROM Orders WHERE DATEADD(day, 0, OrderDate) = '2024-06-15';

-- BAD: Leading wildcard
SELECT * FROM Customers WHERE Email LIKE '%@gmail.com';

-- GOOD: Suffix wildcard can still use index
SELECT * FROM Customers WHERE Email LIKE 'john@%';

-- BAD: NOT EQUAL in most cases
SELECT * FROM Orders WHERE Status <> 'Cancelled';

-- GOOD: Restructure with positive conditions if possible
SELECT * FROM Orders WHERE Status IN ('Pending', 'Processing', 'Shipped');

-- BAD: OR on indexed column
SELECT * FROM Orders WHERE OrderID = 123 OR OrderID = 456;

-- GOOD: Use IN instead
SELECT * FROM Orders WHERE OrderID IN (123, 456);
```

## Best Practices

### 1. Index Design Best Practices

Thiết kế index hiệu quả đòi hỏi sự cân bằng giữa read performance và write overhead:

**Composite Index Column Order**: Luôn đặt columns có high selectivity (few matches) trước. Columns trong WHERE clause với equality conditions (column = value) nên đặt trước columns với range conditions (column > value).

```sql
-- For query: WHERE Status = 'Active' AND OrderDate > '2024-01-01'
-- Good index order:
CREATE INDEX IX_Orders_Status_Date ON Orders(Status, OrderDate);

-- For query: WHERE CustomerID = @custID AND OrderDate BETWEEN @start AND @end
-- Good index:
CREATE INDEX IX_Orders_Customer_Date ON Orders(CustomerID, OrderDate);
```

**Covering Indexes**: Đưa các columns thường được SELECT vào index như included columns để tránh bookmark lookups:

```sql
-- For query: SELECT OrderID, CustomerID, OrderDate FROM Orders WHERE CustomerID = @custID
CREATE INDEX IX_Orders_Customer_Covering 
ON Orders(CustomerID) 
INCLUDE (OrderID, OrderDate);
```

### 2. Query Writing Best Practices

**Avoid DISTINCT and GROUP BY unless necessary**: Chúng thường indicate design issues:

```sql
-- BAD: Using DISTINCT to hide duplicate data
SELECT DISTINCT c.CustomerID, c.CustomerName
FROM Customers c
INNER JOIN Orders o ON c.CustomerID = o.CustomerID;

-- GOOD: Use EXISTS if you only need to check existence
SELECT c.CustomerID, c.CustomerName
FROM Customers c
WHERE EXISTS (SELECT 1 FROM Orders WHERE CustomerID = c.CustomerID);
```

**Use SET-based operations**: Luôn ưu tiên set-based thay vì procedural logic:

```sql
-- BAD: Multiple round-trips to database
var customers = GetAllCustomers();
foreach (var cust in customers)
{
    if (cust.Region == "North")
    {
        UpdateCustomerStatus(cust.ID, "Preferred");
    }
}

-- GOOD: Single set-based operation
UPDATE Customers 
SET Status = 'Preferred' 
WHERE Region = 'North';
```

## Common Patterns

### Pattern 1: Pagination

```sql
-- BAD: Old-style pagination with OFFSET (SQL Server 2012+)
SELECT * FROM Orders 
ORDER BY OrderID 
OFFSET 1000000 ROWS FETCH NEXT 100 ROWS ONLY;
-- Problem: Still scans 1,000,100 rows internally

-- GOOD: Keyset pagination for better performance
SELECT TOP 100 * FROM Orders 
WHERE OrderID > @LastOrderID
ORDER BY OrderID;

-- Implementation with cursor-based pagination
CREATE PROCEDURE GetOrdersPage
    @PageSize INT = 50,
    @LastOrderID INT = 0
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT TOP (@PageSize) 
        OrderID, CustomerID, OrderDate, TotalAmount
    FROM Orders
    WHERE OrderID > @LastOrderID
    ORDER BY OrderID;
END;
```

### Pattern 2: Audit Trail

```sql
-- BAD: Using triggers for everything (triggers run synchronously)
CREATE TRIGGER TR_Orders_Update
ON Orders FOR UPDATE
AS
BEGIN
    INSERT INTO OrdersAudit (...)
    SELECT ... FROM inserted;
END;

-- GOOD: Use OUTPUT clause for simple cases
UPDATE Orders
SET Status = 'Cancelled',
    ModifiedDate = GETDATE()
OUTPUT 
    inserted.OrderID,
    deleted.Status AS OldStatus,
    inserted.Status AS NewStatus,
    GETDATE() AS ChangeDate
INTO OrdersAudit(OrderID, OldStatus, NewStatus, ChangeDate)
WHERE OrderID = @OrderID;

-- GOOD: Use Change Tracking or CDC for comprehensive audit
ALTER DATABASE YourDB SET CHANGE_TRACKING = ON
CHANGE_TRACKING_MODIFICATIONS(ON);
```

## Troubleshooting

### Identifying Performance Issues

```sql
-- Top 10 slowest queries by total execution time
SELECT TOP 10
    qs.total_elapsed_time / qs.execution_count AS avg_elapsed_time,
    qs.total_logical_reads / qs.execution_count AS avg_logical_reads,
    qs.execution_count,
    qs.total_elapsed_time,
    SUBSTRING(st.text, (qs.statement_start_offset / 2) + 1,
        ((CASE qs.statement_end_offset
          WHEN -1 THEN DATALENGTH(st.text)
          ELSE qs.statement_end_offset
         END - qs.statement_start_offset) / 2) + 1) AS query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) st
ORDER BY avg_elapsed_time DESC;

-- Queries with high logical reads (memory pressure)
SELECT TOP 20
    qs.total_logical_reads / qs.execution_count AS avg_logical_reads,
    qs.execution_count,
    SUBSTRING(st.text, 1, 200) AS query_preview
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) st
ORDER BY avg_logical_reads DESC;

-- Queries with missing index warnings
SELECT 
    qp.query_plan
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_query_plan(qs.plan_handle) qp
WHERE qp.query_plan.exist('declare namespace p="http://schemas.microsoft.com/sqlserver/2004/07/showplan";
                          //p:MissingIndexGroup') = 1;
```

## Examples

### Example 1: Converting Cursor to Set-Based

```sql
-- BEFORE: Cursor-based inventory adjustment
CREATE PROCEDURE AdjustInventory_Cursor
    @ProductID INT,
    @Adjustment INT
AS
BEGIN
    DECLARE @WarehouseID INT, @Qty INT;
    DECLARE inv_cursor CURSOR FOR
        SELECT WarehouseID, Quantity 
        FROM Inventory 
        WHERE ProductID = @ProductID;
    
    OPEN inv_cursor;
    FETCH NEXT FROM inv_cursor INTO @WarehouseID, @Qty;
    
    WHILE @@FETCH_STATUS = 0
    BEGIN
        UPDATE Inventory 
        SET Quantity = Quantity + @Adjustment
        WHERE ProductID = @ProductID AND WarehouseID = @WarehouseID;
        
        FETCH NEXT FROM inv_cursor INTO @WarehouseID, @Qty;
    END;
    
    CLOSE inv_cursor;
    DEALLOCATE inv_cursor;
END;

-- AFTER: Set-based inventory adjustment
CREATE PROCEDURE AdjustInventory_SetBased
    @ProductID INT,
    @Adjustment INT
AS
BEGIN
    UPDATE Inventory 
    SET Quantity = Quantity + @Adjustment
    WHERE ProductID = @ProductID;
END;
```

### Example 2: Proper Error Handling with Transactions

```sql
CREATE PROCEDURE ProcessOrder
    @CustomerID INT,
    @OrderData JSON
AS
BEGIN
    SET XACT_ABORT ON;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Validate customer exists
        IF NOT EXISTS (SELECT 1 FROM Customers WHERE CustomerID = @CustomerID)
        BEGIN
            THROW 50000, 'Customer not found', 1;
        END
        
        -- Insert order header
        DECLARE @OrderID INT;
        INSERT INTO Orders (CustomerID, OrderDate, Status)
        VALUES (@CustomerID, GETDATE(), 'Pending');
        SET @OrderID = SCOPE_IDENTITY();
        
        -- Insert order details from JSON
        INSERT INTO OrderDetails (OrderID, ProductID, Quantity, Price)
        SELECT 
            @OrderID,
            JSON_VALUE(value, '$.productId'),
            JSON_VALUE(value, '$.quantity'),
            JSON_VALUE(value, '$.price')
        FROM OPENJSON(@OrderData);
        
        COMMIT TRANSACTION;
        
        SELECT @OrderID AS OrderID;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();
        
        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END;
```

## References

- SQL Server Documentation: https://docs.microsoft.com/en-us/sql/sql-server/
- Performance Tuning and Optimization: https://docs.microsoft.com/en-us/sql/relational-databases/performance/tuning-and-optimizing-server-configuration
- Index Best Practices: https://docs.microsoft.com/en-us/sql/relational-databases/sql-server-index-design-guide
- Query Processing Architecture: https://docs.microsoft.com/en-us/sql/relational-databases/query-processing-architecture-guide
