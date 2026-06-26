---
description: Ponytail Skill - Lazy Senior Dev Mode for Cursor Enterprise Framework. Based on DietrichGebert/ponytail (58k stars)
version: 1.0.0
tags: [ponytail, yagni, minimalist, efficient, senior-dev, lazy-coding]
---

# Ponytail Skill - Lazy Senior Dev Mode

## Overview

**"He says nothing. He writes one line. It works."**

Ponytail brings the wisdom of the lazy senior developer to Cursor Enterprise Framework. The best code is the code you never wrote.

### Benchmark Results

| Metric | Improvement |
|--------|-------------|
| Lines of Code | **-54%** |
| Tokens | **-22%** |
| Cost | **-20%** |
| Time | **-27%** |
| Safety | **100%** |

---

## The YAGNI Ladder

Before writing any code, stop at the first rung that holds:

```
┌─────────────────────────────────────────────────────────────┐
│  1. Does this need to be built?      → SKIP (YAGNI)        │
│  2. Already in this codebase?         → REUSE, don't write  │
│  3. Stdlib does it?                  → USE stdlib           │
│  4. Native platform feature?         → USE platform         │
│  5. Installed dependency?            → USE it               │
│  6. Can this be one line?           → ONE LINE             │
│  7. Only then: minimum that works                          │
└─────────────────────────────────────────────────────────────┘
```

**The ladder runs AFTER you understand the problem, not instead of it.**

---

## Pre-Review Gate (Before Code)

### P.1 YAGNI Check

- [ ] Ask: "Does this need to exist at all?"
- [ ] Check: Is there existing code that solves this?
- [ ] Check: Does stdlib have this?
- [ ] Check: Does the platform/framework have this built-in?
- [ ] Check: Can this be a one-liner?

### P.2 Dependency Check

- [ ] Is the functionality already in an installed package?
- [ ] Is this adding a dependency for < 10 lines of usage?
- [ ] Can native APIs accomplish this?

### P.3 Abstraction Check

- [ ] Is this creating an abstraction layer?
- [ ] Is this requested or necessary?
- [ ] Is this "just in case" code?
- [ ] Are there < 3 usages that would justify this abstraction?

### P.4 Boilerplate Check

- [ ] Is this boilerplate that can be simplified?
- [ ] Is there a framework convention that reduces this?
- [ ] Can this be inlined?

### Pre-Review Checklist

```
[PONYTAIL PRE-REVIEW]
[ ] YAGNI check: Skip if not needed
[ ] Dependency check: Reuse existing
[ ] Abstraction check: Only if justified
[ ] Boilerplate check: Minimize
[ ] Ladder climbed to appropriate rung
```

---

## Common Over-Engineering Traps

| Request | Over-Built | Ponytail Solution |
|---------|-----------|------------------|
| Date picker | flatpickr + wrapper + stylesheet | `<input type="date">` |
| Color picker | npm color library + custom UI | `<input type="color">` |
| Debounce | Custom utility class | `setTimeout` in cleanup |
| Local storage | Wrapper class (200 lines) | `localStorage.getItem/setItem` |
| Form validation | Schema library + validators | Native HTML5 + JS |
| HTTP client | Axios + interceptors | Native fetch |
| Deep clone | Lodash cloneDeep | `structuredClone()` |
| UUID | uuid library | `crypto.randomUUID()` |
| JSON parse | try-catch wrapper class | Native try-catch |

### Native Alternatives to Common Libraries

```
lodash.cloneDeep  → structuredClone()
lodash.debounce   → setTimeout/clearTimeout
lodash.isEmpty   → Object.keys(x).length === 0
uuid.v4()        → crypto.randomUUID()
axios.get()      → fetch()
moment.js        → Intl.DateTimeFormat / date-fns
```

---

## Post-Review Gate (After Code)

### P.5 Code Reduction Check

- [ ] No abstractions without explicit request
- [ ] No new dependencies added unnecessarily
- [ ] No boilerplate that can be simplified
- [ ] Deletion considered (did we remove old code?)
- [ ] Shortest working diff achieved

