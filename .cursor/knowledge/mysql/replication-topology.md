---
title: Replication Topology
description: Kiến trúc Replication - Async Replication, GTID Replication, Semi-synchronous Replication, Multi-source Replication, Replica Lag, Failover
tags: [mysql, replication, gtid, failover, high-availability]
created: 2026-06-23
version: 1.0.0
framework: cursor-enterprise-framework
---

# Replication Topology

## Tổng quan

MySQL Replication là cơ chế cho phép replicate dữ liệu từ một MySQL server (primary/master) sang một hoặc nhiều MySQL servers (replica/slave). Replication là nền tảng cho nhiều kiến trúc enterprise quan trọng bao gồm horizontal scalability, high availability, geographic distribution, và disaster recovery.

Trong môi trường enterprise, replication không chỉ đơn giản là copy dữ liệu. Nó đòi hỏi thiết kế cẩn thận về topology, monitoring, failover strategies, và conflict resolution. Tài liệu này cung cấp hướng dẫn toàn diện về các loại replication topologies và cách triển khai chúng trong production.

## Mục đích của tài liệu

Tài liệu này được viết nhằm giúp các database administrator và system architect:

- Hiểu các loại replication mechanisms khác nhau và trade-offs
- Thiết kế replication topology phù hợp với requirements
- Cấu hình và triển khai replication an toàn
- Implement monitoring và alerting cho replication health
- Plan và execute failover procedures
- Xử lý các vấn đề common replication

## Các Khái niệm Cốt lõi

### 1. Binary Log và Replication Fundamentals

MySQL Replication dựa trên Binary Log (binlog) - một log file ghi lại tất cả các thay đổi dữ liệu. Khi một transaction được commit trên primary, các thay đổi được ghi vào binlog và sau đó được replica đọc và apply.

#### Binary Log Formats

MySQL hỗ trợ ba binlog formats với các đặc điểm khác nhau:

| Format | Description | Pros | Cons |
|--------|-------------|------|------|
| ROW | Ghi thay đổi theo row | Consistent, replicate exact changes | Large log size |
| STATEMENT | Ghi SQL statements | Small log size, some functions work | Non-deterministic issues |
| MIXED | Auto-select ROW/STATEMENT | Best of both | Complex |

```sql
-- Kiểm tra current binlog format
SHOW VARIABLES LIKE 'binlog_format';

-- Đặt binlog format (global hoặc session)
SET GLOBAL binlog_format = 'ROW';
SET SESSION binlog_format = 'MIXED';

-- Cấu hình trong my.cnf
[mysqld]
binlog_format = ROW
binlog_row_image = FULL          -- FULL: ghi toàn bộ row, MINIMAL: chỉ changed columns
binlog_rows_query_log_events = ON  -- Log query events for ROW format
```

```ini
# my.cnf - Binary Log Configuration
[mysqld]
server-id = 1
log_bin = /var/log/mysql/mysql-bin
binlog_format = ROW
binlog_row_image = FULL
binlog_expire_logs_seconds = 604800  # 7 days
max_binlog_size = 1G
binlog_cache_size = 4M
sync_binlog = 1                      # Sync after each transaction (safe but slower)
```

#### Replication Threads

Replication sử dụng nhiều threads trên replica:

- **IO Thread**: Kết nối đến primary, đọc binlog events, và lưu vào relay log
- **SQL Thread (Coordinator)**: Đọc events từ relay log và apply vào database
- **Worker Threads** (nếu dùng parallel replication): Apply events song song

```sql
-- Kiểm tra replication threads
SHOW PROCESSLIST;

-- Output:
-- Id: 45  User: system user  Command: Binlog Dump GTID
-- Id: 47  User: system user  Command: Slave_IO_Running
-- Id: 48  User: system user  Command: Slave_SQL_Running
```

### 2. Async Replication

Async replication là kiểu replication mặc định trong MySQL. Primary commit transaction và gửi binlog events mà không chờ replica nhận và apply.

#### Cách hoạt động

```
Primary (Master)                          Replica (Slave)
    |                                          |
    |  1. BEGIN                                |
    |  2. INSERT INTO orders...                |
    |  3. COMMIT                              |
    |                                          |
    |----binlog events---->   IO Thread        |
    |                            |             |
    |                            v             |
    |                     [Relay Log]          |
    |                            |             |
    |                            v             |
    |                     SQL Thread            |
    |                            |             |
    |                            v             |
    |<---apply--[Database]-------|             |
    |                                          |
```

#### Cấu hình Async Replication

**Trên Primary:**

