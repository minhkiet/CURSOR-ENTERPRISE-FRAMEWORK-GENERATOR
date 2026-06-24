# Security Knowledge - Best Practices

## Authentication Best Practices
- Use established auth libraries (Auth0, Firebase Auth, Clerk)
- JWT access tokens: 15-60 min expiry
- JWT refresh tokens: 7-30 days expiry, stored in httpOnly cookie
- Always hash passwords with bcrypt (cost >= 10) or Argon2
- Enforce strong password policies (min 12 chars, mixed case, numbers, symbols)
- Implement account lockout after failed attempts (5 attempts, 15 min lockout)
- Use MFA for sensitive operations and admin accounts
- Implement "Remember me" with secure long-lived tokens
- Log all auth events (success, failure, token refresh)

## Authorization Best Practices
- Validate permissions on every protected endpoint (defense in depth)
- Check ownership/resource-level authorization for all resource operations
- Implement RBAC with clear role hierarchy
- Use policy-based authorization frameworks
- Never rely solely on client-side checks
- Implement principle of least privilege for all service accounts
- Audit privilege changes and admin actions

## Input Validation Best Practices
- Validate on server side (never trust client)
- Use allowlist/regex for strict validation
- Sanitize HTML input to prevent XSS
- Parameterized queries for all database operations
- Never concatenate user input in SQL, HTML, shell commands
- Validate file uploads: type, size, content scan
- Validate all numeric inputs with range checks
- Use established validation libraries (Zod, Yup, Joi)

## Data Protection Best Practices
- Encrypt PII at rest (AES-256)
- Enforce TLS 1.2+ on all connections
- Never log sensitive data (passwords, tokens, PII)
- Mask PII in logs and error messages
- Implement data retention policies
- Provide data export and deletion capabilities (GDPR)
- Use secure random number generation (crypto.randomBytes)
- Rotate encryption keys periodically

## API Security Best Practices
- Authenticate all endpoints except intentional public ones
- Implement rate limiting (token bucket or sliding window)
- Use CORS allowlist (never `*` for sensitive APIs)
- Validate webhook signatures (HMAC-SHA256)
- Implement idempotency for payment/webhook handlers
- Keep sensitive data out of URLs (use POST body)
- Version APIs from day one
- Document security requirements in OpenAPI spec

## Secrets Management Best Practices
- Store secrets in environment variables or vault
- Never commit secrets to version control
- Rotate secrets regularly (90-day cycle)
- Use different secrets per environment
- Implement secrets audit logging
- Use short-lived credentials where possible
- Never expose secrets in error messages or logs

## Error Handling Best Practices
- Never expose stack traces in production
- Return generic error messages to users
- Log detailed errors server-side with correlation IDs
- Implement circuit breaker for external services
- Handle rate limit errors gracefully with retry-after
- Fail securely (default deny on auth errors)

## Security Headers Best Practices
- Implement CSP with strict directives
- Enable HSTS with max-age >= 31536000
- Set X-Content-Type-Options: nosniff
- Set X-Frame-Options: DENY or SAMEORIGIN
- Set Referrer-Policy: strict-origin-when-cross-origin
- Remove version headers that leak server info

## Dependency Security Best Practices
- Run `npm audit` / `pip check` in CI
- Pin dependency versions in package-lock.json
- Review third-party scripts and CDN resources
- Disable `npm config set ignore-scripts` for untrusted packages
- Use Snyk or Dependabot for vulnerability monitoring
- Keep dependencies updated (monthly review)

## Incident Response Best Practices
- Have incident response plan documented
- Implement security event logging and alerting
- Set up anomaly detection for auth failures
- Define escalation procedures
- Practice incident response with tabletop exercises
- Have rollback procedures ready
- Communicate transparently during incidents
