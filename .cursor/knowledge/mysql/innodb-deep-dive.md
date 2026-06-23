---
title: InnoDB Deep Dive
description: Kiến trúc chi tiết InnoDB - Buffer Pool, Change Buffer, Adaptive Hash Index, Doublewrite Buffer, Tablespaces, Row Formats
tags: [mysql, innodb, storage-engine, buffer-pool, transaction, locking]
created: 2026-06-23
version: 1.0.0
framework: cursor-enterprise-framework
---

# InnoDB Deep Dive

## Tổng quan

InnoDB là storage engine mặc định và được khuyến nghị cho MySQL kể từ phiên bản 5.5 trở lên. InnoDB được thiết kế để cung cấp các tính năng enterprise-grade bao gồm transaction ACID, row-level locking, foreign key constraints, và crash recovery. Tài liệu này đi sâu vào kiến trúc bên trong của InnoDB, giúp bạn hiểu cách MySQL xử lý dữ liệu và tối ưu hóa hiệu suất.

InnoDB sử dụng kiến trúc multi-threaded với các background threads chịu trách nhiệm cho các tác vụ như flush dirty pages, log writing, và I/O operations. Kiến trúc này cho phép InnoDB xử lý high-concurrency workloads một cách hiệu quả trong khi vẫn đảm bảo durability và consistency của dữ liệu.

## Mục đích của tài liệu

Tài liệu này được viết nhằm mục đích giúp các database administrator và developer hiểu sâu về InnoDB để có thể:

- Cấu hình InnoDB một cách tối ưu cho workloads cụ thể
- Chẩn đoán và xử lý các vấn đề liên quan đến hiệu suất
- Thiết kế schema và queries tận dụng tối đa các tính năng của InnoDB
- Lên kế hoạch capacity và resource allocation

## Các Khái niệm Cốt lõi

### 1. Buffer Pool

Buffer Pool là vùng nhớ in-memory chính nơi InnoDB lưu trữ data pages và index pages. Đây là thành phần quan trọng nhất ảnh hưởng đến hiệu suất của InnoDB vì nó giảm thiểu I/O operations bằng cách giữ data trong memory.

#### Cấu trúc của Buffer Pool

Buffer Pool được chia thành nhiều instances để giảm contention khi có nhiều concurrent operations. Mỗi instance quản lý các lists sau:

- **Free List**: Danh sách các pages trống có thể sử dụng
- **LRU List**: Danh sách Least Recently Used để evict pages khi cần
- **Flush List**: Danh sách các dirty pages cần được flush xuống disk
- **Unzip LRu List**: Danh sách pages cho compressed tables

#### Cấu hình Buffer Pool

```ini
# my.cnf - Cấu hình Buffer Pool
[mysqld]
innodb_buffer_pool_size = 64G          # Kích thước buffer pool (60-80% RAM)
innodb_buffer_pool_instances = 8        # Số lượng instances
innodb_buffer_pool_chunk_size = 1G      # Kích thước chunk cho online resizing
innodb_read_io_threads = 16             # Số threads cho read I/O
innodb_write_io_threads = 16           # Số threads cho write I/O
innodb_io_capacity = 2000              # I/O capacity (tùy thuộc vào disk)
innodb_io_capacity_max = 4000          # Max I/O capacity
```

#### Kích thước Buffer Pool tối ưu

Việc chọn kích thước Buffer Pool phụ thuộc vào nhiều yếu tố:

1. **Tổng bộ nhớ RAM**: Nên cấu hình Buffer Pool chiếm 60-80% RAM
2. **Workload type**: OLTP workloads cần buffer pool lớn hơn
3. **Data size**: Nếu working set nhỏ hơn RAM, có thể set gần bằng data size
4. **Other MySQL memory usage**: Cần trừ bộ nhớ cho other components

