---
title: PostgreSQL Replication và High Availability
description: Hướng dẫn toàn diện về streaming replication, logical replication, physical replication, và các giải pháp HA như PgPool và Patroni
tags: [postgresql, replication, high-availability, streaming-replication, logical-replication, patroni, pgpool]
created: 2026-06-23
version: "1.0"
framework: cursor-enterprise-framework
---

# PostgreSQL Replication và High Availability

## Tổng quan

Replication và High Availability (HA) là hai thành phần quan trọng trong việc xây dựng một PostgreSQL infrastructure đáng tin cậy và có khả năng mở rộng. Replication đảm bảo rằng data được copy giữa các servers, trong khi HA đảm bảo rằng database luôn sẵn sàng phục vụ ngay cả khi một node gặp sự cố.

PostgreSQL cung cấp nhiều loại replication khác nhau, mỗi loại phù hợp với các use cases khác nhau. Streaming replication là lựa chọn phổ biến nhất cho việc tạo read replicas và đảm bảo high availability. Logical replication cho phép replicate ở mức database objects, rất hữu ích cho việc migrate data hoặc tạo distributed databases.

Trong môi trường enterprise, việc triển khai replication không chỉ đơn giản là copy data mà còn bao gồm việc quản lý failover tự động, load balancing, và đảm bảo data consistency giữa các nodes.

## Mục đích

Tài liệu này nhằm mục đích:

- Giải thích chi tiết các loại replication trong PostgreSQL
- Hướng dẫn setup và configure streaming replication
- Trình bày logical replication và các use cases của nó
- So sánh synchronous vs asynchronous replication
- Cung cấp hướng dẫn triển khai HA với Patroni và PgPool
- Cung cấp best practices cho việc vận hành replicated clusters

## Các khái niệm chính

### Streaming Replication

Streaming replication là phương pháp replication phổ biến nhất trong PostgreSQL, cho phép standby server nhận WAL (Write-Ahead Logging) records một cách liên tục từ primary server. Điều này tạo ra near real-time copies của primary database.

**Các thành phần chính**:

- **WAL (Write-Ahead Logging)**: PostgreSQL ghi tất cả thay đổi vào WAL trước khi apply vào database files
- **WAL Sender**: Process trên primary gửi WAL records
- **WAL Receiver**: Process trên standby nhận và apply WAL records
- **Replication Slot**: Đảm bảo WAL records không bị xóa cho đến khi standby đã nhận

**Cấu hình trên Primary**:

```conf
# postgresql.conf trên primary server

# Replication settings
wal_level = replica  # hoặc 'logical' cho logical replication
max_wal_senders = 10  # Số lượng replication connections tối đa
max_replication_slots = 10  # Số lượng replication slots
wal_keep_size = 1GB  # Kích thước WAL giữ lại cho replicas
hot_standby = on  # Cho phép read queries trên standby

# Listen on replication connections
listen_addresses = '*'

# Replication user
wal_log_hints = on  # Cần thiết cho some replication scenarios
```

**Cấu hình pg_hba.conf cho replication**:

```
# Replication connections
# IPv4 local connections
host    replication     replicator          127.0.0.1/32            md5
host    replication     replicator          ::1/128                 md5

# Allow standby connections from specific IPs
host    replication     replicator          10.0.1.0/24             md5
```

**Tạo Replication User và Slot**:

```sql
-- Tạo replication user
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'strong_password';

-- Tạo replication slot
SELECT * FROM pg_create_physical_replication_slot('standby_slot');

-- Kiểm tra slots
SELECT slot_name, slot_type, active, restart_lsn 
FROM pg_replication_slots;
```

**Setup Standby Server**:

```bash
# 1. Create base backup từ primary
pg_basebackup -h primary_host -U replicator -D /var/lib/postgresql/data \
    -P -Xs -R -S standby_slot

# Flags:
# -h: Primary host
# -U: Replication user
# -D: Destination directory
# -P: Show progress
# -Xs: Include WAL files (required for streaming)
# -R: Create standby.signal (marks as standby)
# -S: Replication slot name

# 2. Nếu không dùng -R flag, tạo standby.signal manually
touch /var/lib/postgresql/data/standby.signal

# 3. Tạo/kiểm tra primary_conninfo trong postgresql.auto.conf
# (pg_basebackup tự động tạo nếu có slot)
```

