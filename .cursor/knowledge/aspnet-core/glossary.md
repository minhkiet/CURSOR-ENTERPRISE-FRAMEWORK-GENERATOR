---
title: "ASP.NET Core Glossary - Từ Điển Thuật Ngữ ASP.NET Core"
description: "Từ điển toàn diện các thuật ngữ chuyên ngành ASP.NET Core"
tags: ["aspnet-core", "glossary", "terminology", "concepts"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# ASP.NET Core Glossary - Từ Điển Thuật Ngữ ASP.NET Core

## Tổng Quan

Tài liệu này cung cấp một từ điển toàn diện về các thuật ngữ chuyên ngành được sử dụng trong ASP.NET Core development. Mỗi thuật ngữ được định nghĩa rõ ràng với ngữ cảnh sử dụng, ví dụ code, và các thuật ngữ liên quan để giúp developers hiểu và sử dụng đúng các khái niệm này trong thực tế.

ASP.NET Core là một framework phong phú với nhiều concepts và patterns. Việc nắm vững các thuật ngữ này không chỉ giúp giao tiếp hiệu quả hơn trong team mà còn là nền tảng để hiểu sâu các documentation và best practices.

## A

### AbstractValidator

AbstractValidator là base class trong FluentValidation library được sử dụng để define validation rules cho DTOs và models. Nó cung cấp một fluent API cho việc define complex validation logic.

**Ví dụ**:

```csharp
public class CreateOrderRequestValidator : AbstractValidator<CreateOrderRequest>
{
    public CreateOrderRequestValidator()
    {
        RuleFor(x => x.CustomerId)
            .NotEmpty()
            .WithMessage("Customer ID is required");
        
        RuleFor(x => x.Items)
            .NotEmpty()
            .WithMessage("At least one item is required");
        
        RuleForEach(x => x.Items)
            .SetValidator(new OrderItemValidator());
    }
}
```

**Xem thêm**: FluentValidation, IValidator, Data Annotations

### Action Filter

Action Filter là một attribute implement IActionFilter interface cho phép execute code trước và sau khi một action method được executed. Chúng useful cho cross-cutting concerns như logging, validation, và authorization.

**Ví dụ**:

```csharp
public class ValidateModelAttribute : ActionFilterAttribute
{
    public override void OnActionExecuting(ActionExecutingContext context)
    {
        if (!context.ModelState.IsValid)
        {
            context.Result = new BadRequestObjectResult(context.ModelState);
        }
    }
}

[ApiController]
[ValidateModel] // Usage
public class OrdersController : ControllerBase
{
    // ...
}
```

**Xem thêm**: Middleware, IAuthorizationFilter, IResultFilter

### AddScoped / AddTransient / AddSingleton

Đây là các extension methods trong IServiceCollection được sử dụng để register services với different lifetimes:

- **AddSingleton**: Một instance được tạo cho toàn bộ application lifetime
- **AddScoped**: Một instance được tạo per HTTP request
- **AddTransient**: Một instance mới được tạo mỗi khi service được requested

**Ví dụ**:

```csharp
// Singleton - Configuration, Logging
builder.Services.AddSingleton<IAppSettings, AppSettings>();

// Scoped - DbContext, Repositories, Services
builder.Services.AddScoped<IOrderRepository, OrderRepository>();
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString), ServiceLifetime.Scoped);

// Transient - Lightweight stateless services
builder.Services.AddTransient<IDateTimeProvider, DateTimeProvider>();
```

**Xem thêm**: Dependency Injection, IServiceCollection, IoC Container

### ApiController Attribute

ApiController attribute được apply trên một controller class để enable API-specific behaviors như automatic model validation, automatic HTTP 400 responses, và attribute routing requirement.

**Ví dụ**:

```csharp
[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class OrdersController : ControllerBase
{
    // Automatic model validation enabled
    // Automatic 400 responses for invalid models
    // Attribute routing required
}
```

**Xem thêm**: Controller, ControllerBase, Route Attribute

### AsNoTracking

AsNoTracking là một extension method trong Entity Framework Core được sử dụng để disable change tracking cho query. Điều này improves performance đáng kể cho read-only queries vì EF Core không cần create change tracking proxies.

**Ví dụ**:

```csharp
// ⚠️ WITHOUT AsNoTracking - Tracks entities (slower)
var products = await _context.Products
    .Where(p => p.IsActive)
    .ToListAsync();

// ✅ WITH AsNoTracking - Read-only (faster)
var products = await _context.Products
    .AsNoTracking()
    .Where(p => p.IsActive)
    .ToListAsync();
```

**Xem thêm**: Entity Framework Core, Change Tracking, Include

## B

### Background Service

Background Service là một class inherit từ BackgroundService (hoặc implement IHostedService) được sử dụng để run background tasks. Các tasks này chạy after the application starts và trước khi application shuts down.

**Ví dụ**:

```csharp
public class OrderProcessingService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<OrderProcessingService> _logger;
    
    public OrderProcessingService(
        IServiceProvider serviceProvider,
        ILogger<OrderProcessingService> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }
    
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Order processing service starting");
        
        while (!stoppingToken.IsCancellationRequested)
        {
            using var scope = _serviceProvider.CreateScope();
            var orderService = scope.ServiceProvider.GetRequiredService<IOrderService>();
            
            await orderService.ProcessPendingOrdersAsync(stoppingToken);
            
            await Task.Delay(TimeSpan.FromSeconds(30), stoppingToken);
        }
    }
}

// Registration
builder.Services.AddHostedService<OrderProcessingService>();
```

**Xem thêm**: IHostedService, IServiceScope, Task Queue

### Blazor

Blazor là một component-based framework trong ASP.NET Core cho building interactive web UIs sử dụng C# thay vì JavaScript. Có hai hosting models:

- **Blazor Server**: Components run on server, communicate via SignalR
- **Blazor WebAssembly**: Components run in browser as WebAssembly

**Ví dụ**:

```csharp
// Blazor Server Component
@page "/counter"

<h1>Counter</h1>

<p>Current count: @currentCount</p>

<button @onclick="IncrementCount">Click me</button>

@code {
    private int currentCount = 0;
    
    private void IncrementCount()
    {
        currentCount++;
    }
}
```

**Xem thêm**: Razor Components, WebAssembly, SignalR

## C

### Cancellation Token

CancellationToken là một mechanism cho cooperative cancellation của asynchronous operations. Nó cho phép long-running operations bị cancelled gracefully khi client disconnects hoặc timeout.

**Ví dụ**:

```csharp
[HttpGet]
public async Task<ActionResult<IEnumerable<ProductDto>>> GetProducts(
    CancellationToken cancellationToken)
{
    var products = await _context.Products
        .AsNoTracking()
        .Where(p => p.IsActive)
        .ToListAsync(cancellationToken); // Pass token to all async operations
    
    return Ok(products);
}

// Usage in services
public async Task<OrderDto> GetOrderAsync(Guid id, CancellationToken ct)
{
    ct.ThrowIfCancellationRequested(); // Check if cancelled
    
    var order = await _context.Orders
        .FirstOrDefaultAsync(o => o.Id == id, ct);
    
    return _mapper.Map<OrderDto>(order);
}
```

**Xem thêm**: Async/Await, Task, Timeout Pattern

### Configuration System

ASP.NET Core Configuration System là một hierarchical configuration system hỗ trợ multiple sources như JSON files, environment variables, command-line arguments, và user secrets.

**Ví dụ**:

```csharp
// appsettings.json
{
  "AppSettings": {
    "MaxItemsPerPage": 100,
    "EnableCache": true
  },
  "ConnectionStrings": {
    "Default": "Server=localhost;Database=MyApp"
  }
}

// Program.cs
builder.Services.Configure<AppSettings>(
    builder.Configuration.GetSection("AppSettings"));

// Usage with IOptions<T>
public class ProductService
{
    public ProductService(IOptions<AppSettings> settings)
    {
        var maxItems = settings.Value.MaxItemsPerPage;
    }
}

// Environment variable override
// AppSettings__MaxItemsPerPage=50
```

**Xem thêm**: IOptions, User Secrets, Environment Variables

### CQRS (Command Query Responsibility Segregation)

CQRS là một pattern tách biệt read (queries) và write (commands) operations thành different models. Điều này cho phép optimize read và write operations independently.

**Ví dụ**:

```csharp
// Command - Write
public record CreateOrderCommand : IRequest<Result<OrderDto>>
{
    public Guid CustomerId { get; init; }
    public List<OrderItemDto> Items { get; init; }
}

public class CreateOrderCommandHandler : IRequestHandler<CreateOrderCommand, Result<OrderDto>>
{
    // Handle write logic
}

// Query - Read (separate, optimized)
public record GetOrderByIdQuery(Guid Id) : IRequest<OrderDetailDto?>;

public class GetOrderByIdQueryHandler : IRequestHandler<GetOrderByIdQuery, OrderDetailDto?>
{
    // Handle read logic with optimized projection
}
```

**Xem thêm**: MediatR, Repository Pattern, Event Sourcing

### CORS (Cross-Origin Resource Sharing)

CORS là một W3C specification cho phép web pages từ một domain access resources từ một domain khác. ASP.NET Core cung cấp middleware để configure CORS policies.

**Ví dụ**:

```csharp
// Configuration
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.WithOrigins("https://frontend.example.com")
            .AllowAnyMethod()
            .AllowAnyHeader()
            .WithMethods("GET", "POST", "PUT", "DELETE")
            .WithHeaders("Authorization", "Content-Type");
    });
});

// Usage
app.UseCors("AllowFrontend");
```

**Xem thêm**: Same-Origin Policy, HTTP Headers, Security

## D

### DbContext

DbContext là một class trong Entity Framework Core đại diện cho một session với database. Nó là primary object để query và save data và là một implementation của Unit of Work pattern.

**Ví dụ**:

```csharp
public class ApplicationDbContext : DbContext
{
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<Customer> Customers => Set<Customer>();
    public DbSet<Product> Products => Set<Product>();
    
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
        ChangeTracker.QueryTrackingBehavior = QueryTrackingBehavior.NoTracking;
    }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
    }
}

// Registration
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString));
```

**Xem thêm**: Entity Framework Core, DbSet, Unit of Work

### Dependency Injection (DI)

Dependency Injection là một design pattern trong đó dependencies được passed vào một class thay vì được created bên trong class đó. ASP.NET Core có built-in DI container.

**Ví dụ**:

```csharp
// Service registration
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddTransient<IDateTimeProvider, DateTimeProvider>();
builder.Services.AddSingleton<IAppSettings, AppSettings>();

// Constructor injection
public class OrdersController : ControllerBase
{
    private readonly IOrderService _orderService;
    private readonly ILogger<OrdersController> _logger;
    
    public OrdersController(
        IOrderService orderService,
        ILogger<OrdersController> logger)
    {
        _orderService = orderService;
        _logger = logger;
    }
}
```

**Xem thêm**: IoC Container, Service Lifetimes, Service Locator

### Domain-Driven Design (DDD)

Domain-Driven Design là một approach cho software development tập trung vào modeling based on real-world business domain. Nó emphasizes collaboration between technical và domain experts.

**Key Concepts**:
- **Aggregates**: Clusters of related objects treated as a unit
- **Entities**: Objects with distinct identity
- **Value Objects**: Objects defined by their attributes
- **Domain Events**: Events that are significant to the domain
- **Bounded Contexts**: Boundary around a specific domain

**Xem thêm**: Clean Architecture, Entity, Value Object

## E

### Endpoint Routing

Endpoint Routing là một system trong ASP.NET Core cho mapping URLs to endpoints (controllers, Razor Pages, Minimal APIs). Nó combines routing và endpoint resolution.

**Ví dụ**:

```csharp
// Convention-based routing
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    [HttpGet]           // → GET api/orders
    [HttpPost]          // → POST api/orders
    [HttpGet("{id}")]    // → GET api/orders/{id}
}

// Attribute routing
[HttpGet("orders/{year:int}/{month:int}")]
public async Task<IActionResult> GetOrdersByMonth(int year, int month)
{
    // Matches /orders/2024/06
}

// Minimal APIs
app.MapGet("/products", async (AppDbContext db) =>
{
    var products = await db.Products.ToListAsync();
    return Results.Ok(products);
});
```

**Xem thêm**: MapControllers, MapRazorPages, Route Constraints

### Entity Framework Core (EF Core)

EF Core là một lightweight, cross-platform ORM cho .NET. Nó cho phép developers work với databases sử dụng .NET objects thay vì raw SQL.

**Ví dụ**:

```csharp
// Query
var orders = await _context.Orders
    .AsNoTracking()
    .Include(o => o.Customer)
    .Include(o => o.Items)
        .ThenInclude(i => i.Product)
    .Where(o => o.Status == OrderStatus.Pending)
    .OrderByDescending(o => o.CreatedAt)
    .Skip(offset)
    .Take(pageSize)
    .ToListAsync();

// Insert
_context.Products.Add(product);
await _context.SaveChangesAsync();

// Update
_context.Attach(existingProduct);
existingProduct.Price = newPrice;
await _context.SaveChangesAsync();

// Delete
_context.Products.Remove(product);
await _context.SaveChangesAsync();
```

**Xem thêm**: DbContext, DbSet, Migrations

### Exception Handler Middleware

Exception Handler Middleware là một middleware component cho catching và handling exceptions thrown trong the pipeline. Nó có thể be configured với custom error pages hoặc JSON responses.

**Ví dụ**:

```csharp
// Global exception handler
public class GlobalExceptionHandler : IExceptionHandler
{
    private readonly ILogger<GlobalExceptionHandler> _logger;
    
    public GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger)
    {
        _logger = logger;
    }
    
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        var correlationId = httpContext.TraceIdentifier;
        
        _logger.LogError(exception, "Unhandled exception. CorrelationId: {CorrelationId}", correlationId);
        
        var (statusCode, response) = exception switch
        {
            ValidationException ve => (400, new ErrorResponse { /* ... */ }),
            NotFoundException nf => (404, new ErrorResponse { /* ... */ }),
            _ => (500, new ErrorResponse { /* ... */ })
        };
        
        httpContext.Response.StatusCode = statusCode;
        await httpContext.Response.WriteAsJsonAsync(response, cancellationToken);
        
        return true;
    }
}

// Registration
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();

app.UseExceptionHandler();
```

**Xem thêm**: Middleware, Error Handling, Problem Details

## F

### FluentValidation

FluentValidation là một library cho building strongly-typed validation rules sử dụng a fluent interface. Nó là một alternative cho Data Annotations.

**Ví dụ**:

```csharp
public class CustomerValidator : AbstractValidator<Customer>
{
    public CustomerValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty()
            .WithMessage("Name is required")
            .Length(2, 50)
            .WithMessage("Name must be between 2 and 50 characters");
        
        RuleFor(x => x.Email)
            .NotEmpty()
            .EmailAddress()
            .WithMessage("A valid email is required");
        
        RuleFor(x => x.Address)
            .NotNull()
            .SetValidator(new AddressValidator());
        
        RuleForEach(x => x.Orders)
            .SetValidator(new OrderValidator());
    }
}

// Usage
var validator = new CustomerValidator();
var result = await validator.ValidateAsync(customer);

if (!result.IsValid)
{
    var errors = result.Errors
        .GroupBy(e => e.PropertyName)
        .ToDictionary(g => g.Key, g => g.Select(e => e.ErrorMessage).ToArray());
}
```

**Xem thêm**: Data Annotations, IValidator, Validation

## G

### gRPC

gRPC là một high-performance RPC framework sử dụng Protocol Buffers làm interface definition language và HTTP/2 cho transport. Nó lý tưởng cho microservices communication.

**Ví dụ**:

```protobuf
// order.proto
syntax = "proto3";

service OrderService {
    rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);
    rpc GetOrder(GetOrderRequest) returns (Order);
    rpc StreamOrders(StreamOrdersRequest) returns (stream Order);
}

message CreateOrderRequest {
    string customer_id = 1;
    repeated OrderItem items = 2;
}
```

```csharp
// Protobuf service implementation
public class OrderService : OrderServiceBase
{
    private readonly IOrderService _orderService;
    
    public override async Task<CreateOrderResponse> CreateOrder(
        CreateOrderRequest request,
        ServerCallContext context)
    {
        var command = new CreateOrderCommand
        {
            CustomerId = Guid.Parse(request.CustomerId),
            Items = request.Items.Select(i => new OrderItemDto
            {
                ProductId = Guid.Parse(i.ProductId),
                Quantity = i.Quantity
            }).ToList()
        };
        
        var result = await _orderService.CreateOrderAsync(command, context.CancellationToken);
        
        return new CreateOrderResponse
        {
            OrderId = result.Value.Id.ToString(),
            Success = result.IsSuccess
        };
    }
}
```

**Xem thêm**: Protocol Buffers, HTTP/2, Protobuf-net

## H

### Health Checks

Health Checks là một feature trong ASP.NET Core cho monitoring application health. Chúng cung cấp endpoints để check nếu application đang hoạt động và có thể respond requests.

**Ví dụ**:

```csharp
// Configuration
builder.Services.AddHealthChecks()
    .AddDbContextCheck<ApplicationDbContext>("database")
    .AddRedis(builder.Configuration.GetConnectionString("Redis"), "cache")
    .AddUrlGroup(new Uri("https://api.example.com/health"), "external-api");

// Endpoints
app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = async (context, report) =>
    {
        context.Response.ContentType = "application/json";
        await context.Response.WriteAsJsonAsync(new
        {
            status = report.Status.ToString(),
            checks = report.Entries.Select(e => new
            {
                name = e.Key,
                status = e.Value.Status.ToString()
            })
        });
    }
});

// Kubernetes probes
app.MapHealthChecks("/health/live");  // Is app running?
app.MapHealthChecks("/health/ready"); // Can it serve traffic?
```

**Xem thêm**: Monitoring, Kubernetes, Liveness Probe

### HttpClient

HttpClient là một class cho sending HTTP requests và receiving HTTP responses. Trong ASP.NET Core, nó nên được registered as a typed client hoặc sử dụng HttpClientFactory.

**Ví dụ**:

```csharp
// Typed HttpClient
public interface IProductApiClient
{
    Task<ProductDto?> GetProductAsync(int id);
    Task<IReadOnlyList<ProductDto>> GetProductsAsync();
}

public class ProductApiClient : IProductApiClient
{
    private readonly HttpClient _httpClient;
    
    public ProductApiClient(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }
    
    public async Task<ProductDto?> GetProductAsync(int id)
    {
        var response = await _httpClient.GetAsync($"/api/products/{id}");
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<ProductDto>();
    }
}

// Registration with HttpClientFactory
builder.Services.AddHttpClient<IProductApiClient, ProductApiClient>(client =>
{
    client.BaseAddress = new Uri("https://api.example.com");
    client.Timeout = TimeSpan.FromSeconds(30);
});
```

**Xem thêm**: HttpClientFactory, Refit, Polly

## I

### IAsyncEnumerable

IAsyncEnumerable là một interface cho representing an asynchronous stream of values. Nó được sử dụng cho streaming data từ databases hoặc APIs.

**Ví dụ**:

```csharp
[HttpGet]
public async Task<ActionResult> GetOrdersStream(CancellationToken ct)
{
    Response.ContentType = "application/json";
    
    await foreach (var order in _orderService.GetOrdersStreamAsync(ct))
    {
        await Response.WriteAsJsonAsync(order, ct);
        await Response.Body.FlushAsync(ct);
    }
}

// Usage with EF Core for streaming large results
public async IAsyncEnumerable<Order> GetOrdersStreamAsync(
    [EnumeratorCancellation] CancellationToken ct)
{
    await using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync(ct);
    
    await using var command = new SqlCommand("SELECT * FROM Orders", connection);
    await using var reader = await command.ExecuteReaderAsync(ct);
    
    while (await reader.ReadAsync(ct))
    {
        yield return new Order
        {
            Id = reader.GetGuid(0),
            CustomerId = reader.GetGuid(1),
            // ...
        };
    }
}
```

**Xem thêm**: IEnumerable, Stream, Enumerator

### Include / ThenInclude

Include và ThenInclude là extension methods trong Entity Framework Core cho eager loading related entities.

**Ví dụ**:

```csharp
// Single level include
var orders = await _context.Orders
    .Include(o => o.Customer) // Load Customer with Order
    .ToListAsync();

// Multiple levels with ThenInclude
var orders = await _context.Orders
    .Include(o => o.Customer)
        .ThenInclude(c => c.Address) // Load Address with Customer
    .Include(o => o.Items)
        .ThenInclude(i => i.Product)
            .ThenInclude(p => p.Category) // Three levels deep
    .ToListAsync();

// Filtered include (EF Core 7+)
var orders = await _context.Orders
    .Include(o => o.Items.Where(i => i.Quantity > 0)) // Only items with quantity > 0
    .ToListAsync();
```

**Xem thêm**: Eager Loading, Lazy Loading, Explicit Loading

## J

### JWT (JSON Web Token)

JWT là một standard cho creating access tokens claims-based. ASP.NET Core hỗ trợ JWT Bearer authentication out of the box.

**Ví dụ**:

```csharp
// JWT Configuration
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = configuration["Jwt:Issuer"],
            ValidAudience = configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(configuration["Jwt:Key"]!))
        };
    });

// Token Generation
public string GenerateToken(User user)
{
    var claims = new[]
    {
        new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
        new Claim(ClaimTypes.Email, user.Email),
        new Claim(ClaimTypes.Role, user.Role)
    };
    
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
```

**Xem thêm**: Authentication, Authorization, Claims

## K

### Kestrel

Kestrel là cross-platform web server được tích hợp sẵn trong ASP.NET Core. Nó là default server khi running ASP.NET Core applications.

**Ví dụ**:

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Kestrel configuration
builder.WebHost.ConfigureKestrel(options =>
{
    options.ListenAnyIP(5000);
    options.Limits.MaxConcurrentConnections = 100;
    options.Limits.MaxConcurrentUpgradedConnections = 100;
    options.Limits.MaxRequestBodySize = 10 * 1024 * 1024; // 10MB
    options.Limits.MinRequestBodyDataRate = 
        new MinDataRate(bytesPerSecond: 100, gracePeriod: TimeSpan.FromSeconds(10));
});

// Run
var app = builder.Build();
app.Run();
```

**Xem thêm**: Web Server, IIS Integration, Reverse Proxy

## L

### Logging

ASP.NET Core có built-in logging framework với support cho multiple providers. ILogger<T> được inject vào services để log messages.

**Ví dụ**:

```csharp
public class OrderService : IOrderService
{
    private readonly ILogger<OrderService> _logger;
    
    public OrderService(ILogger<OrderService> logger)
    {
        _logger = logger;
    }
    
    public async Task<OrderDto> CreateOrderAsync(CreateOrderCommand command, CancellationToken ct)
    {
        _logger.LogInformation(
            "Creating order for customer {CustomerId} with {ItemCount} items",
            command.CustomerId,
            command.Items.Count);
        
        try
        {
            var order = await _orderRepository.CreateAsync(command, ct);
            
            _logger.LogInformation(
                "Order {OrderId} created successfully",
                order.Id);
            
            return _mapper.Map<OrderDto>(order);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Failed to create order for customer {CustomerId}",
                command.CustomerId);
            throw;
        }
    }
}
```

**Log Levels**:
- **Trace**: Detailed debugging information
- **Debug**: Development debugging
- **Information**: General information
- **Warning**: Abnormal situations
- **Error**: Errors
- **Critical**: Critical failures

**Xem thêm**: Structured Logging, Serilog, Application Insights

## M

### MediatR

MediatR là một library implement Mediator pattern trong .NET. Nó giúp decouple sender và receiver của requests/queries/commands.

**Ví dụ**:

```csharp
// Command
public record CreateOrderCommand : IRequest<Result<OrderDto>>
{
    public Guid CustomerId { get; init; }
    public List<OrderItemDto> Items { get; init; }
}

