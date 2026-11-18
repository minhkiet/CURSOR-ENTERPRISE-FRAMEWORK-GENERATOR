# Testing (Test mode, sandbox) and going live

## Default: test first

Unless the user says production, build and test in **Test mode / sandbox**: base URLs, credentials and data are separate from live; only hosts and credentials change at go-live, the integration steps do not. Read the product's "sandbox" / "so sánh với Live" page to list the differences.

| Product | Sandbox |
|---|---|
| Webhooks, SePay API v2 | Test mode in my.sepay.vn (sidebar → Test mode), API `https://userapi-sandbox.sepay.vn/v2` with a Test mode token |
| Payment gateway | `https://pgapi-sandbox.sepay.vn`, checkout `https://pay-sandbox.sepay.vn`, sandbox merchant credentials |
| Bank Hub | its own sandbox base URL, credentials and test accounts |
| eInvoice | `https://einvoice-api-sandbox.sepay.vn`, sandbox token |

Confirm hosts on the product's sandbox page before hardcoding them.

## Test mode (webhooks, API v2)

With the `sepay` CLI present (`command -v sepay`), set the sandbox up with it instead of clicking through steps 2–4: check what exists (`sepay bank-account list`), then `sepay sandbox init` (bank account, `--with-va`, `--with-webhook-listen` for `sepay webhook listen`, `--seed N`; read `sepay sandbox init --help` first; when not interactive pass every flag or `--yes`). Its `--with-webhook <url>` creates a webhook with no auth and without **Dùng để xác thực thanh toán**: create the webhook that confirms orders with `sepay webhook create` (`webhook.md` step 5). Payment codes: `sepay paycode list` (step 3). Simulate with `sepay sandbox simulate`. Without the CLI, or when a command is missing, use the steps below.

1. Turn on Test mode (SuperAdmin / Admin by default; others need the "Cho phép truy cập Test mode" permission).
2. Create or copy a bank account, optionally a VA (official VA prefix `SBSEPAY`, or a content VA).
3. Configure payment-code recognition for Test mode (separate from live).
4. Create the webhook (same auth types and filters as live), or an API Access token for `userapi-sandbox`.
5. Send a transaction from **Mô phỏng giao dịch**; the payload matches live. Check the delivery in the webhook history.
6. Test mode has quotas per resource (accounts, VAs, webhooks, simulated transactions); see `/vi/tien-ich-khac/test-mode/han-muc`.

## Callbacks from SePay to your machine

Webhooks and IPNs are sent by SePay's servers. While the handler runs on the user's machine, use the `sepay` CLI first; it needs no tunnel and no public URL (`cli.md`). Not installed: suggest it once (`SKILL.md` › Tools worth suggesting), install only with the user's go-ahead:

1. **SePay Webhooks** (sandbox; a production webhook delivers to its own public URL): `sepay webhook listen --forward localhost:3000/<path>` receives a copy of every delivery (same body and headers, so signature checks behave as in production) and forwards it to the local handler. `sepay webhook test` sends a sample delivery. Details: `sepay webhook listen --help`.
   - Start one `listen` only, in the background, and read its output: a `Listening for …` line means it is connected. Then read the coverage lines it prints next: an account that "produces no events", or a reason one is skipped (direction, VA rules, an empty VA list), means a sandbox payment there never reaches the handler; fix that webhook's filters (`sepay webhook list`, `webhook update`) before simulating, instead of waiting for an event. No such line within about 20 seconds, or `cannot reach the hub` / `temporarily unavailable`, means the forwarding service cannot be used right now: stop that process (by its PID), do not retry or start more, and go to step 4 with a sandbox webhook that has the tunnel URL. Tell the user in one line that live forwarding is unavailable for now, so you test through a temporary public address instead.
