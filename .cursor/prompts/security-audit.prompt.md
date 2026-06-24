---
description: Prompt chuan de audit bao mat - OWASP, vulnerabilities, auth
trigger: security audit, vulnerability, bao mat
category: Security
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Prompt: Security Audit - Kiểm tra bảo mật

## Mô tả
Prompt template chuẩn để thực hiện security audit toàn diện.

## Trigger Keywords
- "security audit"
- "kiểm tra bảo mật"
- "security review"
- "vulnerability"
- "bảo mật"

## Prompt Template

```markdown
# Security Audit Workflow

## 1. AUDIT SCOPE
- **Audit ID**: [AUDIT-ID]
- **Scope**: [Full / Partial / Component]
- **Domain**: [Xác định domain]
- **Compliance**: [GDPR / SOC2 / ISO27001 / None]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/security/*
- knowledge/api/*
- knowledge/[relevant-stack]/*
Skip: Tất cả domain không liên quan
Load rules: security.mdc, api.mdc
```

## 3. AUDIT CHECKLIST

### Authentication
- [ ] Password policy enforcement
- [ ] MFA/2FA implementation
- [ ] Session management
- [ ] Token storage
- [ ] OAuth/OIDC implementation
- [ ] SAML configuration

### Authorization
- [ ] Role-based access control
- [ ] Permission matrix
- [ ] Row-level security
- [ ] API authorization
- [ ] Tenant isolation

### Data Protection
- [ ] Encryption at rest
- [ ] Encryption in transit
- [ ] Data masking
- [ ] PII handling
- [ ] Data retention
- [ ] Data export

### Input Validation
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] File upload validation
- [ ] API input validation

### Infrastructure
- [ ] TLS configuration
- [ ] Firewall rules
- [ ] Network segmentation
- [ ] Container security
- [ ] secrets-management

## 4. VULNERABILITY SCANNING

### Automated Scan
```bash
# Dependency audit
npm audit / pip audit / dotnet list

# SAST
semgrep scan
bandit scan

# Container scan
trivy image [image-name]
```

### Manual Review
- [ ] Code review for security
- [ ] Configuration review
- [ ] Architecture review
- [ ] Penetration testing

## 5. FINDINGS FORMAT

### Critical
| ID | Finding | Location | Impact |
|----|---------|----------|--------|
| C-001 | [Finding] | [File] | [Impact] |

### High
| ID | Finding | Location | Impact |
|----|---------|----------|--------|
| H-001 | [Finding] | [File] | [Impact] |

### Medium
| ID | Finding | Location | Impact |
|----|---------|----------|--------|
| M-001 | [Finding] | [File] | [Impact] |

### Low
| ID | Finding | Location | Impact |
|----|---------|----------|--------|
| L-001 | [Finding] | [File] | [Impact] |

## 6. REMEDIATION

### Immediate Actions
- [ ] Fix critical vulnerabilities
- [ ] Implement emergency patches
- [ ] Disable affected features

### Short-term Actions
- [ ] Fix high vulnerabilities
- [ ] Implement security controls
- [ ] Update dependencies

### Long-term Actions
- [ ] Security training
- [ ] Security review process
- [ ] Compliance certification

## 7. LIÊN KẾT
- [[../skills/security-audit]] - Security Audit
- [[../rules/security]] - Security Rules
- [[../rules/secrets-management]] - Secrets Management
- [[../rules/api]] - API Rules
- [[../knowledge/security]] - Security Knowledge
