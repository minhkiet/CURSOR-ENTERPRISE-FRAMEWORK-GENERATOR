---
title: "Supabase Best Practices"
description: "Hướng dẫn thực hành tốt nhất khi sử dụng Supabase trong production environment"
tags: ["supabase", "postgres", "rls", "security", "performance", "edge-functions", "best-practices"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Supabase Best Practices

## Overview

Supabase là một Backend-as-a-Service platform được build trên PostgreSQL, cung cấp database, authentication, realtime subscriptions, file storage, và edge functions trong một unified solution. Để tận dụng tối đa platform này trong production environment, developers cần follow các best practices đã được validated qua nhiều production deployments.

Tài liệu này tổng hợp các best practices từ Supabase documentation, community experience, và production feedback. Các recommendations được organize theo functional areas và include practical examples cho TypeScript/SQL code.

Best practices không chỉ là guidelines mà còn là lessons learned từ real-world implementations. Nhiều trong số này được derived từ debugging production issues và performance optimization efforts.

## Purpose

Tài liệu này phục vụ các mục đích chính sau:

1. **Accelerate Development**: Cung cấp proven patterns để developers không phải reinvent the wheel
2. **Prevent Common Mistakes**: Highlight các areas dễ gây ra problems nếu không implement đúng cách
3. **Ensure Security**: Security best practices để protect data và users
4. **Optimize Performance**: Performance guidelines để ensure scalable applications
5. **Standardize Team Practices**: Unified approach cho development team consistency

Mỗi section bao gồm rationale (tại sao nên làm vậy), implementation details (làm thế nào), và examples (code samples).

## Key Concepts

### 1. Database Design Principles

PostgreSQL là một relational database system mạnh mẽ. Supabase leverages full PostgreSQL capabilities, bao gồm advanced features như JSONB, full-text search, và pgvector cho vector similarity search.

**Normalization vs Denormalization**: Understand khi nào cần normalize (reduce redundancy) và khi nào denormalize (improve read performance). Trong Supabase context, highly normalized schemas benefit từ PostgREST auto-generated APIs, trong khi strategic denormalization improves realtime performance.

**Indexing Strategy**: Indexes là critical cho query performance, nhưng over-indexing increases write overhead. Sử dụng composite indexes cho frequently combined filters và partial indexes cho sparse data.

**Connection Management**: Supabase uses PgBouncer cho connection pooling. Understanding pooling modes (transaction vs session) giúp optimize connection usage trong different scenarios.

### 2. Security Architecture

Security trong Supabase được implement qua multiple layers:

**Row Level Security (RLS)**: Primary mechanism cho data access control. Policies được evaluated cho mỗi query và enforce row-level permissions based on auth.uid().

**Authentication**: Supabase Auth supports multiple providers và methods. JWT tokens được used cho API authentication và RLS policy evaluation.

**Storage Security**: Storage buckets có separate access policies. Files có thể be public hoặc private với signed URLs.

**API Security**: API endpoints được protected qua API keys (anon vs service role) và optional additional validation.

### 3. Performance Optimization

Performance best practices span multiple layers:

**Database Level**: Proper indexing, query optimization, và efficient schema design.

**API Level**: Pagination, filtering, và intelligent use of PostgREST features.

**Client Level**: Caching strategies, optimistic updates, và efficient state management.

**Infrastructure Level**: Connection pooling configuration, caching layers, và CDN usage for static assets.

### 4. Realtime Architecture

Realtime subscriptions là một distinguishing feature của Supabase. Best practices ensure efficient bandwidth usage và minimal server load.

**Filtering at Source**: Subscribe only to relevant data using PostgREST filters. This reduces unnecessary data transfer và client-side processing.

**Channel Management**: Properly manage channel lifecycle để avoid memory leaks và unnecessary connections.

**Hybrid Approaches**: Combine database changes với Broadcast cho different use cases. Database changes for persistent data, Broadcast for ephemeral state.

## Best Practices

### 1. Database Design Best Practices

#### Schema Design Guidelines

**Use UUIDs for Primary Keys**: UUIDs provide globally unique identifiers và work well với distributed systems:

```sql
-- Recommended: UUID primary keys
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Use CASCADE for referential integrity
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**Use Proper Data Types**: Choose appropriate data types for data characteristics:

```sql
-- Use BOOLEAN for flags, not TEXT
ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT FALSE;

-- Use JSONB for flexible schemas but document structure
ALTER TABLE events ADD COLUMN metadata JSONB DEFAULT '{}';

-- Use ARRAY for simple collections
ALTER TABLE users ADD COLUMN interests TEXT[] DEFAULT '{}';

-- Use ENUM for fixed sets
CREATE TYPE user_role AS ENUM ('user', 'moderator', 'admin');
ALTER TABLE users ADD COLUMN role user_role DEFAULT 'user';

-- Use NUMERIC for monetary values, not FLOAT
ALTER TABLE orders ADD COLUMN total_amount NUMERIC(12, 2);
```

#### Indexing Best Practices

**Index Foreign Keys**: Always index columns used in JOINs và foreign keys:

```sql
-- Index foreign keys immediately after creating tables
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_comments_post_id ON comments(post_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);

-- Composite indexes for common query patterns
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at DESC);

