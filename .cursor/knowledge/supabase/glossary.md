# Supabase Glossary - Từ Điển Thuật Ngữ

## Giới thiệu

Tài liệu này cung cấp định nghĩa chi tiết cho các thuật ngữ quan trọng liên quan đến Supabase, được sử dụng trong Cursor Enterprise Framework.

---

## Danh Sách Thuật Ngữ

### 1. Supabase

**Định nghĩa:** Supabase là một open-source alternative cho Firebase, cung cấp database (PostgreSQL), authentication, realtime subscriptions, storage, và các API tự động. Được xây dựng trên PostgreSQL với nhiều tính năng bổ sung.

**Đặc điểm chính:**
- Database: PostgreSQL với RESTful API và Realtime
- Authentication: Email/password, OAuth providers, Magic links
- Storage: File storage và CDN
- Edge Functions: Serverless functions
- Realtime: WebSocket subscriptions
- Dashboard: Web UI để quản lý

** Ví dụ:**
```typescript
// Supabase Client Setup
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  'https://your-project.supabase.co',
  'your-anon-key'
);

// Query data
const { data, error } = await supabase
  .from('posts')
  .select('*')
  .eq('published', true);
```

---

### 2. PostgreSQL

**Định nghĩa:** Supabase sử dụng PostgreSQL làm database engine. PostgreSQL là một advanced, open-source relational database system nổi tiếng với reliability, feature robustness, và performance.

**Các tính năng PostgreSQL mà Supabase kế thừa:**
- ACID compliance
- Complex queries (JOINs, subqueries, window functions)
- Full-text search
- JSON support (JSONB)
- PostGIS (geospatial)
- Row-level security (RLS)
- Array types
- Custom data types

** Ví dụ:**
```sql
-- PostgreSQL query trong Supabase
SELECT 
    u.name,
    COUNT(p.id) as post_count,
    json_agg(p.title) as recent_titles
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.created_at > NOW() - INTERVAL '30 days'
GROUP BY u.id, u.name
HAVING COUNT(p.id) > 5
ORDER BY post_count DESC;
```

---

### 3. Row Level Security (RLS)

**Định nghĩa:** RLS là cơ chế bảo mật của PostgreSQL cho phép kiểm soát truy cập ở cấp độ row. Supabase sử dụng RLS để bảo mật API và đảm bảo users chỉ truy cập được data của họ.

**Hoạt động:**
- Mỗi table có thể có policies
- Policies kiểm tra conditions trước khi SELECT/INSERT/UPDATE/DELETE
- Policies sử dụng current_user() hoặc auth.uid()

** Ví dụ:**
```sql
-- Enable RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Policy cho phép user chỉ đọc profile của chính họ
CREATE POLICY "Users can view own profile"
ON profiles FOR SELECT
USING (auth.uid() = user_id);

-- Policy cho phép user chỉ update profile của chính họ
CREATE POLICY "Users can update own profile"
ON profiles FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
```

---

### 4. Authentication

**Định nghĩa:** Supabase Auth cung cấp multiple authentication methods để xác thực users. Hỗ trợ email/password, OAuth providers, magic links, và phone authentication.

**Các providers được hỗ trợ:**
- Email/Password
- Magic Link
- OAuth Providers:
  - Google
  - GitHub
  - Facebook
  - Twitter/X
  - Apple
  - Microsoft/Azure AD
  - Discord
  - And 20+ more

** Ví dụ:**
```typescript
// Sign up với email/password
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'secure-password',
  options: {
    data: {
      full_name: 'John Doe'
    }
  }
});

// Sign in với OAuth (Google)
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: 'https://yourapp.com/callback'
  }
});

// Sign in với magic link
const { data, error } = await supabase.auth.signInWithOtp({
  email: 'user@example.com'
});
```

---

### 5. Realtime Subscriptions

**Định nghĩa:** Supabase Realtime cho phép ứng dụng subscribe vào changes trong database thông qua WebSockets. Khi có thay đổi (INSERT, UPDATE, DELETE), Supabase push notification đến subscribed clients.

**Các loại realtime events:**
- `INSERT`: Khi có row mới được thêm
- `UPDATE`: Khi row được cập nhật
- `DELETE`: Khi row được xóa
- `*:`: Tất cả các events

