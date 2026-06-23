---
title: "RLS Best Practices"
description: "Hướng dẫn thực hành tốt nhất khi triển khai Row Level Security trong PostgreSQL"
tags: ["rls", "postgres", "security", "best-practices", "database", "supabase"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# RLS Best Practices - Thực Hành Tốt Nhất

## Overview

Row Level Security (RLS) là một trong những cơ chế bảo mật quan trọng nhất trong PostgreSQL để kiểm soát truy cập ở cấp độ row. Việc triển khai RLS đúng cách không chỉ bảo vệ data mà còn đảm bảo hiệu suất và maintainability của hệ thống. Tài liệu này tổng hợp các best practices được đúc kết từ kinh nghiệm thực tế và các production deployments thành công.

Các best practices được chia thành categories theo lifecycle của RLS implementation: từ design, implementation, testing, đến monitoring và maintenance. Mỗi recommendation bao gồm rationale (lý do) và practical examples để bạn có thể apply ngay vào project của mình.

## Purpose

Mục tiêu của tài liệu này là cung cấp một comprehensive guide cho việc implement RLS một cách secure, performant, và maintainable. Dù bạn đang building một simple application hay một complex multi-tenant SaaS platform, các practices trong tài liệu này sẽ giúp bạn tránh common pitfalls và xây dựng một secure database architecture từ đầu.

## Key Concepts

### Defense in Depth

RLS nên được coi là một layer trong multi-layered security architecture. Không nên dựa hoàn toàn vào RLS để protect data - implement additional security measures như input validation, encryption, và audit logging. RLS là last line of defense khi application code có vulnerabilities.

### Principle of Least Privilege

Mỗi user và role chỉ nên có exactly the permissions họ cần để perform their tasks. Không bao giờ grant more permissions than necessary. Điều này áp dụng cả cho application roles và individual user permissions.

### Fail Securely

Khi có lỗi hoặc unexpected conditions, RLS policies nên deny access thay vì allow. Default deny là nguyên tắc cơ bản - nếu không có policy explicitly allows access, access nên bị denied.

## Best Practices

### 1. RLS Setup and Configuration

#### Enable RLS Immediately on Table Creation

**Practice**: Luôn enable RLS ngay khi tạo table, không để sau.

```sql
-- CORRECT: Enable RLS ngay khi tạo table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS immediately
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE users FORCE ROW LEVEL SECURITY;

-- Tạo policies ngay lập tức
CREATE POLICY users_own ON users
    FOR ALL
    USING (id = auth.uid())
    WITH CHECK (id = auth.uid());

-- Grant permissions
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT SELECT, INSERT, UPDATE ON users TO authenticated;
```

**Rationale**: Enabling RLS sau khi table đã có data có thể gây ra unexpected access changes. Nếu enable RLS mà không có policies, all access sẽ be denied, có thể break existing applications.

#### Use FORCE ROW LEVEL SECURITY

**Practice**: Sử dụng FORCE ROW LEVEL SECURITY để đảm bảo policies apply cả cho table owner.

```sql
-- Force RLS even for table owner
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

-- Verify
SELECT relrowsecurity, relforcerowsecurity
FROM pg_class
WHERE relname = 'orders';

-- Result: t (true) for both columns
```

**Rationale**: Theo mặc định, table owner bypasses RLS. FORCE ROW LEVEL SECURITY đảm bảo policies apply cho tất cả users bao gồm cả owner. Điều này ngăn chặn potential security bypasses qua direct database access.

### 2. Policy Naming Conventions

#### Use Descriptive, Consistent Naming

**Practice**: Áp dụng consistent naming convention cho tất cả policies.

```sql
-- Naming Pattern: {table}_{access_type}_{qualifier}
-- Examples:
CREATE POLICY users_select_own ON users FOR SELECT USING (id = auth.uid());
CREATE POLICY users_insert_own ON users FOR INSERT WITH CHECK (id = auth.uid());
CREATE POLICY users_update_own ON users FOR UPDATE USING (id = auth.uid()) WITH CHECK (id = auth.uid());
CREATE POLICY users_delete_own ON users FOR DELETE USING (id = auth.uid());

-- For admin policies:
CREATE POLICY users_select_admin ON users FOR SELECT TO admin USING (true);
CREATE POLICY users_all_admin ON users FOR ALL TO admin USING (true);

-- For public read:
CREATE POLICY products_select_public ON products FOR SELECT USING (is_active = true);
```

**Rationale**: Clear naming giúp developers nhanh chóng hiểu purpose của policy. Nó also makes debugging easier khi bạn có thể identify policies by name trong logs và error messages.

#### Include Version and Documentation in Comments

```sql
/**
 * Policy: orders_all_own
 * Version: 1.2.0
 * Created: 2024-01-15
 * Updated: 2024-06-20
 * Owner: Security Team
 * 
 * Purpose:
 * - Allow users to CRUD their own orders
 * - Allow admins to access all orders
 * 
 * Access Matrix:
 * | Role    | SELECT | INSERT | UPDATE | DELETE |
 * |---------|--------|--------|--------|--------|
 * | Owner   | Yes    | Yes    | Yes    | Yes    |
 * | Admin   | Yes    | Yes    | Yes    | Yes    |
 * | Support | Yes    | No     | Yes*   | No     |
 * 
 * * Only pending orders
 */
CREATE POLICY orders_all_own ON orders
    FOR ALL
    USING (
        customer_id = auth.uid()
        OR EXISTS (SELECT 1 FROM user_roles WHERE user_id = auth.uid() AND role = 'admin')
    )
    WITH CHECK (
        customer_id = auth.uid()
        OR EXISTS (SELECT 1 FROM user_roles WHERE user_id = auth.uid() AND role = 'admin')
    );
```

### 3. Policy Design Patterns

#### Use Single ALL Policy When Possible

**Practice**: Sử dụng single policy với FOR ALL thay vì multiple separate policies khi logic giống nhau.

```sql
-- PREFERRED: Single ALL policy
CREATE POLICY orders_own ON orders
    FOR ALL
    USING (customer_id = auth.uid())
    WITH CHECK (customer_id = auth.uid());

-- AVOID: Multiple separate policies (unless logic differs)
CREATE POLICY orders_select_own ON orders FOR SELECT USING (customer_id = auth.uid());
CREATE POLICY orders_insert_own ON orders FOR INSERT WITH CHECK (customer_id = auth.uid());
CREATE POLICY orders_update_own ON orders FOR UPDATE USING (customer_id = auth.uid());
CREATE POLICY orders_delete_own ON orders FOR DELETE USING (customer_id = auth.uid());
```

**Rationale**: Single policy dễ maintain hơn, nhưng separate policies cho phép different logic cho different operations. Use single policy khi logic giống nhau, separate policies khi cần differentiate.

#### Combine Ownership with Role-Based Access

**Practice**: Kết hợp ownership check với role-based admin access.

```sql
CREATE POLICY documents_access ON documents
    FOR ALL
    USING (
        -- Owner has full access
        owner_id = auth.uid()
        -- Admins have full access
        OR EXISTS (
            SELECT 1 FROM user_roles
            WHERE user_id = auth.uid()
            AND role = 'admin'
        )
        -- Editors can modify shared documents
        OR (
            'editor' IN (
                SELECT role FROM user_roles WHERE user_id = auth.uid()
            )
            AND shared_with_editors = true
        )
    )
    WITH CHECK (
        owner_id = auth.uid()
        OR EXISTS (
            SELECT 1 FROM user_roles
            WHERE user_id = auth.uid()
            AND role = 'admin'
        )
    );
```

#### Use Helper Functions for Complex Logic

**Practice**: Encapsulate complex access logic trong helper functions.

```sql
-- Helper function for admin check
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM user_roles
        WHERE user_id = auth.uid()
        AND role = 'admin'
    );
END;
$$ LANGUAGE plpgsql STABLE;

-- Helper function for tenant access
CREATE OR REPLACE FUNCTION can_access_tenant(p_tenant_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM user_tenants
        WHERE user_id = auth.uid()
        AND tenant_id = p_tenant_id
    );
END;
$$ LANGUAGE plpgsql STABLE;

-- Cleaner policies using helpers
CREATE POLICY orders_tenant_access ON orders
    FOR SELECT
    USING (
        can_access_tenant(tenant_id)
        OR is_admin()
    );
```

### 4. Multi-Tenant Implementation

#### Use Session Settings for Tenant Context

**Practice**: Sử dụng PostgreSQL session settings để maintain tenant context.

```sql
-- Set tenant context function
CREATE OR REPLACE FUNCTION set_tenant_context(p_tenant_id UUID)
RETURNS VOID AS $$
BEGIN
    PERFORM set_config('app.current_tenant_id', p_tenant_id::TEXT, false);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Get tenant context function
CREATE OR REPLACE FUNCTION current_tenant_id()
RETURNS UUID AS $$
BEGIN
    RETURN NULLIF(
        current_setting('app.current_tenant_id', true),
        ''
    )::UUID;
END;
$$ LANGUAGE plpgsql STABLE;

-- Tenant isolation policy
CREATE POLICY orders_tenant_isolation ON orders
    FOR ALL
    USING (
        tenant_id = current_tenant_id()
        OR is_admin()
    )
    WITH CHECK (
        tenant_id = current_tenant_id()
        OR is_admin()
    );

-- Usage in transactions
BEGIN;
    SELECT set_tenant_context('tenant-uuid');
    SELECT * FROM orders;  -- Only tenant's orders
COMMIT;
```

#### Separate Tenant Data Completely

**Practice**: Đảm bảo mỗi tenant chỉ có thể access data của họ.

```sql
-- Tenant-scoped tables
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    plan TEXT DEFAULT 'free',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE tenant_users (
    tenant_id UUID REFERENCES tenants(id),
    user_id UUID REFERENCES auth.users(id),
    role TEXT DEFAULT 'member',
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (tenant_id, user_id)
);

CREATE TABLE tenant_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    created_by UUID REFERENCES auth.users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for performance
CREATE INDEX idx_tenant_documents_tenant ON tenant_documents(tenant_id);

-- Comprehensive tenant isolation
CREATE POLICY tenant_documents_isolation ON tenant_documents
    FOR ALL
    USING (
        tenant_id IN (
            SELECT tenant_id FROM tenant_users WHERE user_id = auth.uid()
        )
        OR is_admin()
    )
    WITH CHECK (
        tenant_id IN (
            SELECT tenant_id FROM tenant_users WHERE user_id = auth.uid()
        )
    );
```

### 5. Performance Optimization

#### Index Policy Columns

**Practice**: Tạo indexes trên columns được sử dụng trong RLS policies.

```sql
-- Common RLS columns that need indexes
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_tenant ON orders(tenant_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_documents_owner ON documents(owner_id);
CREATE INDEX idx_user_tenants_user ON user_tenants(user_id);
CREATE INDEX idx_user_tenants_tenant ON user_tenants(tenant_id);

-- Partial indexes for specific access patterns
CREATE INDEX idx_orders_pending_customer ON orders(customer_id)
    WHERE status = 'pending';

CREATE INDEX idx_products_active ON products(id)
    WHERE is_active = true;

-- Composite indexes for combined conditions
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);
```

#### Use STABLE Functions for RLS

**Practice**: Mark helper functions as STABLE để allow query optimization.

```sql
-- CORRECT: STABLE for read-only functions
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM user_roles
        WHERE user_id = auth.uid()
        AND role = 'admin'
    );
END;
$$ LANGUAGE plpgsql STABLE;  -- Can be cached by optimizer

-- CORRECT: IMMUTABLE for truly constant functions
CREATE OR REPLACE FUNCTION app_version()
RETURNS TEXT AS $$
BEGIN
    RETURN '1.0.0';
END;
$$ LANGUAGE plpgsql IMMUTABLE;  -- Always returns same value

-- AVOID: VOLATILE in RLS helper functions (causes re-evaluation)
```

#### Monitor Query Plans Regularly

```sql
-- Check query plan for RLS impact
EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS)
SELECT * FROM orders WHERE customer_id = auth.uid();

-- Monitor RLS statistics
SELECT
    schemaname,
    tablename,
    policyname,
    cmd,
    permissive,
    roles
FROM pg_policies
WHERE schemaname = 'public';

-- Check for seq scans (potential performance issue)
SELECT
    relname,
    seq_scan,
    seq_tup_read,
    idx_scan,
    idx_tup_fetch
FROM pg_stat_user_tables
WHERE relname IN ('orders', 'users', 'documents');
```

### 6. Testing Strategies

#### Test Each Policy Thoroughly

**Practice**: Test tất cả access scenarios cho mỗi policy.

```sql
-- Test setup
CREATE TABLE test_results (
    test_name TEXT,
    passed BOOLEAN,
    details TEXT,
    tested_at TIMESTAMPTZ DEFAULT NOW()
);

-- Test function
CREATE OR REPLACE FUNCTION test_policy(
    p_test_name TEXT,
    p_expected_pass BOOLEAN,
    p_sql TEXT
) RETURNS VOID AS $$
DECLARE
    v_result BOOLEAN;
    v_count INTEGER;
BEGIN
    EXECUTE p_sql INTO v_count;
    v_result := (v_count > 0 AND p_expected_pass)
             OR (v_count = 0 AND NOT p_expected_pass);
    
    INSERT INTO test_results (test_name, passed, details)
    VALUES (
        p_test_name,
        v_result,
        CASE WHEN v_result THEN 'PASS' ELSE 'FAIL: expected ' || p_expected_pass || ' got ' || v_count || ' rows' END
    );
END;
$$ LANGUAGE plpgsql;

-- Test cases
BEGIN;

-- As regular user
SET ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub":"user-123"}';

SELECT test_policy(
    'User can see own orders',
    TRUE,
    'SELECT COUNT(*) FROM orders WHERE customer_id = ''user-123'''
);

SELECT test_policy(
    'User cannot see other user orders',
    TRUE,
    'SELECT COUNT(*) FROM orders WHERE customer_id = ''user-other'''
);

-- As admin
SET LOCAL request.jwt.claims = '{"sub":"admin-456","app_metadata":{"role":"admin"}}';

SELECT test_policy(
    'Admin can see all orders',
    TRUE,
    'SELECT COUNT(*) FROM orders'
);

-- As anonymous
RESET ROLE;

SELECT test_policy(
    'Anonymous sees no orders',
    TRUE,
    'SELECT COUNT(*) FROM orders'
);

COMMIT;
```

#### Use Automated Policy Testing

```sql
-- Comprehensive test suite
CREATE OR REPLACE FUNCTION run_rls_test_suite()
RETURNS TABLE (
    test_category TEXT,
    test_name TEXT,
    passed BOOLEAN,
    execution_time_ms NUMERIC
) AS $$
DECLARE
    v_start_time TIMESTAMPTZ;
    v_test RECORD;
BEGIN
    FOR v_test IN (
        -- Ownership tests
        SELECT 'ownership' as category, 'user_sees_own_data' as name,
               'SELECT * FROM users WHERE id = auth.uid()' as sql, TRUE as expected,
               'user-123' as user_context, 'authenticated' as role
        UNION ALL
        SELECT 'ownership', 'user_cannot_see_others',
               'SELECT * FROM users WHERE id = ''user-other''', FALSE, 'user-123', 'authenticated'
        UNION ALL
        -- Admin tests
        SELECT 'admin', 'admin_sees_all',
               'SELECT COUNT(*) FROM users', TRUE, 'admin-1', 'admin'
        UNION ALL
        -- Tenant tests
        SELECT 'tenant', 'user_sees_own_tenant_data',
               'SELECT COUNT(*) FROM tenant_data', TRUE, 'tenant-user-1', 'authenticated'
    ) LOOP
        v_start_time := clock_timestamp();
        
        -- Execute test (simplified)
        RETURN NEXT;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

### 7. Security Hardening

#### Restrict Public Schema Access

**Practice**: Không bao giờ grant permissions to PUBLIC role.

```sql
-- Remove all PUBLIC grants
REVOKE USAGE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM PUBLIC;

-- Grant only to specific roles
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT SELECT ON public.products TO PUBLIC;  -- If truly public
GRANT SELECT ON public.categories TO PUBLIC;
```

#### Validate JWT Claims Properly

```sql
-- Safe JWT claim access
CREATE POLICY secure_data_access ON secure_data
    FOR SELECT
    USING (
        auth.uid() IS NOT NULL
        AND (
            owner_id = auth.uid()
            OR (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
        )
    );

-- Validate claim types
CREATE OR REPLACE FUNCTION safe_get_user_role()
RETURNS TEXT AS $$
BEGIN
    RETURN NULLIF(
        auth.jwt() -> 'app_metadata' ->> 'role',
        ''
    );
END;
$$ LANGUAGE plpgsql STABLE;

-- Use in policies
CREATE POLICY role_based_access ON admin_data
    FOR SELECT
    USING (
        safe_get_user_role() = 'admin'
    );
```

#### Implement Audit Logging

```sql
-- Audit log table
CREATE TABLE rls_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name TEXT NOT NULL,
    operation TEXT NOT NULL,
    user_id UUID,
    row_id UUID,
    allowed BOOLEAN NOT NULL,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Audit trigger function
CREATE OR REPLACE FUNCTION audit_rls_access()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO rls_audit_log (
        table_name,
        operation,
        user_id,
        row_id,
        allowed,
        ip_address
    )
    SELECT
        TG_TABLE_NAME,
        TG_OP,
        auth.uid(),
        COALESCE(NEW.id, OLD.id),
        TRUE,
        NULLIF(current_setting('request.client_addr', true), '')::INET;
    
    RETURN NEW;
EXCEPTION WHEN OTHERS THEN
    RAISE WARNING 'Audit failed: %', SQLERRM;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Apply audit to sensitive tables
CREATE TRIGGER orders_rls_audit
    AFTER INSERT OR UPDATE OR DELETE ON orders
    FOR EACH ROW EXECUTE FUNCTION audit_rls_access();
```

### 8. Maintenance and Monitoring

#### Regular Policy Reviews

```sql
-- Policy inventory query
SELECT
    schemaname,
    tablename,
    policyname,
    cmd,
    permissive,
    roles,
    qual::text as condition,
    with_check::text as check_condition,
    pg_get_expr(qual, oid) as using_expression,
    pg_get_expr(with_check, oid) as with_check_expression
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;

-- Check for potentially dangerous policies
SELECT
    tablename,
    policyname,
    qual::text
FROM pg_policies
WHERE qual::text = 'true'::text
   OR qual::text = '(true)'
   OR qual::text LIKE '%1 = 1%';

-- Policy usage statistics
SELECT
    pol.polname as policy_name,
    rel.relname as table_name,
    stat.idx_scan,
    stat.seq_scan
FROM pg_policy pol
JOIN pg_class rel ON pol.polrelid = rel.oid
LEFT JOIN pg_stat_user_tables stat ON stat.relname = rel.relname
WHERE rel.relnamespace = 'public'::regnamespace;
```

#### Monitor for Anomalies

```sql
-- Check for unusual access patterns
SELECT
    user_id,
    table_name,
    COUNT(*) as access_count,
    MAX(created_at) as last_access
FROM rls_audit_log
WHERE created_at > NOW() - INTERVAL '24 hours'
GROUP BY user_id, table_name
HAVING COUNT(*) > 10000;  -- Unusually high access

-- Failed access attempts
SELECT
    user_id,
    table_name,
    COUNT(*) as failed_count
FROM rls_audit_log
WHERE NOT allowed
AND created_at > NOW() - INTERVAL '1 hour'
GROUP BY user_id, table_name;
```

## Common Patterns

### Pattern 1: User-Owned Data

```sql
CREATE POLICY user_owned_data ON user_data
    FOR ALL
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());
```

### Pattern 2: Role-Based Access

```sql
CREATE POLICY admin_only ON sensitive_data
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM user_roles
            WHERE user_id = auth.uid()
            AND role = 'admin'
        )
    );
