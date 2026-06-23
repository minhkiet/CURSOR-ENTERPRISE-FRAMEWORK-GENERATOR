# ASP.NET Core Glossary - Từ Điển Thuật Ngữ

## Giới thiệu

Tài liệu này cung cấp các thuật ngữ chuyên ngành ASP.NET Core framework.

## Các thuật ngữ cơ bản

### 1. Middleware

Middleware là các components được pipeline để xử lý requests và responses. Mỗi middleware có thể short-circuit pipeline, pass to next, hoặc modify response. Examples: Authentication, Authorization, Routing, CORS.

### 2. Razor Pages

Razor Pages là page-based model cho ASP.NET Core, đơn giản hơn MVC. Pages có @page directive và code-behind file. Good cho simple pages.

### 3. MVC Pattern

Model-View-Controller pattern với Controllers, Views, Models. Routes map to controller actions. Views render HTML using Razor syntax.

### 4. Dependency Injection

ASP.NET Core có built-in DI container. Register services in Program.cs. Inject dependencies via constructor.

### 5. Entity Framework Core

EF Core là lightweight ORM cho .NET. Supports migrations, relationships, LINQ queries. Multiple database providers.

### 6. Web API

ASP.NET Core Web API cho building REST APIs. Controllers return IActionResult hoặc typed results. JSON serialization. OpenAPI/Swagger support.

### 7. SignalR

SignalR là library cho real-time web communication. Server-to-client push. WebSocket fallback. Groups và hubs.

### 8. Blazor

Blazor là framework cho building interactive UIs với .NET. Blazor Server (real-time) và Blazor WebAssembly (client-side).

### 9. Minimal APIs

Minimal APIs là lightweight API approach với minimal boilerplate. Map handlers directly to routes. Good cho microservices.

### 10. gRPC

gRPC là high-performance RPC framework. Uses Protocol Buffers. Great cho microservices communication.

### 11. Configuration

Configuration system hỗ trợ multiple sources: JSON files, environment variables, secrets. Strongly-typed options pattern.

### 12. Logging

Built-in logging framework với multiple providers. ILogger interface. Structured logging support.

### 13. Health Checks

Health check endpoints cho monitoring. Uptime checks, database connectivity. ASP.NET Core health checks middleware.

### 14. Rate Limiting

Rate limiting middleware giới hạn requests. Fixed window, sliding window, token bucket algorithms.

### 15. CORS

Cross-Origin Resource Sharing configuration. Allow specific origins, methods, headers.

### 16. Authentication

ASP.NET Core Identity, JWT Bearer, OAuth. Cookie-based authentication. External providers.

### 17. Authorization

Policy-based authorization. Roles, claims, resource-based. RequireAuthorize attribute.

### 18. Background Services

IHostedService interface cho background tasks. BackgroundService base class. Queued background tasks.

### 19. Caching

In-memory caching, distributed caching (Redis). Response caching middleware. Cache headers.

### 20. Testing

xUnit, NUnit, MSTest. Integration tests với WebApplicationFactory. Unit tests với mocks.

## Kết luận

Từ điển này cung cấp nền tảng về ASP.NET Core concepts.
