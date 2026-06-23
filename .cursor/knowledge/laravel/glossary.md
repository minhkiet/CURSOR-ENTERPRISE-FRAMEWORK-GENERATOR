---
title: "Laravel Glossary - Từ Điển Thuật Ngữ Laravel"
description: "Từ điển thuật ngữ toàn diện cho Laravel framework, bao gồm các khái niệm từ cơ bản đến nâng cao như Eloquent ORM, Blade templates, Service Container, và nhiều hơn nữa."
tags: ["laravel", "glossary", "terminology", "php", "web-development"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Laravel Glossary - Từ Điển Thuật Ngữ Laravel

## Tổng Quan

Tài liệu này cung cấp từ điển toàn diện về các thuật ngữ được sử dụng trong Laravel framework. Từ những khái niệm cơ bản như Eloquent ORM và Blade Templates cho đến các thuật ngữ nâng cao như Service Container, Service Providers, và Dependency Injection. Mỗi thuật ngữ được giải thích chi tiết với ví dụ code để giúp developers hiểu rõ ý nghĩa và cách sử dụng trong thực tế.

Laravel là một framework với vocabulary phong phú, và việc nắm vững các thuật ngữ này là essential cho việc đọc documentation, tham gia discussions, và làm việc hiệu quả với codebase.

## A

### Accessor

Accessor là một phương thức trong Eloquent Model cho phép bạn format data khi nó được đọc từ database. Accessors được định nghĩa với quy ước đặt tên `get{Attribute}Attribute`.

```php
// app/Models/User.php
class User extends Model
{
    // Accessor cho first_name
    public function getFirstNameAttribute($value): string
    {
        return ucfirst($value);
    }
    
    // Accessor cho full_name (computed property)
    public function getFullNameAttribute(): string
    {
        return "{$this->first_name} {$this->last_name}";
    }
    
    // Usage in code
    $user = User::find(1);
    echo $user->full_name; // Output: "John Doe"
}
```

### Artisan

Artisan là command-line interface (CLI) của Laravel. Nó cung cấp hàng trăm commands hữu ích cho việc development và deployment.

```bash
# Common Artisan commands
php artisan list                          # List all commands
php artisan make:controller UserController
php artisan make:model Post -m            # Create with migration
php artisan make:migration create_posts_table
php artisan migrate                       # Run migrations
php artisan migrate:rollback             # Rollback last migration
php artisan route:list                   # List all routes
php artisan cache:clear                  # Clear application cache
php artisan config:cache                 # Cache configuration
php artisan queue:work                   # Start queue worker
php artisan tinker                       # Interactive PHP shell
```

### API Resource

API Resources cho phép transform Eloquent models thành JSON responses một cách có cấu trúc và nhất quán.

```php
// app/Http/Resources/UserResource.php
class UserResource extends JsonResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'created_at' => $this->created_at->toIso8601String(),
            'posts_count' => $this->when(
                $this->posts_count !== null,
                $this->posts_count
            ),
        ];
    }
}

// Usage in controller
class UserController extends Controller
{
    public function index(): ResourceCollection
    {
        $users = User::withCount('posts')->paginate(20);
        
        return UserResource::collection($users);
    }
    
    public function show(User $user): JsonResponse
    {
        return new UserResource($user->load('posts'));
    }
}
```

### Auth Scaffold

Laravel cung cấp nhiều authentication scaffolding packages: Breeze (simple), Fortify (headless), Sanctum (API tokens), và Passport (OAuth2).

```bash
# Install Laravel Breeze
composer require laravel/breeze --dev
php artisan breeze:install

# Install Laravel Sanctum
composer require laravel/sanctum
php artisan install:api

# Install Laravel Passport
composer require laravel/passport
php artisan passport:install
```

## B

### Blade

Blade là templating engine của Laravel, cung cấp clean syntax cho việc hiển thị data và building layouts.

```blade
{{-- Layout file: resources/views/layouts/app.blade.php --}}
<!DOCTYPE html>
<html>
<head>
    <title>@yield('title', 'Default Title')</title>
    @stack('styles')
</head>
<body>
    @include('partials.header')
    
    <main>
        @yield('content')
    </main>
    
    @include('partials.footer')
    
    @stack('scripts')
</body>
</html>

{{-- Child view --}}
@extends('layouts.app')

@section('title', 'User Profile')

@section('content')
    <h1>{{ $user->name }}</h1>
    
    @if($user->posts->count() > 0)
        <ul>
            @foreach($user->posts as $post)
                <li>{{ $post->title }}</li>
            @endforeach
        </ul>
    @else
        <p>No posts yet.</p>
    @endif
    
    @verbatim
        {{-- This won't be parsed --}}
    @endverbatim
@endsection

@push('scripts')
    <script src="/js/user-profile.js"></script>
@endpush
```

### Broadcasting

Broadcasting cho phép real-time communication giữa server và client sử dụng WebSockets thông qua Pusher hoặc Laravel Echo.

```php
// app/Events/NewMessage.php
class NewMessage implements ShouldBroadcast
{
    public function __construct(
        public Message $message,
    ) {}
    
    public function broadcastOn(): array
    {
        return [
            new PrivateChannel('chat.' . $this->message->chat_room_id),
        ];
    }
    
    public function broadcastAs(): string
    {
        return 'message.new';
    }
}

// JavaScript (with Laravel Echo)
Echo.private(`chat.${chatRoomId}`)
    .listen('MessageNew', (e) => {
        this.messages.push(e.message);
    });
```

## C

### Collection

Laravel Collections cung cấp wrapper cho arrays, với nhiều methods mạnh mẽ để transform và filter data.

```php
// Creating collections
$collection = collect([1, 2, 3, 4, 5]);
$collection = collect(['name' => 'John', 'age' => 30]);

// Transform methods
$doubled = $collection->map(fn ($item) => $item * 2);
$filtered = $collection->filter(fn ($item) => $item > 2);
$plucked = $collection->pluck('name');

// Query methods
$first = $collection->first();
$last = $collection->last();
$sum = $collection->sum();
$avg = $collection->avg();

// Chaining
$result = $collection
    ->filter(fn ($item) => $item > 2)
    ->map(fn ($item) => $item * 2)
    ->sum();

// Advanced methods
$grouped = $collection->groupBy('category');
$flattened = $collection->flatten();
$unique = $collection->unique();
$chunked = $collection->chunk(2);
```

### Container (Service Container)

Service Container là IoC (Inversion of Control) container của Laravel, quản lý class dependencies và performing dependency injection.

```php
// Basic binding
$this->app->bind('HelpSpot\API', function ($app) {
    return new HelpSpot\API($app->make('HttpClient'));
});

// Singleton - same instance every time
$this->app->singleton('HelpSpot\API', function () {
    return new HelpSpot\API();
});

// Instance binding
$api = new HelpSpot\API();
$this->app->instance('HelpSpot\API', $api);

// Binding with dependencies
$this->app->bind('OrderService', function ($app) {
    return new OrderService(
        $app->make('OrderRepository'),
        $app->make('PaymentGateway')
    );
});

// Automatic resolution
class UserController extends Controller
{
    public function __construct(
        private UserService $userService,
    ) {}
}
```

### Controller

Controllers nhóm related request handling logic lại với nhau, acting như intermediary giữa HTTP requests và application logic.

```php
// app/Http/Controllers/UserController.php
class UserController extends Controller
{
    public function __construct(
        private UserService $userService,
    ) {}
    
    public function index(Request $request): JsonResponse
    {
        $users = $this->userService->getUsers($request->validated());
        
        return UserResource::collection($users);
    }
    
    public function store(CreateUserRequest $request): JsonResponse
    {
        $user = $this->userService->createUser($request->validated());
        
        return (new UserResource($user))
            ->response()
            ->setStatusCode(201);
    }
    
    public function show(User $user): JsonResponse
    {
        return new UserResource($user->load('posts'));
    }
    
    public function update(UpdateUserRequest $request, User $user): JsonResponse
    {
        $user = $this->userService->updateUser($user, $request->validated());
        
        return new UserResource($user);
    }
    
    public function destroy(User $user): JsonResponse
    {
        $this->userService->deleteUser($user);
        
        return response()->json(null, 204);
    }
}
```

### Contract

Contracts là tập hợp các interfaces định nghĩa core services của Laravel framework, giúp maintain loose coupling.

```php
// app/Contracts/OrderRepositoryInterface.php
interface OrderRepositoryInterface
{
    public function find(int $id): ?Order;
    public function findOrFail(int $id): Order;
    public function create(array $data): Order;
    public function update(Order $order, array $data): Order;
    public function delete(Order $order): bool;
    public function paginate(int $perPage): LengthAwarePaginator;
}

// Using contract in service
class OrderService
{
    public function __construct(
        private OrderRepositoryInterface $orderRepository,
    ) {}
    
    public function getOrder(int $id): ?Order
    {
        return $this->orderRepository->find($id);
    }
}

// Binding contract to implementation
// app/Providers/AppServiceProvider.php
$this->app->bind(
    OrderRepositoryInterface::class,
    EloquentOrderRepository::class
);
```

### CSRF Protection

CSRF (Cross-Site Request Forgery) protection ngăn chặn malicious sites từ việc submit forms đến application của bạn.

```blade
{{-- Automatic CSRF token in forms --}}
<form method="POST" action="/profile">
    @csrf
    <input type="text" name="name">
    <button type="submit">Update</button>
</form>

{{-- Manual token for AJAX --}}
<meta name="csrf-token" content="{{ csrf_token() }}">

{{-- In JavaScript --}}
fetch('/api/profile', {
    method: 'PUT',
    headers: {
        'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content
    },
    body: JSON.stringify({ name: 'John' })
})
```

## D

### Database Migration

Migrations là version control cho database schema, cho phép team members share và maintain consistent database structure.

```php
// database/migrations/2024_01_01_000001_create_users_table.php
class CreateUsersTable extends Migration
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
}

// Adding column to existing table
php artisan make:migration add_avatar_to_users_table --table=users

class AddAvatarToUsersTable extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->string('avatar')->nullable()->after('password');
        });
    }

    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->dropColumn('avatar');
        });
    }
}
```

### Dependency Injection

Dependency Injection là pattern trong đó dependencies được passed vào class thay vì được instantiated bên trong class đó.

```php
// Constructor Injection (recommended)
class OrderService
{
    public function __construct(
        private OrderRepository $orderRepository,
        private ProductRepository $productRepository,
        private MailerInterface $mailer,
    ) {}
}

// Method Injection
class InvoiceController extends Controller
{
    public function generate(GenerateInvoiceRequest $request, InvoiceGenerator $generator)
    {
        return $generator->generate($request->order_id);
    }
}

// Property Injection
class ReportGenerator
{
    #[Inject]
    protected PDFGenerator $pdfGenerator;
}
```

### Dispatch

Dispatch là act of sending a job to queue để xử lý asynchronous.

```php
// Dispatching a job
ProcessPaymentJob::dispatch($order, $paymentToken);

// Dispatch with delay
SendReminderEmailJob::dispatch($user, $message)
    ->delay(now()->addMinutes(30));

// Dispatch to specific queue
ProcessImageJob::dispatch($image)
    ->onQueue('images');

// Dispatch to specific connection
SendNewsletterJob::dispatch($subscribers)
    ->onConnection('redis');

// Dispatch after transaction commits
FinalizeOrderJob::dispatch($order)
    ->afterCommit();

// Dispatch immediately (sync)
NotifyUserJob::dispatch($user)
    ->onConnection('sync');
```

### DTO (Data Transfer Object)

DTO là object để transfer data giữa các layers hoặc components của application, thường không có behavior.

```php
// app/DTOs/CreateOrderDTO.php
readonly class CreateOrderDTO
{
    public function __construct(
        public int $customerId,
        public array $items,
        public array $shippingAddress,
        public string $paymentMethod,
        public ?string $notes = null,
    ) {}

    public static function fromArray(array $data): self
    {
        return new self(
            customerId: $data['customer_id'],
            items: $data['items'],
            shippingAddress: $data['shipping_address'],
            paymentMethod: $data['payment_method'],
            notes: $data['notes'] ?? null,
        );
    }
}

// Usage
$dto = CreateOrderDTO::fromArray($request->validated());
$order = $this->orderService->createOrder($dto);
```

## E

### Eloquent ORM

Eloquent là ORM (Object-Relational Mapping) của Laravel, cung cấp beautiful ActiveRecord implementation để interact với database.

```php
// app/Models/Post.php
class Post extends Model
{
    // Table name (optional if following convention)
    protected $table = 'posts';
    
    // Primary key
    protected $primaryKey = 'id';
    
    // Key type
    protected $keyType = 'int';
    
    // Disable auto-increment for UUID
    public $incrementing = false;
    
    // Fillable for mass assignment
    protected $fillable = ['title', 'content', 'user_id'];
    
    // Guarded fields
    protected $guarded = ['id', 'created_at', 'updated_at'];
    
    // Casts
    protected $casts = [
        'published_at' => 'datetime',
        'is_featured' => 'boolean',
        'metadata' => 'array',
    ];
    
    // Relationships
    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'user_id');
    }
    
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
    
    public function tags(): BelongsToMany
    {
        return $this->belongsToMany(Tag::class);
    }
    
    // Scopes
    public function scopePublished($query)
    {
        return $query->whereNotNull('published_at');
    }
    
    public function scopeForUser($query, $userId)
    {
        return $query->where('user_id', $userId);
    }
}
```

### Eloquent Relationships

Eloquent supports nhiều types của relationships để define associations giữa models.

```php
// One to One
class User extends Model
{
    public function profile(): HasOne
    {
        return $this->hasOne(Profile::class);
    }
}

// One to Many
class Post extends Model
{
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}

// Many to Many
class Role extends Model
{
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)
            ->withPivot('granted_at')
            ->withTimestamps();
    }
}

// Has Many Through
class Country extends Model
{
    public function posts(): HasManyThrough
    {
        return $this->hasManyThrough(Post::class, User::class);
    }
}

// Polymorphic One to One
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

// Polymorphic Many to Many
class Tag extends Model
{
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }
}
```

### Event

Events cung cấp way to subscribe và listen to application events, enabling loose coupling giữa components.

```php
// app/Events/OrderShipped.php
class OrderShipped implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public function __construct(
        public Order $order,
        public ?string $trackingNumber = null,
    ) {}

    public function broadcastOn(): array
    {
        return [
            new PrivateChannel('user.' . $this->order->user_id),
        ];
    }
}

// Dispatching event
event(new OrderShipped($order, $trackingNumber));

// Listening for event
// app/Providers/EventServiceProvider.php
protected $listen = [
    OrderShipped::class => [
        SendShippingNotification::class,
        UpdateTrackingJob::class,
    ],
];
```

## F

### Facade

Facades cung cấp static-like interface đến classes trong service container, cho phép easy access đến application services.

```php
// Common Facades
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Redirect;
use Illuminate\Support\Facades\Request;
use Illuminate\Support\Facades\Response;
use Illuminate\Support\Facades\Storage;

// Usage examples
$users = Cache::remember('users', 3600, fn () => User::all());
Log::info('User created', ['user_id' => $user->id]);
$validator = Validator::make($request->all(), $rules);
Mail::to($user)->send(new OrderConfirmation($order));
Storage::disk('s3')->put('avatar.jpg', $contents);
```

### Factory

Factories cung cấp convenient way to define và generate fake data cho testing và seeding.

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
            'password' => Hash::make('password'),
            'remember_token' => Str::random(10),
        ];
    }
    
    // State modifications
    public function unverified(): static
    {
        return $this->state(fn (array $attributes) => [
            'email_verified_at' => null,
        ]);
    }
    
    public function admin(): static
    {
        return $this->state(fn (array $attributes) => [
            'is_admin' => true,
            'role' => 'admin',
        ]);
    }
}

