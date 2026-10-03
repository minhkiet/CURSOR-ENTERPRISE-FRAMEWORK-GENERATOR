---
description: Review skill cho Vietnamese online payment integrations (MoMo, SePay, PayOS, ZaloPay, VNPay, VietQR). Đánh giá API integration, webhook handling, security, compliance, và best practices cho thanh toán nội địa Việt Nam.
purpose: Cung cấp comprehensive review framework cho các payment provider phổ biến tại Việt Nam. Evaluate API integration patterns, webhook security, signature validation, payment flow, error handling, và reconciliation logic.
input:
  - Payment integration code (MoMo, SePay, PayOS, ZaloPay, VNPay, VietQR)
  - Webhook handler implementation
  - API configuration and credentials
  - Payment flow frontend/backend code
output:
  - Integration review report
  - Security assessment
  - Compliance checklist
  - Recommendations
version: 1.0.0
tags:
  - payment
  - vietnam
  - momo
  - sepay
  - payos
  - zalo-pay
  - vnpay
  - vietqr
  - online-payment
  - webhook
---

# Vietnam Payment Review

## PRE-REVIEW GATE (trước khi review payment integration)

### Scope Analysis
- [ ] Identify payment provider(s): MoMo, SePay, PayOS, ZaloPay, VNPay, VietQR
- [ ] List all files: webhook handlers, API clients, payment flow components
- [ ] Confirm environment (testnet/production) and credentials setup
- [ ] Identify all integration points (frontend callback, backend webhook, API calls)

### Pre-Integration Checklist
- [ ] Credentials stored securely (env vars, vault - NOT in code)
- [ ] Webhook endpoint is HTTPS and publicly accessible
- [ ] Idempotency strategy defined (unique requestId per payment)
- [ ] Error handling and retry logic planned
- [ ] Payment flow UX states mapped (pending, processing, success, failed)

>>> PRE-REVIEW PASSED: Proceed with payment integration review
---

## Tổng quan

Vietnam Payment Review là skill chuyên biệt để review các payment integrations phổ biến tại Việt Nam. Bao gồm MoMo, SePay, PayOS, ZaloPay, VNPay, và VietQR. Critical cho các ứng dụng cần hỗ trợ thanh toán nội địa Việt Nam.

## Provider Overview

| Provider | Loại | API Style | Sandbox | Kênh | Đặc điểm |
|----------|------|-----------|---------|------|-----------|
| MoMo | E-Wallet, QR | REST JSON | Có | QR Code, App Deep Link | IPN webhook, HMAC-SHA256 |
| SePay | Banking | REST JSON | Có | Banking Transfer (webhook) | VietQR-based, webhook push, atomic UPDATE idempotency |
| PayOS | Payment Gateway | REST JSON | Có | QR Code, ATM/Card | Checksum, webhook |
| ZaloPay | E-Wallet, Gateway | REST JSON | Có | QR, App, Card | MAC validation |
| VNPay | Payment Gateway | REST POST Form | Có | QR, ATM, Card, E-Wallet | SHA256 hash, IPN |
| VietQR | QR Payment | REST JSON | Có | QR Code (NAPAS) | VietQR/NAPAS standard |

## Review Checklist

### Common (All Providers)

- [ ] All monetary amounts handled as integers (cents/VND), never floats
- [ ] Signature verification on all webhook callbacks
- [ ] Idempotency: webhook processing is idempotent (prevent duplicate)
- [ ] HTTPS only for all payment endpoints
- [ ] Credentials stored in environment variables, never hardcoded
- [ ] Webhook signature secret stored securely
- [ ] Timeout handling on payment gateway calls
- [ ] Retry logic with exponential backoff for API calls
- [ ] Payment status tracked in database with audit trail
- [ ] Graceful handling of gateway downtime

### MoMo

