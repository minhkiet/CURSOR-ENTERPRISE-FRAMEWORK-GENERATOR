---
name: fullstack-web-development
description: Build, modify, debug fullstack web apps using ASP.NET Core Web API, React + TypeScript + TSX, existing project database, REST API, and JWT authentication. Enforces end-to-end data flow (React UI -> API Service -> Controller -> Service -> Data Access -> DB -> Response -> State -> UI), 30 strict engineering rules, 17-point verification checklist, token efficiency, anti-patterns, and zero-breaking-changes safety.
triggers:
  - fullstack
  - fullstack web
  - asp.net core react
  - dotnet react
  - react typescript dotnet
  - build fullstack
  - web api react
  - fullstack-web-development
  - /fullstack
category: Development
version: 1.0.0
---

# FULLSTACK WEB DEVELOPMENT SKILL

> **Domain:** ASP.NET Core Web API + React + TypeScript + TSX  
> **Architecture:** Clean End-to-End RESTful Architecture  
> **Philosophy:** Correctness > Existing functionality > Security > Maintainability > Performance > Simplicity > Token efficiency

---

## PURPOSE

Build, modify, and debug fullstack web applications using:
- **Backend:** ASP.NET Core Web API (C#)
- **Frontend:** React + TypeScript + TSX
- **Database:** Existing project database (SQL Server, PostgreSQL, MySQL, SQLite, etc.)
- **API:** RESTful HTTP conventions with structured JSON envelopes
- **Auth:** JWT (JSON Web Token) / Role & Policy Authorization when required

### The Unbreakable End-to-End Goal

Every fullstack feature must execute cleanly through the complete 9-stage pipeline:

```text
React UI
  └──▶ API Service
        └──▶ ASP.NET Core Controller
              └──▶ Application Service
                    └──▶ Data Access / Repository
                          └──▶ Database
                    ◀─── Database Result
              ◀─── Service DTO
        ◀─── API Response (Envelope)
  ◀─── React State Update
UI Re-renders with Real Data
```

### Priority Hierarchy

When balancing competing concerns, resolve strictly in this order:

```text
1. Correctness (Must function correctly according to business rules)
   > 2. Existing functionality (Never break working features)
      > 3. Security (Never compromise auth, data privacy, or input safety)
         > 4. Maintainability (Clean, readable, idiomatic code)
            > 5. Performance (Optimize where necessary, no premature optimization)
               > 6. Simplicity (YAGNI, minimal abstractions)
                  > 7. Token efficiency (Targeted edits, focused context)
```

---

## 01. PROJECT ANALYSIS

**Before writing or modifying any code, complete these 10 inspection steps:**

1. **Inspect project structure:** Locate root solutions (`.sln`), `.csproj` files, `package.json`, and source folders.
2. **Identify Backend:** Framework version (.NET 8/9), hosting model, middleware pipeline, DI setup in `Program.cs`.
3. **Identify Frontend:** Bundler (Vite, Next.js, CRA), styling (Tailwind, CSS modules, MUI, shadcn), router (React Router v6/v7).
4. **Identify Database:** ORM (EF Core, Dapper, ADO.NET), connection strings in `appsettings.json`, existing migrations or schema scripts.
5. **Identify API layer:** Controller routes, API versioning, base URLs, swagger/OpenAPI definitions.
6. **Identify Authentication:** JWT bearer config, token storage (cookie vs localStorage), claims transformation, auth handlers.
7. **Identify Existing Components:** UI library, shared inputs, modals, layouts, design tokens.
8. **Identify Existing Services:** HTTP clients (Axios instance, fetch wrapper), query libraries (TanStack Query, RTK Query, custom hooks).
9. **Identify Reusable Code:** Extension methods, DTO mappers, validation helpers, utility functions.
10. **Identify Files Requiring Changes:** Build an exact list of files to touch before writing a single line.

> [!IMPORTANT]
> **Strict Guardrails:**
> - Never guess existing architecture. If you cannot find a file, locate it via tools.
> - Never rewrite working code without explicit justification.
> - Prefer the smallest safe change that delivers complete functionality.

---

## 02. BACKEND ARCHITECTURE (ASP.NET CORE WEB API)

The Backend is the single source of truth for business integrity.

### Backend Responsibility Boundaries
Backend owns:
- Business logic & domain invariants
- Data processing & calculations
- Authoritative validation
- Authentication & Authorization
- CRUD operations & transactions
- Database access & schema mapping
- External API integrations
- File uploads, streaming, and processing
- Structured logging & telemetry
- Global error handling & sanitization

### Preferred Backend Structure

```text
Backend/
├── Controllers/         # HTTP endpoints & action results only
├── Services/            # Business logic implementations
├── Interfaces/          # Service & repository contracts
├── DTOs/                # Request & Response Data Transfer Objects
│   ├── Requests/        # Incoming payload definitions
│   └── Responses/       # Outgoing payload definitions
├── Models/              # Domain models & business aggregates
├── Entities/            # Database schema entities
├── Repositories/        # Data access abstraction (when used)
├── Data/                # DbContext, migrations, Dapper contexts
├── Middleware/          # Global exception handling, correlation IDs
├── Extensions/          # ServiceCollection and IApplicationBuilder extensions
├── Helpers/             # Mappers, formatters, cryptography helpers
├── Validators/          # FluentValidation or custom validators
├── Configuration/       # Strongly typed options classes
└── Program.cs           # Host building, DI registration, pipeline configuration
```

> [!TIP]
> Create only required folders. Do not introduce empty layers or unnecessary abstraction without concrete necessity.

---

## 03. CONTROLLERS

Controllers are HTTP adapters—they map HTTP requests to application services and return appropriate HTTP status codes.

### Controller Rules
- Do NOT place database queries or business rules inside Controllers.
- Always use `[ApiController]` and explicit route templates.
- Always return typed `ActionResult<ApiResponse<T>>` or `IActionResult`.
- Always use DTOs for request and response payloads.
- **NEVER** expose raw database entities directly to the client.

### Standard REST Endpoints Pattern

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly IProductService _productService;
    private readonly ILogger<ProductsController> _logger;

    public ProductsController(IProductService productService, ILogger<ProductsController> logger)
    {
        _productService = productService;
        _logger = logger;
    }

    [HttpGet]
    public async Task<ActionResult<ApiResponse<PagedResult<ProductResponseDto>>>> GetPaged(
        [FromQuery] ProductFilterRequest request, 
        CancellationToken cancellationToken)
    {
        var result = await _productService.GetPagedAsync(request, cancellationToken);
        return Ok(ApiResponse<PagedResult<ProductResponseDto>>.Ok(result));
    }

    [HttpGet("{id:guid}")]
    public async Task<ActionResult<ApiResponse<ProductResponseDto>>> GetById(
        Guid id, 
        CancellationToken cancellationToken)
    {
        var product = await _productService.GetByIdAsync(id, cancellationToken);
        if (product == null)
            return NotFound(ApiResponse<ProductResponseDto>.Fail("Product not found", 404));

        return Ok(ApiResponse<ProductResponseDto>.Ok(product));
    }

    [HttpPost]
    public async Task<ActionResult<ApiResponse<ProductResponseDto>>> Create(
        [FromBody] CreateProductRequest request, 
        CancellationToken cancellationToken)
    {
        var created = await _productService.CreateAsync(request, cancellationToken);
        return CreatedAtAction(
            nameof(GetById), 
            new { id = created.Id }, 
            ApiResponse<ProductResponseDto>.Ok(created, "Product created successfully"));
    }

    [HttpPut("{id:guid}")]
    public async Task<ActionResult<ApiResponse<ProductResponseDto>>> Update(
        Guid id, 
        [FromBody] UpdateProductRequest request, 
        CancellationToken cancellationToken)
    {
        var updated = await _productService.UpdateAsync(id, request, cancellationToken);
        return Ok(ApiResponse<ProductResponseDto>.Ok(updated, "Product updated successfully"));
    }

    [HttpDelete("{id:guid}")]
    public async Task<ActionResult<ApiResponse<bool>>> Delete(
        Guid id, 
        CancellationToken cancellationToken)
    {
        await _productService.DeleteAsync(id, cancellationToken);
        return Ok(ApiResponse<bool>.Ok(true, "Product deleted successfully"));
    }
}
```

---

## 04. API AUTHENTICATION & AUTHORIZATION

### Endpoint Security Classification
Every endpoint must belong to one of four access tiers:
1. **Public:** No token required (`[AllowAnonymous]`) - e.g., Login, Register, Public Catalog.
2. **Authenticated:** Valid JWT required (`[Authorize]`) - e.g., User Profile, Orders History.
3. **Authorized / Permissioned:** Specific claims/roles required (`[Authorize(Roles = "Manager")]` or `[Authorize(Policy = "CanEditProducts")]`).
4. **Admin:** Superuser access only (`[Authorize(Roles = "Admin")]`).

### JWT Flow Protocol

```text
1. Client POSTs credentials to /api/auth/login
2. Server validates password hash + MFA -> issues Access Token + Refresh Token
3. Client stores Access Token (memory/state) and sends:
   Authorization: Bearer <access_token>
