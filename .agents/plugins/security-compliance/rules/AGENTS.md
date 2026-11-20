# Security & Compliance Plugin Rules

Assume breach, verify defense. Every code modification must satisfy rigorous security gates:

## Security Quality Gates
1. **Zero Hardcoded Secrets**: Never commit API keys, private tokens, passwords, or credentials. Use environment variables.
2. **Input Validation**: All external inputs must be validated and sanitized at boundaries. Use parameterized SQL queries.
3. **OWASP Top 10 Guard**: Eliminate SQL injection, XSS, SSRF, broken access control, and insecure deserialization.
4. **Payment Gateway Safety**:
   - Verify webhook checksums / HMAC signatures (PayOS, SePay, MoMo, VNPay).
   - Implement idempotent transaction processing with order status locks.
   - Never log raw credit cards or sensitive PII.
