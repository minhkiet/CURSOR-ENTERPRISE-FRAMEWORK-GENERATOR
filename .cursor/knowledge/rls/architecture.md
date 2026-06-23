# Row Level Security Architecture - Kiến Trúc RLS

## Giới thiệu

Tài liệu này mô tả kiến trúc chi tiết của Row Level Security (RLS) trong PostgreSQL và cách nó hoạt động trong hệ thống Supabase.

---

## 1. Tổng Quan Kiến Trúc RLS

### 1.1. Sơ Đồ Kiến Trúc

```
┌─────────────────────────────────────────────────────────────────┐
│                    RLS ARCHITECTURE OVERVIEW                     │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      Client Request                          ││
│  │  Authorization: Bearer eyJhbGci...                         ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Kong API Gateway                          ││
│  │  - Validates JWT Token                                      ││
│  │  - Extracts User Claims                                      ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                  PostgREST                                  ││
│  │  - Sets session variables                                    ││
│  │  - SET LOCAL request.jwt.claims = '...'                     ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                  PostgreSQL Engine                           ││
│  │  ┌───────────────────────────────────────────────────────┐ ││
│  │  │                    Query Parser                        │ ││
│  │  │  - Parses SQL query                                    │ ││
│  │  │  - Identifies target tables                            │ ││
│  │  └───────────────────────────────────────────────────────┘ ││
│  │                              │                              ││
│  │                              ▼                              ││
│  │  ┌───────────────────────────────────────────────────────┐ ││
│  │  │                  RLS Evaluator                       │ ││
│  │  │  - Checks if RLS enabled on table                    │ ││
│  │  │  - Retrieves policies                                  │ ││
│  │  │  - Evaluates USING expressions                         │ ││
│  │  │  - Applies Row Security Check to scan                 │ ││
│  │  └───────────────────────────────────────────────────────┘ ││
│  │                              │                              ││
│  │                              ▼                              ││
│  │  ┌───────────────────────────────────────────────────────┐ ││
│  │  │                    Query Executor                      │ ││
│  │  │  - Executes query with RLS filters                    │ ││
│  │  │  - Returns only authorized rows                        │ ││
│  │  └───────────────────────────────────────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 1.2. JWT Claims Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    JWT CLAIMS FLOW                                │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                 Original JWT Token                           ││
│  │  {                                                          ││
│  │    "sub": "user-uuid-123",                                 ││
│  │    "email": "user@example.com",                             ││
│  │    "role": "authenticated",                                 ││
│  │    "app_metadata": { "role": "admin" },                    ││
│  │    "user_metadata": { "name": "John" }                     ││
│  │  }                                                          ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                 Kong API Gateway                             ││
│  │  - Validates signature with Supabase signing key           ││
│  │  - Checks expiration                                        ││
│  │  - Passes claims to PostgREST                              ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                 PostgREST Configuration                      ││
│  │  jwt-secret = "your-jwt-secret"                           ││
│  │  request.jwt.claims header = "headers"                     ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                 PostgreSQL Session                           ││
│  │  SET LOCAL request.jwt.claims =                            ││
│  │  '{"sub":"user-uuid-123",...}'                             ││
│  │                                                              ││
│  │  Các functions có thể truy cập:                            ││
│  │  - auth.uid() → "user-uuid-123"                            ││
│  │  - auth.jwt() → Full JSON object                           ││
│  │  - auth.role() → "authenticated"                           ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. RLS Policy Evaluation

### 2.1. Policy Evaluation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    POLICY EVALUATION FLOW                         │
│                                                                 │
│  Query: SELECT * FROM orders WHERE status = 'pending';        │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Step 1: Check RLS Enabled                                   ││
│  │                                                              ││
│  │ SELECT relrowsecurity FROM pg_class WHERE relname = 'orders';││
│  │ Result: true (RLS is enabled)                                ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Step 2: Get Applicable Policies                              ││
│  │                                                              ││
│  │ SELECT policyname, cmd FROM pg_policies                     ││
│  │ WHERE tablename = 'orders' AND cmd IN ('SELECT', 'ALL');   ││
│  │                                                              ││
│  │ Policies found:                                              ││
│  │ - "user_orders_select" (SELECT)                             ││
│  │ - "admin_orders_select" (SELECT)                           ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Step 3: Combine Policies (OR)                              ││
│  │                                                              ││
│  │ Original: SELECT * FROM orders WHERE status = 'pending';   ││
│  │                                                              ││
│  │ Combined:                                                    ││
│  │ SELECT * FROM orders WHERE status = 'pending'                ││
│  │ AND (                                                          ││
│  │     (user_id = auth.uid())  -- policy 1                      ││
│  │     OR                                                          ││
│  │     ((auth.jwt()->'app_metadata'->>'role') = 'admin')        ││
│  │ );                                                            ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Step 4: Execute with Row Security Check                    ││
│  │                                                              ││
│  │ Final Query Plan:                                            ││
│  │ Seq Scan on orders                                           ││
│  │   Filter: (status = 'pending' AND (user_id = 'xxx' OR ...))││
│  │   Row Security Filter: (user_id = 'xxx' OR role = 'admin') ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 2.2. Multiple Policies Interaction

```sql
-- Tabela orders có 3 SELECT policies:
-- Policy A: Owner access
CREATE POLICY owner_orders ON orders FOR SELECT
USING (user_id = auth.uid());

