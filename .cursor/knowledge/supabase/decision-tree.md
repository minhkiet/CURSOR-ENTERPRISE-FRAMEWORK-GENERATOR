# Supabase Decision Tree - Cây Quyết Định

## Giới thiệu

Tài liệu này cung cấp cây quyết định để hướng dẫn việc lựa chọn các giải pháp và cấu hình phù hợp cho Supabase trong các tình huống khác nhau.

---

## 1. Authentication Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              AUTHENTICATION METHOD SELECTION                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ What authentication methods     │
              │ do you need?                     │
              └─────────────────────────────────┘
                    │              │              │
            ┌───────┴───────┐      │              │
            │               │      │              │
         [Email +      [OAuth]    [Phone/SMS]   [Magic Link]
          Password]                       │
            │               │              │
            └───────┬───────┘              │
                    │                      │
                    ▼                      ▼
           ┌────────────────┐    ┌─────────────────┐
           │ Email/Password │    │ MFA required?   │
           │ - Simple       │    │                  │
           │ - Most common  │    └────────┬────────┘
           └────────────────┘              │
                              ┌────────────┴────────────┐
                             [Yes]                    [No]
                              │                         │
                              ▼                         ▼
                    ┌─────────────────┐      ┌─────────────────┐
                    │ Implement TOTP  │      │ Basic OAuth     │
                    │ (Authenticator)│      │ Setup           │
                    └─────────────────┘      └─────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ OAuth Providers?                 │
              └─────────────────────────────────┘
                    │              │              │
            ┌───────┴───────┐      │              │
           [Google]    [GitHub]   [More]       [None]
            │           │         │              │
            └─────┬─────┘         │              │
                  │               ▼              │
                  │      ┌─────────────────┐    │
                  │      │ Provider List:  │    │
                  │      │ - Facebook      │    │
                  │      │ - Twitter/X     │    │
                  │      │ - Apple         │    │
                  │      │ - Microsoft     │    │
                  │      │ - Discord       │    │
                  │      │ - And 20+ more  │    │
                  │      └─────────────────┘    │
                  ▼                             │
           ┌─────────────────────┐               │
           │ Configure in        │               │
           │ Supabase Dashboard │               │
           │ + Add credentials   │               │
           └─────────────────────┘               │
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Session Management Strategy?     │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐      │              │
          [Auto-refresh]    [Manual]  [JWT-only]   [Custom]
           │                 │        │              │
           └────────┬────────┘        │              │
                    │                 ▼              │
                    │         ┌─────────────────┐    │
                    │         │ Verify token   │    │
                    │         │ on each request │    │
                    │         └─────────────────┘    │
                    ▼                             │
           ┌─────────────────────┐               │
           │ onAuthStateChange   │               │
           │ + Auto-refresh     │               │
           │ (Recommended)       │               │
           └─────────────────────┘               │

    ┌─────────────────────────────────────────────────────────────┐
    │ RECOMMENDATIONS:                                           │
    ├─────────────────────────────────────────────────────────────┤
    │ • Start with Email/Password + OAuth (Google, GitHub)       │
    │ • Add MFA for sensitive applications                        │
    │ • Use magic link for passwordless experience               │
    │ • Always listen to onAuthStateChange for session sync      │
    └─────────────────────────────────────────────────────────────┘