### Physical Replication

Physical replication (còn gọi là streaming replication) copy toàn bộ physical files của database. Đây là phương pháp replication binary-level, không có selectivity.

**Ưu điểm**:

- Đơn giản, reliable
- Tất cả changes được replicate (bao gồm DDL, DML, ACLs)
- Performance tốt

**Nhược điểm**:

- Không thể replicate subset của database
- Không hỗ trợ selective replication
- Không thể replicate sang different PostgreSQL version

### Logical Replication

Logical replication cho phép replicate ở mức database objects (tables, sequences). Nó sử dụng publish-subscribe model và có thể replicate giữa different PostgreSQL versions và platforms.

**Cấu hình Logical Replication**:

```conf
# postgresql.conf trên publisher
wal_level = logical
max_replication_slots = 10
max_wal_senders = 10
```

**Tạo Publication (Publisher side)**:

```sql
-- Tạo publication cho specific tables
CREATE PUBLICATION my_publication FOR TABLE users, orders, products;

-- Publication cho all tables (trừ một số)
CREATE PUBLICATION app_publication FOR ALL TABLES;

-- Publication với row filters
CREATE PUBLICATION active_users_pub FOR TABLE users 
    WHERE (status = 'active');

-- Publication với column filters
CREATE PUBLICATION users_pub FOR TABLE users (id, email, name);
```

**Tạo Subscription (Subscriber side)**:

```sql
-- Tạo subscription
CREATE SUBSCRIPTION my_subscription
    CONNECTION 'host=primary_host port=5432 dbname=mydb user=replicator password=xxx'
    PUBLICATION my_publication
    WITH (copy_data = true, enabled = true);

-- Kiểm tra subscription status
SELECT * FROM pg_subscription;

-- Xem subscription stats
SELECT 
    s.subname,
    s.subenabled,
    sr.subrecv_lsn,
    sr.sublast_endpos,
    sr.subslot_name
FROM pg_subscription s
JOIN pg_stat_replication_slots sr ON s.oid = sr.slot_id;
```

### Synchronous vs Asynchronous Replication

**Synchronous Replication**:

Đảm bảo rằng transaction chỉ được committed khi data đã được ghi vào cả primary và ít nhất một standby. Đảm bảo zero data loss nhưng có thể tăng latency.

```conf
# postgresql.conf trên primary
synchronous_commit = on  # hoặc remote_write, remote_apply
synchronous_standby_names = 'standby1,standby2'  # Danh sách synchronous standbys
```

**Asynchronous Replication**:

Transaction được committed ngay khi được ghi vào primary, không cần chờ standby. Nhanh hơn nhưng có thể mất data nếu primary fail trước khi WAL được gửi đến standby.

```conf
# Asynchronous replication (default)
synchronous_commit = local
synchronous_standby_names = ''
```

**Synchronous Commit Modes**:

```conf
# Các chế độ synchronous_commit:
# off: Asynchronous, transaction commit không chờ WAL写入
# local: Chờ local WAL flush (default)
# remote_write: Chờ standby nhận và write WAL (không chờ fsync)
# on: Chờ standby nhận và flush WAL
# remote_apply: Chờ standby apply và visible
```

**Cấu hình Quorum Commit**:

```conf
# Quorum synchronous replication
synchronous_standby_names = 'ANY 2 (standby1, standby2, standby3)'

# Với priority
synchronous_standby_names = 'standby1,standby2,standby3'
```

### Cascade Replication

Cascade replication cho phép một standby nhận WAL từ một standby khác thay vì trực tiếp từ primary. Hữu ích trong các deployments lớn với nhiều tiers.

```conf
# Trên intermediate standby
# Enable nhận replication connections
wal_level = replica
max_wal_senders = 5
hot_standby = on
```

```bash
# Setup cascade standby
pg_basebackup -h intermediate_standby -U replicator -D /var/lib/postgresql/cascade \
    -P -Xs -R
```

### PgPool-II

PgPool-II là middleware cho PostgreSQL cung cấp connection pooling, load balancing, automatic failover, và replication support.