-- Policy B: Team member access
CREATE POLICY team_orders ON orders FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM order_team_members
        WHERE order_id = orders.id
        AND user_id = auth.uid()
    )
);

-- Policy C: Admin access
CREATE POLICY admin_orders ON orders FOR SELECT
USING (
    (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
);

-- Combined (OR-ed):
SELECT * FROM orders WHERE status = 'pending'
AND (
    user_id = auth.uid()  -- Policy A
    OR EXISTS (SELECT 1 FROM order_team_members...)  -- Policy B  
    OR (auth.jwt()->'app_metadata'->>'role') = 'admin'  -- Policy C
);
```

---

## 3. RLS và PostgreSQL Architecture

### 3.1. System Catalogs

```
┌─────────────────────────────────────────────────────────────────┐
│                    RLS-RELATED SYSTEM CATALOGS                    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ pg_class - Table metadata                                   ││
│  │  ┌───────────────────────────────────────────────────────┐ ││
│  │  │ relname        │ orders                                │ ││
│  │  │ relrowsecurity │ true (RLS enabled)                   │ ││
│  │  │ relforcerowsecurity │ false (default)                │ ││
│  │  └───────────────────────────────────────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ pg_policy - Policy definitions                             ││
│  │  ┌───────────────────────────────────────────────────────┐ ││
│  │  │ polname        │ user_orders                           │ ││
│  │  │ polcmd         │ SELECT (r)                            │ ││
│  │  │ polpermissive  │ true (permissive mode)                │ ││
│  │  │ polroles       │ {authenticated}                       │ ││
│  │  └───────────────────────────────────────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ pg_authid - Authentication information                      ││
│  │  ┌───────────────────────────────────────────────────────┐ ││
│  │  │ rolname        │ authenticated                        │ ││
│  │  │ rolbypassrls   │ false                                │ ││
│  │  │ rolcanlogin    │ true                                 │ ││
│  │  └───────────────────────────────────────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 3.2. Query Rewriting

```sql
-- Original query từ application
SELECT id, total, status FROM orders WHERE status = 'pending';

-- PostgreSQL rewrites query với RLS:
-- (Pseudocode representation)

WITH row_security AS (
    SELECT id FROM orders
    WHERE 
        -- Policy: owner_orders (SELECT)
        user_id = current_setting('request.jwt.claims')::jsonb->>'sub'
        OR
        -- Policy: admin_orders (SELECT)
        (current_setting('request.jwt.claims')::jsonb->'app_metadata'->>'role') = 'admin'
)
SELECT id, total, status 
FROM orders 
WHERE status = 'pending'
AND id IN (SELECT id FROM row_security);
```

---

## 4. RLS Implementation Patterns

### 4.1. User Ownership Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER OWNERSHIP PATTERN                         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                         Table Structure                      ││
│  │                                                              ││
│  │  ┌─────────────────────────────────────────────────────┐  ││
│  │  │ CREATE TABLE user_data (                             │  ││
│  │  │     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),  │  ││
│  │  │     user_id UUID NOT NULL REFERENCES auth.users,   │  ││
│  │  │     data JSONB NOT NULL,                           │  ││
│  │  │     created_at TIMESTAMPTZ DEFAULT NOW()           │  ││
│  │  │ );                                                  │  ││
│  │  │                                                      │  ││
│  │  │ ALTER TABLE user_data ENABLE ROW LEVEL SECURITY;    │  ││
│  │  └─────────────────────────────────────────────────────┘  ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    RLS Policies                             ││
│  │                                                              ││
│  │  -- SELECT: User can read their own data                   ││
│  │  CREATE POLICY select_own_data ON user_data                ││
│  │  FOR SELECT USING (user_id = auth.uid());                  ││
│  │                                                              ││
│  │  -- INSERT: User can only insert with their own user_id    ││
│  │  CREATE POLICY insert_own_data ON user_data                 ││
│  │  FOR INSERT WITH CHECK (user_id = auth.uid());             ││
│  │                                                              ││
│  │  -- UPDATE: User can only update their own data            ││
│  │  CREATE POLICY update_own_data ON user_data                 ││
│  │  FOR UPDATE USING (user_id = auth.uid())                   ││
│  │  WITH CHECK (user_id = auth.uid());                        ││
│  │                                                              ││
│  │  -- DELETE: User can only delete their own data            ││
│  │  CREATE POLICY delete_own_data ON user_data                  ││
│  │  FOR DELETE USING (user_id = auth.uid());                  ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 4.2. Team/Group Access Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                    TEAM ACCESS PATTERN                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                         Schema                              ││
│  │                                                              ││
│  │  CREATE TABLE teams (                                       ││
│  │      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),      ││
│  │      name TEXT NOT NULL,                                    ││
│  │      created_at TIMESTAMPTZ DEFAULT NOW()                   ││
│  │  );                                                         ││
│  │                                                              ││
│  │  CREATE TABLE team_members (                                 ││
│  │      team_id UUID REFERENCES teams(id),                     ││
│  │      user_id UUID REFERENCES auth.users,                   ││
│  │      role TEXT DEFAULT 'member',                             ││
│  │      PRIMARY KEY (team_id, user_id)                        ││
│  │  );                                                         ││
│  │                                                              ││
│  │  CREATE TABLE team_documents (                              ││
│  │      id UUID PRIMARY KEY,                                    ││
│  │      team_id UUID REFERENCES teams(id),                     ││
│  │      title TEXT,                                            ││
│  │      content TEXT                                           ││
│  │  );                                                         ││
│  │                                                              ││
│  │  ALTER TABLE team_documents ENABLE ROW LEVEL SECURITY;      ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                 Policy Definition                           ││
│  │                                                              ││
│  │  CREATE POLICY team_doc_access ON team_documents           ││
│  │  FOR SELECT USING (                                         ││
│  │      team_id IN (                                          ││
│  │          SELECT team_id FROM team_members                  ││
│  │          WHERE user_id = auth.uid()                        ││
│  │      )                                                      ││
│  │  );                                                         ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 4.3. Multi-Tenant Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                    MULTI-TENANT PATTERN                          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                         Schema                              ││
│  │                                                              ││
│  │  CREATE TABLE tenants (                                    ││
│  │      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),        ││
│  │      name TEXT NOT NULL,                                    ││
│  │      plan TEXT DEFAULT 'free'                               ││
│  │  );                                                         ││
│  │                                                              ││
│  │  CREATE TABLE user_tenant_mapping (                         ││
│  │      user_id UUID REFERENCES auth.users,                   ││
│  │      tenant_id UUID REFERENCES tenants(id),                ││
│  │      is_owner BOOLEAN DEFAULT false,                       ││
│  │      PRIMARY KEY (user_id, tenant_id)                       ││
│  │  );                                                         ││
│  │                                                              ││
│  │  CREATE TABLE tenant_resources (                            ││
│  │      id UUID PRIMARY KEY,                                    ││
│  │      tenant_id UUID REFERENCES tenants(id),                 ││
│  │      data JSONB,                                            ││
│  │      owner_id UUID REFERENCES auth.users                    ││
│  │  );                                                         ││
│  │                                                              ││
│  │  ALTER TABLE tenant_resources ENABLE ROW LEVEL SECURITY;    ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              Shared Tenant Helper Function                   ││
│  │                                                              ││
│  │  CREATE OR REPLACE FUNCTION auth.tenant_id()                ││
│  │  RETURNS UUID AS $$                                          ││
│  │  SELECT tenant_id FROM user_tenant_mapping                   ││
│  │  WHERE user_id = auth.uid()                                  ││
│  │  LIMIT 1;                                                   ││
│  │  $$ LANGUAGE SQL SECURITY DEFINER STABLE;                    ││
│  │                                                              ││
│  │  -- Or using request.jwt.claims for faster access           ││
│  │  CREATE OR REPLACE FUNCTION auth.tenant_id()                 ││
│  │  RETURNS UUID AS $$                                          ││
│  │  SELECT NULLIF(                                             ││
│  │      (current_setting('request.jwt.claims', true)::jsonb    ││
│  │      -> 'app_metadata' ->> 'tenant_id'                      ││
│  │  , '')::UUID;                                               ││
│  │  $$ LANGUAGE SQL SECURITY DEFINER STABLE;                    ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                 Tenant Isolation Policy                      ││
│  │                                                              ││
│  │  CREATE POLICY tenant_isolation ON tenant_resources          ││
│  │  FOR ALL USING (                                            ││
│  │      tenant_id = auth.tenant_id()                          ││
│  │  ) WITH CHECK (                                             ││
│  │      tenant_id = auth.tenant_id()                          ││
│  │  );                                                         ││
│  │                                                              ││
│  │  CREATE INDEX idx_tenant_resources_tenant                   ││
│  │  ON tenant_resources(tenant_id);                            ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. RLS Security Considerations

### 5.1. BYPASSRLS Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    BYPASSRLS ARCHITECTURE                         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    PostgreSQL Roles                          ││
│  │                                                              ││
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   ││
│  │  │   anon      │  │authenticated │  │service_role │   ││
│  │  │             │  │              │  │              │   ││
│  │  │ bypassrls=no │  │ bypassrls=no │  │ bypassrls=yes│   ││
│  │  │ canlogin=yes│  │ canlogin=yes │  │ canlogin=no │   ││
│  │  └──────────────┘  └──────────────┘  └──────────────┘   ││
│  │                                                              ││
│  │  ┌──────────────────────────────────────────────────────┐  ││
│  │  │                  Admin (custom)                      │  ││
│  │  │  bypassrls=yes (if assigned)                        │  ││
│  │  │  Used for maintenance and migrations                  │  ││
│  │  └──────────────────────────────────────────────────────┘  ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Request Flow                              ││
│  │                                                              ││
│  │  Client Request → Kong → PostgREST                          ││
│  │                              │                              ││
│  │                              ▼                              ││
│  │  ┌──────────────────────────────────────────────────────┐  ││
│  │  │ JWT contains:                                         │  ││
│  │  │ - role: "authenticated"                               │  ││
│  │  │ - sub: "user-uuid-123"                               │  ││
│  │  │                                                       │  ││
│  │  │ PostgREST sets:                                       │  ││
│  │  │ SET LOCAL ROLE authenticated;                        │  ││
│  │  │ SET LOCAL request.jwt.claims = '{...}';             │  ││
│  │  └──────────────────────────────────────────────────────┘  ││
│  │                              │                              ││
│  │                              ▼                              ││
│  │  ┌──────────────────────────────────────────────────────┐  ││
│  │  │ PostgreSQL Query Execution                             │  ││
│  │  │ - Role: authenticated                                  │  ││
│  │  │ - bypassrls: false                                    │  ││
│  │  │ - RLS policies ARE enforced                           │  ││
│  │  └──────────────────────────────────────────────────────┘  ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 5.2. Security Barrier Views

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY BARRIER VIEW                         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Regular View (Vulnerable)                 ││
│  │                                                              ││
│  │  CREATE VIEW sensitive_data AS                               ││
│  │  SELECT                                                      ││
│  │      name,                                                   ││
│  │      secret_function(ssn) AS ssn_masked  -- Hàm thấy tất cả││
│  │  FROM raw_data;                                              ││
│  │                                                              ││
│  │  Problem: secret_function() được gọi cho tất cả rows,        ││
│  │  kể cả rows user không có quyền xem                          ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Security Barrier View                      ││
│  │                                                              ││
│  │  CREATE SECURITY BARRIER VIEW sensitive_data AS              ││
│  │  SELECT                                                      ││
│  │      name,                                                   ││
│  │      secret_function(ssn) AS ssn_masked  -- Chỉ gọi cho    ││
│  │  FROM raw_data WHERE authorized = true;  -- authorized rows  ││
│  │                                                              ││
│  │  RLS được apply TRƯỚC khi functions được gọi               ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Execution Order                            ││
│  │                                                              ││
│  │  1. Row Security Check (USING)                               ││
│  │  2. WITH CHECK (nếu có UPDATE/INSERT)                       ││
│  │  3. Security Barrier (ngăn function access unauthorized rows)││
│  │  4. User-Defined Functions                                    ││
│  │  5. Output columns                                          ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. RLS Performance Architecture

### 6.1. Index Strategy for RLS

```
┌─────────────────────────────────────────────────────────────────┐
│                    RLS INDEX STRATEGY                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Policy Column Index                       ││
│  │                                                              ││
│  │  -- Policy: user_id = auth.uid()                             ││
│  │  CREATE INDEX idx_user_data_user_id ON user_data(user_id);   ││
│  │                                                              ││
│  │  Query plan without index:                                   ││
│  │  Seq Scan on user_data (rows filtered by RLS)              ││
│  │                                                              ││
│  │  Query plan with index:                                       ││
│  │  Index Scan using idx_user_data_user_id                      ││
│  │  Index Cond: (user_id = 'xxx')                              ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Composite Index                          ││
│  │                                                              ││
│  │  -- Policy với nhiều điều kiện                              ││
│  │  CREATE POLICY status_filter ON orders                       ││
│  │  FOR SELECT USING (                                          ││
│  │      user_id = auth.uid()                                    ││
│  │      AND status = 'pending'                                  ││
│  │  );                                                          ││
│  │                                                              ││
│  │  CREATE INDEX idx_orders_user_status                         ││
│  │  ON orders(user_id, status);                                ││
│  │                                                              ││
│  │  Query plan:                                                 ││
│  │  Index Scan: user_id = 'xxx' AND status = 'pending'         ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Covering Index                           ││
│  │                                                              ││
│  │  -- Policy với SELECT cụ thể                                  ││
│  │  CREATE POLICY select_specific ON orders                     ││
│  │  FOR SELECT USING (user_id = auth.uid());                  ││
│  │                                                              ││
│  │  -- Query: SELECT id, total FROM orders WHERE user_id = ?   ││
│  │  CREATE INDEX idx_orders_covering                            ││
│  │  ON orders(user_id)                                          ││
│  │  INCLUDE (id, total);  -- Covering columns                 ││
│  │                                                              ││
│  │  Query plan: Index Only Scan (no table access needed)       ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 6.2. Query Plan Analysis

```sql
-- Analyze query plan với RLS
EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS)
SELECT id, total 
FROM orders 
WHERE status = 'pending'
ORDER BY created_at DESC
LIMIT 20;

