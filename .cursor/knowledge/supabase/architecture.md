---
title: "Supabase Architecture"
description: "Tổng quan kiến trúc Supabase - PostgreSQL core, PostgREST, GoTrue, Storage, Realtime, Edge Functions"
tags: ["supabase", "architecture", "postgresql", "postgrest", "gotrue", "storage", "realtime", "edge-functions", "pgvector"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Supabase Architecture

## Overview

Supabase là một open-source Backend-as-a-Service (BaaS) platform được xây dựng trên PostgreSQL, cung cấp một suite của backend services bao gồm database, authentication, realtime subscriptions, file storage, và serverless edge functions. Kiến trúc này được thiết kế để leverage PostgreSQL's robustness và extensibility trong khi providing developer-friendly APIs và abstractions.

Supabase được create bởi Paul Copplestone và được launch vào năm 2020 như một open-source alternative cho Firebase. Platform này đã phát triển nhanh chóng nhờ vào active community contributions và enterprise adoption. Kiến trúc của Supabase tận dụng PostgreSQL làm single source of truth, với các services được add như layers trên top.

Understanding Supabase's architecture giúp developers make better decisions về application design, performance optimization, và scalability planning. Tài liệu này provides comprehensive overview của mỗi component và how they interact.

## Purpose

Tài liệu này phục vụ các mục đích chính sau:

1. **System Understanding**: Provide deep understanding của Supabase's components và how they work together
2. **Architecture Decisions**: Guide architecture decisions cho Supabase-based applications
3. **Performance Optimization**: Help identify optimization opportunities với understanding of data flow
4. **Troubleshooting**: Enable effective troubleshooting by understanding component interactions
5. **Scaling Planning**: Support capacity planning và scaling decisions

Mỗi section mô tả một component của Supabase architecture, bao gồm its purpose, how it works, và practical considerations for usage.

## System Architecture Overview

### High-Level Architecture

Supabase architecture có thể được visualize như một layered system:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Applications                       │
│         (Web, Mobile, Desktop, Server-side Applications)         │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                           API Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  PostgREST  │  │  GoTrue     │  │  Storage    │             │
│  │  (REST API) │  │  (Auth API) │  │  (Files)    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│  ┌─────────────────────────────────────────────────────┐       │
│  │                 Edge Functions (Deno)               │       │
│  └─────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Service Layer                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Realtime   │  │  PgBouncer  │  │  Logflare   │             │
│  │  (WebSocket)│  │  (Pooling)  │  │  (Logging)  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                        PostgreSQL Core                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Storage   │  │   Query     │  │   RLS       │             │
│  │   Engine    │  │   Engine    │  │   Engine    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Extensions (pgvector, PostGIS, etc.)       │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

Understanding data flow là essential cho performance optimization:

**Read Path**:
1. Client sends request via REST/WebSocket
2. PostgREST validates request and extracts auth context
3. PostgreSQL evaluates RLS policies against auth context
4. Query executes with policy restrictions applied
5. Results filtered by policies returned to client

**Write Path**:
1. Client sends mutation request with auth token
2. PostgREST validates JWT token
3. PostgreSQL evaluates RLS policies (WITH CHECK clause)
4. Write operation executes if policies pass
5. Triggers fire if defined
6. Realtime publishes change to subscribers
7. Confirmation returned to client

## PostgreSQL Core

### Why PostgreSQL

PostgreSQL được chọn làm foundation cho Supabase vì nhiều lý do:

**Reliability**: PostgreSQL có reputation cho data integrity và ACID compliance. Transactions work correctly, preventing data corruption.

**Extensibility**: PostgreSQL supports extensions cho specialized use cases như vector storage (pgvector), geographic data (PostGIS), full-text search, và time-series data.

**Maturity**: With over 35 years of development, PostgreSQL is battle-tested và well-understood. Large talent pool available.

**Standards Compliance**: Full SQL standard compliance ensures predictable behavior và portability.

**Performance**: Advanced query optimizer, parallel query execution, và sophisticated indexing mechanisms.

### PostgreSQL in Supabase

Supabase runs PostgreSQL on managed infrastructure với several optimizations:

**Configuration Tweaks**:
- `wal_level = logical` cho replication và realtime
- `max_replication_slots` configured for realtime
- Shared preload libraries for extensions

**Managed Services**:
- Automatic backups với point-in-time recovery
- Automatic minor version upgrades
- Connection pooling via PgBouncer
- Load balancing across replicas

### Connection Pooling

Connection pooling là critical cho Supabase's multi-tenant architecture:

**PgBouncer Integration**:
Supabase sử dụng PgBouncer để multiplex many client connections over fewer database connections:

```sql
-- PgBouncer connection stats
SELECT * FROM pgbouncer.pools;

-- Check connection mode
SHOW pool_mode;

-- Check active connections
SHOW clients;
SHOW servers;
```

**Pooling Modes**:

1. **Session Mode**: Connections held for entire session. Best for long transactions and prepared statements.

2. **Transaction Mode**: Connections released after each transaction. Best for HTTP request/response patterns. Not suitable for PostgreSQL features requiring session state.

3. **Statement Mode**: Connections released after each statement. Most aggressive pooling. Not suitable for transactions.

```typescript
// Connection with specified pool mode
import { Pool } from 'pg';

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    // In transaction mode, prepared statements don't persist
    // In session mode, they work normally
});

// Default Supabase client uses transaction mode
import { createClient } from '@supabase/supabase-js';
const supabase = createClient(url, key);
// Internally uses transaction mode pooling
```

### Extensions

Supabase enables several PostgreSQL extensions out of the box:

**Core Extensions**:
- `uuid-ossp`: UUID generation functions
- `pgcrypto`: Cryptographic functions
- `pgjwt`: JWT functions for PostgreSQL
- `pg_net`: HTTP requests from database
- `vault`: Secure secrets storage

**Specialized Extensions**:
- `pgvector`: Vector storage và similarity search
- `pg_trgm`: Trigram matching for fuzzy search
- `fuzzystrmatch`: String similarity functions
- `postgis`: Geographic data types và functions
- `pg_partman`: Table partitioning management
- `supabase-js`: Custom functions for Supabase features

## PostgREST

### Overview

PostgREST là a standalone web server that turns your PostgreSQL database directly into a RESTful API. Trong Supabase, PostgREST được integrated để provide auto-generated CRUD APIs:

**Key Features**:
- Auto-generated CRUD endpoints
- Filtering và sorting
- Pagination
- Relationship embedding
- Stored procedure calls
- JWT authentication integration

### API Structure

PostgREST exposes PostgreSQL schema as REST endpoints:

```
GET    /table              → SELECT * FROM table
POST   /table              → INSERT INTO table
GET    /table?id=eq.1      → SELECT * FROM table WHERE id = 1
PATCH  /table?id=eq.1      → UPDATE table SET ... WHERE id = 1
DELETE /table?id=eq.1      → DELETE FROM table WHERE id = 1
```

**Filtering Operators**:
```
eq      - Equals
neq     - Not equals
gt      - Greater than
gte     - Greater than or equal
lt      - Less than
lte     - Less than or equal
like    - LIKE pattern match
ilike   - Case-insensitive LIKE
in      - Value in list
is      - IS NULL / IS TRUE / IS FALSE
cs      - Contains (for arrays/JSONB)
cd      - Contained by (for arrays/JSONB)
```

**Example Queries**:
```typescript
// Basic fetch
const { data } = await supabase.from('posts').select('*');

// Filter
const { data } = await supabase
    .from('posts')
    .select('*')
    .eq('status', 'published')
    .gte('created_at', '2024-01-01');

// Complex filter
const { data } = await supabase
    .from('posts')
    .select('*, comments(*)')
    .eq('status', 'published')
    .in('category', ['tech', 'science'])
    .order('created_at', { ascending: false })
    .range(0, 19);

// RPC call
const { data } = await supabase.rpc('function_name', { param: 'value' });
```

### RLS Integration

PostgREST integrates với PostgreSQL's RLS to filter results:

**Request Flow**:
1. Client sends request with Authorization header
2. PostgREST decodes JWT to extract user ID (auth.uid())
3. PostgreSQL evaluates RLS policies using this ID
4. Results are filtered according to policy restrictions

```sql
-- Example: RLS policy evaluated by PostgREST
CREATE POLICY "Users see own posts"
    ON posts FOR SELECT
    USING (user_id = auth.uid());

-- PostgREST automatically injects auth context
-- Equivalent to: SELECT * FROM posts WHERE user_id = current_setting('request.jwt.claim.sub');
```

### Performance Considerations

**Index Strategy**: PostgREST queries benefit from proper indexing:

```sql
-- Index for filter column
CREATE INDEX idx_posts_status ON posts(status);

-- Index for foreign key joins
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Composite index for common query patterns
CREATE INDEX idx_posts_user_status ON posts(user_id, status);
```

**Query Optimization**:
```typescript
// Bad: Select all columns
supabase.from('posts').select('*');

// Good: Select only needed columns
supabase.from('posts').select('id, title, created_at');

// Avoid N+1: Use embedding
const { data } = await supabase
    .from('posts')
    .select('*, author:users(name), comments(*)');
```

## GoTrue (Authentication)

### Architecture

GoTrue là authentication server được developed bởi Netlify và adopted by Supabase. It provides:

- User management (signup, login, logout)
- JWT token issuance và validation
- OAuth provider integration
- Password reset và email confirmation
- Session management

**Supabase Auth Flow**:
```
┌──────────┐     1. Sign Up      ┌──────────┐
│  Client  │ ─────────────────► │  GoTrue  │
└──────────┘                    └──────────┘
     │                                │
     │                                │ 2. Create User
     │                                ▼
     │                           ┌──────────┐
     │                           │ PostgreSQL│
     │                           │  (auth)  │
     │                           └──────────┘
     │                                │
     │◄──────────────────────────────┘
     │         3. JWT Token
```

### JWT Token Structure

Supabase JWTs contain standard claims và custom metadata:

```json
{
  "iss": "supabase",
  "iat": 1700000000,
  "exp": 1700003600,
  "jti": "unique-token-id",
  "role": "authenticated",
  "sub": "user-uuid",
  "email": "user@example.com",
  "app_metadata": {
    "provider": "email",
    "providers": ["email"]
  },
  "user_metadata": {
    "name": "John Doe"
  }
}
```

**Token Claims**:
- `sub`: User ID (maps to auth.uid())
- `role`: Always "authenticated" for logged-in users
- `email`: User's email address
- `app_metadata`: Provider and provider-specific data
- `user_metadata`: Custom user fields

### Auth Providers

**Email/Password**:
```typescript
const { data, error } = await supabase.auth.signUp({
    email: 'user@example.com',
    password: 'secure-password'
});

const { data, error } = await supabase.auth.signInWithPassword({
    email: 'user@example.com',
    password: 'secure-password'
});
```

**OAuth Providers**:
```typescript
const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
        redirectTo: 'https://app.example.com/callback'
    }
});
```

**Magic Links**:
```typescript
const { data, error } = await supabase.auth.signInWithOtp({
    email: 'user@example.com',
    options: {
        emailRedirectTo: 'https://app.example.com/callback'
    }
});
```

### Session Management

**Client-Side Session**:
```typescript
// Supabase client handles session automatically
const supabase = createClient(url, key);

// Access current session
const { data: { session } } = await supabase.auth.getSession();

// Listen to auth changes
supabase.auth.onAuthStateChange((event, session) => {
    if (event === 'SIGNED_IN') {
        console.log('User signed in:', session.user);
    }
    if (event === 'SIGNED_OUT') {
        console.log('User signed out');
    }
    if (event === 'TOKEN_REFRESHED') {
        console.log('Token refreshed:', session);
    }
});
```

**Server-Side Validation**:
```typescript
// Edge Function validation
export async function validateToken(req: Request) {
    const token = req.headers.get('Authorization')?.replace('Bearer ', '');
    
    if (!token) {
        return new Response('Unauthorized', { status: 401 });
    }
    
    const { data: { user }, error } = await supabaseAdmin.auth.getUser(token);
    
    if (error || !user) {
        return new Response('Invalid token', { status: 401 });
    }
    
    // user.id contains the authenticated user's ID
    return new Response(JSON.stringify({ userId: user.id }));
}
```

## Storage

### Architecture

Supabase Storage sử dụng S3-compatible object storage với PostgreSQL-backed metadata:

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│    Client    │ ───► │   Storage    │ ───► │     S3       │
│              │      │    API       │      │   Storage    │
└──────────────┘      └──────────────┘      └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  PostgreSQL  │
                     │  (metadata)  │
                     └──────────────┘
```

### Storage Components

**Buckets**: Containers for files, analogous to S3 buckets:
```typescript
// Create bucket via SQL
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', true);
```

**Files**: Stored in S3 with metadata in PostgreSQL:
```sql
-- Storage objects table (managed by Supabase)
SELECT * FROM storage.objects LIMIT 10;
```

**Policies**: RLS-like access control for storage:
```sql
-- Allow users to upload to their folder
CREATE POLICY "User uploads"
    ON storage.objects FOR INSERT
    WITH CHECK (
        auth.uid()::text = (storage.foldername(name))[1]
    );
```

### Storage Operations

**Upload**:
```typescript
const { data, error } = await supabase.storage
    .from('avatars')
    .upload('user-123/avatar.jpg', file);
```

**Download**:
```typescript
// Download file
const { data, error } = await supabase.storage
    .from('avatars')
    .download('user-123/avatar.jpg');

// Get public URL
const { data } = supabase.storage
    .from('avatars')
    .getPublicUrl('user-123/avatar.jpg');
```

**Signed URLs for Private Files**:
```typescript
const { data, error } = await supabase.storage
    .from('private-docs')
    .createSignedUrl('document.pdf', 3600); // 1 hour expiry
```

### Image Transformations

Supabase Storage supports on-the-fly image transformations:

```typescript
const transformedUrl = supabase.storage
    .from('images')
    .getPublicUrl('photo.jpg', {
        width: 800,
        height: 600,
        resize: 'cover',
        format: 'auto',
        quality: 80
    });
```

**Transformation Options**:
- `width`, `height`: Output dimensions
- `resize`: 'cover', 'contain', 'fill'
- `format`: 'auto', 'webp', 'avif', 'jpeg', 'png'
- `quality`: 1-100

## Realtime

### Architecture

Realtime enables subscribing to database changes via WebSocket connections:

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│    Client    │ ◄──► │   Realtime   │ ◄──► │  PostgreSQL  │
│   (Browser)  │      │   Server     │      │  (Logical   │
│              │      │  (Elixir)    │      │   WAL)       │
└──────────────┘      └──────────────┘      └──────────────┘
```

### Realtime Components

**WAL (Write-Ahead Log) Listener**: Reads PostgreSQL WAL to capture changes:

```sql
-- Enable logical replication for realtime
ALTER PUBLICATION supabase_realtime ADD TABLE your_table;
```

**Broadcast**: For low-latency messaging not persisted to database:

```typescript
channel.send({
    type: 'broadcast',
    event: 'cursor',
    payload: { x: 100, y: 200 }
});
```

**Presence**: For tracking user presence state:

```typescript
channel.track({ user_id: '123', online_at: new Date() });
const state = channel.presenceState();
```

### Subscription Types

**Database Changes**:
```typescript
const channel = supabase
    .channel('db-changes')
    .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'messages'
    }, (payload) => {
        console.log('Change:', payload);
    })
    .subscribe();
```

**Broadcast**:
```typescript
const channel = supabase
    .channel('chat-room')
    .on('broadcast', { event: 'new-message' }, (payload) => {
        console.log('Message:', payload.payload);
    })
    .subscribe();

// Send message
channel.send({
    type: 'broadcast',
    event: 'new-message',
    payload: { text: 'Hello!' }
});
```

**Presence**:
```typescript
const channel = supabase
    .channel('online-users')
    .on('presence', { event: 'sync' }, () => {
        const users = channel.presenceState();
        updateUserList(users);
    })
    .subscribe();

// Track presence
await channel.track({ user_id: userId, name: userName });
```

## Edge Functions

### Architecture

Edge Functions là serverless TypeScript functions deployed to edge locations:

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│    Client    │ ───► │    Deno      │ ───► │  Supabase    │
│              │      │   Runtime    │      │   Services    │
└──────────────┘      │  (Edge)      │      └──────────────┘
                      └──────────────┘
```

### Deno Runtime

Supabase Edge Functions run on Deno, not Node.js:

**Deno vs Node.js**:
- Native TypeScript support (no build step)
- Standard library available without npm
- Permission-based security model
- ES modules by default
- Top-level await support

**Import Patterns**:
```typescript
// Deno standard library
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

// NPM packages via JSR or npm: specifiers
import { createClient } from 'jsr:@supabase/supabase-js@2';
import express from 'npm:express@4';

// File imports
import { helpers } from './_shared/helpers.ts';
```

### Function Structure

```typescript
// supabase/functions/my-function/index.ts
import { createClient } from 'jsr:@supabase/supabase-js@2';

const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

Deno.serve(async (req) => {
    // Handle CORS preflight
    if (req.method === 'OPTIONS') {
        return new Response(null, { headers: corsHeaders });
    }
    
    try {
        // Get authorization
        const authHeader = req.headers.get('Authorization');
        
        // Initialize admin client
        const supabaseAdmin = createClient(
            Deno.env.get('SUPABASE_URL')!,
            Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
        );
        
        // Validate token
        if (authHeader) {
            const token = authHeader.replace('Bearer ', '');
            const { data: { user } } = await supabaseAdmin.auth.getUser(token);
        }
        
        // Process request
        const { data: result } = await supabaseAdmin.from('table').select('*');
        
        return new Response(JSON.stringify(result), {
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

### Shared Code

Share common utilities across functions:

```
supabase/functions/
├── _shared/
│   ├── database.ts      # Database client
│   ├── auth.ts          # Auth helpers
│   └── constants.ts     # Shared constants
├── function-a/
│   └── index.ts
└── function-b/
    └── index.ts
```

```typescript
// supabase/functions/_shared/database.ts
import { createClient } from 'jsr:@supabase/supabase-js@2';

let adminClient: ReturnType<typeof createClient> | null = null;

export function getAdminClient() {
    if (!adminClient) {
        adminClient = createClient(
            Deno.env.get('SUPABASE_URL')!,
            Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
            { auth: { persistSession: false } }
        );
    }
    return adminClient;
}
```

## pgvector Integration

### Vector Storage

pgvector enables vector storage and similarity search in PostgreSQL:

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with vector column
CREATE TABLE embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI ada-002 dimension
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for similarity search
CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops);
```

### Vector Operations

```typescript
// Insert embedding
await supabase.from('embeddings').insert({
    content: 'Sample text',
    embedding: [0.1, 0.2, ...]  // 1536-dimensional array
});

// Search for similar content
const { data } = await supabase.rpc('match_embeddings', {
    query_embedding: queryVector,
    match_threshold: 0.78,
    match_count: 5
});
```

```sql
-- Similarity search function
CREATE OR REPLACE FUNCTION match_embeddings(
    query_embedding vector,
    match_threshold FLOAT,
    match_count INT
)
RETURNS TABLE (
    id UUID,
    content TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        e.id,
        e.content,
        1 - (e.embedding <=> query_embedding) AS similarity
    FROM embeddings e
    WHERE 1 - (e.embedding <=> query_embedding) > match_threshold
    ORDER BY e.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
```

### RAG Implementation

Combine pgvector với full-text search for hybrid search:

```sql
-- Create full-text search index
CREATE INDEX idx_content_fts ON embeddings USING gin(to_tsvector('english', content));

-- Hybrid search function
CREATE OR REPLACE FUNCTION hybrid_search(
    query_text TEXT,
    query_embedding vector,
    match_threshold FLOAT,
    match_count INT
)
RETURNS TABLE (
    id UUID,
    content TEXT,
    similarity FLOAT,
    ts_rank FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        e.id,
        e.content,
        1 - (e.embedding <=> query_embedding) AS similarity,
        ts_rank(to_tsvector('english', e.content), plainto_tsquery('english', query_text)) AS ts_rank
    FROM embeddings e
    WHERE (
        1 - (e.embedding <=> query_embedding) > match_threshold
    )
    AND (
        to_tsvector('english', e.content) @@ plainto_tsquery('english', query_text)
        OR query_text = ''
    )
    ORDER BY similarity DESC, ts_rank DESC
    LIMIT match_count;
END;
$$;
```

## Monitoring and Observability

### Supabase Dashboard

**Database Metrics**:
- Connection usage
- Query performance
- Table sizes
- Index usage
- Replication lag

**Auth Metrics**:
- Active sessions
- Login attempts
- New user signups
- Failed authentications

**Storage Metrics**:
- Bucket sizes
- Bandwidth usage
- Upload/download counts

**Realtime Metrics**:
- Active connections
- Message throughput
- Channel subscriptions

### Custom Monitoring

**Structured Logging**:
```typescript
// Edge function with structured logging
export default async (req: Request) => {
    const startTime = Date.now();
    
    try {
        console.log(JSON.stringify({
            level: 'info',
            message: 'Processing request',
            method: req.method,
            path: new URL(req.url).pathname,
            timestamp: new Date().toISOString()
        }));
        
        // Process request...
        
        console.log(JSON.stringify({
            level: 'info',
            message: 'Request completed',
            duration_ms: Date.now() - startTime,
            timestamp: new Date().toISOString()
        }));
        
    } catch (error) {
        console.log(JSON.stringify({
            level: 'error',
            message: error.message,
            stack: error.stack,
            duration_ms: Date.now() - startTime,
            timestamp: new Date().toISOString()
        }));
    }
};
```

**Metrics Export**:
```typescript
// Export Prometheus metrics
export const metricsHandler = async (req: Request) => {
    const requestCount = await getRequestCount();
    const errorCount = await getErrorCount();
    const avgLatency = await getAvgLatency();
    
    const prometheusMetrics = `
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total ${requestCount}

# HELP http_errors_total Total HTTP errors
# TYPE http_errors_total counter
http_errors_total ${errorCount}

# HELP http_request_duration_ms Average request duration
# TYPE http_request_duration_ms gauge
http_request_duration_ms ${avgLatency}
`.trim();
    
    return new Response(prometheusMetrics, {
        headers: { 'Content-Type': 'text/plain' }
    });
};
```

## Scalability Considerations

### Horizontal Scaling

**Read Replicas**: Distribute read queries across replicas:

```typescript
// Use read replica for read-heavy operations
const supabaseRead = createClient(
    'https://read-replica.supabase.co',
    anonKey
);
```

**Connection Pooling**: Configure for expected load:

```bash
# Pool size configuration
# Default: 10 connections per instance
# For high traffic: 20-50 connections

# Set via Supabase dashboard or CLI
supabase config set PGBOUNCER_POOL_MODE=transaction
supabase config set PGBOUNCER_MAX_CLIENT_CONN=1000
```

### Vertical Scaling

**Database Size**: Upgrade instance size for compute-intensive workloads:

- Free tier: 0.5GB RAM, shared CPU
- Pro tier: 1GB RAM per 125GB storage
- Team tier: Configurable vCPUs and RAM
- Enterprise: Dedicated resources

**Storage Scaling**: Automatic with tier upgrades

### Caching Strategies

**Application-Level Cache**:
```typescript
const cache = new Map();
const CACHE_TTL = 60000; // 1 minute

export async function getCachedData(key: string) {
    const cached = cache.get(key);
    if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
        return cached.data;
    }
    
    const data = await fetchFromDatabase(key);
    cache.set(key, { data, timestamp: Date.now() });
    return data;
}
```

**CDN for Static Assets**:
```typescript
// Upload to storage, serve via CDN
const { data } = supabase.storage
    .from('public-assets')
    .getPublicUrl('images/hero.jpg');

// CDN automatically serves from edge locations
```

## References

1. **Official Documentation**
   - Supabase Docs: https://supabase.com/docs
   - PostgREST: https://postgrest.org/
   - PostgreSQL: https://www.postgresql.org/docs/
   - Deno: https://docs.deno.com/

2. **Architecture Resources**
   - Supabase GitHub: https://github.com/supabase/supabase
   - Realtime Architecture: https://github.com/supabase/realtime
   - GoTrue: https://github.com/supabase/gotrue

3. **Extensions**
   - pgvector: https://github.com/pgvector/pgvector
   - PostGIS: https://postgis.net/
   - PgBouncer: https://www.pgbouncer.org/

---

**Related Documents**:
- `best-practice.md` - Detailed usage recommendations
- `anti-pattern.md` - Common mistakes to avoid
- `checklist.md` - Pre-deployment verification
