# Kiến trúc hệ thống

> **Version:** 1.0.0 | **Category:** Architecture

---

## Tổng quan

Nguyên tắc kiến trúc hướng dẫn cách tổ chức code, phân chia layer, và quản lý dependencies để tạo ra hệ thống dễ bảo trì và mở rộng.

---

## 1. Clean Architecture

### Layer Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    Clean Architecture                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                   Presentation                       │   │
│   │   (Controllers, API Routes, UI Components)           │   │
│   └─────────────────────────────────────────────────────┘   │
│                           ↓ ↑                                │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                   Application                         │   │
│   │   (Use Cases, DTOs, Application Services)            │   │
│   └─────────────────────────────────────────────────────┘   │
│                           ↓ ↑                                │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                      Domain                          │   │
│   │   (Entities, Value Objects, Domain Services)         │   │
│   └─────────────────────────────────────────────────────┘   │
│                           ↓ ↑                                │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                  Infrastructure                      │   │
│   │   (Database, External APIs, File System)             │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Dependency Rule

```
┌────────────────────────────────────────────────────────────┐
│ Dependency Rule                                             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   Outer layers có thể phụ thuộc vào inner layers          │
│   Inner layers KHÔNG BAO GIỜ phụ thuộc vào outer layers   │
│                                                            │
│   Presentation → Application → Domain ← Infrastructure     │
│                                                            │
│   Infrastructure phải implement interfaces từ Domain        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Example Structure

```
src/
├── domain/                    # Domain Layer (core)
│   ├── entities/
│   │   └── User.ts
│   ├── value-objects/
│   │   └── Email.ts
│   ├── interfaces/
│   │   ├── IUserRepository.ts
│   │   └── IEmailService.ts
│   └── services/
│       └── UserDomainService.ts
│
├── application/               # Application Layer
│   ├── use-cases/
│   │   ├── CreateUserUseCase.ts
│   │   └── UpdateUserUseCase.ts
│   ├── dto/
│   │   ├── CreateUserDTO.ts
│   │   └── UserDTO.ts
│   └── ports/
│       └── UserService.ts
│
├── infrastructure/            # Infrastructure Layer
│   ├── database/
│   │   ├── repositories/
│   │   │   └── UserRepository.ts
│   │   └── migrations/
│   └── services/
│       └── EmailService.ts
│
└── presentation/              # Presentation Layer
    ├── api/
    │   ├── controllers/
    │   │   └── UserController.ts
    │   └── routes/
    │       └── userRoutes.ts
    └── middleware/
        └── auth.ts
```

---

## 2. Dependency Injection

### 2.1 Constructor Injection

**Nguyên tắc:** Inject dependencies qua constructor, không tạo bên trong class.

```typescript
// ❌ Hardcoded dependency
class UserService {
  private repository = new UserRepository();
  private emailService = new EmailService();
}

// ✅ Constructor injection
class UserService {
  constructor(
    private userRepository: IUserRepository,
    private emailService: IEmailService
  ) {}
}
```

### 2.2 Interface-Based Design

```typescript
// Domain defines interface
interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  create(user: User): Promise<User>;
  update(id: string, data: Partial<User>): Promise<User>;
  delete(id: string): Promise<void>;
}

// Infrastructure implements interface
class PostgresUserRepository implements IUserRepository {
  constructor(private db: Database) {}
  
  async findById(id: string): Promise<User | null> {
    return this.db.query('SELECT * FROM users WHERE id = $1', [id]);
  }
  
  // ... other methods
}
```

---

## 3. Repository Pattern

### 3.1 Purpose

Tách biệt logic truy cập data khỏi business logic.

### 3.2 Interface

```typescript
interface IRepository<T, TId> {
  findById(id: TId): Promise<T | null>;
  findAll(filter?: Filter): Promise<T[]>;
  create(entity: T): Promise<T>;
  update(id: TId, entity: Partial<T>): Promise<T>;
  delete(id: TId): Promise<void>;
  count(filter?: Filter): Promise<number>;
}
```

### 3.3 Implementation

```typescript
class UserRepository implements IRepository<User, string> {
  constructor(private db: Database) {}
  
  async findById(id: string): Promise<User | null> {
    const result = await this.db.query(
      'SELECT * FROM users WHERE id = $1',
      [id]
    );
    return result.rows[0] || null;
  }
  
  async findByEmail(email: string): Promise<User | null> {
    const result = await this.db.query(
      'SELECT * FROM users WHERE email = $1',
      [email]
    );
    return result.rows[0] || null;
  }
  
