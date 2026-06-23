---
title: "ASP.NET Core FAQ - Câu Hỏi Thường Gặp"
description: "Câu hỏi thường gặp và câu trả lời chuyên sâu cho ASP.NET Core development"
tags: ["aspnet-core", "faq", "troubleshooting", "best-practices", "questions"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# ASP.NET Core FAQ - Câu Hỏi Thường Gặp

## Tổng Quan

Tài liệu này tổng hợp các câu hỏi thường gặp từ developers làm việc với ASP.NET Core, kèm theo câu trả lời chi tiết và practical examples. Mỗi câu hỏi được chọn lọc dựa trên real-world usage và common pain points trong quá trình phát triển.

Các câu hỏi được tổ chức theo topics để dễ dàng reference. Mỗi answer không chỉ provide direct solution mà còn giải thích "why" đằng sau recommendation để bạn có thể apply knowledge một cách hiệu quả trong các scenarios khác nhau.

## Mục Đích

1. **Quick Answers**: Tìm kiếm nhanh các giải pháp cho common issues
2. **Deep Dives**: Hiểu sâu hơn về các concepts và patterns
3. **Best Practices**: Nắm vững recommended approaches
4. **Troubleshooting**: Debug và fix common problems
5. **Learning Path**: Resource cho developers mới học ASP.NET Core

---

## 1. Dependency Injection

### Q1: Sự khác biệt giữa AddSingleton, AddScoped, và AddTransient là gì?

**A:**

Đây là ba service lifetimes trong ASP.NET Core DI container:

| Lifetime | Created | Disposed | Use Cases |
|----------|---------|----------|-----------|
| **Singleton** | First time requested | Application shutdown | Configuration, Logger, Cache |
| **Scoped** | Each HTTP request | End of request | DbContext, Repositories, Services |
| **Transient** | Each injection | When disposed | Validators, DTOs, Lightweight services |

**Ví dụ:**

```csharp
// Singleton - Một instance cho toàn bộ app lifetime
builder.Services.AddSingleton<IAppSettings, AppSettings>();
builder.Services.AddSingleton<ILogger>(LoggerFactory.Create(b => b.AddConsole()));

// Scoped - Một instance per HTTP request
builder.Services.AddScoped<IOrderRepository, OrderRepository>();
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString), ServiceLifetime.Scoped);

// Transient - Instance mới mỗi lần được inject
builder.Services.AddTransient<IDateTimeProvider, DateTimeProvider>();
builder.Services.AddTransient<IValidator<CreateOrderCommand>, CreateOrderCommandValidator>();
```

**Tại sao quan trọng:**

```csharp
// ❌ WRONG: DbContext as Singleton - Causes memory leaks và race conditions!
builder.Services.AddSingleton<DbContext>(); // NEVER DO THIS

// ✅ CORRECT: DbContext as Scoped - Được design cho per-request lifetime
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString));
// DbContext is automatically scoped

// ⚠️ Captive Dependency: Singleton phụ thuộc Scoped
// Đây là pattern cần tránh:
builder.Services.AddSingleton<ISingletonService, SingletonService>();
// Nếu SingletonService inject Scoped service → potential issues!

// ✅ CORRECT: Nếu cần scoped service trong singleton, sử dụng IServiceScopeFactory
public class SingletonService
{
    private readonly IServiceScopeFactory _scopeFactory;
    
    public SingletonService(IServiceScopeFactory scopeFactory)
    {
        _scopeFactory = scopeFactory;
    }
    
    public void DoWork()
    {
        using var scope = _scopeFactory.CreateScope();
        var scopedService = scope.ServiceProvider.GetRequiredService<IScopedService>();
        // Use scopedService within a scope
    }
}
```

---

### Q2: Làm thế nào để resolve services theo thứ tự?

**A:**

Sử dụng `IServiceScopeFactory` để tạo scopes và resolve services theo thời điểm cần thiết:

```csharp
public class BatchProcessingService : IHostedService
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly ILogger<BatchProcessingService> _logger;
    
    public BatchProcessingService(
        IServiceScopeFactory scopeFactory,
        ILogger<BatchProcessingService> logger)
    {
        _scopeFactory = scopeFactory;
        _logger = logger;
    }
    
    public async Task StartAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Batch processing starting");
        
        // Tạo scope mới cho batch operation
        using var scope = _scopeFactory.CreateScope();
        var orderService = scope.ServiceProvider.GetRequiredService<IOrderService>();
        
        await orderService.ProcessPendingOrdersAsync(cancellationToken);
        
        _logger.LogInformation("Batch processing completed");
    }
}
```

---

### Q3: Làm thế nào để inject một service vào middleware?

**A:**

Middleware có constructor injection tương tự như services:

```csharp
public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;
    private readonly IMetricsService _metrics;
    
    public RequestLoggingMiddleware(
        RequestDelegate next,
        ILogger<RequestLoggingMiddleware> logger,
        IMetricsService metrics)
    {
        _next = next;
        _logger = logger;
        _metrics = metrics;
    }
    
    public async Task InvokeAsync(HttpContext context)
    {
        var stopwatch = Stopwatch.StartNew();
        var requestPath = context.Request.Path;
        
        try
        {
            await _next(context);
        }
        finally
        {
            stopwatch.Stop();
            _metrics.RecordRequestDuration(requestPath, stopwatch.ElapsedMilliseconds);
            _logger.LogInformation(
                "Request {Method} {Path} completed in {ElapsedMs}ms with status {StatusCode}",
                context.Request.Method,
                requestPath,
                stopwatch.ElapsedMilliseconds,
                context.Response.StatusCode);
        }
    }
}
```

---

## 2. Controllers và Routing

### Q4: [ApiController] attribute làm gì?

**A:**

`[ApiController]` là một attribute kích hoạt several API-specific behaviors:

1. **Automatic model validation**: Trả về 400 Bad Request nếu model invalid
2. **Binding source inference**: Tự động xác định source của parameters
3. **Problem Details response**: Trả về RFC 7807 compliant error format
4. **Attribute routing required**: Tất cả actions phải có route

**Ví dụ:**

```csharp
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    // Không cần [FromBody] vì automatic inference
    [HttpPost]
    public async Task<ActionResult<OrderDto>> CreateOrder(
        CreateOrderRequest request, // Tự động bind từ body
        CancellationToken cancellationToken) // Tự động bind từ request
    {
        // Nếu request không valid, tự động trả về:
        // {
        //     "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1",
        //     "title": "One or more validation errors occurred.",
        //     "status": 400,
        //     "errors": { "CustomerId": ["Customer ID is required"] }
        // }
        
        var result = await _mediator.Send(request, cancellationToken);
        return Ok(result);
    }
}
```

---

### Q5: Làm thế nào để return các HTTP status codes khác nhau?

**A:**

ASP.NET Core cung cấp nhiều helper methods cho returning responses:

```csharp
[HttpGet("{id}")]
public async Task<ActionResult<OrderDto>> GetOrder(Guid id, CancellationToken ct)
{
    var order = await _orderService.GetByIdAsync(id, ct);
    
    if (order is null)
        return NotFound(); // 404 - Resource not found
        
    return Ok(order); // 200 - Success
}

[HttpPost]
public async Task<ActionResult<OrderDto>> CreateOrder(
    CreateOrderRequest request,
    CancellationToken ct)
{
    if (!ModelState.IsValid)
        return ValidationProblem(ModelState); // 400 with errors
        
    var order = await _orderService.CreateAsync(request, ct);
    
    return CreatedAtAction( // 201 - Created
        nameof(GetOrder),
        new { id = order.Id },
        order);
}

[HttpDelete("{id}")]
public async Task<IActionResult> DeleteOrder(Guid id, CancellationToken ct)
{
    var deleted = await _orderService.DeleteAsync(id, ct);
    
    if (!deleted)
        return NotFound(); // 404
        
    return NoContent(); // 204 - Success, no content
}

[HttpGet]
public async Task<ActionResult<IEnumerable<OrderDto>>> GetOrders(
    [FromQuery] OrderStatus? status,
    CancellationToken ct)
{
    var orders = await _orderService.GetAllAsync(status, ct);
    return Ok(orders); // 200
}

// Custom status codes
[HttpGet("processing")]
public IActionResult GetProcessingStatus()
{
    return StatusCode(StatusCodes.Status202Accepted, "Processing started");
}
```

**Common Status Code Methods:**

| Method | Status Code | Use Case |
|--------|-------------|----------|
| `Ok()` | 200 | Successful GET |
| `CreatedAtAction()` | 201 | Resource created |
| `NoContent()` | 204 | Successful DELETE |
| `BadRequest()` | 400 | Invalid input |
| `Unauthorized()` | 401 | Not authenticated |
| `Forbid()` | 403 | Not authorized |
| `NotFound()` | 404 | Resource not found |
| `Conflict()` | 409 | Resource conflict |
| `UnprocessableEntity()` | 422 | Validation failed |
| `StatusCode()` | Custom | Any status code |

---

### Q6: Làm thế nào để implement async streaming responses?

**A:**

Sử dụng `IAsyncEnumerable<T>` hoặc `FileStream` cho streaming:

```csharp
// JSON Streaming với IAsyncEnumerable
[HttpGet("stream")]
public async IAsyncEnumerable<OrderDto> StreamOrders(
    [FromQuery] DateTime? since,
    [FromServices] IOrderStreamService streamService,
    [EnumeratorCancellation] CancellationToken ct)
{
    await foreach (var order in streamService.StreamOrdersAsync(since, ct))
    {
        yield return order;
    }
}

// CSV Streaming
[HttpGet("export")]
public async Task<IActionResult> ExportOrders(
    [FromQuery] DateTime startDate,
    [FromQuery] DateTime endDate,
    CancellationToken ct)
{
    var fileName = $"orders-{startDate:yyyyMMdd}-{endDate:yyyyMMdd}.csv";
    
    Response.ContentType = "text/csv";
    Response.Headers.ContentDisposition = $"attachment; filename=\"{fileName}\"";
    
    await using var writer = new StreamWriter(Response.Body);
    await writer.WriteLineAsync("OrderId,CustomerId,Total,Status,CreatedAt");
    
    await foreach (var order in _orderService.StreamOrdersAsync(startDate, endDate, ct))
    {
        await writer.WriteLineAsync(
            $"{order.Id},{order.CustomerId},{order.Total},{order.Status},{order.CreatedAt:O}");
        await writer.FlushAsync(ct);
    }
}
```

---

## 3. Entity Framework Core

### Q7: Sự khác biệt giữa AsNoTracking(), AsNoTrackingWithIdentityResolution(), và tracking (default) là gì?

**A:**

| Mode | Change Tracking | Identity Resolution | Performance | Use Case |
|------|----------------|---------------------|-------------|----------|
| **Default (Tracking)** | Yes | Yes | Slowest | Updates needed |
| **AsNoTracking()** | No | No | Fastest | Read-only queries |
| **AsNoTrackingWithIdentityResolution()** | No | Yes | Medium | Read with navigation |

```csharp
public class OrderService
{
    private readonly ApplicationDbContext _context;
    
    // Read-only query - Use AsNoTracking
    public async Task<List<OrderDto>> GetOrdersAsync(CancellationToken ct)
    {
        return await _context.Orders
            .AsNoTracking() // Không track entities - performance tốt nhất
            .Where(o => o.Status == OrderStatus.Pending)
            .OrderByDescending(o => o.CreatedAt)
            .Select(o => new OrderDto
            {
                Id = o.Id,
                Total = o.TotalAmount
            })
            .ToListAsync(ct);
    }
    
    // Need to update - Use default tracking
    public async Task UpdateOrderStatusAsync(Guid orderId, OrderStatus status, CancellationToken ct)
    {
        var order = await _context.Orders // Track entity - default
            .FirstOrDefaultAsync(o => o.Id == orderId, ct);
        
        if (order is not null)
        {
            order.Status = status; // Change tracked và sẽ được save
            await _context.SaveChangesAsync(ct);
        }
    }
    
    // Read but need navigation property resolution - Use AsNoTrackingWithIdentityResolution
    public async Task<List<OrderDto>> GetOrdersWithCustomerAsync(CancellationToken ct)
    {
        return await _context.Orders
            .AsNoTrackingWithIdentityResolution() // Track references for navigation
            .Include(o => o.Customer)
            .Select(o => new OrderDto
            {
                Id = o.Id,
                CustomerName = o.Customer.Name // Navigation resolution
            })
            .ToListAsync(ct);
    }
}
```

---

### Q8: Làm thế nào để implement soft delete?

**A:**

Có hai approaches chính: Query Filters và Global Filters:

```csharp
// Approach 1: Query Filters (Recommended)
public class SoftDeleteEntity
{
    public bool IsDeleted { get; set; }
    public DateTime? DeletedAt { get; set; }
}

public class ApplicationDbContext : DbContext
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Global query filter cho tất cả entities implement ISoftDelete
        modelBuilder.Entity<ISoftDelete>(entity =>
        {
            entity.HasQueryFilter(e => !e.IsDeleted);
        });
    }
}

// Usage
public class Order : ISoftDelete
{
    public Guid Id { get; set; }
    public bool IsDeleted { get; private set; }
    public DateTime? DeletedAt { get; private set; }
    
    public void SoftDelete()
    {
        IsDeleted = true;
        DeletedAt = DateTime.UtcNow;
    }
}

// Query automatically filtered
var orders = await _context.Orders.ToListAsync(); // Không include deleted

// Bypass filter when needed
var allOrders = await _context.Orders
    .IgnoreQueryFilters() // Include deleted
    .Where(o => o.IsDeleted)
    .ToListAsync();

// Approach 2: Query specification
public static class QuerySpecifications
{
    public static IQueryable<T> NotDeleted<T>(this IQueryable<T> query)
        where T : ISoftDelete
    {
        return query.Where(e => !e.IsDeleted);
    }
}
```

---

### Q9: Transaction với EF Core như thế nào?

**A:**

```csharp
public class OrderService
{
    private readonly ApplicationDbContext _context;
    
    public async Task<Result<OrderDto>> CreateOrderAsync(
        CreateOrderCommand command,
        CancellationToken ct)
    {
        // Simple transaction
        await using var transaction = await _context.Database.BeginTransactionAsync(ct);
        
        try
        {
            var order = Order.Create(command.CustomerId);
            
            foreach (var item in command.Items)
            {
                var product = await _context.Products.FindAsync(new object[] { item.ProductId }, ct);
                order.AddItem(product, item.Quantity);
            }
            
            _context.Orders.Add(order);
            await _context.SaveChangesAsync(ct);
            
            // Commit nếu mọi thứ OK
            await transaction.CommitAsync(ct);
            
            return Result.Success(_mapper.Map<OrderDto>(order));
        }
        catch (Exception ex)
        {
            // Rollback tự động khi dispose nếu chưa commit
            _logger.LogError(ex, "Failed to create order");
            return Result.Failure<OrderDto>("Failed to create order");
        }
    }
    
    // Transaction với Isolation Level
    public async Task<Result> TransferFundsAsync(
        Guid fromAccountId,
        Guid toAccountId,
        decimal amount,
        CancellationToken ct)
    {
        await using var transaction = await _context.Database.BeginTransactionAsync(
            IsolationLevel.Serializable, // Highest isolation
            ct);
        
        try
        {
            var fromAccount = await _context.Accounts
                .FirstOrDefaultAsync(a => a.Id == fromAccountId, ct);
            
            var toAccount = await _context.Accounts
                .FirstOrDefaultAsync(a => a.Id == toAccountId, ct);
            
            if (fromAccount.Balance < amount)
                return Result.Failure("Insufficient funds");
            
            fromAccount.Balance -= amount;
            toAccount.Balance += amount;
            
            await _context.SaveChangesAsync(ct);
            await transaction.CommitAsync(ct);
            
            return Result.Success();
        }
        catch
        {
            // Transaction automatically rolled back
            throw;
        }
    }
}
```

---

### Q10: EF Core migration best practices?

**A:**

```bash
# Create migration
dotnet ef migrations add InitialCreate --context ApplicationDbContext

# Add additional migration
dotnet ef migrations add AddOrderStatus --context ApplicationDbContext

# Generate SQL script (for production deployment)
dotnet ef migrations script --context ApplicationDbContext --output migration.sql

# Apply migrations programmatically
public async Task ApplyMigrationsAsync(IServiceProvider services)
{
    using var scope = services.CreateScope();
    var db = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
    
    var pending = await db.Database.GetPendingMigrationsAsync();
    if (pending.Any())
    {
        await db.Database.MigrateAsync();
    }
}

// Use in Program.cs
var app = builder.Build();
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
    await db.Database.EnsureCreatedAsync(); // For development only
    // OR
    await db.Database.MigrateAsync(); // For production
}
```

---

## 4. Configuration và Environment

### Q11: Làm thế nào để access configuration values?

**A:**

```csharp
// Approach 1: IOptions<T> (Recommended for typed settings)
builder.Services.Configure<AppSettings>(
    builder.Configuration.GetSection("AppSettings"));

public class ProductService
{
    private readonly AppSettings _settings;
    
    public ProductService(IOptions<AppSettings> settings)
    {
        _settings = settings.Value;
    }
    
    public int GetMaxPageSize() => _settings.MaxPageSize;
}

// Approach 2: IOptions<T>.Value (Direct access)
var maxSize = app.Services.GetRequiredService<IOptions<AppSettings>>().Value.MaxPageSize;

// Approach 3: Configuration directly (for simple cases)
var connectionString = builder.Configuration.GetConnectionString("Default");

// Approach 4: Environment variables
// AppSettings__MaxPageSize=50
var maxPageSize = builder.Configuration["AppSettings:MaxPageSize"];

// appsettings.json
{
  "AppSettings": {
    "MaxPageSize": 100,
    "EnableCache": true,
    "Features": {
      "NewCheckout": false
    }
  }
}
```

---

### Q12: Sự khác biệt giữa Development, Staging, và Production environments?

**A:**

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Environment-specific configuration
if (builder.Environment.IsDevelopment())
{
    // Development-only services
    builder.Services.AddSwaggerGen();
    builder.Services.AddDatabaseDeveloperPageExceptionHandler();
}

if (builder.Environment.IsProduction())
{
    // Production-only configuration
    builder.WebHost.UseUrls("http://+:80");
}

// Environment-specific startup
var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
    app.UseSwagger();
    app.UseSwaggerUI();
}
else
{
    app.UseExceptionHandler("/error");
    app.UseHsts();
}