** Ví dụ:**
```typescript
// Subscribe to changes on a table
const channel = supabase
  .channel('schema-db-changes')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'messages'
    },
    (payload) => {
      console.log('Change received!', payload);
    }
  )
  .subscribe();

// Subscribe to filtered changes (only new messages for a room)
const channel = supabase
  .channel('room-messages')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'messages',
      filter: 'room_id=eq.123'
    },
    (payload) => {
      addNewMessage(payload.new);
    }
  )
  .subscribe();

// Unsubscribe when done
channel.unsubscribe();
```

---

### 6. Storage

**Định nghĩa:** Supabase Storage cung cấp file storage với CDN integration. Cho phép upload/download files, images, videos, và các loại content khác. Storage được tổ chức theo buckets và folders.

**Các tính năng:**
- Public và private buckets
- Image transformations
- Signed URLs cho temporary access
- Progress tracking cho uploads
- Multiple storage providers

** Ví dụ:**
```typescript
// Upload file
const { data, error } = await supabase.storage
  .from('avatars')
  .upload('public/avatar1.jpg', fileBuffer, {
    cacheControl: '3600',
    upsert: false
  });

// Download file
const { data, error } = await supabase.storage
  .from('avatars')
  .download('public/avatar1.jpg');

// Get public URL
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('public/avatar1.jpg');

// Create signed URL for private files
const { data, error } = await supabase.storage
  .from('documents')
  .createSignedUrl('private/report.pdf', 3600);

// Delete file
const { error } = await supabase.storage
  .from('avatars')
  .remove(['public/avatar1.jpg']);
```

---

### 7. Edge Functions

**Định nghĩa:** Supabase Edge Functions là serverless functions được deploy và chạy trên edge locations sử dụng Deno runtime. Cho phép thực thi code phía server mà không cần quản lý server.

**Đặc điểm:**
- Deno runtime (TypeScript/JavaScript)
- Edge deployment (gần users)
- Request/Response handling
- Database access
- Environment variables
- JWT verification built-in

** Ví dụ:**
```typescript
// supabase/functions/send-email/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  try {
    const { email, subject, content } = await req.json();
    
    // Verify JWT
    const authHeader = req.headers.get('Authorization');
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      { global: { headers: { Authorization: authHeader } } }
    );
    
    // Send email logic here
    // ...
    
    return new Response(
      JSON.stringify({ success: true }),
      { headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
});
```

---

### 8. PostgREST

**Định nghĩa:** PostgREST là RESTful API server tự động được tạo từ PostgreSQL schema. Supabase sử dụng PostgREST để cung cấp instant REST APIs cho database tables và views.

**Tính năng:**
- CRUD operations
- Filtering và pagination
- Ordering
- Column selection
- Relationship navigation (embed)
- Function calls
- RPC (Stored procedures)

** Ví dụ:**
```typescript
// Auto-generated REST API
// GET /rest/v1/posts?select=*,author:users(name)
// POST /rest/v1/posts
// PATCH /rest/v1/posts?id=eq.123
// DELETE /rest/v1/posts?id=eq.123

// Using Supabase client (wraps PostgREST)
const { data, error } = await supabase
  .from('posts')
  .select(`
    *,
    author:users!inner(
      id,
      name,
      avatar_url
    ),
    comments(
      id,
      content
    )
  `)
  .eq('published', true)
  .order('created_at', { ascending: false })
  .range(0, 9);
```

---

### 9. GoTrue

**Định nghĩa:** GoTrue là authentication server của Supabase (được fork từ Netlify Identity). Cung cấp JWT-based authentication với user management.

**Hoạt động:**
- Tạo và verify JWT tokens
- User registration và login
- Password reset
- Session management
- OAuth token exchange

** Ví dụ:**
```typescript
// Get current session
const { data: { session } } = await supabase.auth.getSession();

// Get current user
const { data: { user } } = await supabase.auth.getUser();

// Update user metadata
const { data, error } = await supabase.auth.updateUser({
  data: { full_name: 'Jane Doe' }
});

// Sign out
await supabase.auth.signOut();

// Listen to auth state changes
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_IN') {
    console.log('Signed in:', session.user);
  } else if (event === 'SIGNED_OUT') {
    console.log('Signed out');
  }
});
```

