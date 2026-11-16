---
name: test-driven-development
description: "Strict Test-Driven Development (TDD) workflow enforcing RED-GREEN-REFACTOR cycle. Test must be executed and confirmed failing before implementation code is written, and confirmed passing cleanly after."
---

# Test-Driven Development (TDD) Skill

> **Version:** 1.0.0 | **Pillar:** Quality & Verification | **Cycle:** RED → GREEN → REFACTOR

---

## 1. Core Rule of TDD
Never write production logic without a failing test case that proves its necessity.
Writing code before test leads to confirmation bias, weak assertions, and untestable designs.

---

## 2. The 3-Phase Execution Cycle

```
┌─────────────────────────────────────────────────────────────┐
│ 1. RED Phase (Verify Test Fails Correctly)                  │
├─────────────────────────────────────────────────────────────┤
│ • Write minimal test case expressing the required behavior. │
│ • Execute the test runner (unittest, pytest, jest, etc.).   │
│ • VERIFY: Test MUST fail for the exact expected reason      │
│   (e.g., NotImplementedError, missing method, assertion).   │
│ • If test passes without code, the test is invalid!         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. GREEN Phase (Write Surgical Minimal Implementation)     │
├─────────────────────────────────────────────────────────────┤
│ • Write only the minimum code required to make test pass.   │
│ • Do not anticipate future features (strict YAGNI).         │
│ • Re-run test suite: verify ALL tests PASS.                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. REFACTOR Phase (Clean Code, Preserve Behavior)           │
├─────────────────────────────────────────────────────────────┤
│ • Remove duplicate logic (DRY).                             │
│ • Optimize naming, modularity, and readability (KISS).      │
│ • Run full test suite: ensure ZERO regression.              │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Universal TDD Quality Gate
Before declaring any feature or bugfix complete:
- [ ] Unit test written and verified failing before fix.
- [ ] Minimal implementation added to pass test.
- [ ] All existing automated tests in the repository pass.
- [ ] Edge cases covered (null/empty inputs, boundary conditions, error responses).