```sql
-- Xem kích thước buffer pool hiện tại
SELECT @@innodb_buffer_pool_size / 1024 / 1024 / 1024 AS 'Buffer Pool (GB)';

-- Xem số lượng buffer pool instances
SELECT @@innodb_buffer_pool_instances;

-- Monitoring Buffer Pool statistics
SELECT 
    pool.pool_id,
    pool.lru_count,
    pool.free_count,
    pool.flush_count,
    pages.pages AS 'total_pages',
    pages.hashed_pages,
    pages.old_pages
FROM information_schema.INNODB_BUFFER_POOL_STATS pool
JOIN information_schema.INNODB_BUFFER_PAGE_LRU pool_lru 
    ON pool.pool_id = pool_lru.pool_id;
```

#### Page Replacement Algorithm

InnoDB sử dụng variant của LRU (Least Recently Used) algorithm gọi là "midpoint insertion strategy". Khi một page được access lần đầu, nó được đặt ở giữa LRU list thay vì đầu. Điều này ngăn chặn việc full table scans đẩy hết hot data ra khỏi buffer pool.

LRU list được chia thành hai phần:
- **Young sublist**: 5/8 của list, chứa các pages được access gần đây
- **Old sublist**: 3/8 của list, chứa các pages ít được access

```ini
# Tinh chỉnh LRU
[mysqld]
innodb_old_blocks_pct = 37            # Phần trăm old sublist (default 37%)
innodb_old_blocks_time = 1000         # Thời gian (ms) trước khi move lên young
```

### 2. Change Buffer

Change Buffer là cấu trúc dữ liệu in-memory (cũng có thể được persist xuống disk) lưu trữ các thay đổi cho secondary indexes. Khi có INSERT, UPDATE, hoặc DELETE trên một table có secondary index, thay vì đọc index page vào buffer pool và modify ngay lập tức, InnoDB buffer các thay đổi này.

#### Tại sao cần Change Buffer?

Khi workload có nhiều random INSERTs/UPDATEs trên các bảng có nhiều secondary indexes, việc merge ngay lập tức sẽ gây ra nhiều random I/O operations. Change Buffer giúp batch các thay đổi này lại và merge khi có cơ hội (thường là khi page được đọc vào buffer pool).

#### Monitoring Change Buffer

```sql
-- Xem Change Buffer statistics
SHOW STATUS LIKE 'Innodb_%_change_buffer%';

-- Chi tiết hơn
SELECT 
    SUBSTR(NAME, 18) AS change_buffer_type,
    COMMENT,
    COUNT
FROM information_schema.INNODB_METRICS
WHERE NAME LIKE 'innodb_change_buffer_%'
ORDER BY COUNT DESC;

-- Xem buffered changes trong memory
SELECT * FROM information_schema.INNODB_CMP;
```

```ini
# Cấu hình Change Buffer
[mysqld]
innodb_change_buffer_max_size = 25    # Tối đa 25% buffer pool
innodb_change_buffering = 'all'       # all, none, inserts, deletes, changes, purges
```

### 3. Adaptive Hash Index (AHI)

Adaptive Hash Index là hash table in-memory được InnoDB tự động xây dựng dựa trên patterns của các queries. AHI giúp tăng tốc độ lookup cho các điều kiện WHERE bằng các column đã được index.

#### Cách hoạt động

Khi InnoDB nhận thấy một pattern truy cập liên tục (ví dụ: cùng một primary key lookup), nó sẽ tự động thêm entry vào hash table. Hash index này trỏ trực tiếp đến data page chứa row đó, bỏ qua B-tree traversal.

```sql
-- Monitoring AHI
SHOW ENGINE INNODB STATUS\G

-- Hoặc query metrics
SELECT 
    SUBSTR(NAME, 5) AS metric,
    COMMENT,
    COUNT
FROM information_schema.INNODB_METRICS
WHERE NAME LIKE 'innodb%hash%';
```

