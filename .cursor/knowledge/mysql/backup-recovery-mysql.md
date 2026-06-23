---
title: Backup và Recovery MySQL
description: Hướng dẫn Backup và Recovery - mysqldump, MySQL Enterprise Backup, XtraBackup, Point-in-time Recovery, Binary Log Recovery, Incremental Backups
tags: [mysql, backup, recovery, mysqldump, xtrabackup, point-in-time]
created: 2026-06-23
version: 1.0.0
framework: cursor-enterprise-framework
---

# Backup và Recovery MySQL

## Tổng quan

Backup và recovery là một trong những khía cạnh quan trọng nhất của database administration. Trong môi trường enterprise, việc có chiến lược backup hiệu quả không chỉ là best practice mà còn là yêu cầu kinh doanh bắt buộc. Mất dữ liệu có thể gây ra thiệt hại tài chính nghiêm trọng, ảnh hưởng đến uy tín với khách hàng, và trong một số trường hợp nghiêm trọng, có thể dẫn đến các vấn đề pháp lý.

MySQL cung cấp nhiều phương pháp backup khác nhau, từ logical backups với mysqldump đến physical backups với XtraBackup và MySQL Enterprise Backup. Mỗi phương pháp có ưu nhược điểm riêng và phù hợp với các scenarios khác nhau. Tài liệu này cung cấp hướng dẫn chi tiết về cách implement một chiến lược backup toàn diện.

## Mục đích của tài liệu

Tài liệu này được viết nhằm giúp các database administrators:

- Hiểu các loại backup methods và khi nào nên sử dụng
- Implement backup strategies phù hợp với business requirements
- Thực hiện point-in-time recovery một cách chính xác
- Test và verify backup integrity định kỳ
- Optimize backup performance và storage
- Xây dựng disaster recovery plan

## Các loại Backup

### Logical vs Physical Backups

| Aspect | Logical Backups | Physical Backups |
|--------|----------------|-----------------|
| Method | SQL statements export | Raw file copies |
| Tools | mysqldump, SELECT INTO OUTFILE | XtraBackup, MySQL Enterprise Backup |
| Speed | Chậm cho large databases | Nhanh |
| Size | Thường lớn hơn | Nhỏ hơn (compressed) |
| Restore | Rebuild indexes | Direct file replacement |
| Partial backup | Dễ dàng | Phức tạp hơn |
| Cross-version | Supported | Version specific |

### Full vs Incremental vs Differential Backups

**Full Backup**: Sao lưu toàn bộ database tại một thời điểm.

**Incremental Backup**: Sao lưu chỉ những thay đổi kể từ backup trước đó (full hoặc incremental).

**Differential Backup**: Sao lưu những thay đổi kể từ lần full backup gần nhất.

## mysqldump

mysqldump là tool phổ biến nhất cho logical backups trong MySQL. Nó xuất dữ liệu dưới dạng SQL statements có thể được import lại vào MySQL server.

### Cú pháp cơ bản

```bash
# Basic full database backup
mysqldump -u root -p --all-databases > backup_all.sql

# Single database backup
mysqldump -u root -p database_name > backup_db.sql

# Single table backup
mysqldump -u root -p database_name table_name > backup_table.sql

# Multiple databases
mysqldump -u root -p --databases db1 db2 db3 > backup_dbs.sql
```

### Advanced Options

```bash
# Backup với compression
mysqldump -u root -p database_name | gzip > backup.sql.gz

# Backup với extended inserts (smaller file, faster restore)
mysqldump -u root -p --extended-insert database_name > backup.sql

# Backup với transactions (consistent backup cho InnoDB)
mysqldump -u root -p --single-transaction --routines --triggers --events database_name > backup.sql

# Backup với stored routines, triggers, events
mysqldump -u root -p \
    --routines \
    --triggers \
    --events \
    --all-databases > full_backup.sql

# Backup với master data for replication
mysqldump -u root -p \
    --master-data=2 \
    --dump-slave \
    --include-master-host-port \
    database_name > backup.sql
```

```bash
# Point-in-time recovery support
mysqldump -u root -p \
    --single-transaction \
    --master-data=2 \
    --flush-logs \
    database_name > backup.sql

# Output includes:
-- CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000001', MASTER_LOG_POS=12345;
```

### Script Backup tự động

```bash
#!/bin/bash
# backup_mysqldump.sh

set -e

# Configuration
MYSQL_USER="backup_user"
MYSQL_PASSWORD="StrongP@ssw0rd!"
BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p ${BACKUP_DIR}/daily/${DATE}
mkdir -p ${BACKUP_DIR}/weekly
mkdir -p ${BACKUP_DIR}/logs

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a ${BACKUP_DIR}/logs/backup.log
}

# Full backup function
backup_database() {
    local db_name=$1
    local backup_file="${BACKUP_DIR}/daily/${DATE}/${db_name}.sql"
    
    log "Starting backup for database: ${db_name}"
    
    mysqldump -u ${MYSQL_USER} -p${MYSQL_PASSWORD} \
        --single-transaction \
        --routines \
        --triggers \
        --events \
        --master-data=2 \
        --flush-logs \
        --lock-tables=false \
        ${db_name} | gzip > ${backup_file}.gz
    
    # Verify backup
    if [ -s "${backup_file}.gz" ]; then
        local size=$(du -h ${backup_file}.gz | cut -f1)
        log "Backup completed: ${db_name} (${size})"
        echo "${backup_file}.gz"
    else
        log "ERROR: Backup failed for ${db_name}"
        return 1
    fi
}

# Get list of databases
databases=$(mysql -u ${MYSQL_USER} -p${MYSQL_PASSWORD} -N -e \
    "SHOW DATABASES LIKE '%' WHERE \`Database\` NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys')")

# Backup each database
for db in $databases; do
    backup_database "$db" || log "Failed to backup: $db"
done

# Rotate old backups
log "Cleaning up backups older than ${RETENTION_DAYS} days"
find ${BACKUP_DIR}/daily -type f -mtime +${RETENTION_DAYS} -delete
find ${BACKUP_DIR}/logs -type f -mtime +${RETENTION_DAYS} -delete

log "Backup process completed"
```