// Handler
public class CreateOrderCommandHandler : IRequestHandler<CreateOrderCommand, Result<OrderDto>>
{
    private readonly IOrderRepository _repository;
    
    public CreateOrderCommandHandler(IOrderRepository repository)
    {
        _repository = repository;
    }
    
    public async Task<Result<OrderDto>> Handle(
        CreateOrderCommand request,
        CancellationToken cancellationToken)
    {
        var order = Order.Create(request.CustomerId, request.Items);
        await _repository.AddAsync(order, cancellationToken);
        return Result.Success(_mapper.Map<OrderDto>(order));
    }
}

// Registration
builder.Services.AddMediatR(cfg => 
    cfg.RegisterServicesFromAssemblyContaining<Program>());

// Usage in Controller
public class OrdersController : ControllerBase
{
    private readonly IMediator _mediator;
    
    public OrdersController(IMediator mediator)
    {
        _mediator = mediator;
    }
    
    [HttpPost]
    public async Task<ActionResult<OrderDto>> CreateOrder(
        CreateOrderCommand command,
        CancellationToken ct)
    {
        var result = await _mediator.Send(command, ct);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(result.Error);
    }
}
```

**Xem thêm**: Mediator Pattern, CQRS, Pipeline Behavior

### Middleware

Middleware là các components được pipeline để xử lý requests và responses. Mỗi middleware có thể short-circuit the request, pass to next, hoặc modify the response.

**Ví dụ**:

```csharp
// Custom middleware
public class RequestTimingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestTimingMiddleware> _logger;
    
    public RequestTimingMiddleware(RequestDelegate next, ILogger<RequestTimingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }
    
    public async Task InvokeAsync(HttpContext context)
    {
        var stopwatch = Stopwatch.StartNew();
        
        await _next(context);
        
        stopwatch.Stop();
        
        _logger.LogInformation(
            "Request {Method} {Path} completed in {ElapsedMs}ms",
            context.Request.Method,
            context.Request.Path,
            stopwatch.ElapsedMilliseconds);
    }
}

