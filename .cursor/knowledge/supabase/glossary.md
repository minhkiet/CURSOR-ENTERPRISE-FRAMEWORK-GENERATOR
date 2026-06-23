---
title: "Supabase Glossary"
description: "Từ điển thuật ngữ chuyên ngành Supabase và PostgreSQL"
tags: ["supabase", "glossary", "postgresql", "terms", "definitions"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Supabase Glossary

## Overview

Tài liệu này cung cấp comprehensive glossary của các thuật ngữ chuyên ngành được sử dụng trong Supabase ecosystem. Understanding these terms là essential cho effective Supabase development và communication within teams.

Các thuật ngữ được organize theo categories để facilitate quick reference. Technical terms được giải thích với context về how they apply specifically to Supabase environment.

This glossary serves as a reference guide cho developers at all levels, từ beginners learning Supabase basics đến experienced architects making advanced design decisions.

## Purpose

Mục đích chính của glossary này là:

1. **Standardize Terminology**: Provide consistent definitions cho team communication
2. **Onboarding Support**: Help new team members understand Supabase concepts
3. **Quick Reference**: Enable quick lookup của unfamiliar terms
4. **Documentation Clarity**: Ensure clear communication trong technical documentation

## A

### API Key

A unique identifier used to authenticate requests to Supabase services. Supabase uses two types of API keys:

**Anon Key**: Public key used in client-side code. Has same permissions as an unauthenticated user. Access is controlled by RLS policies.

**Service Role Key**: Private key that bypasses RLS entirely. Should only be used in server-side code or Edge Functions. Never expose in client applications.

```typescript
// Client-side: Use anon key
const supabase = createClient(url, anonKey);

// Server-side: Use service role key
const supabaseAdmin = createClient(url, serviceRoleKey);
```

### Auth

Authentication system provided by Supabase. Supports multiple authentication methods:

- **Email/Password**: Traditional email and password authentication
- **OAuth**: Social login with providers like Google, GitHub, Facebook
- **Magic Links**: Passwordless authentication via email links
- **Phone/SMS**: Phone number authentication with OTP codes

### Auto-Generated API

REST API automatically created by PostgREST from PostgreSQL schema. Provides CRUD operations for all tables and views without manual API development.

```
GET    /posts           → List all posts
POST   /posts           → Create a post
GET    /posts?id=eq.1   → Get post with id=1
PATCH  /posts?id=eq.1   → Update post with id=1
DELETE /posts?id=eq.1   → Delete post with id=1
```

## B

### Backend-as-a-Service (BaaS)

A cloud service model that provides backend infrastructure components (database, authentication, storage, functions) without requiring developers to build and manage their own backend servers.

Supabase is an open-source BaaS built on PostgreSQL, offering an alternative to proprietary services like Firebase.

### Bucket

Container for storing files in Supabase Storage. Analogous to folders in traditional file systems or S3 buckets.

**Public Buckets**: Files accessible without authentication via public URLs.

**Private Buckets**: Files require authentication and signed URLs for access.

```sql
-- Create a public bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('images', 'images', true);

-- Create a private bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('documents', 'documents', false);
```

### Bulk Operations

Operations that process multiple records in a single database request. Supabase supports bulk inserts, updates, and deletes through PostgREST.

```typescript
// Bulk insert
const { data } = await supabase.from('users').insert([
    { name: 'User 1', email: 'user1@example.com' },
    { name: 'User 2', email: 'user2@example.com' },
    { name: 'User 3', email: 'user3@example.com' }
]).select();
```

## C

### CORS (Cross-Origin Resource Sharing)

Security mechanism that controls how web pages from one origin can request resources from another origin. Supabase Edge Functions and API require proper CORS configuration.

```typescript
const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
    'Access-Control-Allow-Methods': 'GET, POST, PATCH, DELETE'
};

Deno.serve(async (req) => {
    if (req.method === 'OPTIONS') {
        return new Response(null, { headers: corsHeaders });
    }
    // Handle request...
});
```

### Connection Pooling

Technique to manage multiple database connections efficiently. Supabase uses PgBouncer to pool connections between clients and PostgreSQL.

**Transaction Mode**: Connections are acquired only during transactions. Recommended for HTTP request/response patterns.

**Session Mode**: Connections persist for entire session. Required for features like prepared statements.

### CRUD

Create, Read, Update, Delete - four basic database operations. Supabase provides auto-generated CRUD endpoints through PostgREST.

```typescript
// Create
await supabase.from('posts').insert({ title: 'New Post' });

// Read
const { data } = await supabase.from('posts').select('*');

// Update
await supabase.from('posts').update({ title: 'Updated' }).eq('id', 1);

// Delete
await supabase.from('posts').delete().eq('id', 1);
```

### Cursor-Based Pagination

Pagination method using cursor (usually timestamp or ID) to paginate through large datasets. More efficient than offset-based pagination for large tables.

```typescript
const { data, error } = await supabase
    .from('posts')
    .select('id, title, created_at')
    .order('created_at', { ascending: false })
    .range(0, 19); // First page

// Next page using last item's timestamp as cursor
const { data, error } = await supabase
    .from('posts')
    .select('id, title, created_at')
    .order('created_at', { ascending: false })
    .lt('created_at', lastTimestamp) // cursor
    .range(0, 19);
```

## D

### Deno

JavaScript/TypeScript runtime used by Supabase Edge Functions. Differs from Node.js in several ways:

- Native TypeScript support without build step
- Permission-based security model
- Standard library available without npm
- ES modules by default

```typescript
// Deno import
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'jsr:@supabase/supabase-js@2';
```

### Edge Functions

Serverless TypeScript functions deployed to edge locations. Run in Deno runtime with access to Supabase services.

**Use Cases**:
- Complex business logic requiring server-side execution
- Third-party API integrations
- Processing that requires service role permissions
- Webhook handlers

```typescript
Deno.serve(async (req) => {
    const { data } = await supabaseAdmin.from('table').select('*');
    return new Response(JSON.stringify(data));
});
```

## E

### Embedding (Table)

PostgREST feature to automatically include related data from foreign key relationships in a single query.

```typescript
// Without embedding: Two queries
const posts = await supabase.from('posts').select('*');
const users = await supabase.from('users').select('*');

// With embedding: Single query with related data
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
            content
        )
    `);
