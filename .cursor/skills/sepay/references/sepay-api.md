# SePay API v2: transactions, bank accounts, VA per order, reconciliation

## When

Read transactions / bank accounts / virtual accounts, create orders with a dedicated VA, or reconcile what webhooks delivered. This file covers v2. New work uses the newest version listed in the docs (SKILL.md rule 5); if a version newer than v2 exists, follow its pages instead of this file. v1 only when maintaining or migrating (`/vi/sepay-api/v2/nang-cap-tu-v1`).

## Basics

- Base URL: production `https://userapi.sepay.vn/v2`, sandbox `https://userapi-sandbox.sepay.vn/v2` (same request / response shapes).
- Auth: `Authorization: Bearer <api_key>` (my.sepay.vn → Cài đặt công ty → API Keys). The key acts for the **whole company**: server side only, never in a browser or mobile app.
- Rate limit per IP (value: `/vi/sepay-api/v2/xac-thuc#rate-limiting`; checked before auth, HTTP 429): back off and retry; never poll in tight loops.

## Flow (orders + VA)

1. Ask language, environment (default sandbox), and the bank **and account type** of the account that will receive the money.
2. Before writing any code, read the supported-banks section; it is the only source for which bank + account type can create VA orders and what each needs (required params, `amount` rules, `order_code` length, partial payment, refunds). Never answer it from memory or from this file:
   ```bash
   curl -sL https://developer.sepay.vn/vi/sepay-api/v2/don-hang/bat-dau-nhanh.md | sed -n '/^## Ngân hàng hỗ trợ/,/^## Trạng thái/p'
   ```
   Not listed there → VA per order is not available for that account; fall back to a payment code in the memo (`webhook.md`). Through the payment gateway checkout the bank list is narrower (`payment-gateway.md`).
3. Fetch the per-bank prerequisite the section names (e.g. a VA prefix list or a terminal list) and keep its value for the order.
4. Create the order: `POST /v2/bank-accounts/{ba_xid}/orders` (`v2CreateOrder`) with `order_code` = your internal order code plus the bank's required fields. The response carries the VA (and QR when asked); show the buyer that account number.
5. Payment arrives → webhook (`webhook.md`) for realtime confirmation; the webhook carries the VA / order code.
6. Confirm from order state: `v2GetOrder` → `status`, `paid_amount`.
7. Extra VA for the same order (`POST …/orders/{order_xid}/va`, `v2CreateOrderVA`) only when the bank's rules allow it (`#thanh-toan-mot-phan`); done or abandoned → cancel the VA / order so it stops accepting money.

## Best practice and traps

1. **VA per order**: one order one VA (or VA prefix), matching is automatic when money arrives; cancel when finished. Read "Vòng đời VA theo đơn hàng" before designing expiry.
2. **Reconcile with webhooks**: webhook = push, realtime confirmation; `GET /v2/transactions` = pull, backfill when a webhook was missed (server down, timeout, retries exhausted). Pull new rows with `since_id`, match each to an order by code / VA and amount, never by id: the API `id` (UUID) is not the webhook `id` (integer). One order on demand: `q=<order code>`, then exact `code` match. Steps: `integration-design.md` § 1 Reconciliation. See `/vi/sepay-webhooks/doi-soat-giao-dich`.
3. **Avoid data mismatches**:
   - `order_code` is unique per company bank account; use your internal order code so webhook codes map to exactly one order.
   - A cancelled or expired VA no longer receives money.
   - Exact-amount vs partial payment, open orders and over-payment differ per bank: design the handler from `#ngan-hang-ho-tro` and `#thanh-toan-mot-phan` (step 2), and expect several webhooks for one order where partial payment is allowed: add amounts atomically (`integration-design.md` § 3).
   - Order status (`status`, `paid_amount`) is the source of truth; dedupe transactions by `id`.
4. Paginate list calls; IDs are strings (xid / UUID), not v1 integers.
5. Sandbox data is simulated and isolated; production needs a production key.

## Docs map

- `/vi/sepay-api/v2/gioi-thieu#moi-truong-api` "Môi trường API"
- `/vi/sepay-api/v2/xac-thuc#xac-thuc` "Xác thực" · `#rate-limiting` "Rate Limiting"
- `/vi/sepay-api/v2/bat-dau-nhanh#cac-buoc-thuc-hanh` "Các bước thực hành"
- `/vi/sepay-api/v2/don-hang/bat-dau-nhanh` VA per order: `#ngan-hang-ho-tro` "Ngân hàng hỗ trợ" · `#luong-xac-thuc-thanh-toan-qua-va-theo-don-hang` · `#cac-buoc-tich-hop` "Các bước tích hợp" · `#thanh-toan-mot-phan` "Thanh toán một phần" · `#huy-don-hang-hoac-va` "Hủy đơn hàng hoặc VA"
- Endpoints: `/vi/sepay-api/v2/don-hang/tao-don-hang`, `.../don-hang/tao-va`, `.../don-hang/chi-tiet`, `.../don-hang/huy-va`, `.../giao-dich/danh-sach`, `.../tai-khoan-ao/danh-sach`
- `/vi/sepay-webhooks/doi-soat-giao-dich#chien-luoc-doi-soat` "Chiến lược đối soát"
- `/vi/sepay-api/v2/nang-cap-tu-v1#bang-chuyen-doi-endpoint` "Bảng chuyển đổi endpoint"

## CLI

`sepay transaction list --json`, `sepay bank-account list`, `sepay va issue`, `sepay paycode`, `sepay apikey create` (sandbox), `sepay api /v2/...` for anything uncovered. Hosts, credentials and the response envelope: the API overview in the docs.
