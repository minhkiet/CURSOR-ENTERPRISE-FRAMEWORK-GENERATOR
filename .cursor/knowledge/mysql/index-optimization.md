---
title: Index Optimization
description: Chiến lược tối ưu hóa Index - B-tree, Composite Index, Covering Index, Index Merge, Invisible Index, Descending Index, Optimizer Hints
tags: [mysql, index, optimization, b-tree, query-performance]
created: 2026-06-23
version: 1.0.0
framework: cursor-enterprise-framework
---

# Index Optimization

## Tổng quan

Index là cấu trúc dữ liệu quan trọng nhất để tối ưu hóa hiệu suất truy vấn MySQL. Việc thiết kế và sử dụng index đúng cách có thể tăng tốc độ truy vấn từ hàng giây xuống mili giây. Tuy nhiên, index cũng có nhược điểm: chúng tiêu tốn không gian lưu trữ, làm chậm các thao tác INSERT, UPDATE, DELETE, và cần được bảo trì để đảm bảo hiệu quả.

Tài liệu này cung cấp hướng dẫn chi tiết về cách thiết kế, triển khai và duy trì các index một cách hiệu quả trong môi trường MySQL enterprise. Chúng ta sẽ đi sâu vào các loại index khác nhau, chiến lược tạo composite indexes, cách sử dụng covering indexes, và các kỹ thuật tối ưu hóa nâng cao.

## Mục đích của tài liệu

Tài liệu này được viết nhằm giúp các developer và database administrator:

- Hiểu cách MySQL sử dụng B-tree indexes và cách optimizer chọn index
- Thiết kế composite indexes tối ưu cho các truy vấn phức tạp
- Sử dụng covering indexes để loại bỏ table access
- Triển khai chiến lược index maintenance hiệu quả
- Chẩn đoán và xử lý các vấn đề liên quan đến index

## Các Khái niệm Cốt lõi

### 1. B-tree Index Structure

MySQL sử dụng B-tree (Balanced Tree) làm cấu trúc dữ liệu mặc định cho indexes. B-tree là cấu trúc dạng cây cân bằng với chiều cao tương đối ổn định, cho phép tìm kiếm với độ phức tạp O(log n) cho hầu hết các operations.

#### Cấu trúc B-tree

```
                    [50, 75]
                   /    |    \
            [25, 30]  [50, 75]  [80, 90]
               |        |         |
            Leaf     Leaf       Leaf
            Pages    Pages      Pages
```

Mỗi node trong B-tree chứa nhiều keys và pointers. Leaf nodes chứa actual data (hoặc pointer đến data) và được liên kết tuần tự, cho phép range scans hiệu quả.

```sql
-- Xem cách index được lưu trữ
SHOW CREATE TABLE orders\G

-- Phân tích index cardinality
SHOW INDEX FROM orders;

-- Sample output:
-- Table: orders
-- Non_unique: 0 (primary key)
-- Key_name: PRIMARY
-- Seq_in_index: 1
-- Column_name: id
-- Collation: A
-- Cardinality: 1500000
-- Sub_part: NULL
-- Packed: NULL
-- Null: 
-- Index_type: BTREE
```

#### Clustered vs Secondary Indexes

**Clustered Index**: 
- Dữ liệu được lưu trữ theo thứ tự của index key
- Mỗi table chỉ có một clustered index (thường là primary key)
- Truy cập row theo clustered index = direct access đến data

**Secondary Index**:
- Chứa index key và pointer đến clustered index
- Truy cập row = index lookup + bookmark lookup đến clustered index

```sql
-- Clustered index (primary key) - data stored in index order
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,  -- Clustered index
    name VARCHAR(100),
    email VARCHAR(255),
    created_at TIMESTAMP
) ENGINE=InnoDB;

-- Secondary index
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,  -- Secondary index
    order_date DATE,
    total DECIMAL(10,2),
    INDEX idx_customer_id (customer_id),  -- Secondary index
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
) ENGINE=InnoDB;

-- Khi query theo customer_id:
-- 1. Tìm customer_id trong idx_customer_id (secondary index)
-- 2. Lấy customer_id từ secondary index
-- 3. Tra cứu trong primary key để lấy full row
```

