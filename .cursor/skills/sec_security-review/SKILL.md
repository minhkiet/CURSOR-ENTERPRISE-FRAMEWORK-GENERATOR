---
name: security-review
description: Comprehensive security review skill for code analysis, vulnerability detection, and penetration testing. Covers OWASP Top 10, LLM/AI Security (ASI Top 10), supply chain security, API security, and reverse-engineering workflows. Use when reviewing code for security vulnerabilities, when user mentions security, vulnerability, penetration test, OWASP, XSS, SQL injection, or when handling sensitive integrations.
---

# Security Review Skill

## Overview

Security review is a mandatory gate for all code involving authentication, authorization, payment, data handling, API endpoints, and external integrations. This skill activates on security/vulnerability keywords and provides layered review:

```
Layer 1: Static Analysis (always runs)
Layer 2: OWASP Top 10 + ASVS Check
Layer 3: LLM/AI Security (ASI Top 10)
Layer 4: API/Webhook Security
Layer 5: Supply Chain & Secrets
Layer 6: Advanced RE (reverse-skill routing)
```

---

## Pre-Review Gate (Before Writing Code)

### S.1 Threat Modeling

Before implementing any security-sensitive feature, document:

- **Attack surface**: What inputs are controlled by untrusted actors?
- **Trust boundaries**: Where does external data cross into trusted systems?
- **Assets at risk**: What would an attacker gain from a compromise?
- **Potential threats**: List top 3 threats based on the feature type

### S.2 Security Requirements

Identify and document:

