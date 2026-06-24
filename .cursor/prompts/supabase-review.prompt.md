---
description: Prompt chuan de review Supabase - auth, database, storage, RLS
trigger: supabase, baas review
category: Database
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Prompt: Supabase Review - Review Supabase

```markdown
# Supabase Review Workflow

## 1. REVIEW SCOPE
- **Review Type**: [Full / Schema / RLS / Performance / Security]
- **Environment**: [Production / Staging / Development]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/supabase/*
- knowledge/postgres/*
- knowledge/rls/*
- knowledge/pgvector/*
Load rules: supabase.mdc, rls.mdc, pgvector.mdc
```

## 3. REVIEW AREAS

### Schema Review
- [ ] Table design
- [ ] Index strategy
- [ ] Foreign keys
- [ ] Constraints
- [ ] Migration scripts

### RLS Review
- [ ] RLS enabled on all tables
- [ ] Policy correctness
- [ ] Performance impact
- [ ] Testing coverage

### Security Review
- [ ] API security
- [ ] Row-level security
- [ ] Storage security
- [ ] Edge functions security

### Performance Review
- [ ] Query performance
- [ ] Index usage
- [ ] Connection pooling
- [ ] Caching strategy

## 4. FINDINGS

### Schema Issues
| ID | Issue | Table | Severity | Fix |
|----|-------|-------|----------|-----|
| S-001 | [Issue] | [Table] | [H/M/L] | [Fix] |

## 5. LIÊN KẾT
- [[../skills/supabase-review]] - Supabase Review
- [[../skills/rls-audit]] - RLS Audit
- [[../rules/supabase]] - Supabase Rules
- [[../rules/rls]] - RLS Rules
```
