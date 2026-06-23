# RLS Architecture - Kiến Trúc Row Level Security

## Tổng quan

RLS (Row Level Security) là PostgreSQL feature cho phép row-level access control. Policies determine which rows visible to which users.

## Kiến trúc chi tiết

### 1. Policy Structure

```sql
CREATE POLICY policy_name ON table_name
FOR operation
USING (condition);
```

### 2. Auth Integration

- auth.uid() returns user ID
- auth.jwt() returns JWT claims
- Service role bypasses RLS

### 3. Types of Policies

- SELECT: Read access
- INSERT: Write access
- UPDATE: Update access
- DELETE: Delete access

## Kết luận

RLS provides fine-grained access control at database level.
