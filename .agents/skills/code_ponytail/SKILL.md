---
description: Ponytail - Lazy Senior Dev. Minimum code, maximum effect. YAGNI optimization overlay.
version: 2.0.0
tags: [ponytail, yagni, minimalist, efficient, lazy-coding, code-reduction]
source: DietrichGebert/ponytail (58k stars)
---

# Ponytail Skill - Lazy Senior Dev Mode

> **Overlay Skill** - Run after karpathy-coding gates. "He says nothing. He writes one line. It works."

## Quick Card

```
┌─────────────────────────────────────────────────────────────┐
│  YAGNI LADDER                            CODE REDUCTION     │
├─────────────────────────────────────────────────────────────┤
│  1. Need it? → SKIP                   Check: abstractions? │
│  2. Exists? → REUSE                   Check: dependencies?  │
│  3. Stdlib? → USE IT                  Check: boilerplate?   │
│  4. Native? → USE IT                  Check: can inline?    │
│  5. Installed? → USE IT               Shortest diff?       │
│  6. One-liner? → ONE LINE             Safety: validated?   │
│  7. Only then: MINIMUM WORKS                               │
└─────────────────────────────────────────────────────────────┘
```

## Workflow

```
Request → karpathy-pre [K.1-K.4] → ponytail-pre [P.1-P.4]
                                       ↓
                                IMPLEMENT
                                       ↓
                               ponytail-post [P.5-P.7]
                                       ↓
                           karpathy-post [K.5-K.7]
                                       ↓
                               DELIVER
```

---

## YAGNI Ladder

**STOP at first rung that applies:**

```
┌─────────────────────────────────────────────────────────────┐
│  1. NEED IT?        → Don't build it (YAGNI)              │
│  2. EXISTS?        → Reuse existing code                   │
│  3. STDLIB?        → Use built-in library                  │
│  4. NATIVE?        → Use platform feature                  │
│  5. INSTALLED?     → Use installed dependency              │
│  6. ONE-LINE?      → Write one line                         │
│  7. Only then:     → MINIMUM VIABLE CODE                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Pre-Code Gates

### P.1 YAGNI Check

```
Ask: Does this need to exist?
     ↓
Check: Already in codebase? → REUSE
Check: Stdlib has it? → USE IT
Check: Platform has it? → USE IT
Check: One-liner possible? → ONE LINE
```

### P.2 Dependency Check

| Scenario | Action |
|----------|--------|
| Already in installed package | Use it |
| Adding for <10 lines | Don't add |
| Native API works | Use native |

### P.3 Abstraction Check

- [ ] Creating abstraction layer?
- [ ] Requested or necessary?
- [ ] "Just in case" code? → Skip
- [ ] <3 usages? → Inline

### P.4 Boilerplate Check

- [ ] Can simplify with framework convention?
- [ ] Can inline this?
- [ ] Is this boilerplate?

---

## Post-Code Gates

### P.5 Code Reduction Check

- [ ] Abstractions justified?
- [ ] Dependencies necessary?
- [ ] Boilerplate minimized?
- [ ] Old code deleted?
- [ ] **Shortest working diff achieved?**

### P.6 Shortcut Documentation

```javascript
// ponytail: [reason]
// Examples:
const id = crypto.randomUUID();  // ponytail: native API

// ponytail: simple validation, full schema in v2
if (!email.includes('@')) return;

// ponytail: O(n²) acceptable for n < 100
for (const a of items) { /* ... */ }
```

### P.7 Safety Check

```
Trust boundary: validated?
Error handling: prevents data loss?
Security: controls in place?
Accessibility: minimum met?
```

---

## Native Alternatives

| Instead of | Use |
|------------|-----|
| `lodash.cloneDeep` | `structuredClone()` |
| `lodash.debounce` | `setTimeout/clearTimeout` |
| `uuid.v4()` | `crypto.randomUUID()` |
| `axios.get()` | `fetch()` |
| `moment.js` | `Intl.DateTimeFormat` |
| Custom date picker | `<input type="date">` |
| Custom color picker | `<input type="color">` |
| LocalStorage wrapper | `localStorage.getItem/setItem` |

---

## Examples

### Debounce

**Over-built:**
```javascript
import debounce from 'lodash.debounce';
export const debouncedSearch = debounce(searchFn, 300);
```

**Ponytail:**
```javascript
let timeout;
input.addEventListener('input', () => {
  clearTimeout(timeout);
  timeout = setTimeout(search, 300);
});
```

### Date Input

**Over-built:**
```javascript
import Flatpickr from 'flatpickr';
export class DatePicker { /* 100 lines */ }
```

**Ponytail:**
```html
<input type="date">
```

### UUID

**Over-built:**
```javascript
import { v4 as uuidv4 } from 'uuid';
export const generateId = () => uuidv4();
```

**Ponytail:**
```javascript
const id = crypto.randomUUID();
```

---

## Red Flags

**These phrases → STOP and reconsider:**
- "Should I create a utility class?"
- "Maybe we need an abstraction layer?"
- "Let's make this configurable just in case"
- "We might need this feature later"
- "I'll add a factory pattern"
- "This might be useful for..."

**Green Lights → Proceed:**
- Native HTML elements
- Built-in APIs
- One-liner implementations
- Framework conventions
- Copy-paste patterns

---

## Modes

| Mode | Use When |
|------|----------|
| `lite` | Senior devs, minimal hints |
| `full` | Default, most effective |
| `ultra` | Maximum enforcement |
| `off` | Disabled (not recommended) |

---

## Integration

```
┌─────────────────────────────────────────────────┐
│  karpathy-coding                               │
│  "What to build? Is scope correct?"            │
└──────────────────┬────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│  ponytail                                   │
│  "How to build with least code?"             │
└─────────────────────────────────────────────────┘
```

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Lines of Code | **-54%** vs verbose |
| Tokens | **-22%** |
| Cost | **-20%** |
| Time | **-27%** |
| Safety | **100%** maintained |
