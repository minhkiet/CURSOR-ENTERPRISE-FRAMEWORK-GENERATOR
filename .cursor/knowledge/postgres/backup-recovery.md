---
title: PostgreSQL Backup và Recovery
description: Hướng dẫn toàn diện về pg_dump, pg_basebackup, WAL archiving, Point-in-Time Recovery (PITR), pgBackRest, và Barman
tags: [postgresql, backup, recovery, pitr, pgbackrest, barman, wal, wal-archiving]
created: 2026-06-23
version: "1.0"
framework: cursor-enterprise-framework
---

# PostgreSQL Backup và Recovery

## Tổng quan

Backup và recovery là một trong những khía cạnh quan trọng nhất của database administration. Không có backup strategy hoàn chỉnh, rủi ro mất dữ liệu có thể gây ra hậu quả nghiêm trọng cho business.

PostgreSQL cung cấp nhiều phương pháp backup phù hợp với các use cases khác nhau:

- **Logical backups** (pg_dump): Export database objects thành SQL statements hoặc archive format
- **Physical backups** (pg_basebackup): Copy toàn bộ data files
- **Continuous archiving** (WAL): Enable point-in-time recovery

Trong môi trường enterprise, việc triển khai backup strategy đáng tin cậy là requirement bắt buộc, thường được mandate bởi SLA và compliance requirements.

## Mục đích

Tài liệu này nhằm mục đích:

- Giải thích các phương pháp backup khác nhau trong PostgreSQL
- Hướng dẫn setup và configure continuous archiving
- Trình bày Point-in-Time Recovery (PITR) procedures
- Cung cấp hướng dẫn sử dụng pgBackRest và Barman
- Trình bày backup verification và testing procedures
- Cung cấp best practices cho backup management

## Các khái niệm chính

### Logical Backup với pg_dump

pg_dump là công cụ logical backup phổ biến nhất, tạo ra file chứa SQL statements để recreate database.

```bash
# Basic pg_dump
pg_dump -h localhost -U postgres -d mydb -f backup.sql

# Compressed backup
pg_dump -h localhost -U postgres -d mydb | gzip > backup.sql.gz

# Custom format (parallel backup, incremental)
pg_dump -h localhost -U postgres -d mydb -Fc -f backup.dump

# Directory format (parallel)
pg_dump -h localhost -U postgres -d mydb -Fd -j 4 -f backup_directory

# Only schema (no data)
pg_dump -h localhost -U postgres -d mydb --schema-only -f schema.sql

# Only data
pg_dump -h localhost -U postgres -d mydb --data-only -f data.sql

# Specific tables
pg_dump -h localhost -U postgres -d mydb -t users -t orders -f tables.sql

# Exclude tables
pg_dump -h localhost -U postgres -d mydb --exclude-table=logs -f backup.sql
```

```bash
# pg_dump options
# -h: Host
# -p: Port
# -U: Username
# -d: Database name
# -f: Output file
# -F: Format (p=plain, c=custom, d=directory, t=tar)
# -j: Number of parallel jobs (directory format)
# -Z: Compression level (0-9)
# --no-owner: Skip ownership commands
# --no-acl: Skip access control commands
# --schema-only: Only schema
# --data-only: Only data
# -t: Table pattern
# --exclude-table: Exclude table pattern
```

### pg_dumpall cho Cluster-level Backup

```bash
# Backup all databases và global objects
pg_dumpall -h localhost -U postgres -f cluster_backup.sql

# Chỉ backup roles và tablespaces
pg_dumpall -h localhost -U postgres --roles-only -f roles.sql
pg_dumpall -h localhost -U postgres --tablespaces-only -f tablespaces.sql

# Backup passwords (requires superuser)
pg_dumpall -h localhost -U postgres --passwords -f auth.sql
```

### Restore từ pg_dump

```bash
# Restore plain SQL
psql -h localhost -U postgres -d mydb -f backup.sql

# Restore compressed
gunzip -c backup.sql.gz | psql -h localhost -U postgres -d mydb

# Restore custom format
pg_restore -h localhost -U postgres -d mydb -v backup.dump

# Restore to different database
pg_restore -h localhost -U postgres -d mydb_new -v backup.dump

# Restore specific objects from custom format
pg_restore -h localhost -U postgres -d mydb -t users -t orders backup.dump

# Drop và recreate database
pg_restore -h localhost -U postgres -C -d postgres backup.dump

# Parallel restore
pg_restore -h localhost -U postgres -d mydb -j 4 backup_directory/
```