// Usage in tests
$user = User::factory()->create();
$users = User::factory()->count(10)->create();
$admin = User::factory()->admin()->create([
    'name' => 'Admin User',
]);
```

### Form Request

Form Requests là custom request classes chứa validation logic, tách biệt validation khỏi controllers.

```php
// app/Http/Requests/CreatePostRequest.php
class CreatePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Post::class);
    }

    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255', 'unique:posts,title'],
            'content' => ['required', 'string', 'min:10'],
            'category_id' => ['required', 'exists:categories,id'],
            'tags' => ['array'],
            'tags.*' => ['exists:tags,id'],
            'featured_image' => ['nullable', 'image', 'max:2048'],
            'publish_at' => ['nullable', 'date', 'after:now'],
        ];
    }

    public function messages(): array
    {
        return [
            'title.unique' => 'A post with this title already exists.',
            'content.min' => 'Post content must be at least 10 characters.',
        ];
    }

    protected function prepareForValidation(): void
    {
        if ($this->has('publish_at')) {
            $this->merge([
                'publish_at' => Carbon::parse($this->publish_at),
            ]);
        }
    }
}
```

## G

### Gate

Gates cung cấp simple authorization checks using Closure definitions, là alternative hoặc complement to Policies.

```php
// app/Providers/AuthServiceProvider.php
class AuthServiceProvider extends ServiceProvider
{
    protected function gate(): void
    {
        Gate::define('update-post', function (User $user, Post $post) {
            return $user->id === $post->user_id || $user->isAdmin();
        });

        Gate::define('delete-post', function (User $user, Post $post) {
            return $user->id === $post->user_id;
        });

        Gate::define('access-admin', function (User $user) {
            return $user->hasRole('admin');
        });

        // With resource
        Gate::resource('post', PostPolicy::class);
    }
}

