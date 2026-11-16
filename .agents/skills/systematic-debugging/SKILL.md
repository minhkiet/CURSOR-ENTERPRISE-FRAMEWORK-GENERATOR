---
name: systematic-debugging
description: "Evidence-first systematic debugging protocol: 4-phase root cause isolation (reproduce, isolate, hypothesize, verify). Eliminates trial-and-error guess-and-check fixes."
---

# Systematic Debugging Skill

> **Version:** 1.0.0 | **Pillar:** Reliability | **Protocol:** Evidence-First RCA

---

## 1. Prime Directive
**NEVER GUESS. NEVER PATCH RANDOMLY.**
Trial-and-error coding (adding random null checks or try-catches) creates technical debt and hides catastrophic bugs. Every fix must be justified by reproducible evidence.

---

## 2. The 4-Phase Debugging Protocol

```
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1: REPRODUCE (100% Deterministic Reproduction)            │
├─────────────────────────────────────────────────────────────────┤
│ • Write a reproduction unit test, script, or exact CLI command. │
│ • Observe and record exact error trace, status code, or log.    │
│ • If reproduction is flaky, isolate state dependencies first.   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 2: ISOLATE (Trace Data Flow & Boundaries)                 │
├─────────────────────────────────────────────────────────────────┤
│ • Inspect logs, stack traces, and variable states at boundary.  │
│ • Narrow down search space using binary search / bisect.        │
│ • Identify the exact line or contract failure causing anomaly.  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 3: HYPOTHESIZE (Formulate Scientific Explanation)         │
├─────────────────────────────────────────────────────────────────┤
│ • State the hypothesis: "X fails because Y violates Z contract".│
│ • Verify hypothesis by adding temporary diagnostic telemetry.   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 4: SURGICAL FIX & VERIFY                                  │
├─────────────────────────────────────────────────────────────────┤
│ • Apply minimal surgical change addressing the root cause.      │
│ • Re-run reproduction test: verify it now PASSES.               │
│ • Run full regression test suite: ensure no collateral damage.  │
│ • Remove temporary diagnostic logging before delivery.          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Systematic Debugging Checklist
- [ ] Error reproduced deterministically with test or command.
- [ ] Root cause identified with evidence, not assumptions.
- [ ] Surgical fix applied only to the failing boundary.
- [ ] Reproduction test added to regression test suite.
