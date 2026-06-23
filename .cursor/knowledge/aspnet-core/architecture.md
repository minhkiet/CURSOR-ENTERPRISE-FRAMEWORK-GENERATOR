---
title: "ASP.NET Core Architecture - Kiến Trúc ASP.NET Core"
description: "Hướng dẫn toàn diện về Clean Architecture, CQRS, Vertical Slice, và Event-Driven Patterns trong ASP.NET Core"
tags: ["aspnet-core", "architecture", "clean-architecture", "cqrs", "event-driven", "ddd"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# ASP.NET Core Architecture - Kiến Trúc ASP.NET Core

## Tổng Quan

Kiến trúc phần mềm là nền tảng quyết định sự thành công lâu dài của một ứng dụng. Một kiến trúc tốt không chỉ giúp code dễ maintain và test mà còn cho phép ứng dụng scale một cách hiệu quả. Trong ASP.NET Core, có nhiều architectural patterns đã được proven trong production environments.

Tài liệu này explore các architectural approaches phổ biến nhất trong ASP.NET Core development: Clean Architecture, CQRS (Command Query Responsibility Segregation), Vertical Slice Architecture, và Event-Driven Architecture. Mỗi pattern có strengths và trade-offs riêng, và việc chọn đúng pattern phụ thuộc vào requirements cụ thể của dự án.

Chúng ta sẽ không chỉ discuss theoretical concepts mà còn cung cấp practical implementation examples từ real-world scenarios. Điều quan trọng là hiểu rằng không có "one size fits all" solution - mỗi architectural pattern có use cases riêng của nó.

## Mục Đích

Mục đích của tài liệu này là cung cấp:

1. **Understanding**: Hiểu sâu về các architectural patterns phổ biến
2. **Comparison**: So sánh pros và cons của từng pattern
3. **Implementation**: Practical examples cho từng pattern
4. **Decision Making**: Guidance cho việc chọn pattern phù hợp
5. **Migration Path**: Cách chuyển đổi giữa các patterns

## 1. Clean Architecture

Clean Architecture là một architectural style được giới thiệu bởi Robert C. Martin (Uncle Bob), tập trung vào separation of concerns và independence of frameworks. Nó enforce một layered architecture where business rules are independent of UI, database, và external services.

### Core Principles

1. **Independence of Frameworks**: Business logic không phụ thuộc vào frameworks
2. **Testability**: Business rules có thể được test without external dependencies
3. **Independence of UI**: UI có thể thay đổi mà không ảnh hưởng business logic
4. **Independence of Database**: Business rules không couple với database
5. **Independence of External Agencies**: Business logic không biết gì về external world

### Project Structure

```
Solution/
├── src/
│   ├── MyApp.Domain/                    # Enterprise Business Rules
│   │   ├── Entities/                     # Core business entities
│   │   │   ├── Order.cs
│   │   │   ├── Customer.cs
│   │   │   └── Product.cs
│   │   ├── ValueObjects/                 # Immutable value types
│   │   │   ├── Money.cs
│   │   │   ├── Address.cs
│   │   │   └── EmailAddress.cs
│   │   ├── Enums/
│   │   │   ├── OrderStatus.cs
│   │   │   └── PaymentStatus.cs
│   │   ├── Interfaces/                    # Port definitions
│   │   │   ├── Repositories/
│   │   │   │   ├── IOrderRepository.cs
│   │   │   │   ├── ICustomerRepository.cs
│   │   │   │   └── IProductRepository.cs
│   │   │   └── Services/
│   │   │       ├── IEmailService.cs
│   │   │       └── IPaymentGateway.cs
│   │   ├── Events/                       # Domain events
│   │   │   ├── OrderCreatedEvent.cs
│   │   │   └── OrderPaidEvent.cs
│   │   ├── Exceptions/                   # Domain exceptions
│   │   │   └── DomainException.cs
│   │   └── Specifications/               # Query specifications
│   │       └── OrderByStatusSpecification.cs
│   │
│   ├── MyApp.Application/               # Application Business Rules
│   │   ├── Common/                       # Shared application logic
│   │   │   ├── Interfaces/
│   │   │   │   ├── IUnitOfWork.cs
│   │   │   │   ├── IMapper.cs
│   │   │   │   └── IDateTimeProvider.cs
│   │   │   ├── Models/
│   │   │   │   └── PaginatedResult.cs
│   │   │   └── Behaviors/
│   │   │       ├── LoggingBehavior.cs
│   │   │       └── ValidationBehavior.cs
│   │   ├── Features/                    # Use cases (feature folders)
│   │   │   └── Orders/
│   │   │       ├── Commands/
│   │   │       │   ├── CreateOrder/
│   │   │       │   │   ├── CreateOrderCommand.cs
│   │   │       │   │   ├── CreateOrderCommandValidator.cs
│   │   │       │   │   └── CreateOrderCommandHandler.cs
│   │   │       │   └── CancelOrder/
│   │   │       │       ├── CancelOrderCommand.cs
│   │   │       │       └── CancelOrderCommandHandler.cs
│   │   │       └── Queries/
│   │   │           ├── GetOrderById/
│   │   │           │   ├── GetOrderByIdQuery.cs
│   │   │           │   └── GetOrderByIdQueryHandler.cs
│   │   │           └── GetOrdersList/
│   │   │               ├── GetOrdersListQuery.cs
│   │   │               └── GetOrdersListQueryHandler.cs
│   │   └── DTOs/
│   │       ├── OrderDto.cs
│   │       └── OrderItemDto.cs
│   │
│   ├── MyApp.Infrastructure/             # Frameworks & Drivers
│   │   ├── Persistence/
│   │   │   ├── ApplicationDbContext.cs
│   │   │   ├── Configurations/          # EF Core configurations
│   │   │   │   ├── OrderConfiguration.cs
│   │   │   │   └── CustomerConfiguration.cs
│   │   │   └── Repositories/
│   │   │       ├── OrderRepository.cs
│   │   │       └── CustomerRepository.cs
│   │   ├── Services/
│   │   │   ├── EmailService.cs
│   │   │   └── PaymentGateway.cs
│   │   ├── Caching/
│   │   │   └── RedisCacheService.cs
│   │   └── External/
│   │       └── ExternalCustomerService.cs
│   │
│   └── MyApp.Api/                       # Interface Adapters
│       ├── Controllers/
│       │   └── OrdersController.cs
│       ├── Middleware/
│       │   ├── ExceptionHandlingMiddleware.cs
│       │   └── CorrelationIdMiddleware.cs
│       ├── Filters/
│       │   └── ValidateModelAttribute.cs
│       ├── Extensions/
│       │   ├── ServiceCollectionExtensions.cs
│       │   └── ApplicationBuilderExtensions.cs
│       └── Program.cs
│
└── tests/
    ├── MyApp.UnitTests/
    └── MyApp.IntegrationTests/
```

### Domain Layer Implementation

```csharp
// Domain/Entities/Order.cs
namespace MyApp.Domain.Entities;

public class Order
{
    public Guid Id { get; private set; }
    public CustomerId CustomerId { get; private set; }
    public OrderStatus Status { get; private set; }
    public Money TotalAmount { get; private set; }
    public DateTime CreatedAt { get; private set; }
    public DateTime? UpdatedAt { get; private set; }
    
    private readonly List<OrderItem> _items = new();
    public IReadOnlyCollection<OrderItem> Items => _items.AsReadOnly();
    
    private readonly List<DomainEvent> _domainEvents = new();
    public IReadOnlyCollection<DomainEvent> DomainEvents => _domainEvents.AsReadOnly();
    
    // Factory method - ensures valid object creation
    public static Order Create(CustomerId customerId, IEnumerable<OrderItemData> items)
    {
        if (customerId is null)
            throw new ArgumentNullException(nameof(customerId));
        
        if (!items.Any())
            throw new DomainException("Order must have at least one item");
        
        var order = new Order
        {
            Id = Guid.NewGuid(),
            CustomerId = customerId,
            Status = OrderStatus.Pending,
            TotalAmount = Money.Zero,
            CreatedAt = DateTime.UtcNow
        };
        
        foreach (var item in items)
        {
            order.AddItem(item.Product, item.Quantity);
        }
        
        order._domainEvents.Add(new OrderCreatedEvent(order.Id, order.CustomerId));
        
        return order;
    }
    
    // Private setter for EF Core
    private Order() { }
    
    public void AddItem(Product product, int quantity)
    {
        if (quantity <= 0)
            throw new DomainException("Quantity must be greater than zero");
        
        var existingItem = _items.FirstOrDefault(i => i.ProductId == product.Id);
        
        if (existingItem is not null)
        {
            existingItem.UpdateQuantity(quantity);
        }
        else
        {
            _items.Add(OrderItem.Create(this, product, quantity));
        }
        
        RecalculateTotal();
    }
    
    public void UpdateStatus(OrderStatus newStatus)
    {
        var previousStatus = Status;
        
        if (!CanTransitionTo(newStatus))
            throw new DomainException(
                $"Cannot transition from {previousStatus} to {newStatus}");
        
        Status = newStatus;
        UpdatedAt = DateTime.UtcNow;
        
        _domainEvents.Add(new OrderStatusChangedEvent(Id, previousStatus, newStatus));
    }
    
    private bool CanTransitionTo(OrderStatus newStatus)
    {
        return (Status, newStatus) switch
        {
            (OrderStatus.Pending, OrderStatus.Paid) => true,
            (OrderStatus.Pending, OrderStatus.Cancelled) => true,
            (OrderStatus.Paid, OrderStatus.Shipped) => true,
            (OrderStatus.Paid, OrderStatus.Cancelled) => true,
            (OrderStatus.Shipped, OrderStatus.Delivered) => true,
            _ => false
        };
    }
    
    private void RecalculateTotal()
    {
        TotalAmount = _items.Aggregate(Money.Zero, (sum, item) => sum + item.Subtotal);
    }
    
    public void ClearDomainEvents() => _domainEvents.Clear();
}
```

```csharp
// Domain/ValueObjects/Money.cs
namespace MyApp.Domain.ValueObjects;

public record Money
{
    public decimal Amount { get; }
    public Currency Currency { get; }
    
    private Money(decimal amount, Currency currency)
    {
        Amount = Math.Round(amount, 2);
        Currency = currency;
    }
    
    public static Money FromDecimal(decimal amount, Currency currency = Currency.USD)
    {
        if (amount < 0)
            throw new ArgumentException("Amount cannot be negative", nameof(amount));
        
        return new Money(amount, currency);
    }
    
    public static Money Zero => new(0, Currency.USD);
    
    public static Money operator +(Money a, Money b)
    {
        EnsureSameCurrency(a, b);
        return new Money(a.Amount + b.Amount, a.Currency);
    }
    
    public static Money operator -(Money a, Money b)
    {
        EnsureSameCurrency(a, b);
        return new Money(a.Amount - b.Amount, a.Currency);
    }
    
    public static Money operator *(Money a, decimal multiplier) =>
        new(a.Amount * multiplier, a.Currency);
    
    public static bool operator >(Money a, Money b)
    {
        EnsureSameCurrency(a, b);
        return a.Amount > b.Amount;
    }
    
    public static bool operator <(Money a, Money b)
    {
        EnsureSameCurrency(a, b);
        return a.Amount < b.Amount;
    }
    
    private static void EnsureSameCurrency(Money a, Money b)
    {
        if (a.Currency != b.Currency)
            throw new DomainException($"Cannot operate on different currencies: {a.Currency} and {b.Currency}");
    }
    
    public override string ToString() => $"{Amount:N2} {Currency}";
}

public enum Currency
{
    USD,
    EUR,
    GBP,
    VND
}
```

```csharp
// Domain/Events/DomainEvent.cs
namespace MyApp.Domain.Events;

public abstract record DomainEvent
{
    public Guid EventId { get; init; } = Guid.NewGuid();
    public DateTime OccurredAt { get; init; } = DateTime.UtcNow;
}

public record OrderCreatedEvent(Guid OrderId, Guid CustomerId) : DomainEvent;

public record OrderPaidEvent(Guid OrderId, decimal Amount) : DomainEvent;

public record OrderStatusChangedEvent(
    Guid OrderId, 
    OrderStatus PreviousStatus, 
    OrderStatus NewStatus) : DomainEvent;

public record OrderItemAddedEvent(
    Guid OrderId, 
    Guid ProductId, 
    int Quantity) : DomainEvent;
```

### Application Layer Implementation

```csharp
// Application/Features/Orders/Commands/CreateOrder/CreateOrderCommand.cs
namespace MyApp.Application.Features.Orders.Commands.CreateOrder;

public record CreateOrderCommand : IRequest<Result<OrderDto>>
{
    public Guid CustomerId { get; init; }
    public List<OrderItemRequest> Items { get; init; } = new();
    public string? Notes { get; init; }
}

public record OrderItemRequest
{
    public Guid ProductId { get; init; }
    public int Quantity { get; init; }
}

// Application/Features/Orders/Commands/CreateOrder/CreateOrderCommandValidator.cs
namespace MyApp.Application.Features.Orders.Commands.CreateOrder;

public class CreateOrderCommandValidator : AbstractValidator<CreateOrderCommand>
{
    public CreateOrderCommandValidator()
    {
        RuleFor(x => x.CustomerId)
            .NotEmpty()
            .WithMessage("Customer ID is required");
        
        RuleFor(x => x.Items)
            .NotEmpty()
            .WithMessage("At least one item is required")
            .Must(items => items.All(i => i.Quantity > 0))
            .WithMessage("All quantities must be greater than zero");
        
        RuleForEach(x => x.Items)
            .ChildRules(item =>
            {
                item.RuleFor(i => i.ProductId)
                    .NotEmpty()
                    .WithMessage("Product ID is required");
            });
        
        RuleFor(x => x.Notes)
            .MaximumLength(500)
            .WithMessage("Notes cannot exceed 500 characters");
    }
}
```

```csharp
// Application/Features/Orders/Commands/CreateOrder/CreateOrderCommandHandler.cs
namespace MyApp.Application.Features.Orders.Commands.CreateOrder;

public class CreateOrderCommandHandler : IRequestHandler<CreateOrderCommand, Result<OrderDto>>
{
    private readonly IOrderRepository _orderRepository;
    private readonly IProductRepository _productRepository;
    private readonly ICustomerRepository _customerRepository;
    private readonly IUnitOfWork _unitOfWork;
    private readonly IMapper _mapper;
    private readonly ILogger<CreateOrderCommandHandler> _logger;
    private readonly IEventBus _eventBus;
    
    public CreateOrderCommandHandler(
        IOrderRepository orderRepository,
        IProductRepository productRepository,
        ICustomerRepository customerRepository,
        IUnitOfWork unitOfWork,
        IMapper mapper,
        ILogger<CreateOrderCommandHandler> logger,
        IEventBus eventBus)
    {
        _orderRepository = orderRepository;
        _productRepository = productRepository;
        _customerRepository = customerRepository;
        _unitOfWork = unitOfWork;
        _mapper = mapper;
        _logger = logger;
        _eventBus = eventBus;
    }
    
    public async Task<Result<OrderDto>> Handle(
        CreateOrderCommand request,
        CancellationToken cancellationToken)
    {
        try
        {
            // Verify customer exists
            var customer = await _customerRepository.GetByIdAsync(request.CustomerId, cancellationToken);
            if (customer is null)
                return Result.Failure<OrderDto>("CUSTOMER_NOT_FOUND", "Customer not found");
            
            // Get products
            var productIds = request.Items.Select(i => i.ProductId).ToList();
            var products = await _productRepository.GetByIdsAsync(productIds, cancellationToken);
            var productsDict = products.ToDictionary(p => p.Id);
            
            // Validate all products exist
            var missingProducts = productIds.Except(productsDict.Keys).ToList();
            if (missingProducts.Any())
                return Result.Failure<OrderDto>(
                    "PRODUCTS_NOT_FOUND", 
                    $"Products not found: {string.Join(", ", missingProducts)}");
            
            // Create order items
            var orderItems = request.Items.Select(item => new OrderItemData
            {
                Product = productsDict[item.ProductId],
                Quantity = item.Quantity
            }).ToList();
            
            // Create order
            var order = Order.Create(customer.Id, orderItems);
            
            // Save
            await _orderRepository.AddAsync(order, cancellationToken);
            await _unitOfWork.SaveChangesAsync(cancellationToken);
            
            _logger.LogInformation(
                "Order {OrderId} created for customer {CustomerId} with {ItemCount} items",
                order.Id, customer.Id, order.Items.Count);
            
            // Publish domain events
            foreach (var domainEvent in order.DomainEvents)
            {
                await _eventBus.PublishAsync(domainEvent, cancellationToken);
            }
            order.ClearDomainEvents();
            
            return Result.Success(_mapper.Map<OrderDto>(order));
        }
        catch (DomainException ex)
        {
            _logger.LogWarning(ex, "Domain exception creating order");
            return Result.Failure<OrderDto>("DOMAIN_ERROR", ex.Message);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating order for customer {CustomerId}", request.CustomerId);
            return Result.ServerError<OrderDto>();
        }
    }
}
```

### MediatR Pipeline Behavior

```csharp
// Application/Common/Behaviors/ValidationBehavior.cs
namespace MyApp.Application.Common.Behaviors;

public class ValidationBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;
    private readonly ILogger<ValidationBehavior<TRequest, TResponse>> _logger;
    
    public ValidationBehavior(
        IEnumerable<IValidator<TRequest>> validators,
        ILogger<ValidationBehavior<TRequest, TResponse>> logger)
    {
        _validators = validators;
        _logger = logger;
    }
    
    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        if (!_validators.Any())
            return await next();
        
        var context = new ValidationContext<TRequest>(request);
        
        var validationResults = await Task.WhenAll(
            _validators.Select(v => v.ValidateAsync(context, cancellationToken)));
        
        var failures = validationResults
            .SelectMany(r => r.Errors)
            .Where(f => f is not null)
            .ToList();
        
        if (failures.Any())
        {
            _logger.LogWarning(
                "Validation failed for {RequestType}: {@Failures}",
                typeof(TRequest).Name,
                failures);
            
            if (typeof(TResponse).IsGenericType && 
                typeof(TResponse).GetGenericTypeDefinition() == typeof(Result<>))
            {
                var errorType = typeof(TResponse).GetGenericArguments()[0];
                var failureMethod = typeof(Result<>)
                    .MakeGenericType(errorType)
                    .GetMethod(nameof(Result<object>.Failure));
                
                var errors = failures
                    .GroupBy(f => f.PropertyName)
                    .ToDictionary(g => g.Key, g => g.Select(e => e.ErrorMessage).ToArray());
                
                return (TResponse)failureMethod!.Invoke(null, new object[] 
                { 
                    "VALIDATION_ERROR", 
                    string.Join("; ", failures.Select(f => f.ErrorMessage))
                })!;
            }
        }
        
        return await next();
    }
}

// Application/Common/Behaviors/LoggingBehavior.cs
public class LoggingBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
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
        
        _logger.LogInformation(
            "Handling {RequestName}",
            requestName);
        
        var stopwatch = Stopwatch.StartNew();
        
        try
        {
            var response = await next();
            
            stopwatch.Stop();
            
            _logger.LogInformation(
                "Handled {RequestName} in {ElapsedMilliseconds}ms",
                requestName,
                stopwatch.ElapsedMilliseconds);
            
            return response;
        }
        catch (Exception ex)
        {
            stopwatch.Stop();
            
            _logger.LogError(ex,
                "Error handling {RequestName} after {ElapsedMilliseconds}ms",
                requestName,
                stopwatch.ElapsedMilliseconds);
            
            throw;
        }
    }
}
```

## 2. CQRS (Command Query Responsibility Segregation)

CQRS là pattern tách biệt read và write operations thành different models. Trong traditional architectures, cùng data model được sử dụng cho cả reading và writing, nhưng trong CQRS, chúng được tách ra để optimize cho từng use case.

### When to Use CQRS

- **Complex domains** với distinct read/write models
- **High read loads** cần optimized read models
- **Different read/write scaling requirements**
- **Team scaling** - different teams can work on read/write separately
- **Event sourcing** integration
- **Multiple presentation views** của same data

### CQRS Implementation

```csharp
// Commands - Write Model
public record CreateProductCommand : IRequest<Result<ProductDto>>
{
    public string Name { get; init; } = string.Empty;
    public string Description { get; init; } = string.Empty;
    public decimal Price { get; init; }
    public Guid CategoryId { get; init; }
    public int StockQuantity { get; init; }
}

public class CreateProductCommandValidator : AbstractValidator<CreateProductCommand>
{
    public CreateProductCommandValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty()
            .MaximumLength(200);
        
        RuleFor(x => x.Price)
            .GreaterThan(0);
        
        RuleFor(x => x.StockQuantity)
            .GreaterThanOrEqualTo(0);
    }
}

public class CreateProductCommandHandler : IRequestHandler<CreateProductCommand, Result<ProductDto>>
{
    private readonly IProductRepository _repository;
    private readonly IUnitOfWork _unitOfWork;
    private readonly IMapper _mapper;
    
    public async Task<Result<ProductDto>> Handle(
        CreateProductCommand command,
        CancellationToken cancellationToken)
    {
        var product = Product.Create(
            command.Name,
            Money.FromDecimal(command.Price),
            command.CategoryId);
        
        product.SetStockQuantity(command.StockQuantity);
        
        if (!string.IsNullOrEmpty(command.Description))
            product.SetDescription(command.Description);
        
        await _repository.AddAsync(product, cancellationToken);
        await _unitOfWork.SaveChangesAsync(cancellationToken);
        
        return Result.Success(_mapper.Map<ProductDto>(product));
    }
}

// Queries - Read Model (Optimized for reads)
public record GetProductDetailQuery(Guid Id) : IRequest<ProductDetailDto?>;

public class GetProductDetailQueryHandler : IRequestHandler<GetProductDetailQuery, ProductDetailDto?>
{
    private readonly ApplicationDbContext _context;
    private readonly IMapper _mapper;
    
    public GetProductDetailQueryHandler(ApplicationDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }
    
    public async Task<ProductDetailDto?> Handle(
        GetProductDetailQuery query,
        CancellationToken cancellationToken)
    {
        // Optimized query với eager loading
        var product = await _context.Products
            .AsNoTracking()
            .Include(p => p.Category)
            .Include(p => p.Reviews)
            .Include(p => p.Images)
            .FirstOrDefaultAsync(p => p.Id == query.Id, cancellationToken);
        
        if (product is null)
            return null;
        
        return new ProductDetailDto
        {
            Id = product.Id,
            Name = product.Name,
            Description = product.Description,
            Price = product.Price.Amount,
            Currency = product.Price.Currency.ToString(),
            Category = new CategoryDto
            {
                Id = product.Category.Id,
                Name = product.Category.Name
            },
            StockQuantity = product.StockQuantity,
            AverageRating = product.Reviews.Any() 
                ? product.Reviews.Average(r => r.Rating) 
                : 0,
            ReviewCount = product.Reviews.Count,
            Images = product.Images.Select(i => new ProductImageDto
            {
                Id = i.Id,
                Url = i.Url,
                IsPrimary = i.IsPrimary
            }).ToList(),
            CreatedAt = product.CreatedAt,
            UpdatedAt = product.UpdatedAt
        };
    }
}
```

### Separate Read/Write Databases (Optional)

```csharp
// For very high-scale scenarios, separate read/write databases
// Write to main database, sync to read replicas

// Infrastructure/Persistence/ReadDbContext.cs
public class ReadDbContext : DbContext
{
    public ReadDbContext(DbContextOptions<ReadDbContext> options) : base(options) { }
    
    public DbSet<ProductReadModel> Products => Set<ProductReadModel>();
    public DbSet<OrderReadModel> Orders => Set<OrderReadModel>();
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<ProductReadModel>(entity =>
        {
            entity.ToTable("Products");
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).IsRequired();
            // Denormalized data for fast reads
        });
    }
}

// Read model gets updated via event handlers
public class ProductEventHandler : 
    IEventHandler<ProductCreatedEvent>,
    IEventHandler<ProductUpdatedEvent>
{
    private readonly ReadDbContext _readContext;
    
    public async Task HandleAsync(ProductCreatedEvent @event, CancellationToken ct)
    {
        var readModel = new ProductReadModel
        {
            Id = @event.ProductId,
            Name = @event.Name,
            Price = @event.Price,
            // ... denormalized fields
            LastModified = DateTime.UtcNow
        };
        
        _readContext.Products.Add(readModel);
        await _readContext.SaveChangesAsync(ct);
    }
}
```

## 3. Vertical Slice Architecture

Vertical Slice Architecture tổ chức code theo features hoặc use cases thay vì layers. Mỗi slice (feature) chứa tất cả code cần thiết để implement một feature, bao gồm controllers, services, repositories, và tests.

### Comparison with Clean Architecture

| Aspect | Clean Architecture | Vertical Slice |
|--------|-------------------|----------------|
| Organization | By layer (Domain, Application, etc.) | By feature (Orders, Products, etc.) |
| Coupling | Low coupling between layers | Low coupling between features |
| Cohesion | Shared infrastructure | Feature-focused |
| Complexity | Better for large systems | Better for medium systems |
| Team scaling | Good for large teams | Good for growing teams |

### Vertical Slice Implementation

```
src/
├── Features/
│   ├── Orders/
│   │   ├── CreateOrder/
│   │   │   ├── CreateOrderEndpoint.cs
│   │   │   ├── CreateOrderRequest.cs
│   │   │   ├── CreateOrderResponse.cs
│   │   │   └── CreateOrderHandler.cs
│   │   ├── GetOrder/
│   │   │   ├── GetOrderEndpoint.cs
│   │   │   └── GetOrderHandler.cs
│   │   └── OrdersDbContext.cs
│   │
│   ├── Products/
│   │   ├── CreateProduct/
│   │   ├── GetProducts/
│   │   └── ProductsDbContext.cs
│   │
│   └── Shared/
│       ├── Endpoints/
│       │   ├── Endpoint.cs
│       │   └── EndpointExtensions.cs
│       └── Validators/
│
├── Core/
│   ├── Entities/
│   ├── ValueObjects/
│   └── Interfaces/
│
└── Infrastructure/
    ├── Persistence/
    └── Services/
```

```csharp
// Features/Orders/CreateOrder/CreateOrderEndpoint.cs
namespace MyApp.Features.Orders.CreateOrder;

public class CreateOrderEndpoint : Endpoint<CreateOrderRequest, CreateOrderResponse>
{
    private readonly IMediator _mediator;
    
    public CreateOrderEndpoint(IMediator mediator)
    {
        _mediator = mediator;
    }
    
    public override void Configure()
    {
        Post("/api/orders");
        AllowAnonymous(); // or specific auth
        Summary(s =>
        {
            s.Summary = "Create a new order";
            s.Description = "Creates a new order with the specified items";
        });
    }
    
    public override async Task HandleAsync(
        CreateOrderRequest request,
        CancellationToken cancellationToken)
    {
        var command = new CreateOrderCommand
        {
            CustomerId = request.CustomerId,
            Items = request.Items.Select(i => new OrderItemCommand
            {
                ProductId = i.ProductId,
                Quantity = i.Quantity
            }).ToList(),
            Notes = request.Notes
        };
        
        var result = await _mediator.Send(command, cancellationToken);
        
        if (result.IsFailure)
        {
            await SendAsync(new CreateOrderResponse
            {
                Success = false,
                Error = result.Error
            }, StatusCodes.Status400BadRequest, cancellationToken);
            return;
        }
        
        await SendAsync(new CreateOrderResponse
        {
            Success = true,
            OrderId = result.Value.Id,
            OrderNumber = result.Value.OrderNumber
        }, StatusCodes.Status201Created, cancellationToken);
    }
}
```

```csharp
// Features/Orders/CreateOrder/CreateOrderHandler.cs
namespace MyApp.Features.Orders.CreateOrder;

public record CreateOrderCommand : ICommand<Result<OrderDto>>
{
    public Guid CustomerId { get; init; }
    public List<OrderItemCommand> Items { get; init; } = new();
    public string? Notes { get; init; }
}

public record OrderItemCommand
{
    public Guid ProductId { get; init; }
    public int Quantity { get; init; }
}

public class CreateOrderHandler : IHandler<CreateOrderCommand, Result<OrderDto>>
{
    private readonly OrdersDbContext _db;
    
    public CreateOrderHandler(OrdersDbContext db)
    {
        _db = db;
    }
    
    public async Task<Result<OrderDto>> Handle(
        CreateOrderCommand command,
        CancellationToken cancellationToken)
    {
        // All logic stays within the feature
        var customer = await _db.Customers
            .FirstOrDefaultAsync(c => c.Id == command.CustomerId, cancellationToken);
        
        if (customer is null)
            return Result.Failure<OrderDto>("Customer not found");
        
        var order = Order.Create(command.CustomerId);
        
        foreach (var item in command.Items)
        {
            var product = await _db.Products.FindAsync(new object[] { item.ProductId }, cancellationToken);
            if (product is null)
                return Result.Failure<OrderDto>($"Product {item.ProductId} not found");
            
            order.AddItem(product, item.Quantity);
        }
        
        _db.Orders.Add(order);
        await _db.SaveChangesAsync(cancellationToken);
        
        return Result.Success(new OrderDto
        {
            Id = order.Id,
            OrderNumber = order.OrderNumber,
            Status = order.Status.ToString(),
            TotalAmount = order.TotalAmount.Amount,
            ItemCount = order.Items.Count
        });
    }
}
```

## 4. Event-Driven Architecture

Event-Driven Architecture là pattern trong đó components communicate qua events thay vì direct calls. Điều này tạo ra loose coupling và cho phép asynchronous processing.

### Components

1. **Domain Events**: Events emitted by domain entities
2. **Integration Events**: Events that cross service boundaries
3. **Event Handlers**: Process events asynchronously
4. **Event Bus**: Infrastructure for event dispatching

### Implementation

```csharp
// Domain/Events/OrderCreatedEvent.cs
namespace MyApp.Domain.Events;

public record OrderCreatedEvent : DomainEvent
{
    public Guid OrderId { get; init; }
    public Guid CustomerId { get; init; }
    public decimal TotalAmount { get; init; }
    public IReadOnlyList<OrderItemEventData> Items { get; init; } = new();
}

public record OrderItemEventData
{
    public Guid ProductId { get; init; }
    public int Quantity { get; init; }
    public decimal UnitPrice { get; init; }
}
```

```csharp
// Application/Common/Interfaces/IEventBus.cs
namespace MyApp.Application.Common.Interfaces;

public interface IEventBus
{
    Task PublishAsync<TEvent>(TEvent @event, CancellationToken ct = default)
        where TEvent : IDomainEvent;
    
    Task PublishAsync<TEvent>(IEnumerable<TEvent> events, CancellationToken ct = default)
        where TEvent : IDomainEvent;
}
```

```csharp
// Infrastructure/Messaging/InMemoryEventBus.cs
namespace MyApp.Infrastructure.Messaging;

public class InMemoryEventBus : IEventBus
{
    private readonly List<Func<IDomainEvent, CancellationToken, Task>> _handlers = new();
    private readonly ILogger<InMemoryEventBus> _logger;
    
    public InMemoryEventBus(ILogger<InMemoryEventBus> logger)
    {
        _logger = logger;
    }
    
    public async Task PublishAsync<TEvent>(TEvent @event, CancellationToken ct = default)
        where TEvent : IDomainEvent
    {
        _logger.LogInformation("Publishing event {EventType} with ID {EventId}",
            typeof(TEvent).Name, @event.EventId);
        
        var tasks = _handlers
            .Select(handler => handler(@event, ct))
            .ToList();
        
        await Task.WhenAll(tasks);
    }
    
    public void Subscribe<TEvent>(Func<TEvent, CancellationToken, Task> handler)
        where TEvent : IDomainEvent
    {
        _handlers.Add((evt, ct) => handler((TEvent)evt, ct));
    }
}
```

```csharp
// Infrastructure/Messaging/IntegrationEventPublisher.cs
// For cross-service communication (via RabbitMQ, Azure Service Bus, etc.)
public interface IIntegrationEventPublisher
{
    Task PublishAsync<TEvent>(TEvent @event, CancellationToken ct = default)
        where TEvent : IntegrationEvent;
}

public class RabbitMqIntegrationEventPublisher : IIntegrationEventPublisher
{
    private readonly IConnection _connection;
    private readonly IMapper _mapper;
    private readonly ILogger<RabbitMqIntegrationEventPublisher> _logger;
    
    public async Task PublishAsync<TEvent>(TEvent @event, CancellationToken ct = default)
        where TEvent : IntegrationEvent
    {
        var channel = _connection.CreateModel();
        var properties = channel.CreateBasicProperties();
        properties.Persistent = true;
        properties.ContentType = "application/json";
        properties.MessageId = @event.EventId.ToString();
        properties.Timestamp = new AmqpTimestamp(((DateTimeOffset)@event.OccurredAt).ToUnixTimeSeconds());
        
        var body = JsonSerializer.SerializeToUtf8Bytes(@event);
        
        channel.BasicPublish(
            exchange: "events",
            routingKey: typeof(TEvent).Name,
            basicProperties: properties,
            body: body);
        
        _logger.LogInformation(
            "Published integration event {EventType} with ID {EventId}",
            typeof(TEvent).Name,
            @event.EventId);
    }
}
```

### Event Handlers

```csharp
// Infrastructure/Events/Handlers/OrderCreatedEventHandler.cs
public class OrderCreatedEventHandler : IEventHandler<OrderCreatedEvent>
{
    private readonly IEmailService _emailService;
    private readonly IInventoryService _inventoryService;
    private readonly ILogger<OrderCreatedEventHandler> _logger;
    
    public OrderCreatedEventHandler(
        IEmailService emailService,
        IInventoryService inventoryService,
        ILogger<OrderCreatedEventHandler> logger)
    {
        _emailService = emailService;
        _inventoryService = inventoryService;
        _logger = logger;
    }
    
    public async Task HandleAsync(OrderCreatedEvent @event, CancellationToken ct)
    {
        _logger.LogInformation(
            "Processing OrderCreatedEvent for order {OrderId}",
            @event.OrderId);
        
        // Update inventory (fire and forget pattern - doesn't block)
        _ = _inventoryService.ReserveStockAsync(@event.Items, ct);
        
        // Send confirmation email
        await _emailService.SendOrderConfirmationAsync(
            @event.CustomerId,
            @event.OrderId,
            ct);
    }
}

// Subscribe to events
public class EventHandlerStartupFilter : IStartupFilter
{
    public Action<IApplicationBuilder> Configure(Action<IApplicationBuilder> next)
    {
        return app =>
        {
            var eventBus = app.ApplicationServices.GetRequiredService<IEventBus>();
            
            eventBus.Subscribe<OrderCreatedEvent>(
                async (@event, ct) =>
                {
                    using var scope = app.ApplicationServices.CreateScope();
                    var handler = scope.ServiceProvider
                        .GetRequiredService<OrderCreatedEventHandler>();
                    await handler.HandleAsync(@event, ct);
                });
            
            next(app);
        };
    }
}
```

## 5. Choosing the Right Architecture

### Decision Matrix

| Requirement | Clean Architecture | Vertical Slice | CQRS |
|-------------|-------------------|----------------|------|
| Small team, simple domain | ✓ | ✓✓ | ✗ |
| Large team, complex domain | ✓✓ | ✓ | ✓✓ |
| High read performance needs | ✓ | ✓ | ✓✓ |
| Event sourcing required | ✓ | ✓ | ✓✓ |
| Rapid feature development | ✓ | ✓✓ | ✓ |
| Strong testability needed | ✓✓ | ✓ | ✓✓ |
| Microservices migration | ✓✓ | ✓ | ✓✓ |

### Hybrid Approaches

```csharp
// Many teams combine patterns for best results:
// - Clean Architecture for overall structure
// - CQRS for complex read/write scenarios
// - Vertical Slices within Application layer
// - Event-Driven for cross-cutting concerns

// Example: Hybrid structure
src/
├── MyApp.Domain/           // Clean Architecture domain layer
│   ├── Entities/
│   ├── ValueObjects/
│   └── Events/
│
├── MyApp.Application/      // Clean Architecture + Vertical Slices
│   ├── Common/
│   │   ├── Behaviors/      // MediatR pipeline
│   │   └── Interfaces/
│   │
│   └── Features/           // Vertical slices
│       ├── Orders/
│       │   ├── Commands/    # CQRS: Commands
│       │   ├── Queries/     # CQRS: Queries
│       │   └── Events/      # Event handlers
│       │
│       └── Products/
│
└── MyApp.Infrastructure/   // Clean Architecture infrastructure
    ├── Persistence/
    ├── Messaging/          # Event bus implementation
    └── External/
```

## 6. Architecture Decision Records (ADR)

Document key architectural decisions:

```markdown
# ADR-001: Architecture Pattern Selection

## Status
Accepted

## Context
We need to choose an architecture pattern for our e-commerce platform that will support:
- 10+ developers working simultaneously
- Complex business logic (orders, inventory, payments)
- High read performance for product browsing
- Eventual consistency across services

## Decision
We will use Clean Architecture with CQRS for the Order and Payment bounded contexts, and Vertical Slice Architecture for simpler contexts like Product Catalog.

## Consequences
### Positive
- Clear separation of concerns
- Independent scaling of read/write operations
- Easier testing and mocking
- Team autonomy for different contexts

### Negative
- More complex initial setup
- Potential for code duplication
- Learning curve for team members

## Alternatives Considered
1. **Pure Clean Architecture**: Too many layers for simpler contexts
2. **Pure Vertical Slice**: Doesn't scale well for complex domains
3. **CQRS everywhere**: Overkill for simple CRUD operations
```

- [ASP.NET Core Best Practices](./best-practice.md)
- [Domain-Driven Design](./ddd.md)

## 7. UI Architecture & Component Library

Phần này mô tả cách tổ chức UI layer sao cho gần với production-grade SPA/SSR applications, tích hợp Clean Architecture từ backend ra đến frontend.

### 7.1 Project Structure - UI Layer

```
src/
├── MyApp.Domain/
├── MyApp.Application/
├── MyApp.Infrastructure/
│
├── MyApp.WebApp/                          # ASP.NET Core MVC / Razor Pages
│   ├── Areas/
│   │   ├── Admin/                        # Admin dashboard area
│   │   │   ├── Pages/
│   │   │   │   ├── Dashboard/
│   │   │   │   │   └── Index.cshtml
│   │   │   │   ├── Products/
│   │   │   │   │   ├── Index.cshtml
│   │   │   │   │   ├── Create.cshtml
│   │   │   │   │   └── Edit.cshtml
│   │   │   │   └── Orders/
│   │   │   │       ├── Index.cshtml
│   │   │   │       └── Detail.cshtml
│   │   │   ├── ViewModels/
│   │   │   └── Components/
│   │   │       ├── ProductTable/
│   │   │       └── OrderStatusBadge/
│   │   │
│   │   └── Api/                          # API area for SPA consumption
│   │
│   ├── wwwroot/
│   │   ├── css/
│   │   │   ├── components/               # BEM-style component CSS
│   │   │   ├── layouts/
│   │   │   └── utilities/
│   │   ├── js/
│   │   │   ├── components/
│   │   │   ├── services/
│   │   │   └── stores/
│   │   └── images/
│   │
│   ├── Views/
│   │   ├── Shared/
│   │   │   ├── _Layout.cshtml
│   │   │   ├── Components/
│   │   │   │   ├── Sidebar/
│   │   │   │   ├── Header/
│   │   │   │   ├── DataTable/
│   │   │   │   ├── Modal/
│   │   │   │   ├── Toast/
│   │   │   │   └── Pagination/
│   │   │   ├── _Sidebar.cshtml
│   │   │   ├── _Header.cshtml
│   │   │   └── _Footer.cshtml
│   │   └── _ViewImports.cshtml
│   │
│   ├── ViewComponents/
│   │   ├── SidebarViewComponent.cs
│   │   ├── NotificationViewComponent.cs
│   │   └── BreadcrumbViewComponent.cs
│   │
│   └── Program.cs
│
├── MyApp.Frontend/                        # Optional: React/Vue SPA
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/               # Shared UI components
│   │   │   ├── features/                # Feature-scoped components
│   │   │   ├── hooks/
│   │   │   ├── layouts/
│   │   │   ├── pages/
│   │   │   ├── services/
│   │   │   ├── store/                   # State management
│   │   │   └── styles/
│   │   └── main.tsx
│   └── package.json
```

### 7.2 Root Layout - Full Application Shell

Đây là layout gốc chứa sidebar, header, và content area — cấu trúc phổ biến trong admin dashboards và SaaS applications thực tế.

```cshtml
@* Views/Shared/_Layout.cshtml *@
@inject IViewLocalizer Localizer
@inject IOptionsSnapshot<AppSettings> Settings

<!DOCTYPE html>
<html lang="@CultureInfo.CurrentUICulture.TwoLetterISOLanguageName"
      data-theme="light"
      class="scroll-smooth">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="@ViewData["Description"]" />
    <title>@ViewData["Title"] - @Settings.Value.AppName</title>

    @* Favicon *@
    <link rel="icon" type="image/svg+xml" href="~/favicon.svg" />

    @* Fonts: Inter từ Google Fonts - font thực tế, không phải system-ui generic *@
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />

    @* Vendor CSS *@
    <link rel="stylesheet" href="~/lib/feather-icons/feather.css" />
    <link rel="stylesheet" href="~/lib/daterangepicker/daterangepicker.css" />

    @* Component CSS (BEM naming) *@
    <link rel="stylesheet" href="~/css/components/reset.css" />
    <link rel="stylesheet" href="~/css/components/variables.css" />
    <link rel="stylesheet" href="~/css/components/base.css" />
    <link rel="stylesheet" href="~/css/layouts/sidebar.css" />
    <link rel="stylesheet" href="~/css/layouts/header.css" />
    <link rel="stylesheet" href="~/css/components/button.css" />
    <link rel="stylesheet" href="~/css/components/table.css" />
    <link rel="stylesheet" href="~/css/components/modal.css" />
    <link rel="stylesheet" href="~/css/components/toast.css" />

    @await RenderSectionAsync("Styles", required: false)
</head>
<body class="app-body">

    @* ===== SIDEBAR ===== *@
    <aside class="sidebar" id="appSidebar" aria-label="Main navigation">
        <div class="sidebar__header">
            <a href="/" class="sidebar__brand">
                <svg class="sidebar__logo" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="32" height="32" rx="8" fill="#6366f1"/>
                    <path d="M8 16L14 22L24 10" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span class="sidebar__brand-text">@Settings.Value.AppName</span>
            </a>
            <button class="sidebar__toggle"
                    aria-label="Toggle sidebar"
                    aria-expanded="true"
                    hx-boost="false"
                    onclick="toggleSidebar()">
                <i data-feather="menu"></i>
            </button>
        </div>

        <nav class="sidebar__nav">
            <div class="sidebar__section">
                <span class="sidebar__section-label">@Localizer["Main"]</span>
                <ul class="sidebar__menu">
                    <li class="sidebar__item">
                        <a href="/admin/dashboard" class="sidebar__link @(IsActive("/admin/dashboard") ? "sidebar__link--active" : "")">
                            <i data-feather="home"></i>
                            <span>@Localizer["Dashboard"]</span>
                        </a>
                    </li>
                    <li class="sidebar__item">
                        <a href="/admin/orders" class="sidebar__link @(IsActive("/admin/orders") ? "sidebar__link--active" : "")">
                            <i data-feather="shopping-bag"></i>
                            <span>@Localizer["Orders"]</span>
                            <span class="sidebar__badge">12</span>
                        </a>
                    </li>
                    <li class="sidebar__item">
                        <a href="/admin/products" class="sidebar__link @(IsActive("/admin/products") ? "sidebar__link--active" : "")">
                            <i data-feather="package"></i>
                            <span>@Localizer["Products"]</span>
                        </a>
                    </li>
                </ul>
            </div>

            <div class="sidebar__section">
                <span class="sidebar__section-label">@Localizer["Management"]</span>
                <ul class="sidebar__menu">
                    <li class="sidebar__item">
                        <a href="/admin/customers" class="sidebar__link @(IsActive("/admin/customers") ? "sidebar__link--active" : "")">
                            <i data-feather="users"></i>
                            <span>@Localizer["Customers"]</span>
                        </a>
                    </li>
                    <li class="sidebar__item has-submenu">
                        <button class="sidebar__link sidebar__link--submenu" aria-expanded="false">
                            <i data-feather="bar-chart-2"></i>
                            <span>@Localizer["Reports"]</span>
                            <i data-feather="chevron-right" class="sidebar__chevron"></i>
                        </button>
                        <ul class="sidebar__submenu">
                            <li><a href="/admin/reports/sales">Sales</a></li>
                            <li><a href="/admin/reports/inventory">Inventory</a></li>
                            <li><a href="/admin/reports/customers">Customers</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </nav>

        <div class="sidebar__footer">
            <div class="sidebar__user">
                <img src="https://i.pravatar.cc/40?u=@User.FindFirst(ClaimTypes.NameIdentifier)?.Value"
                     alt="@User.Identity?.Name"
                     class="sidebar__avatar" />
                <div class="sidebar__user-info">
                    <span class="sidebar__user-name">@User.Identity?.Name</span>
                    <span class="sidebar__user-role">Administrator</span>
                </div>
                <button class="sidebar__user-action" title="Settings" onclick="location.href='/admin/settings'">
                    <i data-feather="settings"></i>
                </button>
            </div>
        </div>
    </aside>

    @* ===== MAIN CONTENT WRAPPER ===== *@
    <div class="app-container" id="appContainer">

        @* ===== HEADER ===== *@
        <header class="app-header">
            <div class="app-header__left">
                @await Component.InvokeAsync("Breadcrumb")
            </div>

            <div class="app-header__right">
                @* Search *@
                <form class="header-search" method="get" action="/admin/search">
                    <i data-feather="search" class="header-search__icon"></i>
                    <input type="search"
                           name="q"
                           class="header-search__input"
                           placeholder="@Localizer["Search..."]"
                           aria-label="@Localizer["Search"]" />
                    <kbd class="header-search__shortcut">Ctrl+K</kbd>
                </form>

                @* Notifications *@
                <div class="header-dropdown" x-data="{ open: false }">
                    <button class="header-icon-btn"
                            @click="open = !open"
                            aria-label="@Localizer["Notifications"]"
                            aria-haspopup="true">
                        <i data-feather="bell"></i>
                        <span class="header-icon-btn__badge">3</span>
                    </button>
                    <div class="header-dropdown__panel header-dropdown__panel--notifications"
                         x-show="open"
                         x-transition
                         @click.away="open = false">
                        <div class="notification__header">
                            <span>@Localizer["Notifications"]</span>
                            <a href="/admin/notifications" class="notification__mark-all">Mark all read</a>
                        </div>
                        @await Component.InvokeAsync("NotificationList")
                    </div>
                </div>

                @* Theme toggle *@
                <button class="header-icon-btn"
                        id="themeToggle"
                        aria-label="Toggle dark mode"
                        title="Toggle theme">
                    <i data-feather="moon" id="themeIcon"></i>
                </button>

                @* Language selector *@
                <div class="header-dropdown" x-data>
                    <button class="header-lang-btn" @click="$dispatch('open-lang-picker')">
                        <span>@CultureInfo.CurrentUICulture.TwoLetterISOLanguageName.ToUpper()</span>
                        <i data-feather="chevron-down"></i>
                    </button>
                </div>
            </div>
        </header>

        @* ===== PAGE CONTENT ===== *@
        <main class="app-content" id="mainContent">
            @RenderBody()
        </main>

        @* ===== FOOTER ===== *@
        <footer class="app-footer">
            <span>&copy; @DateTime.UtcNow.Year @Settings.Value.AppName</span>
            <span class="app-footer__version">v@(Settings.Value.Version)</span>
        </footer>
    </div>

    @* ===== TOAST CONTAINER ===== *@
    <div class="toast-container" id="toastContainer" aria-live="polite" aria-atomic="true">
    </div>

    @* ===== SCRIPTS ===== *@
    <script src="~/lib/feather-icons/feather.min.js"></script>
    <script src="~/lib/alpinejs/cdn.min.js" defer></script>
    <script src="~/lib/htmx/htmx.min.js"></script>

    <script>
        // Initialize Feather icons
        feather.replace();

        // Theme toggle with localStorage persistence
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        const html = document.documentElement;

        const savedTheme = localStorage.getItem('theme') ||
                          (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        applyTheme(savedTheme);

        themeToggle.addEventListener('click', () => {
            const current = html.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            applyTheme(next);
            localStorage.setItem('theme', next);
        });

        function applyTheme(theme) {
            html.setAttribute('data-theme', theme);
            const iconName = theme === 'dark' ? 'sun' : 'moon';
            themeIcon.setAttribute('data-feather', iconName);
            feather.replace();
        }

        // Sidebar toggle (collapse/expand)
        function toggleSidebar() {
            const sidebar = document.getElementById('appSidebar');
            const container = document.getElementById('appContainer');
            sidebar.classList.toggle('sidebar--collapsed');
            container.classList.toggle('app-container--sidebar-collapsed');
        }

        // Keyboard shortcut: Ctrl+K for search focus
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                document.querySelector('.header-search__input')?.focus();
            }
        });

        // Auto-dismiss toasts after 5 seconds
        window.showToast = function(message, type = 'info', duration = 5000) {
            const container = document.getElementById('toastContainer');
            const toast = document.createElement('div');
            toast.className = `toast toast--${type}`;
            toast.innerHTML = `
                <i data-feather="${type === 'success' ? 'check-circle' : type === 'error' ? 'x-circle' : 'info'}"
                   class="toast__icon"></i>
                <span class="toast__message">${message}</span>
                <button class="toast__close" onclick="this.parentElement.remove()">
                    <i data-feather="x"></i>
                </button>`;
            container.appendChild(toast);
            feather.replace();
            setTimeout(() => toast.classList.add('toast--visible'), 10);
            setTimeout(() => {
                toast.classList.remove('toast--visible');
                setTimeout(() => toast.remove(), 300);
            }, duration);
        };
    </script>

    @await RenderSectionAsync("Scripts", required: false)
</body>
</html>
```

### 7.3 CSS Variables & Design Tokens

Design tokens là nền tảng của một design system thực sự. Đây là cách đặt biến CSS đúng cách.

```css
/* css/components/variables.css */

/* ===== COLOR SYSTEM ===== */
/* Không dùng tên màu vô nghĩa như primary-500.
   Dùng semantic naming gần với ngữ cảnh thực tế. */

:root {
    /* Brand colors - chỉ dùng 1 brand color, mọi thứ derivative từ đây */
    --color-brand-50: #eef2ff;
    --color-brand-100: #e0e7ff;
    --color-brand-200: #c7d2fe;
    --color-brand-300: #a5b4fc;
    --color-brand-400: #818cf8;
    --color-brand-500: #6366f1;  /* Primary action */
    --color-brand-600: #4f46e5;  /* Primary hover */
    --color-brand-700: #4338ca;
    --color-brand-800: #3730a3;
    --color-brand-900: #312e81;

    /* Neutral / Gray scale - dùng cho text, borders, backgrounds */
    --color-gray-50: #f9fafb;
    --color-gray-100: #f3f4f6;
    --color-gray-200: #e5e7eb;
    --color-gray-300: #d1d5db;
    --color-gray-400: #9ca3af;
    --color-gray-500: #6b7280;
    --color-gray-600: #4b5563;
    --color-gray-700: #374151;
    --color-gray-800: #1f2937;
    --color-gray-900: #111827;

    /* Semantic colors */
    --color-success-50: #ecfdf5;
    --color-success-500: #10b981;
    --color-success-600: #059669;
    --color-success-700: #047857;

    --color-warning-50: #fffbeb;
    --color-warning-500: #f59e0b;
    --color-warning-600: #d97706;

    --color-error-50: #fef2f2;
    --color-error-500: #ef4444;
    --color-error-600: #dc2626;
    --color-error-700: #b91c1c;

    --color-info-50: #eff6ff;
    --color-info-500: #3b82f6;
    --color-info-600: #2563eb;

    /* ===== TYPOGRAPHY ===== */
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

    /* Font sizes theo 8pt grid */
    --text-xs:   0.6875rem;   /* 11px */
    --text-sm:   0.8125rem;   /* 13px - body small */
    --text-base: 0.9375rem;   /* 15px - body default */
    --text-lg:   1.0625rem;   /* 17px */
    --text-xl:   1.25rem;     /* 20px */
    --text-2xl:  1.5rem;      /* 24px */
    --text-3xl:  1.875rem;     /* 30px */
    --text-4xl:  2.25rem;      /* 36px */

    /* Font weights */
    --font-normal:    400;
    --font-medium:   500;
    --font-semibold: 600;
    --font-bold:     700;

    /* Line heights */
    --leading-tight:  1.25;
    --leading-normal: 1.5;
    --leading-relaxed: 1.75;

    /* ===== SPACING ===== (8pt grid) */
    --space-1:  0.25rem;   /* 4px */
    --space-2:  0.5rem;    /* 8px */
    --space-3:  0.75rem;   /* 12px */
    --space-4:  1rem;      /* 16px */
    --space-5:  1.25rem;   /* 20px */
    --space-6:  1.5rem;    /* 24px */
    --space-8:  2rem;      /* 32px */
    --space-10: 2.5rem;     /* 40px */
    --space-12: 3rem;      /* 48px */
    --space-16: 4rem;       /* 64px */

    /* ===== RADIUS ===== */
    --radius-sm: 0.25rem;   /* 4px */
    --radius-md: 0.375rem;  /* 6px */
    --radius-lg: 0.5rem;    /* 8px */
    --radius-xl: 0.75rem;   /* 12px */
    --radius-2xl: 1rem;     /* 16px */
    --radius-full: 9999px;

    /* ===== SHADOWS ===== */
    /* Shadow nhẹ cho card trên nền sáng, shadow mạnh cho elevated elements */
    --shadow-xs:  0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-sm:  0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
    --shadow-md:  0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --shadow-lg:  0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
    --shadow-xl:  0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
    --shadow-inner: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);

    /* ===== TRANSITIONS ===== */
    --transition-fast:   150ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-normal: 250ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow:   350ms cubic-bezier(0.4, 0, 0.2, 1);

    /* ===== LAYOUT ===== */
    --sidebar-width:         260px;
    --sidebar-width-collapsed: 68px;
    --header-height:         60px;
    --footer-height:         40px;
    --content-max-width:     1400px;

    /* ===== Z-INDEX ===== */
    --z-base:     0;
    --z-dropdown: 100;
    --z-sticky:   200;
    --z-overlay:  300;
    --z-modal:    400;
    --z-toast:    500;
    --z-tooltip:  600;
}

/* ===== DARK MODE ===== */
[data-theme="dark"] {
    --color-gray-50:  #f9fafb;
    --color-gray-100: #f3f4f6;
    --color-gray-200: #e5e7eb;
    --color-gray-300: #d1d5db;
    --color-gray-400: #9ca3af;
    --color-gray-500: #6b7280;
    --color-gray-600: #4b5563;
    --color-gray-700: #374151;
    --color-gray-800: #1f2937;
    --color-gray-900: #111827;

    --bg-page:       #0f172a;
    --bg-surface:    #1e293b;
    --bg-elevated:   #334155;
    --bg-hover:      rgba(255, 255, 255, 0.05);
    --bg-active:     rgba(255, 255, 255, 0.08);

    --text-primary:   #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted:     #64748b;

    --border-default: #334155;
    --border-subtle:  #1e293b;

    --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.3);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.5);
}

/* ===== LIGHT MODE (default) ===== */
:root,
[data-theme="light"] {
    --bg-page:       #f8fafc;
    --bg-surface:    #ffffff;
    --bg-elevated:   #ffffff;
    --bg-hover:      #f1f5f9;
    --bg-active:     #e2e8f0;

    --text-primary:   #0f172a;
    --text-secondary: #475569;
    --text-muted:     #94a3b8;

    --border-default: #e2e8f0;
    --border-subtle:  #f1f5f9;
}
```

### 7.4 Component CSS - Buttons & Form Elements

Thiết kế button system hoàn chỉnh, bao gồm all states và variants.

```css
/* css/components/button.css */

/* ===== BUTTON SYSTEM ===== */
/* Button system dùng CSS custom properties composition,
   không phải utility-first thuần túy. Mỗi variant chỉ override
   những property cần thiết. */

.btn {
    /* Base styles */
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-2);

    /* Sizing */
    height: 2.25rem;          /* 36px - touch-friendly */
    padding: 0 var(--space-4);
    font-size: var(--text-sm);
    font-weight: var(--font-medium);
    line-height: 1;

    /* Shape & Border */
    border-radius: var(--radius-md);
    border: 1px solid transparent;
    cursor: pointer;
    white-space: nowrap;

    /* Transitions */
    transition: all var(--transition-fast);
    outline: none;

    /* Focus ring - phải visible cho accessibility */
    &:focus-visible {
        box-shadow: 0 0 0 3px var(--color-brand-200);
    }

    /* Disabled state */
    &:disabled,
    &[aria-disabled="true"] {
        opacity: 0.5;
        cursor: not-allowed;
        pointer-events: none;
    }

    /* Sizes */
    &--sm {
        height: 1.75rem;     /* 28px */
        padding: 0 var(--space-3);
        font-size: var(--text-xs);
        border-radius: var(--radius-sm);
    }

    &--lg {
        height: 2.75rem;     /* 44px */
        padding: 0 var(--space-6);
        font-size: var(--text-base);
    }

    /* Primary variant - brand color fill */
    &--primary {
        background-color: var(--color-brand-500);
        color: white;
        border-color: var(--color-brand-500);

        &:hover:not(:disabled) {
            background-color: var(--color-brand-600);
            border-color: var(--color-brand-600);
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }

        &:active:not(:disabled) {
            background-color: var(--color-brand-700);
            transform: translateY(0);
            box-shadow: var(--shadow-sm);
        }
    }

    /* Secondary variant - outline style */
    &--secondary {
        background-color: transparent;
        color: var(--text-primary);
        border-color: var(--border-default);

        &:hover:not(:disabled) {
            background-color: var(--bg-hover);
            border-color: var(--color-gray-400);
        }

        &:active:not(:disabled) {
            background-color: var(--bg-active);
        }
    }

    /* Ghost variant - chỉ có text, không border */
    &--ghost {
        background-color: transparent;
        color: var(--text-secondary);
        border-color: transparent;

        &:hover:not(:disabled) {
            background-color: var(--bg-hover);
            color: var(--text-primary);
        }
    }

    /* Danger variant */
    &--danger {
        background-color: var(--color-error-500);
        color: white;
        border-color: var(--color-error-500);

        &:hover:not(:disabled) {
            background-color: var(--color-error-600);
            border-color: var(--color-error-600);
        }
    }

    /* Icon button (square) */
    &--icon {
        width: 2.25rem;
        padding: 0;

        &.btn--sm { width: 1.75rem; }
        &.btn--lg { width: 2.75rem; }
    }

    /* Loading state - spinner replaces content */
    &--loading {
        position: relative;
        color: transparent !important;
        pointer-events: none;

        &::after {
            content: '';
            position: absolute;
            width: 1rem;
            height: 1rem;
            border: 2px solid currentColor;
            border-right-color: transparent;
            border-radius: 50%;
            animation: spin 0.6s linear infinite;
        }
    }
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* ===== INPUT SYSTEM ===== */
.input {
    display: block;
    width: 100%;
    height: 2.25rem;
    padding: 0 var(--space-3);
    font-size: var(--text-sm);
    color: var(--text-primary);
    background-color: var(--bg-surface);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-md);
    transition: border-color var(--transition-fast), box-shadow var(--transition-fast);

    &::placeholder {
        color: var(--text-muted);
    }

    &:hover:not(:disabled):not(:focus) {
        border-color: var(--color-gray-400);
    }

    &:focus {
        outline: none;
        border-color: var(--color-brand-500);
        box-shadow: 0 0 0 3px var(--color-brand-100);
    }

    &:disabled {
        background-color: var(--bg-hover);
        cursor: not-allowed;
        opacity: 0.6;
    }

    /* Error state */
    &--error {
        border-color: var(--color-error-500);

        &:focus {
            box-shadow: 0 0 0 3px var(--color-error-100);
        }
    }

    /* With icon */
    &--with-icon {
        padding-left: 2.5rem;

        ~ .input-icon {
            left: var(--space-3);
            color: var(--text-muted);
        }
    }
}

/* Input label */
.form-label {
    display: block;
    margin-bottom: var(--space-2);
    font-size: var(--text-sm);
    font-weight: var(--font-medium);
    color: var(--text-primary);
}

.form-hint {
    margin-top: var(--space-1);
    font-size: var(--text-xs);
    color: var(--text-muted);
}

.form-error {
    margin-top: var(--space-1);
    font-size: var(--text-xs);
    color: var(--color-error-600);
    display: flex;
    align-items: center;
    gap: var(--space-1);
}
```

### 7.5 Dashboard Page - Real Data Display

Một trang dashboard thực tế hiển thị KPI cards, chart placeholder, và data table.

```cshtml
@* Areas/Admin/Pages/Dashboard/Index.cshtml *@
@page
@model IndexModel
@{
    Layout = "~/Views/Shared/_Layout.cshtml";
    ViewData["Title"] = "Dashboard";
    ViewData["Description"] = "Overview of your store performance";
}

@section Styles {
    <link rel="stylesheet" href="~/css/pages/dashboard.css" />
    <link rel="stylesheet" href="~/lib/chart.js/chart.min.css" />
}

<div class="page-header">
    <div class="page-header__content">
        <h1 class="page-header__title">@Localizer["Dashboard"]</h1>
        <p class="page-header__subtitle">
            @Localizer["Welcome back"], @User.Identity?.Name
            &middot; @DateTime.Today.ToString("dddd, MMMM d, yyyy")
        </p>
    </div>
    <div class="page-header__actions">
        <select class="input input--sm" style="width: auto;" asp-for="DateRange"
                asp-items="Model.DateRangeOptions"
                onchange="this.form.submit()">
        </select>
        <button class="btn btn--secondary btn--sm" onclick="exportDashboard()">
            <i data-feather="download"></i>
            @Localizer["Export"]
        </button>
    </div>
</div>

@* ===== KPI CARDS ===== *@
<section class="kpi-grid" aria-label="Key performance indicators">
    <article class="kpi-card kpi-card--revenue">
        <div class="kpi-card__header">
            <span class="kpi-card__label">@Localizer["Total Revenue"]</span>
            <span class="kpi-card__period">@Model.DateRange</span>
        </div>
        <div class="kpi-card__body">
            <span class="kpi-card__value">@Model.Revenue.ToString("C0", Model.CurrencyFormat)</span>
            <span class="kpi-card__change kpi-card__change--up">
                <i data-feather="trending-up"></i>
                +@Model.RevenueChange.ToString("P1")
            </span>
        </div>
        <div class="kpi-card__sparkline">
            <canvas id="revenueSparkline" width="120" height="40"></canvas>
        </div>
    </article>

    <article class="kpi-card kpi-card--orders">
        <div class="kpi-card__header">
            <span class="kpi-card__label">@Localizer["Total Orders"]</span>
        </div>
        <div class="kpi-card__body">
            <span class="kpi-card__value">@Model.TotalOrders.ToString("N0")</span>
            <span class="kpi-card__change @(Model.OrdersChange >= 0 ? "kpi-card__change--up" : "kpi-card__change--down")">
                <i data-feather="@(Model.OrdersChange >= 0 ? "trending-up" : "trending-down")"></i>
                @Model.OrdersChange.ToString("P1")
            </span>
        </div>
    </article>

    <article class="kpi-card kpi-card--customers">
        <div class="kpi-card__header">
            <span class="kpi-card__label">@Localizer["New Customers"]</span>
        </div>
        <div class="kpi-card__body">
            <span class="kpi-card__value">@Model.NewCustomers.ToString("N0")</span>
            <span class="kpi-card__change kpi-card__change--up">
                <i data-feather="trending-up"></i>
                +@Model.CustomersChange.ToString("P1")
            </span>
        </div>
    </article>

    <article class="kpi-card kpi-card--conversion">
        <div class="kpi-card__header">
            <span class="kpi-card__label">@Localizer["Conversion Rate"]</span>
        </div>
        <div class="kpi-card__body">
            <span class="kpi-card__value">@Model.ConversionRate.ToString("P1")</span>
            <span class="kpi-card__change kpi-card__change--down">
                <i data-feather="trending-down"></i>
                -@Model.ConversionChange.ToString("P1")
            </span>
        </div>
    </article>
</section>

@* ===== CHARTS ROW ===== *@
<section class="charts-grid">
    <div class="chart-card">
        <div class="chart-card__header">
            <h2 class="chart-card__title">@Localizer["Revenue Overview"]</h2>
            <div class="chart-card__legend">
                <span class="chart-legend__item chart-legend__item--actual">Actual</span>
                <span class="chart-legend__item chart-legend__item--projected">Projected</span>
            </div>
        </div>
        <div class="chart-card__body">
            <canvas id="revenueChart" role="img" aria-label="Revenue chart"></canvas>
        </div>
    </div>

    <div class="chart-card">
        <div class="chart-card__header">
            <h2 class="chart-card__title">@Localizer["Orders by Status"]</h2>
        </div>
        <div class="chart-card__body chart-card__body--doughnut">
            <canvas id="ordersDoughnutChart" role="img" aria-label="Orders by status"></canvas>
        </div>
    </div>
</section>

@* ===== RECENT ORDERS TABLE ===== *@
<section class="data-section">
    <div class="data-section__header">
        <h2 class="data-section__title">@Localizer["Recent Orders"]</h2>
        <a href="/admin/orders" class="btn btn--ghost btn--sm">
            @Localizer["View all"]
            <i data-feather="arrow-right"></i>
        </a>
    </div>

    <div class="data-table-wrapper">
        <table class="data-table" role="grid" aria-label="Recent orders">
            <thead>
                <tr>
                    <th scope="col" class="data-table__th data-table__th--sortable" data-sort="orderNumber">
                        @Localizer["Order"]
                        <i data-feather="chevrons-up-down" class="sort-icon"></i>
                    </th>
                    <th scope="col" class="data-table__th">@Localizer["Customer"]</th>
                    <th scope="col" class="data-table__th data-table__th--sortable" data-sort="createdAt">
                        @Localizer["Date"]
                        <i data-feather="chevrons-up-down" class="sort-icon"></i>
                    </th>
                    <th scope="col" class="data-table__th data-table__th--sortable text-right" data-sort="total">
                        @Localizer["Total"]
                        <i data-feather="chevrons-up-down" class="sort-icon"></i>
                    </th>
                    <th scope="col" class="data-table__th data-table__th--sortable" data-sort="status">
                        @Localizer["Status"]
                        <i data-feather="chevrons-up-down" class="sort-icon"></i>
                    </th>
                    <th scope="col" class="data-table__th data-table__th--actions">
                        <span class="sr-only">@Localizer["Actions"]</span>
                    </th>
                </tr>
            </thead>
            <tbody>
                @foreach (var order in Model.RecentOrders)
                {
                    <tr class="data-table__row" onclick="location.href='/admin/orders/@order.Id'">
                        <td class="data-table__td">
                            <span class="order-number">@order.OrderNumber</span>
                        </td>
                        <td class="data-table__td">
                            <div class="customer-cell">
                                <img src="https://i.pravatar.cc/32?u=@order.CustomerId"
                                     alt=""
                                     class="customer-cell__avatar"
                                     loading="lazy" />
                                <span>@order.CustomerName</span>
                            </div>
                        </td>
                        <td class="data-table__td">
                            <time datetime="@order.CreatedAt.ToString("o")">
                                @order.CreatedAt.ToString("MMM d, HH:mm")
                            </time>
                        </td>
                        <td class="data-table__td text-right font-mono">
                            @order.Total.ToString("C", Model.CurrencyFormat)
                        </td>
                        <td class="data-table__td">
                            <span class="status-badge status-badge--@order.Status.ToLower()">
                                @Localizer[order.Status]
                            </span>
                        </td>
                        <td class="data-table__td data-table__td--actions">
                            <div class="table-actions">
                                <a href="/admin/orders/@order.Id"
                                   class="btn btn--ghost btn--icon btn--sm"
                                   title="@Localizer["View details"]">
                                    <i data-feather="eye"></i>
                                </a>
                                <button class="btn btn--ghost btn--icon btn--sm"
                                        title="@Localizer["More options"]"
                                        aria-haspopup="true">
                                    <i data-feather="more-horizontal"></i>
                                </button>
                            </div>
                        </td>
                    </tr>
                }
            </tbody>
        </table>
    </div>

    @await Component.InvokeAsync("Pagination", new {
        CurrentPage = Model.OrdersPage,
        TotalPages = Model.TotalOrdersPages,
        PageSize = 10
    })
</section>

@section Scripts {
    <script src="~/lib/chart.js/chart.umd.min.js"></script>
    <script src="~/js/pages/dashboard.js" type="module"></script>
}
```

### 7.6 Status Badge Component

Component nhỏ nhưng quan trọng - hiển thị trạng thái đơn hàng với màu sắc có ý nghĩa.

```css
/* css/components/badge.css */

/* Status badge - semantic color mapping */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-1);

    padding: 0.2rem var(--space-2);
    font-size: var(--text-xs);
    font-weight: var(--font-medium);
    line-height: 1.4;
    border-radius: var(--radius-full);

    /* Pending: vàng nhạt - chờ xử lý */
    &--pending {
        background-color: #fef3c7;
        color: #92400e;
    }

    &--processing {
        background-color: #dbeafe;
        color: #1e40af;
    }

    /* Paid/Completed: xanh lá - thành công */
    &--paid,
    &--completed,
    &--delivered {
        background-color: #d1fae5;
        color: #065f46;
    }

    /* Shipped: xanh dương nhạt - đang vận chuyển */
    &--shipped {
        background-color: #e0f2fe;
        color: #075985;
    }

    /* Cancelled: đỏ nhạt - thất bại/đã hủy */
    &--cancelled,
    &--failed,
    &--refunded {
        background-color: #fee2e2;
        color: #991b1b;
    }

    /* On hold: xám - tạm dừng */
    &--on-hold {
        background-color: #f3f4f6;
        color: #374151;
    }
}

/* Dark mode variants */
[data-theme="dark"] .status-badge {
    &--pending { background-color: #78350f; color: #fef3c7; }
    &--paid, &--completed { background-color: #064e3b; color: #d1fae5; }
    &--cancelled { background-color: #7f1d1d; color: #fee2e2; }
    &--on-hold { background-color: #1f2937; color: #d1d5db; }
}
```

### 7.7 Responsive Design Breakpoints

Hệ thống breakpoints thực tế, không phải mobile-first generic.

```css
/* css/layouts/_responsive.css */

/* Breakpoints theo device categories thực tế:
   - Mobile: < 640px
   - Tablet: 640px - 1024px
   - Desktop: 1024px - 1280px
   - Wide: > 1280px */

/* ===== SIDEBAR RESPONSIVE ===== */
@media (max-width: 1024px) {
    .sidebar {
        position: fixed;
        top: 0;
        left: 0;
        z-index: var(--z-modal);
        transform: translateX(-100%);
        transition: transform var(--transition-normal);

        &--open {
            transform: translateX(0);
        }

        &--collapsed {
            width: var(--sidebar-width); /* Collapsed chỉ trên desktop */
        }
    }

    .app-container {
        margin-left: 0;
    }
}

/* ===== TABLE RESPONSIVE ===== */
@media (max-width: 768px) {
    .data-table {
        font-size: var(--text-xs);

        /* Ẩn columns không thiết yếu trên mobile */
        .data-table__th:nth-child(3),  /* Date */
        .data-table__td:nth-child(3) {
            display: none;
        }
    }

    .kpi-grid {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 480px) {
    .kpi-grid {
        grid-template-columns: 1fr;
    }

    .charts-grid {
        grid-template-columns: 1fr;
    }

    .page-header__actions {
        flex-direction: column;
        align-items: stretch;
    }
}
```

### 7.8 API Service Layer (Frontend)

```typescript
// wwwroot/js/services/api.service.ts
// Typed API client - tất cả requests đi qua đây

interface ApiResponse<T> {
  data: T;
  error?: { code: string; message: string };
  meta?: { page: number; total: number; pageSize: number };
}

interface OrderSummary {
  id: string;
  orderNumber: string;
  customerName: string;
  total: number;
  status: string;
  createdAt: string;
}

class ApiService {
  private baseUrl: string;
  private defaultHeaders: Record<string, string>;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    };
  }

  private async request<T>(
    method: string,
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`;
    const token = document
      .querySelector('meta[name="csrf-token"]')
      ?.getAttribute('content');

    const headers: Record<string, string> = {
      ...this.defaultHeaders,
      ...(token ? { 'X-CSRF-TOKEN': token } : {}),
      ...(options.headers as Record<string, string>),
    };

    try {
      const response = await fetch(url, {
        method,
        credentials: 'same-origin',
        headers,
        body: options.body ? JSON.stringify(options.body) : undefined,
      });

      if (!response.ok) {
        const errorBody = await response.json().catch(() => ({}));
        throw new ApiError(
          response.status,
          errorBody.error?.code ?? 'UNKNOWN_ERROR',
          errorBody.error?.message ?? response.statusText
        );
      }

      if (response.status === 204) {
        return { data: null as unknown as T };
      }

      return await response.json();
    } catch (err) {
      if (err instanceof ApiError) throw err;
      throw new ApiError(0, 'NETWORK_ERROR', 'Network request failed');
    }
  }

  // Orders API
  async getOrders(params: {
    page?: number;
    pageSize?: number;
    status?: string;
    search?: string;
  }): Promise<ApiResponse<OrderSummary[]>> {
    const query = new URLSearchParams(
      Object.fromEntries(Object.entries(params).filter(([, v]) => v !== undefined))
    );
    return this.request<OrderSummary[]>(
      'GET',
      `/api/admin/orders?${query}`
    );
  }

  async getOrder(id: string): Promise<ApiResponse<OrderDetailDto>> {
    return this.request<OrderDetailDto>('GET', `/api/admin/orders/${id}`);
  }

  async createOrder(payload: CreateOrderRequest): Promise<ApiResponse<OrderDto>> {
    return this.request<OrderDto>('POST', '/api/admin/orders', {
      body: payload,
    });
  }
}