// Environment variable
// ASPNETCORE_ENVIRONMENT=Production
```

| Environment | Use For | Features |
|-------------|---------|----------|
| **Development** | Local dev | Debugging, Swagger, hot reload |
| **Staging** | Pre-production testing | Production-like, test data |
| **Production** | Live application | Optimized, no debug info |

---

## 5. Authentication và Authorization

### Q13: JWT authentication được implement như thế nào?

**A:**

```csharp
// 1. Configuration
builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuer = true,
        ValidateAudience = true,
        ValidateLifetime = true,
        ValidateIssuerSigningKey = true,
        ValidIssuer = builder.Configuration["Jwt:Issuer"],
        ValidAudience = builder.Configuration["Jwt:Audience"],
        IssuerSigningKey = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]!)),
        ClockSkew = TimeSpan.FromMinutes(1)
    };
});

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AdminOnly", policy => policy.RequireRole("Admin"));
    options.AddPolicy("CanManageOrders", policy => 
        policy.RequireAssertion(context =>
            context.User.HasClaim("Permission", "Orders.Manage") ||
            context.User.IsInRole("Admin")));
});

// 2. Token Generation
public class TokenService : ITokenService
{
    public string GenerateToken(User user, IEnumerable<string> roles)
    {
        var claims = new List<Claim>
        {
            new(ClaimTypes.NameIdentifier, user.Id.ToString()),
            new(ClaimTypes.Email, user.Email),
            new(ClaimTypes.Name, user.FullName)
        };
        
        foreach (var role in roles)
        {
            claims.Add(new Claim(ClaimTypes.Role, role));
        }
        
        claims.Add(new Claim("Permission", "Orders.Manage"));
        
        var key = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(_configuration["Jwt:Key"]!));
        var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
        
