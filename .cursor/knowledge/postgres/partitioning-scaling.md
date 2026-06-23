---
title: PostgreSQL Partitioning và Scaling
description: Hướng dẫn toàn diện về table partitioning, partition management, và các chiến lược scaling cho PostgreSQL
tags: [postgresql, partitioning, scaling, declarative-partitioning, partition-pruning, inheritance]
created: 2026-06-23
version: "1.0"
framework: cursor-enterprise-framework
---

# PostgreSQL Partitioning và Scaling

## Tổng quan

Table partitioning là kỹ thuật chia một large table thành nhiều smaller pieces gọi là partitions, mỗi partition lưu trữ một subset của data dựa trên một hoặc nhiều columns. Kỹ thuật này giúp cải thiện đáng kể performance cho các operations như query, insert, update, delete, và đặc biệt hữu ích cho việc quản lý large-scale data.

PostgreSQL hỗ trợ hai loại partitioning chính: legacy approach sử dụng table inheritance và modern approach sử dụng declarative partitioning được giới thiệu từ PostgreSQL 10. Declarative partitioning cung cấp interface đơn giản hơn và tích hợp tốt hơn với các PostgreSQL features khác.

Trong enterprise environments, partitioning là một phần quan trọng của data architecture strategy, đặc biệt khi làm việc với time-series data, audit logs, hoặc các tables có hàng tỷ rows.

## Mục đích

Tài liệu này nhằm mục đích:

- Cung cấp kiến thức chi tiết về các loại partitioning trong PostgreSQL
- Hướng dẫn cách thiết kế và implement partitioned tables
- Giải thích cách partition pruning hoạt động để tối ưu query performance
- Cung cấp best practices cho việc quản lý partitions
- Trình bày các chiến lược scaling hiệu quả
- Xử lý các vấn đề thường gặp khi làm việc với partitioned tables

## Các khái niệm chính

### Các loại Partitioning

**Range Partitioning**: Chia data dựa trên ranges của một column value. Phổ biến nhất là theo date hoặc numeric ranges.

```sql
-- Tạo partitioned table cho orders theo tháng
CREATE TABLE orders (
    order_id BIGSERIAL,
    customer_id BIGINT NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (order_date);

-- Tạo các partitions cho từng tháng
CREATE TABLE orders_2026_01 PARTITION OF orders
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE orders_2026_02 PARTITION OF orders
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

CREATE TABLE orders_2026_03 PARTITION OF orders
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');

-- Tiếp tục cho các tháng khác...
```

**List Partitioning**: Chia data dựa trên các giá trị cụ thể của một column.

```sql
-- Tạo partitioned table theo region
CREATE TABLE sales (
    sale_id BIGSERIAL,
    region VARCHAR(50) NOT NULL,
    sale_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    product_id BIGINT NOT NULL
) PARTITION BY LIST (region);

-- Tạo partitions cho từng region
CREATE TABLE sales_north PARTITION OF sales
    FOR VALUES IN ('North', 'Northeast', 'Northwest');

CREATE TABLE sales_south PARTITION OF sales
    FOR VALUES IN ('South', 'Southeast', 'Southwest');

CREATE TABLE sales_central PARTITION OF sales
    FOR VALUES IN ('Central', 'Midwest');

CREATE TABLE sales_international PARTITION OF sales
    FOR VALUES IN ('Europe', 'Asia', 'Africa', 'Oceania', 'South America');
```

**Hash Partitioning**: Chia data dựa trên hash value của partition key, đảm bảo phân bố đều data across partitions.