### 2. Composite Indexes

Composite index (multi-column index) là index được tạo trên nhiều columns. Thứ tự columns trong composite index rất quan trọng và ảnh hưởng đến hiệu quả sử dụng index.

#### Leftmost Prefix Principle

MySQL có thể sử dụng composite index cho các queries sử dụng leftmost prefix của index. Ví dụ, với index `(a, b, c)`:

| Query | Sử dụng Index? |
|-------|---------------|
| `WHERE a = 1` | ✅ Có (prefix a) |
| `WHERE a = 1 AND b = 2` | ✅ Có (prefix a, b) |
| `WHERE a = 1 AND b = 2 AND c = 3` | ✅ Có (full) |
| `WHERE b = 2` | ❌ Không (không có leftmost prefix) |
| `WHERE c = 3` | ❌ Không (không có leftmost prefix) |
| `WHERE b = 2 AND c = 3` | ❌ Không (không có leftmost prefix) |

```sql
-- Tạo composite index cho bảng orders
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_status VARCHAR(20) NOT NULL,
    order_date DATE NOT NULL,
    total DECIMAL(10,2),
    INDEX idx_status_date (order_status, order_date),
    INDEX idx_customer_status (customer_id, order_status)
) ENGINE=InnoDB;

-- Queries hiệu quả với idx_status_date:
SELECT * FROM orders WHERE order_status = 'completed';
SELECT * FROM orders WHERE order_status = 'completed' AND order_date = '2026-01-15';
SELECT * FROM orders WHERE order_status = 'pending' AND order_date BETWEEN '2026-01-01' AND '2026-01-31';

-- Queries KHÔNG hiệu quả (không có leftmost prefix):
SELECT * FROM orders WHERE order_date = '2026-01-15';  -- Không dùng được idx_status_date
```

#### Sắp xếp Columns trong Composite Index

Quy tắc chung khi sắp xếp columns trong composite index:

1. **Columns có cardinality cao (nhiều distinct values) đặt trước**: Giúp giảm nhanh số lượng rows cần scan
2. **Columns thường xuyên được dùng trong equality conditions đặt trước**: Vì equality lookup nhanh hơn range lookup
3. **Columns có low selectivity KHÔNG nên đặt đầu**: Ví dụ gender (chỉ có 2 values) thường không hiệu quả làm leading column

```sql
-- Ví dụ: Bảng orders với composite indexes được tối ưu

-- Index tốt cho: WHERE customer_id = ? AND order_status = ?
-- Cardinality: customer_id (high) > order_status (medium)
INDEX idx_customer_status (customer_id, order_status)

-- Index tốt cho: WHERE order_status = ? ORDER BY order_date
-- Sắp xếp: equality (status) trước, sau đó là column dùng trong ORDER BY
INDEX idx_status_date (order_status, order_date)

-- Index tốt cho: WHERE customer_id = ? AND order_status = ? AND order_date = ?
-- Sắp xếp: equality columns trước, sau đó là range column
INDEX idx_all_conditions (customer_id, order_status, order_date)
```

### 3. Covering Indexes

Covering index là index chứa TẤT CẢ các columns cần thiết để answer một query mà không cần truy cập vào table rows. Điều này loại bỏ "回表" (bookmark lookup/index lookup), giúp query chạy nhanh hơn đáng kể.

```sql
-- Tạo covering index
-- Query: SELECT order_id, customer_id, order_date FROM orders WHERE customer_id = ?

-- Index này là covering cho query trên
CREATE INDEX idx_covering ON orders (customer_id, order_id, order_date);

-- EXPLAIN cho thấy "Using index" thay vì "Using index condition"
EXPLAIN SELECT order_id, customer_id, order_date 
FROM orders 
WHERE customer_id = 100;
```