// Registration
var app = builder.Build();

app.UseMiddleware<RequestTimingMiddleware>();

// Or using extension method
app.UseRequestTiming();

// Common middleware order
app.UseExceptionHandler();           // 1. Error handling
app.UseHsts();                      // 2. Security headers
app.UseHttpsRedirection();           // 3. HTTPS redirect
app.UseStaticFiles();               // 4. Static files
app.UseResponseCompression();       // 5. Compression
app.UseRouting();                   // 6. Routing
app.UseCors();                      // 7. CORS
app.UseAuthentication();            // 8. Authentication
app.UseAuthorization();             // 9. Authorization
app.MapControllers();               // 10. Endpoints
```

**Xem thêm**: Request Delegate, Middleware Pipeline, Built-in Middleware

### Minimal APIs

Minimal APIs là một approach cho building APIs với minimal boilerplate. Routes được mapped directly to handler functions without controllers.

**Ví dụ**:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Simple endpoint
app.MapGet("/", () => "Hello World!");

// With parameters
app.MapGet("/products/{id:int}", async (int id, AppDbContext db) =>
{
    var product = await db.Products.FindAsync(id);
    return product is null ? Results.NotFound() : Results.Ok(product);
});

// Multiple parameters
app.MapGet("/products/search", async (
    [FromQuery] string? name,
    [FromQuery] decimal? minPrice,
    [FromQuery] int page = 1,
    AppDbContext db = default) =>
{
    var query = db.Products.AsQueryable();
    
    if (!string.IsNullOrEmpty(name))
        query = query.Where(p => p.Name.Contains(name));
    
    if (minPrice.HasValue)
        query = query.Where(p => p.Price >= minPrice.Value);
    
    var products = await query
        .Skip((page - 1) * 10)
        .Take(10)
        .ToListAsync();
    
    return Results.Ok(products);
});

// With dependency injection
app.MapPost("/orders", async (
    CreateOrderRequest request,
    IOrderService orderService,
    CancellationToken ct) =>
{
    var result = await orderService.CreateOrderAsync(request, ct);
    return result.IsSuccess 
        ? Results.Created($"/orders/{result.Value.Id}", result.Value)
        : Results.BadRequest(result.Error);
});
```

