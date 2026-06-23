---
title: "Laravel Decision Tree - Cây Quyết Định Laravel"
description: "Cây quyết định chi tiết giúp developers lựa chọn đúng patterns và approaches trong Laravel, từ authentication solutions đến caching strategies, queue drivers, và database optimization."
tags: ["laravel", "decision-tree", "architecture", "best-practices", "php"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Laravel Decision Tree - Cây Quyết Định Laravel

## Tổng Quan

Laravel cung cấp nhiều options và patterns cho mỗi aspect của application development. Decision tree này giúp developers navigate qua các lựa chọn này và đưa ra quyết định phù hợp dựa trên requirements cụ thể của dự án.

Mỗi decision tree bao gồm các câu hỏi để hỏi, các options có sẵn, và recommendations dựa trên common use cases và best practices. Use trees này như starting point và adjust theo needs của bạn.

## Mục Đích

Tài liệu này cung cấp:

- Structured decision-making framework cho Laravel development
- Clear recommendations dựa trên use cases
- Trade-off analysis cho mỗi decision
- Quick reference cho common scenarios
- Best practices recommendations từ community

---

## 1. Authentication Solution

### Câu hỏi: Bạn cần authentication cho loại application nào?

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AUTHENTICATION TYPE                          │
└─────────────────────────────────────────────────────────────────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           │                     │                     │
           ▼                     ▼                     ▼
    ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
    │   Web App    │      │    API       │      │  Mobile App  │
    │   (SSR)      │      │   (SPA)      │      │              │
    └──────────────┘      └──────────────┘      └──────────────┘
```

#### A. Web Application (Server-Side Rendered)

| Câu hỏi tiếp | Lựa chọn | Recommendation |
|--------------|----------|----------------|
| Bạn cần full authentication scaffold? | Có | **Laravel Breeze** |
| Bạn cần custom authentication logic? | Có | **Laravel Fortify** |
| Bạn cần OAuth (Google, Facebook login)? | Có | **Laravel Socialite + Breeze/Fortify** |
| Bạn cần multi-tenancy? | Có | **Custom implementation hoặc tenancy package** |

```php
// Laravel Breeze - Recommended for simple web apps
composer require laravel/breeze --dev
php artisan breeze:install

// Features included:
// - Login/Register/Password Reset
// - Email verification
// - Session management
// - Simple Blade views
```

```php
// Laravel Fortify - For headless/custom auth
composer require laravel/fortify
php artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"

// Features:
// - Headless authentication
// - Customizable views
// - No predefined views
```

#### B. API Authentication (SPA hoặc Mobile)

| Câu hỏi tiếp | Lựa chọn | Recommendation |
|--------------|----------|----------------|
| Bạn cần OAuth2? | Có | **Laravel Passport** |
| Bạn chỉ cần simple token auth? | Có | **Laravel Sanctum** |
| Bạn cần third-party OAuth (Google, GitHub)? | Có | **Laravel Socialite** |

```php
// Laravel Sanctum - Simple token auth
composer require laravel/sanctum
php artisan install:api

// Token creation
$token = $user->createToken('device-name')->plainTextToken;

// Revocation
$user->currentAccessToken()->delete();

// Middleware
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/user', fn (Request $request) => $request->user());
});
```

```php
// Laravel Passport - Full OAuth2
composer require laravel/passport
php artisan passport:install

// In User model
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens;
}

// Scopes
Passport::tokensCan([
    'posts:read' => 'Read posts',
    'posts:write' => 'Create/update posts',
]);
```

### Decision Matrix

| Use Case | Recommendation | Alternative |
|----------|----------------|-------------|
| Simple web app với sessions | Breeze | Fortify |
| Custom web auth UI | Fortify | Breeze (with customization) |
| API cho SPA (React/Vue) | Sanctum | Passport (nếu cần OAuth) |
| Mobile app API | Sanctum | Passport |
| OAuth with Google/Facebook | Socialite + Breeze/Sanctum | Passport |
| Full OAuth2 provider | Passport | - |

---

## 2. Database Layer

### Câu hỏi: Bạn nên sử dụng Eloquent hay Query Builder?

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATABASE QUERY TYPE                          │
└─────────────────────────────────────────────────────────────────────┘
                                 │
           ┌─────────────────────┴─────────────────────┐
           │                                           │
           ▼                                           ▼
    ┌──────────────┐                           ┌──────────────┐
    │   Eloquent   │                           │ Query Builder│
    │   (ORM)      │                           │  (Raw SQL)   │
    └──────────────┘                           └──────────────┘
```

