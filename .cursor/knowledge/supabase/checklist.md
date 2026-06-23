# Supabase Checklist - Danh Sách Kiểm Tra

## Giới thiệu

Danh sách kiểm tra toàn diện cho việc triển khai và quản lý Supabase trong môi trường enterprise. Sử dụng danh sách này để đảm bảo best practices được tuân thủ.

---

## 1. Project Setup Checklist

### 1.1. Initial Setup

- [ ] Create Supabase project in dashboard
- [ ] Configure project settings:
  - [ ] Set project name
  - [ ] Configure region (closest to users)
  - [ ] Set up team members and roles
- [ ] Install Supabase CLI
  ```bash
  npm install -g supabase
  ```
- [ ] Initialize Supabase in project
  ```bash
  supabase init
  ```
- [ ] Link to remote project
  ```bash
  supabase link --project-ref your-project-ref
  ```
- [ ] Pull existing schema
  ```bash
  supabase db pull
  ```
- [ ] Configure environment variables
  ```bash
  # .env.local
  NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
  NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx
  ```

### 1.2. Database Setup

- [ ] Review default schema
- [ ] Create custom schema structure
  ```sql
  CREATE SCHEMA IF NOT EXISTS public;
  ```
- [ ] Install required extensions
  ```sql
  CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
  CREATE EXTENSION IF NOT EXISTS "pg_trgm";
  CREATE EXTENSION IF NOT EXISTS "vector";
  ```
- [ ] Set up proper permissions
  ```sql
  GRANT USAGE ON SCHEMA public TO authenticated;
  GRANT USAGE ON SCHEMA public TO anon;
  GRANT ALL ON SCHEMA public TO postgres;
  ```

---

## 2. Security Checklist

### 2.1. Row Level Security (RLS)

- [ ] Enable RLS on all user tables
  ```sql
  ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
  ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;
  ALTER TABLE public.comments ENABLE ROW LEVEL SECURITY;
  ```
- [ ] Create policies for each table:
  - [ ] SELECT policies
  - [ ] INSERT policies
  - [ ] UPDATE policies
  - [ ] DELETE policies
- [ ] Test policies with different user roles
- [ ] Document all RLS policies

### 2.2. Authentication

- [ ] Configure authentication providers:
  - [ ] Email/Password enabled
  - [ ] OAuth providers (if needed)
  - [ ] Magic link enabled
  - [ ] Phone auth (if needed)
- [ ] Set up email templates:
  - [ ] Confirmation email
  - [ ] Reset password email
  - [ ] Custom branding
- [ ] Configure redirect URLs:
  - [ ] Development URLs
  - [ ] Production URLs
- [ ] Implement auth callbacks
  ```typescript
  // Auth callback handler
  supabase.auth.getSessionFromUrl({
    storeSession: true
  });
  ```
- [ ] Set up session management:
  - [ ] Session persistence
  - [ ] Token refresh
  - [ ] Logout handling

### 2.3. API Security

- [ ] Rotate initial keys if exposed
- [ ] Use environment variables for keys
- [ ] Never expose service role key in client code
- [ ] Implement proper CORS settings
- [ ] Set up rate limiting (if needed)
- [ ] Use Edge Functions for sensitive operations

---

## 3. Database Design Checklist

### 3.1. Schema Design

- [ ] Use UUID for primary keys
  ```sql
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4()
  ```
- [ ] Set up foreign key relationships
  ```sql
  FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
  ```
- [ ] Add proper indexes
  ```sql
  CREATE INDEX idx_posts_user_id ON posts(user_id);
  CREATE INDEX idx_posts_published ON posts(published) WHERE published = true;
  ```
- [ ] Use appropriate data types:
  - [ ] TEXT instead of VARCHAR(n)
  - [ ] DECIMAL for money (not FLOAT)
  - [ ] TIMESTAMPTZ for timestamps
  - [ ] JSONB for flexible data
- [ ] Add constraints where needed
  ```sql
  CONSTRAINT positive_price CHECK (price >= 0)
  ```

### 3.2. Triggers and Functions

- [ ] Create auto-create profile trigger
  ```sql
  CREATE OR REPLACE FUNCTION handle_new_user()
  RETURNS TRIGGER AS $$
  BEGIN
      INSERT INTO public.profiles (id, email)
      VALUES (NEW.id, NEW.email);
      RETURN NEW;
  END;
  $$ LANGUAGE plpgsql SECURITY DEFINER;

  CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();
  ```
- [ ] Add updated_at triggers
  ```sql
  CREATE OR REPLACE FUNCTION update_updated_at()
  RETURNS TRIGGER AS $$
  BEGIN
      NEW.updated_at = NOW();
      RETURN NEW;
  END;
  $$ LANGUAGE plpgsql;

  CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
  ```
- [ ] Document all database functions
- [ ] Test triggers thoroughly

### 3.3. Migrations

- [ ] Use migration files for all schema changes
  ```bash
  supabase db diff > migrations/xxx_add_table.sql
  ```
