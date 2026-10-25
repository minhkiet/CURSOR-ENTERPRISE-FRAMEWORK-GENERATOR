---
name: planning-and-task-breakdown
description: Breaks work into ordered tasks. Use when you have a spec and need to break work into implementable tasks.
---

# Planning and Task Breakdown

## Overview

Decompose work into small, verifiable tasks with explicit acceptance criteria.

## When to Use

- Have a spec and need to break into units
- Task feels too large or vague
- Work needs parallelization
- Need to communicate scope

## Process

### Step 1: Enter Plan Mode
Read-only mode — no code changes.

### Step 2: Identify Dependency Graph
Map what depends on what.

### Step 3: Slice Vertically
Build complete feature paths, not layers.

### Step 4: Write Tasks
```markdown
## Task N: [Title]

**Acceptance criteria:**
- [ ] [Condition]

**Verification:**
- [ ] Tests pass
- [ ] Build succeeds

**Dependencies:** [Task N or None]
```

### Step 5: Order and Checkpoint
Arrange by dependencies, add checkpoints.

## Task Sizing

| Size | Files | Scope |
|------|-------|-------|
| XS | 1 | Single function |
| S | 1-2 | One component |
| M | 3-5 | One feature slice |
| L | 5-8 | Multi-component |
| XL | 8+ | Too large — split |

## Output Files
- Plan: `tasks/plan.md`
- Tasks: `tasks/todo.md`

## Verification
- [ ] Every task has acceptance criteria
- [ ] Dependencies identified
- [ ] Checkpoints exist
- [ ] Human approved plan
