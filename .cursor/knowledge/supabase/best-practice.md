# Supabase Best Practices - Thực Hành Tốt Nhất

## Giới thiệu

Tài liệu này tổng hợp các best practices đã được kiểm chứng cho Supabase, giúp tối ưu hóa performance, security, và developer experience trong Cursor Enterprise Framework.

---

## 1. Database Design Best Practices

### 1.1. Schema Design

```typescript
// ✅ Good: Proper schema structure
// Use UUID for all primary keys
CREATE TABLE public.products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    category_id UUID REFERENCES categories(id),
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Virtual computed columns
    CONSTRAINT products_price_check CHECK (price >= 0)
);

-- ✅ Good: Create indexes for foreign keys
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_user_id ON products(user_id);

-- ✅ Good: Partial indexes for common queries
CREATE INDEX idx_products_published ON products(user_id) 
WHERE published = true;

CREATE INDEX idx_products_category ON products(category_id) 
WHERE published = true AND deleted_at IS NULL;

-- ✅ Good: Trigram indexes for text search
CREATE INDEX idx_products_name_trgm ON products USING gin(name gin_trgm_ops);

-- ❌ Bad: Missing indexes on foreign keys
// ❌ Bad: No partial indexes for filtered queries
// ❌ Bad: Using serial integers as IDs (harder to merge across systems)
```

### 1.2. Use Appropriate Data Types

```typescript
// ✅ Good: Appropriate data types
CREATE TABLE users (
    -- UUID for primary key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- TEXT for variable length strings
    email TEXT NOT NULL,
    name TEXT,
    
    -- BOOLEAN for flags
    is_active BOOLEAN DEFAULT true,
    is_admin BOOLEAN DEFAULT false,
    
    -- INTEGER for counts
    login_count INTEGER DEFAULT 0,
    
    -- DECIMAL for monetary values (never use FLOAT!)
    account_balance DECIMAL(12, 2) DEFAULT 0,
    
    -- JSONB for flexible data
    preferences JSONB DEFAULT '{}',
    
    -- TIMESTAMPTZ for timestamps with timezone
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ❌ Bad: Using FLOAT for money
// ❌ Bad: Using VARCHAR(255) for all text fields
// ❌ Bad: Using TEXT instead of JSONB when structure is known
// ❌ Bad: Using DATE when TIMESTAMPTZ is needed
```

### 1.3. Table Relationships

```typescript
// ✅ Good: One-to-many relationship
CREATE TABLE authors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL
);

CREATE TABLE books (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    author_id UUID REFERENCES authors(id) ON DELETE CASCADE,
    title TEXT NOT NULL
);

-- ✅ Good: Many-to-many relationship with junction table
CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL
);

CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL
);

CREATE TABLE enrollments (
    student_id UUID REFERENCES students(id) ON DELETE CASCADE,
    course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
    enrolled_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (student_id, course_id)
);

-- ✅ Good: Self-referential relationship
CREATE TABLE employees (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    manager_id UUID REFERENCES employees(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 2. Row Level Security (RLS) Best Practices

### 2.1. Enable RLS on All Tables

```typescript
// ✅ Good: Always enable RLS
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.likes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.follows ENABLE ROW LEVEL SECURITY;

// ✅ Good: Create helper function to check if user is admin
CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM auth.users
        WHERE id = auth.uid()
        AND raw_user_meta_data->>'role' = 'admin'
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER STABLE;

// ✅ Good: Admin bypass policy
CREATE POLICY "Admin can do anything"
ON public.user_profiles
FOR ALL
USING (public.is_admin())
WITH CHECK (public.is_admin());
```

### 2.2. Comprehensive Policy Examples

```typescript
// ✅ Good: Posts with owner and public visibility
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;

-- Anyone can view published posts
CREATE POLICY "Published posts are viewable by everyone"
ON public.posts FOR SELECT
USING (
    published = true
    OR user_id = auth.uid()  -- Owner can see their own posts
);

