# SQL Server Checklist - Danh Sách Kiểm Tra

## Giới thiệu

Danh sách kiểm tra toàn diện cho việc triển khai và quản lý SQL Server trong môi trường enterprise. Sử dụng danh sách này để đảm bảo best practices được tuân thủ.

---

## 1. Installation và Configuration

### 1.1. Pre-Installation

- [ ] Xác định phiên bản SQL Server phù hợp (SQL 2019/2022 Enterprise)
- [ ] Kiểm tra hardware requirements:
  - [ ] CPU: Minimum 2 cores, recommend 4+ cores cho production
  - [ ] RAM: Minimum 4GB, recommend 16GB+, max 50% of OS RAM
  - [ ] Disk: Separate drives cho Data, Log, TempDB, Backup
  - [ ] Storage type: SSD/Flash cho production workloads
- [ ] Verify Windows Server version compatibility
- [ ] Kiểm tra .NET Framework requirements
- [ ] Đảm bảo Windows Updates đã được áp dụng
- [ ] Disable Antivirus trên SQL Server data files (hoặc exclude properly)
- [ ] Verify Service Account permissions

### 1.2. Instance Configuration

```sql
-- Server-level configuration
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;

-- Memory configuration
EXEC sp_configure 'max server memory (MB)', 32768; -- Set to 50-70% of total RAM
EXEC sp_configure 'min server memory (MB)', 8192;

-- CPU configuration
EXEC sp_configure 'max degree of parallelism', 4; -- Set based on cores
EXEC sp_configure 'cost threshold for parallelism', 50;

-- Network configuration
EXEC sp_configure 'network packet size', 8192; -- For large data transfers

-- Additional settings
EXEC sp_configure 'remote admin connections', 1; -- DAC access
EXEC sp_configure 'scan for startup procs', 1;

RECONFIGURE;
```

### 1.3. Database Files Layout

- [ ] Separate data and log files onto different drives
- [ ] Use multiple data files for large databases (1 file per 4-8 cores)
- [ ] Size data files appropriately from the start
- [ ] Set appropriate autogrowth settings (not percentage-based)
- [ ] Enable Instant File Initialization for data files
- [ ] Configure TempDB appropriately:
  - [ ] Multiple data files (equal to CPU cores, max 8)
  - [ ] Size files equally
  - [ ] Remove autogrowth for TempDB

```sql
-- Ideal TempDB configuration
ALTER DATABASE tempdb 
MODIFY FILE (NAME = tempdev, SIZE = 1GB, FILEGROWTH = 256MB);
GO

ALTER DATABASE tempdb 
ADD FILE (NAME = tempdev2, SIZE = 1GB, FILEGROWTH = 256MB);
GO

-- Add more files up to number of cores (max 8)
ALTER DATABASE tempdb 
ADD FILE (NAME = tempdev3, SIZE = 1GB, FILEGROWTH = 256MB);
GO
```

---

## 2. Security Checklist

### 2.1. Authentication và Access Control

- [ ] Use Windows Authentication mode when possible
- [ ] If mixed mode required, enforce strong password policy:
  ```sql
  -- Enforce password policy
  ALTER LOGIN [LoginName] WITH CHECK_POLICY = ON;
  ALTER LOGIN [LoginName] WITH CHECK_EXPIRATION = ON;
  ```
- [ ] Implement Principle of Least Privilege:
  - [ ] Separate application logins from admin logins
  - [ ] Use roles instead of direct permissions
  - [ ] Grant only necessary permissions on objects
- [ ] Disable sa account or rename it
  ```sql
  -- Disable sa login
  ALTER LOGIN sa DISABLE;
  ```
- [ ] Disable SQL Server Browser service if not needed
- [ ] Use dedicated service accounts (not Local System)

### 2.2. Permission Management

- [ ] Create application roles for different access levels
  ```sql
  CREATE APPLICATION ROLE AppReadOnlyRole 
  WITH PASSWORD = 'ComplexPassword123!';
  
  GRANT SELECT ON SCHEMA::dbo TO AppReadOnlyRole;
  ```
- [ ] Implement schema-based security
  ```sql
  CREATE SCHEMA Application AUTHORIZATION dbo;
  CREATE SCHEMA Reporting AUTHORIZATION dbo;
  
  -- Move objects to appropriate schemas
  ALTER SCHEMA Application TRANSFER dbo.MyStoredProcedure;
  ```
