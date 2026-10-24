# ASP.NET Core Stack

> **Version:** 1.0.0 | **Framework:** ASP.NET Core 8 | **ORM:** Dapper

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | ASP.NET Core 8 |
| ORM | Dapper |
| Database | PostgreSQL / MySQL |
| Auth | JWT + Refresh Token |
| API | REST |
| Validation | FluentValidation |
| Testing | xUnit + Moq |

---

## Project Structure

```
src/
├── Domain/
│   ├── Entities/
│   │   └── User.cs
│   ├── ValueObjects/
│   │   └── Email.cs
│   ├── Interfaces/
│   │   ├── IUserRepository.cs
│   │   └── IEmailService.cs
│   └── Services/
│       └── UserDomainService.cs
│
├── Application/
│   ├── UseCases/
│   │   ├── CreateUserUseCase.cs
│   │   └── GetUserUseCase.cs
│   ├── DTOs/
│   │   ├── CreateUserDto.cs
│   │   └── UserDto.cs
│   └── Validators/
│       └── CreateUserValidator.cs
│
├── Infrastructure/
│   ├── Database/
│   │   ├── DapperContext.cs
│   │   └── Repositories/
│   │       └── UserRepository.cs
│   └── Services/
│       └── JwtService.cs
│
├── Presentation/
│   ├── Controllers/
│   │   └── UsersController.cs
│   ├── Middleware/
│   │   └── ExceptionMiddleware.cs
│   └── Filters/
│       └── ValidateModelAttribute.cs
│
├── Program.cs
└── appsettings.json
```

---

## Entity Pattern

```csharp
namespace Domain.Entities;

public class User
{
    public Guid Id { get; private set; }
    public string Email { get; private set; } = null!;
    public string PasswordHash { get; private set; } = null!;
    public string Name { get; private set; } = null!;
    public UserStatus Status { get; private set; }
    public DateTime CreatedAt { get; private set; }
    public DateTime? UpdatedAt { get; private set; }
    
    // Private constructor for ORM
    private User() { }
    
    public static User Create(string email, string passwordHash, string name)
    {
        if (string.IsNullOrWhiteSpace(email))
            throw new ArgumentException("Email is required", nameof(email));
            
        return new User
        {
            Id = Guid.NewGuid(),
            Email = email.ToLowerInvariant(),
            PasswordHash = passwordHash,
            Name = name,
            Status = UserStatus.Active,
            CreatedAt = DateTime.UtcNow
        };
    }
    
    public void UpdateName(string name)
    {
        Name = name;
        UpdatedAt = DateTime.UtcNow;
    }
}

public enum UserStatus
{
    Active,
    Inactive,
    Suspended
}
```

---

## Repository Pattern

```csharp
// Domain/Interfaces/IUserRepository.cs
namespace Domain.Interfaces;

public interface IUserRepository
{
    Task<User?> GetByIdAsync(Guid id, CancellationToken ct = default);
    Task<User?> GetByEmailAsync(string email, CancellationToken ct = default);
    Task<IEnumerable<User>> GetAllAsync(int page, int pageSize, CancellationToken ct = default);
    Task<int> GetCountAsync(CancellationToken ct = default);
    Task<User> CreateAsync(User user, CancellationToken ct = default);
    Task UpdateAsync(User user, CancellationToken ct = default);
    Task DeleteAsync(Guid id, CancellationToken ct = default);
}

// Infrastructure/Database/Repositories/UserRepository.cs
namespace Infrastructure.Database.Repositories;

public class UserRepository : IUserRepository
{
    private readonly DapperContext _context;
    
    public UserRepository(DapperContext context)
    {
        _context = context;
    }
    
    public async Task<User?> GetByIdAsync(Guid id, CancellationToken ct = default)
    {
        const string sql = @"
            SELECT id, email, password_hash, name, status, created_at, updated_at
            FROM users 
            WHERE id = @Id";
            
        await using var connection = _context.CreateConnection();
        var result = await connection.QuerySingleOrDefaultAsync<UserDto>(
            new CommandDefinition(sql, new { Id = id }, cancellationToken: ct));
            
        return result?.ToEntity();
    }
    
    public async Task<User> CreateAsync(User user, CancellationToken ct = default)
    {
        const string sql = @"
            INSERT INTO users (id, email, password_hash, name, status, created_at)
            VALUES (@Id, @Email, @PasswordHash, @Name, @Status, @CreatedAt)";
            
        await using var connection = _context.CreateConnection();
        await connection.ExecuteAsync(
            new CommandDefinition(sql, user, cancellationToken: ct));
            
        return user;
    }
}
```

---

## Use Case Pattern

