# Vietnam Payment Reference

Detailed integration patterns for MoMo, SePay, PayOS, ZaloPay, VNPay, and VietQR.

## MoMo

### Environment Setup

```
MOMO_PARTNER_CODE=    # Your partner code
MOMO_ACCESS_KEY=      # Access key
MOMO_SECRET_KEY=      # Secret key for signing
MOMO_ENDPOINT=        # https://test-payment.momo.vn or https://payment.momo.vn
```

### Payment Creation (Express API)

```typescript
import crypto from 'crypto';

interface MoMoPaymentRequest {
  orderId: string;
  amount: number;       // Amount in VND (integer)
  orderInfo: string;
  returnUrl: string;
  notifyUrl: string;
}

function createMoMoSignature(fields: Record<string, string | number>, secretKey: string): string {
  const rawData = Object.entries(fields)
    .map(([k, v]) => `${k}=${v}`)
    .join('&');
  return crypto.createHmac('sha256', secretKey).update(rawData).digest('hex');
}

async function createMoMoPayment(req: MoMoPaymentRequest) {
  const endpoint = process.env.MOMO_ENDPOINT || 'https://test-payment.momo.vn';
  const partnerCode = process.env.MOMO_PARTNER_CODE!;
  const accessKey = process.env.MOMO_ACCESS_KEY!;
  const secretKey = process.env.MOMO_SECRET_KEY!;

  const requestId = `${Date.now()}-${req.orderId}`;
  const requestType = 'payWithMethod';

  const rawData = [
    `accessKey=${accessKey}`,
    `amount=${req.amount}`,
    `extraData=`,
    `ipnUrl=${req.notifyUrl}`,
    `orderId=${req.orderId}`,
    `orderInfo=${req.orderInfo}`,
    `partnerCode=${partnerCode}`,
    `redirectUrl=${req.returnUrl}`,
    `requestId=${requestId}`,
    `requestType=${requestType}`,
  ].join('&');

  const signature = crypto.createHmac('sha256', secretKey).update(rawData).digest('hex');

  const response = await fetch(`${endpoint}/v2/gateway/api/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      partnerCode,
      partnerName: 'Test',
      storeId: partnerCode,
      requestId,
      amount: req.amount,
      currency: 'VND',
      orderId: req.orderId,
      orderInfo: req.orderInfo,
      redirectUrl: req.returnUrl,
      ipnUrl: req.notifyUrl,
      requestType,
      extraData: '',
      signature,
      lang: 'vi',
    }),
  });

  return response.json();
}
```

### MoMo Webhook Verification

```typescript
async function verifyMoMoWebhook(body: Record<string, string>, signature: string): Promise<boolean> {
  const secretKey = process.env.MOMO_SECRET_KEY!;

  const { signature: _, ...data } = body;
  const rawData = Object.entries(data)
    .map(([k, v]) => `${k}=${v}`)
    .join('&');

  const expectedSignature = crypto.createHmac('sha256', secretKey).update(rawData).digest('hex');
  return signature === expectedSignature;
}

async function handleMoMoWebhook(req: Request) {
  const signature = req.headers['x-momo-signature'] || req.headers['signature'];
  const isValid = await verifyMoMoWebhook(req.body, signature as string);

  if (!isValid) {
    return new Response('Invalid signature', { status: 401 });
  }

  const { orderId, resultCode, amount, transId } = req.body;

  if (resultCode !== 0) {
    return new Response('Payment failed', { status: 200 });
  }

  await processPayment(orderId, amount, transId);
  return new Response('OK', { status: 200 });
}
```

### MoMo Signature Field Order (Critical)

MoMo requires fields in a specific order for signing. Always include ALL fields present in the request. Never change field order.

**Request signing order**: `accessKey|amount|extraData|ipnUrl|orderId|orderInfo|partnerCode|redirectUrl|requestId|requestType`

**Webhook signing order**: Same as request — all fields except `signature` itself.

---

## SePay

### Environment Setup

```
SEPAY_API_KEY=         # Your SePay API key
SEPAY_WEBHOOK_SECRET=  # Webhook callback secret
SEPAY_ENDPOINT=        # https://api.sepay.vn
```

### Bank List (SePay Supported)

SePay supports multiple Vietnamese banks. Common ones:
- Vietcombank (VCB)
- VietinBank (CTG)
- BIDV
- Agribank (AGR)
- TPBank (TPB)
- MB Bank (MB)
- ACB
- Sacombank

### Payment Account Registration

```typescript
async function registerSepayAccount(accountNumber: string, bankCode: string) {
  const response = await fetch('https://api.sepay.vn/account/register', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.SEPAY_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      account_number: accountNumber,
      bank_code: bankCode,
      callback_url: process.env.SEPAY_WEBHOOK_URL,
    }),
  });
  return response.json();
}
```

### SePay Webhook Handler

```typescript
interface SePayTransferEvent {
  id: string;
  transfer_id: string;
  transaction_date: string;
  amount: number;
  currency: string;
  description: string;
  account_number: string;
  reference: string;
  bank_code: string;
  fee: number;
  is_sender: boolean;
}

