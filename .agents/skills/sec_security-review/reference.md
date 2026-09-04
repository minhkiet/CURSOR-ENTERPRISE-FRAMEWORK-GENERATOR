# Security Review — Detailed Reference

## A. Detailed Vulnerability Patterns & Mitigations

### A.1 Injection Attacks

#### SQL Injection

```typescript
// VULNERABLE — Never do this
const query = `SELECT * FROM users WHERE id = ${userId}`;

// SECURE — Parameterized queries
const query = `SELECT * FROM users WHERE id = $1`;
await db.query(query, [userId]);

// VULNERABLE — ORM but raw SQL
await db.query(`SELECT * FROM orders WHERE user_id = ${userId}`);

// SECURE — ORM with proper escaping
await db.orders.findMany({ where: { userId } });
```

Detection patterns (grep your codebase):
- String concatenation with SQL: `` `${`SELECT`} ``, `"SELECT " +`, `\`SELECT \${`
- Template literals with SQL keywords + user input
- Raw `query()` / `execute()` with string interpolation

#### XSS — Cross-Site Scripting

```typescript
// VULNERABLE — Direct HTML injection
res.send(`<h1>${userInput}</h1>`);
element.innerHTML = userInput;

// VULNERABLE — React dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{ __html: userContent }} />

// SECURE — Output encoding (React auto-escapes by default)
<div>{userInput}</div>

// SECURE — DOMPurify for trusted HTML
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(dirty);

// SECURE — CSP header
res.set('Content-Security-Policy', "default-src 'self'; script-src 'self'");
```

Detection patterns:
- `innerHTML`, `outerHTML`, `insertAdjacentHTML`
- `document.write`, `document.writeln`
- `dangerouslySetInnerHTML` (audit each use)
- No output encoding on user-controlled data

#### Command Injection

```typescript
// VULNERABLE — Never pass user input to shell
exec(`ls ${userPath}`);
spawn(`npm install ${userPackage}`);
child_process.execSync(`git clone ${userRepo}`);

// SECURE — Whitelist approach
const allowed = ['/safe/path1', '/safe/path2'];
if (!allowed.includes(userPath)) throw new Error('Invalid path');
exec(`ls ${sanitizedPath}`);

// SECURE — Pass arguments as array (no shell expansion)
spawn('ls', [userPath], { shell: false });
```

#### SSRF — Server-Side Request Forgery

```typescript
// VULNERABLE — User controls URL
const image = await fetch(userProvidedUrl);

// SECURE — Validate URL before fetching
const url = new URL(userProvidedUrl);
if (!['http:', 'https:'].includes(url.protocol)) throw new Error('Invalid protocol');
if (BLOCKED_HOSTS.includes(url.hostname)) throw new Error('Blocked host');
const response = await fetch(url);

// SECURE — Use request library with SSRF protection
const options = { ...ssrfFilter, url: userProvidedUrl };
```

#### XXE — XML External Entity

```typescript
// VULNERABLE — XML parsing without disabling entities
const parser = new xml2js.Parser();
parser.parseString(userXml);

// SECURE — Disable external entities
const parser = new xml2js.Parser({ explicit: false });
// Or use fast-xml-parser with validation
```

#### LDAP Injection

Always use parameterized LDAP queries; never concatenate user input into LDAP search filters.

---

### A.2 Authentication & Session Security

#### JWT Best Practices

```typescript
// VULNERABLE — HS256 with shared secret in multiple services
const token = jwt.sign(payload, 'shared-secret'); // breaks if any service is compromised

// SECURE — RS256 with asymmetric keys
const privateKey = fs.readFileSync('private.pem');
const token = jwt.sign(payload, privateKey, { algorithm: 'RS256' });
// Verify with public key (each service has only the public key)

// SECURE — Short-lived tokens + refresh tokens
const accessToken = jwt.sign({ sub: userId }, privateKey, { expiresIn: '15m' });
const refreshToken = jwt.sign({ sub: userId, type: 'refresh' }, refreshKey, { expiresIn: '7d' });

// ALWAYS — Include necessary claims
jwt.sign({
  sub: userId,
  iat: Math.floor(Date.now() / 1000),
  exp: Math.floor(Date.now() / 1000) + 900, // 15 minutes
  iss: 'your-service',
  aud: 'your-api',
}, privateKey);
```

