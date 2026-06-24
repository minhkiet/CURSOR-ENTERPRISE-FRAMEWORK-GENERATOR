# Multi-Tenant Knowledge - Architecture

## Isolation Strategy Comparison

| Strategy | Isolation | Cost | Complexity | Migration |
|----------|-----------|------|-----------|----------|
| Database per tenant | Highest | High | Medium | Hard |
| Schema per tenant | High | Medium | Medium | Medium |
| Discriminator column | Medium | Low | Low | Easy |
| Application-level | Medium | Low | Medium | Easy |

## Recommended Architecture (Discriminator Column + RLS)
```
[Application]
    |
    v
[API Gateway] --> [Middleware: Inject tenant_id]
    |
    v
[Route Handler] --> [Tenant-scoped DB queries]
    |
    v
[PostgreSQL + RLS]
```

### RLS Implementation
```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

## Tenant Provisioning Workflow
1. Create tenant record in tenants table
2. Generate tenant_id (UUID)
3. Initialize default settings
4. Setup RLS policies
5. Create initial admin user
6. Send welcome email
7. Configure SSO (if applicable)
8. Setup billing subscription

## Cross-Tenant Considerations
- Never expose tenant_id in URLs or logs without masking
- Audit log tenant_id on every data access
- Implement tenant-level rate limiting
- Use separate storage buckets per tenant for file uploads
- Separate cache keys with tenant prefix

## Scaling Considerations
- Connection pooling: Use PgBouncer for connection management
- Separate read replicas for reporting queries
- Tenant-level resource quotas (CPU, storage, API calls)
- Auto-scaling based on aggregate load
