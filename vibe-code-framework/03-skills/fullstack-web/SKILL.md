# Fullstack Web Skill

> **Version:** 1.0.0 | **Category:** Development | **Triggers:** fullstack, web app, frontend backend, api frontend

---

## Goal

Build full-stack web application hoàn chỉnh:
- ASP.NET Core Web API backend
- React/TypeScript frontend
- Database integration
- REST API design
- JWT authentication
- End-to-end data flow

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18+ / TypeScript |
| Backend | ASP.NET Core 8+ |
| Database | PostgreSQL / MySQL |
| ORM | Dapper (high performance) |
| Auth | JWT + Refresh Token |
| API | REST |

## Trigger Conditions

- User cần tạo full-stack web app
- User cần implement API + frontend
- User cần CRUD với database

## Pre-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ P.1: Requirements                                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Feature requirements documented?                         │
│ □ API contracts defined?                                  │
│ □ Database schema designed?                               │
│ □ User flows mapped?                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ P.2: Environment                                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Backend scaffolded?                                     │
│ □ Frontend scaffolded?                                    │
| □ Database connection ready?                              │
│ □ JWT configured?                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Process Steps

### Step 1: Design API Contract

```
┌────────────────────────────────────────────────────────────┐
│ API Contract Design                                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  POST   /api/users              → Create user           │
│  GET    /api/users/:id          → Get user              │
│  GET    /api/users              → List users            │
│  PUT    /api/users/:id          → Update user           │
│  DELETE /api/users/:id          → Delete user           │
│                                                            │
│  Response Format:                                         │
│  {                                                       │
│    "data": { ... },                                     │
│    "meta": { "page": 1, "total": 100 }                │
│  }                                                       │
│                                                            │
│  Error Format:                                          │
│  {                                                       │
│    "error": { "code": "...", "message": "..." }        │
│  }                                                       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 2: Database Schema

```
┌────────────────────────────────────────────────────────────┐
│ Database Design                                           │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Create migration                                    │
│     migrations/20260115_create_users.sql                 │
│                                                            │
│  2. Define entities                                      │
│     - Users (id, email, password_hash, name, created_at) │
│     - [Other entities]                                  │
│                                                            │
│  3. Add indexes                                          │
│     - idx_users_email ON users(email) UNIQUE            │
│     - idx_users_status ON users(status)                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 3: Backend Implementation

#### Domain Layer

```csharp
// Domain/Entities/User.cs
public class User
{
    public Guid Id { get; private set; }
    public string Email { get; private set; }
    public string PasswordHash { get; private set; }
    public string Name { get; private set; }
    public DateTime CreatedAt { get; private set; }
    
    public static User Create(string email, string passwordHash, string name)
    {
        // Validation
        // Domain rules
        return new User { ... };
    }
}
```

#### Repository Interface

```csharp
// Domain/Interfaces/IUserRepository.cs
public interface IUserRepository
{
    Task<User?> GetByIdAsync(Guid id);
    Task<User?> GetByEmailAsync(string email);
    Task<IEnumerable<User>> GetAllAsync(int page, int pageSize);
    Task<User> CreateAsync(User user);
    Task UpdateAsync(User user);
    Task DeleteAsync(Guid id);
}
```

#### DTOs

```csharp
// Application/DTOs/UserDTOs.cs
public record CreateUserDto(
    string Email,
    string Password,
    string Name
);

public record UserDto(
    Guid Id,
    string Email,
    string Name,
    DateTime CreatedAt
);
```

#### Use Case

```csharp
// Application/UseCases/CreateUserUseCase.cs
public class CreateUserUseCase
{
    private readonly IUserRepository _repository;
    private readonly IEmailService _emailService;
    
    public async Task<Result<User>> ExecuteAsync(CreateUserDto dto)
    {
        // 1. Validate
        // 2. Check duplicates
        // 3. Hash password
        // 4. Create user
        // 5. Persist
        // 6. Send notification
        // 7. Return result
    }
}
```

#### Controller

```csharp
// Presentation/Controllers/UsersController.cs
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly CreateUserUseCase _createUser;
    
    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreateUserDto dto)
    {
        var result = await _createUser.ExecuteAsync(dto);
        
        if (!result.Success)
            return BadRequest(new { error = result.Error });
            
        return Created($"/api/users/{result.Data.Id}", 
            new { data = UserDto.FromEntity(result.Data) });
    }
}
```

### Step 4: Frontend Implementation

#### API Client

```typescript
// services/api.ts
const api = axios.create({
  baseURL: '/api',
  withCredentials: true,
});

api.interceptors.response.use(
  response => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Refresh token logic
    }
    return Promise.reject(error);
  }
);

export const usersApi = {
  getAll: (params?: ListParams) => 
    api.get<{ data: User[]; meta: Meta }>('/users', { params }),
    
  getById: (id: string) => 
    api.get<User>(`/users/${id}`),
    
  create: (data: CreateUserDto) => 
    api.post<User>('/users', data),
    
  update: (id: string, data: UpdateUserDto) => 
    api.put<User>(`/users/${id}`, data),
    
  delete: (id: string) => 
    api.delete(`/users/${id}`),
};
```

