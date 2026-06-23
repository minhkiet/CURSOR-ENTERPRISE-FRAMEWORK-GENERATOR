# CRM Decision Tree - Cây Quyết Định Thiết Kế

## 1. Data Model Design Decision Tree

```
BẮT ĐẦU: Thiết kế Data Model cho CRM
│
├─► Bạn cần lưu trữ loại dữ liệu nào?
│   │
│   ├─► Dữ liệu có cấu trúc cố định (customer info, contact details)?
│   │   │
│   │   └─► YES → Sử dụng relational tables (PostgreSQL/MySQL)
│   │           │
│   │           ├─► Cần tracking lịch sử thay đổi?
│   │           │   │
│   │           │   ├─► YES → Temporal tables với valid_from, valid_to
│   │           │   │
│   │           │   └─► NO → Standard tables với updated_at trigger
│   │           │
│   │           └─► Thiết kế indexes cho frequently queried columns
│   │
│   ├─► Dữ liệu semi-structured (metadata, preferences)?
│   │   │
│   │   └─► YES → PostgreSQL JSONB column với GIN index
│   │           │
│   │           ├─► Cần query sâu vào nested JSON?
│   │           │   │
│   │           │   ├─► YES → Sử dụng JSONB operators (->, ->>)
│   │           │   │
│   │           │   └─► NO → Store as TEXT, query parent keys only
│   │           │
│   │           └─► Cần full-text search trên JSON fields?
│   │               │
│   │               ├─► YES → Add separate tsvector column
│   │               │
│   │               └─► NO → GIN index là đủ
│   │
│   └─► Dữ liệu có nhiều relationships phức tạp (org charts)?
│       │
│       └─► YES → Consider Graph Database (Neo4j)
│               │
│               ├─► Relationships cần frequently traversed?
│               │   │
│               │   ├─► YES → Neo4j là lựa chọn tốt
│               │   │
│               │   └─► NO → Adjacency list trong PostgreSQL đủ
│               │
│               └─► Cần path finding algorithms?
│                   │
│                   ├─► YES → Neo4j với Cypher
│                   │
│                   └─► NO → PostgreSQL với recursive CTE
│
│
├─► Bạn cần unique identifiers như thế nào?
│   │
│   ├─► Internal use only, no security concerns?
│   │   │
│   │   └─► YES → Auto-increment integers
│   │           │
│   │           └─► Performance: Fast joins, smaller storage
│   │
│   ├─► Exposed in URLs/API?
│   │   │
│   │   └─► YES → UUID v4 (random)
│   │           │
│   │           ├─► Cần sortable UUIDs?
│   │           │   │
│   │           │   ├─► YES → UUID v7 (time-ordered)
│   │           │   │
│   │           │   └─► NO → UUID v4
│   │           │
│   │           └─► Privacy concern (no information leakage)?
│   │               │
│   │               ├─► YES → UUID v4 với proper authorization
│   │               │
│   │               └─► NO → Hash-based IDs
│   │
│   └─► Cần human-readable IDs (ticket numbers, order codes)?
│       │
│       └─► YES → Hybrid approach
│               │
│               ├─► Public ID: PREFIX-YYYYMMDD-XXXX (e.g., CUST-20260623-0001)
│               │
│               └─► Internal ID: UUID (for joins, references)
│
│
├─► Bạn cần soft delete hay hard delete?
│   │
│   ├─► Cần preserve audit trail?
│   │   │
│   │   └─► YES → Soft delete với deleted_at, deleted_by columns
│   │           │
│   │           ├─► Cần reactivate deleted records?
│   │           │   │
│   │           │   ├─► YES → Keep deleted_at nullable, implement restore
│   │           │   │
│   │           │   └─► NO → Keep deleted records separate table
│   │           │
│   │           └─► Add partial index: WHERE deleted_at IS NULL
│   │
│   └─► NO (data can be permanently deleted)?
│       │
│       └─► YES → Hard delete với CASCADE
│               │
│               ├─► Cần immediate deletion for privacy (GDPR)?
│               │   │
│               │   ├─► YES → Hard delete + backup before deletion
│               │   │
│               │   └─► NO → Soft delete first, batch hard delete later
│               │
│               └─► Consider archiving to separate table before delete
```

