# SQL Server Anti-Patterns - Các Mẫu Cần Tránh

## Giới thiệu

Tài liệu này liệt kê các anti-patterns phổ biến trong SQL Server development, giải thích tại sao chúng gây vấn đề và cung cấp giải pháp thay thế tốt hơn.

---

## 1. Database Design Anti-Patterns

### 1.1. "One Size Fits All" Database

**Mô tả:** Sử dụng cùng một database cho cả OLTP và OLAP workloads.

**Vấn đề:**
```sql
-- Một bảng phục vụ cả transaction và reporting
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATETIME,
    TotalAmount DECIMAL(18,2),
    OrderDetails XML,  -- Chi tiết đơn hàng lưu dạng XML
    ShippingAddress NVARCHAR(MAX),  -- Address lớn
    InternalNotes NVARCHAR(MAX),    -- Notes cho staff
    CustomerEmail NVARCHAR(256),    -- Email copy
    ProductHistory JSON              -- Lịch sử sản phẩm
);

-- Problem: Bảng quá rộng, không có partitioning
-- Index quá nhiều để cover tất cả queries
-- Write performance bị ảnh hưởng bởi indexes phục vụ reads
-- Storage tăng không cần thiết
```

**Giải pháp:**
```sql
-- Tách biệt OLTP và OLAP
-- OLTP Database: Transactional, normalized
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    OrderDate DATETIME2(0) NOT NULL,
    TotalAmount DECIMAL(10,2) NOT NULL,
    ShippingAddressID INT NOT NULL
    -- Chỉ lưu foreign keys, không lưu redundant data
);

-- OLAP Database: Analytical, denormalized
CREATE TABLE FactOrders (
    OrderKey BIGINT IDENTITY PRIMARY KEY,
    OrderID INT NOT NULL,
    CustomerKey INT NOT NULL,
    DateKey INT NOT NULL,
    ProductKey INT NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    Quantity INT NOT NULL
);

CREATE TABLE DimDate (
    DateKey INT PRIMARY KEY,
    FullDate DATE NOT NULL,
    Year INT NOT NULL,
    Quarter INT NOT NULL,
    Month INT NOT NULL,
    DayOfWeek INT NOT NULL
);

-- Sử dụng Linked Server hoặc ETL để sync data
```

### 1.2. Entity-Attribute-Value (EAV) Pattern

**Mô tả:** Lưu trữ dynamic attributes bằng cách sử dụng rows thay vì columns.

**Vấn đề:**
```sql
-- EAV pattern cho products với dynamic attributes
CREATE TABLE ProductAttributes (
    ProductID INT NOT NULL,
    AttributeName NVARCHAR(100) NOT NULL,
    AttributeValue NVARCHAR(MAX) NOT NULL,
    PRIMARY KEY (ProductID, AttributeName)
);

-- Khi cần truy vấn products có specific attributes:
SELECT DISTINCT p.ProductID
FROM Products p
JOIN ProductAttributes pa1 ON p.ProductID = pa1.ProductID
JOIN ProductAttributes pa2 ON p.ProductID = pa2.ProductID
JOIN ProductAttributes pa3 ON p.ProductID = pa3.ProductID
WHERE pa1.AttributeName = 'Color' AND pa1.AttributeValue = 'Red'
  AND pa2.AttributeName = 'Size' AND pa2.AttributeValue = 'Large'
  AND pa3.AttributeName = 'Material' AND pa3.AttributeValue = 'Cotton';

-- Problem: 
-- - Phải self-join nhiều lần
-- - Không thể tạo proper indexes
-- - Type safety không tồn tại
-- - Query phức tạp và chậm
-- - Không thể enforce constraints
```

**Giải pháp:**
```sql
-- Solution 1: Sparse columns (SQL Server 2008+)
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName NVARCHAR(200) NOT NULL,
    Price DECIMAL(10,2),
    -- Sparse columns for optional attributes
    Color NVARCHAR(50) SPARSE NULL,
    Size NVARCHAR(20) SPARSE NULL,
    Material NVARCHAR(50) SPARSE NULL,
    Weight DECIMAL(8,2) SPARSE NULL,
    WarrantyMonths INT SPARSE NULL,
    CustomAttr1 NVARCHAR(MAX) SPARSE NULL,
    CustomAttr2 NVARCHAR(MAX) SPARSE NULL,
    CustomAttr3 NVARCHAR(MAX) SPARSE NULL
);
-- NULL values không tốn storage (sparse columns)

-- Solution 2: Separate tables cho attribute groups
CREATE TABLE ProductColors (
    ProductID INT PRIMARY KEY REFERENCES Products(ProductID),
    Color NVARCHAR(50) NOT NULL
);

CREATE TABLE ProductSizes (
    ProductID INT PRIMARY KEY REFERENCES Products(ProductID),
    Size NVARCHAR(20) NOT NULL
);

CREATE TABLE ProductMaterials (
    ProductID INT PRIMARY KEY REFERENCES Products(ProductID),
    Material NVARCHAR(50) NOT NULL
);

-- Solution 3: JSON columns (SQL Server 2016+)
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName NVARCHAR(200) NOT NULL,
    Price DECIMAL(10,2),
    Attributes JSON -- Store dynamic attributes
);

INSERT INTO Products VALUES (1, 'T-Shirt', 29.99, 
    '{"color": "Red", "size": "Large", "material": "Cotton", "weight": 200}');

-- Query JSON
SELECT * FROM Products
WHERE JSON_VALUE(Attributes, '$.color') = 'Red'
  AND JSON_VALUE(Attributes, '$.size') = 'Large';

-- Index trên JSON path
CREATE INDEX IX_Products_Color 
ON Products((JSON_VALUE(Attributes, '$.color')));
```

