---
title: PostgreSQL Security và Privileges
description: Hướng dẫn toàn diện về GRANT/REVOKE, role membership, Row-Level Security, column-level security, audit logging, và SSL connections
tags: [postgresql, security, privileges, rls, row-level-security, pgaudit, ssl, authentication]
created: 2026-06-23
version: "1.0"
framework: cursor-enterprise-framework
---

# PostgreSQL Security và Privileges

## Tổng quan

Security là một aspect quan trọng trong bất kỳ database deployment nào. PostgreSQL cung cấp một hệ thống security toàn diện bao gồm authentication, authorization, data encryption, và audit capabilities.

Trong enterprise environments, việc implement proper security measures không chỉ là best practice mà còn là requirement thường được mandate bởi compliance frameworks như SOC 2, GDPR, HIPAA, và PCI-DSS.

Tài liệu này trình bày các khía cạnh security quan trọng của PostgreSQL và cách implement chúng một cách hiệu quả.

## Mục đích

Tài liệu này nhằm mục đích:

- Giải thích PostgreSQL authentication và authorization model
- Hướng dẫn cách implement role-based access control (RBAC)
- Trình bày Row-Level Security (RLS) và use cases
- Cung cấp best practices cho audit logging
- Hướng dẫn cấu hình SSL cho encrypted connections
- Xử lý common security issues

## Các khái niệm chính

### Authentication Methods

PostgreSQL hỗ trợ nhiều authentication methods:

**Trust Authentication**:

```conf
# pg_hba.conf
# Cho phép local connections không cần password
local   all             all                                     trust

# IPv4 localhost
host    all             all             127.0.0.1/32            trust
```

**Password Authentication (MD5)**:

```conf
# pg_hba.conf
host    all             all             0.0.0.0/0               md5
```

**SCRAM-SHA-256 (Recommended)**:

```conf
# pg_hba.conf
host    all             all             0.0.0.0/0               scram-sha-256

# postgresql.conf
password_encryption = scram-sha-256
```

**Certificate Authentication (SSL)**:

```conf
# pg_hba.conf
hostssl all             all             0.0.0.0/0               cert clientcert=verify-full
```

**LDAP Authentication**:

```conf
# pg_hba.conf
host    all             all             0.0.0.0/0               ldap ldapserver=ldap.example.com ldapport=389 ldapbasedn="ou=users,dc=example,dc=com" ldapsearchfilter="(uid=$username)"
```

**GSSAPI (Kerberos)**:

```conf
# pg_hba.conf
host    all             all             0.0.0.0/0               gss include_realm=0 krb_realm=EXAMPLE.COM
```

### Role-based Access Control (RBAC)

PostgreSQL sử dụng roles để manage permissions:

```sql
-- Create roles
CREATE ROLE app_readonly;
CREATE ROLE app_writer;
CREATE ROLE app_admin;
CREATE ROLE reporting_user;

-- Role với login capability
CREATE ROLE app_service LOGIN PASSWORD 'strong_password' 
    CONNECTION LIMIT 100;

-- Role với superuser (tránh dùng cho application)
CREATE ROLE dba_superuser WITH SUPERUSER CREATEDB CREATEROLE REPLICATION 
    BYPASSRLS;
```

### GRANT và REVOKE

```sql
-- GRANT basic permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_writer;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;

-- GRANT cho specific table
GRANT SELECT, UPDATE (name, email) ON users TO app_writer;
GRANT SELECT (id, name, email) ON users TO app_readonly;

-- GRANT cho sequences (cần cho SERIAL columns)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_writer;

-- GRANT cho functions
GRANT EXECUTE ON FUNCTION calculate_total(INT, INT) TO app_service;

-- GRANT cho schemas
GRANT USAGE ON SCHEMA app_schema TO app_service;

-- REVOKE permissions
REVOKE DELETE ON orders FROM app_readonly;
REVOKE ALL ON users FROM public;  -- Remove default public access
```

### Role Membership

