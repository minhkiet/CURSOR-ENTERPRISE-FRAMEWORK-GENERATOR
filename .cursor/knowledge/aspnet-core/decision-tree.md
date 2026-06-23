---
title: "ASP.NET Core Decision Tree - Cây Quyết Định ASP.NET Core"
description: "Cây quyết định chi tiết cho việc chọn patterns, architectures, và best practices trong ASP.NET Core"
tags: ["aspnet-core", "decision-tree", "architecture", "patterns", "best-practices"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# ASP.NET Core Decision Tree - Cây Quyết Định ASP.NET Core

## Tổng Quan

Việc đưa ra quyết định kiến trúc và design decisions là một phần quan trọng trong phát triển phần mềm. Mỗi quyết định đều có trade-offs và context-specific factors cần consider. Decision tree này cung cấp một systematic approach để navigate qua các common decisions trong ASP.NET Core development.

Tài liệu này được thiết kế như một practical guide mà developers có thể reference khi faced với các technical decisions. Thay vì chỉ provide answers, nó giúp bạn think through the decision-making process bằng cách highlight các questions cần ask và factors cần consider.

Mỗi decision tree bắt đầu với một question và branches ra based on different scenarios, providing recommendations với reasoning. Các recommendations không phải là absolute rules mà là guidelines dựa trên common scenarios và best practices.

## Mục Đích

1. **Systematic Decision Making**: Cung cấp structured approach cho technical decisions
2. **Knowledge Transfer**: Help team members understand rationale behind decisions
3. **Consistency**: Ensure consistent decisions across the codebase
4. **Quick Reference**: Fast lookup cho common scenarios
5. **Trade-off Understanding**: Highlight pros và cons của different approaches

---

## 1. Dependency Injection Lifetime Decision

```
Bạn cần register một service trong DI container?
│
├── Service có state cần persist across requests?
│   ├── YES ────────────────────────────────────────────────────→ **Xem xét: Singleton**
│   │   │   └── ⚠️ WARNING: Chỉ sử dụng nếu service là thread-safe
│   │   │   └── ✅ Use cases: Configuration, Logger, Cache
│   │   │   └── ❌ AVOID: DbContext, scoped services
│   │   │
│   │   └── Nhưng state đó có liên quan đến HTTP request không?
│   │       ├── YES ───────────────────────────────────────────→ **Scoped**
│   │       │   └── ✅ Use cases: User context, Request-scoped cache
│   │       │
│   │       └── NO (truly global state)
│   │           └── **Singleton** ✅
│   │               └── ✅ Use cases: Application-wide configuration
│   │
│   └── NO (stateless service)
│       │
│       └── Service cần DbContext hoặc database access?
│           ├── YES ───────────────────────────────────────────→ **Scoped**
│           │   └── ✅ EF Core DbContext là Scoped by design
│           │
│           └── NO
│               │
│               └── Service được used trong multiple operations trong một request?
│                   ├── YES ───────────────────────────────────→ **Scoped**
│                   │   └── ✅ Reuse same instance per request
│                   │
│                   └── NO (new instance per usage acceptable)
│                       │
│                       └── Service là lightweight và stateless?
│                           ├── YES ────────────────────────────→ **Transient**
│                           │   └── ✅ Use cases: Validators, DTO mappers
│                           │
│                           └── NO (có state, cần preserve per usage)
│                               └── **Scoped** ✅
```

### Detailed DI Lifetime Guidelines

| Lifetime | When Created | Use Cases | Examples |
|----------|--------------|-----------|----------|
| **Singleton** | First request | Stateless services, caches | `ILogger<T>`, `IOptions<T>`, `IConfiguration` |
| **Scoped** | Per HTTP request | Services with per-request state | `DbContext`, `IRepository<T>`, `IUserService` |
| **Transient** | Each injection | Lightweight stateless services | `IValidator<T>`, `IMapper`, `IDateTimeProvider` |

### Special Cases

```csharp
// ❌ WRONG: DbContext as Singleton
builder.Services.AddSingleton<DbContext>(); // MEMORY LEAK!

// ✅ CORRECT: DbContext as Scoped
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString));

// ⚠️ CAPTIVE DEPENDENCY: Singleton depending on Scoped
builder.Services.AddSingleton<ISingletonService, SingletonService>();
// SingletonService depends on Scoped service ❌ POTENTIAL ISSUE

// ✅ CORRECT: Scoped depending on Singleton
builder.Services.AddSingleton<ISingletonService, SingletonService>();
builder.Services.AddScoped<IScopedService, ScopedService>();

// If you MUST have Singleton depend on Scoped:
builder.Services.AddSingleton<Func<IScopedService>>(sp => 
    () => sp.CreateScope().ServiceProvider.GetRequiredService<IScopedService>());

// OR use IServiceScopeFactory
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
        // Use scopedService
    }
}
```

---

## 2. Controller vs Minimal API Decision

```
Bạn cần tạo một API endpoint?
│
├── API phức tạp với nhiều actions và behaviors?
│   ├── YES ────────────────────────────────────────────────────→ **Controller + [ApiController]**
│   │   └── ✅ Use when:
│   │       - Nhiều HTTP methods cho same resource
│   │       - Cần filters, authorization policies
│   │       - Cần detailed OpenAPI documentation
│   │       - Team familiar với MVC pattern
│   │
│   └── NO (simple endpoint)
│       │
│       └── Cần model binding và validation?
│           ├── YES ───────────────────────────────────────────→ **Minimal API với Request/Response types**
│           │   └── ✅ Modern approach với full ASP.NET Core features
│           │
│           └── NO (very simple, one-liner)
│               └── **Minimal API**
│                   └── ✅ Perfect for microservices, simple CRUD
```

### Comparison Matrix

| Aspect | Controller | Minimal API |
|--------|-----------|-------------|
| **Boilerplate** | More (class, attributes) | Less (delegate-based) |
| **Model Binding** | Automatic with [ApiController] | Automatic |
| **Validation** | Automatic with [ApiController] | Manual or via extension |
| **Filter Pipeline** | Full support | Limited |
| **OpenAPI** | Automatic | Automatic |
| **Testability** | Easy with mocks | Easy with HttpClient |
| **File Organization** | Separate files | Can be inline |
| **Best For** | Complex APIs, large teams | Simple services, microservices |

### Examples

```csharp
// CONTROLLER: Complex API with multiple actions
[ApiController]
[Route("api/[controller]")]
[Produces(MediaTypeNames.Application.Json)]
[Authorize(Policy = "ApiPolicy")]
public class OrdersController : ControllerBase
{
    private readonly IMediator _mediator;
    
    public OrdersController(IMediator mediator)
    {
        _mediator = mediator;
    }
    
    [HttpGet]
    [ProducesResponseType(typeof(PaginatedResponse<OrderDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<PaginatedResponse<OrderDto>>> GetOrders(
        [FromQuery] GetOrdersQuery query,
        CancellationToken ct)
    {
        var result = await _mediator.Send(query, ct);
        return Ok(result);
    }
    
    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(OrderDetailDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ETagCache]
    public async Task<ActionResult<OrderDetailDto>> GetOrder(Guid id, CancellationToken ct)
    {
        var result = await _mediator.Send(new GetOrderByIdQuery(id), ct);
        return result is null ? NotFound() : Ok(result);
    }
    
    [HttpPost]
    [ProducesResponseType(typeof(OrderDto), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<OrderDto>> CreateOrder(
        [FromBody] CreateOrderCommand command,
        CancellationToken ct)
    {
        var result = await _mediator.Send(command, ct);
        return CreatedAtAction(nameof(GetOrder), new { id = result.Value.Id }, result.Value);
    }
}

// MINIMAL API: Simple endpoint
app.MapGet("/products/{id:int}", async (int id, AppDbContext db, CancellationToken ct) =>
{
    var product = await db.Products.FindAsync(new object[] { id }, ct);
    return product is null ? Results.NotFound() : Results.Ok(product);
})
.WithName("GetProduct")
.WithOpenApi(operation =>
{
    operation.Description = "Get a product by ID";
    return operation;
});
```

---

## 3. Data Access Strategy Decision

```
Bạn cần access data?
│
├── Sử dụng relational database?
│   ├── YES
│   │   │
│   │   └── Cần ORM features (relationships, migrations, LINQ)?
│   │       ├── YES ───────────────────────────────────────────→ **Entity Framework Core**
│   │       │   └── ✅ Use when:
│   │       │       - Cần work với complex object graphs
│   │       │       - Cần migrations và schema management
│   │       │       - Team familiar với LINQ
│   │       │       - Cần cross-database portability
│   │       │
│   │       └── NO (simple queries, maximum performance)
│   │           └── **Dapper + Stored Procedures**
│   │               └── ✅ Use when:
│   │                   - Performance là critical
│   │                   - Mostly simple CRUD
│   │                   - Existing stored procedures
│   │                   - Team comfortable với SQL
│   │
│   └── NO (non-relational database)
│       │
│       └── Document database (MongoDB)?
│           ├── YES ───────────────────────────────────────────→ **MongoDB.Driver**
│           │
│           └── Key-value store (Redis)?
│               ├── YES ───────────────────────────────────────→ **StackExchange.Redis**
│               │
│               └── Other NoSQL?
│                   └── **Use appropriate driver**
```

### Data Access Technology Comparison

| Technology | Best For | Pros | Cons |
|------------|----------|------|------|
| **EF Core** | Most scenarios | Rich features, migrations, LINQ | Performance overhead |
| **Dapper** | Performance-critical | Fast, simple SQL | Manual mapping |
| **ADO.NET** | Maximum control | Full control, performance | Verbose code |
| **MongoDB.Driver** | Document stores | Native MongoDB features | Limited to MongoDB |
| **StackExchange.Redis** | Caching, sessions | Fast, flexible | Key-value only |

### EF Core Decision Sub-Tree

```
Sử dụng EF Core cho query?
│
├── Query là read-only (no updates)?
│   ├── YES ────────────────────────────────────────────────────→ **AsNoTracking()**
│   │   └── ✅ Performance improvement, no change tracking overhead
│   │
│   └── NO (need to update entities)
│       │
│       └── Cần track changes và relationships?
│           ├── YES ───────────────────────────────────────────→ **Default tracking**
│           │   └── ✅ Full change tracking capabilities
│           │
│           └── NO (simple update by ID)
│               └── **AsNoTrackingWithIdentityResolution()**
│                   └── ✅ Better performance với still tracking
```

---

## 4. Query Optimization Decision

```
Bạn có performance issue với query?
│
├── Query load nhiều related entities?
│   ├── YES ────────────────────────────────────────────────────→ **Kiểm tra Eager Loading**
│   │   │
│   │   └── Đang load trong loop (N+1)?
│   │       ├── YES ───────────────────────────────────────────→ **Include() + ThenInclude()**
│   │       │   └── ✅ Load all data in single query
│   │       │
│   │       └── NO (proper eager loading)
│   │           └── **Projection với Select()**
│   │               └── ✅ Select chỉ fields cần thiết
│   │
│   └── Query trả về nhiều records?
│       ├── YES ────────────────────────────────────────────→ **Pagination**
│       │   └── ✅ Skip/Take hoặc keyset pagination
│       │
│       └── NO (small dataset)
│           │
│           └── Query chậm với filter?
│               ├── YES ─────────────────────────────────────────→ **Kiểm tra Indexes**
│               │   └── ✅ Index trên filtered/sorted columns
│               │
│               └── NO
│                   └── **Kiểm tra Execution Plan**
│                       └── ✅ Identify missing indexes, table scans
```

### Query Optimization Checklist

```csharp
// ✅ BEFORE: N+1 Query Problem
var orders = await _context.Orders.ToListAsync();
foreach (var order in orders)
{
    var customer = await _context.Customers.FindAsync(order.CustomerId); // N queries!
}

// ✅ AFTER: Eager Loading
var orders = await _context.Orders
    .Include(o => o.Customer)
    .Include(o => o.Items)
        .ThenInclude(i => i.Product)
    .ToListAsync();

// ✅ AFTER: Projection (Even better)
var orders = await _context.Orders
    .Select(o => new OrderSummaryDto
    {
        OrderId = o.Id,
        CustomerName = o.Customer.Name,
        TotalAmount = o.TotalAmount,
        ItemCount = o.Items.Count
    })
    .ToListAsync();

// ✅ AFTER: Pagination
var orders = await _context.Orders
    .OrderByDescending(o => o.CreatedAt)
    .Skip(offset)
    .Take(pageSize)
    .ToListAsync();

// ✅ Add Index for commonly filtered columns
modelBuilder.Entity<Order>()
    .HasIndex(o => new { o.Status, o.CreatedAt })
    .HasDatabaseName("IX_Orders_Status_CreatedAt");
```

---

## 5. Caching Strategy Decision

```
Bạn cần implement caching?
│
├── Cache at what level?
│   │
│   ├── **Response Level** (entire response)
│   │   └── ✅ Use Output Caching (ASP.NET Core 7+) hoặc Response Caching
│   │       └── Perfect cho: API responses, static-ish data
│   │
│   ├── **Data Level** (query results)
│   │   │
│   │   └── Single instance application?
│   │       ├── YES ───────────────────────────────────────────→ **IMemoryCache**
│   │       │   └── ✅ Simple, in-process caching
│   │       │
│   │       └── NO (multiple instances/servers)
│   │           └── **Distributed Cache (Redis)**
│   │               └── ✅ Share cache across instances
│   │
│   └── **Object Level** (individual objects)
│       └── **Cache-aside pattern với Redis**
│           └── ✅ Fine-grained control, automatic serialization
```

### Caching Strategy Comparison

| Strategy | Scope | Performance | Complexity | Use Case |
|----------|-------|-------------|------------|----------|
| **Output Cache** | Entire response | Highest | Low | Public APIs, static data |
| **Memory Cache** | Per instance | High | Low | Single server apps |
| **Redis Cache** | Shared | High | Medium | Distributed systems |
| **No Cache** | N/A | Lowest | None | Real-time, personalized |

### Implementation Examples

```csharp
// OUTPUT CACHING (ASP.NET Core 7+)
builder.Services.AddOutputCache();

app.MapGet("/products", async (AppDbContext db) =>
{
    var products = await db.Products.AsNoTracking().ToListAsync();
    return Results.Ok(products);
})
.CacheOutput(policy => policy
    .Tag("products")
    .Expire(TimeSpan.FromMinutes(10)));

// Invalidation
app.MapPost("/products", async (CreateProductRequest request, 
    AppDbContext db, IOutputCacheStore cache, CancellationToken ct) =>
{
    // Create product...
    await cache.EvictByTagAsync("products", ct);
});

// MEMORY CACHE
public class ProductService
{
    private readonly IMemoryCache _cache;
    private static readonly TimeSpan CacheDuration = TimeSpan.FromMinutes(5);
    
    public async Task<ProductDto?> GetProductAsync(Guid id, CancellationToken ct)
    {
        var cacheKey = $"product:{id}";
        
        if (_cache.TryGetValue(cacheKey, out ProductDto? cached))
            return cached;
        
        var product = await _db.Products
            .AsNoTracking()
            .Where(p => p.Id == id)
            .Select(p => new ProductDto(p.Id, p.Name, p.Price))
            .FirstOrDefaultAsync(ct);
        
        if (product is not null)
            _cache.Set(cacheKey, product, CacheDuration);
        
        return product;
    }
}

// REDIS DISTRIBUTED CACHE
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

## 6. Error Handling Strategy Decision

```
Bạn cần handle exceptions?
│
├── Exception xảy ra trong controller?
│   ├── YES ────────────────────────────────────────────────────→ **Exception Handler Middleware**
│   │   └── ✅ Global exception handling, consistent responses
│   │
│   └── Exception xảy ra trong business logic?
│       │
│       ├── Business rule violation?
│       │   ├── YES ───────────────────────────────────────────→ **Custom Domain Exceptions**
│       │   │   └── ✅ Clear, typed exceptions for domain rules
│       │   │
│       │   └── Validation error?
│       │       ├── YES ───────────────────────────────────────→ **ValidationException**
│       │       │   └── ✅ Structured validation errors
│       │       │
│       │       └── Not found?
│       │           └── **NotFoundException** ✅
│       │
│       └── Infrastructure error?
│           └── **Let propagate to middleware**
│               └── ✅ Global handler formats response
```

### Error Handling Pattern

```csharp
// CUSTOM EXCEPTIONS
public class DomainException : Exception
{
    public string Code { get; }
    
    public DomainException(string code, string message) : base(message)
    {
        Code = code;
    }
}

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

// EXCEPTION HANDLER
public class GlobalExceptionHandler : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        var (statusCode, response) = exception switch
        {
            ValidationException ve => (400, new ErrorResponse 
            { 
                Type = "ValidationError",
                Errors = ve.Errors
            }),
            NotFoundException nf => (404, new ErrorResponse
            {
                Type = "NotFound",
                Message = nf.Message
            }),
            DomainException de => (400, new ErrorResponse
            {
                Type = "DomainError",
                Code = de.Code,
                Message = de.Message
            }),
            _ => (500, new ErrorResponse
            {
                Type = "InternalServerError",
                Message = "An unexpected error occurred"
            })
        };
        
        httpContext.Response.StatusCode = statusCode;
        await httpContext.Response.WriteAsJsonAsync(response, cancellationToken);
        
        return true;
    }
}
```

---

## 7. Authentication & Authorization Decision

```
Bạn cần bảo mật API endpoint?
│
├── Cần authentication?
│   ├── YES
│   │   │
│   │   └── API cho web/mobile clients?
│   │       ├── YES ───────────────────────────────────────────→ **JWT Bearer**
│   │       │   └── ✅ Stateless, scalable, industry standard
│   │       │
│   │       └── Server-to-server communication?
│   │           ├── YES ───────────────────────────────────────→ **API Key hoặc mTLS**
│   │           │   └── ✅ Simple, machine-to-machine auth
│   │           │
│   │           └── SPA (Single Page App)?
│   │               └── **Cookie + CSRF Protection** hoặc **JWT in memory**
│   │
│   └── NO
│       └── **Public endpoint** ✅
│
├── Cần authorization?
│   ├── YES
│   │   │
│   │   └── Đơn giản role-based?
│   │       ├── YES ───────────────────────────────────────────→ **Role-based Authorization**
│   │       │   └── ✅ [Authorize(Roles = "Admin")]
│   │       │
│   │       └── Phức tạp, nhiều conditions?
│   │           ├── YES ───────────────────────────────────────→ **Policy-based Authorization**
│   │           │   └── ✅ Custom IAuthorizationHandler
│   │           │
│   │           └── Resource-based?
│   │               └── **Resource-based Authorization**
│   │                   └── ✅ Check ownership in handler
│   │
│   └── NO
│       └── **AllowAnonymous** ✅
```

### Authorization Pattern Decision

```
Cần authorization với complex logic?
│
├── Simple: Check role/claim exists?
│   ├── YES ────────────────────────────────────────────────────→ **[Authorize(Roles = "Admin")]**
│   │   └── ✅ Simple, declarative
│   │
│   └── NO (complex conditions)
│       │
│       ├── Check multiple claims?
│       │   ├── YES ───────────────────────────────────────────→ **Policy + Requirements**
│       │   │   └── ✅ Combine multiple checks
│       │   │
│       │   └── Check resource ownership?
│       │       ├── YES ───────────────────────────────────────→ **IAuthorizationHandler với resource**
│       │       │   └── ✅ Check if user owns the resource
│       │       │
│       │       └── Check dynamic permissions?
│       │           └── **Permission-based system**
│       │               └── ✅ Database-driven permissions
```

### Implementation Examples

```csharp
// SIMPLE ROLE-BASED
[Authorize(Roles = "Admin")]
public IActionResult AdminOnly() { }

