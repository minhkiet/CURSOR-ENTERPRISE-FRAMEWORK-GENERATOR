---
title: "Laravel Architecture - Kiến Trúc Laravel"
description: "Tài liệu chi tiết về Laravel architecture patterns bao gồm Service Container, Service Providers, Repository pattern, Event-driven architecture, và các mẫu thiết kế khác cho ứng dụng Laravel enterprise."
tags: ["laravel", "architecture", "design-patterns", "enterprise", "php"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Laravel Architecture - Kiến Trúc Laravel

## Tổng Quan

Laravel là một PHP framework được thiết kế với kiến trúc MVC (Model-View-Controller) nhưng có thể mở rộng để hỗ trợ các patterns phức tạp hơn cho enterprise applications. Tài liệu này trình bày chi tiết về các architecture patterns phổ biến trong Laravel development, từ Service Container và Service Providers cho đến Repository Pattern, Event-driven architecture, và các mẫu thiết kế nâng cao khác.

Việc hiểu rõ các thành phần kiến trúc cốt lõi của Laravel không chỉ giúp developers sử dụng framework hiệu quả hơn mà còn mở ra khả năng tùy chỉnh và mở rộng ứng dụng theo nhu cầu business. Mỗi pattern được trình bày với lý do tại sao nên sử dụng, cách implement, và các trade-offs cần cân nhắc.

## Mục Đích

Tài liệu này nhằm mục đích:

- Giải thích các thành phần kiến trúc cốt lõi của Laravel
- Hướng dẫn implement các design patterns trong Laravel
- So sánh các approaches khác nhau và khi nào nên sử dụng
- Cung cấp examples production-ready cho mỗi pattern
- Giúp architects và senior developers design scalable systems

## Key Concepts

### 1. Service Container (IoC Container)

Service Container là core của Laravel's dependency injection system. Nó quản lý class dependencies và thực hiện dependency injection một cách tự động.

### 2. Service Providers

Service Providers là nơi bootstrap các services của ứng dụng, đăng ký bindings, và configure application behavior.

### 3. Facades

Facades cung cấp static-like interface đến services trong container, nhưng thực tế là proxies đến underlying objects.

### 4. Contracts (Interfaces)

Contracts là tập hợp các interfaces định nghĩa core services của framework, giúp maintain loose coupling.

## Service Container

### Dependency Injection Fundamentals

```php
// Constructor Injection - most common
class OrderService
{
    public function __construct(
        private OrderRepositoryInterface $orderRepository,
        private ProductRepositoryInterface $productRepository,
        private PaymentGateway $paymentGateway,
        private EventDispatcher $events,
    ) {}
}

// Property Injection
class InvoiceGenerator
{
    #[Inject]
    protected PDFGenerator $pdfGenerator;
    
    #[Inject]
    protected MailerInterface $mailer;
}

// Method Injection
class OrderController extends Controller
{
    public function processPayment(
        Request $request,
        #[Autowired] PaymentService $paymentService,
    ) {
        // ...
    }
}
```

### Binding và Resolution

```php
// app/Providers/AppServiceProvider.php
class AppServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        // Binding interface to implementation
        $this->app->bind(
            OrderRepositoryInterface::class,
            EloquentOrderRepository::class
        );
        
        // Singleton binding - same instance every time
        $this->app->singleton(
            ConfigService::class,
            function ($app) {
                return new ConfigService($app['config']);
            }
        );
        
        // Instance binding - bind existing instance
        $this->app->instance(StripeClient::class, $stripeClient);
        
        // Contextual binding - different implementations for different contexts
        $this->app->when(AdminOrderController::class)
            ->needs(OrderRepositoryInterface::class)
            ->give(AdminOrderRepository::class);
        
        // Primitive injection
        $this->app->when(EmailNotifier::class)
            ->needs('$fromAddress')
            ->give(config('mail.from.address'));
        
        // Tags - group related bindings
        $this->app->tag([
            ReportGeneratorInterface::class,
            MonthlyReportGenerator::class,
            AnnualReportGenerator::class,
        ], 'reports');
    }
}

// Resolution
$orderService = $this->app->make(OrderService::class);
// hoặc
$orderService = app(OrderService::class);
```

### Automatic Resolution

```php
// Laravel tự động resolve dependencies nếu chúng có type hints
class UserController extends Controller
{
    // Laravel sẽ tự động inject UserService
    public function __construct(
        private UserService $userService,
        // Và resolve từ container
        private LoggerInterface $logger,
    ) {}
    
    public function show(User $user)
    {
        // User model được route model binding tự động inject
        return $this->userService->getUserProfile($user);
    }
}
```

### Extending the Container

```php
// Extending bindings với 'extend'
$this->app->extend(OrderService::class, function ($service, $app) {
    return new OrderServiceDecorator($service, $app->make('logger'));
});

// Container events
$this->app->resolving(function ($object, $app) {
    // Called when any object is resolved
});

$this->app->resolving(OrderService::class, function ($orderService, $app) {
    // Called when OrderService is resolved
});
```

## Service Providers

### Structure và Lifecycle

```php
// app/Providers/AppServiceProvider.php
class AppServiceProvider extends ServiceProvider
{
    /**
     * Register services.
     * Được gọi trước khi services được boot
     * Chỉ nên register bindings, không nên có side effects
     */
    public function register(): void
    {
        // Register service bindings
        $this->app->singleton(OrderServiceInterface::class, OrderService::class);
        
        // Register config files
        $this->mergeConfigFrom(
            __DIR__ . '/../../config/services.php',
            'services'
        );
    }

    /**
     * Bootstrap services.
     * Được gọi sau khi all providers đã được registered
     * Đặt routes, views, middleware ở đây
     */
    public function boot(): void
    {
        // Load views
        $this->loadViewsFrom(
            __DIR__ . '/../../resources/views',
            'admin'
        );
        
        // Load translations
        $this->loadTranslationsFrom(
            __DIR__ . '/../../lang',
            'admin'
        );
        
        // Publish assets
        $this->publishes([
            __DIR__ . '/../../resources/admin-assets' => public_path('vendor/admin'),
        ], 'admin-assets');
        
        // Register commands
        if ($this->app->runningInConsole()) {
            $this->commands([
                SetupCommand::class,
                SeedDemoDataCommand::class,
            ]);
        }
    }
}
```

### Deferred Service Providers

```php
// Deferred providers chỉ load khi cần thiết
// app/Providers/PaymentServiceProvider.php
class PaymentServiceProvider extends ServiceProvider implements DeferrableProvider
{
    public function register(): void
    {
        $this->app->singleton(PaymentGatewayInterface::class, function ($app) {
            return new StripeGateway(
                config('services.stripe.secret'),
                config('services.stripe.webhook_secret')
            );
        });
    }

    public function provides(): array
    {
        return [
            PaymentGatewayInterface::class,
        ];
    }
}

// Đăng ký trong config/app.php
'providers' => [
    // ...
    App\Providers\PaymentServiceProvider::class,
],
```

### Creating Custom Service Provider

```php
// app/Providers/RepositoryServiceProvider.php
class RepositoryServiceProvider extends ServiceProvider
{
    protected array $repositories = [
        UserRepositoryInterface::class => EloquentUserRepository::class,
        ProductRepositoryInterface::class => EloquentProductRepository::class,
        OrderRepositoryInterface::class => EloquentOrderRepository::class,
        CategoryRepositoryInterface::class => EloquentCategoryRepository::class,
    ];

    public function register(): void
    {
        foreach ($this->repositories as $interface => $implementation) {
            $this->app->bind($interface, $implementation);
        }
    }

    public function boot(): void
    {
        //
    }
}
```

## Repository Pattern

### Overview

Repository Pattern tạo abstraction layer giữa data access logic và business logic, giúp code dễ test hơn và maintain hơn.

### Interface Definition

```php
// app/Repositories/Contracts/BaseRepositoryInterface.php
interface BaseRepositoryInterface
{
    /**
     * Find entity by ID
     */
    public function find(int $id): ?Model;
    
    /**
     * Find entity by ID or throw exception
     */
    public function findOrFail(int $id): Model;
    
    /**
     * Get all entities
     */
    public function all(array $columns = ['*']): Collection;
    
    /**
     * Create new entity
     */
    public function create(array $data): Model;
    
    /**
     * Update entity
     */
    public function update(Model $model, array $data): Model;
    
    /**
     * Delete entity
     */
    public function delete(Model $model): bool;
    
    /**
     * Get paginated results
     */
    public function paginate(int $perPage = 15): LengthAwarePaginator;
    
    /**
     * Query builder
     */
    public function query(): Builder;
}

// app/Repositories/Contracts/OrderRepositoryInterface.php
interface OrderRepositoryInterface extends BaseRepositoryInterface
{
    /**
     * Get orders for specific user with relations
     */
    public function forUser(User $user): Builder;
    
    /**
     * Get orders by status
     */
    public function byStatus(string $status): Builder;
    
    /**
     * Find order with all details
     */
    public function findWithDetails(int $id): ?Order;
    
    /**
     * Get orders within date range
     */
    public function betweenDates(Carbon $start, Carbon $end): Builder;
    
    /**
     * Get recent orders
     */
    public function recent(int $limit = 10): Collection;
}
```

### Eloquent Implementation

```php
// app/Repositories/Eloquent/BaseRepository.php
abstract class BaseRepository implements BaseRepositoryInterface
{
    protected Model $model;
    protected array $relations = [];

    public function __construct(Model $model)
    {
        $this->model = $model;
    }

    public function find(int $id): ?Model
    {
        return $this->query()->find($id);
    }

    public function findOrFail(int $id): Model
    {
        return $this->query()->findOrFail($id);
    }

    public function all(array $columns = ['*']): Collection
    {
        return $this->query()->get($columns);
    }

    public function create(array $data): Model
    {
        return $this->model->create($data);
    }

    public function update(Model $model, array $data): Model
    {
        $model->update($data);
        return $model->fresh($this->relations);
    }

    public function delete(Model $model): bool
    {
        return $model->delete();
    }

    public function paginate(int $perPage = 15): LengthAwarePaginator
    {
        return $this->query()->paginate($perPage);
    }

    public function query(): Builder
    {
        $query = $this->model->newQuery();
        
        if (!empty($this->relations)) {
            $query->with($this->relations);
        }
        
        return $query;
    }

    protected function applyDefaultOrdering(Builder $query): Builder
    {
        return $query->latest();
    }
}

// app/Repositories/Eloquent/OrderRepository.php
class OrderRepository extends BaseRepository implements OrderRepositoryInterface
{
    protected array $relations = [
        'customer',
        'items.product',
        'shipping',
    ];

    protected Order $model;

    public function __construct(Order $model)
    {
        $this->model = $model;
    }

    public function forUser(User $user): Builder
    {
        return $this->query()
            ->where('customer_id', $user->id);
    }

    public function byStatus(string $status): Builder
    {
        return $this->query()
            ->where('status', $status);
    }

    public function findWithDetails(int $id): ?Order
    {
        return $this->query()
            ->with([
                'customer:id,name,email,phone',
                'items:id,order_id,product_id,quantity,unit_price,subtotal',
                'items.product:id,name,sku,image',
                'items.product.category:id,name',
                'shipping',
                'payments',
                'notes',
            ])
            ->find($id);
    }

    public function betweenDates(Carbon $start, Carbon $end): Builder
    {
        return $this->query()
            ->whereBetween('created_at', [$start, $end]);
    }

    public function recent(int $limit = 10): Collection
    {
        return $this->query()
            ->with('customer:id,name')
            ->limit($limit)
            ->get();
    }
}
```

### Repository Binding

```php
// app/Providers/RepositoryServiceProvider.php
class RepositoryServiceProvider extends ServiceProvider
{
    protected array $repositoryBindings = [
        UserRepositoryInterface::class => EloquentUserRepository::class,
        ProductRepositoryInterface::class => EloquentProductRepository::class,
        OrderRepositoryInterface::class => EloquentOrderRepository::class,
        CategoryRepositoryInterface::class => EloquentCategoryRepository::class,
    ];

    public function register(): void
    {
        foreach ($this->repositoryBindings as $interface => $implementation) {
            $this->app->bind($interface, $implementation);
        }
    }

    public function provides(): array
    {
        return array_keys($this->repositoryBindings);
    }
}
```

## Event-Driven Architecture

### Event Discovery và Registration

```php
// app/Providers/EventServiceProvider.php
class EventServiceProvider extends ServiceProvider
{
    /**
     * The event handler mappings for the application.
     */
    protected $listen = [
        // Explicit event-listener mapping
        OrderCreated::class => [
            SendOrderConfirmationListener::class,
            UpdateInventoryListener::class,
            NotifyVendorListener::class,
        ],
        
        OrderPaid::class => [
            ProcessFulfillmentListener::class,
            GenerateInvoiceListener::class,
            UpdateAnalyticsListener::class,
        ],
        
        UserRegistered::class => [
            SendWelcomeEmailListener::class,
            CreateUserProfileListener::class,
            AssignDefaultRoleListener::class,
        ],
    ];

    /**
     * Register any events for your application.
     */
    public function boot(): void
    {
        parent::boot();
    }

    /**
     * Determine if events and listeners should be automatically discovered.
     */
    public function shouldDiscoverEvents(): bool
    {
        return $this->app->environment('local', 'testing');
    }
}
```

### Event Classes

```php
// app/Events/OrderCreated.php
class OrderCreated implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public int $tries = 3;
    
    public function __construct(
        public Order $order,
        public ?User $createdBy = null,
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
            'created_at' => $this->order->created_at->toIso8601String(),
        ];
    }

    public function broadcastOn(): array
    {
        return [
            new PrivateChannel('user.' . $this->order->customer_id),
            new Channel('admin.orders'),
        ];
    }

    public function tags(): array
    {
        return [
            'order:' . $this->order->id,
            'customer:' . $this->order->customer_id,
        ];
    }
}

// app/Events/OrderStatusChanged.php
class OrderStatusChanged
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public function __construct(
        public Order $order,
        public string $previousStatus,
        public string $newStatus,
        public ?User $changedBy = null,
    ) {}

    public function hasTransitionedTo(string $status): bool
    {
        return $this->newStatus === $status;
    }

    public function wasChangedBy(User $user): bool
    {
        return $this->changedBy?->id === $user->id;
    }
}
```

### Listeners

```php
// app/Listeners/SendOrderConfirmationListener.php
class SendOrderConfirmationListener implements ShouldQueue
{
    use Queueable;

    public int $tries = 3;
    public int $backoff = 60;

    public function __construct(
        private MailerInterface $mailer,
        private SmsService $smsService,
    ) {}

    public function handle(OrderCreated $event): void
    {
        // Send email
        $this->mailer->to($event->order->customer->email)
            ->send(new OrderConfirmationMail($event->order));

        // Send SMS if enabled
        if ($event->order->customer->prefers_sms) {
            $this->smsService->sendOrderConfirmation($event->order);
        }
    }

    public function failed(OrderCreated $event, Throwable $e): void
    {
        Log::error('Failed to send order confirmation', [
            'order_id' => $event->order->id,
            'error' => $e->getMessage(),
        ]);
        
        // Dispatch job to retry later
        RetrySendOrderConfirmation::dispatch($event->order)->delay(now()->addMinutes(5));
    }

    public function shouldQueue(OrderCreated $event): bool
    {
        return !$event->order->isTestOrder();
    }
}

// app/Listeners/UpdateInventoryListener.php
class UpdateInventoryListener implements ShouldQueue
{
    use Queueable;

    public int $tries = 3;

    public function __construct(
        private InventoryService $inventoryService,
    ) {}

    public function handle(OrderCreated $event): void
    {
        foreach ($event->order->items as $item) {
            $this->inventoryService->reserveStock(
                $item->product_id,
                $item->quantity,
                "Order #{$event->order->order_number}"
            );
        }
    }
}
```

### Event Subscriber

```php
// app/Listeners/OrderEventSubscriber.php
class OrderEventSubscriber
{
    public function subscribe($events): array
    {
        return [
            OrderCreated::class => 'onOrderCreated',
            OrderPaid::class => 'onOrderPaid',
            OrderShipped::class => 'onOrderShipped',
            OrderDelivered::class => 'onOrderDelivered',
            OrderCancelled::class => 'onOrderCancelled',
        ];
    }

    public function onOrderCreated(OrderCreated $event): void
    {
        // Process order creation
    }

    public function onOrderPaid(OrderPaid $event): void
    {
        // Process payment confirmation
    }

    public function onOrderShipped(OrderShipped $event): void
    {
        // Notify customer about shipping
    }

    public function onOrderDelivered(OrderDelivered $event): void
    {
        // Request review, update metrics
    }

    public function onOrderCancelled(OrderCancelled $event): void
    {
        // Release inventory, process refund if needed
    }
}

// Register in EventServiceProvider
public function boot(): void
{
    parent::boot();
    
    $subscriber = $this->app->make(OrderEventSubscriber::class);
    $this->app['events']->subscribe($subscriber);
}
```

## Command Pattern (Jobs)

### Job Structure

```php
// app/Jobs/ProcessPaymentJob.php
class ProcessPaymentJob implements ShouldQueue, ShouldBeUnique
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $maxExceptions = 2;
    public int $timeout = 120;
    public int $backoff = 60;

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
        return 'payment_' . $this->order->id;
    }

    public function tags(): array
    {
        return [
            'order:' . $this->order->id,
            'customer:' . $this->order->customer_id,
            'payments',
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
            event(new OrderPaid($this->order));
        } else {
            $this->order->markPaymentFailed($result->getErrorMessage());
            throw new PaymentFailedException($result->getErrorMessage());
        }
    }

    public function failed(Throwable $exception): void
    {
        event(new PaymentProcessingFailed($this->order, $exception));
    }

    public function retryUntil(): DateTime
    {
        return now()->addHours(24);
    }
}
```

### Job Middleware

```php
// app/Jobs/Middleware/RateLimitedJob.php
class RateLimitedJob
{
    public function handle($job, $next): void
    {
        $ limiter = app(RateLimiter::class);
        
        $key = 'job:' . get_class($job);
        
        if ($limiter->tooManyAttempts($key, 10)) {
            $job->release(60);
            return;
        }
        
        $limiter->hit($key, 60);
        
        $next($job);
    }
}

// app/Jobs/Middleware/LogJobExecution.php
class LogJobExecution
{
    public function handle($job, $next): void
    {
        $startTime = microtime(true);
        
        $next($job);
        
        Log::info('Job executed', [
            'job' => get_class($job),
            'attempts' => $job->attempts(),
            'duration' => round(microtime(true) - $startTime, 2),
        ]);
    }
}

// Apply middleware to job
class ProcessPaymentJob implements ShouldQueue
{
    public Middleware $middleware = [
        new RateLimitedJob(),
        new LogJobExecution(),
    ];
}
```

## Observer Pattern

```php
// app/Observers/OrderObserver.php
class OrderObserver
{
    public function creating(Order $order): void
    {
        if (empty($order->order_number)) {
            $order->order_number = OrderNumberGenerator::generate();
        }
    }

    public function created(Order $order): void
    {
        // Dispatch event
        event(new OrderCreated($order));
        
        // Send notification
        if (!$order->isTestOrder()) {
            NotifyAdminOfNewOrder::dispatch($order);
        }
    }

    public function updating(Order $order): void
    {
        if ($order->isDirty('status')) {
            $previousStatus = $order->getOriginal('status');
            event(new OrderStatusChanged($order, $previousStatus, $order->status));
        }
    }

    public function updated(Order $order): void
    {
        // Cache invalidation
        Cache::forget("order:{$order->id}");
        Cache::forget("customer:{$order->customer_id}:orders");
    }

    public function deleted(Order $order): void
    {
        // Cleanup related data
        $order->items()->delete();
        $order->notes()->delete();
        
        // Clear caches
        Cache::forget("order:{$order->id}");
    }

    public function restored(Order $order): void
    {
        $order->items()->restore();
        $order->notes()->restore();
    }

    public function forceDeleted(Order $order): void
    {
        // Permanent cleanup
    }
}

// Register observer
// app/Providers/AppServiceProvider.php
class AppServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        Order::observe(OrderObserver::class);
        Product::observe(ProductObserver::class);
        User::observe(UserObserver::class);
    }
}
```

## Strategy Pattern

```php
// app/Services/Shipping/Contracts/ShippingStrategy.php
interface ShippingStrategy
{
    public function calculate(float $weight, string $destination): ShippingRate;
    
    public function getDeliveryDate(string $destination): Carbon;
    
    public function isAvailable(string $destination): bool;
    
    public function getName(): string;
}

// app/Services/Shipping/Strategies/StandardShipping.php
class StandardShipping implements ShippingStrategy
{
    public function __construct(
        private array $rates = [],
    ) {}

    public function calculate(float $weight, string $destination): ShippingRate
    {
        $baseRate = $this->rates[$destination] ?? 10.00;
        $weightRate = $weight * 0.50;
        
        return new ShippingRate(
            amount: $baseRate + $weightRate,
            currency: 'USD',
            estimatedDays: 5-7
        );
    }

    public function getDeliveryDate(string $destination): Carbon
    {
        return now()->addBusinessDays(7);
    }

    public function isAvailable(string $destination): bool
    {
        return in_array($destination, array_keys($this->rates));
    }

    public function getName(): string
    {
        return 'Standard Shipping';
    }
}

// app/Services/Shipping/Strategies/ExpressShipping.php
class ExpressShipping implements ShippingStrategy
{
    public function calculate(float $weight, string $destination): ShippingRate
    {
        $baseRate = 25.00;
        $weightRate = $weight * 1.00;
        
        return new ShippingRate(
            amount: $baseRate + $weightRate,
            currency: 'USD',
            estimatedDays: 1-2
        );
    }

    public function getDeliveryDate(string $destination): Carbon
    {
        return now()->addBusinessDays(2);
    }

    public function isAvailable(string $destination): bool
    {
        return true; // Available everywhere
    }

    public function getName(): string
    {
        return 'Express Shipping';
    }
}

// app/Services/Shipping/ShippingService.php
class ShippingService
{
    protected array $strategies = [];

    public function registerStrategy(ShippingStrategy $strategy): self
    {
        $this->strategies[$strategy->getName()] = $strategy;
        return $this;
    }

    public function calculate(string $strategyName, float $weight, string $destination): ShippingRate
    {
        $strategy = $this->strategies[$strategyName] ?? throw new InvalidArgumentException(
            "Strategy not found: {$strategyName}"
        );
        
        if (!$strategy->isAvailable($destination)) {
            throw new ShippingNotAvailableException($destination);
        }
        
        return $strategy->calculate($weight, $destination);
    }

    public function getAvailableStrategies(string $destination): array
    {
        return collect($this->strategies)
            ->filter(fn ($strategy) => $strategy->isAvailable($destination))
            ->map(fn ($strategy) => [
                'name' => $strategy->getName(),
                'rate' => $strategy->calculate(0, $destination),
            ])
            ->values()
            ->toArray();
    }
}
```

## CQRS Alternative (Lightweight)

```php
// Mặc dù Laravel không có built-in CQRS, có thể implement lightweight version

// app/Commands/Handlers/CreateOrderHandler.php
class CreateOrderHandler
{
    public function __construct(
        private OrderRepositoryInterface $orderRepository,
        private EventDispatcher $events,
    ) {}

    public function handle(CreateOrderCommand $command): Order
    {
        $order = $this->orderRepository->create([
            'customer_id' => $command->customerId,
            'total' => $command->calculateTotal(),
            'status' => OrderStatus::PENDING,
        ]);
        
        $this->events->dispatch(new OrderCreated($order));
        
        return $order;
    }
}

// app/Queries/Handlers/GetOrderDetailsHandler.php
class GetOrderDetailsHandler
{
    public function __construct(
        private OrderRepositoryInterface $orderRepository,
        private OrderReadModel $readModel,
    ) {}

    public function handle(GetOrderDetailsQuery $query): OrderDetailsDTO
    {
        // Có thể đọc từ denormalized read model thay vì join nhiều bảng
        return $this->readModel->getOrderDetails($query->orderId);
    }
}

// app/ReadModels/OrderReadModel.php
class OrderReadModel
{
    public function __construct(private Connection $db) {}

    public function getOrderDetails(int $orderId): OrderDetailsDTO
    {
        return $this->db->selectOne(
            "SELECT o.*, 
                    c.name as customer_name, c.email as customer_email,
                    COUNT(oi.id) as items_count,
                    GROUP_CONCAT(p.name) as product_names
             FROM orders o
             JOIN customers c ON o.customer_id = c.id
             LEFT JOIN order_items oi ON o.id = oi.order_id
             LEFT JOIN products p ON oi.product_id = p.id
             WHERE o.id = ?
             GROUP BY o.id",
            [$orderId]
        );
    }
}
```

## Hexagonal Architecture (Ports và Adapters)

```php
// Structure:
// app/
// ├── Domain/           # Business logic, entities
// │   ├── Entities/
// │   ├── ValueObjects/
// │   ├── Services/
// │   └── Repositories/  # Interfaces (Ports)
// ├── Application/       # Use cases, commands, queries
// │   ├── Commands/
// │   ├── Queries/
// │   └── Services/
// └── Infrastructure/    # Adapters
//     ├── Persistence/
//     ├── ExternalServices/
//     └── Http/

// app/Domain/Entities/Order.php
namespace App\Domain\Entities;

class Order
{
    public function __construct(
        private OrderId $id,
        private CustomerId $customerId,
        private Money $total,
        private OrderStatus $status,
        private array $items = [],
    ) {}

    public function addItem(Product $product, int $quantity): void
    {
        $this->items[] = new OrderItem(
            OrderItemId::generate(),
            $this->id,
            $product->id(),
            $product->price(),
            $quantity
        );
        
        $this->recalculateTotal();
    }

    public function recalculateTotal(): void
    {
        $this->total = array_reduce(
            $this->items,
            fn (Money $sum, OrderItem $item) => $sum->add($item->subtotal()),
            Money::zero()
        );
    }
}

// app/Domain/Repositories/OrderRepositoryInterface.php
namespace App\Domain\Repositories;

interface OrderRepositoryInterface
{
    public function save(Order $order): void;
    public function findById(OrderId $id): ?Order;
    public function findByCustomer(CustomerId $customerId): array;
}

// app/Infrastructure/Persistence/EloquentOrderRepository.php
namespace App\Infrastructure\Persistence;

class EloquentOrderRepository implements OrderRepositoryInterface
{
    public function __construct(private Order $model) {}

    public function save(Order $order): void
    {
        $this->model->create([
            'uuid' => $order->id()->toString(),
            'customer_id' => $order->customerId()->toString(),
            'total' => $order->total()->amount(),
        ]);
    }

    public function findById(OrderId $id): ?Order
    {
        $model = $this->model->where('uuid', $id->toString())->first();
        return $model ? $this->toDomain($model) : null;
    }

    private function toDomain(Order $model): Order
    {
        // Convert Eloquent model to Domain entity
    }
}

// app/Application/Services/OrderApplicationService.php
namespace App\Application\Services;

class OrderApplicationService
{
    public function __construct(
        private OrderRepositoryInterface $orderRepository,
    ) {}

    public function createOrder(CreateOrderDTO $dto): OrderDTO
    {
        $order = new Order(/* ... */);
        $this->orderRepository->save($order);
        
        return OrderDTO::fromEntity($order);
    }
}
```

## Service Layer Pattern

```php
// app/Services/OrderService.php
class OrderService
{
    public function __construct(
        private OrderRepositoryInterface $orderRepository,
        private ProductRepositoryInterface $productRepository,
        private InventoryService $inventoryService,
        private PaymentService $paymentService,
        private EventDispatcher $events,
    ) {}

    /**
     * Create a new order
     */
    public function createOrder(array $data): Order
    {
        return DB::transaction(function () use ($data) {
            // Validate products
            $this->validateProducts($data['items']);
            
            // Create order
            $order = $this->orderRepository->create([
                'customer_id' => $data['customer_id'],
                'status' => OrderStatus::PENDING,
                'shipping_address' => $data['shipping_address'],
            ]);
            
            // Add items
            foreach ($data['items'] as $item) {
                $product = $this->productRepository->find($item['product_id']);
                
                $order->addItem($product, $item['quantity']);
            }
            
            // Reserve inventory
            $this->inventoryService->reserveStock($order->items);
            
            // Dispatch event
            $this->events->dispatch(new OrderCreated($order));
            
            return $order;
        });
    }

    /**
     * Cancel an order
     */
    public function cancelOrder(Order $order, string $reason): Order
    {
        $this->authorize('cancel', $order);
        
        return DB::transaction(function () use ($order, $reason) {
            $order->cancel($reason);
            $this->orderRepository->save($order);
            
            // Release inventory
            $this->inventoryService->releaseStock($order->items);
            
            // Dispatch event
            $this->events->dispatch(new OrderCancelled($order, $reason));
            
            return $order;
        });
    }

    /**
     * Process payment for order
     */
    public function processPayment(Order $order, PaymentData $paymentData): PaymentResult
    {
        $result = $this->paymentService->charge($order, $paymentData);
        
        if ($result->isSuccessful()) {
            $order->markAsPaid($result->getTransactionId());
            $this->orderRepository->save($order);
            
            $this->events->dispatch(new OrderPaid($order));
        }
        
        return $result;
    }

    private function validateProducts(array $items): void
    {
        foreach ($items as $item) {
            $product = $this->productRepository->findOrFail($item['product_id']);
            
            if (!$product->isAvailable()) {
                throw new ProductNotAvailableException($product);
            }
            
            if ($product->stock < $item['quantity']) {
                throw new InsufficientStockException($product, $item['quantity']);
            }
        }
    }
}
```

## References

- [Laravel Documentation - Architecture](https://laravel.com/docs/architecture)
- [Laravel Documentation - Service Container](https://laravel.com/docs/container)
- [Laravel Documentation - Service Providers](https://laravel.com/docs/providers)
- [Laravel Documentation - Events](https://laravel.com/docs/events)
- [Hexagonal Architecture by Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture/)
- [Domain-Driven Design in Laravel](https://github.com/ddd-laravel/ddd-laravel)
