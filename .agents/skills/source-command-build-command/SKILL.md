---
name: "source-command-build-command"
description: "Build Feature - Xây dựng feature mới từ requirement đến implementation"
---

# source-command-build-command

Use this skill when the user asks to run the migrated source command `build-command`.

## Command Template

# Command: /build

## Mục tiêu
Xây dựng feature mới từ yêu cầu đến implementation hoàn chỉnh.

## Trigger Keywords
- build feature
- tạo feature
- xây dựng feature
- implement feature
- create feature
- new feature
- thêm feature

## Workflow

### Bước 1: Memory First
- [ ] Check `memory/decisions.sqlite` cho ADRs liên quan
- [ ] Check `memory/bugs.sqlite` cho known issues
- [ ] Check `session-summary/` cho context gần đây
- [ ] Check `technology-stack.json` cho tech stack

### Bước 2: Context Router
- [ ] Identify primary domain (frontend/backend/database/AI/infra)
- [ ] Identify secondary domains
- [ ] Load relevant rules và skills
- [ ] Load relevant knowledge files

### Bước 3: Requirement Analysis
- [ ] Understand feature requirements
- [ ] Identify functional requirements
- [ ] Identify non-functional requirements
- [ ] Check existing similar features
- [ ] Document requirements

### Bước 4: Architecture Design
- [ ] Design data model
- [ ] Design API endpoints
- [ ] Design component structure
- [ ] Create/update ADR if needed
- [ ] Apply relevant design patterns

### Bước 5: Implementation
- [ ] Setup development environment
- [ ] Implement backend (API, database, services)
- [ ] Implement frontend (components, pages)
- [ ] Implement tests
- [ ] Run linters

### Bước 6: Verification
- [ ] Run unit tests
- [ ] Run integration tests
- [ ] Code review
- [ ] Performance check
- [ ] Security check

### Bước 7: Documentation
- [ ] Update README
- [ ] Update API docs
- [ ] Update knowledge base
- [ ] Update memory (decisions, bugs if any)

## Liên kết
- [[../workflows/build-feature]] - Build Feature Workflow
- [[../prompts/feature-build]] - Feature Build Prompt
- [[../skills/feature-builder]] - Feature Builder Skill
- [[../rules/coding-standards]] - Coding Standards
