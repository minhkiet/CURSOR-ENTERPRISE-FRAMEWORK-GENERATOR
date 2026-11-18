# Refunds and voids

Three different things; ask which one applies.

| Case | How | Reference |
|---|---|---|
| Money arrived by bank transfer (VA order or a collected transaction) and must go back | SePay API v2 refund (below) | this file |
| Card payment through the payment gateway | Gateway transaction void / cancel | `payment-gateway.md`, `/vi/cong-thanh-toan/API/giao-dich/huy-giao-dich` |
| Bank without refund support | Manual transfer from the bank app, record it yourself | — |

## Built-in limits

SePay enforces these on the server, whatever the caller sends:

- A refund names one collected transaction (by transaction ID, or by VA order, which picks its transaction or requires `transaction_id`). There is no free-form payout.
- The money goes back to the account that paid; the request has no destination account, only `refund_amount`.
- Cap: the total refunded for a transaction never exceeds what that transaction collected, `pending` refunds included.
- Authenticated API token (Bearer) and a required `X-Idempotency-Key`; a resend with the same key returns the same refund.
- The `sepay` CLI login does not request refund access.

You write and test the refund code (sandbox); a production refund or void is run by the user's app or the user, never by you (`SKILL.md` Security 9).

## SePay API v2 refund

Only some banks support it, and the list changes: never answer which banks from memory or from this file. Read it at answer time from the first callout of the refund overview (it sits before the first `##`, so the heading filter misses it):

```bash
curl -sL https://developer.sepay.vn/vi/sepay-api/v2/hoan-tien.md | sed -n '/^<Callout/,/^<\/Callout>/{p;/^<\/Callout>/q}'
```

The API has the final word: `422 unsupported_bank` = the account's bank cannot refund, `422 not_available` = refunds not enabled for that account. Sandbox skips this check, so a refund that works on Sandbox can still fail on production.

1. Prerequisites: API token, bank account UUID (`/v2/bank-accounts`), refunds enabled for that account.
2. Generate an idempotency key from business data and **store it before the call**: `refund-{order_code}-{n}` (≤ 100 chars, one key per refund). Take `n` from your refund rows with a UNIQUE (order, n) constraint, not from a count read in app code, or two parallel refunds get the same key and one is silently dropped.
3. Send: by order `POST /v2/bank-accounts/{ba_uuid}/orders/{order_uuid}/refund`, or by collected transaction (payment without an order), header `X-Idempotency-Key`. Empty `refund_amount` = refund all that remains of that transaction.
4. Handle the answer:
   - 200 → store `refund_id`, read `status` (`pending` → `succeeded` | `failed` | `rejected`).
   - Timeout, network error, `503 refund_busy`, `503 …connection_error` → wait a few seconds, resend with **the same key** (no double payout).
   - `409 idempotency_key_reused` → the key belongs to another request; check your data.
   - Other `422` → read `error_code`, do not auto-retry.
5. `pending` → check later with the refund detail / list API, until a final status.
6. Reconcile periodically: your stored keys vs the refund list.

## Rules that trip people up

- The limit is per **collected transaction**, not per order. An order paid in two transfers needs two refunds (two keys), and with several transactions you must pass `transaction_id` (else `422 transaction_required`).
- Refunding more than remains → `422`; fully refunded → `422 already_refunded`.
- A refund does not change the order's `status` / `paid_amount`; it is a separate record (`refund_status` on the order).
- `failed` / `rejected` are final; resending the same key returns the same error. To try again, use a new key.
- Never generate the key randomly in memory: after a timeout you could not resend the same refund.

## Docs map

- `/vi/sepay-api/v2/hoan-tien/index` overview: `#quy-tac-so-tien` "Quy tắc số tiền" · `#trang-thai-hoan-tien` · `#cac-buoc-tich-hop`
- `/vi/sepay-api/v2/hoan-tien/hoan-tien-don-hang#hoan-tien-cho-don-hang` · `#trang-thai-hoan-tien-cua-don-hang`
- `/vi/sepay-api/v2/hoan-tien/hoan-tien-giao-dich#hoan-tien-cho-giao-dich`
- `/vi/sepay-api/v2/hoan-tien/chong-trung-va-doi-soat#khoa-chong-trung-hoat-dong-the-nao` · `#luong-gui-lenh-an-toan` · `#doi-soat-dinh-ky`
- `/vi/sepay-api/v2/hoan-tien/danh-sach`, `/vi/sepay-api/v2/hoan-tien/chi-tiet`
- `/vi/sepay-api/v2/don-hang/bat-dau-nhanh#luong-hoan-tien` "Luồng hoàn tiền" (VA orders)
- Card void: `/vi/cong-thanh-toan/API/giao-dich/huy-giao-dich#dieu-kien-huy-giao-dich`