4. ASP.NET Core JwtBearerMiddleware validates signature, issuer, audience, and expiry
5. ClaimsPrincipal injected into HttpContext.User
6. Endpoint checks [Authorize] policies
```

### Secret Protection Rule
**NEVER hardcode:**
- JWT Secret keys
- API Keys
- Database passwords
- OAuth client secrets
- Private encryption certificates

Store all secrets in environment variables, `appsettings.Development.json` (gitignored), or secret managers (User Secrets / Azure Key Vault).

---

## 05. HTTP STATUS CODES & RESPONSE ENVELOPES

Use exact, semantic HTTP status codes:

| Code | Meaning | When to Use |
|------|---------|-------------|
| `200 OK` | Request succeeded | Standard GET, PUT, or POST returning data |
| `201 Created` | Resource created | Successful POST creating a new entity (include Location header) |
| `204 No Content` | Succeeded without body | Successful DELETE or PUT with no payload to return |
| `400 Bad Request` | Client malformed request | Validation failure, invalid parameters, malformed JSON |
| `401 Unauthorized` | Missing/Invalid Token | Unauthenticated access or expired token |
| `403 Forbidden` | Authenticated but unauthorized | User lacks required role, permission, or resource ownership |
| `404 Not Found` | Resource does not exist | Entity with specified ID does not exist |
| `409 Conflict` | State conflict | Duplicate email/username, concurrency violation |
| `422 Unprocessable` | Semantic validation failed | Well-formed JSON but fails domain invariants |
| `500 Server Error` | Unexpected failure | Unhandled server exception (sanitized in production) |

### Standard Response Envelope

```csharp
public class ApiResponse<T>
{
    public bool Success { get; set; }
    public string Message { get; set; } = string.Empty;
    public T? Data { get; set; }
    public IDictionary<string, string[]>? Errors { get; set; }
    public int StatusCode { get; set; }

