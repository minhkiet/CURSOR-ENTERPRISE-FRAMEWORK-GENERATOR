---
description: Stability and reliability skill covering error handling, resilience patterns, monitoring, and graceful degradation. Ensures applications remain operational under adverse conditions.
version: 1.0.0
created: 2026-08-03
tags: [stability, reliability, error-handling, resilience, monitoring, graceful-degradation, fault-tolerance]
role: mandatory
domains: [stability, backend, infrastructure, operations]
confidence:
  base: 0.75
  threshold: 0.75
  auto_select: true
triggers:
  - "stability"
  - "reliability"
  - "error"
  - "handle error"
  - "exception"
  - "crash"
  - "fail"
  - "resilience"
  - "retry"
  - "fallback"
  - "circuit breaker"
  - "timeout"
  - "retry"
  - "health check"
  - "monitor"
  - "alert"
  - "lỗi"
  - "xử lý lỗi"
  - "ổn định"
  - "tin cậy"
---

# Stability & Reliability Skill

## Overview

Ensures applications remain operational under adverse conditions through systematic error handling, resilience patterns, and monitoring.

## Error Handling

### 1. Error Classification

| Severity | Impact | Response |
|----------|--------|----------|
| Critical | System down | Immediate alert + auto-remediate |
| High | Major feature broken | Alert + ticket |
| Medium | Degraded experience | Log + monitor |
| Low | Minor issue | Log only |

### 2. Error Recovery Patterns

**Retry with Backoff**
```javascript
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(Math.pow(2, i) * 1000);
    }
  }
}
```

**Circuit Breaker**
```javascript
class CircuitBreaker {
  constructor(fn, threshold = 5) {
    this.fn = fn;
    this.threshold = threshold;
    this.failures = 0;
    this.state = 'CLOSED';
  }
  
  async execute() {
    if (this.state === 'OPEN') {
      throw new Error('Circuit open');
    }
    try {
      const result = await this.fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
}
```

**Graceful Degradation**
```javascript
async function getData(primaryFn, fallbackFn) {
  try {
    return await primaryFn();
  } catch (error) {
    console.warn('Primary failed, using fallback');
    return fallbackFn();
  }
}
```

## Resilience Patterns

### 1. Bulkhead
Isolate components to prevent cascade failures.

### 2. Rate Limiting
```javascript
const rateLimiter = new RateLimiter({
  maxRequests: 100,
  windowMs: 60000,
  strategy: 'sliding'
});
```

### 3. Health Checks
```javascript
app.get('/health', async (req, res) => {
  const checks = {
    db: await checkDatabase(),
    cache: await checkCache(),
    external: await checkExternal()
  };
  
  const healthy = Object.values(checks).every(Boolean);
  res.status(healthy ? 200 : 503).json({ checks });
});
```

### 4. Timeout Management
```javascript
const withTimeout = (promise, ms) => {
  return Promise.race([
    promise,
    new Promise((_, reject) => 
      setTimeout(() => reject(new Error('Timeout')), ms)
    )
  ]);
};
```

## Monitoring & Alerting

### Golden Signals
| Signal | Description | Target |
|--------|-------------|--------|
| Latency | Response time | p99 < 200ms |
| Traffic | Request volume | Stable |
| Errors | Error rate | < 0.1% |
| Saturation | Resource usage | < 80% |

### Alerting Rules
- Response time > threshold
- Error rate spike > 5%
- Memory usage > 90%
- CPU > 80% for 5min

## Quality Gates

### Pre-Deployment (§S.1)
- [ ] Error handling in place
- [ ] Fallbacks defined
- [ ] Health checks configured
- [ ] Monitoring active

### Post-Deployment (§S.2)
- [ ] Error rate stable
- [ ] No memory leaks
- [ ] Alerts firing correctly
- [ ] Recovery tested

## Anti-Patterns to Reject

- Swallowing exceptions
- No error boundaries
- Silent failures
- Infinite retry loops
- Missing timeouts
- No health checks
- Ignoring alerts
