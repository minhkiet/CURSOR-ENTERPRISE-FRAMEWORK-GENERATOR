# SQL Server FAQ - Câu Hỏi Thường Gặp

## Câu Hỏi Cơ Bản

### 1. SQL Server là gì?

SQL Server là enterprise relational database platform từ Microsoft. Hỗ trợ T-SQL, stored procedures, triggers, replication, high availability.

### 2. Clustered vs Non-clustered Index?

Clustered index sorts data physically. One per table. Non-clustered is separate structure. Multiple per table.

### 3. Always On là gì?

Always On Availability Groups cung cấp HA và DR. Automatic failover, readable replicas.

## Câu Hỏi Kỹ Thuật

### 4. Deadlock xử lý như thế nào?

SQL Server auto-detects deadlocks, terminates one process. MINIMIZE deadlocks through proper design.

### 5. Performance tuning?

Use execution plans, indexes, proper joins, statistics updates.
