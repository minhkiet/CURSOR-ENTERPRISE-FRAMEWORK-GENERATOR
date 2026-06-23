# Supabase Architecture - Kiến Trúc Supabase

## Giới thiệu

Tài liệu này mô tả kiến trúc chi tiết của Supabase, các thành phần, cách chúng tương tác, và các best practices để thiết kế hệ thống enterprise.

---

## 1. Tổng Quan Kiến Trúc

### 1.1. Kiến Trúc Tổng Thể

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUPABASE ARCHITECTURE                         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      CLIENT LAYER                            ││
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          ││
│  │  │Web (JS) │ │Mobile   │ │Flutter  │ │React    │          ││
│  │  │SDK      │ │SDK      │ │SDK      │ │Native   │          ││
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘          ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      API GATEWAY                             ││
│  │  ┌─────────────────────────────────────────────────────┐   ││
│  │  │                    Kong API Gateway                   │   ││
│  │  │  - Rate limiting                                      │   ││
│  │  │  - Authentication                                     │   ││
│  │  │  - Request routing                                   │   ││
│  │  └─────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│         ┌────────────────────┼────────────────────┐            │
│         ▼                    ▼                    ▼            │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────────┐  │
│  │  PostgREST  │     │   GoTrue    │     │  Realtime       │  │
│  │  REST API   │     │   Auth API  │     │  WebSocket      │  │
│  └─────────────┘     └─────────────┘     └─────────────────┘  │
│         │                    │                    │            │
│         └────────────────────┼────────────────────┘            │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   POSTGRESQL DATABASE                        ││
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        ││
│  │  │PostgreSQL│ │ pg_net  │ │ pgvector│ │ pg_rls   │        ││
│  │  │ Core    │ │ HTTP    │ │ Vector   │ │ Security │        ││
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘        ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      STORAGE LAYER                          ││
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐                     ││
│  │  │S3/MinIO │ │ CDN     │ │Image    │                      ││
│  │  │Storage  │ │Cloudflare│ │Transform│                      ││
│  │  └─────────┘ └─────────┘ └─────────┘                     ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   EDGE FUNCTIONS                            ││
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐                     ││
│  │  │Deno     │ │Edge     │ │Deno     │                      ││
│  │  │Runtime  │ │Network  │ │Deploy   │                      ││
│  │  └─────────┘ └─────────┘ └─────────┘                     ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 1.2. Data Flow trong Supabase

```
Client Request
      │
      ▼
┌─────────────────────────────────┐
│ 1. Authentication Check          │
│ - Verify JWT token               │
│ - Extract user ID               │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│ 2. Row Level Security (RLS)     │
│ - Check policies                │
│ - Filter rows based on user    │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│ 3. Database Query                │
│ - PostgreSQL executes query    │
│ - Returns filtered results     │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│ 4. Response                     │
│ - Format as JSON              │
│ - Return to client            │
└─────────────────────────────────┘
```

---

## 2. Database Architecture

### 2.1. PostgreSQL Core

```
┌─────────────────────────────────────────────────────────────────┐
│                      POSTGRESQL LAYER                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Connection Pooler                         ││
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        ││
│  │  │ PgBouncer│ │ Pooler  │ │ Session │ │Trans.   │        ││
│  │  │(default)│ │ Modes   │ │ Mode    │ │Mode     │        ││
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘        ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Query Engine                              ││
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ ││
│  │  │ Parser      │ │ Optimizer   │ │ Executor            │ ││
│  │  │ - Syntax    │ │ - Cost-based│ │ - Node execution   │ ││
│  │  │ - Semantic  │ │ - Statistics│ │ - Parallel exec    │ ││
│  │  └─────────────┘ └─────────────┘ └─────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Storage Engine                            ││
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ ││
│  │  │ Heap        │ │ Indexes     │ │ Write-Ahead Log     │ ││
│  │  │ - Row store │ │ - B-tree    │ │ (WAL)              │ ││
│  │  │ - Pages     │ │ - Hash      │ │ - Durability       │ ││
│  │  └─────────────┘ └─────────────┘ └─────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 2.2. Connection Pooling

```typescript
// Supabase Client với custom pool configuration
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  'https://your-project.supabase.co',
  'your-anon-key',
  {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
    },
    db: {
      schema: 'public',
    },
    global: {
      headers: {
        'x-client-info': 'supabase-js/2.0.0',
      },
    },
  }
);