- [ ] Version control migration files
- [ ] Test migrations locally
  ```bash
  supabase db reset
  ```
- [ ] Review migrations before applying
- [ ] Have rollback plan

---

## 4. Storage Checklist

### 4.1. Bucket Setup

- [ ] Create storage buckets:
  - [ ] Avatars (public)
  - [ ] Posts/Images (public)
  - [ ] Documents (private)
  - [ ] Backups (private)
- [ ] Configure bucket settings:
  - [ ] File size limits
  - [ ] Allowed MIME types
  - [ ] Public/Private access
  ```sql
  INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
  VALUES 
      ('avatars', 'avatars', true, 5242880, ARRAY['image/jpeg', 'image/png']),
      ('documents', 'documents', false, 104857600, ARRAY['application/pdf']);
  ```
- [ ] Set up storage policies:
  - [ ] Upload policies
  - [ ] Download policies
  - [ ] Delete policies
  - [ ] Update policies

### 4.2. Storage Implementation

- [ ] Implement file upload with validation
  ```typescript
  const uploadAvatar = async (file: File) => {
      const { data, error } = await supabase.storage
          .from('avatars')
          .upload(`${userId}/avatar.jpg`, file, {
              cacheControl: '3600',
              upsert: true
          });
  };
  ```
- [ ] Implement file download
- [ ] Implement signed URLs for private files
  ```typescript
  const { data } = await supabase.storage
      .from('documents')
      .createSignedUrl(path, 3600);
  ```
- [ ] Set up CDN (if using custom domain)
- [ ] Configure image transformations

---

## 5. Edge Functions Checklist

### 5.1. Development Setup

- [ ] Initialize Edge Functions
  ```bash
  supabase functions new function-name
  ```
- [ ] Set up local development
  ```bash
  supabase start
  ```
- [ ] Test functions locally
  ```bash
  supabase functions serve function-name
  ```
- [ ] Configure secrets
  ```bash
  supabase secrets set STRIPE_SECRET_KEY=xxx
  ```

### 5.2. Function Security

- [ ] Implement JWT verification
  ```typescript
  const authHeader = req.headers.get('Authorization');
  if (!authHeader) {
      throw new Error('Unauthorized');
  }
  ```
- [ ] Validate all inputs
- [ ] Implement proper error handling
- [ ] Set CORS headers
  ```typescript
  const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'authorization, apikey, content-type',
  };
  ```
- [ ] Log all operations
- [ ] Never expose sensitive data in responses

### 5.3. Function Deployment

- [ ] Deploy function
  ```bash
  supabase functions deploy function-name
  ```
- [ ] Set environment secrets
  - [ ] API keys
  - [ ] Database URLs
  - [ ] Other secrets
- [ ] Monitor function logs
  ```bash
  supabase functions logs function-name
  ```
- [ ] Set up alerting for errors

---

## 6. Realtime Checklist

### 6.1. Configuration

- [ ] Enable realtime for required tables
  ```sql
  ALTER PUBLICATION supabase_realtime ADD TABLE messages;
  ```
- [ ] Configure realtime settings in dashboard
- [ ] Test connection status

### 6.2. Implementation

- [ ] Implement proper subscription management
  ```typescript
  const channel = supabase
      .channel('table-db-changes')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'messages' }, handleChange)
      .subscribe();

  // Cleanup on unmount
  return () => supabase.removeChannel(channel);
  ```
- [ ] Filter subscriptions efficiently
  ```typescript
  .on('postgres_changes', { event: 'INSERT', table: 'messages', filter: 'room_id=eq.123' })
  ```
- [ ] Handle connection states
- [ ] Implement reconnection logic
- [ ] Test with multiple simultaneous connections

### 6.3. Presence (if needed)

- [ ] Implement presence tracking
  ```typescript
  channel.on('presence', { event: 'sync' }, () => {
      const state = channel.presenceState();
  });
  ```
- [ ] Handle join/leave events
- [ ] Set up presence cleanup

---

## 7. Performance Checklist

### 7.1. Database Performance

- [ ] Create appropriate indexes:
  - [ ] Index foreign keys
  - [ ] Index frequently queried columns
  - [ ] Create composite indexes for common queries
  - [ ] Use partial indexes for filtered queries
- [ ] Optimize queries:
  - [ ] Avoid SELECT *
  - [ ] Use EXPLAIN to analyze queries
  - [ ] Use covering indexes
  - [ ] Optimize JOINs
- [ ] Implement pagination
  ```typescript
  .range(0, 9) // First 10
  .range(10, 19) // Next 10
  ```
- [ ] Monitor query performance
- [ ] Review slow query logs

### 7.2. Client Performance

- [ ] Implement proper loading states
- [ ] Use React Query/SWR for data fetching
- [ ] Memoize expensive computations
- [ ] Implement optimistic updates
- [ ] Debounce search inputs
- [ ] Lazy load non-critical data

### 7.3. Connection Pooling

- [ ] Configure connection pool settings
- [ ] Monitor connection usage
- [ ] Handle connection errors gracefully

---

