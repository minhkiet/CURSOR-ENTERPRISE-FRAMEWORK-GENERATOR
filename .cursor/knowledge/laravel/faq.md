---
title: "Laravel FAQ - Câu Hỏi Thường Gặp"
description: "Tổng hợp các câu hỏi thường gặp về Laravel với expert answers, giải thích chi tiết các khái niệm, patterns, và best practices cho developers ở mọi level."
tags: ["laravel", "faq", "questions", "answers", "php"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Laravel FAQ - Câu Hỏi Thường Gặp

## Tổng Quan

Tài liệu này tổng hợp các câu hỏi thường gặp về Laravel framework, được phân loại theo topics để dễ reference. Mỗi câu hỏi được trả lời chi tiết với code examples và explanations, giúp developers hiểu không chỉ "what" mà còn "why" và "how".

Laravel là một framework phong phú với nhiều features và conventions. FAQ này address những questions mà developers thường gặp khi làm việc với Laravel, từ những basics cho đến advanced topics.

## Mục Đích

Tài liệu này phục vụ:

- Quick reference cho common questions
- Deep explanation của Laravel concepts
- Solutions cho common problems
- Best practices guidance
- Onboarding reference cho new developers

---

## 1. Eloquent ORM

### Q1: Làm thế nào để fix N+1 query problem?

**A:** N+1 query problem xảy ra khi Eloquent lazy-loads relationships, gây ra nhiều queries không cần thiết. Solution là sử dụng eager loading với `with()`.

```php
// ❌ N+1 Problem - Mỗi user tạo thêm query cho posts
$users = User::all();
foreach ($users as $user) {
    echo $user->posts->count(); // Query riêng cho mỗi user
}
// 1 query users + N queries posts = N+1 queries

// ✅ Solution - Eager load relationships
$users = User::with('posts')->get();
foreach ($users as $user) {
    echo $user->posts->count(); // Không tạo thêm query
}
// 2 queries (users + posts) bất kể có bao nhiêu users

// Nested eager loading
$users = User::with(['posts.comments', 'profile'])->get();

// Selective columns
$users = User::with(['posts:id,title,user_id'])->get();

// Conditional eager loading
$users = User::with(['posts' => function ($query) {
    $query->where('published', true);
}])->get();

// Counting relations
$users = User::withCount('posts')->get();
echo $users->first()->posts_count;

// Nested counting
$users = User::withCount(['posts', 'posts as published_posts_count' => function ($query) {
    $query->where('published', true);
}])->get();
```

### Q2: Sự khác biệt giữa `create()` và `save()` trong Eloquent là gì?

**A:** Cả hai đều tạo records, nhưng có những khác biệt quan trọng.

```php
// save() - Rõ ràng hơn, có kiểm soát hơn
$post = new Post();
$post->title = 'My Title';
$post->content = 'My Content';
$post->save(); // INSERT hoặc UPDATE tùy thuộc vào model

// create() - Mass assignment với fillable protection
$post = Post::create([
    'title' => 'My Title',
    'content' => 'My Content',
]);
// Tự động INSERT, chỉ hoạt động với fillable fields

// save() với model mới
$post = new Post();
$post->title = 'New Post';
$post->save(); // INSERT

// save() với existing model
$post = Post::find(1);
$post->title = 'Updated Title';
$post->save(); // UPDATE

// save() trả về boolean
if ($post->save()) {
    // Success
}

// create() trả về model instance
// create() throw ValidationException nếu mass assignment fails
```

### Q3: Khi nào nên sử dụng `firstOrCreate()` vs `firstOrNew()`?

**A:** Cả hai đều tìm record hoặc tạo mới nếu không tìm thấy, nhưng có behaviors khác nhau.

```php
// firstOrCreate - Tìm và tạo record trong database
$user = User::firstOrCreate(
    ['email' => 'john@example.com'],  // Search conditions
    ['name' => 'John Doe', 'password' => Hash::make('password')]  // Create data
);
// Nếu tìm thấy: trả về existing record
// Nếu không tìm thấy: tạo và trả về record mới

// firstOrNew - Tìm hoặc tạo instance mới (chưa save)
$user = User::firstOrNew(
    ['email' => 'john@example.com'],
    ['name' => 'John Doe']
);
// Nếu tìm thấy: trả về existing record
// Nếu không tìm thấy: trả về new instance NHƯNG CHƯA SAVE

// Với firstOrNew, bạn cần save thủ công
$user = User::firstOrNew(['email' => 'john@example.com']);
if (!$user->exists) {
    $user->name = 'John Doe';
    $user->password = Hash::make('password');
    $user->save();
}

// firstOrFail - Throw exception nếu không tìm thấy
$user = User::firstOrFail('email', 'john@example.com');
// ModelNotFoundException nếu không tìm thấy
```

### Q4: Làm thế nào để implement soft deletes?

**A:** Soft deletes mark records as deleted bằng cách setting `deleted_at` timestamp thay vì actually deleting.

```php
// 1. Migration - Thêm softDeletes column
Schema::table('posts', function (Blueprint $table) {
    $table->softDeletes();
});

// 2. Model - Sử dụng SoftDeletes trait
use Illuminate\Database\Eloquent\SoftDeletes;

class Post extends Model
{
    use SoftDeletes;
    
    protected $dates = ['deleted_at']; // Auto-cast
}

// 3. Querying soft deleted records
// Mặc định đã exclude soft deleted
$activePosts = Post::all(); // Chỉ lấy posts chưa deleted

// Với soft deleted records
$allPosts = Post::withTrashed()->get();
$deletedPosts = Post::onlyTrashed()->get();

// Restore soft deleted
$post->restore();

// Force delete (thực sự xóa)
$post->forceDelete();

// Check if soft deleted
if ($post->trashed()) {
    // Record đã bị soft delete
}

// Query với soft deletes
Post::withTrashed()->find(1);
Post::onlyTrashed()->where('user_id', 1)->get();
```

### Q5: Accessors và Mutators hoạt động như thế nào?

**A:** Accessors format data khi đọc từ database, Mutators format data khi ghi vào database.

```php
class User extends Model
{
    // ACCESSOR - Format khi đọc
    // Quy ước: get{Attribute}Attribute
    public function getFirstNameAttribute($value): string
    {
        return ucfirst($value);
    }
    
    // Computed accessor (không có DB column)
    public function getFullNameAttribute(): string
    {
        return "{$this->first_name} {$this->last_name}";
    }
    
    // Access attribute
    $user->first_name; // "john" → "John"
    $user->full_name;   // "John Doe"
    
    // MUTATOR - Format khi ghi
    // Quy ước: set{Attribute}Attribute
    public function setPasswordAttribute($value): void
    {
        $this->attributes['password'] = Hash::make($value);
    }
    
    public function setNameAttribute($value): void
    {
        $this->attributes['name'] = trim(ucwords(strtolower($value)));
    }
    
    // Set attribute
    $user->password = 'plaintext'; // Auto hashed
    $user->name = '  JOHN DOE  ';  // Auto "John Doe"
    
    // DATE CASTING - Auto date conversion
    protected $casts = [
        'published_at' => 'datetime',
        'created_at' => 'date:Y-m-d',
        'metadata' => 'array',
        'is_active' => 'boolean',
        'price' => 'decimal:2',
    ];
    
    // Array/JSON casting
    $user->update([
        'metadata' => ['theme' => 'dark', 'notifications' => true]
    ]);
    echo $user->metadata['theme']; // "dark"
}
```

---

## 2. Routing

### Q6: Làm thế nào để pass parameters vào routes?

**A:** Laravel hỗ trợ required, optional, và multiple route parameters.

```php
// Required parameters
Route::get('/users/{id}', fn ($id) => User::find($id));
Route::get('/posts/{post}/comments/{comment}', fn ($post, $comment) => "$post $comment");

// Optional parameters
Route::get('/users/{name?}', fn ($name = 'Guest') => "Hello $name");
Route::get('/users/{id}/posts/{slug?}', fn ($id, $slug = null) => "...");

// Constrained parameters
Route::get('/users/{id}', fn ($id) => User::find($id))
    ->where('id', '[0-9]+'); // Chỉ numbers

Route::get('/users/{id}/{slug}', fn ($id, $slug) => User::find($id))
    ->where([
        'id' => '[0-9]+',
        'slug' => '[a-z0-9-]+',
    ]);

// Global constraints - app/Providers/RouteServiceProvider.php
public function boot(): void
{
    Route::pattern('id', '[0-9]+');
    Route::pattern('uuid', '[a-f0-9-]{36}');
}

// Named routes
Route::get('/users/profile', [UserController::class, 'profile'])->name('users.profile');

// Using named routes
route('users.profile'); // Generate URL
<a href="{{ route('users.profile') }}">Profile</a>

// Redirect with named route
return redirect()->route('users.profile');
```

### Q7: Sự khác biệt giữa `GET` và `POST` routes là gì?

**A:** Chúng là HTTP verbs với different purposes và behaviors.

```php
// GET - Lấy data, idempotent, có thể cache, gửi data qua URL
Route::get('/users', [UserController::class, 'index']);
Route::get('/users/{id}', [UserController::class, 'show']);

// POST - Tạo data, không idempotent, gửi data qua request body
Route::post('/users', [UserController::class, 'store']);
// Data được gửi trong body, không hiển thị trong URL

// PUT - Update/replace entire resource, idempotent
Route::put('/users/{id}', [UserController::class, 'update']);

// PATCH - Update/replace specific fields, idempotent
Route::patch('/users/{id}', [UserController::class, 'partialUpdate']);

// DELETE - Xóa resource, idempotent
Route::delete('/users/{id}', [UserController::class, 'destroy']);

// HTML Forms chỉ hỗ trợ GET và POST
// Sử dụng @method directive để fake other verbs
<form method="POST" action="/users/1">
    @method('PUT')
    @csrf
</form>

// Multiple HTTP verbs for same route
Route::match(['get', 'post'], '/contact', [ContactController::class, 'submit']);
Route::any('/webhook', [WebhookController::class, 'handle']);
```

### Q8: Làm thế nào để group routes và share attributes?

**A:** Route groups cho phép share attributes như middleware, prefix, namespace cho multiple routes.

```php
// Basic group
Route::middleware(['auth'])->group(function () {
    Route::get('/dashboard', DashboardController::class);
    Route::get('/settings', SettingsController::class);
});

// Prefix group
Route::prefix('admin')->group(function () {
    Route::get('/users', [AdminUserController::class, 'index']);
    Route::get('/posts', [AdminPostController::class, 'index']);
});
// URLs: /admin/users, /admin/posts

// Name prefix
Route::name('admin.')->group(function () {
    Route::get('/users', ...)->name('users');
    Route::get('/posts', ...)->name('posts');
});
// Names: admin.users, admin.posts

// Namespace group
Route::prefix('api')->namespace('App\Http\Controllers\Api')->group(function () {
    Route::get('/users', [UserController::class, 'index']);
});

// Combined example
Route::middleware(['auth', 'admin'])
    ->prefix('admin')
    ->name('admin.')
    ->namespace('App\Http\Controllers\Admin')
    ->group(function () {
        Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');
        Route::resource('posts', PostController::class);
    });

// Subdomain routing
Route::domain('{account}.example.com')->group(function () {
    Route::get('/dashboard', fn ($account) => $account);
});
```

---

## 3. Controllers

### Q9: Làm thế nào để validate request trong controller?

**A:** Sử dụng Form Request classes cho validation thay vì inline validation.

```php
// Form Request - Recommended
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
            'title' => 'required|string|max:255|unique:posts',
            'content' => 'required|string|min:10',
            'category_id' => 'required|exists:categories,id',
            'tags' => 'array',
            'tags.*' => 'exists:tags,id',
            'featured_image' => 'nullable|image|max:2048',
        ];
    }

    public function messages(): array
    {
        return [
            'title.unique' => 'This title is already taken.',
            'content.min' => 'Content must be at least 10 characters.',
        ];
    }

    public function withValidator(Validator $validator): void
    {
        $validator->after(function ($validator) {
            if ($this->hasInvalidCombination()) {
                $validator->errors()->add('tags', 'Invalid tag combination.');
            }
        });
    }
}

// Controller
class PostController extends Controller
{
    public function store(CreatePostRequest $request): JsonResponse
    {
        // Request đã được validated
        $validated = $request->validated();
        
        $post = $this->postService->create($validated);
        
        return (new PostResource($post))
            ->response()
            ->setStatusCode(201);
    }
}

// Inline validation - Chỉ cho simple cases
public function store(Request $request): JsonResponse
{
    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'content' => 'required|string',
    ]);
    
    // Hoặc với custom messages
    $validated = $request->validateWithBag('post', [
        'title' => 'required|string|max:255',
    ], [
        'title.required' => 'A title is required.',
    ]);
}
```

### Q10: Khi nào nên sử dụng API Resource classes?

**A:** Sử dụng API Resources khi building APIs để transform models thành consistent JSON responses.

```php
// app/Http/Resources/PostResource.php
class PostResource extends JsonResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'slug' => $this->slug,
            'content' => $this->when($request->user()?->isAdmin(), $this->content),
            'author' => new UserResource($this->whenLoaded('author')),
            'comments_count' => $this->when(
                isset($this->comments_count),
                $this->comments_count
            ),
            'created_at' => $this->created_at->toIso8601String(),
            'updated_at' => $this->updated_at->toIso8601String(),
        ];
    }

    public function with($request): array
    {
        return [
            'meta' => [
                'currency' => 'USD',
            ],
        ];
    }
}

// app/Http/Resources/PostCollection.php
class PostCollection extends ResourceCollection
{
    public $collects = PostResource::class;
    
    public function toArray($request): array
    {
        return [
            'data' => $this->collection,
            'meta' => [
                'total' => $this->total(),
            ],
        ];
    }
}

// Controller usage
class PostController extends Controller
{
    public function index(): PostCollection
    {
        $posts = Post::with(['author', 'tags'])
            ->published()
            ->latest()
            ->paginate(20);
        
        return new PostCollection($posts);
    }
    
    public function show(Post $post): PostResource
    {
        return new PostResource($post->load(['author', 'comments']));
    }
}
```

---

## 4. Authentication

### Q11: Sự khác biệt giữa Auth::check() và Auth::user()?

**A:** Cả hai là methods trên Auth facade nhưng return different values.

```php
// Auth::check() - Kiểm tra user có logged in không (boolean)
if (Auth::check()) {
    // User đã đăng nhập
}

// Tương đương với
if (auth()->check()) {
    // User đã đăng nhập
}

// Auth::user() - Lấy currently authenticated user
$user = Auth::user();
// Trả về User model hoặc null

// Kết hợp check và user
if (Auth::check() && Auth::user()->isAdmin()) {
    // Admin user đã đăng nhập
}

// Trong Controller - automatically available
class PostController extends Controller
{
    public function store(Request $request): JsonResponse
    {
        // Lấy user từ request (recommended)
        $user = $request->user();
        
        // Hoặc từ Auth facade
        $user = Auth::user();
        
        // Check authentication
        if ($request->user()) {
            // User is authenticated
        }
    }
}

// Middleware - Authenticate user
Route::middleware('auth')->group(function () {
    // Routes chỉ accessible bởi authenticated users
});
```

### Q12: Làm thế nào để implement custom authentication?

**A:** Có nhiều approaches tùy thuộc vào requirements.

```php
// Using Laravel Fortify (Recommended for custom auth)
// Register in config/auth.php guards
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

// Manual authentication
class LoginController extends Controller
{
    public function authenticate(Request $request): RedirectResponse
    {
        $credentials = $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);

        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();
            
            return redirect()->intended('/dashboard');
        }

        return back()->withErrors([
            'email' => 'The provided credentials do not match our records.',
        ])->onlyInput('email');
    }
}

// Using Auth::login()
$user = User::where('email', $email)->first();

if ($user && Hash::check($password, $user->password)) {
    Auth::login($user);
    // User is now authenticated
}

// Remember me
Auth::attempt($credentials, $request->boolean('remember'));

// Logout
Auth::logout();
$request->session()->invalidate();
$request->session()->regenerateToken();

// Auth via ID
Auth::loginUsingId(1);
```

---

## 5. Database

### Q13: Làm thế nào để tạo và chạy migrations?

**A:** Migrations là version control cho database schema.

```php
// Tạo migration mới
php artisan make:migration create_posts_table
php artisan make:migration add_avatar_to_users_table --table=users

// Migration file structure
// database/migrations/2024_01_01_000001_create_posts_table.php
class CreatePostsTable extends Migration
{
    public function up(): void
    {
        Schema::create('posts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->string('title');
            $table->text('content');
            $table->timestamp('published_at')->nullable();
            $table->timestamps();
            $table->softDeletes();
            
            // Indexes
            $table->index(['user_id', 'published_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('posts');
    }
}

// Chạy migrations
php artisan migrate
php artisan migrate --force  // Production (bypass confirmation)
php artisan migrate --pretend  // Xem SQL without executing

// Rollback
php artisan migrate:rollback     // Rollback last batch
php artisan migrate:rollback --step=5  // Rollback 5 batches
php artisan migrate:reset       // Rollback all migrations

// Fresh - Drop all tables và migrate again
php artisan migrate:fresh  // Không chạy seeders
php artisan migrate:fresh --seed

// Status
php artisan migrate:status

// Refresh (rollback + migrate)
php artisan migrate:refresh
php artisan migrate:refresh --seed
```

### Q14: Sự khác biệt giữa whereHas và has trong Eloquent?

**A:** `whereHas` filter parent models based on relationship conditions, `has` chỉ kiểm tra existence.

```php
// has - Chỉ lọc parent có relationship
$users = User::has('posts')->get();
// Lấy users có ít nhất 1 post

$users = User::has('posts', '>=', 3)->get();
// Lấy users có 3+ posts

// whereHas - Filter với conditions trên related models
$users = User::whereHas('posts', function ($query) {
    $query->where('published', true);
})->get();
// Lấy users có ít nhất 1 published post

$users = User::whereHas('posts', function ($query) {
    $query->where('title', 'like', '%Laravel%');
}, '>=', 2)->get();
// Lấy users có 2+ posts có "Laravel" trong title

// orWhereHas - OR condition
$users = User::whereHas('posts', fn ($q) => $q->where('published', true))
    ->orWhereHas('videos', fn ($q) => $q->where('published', true))
    ->get();

// withCount với whereHas
$users = User::whereHas('posts', fn ($q) => $q->where('published', true))
    ->withCount('posts')
    ->having('posts_count', '>', 0)
    ->get();

//doesntHave - Users không có posts
$users = User::doesntHave('posts')->get();
```

### Q15: Làm thế nào để tạo database seeders và factories?

**A:** Seeders và Factories tạo test data cho development và testing.

```php
// Factory - database/factories/PostFactory.php
class PostFactory extends Factory
{
    public function definition(): array
    {
        return [
            'title' => fake()->sentence(),
            'content' => fake()->paragraphs(3, true),
            'user_id' => User::factory(),
            'published_at' => fake()->randomElement([
                now(),
                null,
                fake()->dateTimeBetween('-1 year', 'now'),
            ]),
        ];
    }
    
    public function published(): static
    {
        return $this->state(fn (array $attributes) => [
            'published_at' => now(),
        ]);
    }
    
    public function unpublished(): static
    {
        return $this->state(fn (array $attributes) => [
            'published_at' => null,
        ]);
    }
}

// Seeder - database/seeders/PostSeeder.php
class PostSeeder extends Seeder
{
    public function run(): void
    {
        User::factory()
            ->count(10)
            ->hasPosts(5)  // Each user has 5 posts
            ->create();
            
        // Or standalone
        Post::factory()->count(50)->create();
        Post::factory()->published()->count(30)->create();
    }
}

// Main Seeder - database/seeders/DatabaseSeeder.php
class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $this->call([
            UserSeeder::class,
            CategorySeeder::class,
            PostSeeder::class,
            CommentSeeder::class,
        ]);
    }
}

// Running seeders
php artisan db:seed
php artisan db:seed --class=UserSeeder
php artisan migrate:fresh --seed
```

---

## 6. Forms & Views

### Q16: Làm thế nào để handle file uploads trong Laravel?

**A:** Laravel cung cấp convenient methods cho file upload với validation.

```php
// Blade Form
<form method="POST" enctype="multipart/form-data">
    @csrf
    <input type="file" name="avatar">
    <input type="file" name="documents[]" multiple>
</form>

// Controller - Basic upload
public function store(Request $request): RedirectResponse
{
    $request->validate([
        'avatar' => 'required|image|mimes:jpg,jpeg,png,gif|max:2048',
        'documents.*' => 'nullable|file|mimes:pdf,doc,docx|max:5120',
    ]);
    
    // Single file
    $path = $request->file('avatar')->store('avatars', 'public');
    
    // Multiple files
    $paths = [];
    foreach ($request->file('documents') as $document) {
        $paths[] = $document->store('documents', 'public');
    }
    
    // Custom filename
    $path = $request->file('avatar')->storeAs(
        'avatars',
        auth()->id() . '_' . time() . '.jpg',
        'public'
    );
    
    return redirect()->back()->with('success', 'Uploaded successfully');
}

// Storage
// config/filesystems.php - Define disks
'disks' => [
    'local' => [
        'driver' => 'local',
        'root' => storage_path('app'),
    ],
    'public' => [
        'driver' => 'local',
        'root' => storage_path('app/public'),
        'url' => env('APP_URL').'/storage',
        'visibility' => 'public',
    ],
    's3' => [
        'driver' => 's3',
        // S3 configuration
    ],
],

// Link storage (for public access)
php artisan storage:link

// Delete file
Storage::disk('public')->delete($path);

// Get URL
$url = Storage::disk('public')->url($path);
```

### Q17: CSRF protection hoạt động như thế nào?

**A:** CSRF tokens ngăn chặn cross-site request forgery attacks bằng cách verify request origin.

```php
// Blade - Auto include CSRF token
<form method="POST">
    @csrf  <!-- Generates hidden input with token -->
    <!-- Hoặc trong meta tag cho AJAX -->
    <meta name="csrf-token" content="{{ csrf_token() }}">
</form>

// AJAX - Send CSRF token
// Với jQuery
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});

// Với fetch
fetch('/api/data', {
    method: 'POST',
    headers: {
        'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content
    },
    body: JSON.stringify({ name: 'John' })
});

// Routes exempt từ CSRF (thường là webhooks)
Route::post('/webhook/stripe', [WebhookController::class, 'handle'])
    ->withoutMiddleware([\App\Http\Middleware\VerifyCsrfToken::class]);

// Hoặc exclude trong middleware
// app/Http/Middleware/VerifyCsrfToken.php
protected $except = [
    'webhook/*',
    'api/*',
];
```

---

## 7. Security

### Q18: Làm thế nào để prevent SQL injection trong Laravel?

**A:** Laravel tự động ngăn chặn SQL injection khi sử dụng Eloquent và Query Builder đúng cách.

```php
// ✅ SAFE - Eloquent (Recommended)
$user = User::where('email', $email)->first();
$posts = Post::where('category_id', $categoryId)->get();

// ✅ SAFE - Query Builder với bindings
$users = DB::table('users')
    ->where('email', $email)  // Parameterized automatically
    ->where('id', '>', 100)
    ->get();

// ✅ SAFE - Raw queries với bindings
$users = DB::select(
    'SELECT * FROM users WHERE email = ? AND active = ?',
    [$email, true]
);

// ❌ UNSAFE - Raw queries without bindings
$users = DB::select("SELECT * FROM users WHERE email = '$email'");
// KHÔNG LÀM ĐIỀU NÀY!

// LIKE queries
$users = User::where('name', 'like', '%' . $search . '%')->get();
// Search input được parameterized

// OrderBy với user input - Cần validate
$allowedColumns = ['name', 'email', 'created_at'];
$column = in_array($request->get('sort'), $allowedColumns) 
    ? $request->get('sort') 
    : 'name';

$users = User::orderBy($column)->get();

// IN clauses
$ids = [1, 2, 3];
$users = User::whereIn('id', $ids)->get();

// Dynamic IN clauses
$ids = $request->input('ids', []);
$users = User::whereIn('id', $ids)->get();
```

### Q19: Làm thế nào để implement rate limiting?

**A:** Rate limiting ngăn chặn abuse bằng cách giới hạn requests per time window.

```php
// Rate Limiter Configuration
// app/Providers/AppServiceProvider.php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

public function boot(): void
{
    // Basic rate limit
    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(60)->by($request->ip());
    });
    
    // Per user rate limit
    RateLimiter::for('users', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });
    
    // Specific endpoints
    RateLimiter::for('login', function (Request $request) {
        return Limit::perMinute(5)->by($request->ip());
    });
    
    // API endpoints
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });
    
    // Custom response
    RateLimiter::for('expensive', function (Request $request) {
        return Limit::perMinute(10)
            ->by($request->ip())
            ->response(function () {
                return response('Too many requests', 429);
            });
    });
}

// Apply to routes
Route::middleware('throttle:global')->group(function () {
    // Rate limited routes
});

Route::middleware('throttle:login')->group(function () {
    Route::post('/login', [AuthController::class, 'login']);
});

Route::middleware('throttle:60,1')->group(function () {  // 60 requests per minute
    Route::get('/api/data', [DataController::class, 'index']);
});

// Custom throttle per route
Route::middleware('throttle:expensive')->get('/reports', [ReportController::class, 'generate']);
```

---

## 8. Testing

### Q20: Làm thế nào để viết unit tests trong Laravel?

**A:** Laravel tích hợp với PHPUnit cho testing với conventions và helpers.

```php
// tests/Unit/Services/OrderCalculationServiceTest.php
class OrderCalculationServiceTest extends TestCase
{
    use RefreshDatabase;  // Reset database for each test

    private OrderCalculationService $calculator;

    protected function setUp(): void
    {
        parent::setUp();
        $this->calculator = new OrderCalculationService();
    }

    public function test_calculates_subtotal_correctly(): void
    {
        $items = collect([
            ['price' => 10.00, 'quantity' => 2],
            ['price' => 5.50, 'quantity' => 3],
        ]);
        
        $result = $this->calculator->calculateSubtotal($items);
        
        $this->assertEquals(36.50, $result);
    }

    public function test_applies_discount_for_large_orders(): void
    {
        $subtotal = 500.00;
        
        $result = $this->calculator->calculateDiscount($subtotal);
        
        $this->assertEquals(50.00, $result); // 10% discount for orders > $100
    }

    public function test_throws_exception_for_negative_amounts(): void
    {
        $this->expectException(InvalidAmountException::class);
        
        $this->calculator->process(-10.00);
    }

    public function test_rounds_to_two_decimal_places(): void
    {
        $result = $this->calculator->calculateTax(100.555);
        
        $this->assertEquals(10.06, $result); // Rounded up
    }
}

// tests/Feature/Api/PostApiTest.php
class PostApiTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_create_post(): void
    {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user)
            ->postJson('/api/posts', [
                'title' => 'My Post',
                'content' => 'Post content here',
            ]);
        
        $response->assertCreated()
            ->assertJsonPath('data.title', 'My Post');
        
        $this->assertDatabaseHas('posts', [
            'title' => 'My Post',
            'user_id' => $user->id,
        ]);
    }

    public function test_unauthenticated_user_cannot_create_post(): void
    {
        $response = $this->postJson('/api/posts', [
            'title' => 'My Post',
            'content' => 'Post content',
        ]);
        
        $response->assertUnauthorized();
    }

    public function test_post_creation_validates_required_fields(): void
    {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user)
            ->postJson('/api/posts', []);
        
        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['title', 'content']);
    }
}

// Running tests
php artisan test                    // Run all tests
php artisan test --filter=test_name  // Filter by name
php artisan test --filter=OrderTest  // Filter by class
php artisan test tests/Unit/        // Specific folder
```

---

## 9. Performance

### Q21: Làm thế nào để optimize database queries?

**A:** Multiple strategies để improve query performance.

```php
// 1. Eager Loading - Prevent N+1
// ❌ Bad
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->author->name;
}

// ✅ Good
$posts = Post::with('author')->get();

// 2. Select only needed columns
$users = User::select(['id', 'name', 'email'])->get();

// 3. Indexes for frequently queried columns
// In migration
$table->index(['status', 'created_at']);
$table->unique('email');

// 4. Chunking for large datasets
Post::chunk(100, function ($posts) {
    foreach ($posts as $post) {
        // Process each chunk
    }
});

// Or cursor for memory efficiency
foreach (Post::cursor() as $post) {
    // Process each record
}

// 5. Caching
$users = Cache::remember('users:active', 3600, function () {
    return User::where('active', true)->get();
});

// 6. Query optimization
// Explain query
DB::enableQueryLog();
$users = User::with(['posts'])->get();
Log::info(DB::getQueryLog());

// Use exists() instead of count()
if (User::where('email', $email)->exists()) {
    // User exists
}

// Use latest() with limit
$recentPosts = Post::latest()->limit(5)->get();
```

### Q22: Khi nào nên sử dụng caching?

**A:** Caching improve performance cho expensive operations và frequently accessed data.

```php
// Cache expensive queries
$posts = Cache::remember('posts:popular', now()->addMinutes(30), function () {
    return Post::with(['author', 'tags'])
        ->published()
        ->popular()
        ->limit(10)
        ->get();
});

// Cache configuration data
$settings = Cache::rememberForever('settings', function () {
    return Setting::all()->pluck('value', 'key')->toArray();
});

// Cache with tags (for invalidation)
Cache::tags(['posts', 'category:1'])->remember($key, $ttl, $callback);

// Invalidation
Cache::tags(['posts'])->flush();  // Invalidate all posts cache
Cache::forget('posts:popular');   // Invalidate specific key

// View caching (compile once)
php artisan view:cache

// Config caching (load once)
php artisan config:cache

// Route caching (parse once)
php artisan route:cache

// Clear all caches
php artisan cache:clear
php artisan config:clear
php artisan route:clear
php artisan view:clear
php artisan optimize:clear
```

---

## 10. Configuration

### Q23: Sự khác biệt giữa .env và config files?

**A:** `.env` chứa environment-specific values, config files chứa application configuration structure.

```php
// .env - Environment variables
APP_NAME="My Application"
APP_ENV=local
APP_KEY=base64:xxx
APP_DEBUG=true
APP_URL=http://localhost

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=myapp
DB_USERNAME=root
DB_PASSWORD=secret

CACHE_DRIVER=redis
QUEUE_CONNECTION=redis

// config/app.php - Configuration structure
return [
    'name' => env('APP_NAME', 'Laravel'),
    'env' => env('APP_ENV', 'production'),
    'debug' => (bool) env('APP_DEBUG', false),
    'url' => env('APP_URL', 'http://localhost'),
    'timezone' => 'UTC',
    'locale' => 'en',
    // ...
];

// Accessing config
config('app.name');        // Get value
config('app.timezone');   // Get with default

// Caching config
php artisan config:cache  // Combine all configs into single file
php artisan config:clear // Remove cache

// Configuration best practices
// ✅ Use env() in config files
return [
    'driver' => env('CACHE_DRIVER', 'file'),
];

// ❌ Don't use env() directly in application code
$value = env('APP_NAME'); // Bad practice
$value = config('app.name'); // Good practice
```

### Q24: Làm thế nào để tạo custom configuration file?

**A:** Tạo config file và access qua config helper.

```php
// config/services.php - Already exists
return [
    'stripe' => [
        'key' => env('STRIPE_KEY'),
        'secret' => env('STRIPE_SECRET'),
    ],
];

// Create custom config
// config/integration.php
return [
    'api' => [
        'base_url' => env('INTEGRATION_API_URL'),
        'key' => env('INTEGRATION_API_KEY'),
        'timeout' => env('INTEGRATION_TIMEOUT', 30),
    ],
    'sync' => [
        'enabled' => env('INTEGRATION_SYNC_ENABLED', true),
        'interval' => env('INTEGRATION_SYNC_INTERVAL', 60),
    ],
];

// Access in code
$apiKey = config('integration.api.key');
$timeout = config('integration.api.timeout', 30); // Default value

// Publish config for packages
// In package service provider
public function boot(): void
{
    $this->publishes([
        __DIR__ . '/../../config/integration.php' => config_path('integration.php'),
    ]);
}

// Override in .env
INTEGRATION_API_KEY=your_api_key
INTEGRATION_TIMEOUT=60
```

---

## 11. Common Errors

### Q25: "Target class does not exist" error - Cách fix?

**A:** Lỗi này thường do missing service provider hoặc incorrect binding.

```php
// Common causes và solutions:

// 1. Missing Service Provider
// config/app.php
'providers' => [
    // ...
    App\Providers\CustomServiceProvider::class,
],

// 2. Incorrect interface binding
// app/Providers/AppServiceProvider.php
public function register(): void
{
    $this->app->bind(
        OrderRepositoryInterface::class,
        EloquentOrderRepository::class
    );
}

// 3. Typo in class name
// ❌ Wrong
$this->app->make('App\Http\Controllers\PostController')

// ✅ Correct
$this->app->make(\App\Http\Controllers\PostController::class)

// 4. Using facade without importing
use Illuminate\Support\Facades\Route;

// 5. Missing middleware registration
// app/Http/Kernel.php
protected $middlewareAliases = [
    'custom' => \App\Http\Middleware\CustomMiddleware::class,
];

// 6. Cache issue
php artisan config:clear
php artisan cache:clear
php artisan clear-compiled
```

### Q26: "Mass Assignment Exception" - Cách fix?

**A:** Cần định nghĩa `$fillable` hoặc `$guarded` trong model.

```php
// Model - Define fillable fields
class User extends Model
{
    protected $fillable = [
        'name',
        'email',
        'password',
    ];
    
    // OR use guarded (inverse)
    protected $guarded = [
        'id',
        'is_admin',
        'created_at',
        'updated_at',
    ];
}

// Controller - Use validated data
public function store(CreateUserRequest $request): JsonResponse
{
    // ✅ Safe - Only validated fields
    $user = User::create($request->validated());
    
    // ❌ Unsafe - Could throw exception
    $user = User::create($request->all());
}

// When you need to set protected fields
$user = new User();
$user->forceFill([
    'email' => $request->email,
    'is_admin' => true, // This would fail with mass assignment
]);
$user->save(); // Need to use save() or forceFill()
```

---

## References

- [Laravel Documentation](https://laravel.com/docs)
- [Laracasts](https://laracasts.com/)
- [Laravel News](https://laravel-news.com/)
- [Laravel Package Development](https://laravelpackage.com/)