        var token = new JwtSecurityToken(
            issuer: _configuration["Jwt:Issuer"],
            audience: _configuration["Jwt:Audience"],
            claims: claims,
            expires: DateTime.UtcNow.AddHours(1),
            signingCredentials: credentials);
        
        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}

// 3. Usage in Controller
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    [HttpGet]
    [Authorize] // Requires authentication
    public async Task<IActionResult> GetOrders() { }
    
    [HttpPost]
    [Authorize(Policy = "AdminOnly")] // Requires Admin role
    public async Task<IActionResult> CreateOrder() { }
    
    [HttpDelete("{id}")]
    [Authorize(Policy = "CanManageOrders")] // Requires permission
    public async Task<IActionResult> DeleteOrder() { }
}
```

---

### Q14: Làm thế nào để implement policy-based authorization?

**A:**

```csharp
// 1. Define Requirement
public class MinimumAgeRequirement : IAuthorizationRequirement
{
    public int MinimumAge { get; }
    
    public MinimumAgeRequirement(int minimumAge)
    {
        MinimumAge = minimumAge;
    }
}

// 2. Implement Handler
public class MinimumAgeHandler : AuthorizationHandler<MinimumAgeRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        MinimumAgeRequirement requirement)
    {
        var birthDateClaim = context.User.FindFirst("BirthDate");
        
        if (birthDateClaim is not null &&
            DateTime.TryParse(birthDateClaim.Value, out var birthDate))
        {
            var age = DateTime.Today.Year - birthDate.Year;
            
            if (birthDate.Date > DateTime.Today.AddYears(-age))
                age--;
            
            if (age >= requirement.MinimumAge)
            {
                context.Succeed(requirement);
            }
        }
        
        return Task.CompletedTask;
    }
}