**Cấu hình PgPool-II**:

```conf
# pgpool.conf

# Connection Pooling
pooling_mode = transaction  # or session
num_init_children = 32
max_pool = 4

# Load Balancing
load_balance_mode = on
black_function_list = 'nextval,setval,pgpool_backend_ping'
white_function_list = 'nextval,setval'

# Replication Mode
replication_mode = off
enable_pool_hba = on
pool_passwd = 'pool_passwd'

# Backend Configuration
backend_hostname0 = 'primary'
backend_port0 = 5432
backend_weight0 = 1
backend_data_directory0 = '/var/lib/postgresql/data'
backend_flag0 = 'ALWAYS_MASTER'

backend_hostname1 = 'standby1'
backend_port1 = 5432
backend_weight1 = 1
backend_data_directory1 = '/var/lib/postgresql/standby1'

backend_hostname2 = 'standby2'
backend_port2 = 5432
backend_weight2 = 1
backend_data_directory2 = '/var/lib/postgresql/standby2'

# Watchdog (HA)
use_watchdog = on
onlieserver = on
```

**pcp.conf cho PgPool administration**:

```bash
# Tạo hashed password
pg_md5 your_password
# Output: hashed_password

# Thêm vào pcp.conf
echo "postgres:hashed_password" >> /etc/pgpool-II/pcp.conf
```

### Patroni

Patroni là một template cho việc tạo custom HA solutions cho PostgreSQL. Nó sử dụng distributed consensus (thường là etcd, Consul, hoặc ZooKeeper) để quản lý failover tự động.

**Cấu hình Patroni với etcd**:

```yaml
# config.yml
scope: postgres-cluster
namespace: /service/
name: postgres-1

restapi:
  listen: 0.0.0.0:8008
  connect_address: postgres-1:8008

etcd:
  hosts: etcd-1:2379,etcd-2:2379,etcd-3:2379
  username: etcd_user
  password: etcd_password

postgresql:
  listen: 0.0.0.0:5432
  connect_address: postgres-1:5432
  data_dir: /var/lib/postgresql/data
  
  authentication:
    superuser:
      username: postgres
      password: superuser_password
    replication:
      username: replicator
      password: replicator_password
  
  parameters:
    wal_level: replica
    max_wal_senders: 10
    max_replication_slots: 10
    hot_standby: on
  
  create_replica_methods:
    - basebackup
  
  basebackup:
    - checkpoint: 'fast'
    - label: 'slot replication'
    - max-rate: '100M'
    - no-password

consul:
  hosts: consul-1:8500,consul-2:8500,consul-3:8500
  username: consul_user
  password: consul_password
```

**Patroni API**:

```bash
# Check cluster status
patronictl -c /etc/patroni.yml list

# Manual failover
patronictl -c /etc/patroni.yml failover

# Switchover (planned migration)
patronictl -c /etc/patroni.yml switchover

# Restart PostgreSQL
patronictl -c /etc/patroni.yml restart postgres-cluster postgres-1
```

## Best Practices

### Thiết kế Replication Topology

```
                    ┌─────────────┐
                    │  Primary    │
                    │  (Writer)   │
                    └──────┬──────┘
                           │ WAL Stream
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Standby 1│ │ Standby 2│ │ Standby 3│
        │(Sync HA) │ │(Async RO)│ │(Async RO)│
        └──────────┘ └──────────┘ └──────────┘
```

### Giám sát Replication Lag

```sql
-- Kiểm tra replication lag trên primary
SELECT 
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    (sent_lsn - replay_lsn) AS replication_lag
FROM pg_stat_replication;

-- Kiểm tra replication slot lag
SELECT 
    slot_name,
    slot_type,
    restart_lsn,
    (pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) / 1024 / 1024) AS lag_mb
FROM pg_replication_slots
WHERE active = true;

-- Kiểm tra received but not applied
SELECT 
    slot_name,
    confirmed_flush_lsn
FROM pg_replication_origin_status;

-- Monitor lag với monitoring query
SELECT 
    application_name,
    state,
    sent_lsn,
    replay_lsn,
    write_lsn,
    flush_lsn,
    sync_state,
    (pg_wal_lsn_diff(sent_lsn, replay_lsn) / 1024 / 1024)::numeric(10,2) AS lag_mb,
    (pg_wal_lsn_diff(sent_lsn, replay_lsn) / 1024 / 1024 / 1024)::numeric(10,2) AS lag_gb
FROM pg_stat_replication
ORDER BY lag_mb DESC;
```

