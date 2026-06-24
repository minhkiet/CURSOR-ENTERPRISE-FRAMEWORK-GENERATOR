# Multi-Tenant Knowledge - Checklist

## Setup
- [ ] Tenant model with UUID primary key
- [ ] tenant_id column on all tenant-scoped tables
- [ ] RLS enabled on all tenant-scoped tables
- [ ] RLS policies created for each table
- [ ] Application middleware injects tenant context
- [ ] tenant_id validated against authenticated user

## Security
- [ ] No raw tenant_id in public URLs
- [ ] Tenant isolation verified via integration tests
- [ ] Cross-tenant access requires super-admin role
- [ ] Audit logging captures tenant_id on every write
- [ ] SSO configured per tenant
- [ ] Separate secrets per tenant for sensitive integrations

## Performance
- [ ] tenant_id indexed as first column
- [ ] Connection pooler configured (PgBouncer)
- [ ] Tenant-level rate limiting in place
- [ ] Separate cache namespaces per tenant
- [ ] File storage prefixed by tenant_id
- [ ] Query performance verified at scale

## Tenant Lifecycle
- [ ] Automated provisioning workflow
- [ ] Suspension workflow (disable, retain data)
- [ ] Deletion workflow (export, then delete)
- [ ] Upgrade/downgrade workflow
- [ ] Tenant export capability (GDPR)