## MySQL Enterprise Backup

MySQL Enterprise Backup là proprietary tool từ Oracle, cung cấp high-performance physical backups với các tính năng enterprise.

### Cài đặt

```bash
# Linux (RPM)
yum install mysql-enterprise-backup

# Linux (DEB)
dpkg -i mysql-enterprise-backup_8.0.x_linux_x86_64.deb

# Verify installation
mysqlbackup --version
```

### Full Backup

```bash
# Basic full backup
mysqlbackup -u root -p \
    --backup-dir=/backup/mysql/full \
    --backup-image=backup_full.mbi \
    backup-to-image

# Backup với compression
mysqlbackup -u root -p \
    --backup-dir=/backup/mysql/full \
    --backup-image=backup_full_compressed.mbi.zst \
    --compress \
    backup-to-image
```

### Incremental Backup

```bash
# First, create full backup (if not exists)
mysqlbackup -u root -p \
    --backup-dir=/backup/mysql/full \
    --incremental \
    --incremental-base=dir:/backup/mysql/full \
    backup

# Subsequent incremental backups
mysqlbackup -u root -p \
    --backup-dir=/backup/mysql/incr_1 \
    --incremental \
    --incremental-base=dir:/backup/mysql/full \
    backup

# Create image from incremental
mysqlbackup -u root -p \
    --backup-dir=/backup/mysql/incr_1 \
    --backup-image=backup_incr.mbi \
    backup-to-image
```

### Partial Backup

```bash
# Backup specific tablespaces
mysqlbackup -u root -p \
    --backup-dir=/backup/mysql/partial \
    --include-tablespace='mydb\.orders' \
    --include-tablespace='mydb\.order_items' \
    backup

# Backup specific databases
mysqlbackup -u root -p \
    --backup-dir=/backup/mysql/partial \
    --databases="ecommerce analytics" \
    backup
```

### Restore

```bash
# Full restore
mysqlbackup -u root -p \
    --backup-dir=/backup/mysql/full \
    --innodb-log-files-dir=/var/lib/mysql \
    copy-back

# Restore from image
mysqlbackup -u root -p \
    --backup-image=/backup/mysql/full/backup_full.mbi \
    --target-dir=/var/lib/mysql \
    copy-back-and-apply-log

# Point-in-time restore
mysqlbackup -u root -p \
    --backup-dir=/backup/mysql/full \
    --incremental-backup-dir=/backup/mysql/incr_1 \
    --target-dir=/var/lib/mysql \
    copy-back-and-apply-log
```

## XtraBackup (Percona)

XtraBackup là open-source tool cho high-performance MySQL backups, được sử dụng rộng rãi trong production environments.

### Cài đặt

```bash
# Install Percona repository
yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
yum install percona-xtrabackup-80

# Verify
xtrabackup --version
```

### Full Backup

```bash
# Basic full backup
xtrabackup --backup \
    --target-dir=/backup/xtrabackup/full_$(date +%Y%m%d) \
    --user=root \
    --password=StrongP@ssw0rd!

# Backup với compression
xtrabackup --backup \
    --compress \
    --compress-threads=4 \
    --target-dir=/backup/xtrabackup/full_compressed_$(date +%Y%m%d) \
    --user=root \
    --password=StrongP@ssw0rd!

# Backup với encryption
xtrabackup --backup \
    --encrypt=AES256 \
    --encrypt-key-file=/etc/xtrabackup/keyfile \
    --target-dir=/backup/xtrabackup/full_encrypted_$(date +%Y%m%d) \
    --user=root \
    --password=StrongP@ssw0rd!
```

### Incremental Backup

```bash
# Create incremental backup
xtrabackup --backup \
    --target-dir=/backup/xtrabackup/incr_1_$(date +%Y%m%d) \
    --incremental-basedir=/backup/xtrabackup/full_20260622 \
    --user=root \
    --password=StrongP@ssw0rd!

# Multiple incremental backups
xtrabackup --backup \
    --target-dir=/backup/xtrabackup/incr_2_$(date +%Y%m%d) \
    --incremental-basedir=/backup/xtrabackup/incr_1_20260622 \
    --user=root \
    --password=StrongP@ssw0rd!
```

### Prepare và Restore

```bash
# Prepare full backup (apply logs)
xtrabackup --prepare \
    --target-dir=/backup/xtrabackup/full_20260622

# Prepare incremental backup
# Apply to full backup
xtrabackup --prepare \
    --target-dir=/backup/xtrabackup/full_20260622 \
    --incremental-dir=/backup/xtrabackup/incr_1_20260622

# Final prepare
xtrabackup --prepare \
    --target-dir=/backup/xtrabackup/full_20260622

# Restore
xtrabackup --copy-back \
    --target-dir=/backup/xtrabackup/full_20260622 \
    --datadir=/var/lib/mysql

# Set permissions
chown -R mysql:mysql /var/lib/mysql
```

