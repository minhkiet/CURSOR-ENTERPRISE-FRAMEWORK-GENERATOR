---
title: PostgreSQL Performance Tuning
description: Tối ưu hóa hiệu suất PostgreSQL thông qua query planning, EXPLAIN ANALYZE, và các chiến lược indexing nâng cao
tags: [postgresql, performance, indexing, query-optimization, explain-analyze, b-tree, gin, gist, brin]
created: 2026-06-23
version: "1.0"
framework: cursor-enterprise-framework
---

# PostgreSQL Performance Tuning

## Tổng quan

Performance tuning là một trong những kỹ năng quan trọng nhất của DBA và backend engineer khi làm việc với PostgreSQL. Tài liệu này cung cấp hướng dẫn toàn diện về cách phân tích và tối ưu hóa hiệu suất database, từ việc đọc EXPLAIN ANALYZE output cho đến việc lựa chọn đúng loại index cho từng use case cụ thể.

PostgreSQL là một trong những database relational mạnh mẽ nhất hiện nay, nhưng để khai thác tối đa hiệu suất của nó, ta cần hiểu rõ cách query planner hoạt động, khi nào cần tạo index, và làm thế nào để interpret các kết quả từ việc phân tích query.

## Mục đích

Mục đích của tài liệu này bao gồm:

- Cung cấp kiến thức nền tảng về query planning và execution trong PostgreSQL
- Hướng dẫn cách sử dụng EXPLAIN ANALYZE để phân tích hiệu suất query
- Giải thích chi tiết các loại index khác nhau và khi nào nên sử dụng chúng
- Cung cấp best practices cho việc tối ưu hóa schema và query
- Liệt kê các pattern phổ biến và cách xử lý troubleshoot khi gặp vấn đề

## Các khái niệm chính

### Query Planning trong PostgreSQL

PostgreSQL sử dụng một cost-based query optimizer để tạo ra execution plan tối ưu cho mỗi query. Query planner sẽ ước tính cost của các phương án thực thi khác nhau dựa trên statistics của tables và indexes, sau đó chọn plan có cost thấp nhất.

**Cost Model**: PostgreSQL sử dụng cost model với các tham số có thể cấu hình được. Cost được đo bằng đơn vị page reads (thường là disk page, kích thước mặc định 8KB). Các tham số quan trọng bao gồm:

- `seq_page_cost`: Cost để đọc một heap page theo sequential scan (mặc định: 1.0)
- `random_page_cost`: Cost để đọc một heap page ngẫu nhiên (mặc định: 4.0)
- `cpu_tuple_cost`: Cost để xử lý một row (mặc định: 0.01)
- `cpu_index_tuple_cost`: Cost để xử lý một index entry (mặc định: 0.005)
- `cpu_operator_cost`: Cost để thực hiện một operator (mặc định: 0.0025)

Trên các hệ thống có SSD storage, giá trị `random_page_cost` nên được giảm xuống mức gần bằng `seq_page_cost` (ví dụ: 1.1) vì random reads trên SSD không chậm hơn sequential reads nhiều như trên HDD truyền thống.

**Statistics**: Query planner dựa vào statistics được thu thập bởi `ANALYZE` command để ước tính cardinality (số lượng rows) và distribution của data. Statistics bao gồm:

- `pg_statistic`: Bảng chứa các statistics cơ bản
- `pg_stats`: View cho phép đọc statistics một cách dễ dàng hơn
- `n_distinct`: Ước tính số lượng distinct values
- `correlation`: Mức độ correlation giữa physical row ordering và column ordering
- `most_common_vals` và `most_common_freqs`: Các giá trị phổ biến nhất và tần suất của chúng
- `histogram_bounds`: Các boundaries của histogram mô tả distribution

### EXPLAIN và EXPLAIN ANALYZE

**EXPLAIN**: Hiển thị execution plan mà query planner sẽ sử dụng mà không thực sự execute query. Useful để xem plan mà không cần chờ query hoàn thành.

```sql
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';
```

