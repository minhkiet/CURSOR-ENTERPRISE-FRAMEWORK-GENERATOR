---
description: Prompt chuan de implement CQRS - commands, queries, event bus, projection
trigger: cqrs, command query segregation, cqrs implementation
category: Architecture
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Prompt: CQRS Implementation - Implement CQRS

## Mo ta
Prompt chuan de implement CQRS (Command Query Responsibility Segregation) trong ung dung.

## Muc tieu
Tach biet doc/ghi su dung CQRS de toi uu hieu suat va tinh linh hoat.

## Khi nao dung CQRS
- Khi doc va ghi co yeu cau khac nhau ve du lieu
- Khi can toi uu doc-heavy va write-heavy operations rieng biet
- Khi can tai tao read models cho cac use cases khac nhau
- Khi can event sourcing de audit trail

## Workflow

### Buoc 1: Phan tich Domain
- [ ] Xac dinh cac commands (thay doi trang thai)
- [ ] Xac dinh cac queries (doc du lieu)
- [ ] Xac dinh bounded contexts
- [ ] Phan tich read/write patterns

### Buoc 2: Thiet ke Commands
- [ ] Dinh nghia command objects
- [ ] Implement command handlers
- [ ] Xac dinh invariants va business rules
- [ ] Thiet ke command validation

### Buoc 3: Thiet ke Queries
- [ ] Phan tich cac query requirements
- [ ] Thiet ke read models (projections)
- [ ] Implement query handlers
- [ ] Chon read model storage (SQL, NoSQL, cache)

### Buoc 4: Event Bus
- [ ] Chon event bus (in-memory, message queue)
- [ ] Dinh nghia domain events
- [ ] Implement event handlers
- [ ] Thiet ke event projections

### Buoc 5: Projection Implementation
- [ ] Implement read models tu events
- [ ] Cai dat eventual consistency
- [ ] Thiet ke projection rebuild strategy
- [ ] Optimistic concurrency cho projections

### Buoc 6: Implementation
- [ ] Implement command side (domain model)
- [ ] Implement query side (read models)
- [ ] Implement event bus
- [ ] Implement projections
- [ ] Write tests

## Lien ket
- [[../rules/cqrs]] - CQRS Rules
- [[../rules/ddd]] - DDD Rules
- [[../rules/event-sourcing]] - Event Sourcing Rules
- [[../skills/cqrs-implementation]] - CQRS Implementation Skill