```

### Embedding (Vector)

Mathematical representation of data (text, images) as arrays of numbers. Used for similarity search and AI applications. Supabase supports vector embeddings via pgvector extension.

```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    content TEXT,
    embedding vector(1536)
);
```

## F

### Foreign Key

Database constraint that establishes a link between two tables. Ensures referential integrity and enables table relationships.

```sql
CREATE TABLE posts (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL
);
```

**CASCADE**: When referenced row is deleted, related rows are also deleted.

**SET NULL**: When referenced row is deleted, foreign key is set to NULL.

**RESTRICT**: Prevents deletion of referenced row if related rows exist.

### Full-Text Search

Search technique using natural language processing to match text queries. PostgreSQL provides built-in full-text search with `tsvector` and `tsquery`.

```sql
-- Add full-text search index
CREATE INDEX idx_posts_fts ON posts USING gin(to_tsvector('english', title || ' ' || content));

-- Search query
SELECT * FROM posts
WHERE to_tsvector('english', title || ' ' || content) @@ plainto_tsquery('english', 'search terms');
```

## G

### GoTrue

Authentication server developed by Netlify and integrated into Supabase. Handles user authentication, session management, and OAuth flows.

**Features**:
- User signup and login
- JWT token generation
- OAuth provider integration
- Password reset flows
- Session management

### GraphQL Alternative

PostgREST provides RESTful API that can be considered a GraphQL alternative for simple to moderate complexity data fetching. For complex nested queries, some developers combine PostgREST with tools like Hasura.

Supabase also supports GraphQL through third-party solutions like PostGraphile.

## H

### Helper Function

Pre-built utility functions in Supabase client libraries for common operations.

```typescript
// Auth helper
const { data: { user } } = await supabase.auth.getUser();

// Storage helper
const { data } = supabase.storage.from('bucket').getPublicUrl('file.jpg');
```

## I

### Index

Database structure that improves query speed. Indexes on frequently queried columns significantly reduce query execution time.

```sql
-- Single column index
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Composite index for combined filters
CREATE INDEX idx_posts_user_status ON posts(user_id, status);

-- Partial index for specific conditions
CREATE INDEX idx_posts_published ON posts(created_at) WHERE status = 'published';

-- Full-text search index
CREATE INDEX idx_posts_fts ON posts USING gin(to_tsvector('english', title));
```

**Index Types**:
- **B-tree**: Default, good for equality and range queries
- **Hash**: Fast equality lookups
- **GIN**: Good for arrays and full-text search
- **GiST**: Range types and geometric data
- **BRIN**: Efficient for naturally ordered data

### Interpolation

String interpolation in PostgREST filters using values to build dynamic queries.

```typescript
// Using filter with value
await supabase.from('posts').select('*').eq('status', 'published');