---

## 2. Query Anti-Patterns

### 2.1. "SELECT *" Everywhere

**Mô tả:** Sử dụng SELECT * thay vì chỉ định columns cần thiết.

**Vấn đề:**
```sql
-- Bad practice
CREATE PROCEDURE usp_GetOrderDetails
    @OrderID INT
AS
BEGIN
    SELECT * FROM Orders WHERE OrderID = @OrderID;
    -- Returns all columns including potentially large TEXT/IMAGE
    -- Cannot utilize covering indexes
    -- More network bandwidth used
    -- Column order changes break dependent code
END;

-- Another bad pattern: Implicit column list
SELECT * INTO #TempTable FROM LargeTable;
-- #TempTable không có indexes, không có primary key
-- Dữ liệu có thể rất lớn
```

**Giải pháp:**
```sql
-- Good practice: Chỉ định columns cần thiết
CREATE PROCEDURE usp_GetOrderDetails
    @OrderID INT
AS
BEGIN
    SELECT 
        OrderID,
        OrderDate,
        CustomerID,
        TotalAmount,
        Status
    FROM Orders 
    WHERE OrderID = @OrderID;
END;

-- Good practice: Covering index for the query
CREATE INDEX IX_Orders_OrderID_Covering
ON Orders(OrderID)
INCLUDE (OrderDate, CustomerID, TotalAmount, Status);

-- Khi cần copy structure
SELECT TOP 0 * INTO #TempTable FROM Orders;
-- Hoặc explicit column list
SELECT 
    OrderID,
    OrderDate,
    CustomerID,
    TotalAmount,
    Status
INTO #TempTable
FROM Orders
WHERE 1 = 0;
```

### 2.2. Implicit Type Conversion

**Mô tả:** So sánh columns với different data types, gây ra conversion và không thể sử dụng index.

**Vấn đề:**
```sql
-- Column là INT nhưng parameter là VARCHAR
CREATE PROCEDURE usp_GetCustomerOrders
    @CustomerID VARCHAR(50)  -- VARCHAR instead of INT
AS
BEGIN
    SELECT * FROM Orders 
    WHERE CustomerID = @CustomerID;
    -- CustomerID is INT, @CustomerID is VARCHAR
    -- SQL Server converts CustomerID to VARCHAR for comparison
    -- Index on CustomerID cannot be used!
END;

-- Another common issue: VARCHAR comparison with different collation
SELECT * FROM Customers 
WHERE Email = 'test@example.com';
-- Nếu Email column có different collation,
-- implicit conversion xảy ra

-- String comparison with numbers
SELECT * FROM Products 
WHERE Price = '29.99';  -- Price is DECIMAL, '29.99' is string
```

**Giải pháp:**
```sql
-- Solution: Match data types
CREATE PROCEDURE usp_GetCustomerOrders
    @CustomerID INT  -- Match the column type
AS
BEGIN
    SELECT * FROM Orders 
    WHERE CustomerID = @CustomerID;
END;

-- Solution: Explicit conversion in query
SELECT * FROM Products 
WHERE Price = CAST('29.99' AS DECIMAL(10,2));

-- Solution: Use NVARCHAR for Unicode strings
DECLARE @Name NVARCHAR(100) = N'Nguyễn Văn A';
SELECT * FROM Customers WHERE CustomerName = @Name;

-- Check for implicit conversions
SELECT 
    OBJECT_NAME(ps.object_id) AS TableName,
    ps.index_id,
    ps.equality_columns,
    ps.inequality_columns,
    ps.included_columns,
    pc.name AS column_name,
    t.name AS data_type,
    cc.text AS comparison_text
FROM sys.dm_exec_missing_stats ps
CROSS APPLY sys.dm_exec_sql_text(ps.sql_handle) cc
JOIN sys.columns pc ON pc.object_id = ps.object_id 
    AND pc.column_id = ps.column_id
JOIN sys.types t ON t.user_type_id = pc.user_type_id;
```

### 2.3. Non-Sargable Queries

**Mô tả:** Viết query không thể utilize index (Non-SARGable = Non-Search Argument Able).

