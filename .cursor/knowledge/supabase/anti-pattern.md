# Supabase Anti-Patterns - Các Mẫu Cần Tránh

## Anti-Patterns

### 1. No RLS

**Mô tả**: Không enable Row Level Security.

**Giải pháp**: Always enable RLS.

### 2. Overusing Realtime

**Mô tả**: Subscribe to too much data.

**Giải pháp**: Filter subscriptions.

### 3. No API Keys

**Mô tả**: Expose service role key.

**Giải pháp**: Use anon key for client.

## Kết luận

Tránh các anti-patterns này giúp Supabase usage tốt hơn.
