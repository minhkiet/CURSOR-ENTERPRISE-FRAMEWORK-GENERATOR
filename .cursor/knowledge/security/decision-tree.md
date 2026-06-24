# Security Knowledge - Decision Tree

## Is authentication required?
- YES: Is it user-facing or service-to-service?
  - User-facing: Use OAuth2/OIDC with established library (Auth0, Firebase, Clerk)
  - Service-to-service: Use API keys or mTLS
- NO: Is the endpoint intentionally public?
  - Intentional: Document clearly, no auth needed
  - Unintentional: ADD AUTH before proceeding

## What type of authorization?
- Role-based actions: Use RBAC with role hierarchy
- Resource ownership: Check owner_id == current_user_id on every request
- Attribute-based: Use ABAC for complex conditions
- Default: Deny all, explicitly grant only what's needed

## What is the trust boundary?
- Public internet -> Load balancer: TLS required
- Load Balancer -> API Server: mTLS or internal network
- API Server -> Database: Unix socket or encrypted connection
- API Server -> External API: TLS + signature validation

## Input source classification
- User input (forms, API body, URL params): STRICT validation, parameterized queries
- File uploads: Verify type (magic bytes), scan content, limit size
- External API responses: Validate schema, sanitize before use
- Environment variables: Treat as untrusted, validate before use
- Database read: Still validate before processing

## Secrets storage decision
- Production secrets: Use vault (HashiCorp, Azure Key Vault, AWS Secrets Manager)
- Non-secret config: Environment variables
- Development secrets: .env file NOT committed to git
- Database credentials: Vault or encrypted at rest

## Data classification
- Public: No protection needed
- Internal: TLS in transit
- Confidential: TLS + encryption at rest
- Restricted (PII, payment, health): TLS + encryption + access controls + audit logging

## Vulnerability response
- Critical (RCE, SQL injection): Patch immediately, rollback if needed
- High (XSS, CSRF, broken auth): Patch within 24-48h
- Medium (information disclosure): Patch within 30 days
- Low (missing security headers): Patch within 90 days

## When to use encryption?
- Data at rest: Always for PII, payment, health, credentials
- Data in transit: Always (TLS 1.2+ minimum)
- Passwords: Hash only (never encrypt)
- API keys/secrets: Hash or encrypt (vault preferred)
- Tokens: JWT signed, not encrypted (unless containing secrets)