### Streaming và Remote Backups

```bash
# Stream backup to remote server
xtrabackup --backup \
    --stream=xbstream \
    --target-dir=/backup/xtrabackup/stream \
    --user=root \
    --password=StrongP@ssw0rd! | \
    ssh backup-server "xbstream -x -C /remote/backup/"

# Compressed streaming backup
xtrabackup --backup \
    --compress \
    --stream=tar \
    --target-dir=/backup/xtrabackup/stream \
    --user=root \
    --password=StrongP@ssw0rd! | \
    ssh backup-server "tar -xfi - -C /remote/backup/"
```

### Tối ưu Performance

```bash
# Parallel backup
xtrabackup --backup \
    --parallel=8 \
    --target-dir=/backup/xtrabackup/full_$(date +%Y%m%d) \
    --user=root \
    --password=StrongP@ssw0rd!

# Optimize I/O
xtrabackup --backup \
    --use-memory=4G \
    --throttle=100 \
    --target-dir=/backup/xtrabackup/full_$(date +%Y%m%d) \
    --user=root \
    --password=StrongP@ssw0rd!

# Combined options for production
xtrabackup --backup \
    --parallel=8 \
    --compress \
    --compress-threads=4 \
    --use-memory=4G \
    --rsync \
    --target-dir=/backup/xtrabackup/full_$(date +%Y%m%d) \
    --user=root \
    --password=StrongP@ssw0rd!
```

## Binary Log Recovery

Binary logs chứa tất cả các thay đổi dữ liệu và có thể được sử dụng để thực hiện point-in-time recovery.

### Cấu hình Binary Log

```ini
# my.cnf
[mysqld]
server-id = 1
log_bin = /var/log/mysql/mysql-bin
binlog_format = ROW
binlog_expire_logs_seconds = 604800  # 7 days
max_binlog_size = 1G
binlog_row_image = FULL
sync_binlog = 1
```

### Xem Binary Log Contents

```bash
# List binary log files
mysql -u root -p -e "SHOW BINARY LOGS;"

# Show current binary log position
mysql -u root -p -e "SHOW MASTER STATUS;"

# Show events in binary log
mysqlbinlog /var/log/mysql/mysql-bin.000001

# Show events between two positions
mysqlbinlog \
    --start-position=123 \
    --stop-position=456 \
    /var/log/mysql/mysql-bin.000001

# Show events in time range
mysqlbinlog \
    --start-datetime="2026-06-23 10:00:00" \
    --stop-datetime="2026-06-23 11:00:00" \
    /var/log/mysql/mysql-bin.000001
```

### Point-in-time Recovery

```bash
# Step 1: Restore from last full backup
mysql -u root -p database_name < /backup/full_backup.sql

# Step 2: Apply binary logs to reach point in time
mysqlbinlog \
    --database=database_name \
    /var/log/mysql/mysql-bin.000001 \
    /var/log/mysql/mysql-bin.000002 \
    /var/log/mysql/mysql-bin.000003 \
    mysql -u root -p database_name

# Step 3: Apply until specific position
mysqlbinlog \
    --stop-position=12345 \
    /var/log/mysql/mysql-bin.000003 \
    mysql -u root -p database_name

# Step 4: Or apply until specific time
mysqlbinlog \
    --stop-datetime="2026-06-23 10:30:00" \
    /var/log/mysql/mysql-bin.000003 \
    mysql -u root -p database_name
```

### Restore to Specific GTID

```bash
# Get GTID from backup
# Full backup includes: SET @@GLOBAL.gtid_purged = 'uuid:1-123';

# Restore full backup
mysql -u root -p < full_backup.sql

# Apply binlogs to specific GTID
mysqlbinlog \
    --gtid --include-gtids='uuid:124-200' \
    /var/log/mysql/mysql-bin.000001 | mysql -u root -p

# Or exclude specific GTIDs
mysqlbinlog \
    --gtid --exclude-gtids='uuid:150-160' \
    /var/log/mysql/mysql-bin.000001 | mysql -u root -p
```

## Incremental Backups

### Chiến lược Incremental Backup với XtraBackup

```bash
#!/bin/bash
# incremental_backup.sh

set -e

BACKUP_DIR="/backup/xtrabackup"
DATE=$(date +%Y%m%d_%H%M%S)
USER="root"
PASSWORD="StrongP@ssw0rd!"

# Paths
LATEST_FULL="${BACKUP_DIR}/latest_full"
INCR_DIR="${BACKUP_DIR}/incremental"

# Create incremental backup
xtrabackup --backup \
    --target-dir="${INCR_DIR}/${DATE}" \
    --incremental-basedir="${LATEST_FULL}" \
    --user="${USER}" \
    --password="${PASSWORD}" \
    --parallel=4

# Create symlink to latest incremental
ln -sfn "${INCR_DIR}/${DATE}" "${BACKUP_DIR}/latest_incremental"

# Clean old incremental backups (keep 7 days)
find ${INCR_DIR} -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \;

echo "Incremental backup completed: ${DATE}"
```

### Chiến lược Differential Backup

