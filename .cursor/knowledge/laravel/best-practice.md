---
title: "Laravel Best Practices - Thực Hành Tốt Nhất Laravel"
description: "Tài liệu tổng hợp các best practices cho Laravel development, bao gồm Service classes, Repository pattern, Job queues, Form Requests, Policy authorization, và nhiều hơn nữa để xây dựng ứng dụng Laravel chuyên nghiệp."
tags: ["laravel", "best-practices", "architecture", "php", "web-development"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Laravel Best Practices - Thực Hành Tốt Nhất Laravel

## Tổng Quan

Laravel là một trong những PHP frameworks phổ biến nhất hiện nay, cung cấp elegant syntax và powerful features cho việc xây dựng web applications. Tuy nhiên, để tận dụng tối đa potential của Laravel, developers cần tuân thủ các best practices được khuyến nghị bởi cộng đồng và Laravel core team.

Tài liệu này tổng hợp các best practices đã được kiểm chứng trong production environments, giúp bạn xây dựng ứng dụng Laravel có khả năng mở rộng, dễ bảo trì, và hiệu suất cao. Các practices được phân loại theo các areas khác nhau của ứng dụng Laravel.

## Mục Đích

Tài liệu này nhằm:

- Cung cấp hướng dẫn comprehensive về Laravel best practices
- Giúp developers tạo ra code chất lượng cao từ đầu
- Standardize development workflow trong team
- Reduce technical debt và improve maintainability
- Optimize performance và security

## Key Concepts

### 1. Separation of Concerns

Mỗi layer trong ứng dụng nên có trách nhiệm rõ ràng: Controllers handle HTTP requests/responses, Services chứa business logic, Repositories handle data access, Models represent domain entities.

### 2. Dependency Injection

Sử dụng constructor injection để make dependencies explicit, improve testability, và reduce coupling giữa các components.

### 3. Convention Over Configuration

Tuân thủ Laravel's conventions để leverage built-in features và make code predictable cho team members.

### 4. Defensive Programming

Validate input thoroughly, handle edge cases, và provide meaningful error messages.

## Best Practices

### 1. Controller Best Practices

#### Thin Controllers

Controllers nên mỏng nhất có thể, chỉ handle request/response và delegate business logic sang services.

```php
// ✅ GOOD: Thin Controller
class OrderController extends Controller
{
    public function __construct(
        private OrderService $orderService,
        private OrderResource $orderResource,
    ) {}

    public function index(Request $request): JsonResponse
    {
        $orders = $this->orderService->getOrdersForUser(
            $request->user(),
            $request->validated()
        );
        
        return $this->orderResource->collection($orders);
    }

    public function store(CreateOrderRequest $request): JsonResponse
    {
        $order = $this->orderService->createOrder(
            $request->user(),
            $request->validated()
        );
        
        return response()->json([
            'message' => 'Order created successfully',
            'order' => new OrderResource($order),
        ], 201);
    }

    public function show(Request $request, Order $order): JsonResponse
    {
        $this->authorize('view', $order);
        
        return new OrderResource(
            $this->orderService->loadOrderDetails($order)
        );
    }

    public function update(UpdateOrderRequest $request, Order $order): JsonResponse
    {
        $this->authorize('update', $order);
        
        $order = $this->orderService->updateOrder($order, $request->validated());
        
        return new OrderResource($order);
    }

    public function destroy(Request $request, Order $order): JsonResponse
    {
        $this->authorize('delete', $order);
        
        $this->orderService->cancelOrder($order);
        
        return response()->json(null, 204);
    }
}
```

#### Resource Controllers

Sử dụng Resource Controllers cho CRUD operations để maintain consistency.

```php
// app/Http/Controllers/Api/ProductController.php
class ProductController extends Controller
{
    public function __construct(
        private ProductService $productService,
        private ProductResource $productResource,
    ) {}

    public function index(ProductIndexRequest $request): JsonResponse
    {
        $products = $this->productService->getProducts($request->validated());
        
        return $this->productResource->collection($products);
    }

    public function store(CreateProductRequest $request): JsonResponse
    {
        $product = $this->productService->createProduct($request->validated());
        
        return (new ProductResource($product))
            ->response()
            ->setStatusCode(201);
    }

    public function show(Product $product): JsonResponse
    {
        return new ProductResource($product->load(['category', 'tags', 'images']));
    }

    public function update(UpdateProductRequest $request, Product $product): JsonResponse
    {
        $product = $this->productService->updateProduct($product, $request->validated());
        
        return new ProductResource($product);
    }

    public function destroy(Product $product): JsonResponse
    {
        $this->productService->deleteProduct($product);
        
        return response()->json(null, 204);
    }
}

// routes/api.php
Route::apiResource('products', ProductController::class);
```

### 2. Form Request Validation

Sử dụng Form Request classes cho validation thay vì inline validation trong controllers.

```php
// app/Http/Requests/CreateOrderRequest.php
class CreateOrderRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Order::class);
    }

    public function rules(): array
    {
        return [
            'items' => ['required', 'array', 'min:1'],
            'items.*.product_id' => [
                'required',
                'integer',
                Rule::exists('products', 'id')->where(function ($query) {
                    $query->where('is_active', true);
                }),
            ],
            'items.*.quantity' => [
                'required',
                'integer',
                'min:1',
                'max:100',
            ],
            'shipping_address' => ['required', 'array'],
            'shipping_address.street' => ['required', 'string', 'max:255'],
            'shipping_address.city' => ['required', 'string', 'max:100'],
            'shipping_address.country' => ['required', 'string', 'size:2'],
            'shipping_address.postal_code' => ['required', 'string', 'max:20'],
            'payment_method' => [
                'required',
                Rule::in(array_keys(config('payment.methods'))),
            ],
            'notes' => ['nullable', 'string', 'max:1000'],
        ];
    }

    public function withValidator(Validator $validator): void
    {
        $validator->after(function ($validator) {
            if ($this->hasDuplicateProducts()) {
                $validator->errors()->add('items', 'Duplicate products are not allowed');
            }
        });
    }

    public function messages(): array
    {
        return [
            'items.*.product_id.exists' => 'The selected product is not available.',
            'items.*.quantity.max' => 'Maximum quantity per item is 100.',
        ];
    }

    protected function hasDuplicateProducts(): bool
    {
        $productIds = array_column($this->input('items'), 'product_id');
        return count($productIds) !== count(array_unique($productIds));
    }
}
```

### 3. Service Classes

```php
// app/Services/OrderService.php
class OrderService
{
    public function __construct(
        private OrderRepositoryInterface $orderRepository,
        private ProductRepositoryInterface $productRepository,
        private InventoryService $inventoryService,
        private PaymentService $paymentService,
        private NotificationService $notificationService,
        private EventDispatcher $events,
    ) {}

    public function getOrdersForUser(User $user, array $filters = []): LengthAwarePaginator
    {
        return $this->orderRepository->getForUser($user, [
            'customer',
            'items.product',
            'shipping',
        ])->paginate($filters['per_page'] ?? 15);
    }

    public function createOrder(User $user, array $data): Order
    {
        $this->validateOrderItems($data['items']);
        
        return DB::transaction(function () use ($user, $data) {
            $order = $this->orderRepository->create([
                'customer_id' => $user->id,
                'status' => OrderStatus::PENDING,
                'notes' => $data['notes'] ?? null,
                'shipping_address' => $data['shipping_address'],
            ]);
            
            $items = $this->prepareOrderItems($order, $data['items']);
            
            $this->inventoryService->reserveStock($items);
            
            $this->orderRepository->attachItems($order, $items);
            
            $order->calculateTotals();
            
            $this->events->dispatch(new OrderCreated($order));
            
            return $order->load(['items.product', 'shipping']);
        }, 5);
    }

    public function updateOrder(Order $order, array $data): Order
    {
        $this->authorize('update', $order);
        
        if ($order->isLocked()) {
            throw new OrderLockedException('Cannot update locked order');
        }
        
        return $this->orderRepository->update($order, $data);
    }

    public function cancelOrder(Order $order, string $reason = null): Order
    {
        $this->authorize('cancel', $order);
        
        return DB::transaction(function () use ($order, $reason) {
            $order = $this->orderRepository->updateStatus($order, OrderStatus::CANCELLED);
            
            $this->inventoryService->releaseStock($order->items);
            
            $this->notificationService->sendOrderCancelledNotification($order, $reason);
            
            $this->events->dispatch(new OrderCancelled($order));
            
            return $order;
        });
    }

    public function loadOrderDetails(Order $order): Order
    {
        return $this->orderRepository->findWithDetails($order->id);
    }

    protected function validateOrderItems(array $items): void
    {
        foreach ($items as $item) {
            $product = $this->productRepository->find($item['product_id']);
            
            if (!$product->isAvailable()) {
                throw new ProductUnavailableException($product);
            }
            
            if ($product->stock < $item['quantity']) {
                throw new InsufficientStockException($product, $item['quantity']);
            }
        }
    }

    protected function prepareOrderItems(Order $order, array $items): Collection
    {
        return collect($items)->map(function ($item) {
            $product = $this->productRepository->find($item['product_id']);
            
            return [
                'product_id' => $product->id,
                'quantity' => $item['quantity'],
                'unit_price' => $product->current_price,
                'subtotal' => $product->current_price * $item['quantity'],
            ];
        });
    }
}
```

### 4. Repository Pattern

```php
// app/Repositories/Contracts/BaseRepositoryInterface.php
interface BaseRepositoryInterface
{
    public function find(int $id): ?Model;
    public function findOrFail(int $id): Model;
    public function all(): Collection;
    public function create(array $data): Model;
    public function update(Model $model, array $data): Model;
    public function delete(Model $model): bool;
    public function paginate(int $perPage = 15): LengthAwarePaginator;
}

// app/Repositories/Contracts/OrderRepositoryInterface.php
interface OrderRepositoryInterface extends BaseRepositoryInterface
{
    public function getForUser(User $user, array $relations = []): Builder;
    public function findWithDetails(int $id): ?Order;
    public function attachItems(Order $order, Collection $items): void;
    public function updateStatus(Order $order, string $status): Order;
}

// app/Repositories/Eloquent/BaseRepository.php
abstract class BaseRepository implements BaseRepositoryInterface
{
    protected Model $model;

    public function __construct(Model $model)
    {
        $this->model = $model;
    }

    public function find(int $id): ?Model
    {
        return $this->model->find($id);
    }

    public function findOrFail(int $id): Model
    {
        return $this->model->findOrFail($id);
    }

    public function all(): Collection
    {
        return $this->model->all();
    }

    public function create(array $data): Model
    {
        return $this->model->create($data);
    }

    public function update(Model $model, array $data): Model
    {
        $model->update($data);
        return $model->fresh();
    }

    public function delete(Model $model): bool
    {
        return $model->delete();
    }

    public function paginate(int $perPage = 15): LengthAwarePaginator
    {
        return $this->model->paginate($perPage);
    }

    protected function query(): Builder
    {
        return $this->model->newQuery();
    }
}

// app/Repositories/Eloquent/OrderRepository.php
class OrderRepository extends BaseRepository implements OrderRepositoryInterface
{
    protected Order $model;

    public function __construct(Order $model)
    {
        parent::__construct($model);
    }

    public function getForUser(User $user, array $relations = []): Builder
    {
        return $this->query()
            ->where('customer_id', $user->id)
            ->with($relations)
            ->latest();
    }

    public function findWithDetails(int $id): ?Order
    {
        return $this->query()
            ->with([
                'customer',
                'items.product.category',
                'items.product.images',
                'shipping',
                'payments',
                'notes',
            ])
            ->find($id);
    }

    public function attachItems(Order $order, Collection $items): void
    {
        $order->items()->createMany($items->toArray());
    }

    public function updateStatus(Order $order, string $status): Order
    {
        $order->status = $status;
        $order->save();
        
        return $order;
    }
}
```

### 5. Eloquent Model Best Practices

```php
// app/Models/Order.php
class Order extends Model
{
    use HasFactory, HasUuids, SoftDeletes;
    
    protected $table = 'orders';
    protected $guarded = ['id', 'created_at', 'updated_at'];
    
    protected $casts = [
        'total_amount' => 'decimal:2',
        'shipping_address' => 'array',
        'paid_at' => 'datetime',
        'shipped_at' => 'datetime',
        'meta' => 'array',
    ];
    
    protected $dates = ['created_at', 'updated_at', 'deleted_at'];
    
    // Relationships
    public function customer(): BelongsTo
    {
        return $this->belongsTo(Customer::class);
    }

    public function items(): HasMany
    {
        return $this->hasMany(OrderItem::class);
    }

    public function shipping(): MorphOne
    {
        return $this->shipping()->morphOne(Shipping::class, 'shippable');
    }

    public function payments(): HasMany
    {
        return $this->hasMany(Payment::class);
    }

    // Scopes
    public function scopePending($query)
    {
        return $query->where('status', OrderStatus::PENDING);
    }

    public function scopeCompleted($query)
    {
        return $query->where('status', OrderStatus::COMPLETED);
    }

    public function scopeForDateRange($query, $start, $end)
    {
        return $query->whereBetween('created_at', [$start, $end]);
    }

    // Accessors & Mutators
    public function getFormattedTotalAttribute(): string
    {
        return number_format($this->total_amount, 2);
    }

    public function setTotalAmountAttribute($value): void
    {
        $this->attributes['total_amount'] = round($value, 2);
    }

    // Methods
    public function calculateTotals(): void
    {
        $this->total_amount = $this->items->sum('subtotal');
        $this->save();
    }

    public function isLocked(): bool
    {
        return in_array($this->status, [
            OrderStatus::SHIPPED,
            OrderStatus::DELIVERED,
            OrderStatus::CANCELLED,
        ]);
    }

    public function isPending(): bool
    {
        return $this->status === OrderStatus::PENDING;
    }

    // Events
    protected static function booted(): void
    {
        static::creating(function (Order $order) {
            if (empty($order->order_number)) {
                $order->order_number = OrderNumberGenerator::generate();
            }
        });

        static::saved(function (Order $order) {
            if ($order->wasRecentlyCreated) {
                event(new OrderCreatedEvent($order));
            }
        });
    }
}
```

### 6. Job Queue Best Practices

```php
// app/Jobs/ProcessPaymentJob.php
class ProcessPaymentJob implements ShouldQueue, ShouldBeUnique
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $maxExceptions = 2;
    public int $backoff = 60;
    public int $timeout = 120;
    
    public uniqueFor = 3600;

    public function __construct(
        public Order $order,
        public string $paymentToken,
        public array $paymentDetails,
    ) {
        $this->onQueue('payments');
        $this->onConnection('redis');
    }

    public function uniqueId(): string
    {
        return $this->order->id;
    }

    public function tags(): array
    {
        return [
            'order:' . $this->order->id,
            'payment',
            'customer:' . $this->order->customer_id,
        ];
    }

    public function handle(PaymentGateway $gateway): void
    {
        if ($this->order->isPaid()) {
            $this->delete();
            return;
        }

        $result = $gateway->charge(
            $this->order->total_amount,
            $this->paymentToken,
            $this->paymentDetails
        );

        if ($result->isSuccessful()) {
            $this->order->markAsPaid($result->getReference());
            
            SendOrderConfirmationJob::dispatch($this->order);
            GenerateInvoiceJob::dispatch($this->order);
            NotifyVendorJob::dispatch($this->order);
        } else {
            $this->order->markPaymentFailed($result->getErrorMessage());
            
            $this->release(300);
        }
    }

    public function failed(Throwable $exception): void
    {
        $this->order->markPaymentFailed($exception->getMessage());
        
        NotifyAdminJob::dispatch(
            "Payment processing failed for order {$this->order->order_number}",
            [
                'order_id' => $this->order->id,
                'error' => $exception->getMessage(),
            ]
        );
    }

    public function retryUntil(): DateTime
    {
        return now()->addHours(24);
    }
}

// app/Jobs/SendOrderConfirmationJob.php
class SendOrderConfirmationJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 5;
    public int $backoff = 30;

    public function __construct(
        #[DispatchableAfterCommit]
        public Order $order,
    ) {
        $this->onQueue('notifications');
    }

    public function handle(MailerInterface $mailer): void
    {
        $mailer->to($this->order->customer->email)
            ->send(new OrderConfirmationMail($this->order));
    }
}
```

### 7. Policy Authorization

```php
// app/Policies/OrderPolicy.php
class OrderPolicy
{
    public function before(User $user, string $ability): ?bool
    {
        if ($user->isAdmin()) {
            return true;
        }
        
        return null;
    }

    public function view(User $user, Order $order): bool
    {
        return $user->id === $order->customer_id || $user->isStaff();
    }

    public function create(User $user): bool
    {
        return !$user->isBanned() && $user->hasVerifiedEmail();
    }

    public function update(User $user, Order $order): bool
    {
        if ($order->isLocked()) {
            return false;
        }
        
        return $user->id === $order->customer_id || $user->isStaff();
    }

    public function delete(User $user, Order $order): bool
    {
        if (!$order->isPending()) {
            return false;
        }
        
        return $user->id === $order->customer_id;
    }

    public function cancel(User $user, Order $order): bool
    {
        if (!$order->canBeCancelled()) {
            return false;
        }
        
        return $user->id === $order->customer_id || $user->isStaff();
    }

    public function refund(User $user, Order $order): bool
    {
        return $user->isAdmin() && $order->isPaid();
    }

    public function export(User $user): bool
    {
        return $user->isAdmin() || $user->isStaff();
    }
}

// app/Providers/AuthServiceProvider.php
class AuthServiceProvider extends ServiceProvider
{
    protected $policies = [
        Order::class => OrderPolicy::class,
        Product::class => ProductPolicy::class,
        User::class => UserPolicy::class,
    ];

    public function boot(): void
    {
        Gate::define('export-orders', [OrderPolicy::class, 'export']);
        Gate::define('bulk-actions', fn ($user) => $user->isAdmin());
    }
}
```

### 8. API Resources

```php
// app/Http/Resources/OrderResource.php
class OrderResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'order_number' => $this->order_number,
            'status' => $this->status,
            'status_label' => $this->status_label,
            'total_amount' => $this->total_amount,
            'formatted_total' => $this->formatted_total,
            'currency' => $this->currency,
            'item_count' => $this->items_count,
            'customer' => new CustomerBriefResource($this->whenLoaded('customer')),
            'items' => OrderItemResource::collection($this->whenLoaded('items')),
            'shipping_address' => $this->shipping_address,
            'tracking_url' => $this->when(
                $this->shipment?->tracking_number,
                fn () => $this->shipment->tracking_url
            ),
            'created_at' => $this->created_at->toIso8601String(),
            'updated_at' => $this->updated_at->toIso8601String(),
            'can_cancel' => $this->when(
                $request->user(),
                fn () => $request->user()->can('cancel', $this->resource)
            ),
        ];
    }

    public function with(Request $request): array
    {
        return [
            'meta' => [
                'currency' => config('app.currency'),
                'timezone' => $request->user()?->timezone ?? config('app.timezone'),
            ],
        ];
    }
}

// app/Http/Resources/OrderItemResource.php
class OrderItemResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'product' => new ProductBriefResource($this->whenLoaded('product')),
            'product_name' => $this->product_name,
            'quantity' => $this->quantity,
            'unit_price' => $this->unit_price,
            'formatted_unit_price' => $this->formatted_unit_price,
            'subtotal' => $this->subtotal,
            'formatted_subtotal' => $this->formatted_subtotal,
        ];
    }
}
```

### 9. Database Indexes và Migrations

```php
// database/migrations/2024_01_01_000001_create_orders_table.php
class CreateOrdersTable extends Migration
{
    public function up(): void
    {
        Schema::create('orders', function (Blueprint $table) {
            $table->id();
            $table->uuid('uuid')->unique();
            $table->string('order_number', 20)->unique();
            
            $table->foreignId('customer_id')
                ->constrained()
                ->cascadeOnDelete();
            
            $table->string('status', 20)->index();
            $table->decimal('total_amount', 12, 2);
            $table->string('currency', 3)->default('USD');
            
            $table->json('shipping_address');
            $table->json('billing_address')->nullable();
            
            $table->text('notes')->nullable();
            $table->json('meta')->nullable();
            
            $table->timestamps();
            $table->softDeletes();
            
            // Indexes for common queries
            $table->index(['customer_id', 'created_at']);
            $table->index(['status', 'created_at']);
            $table->index(['status', 'customer_id']);
            $table->index('paid_at');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('orders');
    }
}
```

### 10. Event-Driven Architecture

```php
// app/Events/OrderCreated.php
class OrderCreated implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public int $tries = 3;

    public function __construct(
        public Order $order,
    ) {}

    public function broadcastAs(): string
    {
        return 'order.created';
    }

    public function broadcastWith(): array
    {
        return [
            'order_id' => $this->order->id,
            'order_number' => $this->order->order_number,
            'total' => $this->order->total_amount,
            'customer_id' => $this->order->customer_id,
        ];
    }

    public function broadcastOn(): array
    {
        return [
            new PrivateChannel('customer.' . $this->order->customer_id),
            new Channel('admin.orders'),
        ];
    }
}

// app/Listeners/SendOrderNotifications.php
class SendOrderNotifications implements ShouldQueue
{
    use Queueable;

    public int $tries = 3;

    public function __construct(
        private MailerInterface $mailer,
        private SmsService $smsService,
    ) {}

    public function handle(OrderCreated $event): void
    {
        $this->mailer->to($event->order->customer->email)
            ->send(new OrderConfirmationMail($event->order));
        
        if ($event->order->customer->wants_sms_notifications) {
            $this->smsService->send(
                $event->order->customer->phone,
                "Your order {$event->order->order_number} has been placed!"
            );
        }
    }

    public function failed(OrderCreated $event, Throwable $exception): void
    {
        Log::error('Failed to send order notifications', [
            'order_id' => $event->order->id,
            'error' => $exception->getMessage(),
        ]);
    }
}

// app/Providers/EventServiceProvider.php
class EventServiceProvider extends ServiceProvider
{
    protected $listen = [
        OrderCreated::class => [
            SendOrderNotifications::class,
            UpdateInventoryListener::class,
            NotifyVendorListener::class,
            CreateShippingLabelJob::class,
        ],
    ];

    public function shouldDiscoverEvents(): bool
    {
        return $this->app->environment('local', 'testing');
    }
}
```

## Common Patterns

### 1. Query Builder vs Eloquent

```php
// Khi nào dùng Eloquent:
// - CRUD operations với models có relationships
// - Model events và observers
// - Scopes và accessors
// - Single model operations

// Khi nào dùng Query Builder:
// - Complex queries không cần model
// - Reports và analytics
// - Bulk operations
// - Cross-database queries

// Ví dụ Query Builder cho report
public function getSalesReport(Carbon $startDate, Carbon $endDate): array
{
    return DB::table('orders')
        ->join('order_items', 'orders.id', '=', 'order_items.order_id')
        ->join('products', 'order_items.product_id', '=', 'products.id')
        ->join('categories', 'products.category_id', '=', 'categories.id')
        ->select([
            'categories.name as category',
            DB::raw('SUM(order_items.quantity) as total_quantity'),
            DB::raw('SUM(order_items.subtotal) as total_revenue'),
            DB::raw('AVG(order_items.unit_price) as avg_price'),
        ])
        ->whereBetween('orders.created_at', [$startDate, $endDate])
        ->where('orders.status', OrderStatus::COMPLETED)
        ->groupBy('categories.id', 'categories.name')
        ->orderByDesc('total_revenue')
        ->get()
        ->toArray();
}
```

### 2. Caching Strategies

```php
// Cache Service
class CacheService
{
    public function remember(string $key, callable $callback, int $ttl = 3600): mixed
    {
        return Cache::remember($key, $ttl, $callback);
    }

    public function rememberForever(string $key, callable $callback): mixed
    {
        return Cache::rememberForever($key, $callback);
    }

    public function invalidate(string $key): bool
    {
        return Cache::forget($key);
    }

    public function invalidatePattern(string $pattern): int
    {
        $keys = Cache::getStore()->getPrefix() . $pattern;
        return Cache::flush();
    }
}

// Model Cache
class CategoryService
{
    public function __construct(
        private CategoryRepositoryInterface $categoryRepository,
        private CacheService $cache,
    ) {}

    public function getAllCategories(): Collection
    {
        return $this->cache->rememberForever(
            'categories:all',
            fn () => $this->categoryRepository->all()
        );
    }

    public function getCategoryWithProducts(int $id): Category
    {
        return $this->cache->remember(
            "categories:{$id}:with_products",
            fn () => $this->categoryRepository->findWithProducts($id),
            config('cache.categories_ttl', 3600)
        );
    }

    public function invalidateCategoryCache(int $id): void
    {
        $this->cache->invalidate("categories:{$id}:with_products");
        $this->cache->invalidate('categories:all');
    }
}
```

## Troubleshooting

### Common Issues và Solutions

```php
// 1. Memory Issues với Large Datasets
// Sử dụng chunking thay vì get()
Order::chunk(1000, function ($orders) {
    foreach ($orders as $order) {
        // process order
    }
});

// Hoặc cursor() cho iterator-based processing
foreach (Order::cursor() as $order) {
    // process order - memory efficient
}

// 2. Slow Queries
// Sử dụng explain()
DB::enableQueryLog();
$orders = Order::with(['customer', 'items'])->get();
Log::info(DB::getQueryLog());

// 3. Model Events not Firing
// Kiểm tra event discovery trong EventServiceProvider
public function shouldDiscoverEvents(): bool
{
    return true; // hoặc list explicit events
}
```

## Examples

### Complete Service Layer Example

```php
// 1. Interface
interface ProductServiceInterface
{
    public function getProducts(array $filters): LengthAwarePaginator;
    public function getProduct(int $id): Product;
    public function createProduct(array $data): Product;
    public function updateProduct(Product $product, array $data): Product;
    public function deleteProduct(Product $product): bool;
    public function syncCategories(Product $product, array $categoryIds): void;
}

// 2. Implementation
class ProductService implements ProductServiceInterface
{
    public function __construct(
        private ProductRepositoryInterface $productRepository,
        private CategoryRepositoryInterface $categoryRepository,
        private ImageService $imageService,
        private SearchService $searchService,
        private EventDispatcher $events,
    ) {}

    public function getProducts(array $filters): LengthAwarePaginator
    {
        $query = $this->productRepository->query();
        
        if (isset($filters['category'])) {
            $query->forCategory($filters['category']);
        }
        
        if (isset($filters['search'])) {
            $query->search($filters['search']);
        }
        
        if (isset($filters['price_min'])) {
            $query->where('price', '>=', $filters['price_min']);
        }
        
        if (isset($filters['price_max'])) {
            $query->where('price', '<=', $filters['price_max']);
        }
        
        if (isset($filters['status'])) {
            $query->where('status', $filters['status']);
        }
        
        return $query->with(['category', 'images'])
            ->paginate($filters['per_page'] ?? 15);
    }

    public function getProduct(int $id): Product
    {
        return $this->productRepository->findWithRelations($id);
    }

    public function createProduct(array $data): Product
    {
        return DB::transaction(function () use ($data) {
            $product = $this->productRepository->create([
                'name' => $data['name'],
                'slug' => Str::slug($data['name']),
                'description' => $data['description'] ?? null,
                'price' => $data['price'],
                'category_id' => $data['category_id'],
                'status' => $data['status'] ?? ProductStatus::DRAFT,
            ]);
            
            if (isset($data['images'])) {
                $this->imageService->attachImages($product, $data['images']);
            }
            
            if (isset($data['tags'])) {
                $product->syncTags($data['tags']);
            }
            
            $this->searchService->indexProduct($product);
            $this->events->dispatch(new ProductCreated($product));
            
            return $product;
        });
    }

    public function updateProduct(Product $product, array $data): Product
    {
        return DB::transaction(function () use ($product, $data) {
            $product = $this->productRepository->update($product, [
                'name' => $data['name'] ?? $product->name,
                'description' => $data['description'] ?? $product->description,
                'price' => $data['price'] ?? $product->price,
                'category_id' => $data['category_id'] ?? $product->category_id,
                'status' => $data['status'] ?? $product->status,
            ]);
            
            if (isset($data['images'])) {
                $this->imageService->syncImages($product, $data['images']);
            }
            
            $this->searchService->updateProductIndex($product);
            $this->events->dispatch(new ProductUpdated($product));
            
            return $product->fresh(['category', 'images', 'tags']);
        });
    }

    public function deleteProduct(Product $product): bool
    {
        return DB::transaction(function () use ($product) {
            $this->searchService->removeProductFromIndex($product);
            $product->images()->delete();
            $product->tags()->detach();
            
            $deleted = $this->productRepository->delete($product);
            
            if ($deleted) {
                $this->events->dispatch(new ProductDeleted($product));
            }
            
            return $deleted;
        });
    }

    public function syncCategories(Product $product, array $categoryIds): void
    {
        $product->categories()->sync($categoryIds);
        $this->events->dispatch(new ProductCategoriesUpdated($product));
    }
}

// 3. Binding trong ServiceProvider
class AppServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app->singleton(ProductServiceInterface::class, ProductService::class);
        $this->app->singleton(OrderServiceInterface::class, OrderService::class);
    }
}
```

## References

- [Laravel Documentation](https://laravel.com/docs)
- [Laracasts](https://laracasts.com/)
- [Laravel Best Practices GitHub](https://github.com/alexeymezenin/laravel-best-practices)
- [PHP-FIG Standards](https://www.php-fig.org/)
- [Laravel API Documentation](https://laravel.com/api/)