```ini
# Cấu hình AHI
[mysqld]
innodb_adaptive_hash_index = ON        # Bật/tắt AHI (default ON)
innodb_adaptive_hash_index_parts = 8  # Số partitions cho AHI (max 256)
```

#### Khi nào nên tắt AHI?

Trong một số trường hợp, AHI có thể gây contention:

- Khi có quá nhiều concurrent threads truy cập cùng partition
- Khi working set lớn hơn buffer pool đáng kể
- Khi có nhiều point queries trên large primary keys

### 4. Doublewrite Buffer

Doublewrite Buffer là một safety mechanism giúp ngăn chặn partial page writes - tình trạng xảy ra khi system crash ngay sau khi đã write một page nhưng trước khi page được fsync hoàn toàn.

#### Cách hoạt động

1. Trước khi write data page xuống data file, InnoDB copy page vào doublewrite buffer
2. Doublewrite buffer được flush và fsync vào một vùng reserved trong system tablespace
3. Sau đó data page mới được write vào vị trí thực tế trong data file
4. Nếu crash xảy ra trong quá trình step 3, recovery process sẽ restore page từ doublewrite buffer

```sql
-- Kiểm tra doublewrite buffer
SHOW VARIABLES LIKE 'innodb_doublewrite%';

-- Monitoring
SHOW STATUS LIKE 'Innodb_dblwr%';
```

```ini
# Cấu hình Doublewrite
[mysqld]
innodb_doublewrite = ON                # Luôn bật trừ khi có lý do đặc biệt
innodb_doublewrite_dir = '/path'       # Vị trí doublewrite files (MySQL 8.0.20+)
innodb_doublewrite_files = 2           # Số doublewrite files
innodb_doublewrite_pages = 128         # Pages per batch
```

### 5. Tablespaces

InnoDB hỗ trợ nhiều loại tablespaces với các mục đích khác nhau.

#### System Tablespace

System tablespace chứa:

- InnoDB data dictionary
- Change buffer
- Doublewrite buffer
- Undo logs (nếu không dùng temporary tablespace riêng)
- Rollback segments

```ini
# Cấu hình System Tablespace
[mysqld]
innodb_data_home_dir = /var/lib/mysql
innodb_data_file_path = ibdata1:12M:autoextend
innodb_undo_directory = /var/lib/mysql/undo
innodb_undo_tablespaces = 4
```

#### File-per-table Tablespace

Mỗi table và associated indexes được lưu trong file riêng (file_name.ibd). Đây là cấu hình mặc định từ MySQL 5.6.6 trở lên.

```sql
-- Kiểm tra cấu hình
SELECT @@innodb_file_per_table;

-- Chuyển đổi table sang file-per-table
ALTER TABLE sales ENGINE = InnoDB;  -- Sẽ tạo file .ibd mới

-- Transportable Tablespaces
FLUSH TABLES sales FOR EXPORT;
-- Copy .ibd và .cfg files sang location mới
ALTER TABLE sales DISCARD TABLESPACE;
ALTER TABLE sales IMPORT TABLESPACE;
```

#### General Tablespace

Cho phép nhóm nhiều tables vào một tablespace, hữu ích cho việc quản lý space và placement trên different storage.

```sql
-- Tạo general tablespace
CREATE TABLESPACE ts_sales ADD DATAFILE 'ts_sales.ibd';

-- Tạo table trong tablespace
CREATE TABLE orders (
    id BIGINT AUTO_INCREMENT,
    customer_id INT,
    order_date DATE,
    total DECIMAL(10,2),
    PRIMARY KEY (id)
) TABLESPACE ts_sales;

-- Di chuyển table vào tablespace
ALTER TABLE orders TABLESPACE ts_sales;

-- Xem tables trong tablespace
SELECT * FROM information_schema.INNODB_TABLESPACES 
WHERE NAME LIKE 'ts_%';
```

#### Temporary Tablespace