**Vấn đề:**
```sql
-- Function on indexed column
SELECT * FROM Orders 
WHERE YEAR(OrderDate) = 2024;
-- Cannot use index on OrderDate

-- Function on indexed column
SELECT * FROM Customers 
WHERE LOWER(Email) = 'test@example.com';
-- Cannot use index on Email

-- Leading wildcard
SELECT * FROM Customers 
WHERE Email LIKE '%@gmail.com';
-- Cannot use index (starts with wildcard)

-- Calculation on column
SELECT * FROM Orders 
WHERE TotalAmount * 1.1 > 1000;
-- Cannot use index on TotalAmount

-- IN with subquery returning many rows
SELECT * FROM Products 
WHERE ProductID IN (SELECT ProductID FROM DiscontinuedProducts);
-- Có thể efficient hoặc không tùy vào execution plan
```

**Giải pháp:**
```sql
-- Solution: Range predicate
SELECT * FROM Orders 
WHERE OrderDate >= '2024-01-01' 
  AND OrderDate < '2025-01-01';

-- Solution: Function-based index (computed column)
ALTER TABLE Orders
ADD YearOfOrder AS YEAR(OrderDate) PERSISTED;

CREATE INDEX IX_Orders_Year ON Orders(YearOfOrder);

SELECT * FROM Orders WHERE YearOfOrder = 2024;
-- Index on computed column được sử dụng

-- Solution: Case-insensitive collation
-- Khi tạo table, chọn collation case-insensitive
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    Email NVARCHAR(256) COLLATE DATABASE_DEFAULT,
    CustomerName NVARCHAR(200) COLLATE Vietnamese_CI_AI
);
-- CI = Case Insensitive, AI = Accent Insensitive

-- Query sẽ không cần LOWER()
SELECT * FROM Customers 
WHERE Email = 'Test@Example.com';

-- Solution: Sử dụng EXISTS thay vì IN
SELECT * FROM Products p
WHERE EXISTS (
    SELECT 1 FROM DiscontinuedProducts d 
    WHERE d.ProductID = p.ProductID
);

-- Solution: Thay đổi logic cho wildcard
-- Bad: Leading wildcard
SELECT * FROM Customers WHERE Email LIKE '%@gmail.com';

-- Good: Full-text search
CREATE FULLTEXT INDEX ON Customers(Email) 
KEY INDEX PK_Customers;
-- Sau đó:
SELECT * FROM Customers 
WHERE CONTAINS(Email, '@gmail.com');
```

---

## 3. Transaction Anti-Patterns

### 3.1. Long-Running Transactions

**Mô tả:** Transactions chạy quá lâu, giữ locks và blocking other operations.

**Vấn đề:**
```sql
-- Bad: Transaction với user interaction
BEGIN TRANSACTION;
    UPDATE Inventory SET Quantity = Quantity - @OrderQty 
    WHERE ProductID = @ProductID;
    
    -- Gửi email confirmation (mất 5-10 giây)
    EXEC usp_SendOrderConfirmationEmail @CustomerEmail;
    
    -- Gọi external API để verify shipping
    EXEC usp_VerifyShippingRate @ZipCode;
    
    UPDATE Orders SET Status = 'Confirmed' 
    WHERE OrderID = @OrderID;
COMMIT;
-- Locks được giữ trong suốt thời gian chờ I/O

-- Another bad pattern: Cursor trong transaction
BEGIN TRANSACTION;
DECLARE order_cursor CURSOR FOR
    SELECT OrderID FROM PendingOrders;
    
OPEN order_cursor;
FETCH NEXT FROM order_cursor INTO @OrderID;

WHILE @@FETCH_STATUS = 0
BEGIN
    UPDATE Orders SET Status = 'Processing' 
    WHERE OrderID = @OrderID;
    
    -- Mỗi UPDATE giữ lock trên row
    -- Có thể mất vài phút nếu có nhiều orders
    -- Transaction không commit được
    
    FETCH NEXT FROM order_cursor INTO @OrderID;
END

CLOSE order_cursor;
DEALLOCATE order_cursor;
COMMIT;
```

**Giải pháp:**
```sql
-- Solution: Keep transaction short
CREATE PROCEDURE usp_ProcessOrder
    @OrderID INT,
    @CustomerEmail NVARCHAR(256)
AS
BEGIN
    SET XACT_ABORT ON;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Chỉ có database operations trong transaction
        UPDATE Inventory SET Quantity = Quantity - 1 
        WHERE ProductID = (SELECT ProductID FROM Orders WHERE OrderID = @OrderID);
        
        UPDATE Orders SET Status = 'Confirmed' 
        WHERE OrderID = @OrderID;
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
    
    -- Các operations không cần lock ở ngoài transaction
    BEGIN TRY
        EXEC usp_SendOrderConfirmationEmail @CustomerEmail;
    END TRY
    BEGIN CATCH
        -- Log error nhưng không ảnh hưởng transaction
        EXEC usp_LogEmailError @OrderID, ERROR_MESSAGE();
    END CATCH
END;

-- Solution: Batch processing without long transaction
CREATE PROCEDURE usp_ProcessPendingOrders
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Process trong batches nhỏ
    DECLARE @BatchSize INT = 100;
    DECLARE @ProcessedCount INT = 0;
    
    WHILE @ProcessedCount < @BatchSize
    BEGIN
        -- Lấy một batch
        SELECT TOP 100 OrderID 
        INTO #OrderBatch
        FROM PendingOrders
        WHERE Status = 'Pending'
        ORDER BY OrderDate;
        
        IF @@ROWCOUNT = 0 BREAK;
        
        -- Update không cần explicit transaction (mỗi statement tự commit)
        UPDATE o SET o.Status = 'Processing'
        FROM Orders o
        INNER JOIN #OrderBatch b ON o.OrderID = b.OrderID;
        
        -- Log
        INSERT INTO ProcessingLog (BatchDate, RowsProcessed)
        VALUES (GETDATE(), @@ROWCOUNT);
        
        -- Dừng một chút để release resources
        WAITFOR DELAY '00:00:00.100';
        
        SET @ProcessedCount = @ProcessedCount + @@ROWCOUNT;
        
        DROP TABLE #OrderBatch;
    END
END;
```

