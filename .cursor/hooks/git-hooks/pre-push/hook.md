---
description: Pre-Push Hook - Run tests và security scan trước khi push
trigger: git push, trước push
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Hook: pre-push

## Mục tiêu
Chạy tests và security scan trước khi push lên remote.

## Trigger
Tự động trigger khi chạy `git push`.

## Workflow

### Bước 1: Determine Changes
- [ ] Get list of files being pushed
- [ ] Determine affected branches
- [ ] Check for protected branch (main, master)

### Bước 2: Branch Protection Check
- [ ] Check if pushing to protected branch
- [ ] Verify CI passed for this branch
- [ ] Check for required reviewers
- [ ] Fail if not met

### Bước 3: Test Suite
- [ ] Run full test suite
- [ ] Run integration tests
- [ ] Run E2E tests if applicable
- [ ] Fail if tests fail

### Bước 4: Security Scan
- [ ] Run dependency audit
- [ ] Scan for known vulnerabilities
- [ ] Check for secrets in code
- [ ] Fail if critical issues found

### Bước 5: Build Verification
- [ ] Run build process
- [ ] Verify build succeeds
- [ ] Check bundle size
- [ ] Fail if build fails

### Bước 6: Pre-Push Report
- [ ] Print test results
- [ ] Print security findings
- [ ] Provide push status
- [ ] Allow force push with confirmation

## Exit Codes
- `0`: Success - proceed with push
- `1`: Failure - abort push
- `2`: Warnings - allow with confirmation

## Liên kết
- [[../rules/git-workflow]] - Git Workflow Rules
- [[../rules/security]] - Security Rules
- [[../rules/testing]] - Testing Rules
- [[../rules/ci-cd]] - CI/CD Rules