async function handleSepayWebhook(req: Request) {
  const secret = process.env.SEPAY_WEBHOOK_SECRET!;
  const signature = req.headers['x-sepay-signature'] || req.headers['signature'];

  // Verify signature
  const expectedSig = crypto
    .createHmac('sha256', secret)
    .update(JSON.stringify(req.body))
    .digest('hex');

  if (signature !== expectedSig) {
    return new Response('Invalid signature', { status: 401 });
  }

  const event: SePayTransferEvent = req.body;

  // Idempotency: check if already processed
  const existing = await db.sepayTransactions.findUnique({
    where: { transferId: event.transfer_id },
  });

  if (existing) {
    return new Response('Already processed', { status: 200 });
  }

  // Parse description for order matching
  // Format: "TT12345" or "ORDER-12345-MOMO"
  const orderIdMatch = event.description.match(/(?:TT|ORDER)[-_]?(\w+)/);
  const orderId = orderIdMatch ? orderIdMatch[1] : null;

  if (orderId) {
    const order = await db.orders.findUnique({ where: { id: orderId } });
    if (order && event.amount >= order.totalAmountVND) {
      await db.$transaction([
        db.orders.update({ where: { id: orderId }, data: { status: 'PAID' } }),
        db.sepayTransactions.create({
          data: {
            transferId: event.transfer_id,
            orderId,
            amount: event.amount,
            description: event.description,
            bankCode: event.bank_code,
            transactionDate: new Date(event.transaction_date),
          },
        }),
      ]);
    }
  }

  return new Response('OK', { status: 200 });
}
```

### SePay Auto-Match via Description

Format transfer descriptions consistently so SePay webhooks auto-match payments:

```typescript
// Generate consistent payment reference
function generatePaymentReference(orderId: string): string {
  return `TT${orderId}`; // e.g., TTORD-12345
}

// On checkout page, show user the transfer info:
const paymentInfo = {
  bank: 'Vietcombank',
  accountNumber: '1234567890',
  accountName: 'CONG TY ABC',
  amount: 150000,
  reference: generatePaymentReference(order.id),
};
```

---

## PayOS

### Environment Setup

```
PAYOS_CLIENT_ID=     # Your PayOS Client ID
PAYOS_API_KEY=       # PayOS API Key
PAYOS_CHECKSUM_KEY=  # PayOS Checksum Key
PAYOS_ENDPOINT=      # https://api-sandbox.payos.vn or https://api.payos.vn
```

### Payment Creation

```typescript
import crypto from 'crypto';

interface PayOSPaymentRequest {
  orderId: string;
  amount: number;
  description: string;
  returnUrl: string;
  cancelUrl: string;
}

function createPayOSSignature(data: Record<string, string | number>, checksumKey: string): string {
  const rawData = Object.entries(data)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([k, v]) => `${k}=${v}`)
    .join('&');
  return crypto.createHmac('sha256', checksumKey).update(rawData).digest('hex');
}

