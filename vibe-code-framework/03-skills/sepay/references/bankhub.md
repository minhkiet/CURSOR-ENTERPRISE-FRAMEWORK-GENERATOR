# Bank Hub: link other businesses' bank accounts

## When

A platform (POS, marketplace, SaaS) serves many merchants and needs each merchant's bank account linked so the platform sees their incoming payments. The merchant links through a SePay Hosted Link; the platform gets webhook events and balance-change IPNs.

## Flow

1. Ask language, environment (default sandbox), local or public server (IPN needs a public URL, HTTPS recommended, `testing-go-live.md`).
2. Get an access token: `POST /tokens` with the client credentials (Bearer token for every later call; refresh before expiry).
3. Create the merchant's company in Bank Hub; it must be **Active** before linking.
4. Create a link token → Hosted Link URL; open it (redirect or iframe) for the merchant; listen to the iframe `postMessage` events for UI state.
5. Receive webhook events (`BANK_ACCOUNT_LINKED`, unlink, restore…) to update your records.
6. Configure the balance-change IPN URL; handle each IPN: check the `Authorization: Apikey <key>` header (and / or SePay IP allowlist), store by transaction id, reply `{"success": true}` as JSON (`integration-design.md` § 1).
7. Query transactions / balances through the API when needed (endpoint lookup in `docs-lookup.md`).

## Best practice and traps

- IPN is sent only when the company is Active and its `transaction_amount` setting is > 0 or Unlimited; a silent IPN usually means one of these.
- IPN retries only on network failure (Fibonacci, about 33 min, connect timeout 5 s, response wait 8 s): respond fast, process async, dedupe by transaction id.
- Keep platform credentials and tokens server side; one token per platform, not per merchant browser, refreshed under a lock so parallel workers do not race.
- Webhook events and IPN are different channels: events describe link state, IPN describes money. Handle both.
- Sandbox has its own base URL, credentials and test accounts; nothing carries over to production.

## Docs map

- `/vi/bankhub/tong-quan#luong-hoat-dong` "Luồng hoạt động" · `#cac-ngan-hang-ho-tro` "Các ngân hàng hỗ trợ"
- `/vi/bankhub/bat-dau-nhanh#buoc-1-lay-access-token` · `#buoc-2-tao-link-token` · `#buoc-3-nhung-iframe-vao-website` · `#postmessage-events` "PostMessage Events"
- `/vi/bankhub/api/tong-quan-api#xac-thuc-api` "Xác thực API" · `#danh-sach-api-endpoints` "Danh sách API Endpoints" · `#best-practices` "Best Practices"
- `/vi/bankhub/api/tao-token#lam-moi-token` "Làm mới Token"
- `/vi/bankhub/webhook-event#luong-lien-ket-ngan-hang` "Luồng liên kết ngân hàng" · `#goi-lai-webhook` "Gọi lại Webhook"
- `/vi/bankhub/thong-bao-bien-dong-so-du#yeu-cau-bao-mat` "Yêu cầu bảo mật" · `#dieu-kien-sepay-thong-bao-ipn-toi-merchant` · `#co-che-retry` "Cơ chế retry"
- `/vi/bankhub/thong-tin-sandbox#danh-sach-tai-khoan-sandbox` "Danh sách tài khoản Sandbox"
- SDK: `/vi/bankhub/sdk`

## CLI

`sepay bankhub --help`: company create / edit (`--status Active`), link-token, `sepay bankhub ipn set <url> --api-key <key> --yes`, `sepay bankhub webhook set <url> --secret <key> --yes`.
