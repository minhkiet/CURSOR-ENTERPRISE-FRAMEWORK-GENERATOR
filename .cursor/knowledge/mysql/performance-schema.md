---
title: Performance Schema
description: Hướng dẫn Performance Schema - Setup, Instrumented Objects, Wait Events, Statement Events, Query Profiling, Sys Schema
tags: [mysql, performance-schema, monitoring, profiling, sys-schema]
created: 2026-06-23
version: 1.0.0
framework: cursor-enterprise-framework
---

# Performance Schema

## Tổng quan

Performance Schema là công cụ instrumentation framework được tích hợp sẵn trong MySQL, cho phép theo dõi và đo lường hiệu suất của server một cách chi tiết. Khác với `EXPLAIN` chỉ cho biết kế hoạch thực thi của query, Performance Schema cung cấp thông tin về actual execution của tất cả operations trong server.

Performance Schema hoạt động bằng cách instrument các điểm quan trọng trong MySQL server code - các functions như file I/O, table locks, synchronization primitives, memory allocations, và nhiều hơn nữa. Mỗi lần một instrumented event xảy ra, Performance Schema có thể thu thập thông tin về event đó và lưu trữ để phân tích sau.

Tài liệu này cung cấp hướng dẫn toàn diện về cách sử dụng Performance Schema hiệu quả để monitor, troubleshoot, và optimize MySQL performance.

## Mục đích của tài liệu

Tài liệu này được viết nhằm giúp các database administrators và developers:

- Hiểu kiến trúc và cách hoạt động của Performance Schema
- Cấu hình và enable các instruments cần thiết
- Sử dụng Performance Schema để phân tích query performance
- Identify bottlenecks trong database operations
- Sử dụng sys schema để đơn giản hóa việc phân tích

## Kiến trúc Performance Schema

### Cấu trúc tổng quan

Performance Schema bao gồm các thành phần chính sau:

1. **Instruments**: Các điểm code được đánh dấu để thu thập timing và count information
2. **Consumers**: Nơi lưu trữ các event đã thu thập
3. **Threads**: Mỗi server thread được theo dõi
4. **Events**: Thông tin về mỗi instrumented operation

```
┌─────────────────────────────────────────────────────────┐
│                   MySQL Server                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Performance Schema                   │  │
│  │                                                  │  │
│  │  ┌─────────────┐    ┌─────────────────────────┐ │  │
│  │  │  Instruments │───▶│    Event Tables        │ │  │
│  │  │  (Code)      │    │  - events_waits_...    │ │  │
│  │  └─────────────┘    │  - events_statements_..│ │  │
│  │                     │  - events_stages_...   │ │  │
│  │                     │  - events_transactions_│ │  │
│  │                     └─────────────────────────┘ │  │
│  │                                                  │  │
│  │  ┌─────────────┐    ┌─────────────────────────┐ │  │
│  │  │  Consumers   │◀───│    Setup Tables        │ │  │
│  │  │  (Filters)   │    │  - setup_consumers     │ │  │
│  │  └─────────────┘    │  - setup_instruments    │ │  │
│  │                     │  - setup_objects        │ │  │
│  │                     └─────────────────────────┘ │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Event Types

| Event Type | Description | Tables |
|------------|-------------|--------|
| Wait Events | File, socket, table I/O, locks | events_waits_* |
| Stage Events | Query execution stages | events_stages_* |
| Statement Events | SQL statements executed | events_statements_* |
| Transaction Events | Transaction lifecycle | events_transactions_* |

### Setup Tables

Performance Schema được điều khiển thông qua các setup tables trong database `performance_schema`:

```sql
-- Các bảng setup quan trọng
SELECT TABLE_NAME 
FROM performance_schema.tables 
WHERE TABLE_SCHEMA = 'performance_schema'
AND TABLE_NAME LIKE 'setup%';
```

```sql
-- Xem tất cả instruments
SELECT 
    NAME,
    ENABLED,
    TIMED,
    PROPERTIES,
    FLAGS
FROM performance_schema.setup_instruments
ORDER BY NAME;
```

```sql
-- Xem tất cả consumers
SELECT 
    NAME,
    ENABLED
FROM performance_schema.setup_consumers
ORDER BY NAME;
```

## Cấu hình Performance Schema

### Enable/Disable Instruments

```sql
-- Enable tất cả wait instruments
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES', TIMED = 'YES'
WHERE NAME LIKE 'wait/%';

-- Enable specific instrument categories
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES', TIMED = 'YES'
WHERE NAME LIKE 'statement/%';

UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES', TIMED = 'YES'
WHERE NAME LIKE 'stage/%';

-- Disable specific instruments
UPDATE performance_schema.setup_instruments
SET ENABLED = 'NO'
WHERE NAME = 'wait/io/table/sql/handler';
```

### Configure Consumers

```sql
-- Enable consumers cho statement profiling
UPDATE performance_schema.setup_consumers
SET ENABLED = 'YES'
WHERE NAME IN (
    'events_statements_current',
    'events_statements_history',
    'events_statements_history_long',
    'events_stages_current',
    'events_stages_history',
    'events_stages_history_long',
    'events_waits_current',
    'events_waits_history',
    'events_waits_history_long'
);