-- Partial indexes for specific use cases
CREATE INDEX idx_posts_published ON posts(created_at)
    WHERE status = 'published';

-- Covering indexes to avoid table lookups
CREATE INDEX idx_posts_cover ON posts(user_id, created_at DESC)
    INCLUDE (title, status);
```

**Use Indexes for Filter Operations**: Create indexes that match WHERE clause patterns:

```sql
-- Pattern: Equality filter
CREATE INDEX idx_users_role ON users(role);

-- Pattern: Range filter
CREATE INDEX idx_orders_created ON orders(created_at DESC);

-- Pattern: Text search
CREATE INDEX idx_posts_title_fts ON posts USING gin(to_tsvector('english', title));

-- Pattern: JSONB queries
CREATE INDEX idx_events_metadata ON events USING gin(metadata jsonb_path_ops);
```

#### Migrations Best Practices

**Use Versioned Migrations**: Always use migration files for database changes:

```sql
-- migrations/001_create_users.sql
-- Up migration
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- migrations/001_create_users_down.sql
-- Down migration
DROP INDEX IF EXISTS idx_users_email;
DROP TABLE IF EXISTS users;
```

**Make Migrations Idempotent**: Each migration should be safe to run multiple times:

```sql
-- Bad: Fails if index exists
CREATE INDEX idx_users_email ON users(email);

-- Good: Check before creating
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Good: Use OR REPLACE for functions
CREATE OR REPLACE FUNCTION get_user_by_email(email_param TEXT)
RETURNS SETOF users AS $$
BEGIN
    RETURN QUERY SELECT * FROM users WHERE email = email_param;
END;
$$ LANGUAGE plpgsql;
```

**Test Migrations in Development First**: Always test migrations locally before deploying to production:

```bash
# Run migrations locally
supabase db push

# Check migration status
supabase migration list

# Validate migration syntax
psql -f migrations/001_create_users.sql --dry-run
```

### 2. Row Level Security Best Practices

#### RLS Policy Design

**Enable RLS as Default**: Always enable RLS, even for development:

```sql
-- Enable RLS on all tables by default
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;

-- Create policies immediately after enabling RLS
-- to avoid locking yourself out
```

**Use Authenticated and Unauthenticated Policies**: Distinguish between public và authenticated access:

```sql
-- Public content policy
CREATE POLICY "Public profiles are viewable"
    ON profiles FOR SELECT
    USING (is_public = true);

-- Authenticated user policy
CREATE POLICY "Users can view own profile"
    ON profiles FOR SELECT
    USING (auth.uid() = id);

-- Admin bypass policy (use with SECURITY DEFINER)
CREATE POLICY "Admins can view all profiles"
    ON profiles FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM admin_users
            WHERE user_id = auth.uid()
        )
    );
```

**Use Functions for Complex Logic**: Encapsulate complex policy logic in functions:

```sql
-- Helper function to check if user can view a post
CREATE OR REPLACE FUNCTION can_view_post(post_owner_id UUID)
RETURNS BOOLEAN
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
    SELECT
        -- User owns the post
        auth.uid() = post_owner_id
        OR
        -- Post is public
        EXISTS (
            SELECT 1 FROM posts
            WHERE id = post_owner_id AND is_public = true
        )
        OR
        -- User follows the post owner
        EXISTS (
            SELECT 1 FROM follows
            WHERE follower_id = auth.uid()
            AND following_id = post_owner_id
        );
