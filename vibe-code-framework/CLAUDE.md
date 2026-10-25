# CLAUDE.md — Claude Code Format

> **Version:** 1.0.0 | **Tool:** Claude Code

---

# Vibe Code Framework

> Cross-Platform AI Coding Framework

---

## Core Principles

### YAGNI — You Aren't Gonna Need It

**Don't write code for features that aren't needed yet.**

Before coding, ask:
1. Does this need to be built at all? → no: skip it
2. Already in codebase? → reuse it
3. Stdlib has it? → use it
4. One line? → one line
5. Only then: minimum that works

### KISS — Keep It Simple, Stupid

**Simplest solution is usually best.**

- Each function/class does one thing
- Don't premature optimize
- Readable > clever

### DRY — Don't Repeat Yourself

**Extract repeated code to functions/modules.**

- Logic → function
- Types → shared
- Validation → validator

---

## Architecture

### Clean Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Clean Architecture                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   Presentation → Application → Domain ← Infrastructure   │
│                                                          │
│   Inner layers NEVER depend on outer layers              │
│   Infrastructure implements Domain interfaces           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Dependency Injection

```typescript
// ✅ Constructor injection
class UserService {
  constructor(
    private userRepository: IUserRepository,
    private emailService: IEmailService
  ) {}
}

// ❌ Hardcoded dependency
class UserService {
  private repo = new UserRepository(); // Don't do this
}
```

---

## Security Rules

```
┌─────────────────────────────────────────────────────────────┐
│ Pre-Commit Security Checklist                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ □ No hardcoded secrets                                      │
│ □ All user input validated                                  │
│ □ Parameterized SQL queries                                 │
│ □ Output escaped/sanitized                                  │
│ □ Passwords hashed (bcrypt/argon2)                          │
│ □ Rate limiting enabled                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Git Workflow

### Branch Naming

```
feature/{ticket-id}-short-description
fix/{ticket-id}-short-description
chore/{description}
```

### Commit Format

```
<type>(<scope>): <subject>

feat(auth): add JWT refresh token rotation
fix(payment): correct tax calculation
```

---

## Code Quality Checklist

```
□ Logic correct?
□ Edge cases handled?
□ Error handling complete?
□ Performance acceptable?
□ Test coverage sufficient (> 80%)?
□ Meaningful names?
□ Functions small (< 30 lines)?
□ No duplicate code?
□ No console.log/debugger?
```

---

## Development Lifecycle

```
┌─────────────────────────────────────────────────────────┐
│            Development Lifecycle                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  DEFINE → PLAN → BUILD → TEST → REVIEW → SHIP          │
│   /spec    /plan    /build   /test   /review    /ship  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Available Skills

| Skill | Purpose |
|-------|---------|
| `create-feature` | Create feature from spec |
| `create-api` | Design REST/GraphQL API |
| `create-ui` | Design UI components |
| `database-migration` | Manage DB migrations |
| `code-review` | Review with quality gates |
| `debug-error` | Systematic debugging |

---

## Agent Personas

### Solution Architect
Design scalable, maintainable systems.

### Code Reviewer
Five-axis review: Correctness, Design, Security, Performance, Readability.

### Security Auditor
OWASP Top 10, vulnerability detection.