```bash
#!/bin/bash
# differential_backup.sh

set -e

BACKUP_DIR="/backup/xtrabackup"
DATE=$(date +%Y%m%d_%H%M%S)
USER="root"
PASSWORD="StrongP@ssw0rd!"

# Differential always based on latest full
LATEST_FULL="${BACKUP_DIR}/full_$(date +%Y%m%d --date='last sunday')"

xtrabackup --backup \
    --target-dir="${BACKUP_DIR}/diff_${DATE}" \
    --incremental-basedir="${LATEST_FULL}" \
    --user="${USER}" \
    --password="${PASSWORD}"

echo "Differential backup completed: ${DATE}"
```

## Point-in-time Recovery Procedures

### Chuẩn bị cho PITR

```sql
-- Step 1: Xác định thời điểm cần restore
-- Ví dụ: User accidentally deleted records at 14:30

-- Step 2: Lấy binlog position trước khi incident
-- mysqlbinlog --stop-datetime="2026-06-23 14:25:00" binlog.000001

-- Step 3: Thực hiện restore sequence
```

```bash
#!/bin/bash
# point_in_time_recovery.sh

set -e

DATABASE="ecommerce"
BACKUP_DATE="2026-06-23"
INCIDENT_TIME="2026-06-23 14:30:00"
BACKUP_DIR="/backup"
MYSQL_USER="root"
MYSQL_PASSWORD="StrongP@ssw0rd!"

echo "Starting Point-in-Time Recovery"
echo "Target database: ${DATABASE}"
echo "Incident time: ${INCIDENT_TIME}"
echo ""

# Step 1: Stop MySQL
echo "Stopping MySQL..."
systemctl stop mysql

# Step 2: Backup current data (in case we need to revert)
echo "Backing up current data..."
cp -a /var/lib/mysql/${DATABASE} /var/lib/mysql/${DATABASE}.corrupted.$(date +%s)

# Step 3: Clear data directory for this database
rm -rf /var/lib/mysql/${DATABASE}/*

# Step 4: Restore from latest full backup
echo "Restoring from full backup..."
xtrabackup --decompress \
    --target-dir="${BACKUP_DIR}/full" \
    --parallel=4

xtrabackup --prepare \
    --target-dir="${BACKUP_DIR}/full"

xtrabackup --copy-back \
    --target-dir="${BACKUP_DIR}/full" \
    --datadir=/var/lib/mysql

# Step 5: Apply incremental backups up to incident time
for incr in ${BACKUP_DIR}/incremental/*; do
    incr_time=$(stat -c %Y "$incr")
    incident_ts=$(date -d "${INCIDENT_TIME}" +%s)
    
    if [ "$incr_time" -lt "$incident_ts" ]; then
        echo "Applying incremental: $(basename $incr)"
        xtrabackup --prepare \
            --target-dir="${BACKUP_DIR}/full" \
            --incremental-dir="$incr"
    fi
done

# Step 6: Final prepare
xtrabackup --prepare --target-dir="${BACKUP_DIR}/full"

# Step 7: Copy back
xtrabackup --copy-back --target-dir="${BACKUP_DIR}/full" --datadir=/var/lib/mysql

# Step 8: Start MySQL
systemctl start mysql

# Step 9: Apply binlogs after last backup
LAST_BINLOG=$(mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} -N -e "SHOW MASTER STATUS\G" | grep File | awk '{print $2}')
LAST_POS=$(mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} -N -e "SHOW MASTER STATUS\G" | grep Position | awk '{print $2}')

# Note: Adjust start position based on backup's binlog position
mysqlbinlog \
    --stop-datetime="${INCIDENT_TIME}" \
    /var/lib/mysql/${LAST_BINLOG} | \
    mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} ${DATABASE}

echo ""
echo "Point-in-Time Recovery completed"
```

## Các Best Practices

### 1. Backup Strategy Design

```sql
-- Backup rotation policy
-- 
-- Daily: Incremental backup (Mon-Sat)
-- Weekly: Full backup (Sunday)
-- Monthly: Full backup (1st of month)
-- Retention: 7 days incremental, 30 days daily, 90 days weekly
```

```bash
# backup_rotation.sh
#!/bin/bash

BACKUP_BASE="/backup/mysql"
KEEP_DAILY=7
KEEP_WEEKLY=4
KEEP_MONTHLY=12

# Determine backup type
DAY_OF_WEEK=$(date +%w)
DAY_OF_MONTH=$(date +%d)

if [ "$DAY_OF_MONTH" -eq 1 ]; then
    BACKUP_TYPE="monthly"
elif [ "$DAY_OF_WEEK" -eq 0 ]; then
    BACKUP_TYPE="weekly"
else
    BACKUP_TYPE="daily"
fi

echo "Backup type: ${BACKUP_TYPE}"

# Execute appropriate backup
case $BACKUP_TYPE in
    "monthly"|"weekly")
        xtrabackup --backup \
            --target-dir="${BACKUP_BASE}/${BACKUP_TYPE}_$(date +%Y%m%d)" \
            --user=root --password="${MYSQL_ROOT_PASSWORD}"
        ;;
    "daily")
        # Find latest full/weekly backup
        LATEST_FULL=$(ls -dt ${BACKUP_BASE}/weekly_* ${BACKUP_BASE}/monthly_* 2>/dev/null | head -1)
        xtrabackup --backup \
            --target-dir="${BACKUP_BASE}/daily_$(date +%Y%m%d)" \
            --incremental-basedir="${LATEST_FULL}" \
            --user=root --password="${MYSQL_ROOT_PASSWORD}"
        ;;
esac
```

### 2. Verify Backup Integrity