InnoDB sử dụng temporary tablespace cho user-created temporary tables và internal temporary tables được tạo during sorting operations.

```ini
# Cấu hình Temporary Tablespace
[mysqld]
innodb_temp_data_file_path = ibtmp1:12M:autoextend
innodb_temp_tablespaces_dir = /var/lib/mysql/#innodb_temp
```

### 6. Row Formats

InnoDB hỗ trợ nhiều row formats với các đặc điểm khác nhau về space efficiency, performance, và features.

| Row Format | Compact Storage | Variable-Length Columns | Compression | Index Key Prefix Limit |
|------------|-----------------|-------------------------|-------------|------------------------|
| REDUNDANT  | No | No | No | 767 bytes |
| COMPACT    | Yes | Yes | No | 767 bytes |
| DYNAMIC    | Yes | Yes | Yes | 3072 bytes |
| COMPRESSED | Yes | Yes | Yes | 3072 bytes |

#### COMPACT Row Format

```sql
-- Tạo table với COMPACT format
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    price DECIMAL(10,2)
) ENGINE=InnoDB ROW_FORMAT=COMPACT;

-- Variable-length columns được lưu off-page
-- khi row > 16KB page size
```

#### DYNAMIC Row Format

```sql
-- DYNAMIC là default từ MySQL 5.7
CREATE TABLE orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_data JSON,
    notes TEXT,
    metadata VARCHAR(1000)
) ENGINE=InnoDB ROW_FORMAT=DYNAMIC;

-- Variable-length columns luôn được lưu off-page
-- Chỉ lưu 20-byte pointer trong row
```

#### COMPRESSED Row Format

```sql
CREATE TABLE archive_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    log_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB 
ROW_FORMAT=COMPRESSED 
KEY_BLOCK_SIZE=8;

-- Cần cân nhắc trade-off giữa compression ratio và CPU overhead
```

### 7. Redo Log và Undo Log

#### Redo Log

Redo log ghi lại tất cả các thay đổi để đảm bảo durability. Redo logs được write trước (write-ahead logging) và được apply trong quá trình recovery.

```ini
# Cấu hình Redo Log
[mysqld]
innodb_log_file_size = 2G              # Kích thước mỗi log file
innodb_log_files_in_group = 4          # Số lượng log files
innodb_log_group_home_dir = /var/lib/mysql
innodb_flush_log_at_trx_commit = 1     # Durability level (1= safest)
```

Cấu hình `innodb_flush_log_at_trx_commit`:

- **1** (default): Flush redo log và fsync disk sau mỗi commit - đảm bảo ACID
- **2**: Flush redo log sau mỗi commit, fsync định kỳ - trade-off durability/performance
- **0**: Buffer và flush định kỳ - rủi ro mất data cao nhất

```sql
-- Monitoring redo log usage
SHOW ENGINE INNODB STATUS\G
-- Tìm phần "Log sequence number" và "Pages flushed"

-- Kiểm tra checkpoint age
SELECT 
    log.scanned,
    log.not_scanned,
    (log.scanned / (log.scanned + log.not_scanned)) AS scan_ratio
FROM (
    SELECT 
        SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(
            variable_value, ' ', 4), ' ', -1), '.', 1) AS scanned,
        SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(
            variable_value, ' ', 6), ' ', -1), '.', 1) AS not_scanned
    FROM performance_schema.global_status
    WHERE variable_name = 'Innodb_buffer_pool_pages_dirty'
) log;
```

#### Undo Log

Undo log chứa các records cần thiết để rollback transactions và implement consistent reads. Từ MySQL 8.0, undo logs có thể được đặt trong separate tablespaces.

```ini
# Cấu hình Undo Tablespaces
[mysqld]
innodb_undo_tablespaces = 4             # Số lượng undo tablespaces
innodb_undo_directory = /var/lib/mysql/undo
innodb_undo_log_truncate = ON          # Tự động truncate undo logs
```

