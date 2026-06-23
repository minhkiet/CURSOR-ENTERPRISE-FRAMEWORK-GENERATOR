# Supabase FAQ - Câu Hỏi Thường Gặp

## Giới thiệu

Tài liệu này trả lời các câu hỏi thường gặp về Supabase, được đặt ra bởi developers trong quá trình làm việc với Cursor Enterprise Framework.

---

## 1. Authentication Questions

### Q1: Làm thế nào để implement multi-factor authentication (MFA)?

**A:** Supabase hỗ trợ MFA thông qua TOTP (Time-based One-Time Password):

```typescript
// Bật MFA cho user
const enableMFA = async (user: User) => {
  // Bước 1: Tạo TOTP factor
  const { data, error } = await supabase.auth.mfa.enroll({
    factorType: 'totp',
    code: await getVerificationCode() // Code từ authenticator app
  });

  if (error) throw error;

  // data.challenge contains the QR code URL
  return {
    qrCode: data.qrCode,
    secret: data.secret,
    factorId: data.id
  };
};

// Xác minh MFA khi đăng nhập
const verifyMFA = async (factorId: string, code: string) => {
  // Bước 1: Challenge
  const { data: challenge, error: challengeError } = await supabase.auth.mfa.challenge({
    factorId
  });

  if (challengeError) throw challengeError;

  // Bước 2: Verify
  const { data, error } = await supabase.auth.mfa.verify({
    factorId,
    challengeId: challenge.id,
    code
  });

  if (error) throw error;
  return data; // Session created
};

// Kiểm tra MFA status của user
const checkMFAStatus = async () => {
  const { data: { user } } = await supabase.auth.getUser();
  
  const factors = user?.factors || [];
  const hasMFA = factors.some(f => f.factor_type === 'totp');
  
  return { hasMFA, factors };
};
```

---

### Q2: Làm thế nào để handle session expiration?

**A:** Có nhiều strategies để handle session expiration:

```typescript
// Strategy 1: Auto-refresh session
const { data: { session } } = supabase.auth.getSession();

// Listen to token refresh events
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'TOKEN_REFRESHED') {
    console.log('Token refreshed:', session.access_token);
    // Update local storage or state
  }

  if (event === 'SIGNED_OUT') {
    console.log('User signed out');
    // Redirect to login
  }
});

// Strategy 2: Manual refresh before expiration
const refreshSession = async () => {
  const { data, error } = await supabase.auth.refreshSession();
  if (error) {
    // Redirect to login
    window.location.href = '/login';
  }
  return data;
};

// Check and refresh if needed
const ensureValidSession = async () => {
  const { data: { session } } = supabase.auth.getSession();
  
  if (!session) {
    window.location.href = '/login';
    return null;
  }

  // Check if token expires soon (less than 5 minutes)
  const expiresAt = session.expires_at;
  const now = Date.now() / 1000;
  const fiveMinutes = 5 * 60;

  if (expiresAt - now < fiveMinutes) {
    await refreshSession();
  }

  return session;
};

// Strategy 3: React hook for auth state
import { useEffect, useState } from 'react';

const useAuth = () => {
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const { data: { session } } = supabase.auth.getSession();
    setSession(session);
    setLoading(false);

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setSession(session);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  return { session, loading, user: session?.user ?? null };
};
```

---

### Q3: Sự khác biệt giữa anon key và service role key là gì?

**A:** 

| Aspect | Anon Key | Service Role Key |
|--------|----------|-----------------|
| RLS | Respects RLS policies | Bypasses RLS |
| Public | Safe to expose in client | NEVER expose |
| Use Case | Client-side | Server-side/admin |
| Permissions | Limited by RLS | Full database access |
| Security | User-scoped | Admin-scoped |

```typescript
// ✅ Client-side: Use anon key (safe)
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY! // Safe to expose
);

// ✅ Server-side: Use service role for admin tasks (NEVER expose)
const supabaseAdmin = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY! // NEVER put in client code!
);

// Ví dụ: Admin function để delete any user
const adminDeleteUser = async (userId: string) => {
  // This bypasses RLS, use carefully
  const { error } = await supabaseAdmin.auth.admin.deleteUser(userId);
  return { error };
};
```

