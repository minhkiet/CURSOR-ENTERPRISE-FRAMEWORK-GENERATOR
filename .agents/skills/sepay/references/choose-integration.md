# Choosing a SePay integration

Default for confirming payments: **Webhooks**. Recommend the payment gateway only when the user says buyers must pay by card or by NAPAS VietQR; never propose it first.

Ask first if unclear: whose bank account receives the money, must buyers pay by card or NAPAS VietQR, is the app acting for many SePay users.

| Situation | Path | Reference |
|---|---|---|
| Money arrives by bank transfer into the business's **own** account (shop, SaaS, invoices) | **Webhooks** — recommended default, the platform's core | `webhook.md` |
| Same, plus one account number per order, exact-amount matching, or pulling data | Webhooks + **SePay API v2** (VA per order, reconciliation) | `sepay-api.md` |
| Only when buyers must pay by card (Visa / Mastercard / JCB) or NAPAS VietQR on a SePay-hosted page | **Payment gateway** (order + IPN) | `payment-gateway.md` |
| A platform reads bank accounts of **other** businesses it serves | **Bank Hub** (Hosted Link + IPN) | `bankhub.md` |
| Issue e-invoices after payment | **eInvoice API** | `einvoice.md` |
| A partner (POS, payment platform) that buys SePay speakers wholesale (white-label) for its merchants | **Speaker API** | `speaker-api.md` |
| Third-party app acting for SePay users (plugin, marketplace) | **OAuth2** | `oauth2.md` |
| Site runs a platform with an official SePay plugin (e.g. WooCommerce, HostBill; live list in `plugins.md`) | **Official plugin** | `plugins.md` |
| Send money back to a buyer | **Refund API** / gateway void | `refunds.md` |

## Webhooks vs payment gateway

They do not mix; each has its own notification channel.

- **Webhooks**: SePay POSTs each matching bank transaction to your URL. You match it to an order by a payment code in the transfer memo (configured prefix, e.g. `DH123`) or by a per-order VA. You build the QR / payment page yourself (VietQR image URL, see `vietqr.md`). Lowest cost, no card network.
- **Payment gateway**: you create an order, redirect the buyer to `pay.sepay.vn`, the gateway sends an IPN when paid. Use it only when buyers need card or NAPAS VietQR payment. Recurring card payments are not supported: each payment is a one-time order.

## Typical combinations

- Shop with QR checkout: webhook + payment code + VietQR image; reconciliation through `GET /v2/transactions` (`since_id`).
- Strict per-order matching (no memo typos): SePay API v2 order + VA, webhook for realtime, order status as source of truth.
- Buyers need card or NAPAS VietQR: payment gateway only; IPN updates the order.
- Accounting after payment: webhook or IPN → issue e-invoice → poll its status.

## Docs map

- `/vi/sepay-webhooks/tong-quan` "SePay Webhooks là gì?"
- `/vi/cong-thanh-toan/gioi-thieu#cong-thanh-toan-sepay-la-gi` "Cổng thanh toán SePay là gì?"
- `/vi/sepay-api/v2/gioi-thieu#ban-co-the-lam-gi` "Bạn có thể làm gì"
- `/vi/bankhub/tong-quan#doi-tuong-su-dung-sepay-bank-hub` "Đối tượng sử dụng SePay Bank Hub"