### Xử lý Replication Conflicts

```sql
-- Kiểm tra replication conflicts
SELECT * FROM pg_stat_database_conflicts;

-- Conflict có thể xảy ra với:
-- 1. Primary key conflicts (duplicate key)
-- 2. Update/Delete conflicts (row not found)
-- 3. Tablespace conflicts
-- 4. Lock conflicts

-- Giải pháp: Cấu hình hot_standby_feedback
-- Trong postgresql.conf trên standby:
hot_standby_feedback = on
vacuum_defer_cleanup_age = 10000

-- Hoặc sử dụng replication slots để prevent WAL deletion
```

### Backup Strategy với Replication

```bash
# Setup pgBackRest cho backup với replicas
# Repository configuration
[global]
repo1-type=s3
repo1-s3-bucket=my-bucket
repo1-s3-region=us-east-1
repo1-path=/postgresql/backups
repo1-retention-full=2
repo1-retention-diff=7
repo1-retention-arch=14

# Stanza configuration
[db]
db-host=primary
db-user=postgres
db-path=/var/lib/postgresql/16/main
db1-port=5432

# Backup từ replica để giảm load trên primary
[db:standby]
db1-host=standby
```

## Common Patterns

### Pattern 1: Read-Write Splitting

```sql
-- Application-level routing
-- Ví dụ connection string

-- Primary (writes):
postgresql://app:password@primary:5432/mydb

-- Standby (reads):
postgresql://app:password@standby1:5432/mydb

-- PgBouncer setup cho automatic routing
-- pgpool.conf với load balancing
backend_weight0 = 0  # Primary - no load balance
backend_weight1 = 1  # Standby - load balanced
backend_weight2 = 1  # Standby - load balanced
```

### Pattern 2: Automatic Failover với pgpool

```conf
# pgpool.conf - Failover configuration

# Backend status file
backend_clustering_mode = 'streaming replication'
failover_command = '/etc/pgpool/failover.sh %d %H'

# Health check
health_check_period = 10
health_check_timeout = 20
health_check_user = 'pgpool'
health_check_password = 'pgpool_password'
health_check_database = 'postgres'
health_check_max_retries = 3
```

```bash
#!/bin/bash
# failover.sh
# Arguments: node_id new_primary_host

FAILED_NODE=$1
NEW_PRIMARY=$2

echo "Failover triggered for node $FAILED_NODE, promoting $NEW_PRIMARY" | logger

# Các bước promotion được xử lý bởi PgPool tự động
# Script này có thể dùng để notify các services khác

# Notify load balancer
curl -X POST http://api-gateway/failover -d "node=$FAILED_NODE&new_primary=$NEW_PRIMARY"

# Update DNS (nếu cần)
sed -i "s/primary.*/primary\tIN\tCNAME\t$NEW_PRIMARY/" /etc/bind/zones/db.example.com
```

### Pattern 3: Logical Replication với Conflict Resolution

```sql
-- Tạo subscription với conflict handling
CREATE SUBSCRIPTION orders_sub
    CONNECTION 'host=primary port=5432 dbname=mydb user=replicator'
    PUBLICATION orders_pub
    WITH (origin = 'none');

-- Kiểm tra subscription ddlirection
SELECT subname, subpublications, subenabled FROM pg_subscription;

-- Handle conflicts bằng cách tạo trigger trên subscriber
CREATE OR REPLACE FUNCTION handle_replication_conflict()
RETURNS TRIGGER AS $$
BEGIN
    -- Last-write-wins strategy
    IF NEW.updated_at > OLD.updated_at THEN
        RETURN NEW;
    ELSE
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER orders_replication_conflict
    BEFORE UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION handle_replication_conflict();
```

## Troubleshooting

### Vấn đề 1: Replication Lag quá lớn

**Triệu chứng**: Replication lag tăng liên tục, standby không catch up được.