### 3.2. Missing Error Handling in Transactions

**Vấn đề:**
```sql
-- Bad: Không có error handling
BEGIN TRANSACTION;
    INSERT INTO Orders (CustomerID, TotalAmount) VALUES (1, 100);
    INSERT INTO OrderItems (OrderID, ProductID, Quantity) VALUES (@@IDENTITY, 1, 1);
COMMIT;
-- Nếu OrderItems insert thất bại (ví dụ OrderID không tồn tại)
-- Transaction vẫn committed với Order không có items!

-- Bad: Không check rowcount
BEGIN TRANSACTION;
    UPDATE Accounts SET Balance = Balance - @Amount WHERE AccountID = @FromAccount;
    -- @@ROWCOUNT không được kiểm tra!
    UPDATE Accounts SET Balance = Balance + @Amount WHERE AccountID = @ToAccount;
COMMIT;
-- Nếu FROM account không tồn tại, @@ROWCOUNT = 0
-- TO account vẫn được cộng tiền!
```

**Giải pháp:**
```sql
-- Good: Complete error handling
CREATE PROCEDURE usp_SafeTransfer
    @FromAccount INT,
    @ToAccount INT,
    @Amount DECIMAL(18,2)
AS
BEGIN
    SET XACT_ABORT ON;
    SET NOCOUNT ON;
    
    DECLARE @ErrorMessage NVARCHAR(4000);
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Kiểm tra source account exists và đủ tiền
        DECLARE @FromBalance DECIMAL(18,2);
        SELECT @FromBalance = Balance FROM Accounts WITH (UPDLOCK)
        WHERE AccountID = @FromAccount;
        
        IF @FromBalance IS NULL
        BEGIN
            SET @ErrorMessage = 'Source account does not exist: ' + CAST(@FromAccount AS NVARCHAR(20));
            RAISERROR(@ErrorMessage, 16, 1);
        END
        
        IF @FromBalance < @Amount
        BEGIN
            SET @ErrorMessage = 'Insufficient funds. Available: ' + CAST(@FromBalance AS NVARCHAR(20)) + 
                               ', Required: ' + CAST(@Amount AS NVARCHAR(20));
            RAISERROR(@ErrorMessage, 16, 1);
        END
        
        -- Kiểm tra destination account exists
        IF NOT EXISTS (SELECT 1 FROM Accounts WHERE AccountID = @ToAccount)
        BEGIN
            SET @ErrorMessage = 'Destination account does not exist: ' + CAST(@ToAccount AS NVARCHAR(20));
            RAISERROR(@ErrorMessage, 16, 1);
        END
        
        -- Trừ tiền
        UPDATE Accounts SET Balance = Balance - @Amount WHERE AccountID = @FromAccount;
        
        -- Verify row affected
        IF @@ROWCOUNT = 0
        BEGIN
            RAISERROR('Failed to debit source account', 16, 1);
        END
        
        -- Cộng tiền
        UPDATE Accounts SET Balance = Balance + @Amount WHERE AccountID = @ToAccount;
        
        IF @@ROWCOUNT = 0
        BEGIN
            RAISERROR('Failed to credit destination account', 16, 1);
        END
        
        -- Insert transaction record
        INSERT INTO Transactions (FromAccount, ToAccount, Amount, TransactionDate)
        VALUES (@FromAccount, @ToAccount, @Amount, GETDATE());
        
        COMMIT TRANSACTION;
        
        -- Return success
        SELECT 'Success' AS Result, @FromBalance - @Amount AS NewBalance;
        
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0
            ROLLBACK TRANSACTION;
        
        -- Log error
        INSERT INTO ErrorLog (ErrorNumber, ErrorMessage, ErrorProcedure, ErrorTime)
        SELECT ERROR_NUMBER(), ERROR_MESSAGE(), ERROR_PROCEDURE(), GETDATE();
        
        -- Return error
        SELECT 'Error' AS Result, ERROR_MESSAGE() AS ErrorMessage;
    END CATCH
END;
```

---

## 4. Index Anti-Patterns

### 4.1. Too Many Indexes

