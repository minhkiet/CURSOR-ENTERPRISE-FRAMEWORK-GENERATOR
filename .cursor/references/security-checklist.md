# Security Checklist Reference

> Based on [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) references

---

## Pre-Commit Security Checks

### Required Before Every Commit

- [ ] No secrets/credentials in code
- [ ] No API keys hardcoded
- [ ] Environment variables used for secrets
- [ ] Dependencies audited (`npm audit`)
- [ ] No deprecated crypto libraries
- [ ] Lock files committed (package-lock.json, yarn.lock)

### Git Hooks (Recommended)

```bash
# pre-commit hook to scan for secrets
npm install --save-dev git-scripts-scan
```

---

## Authentication & Authorization

### Authentication

- [ ] No hardcoded credentials
- [ ] Passwords hashed (bcrypt cost >= 10, or Argon2)
- [ ] Session tokens random and non-guessable
- [ ] Auth tokens expire appropriately
  - Access token: 15-60 minutes
  - Refresh token: 7-30 days
- [ ] MFA available for sensitive operations
- [ ] Account lockout after failed attempts (configurable)

### Authorization

- [ ] RBAC/ABAC implemented correctly
- [ ] Every endpoint checks permissions
- [ ] Resource-level authorization enforced
- [ ] Least privilege principle applied
- [ ] No privilege escalation possible
- [ ] Admin actions logged

---

## Input Validation

### General

- [ ] All user input validated before use
- [ ] Whitelist over blacklist validation
- [ ] Sanitize HTML/JSON/XML input
- [ ] Validate content types match expectations
- [ ] Reject unexpected parameters

### Injection Prevention

| Type | Prevention |
|------|------------|
| SQL Injection | Parameterized queries, ORM |
| XSS | Output encoding, CSP |
| Command Injection | No exec/eval with user input |
| Path Traversal | Canonicalize paths |
| LDAP Injection | Escape special characters |
| XXE | Disable external entities |

### File Uploads

- [ ] File type validation (magic bytes, not just extension)
- [ ] File size limits enforced
- [ ] Filename sanitization
- [ ] Content scanning (if possible)
- [ ] Files stored outside webroot
- [ ] Execution disabled on upload directory

---

## Data Protection

### Sensitive Data

- [ ] No PII in logs
- [ ] No passwords/tokens in logs
- [ ] Credit card data never stored
- [ ] Encryption at rest for sensitive data
- [ ] TLS 1.2+ enforced
- [ ] Certificate validation enabled

### Secrets Management

- [ ] Secrets in env vars or vault
- [ ] No secrets in code
- [ ] No secrets in version control
- [ ] Rotation strategy in place
- [ ] Secrets scoped to minimum needed

### Error Handling

- [ ] No stack traces in responses
- [ ] No internal paths leaked
- [ ] Generic error messages for users
- [ ] Detailed errors logged server-side
- [ ] Fail securely (default deny)

---

## API Security

### Endpoint Security

- [ ] Authentication required (except public)
- [ ] Rate limiting on all endpoints
- [ ] CORS configured correctly
- [ ] Not `Access-Control-Allow-Origin: *` for sensitive APIs
- [ ] API versioning in place
- [ ] No sensitive data in URLs

### Webhook Security

- [ ] Signature verification (HMAC)
- [ ] Idempotency enforced
- [ ] Replay attack prevention
- [ ] Timeout handling
- [ ] Error handling doesn't leak info

### CSRF Protection

- [ ] CSRF tokens for state-changing operations
- [ ] Double-submit cookie pattern (if stateless)
- [ ] SameSite cookies
- [ ] Origin/Referer header validation

---

## OWASP Top 10 (2021)

### A01: Broken Access Control

- [ ] Access control enforced on every request
- [ ] Deny by default
- [ ] Minimize CORS usage
- [ ] Rate limit API to minimize automated attacks
- [ ] Invalidate sessions on logout

### A02: Cryptographic Failures

- [ ] Sensitive data encrypted
- [ ] Strong algorithms (AES-256, RSA-2048+)
- [ ] No deprecated algorithms (MD5, SHA1 for hashing)
- [ ] Proper IV/nonce generation
- [ ] Secure random number generation

### A03: Injection

- [ ] Parameterized queries
- [ ] Input validation
- [ ] Escape shell arguments
- [ ] Sanitize HTML output

### A04: Insecure Design

- [ ] Threat modeling done
- [ ] Secure defaults
- [ ] Principle of least privilege
- [ ] Fail securely

### A05: Security Misconfiguration

- [ ] Hardened configuration
- [ ] Unnecessary features disabled
- [ ] Error handling configured
- [ ] Security headers set
- [ ] Cloud storage not public

### A06: Vulnerable Components

- [ ] Keep dependencies updated
- [ ] Remove unused dependencies
- [ ] Monitor for CVE
- [ ] Only use official sources

### A07: Authentication Failures

- [ ] Weak password enforcement
- [ ] Credential recovery process secure
- [ ] Session management secure
- [ ] Multi-factor authentication available

### A08: Data Integrity Failures

- [ ] Code/data integrity verified
- [ ] Signed updates
- [ ] No sensitive data in URLs
- [ ] Integrity checks on files

### A09: Logging & Monitoring

- [ ] Log security events
- [ ] Monitor for attacks
- [ ] Alert on anomalies
- [ ] Logs retained appropriately

### A10: Server-Side Request Forgery (SSRF)

- [ ] Validate URLs
- [ ] Allowlist for remote resources
- [ ] Segment networks
- [ ] Deny by default

---

## Security Headers

```http
# Recommended Security Headers
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

---

## Dependency Audit Commands

```bash
# npm
npm audit
npm audit fix

# Python
pip check
safety check

# Docker
trivy image <image>
grype <image>

# Go
go mod verify
gosec ./...
```

---

## Links

- [agent-skills](https://github.com/addyosmani/agent-skills) - Source reference
- [[security-review]] - Security skill
- [[skill-registry]] - Security skill triggers
