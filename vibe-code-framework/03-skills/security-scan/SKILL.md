# Security Scan Skill

> **Version:** 1.0.0 | **Category:** Security | **Triggers:** security scan, vulnerability scan, OWASP, pentest

---

## Goal

Scan và phát hiện security vulnerabilities:
- OWASP Top 10
- Input validation issues
- Authentication/Authorization flaws
- Data exposure risks
- Dependency vulnerabilities

## Trigger Conditions

- User yêu cầu security scan
- Trước khi deploy to production
- Sau khi có major changes
- Periodic security audit

## Pre-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ P.1: Scope Definition                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Scan scope đã được xác định?                          │
│ □ Endpoints/API boundaries đã map?                       │
│ □ Data flows đã được identified?                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ P.2: Environment                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Có test/staging environment?                          │
│ □ Có test data sẵn?                                      │
│ □ Có authorization cho active scan?                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Process Steps

### Step 1: Reconnaissance

```
┌────────────────────────────────────────────────────────────┐
│ Reconnaissance                                             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Discover endpoints                                  │
│     - API documentation                                 │
│     - Swagger/OpenAPI specs                            │
│     - Crawl application                                 │
│                                                            │
│  2. Identify entry points                               │
│     - Authentication endpoints                         │
│     - Data input points                                 │
│     - File upload endpoints                            │
│                                                            │
│  3. Map attack surface                                  │
│     - External APIs                                    │
│     - Third-party integrations                         │
│     - Admin interfaces                                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 2: Vulnerability Detection

#### OWASP Top 10 Checklist

| # | Category | Checks |
|---|----------|--------|
| A01 | Broken Access Control | IDOR, privilege escalation, CORS misconfig |
| A02 | Cryptographic Failures | Hardcoded secrets, weak crypto, unencrypted data |
| A03 | Injection | SQLi, XSS, Command injection, SSRF |
| A04 | Insecure Design | Missing rate limiting, business logic flaws |
| A05 | Security Misconfiguration | Default credentials, debug mode, verbose errors |
| A06 | Vulnerable Components | Outdated deps, known CVEs |
| A07 | Auth Failures | Weak passwords, session fixation, missing MFA |
| A08 | Data Integrity Failures | XXE, deserialization issues |
| A09 | Logging Failures | Missing audit logs, sensitive data in logs |
| A10 | SSRF | Unvalidated URL redirects |

### Step 3: Manual Testing

```
┌────────────────────────────────────────────────────────────┐
│ Manual Security Testing                                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Authentication:                                          │
│  □ Brute force protection                              │
│  □ Password policy enforcement                          │
│  □ Session timeout                                     │
│  □ MFA implementation                                  │
│                                                            │
│  Authorization:                                           │
│  □ Horizontal privilege separation                      │
│  □ Vertical privilege separation                        │
│  □ IDOR vulnerabilities                                │
│                                                            │
│  Input Validation:                                        │
│  □ All inputs validated                                │
│  □ SQL injection protected                              │
│  □ XSS protected                                       │
│                                                            │
│  Data Protection:                                        │
│  □ Sensitive data encrypted                           │
│  □ PII properly handled                                │
│  □ No secrets in code/logs                            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Step 4: Dependency Scan

```bash
# Node.js
npm audit
npx snyk test

# Python
pip-audit
safety check

# Go
go list -m all | nancy漏洞
trivy module

# .NET
dotnet list package --vulnerable
OWASP Dependency-Check
```

### Step 5: Report

```
┌────────────────────────────────────────────────────────────┐
│ Security Report Template                                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  # Executive Summary                                      │
│  - Overall risk rating                                   │
│  - Number of vulnerabilities found                        │
│  - Critical findings requiring immediate action            │
│                                                            │
│  # Findings                                              │
│  ## [Title]                                             │
│  - Severity: Critical/High/Medium/Low                     │
│  - Location: [File/Endpoint]                             │
│  - Description: [What it is]                            │
│  - Impact: [What could happen]                          │
│  - Proof: [How to reproduce]                           │
│  - Remediation: [How to fix]                            │
│                                                            │
│  # Recommendations                                       │
│  - Immediate actions                                   │
│  - Short-term fixes                                    │
│  - Long-term improvements                               │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Severity Levels

| Level | CVSS | Description | Action |
|-------|------|-------------|--------|
| **Critical** | 9.0-10.0 | RCE, data breach | Immediate fix |
| **High** | 7.0-8.9 | SQLi, XSS | < 1 week |
| **Medium** | 4.0-6.9 | Information disclosure | < 1 month |
| **Low** | 0.1-3.9 | Minor issues | Next release |

## Tools Reference

| Tool | Language | Checks |
|------|----------|--------|
| **semgrep** | Multi | SAST, code patterns |
| **OWASP ZAP** | Web apps | DAST, spider |
| **Burp Suite** | Web apps | Manual + automated |
| **sqlmap** | SQLi | SQL injection |
| **nuclei** | Infrastructure | CVE scanning |
| **trivy** | Containers | Vulnerability scan |

## Post-Check Gates

```
┌─────────────────────────────────────────────────────────────┐
│ C.1: Findings Addressed                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Critical issues fixed?                                  │
│ □ High issues scheduled?                                  │
│ □ Medium issues tracked?                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.2: Verification                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Fixed vulnerabilities re-tested?                         │
│ □ No new vulnerabilities introduced?                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ C.3: Documentation                                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Report documented?                                      │
│ □ Remediation tracked in tickets?                         │
│ □ Lessons learned shared?                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Output

```
✅ Security Scan Complete
├── Findings report
├── Risk assessment
├── Remediation plan
└── Follow-up tickets
```
