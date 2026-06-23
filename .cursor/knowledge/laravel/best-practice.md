# Laravel Best Practices - Các Thực Hành Tốt Nhất

## Mục lục
1. [Controller Best Practices](#1-controller-best-practices)
2. [Model Best Practices](#2-model-best-practices)
3. [Database Best Practices](#3-database-best-practices)
4. [Security Best Practices](#4-security-best-practices)
5. [API Best Practices](#5-api-best-practices)
6. [Testing Best Practices](#6-testing-best-practices)
7. [Performance Best Practices](#7-performance-best-practices)

---

## 1. Controller Best Practices

### 1.1 Keep Controllers Thin

**Mô tả**: Controllers chỉ nên xử lý HTTP request/response logic. Business logic nên được đặt trong Services hoặc Repositories.

**Ví dụ**:
```php
// ❌ BAD: Fat controller with business logic
class UserController extends Controller
{
    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|email|unique:users',
            'password' => 'required|string|min:8',
        ]);
        
        $validated['password'] = bcrypt($validated['password']);
        
        $user = User::create($validated);
        
        Mail::to($user)->send(new WelcomeMail($user));
        
        event(new UserRegistered($user));
        
        return redirect()->route('users.show', $user->id);
    }
}

// ✅ GOOD: Thin controller
class UserController extends Controller
{
    public function __construct(
        private UserService $userService
    ) {}
    
    public function store(StoreUserRequest $request): RedirectResponse
    {
        $user = $this->userService->createUser($request->validated());
        
        return redirect()->route('users.show', $user->id)
            ->with('success', 'User created successfully');
    }
}
```

**Khi nào áp dụng**: Mọi controllers.

### 1.2 Use Form Request Validation

**Mô tả**: Sử dụng Form Request classes thay vì inline validation để code sạch hơn và reusable.

**Ví dụ**:
```php
// App\Http\Requests\StoreUserRequest
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
            'email' => [
                'required',
                'email',
                Rule::unique('users')->ignore($this->user()->id),
            ],
            'password' => 'required|string|min:8|confirmed',
            'role' => 'sometimes|in:admin,user,editor',
        ];
    }
    
    public function messages(): array
    {
        return [
            'name.required' => 'Tên người dùng là bắt buộc.',
            'email.unique' => 'Email này đã được sử dụng.',
        ];
    }
}
```

**Khi nào áp dụng**: Mọi form submissions.

### 1.3 Use API Resources

**Mô tả**: Sử dụng API Resources để transform models thành JSON responses một cách nhất quán.

**Ví dụ**:
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
            'posts_count' => $this->whenCounted('posts'),
            'posts' => PostResource::collection($this->whenLoaded('posts')),
        ];
    }
}

// Usage in controller
public function index(): UserCollection
{
    $users = User::with('posts')->paginate();
    return UserCollection::make($users);
}
```

**Khi nào áp dụng**: API responses.

---

## 2. Model Best Practices

### 2.1 Define Relationships Properly

**Mô tả**: Luôn define Eloquent relationships với proper types và constraints.

**Ví dụ**:
```php
// App\Models\User
class User extends Model
{
    protected $fillable = ['name', 'email', 'password'];
    
    protected $hidden = ['password', 'remember_token'];
    
    protected $casts = [
        'email_verified_at' => 'datetime',
        'password' => 'hashed',
    ];
    
    // Relationships
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
    
    public function comments(): HasManyThrough
    {
        return $this->hasManyThrough(Comment::class, Post::class);
    }
    
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class)
            ->withTimestamps();
    }
    
    public function hasRole(string $role): bool
    {
        return $this->roles()->where('name', $role)->exists();
    }
}
```

**Khi nào áp dụng**: Mọi Eloquent models.

### 2.2 Use Scopes for Common Queries

**Mô tả**: Sử dụng query scopes để encapsulate common query logic.

**Ví dụ**:
```php
// App\Models\Post
class Post extends Model
{
    // Local scope
    public function scopePublished($query)
    {
        return $query->where('published', true);
    }
    
    public function scopeForUser($query, User $user)
    {
        return $query->where('user_id', $user->id);
    }
    
    public function scopeSearch($query, string $term)
    {
        return $query->where(function ($q) use ($term) {
            $q->where('title', 'like', "%{$term}%")
              ->orWhere('body', 'like', "%{$term}%");
        });
    }
    
    public function scopeInCategory($query, Category $category)
    {
        return $query->where('category_id', $category->id);
    }
}

// Usage
$posts = Post::published()
    ->forUser(auth()->user())
    ->search('laravel')
    ->latest()
    ->paginate();
```

**Khi nào áp dụng**: Common query patterns.

### 2.3 Use Accessors and Mutators

**Mô tả**: Use accessors (getXxxAttribute) và mutators (setXxxAttribute) để format data.

**Ví dụ**:
```php
class User extends Model
{
    // Accessor
    public function getFullNameAttribute(): string
    {
        return "{$this->first_name} {$this->last_name}";
    }
    
    // Mutator
    public function setPasswordAttribute($value): void
    {
        $this->attributes['password'] = bcrypt($value);
    }
    
    // Date accessor with formatting
    public function getCreatedAtFormattedAttribute(): string
    {
        return $this->created_at->format('d/m/Y H:i');
    }
}
```

**Khi nào áp dụng**: Data formatting logic.

---

## 3. Database Best Practices

### 3.1 Use Indexes Properly

**Mô tả**: Tạo indexes cho các columns thường xuyên được query để improve performance.

**Ví dụ**:
```php
// Migration
Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->onDelete('cascade');
    $table->foreignId('category_id')->constrained();
    $table->string('title');
    $table->text('body');
    $table->boolean('published')->default(false);
    $table->timestamp('published_at')->nullable();
    $table->timestamps();
    
    // Indexes
    $table->index(['published', 'published_at']);
    $table->index(['user_id', 'published']);
    $table->fullText(['title', 'body']);
});
```

**Khi nào áp dụng**: Columns trong WHERE clauses.

### 3.2 Use Transactions for Complex Operations

**Mô tả**: Wrap complex database operations trong transactions để đảm bảo data consistency.

**Ví dụ**:
```php
public function createOrder(array $data): Order
{
    return DB::transaction(function () use ($data) {
        // Create order
        $order = Order::create([
            'user_id' => $data['user_id'],
            'total' => 0,
            'status' => 'pending',
        ]);
        
        $total = 0;
        
        foreach ($data['items'] as $item) {
            $product = Product::findOrFail($item['product_id']);
            
            OrderItem::create([
                'order_id' => $order->id,
                'product_id' => $product->id,
                'quantity' => $item['quantity'],
                'price' => $product->price,
            ]);
            
            $total += $product->price * $item['quantity'];
        }
        
        $order->update(['total' => $total]);
        
        return $order;
    });
}
```

**Khi nào áp dụng**: Multiple related database operations.

### 3.3 Use Eager Loading to Prevent N+1

**Mô tả**: Sử dụng with() để eager load relationships và tránh N+1 query problem.

**Ví dụ**:
```php
// ❌ BAD: N+1 problem
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->user->name; // 1 query for each post!
}

