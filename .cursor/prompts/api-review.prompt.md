---
description: Prompt chuan de review API - REST, GraphQL, contracts, versioning
trigger: api review, review endpoint
category: Architecture
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Prompt: API Review - Review API

```markdown
# API Review Workflow

## 1. REVIEW SCOPE
- **API Type**: [REST / GraphQL / gRPC / WebSocket]
- **Scope**: [Full / Endpoint / Security / Performance]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/api/*
- knowledge/[backend-framework]/*
Load rules: api.mdc, security.mdc
```

## 3. REVIEW AREAS

### Design
- [ ] REST conventions
- [ ] Naming consistency
- [ ] Versioning strategy
- [ ] Error handling

### Security
- [ ] Authentication
- [ ] Authorization
- [ ] Rate limiting
- [ ] Input validation

### Performance
- [ ] Pagination
- [ ] Caching
- [ ] Compression
- [ ] Batch endpoints

## 4. LIÊN KẾT
- [[../skills/api-review]] - API Review
- [[../rules/api]] - API Rules
```
