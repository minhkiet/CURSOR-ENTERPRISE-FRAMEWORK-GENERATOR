# Performance Knowledge - Checklist

## Frontend Performance
- [ ] LCP < 2.5s measured (real users or Lighthouse)
- [ ] INP < 200ms measured
- [ ] CLS < 0.1 measured
- [ ] Images have explicit width/height attributes
- [ ] Critical CSS inlined in head
- [ ] JavaScript deferred or code-split
- [ ] Fonts use font-display: swap
- [ ] No render-blocking resources
- [ ] Lazy loading for below-fold images
- [ ] Modern image formats (WebP/AVIF)

## Database Performance
- [ ] All queries use parameterized statements
- [ ] Indexes on all foreign keys
- [ ] Indexes on columns in WHERE clauses
- [ ] EXPLAIN ANALYZE verified on slow queries
- [ ] No N+1 queries (batch loading implemented)
- [ ] Connection pooling configured
- [ ] Slow query log enabled and monitored
- [ ] Pagination implemented for large queries

## Caching
- [ ] CDN configured for static assets
- [ ] Cache-Control headers set correctly
- [ ] Redis caching for API responses
- [ ] Cache invalidation on data mutations
- [ ] Cache stampede protection implemented
- [ ] Cache hit rate > 80% for frequent reads

## API Performance
- [ ] Response compression enabled (gzip)
- [ ] Pagination on all list endpoints
- [ ] Rate limiting implemented
- [ ] No N+1 in API responses
- [ ] Field selection supported for large responses
- [ ] HTTP/2 or HTTP/3 enabled
- [ ] Connection pooling for external APIs

## Monitoring
- [ ] Core Web Vitals tracked (RUM)
- [ ] Database query times tracked
- [ ] Cache hit/miss rates tracked
- [ ] API latency tracked (p50, p95, p99)
- [ ] Performance alerts configured
- [ ] Baseline performance documented
