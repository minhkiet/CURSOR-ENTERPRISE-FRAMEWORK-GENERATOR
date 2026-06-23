# Row Level Security (RLS) Glossary - Từ Điển Thuật Ngữ

## Giới thiệu

Tài liệu này cung cấp định nghĩa chi tiết cho các thuật ngữ quan trọng liên quan đến Row Level Security (RLS) trong PostgreSQL và Supabase, được sử dụng trong Cursor Enterprise Framework.

---

## Danh Sách Thuật Ngữ

### 1. Row Level Security (RLS)

**Định nghĩa:** Row Level Security là cơ chế bảo mật của PostgreSQL cho phép kiểm soát truy cập ở cấp độ row thay vì cấp độ table. Mỗi row có thể có policies khác nhau dựa trên identity của user.

**Hoạt động:**
- Policies được áp dụng tự động cho tất cả queries
- Bypass possible với `SECURITY DEFINER` functions
- Sử dụng `auth.uid()` để lấy current user ID trong Supabase

** Ví dụ:**
```sql
-- Enable RLS trên table
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Tạo policy cho phép user chỉ xem orders của họ
CREATE POLICY user_orders ON orders
FOR SELECT
USING (user_id = auth.uid());
```

---

### 2. Policy

**Định nghĩa:** Policy là đối tượng database định nghĩa điều kiện để truy cập rows. Mỗi policy gắn với một table và một command type (SELECT, INSERT, UPDATE, DELETE).

**Các thành phần:**
- `ON table_name`: Table mà policy áp dụng
- `FOR command`: SELECT, INSERT, UPDATE, DELETE, ALL
- `USING`: Điều kiện để kiểm tra (cho SELECT, UPDATE, DELETE)
- `WITH CHECK`: Điều kiện để kiểm tra khi INSERT hoặc UPDATE

** Ví dụ:**
```sql
CREATE POLICY policy_name ON table_name
FOR SELECT
USING (condition)
WITH CHECK (condition);
```

---

### 3. auth.uid()

**Định nghĩa:** Hàm Supabase trả về UUID của user hiện tại đang thực hiện query. Được sử dụng trong RLS policies để xác định identity của user.

**Đặc điểm:**
- Trả về NULL nếu không có authenticated user
- Chỉ hoạt động trong context có JWT token
- Có thể sử dụng trong USING và WITH CHECK expressions

** Ví dụ:**
```sql
-- User chỉ có thể xem profile của chính họ
CREATE POLICY own_profiles ON profiles
FOR SELECT
USING (id = auth.uid());

-- User chỉ có thể update profile của chính họ
CREATE POLICY update_own_profile ON profiles
FOR UPDATE
USING (id = auth.uid())
WITH CHECK (id = auth.uid());
```

---

### 4. auth.jwt()

**Định nghĩa:** Hàm trả về JSON object chứa JWT claims của user hiện tại. Cho phép truy cập các metadata từ JWT token.

**Các claims có sẵn:**
- `sub`: User ID (same as auth.uid())
- `email`: User email
- `role`: User role (authenticated, anon, service_role)
- Custom claims từ app_metadata và user_metadata

** Ví dụ:**
```sql
-- Access custom role từ JWT
CREATE POLICY admin_only ON sensitive_data
FOR ALL
USING (
    (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
);

-- Access email từ JWT
CREATE POLICY email_access ON user_settings
FOR SELECT
USING (email = (auth.jwt() ->> 'email'));
```

---

### 5. SECURITY DEFINER

**Định nghĩa:** Attribute của function cho phép function thực thi với quyền của user đã tạo function đó, thay vì quyền của user gọi function.

**Khác biệt với SECURITY INVOKER (default):**
- SECURITY INVOKER: Function chạy với quyền của caller
- SECURITY DEFINER: Function chạy với quyền của definier

