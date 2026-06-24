---
description: Prompt chuan de review CRM SaaS - multi-tenant, RLS, billing
trigger: crm saas, customer management
category: SaaS
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Prompt: CRM SaaS Review

```markdown
# CRM SaaS Review Workflow

## 1. REVIEW SCOPE
- **CRM Type**: [B2B / B2C / Marketplace]
- **Features**: [Sales / Marketing / Service / Analytics]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/crm/*
- knowledge/multi-tenant/*
- knowledge/billing/*
Load rules: crm-saas.mdc, multi-tenant.mdc, billing.mdc
```

## 3. REVIEW AREAS
- [ ] Multi-tenant isolation
- [ ] Scalability
- [ ] Feature completeness
- [ ] Integration capabilities
- [ ] Security

## 4. LIÊN KẾT
- [[../skills/crm-saas-review]] - CRM SaaS Review
- [[../rules/crm-saas]] - CRM SaaS Rules
```