```bash
#!/bin/bash
# verify_backup.sh

BACKUP_FILE=$1

# Check file exists and has content
if [ ! -s "$BACKUP_FILE" ]; then
    echo "ERROR: Backup file is empty or doesn't exist"
    exit 1
fi

# For mysqldump backups
if [[ "$BACKUP_FILE" == *.sql ]]; then
    # Check SQL syntax
    head -100 "$BACKUP_FILE" | grep -q "MySQL dump"
    if [ $? -ne 0 ]; then
        echo "WARNING: File may not be a valid mysqldump"
    fi
    
    # Check for required structure
    grep -q "CREATE TABLE" "$BACKUP_FILE"
    if [ $? -ne 0 ]; then
        echo "WARNING: No CREATE TABLE statements found"
    fi
fi

# For XtraBackup
if [ -d "$BACKUP_FILE" ]; then
    # Check for xtrabackup info file
    if [ -f "${BACKUP_FILE}/xtrabackup_info" ]; then
        cat "${BACKUP_FILE}/xtrabackup_info"
    else
        echo "WARNING: Not a valid XtraBackup directory"
    fi
fi

# For compressed backups
if [[ "$BACKUP_FILE" == *.gz ]]; then
    gzip -t "$BACKUP_FILE" 2>&1
    if [ $? -ne 0 ]; then
        echo "ERROR: Compressed backup is corrupted"
        exit 1
    fi
fi

echo "Backup verification passed"
```

### 3. Offsite Backup

```bash
#!/bin/bash
# offsite_backup.sh

set -e

BACKUP_SOURCE="/backup/mysql"
REMOTE_HOST="backup-server.company.com"
REMOTE_USER="backup"
REMOTE_PATH="/backup/mysql"

# Rsync with compression and progress
rsync -avz --progress \
    -e "ssh -i /root/.ssh/backup_key" \
    "${BACKUP_SOURCE}/" \
    "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/"

# Verify remote backup
ssh -i /root/.ssh/backup_key ${REMOTE_USER}@${REMOTE_HOST} \
    "ls -la ${REMOTE_PATH}/"

echo "Offsite backup completed"
```

### 4. Backup Monitoring

```sql
-- Create backup tracking table
CREATE TABLE backup_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    backup_type ENUM('full', 'incremental', 'differential') NOT NULL,
    backup_method VARCHAR(50),
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    duration_seconds INT,
    backup_size_bytes BIGINT,
    backup_location VARCHAR(500),
    status ENUM('running', 'completed', 'failed') DEFAULT 'running',
    error_message TEXT,
    verified BOOLEAN DEFAULT FALSE,
    verified_at TIMESTAMP NULL,
    INDEX idx_backup_type (backup_type),
    INDEX idx_start_time (start_time),
    INDEX idx_status (status)
) ENGINE=InnoDB;

-- Stored procedure to log backup
DELIMITER //

CREATE PROCEDURE log_backup_start(
    IN p_backup_type VARCHAR(20),
    IN p_backup_method VARCHAR(50),
    IN p_location VARCHAR(500)
)
BEGIN
    INSERT INTO backup_history (backup_type, backup_method, start_time, backup_location, status)
    VALUES (p_backup_type, p_backup_method, NOW(), p_location, 'running');
    
    SELECT LAST_INSERT_ID() AS backup_id;
END //

CREATE PROCEDURE log_backup_complete(
    IN p_backup_id INT,
    IN p_status VARCHAR(20),
    IN p_size_bytes BIGINT,
    IN p_error TEXT
)
BEGIN
    UPDATE backup_history
    SET 
        end_time = NOW(),
        duration_seconds = TIMESTAMPDIFF(SECOND, start_time, NOW()),
        backup_size_bytes = p_size_bytes,
        status = p_status,
        error_message = p_error
    WHERE id = p_backup_id;
END //

DELIMITER ;
```

## Các Common Patterns

### Pattern 1: Zero-Downtime Backup

```bash
#!/bin/bash
# zero_downtime_backup.sh

set -e

# For large databases, use this approach to minimize impact

# 1. Setup replication if not already
# Ensure replica is in sync

# 2. Backup on replica (not primary)
ssh replica-server "xtrabackup --backup \
    --target-dir=/backup/from_replica/$(date +%Y%m%d) \
    --user=backup_user \
    --password='xxx'"

# 3. Copy backup from replica
rsync -av replica-server:/backup/from_replica/ /backup/mysql/

# 4. Verify backup
xtrabackup --prepare --target-dir=/backup/mysql/from_replica/

# 5. Record in backup history
mysql -u root -p -e "CALL log_backup_complete(...)"
```

### Pattern 2: Cloud Backup (S3)

```bash
#!/bin/bash
# backup_to_s3.sh

set -e

BACKUP_FILE="/backup/mysql/full_$(date +%Y%m%d).tar.gz"
S3_BUCKET="s3://company-mysql-backups"
S3_PATH="mysql/$(date +%Y)"

# Create backup
xtrabackup --backup \
    --target-dir=/tmp/xtrabackup_backup \
    --user=root --password="${MYSQL_ROOT_PASSWORD}"

# Prepare and compress
xtrabackup --prepare --target-dir=/tmp/xtrabackup_backup
tar -czf "${BACKUP_FILE}" -C /tmp/xtrabackup_backup .

# Upload to S3
aws s3 cp "${BACKUP_FILE}" "${S3_BUCKET}/${S3_PATH}/"

# Set lifecycle (expire after 30 days)
aws s3api put-bucket-lifecycle-configuration \
    --bucket company-mysql-backups \
    --lifecycle-configuration file://lifecycle.json

# Cleanup local
rm -rf /tmp/xtrabackup_backup
rm "${BACKUP_FILE}"

echo "Backup uploaded to S3"
```