```sql
-- Ví dụ covering index cho reporting query
CREATE TABLE sales (
    sale_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    category_id INT NOT NULL,
    sale_date DATE NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    region VARCHAR(50),
    INDEX idx_category_date (category_id, sale_date),
    INDEX idx_covering_category (category_id, sale_date, quantity, unit_price)
) ENGINE=InnoDB;

-- Query này được cover hoàn toàn bởi idx_covering_category
EXPLAIN 
SELECT 
    category_id,
    sale_date,
    SUM(quantity) AS total_qty,
    SUM(quantity * unit_price) AS total_revenue
FROM sales
WHERE category_id = 5
AND sale_date BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY category_id, sale_date;
```

**Output EXPLAIN mong đợi:**
```
id: 1
select_type: SIMPLE
table: sales
type: range
possible_keys: idx_category_date, idx_covering_category
key: idx_covering_category  <-- Sử dụng covering index
key_len: 4
ref: NULL
rows: 1500
filtered: 100.00
Extra: Using where; Using index  <-- "Using index" = covering index
```

### 4. Index Merge

MySQL optimizer có thể sử dụng nhiều indexes để answer một query và merge kết quả. Index merge có thể sử dụng các chiến lược khác nhau.

#### Index Merge Types

**UNION (OR)**: Kết hợp kết quả từ nhiều index range scans
```sql
-- Ví dụ: Query với OR
SELECT * FROM orders 
WHERE order_status = 'completed' OR customer_id = 1000;

-- EXPLAIN có thể hiển thị:
-- type: index_merge
-- key: idx_status, idx_customer
-- key_len: 13, 4
-- ref: NULL
-- rows: 150, 25
-- Extra: Using union(idx_status, idx_customer); Using where
```

**INTERSECTION (AND)**: Lấy giao của nhiều index scans
```sql
SELECT * FROM orders 
WHERE customer_id = 100 AND order_status = 'completed';
-- type: index_merge
-- key: idx_customer, idx_status
-- Extra: Using intersect(idx_customer, idx_status)
```

**SORT-UNION**: Kết hợp và sort kết quả
```sql
SELECT * FROM orders 
WHERE order_date < '2026-01-01' OR order_date > '2026-12-31';
```

#### Khi nào Index Merge không hiệu quả

Index merge thường kém hiệu quả hơn composite index vì:

1. Cần scan nhiều indexes thay vì một index
2. Cần merge kết quả từ nhiều sources
3. Không tận dụng được index statistics tốt

```sql
-- Thay vì:
SELECT * FROM orders 
WHERE customer_id = 100 OR order_status = 'pending';

-- Tạo composite index có thể hiệu quả hơn
CREATE INDEX idx_customer_status ON orders (customer_id, order_status);

-- Hoặc sử dụng UNION để force separate index usage
SELECT * FROM orders WHERE customer_id = 100
UNION ALL
SELECT * FROM orders WHERE order_status = 'pending' AND customer_id <> 100;
```

### 5. Invisible Indexes

MySQL 8.0 giới thiệu invisible indexes - indexes không được optimizer sử dụng nhưng vẫn được maintain. Đây là công cụ hữu ích để test xóa index mà không cần drop và recreate.

```sql
-- Tạo index như bình thường
CREATE INDEX idx_old_index ON orders (order_status);

-- Đánh dấu là invisible
ALTER TABLE orders ALTER INDEX idx_old_index INVISIBLE;

-- Kiểm tra xem query có sử dụng index không
EXPLAIN SELECT * FROM orders WHERE order_status = 'pending';

-- Nếu performance vẫn tốt, có thể drop index
ALTER TABLE orders DROP INDEX idx_old_index;

-- Hoặc đánh dấu lại là visible nếu cần
ALTER TABLE orders ALTER INDEX idx_old_index VISIBLE;
```

```sql
-- Kiểm tra visibility của tất cả indexes
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    NON_UNIQUE,
    SEQ_IN_INDEX,
    COLUMN_NAME,
    IS_VISIBLE
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = 'your_database'
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;
```

### 6. Descending Indexes

MySQL 8.0 hỗ trợ descending indexes (ASC và DESC tự nhiên trong cùng index). Trước MySQL 8.0, index luôn được sort ASC và DESC queries phải đọc index theo chiều ngược lại.

