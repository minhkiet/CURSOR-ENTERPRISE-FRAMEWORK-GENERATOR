# Debug Error Skill

> **Version:** 1.0.0 | **Category:** Development | **Triggers:** debug, fix bug, error, lỗi, troubleshoot

---

## Goal

Debug và fix lỗi systematic:
- Reproduce the issue
- Identify root cause
- Implement fix
- Verify solution

## Trigger Conditions

- Bug report filed
- User report error
- Tests failing
- Production incident

## Pre-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ P.1: Gather Information                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Đã reproduce được lỗi?                                 │
│ □ Có error message/stack trace?                           │
│ □ Có steps to reproduce?                                   │
│ □ Environment nào (dev/staging/prod)?                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Debug Process

### Phase 1: Reproduce

```
┌────────────────────────────────────────────────────────────┐
│ Reproduce the Issue                                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Verify the bug exists                                 │
│     - Follow exact steps to reproduce                     │
│     - Document what happens vs expected                   │
│                                                            │
│  2. Isolate the conditions                                │
│     - What inputs trigger it?                             │
│     - What environment?                                   │
│     - What user actions?                                  │
│                                                            │
│  3. Create minimal reproduction                           │
│     - Strip down to minimum code                         │
│     - Identify the failing path                          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Phase 2: Identify Root Cause

```
┌────────────────────────────────────────────────────────────┐
│ Root Cause Analysis                                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Narrow down the location                             │
│     - Which layer? (UI/API/DB)                          │
│     - Which file/function?                               │
│     - Which line?                                        │
│                                                            │
│  2. Trace the data flow                                  │
│     - Where does it originate?                           │
│     - How does it transform?                             │
│     - Where does it fail?                                │
│                                                            │
│  3. Form hypothesis                                     │
│     - What is causing the bug?                          │
│     - Why is it happening?                              │
│                                                            │
│  4. Verify hypothesis                                   │
│     - Add logging/breakpoint                            │
│     - Confirm the cause                                  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Phase 3: Implement Fix

```
┌────────────────────────────────────────────────────────────┐
│ Implement Solution                                         │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Design the fix                                       │
│     - What needs to change?                             │
│     - What are the side effects?                        │
│     - What's the minimal fix?                            │
│                                                            │
│  2. Implement carefully                                  │
│     - Don't introduce new bugs                          │
│     - Keep changes minimal                              │
│     - Follow existing patterns                          │
│                                                            │
│  3. Test the fix                                        │
│     - Does it solve the original issue?                 │
│     - Does it break anything else?                      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Phase 4: Verify

```
┌────────────────────────────────────────────────────────────┐
│ Verify Solution                                           │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Run tests                                           │
│     - Unit tests pass                                   │
│     - Integration tests pass                            │
│     - No regressions                                   │
│                                                            │
│  2. Manual verification                                  │
│     - Follow original steps                             │
│     - Confirm fix works                                 │
│                                                            │
│  3. Check edge cases                                    │
│     - Boundary conditions                               │
│     - Error paths                                      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Common Bug Patterns

### Logic Errors

```typescript
// Bug: Wrong comparison
if (userAge < 18) { ... }  // Should be <=

// Fix: Correct comparison
if (userAge <= 18) { ... }
```

### Null/Undefined

```typescript
// Bug: Not handling null
const name = user.profile.name; // Crashes if profile is null

// Fix: Optional chaining
const name = user.profile?.name ?? 'Anonymous';
```

### Async Issues

```typescript
// Bug: Not awaiting
function getUser() {
  fetchUser(); // Returns Promise, not user
  return result; // result is undefined
}

// Fix: Await properly
async function getUser() {
  const result = await fetchUser();
  return result;
}
```

### Race Conditions

```typescript
// Bug: Race condition
async function loadData() {
  fetchData();   // Not awaited
  fetchMore();   // Not awaited
  return data;   // data not ready
}

// Fix: Await all
async function loadData() {
  await Promise.all([fetchData(), fetchMore()]);
  return data;
}
```

## Debug Tools

| Tool | Use Case |
|------|----------|
| `console.log` | Quick logging |
| `debugger` | Breakpoints |
| `try/catch` | Error handling |
| `jest --watch` | Test debugging |
| Chrome DevTools | Frontend debugging |
| PostgreSQL `EXPLAIN` | Query analysis |

## Output

```
✅ Bug Fixed
├── Root cause identified
├── Fix implemented
├── Tests added/updated
├── Documentation updated (if needed)
└── PR ready for review
```

## Anti-Patterns to Avoid

```
❌ Guessing and trying random fixes
❌ Ignoring error messages
❌ Not reproducing the issue first
❌ Fixing symptoms instead of cause
❌ Not testing the fix
❌ Introducing new bugs
❌ Over-engineering the fix
```
