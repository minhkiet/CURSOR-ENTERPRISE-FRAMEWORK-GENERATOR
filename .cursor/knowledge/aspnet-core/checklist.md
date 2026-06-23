---
title: "ASP.NET Core Checklist - Danh Sách Kiểm Tra Triển Khai"
description: "Danh sách kiểm tra toàn diện cho pre-deployment và code review trong ASP.NET Core"
tags: ["aspnet-core", "checklist", "deployment", "code-review", "quality-assurance"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# ASP.NET Core Checklist - Danh Sách Kiểm Tra Triển Khai

## Tổng Quan

Trước khi deploy bất kỳ ứng dụng ASP.NET Core nào lên production, điều quan trọng là phải thực hiện một series của checks để đảm bảo rằng ứng dụng đáp ứng các tiêu chuẩn về quality, security, performance, và reliability. Checklist này cung cấp một comprehensive guide cho cả developers và reviewers để verify rằng tất cả necessary steps đã được completed.

Việc sử dụng checklist không chỉ giúp catch potential issues trước khi chúng trở thành production problems mà còn ensures consistency across deployments và teams. Mỗi section trong checklist được thiết kế để cover một specific area của application quality, từ code structure đến infrastructure configuration.

## Mục Đích

Danh sách kiểm tra này phục vụ nhiều mục đích quan trọng:

1. **Pre-deployment Validation**: Đảm bảo mọi critical requirements được met trước khi deploy
2. **Code Review Guide**: Cung cấp systematic approach cho code reviews
3. **Quality Gate**: Thiết lập minimum standards cho code quality
4. **Knowledge Transfer**: Giúp team members understand what to check và why
5. **Compliance**: Hỗ trợ compliance requirements và audit processes

## Danh Sách Kiểm Tra Chi Tiết

### 1. Project Structure và Configuration

#### 1.1 Project Organization

```markdown
□ Project structure follows Clean Architecture hoặc established pattern
□ Solution file có meaningful structure (src/, tests/, scripts/)
□，每个 project có clear purpose và single responsibility
□ Namespace structure reflects folder structure
□ Common project có minimal dependencies
```

**Verification Commands**:

```bash
# Kiểm tra project structure
dotnet new sln -n MyApp
dotnet sln add src/MyApp.Api
dotnet sln add src/MyApp.Application
dotnet sln add src/MyApp.Domain
dotnet sln add src/MyApp.Infrastructure
dotnet sln add tests/MyApp.UnitTests
dotnet sln add tests/MyApp.IntegrationTests

# Kiểm tra dependencies
dotnet list src/MyApp.Api/package reference
```

#### 1.2 Configuration Management

```markdown
□ appsettings.json chứa base configuration
□ appsettings.Development.json chứa development overrides
□ appsettings.Production.json chứa production settings (không có secrets)
□ Secrets được managed qua environment variables hoặc secret manager
□ Configuration có strong typing với IOptions pattern
□ Connection strings được validate tại startup
□ All configuration values được logged at startup (sanitized)
```

**Configuration Structure Example**:

```json
// appsettings.json
{
  "AppSettings": {
    "Environment": "Development",
    "EnableSwagger": true,
    "DefaultLanguage": "en-US"
  },
  "ConnectionStrings": {
    "Default": "Server=localhost;Database=MyApp;Trusted_Connection=true"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information"
    }
  }
}

// appsettings.Production.json (no connection strings)
{
  "AppSettings": {
    "Environment": "Production",
    "EnableSwagger": false
  },
  "Logging": {
    "LogLevel": {
      "Default": "Warning"
    }
  }
}

// Environment variable overrides
// ASPNETCORE_ENVIRONMENT=Production
// ConnectionStrings__Default=Server=prod-server;Database=MyApp;User Id=user;Password=pass
```

#### 1.3 Dependency Injection Setup

```markdown
□ All services được registered với appropriate lifetimes
□ DbContext registered as Scoped (not Singleton!)
□ Repository pattern implemented for data access
□ Third-party services có interfaces for testability
□ DI container configuration được centralized
□ Potential captive dependencies được identified và resolved
```

**DI Lifetime Verification Checklist**:

```csharp
// Singleton - use for: Configuration, Logging, Caching
builder.Services.AddSingleton<IAppSettings, AppSettings>();

// Scoped - use for: DbContext, Repositories, Services
builder.Services.AddScoped<IOrderRepository, OrderRepository>();
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString), ServiceLifetime.Scoped);

// Transient - use for: Lightweight stateless services
builder.Services.AddTransient<IDateTimeProvider, DateTimeProvider>();

// ❌ DON'T: DbContext as Singleton
// builder.Services.AddSingleton<DbContext>(); // WRONG!

// ❌ DON'T: Captive dependency
// Singleton service depending on Scoped service
```

### 2. Security Checklist

#### 2.1 Authentication và Authorization

```markdown
□ JWT tokens được validated properly
□ Token expiration được handled
□ Refresh token mechanism implemented (if applicable)
□ Authorization policies được defined và documented
□ Role-based access control (RBAC) implemented correctly
□ Claims-based authorization available for complex scenarios
□ Anonymous endpoints được explicitly marked
□ API keys (if used) được stored securely
```

**JWT Security Verification**:

```csharp
// ✅ CORRECT: Full JWT validation
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
                Encoding.UTF8.GetBytes(configuration["Jwt:Key"]!)),
            ClockSkew = TimeSpan.FromMinutes(1),
            RequireExpirationTime = true
        };
    });

// ❌ WRONG: Missing validations
// options.TokenValidationParameters = new TokenValidationParameters
// {
//     ValidateIssuerSigningKey = false, // WRONG!
//     ValidateLifetime = false          // WRONG!
// };
```

#### 2.2 Input Validation

```markdown
□ All input được validated before processing
□ DTOs có Data Annotations hoặc FluentValidation rules
□ SQL injection prevention via parameterized queries
□ XSS prevention via output encoding
□ Mass assignment vulnerabilities được prevented
□ File upload validation (type, size, content)
□ Regex patterns được tested against edge cases
□ Maximum request size được configured
```

**Input Validation Example**:

```csharp
// DTO with validation
public class CreateOrderRequest
{
    [Required(ErrorMessage = "Customer ID is required")]
    public Guid CustomerId { get; set; }
    
    [Required(ErrorMessage = "At least one item is required")]
    [MinLength(1, ErrorMessage = "At least one item is required")]
    public List<OrderItemDto> Items { get; set; } = new();
    
    [Range(1, 100, ErrorMessage = "Quantity must be between 1 and 100")]
    public int Quantity { get; set; }
    
    [EmailAddress(ErrorMessage = "Invalid email format")]
    public string Email { get; set; } = string.Empty;
    
    [StringLength(500, MinimumLength = 10, ErrorMessage = "Description must be between 10 and 500 characters")]
    public string Description { get; set; } = string.Empty;
}

// FluentValidation alternative
public class CreateOrderRequestValidator : AbstractValidator<CreateOrderRequest>
{
    public CreateOrderRequestValidator()
    {
        RuleFor(x => x.CustomerId)
            .NotEmpty()
            .WithMessage("Customer ID is required");
        
        RuleFor(x => x.Items)
            .NotEmpty()
            .WithMessage("At least one item is required")
            .ForEach(item => item.SetValidator(new OrderItemValidator()));
    }
}
```

#### 2.3 Data Protection

```markdown
□ Sensitive data không được logged
□ Passwords được hashed (not encrypted hoặc plain text)
□ API keys và secrets được stored in secure storage
□ Database connection strings không hardcoded
□ HTTPS enforced in production
□ HSTS headers configured
□ Sensitive headers được stripped when necessary
□ PII data được handled according to privacy requirements
```

**Secure Data Handling**:

```csharp
// ✅ CORRECT: Password hashing
public class PasswordService : IPasswordService
{
    private readonly ILogger<PasswordService> _logger;
    
    public PasswordService(ILogger<PasswordService> logger)
    {
        _logger = logger;
    }
    
    public string HashPassword(string password)
    {
        return BCrypt.Net.BCrypt.HashPassword(password, workFactor: 12);
    }
    
    public bool VerifyPassword(string password, string hash)
    {
        return BCrypt.Net.BCrypt.Verify(password, hash);
    }
}

// ❌ WRONG: Plain text or reversible encryption
// _password = password; // WRONG!
// _password = Encrypt(password); // WRONG!
```

#### 2.4 API Security

```markdown
□ CORS policy được configured appropriately
□ Rate limiting được implemented
□ Request throttling configured for heavy endpoints
□ API versioning strategy implemented
□ Deprecation warnings in place for old versions
□ Sensitive endpoints không exposed in Swagger/OpenAPI
□ Admin endpoints có extra security measures
```

**Rate Limiting Configuration**:

```csharp
builder.Services.AddRateLimiter(options =>
{
    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;
    
    // Global policy
    options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(context =>
        RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: context.Connection.RemoteIpAddress?.ToString() ?? "anonymous",
            factory: _ => new FixedWindowRateLimiterOptions
            {
                PermitLimit = 1000,
                Window = TimeSpan.FromMinutes(1)
            }));
    
    // Endpoint-specific policies
    options.AddPolicy("login", httpContext =>
        RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: httpContext.Connection.RemoteIpAddress?.ToString() ?? "anonymous",
            factory: _ => new FixedWindowRateLimiterOptions
            {
                PermitLimit = 5,
                Window = TimeSpan.FromMinutes(1)
            }));
});

app.UseRateLimiter();
```

### 3. Performance Checklist

#### 3.1 Database Performance

```markdown
□ N+1 query issues đã được resolved
□ AsNoTracking() sử dụng cho read-only queries
□ Proper indexes created for frequently queried columns
□ Query optimization via EXPLAIN/Query Plan analysis
□ Batch operations cho bulk inserts/updates
□ Pagination implemented for large result sets
□ Connection pooling configured appropriately
□ Slow queries được monitored và optimized
```

**Database Performance Checklist**:

```csharp
// ✅ CORRECT: Read-only queries
var products = await _context.Products
    .AsNoTracking()
    .Where(p => p.IsActive)
    .OrderBy(p => p.Name)
    .Skip(offset)
    .Take(pageSize)
    .Select(p => new ProductDto(p.Id, p.Name, p.Price))
    .ToListAsync();

// ❌ WRONG: Tracking for read-only
// var products = await _context.Products
//     .Where(p => p.IsActive)
//     .ToListAsync(); // Tracking unnecessary overhead!

// ✅ CORRECT: Eager loading for related data
var orders = await _context.Orders
    .AsNoTracking()
    .Include(o => o.Customer)
    .Include(o => o.Items)
        .ThenInclude(i => i.Product)
    .Where(o => o.Status == OrderStatus.Pending)
    .ToListAsync();

// ❌ WRONG: N+1 queries
// foreach (var order in orders)
// {
//     var customer = await _context.Customers.FindAsync(order.CustomerId);
//     // N+1 problem!
// }
```

#### 3.2 Caching Strategy

```markdown
□ Response caching configured for appropriate endpoints
□ Output caching implemented for static/variable content
□ Cache invalidation strategy documented và implemented
□ Redis/Distributed cache configured for multi-instance deployments
□ Cache key naming convention established
□ Cache TTLs được set appropriately
□ Memory cache size limits configured
□ Cache hit/miss metrics được collected
```

**Caching Implementation**:

```csharp
// Output caching (ASP.NET Core 7+)
builder.Services.AddOutputCache();

app.UseOutputCache();

app.MapGet("/api/products", async (AppDbContext db) =>
{
    var products = await db.Products
        .AsNoTracking()
        .Where(p => p.IsActive)
        .ToListAsync();
    return Results.Ok(products);
})
.CacheOutput(policy => policy
    .Tag("products")
    .VaryByQueryKeys("category", "page")
    .Expire(TimeSpan.FromMinutes(5)));

// Cache invalidation
app.MapPost("/api/products", async (CreateProductRequest request, AppDbContext db) =>
{
    // Create product...
    await db.SaveChangesAsync();
    
    // Invalidate cache
    app.Services.GetRequiredService<OutputCacheService>().Invalidate("products");
    
    return Results.Created($"/api/products/{product.Id}", product);
}).CacheOutput(policy => policy.Tag("products-create"));
```

#### 3.3 Async/Await Pattern

```markdown
□ All I/O operations sử dụng async/await
□ No blocking calls (.Result, .Wait(), .GetAwaiter().GetResult())
□ Cancellation tokens được passed through call chain
□ Task.WhenAll() sử dụng cho parallel operations
□ async void được avoided (except event handlers)
□ Proper exception handling in async methods
```

**Async Pattern Verification**:

```csharp
// ✅ CORRECT: Full async pipeline
[HttpGet]
public async Task<ActionResult<List<ProductDto>>> GetProducts(
    CancellationToken cancellationToken)
{
    var products = await _productRepository
        .GetAllAsync(cancellationToken);
    return Ok(products);
}

// ❌ WRONG: Blocking calls
// var products = _productRepository.GetAllAsync().Result; // BLOCKS!

// ✅ CORRECT: Parallel operations
public async Task<OrderSummaryDto> GetOrderSummaryAsync(
    Guid orderId, 
    CancellationToken ct)
{
    var orderTask = _orderRepository.GetByIdAsync(orderId, ct);
    var statsTask = _orderRepository.GetStatsAsync(orderId, ct);
    var historyTask = _orderRepository.GetHistoryAsync(orderId, ct);
    
    await Task.WhenAll(orderTask, statsTask, historyTask);
    
    return new OrderSummaryDto
    {
        Order = await orderTask,
        Stats = await statsTask,
        History = await historyTask
    };
}

// ❌ WRONG: Sequential when parallel is possible
// var order = await _orderRepository.GetByIdAsync(orderId, ct);
// var stats = await _orderRepository.GetStatsAsync(orderId, ct);
// var history = await _orderRepository.GetHistoryAsync(orderId, ct);
```

### 4. Error Handling và Logging

#### 4.1 Exception Handling

```markdown
□ Global exception handler middleware configured
□ Custom exception types for business errors
□ Structured error responses consistent across API
□ Sensitive information không exposed in error messages
□ Stack traces không returned in production
□ Unhandled exceptions được logged with full context
□ Client-friendly error messages provided
```

**Exception Handling Setup**:

```csharp
// Global exception handler
public class GlobalExceptionHandler : IExceptionHandler
{
    private readonly ILogger<GlobalExceptionHandler> _logger;
    private readonly IHostEnvironment environment;
    
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
        
        var (statusCode, response) = exception switch
        {
            ValidationException ve => (StatusCodes.Status400BadRequest, new ErrorResponse
            {
                Type = "ValidationError",
                Title = "Validation failed",
                Errors = ve.Errors
            }),
            NotFoundException nf => (StatusCodes.Status404NotFound, new ErrorResponse
            {
                Type = "NotFound",
                Title = nf.Message
            }),
            UnauthorizedException ue => (StatusCodes.Status401Unauthorized, new ErrorResponse
            {
                Type = "Unauthorized",
                Title = ue.Message
            }),
            ForbiddenException fe => (StatusCodes.Status403Forbidden, new ErrorResponse
            {
                Type = "Forbidden",
                Title = fe.Message
            }),
            _ => (StatusCodes.Status500InternalServerError, new ErrorResponse
            {
                Type = "InternalServerError",
                Title = environment.IsDevelopment() 
                    ? exception.Message 
                    : "An unexpected error occurred"
            })
        };
        
        _logger.LogError(exception, 
            "Unhandled exception. CorrelationId: {CorrelationId}", 
            correlationId);
        
        httpContext.Response.StatusCode = statusCode;
        await httpContext.Response.WriteAsJsonAsync(response, cancellationToken);
        
        return true;
    }
}
```

#### 4.2 Structured Logging

```markdown
□ All services sử dụng ILogger<T> (not ILoggerFactory)
□ Log levels được used appropriately (Trace, Debug, Info, Warning, Error, Critical)
□ Sensitive data được sanitized in logs
□ Correlation IDs được propagated across requests
□ Performance metrics logged for slow operations
□ Business events logged for audit trail
□ Configuration changes logged
□ Failed authentication attempts logged
```

**Logging Best Practices**:

```csharp
// ✅ CORRECT: Structured logging
_logger.LogInformation(
    "Order {OrderId} created for customer {CustomerId} with {ItemCount} items",
    order.Id,
    order.CustomerId,
    order.Items.Count);

_logger.LogWarning(
    "Order {OrderId} processing time exceeded threshold: {ProcessingTime}ms",
    order.Id,
    processingTime);

_logger.LogError(ex,
    "Failed to process order {OrderId}. Customer: {CustomerId}, Items: {ItemCount}",
    order.Id,
    order.CustomerId,
    order.Items.Count);

// ❌ WRONG: String interpolation in logs
// _logger.LogInformation($"Order {order.Id} created"); // Can't search/filter!
```

### 5. Testing Requirements

#### 5.1 Unit Tests

```markdown
□ All business logic có unit tests
□ Edge cases được covered
□ Happy path và error paths được tested
□ Mocking done correctly (not mocking concrete classes unnecessarily)
□ Test names descriptive và consistent
□ Tests follow Arrange-Act-Assert pattern
□ Tests are independent (no shared state)
□ Code coverage đạt minimum threshold (e.g., 80%)
□ Tests run fast (no external dependencies)
```

**Unit Test Example**:

```csharp
[Fact]
public async Task CreateOrder_WithValidItems_ShouldCreateOrderSuccessfully()
{
    // Arrange
    var command = new CreateOrderCommand
    {
        CustomerId = Guid.NewGuid(),
        Items = new List<CreateOrderItemDto>
        {
            new() { ProductId = Guid.NewGuid(), Quantity = 2 },
            new() { ProductId = Guid.NewGuid(), Quantity = 1 }
        }
    };
    
    var products = new List<Product>
    {
        Product.Create("Product 1", Money.FromDecimal(10m)),
        Product.Create("Product 2", Money.FromDecimal(20m))
    };
    
    _productRepository
        .Setup(x => x.GetByIdsAsync(It.IsAny<IEnumerable<Guid>>(), It.IsAny<CancellationToken>()))
        .ReturnsAsync(products);
    
    _orderRepository
        .Setup(x => x.AddAsync(It.IsAny<Order>(), It.IsAny<CancellationToken>()))
        .Returns(Task.CompletedTask);
    
    _unitOfWork
        .Setup(x => x.SaveChangesAsync(It.IsAny<CancellationToken>()))
        .ReturnsAsync(1);
    
    // Act
    var result = await _sut.CreateOrderAsync(command, CancellationToken.None);
    
    // Assert
    result.IsSuccess.Should().BeTrue();
    result.Value.Should().NotBeNull();
    result.Value!.Items.Should().HaveCount(2);
    
    _orderRepository.Verify(
        x => x.AddAsync(It.IsAny<Order>(), It.IsAny<CancellationToken>()), 
        Times.Once);
}
```

#### 5.2 Integration Tests

```markdown
□ API endpoints có integration tests
□ Database operations được tested against real database (or test container)
□ Authentication/Authorization được tested
□ Health checks được tested
□ External service mocks configured correctly
□ Test data cleanup between tests
□ Parallel test execution supported
```

**Integration Test Example**:

```csharp
public class OrdersControllerIntegrationTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;
    private readonly HttpClient _client;
    private readonly string _authToken;
    
    public OrdersControllerIntegrationTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                // Use test database
                services.RemoveAll(typeof(DbContextOptions<ApplicationDbContext>));
                services.AddDbContext<ApplicationDbContext>(options =>
                    options.UseInMemoryDatabase("IntegrationTestDb"));
                
                // Mock external services
                services.RemoveAll(typeof(IEmailService));
                services.AddScoped<IEmailService, MockEmailService>();
            });
        });
        
        _client = _factory.CreateClient();
        _authToken = GenerateTestToken();
    }
    
    [Fact]
    public async Task CreateOrder_WithValidRequest_ShouldReturn201()
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
        var response = await _client
            .WithBearerToken(_authToken)
            .PostAsJsonAsync("/api/v1/orders", request);
        
        // Assert
        response.StatusCode.Should().Be(StatusCodes.Status201Created);
        
        var createdOrder = await response.Content.ReadFromJsonAsync<OrderDto>();
        createdOrder.Should().NotBeNull();
        createdOrder!.Id.Should().NotBeEmpty();
    }
    
    [Fact]
    public async Task GetOrders_WithoutAuth_ShouldReturn401()
    {
        // Act
        var response = await _client.GetAsync("/api/v1/orders");
        
        // Assert
        response.StatusCode.Should().Be(StatusCodes.Status401Unauthorized);
    }
}
```

### 6. Health và Monitoring

#### 6.1 Health Checks

```markdown
□ Basic liveness endpoint configured
□ Readiness checks for dependencies (database, cache, external services)
□ Health check response có meaningful data
□ Health checks don't cause side effects
□ Kubernetes-style /health/live và /health/ready endpoints
□ Health check status codes appropriate (200 vs 503)
```

**Health Check Implementation**:

```csharp
builder.Services.AddHealthChecks()
    .AddDbContextCheck<ApplicationDbContext>("database")
    .AddRedis(builder.Configuration.GetConnectionString("Redis"), "cache")
    .AddUrlGroup(new Uri("https://api.example.com/health"), "external-api")
    .AddCheck<CustomBusinessHealthCheck>("business-rules");

app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false // Simple liveness
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready"),
    ResponseWriter = async (context, report) =>
    {
        context.Response.ContentType = "application/json";
        await context.Response.WriteAsJsonAsync(new
        {
            status = report.Status.ToString(),
            checks = report.Entries.Select(e => new
            {
                name = e.Key,
                status = e.Value.Status.ToString(),
                duration = e.Value.Duration.TotalMilliseconds
            })
        });
    }
});
```

#### 6.2 Observability

```markdown
□ Logging configured với appropriate providers
□ Metrics collection enabled (Application Insights, Prometheus, etc.)
□ Distributed tracing configured for microservices
□ Request/response logging (sanitized) for debugging
□ Performance counters enabled
□ Custom metrics for business KPIs
□ Alerting rules configured
□ Dashboards created for monitoring
```

### 7. Deployment Readiness

#### 7.1 Build và Release

```markdown
□ Build configuration chính xác (Release mode)
□ Self-contained deployment option considered
□ Trimming/publishing ready for AOT
□ Version information embedded in assembly
□ Build artifacts được signed (if required)
□ Deployment package size optimized
□ Zero-downtime deployment strategy
□ Rollback plan documented
```

**Build Commands**:

```bash
# Release build
dotnet build -c Release

# Self-contained deployment
dotnet publish -c Release -r linux-x64 --self-contained true

# Single file executable
dotnet publish -c Release -r linux-x64 --self-contained true /p:PublishSingleFile=true

# Trimming for smaller size
dotnet publish -c Release /p:PublishTrimmed=true /p:TrimMode=link
```

#### 7.2 Environment Configuration

```markdown
□ Production environment variable documented
□ Connection strings chính xác cho production
□ Feature flags configured appropriately
□ CDN configuration nếu sử dụng
□ Load balancer health check configuration
□ DNS configuration verified
□ SSL/TLS certificates valid và configured
□ Database migration scripts tested
```

#### 7.3 Documentation

```markdown
□ API documentation (OpenAPI/Swagger) complete
□ Deployment guide documented
□ Runbook cho common operations created
□ Troubleshooting guide available
□ Architecture diagram updated
□ Dependencies documented
□ Security considerations documented
□ Contact information for support
```

### 8. Code Quality Standards

#### 8.1 Code Style

```markdown
□ .editorconfig file configured và enforced
□ Consistent naming conventions (PascalCase, camelCase)
□ File organization follows project conventions
□ No magic numbers (use constants)
□ Meaningful variable/function names
□ No commented-out code (use version control)
□ Dead code removed
□ Redundant code eliminated
```

**.editorconfig Example**:

```ini
root = true

[*.cs]
indent_style = space
indent_size = 4
end_of_line = crlf
charset = utf-8-bom
trim_trailing_whitespace = true
insert_final_newline = true

dotnet_naming_rule.interface_should_be_begins_with_i.severity = warning
dotnet_naming_rule.interface_should_be_begins_with_i.symbols = interface
dotnet_naming_rule.interface_should_be_begins_with_i.style = begins_with_i

dotnet_naming_symbols.interface.applicable_kinds = interface
dotnet_naming_style.begins_with_i.required_prefix = I
dotnet_naming_style.begins_with_i.capitalization = pascal_case

csharp_indent_case_contents = true
csharp_new_line_before_open_brace = all
```

#### 8.2 Architecture Compliance

```markdown
□ Project structure follows established pattern
□ Dependency direction correct (Domain → Application → Infrastructure → API)
□ No circular dependencies
□ Business logic không in controllers
□ Data access abstracted via repositories
□ External services abstracted via interfaces
□ Cross-cutting concerns handled via middleware/filters
```

### 9. Database Checklist

```markdown
□ Migrations generated và tested
□ Data seeding scripts documented
□ Index strategy implemented
□ Foreign key constraints enforced
□ Soft delete pattern (nếu sử dụng) consistent
□ Audit fields (CreatedAt, UpdatedAt) implemented
□ Migration rollback tested
□ Backup/restore procedures documented
□ Database performance baseline established
```

### 10. Final Pre-Deployment Verification

```markdown
□ All unit tests passing
□ All integration tests passing
□ Code coverage meets threshold
□ Security scan completed
□ Performance test passed
□ Load test completed
□ UAT signed off
□ Change request approved
□ Rollback plan tested
□ Communication plan in place
□ Monitoring dashboards verified
□ Alerts configured và tested
□ On-call team notified
□ Deployment window scheduled
```

## Quick Reference Checklist

### Pre-Commit Checklist

- [ ] Code compiles without errors
- [ ] All tests passing locally
- [ ] No new compiler warnings
- [ ] Code follows style guidelines
- [ ] No secrets committed
- [ ] Appropriate log levels used
- [ ] Cancellation tokens passed

### Pre-Merge Checklist

- [ ] Code review approved
- [ ] All CI checks passing
- [ ] Documentation updated
- [ ] Breaking changes communicated
- [ ] Feature flags configured
- [ ] Migration scripts reviewed

### Pre-Deploy Checklist

- [ ] Environment variables verified
- [ ] Connection strings correct
- [ ] SSL certificates valid
- [ ] Health checks responding
- [ ] Monitoring dashboards active
- [ ] Rollback plan ready
- [ ] Communication sent
- [ ] On-call coverage arranged

## References

- [ASP.NET Core Security Best Practices](https://docs.microsoft.com/aspnet/core/security/)
- [ASP.NET Core Performance Best Practices](https://docs.microsoft.com/aspnet/core/performance/)
- [Entity Framework Core Performance](https://docs.microsoft.com/ef/core/performance/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Health Checks in ASP.NET Core](https://docs.microsoft.com/aspnet/core/host-and-deploy/health-checks)
