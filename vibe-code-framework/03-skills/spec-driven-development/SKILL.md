---
name: spec-driven-development
description: "Master Spec-Driven Development (SDD) orchestrator inspired by GitHub Spec Kit. Enforces 7-phase structured workflow: Constitution -> Specify -> Clarify -> Plan -> Checklist -> Tasks -> Implement with strict TDD."
---

# Spec-Driven Development (SDD) Skill

> **Version:** 1.0.0 | **Framework:** Vibe Enterprise Framework & GitHub Spec Kit Compatible
> **Core Philosophy:** Intent & Specifications before Implementation | Test-Driven Discipline

---

## 1. Overview & Workflow Lifecycle

Spec-Driven Development replaces ad-hoc "vibe coding" with a systematic, deterministic development lifecycle:

```
[Phase 1: Constitution]  ➔  [Phase 2: Specify]  ➔  [Phase 3: Clarify]
           │
           ▼
   [Phase 4: Plan]       ➔  [Phase 5: Checklist]
           │
           ▼
   [Phase 6: Tasks]      ➔  [Phase 7: Implement (TDD)]
```

Every feature lives under `.specify/specs/<feature-name>/`:
- `spec.md`: What to build, why, and acceptance criteria (BDD scenarios).
- `plan.md`: Technical architecture, data models, API contracts, risk assessment.
- `tasks.md`: Atomic, dependency-ordered task breakdown with verification commands.
- `checklist.md`: Quality gates (CEF CX.1 - CX.7) & verification checks.

---

## 2. The 7 Phases

### Phase 1: Constitution (`/speckit.constitution`)
- **Goal:** Establish or verify project-wide ground rules, invariants, and quality gates.
- **Location:** `.specify/constitution.md`
- **Enforcement:** Stack versions, standard library first, zero unvetted dependencies, TDD requirement.

### Phase 2: Specify (`/speckit.specify`)
- **Goal:** Define user requirements, problem motivation, scope boundaries, and BDD scenarios.
- **Output:** `spec.md`
- **Rules:** Focus strictly on *what* and *why*. Do NOT prescribe code or internal data structures yet.

### Phase 3: Clarify (`/speckit.clarify`)
- **Goal:** Surface edge cases, missing requirements, and potential pitfalls before architecture design.
- **Action:** Ask targeted questions to resolve ambiguities or document safe defaults.

### Phase 4: Plan (`/speckit.plan`)
- **Goal:** Architect the technical blueprint based on the specification and constitution.
- **Output:** `plan.md`
- **Content:** Component diagram, file impact map, data models, API endpoints, testing strategy, rollback plan.

### Phase 5: Checklist (`/speckit.checklist`)
- **Goal:** Audit the spec and plan against CEF Universal Quality Gates (CX.1 - CX.7).
- **Output:** `checklist.md`
- **Gates:** Simplicity check (YAGNI), security review, test harness completeness.

### Phase 6: Tasks (`/speckit.tasks`)
- **Goal:** Deconstruct technical plan into atomic, sequential, verifiable tasks.
- **Output:** `tasks.md`
- **Format:** Every task must specify target files, action, and explicit verification commands.

### Phase 7: Implement (`/speckit.implement`)
- **Goal:** Execute tasks sequentially with strict TDD (Red-Green-Refactor).
- **Execution Rules:**
  - Write test first; confirm test fails with expected failure reason (RED).
  - Write minimal code to pass test (GREEN).
  - Refactor for cleanliness while maintaining passing test suite (REFACTOR).
  - Update `tasks.md` checklist items `[ ]` to `[x]` as each task completes.

---

## 3. CLI Helper Integration

```bash
# Initialize a new feature spec bundle:
python -m vibe_framework spec init <feature-name>

# List all specs and progress:
python -m vibe_framework spec list

# Check status & progress of a feature:
python -m vibe_framework spec status <feature-name>

# Validate against quality gates:
python -m vibe_framework spec validate <feature-name>
```
