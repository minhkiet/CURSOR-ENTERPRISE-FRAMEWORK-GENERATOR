# PostgreSQL Checklist - Danh Sách Kiểm Tra

## Mục lục
1. [Project Setup](#1-project-setup)
2. [Schema Design](#2-schema-design)
3. [Indexing](#3-indexing)
4. [Query Optimization](#4-query-optimization)
5. [Performance Tuning](#5-performance-tuning)
6. [Security](#6-security)
7. [Backup & Recovery](#7-backup--recovery)
8. [Monitoring](#8-monitoring)

---

## 1. Project Setup

### Basic Configuration

- [ ] PostgreSQL version is recent (14+) for modern features
- [ ] `postgresql.conf` configured appropriately:
  - `max_connections` set correctly
  - `shared_buffers` = 25% of RAM
  - `effective_cache_size` = 75% of RAM
  - `work_mem` appropriate for operations
  - `maintenance_work_mem` for maintenance tasks
  - `wal_buffers` configured
  - `checkpoint_completion_target` = 0.9
  - `random_page_cost` adjusted for SSD
- [ ] `pg_hba.conf` configured for authentication
- [ ] Connection pooling configured (pgbouncer/pgpool)
- [ ] SSL/TLS enabled for connections

### Extensions

- [ ] `pgcrypto` installed for password hashing
- [ ] `uuid-ossp` or `pg_uuidv7` for UUID generation
- [ ] `pg_stat_statements` enabled for query analysis
- [ ] `pg_trgm` for fuzzy text search (if needed)
- [ ] `hstore` for key-value storage (if needed)
- [ ] `citext` for case-insensitive text (if needed)

---

## 2. Schema Design

### Table Design

- [ ] Tables use appropriate data types:
  - `VARCHAR(n)` not `CHAR(n)` for variable length
  - `DECIMAL` not `FLOAT`/`REAL` for monetary values
  - `TIMESTAMP WITH TIME ZONE` for timestamps
  - `BOOLEAN` not `INTEGER` for flags
- [ ] Primary keys are defined
- [ ] Foreign keys are implemented with appropriate constraints
- [ ] `NOT NULL` constraints used where applicable
- [ ] Default values specified for optional fields
- [ ] Audit columns present (`created_at`, `updated_at`)
- [ ] Soft delete pattern implemented where needed

### Naming Conventions

- [ ] Table names are plural (`users`, `orders`, `products`)
- [ ] Column names use snake_case
- [ ] Primary key columns named `id`
- [ ] Foreign key columns named `{table}_id`
- [ ] Indexes follow naming convention (`idx_{table}_{columns}`)
- [ ] Constraints named appropriately

### Data Integrity

- [ ] Check constraints for business rules
- [ ] Unique constraints for business keys
- [ ] Exclusion constraints for overlapping ranges (if needed)
- [ ] Domain types created for repeated constraints

---

## 3. Indexing

### Index Strategy

- [ ] Indexes created for foreign keys
- [ ] Indexes for WHERE clause columns in frequent queries
- [ ] Composite indexes for multi-column filters
- [ ] Partial indexes for common query patterns
- [ ] Expression indexes for computed values
- [ ] Covering indexes for read-heavy queries

### Index Maintenance

- [ ] Unused indexes identified and removed
- [ ] Index bloat monitored
- [ ] Index statistics are current (`ANALYZE` run)
- [ ] Duplicate indexes consolidated
- [ ] Low-selectivity indexes reconsidered

### Index Types

- [ ] B-tree indexes for equality and range queries
- [ ] Partial indexes for filtered queries
- [ ] BRIN indexes for time-series data
- [ ] GIN indexes for JSONB and full-text search
- [ ] Expression indexes for function calls

---

## 4. Query Optimization

### Query Analysis

- [ ] All critical queries analyzed with `EXPLAIN ANALYZE`
- [ ] Sequential scans on large tables investigated
- [ ] Index scans used for large table lookups
- [ ] Estimated vs actual row counts similar
- [ ] No implicit type conversions
- [ ] No functions on indexed columns without expression indexes

### Query Patterns

- [ ] `SELECT *` avoided in application code
- [ ] Specific columns selected
- [ ] Batch inserts used for bulk operations
- [ ] `INSERT ... ON CONFLICT` used for upserts
- [ ] `COPY` command for bulk loading
- [ ] Window functions used for analytics

### JOIN Optimization

- [ ] JOINs use appropriate columns (indexed)
- [ ] JOIN order is optimal
- [ ] Large tables on driving side
- [ ] Lateral joins used where appropriate
- [ ] Subqueries converted to JOINs or CTEs

---

## 5. Performance Tuning

### Memory Configuration

- [ ] `work_mem` configured per operation needs
- [ ] `maintenance_work_mem` adequate for maintenance
- [ ] `shared_buffers` sized appropriately
- [ ] `effective_cache_size` reflects available memory

### Table Maintenance

- [ ] VACUUM configured properly (autovacuum)
- [ ] Manual VACUUM scheduled for maintenance windows
- [ ] Table bloat monitored and addressed
- [ ] Statistics are current
- [ ] `pg_stat_user_tables` monitored

### Caching

- [ ] Frequently accessed data cached at application layer
- [ ] Materialized views for expensive aggregations
- [ ] Prepared statements used for repeated queries
- [ ] Connection pooling implemented

### Partitioning

- [ ] Large tables partitioned by date or range
- [ ] Partition pruning enabled
- [ ] Indexes on partition key
- [ ] Partition maintenance automated

---

## 6. Security

### Authentication

- [ ] Strong passwords for all roles
- [ ] SCRAM-SHA-256 password encryption
- [ ] `pg_hba.conf` authentication methods appropriate
- [ ] No trust authentication in production
- [ ] LDAP/SSO integration (if needed)

### Authorization

- [ ] Principle of least privilege applied
- [ ] Application uses limited-privilege role
- [ ] `PUBLIC` privileges revoked
- [ ] Row-Level Security implemented for multi-tenant
- [ ] Separate read/write roles (if applicable)

### Data Protection

- [ ] Passwords hashed with `crypt()` or `pgcrypto`
- [ ] Sensitive data encrypted at rest
- [ ] Sensitive data encrypted in transit (SSL/TLS)
- [ ] Audit logging enabled
- [ ] PII columns identified and protected

### SQL Injection

- [ ] Parameterized queries used everywhere
- [ ] No dynamic SQL with user input
- [ ] Input validation at application layer
- [ ] SQL errors don't expose internals

---

## 7. Backup & Recovery

### Backup Strategy

- [ ] Automated full backups configured
- [ ] WAL archiving enabled
- [ ] Point-in-time recovery possible
- [ ] Backup retention policy defined
- [ ] Backups tested by restoring to test environment

### Backup Types

- [ ] `pg_basebackup` for full backups
- [ ] Continuous archiving for WAL
- [ ] Per-table logical backups (if needed)
- [ ] Cloud storage for backup redundancy

### Recovery Testing

- [ ] Recovery procedure documented
- [ ] Regular recovery tests performed
- [ ] Recovery time objective (RTO) documented
- [ ] Recovery point objective (RPO) documented

---

## 8. Monitoring

### Performance Monitoring

- [ ] `pg_stat_statements` enabled and monitored
- [ ] Slow query log enabled
- [ ] Connection count monitored
- [ ] Cache hit ratio monitored
- [ ] Lock wait times monitored

### Health Monitoring

- [ ] Database uptime monitored
- [ ] Replication lag monitored (if applicable)
- [ ] Disk space monitored
- [ ] Transaction ID age monitored
- [ ] Autovacuum activity monitored

### Alerting

- [ ] Alerts configured for:
  - High connection count
  - Replication lag
  - Disk space low
  - Long-running queries
  - Failed queries
  - Lock waits
  - Transaction ID wraparound

### Logging

- [ ] Appropriate log level configured
- [ ] Log destination configured
- [ ] Log rotation configured
- [ ] Slow queries logged
- [ ] Errors logged and monitored

---

## Summary Checklist

### Pre-Deployment

- [ ] All queries analyzed with EXPLAIN ANALYZE
- [ ] Indexes created and tested
- [ ] Security reviewed and hardened
- [ ] Backup and recovery tested
- [ ] Monitoring and alerting configured
- [ ] Documentation complete

### Post-Deployment

- [ ] Baseline performance established
- [ ] Monitoring active and reviewed
- [ ] Regular maintenance scheduled
- [ ] Team trained on PostgreSQL operations
- [ ] Runbook documented

---

## Liên kết liên quan
- [PostgreSQL Glossary](./glossary.md)
- [PostgreSQL Architecture](./architecture.md)
- [PostgreSQL Best Practices](./best-practice.md)
- [PostgreSQL Anti-Patterns](./anti-pattern.md)
- [PostgreSQL FAQ](./faq.md)
- [PostgreSQL Decision Tree](./decision-tree.md)