```

---

## 2. Database Design Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              DATABASE DESIGN DECISIONS                           │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 1. Primary Key Type              │
              └─────────────────────────────────┘
                    │              │              │
            ┌───────┴───────┐      │              │
           [UUID v4]    [Serial]  [BigSerial]   [Custom]
            │           │        │              │
            ▼           └────────┴──────────────┘
    ┌─────────────────────┐
    │ RECOMMEND: UUID     │
    │ • Mergeable across  │
    │   systems           │
    │ • No guessable IDs  │
    │ • Global uniqueness │
    └─────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 2. Relationships?                │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [One-to-Many]    [Many-to-Many]    [One-to-One]
           │               │                 │
           ▼               ▼                 ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────────┐
    │ FOREIGN KEY │ │ Junction     │ │ Same PK in     │
    │ REFERENCES  │ │ Table        │ │ both tables    │
    └─────────────┘ └──────────────┘ └────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 3. Index Strategy?               │
              └─────────────────────────────────┘
                    │              │              │
            ┌───────┴───────┐      │              │
           [Foreign Keys] [Search]  [Unique]     [Composite]
            │               │        │              │
            ▼               ▼        ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐ ┌────────────┐
    │Always index │ │GIN/Trigram   │ │UNIQUE      │ │Multi-col   │
    │FK columns  │ │for text      │ │constraint  │ │covering    │
    └─────────────┘ └──────────────┘ └────────────┘ └────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 4. Data Types?                   │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [Text/Strings]  [Numbers]  [Date/Time]    [Complex]
           │               │        │              │
           ▼               ▼        ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐ ┌────────────┐
    │TEXT (var)   │ │DECIMAL (not │ │TIMESTAMPTZ │ │JSONB       │
    │not VARCHAR(n)│ │FLOAT) for   │ │(not DATE/  │ │(not JSON)  │
    │             │ │money        │ │DATETIME)   │ │for flex   │
    └─────────────┘ └──────────────┘ └────────────┘ └────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ SECURITY DECISION:                                          │
    ├─────────────────────────────────────────────────────────────┤
    │ Enable RLS on ALL user tables?                            │
    │        │                                                    │
    │   ┌────┴────┐                                               │
    │  [Yes]     [No]                                             │
    │   │         │                                               │
    │   ▼         ▼                                               │
    │ ┌───────────────┐                                          │
    │ │ • auth.uid()  │                                          │
    │ │ • Policies    │                                          │
    │ │ • auth.jwt()  │                                          │
    │ └───────────────┘                                          │
    │                                                              │
    │ ┌────────────────────────────────────────────────────────┐  │
    │ │ NEVER expose service_role key in client code         │  │
    │ │ NEVER skip RLS for "simplicity"                      │  │
    │ └────────────────────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────────────────┘
```

---

## 3. API Selection Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              API METHOD SELECTION                                │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ What type of operation?         │
              └─────────────────────────────────┘
                    │              │              │
                    ▼              ▼              ▼
            ┌─────────────┐ ┌──────────────┐ ┌────────────┐
            │   Simple    │ │   Complex    │ │  Real-time │
            │   CRUD      │ │  Business    │ │  Updates   │
            └─────────────┘ └──────────────┘ └────────────┘
                    │              │              │
                    ▼              ▼              ▼
            ┌─────────────┐ ┌──────────────┐ ┌────────────┐
            │Query Builder│ │   RPC/       │ │Subscribe   │
            │ (direct)    │ │  Functions   │ │to channel  │
            └─────────────┘ └──────────────┘ └────────────┘
                    │              │              │
                    ▼              ▼              ▼
            ┌─────────────┐ ┌──────────────┐ ┌────────────┐
            │.from()      │ │.rpc()         │ │postgres_   │
            │.select()    │ │Stored         │ │changes()   │
            │.eq()        │ │procedures     │ │             │
            └─────────────┘ └──────────────┘ └────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Complex query scenario?         │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [Joins/Aggs]    [Transactions]    [Search/Fulltext]
           │               │                 │
           ▼               ▼                 ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │.select()     │ │RPC with      │ │textSearch() │
    │with embed   │ │BEGIN/        │ │or ILIKE     │
    │             │ │COMMIT        │ │with GIN    │
    └─────────────┘ └──────────────┘ └────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ QUERY METHOD DECISION MATRIX                                │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │ Operation              │ Best Method                        │
    │ ───────────────────────┼───────────────────────────────     │
    │ Get single row        │ .eq().single()                     │
    │ Get all matching      │ .select().eq().order()              │
    │ Get with pagination   │ .select().range(0, 9)             │
    │ Get with joins        │ .select('*, table(*)')              │
    │ Complex aggregations  │ RPC function                       │
    │ Insert single row     │ .insert(object)                    │
    │ Insert multiple rows  │ .insert(array)                     │
    │ Update by condition   │ .update().eq()                    │
    │ Upsert                │ .upsert(array, { onConflict: 'id' })│
    │ Delete soft           │ .update({ deleted_at: now }).eq()  │
    │ Delete hard           │ .delete().eq()                    │
    │ Real-time changes     │ .on('postgres_changes', ...)       │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

---