$$;

-- Use the function in policy
CREATE POLICY "Viewable posts"
    ON posts FOR SELECT
    USING (can_view_post(user_id));
```

#### Testing RLS Policies

**Test with Different Auth Contexts**: Verify policies work correctly for all user types:

```sql
-- As anon user (unauthenticated)
SET ROLE anon;
SELECT * FROM profiles; -- Should only see public profiles

-- As authenticated user
SET ROLE authenticated;
SELECT * FROM profiles WHERE id = current_setting('request.jwt.claim.sub')::UUID;
-- Should see own profile plus public ones

-- As service role (bypasses RLS)
SET ROLE postgres;
SELECT * FROM profiles; -- Should see everything (admin access only)
```

**Use RLS Policy Templates**: Create reusable patterns for common scenarios:

```sql
-- Template: Owner-only access
CREATE OR REPLACE FUNCTION create_owner_policy(
    table_name TEXT,
    user_id_column TEXT
) RETURNS VOID AS $$
BEGIN
    EXECUTE format(
        'CREATE POLICY owner_select ON %I FOR SELECT USING (%I = auth.uid())',
        table_name, user_id_column
    );
    EXECUTE format(
        'CREATE POLICY owner_update ON %I FOR UPDATE USING (%I = auth.uid())',
        table_name, user_id_column
    );
    EXECUTE format(
        'CREATE POLICY owner_delete ON %I FOR DELETE USING (%I = auth.uid())',
        table_name, user_id_column
    );
END;
$$ LANGUAGE plpgsql;

-- Apply template
SELECT create_owner_policy('posts', 'user_id');
```

### 3. Authentication Best Practices

#### Secure Token Management

**Use httpOnly Cookies for Web Applications**: Prevent XSS-based token theft:

```typescript
// Server-side: Set httpOnly cookie
export async function loginHandler(req: Request): Promise<Response> {
    const { email, password } = await req.json();
    
    const { data, error } = await supabaseAdmin.auth.signInWithPassword({
        email,
        password
    });
    
    if (error) {
        return new Response(JSON.stringify({ error: error.message }), {
            status: 401
        });
    }
    
    // Set httpOnly cookie (not accessible to JavaScript)
    const response = new Response(JSON.stringify({ success: true }));
    response.headers.set(
        'Set-Cookie',
        `access_token=${data.session.access_token}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=${data.session.expires_in}`
    );
    
    return response;
}
```

**Implement Token Refresh Logic**: Handle token expiration gracefully:

```typescript
// Client-side token refresh
class AuthManager {
    private supabase: SupabaseClient;
    private refreshing: Promise<Session> | null = null;
    
    constructor(supabase: SupabaseClient) {
        this.supabase = supabase;
    }
    
    async getValidSession(): Promise<Session | null> {
        const { data: { session }, error } = await this.supabase.auth.getSession();
        
        if (error || !session) {
            return null;
        }
        
        // Check if token is about to expire (within 5 minutes)
        const expiresAt = session.expires_at;
        const now = Math.floor(Date.now() / 1000);
        const fiveMinutes = 5 * 60;
        
        if (expiresAt - now < fiveMinutes) {
            // Token expiring soon, refresh it
            if (!this.refreshing) {
                this.refreshing = this.refreshSession();
            }
            return this.refreshing;
        }
        
        return session;
    }
    
    private async refreshSession(): Promise<Session> {
        try {
            const { data, error } = await this.supabase.auth.refreshSession();
            if (error) throw error;
            return data.session!;
        } finally {
            this.refreshing = null;
        }
    }
}
```

#### OAuth Implementation

**Implement Secure OAuth Flow**: Follow OAuth best practices:

```typescript
// Generate secure state parameter
function generateState(): string {
    const array = new Uint8Array(32);
    crypto.getRandomValues(array);
    return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
}

