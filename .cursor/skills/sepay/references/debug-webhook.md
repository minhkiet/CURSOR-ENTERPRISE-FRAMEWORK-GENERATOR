# Debugging SePay webhooks

Orders stopped being confirmed right after a live webhook or payment-code change: follow `cli.md` › Changing a live webhook or payment code, steps 4–6 (step 6 always gives the undo command), and use this file only for the diagnosis inside them.

Ask for the symptom if not given ("no request arrives", "401", "orders not marked paid", "duplicates"). First split the problem in two:

- **A. SePay did not send** (nothing in the delivery history for that transaction): configuration or filters.
- **B. SePay sent, your server failed** (history shows attempts with an error or a wrong response): endpoint, auth, response.

Look at the facts before guessing: the webhook's **Lịch sử gửi** (delivery history: status, `error_code` = cURL code, `response_time_ms`, response body) in my.sepay.vn → Webhooks. If the session has SePay MCP data tools, `list_webhook_logs` / `get_webhook_report` / `list_transactions` give the same facts (see `docs-lookup.md`); the CLI has `sepay webhook --help`. Neither in the session: suggest them once (`SKILL.md` › Tools worth suggesting).

## Checklist, in order (most problems are in the first steps)

1. Webhook is **on** (status Bật; saving does not re-enable a webhook you turned off).
2. URL reachable: "Gửi thử" (send test) from the webhook menu. DNS error, connection refused, SSL error → URL / server / certificate. A test send only shows the URL answers: after a live webhook or payment-code change, only a real transaction proves it (`cli.md` › Changing a live webhook or payment code, step 5).
3. Event type matches (money in / out / both).
4. The bank account that received the money is in the webhook's account list.
5. VA filter: the transaction went to a VA the webhook listens to (or the filter is off).
6. Payment code: if the webhook requires a code, the memo must contain one matching the configured prefix and length; otherwise SePay skips it (`code` null).
7. What your server returned: HTTP 200/201 with `success: true` within 30 s is Thành công; any other body or status is Thất bại. On a payment-verification webhook `{"success": false}` is the right reply for an unmatched / under / duplicate payment (`webhook.md` § Response); only connection failures and (if enabled) non-2xx are retried.
8. Silent retries: failed deliveries retry for about 33 min (8 attempts); your logs may show late duplicates. Dedupe by `id`.
9. OAuth-created webhooks: an expired / revoked token breaks auth; reconnect.

## Reading errors

| Seen in history | Meaning | Fix |
|---|---|---|
| cURL 6 | DNS | domain / DNS record |
| cURL 7 | connection refused | server down, port, firewall |
| cURL 28 | timeout > 30 s | keep the verdict path to the insert + match + conditional update; move side effects to a worker |
| cURL 35 / 51 / 60 | TLS / certificate / CA chain | valid cert, full chain (live rejects self-signed) |
| HTTP 401 | auth mismatch | API key or HMAC secret; HMAC on raw body |
| HTTP 403 | blocked | compare the firewall / WAF allowlist with the current list at `/vi/dia-chi-ip#danh-sach-dia-chi-ip` (fetch it; IPv6 too) |
| HTTP 404 / 405 | wrong path / method | exact path (case), accept POST |
| HTTP 5xx | your server error | your logs |

## Common causes of "paid but order not updated"

- Handler returns 200 but a different body → the transaction shows Thất bại and is not retried.
- Handler replies `success: true` to everything → duplicate, unmatched or wrong-amount payments show as Thành công; staff ship them. Fix the whole handler to `webhook.md` § Response, not only the reply line: auth on the raw body, UNIQUE insert by `id` with the stored verdict replayed, match, conditional paid transition, then the verdict.
- HMAC computed on re-serialized JSON instead of the raw body.
- Matching by memo text, but the bank altered or truncated it; use `code` / VA instead.
- Amount check fails (bank-specific exact-amount rules, partial payments).
- Localhost or a private IP registered as the URL; `sepay webhook listen` or the tunnel stopped (`testing-go-live.md`).

## When something was missed

1. First check whether SePay will still re-send it (**Lịch sử gửi**): no connection or no reply within 30 s always retries; a non-2xx only with **Tự động gửi lại khi server trả lỗi** on; a 2xx never. The schedule runs about 33 min (`#lich-retry`).
2. Retries still pending: fix the endpoint and wait for them; do not re-send by hand, since the manual and the automatic delivery of the same `id` then both arrive.
3. Re-send by hand (**Gửi lại** in Lịch sử gửi, or **Phát lại** in Sự cố) only when no retry will come: every attempt failed, or a non-2xx with automatic retry off. Then run reconciliation for the gap (`sepay-api.md`, `/vi/sepay-webhooks/doi-soat-giao-dich`).
4. On production the user can also re-send with `sepay webhook replay <transaction-id> --webhook <xid> --env production` (they run it, `cli.md` › Commands the user runs). First check that the handler dedupes on payload `id` (`webhook.md` § Response). Replies:
   - says replay works on sandbox only: that CLI version cannot do it; use **Gửi lại**.
   - `replay_already_delivered`: the handler acknowledged it; suggest `--force` only when its own logs show that delivery was not processed.
   - `replay_rate_limited`: the transaction hit SePay's replay cap; wait until the time in the message, do not retry.
   - `replay_busy`: the same replay is still running; try again in a minute.

## Docs map

- `/vi/sepay-webhooks/xu-ly-loi#chan-doan-webhook-khong-gui` "Chẩn đoán webhook không gửi" · `#phan-loai-loi` "Phân loại lỗi" · `#lich-retry` · `#cau-hoi-thuong-gap`
- `/vi/sepay-webhooks/giam-sat#lich-su-gui` "Lịch sử gửi" · `#canh-bao` "Cảnh báo"
- `/vi/sepay-webhooks/tich-hop-webhook#phan-hoi-hop-le` "Phản hồi hợp lệ"
- `/vi/sepay-webhooks/xac-thuc#hmac-sha256` "HMAC-SHA256"
- `/vi/sepay-webhooks/cau-hinh-ma-thanh-toan#ap-dung-cho-bo-loc-webhook` "Áp dụng cho bộ lọc webhook"
