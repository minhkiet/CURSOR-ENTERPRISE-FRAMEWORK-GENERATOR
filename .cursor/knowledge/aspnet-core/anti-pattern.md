---
title: "ASP.NET Core Anti-Patterns - Các Mẫu Cần Tránh"
description: "Danh sách chi tiết các anti-patterns phổ biến trong ASP.NET Core development và cách khắc phục chúng"
tags: ["aspnet-core", "anti-patterns", "best-practices", "performance", "security"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# ASP.NET Core Anti-Patterns - Các Mẫu Cần Tránh

## Tổng Quan

Trong quá trình phát triển ứng dụng ASP.NET Core, có nhiều anti-patterns phổ biến mà developers thường mắc phải. Những anti-patterns này có thể dẫn đến performance kém, security vulnerabilities, khó bảo trì, và scalability issues. Tài liệu này sẽ giúp bạn nhận diện và tránh những mẫu thiết kế xấu này trong production environments.

ASP.NET Core là một framework mạnh mẽ với nhiều built-in features, nhưng việc sử dụng không đúng cách có thể phá vỡ những lợi ích mà nó mang lại. Từ việc sử dụng synchronous I/O trong async context cho đến việc ignore health checks, mỗi anti-pattern đều có thể gây ra những vấn đề nghiêm trọng trong production.

## Mục Đích

Mục đích của tài liệu này là cung cấp một danh sách đầy đủ các anti-patterns phổ biến trong ASP.NET Core, giải thích tại sao chúng là vấn đề, và đưa ra solutions cụ thể cho từng trường hợp. Bằng cách hiểu và tránh những mẫu này, bạn sẽ xây dựng được những ứng dụng web chất lượng cao, dễ bảo trì, và có hiệu suất tốt.

Tài liệu này được thiết kế như một companion guide cho các best practices và architecture patterns trong ASP.NET Core. Nó giúp bạn hiểu không chỉ "what to do" mà còn "what NOT to do" trong quá trình phát triển.

## Khái Niệm Chính

### 1. Synchronous I/O Over Async

**Vấn đề**: Sử dụng synchronous methods cho I/O operations là một trong những anti-pattern phổ biến và nghiêm trọng nhất. Nó block thread pool threads, làm giảm đáng kể khả năng handle concurrent requests của ứng dụng.

```csharp
// ❌ ANTI-PATTERN: Synchronous I/O
[HttpGet]
public IActionResult GetUsers()
{
    var users = _context.Users.ToList(); // Blocking call
    return Ok(users);
}

// ✅ BEST PRACTICE: Async I/O
[HttpGet]
public async Task<ActionResult<IEnumerable<UserDto>>> GetUsers()
{
    var users = await _context.Users.ToListAsync();
    return Ok(users);
}
```

**Tại sao đây là vấn đề**: Trong ASP.NET Core, thread pool có một số lượng giới hạn threads. Khi một thread bị blocked bởi synchronous I/O, nó không thể xử lý other requests. Điều này dẫn đến thread pool starvation, nơi mà ứng dụng không thể respond new requests mặc dù CPU usage có thể thấp.

**Giải pháp**: Luôn sử dụng async/await pattern cho tất cả I/O-bound operations bao gồm database queries, file operations, HTTP calls, và any network communication. Điều này giải phóng threads để xử lý other requests trong khi chờ I/O completion.

```csharp
// ❌ ANTI-PATTERN: Synchronous file reading
public string ReadConfig()
{
    return File.ReadAllText("config.json");
}

// ✅ BEST PRACTICE: Async file reading
public async Task<string> ReadConfigAsync()
{
    return await File.ReadAllTextAsync("config.json");
}

// ❌ ANTI-PATTERN: Synchronous HTTP call
public User GetUserFromApi(int id)
{
    var response = _httpClient.Get($"https://api.example.com/users/{id}");
    return JsonSerializer.Deserialize<User>(response.Content);
}

// ✅ BEST PRACTICE: Async HTTP call
public async Task<User> GetUserFromApiAsync(int id)
{
    var response = await _httpClient.GetAsync($"https://api.example.com/users/{id}");
    response.EnsureSuccessStatusCode();
    var content = await response.Content.ReadAsStringAsync();
    return JsonSerializer.Deserialize<User>(content);
}
```

### 2. N+1 Query Problem

**Vấn đề**: N+1 queries xảy ra khi bạn load một collection và sau đó access mỗi item's related entity một cách riêng biệt, tạo ra N additional queries cho N items.

```csharp
// ❌ ANTI-PATTERN: N+1 Query
[HttpGet]
public async Task<ActionResult<IEnumerable<OrderDto>>> GetOrders()
{
    var orders = await _context.Orders.ToListAsync();
    
    var dtos = new List<OrderDto>();
    foreach (var order in orders)
    {
        // ⚠️ N+1: Query này chạy cho MỖI order!
        var customer = await _context.Customers.FindAsync(order.CustomerId);
        dtos.Add(new OrderDto 
        { 
            OrderId = order.Id,
            CustomerName = customer.Name,
            Total = order.Total
        });
    }
    return Ok(dtos);
}

// ✅ BEST PRACTICE: Eager Loading
[HttpGet]
public async Task<ActionResult<IEnumerable<OrderDto>>> GetOrders()
{
    var orders = await _context.Orders
        .Include(o => o.Customer)
        .Select(o => new OrderDto
        {
            OrderId = o.Id,
            CustomerName = o.Customer.Name,
            Total = o.Total
        })
        .ToListAsync();
    return Ok(orders);
}
```

**Tại sao đây là vấn đề**: Nếu bạn có 100 orders, anti-pattern trên sẽ tạo ra 1 query để get orders + 100 queries để get customers = 101 queries total. Điều này tăng database load đáng kể và làm chậm response time.

**Giải pháp**: Sử dụng Include() và ThenInclude() để eager load related entities trong một single query. Hoặc sử dụng projection với Select() để chỉ lấy những fields cần thiết.

```csharp
// Multiple levels of eager loading
var orders = await _context.Orders
    .Include(o => o.Customer)
        .ThenInclude(c => c.Address)
    .Include(o => o.OrderItems)
        .ThenInclude(i => i.Product)
            .ThenInclude(p => p.Category)
    .Where(o => o.OrderDate >= startDate)
    .OrderByDescending(o => o.OrderDate)
    .ToListAsync();

// Projection alternative - even more efficient
var orders = await _context.Orders
    .Where(o => o.OrderDate >= startDate)
    .Select(o => new
    {
        o.Id,
        o.Total,
        CustomerName = o.Customer.Name,
        ItemCount = o.OrderItems.Count,
        CategoryNames = o.OrderItems
            .Select(i => i.Product.Category.Name)
            .ToList()
    })
    .ToListAsync();
```

### 3. Tight Coupling - Coupling Chặt Chẽ

**Vấn đề**: Directly instantiating dependencies thay vì sử dụng dependency injection tạo ra tight coupling và làm code khó test và maintain.

```csharp
// ❌ ANTI-PATTERN: Direct instantiation
public class UserService
{
    private readonly EmailService _emailService = new EmailService();
    private readonly Logger _logger = new Logger();
    
    public async Task CreateUserAsync(User user)
    {
        _logger.Log("Creating user");
        await _emailService.SendWelcomeEmail(user.Email);
        // ...
    }
}

// ✅ BEST PRACTICE: Dependency Injection
public class UserService : IUserService
{
    private readonly IEmailService _emailService;
    private readonly ILogger<UserService> _logger;
    
    public UserService(IEmailService emailService, ILogger<UserService> logger)
    {
        _emailService = emailService;
        _logger = logger;
    }
    
    public async Task CreateUserAsync(User user)
    {
        _logger.LogInformation("Creating user {UserId}", user.Id);
        await _emailService.SendWelcomeEmailAsync(user.Email);
        // ...
    }
}
```

**Tại sao đây là vấn đề**: Khi một class directly instantiates its dependencies, nó trở nên impossible để substitute those dependencies với mocks hoặc stubs trong unit tests. Điều này dẫn đến brittle tests và khó maintain code.

**Giải pháp**: Luôn sử dụng constructor injection để inject dependencies. Define interfaces cho services để enable proper mocking và loose coupling.

```csharp
// Define interface for testability
public interface IEmailService
{
    Task SendWelcomeEmailAsync(string email);
    Task SendPasswordResetEmailAsync(string email, string resetToken);
}

// Implementation
public class SmtpEmailService : IEmailService
{
    private readonly SmtpSettings _settings;
    private readonly ILogger<SmtpEmailService> _logger;
    
    public SmtpEmailService(IOptions<SmtpSettings> settings, ILogger<SmtpEmailService> logger)
    {
        _settings = settings.Value;
        _logger = logger;
    }
    
    public async Task SendWelcomeEmailAsync(string email)
    {
        // Implementation
    }
}

// Registration
builder.Services.AddScoped<IEmailService, SmtpEmailService>();

// Test mock
public class MockEmailService : IEmailService
{
    public List<string> SentEmails { get; } = new();
    
    public Task SendWelcomeEmailAsync(string email)
    {
        SentEmails.Add(email);
        return Task.CompletedTask;
    }
}
```

### 4. Missing Cancellation Tokens

**Vấn đề**: Không sử dụng CancellationToken trong async operations dẫn đến resource waste và potential memory leaks khi clients disconnect.

```csharp
// ❌ ANTI-PATTERN: No cancellation token
[HttpGet]
public async Task<ActionResult<IEnumerable<Product>>> GetProducts()
{
    var products = await _context.Products.ToListAsync();
    return Ok(products);
}

// ✅ BEST PRACTICE: With cancellation token
[HttpGet]
public async Task<ActionResult<IEnumerable<ProductDto>>> GetProducts(
    CancellationToken cancellationToken)
{
    var products = await _context.Products
        .AsNoTracking()
        .Select(p => new ProductDto { Id = p.Id, Name = p.Name })
        .ToListAsync(cancellationToken);
    return Ok(products);
}
```

**Tại sao đây là vấn đề**: Khi một HTTP client disconnects hoặc timeout trước khi request hoàn thành, server vẫn tiếp tục xử lý operation đó nếu không có cancellation token. Điều này lãng phí CPU cycles, memory, và database connections.

**Giải pháp**: Luôn accept CancellationToken như một parameter trong async controller methods và truyền nó xuống tất cả async operations.

```csharp
// Complete example with cancellation token propagation
[HttpGet("search")]
public async Task<ActionResult<SearchResultDto>> SearchProducts(
    [FromQuery] string query,
    [FromQuery] int page = 1,
    [FromQuery] int pageSize = 20,
    CancellationToken cancellationToken = default)
{
    if (string.IsNullOrWhiteSpace(query))
        return BadRequest("Query is required");
    
    // Validate pagination
    pageSize = Math.Clamp(pageSize, 1, 100);
    var skip = (page - 1) * pageSize;
    
    var products = await _context.Products
        .AsNoTracking()
        .Where(p => p.Name.Contains(query) || p.Description.Contains(query))
        .OrderBy(p => p.Name)
        .Skip(skip)
        .Take(pageSize)
        .Select(p => new ProductDto(p.Id, p.Name, p.Price))
        .ToListAsync(cancellationToken);
    
    var totalCount = await _context.Products
        .Where(p => p.Name.Contains(query) || p.Description.Contains(query))
        .CountAsync(cancellationToken);
    
    return Ok(new SearchResultDto
    {
        Products = products,
        Page = page,
        PageSize = pageSize,
        TotalCount = totalCount
    });
}

// For operations that need longer-running cancellation
public class ReportGenerationService
{
    private readonly ApplicationDbContext _context;
    
    public async Task<byte[]> GenerateReportAsync(
        ReportOptions options,
        CancellationToken cancellationToken)
    {
        var data = await _context.Orders
            .Where(o => o.CreatedAt >= options.StartDate)
            .Where(o => o.CreatedAt <= options.EndDate)
            .Include(o => o.Items)
            .AsAsyncEnumerable()
            .WithCancellation(cancellationToken)
            .ToListAsync(cancellationToken);
        
        return await GeneratePdfAsync(data, cancellationToken);
    }
}
```

### 5. Improper Dependency Injection Lifetime

**Vấn đề**: Sử dụng sai DI lifetime có thể dẫn đến memory leaks, stale data, hoặc performance issues.

```csharp
// ❌ ANTI-PATTERN: DbContext as Singleton
builder.Services.AddSingleton<DbContext, ApplicationDbContext>();

// ❌ ANTI-PATTERN: Service with state as Transient
builder.Services.AddTransient<IShoppingCart, ShoppingCart>();

// ❌ ANTI-PATTERN: Captive dependency
builder.Services.AddSingleton<IConfig>(sp => new Config());
builder.Services.AddScoped<IUserService, UserService>(); // ⚠️ Scoped service depends on Singleton - potential issues
```

**Tại sao đây là vấn đề**: DbContext is NOT thread-safe và designed để be scoped per request. Singleton DbContext dẫn đến race conditions và unpredictable behavior. Similarly, stateful services as Transient có thể lose state unexpectedly.

**Giải pháp**: Understand và follow DI lifetime best practices:

```csharp
// ✅ CORRECT: DbContext as Scoped (default)
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString));

// ✅ CORRECT: Singleton for stateless services
builder.Services.AddSingleton<IConfiguration>(configuration);
builder.Services.AddSingleton<IAppSettings, AppSettings>();

// ✅ CORRECT: Scoped for per-request services
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddScoped<IOrderService, OrderService>();

// ✅ CORRECT: Transient for lightweight stateless services
builder.Services.AddTransient<IDateTimeProvider, DateTimeProvider>();
builder.Services.AddTransient<IIdGenerator, IdGenerator>();

// Correct pattern for scoped service depending on singleton
builder.Services.AddSingleton<IServiceProvider>(sp => sp);
builder.Services.AddScoped<IUserService>(sp =>
{
    var provider = sp.GetRequiredService<IServiceProvider>();
    var config = sp.GetRequiredService<IAppConfig>(); // Singleton is fine
    return new UserService(config, provider.GetRequiredService<DbContext>());
});
```

### 6. Large God Controllers

**Vấn đề**: Đặt too much logic trong controllers dẫn đến monolithic classes khó test, maintain, và reuse.

```csharp
// ❌ ANTI-PATTERN: God Controller
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly ApplicationDbContext _context;
    
    [HttpGet]
    public async Task<IActionResult> GetOrders(...)
    {
        // 50 lines of filtering, validation, query logic
    }
    
    [HttpPost]
    public async Task<IActionResult> CreateOrder(...)
    {
        // 100 lines of business logic
    }
    
    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateOrder(...)
    {
        // 80 lines of update logic
    }
    
    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteOrder(...)
    {
        // 30 lines of deletion logic
    }
}
```

**Tại sao đây là vấn đề**: Controllers với hàng trăm lines of code vi phạm Single Responsibility Principle. Chúng trở nên impossible to test independently và difficult to reuse logic across different endpoints.

**Giải pháp**: Delegate business logic to services layer và keep controllers thin:

```csharp
// ✅ BEST PRACTICE: Thin Controller
[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class OrdersController : ControllerBase
{
    private readonly IOrderService _orderService;
    private readonly IMapper _mapper;
    
    public OrdersController(IOrderService orderService, IMapper mapper)
    {
        _orderService = orderService;
        _mapper = mapper;
    }
    
    [HttpGet]
    [ProducesResponseType(typeof(OrderListResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<OrderListResponse>> GetOrders(
        [FromQuery] OrderQueryParameters parameters,
        CancellationToken cancellationToken)
    {
        var result = await _orderService.GetOrdersAsync(parameters, cancellationToken);
        return Ok(result);
    }
    
    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(OrderDetailResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<OrderDetailResponse>> GetOrder(
        Guid id,
        CancellationToken cancellationToken)
    {
        var order = await _orderService.GetOrderByIdAsync(id, cancellationToken);
        if (order is null)
            return NotFound();
        return Ok(order);
    }
    
    [HttpPost]
    [ProducesResponseType(typeof(OrderDetailResponse), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status422UnprocessableEntity)]
    public async Task<ActionResult<OrderDetailResponse>> CreateOrder(
        [FromBody] CreateOrderRequest request,
        CancellationToken cancellationToken)
    {
        var result = await _orderService.CreateOrderAsync(request, cancellationToken);
        return CreatedAtAction(
            nameof(GetOrder),
            new { id = result.Id },
            result);
    }
}

// ✅ BEST PRACTICE: Rich Service Layer
public interface IOrderService
{
    Task<OrderListResponse> GetOrdersAsync(OrderQueryParameters parameters, CancellationToken ct);
    Task<OrderDetailResponse?> GetOrderByIdAsync(Guid id, CancellationToken ct);
    Task<OrderDetailResponse> CreateOrderAsync(CreateOrderRequest request, CancellationToken ct);
    Task<OrderDetailResponse> UpdateOrderAsync(Guid id, UpdateOrderRequest request, CancellationToken ct);
    Task DeleteOrderAsync(Guid id, CancellationToken ct);
}

public class OrderService : IOrderService
{
    private readonly ApplicationDbContext _context;
    private readonly IMapper _mapper;
    private readonly IOrderValidator _validator;
    private readonly IEventBus _eventBus;
    private readonly ILogger<OrderService> _logger;
    
    public OrderService(
        ApplicationDbContext context,
        IMapper mapper,
        IOrderValidator validator,
        IEventBus eventBus,
        ILogger<OrderService> logger)
    {
        _context = context;
        _mapper = mapper;
        _validator = validator;
        _eventBus = eventBus;
        _logger = logger;
    }
    
    public async Task<OrderListResponse> GetOrdersAsync(
        OrderQueryParameters parameters,
        CancellationToken ct)
    {
        var query = _context.Orders
            .AsNoTracking()
            .FilterByStatus(parameters.Status)
            .FilterByDateRange(parameters.StartDate, parameters.EndDate)
            .FilterByCustomer(parameters.CustomerId);
        
        var totalCount = await query.CountAsync(ct);
        
        var orders = await query
            .OrderByDescending(o => o.CreatedAt)
            .Skip(parameters.Offset)
            .Take(parameters.Limit)
            .ProjectTo<OrderSummaryDto>(_mapper.ConfigurationProvider)
            .ToListAsync(ct);
        
        return new OrderListResponse
        {
            Orders = orders,
            TotalCount = totalCount,
            Offset = parameters.Offset,
            Limit = parameters.Limit
        };
    }
    
    public async Task<OrderDetailResponse> CreateOrderAsync(
        CreateOrderRequest request,
        CancellationToken ct)
    {
        await _validator.ValidateAsync(request, ct);
        
        await using var transaction = await _context.Database.BeginTransactionAsync(ct);
        
        try
        {
            var order = _mapper.Map<Order>(request);
            order.Id = Guid.NewGuid();
            order.Status = OrderStatus.Pending;
            order.CreatedAt = DateTime.UtcNow;
            
            _context.Orders.Add(order);
            await _context.SaveChangesAsync(ct);
            
            await _eventBus.PublishAsync(new OrderCreatedEvent(order.Id), ct);
            
            await transaction.CommitAsync(ct);
            
            _logger.LogInformation("Order {OrderId} created successfully", order.Id);
            
            return _mapper.Map<OrderDetailResponse>(order);
        }
        catch (Exception ex)
        {
            await transaction.RollbackAsync(ct);
            _logger.LogError(ex, "Failed to create order");
            throw;
        }
    }
}
```

### 7. Hard-coded Configuration Values

**Vấn đề**: Hard-coding connection strings, secrets, và configuration values trong code là một security anti-pattern nghiêm trọng.

```csharp
// ❌ ANTI-PATTERN: Hard-coded secrets
public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        var connectionString = "Server=localhost;Database=MyDb;User=admin;Password=secret123";
        services.AddDbContext<ApplicationDbContext>(options =>
            options.UseSqlServer(connectionString));
        
        // JWT Key hardcoded!
        var key = "ThisIsAVerySecretKey123456789012345";
    }
}

// ❌ ANTI-PATTERN: Secrets in code
public class EmailService
{
    public void SendEmail()
    {
        var apiKey = "SG.xxxxxx.yyyyyy"; // Exposed in source control!
    }
}
```

**Tại sao đây là vấn đề**: Hard-coded secrets có thể accidentally committed to source control, exposed in logs, và visible to anyone with code access. Trong production, secrets nên được managed centrally và never stored in plain text.

**Giải pháp**: Use structured configuration và secret management:

```csharp
// ✅ BEST PRACTICE: Configuration with IOptions
public class AppSettings
{
    public DatabaseSettings Database { get; set; } = new();
    public JwtSettings Jwt { get; set; } = new();
    public EmailSettings Email { get; set; } = new();
}

public class DatabaseSettings
{
    public string Host { get; set; }
    public int Port { get; set; }
    public string Name { get; set; }
    public string Username { get; set; }
    public string Password { get; set; }
    
    public string ConnectionString => 
        $"Server={Host},{Port};Database={Name};User Id={Username};Password={Password};";
}

// ✅ BEST PRACTICE: Environment-specific configuration
// appsettings.json (base)
{
  "AppSettings": {
    "Database": {
      "Host": "localhost",
      "Port": 1433,
      "Name": "MyApp"
    }
  }
}

// appsettings.Development.json
{
  "AppSettings": {
    "Database": {
      "Host": "localhost",
      "Password": "dev-password"
    }
  }
}

// appsettings.Production.json (no secrets - they come from environment)
// In Azure/AWS: use Key Vault, Secrets Manager

// Program.cs
builder.Services.Configure<AppSettings>(builder.Configuration.GetSection("AppSettings"));
builder.Services.Configure<JwtSettings>(builder.Configuration.GetSection("Jwt"));
builder.Services.Configure<DatabaseSettings>(builder.Configuration.GetSection("Database"));

// Environment variable override
// ConnectionStrings__Default="Server=prod-server;Database=MyApp;User Id=user;Password=pass"
```

### 8. Not Using Health Checks

**Vấn đề**: Ignoring health checks means you have no way to know if your application is healthy, leading to traffic being routed to unhealthy instances.

```csharp
// ❌ ANTI-PATTERN: No health checks configured
var app = builder.Build();
app.MapControllers();
app.Run();
// No health check endpoint - Kubernetes can't determine if pod is healthy!
```

**Tại sao đây là vấn đề**: Without health checks, load balancers và orchestrators như Kubernetes không thể determine whether an instance is capable of handling requests. This can lead to failed requests being routed to instances that are starting, failing, or overloaded.

**Giải pháp**: Implement comprehensive health checks:

```csharp
// ✅ BEST PRACTICE: Health checks with dependencies
builder.Services.AddHealthChecks()
    // Database connectivity
    .AddDbContextCheck<ApplicationDbContext>("database")
    // Redis cache
    .AddRedis(builder.Configuration.GetConnectionString("Redis"), name: "cache")
    // External API
    .AddUrlGroup(
        new Uri("https://api.example.com/health"),
        name: "external-api",
        failureStatus: HealthStatus.Unhealthy,
        timeout: TimeSpan.FromSeconds(5))
    // Custom health check
    .AddCheck<CustomHealthCheck>("custom-check");

// Custom health check implementation
public class CustomHealthCheck : IHealthCheck
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<CustomHealthCheck> _logger;
    
    public CustomHealthCheck(IServiceProvider serviceProvider, ILogger<CustomHealthCheck> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }
    
    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            using var scope = _serviceProvider.CreateScope();
            var dbContext = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
            
            // Check database connectivity
            var canConnect = await dbContext.Database.CanConnectAsync(cancellationToken);
            if (!canConnect)
                return HealthCheckResult.Unhealthy("Cannot connect to database");
            
            // Check business rules
            var pendingOrders = await dbContext.Orders
                .Where(o => o.Status == OrderStatus.Pending)
                .CountAsync(cancellationToken);
            
            if (pendingOrders > 1000)
                return HealthCheckResult.Degraded($"High pending orders: {pendingOrders}");
            
            return HealthCheckResult.Healthy();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Health check failed");
            return HealthCheckResult.Unhealthy("Health check failed", ex);
        }
    }
}

// Configure health check response
app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = async (context, report) =>
    {
        context.Response.ContentType = "application/json";
        
        var result = new
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
                exception = e.Value.Exception?.Message
            })
        };
        
        await context.Response.WriteAsJsonAsync(result);
    },
    ResultStatusCodes =
    {
        [HealthStatus.Healthy] = StatusCodes.Status200OK,
        [HealthStatus.Degraded] = StatusCodes.Status200OK,
        [HealthStatus.Unhealthy] = StatusCodes.Status503ServiceUnavailable
    }
});

// Liveness vs Readiness probes for Kubernetes
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false // No checks - just confirms app is running
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    // Only checks dependencies needed for serving traffic
    Predicate = check => check.Tags.Contains("required")
});
```

### 9. Improper Middleware Order

**Vấn đề**: Incorrect middleware ordering có thể cause unexpected behavior, security vulnerabilities, hoặc performance issues.

```csharp
// ❌ ANTI-PATTERN: Wrong middleware order
var app = builder.Build();

app.UseRouting();      // ⚠️ Should be first
app.UseAuthentication(); // ✗ Authentication after UseRouting is often wrong
app.UseAuthorization();
app.UseEndpoints(_ => {});

// ❌ ANTI-PATTERN: Static files before compression
app.UseStaticFiles();     // Served uncompressed
app.UseResponseCompression(); // Too late!
```

**Tại sao đây là vấn đề**: Middleware executes in the order it's registered. If authentication runs before routing, the user context won't be available for authorization decisions. If static files are served before compression, they won't be compressed.

**Giải pháp**: Follow the correct middleware order:

```csharp
// ✅ CORRECT: Proper middleware order
var app = builder.Build();

// 1. Exception handling (first to catch all errors)
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseExceptionHandler("/error");
    app.UseHsts();
}

// 2. Security headers
app.UseXContentTypeOptions();
app.UseXFrameOptions("SAMEORIGIN");
app.UseReferrerPolicy(ReferrerPolicy.StrictOriginWhenCrossOrigin);

// 3. HTTPS redirection (if not behind reverse proxy)
app.UseHttpsRedirection();

// 4. Static files with caching and compression
app.UseResponseCompression();
app.UseStaticFiles(new StaticFileOptions
{
    OnPrepareResponse = ctx =>
    {
        // Cache static assets
        ctx.Context.Response.Headers.CacheControl = "public,max-age=31536000";
    }
});

// 5. Routing (must be before auth in most cases)
app.UseRouting();

// 6. CORS (before auth)
app.UseCors();

// 7. Authentication (after routing, before authorization)
app.UseAuthentication();

// 8. Authorization
app.UseAuthorization();

// 9. Session and state (if needed)
app.UseSession();

// 10. Endpoints
app.MapControllers();
app.MapRazorPages();
app.MapHub<ChatHub>();
```

### 10. Not Handling Exceptions Globally

**Vấn đề**: Unhandled exceptions can crash the application hoặc expose sensitive information in responses.

```csharp
// ❌ ANTI-PATTERN: No global exception handling
var app = builder.Build();
app.UseRouting();
app.MapControllers();
app.Run();
// Any unhandled exception = 500 Internal Server Error with stack trace in dev
```

**Tại sao đây là vấn đề**: Without global exception handling, exceptions are exposed to clients (information disclosure), stack traces are logged inconsistently, và errors don't follow a consistent format.

**Giải pháp**: Implement comprehensive exception handling:

```csharp
// ✅ BEST PRACTICE: Global exception handling
public class GlobalExceptionHandler : IExceptionHandler
{
    private readonly ILogger<GlobalExceptionHandler> _logger;
    private readonly IHostEnvironment _environment;
    
    public GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger, IHostEnvironment environment)
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
        
        var (statusCode, error) = exception switch
        {
            ValidationException ve => (
                StatusCodes.Status400BadRequest,
                new ErrorResponse
                {
                    Type = "ValidationError",
                    Title = "Validation failed",
                    Detail = ve.Message,
                    Errors = ve.Errors
                }),
            
            NotFoundException nf => (
                StatusCodes.Status404NotFound,
                new ErrorResponse
                {
                    Type = "NotFound",
                    Title = "Resource not found",
                    Detail = nf.Message
                }),
            
            UnauthorizedException ue => (
                StatusCodes.Status401Unauthorized,
                new ErrorResponse
                {
                    Type = "Unauthorized",
                    Title = "Authentication required",
                    Detail = ue.Message
                }),
            
            ForbiddenException fe => (
                StatusCodes.Status403Forbidden,
                new ErrorResponse
                {
                    Type = "Forbidden",
                    Title = "Access denied",
                    Detail = fe.Message
                }),
            
            ConflictException ce => (
                StatusCodes.Status409Conflict,
                new ErrorResponse
                {
                    Type = "Conflict",
                    Title = "Resource conflict",
                    Detail = ce.Message
                }),
            
            _ => (
                StatusCodes.Status500InternalServerError,
                new ErrorResponse
                {
                    Type = "InternalServerError",
                    Title = "An unexpected error occurred",
                    Detail = _environment.IsDevelopment() ? exception.Message : null
                })
        };
        
        _logger.LogError(exception,
            "Unhandled exception. CorrelationId: {CorrelationId}, StatusCode: {StatusCode}",
            correlationId,
            statusCode);
        
        httpContext.Response.StatusCode = statusCode;
        httpContext.Response.ContentType = "application/problem+json";
        
        await httpContext.Response.WriteAsJsonAsync(new ProblemDetails
        {
            Status = statusCode,
            Title = error.Title,
            Detail = error.Detail,
            Instance = httpContext.Request.Path,
            Extensions =
            {
                ["correlationId"] = correlationId,
                ["errors"] = error.Errors,
                ["traceId"] = httpContext.TraceIdentifier
            }
        }, cancellationToken);
        
        return true;
    }
}

// Program.cs
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();

var app = builder.Build();

app.UseExceptionHandler();
app.UseHttpsRedirection();
app.UseRouting();
app.MapControllers();

// ✅ Custom exception types
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

public class UnauthorizedException : Exception
{
    public UnauthorizedException(string message = "Authentication required")
        : base(message) { }
}

public class ForbiddenException : Exception
{
    public ForbiddenException(string message = "You do not have permission to access this resource")
        : base(message) { }
}

public class ConflictException : Exception
{
    public ConflictException(string message)
        : base(message) { }
}
```

## Common Patterns

### Memory Leak Patterns

```csharp
// ❌ ANTI-PATTERN: Event handler leak
public class EventService
{
    public event EventHandler DataChanged;
    
    public void Start()
    {
        DataChanged += OnDataChanged; // Never unsubscribed!
    }
}

// ✅ BEST PRACTICE: Proper event unsubscribe
public class EventService : IDisposable
{
    private readonly List<Func<DataChangedEvent, Task>> _handlers = new();
    
    public IDisposable Subscribe(Func<DataChangedEvent, Task> handler)
    {
        _handlers.Add(handler);
        return new UnsubscribeToken(_handlers, handler);
    }
    
    private class UnsubscribeToken : IDisposable
    {
        private readonly List<Func<DataChangedEvent, Task>> _handlers;
        private readonly Func<DataChangedEvent, Task> _handler;
        private bool _disposed;
        
        public UnsubscribeToken(List<Func<DataChangedEvent, Task>> handlers, Func<DataChangedEvent, Task> handler)
        {
            _handlers = handlers;
            _handler = handler;
        }
        
        public void Dispose()
        {
            if (!_disposed)
            {
                _handlers.Remove(_handler);
                _disposed = true;
            }
        }
    }
}
```

### Connection Pool Exhaustion

```csharp
// ❌ ANTI-PATTERN: Creating new DbContext for each operation
public async Task<User> GetUserAsync(int id)
{
    using var context = new ApplicationDbContext(); // Connection per call!
    return await context.Users.FindAsync(id);
}

// ✅ BEST PRACTICE: Scoped DbContext from DI
public async Task<User> GetUserAsync(int id, ApplicationDbContext context)
{
    return await context.Users.FindAsync(id);
}

// ✅ Connection string with pooling
"Server=tcp:server.database.windows.net;Database=MyDb;User Id=user@server;Password=pass;Pooling=true;Min Pool Size=5;Max Pool Size=100;"
```

## Troubleshooting

### Diagnosing Performance Issues

1. **Use Application Insights hoặc OpenTelemetry** để track request duration và identify slow endpoints
2. **Check thread pool stats**: `ThreadPool.GetAvailableThreads()` và `ThreadPool.GetMaxThreads()`
3. **Profile with dotnet-trace** để identify CPU và memory bottlenecks
4. **Monitor database query times** với SQL Profiler hoặc EF Core logging

### Common Error Solutions

```csharp
// "Unable to resolve service for type"
ILoggerFactory' while attempting to activate
// → Register ILoggerFactory in DI or use ILogger<T> which is auto-registered

// "Cannot consume scoped service from singleton"
// → Don't inject Scoped service into Singleton. Use IServiceProviderFactory or IServiceScopeFactory

// "A second operation was started on this context"
// → Don't use same DbContext instance for parallel operations
```

## Examples

### Complete Production-Ready Controller

```csharp
[ApiController]
[Route("api/v1/[controller]")]
[Produces(MediaTypeNames.Application.Json)]
public class ProductsController : ControllerBase
{
    private readonly IProductService _productService;
    private readonly IMapper _mapper;
    private readonly ILogger<ProductsController> _logger;
    
    public ProductsController(
        IProductService productService,
        IMapper mapper,
        ILogger<ProductsController> logger)
    {
        _productService = productService;
        _mapper = mapper;
        _logger = logger;
    }
    
    /// <summary>
    /// Get paginated list of products
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(PaginatedResponse<ProductDto>), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<PaginatedResponse<ProductDto>>> GetProducts(
        [FromQuery] ProductQueryParameters parameters,
        CancellationToken cancellationToken)
    {
        _logger.LogInformation("Getting products with filters: {@Parameters}", parameters);
        
        var result = await _productService.GetProductsAsync(parameters, cancellationToken);
        
        Response.Headers.Append("X-Pagination", JsonSerializer.Serialize(result.Pagination));
        
        return Ok(result);
    }
    
    /// <summary>
    /// Get product by ID
    /// </summary>
    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<ProductDto>> GetProduct(
        Guid id,
        CancellationToken cancellationToken)
    {
        var product = await _productService.GetProductByIdAsync(id, cancellationToken);
        
        if (product is null)
            return NotFound(new ProblemDetails
            {
                Status = StatusCodes.Status404NotFound,
                Title = "Product not found",
                Detail = $"Product with ID '{id}' was not found"
            });
        
        return Ok(product);
    }
    
    /// <summary>
    /// Create a new product
    /// </summary>
    [HttpPost]
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status422UnprocessableEntity)]
    public async Task<ActionResult<ProductDto>> CreateProduct(
        [FromBody][Required] CreateProductRequest request,
        CancellationToken cancellationToken)
    {
        _logger.LogInformation("Creating product: {Name}", request.Name);
        
        var result = await _productService.CreateProductAsync(request, cancellationToken);
        
        return CreatedAtAction(
            nameof(GetProduct),
            new { id = result.Id },
            result);
    }
    
    /// <summary>
    /// Update an existing product
    /// </summary>
    [HttpPut("{id:guid}")]
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<ProductDto>> UpdateProduct(
        Guid id,
        [FromBody][Required] UpdateProductRequest request,
        CancellationToken cancellationToken)
    {
        var result = await _productService.UpdateProductAsync(id, request, cancellationToken);
        
        if (result is null)
            return NotFound();
        
        return Ok(result);
    }
    
    /// <summary>
    /// Delete a product
    /// </summary>
    [HttpDelete("{id:guid}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> DeleteProduct(
        Guid id,
        CancellationToken cancellationToken)
    {
        var deleted = await _productService.DeleteProductAsync(id, cancellationToken);
        
        if (!deleted)
            return NotFound();
        
        return NoContent();
    }
}
```

## References

- [Microsoft ASP.NET Core Documentation](https://docs.microsoft.com/aspnet/core)
- [ASP.NET Core Best Practices](./best-practice.md)
- [ASP.NET Core Architecture](./architecture.md)
- [Dependency Injection Guidelines](https://docs.microsoft.com/aspnet/core/fundamentals/dependency-injection)
- [Health checks in ASP.NET Core](https://docs.microsoft.com/aspnet/core/host-and-deploy/health-checks)
- [Exception handling middleware](https://docs.microsoft.com/aspnet/core/fundamentals/error-handling)