// ✅ GOOD: Eager loading
$posts = Post::with('user', 'comments', 'category')->get();
foreach ($posts as $post) {
    echo $post->user->name; // No additional queries!
}

// Nested eager loading
$posts = Post::with('user.comments')->get();

// Conditional eager loading
$posts = Post::with([
    'user',
    'comments' => fn($query) => $query->approved(),
])->get();
```

**Khi nào áp dụng**: Mọi queries return models with relationships.

---

## 4. Security Best Practices

### 4.1 Validate and Sanitize Input

**Mô tả**: Luôn validate và sanitize user input để prevent injection attacks.

**Ví dụ**:
```php
// Form Request validation
class StorePostRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'title' => 'required|string|max:255|strip_tags',
            'body' => 'required|string',
            'category_id' => 'exists:categories,id',
        ];
    }
    
    public function validated($key = null, $default = null): array
    {
        $validated = parent::validated();
        
        // Additional sanitization
        $validated['title'] = strip_tags($validated['title']);
        
        return $validated;
    }
}
```

**Khi nào áp dụng**: Mọi user input.

### 4.2 Use Mass Assignment Protection

**Mô tả**: Sử dụng $fillable hoặc $guarded để protect against mass assignment.

**Ví dụ**:
```php
// Model
class User extends Model
{
    // Only these fields can be mass-assigned
    protected $fillable = ['name', 'email', 'password'];
    
