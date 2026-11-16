# GitHub Copilot Instructions

> **Tool:** GitHub Copilot | **Version:** 1.0.0

---

# Vibe Code Framework — Copilot Instructions

---

## Core Principles

### YAGNI — You Aren't Gonna Need It

**Don't write code for features that aren't needed yet.**

Before coding:
1. Does this need to be built? → no: skip it
2. Already in codebase? → reuse it
3. Stdlib has it? → use it
4. Native feature? → use it
5. One line? → one line
6. Only then: minimum that works

### KISS — Keep It Simple, Stupid

- Simplest solution is usually best
- Each function/class does one thing
- Don't premature optimize
- Readable > clever

### DRY — Don't Repeat Yourself

- Extract repeated logic to functions
- Extract shared types
- Extract common utilities

---

## Security Rules

```
□ No hardcoded secrets (API keys, passwords, tokens)
□ All user input validated
□ Parameterized SQL queries (no string concatenation)
□ Output escaped/sanitized
□ Passwords hashed (bcrypt/argon2)
□ Rate limiting enabled
□ HTTP security headers configured
□ Error messages sanitized
```

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

feat(auth): add JWT refresh token
fix(payment): correct calculation
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `style` | Formatting |
| `refactor` | Refactoring |
| `test` | Tests |
| `chore` | Maintenance |

---

## Code Quality

```
□ Logic correct?
□ Edge cases handled?
□ Error handling complete?
□ Performance acceptable?
□ Test coverage sufficient (> 80%)?
□ Meaningful names?
□ Functions small (< 30 lines)?
□ No duplicate code?
□ No console.log/debugger left?
```

---

## Type Safety

```
□ No `any` types
□ Use explicit types
□ Discriminated unions for state
□ Strict null checks enabled
```

---

## Testing

### Test Pyramid

```
Unit Tests (80%)
    ↓
Integration Tests (15%)
    ↓
E2E Tests (5%)
```

### Naming

```typescript
// [Unit] should [behavior] when [condition]
describe('UserService', () => {
  it('should create user with valid data', async () => { });
});
```

---

## Error Handling

```typescript
// ✅ Result type
async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const user = await db.findById(id);
    if (!user) return { success: false, error: 'NOT_FOUND' };
    return { success: true, data: user };
  } catch (e) {
    return { success: false, error: 'DB_ERROR' };
  }
}
```

---

## API Design

### RESTful Conventions

```
POST   /users      → Create user
GET    /users/:id  → Get user
GET    /users      → List users
PUT    /users/:id  → Update user
DELETE /users/:id  → Delete user
```

### Response Format

```typescript
// Success
{ "data": { ... }, "meta": { ... } }

// Error
{ "error": { "code": "...", "message": "..." } }
```

---

## Development Lifecycle

```
DEFINE → PLAN → BUILD → TEST → REVIEW → SHIP
```