-- Enable global-instrumentation consumers
UPDATE performance_schema.setup_consumers
SET ENABLED = 'YES'
WHERE NAME = 'global_instrumentation';

-- Enable thread-instrumentation
UPDATE performance_schema.setup_consumers
SET ENABLED = 'YES'
WHERE NAME IN ('thread_instrumentation', 'statements_digest');
```

### Configure Object Filtering

```sql
-- Chỉ instrument specific databases/tables
INSERT INTO performance_schema.setup_objects (
    OBJECT_TYPE,
    OBJECT_SCHEMA,
    OBJECT_NAME,
    ENABLED,
    TIMED
) VALUES
('TABLE', 'ecommerce', '%', 'YES', 'YES'),
('TABLE', 'analytics', '%', 'YES', 'YES'),
('PROCEDURE', 'ecommerce', '%', 'YES', 'YES');

-- Disable instrument cho specific objects
INSERT INTO performance_schema.setup_objects (
    OBJECT_TYPE,
    OBJECT_SCHEMA,
    OBJECT_NAME,
    ENABLED,
    TIMED
) VALUES
('TABLE', 'mysql', '%', 'NO', 'NO');
```

### Memory Configuration

```ini
# my.cnf - Performance Schema Memory Configuration
[mysqld]
# Enable Performance Schema (default ON trong MySQL 8.0)
performance_schema = ON

# Memory sizes
performance_schema_events_statements_history_size = 10000
performance_schema_events_statements_history_long_size = 100000
performance_schema_events_waits_history_size = 10000
performance_schema_events_waits_history_long_size = 100000
performance_schema_events_stages_history_size = 10000
performance_schema_events_stages_history_long_size = 100000

# Maximum tables to instrument
performance_schema_max_table_instances = 400

# Maximum file handles
performance_schema_max_file_instances = 10000

# Maximum socket instances
performance_schema_max_socket_instances = 322

# Maximum thread instances
performance_schema_max_thread_instances = 1000

# Statement digests
performance_schema_max_digest_length = 1024
performance_schema_max_digest_sample_age = 60
```

## Các Wait Events

Wait events ghi lại thời gian chờ của các operations như file I/O, locks, và synchronization.

### Wait Event Categories

```sql
-- List all wait event categories
SELECT DISTINCT
    SUBSTRING_INDEX(NAME, '/', 2) AS category
FROM performance_schema.setup_instruments
WHERE NAME LIKE 'wait/%'
ORDER BY category;
```

### File I/O Wait Events

```sql
-- Monitor file I/O performance
SELECT 
    FILE_NAME,
    EVENT_NAME,
    COUNT_READ,
    COUNT_WRITE,
    SUM_NUMBER_OF_BYTES_READ,
    SUM_NUMBER_OF_BYTES_WRITE,
    AVG_TIMER_READ / 1000000000000 AS avg_read_ms,
    AVG_TIMER_WRITE / 1000000000000 AS avg_write_ms
FROM performance_schema.file_summary_BY_INSTANCE
WHERE FILE_NAME IS NOT NULL
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 20;
```

```sql
-- File I/O summary by event type
SELECT 
    EVENT_NAME,
    COUNT_STAR,
    SUM_TIMER_WAIT / 1000000000000 AS total_wait_sec,
    AVG_TIMER_WAIT / 1000000000000 AS avg_wait_ms,
    MAX_TIMER_WAIT / 1000000000000 AS max_wait_ms
FROM performance_schema.events_waits_summary_global_by_event_name
WHERE EVENT_NAME LIKE 'wait/io/file/%'
AND SUM_TIMER_WAIT > 0
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 10;
```

### Table I/O Wait Events

```sql
-- Table I/O statistics
SELECT 
    OBJECT_SCHEMA,
    OBJECT_NAME,
    COUNT_FETCH,
    COUNT_INSERT,
    COUNT_UPDATE,
    COUNT_DELETE,
    SUM_TIMER_FETCH / 1000000000000 AS fetch_sec,
    SUM_TIMER_INSERT / 1000000000000 AS insert_sec,
    SUM_TIMER_UPDATE / 1000000000000 AS update_sec,
    SUM_TIMER_DELETE / 1000000000000 AS delete_sec
FROM performance_schema.table_io_waits_summary_by_table
WHERE OBJECT_SCHEMA NOT IN ('mysql', 'performance_schema', 'information_schema')
AND SUM_TIMER_WAIT > 0
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 20;
```

### Lock Wait Events

```sql
-- Current lock waits
SELECT 
    THREAD_ID,
    EVENT_ID,
    EVENT_NAME,
    OBJECT_SCHEMA,
    OBJECT_NAME,
    INDEX_NAME,
    LOCK_STATUS,
    SOURCE
FROM performance_schema.events_waits_current
WHERE EVENT_NAME LIKE 'wait/lock%'
AND LENGTH(OBJECT_SCHEMA) > 0;

-- Lock wait summary
SELECT 
    OBJECT_SCHEMA,
    OBJECT_NAME,
    INDEX_NAME,
    COUNT_STAR,
    SUM_TIMER_WAIT / 1000000000000 AS total_wait_sec,
    AVG_TIMER_WAIT / 1000000000000 AS avg_wait_ms
