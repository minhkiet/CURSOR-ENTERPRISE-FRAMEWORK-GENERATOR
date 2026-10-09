# Nguyên tắc nền tảng

> **Version:** 1.0.0 | **Category:** Core Principles

---

## Tổng quan

Các nguyên tắc nền tảng hướng dẫn cách tư duy và ra quyết định trong quá trình phát triển. Áp dụng chúng trước khi viết bất kỳ dòng code nào.

---

## 1. YAGNI — You Aren't Gonna Need It

**Nguyên tắc:** Không viết code cho tính năng không cần thiết.

### Triển khai

```
┌────────────────────────────────────────────────────────────┐
│ YAGNI Ladder — Dừng ở bậc thang đầu tiên có thể giữ     │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Có cần xây không?          → không: skip (YAGNI)     │
│  2. Đã có trong codebase?       → reuse, đừng viết lại   │
│  3. Stdlib có không?             → dùng nó                │
│  4. Native platform feature?     → dùng nó                │
│  5. Đã cài dependency?          → dùng nó                │
│  6. Một dòng?                   → một dòng               │
│  7. Chỉ khi đó: tối thiểu nhất                                          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Ví dụ

**Sai:**
```typescript
// Dự đoán future requirement - viết "flexible" abstraction
interface Repository<T> {
  findAll(filter?: Filter<T>, pagination?: Pagination, sorting?: Sorting): Promise<T[]>;
  findById(id: string): Promise<T | null>;
  findOne(filter: Filter<T>): Promise<T | null>;
  create(data: CreateDTO<T>): Promise<T>;
  update(id: string, data: UpdateDTO<T>): Promise<T>;
  delete(id: string): Promise<void>;
  bulkCreate(items: CreateDTO<T>[]): Promise<T[]>;
  bulkUpdate(items: UpdateDTO<T>[]): Promise<T[]>;
  count(filter?: Filter<T>): Promise<number>;
  exists(filter: Filter<T>): Promise<boolean>;
}
```

**Đúng:**
```typescript
// Chỉ những gì cần ngay bây giờ
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  create(data: CreateUserDTO): Promise<User>;
}
```

---

## 2. KISS — Keep It Simple, Stupid

**Nguyên tắc:** Giải pháp đơn giản nhất thường là giải pháp tốt nhất.

### Quy tắc

1. **Ưu tiên đơn giản** — Nếu giải pháp phức tạp, tìm cách đơn giản hơn
2. **Một trách nhiệm** — Mỗi function/class chỉ làm một việc
3. **Tránh premature optimization** — Chạy được trước, tối ưu sau

### Ví dụ

**Sai:**
```typescript
// Over-engineered: singleton factory pattern cho một cái gì đơn giản
class DatabaseConnectionManager {
  private static instance: DatabaseConnectionManager;
  private connections: Map<string, Pool>;
  private retryPolicy: RetryPolicy;
  
  private constructor() {
    this.connections = new Map();
    this.retryPolicy = new ExponentialBackoffRetryPolicy();
  }
  
  static getInstance(): DatabaseConnectionManager {
    if (!this.instance) {
      this.instance = new DatabaseConnectionManager();
    }
    return this.instance;
  }
  
  async getConnection(config: DbConfig): Promise<Pool> {
    // 50 dòng code cho việc lấy connection
  }
}
```

**Đúng:**
```typescript
// Đơn giản: chỉ là một function
import { Pool } from 'pg';

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

export async function query<T>(text: string, params?: unknown[]): Promise<T[]> {
  const result = await pool.query(text, params);
  return result.rows;
}
```

---

## 3. DRY — Don't Repeat Yourself

**Nguyên tắc:** Mỗi kiến thức phải có một biểu diễn duy nhất trong hệ thống.

### Triển khai

```
┌─────────────────────────────────────────────────────────────┐
│ DRY Checklist                                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  □ Logic lặp lại → Extract thành function/module           │
│  □ Validation lặp lại → Extract thành validator            │
│  □ Type lặp lại → Extract thành shared type               │
│  □ Constant lặp lại → Extract thành constants file       │
│  □ Test lặp lại → Extract thành shared test utility       │
│                                                             │
│  ⚠️ Đừng DRY quá mức — có những lúc duplication           │
│     đáng giá hơn wrong abstraction                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Ví dụ