```sql
-- Enable binary logging và set server ID
SET GLOBAL binlog_format = 'ROW';
SET GLOBAL binlog_expire_logs_seconds = 604800;
SET GLOBAL max_binlog_size = 1073741824;

-- Create replication user
CREATE USER 'repl_user'@'%' IDENTIFIED WITH mysql_native_password BY 'StrongP@ssw0rd!';
GRANT REPLICATION SLAVE ON *.* TO 'repl_user'@'%';
FLUSH PRIVILEGES;

-- Get primary status
SHOW MASTER STATUS;
-- Output:
-- File: mysql-bin.000001
-- Position: 12345
-- Binlog_Do_DB: [database names]
-- Binlog_Ignore_DB: [database names]
-- Executable_GTID_set: [GTID position if GTID enabled]
```

**Trên Replica:**

```sql
-- Set server ID (phải unique trong replication group)
SET GLOBAL server_id = 2;

-- Configure replication source
CHANGE MASTER TO
    MASTER_HOST = 'primary-hostname',
    MASTER_PORT = 3306,
    MASTER_USER = 'repl_user',
    MASTER_PASSWORD = 'StrongP@ssw0rd!',
    MASTER_LOG_FILE = 'mysql-bin.000001',
    MASTER_LOG_POS = 12345,
    MASTER_CONNECT_RETRY = 10,
    MASTER_RETRY_COUNT = 10000,
    GET_MASTER_PUBLIC_KEY = 1;

-- Start replication
START SLAVE;

-- Check replication status
SHOW SLAVE STATUS\G

-- Stop replication if needed
STOP SLAVE;
RESET SLAVE ALL;  -- Xóa configuration
```

```ini
# my.cnf - Replica Configuration
[mysqld]
server-id = 2
relay-log = /var/log/mysql/mysql-relay
relay-log-index = /var/log/mysql/mysql-relay.index
replicate-do-db = myapp
replicate-ignore-db = mysql
replicate-do-table = myapp.orders
replicate-wild-do-table = myapp.orders%
log_replica_updates = ON              # Replica ghi các changes vào local binlog
read_only = ON                        # Chỉ cho phép reads (trừ SUPER users)
super_read_only = ON                  # (MySQL 5.7.26+) Không cho phép cả SUPER users
```

### 3. GTID (Global Transaction Identifier) Replication

GTID là một unique identifier được assign cho mỗi transaction trên primary. GTID giúp replication management đơn giản hơn, failover tự động, và consistent position tracking.

#### GTID Format

```
UUID:sequence_number
Example: A29B7641-E2A1-11E9-8B5D-0800200C9A66:12345
```

- **UUID**: Identifies the source server (server_uuid from SHOW MASTER STATUS)
- **sequence_number**: Monotonically increasing number for each transaction

#### Cấu hình GTID Replication

**Trên Primary:**

```sql
-- Enable GTID mode
SET GLOBAL gtid_mode = OFF_PERMISSIVE;
SET GLOBAL gtid_mode = ON_PERMISSIVE;
SET GLOBAL gtid_mode = ON;

-- Create GTID-enabled replication user
CREATE USER 'repl_gtid'@'%' IDENTIFIED WITH mysql_native_password BY 'StrongP@ssw0rd!';
GRANT REPLICATION SLAVE ON *.* TO 'repl_gtid'@'%';
FLUSH PRIVILEGES;

-- Verify GTID mode
SHOW VARIABLES LIKE 'gtid_mode%';
-- Output:
-- gtid_mode: ON
-- enforce_gtid_consistency: ON
```

```ini
# my.cnf - Primary with GTID
[mysqld]
server-id = 1
log_bin = /var/log/mysql/mysql-bin
binlog_format = ROW
gtid_mode = ON
enforce_gtid_consistency = ON
```

**Trên Replica:**

```sql
-- Enable GTID mode
SET GLOBAL gtid_mode = OFF_PERMISSIVE;
SET GLOBAL gtid_mode = ON_PERMISSIVE;
SET GLOBAL gtid_mode = ON;

-- Configure GTID-based replication
CHANGE MASTER TO
    MASTER_HOST = 'primary-hostname',
    MASTER_PORT = 3306,
    MASTER_USER = 'repl_gtid',
    MASTER_PASSWORD = 'StrongP@ssw0rd!',
    MASTER_AUTO_POSITION = 1,      -- Tự động tính position từ GTID
    GET_MASTER_PUBLIC_KEY = 1;

-- Start replica
START SLAVE;

-- Với GTID, không cần chỉ định MASTER_LOG_FILE và MASTER_LOG_POS
```

```ini
# my.cnf - Replica with GTID
[mysqld]
server-id = 2
gtid_mode = ON
enforce_gtid_consistency = ON
log_slave_updates = ON
relay-log = /var/log/mysql/mysql-relay
```