-- Expected output:
/*
Limit  (cost=...)
  ->  Index Scan Backward using idx_orders_date on orders
      Output: id, total
      Index Cond: (status = 'pending')
      Filter: (user_id = 'a1b2c3d4-...'::uuid)  -- RLS Filter
      Rows Removed by Filter: 150
      Buffers: shared hit=45
Planning Time: 0.234 ms
Execution Time: 1.456 ms
*/

-- Performance warnings:
-- "Rows Removed by Filter" cao → Cần index tốt hơn
-- Seq Scan → Cần thêm index
-- Nested Loop → Có thể cần optimize
```

---

## 7. RLS Integration với Supabase

### 7.1. Supabase Auth Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUPABASE RLS FLOW                             │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Client App                              ││
│  │  const supabase = createClient(url, key);                  ││
│  │  await supabase.from('orders').select('*');             ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│  ┌───────────────────────────┼───────────────────────────────┐│
│  │ Request Headers:           │                               ││
│  │ apikey: eyJhbGci...       │                               ││
│  │ Authorization: Bearer ...  │                               ││
│  └───────────────────────────┼───────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Kong API Gateway                        ││
│  │  - Validates JWT (apikey = anon key)                       ││
│  │  - Validates JWT (Authorization header = user JWT)         ││
│  │  - Routes to PostgREST                                    ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    PostgREST                               ││
│  │                                                              ││
│  │  jwt-secret: "your-jwt-secret"                             ││
│  │                                                              ││
│  │  -- Extracts from JWT:                                      ││
│  │  SET LOCAL request.jwt.claims =                            ││
│  │    '{"sub":"user-uuid","role":"authenticated",...}';       ││
│  │                                                              ││
│  │  SET LOCAL request.jwt.role = 'authenticated';             ││
│  │                                                              ││
│  │  -- Role from apikey header:                                ││
│  │  SET LOCAL ROLE authenticated;                             ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    PostgreSQL                               ││
│  │                                                              ││
│  │  -- Functions access JWT claims:                             ││
│  │  auth.uid() → "user-uuid"                                   ││
│  │  auth.role() → "authenticated"                              ││
│  │  auth.jwt() → Full claims object                            ││
│  │                                                              ││
│  │  -- RLS Policy evaluation:                                  ││
│  │  USING (user_id = auth.uid())                               ││
│  │                                                              ││
│  │  Result: Only rows where user_id = 'user-uuid'             ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 7.2. Supabase RLS Setup

```sql
-- Supabase Database Migration Structure
-- migrations/20240101000000_enable_rls.sql