## 2. API Design Decision Tree

```
BẮT ĐẦU: Thiết kế CRM API
│
├─► Chọn communication style
│   │
│   ├─► REST → HTTP/REST API
│   │   │
│   │   ├─► CRUD operations với standard HTTP methods
│   │   │
│   │   ├─► Response format: JSON
│   │   │
│   │   └─► Use case: Standard web/mobile clients
│   │
│   ├─► GraphQL → Flexible queries
│   │   │
│   │   ├─► Client can request exactly what they need
│   │   │
│   │   ├─► Multiple related resources in single request
│   │   │
│   │   └─► Use case: Dashboard, mobile apps
│   │
│   └─► gRPC → High performance, internal services
│       │
│       ├─► Streaming support
│       │
│       ├─► Strong typing với Protocol Buffers
│       │
│       └─► Use case: Microservices communication
│
│
├─► Thiết kế endpoint structure
│   │
│   ├─► Collection endpoints (list, create)
│   │   │
│   │   └─► GET /api/v1/customers
│   │       POST /api/v1/customers
│   │
│   ├─► Resource endpoints (get, update, delete)
│   │   │
│   │   └─► GET /api/v1/customers/{id}
│   │       PATCH /api/v1/customers/{id}
│   │       DELETE /api/v1/customers/{id}
│   │
│   └─► Action endpoints (non-CRUD operations)
│       │
│       ├─► POST /api/v1/customers/{id}/merge
│       │   POST /api/v1/customers/{id}/convert-to-opportunity
│       │
│       └─► Alternative: Action field
│           POST /api/v1/customers/{id}
│           { "action": "merge", "withId": "xxx" }
│
│
├─► Pagination strategy
│   │
│   ├─► Offset-based (LIMIT/OFFSET)
│   │   │
│   │   ├─► Use when: Users can jump to specific pages
│   │   │
│   │   ├─► Pros: Simple, users can navigate freely
│   │   │
│   │   └─► Cons: Slow for large offsets, inconsistent results
│   │
│   ├─► Cursor-based (keyset pagination)
│   │   │
│   │   ├─► Use when: Infinite scroll, large datasets
│   │   │
│   │   ├─► Pros: Consistent, fast, scalable
│   │   │
│   │   └─► Cons: Can't jump to page, only next/previous
│   │
│   └─► Time-based
│       │
│       ├─► Use when: Streaming/real-time data
│       │
│       └─► Cursor based on timestamp
│
│
├─► Error handling strategy
│   │
│   ├─► HTTP Status Codes
│   │   │
│   │   ├─► 400 Bad Request → Validation errors
│   │   ├─► 401 Unauthorized → Authentication required
│   │   ├─► 403 Forbidden → Insufficient permissions
│   │   ├─► 404 Not Found → Resource doesn't exist
│   │   ├─► 409 Conflict → Duplicate, version conflict
│   │   ├─► 422 Unprocessable Entity → Business rule violation
│   │   └─► 429 Too Many Requests → Rate limited
│   │
│   └─► Error Response Format
│       │
│       └─► {
│           "error": "ERROR_CODE",
│           "message": "Human readable message",
│           "details": { ... },
│           "traceId": "xxx"
│         }
│
│
├─► Versioning strategy
│   │
│   ├─► URL versioning → /api/v1/, /api/v2/
│   │   │
│   │   ├─► Pros: Explicit, easy to route
│   │   │
│   │   └─► Cons: URL pollution
│   │
│   ├─► Header versioning → Accept: application/vnd.api.v1+json
│   │   │
│   │   ├─► Pros: Clean URLs
│   │   │
│   │   └─► Cons: Less discoverable
│   │
│   └─► Date-based ( evolutive API)
│       │
│       └─► No versioning, backward compatibility required
```

