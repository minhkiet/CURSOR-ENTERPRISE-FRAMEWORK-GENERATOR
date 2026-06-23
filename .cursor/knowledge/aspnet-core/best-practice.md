# ASP.NET Core Best Practices - Các Thực Hành Tốt Nhất

## Mục lục
1. [Controller Best Practices](#1-controller-best-practices)
2. [Dependency Injection Best Practices](#2-dependency-injection-best-practices)
3. [Entity Framework Best Practices](#3-entity-framework-best-practices)
4. [Security Best Practices](#4-security-best-practices)
5. [Performance Best Practices](#5-performance-best-practices)
6. [API Best Practices](#6-api-best-practices)

---

## 1. Controller Best Practices

### 1.1 Keep Controllers Thin

**Mô tả**: Controllers chỉ nên xử lý HTTP concerns. Business logic nên được đặt trong Services.

**Ví dụ**:
```csharp
// ❌ BAD: Fat controller with business logic
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    public async Task<ActionResult<UserDto>> Create(CreateUserRequest request)
    {
        // Validation inline
        if (string.IsNullOrEmpty(request.Name))
            return BadRequest("Name is required");
            
        // Business logic inline
        var existingUser = await _context.Users
            .FirstOrDefaultAsync(u => u.Email == request.Email);
            
        if (existingUser != null)
            return BadRequest("Email already exists");
            
        // Data access inline
        var user = new User { Name = request.Name, Email = request.Email };
        _context.Users.Add(user);
        await _context.SaveChangesAsync();
        
        return Ok(user);
    }
}

// ✅ GOOD: Thin controller
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;
    
    public UsersController(IUserService userService)
    {
        _userService = userService;
    }
    
    public async Task<ActionResult<UserDto>> Create(CreateUserRequest request)
    {
        var user = await _userService.CreateUserAsync(request);
        return CreatedAtAction(nameof(GetById), new { id = user.Id }, user);
    }
}
```

**Khi nào áp dụng**: Mọi controllers.

### 1.2 Use ActionResult<T>

**Mô tả**: Sử dụng ActionResult<T> để return strongly-typed responses.

**Ví dụ**:
```csharp
// ✅ GOOD: ActionResult<T>
[HttpGet("{id}")]
public async Task<ActionResult<UserDto>> GetById(int id)
{
    var user = await _userService.GetByIdAsync(id);
    
    if (user == null)
        return NotFound();
        
    return Ok(user);
}

// ✅ GOOD: For POST with 201 Created
[HttpPost]
public async Task<ActionResult<UserDto>> Create(CreateUserRequest request)
{
    var user = await _userService.CreateAsync(request);
    return CreatedAtAction(nameof(GetById), new { id = user.Id }, user);
}
```

**Khi nào áp dụng**: API controllers.

### 1.3 Use Dependency Injection Properly

**Mô tả**: Inject dependencies qua constructor.

**Ví dụ**:
```csharp
// ✅ GOOD: Constructor injection
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;
    private readonly ILogger<UsersController> _logger;
    
    public UsersController(
        IUserService userService,
        ILogger<UsersController> logger)
    {
        _userService = userService;
        _logger = logger;
    }
}
```

**Khi nào áp dụng**: Mọi controllers.

---

## 2. Dependency Injection Best Practices

### 2.1 Use Interface-Based Injection

**Mô tả**: Inject interfaces thay vì concrete classes để improve testability.

**Ví dụ**:
```csharp
// ✅ GOOD: Interface-based DI
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddScoped<IEmailService, EmailService>();
builder.Services.AddSingleton<ISettings, Settings>();

// Controller
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;
    
    public UsersController(IUserService userService)
    {
        _userService = userService;
    }
}
```

**Khi nào áp dụng**: Services cần test được.

### 2.2 Register Services Correctly

**Mô tả**: Chọn đúng service lifetime phù hợp với use case.

| Lifetime | Use Case |
|----------|----------|
| Singleton | Configuration, logging |
| Scoped | Database context, services per request |
| Transient | Lightweight, stateless services |

```csharp
builder.Services.AddSingleton<ISettings, Settings>();      // One instance
builder.Services.AddScoped<IUserService, UserService>();   // Per request
builder.Services.AddTransient<IEmailService, EmailService>(); // Each injection
```

**Khi nào áp dụng**: Mọi service registrations.

### 2.3 Avoid Service Locator Pattern

**Mô tả**: Không sử dụng IServiceProvider.GetService() trong code.

**Ví dụ**:
```csharp
// ❌ BAD: Service locator
public class BadService
{
    private readonly IServiceProvider _serviceProvider;
    
    public BadService(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }
    
    public async Task DoSomething()
    {
        var emailService = _serviceProvider.GetService<IEmailService>();
        // ...
    }
}

// ✅ GOOD: Direct injection
public class GoodService
{
    private readonly IEmailService _emailService;
    
    public GoodService(IEmailService emailService)
    {
        _emailService = emailService;
    }
}
```

**Khi nào áp dụng**: Mọi services.

---

## 3. Entity Framework Best Practices

### 3.1 Use AsNoTracking for Read-Only Queries

**Mô tả**: Sử dụng AsNoTracking() để improve performance cho read-only queries.

**Ví dụ**:
```csharp
// ✅ GOOD: AsNoTracking for read-only
public async Task<IEnumerable<User>> GetAllUsersAsync()
{
    return await _context.Users
        .AsNoTracking()
        .Where(u => u.IsActive)
        .OrderBy(u => u.Name)
        .ToListAsync();
}

// ✅ GOOD: AsNoTrackingWithIdentityResolution when needed
public async Task<IEnumerable<User>> GetUsersWithPostsAsync()
{
    return await _context.Users
        .AsNoTrackingWithIdentityResolution()
        .Include(u => u.Posts)
        .ToListAsync();
}
```

**Khi nào áp dụng**: Read-only queries.

### 3.2 Use Projections to Limit Data

**Mô tả**: Select chỉ columns cần thiết thay vì fetch entire entities.

**Ví dụ**:
```csharp
// ❌ BAD: Fetch entire entity
var users = await _context.Users.ToListAsync();
var names = users.Select(u => u.Name).ToList();

// ✅ GOOD: Projection
var names = await _context.Users
    .Select(u => u.Name)
    .ToListAsync();

// ✅ GOOD: DTO projection
var userDtos = await _context.Users
    .Select(u => new UserDto
    {
        Id = u.Id,
        Name = u.Name,
        Email = u.Email
    })
    .ToListAsync();
```

**Khi nào áp dụng**: Mọi queries.

### 3.3 Use Async Properly

**Mô tả**: Sử dụng async/await cho database operations để không block threads.

**Ví dụ**:
```csharp
// ✅ GOOD: Async throughout
public async Task<IEnumerable<User>> GetUsersAsync()
{
    return await _context.Users
        .AsNoTracking()
        .Where(u => u.IsActive)
        .ToListAsync();
}

// ✅ GOOD: Async with cancellation
public async Task<IEnumerable<User>> GetUsersAsync(
    CancellationToken cancellationToken = default)
{
    return await _context.Users
        .AsNoTracking()
        .Where(u => u.IsActive)
        .ToListAsync(cancellationToken);
}
```

**Khi nào áp dụng**: Mọi database operations.

---

## 4. Security Best Practices

### 4.1 Validate Input with Data Annotations

**Mô tả**: Sử dụng validation attributes để ensure data integrity.

**Ví dụ**:
```csharp
public class CreateUserRequest
{
    [Required(ErrorMessage = "Tên là bắt buộc")]
    [StringLength(100, MinimumLength = 2)]
    public string Name { get; set; }
    
    [Required]
    [EmailAddress(ErrorMessage = "Email không hợp lệ")]
    public string Email { get; set; }
    
    [Required]
    [MinLength(8, ErrorMessage = "Mật khẩu phải có ít nhất 8 ký tự")]
    public string Password { get; set; }
}

// Controller with automatic validation
public async Task<ActionResult<UserDto>> Create(
    [FromBody][Required] CreateUserRequest request)
{
    // ModelState is automatically validated
    var user = await _userService.CreateAsync(request);
    return CreatedAtAction(nameof(GetById), new { id = user.Id }, user);
}
```

**Khi nào áp dụng**: Mọi user input.

### 4.2 Use Parameterized Queries

**Mô tả**: Luôn sử dụng parameterized queries để prevent SQL injection.

**Ví dụ**:
```csharp
// ✅ GOOD: Parameterized (via EF Core)
var users = await _context.Users
    .Where(u => u.Email == email)
    .FirstOrDefaultAsync();

// ✅ GOOD: Raw SQL with parameters
var user = await _context.Users
    .FromSqlRaw("SELECT * FROM Users WHERE Email = {0}", email)
    .FirstOrDefaultAsync();

// ❌ BAD: String interpolation
var user = await _context.Users
    .FromSqlRaw($"SELECT * FROM Users WHERE Email = '{email}'")
    .FirstOrDefaultAsync();
```

**Khi nào áp dụng**: Raw SQL queries.

### 4.3 Implement Rate Limiting

**Mô tả**: Implement rate limiting để prevent abuse.

**Ví dụ**:
```csharp
// Program.cs
builder.Services.AddRateLimiter(options =>
{
    options.RejectionStatusCode = StatusCodes.TooManyRequests;
    
    options.AddFixedWindowLimiter("fixed", limiterOptions =>
    {
        limiterOptions.PermitLimit = 100;
        limiterOptions.Window = TimeSpan.FromMinutes(1);
    });
    
    options.OnRejected = async (context, cancellationToken) =>
    {
        context.HttpContext.Response.StatusCode = 429;
        await context.HttpContext.Response.WriteAsJsonAsync(
            new { error = "Too many requests. Please try again later." });
    };
});

// Controller
[HttpGet]
[EnableRateLimiting("fixed")]
public async Task<IActionResult> GetAll() { }
```

**Khi nào áp dụng**: Public API endpoints.

---

## 5. Performance Best Practices

### 5.1 Use Response Caching

**Mô tả**: Cache responses để reduce server load và improve response times.

**Ví dụ**:
```csharp
// Program.cs
builder.Services.AddResponseCaching();

// Controller
[HttpGet]
[ResponseCache(Duration = 60, Location = ResponseCacheLocation.Any)]
public async Task<IActionResult> GetProducts()
{
    return Ok(await _productService.GetAllAsync());
}

// For specific endpoints
[HttpGet("{id}")]
[ResponseCache(Duration = 3600, VaryByQueryKeys = new[] { "id" })]
public async Task<IActionResult> GetProduct(int id) { }
```

**Khi nào áp dụng**: Endpoints với infrequently changing data.

### 5.2 Use Pagination

**Mô tả**: Always paginate large result sets.

**Ví dụ**:
```csharp
public async Task<ActionResult<PagedResult<UserDto>>> GetUsers(
    [FromQuery] int page = 1,
    [FromQuery] int pageSize = 20)
{
    pageSize = Math.Min(pageSize, 100); // Cap at 100
    
    var totalCount = await _context.Users.CountAsync();
    var users = await _context.Users
        .AsNoTracking()
        .OrderBy(u => u.Name)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .Select(u => new UserDto { Id = u.Id, Name = u.Name })
        .ToListAsync();
        
    return Ok(new PagedResult<UserDto>
    {
        Items = users,
        Page = page,
        PageSize = pageSize,
        TotalCount = totalCount,
        TotalPages = (int)Math.Ceiling(totalCount / (double)pageSize)
    });
}
```

**Khi nào áp dụng**: List endpoints.

### 5.3 Use Output Caching

**Mô tả**: Sử dụng output caching cho improved performance.

**Ví dụ**:
```csharp
// Program.cs
builder.Services.AddOutputCache();

var app = builder.Build();

app.UseOutputCache();

// Cache endpoint
app.MapGet("/products", async (AppDbContext db) =>
{
    var products = await db.Products
        .AsNoTracking()
        .ToListAsync();
    return Results.Ok(products);
}).CacheOutput(policy => policy.Expire(TimeSpan.FromMinutes(5)));
```

**Khi nào áp dụng**: Read-heavy endpoints.

---

## 6. API Best Practices

### 6.1 Use API versioning

**Mô tả**: Version APIs để maintain backwards compatibility.

**Ví dụ**:
```csharp
// Program.cs
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
});

// Controller
[ApiVersion("1.0")]
[ApiController]
[Route("api/v{version:apiVersion}/[controller]")]
public class UsersController : ControllerBase { }

// v2 Controller
[ApiVersion("2.0")]
public class UsersV2Controller : UsersController { }
```

**Khi nào áp dụng**: Public APIs.

### 6.2 Return Consistent Error Responses

**Mô tả**: Return consistent error format across API.

**Ví dụ**:
```csharp
public class ErrorResponse
{
    public string Message { get; set; }
    public string Code { get; set; }
    public Dictionary<string, string[]> Errors { get; set; }
    public DateTime Timestamp { get; set; }
}

// Exception filter
public class ValidationExceptionFilter : IExceptionFilter
{
    public void OnException(ExceptionContext context)
    {
        if (context.Exception is ValidationException ex)
        {
            context.Result = new BadRequestObjectResult(new ErrorResponse
            {
                Message = "Validation failed",
                Code = "VALIDATION_ERROR",
                Errors = ex.Errors,
                Timestamp = DateTime.UtcNow
            });
        }
    }
}
```

**Khi nào áp dụng**: Mọi API responses.

### 6.3 Use OpenAPI/Swagger

**Mô tả**: Document API với OpenAPI specification.

**Ví dụ**:
```csharp
// Program.cs
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "My API",
        Version = "v1",
        Description = "API Documentation"
    });
});

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI(options =>
{
    options.SwaggerEndpoint("/swagger/v1/swagger.json", "My API v1");
});
```

**Khi nào áp dụng**: Mọi APIs.

---

## Liên kết liên quan
- [ASP.NET Core Glossary](./glossary.md)
- [ASP.NET Core Architecture](./architecture.md)
- [ASP.NET Core Anti-Patterns](./anti-pattern.md)
- [ASP.NET Core Checklist](./checklist.md)
- [ASP.NET Core FAQ](./faq.md)
- [ASP.NET Core Decision Tree](./decision-tree.md)
