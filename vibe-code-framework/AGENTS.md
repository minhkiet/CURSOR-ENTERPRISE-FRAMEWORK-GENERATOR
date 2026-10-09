# AGENTS.md — OpenAI Codex Format

> **Version:** 1.0.0 | **Tool:** OpenAI Codex

---

# Vibe Code Framework

> Cross-Platform AI Coding Framework

---

## Core Principles

### YAGNI — You Aren't Gonna Need It

Don't write code for features that aren't needed yet.

```
1. Does this need to be built?     → no: skip it (YAGNI)
2. Already in this codebase?       → reuse it
3. Stdlib has it?                  → use it
4. Native feature?                 → use it
5. One line?                      → one line
6. Only then: minimum that works
```

### KISS — Keep It Simple, Stupid

- Simplest solution is usually best
- Each function/class does one thing
- Don't premature optimize

### DRY — Don't Repeat Yourself

- Extract repeated logic to functions
- Extract shared types
- Extract common utilities

---

## Architecture

### Clean Architecture Layers

```
Presentation → Application → Domain ← Infrastructure
```

- Outer layers depend on inner layers
- Inner layers NEVER depend on outer layers
- Infrastructure implements Domain interfaces

### Dependency Injection

```typescript
// ✅ Constructor injection
class UserService {
  constructor(
    private userRepository: IUserRepository,
    private emailService: IEmailService
  ) {}
}
```

---

## Security Rules

```
□ No hardcoded secrets
□ All user input validated
□ Parameterized SQL queries
□ Output escaped
□ Passwords hashed (bcrypt)
□ Rate limiting enabled
```

---

## Git Workflow

### Branch Naming

```
feature/{ticket-id}-short-description
fix/{ticket-id}-short-description
```

### Commit Format

```
<type>(<scope>): <subject>

feat(auth): add JWT refresh token
fix(payment): correct calculation
```

---

## Code Quality Checklist

```
□ Logic correct?
□ Edge cases handled?
□ Error handling complete?
□ Performance acceptable?
□ Test coverage sufficient?
□ Meaningful names?
□ Functions small (< 30 lines)?
□ No duplicate code?
```

---

## Development Lifecycle

```
DEFINE → PLAN → BUILD → TEST → REVIEW → SHIP
```

---

## Skills Available

- **create-feature**: Create new feature from spec
- **create-api**: Design and implement REST/GraphQL API
- **create-ui**: Design and implement UI components
- **database-migration**: Create and manage migrations
- **code-review**: Review code with quality gates
- **debug-error**: Debug and fix errors systematically

---

## Agent Personas

### Solution Architect
- Clean Architecture
- Technology selection
- System design

### Code Reviewer
- Correctness
- Design
- Security
- Performance

### Security Auditor
- OWASP Top 10
- Authentication/Authorization
- Vulnerability detection