- [ ] Review and remove excessive permissions regularly
  ```sql
  -- Find users with sysadmin role
  SELECT name, type_desc, is_disabled 
  FROM sys.server_principals 
  WHERE sysadmin = 1;
  
  -- Find overly permissive logins
  SELECT * FROM sys.server_permissions 
  WHERE permission_name = 'CONTROL SERVER';
  ```
- [ ] Implement column-level security when needed
  ```sql
  CREATE SECURITY POLICY FilterSensitiveData
  ADD FILTER PREDICATE dbo.fn_SensitiveColumnPredicate(EmployeeID) 
  ON HumanResources.Salary
  WITH (STATE = ON);
  ```

### 2.3. Encryption

- [ ] Enable Transparent Data Encryption (TDE) for sensitive databases
  ```sql
  USE master;
  CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'ComplexPassword!';
  CREATE CERTIFICATE TDECert WITH SUBJECT = 'TDE Certificate';
  BACKUP CERTIFICATE TDECert TO FILE = 'C:\Backups\TDECert.cer'
  PRIVATE KEY (FILE = 'C:\Backups\TDECert.key', 
               ENCRYPTION BY PASSWORD = 'KeyPassword!');
  
  USE MyDB;
  CREATE DATABASE ENCRYPTION KEY
  BY ALGORITHM = AES_256
  ENCRYPTION BY SERVER CERTIFICATE TDECert;
  ALTER DATABASE MyDB SET ENCRYPTION ON;
  ```
- [ ] Use Always Encrypted for highly sensitive columns
  ```sql
  CREATE TABLE SensitiveData (
      SSN CHAR(11) COLLATE Latin1_General_BIN2 
          ENCRYPTED WITH (ENCRYPTION_TYPE = DETERMINISTIC,
                         ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256',
                         COLUMN_ENCRYPTION_KEY = MyCEK) NOT NULL
  );
  ```
- [ ] Encrypt connections using TLS
- [ ] Secure backup files with encryption
  ```sql
  BACKUP DATABASE MyDB 
  TO DISK = 'C:\Backups\MyDB_Encrypted.bak'
  WITH COMPRESSION, ENCRYPTION (ALGORITHM = AES_256, 
                               SERVER CERTIFICATE = TDECert);
  ```

### 2.4. Auditing và Compliance

- [ ] Enable SQL Server Audit
  ```sql
  CREATE SERVER AUDIT SPECIFICATION ServerAuditSpec
  FOR SERVER AUDIT MyServerAudit
  ADD (SUCCESSFUL_LOGIN_GROUP),
  ADD (FAILED_LOGIN_GROUP),
  ADD (LOGOUT_GROUP);
  
  ALTER SERVER AUDIT SPECIFICATION ServerAuditSpec WITH (STATE = ON);
  ```
- [ ] Track database changes with DDL triggers
  ```sql
  CREATE TRIGGER trg_AuditDDLChanges
  ON DATABASE
  FOR DDL_DATABASE_LEVEL_EVENTS
  AS
  BEGIN
      INSERT INTO AuditLog (EventType, ObjectName, SQLCommand, LoginName)
      SELECT 
          EVENTDATA().value('(/EVENT_INSTANCE/EventType)[1]', 'NVARCHAR(100)'),
          EVENTDATA().value('(/EVENT_INSTANCE/ObjectName)[1]', 'NVARCHAR(256)'),
          EVENTDATA().value('(/EVENT_INSTANCE/TSQLCommand)[1]', 'NVARCHAR(MAX)'),
          SUSER_SNAME();
  END;
  ```
- [ ] Implement change data capture for audit trail
- [ ] Regular security review and penetration testing

---

## 3. Performance Checklist

### 3.1. Index Management

- [ ] Create clustered index on every table
- [ ] Create non-clustered indexes for foreign keys
- [ ] Create covering indexes for frequent queries
  ```sql
  CREATE INDEX IX_Orders_CustomerID_Covering
  ON Orders(CustomerID, OrderDate)
  INCLUDE (TotalAmount, Status);
  ```