// MULTIPLE ROLES
[Authorize(Roles = "Admin,Manager")]
public IActionResult AdminOrManager() { }

// POLICY-BASED
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("CanManageOrders", policy =>
        policy.RequireAssertion(context =>
            context.User.HasClaim(c => c.Type == "Permission" && c.Value == "Orders.Manage") ||
            context.User.IsInRole("Admin")));
});

[Authorize(Policy = "CanManageOrders")]
public IActionResult ManageOrders() { }

// RESOURCE-BASED AUTHORIZATION
public class OrderAuthorizationHandler : AuthorizationHandler<OrderOperationRequirement, Order>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        OrderOperationRequirement requirement,
        Order order)
    {
        if (context.User.IsInRole("Admin"))
        {
            context.Succeed(requirement);
            return Task.CompletedTask;
        }
        
        // Check if user owns the order
        if (order.CustomerId == context.User.GetUserId())
        {
            context.Succeed(requirement);
        }
        
        return Task.CompletedTask;
    }
}

public class OrderOperationRequirement : IAuthorizationRequirement { }
```

---

## 8. API Versioning Decision

```
Bạn cần version API?
│
├── Breaking changes thường xuyên?
│   ├── YES ────────────────────────────────────────────────────→ **URL Versioning**
│   │   └── ✅ /api/v1/orders, /api/v2/orders
│   │       └── ✅ Clear, cache-friendly, easy routing
│   │
│   └── Breaking changes hiếm khi?
│       │
│       ├── Cần preserve original URLs?
│       │   ├── YES ───────────────────────────────────────────→ **Header Versioning**
│       │   │   └── ✅ API-Version: 2023-01-01
│       │   │
│       │   └── Performance important?
│       │       └── **Query String Versioning**
│       │           └── ✅ /api/orders?version=2023-01-01
│       │
│       └── Cần industry standard?
│           └── **OAS/Accept Header**
│               └── ✅ Accept: application/vnd.api.v2+json
```

### API Versioning Implementation

```csharp
// CONFIGURATION
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
    options.ApiVersionReader = ApiVersionReader.Combine(
        new UrlSegmentApiVersionReader(),
        new HeaderApiVersionReader("API-Version"),
        new QueryStringApiVersionReader("version"));
});