-- Users can insert their own posts
CREATE POLICY "Users can insert their own posts"
ON public.posts FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can update their own posts
CREATE POLICY "Users can update their own posts"
ON public.posts FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Users can delete their own posts
CREATE POLICY "Users can delete their own posts"
ON public.posts FOR DELETE
USING (auth.uid() = user_id);

-- ✅ Good: Comments policy
ALTER TABLE public.comments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Comments are viewable if user can see the post"
ON public.comments FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM public.posts
        WHERE posts.id = comments.post_id
        AND (
            posts.published = true
            OR posts.user_id = auth.uid()
        )
    )
);

CREATE POLICY "Users can insert comments on accessible posts"
ON public.comments FOR INSERT
WITH CHECK (
    auth.uid() = user_id
    AND EXISTS (
        SELECT 1 FROM public.posts
        WHERE posts.id = post_id
        AND (
            posts.published = true
            OR posts.user_id = auth.uid()
        )
    )
);
```

### 2.3. Secure API Access

```typescript
// ✅ Good: Verify user in Edge Functions
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

export async function handler(req: Request): Promise<Response> {
    const authHeader = req.headers.get('Authorization');
    
    if (!authHeader) {
        return new Response(
            JSON.stringify({ error: 'Unauthorized' }),
            { status: 401 }
        );
    }
    
    const supabase = createClient(
        Deno.env.get('SUPABASE_URL')!,
        Deno.env.get('SUPABASE_ANON_KEY')!,
        {
            global: {
                headers: {
                    Authorization: authHeader
                }
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
    
    // Proceed with authenticated request
    // ...
}

// ❌ Bad: Not verifying JWT in Edge Functions
// ❌ Bad: Using service role key in client-side code
```

---

## 3. Query Optimization Best Practices

### 3.1. Efficient Queries

```typescript
// ✅ Good: Select only needed columns
const { data } = await supabase
    .from('posts')
    .select('id, title, created_at, author:users(name, avatar_url)')
    .eq('published', true)
    .order('created_at', { ascending: false })
    .limit(10);

// ❌ Bad: SELECT * for large tables
const { data } = await supabase.from('posts').select('*');

// ✅ Good: Use range for pagination
const { data, error } = await supabase
    .from('posts')
    .select('id, title, content')
    .range(0, 9) // First 10 items
    .order('created_at', { ascending: false });

// Next page
const { data: nextPage } = await supabase
    .from('posts')
    .select('id, title, content')
    .range(10, 19) // Next 10 items
    .order('created_at', { ascending: false });

// ✅ Good: Use .single() when expecting one result
const { data: post } = await supabase
    .from('posts')
    .select('*')
    .eq('slug', 'my-post-slug')
    .single();

// ✅ Good: Use .maybeSingle() when result might be null
const { data: user } = await supabase
    .from('profiles')
    .select('*')
    .eq('username', 'johndoe')
    .maybeSingle();
```

### 3.2. Avoid N+1 Queries

```typescript
// ❌ Bad: N+1 query pattern
const { data: posts } = await supabase
    .from('posts')
    .select('*')
    .eq('user_id', userId);

for (const post of posts) {
    const { data: author } = await supabase
        .from('users')
        .select('name')
        .eq('id', post.user_id)
        .single();
    post.authorName = author?.name;
}

// ✅ Good: Join related data in single query
const { data: posts } = await supabase
    .from('posts')
    .select(`
        *,
        author:users!inner (
            id,
            name,
            avatar_url
        )
    `)
    .eq('user_id', userId);

// ✅ Good: Use embed for multiple relationships
const { data: userWithDetails } = await supabase
    .from('users')
    .select(`
        *,
        posts (
            id,
            title,
            created_at
        ),
        comments (
            id,
            content,
            created_at
        ),
        profile:profiles (
            bio,
            website
        )
    `)
    .eq('id', userId)
    .single();
```

### 3.3. Bulk Operations

```typescript
// ✅ Good: Bulk insert
const newPosts = [
    { title: 'Post 1', content: 'Content 1', user_id: userId },
    { title: 'Post 2', content: 'Content 2', user_id: userId },
    { title: 'Post 3', content: 'Content 3', user_id: userId },
];

const { data, error } = await supabase
    .from('posts')
    .insert(newPosts)
    .select();

// ✅ Good: Bulk update
const { data, error } = await supabase
    .from('products')
    .update({ price: 29.99, updated_at: new Date().toISOString() })
    .in('id', [1, 2, 3, 4, 5])
    .eq('category', 'electronics');

// ✅ Good: Bulk delete
const { error } = await supabase
    .from('temp_data')
    .delete()
    .lt('created_at', new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString());
```

---

## 4. Authentication Best Practices

### 4.1. Secure Auth Implementation

```typescript
// ✅ Good: Complete auth flow
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// Sign up with email verification
const signUp = async (email: string, password: string, metadata: object) => {
    const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
            data: metadata,
            emailRedirectTo: `${window.location.origin}/auth/callback`
        }
    });
    
    if (error) throw error;
    return data;
};