## Các Best Practices

### 1. Buffer Pool Configuration

```sql
-- Script để resize buffer pool an toàn (online)
SET SESSION innodb_fast_shutdown = 0;   -- Ensure clean shutdown

-- Trong MySQL 8.0+, resize online:
SET GLOBAL innodb_buffer_pool_size = 80G;

-- Kiểm tra resize completion
SHOW STATUS LIKE 'Innodb_buffer_pool_resize%';
```

### 2. Monitoring Key Metrics

```sql
-- Tạo monitoring view
CREATE VIEW innodb_metrics AS
SELECT 
    subsystem,
    name,
    status_value AS value,
    type,
    comment
FROM performance_schema.global_status
JOIN performance_schema.global_status USING (variable_name)
WHERE variable_name LIKE 'Innodb_%'
AND variable_name NOT LIKE '%buffer_pool%'
ORDER BY subsystem, name;

-- Monitoring Buffer Pool hit ratio
SELECT 
    (1 - (
        SELECT variable_value 
        FROM performance_schema.global_status 
        WHERE variable_name = 'Innodb_buffer_pool_reads'
    ) / (
        SELECT variable_value 
        FROM performance_schema.global_status 
        WHERE variable_name = 'Innodb_buffer_pool_read_requests'
    )
) * 100 AS buffer_hit_ratio_pct;

-- Monitoring Page Life Expectancy
SELECT 
    variable_value AS pages_flushed,
    variable_value_prev AS prev_pages_flushed,
    (variable_value - variable_value_prev) AS pages_flushed_per_sec
FROM performance_schema.global_status gs1
JOIN performance_schema.global_status gs2
    ON gs1.variable_name = gs2.variable_name
    AND gs1.variable_name = 'Innodb_buffer_pool_pages_flushed'
WHERE gs1.variable_name = 'Innodb_buffer_pool_pages_flushed';
```

### 3. Tối ưu hóa I/O

```ini
# my.cnf - I/O Optimization
[mysqld]
innodb_read_io_threads = 8             # Cho workloads đọc nhiều
innodb_write_io_threads = 8            # Cho workloads ghi nhiều
innodb_io_capacity = 1000             # SSD: 5000+, HDD: 200-500
innodb_io_capacity_max = 2000
innodb_flush_method = O_DIRECT        # Bỏ qua OS cache (Linux)
innodb_flush_neighbors = 1            # Flush adjacent dirty pages
innodb_max_dirty_pages_pct = 75       # Khi nào bắt đầu flush
innodb_max_dirty_pages_pct_lwm = 10   # Low water mark
```

### 4. Log Configuration

```ini
# my.cnf - Log Optimization
[mysqld]
innodb_log_file_size = 4G             # Lớn hơn cho write-heavy workloads
innodb_log_files_in_group = 3         # Balance giữa safety và performance
innodb_flush_log_at_trx_commit = 1   # 1=safe, 2=faster, 0=fastest

# Monitoring checkpoint
innodb_checkpoint_usability = ON
```

## Các Common Patterns

### Pattern 1: Large Buffer Pool với Multiple Instances

```sql
-- Cấu hình cho server có 128GB RAM
-- Dành 80GB cho buffer pool
-- Chia thành 16 instances (mỗi instance 5GB)

SET GLOBAL innodb_buffer_pool_instances = 16;
SET GLOBAL innodb_buffer_pool_size = 85899345920; -- 80GB in bytes
```

```ini
[mysqld]
innodb_buffer_pool_size = 80G
innodb_buffer_pool_instances = 16
```

### Pattern 2: Dedicated Undo Tablespaces

