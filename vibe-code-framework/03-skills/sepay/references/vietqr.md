# VietQR: dynamic payment QR for bank transfers

## When

Show the buyer a QR with account, amount and memo prefilled, so the transfer arrives with the right payment code and the webhook (`webhook.md`) can match it. No API call: the QR is an image URL. Only when buyers must pay by card or NAPAS VietQR, use `payment-gateway.md` instead.

## Image URL

```
https://vietqr.app/img?acc=<account>&bank=<bank>&amount=<VND>&des=<memo>&template=<style>
```

| Param | Notes |
|---|---|
| `acc` (required) | Account number or VA number, depending on the bank rule below |
| `bank` (required) | Bank `short_name`, `alias`, `code` or `bin` from the bank list linked on the page |
| `amount` | Integer VND; empty = buyer types it |
| `des` | Memo: put the payment code (e.g. `DH123`) here; URL-encode it |
| `template` | empty = standard with VietQR logo, `compact` (checkout pages), `qronly`, `standee` (printed at the counter) |
| `showinfo`, `fullacc`, `holder`, `store`, `download` | Show account / holder / store info on the image, or force download |

Preview and copy styles at https://qr.sepay.vn. Read `#cau-truc-link-nhung` for the current parameter list.

## Bank rules (check the page: they change)

- Some banks require a VA (e.g. OCB, KienlongBank, MSB always; BIDV except businesses): use the VA number as `acc`.
- Content VA (TKP): `acc` = main account, `des` = `TKP` + VA code + your memo.
- VietinBank personal / household accounts: `des` must contain `SEVQR`, otherwise the transaction is not pushed to SePay.
- No VA: `acc` = account number, free memo.

## Best practice and traps

- Generate the URL server side from the order (amount + code) so the buyer cannot edit it; the webhook still re-checks the amount.
- Make the payment code unique per order and fit the whole payment-code structure (prefix, suffix character type and length), not only the prefix: see `webhook.md` § Matching. Put it at the **start** of `des` (after any string the bank requires, e.g. `SEVQR`), followed by a space: the sending and receiving banks may add text along the way and cut the memo, so a code at the end can be lost. Keep `des` short, unaccented letters, digits and spaces only.
- Show the account number, amount and memo as text too, for buyers who cannot scan; tell them not to change the memo.
- The payment page learns "paid" from your own backend, never from SePay's API (it is rate limited per IP): poll it about every 3 s and stop on paid, expired or a hidden tab, or push it from the backend over SSE / WebSocket. The status endpoint returns only status and amount due, no personal data. The webhook updates your backend.
- When partial payments are allowed (`integration-design.md` § 4a), after a partial transfer show what was received and what is still due, with a QR for the remainder.
- The QR always comes from the order's current state: a new amount gets a new QR; an expired or cancelled order shows no QR. Money still arriving on an old QR follows the late-payment policy (§ 4a).
- Full page + backend sample (frontend, 3 endpoints, DB schema, production checklist): `/vi/sepay-webhooks/tao-qr-va-form-thanh-toan`.

## Docs map

- `/vi/tien-ich-khac/tao-qr-code#cau-truc-link-nhung` "Cấu trúc link nhúng" · `#chon-kieu-hien-thi-qua-tham-so-template` · `#quy-tac-tao-vietqr-theo-ngan-hang-ma-sepay-ho-tro` · `#vi-du-su-dung` "Ví dụ sử dụng" · `#nhung-ma-qr-code-vao-website`
- `/vi/sepay-webhooks/tao-qr-va-form-thanh-toan#luong-hoat-dong` "Luồng hoạt động" · `#backend-3-endpoint` · `#checklist-production`