---

## 2. Database Questions

### Q4: Làm thế nào để implement soft delete?

**A:** Có nhiều cách để implement soft delete:

```typescript
// Method 1: is_deleted flag
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    content TEXT,
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS policy: Chỉ hiển thị non-deleted posts
CREATE POLICY "View non-deleted posts"
ON posts FOR SELECT
USING (
    is_deleted = FALSE
    OR auth.uid() IN (
        SELECT id FROM auth.users 
        WHERE raw_user_meta_data->>'role' = 'admin'
    )
);

-- Soft delete function
const softDeletePost = async (postId: string) => {
  const { error } = await supabase
    .from('posts')
    .update({
      is_deleted: true,
      deleted_at: new Date().toISOString()
    })
    .eq('id', postId)
    .eq('user_id', auth.uid()); // Chỉ owner mới delete được

  return { error };
};

// Method 2: Sử dụng deleted_at (cleaner)
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    deleted_at TIMESTAMPTZ DEFAULT NULL
);

-- Null = not deleted, timestamp = deleted
CREATE POLICY "View non-deleted documents"
ON documents FOR SELECT
USING (deleted_at IS NULL);

// Method 3: PostgreSQL temporal tables (most robust)
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name TEXT,
    price DECIMAL,
    valid_from TIMESTAMPTZ DEFAULT NOW(),
    valid_to TIMESTAMPTZ DEFAULT '9999-12-31'
);

ALTER TABLE products ADD COLUMN sys_period TSRANGE
GENERATED ALWAYS AS (TSRANGE(valid_from, valid_to)) STORED;

CREATE TABLE products_history (LIKE products);
ALTER TABLE products_history DROP COLUMN sys_period;

CREATE TRIGGER products_history_trigger
BEFORE UPDATE OR DELETE ON products
FOR EACH ROW EXECUTE
FUNCTION history_snapshot();

-- Enable temporal queries
SET他的话 temporal.las_valid_from = '2024-01-01';
SELECT * FROM products FOR SYSTEM_TIME AS OF NOW();
```

---

### Q5: Làm thế nào để implement full-text search?

**A:** Supabase cung cấp nhiều options cho full-text search:

```typescript
// Method 1: PostgreSQL full-text search (built-in)
-- Enable trgm extension
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Add search index
CREATE INDEX idx_posts_title_trgm ON posts USING gin(title gin_trgm_ops);
CREATE INDEX idx_posts_content_trgm ON posts USING gin(content gin_trgm_ops);

-- Search function
const searchPosts = async (query: string) => {
  const { data, error } = await supabase
    .from('posts')
    .select('*')
    .or(`title.ilike.%${query}%,content.ilike.%${query}%`);

  return { data, error };
};

// Method 2: Full-text search với ranking
-- Tạo search vector
ALTER TABLE posts ADD COLUMN search_vector TSVECTOR;

UPDATE posts SET search_vector = 
    setweight(tovector(title), 'A') || 
    setweight(tovector(content), 'B');

-- Create GIN index
CREATE INDEX idx_posts_search ON posts USING gin(search_vector);

-- Search với ranking
CREATE OR REPLACE FUNCTION search_posts(query TEXT)
RETURNS TABLE (
    id UUID,
    title TEXT,
    content TEXT,
    rank REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        p.title,
        p.content,
        ts_rank(p.search_vector, plainto_tsquery('english', query)) AS rank
    FROM posts p
    WHERE p.search_vector @@ plainto_tsquery('english', query)
    ORDER BY rank DESC;
END;
$$ LANGUAGE plpgsql;

const searchWithRanking = async (query: string) => {
  const { data, error } = await supabase
    .rpc('search_posts', { query });

  return { data, error };
};

// Method 3: Sử dụng Supabase text search
const { data } = await supabase
  .from('posts')
  .select('*')
  .textSearch('title', query, { type: 'websearch' });
```

---