## 4. Storage Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              STORAGE DECISION TREE                               │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 1. Bucket Type?                 │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [Public]         [Private]
           │               │
           ▼               ▼
    ┌─────────────┐ ┌──────────────┐
    │ .getPublicUrl()│ │Signed URL   │
    │ works        │ │required      │
    └─────────────┘ └──────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 2. Access Control Level?         │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [Bucket-level]    [File-level]    [Custom]
           │               │                 │
           ▼               ▼                 ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │ RLS on      │ │ RLS with     │ │Edge         │
    │ metadata    │ │ storage.path │ │Function     │
    │ table       │ │ check        │ │middleware   │
    └─────────────┘ └──────────────┘ └─────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 3. File Size Strategy?           │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [<5MB]        [5-50MB]    [>50MB]
           │               │                 │
           ▼               ▼                 ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │ Direct      │ │Chunked       │ │Multipart    │
    │ upload      │ │upload        │ │upload       │
    │ (default)   │ │or XHR with   │ │(S3-like)    │
    │             │ │progress      │ │             │
    └─────────────┘ └──────────────┘ └─────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 4. Image Processing?             │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [Transform]      [No transform]
           │               │
           ▼               ▼
    ┌─────────────┐ ┌──────────────┐
    │ CDN-based   │ │Store original│
    │ transforms   │ │Serve as-is  │
    │ (with URL)  │ │             │
    └─────────────┘ └──────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ BUCKET ORGANIZATION RECOMMENDATION:                         │
    ├─────────────────────────────────────────────────────────────┤
    │ • avatars/       → User profile pictures (public)          │
    │ • posts/         → Post images (public)                   │
    │ • documents/     → Private files (private)                │
    │ • backups/        → Database/file backups (private)        │
    │ • temp/           → Temporary uploads (auto-cleanup)       │
    └─────────────────────────────────────────────────────────────┘
```

---

## 5. Edge Functions Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              EDGE FUNCTION DECISION TREE                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Do you need Edge Function?      │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [Yes]            [No]
           │               │
           ▼               ▼
    ┌─────────────┐ ┌──────────────┐
    │ Use Query   │  │Use direct    │
    │ Builder +   │  │Supabase      │
    │ RPC         │  │client        │
    └─────────────┘ └──────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 1. Authentication Required?      │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [Yes]            [No]
           │               │
           ▼               ▼
    ┌─────────────┐ ┌──────────────┐
    │ Verify JWT  │ │Public        │
    │ in header   │ │endpoint      │
    └─────────────┘ └──────────────┘
           │               │
           └───────┬───────┘
                   │
                   ▼
              ┌─────────────────────────────────┐
              │ 2. Database Access Level?        │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [User-scoped]  [Admin]
           │               │
           ▼               ▼
    ┌─────────────┐ ┌──────────────┐
    │ Anon key    │ │Service role  │
    │ + RLS       │ │key (NEVER    │
    │             │ │expose!)      │
    └─────────────┘ └──────────────┘
           │               │
           └───────┬───────┘
                   │
                   ▼
              ┌─────────────────────────────────┐
              │ 3. When to use Edge Functions?   │
              └─────────────────────────────────┘
                   │          │        │         │
           ┌───────┴───┐      │        │         │
          [Webhook]  [Email]  │        │    [Complex]
           │        │        │        │    Logic
           ▼        ▼        ▼        ▼    │
    ┌─────────────┐┌─────────────┐┌────────────┐│
    │Receive from ││Send via    ││Process    ││
    │Stripe, etc.││SendGrid,   ││AI/ML      ││
    │Validate &   ││Resend      ││operations ││
    │Store        ││Generate &  ││           ││
    │             ││Send        ││           ││
    └─────────────┘└─────────────┘└────────────┘│
                                                 │
                              ┌──────────────────┘
                              │
                              ▼
              ┌─────────────────────────────────┐
              │ 4. Runtime Considerations?        │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [Cold Start]    [Long Running]
           │               │
           ▼               ▼
    ┌─────────────┐ ┌──────────────┐
    │~300ms-1s    │ │Consider job  │
    │Minimize     │ │queue or     │
    │dependencies  │ │background   │
    │             │ │workers      │
    └─────────────┘ └──────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ EDGE FUNCTION SECURITY CHECKLIST:                           │
    ├─────────────────────────────────────────────────────────────┤
    │ □ Always verify JWT token                                  │
    │ □ Validate and sanitize all inputs                         │
    │ □ Use parameterized queries (prevent SQL injection)         │
    │ □ Never log sensitive data                                 │
    │ □ Set proper CORS headers                                  │
    │ □ Use environment variables for secrets                    │
    │ □ Implement rate limiting for public endpoints             │
    └─────────────────────────────────────────────────────────────┘
```