```sql
-- Create role groups
CREATE ROLE analysts;
CREATE ROLE developers;
CREATE ROLE operations;

-- Grant permissions to groups
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analysts;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA app TO developers;
GRANT USAGE ON SCHEMA pg TO operations;

-- Grant roles to users
CREATE ROLE alice LOGIN PASSWORD 'alice_password';
CREATE ROLE bob LOGIN PASSWORD 'bob_password';

GRANT analysts TO alice;
GRANT developers, analysts TO bob;
GRANT operations TO bob;

-- Admin role với ability to grant others
CREATE ROLE team_lead LOGIN PASSWORD 'lead_password';
GRANT analysts, developers TO team_lead;
GRANT team_lead TO alice WITH ADMIN OPTION;

-- Default roles cho new objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
    GRANT SELECT ON TABLES TO app_readonly;

ALTER DEFAULT PRIVILEGES IN SCHEMA public 
    GRANT INSERT, UPDATE, DELETE ON TABLES TO app_writer;
```

### Default Privileges

```sql
-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA app 
    GRANT SELECT ON TABLES TO app_readonly;

ALTER DEFAULT PRIVILEGES FOR ROLE app_service IN SCHEMA app 
    GRANT ALL ON TABLES TO app_admin;

-- Verify default privileges
SELECT 
    defaclrole::regrole AS role,
    defaclnamespace::regnamespace AS schema,
    nspname,
    objtype,
    privname,
    defaclobj
FROM pg_default_acl a
JOIN pg_namespace n ON n.oid = a.defaclnamespace;
```

## Row-Level Security (RLS)

RLS cho phép filter rows dựa trên policy được evaluate cho mỗi query.

### Enable RLS

```sql
-- Enable RLS on table
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Force RLS for table owner
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

-- Check RLS status
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';
```

### Create RLS Policies

```sql
-- Policy cho SELECT - Users chỉ thấy orders của họ
CREATE POLICY orders_select_policy ON orders
    FOR SELECT
    USING (customer_id = current_user_id());

-- Policy cho INSERT - Users chỉ insert orders cho họ
CREATE POLICY orders_insert_policy ON orders
    FOR INSERT
    WITH CHECK (customer_id = current_user_id());

-- Policy cho UPDATE - Users chỉ update orders của họ
CREATE POLICY orders_update_policy ON orders
    FOR UPDATE
    USING (customer_id = current_user_id())
    WITH CHECK (customer_id = current_user_id());

-- Policy cho DELETE
CREATE POLICY orders_delete_policy ON orders
    FOR DELETE
    USING (customer_id = current_user_id());

-- Combined policy for all operations
DROP POLICY orders_select_policy ON orders;
DROP POLICY orders_insert_policy ON orders;
DROP POLICY orders_update_policy ON orders;
DROP POLICY orders_delete_policy ON orders;

CREATE POLICY orders_all_policy ON orders
    FOR ALL
    USING (customer_id = current_user_id())
    WITH CHECK (customer_id = current_user_id());
```

### Multi-tenancy với RLS

```sql
-- Tenant isolation với RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_policy ON orders
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::BIGINT)
    WITH CHECK (tenant_id = current_setting('app.current_tenant')::BIGINT);

-- Set tenant context khi connect
SET app.current_tenant = '12345';

-- Application connection
-- psql "options=-c app.current_tenant=12345"
-- Hoặc trong connection string: options=-capp.current_tenant=12345
```

### RLS với Roles

```sql
-- Bypass RLS for admin roles
CREATE ROLE order_admin BYPASSRLS;

GRANT order_admin TO app_admin;

-- Admin users không bị RLS policies restrict
-- Regular users vẫn bị restrict
```

### Complex RLS Policies

```sql
-- Policy với multiple conditions
CREATE POLICY orders_complex_policy ON orders
    FOR ALL
    USING (
        -- User là owner
        customer_id = current_user_id()
        -- OR user là admin của organization
        OR EXISTS (
            SELECT 1 FROM user_organizations uo
            JOIN organizations o ON uo.organization_id = o.id
            WHERE uo.user_id = current_user_id()
            AND o.id = orders.organization_id
            AND uo.role = 'admin'
        )
        -- OR user có explicit permission
        OR has_table_permission(current_user_id(), 'orders', 'SELECT')
    );

-- Policy với time-based access
CREATE POLICY audit_read_policy ON audit_logs
    FOR SELECT
    USING (
        created_by = current_user_id()
        OR created_at < CURRENT_TIMESTAMP - INTERVAL '30 days'
        OR has_role('security_auditor')
    );
```

## Column-Level Security

