# Performance Knowledge - Glossary

## Core Concepts
- **LCP (Largest Contentful Paint)**: Time to render largest visible element
- **INP (Interaction to Next Paint)**: Responsiveness to user interactions
- **CLS (Cumulative Layout Shift)**: Visual stability score
- **TTFB (Time To First Byte)**: Server response time
- **FP (First Paint)**: Time to first pixel render
- **FCP (First Contentful Paint)**: Time to first content render

## Database Terms
- **N+1 query**: Making N+1 database calls instead of 1 batch query
- **Query plan**: How database executes a query
- **Index scan vs sequential scan**: Different query execution strategies
- **Connection pool**: Reusable database connections
- **Slow query**: Query exceeding defined threshold (e.g., > 100ms)

## Caching Terms
- **Cache hit**: Data served from cache
- **Cache miss**: Cache lookup failed, fetch from source
- **Cache invalidation**: Removing stale data from cache
- **TTL (Time To Live)**: How long cached data is valid
- **Cache stampede**: Multiple requests hitting cache miss simultaneously
- **Write-through**: Update cache and DB simultaneously
- **Write-behind**: Update DB, update cache async

## Frontend Terms
- **Bundle size**: Total JavaScript size
- **Code splitting**: Loading JS in chunks
- **Tree shaking**: Removing unused code
- **Lazy loading**: Loading resources on demand
- **Image optimization**: Compressing and sizing images
- **Critical CSS**: CSS needed for above-the-fold content

## API Performance
- **P50/P95/P99 latency**: Response time percentiles
- **Throughput**: Requests processed per second
- **Rate limiting**: Throttling excessive requests
- **Connection reuse**: HTTP keep-alive for reusing connections
- **Pagination**: Loading data in chunks

## Scalability
- **Horizontal scaling**: Adding more servers
- **Vertical scaling**: Adding more resources to existing server
- **Auto-scaling**: Automatically adjusting capacity
- **Load balancing**: Distributing requests across servers
- **Sharding**: Partitioning data across databases