## 3. Authentication & Authorization Decision Tree

```
BẮT ĐẦU: Thiết kế Authentication cho CRM
│
├─► Chọn authentication method
│   │
│   ├─► Internal users (employees)
│   │   │
│   │   ├─► SSO available?
│   │   │   │
│   │   │   ├─► YES → SAML 2.0 / OAuth 2.0 (OIDC)
│   │   │   │   │
│   │   │   │   ├─► Microsoft/Azure AD → OIDC with Microsoft
│   │   │   │   │
│   │   │   │   ├─► Okta/Auth0 → OIDC/SAML
│   │   │   │   │
│   │   │   │   └─► Custom IdP → SAML or OIDC
│   │   │   │
│   │   │   └─► Additional MFA required?
│   │   │       │
│   │   │       ├─► YES → TOTP or WebAuthn
│   │   │       │
│   │   │       └─► NO → Continue
│   │   │
│   │   └─► NO → Username/Password + MFA
│   │           │
│   │           ├─► Password requirements:
│   │           │   ├─► Minimum 12 characters
│   │           │   ├─► Mixed case, numbers, symbols
│   │           │   └─► Check against known breaches (HaveIBeenPwned)
│   │           │
│   │           └─► MFA options:
│   │               ├─► TOTP (Google Authenticator, Authy)
│   │               ├─► SMS (less secure, backup only)
│   │               └─► WebAuthn (hardware keys, biometrics)
│   │
│   ├─► External users (customers, partners)
│   │   │
│   │   ├─► OAuth 2.0 / Social login
│   │   │   │
│   │   │   ├─► Google, Facebook, Apple
│   │   │   │
│   │   │   └─► + Email/Password as fallback
│   │   │
│   │   └─► Email magic links
│   │       │
│   │       └─► Use when: Reducing password fatigue
│   │
│   └─► API access (machine-to-machine)
│       │
│       └─► API Keys hoặc OAuth 2.0 Client Credentials
│           │
│           ├─► Short-lived tokens (1 hour)
│           │
│           └─► Refresh token rotation
│
│
├─► Chọn authorization model
│   │
│   ├─► Role-Based Access Control (RBAC)
│   │   │
│   │   ├─► Simple permission model (admin, manager, user)
│   │   │
│   │   ├─► Use when: Permissions align with roles
│   │   │
│   │   └─► Implementation:
│   │       │
│   │       ├─► Roles table: id, name, description
│   │       │
│   │       └─► Role permissions: role_id, permission
│   │
│   ├─► Attribute-Based Access Control (ABAC)
│   │   │
│   │   ├─► Complex rules (owner can edit, others read-only)
│   │   │
│   │   ├─► Use when: Context-dependent permissions
│   │   │
│   │   └─► Implementation:
│   │       │
│   │       ├─► Policy engine evaluates conditions
│   │       │
│   │       └─► Conditions: resource.owner_id == user.id
│   │
│   └─► Hybrid (RBAC + ABAC)
│       │
│       └─► Base permissions via roles
│           + Fine-grained rules for specific resources
│
│
├─► Field-level security
│   │
│   ├─► Need to restrict specific fields?
│   │   │
│   │   ├─► YES → Implement field-level ACL
│   │   │   │
│   │   │   ├─► Database level: Column-level grants
│   │   │   │
│   │   │   ├─► Application level: Field filtering
│   │   │   │
│   │   │   └─► Example:
│   │   │       {
│   │   │         "ssn": { "visibleTo": ["admin", "finance"] },
│   │   │         "creditLimit": { "visibleTo": ["admin", "finance", "manager"] }
│   │   │       }
│   │   │
│   │   └─► NO → Skip
│   │
│   └─► Row-level security
│       │
│       ├─► Users see only their data?
│       │   │
│       │   ├─► YES → Add owner_id filter to all queries
│       │   │
│       │   └─► Alternative: Database RLS (PostgreSQL)
│       │
│       └─► Team-based access?
│           │
│           ├─► YES → Team membership check
│           │
│           └─► NO → Continue
│
│
├─► Session management
│   │
│   ├─► Token-based (JWT)
│   │   │
│   │   ├─► Access token lifetime: 15-60 minutes
│   │   │
│   │   ├─► Refresh token lifetime: 7-30 days
│   │   │
│   │   └─► Storage: HttpOnly cookies (not localStorage)
│   │
│   └─► Session-based (traditional)
│       │
│       ├─► Server-side session storage
│       │
│       └─► Session cookie: HttpOnly, Secure, SameSite=Strict
```

