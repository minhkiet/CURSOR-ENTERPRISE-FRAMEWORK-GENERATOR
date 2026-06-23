# ASP.NET Core FAQ - Câu Hỏi Thường Gặp

## Mục lục
1. [General](#1-general)
2. [Controllers](#2-controllers)
3. [Entity Framework](#3-entity-framework)
4. [Authentication](#4-authentication)
5. [Performance](#5-performance)

---

## 1. General

### Q1: Sự khác nhau giữa AddSingleton, AddScoped, và AddTransient?

**A:**

| Lifetime | When Created | When Disposed | Use Case |
|----------|-------------|--------------|----------|
| Singleton | First request | Application shutdown | Configuration, logging |
| Scoped | Each HTTP request | End of HTTP request | DbContext, services per request |
| Transient | Each injection | When disposed | Lightweight, stateless services |

```csharp
// Singleton - one instance for entire app
builder.Services.AddSingleton<ISettings, Settings>();

// Scoped - one instance per request
builder.Services.AddScoped<IUserService, UserService>();

// Transient - new instance each time
builder.Services.AddTransient<IEmailService, EmailService>();
```

---

### Q2: Làm thế nào để configure logging?

**A:**

```csharp
// Program.cs
builder.Services.AddLogging(options =>
{
    options.AddConsole();
    options.AddDebug();
    
    options.AddFilter("Microsoft", LogLevel.Warning);
    options.AddFilter("System", LogLevel.Warning);
    options.AddFilter("Default", LogLevel.Information);
});

//appsettings.json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  }
}

// Usage in service
public class UserService : IUserService
{
    private readonly ILogger<UserService> _logger;
    
    public UserService(ILogger<UserService> logger)
    {
        _logger = logger;
    }
    
    public async Task<User> GetByIdAsync(int id)
    {
        _logger.LogInformation("Getting user {UserId}", id);
        // ...
    }
}
```

---

## 2. Controllers

### Q3: Làm thế nào để return 404 khi resource không tồn tại?

**A:**

```csharp
[HttpGet("{id}")]
public async Task<ActionResult<UserDto>> GetById(int id)
{
    var user = await _userService.GetByIdAsync(id);
    
    if (user == null)
        return NotFound(); // Returns 404
        
    return Ok(user); // Returns 200
}

// With automatic model binding
[HttpGet("{id}")]
public async Task<ActionResult<UserDto>> GetById(User user)
{
    if (user == null)
        return NotFound();
        
    return Ok(user);
}
```

---

### Q4: Sự khác nhau giữa BadRequest, NotFound, và StatusCode?

**A:**

| Method | HTTP Status | Use Case |
|--------|-------------|----------|
| `Ok()` | 200 | Successful GET |
| `CreatedAtAction()` | 201 | Resource created |
| `NoContent()` | 204 | Successful DELETE/PUT |
| `BadRequest()` | 400 | Invalid input |
| `Unauthorized()` | 401 | Not authenticated |
| `Forbid()` | 403 | Authenticated but not authorized |
| `NotFound()` | 404 | Resource not found |
| `StatusCode(500)` | 500 | Server error |

```csharp
// 400 Bad Request
return BadRequest("Invalid input");
return BadRequest(ModelState);

// 404 Not Found
return NotFound();
return NotFound(new { message = "User not found" });

// Custom status
return StatusCode(418, "I'm a teapot");
```

---

## 3. Entity Framework

### Q5: Làm thế nào để eager load multiple levels?

**A:**

```csharp
// Multiple levels with ThenInclude
var orders = await _context.Orders
    .Include(o => o.Customer)
        .ThenInclude(c => c.Address)
    .Include(o => o.OrderItems)
        .ThenInclude(i => i.Product)
            .ThenInclude(p => p.Category)
    .Where(o => o.Status == "Pending")
    .ToListAsync();

// Collection projection alternative
var orders = await _context.Orders
    .Select(o => new 
    {
        o.Id,
        o.Total,
        CustomerName = o.Customer.Name,
        ItemCount = o.OrderItems.Count()
    })
    .ToListAsync();
```

---

### Q6: Làm thế nào để use global filters?

**A:**

```csharp
// In DbContext
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    // Global filter for soft deletes
    modelBuilder.Entity<User>()
        .HasQueryFilter(u => !u.IsDeleted);
        
    // Global filter for tenant
    modelBuilder.Entity<Order>()
        .HasQueryFilter(o => o.TenantId == _currentTenantId);
}

// Disable filter when needed
var users = await _context.Users
    .IgnoreQueryFilters()
    .ToListAsync();
```

---

### Q7: Transaction với EF Core?

**A:**

```csharp
// Simple transaction
await using var transaction = await _context.Database.BeginTransactionAsync();

try
{
    _context.Orders.Add(order);
    await _context.SaveChangesAsync();
    
    _context.OrderItems.AddRange(items);
    await _context.SaveChangesAsync();
    
    await transaction.CommitAsync();
}
catch
{
    await transaction.RollbackAsync();
    throw;
}

// Transaction with isolation level
await using var transaction = await _context.Database.BeginTransactionAsync(
    IsolationLevel.Serializable);
    
// Or use_execute_sql
await _context.Database.ExecuteSqlRawAsync(
    "EXEC UpdateInventory @p0, @p1", parameters);
```

---

## 4. Authentication

### Q8: Làm thế nào để implement JWT authentication?

**A:**

```csharp
// Program.cs
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
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
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]))
        };
    });

// Token generation service
public class TokenService : ITokenService
{
    public string GenerateToken(User user)
    {
        var claims = new[]
        {
            new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
            new Claim(ClaimTypes.Email, user.Email),
            new Claim(ClaimTypes.Role, user.Role)
        };
        
        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_config["Jwt:Key"]));
        var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
        
        var token = new JwtSecurityToken(
            issuer: _config["Jwt:Issuer"],
            audience: _config["Jwt:Audience"],
            claims: claims,
            expires: DateTime.UtcNow.AddHours(1),
            signingCredentials: credentials
        );
        
        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
```

---

### Q9: Policy-based authorization?

**A:**

```csharp
// Program.cs
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AdminOnly", policy => 
        policy.RequireRole("Admin"));
        
    options.AddPolicy("MinimumAge", policy =>
        policy.Requirements.Add(new MinimumAgeRequirement(18)));
});

// Custom requirement
public class MinimumAgeRequirement : IAuthorizationRequirement
{
    public int MinimumAge { get; }
    
    public MinimumAgeRequirement(int minimumAge)
    {
        MinimumAge = minimumAge;
    }
}

public class MinimumAgeHandler : AuthorizationHandler<MinimumAgeRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        MinimumAgeRequirement requirement)
    {
        var birthDate = context.User.FindFirst("BirthDate");
        
        if (birthDate != null && 
            DateTime.Parse(birthDate.Value).AddYears(requirement.MinimumAge) <= DateTime.Today)
        {
            context.Succeed(requirement);
        }
        
        return Task.CompletedTask;
    }
}

// Controller usage
[HttpGet]
[Authorize(Policy = "AdminOnly")]
public IActionResult AdminOnly() { }

[HttpGet]
[Authorize(Policy = "MinimumAge")]
public IActionResult AgeRestricted() { }
```

---

## 5. Performance

### Q10: Response caching?

**A:**

```csharp
// Program.cs
builder.Services.AddResponseCaching();

var app = builder.Build();

app.UseResponseCaching();

// Controller
[HttpGet]
[ResponseCache(Duration = 60, Location = ResponseCacheLocation.Any)]
public async Task<IActionResult> GetProducts()
{
    return Ok(await _productService.GetAllAsync());
}

// Cache profiles
builder.Services.AddControllers(options =>
{
    options.CacheProfiles.Add("ProductCache", new CacheProfile
    {
        Duration = 300,
        Location = ResponseCacheLocation.Any
    });
});

[HttpGet("{id}")]
[ResponseCache(CacheProfileName = "ProductCache")]
public async Task<IActionResult> GetProduct(int id) { }
```

---

### Q11: Output caching (.NET 7+)?

**A:**

```csharp
// Program.cs
builder.Services.AddOutputCache();

var app = builder.Build();

app.UseOutputCache();

// Basic caching
app.MapGet("/products", async (AppDbContext db) =>
{
    var products = await db.Products.ToListAsync();
    return Results.Ok(products);
}).CacheOutput(policy => policy.Expire(TimeSpan.FromMinutes(5)));

// Vary by headers
app.MapGet("/products/{category}", async (string category, AppDbContext db) =>
{
    var products = await db.Products
        .Where(p => p.Category == category)
        .ToListAsync();
    return Results.Ok(products);
}).CacheOutput(policy => policy
    .VaryByHeader("Accept-Language")
    .Expire(TimeSpan.FromMinutes(5)));

// Tags for invalidation
app.MapGet("/products", async (AppDbContext db) =>
{
    // ...
}).CacheOutput(policy => policy
    .Tag("products")
    .Expire(TimeSpan.FromMinutes(5)));
```

---

### Q12: Health checks?

**A:**

```csharp
// Program.cs
builder.Services.AddHealthChecks()
    .AddDbContextCheck<ApplicationDbContext>("database")
    .AddRedis(builder.Configuration.GetConnectionString("Redis"))
    .AddCheck("external", () => 
    {
        // Custom health check
        return HealthCheckResult.Healthy();
    });

var app = builder.Build();

app.MapHealthChecks("/health", new Microsoft.AspNetCore.Diagnostics.HealthChecks.HealthCheckOptions
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
                status = e.Value.Status.ToString(),
                description = e.Value.Description
            })
        });
    }
});
```

---

## Liên kết liên quan
- [ASP.NET Core Glossary](./glossary.md)
- [ASP.NET Core Architecture](./architecture.md)
- [ASP.NET Core Best Practices](./best-practice.md)
- [ASP.NET Core Anti-Patterns](./anti-pattern.md)
- [ASP.NET Core Checklist](./checklist.md)
- [ASP.NET Core Decision Tree](./decision-tree.md)
