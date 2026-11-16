---
name: brainstorming
description: "Structured design brainstorming and requirement discovery before implementation. Explores user intent, trade-offs, edge cases, and architectural alternatives."
---

# Design & Brainstorming Skill

> **Version:** 1.0.0 | **Pillar:** Architecture | **Phase:** Pre-Flight Discovery

---

## 1. Goal
Clarify intent and evaluate alternative approaches before touching production code.
Prevents costly rework caused by misaligned assumptions.

---

## 2. Brainstorming Framework

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Understand User Intent & Problem Space                  │
├─────────────────────────────────────────────────────────────────┤
│ • What is the underlying user need vs stated feature?           │
│ • Who are the actors and what is the expected workflow?         │
│ • What are the non-functional constraints (perf, security)?     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Explore Design Alternatives & Trade-offs                │
├─────────────────────────────────────────────────────────────────┤
│ • Option A (Simplest/YAGNI): Minimal modification to existing.  │
│ • Option B (Standard Enterprise): Idiomatic architecture.       │
│ • Evaluate: Complexity vs Maintainability vs Blast Radius.      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Identify Edge Cases & Blast Radius                      │
├─────────────────────────────────────────────────────────────────┤
│ • Boundary conditions, malformed inputs, concurrency issues.    │
│ • Impact on existing database schemas, APIs, and client apps.   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Quality Gate
- [ ] Clarified ambiguous requirements before coding.
- [ ] Evaluated at least 2 architectural approaches.
- [ ] Identified edge cases and blast radius.
- [ ] Selected simplest path obeying YAGNI.