FROM performance_schema.events_waits_summary_by_index_usage
WHERE INDEX_NAME IS NOT NULL
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 20;
```

## Các Statement Events

Statement events cung cấp thông tin chi tiết về SQL statements được executed.

### Statement Digest

```sql
-- Summary by query digest (normalized queries)
SELECT 
    DIGEST,
    DIGEST_TEXT,
    COUNT_STAR,
    SUM_TIMER_WAIT / 1000000000000 AS total_sec,
    AVG_TIMER_WAIT / 1000000000000 AS avg_ms,
    SUM_ROWS_EXAMINED,
    SUM_ROWS_SENT,
    SUM_CREATED_TMP_DISK_TABLES,
    SUM_SORT_ROWS,
    SUM_NO_INDEX_USED,
    SUM_NO_GOOD_INDEX_USED
FROM performance_schema.events_statements_summary_by_digest
WHERE DIGEST_TEXT IS NOT NULL
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 20;
```

```sql
-- Recent statements with full text
SELECT 
    THREAD_ID,
    EVENT_ID,
    EVENT_NAME,
    DIGEST,
    DIGEST_TEXT,
    CURRENT_SCHEMA,
    SQL_TEXT,
    TIMER_WAIT / 1000000000000 AS duration_ms,
    ROWS_EXAMINED,
    ROWS_SENT,
    CREATED_TMP_DISK_TABLES,
    NO_INDEX_USED
FROM performance_schema.events_statements_current
WHERE DIGEST_TEXT IS NOT NULL
ORDER BY TIMER_WAIT DESC;
```

### Statement History

```sql
-- Statement history for specific thread
SELECT 
    EVENT_ID,
    EVENT_NAME,
    SOURCE,
    TIMER_START,
    TIMER_END,
    TIMER_WAIT / 1000000000000 AS duration_ms,
    SQL_TEXT,
    DIGEST_TEXT,
    ROWS_EXAMINED,
    ROWS_SENT
FROM performance_schema.events_statements_history
WHERE THREAD_ID = 46
ORDER BY TIMER_START;

-- Long-running statements in history
SELECT 
    THREAD_ID,
    SQL_TEXT,
    TIMER_WAIT / 1000000000000 AS duration_sec,
    ROWS_EXAMINED,
    ROWS_SENT,
    CREATED_TMP_TABLES,
    CREATED_TMP_DISK_TABLES
FROM performance_schema.events_statements_history
WHERE TIMER_WAIT > 30000000000000  -- > 30 seconds
ORDER BY TIMER_WAIT DESC;
```

## Các Stage Events

Stage events cho thấy progression của statement execution qua các stages.

### Common Stages

```sql
-- List all stage events
SELECT 
    NAME,
    ENABLED,
    TIMED
FROM performance_schema.setup_instruments
WHERE NAME LIKE 'stage/%'
ORDER BY NAME;
```

### Stage Summary

```sql
-- Summary by stage
SELECT 
    EVENT_NAME,
    COUNT_STAR,
    SUM_TIMER_WAIT / 1000000000000 AS total_sec,
    AVG_TIMER_WAIT / 1000000000000 AS avg_ms,
    MAX_TIMER_WAIT / 1000000000000 AS max_ms
FROM performance_schema.events_stages_summary_global_by_event_name
WHERE SUM_TIMER_WAIT > 0
ORDER BY SUM_TIMER_WAIT DESC;
```

```sql
-- Stages for specific queries
SELECT 
    THREAD_ID,
    EVENT_NAME,
    WORK_COMPLETED,
    WORK_ESTIMATED,
    SOURCE
FROM performance_schema.events_stages_current
WHERE THREAD_ID IN (
    SELECT THREAD_ID 
    FROM performance_schema.events_statements_current
    WHERE DIGEST_TEXT LIKE '%big join%'
);
```

## Query Profiling

### Using Performance Schema for Profiling

```sql
-- Profile a specific query (enable before executing)
-- Step 1: Enable instrumentation
UPDATE performance_schema.setup_consumers
SET ENABLED = 'YES'
WHERE NAME LIKE 'events_statements_%';

UPDATE performance_schema.setup_consumers
SET ENABLED = 'YES'
WHERE NAME LIKE 'events_stages_%';

UPDATE performance_schema.setup_consumers
SET ENABLED = 'YES'
WHERE NAME LIKE 'events_waits_%';

-- Step 2: Get thread ID
SELECT THREAD_ID FROM performance_schema.threads 
WHERE PROCESSLIST_ID = CONNECTION_ID();

-- Step 3: Execute query (from another session)

-- Step 4: Get statement profile
SELECT 
    EVENT_NAME,
    SOURCE,
    TIMER_WAIT / 1000000000000 AS duration_ms,
    SQL_TEXT
FROM performance_schema.events_statements_history
WHERE THREAD_ID = ?
ORDER BY TIMER_START;

-- Step 5: Get stages for that statement
SELECT 
    es.EVENT_NAME,
    es.TIMER_WAIT / 1000000000000 AS stage_duration_ms,
    es.SQL_TEXT