#### Password Hashing

```typescript
// SECURE — bcrypt
const bcrypt = require('bcrypt');
const hash = await bcrypt.hash(password, 12); // cost factor 10-12
const match = await bcrypt.compare(password, hash);

// SECURE — Argon2 (better than bcrypt for new projects)
const argon2 = require('argon2');
const hash = await argon2.hash(password, { type: argon2.argon2id });
```

#### Session Management

```typescript
// SECURE — Secure session configuration
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,   // No JS access
    secure: true,     // HTTPS only
    sameSite: 'strict', // CSRF protection
    maxAge: 3600000   // 1 hour
  }
}));
```

---

### A.3 Authorization & Access Control

#### IDOR — Insecure Direct Object Reference

```typescript
// VULNERABLE — User can access any document
app.get('/documents/:id', async (req, res) => {
  const doc = await db.documents.findById(req.params.id);
  res.json(doc);
});

// SECURE — Ownership check
app.get('/documents/:id', async (req, res) => {
  const doc = await db.documents.findById(req.params.id);
  if (!doc) return res.status(404).json({ error: 'Not found' });
  if (doc.ownerId !== req.user.id) return res.status(403).json({ error: 'Forbidden' });
  res.json(doc);
});

// SECURE — Use middleware for common patterns
const requireOwnership = (resource) => async (req, res, next) => {
  const resource = await db[resource].findById(req.params.id);
  if (!resource) return res.status(404).json({ error: 'Not found' });
  if (resource.userId !== req.user.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  req.resource = resource;
  next();
};
```

#### BOLA — Broken Object Level Authorization

When exposing list endpoints, always filter by the authenticated user's ID:
```typescript
// VULNERABLE — Returns all orders to any authenticated user
const orders = await db.orders.findAll();

// SECURE — Filter by current user
const orders = await db.orders.findAll({ where: { userId: req.user.id } });
```

---

### A.4 Data Protection

#### Sensitive Data Exposure in Logs

```typescript
// VULNERABLE — Leaking sensitive fields
logger.info('Payment processed', { amount, cardNumber, cvv });

// SECURE — Redact sensitive fields
logger.info('Payment processed', {
  amount,
  cardNumber: cardNumber.replace(/.(?=.{4})/g, '*'), // ****1234
  // cvv omitted entirely
});
```

#### Environment Variables for Secrets

```typescript
// VULNERABLE — Hardcoded secrets
const apiKey = 'sk_live_abc123';

// SECURE — Environment variables (never log these)
const apiKey = process.env.PAYMENT_API_KEY;
if (!apiKey) throw new Error('PAYMENT_API_KEY not configured');

// SECURE — Zod validation for env vars at startup
import { z } from 'zod';
const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(32),
  REDIS_URL: z.string().url(),
});
const env = envSchema.parse(process.env);
```

---

### A.5 Webhook Security

```typescript
// SECURE — Verify webhook signatures (MoMo example)
import crypto from 'crypto';

function verifyMomoWebhook(payload: object, signature: string, secretKey: string): boolean {
  const raw = Object.keys(payload)
    .sort()
    .map(key => `${key}=${payload[key as keyof typeof payload]}`)
    .join('&');
  const expected = crypto.createHmac('sha256', secretKey).update(raw).digest('hex');
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
}

// SECURE — Idempotency check
async function handleWebhook(event: WebhookEvent) {
  const processed = await db.webhookEvents.findUnique({
    where: { providerEventId: event.id }
  });
  if (processed) {
    return { status: 'already_processed', duplicate: true };
  }

  await db.$transaction(async (tx) => {
    await tx.webhookEvents.create({
      data: { providerEventId: event.id, status: 'processing' }
    });
    await processPaymentEvent(tx, event);
  });

  return { status: 'processed' };
}

// SECURE — Timestamp validation for replay attack prevention
function validateWebhookTimestamp(timestamp: number, maxAgeSeconds = 300): boolean {
  const now = Math.floor(Date.now() / 1000);
  const age = now - timestamp;
  return age >= 0 && age <= maxAgeSeconds;
}
```

