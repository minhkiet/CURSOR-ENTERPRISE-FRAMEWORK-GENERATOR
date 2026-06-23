# Supabase Anti-Patterns - Các Mẫu Cần Tránh

## Giới thiệu

Tài liệu này liệt kê các anti-patterns phổ biến khi sử dụng Supabase, giải thích tại sao chúng gây vấn đề và cung cấp giải pháp thay thế tốt hơn.

---

## 1. Database Design Anti-Patterns

### 1.1. Missing Row Level Security

**Mô tả:** Không enable RLS hoặc không tạo policies, để lộ data công khai.

**Vấn đề:**
```typescript
// ❌ Bad: Table without RLS
CREATE TABLE public.user_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id),
    sensitive_info TEXT, -- Có thể bị truy cập bởi bất kỳ ai!
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Quên enable RLS
-- Ai cũng có thể truy cập dữ liệu nhạy cảm
```

**Giải pháp:**
```typescript
// ✅ Good: Enable RLS với proper policies
ALTER TABLE public.user_data ENABLE ROW LEVEL SECURITY;

-- Chỉ owner mới đọc được data của họ
CREATE POLICY "Users can view own data"
ON public.user_data FOR SELECT
USING (auth.uid() = user_id);

-- Chỉ owner mới insert được data của họ
CREATE POLICY "Users can insert own data"
ON public.user_data FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Chỉ owner mới update được data của họ
CREATE POLICY "Users can update own data"
ON public.user_data FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Chỉ owner mới delete được data của họ
CREATE POLICY "Users can delete own data"
ON public.user_data FOR DELETE
USING (auth.uid() = user_id);
```

---

### 1.2. Using SELECT *

**Mô tả:** Sử dụng `SELECT *` thay vì chỉ định columns cần thiết.

**Vấn đề:**
```typescript
// ❌ Bad: SELECT * returns all columns
const { data } = await supabase
    .from('posts')
    .select('*')
    .eq('user_id', userId);

// Problems:
// - Returns unnecessary large TEXT/JSON columns
// - Cannot use covering indexes
// - Slower query execution
// - TypeScript types less specific
```

**Giải pháp:**
```typescript
// ✅ Good: Specify only needed columns
const { data } = await supabase
    .from('posts')
    .select('id, title, slug, created_at')
    .eq('user_id', userId)
    .order('created_at', { ascending: false });

// ✅ Good: For list views, avoid large columns
const { data: postList } = await supabase
    .from('posts')
    .select(`
        id,
        title,
        slug,
        created_at,
        author:profiles!inner(name, avatar_url),
        comment_count:comments(count)
    `)
    .eq('published', true)
    .limit(20);

// ✅ Good: Fetch full content only when needed
const { data: post } = await supabase
    .from('posts')
    .select('*')
    .eq('slug', slugParam)
    .single();
```

---

### 1.3. Storing Denormalized Data Without Need

**Mô tả:** Lưu trữ denormalized data (như computed columns) mà không cần thiết.

**Vấn đề:**
```typescript
// ❌ Bad: Storing computed values that can be derived
CREATE TABLE posts (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    title TEXT,
    content TEXT,
    -- Redundant: can be computed
    author_name TEXT, 
    author_avatar TEXT,
    -- Redundant: can be counted
    comment_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    -- These require triggers/maintenance
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger để cập nhật counters mỗi khi có thay đổi
CREATE OR REPLACE FUNCTION update_post_counts()
RETURNS TRIGGER AS $$
BEGIN
    -- Complex logic required
    -- Performance overhead on every insert/update/delete
END;
$$ LANGUAGE plpgsql;
```

