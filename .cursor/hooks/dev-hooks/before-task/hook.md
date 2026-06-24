---
description: Before-Task Hook - Load context va check memory truoc khi lam task
trigger: truoc task, before task, bat dau task
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Hook: before-task

## Muc tieu
Load context, check memory, va prepare workspace truoc khi bat dau task.

## Trigger
Tu dong trigger truoc khi bat dau moi task.

## Workflow

### Buoc 1: Task Analysis
- [ ] Parse task description
- [ ] Identify task type
- [ ] Identify affected domains
- [ ] Determine complexity

### Buoc 2: Memory Check
- [ ] Check `memory/decisions.sqlite` for related ADRs
- [ ] Check `memory/bugs.sqlite` for known issues
- [ ] Check `session-summary/` for recent context
- [ ] Return relevant memory context

### Buoc 3: Context Router
- [ ] Load context-router.json
- [ ] Identify relevant rules
- [ ] Identify relevant skills
- [ ] Identify relevant knowledge files

### Buoc 4: Skill Detection
- [ ] Apply skill-integration.mdc
- [ ] Detect applicable skills
- [ ] Load skill files
- [ ] Prepare skill context

### Buoc 5: Workspace Preparation
- [ ] Check git status
- [ ] Identify modified files
- [ ] Update code index if needed
- [ ] Prepare tool context

### Buoc 6: Report
- [ ] Print task summary
- [ ] Print loaded context
- [ ] Print applicable skills
- [ ] Print relevant rules

## Lien ket
- [[../rules/memory-first]] - Memory First Rules
- [[../rules/context-router]] - Context Router Rules
- [[../rules/skill-integration]] - Skill Integration Rules