### Q6: Làm thế nào để handle concurrent updates?

**A:** Sử dụng optimistic locking hoặc PostgreSQL features:

```typescript
// Method 1: Version-based optimistic locking
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    content TEXT,
    version INTEGER DEFAULT 1,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Update with version check
const updateDocument = async (id: string, updates: any, expectedVersion: number) => {
  // First, try to update with version check
  const { data, error } = await supabase
    .from('documents')
    .update({
      ...updates,
      version: expectedVersion + 1,
      updated_at: new Date().toISOString()
    })
    .eq('id', id)
    .eq('version', expectedVersion)
    .select()
    .single();

  if (error) {
    if (error.code === 'PGRST116') {
      throw new Error('Document was modified by another user. Please refresh and try again.');
    }
    throw error;
  }

  return data;
};

// Method 2: Row-level locking với SELECT FOR UPDATE
CREATE OR REPLACE FUNCTION reserve_document(doc_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    locked_record RECORD;
BEGIN
    -- Lock the row
    SELECT * INTO locked_record
    FROM documents
    WHERE id = doc_id
    FOR UPDATE NOWAIT;

    RETURN TRUE;
EXCEPTION
    WHEN lock_not_available THEN
        RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

// Method 3: Database trigger for optimistic locking
CREATE OR REPLACE FUNCTION check_document_version()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.version + 1 != NEW.version THEN
        RAISE EXCEPTION 'Version conflict: expected % but got %', OLD.version + 1, NEW.version;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER document_version_check
BEFORE UPDATE ON documents
FOR EACH ROW
EXECUTE FUNCTION check_document_version();
```

---

## 3. Realtime Questions

### Q7: Làm thế nào để handle reconnection trong realtime?

**A:** Implement proper reconnection logic:

```typescript
// Custom hook với reconnection logic
import { useEffect, useRef, useState } from 'react';

const useRealtimeSubscription = (
  table: string,
  filter?: string,
  onChange: (payload: any) => void
) => {
  const [status, setStatus] = useState<'connecting' | 'connected' | 'disconnected'>('disconnected');
  const channelRef = useRef<ReturnType<typeof supabase.channel> | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 10;
  const baseDelay = 1000; // 1 second

  const connect = () => {
    if (channelRef.current) {
      supabase.removeChannel(channelRef.current);
    }

    const channel = supabase
      .channel(`${table}-changes-${Date.now()}`)
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table,
          ...(filter && { filter })
        },
        (payload) => {
          reconnectAttempts.current = 0; // Reset on successful message
          onChange(payload);
        }
      )
      .subscribe((status) => {
        if (status === 'SUBSCRIBED') {
          setStatus('connected');
        } else if (status === 'CLOSED') {
          setStatus('disconnected');
          scheduleReconnect();
        } else if (status === 'CHANNEL_ERROR') {
          setStatus('disconnected');
          scheduleReconnect();
        }
      });

    channelRef.current = channel;
  };

  const scheduleReconnect = () => {
    if (reconnectAttempts.current >= maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    // Exponential backoff
    const delay = baseDelay * Math.pow(2, reconnectAttempts.current);
    const jitter = Math.random() * 1000;
    const totalDelay = Math.min(delay + jitter, 30000);

    reconnectTimeoutRef.current = setTimeout(() => {
      reconnectAttempts.current++;
      setStatus('connecting');
      connect();
    }, totalDelay);
  };

  useEffect(() => {
    setStatus('connecting');
    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (channelRef.current) {
        supabase.removeChannel(channelRef.current);
      }
    };
  }, [table, filter]);

  return { status };
};

// Usage
const MessagesList = ({ roomId }: { roomId: string }) => {
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    // Fetch initial messages
    fetchInitialMessages(roomId);
  }, [roomId]);

  const { status } = useRealtimeSubscription(
    'messages',
    `room_id=eq.${roomId}`,
    (payload) => {
      if (payload.eventType === 'INSERT') {
        setMessages(prev => [...prev, payload.new]);
      } else if (payload.eventType === 'UPDATE') {
        setMessages(prev => 
          prev.map(m => m.id === payload.new.id ? payload.new : m)
        );
      } else if (payload.eventType === 'DELETE') {
        setMessages(prev => prev.filter(m => m.id !== payload.old.id));
      }
    }
  );

  return (
    <div>
      <div>Connection status: {status}</div>
      {messages.map(msg => (
        <Message key={msg.id} {...msg} />
      ))}
    </div>
  );
};
```

