---
title: "Laravel Checklist - Danh Sách Kiểm Tra"
description: "Danh sách kiểm tra toàn diện cho Laravel development, bao gồm pre-deployment checks, security audit, code review, performance optimization, và production readiness validation."
tags: ["laravel", "checklist", "deployment", "security", "code-review"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Laravel Checklist - Danh Sách Kiểm Tra

## Tổng Quan

Trước khi deploy ứng dụng Laravel lên production, có rất nhiều thứ cần kiểm tra để đảm bảo ứng dụng hoạt động ổn định, bảo mật, và có hiệu suất tốt. Checklist này cung cấp hướng dẫn chi tiết cho developers và DevOps engineers để thực hiện các bước kiểm tra cuối cùng trước khi release.

Mỗi section được thiết kế để cover một specific area của ứng dụng Laravel, từ configuration và security cho đến database và caching. Các items được đánh dấu theo mức độ ưu tiên: Critical (bắt buộc), Important (nên làm), và Optional (tùy chọn).

## Mục Đích

Tài liệu này phục vụ các mục đích:

- Pre-deployment validation checklist
- Code review guide cho team leads
- Security audit checklist
- Performance optimization verification
- Production readiness assessment
- Onboarding guide cho new developers

## Pre-Deployment Checklist

### Environment Configuration

```bash
# 1. Environment Variables
[ ] APP_ENV=production (không phải local/testing)
[ ] APP_DEBUG=false (KHÔNG ĐỂ true ở production)
[ ] APP_URL=https://correct-domain.com
[ ] DB_HOST, DB_PORT, DB_DATABASE, DB_USERNAME, DB_PASSWORD đã được set đúng
[ ] CACHE_DRIVER=redis (hoặc appropriate driver)
[ ] QUEUE_CONNECTION=redis (hoặc appropriate driver)
[ ] SESSION_DRIVER=redis (hoặc appropriate driver)
[ ] MAIL_MAILER=smtp (hoặc appropriate driver)
[ ] AWS credentials đã được configure cho production
[ ] Stripe/Payment API keys là production keys
```

```php
// config/app.php - Production Settings
return [
    'env' => env('APP_ENV', 'production'),
    'debug' => (bool) env('APP_DEBUG', false),
    'url' => env('APP_URL', 'https://example.com'),
    
    // Timezone configuration
    'timezone' => 'Asia/Ho_Chi_Minh', // Hoặc timezone của bạn
    
    // Locale
    'locale' => 'vi',
    'fallback_locale' => 'en',
    'faker_locale' => 'vi_VN',
];
```

```php
// config/logging.php - Production Log Configuration
return [
    'default' => env('LOG_CHANNEL', 'stack'),
    
    'channels' => [
        'stack' => [
            'driver' => 'stack',
            'channels' => ['daily', 'slack'],
            'ignore_exceptions' => false,
        ],
        
        'daily' => [
            'driver' => 'daily',
            'path' => storage_path('logs/laravel.log'),
            'level' => 'debug',
            'days' => 30,
        ],
        
        'slack' => [
            'driver' => 'slack',
            'url' => env('LOG_SLACK_WEBHOOK_URL'),
            'username' => 'Laravel Log',
            'emoji' => ':boom:',
            'level' => 'error',
        ],
        
        'syslog' => [
            'driver' => 'syslog',
            'level' => 'debug',
        ],
    ],
];
```

### Security Checklist

#### Authentication & Authorization

```bash
# Authentication
[ ] Sử dụng Laravel Sanctum cho API authentication
[ ] Sử dụng Laravel Breeze/Fortify cho web authentication
[ ] Password hashing sử dụng bcrypt (mặc định)
[ ] Session timeout được configured
[ ] CSRF protection enabled (mặc định)
[ ] Rate limiting cho login attempts
[ ] Account lockout after failed attempts
[ ] Password reset token expiration (1 giờ)
[ ] Email verification enabled cho new registrations
```

```php
// config/auth.php - Production Configuration
return [
    'defaults' => [
        'guard' => 'web',
        'passwords' => 'users',
    ],
    
    'guards' => [
        'web' => [
            'driver' => 'session',
            'provider' => 'users',
        ],
        
        'api' => [
            'driver' => 'sanctum',
            'provider' => 'users',
        ],
    ],
    
    'providers' => [
        'users' => [
            'driver' => 'eloquent',
            'model' => App\Models\User::class,
        ],
    ],
    
    'passwords' => [
        'users' => [
            'provider' => 'users',
            'table' => 'password_reset_tokens',
            'expire' => 60, // 1 hour
            'throttle' => 60,
        ],
    ],
    
    'password_timeout' => 10800, // 3 hours
];
```

```php
// app/Providers/AuthServiceProvider.php
class AuthServiceProvider extends ServiceProvider
{
    protected $policies = [
        Post::class => PostPolicy::class,
        Order::class => OrderPolicy::class,
    ];

    public function boot(): void
    {
        $this->registerPolicies();
        
        // Rate limiting
        RateLimiter::for('api', function (Request $request) {
            return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
        });
        
        RateLimiter::for('login', function (Request $request) {
            return Limit::perMinute(5)->by($request->ip());
        });
    }
}
```

#### Input Validation & Sanitization

```bash
# Validation
[ ] Tất cả user inputs được validated sử dụng Form Requests
[ ] Mass assignment protection với $fillable/$guarded
[ ] SQL injection prevention (Eloquent/Query Builder tự động)
[ ] XSS prevention với proper escaping trong Blade
[ ] File upload validation (type, size, dimensions)
[ ] Email validation với MX record check
[ ] URL validation cho external links
[ ] Phone number validation theo format
```

```php
// app/Http/Requests/StoreUserRequest.php
class StoreUserRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'email' => [
                'required',
                'string',
                'email',
                'max:255',
                Rule::unique('users')->whereNull('deleted_at'),
            ],
            'password' => [
                'required',
                'string',
                'min:8',
                'confirmed',
                'regex:/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/',
            ],
            'phone' => ['nullable', 'phone:VN'],
            'avatar' => ['nullable', 'image', 'max:2048', 'mimes:jpg,jpeg,png,gif'],
            'website' => ['nullable', 'url'],
        ];
    }

    public function messages(): array
    {
        return [
            'password.regex' => 'Password must contain at least one uppercase, one lowercase, and one number.',
            'phone.phone' => 'Please provide a valid phone number.',
        ];
    }
}
```

#### Security Headers

```php
// app/Http/Middleware/AddSecurityHeaders.php
class AddSecurityHeaders
{
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);
        
        $response->headers->set('X-Content-Type-Options', 'nosniff');
        $response->headers->set('X-Frame-Options', 'SAMEORIGIN');
        $response->headers->set('X-XSS-Protection', '1; mode=block');
        $response->headers->set('Referrer-Policy', 'strict-origin-when-cross-origin');
        $response->headers->set('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');
        $response->headers->set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
        
        return $response;
    }
}

// app/Http/Kernel.php
protected $middlewareAliases = [
    // ...
    'security.headers' => \App\Http\Middleware\AddSecurityHeaders::class,
    'verified' => \Illuminate\Auth\Middleware\EnsureEmailIsVerified::class,
];
```

### Database Checklist

```bash
# Migrations
[ ] Tất cả migrations đã được run thành công
[ ] Database backup đã được tạo trước khi migrate
[ ] Indexes đã được tạo cho các columns thường query
[ ] Foreign keys đã được set với appropriate ON DELETE actions
[ ] Soft deletes được sử dụng cho các tables có delete operations
[ ] Timestamps có default values
```

```php
// database/migrations/2024_01_01_000001_create_orders_table.php
class CreateOrdersTable extends Migration
{
    public function up(): void
    {
        Schema::create('orders', function (Blueprint $table) {
            $table->id();
            $table->uuid('uuid')->unique();
            
            $table->foreignId('user_id')
                ->constrained()
                ->cascadeOnDelete();
            
            $table->string('order_number', 20)->unique();
            $table->string('status', 30)->index();
            
            $table->decimal('subtotal', 12, 2);
            $table->decimal('tax', 10, 2)->default(0);
            $table->decimal('shipping', 10, 2)->default(0);
            $table->decimal('total', 12, 2);
            
            $table->json('shipping_address');
            $table->json('meta')->nullable();
            
            $table->timestamps();
            $table->softDeletes();
            
            // Composite indexes
            $table->index(['user_id', 'created_at']);
            $table->index(['status', 'created_at']);
        });
    }
}
```

```bash
# Query Performance
[ ] EXPLAIN đã được chạy trên tất cả slow queries
[ ] N+1 queries đã được fix với eager loading
[ ] Appropriate indexes đã được tạo
[ ] Query caching đã được implement cho expensive queries
[ ] Database connection pooling được configured
```

```sql
-- Kiểm tra slow queries
SHOW VARIABLES LIKE 'slow_query_log';
SHOW VARIABLES LIKE 'long_query_time';

-- EXPLAIN example
EXPLAIN ANALYZE 
SELECT * FROM orders 
WHERE status = 'pending' 
AND created_at > '2024-01-01'
ORDER BY created_at DESC
LIMIT 20;
```

### API Development Checklist

```bash
# API Design
[ ] API routes được đặt trong routes/api.php
[ ] API versioning được implement (/v1, /v2)
[ ] API Resources được sử dụng cho response transformation
[ ] Consistent response format (JSON structure)
[ ] Proper HTTP status codes được sử dụng
[ ] Pagination được implement cho list endpoints
[ ] API documentation (OpenAPI/Swagger) đã được tạo
```

```php
// routes/api.php
Route::prefix('v1')->group(function () {
    // Public routes
    Route::get('/products', [ProductController::class, 'index']);
    Route::get('/products/{product}', [ProductController::class, 'show']);
    
    // Authenticated routes
    Route::middleware('auth:sanctum')->group(function () {
        Route::get('/user', fn (Request $request) => $request->user());
        
        Route::apiResource('orders', OrderController::class)->middleware('verified');
        
        Route::post('/logout', [AuthController::class, 'logout']);
    });
    
    // Rate limited routes
    Route::middleware('throttle:60,1')->group(function () {
        Route::post('/contact', [ContactController::class, 'store']);
    });
});
```

```php
// app/Http/Resources/ApiResponse.php
class ApiResponse
{
    public static function success(mixed $data = null, string $message = null, int $code = 200): JsonResponse
    {
        return response()->json([
            'success' => true,
            'message' => $message,
            'data' => $data,
            'timestamp' => now()->toIso8601String(),
        ], $code);
    }

    public static function error(string $message, int $code = 400, array $errors = []): JsonResponse
    {
        $response = [
            'success' => false,
            'message' => $message,
            'errors' => $errors,
            'timestamp' => now()->toIso8601String(),
        ];
        
        return response()->json($response, $code);
    }

    public static function paginated(LengthAwarePaginator $paginator, JsonResource $resource): JsonResponse
    {
        return response()->json([
            'success' => true,
            'data' => $resource->collection($paginator->items()),
            'meta' => [
                'current_page' => $paginator->currentPage(),
                'last_page' => $paginator->lastPage(),
                'per_page' => $paginator->perPage(),
                'total' => $paginator->total(),
            ],
            'links' => [
                'first' => $paginator->url(1),
                'last' => $paginator->url($paginator->lastPage()),
                'prev' => $paginator->previousPageUrl(),
                'next' => $paginator->nextPageUrl(),
            ],
        ]);
    }
}
```

### Performance Checklist

```bash
# Caching
[ ] Config caching: php artisan config:cache
[ ] Route caching: php artisan route:cache
[ ] View caching: php artisan view:cache
[ ] Application bootstrap caching
[ ] Appropriate cache TTLs được set
[ ] Cache invalidation strategy đã được implement
```

```bash
# Optimize Commands
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan optimize:clear
php artisan optimize

# Composer Optimization
composer install --optimize-autoloader --no-dev
```

```php
// bootstrap/app.php
$app = new Application(
    $_ENV['APP_BASE_PATH'] ?? dirname(__DIR__)
);

$app->useStoragePath($app->storagePath());

// Production optimizations
if ($app->environment('production')) {
    $app->bootstrapPath('bootstrap/production.php');
}
```

```bash
# Queue & Background Jobs
[ ] Queue driver đã được set (Redis recommended)
[ ] Queue workers đang chạy với Supervisor
[ ] Failed job table đã được tạo
[ ] Job retry policy đã được configured
[ ] Job timeout appropriately set
[ ] Queue monitoring đã được setup
```

```bash
# Create failed_jobs table
php artisan queue:failed-table
php artisan migrate

# Create jobs table if using database queue
php artisan queue:table
php artisan migrate
```

```php
// config/queue.php
return [
    'default' => env('QUEUE_CONNECTION', 'redis'),
    
    'connections' => [
        'redis' => [
            'driver' => 'redis',
            'connection' => 'default',
            'queue' => env('REDIS_QUEUE', 'default'),
            'retry_after' => 90,
            'block_for' => null,
        ],
    ],
    
    'failed' => [
        'driver' => 'database-uuids',
        'database' => 'mysql',
        'table' => 'failed_jobs',
    ],
];
```

### File Structure Checklist

```bash
# Directories
[ ] storage/app/public tồn tại và có symlink
[ ] bootstrap/cache có write permissions
[ ] storage/logs có write permissions
[ ] All vendor directories tồn tại
```

```bash
# Create storage symlink
php artisan storage:link

# Set permissions (Linux/Mac)
chmod -R 775 storage
chmod -R 775 bootstrap/cache
chown -R www-data:www-data storage
chown -R www-data:www-data bootstrap/cache
```

### Testing Checklist

```bash
# Unit Tests
[ ] Tất cả Models có unit tests
[ ] Tất cả Services có unit tests
[ ] Helper functions có unit tests
[ ] Edge cases đã được covered
[ ] Test coverage > 80% cho critical paths
```

```bash
# Run Tests
php artisan test                    # All tests
php artisan test --coverage         # With coverage report
php artisan test --parallel         # Parallel execution
```

```php
// tests/Unit/Services/OrderServiceTest.php
class OrderServiceTest extends TestCase
{
    use RefreshDatabase;

    private OrderService $orderService;

    protected function setUp(): void
    {
        parent::setUp();
        $this->orderService = app(OrderService::class);
    }

    public function test_create_order_creates_order_with_items(): void
    {
        $user = User::factory()->create();
        $product = Product::factory()->create(['price' => 100]);
        
        $order = $this->orderService->createOrder($user->id, [
            ['product_id' => $product->id, 'quantity' => 2],
        ]);
        
        $this->assertInstanceOf(Order::class, $order);
        $this->assertEquals(200, $order->total);
        $this->assertCount(1, $order->items);
    }

    public function test_create_order_fails_with_insufficient_stock(): void
    {
        $this->expectException(InsufficientStockException::class);
        
        $user = User::factory()->create();
        $product = Product::factory()->create(['stock' => 1]);
        
        $this->orderService->createOrder($user->id, [
            ['product_id' => $product->id, 'quantity' => 5],
        ]);
    }

    public function test_cancel_order_releases_stock(): void
    {
        $order = Order::factory()->hasItems(2)->create();
        $initialStock = $order->items->first()->product->stock;
        
        $this->orderService->cancelOrder($order);
        
        $this->assertEquals($initialStock + $order->items->first()->quantity, 
            $order->items->first()->product->fresh()->stock);
    }
}
```

```bash
# Feature Tests
[ ] Tất cả API endpoints có feature tests
[ ] Authentication flows có tests
[ ] Authorization policies có tests
[ ] Form validation có tests
[ ] Error handling có tests
```

```php
// tests/Feature/Api/OrderApiTest.php
class OrderApiTest extends TestCase
{
    use RefreshDatabase;

    public function test_authenticated_user_can_create_order(): void
    {
        $user = User::factory()->create();
        $product = Product::factory()->create(['price' => 100]);
        
        $response = $this->actingAs($user, 'sanctum')
            ->postJson('/api/v1/orders', [
                'items' => [
                    ['product_id' => $product->id, 'quantity' => 2],
                ],
                'shipping_address' => [
                    'street' => '123 Main St',
                    'city' => 'HCMC',
                    'country' => 'VN',
                    'postal_code' => '70000',
                ],
                'payment_method' => 'credit_card',
            ]);
        
        $response->assertCreated()
            ->assertJsonStructure([
                'data' => ['id', 'order_number', 'total'],
            ]);
        
        $this->assertDatabaseHas('orders', [
            'user_id' => $user->id,
            'total' => 200,
        ]);
    }

    public function test_unauthenticated_user_cannot_create_order(): void
    {
        $response = $this->postJson('/api/v1/orders', [
            'items' => [['product_id' => 1, 'quantity' => 1]],
        ]);
        
        $response->assertUnauthorized();
    }

    public function test_order_creation_validates_required_fields(): void
    {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user, 'sanctum')
            ->postJson('/api/v1/orders', []);
        
        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['items', 'shipping_address']);
    }
}
```

### Error Handling Checklist

```bash
# Exception Handling
[ ] Custom exception handlers đã được configured
[ ] User-friendly error pages đã được tạo
[ ] 404, 500 error pages tùy chỉnh
[ ] API error responses nhất quán
[ ] Logging cho all exceptions
```

```php
// app/Exceptions/Handler.php
class Handler extends ExceptionHandler
{
    protected $dontReport = [
        ValidationException::class,
        AuthenticationException::class,
        AuthorizationException::class,
    ];

    protected $dontFlash = [
        'current_password',
        'password',
        'password_confirmation',
    ];

    public function register(): void
    {
        $this->reportable(function (Throwable $e) {
            if (app()->bound('sentry')) {
                app('sentry')->captureException($e);
            }
        });
    }

    public function render($request, Throwable $e)
    {
        if ($request->expectsJson()) {
            return $this->handleApiException($request, $e);
        }
        
        if ($e instanceof ModelNotFoundException) {
            return response()->view('errors.404', [], 404);
        }
        
        if ($e instanceof HttpExceptionInterface) {
            return response()->view("errors.{$e->getStatusCode()}", [], $e->getStatusCode());
        }
        
        return response()->view('errors.500', [], 500);
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
        
        if ($e instanceof AuthorizationException) {
            return response()->json([
                'success' => false,
                'message' => 'Unauthorized',
            ], 403);
        }
        
        Log::error($e);
        
        return response()->json([
            'success' => false,
            'message' => config('app.debug') ? $e->getMessage() : 'Server error',
        ], 500);
    }
}
```

### Monitoring & Logging Checklist

```bash
# Logging
[ ] Application logs được write vào production log files
[ ] Error logs được gửi đến centralized logging service
[ ] Sensitive data được redact trong logs
[ ] Log rotation được configured
[ ] Structured logging được implement
```

```php
// config/logging.php - Structured Logging
'channels' => [
    'stack' => [
        'driver' => 'stack',
        'channels' => ['daily'],
        'ignore_exceptions' => false,
    ],
    
    'daily' => [
        'driver' => 'daily',
        'path' => storage_path('logs/laravel.log'),
        'level' => 'debug',
        'days' => 30,
        'formatter' => Monolog\Formatter\JsonFormatter::class,
    ],
],
```

```php
// Sử dụng structured logging
Log::info('Order created', [
    'order_id' => $order->id,
    'customer_id' => $order->customer_id,
    'total' => $order->total,
    'items_count' => $order->items->count(),
]);

Log::error('Payment failed', [
    'order_id' => $order->id,
    'error' => $exception->getMessage(),
    'user_id' => $request->user()?->id,
]);
```

### Deployment Verification

```bash
# Pre-Deployment
[ ] All tests pass locally và CI/CD
[ ] Database migrations đã được tested
[ ] Environment variables đã được verified
[ ] SSL certificates đã được renewed
[ ] Backup strategy đã được tested
[ ] Rollback plan đã được documented
```

```bash
# Deployment Commands Sequence
composer install --optimize-autoloader --no-dev
php artisan migrate --force
php artisan db:seed --force  # If needed
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan optimize
php artisan storage:link
php artisan queue:restart
```

```bash
# Post-Deployment
[ ] Application responds correctly
[ ] Database connections work
[ ] Cache works properly
[ ] Queue workers running
[ ] Scheduled jobs configured
[ ] CDN/assets loading correctly
[ ] Error monitoring active
```

### Cron Jobs & Scheduled Tasks

```bash
# Scheduler
[ ] Schedule đã được configured trong Kernel
[ ] Cron entry đã được added vào server
[ ] Các scheduled tasks chạy đúng schedule
[ ] Cleanup tasks đã được scheduled
```

```php
// app/Console/Kernel.php
class Kernel extends ConsoleKernel
{
    protected function schedule(Schedule $schedule): void
    {
        // Hourly tasks
        $schedule->job(new ProcessPendingOrdersJob())->hourly();
        $schedule->command('queue:prune-failed')->hourly();
        
        // Daily tasks
        $schedule->command('backup:run --only-db')->dailyAt('01:00');
        $schedule->command('reports:generate')->dailyAt('02:00');
        $schedule->job(new CleanupExpiredSessionsJob())->daily();
        
        // Weekly tasks
        $schedule->command('cache:prune-stale-tags')->weekly();
        $schedule->job(new GenerateWeeklyReportJob())->weeklyOn(1, '08:00');
        
        // Monthly tasks
        $schedule->command('reports:generate-monthly')->monthlyOn(1, '03:00');
    }

    protected function commands(): void
    {
        $this->load(__DIR__.'/Commands');
    }
}
```

```bash
# Crontab entry
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1

# Hoặc Supervisor config
[program:laravel-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /path-to-your-project/artisan queue:work redis --sleep=3 --tries=3 --max-time=3600
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
user=www-data
numprocs=4
redirect_stderr=true
stdout_logfile=/var/log/worker.log
stopwaitsecs=3600
```

### Backup & Disaster Recovery

```bash
# Backup
[ ] Automated database backups configured
[ ] File backups configured
[ ] Backup retention policy defined
[ ] Backup encryption enabled
[ ] Backup restoration tested
[ ] Backup monitoring active
```

```php
// config/backup.php
return [
    'backup' => [
        'name' => env('APP_NAME', 'laravel'),
        
        'source' => [
            'files' => [
                include: base_path('*'),
                exclude: [
                    base_path('vendor'),
                    base_path('node_modules'),
                    '.git',
                ],
            ],
            
            'databases' => [
                'mysql',
            ],
        ],
        
        'destination' => [
            'filename_prefix' => 'backup_',
            'filename_suffix' => '',
            
            'disks' => [
                's3',
            ],
        ],
        
        'deletion' => [
            'keep' => [
                'daily' => 7,
                'weekly' => 4,
                'monthly' => 6,
                'yearly' => 2,
            ],
        ],
    ],
];
```

## Code Review Checklist

### Architecture

```bash
[ ] Single Responsibility - mỗi class có một trách nhiệm rõ ràng
[ ] Dependency Injection được sử dụng thay vì hard-coded dependencies
[ ] Service layer tách biệt business logic
[ ] Repository pattern được sử dụng cho data access
[ ] Events được sử dụng cho decoupled communication
[ ] No god classes hoặc god methods
```

### Code Quality

```bash
[ ] PSR-12 coding standard được tuân thủ
[ ] Meaningful variable và method names
[ ] Proper PHPDoc comments cho public methods
[ ] No commented out code
[ ] No TODO comments trong production code
[ ] No debug code (dd, dump, print_r)
[ ] Proper error handling với try-catch
[ ] Type hints được sử dụng
[ ] Return types được khai báo
```

```php
// Good Example với Type Hints và Return Types
class OrderCalculationService
{
    /**
     * Calculate order totals including tax and shipping.
     *
     * @param Collection<int, array{product_id: int, quantity: int}> $items
     * @return array{subtotal: float, tax: float, shipping: float, total: float}
     */
    public function calculateTotals(Collection $items, string $country): array
    {
        $subtotal = $this->calculateSubtotal($items);
        $tax = $this->calculateTax($subtotal, $country);
        $shipping = $this->calculateShipping($subtotal, $country);
        
        return [
            'subtotal' => round($subtotal, 2),
            'tax' => round($tax, 2),
            'shipping' => round($shipping, 2),
            'total' => round($subtotal + $tax + $shipping, 2),
        ];
    }
}
```

### Security Review

```bash
[ ] No SQL injection vulnerabilities
[ ] XSS prevention với proper escaping
[ ] CSRF protection enabled
[ ] Mass assignment protection
[ ] File upload security
[ ] Authentication properly implemented
[ ] Authorization properly implemented
[ ] No hardcoded secrets
[ ] Sensitive data not logged
[ ] API rate limiting
```

### Performance Review

```bash
[ ] No N+1 queries
[ ] Appropriate indexes exist
[ ] Caching được sử dụng cho expensive operations
[ ] Lazy loading vs eager loading properly chosen
[ ] No unnecessary queries trong loops
[ ] Pagination cho large datasets
[ ] Query optimization với EXPLAIN
```

### Testing Review

```bash
[ ] Unit tests cho Services/Repositories
[ ] Feature tests cho Controllers/Endpoints
[ ] Test coverage adequate
[ ] Tests are isolated và independent
[ ] Fixtures/factories used correctly
[ ] Assertions are meaningful
[ ] Edge cases covered
```

## Final Production Checklist

```bash
# Core Application
[ ] APP_ENV=production
[ ] APP_DEBUG=false
[ ] APP_KEY đã được generated
[ ] Config cache đã được cleared và recached
[ ] Route cache đã được generated
[ ] View cache đã được generated
[ ] All vendor dependencies installed --no-dev

# Database
[ ] All migrations have been run
[ ] Database indexes created
[ ] Database backup configured
[ ] Connection pooling configured

# Cache & Queue
[ ] Cache driver configured (Redis)
[ ] Queue driver configured (Redis)
[ ] Session driver configured
[ ] Queue workers running với Supervisor

# Security
[ ] SSL/TLS enabled
[ ] Security headers configured
[ ] CSRF protection enabled
[ ] CORS configured properly
[ ] Rate limiting configured

# Monitoring
[ ] Error tracking configured (Sentry, Bugsnag)
[ ] APM configured (New Relic, Scout)
[ ] Log aggregation configured
[ ] Uptime monitoring configured

# CDN & Assets
[ ] Assets compiled (npm run production)
[ ] CDN configured
[ ] Storage symlinks created
[ ] Asset versioning configured

# Backup & Recovery
[ ] Automated backups configured
[ ] Backup retention configured
[ ] Recovery procedures documented
[ ] Backup restoration tested
```

## References

- [Laravel Deployment Documentation](https://laravel.com/docs/deployment)
- [Laravel Security Documentation](https://laravel.com/docs/security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Laravel Envoy](https://laravel.com/docs/envoy) - Deployment tool
- [Laravel Forge](https://forge.laravel.com/) - Server management