builder.Services.AddVersionedApiExplorer(options =>
{
    options.GroupNameFormat = "'v'VVV";
    options.SubstituteApiVersionInUrl = true;
});

// USAGE
[ApiController]
[Route("api/v{version:apiVersion}/[controller]")]
[ApiVersion("1.0")]
[ApiVersion("2.0")]
public class OrdersController : ControllerBase
{
    [HttpGet]
    [MapToApiVersion("1.0")]
    public ActionResult<IEnumerable<OrderV1Dto>> GetOrdersV1() { }
    
    [HttpGet]
    [MapToApiVersion("2.0")]
    public ActionResult<IEnumerable<OrderV2Dto>> GetOrdersV2() { }
}
```

---

## 9. Background Job Decision

```
Bạn cần run background processing?
│
├── Job cần persistence và reliability?
│   ├── YES ────────────────────────────────────────────────────→ **Hangfire / Quartz.NET**
│   │   └── ✅ Dashboard, retry logic, persistence
│   │
│   └── Simple, fire-and-forget?
│       │
│       ├── Short-running (< 30 seconds)?
│       │   ├── YES ───────────────────────────────────────────→ **Task.Run (fire-and-forget)**
│       │   │   └── ⚠️ WARNING: No reliability, only for non-critical
│       │   │
│       │   └── Long-running?
│       │       └── **IHostedService / BackgroundService**
│       │           └── ✅ Lifecycle tied to app, proper cancellation
│       │
│       └── Cần scheduling?
│           ├── YES ───────────────────────────────────────────→ **Hangfire Recurring Jobs**
│           │   └── ✅ Cron expressions, dashboard
│           │
│           └── Real-time processing?
│               └── **Message Queue (RabbitMQ, Azure Service Bus)**
│                   └── ✅ Decoupled, scalable, reliable
```

### Background Job Options

| Option | Persistence | Scheduling | Retry | Dashboard | Best For |
|--------|-------------|------------|-------|-----------|----------|
| **Task.Run** | None | No | No | No | Quick fire-and-forget |
| **BackgroundService** | None | No | Manual | No | Lifecycle-bound tasks |
| **Hangfire** | Yes | Yes | Yes | Yes | Most scenarios |
| **Quartz.NET** | Yes | Yes | Yes | No | Enterprise scheduling |
| **Message Queue** | Yes | Yes | Yes | Separate | Distributed systems |

### Implementation Examples

```csharp
// BACKGROUND SERVICE
public class OrderProcessingService : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            await ProcessOrdersAsync(stoppingToken);
            await Task.Delay(TimeSpan.FromSeconds(30), stoppingToken);
        }
    }
    
    private async Task ProcessOrdersAsync(CancellationToken ct)
    {
        using var scope = _serviceProvider.CreateScope();
        var orderService = scope.ServiceProvider.GetRequiredService<IOrderService>();
        await orderService.ProcessPendingOrdersAsync(ct);
    }
}