// 3. Register
builder.Services.AddScoped<IAuthorizationHandler, MinimumAgeHandler>();

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("MinimumAge21", policy =>
        policy.Requirements.Add(new MinimumAgeRequirement(21)));
});

// 4. Usage
[HttpGet("alcohol")]
[Authorize(Policy = "MinimumAge21")]
public IActionResult GetAlcoholProducts() { }
```

---

## 6. Performance và Caching

### Q15: Làm thế nào để implement output caching?

**A:**

```csharp
// 1. Configuration (ASP.NET Core 7+)
builder.Services.AddOutputCache();

var app = builder.Build();

app.UseOutputCache();

// 2. Basic caching
app.MapGet("/api/products", async (AppDbContext db) =>
{
    var products = await db.Products.AsNoTracking().ToListAsync();
    return Results.Ok(products);
})
.CacheOutput(policy => policy
    .Expire(TimeSpan.FromMinutes(5)));

// 3. Caching với vary by query
app.MapGet("/api/products/search", async (
    string? category,
    decimal? minPrice,
    AppDbContext db) =>
{
    var query = db.Products.AsNoTracking();
    
    if (!string.IsNullOrEmpty(category))
        query = query.Where(p => p.Category == category);
    
    if (minPrice.HasValue)
        query = query.Where(p => p.Price >= minPrice.Value);
    
    var products = await query.ToListAsync();
    return Results.Ok(products);
})
.CacheOutput(policy => policy
    .VaryByQueryKeys("category", "minPrice")
    .Tag("products")
    .Expire(TimeSpan.FromMinutes(5)));

