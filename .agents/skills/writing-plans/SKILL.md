---
name: writing-plans
description: "Decomposes complex features or refactors into atomic implementation steps with explicit success criteria, file maps, dependency order, and test checkpoints."
---

# Writing Plans Skill

> **Version:** 1.0.0 | **Pillar:** Execution Planning | **Phase:** Step-by-Step Roadmapping

---

## 1. Goal
Transform design decisions into an actionable, incremental execution plan. Each step must be self-contained, verifiable, and safe to roll back.

---

## 2. Plan Structure Requirements

Every plan must follow the atomic step format:

```markdown
### Step N: [Clear Action Verb + Target Component]
- **Target Files:** `path/to/file.ext`
- **Dependencies:** Step N-1
- **Action:** Exact modifications or creation steps.
- **Verification Command:** Automated test or CLI verification command.
- **Success Criteria:** Expected observable output.
```

---

## 3. Plan Decomposition Checklist
- [ ] All steps arranged in strict dependency order.
- [ ] Every step has a clear verification command (unit test, build, lint).
- [ ] Blast radius restricted: changes touch only targeted files.
- [ ] Atomic: if step fails, repository remains in a recoverable state.