**Vấn đề:**
```sql
-- Bad: Tạo index cho mỗi query mà không xem xét maintenance cost
CREATE INDEX IX_Orders_CustomerID ON Orders(CustomerID);
CREATE INDEX IX_Orders_OrderDate ON Orders(OrderDate);
CREATE INDEX IX_Orders_Status ON Orders(Status);
CREATE INDEX IX_Orders_ShipDate ON Orders(ShipDate);
CREATE INDEX IX_Orders_CreatedBy ON Orders(CreatedBy);
CREATE INDEX IX_Orders_TotalAmount ON Orders(TotalAmount);
-- ... có thể có 20+ indexes trên một bảng

-- Problem:
-- INSERT/UPDATE phải cập nhật tất cả indexes
-- Storage tăng
-- Statistics có thể stale
-- optimizer có thể chọn sai index
```

**Giải pháp:**
```sql
-- Solution: Consolidate indexes with includes
CREATE INDEX IX_Orders_Composite_Covering
ON Orders(CustomerID, OrderDate)
INCLUDE (Status, TotalAmount, ShipDate, CreatedBy);

-- Solution: Use filtered indexes cho specific use cases
CREATE INDEX IX_Orders_Pending
ON Orders(OrderDate)
WHERE Status = 'Pending';

CREATE INDEX IX_Orders_ActiveCustomer
ON Orders(CustomerID)
WHERE Status IN ('Active', 'Processing');

-- Solution: Regular index review
SELECT 
    OBJECT_NAME(i.object_id) AS TableName,
    i.name AS IndexName,
    i.type_desc,
    i.is_primary_key,
    i.is_unique,
    ps.avg_fragmentation_in_percent,
    ps.page_count,
    u.user_seeks,
    u.user_scans,
    u.user_lookups,
    u.user_updates
FROM sys.indexes i
JOIN sys.dm_db_index_usage_stats u ON i.object_id = u.object_id AND i.index_id = u.index_id
LEFT JOIN sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'DETAILED') ps 
    ON i.object_id = ps.object_id AND i.index_id = ps.index_id
WHERE OBJECTPROPERTY(i.object_id, 'IsUserTable') = 1
ORDER BY u.user_seeks + u.user_scans ASC;

-- Xóa unused indexes
DROP INDEX IX_Orders_CreatedBy ON Orders;
```

### 4.2. Index on Low-Cardinality Columns

**Vấn đề:**
```sql
-- Bad: Index trên boolean hoặc low-cardinality column
CREATE INDEX IX_Orders_IsActive ON Orders(IsActive);
-- Với 99% orders là Active, index không hiệu quả
-- Optimizer sẽ chọn table scan thay vì index seek

CREATE INDEX IX_Customers_Gender ON Customers(Gender);
-- Chỉ có Male/Female, selectivity rất thấp
```

**Giải pháp:**
```sql
-- Solution: Không tạo index cho low-cardinality columns
-- Trừ khi combined với other high-selective columns

-- Solution: Nếu cần, sử dụng filtered index
CREATE INDEX IX_Orders_Inactive
ON Orders(OrderDate)
WHERE IsActive = 0;  -- Chỉ index inactive orders (rare)

-- Solution: Sử dụng filtered statistics
CREATE STATISTICS Stats_Orders_Inactive
ON Orders(OrderDate)
WHERE IsActive = 0;

-- Check cardinality
SELECT 
    c.name AS ColumnName,
    c.max_length,
    c.is_nullable,
    COUNT(DISTINCT c.name) AS DistinctCount,
    (SELECT COUNT(*) FROM Customers) AS TotalRows,
    CAST(COUNT(DISTINCT c.name) AS FLOAT) / (SELECT COUNT(*) FROM Customers) AS Selectivity
FROM sys.columns c
WHERE OBJECT_NAME(c.object_id) = 'Customers'
GROUP BY c.name;
```

---

## 5. Stored Procedure Anti-Patterns

### 5.1. Spaghetti Procedures

**Vấn đề:**
```sql
-- Bad: Một stored procedure làm mọi thứ
CREATE PROCEDURE usp_ProcessOrder
    @OrderID INT,
    @Action NVARCHAR(50)  -- 'Create', 'Update', 'Cancel', 'Ship', etc.
AS
BEGIN
    IF @Action = 'Create'
    BEGIN
        INSERT INTO Orders...;
        INSERT INTO OrderItems...;
        UPDATE Inventory...;
        INSERT INTO AuditLog...;
        EXEC usp_SendEmail...;
    END
    
    IF @Action = 'Update'
    BEGIN
        UPDATE Orders...;
        INSERT INTO OrderHistory...;
        -- Logic khác
    END
    
    IF @Action = 'Cancel'
    BEGIN
        UPDATE Orders SET Status = 'Cancelled'...;
        UPDATE Inventory...;
        INSERT INTO RefundQueue...;
        EXEC usp_ProcessRefund...;
    END
    
    -- Tiếp tục với 20+ IF statements
END;
```

