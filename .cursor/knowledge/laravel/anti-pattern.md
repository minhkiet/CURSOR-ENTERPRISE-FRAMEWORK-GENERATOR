# Laravel Anti-Patterns - Các Mẫu Cần Tránh

## Mục lục
1. [Controller Anti-Patterns](#1-controller-anti-patterns)
2. [Model Anti-Patterns](#2-model-anti-patterns)
3. [Database Anti-Patterns](#3-database-anti-patterns)
4. [Security Anti-Patterns](#4-security-anti-patterns)

---

## 1. Controller Anti-Patterns

### 1.1 Fat Controllers

**Tên Pattern**: God Controller

**Mô tả**: Đặt quá nhiều logic trong controller, làm nó trở nên khó maintain và test.

**Ví dụ (Anti-Pattern)**:
```php
// ❌ BAD: Fat controller with all logic
class OrderController extends Controller
{
    public function store(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'product_id' => 'required|exists:products,id',
            'quantity' => 'required|integer|min:1',
            'shipping_address' => 'required|string',
        ]);
        
        if ($validator->fails()) {
            return redirect()->back()->withErrors($validator)->withInput();
        }
        
        $product = Product::find($request->product_id);
        
        if ($product->stock < $request->quantity) {
            return redirect()->back()->with('error', 'Not enough stock');
        }
        
        $total = $product->price * $request->quantity;
        $total += $product->shipping_cost ?? 0;
        
        if ($request->coupon_code) {
            $coupon = Coupon::where('code', $request->coupon_code)->first();
            if ($coupon && $coupon->expires_at > now()) {
                if ($coupon->type === 'percentage') {
                    $total = $total * (1 - $coupon->value / 100);
                } else {
                    $total = $total - $coupon->value;
                }
            }
        }
        
        $order = Order::create([
            'user_id' => auth()->id(),
            'total' => $total,
            'status' => 'pending',
            // ... more fields
        ]);
        
        // Send email, create invoice, update stock...
        Mail::to(auth()->user())->send(new OrderConfirmation($order));
        Invoice::create(['order_id' => $order->id, /* ... */]);
        $product->decrement('stock', $request->quantity);
        
        return redirect()->route('orders.show', $order);
    }
}
```

**Hậu quả**:
- Controller quá dài và khó đọc
- Khó test business logic riêng lẻ
- Duplicate logic across controllers
- Violates Single Responsibility Principle

**Giải pháp thay thế**:
```php
// ✅ GOOD: Thin controller
class OrderController extends Controller
{
    public function __construct(
        private OrderService $orderService
    ) {}
    
    public function store(StoreOrderRequest $request): RedirectResponse
    {
        $order = $this->orderService->createOrder(
            auth()->user(),
            $request->validated()
        );
        
        return redirect()->route('orders.show', $order)
            ->with('success', 'Order placed successfully');
    }
}
```

---

### 1.2 Direct Request Validation in Controller

**Tên Pattern**: Inline Validation

**Mô tả**: Validation logic được placed trực tiếp trong controller thay vì Form Request.

**Ví dụ (Anti-Pattern)**:
```php
// ❌ BAD: Inline validation
public function store(Request $request)
{
    $request->validate([
        'name' => 'required|string|max:255',
        'email' => 'required|email|unique:users',
        'password' => 'required|string|min:8',
    ]);
    
    User::create($request->only(['name', 'email', 'password']));
    
    return redirect()->route('users.index');
}
```

**Hậu quả**:
- Validation logic khó reuse
- Controller becomes cluttered
- Harder to test
- Authorization logic can't be separated

**Giải pháp thay thế**:
```php
// ✅ GOOD: Form Request validation
public function store(StoreUserRequest $request)
{
    User::create($request->validated());
    return redirect()->route('users.index');
}
```

---

### 1.3 Not Using Resource Classes

**Tên Pattern**: Raw JSON Responses

**Mô tả**: Returning raw arrays hoặc models trực tiếp trong API controllers.

**Ví dụ (Anti-Pattern)**:
```php
// ❌ BAD: Raw model return
public function show(User $user): User
{
    return $user; // Not standardized
}

public function index(): Collection
{
    return User::all(); // No transformation
}
```

**Hậu quả**:
- Inconsistent response format
- Expose sensitive data
- Can't control transformation
- API breaking changes

**Giải pháp thay thế**:
```php
// ✅ GOOD: API Resources
public function show(User $user): UserResource
{
    return UserResource::make($user);
}

public function index(): UserCollection
{
    return UserCollection::make(User::paginate(15));
}
```

---

## 2. Model Anti-Patterns

### 2.1 Not Using Mass Assignment Protection

**Tên Pattern**: Unguarded Mass Assignment

**Mô tả**: Không define $fillable hoặc $guarded, có thể dẫn đến mass assignment vulnerabilities.

**Ví dụ (Anti-Pattern)**:
```php
// ❌ BAD: No mass assignment protection
class User extends Model
{
    // Missing $fillable or $guarded!
    
    public function setIsAdminAttribute($value)
    {
        $this->attributes['is_admin'] = $value;
    }
}

// In controller - potential security issue
User::create($request->all()); // Could set is_admin!
```

**Hậu quả**:
- Security vulnerability
- Users could set admin status
- Unexpected data in database

**Giải pháp thay thế**:
```php
// ✅ GOOD: Proper mass assignment protection
class User extends Model
{
    protected $fillable = ['name', 'email', 'password'];
    protected $guarded = ['id', 'is_admin', 'created_at'];
}
```

---

### 2.2 N+1 Query Problem

**Tên Pattern**: Lazy Loading Everywhere

**Mô tả**: Sử dụng lazy loading cho relationships trong loops, tạo ra N+1 queries.

**Ví dụ (Anti-Pattern)**:
```php
// ❌ BAD: N+1 queries
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->user->name; // Query for each post's user!
    foreach ($post->comments as $comment) {
        echo $comment->user->name; // Query for each comment's user!
    }
}

// This creates: 1 + N + M queries!
```

**Hậu quả**:
- Severe performance issues
- Too many database queries
- Memory bloat
- Slow page loads

**Giải pháp thay thế**:
```php
// ✅ GOOD: Eager loading
$posts = Post::with(['user', 'comments.user'])->get();
foreach ($posts as $post) {
    echo $post->user->name; // No additional query
    foreach ($post->comments as $comment) {
        echo $comment->user->name; // No additional query
    }
}

// This creates: 3 queries total (posts, users, comments_with_users)
```

---

### 2.3 Storing Passwords in Plain Text

**Tên Pattern**: Plain Text Password

**Mô tả**: Lưu trữ passwords không được hashed.

**Ví dụ (Anti-Pattern)**:
```php
// ❌ BAD: Plain text password
class UserController extends Controller
{
    public function store(Request $request)
    {
        User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => $request->password, // Plain text!
        ]);
    }
}
```

**Hậu quả**:
- Severe security vulnerability
- Passwords exposed if database is compromised
- Violates security best practices
- Legal/regulatory issues

**Giải pháp thay thế**:
```php
// ✅ GOOD: Hashed password
class UserController extends Controller
{
    public function store(StoreUserRequest $request)
    {
        User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => bcrypt($request->password),
        ]);
    }
}

// Or use Mutator in Model
class User extends Model
{
    public function setPasswordAttribute($value): void
    {
        $this->attributes['password'] = bcrypt($value);
    }
}
```

---

## 3. Database Anti-Patterns

### 3.1 Using Query Builder Raw Queries Without Parameter Binding

**Tên Pattern**: SQL Injection Vulnerability

**Mô tả**: Sử dụng raw SQL với string interpolation, có thể dẫn đến SQL injection.

**Ví dụ (Anti-Pattern)**:
```php
// ❌ BAD: SQL injection vulnerability
$users = DB::select("SELECT * FROM users WHERE name = '$name'");

// Or worse
$users = DB::table('users')
    ->whereRaw("name = '$name'")
    ->get();
```

**Hậu quả**:
- SQL injection attacks
- Data breach
- Data corruption
- Server compromise

**Giải pháp thay thế**:
```php
// ✅ GOOD: Parameter binding
$users = DB::select("SELECT * FROM users WHERE name = ?", [$name]);

// Or using query builder
$users = DB::table('users')
    ->where('name', $name)
    ->get();

// For complex conditions
$users = DB::table('users')
    ->where(function ($query) use ($name) {
        $query->where('name', 'like', "%{$name}%");
    })
    ->get();
```

---

### 3.2 Not Using Database Transactions

**Tên Pattern**: Incomplete Transactions

**Mô tả**: Thực hiện multiple related database operations mà không có transaction, có thể dẫn đến inconsistent data.

**Ví dụ (Anti-Pattern)**:
```php
// ❌ BAD: No transaction
public function createOrder(array $data)
{
    $order = Order::create([
        'user_id' => $data['user_id'],
        'total' => 0,
    ]);
    
    foreach ($data['items'] as $item) {
        OrderItem::create([
            'order_id' => $order->id,
            'product_id' => $item['product_id'],
            'quantity' => $item['quantity'],
        ]);
        
        Product::find($item['product_id'])->decrement('stock', $item['quantity']);
    }
    
    $total = OrderItem::where('order_id', $order->id)->sum('price');
    $order->update(['total' => $total]);
    
    // If this fails, previous operations are already committed!
}
```

**Hậu quả**:
- Inconsistent data
- Partial updates
- Difficult recovery
- Data integrity issues

**Giải pháp thay thế**:
```php
// ✅ GOOD: Transaction wrapping
public function createOrder(array $data)
{
    return DB::transaction(function () use ($data) {
        $order = Order::create([
            'user_id' => $data['user_id'],
            'total' => 0,
        ]);
        
        foreach ($data['items'] as $item) {
            OrderItem::create([
                'order_id' => $order->id,
                'product_id' => $item['product_id'],
                'quantity' => $item['quantity'],
            ]);
            
            Product::find($item['product_id'])->decrement('stock', $item['quantity']);
        }
        
        $total = OrderItem::where('order_id', $order->id)->sum('price');
        $order->update(['total' => $total]);
        
        return $order;
    });
}
```

---

### 3.3 Not Using Indexes for Frequently Queried Columns

**Tên Pattern**: Missing Indexes

**Mô tả**: Không tạo indexes cho columns thường xuyên được query.

**Ví dụ (Anti-Pattern)**:
```php
// ❌ BAD: No indexes on frequently queried columns
Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('body');
    $table->boolean('published');
    $table->foreignId('user_id')->constrained();
    $table->timestamps();
    
    // No indexes!
});

# Query: SELECT * FROM posts WHERE published = 1 AND user_id = 5
# This will do a full table scan!
```

**Hậu quả**:
- Slow queries
- Poor performance
- Database bottleneck
- Scalability issues

**Giải pháp thay thế**:
```php
// ✅ GOOD: Proper indexes
Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('body');
    $table->boolean('published');
    $table->foreignId('user_id')->constrained();
    $table->timestamps();
    
    // Indexes for common queries
    $table->index(['published', 'user_id']);
    $table->index(['user_id', 'published']);
    $table->fullText(['title', 'body']); // For search
});
```

---

## 4. Security Anti-Patterns

### 4.1 Not Validating Authorization

**Tên Pattern**: Broken Access Control

**Mô tả**: Không kiểm tra authorization trước khi thực hiện actions.

**Ví dụ (Anti-Pattern)**:
```php
// ❌ BAD: No authorization check
public function update(Request $request, $id)
{
    $post = Post::findOrFail($id);
    
    // Anyone can update any post!
    $post->update($request->all());
    
    return $post;
}
```

**Hậu quả**:
- Users can modify others' data
- Privilege escalation
- Data tampering
- Security breach

**Giải pháp thay thế**:
```php
// ✅ GOOD: Authorization check
public function update(UpdatePostRequest $request, Post $post)
{
    $this->authorize('update', $post);
    
    $post->update($request->validated());
    
    return $post;
}

// Or using Policy
public function update(Request $request, Post $post): bool
{
    return $request->user()->id === $post->user_id || 
           $request->user()->isAdmin();
}
```

---

### 4.2 Storing Sensitive Data in Client-Side State

**Tên Pattern**: Sensitive Data Exposure

**Mô tả**: Lưu trữ sensitive data trong cookies hoặc client-accessible storage.

**Ví dụ (Anti-Pattern)**:
```php
// ❌ BAD: Storing sensitive data in cookies
Cookie::queue('user_permissions', json_encode($permissions), 60 * 24 * 7);
Cookie::queue('api_key', $apiKey, 60 * 24 * 7);

// Also bad: Session data that shouldn't be persisted
session(['admin_notes' => 'Sensitive info']);
```

**Hậu quả**:
- Data exposure to users
- XSS vulnerabilities
- Session hijacking
- Token theft

**Giải pháp thay thế**:
```php
// ✅ GOOD: Server-side session storage
session(['user_id' => $user->id]);
// Only retrieve related data from database when needed

// For API tokens
$user->update(['api_token' => Str::random(60)]);
// Send token in response, store on server mapping
```

---

### 4.3 Not Implementing Rate Limiting

**Tên Pattern**: No Rate Limiting

**Mô tả**: Không limit requests per user, cho phép abuse và DoS attacks.

**Ví dụ (Anti-Pattern)**:
```php
// ❌ BAD: No rate limiting
Route::post('/api/login', [AuthController::class, 'login']);

// An attacker can try unlimited passwords!
```

**Hậu quả**:
- Brute force attacks
- Resource exhaustion
- Service degradation
- Cost increase

**Giải pháp thay thế**:
```php
// ✅ GOOD: Rate limiting
Route::middleware(['throttle:5,1'])->group(function () {
    Route::post('/api/login', [AuthController::class, 'login']);
});

// Or in controller
class AuthController extends Controller
{
    public function __construct()
    {
        $this->middleware('throttle:5,1'); // 5 attempts per minute
    }
}
```

---

## Liên kết liên quan
- [Laravel Glossary](./glossary.md)
- [Laravel Architecture](./architecture.md)
- [Laravel Best Practices](./best-practice.md)
- [Laravel Checklist](./checklist.md)
- [Laravel FAQ](./faq.md)
- [Laravel Decision Tree](./decision-tree.md)