#### GTID Operations

```sql
-- Skip a single transaction (when needed for error recovery)
SET SESSION gtid_next = 'A29B7641-E2A1-11E9-8B5D-0800200C9A66:12345';
BEGIN;
COMMIT;
SET SESSION gtid_next = AUTOMATIC;

-- Skip multiple transactions
SET GLOBAL gtid_slave_pos = 'A29B7641-E2A1-11E9-8B5D-0800200C9A66:12344';

-- Check executed GTIDs
SHOW MASTER STATUS;
SHOW SLAVE STATUS;

-- Check GTID sets
SELECT @@GLOBAL.gtid_executed;
SELECT @@GLOBAL.gtid_purged;  -- GTIDs đã bị purge từ binlog
```

### 4. Semi-synchronous Replication

Semi-synchronous replication đảm bảo rằng primary đợi ít nhất một replica nhận và write events vào relay log trước khi commit transaction. Điều này giảm risk của data loss nhưng không ảnh hưởng nhiều đến latency.

#### Installation và Configuration

```sql
-- Install semi-sync plugins trên primary
INSTALL PLUGIN rpl_semi_sync_master SONAME 'semisync_master.so';

-- Install semi-sync plugins trên replicas
INSTALL PLUGIN rpl_semi_sync_slave SONAME 'semisync_slave.so';

-- Enable trên primary
SET GLOBAL rpl_semi_sync_master_enabled = ON;
SET GLOBAL rpl_semi_sync_master_timeout = 10000;  -- 10 seconds timeout

-- Enable trên replica
SET GLOBAL rpl_semi_sync_slave_enabled = ON;

-- Restart IO thread trên replica để apply changes
STOP SLAVE IO_THREAD;
START SLAVE IO_THREAD;
```

```ini
# my.cnf - Semi-synchronous Replication
# Trên Primary
[mysqld]
plugin_load_add = semisync_master.so
rpl_semi_sync_master_enabled = 1
rpl_semi_sync_master_timeout = 10000

# Trên Replica
[mysqld]
plugin_load_add = semisync_slave.so
rpl_semi_sync_slave_enabled = 1
```

#### Monitoring Semi-sync

```sql
-- Trên Primary - kiểm tra semi-sync status
SHOW STATUS LIKE 'Rpl_semi_sync_master%';

-- Sample output:
-- Rpl_semi_sync_master_clients: 2              -- Số replicas hỗ trợ semi-sync
-- Rpl_semi_sync_master_net_avg_wait_time: 150
-- Rpl_semi_sync_master_net_waits: 5000
-- Rpl_semi_sync_master_no_times: 10             -- Số lần chuyển sang async
-- Rpl_semi_sync_master_no_tx: 25                -- Số transactions không được ack
-- Rpl_semi_sync_master_status: ON
-- Rpl_semi_sync_master_timefunc_failures: 0
-- Rpl_semi_sync_master_wait_pos_traverse: 5
-- Rpl_semi_sync_master_wait_sessions: 0
-- Rpl_semi_sync_master_yes_tx: 1000             -- Transactions được ack thành công
```

### 5. Multi-source Replication

Multi-source replication cho phép một replica nhận binlog từ nhiều primaries. Điều này hữu ích cho consolidating data từ nhiều sources hoặc real-time reporting.

#### Cấu hình Multi-source Replication

```sql
-- Replica server_id phải unique
SET GLOBAL server_id = 100;

-- Configure channel cho source 1
CHANGE MASTER TO
    MASTER_HOST = 'source1-host',
    MASTER_USER = 'repl_user',
    MASTER_PASSWORD = 'StrongP@ssw0rd!',
    MASTER_AUTO_POSITION = 1,
    FOR CHANNEL 'source_1';

-- Configure channel cho source 2
CHANGE MASTER TO
    MASTER_HOST = 'source2-host',
    MASTER_USER = 'repl_user',
    MASTER_PASSWORD = 'StrongP@ssw0rd!',
    MASTER_AUTO_POSITION = 1,
    FOR CHANNEL 'source_2';

-- Configure channel cho source 3
CHANGE MASTER TO
    MASTER_HOST = 'source3-host',
    MASTER_USER = 'repl_user',
    MASTER_PASSWORD = 'StrongP@ssw0rd!',
    MASTER_AUTO_POSITION = 1,
    FOR CHANNEL 'source_3';

-- Start all channels
START SLAVE;
START SLAVE FOR CHANNEL 'source_1';
START SLAVE FOR CHANNEL 'source_2';
START SLAVE FOR CHANNEL 'source_3';

-- Check all channels
SHOW SLAVE STATUS\G
SHOW SLAVE STATUS FOR CHANNEL 'source_1'\G
```

