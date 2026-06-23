# Laravel Architecture - Kiến Trúc Chi Tiết

## Mục lục
1. [Tổng quan Kiến trúc](#1-tổng-quan-kiến-trúc)
2. [Request Lifecycle](#2-request-lifecycle)
3. [Directory Structure](#3-directory-structure)
4. [Service Providers](#4-service-providers)
5. [Database Architecture](#5-database-architecture)
6. [API Architecture](#6-api-architecture)

---

## 1. Tổng quan Kiến trúc

### 1.1 Laravel Architecture Overview

Laravel là một PHP framework được thiết kế với mô hình Model-View-Controller (MVC), nhưng mở rộng hơn thế với nhiều architectural patterns.

Core components:
- **Service Container**: Dependency injection container
- **Service Providers**: Bootstrap services
- **Routing**: URL mapping
- **Middleware**: Request/Response filters
- **Controllers**: Business logic
- **Models**: Database abstraction (Eloquent)
- **Views**: Template rendering (Blade)

### 1.2 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LARAVEL APPLICATION ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    HTTP REQUEST                               │   │
│  │                    (index.php)                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    HTTP KERNEL                               │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │   │
│  │  │Middleware│  │Middleware│  │Middleware│  │Middleware│        │   │
│  │  │    1    │→ │    2    │→ │    3    │→ │    N    │        │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                       ROUTER                                  │   │
│  │                                                             │   │
│  │  Route::get('/users', [UserController::class, 'index']);  │   │
│  │  Route::post('/users', [UserController::class, 'store']);  │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     CONTROLLER                               │   │
│  │                                                             │   │
│  │  UserController::index()                                    │   │
│  │      │                                                      │   │
│  │      ├── Validate Request                                   │   │
│  │      │                                                      │   │
│  │      ├── Business Logic                                     │   │
│  │      │                                                      │   │
│  │      └── Return Response                                    │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│          ┌───────────────────┼───────────────────┐                │
│          │                   │                   │                  │
│          ▼                   ▼                   ▼                   │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐          │
│  │   Model      │  │   Service    │  │   Repository  │          │
│  │  (Eloquent)  │  │   Layer     │  │   Layer       │          │
│  └───────────────┘  └───────────────┘  └───────────────┘          │
│          │                   │                   │                  │
│          └───────────────────┴───────────────────┘                │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   DATABASE (MySQL/PostgreSQL)               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Request Lifecycle

### 2.1 Detailed Lifecycle

```
┌─────────────────────────────────────────────────────────────────────┐
│                       REQUEST LIFECYCLE                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. Entry Point (public/index.php)                                  │
│     │                                                               │
│     ├── Load Composer autoloader                                     │
│     ├── Bootstrap Laravel application                                │
│     └── Create Application instance                                 │
│     │                                                               │
│     ▼                                                               │
│  2. HTTP Kernel (Illuminate\Foundation\Http\Kernel)                  │
│     │                                                               │
│     ├── Boot application                                            │
│     ├── Global middleware (Handle)                                  │
│     │   ├── VerifyCsrfToken                                        │
│     │   ├── ShareErrorsFromSession                                 │
│     │   └── ...                                                    │
│     │                                                               │
│     ▼                                                               │
│  3. Router                                                         │
│     │                                                               │
│     ├── Match URL to route                                          │
│     ├── Load route middleware                                       │
│     └── Prepare route handler                                       │
│     │                                                               │
│     ▼                                                               │
│  4. Middleware Stack                                                │
│     │                                                               │
│     │ Middleware 1 (before)                                        │
│     │     │                                                         │
│     │     ├── Middleware 2 (before)                               │
│     │     │     │                                                   │
│     │     │     ├── Controller/Action                             │
│     │     │     │                                                   │
│     │     │     └── Middleware 2 (after)                          │
│     │     │                                                         │
│     │     └── Middleware 1 (after)                                 │
│     │                                                               │
│     ▼                                                               │
│  5. Controller                                                      │
│     │                                                               │
│     ├── Validate input (Form Request)                               │
│     ├── Execute business logic                                      │
│     └── Return Response                                            │
│     │                                                               │
│     ▼                                                               │
│  6. Response                                                        │
│     │                                                               │
│     ├── Response middleware (after)                                 │
│     └── Send to client                                             │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Directory Structure

### 3.1 Standard Laravel Structure

```
project/
├── app/
│   ├── Console/
│   │   └── Commands/              # Artisan commands
│   │
│   ├── Events/                    # Event classes
│   │
│   ├── Exceptions/
│   │   └── Handler.php           # Exception handler
│   │
│   ├── Http/
│   │   ├── Controllers/
│   │   │   ├── Controller.php
│   │   │   └── Api/
│   │   │       └── UserController.php
│   │   │
│   │   ├── Middleware/
│   │   │   ├── Authenticate.php
│   │   │   ├── EnsureUserIsAdmin.php
│   │   │   └── VerifyCsrfToken.php
│   │   │
│   │   └── Requests/             # Form requests
│   │       ├── StoreUserRequest.php
│   │       └── UpdateUserRequest.php
│   │
│   ├── Listeners/               # Event listeners
│   │
│   ├── Mail/                    # Mailable classes
│   │   └── OrderConfirmation.php
│   │
│   ├── Models/
│   │   ├── User.php
│   │   ├── Post.php
│   │   └── Comment.php
│   │
│   ├── Notifications/           # Notification classes
│   │   └── OrderShipped.php
│   │
│   ├── Policies/                # Authorization policies
│   │   └── PostPolicy.php
│   │
│   ├── Providers/
│   │   ├── AppServiceProvider.php
│   │   ├── AuthServiceProvider.php
│   │   ├── EventServiceProvider.php
│   │   └── RouteServiceProvider.php
│   │
│   └── Services/                # Business logic services
│       ├── PaymentService.php
│       └── UserService.php
│
├── bootstrap/
│   ├── app.php                  # Application bootstrap
│   └── cache/
│
├── config/
│   ├── app.php
│   ├── auth.php
│   ├── cache.php
│   ├── database.php
│   ├── filesystems.php
│   ├── mail.php
│   ├── queue.php
│   └── services.php
│
├── database/
│   ├── factories/               # Model factories
│   │   └── UserFactory.php
│   │
│   ├── migrations/              # Database migrations
│   │   └── 2024_01_01_000001_create_users_table.php
│   │
│   └── seeders/                # Database seeders
│       └── DatabaseSeeder.php
│
├── public/
│   ├── index.php                # Entry point
│   ├── css/
│   ├── js/
│   └── .htaccess
│
├── resources/
│   ├── views/                  # Blade templates
│   │   ├── layouts/
│   │   │   └── app.blade.php
│   │   ├── users/
│   │   │   └── index.blade.php
│   │   └── welcome.blade.php
│   │
│   └── lang/
│       ├── en/
│       └── vi/
│
├── routes/
│   ├── api.php                  # API routes
│   ├── channels.php             # Broadcasting channels
│   ├── console.php              # Console routes
│   └── web.php                  # Web routes
│
├── storage/
│   ├── app/
│   ├── framework/
│   │   ├── cache/
│   │   ├── sessions/
│   │   └── views/
│   └── logs/
│
├── tests/
│   ├── Feature/
│   │   └── UserTest.php
│   │
│   └── Unit/
│       └── ExampleTest.php
│
├── .env
├── .env.example
├── artisan                     # CLI
├── composer.json
└── phpunit.xml
```

### 3.2 Domain-Driven Structure (Alternative)

```
project/
├── app/
│   ├── Modules/              # Feature modules
│   │   ├── User/
│   │   │   ├── Http/
│   │   │   │   ├── Controllers/
│   │   │   │   ├── Requests/
│   │   │   │   └── Resources/
│   │   │   ├── Models/
│   │   │   ├── Services/
│   │   │   ├── Policies/
│   │   │   └── Resources/
│   │   │
│   │   ├── Post/
│   │   │   └── ...
│   │   │
│   │   └── Order/
│   │       └── ...
│   │
│   ├── Core/                # Shared/core code
│   │   ├── Exceptions/
│   │   ├── Traits/
│   │   └── Support/
│   │
│   └── Shared/               # Shared components
│       ├── Controllers/
│       ├── Models/
│       └── Services/
```

---

## 4. Service Providers

### 4.1 Service Provider Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SERVICE PROVIDER ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Application                              │   │
│  │                                                             │   │
│  │  ┌──────────────────────────────────────────────────────┐  │   │
│  │  │         Service Providers (boot order)                  │  │   │
│  │  │                                                        │  │   │
│  │  │  1. Illuminate\Foundation\Providers\FoundationServiceProvider │   │
│  │  │  2. Illuminate\Routing\RoutingServiceProvider          │   │
│  │  │  3. Illuminate\Database\DatabaseServiceProvider        │   │
│  │  │  4. Illuminate\Encryption\EncryptionServiceProvider    │   │
│  │  │  5. Illuminate\Filesystem\FilesystemServiceProvider    │   │
│  │  │  ...                                                   │   │
│  │  │  N. App\Providers\AppServiceProvider                   │   │
│  │  │                                                        │  │   │
│  │  └──────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Service Container                         │   │
│  │                                                             │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │   │
│  │  │ Bindings    │  │ Singletons  │  │ Instances   │        │   │
│  │  │             │  │             │  │             │        │   │
│  │  │ Interface → │  │ One instance│  │ Pre-built  │        │   │
│  │  │ Concrete    │  │ always      │  │ instances   │        │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 4.2 Provider Example

```php
// app/Providers/PaymentServiceProvider.php
namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use App\Contracts\PaymentGatewayInterface;
use App\Services\StripePaymentGateway;
use App\Services\PayPalPaymentGateway;

class PaymentServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        // Bind interface to concrete implementation
        $this->app->bind(
            PaymentGatewayInterface::class,
            function ($app) {
                $driver = config('services.payment.driver');
                
                return match($driver) {
                    'stripe' => new StripePaymentGateway(
                        config('services.stripe.secret')
                    ),
                    'paypal' => new PayPalPaymentGateway(
                        config('services.paypal.client_id')
                    ),
                    default => throw new \Exception("Invalid payment driver: $driver"),
                };
            }
        );
        
        // Singleton for one instance
        $this->app->singleton(
            PaymentAnalytics::class,
            fn($app) => new PaymentAnalytics($app->make('log'))
        );
    }
    
    public function boot(): void
    {
        // Publish config
        $this->publishes([
            __DIR__.'/../../config/payment.php' => config_path('payment.php'),
        ]);
    }
}
```

---

## 5. Database Architecture

### 5.1 Eloquent Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ELOQUENT ORM ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Model Layer                               │   │
│  │                                                             │   │
│  │  App\Models\User                                             │   │
│  │  ├── $table = 'users'                                       │   │
│  │  ├── $fillable = ['name', 'email']                          │   │
│  │  ├── $hidden = ['password']                                 │   │
│  │  ├── $casts = ['email_verified_at' => 'datetime']          │   │
│  │  │                                                           │   │
│  │  └── Relationships                                          │   │
│  │      ├── posts() → hasMany(Post::class)                     │   │
│  │      └── roles() → belongsToMany(Role::class)               │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Query Builder                             │   │
│  │                                                             │   │
│  │  User::where('active', true)                               │   │
│  │      ->with(['posts' => fn($q) => $q->latest()])          │   │
│  │      ->orderBy('name')                                      │   │
│  │      ->paginate(15)                                         │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Database Connection                       │   │
│  │                                                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │   │
│  │  │  MySQL   │  │ Postgres │  │ SQLite   │  │   MSSQL  │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 5.2 Repository Pattern

```php
// App\Repositories\Contracts\UserRepositoryInterface
namespace App\Repositories\Contracts;

interface UserRepositoryInterface
{
    public function find(int $id): ?User;
    public function findByEmail(string $email): ?User;
    public function paginate(int $perPage = 15);
    public function create(array $data): User;
    public function update(User $user, array $data): User;
    public function delete(User $user): bool;
}

// App\Repositories\EloquentUserRepository
namespace App\Repositories;

use App\Models\User;
use App\Repositories\Contracts\UserRepositoryInterface;

class EloquentUserRepository implements UserRepositoryInterface
{
    public function find(int $id): ?User
    {
        return User::find($id);
    }
    
    public function findByEmail(string $email): ?User
    {
        return User::where('email', $email)->first();
    }
    
    public function paginate(int $perPage = 15)
    {
        return User::paginate($perPage);
    }
    
    public function create(array $data): User
    {
        return User::create($data);
    }
    
    public function update(User $user, array $data): User
    {
        $user->update($data);
        return $user->fresh();
    }
    
    public function delete(User $user): bool
    {
        return $user->delete();
    }
}

// App\Repositories\RepositoryServiceProvider
namespace App\Repositories;

use Illuminate\Support\ServiceProvider;

class RepositoryServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app->bind(
            UserRepositoryInterface::class,
            EloquentUserRepository::class
        );
    }
}
```

---

## 6. API Architecture

### 6.1 API Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│                         API ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  routes/api.php                                                     │
│  ├── Auth Routes                                                    │
│  │   POST   /api/register                                           │
│  │   POST   /api/login                                              │
│  │   POST   /api/logout                                             │
│  │   POST   /api/forgot-password                                    │
│  │   POST   /api/reset-password                                     │
│  │                                                                  │
│  ├── User Routes (auth required)                                    │
│  │   GET    /api/users          # List users                        │
│  │   POST   /api/users          # Create user                       │
│  │   GET    /api/users/{id}     # Get user                         │
│  │   PUT    /api/users/{id}     # Update user                      │
│  │   DELETE /api/users/{id}     # Delete user                      │
│  │                                                                  │
│  └── Product Routes (public)                                         │
│      GET    /api/products        # List products                   │
│      GET    /api/products/{id}   # Get product                     │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    API Response Format                        │   │
│  │                                                             │   │
│  │  Success:                                                    │   │
│  │  {                                                          │   │
│  │    "success": true,                                         │   │
│  │    "data": { ... },                                         │   │
│  │    "message": "Operation successful"                        │   │
│  │  }                                                          │   │
│  │                                                             │   │
│  │  Error:                                                     │   │
│  │  {                                                          │   │
│  │    "success": false,                                        │   │
│  │    "error": {                                               │   │
│  │      "code": "VALIDATION_ERROR",                           │   │
│  │      "message": "Invalid input",                            │   │
│  │      "details": { ... }                                     │   │
│  │    }                                                        │   │
│  │  }                                                          │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 6.2 API Controller Example

```php
// app/Http\Controllers\Api\UserController
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreUserRequest;
use App\Http\Requests\UpdateUserRequest;
use App\Http\Resources\UserResource;
use App\Http\Resources\UserCollection;
use App\Repositories\Contracts\UserRepositoryInterface;
use Illuminate\Http\JsonResponse;

class UserController extends Controller
{
    public function __construct(
        private UserRepositoryInterface $userRepository
    ) {}
    
    public function index(): UserCollection
    {
        $users = $this->userRepository->paginate(15);
        return new UserCollection($users);
    }
    
    public function store(StoreUserRequest $request): JsonResponse
    {
        $user = $this->userRepository->create($request->validated());
        
        return response()->json([
            'success' => true,
            'data' => new UserResource($user),
            'message' => 'User created successfully',
        ], 201);
    }
    
    public function show(int $id): JsonResponse
    {
        $user = $this->userRepository->find($id);
        
        if (!$user) {
            return response()->json([
                'success' => false,
                'error' => [
                    'code' => 'NOT_FOUND',
                    'message' => 'User not found',
                ],
            ], 404);
        }
        
        return response()->json([
            'success' => true,
            'data' => new UserResource($user),
        ]);
    }
    
    public function update(UpdateUserRequest $request, int $id): JsonResponse
    {
        $user = $this->userRepository->find($id);
        
        if (!$user) {
            return response()->json([
                'success' => false,
                'error' => [
                    'code' => 'NOT_FOUND',
                    'message' => 'User not found',
                ],
            ], 404);
        }
        
        $user = $this->userRepository->update($user, $request->validated());
        
        return response()->json([
            'success' => true,
            'data' => new UserResource($user),
            'message' => 'User updated successfully',
        ]);
    }
    
    public function destroy(int $id): JsonResponse
    {
        $user = $this->userRepository->find($id);
        
        if (!$user) {
            return response()->json([
                'success' => false,
                'error' => [
                    'code' => 'NOT_FOUND',
                    'message' => 'User not found',
                ],
            ], 404);
        }
        
        $this->userRepository->delete($user);
        
        return response()->json([
            'success' => true,
            'message' => 'User deleted successfully',
        ]);
    }
}
```

---

## Liên kết liên quan
- [Laravel Glossary](./glossary.md)
- [Laravel Best Practices](./best-practice.md)
- [Laravel Anti-Patterns](./anti-pattern.md)
- [Laravel Checklist](./checklist.md)
- [Laravel FAQ](./faq.md)
- [Laravel Decision Tree](./decision-tree.md)