```sql
-- Grant column-level permissions
GRANT SELECT (id, name, email, status) ON users TO app_service;
GRANT UPDATE (email, phone, address) ON users TO app_service;

-- Mask sensitive columns
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE OR REPLACE FUNCTION mask_ssn(text)
RETURNS text AS $$
BEGIN
    RETURN '***-**-' || RIGHT($1, 4);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Create view với masked columns
CREATE VIEW users_safe AS
SELECT 
    id,
    name,
    email,
    CASE 
        WHEN has_column_privilege('users', 'ssn', 'SELECT') 
        THEN ssn 
        ELSE mask_ssn(ssn) 
    END AS ssn,
    created_at
FROM users;
```

## Audit Logging với pgAudit

### pgAudit Installation và Setup

```bash
# Install pgAudit
# Ubuntu/Debian
apt-get install postgresql-16-pgaudit

# Or build from source
git clone https://github.com/pgaudit/pgaudit.git
cd pgaudit
git checkout REL_16_STABLE
make
sudo make install
```

```conf
# postgresql.conf
shared_preload_libraries = 'pgaudit'

# pgAudit settings
pgaudit.log = 'ddl, write, misc'  # What to log
pgaudit.log_catalog = on  # Include catalog changes
pgaudit.log_client = on  # Log to client (in addition to log file)
pgaudit.log_level = 'notice'  # Log level
pgaudit.log_parameter = on  # Include query parameters
pgaudit.log_relation = on  # Log relation names
pgaudit.log_statement_once = off  # Log full statement

# Per-role audit logging
pgaudit.role = 'audit_writer';
```

### Configure Audit Writer Role

```sql
-- Create audit writer role
CREATE ROLE audit_writer;

-- Grant necessary permissions
GRANT SELECT ON pg_stat_database TO audit_writer;
GRANT EXECUTE ON FUNCTION pg_logdir_ls() TO audit_writer;
GRANT EXECUTE ON FUNCTION pg_read_file() TO audit_writer;
```

### Audit Log Objects

```sql
-- Grant audit permissions on specific objects
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
GRANT SELECT, INSERT, UPDATE, DELETE ON orders TO audit_writer;

-- Audit specific columns
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
GRANT SELECT (id, name, email, created_at, updated_at) ON users TO auditor;
```

### Custom Audit Table

```sql
-- Create custom audit table
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    audit_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    user_name TEXT,
    action_type TEXT,
    table_name TEXT,
    record_id BIGINT,
    old_data JSONB,
    new_data JSONB,
    ip_address INET,
    application_name TEXT
);

-- Create function để log changes
CREATE OR REPLACE FUNCTION log_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (user_name, action_type, table_name, record_id, new_data, ip_address)
        VALUES (
            current_user,
            TG_OP,
            TG_TABLE_NAME,
            NEW.id,
            to_jsonb(NEW),
            inet_client_addr()
        );
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (user_name, action_type, table_name, record_id, old_data, new_data, ip_address)
        VALUES (
            current_user,
            TG_OP,
            TG_TABLE_NAME,
            NEW.id,
            to_jsonb(OLD),
            to_jsonb(NEW),
            inet_client_addr()
        );
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (user_name, action_type, table_name, record_id, old_data, ip_address)
        VALUES (
            current_user,
            TG_OP,
            TG_TABLE_NAME,
            OLD.id,
            to_jsonb(OLD),
            inet_client_addr()
        );
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create triggers
CREATE TRIGGER users_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION log_changes();

CREATE TRIGGER orders_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON orders
    FOR EACH ROW EXECUTE FUNCTION log_changes();
```

## SSL Configuration

### Generate SSL Certificates

```bash
# Create CA
openssl genrsa -out ca.key 4096
openssl req -new -x509 -days 3650 -key ca.key -out ca.crt \
    -subj "/CN=Root CA/O=My Company/C=US"

# Create server certificate
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr \
    -subj "/CN=postgres.example.com/O=My Company/C=US"

# Sign server certificate với CA
echo "subjectAltName=DNS:postgres.example.com,DNS:localhost,IP:127.0.0.1" > extfile.txt
openssl x509 -req -days 365 -in server.csr -CA ca.crt -CAkey ca.key \
    -out server.crt -extfile extfile.txt -CAcreateserial

# Create client certificate
openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr \
    -subj "/CN=app_user/O=My Company/C=US"

openssl x509 -req -days 365 -in client.csr -CA ca.crt -CAkey ca.key \
    -out client.crt -CAcreateserial

# Set permissions
chmod 600 server.key client.key ca.key
```

