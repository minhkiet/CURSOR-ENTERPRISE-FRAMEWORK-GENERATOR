---
name: source-command-sepay-command
description: SePay - Tích hợp thanh toán SePay (Bank Transfer, Webhook, VietQR, VA, e-Invoice, Gateway)
---

# source-command-sepay-command

Use this skill when the user asks to run the command `/sepay` or work with SePay payment integration.

## Command Template

# Command: /sepay

## Mục tiêu
Tích hợp, cấu hình, kiểm tra và gỡ lỗi hệ thống thanh toán tự động SePay (chuyển khoản ngân hàng, biến động số dư tức thời, VietQR, tài khoản ảo VA, Webhooks, e-Invoice, Payment Gateway, và SePay CLI / MCP).

## Trigger Keywords
- `sepay`, `thanh toán sepay`, `tích hợp sepay`
- `vietqr sepay`, `webhook sepay`, `sepay api`
- `biến động số dư`, `xác nhận chuyển khoản`
- `tài khoản ảo`, `virtual account`, `va sepay`
- `cổng thanh toán sepay`, `bankhub`, `speaker sepay`
- `đối soát sepay`, `hoàn tiền sepay`, `hóa đơn điện tử sepay`

## Workflow Tích Hợp

### 1. Phân Tích Yêu Cầu (Requirements & Scope)
- [ ] Xác định phương thức tích hợp: Webhook chuyển khoản trực tiếp, Tài khoản ảo VA, VietQR động hay Cổng thanh toán (Hosted Gateway)
- [ ] Chọn ngân hàng hỗ trợ phù hợp (tham khảo `references/banks.md`)
- [ ] Thiết lập môi trường thử nghiệm (Sandbox / Test mode trên my.sepay.vn hoặc `sepay sandbox init`)

### 2. Thiết Kế & Cấu Hình Webhook
- [ ] Tạo endpoint HTTPS công khai tiếp nhận Webhook từ SePay
- [ ] Xác thực bảo mật: Kiểm tra Header `Authorization: Apikey <API_KEY>`
- [ ] Đảm bảo tính Idempotency: Kiểm tra `transaction.id` hoặc `reference_number` tránh xử lý trùng lặp giao dịch
- [ ] Xử lý nội dung chuyển khoản (chỉ trích xuất mã đơn hàng, không eval / đưa thô vào prompt AI / SQL)

### 3. Tạo Mã Thanh Toán & VietQR
- [ ] Sinh mã thanh toán động hoặc gắn mã đơn hàng vào nội dung chuyển khoản
- [ ] Tạo link/ảnh VietQR theo chuẩn qua SePay VietQR API hoặc `https://qr.sepay.vn/img`

### 4. Kiểm Thử & Chạy Thật (Testing & Go-Live)
- [ ] Mô phỏng giao dịch trong chế độ Test mode / CLI: `sepay sandbox simulate`
- [ ] Kiểm tra lịch sử gửi Webhook trên dashboard SePay (Xác thực tự động Thành công / Thất bại)
- [ ] Chuyển sang Production và cấu hình tài khoản ngân hàng chính thức

## Liên kết
- [[../skills/sepay]] - SePay Skill
- [[../skills/sec_vietnam-payment-review]] - Vietnam Payment Review Skill
