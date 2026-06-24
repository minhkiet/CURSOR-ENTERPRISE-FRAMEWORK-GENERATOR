# Monitoring Knowledge - Architecture

## Observability Stack
```
[Application]
    |
    +--> [Metrics: Prometheus client] --> [Prometheus Server] --> [Grafana]
    |
    +--> [Logs: structured JSON] --> [Loki / CloudWatch / Datadog] --> [Grafana / Datadog]
    |
    +--> [Traces: OpenTelemetry] --> [Jaeger / Tempo / Datadog] --> [Grafana / Datadog]

[Infrastructure]
    |
    +--> [Node Exporter] --> [Prometheus]
    +--> [Docker stats] --> [Prometheus]
    +--> [CloudWatch metrics] --> [Grafana]
```

## Alerting Architecture
```
[Prometheus] --> [Alerting Rules]
                       |
                       v
              [Alertmanager] --> [Notification channels]
                       |
                       +--> Email
                       +--> Slack
                       +--> PagerDuty
                       +--> Webhook
```

## Distributed Tracing
```
[Client Request]
       |
       v
[API Gateway] --> [Span: gateway]
       |
       v
[Service A] --> [Span: service-a]
       |              |
       |              v
       |        [Span: db-query]
       |
       v
[Service B] --> [Span: service-b]
```

## SLO/SLA Framework
| Service | SLO | SLA | Error Budget |
|---------|-----|-----|--------------|
| API | 99.9% uptime | 99.5% | 43 min/month |
| Database | 99.95% uptime | 99.9% | 22 min/month |
| Auth | 99.99% uptime | 99.95% | 4 min/month |

## Recommended Dashboards
1. **Overview**: Request rate, error rate, latency p95
2. **SLO Dashboard**: Burn rate, error budget remaining
3. **Service Dashboard**: Per-service metrics
4. **Infrastructure Dashboard**: CPU, memory, disk, network
5. **Database Dashboard**: Query latency, connection pool, slow queries
6. **Queue Dashboard**: Queue depth, processing rate, DLQ
