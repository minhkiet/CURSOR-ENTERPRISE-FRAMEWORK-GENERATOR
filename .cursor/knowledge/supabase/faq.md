---
title: "Supabase FAQ"
description: "Câu hỏi thường gặp về Supabase với câu trả lời chuyên sâu từ experts"
tags: ["supabase", "faq", "questions", "answers", "troubleshooting", "postgres"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Supabase FAQ

## Overview

Tài liệu này compile các câu hỏi thường gặp về Supabase từ developers, architects, và teams mới bắt đầu với platform. Mỗi câu hỏi được trả lời với expert-level detail, bao gồm explanations, examples, và references.

Câu hỏi được organize theo categories để facilitate quick lookup. Technical questions bao gồm code examples trong TypeScript/SQL để provide practical answers.

This FAQ addresses common misconceptions và provides clarity on Supabase's architecture và best practices. Questions range từ basic concepts đến advanced troubleshooting scenarios.

## General Questions

### Q1: What is Supabase and how does it compare to Firebase?

**Answer:**

Supabase là một open-source Backend-as-a-Service (BaaS) platform được xây dựng trên PostgreSQL. Nó cung cấp database, authentication, realtime subscriptions, file storage, và edge functions trong một unified solution.

**Key Differences from Firebase:**

| Aspect | Supabase | Firebase |
|--------|----------|----------|
| Database Type | PostgreSQL (Relational SQL) | Firestore (NoSQL Document) |
| Query Model | Full SQL with joins | Document queries |
| Pricing Model | Based on database size and usage | Based on operations |
| Open Source | Full open source | Proprietary |
| Self-Hosting | Yes, complete | Limited (only some services) |
| Real-time | PostgreSQL logical replication | Native Firestore listeners |
| Data Portability | Complete SQL export | Proprietary format |

**When to Choose Supabase:**
- Need complex queries with joins and aggregations
- Require ACID transactions across multiple documents
- Want to use PostgreSQL features (JSONB, full-text search, pgvector)
- Prefer SQL-based data modeling
- Need data portability and vendor independence

**When to Choose Firebase:**
- Mobile-first development with strong offline support
- Simple document-based data model
- Heavy reliance on Firebase ecosystem (Cloud Functions, Analytics)
- Real-time sync is the primary use case

```typescript
// Supabase query example (SQL-style joins)
const { data } = await supabase
    .from('posts')
    .select(`
        id,
        title,
        author:users!user_id (
            id,
            name,
            avatar_url
        ),
        comments (
            id,
            content,
            created_at
        )
    `)
    .eq('status', 'published')
    .order('created_at', { ascending: false });
```

### Q2: Can I self-host Supabase?

**Answer:**

Yes, Supabase is fully open source and can be self-hosted. The complete Supabase stack can be deployed using Docker and includes:

- PostgreSQL database
- PostgREST (auto-generated API)
- GoTrue (authentication)
- Realtime server
- Storage API
- Edge Functions runtime
- pgBouncer (connection pooling)

**Self-Hosting Options:**

1. **Docker Compose**: Quick setup for development and small-scale production

```bash
# Clone the repository
git clone https://github.com/supabase/supabase

# Navigate to docker folder
cd supabase/docker

# Copy environment file
cp .env.example .env

# Start services
docker-compose up -d
```

2. **Kubernetes**: Production-grade deployment with Helm charts

```bash
# Add Supabase Helm repository
helm repo add supabase https://charts.supabase.com

# Install with custom values
helm install my-supabase supabase/supabase -f values.yaml
```

3. **Managed Services**: For production, many teams use Supabase Cloud or services like Railway, Render, or Fly.io.

**Self-Hosting Considerations:**

- **Database Management**: You manage backups, updates, and maintenance
- **Scalability**: You handle scaling decisions and infrastructure
- **Cost**: Infrastructure costs but no per-seat pricing
- **Compliance**: Full control over data residency and compliance

### Q3: What are Supabase's limits on the free tier?

**Answer:**

Supabase's free tier (Hobby tier) provides generous limits suitable for development and small projects:

**Database:**
- 500MB storage
- Up to 2GB transfer/month
- 60 concurrent connections (with PgBouncer)
- Point-in-time recovery disabled

**Auth:**
- 50,000 monthly active users
- Email/password, OAuth providers supported
- Magic links included

**Storage:**
- 1GB storage
- 2GB bandwidth/month
- Public buckets supported

**Realtime:**
- Up to 200 concurrent connections
- 2GB bandwidth/month

**Edge Functions:**
- 500,000 invocations/month
- 100GB-hours compute/month
- 2GB request/response size

**Important Notes:**
- Limits are per project, not per organization
- Exceeding limits triggers automatic upgrades or rate limiting
- Free tier is rate-limited, not shut off
- Pro tier starts at $25/month with expanded limits

## Security Questions

### Q4: How do I prevent SQL injection with Supabase?

**Answer:**

SQL injection is prevented through parameterization when using the Supabase client libraries. The client uses prepared statements internally, ensuring all user input is properly escaped.

**Safe Usage:**

```typescript
// ✅ Safe: Using Supabase client (parameterized)
const { data } = await supabase
    .from('posts')
    .select('*')
    .ilike('title', `%${searchQuery}%`); // Parameterized

// ✅ Safe: Database functions with parameters
await supabase.rpc('search_posts', { query: searchQuery });

// ✅ Safe: Raw SQL with proper escaping
const { data } = await supabase
    .from('posts')
    .select('*')
    .filter('title', 'ilike', `%${searchQuery}%`);
```

**Dangerous Patterns to Avoid:**

```typescript
// ❌ DANGEROUS: String concatenation in raw SQL
// Never do this - creates SQL injection vulnerability
await supabase.rpc('unsafe_raw_sql', { 
    query: `SELECT * FROM users WHERE name = '${userInput}'` 
});
```

**Database Function Best Practices:**

```sql
-- Safe: Use parameterized queries in functions
CREATE OR REPLACE FUNCTION search_users(search_term TEXT)
RETURNS SETOF users AS $$
BEGIN
    RETURN QUERY SELECT * FROM users WHERE name ILIKE '%' || search_term || '%';
END;
$$ LANGUAGE plpgsql;

-- Safe: Use format() with %I for identifiers
CREATE OR REPLACE FUNCTION get_table_data(table_name TEXT)
RETURNS SETOF RECORD AS $$
DECLARE
    query_text TEXT;
    result RECORD;
BEGIN
    -- %I escapes the identifier safely
    query_text := format('SELECT * FROM %I LIMIT 100', table_name);
    RETURN QUERY EXECUTE query_text;
END;
$$ LANGUAGE plpgsql;
```

**Additional Security Layers:**

1. **RLS Policies**: Enable RLS to add database-level access control
2. **Input Validation**: Validate and sanitize input at the application layer
3. **Least Privilege**: Use anon key with RLS instead of service role key

### Q5: Should I use anon key or service role key?

**Answer:**

**Use Anon Key (Public, Client-Side):**

The anon key is designed for client-side usage and respects RLS policies. This is the preferred approach for most applications.

```typescript
// ✅ Correct: Client-side usage with anon key
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
    'https://your-project.supabase.co',
    'your-anon-key' // Public, safe for client
);

// Operations respect RLS policies
const { data } = await supabase.from('posts').select('*');
// Returns only rows allowed by RLS policies for this user
```

**Use Service Role Key (Private, Server-Side Only):**

The service role key bypasses RLS entirely. Use it only in server-side code where you need admin privileges.

```typescript
// ✅ Correct: Server-side usage with service role key
import { createClient } from '@supabase/supabase-js';

const supabaseAdmin = createClient(
    'https://your-project.supabase.co',
    process.env.SUPABASE_SERVICE_ROLE_KEY // Private, never expose
);

// Bypasses RLS - use for admin operations only
const { data } = await supabaseAdmin.from('all_users').select('*');
```

**Security Guidelines:**

| Scenario | Key to Use | Reason |
|----------|-------------|--------|
| Web/Mobile client | Anon Key | RLS controls access |
| Server-side API routes | Service Role | Admin access needed |
| Edge Functions (with RLS) | Anon Key | RLS still applies |
| Edge Functions (admin) | Service Role | Bypass RLS for specific ops |
| Background jobs | Service Role | Admin access needed |

**Common Mistakes:**

```typescript
// ❌ WRONG: Service role key in client code
const supabase = createClient(url, serviceRoleKey);
// This bypasses RLS and exposes all data!
```

### Q6: How do I implement multi-tenancy with RLS?

**Answer:**

Multi-tenancy can be implemented efficiently using RLS with a tenant_id column and membership table.

**Schema Design:**

```sql
-- Tenants table
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tenant members
CREATE TABLE tenant_members (
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    role TEXT DEFAULT 'member' CHECK (role IN ('owner', 'admin', 'member')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (tenant_id, user_id)
);

-- Tenant-scoped tables
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**RLS Policies:**

```sql
-- Enable RLS on all tenant tables
ALTER TABLE tenant_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Helper function to get user's accessible tenants
CREATE OR REPLACE FUNCTION get_user_tenant_ids()
RETURNS SETOF UUID
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
    SELECT tenant_id FROM tenant_members WHERE user_id = auth.uid();
$$;

-- Policy for tenant_members (user sees own memberships)
CREATE POLICY "tenant_members_select" ON tenant_members
    FOR SELECT
    USING (user_id = auth.uid());

-- Policy for projects (user sees their tenant's projects)
CREATE POLICY "projects_select" ON projects
    FOR SELECT
    USING (tenant_id IN (SELECT get_user_tenant_ids()));

CREATE POLICY "projects_insert" ON projects
    FOR INSERT
    WITH CHECK (tenant_id IN (SELECT get_user_tenant_ids()));
```

**Application Usage:**

```typescript
// User's tenants
const { data: memberships } = await supabase
    .from('tenant_members')
    .select('*, tenant:tenants(*)')
    .eq('user_id', userId);

// Projects for user's tenant
const { data: projects } = await supabase
    .from('projects')
    .select('*')
    .eq('tenant_id', currentTenantId);
```

## Performance Questions

### Q7: Why are my queries slow?

**Answer:**

Slow queries can have multiple causes. Here's a systematic approach to diagnose and fix them.

**Diagnosis Steps:**

```sql
-- 1. Check if sequential scan is used (usually bad for large tables)
EXPLAIN ANALYZE SELECT * FROM posts WHERE user_id = 'xxx';

-- 2. Check index existence
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'posts';

-- 3. Check index usage statistics
SELECT
    indexrelname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan ASC;
```

**Common Causes and Solutions:**

**1. Missing Indexes:**

```sql
-- Add index for foreign key
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Add index for filter column
CREATE INDEX idx_posts_status ON posts(status);

-- Add composite index for common query pattern
CREATE INDEX idx_posts_user_status ON posts(user_id, status);
```

**2. N+1 Query Problem:**

```typescript
// ❌ Bad: N+1 queries
const { data: posts } = await supabase.from('posts').select('*');
for (const post of posts) {
    const { data: author } = await supabase
        .from('users')
        .select('name')
        .eq('id', post.user_id)
        .single();
    post.authorName = author.name;
}

// ✅ Good: Single query with embedding
const { data: posts } = await supabase
    .from('posts')
    .select(`
        *,
        author:users!user_id (
            id,
            name
        )
    `);
```

**3. Selecting Too Many Columns:**

```typescript
// ❌ Bad: SELECT *
const { data } = await supabase.from('posts').select('*');

// ✅ Good: Select only needed columns
const { data } = await supabase
    .from('posts')
    .select('id, title, created_at');
```

**4. Missing Pagination:**

```typescript
// ❌ Bad: No pagination on large tables
const { data } = await supabase.from('posts').select('*');

// ✅ Good: Paginated queries
const { data } = await supabase
    .from('posts')
    .select('id, title, created_at')
    .range(offset, offset + pageSize - 1);
```

**5. Inefficient Filtering:**

```typescript
// ❌ Bad: Client-side filtering
const { data } = await supabase.from('posts').select('*');
const filtered = data.filter(post => post.status === 'published');

// ✅ Good: Server-side filtering
const { data } = await supabase
    .from('posts')
    .select('*')
    .eq('status', 'published');
```

### Q8: How do I optimize connection pooling?

**Answer:**

Connection pooling in Supabase is handled by PgBouncer, which sits between your application and PostgreSQL.

**Understanding Pool Modes:**

**Transaction Mode (Recommended for HTTP):**
- Connections acquired only during transactions
- Suitable for most web applications
- Cannot use prepared statements across requests

**Session Mode:**
- Connection held for entire session
- Required for LISTEN/NOTIFY
- Needed for prepared statements

```typescript
// Supabase client uses transaction mode by default
const supabase = createClient(url, anonKey);
// Good for: Web apps, mobile apps, serverless

// For session mode needs (rare):
const supabase = createClient(url, anonKey, {
    db: {
        poolMode: 'session' // Only when needed
    }
});
```

**Connection Pool Settings:**

```sql
-- Check current connections
SELECT count(*) as active_connections FROM pg_stat_activity WHERE state = 'active';

-- Check pool stats
SELECT * FROM pgbouncer.pools;
```

**Optimization Strategies:**

1. **Reuse Client Instance:**
```typescript
// ❌ Bad: Creating new client per request
export async function handler(req) {
    const supabase = createClient(url, key);
    return await supabase.from('table').select('*');
}

// ✅ Good: Reuse client instance
const supabase = createClient(url, key);
export async function handler(req) {
    return await supabase.from('table').select('*');
}
```

2. **Batch Operations:**
```typescript
// ❌ Bad: Individual inserts
for (const item of items) {
    await supabase.from('table').insert(item);
}

// ✅ Good: Batch insert
await supabase.from('table').insert(items);
```

3. **Connection Pool Sizing:**
For Pro tier and above, you can adjust pool size:
- Default pool size: 10
- For high-traffic apps: 20-50
- Monitor with `pg_stat_activity`

### Q9: When should I use database functions vs Edge Functions?

**Answer:**

**Use Database Functions when:**

- Operations are primarily database operations
- Transaction support is needed
- Simple to moderate complexity
- RLS policies should apply
- No external API calls needed
- Want minimal cold start

```sql
-- Complex aggregation and filtering
CREATE OR REPLACE FUNCTION get_dashboard_stats(user_id_param UUID)
RETURNS TABLE (
    total_posts BIGINT,
    total_comments BIGINT,
    recent_activity JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        (SELECT COUNT(*) FROM posts WHERE user_id = user_id_param),
        (SELECT COUNT(*) FROM comments WHERE user_id = user_id_param),
        (SELECT json_agg(json_build_object(
            'type', 'post',
            'id', id,
            'created_at', created_at
        )) FROM (
            SELECT id, created_at FROM posts WHERE user_id = user_id_param
            UNION ALL
            SELECT id, created_at FROM comments WHERE user_id = user_id_param
            ORDER BY created_at DESC
            LIMIT 10
        ) recent
    );
END;
$$ LANGUAGE plpgsql;
```

**Use Edge Functions when:**

- External API integrations needed
- Complex TypeScript/Node.js logic
- Service role key bypass required
- Webhook processing
- Heavy computation or data transformation
- Need for external services (email, SMS, payments)

```typescript
// External API integration
Deno.serve(async (req) => {
    const { data: weatherData } = await fetch(
        `https://api.weather.com/v3/wx?location=${city}`,
        { headers: { 'X-API-Key': Deno.env.get('WEATHER_API_KEY') } }
    ).then(r => r.json());
    
    // Store in database
    await supabaseAdmin.from('weather_cache').upsert({
        city,
        data: weatherData,
        fetched_at: new Date()
    });
    
    return new Response(JSON.stringify(weatherData));
});
```

**Decision Matrix:**

| Criteria | Database Function | Edge Function |
|----------|-------------------|---------------|
| Transaction support | ✅ Native | ⚠️ Manual |
| RLS applies | ✅ Automatic | ⚠️ Need anon key |
| External APIs | ❌ No | ✅ Yes |
| TypeScript ecosystem | ❌ No | ✅ Yes |
| Cold start | ✅ None | ⚠️ ~200ms |
| Complex JSON processing | ⚠️ Limited | ✅ Full |

## Authentication Questions

### Q10: How do I handle JWT token expiration?

**Answer:**

Token expiration should be handled gracefully to maintain good user experience.

**Token Lifecycle:**

```typescript
// Access token: Short-lived (~1 hour)
// Refresh token: Longer-lived (~30 days)

const { data, error } = await supabase.auth.signInWithPassword({
    email, password
});

// Access token expires, refresh token allows getting new one
// Supabase client handles this automatically
```

**Manual Token Refresh:**

```typescript
class AuthManager {
    private supabase: SupabaseClient;
    
    async ensureValidSession() {
        const { data: { session }, error } = await this.supabase.auth.getSession();
        
        if (error || !session) {
            return null;
        }
        
        // Check if token expires within 5 minutes
        const expiresAt = session.expires_at;
        const now = Math.floor(Date.now() / 1000);
        const fiveMinutes = 5 * 60;
        
        if (expiresAt - now < fiveMinutes) {
            // Refresh the session
            const { data: { session: newSession }, error: refreshError } = 
                await this.supabase.auth.refreshSession();
            
            if (refreshError) {
                // Refresh failed, user needs to re-login
                await this.supabase.auth.signOut();
                return null;
            }
            
            return newSession;
        }
        
        return session;
    }
}
```

**Session Expiration Handling:**

```typescript
// Listen for auth state changes
supabase.auth.onAuthStateChange((event, session) => {
    if (event === 'TOKEN_REFRESHED') {
        console.log('Token refreshed:', session.access_token);
        // Update local storage/cookies
    }
    
    if (event === 'SIGNED_OUT') {
        console.log('User signed out');
        // Clear local state, redirect to login
    }
    
    if (event === 'USER_UPDATED') {
        console.log('User updated:', session.user);
    }
});
```

### Q11: How do I implement role-based access control?

**Answer:**

Role-based access control can be implemented at multiple levels:

**Database Level with Profiles:**

```sql
-- Add role to profiles
ALTER TABLE profiles ADD COLUMN role TEXT DEFAULT 'user'
    CHECK (role IN ('user', 'moderator', 'admin'));

-- RLS policy checking role
CREATE POLICY "admin_full_access" ON posts
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "user_own_posts" ON posts
    FOR ALL
    USING (user_id = auth.uid());
```

**Application Level with Edge Functions:**

```typescript
// _shared/auth.ts
export async function requireRole(req: Request, requiredRole: string) {
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
        return { error: new Response('Unauthorized', { status: 401 }) };
    }
    
    const token = authHeader.replace('Bearer ', '');
    const { data: { user } } = await supabaseAdmin.auth.getUser(token);
    
    if (!user) {
        return { error: new Response('Unauthorized', { status: 401 }) };
    }
    
    const { data: profile } = await supabaseAdmin
        .from('profiles')
        .select('role')
        .eq('id', user.id)
        .single();
    
    const roleHierarchy = { admin: 3, moderator: 2, user: 1 };
    const userLevel = roleHierarchy[profile?.role] || 0;
    const requiredLevel = roleHierarchy[requiredRole] || 0;
    
    if (userLevel < requiredLevel) {
        return { error: new Response('Forbidden', { status: 403 }) };
    }
    
    return { userId: user.id, role: profile?.role };
}

// Usage in Edge Function
export default async (req: Request) => {
    const { error, userId, role } = await requireRole(req, 'moderator');
    if (error) return error;
    
    // Proceed with moderator-level operations
};
```

## Realtime Questions

### Q12: How do I prevent excessive realtime subscriptions?

**Answer:**

Excessive realtime subscriptions can cause performance issues and increased costs. Here's how to optimize:

**1. Filter at Source:**

```typescript
// ❌ Bad: Subscribe to all posts
supabase
    .channel('all-posts')
    .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'posts'
    }, handleChange)
    .subscribe();

