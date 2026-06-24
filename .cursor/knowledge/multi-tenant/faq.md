# Multi-Tenant Knowledge - FAQ

**Q: How do we prevent tenant A from seeing tenant B's data?**
A: Use PostgreSQL RLS with a session variable set per request. Every query automatically filters by tenant_id.

**Q: What happens if a tenant exceeds their plan limits?**
A: Implement usage tracking middleware. When limits are exceeded, either upgrade prompt or graceful degradation (read-only mode).

**Q: How do we handle database migrations across tenants?**
A: With RLS, migrations are straightforward. For schema-per-tenant, use tools like Flyway with multi-schema support.

**Q: Should we share Redis across tenants?**
A: Yes, but use key prefixes: `tenant:{id}:{resource}`. Ensure no sensitive tenant data in plain text in Redis.

**Q: How do we handle SSO for multi-tenant?**
A: Support both platform SSO (for subdomains like tenant.platform.com) and tenant-specific SSO (via SAML/OIDC federation).

**Q: Can tenants have custom domains?**
A: Yes, use CNAME records pointing to platform. Handle SSL certificates via Let's Encrypt with SNI for per-tenant certs.