```sql
-- Tạo partitioned table theo hash của customer_id
CREATE TABLE customer_data (
    id BIGSERIAL,
    customer_id BIGINT NOT NULL,
    data_payload JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY HASH (customer_id);

-- Tạo 8 partitions (số lượng nên là power of 2)
CREATE TABLE customer_data_p0 PARTITION OF customer_data
    FOR VALUES WITH (MODULUS 8, REMAINDER 0);

CREATE TABLE customer_data_p1 PARTITION OF customer_data
    FOR VALUES WITH (MODULUS 8, REMAINDER 1);

CREATE TABLE customer_data_p2 PARTITION OF customer_data
    FOR VALUES WITH (MODULUS 8, REMAINDER 2);

CREATE TABLE customer_data_p3 PARTITION OF customer_data
    FOR VALUES WITH (MODULUS 8, REMAINDER 3);

CREATE TABLE customer_data_p4 PARTITION OF customer_data
    FOR VALUES WITH (MODULUS 8, REMAINDER 4);

CREATE TABLE customer_data_p5 PARTITION OF customer_data
    FOR VALUES WITH (MODULUS 8, REMAINDER 5);

CREATE TABLE customer_data_p6 PARTITION OF customer_data
    FOR VALUES WITH (MODULUS 8, REMAINDER 6);

CREATE TABLE customer_data_p7 PARTITION OF customer_data
    FOR VALUES WITH (MODULUS 8, REMAINDER 7);
```

### Declarative Partitioning

PostgreSQL 10+ hỗ trợ declarative partitioning với cú pháp `PARTITION BY`:

```sql
-- Cú pháp cơ bản
CREATE TABLE table_name (...)
PARTITION BY { RANGE | LIST | HASH } (column_list);

-- Partitioned table có thể có PRIMARY KEY và UNIQUE constraints
-- nhưng partition key phải là subset của constraint columns
CREATE TABLE orders (
    order_id BIGINT NOT NULL,
    order_date DATE NOT NULL,
    customer_id BIGINT NOT NULL,
    total_amount DECIMAL(10,2),
    PRIMARY KEY (order_id, order_date)  -- Bao gồm partition key
) PARTITION BY RANGE (order_date);

-- UNIQUE constraint với partition key
CREATE TABLE inventory (
    product_id BIGINT NOT NULL,
    warehouse_id BIGINT NOT NULL,
    quantity INTEGER NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (product_id, warehouse_id, last_updated::date)  -- Bao gồm partition key nếu partition by date
) PARTITION BY RANGE (last_updated);
```

### Partition Pruning

Partition pruning là quá trình PostgreSQL loại bỏ (prune) các partitions không cần thiết khỏi query plan, giúp giảm đáng kể số lượng data cần scan.

**Static Pruning**: Xảy ra khi partition key là constant trong query, PostgreSQL có thể xác định chính xác partition nào cần truy cập ngay lúc planning.

```sql
-- Static pruning - PostgreSQL biết chính xác partition nào
SELECT * FROM orders WHERE order_date = '2026-06-15';

-- EXPLAIN sẽ cho thấy chỉ scan partition chứa ngày đó
EXPLAIN SELECT * FROM orders WHERE order_date = '2026-06-15';
```

**Dynamic Pruning**: Xảy ra khi partition key không phải là constant (ví dụ: subquery, parameter), PostgreSQL phải scan nhiều partitions và loại bỏ những partitions không match sau khi kiểm tra.

```sql
-- Dynamic pruning - cần scan nhiều partitions
SELECT * FROM orders 
WHERE order_date >= (SELECT MIN(order_date) FROM customers WHERE region = 'North');

-- Hoặc với parameterized query
PREPARE get_orders_by_date(date) AS 
SELECT * FROM orders WHERE order_date >= $1;
EXECUTE get_orders_by_date('2026-01-01');
```

**Kiểm tra pruning**:

```sql
EXPLAIN (COSTS OFF) SELECT * FROM orders WHERE order_date = '2026-06-15';
-- Output: Index Scan using orders_2026_06_pkey on orders_2026_06
-- Chỉ partition 2026_06 được scan

-- Với nhiều partitions
EXPLAIN (COSTS OFF) 
SELECT * FROM orders WHERE order_date >= '2026-01-01' AND order_date < '2026-04-01';
-- Output: Bitmap Heap Scan on orders
--         Recheck Cond: ((order_date >= '2026-01-01') AND (order_date < '2026-04-01'))
-- Chỉ partitions Q1 được scan
```

