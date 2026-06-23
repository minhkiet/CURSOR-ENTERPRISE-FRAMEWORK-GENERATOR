---
title: "RLS Glossary"
description: "Từ điển thuật ngữ chuyên ngành Row Level Security trong PostgreSQL"
tags: ["rls", "postgres", "security", "glossary", "database", "terminology"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# RLS Glossary - Từ Điển Thuật Ngữ

## Overview

Row Level Security (RLS) là một feature phức tạp của PostgreSQL với nhiều thuật ngữ và khái niệm chuyên biệt. Tài liệu này cung cấp một glossary toàn diện giải thích tất cả các thuật ngữ quan trọng liên quan đến RLS, từ các khái niệm cơ bản đến các advanced features. Glossary này được thiết kế để serve as a quick reference cho developers, DBAs, và security engineers làm việc với RLS.

Mỗi term bao gồm: định nghĩa chính xác, ngữ cảnh sử dụng, ví dụ thực tế (khi applicable), và cross-references đến các related terms. Terms được sắp xếp theo alphabetical order để dễ tra cứu.

## Purpose

Mục tiêu của glossary này là đảm bảo consistent terminology across all team members và projects. Sử dụng standardized terminology giúp reduce confusion, improve communication, và make documentation more accessible. Glossary cũng serves as a training resource cho new team members learning about RLS và database security.

## Key Terms

### A

#### Access Control

**Definition**: Quá trình xác định ai có thể truy cập resources nào và ở mức nào. Trong context của RLS, access control được implement ở database level thông qua policies.

**Context**: Access control bao gồm identification (xác định identity), authentication (xác minh identity), authorization (xác định permissions), và auditing (theo dõi access).

**Example**:
```sql
-- Access control via RLS policy
CREATE POLICY orders_access ON orders
    FOR SELECT
    USING (customer_id = auth.uid());
```

**Related Terms**: Authentication, Authorization, RLS Policy

#### Audit Log

**Definition**: Bản ghi chi tiết của tất cả các hoạt động truy cập database, bao gồm user identity, timestamp, operation type, và affected data.

**Context**: Audit logs là critical cho compliance requirements (GDPR, SOC2, HIPAA) và security incident investigation.

**Example**:
```sql
CREATE TABLE audit_log (
    id UUID PRIMARY KEY,
    user_id UUID,
    operation TEXT,
    table_name TEXT,
    row_id UUID,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);
```

**Related Terms**: Compliance, Security Monitoring, Row Security Filter

### B

#### Bypass RLS

**Definition**: Khả năng bỏ qua Row Level Security checks. Có thể xảy ra qua service roles, superuser privileges, hoặc SECURITY DEFINER functions.

**Context**: Bypass RLS nên được sử dụng một cách có kiểm soát và chỉ khi cần thiết. Improper bypass configuration là một security risk lớn.

**Example**:
```sql
-- Superuser bypasses RLS
-- This should only be used for administrative tasks

-- Service role with BYPASSRLS attribute
SELECT rolbypassrls FROM pg_roles WHERE rolname = 'service_role';
-- Returns: t (true)
```

**Related Terms**: FORCE ROW LEVEL SECURITY, SECURITY DEFINER, Service Role

### C

#### Column-level Security

**Definition**: Cơ chế bảo mật kiểm soát truy cập ở cấp độ column thay vì row. PostgreSQL không có native column-level security như RLS, nhưng có thể implement qua views hoặc column privileges.

**Context**: Column-level security bổ sung cho RLS bằng cách kiểm soát truy cập đến specific columns.

**Example**:
```sql
-- Create view that hides sensitive columns
CREATE VIEW public_orders AS
SELECT id, customer_id, total, status
FROM orders;

-- Policy on view instead of table
CREATE POLICY public_orders_view ON public_orders
    FOR SELECT USING (true);
```

**Related Terms**: Row Level Security, Column Privileges, Views

#### Command (cmd)

**Definition**: Loại operation mà một RLS policy áp dụng. Các giá trị hợp lệ: SELECT, INSERT, UPDATE, DELETE, ALL.

**Context**: Khi tạo policy, bạn chỉ định command(s) mà policy applies to. Mỗi command có thể có different policies.

**Example**:
```sql
CREATE POLICY orders_select ON orders FOR SELECT USING (...);
CREATE POLICY orders_insert ON orders FOR INSERT WITH CHECK (...);
CREATE POLICY orders_update ON orders FOR UPDATE ...;
CREATE POLICY orders_delete ON orders FOR DELETE USING (...);
```

**Related Terms**: RLS Policy, USING Clause, WITH CHECK

#### Current Setting

**Definition**: PostgreSQL function để get/set configuration parameters cho current session. Được sử dụng trong RLS để access JWT claims và custom settings.

**Context**: `current_setting('request.jwt.claims', true)` được sử dụng để access JWT data trong Supabase. Parameter thứ hai (true) cho phép missing setting trả về NULL thay vì error.

**Example**:
```sql
-- Get JWT claims
SELECT current_setting('request.jwt.claims', true)::jsonb;

-- Get specific claim
SELECT current_setting('request.jwt.claims', true)::jsonb->>'tenant_id';

-- Custom application setting
PERFORM set_config('app.current_tenant_id', 'tenant-123', false);
```

**Related Terms**: JWT, Session Settings, Supabase Auth

### D

#### Database Role

**Definition**: Một database object xác định một tập hợp privileges. Roles có thể represent users hoặc groups và có thể granted permissions.

**Context**: Roles được sử dụng trong RLS để determine which policies apply to a user. `SET ROLE` changes the current user context.

**Example**:
```sql
-- Create roles
CREATE ROLE app_user;
CREATE ROLE app_admin;
CREATE ROLE app_support;

-- Grant role
GRANT app_admin TO authenticated_user;

-- Set role in session
SET ROLE app_admin;
```

**Related Terms**: RLS Policy, GRANT, SET ROLE

#### Default Deny

**Definition**: Nguyên tắc bảo mật where access được denied by default và chỉ granted khi explicitly allowed. RLS follows default deny: nếu không có policy allows access, access bị denied.

**Context**: Default deny là fundamental principle của RLS. Khi RLS enabled mà không có policies, all access is denied.

**Example**:
```sql
-- Enable RLS without policies = default deny
ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;

-- All queries return empty
SELECT * FROM sensitive_data;  -- Returns: (empty)

-- Need explicit policy to allow access
CREATE POLICY allow_read ON sensitive_data
    FOR SELECT USING (true);
```

**Related Terms**: RLS Policy, Default Allow, Permission Model

### E

#### EXPLAIN

**Definition**: PostgreSQL command hiển thị execution plan của một query mà không actually executing nó. Được sử dụng để diagnose RLS performance issues.

**Context**: EXPLAIN output cho biết có bao nhiêu rows were filtered by RLS và có Row Security Filter được applied không.

**Example**:
```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = auth.uid();

/*
Output:
Seq Scan on orders
  Filter: (customer_id = 'xxx')
  Row Security Filter: (customer_id = 'xxx')
*/
```

**Related Terms**: Row Security Filter, Query Performance, pg_stat_statements

### F

#### FORCE ROW LEVEL SECURITY

**Definition**: PostgreSQL option để ensure RLS policies được applied cho tất cả users bao gồm cả table owner. Without this, table owner bypasses RLS.

**Context**: FORCE ROW LEVEL SECURITY nên được enabled cho security-sensitive tables để prevent owner from bypassing policies.

**Example**:
```sql
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

-- Verify
SELECT relrowsecurity, relforcerowsecurity
FROM pg_class WHERE relname = 'orders';
-- Both return: t (true)
```

**Related Terms**: Row Level Security, Table Owner, BYPASSRLS

### G

#### GRANT

**Definition**: SQL command để assign privileges to roles. Được sử dụng để control access ở table và column level.

**Context**: GRANT được sử dụng song song với RLS. RLS controls which rows are visible, GRANT controls which operations are permitted.

**Example**:
```sql
-- Grant table permissions
GRANT SELECT, INSERT, UPDATE ON orders TO authenticated;

-- Grant schema usage
GRANT USAGE ON SCHEMA public TO authenticated;

-- Revoke public access
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
```

**Related Terms**: RLS Policy, REVOKE, Privileges

### H

#### Helper Function

**Definition**: User-defined function được sử dụng trong RLS policies để encapsulate complex logic hoặc provide reusable access checks.

**Context**: Helper functions make policies cleaner và reusable. They should be marked STABLE for query optimization.

**Example**:
```sql
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

-- Use in policy
CREATE POLICY admin_only ON admin_data
    FOR SELECT USING (is_admin());
```

**Related Terms**: RLS Policy, SECURITY DEFINER, STABLE Function

### I

#### Index

**Definition**: Database structure improves query speed by enabling efficient lookup. Indexes on RLS policy columns are critical for performance.

**Context**: RLS policies that filter on columns need indexes to maintain performance. Without indexes, every query requires a full table scan.

**Example**:
```sql
-- Index for user-based RLS
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Composite index for complex policies
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);

-- Partial index for specific access patterns
CREATE INDEX idx_orders_pending ON orders(id)
    WHERE status = 'pending';
```

**Related Terms**: RLS Policy, Query Performance, B-tree Index

### J

#### JWT (JSON Web Token)

**Definition**: A compact, URL-safe means of representing claims to be transferred between two parties. In Supabase, JWTs contain user identity and metadata.

**Context**: JWT claims được used by RLS policies via `auth.jwt()` và `auth.uid()`. JWT should be validated before RLS policy evaluation.

**Example**:
```sql
-- Access JWT claims
SELECT auth.jwt();

-- Access specific claim
SELECT auth.jwt()->>'app_metadata';

-- Policy using JWT claim
CREATE POLICY admin_only ON admin_data
    FOR SELECT
    USING ((auth.jwt()->'app_metadata'->>'role') = 'admin');
```

**Related Terms**: auth.uid(), Supabase, JWT Claims

### L

#### Least Privilege

**Definition**: Security principle where users/roles are granted only the minimum permissions necessary to perform their tasks. Không được confused với default deny.

**Context**: Least privilege applies to both database privileges (via GRANT/REVOKE) và RLS policies. Users should only see data they need, nothing more.

**Example**:
```sql
-- Instead of: GRANT ALL ON table TO user;
-- Use: Specific permissions only
GRANT SELECT ON orders TO user;  -- Can only read, not modify
GRANT INSERT ON orders TO user; -- Separate grant for insert

-- RLS: Only see own orders, not all
CREATE POLICY orders_own ON orders
    FOR SELECT USING (customer_id = auth.uid());
```

**Related Terms**: Default Deny, GRANT, RLS Policy

### M

#### Multi-Tenant

**Definition**: Architecture pattern where a single application instance serves multiple customers (tenants), with data isolation between tenants.

**Context**: RLS is commonly used for multi-tenant data isolation. Each tenant's data must be completely separate from others.

**Example**:
```sql
-- Tenant-scoped table
CREATE TABLE tenant_data (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    data TEXT
);

-- Tenant isolation policy
CREATE POLICY tenant_isolation ON tenant_data
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);

-- Set tenant context
SET app.current_tenant_id = 'tenant-123';
SELECT * FROM tenant_data;  -- Only tenant-123's data
```

**Related Terms**: Tenant Isolation, RLS Policy, Session Settings

### N

#### NULL Comparison

**Definition**: So sánh với NULL trong SQL luôn trả về NULL (unknown), không phải TRUE hoặc FALSE. Đây là common source of RLS bugs.

**Context**: When `auth.uid()` is NULL, comparisons like `column = NULL` always fail. RLS policies must handle NULL explicitly.

**Example**:
```sql
-- WRONG: Doesn't work when auth.uid() is NULL
CREATE POLICY unsafe ON orders
    FOR SELECT USING (customer_id = auth.uid());

-- CORRECT: Explicit NULL check
CREATE POLICY safe ON orders
    FOR SELECT USING (
        auth.uid() IS NOT NULL
        AND customer_id = auth.uid()
    );
```

**Related Terms**: auth.uid(), RLS Policy, SQL NULL Semantics

### O

#### Ownership Model

**Definition**: Pattern where each row has an owner (typically user_id), và access is controlled based on that ownership relationship.

**Context**: Ownership model là most common RLS pattern. Users can only access rows they own (where their user_id matches).

**Example**:
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    owner_id UUID REFERENCES auth.users(id),
    title TEXT,
    content TEXT
);