```csharp
namespace Application.UseCases;

public record CreateUserCommand(
    string Email,
    string Password,
    string Name
);

public class CreateUserUseCase
{
    private readonly IUserRepository _userRepository;
    private readonly IPasswordHasher _passwordHasher;
    private readonly IEventPublisher _eventPublisher;
    
    public CreateUserUseCase(
        IUserRepository userRepository,
        IPasswordHasher passwordHasher,
        IEventPublisher eventPublisher)
    {
        _userRepository = userRepository;
        _passwordHasher = passwordHasher;
        _eventPublisher = eventPublisher;
    }
    
    public async Task<Result<User>> ExecuteAsync(
        CreateUserCommand command, 
        CancellationToken ct = default)
    {
        // Check duplicate
        var existing = await _userRepository.GetByEmailAsync(
            command.Email.ToLowerInvariant(), ct);
            
        if (existing != null)
            return Result.Failure<User>("EMAIL_EXISTS");
        
        // Hash password
        var passwordHash = _passwordHasher.Hash(command.Password);
        
        // Create user
        var user = User.Create(command.Email, passwordHash, command.Name);
        
        // Persist
        await _userRepository.CreateAsync(user, ct);
        
        // Publish event
        await _eventPublisher.PublishAsync(
            new UserCreatedEvent(user.Id, user.Email));
        
        return Result.Success(user);
    }
}

public class Result<T>
{
    public bool Success { get; }
    public T? Data { get; }
    public string? Error { get; }
    
    private Result(bool success, T? data, string? error)
    {
        Success = success;
        Data = data;
        Error = error;
    }
    
    public static Result<T> Success(T data) => new(true, data, null);
    public static Result<T> Failure(string error) => new(false, default, error);
}
```

---

## Controller Pattern

```csharp
namespace Presentation.Controllers;

[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly CreateUserUseCase _createUserUseCase;
    private readonly GetUserUseCase _getUserUseCase;
    private readonly ILogger<UsersController> _logger;
    
    public UsersController(
        CreateUserUseCase createUserUseCase,
        GetUserUseCase getUserUseCase,
        ILogger<UsersController> logger)
    {
        _createUserUseCase = createUserUseCase;
        _getUserUseCase = getUserUseCase;
        _logger = logger;
    }
    
    [HttpPost]
    [ProducesResponseType(typeof(UserDto), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ErrorResponse), StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> Create(
        [FromBody] CreateUserDto dto,
        CancellationToken ct)
    {
        var command = new CreateUserCommand(dto.Email, dto.Password, dto.Name);
        var result = await _createUserUseCase.ExecuteAsync(command, ct);
        
        if (!result.Success)
        {
            _logger.LogWarning("Failed to create user: {Error}", result.Error);
            return BadRequest(new ErrorResponse(result.Error!));
        }
        
        var userDto = UserDto.FromEntity(result.Data!);
        return CreatedAtAction(
            nameof(GetById), 
            new { id = userDto.Id }, 
            new { data = userDto });
    }
    
    [HttpGet("{id:guid}")]
    public async Task<IActionResult> GetById(Guid id, CancellationToken ct)
    {
        var result = await _getUserUseCase.ExecuteAsync(id, ct);
        
        if (!result.Success)
            return NotFound(new ErrorResponse(result.Error!));
            
        return Ok(new { data = UserDto.FromEntity(result.Data!) });
    }
}
```

---

## JWT Service

```csharp
namespace Infrastructure.Services;

public class JwtService
{
    private readonly JwtSettings _settings;
    
    public JwtService(IOptions<JwtSettings> settings)
    {
        _settings = settings.Value;
    }
    
    public string GenerateToken(User user)
    {
        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
            new Claim(JwtRegisteredClaimNames.Email, user.Email),
            new Claim(ClaimTypes.Role, user.Status.ToString()),
            new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
        };
        
        var key = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(_settings.Secret));
            
        var credentials = new SigningCredentials(
            key, SecurityAlgorithms.HmacSha256);
            
        var token = new JwtSecurityToken(
            issuer: _settings.Issuer,
            audience: _settings.Audience,
            claims: claims,
            expires: DateTime.UtcNow.Add(_settings.Expiry),
            signingCredentials: credentials);
            
        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
```

---

## Checklist

```
┌─────────────────────────────────────────────────────────────┐
│ ASP.NET Core + Dapper Checklist                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Clean Architecture (Domain → Application → Infrastructure)│
│ □ Dapper for high-performance queries                     │
│ □ Repository pattern with interfaces                      │
│ □ Use cases for business logic                           │
│ □ JWT authentication                                     │
│ □ FluentValidation for input                             │
│ □ Global exception handling                              │
│ □ Structured logging                                     │
│ □ Unit tests with xUnit + Moq                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