---

### A.6 LLM / AI Security (ASI Top 10)

See also: reverse-skill `llm-security\` directory for OWASP LLM Top 10 and ASI Top 10 deep-dives.

#### Prompt Injection

```typescript
// VULNERABLE — User input directly in system prompt
const prompt = `System: ${userInput}\nAssistant:`;

// SECURE — Isolate system prompt from user input
const systemPrompt = `You are a helpful assistant. Always be helpful and accurate.`;
const messages = [
  { role: 'system', content: systemPrompt },
  { role: 'user', content: sanitizeUserInput(userInput) },
];

// SECURE — Sanitization function
function sanitizeUserInput(input: string): string {
  return input
    .replace(/^system:/imi, '[blocked]')
    .replace(/^ignore previous/imi, '[blocked]')
    .slice(0, MAX_INPUT_LENGTH);
}

// SECURE — Prompt boundary markers
const BOUNDARY = '###INPUT###';
const messages = [
  { role: 'system', content: `${SYSTEM_PROMPT}\nUser input will be separated by: ${BOUNDARY}` },
  { role: 'user', content: `${BOUNDARY}\n${sanitizeUserInput(raw)}` },
];
```

#### Tool/Function Call Validation

```typescript
// SECURE — Validate tool call parameters
const toolSchemas = {
  send_email: {
    allowedParams: ['to', 'subject', 'body'],
    requiredParams: ['to', 'body'],
    maxLength: { to: 254, body: 10000 }
  }
};

function validateToolCall(toolName: string, params: object): void {
  const schema = toolSchemas[toolName];
  if (!schema) throw new Error(`Tool '${toolName}' not allowed`);

  for (const required of schema.requiredParams) {
    if (!(required in params)) throw new Error(`Missing required param: ${required}`);
  }

  for (const [key, value] of Object.entries(params)) {
    if (!schema.allowedParams.includes(key)) throw new Error(`Disallowed param: ${key}`);
    if (typeof value === 'string' && schema.maxLength?.[key] && value.length > schema.maxLength[key]) {
      throw new Error(`Param '${key}' exceeds max length`);
    }
  }
}
```

#### Resource Exhaustion Prevention

```typescript
// SECURE — Token and step limits
const MAX_TOKENS = 4000;
const MAX_STEPS = 10;

let stepCount = 0;
for (const message of conversation) {
  stepCount++;
  if (stepCount > MAX_STEPS) {
    throw new Error('Maximum conversation steps exceeded');
  }
}

// SECURE — Token budget enforcement
function enforceTokenBudget(messages: Message[], maxTokens: number): Message[] {
  let totalTokens = estimateTokens(messages);
  while (totalTokens > maxTokens && messages.length > 2) {
    totalTokens -= estimateTokens(messages.splice(1, 1));
  }
  return messages;
}
```

---

### A.7 Cryptographic Anti-Patterns

```typescript
// VULNERABLE — MD5/SHA1 for hashing passwords
const hash = crypto.createHash('md5').update(password).digest('hex'); // NEVER

// VULNERABLE — DES/3DES encryption
const cipher = crypto.createCipher('des-ecb', key); // DEPRECATED

// VULNERABLE — Using random module instead of crypto for secrets
const token = Math.random().toString(36).slice(2); // PREDICTABLE

// SECURE — crypto.randomBytes for secrets
const token = crypto.randomBytes(32).toString('hex');