CREATE POLICY document_ownership ON documents
    FOR ALL
    USING (owner_id = auth.uid())
    WITH CHECK (owner_id = auth.uid());
```

**Related Terms**: User-Owned Data, RLS Policy, Owner ID

### P

#### Permission Model

**Definition**: Tổng hợp các rules và mechanisms để control database access. Bao gồm privileges, RLS policies, và authentication.

**Context**: Permission model phải be designed carefully và documented. It defines how access decisions are made.

**Related Terms**: Access Control, RLS Policy, GRANT

#### Permissive Policy

**Definition**: Default policy type in PostgreSQL. Multiple permissive policies use OR logic - row is accessible if ANY permissive policy allows.

**Context**: Most policies are permissive by default. Với OR semantics, be careful about combining permissive policies.

**Example**:
```sql
-- Permissive (default)
CREATE POLICY allow_all ON orders FOR SELECT USING (true);

-- With OR semantics:
-- Policy 1: USING (true) - allows everyone
-- Policy 2: USING (customer_id = auth.uid()) - allows owner
-- Result: Everyone can access because Policy 1 allows all
```

**Related Terms**: Restrictive Policy, RLS Policy, OR Semantics

#### pg_class

**Definition**: System catalog table chứa information về all tables, views, sequences, và other relations in the database.

**Context**: pg_class chứa RLS-related columns: relrowsecurity và relforcerowsecurity.

**Example**:
```sql
-- Check RLS status
SELECT relname, relrowsecurity, relforcerowsecurity
FROM pg_class
WHERE relkind = 'r';