class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly code: string,
    public readonly message: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export const api = new ApiService('/api');
```

### 7.9 Modal Component - Production Pattern

```cshtml
@* Views/Shared/Components/Modal/Default.cshtml *@
@model ModalViewModel

<div class="modal-overlay"
     id="@Model.Id"
     role="dialog"
     aria-modal="true"
     aria-labelledby="@(Model.Id)-title"
     x-data="{ open: false }"
     x-init="$nextTick(() => { window.addEventListener('open-modal-@Model.Id', () => { open = true; document.body.style.overflow = 'hidden'; }); })"
     @* Trigger close via custom event *@
     @* Usage: window.dispatchEvent(new CustomEvent('open-modal-@Model.Id')) *@
     x-show="open"
     x-transition:enter="modal-enter"
     x-transition:enter-start="modal-enter-start"
     x-transition:enter-end="modal-enter-end"
     x-transition:leave="modal-leave"
     x-transition:leave-start="modal-leave-start"
     x-transition:leave-end="modal-leave-end">

    <div class="modal-panel modal-panel--@Model.Size"
         @@click.stop
         x-on:click.outside="open = false; document.body.style.overflow = ''">

        @if (Model.ShowHeader)
        {
            <div class="modal-panel__header">
                <h2 id="@(Model.Id)-title" class="modal-panel__title">
                    @Model.Title
                </h2>
                <button class="btn btn--ghost btn--icon btn--sm modal-panel__close"
                        @@click="open = false; document.body.style.overflow = ''"
                        aria-label="@Localizer["Close"]">
                    <i data-feather="x"></i>
                </button>
            </div>
        }

        <div class="modal-panel__body">
            @await RenderBodyAsync()
        </div>

        @if (Model.ShowFooter)
        {
            <div class="modal-panel__footer">
                @await RenderSectionAsync("Footer", required: false)
            </div>
        }
    </div>
