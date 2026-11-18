# Ready-made plugins

If the user's site runs a platform that has an official SePay plugin, recommend the plugin before custom code: it shows the QR, receives the webhook and marks orders / invoices paid.

The plugin list grows; never answer which platforms have one from memory or from this file. Read it at answer time, then read the plugin's page:

```bash
curl -sL https://developer.sepay.vn/vi/plugin | grep -oE '/vi/plugin/[a-z0-9-]+' | sort -u
curl -sL https://developer.sepay.vn/vi/plugin/<slug>.md | grep '^##'
```

The sections below cover plugins known when this file was written; the plugin page wins when they differ.

## WooCommerce (WordPress)

1. Install "SePay Gateway" from WordPress.org (Plugins → Add New → search `sepay`), activate.
2. Connect the SePay account from the plugin's setup screen; the plugin then creates the matching webhook on SePay automatically.
3. Configure: bank account, VA (if the bank requires one), payment-code prefix (must match SePay's payment-code settings), success message, order status after payment, display options.
4. Test with a small order: status moves from On-Hold to Processing once the full amount arrives.

Traps: the site must be reachable from the Internet (no localhost as the webhook URL; while developing locally, `sepay webhook listen` forwards deliveries to the local site, `testing-go-live.md`); after a major-version upgrade read the upgrade section; webhook issues → check the webhook in my.sepay.vn and `debug-webhook.md`.

## HostBill

1. Install and activate the SePay module, then fill: bank, bank info, payment-code prefix, QR template, API key, behaviour for under / over-payment, periodic invoice check interval.
2. Copy the module's **Callback URL**.
3. In my.sepay.vn → Webhooks, create a webhook: event "Có tiền vào", the bank account, URL = that Callback URL, auth API key = the key set in the module, payment-code requirement matching the prefix.
4. Pay a test invoice.

## Other platforms

No official plugin listed → custom integration: `webhook.md` + `vietqr.md`, or `payment-gateway.md` only when buyers must pay by card or NAPAS VietQR. The plugin list lives under section `plugin` on developer.sepay.vn.

## Docs map

- `/vi/plugin/woocommerce#huong-dan-tich-hop` "Hướng dẫn tích hợp" · `#cau-hinh-sepay-gateway` · `#kiem-tra-cau-hinh-cua-ban` · `#xu-ly-su-co`
- `/vi/plugin/hostbill#1-cai-dat-va-cau-hinh-module-sepay-vao-hostbill` · `#123-tao-webhook-phia-sepay` · `#13-thu-nghiem-thanh-toan`
