---
title: "Supabase Decision Tree"
description: "Cây quyết định giúp chọn đúng Supabase feature cho từng use case"
tags: ["supabase", "decision-tree", "architecture", "patterns", "guidance"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Supabase Decision Tree

## Overview

Supabase cung cấp nhiều services và features, đôi khi developers face challenges trong việc chọn đúng approach cho specific use cases. Decision tree này cung cấp structured guidance để help make informed decisions về architecture và implementation choices.

Each decision point được designed để narrow down options based on specific requirements và constraints. Flowcharts provide visual representation of the decision process, while detailed sections explain each option with pros, cons, và examples.

Sử dụng decision tree này khi designing new features, refactoring existing code, hoặc troubleshooting performance issues. The tree covers major architectural decisions: where to run logic, how to secure data access, when to use different Supabase services.

## Purpose

Mục đích chính của decision tree này là:

1. **Reduce Decision Time**: Provide quick guidance for common architectural decisions
2. **Prevent Mistakes**: Help avoid common misuses of Supabase features
3. **Standardize Approaches**: Ensure consistent decisions across the team
4. **Enable Self-Service**: Allow developers to make decisions without waiting for senior review

## Decision Flowchart

```
┌─────────────────────────────────────────────────────────────────────┐
│                        START: Feature Design                         │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Q1: Where should the business logic run?                            │
│       ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐│
│       │ Client-Side     │ │ Database         │ │ Edge Functions   ││
│       │ (PostgREST)     │ │ (PL/pgSQL)       │ │ (TypeScript)     ││
│       └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘│
└────────────────┼───────────────────┼───────────────────┼───────────┘
                 │                   │                   │
                 ▼                   ▼                   ▼
        [See Decision A]      [See Decision B]      [See Decision C]
```

```
┌─────────────────────────────────────────────────────────────────────┐
│  Q2: How should data access be secured?                              │
│       ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐│
│       │ RLS Policies     │ │ Server Middleware │ │ Combination       ││
│       │ (Database)       │ │ (Edge Functions)  │ │ (Both)            ││
│       └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘│
└────────────────┼───────────────────┼───────────────────┼───────────┘
                 │                   │                   │
                 ▼                   ▼                   ▼
        [See Decision D]      [See Decision E]      [See Decision F]
```

```
┌─────────────────────────────────────────────────────────────────────┐
│  Q3: Should changes be persisted or ephemeral?                        │
│       ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐│
│       │ Database Changes │ │ Broadcast         │ │ Presence         ││
│       │ (Realtime Sub)   │ │ (Low-latency)     │ │ (User Tracking)  ││
│       └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘│
└────────────────┼───────────────────┼───────────────────┼───────────┘
                 │                   │                   │
                 ▼                   ▼                   ▼
        [See Decision G]      [See Decision H]      [See Decision I]
```

## Decision A: Client-Side Logic (PostgREST)

**When to Choose**: Logic can be expressed as simple CRUD operations with PostgREST filters.

### Decision Criteria

Choose client-side logic (PostgREST) when:

- Operation is simple CRUD (create, read, update, delete)
- Logic can be expressed using PostgREST operators (eq, neq, gt, lt, in, etc.)
- No complex business rules requiring conditional logic
- No need to aggregate or compute across multiple tables in complex ways
- Response time sensitivity is moderate

### Implementation

```typescript
// Simple filter: Use PostgREST
const { data } = await supabase
    .from('posts')
    .select('*')
    .eq('status', 'published')
    .gte('created_at', startDate)
    .order('created_at', { ascending: false })
    .range(offset, offset + limit);

// Simple update: Use PostgREST
await supabase
    .from('posts')
    .update({ title: 'New Title' })
    .eq('id', postId)
    .eq('user_id', currentUserId);

// Simple delete: Use PostgREST
await supabase
    .from('posts')
    .delete()
    .eq('id', postId)
    .eq('user_id', currentUserId);
```

### Pros

- Minimal code, fast development
- Built-in pagination, filtering, sorting
- RLS policies apply automatically
- Auto-generated API, no maintenance
- Performance optimized by PostgREST

### Cons

- Limited to single-table operations
- Cannot handle complex conditional logic
- No transaction support across tables
- Limited to PostgreSQL-supported operations

### When NOT to Choose

```typescript
// DON'T use PostgREST when:
// 1. Need to update multiple tables atomically
// 2. Need complex conditional logic
// 3. Need to call external APIs
// 4. Need to compute aggregates across multiple queries
```

## Decision B: Database Functions (PL/pgSQL)

**When to Choose**: Business logic requires complex database operations, transactions, or benefits from server-side execution.

### Decision Criteria

Choose database functions when:

- Operation requires transaction across multiple tables
- Logic depends on current database state
- Complex conditional logic with multiple branches
- Data validation requires database context
- Performance benefits from server-side execution
- Need to ensure atomicity of operations

### Implementation

```sql
-- Create database function
CREATE OR REPLACE FUNCTION transfer_funds(
    from_account_id UUID,
    to_account_id UUID,
    amount NUMERIC
) RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    from_balance NUMERIC;
BEGIN
    -- Lock rows to prevent race conditions
    SELECT balance INTO from_balance
    FROM accounts
    WHERE id = from_account_id
    FOR UPDATE;
    
    IF from_balance < amount THEN
        RAISE EXCEPTION 'Insufficient funds';
    END IF;
    
    -- Atomic transfer
    UPDATE accounts SET balance = balance - amount WHERE id = from_account_id;
    UPDATE accounts SET balance = balance + amount WHERE id = to_account_id;
    
    -- Log transaction
    INSERT INTO transactions (from_account, to_account, amount)
    VALUES (from_account_id, to_account_id, amount);
    
    RETURN TRUE;
END;
$$;
```

```typescript
// Call function from client
const { data, error } = await supabase.rpc('transfer_funds', {
    from_account_id: 'xxx',
    to_account_id: 'yyy',
    amount: 100.00
});
```

### Pros

- Transaction support for atomic operations
- RLS policies apply automatically
- No round-trip overhead for complex operations
- Can use all PostgreSQL features
- Consistent with existing database patterns

### Cons

- Requires SQL knowledge
- Harder to debug and test
- Limited to PostgreSQL ecosystem
- Cold start not an issue but deployment is different

### When NOT to Choose

```sql
-- DON'T use database functions when:
// 1. Logic requires external API calls
// 2. Need language features not in PL/pgSQL
// 3. Function is too large (consider Edge Functions)
// 4. Need streaming responses
```

## Decision C: Edge Functions (TypeScript/Deno)

**When to Choose**: Logic requires server-side execution with external API calls, complex TypeScript logic, or service role permissions.

### Decision Criteria

Choose Edge Functions when:

- Need to call external APIs (payment gateways, email services)
- Complex TypeScript/Node.js ecosystem dependencies
- Logic requires SERVICE_ROLE key bypass of RLS
- Need webhook handlers
- Need custom authentication flows
- Complex error handling and retry logic
- Need streaming responses

### Implementation

```typescript
// supabase/functions/process-payment/index.ts
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
        // Initialize admin client
        const supabaseAdmin = createClient(
            Deno.env.get('SUPABASE_URL')!,
            Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
        );
        
        // Validate auth
        const authHeader = req.headers.get('Authorization');
        if (!authHeader) {
            return new Response(JSON.stringify({ error: 'Unauthorized' }), {
                status: 401,
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            });
        }
        
        const { orderId, paymentToken } = await req.json();
        
        // Call external payment API
        const paymentResult = await processPayment(paymentToken, orderId);
        
        if (paymentResult.success) {
            // Update database with admin privileges
            await supabaseAdmin
                .from('orders')
                .update({ status: 'paid', paid_at: new Date() })
                .eq('id', orderId);
        }
        
        return new Response(JSON.stringify(paymentResult), {
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
        
    } catch (error) {
        return new Response(JSON.stringify({ error: error.message }), {
            status: 500,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
    }
});
```

### Pros

- Full TypeScript/JavaScript capabilities
- Access to npm/JSR packages
- Can use service role key
- Can call external APIs
- Global edge deployment for low latency
- Independent deployment and scaling

### Cons

- Cold start latency (though minimal)
- More infrastructure to manage
- RLS bypass requires careful security design
- Higher complexity than database functions

### When NOT to Choose

```typescript
// DON'T use Edge Functions when:
// 1. Simple CRUD operations suffice
// 2. Logic is purely database operations
// 3. Cold start latency is unacceptable
// 4. Can be handled with database functions
```

## Decision D: RLS Policies Only

**When to Choose**: Data access can be controlled entirely through row-level security policies.

### Decision Criteria

Choose RLS-only security when:

- All data access fits RLS model
- Permissions can be expressed as row-level filters
- User context (auth.uid()) is sufficient
- No complex permission hierarchies
- No need for API key or additional authentication

### Implementation

```sql
-- Enable RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- User can only see own posts
CREATE POLICY "user_own_posts_select" ON posts
    FOR SELECT
    USING (user_id = auth.uid());

-- User can only insert own posts
CREATE POLICY "user_own_posts_insert" ON posts
    FOR INSERT
    WITH CHECK (user_id = auth.uid());

-- User can only update own posts
CREATE POLICY "user_own_posts_update" ON posts
    FOR UPDATE
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

-- User can only delete own posts
CREATE POLICY "user_own_posts_delete" ON posts
    FOR DELETE
    USING (user_id = auth.uid());
```

```typescript
// Client automatically respects RLS
const { data } = await supabase.from('posts').select('*');
// Returns only posts where user_id = auth.uid()
```

### Pros

- Automatic enforcement at database level
- Consistent security regardless of API entry point
- RLS policies apply to PostgREST, direct SQL, and Edge Functions
- No application code needed for access control

### Cons

- Limited to row-level and column-level filtering
- Cannot handle complex permission hierarchies
- Performance overhead on complex policies
- Limited debugging capabilities

## Decision E: Server Middleware (Edge Functions)

**When to Choose**: Security requires logic beyond what RLS can express, or additional validation beyond authentication.

### Decision Criteria

Choose server middleware when:

- Need role-based access beyond row-level
- Require custom authentication schemes
- Need to validate third-party tokens
- Complex permission hierarchies
- Rate limiting per user/action
- Audit logging requirements

### Implementation

```typescript
// supabase/functions/_shared/auth.ts
export async function validateRequest(req: Request): Promise<{
    valid: boolean;
    userId?: string;
    role?: string;
    error?: Response;
}> {
    const authHeader = req.headers.get('Authorization');
    
    if (!authHeader) {
        return {
            valid: false,
            error: new Response(JSON.stringify({ error: 'Unauthorized' }), {
                status: 401,
                headers: { 'Content-Type': 'application/json' }
            })
        };
    }
    
    const supabaseAdmin = createClient(
        Deno.env.get('SUPABASE_URL')!,
        Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    );
    
    const token = authHeader.replace('Bearer ', '');
    const { data: { user }, error } = await supabaseAdmin.auth.getUser(token);
    
    if (error || !user) {
        return {
            valid: false,
            error: new Response(JSON.stringify({ error: 'Invalid token' }), {
                status: 401,
                headers: { 'Content-Type': 'application/json' }
            })
        };
    }
    
    // Get user role from database
    const { data: profile } = await supabaseAdmin
        .from('profiles')
        .select('role')
        .eq('id', user.id)
        .single();
    
    return {
        valid: true,
        userId: user.id,
        role: profile?.role || 'user'
    };
}
```

### Pros

- Full control over authentication logic
- Can implement complex permission systems
- Easy to add logging and monitoring
- Centralized security logic

### Cons

- Requires careful implementation
- RLS bypass if using service role key
- Additional infrastructure to maintain

## Decision F: Hybrid (RLS + Middleware)

**When to Choose**: Need both database-level security and application-level validation.

### Decision Criteria

Choose hybrid approach when:

- RLS handles basic row-level access
- Middleware adds additional validation
- Need both user-scoped and admin-scoped operations
- Auditing requirements at application level

### Implementation

```sql
-- RLS for basic access
ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY "user_own_data" ON sensitive_data
    FOR ALL
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

-- Additional column-level security
CREATE POLICY "user_sees_own_data_only" ON sensitive_data
    FOR SELECT
    USING (
        user_id = auth.uid()
        OR
        EXISTS (
            SELECT 1 FROM admin_users
            WHERE user_id = auth.uid() AND has_admin_access = true
        )
    );
```

```typescript
// Edge Function adds additional validation
export default async (req: Request) => {
    const { valid, userId, error } = await validateRequest(req);
    if (!valid) return error!;
    
    // Additional business rule validation
    const { data: userData } = await supabaseAdmin
        .from('profiles')
        .select('subscription_tier')
        .eq('id', userId)
        .single();
    
    if (userData.subscription_tier === 'free' && req.body.includes('premium_feature')) {
        return new Response(JSON.stringify({ error: 'Upgrade required' }), {
            status: 403
        });
    }
    
    // Proceed with RLS-protected operation
    const { data } = await supabase.from('sensitive_data').select('*');
    return new Response(JSON.stringify(data));
};
```

## Decision G: Database Changes (Realtime Subscription)

**When to Choose**: Need to persist data changes and notify clients about them.

### Decision Criteria

Choose database changes subscriptions when:

- Data changes need to be persisted
- Multiple clients need to see updates
- Historical change tracking required
- Changes trigger other database operations

### Implementation

```typescript
// Subscribe to INSERT
const channel = supabase
    .channel('new-posts')
    .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'posts',
        filter: 'status=eq.published'
    }, (payload) => {
        const newPost = payload.new as Post;
        addToFeed(newPost);
    })
    .subscribe();

// Subscribe to UPDATE
supabase
    .channel('post-updates')
    .on('postgres_changes', {
        event: 'UPDATE',
        schema: 'public',
        table: 'posts'
    }, (payload) => {
        updatePostInUI(payload.new.id, payload.new);
    })
    .subscribe();

// Subscribe to DELETE
supabase
    .channel('post-deletes')
    .on('postgres_changes', {
        event: 'DELETE',
        schema: 'public',
        table: 'posts'
    }, (payload) => {
        removePostFromUI(payload.old.id);
    })
    .subscribe();
```

## Decision H: Broadcast (Ephemeral Messaging)

**When to Choose**: Need low-latency messaging that doesn't need to be persisted.

### Decision Criteria

Choose Broadcast when:

- Cursor/presence updates
- Typing indicators
- Live collaboration state
- Gaming/game state
- Notifications that don't need persistence

### Implementation

```typescript
// Setup broadcast channel
const channel = supabase.channel('collaboration-session');

// Listen for cursor updates
channel.on('broadcast', { event: 'cursor' }, ({ payload }) => {
    updateOtherUserCursor(payload.userId, payload.position);
});

// Listen for typing status
channel.on('broadcast', { event: 'typing' }, ({ payload }) => {
    showTypingIndicator(payload.userId, payload.isTyping);
});

channel.subscribe();

// Send cursor update
function sendCursorPosition(position: { x: number; y: number }) {
    channel.send({
        type: 'broadcast',
        event: 'cursor',
        payload: {
            userId: currentUserId,
            position
        }
    });
}

// Send typing status
function sendTypingStatus(isTyping: boolean) {
    channel.send({
        type: 'broadcast',
        event: 'typing',
        payload: {
            userId: currentUserId,
            isTyping
        }
    });
}
```

## Decision I: Presence (User Tracking)

**When to Choose**: Need to track and display online/offline status of users.

### Decision Criteria

Choose Presence when:

- Show online/offline status
- Track who's viewing a page/document
- Implement "active users" features
- Collaborative editing awareness

### Implementation

```typescript
// Setup presence channel
const channel = supabase.channel('document-presence', {
    config: { presence: { key: currentUserId } }
});

// Listen for presence sync
channel.on('presence', { event: 'sync' }, () => {
    const state = channel.presenceState();
    const onlineUsers = Object.values(state).flat() as UserPresence[];
    updateOnlineUserList(onlineUsers);
});

// Listen for user join
channel.on('presence', { event: 'join' }, ({ key, newPresences }) => {
    newPresences.forEach(presence => {
        showNotification(`${presence.name} joined`);
    });
});

// Listen for user leave
channel.on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
    leftPresences.forEach(presence => {
        showNotification(`${presence.name} left`);
    });
});

channel.subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
        await channel.track({
            user_id: currentUserId,
            name: currentUserName,
            avatar: currentUserAvatar,
            online_at: new Date().toISOString()
        });
    }
});
```

## Storage Decision Matrix

| Use Case | Storage Type | Access Pattern | Recommended Approach |
|----------|-------------|---------------|---------------------|
| User avatars | Public bucket | Direct URL | Public bucket, CDN cached |
| User uploads | Private bucket | Signed URL | Private bucket, time-limited signed URLs |
| Generated thumbnails | Public bucket | Direct URL | Transform on upload, store separately |
| Temporary files | Private bucket | Signed URL | Short expiry, cleanup policy |
| Large files (video) | Public bucket | Signed URL | Large signed URL expiry |

### Implementation Examples

```typescript
// Public file access
const avatarUrl = supabase.storage.from('avatars').getPublicUrl(userId + '/avatar.jpg');

// Private file with signed URL
const { data } = await supabase.storage
    .from('documents')
    .createSignedUrl('invoice.pdf', 3600); // 1 hour expiry

// Upload with path restriction
async function uploadUserFile(file: File, userId: string) {
    const path = `${userId}/${Date.now()}-${file.name}`;
    const { data, error } = await supabase.storage
        .from('user-files')
        .upload(path, file);
    return { data, error, path };
}
```

## API Design Decision Matrix

| Requirement | PostgREST | Database Function | Edge Function |
|-------------|-----------|-------------------|--------------|
| Simple CRUD | ✅ Best | ❌ Overkill | ❌ Overkill |
| Complex queries | ❌ Limited | ✅ Best | ⚠️ Complex |
| Transaction | ❌ Not supported | ✅ Best | ⚠️ Manual |
| External API call | ❌ Not supported | ❌ Not supported | ✅ Best |
| Real-time updates | ✅ Best | ⚠️ Manual | ⚠️ Manual |
| RLS integration | ✅ Automatic | ✅ Automatic | ⚠️ Manual |
| Cold start | ✅ None | ✅ None | ⚠️ ~200ms |

## Quick Reference

### When to Use Database Functions vs Edge Functions

```
┌─────────────────────────────────────────────────────────────────┐
│                      Logic Complexity                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Low Complexity                    High Complexity               │
│  ┌─────────────────────┐         ┌─────────────────────┐        │
│  │ • Simple filters   │         │ • External APIs     │        │
│  │ • Basic validation │         │ • Complex logic     │        │
│  │ • Single table ops │         │ • Multiple tables   │        │
│  │ • Conditional updates│        │ • Error handling    │        │
│  └─────────────────────┘         └─────────────────────┘        │
│         │                                  │                    │
│         ▼                                  ▼                    │
│  ┌─────────────────────┐         ┌─────────────────────┐       │
│  │  PostgREST / RLS    │         │  Database Funcs     │       │
│  │  (Preferred)        │         │  (If transaction    │       │
│  │                     │         │   or PostgreSQL     │       │
│  │                     │         │   features needed) │       │
│  └─────────────────────┘         └─────────────────────┘       │
│                                    Or                           │
│                                 ┌─────────────────────┐        │
│                                 │  Edge Functions     │        │
│                                 │  (If TypeScript or  │        │
│                                 │   external APIs     │        │
│                                 │   needed)           │        │
│                                 └─────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

### When to Use RLS vs Application Security

```
┌─────────────────────────────────────────────────────────────────┐
│                        Security Scope                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Data-Level Security              Application-Level Security     │
│  (Use RLS)                       (Use Middleware/Edge Functions) │
│  ┌─────────────────────┐         ┌─────────────────────┐       │
│  │ • Row access        │         │ • Rate limiting     │       │
│  │ • User ownership    │         │ • Role verification │      │
│  │ • Tenant isolation  │         │ • API key validation│       │
│  │ • Basic read/write  │         │ • Complex permissions│      │
│  │   restrictions      │         │ • Audit logging     │      │
│  └─────────────────────┘         └─────────────────────┘       │
│                                                                  │
│                     ┌─────────────────────┐                     │
│                     │   Combine Both      │                     │
│                     │   for defense in    │                     │
│                     │   depth             │                     │
│                     └─────────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

## Common Patterns

### Pattern 1: Simple CRUD with RLS

**Best For**: Basic blog, social app, user profiles

```
Client → PostgREST → RLS → PostgreSQL
```

```typescript
// All operations respect RLS automatically
const { data } = await supabase.from('posts').select('*');
await supabase.from('posts').insert({ title: 'New' });
await supabase.from('posts').update({ title: 'Updated' }).eq('id', id);
```

### Pattern 2: Complex Logic with Database Functions

**Best For**: Financial transactions, inventory management, complex business rules

```
Client → RPC → PostgreSQL Function (with RLS) → PostgreSQL
```

```typescript
const { data } = await supabase.rpc('transfer_funds', {
    from_id: 'xxx',
    to_id: 'yyy',
    amount: 100
});
```

### Pattern 3: External Integration with Edge Functions

**Best For**: Payment processing, email sending, webhooks, third-party APIs

```
Client → Edge Function → External API + PostgreSQL
```

```typescript
// Payment processing
const { data } = await supabase.functions.invoke('process-payment', {
    body: { orderId, paymentToken }
});
```

### Pattern 4: Multi-Layer Security

**Best For**: Enterprise applications, financial services, healthcare

```
Client → Edge Function (auth + validation) → PostgreSQL (RLS + functions)
```

```typescript
// Edge function validates request
const { valid, userId, role } = await validateRequest(req);

// Then uses RLS-protected operations
const { data } = await supabase.from('sensitive_data').select('*');
```

## Troubleshooting Decision Mistakes

### Mistake 1: Using Edge Functions for Simple CRUD

**Problem**: Using Edge Functions when PostgREST would suffice

**Solution**:
```typescript
// ❌ Wrong: Edge Function for simple read
export default async (req: Request) => {
    const { data } = await supabaseAdmin.from('posts').select('*');
    return new Response(JSON.stringify(data));
};

// ✅ Correct: PostgREST directly
const { data } = await supabase.from('posts').select('*');
```

### Mistake 2: Complex RLS Policies

**Problem**: RLS policies too complex, hurting performance

**Solution**:
```sql
-- ❌ Wrong: Multiple subqueries in policy
CREATE POLICY "complex" ON orders FOR SELECT USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND
        EXISTS (SELECT 1 FROM subscriptions WHERE user_id = users.id AND active = true))
);

// ✅ Correct: Use SECURITY DEFINER function
CREATE OR REPLACE FUNCTION user_has_active_subscription()
RETURNS BOOLEAN AS $$
    SELECT EXISTS (
        SELECT 1 FROM subscriptions s
        JOIN users u ON s.user_id = u.id
        WHERE u.id = auth.uid() AND s.active = true
    );
$$ LANGUAGE sql SECURITY DEFINER;

CREATE POLICY "simple" ON orders FOR SELECT USING (user_has_active_subscription());
```

### Mistake 3: Not Using Realtime When Needed

**Problem**: Polling for changes instead of using realtime

**Solution**:
```typescript
// ❌ Wrong: Polling
async function checkForUpdates() {
    const { data } = await supabase.from('messages').select('*');
    updateUI(data);
    setTimeout(checkForUpdates, 5000);
}

// ✅ Correct: Realtime subscription
supabase
    .channel('messages')
    .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'messages'
    }, (payload) => {
        addMessage(payload.new);
    })
    .subscribe();
```

## References

1. **Official Documentation**
   - Supabase Docs: https://supabase.com/docs
   - PostgREST: https://postgrest.org/
   - Deno: https://docs.deno.com/

2. **Architecture Guides**
   - Supabase GitHub: https://github.com/supabase/supabase
   - Realtime Architecture: https://github.com/supabase/realtime

3. **Best Practices**
   - `best-practice.md` - Detailed implementation guidance
   - `anti-pattern.md` - Common mistakes to avoid
   - `checklist.md` - Pre-deployment verification

---

**Related Documents**:
- `architecture.md` - System architecture overview
- `best-practice.md` - Detailed best practices
- `glossary.md` - Term definitions