// Using Gates
if (Gate::allows('update-post', $post)) {
    // Show edit button
}

if (Gate::denies('delete-post', $post)) {
    // Hide delete button
}

// In blade
@can('update', $post)
    <a href="/posts/{{ $post->id }}/edit">Edit</a>
@endcan

// Controller authorization
public function edit(Post $post)
{
    $this->authorize('update', $post);
    // Or with Gate
    Gate::authorize('update', $post);
}
```

## H

### Helper Functions

Laravel cung cấp many global helper functions cho common tasks.

```php
// Array & Object helpers
array_get($data, 'key.nested');
data_get($object, 'property.nested');
array_first($items, fn ($item) => $item['active']);
collect([1, 2, 3])->map(fn ($i) => $i * 2);

// String helpers
Str::slug('Hello World');           // hello-world
Str::limit('Long text...', 50);     // Long text...
Str::upper('hello');                // HELLO
Str::random(40);

// URL helpers
route('posts.show', ['post' => $post]);
action([PostController::class, 'show'], ['post' => $post]);
asset('js/app.js');
secure_asset('css/style.css');

// Other helpers
now();                              // Carbon::now()
optional($user->profile)->address;  // Null-safe access
retry(3, fn () => $this->fetchData());
tap($user, fn ($u) => $u->update(['last_active' => now()]));
```

## I

### IOC Container

Xem Service Container.

### Injection

Xem Dependency Injection.

### Interface

Interface là contract định nghĩa methods mà một class phải implement, promoting loose coupling.

```php
// app/Contracts/PaymentGatewayInterface.php
interface PaymentGatewayInterface
{
    public function charge(float $amount, string $token): PaymentResult;
    public function refund(string $transactionId): RefundResult;
    public function getTransaction(string $transactionId): ?Transaction;
}

