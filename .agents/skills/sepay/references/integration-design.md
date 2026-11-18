# Integration design: duplicates, concurrency, failure, personal data

Applies to every SePay service: webhooks, payment gateway IPN, Bank Hub, VA orders, refunds, e-invoices, Speaker, OAuth2. Read it together with the service file, build these points into the code, and name the risk each one covers when you explain the design.

## 1. Inbound events: deduplicate and store before acknowledging

- Key on the provider's stable id (webhook / Bank Hub transaction `id`; for the gateway IPN, the id its payload page names). UNIQUE column, insert-ignore / `ON CONFLICT DO NOTHING`; never SELECT then INSERT.
- Store the event with a status (`received` → `processed` | `unmatched` | `failed`) in that same insert, then reply. When the reply carries a verdict (SePay webhook with payment verification: `webhook.md` § Response), decide it in the request and store it on the row; otherwise a worker processes `received` rows. Never mark "seen" in one place and enqueue in another: a crash between the two loses the event, and retries are skipped because the id already exists.
- Queues and workers deliver at least once: processing is idempotent by itself, not only the endpoint.
- Re-drive rows left in `received` for more than a few minutes.

### Reconciliation

The webhook `id` (integer) and the SePay API v2 transaction `id` (UUID) are different identifiers, and `reference_number` is not unique: never dedupe API rows against webhook events by id.

- Routine run (cron every 15–30 min): `GET /v2/transactions?since_id=<cursor>&per_page=100` (first run: `transaction_date_from`), page until empty, store the last API `id` as the new cursor (in the DB). Keep processed API ids in their own UNIQUE column so a row is handled once.
- For each money-in row: find the order by its `code` (or VA), apply the shop's amount rule (§ 4a) and run the same conditional paid transition as the webhook. Record on the order which transaction paid it: API `id`, `reference_number`, `transaction_date`, amount, source `reconciliation`.
- Order already paid: compare code, amount, transaction date, account number and reference with the transaction recorded on it. Same transfer (the webhook already handled it) → nothing to do; a different transfer → excess / second payment for review. A webhook arriving after reconciliation paid the order gets the same comparison and replies the paid verdict (`success: true`) when it is the same transfer.
- One order on demand (buyer says they paid, support check): `GET /v2/transactions?q=<order code>&transaction_date_from=<order created>`. `q` is a substring search over code, memo and reference, so keep only rows whose `code` equals the order code (case-insensitive).
- Stay under the API rate limit (`sepay-api.md`): pause between pages, back off on 429.

## 2. Outbound calls: a key stored before the call

- Refund, invoice create / issue, VA order create, Speaker notify: first store an intent row with a deterministic key built from business data (`refund-{order_code}-{n}`, `invoice-{order_id}`), then call, then store the provider's id on that row.
- After a timeout, resend with the same key or look the result up by it; never mint a new key. Where the API takes no idempotency key (check its docs), the stored intent plus a lookup before retrying is the guard.

## 3. State changes: atomic transitions, never check-then-act

- Change state with a conditional update and check the affected rows: `UPDATE orders SET status = 'paid' WHERE id = ? AND status = 'pending'`. One row: this request won, so it alone runs the side effects (fulfilment, credit, email, e-invoice, Speaker). Zero rows: someone else already did; record it and stop.
- Many writers race on one order: webhook, gateway IPN, reconciliation, expiry cron, admin action, a buyer who pays twice. All of them use the same transition. Money arriving after cancel / expiry follows the policy chosen in § 4a, never falls through.
- When partial payments add up (§ 4a), add amounts atomically (`paid_amount = paid_amount + ?` in SQL, or a row lock inside a transaction); never read, add and write back in app code.
- The read that decides a write runs on the primary database inside the same transaction, never on a replica or a cache.
- Unique codes (payment code, `order_code`, `order_invoice_number`) rely on a UNIQUE constraint and retry on conflict, not on "check whether it exists".
- Shared credentials (OAuth refresh token; Bank Hub, Speaker, e-invoice access tokens): refresh under a lock or single flight, so parallel workers do not race or burn a refresh token.
- Browser redirects (`success_url`, return pages) only show state; they never change it.

## 4. Money

- Integer VND, never float.
- Which amounts pay an order is the shop's choice (§ 4a). Whatever the rule, money that does not pay the order is kept on record for review or refund, and a second payment after the order is paid never fulfils it again.

## 4a. Business policies: ask before coding

These depend on the shop's business, not on SePay. Before writing the payment code, ask them in the same batch as the other choices (`SKILL.md` Rule 11), each with options and the recommended one first. In a non-interactive run, take the recommendation and say so in the reply.

**Money after the order is cancelled or expired**
1. Recommended: store as `unmatched`, reply `success: false`, put it on a refund list for a person; nothing ships.
2. Reopen the order and fulfil it if stock and price still allow: fits digital goods (courses, licences); risks overselling physical stock.
3. A setting the shop switches (`refund` / `reopen`), default 1.

With a VA per order the bank refuses transfers once the VA expires, so this case is rare; with a payment code in the memo nothing stops it.

**Which amounts pay the order**
1. Recommended (the usual flow): exact match. One transfer equal to the order amount pays it; any other amount is stored as `unmatched` (reply `success: false`) for review or refund. Put the amount in the paid transition: `UPDATE … SET status = 'paid' WHERE id = ? AND status = 'pending' AND amount = ?`.
2. At least the amount: one transfer `>=` pays; the excess is recorded for a refund.
3. Partial payments add up: keep the order pending with `paid_amount = paid_amount + ?`; it is paid when the total reaches the amount. The payment page shows "received X, Y still due" and a QR for exactly Y with the same code; never keep showing the full amount, or buyers pay it again.

With a VA per order the bank can enforce the exact amount itself (BIDV also supports partial payments).

## 5. Fail closed

- Secret or API key setting empty or missing → reject every callback; never skip verification (an empty HMAC key lets anyone sign).
- Unknown order code, wrong amount, unexpected `transferType` → store the event as `unmatched` for review; do not guess an order.
- Responses to SePay and to buyers carry no stack traces or internal details.

## 6. Logs and personal data

- Payloads carry personal and banking data: account numbers, `subAccount`, holder names, transfer memos that often hold names or phone numbers. Vietnam's personal data rules (Decree 13/2023/NĐ-CP) apply.
- The raw payload is the audit record: keep it in a DB table with restricted access and a retention period, not in application logs.
- Application logs carry identifiers only: event `id`, order code, amount, status, account number masked to the last 4 digits. Never log memos, names, `Authorization` / `X-Secret-Key` / signature headers, tokens or secrets.

## 7. Handover

Every project you create or change ships:

- `.env.example` (variable names, no values) and a lockfile that pins dependencies: run the package manager so it is generated and commit it (`package-lock.json`, `composer.lock`, `poetry.lock` / pinned `requirements.txt`, `go.sum`, `Gemfile.lock`…); a standard-library-only project says so in the README.
- Store `referenceCode` and the verdict with every webhook event.
- README: how to run, configure, and test with the `sepay` CLI.
- Before saying it is done, remove every temporary dump or print of payloads, headers or signatures added while debugging (`grep -rn` the project for them); they must not ship or be committed.
- Automated tests: bad signature rejected; empty secret setting rejects everything; the same `id` twice gives one effect; two different transactions for one order in parallel give one fulfilment; an amount the chosen rule does not accept is not marked paid; a SePay webhook replies `success: false` for an unmatched, under- or second payment and repeats the first verdict for a replayed `id`.