// Using filter with interpolation
const status = 'published';
await supabase.from('posts').select('*').eq('status', status);
```

## J

### JWT (JSON Web Token)

Standard format for securely transmitting information as JSON. Supabase uses JWTs for authentication and authorization.

**Structure**: Header, Payload, Signature

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user-uuid",
    "email": "user@example.com",
    "iat": 1700000000,
    "exp": 1700003600
  },
  "signature": "..."
}
```

**Claims**:
- `sub`: Subject (user ID)
- `iat`: Issued at timestamp
- `exp`: Expiration timestamp
- `email`: User's email
- `role`: Authentication role

## K

### Key

See **API Key**

## L

### Listener (Realtime)

Component that subscribes to database changes. Realtime listeners watch PostgreSQL WAL for changes and broadcast them to connected clients.

```typescript
const channel = supabase
    .channel('db-changes')
    .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'messages'
    }, handleChange)
    .subscribe();
```

### Local Development

Supabase CLI feature allowing local Supabase stack for development without cloud connection.

```bash
# Start local Supabase
supabase start

# Stop local Supabase
supabase stop

# Reset local database
supabase db reset

# Push migrations
supabase db push
```

## M

### Migration

Version-controlled database schema changes. Migrations ensure consistent database structure across environments.

```sql
-- migrations/001_create_users.sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- migrations/001_create_users_down.sql
DROP TABLE IF EXISTS users;
```

```bash
# Apply migrations
supabase db push

# Create new migration
supabase migration new add_phone_column
```

### Multi-Tenancy

Architecture pattern where single application serves multiple customers (tenants) while maintaining data isolation.

```sql
-- Tenant-scoped tables
CREATE TABLE tenant_data (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    data JSONB
);

-- RLS policy for tenant isolation
CREATE POLICY "Tenant isolation"
    ON tenant_data FOR ALL
    USING (tenant_id IN (
        SELECT tenant_id FROM tenant_members WHERE user_id = auth.uid()
    ));
```

## N

### Notification

Realtime message sent to connected clients about database changes. Triggered by INSERT, UPDATE, DELETE operations on subscribed tables.

```typescript
supabase
    .channel('posts')
    .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'posts'
    }, (payload) => {
        console.log('New post:', payload.new);
    })
    .subscribe();
```

## O

### OAuth

Open standard for access delegation. Supabase supports OAuth with providers like Google, GitHub, Facebook, Twitter, and more.

```typescript
const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
        redirectTo: 'https://app.example.com/callback'
    }
});
```

### Optimistic UI

Pattern where UI updates before server confirmation, rolling back if operation fails.

```typescript
// Optimistic update
const previousData = data;
setData(updatedData);

const { error } = await supabase.from('table').update(newData).eq('id', id);

if (error) {
    setData(previousData); // Rollback on failure
    showError();
}
```

## P

### Pagination

Breaking large datasets into smaller chunks. PostgREST supports offset-based and cursor-based pagination.

```typescript
// Offset-based (simple but slower for large offsets)
const { data } = await supabase
    .from('posts')
    .select('*')
    .range(0, 9); // First 10 items

// Cursor-based (efficient for large datasets)
const { data } = await supabase
    .from('posts')
    .select('*')
    .order('created_at')
    .lt('created_at', cursor) // cursor from previous page
    .limit(10);
```

### pgBouncer

Connection pooler used by Supabase to manage database connections. Allows many clients to share fewer database connections.

**Pool Modes**:
- **Transaction**: Connections acquired per transaction (recommended)
- **Session**: Connections held for entire session
- **Statement**: Connections released after each statement

### pgvector

PostgreSQL extension for vector storage and similarity search. Enables AI applications like semantic search and recommendation systems.

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE embeddings (
    id UUID PRIMARY KEY,
    content TEXT,
    embedding vector(1536)
);

-- Search for similar embeddings
SELECT * FROM embeddings
ORDER BY embedding <=> query_vector
LIMIT 5;
```

### Policy (RLS)

Row Level Security rule that controls access to table rows. Policies are evaluated based on the authenticated user context.

```sql
-- Allow users to read their own data
CREATE POLICY "User read own"
    ON posts FOR SELECT
    USING (user_id = auth.uid());

-- Allow users to insert their own data
CREATE POLICY "User insert own"
    ON posts FOR INSERT
    WITH CHECK (user_id = auth.uid());
