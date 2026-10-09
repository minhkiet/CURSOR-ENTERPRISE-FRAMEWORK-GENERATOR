# Bug Fix Workflow

> **Version:** 1.0.0 | **Category:** Workflow | **Steps:** 5

---

## Purpose

Workflow chuẩn để fix bug từ đầu đến cuối.

## Steps

### Step 1: Understand

```
┌────────────────────────────────────────────────────────────┐
│ Step 1: Understand the Bug                                │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Input: Bug report                                       │
│                                                            │
│  Gather:                                                 │
│  ├── Steps to reproduce                                  │
│  ├── Expected behavior                                   │
│  ├── Actual behavior                                     │
│  ├── Error messages/stack traces                         │
│  └── Environment (dev/staging/prod)                     │
│                                                            │
│  Gate: Can reproduce?                                    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 2: Investigate

```
┌────────────────────────────────────────────────────────────┐
│ Step 2: Investigate                                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Find the failing code                               │
│     - Which file/function/line                          │
│                                                            │
│  2. Trace the data flow                                 │
│     - Where does it originate?                          │
│     - Where does it fail?                              │
│                                                            │
│  3. Identify root cause                                  │
│     - Not symptom, but cause                            │
│                                                            │
│  Gate: Root cause identified?                           │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 3: Fix

```
┌────────────────────────────────────────────────────────────┐
│ Step 3: Implement Fix                                     │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Create branch                                       │
│     git checkout -b fix/{ticket-id}-{short-desc}         │
│                                                            │
│  2. Implement minimal fix                                │
│     - Don't over-engineer                               │
│     - Fix the cause, not symptoms                       │
│     - Don't introduce new bugs                         │
│                                                            │
│  3. Add test case                                      │
│     - Prevent regression                               │
│     - Cover the edge case                              │
│                                                            │
│  Gate: Fix works?                                       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 4: Verify

```
┌────────────────────────────────────────────────────────────┐
│ Step 4: Verify                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Run tests                                           │
│     - Original tests pass                               │
│     - New test passes                                   │
│     - No regressions                                   │
│                                                            │
│  2. Manual verification                                 │
│     - Follow original steps                            │
│     - Confirm bug fixed                                │
│                                                            │
│  Gate: Bug fixed and verified?                          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 5: Review & Merge

```
┌────────────────────────────────────────────────────────────┐
│ Step 5: Review & Merge                                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Open PR                                             │
│     - Title: fix(scope): [description]                   │
│     - Link to bug report                               │
│                                                            │
│  2. Review                                              │
│     - Explain root cause                               │
│     - Explain fix                                      │
│                                                            │
│  3. Merge & Deploy                                    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Checklist

```
□ Bug reproduced
□ Root cause identified
□ Fix implemented
□ Test added
□ Tests pass
□ Bug fixed (manual verify)
□ PR opened
□ PR merged
□ Deployed
```

## PR Template

```markdown
## Summary
Fix: [Brief description of bug]

## Bug Report
[Link to bug report]

## Root Cause
[What was causing the bug]

## Fix
[How the fix works]

## Testing
- [ ] Bug reproduced
- [ ] Bug fixed
- [ ] No regressions
- [ ] Test added

## Screenshots (if applicable)
```

## Severity Guide

| Severity | Definition | Response Time |
|----------|------------|--------------|
| Critical | Production down, data loss | Immediate |
| High | Major feature broken | 4 hours |
| Medium | Feature degraded | 24 hours |
| Low | Minor issue | 72 hours |

## Related Workflows

- [new-feature.md](./new-feature.md) - New feature
- [release.md](./release.md) - Release workflow
