---
description: Pre-Deploy Hook - Final checks trước khi deploy
trigger: trước deploy, pre-deploy, deployment check
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Hook: pre-deploy

## Mục tiêu
Final checks và validations trước khi deploy.

## Trigger
Tự động trigger trước khi deploy process bắt đầu.

## Workflow

### Bước 1: Build Verification
- [ ] Verify build artifacts exist
- [ ] Verify build passed
- [ ] Verify no build errors

### Bước 2: Environment Check
- [ ] Verify target environment
- [ ] Check environment variables
- [ ] Verify secrets are set
- [ ] Verify network access

### Bước 3: Health Check
- [ ] Verify database connectivity
- [ ] Verify cache connectivity
- [ ] Verify queue connectivity
- [ ] Verify external services

### Bước 4: Security Check
- [ ] Verify no debug mode
- [ ] Verify HTTPS enforced
- [ ] Verify secrets not in code
- [ ] Verify CORS configured

### Bước 5: Rollback Check
- [ ] Verify previous version exists
- [ ] Verify rollback procedure
- [ ] Verify monitoring active

### Bước 6: Report
- [ ] Print environment info
- [ ] Print health status
- [ ] Print deployment plan
- [ ] Confirm deployment

## Exit Codes
- `0`: Ready to deploy
- `1`: Not ready - abort deploy

## Liên kết
- [[../rules/deployment]] - Deployment Rules
- [[../rules/security]] - Security Rules
- [[../workflows/deployment]] - Deployment Workflow