- [ ] PartnerCode, accessKey, secretKey stored in env
- [ ] Request signing uses HMAC-SHA256 with secretKey
- [ ] IPN (Instant Payment Notification) webhook signature validated
- [ ] `resultCode` checked before fulfilling order
- [ ] `orderId` uniqueness enforced server-side
- [ ] `orderInfo`, `amount`, `returnUrl`, `notifyUrl` all sent correctly
- [ ] Signature order matches MoMo's required field sequence
- [ ] Sanbox testing with MoMo test accounts
- [ ] Production endpoint: `https://payment.momo.vn`
- [ ] Sandbox endpoint: `https://test-payment.momo.vn`

### SePay

#### Core Configuration
- [ ] API key stored in env (`SEPAY_API_KEY`), never in code
- [ ] Webhook endpoint registered at my.sepay.vn
- [ ] Payment code structure configured at **Công ty → Cấu hình chung → Cấu trúc mã thanh toán**

#### QR Code Generation
- [ ] QR URL follows format: `https://vietqr.app/img?acc=...&bank=...&amount=...&des=...`
- [ ] `acc` = Số tài khoản thụ hưởng ( beneficiary account number)
- [ ] `bank` = Mã ngân hàng (bank code, e.g., `Vietcombank`)
- [ ] `amount` = Số tiền VND (integer, no decimals)
- [ ] `des` = Nội dung chuyển khoản (payment code/descriptor)
- [ ] All params URL-encoded properly

