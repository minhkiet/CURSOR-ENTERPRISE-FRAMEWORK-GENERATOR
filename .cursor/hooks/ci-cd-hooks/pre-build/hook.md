---
description: Pre-Build Hook - Verify dependencies trước khi build
trigger: trước build, pre-build, CI build
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Hook: pre-build

## Mục tiêu
Verify dependencies và environment trước khi build.

## Trigger
Tự động trigger trước khi build process bắt đầu.

## Workflow

### Bước 1: Environment Check
- [ ] Check Node.js version
- [ ] Check npm/yarn/pnpm version
- [ ] Check environment variables
- [ ] Check required secrets

### Bước 2: Dependency Check
- [ ] Verify node_modules exists
- [ ] Check package-lock.json matches package.json
- [ ] Check for missing dependencies
- [ ] Verify peer dependencies

### Bước 3: Config Check
- [ ] Verify build configuration exists
- [ ] Check TypeScript config
- [ ] Check environment configs
- [ ] Validate secrets

### Bước 4: Cache Check
- [ ] Check for build cache
- [ ] Check cache validity
- [ ] Prepare cache for build

### Bước 5: Report
- [ ] Print environment info
- [ ] Print cache status
- [ ] Provide build readiness

## Exit Codes
- `0`: Ready to build
- `1`: Not ready - abort build

## Liên kết
- [[../rules/ci-cd]] - CI/CD Rules
- [[../rules/deployment]] - Deployment Rules
