---
title: "Supabase Anti-Patterns"
description: "Các mẫu thiết kế cần tránh khi sử dụng Supabase trong production"
tags: ["supabase", "postgres", "rls", "security", "performance", "anti-patterns"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Supabase Anti-Patterns

## Overview

Supabase cung cấp một nền tảng mạnh mẽ với PostgreSQL làm core, tích hợp authentication, realtime subscriptions, storage, và edge functions. Tuy nhiên, nhiều developers mắc phải các anti-patterns phổ biến dẫn đến security vulnerabilities, performance issues, và scalability problems. Tài liệu này tổng hợp các anti-patterns được document từ thực tế production deployments và cách khắc phục chúng.

Understanding these anti-patterns giúp developers tránh được những pitfalls tốn thời gian để debug và fix trong production. Mỗi anti-pattern được phân tích với root cause, impact assessment, và concrete solutions.

Tài liệu này được thiết kế như một reference guide cho development team, đặc biệt useful trong code review process và architecture planning sessions. Các examples sử dụng TypeScript cho client-side code và SQL cho database operations.

## Purpose

Mục đích chính của tài liệu này là:

1. **Prevents Security Breaches**: Nhiều anti-patterns liên quan đến security, dẫn đến data exposure hoặc unauthorized access
2. **Improves Performance**: Tránh các queries không tối ưu và over-fetching patterns
3. **Reduces Costs**: Một số anti-patterns tạo ra unnecessary compute hoặc bandwidth costs
4. **Ensures Scalability**: Thiết kế không scalable sẽ gây ra problems khi user base tăng trưởng
5. **Standardizes Team Knowledge**: Cung cấp shared understanding về what NOT to do

Mỗi anti-pattern section bao gồm practical examples từ production systems, giúp developers nhận diện và tránh chúng trong codebase của mình.

## Key Concepts

### 1. Row Level Security (RLS) Anti-Patterns

Row Level Security là PostgreSQL feature cho phép row-level access control. Supabase tích hợp RLS với authentication system để secure data access. Tuy nhiên, có nhiều cách để misconfigure RLS dẫn đến security issues.

**RLS Not Enabled**: Một trong những lỗi nghiêm trọng nhất là không enable RLS trên các tables chứa sensitive data. Khi RLS không enabled, tất cả users có database access đều có thể truy cập tất cả rows.

**Overly Permissive Policies**: Policy cho phép tất cả users truy cập tất cả data là equivalent với việc không có RLS. Developers thường tạo policy như `CREATE POLICY "public_read" ON profiles FOR SELECT USING (true);` để simplify development nhưng quên restrict nó sau đó.

**Missing Policy for All Operations**: Chỉ có SELECT policy mà không có INSERT, UPDATE, DELETE policies có thể gây ra unexpected behavior. Operations sẽ fail silently hoặc throw obscure errors.

### 2. API Usage Anti-Patterns

Supabase cung cấp REST API qua PostgREST và client library cho easy data access. Tuy nhiên, việc sử dụng không đúng cách có thể gây ra performance và reliability issues.

**Overusing REST API for Complex Operations**: Sử dụng multiple REST calls để implement business logic thay vì database functions hoặc views. Điều này tạo ra network overhead và race conditions.

**Not Using Database Functions for Complex Logic**: Business logic nên đặt trong PostgreSQL functions để đảm bảo atomicity và reduce client-server round trips. Thay vì fetch data về client, process, rồi update, nên làm tất cả trong một database function.

**Ignoring Pagination**: Fetching toàn bộ table content mà không phân trang. Điều này gây ra memory issues, slow response times, và potential timeout errors.

### 3. Authentication Anti-Patterns

Authentication setup không đúng cách là nguyên nhân phổ biến của security vulnerabilities trong Supabase applications.

**Exposing Service Role Key**: Sử dụng service role key trong client-side code cho phép bypass RLS hoàn toàn. Service role key chỉ nên được sử dụng trong server-side code hoặc Edge Functions.

**Not Validating JWT Tokens Manually**: Supabase client library tự động validate tokens, nhưng khi sử dụng custom server code, developers phải validate JWT signatures manually. Failure to do so allows forged tokens.

**Storing Tokens Improperly**: Lưu trữ tokens trong localStorage (vulnerable to XSS) thay vì httpOnly cookies hoặc secure storage mechanisms.

### 4. Realtime Anti-Patterns

Realtime subscriptions là một trong những features mạnh của Supabase, nhưng misusing chúng có thể gây ra performance issues và increased costs.

**Subscribing to Large Datasets**: Subscribe to entire table hoặc large subsets mà không filter. Điều này tạo ra high bandwidth usage và client-side performance degradation.

**Multiple Unfiltered Subscriptions**: Tạo nhiều subscriptions cho cùng data without consolidating them. Mỗi subscription tạo ra separate WebSocket connection và database replication slot.

**Not Unsubscribing**: Không cleanup subscriptions khi component unmounts, leading to memory leaks và unnecessary server resources.

### 5. Database Design Anti-Patterns

PostgreSQL là một relational database mạnh mẽ, nhưng developers thường apply NoSQL thinking khi thiết kế schema.

**Flat Tables Without Relationships**: Tạo denormalized tables với tất cả data flattened vào một table thay vì normalized schema với proper relationships.

**Missing Indexes**: Không tạo indexes cho frequently queried columns, đặc biệt là foreign keys và columns trong WHERE clauses.

**Over-Indexing**: Ngược lại, tạo quá nhiều indexes trên same table. Mỗi index tăng write overhead và storage requirements.

## Best Practices

### 1. RLS Best Practices

**Always Enable RLS**: Mặc dù có thể disable RLS for development convenience, production tables phải có RLS enabled. Sử dụng this approach để enable RLS safely:

```sql
-- Create policies BEFORE enabling RLS to avoid lockout
-- Step 1: Create a policy that mirrors current (permissive) access
CREATE POLICY "authenticated_full_access" ON public_profiles
    FOR ALL
    USING (auth.uid() IS NOT NULL)
    WITH CHECK (auth.uid() IS NOT NULL);

-- Step 2: Then enable RLS
ALTER TABLE public_profiles ENABLE ROW LEVEL SECURITY;

-- Step 3: Test with anon key
-- Step 4: Then refine the policy to be more restrictive
```

**Policy Testing Strategy**: Test RLS policies với cả anon key (unauthenticated) và service role key (bypasses RLS) để verify correct behavior:

```sql
-- As anon user (should be restricted)
SET ROLE anon;
SELECT * FROM profiles WHERE id = auth.uid();

-- As authenticated user
SET ROLE authenticated;
SELECT * FROM profiles WHERE id = auth.uid();

-- As service role (bypasses RLS - use only for admin operations)
SET ROLE postgres;
```

**Use Security Definer Functions for Admin Operations**: Khi cần bypass RLS cho specific operations, use SECURITY DEFINER functions instead of service role key:

```sql
CREATE OR REPLACE FUNCTION admin_get_all_users()
RETURNS SETOF profiles
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    RETURN QUERY SELECT * FROM profiles;
END;
$$;
```

### 2. API Usage Best Practices

**Use Database Functions for Complex Operations**: Encapsulate complex business logic trong PostgreSQL functions:

```typescript
// Bad: Multiple API calls with race conditions
async function transferCredits(fromUserId: string, toUserId: string, amount: number) {
    const { data: from } = await supabase
        .from('wallets')
        .select('balance')
        .eq('user_id', fromUserId)
        .single();
    
    if (from.balance < amount) throw new Error('Insufficient funds');
    
    await supabase.from('wallets').update({ balance: from.balance - amount }).eq('user_id', fromUserId);
    await supabase.from('wallets').update({ balance: from.balance + amount }).eq('user_id', toUserId);
}

// Good: Single atomic function call
async function transferCredits(fromUserId: string, toUserId: string, amount: number) {
    const { data, error } = await supabase.rpc('transfer_wallet_credits', {
        from_user_id: fromUserId,
        to_user_id: toUserId,
        transfer_amount: amount
    });
    if (error) throw error;
    return data;
}
```

```sql
-- PostgreSQL function for atomic transfer
CREATE OR REPLACE FUNCTION transfer_wallet_credits(
    from_user_id UUID,
    to_user_id UUID,
    transfer_amount NUMERIC
) RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    from_balance NUMERIC;
BEGIN
    -- Lock rows to prevent race conditions
    SELECT balance INTO from_balance
    FROM wallets
    WHERE user_id = from_user_id
    FOR UPDATE;
    
    IF from_balance < transfer_amount THEN
        RAISE EXCEPTION 'Insufficient funds';
    END IF;
    
    UPDATE wallets SET balance = balance - transfer_amount WHERE user_id = from_user_id;
    UPDATE wallets SET balance = balance + transfer_amount WHERE user_id = to_user_id;
    
    RETURN TRUE;
END;
$$;
```

**Implement Proper Pagination**: Use cursor-based pagination cho large datasets:

```typescript
async function fetchPaginatedPosts(cursor?: string, limit: number = 20) {
    let query = supabase
        .from('posts')
        .select('id, title, created_at')
        .order('created_at', { ascending: false })
        .limit(limit);
    
    if (cursor) {
        query = query.lt('created_at', cursor);
    }
    
    const { data, error } = await query;
    if (error) throw error;
    
    return {
        posts: data,
        nextCursor: data.length === limit ? data[data.length - 1].created_at : null
    };
}
```

### 3. Authentication Best Practices

**Use Anon Key for Client-Side**: Chỉ sử dụng anon key trong client applications:

```typescript
// supabaseClient.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

// Anon key is safe for client-side - RLS controls access
export const supabase = createClient(supabaseUrl, supabaseAnonKey);
```

**Implement Proper Token Storage**: Sử dụng httpOnly cookies cho web applications:

```typescript
// server-side token validation (Edge Function or API route)
import { createClient } from '@supabase/supabase-js';

export async function validateUserSession(accessToken: string) {
    const supabaseAdmin = createClient(
        process.env.SUPABASE_URL!,
        process.env.SUPABASE_SERVICE_ROLE_KEY!,
        { auth: { persistSession: false } }
    );
    
    const { data: { user }, error } = await supabaseAdmin.auth.getUser(accessToken);
    
    if (error || !user) {
        throw new Error('Invalid session');
    }
    
    return user;
}
```

**Implement Rate Limiting for Auth Endpoints**: Protect authentication endpoints against brute force attacks:

```typescript
// Edge Function with rate limiting
export const rateLimitAuth = async (req: Request): Promise<Response> => {
    const clientIP = req.headers.get('x-forwarded-for') || 'unknown';
    
    const { data: rateLimit } = await supabaseAdmin
        .from('auth_rate_limits')
        .select('attempts')
        .eq('ip_address', clientIP)
        .single();
    
    if (rateLimit && rateLimit.attempts >= 5) {
        return new Response(JSON.stringify({ error: 'Too many attempts' }), {
            status: 429,
            headers: { 'Retry-After': '60' }
        });
    }
    
    // Increment attempt counter
    // ... rate limit logic
    
    return authHandler(req);
};
```

### 4. Realtime Best Practices

**Use Filtered Subscriptions**: Always apply filters to reduce data transfer:

```typescript
// Bad: Subscribing to entire table
supabase
    .channel('all-posts')
    .on('postgres_changes', { event: '*', schema: 'public', table: 'posts' }, handleChange)
    .subscribe();

// Good: Filtered subscription
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

**Unsubcribe Properly**: Cleanup subscriptions when no longer needed:

```typescript
import { onMount, onUnmounted } from 'svelte';

let channel: RealtimeChannel;

onMount(() => {
    channel = supabase
        .channel('posts-channel')
        .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'posts' }, handleInsert)
        .subscribe();
});