// Connection modes
// Session mode: Mỗi connection per user session
// Transaction mode: Connections reused across requests
// Prepared statement mode: Query plans cached
```

### 2.3. Schema Design Pattern

```sql
-- Recommended schema structure cho Supabase

-- 1. Auth schema (managed by Supabase)
-- Tables: auth.users (managed automatically)

-- 2. Public schema (user data)
CREATE SCHEMA public;
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT USAGE ON SCHEMA public TO anon;
GRANT ALL ON SCHEMA public TO postgres;

-- 3. Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- Full text search
CREATE EXTENSION IF NOT EXISTS "vector";   -- Vector embeddings

-- 4. Tables
CREATE TABLE public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE public.posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content TEXT,
    published BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE public.comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    post_id UUID REFERENCES public.posts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Indexes
CREATE INDEX idx_posts_user_id ON public.posts(user_id);
CREATE INDEX idx_posts_published ON public.posts(published) WHERE published = true;
CREATE INDEX idx_comments_post_id ON public.comments(post_id);
CREATE INDEX idx_comments_user_id ON public.comments(user_id);

-- 6. Enable RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.comments ENABLE ROW LEVEL SECURITY;
```

---

## 3. Authentication Architecture

### 3.1. GoTrue Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      AUTHENTICATION FLOW                          │
│                                                                 │
│  ┌─────────┐         ┌─────────┐         ┌─────────┐          │
│  │ Client  │────────▶│ GoTrue  │────────▶│PostgreSQL│          │
│  │         │◀────────│ (Auth)  │◀────────│  (Users) │          │
│  └─────────┘         └─────────┘         └─────────┘          │
│       │                    │                                    │
│       │ 1. Sign up/Login   │                                    │
│       │───────────────────▶│                                    │
│       │                    │ 2. Create user                     │
│       │                    │──────────────────▶│          │
│       │                    │◀──────────────────│          │
│       │ 3. JWT Token       │                                    │
│       │◀───────────────────│                                    │
│       │                    │                                    │
│       │ 4. API Request     │                                    │
│       │ with JWT           │                                    │
│       └──────────────────────────────────────────────────────────▶│
│                             │                                    │
│                             │ 5. Verify JWT                      │
│                             │ 6. Check RLS                       │
│                             │ 7. Return filtered data            │
│       │◀──────────────────────────────────────────────────────────│
│       │ 8. Filtered Response                                    │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2. JWT Structure

```json
{
  "iss": "supabase",
  "iat": 1704067200,
  "exp": 1704070800,
  "aud": "authenticated",
  "role": "authenticated",
  "sub": "user-uuid-here",
  "email": "user@example.com",
  "app_metadata": {
    "provider": "email",
    "providers": ["email"]
  },
  "user_metadata": {
    "full_name": "John Doe"
  }
}
```

### 3.3. Auth Implementation

```typescript
// Complete auth flow implementation

// 1. Sign up với metadata
const signUp = async (email: string, password: string, fullName: string) => {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        full_name: fullName,
      },
      emailRedirectTo: 'https://yourapp.com/callback',
    },
  });

  if (error) throw error;
  return data;
};

// 2. Sign in
const signIn = async (email: string, password: string) => {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) throw error;
  return data;
};

// 3. OAuth flow
const signInWithGoogle = async () => {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: `${window.location.origin}/auth/callback`,
      scopes: 'email profile', // Optional scopes
    },
  });

  if (error) throw error;
  return data;
};

// 4. Handle OAuth callback
const handleOAuthCallback = async () => {
  const { data, error } = await supabase.auth.getSessionFromUrl({
    storeSession: true, // Auto-save to localStorage
  });

  if (error) throw error;
  return data;
};

// 5. Session management
const { data: { session } } = supabase.auth.getSession();

// 6. Listen to auth changes
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_IN') {
    console.log('User signed in:', session.user);
    // Update global state, redirect, etc.
  }

  if (event === 'SIGNED_OUT') {
    console.log('User signed out');
    // Clear state, redirect to login
  }

  if (event === 'TOKEN_REFRESHED') {
    console.log('Token refreshed:', session.access_token);
  }
});

// 7. Password reset
const resetPassword = async (email: string) => {
  const { data, error } = await supabase.auth.resetPasswordForEmail(email, {
    redirectTo: `${window.location.origin}/reset-password`,
  });
  return { data, error };
};