#### Khi nào sử dụng Eloquent

| Scenario | Recommendation |
|----------|----------------|
| CRUD với models có relationships | **Eloquent** |
| Model events và observers | **Eloquent** |
| Scopes và accessors | **Eloquent** |
| Single model operations | **Eloquent** |
| Most standard web app operations | **Eloquent** |

```php
// Eloquent - Standard CRUD and relationships
$post = Post::with(['author', 'comments', 'tags'])
    ->published()
    ->findOrFail($id);

$posts = Post::where('category_id', $categoryId)
    ->withCount('comments')
    ->orderBy('created_at', 'desc')
    ->paginate(20);

// Creating with relationships
$post = Post::create([
    'title' => 'New Post',
    'content' => 'Content here',
    'author_id' => auth()->id(),
]);

$post->tags()->attach($tagIds);
$post->comments()->create([
    'user_id' => $user->id,
    'content' => 'Great post!',
]);
```

#### Khi nào sử dụng Query Builder

| Scenario | Recommendation |
|----------|----------------|
| Complex queries không cần model | **Query Builder** |
| Reports và analytics | **Query Builder** |
| Bulk operations | **Query Builder** |
| Cross-database queries | **Query Builder** |
| Aggregations và reporting | **Query Builder** |

```php
// Query Builder - Complex reporting
$report = DB::table('orders')
    ->join('order_items', 'orders.id', '=', 'order_items.order_id')
    ->join('products', 'order_items.product_id', '=', 'products.id')
    ->join('categories', 'products.category_id', '=', 'categories.id')
    ->select([
        'categories.name as category',
        DB::raw('SUM(order_items.quantity) as total_quantity'),
        DB::raw('SUM(order_items.subtotal) as total_revenue'),
        DB::raw('AVG(order_items.unit_price) as avg_price'),
        DB::raw('COUNT(DISTINCT orders.id) as order_count'),
    ])
    ->whereBetween('orders.created_at', [$startDate, $endDate])
    ->where('orders.status', 'completed')
    ->groupBy('categories.id', 'categories.name')
    ->orderByDesc('total_revenue')
    ->get();

// Complex conditional queries
$query = DB::table('orders')
    ->select('*');

if ($status) {
    $query->where('status', $status);
}

if ($dateFrom) {
    $query->where('created_at', '>=', $dateFrom);
}

if ($dateTo) {
    $query->where('created_at', '<=', $dateTo);
}

if ($minAmount) {
    $query->where('total', '>=', $minAmount);
}

$results = $query->paginate(20);
```

### Decision Matrix

| Criteria | Eloquent | Query Builder |
|----------|----------|---------------|
| Code readability | ✅ Better for OOP | ⚠️ More verbose |
| Performance | ⚠️ Slightly slower | ✅ Faster |
| Relationships | ✅ Native support | ❌ Manual joins |
| Events | ✅ Built-in | ❌ Manual |
| Complex queries | ⚠️ Can be complex | ✅ Better |
| Security | ✅ Both safe | ✅ Both safe |

---

## 3. Caching Strategy

### Câu hỏi: Bạn nên cache cái gì và bằng cách nào?

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CACHE TARGET                               │
└─────────────────────────────────────────────────────────────────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           │                     │                     │
           ▼                     ▼                     ▼
    ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
    │    Config    │      │     Data     │      │   Views      │
    │   & Routes   │      │  (Queries)   │      │  (Rendered)  │
    └──────────────┘      └──────────────┘      └──────────────┘