## 4. Database Selection Decision Tree

```
BẮT ĐẦU: Chọn Database cho CRM
│
├─► Primary data store (customers, transactions)
│   │
│   ├─► PostgreSQL
│   │   │
│   │   ├─► Use when:
│   │   │   ├─► ACID compliance required
│   │   │   ├─► Complex queries, joins
│   │   │   ├─► JSONB for semi-structured data
│   │   │   ├─► Full-text search needed
│   │   │   └─► Enterprise-grade reliability
│   │   │
│   │   └─► Strengths:
│   │       ├─► Excellent JSON support
│   │       ├─► Rich indexing options
│   │       ├─► Strong reliability
│   │       └─► Great tooling
│   │
│   ├─► MySQL
│   │   │
│   │   ├─► Use when:
│   │   │   ├─► Simple CRUD operations
│   │   │   ├─► High write throughput
│   │   │   └─► PHP/LAMP stack
│   │   │
│   │   └─► Limitations:
│   │       ├─► Weaker JSON support
│   │       └─► Less advanced features
│   │
│   └─► SQL Server
│       │
│       ├─► Use when:
│       │   ├─► Microsoft ecosystem
│       │   ├─► Enterprise Windows integration
│       │   └─► .NET framework
│       │
│       └─► Strengths:
│           ├─► Excellent tooling (SSMS)
│           └─► Strong enterprise features
│
│
├─► Caching layer
│   │
│   └─► Redis
│       │
│       ├─► Use when:
│       │   ├─► Session storage
│       │   ├─► API response caching
│       │   ├─► Real-time data (leaderboards, counters)
│       │   └─► Message queue (pub/sub)
│       │
│       └─► Data structure types:
│           ├─► Strings → Simple caching
│           ├─► Hashes → Objects
│           ├─► Sorted Sets → Rankings
│           └─► Streams → Event processing
│
│
├─► Search engine
│   │
│   ├─► Elasticsearch
│   │   │
│   │   ├─► Use when:
│   │   │   ├─► Complex full-text search
│   │   │   ├─► Faceted search
│   │   │   ├─► Autocomplete/suggestions
│   │   │   └─► Log analytics
│   │   │
│   │   └─► CRM use cases:
│   │       ├─► Customer search
│   │       ├─► Activity log search
│   │       └─► Reporting aggregations
│   │
│   └─► PostgreSQL built-in (alternative)
│       │
│       └─► Use when:
│           ├─► Search requirements simple
│           └─► Want to avoid extra infrastructure
│
│
├─► Analytics/Reporting
│   │
│   ├─► ClickHouse
│   │   │
│   │   ├─► Use when:
│   │   │   ├─► High-volume analytics
│   │   │   ├─► Time-series data
│   │   │   └─► Append-only data
│   │   │
│   │   └─► Good for: Event tracking, usage analytics
│   │
│   ├─► Snowflake/BigQuery/Redshift
│   │   │
│   │   ├─► Use when:
│   │   │   ├─► Data warehouse needs
│   │   │   ├─► Complex analytics
│   │   │   └─► Cloud-native preferred
│   │   │
│   │   └─► Good for: Historical analysis, ML features
│   │
│   └─► PostgreSQL + Materialized Views
│       │
│       └─► Use when:
│           ├─► Analytics needs simple
│           └─► Want to minimize infrastructure
│
│
└─► Document storage (optional)
    │
    ├─► MongoDB
    │   │
    │   ├─► Use when:
    │   │   ├─► Schema-less data
    │   │   ├─► Rapid prototyping
    │   │   └─► Horizontal scaling priority
    │   │
    │   └─► CRM use cases (rare):
    │       ├─► User-generated content
    │       └─► Temporary data
    │
    └─► Skip (use PostgreSQL JSONB instead)
        │
        └─► Most CRM data is structured, JSONB is sufficient
```