**Xem thêm**: Controllers, Endpoints, Route Handlers

## N

### NoTracking

NoTracking là một extension method (alias for AsNoTracking) trong Entity Framework Core disable change tracking cho queries, improving performance cho read-only scenarios.

**Ví dụ**:

```csharp
var customers = await _context.Customers
    .NoTracking()  // Same as AsNoTracking()
    .Where(c => c.IsActive)
    .ToListAsync();
```

**Xem thêm**: AsNoTracking, Change Tracking

## O

### Output Caching

Output Caching (ASP.NET Core 7+) là một feature cho caching entire HTTP responses. Nó có thể be configured per endpoint với tags cho invalidation.

**Ví dụ**:

```csharp
// Configuration
builder.Services.AddOutputCache();

// Endpoints
app.MapGet("/products", async (AppDbContext db) =>
{
    var products = await db.Products.AsNoTracking().ToListAsync();
    return Results.Ok(products);
})
.CacheOutput(policy => policy
    .Tag("products")
    .VaryByQueryKeys("category", "page")
    .Expire(TimeSpan.FromMinutes(5)));

// Cache invalidation
app.MapPost("/products", async (
    CreateProductRequest request,
    AppDbContext db,
    IOutputCacheStore cache,
    CancellationToken ct) =>
{
    // Create product...
    await cache.EvictByTagAsync("products", ct); // Invalidate all cached /products
});
```

