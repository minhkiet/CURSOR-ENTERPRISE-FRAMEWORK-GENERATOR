# Laravel Architecture - Kiến Trúc Laravel

## Tổng quan

Laravel là PHP framework cho web application development. Kiến trúc MVC với service container, service providers, và facades.

## Kiến trúc chi tiết

### 1. Directory Structure

```
├── app/
│   ├── Console/          # Artisan commands
│   ├── Exceptions/       # Exception handling
│   ├── Http/
│   │   ├── Controllers/  # Controllers
│   │   ├── Middleware/   # Middleware
│   │   └── Requests/     # Form requests
│   ├── Models/           # Eloquent models
│   ├── Providers/        # Service providers
│   └── Services/         # Business logic
├── bootstrap/            # App bootstrap
├── config/               # Configuration
├── database/
│   ├── factories/        # Model factories
│   ├── migrations/       # Database migrations
│   └── seeders/          # Database seeders
├── resources/
│   ├── js/               # JavaScript
│   ├── css/              # Styles
│   └── views/            # Blade templates
├── routes/               # Routes
└── tests/                # Tests
```

### 2. MVC Architecture

**Model**: Eloquent ORM, database interactions.
**View**: Blade templates.
**Controller**: Request handling, business logic coordination.

### 3. Service Layer

Business logic nên được tách vào Services. Controllers chỉ handle request/response.

### 4. Database Design

Eloquent models với relationships. Migrations cho schema versioning. Factories cho testing data.

### 5. API Design

API routes trong routes/api.php. API Resources cho JSON transformation. Laravel Sanctum cho authentication.

## Kết luận

Laravel cung cấp complete PHP solution cho web development.
