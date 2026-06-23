# Laravel Glossary - Từ Điển Thuật Ngữ Laravel

## Giới thiệu

Tài liệu này cung cấp các thuật ngữ chuyên ngành Laravel framework.

## Các thuật ngữ cơ bản

### 1. Eloquent ORM

Eloquent là ORM (Object-Relational Mapping) của Laravel, cung cấp beautiful, simple ActiveRecord implementation để làm việc với database. Mỗi database table có một Model tương ứng. Eloquent supports relationships, mutators, accessors, scopes, và events.

Model được tạo với Artisan command: `php artisan make:model Post`. Relationships được định nghĩa như methods trong Model: `return $this->hasMany(Post::class);`.

### 2. Blade Templates

Blade là templating engine của Laravel, cung cấp clean syntax cho displaying data và building layouts. Blade files được stored trong `resources/views`. Features: template inheritance, sections, components, slots, directives.

```blade
@extends('layouts.app')
@section('content')
  <h1>{{ $title }}</h1>
@endsection
```

### 3. Artisan CLI

Artisan là command-line interface của Laravel. Common commands: `make:controller`, `make:model`, `make:migration`, `migrate`, `route:list`. Custom commands có thể được tạo với `make:command`.

### 4. Middleware

Middleware cung cấp mechanism để filter HTTP requests. Built-in middleware: Auth, CORS, CSRF protection. Custom middleware có thể được tạo và registered trong Kernel.

### 5. Eloquent Relationships

Eloquent supports các relationship types: `hasOne`, `hasMany`, `belongsTo`, `belongsToMany`, `morphOne`, `morphMany`, `morphToMany`. Relationships được defined như methods trong Model.

### 6. Routes

Routes được định nghĩa trong `routes/web.php` hoặc `routes/api.php`. HTTP verbs: GET, POST, PUT, DELETE, PATCH. Route parameters, named routes, route groups.

```php
Route::get('/users/{id}', [UserController::class, 'show'])->name('users.show');
```

### 7. Controllers

Controllers nhóm request handling logic. Generated với `php artisan make:controller`. Resource controllers cung cấp CRUD methods.

### 8. Migrations

Migrations là version control cho database schema. Tạo với `php artisan make:migration`. Migrate với `php artisan migrate`. Rollback với `php artisan migrate:rollback`.

### 9. Factories và Seeders

Factories tạo fake data cho testing. Seeders populate database với initial data. Sử dụng Faker library.

### 10. Service Container

Service Container là powerful dependency injection container. Automatic resolution, binding, và resolution of dependencies.

### 11. Service Providers

Service Providers bootstrap services, bindings, và event listeners. Registered trong `config/app.php`.

### 12. Events và Listeners

Events cung cấp observer pattern implementation. Listeners respond to events. Dispatching có thể be synchronous hoặc queued.

### 13. Queues

Queues defer processing của time-consuming tasks. Jobs được tạo với `php artisan make:job`. Queued với Redis, Beanstalkd, hoặc database.

### 14. Broadcasting

Broadcasting cho phép real-time events được pushed đến clients. Pusher và Laravel Echo được sử dụng phổ biến.

### 15. API Resources

API Resources transform models thành JSON. Resource classes được tạo với `php artisan make:resource`.

### 16. Validation

Laravel's validation system cung cấp powerful rules. Validate requests trong controllers hoặc Form Request classes.

### 17. Authentication

Laravel Breeze, Fortify, và Sanctum cung cấp authentication scaffolding. Scaffolding đầy đủ với `php artisan ui:bootstrap --auth`.

### 18. Laravel Sanctum

Sanctum cung cấp lightweight API token authentication. Perfect cho SPAs và mobile apps.

### 19. Policies

Policies authorize actions against models. Registered trong AuthServiceProvider.

### 20. Gates

Gates provide simple authorization via Closure definitions. Alternative to Policies.

## Kết luận

Từ điển này cung cấp nền tảng về Laravel concepts.
