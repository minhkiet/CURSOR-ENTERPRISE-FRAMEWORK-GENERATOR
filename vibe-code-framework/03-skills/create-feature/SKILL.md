# Create Feature Skill

> **Version:** 1.0.0 | **Category:** Development | **Triggers:** tạo feature, implement feature, add new feature, build feature

---

## Goal

Tạo feature mới từ specification đến implementation hoàn chỉnh:
- Clean Architecture với proper layer separation
- Test coverage đầy đủ (80%+)
- Security checks passed
- Documentation đầy đủ

## Trigger Conditions

Skill này được kích hoạt khi:
- User yêu cầu tạo feature mới
- User muốn implement một tính năng cụ thể
- User muốn thêm functionality vào hệ thống

## Pre-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ P.1: Requirements Understanding                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Đã hiểu rõ feature cần làm gì?                          │
│ □ Đã xác định user stories/acceptance criteria?             │
│ □ Đã clarify ambiguous points với user?                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ P.2: Design Review                                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Đã xác định các components cần tạo?                     │
│ □ Đã design API contracts?                                  │
│ □ Đã design database schema nếu cần?                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ P.3: Environment Check                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Branch đúng và updated?                                   │
│ □ Không có uncommitted changes conflict?                     │
│ □ Tests pass ở current state?                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Process Steps

### Step 1: Create Specification

Tạo spec document trước khi code:

```markdown
# Feature: [Tên Feature]

## Overview
[Mô tả ngắn về feature, tại sao cần feature này]

## User Stories
- **As a** [user type], **I want** [action], **so that** [benefit]

## Requirements
1. [Requirement 1 - must have]
2. [Requirement 2 - must have]
3. [Requirement 3 - nice to have]

## Acceptance Criteria
- [ ] AC1: [Criteria - verifiable outcome]
- [ ] AC2: [Criteria - verifiable outcome]
- [ ] AC3: [Criteria - verifiable outcome]

## Technical Design

### Domain
- Entity: [name]
- Value Objects: [list]
- Domain Events: [list]

### Application
- Use Cases: [list]
- DTOs: [list]

### Infrastructure
- Database: [tables/changes]
- External Services: [list]

### API
```
POST   /api/resource        - Create
GET    /api/resource/:id    - Read one
GET    /api/resource        - List
PUT    /api/resource/:id    - Update
DELETE /api/resource/:id    - Delete
```

## Out of Scope
- [Item 1]
- [Item 2]

## Dependencies
- [Dependency 1]
- [Dependency 2]

## Risks
| Risk | Mitigation |
|------|------------|
| [Risk 1] | [Mitigation] |
```

### Step 2: Create Domain Layer

```
Domain Layer
├── entities/
│   └── [EntityName].ts
├── value-objects/
│   └── [ValueObject].ts
├── interfaces/
│   ├── I[Entity]Repository.ts
│   └── I[External]Service.ts
└── services/
    └── [DomainService].ts
```

**Entity Pattern:**
```typescript
class User {
  private constructor(
    private readonly id: string,
    private email: Email,
    private name: string,
    private status: UserStatus
  ) {}
  
  static create(props: CreateUserProps): User {
    // Validate
    if (!props.email) {
      throw new ValidationError('Email is required');
    }
    
    return new User(
      generateId(),
      Email.create(props.email),
      props.name,
      UserStatus.ACTIVE
    );
  }
  
  // Business methods
  deactivate(): void {
    this.status = UserStatus.INACTIVE;
    this.addDomainEvent(new UserDeactivatedEvent(this.id));
  }
}
```

### Step 3: Create Application Layer

```
Application Layer
├── use-cases/
│   ├── Create[Entity]UseCase.ts
│   ├── Get[Entity]UseCase.ts
│   ├── Update[Entity]UseCase.ts
│   └── Delete[Entity]UseCase.ts
├── dto/
│   ├── Create[Entity]DTO.ts
│   └── [Entity]DTO.ts
└── ports/
    └── [Entity]Service.ts
```

**Use Case Pattern:**
```typescript
class CreateUserUseCase {
  constructor(
    private userRepository: IUserRepository,
    private emailService: IEmailService
  ) {}
  
  async execute(dto: CreateUserDTO): Promise<Result<User>> {
    // 1. Validate input
    const validated = CreateUserDTO.parse(dto);
    if (!validated.success) {
      return { success: false, error: validated.error };
    }
    
    // 2. Check business rules
    const existing = await this.userRepository.findByEmail(dto.email);
    if (existing) {
      return { success: false, error: 'Email already exists' };
    }
    
    // 3. Create entity
    const user = User.create(validated.data);
    
    // 4. Persist
    await this.userRepository.create(user);
    
    // 5. Side effects
    await this.emailService.sendWelcome(user.email);
    
    return { success: true, data: user };
  }
}
```

