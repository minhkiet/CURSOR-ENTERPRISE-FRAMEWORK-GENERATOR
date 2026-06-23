---
title: PostgreSQL Connection Pooling
description: Hướng dẫn toàn diện về PgBouncer configuration, pool modes, connection management, và best practices cho connection pooling
tags: [postgresql, connection-pooling, pgbouncer, transaction-pooling, session-pooling, max-connections]
created: 2026-06-23
version: "1.0"
framework: cursor-enterprise-framework
---

# PostgreSQL Connection Pooling

## Tổng quan

Connection pooling là một kỹ thuật quan trọng trong việc quản lý database connections, đặc biệt quan trọng khi ứng dụng cần xử lý nhiều concurrent requests. Mỗi PostgreSQL connection tiêu tốn tài nguyên đáng kể (memory, CPU), và việc tạo/destroy connections mới là một operation tương đối nặng.

PgBouncer là connection pooler phổ biến nhất cho PostgreSQL. Nó hoạt động như một middleware giữa application và PostgreSQL server, duy trì một pool of persistent connections và reuse chúng cho multiple client sessions.

Trong môi trường enterprise với nhiều application servers và microservices, việc triển khai connection pooling không chỉ giúp tiết kiệm tài nguyên mà còn cải thiện đáng kể throughput và latency của hệ thống.

## Mục đích

Tài liệu này nhằm mục đích:

- Giải thích các pool modes khác nhau và use cases của chúng
- Hướng dẫn cấu hình PgBouncer chi tiết
- Trình bày best practices cho connection management
- Xử lý các vấn đề thường gặp với connection pooling
- Cung cấp monitoring và troubleshooting guides

## Các khái niệm chính

### Tại sao cần Connection Pooling?

**Vấn đề với Direct Connections**:

- PostgreSQL có giới hạn `max_connections` (default: 100)
- Mỗi connection tiêu tốn khoảng 5-10MB memory
- Creating/destroying connections là expensive operation
- Connection setup overhead (authentication, SSL handshake)
- Kernel resource consumption (sockets, file descriptors)

**Lợi ích của Connection Pooling**:

- Reuse connections thay vì create/destroy
- Giảm tài nguyên sử dụng trên PostgreSQL server
- Cải thiện response time
- Better resource management
- Connection limit enforcement

### PgBouncer Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Application │     │ Application │     │ Application │
│    (PHP)    │     │   (Node)    │     │  (Python)   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────▼──────┐
                    │   PgBouncer │
                    │ (Connection │
                    │    Pool)    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  PostgreSQL │
                    │   Server    │
                    └─────────────┘
```

**PgBouncer processes**:

- **Client connection**: Kết nối từ application
- **Server connection**: Kết nối đến PostgreSQL
- **Pool**: Tập hợp server connections cho một database/user combination
- **Transaction mode**: Client được assigned server connection per transaction
- **Session mode**: Client giữ server connection trong suốt session

### Pool Modes

**Session Mode**:

Trong session mode, một server connection được assigned cho client trong suốt lifetime của session. Server connection chỉ được trả về pool khi client disconnect.

```ini
; pgbouncer.ini
pool_mode = session

; Khi nào nên dùng:
; - Application cần session-level features (SET, NOTIFY, LISTEN)
; - Long-running transactions với multiple statements
; - Cần giữ connection state giữa requests
```

```sql
-- Ví dụ session mode usage
-- Client kết nối qua PgBouncer
$ psql -h pgbouncer -p 6432 -U app_user -d mydb

-- SET commands hoạt động bình thường
SET statement_timeout = '30s';

-- NOTIFY/LISTEN hoạt động
LISTEN my_channel;

-- Khi client disconnect, connection được return về pool
```

**Transaction Mode**:

Trong transaction mode, server connection chỉ được assigned cho client trong duration của một transaction. Sau khi transaction kết thúc (COMMIT hoặc ROLLBACK), connection được trả về pool và có thể được reuse cho transaction khác.

```ini
; pgbouncer.ini
pool_mode = transaction