-- Check for specific table
SELECT * FROM pg_class WHERE relname = 'orders';
```

**Related Terms**: pg_policies, System Catalog, RLS Status

#### pg_policies

**Definition**: PostgreSQL view cung cấp information về all RLS policies in the database, bao gồm policy conditions và target roles.

**Context**: pg_policies is essential for auditing và debugging RLS policies.

**Example**:
```sql
-- List all policies
SELECT * FROM pg_policies;

-- Policies for specific table
SELECT policyname, cmd, permissive, qual::text
FROM pg_policies
WHERE tablename = 'orders';

-- Check policy conditions
SELECT policyname, qual::text, with_check::text
FROM pg_policies
WHERE tablename = 'orders';
```

**Related Terms**: pg_class, RLS Policy, Policy Audit

#### Policy

**See**: RLS Policy

#### PostgreSQL

**Definition**: Advanced open-source relational database system known for extensibility, ACID compliance, và strong support for complex data types including JSONB.

**Context**: PostgreSQL introduced Row Level Security in version 9.5 và has continuously improved the feature since then.

**Related Terms**: Row Level Security, Database, Supabase

#### PUBLIC Role

**Definition**: Special pseudo-role representing everyone. Any permission granted to PUBLIC is available to all roles.

**Context**: Granting permissions to PUBLIC is a security anti-pattern. Best practice là revoke all PUBLIC grants và explicitly grant permissions.

**Example**:
```sql
-- WRONG: Grant to PUBLIC
GRANT SELECT ON orders TO PUBLIC;  -- Everyone can read!