**Xem thêm**: Response Caching, Memory Cache, Distributed Cache

## P

### Pipeline Behavior

Pipeline Behaviors là các components trong MediatR pipeline cho cross-cutting concerns như logging, validation, và caching được applied cho tất cả requests.

**Ví dụ**:

```csharp
public class LoggingBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
{
    private readonly ILogger<LoggingBehavior<TRequest, TResponse>> _logger;
    
    public LoggingBehavior(ILogger<LoggingBehavior<TRequest, TResponse>> logger)
    {
        _logger = logger;
    }
    
    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        var requestName = typeof(TRequest).Name;
        
        _logger.LogInformation("Handling {RequestName}", requestName);
        
        var response = await next();
        
        _logger.LogInformation("Handled {RequestName}", requestName);
        
        return response;
    }
}

// Registration
builder.Services.AddMediatR(cfg =>
{
    cfg.RegisterServicesFromAssemblyContaining<Program>();
    cfg.AddOpenBehavior(typeof(LoggingBehavior<,>));
    cfg.AddOpenBehavior(typeof(ValidationBehavior<,>));
});
```

**Xem thêm**: MediatR, Cross-cutting Concerns, Decorator Pattern

### Problem Details

Problem Details là một standard format cho representing API errors specified in RFC 7807. ASP.NET Core hỗ trợ nó natively.