// Sign in with rate limiting on frontend
const signIn = async (email: string, password: string) => {
    // Frontend rate limiting
    const lastAttempt = localStorage.getItem('lastSignInAttempt');
    const now = Date.now();
    
    if (lastAttempt && now - parseInt(lastAttempt) < 30000) {
        throw new Error('Please wait 30 seconds before trying again');
    }
    localStorage.setItem('lastSignInAttempt', now.toString());
    
    const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password
    });
    
    if (error) throw error;
    return data;
};

// Sign out with session cleanup
const signOut = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
    
    // Clear local storage
    localStorage.clear();
    sessionStorage.clear();
};

// Protected route wrapper
const withAuth = (Component: React.ComponentType) => {
    return function AuthenticatedComponent(props: any) {
        const { user, isLoading } = useUser();
        const router = useRouter();
        
        useEffect(() => {
            if (!isLoading && !user) {
                router.push('/login');
            }
        }, [user, isLoading, router]);
        
        if (isLoading) {
            return <LoadingSpinner />;
        }
        
        if (!user) {
            return null;
        }
        
        return <Component {...props} />;
    };
};
```

### 4.2. OAuth Best Practices

```typescript
// ✅ Good: Secure OAuth configuration
const signInWithOAuth = async (provider: 'google' | 'github' | 'apple') => {
    const { data, error } = await supabase.auth.signInWithOAuth({
        provider,
        options: {
            redirectTo: `${window.location.origin}/auth/callback`,
            scopes: provider === 'google' ? 'email profile' : undefined,
            queryParams: {
                access_type: 'offline',
                prompt: 'consent'
            }
        }
    });
    
    if (error) throw error;
    return data;
};

// ✅ Good: Handle OAuth callback securely
const handleOAuthCallback = async () => {
    const { data, error } = await supabase.auth.getSessionFromUrl({
        storeSession: true // Auto-persist to localStorage
    });
    
    if (error) {
        console.error('OAuth error:', error);
        return { success: false, error };
    }
    
    // Verify the user exists in your database
    if (data.session) {
        const { data: profile } = await supabase
            .from('profiles')
            .select('*')
            .eq('id', data.session.user.id)
            .single();
        
        if (!profile) {
            // Create profile for new OAuth user
            await supabase.from('profiles').insert({
                id: data.session.user.id,
                email: data.session.user.email
            });
        }
    }
    
    return { success: true, data };
};
```

---

## 5. Storage Best Practices

### 5.1. Organized Bucket Structure

```typescript
// ✅ Good: Organized bucket structure
// Buckets:
// - avatars (public): User profile pictures
// - posts (public): Post images
// - documents (private): Private files
// - backups (private): Database backups

// Create buckets via SQL for consistency
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES 
    ('avatars', 'avatars', true, 5242880, ARRAY['image/jpeg', 'image/png', 'image/webp']),
    ('posts', 'posts', true, 10485760, ARRAY['image/jpeg', 'image/png', 'image/webp', 'video/mp4']),
    ('documents', 'documents', false, 104857600, ARRAY['application/pdf']),
    ('backups', 'backups', false, NULL, NULL);

