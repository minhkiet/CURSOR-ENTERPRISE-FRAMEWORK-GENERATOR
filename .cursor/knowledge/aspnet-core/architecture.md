# ASP.NET Core Architecture - Kiến Trúc ASP.NET Core

## Tổng quan

ASP.NET Core là cross-platform framework cho xây dựng web applications. Kiến trúc tập trung vào modularity, dependency injection, và performance.

## Kiến trúc chi tiết

### 1. Project Structure

```
├── Controllers/          # API Controllers
├── Models/             # Domain models
├── Views/               # Razor views
├── Services/           # Business logic
├── Repositories/        # Data access
├── DTOs/                # Data transfer objects
├── Middleware/          # Custom middleware
├── Extensions/          # Extension methods
└── Program.cs          # Entry point
```

### 2. Clean Architecture

```
├── Domain/             # Entities, interfaces
├── Application/       # Use cases, DTOs
├── Infrastructure/     # EF Core, external services
└── Presentation/        # API, Controllers
```

### 3. Web API Design

```csharp
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<IEnumerable<UserDto>>> GetUsers()
    {
        return Ok(await _service.GetUsersAsync());
    }
}
```

### 4. Dependency Injection

```csharp
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddDbContext<AppDbContext>();
```

### 5. Entity Framework Core

```csharp
public class AppDbContext : DbContext
{
    public DbSet<User> Users => Set<User>();
}
```

## Deployment

### Options

- **Azure App Service**: Managed hosting
- **Docker**: Containerized deployment
- **IIS**: Traditional hosting
- **Kestrel**: Self-hosted

## Kết luận

ASP.NET Core cung cấp powerful, modern web development platform.
