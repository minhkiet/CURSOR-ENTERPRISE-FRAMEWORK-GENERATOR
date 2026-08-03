---
description: Vibe Coding - Unified overlay skill kết hợp Think First (karpathy) + Minimize Code (ponytail). Luôn chạy với mọi task.
version: 1.0.0
tags: [vibe-coding, efficient, think-first, minimize, yagni, surgical, goal-driven]
source: andrej-karpathy-skills + DietrichGebert/ponytail
---

# Vibe Coding - Think First, Code Minimum

> **Unified Overlay Skill** - Kết hợp karpathy-coding + ponytail. Luôn chạy với mọi task.

## Quick Card

```
┌─────────────────────────────────────────────────────────────────────────┐
│  VIBE CODING WORKFLOW                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  REQUEST ──► THINK ──► SCOPE ──► MINIMIZE ──► IMPLEMENT ──► VERIFY   │
│                ↓           ↓          ↓             ↓              ↓       │
│            Assumptions?  What NOT  YAGNI?       Minimum       Done?       │
│                         to touch   Native?                        Goals?   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. THINK (karpathy)                                        │
│     → Đang assume gì?                                       │
│     → Multiple interpretations? → Present options             │
│     → Unclear? → ASK ngay                                  │
├─────────────────────────────────────────────────────────────┤
│  2. SCOPE (karpathy)                                       │
│     → MUST: [list essential changes only]                   │
│     → NOT: [boundaries - what NOT to touch]                │
├─────────────────────────────────────────────────────────────┤
│  3. MINIMIZE (ponytail)                                    │
│     → YAGNI? Already exists? Stdlib? Native?                │
│     → One-liner possible?                                    │
│     → Shortest working diff wins                             │
├─────────────────────────────────────────────────────────────┤
│  4. IMPLEMENT                                              │
│     → Write minimum that solves problem                     │
│     → No speculative features                               │
│     → No unnecessary abstractions                            │
├─────────────────────────────────────────────────────────────┤
│  5. VERIFY (karpathy + ponytail)                           │
│     → §X: Actually ran tests?                               │
│     → §X: Code traces to request?                           │
│     → §X: No banned patterns?                              │
│     → §X: Dead code removed?                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: THINK

### T.1 State Assumptions

```
Ask yourself:
□ Đang assume gì về request này?
□ Có cách interpret nào khác?
□ Có simpler approach không?
```

### T.2 Detect Ambiguity

| Signal | Action |
|--------|--------|
| Multiple valid interpretations | Present options A/B |
| Unclear requirements | STOP → Ask |
| "Just do it" signal | Slow down, check T.1 |

### T.3 Push Back

When simpler approach exists:
```
"Simpler approach: [X] instead of [Y]
 Reason: [brief justification]
 Want me to proceed with X?"
```

---

## Phase 2: SCOPE

### S.1 Define MUST Change

```
MUST change:
1. [file/feature 1]
2. [file/feature 2]
```

### S.2 Define NOT Touch

```
NOT touch:
- [component/file 1] - reason
- [component/file 2] - reason
```

### S.3 Surgical Test

```
Every line I write → traces to MUST?
Yes → proceed
No → remove or question
```

---

## Phase 3: MINIMIZE

### M.1 YAGNI Ladder

```
┌─────────────────────────────────────────────────────────────┐
│  1. NEED IT?      → Don't build (YAGNI)                  │
│  2. EXISTS?       → Reuse existing code                   │
│  3. STDLIB?       → Use built-in library                  │
│  4. NATIVE?       → Use platform feature                 │
│  5. ONE-LINER?    → Write one line                       │
│  6. Only then:    → MINIMUM THAT WORKS                    │
└─────────────────────────────────────────────────────────────┘
```

### M.2 Native Alternatives

| Instead of | Use |
|------------|-----|
| `lodash.cloneDeep` | `structuredClone()` |
| `lodash.debounce` | `setTimeout/clearTimeout` |
| `uuid.v4()` | `crypto.randomUUID()` |
| `axios.get()` | `fetch()` |
| `moment.js` | `Intl.DateTimeFormat` |
| Custom date picker | `<input type="date">` |
| Custom color picker | `<input type="color">` |
| 200-line wrapper | `localStorage.getItem/setItem` |

### M.3 Code Reduction Check

- [ ] No abstractions unless requested
- [ ] No new dependencies
- [ ] No boilerplate
- [ ] Old code deleted?
- [ ] **Shortest working diff?**

---

## Phase 4: IMPLEMENT

### I.1 Write Minimum

```
Rule: If 100 lines can solve it, write 100 lines.
If 10 lines can solve it, write 10 lines.
```

### I.2 Safety Never Skip

```
□ Trust boundary validation
□ Error handling (prevents data loss)
□ Security controls
□ Accessibility minimum
```

### I.3 Mark Shortcuts

```javascript
// vibe: global lock, upgrade = per-request mutex
const globalLock = new Lock();

// vibe: O(n²) acceptable for n < 100
for (const a of items) { /* ... */ }
```

---

## Phase 5: VERIFY

### V.1 Implementation Check

- [ ] Every line traces to MUST
- [ ] No adjacent code "improved"
- [ ] No unrelated refactoring
- [ ] My orphans → removed

### V.2 Goal Achievement

```
Task → "Done when..." → [criteria]
□ Success criteria verified (line-by-line)
□ Tests pass (actually ran, not assumed)
□ No regressions
```

### V.3 §X - Verify for Real

```
□ Read actual code (re-open files, confirm diff)
□ Ran tests? (actually ran, not "should pass")
□ No banned: "// ...", "// TODO", "rest follows pattern"
□ Cross-check: every line of ask → answered?
```

### V.4 Anti-Patterns Caught

| Pattern | Check |
|---------|-------|
| Assumed instead of asked | Rollback, ask |
| Over-engineered | Simplify now |
| Touched unrelated code | Stay surgical |
| No success criteria | Define first |
| 200 lines when 50 works | Rewrite |

---

## Red Flags

**STOP when you hear:**
- "Should I create a utility class?"
- "Maybe we need an abstraction layer?"
- "Let's make this configurable just in case"
- "We might need this feature later"

**GO when you see:**
- Native HTML elements
- Built-in APIs
- One-liner implementations
- Framework conventions
- Shortest working diff

---

## Integration

```
ANY TASK
    ↓
┌─────────────────────────────┐
│ vibe-coding overlay         │
│ (karpathy + ponytail)      │
└──────────┬────────────────┘
           ↓
    Primary skill gates
           ↓
    Domain post-gates
           ↓
        DELIVER
```

**karpathy** → Prevents building wrong things  
**ponytail** → Prevents building too verbosely

Together: **Right thing, right size, no waste.**

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Lines of Code | -54% vs verbose |
| Tokens | -22% |
| Cost | -20% |
| Time | -27% |
| Safety | 100% maintained |
| Surgical changes | 100% |
| Clarifying questions | BEFORE implementation |