**EXPLAIN ANALYZE**: Thực thi query và hiển thị cả execution plan lẫn actual execution statistics. Đây là công cụ quan trọng nhất để phân tích hiệu suất.

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders 
WHERE order_date >= '2025-01-01' 
AND status = 'completed';
```

**Các tùy chọn quan trọng của EXPLAIN**:

- `ANALYZE`: Thực thi query và hiển thị actual times
- `BUFFERS`: Hiển thị buffer usage (shared hit/read, temp read/write)
- `FORMAT`: Định dạng output (TEXT, JSON, YAML, XML)
- `VERBOSE`: Hiển thị thêm thông tin chi tiết về plan
- `COSTS`: Hiển thị cost estimates (mặc định là on)
- `TIMING`: Hiển thị actual timing cho mỗi node (chỉ với ANALYZE)

### Các loại Index trong PostgreSQL

PostgreSQL hỗ trợ nhiều loại index, mỗi loại phù hợp với các use case khác nhau:

**B-tree Index**: Loại index mặc định và phổ biến nhất. Tối ưu cho:

- Equality comparisons (=)
- Range comparisons (<, >, <=, >=, BETWEEN)
- IS NULL / IS NOT NULL
- Pattern matching với LIKE 'prefix%'

**GIN (Generalized Inverted Index)**: Phù hợp cho:

- Full-text search
- Array containment (@>, <@, &&)
- JSONB containment và key existence
- Document indexing

**GiST (Generalized Search Tree)**: Phù hợp cho:

- Geometric data types
- Range types
- PostGIS (spatial data)
- Full-text search (tsvector)

**BRIN (Block Range Index)**: Phù hợp cho:

- Large tables với physical correlation (data inserted in order)
- Time-series data
- Log tables

**Hash Index**: Chỉ hỗ trợ equality comparisons, useful cho temporary data hoặc khi bạn cần index đơn giản.

### Partial Indexes

Partial indexes là index được tạo trên subset của table dựa trên một điều kiện WHERE. Chúng đặc biệt hữu ích khi:

- Chỉ một phần nhỏ của rows thường xuyên được query
- Bạn muốn giảm kích thước index
- Bạn muốn enforce uniqueness trên subset của rows

```sql
-- Tạo partial index cho các orders đang active
CREATE INDEX idx_orders_active ON orders (customer_id, order_date)
WHERE status = 'active';

-- Partial index cho các users đã verified
CREATE INDEX idx_users_verified ON users (email)
WHERE email_verified = true;

-- Unique partial index cho primary email của active users
CREATE UNIQUE INDEX idx_users_primary_email 
ON users (email) 
WHERE deleted_at IS NULL AND is_active = true;
```

### Expression Indexes

Expression indexes cho phép index trên kết quả của một biểu thức hoặc function, không chỉ trên column values trực tiếp.

```sql
-- Index trên lower-cased email để query không phân biệt case
CREATE INDEX idx_users_email_lower ON users (lower(email));

-- Index trên date extraction
CREATE INDEX idx_orders_month ON orders (date_trunc('month', order_date));

-- Index trên JSON field
CREATE INDEX idx_orders_metadata_status 
ON orders USING gin ((metadata -> 'status'));

-- Index trên computed value
CREATE INDEX idx_products_revenue 
ON products ((price * (1 - discount_percent / 100)));
```

### Covering Indexes

Covering indexes (Index-Only Scans) bao gồm tất cả các columns cần thiết cho một query trong index, cho phép PostgreSQL trả về kết quả mà không cần đọc heap page.

```sql
-- Covering index cho query: SELECT name, email FROM users WHERE created_at > '2025-01-01'
CREATE INDEX idx_users_covering 
ON users (created_at) 
INCLUDE (name, email);

-- Query này sẽ sử dụng index-only scan
SELECT name, email FROM users WHERE created_at > '2025-01-01';
```

## Best Practices

### Thu thập Statistics định kỳ

Đảm bảo statistics luôn được cập nhật để query planner có thể đưa ra quyết định tối ưu:

```sql
-- Chạy ANALYZE thủ công sau khi bulk insert/delete
ANALYZE VERBOSE users;

-- Hoặc sử dụng autovacuum để tự động
-- Cấu hình trong postgresql.conf:
-- autovacuum_analyze_scale_factor = 0.1 (10% của table)
-- autovacuum_analyze_threshold = 50 (số rows thay đổi tối thiểu)
```

### Cấu hình autovacuum hiệu quả

Autovacuum là critical cho việc duy trì hiệu suất:

```conf
# postgresql.conf