```

### PostgREST

Web server that generates RESTful API from PostgreSQL schema. Core component of Supabase that provides auto-generated CRUD endpoints.

**Features**:
- Auto CRUD endpoints
- Filtering and sorting
- Pagination
- Relationship embedding
- Stored procedure calls
- JWT authentication

### Prepared Statement

Pre-compiled SQL statement that can be executed multiple times with different parameters. Improves performance for repeated queries.

```typescript
// Supabase client uses prepared statements internally
// For database functions
const { data } = await supabase.rpc('get_user_posts', {
    user_id_param: 'user-uuid',
    limit_param: 10
});
```

### Primary Key

Column(s) that uniquely identify each row in a table. Supabase recommends UUID primary keys for global uniqueness.

```sql
CREATE TABLE users (
    -- UUID primary key (recommended)
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Composite primary key
    org_id UUID,
    user_id UUID,
    PRIMARY KEY (org_id, user_id)
);
```

### Public Schema

Default PostgreSQL schema containing user-created tables, functions, and other objects.

```sql
-- Create in public schema (default)
CREATE TABLE public.users (...);

-- Explicit public schema
CREATE TABLE public.users (...);
```

## R

### RLS (Row Level Security)

PostgreSQL feature for row-level access control. RLS policies determine which rows users can see and modify based on their identity.

```sql
-- Enable RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Public posts" ON posts
    FOR SELECT USING (status = 'public');

CREATE POLICY "Owner access" ON posts
    FOR ALL USING (user_id = auth.uid());
```

### RPC (Remote Procedure Call)

Calling a PostgreSQL function via the API. Used for complex operations that can't be expressed as simple CRUD.

```typescript
// Call database function
const { data, error } = await supabase.rpc('function_name', {
    param1: 'value1',
    param2: 123
});
```

### Realtime

Supabase feature for subscribing to database changes via WebSocket connections.

**Components**:
- **postgres_changes**: Subscribe to table INSERT/UPDATE/DELETE
- **broadcast**: Send/receive low-latency messages
- **presence**: Track user online status

```typescript
// Subscribe to changes
const channel = supabase
    .channel('table-changes')
    .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'messages'
    }, handleChange)
    .subscribe();

// Broadcast message
channel.send({
    type: 'broadcast',
    event: 'typing',
    payload: { userId: '123', isTyping: true }
});

// Track presence
channel.track({ userId: '123', onlineAt: new Date() });
```

### Relationships

Database associations between tables defined through foreign keys.

**One-to-One**: Each row in table A corresponds to one row in table B.

**One-to-Many**: Each row in table A can correspond to multiple rows in table B.

**Many-to-Many**: Rows in table A can correspond to multiple rows in table B, and vice versa.

```sql
-- One-to-Many
CREATE TABLE posts (
    user_id UUID REFERENCES users(id)
);

-- Many-to-Many (junction table)
CREATE TABLE post_tags (
    post_id UUID REFERENCES posts(id),
    tag_id UUID REFERENCES tags(id),
    PRIMARY KEY (post_id, tag_id)
);
```

### REST API

Architectural style for web services. Supabase provides REST API through PostgREST for CRUD operations.

```
GET    /posts           → List posts
POST   /posts           → Create post
GET    /posts?id=eq.1   → Get post 1
PATCH  /posts?id=eq.1   → Update post 1
DELETE /posts?id=eq.1   → Delete post 1
```

### Row Level Security

See **RLS**

## S

### Schema

PostgreSQL container for database objects. Also refers to the structure definition of a database.

```sql
-- Public schema (default)
SELECT * FROM public.users;

-- Information schema (metadata)
SELECT * FROM information_schema.tables;

-- Storage schema (Supabase storage)
SELECT * FROM storage.objects;
```

### Security Definer

Function execution context that runs with the permissions of the function creator, not the caller.

```sql
-- SECURITY DEFINER function bypasses RLS
CREATE FUNCTION admin_get_all_users()
RETURNS SETOF users
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
    SELECT * FROM users;
$$;
```

### Service Role Key

API key that bypasses RLS entirely. Used for server-side operations requiring full database access.

```typescript
// Server-side only - never expose in client code
const supabaseAdmin = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_SERVICE_ROLE_KEY
);
```

### Session

Authenticated user context maintained between requests. Includes user information and authentication tokens.

```typescript
// Get current session
const { data: { session } } = await supabase.auth.getSession();

// Listen to auth changes
supabase.auth.onAuthStateChange((event, session) => {
    if (event === 'SIGNED_IN') {
        console.log('User:', session.user);
    }
});
```

### Signed URL

Time-limited URL providing temporary access to private files in storage.

```typescript
const { data, error } = await supabase.storage
    .from('private-bucket')
    .createSignedUrl('document.pdf', 3600); // 1 hour expiry