**Nguyên nhân có thể**:

- Network bandwidth insufficient
- Standby server quá yếu
- Heavy write workload trên primary
- Disk I/O bottleneck trên standby

**Giải pháp**:

```sql
-- 1. Kiểm tra lag hiện tại
SELECT 
    application_name,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    sync_state
FROM pg_stat_replication;

-- 2. Kiểm tra xem standby có đang catch up không
SELECT 
    now() - pg_last_xact_replay_timestamp() AS replication_delay;

-- 3. Tăng wal_keep_size nếu cần
-- ALTER SYSTEM SET wal_keep_size = '2GB';

-- 4. Sử dụng replication slot thay vì wal_keep_size
SELECT pg_create_physical_replication_slot('standby_slot');
-- Sau đó gắn slot này vào standby

-- 5. Tăng parallel workers cho apply
-- PostgreSQL 16+: parallel apply
-- ALTER SYSTEM SET max_logical_replication_workers = 8;
-- ALTER SYSTEM SET max_worker_processes = 16;
```

### Vấn đề 2: Replication bị ngắt kết nối

**Triệu chứng**: Replication state thay đổi sang "streaming" rồi "catchup" rồi lại ngắt.

**Giải pháp**:

```bash
# 1. Kiểm tra pg_hba.conf trên primary
# Đảm bảo standby IP được allowed

# 2. Kiểm tra firewall
sudo firewall-cmd --list-all

# 3. Test connection từ standby
psql -h primary -U replicator -c "SELECT 1"

# 4. Kiểm tra max_wal_senders
SHOW max_wal_senders;

# 5. Restart replication
# Trên standby:
pg_ctl restart -D /var/lib/postgresql/data -w
```

### Vấn đề 3: Promote Standby không thành công

**Triệu chứng**: pg_ctl promote fails hoặc Patroni không promote được.

**Giải pháp**:

```bash
# 1. Kiểm tra xem có promotion đang diễn ra không
pg_controldata /var/lib/postgresql/data

# 2. Manual promote
pg_ctl promote -D /var/lib/postgresql/data

# 3. Hoặc tạo trigger file
touch /var/lib/postgresql/data/promote
# PostgreSQL sẽ detect file này và promote

# 4. Sau khi promote:
# - Update pg_hba.conf trên new primary
# - Setup replication từ new primary đến old primary
# - Update connection strings
```

### Vấn đề 4: pg_stat_replication không hiển thị standby

**Giải pháp**:

```sql
-- 1. Kiểm tra pg_stat_replication
SELECT * FROM pg_stat_replication;

-- 2. Kiểm tra standby signal file
SELECT pg_is_in_recovery();

-- 3. Kiểm tra pg_log
SELECT pg_read_file('postgresql.log', -1, -1);

-- 4. Manual start replication
-- Trên standby:
pg_ctl start -D /var/lib/postgresql/data -l /var/lib/postgresql/logfile

-- 5. Kiểm tra primary_conninfo
SHOW primary_conninfo;
```

## Ví dụ minh họa

### Ví dụ 1: Setup Streaming Replication Cluster

```bash
#!/bin/bash
# setup_replication.sh

PRIMARY_HOST="10.0.1.10"
STANDBY_HOST="10.0.1.11"
REPLICATOR_PASS="replicator_strong_password"
PG_VERSION="16"
PG_DATA="/var/lib/postgresql/${PG_VERSION}/main"

# Step 1: Configure Primary
ssh postgres@${PRIMARY_HOST} << 'EOF'
cat >> /etc/postgresql/${PG_VERSION}/main/postgresql.conf << 'CONF'
# Replication settings
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
wal_keep_size = 1GB
hot_standby = on
listen_addresses = '*'
CONF

# Add replication user
psql -c "CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD '${REPLICATOR_PASS}';"

# Create replication slot
psql -c "SELECT pg_create_physical_replication_slot('standby_slot');"

# Update pg_hba.conf
echo "host    replication     replicator      ${STANDBY_HOST}/32         md5" >> /etc/postgresql/${PG_VERSION}/main/pg_hba.conf

# Reload PostgreSQL
sudo systemctl reload postgresql
EOF

# Step 2: Create Base Backup
ssh postgres@${STANDBY_HOST} << 'EOF'
sudo -u postgres pg_basebackup -h ${PRIMARY_HOST} -U replicator -D ${PG_DATA} \
    -P -Xs -R -S standby_slot -w

# Set permissions
sudo chown -R postgres:postgres ${PG_DATA}

# Start standby
sudo systemctl start postgresql
EOF

# Step 3: Verify Replication
ssh postgres@${PRIMARY_HOST} << 'EOF'
psql -c "SELECT client_addr, state, sent_lsn FROM pg_stat_replication;"
EOF
```