```ini
# my.cnf - Multi-source Replica
[mysqld]
server-id = 100
gtid_mode = ON
enforce_gtid_consistency = ON
log_slave_updates = ON
relay-log = /var/log/mysql/mysql-relay

# Replication filters (áp dụng cho tất cả channels)
replicate-do-db = consolidated_db
```

#### Monitoring Multi-source

```sql
-- Performance schema tables for multi-source
SELECT * FROM performance_schema.replication_connection_configuration;
SELECT * FROM performance_schema.replication_connection_status;
SELECT * FROM performance_schema.replication_applier_configuration;
SELECT * FROM performance_schema.replication_applier_status;

-- Check lag per channel
SELECT 
    CHANNEL_NAME,
    SERVICE_STATE,
    COUNT_ERRORS,
    LAST_ERROR_NUMBER,
    LAST_ERROR_MESSAGE
FROM performance_schema.replication_connection_status;

-- Check applier status per channel
SELECT 
    CHANNEL_NAME,
    SERVICE_STATE,
    LAST_APPLIED_TRANSACTION,
    LAST_APPLIED_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP,
    APPLYING_TRANSACTION
FROM performance_schema.replication_applier_status_by_worker
WHERE CHANNEL_NAME != 'group_replication_recovery_channel';
```

### 6. Replication Lag

Replication lag là thời gian giữa khi transaction commit trên primary và khi nó được apply trên replica. Lag cao có thể gây ra stale data trên replicas và các vấn đề với read scaling.

#### Nguyên nhân Common

1. **Slow queries trên replica**: Replica đang execute queries chậm
2. **Network latency**: Kết nối giữa primary và replica chậm
3. **Disk I/O bottleneck**: Replica không thể write đủ nhanh
4. **Long transactions**: Large transactions mất nhiều thời gian để replicate
5. **Binary log compression**: Nếu enabled, có thể gây lag

#### Monitoring Lag

```sql
-- Kiểm tra lag từ replica
SHOW SLAVE STATUS\G
-- Seconds_Behind_Master: 0 = up-to-date, NULL = not running
-- Read_Master_Log_Pos: Position trong primary's binlog
-- Relay_Log_Pos: Position trong relay log
-- Exec_Master_Log_Pos: Position đã được applied

-- Sử dụng performance schema (chính xác hơn)
SELECT 
    CHANNEL_NAME,
    LAST_APPLIED_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP,
    LAST_APPLIED_TRANSACTION_IMMEDIATE_COMMIT_TIMESTAMP,
    LAST_APPLIED_TRANSACTION_START_APPLY_TIMESTAMP,
    LAST_APPLIED_TRANSACTION_END_APPLY_TIMESTAMP,
    APPLYING_TRANSACTION,
    APPLYING_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP
FROM performance_schema.replication_applier_status_by_worker;
```

```sql
-- Tạo stored procedure để monitor lag
DELIMITER //

CREATE PROCEDURE check_replication_lag()
BEGIN
    SELECT 
        @@server_id AS current_server_id,
        CHANNEL_NAME,
        SERVICE_STATE AS io_thread_state,
        (
            SELECT SERVICE_STATE 
            FROM performance_schema.replication_connection_status
            WHERE CHANNEL_NAME = 'source_1'
        ) AS sql_thread_state,
        LAST_APPLIED_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP,
        TIMESTAMPDIFF(SECOND, 
            LAST_APPLIED_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP, 
            NOW()
        ) AS lag_seconds,
        COUNT_ERRORS,
        LAST_ERROR_MESSAGE
    FROM performance_schema.replication_applier_status_by_worker
    WHERE CHANNEL_NAME = 'source_1';
END //

DELIMITER ;
```

#### Giảm thiểu Lag

```sql
-- 1. Sử dụng parallel replication
SET GLOBAL slave_parallel_type = 'LOGICAL_CLOCK';
SET GLOBAL slave_parallel_workers = 8;
SET GLOBAL slave_preserve_commit_order = ON;

-- 2. Configure replica to skip certain events
STOP SLAVE;
SET GLOBAL sql_replica_skip_counter = 1;  -- Skip 1 event (dùng cẩn thận!)
START SLAVE;

-- 3. Tăng replica's resources
SET GLOBAL slave_net_timeout = 60;
SET GLOBAL read_buffer_size = 16M;
SET GLOBAL read_rnd_buffer_size = 16M;
```

