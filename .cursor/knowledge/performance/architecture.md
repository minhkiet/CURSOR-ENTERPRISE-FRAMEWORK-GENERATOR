# Performance Knowledge - Architecture

## Performance Optimization Layers
```
[User] --> [CDN] --> [Load Balancer] --> [API Server] --> [Cache] --> [Database]
                                    |                  |
                                    +--> [Queue] --> [Workers]
```

## Caching Architecture
```
[Request] --> [CDN Cache] --> [API Cache (Redis)] --> [Application Cache] --> [Database]
                  |                   |                      |
               Static assets       API responses          In-memory
               (1-7 days)          (1-60 min)           (request scope)
```

## Database Optimization
- Connection pooling: PgBouncer, HikariCP
- Read replicas: Separate read/write queries
- Partitioning: Table partitioning by date/tenant
- Indexing strategy: Composite indexes, partial indexes
- Query analysis: EXPLAIN ANALYZE

## Frontend Performance
- Bundle optimization: Code splitting, tree shaking
- Image pipeline: WebP/AVIF, lazy loading, responsive images
- Font optimization: Font-display: swap, subset fonts
- Critical path: Inline critical CSS, defer non-critical JS
- Service workers: Offline caching, background sync

## API Performance
- Response compression: gzip/brotli for JSON responses
- Connection reuse: HTTP/2 multiplexing
- Batch endpoints: Single endpoint for multiple reads
- Field selection: GraphQL-style field filtering
- Pagination: Cursor-based for large datasets

## Performance Monitoring
```
[Real User Monitoring] --> [Lighthouse/PageSpeed]
         |                       |
    Core Web Vitals          Lab measurements
    (Field data)             (Lab data)
```