**Ví dụ**:

```csharp
// Standard problem details response
{
    "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1",
    "title": "Bad Request",
    "status": 400,
    "detail": "One or more validation errors occurred.",
    "traceId": "00-abc123-def456-00",
    "errors": {
        "CustomerId": ["Customer ID is required"],
        "Items[0].Quantity": ["Quantity must be greater than 0"]
    }
}

// Automatic with ApiController
[ApiController]
public class OrdersController : ControllerBase
{
    // ModelState errors automatically returned as Problem Details
}
```

**Xem thêm**: RFC 7807, Error Handling, Validation

## R

### Razor Pages

Razor Pages là một page-based model cho ASP.NET Core Web Applications. Khác với MVC với controllers và views riêng biệt, Razor Pages combine view và controller logic trong một page model.

**Ví dụ**:

```csharp
// Pages/Orders/Index.cshtml
@page
@model MyApp.Pages.Orders.IndexModel
@{
    ViewData["Title"] = "Orders";
}

<h1>@ViewData["Title"]</h1>

<table class="table">
    @foreach (var order in Model.Orders)
    {
        <tr>
            <td>@order.OrderNumber</td>
            <td>@order.CustomerName</td>
            <td>@order.Total.ToString("C")</td>
        </tr>
    }
</table>

// Pages/Orders/Index.cshtml.cs
public class IndexModel : PageModel
{
    private readonly IOrderService _orderService;
    
    public IndexModel(IOrderService orderService)
    {
        _orderService = orderService;
    }
    
    public IReadOnlyList<OrderDto> Orders { get; private set; } = new List<OrderDto>();
    
    public async Task OnGetAsync()
    {
        Orders = await _orderService.GetOrdersAsync();
    }
}
```

