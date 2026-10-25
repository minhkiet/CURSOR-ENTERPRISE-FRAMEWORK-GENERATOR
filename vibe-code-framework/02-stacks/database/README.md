# Database Stack

> **Version:** 1.0.0 | **Databases:** PostgreSQL, MySQL

---

## Database Patterns

### PostgreSQL Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Table name | snake_case, plural | `user_accounts` |
| Column name | snake_case | `created_at` |
| Primary key | `id UUID` | `id UUID DEFAULT gen_random_uuid()` |
| Index name | `idx_{table}_{columns}` | `idx_users_email` |
| Foreign key | `fk_{table}_{ref}` | `fk_orders_users` |

### MySQL Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Table name | snake_case, plural | `user_accounts` |
| Column name | snake_case | `created_at` |
| Primary key | `id` | `id CHAR(36) PRIMARY KEY` |
| Index name | `idx_{table}_{columns}` | `idx_users_email` |

---

## Schema Pattern

```sql
-- PostgreSQL
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(100) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  deleted_at TIMESTAMP WITH TIME ZONE
);

-- Indexes
CREATE UNIQUE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_created_at ON users(created_at DESC);
```

---

## Migration Pattern

```sql
-- migrations/20260115_001_create_users.sql

-- UP
BEGIN;

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(100) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);

ALTER TABLE users ADD CONSTRAINT users_status_check 
  CHECK (status IN ('active', 'inactive', 'suspended'));

COMMENT ON TABLE users IS 'User accounts';
COMMENT ON COLUMN users.id IS 'Primary key';

COMMIT;

-- DOWN
BEGIN;

ALTER TABLE users DROP CONSTRAINT IF EXISTS users_status_check;
DROP INDEX IF EXISTS idx_users_status;
DROP INDEX IF EXISTS idx_users_email;
DROP TABLE IF EXISTS users;

COMMIT;
```

---

## Query Patterns

### Safe Query with Parameterized Values

```csharp
// ❌ Never do this - SQL injection!
var sql = $"SELECT * FROM users WHERE email = '{email}'";

// ✅ Always use parameterized queries
const string sql = "SELECT * FROM users WHERE email = @Email";
var result = await connection.QuerySingleOrDefaultAsync<User>(
    new CommandDefinition(sql, new { Email = email }));
```

### Pagination

```sql
-- Offset pagination
SELECT * FROM users 
ORDER BY created_at DESC 
LIMIT 20 OFFSET 40;

-- Cursor pagination (better for large tables)
SELECT * FROM users 
WHERE created_at < @cursor
ORDER BY created_at DESC 
LIMIT 20;
```

### Soft Delete

```sql
-- Query active records
SELECT * FROM users WHERE deleted_at IS NULL;

-- Soft delete
UPDATE users SET deleted_at = NOW() WHERE id = @Id;

-- Restore
UPDATE users SET deleted_at = NULL WHERE id = @Id;
```

---

## Index Strategy

```
┌────────────────────────────────────────────────────────────┐
│ Index Decision Guide                                      │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Always Index:                                           │
│  ├── Primary keys                                       │
│  ├── Foreign keys                                       │
│  ├── Columns in WHERE with high cardinality              │
│                                                            │
│  Consider Indexing:                                      │
│  ├── Columns in ORDER BY (if frequent)                 │
│  ├── Columns in JOIN conditions                         │
│  ├── Low cardinality with combined index                │
│                                                            │
│  Avoid Indexing:                                        │
│  ├── Columns with < 1% selectivity                    │
│  ├── Frequently updated columns                         │
│  ├── Large text/blob columns                           │
│                                                            │
│  Concurrent Index (PostgreSQL):                        │
│  CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Backup Strategy

```sql
-- PostgreSQL backup
pg_dump -h localhost -U user -d database > backup.sql

-- MySQL backup
mysqldump -h localhost -u user -p database > backup.sql

-- Point-in-time recovery (PostgreSQL)
-- Configure WAL archiving in postgresql.conf:
wal_level = replica
archive_mode = on
archive_command = 'cp %p /var/lib/postgresql/backups/%f'
```

---

## Checklist

```
┌─────────────────────────────────────────────────────────────┐
│ Database Checklist                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Schema normalized to 3NF                                 │
│ □ Primary keys on all tables                              │
│ □ Timestamps (created_at, updated_at)                    │
│ □ Soft deletes where needed                               │
│ □ Proper data types (not excessive VARCHAR lengths)        │
│ □ Constraints (NOT NULL, CHECK, UNIQUE)                  │
│ □ Foreign keys with appropriate actions                   │
│ □ Indexes on query columns                               │
│ □ Concurrent indexes for large tables                     │
│ □ Parameterized queries (no SQL injection)                │
│ □ Backup strategy documented                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