    public static ApiResponse<T> Ok(T data, string message = "Success", int statusCode = 200) =>
        new() { Success = true, Message = message, Data = data, StatusCode = statusCode };

    public static ApiResponse<T> Fail(string message, int statusCode = 400, IDictionary<string, string[]>? errors = null) =>
        new() { Success = false, Message = message, StatusCode = statusCode, Errors = errors };
}
```

---

## 06. VALIDATION ARCHITECTURE

### The Authority Rule
- **Backend validation is authoritative and mandatory.**
- **Frontend validation exists solely for user experience and responsiveness.**
- **NEVER trust client-side validation alone.**

### Validation Checklist
- [ ] Required fields present
- [ ] Correct primitive types & bounds
- [ ] String length (min/max)
- [ ] Numeric and date ranges
- [ ] Format rules (Email, phone, URL, slug, regex)
- [ ] Business invariants (e.g., StartDate < EndDate, unique SKU)
- [ ] Authorization limits (e.g., cannot transfer more than account balance)
- [ ] Never expose raw exception stack traces in validation error responses

---

## 07. DATABASE & PERSISTENCE

### Strict Layer Separation
Maintain clean separation across the data pipeline:
- **Entity:** Represents database table structure (`Entities/Product.cs`)
- **DTO:** Represents API contract (`DTOs/ProductResponseDto.cs`)
- **Data Access:** DbContext / SQL Queries (`Data/ApplicationDbContext.cs`)
- **Service:** Business coordination & mapping (`Services/ProductService.cs`)
- **Controller:** HTTP serialization & status codes (`Controllers/ProductsController.cs`)

### Persistence Rules
- Prefer existing database technology (do not switch from EF Core to Dapper or vice versa without approval).
- Do not modify database schemas unless explicitly required by the feature.
- Avoid ad-hoc migrations; review generated migration code before applying.
- Always optimize queries:
  - Use `AsNoTracking()` for read-only queries in EF Core.
  - Avoid N+1 queries by using `.Include()` or explicit projections (`.Select()`).
  - Always enforce pagination (`Take` / `Skip` or keyset pagination) on collection endpoints.
  - Never load entire tables into application memory.

---

## 08. FRONTEND ARCHITECTURE (REACT + TYPESCRIPT + TSX)

Frontend is responsible for user interaction, layout, client routing, and state orchestration.

### Frontend Responsibility Boundaries
Frontend owns:
- Component rendering & user experience
- Client-side navigation & route guards
- Form state, controlled inputs, and client validation
- API communication, loading, and error states
- Authentication token lifecycle & user session state
- Responsive layouts & cross-browser styling
- Optimistic updates & UI feedback (spinners, toasts, skeletons)

### Preferred Frontend Structure

```text
src/
├── api/                 # Centralized Axios/fetch client & interceptors
├── components/          # Reusable shared UI components (Button, Modal, etc.)
│   └── ui/              # Base primitives (design system)
├── pages/               # Page-level screen components
├── layouts/             # App shell layouts (MainLayout, AuthLayout, AdminLayout)
├── hooks/               # Custom React hooks (useAuth, useDebounce, etc.)
├── services/            # Domain-specific API service functions (productService.ts)
├── types/               # TypeScript interfaces & DTO type definitions
├── utils/               # Formatting, storage, and helper utilities
├── stores/              # Global state (Zustand, Context, Redux)
├── routes/              # Route definitions & ProtectedRoute wrapper
└── App.tsx              # Root component with providers
```

---

## 09. API CLIENT ARCHITECTURE

- Keep API calls outside UI components.
- Centralize all network calls in `src/services/` or `src/api/`.
- Do not scatter raw `fetch()` or `axios.get()` throughout JSX components.
- Keep frontend TypeScript types strictly synchronized with Backend DTOs.

### Standard Service Implementation

```typescript
// src/services/productService.ts
import { apiClient } from '../api/client';
import { ApiResponse, PagedResult, Product, ProductFilterParams, CreateProductPayload } from '../types';