# Autovacuum parameters
autovacuum = on
autovacuum_max_workers = 4
autovacuum_naptime = 1min

# Per-table overrides có thể set qua ALTER TABLE
# ALTER TABLE big_table SET (autovacuum_vacuum_scale_factor = 0.01);
```

### Giám sát Index Usage

Loại bỏ unused indexes để tiết kiệm space và giảm overhead khi write:

```sql
-- Tìm các indexes không được sử dụng trong 7 ngày
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
AND indexrelid NOT IN (
    SELECT conindid FROM pg_constraint WHERE contype IN ('p', 'u')
)
ORDER BY pg_relation_size(indexrelid) DESC;
```

### Sử dụng Connection Pooling

Tránh tạo quá nhiều connections trực tiếp đến PostgreSQL:

```sql
-- Xem số lượng connections hiện tại
SELECT 
    state,
    COUNT(*)
FROM pg_stat_activity
GROUP BY state;

-- Xem max_connections setting
SHOW max_connections;
```

### Điều chỉnh work_mem

`work_mem` là lượng memory được sử dụng cho các operations như sorting và hashing. Tăng giá trị này có thể cải thiện đáng kể performance cho các query phức tạp:

```sql
-- Xem giá trị hiện tại
SHOW work_mem;

-- Set cho session hiện tại
SET work_mem = '256MB';

-- Set cho một query cụ thể
SELECT ... FROM (
    SELECT /*+ SET(work_mem '512MB') */ ...
) sub;
```

## Common Patterns

### Pattern 1: Index cho ORDER BY và LIMIT

Khi bạn cần lấy top N rows với ORDER BY:

```sql
-- Bảng orders với index
CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_date DESC);

-- Query lấy 10 đơn hàng mới nhất của một customer
EXPLAIN ANALYZE
SELECT order_id, order_date, total_amount
FROM orders
WHERE customer_id = 12345
ORDER BY order_date DESC
LIMIT 10;
```

### Pattern 2: Index cho IN với nhiều giá trị

```sql
-- Tạo index cho IN queries
CREATE INDEX idx_orders_status ON orders (status);

-- Query với nhiều giá trị IN
SELECT * FROM orders WHERE status IN ('pending', 'processing', 'shipped');
```

### Pattern 3: Index cho JSONB queries

```sql
-- Tạo GIN index cho JSONB data
CREATE INDEX idx_orders_metadata ON orders USING gin (metadata);

-- Queries có thể sử dụng index
SELECT * FROM orders 
WHERE metadata @> '{"priority": "high"}';

SELECT * FROM orders 
WHERE metadata ? 'priority';

SELECT * FROM orders 
WHERE metadata ->> 'status' = 'urgent';
```

### Pattern 4: Index cho Full-text Search

```sql
-- Tạo tsvector column và index
ALTER TABLE articles ADD COLUMN search_vector tsvector;

CREATE INDEX idx_articles_search ON articles 
USING gin (search_vector);

-- Trigger để tự động update tsvector
CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := 
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.tags, '')), 'C');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER articles_search_vector_update
    BEFORE INSERT OR UPDATE ON articles
    FOR EACH ROW EXECUTE FUNCTION update_search_vector();

-- Search query
SELECT title, snippet FROM articles
WHERE search_vector @@ to_tsquery('english', 'postgresql & performance')
ORDER BY ts_rank(search_vector, to_tsquery('english', 'postgresql & performance'))
LIMIT 10;
```

### Pattern 5: Index cho Date Range Queries

```sql
-- Tạo index cho các queries về khoảng thời gian
CREATE INDEX idx_events_time_range ON events (start_time, end_time);

-- Range query
SELECT * FROM events
WHERE start_time <= '2026-06-30' 
AND end_time >= '2026-06-01';
```

## Troubleshooting

### Vấn đề 1: Sequential Scan trên Large Table

**Triệu chứng**: Query sử dụng Sequential Scan thay vì Index Scan trên large table.

**Nguyên nhân có thể**:
- Statistics không được cập nhật
- Giá trị `random_page_cost` quá cao
- Table quá nhỏ để index có lợi
- Query trả về quá nhiều rows

**Giải pháp**:

```sql
-- 1. Cập nhật statistics
ANALYZE VERBOSE table_name;

