# Monitoring Knowledge - Decision Tree

## Where to send alerts?
- Page immediately: Production down, data loss risk, security breach
- Notify Slack: Non-critical alerts, trend warnings
- Log only: Informational, debugging
- Auto-resolve: Known maintenance windows

## What to alert on?
- Symptom (error rate, latency spike) over cause (disk full, CPU high)
- SLO burn rate over raw metric values
- Composite signals over single metrics (error rate + latency)

## How many alerts?
- Enough to catch customer-impacting issues
- Not so many that people ignore them
- Target: < 5 pages per engineer per week

## What metrics to collect?
- RED for services: Rate, Errors, Duration
- USE for resources: Utilization, Saturation, Errors
- Business metrics: DAU, conversion, revenue

## Log level decisions?
- DEBUG: Detailed debugging info (development only)
- INFO: Normal operations (every significant event)
- WARN: Unexpected but handled situations
- ERROR: Errors that need attention
- FATAL: System shutdown scenarios
