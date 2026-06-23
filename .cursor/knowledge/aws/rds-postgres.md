---
title: "AWS RDS PostgreSQL Database Management"
description: "Hướng dẫn toàn diện về RDS PostgreSQL, read replicas, Multi-AZ, parameter groups, backups, Performance Insights và Aurora"
tags: ["aws", "rds", "postgresql", "database", "replicas", "multi-az", "aurora", "performance-insights"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# AWS RDS PostgreSQL Database Management

## Tổng Quan (Overview)

Amazon Relational Database Service (RDS) for PostgreSQL cung cấp managed database service với automatic patching, backups, và high availability features. RDS PostgreSQL là lựa chọn phổ biến cho applications cần relational database với minimal operational overhead, trong khi vẫn giữ được PostgreSQL compatibility và extensions.

Tài liệu này bao gồm comprehensive coverage của RDS PostgreSQL operations, bao gồm instance configuration và instance classes, high availability với Multi-AZ deployments, read scaling với read replicas, parameter groups configuration, automated backups và point-in-time recovery, Performance Insights cho monitoring, và migration strategies từ on-premises hoặc EC2-based PostgreSQL. Các best practices cho security, encryption, và cost optimization cũng được covered.

RDS là fully managed service, điều này có nghĩa là AWS handles routine database tasks như provisioning, patching, backups, và hardware failures, allowing teams to focus on application development và data management thay vì infrastructure maintenance.

## Mục Đích (Purpose)

Mục đích chính của tài liệu này bao gồm:

1. **High Availability**: Thiết lập Multi-AZ deployments cho automatic failover
2. **Scalability**: Configure read replicas cho read scaling và cross-region replication
3. **Data Protection**: Implement backup strategies và point-in-time recovery
4. **Performance**: Optimize với parameter groups, Performance Insights, và query analysis
5. **Security**: Apply encryption, IAM authentication, và network isolation
6. **Migration**: Move existing PostgreSQL databases to RDS với minimal downtime

## Các Khái Niệm Chính (Key Concepts)

### 1. RDS Instance Classes

RDS cung cấp nhiều instance classes tối ưu cho các workloads khác nhau:

| Class Family | Use Case | Ví Dụ |
|-------------|----------|-------|
| Standard (M) | General purpose workloads | db.m6g.xlarge, db.m5.large |
| Memory Optimized (R) | High memory requirements | db.r6g.2xlarge, db.r5.4xlarge |
| Burstable (T) | Light, variable workloads | db.t3.medium, db.t3.micro |
| Optimized Read | Heavy read workloads | db.r6gd.2xlarge |

```bash
# List available RDS instance classes
aws rds describe-orderable-db-instance-options \
  --engine postgres \
  --engine-version 15.4 \
  --query 'OrderableDBInstanceOptions[*].[DBInstanceClass,StorageType]' \
  --output table
```

### 2. RDS Instance Configuration

```yaml
# CloudFormation cho RDS PostgreSQL Instance
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  # VPC và Subnets
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: "10.0.0.0/16"
      EnableDnsHostnames: true
      EnableDnsSupport: true

  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: "10.0.1.0/24"
      AvailabilityZone: !Select [0, !GetAZs ""]

  PrivateSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: "10.0.2.0/24"
      AvailabilityZone: !Select [1, !GetAZs ""]

  DBSubnetGroup:
    Type: AWS::RDS::DBSubnetGroup
    Properties:
      DBSubnetGroupName: production-db-subnet-group
      DBSubnetGroupDescription: "Subnet group for RDS PostgreSQL"
      SubnetIds:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2

  # Security Groups
  RDSSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: "Security group for RDS PostgreSQL"
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 5432
          ToPort: 5432
          SourceSecurityGroupId: !Ref AppSecurityGroup
      SecurityGroupEgress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: "0.0.0.0/0"

  AppSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: "Security group for application servers"
      VpcId: !Ref VPC

  # KMS Key cho Encryption
  DBEncryptionKey:
    Type: AWS::KMS::Key
    Properties:
      Description: "KMS key for RDS encryption"
      KeyPolicy:
        Version: '2012-10-17'
        Statement:
          - Sid: Enable IAM User Permissions
            Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: kms:*
            Resource: '*'
          - Sid: Allow RDS to use key
            Effect: Allow
            Principal:
              Service: rds.amazonaws.com
            Action:
              - kms:CreateGrant
              - kms:Decrypt
              - kms:Encrypt
              - kms:GenerateDataKey
              - kms:DescribeKey
            Resource: '*'
            Condition:
              StringEquals:
                kms:ViaService: !Sub 'rds.${AWS::Region}.amazonaws.com'

  # RDS Instance
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: production-postgres
      Engine: postgres
      EngineVersion: "15.4"
      DBInstanceClass: db.r6g.2xlarge
      AllocatedStorage: 500
      StorageType: gp3
      StorageThroughput: 500
      Iops: 16000
      MaxAllocatedStorage: 1000
      DBSubnetGroupName: !Ref DBSubnetGroup
      VPCSecurityGroups:
        - !Ref RDSSecurityGroup
      MasterUsername: postgres_admin
      MasterUserPassword: !Ref DBPassword
      DBName: productiondb
      Port: 5432
      BackupRetentionPeriod: 30
      BackupWindow: "03:00-04:00"
      PreferredBackupWindow: "03:00-04:00"
      PreferredMaintenanceWindow: "sun:04:00-sun:05:00"
      MaintenanceWindow: "sun:04:00-sun:05:00"
      MultiAZ: true
      DBInstanceAutomatedBackupsReplicationEnabled: true
      DBInstanceAutomatedBackupsReplicationRegion: us-west-2
      StorageEncrypted: true
      KmsKeyId: !Ref DBEncryptionKey
      EnablePerformanceInsights: true
      PerformanceInsightsRetentionPeriod: 7
      PerformanceInsightsKMSKeyId: !Ref DBEncryptionKey
      EnableCloudwatchLogsExports:
        - postgresql
        - upgrade
      AutoMinorVersionUpgrade: true
      LicenseModel: postgresql-license
      PubliclyAccessible: false
      DeletionProtection: true
      OptionGroupName: !Ref OptionGroup
      ParameterGroupName: !Ref DBParameterGroup
      Tags:
        - Key: Environment
          Value: Production
        - Key: Application
          Value: ProductionAPI

  # Option Group
  OptionGroup:
    Type: AWS::RDS::OptionGroup
    Properties:
      OptionGroupName: production-option-group
      EngineName: postgres
      MajorEngineVersion: "15"
      OptionGroupDescription: "Option group for PostgreSQL 15"
      Options:
        - OptionName: "TDE"
        - OptionName: "OLE"
          OptionSettings:
            - Name: BACKUP_RETENTION_PERIOD
              Value: "30"
        - OptionName: "RAPID"
        - OptionName: "_AUTO_AOV"

  # Parameter Group
  DBParameterGroup:
    Type: AWS::RDS::DBParameterGroup
    Properties:
      Description: "Custom parameter group for PostgreSQL 15"
      Family: postgres15
      ParameterGroupName: production-pg15-params
      Parameters:
        max_connections: "500"
        shared_buffers: "{DBInstanceClassMemory*1/4}"
        effective_cache_size: "{DBInstanceClassMemory*1/4}"
        maintenance_work_mem: "512MB"
        checkpoint_completion_target: "0.9"
        wal_buffers: "16MB"
        default_statistics_target: "100"
        random_page_cost: "1.1"
        effective_io_concurrency: "200"
        work_mem: "4MB"
        min_wal_size: "1GB"
        max_wal_size: "4GB"
        max_worker_processes: "{DBInstanceClassMemory/8388608}"
        max_parallel_workers_per_gather: "4"
        max_parallel_workers: "8"
        max_parallel_maintenance_workers: "4"
        autovacuum_max_workers: "4"
        autovacuum_naptime: "30"
        log_destination: "csvlog"
        logging_collector: "on"
        log_connections: "on"
        log_disconnections: "on"
        log_duration: "off"
        log_line_prefix: "%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h "
        log_lock_waits: "on"
        log_min_duration_statement: "1000"
        log_temp_files: "0"
        log_min_messages: "WARNING"
        track_activities: "on"
        track_counts: "on"
        track_io_timing: "on"
        track_functions: "pl"
        track_activity_query_size: "4096"
        pgaudit.log: "all"
        pgaudit.log_parameter: "on"
        pgaudit.log_statement_once: "off"
        pgaudit.log_level: "log"

  # Secret cho Master Password
  DBPassword:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: /rds/production/master-password
      GenerateSecretString:
        SecretStringTemplate: '{"username": "postgres_admin"}'
        GenerateStringKey: "password"
        PasswordLength: 32
        ExcludeCharacters: "\"@/\\"
```

### 3. Read Replicas

Read replicas cho phép scale read operations bằng cách replicate data đến multiple instances.

```yaml
# Read Replica Configuration
ReadReplica1:
  Type: AWS::RDS::DBInstance
  Properties:
    DBInstanceIdentifier: production-pg-replica1
    Engine: postgres
    EngineVersion: "15.4"
    SourceDBInstanceIdentifier: !Ref DBInstance
    DBInstanceClass: db.r6g.xlarge
    StorageType: gp3
    PubliclyAccessible: false
    DBSubnetGroupName: !Ref DBSubnetGroup
    VPCSecurityGroups:
      - !Ref RDSSecurityGroup
    StorageEncrypted: true
    KmsKeyId: !Ref DBEncryptionKey
    Tags:
      - Key: Role
        Value: ReadReplica

ReadReplica2:
  Type: AWS::RDS::DBInstance
  Properties:
    DBInstanceIdentifier: production-pg-replica2
    Engine: postgres
    EngineVersion: "15.4"
    SourceDBInstanceIdentifier: !Ref DBInstance
    DBInstanceClass: db.r6g.xlarge
    StorageType: gp3
    PubliclyAccessible: false
    DBSubnetGroupName: !Ref DBSubnetGroup
    VPCSecurityGroups:
      - !Ref RDSSecurityGroup
    StorageEncrypted: true
    KmsKeyId: !Ref DBEncryptionKey
    Tags:
      - Key: Role
        Value: ReadReplica
```

```bash
# Create read replica
aws rds create-db-instance-read-replica \
  --db-instance-identifier production-pg-replica \
  --source-db-instance-identifier arn:aws:rds:us-east-1:123456789012:db:production-postgres \
  --db-instance-class db.r6g.xlarge \
  --storage-type gp3 \
  --no-publicly-accessible \
  --db-subnet-group-name production-db-subnet-group \
  --kms-key-id arn:aws:kms:us-east-1:123456789012:key/1234abcd-1234-1234-1234-123456789012 \
  --enable-performance-insights \
  --performance-insights-retention-period 7

# Promote read replica to standalone instance
aws rds promote-read-replica \
  --db-instance-identifier production-pg-replica \
  --backup-retention-period 30 \
  --preferred-backup-window "03:00-04:00"

# Create cross-region read replica
aws rds create-db-instance-read-replica \
  --db-instance-identifier production-pg-replica-uswest \
  --source-db-instance-identifier production-postgres \
  --db-instance-class db.r6g.xlarge \
  --region us-west-2 \
  --source-region us-east-1 \
  --storage-type gp3 \
  --no-publicly-accessible \
  --db-subnet-group-name production-db-subnet-group-west
```

### 4. Automated Backups và Point-in-Time Recovery

```yaml
# Backup Configuration in RDS Instance
Resources:
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      # ... other properties ...
      BackupRetentionPeriod: 30
      BackupWindow: "03:00-04:00"
      PreferredBackupWindow: "03:00-04:00"
      CopyTagsToSnapshots: true
      DeletionProtection: true
      # Cross-region backup replication
      DBInstanceAutomatedBackupsReplicationEnabled: true
      DBInstanceAutomatedBackupsReplicationRegion: us-west-2
```

```bash
# Create manual snapshot
aws rds create-db-snapshot \
  --db-instance-identifier production-postgres \
  --db-snapshot-identifier production-manual-backup-$(date +%Y%m%d%H%M%S)

# Copy snapshot to another region
aws rds copy-db-snapshot \
  --source-db-snapshot-identifier arn:aws:rds:us-east-1:123456789012:snapshot:production-backup \
  --target-db-snapshot-identifier production-backup-uswest \
  --source-region us-east-1 \
  --target-region us-west-2 \
  --encrypted true \
  --kms-key-id arn:aws:kms:us-west-2:123456789012:key/1234abcd-1234-1234-1234-123456789012

# Restore to point in time
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier production-postgres \
  --target-db-instance-identifier production-restored \
  --restore-time "2024-01-15T10:00:00Z" \
  --db-instance-class db.r6g.xlarge \
  --port 5432 \
  --no-publicly-accessible \
  --db-subnet-group-name production-db-subnet-group

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier production-restored \
  --db-snapshot-identifier production-manual-backup-20240115 \
  --db-instance-class db.r6g.xlarge \
  --no-publicly-accessible \
  --db-subnet-group-name production-db-subnet-group

# List snapshots
aws rds describe-db-snapshots \
  --db-instance-identifier production-postgres \
  --query 'DBSnapshots[*].[DBSnapshotIdentifier,Status,SnapshotCreateTime]' \
  --output table

# List automated backups
aws rds describe-db-instance-automated-backups \
  --db-instance-identifier production-postgres
```

### 5. Parameter Groups Configuration

```sql
-- Common PostgreSQL parameter optimizations for RDS

-- Connection settings
ALTER DATABASE productiondb SET max_connections = '500';

-- Memory settings (adjust based on instance class)
ALTER SYSTEM SET shared_buffers = '8GB';
ALTER SYSTEM SET effective_cache_size = '24GB';
ALTER SYSTEM SET work_mem = '16MB';
ALTER SYSTEM SET maintenance_work_mem = '1GB';

-- WAL settings
ALTER SYSTEM SET wal_buffers = '64MB';
ALTER SYSTEM SET min_wal_size = '2GB';
ALTER SYSTEM SET max_wal_size = '8GB';
ALTER SYSTEM SET checkpoint_completion_target = '0.9';

-- Parallel query settings
ALTER SYSTEM SET max_worker_processes = '16';
ALTER SYSTEM SET max_parallel_workers_per_gather = '4';
ALTER SYSTEM SET max_parallel_workers = '16';
ALTER SYSTEM SET max_parallel_maintenance_workers = '4';

-- Logging configuration
ALTER SYSTEM SET log_destination = 'csvlog';
ALTER SYSTEM SET logging_collector = 'on';
ALTER SYSTEM SET log_connections = 'on';
ALTER SYSTEM SET log_disconnections = 'on';
ALTER SYSTEM SET log_duration = 'off';
ALTER SYSTEM SET log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h';
ALTER SYSTEM SET log_lock_waits = 'on';
ALTER SYSTEM SET log_min_duration_statement = '1000';
ALTER SYSTEM SET log_temp_files = '0';

-- Autovacuum settings
ALTER SYSTEM SET autovacuum_max_workers = '4';
ALTER SYSTEM SET autovacuum_naptime = '30';
ALTER SYSTEM SET autovacuum_vacuum_threshold = '50';
ALTER SYSTEM SET autovacuum_analyze_threshold = '50';
ALTER SYSTEM SET autovacuum_vacuum_scale_factor = '0.1';
ALTER SYSTEM SET autovacuum_analyze_scale_factor = '0.05';

-- Query planner settings
ALTER SYSTEM SET random_page_cost = '1.1';
ALTER SYSTEM SET effective_io_concurrency = '200';
ALTER SYSTEM SET default_statistics_target = '200';

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gin;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS hstore;

-- Reload configuration
SELECT pg_reload_conf();
```

```bash
# Create custom parameter group
aws rds create-db-parameter-group \
  --db-parameter-group-name production-pg15-custom \
  --db-parameter-group-family postgres15 \
  --description "Custom parameter group for production PostgreSQL 15"

# Modify parameter
aws rds modify-db-parameter-group \
  --db-parameter-group-name production-pg15-custom \
  --parameters '[{"ParameterName": "log_min_duration_statement", "ParameterValue": "1000", "ApplyMethod": "pending-reboot"}]'

# List parameters in group
aws rds describe-db-parameters \
  --db-parameter-group-name production-pg15-custom \
  --query 'Parameters[*].[ParameterName,ParameterValue,ApplyMethod]' \
  --output table

# Compare parameter groups
aws rds describe-db-parameters \
  --db-parameter-group-name production-pg15-custom \
  --query 'Parameters[?IsModifiable==`true`].[ParameterName,ParameterValue]' > custom_params.txt

aws rds describe-db-parameters \
  --db-parameter-group-name default.postgres15 \
  --query 'Parameters[?IsModifiable==`true`].[ParameterName,ParameterValue]' > default_params.txt
```

### 6. Performance Insights

```bash
# Enable Performance Insights
aws rds modify-db-instance \
  --db-instance-identifier production-postgres \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --performance-insights-kms-key-id arn:aws:kms:us-east-1:123456789012:key/1234abcd-1234-1234-1234-123456789012

# Get Performance Insights metrics
aws pi get-resource-metrics \
  --service-type RDS \
  --identifier db-ABC123DEF456GHI789JKL \
  --metric-queries '[{"Metric": "db.load.avg", "GroupBy": {"Group": "db.engine_version"}}, {"Metric": "db.sql.stats.elapsed_total.sum", "GroupBy": {"Group": "db.sql.statement"}}, {"Metric": "db.wait_event.total.sum", "GroupBy": {"Group": "db.wait_event_type"}}]' \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T23:59:59Z \
  --period-in-seconds 60

# Get top SQL queries by wait time
aws pi describe-dimension-keys \
  --service-type RDS \
  --identifier db-ABC123DEF456GHI789JKL \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T23:59:59Z \
  --metric db.load.avg \
  --group-by '{"Group":"db.sql.statement"}' \
  --period-in-seconds 3600
```

```sql
-- Query Performance Insights data directly
SELECT 
  dbid,
  queryid,
  calls,
  total_exec_time / 1000 as total_seconds,
  mean_exec_time as mean_milliseconds,
  rows
FROM 
  pg_stat_statements
WHERE 
  calls > 100
ORDER BY 
  total_exec_time DESC
LIMIT 20;

-- Find slow queries
SELECT 
  query,
  calls,
  mean_exec_time,
  stddev_exec_time,
  rows,
  shared_blks_hit,
  shared_blks_read
FROM 
  pg_stat_statements
WHERE 
  mean_exec_time > 1000
ORDER BY 
  mean_exec_time DESC
LIMIT 10;

-- Check for locks
SELECT 
  pid,
  usename,
  pg_blocking_pids(pid) as blocked_by,
  query,
  state,
  wait_event_type,
  wait_event
FROM 
  pg_stat_activity
WHERE 
  state != 'idle'
  AND pid != pg_backend_pid()
ORDER BY 
  query_start;
```

## Best Practices

### 1. Security Best Practices

```yaml
# Enhanced monitoring và logging
DBInstance:
  Type: AWS::RDS::DBInstance
  Properties:
    # ... other properties ...
    EnableCloudwatchLogsExports:
      - postgresql
      - upgrade
    MonitoringInterval: 30
    MonitoringRoleArn: !GetAtt MonitoringRole.Arn
    PerformanceInsightsEnabled: true
    PerformanceInsightsRetentionPeriod: 31
    DeletionProtection: true

MonitoringRole:
  Type: AWS::IAM::Role
  Properties:
    AssumeRolePolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal:
            Service: monitoring.rds.amazonaws.com
          Action: sts:AssumeRole
    ManagedPolicyArns:
      - arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole

# IAM Authentication
DBInstance:
  Type: AWS::RDS::DBInstance
  Properties:
    # ... other properties ...
    EnableIAMDatabaseAuthentication: true
```

```sql
-- Enable IAM authentication
ALTER DATABASE productiondb SET rds.extensions = 'pg_stat_statements,pgaudit';
ALTER DATABASE productiondb SET rds.enable_iam_auth = '1';

-- Create user with IAM authentication
CREATE USER app_user WITH LOGIN;
GRANT rds_iam TO app_user;

-- Connect using IAM authentication (from application)
-- Use AWS SDK to generate auth token
-- Example: postgresql://[IAM User]@host:5432/db?sslrootcert=rds-ca-bundle.pem&sslmode=require
```

```bash
# Generate IAM authentication token
aws rds generate-db-auth-token \
  --hostname production-postgres.abc123def456.us-east-1.rds.amazonaws.com \
  --port 5432 \
  --username app_user
```

### 2. High Availability Configuration

```yaml
# Multi-AZ deployment với standby in different AZ
DBInstance:
  Type: AWS::RDS::DBInstance
  Properties:
    DBInstanceIdentifier: production-postgres
    MultiAZ: true
    # AZs will be automatically selected across availability zones
    # Primary in one AZ, standby in another
```

```bash
# Switchover (planned maintenance)
aws rds reboot-db-instance \
  --db-instance-identifier production-postgres \
  --force-failover

# Check Multi-AZ status
aws rds describe-db-instances \
  --db-instance-identifier production-postgres \
  --query 'DBInstances[0].MultiAZ'

# Check replica lag
aws rds describe-db-instances \
  --db-instance-identifier production-postgres \
  --query 'DBInstances[0].ReadReplicaDBInstanceIdentifiers'
```

### 3. Connection Pooling với PgBouncer

```yaml
# PgBouncer configuration for connection pooling
Resources:
  PgBouncerSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for PgBouncer
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 6432
          ToPort: 6432
          SourceSecurityGroupId: !Ref AppSecurityGroup

  PgBouncerInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t3.medium
      SubnetId: !Ref PrivateSubnet1
      SecurityGroupIds:
        - !Ref PgBouncerSecurityGroup
      ImageId: ami-0c55b159cbfafe1f0
      UserData:
        Fn::Base64: |
          #!/bin/bash
          yum update -y
          amazon-linux-extras install epel -y
          yum install -y pgbouncer
          
          # Configure PgBouncer
          cat > /etc/pgbouncer/pgbouncer.ini << 'EOF'
          [databases]
          production = host=production-postgres.abc123def456.us-east-1.rds.amazonaws.com port=5432 dbname=productiondb

          [pgbouncer]
          listen_addr = *
          listen_port = 6432
          auth_type = md5
          auth_file = /etc/pgbouncer/userlist.txt
          pool_mode = transaction
          max_client_conn = 1000
          default_pool_size = 50
          min_pool_size = 10
          reserve_pool_size = 10
          reserve_pool_timeout = 5
          max_db_connections = 200
          server_idle_timeout = 600
          log_connections = 1
          log_disconnections = 1
          log_pooler_errors = 1
          admin_users = admin
          stats_users = stats
          EOF

          # Create userlist
          cat > /etc/pgbouncer/userlist.txt << 'EOF'
          "admin" "md5..."
          "stats" "md5..."
          "app_user" "md5..."
          EOF

          systemctl start pgbouncer
          systemctl enable pgbouncer
```

## Common Patterns

### Pattern 1: Aurora PostgreSQL Migration

```yaml
# Aurora PostgreSQL Cluster
AuroraCluster:
  Type: AWS::RDS::DBCluster
  Properties:
    DBClusterIdentifier: production-aurora-cluster
    Engine: aurora-postgresql
    EngineVersion: "15.4"
    EngineMode: provisioned
    DatabaseName: productiondb
    MasterUsername: admin
    MasterUserPassword: !Ref DBPassword
    DBClusterParameterGroupName: !Ref AuroraParameterGroup
    DBSubnetGroupName: !Ref DBSubnetGroup
    VpcSecurityGroupIds:
      - !Ref RDSSecurityGroup
    StorageEncrypted: true
    KmsKeyId: !Ref DBEncryptionKey
    BackupRetentionPeriod: 30
    PreferredBackupWindow: "03:00-04:00"
    PreferredMaintenanceWindow: "sun:04:00-sun:05:00"
    Port: 5432
    EnableHttpEndpoint: true
    CopyTagsToSnapshots: true
    DeletionProtection: true
    GlobalClusterIdentifier: !Ref GlobalCluster
    SourceRegion: !Ref AWS::Region

AuroraInstance1:
  Type: AWS::RDS::DBInstance
  Properties:
    DBInstanceIdentifier: production-aurora-instance-1
    Engine: aurora-postgresql
    DBClusterIdentifier: !Ref AuroraCluster
    DBInstanceClass: db.r6g.xlarge
    DBSubnetGroupName: !Ref DBSubnetGroup
    PubliclyAccessible: false
    DBInstanceAutomatedBackupsReplicationEnabled: true
    PerformanceInsightsEnabled: true
    Tags:
      - Key: Role
        Value: Writer

AuroraInstance2:
  Type: AWS::RDS::DBInstance
  Properties:
    DBInstanceIdentifier: production-aurora-instance-2
    Engine: aurora-postgresql
    DBClusterIdentifier: !Ref AuroraCluster
    DBInstanceClass: db.r6g.xlarge
    DBSubnetGroupName: !Ref DBSubnetGroup
    PubliclyAccessible: false
    PromotionTier: 1
    Tags:
      - Key: Role
        Value: Reader

AuroraParameterGroup:
  Type: AWS::RDS::DBClusterParameterGroup
  Properties:
    Description: Aurora PostgreSQL 15 parameter group
    Family: aurora-postgresql15
    Parameters:
      aurora_parallel_query: "ON"
      aurora_optimized_writer: "ON"
      max_connections: "10000"
      shared_buffers: "{DBInstanceClassMemory*1/4}"
```

```bash
# Create Aurora read replica from RDS PostgreSQL
aws rds create-db-cluster \
  --db-cluster-identifier production-aurora-cluster \
  --engine aurora-postgresql \
  --engine-version 15.4 \
  --db-cluster-parameter-group-name default.aurora-postgresql15 \
  --db-subnet-group-name production-db-subnet-group \
  --vpc-security-group-ids sg-0123456789abcdef0 \
  --source-db-instance-identifier production-postgres

# Add instances to cluster
aws rds create-db-instance \
  --db-instance-identifier production-aurora-instance-1 \
  --db-cluster-identifier production-aurora-cluster \
  --engine aurora-postgresql \
  --db-instance-class db.r6g.xlarge

# Promote Aurora cluster to primary
aws rds switchover-global-cluster \
  --global-cluster-identifier production-global-cluster
```

### Pattern 2: Automated Backup và Disaster Recovery

```yaml
# AWS Backup Plan
BackupVault:
  Type: AWS::Backup::BackupVault
  Properties:
    BackupVaultName: production-backup-vault
    EncryptionKeyArn: !Ref BackupKMSKey
    Notifications:
      BackupVaultEvents:
        - BACKUP_JOB_COMPLETED
        - BACKUP_JOB_FAILED
        - COPY_JOB_COMPLETED
        - COPY_JOB_FAILED
      SNSTopicArn: !Ref BackupSNSTopic

BackupPlan:
  Type: AWS::AWS::Backup::BackupPlan
  Properties:
    BackupPlanName: production-backup-plan
    BackupPlanRule:
      - RuleName: daily-backup
        TargetBackupVaultName: !Ref BackupVault
        ScheduleExpression: "cron(0 4 ? * * *)"
        StartWindowMinutes: 60
        CompletionWindowMinutes: 180
        Lifecycle:
          DeleteAfterDays: 35
        CopyActions:
          - DestinationBackupVaultArn: !GetAtt BackupVaultCrossRegion.Arn
            Lifecycle:
              DeleteAfterDays: 90
      - RuleName: monthly-backup
        ScheduleExpression: "cron(0 5 1 * ? *)"
        TargetBackupVaultName: !Ref BackupVault
        StartWindowMinutes: 60
        CompletionWindowMinutes: 300
        Lifecycle:
          DeleteAfterDays: 365
      - RuleName: continuous-backup
        TargetBackupVaultName: !Ref BackupVault
        ScheduleExpression: "cron(0/15 * ? * * *)"
        StartWindowMinutes: 15
        CompletionWindowMinutes: 120
        Lifecycle:
          DeleteAfterDays: 7

BackupSelection:
  Type: AWS::Backup::BackupSelection
  Properties:
    BackupPlanId: !Ref BackupPlan
    BackupSelection:
      SelectionName: production-rds-selection
      IamRoleArn: !GetAtt BackupRole.Arn
      Resources:
        - !Sub 'arn:aws:rds:${AWS::Region}:${AWS::AccountId}:db:${DBInstance}'
        - !GetAtt AuroraCluster.Arn
      ListOfTags:
        - ConditionType: STRINGEQUALS
          ConditionKey: Environment
          ConditionValue: Production
```

## Troubleshooting

### Common Issues và Solutions

**1. High CPU hoặc Memory Usage**

```bash
# Check performance insights
aws pi get-resource-metrics \
  --service-type RDS \
  --identifier db-ABC123DEF456 \
  --metric-queries '[{"Metric": "db.load.avg"}, {"Metric": "db.cpu.utilization.avg"}, {"Metric": "db.memory.utilization.avg"}]' \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period-in-seconds 60

# Get top queries
aws pi describe-statement-history \
  --service-type RDS \
  --identifier db-ABC123DEF456 \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T23:59:59Z \
  --filter-by "db.sql.statement LIKE '%SELECT%'" \
  --sort-by "total_exec_time" \
  --sort-order DESC

# Check for long-running queries
aws rds mod \
  --db-instance-identifier production-postgres
```

```sql
-- Find problematic queries
SELECT 
  pid,
  now() - pg_stat_activity.query_start AS duration,
  usename,
  query,
  state,
  wait_event_type,
  wait_event
FROM 
  pg_stat_activity
WHERE 
  (state != 'idle') 
  AND (now() - pg_stat_activity.query_start) > interval '5 minutes'
ORDER BY 
  duration DESC;

-- Terminate problematic query
SELECT pg_cancel_backend(pid) FROM pg_stat_activity WHERE ...;
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE ...;

-- Check for missing indexes
SELECT 
  schemaname,
  tablename,
  seq_scan,
  seq_tup_read,
  idx_scan,
  idx_tup_fetch,
  n_tup_ins,
  n_tup_upd,
  n_tup_del,
  n_live_tup,
  n_dead_tup
FROM 
  pg_stat_user_tables
WHERE 
  seq_scan > idx_scan * 10
ORDER BY 
  seq_scan DESC;
```

**2. Replication Lag**

```bash
# Check replica lag
aws rds describe-db-instances \
  --db-instance-identifier production-postgres \
  --query 'DBInstances[0].ReadReplicaDBInstanceIdentifiers'

# For each replica:
aws rds describe-db-instances \
  --db-instance-identifier production-pg-replica1 \
  --query 'DBInstances[0].ReplicaStatus'

# Get detailed metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name ReplicaLag \
  --dimensions Name=DBInstanceIdentifier,Value=production-pg-replica1 \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Average,Maximum
```

```sql
-- Check replication status on primary
SELECT 
  pid,
  usesysid,
  usename,
  application_name,
  client_addr,
  client_hostname,
  backend_start,
  backend_xmin,
  state,
  sent_lsn,
  write_lsn,
  flush_lsn,
  replay_lsn,
  write_lag,
  flush_lag,
  replay_lag,
  sync_priority,
  sync_state
FROM 
  pg_stat_replication;

-- Check replication slots
SELECT 
  slot_name,
  plugin,
  slot_type,
  datoid,
  database,
  active,
  pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) as retained_wal
FROM 
  pg_replication_slots;

-- Check wal sender status
SELECT 
  application_name,
  state,
  sent_lsn,
  write_lsn,
  flush_lsn,
  replay_lsn,
  sync_state
FROM 
  pg_stat_replication;
```

**3. Connection Issues**

```bash
# Check max connections
aws rds describe-db-parameters \
  --db-parameter-group-name production-pg15-params \
  --query 'Parameters[?ParameterName==`max_connections`]'

# Check current connections
aws rds describe-db-log-file \
  --db-instance-identifier production-postgres \
  --log-file-name error/postgresql.log.2024-01-15

# Test connectivity
psql -h production-postgres.abc123def456.us-east-1.rds.amazonaws.com \
     -U postgres_admin \
     -d productiondb \
     -c "SELECT 1;"
```

```sql
-- Check active connections
SELECT 
  datname,
  numbackends,
  xact_commit,
  xact_rollback,
  blks_read,
  blks_hit,
  tup_returned,
  tup_fetched,
  tup_inserted,
  tup_updated,
  tup_deleted,
  conflicts,
  temp_files,
  temp_bytes,
  deadlocks,
  blk_read_time,
  blk_write_time,
  stats_reset
FROM 
  pg_stat_database
WHERE 
  datname = 'productiondb';

-- Kill idle connections
SELECT 
  pg_terminate_backend(pid)
FROM 
  pg_stat_activity
WHERE 
  state = 'idle'
  AND state_change < now() - interval '30 minutes';

-- Check for connection leaks in application
SELECT 
  application_name,
  COUNT(*),
  state
FROM 
  pg_stat_activity
GROUP BY 
  application_name,
  state;
```

**4. Storage Issues**

```bash
# Check storage metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name FreeStorageSpace \
  --dimensions Name=DBInstanceIdentifier,Value=production-postgres \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 \
  --statistics Average,Minimum

# Check DiskQueueDepth
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name DiskQueueDepth \
  --dimensions Name=DBInstanceIdentifier,Value=production-postgres \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 60 \
  --statistics Average,Maximum

# Modify storage
aws rds modify-db-instance \
  --db-instance-identifier production-postgres \
  --allocated-storage 1000 \
  --apply-immediately
```

## Examples

### Example 1: Migration từ On-Premises PostgreSQL

```bash
#!/bin/bash
# Migration script from on-premises to RDS PostgreSQL

# Variables
SOURCE_HOST="on-prem-db.example.com"
SOURCE_PORT="5432"
SOURCE_DB="productiondb"
SOURCE_USER="migration_user"
TARGET_DB="productiondb"
RDS_HOST="production-postgres.abc123def456.us-east-1.rds.amazonaws.com"
RDS_PORT="5432"
RDS_USER="postgres_admin"
S3_BUCKET="migration-artifacts"
S3_PREFIX="pg-migration"

# Step 1: Create migration user on source
psql -h $SOURCE_HOST -p $SOURCE_PORT -U postgres -d $SOURCE_DB << EOF
CREATE USER migration_user WITH REPLICATION;
GRANT CONNECT ON DATABASE $SOURCE_DB TO migration_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO migration_user;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO migration_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO migration_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE ON SEQUENCES TO migration_user;
EOF

# Step 2: Set up replication slot on source
psql -h $SOURCE_HOST -p $SOURCE_PORT -U postgres -d $SOURCE_DB << EOF
SELECT pg_create_logical_replication_slot('mydb_replication', 'pgoutput');
EOF

# Step 3: Export schema
pg_dump -h $SOURCE_HOST -p $SOURCE_PORT -U $SOURCE_USER -d $SOURCE_DB \
  --schema-only \
  --no-owner \
  --no-acl \
  --file=schema.sql

# Step 4: Upload schema to S3
aws s3 cp schema.sql s3://$S3_BUCKET/$S3_PREFIX/schema.sql

# Step 5: Restore schema to RDS
psql -h $RDS_HOST -p $RDS_PORT -U $RDS_USER -d postgres << EOF
CREATE DATABASE $TARGET_DB;
EOF

psql -h $RDS_HOST -p $RDS_PORT -U $RDS_USER -d $TARGET_DB < schema.sql

# Step 6: Export data (chunked for large tables)
pg_dump -h $SOURCE_HOST -p $SOURCE_PORT -U $SOURCE_USER -d $SOURCE_DB \
  --data-only \
  --no-owner \
  --no-acl \
  --format=custom \
  --file=data_dump.dump

# Step 7: Upload and restore
aws s3 cp data_dump.dump s3://$S3_BUCKET/$S3_PREFIX/data_dump.dump

# Download and restore
aws s3 cp s3://$S3_BUCKET/$S3_PREFIX/data_dump.dump /tmp/data_dump.dump
pg_restore -h $RDS_HOST -p $RDS_PORT -U $RDS_USER -d $TARGET_DB --data-only /tmp/data_dump.dump

# Step 8: Verify data integrity
psql -h $RDS_HOST -p $RDS_PORT -U $RDS_USER -d $TARGET_DB << EOF
-- Row counts match
SELECT 'users' as table_name, COUNT(*) as row_count FROM users
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'products', COUNT(*) FROM products;

-- Checksum verification
SELECT 'users' as table_name, md5(string_agg(id::text, '')) as checksum FROM users
EOF
```

### Example 2: Terraform Production Setup

```terraform
# Terraform configuration for RDS PostgreSQL
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "rds-vpc"
  }
}

# Subnets
resource "aws_subnet" "private" {
  count = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = false

  tags = {
    Name = "rds-private-subnet-${count.index + 1}"
  }
}

# RDS Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "main-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "main-db-subnet-group"
  }
}

# Security Group
resource "aws_security_group" "rds" {
  name        = "rds-sg"
  description = "Security group for RDS PostgreSQL"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds-security-group"
  }
}

resource "aws_security_group" "app" {
  name        = "app-sg"
  description = "Security group for application servers"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "app-security-group"
  }
}

# KMS Key
resource "aws_kms_key" "main" {
  description = "KMS key for RDS encryption"
  deletion_window_in_days = 10
  enable_key_rotation = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid = "Enable IAM User Permissions"
        Effect = Allow
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action = "kms:*"
        Resource = "*"
      },
      {
        Sid = "Allow RDS to use key"
        Effect = Allow
        Principal = {
          Service = "rds.amazonaws.com"
        }
        Action = [
          "kms:CreateGrant",
          "kms:Decrypt",
          "kms:Encrypt",
          "kms:GenerateDataKey",
          "kms:DescribeKey"
        ]
        Resource = "*"
        Condition = {
          StringEquals = {
            "kms:ViaService" = "rds.${data.aws_region.current.name}.amazonaws.com"
          }
        }
      }
    ]
  })
}

# Parameter Group
resource "aws_db_parameter_group" "main" {
  name   = "production-pg15-params"
  family = "postgres15"
  description = "Custom parameter group for PostgreSQL 15"

  parameter {
    name  = "max_connections"
    value = "500"
  }

  parameter {
    name  = "shared_buffers"
    value = "8GB"
  }

  parameter {
    name  = "effective_cache_size"
    value = "24GB"
  }

  parameter {
    name  = "work_mem"
    value = "16MB"
  }

  parameter {
    name  = "maintenance_work_mem"
    value = "1GB"
  }

  parameter {
    name  = "log_connections"
    value = "on"
  }

  parameter {
    name  = "log_disconnections"
    value = "on"
  }

  parameter {
    name  = "log_min_duration_statement"
    value = "1000"
  }

  parameter {
    name  = "random_page_cost"
    value = "1.1"
  }

  parameter {
    name  = "effective_io_concurrency"
    value = "200"
  }
}

# Option Group
resource "aws_db_option_group" "main" {
  name                 = "production-option-group"
  engine_name          = "postgres"
  major_engine_version = "15"

  option {
    option_name = "PGAUDIT"
    option_settings {
      name  = "LOG_CONNECTIONS"
      value = "1"
    }
    option_settings {
      name  = "LOG_DISCONNECTIONS"
      value = "1"
    }
    option_settings {
      name  = "LOG_STATEMENT"
      value = "all"
    }
  }
}

# RDS Instance
resource "aws_db_instance" "main" {
  identifier = "production-postgres"

  engine               = "postgres"
  engine_version       = "15.4"
  family               = "postgres15"
  parameter_group_name = aws_db_parameter_group.main.name
  option_group_name    = aws_db_option_group.main.name

  instance_class = "db.r6g.2xlarge"

  allocated_storage     = 500
  max_allocated_storage = 1000
  storage_type          = "gp3"
  storage_throughput    = 500
  iops                  = 16000

  db_name  = "productiondb"
  username = "postgres_admin"
  password = data.aws_secretsmanager_secret_version.db_password.secret_string

  port = 5432

  multi_az               = true
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  backup_retention_period   = 30
  backup_window             = "03:00-04:00"
  preferred_backup_window   = "03:00-04:00"
  preferred_maintenance_window = "sun:04:00-sun:05:00"

  deletion_protection = true

  storage_encrypted  = true
  kms_key_id        = aws_kms_key.main.arn

  performance_insights_enabled          = true
  performance_insights_retention_period = 31
  performance_insights_kms_key_id       = aws_kms_key.main.arn

  enable_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  auto_minor_version_upgrade = true

  publicly_accessible = false

  copy_tags_to_snapshot = true

  skip_final_snapshot       = false
  final_snapshot_identifier = "production-postgres-final-snapshot"

  enabled_cloudwatch_logs_exports = ["postgresql"]

  tags = {
    Name        = "production-postgres"
    Environment = "production"
  }
}

# Read Replicas
resource "aws_db_instance" "read_replica1" {
  identifier = "production-postgres-replica1"

  engine               = "postgres"
  engine_version       = "15.4"
  parameter_group_name = aws_db_parameter_group.main.name
  option_group_name    = aws_db_option_group.main.name

  instance_class = "db.r6g.xlarge"

  storage_type          = "gp3"
  storage_throughput    = 500
  iops                  = 8000

  source_db_instance_identifier = aws_db_instance.main.id
  db_subnet_group_name         = aws_db_subnet_group.main.name
  vpc_security_group_ids       = [aws_security_group.rds.id]

  storage_encrypted  = true
  kms_key_id        = aws_kms_key.main.arn

  performance_insights_enabled          = true
  performance_insights_retention_period = 31
  performance_insights_kms_key_id       = aws_kms_key.main.arn

  publicly_accessible = false

  deletion_protection = false

  tags = {
    Name        = "production-postgres-replica1"
    Environment = "production"
    Role        = "read-replica"
  }
}

# Secrets Manager for password
resource "aws_secretsmanager_secret" "db_password" {
  name = "rds-production-password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db_password.result
}

resource "random_password" "db_password" {
  length  = 32
  special = false
}
```

## References

### Official Documentation
- [Amazon RDS Documentation](https://docs.aws.amazon.com/AmazonRDS/)
- [RDS PostgreSQL Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)
- [RDS Best Practices](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.html)
- [Aurora PostgreSQL Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.html)
- [Performance Insights](https://docs.aws.amazon.com/performance-insights/latest/user/working-with-PICS.html)

### Tools
- [AWS Database Migration Service](https://aws.amazon.com/dms/)
- [pglogical](https://www.2ndquadrant.com/en/resources/pglogical/)
- [Babelfish for Aurora PostgreSQL](https://docs.aws.amazon.com/aurora/latest/laws/migrate-babelfish.html)
- [RDS Query Editor](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/query-editor.html)

### PostgreSQL Resources
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html)
- [pgBadger](https://pgbadger.darold.net/)
- [PostgreSQL Wiki - Performance](https://wiki.postgresql.org/wiki/Performance_Optimization)