**Giải pháp:**
```sql
-- Solution: Tách thành nhiều procedures
CREATE PROCEDURE usp_CreateOrder
    @CustomerID INT,
    @Items OrderItemsType READONLY
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Validate customer
        IF NOT EXISTS (SELECT 1 FROM Customers WHERE CustomerID = @CustomerID)
            RAISERROR('Invalid customer', 16, 1);
        
        -- Create order header
        DECLARE @NewOrderID INT;
        INSERT INTO Orders (CustomerID, OrderDate, Status)
        VALUES (@CustomerID, GETDATE(), 'Pending');
        SET @NewOrderID = SCOPE_IDENTITY();
        
        -- Insert order items
        INSERT INTO OrderItems (OrderID, ProductID, Quantity, Price)
        SELECT @NewOrderID, ProductID, Quantity, Price
        FROM @Items;
        
        -- Update inventory
        UPDATE i SET i.Quantity = i.Quantity - oi.Quantity
        FROM Inventory i
        INNER JOIN @Items oi ON i.ProductID = oi.ProductID;
        
        COMMIT TRANSACTION;
        
        SELECT @NewOrderID AS OrderID;
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;

CREATE PROCEDURE usp_CancelOrder
    @OrderID INT,
    @Reason NVARCHAR(500)
AS
BEGIN
    -- Cancel logic
END;

CREATE PROCEDURE usp_ShipOrder
    @OrderID INT,
    @TrackingNumber NVARCHAR(100)
AS
BEGIN
    -- Ship logic
END;

-- Sử dụng Service Layer để orchestrate
CREATE PROCEDURE usp_ProcessOrderAction
    @OrderID INT,
    @Action NVARCHAR(50),
    @Parameters NVARCHAR(MAX)  -- JSON parameters
AS
BEGIN
    IF @Action = 'Create'
        EXEC usp_CreateOrder ...;
    ELSE IF @Action = 'Cancel'
        EXEC usp_CancelOrder ...;
    ELSE IF @Action = 'Ship'
        EXEC usp_ShipOrder ...;
END;
```

### 5.2. Cursors Everywhere

**Vấn đề:**
```sql
-- Bad: Sử dụng cursor cho operations có thể làm bằng SET-based
CREATE PROCEDURE usp_UpdatePrices
    @IncreasePercent DECIMAL(5,2)
AS
BEGIN
    DECLARE @ProductID INT;
    DECLARE @CurrentPrice DECIMAL(10,2);
    
    DECLARE price_cursor CURSOR FOR
        SELECT ProductID, Price FROM Products;
    
    OPEN price_cursor;
    FETCH NEXT FROM price_cursor INTO @ProductID, @CurrentPrice;
    
    WHILE @@FETCH_STATUS = 0
    BEGIN
        UPDATE Products 
        SET Price = @CurrentPrice * (1 + @IncreasePercent / 100)
        WHERE ProductID = @ProductID;
        
        FETCH NEXT FROM price_cursor INTO @ProductID, @CurrentPrice;
    END
    
    CLOSE price_cursor;
    DEALLOCATE price_cursor;
END;
-- Với 100,000 products, procedure này có thể mất vài phút
```

**Giải pháp:**
```sql
-- Solution: SET-based operation
CREATE PROCEDURE usp_UpdatePrices
    @IncreasePercent DECIMAL(5,2)
AS
BEGIN
    UPDATE Products 
    SET Price = Price * (1 + @IncreasePercent / 100)
    WHERE IsActive = 1;
    
    -- Returns affected rows
    SELECT @@ROWCOUNT AS UpdatedRows;
END;

-- Khi cần row-by-row processing (thực sự cần)
-- Sử dụng OUTPUT clause thay vì cursor
CREATE PROCEDURE usp_ProcessAndLogUpdates
    @CategoryID INT
AS
BEGIN
    DECLARE @UpdatedProducts TABLE (
        ProductID INT,
        OldPrice DECIMAL(10,2),
        NewPrice DECIMAL(10,2)
    );
    
    UPDATE p
    SET p.Price = p.Price * 1.1,
        @UpdatedProducts = (
            SELECT ProductID, Price, p.Price * 1.1
            FROM Products
        )
    OUTPUT inserted.ProductID, deleted.Price, inserted.Price
    INTO @UpdatedProducts
    WHERE p.CategoryID = @CategoryID;
    
    -- Log vào audit table
    INSERT INTO PriceUpdateLog (ProductID, OldPrice, NewPrice, UpdateDate)
    SELECT ProductID, OldPrice, NewPrice, GETDATE()
    FROM @UpdatedProducts;
END;

-- Hoặc sử dụng WHILE với batch thay vì cursor
CREATE PROCEDURE usp_HeavyProcessing
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @BatchSize INT = 1000;
    DECLARE @MaxRowID INT, @CurrentMinID INT = 0;
    
    SELECT @MaxRowID = MAX(ProductID) FROM Products;
    
    WHILE @CurrentMinID < @MaxRowID
    BEGIN
        -- Process một batch
        UPDATE TOP (@BatchSize) Products
        SET Processed = 1, ProcessedDate = GETDATE()
        WHERE ProductID > @CurrentMinID AND Processed = 0;
        
        SET @CurrentMinID = @CurrentMinID + @BatchSize;
        
        -- Yield để reduce blocking
        CHECKPOINT;
        WAITFOR DELAY '00:00:00.050';
    END
END;
```

