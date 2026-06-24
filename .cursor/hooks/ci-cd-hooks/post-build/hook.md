---
description: Post-Build Hook - Verify artifacts sau khi build
trigger: sau build, post-build, build complete
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Hook: post-build

## Mục tiêu
Verify build artifacts sau khi build hoàn tất.

## Trigger
Tự động trigger sau khi build process hoàn tất.

## Workflow

### Bước 1: Artifact Verification
- [ ] Verify output directory exists
- [ ] Check for entry files (index.html, main.js, etc.)
- [ ] Verify file sizes are reasonable
- [ ] Check for required assets

### Bước 2: Integrity Check
- [ ] Verify build hash
- [ ] Check for source maps (if enabled)
- [ ] Verify bundle size
- [ ] Compare with previous build

### Bước 3: Quality Check
- [ ] Run bundle analyzer
- [ ] Check for dead code
- [ ] Verify tree shaking worked
- [ ] Check for duplicate dependencies

### Bước 4: Report
- [ ] Print build summary
- [ ] Print bundle sizes
- [ ] Print warnings
- [ ] Store build artifacts

## Exit Codes
- `0`: Build artifacts verified
- `1`: Artifact verification failed

## Liên kết
- [[../rules/ci-cd]] - CI/CD Rules
- [[../rules/performance]] - Performance Rules