## 8. Monitoring and Logging Checklist

### 8.1. Database Monitoring

- [ ] Enable query logging
  ```sql
  ALTER DATABASE postgres SET log_statement = 'all';
  ```
- [ ] Monitor slow queries
- [ ] Track index usage
- [ ] Monitor table sizes
  ```sql
  SELECT 
      schemaname,
      tablename,
      pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
  FROM pg_tables
  WHERE schemaname = 'public'
  ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
  ```
- [ ] Set up pg_stat_statements
  ```sql
  CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
  ```

### 8.2. Application Monitoring

- [ ] Set up error tracking (Sentry, etc.)
- [ ] Log all database operations
- [ ] Monitor Edge Function execution
- [ ] Set up alerting for errors
- [ ] Track user authentication events

### 8.3. Infrastructure Monitoring

- [ ] Monitor disk usage
- [ ] Monitor database connections
- [ ] Monitor storage usage
- [ ] Set up usage alerts

---

## 9. Backup and Recovery Checklist

### 9.1. Backup Configuration

- [ ] Configure database backups:
  - [ ] Point-in-time recovery enabled
  - [ ] Backup schedule configured
  - [ ] Backup retention period set
- [ ] Configure storage backups
- [ ] Test backup restoration

### 9.2. Recovery Plan

- [ ] Document recovery procedures
- [ ] Test point-in-time recovery
- [ ] Document RTO and RPO
- [ ] Have runbook for common scenarios

---

## 10. Deployment Checklist

### 10.1. Pre-Deployment

- [ ] Test all changes locally
  ```bash
  supabase db reset
  ```
- [ ] Run all migrations
  ```bash
  supabase db push
  ```
- [ ] Verify environment variables
- [ ] Check all API keys are correct
- [ ] Review security settings
- [ ] Document changes

### 10.2. Deployment

- [ ] Deploy to staging first
- [ ] Run integration tests
- [ ] Deploy to production
  ```bash
  supabase db push --project-ref production-ref
  supabase functions deploy --project-ref production-ref
  ```
- [ ] Monitor for errors
- [ ] Verify all features work

### 10.3. Post-Deployment

- [ ] Monitor error rates
- [ ] Verify database operations
- [ ] Check Edge Function logs
- [ ] Verify realtime connections
- [ ] Document deployment

---

## 11. TypeScript Checklist

### 11.1. Type Generation

- [ ] Generate TypeScript types
  ```bash
  supabase gen types typescript --project-id your-ref > types/supabase.ts
  ```
- [ ] Update types after schema changes
- [ ] Use strict typing

### 11.2. Client Setup

- [ ] Create typed client
  ```typescript
  import { createClient } from '@supabase/supabase-js';
  import type { Database } from '@/types/database';

  const supabase = createClient<Database>(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
  ```
- [ ] Create admin client for server-side
  ```typescript
  const supabaseAdmin = createClient<Database>(
      process.env.SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
  );
  ```

---

## 12. Testing Checklist

### 12.1. Unit Tests

- [ ] Test database functions
- [ ] Test Edge Functions
- [ ] Test auth flows
- [ ] Test RLS policies

### 12.2. Integration Tests

- [ ] Test API endpoints
- [ ] Test realtime subscriptions
- [ ] Test storage operations
- [ ] Test with different user roles

### 12.3. E2E Tests

- [ ] Test complete user flows
- [ ] Test authentication flows
- [ ] Test payment flows (if applicable)
- [ ] Test error scenarios

---

## 13. Documentation Checklist

### 13.1. Required Documentation

- [ ] API documentation
- [ ] Database schema documentation
- [ ] Authentication flow documentation
- [ ] Storage bucket documentation
- [ ] Edge Functions documentation
- [ ] Deployment procedures
- [ ] Rollback procedures
- [ ] Security policies

### 13.2. Team Documentation

- [ ] Onboarding guide
- [ ] Code style guide
- [ ] Best practices guide
- [ ] Troubleshooting guide
- [ ] Contact list

---

## 14. Compliance Checklist

### 14.1. Data Protection

- [ ] Classify data sensitivity
- [ ] Implement data masking (if needed)
- [ ] Enable encryption at rest
- [ ] Enable encryption in transit
- [ ] Implement data retention policies

### 14.2. Privacy

- [ ] Implement GDPR compliance (if applicable)
- [ ] Add privacy policy
- [ ] Implement data deletion procedures
- [ ] Audit data access

---

## 15. Optimization Checklist

### 15.1. Query Optimization

- [ ] Run EXPLAIN on slow queries
- [ ] Add missing indexes
- [ ] Remove unused indexes
- [ ] Optimize JOINs
- [ ] Use connection pooling

### 15.2. Storage Optimization

- [ ] Compress images before upload
- [ ] Use appropriate image formats
- [ ] Implement lazy loading for images
- [ ] Clean up old files regularly

### 15.3. Edge Functions Optimization

- [ ] Minimize cold start times
- [ ] Use efficient algorithms
- [ ] Cache responses where appropriate
- [ ] Monitor execution times