// 8. Update password (after reset)
const updatePassword = async (newPassword: string) => {
  const { data, error } = await supabase.auth.updateUser({
    password: newPassword,
  });
  return { data, error };
};
```

---

## 4. Realtime Architecture

### 4.1. Realtime Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      REALTIME ARCHITECTURE                       │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     PostgreSQL                              ││
│  │  ┌─────────────────────────────────────────────────────┐   ││
│  │  │ WAL (Write-Ahead Log)                               │   ││
│  │  │ - Captures all changes                              │   ││
│  │  │ - Sequential by default                            │   ││
│  │  └─────────────────────────────────────────────────────┘   ││
│  │         ▲                                                   ││
│  │         │ WAL Logical Replication                           ││
│  └─────────┼───────────────────────────────────────────────────┘│
│            │                                                     │
│            ▼                                                     │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     Realtime Server                          ││
│  │  ┌─────────────────────────────────────────────────────┐   ││
│  │  │ Channel Manager                                     │   ││
│  │  │ - Subscribe/Unsubscribe                            │   ││
│  │  │ - Message routing                                  │   ││
│  │  └─────────────────────────────────────────────────────┘   ││
│  │         ▲                                                   ││
│  │         │                                                   ││
│  │  ┌─────────────────────────────────────────────────────┐   ││
│  │  │ Presence System                                    │   ││
│  │  │ - Track online users                              │   ││
│  │  │ - Broadcast state                                 │   ││
│  │  └─────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────┘│
│            │                                                     │
│            ▼ WebSocket                                           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     Client                                 ││
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           ││
│  │  │ Subscribe   │ │ Listen     │ │ Presence   │           ││
│  │  │ to channel  │ │ for events │ │ tracking   │           ││
│  │  └─────────────┘ └─────────────┘ └─────────────┘           ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 4.2. Realtime Implementation

```typescript
// 1. Enable realtime for table
// In Supabase Dashboard: Table Editor > Enable Realtime
// Or via SQL:
ALTER PUBLICATION supabase_realtime ADD TABLE messages;

// 2. Basic subscription
const subscribeToMessages = () => {
  const channel = supabase
    .channel('messages-channel')
    .on(
      'postgres_changes',
      {
        event: '*',
        schema: 'public',
        table: 'messages',
        filter: 'room_id=eq.123',
      },
      (payload) => {
        handleMessageChange(payload);
      }
    )
    .subscribe((status) => {
      if (status === 'SUBSCRIBED') {
        console.log('Subscribed to messages');
      }
      if (status === 'CHANNEL_ERROR') {
        console.error('Channel error');
      }
      if (status === 'TIMED_OUT') {
        console.error('Connection timed out');
      }
    });

  return () => {
    channel.unsubscribe();
  };
};

// 3. Presence (track online users)
const channelWithPresence = supabase.channel('room-1');

channelWithPresence
  .on('presence', { event: 'sync' }, () => {
    const state = channelWithPresence.presenceState();
    updateOnlineUsers(state);
  })
  .on('presence', { event: 'join' }, ({ key, newPresences }) => {
    console.log('User joined:', key, newPresences);
  })
  .on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
    console.log('User left:', key, leftPresences);
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await channelWithPresence.track({
        user_id: user.id,
        online_at: new Date().toISOString(),
      });
    }
  });

// 4. Broadcast (low-latency messaging)
const broadcastTyping = async () => {
  await supabase.channel('room-1').send({
    type: 'broadcast',
    event: 'typing',
    payload: { user_id: user.id, is_typing: true },
  });
};

// 5. Listen for broadcast
supabase
  .channel('room-1')
  .on('broadcast', { event: 'typing' }, (payload) => {
    if (payload.payload.user_id !== user.id) {
      showTypingIndicator(payload.payload.user_id);
    }
  })
  .subscribe();
