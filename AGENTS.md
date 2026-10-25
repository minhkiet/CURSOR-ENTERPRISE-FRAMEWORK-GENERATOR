# Codex Enterprise Framework — Codex Instructions

> Production-grade coding discipline, quality gates, and surgical implementation rules.

## 1. Core Engineering Principles
- **Think Before Coding**: State assumptions and identify the simplest path before touching code.
- **Surgical Changes**: Modify only what was requested. Preserve formatting, comments, and docstrings.
- **Zero Skeleton Code**: Write complete, runnable implementations. Never leave placeholder TODOs.
- **Verify Everything**: Validate syntax, run automated unit tests, and verify edge cases before delivery.

## 2. Universal Quality Gates (CX.1 - CX.7)
- **[CX.1] Pre-Flight Thinking**: Analyze requirements, dependencies, and potential side effects.
- **[CX.2] Simplicity Guard**: Avoid unnecessary abstractions. YAGNI (You Aren't Gonna Need It).
- **[CX.3] Scope Discipline**: Touch only targeted files; do not refactor unrelated modules.
- **[CX.4] Success Criteria**: Define clear, testable outputs before starting implementation.
- **[CX.5] Traceability**: Every added line must directly trace to the user prompt.
- **[CX.6] Simplicity Re-check**: Review diff to remove debug code, temporary logs, or bloat.
- **[CX.7] Verification**: Run automated test suites and verify all tests pass without errors.
- **[§X] Line-by-Line Audit**: Read actual code changes before declaring the task complete.
- **[§Y] Constructive Response**: Summarize key decisions concisely and link modified files.

## 3. Tool-Specific Runtime Guidelines
- Refer to `AGENTS.md` for framework rules and versioning conventions.

## 4. Verification Commands
```bash
# Run Python test suite
python -m unittest discover -s cursor_framework/tests -v

# Fast package execution via uv
uv run cursor-framework stats
```