```

#### Cache Driver Selection

| Câu hỏi | Kết quả | Recommendation |
|---------|---------|---------------|
| Production environment? | Yes | **Redis** |
| Single server, simple needs? | Yes | **File** |
| Need distributed cache? | Yes | **Redis** |
| Already using Redis? | Yes | **Redis** |
| Development/testing? | Yes | **Array** (null) |

```php
// config/cache.php
return [
    'default' => env('CACHE_DRIVER', 'redis'),
    
    'stores' => [
        'redis' => [
            'driver' => 'redis',
            'connection' => 'cache',
            'lock_connection' => 'default',
        ],
        
        'file' => [
            'driver' => 'file',
            'path' => storage_path('framework/cache/data'),
        ],
        
        'array' => [
            'driver' => 'array',
            'serialize' => false,
        ],
    ],
];
```

#### Cache Patterns

| Pattern | Use Case | Implementation |
|---------|----------|---------------|
| **Remember** | Expensive queries | `Cache::remember()` |
| **Remember Forever** | Configuration data | `Cache::rememberForever()` |
| **Remember + Tags** | Related data | `Cache::tags(['posts'])->remember()` |
| **Cache Aside** | Read-heavy data | Manual cache management |
| **Write Through** | Data must be consistent | Write to cache + DB |
| **Write Behind** | Performance priority | Write to cache, async to DB |

```php
// Remember pattern - Most common
public function getPopularPosts(): Collection
{
    return Cache::remember(
        'posts:popular',
        now()->addMinutes(30),
        fn () => Post::popular()->limit(10)->get()
    );
}

// Cache with tags - For invalidation
public function getCategoryPosts(int $categoryId): Collection
{
    return Cache::tags(['category:' . $categoryId, 'posts'])
        ->remember(
            "category:{$categoryId}:posts",
            now()->addMinutes(15),
            fn () => Post::forCategory($categoryId)->get()
        );
}

// Invalidation
public function updatePost(Post $post): void
{
    $post->update(/* ... */);
    
    // Invalidate related caches
    Cache::tags(['posts', 'category:' . $post->category_id])->flush();
    
    // Or invalidate specific key
    Cache::forget('posts:popular');
}

// Cache::rememberForever - For config-like data
public function getSiteSettings(): array
{
    return Cache::rememberForever('settings:site', function () {
        return Setting::all()->pluck('value', 'key')->toArray();
    });
}
```

### Decision Matrix

| Data Type | TTL | Invalidation Strategy | Cache Method |
|-----------|-----|----------------------|--------------|
| User preferences | Hours | On user update | Key-based |
| Product catalog | Minutes | On product update | Tag-based |
| Popular posts | Minutes | Time-based | Remember |
| API responses | Minutes | On data change | Tags |
| Session data | Session | On logout | Driver-specific |

---

## 4. Queue Driver Selection

### Câu hỏi: Bạn nên sử dụng queue driver nào?

```
┌─────────────────────────────────────────────────────────────────────┐
│                        QUEUE REQUIREMENTS                            │
└─────────────────────────────────────────────────────────────────────┘
                                 │
           ┌─────────────────────┴─────────────────────┐
           │                                           │
           ▼                                           ▼
    ┌──────────────┐                           ┌──────────────┐
    │   High Load  │                           │  Low Volume  │
    │   (1000+/min)│                           │  (<100/min)  │
    └──────────────┘                           └──────────────┘
