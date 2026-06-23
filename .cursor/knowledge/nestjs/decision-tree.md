# NestJS Decision Tree - Cây Quyết Định

## Mục lục
1. [Module Decision](#1-module-decision)
2. [Service Decision](#2-service-decision)
3. [Controller Decision](#3-controller-decision)

---

## 1. Module Decision

```
Bạn cần tạo một module?
│
├── Module là root/main module?
│   ├── YES ─────────────────────────────────→ → → AppModule
│   │                                              └── imports tất cả feature modules
│   │
│   └── NO
│       │
│       └── Module là feature/domain?
│           ├── YES ────────────────────────────→ → → Feature Module
│           │                                              └── Module riêng cho feature
│           │
│           └── Module chứa shared functionality?
│               ├── YES ────────────────────────────→ → → Shared Module
│               │                                              └── exports shared services
│               │
│               └── Module cho external service?
│                   ├── YES ────────────────────────────→ → → External Module
│                   │                                              └── Encapsulates third-party integration
│                   │
│                   └── NO ────────────────────────────→ → → Feature Module
└── (End)
```

---

## 2. Service Decision

```
Bạn cần tạo một service?
│
├── Service chứa business logic?
│   ├── YES
│   │   └── Logic phức tạp?
│   │       ├── YES ────────────────────────────→ → → Service với repository
│   │       │                                              └── Use repository pattern
│   │       │
│   │       └── NO ────────────────────────────→ → → Simple service
│   │                                                              └── Direct data access
│   │
│   └── NO
│       └── Service chỉ encapsulate external service?
│           ├── YES ────────────────────────────→ → → Service wrapper
│           │                                              └── Proxy pattern
│           │
│           └── NO
│               └── Service cần application-wide?
│                   ├── YES ────────────────────────────→ → → Singleton service
│                   │                                              └── @Injectable() - default
│                   │
│                   └── NO ────────────────────────────→ → → Request-scoped service
│                                                              └── requestId injected
```

---

## 3. Controller Decision

```
Bạn cần xử lý HTTP request?
│
├── Request là CRUD operation?
│   ├── YES ────────────────────────────────────→ → → REST Controller
│   │                                              └── @Controller, @Get, @Post, etc.
│   │
│   └── NO
│       │
│       └── Request là GraphQL?
│           ├── YES ────────────────────────────→ → → GraphQL Resolver
│           │                                              └── @Resolver, @Query, @Mutation
│           │
│       └── Request là WebSocket?
│           ├── YES ────────────────────────────→ → → WebSocket Gateway
│           │                                              └── @WebSocketGateway
│           │
│       └── Request là gRPC?
│           ├── YES ────────────────────────────→ → → gRPC Controller
│           │                                              └── @GrpcMethod
│           │
│       └── Request là microservice?
│           ├── YES ────────────────────────────→ → → Microservice Controller
│           │                                              └── @Controller with transport
│           │
│       └── NO ──────────────────────────────────→ → → REST Controller
│
└── Logic nên ở đâu?
    ├── HTTP handling ────────────────────────────→ → → Controller
    │
    ├── Business logic ───────────────────────────→ → → Service
    │
    ├── Data access ───────────────────────────────→ → → Repository
    │
    └── Cross-cutting concerns ────────────────────→ → → Guard/Pipe/Interceptor
```

---

## Quick Reference

### Module
```
Feature → Feature Module
Shared code → Shared Module
External → External Module
Root → AppModule
```

### Service
```
Business logic → Service
Data access → Repository
Singleton → Default scope
```

### Controller
```
HTTP → Controller
GraphQL → Resolver
WebSocket → Gateway
gRPC → Controller
```

---

## Liên kết liên quan
- [NestJS Glossary](./glossary.md)
- [NestJS Architecture](./architecture.md)
- [NestJS Best Practices](./best-practice.md)
- [NestJS Anti-Patterns](./anti-pattern.md)
- [NestJS Checklist](./checklist.md)
- [NestJS FAQ](./faq.md)
