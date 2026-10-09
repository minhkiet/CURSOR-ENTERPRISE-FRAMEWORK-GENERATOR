# Chất lượng code

> **Version:** 1.0.0 | **Category:** Code Quality

---

## Tổng quan

Chất lượng code bao gồm các nguyên tắc viết code sạch, dễ đọc, dễ bảo trì và có test coverage tốt.

---

## 1. Clean Code Principles

### 1.1 Meaningful Names

**Nguyên tắc:** Tên biến, function, class phải mô tả rõ ý nghĩa.

```
┌─────────────────────────────────────────────────────────────┐
│ Naming Convention Quick Reference                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Variables     → noun, descriptive                          │
│  Functions     → verb, action-oriented                       │
│  Classes       → noun, PascalCase                            │
│  Constants     → UPPER_SNAKE_CASE                          │
│  Interfaces    → PascalCase, thường có prefix I             │
│  Types         → PascalCase                                 │
│                                                             │
│  ✅ good: userCount, isActive, getUserById                  │
│  ❌ bad: data, temp, x, doStuff                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Ví dụ

**Sai:**
```typescript
const d = new Date();
const x = users.filter(u => u.s === 'active');
const fn = (n) => n * 2;
```

**Đúng:**
```typescript
const currentDate = new Date();
const activeUsers = users.filter(user => user.status === 'active');
const doubleValue = (value: number) => value * 2;
```

### 1.2 Small Functions

**Nguyên tắc:** Function nên làm một việc, làm tốt, và ngắn gọn.

| Lines | Rating |
|-------|--------|
| 1-10 | ✅ Ideal |
| 11-20 | ✅ Good |
| 21-30 | ⚠️ Caution |
| 30+ | ❌ Should split |

### Ví dụ

**Sai:**
```typescript
async function processOrder(order: Order) {
  // Validate order (10 lines)
  // Calculate total (5 lines)
  // Check inventory (15 lines)
  // Reserve items (10 lines)
  // Process payment (20 lines)
  // Send confirmation (8 lines)
  // Update analytics (5 lines)
  // Send webhook (5 lines)
  // Update inventory (10 lines)
  // Generate invoice (15 lines)
  // Send email (8 lines)
}
```

**Đúng:**
```typescript
async function processOrder(order: Order): Promise<void> {
  const validatedOrder = await validateOrder(order);
  const total = await calculateTotal(validatedOrder);
  await reserveInventory(validatedOrder);
  await processPayment(validatedOrder, total);
  await sendOrderConfirmation(validatedOrder);
}
```

### 1.3 Early Returns

**Nguyên tắc:** Return sớm để giảm nesting và improve readability.

**Sai:**
```typescript
function processUser(user: User | null): Result {
  if (user !== null) {
    if (user.isActive) {
      if (user.email) {
        return doSomething(user);
      } else {
        return { error: 'No email' };
      }
    } else {
      return { error: 'User not active' };
    }
  } else {
    return { error: 'User not found' };
  }
}
```

**Đúng:**
```typescript
function processUser(user: User | null): Result {
  if (!user) {
    return { error: 'User not found' };
  }
  
  if (!user.isActive) {
    return { error: 'User not active' };
  }
  
  if (!user.email) {
    return { error: 'No email' };
  }
  
  return doSomething(user);
}
```

---

## 2. Error Handling

### 2.1 Use Result Types

**Nguyên tắc:** Handle errors explicitly, don't swallow exceptions.

### Ví dụ

**Sai:**
```typescript
try {
  const user = await fetchUser(id);
  return user;
} catch (e) {
  // Swallowed!
}
```

**Đúng:**
```typescript
async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const user = await db.findById(id);
    if (!user) {
      return { error: 'User not found' };
    }
    return { data: user };
  } catch (e) {
    logger.error('Failed to fetch user', { id, error: e });
    return { error: 'Database error' };
  }
}
```

### 2.2 Custom Error Classes

```typescript
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'AppError';
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 'NOT_FOUND', 404);
  }
}

class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 'VALIDATION_ERROR', 400);
  }
}
```

---

## 3. Type Safety

### 3.1 Avoid `any`

**Nguyên tắc:** Use explicit types, avoid `any`.

```typescript
// ❌ any
function processData(data: any): any {
  return data.value;
}

// ✅ explicit
function processData(data: DataInput): OutputType {
  return data.value;
}
```

### 3.2 Use Discriminated Unions

```typescript
// ❌ Nullable without context
type User = UserData | null;

// ✅ Discriminated union
type UserResult = 
  | { success: true; data: UserData }
  | { success: false; error: string };
```

### 3.3 Strict Null Checks

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

---

## 4. Testing Strategy

### 4.1 Test Pyramid

```
         ▲
        ╱ ╲
       ╱   ╲
      ╱     ╲     E2E (5%)
     ╱───────╲
    ╱         ╲
   ╱───────────╲   Integration (15%)
  ╱             ╲
 ╱───────────────╲
╱                 ╲  Unit Tests (80%)
╱───────────────────╲
──────────────────────
```

### 4.2 Naming Conventions

```typescript
// [Unit] should [behavior] when [condition]
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      // test
    });
    
    it('should throw ValidationError with invalid email', async () => {
      // test
    });
  });
});
```

### 4.3 Test Coverage Goals

| Type | Target |
|------|--------|
| Happy path | 100% |
| Error paths | 80%+ |
| Edge cases | Documented |
| Overall | 80%+ |

### 4.4 Example Tests

```typescript
import { describe, it, expect, vi } from 'vitest';
import { UserService } from './UserService';
import { ValidationError } from './errors';

describe('UserService', () => {
  const mockRepository = {
    create: vi.fn(),
    findByEmail: vi.fn(),
  };
  
  const service = new UserService(mockRepository);
  
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      const input = {
        email: 'test@example.com',
        password: 'SecurePass123!',
        name: 'Test User',
      };
      
      mockRepository.create.mockResolvedValue({ id: '1', ...input });
      
      const result = await service.createUser(input);
      
      expect(result).toMatchObject({ id: '1', email: input.email });
      expect(mockRepository.create).toHaveBeenCalledOnce();
    });
    
    it('should throw ValidationError with invalid email', async () => {
      const input = {
        email: 'invalid-email',
        password: 'SecurePass123!',
        name: 'Test User',
      };
      
      await expect(service.createUser(input))
        .rejects.toThrow(ValidationError);
    });
  });
});
```

---

## 5. Code Review Checklist

```
┌─────────────────────────────────────────────────────────────┐
│ Code Review Checklist                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  □ Logic đúng?                                             │
│  □ Edge cases được xử lý?                                  │
│  □ Error handling đầy đủ?                                  │
│  □ Performance acceptable?                                  │
│  □ Security concerns?                                       │
│  □ Test coverage đủ?                                        │
│  □ Naming rõ ràng?                                         │
│  □ Functions small & focused?                               │
│  □ No duplicate code?                                       │
│  □ Documentation cần thiết?                                 │
│  □ Breaking changes được communicate?                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Nguồn tham khảo

- [Clean Code](https://www.goodreads.com/book/show/3735293-clean-code) - Robert C. Martin
- [Effective JavaScript](https://www.pearson.com/en-us/subject-catalog/p/effective-javascript/P200000000470) - David Herman
- [Testing Trophy](https://kentcdodds.com/blog/write-tests) - Kent C. Dodds