#### Webhook Security
- [ ] API Key authentication via `Authorization: Apikey <SEPAY_API_KEY>` header
- [ ] Use `hash_equals()` (constant-time comparison) to prevent timing attacks
- [ ] HMAC-SHA256 signature recommended for production (see [SePay Auth](https://developer.sepay.vn/vi/sepay-webhooks/xac-thuc#hmac-sha256))

#### Idempotent Webhook Processing
- [ ] `transaction_id` stored as UNIQUE key in `webhook_logs` table
- [ ] Use `INSERT IGNORE` or `ON DUPLICATE KEY` to prevent duplicate processing
- [ ] `UNIQUE(transaction_id)` at DB layer + `INSERT IGNORE` in handler = race-safe

#### Payment Code Security
- [ ] Payment codes use cryptographically random values: `bin2hex(random_bytes(6))` or `crypto.randomBytes(6).toString('hex')`
- [ ] **NEVER** use auto-increment IDs or plain timestamps as payment codes
- [ ] Unpredictable codes prevent fake webhook injection or order claiming

#### Amount Verification (Atomic UPDATE)
- [ ] Use single atomic UPDATE with amount check in WHERE clause:
```sql
UPDATE orders 
SET status = 'paid', paid_at = NOW() 
WHERE code = ? AND status = 'pending' AND amount <= ?
```
- [ ] This prevents race conditions without explicit transactions
- [ ] First webhook changes `pending → paid`; subsequent retries hit `status = 'pending'` = false, so nothing happens

#### Backend Endpoints Pattern
- [ ] `POST /api/orders` - Tạo đơn, trả mã + QR URL
- [ ] `GET /api/orders/:code/status` - Frontend poll trạng thái (3s interval)
- [ ] `POST /webhook/sepay` - Nhận webhook từ SePay

#### Database Schema
```sql
CREATE TABLE orders (
  id          BIGINT AUTO_INCREMENT PRIMARY KEY,
  code        VARCHAR(64)  NOT NULL UNIQUE,           -- payment descriptor
  amount      BIGINT       NOT NULL,                   -- VND integer, no decimals
  status      ENUM('pending','paid','expired') DEFAULT 'pending',
  paid_at     DATETIME     NULL,
  created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_status_created (status, created_at)
);

CREATE TABLE webhook_logs (
  id             BIGINT AUTO_INCREMENT PRIMARY KEY,
  transaction_id VARCHAR(128) NOT NULL UNIQUE,         -- SePay transaction ID
  body           JSON         NOT NULL,                -- full webhook payload
  processed_at   DATETIME     DEFAULT CURRENT_TIMESTAMP
);
```
- `amount BIGINT`: VND has no decimals. `INT` max 2.1B, B2B invoices easily overflow.
- `code UNIQUE`: prevents duplicate payment codes at DB level.
- `transaction_id UNIQUE`: idempotency lock for webhooks.
- `body JSON`: query with `JSON_EXTRACT` for debugging.
- `idx_status_created`: find pending orders older than X minutes for expiry jobs.

#### Frontend Payment Page
- [ ] Display QR code via `https://vietqr.app/img?...` URL
- [ ] Poll `/api/orders/:code/status` every 3 seconds
- [ ] 15-minute countdown before marking as expired
- [ ] Status states: `waiting`, `paid`, `expired`
- [ ] Consider SSE/WebSocket for multi-order backends (server push vs client poll)

#### Webhook Response
- [ ] Return `{"success": true}` immediately (before heavy processing)
- [ ] Push heavy work (email, inventory, third-party APIs) to queue (Redis, SQS)
- [ ] Webhook timeout: 30 seconds

#### Transfer Matching
- [ ] Webhook payload fields: `id` (transaction_id), `code` (payment descriptor), `transferAmount`, `transferType` ('in')
- [ ] Check `transferType === 'in'` before processing
- [ ] Match by `code` field in webhook payload

#### Production Checklist
- [ ] HMAC-SHA256 enabled (API Key only = insufficient against payload tampering)
- [ ] Payment codes are cryptographically random
- [ ] Amount validation in SQL WHERE clause (not in application code)
- [ ] Return 200 before heavy processing
- [ ] Webhook HTTPS-only
- [ ] Reconciliation endpoint tested (see [Đối soát giao dịch](https://developer.sepay.vn/vi/sepay-webhooks/doi-soat-giao-dich))

#### Example Webhook Handler (PHP)
```php
// POST /webhook/sepay
$auth = $_SERVER['HTTP_AUTHORIZATION'] ?? '';
if (!hash_equals('Apikey ' . getenv('SEPAY_API_KEY'), $auth)) {
    http_response_code(401);
    exit;
}

$body = json_decode(file_get_contents('php://input'), true);

// Idempotency: skip if already processed
$log = $pdo->prepare('INSERT IGNORE INTO webhook_logs (transaction_id, body) VALUES (?, ?)');
$log->execute([$body['id'], $body]);
if ($log->rowCount() === 0) {
    echo json_encode(['success' => true]); // already handled
    exit;
}

// Atomic UPDATE with amount check
if ($body['transferType'] === 'in' && !empty($body['code'])) {
    $pdo->prepare(
        'UPDATE orders SET status = "paid", paid_at = NOW()
         WHERE code = ? AND status = "pending" AND amount <= ?'
    )->execute([$body['code'], $body['transferAmount']]);
    // TODO: enqueue email / inventory update
}

echo json_encode(['success' => true]);
```

### PayOS

- [ ] Client ID and API Key stored in env
- [ ] Checksum calculated with HMAC-SHA256
- [ ] Webhook signature verified using `signature` field
- [ ] Order ID uniqueness enforced
- [ ] `amount` and `description` sent correctly
- [ ] Cancel URL and return URL configured
- [ ] `transactionStatus` checked before fulfilling
- [ ] Sandbox: `https://api-sandbox.payos.vn`
- [ ] Production: `https://api.payos.vn`

### ZaloPay

- [ ] AppID and Key stored in env
- [ ] MAC (Message Authentication Code) validated on callbacks
- [ ] `transId` checked for duplicate processing
- [ ] `amount` and `appTransId` correctly sent
- [ ] `callbackUrl` configured properly
- [ ] `embedData` for embedded payment flows
- [ ] Sandbox testing: `https://sb-openapi.zalopay.vn`
- [ ] Production: `https://openapi.zalopay.vn`

### VNPay

- [ ] Merchant code and security key in env
- [ ] Secure hash (SHA256) computed correctly with all fields
- [ ] Field order exactly as VNPay requires (alphabetical)
- [ ] Return URL and IPN URL configured
- [ ] `vnp_TransactionStatus` = `00` checked for success
- [ ] `vnp_TxnRef` (order ID) uniqueness validated
- [ ] `vnp_Amount` divided by 100 (VNPay uses smallest unit)
- [ ] `vnp_SecureHash` validated before processing
- [ ] Sandbox: `https://sandbox.vnpayment.vn`
- [ ] Production: `https://pay.vnpayment.vn`

### VietQR

- [ ] API credentials stored securely
- [ ] QR generation follows VietQR/NAPAS standard
- [ ] Bank account number and BIN correctly encoded
- [ ] Amount validation on payment matching
- [ ] Transfer reference parsed correctly from bank callback
- [ ] Multiple bank support: Vietcombank, VietinBank, BIDV, etc.
- [ ] Sandbox testing with test bank accounts
- [ ] Real-time status polling vs webhook for different banks

## Common Anti-Patterns

### Storing Money as Float

```typescript
// ❌ BAD: Floating point for VND
const total = price * 1.1; // Floating point precision errors!

// ✅ GOOD: Integer VND (no decimals in VND)
const totalVND = priceVND + Math.round(priceVND * 0.1);
```

### Skipping Webhook Signature Verification

```typescript
// ❌ BAD: No signature verification
async handleWebhook(req: Request) {
  const { orderId, status } = req.body;
  await fulfillOrder(orderId, status); // UNSAFE!
}

// ✅ GOOD: Verify signature first
async handleWebhook(req: Request) {
  const signature = req.headers['x-momo-signature'];
  if (!verifySignature(req.body, signature)) {
    return res.status(401).send('Invalid signature');
  }
  const { orderId, resultCode } = req.body;
  if (resultCode !== 0) return; // Only process successful payments
  await fulfillOrder(orderId);
}
```

### No Idempotency on Webhooks

```typescript
// ❌ BAD: Processing without idempotency check
async handleWebhook(req: Request) {
  const { orderId, status } = req.body;
  await updateOrderStatus(orderId, status); // May run multiple times!
}

// ✅ GOOD: Idempotent webhook processing
async handleWebhook(req: Request) {
  const { orderId, status } = req.body;
  const existing = await db.orders.findUnique({ where: { orderId } });
  if (existing.status === status) return; // Already processed
  await db.orderStatusLog.create({
    data: { orderId, status, processedAt: new Date() }
  });
  await updateOrderStatus(orderId, status);
}
```

### SePay: Predictable Payment Codes

```php
// ❌ BAD: Auto-increment or timestamp as payment code
$code = 'DH' . $orderId;  // Predictable! Attackers can guess
$code = 'DH' . time();      // Predictable! Can scan future codes

// ✅ GOOD: Cryptographically random payment code
$code = 'DH' . bin2hex(random_bytes(6));  // 12 hex chars, unpredictable
```

```typescript
// ❌ BAD: Predictable code in Node.js
const code = `DH${Date.now()}`;  // Can be predicted!

// ✅ GOOD: Random payment code
import crypto from 'crypto';
const code = 'DH' + crypto.randomBytes(6).toString('hex');
```

### SePay: SELECT-then-UPDATE Race Condition

```php
// ❌ BAD: SELECT then UPDATE — race condition with duplicate webhooks
$order = $pdo->query("SELECT * FROM orders WHERE code = '$code'")->fetch();
if ($order['status'] === 'paid') exit;  // Gap: another webhook could also pass this check
$pdo->exec("UPDATE orders SET status = 'paid' WHERE code = '$code'");
```

```php
// ✅ GOOD: Single atomic UPDATE with amount check in WHERE
$pdo->prepare(
    'UPDATE orders SET status = "paid", paid_at = NOW()
     WHERE code = ? AND status = "pending" AND amount <= ?'
)->execute([$code, $transferAmount]);
// Second webhook: status != 'pending' → no rows affected → safe idempotency
```

```typescript
// ❌ BAD: Credentials in code
const momoConfig = {
  partnerCode: 'MOMO_PARTNER_CODE',
  accessKey: 'momo_access_key_123',
  secretKey: 'momo_secret_key_xyz'
};

// ✅ GOOD: Environment variables
const momoConfig = {
  partnerCode: process.env.MOMO_PARTNER_CODE,
  accessKey: process.env.MOMO_ACCESS_KEY,
  secretKey: process.env.MOMO_SECRET_KEY
};
```

### Trusting Client-Side Payment Amount

```typescript
// ❌ BAD: Amount from client
const payment = { amount: req.body.amount }; // User can manipulate!

// ✅ GOOD: Amount from server-side order record
const order = await db.orders.findUnique({ where: { orderId } });
await momo.createPayment({ amount: order.amount }); // Verified server amount
```

## Security Checklist

- [ ] HMAC-SHA256 signature verification on all webhooks
- [ ] No sensitive data logged (card numbers, secrets)
- [ ] TLS 1.2+ enforced on all payment connections
- [ ] Rate limiting on payment endpoints
- [ ] Webhook IP whitelist if provider supports it
- [ ] Secrets rotated periodically
- [ ] Payment audit log maintained (who, what, when, how much)
- [ ] CSRF protection on payment-related forms
- [ ] Input validation on all payment callback fields

## Multi-Provider Pattern

For applications supporting multiple providers, use the adapter pattern:

```typescript
interface PaymentProvider {
  createPayment(order: Order): Promise<PaymentLink>;
  verifyWebhook(payload: unknown, headers: Record<string, string>): boolean;
  parseWebhook(payload: unknown): WebhookEvent;
  getStatusFromEvent(event: WebhookEvent): PaymentStatus;
}

class PaymentService {
  constructor(private providers: Map<string, PaymentProvider>) {}

  async processWebhook(provider: string, payload: unknown, headers: Record<string, string>) {
    const handler = this.providers.get(provider);
    if (!handler) throw new Error(`Unknown provider: ${provider}`);

    if (!handler.verifyWebhook(payload, headers)) {
      throw new Error('Invalid webhook signature');
    }

    const event = handler.parseWebhook(payload);
    if (handler.getStatusFromEvent(event) === 'SUCCESS') {
      await this.fulfillOrder(event.orderId);
    }
  }
}
```

## Additional Resources

- For detailed API integration code patterns, see [reference.md](reference.md)
- For provider-specific nuances and gotchas, see [reference.md](reference.md)


---

## POST-REVIEW GATE (run after code written)

### API Integration Review
- [ ] All API calls use correct endpoints (testnet vs production)
- [ ] Request parameters validated and signed correctly
- [ ] Response parsing handles all cases (success, pending, failed, error)
- [ ] Timeout and retry logic implemented (idempotent endpoints)
- [ ] Credentials never hardcoded or logged

### Webhook Security Review
- [ ] Webhook signature/checksum validation implemented
- [ ] Timestamp validation (prevent replay attacks)
- [ ] Idempotency: duplicate webhook calls handled safely
- [ ] Webhook URL is HTTPS only
- [ ] Error responses do not expose internal details

### Payment Flow Review
- [ ] All payment states handled: pending, processing, success, failed, cancelled, refunded
- [ ] User redirected/updated correctly on each state transition
- [ ] Payment timeout handled (15-minute default expiry)
- [ ] Refund flow implemented with original payment method
- [ ] Reconciliation logic implemented (daily balance check)

### Vietnam-Specific Review
- [ ] MoMo: partnerCode, accessKey, secretKey not in code; QR format correct
- [ ] **SePay**: cryptographically random payment codes; atomic UPDATE with `amount <= ?` in WHERE; `INSERT IGNORE` for idempotent webhooks; HMAC-SHA256 enabled in production
- [ ] PayOS: checksum validation with checksumKey implemented
- [ ] ZaloPay: appTransId uniqueness guaranteed
- [ ] VNPay: return URL and IPN URL configured correctly
- [ ] VietQR: bank account validation, VietQR format compliance

### Compliance Review
- [ ] PCI-DSS: No card data stored locally
- [ ] Refund policy implemented within allowed window
- [ ] Invoice generation triggered on successful payment
- [ ] Audit log records all payment events

>>> POST-REVIEW PASSED: Payment integration ready for production

## Liens

- [[../rules/skill-integration]] - Skill Integration Rules
- [[../rules/billing]] - Billing Rules
- [[../rules/security]] - Security Rules
- [[../rules/web-security]] - Web Security Rules
- [[../knowledge/security]] - Security Knowledge
- [[../knowledge/billing]] - Billing Knowledge