// Store state in session
export async function initiateOAuth(req: Request): Promise<Response> {
    const state = generateState();
    
    // Store state in session/Redis with expiry
    await supabaseAdmin.rpc('store_oauth_state', {
        state_param: state,
        created_at: new Date().toISOString()
    });
    
    const { data, error } = await supabaseAdmin.auth.signInWithOAuth({
        provider: 'google',
        options: {
            redirectTo: `${getBaseUrl()}/auth/callback`,
            queryParams: {
                access_type: 'offline',
                prompt: 'consent'
            }
        }
    });
    
    if (error) {
        return new Response(JSON.stringify({ error: error.message }), {
            status: 400
        });
    }
    
    return Response.redirect(data.url!, 302);
}
```

### 4. Edge Functions Best Practices

#### Function Organization

**Use Structured Project Layout**: Organize edge functions for maintainability:

```
supabase/
├── functions/
│   ├── _shared/
│   │   ├── database.ts
│   │   ├── auth.ts
│   │   └── cors.ts
│   ├── api-v1/
│   │   ├── index.ts
│   │   └── users.ts
│   └── api-v2/
│       ├── index.ts
│       └── users.ts
```

**Share Common Code**: Extract reusable logic to _shared folder:

```typescript
// supabase/functions/_shared/database.ts
import { createClient, SupabaseClient } from 'jsr:@supabase/supabase-js@2';

let adminClient: SupabaseClient | null = null;

export function getAdminClient(): SupabaseClient {
    if (!adminClient) {
        adminClient = createClient(
            Deno.env.get('SUPABASE_URL')!,
            Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
            { auth: { persistSession: false } }
        );
    }
    return adminClient;
}

// supabase/functions/_shared/auth.ts
export async function validateAuth(req: Request): Promise<{ userId: string; error?: never } | { userId?: never; error: Response }> {
    const authHeader = req.headers.get('Authorization');
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return {
            error: new Response(JSON.stringify({ error: 'Missing authorization header' }), {
                status: 401,
                headers: { 'Content-Type': 'application/json' }
            })
        };
    }
    
    const token = authHeader.substring(7);
    const adminClient = getAdminClient();
    const { data: { user }, error } = await adminClient.auth.getUser(token);
    
    if (error || !user) {
        return {
            error: new Response(JSON.stringify({ error: 'Invalid token' }), {
                status: 401,
                headers: { 'Content-Type': 'application/json' }
            })
        };
    }
    
    return { userId: user.id };
}
```

#### Performance Optimization

**Minimize Cold Start Time**: Keep function size small:

```typescript
// Bad: Large imports that increase cold start
import * as _ from 'lodash-es';
import moment from 'moment';
import validator from 'validator';

// Good: Minimal, specific imports
import { isEmail } from 'jsr:@valibot/i18n';

Deno.serve(async (req) => {
    // Function logic here
});
```

**Use Connection Pooling**: Reuse database connections:

```typescript
// Bad: Create new client for each request
export const badHandler = async (req: Request) => {
    const supabase = createClient(
        Deno.env.get('SUPABASE_URL')!,
        Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    );
    // ...
};

// Good: Module-level client
const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
);

export const goodHandler = async (req: Request) => {
    // Uses existing connection
};
```

### 5. Storage Best Practices

#### Bucket Configuration

**Use Separate Buckets for Different Access Patterns**: Organize storage by security requirements:

```sql
-- Public assets bucket (images, public documents)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'public-assets',
    'public-assets',
    true,
    5242880, -- 5MB
    ARRAY['image/jpeg', 'image/png', 'image/webp', 'application/pdf']
);

-- Private user files bucket
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'user-files',
    'user-files',
    false,
    10485760, -- 10MB
    ARRAY['image/jpeg', 'image/png', 'application/pdf', 'application/msword']
);
```

**Configure Storage Policies**: Set up RLS-like policies for storage:

```sql
-- Allow users to upload to their own folder
CREATE POLICY "Users upload to own folder"
    ON storage.objects FOR INSERT
    WITH CHECK (
        auth.uid()::TEXT = (storage.foldername(name))[1]
    );

-- Allow users to read from their own folder
CREATE POLICY "Users read own files"
    ON storage.objects FOR SELECT
    USING (
        auth.uid()::TEXT = (storage.foldername(name))[1]
    );

-- Allow users to delete their own files
CREATE POLICY "Users delete own files"
    ON storage.objects FOR DELETE
    USING (
        auth.uid()::TEXT = (storage.foldername(name))[1]
    );