; Các features không hoạt động trong transaction mode:
; - SET (sẽ bị reset sau mỗi transaction)
; - PREPARE (global prepared statements không hoạt động)
; - NOTIFY/LISTEN
; - Advisory locks (có thể release sớm)
; - Cursors (trừ khi trong cùng transaction)
```

```sql
-- Ví dụ transaction mode
-- Query 1: BEGIN
BEGIN;

-- Query 2: SELECT (sử dụng connection A)
SELECT * FROM users WHERE id = 1;

-- Query 3: COMMIT (connection A được return về pool)
COMMIT;

-- Query 4: BEGIN (có thể nhận connection B hoặc A nếu available)
BEGIN;

-- SET trong transaction sẽ không persist
BEGIN;
SET LOCAL statement_timeout = '30s';  -- Chỉ có hiệu lực trong transaction này
SELECT * FROM orders;  -- Timeout 30s
COMMIT;
-- SET đã bị reset
```

**Statement Mode**:

Trong statement mode, server connection được assigned cho mỗi statement. Auto-commit được bật mặc định. Useful cho autocommit mode applications.

```ini
; pgbouncer.ini
pool_mode = statement
server_reset_query = ''  # Không cần trong statement mode
```

### PgBouncer Configuration Files

**pgbouncer.ini**:

```ini
[databases]
; Database aliasing
mydb = host=127.0.0.1 port=5432 dbname=postgres

; Với authentication
mydb = host=127.0.0.1 port=5432 dbname=postgres user=pgbouncer

; Multiple databases
appdb = host=db1.internal port=5432 dbname=app
analytics = host=db2.internal port=5432 dbname=analytics

[pgbouncer]
; Connection settings
listen_addr = *
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

; Pool sizes
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 5

; Timeouts (seconds)
server_login_retry = 15
server_idle_timeout = 600
query_timeout = 0
query_wait_timeout = 30
client_idle_timeout = 0

; Connection lifetime
max_db_connections = 100
max_user_connections = 100

; Logging
log_connections = 0
log_disconnections = 0
log_pooler_errors = 1

; Admin database
admin_users = postgres
stats_users = stats_reader

; Security
server_reset_query = DISCARD ALL
server_check_delay = 30
server_lifetime = 3600
server_connect_timeout = 15
```

**userlist.txt (Authentication file)**:

```text
# Format: "username" "password"
# Password phải là MD5 hash của plaintext password

"app_user" "md5abcdef1234567890abcdef1234567"
"readonly_user" "md5987654321abcdef987654321abcd"

# Hoặc sử dụng haproxy-style passwords
# "username" "password"
"admin" "adminpassword"
```

**Tạo MD5 password**:

```bash
# Cách 1: Sử dụng pg_md5 (comes with PgBouncer)
echo "mypassword" | pg_md5
# Output: md5hash

# Cách 2: Sử dụng psql
psql -c "SELECT 'md5' || md5('mypassword')"
```

### Database-level Configuration

```ini
[databases]
; Override pool settings per database
app_production = host=prod-db port=5432 dbname=app pool_size=50
app_staging = host=staging-db port=5432 dbname=app pool_size=10
app_dev = host=dev-db port=5432 dbname=app pool_size=5

; Với connect string options
mydb = host=127.0.0.1 port=5432 dbname=mydb connect_timeout=30

; Pool mode per database
; (Chỉ hoạt động nếu global pool_mode = transaction)
mydb = host=127.0.0.1 port=5432 dbname=mydb pool_mode=session
```

### User-level Configuration

```ini
[pgbouncer]
; Override pool settings per user
; Format: username = pool_size
admin = pool_size=10
app_reader = pool_size=25
app_writer = pool_size=10
```

### Server Connection String Options

```ini
[databases]
mydb = host=127.0.0.1 \
       port=5432 \
       dbname=postgres \
       user=pgbouncer \
       password=pgbouncer_password \
       connect_timeout=10 \
       client_encoding=UNICODE \
       datestyle='iso, mdy' \
       timezone=UTC
```

## Best Practices

### Sizing Connection Pools

**Quy tắc chung**:

```bash
# Ước tính pool size
# pool_size = (core_count * 2) + effective_spindle_count