FROM performance_schema.events_statements_history es
JOIN performance_schema.events_stages_history esh 
    ON es.EVENT_ID = esh.NESTING_EVENT_ID
WHERE es.THREAD_ID = ?
ORDER BY esh.TIMER_START;
```

### Using sys Schema for Profiling

```sql
-- Profile a session's statements
CALL sys.ps_trace_thread('/tmp/statement_trace.json', THREAD_ID);

-- Statement analysis
SELECT * FROM sys.statements_with_full_table_scans
ORDER BY TOTAL_WAIT DESC
LIMIT 10;

SELECT * FROM sys.statements_with_sorting
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 10;

SELECT * FROM sys.statements_with_temp_tables
WHERE DB = 'ecommerce'
ORDER BY CREATED_TMP_DISK_TABLES DESC;
```

## Sys Schema

Sys schema cung cấp các views và stored procedures được thiết kế để đơn giản hóa việc phân tích Performance Schema data.

### Installation

```sql
-- MySQL 8.0: Sys schema được cài đặt sẵn
-- MySQL 5.7: Cần cài đặt thủ công
-- mysql < sys_schema.sql

-- Verify installation
SELECT TABLE_NAME 
FROM information_schema.tables 
WHERE TABLE_SCHEMA = 'sys';
```

### Key Views

```sql
-- Session analysis
SELECT * FROM sys.session;
SELECT * FROM sys.session_by_thread;

-- Wait analysis
SELECT * FROM sys.waits_by_user_by_latency;
SELECT * FROM sys.waits_global_by_latency;

-- Statement analysis
SELECT * FROM sys.statement_analysis;
SELECT * FROM sys.statements_with_errors_or_warnings;
SELECT * FROM sys.statements_with_full_table_scans;
SELECT * FROM sys.statements_with_temp_tables;

-- Table analysis
SELECT * FROM sys.schema_table_statistics;
SELECT * FROM sys.schema_table_statistics_with_buffer;
SELECT * FROM sys.schema_index_statistics;

-- InnoDB analysis
SELECT * FROM sys.innodb_buffer_stats_by_schema;
SELECT * FROM sys.innodb_buffer_stats_by_table;
SELECT * FROM sys.innodb_lock_waits;
```

### Useful Queries

```sql
-- Top 10 slowest statements
SELECT 
    DIGEST,
    SUBSTR(DIGEST_TEXT, 1, 100) AS query,
    COUNT_STAR AS exec_count,
    AVG_TIMER_WAIT / 1000000000000 AS avg_ms,
    SUM_TIMER_WAIT / 1000000000000000 AS total_sec,
    SUM_ROWS_EXAMINED AS rows_scanned
FROM performance_schema.events_statements_summary_by_digest
WHERE DIGEST_TEXT IS NOT NULL
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 10;
```

```sql
-- Find tables with most I/O
SELECT 
    OBJECT_SCHEMA,
    OBJECT_NAME,
    COUNT_FETCH + COUNT_INSERT + COUNT_UPDATE + COUNT_DELETE AS total_io,
    SUM_TIMER_FETCH / 1000000000000 AS fetch_sec,
    SUM_TIMER_WAIT / 1000000000000 AS total_io_sec
FROM performance_schema.table_io_waits_summary_by_table
WHERE OBJECT_SCHEMA NOT IN ('mysql', 'performance_schema', 'information_schema')
AND SUM_TIMER_WAIT > 0
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 20;
```

```sql
-- Find users with most connections
SELECT 
    USER,
    COUNT(*) AS connections,
    SUM(CURRENT_CONNECTIONS) AS current_conns,
    SUM(TOTAL_CONNECTIONS) AS total_conns
FROM sys.user_summary
GROUP BY USER
ORDER BY total_conns DESC;
```

```sql
-- Find InnoDB buffer pool issues
SELECT 
    SUBSTR(FILE, 1, 50) AS file,
    COUNT_READ,
    SUM_NUMBER_OF_BYTES_READ AS bytes_read,
    COUNT_WRITE,
    SUM_NUMBER_OF_BYTES_WRITE AS bytes_write
FROM performance_schema.file_summary_by_instance
WHERE FILE LIKE '%ibd%'
ORDER BY SUM_NUMBER_OF_BYTES_READ DESC
LIMIT 10;
```

## Các Best Practices

### 1. Enable Appropriate Level of Instrumentation

```sql
-- Development/Testing: Full instrumentation
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES', TIMED = 'YES'
WHERE NAME LIKE '%';

UPDATE performance_schema.setup_consumers
SET ENABLED = 'YES';

-- Production: Selective instrumentation
-- Enable only what you need based on troubleshooting objectives
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES', TIMED = 'YES'
WHERE NAME IN (
    'wait/io/file/innodb/innodb_data_file',
    'wait/io/table/sql/handler',
    'statement/abstract/Query',
    'statement/abstract/new_packet',
    'stage/sql/%'
);
```

### 2. Regular Housekeeping

```sql
-- Clear historical data periodically
-- Create event để reset summaries
CREATE EVENT pe_reset_events
ON SCHEDULE EVERY 1 HOUR
DO BEGIN
    -- Clear statement history
    TRUNCATE TABLE performance_schema.events_statements_history;
    TRUNCATE TABLE performance_schema.events_statements_history_long;
    
    -- Clear wait history
    TRUNCATE TABLE performance_schema.events_waits_history;
    TRUNCATE TABLE performance_schema.events_waits_history_long;
    
    -- Clear stage history
    TRUNCATE TABLE performance_schema.events_stages_history;
    TRUNCATE TABLE performance_schema.events_stages_history_long;