---

## 6. Schema Anti-Patterns

### 6.1. Mysterious Keys

**Vấn đề:**
```sql
-- Bad: GUID keys không có cluster
CREATE TABLE Orders (
    OrderID UNIQUEIDENTIFIER PRIMARY KEY,  -- Random GUID
    CustomerID UNIQUEIDENTIFIER,
    ...
);
-- Bảng trở thành heap vì không có clustered index
-- Hoặc clustered index trên random GUID gây page splits

-- Bad: Composite key quá rộng
CREATE TABLE OrderItems (
    OrderID BIGINT,
    ProductCode CHAR(20),
    WarehouseID INT,
    PRIMARY KEY (OrderID, ProductCode, WarehouseID)
    -- Key quá rộng, ảnh hưởng performance
);
```

**Giải pháp:**
```sql
-- Solution: Sử dụng sequential GUIDs
CREATE TABLE Orders (
    OrderID UNIQUEIDENTIFIER DEFAULT NEWSEQUENTIALID() PRIMARY KEY,
    CustomerID UNIQUEIDENTIFIER,
    ...
);

-- Hoặc sử dụng BIGINT identity thay vì GUID
CREATE TABLE Orders (
    OrderID BIGINT IDENTITY(1,1) PRIMARY KEY CLUSTERED,
    CustomerID INT NOT NULL,
    ...
);

-- Solution: Surrogate key nhỏ + natural key
CREATE TABLE OrderItems (
    OrderItemID BIGINT IDENTITY(1,1) PRIMARY KEY CLUSTERED,
    OrderID BIGINT NOT NULL,
    ProductID INT NOT NULL,
    WarehouseID INT NOT NULL,
    Quantity INT NOT NULL,
    UNIQUE (OrderID, ProductID, WarehouseID)  -- Natural key là unique
);

CREATE INDEX IX_OrderItems_OrderID ON OrderItems(OrderID);
```

### 6.2. Over-Normalized Design

**Vấn đề:**
```sql
-- Bad: Over-normalized - mỗi attribute một bảng
CREATE TABLE Entities (
    EntityID INT PRIMARY KEY
);

CREATE TABLE EntityNames (
    EntityID INT PRIMARY KEY REFERENCES Entities(EntityID),
    LanguageCode CHAR(2),
    Name NVARCHAR(200)
);

CREATE TABLE EntityDescriptions (
    EntityID INT PRIMARY KEY REFERENCES Entities(EntityID),
    LanguageCode CHAR(2),
    Description NVARCHAR(MAX)
);

CREATE TABLE EntityStatuses (
    EntityID INT PRIMARY KEY REFERENCES Entities(EntityID),
    StatusID INT,
    StatusName NVARCHAR(50),
    StatusColor NVARCHAR(20)
);

CREATE TABLE EntityCategories (
    EntityID INT PRIMARY KEY REFERENCES Entities(EntityID),
    CategoryID INT,
    CategoryName NVARCHAR(100)
);

-- Để lấy một entity, cần JOIN 5+ bảng
-- Performance rất kém
```

**Giải pháp:**
```sql
-- Solution: Denormalize appropriately
CREATE TABLE Entities (
    EntityID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(200) NOT NULL,           -- Denormalized
    Description NVARCHAR(MAX),              -- Denormalized
    StatusID INT NOT NULL,                   -- FK to status table
    CategoryID INT,                          -- FK to category table
    LanguageCode CHAR(2) DEFAULT 'en',
    CreatedDate DATETIME2(0) DEFAULT SYSDATETIME(),
    ModifiedDate DATETIME2(0) DEFAULT SYSDATETIME()
);

-- Chỉ tách bảng khi có lý do chính đáng
CREATE TABLE EntityDescriptions (
    EntityID INT NOT NULL,
    LanguageCode CHAR(2) NOT NULL,
    Description NVARCHAR(MAX),
    PRIMARY KEY (EntityID, LanguageCode)
);
-- Tách ra chỉ khi multilingual support thực sự cần thiết

-- Tạo index cho common queries
CREATE INDEX IX_Entities_Status ON Entities(StatusID);
CREATE INDEX IX_Entities_Category ON Entities(CategoryID);
CREATE INDEX IX_Entities_Name ON Entities(Name);
```

---

## 7. Security Anti-Patterns

### 7.1. Dynamic SQL with Concatenation

**Vấn đề:**
```sql
-- Bad: SQL Injection vulnerable
CREATE PROCEDURE usp_SearchProducts
    @SearchTerm NVARCHAR(100)
AS
BEGIN
    DECLARE @SQL NVARCHAR(500);
    SET @SQL = N'SELECT * FROM Products WHERE ProductName LIKE ''%' + @SearchTerm + N'%''';
    EXEC sp_executesql @SQL;
    -- Attacker có thể inject: ' OR 1=1 --
    -- Hoặc: '; DROP TABLE Products; --
END;

-- Bad: Insecure query construction
string query = "SELECT * FROM Users WHERE Username = '" + username + "'";
-- Attacker input: ' OR '1'='1 -> Bypass authentication
```