### Physical Backup với pg_basebackup

pg_basebackup tạo binary copy của PostgreSQL data directory:

```bash
# Basic physical backup
pg_basebackup -h localhost -U postgres -D /backup/base -Ft -z -P

# Flags:
# -h: Host
# -U: Replication user
# -D: Destination directory
# -Ft: Tar format (có thể dùng -Fp cho plain format)
# -z: Compress
# -P: Show progress
# -X: Include required WAL files (stream hoặc fetch)

# Backup với replication slot
pg_basebackup -h localhost -U postgres -D /backup/base -Xs -R -S backup_slot -P

# Backup với tablespace mapping
pg_basebackup -h localhost -U postgres -D /backup/base -Tt '/pgdata/tablespace1=/backup/tablespace1'

# Incremental backup (chỉ backup changes từ last checkpoint)
pg_basebackup -h localhost -U postgres -D /backup/base --incremental
```

```bash
# Checkpoint backup với WAL
pg_basebackup -h localhost -U postgres \
    -D /var/backups/postgresql/base \
    -Ft \
    -z \
    -P \
    -X stream \
    -R
```

### Continuous Archiving (WAL Archiving)

WAL archiving là nền tảng cho Point-in-Time Recovery:

```conf
# postgresql.conf

# Enable WAL archiving
wal_level = replica  # hoặc archive cho older versions
archive_mode = on

# Archive command
archive_command = 'test ! -f /archive/wal/%f && cp %p /archive/wal/%f'

# Hoặc sử dụng streaming (pg_receivewal)
archive_command = ''

# WAL settings
wal_keep_size = 1GB  # Giữ ít nhất 1GB WAL
max_wal_size = 1GB
min_wal_size = 80MB

# Checkpoints
checkpoint_timeout = 10min
max_wal_senders = 10
```

```bash
# Archive command với rsync
archive_command = 'rsync -a %p postgres@backup-server:/archive/wal/%f'

# Archive command với cloud storage
archive_command = 'aws s3 cp %p s3://my-bucket/wal/%f'

# Archive command với compression
archive_command = 'gzip -c %p > /archive/wal/%f.gz'
```

### pg_receivewal cho Streaming WAL

```bash
# Stream WAL to archive (thay thế archive_command)
pg_receivewal -h localhost -U postgres -D /archive/wal -v

# Với compression
pg_receivewal -h localhost -U postgres -D /archive/wal -z -v

# Với replication slot
pg_receivewal -h localhost -U postgres -S backup_slot -D /archive/wal -v

# Systemd service
cat > /etc/systemd/system/pg-receivewal.service << 'EOF'
[Unit]
Description=PostgreSQL WAL Receiver
After=postgresql.service

[Service]
User=postgres
ExecStart=/usr/bin/pg_receivewal -D /archive/wal -h localhost -U postgres -S backup_slot -v
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

## Point-in-Time Recovery (PITR)

PITR cho phép khôi phục database đến bất kỳ thời điểm nào trong quá khứ:

### Setup PITR Infrastructure

```conf
# postgresql.conf cho PITR

# Archive settings
wal_level = replica
archive_mode = on
archive_command = 'test ! -f /archive/wal/%f && cp %p /archive/wal/%f'
archive_timeout = 300  # Force archive mỗi 5 phút

# Replication slot để đảm bảo WAL không bị xóa
max_replication_slots = 5

# Recovery target settings
restore_command = 'cp /archive/wal/%f %p'
recovery_target_action = 'promote'
```

```bash
# Create replication slot cho backup
psql -h localhost -U postgres -c "SELECT pg_create_physical_replication_slot('backup_slot');"
```

### Performing Point-in-Time Recovery

```bash
# Step 1: Stop PostgreSQL
sudo systemctl stop postgresql

# Step 2: Backup current data (trong trường hợp cần rollback)
sudo cp -a /var/lib/postgresql/data /backup/pre-recovery-$(date +%Y%m%d%H%M%S)

