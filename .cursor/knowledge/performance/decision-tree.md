# Performance Knowledge - Decision Tree

## Where is the bottleneck?
- Frontend heavy: Optimize images, bundle, caching
- API slow: Add caching, optimize queries, scale horizontally
- Database slow: Add indexes, optimize queries, add replicas
- External service slow: Add caching, async processing, circuit breaker

## Should we add caching?
- Read-heavy (> 80% reads): Yes, cache aggressively
- Write-heavy (> 50% writes): Be careful with cache invalidation
- Frequently changing data: Short TTL or no cache
- User-specific data: Per-user cache keys

## Should we add an index?
- Query filters on column: Consider index
- Query joins on column: Consider composite index
- Query sorts on column: Consider index
- Table < 10K rows: Probably not needed
- EXPLAIN shows sequential scan on large table: Yes

## Should we scale horizontally or vertically?
- Vertical: Simple, works for moderate scale
- Horizontal: Better for > 1000 concurrent users
- Stateless services: Easy to scale horizontally
- Stateful services: More complex, consider read replicas first

## Should we use async processing?
- Long-running task (> 1s): Yes, use queue
- External API calls: Yes, async with retries
- Batch processing: Yes, use worker pool
- Real-time needed: No, use sync with caching

## Should we optimize bundle size?
- Bundle > 500KB gzipped: Yes, tree shake and split
- Route-specific code: Code split by route
- Third-party libs: Lazy load non-critical
- Duplicate dependencies: Deduplicate