** Ví dụ:**
```sql
-- SECURITY INVOKER (default): Sử dụng quyền của caller
CREATE FUNCTION get_user_data()
RETURNS SETOF user_data AS $$
BEGIN
    RETURN QUERY SELECT * FROM user_data WHERE user_id = auth.uid();
END;
$$ LANGUAGE plpgsql;

-- SECURITY DEFINER: Bypass RLS
CREATE FUNCTION admin_get_all_users()
RETURNS SETOF users AS $$
BEGIN
    RETURN QUERY SELECT * FROM users;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Để tránh security issues, nên kết hợp với role check
CREATE FUNCTION admin_get_all_users()
RETURNS SETOF users AS $$
BEGIN
    -- Kiểm tra caller có phải là admin không
    IF (auth.jwt() -> 'app_metadata' ->> 'role') <> 'admin' THEN
        RAISE EXCEPTION 'Admin access required';
    END IF;
    RETURN QUERY SELECT * FROM users;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

---

### 6. USING Expression

**Định nghĩa:** Clause trong policy xác định điều kiện để rows được hiển thị trong SELECT, UPDATE, hoặc DELETE operations.

**Áp dụng cho:**
- SELECT: Xác định rows nào visible
- UPDATE: Xác định rows nào có thể được update
- DELETE: Xác định rows nào có thể được delete

** Ví dụ:**
```sql
-- SELECT: Chỉ hiển thị rows của user
CREATE POLICY select_own_data ON my_data
FOR SELECT
USING (owner_id = auth.uid());

-- UPDATE: Chỉ cho phép update rows của user
CREATE POLICY update_own_data ON my_data
FOR UPDATE
USING (owner_id = auth.uid());

-- DELETE: Chỉ cho phép delete rows của user
CREATE POLICY delete_own_data ON my_data
FOR DELETE
USING (owner_id = auth.uid());
```

---

### 7. WITH CHECK Expression

**Định nghĩa:** Clause trong policy xác định điều kiện mà data mới phải thỏa mãn khi INSERT hoặc UPDATE.

**Khác với USING:**
- USING: Kiểm tra rows hiện có (cho SELECT, UPDATE, DELETE)
- WITH CHECK: Kiểm tra rows mới được tạo/sửa (cho INSERT, UPDATE)

** Ví dụ:**
```sql
-- INSERT: Đảm bảo user chỉ có thể insert với user_id của họ
CREATE POLICY insert_own_data ON my_data
FOR INSERT
WITH CHECK (user_id = auth.uid());

-- UPDATE: Đảm bảo user chỉ có thể update user_id thành giá trị của họ
CREATE POLICY update_own_user_id ON my_data
FOR UPDATE
USING (user_id = auth.uid())  -- Có thể update rows của mình
WITH CHECK (user_id = auth.uid());  -- user_id phải là của mình

-- INSERT với giá trị mặc định
CREATE POLICY insert_with_default ON orders
FOR INSERT
WITH CHECK (
    user_id = auth.uid() OR 
    user_id IS NULL  -- Cho phép NULL nếu cần
);
```

---

### 8. bypassrls

**Định nghĩa:** Role attribute cho phép bypass RLS policies. Thường được gán cho service roles hoặc admin roles.

**Các roles có sẵn trong Supabase:**
- `anon`: Không bypass RLS
- `authenticated`: Không bypass RLS
- `service_role`: Có bypass RLS (bypassrls = true)

** Ví dụ:**
```sql
-- Kiểm tra xem role có bypassrls không
SELECT rolname, rolbypassrls
FROM pg_roles
WHERE rolname = 'service_role';

-- Gán bypassrls cho custom role
ALTER ROLE admin_user WITH BYPASSRLS;

-- Tạo role với bypassrls
CREATE ROLE admin WITH LOGIN BYPASSRLS PASSWORD 'strong_password';
```

---

### 9. PostgreSQL Roles

**Định nghĩa:** PostgreSQL sử dụng roles để quản lý quyền truy cập. Roles có thể là users hoặc groups.

**Các loại roles:**
- Login role: Có thể connect vào database
- Group role: Dùng để nhóm permissions
- SUPERUSER: Full privileges (tránh dùng)

** Ví dụ:**
```sql
-- Tạo login role
CREATE ROLE app_user WITH LOGIN PASSWORD 'secure_password';