builder.Services.AddHostedService<OrderProcessingService>();

// HANGFIRE
builder.Services.AddHangfire(x => x.UseSqlServerStorage(connectionString));

app.UseHangfireDashboard();
app.UseHangfireServer();

// Fire-and-forget
BackgroundJob.Enqueue(() => Console.WriteLine("Fire-and-forget!"));

// Delayed
BackgroundJob.Schedule(() => Console.WriteLine("Delayed!"), TimeSpan.FromMinutes(5));

// Recurring
RecurringJob.AddOrUpdate("process-orders", () => ProcessOrders(), "*/5 * * * *");
```

---

## 10. Project Structure Decision

```
Bạn cần organize project structure?
│
├── Team size nhỏ, domain đơn giản?
│   ├── YES ────────────────────────────────────────────────────→ **Flat Structure**
│   │   └── ✅ Controllers/, Services/, Models/, Data/
│   │       └── Simple, quick to navigate
│   │
│   └── Team lớn, domain phức tạp?
│       │
│       ├── Cần strong separation of concerns?
│       │   ├── YES ───────────────────────────────────────────→ **Clean Architecture**
│       │   │   └── ✅ Domain/, Application/, Infrastructure/, Api/
│       │   │       └── Best for: Complex business logic, testability
│       │   │
│       │   └── Prefer feature-based organization?
│       │       └── **Vertical Slice Architecture**
│       │           └── ✅ Features/Orders/, Features/Products/
│       │               └── Best for: Team scaling, feature development
│       │
│       └── Cần tách read/write?
│           └── **CQRS + Clean Architecture**
│               └── ✅ Separate query và command models
```

### Project Structure Comparison

| Structure | Team Size | Complexity | Changes Needed | Best For |
|-----------|-----------|------------|----------------|----------|
| **Flat** | 1-5 | Low | Low | MVPs, prototypes |
| **Clean Architecture** | 5-20 | High | Medium | Enterprise, testability |
| **Vertical Slice** | Any | Medium | Low | Team scaling, features |
| **CQRS** | 10+ | Very High | High | High-scale read/write |

---

## 11. Async Pattern Decision

```
Bạn cần implement async operation?
│
├── I/O-bound operation (database, network, file)?
│   ├── YES ────────────────────────────────────────────────────→ **Async/Await Pattern**
│   │   └── ✅ Non-blocking, scalability
│   │
│   └── CPU-bound operation (computation)?
│       │
│       ├── Operation chạy nhanh (< 50ms)?
│       │   ├── YES ───────────────────────────────────────────→ **Sync (acceptable)**
│       │   │   └── ⚠️ Async overhead > benefit
│       │   │
│       │   └── Operation chạy lâu?
│       │       └── **Task.Run (offload to thread pool)**
│       │           └── ⚠️ WARNING: Don't block on it
│
├── Cần cancellation?
│   ├── YES ────────────────────────────────────────────────────→ **CancellationToken throughout**
│   │   └── ✅ Graceful cancellation, resource cleanup
│   │
│   └── NO
│       └── **Optional CancellationToken = default**
│           └── ✅ Backwards compatible
```

### Async Best Practices

```csharp
// ✅ CORRECT: Full async pipeline
[HttpGet]
public async Task<ActionResult<IEnumerable<ProductDto>>> GetProducts(
    CancellationToken cancellationToken)
{
    var products = await _context.Products
        .AsNoTracking()
        .Where(p => p.IsActive)
        .ToListAsync(cancellationToken);
    
    return Ok(products);
}

