# Create API Skill

> **Version:** 1.0.0 | **Category:** Development | **Triggers:** tạo api, create api, build api, implement endpoint

---

## Goal

Thiết kế và implement REST/GraphQL API hoàn chỉnh:
- RESTful conventions
- Input validation
- Error handling
- Authentication/Authorization
- Documentation

## Trigger Conditions

- User yêu cầu tạo API endpoint mới
- User cần implement CRUD operations
- User cần tạo webhook
- User cần tạo internal API

## Pre-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ P.1: API Design                                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Resource đã được xác định?                               │
│ □ HTTP methods đã được chọn?                               │
│ □ URL structure đã được define?                            │
│ □ Response format đã được standardize?                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ P.2: Security Design                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Authentication method đã chọn? (JWT, API Key, OAuth)    │
│ □ Authorization logic đã defined?                           │
│ □ Rate limiting cần thiết?                                 │
│ □ Input validation schema đã có?                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ P.3: Integration Points                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Cần tạo database tables?                                 │
│ □ Gọi external APIs?                                       │
│ □ Publish events?                                          │
│ □ Queue messages?                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Process Steps

### Step 1: Design API Contract

```markdown
# API: /api/users

## Endpoints

### POST /api/users
Create a new user

**Request:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "SecurePass123!"
}
```

**Response (201):**
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2026-01-15T10:30:00Z"
  }
}
```

**Errors:**
- 400: Validation error
- 409: Email already exists

### GET /api/users/:id
Get user by ID

**Response (200):**
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2026-01-15T10:30:00Z"
  }
}
```

**Errors:**
- 404: User not found
```

### Step 2: Create Validation Schema

```typescript
import { z } from 'zod';

export const CreateUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  name: z.string().min(1, 'Name is required').max(100),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase')
    .regex(/[a-z]/, 'Password must contain lowercase')
    .regex(/[0-9]/, 'Password must contain number'),
});

export type CreateUserDTO = z.infer<typeof CreateUserSchema>;
```

### Step 3: Create Use Case

```typescript
export class CreateUserUseCase {
  constructor(
    private userRepository: IUserRepository,
    private eventPublisher: IEventPublisher
  ) {}
  
  async execute(dto: CreateUserDTO): Promise<Result<User>> {
    // 1. Validate
    const validated = CreateUserSchema.parse(dto);
    
    // 2. Check duplicates
    const existing = await this.userRepository.findByEmail(validated.email);
    if (existing) {
      return { success: false, error: 'EMAIL_EXISTS' };
    }
    
    // 3. Hash password
    const hashedPassword = await bcrypt.hash(validated.password, 12);
    
    // 4. Create user
    const user = User.create({
      ...validated,
      passwordHash: hashedPassword,
    });
    
    // 5. Persist
    await this.userRepository.create(user);
    
    // 6. Publish event
    await this.eventPublisher.publish(new UserCreatedEvent(user));
    
    return { success: true, data: user };
  }
}
```

### Step 4: Create Controller

```typescript
export class UserController {
  constructor(
    private createUserUseCase: CreateUserUseCase,
    private getUserUseCase: GetUserUseCase
  ) {}
  
  async create(req: Request, res: Response): Promise<void> {
    try {
      const result = await this.createUserUseCase.execute(req.body);
      
      if (!result.success) {
        const statusCode = this.getErrorStatusCode(result.error);
        res.status(statusCode).json({
          error: {
            code: result.error,
            message: this.getErrorMessage(result.error),
          }
        });
        return;
      }
      
      res.status(201).json({
        data: UserDTO.fromEntity(result.data),
      });
    } catch (error) {
      this.handleError(error, res);
    }
  }
  
  async getById(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const result = await this.getUserUseCase.execute(id);
      
      if (!result.success) {
        res.status(404).json({
          error: { code: 'NOT_FOUND', message: 'User not found' }
        });
        return;
      }
      
      res.json({ data: UserDTO.fromEntity(result.data) });
    } catch (error) {
      this.handleError(error, res);
    }
  }
  
  private handleError(error: unknown, res: Response): void {
    if (error instanceof ZodError) {
      res.status(400).json({
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid input',
          details: error.errors.map(e => ({
            field: e.path.join('.'),
            message: e.message,
          })),
        },
      });
      return;
    }
    
    logger.error('Unhandled error', { error });
    res.status(500).json({
      error: { code: 'INTERNAL_ERROR', message: 'Internal server error' }
    });
  }
}
```

### Step 5: Add Routes

```typescript
// routes/userRoutes.ts
const router = Router();

router.post(
  '/users',
  authenticate,
  validate(CreateUserSchema),
  userController.create.bind(userController)
);

router.get(
  '/users/:id',
  authenticate,
  userController.getById.bind(userController)
);

export default router;
```

### Step 6: Add Authentication Middleware

```typescript
export async function authenticate(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (!token) {
      res.status(401).json({ error: 'UNAUTHORIZED' });
      return;
    }
    
    const decoded = jwt.verify(token, config.jwt.secret) as JwtPayload;
    req.user = { id: decoded.userId, role: decoded.role };
    
    next();
  } catch (error) {
    res.status(401).json({ error: 'INVALID_TOKEN' });
  }
}
```

## Post-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ C.1: API Correctness                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ All endpoints respond correctly                          │
│ □ Status codes accurate                                    │
│ □ Response format matches spec                             │
│ □ Pagination works if applicable                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.2: Validation                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ All inputs validated                                     │
│ □ Validation errors are clear                              │
│ □ Edge cases handled (empty, null, overflow)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.3: Security                                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Authentication works                                     │
│ □ Authorization enforced                                   │
│ □ Rate limiting active                                     │
│ □ No sensitive data in responses                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.4: Performance                                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ N+1 queries resolved                                     │
│ □ Indexes used for lookups                                │
│ □ Large responses paginated                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.5: Documentation                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ OpenAPI spec updated                                     │
│ □ Examples provided                                       │
│ □ Error codes documented                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## API Response Templates

### Success Response
```typescript
{
  "data": { /* resource */ },
  "meta": { /* pagination info if applicable */ }
}
```

### Error Response
```typescript
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": [ /* field-level errors if applicable */ ]
  }
}
```

### List Response
```typescript
{
  "data": [ /* array of resources */ ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

## HTTP Status Code Guide

| Code | Usage |
|------|-------|
| 200 | Successful GET, PUT, PATCH |
| 201 | Resource created |
| 204 | Successful DELETE (no body) |
| 400 | Validation error |
| 401 | Not authenticated |
| 403 | Not authorized |
| 404 | Resource not found |
| 409 | Conflict (duplicate) |
| 422 | Business rule violation |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
| 502 | Bad gateway (external service fail) |
| 503 | Service unavailable |

## Related Skills

- [create-feature](./create-feature/) - Overall feature creation
- [database-migration](./database-migration/) - Database schema changes
- [code-review](./code-review/) - Review API implementation