// SECURE — AES-256-GCM for encryption
const iv = crypto.randomBytes(12);
const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
const encrypted = Buffer.concat([cipher.update(plaintext), cipher.final()]);
const authTag = cipher.getAuthTag();
return { iv, encrypted, authTag }; // Store all three

// SECURE — Unique IV per encryption
const iv = crypto.randomBytes(12); // NEVER reuse IVs
```

---

### A.8 API Security Patterns

#### CORS Configuration

```typescript
// VULNERABLE — Permissive CORS
app.use(cors({ origin: '*' })); // Never on production APIs

// SECURE — Explicit whitelist
app.use(cors({
  origin: ['https://app.example.com', 'https://admin.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400,
}));
```

#### Rate Limiting

```typescript
// SECURE — Per-IP and per-user rate limiting
import rateLimit from 'express-rate-limit';

const standardLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: { error: 'Too many requests, please try again later' },
  standardHeaders: true,
  legacyHeaders: false,
});

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // Strict limit on auth endpoints
  skipSuccessfulRequests: true, // Only count failures
  message: { error: 'Too many authentication attempts' },
});

app.use('/api/', standardLimiter);
app.use('/api/auth/', authLimiter);
```

#### HSTS Header

```typescript
// SECURE — HSTS in production
if (process.env.NODE_ENV === 'production') {
  app.use((req, res, next) => {
    res.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');
    res.set('X-Content-Type-Options', 'nosniff');
    res.set('X-Frame-Options', 'DENY');
    res.set('X-XSS-Protection', '1; mode=block');
    res.set('Referrer-Policy', 'strict-origin-when-cross-origin');
    res.set('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');
    next();
  });
}
```

---

## B. Dependency Security Audit

### B.1 Running Audits

```bash
# Node.js
npm audit
npm audit --audit-level=high
npx snyk test
npx npm-check-updates --upgrade

# Python
pip-audit
safety check
pip freeze | pip-review
bandit -r ./src

# Go
npx retire --golang

# All
snyk test
```

### B.2 Semgrep Rules for Common Vulnerabilities

```yaml
# .semgrep/security-rules.yaml
rules:
  - id: sql-injection
    pattern: query(`SELECT ... ${$VAR}`)
    message: "Possible SQL injection. Use parameterized queries."
    severity: ERROR
    languages: [javascript, typescript]

  - id: hardcoded-secret
    pattern: const $KEY = '$STRING';
    message: "Hardcoded secret detected. Use environment variables."
    severity: ERROR
    languages: [javascript, typescript]
    metadata:
      owasp: 'A02:2021 - Cryptographic Failures'
```

---

## C. Reverse-Skill Module Reference

When you need advanced reverse-engineering capabilities for security analysis:

| Module | Path in reverse-skill | Use Case |
|--------|---------------------|----------|
| Main routing | `SKILL.md`, `routing.md` | Entry point for all RE tasks |
| APK RE | `apk-reverse\SKILL.md` | Decompile APK, Frida hooking, certificate pinning |
| IDA Pro RE | `ida-reverse\SKILL.md` | Deep binary analysis, decompilation, xrefs |
| radare2 RE | `radare2\SKILL.md` | CLI binary analysis, patching |
| JS Reverse | `js-reverse\SKILL.md` | Frontend signature, encrypted params, webpack |
| Pentest | `pentest-tools\SKILL.md` | Nmap, Nuclei, SQLMap, FFUF, Hashcat |
| EDR Bypass | `edr-bypass-re\SKILL.md` | Reverse EDR hooks, syscall direct, AMSI bypass |
| Firmware | `firmware-pentest\SKILL.md` | IoT firmware extraction, emulation, fuzzing |
| Pwn Chain | `pwn-chain\SKILL.md` | Stack/heap pwn, exploit writing, pwntools |
| LLM Security | `llm-security\` | OWASP LLM Top 10, ASI Top 10, agent security |
| Field Journal | `field-journal\` | Auto-evolving experience logs from past engagements |

### Quick Reverse-Skill Entry

```bash
# Refresh tool index (required first step on any machine)
powershell -File "<REVERSE_SKILL_ROOT>\skills\scripts\refresh-tool-index.ps1"