- [ ] Use filtered indexes for subset queries
  ```sql
  CREATE INDEX IX_Orders_Active
  ON Orders(OrderDate)
  WHERE Status = 'Active';
  ```
- [ ] Implement index maintenance schedule
  ```sql
  -- Check fragmentation
  SELECT 
      OBJECT_NAME(i.object_id) AS TableName,
      i.name AS IndexName,
      ips.avg_fragmentation_in_percent
  FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'DETAILED') ips
  JOIN sys.indexes i ON ips.object_id = i.object_id AND ips.index_id = i.index_id
  WHERE ips.avg_fragmentation_in_percent > 5;
  ```
- [ ] Remove unused indexes
  ```sql
  SELECT 
      OBJECT_NAME(s.object_id) AS TableName,
      i.name AS IndexName,
      s.user_seeks, s.user_scans
  FROM sys.dm_db_index_usage_stats s
  JOIN sys.indexes i ON s.object_id = i.object_id AND s.index_id = i.index_id
  WHERE s.user_seeks = 0 AND s.user_scans = 0
    AND i.name NOT LIKE 'PK%';
  ```
- [ ] Update statistics regularly
  ```sql
  -- Update statistics with full scan
  EXEC sp_MSforeachtable 'UPDATE STATISTICS ? WITH FULLSCAN';
  ```

### 3.2. Query Performance

- [ ] Enable Query Store for all production databases
  ```sql
  ALTER DATABASE MyDB SET QUERY_STORE = ON;
  ALTER DATABASE MyDB SET QUERY_STORE (
      OPERATION_MODE = READ_WRITE,
      MAX_STORAGE_SIZE_MB = 1024,
      QUERY_CAPTURE_MODE = AUTO,
      WAIT_STATS_CAPTURE_MODE = ON
  );
  ```
- [ ] Review and optimize top resource-consuming queries
  ```sql
  SELECT TOP 20 
      qs.execution_count,
      qs.total_elapsed_time / 1000 AS total_elapsed_ms,
      qs.total_logical_reads,
      SUBSTRING(qt.text, 1, 500) AS query_text
  FROM sys.dm_exec_query_stats qs
  CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
  ORDER BY qs.total_elapsed_time DESC;
  ```
- [ ] Avoid SELECT * - specify columns explicitly
- [ ] Use appropriate JOIN types (avoid OR in WHERE)
- [ ] Implement parameterized queries
- [ ] Review execution plans regularly
  ```sql
  -- Find missing index suggestions
  SELECT 
      OBJECT_NAME(d.object_id) AS TableName,
      d.equality_columns, d.inequality_columns, d.included_columns,
      s.avg_user_impact, s.avg_total_user_cost
  FROM sys.dm_db_missing_index_groups g
  JOIN sys.dm_db_missing_index_details d ON g.index_handle = d.index_handle
  JOIN sys.dm_db_missing_index_group_stats s ON g.index_group_handle = s.group_handle
  ORDER BY s.avg_total_user_cost DESC;
  ```
- [ ] Monitor blocking and deadlocks
  ```sql
  -- Current blocking
  SELECT 
      blocked.session_id AS blocked_id,
      blocker.session_id AS blocker_id,
      blocked_txt.text AS blocked_sql,
      blocker_txt.text AS blocker_sql
  FROM sys.dm_exec_requests blocked
  JOIN sys.dm_exec_requests blocker ON blocked.blocking_session_id = blocker.session_id
  CROSS APPLY sys.dm_exec_sql_text(blocked.sql_handle) blocked_txt
  CROSS APPLY sys.dm_exec_sql_text(blocker.sql_handle) blocker_txt;
  ```

### 3.3. Memory Configuration

- [ ] Set max server memory appropriately
  ```sql
  -- Leave at least 4GB for OS
  EXEC sp_configure 'max server memory', 32768; -- 32GB for 64GB server
  ```
- [ ] Monitor memory pressure
  ```sql
  SELECT 
      object_name,
      counter_name,
      cntr_value / 1024.0 AS value_mb
  FROM sys.dm_os_performance_counters
  WHERE counter_name IN ('Total Server Memory (KB)', 
                         'Target Server Memory (KB)',
                         'Buffer cache hit ratio');
  ```
