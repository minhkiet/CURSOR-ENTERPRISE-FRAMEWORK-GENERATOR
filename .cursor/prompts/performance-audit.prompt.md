---
description: Prompt chuan de audit hieu nang - database, API, frontend
trigger: performance audit, toi uu hieu nang
category: Performance
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Prompt: Performance Audit - Kiểm tra hiệu năng

## Mô tả
Prompt template chuẩn để thực hiện performance audit toàn diện.

## Trigger Keywords
- "performance audit"
- "tối ưu hiệu năng"
- "performance review"
- "optimize"
- "tối ưu"

## Prompt Template

```markdown
# Performance Audit Workflow

## 1. AUDIT SCOPE
- **Audit ID**: [AUDIT-ID]
- **Scope**: [Full / Partial / API / Database / Frontend]
- **Domain**: [Xác định domain]
- **Baseline**: [Current metrics]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/performance/*
- knowledge/database/*
- knowledge/redis/*
- knowledge/[relevant-stack]/*
Load rules: performance.mdc, database.mdc, redis.mdc
```

## 3. METRICS COLLECTION

### Backend Metrics
- [ ] Response time (p50, p95, p99)
- [ ] Throughput (req/s)
- [ ] Error rate
- [ ] CPU usage
- [ ] Memory usage

### Database Metrics
- [ ] Query execution time
- [ ] Connection pool usage
- [ ] Index hit rate
- [ ] Cache hit rate
- [ ] Lock contention

### Frontend Metrics
- [ ] FCP (First Contentful Paint)
- [ ] LCP (Largest Contentful Paint)
- [ ] FID (First Input Delay)
- [ ] CLS (Cumulative Layout Shift)
- [ ] TTFB (Time to First Byte)

## 4. AUDIT AREAS

### Database Optimization
- [ ] Query analysis (EXPLAIN)
- [ ] Index review
- [ ] Query optimization
- [ ] Connection pooling
- [ ] Sharding/replication

### Caching Strategy
- [ ] Redis cache
- [ ] CDN usage
- [ ] Application cache
- [ ] Database cache
- [ ] Cache invalidation

### API Optimization
- [ ] Pagination
- [ ] Compression
- [ ] Batch endpoints
- [ ] GraphQL vs REST
- [ ] CORS optimization

### Frontend Optimization
- [ ] Bundle size
- [ ] Code splitting
- [ ] Lazy loading
- [ ] Image optimization
- [ ] CSS optimization

## 5. FINDINGS

### Critical Performance Issues
| ID | Issue | Location | Impact | Recommendation |
|----|-------|----------|--------|----------------|
| P-001 | [Issue] | [File] | [ms lost] | [Fix] |

## 6. LIÊN KẾT
- [[../skills/performance-audit]] - Performance Audit
- [[../skills/database-optimization]] - Database Optimization
- [[../skills/redis-audit]] - Redis Audit
- [[../rules/performance]] - Performance Rules
- [[../rules/database]] - Database Rules
