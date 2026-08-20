---
name: debugging-and-error-recovery
description: Guides systematic root-cause debugging. Use when tests fail, builds break, behavior doesn't match expectations, or you encounter any unexpected error.
---

# Debugging and Error Recovery

## Overview

Systematic debugging with structured triage. Follow a process to find and fix the root cause.

## The Stop-the-Line Rule

```
1. STOP adding features
2. PRESERVE evidence (error output, logs)
3. DIAGNOSE using triage checklist
4. FIX the root cause
5. GUARD against recurrence
6. RESUME only after verification
```

## Triage Checklist

### Step 1: Reproduce
Make the failure happen reliably.

### Step 2: Localize
Narrow down WHERE the failure happens.

### Step 3: Reduce
Create the minimal failing case.

### Step 4: Fix the Root Cause
Fix the underlying issue, not the symptom.

### Step 5: Guard Against Recurrence
Write a test that catches this failure.

### Step 6: Verify End-to-End
Run tests, build, spot check.

## Error Patterns

### Test Failure
- Did you change code the test covers?
- Did you change unrelated code?

### Build Failure
- Type error, import error, config error, dependency error

### Runtime Error
- null/undefined, network/CORS, render error

## Safe Fallbacks

```typescript
// Safe default + warning
function getConfig(key: string): string {
  const value = process.env[key];
  if (!value) {
    console.warn(`Missing config: ${key}, using default`);
    return DEFAULTS[key] ?? '';
  }
  return value;
}
```

## Verification

- [ ] Root cause identified
- [ ] Fix addresses root cause
- [ ] Regression test added
- [ ] All tests pass
- [ ] Build succeeds
