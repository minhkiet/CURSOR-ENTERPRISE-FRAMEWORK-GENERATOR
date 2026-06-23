# Prompt: Cost Reduction - Giảm chi phí

```markdown
# Cost Reduction Workflow

## 1. COST ANALYSIS
- **Scope**: [Infrastructure / Database / AI / Storage / Network]
- **Current Spend**: [Amount/month]
- **Target Reduction**: [Percentage]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/[cloud-provider]/*
- knowledge/docker/*
- knowledge/postgres/*
- knowledge/redis/*
Load rules: cost-optimization.mdc, [cloud-provider].mdc
```

## 3. OPTIMIZATION AREAS

### Infrastructure
- [ ] Right-sizing instances
- [ ] Spot/preemptible instances
- [ ] Reserved capacity
- [ ] Auto-scaling policies

### Database
- [ ] Connection pooling
- [ ] Query optimization
- [ ] Storage tiering
- [ ] Backup strategy

### AI/LLM
- [ ] Model selection
- [ ] Caching responses
- [ ] Batching requests
- [ ] Prompt optimization

### Storage
- [ ] Lifecycle policies
- [ ] Compression
- [ ] CDN caching
- [ ] Archive tier

## 4. LIÊN KẾT
- [[../skills/cost-optimization-review]] - Cost Optimization
- [[../rules/cost-optimization]] - Cost Optimization Rules
```