async function createPayOSPaymentLink(req: PayOSPaymentRequest) {
  const clientId = process.env.PAYOS_CLIENT_ID!;
  const apiKey = process.env.PAYOS_API_KEY!;
  const checksumKey = process.env.PAYOS_CHECKSUM_KEY!;

  const data = {
    orderCode: req.orderId,
    amount: req.amount,
    description: req.description,
    returnUrl: req.returnUrl,
    cancelUrl: req.cancelUrl,
  };

  const signature = createPayOSSignature(data, checksumKey);

  const response = await fetch(`${process.env.PAYOS_ENDPOINT}/v2/payment-requests`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Client-Id': clientId,
      'X-Api-Key': apiKey,
    },
    body: JSON.stringify({ ...data, signature }),
  });

  return response.json();
}
```

### PayOS Webhook Handler

```typescript
async function handlePayOSWebhook(req: Request) {
  const checksumKey = process.env.PAYOS_CHECKSUM_KEY!;
  const { code, desc, status, orderCode, amount, transactionId, signature } = req.body;

  // Verify signature
  const data = { code, desc, status, orderCode, amount, transactionId };
  const expectedSig = createPayOSSignature(data, checksumKey);

  if (signature !== expectedSig) {
    return new Response('Invalid signature', { status: 401 });
  }

  // Idempotency check
  const existing = await db.payOSCallbacks.findUnique({
    where: { transactionId },
  });

  if (existing) {
    return new Response('Already processed', { status: 200 });
  }

  // status: 'PAID', 'CANCELLED'
  if (status === 'PAID') {
    await db.$transaction([
      db.orders.update({ where: { id: orderCode }, data: { status: 'PAID' } }),
      db.payOSCallbacks.create({
        data: { transactionId, orderCode, amount, status },
      }),
    ]);
  }

  return new Response('OK', { status: 200 });
}
```

---

## ZaloPay

### Environment Setup

```
ZALOPAY_APPID=      # ZaloPay App ID
ZALOPAY_KEY1=        # Key1 for callback verification
ZALOPAY_KEY2=        # Key2 for create payment
ZALOPAY_ENDPOINT=   # https://sb-openapi.zalopay.vn or https://openapi.zalopay.vn
```

### Payment Creation

```typescript
async function createZaloPayOrder(orderId: string, amount: number, items: unknown[]) {
  const appId = Number(process.env.ZALOPAY_APPID!);
  const key2 = process.env.ZALOPAY_KEY2!;
  const endpoint = process.env.ZALOPAY_ENDPOINT || 'https://sb-openapi.zalopay.vn';

  const appTransId = `${new Date().toISOString().slice(0, 10).replace(/-/g, '')}_${orderId}`;
  const embedData = JSON.stringify({ redirecturl: process.env.ZALOPAY_RETURN_URL });
  const itemsJson = JSON.stringify(items);

  const appTime = Date.now().toString();
  const rawData = `${appId}|${appTransId}|${appUser}|${amount}|${appTime}|${embedData}|${itemsJson}`;
  const mac = crypto.createHmac('sha256', key2).update(rawData).digest('hex');

  const response = await fetch(`${endpoint}/v2/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      app_id: appId,
      app_user: 'user_123',
      app_trans_id: appTransId,
      app_time,
      amount,
      app_secret: key2,
      embed_data: embedData,
      item: itemsJson,
      callback_url: process.env.ZALOPAY_CALLBACK_URL,
      description: `Thanh toan don hang ${orderId}`,
      bank_code: '',
      mac,
    }),
  });

  return response.json();
}
```

### ZaloPay Callback Verification

```typescript
async function handleZaloPayCallback(req: Request) {
  const key1 = process.env.ZALOPAY_KEY1!;

  // Parse callback data
  let data: Record<string, string>;
  if (typeof req.body === 'string') {
    data = JSON.parse(req.body);
  } else {
    data = req.body;
  }

  const { appid, apptransid, zp_trans_id, amount, status, checksum } = data;

  // Verify checksum
  const callbackData = `${appid}|${apptransid}|${key1}`;
  const expectedMac = crypto.createHmac('sha256', key1).update(callbackData).digest('hex');

  if (checksum !== expectedMac) {
    return new Response('Invalid checksum', { status: 401 });
  }

  // Idempotency check
  if (status !== 1) return new Response('OK', { status: 200 }); // 1 = success

  const existing = await db.zaloTransactions.findUnique({
    where: { appTransId: apptransid },
  });

  if (!existing) {
    await db.$transaction([
      db.orders.update({ where: { id: apptransid.split('_')[1] }, data: { status: 'PAID' } }),
      db.zaloTransactions.create({ data: { appTransId: apptransid, zpTransId: zp_trans_id, amount } }),
    ]);
  }

  return new Response('[200]', { status: 200 });
}
```

---

## VNPay

### Environment Setup

```
VNPAY_TMN_CODE=       # Terminal Merchant ID
VNPAY_HASH_SECRET=    # Secret key for hashing
VNPAY_URL=            # https://sandbox.vnpayment.vn or https://pay.vnpayment.vn
VNPAY_RETURN_URL=     # Your return URL after payment
```

### Payment URL Generation

```typescript
import crypto from 'crypto';
import querystring from 'querystring';

interface VNPayPaymentRequest {
  orderId: string;
  amount: number;      // Amount in VND (NOT divided by 100 in request)
  orderInfo: string;
  ipAddr: string;
}

function createVNPayUrl(req: VNPayPaymentRequest): string {
  const tmnCode = process.env.VNPAY_TMN_CODE!;
  const hashSecret = process.env.VNPAY_HASH_SECRET!;
  const vnpUrl = process.env.VNPAY_URL!;

  const now = new Date();
  const vnpCreateDate = now.toISOString().replace(/[-:T]/g, '').slice(0, 14);
  const vnpExpireDate = new Date(now.getTime() + 15 * 60 * 1000)
    .toISOString()
    .replace(/[-:T]/g, '')
    .slice(0, 14);

  const params: Record<string, string> = {
    vnp_Version: '2.1.0',
    vnp_Command: 'pay',
    vnp_TmnCode: tmnCode,
    vnp_Locale: 'vn',
    vnp_CurrCode: 'VND',
    vnp_TxnRef: req.orderId,
    vnp_OrderInfo: req.orderInfo,
    vnp_OrderType: 'other',
    vnp_Amount: String(req.amount * 100), // VNPay multiplies by 100
    vnp_ReturnUrl: process.env.VNPAY_RETURN_URL!,
    vnp_IpAddr: req.ipAddr,
    vnp_CreateDate: vnpCreateDate,
    vnp_ExpireDate: vnpExpireDate,
  };

  // Sort alphabetically — VNPay requires this
  const sortedKeys = Object.keys(params).sort();
  const signData = sortedKeys.map((k) => `${k}=${params[k]}`).join('&');
  const vnpSecureHash = crypto
    .createHmac('sha512', hashSecret)
    .update(signData)
    .digest('hex');

  const query = querystring.stringify({ ...params, vnp_SecureHash: vnpSecureHash, vnp_SecureHashType: 'SHA512' });

  return `${vnpUrl}/paymentv2/vpcpay.html?${query}`;
}
```

### VNPay Return Handler

```typescript
async function handleVNPayReturn(req: Request) {
  const hashSecret = process.env.VNPAY_HASH_SECRET!;

  const {
    vnp_TxnRef,      // Order ID
    vnp_Amount,      // Amount (already * 100 by VNPay)
    vnp_ResponseCode, // 00 = success
    vnp_TransactionNo,
    vnp_BankCode,
    vnp_PayDate,
    vnp_SecureHash,
    ...fields
  } = req.query as Record<string, string>;

  // Remove secure hash and re-compute
  const sortedKeys = Object.keys(fields).filter(k => k.startsWith('vnp_')).sort();
  const signData = sortedKeys.map((k) => `${k}=${fields[k]}`).join('&');
  const expectedHash = crypto
    .createHmac('sha512', hashSecret)
    .update(signData)
    .digest('hex');

  if (vnp_SecureHash !== expectedHash) {
    return Response.redirect('/payment/failed?error=invalid_signature');
  }

  if (vnp_ResponseCode !== '00') {
    return Response.redirect(`/payment/failed?code=${vnp_ResponseCode}`);
  }

  const amountVND = Number(vnp_Amount) / 100;
  await db.$transaction([
    db.orders.update({ where: { id: vnp_TxnRef }, data: { status: 'PAID' } }),
    db.vnpayTransactions.create({
      data: {
        orderId: vnp_TxnRef,
        amount: amountVND,
        transactionNo: vnp_TransactionNo,
        bankCode: vnp_BankCode,
        payDate: vnp_PayDate,
      },
    }),
  ]);

  return Response.redirect('/payment/success');
}
```

### VNPay Signature Gotcha

VNPay requires **alphabetical ordering** of all fields when computing the secure hash. The fields must be exactly what was sent — do not include `vnp_SecureHash` or `vnp_SecureHashType` in the hash computation.

---

## VietQR

### Environment Setup

```
VIETQR_API_KEY=     # VietQR API key
VIETQR_BANK_BIN=    # Default bank BIN code
VIETQR_ENDPOINT=    # https://api.vietqr.io or sandbox
```

### QR Code Generation

```typescript
async function generateVietQR(orderId: string, amount: number, accountNumber: string, bankBin: string) {
  const accountName = 'CONG TY ABC'; // Registered account name

  const qrPayload = buildVietQRPayload({
    bankBin,
    accountNumber,
    accountName,
    amount,
    orderId,
  });

  const response = await fetch('https://api.vietqr.io/v2/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-client-id': process.env.VIETQR_CLIENT_ID!,
      'x-api-key': process.env.VIETQR_API_KEY!,
    },
    body: JSON.stringify({
      accountNo: accountNumber,
      accountName,
      acqId: bankBin,  // Acquiring bank ID
      addData: `TT${orderId}`,
      amount: String(amount),
      format: 'text',
      template: 'compact2',
    }),
  });

  return response.json();
}

function buildVietQRPayload(data: {
  bankBin: string;
  accountNumber: string;
  accountName: string;
  amount: number;
  orderId: string;
}): string {
  // VietQR follows EMVCo standard
  const fields = [
    { id: '00', value: '01' },                              // Payload Format Indicator
    { id: '01', value: '11' },                              // Point of Initiation Method (static = 11)
    { id: '38', value: `${data.accountName.length}${data.accountName}` }, // Merchant Name
    { id: '52', value: data.bankBin },                      // Merchant Category Code
    { id: '53', value: '704' },                             // Transaction Currency (VND = 704)
    { id: '54', value: String(data.amount) },              // Transaction Amount
    { id: '58', value: 'VN' },                             // Country Code
    { id: '63', value: '01' },                              // Checksum (CRC16)
  ];

  const payload = fields.map(f => `${f.id}${f.value}`).join('');
  const crc = calculateCRC16(payload); // CRC-16/CCITT-FALSE
  return `${payload}${crc}`;
}
```

---

## Common Infrastructure

### Webhook Idempotency Table

```sql
CREATE TABLE webhook_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  provider VARCHAR(50) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(100) NOT NULL,
  payload JSONB NOT NULL,
  processed_at TIMESTAMPTZ DEFAULT NOW(),
  status VARCHAR(20) DEFAULT 'PROCESSING',
  UNIQUE(provider, event_id)
);

CREATE INDEX idx_webhook_events_status ON webhook_events(provider, status);
```

### Retry Pattern for Payment API Calls

```typescript
async function callPaymentAPIWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelayMs = 1000
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      // Only retry on transient errors
      if (!isTransientError(error)) {
        throw error;
      }

      if (attempt < maxRetries - 1) {
        const delay = baseDelayMs * Math.pow(2, attempt);
        await new Promise((resolve) => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError!;
}

function isTransientError(error: Error): boolean {
  const transientCodes = ['ECONNRESET', 'ETIMEDOUT', 'ECONNREFUSED', '502', '503', '504'];
  return transientCodes.some(
    (code) => error.message.includes(code) || (error as NodeJS.ErrnoException).code === code
  );
}
```

### Payment Status State Machine

```
PENDING → SUCCESS (webhook received, amount verified)
PENDING → FAILED (webhook with error code)
PENDING → EXPIRED (timeout, e.g., 15 min)
SUCCESS → REFUNDED (refund processed)
SUCCESS → DISPUTED (customer dispute)
```

### Testing Banks & Sandboxes

| Provider | Sandbox URL | Test Credentials |
|----------|-------------|-------------------|
| MoMo | `test-payment.momo.vn` | Use MoMo test accounts |
| SePay | `api.sepay.vn` (has test mode) | Test bank accounts via dashboard |
| PayOS | `api-sandbox.payos.vn` | Test via PayOS dashboard |
| ZaloPay | `sb-openapi.zalopay.vn` | Test merchants via ZaloPay portal |
| VNPay | `sandbox.vnpayment.vn` | Test TMN code from VNPay portal |
| VietQR | `https://api.vietqr.io` | Test mode available |