// 4. Cache invalidation
app.MapPost("/api/products", async (
    CreateProductRequest request,
    AppDbContext db,
    IOutputCacheStore cache,
    CancellationToken ct) =>
{
    var product = new Product { Name = request.Name, Price = request.Price };
    db.Products.Add(product);
    await db.SaveChangesAsync(ct);
    
    // Invalidate all cached endpoints tagged "products"
    await cache.EvictByTagAsync("products", ct);
    
    return Results.Created($"/api/products/{product.Id}", product);
});
```

---

### Q16: Memory cache vs Redis cache - khi nào nên dùng?

**A:**

| Scenario | Memory Cache | Redis Cache |
|----------|-------------|-------------|
| Single instance | ✅ Perfect | ✅ Works |
| Multiple instances | ❌ Not shared | ✅ Shared |
| Containerized apps | ❌ Not persistent | ✅ Persistent |
| Session storage | ❌ Lost on restart | ✅ Survives restart |
| Performance | Faster (in-process) | Network latency |
| Complexity | Lower | Higher |

```csharp
// Memory Cache (IMemoryCache)
builder.Services.AddMemoryCache();

public class ProductService
{
    private readonly IMemoryCache _cache;
    
    public async Task<ProductDto?> GetProductAsync(Guid id, CancellationToken ct)
    {
        var cacheKey = $"product:{id}";
        
        if (_cache.TryGetValue(cacheKey, out ProductDto? cached))
            return cached;
        
        var product = await _db.Products.FindAsync(new object[] { id }, ct);
        
        if (product is not null)
        {
            _cache.Set(cacheKey, product, TimeSpan.FromMinutes(5));
        }
        
        return product;
    }
}

