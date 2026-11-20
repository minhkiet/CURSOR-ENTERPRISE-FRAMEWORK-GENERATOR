# Performance Guard Plugin Rules

Measure first, optimize second. Every feature must respect performance budgets:

## Performance Targets
1. **Core Web Vitals**:
   - Largest Contentful Paint (LCP): < 2.5s
   - Interaction to Next Paint (INP): < 200ms
   - Cumulative Layout Shift (CLS): < 0.1
2. **Context & Token Economy**:
   - Keep prompt context lean and focused on targeted files.
   - Utilize prompt caching by preserving stable system instructions.
3. **Database Performance**:
   - Zero N+1 query patterns.
   - Ensure foreign keys and high-frequency filter columns are indexed.