END;
```

### 3. Memory Budget Planning

```sql
-- Calculate Performance Schema memory usage
SELECT 
    SUBSTRING_INDEX(NAME, '/', 1) AS subsystem,
    SUM(CURRENT_NUMBER_OF_BYTES_USED) / 1024 / 1024 AS memory_used_mb
FROM performance_schema.memory_summary_global_by_event_name
GROUP BY subsystem
ORDER BY memory_used_mb DESC;

-- Monitor memory consumption
SELECT 
    VARIABLE_NAME,
    VARIABLE_VALUE / 1024 / 1024 AS memory_mb
FROM performance_schema.variables_info
WHERE VARIABLE_NAME LIKE 'performance_schema%size';
```

### 4. Integration với Monitoring

```sql
-- Create view cho monitoring integration
CREATE OR REPLACE VIEW monitoring_replication AS
SELECT 
    CHANNEL_NAME,
    SERVICE_STATE,
    LAST_ERROR_NUMBER,
    LAST_ERROR_MESSAGE,
    LAST_APPLIED_TRANSACTION,
    TIMESTAMPDIFF(SECOND, 
        LAST_APPLIED_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP, 
        NOW()
    ) AS lag_seconds
FROM performance_schema.replication_applier_status_by_worker;

-- Create view cho slow queries
CREATE OR REPLACE VIEW monitoring_slow_queries AS
SELECT 
    DIGEST_TEXT AS query,
    COUNT_STAR AS executions,
    AVG_TIMER_WAIT / 1000000000000 AS avg_duration_ms,
    SUM_TIMER_WAIT / 1000000000000000 AS total_duration_sec,
    SUM_ROWS_EXAMINED AS total_rows_scanned,
    SUM_ROWS_SENT AS total_rows_returned,
    SUM_CREATED_TMP_DISK_TABLES AS disk_tables_created,
    SUM_NO_INDEX_USED AS full_scans
FROM performance_schema.events_statements_summary_by_digest
WHERE DIGEST_TEXT IS NOT NULL
AND AVG_TIMER_WAIT > 100000000000  -- > 100ms
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 50;
```

## Các Common Patterns

### Pattern 1: Identify Bottleneck Query

```sql
-- Step 1: Find the slowest queries overall
SELECT 
    DIGEST_TEXT,
    COUNT_STAR AS exec_count,
    SUM_TIMER_WAIT / 1000000000000000 AS total_sec,
    AVG_TIMER_WAIT / 1000000000000 AS avg_ms
FROM performance_schema.events_statements_summary_by_digest
WHERE DIGEST_TEXT IS NOT NULL
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 10;
```

```sql
-- Step 2: Analyze why it's slow
SELECT 
    DIGEST_TEXT,
    SUM_ROWS_EXAMINED / COUNT_STAR AS avg_rows_scanned,
    SUM_ROWS_SENT / COUNT_STAR AS avg_rows_sent,
    SUM_CREATED_TMP_TABLES AS tmp_tables,
    SUM_CREATED_TMP_DISK_TABLES AS disk_tmp_tables,
    SUM_SORT_ROWS AS total_sorted,
    SUM_NO_INDEX_USED AS full_scans,
    SUM_NO_GOOD_INDEX_USED AS bad_index_scans
FROM performance_schema.events_statements_summary_by_digest
WHERE DIGEST = 'abc123...'  -- Thay bằng digest từ step 1
GROUP BY DIGEST_TEXT;
```

### Pattern 2: Connection Pool Analysis

```sql
-- Analyze active connections
SELECT 
    PROCESSLIST_USER,
    PROCESSLIST_DB,
    COUNT(*) AS connection_count,
    PROCESSLIST_STATE,
    PROCESSLIST_COMMAND
FROM performance_schema.threads
WHERE PROCESSLIST_USER IS NOT NULL
GROUP BY PROCESSLIST_USER, PROCESSLIST_DB, PROCESSLIST_STATE, PROCESSLIST_COMMAND
ORDER BY connection_count DESC;
```

```sql
-- Find blocking connections
SELECT 
    t.PROCESSLIST_ID,
    t.PROCESSLIST_USER,
    t.PROCESSLIST_INFO,
    w.EVENT_ID,
    w.EVENT_NAME,
    w.OBJECT_SCHEMA,
    w.OBJECT_NAME,
    w.SOURCE
FROM performance_schema.events_waits_current w
JOIN performance_schema.threads t ON w.THREAD_ID = t.THREAD_ID
WHERE w.EVENT_NAME LIKE 'wait/lock%'
AND t.PROCESSLIST_ID IS NOT NULL;
```

### Pattern 3: Index Usage Analysis

```sql
-- Tables with full table scans
SELECT 
    OBJECT_SCHEMA,
    OBJECT_NAME,
    COUNT_READ,
    COUNT_FETCH,
    SUM_TIMER_WAIT / 1000000000000 AS wait_sec
