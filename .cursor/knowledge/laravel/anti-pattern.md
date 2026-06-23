---
title: "Laravel Anti-Patterns - Các Mẫu Cần Tránh"
description: "Tài liệu tổng hợp các anti-patterns phổ biến trong Laravel development cùng giải pháp khắc phục, giúp tránh những sai lầm thường gặp và xây dựng ứng dụng Laravel chất lượng cao."
tags: ["laravel", "anti-patterns", "best-practices", "php", "web-development"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Laravel Anti-Patterns - Các Mẫu Cần Tránh

## Tổng Quan

Trong quá trình phát triển ứng dụng Laravel, developers thường mắc phải những anti-patterns - các mẫu thiết kế gây ra vấn đề về maintainability, performance, và security. Tài liệu này liệt kê chi tiết các anti-patterns phổ biến nhất, giải thích tại sao chúng gây hại, và cung cấp giải pháp thay thế tối ưu cho production-ready applications.

Laravel cung cấp nhiều công cụ mạnh mẽ nhưng đi kèm là responsiblity trong việc sử dụng chúng đúng cách. Những anti-patterns dưới đây được chia thành các categories dựa trên layer của ứng dụng: Controllers, Models, Database, Security, và Architecture.

## Mục Đích

Tài liệu này nhằm mục đích giúp developers:

- Nhận diện các anti-patterns trong codebase hiện tại
- Hiểu lý do tại sao chúng là vấn đề
- Áp dụng giải pháp thay thế phù hợp
- Xây dựng thói quen code tốt từ đầu
- Tránh những pitfalls phổ biến trong Laravel development

## Key Concepts

### 1. Fat Controllers (Controllers Béo)

Fat Controllers là tình trạng controllers chứa quá nhiều business logic thay vì chỉ handle HTTP requests và responses. Điều này vi phạm Single Responsibility Principle và làm code khó test, khó maintain.

### 2. N+1 Query Problem

N+1 queries xảy ra khi Eloquent lazy-loads relationships, gây ra một query cho parent và N queries cho mỗi related model. Điều này có thể làm chậm ứng dụng đáng kể với dữ liệu lớn.

### 3. Mass Assignment Vulnerabilities

Mass assignment xảy ra khi không kiểm soát được fields nào có thể được set từ user input, dẫn đến potential security vulnerabilities.

### 4. Improper Facade Usage

Facades trong Laravel cực kỳ tiện lợi nhưng có thể bị lạm dụng, làm giảm testability và tạo hidden dependencies.

### 5. Missing Database Indexes

Không có indexes trên các columns thường được query dẫn đến slow database performance, đặc biệt nghiêm trọng khi dữ liệu tăng trưởng.

## Common Anti-Patterns

### 1. Fat Controllers

#### Vấn Đề

```php
// ❌ ANTI-PATTERN: Fat Controller
class OrderController extends Controller
{
    public function store(Request $request)
    {
        // Validation trong controller
        $validated = $request->validate([
            'customer_name' => 'required|string|max:255',
            'customer_email' => 'required|email',
            'items' => 'required|array',
            'items.*.product_id' => 'required|exists:products,id',
            'items.*.quantity' => 'required|integer|min:1',
            'shipping_address' => 'required|string',
            'payment_method' => 'required|in:credit_card,paypal,bank_transfer',
        ]);

        // Business logic trong controller
        $customer = Customer::where('email', $validated['customer_email'])->first();
        
        if (!$customer) {
            $customer = Customer::create([
                'name' => $validated['customer_name'],
                'email' => $validated['customer_email'],
            ]);
        }

        // Tính toán phức tạp
        $subtotal = 0;
        foreach ($validated['items'] as $item) {
            $product = Product::find($item['product_id']);
            $subtotal += $product->price * $item['quantity'];
        }

        $tax = $subtotal * 0.1;
        $shipping = $subtotal > 100 ? 0 : 10;
        $total = $subtotal + $tax + $shipping;

        // Tạo order
        $order = Order::create([
            'customer_id' => $customer->id,
            'total_amount' => $total,
            'shipping_address' => $validated['shipping_address'],
            'status' => 'pending',
        ]);

        // Tạo order items
        foreach ($validated['items'] as $item) {
            $product = Product::find($item['product_id']);
            OrderItem::create([
                'order_id' => $order->id,
                'product_id' => $product->id,
                'quantity' => $item['quantity'],
                'unit_price' => $product->price,
            ]);
        }

        // Gửi email notification
        Mail::to($customer->email)->send(new OrderConfirmation($order));

        // Log activity
        ActivityLog::create([
            'action' => 'order_created',
            'model_type' => 'Order',
            'model_id' => $order->id,
        ]);

        return response()->json(['order' => $order], 201);
    }
}
```

#### Giải Pháp

```php
// ✅ SOLUTION: Thin Controller với Service Layer
// app/Http/Requests/CreateOrderRequest.php
class CreateOrderRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'customer_name' => 'required|string|max:255',
            'customer_email' => 'required|email',
            'items' => 'required|array|min:1',
            'items.*.product_id' => 'required|exists:products,id',
            'items.*.quantity' => 'required|integer|min:1',
            'shipping_address' => 'required|string',
            'payment_method' => 'required|in:credit_card,paypal,bank_transfer',
        ];
    }
}

// app/Services/OrderService.php
class OrderService
{
    public function __construct(
        private CustomerService $customerService,
        private ProductService $productService,
        private OrderCalculationService $calculationService,
        private OrderNotificationService $notificationService,
        private ActivityLogService $activityLogService,
    ) {}

    public function createOrder(array $data): Order
    {
        $customer = $this->customerService->findOrCreateByEmail(
            $data['customer_email'],
            $data['customer_name']
        );

        $items = $this->productService->getProductsWithPrices($data['items']);
        $calculations = $this->calculationService->calculateOrder($items);
        
        $order = Order::create([
            'customer_id' => $customer->id,
            'total_amount' => $calculations['total'],
            'subtotal' => $calculations['subtotal'],
            'tax' => $calculations['tax'],
            'shipping' => $calculations['shipping'],
            'shipping_address' => $data['shipping_address'],
            'status' => OrderStatus::PENDING,
        ]);

        $this->productService->attachOrderItems($order, $items);
        
        $this->notificationService->sendOrderConfirmation($order);
        $this->activityLogService->logOrderCreated($order);

        return $order->load(['customer', 'items.product']);
    }
}

// app/Http/Controllers/Api/OrderController.php
class OrderController extends Controller
{
    public function __construct(private OrderService $orderService) {}

    public function store(CreateOrderRequest $request): JsonResponse
    {
        $order = $this->orderService->createOrder($request->validated());
        
        return response()->json([
            'message' => 'Order created successfully',
            'order' => new OrderResource($order),
        ], 201);
    }
}
```

### 2. N+1 Query Problem

#### Vấn Đề

```php
// ❌ ANTI-PATTERN: N+1 Queries
class OrderController extends Controller
{
    public function index()
    {
        // Query 1: Lấy tất cả orders
        $orders = Order::all();
        
        // Query N+1: Mỗi order gọi thêm queries cho relationships
        return view('orders.index', compact('orders'));
    }
}

// Trong Blade template - mỗi lần truy cập $order->customer sẽ tạo 1 query
@foreach($orders as $order)
    <tr>
        <td>{{ $order->id }}</td>
        <td>{{ $order->customer->name }}</td>  <!-- Query +1 -->
        <td>{{ $order->customer->email }}</td> <!-- Query +1 -->
        <td>
            @foreach($order->items as $item)     <!-- Query +1 mỗi order -->
                {{ $item->product->name }}      <!-- Query +1 mỗi item -->
            @endforeach
        </td>
        <td>{{ $order->created_at->format('d/m/Y') }}</td>
    </tr>
@endforeach

// Với 100 orders, 3 items mỗi order:
// 1 + 100 + 100 + 300 + 300 = 701 queries thay vì 4
```

#### Giải Pháp

```php
// ✅ SOLUTION: Eager Loading với with()
class OrderController extends Controller
{
    public function index()
    {
        $orders = Order::with([
            'customer:id,name,email',
            'items.product:id,name,price',
        ])
        ->select(['id', 'customer_id', 'total_amount', 'created_at'])
        ->latest()
        ->paginate(20);
        
        return view('orders.index', compact('orders'));
    }
}

// Hoặc sử dụng lazy loading với count queries tối ưu
// Trong Model
class Order extends Model
{
    protected $withCount = ['items'];
    
    public function getTotalItemsCountAttribute(): int
    {
        return $this->items_count;
    }
}
```

#### Advanced Eager Loading Techniques

```php
// Nested Eager Loading
$orders = Order::with([
    'customer.address',
    'items.product.category',
    'items.product.inventory',
])->get();

// Constrained Eager Loading - chỉ load orders có status cụ thể
$orders = Order::with(['customer' => function ($query) {
    $query->where('status', 'active');
}])->get();

// Lazy Eager Loading - khi đã có data rồi
$orders = Order::all();
// Sau đó load thêm relationships khi cần
$orders->load(['items.product', 'shipment']);

// Count với Eager Loading
$orders = Order::withCount('items')->get();

// Subquery Eager Loading cho performance tối ưu
$orders = Order::query()
    ->withSum('items', 'quantity')
    ->withMax('items', 'unit_price')
    ->get();
```

### 3. Mass Assignment Vulnerabilities

#### Vấn Đề

```php
// ❌ ANTI-PATTERN: Không kiểm soát Mass Assignment
class UserController extends Controller
{
    public function update(Request $request, $id)
    {
        $user = User::findOrFail($id);
        
        // Tất cả input được update mà không kiểm soát
        $user->update($request->all());
        
        return $user;
    }
}

// Attacker có thể gửi:
// { "email": "admin@evil.com", "is_admin": true, "password": "hacked" }
```

#### Giải Pháp

```php
// ✅ SOLUTION: Sử dụng $fillable hoặc $guarded

// app/Models/User.php
class User extends Model
{
    // Chỉ định rõ fields nào được phép mass-assign
    protected $fillable = [
        'name',
        'email',
        'password',
        'phone',
        'address',
    ];

    // Các fields bị cấm mass-assign
    protected $guarded = [
        'id',
        'is_admin',
        'role',
        'permissions',
        'created_at',
        'updated_at',
    ];

    // Hoặc block tất cả và chỉ cho phép từng field
    protected $guarded = ['*'];
}

// app/Http/Requests/UpdateUserRequest.php
class UpdateUserRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('update', $this->route('user'));
    }

    public function rules(): array
    {
        return [
            'name' => 'sometimes|string|max:255',
            'email' => 'sometimes|email|unique:users,email,' . $this->route('user')->id,
            'password' => 'sometimes|string|min:8|confirmed',
        ];
    }
}

// Controller sử dụng validated data
class UserController extends Controller
{
    public function update(UpdateUserRequest $request, User $user): JsonResponse
    {
        // Chỉ validated fields được update
        $user->update($request->validated());
        
        return new UserResource($user);
    }
}
```

### 4. Improper Facade Usage

#### Vấn Đề

```php
// ❌ ANTI-PATTERN: Facade abuse trong Models và Services
class Order extends Model
{
    public function calculateTotal(): float
    {
        $items = $this->items;
        
        // Sử dụng Facade không cần thiết
        $subtotal = $items->sum(function ($item) {
            return $item->quantity * $item->price;
        });
        
        $tax = Config::get('tax.rate') * $subtotal;
        
        // Hard-coded dependency
        Mail::to($this->customer->email)->send(new OrderConfirmed());
        
        return $subtotal + $tax;
    }
}

// Test khó khăn vì có hidden dependencies
// Không thể mock Config hoặc Mail dễ dàng
```

#### Giải Pháp

```php
// ✅ SOLUTION: Dependency Injection thay vì Facades

// app/Services/OrderCalculationService.php
class OrderCalculationService
{
    public function __construct(
        private TaxConfig $taxConfig,
    ) {}

    public function calculateTax(float $subtotal): float
    {
        return $subtotal * $this->taxConfig->getRate();
    }
}

// app/Models/Order.php
class Order extends Model
{
    public function calculateTotal(): float
    {
        $subtotal = $this->items->sum(fn($item) => $item->quantity * $item->price);
        $tax = $this->orderCalculationService->calculateTax($subtotal);
        
        return $subtotal + $tax;
    }
}

// Khi cần dùng Facade (trong Controllers), inject interface
class NotificationService
{
    public function __construct(
        private MailerInterface $mailer,
    ) {}
    
    public function sendOrderConfirmation(Order $order): void
    {
        $this->mailer->to($order->customer->email)
            ->send(new OrderConfirmationMail($order));
    }
}

// Trong Service Provider
$this->app->bind(MailerInterface::class, function () {
    return new LaravelMailerWrapper();
});
```

### 5. Missing Database Indexes

#### Vấn Đề

```php
// ❌ ANTI-PATTERN: Không có indexes cho các columns thường query
// database/migrations/2024_01_01_create_orders_table.php
public function up()
{
    Schema::create('orders', function (Blueprint $table) {
        $table->id();
        $table->unsignedBigInteger('customer_id');
        $table->string('status'); // Thường được filter nhưng không index
        $table->string('tracking_number'); // Tìm kiếm theo tracking nhưng không index
        $table->decimal('total_amount', 10, 2);
        $table->timestamp('created_at');
        
        $table->foreign('customer_id')->references('id')->on('customers');
        // Thiếu: $table->index('status');
        // Thiếu: $table->index('tracking_number');
        // Thiếu: $table->index(['customer_id', 'created_at']);
    });
}

// Khi query:
// SELECT * FROM orders WHERE status = 'pending' AND created_at > '2024-01-01'
// Sẽ scan toàn bộ table thay vì sử dụng index
```

#### Giải Pháp

```php
// ✅ SOLUTION: Thêm indexes phù hợp

// database/migrations/2024_01_01_create_orders_table.php
public function up()
{
    Schema::create('orders', function (Blueprint $table) {
        $table->id();
        $table->unsignedBigInteger('customer_id');
        $table->string('status');
        $table->string('tracking_number')->nullable();
        $table->decimal('total_amount', 10, 2);
        $table->timestamp('created_at');
        
        $table->foreign('customer_id')->references('id')->on('customers');
        
        // Indexes cho các truy vấn thường xuyên
        $table->index('status');                                    // Single column index
        $table->index('tracking_number');                           // Single column index
        $table->index(['customer_id', 'created_at']);              // Composite index
        $table->index(['status', 'created_at']);                   // Composite index cho filter + sort
        
        // Unique index cho tracking number
        $table->unique('tracking_number');
    });
}

// Hoặc thêm index riêng
Schema::table('orders', function (Blueprint $table) {
    $table->index(['customer_id', 'status']);
});

// Trong Model - định nghĩa indexes để generate migration tự động
class Order extends Model
{
    protected $table = 'orders';
    
    // Eloquent sẽ sử dụng indexes khi query
    public function scopePending($query)
    {
        return $query->where('status', 'pending');
    }
    
    public function scopeForCustomer($query, $customerId)
    {
        return $query->where('customer_id', $customerId);
    }
}

// Query sẽ sử dụng indexes một cách hiệu quả
$orders = Order::where('status', 'pending')
    ->where('created_at', '>=', now()->subMonth())
    ->orderBy('created_at', 'desc')
    ->paginate(20);
// EXPLAIN cho thấy sử dụng index thay vì full table scan
```

### 6. Ignoring Queues for Long-Running Tasks

#### Vấn Đề

```php
// ❌ ANTI-PATTERN: Xử lý tác vụ nặng trong request
class OrderController extends Controller
{
    public function processPayment(Request $request)
    {
        $order = Order::findOrFail($request->order_id);
        
        // 3rd party API call - có thể timeout
        $paymentResult = PaymentGateway::charge([
            'amount' => $order->total_amount,
            'card_token' => $request->card_token,
        ]);
        
        // Gửi nhiều emails
        foreach ($order->items as $item) {
            Mail::to($item->product->vendor->email)
                ->send(new OrderReceivedNotification($order, $item));
        }
        
        // Tạo PDF invoice
        $pdf = PDF::loadView('invoices.order', ['order' => $order]);
        Storage::put("invoices/{$order->id}.pdf", $pdf->output());
        
        // Update inventory
        InventoryService::decrementStock($order->items);
        
        $order->update(['status' => 'paid', 'paid_at' => now()]);
        
        return response()->json(['success' => true]);
        // User phải đợi 10-30 giây cho tất cả tác vụ hoàn thành
    }
}
```

#### Giải Pháp

```php
// ✅ SOLUTION: Sử dụng Jobs để xử lý background

// app/Jobs/ProcessPaymentJob.php
class ProcessPaymentJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $backoff = 60;
    
    public function __construct(
        public Order $order,
        public string $cardToken,
    ) {}

    public function handle(PaymentGateway $paymentGateway): void
    {
        if ($this->order->status !== OrderStatus::PENDING) {
            return;
        }
        
        $paymentResult = $paymentGateway->charge([
            'amount' => $this->order->total_amount,
            'card_token' => $this->cardToken,
        ]);
        
        if ($paymentResult->isSuccessful()) {
            $this->order->update([
                'status' => OrderStatus::PAID,
                'paid_at' => now(),
                'payment_reference' => $paymentResult->reference,
            ]);
            
            // Dispatch các jobs khác
            SendOrderNotificationJob::dispatch($this->order);
            GenerateInvoiceJob::dispatch($this->order);
            UpdateInventoryJob::dispatch($this->order);
        } else {
            $this->order->markPaymentFailed($paymentResult->errorMessage);
        }
    }

    public function failed(Throwable $exception): void
    {
        $this->order->markPaymentFailed($exception->getMessage());
        NotifyAdminJob::dispatch("Payment failed for order {$this->order->id}: {$exception->getMessage()}");
    }
}

// app/Http/Controllers/OrderController.php
class OrderController extends Controller
{
    public function processPayment(ProcessPaymentRequest $request): JsonResponse
    {
        $order = Order::findOrFail($request->order_id);
        
        ProcessPaymentJob::dispatch($order, $request->card_token);
        
        return response()->json([
            'message' => 'Payment processing initiated',
            'order_id' => $order->id,
        ], 202);
    }
}

// Chạy queue worker
// php artisan queue:work redis --queue=default,payments
```

### 7. Hard-Coded Configuration Values

#### Vấn Đề

```php
// ❌ ANTI-PATTERN: Hard-coded values
class ProductController extends Controller
{
    public function index()
    {
        $products = Product::where('is_active', true)
            ->where('category_id', 5)  // Magic number
            ->orderBy('name')
            ->limit(100)  // Hard-coded limit
            ->get();
            
        // Sử dụng magic strings
        if ($user->role === 'admin') {
            // admin logic
        }
        
        // Gọi API với hard-coded URL
        $response = Http::post('https://api.example.com/v1/products', [
            'api_key' => 'sk_live_1234567890',  // Hard-coded API key
            'timeout' => 30,  // Magic number
        ]);
    }
}
```

#### Giải Pháp

```php
// ✅ SOLUTION: Sử dụng config files và constants

// config/products.php
return [
    'per_page' => env('PRODUCTS_PER_PAGE', 20),
    'max_per_page' => 100,
    'default_category' => env('DEFAULT_PRODUCT_CATEGORY_ID'),
    'cache_ttl' => env('PRODUCTS_CACHE_TTL', 3600),
    'api' => [
        'timeout' => env('PRODUCT_API_TIMEOUT', 30),
        'retry_attempts' => 3,
    ],
];

// config/constants.php
return [
    'roles' => [
        'admin' => 'admin',
        'editor' => 'editor',
        'viewer' => 'viewer',
    ],
    'product_categories' => [
        'electronics' => 1,
        'clothing' => 2,
        'books' => 3,
        'home' => 5,  // Named constant thay vì magic number
    ],
];

// app/Http/Controllers/ProductController.php
class ProductController extends Controller
{
    public function index(): JsonResponse
    {
        $products = Product::where('is_active', true)
            ->where('category_id', config('products.default_category'))
            ->orderBy('name')
            ->limit(config('products.per_page'))
            ->get();
            
        if ($user->role === config('constants.roles.admin')) {
            // admin logic
        }
        
        $response = Http::timeout(config('products.api.timeout'))
            ->retry(config('products.api.retry_attempts'))
            ->post(config('services.external_api.url'), [
                'api_key' => config('services.external_api.key'),
            ]);
    }
}
```

### 8. Ignoring Database Transactions

#### Vấn Đề

```php
// ❌ ANTI-PATTERN: Không sử dụng transactions cho related operations
class OrderService
{
    public function createOrder(array $data): Order
    {
        // Tạo order
        $order = Order::create([
            'customer_id' => $data['customer_id'],
            'total' => $data['total'],
        ]);
        
        // Tạo order items - nếu fails, order đã được tạo
        foreach ($data['items'] as $item) {
            OrderItem::create([
                'order_id' => $order->id,
                'product_id' => $item['product_id'],
                'quantity' => $item['quantity'],
            ]);
        }
        
        // Update inventory - nếu fails, inventory không khớp
        foreach ($data['items'] as $item) {
            Product::where('id', $item['product_id'])
                ->decrement('stock', $item['quantity']);
        }
        
        // Partial success = data inconsistency
        return $order;
    }
}
```

#### Giải Pháp

```php
// ✅ SOLUTION: Sử dụng Database Transactions

// app/Services/OrderService.php
use Illuminate\Support\Facades\DB;

class OrderService
{
    public function __construct(
        private InventoryService $inventoryService,
    ) {}

    public function createOrder(array $data): Order
    {
        return DB::transaction(function () use ($data) {
            // Tạo order
            $order = Order::create([
                'customer_id' => $data['customer_id'],
                'total' => $data['total'],
                'status' => OrderStatus::PENDING,
            ]);
            
            // Tạo order items
            foreach ($data['items'] as $item) {
                OrderItem::create([
                    'order_id' => $order->id,
                    'product_id' => $item['product_id'],
                    'quantity' => $item['quantity'],
                    'unit_price' => Product::find($item['product_id'])->price,
                ]);
            }
            
            // Update inventory - nếu fails, toàn bộ được rollback
            $this->inventoryService->decrementForOrder($data['items']);
            
            return $order;
        }, 5); // 5 retries nếu deadlock xảy ra
    }
}

// Với Laravel 10+ có thể dùng transaction method chain
public function createOrder(array $data): Order
{
    return Order::createWithItems($data['customer_id'], $data['items'], function ($order) use ($data) {
        $order->total = $this->calculateTotal($data['items']);
    });
}
```

## Best Practices Để Tránh Anti-Patterns

### 1. Service Layer Pattern

```php
// app/Services/BaseService.php
abstract class BaseService
{
    protected array $relations = [];

    protected function findOrFail(string $modelClass, int|string $id): Model
    {
        return $modelClass::findOrFail($id);
    }

    protected function paginate(Builder $query, int $perPage = null): LengthAwarePaginator
    {
        return $query->with($this->relations)
            ->paginate($perPage ?? config('app.pagination.per_page'));
    }
}

// app/Services/OrderService.php
class OrderService extends BaseService
{
    protected array $relations = ['customer', 'items.product', 'shipping'];

    public function getOrdersForCustomer(int $customerId): Collection
    {
        return Order::forCustomer($customerId)
            ->with($this->relations)
            ->latest()
            ->get();
    }
}
```

### 2. Repository Pattern

```php
// app/Repositories/Contracts/OrderRepositoryInterface.php
interface OrderRepositoryInterface
{
    public function find(int $id): ?Order;
    public function findWithRelations(int $id): ?Order;
    public function create(array $data): Order;
    public function update(Order $order, array $data): Order;
    public function delete(Order $order): bool;
    public function paginate(int $perPage): LengthAwarePaginator;
}

// app/Repositories/Eloquent/OrderRepository.php
class OrderRepository implements OrderRepositoryInterface
{
    public function __construct(
        private Order $model,
    ) {}

    public function find(int $id): ?Order
    {
        return $this->model->find($id);
    }

    public function findWithRelations(int $id): ?Order
    {
        return $this->model->with(['customer', 'items.product'])
            ->find($id);
    }

    public function create(array $data): Order
    {
        return $this->model->create($data);
    }

    public function update(Order $order, array $data): Order
    {
        $order->update($data);
        return $order->fresh();
    }

    public function delete(Order $order): bool
    {
        return $order->delete();
    }

    public function paginate(int $perPage): LengthAwarePaginator
    {
        return $this->model->with(['customer'])
            ->latest()
            ->paginate($perPage);
    }
}

// app/Repositories/RepositoryServiceProvider.php
class RepositoryServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app->singleton(OrderRepositoryInterface::class, OrderRepository::class);
        $this->app->singleton(ProductRepositoryInterface::class, ProductRepository::class);
    }
}
```

### 3. Query Scopes for Reusability

```php
// app/Models/Traits/HasCommonScopes.php
trait HasCommonScopes
{
    public function scopeActive($query)
    {
        return $query->where('is_active', true);
    }

    public function scopeForDateRange($query, $startDate, $endDate)
    {
        return $query->whereBetween('created_at', [$startDate, $endDate]);
    }
}

// app/Models/Order.php
class Order extends Model
{
    use HasCommonScopes;

    public function scopePending($query)
    {
        return $query->where('status', OrderStatus::PENDING);
    }

    public function scopeCompleted($query)
    {
        return $query->where('status', OrderStatus::COMPLETED);
    }

    public function scopeForCustomer($query, int $customerId)
    {
        return $query->where('customer_id', $customerId);
    }

    public function scopeWithTotalAbove($query, float $amount)
    {
        return $query->where('total_amount', '>=', $amount);
    }
}

// Usage
$orders = Order::forCustomer($customerId)
    ->pending()
    ->active()
    ->forDateRange($startDate, $endDate)
    ->withTotalAbove(100)
    ->with(['items.product'])
    ->paginate(20);
```

## Troubleshooting

### Debugging N+1 Queries

```php
// Sử dụng Laravel Debugbar
// config/debugbar.php
'enabled' => env('DEBUGBAR_ENABLED', false),

// Trong code - kiểm tra queries
DB::listen(function ($query) {
    Log::info($query->sql, [
        'bindings' => $query->bindings,
        'time' => $query->time,
    ]);
});

// Hoặc sử dụng toSql() để debug
$query = Order::with(['customer', 'items']);
Log::info($query->toSql(), $query->getBindings());

// Sử dụng relationships without touching
$orders = Order::find(1);
$orders->loadCount('items');  // Đếm items không load collection
```

### Performance Profiling

```php
// Sử dụng Clockwork hoặc Laravel Debugbar
// Hoặc benchmark thủ công
use Illuminate\Support\Facades\DB;

public function benchmarkQueries()
{
    $start = microtime(true);
    
    $orders = Order::with(['customer', 'items.product'])->get();
    
    $end = microtime(true);
    
    Log::info("Query took " . ($end - $start) * 1000 . "ms");
    
    return $orders;
}
```

## Examples

### Complete Refactored Example

```php
// ❌ BEFORE: Fat Controller với tất cả anti-patterns
class UserController extends Controller
{
    public function show($id)
    {
        $user = User::find($id);
        
        foreach ($user->posts as $post) {
            foreach ($post->comments as $comment) {
                Mail::to($comment->author->email)->send(new CommentNotification());
            }
        }
        
        $user->update(['last_viewed_at' => now()]);
        
        return view('users.show', compact('user'));
    }
}

// ✅ AFTER: Refactored với Service, Repository, và Jobs
// app/Http/Controllers/UserController.php
class UserController extends Controller
{
    public function __construct(
        private UserService $userService,
    ) {}

    public function show(int $id): View
    {
        $user = $this->userService->getUserWithActivity($id);
        
        return view('users.show', [
            'user' => $user,
        ]);
    }
}

// app/Services/UserService.php
class UserService
{
    public function __construct(
        private UserRepositoryInterface $userRepository,
        private PostRepositoryInterface $postRepository,
    ) {}

    public function getUserWithActivity(int $id): User
    {
        $user = $this->userRepository->findWithRelations($id);
        
        $this->userRepository->updateLastViewed($user);
        
        return $user;
    }
}

// app/Jobs/NotifyPostAuthorsJob.php
class NotifyPostAuthorsJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;

    public function __construct(
        public Collection $comments,
    ) {}

    public function handle(): void
    {
        $this->comments->each(function ($comment) {
            SendEmailJob::dispatch(
                $comment->author->email,
                new CommentNotification($comment)
            );
        });
    }
}
```

## References

- [Laravel Documentation](https://laravel.com/docs)
- [Laravel Best Practices](https://github.com/alexeymezenin/laravel-best-practices)
- [PHP The Right Way](https://phptherightway.com/)
- [Laracasts - Laravel Video Tutorials](https://laracasts.com/)
- [Laravel Up & Running - Matt Stauffer](https://www.oreilly.com/library/view/laravel-up/9781492041205/)