    // These fields cannot be mass-assigned (opposite of fillable)
    protected $guarded = ['id', 'is_admin'];
    
    // Hidden fields won't be returned in JSON
    protected $hidden = ['password', 'remember_token'];
}
```

**Khi nào áp dụng**: Mọi Eloquent models.

### 4.3 Implement CSRF Protection

**Mô tả**: Laravel tự động protect against CSRF attacks cho web routes. Đảm bảo sử dụng CSRF token cho forms.

**Ví dụ**:
```blade
{{-- Blade form with CSRF --}}
<form method="POST" action="{{ route('logout') }}">
    @csrf
    @method('DELETE')
    <button type="submit">Logout</button>
</form>

{{-- AJAX request with CSRF --}}
$.ajax({
    url: '/api/posts',
    method: 'POST',
    headers: {
        'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content,
    },
    data: { title: 'New Post' },
});
```

**Khi nào áp dụng**: Mọi state-changing requests.

---

## 5. API Best Practices

### 5.1 Use Versioning

**Mô tả**: Version your API để maintain backwards compatibility.

**Ví dụ**:
```php
// routes/api.php
Route::prefix('v1')->group(function () {
    Route::apiResource('users', \App\Http\Controllers\Api\V1\UserController::class);
});

Route::prefix('v2')->group(function () {
    Route::apiResource('users', \App\Http\Controllers\Api\V2\UserController::class);
});

// URLs: /api/v1/users, /api/v2/users
```

**Khi nào áp dụng**: Public APIs.

### 5.2 Return Consistent Response Format

**Mô tả**: Sử dụng consistent response format cho tất cả API endpoints.

**Ví dụ**:
```php
// App\Traits\ApiResponse
trait ApiResponse
{
    protected function success(mixed $data = null, string $message = null, int $status = 200): JsonResponse
    {
        return response()->json([
            'success' => true,
            'data' => $data,
            'message' => $message,
        ], $status);
    }
    
    protected function error(string $message, int $status = 400, array $errors = []): JsonResponse
    {
        return response()->json([
            'success' => false,
            'error' => [
                'message' => $message,
                'errors' => $errors,
            ],
        ], $status);
    }
}

// Usage
class UserController extends Controller
{
    use ApiResponse;
    
    public function show(User $user): JsonResponse
    {
        return $this->success(new UserResource($user));
    }
}
```

**Khi nào áp dụng**: API responses.

### 5.3 Use Pagination

**Mô tả**: Always paginate large datasets to prevent memory issues.

**Ví dụ**:
```php
// Controller
public function index(): UserCollection
{
    $users = User::paginate(15);
    return UserCollection::make($users);
}

// Custom pagination
$users = User::query()
    ->where('active', true)
    ->orderBy('name')
    ->paginate(15);

// Simple pagination (faster for large datasets)
$users = User::simplePaginate(15);
```

**Khi nào áp dụng**: Mọi list endpoints.

---

## 6. Testing Best Practices

### 6.1 Write Feature Tests

**Mô tả**: Viết feature tests để test complete user workflows.

**Ví dụ**:
```php
// tests/Feature/UserRegistrationTest.php
class UserRegistrationTest extends TestCase
{
    use RefreshDatabase;
    
    public function test_user_can_register_with_valid_data(): void
    {
        $response = $this->post(route('register'), [
            'name' => 'Nguyen Van A',
            'email' => 'nguyenvana@example.com',
            'password' => 'password123',
            'password_confirmation' => 'password123',
        ]);
        
        $response->assertRedirect(route('home'));
        $this->assertDatabaseHas('users', [
            'email' => 'nguyenvana@example.com',
        ]);
        $this->assertAuthenticated();
    }
    
