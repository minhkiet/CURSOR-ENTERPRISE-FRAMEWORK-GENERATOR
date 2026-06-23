---
title: "SQL Server Deployment and Performance Checklist"
description: "Comprehensive pre-deployment and performance review checklist for SQL Server databases. Covers security, indexing, query optimization, backup, monitoring, and production readiness validation."
tags: ["sql-server", "checklist", "deployment", "performance", "database", "review", "production"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# SQL Server Deployment and Performance Checklist

## Tổng Quan (Overview)

Checklist này được thiết kế như một framework toàn diện để review SQL Server databases trước khi deploy lên production environment. Nó bao gồm tất cả các khía cạnh quan trọng: security configuration, index design, query performance, backup strategy, high availability setup, và monitoring requirements.

Việc sử dụng checklist một cách systematic trước mỗi deployment giúp đảm bảo rằng không có critical issues bị miss và giảm thiểu rủi ro của production incidents. Mỗi item trong checklist đều có giải thích ngắn gọn về lý do tại sao nó quan trọng và hướng dẫn cách verify.

Checklist này phù hợp cho nhiều loại deployments: new database schema, application upgrades, major changes to existing tables, stored procedures, và indexes. Đối với mỗi deployment type, bạn nên focus vào các sections liên quan nhưng vẫn verify các items critical khác.

## Mục Đích (Purpose)

Tài liệu này phục vụ như một operational guide cho đội ngũ phát triển và vận hành. Mục đích chính là cung cấp một standardized process để:

**Pre-Deployment Review**: Đảm bảo tất cả các changes đã được thoroughly reviewed trước khi đưa lên production. Checklist giúp identify potential issues trước khi chúng trở thành production problems.

**Performance Validation**: Xác nhận rằng các changes mới không gây ra performance regressions và tuân thủ performance standards của organization.

**Security Compliance**: Verify rằng database configuration và application code tuân thủ security policies và best practices.

**Documentation**: Tạo ra audit trail của các reviews đã thực hiện, decisions đã made, và any exceptions đã được documented.

## Key Concepts

### Checklist Structure

Mỗi section trong checklist bao gồm:

**Category Description**: Giải thích ngắn về lý do tại sao category này quan trọng.

**Checklist Items**: Danh sách các specific checks với:
- Check description
- Verification method (how to verify)
- Pass criteria
- Severity level

**Exceptions**: Section để document any exceptions với rationale và approval.

## Pre-Deployment Security Checklist

### Authentication and Authorization

- [ ] **SQL Server Authentication Mode**: Verify production uses Windows Authentication hoặc Mixed Mode với strong password policies enforced. Mixed Mode nên chỉ được sử dụng khi applications require it.

- [ ] **Server-level Logins**: Audit all server-level logins. Remove any unused or unnecessary logins. Principle of Least Privilege phải được áp dụng.

```sql
-- Script to list all server logins with last login time
SELECT 
    sp.name AS login_name,
    sp.type_desc AS login_type,
    sp.create_date,
    sp.modify_date,
    sp.is_disabled,
    LOGINPROPERTY(sp.name, 'LastLoginsTime') AS last_login_time,
    LOGINPROPERTY(sp.name, 'PasswordLastSetTime') AS password_last_set
FROM sys.server_principals sp
WHERE sp.type IN ('S', 'U')  -- SQL login and Windows user
    AND sp.name NOT LIKE '##%'  -- Exclude system logins
ORDER BY sp.create_date DESC;
```

- [ ] **Database Users**: Verify all database users are mapped to appropriate server logins. Orphaned users (users without login mappings) phải được investigated và fixed.

```sql
-- Find orphaned users
EXEC sp_change_users_login 'Report';

-- Fix orphaned user
EXEC sp_change_users_login 'Auto_Fix', 'username';
```

- [ ] **Server Roles**: Review membership of server roles, đặc biệt là sysadmin, securityadmin, và db_owner. Minimize số lượng users trong high-privilege roles.

```sql
-- List members of fixed server roles
SELECT 
    sp.name AS role_name,
    sp.type_desc,
    rm.member_principal_id,
    mp.name AS member_name,
    mp.type_desc AS member_type
FROM sys.server_role_members rm
JOIN sys.server_principals sp ON rm.role_principal_id = sp.principal_id
JOIN sys.server_principals mp ON rm.member_principal_id = mp.principal_id
WHERE sp.is_fixed_role = 1
ORDER BY sp.name, mp.name;
```

- [ ] **Application Roles**: If using application roles, verify passwords are stored securely và application code properly activates roles.

### Database-level Security

- [ ] **Database Ownership**: Verify database owner là một appropriate account (thường là a service account hoặc dedicated admin account), không phải individual user account.

```sql
-- Check database owner
SELECT 
    name AS database_name,
    owner_sid,
    SUSER_SNAME(owner_sid) AS owner_name,
    create_date
FROM sys.databases
WHERE name = 'YourDatabase';
```

- [ ] **Schemas**: Review all database schemas. Ensure schemas align with security boundaries và ownership is properly assigned.

```sql
-- List schemas with owners
SELECT 
    s.name AS schema_name,
    SCHEMA_OWNER(s.schema_id) AS owner_name,
    dp.name AS owner_login
FROM sys.schemas s
JOIN sys.database_principals dp ON SCHEMA_OWNER(s.schema_id) = dp.principal_id
ORDER BY s.name;
```

- [ ] **Schema Permissions**: Audit explicit permissions on schemas, tables, views, và stored procedures. Remove unnecessary grants.

```sql
-- List explicit database permissions
SELECT 
    dp.name AS principal_name,
    dp.type_desc AS principal_type,
    OBJECT_SCHEMA_NAME(o.object_id) AS schema_name,
    o.name AS object_name,
    o.type_desc AS object_type,
    pm.permission_name,
    pm.state_desc
FROM sys.database_permissions pm
JOIN sys.database_principals dp ON pm.grantee_principal_id = dp.principal_id
LEFT JOIN sys.objects o ON pm.major_id = o.object_id
WHERE dp.type IN ('S', 'U', 'G')  -- SQL user, Windows user, Windows group
ORDER BY dp.name, OBJECT_SCHEMA_NAME(o.object_id), o.name;
```

- [ ] **Sensitive Data Classification**: Verify all sensitive columns (PII, financial data, credentials) are properly classified và protected.

```sql
-- Check for potential sensitive columns
SELECT 
    TABLE_SCHEMA,
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME IN (SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE')
    AND (
        COLUMN_NAME LIKE '%password%'
        OR COLUMN_NAME LIKE '%ssn%'
        OR COLUMN_NAME LIKE '%credit%'
        OR COLUMN_NAME LIKE '%address%'
        OR COLUMN_NAME LIKE '%phone%'
        OR COLUMN_NAME LIKE '%email%'
        OR COLUMN_NAME LIKE '%dob%'
        OR COLUMN_NAME LIKE '%birth%'
    )
ORDER BY TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME;
```

### Encryption and Network Security

- [ ] **Connection Encryption**: Verify production connections use TLS/SSL encryption. Check `Force Encryption` setting in SQL Server Configuration Manager.

```sql
-- Check encryption status of current connection
SELECT 
    encrypt_option,
    session_id,
    connect_time,
    client_net_address
FROM sys.dm_exec_connections
WHERE session_id = @@SPID;
```

- [ ] **Transparent Data Encryption (TDE)**: For databases containing sensitive data, verify TDE is enabled hoặc evaluate if it should be.

```sql
-- Check TDE status
SELECT 
    db.name AS database_name,
    db.is_encrypted,
    db.encryption_state,
    db.percent_complete,
    db.key_algorithm,
    db.encryption_type_desc,
    dm_cryptographic_provider_name
FROM sys.databases db
LEFT JOIN sys.dm_database_encryption_keys dek ON db.database_id = dm_database_id = dek.database_id
WHERE db.name = 'YourDatabase';
```

- [ ] **Backup Encryption**: Verify backups are encrypted, especially for production databases.

```sql
-- Check for encrypted backups
SELECT 
    bs.backup_set_id,
    bs.media_set_id,
    bs.backup_start_date,
    bs.backup_finish_date,
    bs.compression_status,
    CASE WHEN bf.encrypted = 1 THEN 'Encrypted' ELSE 'Not Encrypted' END AS encryption_status,
    bs.backup_size,
    bs.encrypted
FROM msdb.dbo.backupset bs
LEFT JOIN msdb.dbo.backupmediafamily bf ON bs.media_set_id = bf.media_set_id
WHERE bs.database_name = 'YourDatabase'
ORDER BY bs.backup_start_date DESC;
```

## Database Design and Schema Checklist

### Table Design

- [ ] **Primary Keys**: Verify all tables have primary keys defined. Natural keys vs surrogate keys đã được properly evaluated.

```sql
-- Find tables without primary keys
SELECT 
    OBJECT_SCHEMA_NAME(t.object_id) AS schema_name,
    t.name AS table_name
FROM sys.tables t
LEFT JOIN sys.key_constraints kc ON t.object_id = kc.parent_object_id 
    AND kc.type = 'PK'
WHERE kc.object_id IS NULL
    AND t.is_ms_shipped = 0
ORDER BY schema_name, table_name;
```

- [ ] **Data Types**: Review data types for columns. Ensure appropriate types are used (e.g., INT for IDs, DECIMAL for monetary values, DATETIME2 for new development).

```sql
-- List columns with deprecated data types
SELECT 
    OBJECT_SCHEMA_NAME(c.object_id) AS schema_name,
    OBJECT_NAME(c.object_id) AS table_name,
    c.name AS column_name,
    t.name AS data_type,
    c.max_length,
    c.precision,
    c.scale
FROM sys.columns c
JOIN sys.types t ON c.user_type_id = t.user_type_id
WHERE t.name IN ('text', 'ntext', 'image')
    AND c.object_id IN (SELECT object_id FROM sys.tables WHERE is_ms_shipped = 0)
ORDER BY schema_name, table_name, column_name;
```

- [ ] **NULL vs NOT NULL**: Verify all columns have appropriate NULL/NOT NULL constraints. Avoid allowing NULLs in columns where they don't make sense (e.g., primary keys).

```sql
-- List columns allowing NULLs in tables
SELECT 
    OBJECT_SCHEMA_NAME(c.object_id) AS schema_name,
    OBJECT_NAME(c.object_id) AS table_name,
    c.name AS column_name,
    t.name AS data_type,
    c.is_nullable
FROM sys.columns c
JOIN sys.types t ON c.user_type_id = t.user_type_id
WHERE c.is_nullable = 1
    AND c.object_id IN (SELECT object_id FROM sys.tables WHERE is_ms_shipped = 0)
    AND t.name NOT IN ('varbinary', 'varchar', 'nvarchar', 'varbinary(max)', 'varchar(max)', 'nvarchar(max)')
ORDER BY schema_name, table_name;
```

- [ ] **Default Values**: Verify columns have appropriate DEFAULT constraints where applicable to avoid NULL issues và improve INSERT performance.

- [ ] **Computed Columns**: Consider using computed columns for derived values that are frequently queried. Verify PERSISTED attribute is used when appropriate.

### Constraint Design

- [ ] **Foreign Keys**: Verify all referential integrity is enforced through proper foreign key constraints. Check ON DELETE và ON UPDATE actions are appropriate.

```sql
-- List all foreign key constraints
SELECT 
    OBJECT_SCHEMA_NAME(f.parent_object_id) AS schema_name,
    OBJECT_NAME(f.parent_object_id) AS table_name,
    f.name AS foreign_key_name,
    COL_NAME(fc.parent_object_id, fc.parent_column_id) AS column_name,
    OBJECT_SCHEMA_NAME(f.referenced_object_id) AS referenced_schema,
    OBJECT_NAME(f.referenced_object_id) AS referenced_table,
    COL_NAME(fc.referenced_object_id, fc.referenced_column_id) AS referenced_column,
    f.delete_referential_action_desc,
    f.update_referential_action_desc,
    f.is_disabled
FROM sys.foreign_keys f
INNER JOIN sys.foreign_key_columns fc ON f.object_id = fc.constraint_object_id
WHERE f.parent_object_id IN (SELECT object_id FROM sys.tables WHERE is_ms_shipped = 0)
ORDER BY schema_name, table_name;
```

- [ ] **Check Constraints**: Review CHECK constraints for data validation. Ensure they are not overly complex (complex CHECK constraints can impact INSERT/UPDATE performance).

- [ ] **Unique Constraints**: Verify all uniqueness requirements are enforced through UNIQUE constraints or unique indexes.

- [ ] **Disabled Constraints**: Identify any disabled constraints that might allow invalid data to be entered. Investigate và re-enable or drop if no longer needed.

```sql
-- Find disabled constraints
SELECT 
    OBJECT_SCHEMA_NAME(parent_object_id) AS schema_name,
    OBJECT_NAME(parent_object_id) AS table_name,
    name AS constraint_name,
    type_desc,
    is_disabled,
    is_not_for_replication
FROM sys.check_constraints
WHERE is_disabled = 1;

SELECT 
    OBJECT_SCHEMA_NAME(parent_object_id) AS schema_name,
    OBJECT_NAME(parent_object_id) AS table_name,
    name AS foreign_key_name,
    is_disabled
FROM sys.foreign_keys
WHERE is_disabled = 1;
```

## Index Design Checklist

### Clustered Index

- [ ] **Clustered Index Strategy**: Verify each table has appropriate clustered index. Consider sequential keys (IDENTITY) for high-insert tables to minimize page splits.

```sql
-- List clustered indexes
SELECT 
    OBJECT_SCHEMA_NAME(i.object_id) AS schema_name,
    OBJECT_NAME(i.object_id) AS table_name,
    i.name AS index_name,
    i.type_desc,
    i.is_primary_key,
    STUFF((
        SELECT ', ' + c.name
        FROM sys.index_columns ic
        JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
        WHERE ic.object_id = i.object_id AND ic.index_id = i.index_id AND ic.is_included_column = 0
        ORDER BY ic.key_ordinal
        FOR XML PATH('')
    ), 1, 2, '') AS key_columns
FROM sys.indexes i
WHERE i.type = 1  -- Clustered
    AND i.object_id IN (SELECT object_id FROM sys.tables WHERE is_ms_shipped = 0)
ORDER BY schema_name, table_name;
```

- [ ] **Wide vs Narrow Keys**: Evaluate clustered index key width. Narrow keys result in smaller non-clustered indexes và better overall performance.

### Non-Clustered Indexes

- [ ] **Index Coverage Analysis**: For frequently executed queries, verify covering indexes exist to eliminate bookmark lookups.

- [ ] **Unused Indexes**: Identify và remove indexes that are never used (no seeks, scans, or lookups).

```sql
-- Find unused indexes (not used in last 30 days)
SELECT 
    OBJECT_SCHEMA_NAME(i.object_id) AS schema_name,
    OBJECT_NAME(i.object_id) AS table_name,
    i.name AS index_name,
    i.type_desc,
    i.is_primary_key,
    i.is_unique,
    SUM(us.user_seeks) AS total_seeks,
    SUM(us.user_scans) AS total_scans,
    SUM(us.user_lookups) AS total_lookups,
    SUM(us.user_seeks + us.user_scans) AS total_usage
FROM sys.indexes i
LEFT JOIN sys.dm_db_index_usage_stats us ON i.object_id = us.object_id AND i.index_id = us.index_id
WHERE i.type > 0  -- Non-clustered
    AND i.is_primary_key = 0
    AND i.object_id IN (SELECT object_id FROM sys.tables WHERE is_ms_shipped = 0)
GROUP BY i.object_id, i.name, i.type_desc, i.is_primary_key, i.is_unique
HAVING SUM(us.user_seeks + us.user_scans + us.user_lookups) = 0
    OR SUM(us.user_seeks + us.user_scans + us.user_lookups) IS NULL
ORDER BY schema_name, table_name;
```

- [ ] **Duplicate Indexes**: Identify indexes with identical or overlapping columns that can be consolidated.

```sql
-- Find potentially duplicate indexes
SELECT 
    OBJECT_SCHEMA_NAME(i1.object_id) AS schema_name,
    OBJECT_NAME(i1.object_id) AS table_name,
    i1.name AS index1_name,
    i1.type_desc AS index1_type,
    i2.name AS index2_name,
    i2.type_desc AS index2_type,
    STUFF((
        SELECT ', ' + c.name
        FROM sys.index_columns ic
        JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
        WHERE ic.object_id = i1.object_id AND ic.index_id = i1.index_id AND ic.is_included_column = 0
        ORDER BY ic.key_ordinal
        FOR XML PATH('')
    ), 1, 2, '') AS index1_columns,
    STUFF((
        SELECT ', ' + c.name
        FROM sys.index_columns ic
        JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
        WHERE ic.object_id = i2.object_id AND ic.index_id = i2.index_id AND ic.is_included_column = 0
        ORDER BY ic.key_ordinal
        FOR XML PATH('')
    ), 1, 2, '') AS index2_columns
FROM sys.indexes i1
JOIN sys.indexes i2 ON i1.object_id = i2.object_id 
    AND i1.index_id < i2.index_id
    AND i1.type > 0
    AND i2.type > 0
WHERE i1.object_id IN (SELECT object_id FROM sys.tables WHERE is_ms_shipped = 0)
ORDER BY schema_name, table_name;
```

### Columnstore Indexes

- [ ] **Analytical Workload**: If database supports both OLTP và analytical workloads, evaluate columnstore indexes for analytical queries.

```sql
-- Check for columnstore indexes
SELECT 
    OBJECT_SCHEMA_NAME(i.object_id) AS schema_name,
    OBJECT_NAME(i.object_id) AS table_name,
    i.name AS index_name,
    i.type_desc
FROM sys.indexes i
WHERE i.type IN (5, 6)  -- Clustered and Non-clustered columnstore
ORDER BY schema_name, table_name;
```

## Query Performance Checklist

### Execution Plan Analysis

- [ ] **Plan Quality Review**: For critical stored procedures và frequently executed queries, review actual execution plans. Look for:
  - Table scans vs index seeks
  - Bookmark lookups
  - Large row estimates vs actuals
  - Sort operations without index support

```sql
-- Get top queries by total execution time
SELECT TOP 20
    SUBSTRING(st.text, (qs.statement_start_offset / 2) + 1,
        ((CASE qs.statement_end_offset
          WHEN -1 THEN DATALENGTH(st.text)
          ELSE qs.statement_end_offset
         END - qs.statement_start_offset) / 2) + 1) AS query_text,
    qs.execution_count,
    qs.total_elapsed_time / 1000 AS total_elapsed_ms,
    qs.total_elapsed_time / (qs.execution_count * 1000) AS avg_elapsed_ms,
    qs.total_logical_reads / qs.execution_count AS avg_logical_reads,
    qs.total_physical_reads / qs.execution_count AS avg_physical_reads,
    qp.query_plan
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) st
CROSS APPLY sys.dm_exec_query_plan(qs.plan_handle) qp
WHERE qs.execution_count > 10
ORDER BY qs.total_elapsed_time DESC;
```

- [ ] **Missing Index Recommendations**: Review DMF output for missing index recommendations. Evaluate và implement where appropriate.

```sql
-- Get missing index details
SELECT 
    migs.avg_user_impact,
    migs.user_seeks,
    migs.user_scans,
    mid.statement,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns,
    'CREATE INDEX IX_' + OBJECT_NAME(mid.object_id) + '_' 
        + REPLACE(REPLACE(ISNULL(mid.equality_columns, ''), '[', ''), ']', '')
        + '_' + REPLACE(REPLACE(ISNULL(mid.inequality_columns, ''), '[', ''), ']', '')
        + ' ON ' + mid.statement 
        + ' (' + ISNULL(mid.equality_columns, '') 
            + CASE WHEN mid.inequality_columns IS NOT NULL THEN ', ' + mid.inequality_columns ELSE '' END + ')'
        + CASE WHEN mid.included_columns IS NOT NULL THEN ' INCLUDE (' + mid.included_columns + ')' ELSE '' END
        AS recommended_index
FROM sys.dm_db_missing_index_details mid
JOIN sys.dm_db_missing_index_groups mig ON mid.index_handle = mig.index_handle
JOIN sys.dm_db_missing_index_group_stats migs ON mig.index_group_handle = migs.group_handle
WHERE migs.avg_user_impact > 30
    AND migs.user_seeks > 100
ORDER BY migs.avg_user_impact DESC;
```

### Query Pattern Review

- [ ] **SELECT * Usage**: Search codebase cho queries sử dụng SELECT *. These should be replaced with specific column lists.

```sql
-- Find cached plans with wide selects
-- Note: This requires parsing query text
```

- [ ] **Cursor Usage**: Identify stored procedures sử dụng cursors. Evaluate if set-based alternatives are feasible.

```sql
-- Search for cursor usage in stored procedures
SELECT 
    OBJECT_NAME(object_id) AS procedure_name,
    definition
FROM sys.sql_modules
WHERE definition LIKE '%CURSOR%'
ORDER BY OBJECT_NAME(object_id);
```

- [ ] **NOLOCK Usage**: Review queries using NOLOCK hint. Ensure appropriate justification và consider alternative isolation levels.

```sql
-- Find NOLOCK usage in stored procedures
SELECT 
    OBJECT_NAME(object_id) AS procedure_name,
    definition
FROM sys.sql_modules
WHERE definition LIKE '%NOLOCK%'
ORDER BY OBJECT_NAME(object_id);
```

## Backup and Recovery Checklist

### Backup Verification

- [ ] **Backup History**: Verify backup history shows successful backups. Check for any gaps in backup chain.

```sql
-- Recent backup history
SELECT 
    bs.backup_set_id,
    bs.database_name,
    bs.backup_start_date,
    bs.backup_finish_date,
    CASE bs.type
        WHEN 'D' THEN 'Full'
        WHEN 'I' THEN 'Differential'
        WHEN 'L' THEN 'Log'
        ELSE 'Other'
    END AS backup_type,
    bs.compression_status,
    bs.backup_size / 1024 / 1024 AS backup_size_mb,
    CAST(100.0 * bs.backup_size / NULLIF(bf.file_size, 0) AS DECIMAL(5,2)) AS compression_ratio,
    CASE WHEN bs.is_copy_only = 1 THEN 'Yes' ELSE 'No' END AS is_copy_only,
    bs.is_damaged,
    bs.has_backup_checksums,
    bs.first_family_number,
    bm.physical_device_name,
    bs.user_name,
    bs.machine_name
FROM msdb.dbo.backupset bs
JOIN msdb.dbo.backupmediafamily bm ON bs.media_set_id = bm.media_set_id
WHERE bs.backup_start_date > DATEADD(DAY, -30, GETDATE())
ORDER BY bs.backup_start_date DESC;
```

- [ ] **Backup Validation**: Run RESTORE VERIFYONLY để confirm backups are valid và restorable.

```sql
-- Verify most recent backup
RESTORE VERIFYONLY 
FROM DISK = 'D:\Backups\YourDatabase_Full.bak'
WITH CHECKSUM;
```

### Recovery Model

- [ ] **Recovery Model**: Verify recovery model is appropriate for RPO requirements:
  - FULL: For databases requiring point-in-time recovery
  - BULK_LOGGED: For databases with large bulk operations
  - SIMPLE: For databases where simple recovery is acceptable

```sql
-- Check recovery model
SELECT 
    name AS database_name,
    recovery_model_desc,
    log_reuse_wait_desc,
    state_desc
FROM sys.databases
WHERE name = 'YourDatabase';
```

### DR Testing

- [ ] **Restore Test**: Perform periodic restore tests to verify backup integrity và familiarize team với restore procedures.

- [ ] **RPO/RTO Documentation**: Document actual RPO (Recovery Point Objective) và RTO (Recovery Time Objective) achievable với current backup strategy.

## High Availability Checklist

### Always On Availability Groups

- [ ] **AG Health**: Verify all availability groups are healthy với synchronized replicas.

```sql
-- Check AG health
SELECT 
    ag.name AS ag_name,
    ag.is_failover_cluster,
    ag.automatic_failover_mode_desc,
    replicas.replica_server_name,
    replicas.availability_mode_desc,
    replicas.failover_mode_desc,
    replica_states.synchronization_state_desc,
    replica_states.is_local,
    replica_states.last_redone_lsn,
    replica_states.last_commit_lsn,
    replica_states.secondary_lag_seconds
FROM sys.availability_groups ag
JOIN sys.availability_replicas replicas ON ag.group_id = replicas.group_id
JOIN sys.dm_hadr_availability_replica_states replica_states ON replicas.replica_id = replica_states.replica_id
ORDER BY ag.name, replicas.replica_server_name;
```

- [ ] **Backup Preferences**: Verify backup preferences are configured và backups are running on secondary replicas if configured.

- [ ] **Read-Only Routing**: If using read-scale availability groups, verify read-only routing is configured correctly.

### Failover Cluster

- [ ] **Cluster Health**: Verify Windows Failover Cluster is healthy with all nodes online.

```powershell
# PowerShell command to check cluster health
Get-Cluster | Get-ClusterNode | Format-Table Name, State, NodeWeight
Get-Cluster | Get-ClusterResource | Format-Table Name, State, OwnerNode
```

- [ ] **Quorum**: Verify cluster quorum configuration is appropriate.

## Monitoring and Maintenance Checklist

### Index Maintenance

- [ ] **Fragmentation Review**: Check index fragmentation levels và schedule appropriate maintenance (rebuild vs reorganize).

```sql
-- Check index fragmentation
SELECT 
    OBJECT_SCHEMA_NAME(i.object_id) AS schema_name,
    OBJECT_NAME(i.object_id) AS table_name,
    i.name AS index_name,
    ips.avg_fragmentation_in_percent,
    ips.page_count,
    ips.avg_page_space_used_in_percent,
    CASE 
        WHEN ips.avg_fragmentation_in_percent > 40 THEN 'Rebuild'
        WHEN ips.avg_fragmentation_in_percent > 10 THEN 'Reorganize'
        ELSE 'No Action'
    END AS recommended_action
FROM sys.dm_db_index_physical_stats(
    DB_ID(), NULL, NULL, NULL, 'DETAILED') ips
JOIN sys.indexes i ON ips.object_id = i.object_id AND ips.index_id = i.index_id
WHERE ips.alloc_unit_type_desc = 'IN_ROW_DATA'
    AND ips.page_count > 100
ORDER BY ips.avg_fragmentation_in_percent DESC;
```

### Statistics Maintenance

- [ ] **Statistics Update Status**: Verify statistics are being automatically updated và are current.

```sql
-- Check statistics update dates
SELECT 
    OBJECT_SCHEMA_NAME(s.object_id) AS schema_name,
    OBJECT_NAME(s.object_id) AS table_name,
    s.name AS statistics_name,
    STATS_DATE(s.object_id, s.stats_id) AS last_updated,
    s.auto_created,
    s.user_created,
    s.no_recompute,
    sc.name AS column_name
FROM sys.stats s
CROSS APPLY sys.stats_columns sc
WHERE s.object_id = sc.object_id 
    AND s.stats_id = sc.stats_id
    AND sc.stats_column_id = 1
    AND OBJECTPROPERTY(s.object_id, 'IsUserTable') = 1
ORDER BY STATS_DATE(s.object_id, s.stats_id);
```

### Performance Baseline

- [ ] **Baseline Metrics**: Document baseline performance metrics (CPU, memory, disk I/O, query performance) để compare against future performance.

```sql
-- Get current performance metrics
SELECT 
    @@SERVERNAME AS server_name,
    GETDATE() AS capture_time,
    (SELECT COUNT(*) FROM sys.dm_exec_requests) AS active_requests,
    (SELECT COUNT(*) FROM sys.dm_exec_sessions WHERE status = 'sleeping') AS sleeping_sessions,
    (SELECT COUNT(*) FROM sys.dm_exec_sessions WHERE is_user_process = 1 AND status = 'running') AS user_running,
    (SELECT COUNT(*) FROM sys.dm_exec_sessions WHERE is_user_process = 1 AND status = 'runnable') AS user_runnable,
    (SELECT COUNT(*) FROM sys.dm_exec_sessions WHERE is_user_process = 1 AND status = 'suspended') AS user_suspended,
    (SELECT COUNT(*) FROM sys.dm_exec_sessions WHERE is_user_process = 1 AND status = 'blocked') AS user_blocked,
    (SELECT COUNT(*) FROM sys.dm_exec_requests WHERE blocking_session_id > 0) AS blocking_chains;
```

## Production Readiness Checklist

### Documentation

- [ ] **Schema Documentation**: All tables, columns, và constraints are documented.

- [ ] **Stored Procedure Documentation**: All stored procedures have header comments describing purpose, parameters, và usage examples.

- [ ] **Architecture Documentation**: Database architecture (including HA/DR setup) is documented và current.

### Operational Procedures

- [ ] **Runbook**: Runbook exists for common operational tasks:
  - Deployment procedures
  - Backup/restore procedures
  - Failover procedures
  - Performance troubleshooting
  - Common issue resolution

- [ ] **Alerting**: Production monitoring alerts are configured và tested.

```sql
-- Verify SQL Agent jobs are enabled
SELECT 
    j.name AS job_name,
    j.enabled,
    j.description,
    j.date_created,
    j.date_modified,
    jh.run_status,
    jh.run_date,
    jh.run_time,
    jh.run_duration,
    CASE jh.run_status
        WHEN 0 THEN 'Failed'
        WHEN 1 THEN 'Succeeded'
        WHEN 2 THEN 'Retry'
        WHEN 3 THEN 'Canceled'
        WHEN 4 THEN 'In Progress'
    END AS last_run_status
FROM msdb.dbo.sysjobs j
LEFT JOIN (
    SELECT job_id, run_status, run_date, run_time, run_duration,
           ROW_NUMBER() OVER (PARTITION BY job_id ORDER BY run_date DESC, run_time DESC) AS rn
    FROM msdb.dbo.sysjobhistory
    WHERE step_id = 0
) jh ON j.job_id = jh.job_id AND jh.rn = 1
WHERE j.enabled = 0
ORDER BY j.name;
```

- [ ] **Change Control**: Change control process is followed for all production changes.

## Sign-Off Section

### Review Completion

| Check Category | Reviewer | Date | Status |
|---------------|----------|------|--------|
| Security | | | |
| Schema Design | | | |
| Index Design | | | |
| Query Performance | | | |
| Backup/Recovery | | | |
| High Availability | | | |
| Monitoring | | | |
| Documentation | | | |

### Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Database Lead | | | |
| Security Reviewer | | | |
| Application Owner | | | |
| Operations | | | |

### Known Issues and Exceptions

| Issue/Exception | Impact | Mitigation | Approved By | Date |
|----------------|--------|------------|-------------|------|
| | | | | |

## References

- SQL Server Documentation: https://docs.microsoft.com/en-us/sql/sql-server/
- Security Best Practices: https://docs.microsoft.com/en-us/sql/relational-databases/security/securing-sql-server
- Index Best Practices: https://docs.microsoft.com/en-us/sql/relational-databases/sql-server-index-design-guide
- Backup and Restore: https://docs.microsoft.com/en-us/sql/relational-databases/backup-restore/back-up-and-restore-of-sql-server-databases
- Always On Availability Groups: https://docs.microsoft.com/en-us/sql/database-engine/availability-groups/windows/always-on-availability-groups-sql-server