-- CORRECT: Revoke PUBLIC and grant explicitly
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
GRANT SELECT ON orders TO authenticated;
```

**Related Terms**: GRANT, REVOKE, Least Privilege

### R

#### Restrictive Policy

**Definition**: Policy type where multiple policies use AND logic - row is accessible only if ALL restrictive policies allow.

**Context**: Restrictive policies are less common và used when you need AND semantics (all conditions must be true).

**Example**:
```sql
-- Two restrictive policies
CREATE POLICY require_auth ON orders
    FOR SELECT
    USING (true);

CREATE POLICY require_owner ON orders
    FOR SELECT
    USING (customer_id = auth.uid());

-- AND semantics: User must match owner
```

**Related Terms**: Permissive Policy, RLS Policy, AND Semantics

#### REVOKE

**Definition**: SQL command to remove privileges from roles. Used to implement least privilege và remove dangerous grants.

**Context**: REVOKE is often overlooked but critical for security. Always revoke PUBLIC grants và review default privileges.

**Example**:
```sql
-- Remove all PUBLIC grants
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM PUBLIC;

-- Revoke specific grant
REVOKE DELETE ON orders FROM authenticated;
```

**Related Terms**: GRANT, PUBLIC Role, Least Privilege

#### Role

**See**: Database Role

#### Row Level Security (RLS)

**Definition**: PostgreSQL feature cho phép kiểm soát truy cập ở cấp độ individual rows thay vì cấp độ table. Policies được attached to tables và evaluated for each row.

**Context**: RLS is critical component của database security, đặc biệt cho multi-tenant applications. Nó provides defense-in-depth by enforcing access control at database level.

**Example**:
```sql
-- Enable RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Create policy
CREATE POLICY orders_own ON orders
    FOR SELECT
    USING (customer_id = auth.uid());
