# eInvoice API: issue e-invoices (hóa đơn điện tử)

## When

Issue, adjust, replace or look up Vietnamese e-invoices for a household business or company after a sale, through SePay's provider accounts.

## Flow

1. Ask language and environment (default sandbox: `https://einvoice-api-sandbox.sepay.vn`; production `https://einvoice-api.sepay.vn`).
2. `POST /v1/token` → Bearer `access_token` for every call.
3. `GET /v1/provider-accounts` → pick an active account; `GET /v1/provider-accounts/{id}` → its templates and **invoice series**.
4. `POST /v1/invoices/create` → `tracking_code`. With `is_draft: false` this creates, signs and submits in one step; with a draft, follow with `POST /v1/invoices/issue` (its own `tracking_code`).
5. Poll `GET /v1/invoices/create/check/{tracking_code}` (or `/issue/check/…`) until `status` is `Success` or `Failed`.
6. `GET /v1/invoices/{reference_code}` for the final invoice; `GET /v1/usage` for remaining quota.

## Three hard rules (an invoice that breaks one is rejected)

1. **`invoice_series` matches the current year**: form `C{YY}` (2026 → `C26`, 2027 → `C27`). Never hardcode it; read it from the provider-account detail API.
2. **`issued_date` within [tax authority's approval date of the registration, today]**, never in the future. Production checks the approval date; sandbox skips that check, so test the rule yourself.
3. **Always poll `tracking_code` to a final result** (Success / Failed) before ending the job. Creation is asynchronous; a request can stay `Pending` for up to 2 hours while SePay retries. Poll every 2–3 s at first, then follow `retry.next_retry_at`. Never fire-and-forget: a failed invoice must surface.

## Other best practice

- Make the create call idempotent on your side: store an intent row for the order **before** the call, then its `tracking_code`; after a crash, look the order up before creating again, so it never gets two invoices (`integration-design.md` § 2).
- Tax rates and decimal quantities have their own rules: read `#thong-tin-thue-suat` and `#so-luong-thap-phan` on the create page before building line items.
- Corrections go through adjustment / replacement invoices, never deletion of an issued invoice; only drafts can be deleted.
- Treat 4xx validation errors as final (fix the data), 5xx / timeouts as retryable with the documented schedule.

## Docs map

- `/vi/einvoice-api/v1/tong-quan#luong-xuat-hoa-don-dien-tu` "Luồng xuất hóa đơn điện tử" · `#dieu-chinh-hoa-don-da-phat-hanh` · `#moi-truong` "Môi trường"
- `/vi/einvoice-api/v1/bat-dau-nhanh` four steps: `#buoc-1-lay-access-token` · `#buoc-3-tao-va-phat-hanh-hoa-don` · `#buoc-4-kiem-tra-trang-thai-tao-hoa-don` (page is long: read one step)
- `/vi/einvoice-api/v1/xuat-hoa-don-dien-tu#api-request` "API Request" · `#thong-tin-thue-suat` · `#so-luong-thap-phan` · `#tham-so-mau-cho-cac-loai-hoa-don`
- `/vi/einvoice-api/v1/theo-doi-trang-thai-xuat-hoa-don#api-response` "API Response"
- `/vi/einvoice-api/v1/phat-hanh-hoa-don-dien-tu` (issue from draft)
- `/vi/einvoice-api/v1/xu-ly-loi#phan-loai-loi` "Phân loại lỗi" · `#lich-retry` · `#chan-doan-khi-hoa-don-khong-duoc-phat-hanh`
- `/vi/einvoice-api/v1/sandbox#lay-token-sandbox` "Lấy token Sandbox"
- Adjust / replace: `/vi/einvoice-api/v1/xuat-hoa-don-dieu-chinh`, `/vi/einvoice-api/v1/xuat-hoa-don-thay-the`

## CLI

`sepay einvoice --help` (sandbox first).