```

### Pattern 3: Team/Group Shared Data

```sql
CREATE POLICY team_shared ON team_documents
    FOR ALL
    USING (
        owner_id = auth.uid()
        OR team_id IN (
            SELECT team_id FROM team_members
            WHERE user_id = auth.uid()
        )
    );
```

### Pattern 4: Time-Limited Access

```sql
CREATE POLICY document_time_access ON documents
    FOR SELECT
    USING (
        owner_id = auth.uid()
        OR (
            valid_from <= NOW()
            AND (valid_until IS NULL OR valid_until > NOW())
            AND has_subscription(auth.uid())
        )
    );
```

## Troubleshooting

### Common Issues and Solutions

**Issue**: User không thấy data dù có quyền

```sql
-- Check 1: auth.uid() returns NULL?
SELECT auth.uid();  -- Should return UUID

-- Check 2: RLS enabled?
SELECT relrowsecurity FROM pg_class WHERE relname = 'your_table';

-- Check 3: Policy exists?
SELECT * FROM pg_policies WHERE tablename = 'your_table';

-- Check 4: Test policy directly
EXPLAIN SELECT * FROM your_table;
```

**Issue**: Performance chậm với RLS

```sql
-- Check 1: Seq scans?
EXPLAIN SELECT * FROM orders WHERE customer_id = auth.uid();