**Xem thêm**: Razor Syntax, Page Model, MVC

### Repository Pattern

Repository Pattern là một abstraction layer giữa data access logic và business logic. Nó hide data access implementation details.

**Ví dụ**:

```csharp
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(Guid id, CancellationToken ct = default);
    Task<Order?> GetByIdWithItemsAsync(Guid id, CancellationToken ct = default);
    Task<IReadOnlyList<Order>> GetByCustomerIdAsync(Guid customerId, CancellationToken ct = default);
    Task AddAsync(Order order, CancellationToken ct = default);
    void Update(Order order);
    void Delete(Order order);
}

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
            .FirstOrDefaultAsync(o => o.Id == id, ct);
    }
    
    // ... other methods
}
```

**Xem thêm**: Unit of Work, Data Access, Abstraction

## S

### SignalR

SignalR là một library cho adding real-time web functionality cho applications. Nó cho phép server-to-client push communication sử dụng WebSockets với fallback to other transports.

**Ví dụ**:

```csharp
// Hub definition
public class ChatHub : Hub
{
    public async Task SendMessage(string user, string message)
    {
        await Clients.All.SendAsync("ReceiveMessage", user, message);
    }
    
    public async Task JoinRoom(string roomName)
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, roomName);
        await Clients.Group(roomName).SendAsync("UserJoined", Context.ConnectionId);
    }
    
    public override async Task OnConnectedAsync()
    {
        await base.OnConnectedAsync();
        // Connection established
    }
    
    public override async Task OnDisconnectedAsync(Exception? exception)
    {
        await base.OnDisconnectedAsync(exception);
        // Connection terminated
    }
}

// Client-side (JavaScript)
const connection = new signalR.HubConnectionBuilder()
    .withUrl("/chatHub")
    .withAutomaticReconnect()
    .build();

connection.on("ReceiveMessage", (user, message) => {
    console.log(`${user}: ${message}`);
});

await connection.start();
await connection.invoke("SendMessage", "User", "Hello!");
```

**Xem thêm**: WebSockets, Real-time, Hubs

## T

### TestServer

TestServer là một class trong ASP.NET Core testing infrastructure cho creating an in-memory test server. Nó cho phép integration tests mà không cần actual HTTP requests.