- [ ] Enable lock pages in memory (Windows)
  ```sql
  -- Windows: Grant Lock Pages in Memory privilege to SQL Service account
  -- Then configure:
  EXEC sp_configure 'locks', 0; -- Auto-configure
  ```
- [ ] Configure optimal buffer pool size

### 3.4. TempDB Optimization

- [ ] Create multiple data files (equal to CPU cores, max 8)
- [ ] Size files equally with same growth rate
- [ ] Remove autogrowth if possible
- [ ] Enable TF 1118 (SQL 2014 and earlier)
- [ ] Monitor tempdb usage
  ```sql
  SELECT 
      SUM(user_object_reserved_kb) AS user_objects_kb,
      SUM(internal_object_reserved_kb) AS internal_objects_kb,
      SUM(version_store_reserved_kb) AS version_store_kb
  FROM sys.dm_db_file_space_usage;
  ```

---

## 4. High Availability và Disaster Recovery

### 4.1. Backup Strategy

- [ ] Implement full backup schedule (daily minimum)
  ```sql
  BACKUP DATABASE MyDB 
  TO DISK = 'C:\Backups\MyDB_Full.bak'
  WITH COMPRESSION, CHECKSUM, STATS = 10;
  ```
- [ ] Implement differential backup (every 4-6 hours)
- [ ] Implement transaction log backup (every 15-30 minutes)
  ```sql
  BACKUP LOG MyDB 
  TO DISK = 'C:\Backups\MyDB_Log.trn'
  WITH COMPRESSION, CHECKSUM;
  ```
- [ ] Test backup restore regularly
  ```sql
  RESTORE VERIFYONLY FROM DISK = 'C:\Backups\MyDB_Full.bak'
  WITH CHECKSUM;
  
  RESTORE DATABASE MyDB_TestRestore
  FROM DISK = 'C:\Backups\MyDB_Full.bak'
  WITH MOVE 'MyDB_Data' TO 'C:\Restore\MyDB.mdf',
       MOVE 'MyDB_Log' TO 'C:\Restore\MyDB.ldf',
       RECOVERY;
  ```
- [ ] Store backups on separate location/drives
- [ ] Verify backup integrity with CHECKSUM
- [ ] Implement backup retention policy

### 4.2. High Availability Options

- [ ] Evaluate Always On Availability Groups for critical databases
  ```sql
  -- Check AG health
  SELECT 
      ag.name AS AGName,
      ar.replica_server_name,
      ar.availability_mode_desc,
      rs.synchronization_state_desc,
      rs.last_commit_time
  FROM sys.availability_groups ag
  JOIN sys.availability_replicas ar ON ag.group_id = ar.group_id
  JOIN sys.dm_hadr_database_replica_states rs ON ar.replica_id = rs.replica_id;
  ```
- [ ] Configure automatic backups on secondary replicas
- [ ] Implement read-only routing for scale-out
- [ ] Test failover procedures
- [ ] Document RPO and RTO objectives

### 4.3. Disaster Recovery Planning

- [ ] Document recovery procedures
- [ ] Test disaster recovery annually
- [ ] Maintain runbooks for common scenarios
- [ ] Implement geographic redundancy for critical data
- [ ] Document contact procedures for incidents

---

## 5. Maintenance Checklist

### 5.1. Regular Maintenance Tasks

- [ ] Index maintenance (rebuild/reorganize)
  ```sql
  -- Weekly index maintenance
  EXEC sp_IndexMaintenance; -- Custom procedure
  ```
- [ ] Statistics update
  ```sql
  -- Daily statistics update
  EXEC sp_MSforeachtable 'UPDATE STATISTICS ? WITH RESAMPLE';
  ```
- [ ] Consistency checks (DBCC CHECKDB)
  ```sql
  -- Weekly consistency check
  DBCC CHECKDB('MyDB') WITH NO_INFOMSGS;
  ```
- [ ] Log file management
  ```sql
  -- Monitor log usage
  SELECT 
      name,
      size * 8.0 / 1024 AS size_mb,
      (size - FILEPROPERTY(name, 'SpaceUsed')) * 8.0 / 1024 AS free_space_mb
  FROM sys.master_files
  WHERE type = 1;
  ```
- [ ] Clean up old data and logs
- [ ] Update SQL Server patches