```

**Related Terms**: RLS Policy, Row Security Filter, Defense in Depth

#### Row Security Filter

**Definition**: Internal PostgreSQL mechanism that applies RLS policy conditions to queries. Appears in EXPLAIN output.

**Context**: Row Security Filter là what actually filters rows. Understanding it helps diagnose RLS issues và performance problems.

**Example**:
```sql
EXPLAIN SELECT * FROM orders;

/*
Output:
Seq Scan on orders
  Filter: (customer_id = 'xxx')
  Row Security Filter: (customer_id = 'xxx')
         ^^^^^^^^^^^^
         This shows RLS is applied
*/
```

**Related Terms**: EXPLAIN, RLS Policy, Query Performance

### S

#### SECURITY DEFINER

**Definition**: Function attribute causes function to execute with the privileges of the user who created it, not the calling user. Can bypass RLS.

**Context**: SECURITY DEFINER functions are powerful but dangerous. Always include permission checks inside SECURITY DEFINER functions.

**Example**:
```sql
-- SECURITY DEFINER function
CREATE OR REPLACE FUNCTION admin_only()
RETURNS SETOF admin_data AS $$
BEGIN
    -- Always check permissions!
    IF NOT is_admin() THEN
        RAISE EXCEPTION 'Unauthorized';
    END IF;
    RETURN QUERY SELECT * FROM admin_data;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

**Related Terms**: SECURITY INVOKER, Bypass RLS, Function Security

#### SECURITY INVOKER

**Definition**: Function attribute causes function to execute with the privileges of the calling user. This is the default behavior.

**Context**: SECURITY INVOKER is safer than SECURITY DEFINER. Use it by default và only switch to SECURITY DEFINER when necessary.

**Related Terms**: SECURITY DEFINER, Function Security

#### SELECT Policy

**Definition**: RLS policy type that controls read access. Uses USING clause to determine which rows are visible.

**Context**: SELECT policies are most commonly used. They control which rows a user can see in SELECT queries.

**Example**:
```sql
CREATE POLICY orders_select ON orders
    FOR SELECT
    USING (customer_id = auth.uid());
```

**Related Terms**: RLS Policy, USING Clause, SELECT Command

#### Sequence

**Definition**: Database object that generates auto-incrementing numbers. Often used for primary keys.

**Context**: Sequences may need special handling với RLS. Ensure users can still INSERT rows with sequence-generated IDs.