---

### 10. Foreign Data Wrappers (FDW)

**Định nghĩa:** Supabase cho phép kết nối đến các data sources bên ngoài như MongoDB, MySQL, Salesforce thông qua Foreign Data Wrappers.

**Các FDW được hỗ trợ:**
- postgres_fdw (PostgreSQL to PostgreSQL)
- mysql_fdw (PostgreSQL to MySQL)
- mongo_fdw (PostgreSQL to MongoDB)
- Multicorn (Multiple data sources)

** Ví dụ:**
```sql
-- Tạo foreign server cho MySQL database
CREATE EXTENSION mysql_fdw;

CREATE SERVER mysql_server
FOREIGN DATA WRAPPER mysql_fdw
OPTIONS (host 'mysql.example.com', port '3306');

CREATE USER MAPPING FOR current_user
SERVER mysql_server
OPTIONS (username 'remote_user', password 'password');

-- Import foreign schema
IMPORT FOREIGN SCHEMA remote_database
FROM SERVER mysql_server
INTO public;
```

---

### 11. pg_net

**Định nghĩa:** pg_net là extension cho phép Supabase functions gọi external HTTP requests một cách async. Cần thiết cho việc integrate với external APIs.

**Hoạt động:**
- Non-blocking HTTP requests từ database
- Retry logic tích hợp
- Response handling

** Ví dụ:**
```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS pg_net;

-- Make async HTTP request
SELECT net.http_post(
    url := 'https://api.example.com/webhook',
    headers := '{"Content-Type": "application/json"}'::jsonb,
    body := '{"event": "user_signup", "user_id": "' || NEW.id || '"}'::jsonb
);
```

---

### 12. Supabase CLI

**Định nghĩa:** Supabase CLI là command-line tool để phát triển local với Supabase. Cho phép start local Supabase stack, run migrations, và deploy.

**Các commands chính:**
```bash
# Start local Supabase
supabase init
supabase start

# Link to remote project
supabase link --project-ref your-project-ref

# Pull remote schema
supabase db pull

# Push local changes
supabase db push

# Generate types
supabase gen types typescript

# Deploy edge functions
supabase functions deploy function-name

# Status
supabase status
```

---

### 13. Database Migration

**Định nghĩa:** Migrations là cách để version control database schema. Supabase hỗ trợ migrations qua Supabase CLI và có thể track qua git.

**Cấu trúc migration file:**
```
supabase/migrations/
  20240101000000_create_users_table.sql
  20240102000000_create_posts_table.sql
  20240103000000_add_rls_policies.sql
```

** Ví dụ migration:**
```sql
-- migrations/20240101000000_create_users_table.sql

CREATE TABLE public.profiles (
    id UUID REFERENCES auth.users NOT NULL PRIMARY KEY,
    email TEXT,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Create policy
CREATE POLICY "Users can view own profile"
ON public.profiles FOR SELECT
USING (auth.uid() = id);

-- Trigger để auto-create profile
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email)
    VALUES (NEW.id, NEW.email);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
AFTER INSERT ON auth.users
FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

---

### 14. Supabase Dashboard

**Định nghĩa:** Supabase Dashboard là web-based UI để quản lý Supabase project. Cung cấp visual editor cho database, table editor, authentication management, và nhiều hơn nữa.

**Các tabs chính:**
- **Table Editor**: Visual table editor
- **SQL Editor**: Run SQL queries
- **Authentication**: Manage users và providers
- **Storage**: Manage buckets và files
- **Functions**: Deploy và monitor edge functions
- **Logs**: View API và function logs
- **Database**: Settings và connection info

---

### 15. Embed and Include

**Định nghĩa:** Supabase hỗ trợ embedding related data từ các bảng khác sử dụng JOIN syntax trong query. Tương tự như eager loading trong ORMs.

** Ví dụ:**
```typescript
// Single relationship (has_one)
const { data: post } = await supabase
  .from('posts')
  .select(`
    *,
    author:users!posts.user_id (
      id,
      name,
      avatar_url
    )
  `)
  .eq('id', 123)
  .single();

// Multiple relationships (has_many)
const { data: user } = await supabase
  .from('users')
  .select(`
    *,
    posts (
      id,
      title
    ),
    comments (
      id,
      content
    )
  `)
  .eq('id', 456)
  .single();

