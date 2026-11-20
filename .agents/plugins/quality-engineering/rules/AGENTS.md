# Quality Engineering Plugin Rules

Tests are proof, not decoration. The agent must enforce the Prove-It pattern:

## Prove-It Pattern
1. **Red**: Write a minimal failing unit/integration test before touching implementation code.
2. **Green**: Write the minimal code required to satisfy the test.
3. **Refactor**: Clean up the design, remove duplication, and preserve green tests.

## Coverage Requirements
- Happy path: 100%
- Error paths & edge cases: ≥ 80%
- Zero tolerance for placeholder `TODO` comments or stub code that "almost works".
