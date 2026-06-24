# Multi-Tenant Knowledge - Glossary

## Core Concepts
- **Tenant**: Independent customer organization with isolated data
- **Tenant ID**: Unique identifier per tenant
- **Tenant isolation**: Data cannot cross tenant boundaries
- **Tenant discriminator**: Column (tenant_id) used for filtering
- **Row Level Security (RLS)**: PostgreSQL feature for tenant isolation

## Isolation Strategies
- **Database per tenant**: Complete isolation, higher cost
- **Schema per tenant**: Isolated namespaces within single DB
- **Discriminator column**: Single schema, filtered by tenant_id
- **Application-level**: Code enforces tenant boundaries

## Tenant Lifecycle
- **Provision**: Create tenant record and resources
- **Configure**: Setup tenant-specific settings
- **Upgrade/downgrade**: Change subscription tier
- **Suspend**: Temporarily disable without deletion
- **Delete**: Permanent removal with data export

## Roles & Permissions
- **Tenant owner**: Full control over tenant
- **Tenant admin**: Manage users and settings
- **Tenant member**: Access tenant resources
- **Cross-tenant admin**: Platform-level administrator

## Billing Models
- **Per-seat**: Per active user pricing
- **Per-tenant**: Flat fee per tenant
- **Usage-based**: Based on consumption metrics
- **Tiered**: Volume discounts at higher tiers
