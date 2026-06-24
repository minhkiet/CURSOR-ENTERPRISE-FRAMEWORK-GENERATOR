# Multi-Tenant Knowledge - Best Practices

## Isolation Best Practices
- Always include tenant_id on every tenant-scoped table
- Never expose raw tenant_id in URLs (use slugs)
- Implement RLS on all tenant-scoped PostgreSQL tables
- Use separate cache namespaces per tenant
- Separate file storage (S3 prefix, R2 namespace)
- Validate tenant_id matches authenticated tenant on every request

## Security Best Practices
- Cross-tenant access requires explicit super-admin role
- Audit log all cross-tenant operations
- Encrypt tenant-specific secrets separately
- Implement tenant-level IP allowlisting
- SSO per tenant (SAML/OIDC)
- Session isolation between tenants

## Performance Best Practices
- Index tenant_id columns as first column
- Partition large tables by tenant_id for archival
- Use connection poolers (PgBouncer) to handle many tenants
- Implement tenant-level caching with TTL
- Separate reporting queries from transactional
- Implement request queuing per tenant

## Tenant Management Best Practices
- Provisioning automation for fast onboarding
- Idempotent tenant creation (safe to retry)
- Graceful suspension (retain data, disable access)
- Data export capability before deletion
- Automated backup per tenant
- Tenant-specific feature flags
