# Supported banks

The lists change; never answer from memory or from this file. Each question has its own list; fetch only that section (`?anchor=` returns just the section, as Markdown):

| Question | Vietnamese | English |
|---|---|---|
| Which banks send webhooks (linked accounts, VA, tiền vào / ra) | https://developer.sepay.vn/vi/sepay-webhooks/tai-khoan-ngan-hang.md?anchor=ngan-hang-ho-tro | https://developer.sepay.vn/en/sepay-webhooks/tai-khoan-ngan-hang.md?anchor=supported-banks |
| VA per order (SePay API v2): banks, exact-amount and multi-payment rules | https://developer.sepay.vn/vi/sepay-api/v2/don-hang/bat-dau-nhanh.md?anchor=ngan-hang-ho-tro | https://developer.sepay.vn/en/sepay-api/v2/don-hang/bat-dau-nhanh.md?anchor=supported-banks |
| Bank Hub (linking other businesses' accounts) | https://developer.sepay.vn/vi/bankhub/tong-quan.md?anchor=cac-ngan-hang-ho-tro | https://developer.sepay.vn/en/bankhub/tong-quan.md?anchor=supported-banks |

```bash
curl -sL 'https://developer.sepay.vn/vi/sepay-webhooks/tai-khoan-ngan-hang.md?anchor=ngan-hang-ho-tro'
```

Anchors differ by language. A wrong one returns `{"error":"Anchor not found","anchors":[…]}` with the valid list; pick from it. With SePay MCP tools: `fetch_content` id `sepay-webhooks/tai-khoan-ngan-hang` (see `docs-lookup.md`).

## Reading the table

One row per bank and account type (cá nhân, hộ kinh doanh, doanh nghiệp; VPBank has 4 rows: NEO cá nhân, NEO hộ kinh doanh, NEOBiz hộ kinh doanh, NEOBiz doanh nghiệp). Always ask the user's account type before answering for BIDV, VietinBank or VPBank: the answer differs by type. For an account already linked, read it instead of guessing from the type: `sepay bank-account list --json` (or `get`) gives `va_only` (true = money reaches the shop only through a VA) and `official_va_supported`; these fields decide over the table.

| Column | Meaning |
|---|---|
| Loại tài khoản | The account type chosen when linking the account in my.sepay.vn. |
| Nhận tiền ở tài khoản chính | "Không, chỉ qua VA" = transfers to the main account number are not received; create at least 1 official VA and have buyers pay into it. |
| VA chính thức | The bank issues real VA numbers for this account type. "Không" + main account "Có" → use content VA (TKP). |
| Tiền vào / Tiền ra | SePay reports incoming / outgoing transfers. A webhook "Chỉ tiền ra" only works where Tiền ra = Có, and not with official VAs. |

- **Official VA**: the buyer transfers to a dedicated account number; matching by that number.
- **Content VA (TKP)**: no own number; the buyer transfers to the main account with the TKP code in the memo; matching by memo. Both arrive in the webhook field `subAccount`.
- A bank missing from the table does not support webhooks. The most current list is in my.sepay.vn → Tài khoản ngân hàng → Thêm tài khoản.

## Other bank lists (different questions)

- VA per order and Bank Hub have their own lists (table above); never answer them from the webhook table.
- Payment gateway: bank transfer pays into a linked account, so it uses **this** table (same banks, same "chỉ qua VA" rule; `payment-gateway.md`). The list of payment methods (VietQR, NAPAS, cards) is at `/vi/cong-thanh-toan/gioi-thieu#phuong-thuc-thanh-toan-duoc-ho-tro`.
- VietQR bank codes and per-bank QR rules (VA required, `SEVQR` memo): `vietqr.md`.
- `https://vietqr.app/banks.json` lists bank codes for building QR images. Its `supported` field means the bank works with the QR image, not that it sends webhooks: never answer "which banks support SePay" from it.
- Banks that support refunds: `refunds.md` (read live from the docs).

## CLI

`sepay bank-account list` shows the accounts already linked to the user's company (not the supported list).
