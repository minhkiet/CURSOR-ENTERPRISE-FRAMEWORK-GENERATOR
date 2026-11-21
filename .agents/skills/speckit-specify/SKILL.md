---
name: speckit-specify
description: "Author high-fidelity feature specifications (spec.md) focusing on user problems, scope boundaries, and BDD Given/When/Then scenarios before technical planning."
---

# SpecKit Specify Skill

> **Version:** 1.0.0 | **Phase:** Specification Authoring | **Output:** `spec.md`

---

## 1. Objective
Author a crystal-clear feature specification (`spec.md`) that documents *what* needs to be built and *why*, without committing prematurely to implementation details or internal abstractions.

---

## 2. Specification Protocol
When invoked or requested to specify a feature:
1. **Locate or Scaffold Spec**: Verify `.specify/specs/<feature-name>/spec.md` exists (or create via `python -m vibe_framework spec init <feature-name>`).
2. **Problem Statement**: Articulate the exact user pain point or developer requirement.
3. **Scope Guard**:
   - **In Scope**: Explicit bulleted list of deliverables.
   - **Out of Scope**: Explicit list of deferred or intentionally omitted capabilities.
4. **Behavior-Driven Scenarios (Gherkin format)**:
   ```gherkin
   Scenario: [Happy path scenario]
     Given [precondition or system state]
     When [action occurs]
     Then [observable outcome]

   Scenario: [Error or edge case scenario]
     Given [invalid input or network error]
     When [action is attempted]
     Then [graceful error response]
   ```
5. **Functional & Non-Functional Requirements**: Define testable assertions (performance targets, security requirements, telemetry).
