---
description: Prompt chuan de audit queue - Redis, RabbitMQ, consumer patterns
trigger: queue, message broker, audit
category: Database
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Prompt: Queue Audit - Kiểm tra Queue

```markdown
# Queue Audit Workflow

## 1. AUDIT SCOPE
- **Queue Type**: [Redis / RabbitMQ / SQS / Kafka]
- **Scope**: [Full / Consumer / Producer / Performance]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/redis/* OR knowledge/rabbitmq/* (if applicable)
Load rules: queue.mdc
```

## 3. AUDIT AREAS

### Configuration
- [ ] Connection pooling
- [ ] Retry strategy
- [ ] Dead letter queue
- [ ] Message TTL

### Performance
- [ ] Throughput
- [ ] Latency
- [ ] Consumer lag
- [ ] Queue depth

### Reliability
- [ ] Message ordering
- [ ] At-least-once delivery
- [ ] Idempotency
- [ ] Error handling

## 4. LIÊN KẾT
- [[../skills/queue-audit]] - Queue Audit
- [[../rules/queue]] - Queue Rules
```
