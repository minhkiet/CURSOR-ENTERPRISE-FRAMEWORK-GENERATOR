---
name: code-simplification
description: Simplifies code for clarity. Use when refactoring code for clarity without changing behavior. Use when code works but is harder to read, maintain, or extend than it should be.
---

# Code Simplification

## Overview

Simplify code by reducing complexity while preserving exact behavior. The goal is code that is easier to read, understand, modify, and debug.

## When to Use

- After a feature works but feels heavier than needed
- During code review when complexity issues are flagged
- When encountering deeply nested logic, long functions, unclear names

## Five Principles

### 1. Preserve Behavior Exactly
All inputs, outputs, side effects, error behavior must remain identical.

### 2. Follow Project Conventions
Match existing patterns, naming, and style.

### 3. Prefer Clarity Over Cleverness
Explicit code beats compact code.

### 4. Maintain Balance
Avoid over-simplification.

### 5. Scope to What Changed
Focus on recently modified code.

## Simplification Patterns

| Pattern | Signal | Simplification |
|---------|--------|----------------|
| Deep nesting | 3+ levels | Guard clauses or helpers |
| Long functions | 50+ lines | Split by responsibility |
| Nested ternaries | Hard to parse | if/else or lookup object |
| Generic names | data, temp, val | Descriptive names |
| Duplicated logic | Same 5+ lines | Shared function |

## Process

1. Understand before touching (Chesterton's Fence)
2. Identify opportunities
3. Apply incrementally — run tests after each
4. Verify the result

## Verification

- [ ] All tests pass
- [ ] Build succeeds
- [ ] Code is genuinely simpler
- [ ] Follows project conventions