#### Type Definitions

```typescript
// types/user.ts
export interface User {
  id: string;
  email: string;
  name: string;
  createdAt: string;
}

export interface CreateUserDto {
  email: string;
  password: string;
  name: string;
}

export interface UpdateUserDto {
  email?: string;
  name?: string;
}
```

#### React Component

```tsx
// components/UserList.tsx
import { useState, useEffect } from 'react';
import { usersApi } from '@/services/api';

export function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    loadUsers();
  }, []);
  
  async function loadUsers() {
    try {
      setLoading(true);
      const response = await usersApi.getAll({ page: 1, limit: 20 });
      setUsers(response.data.data);
    } catch (e) {
      setError('Failed to load users');
    } finally {
      setLoading(false);
    }
  }
  
  if (loading) return <Spinner />;
  if (error) return <ErrorMessage message={error} />;
  
  return (
    <div className="user-list">
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}
```

### Step 5: Authentication

```csharp
// Infrastructure/Services/JwtService.cs
public class JwtService
{
    public string GenerateToken(User user, TimeSpan expiry)
    {
        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
            new Claim(JwtRegisteredClaimNames.Email, user.Email),
            new Claim(ClaimTypes.Role, user.Role),
        };
        
        var key = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(_config.JwtSecret));
        var credentials = new SigningCredentials(
            key, SecurityAlgorithms.HmacSha256);
            
        return new JwtSecurityToken(
            issuer: _config.Issuer,
            audience: _config.Audience,
            claims: claims,
            expires: DateTime.UtcNow.Add(expiry),
            signingCredentials: credentials
        ).RawToken;
    }
}
```

### Step 6: Testing

```typescript
// tests/unit/CreateUserUseCase.test.ts
describe('CreateUserUseCase', () => {
  const mockRepository = {
    getByEmail: vi.fn(),
    create: vi.fn(),
  };
  
  const useCase = new CreateUserUseCase(mockRepository);
  
  it('should create user with valid data', async () => {
    const dto = { email: 'test@test.com', password: 'Pass123!', name: 'Test' };
    mockRepository.getByEmail.mockResolvedValue(null);
    mockRepository.create.mockResolvedValue({ id: '1', ...dto });
    
    const result = await useCase.execute(dto);
    
    expect(result.success).toBe(true);
    expect(result.data?.email).toBe(dto.email);
  });
});
```

## Post-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ C.1: End-to-End Flow                                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ UI → API → Controller → UseCase → Repository → DB       │
│ □ Response → State → UI                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.2: Security                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ JWT authentication works?                                │
│ □ Input validation on both layers?                        │
│ □ SQL injection prevented?                                │
│ □ No sensitive data exposed?                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.3: Quality                                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Backend tests passing?                                  │
│ □ Frontend tests passing?                                 │
| □ Integration tests passing?                              │
│ □ No console errors?                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## End-to-End Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ End-to-End Data Flow                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────┐                                             │
│   │   UI    │  ← User interaction                       │
│   └────┬────┘                                             │
│        │ React state update                               │
│        ↓                                                   │
│   ┌─────────┐                                             │
│   │  API    │  ← HTTP request                           │
│   │ Client  │                                             │
│   └────┬────┘                                             │
│        │ HTTP POST /api/users                              │
│        ↓                                                   │
│   ┌─────────┐                                             │
│   │Controller│  ← Route matching                         │
│   └────┬────┘                                             │
│        │ Use case call                                    │
│        ↓                                                   │
│   ┌─────────┐                                             │
│   │ UseCase │  ← Business logic                          │
│   └────┬────┘                                             │
│        │ Repository call                                   │
│        ↓                                                   │
│   ┌─────────┐                                             │
│   │Repository│  ← SQL query                               │
│   └────┬────┘                                             │
│        │ SQL INSERT                                        │
│        ↓                                                   │
│   ┌─────────┐                                             │
│   │   DB    │  ← PostgreSQL / MySQL                      │
│   └─────────┘                                             │
│                                                             │
│   Response flows back: DB → Repository → UseCase →        │
│   Controller → HTTP Response → API Client → React State    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Output

```
✅ Fullstack Web App Complete
├── Backend (ASP.NET Core)
│   ├── Domain (Entities, Interfaces)
│   ├── Application (Use Cases, DTOs)
│   ├── Infrastructure (Repositories, Services)
│   └── Presentation (Controllers)
├── Frontend (React + TypeScript)
│   ├── Components
│   ├── Services (API client)
│   ├── Types
│   └── Hooks
├── Tests
│   ├── Unit tests
│   └── Integration tests
└── Documentation
```
