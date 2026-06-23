# MySQL Best Practices - Các Thực Hành Tốt Nhất

## Mục lục
1. [Schema Design](#1-schema-design)
2. [Indexing](#2-indexing)
3. [Query Optimization](#3-query-optimization)
4. [Transaction Management](#4-transaction-management)
5. [Security](#5-security)
6. [Backup & Recovery](#6-backup--recovery)

---

## 1. Schema Design

### 1.1 Use Appropriate Data Types

**Mô tả**: Chọn data types phù hợp để optimize storage và performance.

**Ví dụ**:
```sql
-- ❌ BAD: Using VARCHAR for fixed-length data
CREATE TABLE user_bad (
  phone VARCHAR(20),  -- 20 bytes always
  status VARCHAR(10)  -- Only 'active'/'inactive'
);

-- ✅ GOOD: Using appropriate types
CREATE TABLE user_good (
  phone VARCHAR(20),  -- Variable length
  status ENUM('active', 'inactive', 'pending') DEFAULT 'pending',
  -- ENUM uses 1 byte internally for up to 255 values
);

-- Use appropriate sizes
CREATE TABLE products (
  id INT UNSIGNED,        -- No negative IDs needed
  price DECIMAL(10,2),   -- For currency (10 digits, 2 decimals)
  weight FLOAT,          -- Scientific values, not precise
  ratio DECIMAL(5,2),     -- Precision needed: 123.45
  flag TINYINT(1),       -- Boolean as 0/1
  created_at DATETIME,     -- Full timestamp
  created_date DATE       -- Date only
);

-- Use JSON for semi-structured data
CREATE TABLE app_config (
  id INT PRIMARY KEY,
  config JSON,
  -- Access: config->>'$.theme'
  -- Index on virtual columns if needed
);
```

**Khi nào áp dụng**: Mọi table definitions.

### 1.2 Normalize Appropriately

**Mô tả**: Áp dụng normalization (3NF typically) để minimize redundancy nhưng không over-normalize.

**Ví dụ**:
```sql
-- ✅ GOOD: Properly normalized schema
CREATE TABLE customers (
  customer_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL,
  UNIQUE KEY idx_email (email)
);

CREATE TABLE products (
  product_id INT PRIMARY KEY AUTO_INCREMENT,
  category_id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE orders (
  order_id INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT NOT NULL,
  order_date DATETIME NOT NULL,
  status ENUM('pending', 'processing', 'shipped', 'delivered') DEFAULT 'pending',
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT UNSIGNED NOT NULL DEFAULT 1,
  price DECIMAL(10,2) NOT NULL,  -- Snapshot at time of order
  PRIMARY KEY (order_id, product_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Denormalize judiciously for read performance
CREATE TABLE order_summary (
  order_id INT PRIMARY KEY,
  customer_id INT NOT NULL,
  total_items INT UNSIGNED,
  total_amount DECIMAL(10,2),
  -- Materialized from orders + order_items for fast reporting
  INDEX idx_customer (customer_id),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

**Khi nào áp dụng**: Database schema design.

### 1.3 Include Audit Columns

**Mô tả**: Thêm columns để track creation và modification metadata.

**Ví dụ**:
```sql
CREATE TABLE users (
  id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL,
  
  -- Audit columns
  created_by INT UNSIGNED NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_by INT UNSIGNED NULL,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at DATETIME NULL,  -- Soft delete
  deleted_by INT UNSIGNED NULL,
  version INT UNSIGNED NOT NULL DEFAULT 1,  -- Optimistic locking
  
  INDEX idx_deleted_at (deleted_at),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Trigger to auto-update version
DELIMITER //
CREATE TRIGGER users_version_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
  SET NEW.version = OLD.version + 1;
  SET NEW.updated_at = NOW();
END//
DELIMITER ;
```

**Khi nào áp dụng**: Tables cần audit trail.

---

## 2. Indexing

### 2.1 Create Indexes for Foreign Keys

**Mô tả**: Luôn tạo indexes trên foreign key columns để improve join performance.

**Ví dụ**:
```sql
-- ✅ GOOD: Index on foreign key
CREATE TABLE orders (
  id INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT NOT NULL,
  order_date DATETIME NOT NULL,
  INDEX idx_customer (customer_id),  -- Foreign key column indexed
  FOREIGN KEY (customer_id) REFERENCES customers(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

-- ✅ GOOD: Composite index for common query patterns
CREATE TABLE order_items (
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT UNSIGNED NOT NULL DEFAULT 1,
  PRIMARY KEY (order_id, product_id),  -- Composite PK covers both
  INDEX idx_product (product_id),  -- For: "find all orders containing product X"
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (product_id) REFERENCES products(id)
);
```

**Khi nào áp dụng**: Mọi foreign key columns.

### 2.2 Use Covering Indexes

**Mô tả**: Tạo covering indexes để satisfy entire query từ index mà không cần access table.

**Ví dụ**:
```sql
-- ❌ BAD: Index doesn't cover all needed columns
CREATE INDEX idx_status ON orders(status);
-- Query: SELECT id, status, created_at FROM orders WHERE status = 'pending'
-- Needs: index lookup + table access for created_at

-- ✅ GOOD: Covering index
CREATE INDEX idx_status_covering ON orders(status, id, created_at);
-- Query: SELECT id, status, created_at FROM orders WHERE status = 'pending'
-- Result: Entire query satisfied from index

-- ✅ GOOD: Composite covering index for complex query
CREATE TABLE posts (
  id INT PRIMARY KEY AUTO_INCREMENT,
  author_id INT NOT NULL,
  status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
  created_at DATETIME NOT NULL,
  title VARCHAR(200) NOT NULL,
  INDEX idx_author_status_date (author_id, status, created_at, id)
);

-- Query satisfied from index:
-- SELECT id, title, created_at FROM posts 
-- WHERE author_id = 1 AND status = 'published'
-- ORDER BY created_at DESC
```

**Khi nào áp dụng**: Frequently executed queries.

### 2.3 Index Column Order Matters

**Mô tả**: Thứ tự columns trong composite index ảnh hưởng đến usability.

**Ví dụ**:
```sql
-- Column order: Equal conditions first, then range
CREATE INDEX idx_user_status_created ON orders(user_id, status, created_at);

-- Query patterns:
-- ✓ WHERE user_id = 1 AND status = 'pending' AND created_at > '2024-01-01'
-- ✓ WHERE user_id = 1 AND status = 'pending'
-- ✓ WHERE user_id = 1
-- ✗ WHERE status = 'pending'  -- Can't use index efficiently

-- For OR conditions, consider separate indexes or UNION
-- ❌ BAD: OR makes index less useful
-- SELECT * FROM orders WHERE user_id = 1 OR status = 'pending'

-- ✅ GOOD: UNION approach
(SELECT * FROM orders WHERE user_id = 1)
UNION ALL
(SELECT * FROM orders WHERE status = 'pending' AND user_id != 1);
```

**Khi nào áp dụng**: Composite indexes.

---

## 3. Query Optimization

### 3.1 Avoid SELECT *

**Mô tả**: Chỉ select columns cần thiết để reduce data transfer và enable covering indexes.

**Ví dụ**:
```sql
-- ❌ BAD: SELECT *
SELECT * FROM users WHERE id = 1;

-- ✅ GOOD: Specific columns
SELECT id, name, email, created_at 
FROM users 
WHERE id = 1;

-- ✅ GOOD: Count specific column (not all)
SELECT COUNT(id) FROM orders WHERE status = 'completed';
-- vs COUNT(*) which may be slower
```

**Khi nào áp dụng**: Mọi SELECT statements.

### 3.2 Use EXPLAIN to Analyze Queries

**Mô tả**: Sử dụng EXPLAIN để understand query execution plan.

**Ví dụ**:
```sql
-- Basic EXPLAIN
EXPLAIN SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
GROUP BY u.id
HAVING COUNT(o.id) > 5;

-- JSON format for detailed analysis
EXPLAIN FORMAT=JSON
SELECT * FROM orders WHERE status = 'pending';

-- EXPLAIN ANALYZE (MySQL 8.0+)
EXPLAIN ANALYZE
SELECT * FROM orders WHERE created_at > '2024-01-01';
-- Shows actual vs estimated rows, execution time
```

**Khi nào áp dụng**: Query optimization.

### 3.3 Optimize JOINs

**Mô tả**: Ensure JOINs sử dụng indexes và không produce large intermediate results.

**Ví dụ**:
```sql
-- ✅ GOOD: Join on indexed columns
SELECT o.id, u.name
FROM orders o
INNER JOIN users u ON o.user_id = u.id  -- Both indexed

-- ✅ GOOD: Small driving table first
EXPLAIN SELECT /*+ JOIN_PREFIX(order_items) */ ...
-- Force smaller table as driving table

-- ✅ GOOD: Use STRAIGHT_JOIN when order matters
SELECT STRAIGHT_JOIN o.id, u.name
FROM users u
STRAIGHT_JOIN orders o ON o.user_id = u.id;
-- Forces users as driving table

-- ❌ BAD: Function on indexed column
SELECT * FROM orders WHERE YEAR(created_at) = 2024;

-- ✅ GOOD: Range condition on column
SELECT * FROM orders 
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
```

**Khi nào áp dụng**: Query với JOINs.

---

## 4. Transaction Management

### 4.1 Keep Transactions Short

**Mô tả**: Giữ transactions ngắn để minimize locking và improve concurrency.

**Ví dụ**:
```sql
-- ❌ BAD: Long transaction
START TRANSACTION;
SELECT * FROM users;  -- Locks rows
-- User goes to lunch
UPDATE users SET last_login = NOW() WHERE id = 1;  -- Lock held too long
COMMIT;

-- ✅ GOOD: Short transaction
START TRANSACTION;
UPDATE users SET last_login = NOW() WHERE id = 1;
COMMIT;
```

**Khi nào áp dụng**: Mọi transactions.

### 4.2 Handle Deadlocks Gracefully

**Mô tả**: Implement retry logic cho deadlock situations.

**Ví dụ**:
```sql
DELIMITER //

CREATE PROCEDURE transfer_funds(
  IN from_account INT,
  IN to_account INT,
  IN amount DECIMAL(10,2)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    ROLLBACK;
    RESIGNAL;
  END;
  
  DECLARE deadlock_attempt INT DEFAULT 0;
  DECLARE max_attempts INT DEFAULT 3;
  
  retry_block: WHILE deadlock_attempt < max_attempts DO
    BEGIN
      DECLARE deadlock_detected CONDITION FOR 1213;
      DECLARE EXIT HANDLER FOR deadlock_detected
      BEGIN
        SET deadlock_attempt = deadlock_attempt + 1;
        IF deadlock_attempt < max_attempts THEN
          -- Wait and retry
          DO SLEEP(0.1 * deadlock_attempt);
          ITERATE retry_block;
        ELSE
          SIGNAL SQLSTATE '45000' 
          SET MESSAGE_TEXT = 'Transaction failed after max retries';
        END IF;
      END;
      
      START TRANSACTION;
      UPDATE accounts SET balance = balance - amount WHERE id = from_account;
      UPDATE accounts SET balance = balance + amount WHERE id = to_account;
      COMMIT;
      
      LEAVE retry_block;
    END;
  END WHILE;
END //

DELIMITER ;
```

**Khi nào áp dụng**: Applications handling concurrent transactions.

---

## 5. Security

### 5.1 Use Strong Passwords

**Mô tả**: Enforce strong passwords cho database users.

**Ví dụ**:
```sql
-- Create user with strong password
CREATE USER 'app_user'@'%' IDENTIFIED BY 'UseStr0ng!Pass#2024';

-- Password validation plugin
INSTALL PLUGIN validate_password SONAME 'validate_password.so';

SET GLOBAL validate_password.policy = 'STRONG';
SET GLOBAL validate_password.length = 12;
SET GLOBAL validate_password.mixed_case_count = 1;
SET GLOBAL validate_password.number_count = 1;
SET GLOBAL validate_password.special_count = 1;

-- Force password expiration
ALTER USER 'app_user'@'%' PASSWORD EXPIRE INTERVAL 90 DAY;
```

**Khi nào áp dụng**: User management.

### 5.2 Principle of Least Privilege

**Mô tả**: Chỉ grant những permissions cần thiết.

**Ví dụ**:
```sql
-- Application user - only DML on specific tables
GRANT SELECT, INSERT, UPDATE, DELETE 
ON shop_db.products TO 'app_user'@'%';

-- Read-only user for reporting
GRANT SELECT 
ON shop_db.* TO 'report_user'@'%';

-- Admin user - limited DDL
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX 
ON shop_db.* TO 'admin_user'@'localhost';

-- DBA user - full access
GRANT ALL PRIVILEGES 
ON *.* TO 'dba_user'@'localhost' WITH GRANT OPTION;

-- Regular review of privileges
SELECT user, host FROM mysql.user;
SHOW GRANTS FOR 'app_user'@'%';
```

**Khi nào áp dụng**: Database user management.

---

## 6. Backup & Recovery

### 6.1 Regular Backups

**Mô tả**: Implement backup strategy phù hợp với RTO/RPO requirements.

**Ví dụ**:
```bash
#!/bin/bash
# Full backup with locking
mysqldump \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  --master-data=2 \
  --flush-logs \
  --delete-master-logs \
  --user=backup_user \
  --password=SecurePassword123 \
  --all-databases \
  | gzip > /backup/mysql_$(date +%Y%m%d_%H%M%S).sql.gz

# Incremental backup (binlog)
mysqladmin flush-logs
cp /var/lib/mysql/mysql-bin.* /backup/incremental/

# Point-in-time recovery
mysqlbinlog \
  --start-datetime="2024-01-15 10:00:00" \
  --stop-datetime="2024-01-15 11:00:00" \
  /var/lib/mysql/mysql-bin.000123 | mysql
```

**Khi nào áp dụng**: Production databases.

### 6.2 Test Recovery Procedures

**Mô tả**: Regular test backup và recovery để đảm bảo procedures work.

**Ví dụ**:
```bash
#!/bin/bash
# Test restore to different server
set -e

BACKUP_FILE="/backup/mysql_$(date +%Y%m%d).sql.gz"
TEST_DB="mysql_test_restore"

# Create test database
mysql -e "DROP DATABASE IF EXISTS ${TEST_DB}; CREATE DATABASE ${TEST_DB};"

# Restore
gunzip < $BACKUP_FILE | mysql $TEST_DB

# Verify
TABLE_COUNT=$(mysql -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='${TEST_DB}';")
echo "Restored $TABLE_COUNT tables"

# Check data integrity
ROW_COUNT=$(mysql -N -e "SELECT COUNT(*) FROM ${TEST_DB}.users;")
echo "Users table has $ROW_COUNT rows"

# Cleanup
mysql -e "DROP DATABASE ${TEST_DB};"
```

**Khi nào áp dụng**: Backup procedures.

---

## Liên kết liên quan
- [MySQL Glossary](./glossary.md)
- [MySQL Architecture](./architecture.md)
- [MySQL Anti-Patterns](./anti-pattern.md)
- [MySQL Checklist](./checklist.md)
- [MySQL FAQ](./faq.md)
- [MySQL Decision Tree](./decision-tree.md)
