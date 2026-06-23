---
title: "RLS Anti-Patterns"
description: "Các mẫu thiết kế RLS cần tránh trong PostgreSQL"
tags: ["rls", "postgres", "security", "anti-patterns", "database"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# RLS Anti-Patterns - Các Mẫu Thiết Kế Cần Tránh

## Overview

Row Level Security (RLS) là một cơ chế bảo mật mạnh mẽ trong PostgreSQL, nhưng việc triển khai không đúng cách có thể dẫn đến các lỗ hổng bảo mật nghiêm trọng hoặc vấn đề hiệu suất nghiêm trọng. Tài liệu này tổng hợp các anti-patterns phổ biến nhất mà developers thường gặp phải khi làm việc với RLS, cùng với giải thích chi tiết về lý do tại sao chúng là vấn đề và cách khắc phục.

Các anti-patterns được trình bày theo mức độ nghiêm trọng: Critical (Nghiêm trọng), High (Cao), Medium (Trung bình), và Low (Thấp). Mỗi anti-pattern bao gồm mô tả, ví dụ thực tế, tác động, và giải pháp thay thế.

## Purpose

Mục tiêu của tài liệu này là giúp developers nhận diện và tránh các sai lầm phổ biến khi triển khai RLS. Việc hiểu rõ các anti-patterns không chỉ giúp tránh bugs mà còn đảm bảo hệ thống database hoạt động đúng đắn từ đầu. Mỗi section bao gồm code examples thực tế để bạn có thể dễ dàng nhận diện và tránh các vấn đề này trong codebase của mình.

## Key Concepts

### Tại Sao Anti-Patterns Xảy Ra?

Các anti-patterns RLS thường xảy ra do nhiều lý do: thiếu hiểu biết về cách RLS hoạt động, áp lực thời gian trong development, hoặc đơn giản là copy-paste code mà không hiểu rõ. RLS là một feature tương đối phức tạp với nhiều edge cases và nuances mà không phải developer nào cũng nắm vững.

Một số anti-patterns có thể dẫn đến data leakage nghiêm trọng, trong khi những cái khác có thể gây ra performance degradation hoặc maintainability issues. Việc hiểu rõ các patterns này sẽ giúp bạn thiết kế và implement RLS policies một cách an toàn và hiệu quả hơn.

### Phân Loại Anti-Patterns

**Critical Level** bao gồm các patterns có thể dẫn đến data breach hoặc complete security bypass. Đây là những vấn đề cần được ưu tiên sửa chữa ngay lập tức nếu phát hiện trong hệ thống.

**High Level** bao gồm các patterns có thể gây ra unauthorized access hoặc significant security risks nhưng không nghiêm trọng như Critical.

**Medium Level** bao gồm các patterns có thể gây ra performance issues hoặc maintenance difficulties nhưng không trực tiếp ảnh hưởng đến security.

**Low Level** bao gồm các patterns không tuân thủ best practices và có thể gây confusion hoặc technical debt về lâu dài.

## Common Anti-Patterns

### 1. DISABLED RLS - Critical

**Mô tả**: Disable RLS completely hoặc không enable RLS trên sensitive tables.

```sql
-- ANTI-PATTERN: Không enable RLS
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user'
);
-- RLS không được enable!

-- ANTI-PATTERN: Disable RLS "tạm thời" cho testing
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
-- Để lại trong production!
```

**Tại sao đây là vấn đề**: Khi RLS không được enable, bất kỳ ai có quyền truy cập database đều có thể đọc, sửa, hoặc xóa tất cả data trong table mà không có bất kỳ ràng buộc nào. Điều này đặc biệt nguy hiểm với các tables chứa sensitive information như user credentials, personal information, hoặc financial data.

```sql
-- Không có RLS, query này trả về TẤT CẢ users
SELECT * FROM users;
-- Kẻ tấn công có thể dump toàn bộ database
```

**Tác động**: Data breach tiềm năng, unauthorized access đến all user data, compliance violations (GDPR, SOC2, etc.).

**Giải pháp**: Luôn enable RLS trên tất cả tables chứa sensitive data.

```sql
-- CORRECT: Enable RLS ngay khi tạo table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user'
);

-- Enable RLS ngay lập tức
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE users FORCE ROW LEVEL SECURITY;

-- Tạo policies ngay lập tức
CREATE POLICY users_select ON users
    FOR SELECT USING (id = auth.uid());

CREATE POLICY users_insert ON users
    FOR INSERT WITH CHECK (id = auth.uid());

CREATE POLICY users_update ON users
    FOR UPDATE USING (id = auth.uid())
    WITH CHECK (id = auth.uid());
```

### 2. OVERLY PERMISSIVE POLICIES - Critical

**Mô tả**: Tạo policies cho phép tất cả users truy cập tất cả data.

```sql
-- ANTI-PATTERN: Policy cho phép tất cả
CREATE POLICY public_access ON sensitive_data
    FOR ALL USING (true);

-- ANTI-PATTERN: Policy không có điều kiện
CREATE POLICY no_restriction ON user_profiles
    FOR SELECT USING (1=1);

-- ANTI-PATTERN: Auth check nhưng không enforce
CREATE POLICY weak_check ON orders
    FOR SELECT USING (
        auth.uid() IS NOT NULL  -- Chỉ check NOT NULL, không check ownership
    );
```

**Tại sao đây là vấn đề**: Policies với `USING (true)` hoặc `USING (1=1)` không cung cấp bất kỳ security nào - chúng cho phép bất kỳ authenticated user truy cập tất cả rows. Điều này completely defeats the purpose của RLS và tạo ra một false sense of security.

```sql
-- Với policy "USING (true)", user A có thể đọc data của user B
SELECT * FROM orders WHERE customer_id = 'different-user-uuid';  -- Returns data!
```

**Tác động**: Complete data leakage, unauthorized access đến other users' data, potential GDPR violations.

**Giải pháp**: Luôn enforce ownership hoặc appropriate access checks.

```sql
-- CORRECT: Enforce ownership
CREATE POLICY orders_own ON orders
    FOR SELECT USING (customer_id = auth.uid());

-- CORRECT: Combined ownership + role-based access
CREATE POLICY orders_access ON orders
    FOR SELECT USING (
        customer_id = auth.uid()
        OR EXISTS (
            SELECT 1 FROM user_roles
            WHERE user_id = auth.uid()
            AND role IN ('admin', 'support')
        )
    );
```

### 3. BYPASSING RLS WITH SECURITY DEFINER - Critical

**Mô tả**: Sử dụng SECURITY DEFINER functions không đúng cách, tạo ra security bypass.

```sql
-- ANTI-PATTERN: SECURITY DEFINER không kiểm tra permissions
CREATE OR REPLACE FUNCTION get_all_users()
RETURNS SETOF users AS $$
BEGIN
    RETURN QUERY SELECT * FROM users;  -- Không check gì cả!
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ANTI-PATTERN: Service role key exposed trong client code
const supabase = createClient(
    SUPABASE_URL,
    'eyJhbGciOiJIUzI1NiIs...'  // Service role key - NEVER in client!
);
```

**Tại sao đây là vấn đề**: SECURITY DEFINER functions chạy với privileges của người tạo function, không phải người gọi. Nếu không có proper permission checks bên trong, đây là một complete security bypass. Attackers có thể gọi các functions này để truy cập data mà họ không được phép.

```sql
-- Ai cũng có thể gọi function này và lấy tất cả data
SELECT * FROM get_all_users();  -- Returns all users!
```

**Tác động**: Complete security bypass, unauthorized data access, potential data exfiltration.

**Giải pháp**: Luôn verify permissions trong SECURITY DEFINER functions.

```sql
-- CORRECT: SECURITY DEFINER với permission checks
CREATE OR REPLACE FUNCTION get_all_users_admin()
RETURNS SETOF users AS $$
BEGIN
    -- Verify caller là admin
    IF NOT EXISTS (
        SELECT 1 FROM user_roles
        WHERE user_id = auth.uid()
        AND role = 'admin'
    ) THEN
        RAISE EXCEPTION 'Admin access required';
    END IF;
    
    RETURN QUERY SELECT * FROM users;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- CORRECT: Wrapper function với proper access control
CREATE OR REPLACE FUNCTION get_user_by_id(p_user_id UUID)
RETURNS users AS $$
BEGIN
    -- Users chỉ có thể xem chính họ, admins có thể xem tất cả
    IF auth.uid() = p_user_id THEN
        RETURN QUERY SELECT * FROM users WHERE id = p_user_id;
    ELSIF EXISTS (
        SELECT 1 FROM user_roles
        WHERE user_id = auth.uid()
        AND role = 'admin'
    ) THEN
        RETURN QUERY SELECT * FROM users WHERE id = p_user_id;
    ELSE
        RETURN NULL;
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 4. MISSING POLICIES FOR OPERATIONS - High

**Mô tả**: Enable RLS nhưng không tạo policies cho tất cả các operations cần thiết.

```sql
-- ANTI-PATTERN: Enable RLS nhưng chỉ có SELECT policy
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY orders_select ON orders
    FOR SELECT USING (customer_id = auth.uid());
-- INSERT, UPDATE, DELETE policies không có!

-- Hậu quả: INSERT sẽ bị DENIED vì không có policy
INSERT INTO orders (customer_id, total) VALUES (auth.uid(), 100);
-- ERROR: no policy with CHECK for this statement
```

**Tại sao đây là vấn đề**: Khi RLS được enable mà không có policies cho tất cả operations, PostgreSQL sử dụng default deny policy. Điều này có thể gây ra unexpected application errors hoặc silent failures mà developers có thể không nhận ra trong testing.

```sql
-- User muốn tạo order nhưng bị denied
INSERT INTO orders (customer_id, total) VALUES (auth.uid(), 100);
-- Error: permission denied for table orders
```

**Tác động**: Application functionality breaks, silent data access denials, user confusion.

**Giải pháp**: Tạo policies cho tất cả operations hoặc sử dụng policy cho ALL operations.

```sql
-- CORRECT: Policy cho ALL operations
CREATE POLICY orders_all ON orders
    FOR ALL
    USING (customer_id = auth.uid())
    WITH CHECK (customer_id = auth.uid());

-- CORRECT: Separate policies cho từng operation
CREATE POLICY orders_select ON orders FOR SELECT USING (customer_id = auth.uid());
CREATE POLICY orders_insert ON orders FOR INSERT WITH CHECK (customer_id = auth.uid());
CREATE POLICY orders_update ON orders FOR UPDATE USING (customer_id = auth.uid()) WITH CHECK (customer_id = auth.uid());
CREATE POLICY orders_delete ON orders FOR DELETE USING (customer_id = auth.uid());
```

### 5. NULL AUTH.UID() NOT HANDLED - High

**Mô tả**: Policies không handle trường hợp auth.uid() trả về NULL.

```sql
-- ANTI-PATTERN: Không handle NULL
CREATE POLICY orders_unsafe ON orders
    FOR SELECT USING (customer_id = auth.uid());
-- Nếu auth.uid() là NULL, so sánh NULL = NULL trả về NULL (not TRUE)
-- Kết quả: User không thấy data dù có quyền

-- ANTI-PATTERN: NULL handling sai
CREATE POLICY orders_wrong ON orders
    FOR SELECT USING (customer_id = COALESCE(auth.uid(), 'unknown'));
-- Logic này sai vì NULL auth.uid() không có nghĩa là 'unknown'
```

**Tại sao đây là vấn đề**: Khi user không authenticated hoặc JWT invalid, auth.uid() trả về NULL. So sánh `column = NULL` trong SQL luôn trả về NULL (không phải TRUE hoặc FALSE), nghĩa là row sẽ không được trả về. Điều này có thể gây ra confusing errors.

```sql
-- Demo: NULL comparison behavior
SELECT 1 WHERE NULL = NULL;  -- Returns: (no rows)
SELECT 1 WHERE NULL IS NULL; -- Returns: 1

-- Với policy "customer_id = auth.uid()" và auth.uid() = NULL
-- Query trả về 0 rows thay vì deny access
```

**Tác động**: Unexpected empty results, confusing behavior, potential security misconfiguration.

**Giải pháp**: Handle NULL explicitly và ensure proper authentication.

```sql
-- CORRECT: Handle NULL explicitly
CREATE POLICY orders_safe ON orders
    FOR SELECT USING (
        auth.uid() IS NOT NULL  -- Check trước
        AND customer_id = auth.uid()
    );

-- CORRECT: Combine với admin bypass
CREATE POLICY orders_complete ON orders
    FOR SELECT USING (
        auth.uid() IS NOT NULL
        AND (
            customer_id = auth.uid()
            OR EXISTS (
                SELECT 1 FROM user_roles
                WHERE user_id = auth.uid()
                AND role = 'admin'
            )
        )
    );
```

### 6. COMPLEX SUBQUERIES IN POLICIES - Medium

**Mô tả**: Sử dụng deeply nested subqueries hoặc complex joins trong policy definitions.

```sql
-- ANTI-PATTERN: Deep nesting
CREATE POLICY orders_complex ON orders
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM (
                SELECT 1 FROM (
                    SELECT 1 FROM users
                    WHERE users.id = orders.customer_id
                    AND users.team_id IN (
                        SELECT team_id FROM (
                            SELECT team_id FROM team_members
                            WHERE user_id = auth.uid()
                        ) AS nested
                    )
                ) AS deep_nested
            ) AS very_deep
        )
    );

