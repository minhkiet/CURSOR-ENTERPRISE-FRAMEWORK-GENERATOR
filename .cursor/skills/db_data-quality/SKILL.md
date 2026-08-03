---
description: Data quality and database skill covering data validation, integrity, database schema design, migrations, and query optimization. Ensures data correctness and reliability.
version: 1.0.0
created: 2026-08-03
tags: [data, database, validation, integrity, schema, migration, query, sql, nosql]
role: mandatory
domains: [data, database, backend, infrastructure]
confidence:
  base: 0.75
  threshold: 0.75
  auto_select: true
triggers:
  - "data"
  - "database"
  - "schema"
  - "migration"
  - "validation"
  - "integrity"
  - "sql"
  - "query"
  - "orm"
  - "prisma"
  - "drizzle"
  - "supabase"
  - "postgresql"
  - "mysql"
  - "mongodb"
  - "redis"
  - "index"
  - "foreign key"
  - "relationship"
  - "transaction"
  - "dữ liệu"
  - "cơ sở dữ liệu"
  - "xác thực"
---

# Data Quality & Database Skill

## Overview

Ensures data correctness, integrity, and reliability through systematic validation, schema design, and query optimization.

## Data Validation

### 1. Input Validation Layers

| Layer | Purpose | Example |
|-------|---------|---------|
| Client | UX | Real-time feedback |
| API | Security | Sanitization |
| Service | Business | Rules |
| Database | Integrity | Constraints |

### 2. Validation Patterns

**Schema Validation**
```javascript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.number().int().min(0).max(150).optional(),
  createdAt: z.date().default(() => new Date())
});

const validateUser = (data) => UserSchema.parse(data);
```

**Business Rule Validation**
```javascript
const validateOrder = (order) => {
  const errors = [];
  
  if (order.total < 0) {
    errors.push('Total cannot be negative');
  }
  
  if (order.items.length === 0) {
    errors.push('Order must have at least one item');
  }
  
  const maxDiscount = order.subtotal * 0.5;
  if (order.discount > maxDiscount) {
    errors.push('Discount exceeds maximum allowed');
  }
  
  return { valid: errors.length === 0, errors };
};
```

## Database Schema Design

### 1. Naming Conventions

| Object | Convention | Example |
|--------|------------|---------|
| Table | snake_case, plural | `user_accounts` |
| Column | snake_case | `created_at` |
| Primary Key | `id` | `id UUID PK` |
| Foreign Key | `table_singular_id` | `user_id` |
| Index | `idx_table_column` | `idx_orders_user_id` |
| Unique | `uq_table_columns` | `uq_users_email` |

### 2. Schema Patterns

**Soft Delete**
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  deleted_at TIMESTAMP NULL,
  CONSTRAINT fk_user_deleted CHECK (deleted_at IS NULL OR deleted_at > created_at)
);

CREATE INDEX idx_users_active ON users (email) WHERE deleted_at IS NULL;
```

**Audit Trail**
```sql
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  table_name VARCHAR(100) NOT NULL,
  record_id UUID NOT NULL,
  action VARCHAR(20) NOT NULL,
  old_data JSONB,
  new_data JSONB,
  changed_by UUID REFERENCES users(id),
  changed_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_table_record ON audit_log (table_name, record_id);
```

## Migrations

### 1. Migration Best Practices

```sql
-- Safe migration template
BEGIN;

-- Step 1: Add nullable column
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Step 2: Backfill data
UPDATE users SET phone = 'unknown' WHERE phone IS NULL;

-- Step 3: Add NOT NULL constraint
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;

-- Step 4: Add index
CREATE INDEX idx_users_phone ON users (phone);

COMMIT;
```

### 2. Rollback Strategy

```javascript
// Drizzle migration with rollback
export async function up(db) {
  await db.schema.alterTable('users', (table) => {
    table.addColumn('phone', 'varchar', { length: 20, notNull: true });
  });
  
  await db.execute(sql`UPDATE users SET phone = 'unknown' WHERE phone IS NULL`);
}

export async function down(db) {
  await db.schema.alterTable('users', (table) => {
    table.dropColumn('phone');
  });
}
```

## Query Optimization

### 1. Indexing Strategy

```sql
-- Composite index for common query
CREATE INDEX idx_orders_user_status_date 
  ON orders (user_id, status, created_at);

-- Partial index for active records
CREATE INDEX idx_products_active 
  ON products (category, price) 
  WHERE deleted_at IS NULL;

-- GIN index for JSON queries
CREATE INDEX idx_metadata ON events USING GIN (metadata jsonb_path_ops);
```

### 2. Query Patterns

**Avoid N+1**
```javascript
// Bad: N+1 query
const users = await db.select().from(usersTable);
for (const user of users) {
  user.posts = await db.select().from(postsTable).where(eq(postsTable.userId, user.id));
}

// Good: Join
const usersWithPosts = await db
  .select({
    user: usersTable,
    posts: postsTable
  })
  .from(usersTable)
  .leftJoin(postsTable, eq(postsTable.userId, usersTable.id));
```

**Pagination**
```javascript
// Cursor-based pagination
const getUsers = async (cursor, limit = 20) => {
  const query = db.select().from(usersTable)
    .orderBy(usersTable.id)
    .limit(limit + 1);
  
  if (cursor) {
    query.where(gte(usersTable.id, cursor));
  }
  
  const results = await query;
  const hasMore = results.length > limit;
  const items = hasMore ? results.slice(0, -1) : results;
  
  return {
    items,
    nextCursor: hasMore ? items[items.length - 1].id : null
  };
};
```

## Data Integrity

### 1. Constraints

```sql
-- Check constraints
ALTER TABLE orders 
  ADD CONSTRAINT chk_order_total 
  CHECK (total >= 0 AND total <= subtotal + tax);

-- Exclusion constraints (no overlapping bookings)
ALTER TABLE bookings
  ADD CONSTRAINT no_overlap
  EXCLUDE USING gist (
    room_id WITH =,
    daterange(start_date, end_date) WITH &&
  );
```

### 2. Transactions

```javascript
const transferFunds = async (fromId, toId, amount) => {
  return db.transaction(async (tx) => {
    const from = await tx.select()
      .from(accounts)
      .where(eq(accounts.id, fromId))
      .forUpdate();
    
    if (from.balance < amount) {
      throw new Error('Insufficient funds');
    }
    
    await tx.update(accounts)
      .set({ balance: from.balance - amount })
      .where(eq(accounts.id, fromId));
    
    await tx.update(accounts)
      .set({ balance: sql`balance + ${amount}` })
      .where(eq(accounts.id, toId));
    
    return { success: true };
  });
};
```

## Quality Gates

### Pre-Migration (§D.1)
- [ ] Backup created
- [ ] Migration tested on staging
- [ ] Rollback plan ready
- [ ] Lock duration estimated

### Post-Migration (§D.2)
- [ ] Data integrity verified
- [ ] Index usage confirmed
- [ ] Query performance acceptable
- [ ] No regression in app

## Anti-Patterns to Reject

- Missing foreign keys
- No indexes on large tables
- Storing JSON in text fields
- No soft delete pattern
- N+1 queries
- Missing pagination
- Unvalidated input
- No backup before migration
