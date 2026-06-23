# Supabase Architecture - Kiến Trúc Supabase

## Tổng quan

Supabase là open-source Firebase alternative built on PostgreSQL. Kiến trúc bao gồm database, auth, realtime, storage.

## Kiến trúc chi tiết

### 1. Database

- PostgreSQL core
- PostgREST for API
- Connection pooling
- Backups

### 2. Auth

- GoTrue server
- JWT tokens
- OAuth providers
- RLS integration

### 3. Realtime

- PostgreSQL changes
- WebSocket broadcast
- Filters
- Presence

### 4. Storage

- S3-compatible
- Buckets
- CDN
- Transformations

## Kết luận

Supabase cung cấp complete backend-as-a-service.
