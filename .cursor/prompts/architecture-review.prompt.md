# Prompt: Architecture Review - Review kiến trúc

```markdown
# Architecture Review Workflow

## 1. REVIEW SCOPE
- **Review ID**: [REVIEW-ID]
- **Scope**: [Full / Module / Component]
- **Architecture Pattern**: [Monolith / Microservice / Modular]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/architecture/*
- knowledge/ddd/*
- knowledge/cqrs/*
- knowledge/clean-architecture/*
Load rules: enterprise-architecture.mdc, ddd.mdc, cqrs.mdc
```

## 3. REVIEW AREAS

### Structural Review
- [ ] Layer separation
- [ ] Module boundaries
- [ ] Dependency direction
- [ ] Interface design

### Design Patterns
- [ ] Pattern usage correctness
- [ ] Pattern appropriateness
- [ ] Anti-pattern detection

### Quality Attributes
- [ ] Scalability
- [ ] Maintainability
- [ ] Testability
- [ ] Security
- [ ] Performance

## 4. DECISION RECORD
```
ADR-[ID]: [Title]
Status: [proposed/accepted]
Context: [Problem statement]
Decision: [Chosen approach]
Consequences: [Positive/Negative]
```

## 5. LIÊN KẾT
- [[../skills/refactor-planner]] - Refactor Planner
- [[../rules/enterprise-architecture]] - Enterprise Architecture
- [[../rules/ddd]] - DDD
- [[../rules/cqrs]] - CQRS
```