## 5. Caching Strategy Decision Tree

```
BẮT ĐẦU: Thiết kế Caching Strategy cho CRM
│
├─► Cache nào phù hợp?
│   │
│   ├─► In-memory (L1)
│   │   │
│   │   ├─► Caffeine (JVM) / current library (Node)
│   │   │
│   │   ├─► Use when:
│   │   │   ├─► Hot data accessed frequently
│   │   │   └─► Need sub-millisecond latency
│   │   │
│   │   └─► Configuration:
│   │       │
│   │       ├─► Max size: Based on available memory
│   │       ├─► TTL: 5-30 minutes
│   │       └─► Eviction: LRU hoặc LFU
│   │
│   ├─► Distributed (L2)
│   │   │
│   │   └─► Redis
│   │       │
│   │       ├─► Use when:
│   │       │   ├─► Multi-instance deployment
│   │       │   ├─► Need shared session storage
│   │       │   └─► Want persistence option
│   │       │
│   │       └─► Cache patterns:
│   │           │
│   │           ├─► Cache-aside (read-through)
│   │           ├─► Write-through
│   │           └─► Write-behind
│   │
│   └─► CDN (L3)
│       │
│       └─► Use when:
│           ├─► Static assets
│           └─► Public API responses
│
│
├─► Cache invalidation strategy
│   │
│   ├─► Time-based (TTL)
│   │   │
│   │   ├─► Use when: Stale data acceptable
│   │   │
│   │   └─► TTL selection:
│   │       ├─► User preferences: 1 hour
│   │       ├─► Dashboard data: 5-15 minutes
│   │       └─► Reference data: 24 hours
│   │
│   ├─► Event-based invalidation
│   │   │
│   │   ├─► Use when: Need immediate updates
│   │   │
│   │   ├─► Implementation:
│   │   │   │
│   │   │   ├─► Publish event on data change
│   │   │   │
│   │   │   └─► Cache consumer invalidates related keys
│   │   │
│   │   └─► Example:
│   │       ├─► Customer updated → Invalidate customer:{id}
│   │       ├─► Customer updated → Invalidate user:{ownerId}:dashboard
│   │       └─► Customer updated → Invalidate list pages
│   │
│   └─► Version-based
│       │
│       └─► Store version number with cache
│           │
│           ├─► Compare version on read
│           │
│           └─► Invalidate if version mismatch
│
│
├─► What to cache?
│   │
│   ├─► Database query results
│   │   │
│   │   ├─► Yes: Expensive aggregations (dashboard summary)
│   │   ├─► Yes: Reference data (countries, industries)
│   │   ├─► Yes: User permissions
│   │   ├─► No: Real-time data (stock prices)
│   │   └─► No: User-specific data (shopping cart)
│   │
│   ├─► API responses
│   │   │
│   │   ├─► Yes: Public endpoints
│   │   ├─► Yes: Expensive computations
│   │   ├─► Yes: Third-party API responses
│   │   └─► No: Personalized responses
│   │
│   └─► Computed values
│       │
│       ├─► Yes: CLV calculations
│       ├─► Yes: Lead scores
│       ├─► Yes: Recommendation engine output
│       └─► No: Real-time metrics
│
│
├─► Cache warming strategy
│   │
│   ├─► Eager loading
│   │   │
│   │   └─► Pre-populate cache on startup
│   │       │
│   │       ├─► Load hot data
│   │       │
│   │       └─► Background job
│   │
│   └─► Lazy loading
│       │
│       └─► Populate on first access
│           │
│           ├─► Simple
│           │
│           └─► Risk: Cold start latency
```