### Configure PostgreSQL SSL

```conf
# postgresql.conf
ssl = on
ssl_cert_file = '/etc/ssl/certs/server.crt'
ssl_key_file = '/etc/ssl/private/server.key'
ssl_ca_file = '/etc/ssl/certs/ca.crt'

# SSL preferences
ssl_min_protocol_version = 'TLSv1.2'
ssl_max_protocol_version = 'TLSv1.3'
ssl_prefer_server_ciphers = on
```

```conf
# pg_hba.conf - Require SSL
# IPv4 local connections
host     all             all             127.0.0.1/32            scram-sha-256

# Remote connections - require SSL
hostssl  all             all             0.0.0.0/0               scram-sha-256

# Certificate-based auth
hostssl  all             postgres        0.0.0.0/0               cert clientcert=verify-full
```

### Test SSL Connection

```sql
-- Check SSL status
SELECT ssl_is_used(), ssl_cipher, ssl_bits, ssl_client_serial, 
       ssl_client_dn, ssl_client_verify
FROM pg_stat_ssl;

-- Verify certificate
SELECT * FROM pg_stat_ssl
WHERE pid = pg_backend_pid();
```

```bash
# Test SSL connection với psql
psql "postgresql://user:pass@host:5432/db?sslmode=require"
psql "postgresql://user:pass@host:5432/db?sslmode=verify-ca&sslrootcert=ca.crt"
psql "postgresql://user:pass@host:5432/db?sslmode=verify-full&sslrootcert=ca.crt&sslcert=client.crt&sslkey=client.key"
```

## Best Practices

### Principle of Least Privilege

```sql
-- Bad practice: Grant excessive permissions
GRANT ALL PRIVILEGES ON DATABASE mydb TO app_service;

-- Good practice: Grant only necessary permissions
GRANT CONNECT ON DATABASE mydb TO app_service;
GRANT USAGE ON SCHEMA app TO app_service;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app TO app_service;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA app TO app_service;
```

### Secure Password Policies

```sql
-- Create password policy function
CREATE OR REPLACE FUNCTION validate_password(password TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    IF length(password) < 12 THEN
        RAISE EXCEPTION 'Password must be at least 12 characters';
    END IF;
    IF password ~ '[A-Z]' IS FALSE THEN
        RAISE EXCEPTION 'Password must contain uppercase letter';
    END IF;
    IF password ~ '[a-z]' IS FALSE THEN
        RAISE EXCEPTION 'Password must contain lowercase letter';
    END IF;
    IF password ~ '[0-9]' IS FALSE THEN
        RAISE EXCEPTION 'Password must contain number';
    END IF;
    IF password ~ '[!@#$%^&*()]' IS FALSE THEN
        RAISE EXCEPTION 'Password must contain special character';
    END IF;
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- Use password check hook
ALTER SYSTEM SET password_check_function = 'validate_password';
SELECT pg_reload_conf();
```

### Connection Security

```conf
# postgresql.conf - Connection limits
max_connections = 100
superuser_reserved_connections = 3

# Idle connection timeout
idle_session_timeout = 600

# Statement timeout
statement_timeout = 60000  # 60 seconds

# Lock timeout
lock_timeout = 10000  # 10 seconds
```

### Regular Security Audits

```sql
-- Check for excessive permissions
SELECT 
    grantee,
    table_schema,
    privilege_type,
    COUNT(*) as count
FROM information_schema.table_privileges
GROUP BY grantee, table_schema, privilege_type
ORDER BY count DESC;

-- Check for public schema access
SELECT 
    schemaname,
    tablename,
    privilege_type
FROM information_schema.table_privileges
WHERE grantee = 'PUBLIC';

-- Find users with superuser
SELECT 
    rolname,
    rolsuper,
    rolinherit,
    rolcreaterole,
    rolcreatedb,
    rolreplication
FROM pg_roles
WHERE rolsuper = TRUE;

-- Check RLS status
SELECT 
    schemaname,
    tablename,
    rowsecurity,
   forcerowsecurity
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema');
```

## Common Patterns

### Pattern 1: Application Service Account