**Giải pháp:**
```typescript
// ✅ Good: Compute on read, not write
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Fetch với computed fields khi cần
const { data: postWithCounts } = await supabase
    .from('posts')
    .select(`
        *,
        author:profiles(name, avatar_url),
        comments(id)
    `)
    .eq('id', postId)
    .single();

// client-side computation
const commentCount = postWithCounts.comments.length;

// ✅ Good: Use views for common aggregations
CREATE OR REPLACE VIEW posts_with_counts AS
SELECT 
    p.*,
    pr.name as author_name,
    pr.avatar_url as author_avatar,
    (SELECT COUNT(*) FROM comments WHERE post_id = p.id)::INT as comment_count,
    (SELECT COUNT(*) FROM likes WHERE post_id = p.id)::INT as like_count
FROM posts p
JOIN profiles pr ON p.user_id = pr.id;
```

---

## 2. Query Anti-Patterns

### 2.1. N+1 Query Problem

**Mô tả:** Loop qua results để fetch related data, tạo ra N queries.

**Vấn đề:**
```typescript
// ❌ Bad: N+1 queries
const { data: posts } = await supabase
    .from('posts')
    .select('*')
    .eq('user_id', userId);

const postsWithAuthors = [];
for (const post of posts) {
    // Query này chạy N lần!
    const { data: author } = await supabase
        .from('profiles')
        .select('name, avatar_url')
        .eq('id', post.user_id)
        .single();
    
    postsWithAuthors.push({ ...post, author });
}

// Với 100 posts = 101 queries!
```

**Giải pháp:**
```typescript
// ✅ Good: Single query với JOIN/embed
const { data: posts } = await supabase
    .from('posts')
    .select(`
        *,
        author:profiles!inner(
            id,
            name,
            avatar_url
        )
    `)
    .eq('user_id', userId);

// posts[0].author.name - works!

// ✅ Good: Use RPC for complex joins
const { data } = await supabase.rpc('get_posts_with_details', {
    p_user_id: userId,
    p_limit: 20
});

// ✅ Good: Batch fetch related data
const { data: posts } = await supabase
    .from('posts')
    .select('user_id')
    .eq('user_id', userId);

const userIds = [...new Set(posts.map(p => p.user_id))];

const { data: profiles } = await supabase
    .from('profiles')
    .select('*')
    .in('id', userIds);

const profileMap = new Map(profiles.map(p => [p.id, p]));
const postsWithProfiles = posts.map(p => ({
    ...p,
    author: profileMap.get(p.user_id)
}));
```

---

### 2.2. Inefficient Filtering

**Mô tả:** Sử dụng filter không hiệu quả, gây ra full table scan.

**Vấn đề:**
```typescript
// ❌ Bad: Filter trên column không có index
const { data } = await supabase
    .from('posts')
    .select('*')
    .ilike('title', '%javascript%'); -- Full scan!

// ❌ Bad: Filter trên function result
const { data } = await supabase
    .from('posts')
    .select('*')
    .filter('LOWER(title)', 'ilike', '%javascript%'); -- Không dùng được index

// ❌ Bad: Sử dụng OR khi có thể dùng IN
const { data } = await supabase
    .from('posts')
    .select('*')
    .or('category.eq.tech,category.eq.science,category.eq.health');
```

**Giải pháp:**
```typescript
// ✅ Good: Tạo index cho search columns
CREATE INDEX idx_posts_title_trgm ON posts USING gin(title gin_trgm_ops);
CREATE INDEX idx_posts_category ON posts(category);

// Sử dụng text search
const { data } = await supabase
    .from('posts')
    .select('*')
    .textSearch('title', 'javascript', { type: 'websearch' });

// ✅ Good: Sử dụng IN thay vì OR
const { data } = await supabase
    .from('posts')
    .select('*')
    .in('category', ['tech', 'science', 'health']);

// ✅ Good: Multiple eq() calls are AND-ed
const { data } = await supabase
    .from('posts')
    .select('*')
    .eq('published', true)
    .eq('category', 'tech')
    .gte('created_at', startDate);
```

---

### 2.3. Missing Pagination

**Mô tả:** Fetch tất cả data mà không pagination.

**Vấn đề:**
```typescript
// ❌ Bad: Fetch all users (could be millions!)
const { data: allUsers } = await supabase
    .from('users')
    .select('*');

// Memory issues, slow response, wasted bandwidth
```