// ✅ Good: Filter to relevant subset
supabase
    .channel('my-posts')
    .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'posts',
        filter: `user_id=eq.${currentUserId}`
    }, handleChange)
    .subscribe();
```

**2. Consolidate Related Subscriptions:**

```typescript
// ❌ Bad: Multiple separate subscriptions
supabase.channel('posts').on(...).subscribe();
supabase.channel('comments').on(...).subscribe();
supabase.channel('likes').on(...).subscribe();

// ✅ Good: Single channel with multiple handlers
const channel = supabase
    .channel('post-detail')
    .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'posts',
        filter: `id=eq.${postId}`
    }, handlePostChange)
    .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'comments',
        filter: `post_id=eq.${postId}`
    }, handleNewComment)
    .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'likes',
        filter: `post_id=eq.${postId}`
    }, handleNewLike)
    .subscribe();
```

**3. Unsubscribe When Done:**

```typescript
import { onMount, onUnmounted } from 'react';

function PostDetail({ postId }) {
    const channelRef = useRef(null);
    
    onMount(() => {
        channelRef.current = supabase
            .channel(`post-${postId}`)
            .on('postgres_changes', {...})
            .subscribe();
    });
    
    onUnmounted(() => {
        if (channelRef.current) {
            supabase.removeChannel(channelRef.current);
        }
    });
}
```

**4. Use Broadcast for Ephemeral Data:**

```typescript
// For cursor positions, typing indicators, etc.
// These don't need database persistence
channel.on('broadcast', { event: 'cursor' }, handleCursor);
```

### Q13: How does realtime work with RLS?

**Answer:**

Realtime subscriptions respect RLS policies, filtering what clients receive based on their permissions.

**How It Works:**

```sql
-- Enable realtime on a table
ALTER PUBLICATION supabase_realtime ADD TABLE posts;