// app/Services/StripePaymentGateway.php
class StripePaymentGateway implements PaymentGatewayInterface
{
    public function __construct(private StripeClient $client) {}

    public function charge(float $amount, string $token): PaymentResult
    {
        $charge = $this->client->charges->create([
            'amount' => $amount * 100,
            'currency' => 'usd',
            'source' => $token,
        ]);
        
        return new PaymentResult(
            success: $charge->status === 'succeeded',
            transactionId: $charge->id,
        );
    }
    
    public function refund(string $transactionId): RefundResult
    {
        // Implementation
    }
    
    public function getTransaction(string $transactionId): ?Transaction
    {
        // Implementation
    }
}
```

## J

### Job

Jobs represent background tasks có thể be dispatched to queue để xử lý asynchronous.

```php
// app/Jobs/ProcessImageJob.php
class ProcessImageJob implements ShouldQueue, ShouldBeUnique
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $timeout = 120;
    public int $backoff = 60;

    public function __construct(
        public Image $image,
    ) {
        $this->onQueue('images');
        $this->onConnection('redis');
    }

    public function handle(ImageProcessor $processor): void
    {
        $processor->process($this->image);
        
        $this->image->update(['processed' => true]);
    }

    public function failed(Throwable $exception): void
    {
        $this->image->update([
            'processed' => false,
            'error' => $exception->getMessage(),
        ]);
    }

    public function uniqueId(): string
    {
        return $this->image->id;
    }
}
```

## L

### Listener

Listeners respond to events và handle event-related logic, often dispatching jobs or performing side effects.

```php
// app/Listeners/SendWelcomeEmail.php
class SendWelcomeEmail implements ShouldQueue
{
    use Queueable;