## 6. Event Processing Decision Tree

```
BẮT ĐẦU: Thiết kế Event Processing cho CRM
│
├─► Event types
│   │
│   ├─► Domain Events (business meaningful)
│   │   │
│   │   ├─► customer.created
│   │   ├─► opportunity.stage_changed
│   │   ├─► lead.converted
│   │   └─► customer.lifecycle_stage_changed
│   │
│   ├─► Integration Events (external communication)
│   │   │
│   │   ├─► customer.sync_requested
│   │   └─► invoice.generated
│   │
│   └─► System Events (infrastructure)
│       │
│       ├─► user.login
│       ├─► api.request
│       └─► cache.invalidated
│
│
├─► Event delivery patterns
│   │
│   ├─► Fire-and-forget
│   │   │
│   │   └─► Use when: Best effort acceptable
│   │       │
│   │       └─► Example: Analytics tracking
│   │
│   ├─► At-least-once delivery
│   │   │
│   │   └─► Use when: Must not lose events
│   │       │
│   │       ├─► Implement idempotency
│   │       │
│   │       └─► Example: Order processing
│   │
│   └─► Exactly-once delivery
│       │
│       └─► Use when: Critical consistency required
│           │
│           ├─► Most complex to implement
│           │
│           └─► Example: Payment processing
│
│
├─► Message queue selection
│   │
│   ├─► Apache Kafka
│   │   │
│   │   ├─► Use when:
│   │   │   ├─► High throughput (100k+ events/sec)
│   │   │   ├─► Event streaming (Kafka Streams)
│   │   │   ├─► Log compaction needed
│   │   │   └─► Multi-consumer groups
│   │   │
│   │   └─► Good for: Audit logs, event sourcing
│   │
│   ├─► RabbitMQ
│   │   │
│   │   ├─► Use when:
│   │   │   ├─► Task queues (one consumer)
│   │   │   ├─► Complex routing
│   │   │   └─► Request/response patterns
│   │   │
│   │   └─► Good for: Background jobs, notifications
│   │
│   └─► Redis Streams
│       │
│       ├─► Use when:
│       │   ├─► Low-medium throughput
│       │   └─► Already using Redis
│       │
│       └─► Good for: Simple queuing, rate limiting
│
│
├─► Consumer patterns
│   │
│   ├─► Point-to-point
│   │   │
│   │   └─► One consumer per event type
│   │       │
│   │       └─► Example: EmailService consumes customer.created
│   │
│   ├─► Pub/Sub
│   │   │
│   │   └─► Multiple independent consumers
│   │       │
│   │       └─► Example: Analytics + Email + CRM all need customer.created
│   │
│   └─► Saga/Orchestration
│       │
│       └─► Coordinated multi-step processes
│           │
│           ├─► Order creation → Inventory check → Payment → Confirmation
│           │
│           └─► Use compensating transactions for rollback
│
│
├─► Error handling in event processing
│   │
│   ├─► Retry with backoff
│   │   │
│   │   ├─► Exponential backoff: 1s, 2s, 4s, 8s...
│   │   │
│   │   └─► Max retries: 3-5
│   │
│   ├─► Dead Letter Queue (DLQ)
│   │   │
│   │   ├─► After max retries → Move to DLQ
│   │   │
│   │   └─► DLQ processing:
│   │       ├─► Manual review
│   │       ├─► Automated repair
│   │       └─► Discard after investigation
│   │
│   └─► Circuit breaker
│       │
│       ├─► Fail fast when downstream is down
│       │
│       └─► States: Closed (normal) → Open (blocking) → Half-open (testing)
```