-- RLS policy filters what users receive
CREATE POLICY "user_own_posts" ON posts
    FOR SELECT
    USING (user_id = auth.uid());
```

**Behavior:**

```typescript
// Authenticated user subscribes
const userId = 'xxx';
const channel = supabase
    .channel('posts-realtime')
    .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'posts'
    }, handleChange)
    .subscribe();

// User will ONLY receive changes for posts where user_id = xxx
// Other users' posts are filtered by RLS
```

**Important Considerations:**

1. **RLS Must Be Enabled**: Realtime works with or without RLS, but filtering only works with RLS enabled.

2. **Admin Access**: Using service role key subscribes to all changes (bypasses RLS).

3. **Performance Impact**: Complex RLS policies can impact realtime performance.

4. **Publication Requirements**: Tables must be added to `supabase_realtime` publication:

```sql
-- Check what's in the publication
SELECT * FROM pg_publication_tables WHERE pubname = 'supabase_realtime';

-- Add table if missing
ALTER PUBLICATION supabase_realtime ADD TABLE your_table;
```

## Storage Questions

### Q14: How do I handle file uploads securely?

**Answer:**

Secure file uploads require validation at multiple levels.

**Server-Side Validation (Edge Function):**

```typescript
// supabase/functions/upload-file/index.ts
import { createClient } from 'jsr:@supabase/supabase-js@2';