```sql
-- Tạo dedicated undo tablespaces
-- Thực hiện khi MySQL đang chạy

-- Step 1: Tắt implicit undo logging
SET GLOBAL innodb_undo_log_truncate = OFF;

-- Step 2: Shutdown MySQL
-- systemctl stop mysql

-- Step 3: Thêm cấu hình vào my.cnf
[mysqld]
innodb_undo_tablespaces = 4
innodb_undo_directory = /var/lib/mysql/undo
innodb_undo_log_truncate = ON

-- Step 4: Start MySQL
-- Kiểm tra
SELECT TABLESPACE_NAME, FILE_NAME 
FROM information_schema.INNODB_TABLESPACES 
WHERE TABLESPACE_TYPE = 'UNDO';
```

### Pattern 3: Compressed Tables cho Archive

```sql
-- Tạo compressed archive table
CREATE TABLE app_logs_archive (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    log_level ENUM('DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL'),
    message TEXT,
    context JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created (created_at),
    INDEX idx_level (log_level)
) ENGINE=InnoDB
ROW_FORMAT=COMPRESSED
KEY_BLOCK_SIZE=4
TABLESPACE ts_archive;

-- Partition theo tháng để dễ quản lý
ALTER TABLE app_logs_archive
PARTITION BY RANGE (UNIX_TIMESTAMP(created_at)) (
    PARTITION p_2026_01 VALUES LESS THAN (UNIX_TIMESTAMP('2026-02-01')),
    PARTITION p_2026_02 VALUES LESS THAN (UNIX_TIMESTAMP('2026-03-01')),
    PARTITION p_2026_03 VALUES LESS THAN (UNIX_TIMESTAMP('2026-04-01')),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

### Pattern 4: Monitoring và Alerting

```sql
-- Tạo stored procedure cho health check
DELIMITER //

CREATE PROCEDURE check_innodb_health()
BEGIN
    DECLARE buffer_hit_ratio DECIMAL(5,2);
    DECLARE dirty_pages_pct DECIMAL(5,2);
    DECLARE undo_pages INT;
    
    -- Buffer hit ratio
    SELECT ROUND(
        (1 - (v1.value / v2.value)) * 100, 2
    ) INTO buffer_hit_ratio
    FROM performance_schema.global_status v1
    CROSS JOIN performance_schema.global_status v2
    WHERE v1.variable_name = 'Innodb_buffer_pool_reads'
    AND v2.variable_name = 'Innodb_buffer_pool_read_requests';
    
    -- Dirty pages percentage
    SELECT ROUND(
        (v1.value / v2.value) * 100, 2
    ) INTO dirty_pages_pct
    FROM performance_schema.global_status v1
    CROSS JOIN performance_schema.global_status v2
    WHERE v1.variable_name = 'Innodb_buffer_pool_pages_dirty'
    AND v2.variable_name = 'Innodb_buffer_pool_pages_total';
    
    -- Undo pages
    SELECT COUNT(*) INTO undo_pages
    FROM information_schema.INNODB_TABLESPACES
    WHERE TABLESPACE_TYPE = 'UNDO';
    
    SELECT 
        buffer_hit_ratio AS 'Buffer Hit Ratio %',
        dirty_pages_pct AS 'Dirty Pages %',
        undo_pages AS 'Undo Tablespaces',
        NOW() AS 'Check Time';
END //

DELIMITER ;

-- Usage
CALL check_innodb_health();
```

## Troubleshooting

### Vấn đề 1: Buffer Pool quá nhỏ (OOM)

**Symptom**: MySQL bị kill bởi OOM killer, hoặc buffer pool resize failures.

**Diagnosis**:
```sql
-- Kiểm tra buffer pool size vs data size
SELECT 
    (SELECT @@innodb_buffer_pool_size) / 1024 / 1024 / 1024 AS 'Buffer Pool (GB)',
    (SELECT SUM(data_length + index_length) / 1024 / 1024 / 1024 
     FROM information_schema.tables 
     WHERE engine = 'InnoDB') AS 'Data Size (GB)';