-- 2. Kiểm tra statistics của column
SELECT 
    attname,
    n_distinct,
    correlation,
    most_common_vals,
    histogram_bounds
FROM pg_stats
WHERE tablename = 'table_name'
AND attname = 'column_name';

-- 3. Giảm random_page_cost nếu dùng SSD
SET random_page_cost = 1.1;

-- 4. Force index usage (chỉ để test)
SET enable_seqscan = off;
EXPLAIN ANALYZE SELECT * FROM table_name WHERE column = 'value';
SET enable_seqscan = on;

-- 5. Kiểm tra xem index có phù hợp không
SELECT * FROM pg_indexes WHERE tablename = 'table_name';
```

### Vấn đề 2: Poor Cardinality Estimation

**Triệu chứng**: Query planner ước tính số rows sai, dẫn đến plan không tối ưu.

**Giải pháp**:

```sql
-- 1. Tăng target cho statistics collection
ALTER TABLE orders 
ALTER COLUMN status 
SET STATISTICS 500;

-- 2. Thu thập lại statistics
ANALYZE orders;

-- 3. Kiểm tra estimate vs actual
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE status = 'pending';

-- 4. Tăng default_statistics_target
SET default_statistics_target = 500;

-- 5. Kiểm tra extimate
ANALYZE VERBOSE;
```

### Vấn đề 3: Index Bloat

**Triệu chứng**: Index size lớn bất thường, performance giảm theo thời gian.

**Giải pháp**:

```sql
-- 1. Kiểm tra index bloat
SELECT 
    schemaname || '.' || tablename AS table,
    indexname,
    pg_size_pretty(pg_relation_size(i.indexrelid)) AS index_size,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes ui
JOIN pg_index i ON ui.indexrelid = i.indexrelid
WHERE schemaname = 'public'
ORDER BY pg_relation_size(i.indexrelid) DESC;

-- 2. Rebuild index
REINDEX INDEX CONCURRENTLY index_name;

-- 3. Hoặc sử dụng VACUUM FULL (chặn table)
VACUUM FULL index_name;

-- 4. Monitor index bloat thường xuyên
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size,
    idx_scan,
    (SELECT COUNT(*) FROM pg_stat_user_tables WHERE relname = ui.tablename) AS table_scans
FROM pg_stat_user_indexes ui
WHERE idx_scan = 0
AND NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conindid = ui.indexrelid
);
```

### Vấn đề 4: Lock Contention

**Triệu chứng**: Queries bị blocked hoặc chậm do lock contention.

**Giải pháp**:

```sql
-- 1. Xem các locks đang chờ
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocking_locks.pid AS blocking_pid,
    blocked_activity.query AS blocked_query,
    blocking_activity.query AS blocking_query
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity 
    ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity 
    ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- 2. Hủy blocking query
SELECT pg_cancel_backend(pid);
-- Hoặc force terminate:
SELECT pg_terminate_backend(pid);

-- 3. Sử dụng index để tránh lock
CREATE INDEX CONCURRENTLY ON orders (customer_id);
```

## Ví dụ minh họa

### Ví dụ 1: Phân tích slow query

```sql
-- Step 1: Bật pg_stat_statements (extension cần được tạo)
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Step 2: Tìm các slow queries
SELECT 
    query,
    calls,
    mean_exec_time,
    total_exec_time,
    rows,
    (100 * shared_blks_hit / NULLIF(shared_blks_hit + shared_blks_read, 0))::numeric(5,2) AS cache_hit_ratio
FROM pg_stat_statements
WHERE query LIKE '%orders%'
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Step 3: EXPLAIN ANALYZE slow query
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.order_id, o.order_date, c.customer_name, o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2025-01-01'
AND o.status = 'completed'
ORDER BY o.order_date DESC
LIMIT 100;

-- Step 4: Tạo index nếu cần
CREATE INDEX CONCURRENTLY idx_orders_date_status 
ON orders (order_date DESC, status) 
INCLUDE (customer_id, total_amount);

