# GEMINI.md — Google Antigravity Format

> **Version:** 1.0.0 | **Tool:** Google Antigravity (Gemini)

---

# Vibe Code Framework — Antigravity Instructions

---

## Tổng quan

Framework này sử dụng Vibe Code Framework - một cross-platform AI coding framework với:
- **Rules:** Nguyên tắc luôn phải tuân thủ
- **Skills:** Quy trình chuyên biệt cho từng task
- **Agents:** Vai trò chuyên môn

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
- Đừng premature optimize

### DRY — Don't Repeat Yourself

- Logic lặp lại → Extract thành function/module
- Type lặp lại → Extract thành shared type
- Validation lặp lại → Extract thành validator

---

## Security Rules

```
□ No hardcoded secrets
□ All user input validated
□ Parameterized SQL queries
□ Output escaped/sanitized
□ Passwords hashed (bcrypt)
□ Rate limiting enabled
```

---

## Architecture

### Clean Architecture

```
Presentation → Application → Domain ← Infrastructure
```

- Outer layers phụ thuộc vào inner layers
- Inner layers KHÔNG phụ thuộc vào outer layers

### Dependency Injection

```typescript
// ✅ Constructor injection
class UserService {
  constructor(
    private userRepository: IUserRepository
  ) {}
}
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

feat(auth): add JWT
fix(payment): correct calc
```

---

## Code Quality Checklist

```
□ Logic đúng?
□ Edge cases xử lý?
□ Error handling đầy đủ?
□ Performance acceptable?
□ Test coverage đủ (> 80%)?
□ Naming rõ ràng?
□ Functions nhỏ (< 30 lines)?
□ Không duplicate code?
□ Không console.log/debugger?
```

---

## Development Lifecycle

```
DEFINE → PLAN → BUILD → TEST → REVIEW → SHIP
```

---

## Skills

| Skill | Purpose |
|-------|---------|
| `create-feature` | Tạo feature mới |
| `create-api` | Thiết kế REST API |
| `create-ui` | Thiết kế UI |
| `database-migration` | Quản lý migrations |
| `code-review` | Review code |
| `debug-error` | Debug lỗi |

---

## Liên kết

- [Vibe Code Framework](../vibe-code-framework/README.md)
