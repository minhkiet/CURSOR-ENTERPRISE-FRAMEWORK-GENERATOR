# Testing Skill

> **Version:** 1.0.0 | **Category:** Quality | **Triggers:** test, testing, unit test, integration test, tdd

---

## Goal

Implement comprehensive testing strategy:
- Unit tests (80%)
- Integration tests (15%)
- E2E tests (5%)

## Trigger Conditions

- Writing new feature
- Fixing bug
- Before deployment

## Pre-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ P.1: Test Strategy                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Unit tests for business logic?                           │
│ □ Integration tests for API?                              │
│ □ E2E tests for critical flows?                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Process Steps

### 1. Unit Tests

```
┌────────────────────────────────────────────────────────────┐
│ Unit Test Characteristics                                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Scope: Single function/method                          │
│  Speed: < 10ms                                           │
│  Dependencies: Mocked                                    │
│  Coverage Target: 80%+                                   │
│                                                            │
│  When to Write:                                         │
│  ├── Business logic                                     │
│  ├── Complex algorithms                                 │
│  ├── Data transformations                               │
│  └── Validation logic                                   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 2. Integration Tests

```
┌────────────────────────────────────────────────────────────┐
│ Integration Test Characteristics                          │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Scope: Multiple components                            │
│  Speed: < 100ms                                         │
│  Dependencies: Real DB, mocked external services          │
│  Coverage Target: 50%+                                 │
│                                                            │
│  When to Write:                                         │
│  ├── API endpoints                                     │
│  ├── Database operations                                │
│  ├── Service integrations                               │
│  └── Auth flows                                        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 3. E2E Tests

```
┌────────────────────────────────────────────────────────────┐
│ E2E Test Characteristics                                 │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Scope: Full application                                 │
│  Speed: > 100ms                                          │
│  Dependencies: Real everything                            │
│  Coverage Target: Critical paths only                     │
│                                                            │
│  When to Write:                                         │
│  ├── User login                                         │
│  ├── Checkout flow                                      │
│  ├── Critical business flows                            │
│  └── Smoke tests                                       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Test Pyramid

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

## Test Naming Convention

```typescript
// Pattern: [Unit] should [behavior] when [condition]
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      // ...
    });
    
    it('should throw ValidationError with invalid email', async () => {
      // ...
    });
    
    it('should throw ConflictError with duplicate email', async () => {
      // ...
    });
  });
});
```

## Example Tests

### Unit Test

```typescript
// userService.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserService } from './userService';
import { IUserRepository, MockUserRepository } from './mocks';

describe('UserService', () => {
  let service: UserService;
  let mockRepository: MockUserRepository;
  
  beforeEach(() => {
    mockRepository = new MockUserRepository();
    service = new UserService(mockRepository);
  });
  
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      const dto = {
        email: 'test@example.com',
        password: 'SecurePass123!',
        name: 'Test User'
      };
      
      mockRepository.findByEmail.mockResolvedValue(null);
      mockRepository.create.mockResolvedValue({ id: '1', ...dto });
      
      const result = await service.createUser(dto);
      
      expect(result.success).toBe(true);
      expect(result.data?.email).toBe(dto.email);
      expect(mockRepository.create).toHaveBeenCalledOnce();
    });
    
    it('should fail with duplicate email', async () => {
      const dto = {
        email: 'existing@example.com',
        password: 'SecurePass123!',
        name: 'Test User'
      };
      
      mockRepository.findByEmail.mockResolvedValue({ id: '1' });
      
      const result = await service.createUser(dto);
      
      expect(result.success).toBe(false);
      expect(result.error).toBe('EMAIL_EXISTS');
    });
    
    it('should fail with weak password', async () => {
      const dto = {
        email: 'test@example.com',
        password: 'weak',
        name: 'Test User'
      };
      
      const result = await service.createUser(dto);
      
      expect(result.success).toBe(false);
      expect(result.error).toContain('PASSWORD');
    });
  });
});
```

### Integration Test

```typescript
// users.integration.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import { app } from '../app';
import { testDb } from './test-database';

describe('POST /api/users', () => {
  beforeAll(async () => {
    await testDb.connect();
  });
  
  afterAll(async () => {
    await testDb.disconnect();
  });
  
  it('should create user with valid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'test@example.com',
        password: 'SecurePass123!',
        name: 'Test User'
      })
      .expect(201);
    
    expect(response.body.data.email).toBe('test@example.com');
  });
  
  it('should return 400 with invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'invalid-email',
        password: 'SecurePass123!',
        name: 'Test User'
      })
      .expect(400);
    
    expect(response.body.error.code).toBe('VALIDATION_ERROR');
  });
  
  it('should return 409 with duplicate email', async () => {
    // Create first user
    await request(app)
      .post('/api/users')
      .send({
        email: 'duplicate@example.com',
        password: 'SecurePass123!',
        name: 'First User'
      });
    
    // Try to create duplicate
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'duplicate@example.com',
        password: 'SecurePass123!',
        name: 'Second User'
      })
      .expect(409);
    
    expect(response.body.error.code).toBe('EMAIL_EXISTS');
  });
});
```

### E2E Test

```typescript
// login.e2e.test.ts
import { test, expect } from '@playwright/test';

test.describe('Login Flow', () => {
  test('should login successfully with valid credentials', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.click('[type="submit"]');
    
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('.user-name')).toHaveText('Test User');
  });
  
  test('should show error with invalid credentials', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('[name="email"]', 'wrong@example.com');
    await page.fill('[name="password"]', 'WrongPass');
    await page.click('[type="submit"]');
    
    await expect(page.locator('.error-message')).toContainText('Invalid credentials');
  });
});
```

## Mock Patterns

```typescript
// Mock function
const mockFn = vi.fn();
mockFn.mockReturnValue('value');
mockFn.mockResolvedValue({ id: '1' });
mockFn.mockImplementation((input) => input * 2);

// Mock module
vi.mock('./userRepository', () => ({
  UserRepository: {
    findByEmail: vi.fn()
  }
}));

// Mock class
class MockUserRepository {
  findByEmail = vi.fn();
  create = vi.fn();
}
```

## Coverage

```
┌────────────────────────────────────────────────────────────┐
│ Coverage Requirements                                      │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Overall: > 80%                                          │
│  Business logic: 100%                                    │
│  Error paths: > 80%                                      │
│  Happy path: 100%                                        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Post-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ C.1: Test Quality                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ All tests pass                                           │
│ □ No flaky tests                                          │
│ □ Clear test names                                        │
│ □ Single assertion per test (when possible)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.2: Coverage                                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Unit tests: > 80%                                       │
│ □ Integration tests: > 50%                               │
│ □ Critical paths covered                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Output

```
✅ Testing Complete
├── Unit tests (80%)
├── Integration tests (15%)
├── E2E tests (5%)
└── Coverage report
```
