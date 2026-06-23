# PostgreSQL FAQ - Câu Hỏi Thường Gặp

## Mục lục
1. [General Questions](#1-general-questions)
2. [Schema & Tables](#2-schema--tables)
3. [Indexes](#3-indexes)
4. [Performance](#4-performance)
5. [Replication & HA](#5-replication--ha)
6. [Security](#6-security)

---

## 1. General Questions

### Q1: SERIAL vs UUID - Nên dùng cái nào?

**Trả lời**: SERIAL (hoặc BIGSERIAL) là lựa chọn tốt cho hầu hết applications, trong khi UUID phù hợp cho distributed systems hoặc khi cần merge data từ nhiều sources.

**Khi nào dùng SERIAL**:
- Single database instance
- Sequential IDs acceptable
- Performance important
- URL-safe IDs acceptable

**Khi nào dùng UUID**:
- Distributed systems
- Data merging from multiple sources
- External API references
- Security through obscurity (non-guessable IDs)

**Ví dụ**:
```sql
-- SERIAL (simple, efficient)
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  total DECIMAL(10,2)
);
-- Insert returns ID
INSERT INTO orders (total) VALUES (100) RETURNING id;

-- UUID v4 (random)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE TABLE distributed_orders (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  total DECIMAL(10,2)
);

-- UUID v7 (time-ordered, PostgreSQL 17+)
CREATE EXTENSION IF NOT EXISTS "pg_uuidv7";
CREATE TABLE time_ordered_records (
  id UUID DEFAULT uuid_generate_v7() PRIMARY KEY,
  data TEXT
);
```

### Q2: VARCHAR(n) vs TEXT vs CHAR - Khác nhau gì?

**Trả lời**: 
- `VARCHAR(n)` và `TEXT` có performance gần như tương đương trong PostgreSQL. `CHAR(n)` pad spaces nên lãng phí storage cho variable-length data.

**So sánh chi tiết**:
```sql
-- VARCHAR(n): Variable length, max n characters
CREATE TABLE t1 (name VARCHAR(50));  -- Efficient

-- TEXT: Variable length, no limit
CREATE TABLE t2 (content TEXT);  -- Same performance as VARCHAR

-- CHAR(n): Fixed length, padded with spaces
CREATE TABLE t3 (code CHAR(10));  -- Inefficient for variable data

-- Storage comparison
-- 'hello' stored as CHAR(10): 'hello     ' (10 bytes)
-- 'hello' stored as VARCHAR(10): 'hello' (5 bytes)

-- Recommendation: Use VARCHAR or TEXT, avoid CHAR
CREATE TABLE users (
  username VARCHAR(50) NOT NULL,  -- For short text
  bio TEXT,  -- For longer text
  country_code CHAR(2)  -- Only for fixed-length codes
);
```

### Q3: SINGLE vs MULTI-STATEMENT Transactions - Cái nào tốt hơn?

**Trả lời**: Sử dụng multi-statement transactions (BEGIN...COMMIT) cho data integrity và rollback capability. Single statements chỉ phù hợp cho simple, independent operations.

**Ví dụ**:
```sql
-- ✅ Multi-statement transaction (recommended)
BEGIN;

-- Multiple related operations
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
INSERT INTO transactions (from_account, to_account, amount) VALUES (1, 2, 100);

-- All or nothing
COMMIT;  -- Or ROLLBACK on error

-- ✅ Error handling in transaction
DO $$
BEGIN
  BEGIN
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    IF (SELECT balance FROM accounts WHERE id = 1) < 0 THEN
      RAISE EXCEPTION 'Insufficient funds';
    END IF;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
    COMMIT;
  EXCEPTION WHEN OTHERS THEN
    ROLLBACK;
    RAISE;
  END;
END $$;

-- Single statement (OK for simple operations)
INSERT INTO audit_log (action) VALUES ('user_login');
```

---

## 2. Schema & Tables

### Q4: Làm thế nào để thêm column an toàn?

**Trả lời**: Sử dụng `ALTER TABLE ... ADD COLUMN` với DEFAULT value hoặc nullable column để tránh table rewrite và lock issues.

**Ví dụ**:
```sql
-- ✅ Safe: Add nullable column (no table rewrite)
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- ✅ Safe: Add column with default in PostgreSQL 11+
ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active';
-- PostgreSQL 11+ doesn't rewrite table for DEFAULT with constant

-- ⚠️ Careful: Adding column with non-constant default may rewrite table
ALTER TABLE users ADD COLUMN counter INTEGER DEFAULT 0;
-- Before PostgreSQL 11: rewrites entire table (locks writes)

-- ✅ For large tables, use multiple steps
-- Step 1: Add nullable column
ALTER TABLE orders ADD COLUMN metadata JSONB;
-- Step 2: Backfill in batches
UPDATE orders SET metadata = '{}'::JSONB WHERE metadata IS NULL LIMIT 10000;
-- Step 3: Add NOT NULL after backfill
ALTER TABLE orders ALTER COLUMN metadata SET NOT NULL;

-- ✅ Use concurrent operation for production
ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(20);
```

### Q5: Soft Delete vs Hard Delete - Nên dùng cái nào?

**Trả lời**: Soft delete phù hợp cho business records cần audit trail và potential recovery. Hard delete phù hợp cho temporary data hoặc privacy compliance.

**Ví dụ**:
```sql
-- ✅ Soft Delete pattern
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  total DECIMAL(10,2),
  deleted_at TIMESTAMP WITH TIME ZONE,  -- Soft delete column
  CONSTRAINT orders_deleted CHECK (deleted_at IS NOT NULL OR status != 'cancelled')
);

-- Soft delete
UPDATE orders SET deleted_at = NOW() WHERE id = 123;

-- Query active records only
SELECT * FROM orders WHERE deleted_at IS NULL;

-- Create partial index for performance
CREATE INDEX idx_orders_active ON orders(user_id) WHERE deleted_at IS NULL;

-- ✅ Hard Delete (when needed)
DELETE FROM temp_sessions WHERE expires_at < NOW();

-- ✅ Recover soft-deleted records
UPDATE orders SET deleted_at = NULL WHERE id = 123;

-- ✅ Cascade soft delete (trigger)
CREATE OR REPLACE FUNCTION soft_delete_orders()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE order_items SET deleted_at = NEW.deleted_at WHERE order_id = OLD.id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_soft_delete_order_items
  AFTER UPDATE ON orders
  FOR EACH ROW
  WHEN (NEW.deleted_at IS DISTINCT FROM OLD.deleted_at)
  EXECUTE FUNCTION soft_delete_orders();
```

### Q6: ARRAY vs JSONB - Khi nào dùng cái nào?

**Trả lờa**: ARRAY phù hợp cho homogeneous, simple data với known structure. JSONB phù hợp cho heterogeneous, complex data với flexible schema.

**Ví dụ**:
```sql
-- ✅ ARRAY for simple lists
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  tags TEXT[]  -- Simple string array
);

-- Query array
INSERT INTO products (name, tags) VALUES ('Laptop', ARRAY['electronics', 'computers']);

SELECT * FROM products WHERE 'electronics' = ANY(tags);
SELECT * FROM products WHERE tags && ARRAY['electronics'];

-- ✅ JSONB for complex data
CREATE TABLE events (
  id SERIAL PRIMARY KEY,
  event_type VARCHAR(50),
  payload JSONB
);

-- Query JSONB
INSERT INTO events (event_type, payload) VALUES (
  'user_action',
  '{"user_id": 123, "action": "purchase", "items": [{"sku": "A1", "qty": 2}]}'
);

SELECT * FROM events WHERE payload @> '{"user_id": 123}';
SELECT payload->>'action' FROM events WHERE payload->>'action' = 'purchase';

-- ✅ Performance: Both support indexes
CREATE INDEX idx_products_tags ON products USING gin(tags);
CREATE INDEX idx_events_payload ON events USING gin(payload);
```

---

## 3. Indexes

### Q7: Composite Index - Column order như thế nào?

**Trả lời**: Place highly selective columns first và columns used in equality conditions before range conditions.

**Nguyên tắc**:
1. Columns in equality (=) conditions first
2. Columns in range conditions last
3. Columns in ORDER BY next
4. Consider query patterns

**Ví dụ**:
```sql
-- Query: WHERE user_id = ? AND status = ? AND created_at > ?
CREATE INDEX idx_orders_composite ON orders (user_id, status, created_at);
-- user_id and status first (equality), created_at last (range)

-- Query: WHERE user_id = ? AND status IN (?, ?) AND total > ?
-- Note: IN is equality for each value
CREATE INDEX idx_orders_composite2 ON orders (user_id, status, total);
-- total last (range condition)

-- Query: WHERE user_id = ? ORDER BY created_at DESC
CREATE INDEX idx_orders_user_date ON orders (user_id, created_at DESC);
-- Index covers both WHERE and ORDER BY

-- ❌ Wrong order: Range column first prevents index usage for equality
-- This is BAD:
CREATE INDEX idx_orders_bad ON orders (created_at, user_id);
-- WHERE user_id = ? cannot use this index efficiently
```

### Q8: EXPLAIN output như thế nào để hiểu?

**Trả lời**: EXPLAIN hiển thị estimated costs, EXPLAIN ANALYZE hiển thị actual execution. Focus vào cost, rows estimate, và actual vs estimated comparison.

**Ví dụ**:
```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id;

-- Sample output analysis:
-- Hash Left Join  (cost=1000.00..5000.00 rows=10000 width=40)
--   (actual time=10.5..50.2 rows=5000 loops=1)
--   Buffers: shared hit=500 read=100
--   -> Seq Scan on users  (cost=0.00..3000.00 rows=10000 width=20)
--         (actual time=0.1..10.0 rows=5000 loops=1)
--         Filter: (created_at > '2024-01-01')
--         Rows Removed by Filter: 5000
--   -> Hash  (cost=500.00..500.00 rows=10000 width=20)
--         -> Seq Scan on orders  (cost=0.00..500.00 rows=10000 width=20)

-- Key metrics:
-- cost=start..end: Estimated I/O + CPU cost
-- rows=XXXXX: Estimated rows
-- actual time=start..end: Real execution time (ms)
-- loops: How many times node executed
-- Buffers: Pages read from cache (hit) vs disk (read)
-- Rows Removed by Filter: Efficiency indicator
```

### Q9: Partial Index - Khi nào nên dùng?

**Trả lời**: Partial Index phù hợp khi queries thường filter trên một subset của rows (ví dụ: active records, pending orders).

**Ví dụ**:
```sql
-- ✅ Index only active users (most queries filter by is_active)
CREATE INDEX idx_users_active_email ON users (email) 
WHERE is_active = TRUE;

-- Query uses partial index automatically
SELECT * FROM users WHERE is_active = TRUE AND email = 'test@example.com';

-- ✅ Index pending orders
CREATE INDEX idx_orders_pending_date ON orders (created_at) 
WHERE status = 'pending';

-- ✅ Composite partial index
CREATE INDEX idx_orders_pending_user ON orders (user_id, created_at) 
WHERE status = 'pending';

-- Benefits:
-- 1. Smaller index size
-- 2. Faster writes (less to maintain)
-- 3. More relevant data indexed

-- Check if partial index is used
EXPLAIN SELECT * FROM orders WHERE status = 'pending' AND created_at > '2024-01-01';
```

---

## 4. Performance

### Q10: Tối ưu slow query như thế nào?

**Trả lời**: Sử dụng EXPLAIN ANALYZE để identify bottlenecks, sau đó address index issues, rewrite queries, hoặc optimize schema.

**Step-by-step**:
```sql
-- Step 1: Identify slow queries
SELECT query, calls, mean_time, total_time, rows
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Step 2: Analyze with EXPLAIN
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) 
SELECT * FROM orders WHERE user_id = 123 ORDER BY created_at DESC LIMIT 10;

-- Step 3: Check for issues
-- ❌ Sequential scan on large table
-- ✅ Should use index scan

-- Step 4: Create missing indexes
CREATE INDEX idx_orders_user_date ON orders (user_id, created_at DESC);

-- Step 5: Verify fix
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM orders WHERE user_id = 123 ORDER BY created_at DESC LIMIT 10;

-- Step 6: If still slow, consider query rewrite
-- Instead of subquery:
SELECT * FROM orders 
WHERE user_id IN (SELECT id FROM users WHERE status = 'active')
ORDER BY created_at DESC;

-- Use JOIN:
SELECT o.* FROM orders o
INNER JOIN users u ON o.user_id = u.id
WHERE u.status = 'active'
ORDER BY o.created_at DESC;
```

### Q11: VACUUM vs VACUUM FULL - Khác nhau gì?

**Trả lời**: VACUUM reclaim dead tuples nhưng không shrink table size. VACUUM FULL reclaim space và shrink table nhưng requires exclusive lock.

**Ví dụ**:
```sql
-- Regular VACUUM (non-blocking)
VACUUM orders;  -- Reclaims dead tuples, doesn't shrink

-- VACUUM with ANALYZE
VACUUM ANALYZE orders;

-- Full VACUUM (blocking, requires exclusive lock)
VACUUM FULL orders;
-- ⚠️ Takes exclusive lock - don't run on production!

-- For online table reorganization, use pg_repack
-- Install: CREATE EXTENSION pg_repack;
SELECT * FROM pg_repack.repack_table('orders');

-- Monitor VACUUM activity
SELECT relname, n_dead_tup, n_live_tup, 
       last_vacuum, last_autovacuum
FROM pg_stat_user_tables
WHERE relname = 'orders';

-- Autovacuum tuning
ALTER TABLE orders SET (
  autovacuum_vacuum_scale_factor = 0.01,  -- Trigger at 1% dead tuples
  autovacuum_analyze_scale_factor = 0.005,
  autovacuum_vacuum_cost_delay = 10  -- ms
);
```

### Q12: Materialized View vs View - Khi nào dùng cái nào?

**Trả lời**: View compute data mỗi lần truy vấn. Materialized View lưu trữ kết quả và cần refresh để update.

**Ví dụ**:
```sql
-- ✅ Regular View (computed each query)
CREATE VIEW monthly_stats AS
SELECT 
  DATE_TRUNC('month', created_at) as month,
  COUNT(*) as order_count,
  SUM(total) as revenue
FROM orders
GROUP BY DATE_TRUNC('month', created_at);

-- Query: Always fresh data, no storage
SELECT * FROM monthly_stats WHERE month = '2024-01-01';

-- ✅ Materialized View (stored result)
CREATE MATERIALIZED VIEW monthly_revenue AS
SELECT 
  DATE_TRUNC('month', created_at) as month,
  COUNT(*) as order_count,
  SUM(total) as revenue
FROM orders
GROUP BY DATE_TRUNC('month', created_at)
WITH DATA;

-- Query: Fast (no computation), potentially stale
SELECT * FROM monthly_revenue WHERE month = '2024-01-01';

-- Refresh manually
REFRESH MATERIALIZED VIEW monthly_revenue;

-- Refresh concurrently (no lock)
CREATE UNIQUE INDEX ON monthly_revenue(month);
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_revenue;

-- Auto-refresh with pg_cron
SELECT cron.schedule(
  'refresh-monthly-revenue', 
  '0 0 * * *',  -- Daily at midnight
  'REFRESH MATERIALIZED VIEW monthly_revenue'
);
```

---

## 5. Replication & HA

### Q13: Streaming Replication setup như thế nào?

**Trả lời**: Streaming Replication cho phép replicas receive WAL records real-time. Cần configure primary và replicas.

**Primary configuration (postgresql.conf)**:
```bash
# Enable WAL archiving
wal_level = replica
max_wal_senders = 5
max_replication_slots = 5
wal_keep_size = 1GB

# Or for cloud environments:
# hot_standby = on
```

**Primary pg_hba.conf**:
```
# Allow replication connections
host     replication     repl_user      127.0.0.1/32     md5
host     replication     repl_user      10.0.0.0/24      md5
```

**Create replication user**:
```sql
CREATE ROLE repl_user WITH REPLICATION LOGIN ENCRYPTED PASSWORD 'secure_password';
```

**Backup primary for replica**:
```bash
pg_basebackup -h 127.0.0.1 -U repl_user -D /var/lib/postgresql/replica1 -P -Xs -R
```

**Replica configuration (postgresql.conf)**:
```bash
hot_standby = on
primary_conninfo = 'host=127.0.0.1 port=5432 user=repl_user application_name=replica1'
```

**Monitor replication**:
```sql
-- On primary
SELECT client_addr, state, sent_lsn, write_lsn, flush_lsn, replay_lsn
FROM pg_stat_replication;

-- On replica
SELECT pg_is_in_recovery();
SELECT * FROM pg_stat_wal_receiver;
```

### Q14: Read replicas có được đọc ngay không?

**Trả lời**: Có, với Hot Standby enabled. Replicas accept read queries trong standby mode.

**Ví dụ**:
```sql
-- Replica configuration (postgresql.conf)
hot_standby = on

-- Connection string for read replicas
# In application:
# - Write operations: primary connection
# - Read operations: replica connection(s)

-- Some data may lag slightly
-- Check replication lag:
-- On primary:
SELECT client_addr, state, 
       (sent_lsn - replay_lsn) as lag_bytes
FROM pg_stat_replication;

-- Queries that modify data fail on replica
-- ❌ This fails on replica:
INSERT INTO orders (total) VALUES (100);  -- ERROR: cannot execute

-- Read-only operations work
-- ✅ This works on replica:
SELECT * FROM orders WHERE status = 'pending';
```

---

## 6. Security

### Q15: Row-Level Security setup như thế nào?

**Trả lời**: RLS enforce access control at row level trong database. Enable RLS và create policies.

**Ví dụ**:
```sql
-- Enable RLS on table
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Create policy for user access
CREATE POLICY orders_user_policy ON orders
  FOR ALL
  USING (user_id = current_setting('app.current_user_id')::INTEGER);

-- Application sets current user before queries
SET app.current_user_id = '123';
SELECT * FROM orders;  -- Only returns user's orders

-- Or use SESSION_USER for simple cases
CREATE POLICY orders_own_policy ON orders
  FOR SELECT
  USING (user_id = (SELECT id FROM users WHERE username = current_user));

-- Multi-tenant example
CREATE POLICY orders_tenant_policy ON orders
  FOR ALL
  USING (tenant_id = current_setting('app.tenant_id')::UUID);

-- Test policy
EXPLAIN SELECT * FROM orders WHERE user_id = 123;
-- Shows filter applied by policy
```

### Q16: Backup encrypted có cần không?

**Trả lời**: Có, backups nên được encrypted để protect sensitive data. Sử dụng pg_dump với encryption hoặc external encryption.

**Ví dụ**:
```sql
-- ✅ Encrypted backup with pg_dump
pg_dump -h localhost -U postgres -F c -Z 6 -f backup.dump.gz mydb
# -F c: Custom format
# -Z 6: Compression level 6

-- ✅ Use GPG for additional encryption
pg_dump mydb | gpg -c > backup.dump.gpg

-- ✅ Restore encrypted backup
gpg -d backup.dump.gpg | pg_restore -h localhost -U postgres -d mydb

-- ✅ pg_backrest for advanced backup management
[backup]
pg1-path=/var/lib/postgresql/14/main
repo1-path=/var/backups/postgresql
repo1-retention-full=2

[postgres]
pg1-path=/var/lib/postgresql/14/main

-- ✅ Verify backup integrity
pg_restore --dbname=postgres --list backup.dump | head
```

---

## Liên kết liên quan
- [PostgreSQL Glossary](./glossary.md)
- [PostgreSQL Architecture](./architecture.md)
- [PostgreSQL Best Practices](./best-practice.md)
- [PostgreSQL Anti-Patterns](./anti-pattern.md)
- [PostgreSQL Checklist](./checklist.md)
- [PostgreSQL Decision Tree](./decision-tree.md)