---

## 6. Realtime Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              REALTIME DECISION TREE                              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Do you need realtime?            │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [Yes]            [No]
           │               │
           ▼               ▼
    ┌─────────────┐ ┌──────────────┐
    │Use polling │  │Regular       │
    │or periodic │  │queries       │
    │refresh     │  │(simpler)     │
    └─────────────┘ └──────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 1. What type of realtime?       │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [Database]      [Direct]  [Presence]    [Mixed]
           │changes         │        │              │
           ▼                ▼        ▼              ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐ ┌────────────┐
    │postgres_    │ │broadcast()  │ │presence   │ │Combine     │
    │changes()    │ │             │ │tracking   │ │all three  │
    │             │ │For typing   │ │            │ │in one     │
    │For sync     │ │indicators,  │ │Online     │ │channel    │
    │data state   │ │cursors      │ │status     │ │           │
    └─────────────┘ └──────────────┘ └────────────┘ └────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 2. Subscription Scope?           │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [All changes]    [Filtered]
           │               │
           ▼               ▼
    ┌─────────────┐ ┌──────────────┐
    │ event: '*' │ │ event: 'INSERT'│
    │Subscribe   │ │ filter:       │
    │to all      │ │ 'room_id=eq.1'│
    └─────────────┘ └──────────────┘
           │               │
           └───────┬───────┘
                   │
                   ▼
              ┌─────────────────────────────────┐
              │ 3. Channel Management?           │
              └─────────────────────────────────┘
                   │          │        │
           ┌───────┴───┐      │        │
          [Reuse]  [Create]   │   [Clean up]
           │        │new     │       │
           ▼        ▼        ▼       ▼
    ┌─────────────┐┌─────────────┐┌────────────┐
    │Single       ││Unique       ││removeChannel()│
    │channel      ││channel per  ││on unmount    │
    │for app      ││room/user    ││              │
    └─────────────┘└─────────────┘└────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ REALTIME PERFORMANCE TIPS:                                  │
    ├─────────────────────────────────────────────────────────────┤
    │ • Filter subscriptions whenever possible                    │
    │ • Clean up subscriptions in useEffect cleanup               │
    │ • Use separate channels for different concerns              │
    │ • Don't subscribe to all events when you only need INSERT   │
    │ • Consider connection pooling for many simultaneous users    │
    │ • Monitor subscription limits and connection counts         │
    └─────────────────────────────────────────────────────────────┘
```

---

## 7. Security Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              SECURITY DECISION TREE                              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 1. API Key Type?                 │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [Anon Key]     [Service Role]
           │               │
           ▼               ▼
    ┌─────────────┐ ┌──────────────┐
    │✓ Safe in    │ │✗ NEVER in   │
    │client code │ │client code   │
    │✓ Respects  │ │✓ Bypasses    │
    │RLS policies │ │RLS policies  │
    └─────────────┘ └──────────────┘
           │               │
           └───────┬───────┘
                   │
                   ▼
              ┌─────────────────────────────────┐
              │ 2. RLS Policies Required?       │
              └─────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │ Enable RLS on ALL tables  │
        │ containing user data?      │
        └───────────────────────────┘
                    │
           ┌────────┴────────┐
          [Yes]            [No - STOP!]
           │               │
           ▼               ▼
    ┌─────────────┐ ┌──────────────┐
    │Create per-  │ │You WILL have │
    │table        │ │security      │
    │policies     │ │vulnerabilities│
    └─────────────┘ └──────────────┘
           │
           ▼
    ┌─────────────────────────────────────────┐
    │ POLICY TYPES FOR EACH TABLE:            │
    ├─────────────────────────────────────────┤
    │                                         │
    │ SELECT: Who can view the data?          │
    │   - Public: USING (true)                │
    │   - Owner: USING (auth.uid() = user_id) │
    │                                         │
    │ INSERT: Who can create data?            │
    │   - Users: WITH CHECK (auth.uid() = ...)│
    │                                         │
    │ UPDATE: Who can modify data?            │
    │   - Owner: USING (auth.uid() = user_id) │
    │   - Admin: USING (is_admin())          │
    │                                         │
    │ DELETE: Who can remove data?            │
    │   - Owner: USING (auth.uid() = user_id) │
    │   - Admin: USING (is_admin())          │
    │                                         │
    └─────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 3. Data Sensitivity?            │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [Sensitive]    [Non-Sensitive]
           │               │
           ▼               ▼
    ┌─────────────┐ ┌──────────────┐
    │• Enable TDE│ │• Standard    │
    │• Encrypt   │ │RLS policies  │
    │columns     │ │sufficient    │
    │• Use Vault │ │              │
    └─────────────┘ └──────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ 4. Row-Level Security Helper?    │
              └─────────────────────────────────┘
                    │
                    ▼
           ┌─────────────────────────┐
           │ Create helper functions: │
           ├─────────────────────────┤
           │ • auth.uid()            │
           │ • auth.jwt()           │
           │ • is_admin()            │
           │ • has_role('moderator')│
           │ • tenant_id()           │
           └─────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ SECURITY AUDIT CHECKLIST:                                   │
    ├─────────────────────────────────────────────────────────────┤
    │ □ RLS enabled on all user tables                           │
    │ □ Service role key never exposed to client                 │
    │ □ All inputs validated and sanitized                       │
    │ □ SQL injection prevented (parameterized queries)           │
    │ □ Rate limiting on public endpoints                        │
    │ □ CORS configured for allowed origins only                 │
    │ □ Sensitive data encrypted at rest                         │
    │ □ HTTPS enforced for all connections                       │
    │ □ Audit logging for sensitive operations                  │
    │ □ Regular security reviews and penetration testing         │
    └─────────────────────────────────────────────────────────────┘
```

