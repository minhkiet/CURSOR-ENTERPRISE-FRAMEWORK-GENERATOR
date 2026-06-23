# MySQL FAQ - Câu Hỏi Thường Gặp

## Mục lục
1. [General](#1-general)
2. [Indexes](#2-indexes)
3. [Performance](#3-performance)
4. [Replication](#4-replication)

---

## 1. General

### Q1: Sự khác nhau giữa CHAR và VARCHAR?

**A:**

| Aspect | CHAR | VARCHAR |
|--------|------|---------|
| Storage | Fixed length | Variable length |
| Max length | 255 bytes | 65,535 bytes |
| Padding | Right-padded with spaces | No padding |
| Trailing spaces | Removed on retrieval | Kept |
| Use case | Fixed-length data | Variable-length data |

```sql
-- CHAR(10) uses 10 bytes always
CHAR(10) 'hello'    -- Stored as 'hello     ' (10 bytes)
VARCHAR(10) 'hello' -- Stored as 'hello' (5 bytes)

-- Use CHAR for: country codes (US, VN), status codes
-- Use VARCHAR for: names, emails, addresses
```

---

### Q2: InnoDB vs MyISAM?

**A:**

| Feature | InnoDB | MyISAM |
|---------|--------|--------|
| Transactions | Yes | No |
| Foreign Keys | Yes | No |
| Row-level Locking | Yes | No |
| Full-text Search | Yes (5.6+) | Yes |
| Crash Recovery | Yes | No |
| Table-level Locking | No | Yes |

**Khuyến nghị**: Use InnoDB for almost all use cases. MyISAM only for:
- Full-text search in very old MySQL versions
- Read-heavy tables where transactions not needed
- Legacy applications

---

### Q3: TINYINT(1) vs BOOLEAN?

**A:** TINYINT(1) và BOOLEAN là equivalent trong MySQL.

```sql
-- These are the same:
CREATE TABLE t1 (flag TINYINT(1));
CREATE TABLE t2 (flag BOOLEAN);

-- Both store 0 or 1
-- Use BOOLEAN for clarity in DDL
```

---

## 2. Indexes

### Q4: Khi nào nên tạo index?

**A:** Tạo index khi:

1. Column được used trong WHERE clause thường xuyên
2. Column được used trong JOIN conditions
3. Column được used trong ORDER BY clauses
4. Column có high cardinality (> 100 distinct values)
5. Query returns < 10-15% of table rows

```sql
-- Index for foreign key
CREATE TABLE orders (
  user_id INT NOT NULL,
  INDEX idx_user (user_id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Index for WHERE + ORDER BY
CREATE INDEX idx_status_created ON orders(status, created_at);
-- Query: SELECT * FROM orders WHERE status = 'pending' ORDER BY created_at
```

---

### Q5: Composite index column order?

**A:** Columns có equality conditions (WHERE col = value) nên đứng trước columns có range conditions.

```sql
-- Query pattern:
WHERE user_id = 1 AND status = 'pending' AND created_at > '2024-01-01'

-- Good index order:
INDEX idx_user_status_date (user_id, status, created_at)

-- Can use: user_id=1 AND status='pending' AND created_at > date
-- Can't use: status='pending' alone (not leading column)

-- For queries without user_id:
-- Better to have separate index or reorganize query
```

---

### Q6: EXPLAIN output quan trọng fields?

**A:**

| Field | What to check |
|-------|---------------|
| type | 'ref' or 'range' is good, 'ALL' is table scan |
| key | Index actually used |
| rows | Rows examined (lower is better) |
| Extra | 'Using filesort', 'Using temporary' are warnings |

```sql
-- Good: Uses index
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
-- type: ref, key: idx_email, rows: 1

-- Bad: Full table scan
EXPLAIN SELECT * FROM users WHERE name LIKE '%john%';
-- type: ALL (full table scan)
```

---

## 3. Performance

### Q7: Làm thế nào để optimize slow queries?

**A:** Systematic approach:

```sql
-- 1. Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- Log queries > 1 second

-- 2. Find slow queries
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;

-- 3. Analyze with EXPLAIN
EXPLAIN SELECT ...;

-- 4. Check indexes
SHOW INDEX FROM table_name;

-- 5. Optimize query or add index
CREATE INDEX idx_needed ON table_name(column);

-- 6. Verify improvement
EXPLAIN SELECT ...;  -- Should show better plan
```

---

### Q8: Tại sao query chậm dù có index?

**A:** Common reasons:

1. **Function on column**: `WHERE YEAR(date) = 2024` → Use range: `WHERE date >= '2024-01-01'`

2. **Low cardinality**: Index on boolean column → Only 2 values

3. **Small table**: Full scan faster than index lookup

4. **Statistics outdated**: `ANALYZE TABLE table_name;`

5. **Tipping point**: MySQL chooses table scan when index returns >20% rows

```sql
-- Check table statistics
SHOW TABLE STATUS FROM database_name;

-- Update statistics
ANALYZE TABLE users;

-- Check index statistics
SELECT 
  index_name,
  cardinality
FROM information_schema.statistics
WHERE table_name = 'users';
```

---

### Q9: Buffer pool size nên đặt bao nhiêu?

**A:** General guidelines:

| Available RAM | Buffer Pool Size |
|--------------|------------------|
| 1 GB | 128-256 MB |
| 2 GB | 512-1024 MB |
| 4 GB | 1-2 GB |
| 8 GB | 4-6 GB |
| 16 GB | 8-12 GB |
| 32+ GB | 70-80% of RAM |

```sql
-- Check current settings
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';

-- Set in my.cnf
[mysqld]
innodb_buffer_pool_size = 8G
innodb_buffer_pool_instances = 8  # For multiple instances

-- Dynamic resize (MySQL 8.0+)
SET GLOBAL innodb_buffer_pool_size = 8589934592;  -- 8GB
```

---

## 4. Replication

### Q10: Làm thế nào để set up replication?

**A:**

```sql
-- 1. On PRIMARY: Create replication user
CREATE USER 'repl_user'@'%' IDENTIFIED BY 'repl_password';
GRANT REPLICATION SLAVE ON *.* TO 'repl_user'@'%';

-- 2. Get binlog position
SHOW MASTER STATUS;
-- Note: File and Position values

-- 3. Configure PRIMARY in my.cnf
[mysqld]
log-bin = mysql-bin
server-id = 1  # Must be unique

-- 4. Configure REPLICA in my.cnf
[mysqld]
log-bin = mysql-bin
server-id = 2  # Unique!

-- 5. On REPLICA: START REPLICATION
CHANGE MASTER TO
  MASTER_HOST = 'primary_host',
  MASTER_USER = 'repl_user',
  MASTER_PASSWORD = 'repl_password',
  MASTER_LOG_FILE = 'mysql-bin.000001',
  MASTER_LOG_POS = 123;

START SLAVE;

-- 6. Check status
SHOW SLAVE STATUS\G
```

---

### Q11: Replication lag là gì và xử lý thế nào?

**A:** Replication lag là thời gian REPLICA chạy sau PRIMARY.

```sql
-- Check lag
SHOW SLAVE STATUS\G
-- Seconds_Behind_Master: 0 = caught up, >0 = lag

-- Common causes:
-- 1. Slow queries on PRIMARY
-- 2. Network issues
-- 3. REPLICA can't keep up (slow disk/CPU)

-- Solutions:

-- 1. Enable parallel replication
STOP SLAVE;
SET GLOBAL slave_parallel_threads = 4;
START SLAVE;

-- 2. Compress binlog for transfer
[mysqld]
binlog_transaction_compression = ON

-- 3. Skip problematic events
STOP SLAVE;
SET GLOBAL sql_slave_skip_counter = 1;
START SLAVE;
```

---

## Liên kết liên quan
- [MySQL Glossary](./glossary.md)
- [MySQL Architecture](./architecture.md)
- [MySQL Best Practices](./best-practice.md)
- [MySQL Anti-Patterns](./anti-pattern.md)
- [MySQL Checklist](./checklist.md)
- [MySQL Decision Tree](./decision-tree.md)