### 5.2. Monitoring Setup

- [ ] Configure Database Mail for alerts
  ```sql
  EXEC sp_configure 'Database Mail XPs', 1;
  RECONFIGURE;
  
  -- Create operator
  EXEC msdb.dbo.sp_add_operator 
      @name = 'DBA Team',
      @email_address = 'dba-team@company.com';
  ```
- [ ] Set up SQL Agent jobs for monitoring
- [ ] Configure alerts for:
  - [ ] Severity 017-025 (media errors, hardware failures)
  - [ ] Blocking lasting > 30 seconds
  - [ ] Job failures
  - [ ] Disk space < 10%
  - [ ] Database corruption detected
- [ ] Implement baseline monitoring
  ```sql
  -- Capture baseline metrics
  INSERT INTO PerformanceBaseline
  SELECT 
      SYSDATETIME(),
      'BatchRequests' AS Metric,
      cntr_value AS Value
  FROM sys.dm_os_performance_counters
  WHERE counter_name = 'Batch Requests/sec';
  ```

### 5.3. SQL Server Agent Jobs

- [ ] Create job categories for organization
- [ ] Schedule maintenance jobs:
  - [ ] Index maintenance (weekly)
  - [ ] Statistics update (daily)
  - [ ] DBCC CHECKDB (weekly)
  - [ ] Backup verification (daily)
  - [ ] Log backup (every 15-30 min)
  - [ ] Full backup (daily)
- [ ] Set up job failure notifications
- [ ] Document all jobs and schedules
- [ ] Implement job history retention

---

## 6. Development Standards

### 6.1. Coding Standards

- [ ] Use stored procedures for data access (not ad-hoc SQL)
- [ ] Always use TRY-CATCH for error handling
  ```sql
  BEGIN TRY
      BEGIN TRANSACTION;
      -- operations
      COMMIT;
  END TRY
  BEGIN CATCH
      IF XACT_STATE() <> 0 ROLLBACK;
      -- log error
      THROW;
  END CATCH;
  ```
- [ ] Use SET NOCOUNT ON
- [ ] Use fully qualified object names
- [ ] Avoid SELECT * in production code
- [ ] Use appropriate data types
- [ ] Implement pagination for large result sets
  ```sql
  SELECT * FROM Products
  ORDER BY ProductID
  OFFSET 100 ROWS FETCH NEXT 50 ROWS ONLY;
  ```
- [ ] Use parameters for all user inputs
- [ ] Implement SET XACT_ABORT ON for critical procedures

### 6.2. Object Naming Conventions

- [ ] Use consistent naming:
  - [ ] Tables: PascalCase, singular (Customer, not Customers)
  - [ ] Columns: PascalCase (OrderDate, not order_date)
  - [ ] Stored Procedures: usp_<Entity>_<Action> (usp_Order_Create)
  - [ ] Functions: fn_<Name> (fn_CalculateTotal)
  - [ ] Indexes: IX_<Table>_<Columns> (IX_Order_CustomerID)
  - [ ] Views: vw_<Name> (vw_ActiveCustomers)
  - [ ] Triggers: trg_<Table>_<Event> (trg_Order_AfterUpdate)

### 6.3. Database Object Management

- [ ] Document all database objects
- [ ] Implement version control for schema changes
- [ ] Use migration scripts for deployments
- [ ] Review and approve schema changes
- [ ] Test changes in non-production environment

---

## 7. Capacity Planning

### 7.1. Storage Capacity

- [ ] Monitor disk space usage
  ```sql
  SELECT 
      DB_NAME(database_id) AS DatabaseName,
      type_desc,
      name AS FileName,
      size * 8.0 / 1024 AS SizeGB,
      FILEPROPERTY(name, 'SpaceUsed') * 8.0 / 1024 AS UsedGB,
      (size - FILEPROPERTY(name, 'SpaceUsed')) * 8.0 / 1024 AS FreeGB
  FROM sys.master_files
  WHERE type IN (0, 1)
  ORDER BY database_id, type;
  ```
- [ ] Project growth trends
- [ ] Plan for 6-12 months of growth
- [ ] Configure alerts for low disk space

### 7.2. Performance Capacity