### Pattern 3: Clone Database for Testing

```bash
#!/bin/bash
# clone_for_testing.sh

set -e

SOURCE_DB="production_db"
CLONE_DB="test_db_clone_$(date +%Y%m%d)"
BACKUP_DIR="/backup/clones"

# Create clone from recent backup
xtrabackup --backup \
    --target-dir="${BACKUP_DIR}/${CLONE_DB}" \
    --user=root --password="${MYSQL_ROOT_PASSWORD}"

xtrabackup --prepare --target-dir="${BACKUP_DIR}/${CLONE_DB}"

# Create new data directory for clone
mkdir -p /var/lib/mysql/${CLONE_DB}
chown mysql:mysql /var/lib/mysql/${CLONE_DB}

# Copy to new location
xtrabackup --copy-back \
    --target-dir="${BACKUP_DIR}/${CLONE_DB}" \
    --datadir=/var/lib/mysql/${CLONE_DB}

# Create database and import
mysql -u root -p -e "CREATE DATABASE ${CLONE_DB}"

# Import data (for mysqldump backup)
# mysql -u root -p ${CLONE_DB} < /backup/${SOURCE_DB}.sql

echo "Clone created: ${CLONE_DB}"
```

## Troubleshooting

### Vấn đề 1: Backup Fails với Lock Timeout

**Symptom**: mysqldump fails với error về table locks.

**Diagnosis**:
```sql
SHOW FULL PROCESSLIST;
-- Tìm các queries đang blocking
```

**Solution**:
```bash
# Use --single-transaction cho InnoDB tables
mysqldump -u root -p \
    --single-transaction \
    --database your_db > backup.sql

# Hoặc sử dụng --lock-tables=false
mysqldump -u root -p \
    --lock-tables=false \
    --quick \
    --database your_db > backup.sql

# Hoặc backup vào giờ low-traffic
```

### Vấn đề 2: XtraBackup Fails với Corruption

**Symptom**: XtraBackup prepare fails với checksum errors.

**Diagnosis**:
```bash
xtrabackup --prepare \
    --target-dir=/backup/full \
    2>&1 | grep -i error
```

**Solution**:
1. **Verify source data**
```bash
# Check tablespace integrity
mysql -u root -p -e "CHECK TABLE your_table;"
```

2. **Try partial prepare**
```bash
xtrabackup --prepare \
    --target-dir=/backup/full \
    --export
```

3. **Discard và reimport affected tablespace**
```sql
ALTER TABLE your_table DISCARD TABLESPACE;
-- Copy .ibd file
ALTER TABLE your_table IMPORT TABLESPACE;
```

### Vấn đề 3: Binary Log Bị Purge Trước Khi Backup Complete

**Symptom**: Cannot find binlog position needed for PITR.

**Solution**:
```ini
# Increase binlog retention
[mysqld]
binlog_expire_logs_seconds = 2592000  # 30 days
expire_logs_days = 30  # Deprecated but still works

# Schedule purges carefully
# Never purge logs automatically if using for PITR
```

```sql
-- Set purge schedule
-- Run during low traffic, after backup completes
PURGE BINARY LOGS BEFORE '2026-05-23 00:00:00';
```

### Vấn đề 4: Backup Too Large

**Symptom**: Backup files quá lớn, mất nhiều thời gian backup và restore.

**Solutions**:

1. **Use compression**
```bash
mysqldump | gzip > backup.sql.gz
xtrabackup --compress --compress-threads=4
```

2. **Partial backups**
```bash
# Backup chỉ critical tables
mysqldump db table1 table2 table3 > partial.sql
```

3. **Tune InnoDB settings for backup**
```ini
[mysqld]
innodb_flush_log_at_trx_commit = 2  # Slightly less safe but faster
```

4. **Use streaming backup**
```bash
xtrabackup --backup \
    --stream=xbstream \
    --target-dir=/backup \
    | ssh remote "xbstream -x -C /remote/backup"
```

## Ví dụ Thực tế

### Ví dụ 1: Complete Backup Automation System

