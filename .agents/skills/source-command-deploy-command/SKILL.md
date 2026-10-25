---
name: "source-command-deploy-command"
description: "Deploy - Deployment workflow từ build đến production"
---

# source-command-deploy-command

Use this skill when the user asks to run the migrated source command `deploy-command`.

## Command Template

# Command: /deploy

## Mục tiêu
Thực hiện deployment workflow từ build đến production.

## Trigger Keywords
- deploy
- deployment
- triển khai
- release
- production deploy
- staging deploy
- release deploy
- ship to production
- go live

## Workflow

### Bước 1: Pre-Deployment
- [ ] Load deployment rules
- [ ] Check environment variables
- [ ] Check secrets management
- [ ] Run tests (unit, integration)
- [ ] Security scan
- [ ] Performance baseline

### Bước 2: Build
- [ ] Build application
- [ ] Run linters
- [ ] Run type checks
- [ ] Bundle optimization
- [ ] Generate artifacts

### Bước 3: Staging Deployment
- [ ] Deploy to staging
- [ ] Smoke tests
- [ ] Integration tests
- [ ] Performance tests
- [ ] User acceptance tests

### Bước 4: Production Deployment
- [ ] Blue-green hoặc canary deployment
- [ ] Health checks
- [ ] Monitoring setup
- [ ] Rollback plan ready

### Bước 5: Post-Deployment
- [ ] Verify production health
- [ ] Check monitoring dashboards
- [ ] Verify no regression
- [ ] Update documentation

## Liên kết
- [[../workflows/deployment]] - Deployment Workflow
- [[../prompts/deployment]] - Deployment Prompt
- [[../skills/deployment-review]] - Deployment Review Skill
- [[../rules/deployment]] - Deployment Rules
- [[../rules/ci-cd]] - CI/CD Rules
- [[../rules/docker]] - Docker Rules
- [[../rules/kubernetes]] - Kubernetes Rules