    public int $tries = 3;

    public function __construct(
        private MailerInterface $mailer,
    ) {}

    public function handle(UserRegistered $event): void
    {
        $this->mailer->to($event->user->email)
            ->send(new WelcomeEmail($event->user));
    }

    public function failed(UserRegistered $event, Throwable $exception): void
    {
        Log::error('Failed to send welcome email', [
            'user_id' => $event->user->id,
            'error' => $exception->getMessage(),
        ]);
    }
}
```

## M

### Mass Assignment

Mass assignment là cách set multiple model attributes cùng lúc, nhưng cần được protected để tránh security vulnerabilities.

```php
// app/Models/User.php
class User extends Model
{
    // Only these fields can be mass-assigned
    protected $fillable = [
        'name',
        'email',
        'password',
    ];
    
    // Or these fields are protected from mass assignment
    protected $guarded = [
        'id',
        'is_admin',
        'role',
    ];
}

// Creating with mass assignment
$user = User::create($request->only(['name', 'email', 'password']));

// Or using fill
$user = new User();
$user->fill($request->validated());
$user->save();
```

### Middleware

Middleware cung cấp way to filter HTTP requests trước khi chúng được passed đến application logic.

```php
// app/Http/Middleware/EnsureUserIsSubscribed.php
class EnsureUserIsSubscribed
{
    public function handle(Request $request, Closure $next): Response
    {
        if (!$request->user() || !$request->user()->isSubscribed()) {
            if ($request->expectsJson()) {
                return response()->json([
                    'message' => 'Subscription required.',
                ], 403);
            }
            
            return Redirect::route('subscription.create');
        }
        
        return $next($request);
    }
}

// Registering middleware
// app/Http/Kernel.php
protected $middlewareAliases = [
    'auth' => \Illuminate\Auth\Middleware\Authenticate::class,
    'auth.basic' => \Illuminate\Auth\Middleware\AuthenticateWithBasicAuth::class,
    'throttle' => \Illuminate\Routing\Middleware\ThrottleRequests::class,
    'verified' => \Illuminate\Auth\Middleware\EnsureEmailIsVerified::class,
    'subscribed' => \App\Http\Middleware\EnsureUserIsSubscribed::class,
];