```ini
# my.cnf - Optimize Replica for less lag
[mysqld]
slave_parallel_type = LOGICAL_CLOCK
slave_parallel_workers = 8
slave_preserve_commit_order = ON
slave_compressed_protocol = ON         # Compress replication traffic
slave_net_timeout = 60
replica_preserve_commit_order = ON

# InnoDB settings for better apply speed
innodb_flush_log_at_trx_commit = 2    # Less strict flushing
innodb_flush_sync = ON
innodb_io_capacity = 1000
innodb_io_capacity_max = 2000
```

### 7. Failover Strategies

Failover là quá trình chuyển đổi từ primary sang replica khi primary gặp sự cố. Có nhiều chiến lược failover với các trade-offs khác nhau.

#### Manual Failover với GTID

```sql
-- Step 1: Đảm bảo replica đã apply tất cả relay logs
STOP SLAVE IO_THREAD;
-- Đợi cho SQL thread apply hết
-- Kiểm tra: SHOW SLAVE STATUS\G (Read_Master_Log_Pos = Exec_Master_Log_Pos)

-- Step 2: Promote replica thành primary
STOP SLAVE;
RESET SLAVE ALL;

-- Step 3: Enable binlog trên new primary
SET GLOBAL read_only = OFF;
SET GLOBAL super_read_only = OFF;
SET GLOBAL log_slave_updates = ON;  -- Nếu replica sẽ là source cho replicas khác

-- Step 4: Update application connection strings
-- Point sang new primary

-- Step 5: Configure other replicas sang new primary
-- (Trên mỗi replica khác)
CHANGE MASTER TO
    MASTER_HOST = 'new-primary-host',
    MASTER_USER = 'repl_user',
    MASTER_PASSWORD = 'StrongP@ssw0rd!',
    MASTER_AUTO_POSITION = 1;
START SLAVE;
```

#### Automatic Failover với MySQL Router và Orchestrator

**Orchestrator** là tool phổ biến để quản lý failover tự động.

```bash
# Install orchestrator
# orchestrator.conf.json configuration
{
  "Debug": false,
  "ListenAddress": ":3000",
  "MySQLTopologyConfig": {
    "MySQLOrchestratorPort": 3306,
    "DiscoverByShowSlaveHosts": true,
    "DiscoverByReplicationUser": true
  },
  "MySQLConnectTimeout": 5,
  "ReplicationLagQuery": "SELECT SLAVE_STATUS.Seconds_Behind_Master",
  "RecoveryPeriodBlockSeconds": 60,
  "RecoveryIgnoreFile": "/etc/orchestrator/recoveryignore",
  "FailureDetectionPeriodBlockMinutes": 10
}
```

```bash
# Commands
orchestrator -c discover                 # Discover cluster
orchestrator -c clusters                 # List clusters
orchestrator -c topology                # Show topology
orchestrator -c graceful-master-takeover  # Graceful failover
orchestrator -c graceful-master-takeover-auto  # Automatic failover
orchestrator -c which-replica-lag       # Check replica lag
```

## Các Best Practices

### 1. Replication Security

```sql
-- Sử dụng dedicated replication user với minimal privileges
CREATE USER 'repl'@'replica-subnet' IDENTIFIED BY 'StrongP@ssw0rd!';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'replica-subnet';
GRANT SELECT ON mysql.rpl_sender_history TO 'monitor'@'monitoring-host';

-- Sử dụng SSL cho replication
CHANGE MASTER TO
    MASTER_SSL = 1,
    MASTER_SSL_CA = '/etc/mysql/certs/ca.pem',
    MASTER_SSL_CERT = '/etc/mysql/certs/client-cert.pem',
    MASTER_SSL_KEY = '/etc/mysql/certs/client-key.pem',
    GET_MASTER_PUBLIC_KEY = 1;

-- Verify SSL
SHOW SLAVE STATUS\G
-- Slave_IO_Running: Connecting hoặc Yes
-- Master_SSL_Allowed: Yes
```

```ini
# my.cnf - SSL Configuration
[client]
ssl-ca = /etc/mysql/certs/ca.pem
ssl-cert = /etc/mysql/certs/client-cert.pem
ssl-key = /etc/mysql/certs/client-key.pem

[mysqld]
ssl-ca = /etc/mysql/certs/ca.pem
ssl-cert = /etc/mysql/certs/server-cert.pem
ssl-key = /etc/mysql/certs/server-key.pem
tls_version = TLSv1.2,TLSv1.3
```

### 2. Monitoring Configuration

