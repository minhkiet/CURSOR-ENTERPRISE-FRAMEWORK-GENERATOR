---
name: redis-observability
description: "Redis observability guidance — which metrics to monitor (memory, connections, hit ratio, ops/sec, rejected connections), which built-in commands to reach for during incident triage (SLOWLOG, INFO, MEMORY DOCTOR, CLIENT LIST, FT.PROFILE), and when to use the Redis Insight GUI. Use when setting up monitoring or alerts for a Redis instance, diagnosing a performance regression, profiling a slow FT.SEARCH query, or wiring Redis metrics into Prometheus, Datadog, or similar."
---

# Alias: redis-observability

**DEPRECATED**: This skill has been renamed to `db_redis-observability`.

For backward compatibility, this alias redirects to the new skill.

## Migration

Update your code to use:
`
.cursor/skills/db_redis-observability/SKILL.md
`

## Auto-Redirect

This alias is maintained for backward compatibility.
The skill-registry will automatically redirect to the new name.

---
Auto-generated alias file
Last updated: 2026-08-03
