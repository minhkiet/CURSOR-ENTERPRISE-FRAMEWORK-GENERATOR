# SQL Server Glossary - Từ Điển Thuật Ngữ SQL Server

## Giới thiệu

Tài liệu này cung cấp các thuật ngữ chuyên ngành SQL Server.

## Các thuật ngữ cơ bản

### 1. T-SQL

T-SQL (Transact-SQL) là extension của SQL cho SQL Server. Thêm programming features: variables, loops, procedures. Stored procedures, triggers, functions.

### 2. Execution Plan

Execution Plan là roadmap của query execution. Show how optimizer executes query. Sử dụng SSMS hoặc SET SHOWPLAN.

### 3. Indexes

B-tree indexes (default). Clustered (data stored in order). Non-clustered (separate structure). Columnstore for analytics.

### 4. Stored Procedures

Stored Procedures là precompiled SQL batches. Improve performance, security. Parameters, return values.

### 5. Triggers

Triggers là automatically executed code on DML events. INSERT, UPDATE, DELETE triggers. DDL triggers for schema changes.

### 6. Views

Views là virtual tables. Simplify complex queries. Materialized views (indexed views) stored physically.

### 7. Transactions

BEGIN TRANSACTION, COMMIT, ROLLBACK. ACID properties. Isolation levels.

### 8. Isolation Levels

READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE, SNAPSHOT.

### 9. Deadlocks

Deadlock là circular wait for resources. SQL Server auto-detects và terminates one. Minimizing through proper design.

### 10. Always On

Always On Availability Groups cho HA và DR. Automatic failover. Read-scale out.

## Kết luận

Từ điển này cung cấp nền tảng về SQL Server.
