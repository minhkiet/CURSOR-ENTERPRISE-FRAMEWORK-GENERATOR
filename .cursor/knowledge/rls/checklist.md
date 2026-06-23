---
title: "RLS Security Checklist"
description: "Danh sách kiểm tra bảo mật toàn diện cho việc triển khai Row Level Security"
tags: ["rls", "postgres", "security", "checklist", "database", "deployment"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# RLS Security Checklist - Danh Sách Kiểm Tra Bảo Mật

## Overview

Security checklist là công cụ không thể thiếu trong quá trình triển khai RLS. Việc có một checklist chuẩn giúp đảm bảo không bỏ sót bất kỳ bước quan trọng nào và giảm thiểu rủi ro bảo mật trước khi deploy lên production. Tài liệu này cung cấp một comprehensive checklist được tổ chức theo các phases của development lifecycle.

Checklist được thiết kế để sử dụng bởi developers, security engineers, và DevOps teams. Mỗi item bao gồm mô tả, lý do tại sao nó quan trọng, và cách verify. Các items được đánh dấu priority để bạn có thể tập trung vào những items quan trọng nhất trước.

## Purpose

Mục tiêu của checklist này là cung cấp một systematic approach để verify RLS implementation trước khi deployment. Sử dụng checklist này giúp đảm bảo consistency across deployments, reduce human error, và provide documentation cho audit purposes. Checklist cũng serves as a training tool cho new team members hiểu về RLS security requirements.

## Key Concepts

### Priority Levels

**P0 - Critical**: Những items phải hoàn thành trước khi deploy. Failure có thể dẫn đến immediate security breach.

**P1 - High**: Những items quan trọng phải hoàn thành trước production. Failure có thể dẫn đến security vulnerabilities.

**P2 - Medium**: Những items nên hoàn thành trước production. Failure có thể dẫn đến operational issues.

**P3 - Low**: Những items nice-to-have. Failure có thể gây ra minor inconveniences.

### Verification Methods

**Automated**: Items có thể verify bằng automated tests hoặc scripts.

**Manual**: Items cần manual review hoặc inspection.

**Review**: Items cần peer review hoặc security team review.

## Pre-Implementation Phase

### Requirements Analysis

- [ ] **P0** Xác định tất cả tables cần RLS protection
  - Verify: List all tables với sensitive data
  - Documentation: Complete data classification

- [ ] **P0** Xác định access control requirements cho mỗi table
  - Verify: Document allowed operations per role
  - Documentation: Access matrix

- [ ] **P1** Xác định ownership model (user-owned, tenant-owned, public)
  - Verify: Document ownership hierarchy
  - Documentation: Schema với owner columns

- [ ] **P1** Xác định role hierarchy
  - Verify: Role definitions and relationships
  - Documentation: Role hierarchy diagram

- [ ] **P2** Review compliance requirements (GDPR, SOC2, HIPAA, etc.)
  - Verify: Compliance checklist
  - Documentation: Compliance mapping

- [ ] **P2** Xác định audit requirements
  - Verify: Audit log specifications
  - Documentation: Audit data retention policy

### Architecture Review

- [ ] **P0** Review RLS architecture với security team
  - Review: Architecture design document
  - Sign-off: Security team approval

- [ ] **P1** Review multi-tenant isolation design
  - Review: Tenant isolation diagram
  - Testing: Cross-tenant access tests

- [ ] **P1** Review helper function design
  - Review: Function signatures và logic
  - Documentation: Function API documentation

- [ ] **P2** Review performance impact assessment
  - Review: Expected query patterns
  - Documentation: Performance test plan

## Implementation Phase

### Schema Design

- [ ] **P0** Thêm owner columns (user_id, tenant_id) vào tất cả relevant tables
  - Verify: `SELECT column_name FROM information_schema.columns WHERE table_name = 'your_table'`
  - SQL: `ALTER TABLE orders ADD COLUMN customer_id UUID REFERENCES auth.users(id)`

- [ ] **P0** Tạo indexes cho RLS policy columns
  - Verify: `SELECT indexname FROM pg_indexes WHERE tablename = 'your_table'`
  - SQL: `CREATE INDEX idx_orders_customer ON orders(customer_id)`

- [ ] **P1** Thêm soft delete columns (deleted_at)
  - Verify: Column exists với proper type
  - Migration: Add column với DEFAULT NULL

- [ ] **P1** Thêm audit columns (created_by, updated_by)
  - Verify: Columns exist và populated
  - Trigger: Audit trigger setup

### RLS Configuration

- [ ] **P0** Enable RLS on all sensitive tables
  - Verify: `SELECT relrowsecurity FROM pg_class WHERE relname = 'your_table'`
  - SQL: `ALTER TABLE your_table ENABLE ROW LEVEL SECURITY`

- [ ] **P0** Enable FORCE ROW LEVEL SECURITY
  - Verify: `SELECT relforcerowsecurity FROM pg_class WHERE relname = 'your_table'`
  - SQL: `ALTER TABLE your_table FORCE ROW LEVEL SECURITY`

- [ ] **P0** Create policies cho ALL operations (SELECT, INSERT, UPDATE, DELETE)
  - Verify: `SELECT * FROM pg_policies WHERE tablename = 'your_table'`
  - Coverage: Minimum 1 policy per operation

- [ ] **P1** Implement WITH CHECK policies cho INSERT và UPDATE
  - Verify: WITH CHECK clause present
  - Testing: Attempt invalid data insertion

### Policy Design

- [ ] **P0** Ensure policies use auth.uid() for user identification
  - Verify: Policy contains `auth.uid()`
  - Review: Manual code review

- [ ] **P0** Ensure policies handle NULL auth.uid()
  - Verify: Policy has `auth.uid() IS NOT NULL` check
  - Testing: Test với anonymous access

- [ ] **P0** Ensure policies enforce ownership checks
  - Verify: Policy compares owner_id với auth.uid()
  - Testing: Test cross-user access denial

- [ ] **P1** Implement role-based access in policies
  - Verify: Admin bypass exists và working
  - Testing: Test admin vs regular user access

- [ ] **P1** Document all policies với comments
  - Verify: All policies have documentation
  - Review: Documentation review

- [ ] **P2** Use consistent naming convention
  - Verify: Policy names follow pattern
  - Review: Naming convention document

### Security Configuration

- [ ] **P0** Revoke all PUBLIC grants on schema
  - Verify: `SELECT * FROM information_schema.table_privileges WHERE grantee = 'PUBLIC'`
  - SQL: `REVOKE ALL ON SCHEMA public FROM PUBLIC`

- [ ] **P0** Grant only necessary permissions to roles
  - Verify: Minimal privileges principle
  - Review: Permission audit

- [ ] **P1** Configure connection pooling restrictions
  - Verify: Pool size limits
  - Review: Connection pool config

- [ ] **P1** Implement rate limiting
  - Verify: Rate limit configuration
  - Testing: Load testing

### Helper Functions

- [ ] **P1** Create is_admin() helper function
  - Verify: Function exists và working
  - Testing: Test với admin và non-admin users

- [ ] **P1** Create tenant context functions
  - Verify: Functions set và get context
  - Testing: Test tenant isolation

- [ ] **P2** Document all helper functions
  - Verify: Function documentation
  - Review: API documentation

## Testing Phase

### Unit Testing

- [ ] **P0** Test ownership policies (user can access own data)
  - SQL: `SET ROLE authenticated; SET LOCAL request.jwt.claims = '{"sub":"user-1"}'; SELECT * FROM orders;`
  - Expected: Returns only user's orders

- [ ] **P0** Test ownership policies (user cannot access other's data)
  - SQL: `SET ROLE authenticated; SET LOCAL request.jwt.claims = '{"sub":"user-1"}'; SELECT * FROM orders WHERE customer_id = 'user-2';`
  - Expected: Returns empty result

- [ ] **P0** Test admin bypass policies
  - SQL: `SET ROLE authenticated; SET LOCAL request.jwt.claims = '{"sub":"admin-1","app_metadata":{"role":"admin"}}'; SELECT * FROM orders;`
  - Expected: Returns all orders

- [ ] **P1** Test NULL auth.uid() handling
  - SQL: `RESET ROLE; SELECT * FROM orders;`
  - Expected: Returns empty result (denied)

- [ ] **P1** Test INSERT policies
  - SQL: `SET ROLE authenticated; SET LOCAL request.jwt.claims = '{"sub":"user-1"}'; INSERT INTO orders (customer_id) VALUES ('user-1');`
  - Expected: Success

- [ ] **P1** Test UPDATE policies
  - SQL: `SET ROLE authenticated; SET LOCAL request.jwt.claims = '{"sub":"user-1"}'; UPDATE orders SET total = 100 WHERE customer_id = 'user-1';`
  - Expected: Success

- [ ] **P1** Test DELETE policies
  - SQL: `SET ROLE authenticated; SET LOCAL request.jwt.claims = '{"sub":"user-1"}'; DELETE FROM orders WHERE customer_id = 'user-1';`
  - Expected: Success based on policy

### Integration Testing

- [ ] **P0** Test complete user flows với RLS
  - Testing: End-to-end user journeys
  - Coverage: All critical user paths

- [ ] **P0** Test multi-tenant isolation
  - Testing: Cross-tenant access attempts
  - Coverage: All tenant-scoped tables

- [ ] **P1** Test role transitions
  - Testing: Permission changes
  - Verification: Immediate effect

- [ ] **P1** Test concurrent access
  - Testing: Multiple users simultaneously
  - Verification: No data leaks

### Performance Testing

- [ ] **P1** Measure query performance impact với RLS
  - Testing: Compare query times before/after
  - Threshold: < 10% degradation acceptable

- [ ] **P1** Load test with RLS policies
  - Testing: High concurrency scenarios
  - Monitoring: CPU, memory, query times

- [ ] **P2** Profile complex policies
  - Testing: EXPLAIN ANALYZE on critical queries
  - Optimization: Address bottlenecks

### Security Testing

- [ ] **P0** Test SQL injection with RLS
  - Testing: Attempt common injection patterns
  - Verification: All blocked by RLS

- [ ] **P0** Test direct database access bypass attempts
  - Testing: Admin/superuser access attempts
  - Verification: All blocked by FORCE ROW LEVEL SECURITY

- [ ] **P0** Test anonymous access attempts
  - Testing: Unauthenticated requests
  - Verification: All denied

- [ ] **P1** Test privilege escalation attempts
  - Testing: JWT manipulation attempts
  - Verification: All blocked

- [ ] **P1** Test rate limiting bypass attempts
  - Testing: Rapid request patterns
  - Verification: Proper throttling

## Pre-Deployment Phase

### Code Review

- [ ] **P0** Security team review of all policies
  - Review: Complete policy code review
  - Sign-off: Security team approval

- [ ] **P0** Peer review of all SQL migrations
  - Review: Two-person review rule
  - Sign-off: Peer approval

- [ ] **P1** Documentation review
  - Review: All policies documented
  - Completeness: Every policy has comments

### Environment Verification

- [ ] **P0** Test in staging environment matching production
  - Verification: Identical configuration
  - Duration: Minimum 1 week soak test

- [ ] **P0** Verify RLS enabled in staging
  - Verification: `SELECT relrowsecurity FROM pg_class`
  - Environment: Staging

- [ ] **P1** Verify all indexes created
  - Verification: Compare with production indexes
  - Optimization: Matching configuration

- [ ] **P2** Verify monitoring/alerting configured
  - Verification: Alert rules active
  - Testing: Test alert delivery

### Rollback Plan

- [ ] **P0** Document rollback procedures
  - Documentation: Step-by-step instructions
  - Review: Tested by operations team

- [ ] **P0** Create rollback migration scripts
  - Scripts: Ready to execute
  - Testing: Verified in staging

- [ ] **P1** Define rollback triggers/conditions
  - Documentation: Clear criteria
  - Communication: Team notified

### Communication Plan

- [ ] **P1** Notify stakeholders of RLS changes
  - Communication: Email/chat message
  - Timing: Before deployment

- [ ] **P1** Document known breaking changes
  - Documentation: Change log
  - Communication: Developer notification

- [ ] **P2** Prepare user communication (if needed)
  - Communication: User-facing notices
  - Channels: App notification, email

## Deployment Phase

### Deployment Checklist

- [ ] **P0** Deploy during low-traffic window
  - Timing: Off-peak hours
  - Window: Minimum 4 hours for rollback

- [ ] **P0** Enable pg_stat_statements for monitoring
  - Verification: Extension loaded
  - Configuration: Proper retention

- [ ] **P0** Monitor error logs continuously
  - Monitoring: Real-time log watching
  - Alert: Immediate notification

- [ ] **P0** Have DBA on standby
  - Resource: DBA available
  - Escalation: Clear path

- [ ] **P1** Monitor query performance
  - Monitoring: Slow query log
  - Threshold: Define and alert

- [ ] **P1** Monitor application errors
  - Monitoring: Error tracking
  - Response: Defined SLAs

### Post-Deployment Verification

- [ ] **P0** Verify RLS policies active in production
  - Verification: Query pg_policies
  - Confirmation: All policies present

- [ ] **P0** Run smoke tests
  - Testing: Core functionality
  - Coverage: Critical user flows

- [ ] **P0** Verify no new errors in logs
  - Verification: Error rate normal
  - Alert: Immediate investigation

- [ ] **P1** Run full test suite
  - Testing: Complete test coverage
  - Results: All pass

- [ ] **P1** Verify performance metrics
  - Metrics: Query times, throughput
  - Comparison: Baseline established

- [ ] **P2** Update documentation
  - Documentation: Final architecture docs
  - Version: New version tagged

## Ongoing Maintenance

### Regular Audits

- [ ] **P1** Monthly policy review
  - Review: All policies reviewed
  - Documentation: Updates logged

- [ ] **P1** Quarterly security audit
  - Audit: External/internal review
  - Reporting: Findings documented

- [ ] **P2** Annual compliance review
  - Review: GDPR, SOC2, etc.
  - Certification: Updated if needed

### Monitoring

- [ ] **P0** Monitor failed authentication attempts
  - Alert: Multiple failures trigger alert
  - Response: Security investigation

- [ ] **P0** Monitor query performance trends
  - Alert: Degradation detected
  - Investigation: Root cause analysis

- [ ] **P1** Monitor unusual access patterns
  - Alert: Anomaly detection
  - Investigation: Potential threat

- [ ] **P1** Monitor policy changes
  - Alert: Unauthorized changes
  - Audit: Change logging

### Updates and Changes

- [ ] **P0** Review RLS before adding new tables
  - Process: Security review required
  - Documentation: Access matrix updated

- [ ] **P0** Review RLS before modifying access patterns
  - Process: Impact assessment
  - Testing: Full regression

- [ ] **P1** Update documentation with changes
  - Process: Change documentation
  - Version: Semantic versioning

## Compliance Checklist

### GDPR Compliance

- [ ] **P0** Data access documented
  - Documentation: All access points
  - Review: Legal team approval

- [ ] **P0** Right to deletion implemented
  - Implementation: Cascade policies
  - Testing: Deletion verification

- [ ] **P0** Data portability supported
  - Implementation: Export functionality
  - Testing: Export verification

### SOC2 Compliance

- [ ] **P0** Access controls documented
  - Documentation: Complete access matrix
  - Review: Auditor review

- [ ] **P1** Audit logging implemented
  - Implementation: Comprehensive logs
  - Retention: Per compliance requirements

- [ ] **P1** Change management process
  - Process: Documented procedures
  - Review: Annual review

### HIPAA Compliance (if applicable)

- [ ] **P0** PHI access controls implemented
  - Implementation: Role-based access
  - Testing: Access verification

- [ ] **P0** Audit trail for PHI access
  - Implementation: Comprehensive logging
  - Retention: 6 years minimum

- [ ] **P0** Minimum necessary access
  - Implementation: Principle of least privilege
  - Verification: Access review

## Emergency Procedures

### Incident Response

- [ ] **P0** Document security incident procedures
  - Documentation: Response playbooks
  - Training: Team trained

- [ ] **P0** Define RLS bypass procedures
  - Documentation: Emergency access only
  - Approval: C-level authorization

- [ ] **P1** Test incident response quarterly
  - Testing: Tabletop exercises
  - Documentation: Lessons learned

### Quick Disable Procedures

- [ ] **P0** Document quick disable procedure
  - Documentation: Step-by-step
  - Testing: Verified working

- [ ] **P0** Maintain disable scripts
  - Scripts: Tested and working
  - Storage: Secure location

## Quick Reference

### Pre-Deployment Quick Checklist

```
□ RLS enabled on all tables
□ FORCE ROW LEVEL SECURITY set
□ Policies for all operations exist
□ NULL auth.uid() handled
□ Indexes created for policy columns
□ Helper functions tested
□ All PUBLIC grants revoked
□ Staging tests passed
□ Security review completed
□ Rollback plan prepared
□ Monitoring active
□ DBA on standby
```

### Common Verification Queries

```sql
-- Check RLS status
SELECT relname, relrowsecurity, relforcerowsecurity
FROM pg_class
WHERE relnamespace = 'public'::regnamespace
AND relkind = 'r';

-- List all policies
SELECT policyname, tablename, cmd, permissive
FROM pg_policies
WHERE schemaname = 'public';

-- Check indexes
SELECT indexname, tablename
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- Verify PUBLIC grants
SELECT * FROM information_schema.table_privileges
WHERE grantee = 'PUBLIC'
AND table_schema = 'public';

-- Check helper functions
SELECT proname, prosrc
FROM pg_proc
WHERE pronamespace = 'public'::regnamespace
AND prokind = 'f';
```

## Sign-Off

### Pre-Deployment Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| Security Review | | | |
| DBA | | | |
| Product Owner | | | |
| Compliance | | | |

### Post-Deployment Verification

| Check | Date | Result | Verified By |
|-------|------|--------|-------------|
| Policies Active | | | |
| Smoke Tests Pass | | | |
| No New Errors | | | |
| Performance OK | | | |

## References

- [PostgreSQL Row Level Security Documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [Supabase RLS Guidelines](https://supabase.com/docs/guides/auth/row-level-security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Cursor Enterprise Framework Security Rules](../rules/security.md)
- [Cursor Enterprise Framework Deployment Rules](../rules/deployment.md)
