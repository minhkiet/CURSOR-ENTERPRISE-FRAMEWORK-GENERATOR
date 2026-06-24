---
description: Prompt chuan de tao ADR - Architecture Decision Record
trigger: adr, architecture decision
category: Memory
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Prompt: ADR Generator - Tạo Architecture Decision Record

```markdown
# ADR Generator Workflow

## 1. DECISION CONTEXT
- **Decision ID**: ADR-[NEXT-ID]
- **Title**: [Tiêu đề decision]
- **Domain**: [architecture/frontend/backend/database/ai/infra]
- **Priority**: [Critical/High/Medium/Low]

## 2. CONTEXT LOADING
```
Load:
- memory/decisions.sqlite (existing ADRs)
- knowledge/architecture/*
Load rules: enterprise-architecture.mdc
```

## 3. ADR TEMPLATE

### Status: Proposed

### Context
[Problem statement - mô tả vấn đề cần giải quyết]

### Decision
[Chosen approach - giải pháp được chọn]

### Options Considered
1. **Option A**: [Description]
   - Pros: [List]
   - Cons: [List]

2. **Option B**: [Description]
   - Pros: [List]
   - Cons: [List]

### Consequences
#### Positive
- [List positive consequences]

#### Negative
- [List negative consequences]

### Risks
| Risk | Severity | Mitigation |
|------|----------|------------|
| [Risk 1] | [H/M/L] | [Mitigation] |

### Related Decisions
- [ADR-ID]: [Title]

## 4. LIÊN KẾT
- [[../skills/adr-generator]] - ADR Generator
- [[../rules/enterprise-architecture]] - Enterprise Architecture
```
