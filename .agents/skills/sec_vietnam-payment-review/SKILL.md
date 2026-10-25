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

| Provider | Loại | API Style | Sandbox | Kênh |
|----------|------|-----------|---------|------|
| MoMo | E-Wallet, QR | REST JSON | Có | QR Code, App Deep Link |
| SePay | Banking | REST JSON | Có | Banking Transfer (webhook) |
| PayOS | Payment Gateway | REST JSON | Có | QR Code, ATM/Card |
| ZaloPay | E-Wallet, Gateway | REST JSON | Có | QR, App, Card |
| VNPay | Payment Gateway | REST POST Form | Có | QR, ATM, Card, E-Wallet |
| VietQR | QR Payment | REST JSON | Có | QR Code (NAPAS) |

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

- [ ] API key stored in env, not in code
- [ ] Webhook secret validated on incoming transfers
- [ ] Duplicate transfer detection (same `transferId` processed once)
- [ ] Amount matching: verify transferred amount >= expected amount
- [ ] Account number validation before processing
- [ ] Bank code mapping handled correctly
- [ ] Sandbox testing with SePay test bank accounts
- [ ] Transfer descriptor/description parsing for auto-matching
- [ ] Handle both `transfer_in` and `transfer_out` events
- [ ] Sandbox endpoint: `https://api.sepay.vn`

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

### Hardcoded Credentials

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
- [ ] SePay: auto-reconciliation by amount+content implemented
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