// Redis Cache (IDistributedCache)
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration.GetConnectionString("Redis");
    options.InstanceName = "MyApp:";
});

public class ProductService
{
    private readonly IDistributedCache _cache;
    
    public async Task<ProductDto?> GetProductAsync(Guid id, CancellationToken ct)
    {
        var cacheKey = $"product:{id}";
        var cached = await _cache.GetStringAsync(cacheKey);
        
        if (cached is not null)
            return JsonSerializer.Deserialize<ProductDto>(cached);
        
        var product = await _db.Products.FindAsync(new object[] { id }, ct);
        
        if (product is not null)
        {
            var serialized = JsonSerializer.Serialize(product);
            await _cache.SetStringAsync(cacheKey, serialized,
                new DistributedCacheEntryOptions
                {
                    AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5)
                });
        }
        
        return product;
    }
}
```

---

## 7. Testing

### Q17: Làm thế nào để test controllers?

**A:**

```csharp
// Unit Test với Mock
public class OrdersControllerTests
{
    private readonly Mock<IMediator> _mediator;
    private readonly OrdersController _controller;
    
    public OrdersControllerTests()
    {
        _mediator = new Mock<IMediator>();
        _controller = new OrdersController(_mediator.Object);
    }
    
    [Fact]
    public async Task GetOrder_WithValidId_ReturnsOk()
    {
        // Arrange
        var orderId = Guid.NewGuid();
        var orderDto = new OrderDto { Id = orderId, Total = 100 };
        
        _mediator
            .Setup(m => m.Send(It.IsAny<GetOrderByIdQuery>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(orderDto);
        
        // Act
        var result = await _controller.GetOrder(orderId, CancellationToken.None);
        
        // Assert
        var okResult = result.Result.Should().BeOfType<OkObjectResult>().Subject;
        var returnedOrder = okResult.Value.Should().BeOfType<OrderDto>().Subject;
        returnedOrder.Id.Should().Be(orderId);
    }
    
    [Fact]
    public async Task GetOrder_WithInvalidId_ReturnsNotFound()
    {
        // Arrange
        var orderId = Guid.NewGuid();
        
        _mediator
            .Setup(m => m.Send(It.IsAny<GetOrderByIdQuery>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync((OrderDto?)null);
        
        // Act
        var result = await _controller.GetOrder(orderId, CancellationToken.None);
        
        // Assert
        result.Result.Should().BeOfType<NotFoundResult>();
    }
}

// Integration Test với WebApplicationFactory
public class OrdersControllerIntegrationTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;
    private readonly HttpClient _client;
    
    public OrdersControllerIntegrationTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                services.RemoveAll(typeof(DbContextOptions<ApplicationDbContext>));
                services.AddDbContext<ApplicationDbContext>(options =>
                    options.UseInMemoryDatabase("TestDb"));
            });
        });
        
        _client = _factory.CreateClient();
    }
    
    [Fact]
    public async Task CreateOrder_WithValidRequest_ReturnsCreated()
    {
        // Arrange
        var request = new CreateOrderRequest
        {
            CustomerId = Guid.NewGuid(),
            Items = new List<OrderItemDto>
            {
                new() { ProductId = Guid.NewGuid(), Quantity = 1 }
            }
        };
        
        // Act
        var response = await _client.PostAsJsonAsync("/api/orders", request);
        
        // Assert
        response.StatusCode.Should().Be(StatusCodes.Status201Created);
        
        var order = await response.Content.ReadFromJsonAsync<OrderDto>();
        order.Should().NotBeNull();
    }
}
```

---

## 8. Logging và Monitoring

### Q18: Structured logging là gì và implement như thế nào?

**A:**

Structured logging cho phép log messages với named parameters thay vì string interpolation, enabling better searching và analysis:

```csharp
// ❌ BAD: String interpolation (hard to search)
_logger.LogInformation($"Order {order.Id} created for customer {customer.Name}");

// ✅ GOOD: Structured logging (easily searchable)
_logger.LogInformation(
    "Order {OrderId} created for customer {CustomerName}",
    order.Id,
    customer.Name);

// Structured logging output (JSON)
{
    "Timestamp": "2024-01-15T10:30:00Z",
    "Level": "Information",
    "Message": "Order {OrderId} created for customer {CustomerName}",
    "OrderId": "abc-123",
    "CustomerName": "John Doe"
}

