# Code Review Skill

> **Version:** 1.0.0 | **Category:** Quality | **Triggers:** review, code review, check, audit

---

## Goal

Review code theo quality gates:
- Correctness
- Design
- Security
- Performance
- Maintainability

## Trigger Conditions

- PR opened
- User yêu cầu review
- Trước khi merge

## Pre-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ P.1: Understand Context                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Đã hiểu feature/fix là gì?                           │
│ □ Đã xem PR description?                                  │
│ □ Đã chạy code local?                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Review Process

### 1. Analyze Change

```
┌────────────────────────────────────────────────────────────┐
│ Analysis Checklist                                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Scope:                                                    │
│  ├── Files changed                                       │
│  ├── Lines added/removed                                │
│  └── Complexity                                          │
│                                                            │
│  Risk:                                                     │
│  ├── Database changes                                     │
│  ├── API changes                                         │
│  ├── Authentication/Authorization                        │
│  └── Performance impact                                  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 2. Apply Five-Axis Review

#### Axis 1: Correctness

```
□ Logic produces correct results
□ Edge cases handled
□ Error paths tested
□ No off-by-one errors
□ No race conditions
□ No memory leaks
```

#### Axis 2: Design

```
□ Single responsibility
□ Open/closed principle
□ Dependencies inverted
□ Layer separation maintained
□ No tight coupling
□ Reusable abstractions
```

#### Axis 3: Readability

```
□ Meaningful names
□ Functions small (< 30 lines)
□ Logic easy to follow
□ Comments explain "why"
□ No magic numbers
□ Consistent style
```

#### Axis 4: Security

```
□ No hardcoded secrets
□ Input validated
□ SQL injection prevented
□ XSS prevented
□ Proper auth/authz
□ No sensitive data in logs
```

#### Axis 5: Performance

```
□ No N+1 queries
□ Indexes used properly
□ Expensive ops cached
□ No unnecessary allocations
□ Async where appropriate
```

### 3. Provide Feedback

**Feedback Levels:**

| Level | Meaning | Required |
|-------|---------|----------|
| **Blocking** | Must fix before merge | Yes |
| **Suggestion** | Nice to have | No |
| **Nit** | Minor style issue | No |

**Template:**

```markdown
## [BLOCKING] [Title]

Issue: [Description]

Why this matters: [Impact]

Suggestion: [How to fix]

---

## [SUGGESTION] [Title]

Current: [What is done]

Better: [Alternative]

---

## [LGTM]

Changes look good:
- ✅ [Good point 1]
- ✅ [Good point 2]

Minor suggestions (non-blocking):
- 💡 [Suggestion 1]
- 💡 [Suggestion 2]
```

## Post-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ Final Approval                                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ All blocking issues resolved?                             │
│ □ Tests pass?                                              │
│ □ Documentation updated?                                   │
│ □ Security concerns addressed?                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Change Size Guidelines

| Size | Lines | Recommendation |
|------|-------|----------------|
| XS | 1-10 | ✅ Ideal |
| S | 11-50 | ✅ Good |
| M | 51-200 | ⚠️ Consider splitting |
| L | 201-500 | ⚠️ Needs justification |
| XL | 500+ | ❌ Must split |

## Communication Principles

1. **Be respectful** — Critique code, not person
2. **Be specific** — Point to exact lines
3. **Be actionable** — Suggest how to fix
4. **Be balanced** — Acknowledge good work
5. **Be timely** — Review within 24 hours
