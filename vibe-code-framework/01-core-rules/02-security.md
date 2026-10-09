# Bảo mật cơ bản

> **Version:** 1.0.0 | **Category:** Core Security | **OWASP:** Top 10 2021

---

## Tổng quan

Nguyên tắc bảo mật cơ bản áp dụng cho mọi project. Đây là tập con của OWASP Top 10 và các best practices thiết yếu.

---

## 1. Không Hardcode Secrets

**Nguyên tắc:** Không bao giờ commit secrets vào source code.

### Checklist

```
□ Không có API keys trong code
□ Không có passwords trong code
□ Không có database credentials trong code
□ Không có private keys trong code
□ Sử dụng environment variables
□ .env file trong .gitignore
```

### Ví dụ

**Sai:**
```typescript
// ❌ Hardcoded secrets
const apiKey = 'sk-1234567890abcdef';
const dbPassword = 'admin123';

fetch('https://api.example.com', {
  headers: { 'Authorization': `Bearer ${apiKey}` }
});
```

**Đúng:**
```typescript
// ✅ Environment variables
const apiKey = process.env.API_KEY;
const dbPassword = process.env.DB_PASSWORD;

// Sử dụng config module
import config from './config';
const apiKey = config.api.key;
```

### File cấu hình

```bash
# .env.example — Template (safe to commit)
API_KEY=
DB_PASSWORD=
JWT_SECRET=
STRIPE_SECRET=

# .env — Actual secrets (NEVER commit)
API_KEY=sk-xxxxx
DB_PASSWORD=actual-password
```

```gitignore
# .gitignore
.env
.env.local
.env.*.local
*.pem
*.key
credentials.json
```

---

## 2. Input Validation

**Nguyên tắc:** Validate tất cả input từ user/external, không tin bất kỳ ai.

### Checklist

```
□ Validate input length
□ Validate input format (email, phone, URL)
□ Validate numeric ranges
□ Validate enum values
□ Sanitize HTML/SQL input
□ Use typed validation (Zod, Yup, Joi)
```

### Ví dụ

**Sai:**
```typescript
// ❌ Trusting user input
app.get('/users/:id', async (req, res) => {
  const user = await db.query(
    `SELECT * FROM users WHERE id = ${req.params.id}`
  );
  res.json(user);
});
```

**Đúng:**
```typescript
// ✅ Validate & sanitize
import { z } from 'zod';

const paramsSchema = z.object({
  id: z.string().uuid()
});

app.get('/users/:id', async (req, res) => {
  const { id } = paramsSchema.parse(req.params);
  const user = await db.query(
    'SELECT * FROM users WHERE id = $1',
    [id]  // Parameterized query
  );
  res.json(user);
});
```

---

## 3. SQL Injection Prevention

**Nguyên tắc:** Luôn sử dụng parameterized queries, NEVER concatenate user input vào SQL.

### Checklist

```
□ Sử dụng parameterized queries
□ Sử dụng ORM với built-in protection
□ Không dùng string concatenation cho SQL
□ Validate input format trước khi query
```

### Ví dụ

**Sai:**
```typescript
// ❌ SQL Injection vulnerable
const query = `SELECT * FROM users WHERE name = '${req.body.name}'`;
db.query(query);
```

**Đúng:**
```typescript
// ✅ Parameterized query
const query = 'SELECT * FROM users WHERE name = $1';
db.query(query, [req.body.name]);
```

---

## 4. XSS Prevention

**Nguyên tắc:** Escape output khi render user content, never trust raw HTML.

### Checklist

```
□ Escape HTML entities khi render user input
□ Use Content Security Policy (CSP)
□ HTTPOnly cookies
□ Validate & sanitize file uploads
□ Use templating engines với auto-escaping
```

### Ví dụ

**Sai:**
```typescript
// ❌ XSS vulnerable
res.send(`<h1>${user.name}</h1>`);
```