```sql
-- Tạo descending index
CREATE INDEX idx_date_desc ON orders (order_date DESC);

-- Composite index với mixed sort order
CREATE INDEX idx_status_date ON orders (order_status ASC, order_date DESC);

-- Query với ORDER BY matching index order
SELECT * FROM orders 
WHERE order_status = 'pending'
ORDER BY order_date DESC;
-- Sử dụng index mà không cần filesort
```

```sql
-- Ví dụ thực tế cho dashboard query
CREATE TABLE metrics (
    metric_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    metric_name VARCHAR(100),
    metric_value DOUBLE,
    recorded_at TIMESTAMP,
    INDEX idx_metric_time (metric_name, recorded_at DESC)
) ENGINE=InnoDB;

-- Lấy latest values cho mỗi metric
SELECT m.*
FROM metrics m
INNER JOIN (
    SELECT metric_name, MAX(recorded_at) AS max_time
    FROM metrics
    GROUP BY metric_name
) latest ON m.metric_name = latest.metric_name 
        AND m.recorded_at = latest.max_time;
```

### 7. Optimizer Hints

Optimizer hints cho phép developer gợi ý cho MySQL optimizer cách execute query. Cần sử dụng cẩn thận vì hints có thể trở nên obsolete khi data distribution thay đổi.

```sql
-- FORCE INDEX - yêu cầu sử dụng index cụ thể
SELECT * FROM orders FORCE INDEX (idx_customer_id)
WHERE customer_id = 100;

-- USE INDEX - gợi ý sử dụng index
SELECT * FROM orders USE INDEX (idx_status_date)
WHERE order_status = 'pending';

-- IGNORE INDEX - yêu cầu bỏ qua index
SELECT * FROM orders IGNORE INDEX (idx_old_index)
WHERE order_status = 'pending';
```

```sql
-- JOIN order hints
SELECT STRAIGHT_JOIN *  -- Force join theo thứ tự trong query
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
WHERE c.region = 'North';

-- Hints cho join_buffer_size
SELECT /*+ SET_VAR(join_buffer_size = 16M) */ *
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id;
```

```sql
-- MAX_EXECUTION_TIME hint (MySQL 5.7.8+)
SELECT /*+ MAX_EXECUTION_TIME(5000) */ *
FROM orders
WHERE order_date > '2025-01-01';

-- BKA hint cho batched key access
SELECT /*+ BKA(oi) */ *
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id;
```

```sql
-- NO_ICP hint - disable Index Condition Pushdown
SELECT /*+ NO_ICP(orders) */ *
FROM orders
WHERE order_status = 'pending'
AND order_date BETWEEN '2026-01-01' AND '2026-06-30';

-- NO_MRR hint - disable Multi-Range Read
SELECT /*+ NO_MRR(orders) */ *
FROM orders
WHERE customer_id IN (1, 2, 3, 4, 5);
```

## Các Best Practices

### 1. Index Design Guidelines

```sql
-- Quy tắc 1: Chỉ index các columns thực sự cần thiết
-- BAD: Index trên TẤT CẢ columns
CREATE INDEX idx_all ON orders (order_id, customer_id, order_status, order_date, total);

-- GOOD: Chỉ index columns được sử dụng trong WHERE, JOIN, ORDER BY
CREATE INDEX idx_lookup ON orders (customer_id, order_date);

-- Quy tắc 2: Sử dụng appropriate data types
-- BAD: VARCHAR cho numeric IDs
CREATE INDEX idx_bad ON orders (status_string);  -- VARCHAR

-- GOOD: ENUM hoặc TINYINT cho limited values
ALTER TABLE orders MODIFY status TINYINT;
CREATE INDEX idx_good ON orders (status);  -- TINYINT, nhỏ hơn, nhanh hơn

-- Quy tắc 3: Consider prefix indexes cho long VARCHAR columns
CREATE INDEX idx_email_prefix ON customers (email(50));

-- Quy tắc 4: Index foreign keys
-- Nếu có FOREIGN KEY, indexes trên referenced columns là bắt buộc
ALTER TABLE orders ADD FOREIGN KEY (customer_id) REFERENCES customers(id);
-- InnoDB tự động tạo index trên customer_id
```