```sql
-- Create dedicated application role
CREATE ROLE app_service LOGIN PASSWORD 'extremely_strong_password';
GRANT USAGE ON SCHEMA public TO app_service;
GRANT USAGE ON SCHEMA app TO app_service;

-- Grant specific table access
GRANT SELECT, INSERT, UPDATE, DELETE ON app.orders TO app_service;
GRANT SELECT ON app.products TO app_service;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA app TO app_service;

-- Restrict DDL
REVOKE ALL ON SCHEMA public FROM app_service;
GRANT USAGE ON SCHEMA public TO app_service;

-- Set default privileges
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA app
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_service;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA app
    GRANT USAGE, SELECT ON SEQUENCES TO app_service;
```

### Pattern 2: Multi-tenant Database

```sql
-- Tenant isolation
CREATE TABLE tenants (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    database_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tenant_users (
    id BIGSERIAL PRIMARY KEY,
    tenant_id BIGINT NOT NULL REFERENCES tenants(id),
    email VARCHAR(255) NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(50) DEFAULT 'member'
);

-- RLS policy
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON orders
    FOR ALL
    USING (
        tenant_id = current_setting('app.tenant_id')::BIGINT
    )
    WITH CHECK (
        tenant_id = current_setting('app.tenant_id')::BIGINT
    );

-- Trigger to auto-set tenant
CREATE OR REPLACE FUNCTION set_tenant()
RETURNS TRIGGER AS $$
BEGIN
    NEW.tenant_id = current_setting('app.tenant_id')::BIGINT;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER orders_set_tenant
    BEFORE INSERT ON orders
    FOR EACH ROW EXECUTE FUNCTION set_tenant();
```

### Pattern 3: Time-limited Access

```sql
-- Create temporary access role
CREATE OR REPLACE FUNCTION grant_temporary_access(
    user_name TEXT,
    table_name TEXT,
    expire_at TIMESTAMPTZ
)
RETURNS void AS $$
DECLARE
    role_name TEXT;
BEGIN
    role_name := 'temp_access_' || replace(user_name, '-', '_');
    
    -- Create role
    EXECUTE format('CREATE ROLE %I LOGIN', role_name);
    EXECUTE format('GRANT SELECT ON %I TO %I', table_name, role_name);
    
    -- Schedule role removal
    PERFORM pg_sleep(
        EXTRACT(EPOCH FROM (expire_at - CURRENT_TIMESTAMP))
    );
    EXECUTE format('DROP ROLE IF EXISTS %I', role_name);
END;
$$ LANGUAGE plpgsql;
```

## Troubleshooting

### Vấn đề 1: Permission Denied

**Giải pháp**:

```sql
-- Check current user
SELECT current_user, session_user;

-- Check user's effective permissions
SELECT 
    table_schema,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE grantee = current_user;

-- Check RLS policies
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE tablename = 'orders';

-- Temporarily bypass RLS (for debugging)
SET ROLE postgres;
SET row_security = off;  -- Superuser only
```

### Vấn đề 2: RLS Performance Issues

**Giải pháp**:

```sql
-- Check query plan
EXPLAIN ANALYZE SELECT * FROM orders WHERE id = 1;

-- Index for RLS filter
CREATE INDEX ON orders (tenant_id) WHERE rowsecurity = TRUE;

-- Use SECURITY DEFINER functions for performance
CREATE OR REPLACE FUNCTION get_orders()
RETURNS SETOF orders AS $$
BEGIN
    RETURN QUERY SELECT * FROM orders WHERE customer_id = current_user_id();
END;
$$ LANGUAGE SQL SECURITY DEFINER;
```

### Vấn đề 3: SSL Certificate Errors

**Giải pháp**:

```bash
# Verify certificate
openssl x509 -in server.crt -text -noout

# Check certificate chain
openssl verify -CAfile ca.crt server.crt

# Test connection
psql "postgresql://user:pass@host:5432/db?sslmode=require&sslcert=client.crt&sslkey=client.key"

# View SSL info
openssl s_client -connect host:5432 -starttls postgres
```

## Ví dụ minh họa

### Ví dụ 1: Complete Security Setup Script

