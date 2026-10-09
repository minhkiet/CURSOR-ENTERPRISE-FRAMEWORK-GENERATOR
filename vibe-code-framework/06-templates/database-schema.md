# Database Schema Template

> **Version:** 1.0.0 | **Database:** PostgreSQL

---

## Migration Template

```sql
-- Migration: [description]
-- Author: [author]
-- Date: [YYYY-MM-DD]
-- Ticket: [ticket-id]

-- =====================================================
-- UP MIGRATION
-- =====================================================

BEGIN;

-- Step 1: Create tables
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(100) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'user',
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  email_verified_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  deleted_at TIMESTAMP WITH TIME ZONE
);

-- Step 2: Add comments
COMMENT ON TABLE users IS 'User accounts';
COMMENT ON COLUMN users.id IS 'Primary key';
COMMENT ON COLUMN users.email IS 'Unique email address';
COMMENT ON COLUMN users.password_hash IS 'Bcrypt hashed password';
COMMENT ON COLUMN users.role IS 'User role: user, admin';
COMMENT ON COLUMN users.status IS 'Account status: active, inactive, suspended';
COMMENT ON COLUMN users.deleted_at IS 'Soft delete timestamp';

-- Step 3: Add indexes
CREATE UNIQUE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created_at ON users(created_at DESC);

-- Step 4: Add constraints
ALTER TABLE users ADD CONSTRAINT users_role_check 
  CHECK (role IN ('user', 'admin', 'moderator'));
ALTER TABLE users ADD CONSTRAINT users_status_check 
  CHECK (status IN ('active', 'inactive', 'suspended'));

-- Step 5: Add foreign keys (if referencing other tables)
-- ALTER TABLE posts ADD CONSTRAINT posts_user_id_fkey
--   FOREIGN KEY (user_id) REFERENCES users(id);

COMMIT;

-- =====================================================
-- DOWN MIGRATION
-- =====================================================

BEGIN;

-- Remove constraints
ALTER TABLE users DROP CONSTRAINT IF EXISTS users_status_check;
ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_check;

-- Remove indexes
DROP INDEX IF EXISTS idx_users_created_at;
DROP INDEX IF EXISTS idx_users_role;
DROP INDEX IF EXISTS idx_users_status;
DROP INDEX IF EXISTS idx_users_email;

-- Remove table
DROP TABLE IF EXISTS users;

COMMIT;
```

## Entity Relationship Example

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(100) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Posts table
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  content TEXT,
  published BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Comments table
CREATE TABLE comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tags table (many-to-many)
CREATE TABLE tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(50) NOT NULL UNIQUE,
  slug VARCHAR(50) NOT NULL UNIQUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Junction table
CREATE TABLE post_tags (
  post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  tag_id UUID NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (post_id, tag_id)
);

-- Indexes
CREATE UNIQUE INDEX idx_posts_slug ON posts(slug);
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_published ON posts(published) WHERE published = TRUE;
CREATE INDEX idx_comments_post_id ON comments(post_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_post_tags_tag_id ON post_tags(tag_id);
```

## Seeding Template

```sql
-- Seed data for development
INSERT INTO users (id, email, password_hash, name, role, created_at) VALUES
  ('550e8400-e29b-41d4-a716-446655440001', 'admin@example.com', '$2b$12$...', 'Admin User', 'admin', NOW()),
  ('550e8400-e29b-41d4-a716-446655440002', 'user@example.com', '$2b$12$...', 'Regular User', 'user', NOW());

-- Seed tags
INSERT INTO tags (id, name, slug) VALUES
  ('550e8400-e29b-41d4-a716-446655440010', 'Technology', 'technology'),
  ('550e8400-e29b-41d4-a716-446655440011', 'Business', 'business'),
  ('550e8400-e29b-41d4-a716-446655440012', 'Lifestyle', 'lifestyle');
```

## Rollback Template

```sql
-- Rollback script for emergency
BEGIN;

-- Check data before dropping
SELECT COUNT(*) AS user_count FROM users;
SELECT COUNT(*) AS post_count FROM posts;

-- If counts are acceptable:
DROP TABLE IF EXISTS post_tags;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS users;

COMMIT;

-- Verify tables dropped
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE';
```

## Common Patterns

### Soft Delete

```sql
-- Add deleted_at column
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE;

-- Query active records only
SELECT * FROM users WHERE deleted_at IS NULL;

-- Query soft-deleted records
SELECT * FROM users WHERE deleted_at IS NOT NULL;

-- Soft delete a record
UPDATE users SET deleted_at = NOW() WHERE id = 'xxx';

-- Restore a record
UPDATE users SET deleted_at = NULL WHERE id = 'xxx';
```

### Timestamp Triggers

```sql
-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

### JSONB Column

```sql
-- Add metadata column
ALTER TABLE users ADD COLUMN metadata JSONB DEFAULT '{}';

-- Query JSONB
SELECT * FROM users WHERE metadata @> '{"theme": "dark"}';

-- Update JSONB
UPDATE users 
SET metadata = jsonb_set(metadata, '{preferences}', '"en"')
WHERE id = 'xxx';
```

### UUID Functions

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Use uuid_generate_v4() for random UUIDs
INSERT INTO users (id, email) VALUES (uuid_generate_v4(), 'test@example.com');

-- Generate UUID from string (for seeding)
SELECT '550e8400-e29b-41d4-a716-446655440001'::uuid;
```