```bash
#!/bin/bash
# mysql_backup_manager.sh

set -e

###############################################################################
# Configuration
###############################################################################
MYSQL_USER="backup_admin"
MYSQL_PASSWORD="SecureP@ssw0rd!"
BACKUP_BASE="/backup/mysql"
RETENTION_FULL=30
RETENTION_INCR=7
REMOTE_BACKUP=""
S3_BUCKET=""
EMAIL_ALERT="dba-team@company.com"

###############################################################################
# Functions
###############################################################################

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

error_exit() {
    log "ERROR: $1"
    send_alert "BACKUP FAILED: $1"
    exit 1
}

send_alert() {
    echo "$1" | mail -s "MySQL Backup Alert" ${EMAIL_ALERT}
}

cleanup_old_backups() {
    local type=$1
    local days=$2
    
    log "Cleaning up ${type} backups older than ${days} days"
    find ${BACKUP_BASE}/${type}* -maxdepth 0 -type d -mtime +${days} -exec rm -rf {} \; 2>/dev/null || true
}

run_full_backup() {
    local backup_dir="${BACKUP_BASE}/full_$(date +%Y%m%d_%H%M%S)"
    
    log "Starting FULL backup to ${backup_dir}"
    
    xtrabackup --backup \
        --target-dir="${backup_dir}" \
        --user="${MYSQL_USER}" \
        --password="${MYSQL_PASSWORD}" \
        --compress \
        --compress-threads=4 \
        --parallel=4 \
        --use-memory=2G \
        || error_exit "Full backup failed"
    
    # Calculate size
    local size=$(du -sh "${backup_dir}" | cut -f1)
    log "Full backup completed. Size: ${size}"
    
    # Update symlink
    ln -sfn "${backup_dir}" "${BACKUP_BASE}/latest_full"
    
    # Log to database
    mysql -u "${MYSQL_USER}" -p"${MYSQL_PASSWORD}" -e \
        "CALL log_backup_complete(1, 'completed', 0, NULL)"
    
    echo "${backup_dir}"
}

run_incremental_backup() {
    local basedir=$1
    local backup_dir="${BACKUP_BASE}/incr_$(date +%Y%m%d_%H%M%S)"
    
    log "Starting INCREMENTAL backup to ${backup_dir}"
    log "Base: ${basedir}"
    
    xtrabackup --backup \
        --target-dir="${backup_dir}" \
        --incremental-basedir="${basedir}" \
        --user="${MYSQL_USER}" \
        --password="${MYSQL_PASSWORD}" \
        --compress \
        --compress-threads=4 \
        --parallel=4 \
        || error_exit "Incremental backup failed"
    
    # Calculate size
    local size=$(du -sh "${backup_dir}" | cut -f1)
    log "Incremental backup completed. Size: ${size}"
    
    # Update symlink
    ln -sfn "${backup_dir}" "${BACKUP_BASE}/latest_incremental"
    
    echo "${backup_dir}"
}

upload_to_remote() {
    local backup_dir=$1
    
    if [ -n "${REMOTE_BACKUP}" ]; then
        log "Uploading backup to remote: ${REMOTE_BACKUP}"
        rsync -avz --delete \
            -e "ssh -i /root/.ssh/backup_key" \
            "${backup_dir}/" \
            "${REMOTE_BACKUP}/"
    fi
    
    if [ -n "${S3_BUCKET}" ]; then
        log "Uploading to S3: ${S3_BUCKET}"
        aws s3 sync "${backup_dir}/" "${S3_BUCKET}/mysql/$(basename ${backup_dir})/"
    fi
}

verify_backup() {
    local backup_dir=$1
    
    log "Verifying backup: ${backup_dir}"
    
    # Check directory exists
    [ -d "${backup_dir}" ] || error_exit "Backup directory not found"
    
    # Check xtrabackup_info exists
    [ -f "${backup_dir}/xtrabackup_info" ] || error_exit "xtrabackup_info not found"
    
    # Prepare backup
    xtrabackup --prepare \
        --target-dir="${backup_dir}" \
        --parallel=4 \
        2>&1 | grep -i "error\|warning" || true
    
    log "Backup verification completed"
}

###############################################################################
# Main
###############################################################################

# Ensure backup directory exists
mkdir -p ${BACKUP_BASE}/{full,incr,logs}

# Start backup
log "=== Starting MySQL Backup Process ==="

# Determine backup type
DAY_OF_WEEK=$(date +%w)
DAY_OF_MONTH=$(date +%d)

if [ "$DAY_OF_MONTH" -eq 1 ]; then
    # Monthly - full backup
    BACKUP_DIR=$(run_full_backup)
    cleanup_old_backups "full" ${RETENTION_FULL}
elif [ "$DAY_OF_WEEK" -eq 0 ]; then
    # Weekly - full backup
    BACKUP_DIR=$(run_full_backup)
    cleanup_old_backups "full" ${RETENTION_FULL}
else
    # Daily - incremental backup
    LATEST_FULL=$(readlink -f "${BACKUP_BASE}/latest_full" 2>/dev/null || echo "")
    
    if [ -z "${LATEST_FULL}" ] || [ ! -d "${LATEST_FULL}" ]; then
        log "No full backup found, creating one"
        BACKUP_DIR=$(run_full_backup)
    else
        BACKUP_DIR=$(run_incremental_backup "${LATEST_FULL}")
    fi
    
    cleanup_old_backups "incr" ${RETENTION_INCR}
fi

# Verify backup
verify_backup "${BACKUP_DIR}"

# Upload to remote/S3
upload_to_remote "${BACKUP_DIR}"

# Final cleanup
find ${BACKUP_BASE}/logs -type f -mtime +30 -delete

log "=== Backup Process Completed Successfully ==="
```

### Ví dụ 2: Disaster Recovery Runbook