```

#### Image Transformations

**Use Built-in Image Transformations**: Leverage Supabase Storage transformation capabilities:

```typescript
// Generate thumbnail URL
function getThumbnailUrl(originalUrl: string, width: number = 200): string {
    const url = new URL(originalUrl);
    url.searchParams.set('width', width.toString());
    url.searchParams.set('height', (width * 0.75).toString()); // 4:3 aspect ratio
    url.searchParams.set('resize', 'cover');
    url.searchParams.set('format', 'auto');
    url.searchParams.set('quality', '80');
    return url.toString();
}

// Generate responsive image set
function getResponsiveImages(originalUrl: string) {
    return [
        { size: 'sm', url: getThumbnailUrl(originalUrl, 320) },
        { size: 'md', url: getThumbnailUrl(originalUrl, 640) },
        { size: 'lg', url: getThumbnailUrl(originalUrl, 1024) },
        { size: 'xl', url: getThumbnailUrl(originalUrl, 1920) }
    ];
}
```

### 6. Realtime Best Practices

#### Subscription Optimization

**Filter at Database Level**: Use PostgREST filters to reduce data transfer:

```typescript
// Bad: Subscribe to all posts, filter in client
supabase
    .channel('all-posts')
    .on('postgres_changes', { event: '*', schema: 'public', table: 'posts' }, handleChange)
    .subscribe();

// Good: Filter at subscription level
supabase
    .channel('followed-posts')
    .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'posts',
        filter: `user_id=in.(${followedUserIds.join(',')})`
    }, handleChange)
    .subscribe();
```

**Consolidate Related Subscriptions**: Single channel for related data:

```typescript
// Instead of multiple channels for related data
// Use single channel with multiple handlers

const channel = supabase.channel('post-detail')
    .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'posts',
        filter: `id=eq.${postId}`
    }, (payload) => updatePost(payload.new))
    .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'comments',
        filter: `post_id=eq.${postId}`
    }, (payload) => addComment(payload.new))
    .on('postgres_changes', {
        event: 'DELETE',
        schema: 'public',
        table: 'comments',
        filter: `post_id=eq.${postId}`
    }, (payload) => removeComment(payload.old.id))
    .subscribe();
```

#### Presence and Broadcast

**Use Broadcast for Ephemeral State**: Presence tracking, cursors, typing indicators:

```typescript
// Cursor position updates (ephemeral, not persisted)
channel.on('broadcast', { event: 'cursor' }, ({ payload }) => {
    updateOtherUserCursor(payload.userId, payload.position);
});

// Typing indicator (ephemeral)
channel.on('broadcast', { event: 'typing' }, ({ payload }) => {
    showTypingIndicator(payload.userId, payload.isTyping);
});

// Send cursor updates
function sendCursorUpdate(position: { x: number; y: number }) {
    channel.send({
        type: 'broadcast',
        event: 'cursor',
        payload: { userId: currentUserId, position }
    });
}
```

### 7. API Optimization Best Practices

#### Query Optimization

**Select Only Needed Columns**: Avoid SELECT *:

```typescript
// Bad: Fetching all columns
const { data } = await supabase.from('posts').select('*').eq('user_id', userId);

// Good: Select specific columns
const { data } = await supabase
    .from('posts')
    .select('id, title, created_at, status')
    .eq('user_id', userId)
    .eq('status', 'published')
    .order('created_at', { ascending: false });
```

**Use Embed for Related Data**: Use PostgREST embed feature:

```typescript
// Single query with related data
const { data: posts } = await supabase
    .from('posts')
    .select(`
        id,
        title,
        created_at,
        author:profiles!user_id (
            id,
            username,
            avatar_url
        ),
        comments (
            id,
            content,
            created_at
        )
    `)
    .eq('status', 'published')
    .single();
```

**Use RPC for Complex Queries**: Database functions for complex logic:

```typescript
// Complex query in database function
const { data, error } = await supabase.rpc('get_dashboard_stats', {
    user_id: currentUserId,
    date_from: startDate,
    date_to: endDate
});
```

#### Caching Strategy

**Implement Application-Level Caching**: Reduce database queries:

```typescript
interface CacheEntry<T> {
    data: T;
    expiresAt: number;
}

