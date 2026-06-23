# ASP.NET Core Decision Tree - Cây Quyết Định

## Mục lục
1. [Service Lifetime Decision](#1-service-lifetime-decision)
2. [Controller Decision](#2-controller-decision)
3. [Data Access Decision](#3-data-access-decision)
4. [Security Decision](#4-security-decision)

---

## 1. Service Lifetime Decision

```
Bạn cần đăng ký một service?
│
├── Service cần one instance cho toàn bộ app?
│   ├── YES ────────────────────────────────→ → → Singleton
│   │                                              └── AddSingleton<IService, Service>()
│   │                                              └── Use for: Configuration, logging, caches
│   │
│   └── NO
│       │
│       └── Service cần one instance per HTTP request?
│           ├── YES ────────────────────────────────→ → → Scoped
│           │                                              └── AddScoped<IService, Service>()
│           │                                              └── Use for: DbContext, repositories
│           │
│           └── NO (new instance mỗi lần được inject)
│               └── → → → Transient
│                      └── AddTransient<IService, Service>()
│                      └── Use for: Lightweight, stateless services
```

---

## 2. Controller Decision

```
Bạn cần xử lý HTTP request?
│
├── Request là API endpoint?
│   ├── YES
│   │   └── → → → Use [ApiController] + ControllerBase
│   │          └── Returns ActionResult<T>
│   │
│   └── NO
│       └── Request là MVC page?
│           └── → → → Use Controller + IActionResult
│                  └── Returns View(), Redirect(), etc.
│
└── Logic phức tạp?
    ├── YES ────────────────────────────────→ → → Delegate to Service
    │                                              └── IUserService in constructor
    │
    └── NO
        └── → → → Simple CRUD
               └── Can use in controller directly
```

---

## 3. Data Access Decision

```
Bạn cần truy xuất database?
│
├── Sử dụng ORM?
│   ├── YES
│   │   └── Entity Framework Core
│   │       └── → → → Use DbContext + DbSet
│   │              └── Include(), AsNoTracking() for reads
│   │
│   └── NO
│       └── Raw SQL?
│           ├── YES
│           │   └── → → → Use FromSqlRaw or ExecuteSqlRaw
│           │          └── Parameterized queries only!
│           │
│           └── NO
│               └── → → → Consider EF Core
│
└── Query type?
    ├── Read-only, no tracking?
    │   └── → → → AsNoTracking()
    │
    ├── With relationships?
    │   └── → → → Include() + ThenInclude()
    │
    ├── Complex projection?
    │   └── → → → Select() with DTO
    │
    └── Large dataset?
        └── → → → Pagination + Skip/Take
```

---

## 4. Security Decision

```
Bạn cần bảo mật endpoint?
│
├── Cần authentication?
│   ├── YES
│   │   └── → → → Configure JWT Bearer
│   │          └── [Authorize] attribute
│   │
│   └── NO
│       └── → → → Public endpoint
│
└── Cần authorization?
    ├── YES
    │   └── Role-based?
    │       ├── YES ────────────────────────────→ → → RequireRole("Admin")
    │       │
    │       └── NO
    │           └── Policy-based?
    │               ├── YES ────────────────────────────→ → → Custom policy
    │               │                                      └── IAuthorizationHandler
    │               │
    │               └── NO ────────────────────────────→ → → Simple check
    │                      └── [Authorize(Policy = "...")]
    │
    └── NO
        └── → → → No additional authorization needed
```

---

## Quick Reference

### Service Lifetime
```
One app-wide instance → Singleton
One per request → Scoped
New each time → Transient
```

### Controller
```
API → [ApiController] ControllerBase
MVC → Controller
Logic → Service layer
```

### Data Access
```
EF Core → DbContext + DbSet
Read-only → AsNoTracking()
Relationships → Include()
```

### Security
```
Auth → JWT Bearer
Roles → RequireRole()
Policies → Custom handler
```

---

## Liên kết liên quan
- [ASP.NET Core Glossary](./glossary.md)
- [ASP.NET Core Architecture](./architecture.md)
- [ASP.NET Core Best Practices](./best-practice.md)
- [ASP.NET Core Anti-Patterns](./anti-pattern.md)
- [ASP.NET Core Checklist](./checklist.md)
- [ASP.NET Core FAQ](./faq.md)