```markdown
# MySQL Disaster Recovery Runbook

## Emergency Contacts
- DBA Lead: +1-555-0100
- DevOps Lead: +1-555-0101
- CTO: +1-555-0102

## Recovery Time Objectives
- RTO (Recovery Time Objective): 4 hours
- RPO (Recovery Point Objective): 1 hour

## Recovery Scenarios

### Scenario 1: Single Table Corruption
1. Identify corrupted table: `CHECK TABLE tablename;`
2. Determine last good backup containing table
3. Export table from backup: `xtrabackup --export`
4. Discard corrupted tablespace: `ALTER TABLE tablename DISCARD TABLESPACE;`
5. Copy good .ibd file
6. Import tablespace: `ALTER TABLE tablename IMPORT TABLESPACE;`
7. Verify: `CHECK TABLE tablename; ANALYZE TABLE tablename;`

### Scenario 2: Full Database Corruption
1. Stop MySQL: `systemctl stop mysql`
2. Assess damage
3. If replica available:
   - Promote replica to primary
   - Reconfigure other replicas
4. If no replica:
   - Restore from latest full backup
   - Apply incremental backups
   - Apply binlog to point-in-time
   - Verify data integrity

### Scenario 3: Server Failure (Complete Loss)
1. Provision new server
2. Install MySQL same version
3. Restore from backup:
   ```bash
   xtrabackup --copy-back --target-dir=/backup/full_latest --datadir=/var/lib/mysql
   ```
4. Update configuration
5. Start MySQL
6. Verify and test
7. Redirect traffic

### Scenario 4: Ransomware Attack
1. ISOLATE affected servers immediately
2. Do NOT pay ransom
3. Identify scope of damage
4. Restore from clean backup (before attack)
5. Apply binlogs up to attack time
6. Investigate breach vector
7. Implement additional security measures
8. Restore services gradually

## Verification Checklist
- [ ] MySQL starts successfully
- [ ] All databases accessible
- [ ] Replication configured (if applicable)
- [ ] Application connectivity tested
- [ ] Data integrity verified (row counts, checksums)
- [ ] Performance acceptable
- [ ] Monitoring alerts working
- [ ] Backup jobs resumed
```

### Ví dụ 3: Restore Testing Script

```bash
#!/bin/bash
# test_restore.sh

set -e

TEST_DB="test_restore_$(date +%Y%m%d%H%M%S)"
BACKUP_DIR="/backup/mysql"
MYSQL_USER="root"
MYSQL_PASSWORD="StrongP@ssw0rd!"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "=== Starting Restore Test ==="
log "Test database: ${TEST_DB}"

# 1. Count rows in production (source)
log "Counting rows in production..."
for table in $(mysql -u ${MYSQL_USER} -p${MYSQL_PASSWORD} -N -e \
    "SELECT TABLE_NAME FROM information_schema.tables WHERE table_schema='ecommerce' AND table_type='BASE TABLE'"); do
    count=$(mysql -u ${MYSQL_USER} -p${MYSQL_PASSWORD} -N -e \
        "SELECT COUNT(*) FROM ecommerce.${table}")
    echo "${table}:${count}" >> /tmp/source_counts.txt
done

# 2. Create test database
log "Creating test database..."
mysql -u ${MYSQL_USER} -p${MYSQL_PASSWORD} -e "CREATE DATABASE ${TEST_DB}"

# 3. Restore backup to test database
log "Restoring to test database..."
xtrabackup --prepare --target-dir="${BACKUP_DIR}/latest_full"
xtrabackup --copy-back \
    --target-dir="${BACKUP_DIR}/latest_full" \
    --datadir=/var/lib/mysql/${TEST_DB}

# 4. Compare row counts
log "Comparing row counts..."
mismatches=0

while IFS=: read -r table count; do
    test_count=$(mysql -u ${MYSQL_USER} -p${MYSQL_PASSWORD} -N -e \
        "SELECT COUNT(*) FROM ${TEST_DB}.${table}" 2>/dev/null || echo "0")
    
    if [ "$count" != "$test_count" ]; then
        log "MISMATCH: ${table} - source: ${count}, test: ${test_count}"
        ((mismatches++))
    fi
done < /tmp/source_counts.txt

# 5. Cleanup
log "Cleaning up..."
mysql -u ${MYSQL_USER} -p${MYSQL_PASSWORD} -e "DROP DATABASE ${TEST_DB}"
rm -f /tmp/source_counts.txt

# 6. Report
if [ $mismatches -eq 0 ]; then
    log "=== RESTORE TEST PASSED ==="
    exit 0
else
    log "=== RESTORE TEST FAILED: ${mismatches} mismatches ==="
    exit 1
fi
```

## Tham khảo

### Official Documentation

- [MySQL Backup and Recovery](https://dev.mysql.com/doc/refman/8.0/en/backup-and-recovery.html)
- [mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)
- [MySQL Enterprise Backup](https://dev.mysql.com/doc/mysql-enterprise-backup/8.0/en/)
- [XtraBackup Documentation](https://www.percona.com/doc/percona-xtrabackup/)

### Tools

- **mysqldump**: Logical backup (built-in)
- **MySQL Enterprise Backup**: Physical backup (Oracle)
- **Percona XtraBackup**: Physical backup (open-source)
- **mydumper**: Multi-threaded logical backup
- **MyDumper**: Alternative logical backup tool

### Monitoring và Alerting

```sql
-- Create view for backup monitoring
CREATE VIEW v_backup_status AS
SELECT 
    id,
    backup_type,
    backup_method,
    start_time,
    end_time,
    duration_seconds,
    ROUND(backup_size_bytes / 1024 / 1024, 2) AS size_mb,
    status,
    verified,
    error_message
FROM backup_history
ORDER BY start_time DESC
LIMIT 100;

-- Check recent backups
SELECT * FROM v_backup_status LIMIT 10;

-- Failed backups
SELECT * FROM backup_history 
WHERE status = 'failed' 
AND start_time > DATE_SUB(NOW(), INTERVAL 7 DAY);

-- Backup success rate
SELECT 
    COUNT(*) AS total,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS successful,
    ROUND(SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS success_rate
FROM backup_history
WHERE start_time > DATE_SUB(NOW(), INTERVAL 30 DAY);
```

---

*Document version: 1.0.0*
*Last updated: 2026-06-23*
*Framework: Cursor Enterprise Framework*