// Foreign key constraints cần được set đúng
```

---

### 16. RPC (Remote Procedure Call)

**Định nghĩa:** RPC cho phép gọi stored procedures/functions trong database từ client. Supabase hỗ trợ RPC thông qua `.rpc()` method.

** Ví dụ:**
```typescript
// Define function in database
// migrations/20240101000000_create_functions.sql
CREATE OR REPLACE FUNCTION get_user_stats(user_id UUID)
RETURNS TABLE (
    post_count BIGINT,
    comment_count BIGINT,
    total_likes BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(DISTINCT p.id)::BIGINT,
        COUNT(DISTINCT c.id)::BIGINT,
        COALESCE(SUM(l.count), 0)::BIGINT
    FROM users u
    LEFT JOIN posts p ON p.user_id = u.id
    LEFT JOIN comments c ON c.user_id = u.id
    LEFT JOIN likes l ON l.post_id = p.id
    WHERE u.id = get_user_stats.user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

// Call from client
const { data, error } = await supabase.rpc('get_user_stats', {
  user_id: 'user-uuid-here'
});
```

---

### 17. Vault

**Định nghĩa:** Supabase Vault là extension cho phép lưu trữ secrets và sensitive data trong database một cách an toàn. Được mã hóa bằng encryption keys.

** Ví dụ:**
```typescript
// Store a secret
const { data, error } = await supabase.rpc('vault.store_secret', {
  secret_key: 'api_key_stripe',
  secret_value: 'sk_live_xxxxx'
});

// Retrieve a secret
const { data, error } = await supabase.rpc('vault.get_secret', {
  secret_key: 'api_key_stripe'
});

// The secret is decrypted automatically
```

---

### 18. Vector Support

**Định nghĩa:** Supabase hỗ trợ vector operations thông qua pg_vector extension, cho phép lưu trữ và tìm kiếm embeddings cho AI/ML applications.

**Các operations:**
- Storage: Lưu trữ vector arrays
- L2 distance: Euclidean distance
- Cosine distance: Similarity measure
- Inner product: Alternative similarity

** Ví dụ:**
```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with vector column
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(1536)
);

-- Create index for fast similarity search
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Insert with embedding
INSERT INTO documents (content, embedding)
VALUES ('Sample text', '[0.1, 0.2, ...]');

-- Search for similar documents
SELECT content, 1 - (embedding <=> '[0.1, 0.2, ...]') as similarity
FROM documents
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 5;
```

---

### 19. Triggers và Functions

**Định nghĩa:** PostgreSQL triggers và functions cho phép tự động hóa business logic ở database level. Supabase cung cấp templates cho common trigger patterns.

** Ví dụ:**
```sql
-- Function để update timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger để auto-update timestamp
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON profiles
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- Function để handle user deletion
CREATE OR REPLACE FUNCTION handle_deleted_user()
RETURNS TRIGGER AS $$
BEGIN
    -- Clean up related data
    DELETE FROM posts WHERE user_id = OLD.id;
    DELETE FROM comments WHERE user_id = OLD.id;
    DELETE FROM profiles WHERE id = OLD.id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_user_deleted
AFTER DELETE ON auth.users
FOR EACH ROW EXECUTE FUNCTION handle_deleted_user();
```

---

### 20. Environment Variables

**Định nghĩa:** Supabase sử dụng environment variables để configure các services. Trong Edge Functions, có thể truy cập qua `Deno.env`.

**Các biến quan trọng:**
```bash
# System environment variables
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJxxx
SUPABASE_SERVICE_ROLE_KEY=eyJxxx
SUPABASE_DB_URL=postgres://postgres:xxx@db.xxx.supabase.co:5432/postgres

# Custom environment variables (Edge Functions)
# Set in Supabase Dashboard > Edge Functions > Secrets
STRIPE_SECRET_KEY=sk_live_xxx
SENDGRID_API_KEY=SG.xxx
```

** Ví dụ trong Edge Function:**
```typescript
Deno.env.get('SUPABASE_URL');
Deno.env.get('SUPABASE_ANON_KEY');
Deno.env.get('STRIPE_SECRET_KEY'); // Custom secret
```
