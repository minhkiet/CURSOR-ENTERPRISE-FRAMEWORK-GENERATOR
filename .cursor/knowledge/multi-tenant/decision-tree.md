# Multi-Tenant Knowledge - Decision Tree

## Which isolation strategy?
- < 100 tenants, simple needs: Discriminator column + RLS
- 100-1000 tenants, compliance required: Schema per tenant
- > 1000 tenants, strict isolation: Database per tenant
- Hybrid: Use discriminator for most, separate DB for enterprise tier

## Where to store tenant context?
- JWT claim: Good for stateless APIs
- Thread-local/request context: Good for ORM-heavy apps
- Request header: Good for API gateways
- Session: Good for server-rendered apps

## How to handle tenant billing?
- Per-seat: Track active users, bill monthly
- Flat fee: Simple monthly/annual invoice
- Usage-based: Track metered events (API calls, storage, compute)
- Tiered: Define feature tiers, map tenants to tiers

## How to handle tenant deletion?
1. Export all data (GDPR compliance)
2. Suspend tenant (prevent new activity)
3. Wait for data retention period
4. Delete from database (cascade or manual)
5. Delete from file storage
6. Delete from cache
7. Cancel billing subscription
8. Send deletion confirmation email