// Configuration
builder.Services.AddLogging(options =>
{
    options.AddConsole(options =>
    {
        options.FormatterName = "json"; // Use JSON formatter
    });
    options.AddDebug();
    
    options.Filter = (category, logLevel) =>
        logLevel >= LogLevel.Information ||
        category.Contains("MyApp"); // Include app logs at all levels
});

// Custom log levels per category
builder.Logging.AddFilter("Microsoft", LogLevel.Warning);
builder.Logging.AddFilter("Microsoft.EntityFrameworkCore", LogLevel.Warning);
builder.Logging.AddFilter("MyApp.Services", LogLevel.Debug);
```

---

### Q19: Health checks nên implement như thế nào?

**A:**

```csharp
// 1. Configuration
builder.Services.AddHealthChecks()
    .AddDbContextCheck<ApplicationDbContext>("database")
    .AddRedis(builder.Configuration.GetConnectionString("Redis"), "cache")
    .AddUrlGroup(
        new Uri("https://api.example.com/health"),
        name: "external-api",
        failureStatus: HealthStatus.Degraded,
        tags: new[] { "external" })
    .AddCheck<CustomHealthCheck>("custom");

// 2. Custom health check
public class CustomHealthCheck : IHealthCheck
{
    private readonly IServiceProvider _serviceProvider;
    
    public CustomHealthCheck(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }
    
    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            using var scope = _serviceProvider.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
            
            if (!await db.Database.CanConnectAsync(cancellationToken))
                return HealthCheckResult.Unhealthy("Cannot connect to database");
            
            var pendingOrders = await db.Orders
                .CountAsync(o => o.Status == OrderStatus.Pending, cancellationToken);
            
            if (pendingOrders > 1000)
                return HealthCheckResult.Degraded($"High pending orders: {pendingOrders}");
            
            return HealthCheckResult.Healthy();
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("Health check failed", ex);
        }
    }
}

// 3. Endpoints
app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = async (context, report) =>
    {
        context.Response.ContentType = "application/json";
        await context.Response.WriteAsJsonAsync(new
        {
            status = report.Status.ToString(),
            timestamp = DateTime.UtcNow,
            checks = report.Entries.Select(e => new
            {
                name = e.Key,
                status = e.Value.Status.ToString(),
                duration = $"{e.Value.Duration.TotalMilliseconds}ms",
                description = e.Value.Description
            })
        });
    }
});

// 4. Kubernetes probes
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false // Liveness - just confirms app is running
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("database") // Readiness - dependencies
});
```

---

## 9. Error Handling

### Q20: Global exception handling implement như thế nào?

**A:**

```csharp
// 1. Custom Exception Types
public class ValidationException : Exception
{
    public Dictionary<string, string[]> Errors { get; }
    
    public ValidationException(Dictionary<string, string[]> errors)
        : base("One or more validation errors occurred")
    {
        Errors = errors;
    }
}

public class NotFoundException : Exception
{
    public string ResourceType { get; }
    public object ResourceId { get; }
    
    public NotFoundException(string resourceType, object resourceId)
        : base($"{resourceType} with ID '{resourceId}' was not found")
    {
        ResourceType = resourceType;
        ResourceId = resourceId;
    }
}

// 2. Exception Handler
public class GlobalExceptionHandler : IExceptionHandler
{
    private readonly ILogger<GlobalExceptionHandler> _logger;
    private readonly IHostEnvironment _environment;
    
    public GlobalExceptionHandler(
        ILogger<GlobalExceptionHandler> logger,
        IHostEnvironment environment)
    {
        _logger = logger;
        _environment = environment;
    }
    
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        var correlationId = httpContext.TraceIdentifier;
        
        var (statusCode, response) = exception switch
        {
            ValidationException ve => (400, new ErrorResponse
            {
                Type = "ValidationError",
                Title = "Validation failed",
                Errors = ve.Errors
            }),
            NotFoundException nf => (404, new ErrorResponse
            {
                Type = "NotFound",
                Title = nf.Message
            }),
            UnauthorizedException ue => (401, new ErrorResponse
            {
                Type = "Unauthorized",
                Title = ue.Message
            }),
            _ => (500, new ErrorResponse
            {
                Type = "InternalServerError",
                Title = _environment.IsDevelopment() 
                    ? exception.Message 
                    : "An unexpected error occurred"
            })
        };
        
        _logger.LogError(exception,
            "Unhandled exception. CorrelationId: {CorrelationId}, StatusCode: {StatusCode}",
            correlationId,
            statusCode);
        
        httpContext.Response.StatusCode = statusCode;
        await httpContext.Response.WriteAsJsonAsync(response, cancellationToken);
        
        return true;
    }
}