-- ANTI-PATTERN: Multiple complex joins
CREATE POLICY posts_complex ON posts
    FOR SELECT USING (
        author_id = auth.uid()
        OR group_id IN (
            SELECT gm.group_id
            FROM group_members gm
            JOIN groups g ON gm.group_id = g.id
            JOIN user_profiles up ON gm.user_id = up.user_id
            WHERE gm.user_id = auth.uid()
            AND g.status = 'active'
            AND up.membership_status = 'active'
        )
    );
```

**Tại sao đây là vấn đề**: Complex policy expressions được execute cho mỗi row, gây ra significant performance overhead. Nested subqueries có thể không use indexes hiệu quả và có thể dẫn đến nested loop scans. Điều này đặc biệt problematic với large tables.

```sql
-- Performance impact: Query plan với complex policy
EXPLAIN SELECT * FROM orders;
-- Output:
-- Seq Scan on orders
--   Filter: (alternatives: SubPlan 1, SubPlan 2, ...)
--   Row Security Filter: (SubPlan 1)
-- Planning Time: 10ms
-- Execution Time: 5000ms  -- Rất chậm!
```

**Tác động**: Significant performance degradation, increased query execution time, poor scalability.

**Giải pháp**: Simplify policies, use helper functions, denormalize where appropriate.

```sql
-- CORRECT: Simple direct comparison
CREATE POLICY orders_simple ON orders
    FOR SELECT USING (customer_id = auth.uid());