  // ... other methods
}
```

---

## 4. Service Layer

### 4.1 Application Services

Xử lý use case cụ thể, điều phối giữa presentation và domain.

```typescript
class CreateUserUseCase {
  constructor(
    private userRepository: IUserRepository,
    private emailService: IEmailService,
    private eventDispatcher: IEventDispatcher
  ) {}
  
  async execute(dto: CreateUserDTO): Promise<Result<User>> {
    // 1. Validate
    const validation = this.validate(dto);
    if (!validation.success) {
      return { success: false, error: validation.error };
    }
    
    // 2. Check duplicates
    const existing = await this.userRepository.findByEmail(dto.email);
    if (existing) {
      return { success: false, error: 'Email already exists' };
    }
    
    // 3. Create
    const user = User.create(dto);
    await this.userRepository.create(user);
    
    // 4. Send notification
    await this.emailService.sendWelcome(user.email);
    
    // 5. Dispatch events
    await this.eventDispatcher.dispatch(new UserCreatedEvent(user));
    
    return { success: true, data: user };
  }
}
```

### 4.2 Domain Services

Logic nghiệp vụ không thuộc về một entity cụ thể.

```typescript
class UserDomainService {
  constructor(private userRepository: IUserRepository) {}
  
  async transferOwnership(
    userId: string, 
    newOwnerId: string
  ): Promise<Result<void>> {
    const user = await this.userRepository.findById(userId);
    const newOwner = await this.userRepository.findById(newOwnerId);
    
    if (!user || !newOwner) {
      return { success: false, error: 'User not found' };
    }
    
    if (!newOwner.isAdmin) {
      return { success: false, error: 'New owner must be admin' };
    }
    
    user.transferOwnership(newOwnerId);
    await this.userRepository.update(userId, user);
    
    return { success: true };
  }
}
```

---

## 5. API Design

### 5.1 RESTful Conventions

```
┌────────────────────────────────────────────────────────────┐
│ RESTful Endpoint Convention                                │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Resource (plural noun)                                    │
│  ├── GET    /users           → List users                 │
│  ├── GET    /users/:id       → Get user                   │
│  ├── POST   /users           → Create user                 │
│  ├── PUT    /users/:id       → Update user                 │
│  ├── PATCH  /users/:id       → Partial update              │
│  ├── DELETE /users/:id       → Delete user                 │
│  └── GET    /users/:id/posts → Get user's posts           │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 5.2 Response Format

```typescript
// Success
{
  "data": { ... },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  }
}
```

---

## 6. Configuration Management

### 6.1 Environment-Based Config

```typescript
// config/index.ts
const config = {
  database: {
    host: process.env.DB_HOST,
    port: parseInt(process.env.DB_PORT || '5432'),
    name: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
  },
  
  api: {
    port: parseInt(process.env.PORT || '3000'),
    env: process.env.NODE_ENV,
    corsOrigins: process.env.CORS_ORIGINS?.split(',') || [],
  },
  
  auth: {
    jwtSecret: process.env.JWT_SECRET,
    jwtExpiry: process.env.JWT_EXPIRY || '15m',
    refreshSecret: process.env.REFRESH_SECRET,
    refreshExpiry: process.env.REFRESH_EXPIRY || '7d',
  },
};

export default config;
```

### 6.2 Validation

```typescript
import { z } from 'zod';

const configSchema = z.object({
  database: z.object({
    host: z.string(),
    port: z.number().int().positive(),
    name: z.string(),
    user: z.string(),
    password: z.string(),
  }),
  api: z.object({
    port: z.number().int().min(1).max(65535),
    env: z.enum(['development', 'staging', 'production']),
  }),
  auth: z.object({
    jwtSecret: z.string().min(32),
    jwtExpiry: z.string(),
  }),
});

// Validate on startup
const validated = configSchema.safeParse(config);
if (!validated.success) {
  throw new Error(`Invalid config: ${validated.error}`);
}

export default validated.data;
```

---

## 7. Error Handling Strategy

```
┌────────────────────────────────────────────────────────────┐
│ Error Handling Strategy                                     │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Domain Errors (Business Logic)                            │
│  ├── NotFoundError        → 404                           │
│  ├── ValidationError      → 400                           │
│  ├── ConflictError        → 409                           │
│  └── DomainRuleError      → 422                           │
│                                                            │
│  Infrastructure Errors (External)                          │
│  ├── DatabaseError        → 500 (log detailed)             │
│  ├── ExternalServiceError → 502/503                        │
│  └── TimeoutError         → 504                           │
│                                                            │
│  All errors: Log details server-side                       │
│             Return generic message client-side              │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Nguồn tham khảo

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) - Robert C. Martin
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn
- [Repository Pattern](https://docs.microsoft.com/en-us/aspnet/csharp/fundamentals/coding-concepts/cqrs-and-event-sourcing)
