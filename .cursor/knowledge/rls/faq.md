# Row Level Security FAQ - Câu Hỏi Thường Gặp

## Giới thiệu

Tài liệu này trả lời các câu hỏi thường gặp về Row Level Security (RLS) trong PostgreSQL và Supabase.

---

## 1. Fundamentals Questions

### Q1: RLS là gì và nó hoạt động như thế nào?

**A:** Row Level Security (RLS) là cơ chế bảo mật của PostgreSQL cho phép kiểm soát truy cập ở cấp độ row thay vì cấp độ table.

**Cách hoạt động:**
```sql
-- 1. Enable RLS trên table
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- 2. Tạo policy
CREATE POLICY user_orders ON orders
FOR SELECT
USING (user_id = auth.uid());

-- 3. Khi user query, PostgreSQL tự động thêm filter
-- Original: SELECT * FROM orders
-- Actual:  SELECT * FROM orders WHERE user_id = 'current-user-id'
```

**Luồng xử lý:**
```
User Query → PostgreSQL Parser → RLS Evaluator → Policy Check → Filter Applied → Results
```

---

### Q2: Sự khác biệt giữa USING và WITH CHECK là gì?

**A:** 

| Clause | Áp dụng cho | Mục đích |
|--------|--------------|----------|
| USING | SELECT, UPDATE, DELETE | Xác định rows nào visible/modifiable |
| WITH CHECK | INSERT, UPDATE | Xác định rows mới phải thỏa mãn điều kiện gì |

```sql
-- USING: Kiểm tra rows hiện có
CREATE POLICY update_own_data ON user_data
FOR UPDATE
USING (user_id = auth.uid());  -- Chỉ cho phép UPDATE rows của mình

-- WITH CHECK: Kiểm tra data mới được insert/update
CREATE POLICY update_own_data ON user_data
FOR UPDATE
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());  -- user_id phải là của mình

-- Ví dụ khác:
-- UPDATE chỉ cho phép với rows của mình
-- INSERT chỉ cho phép insert với user_id của mình
```

---

### Q3: Default Deny nghĩa là gì?

**A:** Default Deny có nghĩa là khi RLS được enable nhưng không có policies nào, không ai có thể truy cập table.

```sql
-- Enable RLS without policies
ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;

-- Mọi query đều trả về empty result
SELECT * FROM sensitive_data;  -- Returns: (empty)

-- Phải tạo policy để cho phép access
CREATE POLICY access_sensitive ON sensitive_data
FOR SELECT
USING (true);  -- Cho phép tất cả authenticated users
```

---

## 2. Supabase-Specific Questions

### Q4: Làm thế nào để lấy user ID trong RLS policies?

**A:** Supabase cung cấp `auth.uid()` function:

```sql
-- Basic usage
CREATE POLICY select_own ON user_data
FOR SELECT
USING (user_id = auth.uid());

-- Access JWT claims
CREATE POLICY admin_access ON admin_data
FOR SELECT
USING (
    (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
);

-- Access email
CREATE POLICY email_match ON user_settings
FOR SELECT
USING (
    email = auth.jwt() ->> 'email'
);
```

---

### Q5: Làm thế nào để bypass RLS trong Supabase?

**A:** Có vài cách:

**Cách 1: Sử dụng service_role key**
```typescript
// service_role key bypasses ALL RLS
// CHỉ sử dụng trong server-side code
const supabaseAdmin = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY  // Never expose this!
);
```

**Cách 2: Tạo SECURITY DEFINER function**
```sql
-- SECURITY DEFINER bypasses RLS
CREATE OR REPLACE FUNCTION get_all_data()
RETURNS SETOF data AS $$
BEGIN
    RETURN QUERY SELECT * FROM data;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
-- Warning: This bypasses ALL RLS!
```

**Cách 3: Tạo role với BYPASSRLS**
```sql
-- Tạo role có BYPASSRLS
CREATE ROLE admin_with_bypass BYPASSRLS;

-- Gán cho user khi cần
GRANT admin_with_bypass TO admin_user;
```

---

### Q6: Tại sao auth.uid() trả về NULL?

**A:** Có thể do:

**Nguyên nhân 1: Không có JWT token**
```sql
-- Chạy query mà không có Authorization header
SELECT auth.uid();  -- Returns: NULL
```

**Nguyên nhân 2: JWT không hợp lệ**
```sql
-- Token hết hạn hoặc sai signature
SELECT auth.uid();  -- Returns: NULL
```

**Nguyên nhân 3: Role không phải authenticated**
```sql
-- Sử dụng anon key hoặc không set role
SET ROLE anon;
SELECT auth.uid();  -- Returns: NULL
```

**Giải pháp:**
```sql
-- Kiểm tra NULL trước khi sử dụng
CREATE POLICY safe_select ON user_data
FOR SELECT
USING (
    auth.uid() IS NOT NULL  -- Check trước
    AND user_id = auth.uid()
);
```

---

## 3. Security Questions

### Q7: RLS có thể bị bypass không?

**A:** Có, có vài cách:

**Cách 1: BYPASSRLS role**
```sql
-- Role có BYPASSRLS attribute sẽ bypass policies
SELECT rolbypassrls FROM pg_roles WHERE rolname = 'service_role';
-- Result: t (true)

-- CHỉ nên dùng cho service accounts
```

**Cách 2: SUPERUSER**
```sql
-- PostgreSQL superuser bypasses RLS
-- KHÔNG nên dùng superuser cho application
```

**Cách 3: SECURITY DEFINER functions**
```sql
-- Function với SECURITY DEFINER có thể bypass RLS
CREATE FUNCTION bypass_all()
RETURNS SETOF data AS $$
BEGIN
    RETURN QUERY SELECT * FROM data;  -- No RLS check!
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

**Best Practice:**
```sql
-- Luôn verify permissions trong SECURITY DEFINER functions
CREATE FUNCTION safe_admin_data()
RETURNS SETOF data AS $$
BEGIN
    -- Check nếu caller là admin
    IF NOT is_admin() THEN
        RAISE EXCEPTION 'Unauthorized';
    END IF;
    
    RETURN QUERY SELECT * FROM data;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

---

### Q8: Làm thế nào để implement multi-tenant với RLS?

**A:** Có nhiều cách:

**Cách 1: Tenant ID in JWT**
```sql
-- 1. Store tenant_id in JWT when creating token
-- JWT payload: { "sub": "user-id", "tenant_id": "tenant-id" }

-- 2. Tạo function để lấy tenant_id
CREATE OR REPLACE FUNCTION auth.tenant_id()
RETURNS UUID AS $$
BEGIN
    RETURN NULLIF(
        current_setting('request.jwt.claims', true)::jsonb->>'tenant_id',
        ''
    )::UUID;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER STABLE;

-- 3. Policy
CREATE POLICY tenant_isolation ON tenant_data
FOR ALL
USING (tenant_id = auth.tenant_id())
WITH CHECK (tenant_id = auth.tenant_id());
```

**Cách 2: Tenant membership table**
```sql
-- 1. Tenant membership table
CREATE TABLE user_tenants (
    user_id UUID REFERENCES auth.users(id),
    tenant_id UUID REFERENCES tenants(id),
    PRIMARY KEY (user_id, tenant_id)
);

-- 2. Policy
CREATE POLICY tenant_access ON tenant_data
FOR SELECT
USING (
    tenant_id IN (
        SELECT tenant_id FROM user_tenants WHERE user_id = auth.uid()
    )
);
```

---

### Q9: RLS có ảnh hưởng đến performance không?

**A:** Có, nhưng có thể tối ưu:

**Performance impact:**
```sql
-- RLS thêm filter vào query plan
EXPLAIN SELECT * FROM orders WHERE status = 'pending';

-- Output:
/*
Seq Scan on orders
  Filter: (user_id = 'xxx' AND status = 'pending')
  Row Security Filter: (user_id = 'xxx')
*/
```

**Optimization:**
```sql
-- 1. Index on policy columns
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- 2. Covering index
CREATE INDEX idx_orders_covering ON orders(user_id)
INCLUDE (id, total, created_at);

-- 3. Partial index
CREATE INDEX idx_orders_pending ON orders(id)
WHERE status = 'pending';

-- 4. Simplify policy logic
-- Bad: Complex nested subqueries
-- Good: Simple direct comparisons
```

---

## 4. Policy Design Questions

### Q10: Nên tạo bao nhiêu policies trên một table?

**A:** Depends on access patterns:

**Tối ưu: 1-3 policies per operation type**
```sql
-- Good: Combined policies
CREATE POLICY select_data ON user_data
FOR SELECT
USING (
    user_id = auth.uid()  -- Owner
    OR is_public = true   -- Public
    OR team_id IN (SELECT team_id FROM team_members WHERE user_id = auth.uid())  -- Team
);

-- Bad: Too many granular policies
CREATE POLICY select_own ON user_data FOR SELECT USING (user_id = auth.uid());
CREATE POLICY select_public ON user_data FOR SELECT USING (is_public = true);
CREATE POLICY select_team ON user_data FOR SELECT USING (...);
```

**Khi nào cần nhiều policies:**
```sql
-- Khi operations có different logic
CREATE POLICY select_own ON user_data FOR SELECT USING (user_id = auth.uid());
CREATE POLICY update_own ON user_data FOR UPDATE USING (user_id = auth.uid()) 
    WITH CHECK (user_id = auth.uid());
CREATE POLICY delete_admin ON user_data FOR DELETE USING (is_admin() = true);
```

---

### Q11: Làm thế nào để test RLS policies?

**A:** Sử dụng SET ROLE và SET LOCAL:

```sql
-- Test 1: Regular user
SET ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub":"user-uuid","role":"authenticated"}';
SELECT * FROM user_data;  -- Should see only own data

-- Test 2: Admin user
SET LOCAL request.jwt.claims = '{"sub":"admin-uuid","role":"admin","app_metadata":{"role":"admin"}}';
SELECT * FROM admin_data;  -- Should see all data

-- Test 3: Unauthenticated
RESET ROLE;
SELECT * FROM user_data;  -- Should return empty or error

-- Test 4: Check query plan
EXPLAIN (ANALYZE, COSTS, VERBOSE) SELECT * FROM user_data;
```