```

#### Driver Selection Matrix

| Criteria | Redis | Database | Sync | Beanstalkd | SQS |
|----------|-------|----------|------|------------|-----|
| Speed | ✅ Fastest | ⚠️ Medium | ✅ Instant | ⚠️ Medium | ⚠️ Medium |
| Reliability | ✅ High | ✅ High | ❌ None | ⚠️ Medium | ✅ High |
| Setup | ⚠️ Medium | ✅ Easy | ✅ Easy | ⚠️ Medium | ⚠️ Medium |
| Cost | 💰 Medium | 💰 Low | 💰 Free | 💰 Low | 💰 Pay-per-use |
| Persistence | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| Scalability | ✅ Easy | ⚠️ Hard | ❌ None | ⚠️ Medium | ✅ Easy |

```php
// config/queue.php
return [
    'default' => env('QUEUE_CONNECTION', 'redis'),
    
    'connections' => [
        'sync' => [
            'driver' => 'sync',
        ],
        
        'database' => [
            'driver' => 'database',
            'table' => 'jobs',
            'queue' => 'default',
            'retry_after' => 90,
        ],
        
        'redis' => [
            'driver' => 'redis',
            'connection' => 'default',
            'queue' => env('REDIS_QUEUE', 'default'),
            'retry_after' => 90,
            'block_for' => null,
        ],
    ],
];
```

#### Queue Configuration Recommendations

| Volume | Driver | Workers | Configuration |
|--------|--------|---------|----------------|
| Development | sync/null | N/A | `QUEUE_CONNECTION=sync` |
| Small/Medium | Redis | 2-4 | Single Redis server |
| Large | Redis/SQS | 10+ | Queue scaling |
| Enterprise | SQS | Variable | Auto-scaling workers |

```php
// Queue configuration
php artisan queue:work redis --queue=high,default,low --tries=3 --timeout=60

