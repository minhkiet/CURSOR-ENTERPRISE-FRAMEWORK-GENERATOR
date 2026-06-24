---
description: Post-Checkout Hook - Update workspace context sau checkout
trigger: git checkout (sau khi checkout thanh cong)
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Hook: post-checkout

## Muc tieu
Cap nhat workspace context sau khi checkout thanh cong (branch hoac file).

## Trigger
Tu dong trigger sau khi `git checkout` hoan tat.

## Workflow

### Buoc 1: Get Checkout Info
- [ ] Get previous branch
- [ ] Get new branch
- [ ] Get list of changed files
- [ ] Determine if branch or file checkout

### Buoc 2: Update Workspace Context
- [ ] Detect technology stack from files
- [ ] Update code index if new files
- [ ] Reload relevant domain knowledge
- [ ] Clear stale caches

### Buoc 3: Environment Check
- [ ] Check for new dependencies
- [ ] Check for new environment variables
- [ ] Warn if build config changed

### Buoc 4: Report
- [ ] Print branch info
- [ ] Print changed files summary
- [ ] Print loaded context

## Exit Codes
- `0`: Always succeed (informational only)

## Lien ket
- [[../rules/memory-first]] - Memory First Rules
- [[../rules/context-router]] - Context Router Rules
- [[../hooks/dev-hooks/before-task]] - Before Task Hook
