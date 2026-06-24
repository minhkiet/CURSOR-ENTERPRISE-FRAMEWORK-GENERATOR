# Performance Knowledge - FAQ

**Q: How do we identify the actual bottleneck?**
A: Use APM tools (Datadog, New Relic) to trace request paths. Profile the slowest endpoints first. Measure before optimizing to establish baseline.

**Q: When should we add caching?**
A: When the same data is read frequently and changes infrequently. Cache read-heavy endpoints, expensive computations, and static assets.

**Q: N+1 query - how to fix?**
A: Use eager loading (JOIN, IN clause with batch query). For ORMs, use include/preload/eager. For raw SQL, batch queries by collecting IDs first.

**Q: When are indexes actually used?**
A: When WHERE, JOIN, or ORDER BY uses the column. When the query selectivity is high (few rows match). Verify with EXPLAIN ANALYZE.

**Q: Core Web Vitals failing - where to start?**
A: LCP: Preload hero image, optimize server response. INP: Reduce JavaScript, defer non-critical. CLS: Reserve space for images/fonts.