FROM performance_schema.table_io_waits_summary_by_table
WHERE OBJECT_SCHEMA NOT IN ('performance_schema', 'information_schema', 'mysql')
AND (COUNT_READ - COUNT_FETCH) > 0  -- Has reads not served by index
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 20;
```

```sql
-- Index statistics
SELECT 
    OBJECT_SCHEMA,
    OBJECT_NAME,
    INDEX_NAME,
    COUNT_FETCH,
    COUNT_INSERT,
    COUNT_UPDATE,
    COUNT_DELETE,
    SUM_TIMER_WAIT / 1000000000000 AS total_wait_sec
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE INDEX_NAME IS NOT NULL
AND OBJECT_SCHEMA = 'ecommerce'
ORDER BY SUM_TIMER_WAIT DESC;
```

### Pattern 4: Memory Leak Detection

```sql
-- Track memory allocation over time
SELECT 
    EVENT_NAME,
    CURRENT_NUMBER_OF_BYTES_USED / 1024 / 1024 AS current_mb,
    HIGH_NUMBER_OF_BYTES_USED / 1024 / 1024 AS high_mb,
    TOTAL_NUMBER_OF_BYTES_USED / 1024 / 1024 AS total_mb
FROM performance_schema.memory_summary_global_by_event_name
WHERE CURRENT_NUMBER_OF_BYTES_USED > 0
ORDER BY CURRENT_NUMBER_OF_BYTES_USED DESC
LIMIT 20;

-- Check for growing allocations
SELECT 
    THREAD_ID,
    EVENT_NAME,
    CURRENT_NUMBER_OF_BYTES_USED,
    HIGH_NUMBER_OF_BYTES_USED,
    CURRENT_NUMBER_OF_BYTES_USED - HIGH_NUMBER_OF_BYTES_USED AS delta
FROM performance_schema.memory_summary_by_thread_by_event_name
WHERE THREAD_ID IN (
    SELECT THREAD_ID FROM performance_schema.threads 
    WHERE PROCESSLIST_USER = 'app_user'
)
AND CURRENT_NUMBER_OF_BYTES_USED > 0
ORDER BY CURRENT_NUMBER_OF_BYTES_USED DESC;
```

## Troubleshooting

### Vấn đề 1: Performance Schema Memory Full

**Symptom**: Performance Schema không thể allocate thêm memory.

**Diagnosis**:
```sql
-- Check current memory usage
SELECT * FROM performance_schema.memory_summary_global_by_event_name
ORDER BY CURRENT_NUMBER_OF_BYTES_USED DESC
LIMIT 10;

-- Check if any limits were reached
SHOW STATUS LIKE 'Performance_schema%';
```

**Solution**:
```sql
-- Tăng memory limits (requires restart)
SET GLOBAL performance_schema_max_table_instances = 1000;
SET GLOBAL performance_schema_max_file_instances = 15000;

-- Hoặc giảm history sizes (online)
SET GLOBAL performance_schema_events_statements_history_size = 1000;
SET GLOBAL performance_schema_events_waits_history_size = 1000;
```

```ini
# my.cnf
[mysqld]
performance_schema_max_table_instances = 1000
performance_schema_max_file_instances = 15000
performance_schema_max_socket_instances = 500
performance_schema_max_thread_instances = 500
```

### Vấn đề 2: Too Much Overhead

**Symptom**: Performance Schema gây overhead đáng kể cho production workload.

**Diagnosis**:
```sql
-- Compare with/without Performance Schema
-- Run: SET GLOBAL performance_schema = 'OFF';

-- Check overhead
SHOW STATUS LIKE 'Performance_schema%';
```

**Solution**:
```sql
-- Disable unnecessary instruments
UPDATE performance_schema.setup_instruments
SET ENABLED = 'NO'
WHERE NAME LIKE 'wait/sync/%'
AND NAME NOT LIKE '%cond%'
AND NAME NOT LIKE '%mutex%'
AND NAME NOT LIKE '%rwlock%';

-- Reduce history sizes
SET GLOBAL performance_schema_events_statements_history_long_size = 10000;
SET GLOBAL performance_schema_events_stages_history_long_size = 10000;
```

### Vấn đề 3: Cannot Find Expected Data

**Symptom**: Query vào Performance Schema tables không trả về expected results.

**Diagnosis**:
```sql
-- Check if instruments are enabled
SELECT NAME, ENABLED, TIMED 
FROM performance_schema.setup_instruments
WHERE NAME LIKE '%specific_instrument%';

-- Check if consumers are enabled
SELECT NAME, ENABLED 
FROM performance_schema.setup_consumers;

