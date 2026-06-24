# Monitoring Knowledge - Glossary

## Core Concepts
- **Observability**: Ability to understand internal state from external outputs
- **Telemetry**: Collection of metrics, logs, and traces
- **SLO (Service Level Objective)**: Target level of service availability
- **SLA (Service Level Agreement)**: Contractual SLO with customers
- **SLI (Service Level Indicator)**: Metric used to measure SLO

## Three Pillars
- **Metrics**: Numerical measurements over time (Prometheus, CloudWatch)
- **Logs**: Discrete events with timestamps (structured JSON logs)
- **Traces**: Request paths across services (OpenTelemetry, Jaeger)

## Alerting Terms
- **Alert**: Notification that something needs attention
- **Alert rule**: Condition that triggers an alert
- **Alert severity**: Critical, High, Medium, Low, Info
- **Alert fatigue**: Too many alerts causing desensitization
- **MTTR (Mean Time To Recovery)**: Average time to resolve incident
- **MTTD (Mean Time To Detect)**: Average time to detect incident

## Infrastructure Metrics
- **CPU usage**: Percentage of CPU utilization
- **Memory usage**: RAM utilization
- **Disk I/O**: Read/write operations
- **Network throughput**: Bandwidth utilization
- **Container metrics**: CPU, memory, network per container

## Application Metrics
- **Latency**: Response time (p50, p95, p99)
- **Throughput**: Requests per second
- **Error rate**: Percentage of failed requests
- **Saturation**: How full the system is
- **Active connections**: WebSocket, database connections
- **Queue depth**: Messages waiting in queue

## Logging Terms
- **Structured logging**: JSON-formatted logs with fields
- **Log levels**: DEBUG, INFO, WARN, ERROR, FATAL
- **Log correlation**: Shared request ID across all logs
- **Sampling**: Logging a percentage of requests
- **PII redaction**: Removing sensitive data from logs
