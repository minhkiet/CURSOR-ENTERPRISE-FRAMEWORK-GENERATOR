---
name: "source-command-refactor-command"
description: "Refactor - Refactor code với design patterns và best practices"
---

# source-command-refactor-command

Use this skill when the user asks to run the migrated source command `refactor-command`.

## Command Template

# Command: /refactor

## Mục tiêu
Refactor code để cải thiện quality, maintainability, và performance.

## Trigger Keywords
- refactor
- tái cấu trúc
- code refactor
- improve code
- clean code
- restructure
- clean up
- code cleanup
- technical debt

## Workflow

### Bước 1: Analysis
- [ ] Load refactor-planner skill
- [ ] Analyze current code structure
- [ ] Identify refactoring opportunities
- [ ] Assess impact và risks
- [ ] Prioritize refactoring tasks

### Bước 2: Planning
- [ ] Design target structure
- [ ] Plan migration path
- [ ] Define success criteria
- [ ] Create rollback plan
- [ ] Update/create ADR if needed

### Bước 3: Implementation
- [ ] Apply refactoring incrementally
- [ ] Run tests after each change
- [ ] Maintain backward compatibility
- [ ] Update dependent code
- [ ] Run linters

### Bước 4: Verification
- [ ] Run full test suite
- [ ] Verify no regression
- [ ] Verify performance improved
- [ ] Code review

## Liên kết
- [[../prompts/refactor]] - Refactor Prompt
- [[../skills/refactor-planner]] - Refactor Planner Skill
- [[../rules/coding-standards]] - Coding Standards Rules
- [[../rules/clean-architecture]] - Clean Architecture Rules
