# MySQL Checklist - Danh Sách Kiểm Tra

## Mục lục
1. [Schema Design](#1-schema-design)
2. [Indexing](#2-indexing)
3. [Query Optimization](#3-query-optimization)
4. [Security](#4-security)
5. [Backup & Recovery](#5-backup--recovery)
6. [Monitoring](#6-monitoring)

---

## 1. Schema Design

### 1.1 Data Types

- [ ] Use appropriate data types (not VARCHAR for everything)
- [ ] Use ENUM for fixed sets of values
- [ ] Use DECIMAL for monetary values
- [ ] Use appropriate string lengths (not max possible)
- [ ] Use DATETIME vs TIMESTAMP appropriately
- [ ] Consider JSON type for semi-structured data

### 1.2 Constraints

- [ ] Primary keys defined for all tables
- [ ] Foreign keys with appropriate actions (CASCADE, RESTRICT)
- [ ] NOT NULL constraints where appropriate
- [ ] UNIQUE constraints for columns requiring uniqueness
- [ ] CHECK constraints for data validation (MySQL 8.0+)

### 1.3 Audit & Metadata

- [ ] created_at/updated_at columns
- [ ] deleted_at for soft delete
- [ ] created_by/updated_by for audit trail
- [ ] Version column for optimistic locking

---

## 2. Indexing

### 2.1 Index Creation

- [ ] Index foreign key columns
- [ ] Index columns in WHERE clauses
- [ ] Index columns in ORDER BY clauses
- [ ] Index columns in JOIN conditions
- [ ] Create composite indexes for multi-column queries
- [ ] Place equality columns before range columns in composite index

### 2.2 Index Maintenance

- [ ] Remove unused indexes
- [ ] Monitor index cardinality
- [ ] Consider covering indexes for frequent queries
- [ ] Use partial indexes for selective data (MySQL 8.0+)

### 2.3 Full-Text Search

- [ ] Use FULLTEXT index for text search
- [ ] Choose appropriate search mode (BOOLEAN, NATURAL LANGUAGE)
- [ ] Consider external search engine for complex search

---

## 3. Query Optimization

### 3.1 Query Writing

- [ ] Avoid SELECT *
- [ ] Use appropriate JOIN type (INNER vs LEFT vs RIGHT)
- [ ] Use UNION instead of OR where possible
- [ ] Avoid functions on indexed columns
- [ ] Use appropriate comparison operators
- [ ] Use LIMIT for pagination

### 3.2 Query Analysis

- [ ] Use EXPLAIN to analyze queries
- [ ] Use EXPLAIN ANALYZE in MySQL 8.0+
- [ ] Check for full table scans
- [ ] Verify index usage
- [ ] Monitor slow query log

### 3.3 Query Patterns

- [ ] Use parameterized queries (prevent SQL injection)
- [ ] Batch operations when possible
- [ ] Use transactions for multi-statement operations
- [ ] Avoid long transactions

---

## 4. Security

### 4.1 Access Control

- [ ] Use strong passwords
- [ ] Follow principle of least privilege
- [ ] Separate application users from admin users
- [ ] Use SSL/TLS for connections
- [ ] Rotate credentials regularly

### 4.2 User Management

- [ ] No root access from remote hosts
- [ ] Host-specific users (% vs localhost)
- [ ] Regular privilege audit
- [ ] Revoke unnecessary privileges

### 4.3 Data Protection

- [ ] Encrypt sensitive columns
- [ ] Use SSL for data in transit
- [ ] Implement row-level security (application-level)
- [ ] Mask sensitive data in logs

---

## 5. Backup & Recovery

### 5.1 Backup Strategy

- [ ] Regular full backups
- [ ] Incremental backups (binlog)
- [ ] Off-site backup storage
- [ ] Backup verification process

### 5.2 Recovery

- [ ] Documented recovery procedures
- [ ] Regular recovery testing
- [ ] Point-in-time recovery capability
- [ ] Recovery time objectives (RTO) documented

### 5.3 Tools

- [ ] mysqldump for logical backups
- [ ] MySQL Enterprise Backup for large databases
- [ ] Point-in-time recovery with binlog

---

## 6. Monitoring

### 6.1 Performance Monitoring

- [ ] Monitor slow query log
- [ ] Track query execution times
- [ ] Monitor connection pool usage
- [ ] Track buffer pool hit ratio
- [ ] Monitor replication lag

### 6.2 Capacity Planning

- [ ] Monitor disk usage
- [ ] Monitor table sizes
- [ ] Plan for growth
- [ ] Monitor memory usage

### 6.3 Health Checks

- [ ] Connection availability
- [ ] Replication status
- [ ] Disk space
- [ ] InnoDB status

---

## Quick Reference

### Schema Checklist
```
[ ] Primary key defined
[ ] Appropriate data types
[ ] Foreign keys enforced
[ ] Audit columns
[ ] Not over-normalized
```

### Index Checklist
```
[ ] Foreign keys indexed
[ ] WHERE columns indexed
[ ] High-cardinality columns preferred
[ ] No redundant indexes
[ ] Covering indexes for critical queries
```

### Query Checklist
```
[ ] No SELECT *
[ ] EXPLAIN analyzed
[ ] No functions on indexed columns
[ ] Parameterized queries
[ ] Appropriate pagination
```

---

## Liên kết liên quan
- [MySQL Glossary](./glossary.md)
- [MySQL Architecture](./architecture.md)
- [MySQL Best Practices](./best-practice.md)
- [MySQL Anti-Patterns](./anti-pattern.md)
- [MySQL FAQ](./faq.md)
- [MySQL Decision Tree](./decision-tree.md)
