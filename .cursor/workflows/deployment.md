# Workflow: Deployment - Triển khai

## Mục tiêu
Workflow chuẩn để deploy ứng dụng.

## Trigger
Khi user yêu cầu deploy.

## Workflow Steps

### Bước 1: Pre-deployment
- [ ] Run tests
- [ ] Build artifacts
- [ ] Security scan
- [ ] Create backup

### Bước 2: Deployment
- [ ] Deploy to target
- [ ] Health check
- [ ] Smoke test

### Bước 3: Post-deployment
- [ ] Verify deployment
- [ ] Monitor logs
- [ ] Update DNS (if needed)

## Liên kết
- [[../prompts/deployment]] - Deployment Prompt
- [[../skills/deployment-review]] - Deployment Review Skill
- [[../rules/deployment]] - Deployment Rules
