# Performance Checklist Reference

> Based on [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) references

---

## Core Web Vitals Targets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5s - 4s | > 4s |
| **INP** (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 |

---

## Frontend Performance

### Critical Rendering Path

- [ ] Minimize critical resources
- [ ] Defer non-critical CSS/JS
- [ ] Inline critical CSS
- [ ] Preload key assets
- [ ] Preconnect to origins

### Images

- [ ] Use modern formats (WebP, AVIF)
- [ ] Responsive images with srcset
- [ ] Lazy loading for below-fold
- [ ] Explicit width/height (prevent CLS)
- [ ] Optimize images (compress, resize)
- [ ] Use CDN for static assets
- [ ] LCP image preloaded

### JavaScript

- [ ] Code splitting
- [ ] Tree shaking
- [ ] Minification
- [ ] Compression (Brotli/Gzip)
- [ ] Lazy load routes/components
- [ ] Avoid blocking scripts
- [ ] Use `defer` or `async`

### Fonts

- [ ] `font-display: swap`
- [ ] Preload fonts
- [ ] Subset fonts
- [ ] WOFF2 preferred
- [ ] System font fallback

### CSS

- [ ] Critical CSS inlined
- [ ] Non-critical deferred
- [ ] Minified
- [ ] Purge unused styles
- [ ] No render-blocking stylesheets (media='print')

---

## Bundle Analysis

### Size Budgets

| Bundle Type | Budget |
|-------------|--------|
| Initial JS | < 200KB gzipped |
| Initial CSS | < 50KB gzipped |
| Total page weight | < 3MB |
| Largest image | < 500KB |
| LCP image | < 500KB |

### Analysis Commands

```bash
# Next.js
next build && next lint
# View .next/analyze/

# Vite
vite build --mode production
npx vite-bundle-visualizer

# Webpack
npx webpack-bundle-analyzer

# Lighthouse
lighthouse https://example.com --output=html
```

---

## Backend Performance

### Database

- [ ] Indexes on query columns
- [ ] Query optimization (EXPLAIN)
- [ ] Connection pooling
- [ ] Read replicas for read-heavy
- [ ] Pagination for large datasets
- [ ] Avoid N+1 queries
- [ ] Denormalization where needed

### Caching

- [ ] HTTP caching headers
- [ ] CDN caching
- [ ] Redis/Memcached for hot data
- [ ] Cache invalidation strategy
- [ ] Cache-Control directives

### API

- [ ] Rate limiting
- [ ] Response compression
- [ ] Pagination
- [ ] Field selection
- [ ] Batch operations
- [ ] Async for heavy operations

---

## Network Optimization

### Connection Management

- [ ] Keep-alive enabled
- [ ] Connection pooling
- [ ] HTTP/2 or HTTP/3
- [ ] Reduce DNS lookups
- [ ] Preconnect to critical origins

### Resource Loading

```
Priority Order:
1. HTML document
2. Stylesheets (blocking)
3. Scripts (deferred/async)
4. Preload critical assets
5. Prefetch future pages
6. Lazy load remaining
```

### Third-Party Scripts

- [ ] Load async/defer
- [ ] Lazy load below fold
- [ ] Self-host if possible
- [ ] Monitor impact
- [ ] Allowlist only needed

---

## Rendering Performance

### Browser Rendering

- [ ] Avoid layout thrashing
- [ ] Use `transform`/`opacity` for animations
- [ ] `will-change` for animated elements
- [ ] Avoid large JS in animations
- [ ] `contain` for isolated components
- [ ] Virtualize long lists

### Animation Guidelines

| Property | Cost | Use |
|----------|------|-----|
| transform | Low | Position, scale |
| opacity | Low | Visibility |
| width/height | High | ❌ Avoid |
| top/left | High | ❌ Avoid |
| box-shadow | High | ❌ Avoid |

### Memory

- [ ] No memory leaks
- [ ] Clean up event listeners
- [ ] Avoid global state
- [ ] Use WeakMap/WeakSet
- [ ] Monitor performance.memory

---

## Measurement & Tools

### Performance Budget

```json
{
  " budgets": [
    {
      "resourceSizes": [
        { "resourceType": "total", "budget": 300 },
        { "resourceType": "script", "budget": 200 }
      ],
      "resourceCounts": [
        { "resourceType": "third-party", "budget": 10 }
      ]
    }
  ]
}
```

### Monitoring

| Metric | Tool |
|--------|------|
| Real User Monitoring | Datadog, New Relic |
| Synthetic | Lighthouse CI |
| Core Web Vitals | web-vitals library |
| Bundle | bundle-buddy |
| Bundle size | size-limit |

### Web Vitals Library

```javascript
import { onCLS, onFID, onLCP } from 'web-vitals';

function sendToAnalytics({ name, value, id }) {
  // Send to analytics
  fetch('/analytics', {
    body: JSON.stringify({ name, value, id })
  });
}

onCLS(sendToAnalytics);
onFID(sendToAnalytics);
onLCP(sendToAnalytics);
```

---

## Anti-Patterns

| Anti-Pattern | Impact | Fix |
|--------------|--------|-----|
| Large bundle | Slow load | Code split |
| Blocking scripts | Render delay | async/defer |
| Unoptimized images | High LCP | Compress, srcset |
| Layout thrashing | Jank | Batch reads/writes |
| Memory leaks | Crash | Cleanup listeners |
| Sync XHR | UI freeze | Use fetch |
| No compression | Large transfer | Enable gzip/brotli |

---

## Performance Checklist Before Launch

- [ ] Lighthouse score > 90
- [ ] LCP < 2.5s
- [ ] INP < 200ms
- [ ] CLS < 0.1
- [ ] Bundle < 200KB
- [ ] Images optimized
- [ ] Fonts optimized
- [ ] Caching headers set
- [ ] Compression enabled
- [ ] CDN configured
- [ ] Performance budget enforced
- [ ] Real user monitoring set up

---

## Links

- [agent-skills](https://github.com/addyosmani/agent-skills) - Source reference
- [web-vitals](https://github.com/GoogleChrome/web-vitals) - Core Web Vitals library
- [[skill-registry]] - Performance triggers
