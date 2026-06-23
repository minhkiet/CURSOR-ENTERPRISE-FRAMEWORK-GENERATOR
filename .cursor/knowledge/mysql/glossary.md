# MySQL Glossary - Thuật Ngữ Chuyên Ngành

## Mục lục
1. [Database Objects](#1-database-objects)
2. [Data Types](#2-data-types)
3. [Indexes](#3-indexes)
4. [Query Operations](#4-query-operations)
5. [Transactions](#5-transactions)
6. [Replication](#6-replication)
7. [Storage Engines](#7-storage-engines)

---

## Database

**Định nghĩa**: Database là container chứa tables, views, stored procedures, và các objects khác. Trong MySQL, mỗi database tương ứng với một thư mục trong data directory.

**Ví dụ**:
```sql
-- Create database
CREATE DATABASE IF NOT EXISTS shop_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Use database
USE shop_db;

-- Show databases
SHOW DATABASES;

-- Drop database
DROP DATABASE IF EXISTS old_db;
```

---

## Table

**Định nghĩa**: Table là cấu trúc dữ liệu cơ bản trong MySQL, chứa rows (records) và columns (fields). Mỗi table có definition về columns, indexes, và constraints.

**Ví dụ**:
```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash CHAR(60) NOT NULL,
  role ENUM('user', 'admin', 'moderator') DEFAULT 'user',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL,
  
  INDEX idx_email (email),
  INDEX idx_role (role),
  INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## Primary Key

**Định nghĩa**: Primary Key là column hoặc set of columns uniquely identify mỗi row trong table. Nó không thể chứa NULL values và phải unique.

**Ví dụ**:
```sql
-- Single column primary key
CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  -- ...
);

-- Composite primary key
CREATE TABLE order_items (
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL DEFAULT 1,
  PRIMARY KEY (order_id, product_id)
);

-- Add primary key to existing table
ALTER TABLE users ADD PRIMARY KEY (id);
```

---

## Foreign Key

**Định nghĩa**: Foreign Key là column hoặc set of columns tham chiếu đến primary key của table khác, enforce referential integrity.

**Ví dụ**:
```sql
CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  status VARCHAR(50) DEFAULT 'pending',
  
  FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

-- Self-referencing foreign key
CREATE TABLE categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  parent_id INT NULL,
  FOREIGN KEY (parent_id) REFERENCES categories(id)
    ON DELETE SET NULL
);
```

---

## Index

**Định nghĩa**: Index là cấu trúc dữ liệu cải thiện tốc độ truy xuất data. MySQL support nhiều loại indexes: B-tree, Hash, Full-text, Spatial.

**Ví dụ**:
```sql
-- Single column index
CREATE INDEX idx_email ON users(email);

-- Composite index (multiple columns)
CREATE INDEX idx_user_status ON orders(user_id, status);

-- Unique index
CREATE UNIQUE INDEX idx_unique_email ON users(email);

-- Full-text index for text search
CREATE FULLTEXT INDEX idx_search ON posts(title, content);

-- Drop index
DROP INDEX idx_email ON users;
```

---

## SELECT

**Định nghĩa**: SELECT là câu lệnh truy vấn data từ một hoặc nhiều tables, có thể filter, sort, và aggregate data.

**Ví dụ**:
```sql
-- Basic select
SELECT id, name, email FROM users WHERE active = 1;

-- Join multiple tables
SELECT o.id, o.created_at, u.name, u.email
FROM orders o
INNER JOIN users u ON o.user_id = u.id
WHERE o.status = 'completed'
ORDER BY o.created_at DESC
LIMIT 10 OFFSET 0;

-- Subquery
SELECT * FROM products 
WHERE price > (SELECT AVG(price) FROM products);

-- Common Table Expression (CTE)
WITH active_users AS (
  SELECT * FROM users WHERE status = 'active'
)
SELECT * FROM active_users WHERE created_at > '2024-01-01';
```

---

## JOIN

**Định nghĩa**: JOIN kết hợp rows từ hai hoặc nhiều tables dựa trên related columns.

**Ví dụ**:
```sql
-- INNER JOIN: chỉ rows có matches
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN: tất cả rows từ left table
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

-- RIGHT JOIN: tất cả rows từ right table
SELECT u.name, o.total
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;

-- Multiple joins
SELECT p.name, oi.quantity, o.total
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id;
```

---

## GROUP BY

**Định nghĩa**: GROUP BY nhóm rows có cùng values trong specified columns, cho phép aggregate functions.

**Ví dụ**:
```sql
-- Basic group by
SELECT user_id, COUNT(*) as order_count, SUM(total) as total_spent
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 5;

-- With aggregate functions
SELECT 
  DATE(created_at) as date,
  COUNT(*) as orders,
  AVG(total) as avg_order_value,
  MAX(total) as max_order_value,
  MIN(total) as min_order_value
FROM orders
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

---

## Transaction

**Định nghĩa**: Transaction là unit of work bao gồm một hoặc nhiều SQL statements được executed như một atomic unit.

**Ví dụ**:
```sql
START TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Check if successful
IF @@error_count = 0 THEN
  COMMIT;
ELSE
  ROLLBACK;
END IF;

-- Savepoint
SAVEPOINT before_update;

UPDATE users SET name = 'New Name' WHERE id = 1;
ROLLBACK TO SAVEPOINT before_update;
```

---

## ACID

**Định nghĩa**: ACID là properties đảm bảo reliability của transactions: Atomicity, Consistency, Isolation, Durability.

**Ví dụ**:
```sql
-- Atomicity: All or nothing
START TRANSACTION;
INSERT INTO orders (user_id, total) VALUES (1, 100);
INSERT INTO order_items (order_id, product_id, quantity) VALUES (LAST_INSERT_ID(), 1, 1);
COMMIT; -- Both succeed or both fail

-- Isolation: MVCC prevents dirty reads
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
-- Your changes are isolated from other transactions
COMMIT;

-- Durability: InnoDB ensures committed data survives crashes
-- Uses redo logs and doublewrite buffer
```

---

## Storage Engine

**Định nghĩa**: Storage Engine là component xử lý storage và retrieval of data. MySQL có nhiều engines, phổ biến nhất là InnoDB và MyISAM.

**Ví dụ**:
```sql
-- Create table with specific engine
CREATE TABLE innodb_table (
  id INT PRIMARY KEY
) ENGINE=InnoDB;

-- Create table with MyISAM (legacy)
CREATE TABLE myisam_table (
  id INT PRIMARY KEY,
  FULLTEXT INDEX idx_content (content)
) ENGINE=MyISAM;

-- Check engine of table
SHOW TABLE STATUS FROM database_name WHERE Name = 'users';

-- Change engine
ALTER TABLE users ENGINE=InnoDB;
```

---

## EXPLAIN

**Định nghĩa**: EXPLAIN hiển thị execution plan của query, giúp understand cách MySQL execute query và identify performance issues.

**Ví dụ**:
```sql
EXPLAIN SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
GROUP BY u.id;

EXPLAIN FORMAT=JSON SELECT * FROM users WHERE email = 'test@example.com';

-- Analyze query
EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'pending';
```

---

## Normalization

**Định nghĩa**: Normalization là quá trình tổ chức data vào tables để minimize redundancy và ensure data integrity.

**Ví dụ**:
```sql
-- 1NF: Atomic values, no repeating groups
CREATE TABLE contacts (
  id INT PRIMARY KEY,
  name VARCHAR(100),  -- atomic
  phone1 VARCHAR(20),   -- repeating group ❌
  phone2 VARCHAR(20),  -- repeating group ❌
  phone3 VARCHAR(20)   -- repeating group ❌
);

-- Better: Separate phone numbers
CREATE TABLE contact_phones (
  contact_id INT,
  phone VARCHAR(20),
  PRIMARY KEY (contact_id, phone)
);

-- 3NF: No transitive dependencies
-- users table should not have department_name
-- (depends on dept_id, which depends on user_id - transitive)
CREATE TABLE users (
  user_id INT PRIMARY KEY,
  name VARCHAR(100),
  dept_id INT,
  FOREIGN KEY (dept_id) REFERENCES departments(id)
);
```

---

## Stored Procedure

**Định nghĩa**: Stored Procedure là pre-compiled collection of SQL statements được stored trong database và có thể được gọi bằng CALL statement.

**Ví dụ**:
```sql
DELIMITER //

CREATE PROCEDURE get_user_orders(
  IN user_id_param INT,
  OUT order_count INT
)
BEGIN
  SELECT COUNT(*) INTO order_count
  FROM orders
  WHERE user_id = user_id_param;
  
  SELECT o.*, u.name as customer_name
  FROM orders o
  INNER JOIN users u ON o.user_id = u.id
  WHERE o.user_id = user_id_param
  ORDER BY o.created_at DESC;
END //

DELIMITER ;

-- Call procedure
CALL get_user_orders(1, @count);
SELECT @count as total_orders;
```

---

## Trigger

**Định nghĩa**: Trigger là named database object được execute tự động khi một DML event (INSERT, UPDATE, DELETE) xảy ra trên table.

**Ví dụ**:
```sql
DELIMITER //

CREATE TRIGGER before_order_insert
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
  SET NEW.order_number = CONCAT('ORD-', YEAR(NOW()), '-', LPAD(NEW.id, 6, '0'));
END //

CREATE TRIGGER after_order_delete
AFTER DELETE ON orders
FOR EACH ROW
BEGIN
  INSERT INTO order_audit (action, order_id, deleted_at)
  VALUES ('DELETE', OLD.id, NOW());
END //

DELIMITER ;
```

---

## View

**Định nghĩa**: View là virtual table được defined bởi một query. Nó không lưu trữ data thực tế mà luuw trữ definition.

**Ví dụ**:
```sql
-- Simple view
CREATE VIEW active_users AS
SELECT id, name, email
FROM users
WHERE status = 'active' AND deleted_at IS NULL;

-- Complex view with joins
CREATE VIEW order_summary AS
SELECT 
  o.id,
  o.created_at,
  u.name as customer_name,
  u.email,
  COUNT(oi.id) as item_count,
  o.total
FROM orders o
INNER JOIN users u ON o.user_id = u.id
LEFT JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id;

-- Updatable view
CREATE VIEW editable_products AS
SELECT id, name, price, stock
FROM products
WHERE deleted_at IS NULL
WITH CHECK OPTION;
```

---

## Partitioning

**Định nghĩa**: Partitioning chia một large table thành smaller, more manageable pieces gọi là partitions.

**Ví dụ**:
```sql
-- Range partitioning by date
CREATE TABLE orders (
  id INT NOT NULL,
  created_at DATETIME NOT NULL,
  total DECIMAL(10,2),
  PRIMARY KEY (id, created_at)
)
PARTITION BY RANGE (YEAR(created_at)) (
  PARTITION p2022 VALUES LESS THAN (2023),
  PARTITION p2023 VALUES LESS THAN (2024),
  PARTITION p2024 VALUES LESS THAN (2025),
  PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- List partitioning
CREATE TABLE products (
  id INT,
  category VARCHAR(50),
  name VARCHAR(100)
)
PARTITION BY LIST COLUMNS (category) (
  PARTITION p_electronics VALUES IN ('electronics', 'computers'),
  PARTITION p_clothing VALUES IN ('clothing', 'shoes'),
  PARTITION p_other VALUES IN (DEFAULT)
);

-- Hash partitioning
CREATE TABLE logs (
  id BIGINT,
  created_at DATETIME
)
PARTITION BY HASH(id)
PARTITIONS 8;
```

---

## Liên kết liên quan
- [MySQL Architecture](./architecture.md)
- [MySQL Best Practices](./best-practice.md)
- [MySQL Anti-Patterns](./anti-pattern.md)
- [MySQL Checklist](./checklist.md)
- [MySQL FAQ](./faq.md)
- [MySQL Decision Tree](./decision-tree.md)
