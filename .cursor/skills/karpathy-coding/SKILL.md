---
description: Karpathy Coding - Think Before Code. Minimal overlay skill cho mọi task. 5 phút review trước/sau code.
version: 2.0.0
tags: [karpathy, coding-discipline, think-first, minimal, goal-driven, surgical, verification]
source: andrej-karpathy-skills (186k stars)
---

# Karpathy Coding Discipline

> **Overlay Skill** - Chạy với mọi coding task. Không skip.

## Quick Card

```
┌─────────────────────────────────────────────────────────────┐
│  BEFORE CODE                    AFTER CODE                  │
├─────────────────────────────────────────────────────────────┤
│  K.1 Think: assumptions?           K.5 Verify: traceable?  │
│  K.2 Simple: over-engineer?       K.6 Simple: 200→50?     │
│  K.3 Scope: surgical?             K.7 Done: goals met?      │
│  K.4 Goals: verifiable?           §X   Verify for real     │
└─────────────────────────────────────────────────────────────┘
         ↓                                       ↓
    [ASK if unclear]                    [VERIFY it works]
```

## Workflow

```
Request → K.1-K.4 → IMPLEMENT → K.5-K.7 → §X → DELIVER
              ↑                            ↓
         [CLARIFY]              [VERIFIED? NO → loop]
```

---

## Pre-Code Gates

### K.1 Think Before Code

**Luôn hỏi:**
- Đang assume gì? (state explicitly)
- Có cách nào simpler? (push back nếu warranted)
- Unclear → **STOP, ask ngay**

**Nếu multiple interpretations:**
```
Option A: [mô tả]
Option B: [mô tả]
Recommendation: [vì sao]
```

### K.2 Simplicity Check

| Check | Action |
|-------|--------|
| 200 lines có thể 50? | Rewrite |
| Speculative features? | Remove |
| Single-use abstraction? | Inline |
| "Flexibility" không được request? | Skip |

### K.3 Surgical Scope

```
MUST change:    [list only essential]
NOT touch:      [list boundaries]
Every line traces to request? [yes/no]
Style matched?  [yes/no]
```

### K.4 Goal Definition

```
Task → "Done when..." → [verifiable criteria]
```

**Examples:**
- "Fix bug" → "Test passes, edge cases covered"
- "Add feature" → "Demo works, no regressions"
- "Refactor" → "Tests pass before & after"

---

## Post-Code Gates

### K.5 Implementation Verification

- [ ] Every line traces to request
- [ ] No adjacent code "improved"
- [ ] No unrelated refactoring
- [ ] My orphans → removed

### K.6 Simplicity Re-Check

- [ ] 200 lines written → can be 50? Rewrite now.
- [ ] Speculative abstractions? Remove.
- [ ] Single-use code? Inline.

### K.7 Goal Achievement

- [ ] Success criteria verified (line-by-line)
- [ ] Tests pass (actually ran, not assumed)
- [ ] No regressions

---

## §X - Verify Before Deliver

**Đây là bước BẮT BUỘC, không skip:**

```
□ Read actual code (re-open files)
□ Verify each K.4 criterion (line-by-line)
□ Run verification step (actually ran it)
□ No banned patterns: "// ...", "// TODO"
□ Cross-check with original request
```

**Anti-pattern:** "I think it works" → §X prevents this.

---

## §Y - Receiving Feedback

```
1. Read FULL feedback before responding
2. Verify each claim against code
3. Ask clarification if unclear
4. Push back if wrong (with evidence)
5. Fix or document "won't fix - because..."
6. Re-run §X after changes
```

---

## Integration Flow

```
┌─────────────┐
│ Any Task    │
└──────┬──────┘
       ↓
┌──────────────────────────────────────┐
│ karpathy-pre [K.1-K.4]               │ ← Think + Scope + Goals
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│ [primary skill]                     │ ← frontend-taste, etc.
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│ karpathy-post [K.5-K.7] + §X        │ ← Verify surgical + goals
└──────┬───────────────────────────────┘
       ↓
   DELIVER
```

---

## Indicators → Actions

| Signal | Action |
|--------|--------|
| "just do it" | Slow down, K.1-K.2 first |
| Unclear request | Ask before assuming |
| 200+ lines proposed | Check if 50 works |
| Adjacent "improved" | Roll back |
| Multiple interpretations | Present options |
| "I assumed..." | Should have asked first |

---

## Anti-Patterns

| Violation | Fix |
|-----------|-----|
| Assume instead of ask | Stop, ask |
| Over-engineer | Simplify |
| Touch unrelated code | Stay surgical |
| No success criteria | Define first |
| 200 lines when 50 works | Rewrite |

---

## Success Metrics

- Fewer unnecessary changes in diffs
- Clarifying questions BEFORE implementation
- Simplicity maintained
- Surgical changes only