### Ví dụ 2: Patroni Cluster Setup

```bash
#!/bin/bash
# setup_patroni.sh

# Prerequisites
apt-get update && apt-get install -y postgresql patroni etcd

# Create Patroni configuration
cat > /etc/patroni.yml << 'EOF'
scope: postgres-cluster
namespace: /service/
name: node-1

restapi:
  listen: 0.0.0.0:8008
  connect_address: node-1:8008
  authentication:
    username: patroni
    password: patroni_password

etcd:
  hosts: etcd-1:2379,etcd-2:2379,etcd-3:2379
  username: etcd_user
  password: etcd_password

postgresql:
  listen: 0.0.0.0:5432
  connect_address: node-1:5432
  data_dir: /var/lib/postgresql/data
  authentication:
    superuser:
      username: postgres
      password: postgres_password
    replication:
      username: replicator
      password: replicator_password
  parameters:
    wal_level: replica
    max_wal_senders: 10
    max_replication_slots: 10
    hot_standby: on
    wal_keep_size: 1GB
  create_replica_methods:
    - basebackup
  basebackup:
    - checkpoint: fast
    - max-rate: '100M'
    - no-password

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pg_rewind: true
  initdb:
  - encoding: UTF8
  - locale: en_US.UTF-8
  - data-checksums
  users:
    admin:
      password: admin_password
      options:
        - createrole
        - createdb
EOF

# Start Patroni
systemctl enable patroni
systemctl start patroni

# Verify cluster
patronictl -c /etc/patroni.yml list
```

### Ví dụ 3: Monitoring Replication với Prometheus

```sql
-- Install pg_exporter collector functions
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Create monitoring view
CREATE OR REPLACE VIEW pg_replication_metrics AS
SELECT 
    application_name,
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    sync_state,
    (sent_lsn - replay_lsn) AS lag_bytes,
    (sent_lsn - replay_lsn)::numeric / 1024 / 1024 AS lag_mb,
    backend_xmin,
    backend_start,
    now() - backend_start AS connection_age
FROM pg_stat_replication;

-- Export for Prometheus
CREATE OR REPLACE FUNCTION pg_replication_lag()
RETURNS TABLE (
    slot_name text,
    lag_bytes bigint
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        slot_name,
        (sent_lsn - restart_lsn) AS lag_bytes
    FROM pg_stat_replication 
    JOIN pg_replication_slots USING (slot_name)
    WHERE active;
END;
$$ LANGUAGE plpgsql;
```

```conf
# prometheus.yml scrape config
scrape_configs:
  - job_name: 'postgresql'
    static_configs:
      - targets: ['postgres-exporter:9187']
    metrics_path: /metrics
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
```

## References

### Official Documentation
- [PostgreSQL High Availability](https://www.postgresql.org/docs/current/high-availability.html)
- [Streaming Replication](https://www.postgresql.org/docs/current/warm-standby.html)
- [Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html)
- [PgPool-II Documentation](http://www.pgpool.net/docs/latest/en/html/index.html)
- [Patroni Documentation](https://patroni.readthedocs.io/en/latest/)

### Tools
- **PgPool-II**: Connection pooling, load balancing, replication
- **Patroni**: HA solution với distributed consensus
- **pglogical**: Advanced logical replication (2ndQuadrant)
- **BDR**: Bi-directional replication (2ndQuadrant)
- **pg_backrest**: Backup and restore tool

### Books và Resources
- "PostgreSQL 16 Administration Cookbook" - Simon Riggs
- "The Replication Specialist" - Gabriele Bartolini
- PostgreSQL wiki về Replication
- pgsql-hackers mailing list
