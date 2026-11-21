---
name: speckit-implement
description: "Execute implementation tasks sequentially from tasks.md using strict TDD (Red-Green-Refactor) and automated verification, maintaining live task checklists."
---

# SpecKit Implement Skill

> **Version:** 1.0.0 | **Phase:** Execution & Verification | **Input:** `tasks.md`

---

## 1. Objective
Execute the tasks defined in `.specify/specs/<feature-name>/tasks.md` one by one, adhering strictly to Test-Driven Development and CEF Quality Gates.

---

## 2. Implementation Loop

For each uncompleted task `[ ]` in `tasks.md`:

```
┌────────────────────────────────────────────────────────┐
│ 1. Read Task Description & Files                        │
│ 2. RED: Write unit test & confirm failing reason       │
│ 3. GREEN: Write minimal code to pass test              │
│ 4. REFACTOR: Clean code while keeping tests green      │
│ 5. Mark task as completed [x] in tasks.md               │
│ 6. Check status via: vibe-framework spec status      │
└────────────────────────────────────────────────────────┘
```

---

## 3. Strict Execution Rules
1. **Never Skip RED**: Verify the test fails for the expected reason before writing production code.
2. **Surgical Edits**: Touch only the files specified in the current task. Do not refactor unrelated modules.
3. **Zero Skeleton Code**: Implement working, concrete logic. Never leave TODO or pass placeholders.
4. **Live Checkpointing**: Update `tasks.md` immediately after each verified task so that session memory and progress tracking remain accurate.
5. **Quality Gate Audit**: Once all tasks are checked `[x]`, execute `python -m vibe_framework spec validate <feature-name>` to confirm all gates pass.
