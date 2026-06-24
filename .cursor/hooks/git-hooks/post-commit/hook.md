---
description: Post-Commit Hook - Update session summary sau commit
trigger: git commit (sau khi commit thanh cong)
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Hook: post-commit

## Muc tieu
Cap nhat session summary va memory sau khi commit thanh cong.

## Trigger
Tu dong trigger sau khi commit thanh cong.

## Workflow

### Buoc 1: Get Commit Info
- [ ] Get commit hash
- [ ] Get commit message
- [ ] Get author
- [ ] Get timestamp
- [ ] Get list of changed files

### Buoc 2: Update Session Summary
- [ ] Load current session summary
- [ ] Add commit to history
- [ ] Update context
- [ ] Save session summary

### Buoc 3: Update Memory
- [ ] Check for new ADRs to add
- [ ] Check for bug fixes to log
- [ ] Update decision memory if needed
- [ ] Update code index if needed

### Buoc 4: Cleanup
- [ ] Clear staged changes indicator
- [ ] Update git status cache
- [ ] Print summary

## Exit Codes
- `0`: Always succeed (informational only)

## Lien ket
- [[../rules/memory-first]] - Memory First Rules
- [[../scripts/memory-builder]] - Memory Builder Script
- [[../memory/]] - Memory Directory
