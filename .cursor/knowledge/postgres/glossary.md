# PostgreSQL Glossary - Thuật Ngữ Chuyên Ngành

## Mục lục
1. [Database Objects](#1-database-objects)
2. [Data Types](#2-data-types)
3. [Index Types](#3-index-types)
4. [Query Operations](#4-query-operations)
5. [Transactions](#5-transactions)
6. [Advanced Features](#6-advanced-features)

---

## Database

**Định nghĩa**: Database là container cấp cao nhất chứa schemas, tables, views, và các objects khác trong PostgreSQL.

**Ví dụ**:
```sql
-- Create database
CREATE DATABASE shop_db
  WITH ENCODING 'UTF8'
  LC_COLLATE = 'en_US.UTF-8'
  LC_CTYPE = 'en_US.UTF-8'
  TEMPLATE template0;

-- Connect to database
\c shop_db

-- List databases
SELECT datname FROM pg_database WHERE datistemplate = false;

-- Drop database
DROP DATABASE IF EXISTS old_db;
```

---

## Schema

**Định nghĩa**: Schema là namespace chứa tables, views, functions, và other objects. Default schema là 'public'.

**Ví dụ**:
```sql
-- Create schema
CREATE SCHEMA inventory;

-- Create schema with authorization
CREATE SCHEMA orders AUTHORIZATION app_user;

-- Set search path
SET search_path TO inventory, public;

-- Create table in schema
CREATE TABLE inventory.products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  quantity INTEGER DEFAULT 0
);

-- Access with schema prefix
SELECT * FROM inventory.products;
```

---

## Table

**Định nghĩa**: Table là cấu trúc dữ liệu cơ bản trong PostgreSQL, chứa rows và columns với constraints và indexes.

**Ví dụ**:
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL,
  password_hash CHAR(60) NOT NULL,
  role VARCHAR(20) DEFAULT 'user',
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table with constraints
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  total DECIMAL(10,2) NOT NULL DEFAULT 0,
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  CONSTRAINT orders_total_positive CHECK (total >= 0),
  CONSTRAINT orders_status_valid CHECK (
    status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')
  )
);
```

---

## Primary Key

**Định nghĩa**: Primary Key là column hoặc set of columns uniquely identify mỗi row trong table. PostgreSQL tự động tạo unique index.

**Ví dụ**:
```sql
-- Single column primary key
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  -- ...
);

-- Composite primary key
CREATE TABLE order_items (
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL DEFAULT 1,
  
  PRIMARY KEY (order_id, product_id)
);

-- Add primary key to existing table
ALTER TABLE users ADD PRIMARY KEY (id);
```

---

## Foreign Key

**Định nghĩa**: Foreign Key enforce referential integrity bằng cách đảm bảo values trong column tham chiếu đến existing rows trong table khác.

**Ví dụ**:
```sql
-- Basic foreign key
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  -- ...
);

-- Foreign key with actions
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',
  
  CONSTRAINT fk_user
    FOREIGN KEY (user_id) 
    REFERENCES users(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

-- Self-referencing foreign key
CREATE TABLE employees (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  manager_id INTEGER REFERENCES employees(id)
);
```

---

## Index

**Định nghĩa**: Index là cấu trúc dữ liệu cải thiện tốc độ truy xuất data. PostgreSQL support nhiều loại index types.

**Ví dụ**:
```sql
-- B-tree index (default)
CREATE INDEX idx_users_email ON users(email);

-- Unique index
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Composite index
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial index
CREATE INDEX idx_orders_pending ON orders(created_at) 
WHERE status = 'pending';

-- Expression index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Covering index (INCLUDE)
CREATE INDEX idx_orders_user ON orders(user_id) INCLUDE (status, total);
```

---

## SELECT

**Định nghĩa**: SELECT truy vấn data từ một hoặc nhiều tables với filtering, sorting, và aggregation.

**Ví dụ**:
```sql
-- Basic select
SELECT id, name, email FROM users WHERE is_active = TRUE;

-- Join with aliases
SELECT o.id, u.name, u.email, o.total
FROM orders o
INNER JOIN users u ON o.user_id = u.id
WHERE o.status = 'delivered'
ORDER BY o.created_at DESC
LIMIT 10 OFFSET 0;

-- Window function
SELECT 
  o.id,
  u.name,
  o.total,
  SUM(o.total) OVER (PARTITION BY u.id) as user_total,
  RANK() OVER (ORDER BY o.total DESC) as order_rank
FROM orders o
INNER JOIN users u ON o.user_id = u.id;

-- Common Table Expression (CTE)
WITH recent_orders AS (
  SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '30 days'
)
SELECT u.name, COUNT(o.id) as order_count, SUM(o.total) as total_spent
FROM users u
LEFT JOIN recent_orders o ON u.id = o.user_id
GROUP BY u.id;
```

---

## JOIN

**Định nghĩa**: JOIN kết hợp rows từ multiple tables dựa trên related columns.

**Ví dụ**:
```sql
-- INNER JOIN
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

-- RIGHT JOIN
SELECT u.name, o.total
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;

-- CROSS JOIN (cartesian product)
SELECT u.name, p.name
FROM users u
CROSS JOIN products p;

-- LATERAL JOIN
SELECT u.name, top_orders.order_count
FROM users u
CROSS JOIN LATERAL (
  SELECT COUNT(*) as order_count
  FROM orders o
  WHERE o.user_id = u.id
) as top_orders;
```

---

## GROUP BY

**Định nghĩa**: GROUP BY nhóm rows theo columns để tính toán aggregates.

**Ví dụ**:
```sql
-- Basic group by
SELECT 
  user_id,
  COUNT(*) as order_count,
  SUM(total) as total_spent,
  AVG(total) as avg_order_value,
  MAX(total) as max_order,
  MIN(total) as min_order
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 5
ORDER BY total_spent DESC;

-- Group by with filtering
SELECT 
  DATE_TRUNC('day', created_at) as day,
  COUNT(*) as orders,
  SUM(total) as revenue
FROM orders
WHERE created_at >= DATE_TRUNC('month', NOW())
GROUP BY DATE_TRUNC('day', created_at)
ORDER BY day;
```

---

## Transaction

**Định nghĩa**: Transaction là atomic unit of work đảm bảo ACID properties.

**Ví dụ**:
```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Check constraints
IF (SELECT balance FROM accounts WHERE id = 1) < 0 THEN
  ROLLBACK;
ELSE
  COMMIT;
END IF;

-- Savepoint
SAVEPOINT before_update;
UPDATE users SET name = 'New Name' WHERE id = 1;
ROLLBACK TO SAVEPOINT before_update;
COMMIT;
```

---

## MVCC

**Định nghĩa**: Multi-Version Concurrency Control cho phép concurrent transactions không blocking nhau bằng cách maintain multiple versions của rows.

**Ví dụ**:
```sql
-- Default isolation level (READ COMMITTED)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Serializable for stricter isolation
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Read uncommitted (allows dirty reads - not recommended)
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

-- Repeatable read
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

---

## VACUUM

**Định nghĩa**: VACUUM reclaim storage space từ deleted/updated rows và update statistics.

**Ví dụ**:
```sql
-- Regular vacuum
VACUUM;

-- Vacuum specific table
VACUUM users;

-- Vacuum and analyze
VACUUM ANALYZE;

-- Vacuum all databases
VACUUM FULL;

-- Autovacuum configuration
ALTER TABLE orders SET (
  autovacuum_vacuum_scale_factor = 0.02,
  autovacuum_analyze_scale_factor = 0.01
);
```

---

## EXPLAIN

**Định nghĩa**: EXPLAIN hiển thị execution plan của query.

**Ví dụ**:
```sql
-- Basic explain
EXPLAIN SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

-- Explain with costs
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE status = 'pending';

-- Explain JSON format
EXPLAIN (FORMAT JSON)
SELECT * FROM users WHERE email = 'test@example.com';
```

---

## Stored Procedure

**Định nghĩa**: Stored Procedure là named collection of SQL statements được stored và có thể được gọi.

**Ví dụ**:
```sql
CREATE OR REPLACE FUNCTION get_user_orders(
  p_user_id INTEGER,
  OUT order_count INTEGER,
  OUT total_amount DECIMAL
)
RETURNS RECORD AS $$
BEGIN
  SELECT COUNT(*), COALESCE(SUM(total), 0)
  INTO order_count, total_amount
  FROM orders
  WHERE user_id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- Call function
SELECT * FROM get_user_orders(1);
```

---

## Trigger

**Định nghĩa**: Trigger là function được execute tự động khi DML event xảy ra.

**Ví dụ**:
```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

-- Trigger for audit log
CREATE OR REPLACE FUNCTION audit_log()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_log (table_name, action, old_data, new_data, changed_at)
  VALUES (TG_TABLE_NAME, TG_OP, OLD, NEW, NOW());
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;
```

---

## View

**Định nghĩa**: View là virtual table được defined bởi query, không lưu trữ data.

**Ví dụ**:
```sql
-- Simple view
CREATE VIEW active_users AS
SELECT id, username, email
FROM users
WHERE is_active = TRUE;

-- Materialized view (stores data)
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT 
  DATE_TRUNC('month', created_at) as month,
  COUNT(*) as orders,
  SUM(total) as revenue
FROM orders
GROUP BY DATE_TRUNC('month', created_at)
WITH DATA;

REFRESH MATERIALIZED VIEW monthly_sales;

-- Updatable view
CREATE VIEW pending_orders AS
SELECT * FROM orders WHERE status = 'pending';

INSERT INTO pending_orders (user_id, total) VALUES (1, 100);
```

---

## Partitioning

**Định nghĩa**: Partitioning chia table thành smaller pieces gọi là partitions.

**Ví dụ**:
```sql
-- Range partitioning
CREATE TABLE orders (
  id SERIAL,
  user_id INTEGER NOT NULL,
  total DECIMAL(10,2),
  created_at TIMESTAMP WITH TIME ZONE,
  PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2024_01 PARTITION OF orders
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE orders_2024_02 PARTITION OF orders
  FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- List partitioning
CREATE TABLE products (
  id SERIAL,
  category VARCHAR(50),
  name VARCHAR(100)
) PARTITION BY LIST (category);

CREATE TABLE products_electronics PARTITION OF products
  FOR VALUES IN ('electronics', 'computers');
```

---

## Liên kết liên quan
- [PostgreSQL Architecture](./architecture.md)
- [PostgreSQL Best Practices](./best-practice.md)
- [PostgreSQL Anti-Patterns](./anti-pattern.md)
- [PostgreSQL Checklist](./checklist.md)
- [PostgreSQL FAQ](./faq.md)
- [PostgreSQL Decision Tree](./decision-tree.md)
