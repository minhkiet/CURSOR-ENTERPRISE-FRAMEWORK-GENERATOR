---
description: Performance optimization skill covering memory optimization, speed enhancement, token reduction, and caching strategies. Ensures applications run efficiently and cost-effectively.
version: 1.0.0
created: 2026-08-03
tags: [performance, optimization, memory, speed, token, caching, profiling]
role: mandatory
domains: [performance, frontend, backend, infrastructure]
confidence:
  base: 0.75
  threshold: 0.75
  auto_select: true
triggers:
  - "performance"
  - "optimize"
  - "memory"
  - "speed"
  - "fast"
  - "slow"
  - "token"
  - "cost"
  - "cache"
  - "profiling"
  - "benchmark"
  - "lazy"
  - "memo"
  - "debounce"
  - "throttle"
  - "bundle"
  - "size"
  - "load time"
  - "render"
  - "fps"
  - "latency"
  - "tối ưu"
  - "hiệu năng"
  - "bộ nhớ"
  - "tốc độ"
---

# Performance Optimization Skill

## Overview

Systematic approach to performance optimization covering memory, speed, token efficiency, and caching strategies.

## Core Metrics

### Frontend Metrics
| Metric | Target | Critical |
|--------|--------|----------|
| LCP | < 2.5s | < 4s |
| INP | < 200ms | < 500ms |
| CLS | < 0.1 | < 0.25 |
| FCP | < 1.8s | < 3s |
| TTFB | < 800ms | < 1800ms |

### Backend Metrics
| Metric | Target |
|--------|--------|
| Response Time | < 200ms |
| Throughput | > 1000 req/s |
| Error Rate | < 0.1% |
| Memory Usage | < 70% |

## Optimization Categories

### 1. Memory Optimization

**Heap Analysis**
- Identify memory leaks
- Reduce object allocations
- Use WeakMap/WeakSet for caches
- Implement object pooling

**Strategies:**
```javascript
// Use WeakMap for DOM node associations
const nodeData = new WeakMap();

// Use memoization wisely
const expensiveResult = useMemo(() => computeExpensive(data), [data]);

// Clean up subscriptions
useEffect(() => {
  const sub = subscribe(handler);
  return () => sub.unsubscribe();
}, []);
```

### 2. Speed Optimization

**Code Splitting**
```javascript
const HeavyComponent = dynamic(() => import('./Heavy'), {
  loading: () => <Skeleton />
});
```

**Parallel Execution**
```javascript
// Sequential (slow)
const user = await fetchUser();
const posts = await fetchPosts();

// Parallel (fast)
const [user, posts] = await Promise.all([fetchUser(), fetchPosts()]);
```

**Lazy Loading**
```javascript
// Only load when needed
if (condition) {
  await import('./heavy-module');
}
```

### 3. Token Optimization

**Context Management**
- Minimize context size
- Use semantic compression
- Prioritize relevant knowledge
- Clear stale context

**Prompt Engineering**
- Concise instructions
- Avoid repetition
- Use references over embedding
- Batch similar operations

### 4. Caching Strategies

| Strategy | Use Case | TTL |
|----------|----------|-----|
| Memory | Session data | Short |
| Redis | Shared cache | Medium |
| CDN | Static assets | Long |
| Service Worker | Offline | Variable |

## Quality Gates

### Pre-Optimization (§P.1)
- [ ] Performance baseline established
- [ ] Profiling tools ready
- [ ] Critical metrics identified
- [ ] Budget defined

### Post-Optimization (§P.2)
- [ ] Metrics improved > 20%
- [ ] No regression introduced
- [ ] Bundle size acceptable
- [ ] Memory stable

## Anti-Patterns to Reject

- Premature optimization
- Memory leaks (unclosed streams, listeners)
- Blocking the main thread
- Large bundle without code splitting
- Inefficient loops
- N+1 queries
- Uncached repeated calculations
