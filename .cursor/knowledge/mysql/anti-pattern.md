# MySQL Anti-Patterns - Các Mẫu Cần Tránh

## Mục lục
1. [Schema Design Anti-Patterns](#1-schema-design-anti-patterns)
2. [Query Anti-Patterns](#2-query-anti-patterns)
3. [Index Anti-Patterns](#3-index-anti-patterns)

---

## 1. Schema Design Anti-Patterns

### 1.1 Storing Data in Wrong Types

**Tên Pattern**: Type Mismatch

**Mô tả**: Sử dụng sai data types dẫn đến storage waste, performance issues, và incorrect results.

**Ví dụ (Anti-Pattern)**:
```sql
-- ❌ BAD: Using VARCHAR for everything
CREATE TABLE events (
  id INT PRIMARY KEY,
  event_name VARCHAR(1000),  -- Too long for event names
  event_date VARCHAR(50),    -- Should be DATE/DATETIME
  event_type VARCHAR(20),    -- Should be ENUM
  is_active VARCHAR(10)       -- Should be BOOLEAN/TINYINT(1)
);

-- ❌ BAD: Using TEXT for short strings
CREATE TABLE settings (
  key VARCHAR(50) PRIMARY KEY,
  value TEXT              -- Unnecessary, VARCHAR(255) is enough
);
```

**Hậu quả**:
- Wasted storage
- Slower queries (TEXT can't be indexed properly)
- Type conversion overhead
- Incorrect sorting/filtering

**Giải pháp thay thế**:
```sql
-- ✅ GOOD: Appropriate types
CREATE TABLE events (
  id INT PRIMARY KEY,
  event_name VARCHAR(100),
  event_date DATETIME,
  event_type ENUM('conference', 'workshop', 'webinar') DEFAULT 'webinar',
  is_active TINYINT(1) DEFAULT 1
);
```

---

### 1.2 Not Using Foreign Keys

**Tên Pattern**: Orphaned Data

**Mô tả**: Không enforce referential integrity với foreign keys.

**Ví dụ (Anti-Pattern)**:
```sql
-- ❌ BAD: No foreign key constraint
CREATE TABLE orders (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,  -- No constraint!
  total DECIMAL(10,2),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Application code "hopes" user_id exists
-- But orphaned orders can be created
INSERT INTO orders (user_id, total) VALUES (999, 100.00);
-- user_id 999 doesn't exist!
```

**Hậu quả**:
- Orphaned records (dangling references)
- Inconsistent data
- Application must enforce integrity (error-prone)
- JOINs return unexpected results

**Giải pháp thay thế**:
```sql
-- ✅ GOOD: Foreign key enforces integrity
CREATE TABLE orders (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  total DECIMAL(10,2),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);
```

---

### 1.3 Over-Normalization

**Tên Pattern**: Excessive Normalization

**Mô tả**: Breaking tables into too many pieces, making queries complex và slow.

**Ví dụ (Anti-Pattern)**:
```sql
-- ❌ BAD: Over-normalized address
CREATE TABLE address_street_type (
  id TINYINT PRIMARY KEY,
  name VARCHAR(20)  -- 'Street', 'Avenue', 'Road'
);

CREATE TABLE address_suffix (
  id TINYINT PRIMARY KEY,
  name VARCHAR(20)  -- 'North', 'South'
);

CREATE TABLE addresses (
  id INT PRIMARY KEY,
  street_type_id TINYINT,
  street_name VARCHAR(100),
  street_number VARCHAR(20),
  suffix_id TINYINT,
  city_id INT,
  -- Too many joins needed!
  FOREIGN KEY (street_type_id) REFERENCES address_street_type(id),
  FOREIGN KEY (suffix_id) REFERENCES address_suffix(id),
  FOREIGN KEY (city_id) REFERENCES cities(id)
);

-- Query becomes a nightmare:
SELECT 
  s.street_number, s.street_name, t.name, f.name, c.name
FROM addresses s
JOIN address_street_type t ON s.street_type_id = t.id
JOIN address_suffix f ON s.suffix_id = f.id
JOIN cities c ON s.city_id = c.id;
```

**Hậu quả**:
- Complex, slow queries
- Excessive JOINs
- Difficult to maintain
- Poor read performance

**Giải pháp thay thế**:
```sql
-- ✅ GOOD: Sensible normalization
CREATE TABLE addresses (
  id INT PRIMARY KEY AUTO_INCREMENT,
  street VARCHAR(255) NOT NULL,  -- '123 Main Street North'
  city VARCHAR(100) NOT NULL,
  state VARCHAR(50) NOT NULL,
  postal_code VARCHAR(20) NOT NULL,
  country VARCHAR(100) NOT NULL DEFAULT 'USA'
);

-- Or a lookup table for countries only
CREATE TABLE countries (
  code CHAR(2) PRIMARY KEY,  -- 'US', 'VN', 'JP'
  name VARCHAR(100) NOT NULL
);
```

---

## 2. Query Anti-Patterns

### 2.1 Using OR in WHERE Clause

**Tên Pattern**: OR Performance Killer

**Mô tả**: Sử dụng OR conditions làm query optimizer không thể use indexes efficiently.

**Ví dụ (Anti-Pattern)**:
```sql
-- ❌ BAD: OR prevents index usage
SELECT * FROM orders 
WHERE customer_id = 1 OR customer_id = 2 OR customer_id = 3;

-- ❌ BAD: OR with different columns
SELECT * FROM users 
WHERE email = 'test@example.com' OR phone = '1234567890';
```

**Hậu quả**:
- Full table scan or multiple index scans
- Poor performance
- OR doesn't scale

**Giải pháp thay thế**:
```sql
-- ✅ GOOD: Use IN for multiple values
SELECT * FROM orders WHERE customer_id IN (1, 2, 3);

-- ✅ GOOD: UNION for different columns
(SELECT * FROM users WHERE email = 'test@example.com')
UNION ALL
(SELECT * FROM users WHERE phone = '1234567890');

-- ✅ GOOD: Separate queries with conditional index usage
SELECT * FROM users WHERE email = 'test@example.com';
SELECT * FROM users WHERE phone = '1234567890';
```

---

### 2.2 Implicit Type Conversion

**Tên Pattern**: String Number Comparison

**Mô tả**: So sánh different types gây ra implicit conversion và prevents index usage.

**Ví dụ (Anti-Pattern)**:
```sql
-- ❌ BAD: String compared to number
SELECT * FROM users WHERE id = '123';  -- String '123' converted to number

-- ❌ BAD: Number column compared to string
CREATE TABLE products (
  product_id VARCHAR(10) PRIMARY KEY  -- String IDs
);

SELECT * FROM products WHERE product_id = 123;
-- '123' converted to number 123!

-- ❌ BAD: Date comparison with string
SELECT * FROM orders WHERE created_at = '2024-01-15';
-- Works but implicit conversion
```

**Hậu quả**:
- Index not used
- Full table scan
- Potential incorrect results
- Performance degradation

**Giải pháp thay thế**:
```sql
-- ✅ GOOD: Match types
SELECT * FROM users WHERE id = 123;
SELECT * FROM users WHERE id = CAST('123' AS UNSIGNED);

-- ✅ GOOD: String column, string value
SELECT * FROM products WHERE product_id = '123';

-- ✅ GOOD: Explicit date handling
SELECT * FROM orders WHERE created_at = '2024-01-15 00:00:00';
SELECT * FROM orders WHERE DATE(created_at) = '2024-01-15';
```

---

### 2.3 Function on Indexed Column

**Tên Pattern**: Function Wrapper

**Mô tả**: Wrapping indexed column trong function prevents index usage.

**Ví dụ (Anti-Pattern)**:
```sql
-- ❌ BAD: Function prevents index use
SELECT * FROM users WHERE YEAR(created_at) = 2024;
SELECT * FROM users WHERE MONTH(created_at) = 1;
SELECT * FROM users WHERE DAY(created_at) = 15;

-- ❌ BAD: String function on indexed column
SELECT * FROM products WHERE LOWER(name) = 'iphone';
SELECT * FROM users WHERE SUBSTRING(email, 1, 5) = 'admin';

-- ❌ BAD: Math operation on column
SELECT * FROM orders WHERE total * 1.1 > 1000;
```

**Hậu quả**:
- Full table scan
- Cannot use index
- Slow queries

**Giải pháp thay thế**:
```sql
-- ✅ GOOD: Range query on column
SELECT * FROM users 
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';

-- ✅ GOOD: Separate column for search-friendly value
ALTER TABLE products ADD COLUMN name_lower VARCHAR(200);
CREATE INDEX idx_name_lower ON products(name_lower);

UPDATE products SET name_lower = LOWER(name);

SELECT * FROM products WHERE name_lower = 'iphone';

-- ✅ GOOD: Pre-computed values
SELECT * FROM orders WHERE total > 909.09;
```

---

## 3. Index Anti-Patterns

### 3.1 Too Many Indexes

**Tên Pattern**: Index Proliferation

**Mô tả**: Tạo quá nhiều indexes trên table.

**Ví dụ (Anti-Pattern)**:
```sql
-- ❌ BAD: Redundant indexes
CREATE TABLE users (
  id INT PRIMARY KEY,
  email VARCHAR(255),
  name VARCHAR(100),
  status VARCHAR(20),
  created_at DATETIME,
  
  INDEX idx_email (email),         -- Unique constraint already creates index
  INDEX idx_status (status),       -- Never queried alone
  INDEX idx_created (created_at),  -- Rarely sorted by this
  INDEX idx_status_created (status, created_at),  -- Redundant
  INDEX idx_created_status (created_at, status)   -- Redundant
);

-- Every INSERT/UPDATE/DELETE must update all these indexes
```

**Hậu quả**:
- Slow INSERT/UPDATE/DELETE
- Wasted storage
- Memory pressure for buffer pool
- Optimizer confusion

**Giải pháp thay thế**:
```sql
-- ✅ GOOD: Only necessary indexes
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(100),
  status ENUM('active', 'inactive', 'pending') DEFAULT 'active',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_status_created (status, created_at)  -- Covers: WHERE status = ? ORDER BY created_at
);

-- Review and remove unused indexes
SELECT 
  object_schema, object_name, index_name
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE index_name IS NOT NULL
  AND count_star = 0
ORDER BY object_schema, object_name;
```

---

### 3.2 Leading Wildcard in LIKE

**Tên Pattern**: Wildcard Prefix

**Mô tả**: Using leading wildcard in LIKE pattern prevents index usage.

**Ví dụ (Anti-Pattern)**:
```sql
-- ❌ BAD: Leading wildcard
SELECT * FROM products WHERE name LIKE '%phone%';
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- ❌ BAD: Variable leading wildcard
SELECT * FROM products WHERE name LIKE CONCAT('%', ?, '%');
```

**Hậu quả**:
- Full table scan
- No index usage possible
- Very slow queries

**Giải pháp thay thế**:
```sql
-- ✅ GOOD: Use FULLTEXT index for text search
ALTER TABLE products ADD FULLTEXT INDEX ft_name (name);

SELECT * FROM products 
WHERE MATCH(name) AGAINST('phone' IN NATURAL LANGUAGE MODE);

-- ✅ GOOD: Trailing wildcard only (can use index)
SELECT * FROM products WHERE name LIKE 'iPhone%';

-- ✅ GOOD: Use Elasticsearch for complex search
-- Keep MySQL for structured queries
```

---

### 3.3 Low-Selectivity Index

**Tên Pattern**: Skewed Index

**Mô tả**: Index trên column có very few distinct values (low cardinality).

**Ví dụ (Anti-Pattern)**:
```sql
-- ❌ BAD: Index on boolean column
CREATE TABLE orders (
  id INT PRIMARY KEY,
  status ENUM('pending', 'completed', 'cancelled'),
  INDEX idx_status (status)  -- Only 3 values!
);

-- 99% are 'completed', index won't help

-- ❌ BAD: Index on gender
CREATE TABLE users (
  id INT PRIMARY KEY,
  gender ENUM('M', 'F'),
  INDEX idx_gender (gender)
);

-- Only 2 values
```

**Hậu quả**:
- Optimizer ignores index
- Full table scan faster than index scan
- Wasted storage

**Giải pháp thay thế**:
```sql
-- ✅ GOOD: Composite index with high-selectivity column first
CREATE INDEX idx_status_created ON orders(status, created_at);
-- Query: WHERE status = 'pending' ORDER BY created_at

-- ✅ GOOD: Don't index very low cardinality columns alone
-- Rely on other high-selectivity indexes

-- ✅ GOOD: Partial index (MySQL 8.0+)
CREATE INDEX idx_pending ON orders (created_at)
WHERE status = 'pending';
-- Only indexes pending orders!
```

---

## Liên kết liên quan
- [MySQL Glossary](./glossary.md)
- [MySQL Architecture](./architecture.md)
- [MySQL Best Practices](./best-practice.md)
- [MySQL Checklist](./checklist.md)
- [MySQL FAQ](./faq.md)
- [MySQL Decision Tree](./decision-tree.md)
