# Implementation Tasks: [Feature Name]

> **Spec Reference:** `spec.md` | **Plan Reference:** `plan.md`  
> **Progress:** 0 / N Tasks Completed (0%)

---

## Task Execution Instructions
1. Execute tasks in strict sequential order (Phase by Phase).
2. For every task, follow the TDD Red-Green-Refactor cycle.
3. Verify using the specified verification command before checking off `[x]`.
4. Keep atomic commits: one logical commit per task.

---

## Phase 1: Environment & Test Harness (RED)
- [ ] **Task 1.1: Setup test scaffolding & fixtures**
  - **Files:** `tests/test_[feature].py`
  - **Action:** Write failing test cases covering core acceptance scenarios from `spec.md`.
  - **Verification:** `pytest tests/test_[feature].py` (Must FAIL with expected reason).

---

## Phase 2: Core Domain & Data Layer (GREEN)
- [ ] **Task 2.1: Implement core models & data structures**
  - **Files:** `src/models/[feature].py`
  - **Action:** Define models and serialization logic.
  - **Verification:** Run type check and unit tests.
- [ ] **Task 2.2: Implement business logic service**
  - **Files:** `src/services/[feature]_service.py`
  - **Action:** Write minimal implementation to satisfy failing unit tests.
  - **Verification:** `pytest tests/test_[feature].py` (Must PASS cleanly).

---

## Phase 3: Integration & API Exposure
- [ ] **Task 3.1: Expose API routes / CLI commands**
  - **Files:** `src/api/[feature]_router.py`
  - **Action:** Connect service layer to router/CLI handler.
  - **Verification:** Test endpoint responses and error handling.

---

## Phase 4: Refactor & Polish
- [ ] **Task 4.1: Code review against CEF Quality Gates (CX.1-CX.7)**
  - **Action:** Eliminate temporary code, verify zero skeleton code, check docstrings.
  - **Verification:** Full test suite run + lint check.
- [ ] **Task 4.2: Update documentation & changelog**
  - **Files:** `docs/` or `README.md`
  - **Action:** Add usage guide and configuration reference.
