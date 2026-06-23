# Row Level Security Decision Tree - Cây Quyết Định

## Giới thiệu

Tài liệu này cung cấp cây quyết định để hướng dẫn việc lựa chọn các giải pháp và cấu hình phù hợp cho Row Level Security (RLS).

---

## 1. RLS Implementation Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              RLS IMPLEMENTATION DECISION                           │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Is this a user-facing table?      │
              └─────────────────────────────────┘
                    │              │
                   [Yes]           [No]
                    │              │
                    ▼              ▼
         ┌─────────────────┐ ┌─────────────────┐
         │ Enable RLS      │ │ Consider if RLS │
         │                 │ │ is needed       │
         └─────────────────┘ └─────────────────┘
                    │
                    ▼
    ┌─────────────────────────────────────────┐
    │ What is the ownership model?            │
    └─────────────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [User]        [Team/Tenant] │         [Public]
           │              │              │
           ▼              ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │ user_id =   │ │ tenant_id =  │ │ USING(true)│
    │ auth.uid()  │ │ auth.tenant_ │ │ or policy  │
    │             │ │ id()         │ │ based on   │
    │             │ │              │ │ other     │
    │             │ │              │ │ criteria   │
    └─────────────┘ └──────────────┘ └────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ POLICY STRUCTURE DECISION:                                   │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │ One policy for all operations (ALL)?                        │
    │        │                                                    │
    │   ┌────┴────┐                                               │
    │  [Yes]    [No]                                             │
    │   │          │                                               │
    │   ▼          ▼                                               │
    │ ┌─────────┐ ┌─────────────────────────────────────────┐   │
    │ │ ALL    │ │ Separate policies for:                    │   │
    │ │ USING = │ │ - SELECT (USING)                          │   │
    │ │ policy  │ │ - INSERT (WITH CHECK)                     │   │
    │ │         │ │ - UPDATE (USING + WITH CHECK)             │   │
    │ └─────────┘ │ - DELETE (USING)                          │   │
    │              └─────────────────────────────────────────┘   │
    │                                                              │
    │ WHEN TO USE COMBINED (ALL):                                 │
    │ • Same logic for all operations                             │
    │ • Simple ownership model                                    │
    │ • No need to differentiate                                  │
    │                                                              │
    │ WHEN TO USE SEPARATE:                                       │
    │ • Different conditions for different ops                     │
    │ • INSERT has different requirements than SELECT             │
    │ • Need to prevent certain updates                           │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## 2. Policy Condition Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              POLICY CONDITION DECISION                             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ What condition to use?           │
              └─────────────────────────────────┘
                    │              │              │              │
           ┌────────┴────────┐     │              │              │
          [Direct Match]  [Complex] │         [Role-Based]  [Public]
           │              │              │              │
           ▼              ▼              ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐ ┌────────────┐
    │user_id =    │ │EXISTS/IN    │ │JWT role   │ │is_public  │
    │auth.uid()  │ │subqueries   │ │check      │ │= true     │
    └─────────────┘ └──────────────┘ └────────────┘ └────────────┘
           │              │              │              │
           ▼              ▼              ▼              ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ OPTIMIZATION:                                               │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │ Direct Match:                    Complex Conditions:          │
    │ • Fast                         • Use helper functions      │
    │ • Simple index works           • Consider denormalization  │
    │ • Best performance             • May need composite indexes │
    │                                                              │
    │ EXISTS/IN subqueries:         Role-Based:                  │
    │ • Index the subquery column   • Use is_admin() helper       │
    │ • Consider denormalization     • Cache role in JWT          │
    │ • Keep subqueries simple       • Fast for frequent checks    │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## 3. Authentication Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              AUTHENTICATION DECISION TREE                           │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ How to get user identity?      │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [auth.uid()]    [JWT Claims] │         [Both]
           │              │              │
           ▼              ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │Use direct   │ │auth.jwt()    │ │Combine    │
    │             │ │-> 'sub'      │ │both       │
    └─────────────┘ └──────────────┘ └────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ AUTH.UID() vs AUTH.JWT() COMPARISON:                       │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │ auth.uid():                  auth.jwt():                    │
    │ • Returns user UUID directly   • Returns full JWT object    │
    │ • Fast and simple            • Access any claim            │
    │ • Most common use            • Custom metadata              │
    │ • Pre-validated             • Role information             │
    │                              • Tenant ID                   │
    │                                                              │
    │ USE auth.uid() WHEN:           USE auth.jwt() WHEN:        │
    │ • Just need user ID           • Need role information       │
    │ • Simple ownership            • Need custom claims          │
    │ • Performance critical         • Need tenant ID              │
    │                              • Need group membership        │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## 4. Multi-Tenant Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              MULTI-TENANT ISOLATION DECISION                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Tenant isolation approach?       │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [JWT tenant_id]   [Membership Table] │         [Both]
           │              │              │
           ▼              ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │Store in     │ │user_tenant  │ │Hybrid:    │
    │JWT token    │ │mapping      │ │JWT for    │
    │             │ │table        │ │common,   │
    │             │ │             │ │table for │
    │             │ │             │ │complex   │
    └─────────────┘ └──────────────┘ └────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ TIER 1: JWT-BASED ISOLATION                                 │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │ Pros:                                                        │
    │ • Fast (no table lookup)                                    │
    │ • Simple policy                                              │
    │ • Stateless validation                                       │
    │                                                              │
    │ Cons:                                                        │
    │ • Must refresh JWT to change tenant                         │
    │ • Limited for complex tenant hierarchies                    │
    │ • Token size grows with claims                              │
    │                                                              │
    │ Use when:                                                    │
    │ • Simple tenant model                                      │
    │ • Performance critical                                     │
    │ • Users belong to one tenant                               │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ TIER 2: TABLE-BASED ISOLATION                              │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │ Pros:                                                        │
    │ • Flexible (supports hierarchies)                           │
    │ • Easy to query tenant relationships                        │
    │ • Can support multiple tenant membership                   │
    │                                                              │
    │ Cons:                                                        │
    │ • Extra lookup per query                                    │
    │ • Must maintain table                                      │
    │ • More complex policies                                    │
    │                                                              │
    │ Use when:                                                    │
    │ • Users belong to multiple tenants                         │
    │ • Complex tenant hierarchies                               │
    │ • Need to query tenant relationships                       │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## 5. Index Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              INDEX STRATEGY DECISION                             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ What columns need indexing?     │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [RLS Columns]  [Query Columns] │     [Composite]
           │              │              │
           ▼              ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │user_id      │ │status, date │ │(user_id,  │
    │tenant_id    │ │             │ │status)    │
    └─────────────┘ └──────────────┘ └────────────┘
           │              │              │
           ▼              ▼              ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ INDEX TYPE SELECTION:                                       │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │ Single Column:            Composite Index:                   │
    │ • B-tree (default)        • Column order matters            │
    │ • user_id = auth.uid()    • Equality first                 │
    │                           • Range second                     │
    │                           • Sort last                       │
    │                                                              │
    │ Partial Index:             Covering Index:                   │
    │ • WHERE published = true  • INCLUDE (id, name)            │
    │ • Smaller size            • Avoid table lookup              │
    │ • Faster writes           • Best for SELECT queries         │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## 6. Security Level Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              SECURITY LEVEL DECISION                             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ What is data sensitivity?       │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [High]        [Medium]  │         [Low]
           │              │              │
           ▼              ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │Defense in   │ │RLS + Basic  │ │RLS only   │
    │depth:       │ │Validation    │ │           │
    │• RLS       │ │• Input      │ │           │
    │• Encryption │ │  validation │ │           │
    │• Vault     │ │• JWT checks │ │           │
    │• Audit     │ │• Rate limit │ │           │
    └─────────────┘ └──────────────┘ └────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ SECURITY LAYER COMBINATION:                                  │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │ LOW SENSITIVITY:         MEDIUM SENSITIVITY:                 │
    │ • RLS only             • RLS + Input validation            │
    │ • Simple ownership     • JWT claim verification           │
    │                       • Basic audit logging               │
    │                                                              │
    │ HIGH SENSITIVITY:                                           │
    │ • RLS + Encryption at rest (TDE)                           │
    │ • Column-level encryption for highly sensitive              │
    │ • Separate secrets management (Vault)                      │
    │ • Comprehensive audit logging                              │
    │ • Rate limiting                                            │
    │ • IP whitelisting if needed                               │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## 7. Performance Optimization Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              PERFORMANCE OPTIMIZATION DECISION                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Is query slow?                   │
              └─────────────────────────────────┘
                    │              │
                   [Yes]          [No]
                    │              │
                    ▼              ▼
         ┌─────────────────┐ ┌─────────────────┐
         │Check EXPLAIN    │ │RLS is optimized │
         │                 │ │                 │
         └─────────────────┘ └─────────────────┘
                    │
                    ▼
    ┌─────────────────────────────────────────┐
    │ EXPLAIN Analysis:                         │
    └─────────────────────────────────────────┘
                    │
                    ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ CHECK RESULTS:                                               │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │ Seq Scan on table?                                          │
    │        │                                                    │
    │       [Yes]                                                 │
    │        │                                                    │
    │        ▼                                                    │
    │ ┌───────────────────────────────────────────────────────┐ │
    │ │ SOLUTION: Add index on RLS column                       │ │
    │ │ CREATE INDEX idx_user_id ON table(user_id);           │ │
    │ └───────────────────────────────────────────────────────┘ │
    │                                                              │
    │ Rows Removed by Filter: High?                               │
    │        │                                                    │
    │       [Yes]                                                 │
    │        │                                                    │
    │        ▼                                                    │
    │ ┌───────────────────────────────────────────────────────┐ │
    │ │ SOLUTIONS:                                            │ │
    │ │ 1. Create covering index                             │ │
    │ │ 2. Add composite index                             │ │
    │ │ 3. Consider denormalization                         │ │
    │ │ 4. Review policy conditions                        │ │
    │ └───────────────────────────────────────────────────────┘ │
    │                                                              │
    │ Nested Loop with subqueries?                               │
    │        │                                                    │
    │       [Yes]                                                 │
    │        │                                                    │
    │        ▼                                                    │
    │ ┌───────────────────────────────────────────────────────┐ │
    │ │ SOLUTIONS:                                            │ │
    │ │ 1. Index subquery columns                            │ │
    │ │ 2. Use EXISTS instead of IN                         │ │
    │ │ 3. Denormalize for simpler policy                    │ │
    │ │ 4. Create helper function                           │ │
    │ └───────────────────────────────────────────────────────┘ │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## 8. Testing Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              TESTING DECISION TREE                                │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ What to test?                    │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [Policy Logic] [Performance] │         [Security]
           │              │              │
           ▼              ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │Unit test    │ │EXPLAIN      │ │Edge cases  │
    │Helper funcs │ │ANALYZE      │ │Testing    │
    │             │ │Query plans  │ │           │
    └─────────────┘ └──────────────┘ └────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ POLICY TESTING SCENARIOS:                                    │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │ 1. REGULAR USER:                                            │
    │    SET ROLE authenticated;                                   │
    │    SET LOCAL request.jwt.claims = '{"sub":"user-uuid"}';    │
    │    SELECT * FROM table;  -- Should see own data only         │
    │                                                              │
    │ 2. ADMIN USER:                                              │
    │    SET LOCAL request.jwt.claims = '{"sub":"admin-uuid",    │
    │              "app_metadata":{"role":"admin"}}';             │
    │    SELECT * FROM table;  -- Should see all or admin data    │
    │                                                              │
    │ 3. UNAUTHENTICATED:                                         │
    │    RESET ROLE;                                              │
    │    SELECT * FROM table;  -- Should return empty or error   │
    │                                                              │
    │ 4. EDGE CASES:                                              │
    │    • NULL user_id                                           │
    │    • Invalid UUID                                           │
    │    • Empty results                                          │
    │    • SQL injection attempts                                 │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## 9. Deployment Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              DEPLOYMENT DECISION TREE                            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ When to enable RLS?              │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [During table] [After table exists]
           │              │
           ▼              ▼
    ┌─────────────┐ ┌──────────────┐
    │Enable with │ │Careful:      │
    │initial     │ │1. Create policies first │
    │CREATE      │ │2. Test thoroughly   │
    │             │ │3. Enable RLS       │
    │             │ │4. Monitor closely  │
    └─────────────┘ └──────────────┘
                                │
                                ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ DEPLOYMENT STRATEGY:                                        │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │ OPTION 1: Migration-based (Recommended)                     │
    │                                                              │
    │ migrations/001_create_tables.sql                             │
    │ migrations/002_enable_rls.sql                                 │
    │ migrations/003_add_policies.sql                              │
    │ migrations/004_add_indexes.sql                               │
    │                                                              │
    │ OPTION 2: Single migration (Simple tables)                  │
    │                                                              │
    │ CREATE TABLE ...;                                           │
    │ ALTER TABLE ... ENABLE ROW LEVEL SECURITY;                   │
    │ CREATE POLICY ...;                                          │
    │ CREATE INDEX ...;                                            │
    │                                                              │
    │ OPTION 3: Phased rollout (Large tables)                     │
    │                                                              │
    │ Phase 1: Create policies, enable RLS in permissive mode      │
    │ Phase 2: Monitor for issues                                 │
    │ Phase 3: Switch to enforce mode                            │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## 10. Troubleshooting Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              TROUBLESHOOTING DECISION TREE                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Problem: No access to table      │
              └─────────────────────────────────┘
                    │
                    ▼
    ┌─────────────────────────────────────────┐
    │ Checklist:                               │
    │ 1. RLS enabled?                        │
    │    SELECT relrowsecurity FROM pg_class  │
    │    WHERE relname = 'table_name';        │
    │                                         │
    │ 2. Policy exists?                      │
    │    SELECT * FROM pg_policies            │
    │    WHERE tablename = 'table_name';      │
    │                                         │
    │ 3. auth.uid() returns value?            │
    │    SELECT auth.uid();                   │
    │                                         │
    │ 4. Policy condition matches?            │
    │    Test with SET ROLE;                 │
    └─────────────────────────────────────────┘
                    │
                    ▼
    ┌─────────────────────────────────────────────────────────────┐
    │ ISSUE → SOLUTION MAPPING:                                   │
    ├─────────────────────────────────────────────────────────────┤
    │                                                              │
    │ RLS not enabled?                                            │
    │        ↓                                                     │
    │ ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;            │
    │                                                              │
    │ No policies exist?                                          │
    │        ↓                                                     │
    │ CREATE POLICY ...;                                          │
    │                                                              │
    │ auth.uid() is NULL?                                         │
    │        ↓                                                     │
    │ • Check Authorization header                                │
    │ • Verify JWT is valid                                       │
    │ • Ensure role is authenticated                             │
    │                                                              │
    │ Policy condition doesn't match?                             │
    │        ↓                                                     │
    │ • Check policy logic                                        │
    │ • Test with direct query                                   │
    │ • Review EXPLAIN output                                    │
    │                                                              │
    │ Performance issues?                                        │
    │        ↓                                                     │
    │ • Add indexes on policy columns                             │
    │ • Simplify policy conditions                               │
    │ • Use covering indexes                                     │
    │                                                              │
    └─────────────────────────────────────────────────────────────┘
```