---

### Q8: Sự khác biệt giữa postgres_changes và broadcast/presence là gì?

**A:**

| Feature | postgres_changes | Broadcast | Presence |
|---------|------------------|-----------|----------|
| Purpose | Database changes | Direct messaging | Online status |
| Source | PostgreSQL WAL | Client-to-client | Client-to-client |
| Persistence | Stored in DB | Ephemeral | Ephemeral |
| Use case | Sync database state | Typing indicators, cursors | Online users |
| Filters | Yes (where clauses) | No | No |

```typescript
// postgres_changes: Database sync
const channel1 = supabase
  .channel('db-changes')
  .on('postgres_changes', {
    event: 'INSERT',
    schema: 'public',
    table: 'messages',
    filter: 'room_id=eq.123'
  }, (payload) => {
    // New message inserted
  })
  .subscribe();

// broadcast: Direct messaging (no DB)
const channel2 = supabase
  .channel('typing')
  .on('broadcast', { event: 'typing' }, ({ payload }) => {
    // payload: { user_id: '123', is_typing: true }
  })
  .subscribe();

// Send typing indicator
const sendTyping = async () => {
  await channel2.send({
    type: 'broadcast',
    event: 'typing',
    payload: { user_id: currentUser.id, is_typing: true }
  });
};

// presence: Track online status
const channel3 = supabase
  .channel('online-users')
  .on('presence', { event: 'sync' }, () => {
    const state = channel3.presenceState();
    const users = Object.values(state).flat();
    setOnlineUsers(users);
  })
  .on('presence', { event: 'join' }, ({ key, newPresences }) => {
    console.log('User joined:', key);
  })
  .on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
    console.log('User left:', key);
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await channel3.track({
        user_id: currentUser.id,
        email: currentUser.email
      });
    }
  });
```

---

## 4. Storage Questions

### Q9: Làm thế nào để upload large files với progress?

**A:** Sử dụng XMLHttpRequest với progress tracking:

```typescript
// Upload with progress tracking
const uploadFileWithProgress = async (
  bucket: string,
  path: string,
  file: File,
  onProgress: (progress: number) => void
): Promise<{ data: any; error: any }> => {
  return new Promise((resolve, reject) => {
    // Get upload URL (requires signed upload for large files)
    supabase.storage
      .from(bucket)
      .upload(path, file, {
        // Options for large files
        cacheControl: '3600',
        upsert: true
      })
      .then(result => {
        // For progress tracking, use XHR instead
        resolve(result);
      })
      .catch(reject);
  });
};

// Alternative: Use XHR for progress
const uploadWithXHR = (
  bucket: string,
  path: string,
  file: File,
  onProgress: (percent: number) => void
): Promise<{ data: any; error: any }> => {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    
    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable) {
        const percent = (e.loaded / e.total) * 100;
        onProgress(percent);
      }
    };

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve({ data: JSON.parse(xhr.responseText), error: null });
      } else {
        reject({ data: null, error: JSON.parse(xhr.responseText) });
      }
    };

    xhr.onerror = () => reject({ data: null, error: 'Upload failed' });

    // Note: This requires custom upload endpoint
    xhr.open('POST', `${SUPABASE_URL}/storage/v1/object/upload/${bucket}/${path}`);
    xhr.setRequestHeader('Authorization', `Bearer ${SUPABASE_ANON_KEY}`);
    xhr.send(file);
  });
};

// Chunked upload for very large files
const chunkUpload = async (
  bucket: string,
  path: string,
  file: File,
  chunkSize: number = 5 * 1024 * 1024, // 5MB chunks
  onProgress: (percent: number) => void
) => {
  const totalChunks = Math.ceil(file.size / chunkSize);
  const uploadedParts = [];

  for (let i = 0; i < totalChunks; i++) {
    const start = i * chunkSize;
    const end = Math.min(start + chunkSize, file.size);
    const chunk = file.slice(start, end);

    const { data, error } = await supabase.storage
      .from(bucket)
      .upload(`${path}.part${i}`, chunk, {
        contentType: 'application/octet-stream'
      });

    if (error) throw error;
    uploadedParts.push(data.path);

    onProgress(((i + 1) / totalChunks) * 100);
  }

  // Finalize upload (requires edge function to combine parts)
  return { uploadedParts };
};
```

