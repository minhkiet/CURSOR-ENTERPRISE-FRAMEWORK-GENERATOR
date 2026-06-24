---
description: Security - Security review (OWASP, vulnerabilities, authentication, authorization)
trigger: security, bảo mật, security review, vulnerability, penetration test, owasp, xss, sqli, csrf
category: Security
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Command: /security

## Mục tiêu
Comprehensive security review theo OWASP Top 10 và các security best practices.

## Trigger Keywords
- security
- bảo mật
- security review
- vulnerability
- penetration test
- owasp
- xss
- sqli
- csrf
- ssrf
- injection
- authentication
- authorization
- jwt
- oauth
- api key
- secret
- cve
- exploit
- malware
- llm security
- prompt injection

## Security Layers

### Authentication & Authorization
- [ ] JWT implementation review
- [ ] Session management review
- [ ] OAuth/OIDC review
- [ ] API key management
- [ ] RBAC/ABAC implementation

### Input Validation
- [ ] SQL injection check
- [ ] XSS check
- [ ] Command injection check
- [ ] Path traversal check
- [ ] File upload validation

### Data Protection
- [ ] Encryption at rest
- [ ] TLS/SSL configuration
- [ ] Secrets management
- [ ] PII handling
- [ ] GDPR compliance

### API Security
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] CSRF protection
- [ ] Webhook signature validation
- [ ] Idempotency

### LLM/AI Security
- [ ] Prompt injection
- [ ] System prompt leakage
- [ ] Output sanitization
- [ ] Tool validation

## Liên kết
- [[../skills/security-audit]] - Security Audit Skill
- [[../skills/security-review]] - Security Review Skill
- [[../rules/security]] - Security Rules
- [[../rules/web-security]] - Web Security Rules
- [[../rules/authentication]] - Authentication Rules
- [[../rules/authorization]] - Authorization Rules