**Example**:
```sql
CREATE SEQUENCE orders_id_seq;

CREATE TABLE orders (
    id BIGINT DEFAULT nextval('orders_id_seq') PRIMARY KEY,
    customer_id UUID,
    total DECIMAL
);

-- Grant usage on sequence
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO authenticated;
```

**Related Terms**: Primary Key, GRANT, Auto-increment

#### Session Settings

**Definition**: PostgreSQL configuration parameters that persist for the duration of a database session. Used for tenant context, custom data, etc.

**Context**: Session settings enable passing dynamic data to RLS policies. Common use cases: multi-tenant isolation, feature flags.

**Example**:
```sql
-- Set tenant context
SET app.current_tenant_id = 'tenant-123';

-- Get in policy
SELECT current_setting('app.current_tenant_id', true);

-- Reset
RESET app.current_tenant_id;
```

**Related Terms**: Multi-Tenant, current_setting, set_config

#### SET ROLE

**Definition**: SQL command to change the current user context within a session. Affects which RLS policies apply.

**Context**: SET ROLE is used in testing và for switching user contexts. The new role must have been granted to the current user.

**Example**:
```sql
-- Set role for testing
SET ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub":"user-123"}';

-- Now RLS applies as if we're user-123
SELECT * FROM orders;  -- Only user-123's orders

-- Reset role
RESET ROLE;
```

**Related Terms**: Database Role, RLS Policy, Authentication

#### Soft Delete

**Definition**: Pattern where records are marked as deleted (via deleted_at column) rather than physically removed. RLS policies typically filter out soft-deleted records.

**Context**: Soft delete enables data recovery và auditing. RLS should exclude soft-deleted rows from normal queries.

**Example**:
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    title TEXT,
    deleted_at TIMESTAMPTZ  -- NULL = not deleted
);

CREATE POLICY active_documents ON documents
    FOR SELECT
    USING (
        deleted_at IS NULL
        AND owner_id = auth.uid()
    );
```

**Related Terms**: RLS Policy, deleted_at, Data Recovery

#### STABLE Function

**Definition**: Function volatility category indicating function value is stable within a query (same arguments = same result) but may change across statements.

**Context**: Mark RLS helper functions as STABLE to enable query optimization. This allows PostgreSQL to cache function results within a query.

**Example**:
```sql
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM user_roles
        WHERE user_id = auth.uid()
        AND role = 'admin'
    );
END;
$$ LANGUAGE plpgsql STABLE;  -- Can be cached
```

**Related Terms**: IMMUTABLE, VOLATILE, Function Optimization

#### Supabase

**Definition**: Open-source Firebase alternative built on PostgreSQL. Provides authentication, real-time subscriptions, và automatic RLS configuration.

**Context**: Supabase makes RLS easy by providing auth.uid() và auth.jwt() helper functions. All Supabase tables have RLS enabled by default.

**Example**:
```sql
-- Supabase RLS policy
CREATE POLICY "Users can view own data" ON profiles
    FOR SELECT
    USING (auth.uid() = user_id);
```

**Related Terms**: PostgreSQL, auth.uid(), Firebase Alternative

### T

#### Tenant Isolation

**Definition**: Cơ chế đảm bảo data của mỗi tenant trong multi-tenant application được completely separate từ other tenants.

**Context**: Tenant isolation là critical security requirement. RLS policies must ensure zero cross-tenant data access.

**Example**:
```sql
-- Tenant isolation via RLS
CREATE POLICY tenant_isolation ON tenant_data
    FOR ALL
    USING (
        tenant_id = current_setting('app.current_tenant_id')::UUID
        OR is_admin()
    )
    WITH CHECK (
        tenant_id = current_setting('app.current_tenant_id')::UUID
    );
```

**Related Terms**: Multi-Tenant, RLS Policy, Data Isolation

#### Transaction

**Definition**: Atomic unit of work in PostgreSQL. RLS policies are evaluated within transaction context.

**Context**: Session settings set within a transaction are automatically rolled back when transaction aborts, helping maintain security.

**Example**:
```sql
BEGIN;

