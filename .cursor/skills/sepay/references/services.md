# What SePay offers

Overview of every product: https://developer.sepay.vn (vi) · https://developer.sepay.vn/en. Each line: what it is, entry page, reference file, CLI noun.

| Product | What it does | Entry page | Reference | CLI |
|---|---|---|---|---|
| SePay Webhooks | Push each bank transaction on your own accounts to your server | `/vi/sepay-webhooks/tong-quan` | `webhook.md` | `sepay webhook` |
| Payment gateway (Cổng thanh toán) | Hosted checkout for card and NAPAS VietQR payments (one-time); IPN. Use only when buyers need these | `/vi/cong-thanh-toan/gioi-thieu` | `payment-gateway.md` | `sepay pg` |
| SePay API v2 | Transactions, bank accounts, VA per order, orders | `/vi/sepay-api/v2/gioi-thieu` | `sepay-api.md` | `sepay transaction`, `bank-account`, `va`, `paycode`, `api` |
| Bank Hub | Link and read other businesses' bank accounts (Hosted Link) | `/vi/bankhub/tong-quan` | `bankhub.md` | `sepay bankhub` |
| eInvoice API | Issue e-invoices | `/vi/einvoice-api/v1/tong-quan` | `einvoice.md` | `sepay einvoice` |
| Speaker API | Payment announcer speakers sold wholesale (white-label) to partners, who pair them with their merchants | `/vi/speaker-api/tong-quan` | `speaker-api.md` | — |
| OAuth2 | Third-party apps acting for SePay users | `/vi/sepay-oauth2/tong-quan` | `oauth2.md` | — |
| VietQR image | Dynamic QR image URL for transfers | `/vi/tien-ich-khac/tao-qr-code` | `vietqr.md` | — |
| Refunds | Refund collected transfers (API v2), void card payments | `/vi/sepay-api/v2/hoan-tien` | `refunds.md` | — |
| Test mode | Sandbox in my.sepay.vn, simulated transactions | `/vi/tien-ich-khac/test-mode` | `testing-go-live.md` | `sepay sandbox` |
| Plugins | Official plugins for e-commerce / billing platforms (e.g. WooCommerce, HostBill) | `/vi/plugin` (live list) | `plugins.md` | — |
| SePay IPs | Addresses SePay calls from (allowlist) | `/vi/dia-chi-ip` | — | — |
| Changelog | What changed | `/vi/changelog` | `docs-lookup.md` | — |

Pages are under `https://developer.sepay.vn`; append `.md` for markdown. The site's navigation is the authority: if a product is missing here, check `https://developer.sepay.vn/llms.txt`.

## Researching a product ("SePay X là gì / hoạt động thế nào")

1. Pick the section from the table; if unsure, search (`docs-lookup.md`).
2. Read the overview page's sections "what it is", "who it is for", "flow" (one section at a time), then the quick start's step list.
3. Answer: the problem it solves, the main flow, the integration steps at a high level, then point to the reference file for details. Cite the pages.

## This skill

- Install: `npx skills add sepayvn/sepay-skills` (Claude Code only: add `-a claude-code`; Codex: `-a codex`; all projects: `-g`).
- Update: Claude Code plugin `claude plugin update sepay`; `npx` install `npx skills update sepay`; uploaded or unzipped file: download `sepay.zip` again. When to suggest it: `SKILL.md` › Tools worth suggesting.
- Hosted on skills.sh; source of truth for SePay facts stays developer.sepay.vn.
