# NestJS Checklist - Danh Sách Kiểm Tra

## Mục lục
1. [Project Setup](#1-project-setup)
2. [Modules](#2-modules)
3. [Controllers](#3-controllers)
4. [Services](#4-services)
5. [Database](#5-database)
6. [Security](#6-security)
7. [Testing](#7-testing)
8. [Deployment](#8-deployment)

---

## 1. Project Setup

### 1.1 Initial Configuration

- [ ] Sử dụng NestJS CLI để tạo project
- [ ] Cấu hình TypeScript (strict mode)
- [ ] Cài đặt ESLint và Prettier
- [ ] Cấu hình path aliases (@/)
- [ ] Cài đặt TypeORM hoặc Prisma

### 1.2 Dependencies

- [ ] @nestjs/typeorm (TypeORM)
- [ ] @nestjs/config (Configuration)
- [ ] @nestjs/jwt (JWT)
- [ ] @nestjs/passport (Authentication)
- [ ] class-validator & class-transformer

### 1.3 Structure

- [ ] Feature-based module structure
- [ ] Shared module for common code
- [ ] Clean separation of concerns

---

## 2. Modules

### 2.1 Module Organization

- [ ] One module per feature
- [ ] Shared module for common services
- [ ] No circular dependencies
- [ ] Clear module exports

### 2.2 Module Configuration

- [ ] TypeORM configured per module
- [ ] Async configuration for external services
- [ ] Proper imports/exports

---

## 3. Controllers

### 3.1 Controller Structure

- [ ] Thin controllers (delegate to services)
- [ ] Proper HTTP status codes
- [ ] Async handlers for async operations
- [ ] Proper error handling

### 3.2 Routing

- [ ] RESTful naming conventions
- [ ] Proper HTTP methods
- [ ] Route parameters with validation
- [ ] Query parameters with type casting

### 3.3 DTOs

- [ ] DTOs for all inputs
- [ ] Validation decorators
- [ ] Response transformation
- [ ] Type safety

---

## 4. Services

### 4.1 Service Design

- [ ] Business logic in services
- [ ] Single responsibility
- [ ] Async/await throughout
- [ ] Proper error handling

### 4.2 Repository Pattern

- [ ] Data access in repositories
- [ ] TypeORM/Prisma queries in repository layer
- [ ] Service uses repository

### 4.3 Error Handling

- [ ] Throw appropriate NestJS exceptions
- [ ] NotFoundException for missing resources
- [ ] ConflictException for duplicates
- [ ] InternalServerErrorException for failures

---

## 5. Database

### 5.1 Entity Design

- [ ] Proper column types
- [ ] Indexes for frequently queried columns
- [ ] Relationships properly defined
- [ ] Soft deletes if needed

### 5.2 Queries

- [ ] Use query builder for complex queries
- [ ] Transactions for multi-step operations
- [ ] Pagination for large datasets
- [ ] Eager loading carefully used

### 5.3 Migrations

- [ ] Track migrations
- [ ] Seed data for development
- [ ] Production migration strategy

---

## 6. Security

### 6.1 Authentication

- [ ] JWT configured
- [ ] Passport strategies
- [ ] Token refresh mechanism
- [ ] Secure password hashing

### 6.2 Authorization

- [ ] Guards implemented
- [ ] Roles-based access control
- [ ] Resource ownership checks

### 6.3 Input Validation

- [ ] ValidationPipe enabled globally
- [ ] DTOs with validation decorators
- [ ] Whitelist enabled
- [ ] Forbid non-whitelisted properties

### 6.4 Rate Limiting

- [ ] @nestjs/throttler configured
- [ ] Public endpoints rate limited
- [ ] Auth endpoints more restricted

---

## 7. Testing

### 7.1 Unit Tests

- [ ] Test services
- [ ] Test repositories
- [ ] Mock dependencies
- [ ] High coverage for critical paths

### 7.2 Integration Tests

- [ ] Test controllers
- [ ] Test module integration
- [ ] Test with in-memory database
- [ ] Test error scenarios

### 7.3 E2E Tests

- [ ] Test user flows
- [ ] Test auth flows
- [ ] Test CRUD operations

---

## 8. Deployment

### 8.1 Build Configuration

- [ ] Production build optimized
- [ ] Environment variables configured
- [ ] Source maps disabled in production

### 8.2 Docker

- [ ] Dockerfile created
- [ ] Multi-stage build
- [ ] Health check endpoint
- [ ] Non-root user

### 8.3 CI/CD

- [ ] Build pipeline
- [ ] Test execution
- [ ] Lint checks
- [ ] Deployment automation

---

## Quick Reference

### Controller Checklist
```
[ ] Thin controller
[ ] DTOs for input
[ ] Async handlers
[ ] Proper HTTP status codes
```

### Service Checklist
```
[ ] Business logic
[ ] Async/await
[ ] Error handling
[ ] Repository pattern
```

### Security Checklist
```
[ ] JWT auth
[ ] Guards
[ ] Validation
[ ] Rate limiting
```

---

## Liên kết liên quan
- [NestJS Glossary](./glossary.md)
- [NestJS Architecture](./architecture.md)
- [NestJS Best Practices](./best-practice.md)
- [NestJS Anti-Patterns](./anti-pattern.md)
- [NestJS FAQ](./faq.md)
- [NestJS Decision Tree](./decision-tree.md)