**Giải pháp:**
```typescript
// ✅ Good: Offset-based pagination
const fetchPage = async (page: number, pageSize = 20) => {
    const from = page * pageSize;
    const to = from + pageSize - 1;
    
    const { data, error } = await supabase
        .from('posts')
        .select('id, title, created_at')
        .order('created_at', { ascending: false })
        .range(from, to);
    
    return { data, error, hasMore: data?.length === pageSize };
};

// ✅ Good: Keyset pagination (better performance for large tables)
const fetchMore = async (lastPost: Post) => {
    const { data, error } = await supabase
        .from('posts')
        .select('id, title, created_at')
        .order('created_at', { ascending: false })
        .lt('created_at', lastPost.created_at)
        .lt('id', lastPost.id) // Tie-breaker
        .limit(20);
    
    return { data, error };
};

// ✅ Good: Infinite scroll implementation
const useInfiniteScroll = () => {
    const [posts, setPosts] = useState<Post[]>([]);
    const [loading, setLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    const [lastPost, setLastPost] = useState<Post | null>(null);
    
    const loadMore = async () => {
        if (loading || !hasMore) return;
        
        setLoading(true);
        const { data, error } = await supabase
            .from('posts')
            .select('*')
            .order('created_at', { ascending: false })
            .gt('created_at', lastPost?.created_at || '9999-12-31')
            .limit(20);
        
        if (data?.length) {
            setPosts([...posts, ...data]);
            setLastPost(data[data.length - 1]);
        }
        if (!data?.length || data.length < 20) {
            setHasMore(false);
        }
        setLoading(false);
    };
    
    return { posts, loading, hasMore, loadMore };
};
```

---

## 3. Authentication Anti-Patterns

### 3.1. Exposing Service Role Key

**Mô tả:** Sử dụng service role key ở client-side, bypass RLS hoàn toàn.

**Vấn đề:**
```typescript
// ❌ Bad: Service role key in client code
const supabase = createClient(
    'https://xxx.supabase.co',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' // Service role key!
);

// Service role bypasses ALL RLS policies!
// Any client can access ANY data!
```

**Giải pháp:**
```typescript
// ✅ Good: Use anon key at client, service role at server
// Client (browser):
const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY! // Safe to expose
);

// Server (API route):
const supabaseAdmin = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY! // Never expose this!
);

// ✅ Good: Verify user in server-side code
export async function deletePostServer(postId: string, userId: string) {
    const supabaseAdmin = createClient(...);
    
    // First verify ownership
    const { data: post } = await supabaseAdmin
        .from('posts')
        .select('user_id')
        .eq('id', postId)
        .single();
    
    if (post?.user_id !== userId) {
        throw new Error('Unauthorized');
    }
    
    // Then delete
    return supabaseAdmin.from('posts').delete().eq('id', postId);
}
```

---

### 3.2. Not Validating Auth Token

**Mô tả:** Không verify JWT token trong Edge Functions hoặc API routes.

**Vấn đề:**
```typescript
// ❌ Bad: Not checking auth header
Deno.serve(async (req) => {
    const { data } = await req.json();
    
    // No authentication check!
    // Anyone can call this endpoint!
    
    await supabase.from('sensitive_data').delete().eq('id', data.id);
});
```

**Giải pháp:**
```typescript
// ✅ Good: Always validate auth
Deno.serve(async (req) => {
    const authHeader = req.headers.get('Authorization');
    
    if (!authHeader) {
        return new Response(
            JSON.stringify({ error: 'Unauthorized' }),
            { status: 401 }
        );
    }
    
    // Verify token
    const supabase = createClient(
        Deno.env.get('SUPABASE_URL')!,
        Deno.env.get('SUPABASE_ANON_KEY')!,
        {
            global: {
                headers: { Authorization: authHeader }
            }
        }
    );
    
    const { data: { user }, error } = await supabase.auth.getUser();
    
    if (error || !user) {
        return new Response(
            JSON.stringify({ error: 'Invalid token' }),
            { status: 401 }
        );
    }
    
    // Now you can safely use user.id
    // ...
});
```

