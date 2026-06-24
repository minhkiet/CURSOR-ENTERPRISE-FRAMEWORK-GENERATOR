---
description: Post-Deploy Hook - Health check và notify sau deploy
trigger: sau deploy, post-deploy, deployment complete
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Hook: post-deploy

## Mục tiêu
Health check, verification, và notification sau khi deploy hoàn tất.

## Trigger
Tự động trigger sau khi deploy hoàn tất.

## Workflow

### Bước 1: Health Check
- [ ] GET health endpoint
- [ ] Check database connectivity
- [ ] Check cache connectivity
- [ ] Check queue connectivity
- [ ] Wait for warmup if needed

### Bước 2: Smoke Test
- [ ] Test critical endpoints
- [ ] Test authentication flow
- [ ] Test basic CRUD operations
- [ ] Verify no errors

### Bước 3: Monitoring Setup
- [ ] Verify logging active
- [ ] Verify metrics active
- [ ] Verify alerting configured
- [ ] Verify dashboards updated

### Bước 4: Notification
- [ ] Send deployment notification
- [ ] Include version info
- [ ] Include changelog
- [ ] Include health status

### Bước 5: Documentation
- [ ] Update deployment log
- [ ] Update service catalog
- [ ] Update runbook

## Exit Codes
- `0`: Deployment successful
- `1`: Health check failed - trigger rollback

## Liên kết
- [[../rules/deployment]] - Deployment Rules
- [[../rules/monitoring]] - Monitoring Rules
- [[../rules/incident-response]] - Incident Response Rules