class QueryCache {
    private cache = new Map<string, CacheEntry<unknown>>();
    private ttl: number;
    
    constructor(ttlSeconds: number = 60) {
        this.ttl = ttlSeconds * 1000;
    }
    
    get<T>(key: string): T | null {
        const entry = this.cache.get(key);
        if (!entry) return null;
        if (Date.now() > entry.expiresAt) {
            this.cache.delete(key);
            return null;
        }
        return entry.data as T;
    }
    
    set<T>(key: string, data: T): void {
        this.cache.set(key, {
            data,
            expiresAt: Date.now() + this.ttl
        });
    }
    
    invalidate(pattern: string): void {
        for (const key of this.cache.keys()) {
            if (key.includes(pattern)) {
                this.cache.delete(key);
            }
        }
    }
}
```

## Common Patterns

### Pattern 1: Multi-Tenant SaaS Implementation

```sql
-- Schema for multi-tenant application
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    plan TEXT DEFAULT 'free',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE tenant_members (
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    role TEXT DEFAULT 'member',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (tenant_id, user_id)
);

CREATE TABLE tenant_resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE tenant_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE tenant_resources ENABLE ROW LEVEL SECURITY;

-- Helper function to get user's tenants
CREATE OR REPLACE FUNCTION get_user_tenants()
RETURNS SETOF UUID
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
    SELECT tenant_id FROM tenant_members WHERE user_id = auth.uid();
$$;

-- Policy for tenant_resources
CREATE POLICY "Tenant resource access"
    ON tenant_resources FOR ALL
    USING (
        tenant_id IN (SELECT get_user_tenants())
    );
```

### Pattern 2: Optimistic UI Updates with Realtime

```typescript
// Optimistic update pattern
async function updatePost(postId: string, updates: Partial<Post>) {
    // 1. Optimistically update local state
    const previousPost = currentPosts.find(p => p.id === postId);
    setPosts(posts.map(p => p.id === postId ? { ...p, ...updates } : p));
    
    try {
        // 2. Make the actual update
        const { data, error } = await supabase
            .from('posts')
            .update(updates)
            .eq('id', postId)
            .select()
            .single();
        
        if (error) throw error;
        
        // 3. Update with server response
        setPosts(posts.map(p => p.id === postId ? data : p));
        
    } catch (error) {
        // 4. Rollback on failure
        setPosts(posts.map(p => p.id === postId ? previousPost : p));
        showError('Failed to update post');
    }
}
```

### Pattern 3: Soft Delete Pattern

```sql
-- Add deleted_at column for soft deletes
ALTER TABLE posts ADD COLUMN deleted_at TIMESTAMPTZ;

-- Create soft delete policy
CREATE POLICY "View non-deleted posts"
    ON posts FOR SELECT
    USING (deleted_at IS NULL);

-- Create soft delete function
CREATE OR REPLACE FUNCTION soft_delete_post(post_id UUID)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    UPDATE posts
    SET deleted_at = NOW()
    WHERE id = post_id AND user_id = auth.uid() AND deleted_at IS NULL;
    
    RETURN FOUND;
END;
$$;

-- Create restore function
CREATE OR REPLACE FUNCTION restore_post(post_id UUID)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    UPDATE posts
    SET deleted_at = NULL
    WHERE id = post_id AND user_id = auth.uid() AND deleted_at IS NOT NULL;
    
    RETURN FOUND;
END;
$$;
```

## Troubleshooting

### Issue: Slow Query Performance

**Diagnosis Steps**:
```sql
-- 1. Check query execution plan
EXPLAIN ANALYZE SELECT * FROM posts WHERE user_id = 'xxx' ORDER BY created_at DESC;

-- 2. Check index usage
SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- 3. Check table bloat
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

**Common Solutions**:
- Add missing indexes
- Update table statistics: `ANALYZE table_name;`
- Vacuum table: `VACUUM ANALYZE table_name;`
- Rewrite query to use indexes

### Issue: RLS Causing Unexpected Behavior