---

### 3.3. Storing Passwords in User Metadata

**Mô tả:** Cố gắng lưu trữ password hoặc sensitive data trong user metadata.

**Vấn đề:**
```typescript
// ❌ Bad: Trying to store password in metadata
await supabase.auth.updateUser({
    data: {
        password_hash: 'some_hash', // DON'T DO THIS!
        api_key: 'secret_key'
    }
});

// user_metadata is readable by the user themselves!
```

**Giải pháp:**
```typescript
// ✅ Good: Use auth.users for auth, separate table for app data
// Store sensitive app data in your own tables
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    key_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ
);

-- Use RLS to protect
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own api keys"
ON api_keys FOR ALL
USING (auth.uid() = user_id);

-- ✅ Good: Store only non-sensitive metadata
await supabase.auth.updateUser({
    data: {
        display_name: 'John Doe',
        avatar_url: 'https://...',
        preferences: { theme: 'dark' }
        // No sensitive data!
    }
});
```

---

## 4. Storage Anti-Patterns

### 4.1. Storing Files in Database

**Mô tả:** Lưu trữ file content trong database columns thay vì Storage.

**Vấn đề:**
```sql
-- ❌ Bad: Storing base64 images in TEXT column
CREATE TABLE posts (
    id UUID PRIMARY KEY,
    title TEXT,
    content TEXT,
    thumbnail_base64 TEXT -- Large data in database!
);

-- Problems:
-- - Bloats database size
-- - Slows down queries
-- - Can't use CDN
-- - No streaming for large files
```

**Giải pháp:**
```typescript
// ✅ Good: Store files in Supabase Storage
const uploadPostThumbnail = async (postId: string, file: File) => {
    const ext = file.name.split('.').pop();
    const path = `posts/${postId}/thumbnail.${ext}`;
    
    const { error: uploadError } = await supabase.storage
        .from('images')
        .upload(path, file, {
            cacheControl: '3600',
            upsert: true
        });
    
    if (uploadError) throw uploadError;
    
    const { data: urlData } = supabase.storage
        .from('images')
        .getPublicUrl(path);
    
    // Save only URL in database
    await supabase
        .from('posts')
        .update({ thumbnail_url: urlData.publicUrl })
        .eq('id', postId);
};

// ✅ Good: Store metadata in database, file in storage
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    mime_type TEXT,
    size_bytes BIGINT,
    uploaded_by UUID REFERENCES auth.users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

### 4.2. Not Using Signed URLs for Private Files

**Mô tả:** Cố gắng access private files mà không có signed URL.

**Vấn đề:**
```typescript
// ❌ Bad: Trying to get public URL for private bucket
const { data } = supabase.storage
    .from('private-files') // Bucket is private!
    .getPublicUrl('secret.pdf');

// Returns invalid URL, won't work!
```

**Giải pháp:**
```typescript
// ✅ Good: Use signed URL for private files
const getPrivateFile = async (path: string) => {
    const { data, error } = await supabase.storage
        .from('private-files')
        .createSignedUrl(path, 3600); // Expires in 1 hour
    
    if (error) throw error;
    
    // Redirect user to signed URL
    window.open(data.signedUrl, '_blank');
};

