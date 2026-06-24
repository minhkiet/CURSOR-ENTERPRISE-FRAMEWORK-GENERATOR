# Monitoring Knowledge - Best Practices

## Metrics Best Practices
- Define SLOs before setting up monitoring
- Use the RED method: Rate, Errors, Duration
- Use the USE method: Utilization, Saturation, Errors
- Label cardinality: Keep high-cardinality labels under control
- Metric naming: `service_operation_type_unit` (e.g., `api_request_duration_seconds`)
- Scrape intervals: Match to SLO precision needs

## Logging Best Practices
- Always use structured JSON logging
- Include correlation ID on every log entry
- Use consistent log levels: DEBUG for dev, INFO for prod, WARN/ERROR as needed
- Never log sensitive data (PII, passwords, tokens)
- Log at decision points, not inside loops
- Use sampling for high-traffic endpoints
- Set log retention based on compliance needs

## Tracing Best Practices
- Propagate trace context across all async boundaries
- Add span annotations at significant events
- Use sampling: 100% for errors, 1-10% for success
- Instrument HTTP calls, database queries, cache operations
- Keep span names consistent and descriptive
- Add relevant tags: service, operation, user_id

## Alerting Best Practices
- Alert on symptoms, not causes (e.g., error rate > 1%, not disk full)
- Use multi-window alerts to prevent flapping
- Set alert severity based on business impact
- Page only for things requiring human action
- Include runbook links in every alert
- Alert on SLO burn rate, not just infrastructure

## Dashboards Best Practices
- SLO dashboard first (burn rate, error budget)
- Use templated dashboards for service consistency
- Include comparisons: current vs previous period
- Show both absolute numbers and percentages
- Include relevant labels for filtering
- Avoid over-aggregation (mixing unrelated services)

## Error Budget Policies
- Error budget > 50%: Normal operations
- Error budget 20-50%: Allocate time to reliability work
- Error budget 5-20%: Reliability is top priority
- Error budget < 5%: Immediate action, freeze changes
