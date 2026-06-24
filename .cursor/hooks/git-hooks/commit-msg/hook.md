---
description: Commit-Msg Hook - Validate commit message format
trigger: git commit message, sau khi viết commit message
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Hook: commit-msg

## Mục tiêu
Validate commit message format trước khi commit được tạo.

## Trigger
Tự động trigger sau khi viết commit message.

## Commit Message Format

### Conventional Commits Format
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Allowed Types
| Type | Mô tả |
|------|--------|
| feat | Feature mới |
| fix | Bug fix |
| docs | Documentation |
| style | Formatting, no code change |
| refactor | Code refactoring |
| perf | Performance improvement |
| test | Adding tests |
| build | Build system, CI/CD |
| chore | Maintenance tasks |
| revert | Revert previous commit |

### Allowed Scopes
| Scope | Mô tả |
|-------|--------|
| api | API changes |
| auth | Authentication |
| db | Database |
| ui | Frontend/UI |
| api | API endpoints |
| security | Security changes |
| performance | Performance |
| docs | Documentation |
| test | Testing |
| infra | Infrastructure |
| ci | CI/CD |
| core | Core changes |

## Workflow

### Bước 1: Read Message
- [ ] Read commit message from file
- [ ] Trim whitespace
- [ ] Skip if empty (allow amend)

### Bước 2: Parse Message
- [ ] Parse type:scope:subject
- [ ] Extract body if present
- [ ] Extract footer ( trailer) if present

### Bước 3: Validate Format
- [ ] Check type is allowed
- [ ] Check scope is allowed (optional)
- [ ] Check subject is not empty
- [ ] Check subject length (max 72 chars)
- [ ] Check subject is lowercase
- [ ] Check no trailing period

### Bước 4: Validate Body
- [ ] Check body lines length (max 80 chars)
- [ ] Check body has blank line separator

### Bước 5: Special Checks
- [ ] Check for WIP commits (allow with warning)
- [ ] Check for merge commits (allow)
- [ ] Check for revert commits (allow)

## Exit Codes
- `0`: Success
- `1`: Invalid format - reject
- `2`: Warning - allow with confirmation

## Liên kết
- [[../rules/git-workflow]] - Git Workflow Rules
- [[../templates/session-summary-template]] - Session Summary Template