// ✅ Good: Download through signed URL
const downloadPrivateFile = async (path: string) => {
    const { data, error } = await supabase.storage
        .from('private-documents')
        .createSignedUrl(path, 3600);
    
    if (error) throw error;
    
    // Fetch through signed URL
    const response = await fetch(data.signedUrl);
    const blob = await response.blob();
    
    // Create download link
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = path.split('/').pop()!;
    a.click();
    URL.revokeObjectURL(url);
};
```

---

## 5. Realtime Anti-Patterns

### 5.1. Not Cleaning Up Subscriptions

**Mô tả:** Không unsubscribe channels, dẫn đến memory leaks.

**Vấn đề:**
```typescript
// ❌ Bad: Subscribe without cleanup
function ChatRoom({ roomId }: { roomId: string }) {
    const [messages, setMessages] = useState([]);
    
    useEffect(() => {
        // Subscribes but never unsubscribes!
        supabase
            .channel(`room-${roomId}`)
            .on('postgres_changes', { event: '*', table: 'messages' }, 
                (payload) => setMessages(m => [...m, payload.new]))
            .subscribe();
        
        // Missing cleanup = memory leak!
    }, [roomId]);
}
```

**Giải pháp:**
```typescript
// ✅ Good: Clean up subscriptions
function ChatRoom({ roomId }: { roomId: string }) {
    const [messages, setMessages] = useState([]);
    
    useEffect(() => {
        const channel = supabase
            .channel(`room-${roomId}`)
            .on('postgres_changes', 
                { event: 'INSERT', table: 'messages', filter: `room_id=eq.${roomId}` },
                (payload) => setMessages(m => [...m, payload.new]))
            .subscribe();
        
        // Cleanup when component unmounts or roomId changes
        return () => {
            supabase.removeChannel(channel);
        };
    }, [roomId]);
}

// ✅ Good: Use custom hook for cleaner code
function useRealtimeMessages(roomId: string) {
    const [messages, setMessages] = useState([]);
    const [channel, setChannel] = useState<ReturnType<typeof supabase.channel> | null>(null);
    
    useEffect(() => {
        if (!roomId) return;
        
        const newChannel = supabase
            .channel(`messages-${roomId}`)
            .on('postgres_changes', 
                { event: 'INSERT', table: 'messages', filter: `room_id=eq.${roomId}` },
                (payload) => setMessages(m => [...m, payload.new]))
            .subscribe();
        
        setChannel(newChannel);
        
        return () => {
            if (newChannel) {
                supabase.removeChannel(newChannel);
            }
        };
    }, [roomId]);
    
    return messages;
}
```

---

### 5.2. Subscribing to All Events When Not Needed

**Mô tả:** Subscribe to `*` event khi chỉ cần một số loại events.

**Vấn đề:**
```typescript
// ❌ Bad: Subscribe to all events
supabase
    .channel('changes')
    .on('postgres_changes', 
        { event: '*', table: 'messages' }, // INSERT, UPDATE, DELETE all
        (payload) => {
            // Have to check payload.eventType every time!
            if (payload.eventType === 'INSERT') { ... }
            if (payload.eventType === 'DELETE') { ... }
        })
    .subscribe();
```

**Giải pháp:**
```typescript
// ✅ Good: Subscribe only to needed events
supabase
    .channel('new-messages')
    .on('postgres_changes', 
        { event: 'INSERT', table: 'messages' },
        (payload) => addMessage(payload.new))
    .subscribe();

// ✅ Good: Separate handlers for different events
const channel = supabase.channel('messages-with-status');

channel
    .on('postgres_changes', 
        { event: 'INSERT', table: 'messages' },
        (payload) => addMessage(payload.new))
    .on('postgres_changes', 
        { event: 'UPDATE', table: 'messages', filter: 'status=eq.delivered' },
        (payload) => markDelivered(payload.new.id))
    .on('postgres_changes', 
        { event: 'DELETE', table: 'messages' },
        (payload) => removeMessage(payload.old.id))
    .subscribe();
```

---

## 6. Error Handling Anti-Patterns

### 6.1. Ignoring Error Objects

**Mô tả:** Không kiểm tra error từ Supabase responses.

**Vấn đề:**
```typescript
// ❌ Bad: Ignoring errors
const { data } = await supabase
    .from('posts')
    .select('*')
    .eq('id', postId)
    .single();

// No error checking!
// data might be null, error might exist
// App continues with undefined data!

// ❌ Bad: Catching but not handling properly
try {
    const { data } = await supabase.from('posts').insert({...});
} catch (e) {
    console.log('Error!'); // Too generic!
}
```

**Giải pháp:**
```typescript
// ✅ Good: Always check for errors
const { data, error } = await supabase
    .from('posts')
    .select('*')
    .eq('id', postId)
    .single();

