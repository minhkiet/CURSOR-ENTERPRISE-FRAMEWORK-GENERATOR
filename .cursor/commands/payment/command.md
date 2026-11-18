---
description: Payment - Review payment integration Việt Nam (MoMo, SePay, PayOS, ZaloPay, VNPay, VietQR)
trigger: payment, thanh toán, momo, sepay, payos, zalo pay, vnpay, vietqr, payment integration, webhook
category: Domain
framework: Cursor Enterprise Framework V4
version: 1.0.0
---

# Command: /payment

## Mục tiêu
Review payment integration cho các payment provider phổ biến tại Việt Nam.

## Trigger Keywords
- payment
- thanh toán
- momo
- sepay
- payos
- zalo pay
- zalo pay integration
- vnpay
- vietqr
- payment integration
- webhook payment
- thanh toán momo
- thanh toán vn
- payment gateway
- payment provider
- refund
- refund payment
- payment reconciliation
- payment flow

## Supported Providers

### MoMo (MoMo Payment)
- [ ] API integration review
- [ ] Webhook security (signature validation)
- [ ] Payment flow (create, confirm, refund)
- [ ] Error handling
- [ ] Idempotency
- [ ] Reconciliation

### SePay (SePay Banking - AI Agent 7-Step Lifecycle)
- [ ] **1. Skills**: Nạp kỹ năng sepay & sec_vietnam-payment-review
- [ ] **2. CLI & Auth**: Chạy sepay login (hoặc 	ools/api_integrations/sepay_integration.py)
- [ ] **3. Sandbox & Listen**: Khởi tạo sandbox & webhook listen: sepay sandbox init --with-webhook-listen --yes
- [ ] **4. Build Integration**: Xác thực webhook (Apikey), chống trùng UNIQUE(transaction_id) + INSERT IGNORE, mã đơn ngẫu nhiên, atomic SQL update
- [ ] **5. Test & Simulate**: Kiểm thử giao dịch mô phỏng: sepay webhook test --forward localhost:3000 --amount 50000 --order <CODE>
- [ ] **6. Production Go-Live**: Đăng ký webhook production: sepay webhook create --env production --url <LIVE_URL> (sau khi duyệt)
- [ ] **7. MCP Daily Monitor**: Giám sát lỗi webhook và đối soát dòng tiền qua SePay MCP

### PayOS (PayOS Open Banking Gateway API v2)
- [ ] **1. Credentials**: PAYOS_CLIENT_ID, PAYOS_API_KEY, PAYOS_CHECKSUM_KEY lưu trong .env
- [ ] **2. Payment Request (POST /v2/payment-requests)**: orderCode số nguyên dương (<= MAX_SAFE_INTEGER), amount VND, description tối đa 25 ký tự
- [ ] **3. Chữ ký request**: Tính HMAC-SHA256 với PAYOS_CHECKSUM_KEY theo 5 tham số A-Z (amount, cancelUrl, description, orderCode, returnUrl)
- [ ] **4. Checksum Webhook**: Xác thực HMAC-SHA256 từ dictionary data (sắp xếp keys A-Z) với signature nhận được
- [ ] **5. Idempotency & Database**: Đánh chỉ mục UNIQUE cho orderCode, cập nhật Atomic UPDATE ... WHERE order_code = ? AND status = 'pending' AND amount <= ?
- [ ] **6. Phản hồi Webhook**: Trả lời HTTP 200 {"success": true} ngay sau khi xác thực
- [ ] **7. Quản lý trạng thái**: Xử lý đầy đủ PENDING, PAID, CANCELLED

### Pay2S (Pay2S Banking Webhook & Recipient Name API)
- [ ] **1. Webhook Auth**: Xác thực header Authorization: Bearer <PAY2S_WEBHOOK_TOKEN>
- [ ] **2. Transaction Extraction**: Xử lý mảng transactions: [...], lọc transferType === "IN"
- [ ] **3. Phản hồi bắt buộc**: Trả lời HTTP 200 {"success": true} ngay lập tức
- [ ] **4. Retry Handling**: Cơ chế xử lý dưới 2s, đẩy việc nặng vào Queue để tránh 5 lần retry của Pay2S
- [ ] **5. Idempotency**: Đánh chỉ mục UNIQUE cho id / transactionNumber
- [ ] **6. Recipient Name Lookup (get-recipient-name)**: Gửi pay2s-token: <BASE64_SECRET_KEY>, body accountNumber và bankCode
- [ ] **7. Rate Limit**: Áp dụng cache (Redis/DB) không vượt quá 10 req/phút

### ZaloPay
- [ ] API integration review
- [ ] App-based payment
- [ ] Webhook security
- [ ] Error handling

### VNPay
- [ ] Gateway integration review
- [ ] Payment flow
- [ ] Return URL handling
- [ ] Security checks
- [ ] Error handling

### VietQR
- [ ] QR payment integration
- [ ] Bank account validation
- [ ] Transaction verification
- [ ] Error handling

### Multi-Provider Quota & Auto-Failover (SePay -> PayOS -> Pay2S -> Manual)
- [ ] **1. Quota Tracking**: Thiết lập `daily_tx_limit` và `daily_amount_limit` cho từng tài khoản
- [ ] **2. Priority Routing**: Tự động chuyển tuần tự Priority 1 (SePay) -> Priority 2 (PayOS) -> Priority 3 (Pay2S)
- [ ] **3. Auto-Failover**: Tự động chuyển cổng kế tiếp ngay khi cổng trước đạt trần hạn mức hoặc vượt giới hạn số tiền
- [ ] **4. Fallback thủ công**: Khi toàn bộ cổng tự động hết hạn mức, tự động chuyển đơn sang chế độ chuyển khoản thủ công
- [ ] **5. Kênh liên hệ xác thực**: Cung cấp hotline/Zalo/Telegram của hỗ trợ viên trong thông báo đơn hàng
- [ ] **6. Tải hình ảnh hóa đơn (Receipt Proof)**: Cho phép khách hàng tải ảnh biên lai chuyển khoản (.jpg, .png, .pdf)
- [ ] **7. Admin Review Workflow**: Giao diện nhân viên duyệt (approve/reject) đối soát tiền về tài khoản thủ công

## Liên kết
- [[../skills/pay2s]] - Pay2S Integration Skill
- [[../skills/payos]] - PayOS Integration Skill
- [[../skills/sepay]] - SePay Integration Skill
- [[../skills/vietnam-payment-review]] - Vietnam Payment Review Skill
- [[../rules/billing]] - Billing Rules
- [[../rules/security]] - Security Rules
- [[../rules/web-security]] - Web Security Rules