### Partition Management

**Thêm Partition**:

```sql
-- Thêm partition cho tháng tiếp theo
CREATE TABLE orders_2026_07 PARTITION OF orders
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');

-- Hoặc sử dụng function để tự động tạo
CREATE OR REPLACE FUNCTION create_monthly_partition()
RETURNS void AS $$
DECLARE
    partition_date DATE;
    partition_name TEXT;
    start_date DATE;
    end_date DATE;
BEGIN
    -- Tạo partition cho tháng tiếp theo
    partition_date := DATE_TRUNC('month', CURRENT_DATE + INTERVAL '1 month');
    partition_name := 'orders_' || TO_CHAR(partition_date, 'YYYY_MM');
    start_date := partition_date;
    end_date := partition_date + INTERVAL '1 month';
    
    EXECUTE format(
        'CREATE TABLE IF NOT EXISTS %I PARTITION OF orders FOR VALUES FROM (%L) TO (%L)',
        partition_name, start_date, end_date
    );
END;
$$ LANGUAGE plpgsql;
```

**Detach Partition**:

```sql
-- Detach partition để chuyển thành independent table
ALTER TABLE orders DETACH PARTITION orders_2025_01;

-- Partition giờ là independent table
SELECT * FROM orders_2025_01;  -- Vẫn truy cập được

-- Có thể attach lại nếu cần
ALTER TABLE orders ATTACH PARTITION orders_2025_01
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
```

**Drop Partition**:

```sql
-- Drop partition và tất cả data
DROP TABLE orders_2024_01;

-- Hoặc detach trước rồi drop
ALTER TABLE orders DETACH PARTITION orders_2024_01;
DROP TABLE orders_2024_01;
```

**Attach Partition**:

```sql
-- Attach existing table như partition
ALTER TABLE orders ATTACH PARTITION orders_legacy
    FOR VALUES FROM ('2020-01-01') TO ('2024-01-01');
```

## Best Practices

### Chọn Partition Key

**Nên**:

- Chọn column được sử dụng thường xuyên trong WHERE clause
- Ưu tiên columns với high cardinality (nhiều distinct values)
- Date/timestamp columns là lựa chọn phổ biến nhất
- Đảm bảo partition key là immutable (không thay đổi sau khi insert)

**Không nên**:

- Partition quá nhỏ (under-partitioning) - mất lợi ích của partitioning
- Partition quá lớn (over-partitioning) - quá nhiều metadata overhead
- Chọn column thường xuyên được UPDATE - có thể gây row movement

### Số lượng Partitions

```sql
-- Quy tắc chung:
-- - Ít nhất 100MB data per partition
-- - Tối đa 1000 partitions per table
-- - Partition size lý tưởng: 1-10 GB

-- Ví dụ cho time-series data:
-- Daily partitions cho 3 tháng gần nhất (90 partitions)
-- Monthly partitions cho data từ 3 tháng đến 1 năm (12 partitions)
-- Yearly partitions cho data trên 1 năm (archive)
```

### Indexes trên Partitioned Tables

```sql
-- Tạo indexes trên partitioned table (tự động apply cho tất cả partitions)
CREATE INDEX idx_orders_customer ON orders (customer_id);
CREATE INDEX idx_orders_status ON orders (status);

-- Partial indexes cho partitioned tables
CREATE INDEX idx_orders_pending ON orders (order_date) 
WHERE status = 'pending';

-- Unique index (partition key phải included)
CREATE UNIQUE INDEX idx_orders_id_date ON orders (order_id, order_date);

-- Attach indexes cho existing partitions
CREATE INDEX ON orders_2026_06 (customer_id);
```

### Partitioning Strategies

**Strategy 1: Monthly Range Partitioning**:

