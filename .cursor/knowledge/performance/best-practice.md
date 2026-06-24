# Performance Knowledge - Best Practices

## Frontend Performance
- Target Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1
- Preload critical resources: fonts, hero images, critical CSS
- Lazy load below-the-fold content: images, components, routes
- Use modern image formats: WebP, AVIF with fallbacks
- Set image dimensions: Prevent CLS from late-loading images
- Code split: Load only what the current route needs
- Tree shake: Remove unused code from bundles
- Monitor real user metrics: Not just synthetic tests

## Database Performance
- Always use parameterized queries (helps query cache)
- Index columns in WHERE, JOIN, ORDER BY clauses
- Use composite indexes for multi-column queries
- Cover indexes for read-heavy queries (include SELECT columns)
- Avoid SELECT * - only fetch needed columns
- Use EXPLAIN ANALYZE to verify index usage
- Batch operations instead of N queries
- Use pagination for large result sets
- Connection pool: Reuse connections, avoid connection exhaustion

## Caching Strategy
- Cache expensive computations: computed results, aggregations
- Cache API responses with appropriate TTLs
- Cache static assets at CDN level (1-7 days)
- Cache user-specific data in Redis with user-scoped keys
- Use cache-aside pattern: app checks cache, then DB
- Implement cache invalidation on writes
- Handle cache stampede: Use locks or probabilistic early expiration
- Separate cache clusters for different data types

## API Performance
- Return minimal data: Only include necessary fields
- Use compression: gzip for JSON responses > 1KB
- Implement pagination: Cursor-based for large datasets
- Rate limit per-client: Prevent abuse
- Use HTTP/2: Multiplexing reduces connection overhead
- Batch requests where possible: GraphQL-style queries
- Async for long operations: Return 202, process in queue

## Backend Performance
- Horizontal scaling: Stateless services behind load balancer
- Async processing: Move heavy work to background queues
- Connection pooling: Database and HTTP connection pools
- Profile before optimizing: Use APM tools to find real bottlenecks
- 80/20 rule: 80% of time spent in 20% of code
- Pre-compute expensive results: Denormalize for read-heavy workloads

## CDN & Static Assets
- Serve from CDN: Reduces latency and origin load
- Set Cache-Control headers appropriately
- Use immutable hashes for cache-busting on deployments
- Inline critical CSS in HTML head
- Defer non-critical JavaScript
- Preconnect to critical third-party origins
