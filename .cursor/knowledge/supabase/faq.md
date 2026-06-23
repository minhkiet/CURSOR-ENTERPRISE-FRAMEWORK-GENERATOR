# Supabase FAQ - Câu Hỏi Thường Gặp

## Câu Hỏi Cơ Bản

### 1. Supabase là gì?

Supabase là open-source Firebase alternative. Cung cấp PostgreSQL database, authentication, realtime subscriptions, storage, edge functions.

### 2. Supabase khác Firebase như thế nào?

Supabase dựa trên PostgreSQL (SQL), mã nguồn mở, self-hostable. Firebase dựa trên NoSQL (Firestore), proprietary.

### 3. RLS là gì?

Row Level Security là PostgreSQL feature cho phép row-level access control. Supabase tích hợp RLS với authentication.

## Câu Hỏi Kỹ Thuật

### 4. Realtime hoạt động như thế nào?

Supabase lắng nghe PostgreSQL changes và broadcast qua WebSocket. Subscribe to table changes với realtime().

### 5. Auth được implement như thế nào?

Supabase Auth cung cấp email/password, OAuth. JWT tokens cho API authentication. RLS integration.