# Tool availability check
jadx --version
apktool --version
frida-ps -U
r2 -v
node -v
```

### IDA Pro MCP Setup (for binary analysis)

```powershell
# 1. Set IDADIR
[Environment]::SetEnvironmentVariable('IDADIR', 'D:\APP\IDA\', 'User')

# 2. Install idalib-mcp
pip install git+https://github.com/mrexodia/ida-pro-mcp.git

# 3. Install IDA plugin
ida-pro-mcp --install
# Choose: Streamable HTTP -> Global -> select all clients

# 4. Start MCP service
powershell -File "<REVERSE_SKILL_ROOT>\ida-reverse\scripts\start.ps1"

# 5. Open sample
powershell -File "<REVERSE_SKILL_ROOT>\ida-reverse\scripts\open.ps1" -Path "C:\path\to\sample.exe"
```

### APK Security Analysis Workflow

```powershell
# 1. Decode APK
powershell -File "<REVERSE_SKILL_ROOT>\apk-reverse\scripts\decode.ps1" -ApkPath ".\app.apk"

# 2. Summarize manifest
powershell -File "<REVERSE_SKILL_ROOT>\apk-reverse\scripts\manifest-summary.ps1" -DecodedDir ".\app_decoded"

# 3. Decompile with jadx
jadx -d jadx_output .\app.apk

# 4. Frida hooking (example: bypass SSL pinning)
powershell -File "<REVERSE_SKILL_ROOT>\apk-reverse\scripts\frida-run.ps1" -PackageName "com.example.app" -Script "frida_scripts/ssl-bypass.js"

# 5. Rebuild and resign
powershell -File "<REVERSE_SKILL_ROOT>\apk-reverse\scripts\rebuild-sign-install.ps1" -DecodedDir ".\app_decoded"
```

---

## D. Security Review Report Template

```markdown
# Security Review Report

**Project**: [Name]
**Date**: [YYYY-MM-DD]
**Reviewer**: [Agent / Human]
**Scope**: [What was reviewed]

## Executive Summary
[Brief overview of findings and overall risk level]

## Findings

### [CRITICAL] [Title]
**Severity**: CRITICAL
**File**: [path]
**Description**: [What the vulnerability is]
**Impact**: [What an attacker can do]
**Evidence**:
```[language]
// Vulnerable code
```
**Remediation**:
```[language]
// Fixed code
```
**References**: [CWE, CVE, OWASP reference if applicable]

### [HIGH] [Title]
...

## Metrics
- Total Findings: N
- CRITICAL: N
- HIGH: N
- MEDIUM: N
- LOW: N
- INFO: N

## Tools Used
- [Static analysis tool]
- [Dependency scanner]
- [Manual code review]
- [reverse-skill modules used]
```

---

## E. OWASP ASVS Quick Checklist (Level 2)

| Requirement | Description |
|------------|-------------|
| V1.1 | Security requirements defined |
| V2.1 | Authentication enforced on all endpoints |
| V2.2 | Credentials stored with proper hashing |
| V2.3 | Session management is secure |
| V3.1 | Access control enforced server-side |
| V3.2 | Resource-level authorization enforced |
| V4.1 | All input validated |
| V5.1 | Output encoded per context |
| V6.1 | Cryptographic functions used correctly |
| V7.1 | Error handling does not leak information |
| V8.1 | Data protection requirements met |
| V9.1 | Communication security (TLS) |
| V10.1 | Malicious code prevention |
| V11.1 | Business logic vulnerabilities addressed |
| V12.1 | File handling is secure |
| V13.1 | API security requirements met |