// Using middleware in routes
Route::middleware(['auth', 'subscribed'])->group(function () {
    Route::get('/premium/content', PremiumController::class);
});
```

### Migration

Xem Database Migration.

### Model

Xem Eloquent ORM.

### Mutator

Mutator cho phép bạn modify data trước khi nó được saved vào database.

```php
// app/Models/User.php
class User extends Model
{
    // Mutator for password
    public function setPasswordAttribute($value): void
    {
        $this->attributes['password'] = Hash::make($value);
    }
    
    // Mutator for name
    public function setNameAttribute($value): void
    {
        $this->attributes['name'] = trim(ucwords(strtolower($value)));
    }
    
    // Mutator for JSON field
    public function setSettingsAttribute(array $value): void
    {
        $this->attributes['settings'] = json_encode($value);
    }
}

// Usage
$user = new User();
$user->password = 'plaintext';  // Will be hashed automatically
$user->name = '  john doe  ';  // Will be "John Doe"
```

## N

### Notification

Notifications cung cấp way to send notifications qua multiple channels như email, SMS, Slack, etc.

```php
// app/Notifications/OrderShipped.php
class OrderShipped extends Notification
{
    public function __construct(
        public Order $order,
    ) {}

    public function via(object $notifiable): array
    {
        return ['mail', 'database', 'slack'];
    }

    public function toMail(object $notifiable): MailMessage
    {
        return (new MailMessage)
            ->subject('Your Order Has Been Shipped')
            ->line("Order #{$this->order->order_number} has been shipped.")
            ->action('Track Order', url("/orders/{$this->order->id}"))
            ->line('Thank you for your purchase!');
    }

    public function toArray(object $notifiable): array
    {
        return [
            'order_id' => $this->order->id,
            'message' => "Order {$this->order->order_number} shipped",
        ];
    }
}

// Sending notification
$user->notify(new OrderShipped($order));
Notification::send($users, new OrderShipped($order));
```

## O

### Observer

Observers listen to model events và perform actions khi models được created, updated, deleted, etc.

```php
// app/Observers/PostObserver.php
class PostObserver
{
    public function created(Post $post): void
    {
        // New post created
        Cache::forget("user.{$post->user_id}.posts");
    }

    public function updating(Post $post): void
    {
        // Post is being updated
    }

    public function updated(Post $post): void
    {
        // Post was updated
    }

    public function deleted(Post $post): void
    {
        // Post was deleted
        Cache::forget("post.{$post->id}");
    }

    public function restored(Post $post): void
    {
        // Post was restored
    }

    public function forceDeleted(Post $post): void
    {
        // Post was permanently deleted
    }
}

// Registering observer
// app/Providers/AppServiceProvider.php
class AppServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        Post::observe(PostObserver::class);
    }
}
```

## P

### Pagination

Pagination cho phép chia large result sets thành multiple pages.

```php
// Controller
public function index(Request $request): JsonResponse
{
    $posts = Post::with(['author', 'tags'])
        ->published()
        ->latest()
        ->paginate($request->get('per_page', 15));
    
    return PostResource::collection($posts);
}

// With cursor pagination (faster for large datasets)
public function index(Request $request): JsonResponse
{
    $posts = Post::cursorPaginate(15);
    
    return PostResource::collection($posts);
}

// Manual pagination
$posts = Post::paginate(15);
$posts->withPath('/custom/path');

// In Blade
@foreach($posts as $post)
    <h2>{{ $post->title }}</h2>
@endforeach

{{ $posts->links() }}
```

### Policy

Policies authorization logic cho specific models.

```php
// app/Policies/PostPolicy.php
class PostPolicy
{
    public function before(User $user, string $ability): ?bool
    {
        if ($user->isAdmin()) {
            return true;
        }
        return null;
    }

    public function viewAny(User $user): bool
    {
        return true;
    }

    public function view(User $user, Post $post): bool
    {
        if ($post->isPublished()) {
            return true;
        }
        return $user->id === $post->user_id;
    }

    public function create(User $user): bool
    {
        return $user->isAuthor();
    }

    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }

    public function delete(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }
}

// Register policy
// app/Providers/AuthServiceProvider.php
protected $policies = [
    Post::class => PostPolicy::class,
];
```

### Provider

Xem Service Provider.

## Q

### Queue

Queue cho phép defer time-consuming tasks như sending emails, processing images, để improve application response time.

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

// Queue worker commands
php artisan queue:work redis --queue=high,default
php artisan queue:listen
php artisan queue:retry all
php artisan queue:retry 5
php artisan queue:flush
php artisan queue:failed
```