# PostgreSQL recommendation:
# max_connections = (max_wal_senders * average_connections_per_replica) + replica_count

# Ví dụ:
# - PostgreSQL server: 16 cores
# - 4 application servers
# - Mỗi app: 25 connections (with pooling)

# Total connections = 4 * 25 = 100
# max_connections = 100 (primary) + connections to replicas
```

**Tính toán pool size**:

```bash
# Công thức cho pool_size
# pool_size = ((core_count * 2) +磁盘数)

# Ví dụ cho DB server:
# - 16 CPU cores
# - SSD storage (1 spindle tương đương)
# - PostgreSQL: 32 max_connections

# Với PgBouncer:
# - max_client_conn = 1000
# - default_pool_size = 25 (4 pools per DB = 100 total connections)

# Rule of thumb:
# - default_pool_size nên nhỏ hơn max_connections / num_databases
# - Giữ reserve_pool cho burst traffic
```

### Configuring for Different Workloads

**OLTP Workload**:

```ini
[pgbouncer]
pool_mode = transaction
default_pool_size = 25
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 3
query_wait_timeout = 30
query_timeout = 60
server_idle_timeout = 600
max_client_conn = 500
```

**Reporting/Analytics**:

```ini
[pgbouncer]
pool_mode = session
default_pool_size = 10
max_client_conn = 100
query_timeout = 3600  # 1 hour for long queries
server_idle_timeout = 3600
```

**Microservices (many small services)**:

```ini
[pgbouncer]
pool_mode = transaction
default_pool_size = 5
min_pool_size = 1
reserve_pool_size = 2
reserve_pool_timeout = 5
query_wait_timeout = 30
max_client_conn = 2000
```

### Authentication Configuration

```ini
[pgbouncer]
; Auth type options:
; - md5: MD5 hashed passwords
; - plain: Plain text passwords (not recommended)
; - cert: Client certificates
; - hba: HBA-style auth (similar to PostgreSQL)
; - trust: No authentication
; - any: Accept any password, use first matching user

auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

; Hoặc sử dụng HBA-style auth
auth_type = hba
auth_hba_file = /etc/pgbouncer/pgb_hba.conf
```

```conf
# pgb_hba.conf (tương tự PostgreSQL HBA)
# type   database   user   address        method

host    all        all    127.0.0.1/32    md5
host    all        all    ::1/128         md5
host    all        all    10.0.0.0/8      md5
host    all        all    192.168.0.0/16   md5

# Cert-based auth
hostssl all        all    0.0.0.0/0       cert clientcert=1
```

### SSL Configuration

```ini
[pgbouncer]
; SSL between clients and PgBouncer
; (PgBouncer không terminate SSL)

; SSL to PostgreSQL
; Sử dụng sslmode trong connection string
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb sslmode=require
```

```bash
# PostgreSQL server cần được cấu hình SSL
# postgresql.conf
ssl = on
ssl_cert_file = '/path/to/server.crt'
ssl_key_file = '/path/to/server.key'
ssl_ca_file = '/path/to/ca.crt'

# pg_hba.conf
hostssl all all 0.0.0.0/0 md5 clientcert=1
```

## Common Patterns

### Pattern 1: Application Connection Strings

```python
# Python (psycopg2)
import psycopg2

conn = psycopg2.connect(
    host='pgbouncer',
    port=6432,
    database='mydb',
    user='app_user',
    password='app_password',
    # Connection pool settings
    connect_timeout=10
)

# Với connection pool (SQLAlchemy)
from sqlalchemy import create_engine