```sql
-- Performance Schema replication tables
CREATE TABLE replication_health (
    id INT AUTO_INCREMENT PRIMARY KEY,
    server_id INT,
    channel_name VARCHAR(64),
    io_running VARCHAR(20),
    sql_running VARCHAR(20),
    lag_seconds BIGINT,
    last_error VARCHAR(500),
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stored procedure để record health
DELIMITER //

CREATE PROCEDURE record_replication_health()
BEGIN
    INSERT INTO replication_health (server_id, channel_name, io_running, sql_running, lag_seconds, last_error)
    SELECT 
        @@server_id,
        COALESCE(CHANNEL_NAME, 'default'),
        Service_State,
        (SELECT Service_State FROM performance_schema.replication_connection_status WHERE CHANNEL_NAME = COALESCE(replication_health.channel_name, 'default')),
        TIMESTAMPDIFF(SECOND, 
            (SELECT LAST_APPLIED_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP 
             FROM performance_schema.replication_applier_status_by_worker 
             WHERE CHANNEL_NAME = COALESCE(replication_health.channel_name, 'default') 
             LIMIT 1),
            NOW()
        ),
        (SELECT LAST_ERROR_MESSAGE FROM performance_schema.replication_applier_status WHERE CHANNEL_NAME = COALESCE(replication_health.channel_name, 'default'))
    FROM performance_schema.replication_connection_status;
END //

-- Create event để schedule health checks
CREATE EVENT record_replication_health_event
ON SCHEDULE EVERY 30 SECOND
DO CALL record_replication_health();
```

### 3. Backup Considerations

```sql
-- Khi backup replica (để không ảnh hưởng primary)
STOP SLAVE;
-- Perform backup
START SLAVE;

-- Consistent backup với GTID
SET GTID_PURGED = (SELECT @@GLOBAL.gtid_executed);
-- Bây giờ backup chứa GTID position để restore đúng

-- Backup relay logs (không cần thiết cho restore thông thường)
-- Nhưng useful nếu replica crash trước khi apply
```

## Các Common Patterns

### Pattern 1: Read/Write Splitting với ProxySQL

```ini
# ProxySQL configuration cho read/write splitting

# mysql_servers
INSERT INTO mysql_servers (hostgroup_id, hostname, port, status) VALUES
(10, 'primary-host', 3306, 'MASTER'),
(20, 'replica1-host', 3306, 'SLAVE'),
(20, 'replica2-host', 3306, 'SLAVE');

# mysql_users
INSERT INTO mysql_users (username, password, default_hostgroup) VALUES
('app_user', 'StrongP@ssw0rd!', 10);

# mysql_query_rules
INSERT INTO mysql_query_rules (rule_id, active, match_pattern, destination_hostgroup, comment) VALUES
(1, 1, '^SELECT.*FOR UPDATE', 10, 'Writes FOR UPDATE'),
(2, 1, '^SELECT', 20, 'Reads'),
(3, 1, '^INSERT', 10, 'Inserts'),
(4, 1, '^UPDATE', 10, 'Updates'),
(5, 1, '^DELETE', 10, 'Deletes');
```

### Pattern 2: Cascaded Replication

```
Primary --> Replica1 --> Replica2 --> Replica3
```

```sql
-- Trên Primary
[mysqld]
server-id = 1
log_bin = /var/log/mysql/mysql-bin
binlog_format = ROW

-- Trên Replica1 (intermediate)
[mysqld]
server-id = 2
log_bin = /var/log/mysql/mysql-bin
binlog_format = ROW
log_slave_updates = ON   -- CRITICAL: ghi vào local binlog
relay-log = /var/log/mysql/mysql-relay

-- Trên Replica2
[mysqld]
server-id = 3
log_slave_updates = ON
relay-log = /var/log/mysql/mysql-relay

-- Configure Replica1 to replicate from Primary
CHANGE MASTER TO MASTER_HOST = 'primary-host', MASTER_AUTO_POSITION = 1;

-- Configure Replica2 to replicate from Replica1
CHANGE MASTER TO MASTER_HOST = 'replica1-host', MASTER_AUTO_POSITION = 1;
```

### Pattern 3: Delayed Replication

```sql
-- Configure replica với 1 hour delay
CHANGE MASTER TO MASTER_DELAY = 3600;

-- Check delay configuration
SHOW SLAVE STATUS\G
-- SQL_Delay: 3600

-- Useful cho:
-- - Recover from accidental DROP TABLE (within 1 hour)
-- - Test replication lag impact
-- - Protect against application bugs propagating immediately
```

## Troubleshooting

### Vấn đề 1: Replication Stopped với Error

**Symptom**: `SHOW SLAVE STATUS\G` cho thấy `Slave_IO_Running: No` hoặc `Slave_SQL_Running: No`.

**Diagnosis**:
```sql
SHOW SLAVE STATUS\G
-- Tìm Last_Error, Last_IO_Error, Last_SQL_Error

-- Kiểm tra error logs
-- tail -f /var/log/mysql/error.log
```

