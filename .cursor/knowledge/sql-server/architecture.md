# SQL Server Architecture - Kiến Trúc SQL Server

## Tổng quan

SQL Server là enterprise database platform từ Microsoft. Kiến trúc bao gồm storage engine, query optimizer, transaction manager.

## Kiến trúc chi tiết

### 1. Storage Engine

- **Buffer Pool**: Cache data pages
- **Transaction Log**: Write-ahead logging
- **Data Files**: .mdf, .ndf
- **Log Files**: .ldf

### 2. Query Processing

- **Parser**: Syntax validation
- **Optimizer**: create execution plan
- **Executor**: run plan

### 3. High Availability

- **Always On AG**: HA/DR solution
- **Failover Clustering**: Windows failover
- **Log Shipping**: DR solution
- **Replication**: Data distribution

## Kết luận

SQL Server cung cấp enterprise database solution.
