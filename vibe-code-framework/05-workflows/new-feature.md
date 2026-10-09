# New Feature Workflow

> **Version:** 1.0.0 | **Category:** Workflow | **Steps:** 6

---

## Purpose

Workflow chuẩn để tạo feature mới từ đầu đến cuối.

## Steps

### Step 1: Define

```
┌────────────────────────────────────────────────────────────┐
│ Step 1: Define Feature                                    │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Input: User requirement                                  │
│                                                            │
│  Output: Feature spec with:                              │
│  ├── Overview                                           │
│  ├── User stories                                       │
│  ├── Requirements                                       │
│  ├── Acceptance criteria                                │
│  └── Technical design (if needed)                       │
│                                                            │
│  Gate: Requirements clear?                              │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Output Template:**

```markdown
# Feature: [Name]

## Overview
[Brief description]

## User Stories
- **As a** [user], **I want** [action], **so that** [benefit]

## Requirements
1. [Requirement]
2. [Requirement]

## Acceptance Criteria
- [ ] AC1: [Verifiable outcome]
- [ ] AC2: [Verifiable outcome]

## Technical Notes
- [Any technical decisions]

## Out of Scope
- [Items not included]
```

### Step 2: Design

```
┌────────────────────────────────────────────────────────────┐
│ Step 2: Design                                             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Input: Feature spec                                      │
│                                                            │
│  Output: Technical design with:                          │
│  ├── Domain model                                       │
│  ├── API contracts                                      │
│  ├── Database schema                                    │
│  └── Component structure                                │
│                                                            │
│  Gate: Design approved?                                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 3: Plan

```
┌────────────────────────────────────────────────────────────┐
│ Step 3: Plan Tasks                                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Input: Technical design                                  │
│                                                            │
│  Output: Task list with:                                │
│  ├── Task 1: [Description]                             │
│  ├── Task 2: [Description]                             │
│  └── Task 3: [Description]                             │
│                                                            │
│  Each task should be:                                   │
│  ├── Atomic (can be done in one session)               │
│  ├── Verifiable (has clear AC)                         │
│  └── Independent (can be reviewed separately)            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 4: Implement

```
┌────────────────────────────────────────────────────────────┐
│ Step 4: Implement                                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  For each task:                                          │
│                                                            │
│  1. Create branch                                       │
│     git checkout -b feature/task-name                     │
│                                                            │
│  2. Implement                                           │
│     - Domain layer                                      │
│     - Application layer                                 │
│     - Infrastructure layer                              │
│     - Presentation layer                                │
│                                                            │
│  3. Write tests                                         │
│     - Unit tests                                        │
│     - Integration tests (if needed)                     │
│                                                            │
│  4. Self-review                                        │
│     - Run lint, type-check                             │
│     - Review own code                                   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 5: Test

```
┌────────────────────────────────────────────────────────────┐
│ Step 5: Test                                              │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Run tests                                           │
│     - All tests pass                                    │
│     - Coverage acceptable (> 80%)                       │
│                                                            │
│  2. Manual testing                                       │
│     - Follow acceptance criteria                        │
│     - Test edge cases                                   │
│                                                            │
│  3. Verify                                             │
│     - Feature works as specified                        │
│     - No regressions                                   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 6: Review & Merge

```
┌────────────────────────────────────────────────────────────┐
│ Step 6: Review & Merge                                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Open PR                                             │
│     - Title: feat(scope): description                    │
│     - Description: summary, testing, checklist          │
│                                                            │
│  2. Review                                              │
│     - Address feedback                                  │
│     - Get approval                                      │
│                                                            │
│  3. Merge                                               │
│     - Squash if small                                  │
│     - Merge commit if multiple logical changes          │
│                                                            │
│  4. Deploy                                              │
│     - Deploy to staging                                │
│     - Deploy to production                             │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Checklist

```
□ Feature spec created
□ Technical design reviewed
□ Tasks planned
□ Code implemented
□ Tests written
□ Tests pass
□ PR opened
□ PR reviewed
□ PR merged
□ Deployed
```

## Timeline Guide

| Task Size | Estimate | Review |
|-----------|----------|--------|
| Small | 1-2 hours | 15-30 min |
| Medium | 4-8 hours | 30-60 min |
| Large | 1-2 days | 1-2 hours |

## Related Workflows

- [bug-fix.md](./bug-fix.md) - Fix bug
- [release.md](./release.md) - Release workflow