// Supervisor config for production
// /etc/supervisor/conf.d/laravel-worker.conf
[program:laravel-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /path/to/artisan queue:work redis --sleep=3 --tries=3 --max-time=3600
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
numprocs=4
redirect_stderr=true
stdout_logfile=/var/log/worker.log
stopwaitsecs=3600
```

---

## 5. Jobs vs Events vs Commands

### Câu hỏi: Bạn nên sử dụng cái nào?

```
┌─────────────────────────────────────────────────────────────────────┐
│                       ACTION TYPE                                    │
└─────────────────────────────────────────────────────────────────────┘
                                 │
           ┌─────────────────────┴─────────────────────┐
           │                                           │
           ▼                                           ▼
    ┌──────────────┐                           ┌──────────────┐
    │   Async/    │                           │   Sync/      │
    │   Background│                           │   Decouple   │
    └──────────────┘                           └──────────────┘
           │                                           │
           ▼                                           ▼
    ┌──────────────┐                           ┌──────────────┐
    │     Job      │                           │    Event     │
    │ (Single Task)│                           │ (Broadcast)  │
    └──────────────┘                           └──────────────┘
```

### Decision Matrix

| Action | Use Case | Pattern | Example |
|--------|----------|---------|---------|
| **Job** | Background processing, retry needed | `ShouldQueue` | Send email, Process payment, Generate PDF |
| **Event** | Notify multiple listeners, decoupling | `Event/Listener` | Order created → Send email + Update inventory + Notify vendor |
| **Command** | CLI operations | `Artisan Command` | Cleanup, Import, Export, Scheduled tasks |
| **Notification** | Multi-channel user communication | `Notification` | Password reset, Order shipped |

```php
// JOB - For background processing with retry
class ProcessPaymentJob implements ShouldQueue
{
    public int $tries = 3;
    public int $backoff = 60;

    public function handle(PaymentGateway $gateway): void
    {
        $gateway->charge($this->order->total, $this->token);
    }
}

// EVENT - For broadcasting to multiple listeners
class OrderCreated
{
    public function broadcastOn(): array
    {
        return [new Channel('orders')];
    }
}

// Event listeners
protected $listen = [
    OrderCreated::class => [
        SendOrderEmail::class,
        UpdateInventory::class,
        NotifyVendor::class,
    ],
];

// COMMAND - For CLI operations
class ImportProductsCommand extends Command
{
    public function handle(): int
    {
        // CLI logic
    }
}
```

### When to Use Each

| Scenario | Recommendation |
|----------|----------------|
| Sending email asynchronously | **Job** |
| Processing image | **Job** |
| Sending to multiple channels | **Event + Notification** |
| Decoupling components | **Event** |
| Database update triggering other actions | **Event** |
| Cron job / scheduled task | **Command** |
| User notification | **Notification** |
| External API call with retry | **Job** |

---

## 6. API Design

### Câu hỏi: Bạn nên design API như thế nào?

#### REST Conventions

| Resource | GET | POST | PUT | DELETE |
|----------|-----|------|-----|--------|
| `/posts` | List all | Create | Bulk update | Delete all |
| `/posts/{id}` | Get one | Error | Update | Delete |
| `/posts/{id}/comments` | List comments | Add comment | - | - |
| `/posts/{id}/publish` | - | Publish | - | - |

```php
// RESTful API Routes
Route::apiResource('posts', PostController::class);
Route::apiResource('posts.comments', CommentController::class)->shallow();

// Custom actions
Route::post('/posts/{post}/publish', [PostController::class, 'publish'])
    ->name('posts.publish');
Route::post('/posts/{post}/archive', [PostController::class, 'archive'])
    ->name('posts.archive');
```

#### API Versioning

| Strategy | Pros | Cons | Recommendation |
|----------|------|------|----------------|
| URL Path (`/v1/`) | Clear, easy | URL changes | ✅ **Recommended** |
| Header (`Accept: v=2`) | Clean URLs | Complex | ⚠️ Alternative |
| Query (`?version=2`) | Easy | Clutters URLs | ❌ Not recommended |

```php
// URL Versioning - Recommended
Route::prefix('v1')->group(function () {
    require base_path('routes/api_v1.php');
});

Route::prefix('v2')->group(function () {
    require base_path('routes/api_v2.php');
});

// API Routes file
// routes/api_v1.php
Route::get('/posts', [PostController::class, 'index']);
```

#### Response Format

```php
// Consistent API Response
class ApiResponse
{
    public static function success(mixed $data, string $message = null): JsonResponse
    {
        return response()->json([
            'success' => true,
            'message' => $message,
            'data' => $data,
            'timestamp' => now()->toIso8601String(),
        ]);
    }

    public static function paginated(LengthAwarePaginator $paginator, $resource): JsonResponse
    {
        return response()->json([
            'success' => true,
            'data' => $resource::collection($paginator->items()),
            'meta' => [
                'current_page' => $paginator->currentPage(),
                'last_page' => $paginator->lastPage(),
                'per_page' => $paginator->perPage(),
                'total' => $paginator->total(),
            ],
        ]);
    }

    public static function error(string $message, int $code = 400): JsonResponse
    {
        return response()->json([
            'success' => false,
            'message' => $message,
        ], $code);
    }
}
```

---

## 7. Service Layer Design

### Câu hỏi: Bạn nên organize business logic như thế nào?

```
┌─────────────────────────────────────────────────────────────────────┐
│                     APPLICATION SCALE                                │
└─────────────────────────────────────────────────────────────────────┘
                                 │
           ┌─────────────────────┴─────────────────────┐
           │                                           │
           ▼                                           ▼
    ┌──────────────┐                           ┌──────────────┐
    │   Small/    │                           │   Medium/    │
    │   Simple   │                           │   Complex    │
    └──────────────┘                           └──────────────┘
           │                                           │
           ▼                                           ▼
    ┌──────────────┐                           ┌──────────────┐
    │ Direct in   │                           │   Service    │
    │ Controller  │                           │   Layer      │
    └──────────────┘                           └──────────────┘
```

### Decision Matrix

| Application Size | Pattern | Complexity | When |
|-----------------|---------|------------|------|
| Small/Prototype | Controller + Model | Low | Simple CRUD, few endpoints |
| Medium | Service Layer | Medium | Business logic, multiple use cases |
| Large/Enterprise | Repository + Service + DTO | High | Complex domain, team collaboration |

```php
// SMALL - Direct in Controller (Simple CRUD)
class PostController extends Controller
{
    public function index(): JsonResponse
    {
        return PostResource::collection(Post::published()->paginate());
    }
    
    public function store(StorePostRequest $request): JsonResponse
    {
        $post = Post::create($request->validated());
        return (new PostResource($post))->response()->setStatusCode(201);
    }
}

// MEDIUM - Service Layer
class OrderService
{
    public function __construct(
        private OrderRepositoryInterface $orderRepository,
        private ProductRepositoryInterface $productRepository,
    ) {}
    
    public function createOrder(array $data): Order
    {
        // Business logic here
    }
}

// LARGE - Repository + Service + DTOs
// See Architecture document for full examples
```

---

## 8. Database Design

### Câu hỏi: Bạn nên sử dụng relationship type nào?

```
┌─────────────────────────────────────────────────────────────────────┐
│                     RELATIONSHIP TYPE                                │
└─────────────────────────────────────────────────────────────────────┘
                                 │
           ┌─────────────────────┴─────────────────────┐
           │                                           │
           ▼                                           ▼
    ┌──────────────┐                           ┌──────────────┐
    │   One-to-    │                           │  Many-to-    │
    │     One      │                           │    Many      │
    └──────────────┘                           └──────────────┘
           │                                           │
           ▼                                           ▼
    ┌──────────────┐                           ┌──────────────┐
    │ belongsTo/   │                           │ belongsToMany│
    │ hasOne       │                           │ pivot table  │
    └──────────────┘                           └──────────────┘
```

### Relationship Selection Guide

| Relationship | When to Use | Example |
|--------------|-------------|---------|
| **hasOne** | One record belongs to another | User → Profile |
| **belongsTo** | Inverse of hasOne | Profile → User |
| **hasMany** | One parent, many children | User → Posts |
| **belongsToMany** | Many-to-many | Posts ↔ Tags |
| **hasOneThrough** | Indirect one-to-one | User → Profile → Account |
| **hasManyThrough** | Indirect one-to-many | Country → Users → Posts |
| **morphOne** | Polymorphic one-to-one | Image → (User, Post) |
| **morphMany** | Polymorphic one-to-many | Comments → (User, Post) |

```php
// hasOne - One user has one profile
class User extends Model
{
    public function profile(): HasOne
    {
        return $this->hasOne(Profile::class);
    }
}

// hasMany - One user has many posts
class User extends Model
{
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}

// belongsToMany - Many-to-many with pivot
class Post extends Model
{
    public function tags(): BelongsToMany
    {
        return $this->belongsToMany(Tag::class)
            ->withPivot('created_at')
            ->withTimestamps();
    }
}

// Polymorphic - One model belongs to multiple types
class Image extends Model
{
    public function imageable(): MorphTo
    {
        return $this->morphTo();
    }
}

class User extends Model
{
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}

class Post extends Model
{
    public function images(): MorphMany
    {
        return $this->morphMany(Image::class, 'imageable');
    }
}
```

---

## 9. File Storage

### Câu hỏi: Bạn nên lưu trữ files ở đâu?

```
┌─────────────────────────────────────────────────────────────────────┐
│                       STORAGE TYPE                                   │
└─────────────────────────────────────────────────────────────────────┘
                                 │
           ┌─────────────────────┴─────────────────────┐
           │                                           │
           ▼                                           ▼
    ┌──────────────┐                           ┌──────────────┐
    │   Local      │                           │   Cloud      │
    └──────────────┘                           └──────────────┘
           │                                           │
           ▼                                           ▼
    ┌──────────────┐                           ┌──────────────┐
    │ Development/ │                           │  Production  │
    │ Cheap hosting│                           │ S3/R2/Azure  │
    └──────────────┘                           └──────────────┘
```

### Storage Selection Matrix

| Storage | Cost | Speed | Scalability | Use Case |
|---------|------|-------|-------------|----------|
| Local | Free | Fast (local) | ❌ Poor | Development |
| S3 | 💰 Pay | Fast | ✅ Excellent | Production, CDN |
| R2 | 💰 Pay | Fast | ✅ Excellent | Production, no egress |
| Azure Blob | 💰 Pay | Fast | ✅ Excellent | Enterprise |
| FTP | 💰 Low | ⚠️ Medium | ⚠️ Poor | Legacy systems |

```php
// config/filesystems.php
return [
    'default' => env('FILESYSTEM_DISK', 'local'),
    
    'disks' => [
        'local' => [
            'driver' => 'local',
            'root' => storage_path('app'),
            'throw' => false,
        ],
        
        'public' => [
            'driver' => 'local',
            'root' => storage_path('app/public'),
            'url' => env('APP_URL').'/storage',
            'visibility' => 'public',
        ],
        
        's3' => [
            'driver' => 's3',
            'key' => env('AWS_ACCESS_KEY_ID'),
            'secret' => env('AWS_SECRET_ACCESS_KEY'),
            'region' => env('AWS_DEFAULT_REGION'),
            'bucket' => env('AWS_BUCKET'),
            'url' => env('AWS_URL'),
            'endpoint' => env('AWS_ENDPOINT'),
        ],
    ],
];

// Usage
Storage::disk('s3')->put('avatars/1.jpg', $contents);
$url = Storage::disk('s3')->url('avatars/1.jpg');
Storage::disk('s3')->delete('avatars/1.jpg');

// Link storage for public access
php artisan storage:link
```

---

## 10. Error Handling

### Câu hỏi: Bạn nên xử lý errors như thế nào?

```
┌─────────────────────────────────────────────────────────────────────┐
│                       ERROR TYPE                                     │
└─────────────────────────────────────────────────────────────────────┘
                                 │
           ┌─────────────────────┴─────────────────────┐
           │                                           │
           ▼                                           ▼
    ┌──────────────┐                           ┌──────────────┐
    │   Web App    │                           │   API        │
    │  (HTML Page) │                           │  (JSON)      │
    └──────────────┘                           └──────────────┘
```

### Error Handling Strategy

| Application Type | Response | Handler |
|-----------------|----------|---------|
| Web App | Blade views | Exception handler → views |
| API | JSON | Exception handler → JSON |
| SPA + API | JSON | Consistent error format |

```php
// app/Exceptions/Handler.php
class Handler extends ExceptionHandler
{
    protected $dontReport = [
        ValidationException::class,
        AuthenticationException::class,
    ];

    public function render($request, Throwable $e)
    {
        if ($request->expectsJson()) {
            return $this->handleApiException($request, $e);
        }
        
        if ($e instanceof ModelNotFoundException) {
            return response()->view('errors.404', [], 404);
        }
        
        return parent::render($request, $e);
    }

    protected function handleApiException(Request $request, Throwable $e): JsonResponse
    {
        if ($e instanceof ValidationException) {
            return response()->json([
                'success' => false,
                'message' => 'Validation failed',
                'errors' => $e->errors(),
            ], 422);
        }
        
        if ($e instanceof ModelNotFoundException) {
            return response()->json([
                'success' => false,
                'message' => 'Resource not found',
            ], 404);
        }
        
        if ($e instanceof AuthenticationException) {
            return response()->json([
                'success' => false,
                'message' => 'Unauthenticated',
            ], 401);
        }
        
        // Log error for debugging
        Log::error($e);
        
        return response()->json([
            'success' => false,
            'message' => config('app.debug') ? $e->getMessage() : 'Server error',
        ], 500);
    }
}
```

---

## Quick Reference Summary

### Authentication
- **Web App** → Breeze hoặc Fortify
- **API (Simple)** → Sanctum
- **OAuth** → Passport

### Database
- **Standard CRUD** → Eloquent
- **Complex Reports** → Query Builder

### Caching
- **Production** → Redis
- **Simple** → File

### Queue
- **Production** → Redis hoặc SQS
- **Development** → Sync

### Service Layer
- **Simple App** → Direct in Controller
- **Complex App** → Service Layer

### File Storage
- **Production** → S3/R2
- **Development** → Local

## References

- [Laravel Documentation](https://laravel.com/docs)
- [Laracasts](https://laracasts.com/)
- [Laravel Best Practices](https://github.com/alexeymezenin/laravel-best-practices)
- [API Design Best Practices](https://RESTfulAPI.net/)