### Query Builder

Query Builder cung cấp fluent interface để build và execute database queries.

```php
// Basic queries
$users = DB::table('users')->get();
$user = DB::table('users')->where('email', $email)->first();
$count = DB::table('orders')->count();

// Joins
$results = DB::table('orders')
    ->join('users', 'orders.user_id', '=', 'users.id')
    ->select('orders.*', 'users.name')
    ->where('orders.status', 'completed')
    ->groupBy('orders.user_id')
    ->havingRaw('SUM(orders.total) > ?', [1000])
    ->orderBy('total', 'desc')
    ->get();

// Aggregates
$maxPrice = DB::table('products')->max('price');
$avgRating = DB::table('reviews')->avg('rating');

// Subqueries
$latestOrders = DB::table('orders')
    ->whereIn('user_id', function ($query) {
        $query->select('id')
            ->from('users')
            ->where('status', 'active');
    })
    ->get();
```

## R

### Repository

Xem Repository Pattern trong Architecture document.

### Resource

Xem API Resource.

### Route Model Binding

Route Model Binding tự động inject model instances vào controllers dựa trên route parameters.

```php
// app/Models/Post.php
class Post extends Model
{
    // Customize the key used for resolution
    public function getRouteKeyName(): string
    {
        return 'slug';
    }
}

// routes/web.php
Route::get('/posts/{post}', [PostController::class, 'show']);

// Implicit binding - Laravel auto-resolves Post
public function show(Post $post)
{
    return $post;
}

// Explicit binding
// app/Providers/RouteServiceProvider.php
public function boot(): void
{
    Route::model('user', User::class);
    
    Route::bind('post', function ($value) {
        return Post::where('slug', $value)->firstOrFail();
    });
}
```

### Routing

Routing định nghĩa HTTP endpoints và maps chúng đến controller actions hoặc closures.

```php
// routes/web.php
use App\Http\Controllers\PostController;
use App\Http\Controllers\UserController;

// Basic routes
Route::get('/', fn () => view('welcome'));
Route::post('/contact', [ContactController::class, 'store']);
Route::put('/posts/{post}', [PostController::class, 'update']);
Route::delete('/posts/{post}', [PostController::class, 'destroy']);

// Route groups
Route::prefix('admin')->middleware(['auth', 'admin'])->group(function () {
    Route::get('/dashboard', [AdminController::class, 'dashboard']);
    Route::resource('posts', PostController::class);
});

// Resource routes
Route::apiResources([
    'posts' => PostController::class,
    'users' => UserController::class,
]);

// Named routes
Route::get('/profile', fn () => view('profile'))->name('profile');
<a href="{{ route('profile') }}">Profile</a>

// Route parameters
Route::get('/users/{id}', fn ($id) => $id);
Route::get('/posts/{post}/comments/{comment}', fn ($post, $comment) => "$post, $comment");

// Optional parameters
Route::get('/users/{name?}', fn ($name = 'Guest') => $name);
```

## S

### Sanctum

Laravel Sanctum cung cấp lightweight authentication system cho SPAs và API token authentication.

```php
// Installation
composer require laravel/sanctum
php artisan install:api

// app/Models/User.php
class User extends Authenticatable
{
    use HasApiTokens;
}

// Creating tokens
$user = User::find(1);
$token = $user->createToken('device-name')->plainTextToken;

// Authenticating
$response = $user->currentAccessToken();

// Revoking tokens
$user->tokens()->delete();
$user->currentAccessToken()->delete();

// Middleware
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/user', fn (Request $request) => $request->user());
});
```

### Scope

Scopes cho phép define reusable query constraints trong models.

```php
// app/Models/Post.php
class Post extends Model
{
    // Local scope
    public function scopePublished($query)
    {
        return $query->whereNotNull('published_at');
    }
    
    public function scopeDraft($query)
    {
        return $query->whereNull('published_at');
    }
    
    public function scopeForUser($query, $userId)
    {
        return $query->where('user_id', $userId);
    }
    
    public function scopeWithTag($query, $tag)
    {
        return $query->whereHas('tags', fn ($q) => 
            $q->where('name', $tag)
        );
    }
    
    // Dynamic scope
    public function scopeStatus($query, $status)
    {
        return $query->where('status', $status);
    }
}

// Usage
$publishedPosts = Post::published()->get();
$userPosts = Post::forUser(auth()->id())->draft()->get();
$activePosts = Post::status('active')->get();
```

### Seeder

Seeders populate database với initial data.

