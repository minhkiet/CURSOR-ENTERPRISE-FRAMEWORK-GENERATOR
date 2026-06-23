# SQL Server Decision Tree - Cây Quyết Định

## Quyết định về Index

### Câu hỏi: Index strategy nào?

- **Clustered**: Primary ordering
- **Non-clustered**: Additional lookups
- **Columnstore**: Analytics

## Quyết định về HA

### Câu hỏi: HA solution nào?

- **Always On AG**: Full HA/DR
- **Failover Cluster**: Shared storage
- **Log Shipping**: DR only

## Summary

SQL Server + Always On là enterprise approach.