**Sai (Duplicate):**
```typescript
// User validation
function createUser(data: unknown) {
  if (!data.email || !data.email.includes('@')) {
    throw new Error('Invalid email');
  }
  if (!data.password || data.password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }
  // ...
}

// Admin validation - duplicate!
function createAdmin(data: unknown) {
  if (!data.email || !data.email.includes('@')) {
    throw new Error('Invalid email');
  }
  if (!data.password || data.password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }
  // ...
}
```

**Đúng (Shared):**
```typescript
// Shared validator
import { z } from 'zod';

const emailSchema = z.string().email();
const passwordSchema = z.string().min(8);

function validateUserInput(data: unknown) {
  const email = emailSchema.parse(data.email);
  const password = passwordSchema.parse(data.password);
  return { email, password };
}

// Sử dụng ở cả hai nơi
function createUser(data: unknown) {
  const { email, password } = validateUserInput(data);
  // ...
}
```

---

## 4. SOLID Principles

### S — Single Responsibility Principle

> Mỗi class chỉ có một lý do để thay đổi.

**Sai:**
```typescript
class User {
  save() { /* save to DB */ }
  sendEmail() { /* send email */ }
  generateReport() { /* generate PDF */ }
  calculateMetrics() { /* calculate analytics */ }
}
```

**Đúng:**
```typescript
class User {
  constructor(
    private repository: UserRepository,
    private emailService: EmailService
  ) {}
  
  save() { this.repository.save(this); }
  notify() { this.emailService.send(this.email); }
}
```

### O — Open/Closed Principle

> Mở rộng bằng kế thừa, đóng với sửa đổi.

**Sai:**
```typescript
function calculateArea(shape: { type: 'circle' | 'square'; radius?: number; side?: number }) {
  if (shape.type === 'circle') {
    return Math.PI * shape.radius! ** 2;
  }
  if (shape.type === 'square') {
    return shape.side! ** 2;
  }
  // Khi thêm shape mới, phải sửa function này
}
```

**Đúng:**
```typescript
interface Shape {
  area(): number;
}

class Circle implements Shape {
  constructor(private radius: number) {}
  area(): number { return Math.PI * this.radius ** 2; }
}

class Square implements Shape {
  constructor(private side: number) {}
  area(): number { return this.side ** 2; }
}
```

### L — Liskov Substitution Principle

> Objects của subclass có thể thay thế objects của parent class mà không làm sai behavior.

### I — Interface Segregation Principle

> Nhiều interfaces nhỏ, chuyên biệt tốt hơn một interface lớn.

### D — Dependency Inversion Principle

> Phụ thuộc vào abstractions, không phải concretions.

---

## 5. Pre-Implementation Checklist

Trước khi viết code, hãy tự hỏi:

```
┌─────────────────────────────────────────────────────────────┐
│ Pre-Implementation Checklist                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  □ Tôi đã hiểu rõ requirement chưa?                        │
│  □ Tôi đã thực sự cần tính năng này không? (YAGNI)         │
│  □ Có cách nào đơn giản hơn không? (KISS)                  │
│  □ Tôi đang duplicate code/logic không? (DRY)               │
│  □ Đây có phải là đúng abstraction không? (SOLID)          │
│  □ Tôi đã test được trong đầu chưa?                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Nguồn tham khảo

- [YAGNI - Martin Fowler](https://martinfowler.com/bliki/Yagni.html)
- [KISS Principle](https://people.apache.org/~fhanik/kiss.html)
- [DRY Principle](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