```

**Solution**:
1. Tăng `innodb_buffer_pool_size` nếu có RAM available
2. Tối ưu hóa queries để giảm working set
3. Cân nhắc query caching strategies
4. Partition tables để giảm data size

### Vấn đề 2: High Buffer Pool Page Eviction

**Symptom**: Buffer hit ratio thấp, nhiều disk reads.

**Diagnosis**:
```sql
-- Kiểm tra eviction rate
SHOW ENGINE INNODB STATUS\G
-- Tìm "Pages made young" và "Pages not made young"

-- Hoặc query metrics
SELECT name, count
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10;
```

**Solution**:
1. Tăng buffer pool size
2. Tối ưu hóa queries để sử dụng indexes hiệu quả
3. Giảm `innodb_old_blocks_time` nếu có nhiều full table scans
4. Sử dụng query hints để force index usage

### Vấn đề 3: Excessive Dirty Pages

**Symptom**: Checkpoint warnings, I/O spikes, replication lag.

**Diagnosis**:
```sql
-- Kiểm tra dirty page ratio
SHOW STATUS LIKE 'Innodb_buffer_pool_pages_dirty';

-- Kiểm tra flush rate
SHOW STATUS LIKE 'Innodb_pages_flushed%';

-- Kiểm tra log capacity
SHOW ENGINE INNODB STATUS\G
-- Tìm "Log sequence number" và "Last checkpoint at"
```

**Solution**:
1. Tăng `innodb_io_capacity` và `innodb_io_capacity_max`
2. Tăng `innodb_max_dirty_pages_pct` (nhưng cân nhắc crash recovery time)
3. Tăng `innodb_log_file_size` để cho phép more batching
4. Thay đổi `innodb_flush_neighbors` tùy workload

### Vấn đề 4: InnoDB Tablespace Out of Space

**Symptom**: Error 1114 (Table is full), system tablespace full.

**Diagnosis**:
```sql
-- Kiểm tra tablespace usage
SELECT 
    NAME AS tablespace_name,
    SPACE_TYPE AS type,
    FILE_SIZE / 1024 / 1024 AS file_size_mb,
    TOTAL_EXTENTS,
    FREE_EXTENTS,
    (FREE_EXTENTS / TOTAL_EXTENTS * 100) AS free_pct
FROM information_schema.INNODB_TABLESPACES
JOIN information_schema.INNODB_DATAFILES USING (SPACE);

-- Kiểm tra autoextend status
SHOW VARIABLES LIKE 'innodb_data_file_path';
```

**Solution**:
1. Nếu dùng file-per-table, có thể reclaim space bằng OPTIMIZE TABLE
2. Thêm datafile vào system tablespace
3. Tăng `innodb_temp_data_file_path` size
4. Xóa hoặc archive old data

## Ví dụ Thực tế

### Ví dụ 1: Cấu hình MySQL cho High-Concurrency OLTP

```ini
# my.cnf - High Concurrency OLTP Configuration
[mysqld]
# Buffer Pool
innodb_buffer_pool_size = 64G
innodb_buffer_pool_instances = 8
innodb_buffer_pool_chunk_size = 1G

# I/O
innodb_read_io_threads = 16
innodb_write_io_threads = 16
innodb_io_capacity = 4000
innodb_io_capacity_max = 8000
innodb_flush_method = O_DIRECT
innodb_flush_neighbors = 0            # SSD: disable neighbor flushing

# Locking & Concurrency
innodb_thread_concurrency = 0          # Unlimited
innodb_concurrency_tickets = 5000
innodb_commit_concurrency = 0         # Unlimited

# Log
innodb_log_file_size = 4G
innodb_log_files_in_group = 3
innodb_flush_log_at_trx_commit = 1

# Thread Pool
thread_cache_size = 100
table_open_cache = 10000
table_definition_cache = 8000