-- Step 5: Verify improvement
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.order_id, o.order_date, c.customer_name, o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2025-01-01'
AND o.status = 'completed'
ORDER BY o.order_date DESC
LIMIT 100;
```

### Ví dụ 2: Tối ưu hóa dashboard query

```sql
-- Dashboard query: Top customers by revenue
EXPLAIN ANALYZE
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_revenue,
    AVG(o.total_amount) AS avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
AND o.status = 'completed'
GROUP BY c.customer_id, c.customer_name
ORDER BY total_revenue DESC
LIMIT 20;

-- Optimization: Materialized view
CREATE MATERIALIZED VIEW mv_monthly_top_customers AS
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_revenue,
    AVG(o.total_amount) AS avg_order_value,
    DATE_TRUNC('month', o.order_date) AS month
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.customer_name, DATE_TRUNC('month', o.order_date);

CREATE UNIQUE INDEX idx_mv_top_customers 
ON mv_monthly_top_customers (month, total_revenue DESC, customer_id);

-- Refresh function
CREATE OR REPLACE FUNCTION refresh_top_customers()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_monthly_top_customers;
END;
$$ LANGUAGE plpgsql;

-- Scheduled refresh (pg_cron extension)
SELECT cron.schedule(
    'refresh-top-customers',
    '0 1 * * *',  -- Chạy lúc 1:00 AM mỗi ngày
    'SELECT refresh_top_customers()'
);
```

### Ví dụ 3: Monitoring index health

```sql
-- Tạo function để check index health
CREATE OR REPLACE FUNCTION check_index_health()
RETURNS TABLE (
    schema_name text,
    table_name text,
    index_name text,
    index_size bigint,
    index_scans bigint,
    index_bloat_ratio numeric,
    recommendation text
) AS $$
BEGIN
    RETURN QUERY
    WITH index_stats AS (
        SELECT 
            schemaname,
            tablename,
            indexname,
            relid,
            indexrelid,
            pg_relation_size(indexrelid) AS size_bytes,
            idx_scan,
            idx_tup_read,
            idx_tup_fetch,
            idx_tup_write
        FROM pg_stat_user_indexes
    ),
    table_stats AS (
        SELECT 
            schemaname,
            relname AS tablename,
            n_live_tup,
            n_dead_tup,
            pg_relation_size(relid) AS table_size
        FROM pg_stat_user_tables
    )
    SELECT
        i.schemaname::text,
        i.tablename::text,
        i.indexname::text,
        i.size_bytes,
        i.idx_scan,
        CASE 
            WHEN t.table_size > 0 THEN
                round((i.size_bytes::numeric / t.table_size * 100)::numeric, 2)
            ELSE 0
        END AS bloat_ratio,
        CASE
            WHEN i.idx_scan = 0 AND NOT EXISTS (
                SELECT 1 FROM pg_constraint c 
                WHERE c.conindid = i.indexrelid
            ) THEN 'UNUSED - Consider dropping'
            WHEN i.size_bytes > 1024*1024*1024 AND i.idx_scan < 1000 THEN 
                'Large but rarely used - Review necessity'
            WHEN i.size_bytes > 1024*1024*1024 AND 
                 (i.idx_tup_write::float / NULLIF(i.idx_scan, 0) > 10) THEN 
                'High write overhead - Consider partial index'
            ELSE 'Healthy'
        END::text AS recommendation
    FROM index_stats i
    JOIN table_stats t ON i.schemaname = t.schemaname AND i.tablename = t.tablename
    ORDER BY i.size_bytes DESC;
END;
$$ LANGUAGE plpgsql;

-- Run health check
SELECT * FROM check_index_health()
WHERE recommendation != 'Healthy'
ORDER BY index_size DESC;
```

## References

### Official Documentation
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)
- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [PostgreSQL Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL Statistics](https://www.postgresql.org/docs/current/monitoring-stats.html)

### Extensions hữu ích
- `pg_stat_statements`: Query performance tracking
- `pg_proctab`: OS-level metrics
- `pgstattuple`: Index/table statistics
- `pg_qualstats`: Predicate statistics

### Books và Resources
- "The Art of PostgreSQL" - Dimitri Fontaine
- "PostgreSQL 16 Administration Cookbook" - Simon Riggs
- pgsql-performance mailing list
- Planet PostgreSQL blog aggregate
