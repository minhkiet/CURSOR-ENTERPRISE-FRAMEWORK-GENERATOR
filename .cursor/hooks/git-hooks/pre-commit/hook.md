---
description: Pre-Commit Hook - Lint, format, type check trước khi commit
trigger: git commit, trước commit
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Hook: pre-commit

## Mục tiêu
Chạy linting, formatting, và type checking trước khi commit.

## Trigger
Tự động trigger khi chạy `git commit`.

## Workflow

### Bước 1: Staged Files Check
- [ ] Get list of staged files
- [ ] Filter by file type (ts, js, tsx, jsx, etc.)
- [ ] Skip binary files

### Bước 2: Lint Check
- [ ] Run ESLint / TSLint
- [ ] Check for errors
- [ ] Auto-fix if possible
- [ ] Fail if errors cannot be auto-fixed

### Bước 3: Format Check
- [ ] Run Prettier
- [ ] Check formatting
- [ ] Auto-fix formatting issues
- [ ] Warn if formatting changed

### Bước 4: Type Check
- [ ] Run TypeScript compiler
- [ ] Check for type errors
- [ ] Fail if type errors found

### Bước 5: Test Check (optional)
- [ ] Run tests for changed files
- [ ] Fail if tests fail
- [ ] Skip if `--no-verify` used

### Bước 6: Security Check
- [ ] Scan for secrets in staged files
- [ ] Check for hardcoded credentials
- [ ] Fail if secrets found

### Bước 7: Report
- [ ] Print summary
- [ ] Show files modified by hooks
- [ ] Provide instructions to continue

## Exit Codes
- `0`: Success - proceed with commit
- `1`: Failure - abort commit
- `2`: Warnings only - allow commit with confirmation

## Liên kết
- [[../rules/coding-standards]] - Coding Standards
- [[../rules/security]] - Security Rules
- [[../rules/git-workflow]] - Git Workflow Rules
