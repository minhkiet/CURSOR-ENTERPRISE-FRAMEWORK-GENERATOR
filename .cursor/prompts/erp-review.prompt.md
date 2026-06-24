---
description: Prompt chuan de review ERP - inventory, finance, HR
trigger: erp, enterprise resource planning
category: Business
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Prompt: ERP Review - Review ERP

```markdown
# ERP Review Workflow

## 1. REVIEW SCOPE
- **ERP Type**: [Full / Modular / Industry-specific]
- **Modules**: [Finance / HR / Inventory / SCM / CRM]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/crm/* (if applicable)
Load rules: crm-saas.mdc
```

## 3. REVIEW AREAS
- [ ] Module integration
- [ ] Data consistency
- [ ] Workflow automation
- [ ] Reporting
- [ ] Multi-tenant support

## 4. LIÊN KẾT
- [[../skills/crm-saas-review]] - CRM SaaS Review
- [[../rules/crm-saas]] - CRM SaaS Rules
```