const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

Deno.serve(async (req) => {
    if (req.method === 'OPTIONS') {
        return new Response(null, { headers: corsHeaders });
    }
    
    try {
        const authHeader = req.headers.get('Authorization');
        if (!authHeader) {
            return new Response(JSON.stringify({ error: 'Unauthorized' }), {
                status: 401,
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            });
        }
        
        const supabaseAdmin = createClient(
            Deno.env.get('SUPABASE_URL')!,
            Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
        );
        
        // Validate auth
        const token = authHeader.replace('Bearer ', '');
        const { data: { user }, error: authError } = await supabaseAdmin.auth.getUser(token);
        
        if (authError || !user) {
            return new Response(JSON.stringify({ error: 'Unauthorized' }), {
                status: 401,
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            });
        }
        
        // Parse multipart form data
        const formData = await req.formData();
        const file = formData.get('file') as File;
        
        // Validate file type
        const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf'];
        if (!allowedTypes.includes(file.type)) {
            return new Response(JSON.stringify({ 
                error: 'Invalid file type' 
            }), {
                status: 400,
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            });
        }
        
        // Validate file size (5MB limit)
        const maxSize = 5 * 1024 * 1024;
        if (file.size > maxSize) {
            return new Response(JSON.stringify({ 
                error: 'File too large' 
            }), {
                status: 400,
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            });
        }
        
        // Generate unique path
        const ext = file.name.split('.').pop();
        const filename = `${crypto.randomUUID()}.${ext}`;
        const path = `uploads/${user.id}/${filename}`;
        
        // Upload to storage
        const buffer = await file.arrayBuffer();
        const { data, error: uploadError } = await supabaseAdmin.storage
            .from('user-uploads')
            .upload(path, buffer, {
                contentType: file.type,
                upsert: false
            });
        
        if (uploadError) {
            return new Response(JSON.stringify({ 
                error: uploadError.message 
            }), {
                status: 500,
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            });
        }
        
        return new Response(JSON.stringify({
            success: true,
            path: data.path
        }), {
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
        
    } catch (error) {
        return new Response(JSON.stringify({ 
            error: 'Internal server error' 
        }), {
            status: 500,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
    }
});
```

**Storage Policies:**

```sql
-- Users can only upload to their folder
CREATE POLICY "user_upload_own_folder" ON storage.objects
    FOR INSERT
    WITH CHECK (
        auth.uid()::TEXT = (storage.foldername(name))[1]
    );

-- Users can only read from their folder
CREATE POLICY "user_read_own_folder" ON storage.objects
    FOR SELECT
    USING (
        auth.uid()::TEXT = (storage.foldername(name))[1]
    );

-- Users can only delete from their folder
CREATE POLICY "user_delete_own_folder" ON storage.objects
    FOR DELETE
    USING (
        auth.uid()::TEXT = (storage.foldername(name))[1]
    );
```

## Troubleshooting Questions

### Q15: Why am I getting "permission denied" errors?

**Answer:**

Permission denied errors usually indicate RLS policy issues.

**Diagnosis Steps:**

```sql
-- 1. Check if RLS is enabled
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';

-- 2. Check existing policies
SELECT policyname, cmd, permissive
FROM pg_policies
WHERE tablename = 'your_table';

-- 3. Test with different roles
SET ROLE anon; SELECT * FROM your_table LIMIT 1;
SET ROLE authenticated; SELECT * FROM your_table LIMIT 1;
```

**Common Causes:**

**1. Missing RLS Policies:**
```sql
-- Add missing policies
CREATE POLICY "select_all" ON your_table
    FOR SELECT USING (true);

CREATE POLICY "insert_own" ON your_table
    FOR INSERT WITH CHECK (user_id = auth.uid());
```

**2. auth.uid() Returns NULL:**
```sql
-- This happens when no authenticated session
-- Check if policies handle NULL properly
CREATE POLICY "safe_select" ON your_table
    FOR SELECT
    USING (
        auth.uid() IS NOT NULL 
        AND user_id = auth.uid()
    );
```

**3. Policy Logic Error:**
```sql
-- Debug policy by testing
SELECT 
    auth.uid() AS current_user,
    (SELECT id FROM your_table LIMIT 1) AS row_user,
    auth.uid() = (SELECT id FROM your_table LIMIT 1) AS should_allow;
```

### Q16: How do I debug RLS policies?

**Answer:**

**Method 1: Test with SET ROLE:**

```sql
-- As anon user
SET ROLE anon;
SELECT * FROM posts WHERE id = 'xxx'; -- Should fail or return empty

-- As authenticated user (replace UUID)
SET ROLE authenticated;
SET request.jwt.claim.sub = 'user-uuid-here';
SELECT * FROM posts WHERE id = 'xxx'; -- Should succeed if user owns post
```

**Method 2: Create Debug Function:**

```sql
CREATE OR REPLACE FUNCTION debug_rls_check()
RETURNS TABLE (
    check_name TEXT,
    result BOOLEAN,
    details TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'auth.uid()'::TEXT,
        auth.uid() IS NOT NULL,
        COALESCE(auth.uid()::TEXT, 'NULL')::TEXT;
    
    RETURN QUERY
    SELECT 
        'current_user'::TEXT,
        current_setting('request.jwt.claim.sub', true) IS NOT NULL,
        COALESCE(current_setting('request.jwt.claim.sub', true), 'NULL')::TEXT;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Run as the user
SELECT * FROM debug_rls_check();
```

**Method 3: Log Policy Evaluations:**

```sql
-- Create a logging function
CREATE OR REPLACE FUNCTION log_policy_check(
    table_name TEXT,
    operation TEXT,
    user_id UUID
) RETURNS VOID AS $$
BEGIN
    RAISE NOTICE 'RLS Check: table=%, op=%, user=%', table_name, operation, user_id;
END;
$$ LANGUAGE plpgsql;

-- Add to policy for debugging (remove in production)
CREATE POLICY "debug_select" ON posts
    FOR SELECT
    USING (
        log_policy_check('posts', 'select', auth.uid()),
        true
    );
```

### Q17: How do I handle timezone issues?

**Answer:**

Timezone handling is important for consistent date/time operations.

**Best Practices:**

**1. Store as TIMESTAMPTZ:**
```sql
-- Always use TIMESTAMPTZ for user-facing timestamps
CREATE TABLE events (
    id UUID PRIMARY KEY,
    name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    scheduled_at TIMESTAMPTZ
);

-- TIMESTAMPTZ stores UTC, converts to client's timezone
```

**2. Convert to User's Timezone in Application:**

```typescript
// Store UTC in database
await supabase.from('events').insert({
    name: 'Meeting',
    scheduled_at: new Date().toISOString() // Already UTC
});

// Convert to user's timezone when displaying
const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
const localTime = new Date(event.scheduled_at).toLocaleString('en-US', {
    timeZone: userTimezone
});
```

**3. Filter by Date Ranges:**

```typescript
// Filter by date range (UTC)
const startDate = '2024-01-01T00:00:00Z';
const endDate = '2024-01-31T23:59:59Z';

const { data } = await supabase
    .from('events')
    .select('*')
    .gte('scheduled_at', startDate)
    .lte('scheduled_at', endDate);
```

**4. Use at Time Zone in Queries:**

```sql
-- Convert to specific timezone in query
SELECT 
    id,
    name,
    scheduled_at,
    scheduled_at AT TIME ZONE 'America/New_York' AS scheduled_ny
FROM events;
```

## Migration Questions

### Q18: How do I migrate from Firebase to Supabase?

**Answer:**

Migration requires careful planning and data transformation.

**Migration Steps:**

**1. Analyze Current Schema:**

```javascript
// Firebase structure (NoSQL)
{
  "posts": {
    "post1": {
      "title": "Hello",
      "author": { "name": "John", "avatar": "url" },
      "comments": [
        { "text": "Great!", "author": "Jane" }
      ]
    }
  }
}

// Supabase structure (Relational)
-- posts table
-- users table
-- comments table
-- posts_authors foreign key
```

**2. Create Target Schema:**

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    auth_id UUID REFERENCES auth.users(id),
    name TEXT,
    avatar TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    author_id UUID REFERENCES users(id),
    title TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    author_id UUID REFERENCES users(id),
    text TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**3. Export Firebase Data:**

```javascript
// Use Firebase Admin SDK to export
const admin = require('firebase-admin');
const data = await admin.database().ref('/posts').once('value');
const posts = data.val();
```

**4. Transform and Import:**

```typescript
// Transform Firebase data to Supabase format
const transformedUsers = Object.values(posts).map(post => ({
    id: uuidv4(),
    name: post.author.name,
    avatar: post.author.avatar
}));

const transformedPosts = Object.values(posts).map(post => ({
    id: uuidv4(),
    author_id: findAuthorId(post.author),
    title: post.title
}));

const transformedComments = Object.values(posts)
    .flatMap(post => 
        post.comments.map(comment => ({
            id: uuidv4(),
            post_id: findPostId(post.title),
            author_id: findAuthorId(comment.author),
            text: comment.text
        }))
    );

// Batch insert
await supabase.from('users').insert(transformedUsers);
await supabase.from('posts').insert(transformedPosts);
await supabase.from('comments').insert(transformedComments);
```

**5. Handle Authentication:**

```typescript
// Firebase Auth export → Supabase Auth migration
// Note: Direct password migration isn't possible
// Users will need to reset passwords

// Export Firebase users
const users = await admin.auth().listUsers();
// Create corresponding Supabase users
for (const user of users.users) {
    await supabaseAdmin.auth.admin.createUser({
        email: user.email,
        email_confirm: true,
        user_metadata: { firebase_uid: user.uid }
    });
}
```

### Q19: How do I backup and restore Supabase?

**Answer:**

**Supabase Cloud Backups:**

```sql
-- Point-in-time recovery (Pro tier and above)
-- Automatic backups enabled by default
-- Restore via Supabase Dashboard or CLI

-- Check backup status
-- Dashboard > Database > Backups
```

**Manual pg_dump Export:**

```bash
# Export entire database
pg_dump -h db.xxx.supabase.co -U postgres -d postgres \
    -f backup.sql --clean --if-exists

# Export specific tables
pg_dump -h db.xxx.supabase.co -U postgres -d postgres \
    -t public.posts -t public.users \
    -f tables.sql

# Export with data only
pg_dump -h db.xxx.supabase.co -U postgres -d postgres \
    --data-only -t public.posts -f data.sql
```

**Restore:**

```bash
# Via psql (for smaller databases)
psql -h db.xxx.supabase.co -U postgres -d postgres -f backup.sql

# Via Supabase CLI
supabase db restore -p your-project-ref 2024-01-15-00-00-00
```

**Point-in-Time Recovery:**

```bash
# List available backups
supabase backup list -p your-project-ref

# Restore to specific point in time
supabase db restore -p your-project-ref --time "2024-01-15T12:00:00Z"
```

## References

1. **Official Documentation**
   - Supabase Docs: https://supabase.com/docs
   - PostgREST: https://postgrest.org/
   - PostgreSQL: https://www.postgresql.org/docs/

2. **Community Resources**
   - Supabase Discord: https://discord.gg/supabase
   - GitHub Discussions: https://github.com/supabase/supabase/discussions
   - Stack Overflow: https://stackoverflow.com/questions/tagged/supabase

3. **Migration Resources**
   - Firebase to Supabase Guide: https://supabase.com/docs/guides/migrations/firebase
   - PostgreSQL vs MongoDB: https://supabase.com/docs/guides/database/export

---

**Related Documents**:
- `architecture.md` - System architecture
- `best-practice.md` - Detailed best practices
- `decision-tree.md` - Feature selection guidance
- `checklist.md` - Pre-deployment checklist