    public function test_registration_fails_with_duplicate_email(): void
    {
        User::factory()->create(['email' => 'existing@example.com']);
        
        $response = $this->post(route('register'), [
            'name' => 'Test User',
            'email' => 'existing@example.com',
            'password' => 'password123',
            'password_confirmation' => 'password123',
        ]);
        
        $response->assertSessionHasErrors('email');
    }
}
```

**Khi nào áp dụng**: Mọi user-facing features.

### 6.2 Use Factories for Test Data

**Mô tả**: Sử dụng Model Factories thay vì hardcoded test data.

**Ví dụ**:
```php
// database/factories/UserFactory.php
class UserFactory extends Factory
{
    public function definition(): array
    {
        return [
            'name' => fake()->name(),
            'email' => fake()->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => bcrypt('password'),
        ];
    }
    
    public function admin(): static
    {
        return $this->state(fn (array $attributes) => [
            'is_admin' => true,
        ]);
    }
}

// Test usage
$user = User::factory()->create();
$admin = User::factory()->admin()->create();
$users = User::factory()->count(5)->create();
```

**Khi nào áp dụng**: Test data creation.

### 6.3 Use Http Tests for APIs

**Mô tả**: Test API endpoints với proper assertions.

**Ví dụ**:
```php
// tests/Feature/Api/UserApiTest.php
class UserApiTest extends TestCase
{
    use RefreshDatabase;
    
    public function test_api_returns_users_list(): void
    {
        User::factory()->count(3)->create();
        
        $response = $this->getJson('/api/users');
        
        $response->assertOk()
            ->assertJsonStructure([
                'data' => [
                    '*' => ['id', 'name', 'email']
                ],
                'links',
                'meta',
            ]);
    }
    
    public function test_api_requires_authentication(): void
    {
        $response = $this->getJson('/api/users');
        
        $response->assertUnauthorized();
    }
    
    public function test_api_validates_user_creation(): void
    {
        $response = $this->postJson('/api/users', [
            'name' => '',
            'email' => 'invalid-email',
        ]);
        
        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['name', 'email']);
    }
}
```

**Khi nào áp dụng**: API testing.

---

## 7. Performance Best Practices

### 7.1 Cache Expensive Operations

**Mô tả**: Cache kết quả của expensive operations để reduce database load.

**Ví dụ**:
```php
// Using Cache facade
$users = Cache::remember('users.active', 3600, function () {
    return User::where('active', true)->get();
});

// Cache tags (Redis)
Cache::tags(['users', 'active'])->remember('active_users', 3600, function () {
    return User::where('active', true)->get();
});

// Cache invalidation
Cache::forget('users.active');
Cache::tags(['users'])->flush();

// Route caching
php artisan route:cache

// Config caching
php artisan config:cache
```

**Khi nào áp dụng**: Expensive queries, computations.

### 7.2 Use Queue for Long Tasks

**Mô tả**: Defer time-consuming tasks đến queues để improve response times.

**Ví dụ**:
```php
// Dispatch job
SendWelcomeEmail::dispatch($user);

// Delayed job
SendWelcomeEmail::dispatch($user)->delay(now()->addMinutes(5));

// Batch jobs
Bus::batch([
    new ProcessCsvFile($file1),
    new ProcessCsvFile($file2),
])->dispatch();

// Job chaining
SendWelcomeEmail::withChain([
    new SetupUserAccount($user),
    new SendSlackNotification($user),
])->dispatch();
```

**Khi nào áp dụng**: Email sending, heavy processing.

### 7.3 Optimize Database Queries

**Mô tả**: Monitor và optimize slow queries.

**Ví dụ**:
```php
// Use select for specific columns
$users = User::select('id', 'name', 'email')->get();

// Use whereIn for multiple IDs
$users = User::whereIn('id', [1, 2, 3])->get();

// Use chunks for large datasets
User::chunk(100, function ($users) {
    foreach ($users as $user) {
        // Process each user
    }
});

// Use cursor for memory efficiency
foreach (User::cursor() as $user) {
    // Process each user
}
```

**Khi nào áp dụng**: Large dataset operations.

---

## Liên kết liên quan
- [Laravel Glossary](./glossary.md)
- [Laravel Architecture](./architecture.md)
- [Laravel Anti-Patterns](./anti-pattern.md)
- [Laravel Checklist](./checklist.md)
- [Laravel FAQ](./faq.md)
- [Laravel Decision Tree](./decision-tree.md)