---

### Q10: Làm thế nào để protect uploaded files?

**A:** Implement proper access control:

```typescript
// Method 1: Signed URLs for time-limited access
const getSecureUrl = async (path: string, expiresIn: number = 3600) => {
  const { data, error } = await supabase.storage
    .from('private-documents')
    .createSignedUrl(path, expiresIn);

  return { url: data.signedUrl, error };
};

// Method 2: Verify ownership before granting access
const downloadPrivateFile = async (userId: string, filePath: string) => {
  // Step 1: Verify user owns this file
  const { data: file, error: fileError } = await supabase
    .from('user_files')
    .select('*')
    .eq('user_id', userId)
    .eq('storage_path', filePath)
    .single();

  if (fileError || !file) {
    throw new Error('Access denied');
  }

  // Step 2: Generate signed URL
  const { data, error } = await supabase.storage
    .from('private-documents')
    .createSignedUrl(filePath, 3600);

  if (error) throw error;

  return data.signedUrl;
};

// Method 3: Stream through Edge Function for complex access control
Deno.serve(async (req) => {
  const authHeader = req.headers.get('Authorization');
  const { path } = await req.json();

  // Verify user
  const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
    global: { headers: { Authorization: authHeader } }
  });
  const { data: { user } } = await supabase.auth.getUser();

  // Check if user has access
  const { data: access } = await supabase
    .from('file_access')
    .select('*')
    .eq('user_id', user.id)
    .eq('file_path', path)
    .single();

  if (!access) {
    return new Response('Access denied', { status: 403 });
  }

  // Download and stream file
  const { data } = await supabase.storage
    .from('private-documents')
    .download(path);

  return new Response(data);
});
```

---

## 5. Edge Functions Questions

### Q11: Làm thế nào để debug Edge Functions?

**A:** Có nhiều methods để debug:

```typescript
// Method 1: Local development
supabase functions serve function-name
// Then call with curl or HTTP client

// Method 2: Console logging
Deno.serve(async (req) => {
  console.log('Request received:', req.method);
  console.log('Headers:', Object.fromEntries(req.headers));

  try {
    const body = await req.json();
    console.log('Body:', body);
    
    // Your logic here
    const result = processData(body);
    console.log('Result:', result);

    return new Response(JSON.stringify(result));
  } catch (error) {
    console.error('Error:', error);
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500
    });
  }
});

// Method 3: View logs
supabase functions logs function-name

// Method 4: Tail logs in real-time
supabase functions logs function-name --follow

// Method 5: Structured logging
interface LogEntry {
  timestamp: string;
  level: 'info' | 'warn' | 'error';
  requestId: string;
  message: string;
  metadata?: Record<string, any>;
}

const log = (entry: Omit<LogEntry, 'timestamp' | 'requestId'>) => {
  const logEntry: LogEntry = {
    ...entry,
    timestamp: new Date().toISOString(),
    requestId: crypto.randomUUID()
  };
  console.log(JSON.stringify(logEntry));
};

Deno.serve(async (req) => {
  const requestId = crypto.randomUUID();
  
  log({
    level: 'info',
    requestId,
    message: 'Processing request'
  });

  // ... rest of code
});

// Method 6: Use Sentry for error tracking
import * as Sentry from 'https://esm.sh/@sentry/browser@7.50.0';

Sentry.init({
  dsn: Deno.env.get('SENTRY_DSN'),
  tracesSampleRate: 1.0,
});

Deno.serve(async (req) => {
  try {
    // Your code
  } catch (error) {
    Sentry.captureException(error);
    throw error;
  }
});
```