// ✅ Good: Organized file paths
const uploadAvatar = async (userId: string, file: File) => {
    const ext = file.name.split('.').pop();
    const path = `${userId}/avatar.${ext}`;
    
    const { data, error } = await supabase.storage
        .from('avatars')
        .upload(path, file, {
            cacheControl: '31536000', // 1 year
            upsert: true
        });
    
    if (error) throw error;
    
    const { data: urlData } = supabase.storage
        .from('avatars')
        .getPublicUrl(path);
    
    return urlData.publicUrl;
};

// ✅ Good: Upload with progress tracking
const uploadWithProgress = async (file: File, onProgress: (p: number) => void) => {
    const xhr = new XMLHttpRequest();
    
    return new Promise((resolve, reject) => {
        xhr.upload.onprogress = (e) => {
            if (e.lengthComputable) {
                const progress = (e.loaded / e.total) * 100;
                onProgress(progress);
            }
        };
        
        xhr.onload = () => {
            if (xhr.status === 200) {
                resolve(JSON.parse(xhr.responseText));
            } else {
                reject(new Error('Upload failed'));
            }
        };
        
        xhr.onerror = () => reject(new Error('Upload failed'));
        
        // Use Supabase Storage upload
        supabase.storage
            .from('posts')
            .upload(file.name, file);
    });
};
```

### 5.2. Signed URLs for Private Files

```typescript
// ✅ Good: Generate signed URL for private file access
const getPrivateFileUrl = async (path: string, expiresIn = 3600) => {
    const { data, error } = await supabase.storage
        .from('documents')
        .createSignedUrl(path, expiresIn);
    
    if (error) throw error;
    return data.signedUrl;
};

// ✅ Good: Download private file
const downloadPrivateFile = async (path: string) => {
    const { data, error } = await supabase.storage
        .from('documents')
        .download(path);
    
    if (error) throw error;
    return URL.createObjectURL(data);
};