export const productService = {
  async getPaged(params: ProductFilterParams): Promise<PagedResult<Product>> {
    const response = await apiClient.get<ApiResponse<PagedResult<Product>>>('/products', { params });
    if (!response.data.success || !response.data.data) {
      throw new Error(response.data.message || 'Failed to fetch products');
    }
    return response.data.data;
  },

  async getById(id: string): Promise<Product> {
    const response = await apiClient.get<ApiResponse<Product>>(`/products/${id}`);
    if (!response.data.success || !response.data.data) {
      throw new Error(response.data.message || 'Failed to fetch product');
    }
    return response.data.data;
  },

  async create(payload: CreateProductPayload): Promise<Product> {
    const response = await apiClient.post<ApiResponse<Product>>('/products', payload);
    if (!response.data.success || !response.data.data) {
      throw new Error(response.data.message || 'Failed to create product');
    }
    return response.data.data;
  }
};
```

---

## 10. FRONTEND AUTHENTICATION & SESSION MANAGEMENT

Handle all phases of authentication state cleanly:
- **Login / Logout flow**
- **Token management:** Store access token securely in memory/state; store refresh token in HttpOnly cookie or secure storage.
- **Request Interceptor:** Attach `Authorization: Bearer <token>` automatically on authenticated requests.
- **Response Interceptor:** Intercept `401 Unauthorized`:
  - Attempt token refresh once.
  - If refresh succeeds, retry the original failed request.
  - If refresh fails, clear tokens, redirect to `/login`, and prevent infinite retry loops.
- Handle `403 Forbidden` with a friendly "Access Denied" view rather than throwing unhandled errors.

---

## 11. ROUTING & ACCESS TIERS

Separate routes cleanly with higher-order guards:
- **Public Routes:** `/`, `/login`, `/register`, `/forgot-password`
- **Authenticated Routes:** `/dashboard`, `/profile`, `/orders`
- **Admin / Privileged Routes:** `/admin`, `/admin/users`, `/admin/settings`

### Protected Route Guard Pattern

```tsx
// src/routes/ProtectedRoute.tsx
import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface ProtectedRouteProps {
  requiredRole?: string;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ requiredRole }) => {
  const { user, isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <div className="flex h-screen items-center justify-center">Loading session...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requiredRole && user?.role !== requiredRole) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <Outlet />;
};
```

---

## 12. RESPONSIVE DESIGN & CROSS-BROWSER COMPLIANCE

UI must render cleanly on:
- Mobile (< 640px)
- Tablet (640px - 1024px)
- Desktop (1024px - 1440px)
- Large Desktop (> 1440px)

Cross-browser verification: Chrome, Edge, Firefox, Safari.

### Anti-Defect Rules
- Prevent horizontal scrollbars on viewports (`overflow-x-hidden` on roots where necessary).
- Ensure modal dialogs and dropdowns fit within mobile viewports with proper scroll containers.
- Tables must have horizontal scroll wrappers or convert to card layouts on mobile.
- Form inputs must maintain accessible tap targets (minimum 44x44px on touch devices).
- Text must wrap cleanly (`break-words`, `truncate` where intended) without breaking card layouts.

---

## 13. COMPONENT REUSABILITY & ATOMIC HYGIENE

Prefer reusable, composable component primitives:
- `Button`, `Input`, `Select`, `Textarea`, `Checkbox`, `Switch`
- `Modal`, `Dialog`, `Drawer`, `Dropdown`, `Popover`
- `Card`, `Badge`, `Avatar`, `Table`, `Pagination`
- `LoadingSpinner`, `Skeleton`, `EmptyState`, `ErrorState`, `Toast`
- `Navbar`, `Sidebar`, `Header`, `Footer`

> [!CAUTION]
> - Do not duplicate UI elements across pages.
> - Do not create premature abstractions for one-off markup.

---

## 14. FORM HANDLING DISCIPLINE

Every form must explicitly implement:
1. **Validation state:** Inline field errors matching backend field names.
2. **Pending / Loading state:** Disable submit button and inputs while API request is in-flight.
3. **Double-submit prevention:** Debounce or lock submission handler during active requests.
4. **Server error mapping:** Parse backend `errors` dictionary and map to corresponding form fields.
5. **Success feedback:** Clear form or show toast upon successful completion.

---

## 15. ERROR HANDLING PROTOCOL

### Backend
- Global Exception Handling Middleware intercepts all unhandled exceptions.
- Log error details with correlation ID to server logs.
- Return structured `ApiResponse<T>` with sanitized message to client.
- **NEVER** return stack traces, database query texts, or internal path names in production responses.

### Frontend
- Catch errors at the service or query boundary.
- Display user-friendly, actionable error messages.
- Provide a "Retry" button for transient network failures.
- Implement React `ErrorBoundary` around major page regions to prevent blank-screen crashes.

---

## 16. SECURITY CONTROLS

Always enforce:
- **Authentication & Authorization:** Check permissions at the backend controller/service level on every request.
- **SQL Injection Prevention:** Use parameterized queries or ORM LINQ expressions exclusively; never string-concatenate SQL.
- **XSS Prevention:** Let React escape variables; sanitize any raw HTML with DOMPurify if `dangerouslySetInnerHTML` is unavoidable.
- **CORS:** Restrict allowed origins in `Program.cs` to explicit frontend URLs; avoid `AllowAnyOrigin()` with credentials.
- **Rate Limiting:** Protect sensitive endpoints (`/api/auth/*`, payment, password reset) with ASP.NET Core RateLimiter.
- **Password Security:** Use ASP.NET Core Identity PasswordHasher (PBKDF2/Argon2/bcrypt) with work factor > 10.
- **Sensitive Data:** Exclude passwords, hashes, and internal tokens from JSON responses.

---

## 17. CONFIGURATION MANAGEMENT

- **Backend:** Environment variables > `appsettings.json` > `appsettings.Development.json`.
- **Frontend:** `.env`, `.env.development`, `.env.production` (e.g., `VITE_API_BASE_URL`).
- Never hardcode API base URLs, tenant keys, or credentials inside React components or C# classes.
- Ensure all environment variable names are documented in `.env.example`.

---

## 18. PERFORMANCE OPTIMIZATION

- **API & Database:**
  - Paginate all list endpoints.
  - Select only needed columns via DTO projections.
  - Index foreign keys, search fields, and frequently filtered columns.
  - Implement response caching (`IMemoryCache` / Redis) for read-heavy, low-churn data.
- **Frontend:**
  - Code-split routes with `React.lazy()` and `Suspense`.
  - Debounce search inputs (300-500ms) to prevent flooding the backend API.
  - Memoize expensive client calculations with `useMemo`.
  - Optimize images (WebP format, lazy loading attributes).

---

## 19. EXISTING PROJECT RULE (PRESERVATION MANDATE)

When working in an existing codebase:
- **DO NOT** rewrite the entire project or replace core frameworks.
- **DO NOT** redesign UI components unless explicitly requested.
- **DO NOT** delete working features or modify existing public API contracts unnecessarily.
- **DO NOT** alter database schemas unless required by the new requirement.
- **DO NOT** duplicate existing components or services—search first and reuse.
- **Hierarchy:** Reuse first ➔ Modify second ➔ Create new code only when necessary.

---

## 20. END-TO-END IMPLEMENTATION FLOW

For every feature request, follow this exact linear sequence:

```text
[1] Analyze requirement & inspect existing code
 └──▶ [2] Identify affected backend and frontend modules
       └──▶ [3] Update Database entity / migration (if required)
             └──▶ [4] Implement Backend Repository / Data Access
                   └──▶ [5] Implement Service business logic & DTOs
                         └──▶ [6] Implement Controller endpoint & Auth attributes
                               └──▶ [7] Test API endpoint (Swagger/Postman/Integration)
                                     └──▶ [8] Define Frontend TypeScript types matching DTOs
                                           └──▶ [9] Implement Frontend API service function
                                                 └──▶ [10] Connect state (React hook / store)
                                                       └──▶ [11] Build/Update UI components
                                                             └──▶ [12] Implement validation & error states
                                                                   └──▶ [13] Verify responsive layout
                                                                         └──▶ [14] Execute full flow test
                                                                               └──▶ [15] Final verification & cleanup
```

> [!IMPORTANT]
> The feature must work end-to-end. No mock buttons, no fake APIs, no dead links, no hardcoded demo arrays when a real API exists.

---

## 21. CHANGE SAFETY PROTOCOL

Before modifying any file:
1. Understand the current behavior and side effects.
2. Preserve unrelated logic, comments, and public methods.
3. Make the smallest safe diff that solves the problem.
4. Avoid incidental formatting changes across unchanged lines.
5. Do not refactor unrelated code during feature implementation.

---

## 22. DEBUGGING & ROOT CAUSE ANALYSIS (RCA)

When a bug or runtime exception occurs:
1. **Read the exact error message** and stack trace.
2. **Locate the originating source file and line.**
3. **Trace the request/data flow** from UI to Database to see where the contract broke.
4. **Identify the root cause** (type mismatch, null reference, missing migration, auth failure).
5. **Fix the root cause directly at the source.**
6. **Re-test the complete affected flow.**
7. **Verify that no regressions were introduced.**

> [!CAUTION]
> Never silence errors with empty `catch` blocks or suppress TypeScript types with `any` / `@ts-ignore` without genuine technical reasons.

---

## 23. PRE-COMPLETION VERIFICATION CHECKLIST

Before marking any fullstack task complete, verify every single item:

- [ ] **Backend Compiles:** Zero C# compilation errors or warnings.
- [ ] **Frontend Compiles:** Zero TypeScript compiler errors (`tsc --noEmit`).
- [ ] **API Endpoint Functions:** Returns correct HTTP status code and response envelope.
- [ ] **Database Persistence:** Data is correctly read from and saved to the database.
- [ ] **Authentication Enforced:** Unauthorized requests receive `401 Unauthorized`.
- [ ] **Authorization Enforced:** Insufficient role requests receive `403 Forbidden`.
- [ ] **Backend Validation Active:** Malformed payloads return `400 Bad Request` with field errors.
- [ ] **Frontend Validation UX:** User is prompted before submitting invalid data.
- [ ] **Error Handling Graceful:** Server errors do not crash the UI or leak stack traces.
- [ ] **Loading States Visible:** Spinners, skeletons, or disabled buttons reflect pending requests.
- [ ] **Responsive Tested:** Layout works across mobile, tablet, and desktop viewports.
- [ ] **Routes Work:** Client router navigates correctly without page reloads.
- [ ] **API Contracts Synchronized:** TypeScript interfaces match backend DTOs field-for-field.
- [ ] **No Broken Imports:** All imports resolve cleanly.
- [ ] **No Secrets Exposed:** No passwords, connection strings, or JWT keys committed.
- [ ] **Existing Features Preserved:** Pre-existing tests and flows remain fully functional.
- [ ] **No Dead Code:** No unused mock data, placeholder functions, or orphaned files.

---

## 24. TOKEN EFFICIENCY GUIDELINES

Maximize agent intelligence while minimizing token expenditure:
- Read only files relevant to the specific feature or bug.
- Do not re-read unchanged files repeatedly.
- Provide surgical, targeted file modifications rather than reprinting entire large files.
- Keep explanatory summaries concise and structured.
- When reporting completed work, use the standard format:

```text
Changed:
- <file_path_1>
- <file_path_2>

Reason:
- <concise technical rationale>

Verification:
- <verification results against checklist>
```

---

## 25. DEPENDENCY MANAGEMENT

Before installing any NuGet or NPM package:
1. Check existing `package.json` and `.csproj` dependencies.
2. Determine if the desired capability is already provided by an installed library or language built-in.
3. Install a new dependency only if it provides significant value and is actively maintained.
4. Never introduce two competing packages for the same purpose (e.g., Axios AND Redux Toolkit Query, or Dapper AND EF Core for identical queries).

---

## 26. FILE CREATION GOVERNANCE

Before creating any new file:
1. Search the existing codebase for equivalent functionality.
2. Reuse or extend existing files if architecturally appropriate.
3. Follow existing naming conventions and file paths.
4. Never create duplicate controllers, services, repositories, or UI components.

---

## 27. CODE STYLE & IDIOMS

### C# / .NET Conventions
- **Naming:** `PascalCase` for classes, methods, properties, DTOs; `_camelCase` for private fields; `camelCase` for parameters.
- **Asynchrony:** Always use `async` / `await` with `CancellationToken` support on I/O-bound operations.
- **Nullability:** Enable Nullable Reference Types (`#nullable enable`); avoid suppressing null warnings.
- **Dependency Injection:** Register dependencies via interfaces in `Program.cs` (`Scoped` for services/contexts, `Singleton` for stateless utilities).

### TypeScript / React Conventions
- **Naming:** `PascalCase` for components, interfaces, types; `camelCase` for variables, functions, hooks; `UPPER_SNAKE_CASE` for constants.
- **Strict Typing:** Strictly type all props, state, API responses, and function parameters.
- **No `any`:** Avoid `any`; use `unknown` with type guards or generic types if type is dynamic.
- **Hooks:** Follow Rules of Hooks; keep dependency arrays accurate.

---

## 28. NO OVER-ENGINEERING PRINCIPLE

- Prefer simple, explicit, readable implementations over complex abstractions.
- Avoid unnecessary architectural patterns:
  - Do NOT introduce CQRS, MediatR, Event Sourcing, or complex Generic Repositories unless the project is already built on them or the user explicitly asks for them.
  - Do NOT introduce Redux or complex global state for data that belongs in local component state or React Query cache.
- Existing project conventions always take precedence.

---

## 29. COMPLETION & INTEGRITY RULE

- **Never terminate a task after writing partial code.**
- A feature is only complete when the end-to-end chain is connected and functional:
  `UI Component ➔ API Client ➔ Controller ➔ Service ➔ Database ➔ Response ➔ State ➔ UI Component`.
- If an implementation touches 5 files across backend and frontend, update all 5 files completely. Do not leave the frontend disconnected from the backend.

---

## 30. SENIOR AGENT BEHAVIOR PROTOCOL

As a Senior Fullstack Engineer:
- **Inspect before you modify.** Look at existing code to match style, patterns, and conventions.
- **Fix root causes, not symptoms.** Trace bugs to their origin.
- **Preserve existing functionality.** Guard existing contracts rigorously.
- **Deliver production-grade code.** No TODO comments, no placeholders, no truncated functions.
- **Execute with autonomy when clear.** If the prompt provides clear requirements, implement directly.
- **Ask focused questions only when blocked.** If a critical ambiguity prevents implementation, ask exactly one clear question.
- **Never fabricate files or API routes.** Reference only real files and real endpoints.