### 2. Index Maintenance

```sql
-- Phân tích index statistics
ANALYZE TABLE orders;

-- Kiểm tra index usage
SELECT 
    OBJECT_SCHEMA,
    OBJECT_NAME,
    INDEX_NAME,
    COUNT_STAR,
    COUNT_READ,
    COUNT_WRITE,
    SUM_TIMER_WAIT
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE OBJECT_SCHEMA = 'your_database'
ORDER BY COUNT_STAR DESC;

-- Tìm unused indexes
SELECT 
    OBJECT_SCHEMA,
    OBJECT_NAME,
    INDEX_NAME
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE OBJECT_SCHEMA = 'your_database'
AND INDEX_NAME IS NOT NULL
AND COUNT_READ = 0
AND INDEX_NAME != 'PRIMARY';
```

```sql
-- Script để identify unused indexes
DELIMITER //

CREATE PROCEDURE find_unused_indexes()
BEGIN
    SELECT 
        t.TABLE_NAME,
        s.INDEX_NAME,
        s.COLUMN_NAME,
        s.SEQ_IN_INDEX,
        s.CARDINALITY,
        t.TABLE_ROWS,
        ROUND(s.CARDINALITY / t.TABLE_ROWS * 100, 2) AS selectivity_pct
    FROM information_schema.STATISTICS s
    JOIN information_schema.TABLES t 
        ON s.TABLE_SCHEMA = t.TABLE_SCHEMA 
        AND s.TABLE_NAME = t.TABLE_NAME
    WHERE s.TABLE_SCHEMA = DATABASE()
    AND s.NON_UNIQUE = 1  -- Non-primary indexes
    ORDER BY t.TABLE_NAME, s.INDEX_NAME, s.SEQ_IN_INDEX;
END //

DELIMITER ;

CALL find_unused_indexes();
```

### 3. Query Optimization Patterns

```sql
-- Pattern 1: Sử dụng covering index cho frequently executed queries
CREATE INDEX idx_order_lookup 
ON orders (customer_id, order_status, order_date, order_id, total);

-- Pattern 2: Composite index cho range + ORDER BY
CREATE INDEX idx_date_status 
ON orders (order_date DESC, order_status);

SELECT * FROM orders 
WHERE order_date >= '2026-01-01'
ORDER BY order_date DESC, order_status;

-- Pattern 3: Index cho LIKE with prefix wildcard
-- LIKE 'value%' có thể sử dụng index
-- LIKE '%value%' KHÔNG thể sử dụng index
CREATE INDEX idx_name ON customers (name);  -- Cho LIKE 'John%'
-- Sử dụng FULLTEXT INDEX cho LIKE '%value%'
ALTER TABLE customers ADD FULLTEXT INDEX ft_name (name);
SELECT * FROM customers WHERE MATCH(name) AGAINST('John*' IN BOOLEAN MODE);
```

```sql
-- Pattern 4: Index cho OR conditions
-- BAD: OR không thể sử dụng index hiệu quả
SELECT * FROM orders WHERE customer_id = 1 OR order_id = 1;

-- GOOD: Sử dụng UNION thay vì OR
SELECT * FROM orders WHERE customer_id = 1
UNION ALL
SELECT * FROM orders WHERE order_id = 1 AND customer_id != 1;

-- GOOD: IN thay vì OR (ít nhất là với bounded values)
SELECT * FROM orders WHERE customer_id IN (1, 2, 3, 4, 5);
```

### 4. Monitoring Index Performance

```sql
-- Tạo bảng để lưu index statistics history
CREATE TABLE index_stats_history (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(64),
    index_name VARCHAR(64),
    cardinality BIGINT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stored procedure để record stats
DELIMITER //

CREATE PROCEDURE record_index_stats()
BEGIN
    INSERT INTO index_stats_history (table_name, index_name, cardinality)
    SELECT 
        TABLE_NAME,
        INDEX_NAME,
        CARDINALITY
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE();
END //

-- Schedule: CALL record_index_stats() every hour
-- CREATE EVENT record_index_stats_event
-- ON SCHEDULE EVERY 1 HOUR
-- DO CALL record_index_stats();
```