-- CORRECT: Helper function cho complex logic
CREATE OR REPLACE FUNCTION is_order_visible(p_order_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    v_customer_id UUID;
    v_is_admin BOOLEAN;
BEGIN
    -- Simple, index-friendly queries
    SELECT customer_id INTO v_customer_id
    FROM orders WHERE id = p_order_id;
    
    SELECT EXISTS (
        SELECT 1 FROM user_roles
        WHERE user_id = auth.uid()
        AND role = 'admin'
    ) INTO v_is_admin;
    
    RETURN v_customer_id = auth.uid() OR v_is_admin;
END;
$$ LANGUAGE plpgsql STABLE;

-- CORRECT: Materialized relationship table
CREATE TABLE user_teams (
    user_id UUID REFERENCES users(id),
    team_id UUID REFERENCES teams(id),
    PRIMARY KEY (user_id, team_id)
);

CREATE INDEX idx_user_teams_user ON user_teams(user_id);

CREATE POLICY posts_optimized ON posts
    FOR SELECT USING (
        author_id = auth.uid()
        OR team_id IN (SELECT team_id FROM user_teams WHERE user_id = auth.uid())
    );
```

### 7. ROLE CONFUSION - Medium

**Mô tả**: Không phân biệt rõ ràng giữa các roles và permissions.

```sql
-- ANTI-PATTERN: Tất cả users có cùng role
CREATE ROLE app_user;
GRANT app_user TO ALL;

CREATE POLICY everything_for_users ON sensitive_data
    FOR ALL TO app_user USING (true);

-- ANTI-PATTERN: Không có role hierarchy
CREATE ROLE viewer;
CREATE ROLE editor;
CREATE ROLE admin;
-- Không có distinction, mọi thứ merge vào nhau
```

**Tại sao đây là vấn đề**: Khi tất cả users có cùng role, bạn không thể differentiate permissions. Điều này dẫn đến either over-permissive access (nếu policy quá rộng) hoặc under-permissive access (nếu policy quá hẹp).

```sql
-- User bình thường có thể thấy admin-only data
SELECT * FROM admin_logs;  -- Không có distinction!
```

**Tác động**: Security misconfiguration, inability to implement proper access control, compliance issues.

**Giải pháp**: Implement clear role hierarchy và specific permissions per role.

```sql
-- CORRECT: Role hierarchy
CREATE ROLE authenticated;      -- Base role
CREATE ROLE viewer;             -- Inherits from authenticated
CREATE ROLE editor;              -- Inherits from viewer
CREATE ROLE admin;               -- Inherits from editor

GRANT authenticated TO viewer;
GRANT authenticated TO editor;
GRANT authenticated TO admin;
GRANT editor TO admin;

-- CORRECT: Role-specific policies
CREATE POLICY viewer_read ON documents
    FOR SELECT TO viewer USING (is_published = true);

CREATE POLICY editor_crud ON documents
    FOR ALL TO editor USING (author_id = auth.uid());

CREATE POLICY admin_all ON documents
    FOR ALL TO admin USING (true);
```

### 8. PUBLIC ACCESS MISTAKES - Medium

**Mô tả**: Cấu hình public schema access không đúng cách.

```sql
-- ANTI-PATTERN: Public schema không secure
GRANT USAGE ON SCHEMA public TO PUBLIC;
GRANT ALL ON ALL TABLES IN SCHEMA public TO PUBLIC;

-- ANTI-PATTERN: Default privileges cho public
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT ALL ON TABLES TO PUBLIC;
```

**Tại sao đây là vấn đề**: Granting permissions to PUBLIC có nghĩa là EVERYONE gets those permissions, bao gồm cả anonymous và newly created users. Điều này tạo ra một huge security hole nếu không được control carefully.

```sql
-- Ai cũng có thể truy cập mọi thứ
SET ROLE postgres;  -- Giả sử attacker có access
SELECT * FROM sensitive_data;  -- Returns all data!
```

**Tác động**: Unrestricted public access, potential data leakage, security misconfiguration.

**Giải pháp**: Restrict public schema access và grant only specific permissions.

```sql
-- CORRECT: Restrict public schema
REVOKE USAGE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public FROM PUBLIC;

-- CORRECT: Explicit grants to specific roles
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT SELECT ON public.products TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.orders TO authenticated;
```

### 9. IGNORING POLICY INTERACTIONS - Low

**Mô tả**: Không hiểu cách multiple policies interact với nhau.

```sql
-- ANTI-PATTERN: Multiple permissive policies
CREATE POLICY allow_all_auth ON orders
    FOR SELECT TO authenticated USING (true);

CREATE POLICY allow_customer ON orders
    FOR SELECT USING (customer_id = auth.uid());

-- Kết quả: OR semantics, user thấy tất cả orders
```

**Tại sao đây là vấn đề**: Với PERMISSIVE policies (default), PostgreSQL sử dụng OR semantics - row được visible nếu ANY policy allows. Với RESTRICTIVE policies, sử dụng AND semantics - row chỉ visible nếu ALL policies allow. Hiểu sai semantics có thể dẫn đến unintended access grants.

```sql
-- Demo: Policy interaction
-- Policy 1: USING (true) - allows everyone
-- Policy 2: USING (customer_id = auth.uid()) - allows owner
-- OR semantics: Nếu policy 1 allows, row visible cho tất cả!
```

**Tác động**: Unintended data access, security misconfiguration, confusion.

**Giải ph�**: Document policy interactions và use RESTRICTIVE policies for security-critical access.

```sql
-- CORRECT: Single comprehensive policy
CREATE POLICY orders_access ON orders
    FOR SELECT USING (
        customer_id = auth.uid()
        OR EXISTS (
            SELECT 1 FROM user_roles
            WHERE user_id = auth.uid()
            AND role = 'admin'
        )
    );

-- CORRECT: RESTRICTIVE for additional security
CREATE POLICY admin_only_restrictive ON admin_logs
    FOR SELECT USING (false);  -- Deny all by default

CREATE POLICY admin_view_logs ON admin_logs
    FOR SELECT TO admin
    USING (true);  -- Allow only admin role
```

### 10. NO POLICY DOCUMENTATION - Low

**Mô tả**: Không document policies, dẫn đến confusion và maintenance issues.

```sql
-- ANTI-PATTERN: Không có comments
CREATE POLICY p1 ON orders FOR SELECT USING (customer_id = auth.uid());
CREATE POLICY p2 ON orders FOR INSERT WITH CHECK (customer_id = auth.uid());

-- Ai hiểu policy này làm gì sau 6 tháng?
```

**Tại sao đây là vấn đề**: Không có documentation, developers không hiểu rõ tại sao policies được design như vậy. Điều này dẫn đến incorrect modifications, duplicated effort, và security gaps khi refactoring.

**Tác động**: Maintainability issues, potential security gaps, technical debt.

**Giải pháp**: Document all policies với clear comments và naming conventions.

```sql
-- CORRECT: Well-documented policies
/**
 * Orders Access Policy
 * 
 * Purpose: Control access to orders table
 * Owner: Security Team
 * Created: 2024-01-15
 * Last Updated: 2024-06-20
 * 
 * Access Rules:
 * - Users can view their own orders
 * - Users can create orders for themselves
 * - Users can update their own pending orders
 * - Admins can view/update all orders
 * 
 * Security Considerations:
 * - customer_id must match auth.uid() for non-admins
 * - Only admins can modify order status
 * - All updates are audited via audit_logs table
 */
CREATE POLICY orders_access ON orders
    FOR ALL
    USING (
        -- Owner access: Users can access their own orders
        customer_id = auth.uid()
        -- Admin bypass: Admins can access all orders
        OR EXISTS (
            SELECT 1 FROM user_roles
            WHERE user_id = auth.uid()
            AND role = 'admin'
        )
    )
    WITH CHECK (
        -- Prevent customer_id changes
        customer_id = customer_id
        -- Only allow total changes for admins
        AND (
            total = total
            OR EXISTS (
                SELECT 1 FROM user_roles
                WHERE user_id = auth.uid()
                AND role = 'admin'
            )
        )
    );
```

## Troubleshooting

### Debugging RLS Issues

Khi gặp vấn đề với RLS, follow these steps:

```sql
-- Step 1: Check if RLS is enabled
SELECT
    relname,
    relrowsecurity,
    relforcerowsecurity
FROM pg_class
WHERE relname IN ('orders', 'users', 'products');

-- Step 2: List all policies on table
SELECT
    policyname,
    permissive,
    cmd,
    roles,
    qual::text,
    with_check::text
FROM pg_policies
WHERE tablename = 'orders';

-- Step 3: Check current user context
SELECT
    current_user,
    session_user,
    auth.uid(),
    auth.role();

-- Step 4: Test policy with EXPLAIN
EXPLAIN (ANALYZE, COSTS, VERBOSE)
SELECT * FROM orders WHERE customer_id = 'test-uuid';

-- Step 5: Check for NULL auth.uid()
SELECT auth.uid() IS NULL;  -- Should be FALSE for authenticated users
```

### Common Error Messages

```sql
-- Error: permission denied for table
-- Cause: No RLS policy exists for the operation
-- Fix: Create appropriate policy

-- Error: no policy with CHECK for this statement
-- Cause: INSERT/UPDATE without WITH CHECK policy
-- Fix: Add policy with WITH CHECK clause

-- Error: row security filter violates with CHECK expression
-- Cause: INSERT/UPDATE data doesn't satisfy WITH CHECK
-- Fix: Ensure data meets policy requirements
```

## Examples

### Complete Anti-Pattern Examples

```sql
-- ============================================
-- ANTI-PATTERN: Insecure E-commerce Schema
-- ============================================

-- Tables without proper RLS
CREATE TABLE customers (
    id UUID PRIMARY KEY,
    email TEXT,
    password_hash TEXT,
    credit_card TEXT  -- SENSITIVE!
);

CREATE TABLE orders (
    id UUID PRIMARY KEY,
    customer_id UUID REFERENCES customers(id),
    total DECIMAL,
    shipping_address TEXT  -- SENSITIVE!
);

CREATE TABLE products (
    id UUID PRIMARY KEY,
    name TEXT,
    price DECIMAL
);

-- PROBLEM: No RLS enabled
-- ANTI-PATTERN: Everyone can see everything
GRANT SELECT ON ALL TABLES IN SCHEMA public TO PUBLIC;

-- ============================================
-- CORRECT: Secure E-commerce Schema
-- ============================================

-- Enable RLS on all tables
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE customers FORCE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;

-- Customer policies
CREATE POLICY customers_own ON customers
    FOR ALL USING (id = auth.uid())
    WITH CHECK (id = auth.uid());

-- Order policies
CREATE POLICY orders_own ON orders
    FOR SELECT USING (customer_id = auth.uid());

CREATE POLICY orders_insert ON orders
    FOR INSERT WITH CHECK (customer_id = auth.uid());

-- Product policies (public read for browsing)
CREATE POLICY products_public ON products
    FOR SELECT USING (is_active = true);

CREATE POLICY products_admin ON products
    FOR ALL TO admin USING (true);

-- Proper privileges
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT SELECT ON products TO authenticated;
```

## References

- [PostgreSQL Row Level Security Documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [Supabase RLS Guidelines](https://supabase.com/docs/guides/auth/row-level-security)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [PostgreSQL pg_policies](https://www.postgresql.org/docs/current/view-pg-policies.html)
- [Cursor Enterprise Framework Security Rules](../rules/security.md)
- [Cursor Enterprise Framework Multi-Tenant Rules](../rules/multi-tenant.md)