-- 1. Enable RLS on all user tables
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.likes ENABLE ROW LEVEL SECURITY;

-- 2. Create auth helper functions
CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM auth.users
        WHERE id = auth.uid()
        AND raw_user_meta_data->>'role' = 'admin'
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER STABLE;

-- 3. Create policies for profiles
CREATE POLICY "Users can view all profiles"
ON public.profiles FOR SELECT
USING (true);

CREATE POLICY "Users can update own profile"
ON public.profiles FOR UPDATE
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);

-- 4. Create policies for posts
CREATE POLICY "Published posts are public"
ON public.posts FOR SELECT
USING (published = true);

CREATE POLICY "Users can view own posts"
ON public.posts FOR SELECT
USING (user_id = auth.uid());

CREATE POLICY "Users can create posts"
ON public.posts FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own posts"
ON public.posts FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own posts"
ON public.posts FOR DELETE
USING (auth.uid() = user_id);

-- 5. Create policies for comments
CREATE POLICY "Users can view comments on accessible posts"
ON public.comments FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM public.posts p
        WHERE p.id = comments.post_id
        AND (p.published = true OR p.user_id = auth.uid())
    )
);

CREATE POLICY "Users can create comments"
ON public.comments FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own comments"
ON public.comments FOR DELETE
USING (auth.uid() = user_id);