### Step 4: Create Infrastructure Layer

```
Infrastructure Layer
├── database/
│   ├── repositories/
│   │   └── [Entity]Repository.ts
│   └── migrations/
│       └── [timestamp]_create_[table].sql
└── services/
    └── [External]Service.ts
```

**Repository Pattern:**
```typescript
class PostgresUserRepository implements IUserRepository {
  constructor(private db: Database) {}
  
  async findById(id: string): Promise<User | null> {
    const result = await this.db.query(
      'SELECT * FROM users WHERE id = $1',
      [id]
    );
    return result.rows[0] ? this.mapToEntity(result.rows[0]) : null;
  }
  
  async create(user: User): Promise<void> {
    await this.db.query(
      `INSERT INTO users (id, email, name, status, created_at)
       VALUES ($1, $2, $3, $4, $5)`,
      [user.id, user.email.value, user.name, user.status, user.createdAt]
    );
  }
}
```

### Step 5: Create Presentation Layer

```
Presentation Layer
├── api/
│   ├── controllers/
│   │   └── [Entity]Controller.ts
│   └── routes/
│       └── [entity]Routes.ts
└── middleware/
    ├── auth.ts
    └── validation.ts
```

**Controller Pattern:**
```typescript
class UserController {
  constructor(private createUserUseCase: CreateUserUseCase) {}
  
  async create(req: Request, res: Response): Promise<void> {
    const result = await this.createUserUseCase.execute(req.body);
    
    if (!result.success) {
      res.status(400).json({ error: result.error });
      return;
    }
    
    res.status(201).json({ data: result.data });
  }
}
```

### Step 6: Write Tests

```
tests/
├── unit/
│   ├── domain/
│   │   └── User.test.ts
│   └── application/
│       └── CreateUserUseCase.test.ts
└── integration/
    └── api/
        └── UserController.test.ts
```

**Test Pattern:**
```typescript
describe('CreateUserUseCase', () => {
  const mockRepository = {
    findByEmail: vi.fn(),
    create: vi.fn(),
  };
  
  const useCase = new CreateUserUseCase(mockRepository);
  
  it('should create user with valid data', async () => {
    const dto = {
      email: 'test@example.com',
      name: 'Test User',
      password: 'SecurePass123!',
    };
    
    mockRepository.findByEmail.mockResolvedValue(null);
    mockRepository.create.mockResolvedValue(undefined);
    
    const result = await useCase.execute(dto);
    
    expect(result.success).toBe(true);
    expect(result.data?.email.value).toBe(dto.email);
  });
  
  it('should fail with duplicate email', async () => {
    const dto = {
      email: 'existing@example.com',
      name: 'Test User',
      password: 'SecurePass123!',
    };
    
    mockRepository.findByEmail.mockResolvedValue({ id: '1' });
    
    const result = await useCase.execute(dto);
    
    expect(result.success).toBe(false);
    expect(result.error).toBe('Email already exists');
  });
});
```

## Post-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ C.1: Code Quality                                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ npm run lint passed                                      │
│ □ npm run type-check passed                                │
│ □ No console.log/debugger left                             │
│ □ No TODO comments without ticket                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.2: Tests                                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Unit tests: all passed                                   │
│ □ Integration tests: all passed                            │
│ □ Coverage: > 80%                                          │
│ □ Edge cases tested                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.3: Functionality                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Feature works as specified                               │
│ □ Edge cases handled                                       │
│ □ Error handling correct                                   │
│ □ Error messages user-friendly                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.4: Security                                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ No hardcoded secrets                                     │
│ □ Input validated (Zod/Joi)                               │
│ □ SQL injection protected                                   │
│ □ XSS protected                                            │
│ □ Rate limiting if needed                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.5: Documentation                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Complex logic commented                                  │
│ □ README updated if public API                            │
│ □ API docs updated                                        │
│ □ CHANGELOG updated                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Output

```
✅ Feature hoàn chỉnh
├── Domain layer (entity, interfaces)
├── Application layer (use cases, DTOs)
├── Infrastructure layer (repository, migrations)
├── Presentation layer (controller, routes)
├── Tests (unit + integration)
└── Documentation (if needed)
```

## Error Handling

| Error | Response |
|-------|----------|
| Requirements unclear | Dừng, hỏi user để clarify |
| Design issue discovered | Đề xuất alternatives, get approval |
| Test failure | Debug và fix code hoặc fix test |
| Build failure | Check dependencies, imports |
| Database migration error | Rollback, fix migration |

## Related Skills

- [create-api](./create-api/) - Nếu feature cần API mới
- [database-migration](./database-migration/) - Nếu feature cần schema change
- [code-review](./code-review/) - Áp dụng sau khi feature xong
