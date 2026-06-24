# Monitoring Knowledge - FAQ

**Q: How do we set appropriate SLOs?**
A: Start with current baseline measurements. Set SLO slightly better than reality. Review quarterly based on customer impact.

**Q: How do we reduce alert fatigue?**
A: Use multi-window alerts (sustained for 5+ minutes). Deduplicate similar alerts. Alert on symptoms, not causes. Set escalation paths.

**Q: When should we sample logs/traces?**
A: Log 100% of errors and rare events. For high-traffic success paths, sample 1-5%. Always sample trace spans.

**Q: How long should we retain metrics/logs/traces?**
A: Metrics: 13 months (for yearly comparisons). Logs: 30-90 days (adjust for compliance). Traces: 7-30 days.

**Q: How do we monitor async jobs/queues?**
A: Track queue depth, processing rate, dead letter queue size, and consumer lag. Alert if queue depth exceeds threshold or if consumers fall behind.
