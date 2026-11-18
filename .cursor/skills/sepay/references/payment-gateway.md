# Payment gateway (cổng thanh toán): hosted checkout + IPN

## When

Only when the user needs buyers to pay by card (Visa / Mastercard / JCB) or NAPAS VietQR on a SePay-hosted page. Plain bank transfer into the business's own account → `webhook.md` + `vietqr.md` instead; do not propose the gateway for it. Each payment is a one-time order; recurring card payments are not supported. The gateway reports results by IPN. Not the same channel as bank webhooks (`webhook.md`); do not mix them.

## Flow

1. Ask the user's language and environment (default sandbox) and whether the server is local (sandbox IPN then comes through `sepay pg ipn listen`, else a tunnel: `testing-go-live.md` › Callbacks).
2. Get sandbox `merchant_id` + `secret_key` (my.sepay.vn → Cổng thanh toán). Keep the secret server side.
3. Create the order server side: build the checkout form fields (`merchant`, `operation=PURCHASE`, `order_amount`, `currency=VND`, `order_invoice_number`, `order_description`, `success_url` / `error_url` / `cancel_url`, optional `payment_method`, `customer_id`), sign them, POST the form to `{checkout host}/v1/checkout/init`. Or use the PHP / Node SDK.
4. Configure the IPN URL (Cổng thanh toán → Cấu hình → IPN) and auth type.
5. Handle IPN: verify `X-Secret-Key` (when auth type SECRET_KEY), find the order by `order.order_invoice_number`, check `notification_type` (e.g. `ORDER_PAID`) and amount, mark it paid with a conditional transition (`integration-design.md` § 3), reply HTTP 200.
6. Redirect pages (`success_url`…) only show a message; the order is paid only after the IPN (or an order API check).
7. Test in sandbox in the browser, then switch hosts and credentials for production.

## Hosts

Sandbox: API `https://pgapi-sandbox.sepay.vn`, checkout `https://pay-sandbox.sepay.vn`. Production: `https://pgapi.sepay.vn`, `https://pay.sepay.vn`. API calls use Basic auth `merchant_id:secret_key`. Confirm on `/vi/cong-thanh-toan/API/tong-quan` before relying on them.

## Best practice and traps

- Signature: only the allowed fields, **in the documented order** (do not sort), joined as `field=value` with commas, `base64(HMAC-SHA256(secret, string))` raw bytes. A reordered or extra field breaks it. Read `#xac-thuc-chu-ky` for the current field list.
- Never compute the signature in the browser; never expose `secret_key`.
- IPN is the source of truth, not the redirect; the buyer may close the tab.
- Idempotent IPN handler: the same notification can arrive more than once. "Update only if not already paid" must be one conditional `UPDATE … WHERE status = 'pending'` with the affected rows checked, not a read followed by a write; only the request that changed the row fulfils the order.
- `order_invoice_number` must be unique per order; use your internal order code so IPN maps straight back.
- IPN URL: a public address, never localhost or a private IP; HTTPS recommended in production, HTTP not blocked (SKILL.md Rule 5).
- Recurring card payments are not supported: do not design or promise subscriptions on the gateway.
- Sandbox data is isolated from production; switching = change hosts + credentials + IPN URL, nothing else.
- Bank transfer (`payment_method=BANK_TRANSFER`) pays into a bank account the merchant linked in my.sepay.vn, so the banks and account types it works with are the SePay Webhooks supported-banks table: read it via `banks.md` (do not answer from memory). An account marked "chỉ qua VA" there needs a VA chosen in the gateway's bank transfer settings, or the gateway rejects the setup.
- Gateway rules that differ from the webhook table. State them as how the gateway works today:
  - VA per order (VA theo đơn hàng) on the gateway works only for BIDV business accounts and Shinhan Bank business accounts. Sacombank, Vietcombank and VietinBank (MAP) can create VA orders only through SePay API v2 (`/vi/sepay-api/v2/don-hang/bat-dau-nhanh`), not through the gateway checkout.
  - BIDV of every account type, MSB, KienlongBank and OCB must use a VA (a fixed VA or VA per order) in the gateway's bank transfer settings, even BIDV business accounts that receive on the main account for webhooks.
  - Any account marked "chỉ qua VA" in the webhook table (e.g. Vietcombank, VietinBank business with MAP) must also use a fixed VA in the gateway. The gateway lets you save their main account, but transfers to it are never recorded and the order stays unpaid. Never advise paying into the main account of such an account.

## Docs map

- `/vi/cong-thanh-toan/gioi-thieu#phuong-thuc-thanh-toan-duoc-ho-tro` "Phương thức thanh toán được hỗ trợ"
- Banks for bank transfer: `/vi/sepay-webhooks/tai-khoan-ngan-hang#ngan-hang-ho-tro` "Ngân hàng hỗ trợ" (see `banks.md`)
- `/vi/cong-thanh-toan/bat-dau` "Bắt đầu nhanh" (full walkthrough with code) · `#luong-hoat-dong-tong-quan` "Luồng hoạt động tổng quan"
- `/vi/cong-thanh-toan/API/don-hang/form-thanh-toan#danh-sach-tham-so` "Danh sách tham số" · `#xac-thuc-chu-ky` "Xác thực chữ ký"
- `/vi/cong-thanh-toan/IPN#cau-hinh-ipn-url` "Cấu hình IPN URL" · `#request-tu-sepay-den-merchant` "Request từ SePay đến Merchant"
- `/vi/cong-thanh-toan/luong-thanh-toan` "Luồng thanh toán"
- `/vi/cong-thanh-toan/sandbox#url-moi-truong-sandbox` "URL môi trường Sandbox" · `#chuyen-sang-production-khi-san-sang` "Chuyển sang Production khi sẵn sàng"
- `/vi/cong-thanh-toan/API/tong-quan#xac-thuc-api` "Xác thực API" · `#ma-loi-chung` "Mã lỗi chung"
- SDK: `/vi/cong-thanh-toan/sdk/php`, `/vi/cong-thanh-toan/sdk/nodejs`
- Order / transaction APIs: section `cong-thanh-toan`, pages under `API/don-hang/` and `API/giao-dich/`

## CLI

`sepay pg checkout init` creates a sandbox order and prints the checkout URL; `sepay pg ipn listen --forward localhost:<port>/<path>` brings sandbox IPN to a local handler without a tunnel (`testing-go-live.md` › Callbacks); `sepay pg --help` for the rest; the IPN body from the docs (map below).
