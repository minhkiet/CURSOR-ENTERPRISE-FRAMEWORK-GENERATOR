---
title: "ASP.NET Core Best Practices - Thực Hành Tốt Nhất"
description: "Hướng dẫn toàn diện về các best practices cho phát triển ứng dụng ASP.NET Core production-ready"
tags: ["aspnet-core", "best-practices", "architecture", "performance", "security", "testing"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# ASP.NET Core Best Practices - Thực Hành Tốt Nhất

## Tổng Quan

ASP.NET Core là một framework hiện đại và mạnh mẽ để xây dựng web applications. Tuy nhiên, để tận dụng tối đa potential của nó, developers cần follow các best practices đã được proven trong production environments. Tài liệu này cung cấp một comprehensive guide về các best practices cho mọi aspect của ASP.NET Core development.

Những best practices này được xây dựng dựa trên years of production experience và được aligned với Microsoft's official guidance. Chúng cover từ project structure và architecture đến security, performance, và testing.

Mục tiêu của chúng tôi là cung cấp không chỉ "what to do" mà còn "why to do it" và "how to do it correctly". Mỗi recommendation đi kèm với practical examples và explanations để bạn có thể apply chúng một cách hiệu quả trong codebase của mình.

## Mục Đích

Tài liệu này phục vụ như một definitive guide cho development teams working with ASP.NET Core. Nó giúp:

1. **Onboarding**: New team members có thể quickly understand best practices
2. **Code Review**: Reviewers có một standard để evaluate code quality
3. **Architecture Decisions**: Teams có guidance cho major technical decisions
4. **Performance Optimization**: Proven patterns cho high-performance applications
5. **Security Compliance**: Security best practices aligned với industry standards

## Khái Niệm Chính

### 1. Clean Architecture

Clean Architecture là một software design philosophy tập trung vào separation of concerns và independence of frameworks. Trong ASP.NET Core, Clean Architecture giúp maintainability, testability, và scalability.

```
├── src/
│   ├── MyApp.Domain/           # Enterprise Business Rules
│   │   ├── Entities/           # Core business entities
│   │   ├── ValueObjects/       # Immutable value types
│   │   ├── Interfaces/         # Repository & service contracts
│   │   └── Events/             # Domain events
│   │
│   ├── MyApp.Application/       # Application Business Rules
│   │   ├── Interfaces/         # Use case interfaces
│   │   ├── Services/           # Use case implementations
│   │   ├── DTOs/               # Data transfer objects
│   │   ├── Validators/         # Input validation
│   │   └── Behaviors/          # MediatR behaviors (pipeline)
│   │
│   ├── MyApp.Infrastructure/    # Frameworks & Drivers
│   │   ├── Persistence/        # EF Core, migrations
│   │   ├── Repositories/       # Repository implementations
│   │   ├── Services/           # External service integrations
│   │   └── Caching/            # Redis, memory cache
│   │
│   └── MyApp.Api/              # Interface Adapters
│       ├── Controllers/        # API endpoints
│       ├── Middleware/          # Custom middleware
│       ├── Filters/            # Action filters
│       └── Extensions/         # Extension methods
│
└── tests/
    ├── MyApp.UnitTests/
    └── MyApp.IntegrationTests/
```

**Nguyên tắc cốt lõi**:

```csharp
// Domain Layer - Không có dependencies bên ngoài
namespace MyApp.Domain.Entities;

public class Order
{
    public Guid Id { get; private set; }
    public CustomerId CustomerId { get; private set; }
    public OrderStatus Status { get; private set; }
    public Money TotalAmount { get; private set; }
    private readonly List<OrderItem> _items = new();
    public IReadOnlyCollection<OrderItem> Items => _items.AsReadOnly();
    
    public static Order Create(CustomerId customerId)
    {
        if (customerId is null)
            throw new ArgumentNullException(nameof(customerId));
        
        return new Order
        {
            Id = Guid.NewGuid(),
            CustomerId = customerId,
            Status = OrderStatus.Pending,
            TotalAmount = Money.Zero
        };
    }
    
    public void AddItem(Product product, int quantity)
    {
        if (quantity <= 0)
            throw new DomainException("Quantity must be positive");
        
        var existingItem = _items.FirstOrDefault(i => i.ProductId == product.Id);
        
        if (existingItem is not null)
        {
            existingItem.UpdateQuantity(existingItem.Quantity + quantity);
        }
        else
        {
            _items.Add(OrderItem.Create(this, product, quantity));
        }
        
        RecalculateTotal();
        AddDomainEvent(new OrderItemAddedEvent(Id, product.Id, quantity));
    }
    
    private void RecalculateTotal()
    {
        TotalAmount = _items.Aggregate(
            Money.Zero, 
            (sum, item) => sum + item.Subtotal);
    }
}

// Value Objects - Immutable
public record Money
{
    public decimal Amount { get; }
    public Currency Currency { get; }
    
    public Money(decimal amount, Currency currency = Currency.USD)
    {
        if (amount < 0)
            throw new ArgumentException("Amount cannot be negative", nameof(amount));
        
        Amount = Math.Round(amount, 2);
        Currency = currency;
    }
    
    public static Money Zero => new(0);
    
    public static Money operator +(Money a, Money b)
    {
        if (a.Currency != b.Currency)
            throw new InvalidOperationException("Cannot add different currencies");
        return new Money(a.Amount + b.Amount, a.Currency);
    }
    
    public static Money operator *(Money a, decimal multiplier) =>
        new(a.Amount * multiplier, a.Currency);
}

// Domain Events
public abstract record DomainEvent
{
    public Guid EventId { get; } = Guid.NewGuid();
    public DateTime OccurredAt { get; } = DateTime.UtcNow;
}

public record OrderItemAddedEvent(Guid OrderId, Guid ProductId, int Quantity) 
    : DomainEvent;
```

```csharp
// Application Layer - Depends only on Domain
namespace MyApp.Application.Interfaces;

public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(Guid id, CancellationToken ct = default);
    Task<Order?> GetByIdWithItemsAsync(Guid id, CancellationToken ct = default);
    Task<IReadOnlyList<Order>> GetByCustomerIdAsync(Guid customerId, CancellationToken ct = default);
    Task AddAsync(Order order, CancellationToken ct = default);
    Task UpdateAsync(Order order, CancellationToken ct = default);
    Task DeleteAsync(Guid id, CancellationToken ct = default);
}

public interface IProductRepository
{
    Task<Product?> GetByIdAsync(Guid id, CancellationToken ct = default);
    Task<IReadOnlyList<Product>> GetByIdsAsync(IEnumerable<Guid> ids, CancellationToken ct = default);
}

public interface IUnitOfWork
{
    IOrderRepository Orders { get; }
    IProductRepository Products { get; }
    ICustomerRepository Customers { get; }
    
    Task<int> SaveChangesAsync(CancellationToken ct = default);
    Task<int> SaveChangesAsync(bool acceptAllChangesOnSuccess, CancellationToken ct = default);
    Task BeginTransactionAsync(CancellationToken ct = default);
    Task CommitTransactionAsync(CancellationToken ct = default);
    Task RollbackTransactionAsync(CancellationToken ct = default);
}
```

```csharp
// Application Services - Use Cases
namespace MyApp.Application.Services;

public interface IOrderService
{
    Task<OrderDto> CreateOrderAsync(CreateOrderCommand command, CancellationToken ct = default);
    Task<OrderDto> GetOrderByIdAsync(Guid id, CancellationToken ct = default);
    Task<PaginatedResult<OrderSummaryDto>> GetOrdersAsync(GetOrdersQuery query, CancellationToken ct = default);
    Task CancelOrderAsync(Guid id, CancellationToken ct = default);
}

public class CreateOrderCommandValidator : AbstractValidator<CreateOrderCommand>
{
    public CreateOrderCommandValidator()
    {
        RuleFor(x => x.CustomerId)
            .NotEmpty()
            .WithMessage("Customer ID is required");
        
        RuleFor(x => x.Items)
            .NotEmpty()
            .WithMessage("At least one item is required");
        
        RuleForEach(x => x.Items)
            .ChildRules(item =>
            {
                item.RuleFor(i => i.ProductId)
                    .NotEmpty();
                item.RuleFor(i => i.Quantity)
                    .GreaterThan(0)
                    .WithMessage("Quantity must be greater than 0");
            });
    }
}

public class OrderService : IOrderService
{
    private readonly IOrderRepository _orderRepository;
    private readonly IProductRepository _productRepository;
    private readonly IUnitOfWork _unitOfWork;
    private readonly ILogger<OrderService> _logger;
    private readonly IMapper _mapper;
    
    public OrderService(
        IOrderRepository orderRepository,
        IProductRepository productRepository,
        IUnitOfWork unitOfWork,
        ILogger<OrderService> logger,
        IMapper mapper)
    {
        _orderRepository = orderRepository;
        _productRepository = productRepository;
        _unitOfWork = unitOfWork;
        _logger = logger;
        _mapper = mapper;
    }
    
    public async Task<OrderDto> CreateOrderAsync(
        CreateOrderCommand command, 
        CancellationToken ct = default)
    {
        // Validate
        var validator = new CreateOrderCommandValidator();
        var validationResult = await validator.ValidateAsync(command, ct);
        
        if (!validationResult.IsValid)
            throw new ValidationException(validationResult.Errors
                .GroupBy(e => e.PropertyName)
                .ToDictionary(g => g.Key, g => g.Select(e => e.ErrorMessage).ToArray()));
        
        // Get products
        var productIds = command.Items.Select(i => i.ProductId).ToList();
        var products = await _productRepository.GetByIdsAsync(productIds, ct);
        var productsDict = products.ToDictionary(p => p.Id);
        
        // Create order
        var order = Order.Create(command.CustomerId);
        
        foreach (var item in command.Items)
        {
            if (!productsDict.TryGetValue(item.ProductId, out var product))
                throw new NotFoundException("Product", item.ProductId);
            
            order.AddItem(product, item.Quantity);
        }
        
        // Persist
        await _orderRepository.AddAsync(order, ct);
        await _unitOfWork.SaveChangesAsync(ct);
        
        _logger.LogInformation("Order {OrderId} created for customer {CustomerId}", 
            order.Id, command.CustomerId);
        
        return _mapper.Map<OrderDto>(order);
    }
}
```

### 2. Dependency Injection Best Practices

Proper DI usage là critical cho testability, maintainability, và loose coupling.

```csharp
// Program.cs - Service Registration
var builder = WebApplication.CreateBuilder(args);

// 1. Configuration - Strongly typed
builder.Services.Configure<AppSettings>(
    builder.Configuration.GetSection("AppSettings"));
builder.Services.Configure<JwtSettings>(
    builder.Configuration.GetSection("Jwt"));
builder.Services.Configure<EmailSettings>(
    builder.Configuration.GetSection("Email"));

// 2. Database - Scoped (correct lifetime)
builder.Services.AddDbContext<ApplicationDbContext>(options =>
{
    options.UseSqlServer(
        builder.Configuration.GetConnectionString("Default"),
        sqlOptions =>
        {
            sqlOptions.EnableRetryOnFailure(
                maxRetryCount: 3,
                maxRetryDelay: TimeSpan.FromSeconds(10),
                errorNumbersToAdd: null);
            sqlOptions.CommandTimeout(30);
        });
}, 
ServiceLifetime.Scoped);

// 3. Repositories - Scoped
builder.Services.AddScoped<IOrderRepository, OrderRepository>();
builder.Services.AddScoped<IProductRepository, ProductRepository>();
builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();

// 4. Application Services - Scoped (with interfaces)
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddScoped<IProductService, ProductService>();
builder.Services.AddScoped<IAuthService, AuthService>();

// 5. Infrastructure Services - Singleton hoặc Scoped
builder.Services.AddSingleton<ICacheService, RedisCacheService>();
builder.Services.AddSingleton<IEmailSender, SmtpEmailSender>();
builder.Services.AddSingleton<ILoggerFactory, LoggerFactory>();

// 6. MediatR - Scoped cho request handling
builder.Services.AddMediatR(cfg => 
    cfg.RegisterServicesFromAssemblyContaining<Program>());

// 7. FluentValidation - From assemblies
builder.Services.AddValidatorsFromAssemblies(
    AppDomain.CurrentDomain.GetAssemblies()
        .Where(a => a.FullName!.Contains("MyApp"))
        .ToArray());

var app = builder.Build();

// 8. Middleware
app.UseExceptionHandler();
app.UseHttpsRedirection();
app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
```

**DI Lifetime Guidelines**:

| Lifetime | Use Case | Examples |
|----------|----------|----------|
| Singleton | Stateless services, configuration, logging | `ILogger<T>`, `IOptions<T>`, `IConfiguration` |
| Scoped | Per-request services, DbContext | `IRepository<T>`, `IUnitOfWork`, Services |
| Transient | Lightweight stateless services | `IDateTimeProvider`, validators, mappers |

### 3. Async/Await Pattern

Async/await là essential cho scalability trong web applications.

```csharp
// ✅ CORRECT: Full async pipeline
[HttpGet]
public async Task<ActionResult<PaginatedResult<ProductDto>>> GetProducts(
    [FromQuery] GetProductsQuery query,
    CancellationToken cancellationToken)
{
    var result = await _mediator.Send(query, cancellationToken);
    return Ok(result);
}

// ✅ CORRECT: Async with proper error handling
public async Task<Result<OrderDto>> CreateOrderAsync(
    CreateOrderCommand command,
    CancellationToken ct)
{
    try
    {
        // Validate
        var validationResult = await _validator.ValidateAsync(command, ct);
        if (!validationResult.IsValid)
            return Result.Failure<OrderDto>(validationResult.Errors);
        
        // Business logic
        var order = await _orderRepository.CreateAsync(command, ct);
        
        // Publish event
        await _eventBus.PublishAsync(new OrderCreatedEvent(order.Id), ct);
        
        return Result.Success(_mapper.Map<OrderDto>(order));
    }
    catch (ConcurrencyException ex)
    {
        _logger.LogWarning(ex, "Concurrency conflict creating order");
        return Result.Conflict<OrderDto>("The order was modified by another user");
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error creating order");
        return Result.ServerError<OrderDto>();
    }
}

// ❌ AVOID: Blocking in async context
public async Task<IActionResult> GetUsers()
{
    var users = Task.Run(() => _userService.GetUsersSync()).Result; // ❌ BLOCKING!
    return Ok(users);
}

// ❌ AVOID: Fire-and-forget without proper handling
public async Task<IActionResult> SendEmail([FromBody] EmailRequest request)
{
    _ = _emailService.SendAsync(request); // ❌ No awaiting!
    return Ok(); // Returns before email is sent
}
```

### 4. Entity Framework Core Best Practices

```csharp
// DbContext Configuration
public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
        ChangeTracker.QueryTrackingBehavior = QueryTrackingBehavior.NoTracking;
    }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        
        // Apply all entity configurations
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
        
        // Global query filters
        modelBuilder.Entity<User>()
            .HasQueryFilter(u => !u.IsDeleted);
        
        // Indexes
        modelBuilder.Entity<Order>()
            .HasIndex(o => o.CustomerId)
            .HasDatabaseName("IX_Orders_CustomerId");
        
        modelBuilder.Entity<Order>()
            .HasIndex(o => new { o.Status, o.CreatedAt })
            .HasDatabaseName("IX_Orders_Status_CreatedAt");
    }
}

// Entity Configuration
public class OrderEntityConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("Orders");
        
        builder.HasKey(o => o.Id);
        
        builder.Property(o => o.Status)
            .HasConversion<string>()
            .HasMaxLength(50);
        
        builder.Property(o => o.TotalAmount)
            .HasPrecision(18, 2);
        
        builder.HasOne(o => o.Customer)
            .WithMany(c => c.Orders)
            .HasForeignKey(o => o.CustomerId)
            .OnDelete(DeleteBehavior.Restrict);
        
        builder.HasMany(o => o.Items)
            .WithOne(i => i.Order)
            .HasForeignKey(i => i.OrderId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}

// Repository Implementation
public class OrderRepository : IOrderRepository
{
    private readonly ApplicationDbContext _context;
    
    public OrderRepository(ApplicationDbContext context)
    {
        _context = context;
    }
    
    public async Task<Order?> GetByIdAsync(Guid id, CancellationToken ct = default)
    {
        return await _context.Orders
            .FirstOrDefaultAsync(o => o.Id == id, ct);
    }
    
    public async Task<Order?> GetByIdWithItemsAsync(Guid id, CancellationToken ct = default)
    {
        return await _context.Orders
            .Include(o => o.Items)
                .ThenInclude(i => i.Product)
            .Include(o => o.Customer)
            .FirstOrDefaultAsync(o => o.Id == id, ct);
    }
    
    public async Task<IReadOnlyList<Order>> GetByCustomerIdAsync(
        Guid customerId, 
        CancellationToken ct = default)
    {
        return await _context.Orders
            .AsNoTracking()
            .Where(o => o.CustomerId == customerId)
            .OrderByDescending(o => o.CreatedAt)
            .ToListAsync(ct);
    }
    
    public async Task AddAsync(Order order, CancellationToken ct = default)
    {
        await _context.Orders.AddAsync(order, ct);
    }
    
    public void Update(Order order)
    {
        _context.Orders.Update(order);
    }
    
    public void Delete(Order order)
    {
        _context.Orders.Remove(order);
    }
}
```

### 5. API Design Best Practices

```csharp
// Consistent Response Wrapper
public class ApiResponse<T>
{
    public T? Data { get; set; }
    public bool Success { get; set; }
    public ApiError? Error { get; set; }
    public Dictionary<string, object> Metadata { get; set; } = new();
}

public class ApiError
{
    public string Code { get; set; } = string.Empty;
    public string Message { get; set; } = string.Empty;
    public Dictionary<string, string[]>? ValidationErrors { get; set; }
}

// Global Response Filter
public class ResponseWrapperFilter : IResultFilter
{
    public void OnResultExecuting(ResultExecutingContext context)
    {
        // Skip for non-success responses
        if (context.Result is not ObjectResult { StatusCode: >= 200 and < 300 } result)
            return;
        
        // Skip for specific content types
        if (context.HttpContext.Response.ContentType?.Contains("problem") == true)
            return;
        
        var apiResponse = new ApiResponse<object>
        {
            Data = result.Value,
            Success = true
        };
        
        result.Value = apiResponse;
    }
    
    public void OnResultExecuted(ResultExecutedContext context) { }
}

// Controller with proper documentation
[ApiController]
[Route("api/v1/[controller]")]
[Produces(MediaTypeNames.Application.Json)]
[Consumes(MediaTypeNames.Application.Json)]
public class OrdersController : ControllerBase
{
    private readonly IMediator _mediator;
    
    public OrdersController(IMediator mediator)
    {
        _mediator = mediator;
    }
    
    /// <summary>
    /// Get a paginated list of orders
    /// </summary>
    /// <param name="query">Query parameters for filtering and pagination</param>
    /// <param name="ct">Cancellation token</param>
    /// <returns>Paginated list of orders</returns>
    /// <response code="200">Returns the paginated list of orders</response>
    /// <response code="400">If the query parameters are invalid</response>
    [HttpGet]
    [ProducesResponseType(typeof(PaginatedResponse<OrderSummaryDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    [ResponseCache(CacheProfileName = "OrdersList")]
    public async Task<ActionResult<PaginatedResponse<OrderSummaryDto>>> GetOrders(
        [FromQuery] GetOrdersQuery query,
        CancellationToken ct)
    {
        var result = await _mediator.Send(query, ct);
        return Ok(result);
    }
    
    /// <summary>
    /// Get order by ID
    /// </summary>
    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(OrderDetailDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ETagCache]
    public async Task<ActionResult<OrderDetailDto>> GetOrder(
        Guid id,
        CancellationToken ct)
    {
        var result = await _mediator.Send(new GetOrderByIdQuery(id), ct);
        
        if (result is null)
            return NotFound();
        
        return Ok(result);
    }
}
```

### 6. Health Checks Implementation

```csharp
// Comprehensive Health Check Setup
builder.Services.AddHealthChecks()
    // Database
    .AddDbContextCheck<ApplicationDbContext>("database", tags: new[] { "ready", "db" })
    
    // Redis Cache
    .AddRedis(
        builder.Configuration.GetConnectionString("Redis")!,
        name: "cache",
        tags: new[] { "ready", "cache" })
    
    // External APIs
    .AddUrlGroup(
        new Uri($"{builder.Configuration["Services:PaymentApi"]}/health"),
        name: "payment-api",
        failureStatus: HealthStatus.Degraded,
        tags: new[] { "ready", "external" })
    
    // Custom business health check
    .AddCheck<DatabaseMigrationHealthCheck>(
        "database-migration",
        tags: new[] { "startup" })
    
    // Memory usage
    .AddCheck<MemoryHealthCheck>(
        "memory",
        failureStatus: HealthStatus.Degraded,
        tags: new[] { "ready" },
        threshold: 1024 * 1024 * 512); // 512MB

// Custom Health Check
public class DatabaseMigrationHealthCheck : IHealthCheck
{
    private readonly IServiceProvider _serviceProvider;
    
    public DatabaseMigrationHealthCheck(IServiceProvider serviceProvider)
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
            var dbContext = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
            
            var pendingMigrations = await dbContext.Database
                .GetPendingMigrationsAsync(cancellationToken);
            
            if (pendingMigrations.Any())
            {
                return HealthCheckResult.Unhealthy(
                    $"Database has {pendingMigrations.Count()} pending migrations",
                    data: new Dictionary<string, object>
                    {
                        ["pendingMigrations"] = pendingMigrations.ToList()
                    });
            }
            
            return HealthCheckResult.Healthy("Database migrations are up to date");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("Database health check failed", ex);
        }
    }
}

// Health Check Endpoint Configuration
app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = async (context, report) =>
    {
        context.Response.ContentType = "application/json";
        
        var response = new
        {
            status = report.Status.ToString(),
            timestamp = DateTime.UtcNow,
            duration = report.TotalDuration.TotalMilliseconds,
            checks = report.Entries.Select(e => new
            {
                name = e.Key,
                status = e.Value.Status.ToString(),
                duration = e.Value.Duration.TotalMilliseconds,
                description = e.Value.Description,
                data = e.Value.Data
            })
        };
        
        await context.Response.WriteAsJsonAsync(response);
    },
    
    ResultStatusCodes =
    {
        [HealthStatus.Healthy] = StatusCodes.Status200OK,
        [HealthStatus.Degraded] = StatusCodes.Status200OK,
        [HealthStatus.Unhealthy] = StatusCodes.Status503ServiceUnavailable
    }
});

// Kubernetes Probes
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false // Liveness: is the app running?
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready") // Readiness: can it serve traffic?
});
```

### 7. Security Best Practices

```csharp
// JWT Configuration
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
    
    options.Events = new JwtBearerEvents
    {
        OnAuthenticationFailed = context =>
        {
            if (context.Exception is SecurityTokenExpiredException)
            {
                context.Response.Headers.Append("Token-Expired", "true");
            }
            return Task.CompletedTask;
        }
    };
});

// Authorization Policies
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AdminOnly", policy =>
        policy.RequireRole("Admin"));
    
    options.AddPolicy("CanManageOrders", policy =>
        policy.RequireAssertion(context =>
            context.User.HasClaim(c => c.Type == "Permission" && c.Value == "Orders.Manage") ||
            context.User.IsInRole("Admin")));
    
    options.AddPolicy("MinimumAge", policy =>
        policy.Requirements.Add(new MinimumAgeRequirement(18)));
});

// Security Headers Middleware
public class SecurityHeadersMiddleware
{
    private readonly RequestDelegate _next;
    
    public SecurityHeadersMiddleware(RequestDelegate next)
    {
        _next = next;
    }
    
    public async Task InvokeAsync(HttpContext context)
    {
        // X-Content-Type-Options
        context.Response.Headers.XContentTypeOptions = "nosniff";
        
        // X-Frame-Options
        context.Response.Headers.XFrameOptions = "DENY";
        
        // X-XSS-Protection
        context.Response.Headers.XXssProtection = "1; mode=block";
        
        // Referrer-Policy
        context.Response.Headers.ReferrerPolicy = "strict-origin-when-cross-origin";
        
        // Content-Security-Policy
        context.Response.Headers.ContentSecurityPolicy = 
            "default-src 'self'; " +
            "script-src 'self' 'nonce-{nonce}'; " +
            "style-src 'self' 'nonce-{nonce}'; " +
            "img-src 'self' data: https:; " +
            "font-src 'self'; " +
            "connect-src 'self' https://api.example.com; " +
            "frame-ancestors 'none';";
        
        // Permissions-Policy
        context.Response.Headers.PermissionsPolicy = 
            "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=()";
        
        await _next(context);
    }
}

// Rate Limiting
builder.Services.AddRateLimiter(options =>
{
    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;
    
    options.AddPolicy("fixed", httpContext =>
        RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: httpContext.User.Identity?.Name ?? httpContext.Connection.RemoteIpAddress?.ToString()!,
            factory: _ => new FixedWindowRateLimiterOptions
            {
                PermitLimit = 100,
                Window = TimeSpan.FromMinutes(1)
            }));
    
    options.AddPolicy("sliding", httpContext =>
        RateLimitPartition.GetSlidingWindowLimiter(
            partitionKey: httpContext.User.Identity?.Name ?? httpContext.Connection.RemoteIpAddress?.ToString()!,
            factory: _ => new SlidingWindowRateLimiterOptions
            {
                PermitLimit = 100,
                SegmentsPerWindow = 10,
                Window = TimeSpan.FromMinutes(1)
            }));
});

app.UseRateLimiter();
```

### 8. Performance Best Practices

```csharp
// Response Compression
builder.Services.AddResponseCompression(options =>
{
    options.EnableForHttps = true;
    options.Providers.Add<BrotliCompressionProvider>();
    options.Providers.Add<GzipCompressionProvider>();
});

builder.Services.Configure<BrotliCompressionProviderOptions>(options =>
{
    options.Level = CompressionLevel.Fastest;
});

// Caching
builder.Services.AddOutputCache(options =>
{
    options.DefaultExpirationTimeSpan = TimeSpan.FromMinutes(5);
    options.AddBasePolicy(builder => builder.With(c => true));
    options.AddPolicy("Products", builder =>
        builder.SetVaryByQuery("page", "pageSize", "sort", "category")
            .Tag("products")
            .Expire(TimeSpan.FromMinutes(10)));
    options.AddPolicy("ProductDetail", builder =>
        builder.SetVaryByRouteParams("id")
            .Tag("products")
            .Expire(TimeSpan.FromMinutes(30)));
});

var app = builder.Build();
app.UseResponseCompression();
app.UseOutputCache();

// Eager Loading & Query Optimization
public class ProductRepository
{
    private readonly ApplicationDbContext _context;
    
    public async Task<PaginatedResult<ProductListDto>> GetProductsAsync(
        ProductQueryParameters query,
        CancellationToken ct)
    {
        var queryable = _context.Products.AsNoTracking();
        
        // Apply filters
        if (!string.IsNullOrEmpty(query.Search))
        {
            var searchTerm = query.Search.ToLower();
            queryable = queryable.Where(p => 
                EF.Functions.ILike(p.Name, $"%{searchTerm}%") ||
                EF.Functions.ILike(p.Description, $"%{searchTerm}%"));
        }
        
        if (query.CategoryId.HasValue)
        {
            queryable = queryable.Where(p => p.CategoryId == query.CategoryId);
        }
        
        if (query.MinPrice.HasValue)
        {
            queryable = queryable.Where(p => p.Price >= query.MinPrice);
        }
        
        if (query.MaxPrice.HasValue)
        {
            queryable = queryable.Where(p => p.Price <= query.MaxPrice);
        }
        
        // Count total
        var totalCount = await queryable.CountAsync(ct);
        
        // Apply sorting
        queryable = query.SortBy?.ToLower() switch
        {
            "price_asc" => queryable.OrderBy(p => p.Price),
            "price_desc" => queryable.OrderByDescending(p => p.Price),
            "name_asc" => queryable.OrderBy(p => p.Name),
            "name_desc" => queryable.OrderByDescending(p => p.Name),
            "newest" => queryable.OrderByDescending(p => p.CreatedAt),
            _ => queryable.OrderByDescending(p => p.CreatedAt)
        };
        
        // Pagination
        var items = await queryable
            .Skip(query.Offset)
            .Take(query.Limit)
            .ProjectTo<ProductListDto>(_mapper.ConfigurationProvider)
            .ToListAsync(ct);
        
        return new PaginatedResult<ProductListDto>(items, totalCount, query.Offset, query.Limit);
    }
}
```

### 9. Testing Best Practices

```csharp
// Unit Test Example
public class OrderServiceTests
{
    private readonly Mock<IOrderRepository> _orderRepository;
    private readonly Mock<IProductRepository> _productRepository;
    private readonly Mock<IUnitOfWork> _unitOfWork;
    private readonly Mock<IMapper> _mapper;
    private readonly OrderService _sut;
    
    public OrderServiceTests()
    {
        _orderRepository = new Mock<IOrderRepository>();
        _productRepository = new Mock<IProductRepository>();
        _unitOfWork = new Mock<IUnitOfWork>();
        _mapper = new Mock<IMapper>();
        
        _sut = new OrderService(
            _orderRepository.Object,
            _productRepository.Object,
            _unitOfWork.Object,
            Mock.Of<ILogger<OrderService>>(),
            _mapper.Object);
    }
    
    [Fact]
    public async Task CreateOrderAsync_WithValidCommand_ShouldCreateOrder()
    {
        // Arrange
        var command = new CreateOrderCommand
        {
            CustomerId = Guid.NewGuid(),
            Items = new List<CreateOrderItemDto>
            {
                new() { ProductId = Guid.NewGuid(), Quantity = 2 }
            }
        };
        
        var product = Product.Create("Test Product", Money.FromDecimal(10m));
        _productRepository
            .Setup(x => x.GetByIdsAsync(It.IsAny<IEnumerable<Guid>>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new[] { product });
        
        _orderRepository
            .Setup(x => x.AddAsync(It.IsAny<Order>(), It.IsAny<CancellationToken>()))
            .Returns(Task.CompletedTask);
        
        _unitOfWork
            .Setup(x => x.SaveChangesAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(1);
        
        _mapper
            .Setup(x => x.Map<OrderDto>(It.IsAny<Order>()))
            .Returns(new OrderDto { Id = Guid.NewGuid() });
        
        // Act
        var result = await _sut.CreateOrderAsync(command);
        
        // Assert
        result.IsSuccess.Should().BeTrue();
        result.Value.Should().NotBeNull();
        _orderRepository.Verify(x => x.AddAsync(It.IsAny<Order>(), It.IsAny<CancellationToken>()), Times.Once);
        _unitOfWork.Verify(x => x.SaveChangesAsync(It.IsAny<CancellationToken>()), Times.Once);
    }
    
    [Fact]
    public async Task CreateOrderAsync_WithEmptyItems_ShouldFail()
    {
        // Arrange
        var command = new CreateOrderCommand
        {
            CustomerId = Guid.NewGuid(),
            Items = new List<CreateOrderItemDto>()
        };
        
        // Act
        var result = await _sut.CreateOrderAsync(command);
        
        // Assert
        result.IsFailure.Should().BeTrue();
        result.Error.Should().Contain("At least one item is required");
    }
}

// Integration Test Example
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
                // Replace with test database
                services.RemoveAll(typeof(DbContextOptions<ApplicationDbContext>));
                services.AddDbContext<ApplicationDbContext>(options =>
                {
                    options.UseInMemoryDatabase("TestDb");
                });
            });
        });
        
        _client = _factory.CreateClient();
    }
    
    [Fact]
    public async Task GetOrders_ShouldReturnOk()
    {
        // Arrange
        var user = await CreateTestUserAsync();
        var token = GenerateJwtToken(user);
        _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
        
        // Act
        var response = await _client.GetAsync("/api/v1/orders");
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        
        var content = await response.Content.ReadFromJsonAsync<PaginatedResponse<OrderDto>>();
        content.Should().NotBeNull();
    }
    
    [Fact]
    public async Task CreateOrder_WithoutAuth_ShouldReturnUnauthorized()
    {
        // Act
        var response = await _client.PostAsJsonAsync("/api/v1/orders", new { });
        
        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Unauthorized);
    }
}
```

### 10. Logging Best Practices

```csharp
// Structured Logging
public class OrderService : IOrderService
{
    private readonly ILogger<OrderService> _logger;
    
    public async Task<OrderDto> CreateOrderAsync(CreateOrderCommand command, CancellationToken ct)
    {
        _logger.LogInformation(
            "Creating order for customer {CustomerId} with {ItemCount} items",
            command.CustomerId,
            command.Items.Count);
        
        try
        {
            // Business logic
            
            _logger.LogInformation(
                "Order {OrderId} created successfully for customer {CustomerId}",
                order.Id,
                command.CustomerId);
            
            return _mapper.Map<OrderDto>(order);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Failed to create order for customer {CustomerId}. Items: {@Items}",
                command.CustomerId,
                command.Items);
            throw;
        }
    }
}

// Log Levels Usage
// - Trace: Detailed debugging information
// - Debug: Development debugging (not in production)
// - Information: Normal application flow
// - Warning: Abnormal but expected situations
// - Error: Errors that need attention
// - Critical: System-level failures

// Configuration
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore": "Warning",
      "Microsoft.Hosting.Lifetime": "Information",
      "MyApp": "Debug"
    },
    "Console": {
      "FormatterName": "json",
      "FormatterOptions": {
        "SingleLine": true,
        "IncludeScopes": true,
        "TimestampFormat": "yyyy-MM-dd HH:mm:ss "
      }
    }
  }
}
```

## Common Patterns

### Result Pattern

```csharp
// Generic Result type
public class Result
{
    public bool IsSuccess { get; }
    public bool IsFailure => !IsSuccess;
    public Error? Error { get; }
    
    protected Result(bool isSuccess, Error? error)
    {
        if (isSuccess && error is not null)
            throw new InvalidOperationException();
        if (!isSuccess && error is null)
            throw new InvalidOperationException();
        
        IsSuccess = isSuccess;
        Error = error;
    }
    
    public static Result Success() => new(true, null);
    public static Result Failure(Error error) => new(false, error);
    public static Result Failure(string code, string message) => 
        new(false, new Error(code, message));
}

public class Result<T> : Result
{
    public T? Value { get; }
    
    protected Result(T? value, bool isSuccess, Error? error) : base(isSuccess, error)
    {
        Value = value;
    }
    
    public static Result<T> Success(T value) => new(value, true, null);
    public new static Result<T> Failure(Error error) => new(default, false, error);
    public new static Result<T> Failure(string code, string message) => 
        new(default, false, new Error(code, message));
    
    public static implicit operator Result<T>(T value) => Success(value);
}

// Usage
public async Task<Result<OrderDto>> CreateOrderAsync(CreateOrderCommand command, CancellationToken ct)
{
    var validation = await _validator.ValidateAsync(command, ct);
    if (!validation.IsValid)
        return Result.Failure<OrderDto>("VALIDATION_ERROR", validation.ToString());
    
    try
    {
        var order = await _orderService.CreateOrderAsync(command, ct);
        return Result.Success(_mapper.Map<OrderDto>(order));
    }
    catch (NotFoundException ex)
    {
        return Result.Failure<OrderDto>("NOT_FOUND", ex.Message);
    }
    catch (BusinessRuleException ex)
    {
        return Result.Failure<OrderDto>("BUSINESS_RULE", ex.Message);
    }
}
```

### Specification Pattern

```csharp
// Specification for complex queries
public interface ISpecification<T>
{
    Expression<Func<T, bool>> Criteria { get; }
    List<Expression<Func<T, object>>> Includes { get; }
    List<string> IncludeStrings { get; }
    Expression<Func<T, object>>? OrderBy { get; }
    Expression<Func<T, object>>? OrderByDescending { get; }
    int Take { get; }
    int Skip { get; }
    bool IsPagingEnabled { get; }
}

public class OrderByStatusSpecification : ISpecification<Order>
{
    public Expression<Func<Order, bool>> Criteria => o => o.Status == OrderStatus.Pending;
    public List<Expression<Func<Order, object>>> Includes => new();
    public List<string> IncludeStrings => new();
    public Expression<Func<Order, object>>? OrderBy => o => o.CreatedAt;
    public Expression<Func<Order, object>>? OrderByDescending => null;
    public int Take => 0;
    public int Skip => 0;
    public bool IsPagingEnabled => false;
}

public class PaginatedOrdersSpecification : ISpecification<Order>
{
    private readonly int _skip;
    private readonly int _take;
    
    public PaginatedOrdersSpecification(int skip, int take)
    {
        _skip = skip;
        _take = take;
    }
    
    public Expression<Func<Order, bool>> Criteria => _ => true;
    public List<Expression<Func<Order, object>>> Includes => new() { o => o.Customer };
    public List<string> IncludeStrings => new();
    public Expression<Func<Order, object>>? OrderBy => null;
    public Expression<Func<Order, object>>? OrderByDescending => o => o.CreatedAt;
    public int Take => _take;
    public int Skip => _skip;
    public bool IsPagingEnabled => true;
}
```

## Troubleshooting

### Common Issues and Solutions

1. **"Cannot resolve service" errors**
   - Ensure all services are registered in DI
   - Check interface/base class registration
   - Verify lifetime compatibility

2. **DbContext threading issues**
   - Never use same DbContext across threads
   - Always inject scoped DbContext in controllers/services

3. **Memory leaks with singletons**
   - Don't capture scoped services in singletons
   - Use IServiceScopeFactory for scoped dependencies

4. **Slow startup**
   - Lazy load optional services
   - Use AOT compilation where possible

## Examples

### Complete Production Program.cs

```csharp
var builder = WebApplication.CreateBuilder(args);

// 1. Configuration
builder.Host.ConfigureAppConfiguration((context, config) =>
{
    var builtConfig = config.Build();
    
    if (context.HostingEnvironment.IsProduction())
    {
        config.AddAzureKeyVault(
            $"https://{builtConfig["KeyVault:Vault"]}.vault.azure.net/",
            builtConfig["KeyVault:ClientId"],
            builtConfig["KeyVault:ClientSecret"]);
    }
    
    config.AddEnvironmentVariables();
    config.AddCommandLine(args);
});

// 2. Logging
builder.Logging.ClearProviders();
builder.Logging.AddConsole(options =>
{
    options.FormatterName = "json";
});
builder.Logging.AddApplicationInsights(
    builder.Configuration.GetConnectionString("ApplicationInsights"));

// 3. Services
builder.Services.AddControllers(options =>
{
    options.Filters.Add<ValidationFilter>();
    options.Filters.Add<AuditFilter>();
    options.Filters.Add<ExceptionFilter>();
})
.AddJsonOptions(options =>
{
    options.JsonSerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
    options.JsonSerializerOptions.WriteIndented = builder.Environment.IsDevelopment();
})
.AddFluentValidation();

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "MyApp API",
        Version = "v1",
        Description = "Production-ready API for MyApp"
    });
    
    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Description = "JWT Authorization header using the Bearer scheme",
        Name = "Authorization",
        In = ParameterLocation.Header,
        Type = SecuritySchemeType.ApiKey,
        Scheme = "Bearer"
    });
});

// 4. Security
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.AllowAnyOrigin()
            .AllowAnyMethod()
            .AllowAnyHeader();
    });
});

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme);
builder.Services.AddAuthorization();

// 5. Infrastructure
builder.Services.AddDbContext<ApplicationDbContext>();
builder.Services.AddRedis(builder.Configuration.GetConnectionString("Redis"));
builder.Services.AddScoped(typeof(IRepository<>), typeof(Repository<>));
builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssemblyContaining<Program>());
builder.Services.AddAutoMapper(AppDomain.CurrentDomain.GetAssemblies());

// 6. Health Checks
builder.Services.AddHealthChecks();

var app = builder.Build();

// Middleware Pipeline
app.UseExceptionHandler();
app.UseSecurityHeaders();
app.UseHttpsRedirection();
app.UseCors();
app.UseSwagger();
app.UseSwaggerUI();
app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
app.MapHealthChecks("/health");

app.Run();
```

## References

- [Microsoft ASP.NET Core Documentation](https://docs.microsoft.com/aspnet/core)
- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Entity Framework Core Documentation](https://docs.microsoft.com/ef/core)
- [ASP.NET Core Security Best Practices](https://docs.microsoft.com/aspnet/core/security/)
- [Performance Best Practices](https://docs.microsoft.com/aspnet/core/performance/)
- [Testing ASP.NET Core Applications](https://docs.microsoft.com/aspnet/core/test/)