```

---

## 5. Storage Architecture

### 5.1. Storage Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      STORAGE ARCHITECTURE                        │
│                                                                 │
│  ┌─────────┐         ┌─────────┐         ┌─────────┐          │
│  │ Client  │────────▶│ Supabase│────────▶│   S3    │          │
│  │         │◀────────│ Storage │◀────────│ Storage │          │
│  └─────────┘         └─────────┘         └─────────┘          │
│       │                   │                                    │
│       │ 1. Upload request│                                    │
│       │──────────────────▶│                                    │
│       │                   │ 2. Generate presigned URL           │
│       │                   │──────────────────▶│          │
│       │                   │◀──────────────────│          │
│       │ 3. Presigned URL │                                    │
│       │◀──────────────────│                                    │
│       │                   │                                    │
│       │ 4. Direct upload to S3                                  │
│       │─────────────────────────────────────────────────────────▶│
│       │                   │                                    │
│       │ 5. Confirm upload│                                    │
│       │──────────────────▶│                                    │
│       │                   │ 6. Verify upload                    │
│       │                   │──────────────────▶│          │
│       │ 7. Success        │                                    │
│       │◀──────────────────│                                    │
│       │                   │                                    │
│       └───────────────────┴─────────────────────────────────────│
│       │                                                            │
│       │ Access via CDN                                            │
│       └────────────────────────────────────────────────────────────▶│
└─────────────────────────────────────────────────────────────────┘
```

### 5.2. Storage Implementation

```typescript
// 1. Create bucket
const createBucket = async () => {
  const { data, error } = await supabase.storage.createBucket('avatars', {
    public: true, // or false for private
    allowedMimeTypes: ['image/png', 'image/jpeg'],
    fileSizeLimit: 1024 * 1024 * 2, // 2MB
  });
  return { data, error };
};

// 2. Upload file
const uploadAvatar = async (userId: string, file: File) => {
  const fileExt = file.name.split('.').pop();
  const filePath = `${userId}/avatar.${fileExt}`;

  const { data, error } = await supabase.storage
    .from('avatars')
    .upload(filePath, file, {
      cacheControl: '3600',
      upsert: true,
    });

  if (error) throw error;

  // Get public URL
  const { data: urlData } = supabase.storage
    .from('avatars')
    .getPublicUrl(filePath);

  return urlData.publicUrl;
};

// 3. Download file
const downloadFile = async (path: string) => {
  const { data, error } = await supabase.storage
    .from('documents')
    .download(path);

  if (error) throw error;
  return data;
};

// 4. List files
const listFiles = async (folderPath: string = '') => {
  const { data, error } = await supabase.storage
    .from('documents')
    .list(folderPath, {
      limit: 100,
      sortBy: { column: 'name', order: 'asc' },
    });

  if (error) throw error;
  return data;
};

// 5. Signed URL for private files
const getSignedUrl = async (path: string) => {
  const { data, error } = await supabase.storage
    .from('private-documents')
    .createSignedUrl(path, 3600); // 1 hour expiry

  if (error) throw error;
  return data.signedUrl;
};

// 6. Move/Rename file
const moveFile = async (fromPath: string, toPath: string) => {
  const { data, error } = await supabase.storage
    .from('documents')
    .move(fromPath, toPath);

  if (error) throw error;
  return data;
};

// 7. Copy file
const copyFile = async (fromPath: string, toPath: string) => {
  const { data, error } = await supabase.storage
    .from('documents')
    .copy(fromPath, toPath);

  if (error) throw error;
  return data;
};
```

---

## 6. Edge Functions Architecture

### 6.1. Edge Function Deployment

