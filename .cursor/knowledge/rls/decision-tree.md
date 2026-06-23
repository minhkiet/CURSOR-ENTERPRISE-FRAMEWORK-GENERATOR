---
title: "RLS Decision Tree"
description: "Cây quyết định cho việc thiết kế và triển khai Row Level Security"
tags: ["rls", "postgres", "security", "decision-tree", "architecture", "database"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# RLS Decision Tree - Cây Quyết Định

## Overview

Việc thiết kế và triển khai Row Level Security (RLS) đòi hỏi nhiều quyết định quan trọng, từ việc xác định access model, đến việc chọn policy structure, và cuối cùng là implement và test. Tài liệu này cung cấp một decision tree toàn diện giúp developers navigate through các quyết định này một cách systematic và đưa ra choices phù hợp với requirements của hệ thống.

Decision tree được thiết kế theo logical flow từ design đến implementation. Mỗi decision point bao gồm các options, pros/cons của mỗi option, và recommendations dựa trên common scenarios.

## Purpose

Mục tiêu của decision tree này là cung cấp a structured approach để make RLS design decisions. Thay vì relying on ad-hoc decisions hoặc trial-and-error, developers có thể follow the tree để reach well-informed conclusions. Tree cũng serves as a documentation tool, capturing rationale behind design choices.

## Key Concepts

### Decision Types

**Architecture Decisions**: Những quyết định về cấu trúc tổng thể của RLS implementation, như access model và tenant isolation strategy.

**Policy Decisions**: Những quyết định về cách thiết kế và structure individual policies.

**Implementation Decisions**: Những quyết định về cách implement policies, bao gồm performance optimization và testing strategies.

### Decision Criteria

Mỗi decision point đánh giá các options dựa trên:
- Security: Mức độ bảo mật
- Performance: Tác động đến query performance
- Maintainability: Dễ dàng maintain và debug
- Complexity: Độ phức tạp của implementation

---

## 1. Access Model Decision Tree

### Primary Decision: What is the primary access model?

```
┌─────────────────────────────────────────────────────────────────┐
│              ACCESS MODEL DECISION TREE                               │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Is this user-owned data?          │
              │ (Each user owns their own rows)   │
              └─────────────────────────────────┘
                    │              │
                   [Yes]          [No]
                    │              │
                    ▼              ▼
         ┌─────────────────┐ ┌─────────────────────┐
         │ User Ownership │ │ Continue to next    │
         │ Model          │ │ question            │
         └─────────────────┘ └─────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Is this multi-tenant data?       │
              │ (Data belongs to organizations)  │
              └─────────────────────────────────┘
                    │              │
                   [Yes]          [No]
                    │              │
                    ▼              ▼
         ┌─────────────────┐ ┌─────────────────────┐
         │ Multi-Tenant    │ │ Public or Team      │
         │ Model           │ │ Shared Model        │
         └─────────────────┘ └─────────────────────┘
```

### Decision 1.1: User Ownership vs Multi-Tenant

**Question**: Should access be based on individual user ownership or organizational (tenant) ownership?

**Option A: User Ownership**
```
When to use:
• Users own their own data (documents, profiles, settings)
• No organizational hierarchy needed
• Simple ownership model
• Independent user accounts

Policy structure:
CREATE POLICY user_data ON user_data
    FOR ALL
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

Pros:
• Simple to implement
• Clear ownership model
• Easy to audit
• Minimal performance overhead

Cons:
• Doesn't scale well for team scenarios
• Requires separate mechanism for shared data
```

**Option B: Multi-Tenant**
```
When to use:
• Data belongs to organizations
• Users belong to organizations
• Need complete data isolation
• SaaS or B2B applications

Policy structure:
CREATE POLICY tenant_data ON tenant_data
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID)
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::UUID);

Pros:
• Complete data isolation
• Scalable for many tenants
• Natural organization boundary
• Compliance friendly (GDPR)

Cons:
• More complex to implement
• Requires tenant context management
• Cross-tenant queries impossible
```

---

## 2. RLS Policy Structure Decision Tree

### Primary Decision: How should policies be structured?

```
┌─────────────────────────────────────────────────────────────────┐
│              POLICY STRUCTURE DECISION TREE                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Do all operations need the same   │
              │ access rules?                    │
              └─────────────────────────────────┘
                    │              │
                   [Yes]          [No]
                    │              │
                    ▼              ▼
         ┌─────────────────┐ ┌─────────────────────┐
         │ Use FOR ALL     │ │ Use separate        │
         │ policy         │ │ policies per        │
         │                 │ │ operation           │
         └─────────────────┘ └─────────────────────┘
```

### Decision 2.1: Combined (ALL) vs Separate Policies

**Question**: Should you use one policy for ALL operations or separate policies per operation?

**Option A: Single FOR ALL Policy**

```sql
-- When to use:
-- • Same logic for SELECT, INSERT, UPDATE, DELETE
-- • Simple ownership model
-- • No need to differentiate access by operation

CREATE POLICY orders_all ON orders
    FOR ALL
    USING (
        customer_id = auth.uid()
        OR is_admin()
    )
    WITH CHECK (
        customer_id = auth.uid()
        OR is_admin()
    );

Pros:
• Easier to maintain
• Single place for logic
• Less chance of inconsistency
• Better overview of access

Cons:
• Can't differentiate by operation
• May be too permissive for some ops
• Less granular control
```

**Option B: Separate Policies Per Operation**

```sql
-- When to use:
-- • Different conditions for different operations
-- • INSERT has different requirements than SELECT
-- • Need to prevent certain operations entirely
-- • Audit requires granular policies

-- SELECT: Can view own orders or all (for admins)
CREATE POLICY orders_select ON orders
    FOR SELECT
    USING (
        customer_id = auth.uid()
        OR is_admin()
    );

-- INSERT: Can only create orders for self
CREATE POLICY orders_insert ON orders
    FOR INSERT
    WITH CHECK (customer_id = auth.uid());

-- UPDATE: Can update own, admins can update all
CREATE POLICY orders_update ON orders
    FOR UPDATE
    USING (
        customer_id = auth.uid()
        OR is_admin()
    )
    WITH CHECK (
        customer_id = auth.uid()
        OR is_admin()
    );

-- DELETE: Only admins can delete
CREATE POLICY orders_delete ON orders
    FOR DELETE
    USING (is_admin());

Pros:
• Granular control per operation
• Can completely block operations
• Better for security-sensitive apps
• Easier to audit specific operations

Cons:
• More policies to maintain
• Potential for policy conflicts
• Harder to get complete picture
```

**Decision Matrix**:

| Scenario | Recommended |
|----------|------------|
| Simple CRUD with same access | FOR ALL |
| Different access per operation | Separate policies |
| Some operations blocked | Separate policies |
| Admin needs full access, users limited | Separate policies |
| Read-heavy, write-restricted | Separate policies |

---

## 3. Authentication Integration Decision Tree

### Primary Decision: How to integrate authentication with RLS?

```
┌─────────────────────────────────────────────────────────────────┐
│              AUTHENTICATION INTEGRATION TREE                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ What authentication method?      │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [Supabase Auth]   [Custom JWT]   [Session-based]
           │              │              │
           ▼              ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │ auth.uid() │ │ auth.jwt()   │ │ custom    │
    │ auth.jwt() │ │ direct       │ │ function  │
    └─────────────┘ └──────────────┘ └────────────┘
```

### Decision 3.1: Auth.uid() vs Auth.jwt() vs Custom Function

**Question**: Which authentication integration method should you use?

**Option A: auth.uid() (Supabase)**

```sql
-- When to use:
-- • Using Supabase
-- • User ID is primary identifier
-- • Simple, straightforward access control

-- Basic usage
CREATE POLICY user_data ON user_data
    FOR ALL
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

-- Check if authenticated
CREATE POLICY public_data ON public_data
    FOR SELECT
    USING (auth.uid() IS NOT NULL);

Pros:
• Simplest implementation
• Always returns correct user ID
• Works seamlessly with Supabase
• Minimal configuration

Cons:
• Only works with Supabase
• Limited to user ID only
• Can't access custom claims without auth.jwt()
```

**Option B: auth.jwt() for Claims**

```sql
-- When to use:
-- • Need role information
-- • Custom metadata in JWT
-- • Tenant ID in token
-- • Complex claim-based access

-- Access role from JWT
CREATE POLICY admin_data ON admin_data
    FOR ALL
    USING (
        (auth.jwt()->'app_metadata'->>'role') = 'admin'
    );

-- Access tenant ID
CREATE POLICY tenant_data ON tenant_data
    FOR ALL
    USING (
        (auth.jwt()->>'tenant_id') = tenant_id::TEXT
    );

-- Combine with auth.uid()
CREATE POLICY user_data ON user_data
    FOR ALL
    USING (
        user_id = auth.uid()
        OR (auth.jwt()->'app_metadata'->>'role') = 'admin'
    );

Pros:
• Access to full JWT claims
• Role-based access control
• Custom metadata support
• Flexible

Cons:
• More complex policies
• Need to understand JWT structure
• Claims must be properly configured
```

**Option C: Custom Helper Functions**

```sql
-- When to use:
-- • Complex authentication logic
-- • Need to query database for permissions
-- • Role hierarchies
-- • Reusable across many policies

-- Helper function for role check
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

-- Helper function for team membership
CREATE OR REPLACE FUNCTION is_team_member(p_team_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM team_members
        WHERE team_id = p_team_id
        AND user_id = auth.uid()
    );
END;
$$ LANGUAGE plpgsql STABLE;

-- Use in policies
CREATE POLICY team_data ON team_data
    FOR SELECT
    USING (
        is_team_member(team_id)
        OR is_admin()
    );

Pros:
• Encapsulates complex logic
• Reusable across policies
• Easy to modify and test
• Can query database tables

Cons:
• Requires function creation
• Performance may vary
• Need to maintain functions
• Potential for errors in function logic
```

---

## 4. Multi-Tenant Isolation Decision Tree

### Primary Decision: How to implement tenant isolation?

```
┌─────────────────────────────────────────────────────────────────┐
│              MULTI-TENANT ISOLATION TREE                            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Tenant membership model?          │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [One tenant per  [Multiple tenants  [Both]
           user]            per user]
           │              │              │
           ▼              ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │Simple:      │ │Complex:     │ │Hybrid:    │
    │tenant_id in │ │Membership   │ │JWT for    │
    │user table   │ │table        │ │simple,   │
    │             │ │             │ │table for │
    │             │ │             │ │complex   │
    └─────────────┘ └──────────────┘ └────────────┘
```

### Decision 4.1: Simple vs Membership Table vs Hybrid

**Option A: JWT-Based (Simple)**

```sql
-- When to use:
-- • Users belong to exactly one tenant
-- • Tenants are static (no frequent changes)
-- • Performance is critical
-- • Simple tenant model

-- Store tenant_id in JWT
-- JWT payload: { "sub": "user-id", "tenant_id": "tenant-uuid" }

-- Function to get tenant from JWT
CREATE OR REPLACE FUNCTION auth.tenant_id()
RETURNS UUID AS $$
BEGIN
    RETURN NULLIF(
        current_setting('request.jwt.claims', true)::jsonb->>'tenant_id',
        ''
    )::UUID;
END;
$$ LANGUAGE plpgsql STABLE;

-- Policy using JWT tenant
CREATE POLICY tenant_data ON tenant_data
    FOR ALL
    USING (
        tenant_id = auth.tenant_id()
        OR is_admin()
    )
    WITH CHECK (
        tenant_id = auth.tenant_id()
    );

Pros:
• Fastest performance (no table lookup)
• Simple policy logic
• Stateless validation
• Minimal overhead

Cons:
• Can't support multi-tenant users easily
• Token must be refreshed for tenant changes
• Limited for complex hierarchies
• Token size grows with claims
```

**Option B: Membership Table**

```sql
-- When to use:
-- • Users can belong to multiple tenants
-- • Need to query tenant relationships
-- • Complex tenant hierarchies
-- • Dynamic tenant assignments

-- Membership table
CREATE TABLE user_tenants (
    user_id UUID REFERENCES auth.users(id),
    tenant_id UUID REFERENCES tenants(id),
    role TEXT DEFAULT 'member',
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, tenant_id)
);

CREATE INDEX idx_user_tenants_user ON user_tenants(user_id);
CREATE INDEX idx_user_tenants_tenant ON user_tenants(tenant_id);

-- Policy using membership table
CREATE POLICY tenant_data ON tenant_data
    FOR ALL
    USING (
        tenant_id IN (
            SELECT tenant_id FROM user_tenants WHERE user_id = auth.uid()
        )
        OR is_admin()
    )
    WITH CHECK (
        tenant_id IN (
            SELECT tenant_id FROM user_tenants WHERE user_id = auth.uid()
        )
    );

Pros:
• Supports multiple tenants per user
• Can query tenant relationships
• Flexible for hierarchies
• Easy to add/remove tenants

Cons:
• Extra table lookup per query
• Must maintain membership table
• Slightly more complex policies
• Potential performance impact
```

**Option C: Hybrid Approach**

```sql
-- When to use:
-- • Most users are single-tenant (use JWT)
-- • Some users are multi-tenant (use table)
-- • Balance performance and flexibility

-- Current tenant from JWT (common case)
CREATE OR REPLACE FUNCTION current_tenant_id()
RETURNS UUID AS $$
BEGIN
    -- First try JWT (most common)
    RETURN NULLIF(
        current_setting('request.jwt.claims', true)::jsonb->>'tenant_id',
        ''
    )::UUID;
END;
$$ LANGUAGE plpgsql STABLE;

-- Is multi-tenant user?
CREATE OR REPLACE FUNCTION is_multi_tenant_user()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN (
        SELECT COUNT(*) > 1
        FROM user_tenants
        WHERE user_id = auth.uid()
    );
END;
$$ LANGUAGE plpgsql STABLE;

-- Get all tenant IDs for current user
CREATE OR REPLACE FUNCTION user_tenant_ids()
RETURNS TABLE(tenant_id UUID) AS $$
BEGIN
    RETURN QUERY
    SELECT tenant_id FROM user_tenants WHERE user_id = auth.uid();
END;
$$ LANGUAGE plpgsql STABLE;

-- Hybrid policy
CREATE POLICY tenant_data ON tenant_data
    FOR SELECT
    USING (
        -- Single tenant: use JWT tenant_id
        tenant_id = current_tenant_id()
        -- Multi-tenant: use membership table
        OR tenant_id IN (SELECT tenant_id FROM user_tenant_ids())
        OR is_admin()
    );

Pros:
• Best performance for common case
• Flexible for edge cases
• Supports both models
• Gradual complexity

Cons:
• Most complex to implement
• Multiple code paths
• Harder to test
• Need clear documentation
```

---

## 5. Policy Condition Decision Tree

### Primary Decision: What type of condition should the policy use?

```
┌─────────────────────────────────────────────────────────────────┐
│              POLICY CONDITION DECISION TREE                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ What type of access control?     │
              └─────────────────────────────────┘
                    │              │              │              │
           ┌────────┴────────┐     │              │              │
          [Ownership]    [Role-Based]  [Team-Based]  [Public]
           │              │              │              │
           ▼              ▼              ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐ ┌────────────┐
    │user_id =   │ │Check role   │ │Team       │ │USING(true)│
    │auth.uid()  │ │in table or │ │membership │ │No filter  │
    │             │ │JWT         │ │check      │ │           │
    └─────────────┘ └──────────────┘ └────────────┘ └────────────┘
```

### Decision 5.1: Ownership vs Role vs Team vs Public

**Option A: Ownership-Based**

```sql
-- When to use:
-- • Clear owner for each row
-- • Owner has full access
-- • Simple permission model

CREATE POLICY user_documents ON documents
    FOR ALL
    USING (
        owner_id = auth.uid()
    )
    WITH CHECK (
        owner_id = auth.uid()
    );

-- With additional permissions
CREATE POLICY shared_documents ON documents
    FOR SELECT
    USING (
        owner_id = auth.uid()
        OR viewer_id = auth.uid()
        OR shared_with_user(auth.uid(), id)
    );
```

**Option B: Role-Based**

```sql
-- When to use:
-- • Access based on user role (admin, editor, viewer)
-- • Role stored in database or JWT
-- • Hierarchical permissions

-- From database
CREATE OR REPLACE FUNCTION user_role()
RETURNS TEXT AS $$
BEGIN
    RETURN (
        SELECT role FROM user_roles WHERE user_id = auth.uid()
    );
END;
$$ LANGUAGE plpgsql STABLE;

CREATE POLICY role_documents ON documents
    FOR ALL
    USING (
        user_role() IN ('admin', 'editor', 'owner')
        OR owner_id = auth.uid()
    );

-- From JWT
CREATE POLICY jwt_role_documents ON documents
    FOR SELECT
    USING (
        (auth.jwt()->'app_metadata'->>'role') IN ('admin', 'editor')
        OR owner_id = auth.uid()
    );
```

**Option C: Team-Based**

```sql
-- When to use:
-- • Data shared within teams/groups
-- • Users can belong to multiple teams
-- • Team collaboration scenarios

CREATE TABLE team_members (
    team_id UUID REFERENCES teams(id),
    user_id UUID REFERENCES auth.users(id),
    PRIMARY KEY (team_id, user_id)
);

CREATE TABLE team_data (
    id UUID PRIMARY KEY,
    team_id UUID REFERENCES teams(id),
    content TEXT
);

CREATE POLICY team_documents ON team_data
    FOR ALL
    USING (
        team_id IN (
            SELECT team_id FROM team_members WHERE user_id = auth.uid()
        )
    )
    WITH CHECK (
        team_id IN (
            SELECT team_id FROM team_members WHERE user_id = auth.uid()
        )
    );
```

**Option D: Public Access**

```sql
-- When to use:
-- • Data is intentionally public
-- • No authentication required
-- • Read-only access

CREATE POLICY public_products ON products
    FOR SELECT
    USING (is_published = true);

-- With optional authenticated enhancements
CREATE POLICY public_products_auth ON products
    FOR SELECT
    USING (
        is_published = true
        OR owner_id = auth.uid()  -- Owners see even unpublished
    );
```

---

## 6. Performance Optimization Decision Tree

### Primary Decision: How to optimize RLS performance?

```
┌─────────────────────────────────────────────────────────────────┐
│              PERFORMANCE OPTIMIZATION TREE                           │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Is query performance acceptable?│
              └─────────────────────────────────┘
                    │              │
                   [Yes]          [No]
                    │              │
                    ▼              ▼
              ┌─────────┐ ┌─────────────────────┐
              │ Done    │ │ Analyze query plan │
              └─────────┘ └─────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ What does EXPLAIN show?          │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [Seq Scan]   [Index Scan]  [Nested Loop]
           │              │              │
           ▼              ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │Add index   │ │Check index  │ │Optimize    │
    │on policy   │ │coverage     │ │subqueries  │
    │columns     │ │             │ │or simplify │
    └─────────────┘ └──────────────┘ └────────────┘
```

### Decision 6.1: Index Strategy

**Option A: Single Column Index**

```sql
-- When to use:
-- • Simple ownership check
-- • One column in policy
-- • Most common pattern

CREATE INDEX idx_orders_customer ON orders(customer_id);
```

**Option B: Composite Index**

```sql
-- When to use:
-- • Multiple columns in policy condition
-- • Common query patterns
-- • Range queries combined with equality

-- For policy: WHERE customer_id = auth.uid() AND status = 'pending'
CREATE INDEX idx_orders_customer_status
    ON orders(customer_id, status)
    WHERE status = 'pending';  -- Partial index
```

**Option C: Covering Index**

```sql
-- When to use:
-- • Frequently accessed columns not in policy
-- • Want to avoid table heap access
-- • SELECT * queries common

CREATE INDEX idx_orders_covering
    ON orders(customer_id)
    INCLUDE (id, total, created_at, status);
```

**Option D: Partial Index**

```sql
-- When to use:
-- • Policy only applies to subset of rows
-- • Want smaller, faster indexes
-- • Common filter conditions

-- For policy that only cares about active orders
CREATE INDEX idx_orders_active
    ON orders(customer_id)
    WHERE status IN ('pending', 'processing', 'shipped');
```

---

## 7. Testing Strategy Decision Tree

### Primary Decision: How to test RLS policies?

```
┌─────────────────────────────────────────────────────────────────┐
│              TESTING STRATEGY DECISION TREE                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ What aspects to test?            │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [Positive Tests] [Negative Tests]  [Edge Cases]
           │              │              │
           ▼              ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │User can    │ │User cannot  │ │NULL auth  │
    │access own  │ │access others│ │Test soft  │
    │data        │ │data         │ │delete etc │
    └─────────────┘ └──────────────┘ └────────────┘
```

### Decision 7.1: Testing Scenarios

**Positive Tests (User should have access)**

```sql
-- Test 1: Owner can access own data
SET ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub":"user-123"}';
SELECT * FROM orders WHERE customer_id = 'user-123';
-- Expected: Returns user's orders

-- Test 2: Admin can access all data
SET LOCAL request.jwt.claims = '{"sub":"admin-1","app_metadata":{"role":"admin"}}';
SELECT * FROM orders;
-- Expected: Returns all orders

-- Test 3: Team member can access team data
SET LOCAL request.jwt.claims = '{"sub":"user-456"}';
SELECT * FROM team_data WHERE team_id = 'team-1';
-- Expected: Returns team's data (if user is member)
```

**Negative Tests (User should be denied)**

```sql
-- Test 1: User cannot access other's data
SET ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub":"user-123"}';
SELECT * FROM orders WHERE customer_id = 'user-other';
-- Expected: Returns empty (denied by RLS)

-- Test 2: Non-admin cannot access admin data
SET LOCAL request.jwt.claims = '{"sub":"user-123","app_metadata":{"role":"user"}}';
SELECT * FROM admin_logs;
-- Expected: Returns empty

-- Test 3: Anonymous cannot access private data
RESET ROLE;
SELECT * FROM user_data;
-- Expected: Returns empty
```

**Edge Case Tests**

```sql
-- Test 1: NULL auth.uid()
SET ROLE authenticated;
-- Don't set JWT claims
SELECT * FROM orders;
-- Expected: Returns empty

-- Test 2: Invalid UUID
SET LOCAL request.jwt.claims = '{"sub":"not-a-uuid"}';
SELECT * FROM orders WHERE customer_id = 'not-a-uuid';
-- Expected: Proper error or empty

-- Test 3: Soft-deleted records
SET ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub":"user-123"}';
SELECT * FROM documents WHERE id = 'deleted-doc-id';
-- Expected: Returns empty (soft delete filter)

-- Test 4: Concurrent access
-- Run multiple sessions simultaneously
-- Expected: No data leaks between sessions
```

---

## 8. Deployment Strategy Decision Tree

### Primary Decision: How to deploy RLS policies?

```
┌─────────────────────────────────────────────────────────────────┐
│              DEPLOYMENT STRATEGY DECISION TREE                       │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Is this new table or existing?   │
              └─────────────────────────────────┘
                    │              │
                   [New]          [Existing]
                    │              │
                    ▼              ▼
         ┌─────────────────┐ ┌─────────────────────┐
         │Enable with      │ │Phased approach     │
         │table creation  │ │recommended         │
         └─────────────────┘ └─────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Data sensitivity level?           │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [High]        [Medium]  [Low]
           │              │              │
           ▼              ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │Migrate with │ │Add policies, │ │Add policies│
    │policies,   │ │monitor,     │ │and deploy  │
    │verify first │ │then enforce │ │            │
    └─────────────┘ └──────────────┘ └────────────┘
```

### Decision 8.1: Deployment Approaches

**Option A: Migration-Based (Recommended)**

```sql
-- migrations/001_create_tables.sql
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    customer_id UUID,
    total DECIMAL
);

-- migrations/002_enable_rls.sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

-- migrations/003_add_policies.sql
CREATE POLICY orders_select ON orders FOR SELECT USING (customer_id = auth.uid());
CREATE POLICY orders_insert ON orders FOR INSERT WITH CHECK (customer_id = auth.uid());

-- migrations/004_add_indexes.sql
CREATE INDEX idx_orders_customer ON orders(customer_id);
```

**Option B: Single Migration**

```sql
-- For new tables: all in one migration
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    customer_id UUID,
    total DECIMAL
);

ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

CREATE POLICY orders_all ON orders
    FOR ALL
    USING (customer_id = auth.uid())
    WITH CHECK (customer_id = auth.uid());

CREATE INDEX idx_orders_customer ON orders(customer_id);
```

**Option C: Phased Rollout (For Existing Data)**

```sql
-- Phase 1: Add policies but don't enforce
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
-- Don't add FORCE yet

CREATE POLICY orders_all ON orders
    FOR ALL
    USING (true)  -- Permissive for migration
    WITH CHECK (true);

-- Phase 2: Migrate data, set correct customer_id

-- Phase 3: Update policies to proper logic
DROP POLICY orders_all ON orders;

CREATE POLICY orders_all ON orders
    FOR ALL
    USING (customer_id = auth.uid())
    WITH CHECK (customer_id = auth.uid());

-- Phase 4: Force RLS
ALTER TABLE orders FORCE ROW LEVEL SECURITY;
```

---

## 9. Troubleshooting Decision Tree

### Primary Decision: What problem are you experiencing?

```
┌─────────────────────────────────────────────────────────────────┐
│              TROUBLESHOOTING DECISION TREE                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ What is the problem?              │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [No access]   [Too much access] [Performance]
           │              │              │
           ▼              ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │Check RLS   │ │Check policy  │ │Run EXPLAIN │
    │enabled?    │ │conditions    │ │Analyze     │
    │Check auth  │ │Check USING   │ │Check       │
    │Check NULL  │ │truth value   │ │indexes     │
    └─────────────┘ └──────────────┘ └────────────┘
```

### Decision 9.1: Access Issues

**Problem: User cannot access their own data**

```sql
-- Step 1: Check RLS is enabled
SELECT relrowsecurity FROM pg_class WHERE relname = 'orders';
-- If false: ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Step 2: Check policy exists
SELECT * FROM pg_policies WHERE tablename = 'orders' AND cmd = 'SELECT';
-- If empty: CREATE POLICY orders_select ON orders FOR SELECT USING (...);

-- Step 3: Check auth.uid() returns value
SELECT auth.uid();
-- If NULL: Check JWT is valid and role is authenticated

-- Step 4: Check policy condition
SET ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub":"user-123"}';
EXPLAIN SELECT * FROM orders WHERE customer_id = auth.uid();
-- Check Row Security Filter appears

-- Step 5: Test directly
SELECT * FROM orders WHERE customer_id = auth.uid();
-- Should return rows if user owns any
```

**Problem: User can see other users' data**

```sql
-- Step 1: Check policy logic
SELECT qual::text FROM pg_policies WHERE tablename = 'orders';

-- Step 2: Look for USING (true) or overly permissive conditions
-- If found: Fix policy with proper conditions

-- Step 3: Check if FORCE ROW LEVEL SECURITY is set
SELECT relforcerowsecurity FROM pg_class WHERE relname = 'orders';
-- If false: ALTER TABLE orders FORCE ROW LEVEL SECURITY;

-- Step 4: Verify ownership column matches
SELECT * FROM orders LIMIT 1;
-- Check customer_id matches actual owner
```

### Decision 9.2: Performance Issues

**Problem: Queries are slow with RLS**

```sql
-- Step 1: Run EXPLAIN ANALYZE
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT * FROM orders WHERE customer_id = auth.uid();

-- Step 2: Look for Seq Scan
-- If found: Create index on customer_id

-- Step 3: Check for Row Security Filter bottlenecks
-- Look for "Rows Removed by Filter:" with high numbers
-- This indicates policy is filtering many rows

-- Step 4: Check for nested loops
-- Consider simplifying policy or adding more indexes

-- Step 5: Test without RLS for comparison
SET row_security = off;
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 'test';
-- Compare timing with RLS on

-- Step 6: Optimize based on findings
CREATE INDEX idx_orders_customer ON orders(customer_id);
-- Or use partial indexes
-- Or denormalize for simpler policies
```

---

## 10. Quick Reference Decision Matrix

### Scenario-Based Recommendations

| Scenario | Access Model | Policy Structure | Auth Integration | Performance |
|----------|-------------|-------------------|------------------|-------------|
| User profiles | User ownership | FOR ALL | auth.uid() | Index on user_id |
| Multi-tenant SaaS | Multi-tenant | Separate policies | JWT tenant_id | Composite index |
| Team collaboration | Team-based | Separate policies | Helper functions | Index on team_id |
| Public + private | Hybrid | Separate policies | auth.uid() + public | Partial indexes |
| Admin + users | Role-based | Separate policies | JWT role + auth.uid() | Role check optimization |
| Time-limited access | Custom | Separate policies | Helper functions | Date index |

### Common Patterns Quick Reference

```sql
-- Pattern 1: User ownership
USING (user_id = auth.uid())

-- Pattern 2: Multi-tenant
USING (tenant_id = current_setting('app.current_tenant_id')::UUID)

-- Pattern 3: Role-based
USING (EXISTS (SELECT 1 FROM user_roles WHERE user_id = auth.uid() AND role = 'admin'))

-- Pattern 4: Team-based
USING (team_id IN (SELECT team_id FROM team_members WHERE user_id = auth.uid()))

-- Pattern 5: Combined
USING (
    user_id = auth.uid()
    OR is_admin()
    OR is_team_member(team_id)
)

-- Pattern 6: Time-limited
USING (
    owner_id = auth.uid()
    OR (valid_from <= NOW() AND (valid_until IS NULL OR valid_until > NOW()))
)
```

---

## References

- [PostgreSQL Row Level Security Documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [Supabase RLS Guidelines](https://supabase.com/docs/guides/auth/row-level-security)
- [PostgreSQL Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html)
- [Cursor Enterprise Framework Architecture](../rules/architecture.md)
- [Cursor Enterprise Framework Security](../rules/security.md)
- [Cursor Enterprise Framework Multi-Tenant](../rules/multi-tenant.md)
