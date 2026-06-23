# Laravel Checklist - Danh Sách Kiểm Tra

## Mục lục
1. [Project Setup](#1-project-setup)
2. [Controllers](#2-controllers)
3. [Models](#3-models)
4. [Database](#4-database)
5. [Security](#5-security)
6. [API](#6-api)
7. [Performance](#7-performance)
8. [Testing](#8-testing)
9. [Deployment](#9-deployment)

---

## 1. Project Setup

### 1.1 Initial Configuration

- [ ] Cài đặt Laravel mới với Composer
- [ ] Cấu hình .env file
- [ ] Cài đặt database connection
- [ ] Cài đặt mail driver
- [ ] Cài đặt cache driver
- [ ] Cài đặt queue driver

### 1.2 Security Configuration

- [ ] Đặt APP_KEY với php artisan key:generate
- [ ] Cấu hình session driver
- [ ] Cấu hình CSRF protection
- [ ] Cài đặt SSL/HTTPS
- [ ] Cấu hình CORS

### 1.3 Development Tools

- [ ] Cài đặt Laravel Debugbar (dev)
- [ ] Cài đặt IDE helper
- [ ] Cấu hình Laravel Pint (code style)
- [ ] Cài đặt Pest/ PHPUnit

---

## 2. Controllers

### 2.1 Controller Structure

- [ ] Keep controllers thin
- [ ] Use Form Requests cho validation
- [ ] Use Service layer cho business logic
- [ ] Return proper HTTP status codes
- [ ] Use API Resources cho API responses

### 2.2 Validation

- [ ] Create Form Request classes
- [ ] Define validation rules
- [ ] Add custom error messages
- [ ] Implement authorization logic
- [ ] Sanitize input data

### 2.3 Error Handling

- [ ] Handle exceptions properly
- [ ] Return consistent error responses
- [ ] Log errors appropriately
- [ ] Use try-catch when needed
- [ ] Return 404 for not found resources

---

## 3. Models

### 3.1 Model Configuration

- [ ] Define $fillable hoặc $guarded
- [ ] Define $hidden fields
- [ ] Define $casts
- [ ] Define $dates
- [ ] Define $table name if custom

### 3.2 Relationships

- [ ] Define all relationships
- [ ] Use proper relationship types
- [ ] Add inverse relationships
- [ ] Use pivot tables cho many-to-many
- [ ] Add timestamps to pivot tables

### 3.3 Model Features

- [ ] Use scopes for common queries
- [ ] Use accessors and mutators
- [ ] Use model observers if needed
- [ ] Implement soft deletes if needed
- [ ] Use UUIDs if needed

---

## 4. Database

### 4.1 Migrations

- [ ] Create migrations for all tables
- [ ] Define proper column types
- [ ] Add necessary indexes
- [ ] Add foreign key constraints
- [ ] Define up() và down() methods
- [ ] Test migrations both directions

### 4.2 Seeding

- [ ] Create factories for models
- [ ] Create seeders for test data
- [ ] Use factories in tests
- [ ] Don't seed production database

### 4.3 Query Optimization

- [ ] Use eager loading (with)
- [ ] Use select() for specific columns
- [ ] Add indexes for frequent queries
- [ ] Use query scopes
- [ ] Use pagination for large datasets

---

## 5. Security

### 5.1 Authentication

- [ ] Use Laravel's built-in auth
- [ ] Hash passwords with bcrypt()
- [ ] Use Auth::attempt() properly
- [ ] Implement proper logout
- [ ] Use remember me functionality
- [ ] Handle failed authentication

### 5.2 Authorization

- [ ] Use Policies for authorization
- [ ] Use Gates for simple checks
- [ ] Check authorization in controllers
- [ ] Use @can directive in Blade
- [ ] Don't trust user input for authorization

### 5.3 Input Validation

- [ ] Validate all user input
- [ ] Sanitize input data
- [ ] Use type casting
- [ ] Validate file uploads
- [ ] Limit request sizes
- [ ] Use CSRF protection

### 5.4 SQL Injection Prevention

- [ ] Use Eloquent ORM
- [ ] Use query builder
- [ ] Parameter binding for raw queries
- [ ] Don't use string interpolation in queries
- [ ] Validate input types

---

## 6. API

### 6.1 API Structure

- [ ] Use API routes (api.php)
- [ ] Version your API
- [ ] Use API Resources
- [ ] Return consistent response format
- [ ] Use proper HTTP status codes
- [ ] Document your API

### 6.2 Authentication

- [ ] Use Laravel Sanctum hoặc Passport
- [ ] Implement token authentication
- [ ] Rate limit API endpoints
- [ ] Handle token expiration
- [ ] Implement refresh tokens

### 6.3 API Best Practices

- [ ] Paginate list endpoints
- [ ] Filter and sort endpoints
- [ ] Validate request data
- [ ] Return appropriate errors
- [ ] Use cache for expensive operations
- [ ] Optimize database queries

---

## 7. Performance

### 7.1 Caching

- [ ] Cache configuration
- [ ] Cache routes (production)
- [ ] Cache views (production)
- [ ] Cache expensive queries
- [ ] Use cache tags if supported
- [ ] Implement cache invalidation

### 7.2 Queue

- [ ] Use queues for long tasks
- [ ] Configure queue driver
- [ ] Create job classes
- [ ] Handle job failures
- [ ] Use job batching if needed
- [ ] Monitor queue workers

### 7.3 Database Optimization

- [ ] Add database indexes
- [ ] Use query optimization
- [ ] Use pagination
- [ ] Use chunking for large datasets
- [ ] Use cursor() for memory efficiency
- [ ] Monitor slow queries

---

## 8. Testing

### 8.1 Unit Tests

- [ ] Test models
- [ ] Test services
- [ ] Test utilities
- [ ] Test business logic
- [ ] Use factories for test data
- [ ] Mock external services

### 8.2 Feature Tests

- [ ] Test HTTP endpoints
- [ ] Test authentication
- [ ] Test authorization
- [ ] Test validation
- [ ] Test responses
- [ ] Use RefreshDatabase trait

### 8.3 Test Coverage

- [ ] Test critical paths
- [ ] Test edge cases
- [ ] Test error handling
- [ ] Test authorization
- [ ] Target >80% coverage

---

## 9. Deployment

### 9.1 Pre-Deployment

- [ ] Run all tests
- [ ] Clear and optimize caches
- [ ] Check environment configuration
- [ ] Verify storage permissions
- [ ] Check queue configuration
- [ ] Review error handling

### 9.2 Server Configuration

- [ ] Point document root to public/
- [ ] Configure web server (Nginx/Apache)
- [ ] Enable HTTPS
- [ ] Configure queue workers
- [ ] Set up scheduler
- [ ] Configure logging

### 9.3 Production Checks

- [ ] APP_ENV=production
- [ ] APP_DEBUG=false
- [ ] APP_KEY set
- [ ] Cache cleared
- [ ] Routes cached
- [ ] Config cached

---

## Quick Reference

### Controller Checklist
```
[ ] Thin controller (delegates to services)
[ ] Form Request for validation
[ ] Proper HTTP status codes
[ ] API Resources for API responses
[ ] Error handling
```

### Model Checklist
```
[ ] $fillable/$guarded defined
[ ] Relationships defined
[ ] Scopes for common queries
[ ] $casts for type conversion
[ ] Soft deletes if needed
```

### Security Checklist
```
[ ] Passwords hashed
[ ] CSRF protection
[ ] Authorization checks
[ ] Input validation
[ ] SQL injection prevention
[ ] Rate limiting
```

---

## Liên kết liên quan
- [Laravel Glossary](./glossary.md)
- [Laravel Architecture](./architecture.md)
- [Laravel Best Practices](./best-practice.md)
- [Laravel Anti-Patterns](./anti-pattern.md)
- [Laravel FAQ](./faq.md)
- [Laravel Decision Tree](./decision-tree.md)