**Giải pháp:**
```sql
-- Good: Parameterized query
CREATE PROCEDURE usp_SearchProducts
    @SearchTerm NVARCHAR(100)
AS
BEGIN
    SELECT * FROM Products 
    WHERE ProductName LIKE '%' + @SearchTerm + '%';
    -- SQL Server tự động parameterized
END;

-- Good: sp_executesql với parameters
CREATE PROCEDURE usp_SearchProductsSecure
    @SearchTerm NVARCHAR(100)
AS
BEGIN
    DECLARE @SQL NVARCHAR(500);
    SET @SQL = N'SELECT * FROM Products WHERE ProductName LIKE @SearchTerm';
    
    EXEC sp_executesql @SQL, 
        N'@SearchTerm NVARCHAR(100)', 
        @SearchTerm = '%' + @SearchTerm + '%';
END;

-- Application: Always use parameterized queries
// C#
var query = "SELECT * FROM Users WHERE Username = @username";
var cmd = new SqlCommand(query, connection);
cmd.Parameters.AddWithValue("@username", username);
```

---

## 8. Application Anti-Patterns

### 8.1. Connection Pool Exhaustion

**Vấn đề:**
```csharp
// Bad: Connection không được close
public DataTable GetData(string query)
{
    SqlConnection conn = new SqlConnection(connectionString);
    conn.Open();
    
    SqlCommand cmd = new SqlCommand(query, conn);
    SqlDataAdapter adapter = new SqlDataAdapter(cmd);
    DataTable dt = new DataTable();
    adapter.Fill(dt);
    
    // Connection không được close!
    // Sẽ bị leak sau vài calls
    
    return dt;
}

// Bad: Connection không được dispose
public void ProcessData()
{
    SqlConnection conn = new SqlConnection(connectionString);
    conn.Open();
    // ... process ...
    if (success)
        return;  // Connection leak!
    conn.Close();
}
```

**Giải pháp:**
```csharp
// Good: Using statement ensures proper disposal
public DataTable GetData(string query)
{
    using (SqlConnection conn = new SqlConnection(connectionString))
    {
        conn.Open();
        
        using (SqlCommand cmd = new SqlCommand(query, conn))
        {
            using (SqlDataAdapter adapter = new SqlDataAdapter(cmd))
            {
                DataTable dt = new DataTable();
                adapter.Fill(dt);
                return dt;
            }
        }
    }
}

// Good: Async pattern for scalability
public async Task<DataTable> GetDataAsync(string query)
{
    using (SqlConnection conn = new SqlConnection(connectionString))
    {
        await conn.OpenAsync();
        
        using (SqlCommand cmd = new SqlCommand(query, conn))
        {
            using (SqlDataReader reader = await cmd.ExecuteReaderAsync())
            {
                DataTable dt = new DataTable();
                dt.Load(reader);
                return dt;
            }
        }
    }
}

// Good: Dapper for lightweight data access
public async Task<IEnumerable<Product>> GetProductsAsync(int categoryId)
{
    using (var conn = new SqlConnection(connectionString))
    {
        return await conn.QueryAsync<Product>(
            "SELECT * FROM Products WHERE CategoryID = @CategoryID",
            new { CategoryID = categoryId }
        );
    }
}
```

### 8.2. N+1 Query Problem

**Vấn đề:**
```csharp
// Bad: Một query chính + N queries cho mỗi row
public List<CustomerOrderSummary> GetCustomerSummaries()
{
    var customers = _context.Customers.ToList();
    var result = new List<CustomerOrderSummary>();
    
    foreach (var customer in customers)  // N queries!
    {
        var orderCount = _context.Orders
            .Count(o => o.CustomerID == customer.CustomerID);
        
        result.Add(new CustomerOrderSummary
        {
            CustomerName = customer.Name,
            OrderCount = orderCount
        });
    }
    
    return result;
}
// Với 1000 customers = 1001 queries!
```

**Giải pháp:**
```csharp
// Good: Single query với aggregation
public List<CustomerOrderSummary> GetCustomerSummaries()
{
    return _context.Customers
        .Select(c => new CustomerOrderSummary
        {
            CustomerName = c.Name,
            OrderCount = c.Orders.Count()  // Single query với JOIN
        })
        .ToList();
}

// Good: Explicit JOIN
public List<CustomerOrderSummary> GetCustomerSummaries()
{
    return _context.Customers
        .GroupJoin(_context.Orders,
            c => c.CustomerID,
            o => o.CustomerID,
            (c, orders) => new CustomerOrderSummary
            {
                CustomerName = c.Name,
                OrderCount = orders.Count()
            })
        .ToList();
}

// Good: Raw SQL khi cần
public List<CustomerOrderSummary> GetCustomerSummaries()
{
    string sql = @"
        SELECT 
            c.CustomerName,
            COUNT(o.OrderID) AS OrderCount
        FROM Customers c
        LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
        GROUP BY c.CustomerName";
    
    return _context.Database
        .SqlQuery<CustomerOrderSummary>(sql)
        .ToList();
}
```