engine = create_engine(
    'postgresql+psycopg2://app_user:pass@pgbouncer:6432/mydb',
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

```javascript
// Node.js (pg)
const { Pool } = require('pg');

const pool = new Pool({
    host: 'pgbouncer',
    port: 6432,
    database: 'mydb',
    user: 'app_user',
    password: 'app_password',
    max: 20,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 5000
});
```

```php
<?php
// PHP (PDO)
$dsn = 'pgsql:host=pgbouncer;port=6432;dbname=mydb';
$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
];

$pdo = new PDO($dsn, 'app_user', 'app_password', $options);

// Với persistent connection (cẩn thận với transaction mode)
$pdo->setAttribute(PDO::ATTR_PERSISTENT, true);
?>
```

### Pattern 2: PgBouncer với Kubernetes

```yaml
# pgbouncer-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pgbouncer
  labels:
    app: pgbouncer
spec:
  replicas: 2
  selector:
    matchLabels:
      app: pgbouncer
  template:
    metadata:
      labels:
        app: pgbouncer
    spec:
      containers:
      - name: pgbouncer
        image: edoburu/pgbouncer:latest
        ports:
        - containerPort: 6432
          name: pgbouncer
        - containerPort: 8080
          name: admin
        env:
        - name: DATABASE_URL
          value: "postgresql://postgres:password@postgres-service:5432/mydb"
        - name: POOL_MODE
          value: "transaction"
        - name: MAX_CLIENT_CONN
          value: "1000"
        - name: DEFAULT_POOL_SIZE
          value: "25"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          tcpSocket:
            port: 6432
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          tcpSocket:
            port: 6432
          initialDelaySeconds: 5
          periodSeconds: 5
```

```yaml
# pgbouncer-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: pgbouncer-service
spec:
  type: ClusterIP
  ports:
  - port: 6432
    targetPort: 6432
    protocol: TCP
  selector:
    app: pgbouncer
---
# Headless service cho PgBouncer discovery (nếu cần)
apiVersion: v1
kind: Service
metadata:
  name: pgbouncer-headless
spec:
  clusterIP: None
  ports:
  - port: 6432
    targetPort: 6432
  selector:
    app: pgbouncer
```

### Pattern 3: PgBouncer Admin và Monitoring

```sql
-- Kết nối đến PgBouncer admin database
-- psql -h pgbouncer -p 6432 -U pgbouncer pgbouncer

-- Xem pools
SHOW POOLS;

-- Xem clients
SHOW CLIENTS;

-- Xem servers
SHOW SERVERS;

-- Xem config
SHOW CONFIG;

-- Xem version
SHOW VERSION;

-- Xem lists
SHOW LISTS;

-- Xem help
SHOW HELP;
```

```sql
-- Detailed pool info
SHOW DATABASES;
SHOW USERS;

-- Realtime stats
SELECT 
    database,
    pool_size,
    free,
    used,
    reserved,
    maxwait,
    maxwait_us
FROM pg_stat_pooler;
```

### Pattern 4: Prepared Statements

**Vấn đề với Prepared Statements trong Transaction Mode**:

```sql
-- Trong transaction mode, prepared statements không hoạt động như mong đợi
-- vì connection được released sau mỗi transaction

-- WRONG - prepared statement bị mất giữa transactions
BEGIN;
PREPARE stmt AS SELECT * FROM users WHERE id = $1;
EXECUTE stmt(1);
COMMIT;
BEGIN;
EXECUTE stmt(2);  -- Lỗi! Statement không tồn tại
COMMIT;
```

**Giải pháp 1: Sử dụng Prepared Statements ngay trong query**:

```sql
-- Sử dụng unnamed prepared statement (vẫn có vấn đề)
PREPARE stmt (int) AS SELECT * FROM users WHERE id = $1;
EXECUTE stmt(1);
DEALLOCATE stmt;
```

**Giải pháp 2: Sử dụng Function**:

```sql
-- Tạo function thay vì prepared statement
CREATE OR REPLACE FUNCTION get_user(p_user_id BIGINT)
RETURNS SETOF users AS $$
BEGIN
    RETURN QUERY SELECT * FROM users WHERE id = p_user_id;
END;
$$ LANGUAGE plpgsql STABLE;

-- Gọi function
SELECT * FROM get_user(1);
```

**Giải pháp 3: Sử dụng Session Mode cho specific connections**:

```ini
[databases]
# Use session mode for this specific connection
app_with_prepared = host=127.0.0.1 port=5432 dbname=mydb pool_mode=session
```

## Troubleshooting

### Vấn đề 1: "no more connections allowed"

**Triệu chứng**: Application nhận được lỗi "no more connections allowed" hoặc "pooler error: no more connections in pool"

**Nguyên nhân**: Tất cả connections trong pool đang được sử dụng, không còn available connection.

**Giải pháp**:

```sql
-- 1. Kiểm tra PgBouncer stats
SHOW POOLS;

-- 2. Kiểm tra xem có clients đang wait không
SHOW CLIENTS;

-- 3. Kiểm tra server connections
SHOW SERVERS;

-- Output example:
-- database |  user  | pool_mode | pool_size | free | used | reserved
-- ---------|--------|-----------|-----------|------|------|----------
-- mydb     | app    | session   |        25 |    5 |   20 |        0

-- 4. Tăng pool size
ALTER DATABASE mydb SET pool_size = 50;

-- 5. Hoặc kiểm tra application có connection leak không
```

**Configuration fix**:

```ini
[pgbouncer]
max_client_conn = 2000
default_pool_size = 50
reserve_pool_size = 10
query_wait_timeout = 30  # Timeout cho waiting clients
```

### Vấn đề 2: High latency với PgBouncer

**Triệu chứng**: Queries chậm hơn khi đi qua PgBouncer.

**Giải pháp**:

```bash
# 1. Kiểm tra network latency
ping pgbouncer
ping postgresql

# 2. Kiểm tra PgBouncer resource usage
top -p $(pgrep pgbouncer)

# 3. Kiểm tra log cho errors
tail -f /var/log/pgbouncer/pgbouncer.log

# 4. Tối ưu PgBouncer settings
# - Tăng worker processes nếu single-threaded
# - Sử dụng unix socket thay vì TCP cho local connections
```

```ini
[pgbouncer]
; Tăng worker threads/processes
; PgBouncer có thể chạy multithreaded hoặc multi-process

; Unix socket thay vì TCP
listen_addr = /var/run/pgbouncer
listen_port = 6432
; Client connect: /var/run/pgbouncer/.s.PGSQL.6432
```

### Vấn đề 3: Connections không được released

**Triệu chứng**: Pool có used connections cao nhưng không giảm.

**Nguyên nhân**: Application không properly close connections/transactions.

**Giải pháp**:

```sql
-- 1. Identify idle sessions in PostgreSQL
SELECT 
    pid,
    usename,
    application_name,
    state,
    query_start,
    state_change
FROM pg_stat_activity
WHERE state != 'idle'
AND application_name LIKE '%pgbouncer%'
ORDER BY query_start;

-- 2. Check PgBouncer clients
SHOW CLIENTS;

-- 3. Check transactions
SHOW TRANSACTIONS;

-- 4. Terminate problematic PostgreSQL backend
SELECT pg_terminate_backend(pid);

-- 5. Check application code cho connection leaks
```

```python
# Python - Always use context manager
with pool.connect() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
# Connection được trả về pool tự động

# WRONG - Connection leak
conn = pool.connect()
cur = conn.cursor()
cur.execute("SELECT 1")
# conn không được close!
```

### Vấn đề 4: Authentication failures

**Giải pháp**:

```bash
# 1. Verify userlist.txt format
cat /etc/pgbouncer/userlist.txt
# "username" "md5hash"

# 2. Generate correct MD5 hash
echo -n "password" | md5sum
# Hoặc từ PostgreSQL:
psql -c "SELECT 'md5' || md5('password')"

# 3. Reload PgBouncer
ps aux | grep pgbouncer
kill -HUP pgbouncer_pid

# 4. Verify PgBouncer can connect to PostgreSQL
psql -h pgbouncer -p 6432 -U pgbouncer -c "SHOW VERSION"
```

## Ví dụ minh họa

### Ví dụ 1: Production PgBouncer Setup

```bash
#!/bin/bash
# setup_pgbouncer.sh

# 1. Install PgBouncer
apt-get update && apt-get install -y pgbouncer

# 2. Create configuration
cat > /etc/pgbouncer/pgbouncer.ini << 'EOF'
[databases]
* = host=127.0.0.1 port=5432

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
auth_query = SELECT usename, passwd FROM pg_shadow WHERE usename = $1

; Pool settings
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 5

; Timeouts
server_login_retry = 15
server_idle_timeout = 600
query_wait_timeout = 30
query_timeout = 0
client_idle_timeout = 0

; Connection management
server_lifetime = 3600
server_idle_timeout = 600
server_connect_timeout = 15
server_fast_close = off

; Reset query
server_reset_query = DISCARD ALL

; Logging
log_connections = 0
log_disconnections = 0
log_pooler_errors = 1

; Admin
admin_users = postgres
stats_users = monitoring
EOF

# 3. Create userlist with PostgreSQL users
cat > /etc/pgbouncer/userlist.txt << 'EOF'
"postgres" "md5passwordhash"
"app_user" "md5passwordhash"
"readonly" "md5passwordhash"
EOF

# 4. Enable and start
systemctl enable pgbouncer
systemctl start pgbouncer

# 5. Test
psql -h localhost -p 6432 -U postgres -d pgbouncer -c "SHOW VERSION;"
```

### Ví dụ 2: PgBouncer với HAProxy

```conf
# haproxy.cfg

frontend postgres_cluster
    bind *:5432
    default_backend pgpool

backend pgpool
    balance leastconn
    option httpchk
    http-check expect status 200
    
    # PgBouncer instances
    server pgbouncer1 pgbouncer1:6432 check inter 5s rise 2 fall 3
    server pgbouncer2 pgbouncer2:6432 check inter 5s rise 2 fall 3 backup
    
    # Connection settings
    maxconn 1000
    timeout server 3600s
    timeout connect 10s
    timeout client 3600s
```

### Ví dụ 3: Monitoring PgBouncer with Prometheus

```yaml
# Prometheus scrape config for PgBouncer
scrape_configs:
  - job_name: 'pgbouncer'
    static_configs:
      - targets: ['pgbouncer:8080']
    metrics_path: /metrics
```

```python
# Python exporter for custom PgBouncer metrics
#!/usr/bin/env python3
from prometheus_client import start_http_server, Gauge
import psycopg2
import time

pgb_pool_clients = Gauge('pgbouncer_pool_clients', 'Number of clients in pool',
                        ['database', 'user', 'pool_mode'])
pgb_pool_free = Gauge('pgbouncer_pool_free', 'Number of free connections in pool',
                      ['database', 'user'])
pgb_pool_used = Gauge('pgbouncer_pool_used', 'Number of used connections in pool',
                     ['database', 'user'])

def collect_metrics():
    conn = psycopg2.connect(
        host='pgbouncer',
        port=6432,
        database='pgbouncer',
        user='monitoring'
    )
    cur = conn.cursor()
    cur.execute('SHOW POOLS')
    
    for row in cur.fetchall():
        database, user, pool_mode, pool_size, free, used, reserved, _, _, _ = row
        pgb_pool_clients.labels(database=database, user=user, pool_mode=pool_mode).set(pool_size)
        pgb_pool_free.labels(database=database, user=user).set(free)
        pgb_pool_used.labels(database=database, user=user).set(used)
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    start_http_server(9090)
    while True:
        collect_metrics()
        time.sleep(15)
```

## References

### Official Documentation
- [PgBouncer Documentation](https://www.pgbouncer.org/)
- [PgBouncer Config](https://www.pgbouncer.org/config.html)
- [PgBouncer Admin](https://www.pgbouncer.org/admin.html)
- [PostgreSQL Connection Settings](https://www.postgresql.org/docs/current/runtime-config-connection.html)

### Best Practices
- Scale connections proportionally với CPU cores
- Use transaction mode for OLTP workloads
- Monitor pool utilization regularly
- Set appropriate timeouts to prevent stuck connections
- Use `server_reset_query = DISCARD ALL` in session mode

### Tools
- **pgb_top**: Real-time PgBouncer monitoring
- **pgbouncer_exporter**: Prometheus exporter for PgBouncer
- **OmniDB**: Web-based PostgreSQL management tool với PgBouncer support