```sql
CREATE TABLE events (
    id BIGSERIAL,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Tạo partitions cho 12 tháng
CREATE OR REPLACE FUNCTION create_yearly_partitions()
RETURNS void AS $$
DECLARE
    i INTEGER;
    partition_date DATE;
    partition_name TEXT;
BEGIN
    FOR i IN 0..11 LOOP
        partition_date := DATE_TRUNC('month', CURRENT_DATE) + (i || ' months')::interval;
        partition_name := 'events_' || TO_CHAR(partition_date, 'YYYY_MM');
        
        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS %I PARTITION OF events 
             FOR VALUES FROM (%L) TO (%L)',
            partition_name,
            partition_date,
            partition_date + '1 month'::interval
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

**Strategy 2: Multi-level Partitioning**:

```sql
-- Level 1: Year
-- Level 2: Month within year
CREATE TABLE logs (
    id BIGSERIAL,
    log_level VARCHAR(10),
    message TEXT,
    created_at TIMESTAMPTZ
) PARTITION BY RANGE (created_at);

CREATE TABLE logs_2026 PARTITION OF logs
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

CREATE TABLE logs_2026_01 PARTITION OF logs_2026
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```

### Cấu hình autovacuum cho Partitioned Tables

```sql
-- Set autovacuum parameters cho partitioned table
ALTER TABLE orders SET (
    autovacuum_vacuum_scale_factor = 0.01,
    autovacuum_analyze_scale_factor = 0.01,
    autovacuum_vacuum_threshold = 50,
    autovacuum_analyze_threshold = 50
);

-- Hoặc set cho partition cụ thể
ALTER TABLE orders_2026_06 SET (
    autovacuum_vacuum_scale_factor = 0.05
);
```

## Common Patterns

### Pattern 1: Automatic Partition Maintenance

```sql
-- Function để maintain partitions tự động
CREATE OR REPLACE FUNCTION maintain_partitions(
    parent_table TEXT,
    partition_column TEXT,
    partition_type TEXT DEFAULT 'monthly',
    retention_months INTEGER DEFAULT 24
)
RETURNS void AS $$
DECLARE
    partition_date DATE;
    partition_name TEXT;
    start_date DATE;
    end_date DATE;
    old_partition_date DATE;
BEGIN
    -- Tạo partition tương lai
    CASE partition_type
        WHEN 'daily' THEN
            partition_date := DATE_TRUNC('day', CURRENT_DATE + INTERVAL '7 days');
            partition_name := parent_table || '_' || TO_CHAR(partition_date, 'YYYY_MM_DD');
            start_date := partition_date;
            end_date := partition_date + INTERVAL '1 day';
        WHEN 'monthly' THEN
            partition_date := DATE_TRUNC('month', CURRENT_DATE + INTERVAL '2 months');
            partition_name := parent_table || '_' || TO_CHAR(partition_date, 'YYYY_MM');
            start_date := partition_date;
            end_date := partition_date + INTERVAL '1 month';
        WHEN 'yearly' THEN
            partition_date := DATE_TRUNC('year', CURRENT_DATE + INTERVAL '2 years');
            partition_name := parent_table || '_' || TO_CHAR(partition_date, 'YYYY');
            start_date := partition_date;
            end_date := partition_date + INTERVAL '1 year';
    END CASE;
    
    -- Check nếu partition đã tồn tại
    IF NOT EXISTS (
        SELECT 1 FROM pg_tables 
        WHERE tablename = partition_name
    ) THEN
        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS %I PARTITION OF %I 
             FOR VALUES FROM (%L) TO (%L)',
            partition_name, parent_table, start_date, end_date
        );
        RAISE NOTICE 'Created partition: %', partition_name;
    END IF;
    
    -- Xóa partitions cũ (retention policy)
    old_partition_date := CASE partition_type
        WHEN 'daily' THEN CURRENT_DATE - (retention_months * INTERVAL '1 month')
        WHEN 'monthly' THEN CURRENT_DATE - (retention_months * INTERVAL '1 month')
        WHEN 'yearly' THEN CURRENT_DATE - (retention_months * INTERVAL '1 year')
    END;
    
    -- Implement dropping logic here (với proper validation)