if (error) {
    console.error('Failed to fetch post:', error.message);
    // Handle specific error codes
    if (error.code === 'PGRST116') { // No rows returned
        return null;
    }
    throw error;
}

// ✅ Good: Type-safe error handling
const fetchPost = async (id: string): Promise<Post> => {
    const { data, error } = await supabase
        .from('posts')
        .select('*')
        .eq('id', id)
        .single();
    
    if (error) {
        if (error.code === 'PGRST116') {
            throw new NotFoundError(`Post ${id} not found`);
        }
        throw new DatabaseError(error.message);
    }
    
    return data;
};

// ✅ Good: Wrapper function with error handling
const safeQuery = async <T>(
    query: () => Promise<{ data: T | null; error: any }>
): Promise<T> => {
    const { data, error } = await query();
    
    if (error) {
        throw new Error(`Query failed: ${error.message}`);
    }
    
    if (!data) {
        throw new Error('No data returned');
    }
    
    return data;
};

// Usage
const posts = await safeQuery(() => 
    supabase.from('posts').select('*')
);
```

---

### 6.2. Unhandled Promise Rejections

**Mô tả:** Không handle promise rejections, gây ra unhandled errors.

**Vấn đề:**
```typescript
// ❌ Bad: Unhandled promise
supabase
    .from('posts')
    .select('*')
    .then(data => console.log(data))
    .catch(err => console.error(err));

// If this code is in production without proper error boundary,
// Unhandled promise rejection!

// ❌ Bad: Async function without try/catch
const createPost = async (post: NewPost) => {
    // No error handling!
    const { data } = await supabase.from('posts').insert(post);
    return data;
};
```

**Giải pháp:**
```typescript
// ✅ Good: Proper async/await with try/catch
const createPost = async (post: NewPost) => {
    try {
        const { data, error } = await supabase
            .from('posts')
            .insert(post)
            .select()
            .single();
        
        if (error) {
            throw new Error(`Failed to create post: ${error.message}`);
        }
        
        return data;
    } catch (err) {
        console.error('Error creating post:', err);
        throw err; // Re-throw for caller to handle
    }
};

// ✅ Good: Error boundary in React
class ErrorBoundary extends React.Component {
    componentDidCatch(error, errorInfo) {
        console.error('Error:', error, errorInfo);
        // Send to error tracking service
    }
    
    render() {
        return this.props.children;
    }
}

// ✅ Good: Global unhandled rejection handler (Node.js)
process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
    // Send to error tracking service
});
```

---

## 7. Security Anti-Patterns

### 7.1. SQL Injection via RPC

**Mô tả:** Concatenating user input in RPC calls.

**Vấn đề:**
```typescript
// ❌ Bad: SQL injection vulnerability
CREATE OR REPLACE FUNCTION search_posts(query TEXT)
RETURNS SETOF posts AS $$
BEGIN
    RETURN QUERY EXECUTE 
        'SELECT * FROM posts WHERE title ILIKE ''%' || query || '%''';
    -- Vulnerable to SQL injection!
END;
$$ LANGUAGE plpgsql;

// If user passes: '; DROP TABLE posts; --
```

**Giải pháp:**
```typescript
// ✅ Good: Use parameterized queries
CREATE OR REPLACE FUNCTION search_posts(query TEXT)
RETURNS SETOF posts AS $$
BEGIN
    RETURN QUERY SELECT * FROM posts 
    WHERE title ILIKE '%' || query || '%';
    -- PostgreSQL handles escaping
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

// ✅ Good: Use Supabase query builder
const searchPosts = async (searchTerm: string) => {
    const { data, error } = await supabase
        .from('posts')
        .select('*')
        .ilike('title', `%${searchTerm}%`);
    
    return { data, error };
};
```

---

### 7.2. Not Rate Limiting Public Endpoints

**Mô tả:** Không có rate limiting cho authentication endpoints.

**Vấn đề:**
```typescript
// ❌ Bad: No rate limiting on auth endpoints
// Attackers can:
// - Brute force passwords
// - Request unlimited magic links
// - Enumerate valid emails