-- Tạo group role
CREATE ROLE data_analyst;

-- Thêm user vào group
GRANT data_analyst TO app_user;

-- Gán permissions cho group
GRANT SELECT ON ALL TABLES IN SCHEMA public TO data_analyst;

-- Gán default role cho database
ALTER DATABASE mydb SET session_preload_libraries = 'pg_stat_statements';
```

---

### 10. pg_roles

**Định nghĩa:** System catalog chứa thông tin về tất cả database roles.

**Các columns quan trọng:**
- `rolname`: Tên role
- `rolsuper`: Có phải superuser không
- `rolbypassrls`: Có bypass RLS không
- `rolcanlogin`: Có thể login không
- `rolvaliduntil`: Thời hạn password

** Ví dụ:**
```sql
-- Xem tất cả roles
SELECT rolname, rolsuper, rolbypassrls, rolcanlogin
FROM pg_roles;

-- Xem role của current session
SELECT current_role, session_user, current_user;

-- Xem permissions của role
SELECT * FROM information_schema.role_table_grants
WHERE grantee = 'my_role';
```

---

### 11. FOR ALL Command

**Định nghĩa:** Command shorthand cho tất cả các operations (SELECT, INSERT, UPDATE, DELETE) trên một policy.

**Tương đương với:**
```sql
CREATE POLICY name ON table FOR ALL;

-- Tương đương với:
CREATE POLICY name ON table FOR SELECT USING (...) WITH CHECK (...);
CREATE POLICY name ON table FOR INSERT WITH CHECK (...);
CREATE POLICY name ON table FOR UPDATE USING (...) WITH CHECK (...);
CREATE POLICY name ON table FOR DELETE USING (...);
```

** Ví dụ:**
```sql
-- Policy đơn giản cho tất cả operations
CREATE POLICY admin_full_access ON admin_data
FOR ALL
USING (
    (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
)
WITH CHECK (
    (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
);
```

---

### 12. Role Inheritance

**Định nghĩa:** Cơ chế cho phép role nhận permissions từ role khác. Child roles tự động có các permissions của parent roles.

**Các loại:**
- INHERIT (default): Nhận tất cả privileges
- NOINHERIT: Phải SET ROLE để sử dụng parent permissions
- ADMIN OPTION: Có thể grant role cho others

** Ví dụ:**
```sql
-- Tạo hierarchy
CREATE ROLE manager;
CREATE ROLE team_lead INHERIT;  -- Mặc định
CREATE ROLE developer INHERIT;

GRANT manager TO team_lead;
GRANT team_lead TO developer;

-- Giờ developer có permissions của manager thông qua team_lead
GRANT SELECT, INSERT ON projects TO manager;

-- Xem inherited roles
SELECT 
    r.rolname AS role_name,
    r.rolinherit,
    pg_roles WHERE pg_has_role(developer, r.oid, 'member');
```

---

### 13. Policy Validation

**Định nghĩa:** Quá trình kiểm tra policies có hoạt động đúng như mong đợi không trước khi deploy.

**Các bước validation:**
1. Test với vai trò khác nhau
2. Verify all access paths
3. Check edge cases (NULL, edge values)
4. Performance impact assessment

** Ví dụ:**
```sql
-- Test policy với EXPLAIN
EXPLAIN (COSTS, VERBOSE) 
SELECT * FROM orders WHERE user_id = 'test-user-id';

-- Test với SET ROLE
SET ROLE authenticated;
SET LOCAL request.jwt.claims = '{"sub": "user-123", "role": "authenticated"}';

SELECT * FROM orders;  -- Should only see own orders

RESET ROLE;

-- Test edge cases
SELECT * FROM orders WHERE user_id IS NULL;  -- Should return nothing
SELECT * FROM orders WHERE user_id = 'non-existent';  -- Should return nothing
```

---

### 14. RLS Performance

**Định nghĩa:** Row Level Security có thể ảnh hưởng đến query performance, đặc biệt khi policies phức tạp hoặc trên tables lớn.

**Các yếu tố ảnh hưởng:**
- Số lượng policies trên table
- Độ phức tạp của USING expressions
- Index availability cho policy conditions
- Security barrier views

** Optimization strategies:**
```sql
-- Tạo index cho policy columns
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Sử dụng partial indexes
CREATE INDEX idx_orders_pending ON orders(id) 
WHERE status = 'pending' AND user_id = auth.uid();  -- Không hỗ trợ trong policy

-- Simplify policy logic
-- BAD: Complex subquery
CREATE POLICY complex ON data
FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM user_teams 
        WHERE team_id = data.team_id 
        AND user_id = auth.uid()
    )
);

