# ASP.NET Core Glossary - Thuật Ngữ Chuyên Ngành

## Mục lục
1. [Middleware](#1-middleware)
2. [Controllers](#2-controllers)
3. [Dependency Injection](#3-dependency-injection)
4. [Entity Framework Core](#4-entity-framework-core)
5. [Routing](#5-routing)
6. [Configuration](#6-configuration)
7. [Authentication](#7-authentication)

---

## Middleware

**Định nghĩa**: Middleware là software components được đặt trong request pipeline. Mỗi component chọn có forward request đến next component hoặc short-circuit the pipeline.

**Ví dụ**:
```csharp
// Custom middleware
public class RequestTimingMiddleware
{
    private readonly RequestDelegate _next;
    
    public RequestTimingMiddleware(RequestDelegate next)
    {
        _next = next;
    }
    
    public async Task InvokeAsync(HttpContext context)
    {
        var stopwatch = Stopwatch.StartNew();
        
        await _next(context);
        
        stopwatch.Stop();
        context.Response.Headers["X-Request-Time"] = stopwatch.ElapsedMilliseconds.ToString();
    }
}

// Register middleware
app.UseMiddleware<RequestTimingMiddleware>();

// Or short syntax
app.Use(async (context, next) =>
{
    var stopwatch = Stopwatch.StartNew();
    await next();
    stopwatch.Stop();
    context.Response.Headers["X-Request-Time"] = stopwatch.ElapsedMilliseconds.ToString();
});
```

---

## Controller

**Định nghĩa**: Controllers là classes xử lý HTTP requests, nhận input từ user, thực hiện business logic, và trả về responses.

**Ví dụ**:
```csharp
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;
    
    public UsersController(IUserService userService)
    {
        _userService = userService;
    }
    
    [HttpGet]
    public async Task<ActionResult<IEnumerable<UserDto>>> GetUsers()
    {
        var users = await _userService.GetAllUsersAsync();
        return Ok(users);
    }
    
    [HttpGet("{id}")]
    public async Task<ActionResult<UserDto>> GetUser(int id)
    {
        var user = await _userService.GetUserByIdAsync(id);
        
        if (user == null)
            return NotFound();
            
        return Ok(user);
    }
    
    [HttpPost]
    public async Task<ActionResult<UserDto>> CreateUser(CreateUserRequest request)
    {
        var user = await _userService.CreateUserAsync(request);
        return CreatedAtAction(nameof(GetUser), new { id = user.Id }, user);
    }
}
```

---

## Dependency Injection (DI)

**Định nghĩa**: Dependency Injection là design pattern cho phép các dependencies được injected vào class thay vì class tự tạo. ASP.NET Core có built-in DI container.

**Ví dụ**:
```csharp
// Register services
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddTransient<IEmailService, EmailService>();
builder.Services.AddSingleton<ISettings, Settings>();

// Inject into controller
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;
    
    public UsersController(IUserService userService)
    {
        _userService = userService;
    }
}

// Or use [FromServices] attribute
[HttpGet]
public async Task<ActionResult<UserDto>> Get([FromServices] IUserService userService)
{
    return Ok(await userService.GetAllAsync());
}
```

---

## Entity Framework Core

**Định nghĩa**: Entity Framework Core là lightweight, extensible ORM cho .NET, cho phép developers làm việc với database sử dụng .NET objects.

**Ví dụ**:
```csharp
// DbContext
public class ApplicationDbContext : DbContext
{
    public DbSet<User> Users { get; set; }
    public DbSet<Post> Posts { get; set; }
    
    protected override void OnConfiguring(DbContextOptionsBuilder options)
    {
        options.UseSqlServer("ConnectionString");
    }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<User>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).IsRequired().HasMaxLength(100);
            entity.HasMany(e => e.Posts).WithOne(p => p.User);
        });
    }
}

// Usage
public class UserService : IUserService
{
    private readonly ApplicationDbContext _context;
    
    public UserService(ApplicationDbContext context)
    {
        _context = context;
    }
    
    public async Task<IEnumerable<User>> GetAllAsync()
    {
        return await _context.Users.Include(u => u.Posts).ToListAsync();
    }
}
```

---

## Routing

**Định nghĩa**: Routing là process của matching incoming HTTP requests đến endpoints. ASP.NET Core hỗ trợ attribute-based routing và conventional routing.

**Ví dụ**:
```csharp
// Attribute routing
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpGet]                      // GET api/products
    public async Task<IActionResult> GetAll() { }
    
    [HttpGet("{id}")]             // GET api/products/{id}
    public async Task<IActionResult> GetById(int id) { }
    
    [HttpPost]                     // POST api/products
    public async Task<IActionResult> Create(Product product) { }
    
    [HttpPut("{id}")]             // PUT api/products/{id}
    public async Task<IActionResult> Update(int id, Product product) { }
    
    [HttpDelete("{id}")]          // DELETE api/products/{id}
    public async Task<IActionResult> Delete(int id) { }
}

// Conventional routing
app.UseEndpoints(endpoints =>
{
    endpoints.MapControllerRoute(
        name: "default",
        pattern: "{controller=Home}/{action=Index}/{id?}");
        
    endpoints.MapControllerRoute(
        name: "admin",
        pattern: "admin/{controller=Dashboard}/{action=Index}/{id?}");
});
```

---

## Configuration

**Định nghĩa**: Configuration trong ASP.NET Core được xây dựng trên key-value pairs, có thể đọc từ multiple sources như JSON files, environment variables.

**Ví dụ**:
```csharp
// appsettings.json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning"
    }
  },
  "AllowedHosts": "*",
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=MyDb;Trusted_Connection=True;"
  }
}

// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Access configuration
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
var logLevel = builder.Configuration["Logging:LogLevel:Default"];

// Bind to strongly-typed settings
var appSettings = new AppSettings();
builder.Configuration.Bind(appSettings);

// Use options pattern
builder.Services.Configure<EmailSettings>(
    builder.Configuration.GetSection("EmailSettings"));
```

---

## Authentication & Authorization

**Định nghĩa**: Authentication là process xác định identity của user. Authorization là process kiểm tra permissions để access resources.

**Ví dụ**:
```csharp
// Program.cs - Authentication
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

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AdminOnly", policy => policy.RequireRole("Admin"));
    options.AddPolicy("MinimumAge", policy => 
        policy.Requirements.Add(new MinimumAgeRequirement(18)));
});

// Controller usage
[Authorize]
public class AdminController : ControllerBase
{
    [Authorize(Roles = "Admin")]
    public IActionResult AdminOnly() { }
    
    [Authorize(Policy = "MinimumAge")]
    public IActionResult AgeRestricted() { }
}
```

---

## Action Result

**Định nghĩa**: ActionResult là return type cho controller actions, cho phép trả về nhiều types của responses như Ok, NotFound, BadRequest.

**Ví dụ**:
```csharp
public class UsersController : ControllerBase
{
    [HttpGet("{id}")]
    public async Task<ActionResult<UserDto>> GetUser(int id)
    {
        var user = await _userService.GetByIdAsync(id);
        
        if (user == null)
            return NotFound(); // 404
            
        return Ok(user); // 200
    }
    
    [HttpPost]
    public async Task<ActionResult<UserDto>> CreateUser(CreateUserRequest request)
    {
        if (!ModelState.IsValid)
            return BadRequest(ModelState); // 400
            
        var user = await _userService.CreateAsync(request);
        return CreatedAtAction(nameof(GetUser), new { id = user.Id }, user); // 201
    }
    
    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteUser(int id)
    {
        var result = await _userService.DeleteAsync(id);
        
        if (!result)
            return NotFound(); // 404
            
        return NoContent(); // 204
    }
}
```

---

## LINQ

**Định nghĩa**: Language Integrated Query (LINQ) là syntax để query collections trong C#, có thể sử dụng với databases qua EF Core.

**Ví dụ**:
```csharp
// Query syntax
var adults = from user in _context.Users
             where user.Age >= 18
             orderby user.Name
             select user;

// Method syntax
var adults = _context.Users
    .Where(u => u.Age >= 18)
    .OrderBy(u => u.Name)
    .ToListAsync();

// With projection
var userDtos = _context.Users
    .Select(u => new UserDto
    {
        Id = u.Id,
        FullName = u.FirstName + " " + u.LastName,
        PostCount = u.Posts.Count()
    })
    .ToListAsync();

// Grouping
var groupedByCity = _context.Users
    .GroupBy(u => u.City)
    .Select(g => new 
    {
        City = g.Key,
        Count = g.Count(),
        Users = g.ToList()
    })
    .ToListAsync();
```

---

## Options Pattern

**Định nghĩa**: Options pattern sử dụng classes để strongly-typed access đến groups của related settings.

**Ví dụ**:
```csharp
// Settings class
public class EmailSettings
{
    public const string Position = "EmailSettings";
    
    public string SmtpServer { get; set; }
    public int Port { get; set; }
    public string Username { get; set; }
    public string Password { get; set; }
    public bool EnableSsl { get; set; }
}

// appsettings.json
{
  "EmailSettings": {
    "SmtpServer": "smtp.gmail.com",
    "Port": 587,
    "Username": "noreply@example.com",
    "Password": "secret",
    "EnableSsl": true
  }
}

// Register and use
builder.Services.Configure<EmailSettings>(
    builder.Configuration.GetSection(EmailSettings.Position));

// Inject
public class EmailService : IEmailService
{
    private readonly EmailSettings _settings;
    
    public EmailService(IOptions<EmailSettings> options)
    {
        _settings = options.Value;
    }
}
```

---

## Liên kết liên quan
- [ASP.NET Core Architecture](./architecture.md)
- [ASP.NET Core Best Practices](./best-practice.md)
- [ASP.NET Core Anti-Patterns](./anti-pattern.md)
- [ASP.NET Core Checklist](./checklist.md)
- [ASP.NET Core FAQ](./faq.md)
- [ASP.NET Core Decision Tree](./decision-tree.md)