---

### Q12: Có thể disable RLS tạm thời không?

**A:** Có:

```sql
-- Disable RLS for session
SET row_security = off;
SELECT * FROM user_data;  -- No RLS check

-- Disable RLS for table
ALTER TABLE user_data DISABLE ROW LEVEL SECURITY;

-- Warning: This bypasses ALL RLS on this table!
-- Only use for debugging/maintenance

-- Re-enable
ALTER TABLE user_data ENABLE ROW LEVEL SECURITY;
```

**Warning:** Never disable RLS in production unless absolutely necessary and for shortest time possible.

---

## 5. Troubleshooting Questions

### Q13: Query không trả về kết quả, có thể do đâu?

**A:** Kiểm tra theo thứ tự:

**1. RLS enabled?**
```sql
SELECT relrowsecurity FROM pg_class WHERE relname = 'your_table';
-- Must be true
```

**2. Policies tồn tại?**
```sql
SELECT * FROM pg_policies WHERE tablename = 'your_table';
-- Must have at least one policy for your operation
```

**3. auth.uid() có giá trị?**
```sql
SELECT auth.uid();
-- Must return UUID, not NULL
```

**4. Policy condition đúng?**
```sql
-- Test với direct query
SET ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub":"test-uuid"}';
EXPLAIN SELECT * FROM your_table;
-- Check if Row Security Filter appears
```

---

### Q14: Có thể debug RLS policies không?

**A:** Có:

**1. EXPLAIN ANALYZE**
```sql
EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS)
SELECT * FROM user_data WHERE id = 'some-id';
```

**2. pg_policies view**
```sql
SELECT 
    policyname,
    cmd,
    permissive,
    qual::text AS using_condition,
    with_check::text AS check_condition
FROM pg_policies
WHERE tablename = 'user_data';
```

**3. Test function**
```sql
CREATE OR REPLACE FUNCTION debug_rls()
RETURNS TABLE (
    current_user_id UUID,
    jwt_claims JSONB,
    role TEXT
) AS $$
BEGIN
    current_user_id := auth.uid();
    jwt_claims := auth.jwt();
    role := auth.role();
    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM debug_rls();
```

---

### Q15: RLS có hoạt động với JOIN không?

**A:** Có:

```sql
-- RLS được áp dụng cho từng table trong JOIN
SELECT u.name, p.title
FROM users u
JOIN posts p ON u.id = p.user_id
WHERE u.id = auth.uid();

-- User chỉ thấy posts của mình vì:
-- 1. users table có RLS: u.id = auth.uid()
-- 2. posts table có RLS: p.user_id = auth.uid()

-- Cross-table access có thể tricky
CREATE POLICY team_posts ON posts
FOR SELECT
USING (
    user_id = auth.uid()  -- Own posts
    OR team_id IN (
        SELECT team_id FROM team_members WHERE user_id = auth.uid()
    )
);
```

---

## 6. Best Practices Questions

### Q16: Nên sử dụng role-based hay ownership-based access control?

**A:** Thường kết hợp cả hai:

```sql
-- Ownership-based: User owns the data
CREATE POLICY own_data ON user_data
FOR ALL
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

-- Role-based: User has specific role
CREATE POLICY admin_access ON admin_data
FOR ALL
USING (
    (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
);

-- Combined
CREATE POLICY combined_access ON project_data
FOR ALL
USING (
    owner_id = auth.uid()  -- Is owner
    OR (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'  -- Or admin
    OR project_id IN (
        SELECT project_id FROM project_members WHERE user_id = auth.uid()
    )
);
```

---

### Q17: Có nên sử dụng soft delete với RLS không?

**A:** Rất khuyến khích:

```sql
-- Schema
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    user_id UUID,
    title TEXT,
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS: Only show non-deleted
CREATE POLICY active_documents ON documents
FOR SELECT
USING (
    user_id = auth.uid()
    AND deleted_at IS NULL
);

-- Soft delete
CREATE OR REPLACE FUNCTION soft_delete_doc(doc_id UUID)
RETURNS VOID AS $$
BEGIN
    UPDATE documents 
    SET deleted_at = NOW() 
    WHERE id = doc_id AND user_id = auth.uid();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

---

### Q18: Khi nào nên sử dụng SECURITY DEFINER functions?

**A:** Chỉ khi cần bypass RLS một cách có kiểm soát:

```sql
-- Khi nào dùng:
-- 1. System operations cần bypass (audit logging)
-- 2. Admin tasks cần full access
-- 3. Background jobs

-- Ví dụ: Audit log (service_role inserts, bypasses RLS)
CREATE OR REPLACE FUNCTION log_action(...)
RETURNS VOID AS $$
BEGIN
    INSERT INTO audit_log (...) VALUES (...);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Always verify permissions!
CREATE OR REPLACE FUNCTION admin_only_data()
RETURNS SETOF sensitive_data AS $$
BEGIN
    IF NOT is_admin() THEN
        RAISE EXCEPTION 'Admin access required';
    END IF;
    RETURN QUERY SELECT * FROM sensitive_data;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```
