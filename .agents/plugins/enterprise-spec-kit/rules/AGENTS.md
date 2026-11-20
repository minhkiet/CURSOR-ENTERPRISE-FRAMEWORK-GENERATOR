# Enterprise Spec Kit Plugin Rules (SDD Protocol)

Whenever starting a new feature or complex refactor, the agent MUST follow the Spec-Driven Development (SDD) protocol:

## 7-Phase SDD Protocol
1. **Constitution**: Consult project constraints, architecture decision records (ADRs), and quality principles.
2. **Specify (`spec.md`)**: Define user problem, acceptance criteria, boundaries, and Given/When/Then scenarios. No code in this phase.
3. **Clarify**: Identify ambiguities or edge cases upfront before technical choices are made.
4. **Plan (`plan.md`)**: Map requirements to models, API contracts, dependencies, and testing strategies.
5. **Checklist**: Enforce explicit pass/fail checklist items before coding.
6. **Tasks (`tasks.md`)**: Break the plan into sequential, atomic, verifiable implementation slices.
7. **Implement**: Execute tasks sequentially using strict TDD (Red-Green-Refactor).
