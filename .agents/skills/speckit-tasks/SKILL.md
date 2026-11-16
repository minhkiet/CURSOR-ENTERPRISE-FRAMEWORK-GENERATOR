---
name: speckit-tasks
description: "Decompose technical implementation plans into atomic, sequential, verifiable tasks (tasks.md) ordered by dependency and paired with automated test commands."
---

# SpecKit Tasks Skill

> **Version:** 1.0.0 | **Phase:** Task Decomposition | **Output:** `tasks.md`

---

## 1. Objective
Break down `plan.md` into granular, self-contained implementation tasks. Each task must be independently verifiable, safe to roll back, and ordered by dependency.

---

## 2. Task Formatting Standard

Every task entry in `tasks.md` must follow the format:

```markdown
- [ ] **Task X.Y: [Verb + Target Component]**
  - **Files:** `path/to/file.ext`
  - **Dependencies:** Task X.(Y-1)
  - **Action:** Exact implementation or refactoring steps.
  - **Verification:** Command to run (e.g. `pytest tests/test_feature.py -k test_happy_path`).
  - **Success Criteria:** Observable expected output or status code.
```

---

## 3. Phased Task Progression

Structure tasks into 4 logical phases:
1. **Phase 1: Test Harness & Scaffolding (RED)**
   - Create test fixtures and failing test cases covering scenarios from `spec.md`.
2. **Phase 2: Core Domain & Data Layer (GREEN)**
   - Implement data models, serialization, and business logic to satisfy tests.
3. **Phase 3: Integration & API Exposure**
   - Wire domain logic to controllers, routers, CLI commands, or UI components.
4. **Phase 4: Refactor, Polish & Audit (REFACTOR)**
   - Clean up code, check CEF Quality Gates, run linters and full regression suite.