---

## 8. Performance Optimization Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              PERFORMANCE DECISION TREE                           │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Performance Issue Type?          │
              └─────────────────────────────────┘
                    │              │              │
                    ▼              ▼              ▼
            ┌─────────────┐ ┌──────────────┐ ┌────────────┐
            │ Slow Queries│ │ High Memory   │ │ Too Many   │
            │             │ │ Usage         │ │ Requests   │
            └─────────────┘ └──────────────┘ └─────────────┘
                    │              │              │
                    ▼              ▼              ▼
    ┌───────────────────┐┌───────────────┐┌───────────────┐
    │ 1. Check EXPLAIN   ││1. Reduce data ││1. Implement   │
    │ 2. Add indexes     ││transferred    ││caching        │
    │ 3. Optimize query  ││2. Use         ││2. Batch       │
    │ 4. Use RPC        ││pagination     ││requests       │
    │ 5. Covering index  ││3. Avoid       ││3. Debounce    │
    │                   ││SELECT *       ││4. Rate limit  │
    └───────────────────┘└───────────────┘└───────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ QUERY OPTIMIZATION CHECKLIST:    │
              └─────────────────────────────────┘
                    │
                    ▼
           ┌─────────────────────────┐
           │ □ SELECT only needed     │
           │   columns (not *)        │
           │                          │
           │ □ Index foreign keys     │
           │                          │
           │ □ Use .single() for     │
           │   single row results     │
           │                          │
           │ □ Use .in() for batch   │
           │   queries, not loops     │
           │                          │
           │ □ Add partial indexes    │
           │   for common filters     │
           │                          │
           │ □ Use covering indexes   │
           │   for include columns    │
           │                          │
           │ □ Paginate large        │
           │   result sets           │
           │                          │
           │ □ Use RPC for complex   │
           │   aggregations          │
           │                          │
           │ □ Filter before join    │
           │   (reduce join size)    │
           └─────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ INDEX TYPE SELECTION:            │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [B-tree]        [GIN]     [Hash]
           │               │         │
           ▼               ▼         ▼
    ┌─────────────┐ ┌──────────────┐┌────────────┐
    │Equality    │ │Full-text    ││Large IN    │
    │Range       │ │search       ││clauses     │
    │Sorting     │ │JSONB        ││(rare)      │
    │            │ │Array        ││            │
    └─────────────┘ └──────────────┘└────────────┘
           │
           ▼
    ┌─────────────────────────────────────────┐
    │ COMPOSITE INDEX COLUMN ORDER:             │
    ├─────────────────────────────────────────┤
    │ 1. Columns with equality conditions ( = )│
    │    first                                │
    │ 2. Columns with range conditions (>, <) │
    │    second                               │
    │ 3. Columns used for sorting (ORDER BY)  │
    │    last                                 │
    │                                         │
    │ Example: WHERE status = 'active'       │
    │           AND category = 'books'        │
    │           AND created_at > '2024-01-01'│
    │           ORDER BY created_at DESC      │
    │                                         │
    │ Good index: (status, category, created_at)│
    └─────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ WHEN TO USE RPC INSTEAD OF QUERIES:                          │
    ├─────────────────────────────────────────────────────────────┤
    │ • Complex joins across multiple tables                       │
    │ • Business logic that shouldn't be exposed to client        │
    │ • Transactions that need atomicity                          │
    │ • Heavy aggregations or computations                        │
    │ • Dynamic pivot tables or complex reporting                  │
    │ • When you need to protect proprietary logic                │
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
              │ Environment Setup?               │
              └─────────────────────────────────┘
                    │              │              │
           ┌────────┴────────┐     │              │
          [Development]  [Staging]   [Production]
           │               │                 │
           ▼               ▼                 ▼
    ┌─────────────┐ ┌──────────────┐ ┌────────────┐
    │Local CLI   │ │Preview       │ │Production  │
    │ supabase   │ │deployments   │ │deployments │
    │ start      │ │             │ │            │
    └─────────────┘ └──────────────┘ └────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Deployment Method?               │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [Git-based]    [Manual]
           │               │
           ▼               ▼
    ┌─────────────┐ ┌──────────────┐
    │ CI/CD with  │ │supabase CLI │
    │ GitHub      │ │commands     │
    │ Actions     │ │            │
    └─────────────┘ └──────────────┘
           │
           ▼
    ┌─────────────────────────────────────────┐
    │ CI/CD PIPELINE STEPS:                     │
    ├─────────────────────────────────────────┤
    │                                          │
    │ 1. Lint & Type Check                    │
    │    └─ eslint, tsc --noEmit             │
    │                                          │
    │ 2. Run Tests                            │
    │    └─ unit, integration, e2e           │
    │                                          │
    │ 3. Database Migrations                   │
    │    └─ supabase db push (dry-run)        │
    │    └─ supabase db push                  │
    │                                          │
    │ 4. Deploy Edge Functions                │
    │    └─ supabase functions deploy         │
    │                                          │
    │ 5. Verify Deployment                    │
    │    └─ health checks                     │
    │    └─ smoke tests                      │
    │                                          │
    └─────────────────────────────────────────┘
                                │
                                ▼
              ┌─────────────────────────────────┐
              │ Migration Strategy?              │
              └─────────────────────────────────┘
                    │              │
           ┌────────┴────────┐     │
          [Zero-downtime]  [Maintenance]
           │               │
           ▼               ▼
    ┌─────────────┐ ┌──────────────┐
    │Backward-   │ │Scheduled    │
    │compatible  │ │maintenance  │
    │changes     │ │window       │
    └─────────────┘ └──────────────┘
           │
           ▼
    ┌─────────────────────────────────────────┐
    │ ZERO-DOWNTIME MIGRATION PATTERN:          │
    ├─────────────────────────────────────────┤
    │                                          │
    │ Phase 1: Add new structure              │
    │   └─ Add nullable columns                │
    │   └─ Add new tables                     │
    │   └─ Add new indexes (CONCURRENTLY)     │
    │                                          │
    │ Phase 2: Deploy application              │
    │   └─ Deploy code that writes to both     │
    │   └─ Read from new structure             │
    │                                          │
    │ Phase 3: Backfill data                   │
    │   └─ Background job to populate         │
    │   └─ new columns/tables                  │
    │                                          │
    │ Phase 4: Remove old structure            │
    │   └─ Only after full backfill           │
    │   └─ Remove nullable constraint         │
    │   └─ Drop old columns (later)           │
    │                                          │
    └─────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │ PRE-DEPLOYMENT CHECKLIST:                                   │
    ├─────────────────────────────────────────────────────────────┤
    │ □ Test locally with supabase db reset                      │
    │ □ Review migration files                                    │
    │ □ Verify environment variables                              │
    │ □ Check API key rotation                                   │
    │ □ Review RLS policies                                      │
    │ □ Test with staging environment                            │
    │ □ Document rollback procedure                              │
    │ □ Notify stakeholders                                      │
    │ □ Schedule maintenance window (if needed)                  │
    │ □ Set up monitoring alerts                                 │
    └─────────────────────────────────────────────────────────────┘
```
