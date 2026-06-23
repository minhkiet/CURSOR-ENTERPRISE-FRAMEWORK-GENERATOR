---
title: "Supabase Pre-Deployment Checklist"
description: "Danh sách kiểm tra toàn diện trước khi deploy Supabase project lên production"
tags: ["supabase", "deployment", "security", "checklist", "production", "pre-deployment"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Supabase Pre-Deployment Checklist

## Overview

Deploying một Supabase application lên production đòi hỏi systematic approach để đảm bảo security, performance, và reliability. Checklist này cung cấp comprehensive guide cho developers và DevOps teams để verify mọi aspects của Supabase deployment trước khi go live.

Production deployments khác với development environments ở nhiều khía cạnh quan trọng. Security requirements cao hơn, performance expectations lớn hơn, và reliability expectations nghiêm ngặt hơn. A single oversight có thể dẫn đến security breaches, data loss, hoặc service disruptions.

This checklist được organized thành logical sections, từ initial setup đến final deployment verification. Mỗi item bao gồm verification steps và expected outcomes để ensure nothing is missed.

## Purpose

Mục đích chính của checklist này là:

1. **Ensure Complete Security Coverage**: Verify tất cả security measures được implemented đúng cách
2. **Prevent Common Deployment Issues**: Catch potential problems trước khi production deployment
3. **Standardize Deployment Process**: Provide consistent deployment procedure cho team
4. **Reduce Post-Deployment Incidents**: Minimize production issues thông qua thorough pre-deployment checks
5. **Enable Audit Compliance**: Document security và compliance measures cho audit purposes

The checklist covers multiple deployment stages: Database Configuration, Authentication, Storage, Edge Functions, API Configuration, Monitoring và Logging, và Final Verification.

## Key Concepts

### Security Layers in Supabase

Supabase security được implement qua multiple layers, mỗi layer cần được configured và verified independently:

**Database Layer**: Row Level Security (RLS) policies control data access at the row level. Each table requires appropriate policies for SELECT, INSERT, UPDATE, và DELETE operations.

**Authentication Layer**: User authentication được managed qua Supabase Auth, với JWT tokens used for API authentication. Token validation và session management cần được properly configured.

**Storage Layer**: File storage có separate access policies. Buckets có thể be public hoặc private, với signed URLs cho secure access to private files.

**API Layer**: API endpoints được protected via API keys (anon vs service role) và optional additional validation layers.

**Edge Functions Layer**: Serverless functions chạy với specific permissions, cần properly validate authentication tokens.

### Deployment Environments

Understanding the distinction between deployment environments là critical:

**Development Environment**: Used for active development. Relaxed security acceptable for testing. May have verbose logging. Connection pooling minimal.

**Staging Environment**: Mirror of production. Should have same configuration as production. Used for final testing before deployment.

**Production Environment**: Live environment serving end users. Strict security required. Performance optimized. Comprehensive monitoring active.

## Pre-Deployment Verification

### 1. Database Configuration

#### Schema Design Verification

**Table Structure Review**:
- [ ] All tables have appropriate primary keys (UUID recommended)
- [ ] Foreign key relationships are properly defined with CASCADE deletes where appropriate
- [ ] Indexes exist for all foreign keys and frequently queried columns
- [ ] Data types are appropriate for the data being stored
- [ ] Timestamps have proper defaults and timezone handling

**Verification SQL**:
```sql
-- Check all tables have primary keys
SELECT tablename
FROM pg_tables
WHERE schemaname = 'public'
AND tablename NOT IN (
    SELECT DISTINCT tablename
    FROM pg_indexes
    WHERE indexname LIKE '%pkey%'
);

-- Check for missing indexes on foreign keys
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
AND tc.table_schema = 'public'
AND NOT EXISTS (
    SELECT 1 FROM pg_indexes
    WHERE tablename = tc.table_name
    AND indexdef LIKE '%' || kcu.column_name || '%'
);

-- Verify enum types are used for fixed sets
SELECT typname, typarray::regtype
FROM pg_type
WHERE typnamespace = 'public'::regnamespace
AND typisdefined
ORDER BY typname;
```

#### Index Performance Verification

- [ ] Run EXPLAIN ANALYZE on all critical queries
- [ ] Verify indexes are being used (Index Scan, not Seq Scan)
- [ ] Check for sequential scans on large tables
- [ ] Verify composite indexes match query patterns

**Verification SQL**:
```sql
-- Check for sequential scans on large tables
SELECT
    schemaname,
    relname,
    seq_scan,
    seq_tup_read,
    idx_scan,
    idx_tup_fetch,
    n_tup_ins,
    n_tup_upd,
    n_tup_del
FROM pg_stat_user_tables
WHERE seq_scan > 1000
ORDER BY seq_scan DESC;

-- Check index hit rates
SELECT
    schemaname,
    relname AS table_name,
    indexrelname AS index_name,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;
```

#### Migration Readiness

- [ ] All migrations are version-controlled
- [ ] Migrations are idempotent (can run multiple times safely)
- [ ] Rollback migrations are available
- [ ] Migrations have been tested in staging environment
- [ ] Long-running migrations are scheduled for low-traffic periods

**Verification Commands**:
```bash
# Check migration status
supabase migration list

# Verify migration files exist
ls -la supabase/migrations/

# Dry run migrations
supabase db push --dry-run
```

### 2. Row Level Security (RLS) Verification

#### Policy Coverage

**RLS Enable Status**:
- [ ] RLS is enabled on ALL user-facing tables
- [ ] No tables are missing RLS that should have it
- [ ] Development-only tables have appropriate exemptions

**Verification SQL**:
```sql
-- List all tables with RLS status
SELECT
    schemaname,
    tablename,
    rowsecurity AS rls_enabled
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

-- Tables without RLS that might need it
SELECT tablename
FROM pg_tables
WHERE schemaname = 'public'
AND tablename NOT IN (
    SELECT tablename FROM pg_tables WHERE rowsecurity = true
)
AND tablename NOT LIKE 'pg_%'
AND tablename NOT LIKE 'sql_%'
AND tablename NOT IN ('storage.objects', 'auth.users');
```

#### Policy Completeness

**CRUD Policy Coverage**:
- [ ] SELECT policies exist for all tables
- [ ] INSERT policies exist where data insertion is required
- [ ] UPDATE policies exist for mutable tables
- [ ] DELETE policies exist where data deletion is required
- [ ] WITH CHECK clauses are present for INSERT/UPDATE policies

**Verification SQL**:
```sql
-- Check policy coverage per table
SELECT
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    CASE WHEN cmd IN ('INSERT', 'UPDATE') THEN 'Yes' ELSE 'N/A' END AS has_with_check
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, cmd;
```

#### Policy Testing

**Security Testing Scenarios**:
- [ ] Anon users can only access intended public data
- [ ] Authenticated users cannot access other users' private data
- [ ] Users can only modify their own data
- [ ] Admin operations work correctly with elevated permissions
- [ ] Failed authorization returns appropriate error messages

**Test Cases**:
```sql
-- Test 1: Anon user access
SET ROLE anon;
SELECT COUNT(*) FROM profiles; -- Should return only public profiles

-- Test 2: Authenticated user access
SET ROLE authenticated;
SELECT * FROM profiles WHERE id = 'test-user-uuid'; -- Should only see own profile

-- Test 3: Cross-user access attempt
SET ROLE authenticated;
SELECT * FROM profiles WHERE id != auth.uid(); -- Should return empty for private data

-- Test 4: Insert permission
SET ROLE authenticated;
INSERT INTO posts (user_id, title) VALUES (auth.uid(), 'Test'); -- Should succeed
INSERT INTO posts (user_id, title) VALUES ('other-user', 'Test'); -- Should fail
```

### 3. Authentication Configuration

#### Auth Providers Setup

**Provider Configuration**:
- [ ] Required OAuth providers are configured (Google, GitHub, etc.)
- [ ] OAuth redirect URLs are correctly set in provider dashboards
- [ ] Email/password authentication is properly configured
- [ ] Magic link configuration is complete if used

**Security Settings**:
- [ ] Password minimum requirements meet security policy
- [ ] Email confirmation is required for new signups (if required)
- [ ] Password reset flow is tested and working
- [ ] Session timeout is appropriate for use case

**Verification Steps**:
```bash
# Check auth configuration
supabase auth secrets list

# Verify OAuth providers
# Check in Supabase Dashboard > Authentication > Providers
```

#### Token Security

**JWT Configuration**:
- [ ] JWT expiry is set appropriately (not too long)
- [ ] JWT secret is strong and stored securely
- [ ] Refresh token rotation is enabled
- [ ] Multiple sessions per user is handled correctly

**Client-Side Token Handling**:
- [ ] Tokens are stored securely (httpOnly cookies preferred)
- [ ] Token refresh logic is implemented
- [ ] Session expiration is handled gracefully
- [ ] Logout clears all token storage

**Verification Checklist**:
- [ ] Test token refresh flow manually
- [ ] Test session expiration behavior
- [ ] Verify logout clears all authentication state
- [ ] Check browser dev tools for token exposure

### 4. Storage Configuration

#### Bucket Security

**Public Buckets**:
- [ ] Only intended buckets are set to public
- [ ] File type restrictions are configured
- [ ] File size limits are set appropriately
- [ ] Public bucket policies are reviewed

**Private Buckets**:
- [ ] Private buckets require authentication
- [ ] Signed URL generation works correctly
- [ ] URL expiry is set appropriately
- [ ] Storage policies restrict access properly

**Verification SQL**:
```sql
-- Check bucket configurations
SELECT id, name, public, file_size_limit, allowed_mime_types
FROM storage.buckets;

-- Check storage policies
SELECT schemaname, tablename, policyname, cmd, permissive
FROM pg_policies
WHERE schemaname = 'storage';
```

#### Upload Security

**File Validation**:
- [ ] Client-side file type validation is implemented
- [ ] Server-side file type validation is enforced
- [ ] File size limits are enforced
- [ ] Filename sanitization prevents path traversal

**Upload Path Validation**:
- [ ] Users can only upload to their own folders
- [ ] Upload paths are validated against user ID
- [ ] Filename extension whitelist is enforced
- [ ] Duplicate filename handling is secure

**Access Control**:
- [ ] Users can only access their own files
- [ ] Admin access to all files is properly restricted
- [ ] Deleted files are properly removed
- [ ] File metadata is not exposed inappropriately

### 5. Edge Functions Security

#### Function Security

**Authentication Validation**:
- [ ] All functions validate auth tokens
- [ ] Token validation uses proper verification
- [ ] Invalid tokens return 401 errors
- [ ] Expired tokens are rejected

**Authorization Checks**:
- [ ] Functions verify user permissions before operations
- [ ] Role-based access is properly enforced
- [ ] Tenant isolation is maintained in multi-tenant apps

**Input Validation**:
- [ ] All input parameters are validated
- [ ] SQL injection prevention is in place
- [ ] XSS prevention for returned data
- [ ] Rate limiting is implemented where needed

**Code Security**:
- [ ] No sensitive data in function code
- [ ] Environment variables used for secrets
- [ ] Proper error handling without data exposure
- [ ] CORS configuration is appropriate

**Verification Template**:
```typescript
// Edge function security checklist
export default async (req: Request): Promise<Response> => {
    // 1. Authentication
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
        return new Response(JSON.stringify({ error: 'Unauthorized' }), { status: 401 });
    }
    
    // 2. Token validation
    const { data: { user }, error } = await supabaseAdmin.auth.getUser(
        authHeader.replace('Bearer ', '')
    );
    if (error || !user) {
        return new Response(JSON.stringify({ error: 'Invalid token' }), { status: 401 });
    }
    
    // 3. Authorization (example: check user role)
    const { data: profile } = await supabaseAdmin
        .from('profiles')
        .select('role')
        .eq('id', user.id)
        .single();
    
    if (profile?.role !== 'admin') {
        return new Response(JSON.stringify({ error: 'Forbidden' }), { status: 403 });
    }
    
    // 4. Input validation
    const body = await req.json();
    if (!validateInput(body)) {
        return new Response(JSON.stringify({ error: 'Invalid input' }), { status: 400 });
    }
    
    // 5. Process request
    // ... business logic
    
    // 6. Return response without sensitive data
    return new Response(JSON.stringify({ success: true }));
};
```

### 6. API Configuration

#### PostgREST Settings

**API Security**:
- [ ] Anon key is not exposed in public repositories
- [ ] Service role key is never used client-side
- [ ] API rate limiting is configured appropriately
- [ ] CORS settings are properly configured

**Performance Settings**:
- [ ] Connection pooler settings are optimized
- [ ] Max rows limit is appropriate
- [ ] Request timeout is configured
- [ ] Body size limit is set appropriately

**Verification**:
```bash
# Check API settings in Dashboard
# Settings > API > API Settings

# Verify rate limiting headers
curl -I https://your-project.supabase.co/rest/v1/users
# Should include rate limit headers
```

#### Environment Variables

**Required Variables**:
- [ ] SUPABASE_URL is correctly set
- [ ] SUPABASE_ANON_KEY is correctly set (public)
- [ ] SUPABASE_SERVICE_ROLE_KEY is securely stored (never client-side)
- [ ] All required API keys are in environment

**Verification**:
```bash
# Verify environment variables are set
# Client-side (.env)
echo $VITE_SUPABASE_URL
echo $VITE_SUPABASE_ANON_KEY

# Server-side (deployment environment)
echo $SUPABASE_SERVICE_ROLE_KEY
# Should NOT be exposed in client bundle
```

### 7. Monitoring and Logging

#### Alert Configuration

**Database Monitoring**:
- [ ] Connection count alerts are configured
- [ ] Query performance alerts are set
- [ ] Replication lag alerts are configured
- [ ] Storage usage alerts are in place

**Auth Monitoring**:
- [ ] Failed login alerts are configured
- [ ] Suspicious activity detection is enabled
- [ ] Session anomaly alerts are set
- [ ] New user creation alerts are configured

**Application Monitoring**:
- [ ] Edge function error alerts are configured
- [ ] API error rate alerts are set
- [ ] Latency alerts are in place
- [ ] Storage quota alerts are configured

#### Logging Configuration

**Log Retention**:
- [ ] Auth logs are retained per policy requirements
- [ ] API logs are retained appropriately
- [ ] Error logs are preserved for debugging
- [ ] Log rotation is configured

**Log Analysis**:
- [ ] Failed authentication attempts are logged
- [ ] Permission denied errors are logged
- [ ] Rate limit violations are logged
- [ ] Unusual patterns are detectable from logs

### 8. Backup and Recovery

#### Backup Configuration

**Database Backups**:
- [ ] Point-in-time recovery is enabled
- [ ] Backup schedule meets RTO/RPO requirements
- [ ] Backup integrity is verified regularly
- [ ] Backup restoration is tested

**Storage Backups**:
- [ ] Critical files are backed up
- [ ] Backup verification process exists
- [ ] Restoration procedures are documented

#### Recovery Procedures

**Disaster Recovery Plan**:
- [ ] Recovery time objective (RTO) is documented
- [ ] Recovery point objective (RPO) is documented
- [ ] Recovery procedures are documented
- [ ] Recovery is tested regularly

### 9. Performance Verification

#### Load Testing

**Pre-Production Testing**:
- [ ] Load testing completed at expected peak load
- [ ] Performance benchmarks are met
- [ ] No memory leaks detected
- [ ] Connection pool settings are optimized

**Verification Commands**:
```bash
# Run load test (example with k6)
k6 run tests/load-test.js

# Check connection pool stats
SELECT * FROM pg_stat_activity WHERE state = 'active';
```

#### Optimization Verification

**Database Optimization**:
- [ ] All critical queries use indexes
- [ ] EXPLAIN plans show efficient execution
- [ ] No N+1 query patterns in application code
- [ ] Pagination is implemented for large datasets

**Client Optimization**:
- [ ] Caching is implemented for static data
- [ ] Images are optimized and lazy-loaded
- [ ] Bundle size is reasonable
- [ ] CDN is configured for static assets

### 10. Compliance Verification

#### Data Protection

**Privacy Compliance**:
- [ ] PII handling meets requirements
- [ ] Data retention policies are implemented
- [ ] Right to deletion is supported
- [ ] Consent management is in place

**Security Compliance**:
- [ ] Encryption at rest is verified
- [ ] Encryption in transit is enforced
- [ ] Access controls meet requirements
- [ ] Audit logging is comprehensive

## Security Review Checklist

### Pre-Security Audit Checklist

**Access Control Review**:
- [ ] All admin accounts use MFA
- [ ] Service accounts have minimal required permissions
- [ ] API keys are rotated regularly
- [ ] Unused accounts are disabled

**Data Protection Review**:
- [ ] Sensitive data is encrypted
- [ ] Data classification is complete
- [ ] Access logging is enabled
- [ ] Data masking is applied where needed

**Network Security Review**:
- [ ] Database is not directly exposed
- [ ] API endpoints require authentication
- [ ] Rate limiting is enforced
- [ ] DDoS protection is in place

### Security Test Scenarios

**Authorization Tests**:
```typescript
// Test 1: Verify anon access is restricted
const { data, error } = await supabase
    .from('private_data')
    .select('*');
// Expected: Should return empty or error

// Test 2: Verify cross-tenant access is blocked
const { data, error } = await supabase
    .from('tenant_resources')
    .select('*')
    .neq('tenant_id', currentUserTenantId);
// Expected: Should return empty

// Test 3: Verify admin functions require admin role
const { data, error } = await supabase.functions
    .invoke('admin-delete-user', { body: { userId: 'xxx' } });
// Expected: Should return 403 for non-admin users
```

## Final Deployment Verification

### Pre-Launch Checklist

**Environment Configuration**:
- [ ] Production environment variables are set
- [ ] Debug mode is disabled
- [ ] Verbose logging is disabled
- [ ] Test data is cleaned from production

**Final Verification Tests**:
```bash
# 1. Database connectivity
psql $DATABASE_URL -c "SELECT 1;"

# 2. RLS policies working
psql $DATABASE_URL -c "SET ROLE anon; SELECT * FROM users LIMIT 1;"

# 3. Auth working
curl -X POST https://your-project.supabase.co/auth/v1/token?grant_type=password \
  -H "apikey: $ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# 4. Storage accessible
supabase storage ls

# 5. Edge functions deployed
supabase functions list
```

**Documentation Review**:
- [ ] API documentation is updated
- [ ] Deployment runbook is complete
- [ ] On-call procedures are documented
- [ ] Rollback plan is documented

### Post-Deployment Verification

**Immediate Post-Deploy Checks**:
- [ ] Health check endpoint returns 200
- [ ] Critical user flows are tested
- [ ] Monitoring dashboards show healthy metrics
- [ ] Error rates are normal

**Ongoing Monitoring Setup**:
- [ ] Dashboards are configured
- [ ] Alerts are tested and working
- [ ] On-call rotation is informed
- [ ] Incident response plan is ready

## Appendix

### Quick Reference: Environment-Specific Settings

**Development**:
```
RLS: Per-table decision
Auth: Relaxed validation
Logging: Verbose
Connection Pool: Minimal
```

**Staging**:
```
RLS: Full enforcement
Auth: Production-like validation
Logging: Moderate
Connection Pool: Production-like
```

**Production**:
```
RLS: Full enforcement on all tables
Auth: Strict validation with MFA
Logging: Minimal, performance-focused
Connection Pool: Optimized for load
Rate Limiting: Configured per API
Backups: Point-in-time enabled
```

### Troubleshooting Common Issues

**Issue: RLS blocking all access**
- Check if auth.uid() returns null
- Verify policies have proper USING clauses
- Test with service role key first

**Issue: Slow performance**
- Check for missing indexes
- Verify connection pool settings
- Review query EXPLAIN plans

**Issue: Auth not working**
- Verify JWT secret configuration
- Check token expiry settings
- Test token refresh flow

**Issue: Storage upload failing**
- Verify bucket policies
- Check file size limits
- Validate path restrictions

### Sign-Off Requirements

Before production deployment, the following sign-offs are required:

- [ ] **Security Review**: Security team has reviewed and approved
- [ ] **Database Review**: Database team has verified schema and indexes
- [ ] **DevOps Review**: DevOps team has verified infrastructure
- [ ] **QA Sign-Off**: QA team has completed testing
- [ ] **Product Sign-Off**: Product owner has approved feature readiness

---

**Related Documents**:
- `best-practice.md` - Detailed best practices for each component
- `anti-pattern.md` - Common mistakes to avoid
- `architecture.md` - System architecture overview