---

### Q12: Edge Functions có thể truy cập database không?

**A:** Có, Edge Functions có full database access:

```typescript
Deno.serve(async (req) => {
  // Create Supabase client with auth
  const authHeader = req.headers.get('Authorization');
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    {
      global: { headers: { Authorization: authHeader } }
    }
  );

  // Access as authenticated user
  const { data: { user } } = await supabase.auth.getUser();

  // Query database
  const { data, error } = await supabase
    .from('posts')
    .select('*')
    .eq('user_id', user.id);

  // Insert/Update
  const { data: newPost, error: insertError } = await supabase
    .from('posts')
    .insert({ title: 'New Post', user_id: user.id })
    .select()
    .single();

  // Admin operations (use service role)
  const supabaseAdmin = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  );

  // Admin can bypass RLS
  const { data: allUsers } = await supabaseAdmin
    .from('users')
    .select('*');

  return new Response(JSON.stringify({ data, newPost, allUsers }));
});
```

---

## 6. Performance Questions

### Q13: Làm thế nào để optimize query performance?

**A:** Áp dụng các optimization techniques:

```typescript
// 1. Use SELECT only needed columns
// Bad
const { data } = await supabase.from('posts').select('*');

// Good
const { data } = await supabase
  .from('posts')
  .select('id, title, created_at');

// 2. Use .single() for single row results
// Bad
const { data } = await supabase.from('posts').select('*').eq('id', id);
// if (data.length > 0) { ... }

// Good
const { data } = await supabase.from('posts').select('*').eq('id', id).single();

// 3. Use .maybeSingle() when result might be null
const { data } = await supabase
  .from('profiles')
  .select('*')
  .eq('username', 'unknown')
  .maybeSingle(); // Returns null instead of error if no rows

// 4. Use IN for batch queries
// Bad
for (const id of ids) {
  const { data } = await supabase.from('posts').select('*').eq('id', id);
}

// Good
const { data } = await supabase
  .from('posts')
  .select('*')
  .in('id', ids);

// 5. Use RPC for complex queries
// Create in database
CREATE OR REPLACE FUNCTION get_user_feed(
  p_user_id UUID,
  p_limit INT DEFAULT 20
)
RETURNS SETOF posts AS $$
BEGIN
  RETURN QUERY
  SELECT * FROM posts
  WHERE user_id = p_user_id
  ORDER BY created_at DESC
  LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

// Call RPC
const { data } = await supabase.rpc('get_user_feed', {
  p_user_id: userId,
  p_limit: 20
});

// 6. Add indexes for frequently queried columns
// In migration
CREATE INDEX CONCURRENTLY idx_posts_user_id ON posts(user_id);
CREATE INDEX CONCURRENTLY idx_posts_published ON posts(published) WHERE published = true;

// 7. Use covering indexes
CREATE INDEX idx_posts_user_date 
ON posts(user_id, created_at DESC) 
INCLUDE (title, slug);

// 8. Analyze query with EXPLAIN
// In SQL Editor
EXPLAIN ANALYZE
SELECT * FROM posts 
WHERE user_id = 'xxx' 
ORDER BY created_at DESC 
LIMIT 20;
```

---

### Q14: Khi nào nên sử dụng RPC thay vì direct queries?

**A:** RPC tốt trong các trường hợp:

| Scenario | Use RPC | Use Direct Query |
|----------|---------|-----------------|
| Complex joins | ✅ | ❌ |
| Aggregations | ✅ | ❌ |
| Business logic | ✅ | ❌ |
| Transaction | ✅ | ❌ |
| Simple CRUD | ❌ | ✅ |
| Real-time filters | ❌ | ✅ |

