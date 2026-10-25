# Database Migration Skill

> **Version:** 1.0.0 | **Category:** Database | **Triggers:** database migration, create table, alter schema, migrate

---

## Goal

Tạo và quản lý database migrations an toàn:
- Reversible migrations
- Data integrity maintained
- Zero-downtime deployments
- Proper rollback strategy

## Trigger Conditions

- User cần tạo database table mới
- User cần thay đổi schema hiện có
- User cần thêm/chỉnh sửa indexes
- User cần migrate data

## Pre-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ P.1: Schema Design                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Table structure đã được design?                        │
│ □ Relationships đã được xác định?                         │
│ □ Indexes đã được planned?                                 │
│ □ Constraints đã được define?                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ P.2: Impact Assessment                                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Migration ảnh hưởng đến bảng lớn?                      │
│ □ Cần locking?                                            │
│ □ Downtime acceptable?                                     │
│ □ Backup strategy?                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Process Steps

### Step 1: Write Migration

```sql
-- migrations/20260115_001_create_users.sql

-- Up Migration
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(100) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);

-- Down Migration
DROP INDEX IF EXISTS idx_users_status;
DROP INDEX IF EXISTS idx_users_email;
DROP TABLE IF EXISTS users;
```

### Step 2: Expand-Migrate-Contract Pattern

```
┌────────────────────────────────────────────────────────────┐
│ Expand-Migrate-Contract Pattern                             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Phase 1: EXPAND (Zero downtime)                          │
│  ├── Add new column as nullable                           │
│  ├── Deploy new code using new column                    │
│  └── Backfill data                                       │
│                                                            │
│  Phase 2: MIGRATE                                         │
│  ├── Add NOT NULL constraint                             │
│  ├── Add indexes                                         │
│  └── Add foreign keys                                    │
│                                                            │
│  Phase 3: CONTRACT (Cleanup)                              │
│  ├── Remove old columns                                 │
│  ├── Remove deprecated values                            │
│  └── Rename columns                                      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 3: Safe Alter Table

```sql
-- ❌ Dangerous - causes table rewrite
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- ✅ Safe - online operation
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- ❌ Dangerous - locks table
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;

-- ✅ Safe - requires backfill first
-- 1. Add nullable column
-- 2. Backfill data
-- 3. Add constraint in separate migration
ALTER TABLE users ADD CONSTRAINT users_phone_not_null CHECK (phone IS NOT NULL);
```

### Step 4: Create Index Safely

```sql
-- ❌ Dangerous - locks table on large table
CREATE INDEX CONCURRENTLY idx_users_phone ON users(phone);

-- ✅ Safe - concurrent index doesn't lock
CREATE INDEX CONCURRENTLY idx_users_phone ON users(phone);

-- ❌ Dangerous - locks table
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- ✅ Safe - concurrent unique index
CREATE UNIQUE INDEX CONCURRENTLY idx_users_email ON users(email);
```

### Step 5: Rollback Strategy

```sql
-- Always write down migration
-- migrations/20260115_001_create_users_down.sql

BEGIN;

-- Check if data exists before dropping
SELECT COUNT(*) FROM users WHERE status = 'deleted';
-- If count > 0, investigate before proceeding

DROP INDEX IF EXISTS idx_users_status;
DROP INDEX IF EXISTS idx_users_email;
DROP TABLE IF EXISTS users;

COMMIT;
```

## Migration Template

```sql
-- Migration: {description}
-- Author: {author}
-- Date: {date}
-- Ticket: {ticket-id}

-- =====================================================
-- UP MIGRATION
-- =====================================================

BEGIN;

-- Step 1: Create tables/columns
CREATE TABLE ...

-- Step 2: Add indexes
CREATE INDEX CONCURRENTLY ...

-- Step 3: Add constraints
ALTER TABLE ...

COMMIT;

-- =====================================================
-- DOWN MIGRATION
-- =====================================================

BEGIN;

-- Step 1: Remove constraints
ALTER TABLE ...

-- Step 2: Remove indexes
DROP INDEX ...

-- Step 3: Drop tables/columns
DROP TABLE ...

COMMIT;
```

## Post-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ C.1: Migration Quality                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Up migration tested?                                     │
│ □ Down migration tested?                                   │
│ □ Rollback strategy documented?                            │
│ □ No data loss?                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.2: Performance                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Indexes appropriate?                                     │
│ □ No table scans on large tables?                         │
│ □ Query performance acceptable?                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.3: Safety                                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Concurrent index for large tables?                       │
│ □ Backfill batched?                                       │
│ □ Locks minimized?                                         │
│ □ Alerts set?                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Checklist for Production Migration

```
□ Backup created before migration
□ Migration tested on staging
□ Rollback tested on staging
□ Monitoring/alerting configured
□ Database logs reviewed
□ Runbook prepared
□ Communication sent to stakeholders
□ Maintenance window scheduled (if needed)
□ DBA/Team approval obtained
□ Migration scheduled during low traffic
```