-- Check 2: Missing indexes?
SELECT indexname FROM pg_indexes WHERE tablename = 'orders';

-- Check 3: Complex policy?
EXPLAIN ANALYZE SELECT * FROM orders;
```

## Examples

### Complete Multi-Tenant SaaS Example

```sql
-- ============================================
-- Schema Setup
-- ============================================

-- Core tables
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    plan TEXT DEFAULT 'free',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE tenant_members (
    tenant_id UUID REFERENCES tenants(id),
    user_id UUID REFERENCES auth.users(id),
    role TEXT DEFAULT 'member',
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (tenant_id, user_id)
);

CREATE TABLE tenant_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) NOT NULL,
    name TEXT NOT NULL,
    created_by UUID REFERENCES auth.users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for RLS performance
CREATE INDEX idx_tenant_members_user ON tenant_members(user_id);
CREATE INDEX idx_tenant_members_tenant ON tenant_members(tenant_id);
CREATE INDEX idx_tenant_data_tenant ON tenant_data(tenant_id);

-- ============================================
-- RLS Setup
-- ============================================

-- Enable RLS
ALTER TABLE tenant_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE tenant_members FORCE ROW LEVEL SECURITY;
ALTER TABLE tenant_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE tenant_data FORCE ROW LEVEL SECURITY;