-- GOOD: Simple direct comparison (nếu có denormalized column)
CREATE POLICY simple ON data
FOR SELECT
USING (team_user_id = auth.uid());
```

---

### 15. Default Deny

**Định nghĩa:** Nguyên tắc thiết kế bảo mật where không có policy means no access được cho phép. Tables với RLS enabled mặc định không cho phép access.

**Trong Supabase:**
- Tables không có policies: Không ai truy cập được
- Policies phải explicitly cho phép access

** Ví dụ:**
```sql
-- RLS enabled nhưng không có policy = Default Deny
ALTER TABLE secret_data ENABLE ROW LEVEL SECURITY;
-- Bây giờ secret_data hoàn toàn không thể truy cập được

-- Phải tạo policy để cho phép access
CREATE POLICY access_secret ON secret_data
FOR SELECT
USING (true);  -- Cho phép tất cả authenticated users

-- Nếu muốn block tất cả (emergency)
CREATE POLICY block_all ON secret_data
FOR SELECT
USING (false);  -- Block tất cả users
```

---

### 16. Multiple Policies

**Định nghĩa:** Một table có thể có nhiều policies cho cùng một command type. Các policies được OR-ed với nhau.

** Ví dụ:**
```sql
-- Policy 1: Owner có thể xem
CREATE POLICY owner_view ON documents
FOR SELECT
USING (owner_id = auth.uid());

-- Policy 2: Team members có thể xem
CREATE POLICY team_view ON documents
FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM document_teams dt
        WHERE dt.document_id = documents.id
        AND dt.user_id = auth.uid()
    )
);

-- Cả hai policies được OR-ed
-- User có thể xem document nếu:
-- - Là owner, HOẶC
-- - Là team member
```

---

### 17. Security Barrier Views

**Định nghĩa:** Views với RLS policies được applied trước khi user-defined functions (UDFs) được execute, ngăn chặn information leakage.

**Khi nào cần:**
- View sử dụng functions
- Cần ngăn chặn function access đến unauthorized data
- Security-sensitive aggregations

** Ví dụ:**
```sql
-- SECURITY BARRIER view
CREATE SECURITY BARRIER VIEW sensitive_summary AS
SELECT 
    department,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary
FROM employees
WHERE visible = true
GROUP BY department;

-- Grant access to view (policies apply)
GRANT SELECT ON sensitive_summary TO analyst_role;

-- Tạo policy on view
ALTER VIEW sensitive_summary ENABLE ROW LEVEL SECURITY;
CREATE POLICY analyst_view ON sensitive_summary
FOR SELECT
USING (
    (auth.jwt() -> 'app_metadata' ->> 'role') IN ('analyst', 'admin')
);
```

---

### 18. Policy Dependencies

**Định nghĩa:** RLS policies có thể phụ thuộc vào nhau, tạo ra potential circular dependencies hoặc performance issues.

**Các loại dependencies:**
- Cross-table references
- Function calls
- Subqueries đến tables có RLS
- Triggers

** Ví dụ:**
```sql
-- Dependencies: orders -> customers -> profiles
-- Policy on orders references customers
CREATE POLICY view_orders ON orders
FOR SELECT
USING (
    customer_id IN (
        SELECT id FROM customers 
        WHERE profile_id IN (
            SELECT id FROM profiles WHERE user_id = auth.uid()
        )
    )
);

