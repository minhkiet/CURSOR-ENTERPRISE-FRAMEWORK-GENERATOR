# PostgreSQL Best Practices - Các Thực Hành Tốt Nhất

## Mục lục
1. [Schema Design](#1-schema-design)
2. [Indexing](#2-indexing)
3. [Query Optimization](#3-query-optimization)
4. [Performance Tuning](#4-performance-tuning)
5. [Security](#5-security)

---

## 1. Schema Design

### 1.1 Use Appropriate Data Types

**Mô tả**: Chọn data types phù hợp để optimize storage và ensure data integrity.

**Ví dụ**:
```sql
-- ✅ GOOD: Appropriate types
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(20),  -- VARCHAR, not CHAR
  birth_date DATE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  balance DECIMAL(10,2) DEFAULT 0,  -- For money
  is_active BOOLEAN DEFAULT TRUE,
  status VARCHAR(20) DEFAULT 'pending',
  metadata JSONB  -- For flexible data
);

-- ✅ GOOD: Use domains for business rules
CREATE DOMAIN positive_int AS INTEGER CHECK (VALUE > 0);
CREATE DOMAIN email_address AS VARCHAR(255) 
  CHECK (VALUE ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

CREATE TABLE orders (
  quantity positive_int NOT NULL,
  customer_email email_address NOT NULL
);
```

### 1.2 Use UUIDs Appropriately

**Mô tả**: UUIDs cung cấp global uniqueness nhưng có trade-offs về storage và performance.

**Ví dụ**:
```sql
-- ✅ GOOD: UUID v7 for time-ordered UUIDs (PostgreSQL 17+)
CREATE EXTENSION IF NOT EXISTS "pg_uuidv7";

CREATE TABLE distributed_records (
  id UUID DEFAULT uuid_generate_v7() PRIMARY KEY,
  name VARCHAR(100)
);

-- ✅ GOOD: UUID v4 for general use
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name VARCHAR(100)
);

-- ⚠️ Consider: UUIDs add 16 bytes vs 4 bytes for SERIAL
-- Use SERIAL for simple, local-only IDs
-- Use UUID for distributed systems or external references
```

### 1.3 Use JSONB for Semi-Structured Data

**Mô tả**: JSONB lưu trữ binary representation với indexes support, tốt hơn JSON text.

**Ví dụ**:
```sql
-- ✅ GOOD: JSONB for flexible data
CREATE TABLE events (
  id SERIAL PRIMARY KEY,
  event_type VARCHAR(50) NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create GIN index for JSONB queries
CREATE INDEX idx_events_payload ON events USING gin (payload);

-- Query JSONB efficiently
SELECT * FROM events 
WHERE payload @> '{"user_id": 123}';
SELECT * FROM events 
WHERE payload ->> 'action' = 'purchase';

-- Add JSONB column for event sourcing
ALTER TABLE orders ADD COLUMN metadata JSONB DEFAULT '{}';
```

---

## 2. Indexing

### 2.1 Use Partial Indexes

**Mô tả**: Partial indexes chỉ index một subset của rows, tiết kiệm space và improve performance.

**Ví dụ**:
```sql
-- ✅ GOOD: Index only active users
CREATE INDEX idx_users_active ON users (email) 
WHERE is_active = TRUE;

-- ✅ GOOD: Index pending orders
CREATE INDEX idx_orders_pending ON orders (created_at) 
WHERE status = 'pending';

-- ✅ GOOD: Index expensive queries
CREATE INDEX idx_products_electronics 
ON products (category, price) 
WHERE category = 'electronics';

-- Query uses partial index
SELECT * FROM orders 
WHERE status = 'pending' 
ORDER BY created_at LIMIT 10;
```

### 2.2 Use Composite Indexes Effectively

**Mô tả**: Composite indexes có thể cover nhiều query patterns nhưng column order matters.

**Ví dụ**:
```sql
-- Query: WHERE user_id = ? AND status = ? ORDER BY created_at DESC
-- ✅ GOOD: Match query pattern
CREATE INDEX idx_orders_user_status_date 
ON orders (user_id, status, created_at DESC);

-- ✅ GOOD: Covering index with INCLUDE
CREATE INDEX idx_orders_user_status 
ON orders (user_id, status) 
INCLUDE (total, created_at);

-- Query: SELECT total FROM orders WHERE user_id = ? AND status = 'pending'
-- ✅ GOOD: Index only needed columns
CREATE INDEX idx_orders_total 
ON orders (user_id) 
INCLUDE (total) 
WHERE status = 'pending';
```

### 2.3 Use Expression Indexes

**Mô tả**: Index computed expressions để improve queries sử dụng functions.

**Ví dụ**:
```sql
-- ✅ GOOD: Index lowercased email
CREATE INDEX idx_users_email_lower ON users (LOWER(email));

-- Query uses expression index
SELECT * FROM users WHERE LOWER(email) = LOWER('Test@Email.Com');

-- ✅ GOOD: Index date extraction
CREATE INDEX idx_orders_month ON orders (DATE_TRUNC('month', created_at));

-- Query uses expression index
SELECT DATE_TRUNC('month', created_at) as month, SUM(total)
FROM orders
GROUP BY DATE_TRUNC('month', created_at);

-- ✅ GOOD: Index for case-insensitive search
CREATE INDEX idx_products_name_lower ON products (LOWER(name));
```

---

## 3. Query Optimization

### 3.1 Use EXPLAIN ANALYZE

**Mô tả**: EXPLAIN ANALYZE hiển thị actual execution plan với timing.

**Ví dụ**:
```sql
-- ✅ GOOD: Analyze query with timing
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > NOW() - INTERVAL '30 days'
GROUP BY u.id;

-- Sample output:
-- Hash Left Join  (cost=1000.00..5000.00 rows=10000 width=40)
--   (actual time=10.5..50.2 rows=5000 loops=1)
--   Buffers: shared hit=500 read=100
--   -> Seq Scan on users  (cost=0.00..3000.00 rows=10000 width=20)
```

### 3.2 Avoid SELECT *

**Mô tả**: Chỉ select columns cần thiết để improve performance và enable index-only scans.

**Ví dụ**:
```sql
-- ❌ BAD: SELECT *
SELECT * FROM users WHERE id = 1;

-- ✅ GOOD: Specific columns
SELECT id, username, email FROM users WHERE id = 1;

-- ✅ GOOD: Index-only scan possible
SELECT id, email FROM users WHERE email = 'test@example.com';

-- ✅ GOOD: Count only
SELECT COUNT(*) FROM orders WHERE status = 'completed';
-- Uses index, doesn't need to fetch rows
```

### 3.3 Use Window Functions

**Mô tả**: Window functions cung cấp powerful analytics mà không cần self-joins.

**Ví dụ**:
```sql
-- ✅ GOOD: Running total
SELECT 
  id,
  total,
  SUM(total) OVER (ORDER BY created_at) as running_total
FROM orders;

-- ✅ GOOD: Rank within group
SELECT 
  name,
  total,
  RANK() OVER (ORDER BY total DESC) as rank
FROM users u
JOIN (
  SELECT user_id, SUM(total) as total 
  FROM orders 
  GROUP BY user_id
) o ON u.id = o.user_id;

-- ✅ GOOD: Moving average
SELECT 
  created_at,
  total,
  AVG(total) OVER (
    ORDER BY created_at 
    ROWS BETWEEN 7 PRECEDING AND CURRENT ROW
  ) as moving_avg_7_days
FROM orders;
```

---

## 4. Performance Tuning

### 4.1 Configure work_mem Appropriately

**Mô tả**: work_mem control memory cho sorting và hashing operations.

**Ví dụ**:
```sql
-- ✅ GOOD: Set per-session for large sorts
SET work_mem = '256MB';

-- Sort operation uses work_mem
SELECT * FROM large_table ORDER BY created_at DESC;

-- Complex query with multiple sorts
SET work_mem = '512MB';
SELECT * FROM (
  SELECT * FROM orders ORDER BY total
) o1
UNION ALL
SELECT * FROM (
  SELECT * FROM orders ORDER BY created_at
) o2;

-- Reset to default
RESET work_mem;
```

### 4.2 Use Materialized Views for Expensive Queries

**Mô tả**: Materialized views store results của expensive queries để reuse.

**Ví dụ**:
```sql
-- ✅ GOOD: Create materialized view
CREATE MATERIALIZED VIEW monthly_revenue AS
SELECT 
  DATE_TRUNC('month', created_at) as month,
  COUNT(*) as order_count,
  SUM(total) as revenue
FROM orders
GROUP BY DATE_TRUNC('month', created_at)
WITH DATA;

-- Create unique index for efficient refresh
CREATE UNIQUE INDEX idx_monthly_revenue_month 
ON monthly_revenue(month);

-- Query from materialized view (fast!)
SELECT * FROM monthly_revenue ORDER BY month DESC;

-- Refresh when data changes
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_revenue;

-- Automatic refresh with pg_cron
SELECT cron.schedule(
  'refresh-monthly-revenue',
  '0 0 * * *',  -- Daily at midnight
  'REFRESH MATERIALIZED VIEW monthly_revenue'
);
```

### 4.3 Use Connection Pooling

**Mô tả**: Connection pooling giảm overhead của creating new connections.

**Ví dụ**:
```sql
-- pgBancer configuration (pgbouncer.ini)
[databases]
shop = host=127.0.0.1 port=5432 dbname=shop

[pgbouncer]
listen_port = 6432
listen_addr = 127.0.0.1
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20

-- Application connects to pgbouncer (port 6432)
-- Instead of PostgreSQL directly (port 5432)
-- Reduces connection overhead significantly
```

---

## 5. Security

### 5.1 Use Row-Level Security

**Mô tả**: RLS enforce access control at row level trong database.

**Ví dụ**:
```sql
-- ✅ GOOD: Enable RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own orders
CREATE POLICY orders_user_policy ON orders
  FOR ALL
  USING (user_id = current_user_id());

-- Policy: Users can only see active records
CREATE POLICY orders_active_policy ON orders
  FOR SELECT
  USING (is_active = TRUE);

-- Now queries automatically filter
-- SELECT * FROM orders;  -- Only returns user's orders
-- DELETE FROM orders WHERE id = 5;  -- Only deletes user's orders
```

### 5.2 Use GRANT Effectively

**Mô tả**: Apply principle of least privilege với proper grants.

**Ví dụ**:
```sql
-- ✅ GOOD: Application role with limited permissions
CREATE ROLE app_user LOGIN PASSWORD 'secure_password';

-- Grant only needed permissions
GRANT CONNECT ON DATABASE shop_db TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- ✅ GOOD: Read-only role
CREATE ROLE app_reader LOGIN PASSWORD 'reader_password';
GRANT CONNECT ON DATABASE shop_db TO app_reader;
GRANT USAGE ON SCHEMA public TO app_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_reader;

-- Revoke dangerous permissions
REVOKE ALL ON DATABASE shop_db FROM PUBLIC;
```

### 5.3 Encrypt Sensitive Data

**Mô tả**: Sử dụng pgcrypto để encrypt sensitive columns.

**Ví dụ**:
```sql
-- ✅ GOOD: Encrypt at application level with separate key
-- Store encrypted data
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  ssn_encrypted BYTEA NOT NULL
);

-- Encrypt on insert
INSERT INTO users (ssn_encrypted) 
VALUES (pgp_sym_encrypt('123-45-6789', 'encryption_key'));

-- Decrypt on select
SELECT id, pgp_sym_decrypt(ssn_encrypted::BYTEA, 'encryption_key') as ssn 
FROM users;

-- ✅ GOOD: Use for columns with sensitive data
ALTER TABLE users ADD COLUMN credit_card_encrypted BYTEA;
ALTER TABLE users ADD COLUMN health_record_encrypted BYTEA;
```

---

## Liên kết liên quan
- [PostgreSQL Glossary](./glossary.md)
- [PostgreSQL Architecture](./architecture.md)
- [PostgreSQL Anti-Patterns](./anti-pattern.md)
- [PostgreSQL Checklist](./checklist.md)
- [PostgreSQL FAQ](./faq.md)
- [PostgreSQL Decision Tree](./decision-tree.md)
