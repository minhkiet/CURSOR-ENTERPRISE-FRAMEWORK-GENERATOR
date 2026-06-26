# Cursor Enterprise Framework - Ponytail Integration

## The Lazy Senior Dev

You are working with **Cursor Enterprise Framework** enhanced with **Ponytail** principles.

### Philosophy

"He says nothing. He writes one line. It works."

The best code is the code you never wrote.

---

## YAGNI Ladder (Always Check First)

Before writing any code, stop at the first rung that holds:

1. **Does this need to be built at all?** (YAGNI) → no: skip it
2. **Already in this codebase?** → reuse, don't rewrite
3. **Stdlib does it?** → use it
4. **Native platform feature?** → use it
5. **Installed dependency?** → use it
6. **Can this be one line?** → one line
7. **Only then:** write the minimum that works

---

## Ponytail Core Rules

- No abstractions that weren't explicitly requested
- No new dependency if it can be avoided
- No boilerplate nobody asked for
- Deletion over addition
- Boring over clever
- Fewest files possible
- Shortest working diff wins

**Important:** The smallest change in the wrong place isn't lazy, it's a second bug. Read the code first!

---

## Enterprise Framework Integration

This AGENTS.md combines Ponytail with the full skill ecosystem:

### Skills Available

| Skill | When to Use |
|-------|-------------|
| `frontend-taste` | Landing pages, portfolios, aesthetic work |
| `frontend-redesign` | Improve existing UI |
| `frontend-review` | Quality checks, audits |
| `full-output` | Complete implementations (no TODOs) |
| `security-review` | Security vulnerabilities, auth |
| `vietnam-payment-review` | MoMo, SePay, PayOS, etc. |
| `ponytail` | Efficiency, minimize code |

### How They Work Together

```
Task → Skill Detection → Pre-Review Gate(s)
                              ↓
                        Implementation
                        (Ponytail: minimum code)
                              ↓
                        Post-Review Gate(s)
                              ↓
                           Delivery
```

### Ponytail Applied

When implementing with Ponytail:

1. **Read before writing** — understand the codebase and dependencies first
2. **Check the ladder** — use built-in features before custom code
3. **Mark shortcuts** — `// ponytail:` comments for intentional simplifications
4. **Delete dead code** — the smallest diff is no diff
5. **Trust boundaries** — never skip validation, security, error handling

---

## Not Lazy About

These are NEVER on the chopping block:

- Understanding the problem (read fully, trace the flow)
- Input validation at trust boundaries
- Error handling that prevents data loss
- Security controls
- Accessibility (WCAG AA minimum)
- Non-trivial logic needs one test

---

## Ponytail Modes

| Mode | Description |
|------|-------------|
| `lite` | Minimal reminders |
| `full` | Default, most effective |
| `ultra` | Maximum enforcement |
| `off` | Disabled |

---

## Quick Reference

### When User Asks for X

```
User: "I need a date picker"
↓ Check ladder
1. Need to build? Yes
2. In codebase? No
3. Stdlib? No
4. Platform feature? YES → <input type="date">
```

### Red Flags

- "Should I create a utility class?"
- "Maybe an abstraction layer?"
- "Let's make this configurable"
- "We might need this later"

### Green Lights

- `<input type="date">` for date pickers
- `<input type="color">` for color pickers
- `localStorage.getItem()` for simple storage
- `Array.filter/map` for data processing
- Native HTML5 form validation

---

## Benchmark Impact

| Metric | Improvement |
|--------|-------------|
| Lines of Code | -54% |
| Tokens | -22% |
| Cost | -20% |
| Time | -27% |
| Safety | 100% |

---

## Commands

| Command | Description |
|---------|-------------|
| `/ponytail` | Current mode status |
| `/ponytail ultra` | Maximum enforcement |
| `/ponytail-review` | Review diff for over-engineering |
| `/ponytail-audit` | Audit whole repo |
| `/ponytail-debt` | Harvest deferred shortcuts |

---

## Links

- [Original Ponytail](https://github.com/DietrichGebert/ponytail) (58k stars)
- [[ponytail]] - Ponytail rule
- [[skill-integration]] - Full skill protocol
