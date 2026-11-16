# Quality & Verification Checklist: [Feature Name]

> **Spec:** `spec.md` | **Plan:** `plan.md` | **Tasks:** `tasks.md`

---

## 1. Specification & Requirements Verification
- [ ] Problem statement is clear, unambiguous, and justified.
- [ ] Scope boundary clearly states what is IN and OUT of scope.
- [ ] Acceptance criteria written in deterministic Given/When/Then format.
- [ ] Edge cases (empty data, network timeouts, invalid inputs) addressed.

---

## 2. Technical Architecture & Plan Verification
- [ ] Architecture respects existing codebase patterns and constitution.
- [ ] Simplicity check: adheres to YAGNI (no speculative generic helpers).
- [ ] Security reviewed: inputs validated, authorization verified, zero leaked secrets.
- [ ] Data models and API contracts defined and backwards-compatible.

---

## 3. Implementation & Testing Gates (CEF CX.1 - CX.7)
- [ ] **[CX.TDD] Strict RED-GREEN-REFACTOR**: Failing test written before production code.
- [ ] **[CX.5] Traceability**: Every added line maps directly to a task in `tasks.md`.
- [ ] **[CX.6] Zero Skeleton Code**: Complete runnable implementation without TODO placeholders.
- [ ] **[CX.7] Automated Verification**: 100% test pass with zero regression in existing test suite.
- [ ] **[§X] Line-by-Line Audit**: Diff reviewed, debug code and temporary logs removed.