# Query Cache (MySQL 5.7 only, removed in 8.0)
# query_cache_type = 0
# query_cache_size = 0
```

### Ví dụ 2: Monitoring Script cho Production

```bash
#!/bin/bash
# mysql_health_check.sh

MYSQL_OPTS="--defaults-file=/etc/mysql/my.cnf -u root"
LOG_FILE="/var/log/mysql/health_check.log"

# Functions
get_buffer_hit_ratio() {
    mysql $MYSQL_OPTS -N -e "
        SELECT ROUND(
            (1 - (v1.value / v2.value)) * 100, 2
        ) AS buffer_hit_ratio
        FROM performance_schema.global_status v1
        CROSS JOIN performance_schema.global_status v2
        WHERE v1.variable_name = 'Innodb_buffer_pool_reads'
        AND v2.variable_name = 'Innodb_buffer_pool_read_requests';"
}

get_dirty_pages() {
    mysql $MYSQL_OPTS -N -e "
        SELECT ROUND(
            (v1.value / v2.value) * 100, 2
        ) AS dirty_pages_pct
        FROM performance_schema.global_status v1
        CROSS JOIN performance_schema.global_status v2
        WHERE v1.variable_name = 'Innodb_buffer_pool_pages_dirty'
        AND v2.variable_name = 'Innodb_buffer_pool_pages_total';"
}

# Main
echo "=== MySQL Health Check - $(date) ===" >> $LOG_FILE
echo "Buffer Hit Ratio: $(get_buffer_hit_ratio)%" >> $LOG_FILE
echo "Dirty Pages: $(get_dirty_pages)%" >> $LOG_FILE

# Check alerts
if [ $(get_buffer_hit_ratio) -lt 95 ]; then
    echo "ALERT: Buffer hit ratio below 95%" | tee -a $LOG_FILE
fi

if [ $(get_dirty_pages) -gt 80 ]; then
    echo "ALERT: Dirty pages above 80%" | tee -a $LOG_FILE
fi
```

### Ví dụ 3: Online Buffer Pool Resize

```sql
-- Step 1: Kiểm tra trạng thái hiện tại
SELECT @@innodb_buffer_pool_size;
SHOW STATUS LIKE 'Innodb_buffer_pool_resize%';

-- Step 2: Resize buffer pool (MySQL 8.0+)
SET GLOBAL innodb_buffer_pool_size = 96 * 1024 * 1024 * 1024; -- 96GB

-- Step 3: Monitor progress
SHOW STATUS LIKE 'Innodb_buffer_pool_resize%';

-- Step 4: Kiểm tra completion trong status
SHOW ENGINE INNODB STATUS\G
-- Tìm dòng "Buffer pool(s) middloaded"

-- Step 5: Verify new size
SELECT @@innodb_buffer_pool_size;
```

## Tham khảo

### Official Documentation

- [InnoDB Architecture](https://dev.mysql.com/doc/refman/8.0/en/innodb-architecture.html)
- [InnoDB Buffer Pool](https://dev.mysql.com/doc/refman/8.0/en/innodb-buffer-pool.html)
- [InnoDB Tablespaces](https://dev.mysql.com/doc/refman/8.0/en/innodb-tablespace.html)
- [InnoDB Row Formats](https://dev.mysql.com/doc/refman/8.0/en/innodb-row-format.html)

### Performance Schema Tables

```sql
-- Useful Performance Schema tables for InnoDB monitoring
SELECT * FROM performance_schema.innodb_buffer_stats_by_schema;
SELECT * FROM performance_schema.innodb_buffer_stats_by_table;
SELECT * FROM performance_schema.innodb_lock_waits;
SELECT * FROM performance_schema.memory_summary_by_account_by_event_name;
```

### Books

- "High Performance MySQL" - Baron Schwartz et al.
- "MySQL Performance Tuning" - Tony Needham

---

*Document version: 1.0.0*
*Last updated: 2026-06-23*
*Framework: Cursor Enterprise Framework*
