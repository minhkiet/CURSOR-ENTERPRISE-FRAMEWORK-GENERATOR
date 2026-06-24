---
description: Pre-Rebase Hook - Check conflicts truoc khi rebase
trigger: git rebase, truoc rebase
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Hook: pre-rebase

## Muc tieu
Kiem tra conflicts va tien quyet truoc khi thuc hien rebase.

## Trigger
Tu dong trigger truoc khi chay `git rebase`.

## Workflow

### Buoc 1: Get Rebase Info
- [ ] Get source branch
- [ ] Get target branch
- [ ] Get number of commits being rebased

### Buoc 2: Check Working Directory
- [ ] Verify working directory is clean
- [ ] Warn if uncommitted changes exist
- [ ] Suggest stash if needed

### Buoc 3: Check Branch Protection
- [ ] Verify branch is not protected
- [ ] Warn if rebasing shared branches
- [ ] Check for active PRs

### Buoc 4: Backup
- [ ] Create backup branch before rebase
- [ ] Tag backup with timestamp
- [ ] Report backup info

## Exit Codes
- `0`: Ready to rebase
- `1`: Not ready - abort rebase (dirty working directory)

## Lien ket
- [[../rules/git-workflow]] - Git Workflow Rules
- [[../rules/memory-first]] - Memory First Rules