**Đúng:**
```typescript
// ✅ Safe rendering
import escapeHtml from 'escape-html';

res.send(`<h1>${escapeHtml(user.name)}</h1>`);

// Hoặc dùng templating engine
res.render('user-profile', { userName: escapeHtml(user.name) });
```

---

## 5. Authentication & Authorization

**Nguyên tắc:** Xác thực user, phân quyền rõ ràng.

### Checklist

```
□ Hash passwords (bcrypt, argon2)
□ Use JWT với short expiration
□ Implement refresh token rotation
□ Check permissions trước mỗi action
□ Log authentication attempts
□ Rate limit login endpoints
```

### Ví dụ

**Sai:**
```typescript
// ❌ Weak password handling
if (user.password === inputPassword) {
  // So sánh plain text!
  return generateToken(user);
}
```

**Đúng:**
```typescript
// ✅ Secure authentication
import bcrypt from 'bcrypt';

async function authenticate(email: string, password: string) {
  const user = await db.findUserByEmail(email);
  
  if (!user) return null;
  
  const isValid = await bcrypt.compare(password, user.passwordHash);
  if (!isValid) return null;
  
  return generateToken(user);
}
```

---

## 6. Rate Limiting

**Nguyên tắc:** Giới hạn số request để prevent abuse.

### Checklist

```
□ Rate limit API endpoints
□ Rate limit authentication endpoints
□ Use exponential backoff cho retries
□ Implement account lockout sau failed attempts
```

### Ví dụ

```typescript
import rateLimit from 'express-rate-limit';

// General API limit
app.use('/api/', rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100  // 100 requests per window
}));

// Strict limit cho auth endpoints
app.use('/api/auth/', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,  // 5 attempts per window
  message: 'Too many attempts, please try again later'
}));
```

---

## 7. Secure Headers

**Nguyên tắc:** Set secure HTTP headers để protect against common attacks.

### Required Headers

```
□ Content-Security-Policy (CSP)
□ X-Content-Type-Options: nosniff
□ X-Frame-Options: DENY
□ Strict-Transport-Security (HSTS)
□ X-XSS-Protection: 1; mode=block
□ Referrer-Policy: strict-origin-when-cross-origin
```

### Ví dụ

```typescript
// helmet.js - automatic secure headers
import helmet from 'helmet';

app.use(helmet());

// Custom CSP
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'nonce-{generated}'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", "data:", "https:"],
    connectSrc: ["'self'", "https://api.example.com"],
  }
}));
```

---

## 8. Error Handling

**Nguyên tắc:** Không leak sensitive information trong error messages.

### Checklist

```
□ Không expose stack traces
□ Log errors chi tiết server-side
□ Return generic messages cho user
□ Handle 404, 403, 500 properly
```

### Ví dụ

**Sai:**
```typescript
// ❌ Leaking information
app.get('/user/:id', (req, res) => {
  try {
    const user = db.findById(req.params.id);
    res.json(user);
  } catch (e) {
    res.status(500).json({
      error: e.message,
      stack: e.stack,
      query: db.lastQuery
    });
  }
});
```

**Đúng:**
```typescript
// ✅ Safe error handling
import { logger } from './logger';

app.get('/user/:id', (req, res) => {
  try {
    const user = db.findById(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  } catch (e) {
    logger.error('Error fetching user', { id: req.params.id, error: e });
    res.status(500).json({
      error: 'Internal server error'
    });
  }
});
```

---

## Security Checklist Summary

```
┌─────────────────────────────────────────────────────────────┐
│ Pre-Commit Security Checklist                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  □ No hardcoded secrets                                    │
│  □ All user input validated                                │
│  □ Parameterized SQL queries                                │
│  □ Output escaped/sanitized                                │
│  □ Passwords hashed (bcrypt/argon2)                        │
│  □ Rate limiting enabled                                   │
│  □ Secure headers configured                                │
│  □ Error messages sanitized                                │
│  □ Authentication required for protected routes             │
│  □ Authorization checked per action                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Nguồn tham khảo

- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [Mozilla Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