## Các Common Patterns

### Pattern 1: High-Cardinality Primary Keys

```sql
-- BIGINT AUTO_INCREMENT cho primary keys
CREATE TABLE users (
    user_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB;

-- Hoặc UUID với index optimization
CREATE TABLE sessions (
    session_id CHAR(36) PRIMARY KEY,  -- UUID stored as CHAR
    user_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_sessions (user_id, created_at)
) ENGINE=InnoDB;

-- Nếu cần UUID với performance tốt hơn, cân nh nhắc:
-- - CAPPENDIX: UUID v1 (timestamp-based) cho locality tốt hơn
-- - Các user-generated IDs có thể dùng index prefix
```

### Pattern 2: Time-Series Data Indexing

```sql
CREATE TABLE sensor_readings (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    sensor_id INT NOT NULL,
    reading_time TIMESTAMP NOT NULL,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    INDEX idx_sensor_time (sensor_id, reading_time DESC),
    INDEX idx_time_range (reading_time)
) ENGINE=InnoDB
PARTITION BY RANGE (UNIX_TIMESTAMP(reading_time)) (
    PARTITION p_2026_q1 VALUES LESS THAN (UNIX_TIMESTAMP('2026-04-01')),
    PARTITION p_2026_q2 VALUES LESS THAN (UNIX_TIMESTAMP('2026-07-01')),
    PARTITION p_2026_q3 VALUES LESS THAN (UNIX_TIMESTAMP('2026-10-01')),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Query: Latest readings per sensor
SELECT s.*
FROM sensor_readings s
INNER JOIN (
    SELECT sensor_id, MAX(reading_time) AS max_time
    FROM sensor_readings
    GROUP BY sensor_id
) latest ON s.sensor_id = latest.sensor_id 
         AND s.reading_time = latest.max_time;

-- Query: Readings in time range
SELECT * FROM sensor_readings
WHERE reading_time BETWEEN '2026-06-01' AND '2026-06-30'
AND sensor_id = 5;
```

### Pattern 3: E-commerce Product Search

```sql
CREATE TABLE products (
    product_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) UNIQUE,
    name VARCHAR(255) NOT NULL,
    brand_id INT,
    category_id INT,
    price DECIMAL(10,2),
    stock INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FULLTEXT INDEX ft_name (name),
    INDEX idx_brand (brand_id),
    INDEX idx_category (category_id),
    INDEX idx_price (price),
    INDEX idx_brand_category (brand_id, category_id)
) ENGINE=InnoDB;

-- Search by name
SELECT * FROM products 
WHERE MATCH(name) AGAINST('+wireless +headphones' IN BOOLEAN MODE);

-- Combined search with filters
SELECT * FROM products 
WHERE MATCH(name) AGAINST('headphones' IN NATURAL LANGUAGE MODE)
AND brand_id = 5
AND price BETWEEN 50 AND 200
AND stock > 0
ORDER BY price ASC;
```

### Pattern 4: Pagination với Keyset

```sql
-- Thay vì OFFSET (chậm với large offsets)
-- SELECT * FROM orders ORDER BY order_id LIMIT 1000000, 20;

-- Sử dụng keyset pagination (cursor-based)
-- Page 1
SELECT * FROM orders ORDER BY order_id DESC LIMIT 20;

-- Giả sử last order_id là 12345
-- Page 2
SELECT * FROM orders 
WHERE order_id < 12345 
ORDER BY order_id DESC 
LIMIT 20;

-- Tạo index để support keyset pagination
CREATE INDEX idx_order_id_desc ON orders (order_id DESC);
```

## Troubleshooting

### Vấn đề 1: Query không sử dụng Index

**Symptom**: EXPLAIN cho thấy type=ALL hoặc type=index thay vì range/ref/eq_ref.

**Diagnosis**:
```sql
EXPLAIN SELECT * FROM orders 
WHERE order_date >= '2026-01-01' 
AND order_status = 'pending';

-- Kiểm tra available indexes
SHOW CREATE TABLE orders;

-- Kiểm tra index statistics
SHOW INDEX FROM orders;
ANALYZE TABLE orders;
```

