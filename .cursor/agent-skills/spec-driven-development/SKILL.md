---
name: spec-driven-development
description: Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet.
---

# Spec-Driven Development

## Overview

Write a structured specification before writing any code. The spec defines what we're building, why, and how we'll know it's done.

## Phases

```
SPECIFY ──→ PLAN ──→ TASKS ──→ IMPLEMENT
```

### Phase 0: Scope Check
Detect if request bundles multiple capabilities.

### Phase 1: Specify
Write spec covering:
1. **Objective** — What and why
2. **Commands** — Build, test, lint commands
3. **Project Structure** — Directory layout
4. **Code Style** — Conventions
5. **Testing Strategy** — Framework, coverage
6. **Boundaries** — Always/Ask First/Never

### Phase 2: Plan
Generate technical implementation plan.

### Phase 3: Tasks
Break into discrete, implementable tasks.

### Phase 4: Implement
Execute using incremental-implementation and TDD.

## Spec Template

```markdown
# Spec: [Project/Feature]

## Objective
[What we're building and why]

## Commands
[Build, test, lint commands]

## Project Structure
[Directory layout]

## Code Style
[Conventions]

## Testing Strategy
[Framework, coverage expectations]

## Boundaries
- Always: [...]
- Ask first: [...]
- Never: [...]

## Success Criteria
[How we'll know it's done]
```

## When NOT to Use
- Single-line fixes
- Typo corrections
- Self-contained changes

## Keep Spec Alive
- Update when decisions change
- Commit the spec
- Reference in PRs
