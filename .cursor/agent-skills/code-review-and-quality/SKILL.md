---
name: code-review-and-quality
description: Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use when you need to assess code quality across multiple dimensions before it enters the main branch.
---

# Code Review and Quality

## Overview

Multi-dimensional code review with quality gates. Every change gets reviewed before merge — no exceptions. Review covers five axes: correctness, readability, architecture, security, and performance.

## When to Use

- Before merging any PR or change
- After completing a feature implementation
- When another agent or model produced code you need to evaluate
- When refactoring existing code
- After any bug fix

## The Five-Axis Review

### 1. Correctness
- Does it match the spec or task requirements?
- Are edge cases handled?
- Are error paths handled?
- Do tests verify the change?

### 2. Readability & Simplicity
- Are names descriptive?
- Is control flow straightforward?
- Is the code organized logically?
- Could this be simpler?

### 3. Architecture
- Does it follow existing patterns?
- Are dependencies flowing correctly?
- Is the abstraction level appropriate?

### 4. Security
- Is input validated and sanitized?
- Are secrets kept out of code?
- Are SQL queries parameterized?

### 5. Performance
- Any N+1 query patterns?
- Any unbounded operations?
- Any missing pagination?

## Change Sizing

| Lines Changed | Assessment |
|---------------|------------|
| ~100 | Good — reviewable |
| ~300 | Acceptable |
| ~1000 | Too large — split |

## Review Checklist

```markdown
## Review Checklist

### Correctness
- [ ] Matches spec/task
- [ ] Edge cases handled
- [ ] Error paths covered
- [ ] Tests adequate

### Readability
- [ ] Clear names
- [ ] Straightforward logic
- [ ] No unnecessary complexity

### Architecture
- [ ] Follows patterns
- [ ] Clean boundaries
- [ ] Right abstraction

### Security
- [ ] Input validated
- [ ] No secrets
- [ ] Auth checked

### Performance
- [ ] No N+1
- [ ] No unbounded ops
- [ ] Pagination present
```