**Common Causes và Solutions**:

1. **Statistics chưa up-to-date**: Run `ANALYZE TABLE`
2. **Wrong data type**: Kiểm tra column types trong query vs table definition
3. **Function applied to column**: `WHERE YEAR(order_date) = 2026` không dùng được index
4. **OR condition không match index**: Thử UNION thay vì OR

```sql
-- Wrong: Function prevents index usage
SELECT * FROM orders WHERE YEAR(order_date) = 2026;

-- Correct: Range condition can use index
SELECT * FROM orders WHERE order_date >= '2026-01-01' AND order_date < '2027-01-01';

-- Wrong: Implicit type conversion
SELECT * FROM orders WHERE customer_id = '100';  -- String vs INT

-- Correct: Match data types
SELECT * FROM orders WHERE customer_id = 100;
```

### Vấn đề 2: Composite Index không được sử dụng đúng

**Symptom**: Composite index được tạo nhưng query vẫn chậm.

**Diagnosis**:
```sql
-- Kiểm tra xem query có sử dụng index không
EXPLAIN SELECT * FROM orders 
WHERE customer_id = 100 
AND order_date >= '2026-01-01';

-- Index: (customer_id, order_date, order_status)

-- Problem: Range condition sau equality có thể limit index usage
```

**Solution**: Reorder columns hoặc tạo separate index

```sql
-- Option 1: Tạo index phù hợp với query pattern
CREATE INDEX idx_cust_date ON orders (customer_id, order_date);

-- Option 2: Sử dụng index hint
SELECT * FROM orders USE INDEX (idx_cust_date)
WHERE customer_id = 100 AND order_date >= '2026-01-01';
```

### Vấn đề 3: Too Many Indexes

**Symptom**: INSERT/UPDATE operations chậm, disk space cao.

**Diagnosis**:
```sql
-- Đếm số indexes trên mỗi bảng
SELECT 
    TABLE_NAME,
    COUNT(*) AS num_indexes,
    SUM(INDEX_LENGTH) AS total_index_size
FROM information_schema.STATISTICS
JOIN information_schema.TABLES USING (TABLE_SCHEMA, TABLE_NAME)
WHERE TABLE_SCHEMA = DATABASE()
GROUP BY TABLE_NAME
HAVING num_indexes > 5
ORDER BY total_index_size DESC;
```

**Solution**:
1. Identify unused indexes
2. Consolidate similar indexes
3. Sử dụng partial indexes nếu có thể (MySQL không support, cân nhắc other approaches)

```sql
-- Tìm và drop unused indexes
SELECT 
    OBJECT_SCHEMA,
    OBJECT_NAME,
    INDEX_NAME
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE OBJECT_SCHEMA = DATABASE()
AND INDEX_NAME IS NOT NULL
AND COUNT_READ = 0
AND COUNT_WRITE > 0;

-- Drop after confirming with monitoring
-- ALTER TABLE orders DROP INDEX idx_unused;
```

## Ví dụ Thực tế

### Ví dụ 1: E-commerce Database Index Design

```sql
-- Complete index strategy cho e-commerce schema

-- Categories table
CREATE TABLE categories (
    category_id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id SMALLINT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(category_id),
    INDEX idx_parent (parent_id)
) ENGINE=InnoDB;

-- Products table với comprehensive indexing
CREATE TABLE products (
    product_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    brand_id INT UNSIGNED,
    category_id SMALLINT UNSIGNED,
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FULLTEXT INDEX ft_search (name, sku),
    INDEX idx_brand (brand_id),
    INDEX idx_category (category_id),
    INDEX idx_price (price),
    INDEX idx_active_created (is_active, created_at DESC),
    INDEX idx_brand_category (brand_id, category_id),
    INDEX idx_lookup (category_id, is_active, price),
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
) ENGINE=InnoDB;

-- Orders table với order fulfillment indexing
CREATE TABLE orders (
    order_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    customer_id INT UNSIGNED NOT NULL,
    order_status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    payment_status ENUM('pending', 'paid', 'refunded') DEFAULT 'pending',
    shipping_method VARCHAR(50),
    order_total DECIMAL(10,2) NOT NULL,
    shipping_address_id INT UNSIGNED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_customer (customer_id),
    INDEX idx_status (order_status),
    INDEX idx_created (created_at DESC),
    INDEX idx_customer_status (customer_id, order_status),
    INDEX idx_customer_created (customer_id, created_at DESC),
    INDEX idx_status_created (order_status, created_at DESC),
    INDEX idx_payment_status (payment_status),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
) ENGINE=InnoDB;
```