// ❌ WRONG: Blocking calls
// var products = _context.Products.ToListAsync().Result; // BLOCKS!

// ✅ CORRECT: Parallel async operations
public async Task<OrderSummaryDto> GetOrderSummaryAsync(Guid orderId, CancellationToken ct)
{
    var orderTask = _orderRepository.GetByIdAsync(orderId, ct);
    var statsTask = _orderRepository.GetStatsAsync(orderId, ct);
    
    await Task.WhenAll(orderTask, statsTask);
    
    return new OrderSummaryDto
    {
        Order = await orderTask,
        Stats = await statsTask
    };
}

// ✅ CORRECT: Timeout handling
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30));
try
{
    var result = await SomeLongRunningOperationAsync(cts.Token);
}
catch (OperationCanceledException)
{
    // Handle timeout
}
```

---

## 12. Database Connection Decision

```
Bạn cần kết nối database?
│
├── Entity Framework Core?
│   ├── YES
│   │   │
│   │   └── Use built-in connection resilience?
│   │       ├── YES ───────────────────────────────────────────→ **EnableRetryOnFailure**
│   │       │   └── ✅ Automatic retry với exponential backoff
│   │       │       └── Recommended for Azure SQL, unreliable networks
│   │       │
│   │       └── NO (stable network, need control)
│   │           └── **CommandTimeout configuration**
│   │               └── ✅ Set appropriate timeout
│   │
│   └── Raw ADO.NET?
│       └── **SqlConnection với using statement**
│           └── ✅ Ensure proper disposal
│
├── Connection pooling cần configure?
│   ├── YES ───────────────────────────────────────────────────→ **Connection String Settings**
│   │   └── Min Pool Size, Max Pool Size, Connection Timeout
│   │
│   └── NO
│       └── **Use defaults** ✅
```

### Connection Configuration Best Practices

```csharp
// EF Core with retry policy
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString, sqlOptions =>
    {
        sqlOptions.EnableRetryOnFailure(
            maxRetryCount: 3,
            maxRetryDelay: TimeSpan.FromSeconds(10),
            errorNumbersToAdd: null);
        sqlOptions.CommandTimeout(30);
    }));