**Diagnosis Steps**:
```sql
-- 1. Check RLS is enabled
SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';

-- 2. Check policies for table
SELECT policyname, permissive, cmd, qual, with_check
FROM pg_policies
WHERE tablename = 'your_table';

-- 3. Test as different roles
SET ROLE anon; SELECT * FROM your_table LIMIT 1;
SET ROLE authenticated; SELECT * FROM your_table LIMIT 1;
```

**Common Solutions**:
- Policy returns no rows: Check auth.uid() usage
- Unexpected data visible: Review USING clause
- Updates failing: Check WITH CHECK clause

### Issue: Realtime Not Working

**Diagnosis Steps**:
```sql
-- 1. Check replication is enabled
SELECT * FROM pg_replication_slots WHERE plugin = 'supabase_realtime';

-- 2. Check publications
SELECT * FROM pg_publication_tables WHERE pubname = 'supabase_realtime';

-- 3. Check if table is in publication
SELECT tablename FROM information_schema.tables
WHERE table_schema = 'public'
AND NOT EXISTS (
    SELECT 1 FROM pg_publication_tables
    WHERE pubname = 'supabase_realtime'
    AND tablename = information_schema.tables.table_name
);
```

**Common Solutions**:
- Add table to publication: `ALTER PUBLICATION supabase_realtime ADD TABLE your_table;`
- Enable RLS on table: `ALTER TABLE your_table ENABLE ROW LEVEL SECURITY;`
- Check client subscription syntax

## Examples

### Example: Complete Database Schema with RLS

```sql
-- Full schema setup with comprehensive RLS
BEGIN;

-- Users table
CREATE TABLE public.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Posts table
CREATE TABLE public.posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content TEXT,
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    tags TEXT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Comments table
CREATE TABLE public.comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Likes table
CREATE TABLE public.likes (
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (post_id, user_id)
);

-- Create indexes
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_status ON posts(status);
CREATE INDEX idx_posts_created ON posts(created_at DESC);
CREATE INDEX idx_comments_post_id ON comments(post_id);
CREATE INDEX idx_likes_post_id ON likes(post_id);

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE likes ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
-- Users policies
CREATE POLICY "Users can view own profile"
    ON users FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON users FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

-- Posts policies
CREATE POLICY "Published posts are public"
    ON posts FOR SELECT
    USING (status = 'published');

CREATE POLICY "Users can view own posts"
    ON posts FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create posts"
    ON posts FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own posts"
    ON posts FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own posts"
    ON posts FOR DELETE
    USING (auth.uid() = user_id);

-- Comments policies
CREATE POLICY "Comments on published posts are public"
    ON comments FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM posts
            WHERE posts.id = comments.post_id AND posts.status = 'published'
        )
    );

CREATE POLICY "Authenticated users can create comments"
    ON comments FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own comments"
    ON comments FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own comments"
    ON comments FOR DELETE
    USING (auth.uid() = user_id);

-- Likes policies
CREATE POLICY "Users can view likes"
    ON likes FOR SELECT
    USING (true);

CREATE POLICY "Users can like"
    ON likes FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can unlike"
    ON likes FOR DELETE
    USING (auth.uid() = user_id);

-- Enable realtime
ALTER PUBLICATION supabase_realtime ADD TABLE posts;
ALTER PUBLICATION supabase_realtime ADD TABLE comments;
ALTER PUBLICATION supabase_realtime ADD TABLE likes;

COMMIT;
```

## References

1. **Official Documentation**
   - Supabase Docs: https://supabase.com/docs
   - PostgreSQL Documentation: https://www.postgresql.org/docs/
   - PostgREST Documentation: https://postgrest.org/

2. **Security Resources**
   - OWASP Security Guidelines: https://owasp.org/
   - JWT Best Practices: https://auth0.com/blog/refresh-tokens-what-are-they-and-how-to-use-them/

3. **Performance Optimization**
   - PostgreSQL Performance Tips: https://www.postgresql.org/docs/current/performance-tips.html
   - Database Indexing Strategies: https://use-the-index-luke.com/

4. **Community Resources**
   - Supabase Discord: https://discord.gg/supabase
   - Supabase GitHub: https://github.com/supabase/supabase

---

**Related Documents**:
- `anti-pattern.md` - Common mistakes to avoid
- `architecture.md` - System architecture overview
- `checklist.md` - Pre-deployment verification checklist