const signIn = async (email: string, password: string) => {
    // No rate limiting!
    return supabase.auth.signInWithPassword({ email, password });
};

const requestMagicLink = async (email: string) => {
    // Attacker can spam this endpoint!
    return supabase.auth.signInWithOtp({ email });
};
```

**Giải pháp:**
```typescript
// ✅ Good: Implement rate limiting in Edge Function
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

const RATE_LIMIT_WINDOW = 60 * 1000; // 1 minute
const MAX_REQUESTS = 5;

const rateLimits = new Map<string, { count: number; resetAt: number }>();

const checkRateLimit = (identifier: string): boolean => {
    const now = Date.now();
    const limit = rateLimits.get(identifier);
    
    if (!limit || now > limit.resetAt) {
        rateLimits.set(identifier, { count: 1, resetAt: now + RATE_LIMIT_WINDOW });
        return true;
    }
    
    if (limit.count >= MAX_REQUESTS) {
        return false;
    }
    
    limit.count++;
    return true;
};

serve(async (req) => {
    const email = req.headers.get('x-forwarded-for') || 'anonymous';
    
    if (!checkRateLimit(email)) {
        return new Response(
            JSON.stringify({ error: 'Too many requests' }),
            { status: 429 }
        );
    }
    
    // Process request...
});
```

---

## 8. Performance Anti-Patterns

### 8.1. Unnecessary Realtime Subscriptions

**Mô tả:** Subscribe realtime cho data không cần real-time updates.

**Vấn đề:**
```typescript
// ❌ Bad: Realtime for static data
function StaticPage() {
    useEffect(() => {
        // Don't need realtime for FAQ!
        supabase
            .channel('faq-updates')
            .on('postgres_changes', { event: '*', table: 'faqs' }, handler)
            .subscribe();
    }, []);
    
    // Should just fetch once!
}
```

**Giải pháp:**
```typescript
// ✅ Good: Use regular query for static data
function StaticPage() {
    const [faqs, setFaqs] = useState([]);
    
    useEffect(() => {
        // Single fetch is enough
        supabase
            .from('faqs')
            .select('*')
            .then(({ data }) => setFaqs(data || []));
    }, []);
}

// ✅ Good: Use realtime only for dynamic data
function ChatRoom() {
    const [messages, setMessages] = useState([]);
    
    useEffect(() => {
        // Realtime is needed here!
        const channel = supabase
            .channel('messages')
            .on('postgres_changes', { event: 'INSERT', table: 'messages' }, 
                (payload) => setMessages(m => [...m, payload.new]))
            .subscribe();
        
        return () => supabase.removeChannel(channel);
    }, []);
}
```

---

### 8.2. Large Batch Operations Without Consideration

**Mô tả:** Insert/update hàng ngàn rows mà không tối ưu.

**Vấn đề:**
```typescript
// ❌ Bad: Insert 10000 rows one by one
const insertManySlowly = async (items: Item[]) => {
    for (const item of items) {
        await supabase.from('items').insert(item);
        // 10000 separate requests!
    }
};

// ❌ Bad: Insert without batching
const insertWithoutBatching = async (items: Item[]) => {
    for (const item of items) {
        await supabase.from('items').insert(item);
    }
};
```

**Giải pháp:**
```typescript
// ✅ Good: Batch insert (Supabase supports up to ~1000 per request)
const insertBatch = async (items: Item[]) => {
    const batchSize = 1000;
    const results = [];
    
    for (let i = 0; i < items.length; i += batchSize) {
        const batch = items.slice(i, i + batchSize);
        const { data, error } = await supabase
            .from('items')
            .insert(batch)
            .select();
        
        if (error) throw error;
        results.push(data);
    }
    
    return results.flat();
};

// ✅ Good: Use database COPY for very large imports
// Use Supabase Management API or pg_dump/pg_restore

// ✅ Good: Use RPC for server-side batch processing
CREATE OR REPLACE FUNCTION batch_insert_items(items JSONB)
RETURNS SETOF items AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM jsonb_populate_recordset(null::items, items);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```
