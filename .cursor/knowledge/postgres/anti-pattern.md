# PostgreSQL Anti-Patterns - Các Mẫu Thiết Kế Xấu

## Mục lục
1. [Schema Design Anti-Patterns](#1-schema-design-anti-patterns)
2. [Query Anti-Patterns](#2-query-anti-patterns)
3. [Index Anti-Patterns](#3-index-anti-patterns)
4. [Performance Anti-Patterns](#4-performance-anti-patterns)
5. [Security Anti-Patterns](#5-security-anti-patterns)

---

## 1. Schema Design Anti-Patterns

### 1.1 Using CHAR(n) Instead of VARCHAR

**Mô tả**: Sử dụng CHAR(n) cho strings có độ dài không cố định gây lãng phí storage.

**Hậu quả**:
- CHAR(n) luôn pad spaces đến n characters
- VARCHAR(n) chỉ lưu actual bytes
- Storage waste cho data có varying lengths
- Performance degradation khi storage engine pad/trim

**Giải pháp thay thế**:
```sql
-- ❌ BAD: CHAR(50) for variable length data
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username CHAR(50) NOT NULL,  -- Wasteful: "john" becomes "john                                           "
  country CHAR(3)  -- OK for fixed codes like "USA"
);

-- ✅ GOOD: VARCHAR for variable length
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL,  -- Efficient storage
  email VARCHAR(255) NOT NULL,
  bio VARCHAR(1000)  -- For longer text
);

-- ✅ GOOD: Use TEXT when no length limit needed
CREATE TABLE articles (
  id SERIAL PRIMARY KEY,
  title VARCHAR(200),
  content TEXT  -- No practical limit
);
```

### 1.2 Storing Money as FLOAT

**Mô tả**: Sử dụng REAL hoặc DOUBLE PRECISION cho monetary values gây rounding errors.

**Hậu quả**:
- FLOAT không lưu chính xác decimal values
- Accumulated rounding errors trong financial calculations
- 0.1 + 0.2 ≠ 0.3 trong floating point
- Không suitable cho currency calculations

**Giải pháp thay thế**:
```sql
-- ❌ BAD: FLOAT for money
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  price REAL NOT NULL  -- Rounding errors!
);

-- ❌ BAD: Even DOUBLE PRECISION
CREATE TABLE orders (
  total DOUBLE PRECISION NOT NULL  -- Still has precision issues
);

-- ✅ GOOD: DECIMAL/NUMERIC for exact precision
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  price DECIMAL(10,2) NOT NULL  -- Exactly 10 digits, 2 after decimal
);

-- ✅ GOOD: For very large monetary values
CREATE TABLE financial_records (
  id SERIAL PRIMARY KEY,
  amount NUMERIC(15,4) NOT NULL,  -- More precision for calculations
  currency VARCHAR(3) NOT NULL
);

-- Calculations are exact
SELECT 0.1::DECIMAL + 0.2::DECIMAL;  -- Returns 0.3 exactly
```

### 1.3 Over-Normalization

**Mô tả**: Tạo quá nhiều tables với mối quan hệ phức tạp khi không cần thiết.

**Hậu quả**:
- Complex joins cho simple queries
- Performance degradation từ multiple table lookups
- Difficult to maintain and understand
- Over-engineering cho simple use cases

**Giải pháp thay thế**:
```sql
-- ❌ BAD: Over-normalized - too many tables
CREATE TABLE address_types (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50)  -- 'shipping', 'billing'
);

CREATE TABLE countries (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  code CHAR(2)
);

CREATE TABLE states (
  id SERIAL PRIMARY KEY,
  country_id INTEGER REFERENCES countries(id),
  name VARCHAR(100)
);

CREATE TABLE cities (
  id SERIAL PRIMARY KEY,
  state_id INTEGER REFERENCES states(id),
  name VARCHAR(100)
);

CREATE TABLE addresses (
  id SERIAL PRIMARY KEY,
  address_type_id INTEGER REFERENCES address_types(id),
  city_id INTEGER REFERENCES cities(id),
  street VARCHAR(200),
  zip_code VARCHAR(20)
);
-- Too complex for most applications!

-- ✅ GOOD: Simpler design for most cases
CREATE TABLE addresses (
  id SERIAL PRIMARY KEY,
  address_type VARCHAR(20) NOT NULL,  -- 'shipping' or 'billing'
  street VARCHAR(200) NOT NULL,
  city VARCHAR(100),
  state VARCHAR(100),
  country VARCHAR(100),
  country_code CHAR(2),
  zip_code VARCHAR(20)
);

-- Use ENUM if values are fixed
CREATE TYPE address_type AS ENUM ('shipping', 'billing');
CREATE TABLE addresses (
  id SERIAL PRIMARY KEY,
  address_type address_type NOT NULL,
  -- other fields...
);
```

---

## 2. Query Anti-Patterns

### 2.1 Using OR in WHERE Clause

**Mô tả**: Sử dụng OR nhiều lần có thể prevent index usage.

**Hậu quả**:
- OR conditions có thể gây sequential scans
- Kết hợp OR có thể khó optimize
- Performance degradation cho large tables

**Giải pháp thay thế**:
```sql
-- ❌ BAD: Multiple OR conditions
SELECT * FROM orders
WHERE status = 'pending'
   OR status = 'processing'
   OR status = 'shipped'
   OR status = 'delivered';

-- ❌ BAD: OR prevents index usage
SELECT * FROM users
WHERE email = 'test@example.com'
   OR phone = '1234567890';

-- ✅ GOOD: Use IN for multiple values
SELECT * FROM orders
WHERE status IN ('pending', 'processing', 'shipped', 'delivered');

-- ✅ GOOD: Use UNION for different conditions
SELECT * FROM users WHERE email = 'test@example.com'
UNION ALL
SELECT * FROM users WHERE phone = '1234567890';

-- ✅ GOOD: Use UNION with index-friendly conditions
(SELECT * FROM users WHERE email = 'test@example.com')
UNION ALL
(SELECT * FROM users WHERE phone = '1234567890' AND email IS DISTINCT FROM 'test@example.com');

-- ✅ GOOD: Combine with UNION ALL and push down conditions
SELECT * FROM orders WHERE status IN ('pending', 'processing')
UNION ALL
SELECT * FROM orders WHERE status IN ('shipped', 'delivered');
```

### 2.2 Implicit Type Conversion

**Mô tả**: PostgreSQL tự động convert types, có thể prevent index usage.

**Hậu quả**:
- Implicit casts có thể gây sequential scans
- Performance degradation
- Khó debug vì query看起来 valid

**Giải pháp thay thế**:
```sql
-- ❌ BAD: Integer column compared with string
SELECT * FROM orders WHERE user_id = '123';  -- String '123' cast to integer
-- This prevents index use on user_id!

-- ❌ BAD: Date comparison with string
SELECT * FROM orders WHERE created_at = '2024-01-01';  -- String to date cast

-- ✅ GOOD: Match types explicitly
SELECT * FROM orders WHERE user_id = 123;  -- Integer
SELECT * FROM orders WHERE created_at = '2024-01-01'::DATE;
SELECT * FROM orders WHERE created_at = TIMESTAMP '2024-01-01 00:00:00';

-- ✅ GOOD: Use parameterized queries (application level)
-- Parameter :user_id is already integer type
SELECT * FROM orders WHERE user_id = $1;

-- ✅ GOOD: Use date_trunc for date range
SELECT * FROM orders 
WHERE created_at >= '2024-01-01'::DATE 
  AND created_at < '2024-01-02'::DATE;

-- ✅ GOOD: Cast at storage level if needed
ALTER TABLE orders ALTER COLUMN user_id TYPE INTEGER;
```

### 2.3 Function on Indexed Column in WHERE

**Mô tả**: Sử dụng function trên indexed column ngăn cản index usage.

**Hậu quả**:
- Index không được sử dụng
- Sequential scan thay vì index scan
- Performance degradation

**Giải pháp thay thế**:
```sql
-- ❌ BAD: Function on indexed column
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';
-- Index on email cannot be used!

-- ❌ BAD: Math operation on indexed column
SELECT * FROM products WHERE price * 1.1 > 100;

-- ❌ BAD: String function on column
SELECT * FROM orders WHERE SUBSTRING(status, 1, 4) = 'pend';

-- ✅ GOOD: Use expression index
CREATE INDEX idx_users_email_lower ON users (LOWER(email));
-- Now the query can use the index
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';

-- ✅ GOOD: Restructure query
SELECT * FROM products WHERE price > 100 / 1.1;

-- ✅ GOOD: Use functional index with expression
CREATE INDEX idx_orders_status_pending ON orders (created_at) 
WHERE status = 'pending';

-- ✅ GOOD: Pattern matching alternatives
-- Instead of:
SELECT * FROM users WHERE SUBSTRING(phone, 1, 3) = '+84';
-- Use:
SELECT * FROM users WHERE phone LIKE '+84%';
-- Or create an expression index:
CREATE INDEX idx_users_phone_prefix ON users (LEFT(phone, 3));
```

---

## 3. Index Anti-Patterns

### 3.1 Creating Too Many Indexes

**Mô tả**: Tạo indexes cho mọi column hoặc không drop unused indexes.

**Hậu quả**:
- Slow INSERT/UPDATE/DELETE vì tất cả indexes phải update
- Wasted storage space
- VACUUM chậm hơn
- Planner có thể chọn suboptimal index

**Giải pháp thay thế**:
```sql
-- ❌ BAD: Too many indexes
CREATE INDEX idx_orders_id ON orders(id);  -- Primary key already has index
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_total ON orders(total);
CREATE INDEX idx_orders_created ON orders(created_at);
CREATE INDEX idx_orders_updated ON orders(updated_at);
-- All these separate indexes may not be optimal!

-- ✅ GOOD: Composite indexes for common query patterns
-- If you often query: WHERE user_id = ? AND status = ?
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- ✅ GOOD: Covering indexes
CREATE INDEX idx_orders_user_status_cover 
ON orders(user_id, status) INCLUDE (total, created_at);
-- Supports: SELECT total, created_at FROM orders WHERE user_id = ? AND status = ?

-- ✅ GOOD: Partial indexes for specific use cases
CREATE INDEX idx_orders_pending ON orders(created_at) 
WHERE status = 'pending';

-- ✅ GOOD: Monitor and drop unused indexes
SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_write
FROM pg_stat_user_indexes
WHERE idx_scan = 0  -- Never used
ORDER BY pg_relation_size(indexrelid) DESC;

-- Drop unused indexes
DROP INDEX IF EXISTS idx_unused_index;
```

### 3.2 Low-Selectivity Index

**Mô tả**: Index trên columns với few distinct values không cải thiện performance.

**Hậu quả**:
- Index scan có thể chậm hơn sequential scan
- PostgreSQL optimizer bỏ qua index vì selectivity thấp
- Wasted storage và maintenance overhead

**Giải pháp thay thế**:
```sql
-- ❌ BAD: Index on boolean column
CREATE INDEX idx_users_active ON users(is_active);
-- Only 2 values: true/false

-- ❌ BAD: Index on low-cardinality column
CREATE INDEX idx_orders_status ON orders(status);
-- Only 5 status values

-- ✅ GOOD: Use partial index instead
CREATE INDEX idx_users_active_true ON users(created_at) 
WHERE is_active = TRUE;
-- Only indexes active users

-- ✅ GOOD: Composite index with high-selectivity column
CREATE INDEX idx_orders_status_user ON orders(status, user_id);
-- More selective when combined

-- ✅ GOOD: BRIN index for naturally ordered data
CREATE INDEX idx_orders_created_brin ON orders USING brin(created_at);
-- Efficient for time-series data

-- ✅ GOOD: Don't index low-cardinality unless combined
-- If you need to find 'completed' orders frequently:
CREATE INDEX idx_orders_completed ON orders(user_id) 
WHERE status = 'completed';
```

### 3.3 Indexing Before Loading Data

**Mô tả**: Tạo indexes trước khi bulk load data chậm và tốn space.

**Hậu quả**:
- Index phải update sau mỗi row insert
- Load chậm hơn nhiều
- Index files không optimized

**Giải pháp thay thế**:
```sql
-- ❌ BAD: Create indexes before bulk load
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
-- Then bulk insert - SLOW!

-- ✅ GOOD: Drop indexes, load data, recreate indexes
-- 1. Drop indexes
DROP INDEX IF EXISTS idx_orders_user;
DROP INDEX IF EXISTS idx_orders_status;

-- 2. Bulk load data
COPY orders(id, user_id, total, status, created_at) 
FROM '/path/to/orders.csv' WITH (FORMAT csv);

-- 3. Create indexes
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);

-- 4. Rebuild if needed for optimization
REINDEX TABLE orders;

-- ✅ GOOD: Use UNLOGGED table for staging (if safe)
CREATE UNLOGGED TABLE orders_staging (LIKE orders INCLUDING ALL);

-- Load data to staging
COPY orders_staging FROM '/path/to/orders.csv' WITH (FORMAT csv);

-- Add indexes to staging
CREATE INDEX ON orders_staging(user_id);

-- Insert from staging to main table
INSERT INTO orders SELECT * FROM orders_staging;

-- Clean up
DROP TABLE orders_staging;
```

---

## 4. Performance Anti-Patterns

### 4.1 Not Using EXPLAIN ANALYZE

**Mô tả**: Không kiểm tra query plan trước khi deploy.

**Hậu quả**:
- Không biết queries có sử dụng indexes không
- Production performance issues
- Khó debug slow queries

**Giải pháp thay thế**:
```sql
-- ✅ GOOD: Always EXPLAIN ANALYZE before deploying
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > NOW() - INTERVAL '30 days'
GROUP BY u.id;

-- ✅ GOOD: Check for sequential scans on large tables
-- Bad: Seq Scan on large_table (cost=0.00..1000000.00 rows=10000000)
-- Good: Index Scan using idx_column on large_table

-- ✅ GOOD: Look for high actual vs estimated rows
-- If actual rows >> estimated rows, statistics might be stale
ANALYZE users;
ANALYZE orders;

-- ✅ GOOD: Use pg_stat_statements to find slow queries
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 20;
```

### 4.2 Not Using Connection Pooling

**Mô tả**: Mỗi request tạo new database connection.

**Hậu quả**:
- Connection overhead cho mỗi request
- Connection limit exhaustion
- Memory bloat từ many connections
- Poor performance under load

**Giải pháp thay thế**:
```sql
-- ❌ BAD: Direct connections
-- Application connects directly to PostgreSQL
-- Every request creates new connection (expensive!)

-- ✅ GOOD: Use connection pooler (pgbouncer/pgpool)
-- pgbouncer.ini
[databases]
shop = host=127.0.0.1 port=5432 dbname=shop

[pgbouncer]
listen_port = 6432
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 50

-- Application connects to pgbouncer
-- Connections are reused efficiently

-- ✅ GOOD: Configure PostgreSQL for expected load
-- postgresql.conf
max_connections = 100  -- Reasonable for pooling
shared_buffers = 4GB  -- 25% of RAM
effective_cache_size = 12GB  -- 75% of RAM
work_mem = 64MB  -- Per operation, not per connection
maintenance_work_mem = 256MB
```

### 4.3 Not Vacuuming Regularly

**Mô tąc**: Dead tuples accumulate và statistics become stale.

**Hậu quả**:
- Table bloat tăng storage
- Slow queries vì dead tuples
- Statistics inaccurate → bad query plans
- Transaction ID wraparound risk

**Giải pháp thay thế**:
```sql
-- ✅ GOOD: Configure autovacuum properly
ALTER TABLE orders SET (
  autovacuum_vacuum_scale_factor = 0.01,  -- Vacuum when 1% dead tuples
  autovacuum_analyze_scale_factor = 0.005,
  autovacuum_vacuum_cost_delay = 10  -- ms
);

-- ✅ GOOD: Monitor table bloat
SELECT relname, n_dead_tup, n_live_tup, 
       ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) as dead_pct,
       last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- ✅ GOOD: Manual VACUUM when needed
VACUUM (VERBOSE, ANALYZE) orders;

-- ✅ GOOD: VACUUM FULL for severely bloated tables (requires exclusive lock)
VACUUM FULL orders;

-- Or use pg_repack for online table reorganization
SELECT * FROM pg_repack.repack_table('orders');
```

---

## 5. Security Anti-Patterns

### 5.1 Storing Passwords in Plain Text

**Mô tả**: Lưu trữ passwords không hashed.

**Hậu quả**:
- Security breach reveals all passwords
- Legal/regulatory compliance issues
- User trust issues

**Giải pháp thay thế**:
```sql
-- ❌ BAD: Plain text password
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50),
  password VARCHAR(255)  -- Stored in plain text!
);

-- ✅ GOOD: Hash passwords with pgcrypto
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50),
  password_hash CHAR(60) NOT NULL  -- bcrypt output
);

-- Hash on insert
INSERT INTO users (username, password_hash)
VALUES ('john', crypt('secret123', gen_salt('bf')));

-- Verify on login
SELECT * FROM users 
WHERE username = 'john' 
  AND password_hash = crypt('secret123', password_hash);

-- ✅ GOOD: Use SCRAM-SHA-256 (PostgreSQL default)
-- PostgreSQL handles password hashing automatically
ALTER SYSTEM SET password_encryption = 'scram-sha-256';
SELECT pg_reload_conf();

CREATE USER app_user WITH PASSWORD 'secure_password';
```

### 5.2 SQL Injection Vulnerability

**Mô tả**: Concatenating user input directly vào SQL queries.

**Hậu quả**:
- Attacker có thể execute arbitrary SQL
- Data breach, data loss
- System compromise

**Giải pháp thay thế**:
```sql
-- ❌ BAD: String concatenation
-- In application code:
query = "SELECT * FROM users WHERE id = " + userId;
-- Attacker: userId = "1; DROP TABLE users;"

-- ❌ BAD: Format string
query = sprintf("SELECT * FROM users WHERE name = '%s'", username);
-- Attacker: username = "'; DROP TABLE users; --"

-- ✅ GOOD: Parameterized queries
-- In application code:
query = "SELECT * FROM users WHERE id = $1";
-- Parameters: [userId]

-- ✅ GOOD: Use GIN arrays for search
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Application sanitizes and validates input
-- Use ORM that handles SQL injection

-- ✅ GOOD: Input validation at application level
function validateUserId(id) {
  if (!Number.isInteger(id)) {
    throw new Error('Invalid user ID');
  }
  if (id < 1 || id > 2147483647) {
    throw new Error('User ID out of range');
  }
  return id;
}
```

### 5.3 Over-Privileged Database Roles

**Mô tả**: Application sử dụng superuser hoặc overly permissive roles.

**Hậu quả**:
- Security breach có full database access
- Compliance violations
- Accidental destructive operations

**Giải pháp thay thế**:
```sql
-- ❌ BAD: Application uses superuser
CREATE ROLE app_admin SUPERUSER CREATEDB CREATEROLE;

-- ❌ BAD: Grant everything
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;

-- ✅ GOOD: Minimal privileges
CREATE ROLE app_user LOGIN PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE shop TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- ✅ GOOD: Revoke dangerous privileges
REVOKE ALL ON DATABASE shop FROM PUBLIC;
REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA public FROM PUBLIC;

-- ✅ GOOD: Separate roles for different functions
CREATE ROLE app_readonly LOGIN PASSWORD 'readonly_password';
GRANT CONNECT ON DATABASE shop TO app_readonly;
GRANT USAGE ON SCHEMA public TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;
```

---

## Liên kết liên quan
- [PostgreSQL Glossary](./glossary.md)
- [PostgreSQL Architecture](./architecture.md)
- [PostgreSQL Best Practices](./best-practice.md)
- [PostgreSQL Checklist](./checklist.md)
- [PostgreSQL FAQ](./faq.md)
- [PostgreSQL Decision Tree](./decision-tree.md)