```sql
-- Complete security setup cho application database

-- 1. Create schema
CREATE SCHEMA IF NOT EXISTS app;

-- 2. Create application roles
DO $$
BEGIN
    -- Read-only role
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_readonly') THEN
        CREATE ROLE app_readonly;
    END IF;
    
    -- Read-write role
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_writer') THEN
        CREATE ROLE app_writer;
    END IF;
    
    -- Admin role
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_admin') THEN
        CREATE ROLE app_admin BYPASSRLS;
    END IF;
END
$$;

-- 3. Grant schema permissions
GRANT USAGE ON SCHEMA app TO app_readonly, app_writer, app_admin;

-- 4. Grant table permissions
GRANT SELECT ON ALL TABLES IN SCHEMA app TO app_readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app TO app_writer;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA app TO app_admin;

-- 5. Grant sequence permissions (for SERIAL columns)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA app TO app_readonly;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA app TO app_writer;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA app TO app_admin;

-- 6. Default privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA app
    GRANT SELECT ON TABLES TO app_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA app
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA app
    GRANT ALL ON TABLES TO app_admin;

-- 7. Create application user
CREATE ROLE app_user LOGIN PASSWORD 'extremely_strong_password_here';
GRANT app_readonly TO app_user;
-- Hoặc grant multiple roles
-- GRANT app_readonly, app_writer TO app_user;

-- 8. Create admin user
CREATE ROLE admin_user LOGIN PASSWORD 'another_strong_password' SUPERUSER;
GRANT app_admin TO admin_user;

-- 9. Revoke public access
REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON DATABASE mydb FROM PUBLIC;

-- 10. Create audit role
CREATE ROLE audit_role;
GRANT SELECT ON ALL TABLES IN SCHEMA app TO audit_role;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO audit_role;
```

### Ví dụ 2: pgaudit Configuration

```conf
# postgresql.conf additions for pgaudit

# Load pgaudit
shared_preload_libraries = 'pgaudit'

# pgaudit configuration
pgaudit.log = 'ddl, write, misc'  # Log DDL, INSERT/UPDATE/DELETE, miscellaneous
pgaudit.log_catalog = on  # Include catalog changes in log
pgaudit.log_client = on  # Write log to client connection
pgaudit.log_level = 'info'  # Log level
pgaudit.log_parameter = on  # Include query parameters in log
pgaudit.log_relation = on  # Log per-relation statements
pgaudit.log_statement_once = off  # Log full statement
pgaudit.log_rows = off  # Don't log rows affected

# Per-role logging
pgaudit.role = 'audit_writer'

# Exclude certain statements from logging
# pgaudit.log_statement = 'ddl, write'
```

```sql
-- Create audit writer role
CREATE ROLE audit_writer;

-- Grant necessary permissions
GRANT SELECT ON pg_stat_database TO audit_writer;
GRANT EXECUTE ON FUNCTION pg_logdir_ls() TO audit_writer;

-- Grant permission to specific tables
GRANT SELECT ON ALL TABLES IN SCHEMA app TO audit_writer;
```

### Ví dụ 3: pg_hba.conf Security Configuration

```conf
# pg_hba.conf - PostgreSQL Client Authentication

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# Local connections - use peer/trust for OS user matching
local   all             postgres                                peer
local   replication     postgres                                peer
local   all             all                                     peer

# IPv4 local connections:
host    all             postgres        127.0.0.1/32            scram-sha-256
host    all             all             127.0.0.1/32            scram-sha-256

# Application servers - require strong authentication
host    mydb            app_user        10.0.0.0/8              scram-sha-256
host    mydb            app_writer      10.0.0.0/8              scram-sha-256

# Reporting/BI servers
host    mydb            readonly        10.1.0.0/16             scram-sha-256

# Development environments
host    mydb            dev_user        192.168.0.0/16          scram-sha-256

# SSL-only for all remote connections
hostssl all             all             0.0.0.0/0               scram-sha-256

# Replication connections
host    replication     replicator      10.0.1.0/24             scram-sha-256

# Admin access from specific IP
host    all             admin_user      10.0.0.1/32             scram-sha-256
```

## References

### Official Documentation
- [PostgreSQL Authentication](https://www.postgresql.org/docs/current/auth-password.html)
- [PostgreSQL GRANT](https://www.postgresql.org/docs/current/sql-grant.html)
- [PostgreSQL REVOKE](https://www.postgresql.org/docs/current/sql-revoke.html)
- [Row-Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [pgAudit](https://github.com/pgaudit/pgaudit)
- [SSL Support](https://www.postgresql.org/docs/current/ssl-tcp.html)

### Security Best Practices
- [OWASP Database Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html)
- [CIS PostgreSQL Benchmark](https://www.cisecurity.org/benchmark/postgresql)

### Compliance
- [GDPR Article 32](https://gdpr.eu/article-32-processing-security/) - Security of processing
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