END;
$$ LANGUAGE plpgsql;
```

### Pattern 2: Partitioned Table với Real-time Stats

```sql
-- Create partitioned table cho metrics
CREATE TABLE metrics (
    metric_id BIGSERIAL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DOUBLE PRECISION NOT NULL,
    dimension JSONB,
    recorded_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (recorded_at);

-- Create partitions
CREATE TABLE metrics_2026_06 PARTITION OF metrics
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');

CREATE TABLE metrics_2026_07 PARTITION OF metrics
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');

-- Partition-specific indexes
CREATE INDEX idx_metrics_2026_06_name ON metrics_2026_06 (metric_name);

-- View để query across partitions
CREATE OR REPLACE VIEW recent_metrics AS
SELECT 
    metric_name,
    AVG(metric_value) AS avg_value,
    MIN(metric_value) AS min_value,
    MAX(metric_value) AS max_value,
    COUNT(*) AS sample_count,
    recorded_at
FROM metrics
WHERE recorded_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY metric_name, recorded_at
ORDER BY recorded_at DESC;
```

### Pattern 3: Archive Old Partitions

```sql
-- Function để archive partition sang compressed format
CREATE OR REPLACE FUNCTION archive_partition(
    partition_name TEXT,
    archive_path TEXT
)
RETURNS void AS $$
BEGIN
    -- Detach partition
    EXECUTE format('ALTER TABLE orders DETACH PARTITION %I', partition_name);
    
    -- Export to CSV
    EXECUTE format(
        'COPY %I TO %L WITH (FORMAT csv, HEADER)',
        partition_name, archive_path || partition_name || '.csv'
    );
    
    -- Drop partition table (data đã được backup)
    EXECUTE format('DROP TABLE %I', partition_name);
    
    RAISE NOTICE 'Archived partition % to %', partition_name, archive_path;
END;
$$ LANGUAGE plpgsql;
```

## Troubleshooting

### Vấn đề 1: Partition không được tạo đúng cách

**Triệu chứng**: Insert thất bại với lỗi "no partition of relation"

**Nguyên nhân**: Partition cho giá trị cần insert chưa được tạo.

**Giải pháp**:

```sql
-- Kiểm tra partitions hiện tại
SELECT 
    relname AS partition_name,
    pg_get_expr(relpartbound, oid) AS partition_bound
FROM pg_class c
JOIN pg_inherits i ON c.oid = i.inhrelid
JOIN pg_class p ON p.oid = i.inhparent
WHERE p.relname = 'orders';

-- Tạo partition bị thiếu
CREATE TABLE orders_2026_08 PARTITION OF orders
    FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');

-- Hoặc tạo default partition để catch all
CREATE TABLE orders_default PARTITION OF orders DEFAULT;
```

### Vấn đề 2: Slow Queries do Full Partition Scan

**Triệu chứng**: Query mất nhiều thời gian dù đã có partition.

**Giải pháp**:

```sql
-- Kiểm tra xem partition pruning có hoạt động không
EXPLAIN (COSTS OFF) SELECT * FROM orders 
WHERE order_date >= '2026-01-01' AND order_date < '2026-02-01';

-- Đảm bảo statistics được cập nhật
ANALYZE orders;

-- Kiểm tra partition bounds
SELECT 
    c.relname AS partition,
    pg_get_expr(m.relpartbound, m.oid, true) AS partition_range
FROM pg_class m
JOIN pg_inherits i ON m.oid = i.inhrelid
JOIN pg_class c ON m.oid = c.oid
WHERE i.inhparent = 'orders'::regclass;

-- Thêm indexes cho partition-specific columns
CREATE INDEX ON orders (customer_id);
CREATE INDEX ON orders (status);
```

### Vấn đề 3: Lock Contention khi Truncate Partition

**Triệu chứng**: Queries bị blocked khi truncate partition.

**Giải pháp**:

```sql
-- Sử dụng CONCURRENTLY để truncate không blocking
TRUNCATE TABLE orders_2025_01;

-- Hoặc drop và recreate partition
BEGIN;
ALTER TABLE orders DETACH PARTITION orders_2025_01;
DROP TABLE orders_2025_01;

-- Tạo lại partition empty
CREATE TABLE orders_2025_01 PARTITION OF orders
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
COMMIT;
```

### Vấn đề 4: Large Number of Partitions

**Triệu chứn**: Quá nhiều partitions gây ra planning overhead.

**Giải pháp**:

```sql
-- Kiểm tra số lượng partitions
SELECT 
    parent.relname AS parent_table,
    COUNT(child.relname) AS partition_count,
    SUM(pg_relation_size(child.oid)) AS total_size
FROM pg_inherits
JOIN pg_class parent ON pg_inherits.inhparent = parent.oid
JOIN pg_class child ON pg_inherits.inhrelid = child.oid
GROUP BY parent.relname;

-- Nếu quá nhiều, cân nhắc:
-- 1. Giảm granularity (từ daily sang monthly)
-- 2. Sử dụng BRIN index thay vì B-tree
-- 3. Xóa partitions cũ

-- BRIN index cho large append-only tables
CREATE INDEX idx_events_brin ON events USING brin (recorded_at);
```

## Ví dụ minh họa

### Ví dụ 1: E-commerce Orders System

```sql
-- Setup partitioned orders table
CREATE TABLE orders (
    order_id BIGSERIAL,
    customer_id BIGINT NOT NULL,
    order_date DATE NOT NULL,
    shipping_address JSONB,
    billing_address JSONB,
    total_amount DECIMAL(12,2) NOT NULL,
    discount_amount DECIMAL(12,2) DEFAULT 0,
    tax_amount DECIMAL(12,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    payment_method VARCHAR(20),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (order_id, order_date)
) PARTITION BY RANGE (order_date);

-- Create monthly partitions
DO $$
DECLARE
    start_date DATE := '2025-01-01';
    end_date DATE := '2027-01-01';
    current_date DATE := start_date;
BEGIN
    WHILE current_date < end_date LOOP
        EXECUTE format(
            'CREATE TABLE orders_%s PARTITION OF orders 
             FOR VALUES FROM (%L) TO (%L)',
            TO_CHAR(current_date, 'YYYY_MM'),
            current_date,
            current_date + INTERVAL '1 month'
        );
        current_date := current_date + INTERVAL '1 month';
    END LOOP;
END $$;

-- Create indexes
CREATE INDEX idx_orders_customer ON orders (customer_id);
CREATE INDEX idx_orders_status ON orders (status);
CREATE INDEX idx_orders_date_status ON orders (order_date, status);
CREATE INDEX idx_orders_billing ON orders (total_amount) WHERE status = 'completed';

-- Create partitions
CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_date DESC);
```

### Ví dụ 2: Time-series Metrics với Retention

```sql
-- Create partitioned metrics table
CREATE TABLE sensor_metrics (
    metric_id BIGSERIAL,
    sensor_id BIGINT NOT NULL,
    metric_type VARCHAR(50) NOT NULL,
    metric_value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20),
    recorded_at TIMESTAMPTZ NOT NULL,
    quality VARCHAR(10) DEFAULT 'good',
    metadata JSONB,
    PRIMARY KEY (metric_id, recorded_at)
) PARTITION BY RANGE (recorded_at);

