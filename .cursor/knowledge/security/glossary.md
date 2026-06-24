# Security Knowledge - Glossary

## Core Concepts

### Authentication
- **JWT (JSON Web Token)**: Stateless token-based authentication
- **OAuth2**: Authorization framework (authorization_code, client_credentials, refresh_token)
- **OIDC (OpenID Connect)**: Identity layer on top of OAuth2
- **Session-based auth**: Server-side session with session ID cookie
- **API Key auth**: Static key for service-to-service communication
- **MFA/2FA**: Multi-factor authentication

### Authorization
- **RBAC (Role-Based Access Control)**: Permissions assigned to roles
- **ABAC (Attribute-Based Access Control)**: Permissions based on attributes
- **Ownership check**: Verifying resource belongs to requester
- **Least privilege**: Grant minimum necessary permissions
- **Defense in depth**: Multiple security layers

### Data Protection
- **Encryption at rest**: Data encrypted when stored
- **Encryption in transit**: TLS/SSL for data in motion
- **PII (Personally Identifiable Information)**: Data that identifies individuals
- **Data minimization**: Collect only necessary data
- **Data retention**: Time-bound storage policies

### Common Vulnerabilities
- **Injection**: SQL, NoSQL, Command, LDAP, OS injection
- **XSS (Cross-Site Scripting)**: Stored, reflected, DOM-based
- **CSRF (Cross-Site Request Forgery)**: Unauthorized actions on behalf of user
- **IDOR (Insecure Direct Object Reference)**: Access to unauthorized resources
- **SSRF (Server-Side Request Forgery)**: Internal resource access from server
- **Broken authentication**: Credential stuffing, weak passwords, session fixation
- **Sensitive data exposure**: Unencrypted data, missing masking
- **Security misconfiguration**: Default credentials, verbose errors, missing hardening
- **Broken access control**: Privilege escalation, CORS misconfiguration

### API Security
- **Rate limiting**: Prevent abuse and DoS
- **Input validation**: Sanitize all user inputs
- **Output encoding**: Prevent XSS
- **Webhook security**: HMAC signature validation
- **CORS**: Cross-Origin Resource Sharing policy
- **API versioning**: Maintain backward compatibility

### Secrets Management
- **Vault**: HashiCorp Vault, Azure Key Vault, AWS Secrets Manager
- **Environment variables**: For non-sensitive config
- **KMS (Key Management Service)**: Cloud-managed encryption keys
- **Secret rotation**: Periodic key rotation policies

### Compliance
- **GDPR**: EU data protection regulation
- **SOC 2**: Security, Availability, Confidentiality
- **PCI-DSS**: Payment card data security
- **HIPAA**: Healthcare data protection
- **ISO 27001**: Information security management

### Security Headers
- **CSP (Content Security Policy)**: Prevent XSS/injection
- **HSTS (HTTP Strict Transport Security)**: Enforce HTTPS
- **X-Content-Type-Options**: Prevent MIME sniffing
- **X-Frame-Options**: Prevent clickjacking
- **Referrer-Policy**: Control referrer information
- **Permissions-Policy**: Control browser feature access

### Threat Modeling
- **STRIDE**: Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege
- **Attack surface**: All entry points to system
- **Trust boundaries**: Lines between different trust levels
- **Threat agents**: Who might attack (internal, external, automated)
