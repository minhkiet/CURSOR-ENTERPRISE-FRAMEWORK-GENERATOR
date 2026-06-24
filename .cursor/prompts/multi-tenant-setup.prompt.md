---
description: Prompt chuan de setup multi-tenant - RLS, tenant isolation
trigger: multi-tenant, tenant isolation
category: SaaS
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Prompt: Multi-Tenant Setup - Thiết lập Multi-Tenant

```markdown
# Multi-Tenant Setup Workflow

## 1. TENANT ARCHITECTURE
- **Isolation Strategy**: [RLS / Schema / Database]
- **Tenant Model**: [Dedicated / Shared]
- **Scale**: [Small / Medium / Large]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/multi-tenant/*
- knowledge/rls/*
- knowledge/postgres/*
Load rules: multi-tenant.mdc, rls.mdc
```

## 3. SETUP STEPS

### Database
- [ ] Create tenant discriminator column
- [ ] Enable RLS on all tables
- [ ] Create tenant policies
- [ ] Create indexes

### Application
- [ ] Tenant context middleware
- [ ] Tenant-aware ORM
- [ ] Tenant-scoped queries

### Security
- [ ] Tenant isolation verification
- [ ] Cross-tenant access prevention
- [ ] Audit logging

## 4. LIÊN KẾT
- [[../skills/tenant-isolation-review]] - Tenant Isolation
- [[../rules/multi-tenant]] - Multi-Tenant Rules
```
