# ASP.NET Core Architecture - Kiến Trúc Chi Tiết

## Mục lục
1. [Tổng quan Kiến trúc](#1-tổng-quan-kiến-trúc)
2. [Request Pipeline](#2-request-pipeline)
3. [Project Structure](#3-project-structure)
4. [Clean Architecture](#4-clean-architecture)
5. [Data Access Layer](#5-data-access-layer)

---

## 1. Tổng quan Kiến trúc

### 1.1 ASP.NET Core Overview

ASP.NET Core là cross-platform framework để xây dựng modern, cloud-based web applications. Nó được thiết kế modular với dependency injection, middleware, và lightweight components.

Core components:
- **Host**: Configures services và middleware
- **Middleware**: Request/Response pipeline
- **Controllers**: Handle HTTP requests
- **Models**: Data representations
- **Services**: Business logic
- **Data Access**: Database operations

### 1.2 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ASP.NET CORE APPLICATION                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    HTTP REQUEST                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    MIDDLEWARE PIPELINE                        │   │
│  │                                                             │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │   │
│  │  │ Exception│→ │  Auth   │→ │  CORS   │→ │  Custom │→   │   │
│  │  │ Handler │  │         │  │         │  │         │    │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘    │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      CONTROLLER                                │   │
│  │                                                             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │ [HttpGet] [HttpPost] [Authorize] [Route(...)]       │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│          ┌───────────────────┼───────────────────┐                │
│          │                   │                   │                  │
│          ▼                   ▼                   ▼                   │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐          │
│  │   Services   │  │   Validators │  │   Mappers    │          │
│  │              │  │              │  │              │          │
│  └───────────────┘  └───────────────┘  └───────────────┘          │
│          │                   │                   │                  │
│          └───────────────────┴───────────────────┘                │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    DATA ACCESS LAYER                        │   │
│  │                                                             │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  │   │
│  │  │    Entity    │  │   DbContext  │  │  Repositories │  │   │
│  │  │   Framework  │  │              │  │              │  │   │
│  │  └───────────────┘  └───────────────┘  └───────────────┘  │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      DATABASE                                 │   │
│  │                 (SQL Server, PostgreSQL)                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Request Pipeline

### 2.1 Middleware Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                      REQUEST PIPELINE                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  HTTP Request                                                       │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   SERVER (Kestrel)                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 1. Exception Handler Middleware                              │   │
│  │    - Catches exceptions globally                            │   │
│  │    - Logs errors                                           │   │
│  │    - Returns error response                                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 2. HTTPS Redirection (if enabled)                           │   │
│  │    - Redirects HTTP to HTTPS                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 3. Static Files                                            │   │
│  │    - Serves static files (CSS, JS, images)                 │   │
│  │    - Short-circuits pipeline for static content            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 4. Authentication Middleware                                │   │
│  │    - Parses auth headers                                   │   │
│  │    - Creates User principal                                 │   │
│  │    - Sets HttpContext.User                                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 5. CORS Middleware                                         │   │
│  │    - Handles Cross-Origin Resource Sharing                  │   │
│  │    - Adds CORS headers                                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 6. Custom Middleware                                       │   │
│  │    - Application-specific logic                            │   │
│  │    - Logging, monitoring, etc.                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 7. Authorization Middleware                                 │   │
│  │    - Checks [Authorize] attributes                          │   │
│  │    - Enforces policies                                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 8. Endpoints (Controller Action)                           │   │
│  │    - Executes controller action                            │   │
│  │    - Returns ActionResult                                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│       │                                                             │
│       ▼                                                             │
│  HTTP Response                                                      │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 2.2 Middleware Registration

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Authentication & Authorization
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options => { /* ... */ });
builder.Services.AddAuthorization();

// Add application services
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddScoped<IProductService, ProductService>();

var app = builder.Build();

// Configure middleware pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseExceptionHandler("/error"); // Must be first after build
app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();

app.UseAuthentication(); // Before authorization
app.UseAuthorization();

app.MapControllers();

app.Run();
```

---

## 3. Project Structure

### 3.1 Standard Project Structure

```
Solution/
├── src/
│   └── MyApp.Api/
│       ├── Controllers/
│       │   ├── UsersController.cs
│       │   └── ProductsController.cs
│       │
│       ├── Program.cs
│       ├── MyApp.Api.csproj
│       └── appsettings.json
│
└── tests/
    └── MyApp.Tests/
        ├── Controllers/
        ├── Services/
        └── MyApp.Tests.csproj
```

### 3.2 Comprehensive Project Structure

```
MyApp/
├── src/
│   └── MyApp.Api/
│       ├── Configuration/           # Settings classes
│       │   └── Settings.cs
│       │
│       ├── Controllers/            # API Controllers
│       │   ├── Base/
│       │   │   └── BaseApiController.cs
│       │   ├── UsersController.cs
│       │   └── ProductsController.cs
│       │
│       ├── Data/                  # Data access
│       │   ├── ApplicationDbContext.cs
│       │   └── Configurations/
│       │       ├── UserConfiguration.cs
│       │       └── ProductConfiguration.cs
│       │
│       ├── DTOs/                  # Data Transfer Objects
│       │   ├── Requests/
│       │   │   ├── CreateUserRequest.cs
│       │   │   └── UpdateUserRequest.cs
│       │   └── Responses/
│       │       ├── UserResponse.cs
│       │       └── ProductResponse.cs
│       │
│       ├── Entities/              # Domain entities
│       │   ├── User.cs
│       │   ├── Product.cs
│       │   └── Base/
│       │       └── BaseEntity.cs
│       │
│       ├── Middleware/            # Custom middleware
│       │   ├── RequestTimingMiddleware.cs
│       │   └── ExceptionHandlingMiddleware.cs
│       │
│       ├── Program.cs
│       ├── appsettings.json
│       └── MyApp.Api.csproj
│
├── tests/
│   └── MyApp.Tests/
│       ├── Controllers/
│       ├── Services/
│       └── MyApp.Tests.csproj
│
├── MyApp.sln
└── README.md
```

---

## 4. Clean Architecture

### 4.1 Clean Architecture Layers

```
┌─────────────────────────────────────────────────────────────────────┐
│                      CLEAN ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    PRESENTATION LAYER                         │   │
│  │                                                             │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  │   │
│  │  │  Controllers  │  │    DTOs      │  │   Filters    │  │   │
│  │  └───────────────┘  └───────────────┘  └───────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    APPLICATION LAYER                         │   │
│  │                                                             │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  │   │
│  │  │   Services   │  │   Interfaces  │  │   Mappers    │  │   │
│  │  └───────────────┘  └───────────────┘  └───────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                      DOMAIN LAYER                            │   │
│  │                                                             │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  │   │
│  │  │   Entities   │  │  Interfaces   │  │   Value       │  │   │
│  │  │              │  │              │  │   Objects    │  │   │
│  │  └───────────────┘  └───────────────┘  └───────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  INFRASTRUCTURE LAYER                         │   │
│  │                                                             │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  │   │
│  │  │ Repository   │  │    EF Core    │  │  External    │  │   │
│  │  │ Implementations│  │   Context    │  │  Services   │  │   │
│  │  └───────────────┘  └───────────────┘  └───────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 4.2 Project Structure with Clean Architecture

```
Solution/
├── src/
│   ├── MyApp.Domain/           # Domain Layer
│   │   ├── Entities/
│   │   │   ├── User.cs
│   │   │   └── Product.cs
│   │   ├── Interfaces/
│   │   │   ├── IUserRepository.cs
│   │   │   └── IProductRepository.cs
│   │   └── ValueObjects/
│   │       └── Address.cs
│   │
│   ├── MyApp.Application/     # Application Layer
│   │   ├── DTOs/
│   │   │   ├── UserDto.cs
│   │   │   └── CreateUserDto.cs
│   │   ├── Interfaces/
│   │   │   ├── IUserService.cs
│   │   │   └── IProductService.cs
│   │   ├── Services/
│   │   │   ├── UserService.cs
│   │   │   └── ProductService.cs
│   │   └── Mappings/
│   │       └── MappingProfile.cs
│   │
│   └── MyApp.Api/              # Infrastructure & Presentation
│       ├── Controllers/
│       ├── Data/
│       ├── Middleware/
│       └── Program.cs
│
└── tests/
    ├── MyApp.Domain.Tests/
    ├── MyApp.Application.Tests/
    └── MyApp.Api.Tests/
```

---

## 5. Data Access Layer

### 5.1 Entity Framework Core Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ENTITY FRAMEWORK CORE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    DbContext                                 │   │
│  │                                                             │   │
│  │  public class ApplicationDbContext : DbContext              │   │
│  │  {                                                          │   │
│  │      public DbSet<User> Users { get; set; }                │   │
│  │      public DbSet<Product> Products { get; set; }          │   │
│  │                                                             │   │
│  │      protected override void OnModelCreating(ModelBuilder)   │   │
│  │      {                                                      │   │
│  │          // Fluent API configurations                       │   │
│  │      }                                                      │   │
│  │  }                                                          │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  ENTITY CONFIGURATION                       │   │
│  │                                                             │   │
│  │  public class UserConfiguration : IEntityTypeConfiguration<User> │   │
│  │  {                                                          │   │
│  │      public void Configure(EntityTypeBuilder<User> builder) │   │
│  │      {                                                      │   │
│  │          builder.ToTable("Users");                           │   │
│  │          builder.HasKey(u => u.Id);                         │   │
│  │          builder.Property(u => u.Name).IsRequired();        │   │
│  │          builder.HasIndex(u => u.Email).IsUnique();        │   │
│  │          builder.HasMany(u => u.Posts)                      │   │
│  │              .WithOne(p => p.User)                         │   │
│  │              .HasForeignKey(p => p.UserId);               │   │
│  │      }                                                      │   │
│  │  }                                                          │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    DATABASE PROVIDER                         │   │
│  │                                                             │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │   SQL Server  │  │  PostgreSQL   │  │    SQLite    │    │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 5.2 Repository Pattern

```csharp
// Domain Layer - Interface
public interface IUserRepository
{
    Task<User> GetByIdAsync(int id);
    Task<IEnumerable<User>> GetAllAsync();
    Task<User> AddAsync(User user);
    Task UpdateAsync(User user);
    Task DeleteAsync(int id);
    Task<User> GetByEmailAsync(string email);
}

// Infrastructure Layer - Implementation
public class UserRepository : IUserRepository
{
    private readonly ApplicationDbContext _context;
    
    public UserRepository(ApplicationDbContext context)
    {
        _context = context;
    }
    
    public async Task<User> GetByIdAsync(int id)
    {
        return await _context.Users
            .Include(u => u.Posts)
            .FirstOrDefaultAsync(u => u.Id == id);
    }
    
    public async Task<IEnumerable<User>> GetAllAsync()
    {
        return await _context.Users.ToListAsync();
    }
    
    public async Task<User> AddAsync(User user)
    {
        await _context.Users.AddAsync(user);
        await _context.SaveChangesAsync();
        return user;
    }
    
    public async Task UpdateAsync(User user)
    {
        _context.Entry(user).State = EntityState.Modified;
        await _context.SaveChangesAsync();
    }
    
    public async Task DeleteAsync(int id)
    {
        var user = await _context.Users.FindAsync(id);
        if (user != null)
        {
            _context.Users.Remove(user);
            await _context.SaveChangesAsync();
        }
    }
    
    public async Task<User> GetByEmailAsync(string email)
    {
        return await _context.Users
            .FirstOrDefaultAsync(u => u.Email == email);
    }
}
```

---

## Liên kết liên quan
- [ASP.NET Core Glossary](./glossary.md)
- [ASP.NET Core Best Practices](./best-practice.md)
- [ASP.NET Core Anti-Patterns](./anti-pattern.md)
- [ASP.NET Core Checklist](./checklist.md)
- [ASP.NET Core FAQ](./faq.md)
- [ASP.NET Core Decision Tree](./decision-tree.md)