</div>
```

### 7.10 Anti-Patterns - UI do AI tạo thường mắc phải

Dưới đây là những dấu hiệu nhận biết giao diện do AI tạo, cần tránh:

| Dấu hiệu AI-generated | Thực tế production |
|---|---|
| Dùng system-ui font mặc định | Inter, SF Pro, Roboto từ Google Fonts |
| Màu primary cứng `#007bff` cho mọi thứ | Brand color system với semantic naming |
| Button chỉ có 2 states (enabled/disabled) | 5 states: default, hover, active, focus, loading, disabled |
| Spacing random `margin: 10px` | 8pt grid system với scale nhất quán |
| Box-shadow mờ nhạt hoặc không có | Shadow system分层 (sm/md/lg/xl) |
| Không có border-radius hoặc `border-radius: 0` | Consistent border-radius scale |
| Màu text trắng/đen cứng | Semantic text colors (primary/secondary/muted) |
| Table không có pagination, sort, hover states | Full data table với sort, pagination, row selection |
| Toast notification đơn giản | Multi-type, auto-dismiss, action buttons, stacking |
| Responsive đơn giản hoặc không có | 4-6 breakpoints với layout adaptations |
| CSS không có variables | Full CSS custom properties system |
| Hard-coded colors everywhere | Design tokens composition |
| Font sizes random | Type scale consistent |
| Animation đơn giản hoặc không có | Meaningful micro-interactions với proper easing |

### 7.11 Quy trình thiết kế UI thực tế

1. **Design Tokens trước**: Định nghĩa color palette, typography scale, spacing grid, shadows trước khi code bất kỳ component nào
2. **Component API Design**: Mỗi component cần rõ inputs (props), outputs (events), và states
3. **Composition over Configuration**: Layouts được compose từ components nhỏ, không phải ngược lại
4. **Accessibility từ đầu**: ARIA labels, keyboard navigation, focus management, color contrast
5. **Dark mode-first**: Implement dark mode bằng CSS variables từ đầu, không phải sau
6. **Performance Budgeting**: Lazy load images, code-split routes, preload critical fonts
- [CQRS Pattern - Microsoft](https://docs.microsoft.com/en-us/azure/architecture/patterns/cqrs)
- [Vertical Slice Architecture - Jimmy Bogard](https://jimmybogard.com/vertical-slice-architecture/)
- [Event-Driven Architecture - Martin Fowler](https://martinfowler.com/articles/201701-event-driven.html)
- [MediatR Documentation](https://github.com/jbogard/MediatR)
- [ASP.NET Core Best Practices](./best-practice.md)
- [Domain-Driven Design](./ddd.md)