```
┌─────────────────────────────────────────────────────────────────┐
│                    EDGE FUNCTIONS ARCHITECTURE                   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     Supabase CLI                             ││
│  │  ┌─────────────────────────────────────────────────────┐   ││
│  │  │ supabase functions deploy function-name              │   ││
│  │  └─────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     Edge Network                             ││
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          ││
│  │  │ Edge 1  │ │ Edge 2  │ │ Edge 3  │ │ Edge N  │          ││
│  │  │ (US)   │ │ (EU)   │ │ (Asia)  │ │ (More)  │          ││
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘          ││
│  │         ▲                                                   ││
│  │         │ Deploy to all edges                               ││
│  │  ┌─────────────────────────────────────────────────────┐   ││
│  │  │                    Deno Runtime                       │   ││
│  │  │  - TypeScript execution                             │   ││
│  │  │  - Secure sandbox                                   │   ││
│  │  │  - Built-in APIs                                    │   ││
│  │  └─────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 6.2. Edge Function Examples

```typescript
// supabase/functions/send-email/index.ts

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    // Get auth header
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
      throw new Error('Missing authorization header');
    }

    // Create Supabase client
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      {
        global: { headers: { Authorization: authHeader } },
      }
    );

    // Verify user
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      throw new Error('Unauthorized');
    }

    // Parse request body
    const { to, subject, content } = await req.json();

    // Process email (using external API)
    // const sendgridResponse = await fetch('https://api.sendgrid.com/v3/mail/send', {
    //   method: 'POST',
    //   headers: {
    //     'Authorization': `Bearer ${Deno.env.get('SENDGRID_API_KEY')}`,
    //     'Content-Type': 'application/json',
    //   },
    //   body: JSON.stringify({
    //     personalizations: [{ to: [{ email: to }] }],
    //     from: { email: 'noreply@yourapp.com' },
    //     subject,
    //     content: [{ type: 'text/html', value: content }],
    //   }),
    // });

    return new Response(
      JSON.stringify({ success: true, message: 'Email sent' }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200,
      }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 400,
      }
    );
  }
});
```

```typescript
// supabase/functions/generate-pdf/index.ts

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  try {
    const authHeader = req.headers.get('Authorization');
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      { global: { headers: { Authorization: authHeader } } }
    );

    const { report_id } = await req.json();

    // Fetch report data
    const { data: report, error } = await supabase
      .from('reports')
      .select('*')
      .eq('id', report_id)
      .single();

    if (error || !report) {
      throw new Error('Report not found');
    }

    // Generate PDF (simplified - use a real PDF library)
    const pdfContent = generatePDFHTML(report);

    return new Response(pdfContent, {
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename="report-${report_id}.pdf"`,
      },
    });
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500 }
    );
  }
});
```

---

## 7. Security Architecture

### 7.1. Security Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                      SECURITY LAYERS                             │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 1. Network Security                                         ││
│  │  - HTTPS/TLS encryption                                    ││
│  │  - Firewall rules                                          ││
│  │  - CDN protection (Cloudflare)                            ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 2. API Gateway Security                                     ││
│  │  - Rate limiting                                            ││
│  │  - API key validation                                       ││
│  │  - CORS configuration                                       ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 3. Authentication (GoTrue)                                   ││
│  │  - JWT token validation                                     ││
│  │  - OAuth provider verification                              ││
│  │  - Session management                                       ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 4. Row Level Security (RLS)                                  ││
│  │  - Per-table policies                                       ││
│  │  - User-based access control                                ││
│  │  - Role-based permissions                                   ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 5. Database Security                                        ││
│  │  - Role permissions                                         ││
│  │  - Schema isolation                                         ││
│  │  - Column-level security (future)                          ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 7.2. RLS Implementation Pattern

```sql
-- Complete RLS setup pattern

-- 1. Create custom roles
CREATE ROLE authenticated_user;
CREATE ROLE admin;
CREATE ROLE moderator;

-- 2. Grant schema access
GRANT USAGE ON SCHEMA public TO authenticated_user;
GRANT ALL ON SCHEMA public TO admin;

-- 3. Grant table access
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.profiles TO authenticated_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.posts TO authenticated_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.comments TO authenticated_user;

-- 4. Profiles policies
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Anyone can view profiles
CREATE POLICY "Public profiles are viewable by everyone"
ON public.profiles FOR SELECT
USING (true);

-- Users can insert their own profile
CREATE POLICY "Users can insert their own profile"
ON public.profiles FOR INSERT
WITH CHECK (auth.uid() = id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile"
ON public.profiles FOR UPDATE
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);

-- 5. Posts policies
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;

-- Published posts are public
CREATE POLICY "Published posts are viewable by everyone"
ON public.posts FOR SELECT
USING (published = true OR auth.uid() = user_id);

-- Users can insert their own posts
CREATE POLICY "Users can insert their own posts"
ON public.posts FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can update their own posts
CREATE POLICY "Users can update own posts"
ON public.posts FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Users can delete their own posts
CREATE POLICY "Users can delete own posts"
ON public.posts FOR DELETE
USING (auth.uid() = user_id);

-- 6. Comments policies
ALTER TABLE public.comments ENABLE ROW LEVEL SECURITY;

-- Users can view comments on published posts
CREATE POLICY "Comments are viewable by everyone"
ON public.comments FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM public.posts
    WHERE posts.id = comments.post_id
    AND (posts.published = true OR posts.user_id = auth.uid())
  )
);

-- Users can insert their own comments
CREATE POLICY "Users can insert their own comments"
ON public.comments FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can update their own comments
CREATE POLICY "Users can update own comments"
ON public.comments FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Users can delete their own comments
CREATE POLICY "Users can delete own comments"
ON public.comments FOR DELETE
USING (auth.uid() = user_id);

-- 7. Admin bypass for RLS
GRANT ALL ON public.profiles TO admin;
GRANT ALL ON public.posts TO admin;
GRANT ALL ON public.comments TO admin;

-- Admin has bypass RLS (applies to service_role key only!)
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.comments ENABLE ROW LEVEL SECURITY;

-- Note: Service role bypasses RLS automatically
-- Use only server-side, never expose in client code
```

---

## 8. Monitoring và Logging

### 8.1. Logging Architecture

```typescript
// Edge function with structured logging

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

interface LogEntry {
  timestamp: string;
  level: 'info' | 'warn' | 'error';
  message: string;
  userId?: string;
  requestId?: string;
  metadata?: Record<string, unknown>;
}

const log = (entry: LogEntry) => {
  const logLine = JSON.stringify({
    ...entry,
    timestamp: new Date().toISOString(),
  });
  console.log(logLine);
};

serve(async (req) => {
  const requestId = crypto.randomUUID();

  try {
    log({
      level: 'info',
      message: 'Request received',
      requestId,
    });

    // Process request
    // ...

    log({
      level: 'info',
      message: 'Request completed',
      requestId,
    });

    return new Response(JSON.stringify({ success: true }), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    log({
      level: 'error',
      message: error.message,
      requestId,
    });

    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
});
```

### 8.2. Database Logging

```sql
-- Enable query logging
ALTER DATABASE postgres SET log_statement = 'all';
ALTER DATABASE postgres SET log_min_duration_statement = 1000;

-- View recent queries
SELECT 
    now() - query_start AS duration,
    usename,
    query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY query_start;

-- View slow queries
SELECT 
    query,
    calls,
    mean_time,
    total_time,
    rows
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 20;

-- Enable extension first
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

---

## 9. Scalability Patterns

### 9.1. Horizontal Scaling

```
┌─────────────────────────────────────────────────────────────────┐
│                      HORIZONTAL SCALING                          │
│                                                                 │
│                    ┌─────────────┐                              │
│                    │ Load Balancer│                              │
│                    └──────┬──────┘                              │
│                           │                                     │
│         ┌─────────────────┼─────────────────┐                   │
│         │                 │                 │                   │
│         ▼                 ▼                 ▼                   │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐          │
│  │ Supabase    │   │ Supabase    │   │ Supabase    │          │
│  │ Instance 1  │   │ Instance 2  │   │ Instance 3  │          │
│  │             │   │             │   │             │          │
│  │ ┌─────────┐ │   │ ┌─────────┐ │   │ ┌─────────┐ │          │
│  │ │PostgreSQL│ │   │ │PostgreSQL│ │   │ │PostgreSQL│ │          │
│  │ │Primary   │ │   │ │Read Replica│ │   │ │Read Replica│ │          │
│  │ └─────────┘ │   │ └─────────┘ │   │ └─────────┘ │          │
│  └─────────────┘   └─────────────┘   └─────────────┘          │
│         │                 │                 │                   │
│         └─────────────────┼─────────────────┘                   │
│                           │                                     │
│                           ▼                                     │
│                    ┌─────────────┐                              │
│                    │   Shared    │                              │
│                    │   Storage   │                              │
│                    │   (S3)      │                              │
│                    └─────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2. Read Replica Configuration

```typescript
// Configure read replica client
import { createClient } from '@supabase/supabase-js';

// Main client (writes)
const supabase = createClient(
  'https://your-project.supabase.co',
  'your-anon-key'
);

// Read replica client (reads)
const supabaseReadOnly = createClient(
  'https://your-read-replica.supabase.co', // Different URL
  'your-anon-key'
);

// Use read replica for read-heavy operations
const fetchPosts = async () => {
  const { data } = await supabaseReadOnly
    .from('posts')
    .select('*')
    .eq('published', true);
  return data;
};

// Use main client for writes
const createPost = async (post: NewPost) => {
  const { data } = await supabase
    .from('posts')
    .insert(post)
    .select()
    .single();
  return data;
};
```