**Ví dụ**:

```csharp
public class OrdersControllerTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;
    
    public OrdersControllerTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                // Replace services for testing
                services.RemoveAll(typeof(DbContextOptions<ApplicationDbContext>));
                services.AddDbContext<ApplicationDbContext>(options =>
                    options.UseInMemoryDatabase("TestDb"));
            });
        });
    }
    
    [Fact]
    public async Task CreateOrder_WithValidRequest_ReturnsCreated()
    {
        // Arrange
        var client = _factory.CreateClient();
        var request = new CreateOrderRequest
        {
            CustomerId = Guid.NewGuid(),
            Items = new List<OrderItemDto>
            {
                new() { ProductId = Guid.NewGuid(), Quantity = 1 }
            }
        };
        
        // Act
        var response = await client.PostAsJsonAsync("/api/orders", request);
        
        // Assert
        response.StatusCode.Should().Be(StatusCodes.Status201Created);
        
        var order = await response.Content.ReadFromJsonAsync<OrderDto>();
        order.Should().NotBeNull();
    }
}
```

**Xem thêm**: Integration Testing, WebApplicationFactory, Mocking

## V

### Value Objects

Value Objects là các objects được defined bởi their attributes thay vì a unique identity. Chúng là immutable và được compared by value.

**Ví dụ**:

```csharp
public record Money
{
    public decimal Amount { get; init; }
    public Currency Currency { get; init; }
    
    private Money(decimal amount, Currency currency)
    {
        if (amount < 0)
            throw new ArgumentException("Amount cannot be negative");
        Amount = Math.Round(amount, 2);
        Currency = currency;
    }
    
    public static Money From(decimal amount, Currency currency = Currency.USD) =>
        new(amount, currency);
    
    public static Money Zero => new(0, Currency.USD);
    
    public static Money operator +(Money a, Money b)
    {
        if (a.Currency != b.Currency)
            throw new InvalidOperationException("Cannot add different currencies");
        return new Money(a.Amount + b.Amount, a.Currency);
    }
    
    // EF Core value converter
    private class EFConverter : ValueConverter<Money, decimal>
    {
        public EFConverter() : base(
            m => m.Amount,
            v => new Money(v, Currency.USD))
        { }
    }
}

// Usage
public class Order
{
    public Money TotalAmount { get; private set; }
}
```

**Xem thêm**: Entity, DDD, Immutability

## W

### WebApplicationFactory

WebApplicationFactory là một class trong Microsoft.AspNetCore.Mvc.Testing cho creating test servers với TestServer infrastructure. Nó simplified integration testing.

**Ví dụ**:

```csharp
public class IntegrationTestFixture : IDisposable
{
    public readonly WebApplicationFactory<Program> Factory;
    
    public IntegrationTestFixture()
    {
        Factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(builder =>
            {
                builder.ConfigureServices(services =>
                {
                    // Add test-specific services
                    services.AddScoped<IAuthorizationHandler, TestAuthorizationHandler>();
                });
                
                builder.Configure(app =>
                {
                    // Add test middleware
                    app.Use(async (context, next) =>
                    {
                        context.Items["TestMode"] = true;
                        await next();
                    });
                });
            });
    }
    
    public void Dispose()
    {
        Factory.Dispose();
    }
}
```

**Xem thêm**: TestServer, Integration Tests, Fixture

## X

### XML Documentation

XML Documentation là các comments trong source code được marked với triple-slash (///) được sử dụng để generate documentation.

**Ví dụ**:

```csharp
/// <summary>
/// Creates a new order for the specified customer.
/// </summary>
/// <param name="command">The create order command containing customer and item information.</param>
/// <param name="cancellationToken">A cancellation token to cancel the operation.</param>
/// <returns>
/// A result containing the created order DTO if successful,
/// or an error result if validation failed or the customer was not found.
/// </returns>
/// <exception cref="ArgumentException">
/// Thrown when the command contains invalid data.
/// </exception>
/// <remarks>
/// This method validates the customer exists and all products are available
/// before creating the order. Domain events are published after successful creation.
/// </remarks>
/// <example>
/// ```csharp
/// var command = new CreateOrderCommand
/// {
///     CustomerId = customerId,
///     Items = new List&lt;OrderItemDto&gt; { new() { ProductId = productId, Quantity = 2 } }
/// };
/// var result = await _mediator.Send(command, CancellationToken.None);
/// ```
/// </example>
public async Task<Result<OrderDto>> Handle(
    CreateOrderCommand command,
    CancellationToken cancellationToken)
{
    // Implementation
}
```

**Xem thêm**: IntelliSense, XML Comments, Documentation Generation

## References

- [Microsoft ASP.NET Core Documentation](https://docs.microsoft.com/aspnet/core)
- [Entity Framework Core Documentation](https://docs.microsoft.com/ef/core)
- [ASP.NET Core Security](https://docs.microsoft.com/aspnet/core/security/)
- [FluentValidation Documentation](https://docs.fluentvalidation.net/)
- [MediatR GitHub Repository](https://github.com/jbogard/MediatR)