**Common Causes và Solutions**:

1. **Duplicate entry**: Conflict trên unique key
```sql
-- Option 1: Skip the error
STOP SLAVE;
SET GLOBAL sql_replica_skip_counter = 1;
START SLAVE;

-- Option 2: Investigate and fix the data
-- Identify the conflicting row
SELECT * FROM problematic_table WHERE id = conflicting_id;
```

2. **Connection lost**: Network issues
```sql
-- Check network connectivity
-- telnet primary-host 3306

-- Adjust timeout values
CHANGE MASTER TO MASTER_CONNECT_RETRY = 30;
START SLAVE;
```

3. **Binlog purged**: Primary đã purge logs mà replica cần
```sql
-- Đồng bộ lại từ đầu
-- Option 1: Nếu có backup
-- Restore backup trên replica và configure lại

-- Option 2: Nếu có another replica up-to-date
-- Point replica này sang other replica
CHANGE MASTER TO MASTER_HOST = 'other-replica-host', MASTER_AUTO_POSITION = 1;
START SLAVE;
```

### Vấn đề 2: High Replication Lag

**Symptom**: `Seconds_Behind_Master` tăng liên tục.

**Diagnosis**:
```sql
-- Kiểm tra replica performance
SHOW PROCESSLIST;
SHOW ENGINE INNODB STATUS\G

-- Kiểm tra network
SHOW SLAVE STATUS\G
-- Kiểm tra Read_Master_Log_Pos vs Exec_Master_Log_Pos

-- IO Thread lag
SELECT 
    CHANNEL_NAME,
    LAST_QUEUED_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP,
    LAST_QUEUED_TRANSACTION_IMMEDIATE_COMMIT_TIMESTAMP,
    QUEUE_SIZE
FROM performance_schema.replication_connection_status;
```

**Solutions**:

1. **Parallel replication settings**
```sql
STOP SLAVE;
SET GLOBAL slave_parallel_type = 'LOGICAL_CLOCK';
SET GLOBAL slave_parallel_workers = 16;
START SLAVE;
```

2. **Optimize replica's InnoDB settings**
```ini
[mysqld]
innodb_flush_log_at_trx_commit = 2
innodb_flush_sync = OFF
innodb_io_capacity = 2000
innodb_io_capacity_max = 4000
```

3. **Slow queries on replica**
```sql
-- Enable slow query log trên replica
SET GLOBAL slow_query_log = 1;
SET GLOBAL slow_query_log_file = '/var/log/mysql/replica-slow.log';
SET GLOBAL long_query_time = 1;

-- Analyze slow queries
-- mysqldumpslow /var/log/mysql/replica-slow.log
```

### Vấn đề 3: GTID Conflicts

**Symptom**: Replication fail với error như "Could not execute write_rows event on table; Duplicate entry".

**Diagnosis**:
```sql
-- Kiểm tra GTID state trên cả primary và replica
SELECT @@GLOBAL.gtid_executed;
SHOW MASTER STATUS;

SELECT @@GLOBAL.gtid_executed;
SHOW SLAVE STATUS;
```

**Solution**:
```sql
-- Option 1: Skip conflicting transaction
SET GTID_NEXT = 'uuid:transaction_number';
BEGIN;
COMMIT;
SET GTID_NEXT = AUTOMATIC;

-- Option 2: Empty conflicting table và replicate lại
DELETE FROM conflicting_table;
-- Replication sẽ tự repopulate

-- Option 3: Skip range of transactions
SET GLOBAL gtid_slave_pos = 'uuid:transaction_number_before_conflict';
START SLAVE;
```

## Ví dụ Thực tế

### Ví dụ 1: Production Replication Setup Script