-- Create partitions for 2 years ahead
DO $$
DECLARE
    i INTEGER;
    partition_date DATE;
BEGIN
    FOR i IN 0..23 LOOP
        partition_date := DATE_TRUNC('month', CURRENT_DATE) + (i || ' months')::interval;
        EXECUTE format(
            'CREATE TABLE sensor_metrics_%s PARTITION OF sensor_metrics 
             FOR VALUES FROM (%L) TO (%L)',
            TO_CHAR(partition_date, 'YYYY_MM'),
            partition_date,
            partition_date + '1 month'::interval
        );
    END LOOP;
END $$;

-- Create retention policy function
CREATE OR REPLACE FUNCTION cleanup_old_metrics(retention_days INTEGER DEFAULT 90)
RETURNS INTEGER AS $$
DECLARE
    cutoff_date DATE := CURRENT_DATE - (retention_days || ' days')::interval;
    partition_date DATE;
    partition_name TEXT;
    deleted_count INTEGER := 0;
BEGIN
    FOR partition_name IN 
        SELECT c.relname
        FROM pg_class c
        JOIN pg_inherits i ON c.oid = i.inhrelid
        JOIN pg_class p ON p.oid = i.inhparent
        WHERE p.relname = 'sensor_metrics'
        AND c.relname ~ '^sensor_metrics_[0-9]{4}_[0-9]{2}$'
    LOOP
        partition_date := TO_DATE(
            SUBSTRING(partition_name FROM 'sensor_metrics_(.*)'), 
            'YYYY_MM'
        );
        
        IF partition_date < cutoff_date THEN
            EXECUTE format('DROP TABLE %I', partition_name);
            RAISE NOTICE 'Dropped partition: %', partition_name;
            deleted_count := deleted_count + 1;
        END IF;
    END LOOP;
    
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Usage
SELECT cleanup_old_metrics(90);  -- Keep 90 days
```

### Ví dụ 3: Scalable User Activity Tracking

```sql
-- Create partitioned activity log
CREATE TABLE user_activity_log (
    activity_id BIGSERIAL,
    user_id BIGINT NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50),
    resource_id BIGINT,
    ip_address INET,
    user_agent TEXT,
    metadata JSONB,
    occurred_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (activity_id, occurred_at)
) PARTITION BY RANGE (occurred_at);