### Ví dụ 2: Monitoring và Alerting Script

```bash
#!/bin/bash
# index_performance_monitor.sh

MYSQL_OPTS="--defaults-file=/etc/mysql/my.cnf -u root"
DATABASE="ecommerce"
LOG_DIR="/var/log/mysql"
ALERT_EMAIL="dba-team@company.com"

# Function: Get slow queries using indexes poorly
check_slow_index_usage() {
    mysql $MYSQL_OPTS -N -e "
        SELECT 
            ROUND(SUM_TIMER_WAIT / 1000000000000, 3) AS total_seconds,
            COUNT_STAR AS execution_count,
            DIGEST AS query_digest
        FROM performance_schema.events_statements_history
        WHERE DIGEST_TEXT LIKE '%orders%'
        ORDER BY SUM_TIMER_WAIT DESC
        LIMIT 5;"
}

# Function: Find unused indexes
find_unused_indexes() {
    mysql $MYSQL_OPTS -N -e "
        SELECT 
            CONCAT(t.TABLE_SCHEMA, '.', t.TABLE_NAME) AS full_table,
            s.INDEX_NAME,
            ROUND(t.DATA_LENGTH / 1024 / 1024, 2) AS data_mb,
            ROUND(s.CARDINALITY / t.TABLE_ROWS * 100, 2) AS selectivity
        FROM information_schema.STATISTICS s
        JOIN information_schema.TABLES t 
            ON s.TABLE_SCHEMA = t.TABLE_SCHEMA 
            AND s.TABLE_NAME = t.TABLE_NAME
        WHERE s.TABLE_SCHEMA = '$DATABASE'
        AND s.NON_UNIQUE = 1
        AND s.INDEX_NAME != 'PRIMARY'
        ORDER BY t.DATA_LENGTH DESC;"
}

# Main
echo "=== Index Performance Report - $(date) ==="
echo "--- Unused Indexes ---"
find_unused_indexes

echo "--- Slow Queries ---"
check_slow_index_usage
```

## Tham khảo

### Official Documentation

- [MySQL Indexes](https://dev.mysql.com/doc/refman/8.0/en/mysql-indexes.html)
- [B-Tree Indexes](https://dev.mysql.com/doc/refman/8.0/en/optimization.html#btree-indexes)
- [Invisible Indexes](https://dev.mysql.com/doc/refman/8.0/en/invisible-indexes.html)
- [Descending Indexes](https://dev.mysql.com/doc/refman/8.0/en/descending-indexes.html)
- [Optimizer Hints](https://dev.mysql.com/doc/refman/8.0/en/optimizer-hints.html)

### Performance Schema Tables

```sql
-- Useful Performance Schema tables for index monitoring
SELECT * FROM performance_schema.table_io_waits_summary_by_index_usage;
SELECT * FROM performance_schema.table_lock_waits_summary_by_table;
SELECT * FROM performance_schema.events_statements_summary_by_digest;
```

### Tools

- `EXPLAIN` - Query execution plan analysis
- `EXPLAIN ANALYZE` (MySQL 8.0.18+) - Actual execution statistics
- `optimizer_switch` - Control optimizer behavior
- `index_statistics` - Table statistics

### Books

- "High Performance MySQL" - Chapter on Indexing
- "MySQL Performance Tuning" - Index optimization strategies

---

*Document version: 1.0.0*
*Last updated: 2026-06-23*
*Framework: Cursor Enterprise Framework*
