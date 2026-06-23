# RLS Glossary - Từ Điển Thuật Ngữ Row Level Security

## Giới thiệu

Tài liệu này cung cấp các thuật ngữ chuyên ngành Row Level Security (RLS) trong PostgreSQL.

## Các thuật ngữ cơ bản

### 1. Row Level Security (RLS)

RLS là PostgreSQL feature cho phép control access đến rows based on user characteristics. Policies được attach đến tables. Rows invisible unless policy passes.

### 2. Policy

Policy là database object xác định which rows visible to which users. CREATE POLICY statement. Policies có thể be FOR SELECT, INSERT, UPDATE, DELETE.

### 3. Authentication

RLS uses authenticated user identity. auth.uid() function returns current user ID. auth.jwt() returns JWT claims.

### 4. Bypass RLS

Tables can have RLS bypass for superusers. ALTER TABLE ... FORCE ROW LEVEL SECURITY. Service role có thể bypass RLS.

### 5. Integration

Supabase uses RLS for security. JWT tokens với user ID. anon key vs service_role key.

### 6. Best Practices

- Always enable RLS
- Create policies for all tables
- Test with anon key
- Use separate policies per operation

## Kết luận

RLS là security feature quan trọng trong PostgreSQL/Supabase.
