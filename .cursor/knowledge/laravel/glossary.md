# Laravel Glossary - Thuật Ngữ Chuyên Ngành

## Mục lục
1. [Eloquent ORM](#1-eloquent-orm)
2. [Routing](#2-routing)
3. [Controllers](#3-controllers)
4. [Middleware](#4-middleware)
5. [Migrations](#5-migrations)
6. [Blade Templates](#6-blade-templates)
7. [Service Container](#7-service-container)

---

## Eloquent ORM

**Định nghĩa**: Eloquent là Object-Relational Mapping (ORM) trong Laravel, cung cấp beautiful active record implementation để làm việc với database. Mỗi database table có một Model tương ứng.

**Ví dụ**:
```php
// App\Models\User
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    protected $fillable = ['name', 'email', 'password'];
    protected $hidden = ['password', 'remember_token'];
    
    public function posts()
    {
        return $this->hasMany(Post::class);
    }
}

// Usage
$user = User::find(1);
$user->posts->each(fn($post) => $post->title);
```

---

## Route

**Định nghĩa**: Routes định nghĩa endpoints của ứng dụng và ánh xạ URLs đến controllers hoặc closures. Được định nghĩa trong `routes/web.php` hoặc `routes/api.php`.

**Ví dụ**:
```php
// Basic routes
Route::get('/users', [UserController::class, 'index']);
Route::post('/users', [UserController::class, 'store']);
Route::put('/users/{id}', [UserController::class, 'update']);
Route::delete('/users/{id}', [UserController::class, 'destroy']);

// Route with middleware
Route::middleware(['auth', 'throttle:60,1'])->group(function () {
    Route::get('/dashboard', fn() => view('dashboard'));
});

// Resource routes
Route::resource('posts', PostController::class);
```

---

## Controller

**Định nghĩa**: Controllers nhóm related request handling logic vào một class. Chúng act như intermediaries giữa routes và business logic.

**Ví dụ**:
```php
// App\Http\Controllers\UserController
namespace App\Http\Controllers;

use App\Models\User;
use App\Http\Requests\StoreUserRequest;
use Illuminate\Http\Request;

class UserController extends Controller
{
    public function index()
    {
        $users = User::paginate(15);
        return view('users.index', compact('users'));
    }
    
    public function store(StoreUserRequest $request)
    {
        User::create($request->validated());
        return redirect()->route('users.index')
            ->with('success', 'User created successfully');
    }
}
```

---

## Middleware

**Định nghĩa**: Middleware cung cấp mechanism để filter HTTP requests entering your application. Ví dụ: authentication, logging, CORS.

**Ví dụ**:
```php
// App\Http\Middleware\EnsureUserIsAdmin
namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class EnsureUserIsAdmin
{
    public function handle(Request $request, Closure $next)
    {
        if (!$request->user() || !$request->user()->isAdmin()) {
            return redirect()->route('home');
        }
        
        return $next($request);
    }
}

// Register in Kernel.php or using Route::middleware()
Route::middleware(['auth', EnsureUserIsAdmin::class])->group(function () {
    Route::get('/admin', fn() => view('admin'));
});
```

---

## Migration

**Định nghĩa**: Migrations là version control cho database, cho phép define và share application database schema definition.

**Ví dụ**:
```php
// database/migrations/2024_01_01_000001_create_users_table.php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('users', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('email')->unique();
            $table->timestamp('email_verified_at')->nullable();
            $table->string('password');
            $table->rememberToken();
            $table->timestamps();
        });
    }
    
    public function down(): void
    {
        Schema::dropIfExists('users');
    }
};
```

---

## Blade Template

**Định nghĩa**: Blade là Laravel's powerful templating engine. Nó cung cấp clean syntax cho displaying data, layouts, và control structures.

**Ví dụ**:
```blade
{{-- layouts/app.blade.php --}}
<!DOCTYPE html>
<html>
<head>
    <title>@yield('title', 'My App')</title>
</head>
<body>
    @include('partials.header')
    
    <main>
        @yield('content')
    </main>
    
    @stack('scripts')
</body>
</html>

{{-- resources/views/posts/index.blade.php --}}
@extends('layouts.app')

@section('title', 'Posts')

@section('content')
    @forelse($posts as $post)
        <article>
            <h2>{{ $post->title }}</h2>
            <p>{{ Str::limit($post->body, 100) }}</p>
        </article>
    @empty
        <p>No posts found.</p>
    @endforelse
    
    {{ $posts->links() }}
@endsection
```

---

## Service Container

**Định nghĩa**: Service Container là powerful tool để manage class dependencies và performing dependency injection trong Laravel.

**Ví dụ**:
```php
// Binding
app()->bind(UserRepositoryInterface::class, EloquentUserRepository::class);

// Singleton (same instance every time)
app()->singleton(App\Services\CacheService::class, function ($app) {
    return new CacheService($app['cache.store']);
});

// Singleton instance
app()->instance('helpdesk', new HelpDesk(new ApiImplementation));

// Resolving
$userRepo = app(UserRepositoryInterface::class);
$service = app()->make(ServiceClass::class);
```

---

## Service Provider

**Định nghĩa**: Service Providers là central place để configure your application, register services, và bootstrap applications.

**Ví dụ**:
```php
// App\Providers\AppServiceProvider
namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use App\Services\PaymentGateway;

class AppServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app->singleton(PaymentGateway::class, function ($app) {
            return new PaymentGateway(config('services.stripe.secret'));
        });
    }
    
    public function boot(): void
    {
        // Boot logic here
    }
}
```

---

## Artisan

**Định nghĩa**: Artisan là command-line interface included với Laravel, cung cấp helpful commands cho development.

**Ví dụ**:
```bash
# Create a controller
php artisan make:controller UserController

# Create a model with migration
php artisan make:model User -m

# Run migrations
php artisan migrate

# Create a middleware
php artisan make:middleware EnsureUserIsAdmin

# Clear caches
php artisan config:clear
php artisan cache:clear
php artisan route:clear

# List routes
php artisan route:list
```

---

## Eloquent Relationships

**Định nghĩa**: Eloquent relationships là methods để define relationships giữa models, như one-to-one, one-to-many, many-to-many.

**Ví dụ**:
```php
// One to One
public function phone()
{
    return $this->hasOne(Phone::class);
}

// One to Many
public function posts()
{
    return $this->hasMany(Post::class);
}

// Many to Many
public function roles()
{
    return $this->belongsToMany(Role::class);
}

// Has Many Through
public function posts()
{
    return $this->hasManyThrough(Post::class, Category::class);
}
```

---

## Query Builder

**Định nghĩa**: Laravel's database query builder cung cấp convenient, fluent interface để create và execute database queries.

**Ví dụ**:
```php
use Illuminate\Support\Facades\DB;

// Basic queries
$users = DB::table('users')
    ->where('active', true)
    ->orderBy('name')
    ->get();

// With joins
$orders = DB::table('orders')
    ->join('users', 'orders.user_id', '=', 'users.id')
    ->select('orders.*', 'users.name')
    ->where('orders.status', 'pending')
    ->get();

// Aggregates
$count = DB::table('orders')->count();
$max = DB::table('orders')->max('total');
```

---

## Form Request

**Định nghĩa**: Form Requests là custom request classes chứa validation logic cho incoming form/hTTP requests.

**Ví dụ**:
```php
// App\Http\Requests\StoreUserRequest
namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreUserRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', User::class);
    }
    
    public function rules(): array
    {
        return [
            'name' => 'required|string|max:255',
            'email' => 'required|email|unique:users,email',
            'password' => 'required|string|min:8|confirmed',
        ];
    }
}

// Usage in controller
public function store(StoreUserRequest $request)
{
    // Request is already validated
    User::create($request->validated());
}
```

---

## Policy

**Định nghĩa**: Policies là classes organize authorization logic around a particular model or resource.

**Ví dụ**:
```php
// App\Policies\PostPolicy
namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    public function viewAny(User $user): bool
    {
        return true;
    }
    
    public function view(User $user, Post $post): bool
    {
        return $post->published || $user->isAdmin();
    }
    
    public function create(User $user): bool
    {
        return $user->hasPermission('create-posts');
    }
    
    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id || $user->isAdmin();
    }
}
```

---

## Event & Listener

**Định nghĩa**: Events cung cấp observer pattern implementation, cho phép you subscribe và listen to events trong application.

**Ví dụ**:
```php
// Event: App\Events\OrderPlaced
class OrderPlaced
{
    public function __construct(public Order $order) {}
}

// Listener: App\Listeners\SendOrderNotification
class SendOrderNotification
{
    public function handle(OrderPlaced $event): void
    {
        Mail::to($event->order->user)->send(new OrderConfirmation($event->order));
    }
}

// EventServiceProvider
protected $listen = [
    OrderPlaced::class => [
        SendOrderNotification::class,
        UpdateInventory::class,
    ],
];
```

---

## Queue

**Định nghĩa**: Queues cho phép defer processing of time-consuming tasks như sending emails, processing uploads, để improve application responsiveness.

**Ví dụ**:
```php
// Job: App\Jobs\SendWelcomeEmail
class SendWelcomeEmail implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable;
    
    public function __construct(public User $user) {}
    
    public function handle(): void
    {
        Mail::to($this->user)->send(new WelcomeMail($this->user));
    }
}

// Dispatching
SendWelcomeEmail::dispatch($user);

// Delayed dispatch
SendWelcomeEmail::dispatch($user)->delay(now()->addMinutes(5));

// Chain jobs
SendWelcomeEmail::withChain([
    new SetupUserProfile($user),
    new SendSlackNotification($user),
])->dispatch();
```

---

## Collection

**Định nghĩa**: Eloquent collections là extended Laravel collections chứa kết quả từ Eloquent queries, cung cấp powerful methods để manipulate data.

**Ví dụ**:
```php
$users = User::all();

// Filter
$admins = $users->filter(fn($user) => $user->isAdmin());

// Map
$emails = $users->map(fn($user) => $user->email);

// Group
$grouped = $users->groupBy('role');

// Sort
$sorted = $users->sortBy('name');

// Find
$user = $users->find(1);

// Chunk
$chunks = $users->chunk(10);
```

---

## liên kết liên quan
- [Laravel Architecture](./architecture.md)
- [Laravel Best Practices](./best-practice.md)
- [Laravel Anti-Patterns](./anti-pattern.md)
- [Laravel Checklist](./checklist.md)
- [Laravel FAQ](./faq.md)
- [Laravel Decision Tree](./decision-tree.md)