onUnmounted(() => {
    supabase.removeChannel(channel);
});
```

**Use Presence for Collaborative Features**: Presence API cho user presence tracking hiệu quả hơn:

```typescript
// Track user presence in a document
const channel = supabase.channel('document-123', {
    config: { presence: { key: currentUserId } }
});

channel
    .on('presence', { event: 'sync' }, () => {
        const state = channel.presenceState();
        onlineUsers = Object.values(state).flat();
    })
    .subscribe(async (status) => {
        if (status === 'SUBSCRIBED') {
            await channel.track({
                user_id: currentUserId,
                online_at: new Date().toISOString()
            });
        }
    });
```

### 5. Database Design Best Practices

**Use Proper Normalization**: Follow database normalization principles:

```sql
-- Bad: Flat table with repeated data
CREATE TABLE orders_bad (
    id UUID PRIMARY KEY,
    customer_name TEXT,
    customer_email TEXT,
    customer_address TEXT,
    product_names TEXT,  -- Comma-separated
    product_prices TEXT, -- Comma-separated
    total_amount NUMERIC
);

-- Good: Normalized schema
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    address TEXT
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    price NUMERIC NOT NULL
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id),
    total_amount NUMERIC NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id),
    product_id UUID REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC NOT NULL
);
```

**Create Appropriate Indexes**: Index foreign keys and frequently queried columns:

```sql
-- Index foreign keys for join performance
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- Index columns used in WHERE clauses
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_status ON orders(status) WHERE status != 'completed';

