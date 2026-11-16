# Vibe Code Framework — Vibe Code Framework

> **Version:** 1.0.0 | **Tool:** Cursor | **Generated from:** vibe-code-framework

---

## Tổng quan

Framework này sử dụng Vibe Code Framework - một cross-platform AI coding framework với:
- **Rules:** Nguyên tắc luôn phải tuân thủ
- **Skills:** Quy trình chuyên biệt cho từng task
- **Agents:** Vai trò chuyên môn

---

## Agent Personas

### Solution Architect

**Role:** Architecture Design  
**Perspective:** "Design before code, architect for change"

- Clean Architecture
- Hexagonal Architecture
- CQRS
- Domain-Driven Design
- Technology Selection

### Code Reviewer

**Role:** Senior Staff Engineer  
**Perspective:** "Would a staff engineer approve this?"

**Review Axes:**
1. **Correctness** — Logic, edge cases, error paths
2. **Design** — SRP, OCP, dependencies, layer separation
3. **Readability** — Names, function size, comments
4. **Security** — Secrets, input validation, injection
5. **Performance** — N+1, indexes, caching

### Security Auditor

**Role:** Security Engineer  
**Perspective:** "Assume breach, verify defense"

- OWASP Top 10
- Authentication & Authorization
- Input Validation
- Secrets Management
- Supply Chain Security

### Database Engineer

**Role:** Data Specialist  
**Perspective:** "Schema first, optimize later"

- Schema Design
- Query Optimization
- Indexing Strategy
- Migration Safety
- Data Integrity

---

## Development Lifecycle

```
DEFINE          PLAN           BUILD          VERIFY         SHIP
┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
│ Idea │ ───▶ │ Spec │ ───▶ │ Code │ ───▶ │ Test │ ───▶ │  Go  │
│Refine│      │  PRD │      │ Impl │      │Debug │      │ Live │
└──────┘      └──────┘      └──────┘      └──────┘      └──────┘
```

---

## Core Principles

### YAGNI — You Aren't Gonna Need It

```
1. Có cần xây không?          → không: skip (YAGNI)
2. Đã có trong codebase?       → reuse, đừng viết lại
3. Stdlib có không?             → dùng nó
4. Native platform feature?     → dùng nó
5. Đã cài dependency?          → dùng nó
6. Một dòng?                   → một dòng
7. Chỉ khi đó: tối thiểu nhất
```

### KISS — Keep It Simple, Stupid

- Giải pháp đơn giản nhất thường là tốt nhất
- Mỗi function/class chỉ làm một việc
- Tránh premature optimization

### DRY — Don't Repeat Yourself

- Logic lặp lại → Extract thành function/module
- Validation lặp lại → Extract thành validator
- Type lặp lại → Extract thành shared type

---

## Security Checklist

```
□ No hardcoded secrets
□ All user input validated
□ Parameterized SQL queries
□ Output escaped/sanitized
□ Passwords hashed (bcrypt/argon2)
□ Rate limiting enabled
□ Secure headers configured
□ Error messages sanitized
□ Authentication required for protected routes
□ Authorization checked per action
```

---

## Architecture Rules

### Clean Architecture Layers

```
Presentation → Application → Domain ← Infrastructure
```

- Outer layers phụ thuộc vào inner layers
- Inner layers KHÔNG phụ thuộc vào outer layers
- Infrastructure implement interfaces từ Domain

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
fix(payment): correct tax calculation
```

### PR Size

| Size | Lines | Recommendation |
|------|-------|----------------|
| XS | 1-10 | ✅ Ideal |
| S | 11-50 | ✅ Good |
| M | 51-200 | ⚠️ Split if possible |
| XL | 500+ | ❌ Must split |

---

## Code Quality Checklist

```
□ Logic đúng?
□ Edge cases được xử lý?
□ Error handling đầy đủ?
□ Performance acceptable?
□ Test coverage đủ?
□ Naming rõ ràng?
□ Functions small & focused?
□ No duplicate code?
□ No console.log/debugger left?
```

---

## Quick Reference

### Which Agent for Which Task?

| Task | Agent |
|------|-------|
| Architecture design | Solution Architect |
| Code review | Code Reviewer |
| Security audit | Security Auditor |
| Database changes | Database Engineer |
| Full feature | Solution Architect → Implementation |

---

## Links

- [Vibe Code Framework](https://github.com/vibe-code-framework)
- [OWASP Top 10](https://owasp.org/Top10/)
- [Conventional Commits](https://www.conventionalcommits.org/)