- [ ] Authentication requirements (what needs auth, what doesn't)
- [ ] Authorization model (RBAC, ABAC, ownership checks)
- [ ] Data classification (public, internal, sensitive, restricted)
- [ ] Compliance requirements (GDPR, PCI-DSS, SOC2, etc.)
- [ ] Encryption requirements (at rest, in transit)
- [ ] Audit logging requirements

### S.3 Security Design Review

For any new endpoint, API, or integration:

- [ ] Input validation strategy defined
- [ ] Output encoding strategy defined
- [ ] Error handling does not leak sensitive information
- [ ] Rate limiting strategy defined
- [ ] Authentication method selected (JWT, sessions, API keys, OAuth2)
- [ ] Authorization model defined (who can call what)
- [ ] Secrets storage strategy (env vars, vault, KMS)
- [ ] Logging strategy for security events

---

## Post-Review Gate (After Code)

### Security-1: Authentication & Authorization

- [ ] No hardcoded credentials, API keys, or secrets in code
- [ ] Authentication tokens have appropriate expiration
- [ ] Passwords hashed with strong algorithms (bcrypt, Argon2, PBKDF2)
- [ ] Session tokens are random, non-guessable
- [ ] Authorization checks on every protected endpoint
- [ ] Ownership/resource-level authorization enforced
- [ ] Privilege escalation prevented (least privilege)
- [ ] No authentication bypass (test edge cases)

### Security-2: Input Validation & Injection

- [ ] All user input validated before use
- [ ] SQL injection prevention (parameterized queries, ORM)
- [ ] No string concatenation/interpolation in SQL, HTML, or shell commands
- [ ] XSS prevention (output encoding, CSP, Content-Security-Policy)
- [ ] Command injection prevention (no `exec`, `eval`, `spawn` with user input)
- [ ] Path traversal prevention (canonicalize paths, whitelist allowed paths)
- [ ] Deserialization vulnerabilities addressed
- [ ] File upload validation (type, size, content scanning)
- [ ] Email/URL validation uses established libraries
- [ ] Number/range validation on all numeric inputs

### Security-3: Data Protection

- [ ] Sensitive data not logged (passwords, tokens, PII)
- [ ] Sensitive data encrypted at rest (database fields, files)
- [ ] TLS 1.2+ enforced on all external connections
- [ ] Certificate validation enabled (no `verify: false` in production)
- [ ] Secrets not in environment variable names that get logged
- [ ] PII handled per GDPR/compliance requirements
- [ ] Data minimization: only collect/store what is necessary
- [ ] Secure deletion of sensitive data when no longer needed
- [ ] API responses do not leak internal details (stack traces, paths)

### Security-4: API & Webhook Security

- [ ] All endpoints require authentication (except intentional public ones)
- [ ] Rate limiting on all endpoints
- [ ] CORS policy correctly configured (not `*` for sensitive APIs)
- [ ] CSRF protection on state-changing operations
- [ ] Webhook signatures verified (HMAC validation)
- [ ] Idempotency enforced on webhook/payment handlers
- [ ] Webhook replay attack prevention (timestamp validation)
- [ ] No sensitive data in URLs (use POST body for secrets)
- [ ] API versioning strategy in place
- [ ] OpenAPI spec matches implementation

### Security-5: LLM / AI Security (ASI Top 10)

- [ ] Prompt injection: user input sanitized before LLM context
- [ ] No system prompt leakage (defense-in-depth)
- [ ] Output filtering: LLM responses sanitized before display/storage
- [ ] Rate limiting on LLM calls (token budget, request budget)
- [ ] Sensitive data not sent to LLM (PII redaction before context)
- [ ] Tool/function call validation (no unsafe tool execution)
- [ ] Resource exhaustion prevention (max tokens, max steps)
- [ ] Jailbreak resistance (prompt boundary enforcement)
- [ ] Agentic action approval: sensitive actions require human confirmation
- [ ] LLM-specific audit logging for compliance

### Security-6: Supply Chain & Dependencies

- [ ] No `npm install --legacy-peer-deps` or `pip install --trusted-host`
- [ ] Lock files committed and reviewed (`package-lock.json`, `requirements.lock`)
- [ ] Dependency audit run: `npm audit`, `pip check`, `safety check`
- [ ] No `@ts-ignore` or `// eslint-disable` masking security warnings
- [ ] No deprecated cryptographic libraries
- [ ] Known vulnerable patterns checked (checkmarx, snyk, semgrep rules)
- [ ] Third-party scripts/CDN resources verified (integrity hashes)
- [ ] No telemetry/analytics sending data without disclosure
- [ ] License compliance checked for all dependencies

### Security-7: Cryptographic Practices

- [ ] No custom cryptographic implementations
- [ ] Strong random number generation used (`crypto.getRandomValues`, `secrets.token_bytes`)
- [ ] Keys have appropriate rotation periods
- [ ] Key storage follows best practices (env vars, KMS, vault)
- [ ] Deprecated algorithms avoided (MD5, SHA1 for hashing, DES, 3DES)
- [ ] IV/nonce is unique per encryption operation
- [ ] Password-based key derivation uses appropriate parameters
- [ ] JWT signed with RS256/ES256, not HS256 with shared secrets across services
- [ ] HTTPS enforced in production (HSTS header)

### Security-8: Error Handling & Logging

- [ ] No stack traces or internal paths in error responses
- [ ] Error messages are user-friendly, not revealing system internals
- [ ] All security events logged (auth failures, authorization denials, input validation failures)
- [ ] Logs do not contain sensitive data (redact PII, tokens, passwords)
- [ ] Log integrity: logs are append-only, tampering detectable
- [ ] Log aggregation covers all security-relevant events
- [ ] Alerting configured for security anomaly patterns

---

## Advanced Reverse-Engineering Review (Security-9)

When the task involves APK, binary, frontend JS, or firmware analysis:

### Security-9.1 APK / Android Review

- [ ] SSL pinning implemented and bypass-tested
- [ ] Root/jailbreak detection in place (defense-in-depth, not relied upon solely)
- [ ] No hardcoded API keys or secrets in APK
- [ ] Obfuscation applied (ProGuard, R8, DexGuard)
- [ ] Debug flags disabled in release builds
- [ ] Certificate validation cannot be bypassed via Frida
- [ ] Native libraries reviewed for exposed JNI interfaces
- [ ] SharedPreferences / storage properly encrypted

### Security-9.2 Frontend / JS Security Review

- [ ] No secrets or API keys in frontend code or bundled JS
- [ ] Environment variables prefixed correctly (public vs private)
- [ ] Source maps disabled in production
- [ ] Sensitive data not stored in localStorage/sessionStorage
- [ ] Request signing implemented for API calls
- [ ] WebSocket connections use WSS (TLS)
- [ ] Content Security Policy (CSP) configured
- [ ] Subresource Integrity (SRI) on CDN scripts
- [ ] Clickjacking protection (X-Frame-Options, CSP frame-ancestors)
- [ ] MIME type sniffing prevented (X-Content-Type-Options)

### Security-9.3 Binary / Firmware Review

- [ ] Firmware integrity verified (signature validation)
- [ ] No hardcoded credentials or backdoor accounts
- [ ] Secure boot chain documented
- [ ] Default credentials changed or disabled
- [ ] Debug interfaces disabled in production builds
- [ ] Memory protection: NX, ASLR, stack canaries verified
- [ ] OTA update mechanism uses signed updates

---

## Output Format

### Pre-Review Output

```
══════════════════════════════════════
[SECURITY PRE-REVIEW GATE]
══════════════════════════════════════

Threat Model:
- Attack Surface: [described]
- Trust Boundaries: [identified]
- Top Threats: [1, 2, 3]

Security Requirements Locked:
- Auth Model: [defined]
- Data Classification: [level]
- Compliance: [list]

Design Review: [N/N PASS]

>>> SECURITY APPROVED — Proceed with implementation
```

### Post-Review Output

```
══════════════════════════════════════
[SECURITY POST-REVIEW GATE]
══════════════════════════════════════

Gate Results:
  ✓ Authentication & Authorization: PASS
  ✓ Input Validation & Injection:   PASS
  ✓ Data Protection:               PASS
  ✓ API & Webhook Security:        PASS
  ✓ LLM / AI Security:             PASS (if applicable)
  ✓ Supply Chain & Dependencies:    PASS
  ✓ Cryptographic Practices:        PASS
  ✓ Error Handling & Logging:      PASS
  ✓ Advanced RE Review:             PASS (if applicable)

Total Items Checked: N+

Reviewer Notes:
- [Any findings and their severity]

Severity Scale: CRITICAL > HIGH > MEDIUM > LOW > INFO
```

---

## Severity & Remediation

| Severity | Action |
|----------|--------|
| CRITICAL | Fix before merge, mandatory |
| HIGH | Fix before merge, mandatory |
| MEDIUM | Fix within sprint, tracked |
| LOW | Fix within next release, tracked |
| INFO | Consider for future improvement |

**CRITICAL and HIGH findings must be fixed before delivery. No exceptions.**

---

## Reference & Advanced Topics

For detailed vulnerability patterns, exploit techniques, and advanced reverse-engineering workflows, see:

- [reference.md](reference.md) — Detailed vulnerability patterns, exploit examples, and mitigation strategies
- [reverse-skill package](https://github.com/zhaoxuya520/reverse-skill) — Advanced RE workflows for APK, binary, JS, firmware analysis

### Reverse-Skill Integration

When handling APK/binary/JS reverse-engineering for security purposes:

1. **APK Security**: Read `apk-reverse\SKILL.md` from reverse-skill for APK decompilation, Frida hooking, and certificate pinning bypass analysis
2. **Binary Analysis**: Read `ida-reverse\SKILL.md` or `radare2\SKILL.md` for native binary analysis
3. **JS Reverse**: Read `js-reverse\SKILL.md` for frontend signature analysis and environment simulation
4. **Firmware**: Read `firmware-pentest\SKILL.md` for IoT/firmware security testing
5. **Pentest**: Read `pentest-tools\SKILL.md` for network-level penetration testing workflows
6. **LLM Security**: Read `llm-security\` in reverse-skill for OWASP LLM + ASI Top 10 deep-dives

For full integration details (tool availability, MCP setup, quick commands), see [reverse-skill-integration.md](reverse-skill-integration.md).

### Common Vulnerability Quick Reference

| Category | Top Issues |
|----------|-----------|
| Injection | SQLi, XSS, Command Injection, LDAP Injection, XXE |
| Auth | Broken Auth, Credential Stuffing, Session Fixation |
| Sensitive Data | Data Exposure, Insecure Storage, Transport Risk |
| XXE | XML External Entity parsing |
| Access Control | IDOR, BOLA, Broken Access Control |
| Misconfiguration | Debug enabled, Default creds, Error verbose |
| XSS | Reflected, Stored, DOM-based, CSP bypass |
| Deserialization | Insecure deserialization, YAML loading |
| Vulnerable Components | Outdated deps, Known CVEs |
| Insufficient Logging | No audit trail, Missing alerts |

---

## Trigger Keywords

Activate this skill when encountering:

- security, vulnerability, CVE, exploit, penetration test
- OWASP, ASVS, WAF, firewall, rate limit
- authentication, authorization, RBAC, permission, access control
- injection, XSS, SQLi, SSRF, CSRF, XXE
- encryption, cryptography, hashing, signing, JWT, OAuth
- API key, secret, credential, token, session
- webhook, callback, IPN, payment, MoMo, SePay, PayOS, ZaloPay, VNPay, VietQR
- APK, binary, decompile, reverse, Frida, hooking
- LLM, AI, prompt injection, prompt leakage, jailbreak
- CORS, CSP, HTTPS, TLS, HSTS, certificate
- GDPR, compliance, PII, data protection, privacy
- supply chain, dependency, npm audit, vulnerability scan
- malware, backdoor, rootkit, forensic analysis


---

## Liens

- [[../rules/skill-integration]] - Skill Integration Rules
- [[../rules/security]] - Security Rules
- [[../rules/web-security]] - Web Security Rules
- [[../rules/authentication]] - Authentication Rules
- [[../rules/authorization]] - Authorization Rules
- [[../knowledge/security]] - Security Knowledge
- [[../skills/vietnam-payment-review]] - Vietnam Payment Review Skill