### P.6 Intentional Shortcut Documentation

Mark shortcuts with `// ponytail:` comment:

```javascript
// ponytail: global lock, upgrade path = per-request mutex
const globalLock = new Lock();

// ponytail: O(n²) acceptable for n < 100
for (const a of items) { /* ... */ }

// ponytail: simple validation, full schema in v2
if (!email.includes('@')) { /* ... */ }

// ponytail: browser has one built-in
<input type="date">
```

### P.7 Safety Check

- [ ] Trust-boundary validation present
- [ ] Error handling prevents data loss
- [ ] Security controls in place
- [ ] Accessibility minimum met

### Post-Review Checklist

```
[PONYTAIL POST-REVIEW]
[ ] Code reduction achieved
[ ] Dependencies justified
[ ] Abstractions only when needed
[ ] Boilerplate minimized
[ ] Dead code deleted
[ ] Shortcuts documented with ponytail:
[ ] Safety: validation, error handling, security
```

---

## Ponytail Modes

| Mode | Description |
|------|-------------|
| `lite` | Minimal hints, senior devs |
| `full` | Default, most effective |
| `ultra` | Maximum enforcement |
| `off` | Disabled |

### Mode Configuration

```
PONYTAIL_DEFAULT_MODE=full  # env var
~/.config/ponytail/config.json  # config file
```

---

## Red Flags

These phrases indicate over-engineering:

- "Should I create a utility class?"
- "Maybe we need an abstraction layer?"
- "Let's make this configurable just in case"
- "We might need this feature later"
- "I'll add a factory pattern"
- "This might be useful for..."

### Green Lights

Safe to proceed:

- Native HTML elements (`<input type="date">`)
- Built-in APIs (`fetch`, `localStorage`, `crypto`)
- One-liner implementations
- Framework conventions
- Copy-paste patterns (when appropriate)

---

## Integration with Enterprise Framework Skills

### With `frontend-taste`

Ponytail enhances frontend-taste by:
- Preventing unnecessary component libraries
- Using native HTML elements first
- Minimizing CSS abstractions
- Reducing animation complexity

### With `frontend-redesign`

Ponytail during redesign:
- Delete dead code aggressively
- Replace abstractions with inline code
- Remove unused dependencies
- Simplify complex components

### With `security-review`

Ponytail respects security:
- Never skip trust-boundary validation
- Never remove error handling
- Never bypass security controls
- Ponytail applies only to business logic, not safety nets

---

## Examples

### Example 1: Date Input

**Request:** "Add a date picker"
**Over-built:**
```javascript
// utils/datePicker.ts
import Flatpickr from 'flatpickr';
export class DatePicker { /* 100 lines */ }
```

**Ponytail:**
```html
<!-- ponytail: browser has one built-in -->
<input type="date">
```

### Example 2: Debounce

**Request:** "Add debounce to search input"
**Over-built:**
```javascript
// utils/debounce.ts
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

### Example 3: UUID Generation

**Request:** "Generate unique IDs"
**Over-built:**
```javascript
// utils/idGenerator.ts
import { v4 as uuidv4 } from 'uuid';
export const generateId = () => uuidv4();
```

**Ponytail:**
```javascript
const id = crypto.randomUUID();
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/ponytail` | Current mode status |
| `/ponytail lite` | Minimal hints |
| `/ponytail full` | Default mode |
| `/ponalt ultra` | Maximum enforcement |
| `/ponytail off` | Disable |
| `/ponytail-review` | Review diff for over-engineering |
| `/ponytail-audit` | Audit whole repo |
| `/ponytail-debt` | Harvest deferred shortcuts |
| `/ponytail-gain` | Show benchmark impact |

---

## Links

- [[ponytail]] - Full Ponytail rule
- [[skill-integration]] - Skill auto-discovery protocol
- [[coding-standards]] - Coding standards
- [Original Ponytail](https://github.com/DietrichGebert/ponytail) - 58k stars