# Step 3: Clear data directory
sudo rm -rf /var/lib/postgresql/data/*
sudo rm -f /var/lib/postgresql/data/recovery.signal

# Step 4: Restore base backup
pg_basebackup -h localhost -U postgres -D /var/lib/postgresql/data -X stream -R

# Step 5: Create recovery.conf (PostgreSQL < 12)
# PostgreSQL >= 12: Sử dụng postgresql.conf hoặc cấu hình trong data directory
cat > /var/lib/postgresql/data/postgresql.auto.conf << 'EOF'
restore_command = 'cp /archive/wal/%f %p'
recovery_target_time = '2026-06-20 15:30:00 UTC'
recovery_target_action = 'promote'
EOF

# PostgreSQL < 12: Tạo recovery.conf
cat > /var/lib/postgresql/data/recovery.conf << 'EOF'
restore_command = 'cp /archive/wal/%f %p'
recovery_target_time = '2026-06-20 15:30:00 UTC'
recovery_target_action = 'promote'
EOF

# Step 6: Start PostgreSQL
sudo systemctl start postgresql

# Step 7: Verify recovery
psql -h localhost -U postgres -c "SELECT pg_is_in_recovery();"
# Output: pg_is_in_recovery 
# ---------------------
# f
# (1 row)
```

### PITR Recovery Options

```bash
# Recovery đến specific timestamp
recovery_target_time = '2026-06-20 15:30:00 UTC'
recovery_target_inclusive = on  # Inclusive of target time

# Recovery đến specific WAL LSN
recovery_target_lsn = '0/2000000'

# Recovery đến specific transaction ID
recovery_target_xid = '12345'

# Recovery đến named restore point
recovery_target_name = 'before_major_update'
# Tạo restore point:
# SELECT pg_create_restore_point('before_major_update');

# Recovery đến latest
recovery_target = 'latest'

# Recovery đến immediate (stop as soon as consistency reached)
recovery_target = 'immediate'

# Recovery action
recovery_target_action = 'pause'  # Pause for inspection
recovery_target_action = 'promote'  # Promote immediately
recovery_target_action = 'shutdown'  # Shutdown after recovery
```

### Pause Recovery for Inspection

```conf
# postgresql.conf
recovery_target_action = 'pause'
```

```sql
-- Kiểm tra recovery status
SELECT pg_is_wal_replay_paused();
-- Output: t (true) = paused

-- Pause replay
SELECT pg_wal_replay_pause();

-- Resume replay
SELECT pg_wal_replay_resume();

-- Check replay progress
SELECT 
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS replay_lag
FROM pg_stat_replication;
```

## pgBackRest

pgBackRest là enterprise backup tool với nhiều features:

- Incremental backup
- Parallel backup/restore
- Differential backup
- Retention policies
- Encryption
- S3/Azure/GCS support

### Installation và Setup

```bash
# Install pgBackRest
apt-get install pgbackrest

# Hoặc từ source
git clone https://github.com/pgbackrest/pgbackrest.git
cd pgbackrest
./configure --with-openssl --withlz4 --withzstd
make -j$(nproc)
sudo make install
```

```ini
# /etc/pgbackrest/pgbackrest.conf

[global]
repo1-type=s3
repo1-s3-bucket=my-pgbackrest-bucket
repo1-s3-region=us-east-1
repo1-s3-key=AKIAIOSFODNN7EXAMPLE
repo1-s3-key-secret=${AWS_SECRET_ACCESS_KEY}
repo1-path=/postgresql/cluster1
repo1-retention-full=2
repo1-retention-diff=7
repo1-retention-archive=14
process-max=4
log-level-console=info
log-level-file=debug
start-fast=y
stop-auto=y
archive-async=y
spool-path=/var/spool/pgbackrest

[db]
db-path=/var/lib/postgresql/16/main
db-port=5432
db-socket-path=/var/run/postgresql
db-user=postgres

# Với compression
[global]
repo1-cipher-pass=${REPO_CIPHER_PASS}
repo1-cipher-type=aes-256-cbc

# Local repository
[db]
db1-host=localhost
db1-path=/var/lib/postgresql/16/main
```

### pgBackRest Commands

```bash
# Backup
pgbackrest backup --stanza=db --type=full
pgbackrest backup --stanza=db --type=incr
pgbackrest backup --stanza=db --type=diff

# Restore
pgbackrest restore --stanza=db --db-path=/var/lib/postgresql/restore
pgbackrest restore --stanza=db --type=time --target="2026-06-20 15:30:00"

# Archive
pgbackrest archive-get /archive/wal/%f %p
pgbackrest archive-push /wal/%p

# Info
pgbackrest info --stanza=db

# Check configuration
pgbackrest check --stanza=db

# Expire old backups
pgbackrest expire --stanza=db
```

### Configure PostgreSQL với pgBackRest

```conf
# postgresql.conf

# Archive
wal_level = replica
max_wal_senders = 3
wal_keep_size = 1GB

archive_mode = always
archive_command = 'pgbackrest archive-push %p'
archive_timeout = 300

# Recovery (for PITR)
restore_command = 'pgbackrest archive-get %f %p'
recovery_target_action = 'promote'
```

```ini
# /etc/pgbackrest/pgbackrest.conf
# Stanza configuration

[db]
db1-path=/var/lib/postgresql/16/main
db1-port=5432
db1-socket-path=/var/run/postgresql
```

```bash
# Create stanza
pgbackrest stanza-create --stanza=db --log-level-console=info

# Verify
pgbackrest check --stanza=db
```

### pgBackRest Scheduled Backups

```bash
# Cron job
cat > /etc/cron.d/pgbackrest << 'EOF'
# PostgreSQL Backup
0 2 * * 0 postgres pgbackrest --stanza=db backup --type=full --log-level-console=info
0 2 * * 1-6 postgres pgbackrest --stanza=db backup --type=diff --log-level-console=info
0 * * * * postgres pgbackrest --stanza=db expire --log-level-console=info
EOF

# Hoặc systemd timer
cat > /etc/systemd/system/pgbackrest-backup.timer << 'EOF'
[Unit]
Description=pgBackRest Backup Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
EOF
```

## Barman

Barman (Backup and Recovery Manager) là tool quản lý backup cho PostgreSQL:

```bash
# Install Barman
apt-get install barman barman-cli

# Or from source
pip install barman
```

```ini
# /etc/barman.conf hoặc ~/.barman.conf

[barman]
barman_home = /var/lib/barman
barman_user = barman
log_file = /var/log/barman/barman.log
compression = gzip
bandwidth_limit = 100MB/s
network_compression = yes

[my_server]
description = "Production PostgreSQL Server"
ssh_command = ssh postgres@db-server
conninfo = host=db-server user=postgres dbname=postgres
backup_directory = /var/lib/barman/my_server
retention_policy = REDUNDANCY 2
retention_policy_mode = auto
wal_retention_policy = MAIN

[db_server]
description = "DB Server"
ssh_command = ssh postgres@db-server
conninfo = host=db-server user=postgres port=5433
backup_directory = /var/lib/barman/db_server
```

```bash
# Init Barman
barman switch-wal --archive --server my_server

# List servers
barman list-servers

# Check server
barman check my_server

# Backup
barman backup my_server

# List backups
barman list-backups my_server

# Restore
barman recover my_server latest /var/lib/postgresql/restore

# Point-in-time recovery
barman recover my_server 20260620T020000 /var/lib/postgresql/restore \
    --target-time "2026-06-20 15:30:00"

# Status
barman status my_server

# Cron jobs
# 0 * * * * barman cron
# 0 2 * * * barman backup my_server
```

## Backup Verification

### Verify pg_dump Backup

```bash
# Check backup file
file backup.sql.gz
gunzip -t backup.sql.gz

# Verify content
gunzip -c backup.sql.gz | head -100

# Restore to test database
psql -h localhost -U postgres -c "CREATE DATABASE test_restore;"
psql -h localhost -U postgres -d test_restore -f backup.sql

# Check data
psql -h localhost -U postgres -d test_restore -c "SELECT COUNT(*) FROM users;"
psql -h localhost -U postgres -d test_restore -c "SELECT * FROM pg_tables;"
```

### Verify Physical Backup

```bash
# List backup contents
tar -tzf base.tar.gz | head -20

# Verify backup integrity
pg_basebackup --verify-backup -D /tmp/verify_backup

# Check WAL segments
ls /archive/wal/ | wc -l
```

### Automated Verification

```bash
#!/bin/bash
# verify_backup.sh

set -e

BACKUP_FILE=${1:-/backup/latest.dump}
TEST_DB="backup_test_$(date +%s)"

echo "Starting backup verification..."

# Create test database
psql -h localhost -U postgres -c "DROP DATABASE IF EXISTS $TEST_DB;"
psql -h localhost -U postgres -c "CREATE DATABASE $TEST_DB;"

# Restore backup
echo "Restoring backup to $TEST_DB..."
pg_restore -h localhost -U postgres -d $TEST_DB --no-owner --no-acl -v $BACKUP_FILE

# Verify tables
echo "Verifying tables..."
TABLE_COUNT=$(psql -h localhost -U postgres -d $TEST_DB -t -c "SELECT COUNT(*) FROM pg_tables WHERE schemaname = 'public';")
echo "Tables restored: $TABLE_COUNT"

# Verify row counts
echo "Verifying data..."
psql -h localhost -U postgres -d $TEST_DB -c "SELECT COUNT(*) FROM users;"
psql -h localhost -U postgres -d $TEST_DB -c "SELECT COUNT(*) FROM orders;"

# Cleanup
psql -h localhost -U postgres -c "DROP DATABASE $TEST_DB;"

echo "Backup verification completed successfully!"
```

## Common Patterns

### Pattern 1: Automated Backup Script

```bash
#!/bin/bash
# backup.sh - Production backup script

set -euo pipefail

# Configuration
BACKUP_DIR="/backup/postgresql"
RETENTION_DAYS=30
PGHOST="localhost"
PGPORT="5432"
PGUSER="postgres"
PGDATABASE="mydb"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${PGDATABASE}_${DATE}.dump.gz"

# S3 settings (optional)
S3_BUCKET="my-backups"
S3_PATH="postgresql/${PGDATABASE}"

# Create backup directory
mkdir -p ${BACKUP_DIR}

# Perform backup
echo "Starting backup of ${PGDATABASE}..."
pg_dump -h ${PGHOST} -p ${PGPORT} -U ${PGUSER} -d ${PGDATABASE} \
    -Fc -Z 9 -j 4 -f /tmp/backup_temp.dump

# Move to final location
mv /tmp/backup_temp.dump ${BACKUP_FILE}

# Upload to S3 if configured
if [ -n "${S3_BUCKET:-}" ]; then
    echo "Uploading to S3..."
    aws s3 cp ${BACKUP_FILE} s3://${S3_BUCKET}/${S3_PATH}/${PGDATABASE}_${DATE}.dump.gz
fi

# Cleanup old backups
echo "Cleaning up backups older than ${RETENTION_DAYS} days..."
find ${BACKUP_DIR} -name "${PGDATABASE}_*.dump.gz" -mtime +${RETENTION_DAYS} -delete

# Verify backup
echo "Verifying backup..."
pg_restore --list ${BACKUP_FILE} | head -20

# Log completion
echo "[$(date)] Backup completed: ${BACKUP_FILE}" >> /var/log/backup.log

# Send notification on failure
trap 'echo "[$(date)] Backup FAILED!" | tee -a /var/log/backup.log; exit 1' ERR
```

### Pattern 2: Replication-based Backup

```bash
#!/bin/bash
# backup_from_replica.sh - Backup từ replica để giảm load trên primary

set -euo pipefail

REPLICA_HOST="replica-server"
BACKUP_DIR="/backup/postgresql"
DATE=$(date +%Y%m%d_%H%M%S)

echo "Starting backup from replica ${REPLICA_HOST}..."

# Stop replication temporarily (optional - nếu cần consistent backup)
# psql -h ${REPLICA_HOST} -U postgres -c "SELECT pg_backup_start('backup');"

# Perform base backup
pg_basebackup -h ${REPLICA_HOST} -U postgres -D ${BACKUP_DIR}/base_${DATE} -Ft -z -P -Xs

# Resume replication
# psql -h ${REPLICA_HOST} -U postgres -c "SELECT pg_backup_stop();"

echo "Backup completed: ${BACKUP_DIR}/base_${DATE}"
```

### Pattern 3: PITR Recovery Script

```bash
#!/bin/bash
# pitr_recovery.sh

TARGET_TIME="${1:-}"
BACKUP_DIR="/backup/postgresql"
PG_DATA="/var/lib/postgresql/16/main"

if [ -z "$TARGET_TIME" ]; then
    echo "Usage: $0 <target_time>"
    echo "Example: $0 '2026-06-20 15:30:00 UTC'"
    exit 1
fi

echo "Starting PITR recovery to ${TARGET_TIME}..."

# Stop PostgreSQL
systemctl stop postgresql

# Backup current state
cp -a ${PG_DATA} ${PG_DATA}.pre-recovery-$(date +%Y%m%d%H%M%S)

# Clear data directory
rm -rf ${PG_DATA}/*

# Restore base backup
pg_basebackup -h localhost -U postgres -D ${PG_DATA} -X stream -R

# Configure recovery
cat > ${PG_DATA}/postgresql.auto.conf << EOF
restore_command = 'cp /archive/wal/%f %p'
recovery_target_time = '${TARGET_TIME}'
recovery_target_action = 'promote'
EOF

# Start PostgreSQL
systemctl start postgresql

# Wait for recovery to complete
sleep 5

# Verify
psql -U postgres -c "SELECT pg_is_in_recovery();"
```

## Troubleshooting

### Vấn đề 1: WAL Archive Fails

**Triệu chứng**: WAL segments không được archive, disk đầy.

**Giải pháp**:

```bash
# 1. Check PostgreSQL log
tail -f /var/log/postgresql/postgresql-16-main.log

# 2. Check archive status
psql -U postgres -c "SELECT * FROM pg_stat_archiver;"

# 3. Test archive command manually
# cp /var/lib/postgresql/16/main/pg_wal/000000010000000000000001 /archive/wal/

# 4. Check disk space
df -h /archive/wal

# 5. Fix permissions
chown postgres:postgres /archive/wal
chmod 755 /archive/wal
```

### Vấn đề 2: Backup Restore Fails

**Triệu chứng**: pg_restore fails với errors.

**Giải pháp**:

```bash
# 1. Check backup file integrity
file backup.dump
pg_restore --help | head

# 2. Restore to new database (avoid overwriting)
pg_restore -h localhost -U postgres -C -d postgres backup.dump

# 3. Check for version mismatch
pg_restore --version
psql --version

# 4. Restore with clean
pg_restore -h localhost -U postgres --clean --if-exists -C -d postgres backup.dump

# 5. Skip errors và continue
pg_restore -h localhost -U postgres --continue-on-error -d mydb backup.dump
```

### Vấn đề 3: PITR Fails

**Triệu chứng**: Recovery không hoàn thành.

**Giải pháp**:

```bash
# 1. Check recovery.conf/postgresql.auto.conf
cat /var/lib/postgresql/16/main/postgresql.auto.conf

# 2. Check WAL archive
ls -la /archive/wal/ | tail -20

# 3. Verify base backup
pg_basebackup --verify-backup -D /tmp/verify

# 4. Check PostgreSQL log for errors
tail -100 /var/lib/postgresql/16/main/log/*.csv

# 5. Manual recovery
# rm -f /var/lib/postgresql/16/main/recovery.conf
# touch /var/lib/postgresql/16/main/recovery.signal
# systemctl restart postgresql
```

### Vấn đề 4: Replication Slot Issues

**Giải pháp**:

```sql
-- Check replication slots
SELECT * FROM pg_replication_slots;

-- Drop inactive slot
SELECT pg_drop_replication_slot('inactive_slot');

-- Monitor slot lag
SELECT 
    slot_name,
    pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag_bytes
FROM pg_replication_slots
WHERE active = false;
```

## Ví dụ minh họa

### Ví dụ 1: Complete Backup Strategy

```bash
#!/bin/bash
# complete_backup.sh

set -euo pipefail

# Configuration
RETENTION_FULL=4
RETENTION_DIFF=7
RETENTION_ARCH=14
BACKUP_HOST="localhost"
BACKUP_USER="postgres"

# pgBackRest configuration
cat > /etc/pgbackrest/pgbackrest.conf << 'EOF'
[global]
repo1-type=s3
repo1-s3-bucket=company-pgbackrest
repo1-s3-region=us-east-1
repo1-path=/prod/cluster1
repo1-retention-full=${RETENTION_FULL}
repo1-retention-diff=${RETENTION_DIFF}
repo1-retention-archive=${RETENTION_ARCH}
process-max=4
log-level-console=info
log-level-file=debug
start-fast=y
archive-async=y

[prod]
db1-host=${BACKUP_HOST}
db1-path=/var/lib/postgresql/16/main
db1-port=5432
db1-user=${BACKUP_USER}
EOF

# Create stanza
pgbackrest stanza-create --stanza=prod --log-level-console=info

# Initial full backup
pgbackrest backup --stanza=prod --type=full --log-level-console=info

# Verify
pgbackrest info --stanza=prod
```

### Ví dụ 2: Point-in-Time Recovery to S3

```bash
#!/bin/bash
# pitr_to_s3.sh

STANZA="prod"
TARGET_TIME="2026-06-20 15:30:00 UTC"
RECOVERY_DIR="/var/lib/postgresql/16/main-recovery"
S3_BUCKET="company-pgbackrest"
S3_PREFIX="prod/cluster1"

# Create recovery directory
mkdir -p ${RECOVERY_DIR}

# Restore latest full backup
echo "Restoring latest full backup..."
pgbackrest restore --stanza=${STANZA} \
    --type=time \
    --target="${TARGET_TIME}" \
    --db-path=${RECOVERY_DIR} \
    --log-level-console=info

# Verify recovery
echo "Recovery completed!"
echo "Data is in: ${RECOVERY_DIR}"

# Optional: Start as temporary instance
# chown -R postgres:postgres ${RECOVERY_DIR}
# chmod 700 ${RECOVERY_DIR}
```

### Ví dụ 3: Backup Monitoring

```sql
-- Create backup monitoring view
CREATE OR REPLACE FUNCTION get_backup_status()
RETURNS TABLE (
    backup_type TEXT,
    start_time TIMESTAMPTZ,
    end_time TIMEMPTZ,
    duration INTERVAL,
    size_bytes BIGINT,
    verification_status TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'pg_stat_archiver'::TEXT AS backup_type,
        NULL::TIMESTAMPTZ AS start_time,
        NULL::TIMESTAMPTZ AS end_time,
        NULL::INTERVAL AS duration,
        NULL::BIGINT AS size_bytes,
        CASE 
            WHEN last_archive_age < '1 hour'::interval THEN 'OK'
            WHEN last_archive_age < '1 day'::interval THEN 'WARNING'
            ELSE 'CRITICAL'
        END AS verification_status
    FROM (
        SELECT 
            now() - last_archive_time AS last_archive_age
        FROM pg_stat_archiver
    ) sub;
END;
$$ LANGUAGE plpgsql;

-- Check archive status
SELECT 
    archived_count,
    last_archived_wal,
    last_archived_time,
    now() - last_archived_time AS archive_age,
    failed_count
FROM pg_stat_archiver;
```

## References

### Official Documentation
- [PostgreSQL Backup và Recovery](https://www.postgresql.org/docs/current/backup.html)
- [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html)
- [pg_basebackup](https://www.postgresql.org/docs/current/app-pgbasebackup.html)
- [Continuous Archiving](https://www.postgresql.org/docs/current/continuous-archiving.html)
- [pgBackRest](https://pgbackrest.org/)
- [Barman](https://www.pgbarman.org/)

### Best Practices
- 3-2-1 backup rule: 3 copies, 2 different media, 1 offsite
- Test backups regularly (at least monthly)
- Document recovery procedures
- Automate backup verification
- Monitor backup success/failure
- Implement retention policies

### Tools
- [pgBackRest](https://pgbackrest.org/) - Enterprise backup tool
- [Barman](https://www.pgbarman.org/) - Backup manager
- [pg_probackup](https://github.com/postgrespro/pg_probackup) - Incremental backup
- [Wal-g](https://github.com/wal-g/wal-g) - Backup tool với compression
