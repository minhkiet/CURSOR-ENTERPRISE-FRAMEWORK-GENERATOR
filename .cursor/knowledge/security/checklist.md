# Security Knowledge - Checklist

## Pre-Development
- [ ] Threat model created for new features
- [ ] Security requirements documented
- [ ] Auth model defined (JWT, sessions, OAuth2)
- [ ] Secrets storage strategy defined (vault, env vars, KMS)
- [ ] Data classification completed
- [ ] Compliance requirements identified (GDPR, PCI-DSS, SOC2)

## Authentication & Authorization
- [ ] JWT implementation uses RS256/ES256 (not HS256)
- [ ] Passwords hashed with bcrypt (cost >= 10) or Argon2
- [ ] Session tokens use crypto.randomBytes for randomness
- [ ] Auth tokens have appropriate expiration
- [ ] Authorization checked on every protected endpoint
- [ ] Ownership/resource-level authorization enforced
- [ ] MFA implemented for sensitive operations
- [ ] No hardcoded credentials or API keys in code

## Input Validation & Injection
- [ ] All user input validated before use
- [ ] SQL injection prevention (parameterized queries, ORM)
- [ ] No string concatenation in SQL, HTML, shell commands
- [ ] XSS prevention (output encoding, CSP header)
- [ ] Command injection prevention (no exec/eval with user input)
- [ ] Path traversal prevention (canonicalize paths)
- [ ] File upload validation (type, size, content scan)
- [ ] Number/range validation on all numeric inputs
- [ ] Email/URL validation uses established libraries

## Data Protection
- [ ] Sensitive data not logged (passwords, tokens, PII)
- [ ] Sensitive data encrypted at rest
- [ ] TLS 1.2+ enforced on all external connections
- [ ] Certificate validation enabled (no `verify: false`)
- [ ] PII handled per GDPR/compliance requirements
- [ ] Data minimization applied (collect only necessary)
- [ ] API responses do not leak internal details

## API & Webhook Security
- [ ] All endpoints require authentication (except intentional public)
- [ ] Rate limiting on all endpoints
- [ ] CORS policy correctly configured (not `*` for sensitive APIs)
- [ ] CSRF protection on state-changing operations
- [ ] Webhook signatures verified (HMAC validation)
- [ ] Idempotency enforced on webhook/payment handlers
- [ ] No sensitive data in URLs
- [ ] API versioning in place

## Cryptographic Practices
- [ ] No custom cryptographic implementations
- [ ] Strong random number generation used
- [ ] Keys stored securely (env vars, KMS, vault)
- [ ] Deprecated algorithms avoided (MD5, SHA1 for hashing, DES, 3DES)
- [ ] IV/nonce is unique per encryption operation
- [ ] HTTPS enforced in production (HSTS header)

## Error Handling & Logging
- [ ] No stack traces or internal paths in error responses
- [ ] User-friendly error messages (no system internals)
- [ ] All security events logged (auth failures, authorization denials)
- [ ] Logs do not contain sensitive data
- [ ] Alerting configured for security anomaly patterns

## Supply Chain & Dependencies
- [ ] Lock files committed (package-lock.json, requirements.lock)
- [ ] Dependency audit run in CI (npm audit, pip check)
- [ ] No `@ts-ignore` masking security warnings
- [ ] No deprecated cryptographic libraries
- [ ] Third-party scripts/CDN resources verified (SRI hashes)
- [ ] License compliance checked for all dependencies

## Security Headers
- [ ] CSP header configured
- [ ] HSTS header enabled
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY or SAMEORIGIN
- [ ] Referrer-Policy set appropriately
- [ ] Server version header removed
