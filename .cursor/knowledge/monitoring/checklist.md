# Monitoring Knowledge - Checklist

## Observability Foundation
- [ ] Prometheus or equivalent metrics system deployed
- [ ] Structured logging (JSON) implemented
- [ ] Distributed tracing (OpenTelemetry) configured
- [ ] Correlation ID propagated across all services

## SLO/SLA
- [ ] SLOs defined for each service
- [ ] Error budget tracking in place
- [ ] SLO dashboard created
- [ ] Alerting on SLO burn rate

## Application Metrics
- [ ] Request rate tracked
- [ ] Error rate tracked
- [ ] Latency tracked (p50, p95, p99)
- [ ] Saturation metrics (CPU, memory, connections)

## Infrastructure Metrics
- [ ] CPU utilization tracked
- [ ] Memory utilization tracked
- [ ] Disk I/O tracked
- [ ] Network throughput tracked

## Database Metrics
- [ ] Query latency tracked
- [ ] Connection pool tracked
- [ ] Slow query log configured
- [ ] Replication lag tracked

## Queue Metrics
- [ ] Queue depth tracked
- [ ] Processing rate tracked
- [ ] Dead letter queue monitored
- [ ] Consumer lag tracked

## Alerting
- [ ] Alert rules created for critical services
- [ ] Alert severity assigned
- [ ] Runbook links in alerts
- [ ] Alert routing configured (PagingDuty, Slack)
- [ ] Alert noise reduced (no duplicate alerts)

## Dashboards
- [ ] SLO overview dashboard
- [ ] Per-service dashboards
- [ ] Infrastructure dashboard
- [ ] Database dashboard
- [ ] Alert history dashboard
