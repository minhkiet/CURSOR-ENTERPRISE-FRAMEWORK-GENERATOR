# Vibe Enterprise Framework — Codex Instructions

> Production-grade coding discipline, quality gates, and surgical implementation rules.
> Harmonized with Superpowers methodology (TDD, Systematic Debugging, Multi-Agent Verification).

## 1. Core Engineering Principles
- **Think Before Coding**: State assumptions, explore edge cases, and identify the simplest path before touching code.
- **Test-Driven Discipline (TDD)**: Test must be written and confirmed failing before implementation logic is created.
- **Evidence-First Debugging**: Zero guesswork. Every bug fix must begin with a deterministic reproduction.
- **Surgical Changes**: Modify only what was requested. Preserve formatting, comments, and docstrings.
- **Zero Skeleton Code**: Write complete, runnable implementations. Never leave placeholder TODOs.
- **Verify Everything**: Validate syntax, run automated unit tests, and verify edge cases before delivery.

## 2. Universal Quality Gates (CX.1 - CX.7 & Superpowers Extensions)
- **[CX.1] Pre-Flight Thinking & Brainstorming**: Analyze requirements, dependencies, and edge cases. Apply YAGNI Ladder.
- **[CX.2] Simplicity Guard**: Avoid unnecessary abstractions. YAGNI (You Aren't Gonna Need It).
- **[CX.3] Scope Discipline & Isolation**: Touch only targeted files; use git worktree isolation for major refactors.
- **[CX.4] Success Criteria & Planning**: Decompose task into atomic steps with explicit verification commands.
- **[CX.TDD] Strict RED-GREEN-REFACTOR Cycle**:
  1. *RED*: Write unit test, run test runner, verify test FAILS for the expected reason.
  2. *GREEN*: Write minimal production code to make test PASS.
  3. *REFACTOR*: Optimize clean code while keeping test suite green.
- **[CX.DBG] Systematic 4-Phase Debugging**:
  1. *Reproduce*: Create minimal reproduction test case or command.
  2. *Isolate*: Trace data flow boundaries to find the exact anomaly.
  3. *Hypothesize*: State clear cause-and-effect hypothesis before modifying code.
  4. *Verify*: Confirm reproduction test passes and full regression suite is green.
- **[CX.5] Traceability**: Every added line must directly trace to the user prompt.
- **[CX.6] Simplicity Re-check**: Review diff to remove debug code, temporary logs, or bloat.
- **[CX.7] Verification**: Run automated test suites and verify all tests pass without errors.
- **[CX.SUB] Subagent Independent Review**: When orchestrating multi-agent tasks, Maker code must be audited by an independent Verifier agent.
- **[§X] Line-by-Line Audit**: Read actual code changes before declaring the task complete.
- **[§Y] Constructive Response**: Summarize key decisions concisely and link modified files.

## 3. Tool-Specific Runtime Guidelines
- Follow standard `SKILL.md` format (lowercase hyphenated name, clear description) for all agent skills.
- Zero tolerance for UTF-8 BOM, unquoted YAML colons, or duplicate skill names across workspaces.

## 4. Verification Commands
```bash
# Run Python test suite
python -m unittest discover -s vibe_framework/tests -v

# Fast package execution via uv
uv run vibe-framework stats
```
