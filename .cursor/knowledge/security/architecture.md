# Security Knowledge - Architecture

## Security Architecture Principles
- Defense in depth: Multiple security layers
- Zero trust: Never trust, always verify
- Least privilege: Minimum necessary permissions
- Fail securely: Default deny, fail with safe defaults
- Separation of duties: No single point of trust

## Security Layers
```
[Internet] --> [WAF/CDN] --> [Load Balancer] --> [API Server]
                                              |--> [Auth Service]
                                              |--> [Database]
                                              |--> [Cache]
                                              |--> [Queue]
```

### Perimeter Security
- WAF: Protect against OWASP Top 10
- CDN: DDoS protection, rate limiting
- Load Balancer: SSL termination, health checks
- Network segmentation: DMZ for public-facing services

### Application Security
- Auth service: Centralized authentication/authorization
- API Gateway: Rate limiting, auth validation, request routing
- Input validation layer: Sanitize all incoming data
- Output encoding layer: Prevent XSS

### Data Security
- Database: Encryption at rest (AES-256), RLS in PostgreSQL
- Cache (Redis): No sensitive data in plain text
- Queue: Message encryption for sensitive payloads
- Backup: Encrypted backups with key rotation

### Secrets Management Architecture
```
[Application] --> [Vault Agent] --> [Vault Server]
                                     |--> AWS Secrets Manager
                                     |--> Azure Key Vault
                                     |--> HashiCorp Vault
```
- Short-lived credentials preferred
- Secret rotation automated
- Audit logging for all secret access

## Auth Architecture Patterns

### Option 1: JWT Stateless
```
Client --> API Gateway --> Validate JWT --> Resource Server
                |
                +--> Auth Service (issue/refresh JWT)
```
Pros: Scalable, no session storage
Cons: Token revocation is challenging

### Option 2: Session-based
```
Client --> API Gateway --> Session Store (Redis) --> Resource Server
                                    |
                                    +--> Auth Service (issue session)
```
Pros: Easy revocation, server-side control
Cons: Session storage overhead

### Option 3: OAuth2 + API Gateway
```
Client --> Auth Provider --> Access Token --> API Gateway --> Services
                                                  |
                                                  +--> Token Introspection
```
Pros: Centralized auth, supports multiple clients
Cons: Dependency on auth provider

## Security Monitoring Architecture
- Centralized logging: All services log to SIEM
- Metrics: Prometheus + Grafana for security metrics
- Alerting: PagerDuty for critical security events
- Audit trail: Immutable log for compliance
- Anomaly detection: ML-based threat detection

## Incident Response Architecture
- Automated detection: WAF rules, rate limit alerts
- Triage: Automated classification of severity
- Containment: Auto-block IPs, revoke tokens
- Investigation: Centralized log aggregation
- Recovery: Automated rollback capabilities