public class ErrorResponse
{
    public string Type { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty;
    public string? Detail { get; set; }
    public Dictionary<string, string[]>? Errors { get; set; }
}

// 3. Registration
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();

var app = builder.Build();

app.UseExceptionHandler(); // Uses registered handler
```

---

## 10. Common Troubleshooting

### Q21: "Cannot resolve service" error - làm sao fix?

**A:**

Lỗi này xảy ra khi DI container không thể resolve một service. Common causes:

```csharp
// ❌ CAUSE 1: Service not registered
// Error: "Unable to resolve service for type 'IOrderService'"

// Fix: Register the service
builder.Services.AddScoped<IOrderService, OrderService>();

// ❌ CAUSE 2: Wrong interface
// Error: "Unable to resolve service for type 'IOrderService'"

// Fix: Make sure you're registering the interface, not the implementation
builder.Services.AddScoped<IOrderService, OrderService>(); // ✅ Correct
// builder.Services.AddScoped<OrderService>(); // ❌ Wrong

// ❌ CAUSE 3: Missing dependency in registration
// Error: "Unable to resolve service for type 'ISubService' while attempting to activate 'OrderService'"

// Fix: Ensure all dependencies are registered
builder.Services.AddScoped<ISubService, SubService>();
builder.Services.AddScoped<IOrderService, OrderService>();

// ❌ CAUSE 4: Captive dependency
// Error: "Cannot consume scoped service from singleton"

// Fix: Use IServiceScopeFactory for scoped services in singleton
public class SingletonService
{
    private readonly IServiceScopeFactory _scopeFactory;
    
    public SingletonService(IServiceScopeFactory scopeFactory)
    {
        _scopeFactory = scopeFactory;
    }
    
    public void DoWork()
    {
        using var scope = _scopeFactory.CreateScope();
        var scopedService = scope.ServiceProvider.GetRequiredService<IScopedService>();
    }
}
```

---

### Q22: Memory leak với DbContext - làm sao debug?

**A:**

Common causes của DbContext memory leaks:

```csharp
// ❌ CAUSE 1: DbContext as Singleton
builder.Services.AddSingleton<DbContext>(); // NEVER DO THIS

// ✅ FIX: DbContext as Scoped
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString));

// ❌ CAUSE 2: Large result sets without pagination
public async Task<IActionResult> GetAllProducts()
{
    var products = await _context.Products.ToListAsync(); // Memory leak if millions of rows!
    return Ok(products);
}

// ✅ FIX: Always paginate large queries
public async Task<IActionResult> GetProducts([FromQuery] int page = 1, [FromQuery] int pageSize = 20)
{
    pageSize = Math.Clamp(pageSize, 1, 100);
    
    var products = await _context.Products
        .AsNoTracking()
        .OrderBy(p => p.Name)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ToListAsync();
    
    return Ok(products);
}

// ❌ CAUSE 3: Tracking many entities
public async Task<IActionResult> GetLargeDataset()
{
    var data = await _context.LargeTable.ToListAsync(); // All tracked!
    return Ok(data);
}

// ✅ FIX: Use AsNoTracking for read-only
public async Task<IActionResult> GetLargeDataset()
{
    var data = await _context.LargeTable
        .AsNoTracking() // Don't track
        .ToListAsync();
    return Ok(data);
}

// Debugging tips:
// 1. Check ChangeTracker entries
var entries = _context.ChangeTracker.Entries().Count();

// 2. Clear tracker manually if needed
_context.ChangeTracker.Clear();

// 3. Use memory profiler to identify leaks
```

---

### Q23: "An item with the same key has already been added" - fix như thế nào?

**A:**

Đây thường là lỗi khi add duplicate items vào một dictionary hoặc khi configure services multiple times:

```csharp
// ❌ CAUSE 1: Duplicate service registration
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddScoped<IOrderService, OrderService>(); // Duplicate!

// ✅ FIX: Use TryAdd instead
builder.Services.TryAddScoped<IOrderService, OrderService>();
builder.Services.TryAddScoped<IOrderService, OrderService>(); // Ignored

// ❌ CAUSE 2: Add same endpoint multiple times
app.MapGet("/products", async (AppDbContext db) => await db.Products.ToListAsync());
app.MapGet("/products", async (AppDbContext db) => await db.Products.ToListAsync()); // Duplicate!

// ✅ FIX: Check for duplicates before adding
if (!app.Urls.Contains("http://localhost:5000"))
{
    app.Urls.Add("http://localhost:5000");
}

// ❌ CAUSE 3: Duplicate configuration
modelBuilder.Entity<Order>(entity =>
{
    entity.HasKey(e => e.Id);
    entity.HasKey(e => e.Id); // Duplicate!
});

// ✅ FIX: Use separate configurations
modelBuilder.Entity<Order>(entity =>
{
    entity.HasKey(e => e.Id);
    // other configurations
});
```

---

## References

- [ASP.NET Core Documentation](https://docs.microsoft.com/aspnet/core)
- [Entity Framework Core Documentation](https://docs.microsoft.com/ef/core)
- [ASP.NET Core Security](https://docs.microsoft.com/aspnet/core/security/)
- [Testing in ASP.NET Core](https://docs.microsoft.com/aspnet/core/test/)
- [Performance Best Practices](https://docs.microsoft.com/aspnet/core/performance/)
