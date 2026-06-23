# Laravel FAQ - Câu Hỏi Thường Gặp

## Mục lục
1. [General](#1-general)
2. [Controllers & Routing](#2-controllers--routing)
3. [Models & Database](#3-models--database)
4. [Authentication](#4-authentication)
5. [API](#5-api)
6. [Performance](#6-performance)

---

## 1. General

### Q1: Sự khác nhau giữa Service Provider register() và boot() là gì?

**A:**

| Method | Purpose | When Called | Use For |
|--------|---------|-------------|---------|
| `register()` | Register services into container | Early in bootstrap | Binding interfaces to implementations |
| `boot()` | Boot services | After all providers registered | Using other services, view composers |

```php
// ServiceProvider.php
class AppServiceProvider extends ServiceProvider
{
    // Called first - services not yet available
    public function register(): void
    {
        // Bind interface to implementation
        $this->app->bind(
            PaymentGatewayInterface::class,
            StripePaymentGateway::class
        );
        
        // Register singletons
        $this->app->singleton(CacheService::class);
    }
    
    // Called after all providers register() - services available
    public function boot(): void
    {
        // Use other services
        $repos = $this->app->make(RepositoryManager::class);
        
        // Register view composers
        View::composer('layouts.app', LayoutComposer::class);
        
        // Register blade directives
        Blade::directive('money', fn($amount) => "<?php echo number_format($amount, 0, ',', '.'); ?>");
    }
}
```

---

### Q2: Làm thế nào để debug queries trong Laravel?

**A:** Multiple methods:

**1. DB::listen()**
```php
// In ServiceProvider boot()
DB::listen(function ($query) {
    logger()->info($query->sql, [
        'bindings' => $query->bindings,
        'time' => $query->time,
    ]);
});
```

**2. Query Log**
```php
DB::enableQueryLog();
$users = User::all();
dd(DB::getQueryLog());
```

**3. Laravel Debugbar**
```bash
composer require barryvdh/laravel-debugbar --dev
```

**4. toSql() method**
```php
$query = User::where('active', true)->toSql();
dd($query);
```

---

### Q3: Composer autoload không hoạt động?

**A:** Run these commands:

```bash
# Clear and rebuild autoload
composer dump-autoload

# If using packages
composer dump-autoload -o

# Or reinstall
composer install
```

---

## 2. Controllers & Routing

### Q4: Làm thế nào để validate và redirect back với errors?

**A:** Using Form Request:

```php
// FormRequest
class CreatePostRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'title' => 'required|string|max:255',
            'body' => 'required|string',
        ];
    }
}

// Controller
public function store(CreatePostRequest $request)
{
    // Request already validated
    Post::create($request->validated());
    
    return redirect()->route('posts.index')
        ->with('success', 'Post created successfully');
}
```

---

### Q5: Sự khác nhau giữa redirect() và back()?

**A:**

| Method | Behavior |
|--------|----------|
| `redirect()->back()` | Go back to previous URL |
| `redirect()->route('name')` | Go to named route |
| `redirect()->intended()` | Go to intended URL after auth |

```php
// Back with input
return redirect()->back()->withInput();

// Back with errors
return redirect()->back()->withErrors($errors);

// Intended after login
return redirect()->intended('/dashboard');
```

---

### Q6: Route model binding hoạt động như thế nào?

**A:** Laravel automatically resolves models based on route parameters:

```php
// routes/web.php
Route::get('/posts/{post}', [PostController::class, 'show']);

// PostController.php
public function show(Post $post)
{
    // Laravel automatically finds Post by ID from URL
    return view('posts.show', compact('post'));
}

// Custom key
Route::get('/posts/{post:slug}', [PostController::class, 'show']);

// Custom binding in RouteServiceProvider
public function boot(): void
{
    Route::model('post', Post::class);
    
    // Or with custom resolution
    Route::bind('post', function ($value) {
        return Post::where('slug', $value)->firstOrFail();
    });
}
```

---

## 3. Models & Database

### Q7: Soft Deletes vs Hard Deletes?

**A:**

| Aspect | Soft Deletes | Hard Deletes |
|--------|-------------|--------------|
| Data | Marked with deleted_at | Permanently removed |
| Recovery | Can be restored | Cannot recover |
| Query | Excluded by default | Included |
| Use Case | User data, archives | Temporary data |

```php
// Model with soft deletes
class Post extends Model
{
    use SoftDeletes;
}

// Usage
$post->delete(); // Soft delete
$post->restore(); // Restore
$post->forceDelete(); // Permanent delete

// Include soft deleted in query
Post::withTrashed()->find($id);
Post::onlyTrashed()->get();
```

---

### Q8: Eloquent has() vs whereHas()?

**A:**

| Method | Purpose |
|--------|---------|
| `has()` | Filter models that have at least one related model |
| `whereHas()` | Filter models with conditions on related model |
| `orHas()` | OR condition for has |
| `doesntHave()` | Filter models without related |

```php
// Has - users with at least one post
User::has('posts')->get();

// WhereHas - users with published posts
User::whereHas('posts', function ($q) {
    $q->where('published', true);
})->get();

// With count
User::has('posts', '>=', 3)->get();
```

---

### Q9: Làm thế nào để updateOrCreate?

**A:** Update existing record or create new:

```php
// Update if exists, create if not
$user = User::updateOrCreate(
    ['email' => $request->email],
    [
        'name' => $request->name,
        'password' => bcrypt($request->password),
    ]
);

// With unique constraint
$product = Product::updateOrCreate(
    [
        'sku' => $productData['sku'],
        'company_id' => auth()->company_id,
    ],
    $productData
);
```

---

### Q10: Pagination vs SimplePagination vs CursorPagination?

**A:**

| Method | SQL | Use Case |
|--------|-----|----------|
| `paginate(n)` | OFFSET/LIMIT with count | User-facing with page numbers |
| `simplePaginate(n)` | LIMIT with next IDs | Faster, no total count |
| `cursorPaginate(n)` | WHERE id > ? | Very large datasets |

```php
// Paginate - shows total, page numbers
$users = User::paginate(15);
$users->links(); // Page links
$users->total(); // Total count

// Simple - faster, no total
$users = User::simplePaginate(15);

// Cursor - fastest for large data
$users = User::cursorPaginate(15);
```

---

## 4. Authentication

### Q11: Làm thế nào để implement custom authentication?

**A:** Using AuthController:

```php
// Login
public function login(LoginRequest $request)
{
    $credentials = $request->only('email', 'password');
    
    if (Auth::attempt($credentials, $request->remember)) {
        $request->session()->regenerate();
        return redirect()->intended('/dashboard');
    }
    
    return back()->withErrors([
        'email' => 'Thông tin đăng nhập không đúng.',
    ]);
}

// Logout
public function logout(Request $request)
{
    Auth::logout();
    $request->session()->invalidate();
    $request->session()->regenerateToken();
    return redirect('/');
}
```

---

### Q12: Middleware auth vs guest?

**A:**

| Middleware | Purpose |
|-----------|---------|
| `auth` | Redirect if not logged in |
| `guest` | Redirect if already logged in |
| `auth:admin` | Redirect if not logged in as admin |
| `throttle` | Rate limiting |

```php
// Protect routes
Route::middleware(['auth'])->group(function () {
    Route::get('/dashboard', fn() => view('dashboard'));
});

// Guest only (login page, etc)
Route::middleware(['guest'])->group(function () {
    Route::get('/login', [AuthController::class, 'showLogin']);
    Route::post('/login', [AuthController::class, 'login']);
});

// Multiple guards
Route::middleware(['auth:admin'])->group(function () {
    Route::get('/admin', fn() => view('admin'));
});
```

---

### Q13: Làm thế nào để check multiple user roles?

**A:** Using authorization:

```php
// Gate
Gate::before(function ($user, $ability) {
    return $user->isAdmin() ? true : null;
});

// Policy method
public function before(User $user, string $ability): ?bool
{
    return $user->isAdmin() ? true : null;
}

// Controller
$this->authorize('update', $post);

// Blade
@can('update', $post)
    <button>Edit</button>
@endcan
```

---

## 5. API

### Q14: Laravel Sanctum vs Passport vs JWT?

**A:**

| Package | Best For | Token Type |
|--------|----------|------------|
| Sanctum | SPA, simple APIs | Session + Tokens |
| Passport | Full OAuth2 | OAuth2 tokens |
| JWT | Stateless APIs | Custom JWT |

```php
// Sanctum (recommended for most)
composer require laravel/sanctum
php artisan install:api

// Use in controller
public function index(Request $request)
{
    return $request->user()->tokens;
}

// Revoke token
$request->user()->currentAccessToken()->delete();
```

---

### Q15: Làm thế nào để format API response?

**A:** Using API Resources:

```php
// App\Http\Resources\UserResource
class UserResource extends JsonResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'created_at' => $this->created_at->toIso8601String(),
        ];
    }
}

// App\Http\Resources\UserCollection
class UserCollection extends ResourceCollection
{
    public $collects = UserResource::class;
}

// Controller
return UserResource::make($user);
// or
return UserCollection::make(User::paginate());
```

---

## 6. Performance

### Q16: Caching Strategies?

**A:** Multiple caching approaches:

```php
// Cache::remember
$users = Cache::remember('users.active', 3600, function () {
    return User::where('active', true)->get();
});

// Cache tags (Redis)
Cache::tags(['users'])->put('active', $users, 3600);
$users = Cache::tags(['users'])->get('active');

// Cache invalidation
Cache::forget('users.active');
Cache::tags(['users'])->flush();

// Route caching
php artisan route:cache
php artisan route:clear

// Config caching
php artisan config:cache
php artisan config:clear
```

---

### Q17: Queue jobs không chạy?

**A:** Debug steps:

```php
// 1. Check queue driver in .env
QUEUE_CONNECTION=sync // ❌ synchronous (for testing only)
QUEUE_CONNECTION=database // ✅ database
QUEUE_CONNECTION=redis // ✅ redis

// 2. Run queue worker
php artisan queue:work

// 3. Check failed_jobs table
php artisan queue:failed-table
php artisan queue:retry all

// 4. Monitor
php artisan queue:monitor

// 5. Check job dispatch
Log::info('Job dispatched', ['job' => ProcessPodcast::class]);
```

---

### Q18: Làm thế nào để optimize database queries?

**A:** Best practices:

```php
// 1. Select only needed columns
$users = User::select('id', 'name', 'email')->get();

// 2. Use indexes
Schema::table('posts', function ($table) {
    $table->index(['user_id', 'published']);
});

// 3. Eager load relationships
$posts = Post::with('user', 'comments')->get();

// 4. Use pagination
$posts = Post::paginate(20);

// 5. Chunk large results
User::chunk(100, function ($users) {
    foreach ($users as $user) {
        // Process
    }
});

// 6. Use cursor for memory efficiency
foreach (User::cursor() as $user) {
    // Process
}
```

---

## Liên kết liên quan
- [Laravel Glossary](./glossary.md)
- [Laravel Architecture](./architecture.md)
- [Laravel Best Practices](./best-practice.md)
- [Laravel Anti-Patterns](./anti-pattern.md)
- [Laravel Checklist](./checklist.md)
- [Laravel Decision Tree](./decision-tree.md)
