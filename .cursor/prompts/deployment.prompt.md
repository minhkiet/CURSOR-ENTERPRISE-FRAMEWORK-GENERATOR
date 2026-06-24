---
description: Prompt chuan de deployment - staging, production, rollback
trigger: deployment, deploy, trien khai
category: DevOps
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Prompt: Deployment - Triển khai

```markdown
# Deployment Workflow

## 1. DEPLOYMENT CONTEXT
- **Environment**: [Production / Staging / Preview]
- **Method**: [GitOps / CI-CD / Manual]
- **Strategy**: [Blue-Green / Canary / Rolling]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/docker/*
- knowledge/kubernetes/*
- knowledge/[cloud-provider]/*
Load rules: deployment.mdc, docker.mdc, [cloud-provider].mdc
```

## 3. DEPLOYMENT STEPS

### Pre-deployment
- [ ] Run tests
- [ ] Build artifacts
- [ ] Security scan
- [ ] Performance test

### Deployment
- [ ] Deploy to [target]
- [ ] Health check
- [ ] Smoke test

### Post-deployment
- [ ] Verify deployment
- [ ] Monitor metrics
- [ ] Update documentation

## 4. LIÊN KẾT
- [[../skills/deployment-review]] - Deployment Review
- [[../rules/deployment]] - Deployment Rules
```