2. **Payment gateway IPN** (sandbox): `sepay pg ipn listen --forward localhost:3000/<path>` mirrors each IPN (same body and headers, `X-Secret-Key` included for a loopback address). It mirrors deliveries to the sandbox IPN endpoint, so one must be set: read it with `sepay pg ipn get`; set one with `sepay pg ipn set <url>` only when none is set, or after the user agrees to replace theirs. `sepay webhook listen` never carries IPN.
3. **Bank Hub IPN** (sandbox): `sepay bankhub ipn listen`.
4. **Only when the CLI cannot forward the callback** (a `listen` failed its check above) or the user cannot use the CLI: expose the port with a tunnel. Check what is installed (`command -v cloudflared`, `command -v ngrok`); offer to install one only with the user's go-ahead, then run e.g. `cloudflared tunnel --url http://localhost:3000` and use the HTTPS URL it prints.
5. A server with a public domain uses that URL directly (HTTPS recommended, HTTP accepted).
6. Never register `localhost`, `127.0.0.1`, `192.168.x`, `10.x` or other private addresses as the callback URL.

HTTP is accepted in Test mode and on live. An HTTPS URL needs a valid certificate on live (self-signed is rejected); Test mode also accepts self-signed.

## Go-live

Steps on my.sepay.vn (or with the `sepay` CLI, where each `--env production` write is the user's to run, Rule 3), in order:

1. Link the real bank account that receives the money.
2. Payment code structure on live matches the shop's order codes (**Công ty → Cấu hình chung → Cấu trúc mã thanh toán**); VA configuration recreated too. Test mode settings do not carry over.
3. The web is online at a public URL: HTTPS with a valid certificate recommended (HTTP works, with payload and headers in clear text); optionally SePay IP allowlist (`/vi/dia-chi-ip`).
4. Before creating it, list the live webhooks (`sepay webhook list --env production`) and tell the user which already receive the same bank account (all accounts, or that one), since each of them also gets the shop's transactions; changing or deleting any is the user's call. Then create the live webhook to that URL with the options of `webhook.md` step 5, auth on (HMAC-SHA256 or API key), read back with `sepay webhook get`.
5. Code that calls the SePay API on live (reconciliation, VA orders, refunds) needs a production API key: the user creates it in my.sepay.vn → **Cài đặt công ty → API Keys** and puts it in the server's environment; `sepay apikey create` makes sandbox keys only.
6. One small real transfer end to end before announcing.
7. Monitoring on: § After go-live (retry on server errors, the failure alert).

## After go-live: monitoring

- Turn on **Tự động gửi lại khi server trả lỗi** and **Bật cảnh báo khi webhook gặp lỗi liên tiếp** (with a threshold) in my.sepay.vn → Webhooks; the CLI cannot set them. Alert channels: `/vi/sepay-webhooks/giam-sat`.
- Reconciliation job running (`sepay-api.md`).
- In the first days, check the webhook's **Lịch sử gửi** and the **Xác thực tự động** label of each transaction for Thất bại (`debug-webhook.md`).

## Code ready for live (developers)

- Production credentials (payment gateway, API token, client secret) stored as secrets, never in the repo or the frontend; rate limits respected.
- Handler as in `integration-design.md`: `success` verdict (`webhook.md` § Response), idempotent, conditional state transitions (§ 3), empty secret rejects everything (§ 5), raw payload restricted and logs without memo, names or secrets (§ 6).

## Docs map

- `/vi/tien-ich-khac/test-mode#bat-test-mode` "Bật Test mode" · `#tai-nguyen-cau-hinh-trong-test-mode`
- `/vi/tien-ich-khac/test-mode/mo-phong-giao-dich#cac-truong-trong-form` · `#payload-webhook` "Payload webhook"
- `/vi/sepay-webhooks/test-mode/so-sanh-voi-live#khac-biet-giua-test-mode-va-live`
- `/vi/sepay-webhooks/test-mode/bat-dau-nhanh`
- `/vi/cong-thanh-toan/sandbox#chuyen-sang-production-khi-san-sang`
- `/vi/einvoice-api/v1/sandbox#chuyen-sang-production-khi-san-sang`
- `/vi/bankhub/thong-tin-sandbox#base-url-sandbox`
- `/vi/dia-chi-ip#danh-sach-dia-chi-ip`

## CLI

`sepay sandbox init`, `sepay sandbox simulate` (simulated transaction), `sepay sandbox reset --yes`, `sepay webhook listen`. `--env production` only when the user asks.