```typescript
// Use RPC for complex logic
const getDashboardStats = async (userId: string) => {
  const { data, error } = await supabase.rpc('get_dashboard_stats', {
    p_user_id: userId,
    p_start_date: '2024-01-01',
    p_end_date: '2024-12-31'
  });
  return { data, error };
};

// RPC with transaction
CREATE OR REPLACE FUNCTION transfer_credits(
  from_user_id UUID,
  to_user_id UUID,
  amount DECIMAL
) RETURNS BOOLEAN AS $$
DECLARE
  from_balance DECIMAL;
BEGIN
  -- Check balance
  SELECT balance INTO from_balance
  FROM user_balances
  WHERE user_id = from_user_id
  FOR UPDATE; -- Lock row

  IF from_balance < amount THEN
    RETURN FALSE;
  END IF;

  -- Deduct from sender
  UPDATE user_balances
  SET balance = balance - amount
  WHERE user_id = from_user_id;

  -- Add to receiver
  UPDATE user_balances
  SET balance = balance + amount
  WHERE user_id = to_user_id;

  RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

---

## 7. Migration Questions

### Q15: Làm thế nào để migrate từ Firebase?

**A:** Systematic migration approach:

```typescript
// 1. Map Firebase concepts to Supabase
const migrationMap = {
  'users': 'auth.users + public.profiles',
  'posts': 'public.posts',
  'comments': 'public.comments',
  'likes': 'public.likes',
  // Firestore collections map to PostgreSQL tables
};

// 2. Export Firebase data
// Use Firebase Admin SDK to export all collections

// 3. Transform and import
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);

const migrateUsers = async (firebaseUsers: FirebaseUser[]) => {
  for (const user of firebaseUsers) {
    // Create auth user
    const { data: authUser, error: authError } = await supabase.auth.admin.createUser({
      email: user.email,
      email_confirm: true,
      user_metadata: {
        firebase_uid: user.uid,
        display_name: user.displayName,
        photo_url: user.photoURL
      }
    });

    if (authError) {
      console.error('Failed to create user:', authError);
      continue;
    }

    // Create profile
    await supabase.from('profiles').insert({
      id: authUser.user.id,
      email: user.email,
      display_name: user.displayName,
      photo_url: user.photoURL
    });
  }
};

const migratePosts = async (firebasePosts: FirebasePost[]) => {
  for (const post of firebasePosts) {
    await supabase.from('posts').insert({
      id: post.id, // Use same ID or generate new
      user_id: userIdMap[post.userId], // Map to new user ID
      title: post.title,
      content: post.content,
      created_at: new Date(post.createdAt).toISOString()
    });
  }
};

// 4. Migrate files
const migrateFiles = async (firebaseFiles: FirebaseFile[]) => {
  for (const file of firebaseFiles) {
    // Download from Firebase Storage
    const response = await fetch(file.downloadURL);
    const blob = await response.blob();

    // Upload to Supabase Storage
    const path = `migrated/${file.id}/${file.name}`;
    await supabase.storage.from('uploads').upload(path, blob);
  }
};
```

---

### Q16: Làm thế nào để handle schema migrations?

**A:** Best practices cho migrations:

```typescript
// 1. Create migration files
// supabase/migrations/20240101_add_soft_delete.sql
CREATE TABLE IF NOT EXISTS posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    content TEXT,
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "View non-deleted posts"
ON posts FOR SELECT
USING (deleted_at IS NULL);

-- 2. Apply migrations locally
supabase db push

// 3. Review diff before production
supabase db diff > migrations/new_migration.sql

// 4. Apply to production
supabase db push --project-ref production-ref

// 5. For risky migrations, use concurrent index creation
-- Good: Non-blocking
CREATE INDEX CONCURRENTLY idx_posts_user_id ON posts(user_id);

-- Bad: Locks table
CREATE INDEX idx_posts_user_id ON posts(user_id);

// 6. Rollback strategy
-- migrations/20240101_add_soft_delete_rollback.sql
ALTER TABLE posts DROP COLUMN deleted_at;

// 7. Verify migration
const verifyMigration = async () => {
  const { data, error } = await supabase
    .from('posts')
    .select('deleted_at')
    .limit(1);

  return { success: !error, error };
};
```