-- Kiểm tra dependencies
SELECT 
    schemaname,
    tablename,
    policyname,
    cmd
FROM pg_policies
WHERE schemaname = 'public';

-- Drop policy với CASCADE nếu có dependencies
DROP POLICY IF EXISTS old_policy ON table_name CASCADE;
```

---

### 19. Auth Helper Functions

**Định nghĩa:** Các functions được cung cấp bởi Supabase để simplify RLS policy writing.

**Các functions có sẵn:**
- `auth.uid()`: Current user ID
- `auth.jwt()`: Full JWT claims
- `auth.role()`: Current role name
- `auth.email()`: Current user email

** Ví dụ:**
```sql
-- Sử dụng auth.email() cho email-based policies
CREATE POLICY email_match ON user_settings
FOR SELECT
USING (user_email = auth.email());

-- Sử dụng auth.role() cho role-based policies
CREATE POLICY admin_only ON admin_panel
FOR ALL
USING (auth.role() = 'admin')
WITH CHECK (auth.role() = 'admin');

-- Tạo custom helper function
CREATE OR REPLACE FUNCTION is_owner(table_user_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN table_user_id = auth.uid();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER STABLE;

-- Sử dụng trong policy
CREATE POLICY owner_access ON resources
FOR ALL
USING (is_owner(user_id))
WITH CHECK (is_owner(user_id));
```

---

### 20. Tenant Isolation

**Định nghĩa:** Pattern để isolate data giữa các tenants trong multi-tenant applications sử dụng RLS.

**Implementation approaches:**
- Tenant ID column
- Schema per tenant
- Row-level tenant filter

** Ví dụ:**
```sql
-- Add tenant_id column
ALTER TABLE resources ADD COLUMN tenant_id UUID NOT NULL;

-- Create policy for tenant isolation
CREATE POLICY tenant_isolation ON resources
FOR ALL
USING (
    tenant_id = (
        SELECT tenant_id 
        FROM user_tenants 
        WHERE user_id = auth.uid()
    )
)
WITH CHECK (
    tenant_id = (
        SELECT tenant_id 
        FROM user_tenants 
        WHERE user_id = auth.uid()
    )
);

-- Index for performance
CREATE INDEX idx_resources_tenant ON resources(tenant_id);
```

---

### 21. Row Security Check

**Định nghĩa:** PostgreSQL kiểm tra row security policies trước khi trả về results hoặc thực hiện modifications.

**Check timing:**
- SELECT: Kiểm tra trước khi return rows
- INSERT: Kiểm tra WITH CHECK trước khi insert
- UPDATE: Kiểm tra USING và WITH CHECK
- DELETE: Kiểm tra USING trước khi delete

** Ví dụ:**
```sql
-- PostgreSQL sẽ tự động thêm CHECK vào query plan
EXPLAIN (COSTS, VERBOSE)
SELECT * FROM orders;

-- Output sẽ show Row Security Check:
/*
Seq Scan on public.orders  (cost=...)
  Output: ...
  Filter: ((user_id = '...'::uuid) OR (user_id = NULL))
  Row Security: ((user_id = '...'::uuid) OR (user_id = NULL))
*/
```

---

### 22. force_row_level_security

**Định nghĩa:** Database parameter để enforce RLS ngay cả cho superusers và roles có BYPASSRLS.

**Use cases:**
- Testing policies
-强制 strict security cho tất cả users
- Prevent accidental data access

** Ví dụ:**
```sql
-- Enable cho database
ALTER DATABASE mydb SET force_row_level_security = on;

-- Hoặc cho session
SET force_row_level_security = on;

-- Kiểm tra
SHOW force_row_level_security;

-- Khi enabled, ngay cả postgres superuser cũng phải tuân theo RLS
```