```php
// database/seeders/DatabaseSeeder.php
class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $this->call([
            UserSeeder::class,
            CategorySeeder::class,
            PostSeeder::class,
        ]);
    }
}

// database/seeders/PostSeeder.php
class PostSeeder extends Seeder
{
    public function run(): void
    {
        $users = User::all();
        
        $users->each(function ($user) {
            Post::factory()->count(5)->create([
                'user_id' => $user->id,
            ]);
        });
    }
}

// Running seeders
php artisan db:seed
php artisan db:seed --class=UserSeeder
php artisan migrate:fresh --seed
```

### Service Provider

Service Providers bootstrap application services, register bindings, và configure application behavior.

```php
// app/Providers/AppServiceProvider.php
class AppServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        // Register bindings
        $this->app->singleton(OrderService::class, function ($app) {
            return new OrderService(
                $app->make(OrderRepositoryInterface::class)
            );
        });
    }

    public function boot(): void
    {
        // Configure application
        View::share('siteName', config('app.name'));
        
        // Load resources
        $this->loadTranslationsFrom(__DIR__.'/../../lang', 'messages');
    }
}
```

### Soft Deletes

Soft Deletes mark records as deleted bằng cách set deleted_at timestamp thay vì actually deleting them.

```php
// Migration
$table->softDeletes();

// Model
class Post extends Model
{
    use SoftDeletes;
}

// Querying soft deleted records
$posts = Post::withTrashed()->get();
$posts = Post::onlyTrashed()->get();
$post = Post::withTrashed()->find(1);

// Restoring
$post->restore();

// Force delete
$post->forceDelete();

// Global scope for soft deletes (automatic)
Post::all(); // Excludes soft deleted

// Check if soft deleted
if ($post->trashed()) {
    // Record is soft deleted
}
```

## T

### Trait

Traits cho phép reuse methods across multiple classes.

```php
// app/Traits/HasAuthor.php
trait HasAuthor
{
    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'author_id');
    }
    
    public function authoredBy(User $user): bool
    {
        return $this->author_id === $user->id;
    }
}

// app/Models/Post.php
class Post extends Model
{
    use HasAuthor, HasTags, HasImages, HasUuid;
}

// app/Models/Comment.php
class Comment extends Model
{
    use HasAuthor;
}
```

## V

### Validation

Laravel's validation system cung cấp powerful rules để validate user input.

```php
// In Controller
public function store(Request $request): JsonResponse
{
    $validated = $request->validate([
        'title' => 'required|string|max:255|unique:posts',
        'content' => 'required|string|min:10',
        'category_id' => 'required|exists:categories,id',
        'tags' => 'array',
        'tags.*' => 'exists:tags,id',
        'publish_at' => 'nullable|date|after:now',
        'featured_image' => 'nullable|image|max:2048',
    ]);
    
    // $validated is guaranteed to be safe
}

// Form Request validation
class StorePostRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'title' => ['required', 'string', 'max:255'],
        ];
    }
}

// Manual validation
$validator = Validator::make($data, $rules);

if ($validator->fails()) {
    return redirect()->back()
        ->withErrors($validator)
        ->withInput();
}

// Custom validation rules
Validator::extend('phone', function ($attribute, $value) {
    return preg_match('/^[0-9]{10,11}$/', $value);
});
```

### View

Views chứa rendered HTML output của application, sử dụng Blade templating engine.

```php
// app/Http/Controllers/PostController.php
class PostController extends Controller
{
    public function index(): View
    {
        $posts = Post::published()->paginate(10);
        
        return view('posts.index', [
            'posts' => $posts,
        ]);
    }
    
    public function show(Post $post): View
    {
        return view('posts.show', [
            'post' => $post->load(['author', 'comments']),
        ]);
    }
}

// Blade view: resources/views/posts/index.blade.php
@extends('layouts.app')

@section('content')
    @forelse($posts as $post)
        <article>
            <h2>
                <a href="{{ route('posts.show', $post) }}">
                    {{ $post->title }}
                </a>
            </h2>
            <p>By {{ $post->author->name }}</p>
        </article>
    @empty
        <p>No posts found.</p>
    @endforelse
    
    {{ $posts->links() }}
@endsection
```

## W

### Watch

Watcher là feature trong Laravel Sanctum để manage authentication tokens.

```php
// Creating tokens with abilities (Laravel 11+)
$token = $user->createToken('token-name', ['posts:read', 'posts:write']);

// Checking abilities
if ($request->user()->tokenCan('posts:write')) {
    // Can write posts
}

// Using middleware
Route::middleware('token.can:posts:write')->group(function () {
    Route::post('/posts', [PostController::class, 'store']);
});
```

## References

- [Laravel Documentation](https://laravel.com/docs)
- [Laravel API Documentation](https://laravel.com/api/)
- [Laracasts](https://laracasts.com/)
- [Laravel News](https://laravel-news.com/)