-- 6. Create policies for likes
CREATE POLICY "Users can view likes"
ON public.likes FOR SELECT
USING (true);

CREATE POLICY "Users can like"
ON public.likes FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can unlike"
ON public.likes FOR DELETE
USING (auth.uid() = user_id);

-- 7. Indexes for performance
CREATE INDEX idx_profiles_id ON public.profiles(id);
CREATE INDEX idx_posts_user_id ON public.posts(user_id);
CREATE INDEX idx_posts_published ON public.posts(published) WHERE published = true;
CREATE INDEX idx_comments_post_id ON public.comments(post_id);
CREATE INDEX idx_likes_user_post ON public.likes(user_id, post_id);
```

---

## 8. Testing RLS Architecture

### 8.1. Test Environment Setup

```
┌─────────────────────────────────────────────────────────────────┐
│                    RLS TESTING ARCHITECTURE                      │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Local Supabase                           ││
│  │                                                              ││
│  │  supabase/start → Starts Docker containers                 ││
│  │  - PostgreSQL with RLS                                     ││
│  │  - PostgREST                                               ││
│  │  - GoTrue                                                  ││
│  │  - Kong                                                    ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Test Users                                ││
│  │                                                              ││
│  │  -- User A (regular user)                                   ││
│  │  INSERT INTO auth.users (id, email)                        ││
│  │  VALUES ('user-a-uuid', 'a@test.com');                       ││
│  │                                                              ││
│  │  -- User B (admin)                                          ││
│  │  INSERT INTO auth.users (id, email, raw_user_meta_data)      ││
│  │  VALUES ('user-b-uuid', 'b@test.com', '{"role":"admin"}'); ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Test Data                                 ││
│  │                                                              ││
│  │  -- Data owned by User A                                    ││
│  │  INSERT INTO user_data (id, user_id, data)                  ││
│  │  VALUES ('data-a', 'user-a-uuid', '{"test": true}');       ││
│  │                                                              ││
│  │  -- Data owned by User B                                     ││
│  │  INSERT INTO user_data (id, user_id, data)                  ││
│  │  VALUES ('data-b', 'user-b-uuid', '{"test": true}');       ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 8.2. Test Scenarios

```sql
-- Test 1: Regular user can only see own data
SET ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub":"user-a-uuid","role":"authenticated"}';

SELECT * FROM user_data;
-- Expected: Only data-a rows

-- Test 2: Admin can see all data (if admin policy exists)
SET ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub":"user-b-uuid","role":"admin","app_metadata":{"role":"admin"}}';

SELECT * FROM user_data;
-- Expected: All rows (if admin policy exists)

-- Test 3: INSERT with wrong user_id should fail
SET ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub":"user-a-uuid","role":"authenticated"}';

INSERT INTO user_data (id, user_id, data)
VALUES ('data-c', 'user-b-uuid', '{"test": true}');
-- Expected: Policy violation (WITH CHECK fails)

-- Test 4: Verify no data leakage
SET ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub":"user-a-uuid","role":"authenticated"}';

-- Should not see other users' data even with subqueries
SELECT * FROM user_data WHERE user_id IN (
    SELECT user_id FROM user_data
);
-- Expected: Only own data
```