```bash
#!/bin/bash
# setup_replication.sh

set -e

PRIMARY_HOST="primary.prod.internal"
REPLICA_HOST="replica1.prod.internal"
REPLICA_ID=2
REPLICA_USER="repl_user"
REPLICA_PASSWORD="StrongP@ssw0rd!"

echo "=== Setting up replication ==="

# On Replica: Stop MySQL
systemctl stop mysql

# Generate server UUID for replica
REPLICA_UUID=$(uuidgen)
cat > /etc/mysql/mysql.conf.d/server-uuid.cnf <<EOF
[mysqld]
server_uuid=${REPLICA_UUID}
EOF

# Configure my.cnf
cat > /etc/mysql/mysql.conf.d/replica.cnf <<EOF
[mysqld]
server-id = ${REPLICA_ID}
gtid_mode = ON
enforce_gtid_consistency = ON
log_slave_updates = ON
relay-log = /var/log/mysql/mysql-relay
read_only = ON
super_read_only = ON

# Performance tuning for replica
slave_parallel_type = LOGICAL_CLOCK
slave_parallel_workers = 8
slave_preserve_commit_order = ON
slave_compressed_protocol = ON

# InnoDB settings
innodb_flush_log_at_trx_commit = 2
innodb_io_capacity = 1000
EOF

# Start MySQL
systemctl start mysql

# Get GTID position from primary
GTID_POSITION=$(mysql -h ${PRIMARY_HOST} -u ${REPLICA_USER} -p${REPLICA_PASSWORD} -N -e "SELECT @@GLOBAL.gtid_executed;")

# Configure replication
mysql -e "
CHANGE MASTER TO
    MASTER_HOST = '${PRIMARY_HOST}',
    MASTER_PORT = 3306,
    MASTER_USER = '${REPLICA_USER}',
    MASTER_PASSWORD = '${REPLICA_PASSWORD}',
    MASTER_AUTO_POSITION = 1,
    GET_MASTER_PUBLIC_KEY = 1,
    MASTER_CONNECT_RETRY = 10,
    MASTER_RETRY_COUNT = 10000;
"

# Start replication
mysql -e "START SLAVE;"

# Wait and verify
sleep 5
mysql -e "SHOW SLAVE STATUS\G" | grep -E "Slave_IO_Running|Slave_SQL_Running|Seconds_Behind_Master|Last_Error"

echo "=== Replication setup complete ==="
```

### Ví dụ 2: Monitoring Dashboard Query

```sql
-- Tạo view cho replication monitoring
CREATE OR REPLACE VIEW v_replication_health AS
SELECT 
    ps.connection_status.CHANNEL_NAME,
    ps.connection_status.SERVICE_STATE AS IO_RUNNING,
    ps.applier_status.SERVICE_STATE AS SQL_RUNNING,
    ps.connection_status.COUNT_ERRORS,
    ps.connection_status.LAST_ERROR_MESSAGE,
    ps.connection_status.LAST_QUEUED_TRANSACTION,
    ps.connection_status.LAST_QUEUED_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP,
    ps.applier_status.LAST_APPLIED_TRANSACTION,
    ps.applier_status.LAST_APPLIED_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP,
    TIMESTAMPDIFF(SECOND, 
        ps.applier_status.LAST_APPLIED_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP,
        NOW()
    ) AS LAG_SECONDS,
    ps.applier_status.APPLYING_TRANSACTION,
    ps.applier_status.APPLYING_TRANSACTION_ORIGINAL_COMMIT_TIMESTAMP,
    ps.config.MASTER_HOST,
    ps.config.MASTER_PORT,
    ps.config.MASTER_USER
FROM performance_schema.replication_connection_status AS ps
JOIN performance_schema.replication_applier_status_by_worker AS ps
ON ps.connection_status.CHANNEL_NAME = ps.applier_status.CHANNEL_NAME
JOIN performance_schema.replication_connection_configuration AS ps
ON ps.connection_status.CHANNEL_NAME = ps.config.CHANNEL_NAME;

-- Sử dụng view
SELECT * FROM v_replication_health WHERE LAG_SECONDS > 60;
SELECT * FROM v_replication_health WHERE IO_RUNNING = 'OFF';
```

## Tham khảo

### Official Documentation

- [MySQL Replication](https://dev.mysql.com/doc/refman/8.0/en/replication.html)
- [GTID Replication](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids.html)
- [Semi-synchronous Replication](https://dev.mysql.com/doc/refman/8.0/en/replication-semisync.html)
- [Replication Threads](https://dev.mysql.com/doc/refman/8.0/en/replication-implementation-details.html)
- [Group Replication](https://dev.mysql.com/doc/refman/8.0/en/group-replication.html)

### Performance Schema Tables

```sql
-- Replication monitoring tables
SELECT * FROM performance_schema.replication_connection_configuration;
SELECT * FROM performance_schema.replication_connection_status;
SELECT * FROM performance_schema.replication_applier_configuration;
SELECT * FROM performance_schema.replication_applier_status;
SELECT * FROM performance_schema.replication_applier_status_by_worker;
```

### Tools

- **MySQL Shell**: Advanced replication administration
- **Orchestrator**: Automated failover và topology management
- **MySQL Router**: Read/write splitting
- **Percona Toolkit**: Replication helpers (pt-table-checksum, pt-table-sync)

### Books

- "High Performance MySQL" - Replication chapter
- "MySQL High Availability" - Detailed replication architectures

---

*Document version: 1.0.0*
*Last updated: 2026-06-23*
*Framework: Cursor Enterprise Framework*