// ✅ Good: Temporary access token
const getTemporaryAccess = async (userId: string, filePath: string) => {
    // Verify user has access
    const { data: document, error } = await supabase
        .from('documents')
        .select('user_id')
        .eq('path', filePath)
        .single();
    
    if (error || document.user_id !== userId) {
        throw new Error('Access denied');
    }
    
    // Generate signed URL
    return getPrivateFileUrl(filePath, 3600);
};
```

---

## 6. Edge Functions Best Practices

### 6.1. Secure Edge Functions

```typescript
// ✅ Good: Complete secure edge function template
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const corsHeaders = {
    'Access-Control-Allow-Origin': process.env.ALLOWED_ORIGIN || '*',
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

interface RequestBody {
    action: string;
    data: Record<string, unknown>;
}

const validateRequest = async (req: Request): Promise<{ user: any; supabase: any }> => {
    const authHeader = req.headers.get('Authorization');
    
    if (!authHeader) {
        throw new Error('Missing authorization header');
    }
    
    const supabase = createClient(
        Deno.env.get('SUPABASE_URL') ?? '',
        Deno.env.get('SUPABASE_ANON_KEY') ?? '',
        {
            global: { headers: { Authorization: authHeader } }
        }
    );
    
    const { data: { user }, error } = await supabase.auth.getUser();
    
    if (error || !user) {
        throw new Error('Invalid or expired token');
    }
    
    return { user, supabase };
};

serve(async (req) => {
    // Handle CORS preflight
    if (req.method === 'OPTIONS') {
        return new Response('ok', { headers: corsHeaders });
    }
    
    try {
        const { user, supabase } = await validateRequest(req);
        const body: RequestBody = await req.json();
        
        // Process based on action
        switch (body.action) {
            case 'send_email':
                // Process email
                break;
            case 'generate_report':
                // Generate report
                break;
            default:
                throw new Error('Invalid action');
        }
        
        return new Response(
            JSON.stringify({ success: true }),
            {
                headers: { ...corsHeaders, 'Content-Type': 'application/json' },
                status: 200
            }
        );
    } catch (error) {
        return new Response(
            JSON.stringify({ error: error.message }),
            {
                headers: { ...corsHeaders, 'Content-Type': 'application/json' },
                status: error.message === 'Invalid or expired token' ? 401 : 400
            }
        );
    }
});
```

### 6.2. Database Operations in Edge Functions

```typescript
// ✅ Good: Efficient database operations in Edge Functions
serve(async (req) => {
    try {
        const { user, supabase } = await validateRequest(req);
        
        // Batch fetch related data
        const { data: posts, error: postsError } = await supabase
            .from('posts')
            .select(`
                *,
                author:profiles!inner(id, name, avatar_url),
                comments(count)
            `)
            .eq('published', true)
            .order('created_at', { ascending: false })
            .limit(20);
        
        if (postsError) throw postsError;
        
        // Perform complex operations
        const enrichedPosts = await Promise.all(
            posts.map(async (post) => {
                const { data: likes } = await supabase
                    .from('likes')
                    .select('user_id')
                    .eq('post_id', post.id)
                    .eq('user_id', user.id);
                
                return {
                    ...post,
                    is_liked: likes.length > 0
                };
            })
        );
        
        return new Response(
            JSON.stringify({ data: enrichedPosts }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        );
    } catch (error) {
        return new Response(
            JSON.stringify({ error: error.message }),
            { status: 500 }
        );
    }
});
```

---

## 7. Realtime Best Practices

### 7.1. Efficient Subscriptions

```typescript
// ✅ Good: Reuse channel subscriptions
const useRealtime = (roomId: string) => {
    const [messages, setMessages] = useState<Message[]>([]);
    
    useEffect(() => {
        const channel = supabase
            .channel(`room-${roomId}`)
            .on(
                'postgres_changes',
                {
                    event: 'INSERT',
                    schema: 'public',
                    table: 'messages',
                    filter: `room_id=eq.${roomId}`
                },
                (payload) => {
                    setMessages((prev) => [...prev, payload.new as Message]);
                }
            )
            .on(
                'postgres_changes',
                {
                    event: 'UPDATE',
                    schema: 'public',
                    table: 'messages',
                    filter: `room_id=eq.${roomId}`
                },
                (payload) => {
                    setMessages((prev) =>
                        prev.map((msg) =>
                            msg.id === payload.new.id ? payload.new as Message : msg
                        )
                    );
                }
            )
            .on(
                'postgres_changes',
                {
                    event: 'DELETE',
                    schema: 'public',
                    table: 'messages',
                    filter: `room_id=eq.${roomId}`
                },
                (payload) => {
                    setMessages((prev) =>
                        prev.filter((msg) => msg.id !== payload.old.id)
                    );
                }
            )
            .subscribe();
        
        return () => {
            supabase.removeChannel(channel);
        };
    }, [roomId]);
    
    return messages;
};

// ✅ Good: Presence for online status
const useOnlineUsers = (roomId: string) => {
    const [onlineUsers, setOnlineUsers] = useState<any[]>([]);
    
    useEffect(() => {
        const channel = supabase.channel(`presence-${roomId}`);
        
        channel
            .on('presence', { event: 'sync' }, () => {
                const state = channel.presenceState();
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
                    await channel.track({
                        user_id: currentUser.id,
                        online_at: new Date().toISOString()
                    });
                }
            });
        
        return () => {
            supabase.removeChannel(channel);
        };
    }, [roomId]);
    
    return onlineUsers;
};

// ❌ Bad: Creating new subscription on every render
// ❌ Bad: Not cleaning up subscriptions on unmount
// ❌ Bad: Subscribing to all changes when filtered subscription is possible
```

---

## 8. Error Handling Best Practices

### 8.1. Centralized Error Handling

```typescript
// ✅ Good: Custom error class
export class AppError extends Error {
    constructor(
        message: string,
        public code: string,
        public statusCode: number = 400,
        public details?: Record<string, unknown>
    ) {
        super(message);
        this.name = 'AppError';
    }
}

// ✅ Good: Error handling utility
export const handleSupabaseError = (error: any): AppError => {
    if (!error) {
        return new AppError('Unknown error', 'UNKNOWN_ERROR', 500);
    }
    
    if (error.code === 'PGRST301') {
        return new AppError(
            'RLS policy violation',
            'ACCESS_DENIED',
            403
        );
    }
    
    if (error.code === '23505') {
        return new AppError(
            'Duplicate entry',
            'DUPLICATE_KEY',
            409
        );
    }
    
    if (error.code === '22P02') {
        return new AppError(
            'Invalid UUID format',
            'INVALID_UUID',
            400
        );
    }
    
    if (error.message?.includes('JWT')) {
        return new AppError(
            'Authentication required',
            'AUTH_REQUIRED',
            401
        );
    }
    
    return new AppError(
        error.message || 'Database error',
        'DATABASE_ERROR',
        500
    );
};

// ✅ Good: API wrapper with error handling
export const api = {
    async getUser(id: string) {
        try {
            const { data, error } = await supabase
                .from('users')
                .select('*')
                .eq('id', id)
                .single();
            
            if (error) throw handleSupabaseError(error);
            return data;
        } catch (e) {
            if (e instanceof AppError) throw e;
            throw new AppError('Failed to fetch user', 'FETCH_ERROR', 500);
        }
    },
    
    async createPost(post: NewPost) {
        try {
            const { data, error } = await supabase
                .from('posts')
                .insert(post)
                .select()
                .single();
            
            if (error) throw handleSupabaseError(error);
            return data;
        } catch (e) {
            if (e instanceof AppError) throw e;
            throw new AppError('Failed to create post', 'CREATE_ERROR', 500);
        }
    }
};
```

---

## 9. Performance Best Practices

### 9.1. Database Performance

```typescript
// ✅ Good: Use RPC for complex queries
// In database:
CREATE OR REPLACE FUNCTION get_user_feed(
    p_user_id UUID,
    p_limit INT DEFAULT 20,
    p_offset INT DEFAULT 0
)
RETURNS TABLE (
    id UUID,
    title TEXT,
    content TEXT,
    created_at TIMESTAMPTZ,
    author_name TEXT,
    like_count BIGINT,
    comment_count BIGINT,
    is_liked BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        p.title,
        p.content,
        p.created_at,
        pr.name as author_name,
        COALESCE(l.like_count, 0)::BIGINT as like_count,
        COALESCE(c.comment_count, 0)::BIGINT as comment_count,
        EXISTS (
            SELECT 1 FROM likes l2 
            WHERE l2.post_id = p.id AND l2.user_id = p_user_id
        ) as is_liked
    FROM posts p
    JOIN profiles pr ON p.user_id = pr.id
    LEFT JOIN (
        SELECT post_id, COUNT(*) as like_count
        FROM likes
        GROUP BY post_id
    ) l ON p.id = l.post_id
    LEFT JOIN (
        SELECT post_id, COUNT(*) as comment_count
        FROM comments
        GROUP BY post_id
    ) c ON p.id = c.post_id
    WHERE p.published = true
    ORDER BY p.created_at DESC
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

// In client:
const fetchFeed = async (userId: string, page = 0) => {
    const { data, error } = await supabase.rpc('get_user_feed', {
        p_user_id: userId,
        p_limit: 20,
        p_offset: page * 20
    });
    
    if (error) throw error;
    return data;
};

// ✅ Good: Optimize with EXPLAIN
// Run in SQL Editor:
EXPLAIN ANALYZE
SELECT p.*, u.name as author_name
FROM posts p
JOIN users u ON p.user_id = u.id
WHERE p.published = true
ORDER BY p.created_at DESC
LIMIT 20;

// ✅ Good: Use connection pooling
// For server-side, use service role key for better connection pooling
const supabaseAdmin = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
);
```

### 9.2. Client-Side Performance

```typescript
// ✅ Good: Memoize queries
const usePosts = (userId: string) => {
    return useMemo(() => {
        return supabase
            .from('posts')
            .select('*')
            .eq('user_id', userId)
            .order('created_at', { ascending: false });
    }, [userId]);
};

// ✅ Good: Debounce search queries
const useDebouncedQuery = (searchTerm: string, delay = 300) => {
    const [debouncedTerm, setDebouncedTerm] = useState(searchTerm);
    
    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedTerm(searchTerm);
        }, delay);
        
        return () => clearTimeout(timer);
    }, [searchTerm, delay]);
    
    return debouncedTerm;
};