-- Set context for transaction
SET LOCAL app.current_tenant_id = 'tenant-123';

-- All queries in transaction use this tenant
SELECT * FROM orders;

COMMIT;  -- Context is automatically reset
```

**Related Terms**: Session Settings, SET LOCAL, Transaction Isolation

### U

#### Unauthorized Access

**Definition**: Truy cập vào data mà user không có permission. RLS prevents unauthorized access by filtering rows.

**Context**: Unauthorized access prevention là primary purpose của RLS. Well-designed policies ensure no user can access data they shouldn't.

**Related Terms**: RLS Policy, Access Control, Data Breach

#### USING Clause

**Definition**: RLS policy clause xác định which existing rows are visible or modifiable. Used for SELECT, UPDATE, DELETE.

**Context**: USING clause evaluates to boolean for each row. If true, row is accessible. If false, row is hidden.

**Example**:
```sql
CREATE POLICY orders_own ON orders
    FOR SELECT
    USING (customer_id = auth.uid());
    --              ^^^^^^^^^^^^^^^^
    --              USING clause: true = row visible
```

**Related Terms**: WITH CHECK, RLS Policy, Row Security Filter

#### User-Owned Data

**Definition**: Pattern where each row belongs to a specific user (via user_id column), và access is controlled by ownership.

**Context**: User-owned data là simplest RLS pattern. Each user can only see/modify rows they own.

**Example**:
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    title TEXT
);

CREATE POLICY user_own ON documents
    FOR ALL
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());
```

**Related Terms**: Ownership Model, RLS Policy, auth.uid()

### V

#### View

**Definition**: Virtual table based on a query. Views can have RLS policies applied to them, providing column-level security.

**Context**: Views are often used with RLS to control which columns are visible or to combine multiple tables with different policies.

**Example**:
```sql
-- View that excludes sensitive columns
CREATE VIEW public_profiles AS
SELECT id, name, avatar_url
FROM profiles;

-- RLS on view
ALTER TABLE public_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY public_profiles_view ON public_profiles
    FOR SELECT USING (true);
```

**Related Terms**: Column-level Security, RLS Policy, Materialized View

### W

#### WITH CHECK

**Definition**: RLS policy clause xác định constraints cho new rows being inserted or updated. Only used for INSERT và UPDATE.

**Context**: WITH CHECK ensures that when data is inserted/updated, it satisfies the policy. If check fails, operation is rejected.

**Example**:
```sql
CREATE POLICY orders_insert ON orders
    FOR INSERT
    WITH CHECK (customer_id = auth.uid());
    --                        ^^^^^^^^^^^^^^^^
    --                        Must match for INSERT to succeed

-- UPDATE with both USING and WITH CHECK
CREATE POLICY orders_update ON orders
    FOR UPDATE
    USING (customer_id = auth.uid())       -- Can only UPDATE rows you own
    WITH CHECK (customer_id = auth.uid()); -- INSERT must have your customer_id
```

**Related Terms**: USING Clause, RLS Policy, INSERT Policy

## Cross-Reference Index

### Terms by Category

**Policy Components**:
- USING Clause, WITH CHECK, Command, Row Security Filter

**Security Concepts**:
- Access Control, Default Deny, Least Privilege, Unauthorized Access

**Roles and Users**:
- Database Role, PUBLIC Role, SET ROLE, Ownership Model

**Performance**:
- Index, EXPLAIN, STABLE Function

**Multi-Tenant**:
- Multi-Tenant, Tenant Isolation, Session Settings

**Supabase**:
- Supabase, auth.uid(), JWT

**Advanced**:
- SECURITY DEFINER, Column-level Security, Soft Delete, View

## References

- [PostgreSQL Row Level Security Documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [PostgreSQL pg_policies View](https://www.postgresql.org/docs/current/view-pg-policies.html)
- [Supabase RLS Documentation](https://supabase.com/docs/guides/auth/row-level-security)
- [OWASP Access Control Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html)