-- Composite index for common query patterns
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);
```

## Common Patterns

### Pattern 1: Secure API Routes with Edge Functions

Edge Functions cung cấp serverless execution environment cho logic cần run server-side. Sử dụng chúng để protect sensitive operations:

```typescript
// supabase/functions/secure-transfer/index.ts
import { createClient } from '@supabase/supabase-js';

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
            return new Response(JSON.stringify({ error: 'No authorization' }), {
                status: 401,
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            });
        }
        
        const supabaseAdmin = createClient(
            Deno.env.get('SUPABASE_URL')!,
            Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
        );
        
        const { data: { user }, error: authError } = await supabaseAdmin.auth.getUser(
            authHeader.replace('Bearer ', '')
        );
        
        if (authError || !user) {
            return new Response(JSON.stringify({ error: 'Invalid token' }), {
                status: 401,
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            });
        }
        
        const { from_account, to_account, amount } = await req.json();
        
        // Business logic with full server-side control
        const { data, error } = await supabaseAdmin.rpc('secure_transfer', {
            from_acc: from_account,
            to_acc: to_account,
            amt: amount,
            user_id: user.id
        });
        
        if (error) {
            return new Response(JSON.stringify({ error: error.message }), {
                status: 400,
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            });
        }
        
        return new Response(JSON.stringify({ success: true, data }), {
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
        
    } catch (error) {
        return new Response(JSON.stringify({ error: 'Internal server error' }), {
            status: 500,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
    }
});
```

### Pattern 2: Multi-Tenant RLS Implementation

Implementing row-level security cho multi-tenant applications:

```sql
-- Add tenant_id to all tenant-scoped tables
ALTER TABLE projects ADD COLUMN tenant_id UUID REFERENCES tenants(id);
ALTER TABLE tasks ADD COLUMN tenant_id UUID REFERENCES tenants(id);

-- Enable RLS
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

-- Create policies that check tenant membership
CREATE POLICY "tenant_isolation_projects" ON projects
    FOR ALL
    USING (
        tenant_id IN (
            SELECT tenant_id FROM tenant_members WHERE user_id = auth.uid()
        )
    )
    WITH CHECK (
        tenant_id IN (
            SELECT tenant_id FROM tenant_members WHERE user_id = auth.uid()
        )
    );

-- Function to get user's tenant IDs
CREATE OR REPLACE FUNCTION get_user_tenant_ids()
RETURNS SETOF UUID
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
    SELECT tenant_id FROM tenant_members WHERE user_id = auth.uid();
$$;
```

### Pattern 3: Optimized Realtime with Broadcast

Sử dụng Broadcast thay vì database changes cho high-frequency updates:

```typescript
// For cursor/presence updates that don't need persistence
const channel = supabase.channel('room-123');

// Broadcast for low-latency updates
channel
    .on('broadcast', { event: 'cursor' }, (payload) => {
        updateCursorPosition(payload.payload.userId, payload.payload.position);
    })
    .subscribe();

// Send cursor position (not stored in database)
function sendCursorUpdate(position: { x: number; y: number }) {
    channel.send({
        type: 'broadcast',
        event: 'cursor',
        payload: {
            userId: currentUserId,
            position
        }
    });
}
```

## Troubleshooting

### Issue 1: RLS Blocking All Access

**Symptom**: All queries return empty results or permission denied errors.

**Diagnosis**:
```sql
-- Check if RLS is enabled
SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';

-- Check existing policies
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual, with_check
FROM pg_policies
WHERE schemaname = 'public' AND tablename = 'your_table';
```

**Solution**: Review and fix policies. Often caused by incorrect auth.uid() usage:

```sql
-- Wrong: Policy assumes every table has user_id matching auth.uid()
CREATE POLICY "user_access" ON documents FOR SELECT USING (user_id = auth.uid());

-- Correct: Check if auth.uid() exists first
CREATE POLICY "user_access" ON documents FOR SELECT USING (
    auth.uid() IS NOT NULL AND user_id = auth.uid()
);
```

### Issue 2: Slow Queries Despite Indexes

**Symptom**: Queries are slow even with indexes in place.

**Diagnosis**:
```sql
-- Check query execution plan
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 'xxx';

-- Check index usage
SELECT indexrelname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

**Solution**: Indexes may not be used if statistics are outdated:

```sql
-- Update table statistics
ANALYZE your_table;

-- Check for missing indexes on foreign keys
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
AND tc.table_schema = 'public';

-- Create missing indexes
CREATE INDEX CONCURRENTLY idx_orders_customer ON orders(customer_id);
```

### Issue 3: Realtime Connection Issues

**Symptom**: Realtime subscriptions fail to connect or disconnect frequently.

**Diagnosis**:
```sql
-- Check replication slots
SELECT slot_name, plugin, slot_type, active, restart_lsn
FROM pg_replication_slots
WHERE slot_type = 'logical';

-- Check publication
SELECT * FROM pg_publication_tables WHERE pubname = 'supabase_realtime';
```

**Solution**: Publications may be misconfigured:

```sql
-- Recreate realtime publication
BEGIN;
DROP PUBLICATION IF EXISTS supabase_realtime;
CREATE PUBLICATION supabase_realtime FOR ALL TABLES;
COMMIT;

-- For specific tables only
ALTER PUBLICATION supabase_realtime ADD TABLE your_table;
```

### Issue 4: Edge Function Timeout

**Symptom**: Edge Functions timing out for long operations.

**Solution**: Break long operations into chunks or use background jobs:

```typescript
// Instead of long synchronous operation
export const longOperation = async (req: Request) => {
    // Process in chunks with continuation
    const { cursor, action } = await req.json();
    
    if (action === 'start') {
        // Initialize job
        const jobId = crypto.randomUUID();
        await supabaseAdmin.from('jobs').insert({
            id: jobId,
            status: 'processing',
            progress: 0
        });
        
        // Queue first chunk
        await supabaseAdmin.rpc('process_chunk', {
            job_id: jobId,
            offset: 0
        });
        
        return new Response(JSON.stringify({ jobId, status: 'processing' }));
    }
    // Handle continuation...
};
```

## Examples

### Example 1: Complete RLS Policy Setup

```sql
-- Complete example for a social media-like application

-- 1. Users table - users can see their own profile, others can see public fields
CREATE TABLE public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    bio TEXT,
    is_private BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Follows table - who follows whom
CREATE TABLE public.follows (
    follower_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    following_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (follower_id, following_id)
);

-- 3. Posts table
CREATE TABLE public.posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS on all tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE follows ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- 4. Policies for profiles
-- Anyone can view public profiles
CREATE POLICY "Public profiles are viewable by everyone"
    ON profiles FOR SELECT
    USING (is_private = false);

-- Users can view their own profile
CREATE POLICY "Users can view own profile"
    ON profiles FOR SELECT
    USING (auth.uid() = id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile"
    ON profiles FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

-- 5. Policies for follows
-- Anyone can see who someone is following (public follow lists)
CREATE POLICY "Follows are viewable by everyone"
    ON follows FOR SELECT
    USING (true);

-- Users can create follows for themselves
CREATE POLICY "Users can follow others"
    ON follows FOR INSERT
    WITH CHECK (auth.uid() = follower_id);

-- Users can unfollow themselves
CREATE POLICY "Users can unfollow"
    ON follows FOR DELETE
    USING (auth.uid() = follower_id);

-- 6. Policies for posts
-- View posts from public profiles or followed users
CREATE POLICY "Viewable posts"
    ON posts FOR SELECT
    USING (
        -- Author's profile is public
        EXISTS (
            SELECT 1 FROM profiles
            WHERE id = posts.user_id AND is_private = false
        )
        OR
        -- Or user follows the author
        EXISTS (
            SELECT 1 FROM follows
            WHERE follower_id = auth.uid() AND following_id = posts.user_id
        )
        OR
        -- Or user is the author
        auth.uid() = user_id
    );

-- Users can insert their own posts
CREATE POLICY "Users can create posts"
    ON posts FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Users can update their own posts
CREATE POLICY "Users can update own posts"
    ON posts FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Users can delete their own posts
CREATE POLICY "Users can delete own posts"
    ON posts FOR DELETE
    USING (auth.uid() = user_id);
```

### Example 2: Efficient Pagination Implementation

```typescript
// Cursor-based pagination for large datasets
class PostRepository {
    private supabase: SupabaseClient;
    
    constructor(supabase: SupabaseClient) {
        this.supabase = supabase;
    }
    
    async getFeed(options: {
        cursor?: string;
        limit?: number;
        userId: string;
    }): Promise<{
        posts: Post[];
        nextCursor: string | null;
    }> {
        const { cursor, limit = 20, userId } = options;
        
        let query = this.supabase
            .from('posts')
            .select(`
                id,
                content,
                created_at,
                user:profiles!user_id (
                    id,
                    username,
                    avatar_url
                )
            `)
            .order('created_at', { ascending: false })
            .limit(limit + 1); // Fetch one extra to determine if there's a next page
        
        // Apply cursor for pagination
        if (cursor) {
            query = query.lt('created_at', cursor);
        }
        
        // Only show posts from followed users and self
        const { data, error } = await query;
        
        if (error) {
            throw new Error(`Failed to fetch feed: ${error.message}`);
        }
        
        const hasMore = data.length > limit;
        const posts = hasMore ? data.slice(0, -1) : data;
        const nextCursor = hasMore 
            ? posts[posts.length - 1].created_at 
            : null;
        
        return { posts, nextCursor };
    }
    
    async getUserPosts(userId: string, options: {
        cursor?: string;
        limit?: number;
    }): Promise<{ posts: Post[]; nextCursor: string | null }> {
        const { cursor, limit = 20 } = options;
        
        let query = this.supabase
            .from('posts')
            .select('*')
            .eq('user_id', userId)
            .order('created_at', { ascending: false })
            .limit(limit + 1);
        
        if (cursor) {
            query = query.lt('created_at', cursor);
        }
        
        const { data, error } = await query;
        
        if (error) {
            throw new Error(`Failed to fetch posts: ${error.message}`);
        }
        
        const hasMore = data.length > limit;
        const posts = hasMore ? data.slice(0, -1) : data;
        const nextCursor = hasMore 
            ? posts[posts.length - 1].created_at 
            : null;
        
        return { posts, nextCursor };
    }
}
```

### Example 3: Secure File Upload with Storage

```typescript
import { createClient, SupabaseClient } from '@supabase/supabase-js';
import { v4 as uuidv4 } from 'uuid';

interface UploadOptions {
    file: File;
    bucket: string;
    folder: string;
    userId: string;
    maxSizeMB?: number;
    allowedTypes?: string[];
}

interface UploadResult {
    success: boolean;
    path?: string;
    error?: string;
}

class SecureStorage {
    private supabase: SupabaseClient;
    private supabaseAdmin: SupabaseClient;
    
    constructor(supabase: SupabaseClient, supabaseAdmin: SupabaseClient) {
        this.supabase = supabase;
        this.supabaseAdmin = supabaseAdmin;
    }
    
    async uploadUserFile(options: UploadOptions): Promise<UploadResult> {
        const {
            file,
            bucket,
            folder,
            userId,
            maxSizeMB = 5,
            allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf']
        } = options;
        
        // 1. Validate file size
        if (file.size > maxSizeMB * 1024 * 1024) {
            return { success: false, error: `File size exceeds ${maxSizeMB}MB limit` };
        }
        
        // 2. Validate file type
        if (!allowedTypes.includes(file.type)) {
            return { 
                success: false, 
                error: `File type ${file.type} not allowed. Allowed: ${allowedTypes.join(', ')}` 
            };
        }
        
        // 3. Generate unique filename
        const ext = file.name.split('.').pop();
        const filename = `${uuidv4()}.${ext}`;
        const path = `${folder}/${userId}/${filename}`;
        
        // 4. Upload to storage (using user's auth context)
        const { data, error } = await this.supabase.storage
            .from(bucket)
            .upload(path, file, {
                cacheControl: '3600',
                upsert: false
            });
        
        if (error) {
            return { success: false, error: error.message };
        }
        
        return { success: true, path: data.path };
    }
    
    async deleteUserFile(bucket: string, path: string, userId: string): Promise<UploadResult> {
        // Verify path belongs to user before deletion
        if (!path.includes(`/users/${userId}/`) && !path.includes(`/${userId}/`)) {
            return { success: false, error: 'Unauthorized deletion attempt' };
        }
        
        const { error } = await this.supabase.storage
            .from(bucket)
            .remove([path]);
        
        if (error) {
            return { success: false, error: error.message };
        }
        
        return { success: true };
    }
    
    getPublicUrl(bucket: string, path: string): string {
        const { data } = this.supabase.storage
            .from(bucket)
            .getPublicUrl(path);
        return data.publicUrl;
    }
}
```

## References

1. **Supabase Documentation**
   - Row Level Security: https://supabase.com/docs/guides/auth/row-level-security
   - Realtime: https://supabase.com/docs/guides/realtime
   - Storage: https://supabase.com/docs/guides/storage

2. **PostgreSQL Documentation**
   - RLS Documentation: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
   - Index Types: https://www.postgresql.org/docs/current/indexes-types.html
   - Query Planning: https://www.postgresql.org/docs/current/using-explain.html

3. **Security Best Practices**
   - OWASP Top 10: https://owasp.org/www-project-top-ten/
   - JWT Security: https://auth0.com/blog/refresh-tokens-what-are-they-and-how-to-use-them/

4. **Performance Optimization**
   - PostgreSQL Performance: https://www.postgresql.org/docs/current/performance-tips.html
   - Connection Pooling: https://supabase.com/docs/guides/database/connection-pooling

5. **Edge Functions**
   - Deno Documentation: https://docs.deno.com/
   - Supabase Edge Functions: https://supabase.com/docs/guides/functions

---

**Related Documents**:
- `best-practice.md` - Complementary guide to avoid these anti-patterns
- `architecture.md` - Understanding Supabase architecture to design better
- `checklist.md` - Pre-deployment checklist to verify anti-patterns are avoided