-- Check object filters
SELECT * FROM performance_schema.setup_objects;
```

**Solutions**:

1. **Enable missing instruments**
```sql
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES', TIMED = 'YES'
WHERE NAME LIKE '%your_instrument%';
```

2. **Enable missing consumers**
```sql
UPDATE performance_schema.setup_consumers
SET ENABLED = 'YES'
WHERE NAME = 'events_statements_history';
```

3. **Check setup_objects filter**
```sql
-- Remove restrictive filters
DELETE FROM performance_schema.setup_objects
WHERE OBJECT_SCHEMA = 'specific_db';
```

## Ví dụ Thực tế

### Ví dụ 1: Complete Performance Monitoring Setup

```sql
-- Create monitoring user
CREATE USER 'pmm_agent'@'localhost' IDENTIFIED BY 'P@ssw0rd!';
GRANT PROCESS, SELECT ON *.* TO 'pmm_agent'@'localhost';
GRANT SELECT ON performance_schema.* TO 'pmm_agent'@'localhost';
GRANT SELECT ON sys.* TO 'pmm_agent'@'localhost';
```

```sql
-- Create custom monitoring views
CREATE OR REPLACE VIEW v_query_performance AS
SELECT 
    s.digest_text AS query,
    s.count_star AS exec_count,
    ROUND(s.avg_timer_wait / 1000000000000, 2) AS avg_ms,
    ROUND(s.sum_timer_wait / 1000000000000000, 2) AS total_sec,
    s.sum_rows_examined AS rows_scanned,
    s.sum_rows_sent AS rows_sent,
    s.sum_created_tmp_disk_tables AS disk_tables,
    s.sum_no_index_used AS full_scans,
    s.sum_no_good_index_used AS bad_scans
FROM performance_schema.events_statements_summary_by_digest s
WHERE s.digest_text IS NOT NULL
AND s.count_star > 0
ORDER BY s.sum_timer_wait DESC
LIMIT 100;
```

```sql
-- Create table for performance baseline
CREATE TABLE perf_baseline (
    id INT AUTO_INCREMENT PRIMARY KEY,
    metric_name VARCHAR(255),
    metric_value DOUBLE,
    baseline_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY idx_metric (metric_name, baseline_time)
);

-- Create stored procedure to record baseline
DELIMITER //

CREATE PROCEDURE record_performance_baseline()
BEGIN
    INSERT INTO perf_baseline (metric_name, metric_value)
    SELECT 'buffer_pool_hit_ratio', 
           (1 - (SELECT variable_value FROM performance_schema.global_status WHERE variable_name = 'Innodb_buffer_pool_reads') / 
            (SELECT variable_value FROM performance_schema.global_status WHERE variable_name = 'Innodb_buffer_pool_read_requests'))) * 100
    WHERE (SELECT variable_value FROM performance_schema.global_status WHERE variable_name = 'Innodb_buffer_pool_read_requests') > 0;
    
    INSERT INTO perf_baseline (metric_name, metric_value)
    SELECT 'queries_per_second',
           (SELECT variable_value FROM performance_schema.global_status WHERE variable_name = 'Queries');
    
    INSERT INTO perf_baseline (metric_name, metric_value)
    SELECT 'connections',
           (SELECT variable_value FROM performance_schema.global_status WHERE variable_name = 'Threads_connected');
END //

-- Create event for regular baseline collection
CREATE EVENT collect_baseline
ON SCHEDULE EVERY 5 MINUTE
DO CALL record_performance_baseline();
```

### Ví dụ 2: Deep-Dive Query Analysis

```sql
-- Stored procedure for detailed query analysis
DELIMITER //

CREATE PROCEDURE analyze_slow_query(IN p_digest VARCHAR(64))
BEGIN
    DECLARE v_query TEXT;
    
    -- Get the query
    SELECT DIGEST_TEXT INTO v_query
    FROM performance_schema.events_statements_summary_by_digest
    WHERE DIGEST = p_digest;
    
    -- Create temporary table for analysis
    CREATE TEMPORARY TABLE IF NOT EXISTS query_analysis (
        metric VARCHAR(255),
        value VARCHAR(255)
    );
    
    TRUNCATE TABLE query_analysis;
    
    -- Insert summary stats
    INSERT INTO query_analysis
    SELECT 'Query', v_query;
    
    INSERT INTO query_analysis
    SELECT 'Executions', COUNT_STAR
    FROM performance_schema.events_statements_summary_by_digest
    WHERE DIGEST = p_digest;
    
    INSERT INTO query_analysis
    SELECT 'Total Time (sec)', SUM_TIMER_WAIT / 1000000000000000
    FROM performance_schema.events_statements_summary_by_digest
    WHERE DIGEST = p_digest;
    
    INSERT INTO query_analysis
    SELECT 'Avg Time (ms)', AVG_TIMER_WAIT / 1000000000000
    FROM performance_schema.events_statements_summary_by_digest
    WHERE DIGEST = p_digest;
    
    INSERT INTO query_analysis
    SELECT 'Max Time (ms)', MAX_TIMER_WAIT / 1000000000000
    FROM performance_schema.events_statements_summary_by_digest
    WHERE DIGEST = p_digest;
    
    INSERT INTO query_analysis
    SELECT 'Rows Scanned', SUM_ROWS_EXAMINED
    FROM performance_schema.events_statements_summary_by_digest
    WHERE DIGEST = p_digest;
    
    INSERT INTO query_analysis
    SELECT 'Rows Sent', SUM_ROWS_SENT
    FROM performance_schema.events_statements_summary_by_digest
    WHERE DIGEST = p_digest;
    
    INSERT INTO query_analysis
    SELECT 'Disk Temp Tables', SUM_CREATED_TMP_DISK_TABLES
    FROM performance_schema.events_statements_summary_by_digest
    WHERE DIGEST = p_digest;
    
    INSERT INTO query_analysis
    SELECT 'Full Table Scans', SUM_NO_INDEX_USED
    FROM performance_schema.events_statements_summary_by_digest
    WHERE DIGEST = p_digest;
    
    -- Return results
    SELECT * FROM query_analysis;
    
    -- Cleanup
    DROP TEMPORARY TABLE query_analysis;
