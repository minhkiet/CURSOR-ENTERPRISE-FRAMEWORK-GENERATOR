---
name: source-command-pay2s-command
description: Pay2S - Tích hợp biến động số dư ngân hàng và tra cứu tài khoản Pay2S (Webhook Bearer Token, get-recipient-name API)
---

# source-command-pay2s-command

Use this skill when the user asks to run the command `/pay2s` or work with Pay2S webhook and recipient name lookup.

## Command Template

# Command: /pay2s

## Mục tiêu
Tích hợp, cấu hình, kiểm tra và gỡ lỗi dịch vụ Pay2S: tiếp nhận và xử lý Webhook biến động số dư ngân hàng qua Bearer Token, bóc tách danh sách giao dịch, chống xử lý trùng lặp, và tra cứu tên chủ tài khoản ngân hàng thụ hưởng (`get-recipient-name`).

## Trigger Keywords
- `pay2s`, `thanh toán pay2s`, `tích hợp pay2s`
- `webhook pay2s`, `biến động số dư pay2s`
- `tra cứu tên tài khoản pay2s`, `get-recipient-name`
- `kiểm tra số tài khoản pay2s`, `pay2s token`

## Workflow Tích Hợp

### 1. Webhook Biến Động Số Dư
- [ ] Lấy `Webhook Token` từ trang quản lý Pay2S
- [ ] Cấu hình Endpoint HTTPS trên hệ thống
- [ ] Xác thực Header: `Authorization: Bearer <PAY2S_WEBHOOK_TOKEN>`
- [ ] Bóc tách `transactions: [...]` và lọc `transferType === "IN"`
- [ ] Chống trùng (Idempotency) bằng `id` hoặc `transactionNumber`
- [ ] Phản hồi HTTP 200 với body JSON: `{"success": true}` ngay lập tức

### 2. Tra Cứu Tên Chủ Tài Khoản (`get-recipient-name`)
- [ ] Lấy `SecretKey` từ Pay2S và mã hóa sang Base64 để tạo header `pay2s-token`
- [ ] Gọi `POST https://api.pay2s.vn/userapi/get-recipient-name` với body:
  ```json
  {
    "accountNumber": "<SỐ_TÀI_KHOẢN>",
    "bankCode": "<MÃ_NGÂN_HÀNG>"
  }
  ```
- [ ] Bóc tách tên chủ tài khoản từ `data.accountName`
- [ ] Triển khai bộ nhớ đệm (Cache) để tuân thủ hạn mức 10 requests / phút

## Liên kết
- [[../skills/pay2s]] - Pay2S Skill
- [[../skills/sec_vietnam-payment-review]] - Vietnam Payment Review Skill
- [[../commands/payment]] - Payment Command Tổng Hợp