// ✅ Good: Lazy load data
const useLazyLoadPosts = () => {
    const [posts, setPosts] = useState<Post[]>([]);
    const [loading, setLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    
    const loadMore = async () => {
        if (loading || !hasMore) return;
        
        setLoading(true);
        const { data, error } = await supabase
            .from('posts')
            .select('*')
            .order('created_at', { ascending: false })
            .range(posts.length, posts.length + 20);
        
        if (error) {
            console.error(error);
            setLoading(false);
            return;
        }
        
        if (data.length === 0) {
            setHasMore(false);
        } else {
            setPosts([...posts, ...data]);
        }
        
        setLoading(false);
    };
    
    return { posts, loading, hasMore, loadMore };
};
```

---

## 10. Type Safety Best Practices

### 10.1. TypeScript Types

```typescript
// ✅ Good: Define database types
export type Json =
    | string
    | number
    | boolean
    | null
    | { [key: string]: Json | undefined }
    | Json[];

export interface Database {
    public: {
        Tables: {
            profiles: {
                Row: {
                    id: string;
                    email: string | null;
                    full_name: string | null;
                    avatar_url: string | null;
                    created_at: string;
                    updated_at: string;
                };
                Insert: {
                    id: string;
                    email?: string | null;
                    full_name?: string | null;
                    avatar_url?: string | null;
                    created_at?: string;
                    updated_at?: string;
                };
                Update: {
                    email?: string | null;
                    full_name?: string | null;
                    avatar_url?: string | null;
                    updated_at?: string;
                };
            };
            posts: {
                Row: {
                    id: string;
                    user_id: string;
                    title: string;
                    content: string | null;
                    published: boolean;
                    created_at: string;
                    updated_at: string;
                };
                Insert: {
                    id?: string;
                    user_id: string;
                    title: string;
                    content?: string | null;
                    published?: boolean;
                    created_at?: string;
                    updated_at?: string;
                };
                Update: {
                    title?: string;
                    content?: string | null;
                    published?: boolean;
                    updated_at?: string;
                };
            };
        };
    };
}

// ✅ Good: Create typed client
import { createClient } from '@supabase/supabase-js';

const supabase = createClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// Usage
const { data: profile } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', userId)
    .single();

// profile is now typed as Database['public']['Tables']['profiles']['Row']
```

### 10.2. Type Generation

```bash
# ✅ Good: Generate types from database schema
supabase gen types typescript --project-id your-project-ref > types/supabase.ts

# Or using npx
npx supabase gen types typescript --project-id your-project-ref > types/database.ts
```

```typescript
// ✅ Good: Use generated types
import { Database } from '@/types/database';

type Profile = Database['public']['Tables']['profiles']['Row'];
type NewProfile = Database['public']['Tables']['profiles']['Insert'];
type UpdateProfile = Database['public']['Tables']['profiles']['Update'];

// Use in functions
const updateProfile = async (id: string, data: UpdateProfile): Promise<Profile> => {
    const { data: result, error } = await supabase
        .from('profiles')
        .update(data)
        .eq('id', id)
        .select()
        .single();
    
    if (error) throw error;
    return result;
};
```