END //

DELIMITER ;

-- Usage
CALL analyze_slow_query('your-digest-here');
```

### Ví dụ 3: Automated Alerting

```sql
-- Create table for alerts
CREATE TABLE performance_alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alert_type VARCHAR(100),
    metric_name VARCHAR(255),
    threshold_value DOUBLE,
    actual_value DOUBLE,
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_by VARCHAR(100),
    acknowledged_at TIMESTAMP
);

-- Create stored procedure for checking alerts
DELIMITER //

CREATE PROCEDURE check_performance_alerts()
BEGIN
    DECLARE v_buffer_hit DECIMAL(5,2);
    DECLARE v_threads_connected INT;
    DECLARE v_slow_query_count INT;
    DECLARE v_long_trx_count INT;
    
    -- Buffer pool hit ratio
    SELECT ROUND(
        (1 - (SELECT variable_value FROM performance_schema.global_status WHERE variable_name = 'Innodb_buffer_pool_reads') / 
         (SELECT variable_value FROM performance_schema.global_status WHERE variable_name = 'Innodb_buffer_pool_read_requests')) * 100, 2
    ) INTO v_buffer_hit
    FROM DUAL;
    
    IF v_buffer_hit < 95 THEN
        INSERT INTO performance_alerts (alert_type, metric_name, threshold_value, actual_value)
        VALUES ('performance', 'buffer_pool_hit_ratio', 95, v_buffer_hit);
    END IF;
    
    -- Thread connections
    SELECT variable_value INTO v_threads_connected
    FROM performance_schema.global_status
    WHERE variable_name = 'Threads_connected';
    
    IF v_threads_connected > 500 THEN
        INSERT INTO performance_alerts (alert_type, metric_name, threshold_value, actual_value)
        VALUES ('capacity', 'threads_connected', 500, v_threads_connected);
    END IF;
    
    -- Slow queries (> 10 seconds)
    SELECT COUNT(*) INTO v_slow_query_count
    FROM performance_schema.events_statements_summary_by_digest
    WHERE DIGEST_TEXT IS NOT NULL
    AND MAX_TIMER_WAIT > 10000000000000;
    
    IF v_slow_query_count > 10 THEN
        INSERT INTO performance_alerts (alert_type, metric_name, threshold_value, actual_value)
        VALUES ('performance', 'slow_query_count', 10, v_slow_query_count);
    END IF;
    
    -- Long running transactions
    SELECT COUNT(DISTINCT THREAD_ID) INTO v_long_trx_count
    FROM performance_schema.events_transactions_current
    WHERE STATE = 'ACTIVE'
    AND TIME > 60;
    
    IF v_long_trx_count > 0 THEN
        INSERT INTO performance_alerts (alert_type, metric_name, threshold_value, actual_value)
        VALUES ('locks', 'long_transactions', 0, v_long_trx_count);
    END IF;
END //

-- Create event for regular alert checks
CREATE EVENT check_alerts
ON SCHEDULE EVERY 1 MINUTE
DO CALL check_performance_alerts();
```

## Tham khảo

### Official Documentation

- [MySQL Performance Schema](https://dev.mysql.com/doc/refman/8.0/en/performance-schema.html)
- [Performance Schema Configuration](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-configuration.html)
- [Performance Schema Statement Digests](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-statement-digests.html)
- [sys Schema](https://dev.mysql.com/doc/refman/8.0/en/sys-schema.html)

### Performance Schema Tables

```sql
-- List all Performance Schema tables
SELECT TABLE_NAME 
FROM information_schema.tables 
WHERE TABLE_SCHEMA = 'performance_schema'
ORDER BY TABLE_NAME;

-- Key tables
-- setup tables
-- events_waits_current/history/history_long
-- events_stages_current/history/history_long
-- events_statements_current/history/history_long
-- events_transactions_current/history/history_long
-- file_summary_by_instance/by_event_name
-- table_io_waits_summary_by_table/by_index_usage
-- memory_summary_global_by_event_name
-- replication tables
```

### Tools

- **MySQL Workbench**: Visual Performance Schema explorer
- **PMM (Percona Monitoring and Management)**: Comprehensive monitoring
- **MySQL Enterprise Monitor**: Oracle's monitoring solution
- **sys schema**: Built-in analysis views

### Books

- "MySQL Performance Tuning" - Performance Schema chapters
- "High Performance MySQL" - Monitoring and profiling sections

---

*Document version: 1.0.0*
*Last updated: 2026-06-23*
*Framework: Cursor Enterprise Framework*