// Connection string with pooling
"Server=tcp:server.database.windows.net;Database=MyDb;" +
"User Id=user@server;Password=password;" +
"Pooling=true;Min Pool Size=5;Max Pool Size=100;" +
"Connection Timeout=30;"

// Direct ADO.NET with proper disposal
public async Task<List<Order>> GetOrdersAsync(CancellationToken ct)
{
    await using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync(ct);
    
    await using var command = new SqlCommand("SELECT * FROM Orders", connection);
    await using var reader = await command.ExecuteReaderAsync(ct);
    
    var orders = new List<Order>();
    while (await reader.ReadAsync(ct))
    {
        orders.Add(MapToOrder(reader));
    }
    
    return orders;
}
```

---

## Quick Reference Summary

### Common Decisions Quick Lookup

| Decision | Quick Answer |
|----------|-------------|
| **Service Lifetime** | Scoped for most services, Singleton for stateless/utility |
| **API Type** | Controller for complex, Minimal for simple |
| **Data Access** | EF Core for most, Dapper for performance |
| **Caching** | Output Cache for responses, IMemoryCache for single-server |
| **Error Handling** | Global exception handler + custom exceptions |
| **Authentication** | JWT Bearer for APIs |
| **Background Jobs** | BackgroundService for simple, Hangfire for complex |
| **Project Structure** | Clean Architecture for enterprise, Vertical for teams |

### When in Doubt

- **Prefer async**: Non-blocking I/O improves scalability
- **Use DI**: Dependency injection improves testability
- **Add logging**: Structured logging aids debugging
- **Handle errors**: Global exception handling ensures consistency
- **Use cancellation tokens**: Proper cancellation prevents resource waste
- **Prefer interfaces**: Abstractions improve flexibility

---

## References

- [Microsoft Dependency Injection](https://docs.microsoft.com/aspnet/core/fundamentals/dependency-injection)
- [EF Core Performance](https://docs.microsoft.com/ef/core/performance/)
- [ASP.NET Core Caching](https://docs.microsoft.com/aspnet/core/performance/caching/)
- [Authentication in ASP.NET Core](https://docs.microsoft.com/aspnet/core/security/authentication/)
- [Background Tasks](https://docs.microsoft.com/aspnet/core/fundamentals/host/hosted-services)