## 7. Deployment Decision Tree

```
BẮT ĐẦU: Chọn Deployment Strategy cho CRM
│
├─► Infrastructure type
│   │
│   ├─► On-premises
│   │   │
│   │   ├─► Use when:
│   │   │   ├─► Data sovereignty requirements
│   │   │   ├─► Regulatory compliance (no cloud)
│   │   │   └─► Existing infrastructure investment
│   │   │
│   │   └─► Considerations:
│   │       ├─► Higher operational burden
│   │       └─► Need DevOps team
│   │
│   ├─► Cloud (IaaS)
│   │   │
│   │   ├─► Use when:
│   │   │   ├─► Want control over infrastructure
│   │   │   ├─► Existing cloud expertise
│   │   │   └─► Cost optimization needed
│   │   │
│   │   └─► Examples:
│   │       ├─► AWS EC2, AWS RDS
│   │       └─► Azure VMs, Azure SQL
│   │
│   ├─► Platform as a Service (PaaS)
│   │   │
│   │   ├─► Use when:
│   │   │   ├─► Want to focus on code
│   │   │   ├─► Faster deployment
│   │   │   └─► Scalability needed
│   │   │
│   │   └─► Examples:
│   │       ├─► Heroku, Render
│   │       ├─► AWS Elastic Beanstalk
│   │       └─► Azure App Service
│   │
│   └─► Container/Kubernetes
│       │
│       ├─► Use when:
│       │   ├─► Microservices architecture
│       │   ├─► Need auto-scaling
│       │   ├─► Multi-environment consistency
│       │   └─► High availability required
│       │
│       └─► Tools:
│           ├─► Amazon EKS, Azure AKS
│           ├─► Google GKE
│           └─► Self-hosted Kubernetes
│
│
├─► Deployment strategy
│   │
│   ├─► All-at-once (big bang)
│   │   │
│   │   ├─► Pros: Simple, fast
│   │   │
│   │   └─► Cons: High risk, no rollback
│   │
│   ├─► Rolling deployment
│   │   │
│   │   ├─► Pros: Zero downtime, gradual rollout
│   │   │
│   │   └─► Cons: Harder to rollback, mixed versions
│   │
│   ├─► Blue-green deployment
│   │   │
│   │   ├─► Pros: Instant rollback, easy testing
│   │   │
│   │   └─► Cons: Double infrastructure cost
│   │
│   └─► Canary deployment
│       │
│       ├─► Pros: Low risk, real-world testing
│       │
│       └─► Cons: Complex routing, monitoring
│
│
├─► Database migration strategy
│   │
│   ├─► Expand-Contract pattern
│   │   │
│   │   ├─► Phase 1: Expand (add new column)
│   │   ├─► Phase 2: Migrate (backfill data)
│   │   ├─► Phase 3: Contract (remove old column)
│   │   │
│   │   └─► Use when: Breaking schema changes
│   │
│   └─► Backward compatible migrations
│       │
│       ├─► Add nullable columns first
│       ├─► Deploy code that uses new schema
│       └─► Backfill old records
│
│
└─► Monitoring setup
    │
    ├─► Metrics
    │   │
    │   ├─► Prometheus + Grafana
    │   │
    │   └─► CloudWatch/Datadog
    │
    ├─► Logging
    │   │
    │   ├─► ELK Stack (Elasticsearch, Logstash, Kibana)
    │   │
    │   └─► Loki + Grafana
    │
    ├─► Tracing
    │   │
    │   └─► Jaeger, Zipkin
    │
    └─► Alerting
        │
        ├─► PagerDuty, Opsgenie
        │
        └─► Alert on:
            ├─► Error rate spike
            ├─► Latency increase
            ├─► Resource exhaustion
            └─► Failed deployments
```