```

### Soft Delete

Pattern where records are marked as deleted rather than physically removed. Allows recovery and auditing.

```sql
-- Add deleted_at column
ALTER TABLE posts ADD COLUMN deleted_at TIMESTAMPTZ;

-- Soft delete function
CREATE FUNCTION soft_delete_post(post_id UUID)
RETURNS VOID AS $$
    UPDATE posts SET deleted_at = NOW() WHERE id = post_id;
$$ LANGUAGE sql;

-- RLS to hide soft-deleted records
CREATE POLICY "Active posts only"
    ON posts FOR SELECT
    USING (deleted_at IS NULL);
```

### Storage

Supabase service for storing and managing files. Built on S3-compatible storage.

**Operations**:
- Upload files
- Download files
- Generate public URLs
- Create signed URLs for private files
- Image transformations

```typescript
// Upload
await supabase.storage.from('avatars').upload(filePath, file);

// Download
const { data } = await supabase.storage.from('avatars').download(filePath);

// Public URL
const { data } = supabase.storage.from('avatars').getPublicUrl(filePath);
```

### Subscription

Realtime connection to receive database change notifications.

```typescript
const subscription = supabase
    .channel('posts')
    .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'posts'
    }, handleInsert)
    .subscribe();

// Unsubscribe
supabase.removeChannel(subscription);
```

## T

### Table

Primary database object for storing rows of data. Tables have columns with defined data types.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Trigger

Database function that automatically executes in response to certain events on a table.

```sql
-- Update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER posts_updated_at
    BEFORE UPDATE ON posts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

### TypeScript Client

Official Supabase client library for TypeScript/JavaScript applications.

```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Database queries
const { data } = await supabase.from('table').select('*');

// Auth operations
await supabase.auth.signInWithPassword({ email, password });

// Storage operations
await supabase.storage.from('bucket').upload(path, file);

// Realtime subscriptions
supabase.channel('table').on('postgres_changes', {...}).subscribe();
```

## U

### UUID (Universally Unique Identifier)

128-bit identifier that can be generated independently on different systems. Recommended for primary keys in Supabase.

```sql
-- Generate UUID
SELECT gen_random_uuid();

-- UUID as primary key
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid()
);
```

### UPSERT

Insert or update operation that inserts a new row or updates an existing one if a conflict occurs.

```typescript
await supabase.from('users').upsert(
    { id: existingId, name: 'Updated Name' },
    { onConflict: 'id' }
);
```

### auth.uid()

PostgreSQL function that returns the authenticated user's ID. Used in RLS policies to identify the current user.

```sql
-- RLS policy using auth.uid()
CREATE POLICY "User access"
    ON posts FOR SELECT
    USING (user_id = auth.uid());
```

## V

### View

Virtual table defined by a query. Views can simplify complex queries and provide additional security through selective column exposure.

```sql
-- Simple view
CREATE VIEW active_users AS
SELECT id, email, name
FROM users
WHERE deleted_at IS NULL;

-- Join view
CREATE VIEW user_posts AS
SELECT
    u.id AS user_id,
    u.name AS user_name,
    p.id AS post_id,
    p.title AS post_title
FROM users u
LEFT JOIN posts p ON u.id = p.user_id;
```

## W

### WAL (Write-Ahead Log)

PostgreSQL mechanism that records all database changes before they're applied. Used for replication and realtime change detection.

Realtime subscriptions in Supabase read from WAL to detect and broadcast changes to connected clients.

```sql
-- Enable logical replication
ALTER DATABASE postgres SET wal_level = logical;

-- Create publication for realtime
CREATE PUBLICATION supabase_realtime FOR ALL TABLES;
```

## References

1. **PostgreSQL Documentation**
   - https://www.postgresql.org/docs/current/
   - RLS: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
   - Extensions: https://www.postgresql.org/docs/current/external-extensions.html

2. **Supabase Documentation**
   - https://supabase.com/docs
   - Storage: https://supabase.com/docs/guides/storage
   - Realtime: https://supabase.com/docs/guides/realtime

3. **Related Concepts**
   - JWT: https://jwt.io/
   - REST: https://restfulapi.net/
   - pgvector: https://github.com/pgvector/pgvector

---

**Related Documents**:
- `architecture.md` - System architecture
- `best-practice.md` - Usage best practices
- `decision-tree.md` - When to use what