- [ ] Monitor CPU usage trends
  ```sql
  SELECT 
      DATEADD(hh, DATEPART(hour, r.start_time), CAST(CAST(r.start_time AS DATE) AS DATETIME)) AS Hour,
      COUNT(*) AS BatchCount,
      SUM(r.cpu_time) / 1000 AS TotalCpuSeconds
  FROM sys.dm_exec_query_stats r
  WHERE r.start_time >= DATEADD(day, -7, GETDATE())
  GROUP BY DATEADD(hh, DATEPART(hour, r.start_time), CAST(CAST(r.start_time AS DATE) AS DATETIME))
  ORDER BY Hour;
  ```
- [ ] Monitor memory pressure
- [ ] Track query performance over time
- [ ] Plan for increased load

---

## 8. Compliance Checklist

### 8.1. Data Protection

- [ ] Classify data sensitivity levels
- [ ] Implement data masking for sensitive data
  ```sql
  -- Static data masking
  ALTER TABLE Customers 
  ADD EmailMasked AS CONCAT('****', SUBSTRING(Email, CHARINDEX('@', Email), LEN(Email)));
  
  -- Dynamic data masking
  CREATE TABLE SensitiveData (
      SSN VARCHAR(11) MASKED WITH (FUNCTION = 'partial(0,"XXX-XX-",4)') NULL,
      Email VARCHAR(100) MASKED WITH (FUNCTION = 'email()') NULL,
      Phone VARCHAR(20) MASKED WITH (FUNCTION = 'default()') NULL
  );
  ```
- [ ] Implement row-level security
  ```sql
  CREATE SECURITY POLICY SalesFilter
  ADD FILTER PREDICATE dbo.fn_FilterByRegion(UserRegion()) 
  ON dbo.Sales
  WITH (STATE = ON);
  ```
- [ ] Regular data privacy audits
- [ ] Document data retention policies

### 8.2. Audit Trails

- [ ] Track all data access
- [ ] Maintain change history
- [ ] Implement automated audit reporting
- [ ] Review audit logs regularly

---

## 9. Pre-Production Deployment

### 9.1. Testing Requirements

- [ ] Unit testing for stored procedures
- [ ] Integration testing with application
- [ ] Performance testing with production-like data
- [ ] Load testing for concurrent users
- [ ] Security penetration testing

### 9.2. Deployment Checklist

- [ ] Review execution plans
- [ ] Test in staging environment
- [ ] Document rollback procedures
- [ ] Plan maintenance window
- [ ] Notify stakeholders
- [ ] Have rollback plan ready
- [ ] Monitor post-deployment metrics

---

## 10. Daily Operations

### 10.1. Daily Checks

- [ ] Verify all backups completed successfully
- [ ] Check for blocking processes
- [ ] Review error logs
  ```sql
  EXEC sp_readerrorlog 0, 1, 'error';
  ```
- [ ] Monitor disk space
- [ ] Check job status
- [ ] Review alerts from overnight

### 10.2. Weekly Reviews

- [ ] Review performance metrics
- [ ] Check index fragmentation
- [ ] Review wait statistics
  ```sql
  SELECT TOP 10
      wait_type,
      waiting_tasks_count,
      wait_time_ms / 1000.0 AS wait_time_sec,
      signal_wait_time_ms / 1000.0 AS signal_wait_sec
  FROM sys.dm_os_wait_stats
  WHERE wait_time_ms > 1000
  ORDER BY wait_time_ms DESC;
  ```
- [ ] Review long-running queries
- [ ] Check database consistency

### 10.3. Monthly Reviews

- [ ] Capacity planning review
- [ ] Security audit
- [ ] Index usage analysis
- [ ] Query performance trends
- [ ] Backup restore testing
- [ ] Disaster recovery test

---

## 11. Documentation Requirements

### 11.1. Required Documentation

- [ ] Database architecture diagram
- [ ] Data dictionary
- [ ] Stored procedure documentation
- [ ] Backup and recovery procedures
- [ ] High availability configuration
- [ ] Security configuration
- [ ] Monitoring setup
- [ ] Contact list and escalation procedures

### 11.2. Change Documentation

- [ ] Document all schema changes
- [ ] Record performance tuning activities
- [ ] Update diagrams and documentation
- [ ] Maintain version history