-- Helper functions
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM user_roles
        WHERE user_id = auth.uid()
        AND role = 'admin'
    );
END;
$$ LANGUAGE plpgsql STABLE;

CREATE OR REPLACE FUNCTION is_tenant_member(p_tenant_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM tenant_members
        WHERE tenant_id = p_tenant_id
        AND user_id = auth.uid()
    );
END;
$$ LANGUAGE plpgsql STABLE;

-- Tenant membership policies
CREATE POLICY tenant_members_self ON tenant_members
    FOR SELECT
    USING (user_id = auth.uid() OR is_admin());

-- Tenant data policies
CREATE POLICY tenant_data_access ON tenant_data
    FOR SELECT
    USING (
        is_tenant_member(tenant_id)
        OR is_admin()
    );

CREATE POLICY tenant_data_insert ON tenant_data
    FOR INSERT
    WITH CHECK (
        is_tenant_member(tenant_id)
        OR is_admin()
    );

CREATE POLICY tenant_data_update ON tenant_data
    FOR UPDATE
    USING (
        is_tenant_member(tenant_id)
        OR is_admin()
    )
    WITH CHECK (
        is_tenant_member(tenant_id)
        OR is_admin()
    );

CREATE POLICY tenant_data_delete ON tenant_data
    FOR DELETE
    USING (is_admin());

-- Permissions
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT SELECT, INSERT, UPDATE ON tenant_members TO authenticated;
GRANT ALL ON tenant_data TO authenticated;
```

## References

- [PostgreSQL Row Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [Supabase RLS](https://supabase.com/docs/guides/auth/row-level-security)
- [PostgreSQL Performance Tuning](https://www.postgresql.org/docs/current/performance-tips.html)
- [Cursor Enterprise Framework Security Rules](../rules/security.md)
- [Cursor Enterprise Framework Multi-Tenant Rules](../rules/multi-tenant.md)
- [Cursor Enterprise Framework Database Rules](../rules/database.md)