-- Create partitions
CREATE TABLE user_activity_log_2026_01 PARTITION OF user_activity_log
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE user_activity_log_2026_02 PARTITION OF user_activity_log
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE user_activity_log_2026_03 PARTITION OF user_activity_log
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE user_activity_log_2026_04 PARTITION OF user_activity_log
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE user_activity_log_2026_05 PARTITION OF user_activity_log
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
CREATE TABLE user_activity_log_2026_06 PARTITION OF user_activity_log
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');

-- Create indexes
CREATE INDEX idx_activity_user ON user_activity_log (user_id, occurred_at DESC);
CREATE INDEX idx_activity_type ON user_activity_log (activity_type, occurred_at DESC);
CREATE INDEX idx_activity_resource ON user_activity_log (resource_type, resource_id) 
    WHERE resource_id IS NOT NULL;

-- View for recent activity
CREATE OR REPLACE VIEW v_user_recent_activity AS
SELECT 
    u.user_id,
    u.email,
    a.activity_type,
    a.resource_type,
    a.occurred_at
FROM user_activity_log a
JOIN users u ON a.user_id = u.user_id
WHERE a.occurred_at >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
ORDER BY a.occurred_at DESC;

-- Aggregation view
CREATE MATERIALIZED VIEW mv_daily_activity_stats AS
SELECT 
    DATE_TRUNC('day', occurred_at) AS activity_date,
    activity_type,
    COUNT(*) AS event_count,
    COUNT(DISTINCT user_id) AS unique_users
FROM user_activity_log
WHERE occurred_at >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY 1, 2;
```

## References

### Official Documentation
- [PostgreSQL Partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)
- [DDL for Partitioning](https://www.postgresql.org/docs/current/sql-createtable.html#SQL-CREATETABLE-PARTITIONING)
- [Partition Pruning](https://www.postgresql.org/docs/current/partition-pruning.html)
- [Partitioning and Constraint Exclusion](https://www.postgresql.org/docs/current/ddl-partitioning.html#DDL-PARTITIONING-CONSTRAINT-EXCLUSION)

### Tools và Extensions
- `pg_partman`: Automatic partition management
- `pg_pathman`: Fast partitioning (third-party)
- `timescaledb`: Time-series extension với automatic partitioning

### Books và Resources
- "PostgreSQL 16 Administration Cookbook" - Simon Riggs
- "The Art of PostgreSQL" - Dimitri Fontaine
- pgsql-general mailing list
- Planet PostgreSQL blog aggregate
