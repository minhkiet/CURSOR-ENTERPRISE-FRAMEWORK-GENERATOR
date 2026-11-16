---
name: subagent-driven-development
description: "Orchestrates multi-agent execution and independent code reviews: divides work into atomic tasks verified by dedicated review subagents (Maker vs Verifier)."
---

# Subagent-Driven Development Skill

> **Version:** 1.0.0 | **Pillar:** Multi-Agent Orchestration | **Model:** Maker-Verifier Pattern

---

## 1. Concept: The Two-Person Rule for AI
Self-review by the same agent context suffers from confirmation bias.
Subagent-Driven Development separates execution from verification:
1. **Maker Agent:** Focuses on implementing the specific atomic task.
2. **Verifier / Reviewer Agent:** Independent context running an unbiased audit against quality gates.

---

## 2. Orchestration Workflow

```
[Coordinator]
      │
      ▼
[Dispatch Maker Subagent] ──► Implements surgical change according to plan
      │
      ▼
[Run Automated Verification] ──► Test suite passes (CX.7)
      │
      ▼
[Dispatch Verifier Subagent] ──► Performs Line-by-Line Audit against CX.1-CX.6
      │
      ├─► Issues Found? ──► Send feedback to Maker for targeted fix
      │
      ▼
[Merge / Approve Task] ──► Proceed to next step in execution plan
```

---

## 3. Reviewer Gate Checklist
- [ ] Code strictly fulfills the requested step without bloat.
- [ ] No skeleton code, TODOs, or placeholder comments.
- [ ] Automated tests cover new logic and pass completely.
- [ ] No regression or breaking changes to existing contracts.
