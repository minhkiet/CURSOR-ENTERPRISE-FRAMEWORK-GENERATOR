---
name: source-command-payos-command
description: PayOS - Tích hợp cổng thanh toán VietQR PayOS (Open Banking Gateway, Payment Links, Webhook Checksum)
---

# source-command-payos-command

Use this skill when the user asks to run the command `/payos` or work with PayOS payment gateway integration.

## Command Template

# Command: /payos

## Mục tiêu
Tích hợp, cấu hình, kiểm tra và gỡ lỗi cổng thanh toán mở PayOS (tạo payment link, sinh mã VietQR, xác thực chữ ký Webhook HMAC-SHA256 bằng Checksum Key, xử lý Idempotency và hoàn tất đơn hàng).

## Trigger Keywords
- `payos`, `thanh toán payos`, `tích hợp payos`
- `cổng thanh toán payos`, `vietqr payos`, `payos api`
- `webhook payos`, `checksum key payos`, `chữ ký payos`
- `payment-requests payos`, `payos sdk`

## Workflow Tích Hợp

### 1. Cấu hình thông tin (Credentials)
- [ ] Lấy `PAYOS_CLIENT_ID`, `PAYOS_API_KEY`, `PAYOS_CHECKSUM_KEY` từ trang quản trị `my.payos.vn`
- [ ] Lưu trữ an toàn trong file `.env` ở Backend (tuyệt đối không đưa ra Frontend)

### 2. Tạo link thanh toán (`POST /v2/payment-requests`)
- [ ] Chuẩn hóa `orderCode`: Bắt buộc là số nguyên dương (`integer`) không quá 16 chữ số
- [ ] Số tiền `amount`: Số nguyên VND (không chứa số thập phân)
- [ ] Mô tả `description`: Tối đa 25 ký tự, không dấu
- [ ] Tạo chữ ký `signature` bằng HMAC-SHA256 trên chuỗi 5 tham số sắp xếp theo bảng chữ cái:
  `amount={amount}&cancelUrl={cancelUrl}&description={description}&orderCode={orderCode}&returnUrl={returnUrl}`
- [ ] Nhận `checkoutUrl` và chuyển hướng khách hàng (Hosted hoặc Embedded)

### 3. Cấu hình & Xử lý Webhook
- [ ] Cấu hình Webhook URL công khai trên `my.payos.vn`
- [ ] Bóc tách `data` và `signature` từ webhook payload
- [ ] Sắp xếp các keys trong `data` theo thứ tự alphabet A-Z, nối chuỗi `key1=value1&key2=value2...`
- [ ] Tính mã băm HMAC-SHA256 với `PAYOS_CHECKSUM_KEY` và so sánh an toàn bằng `hash_equals` / `compare_digest`
- [ ] Phản hồi HTTP 200 `{"success": true}` ngay lập tức

### 4. An toàn dữ liệu & Chống trùng (Idempotency)
- [ ] Đặt chỉ mục `UNIQUE` cho `order_code`
- [ ] Sử dụng Atomic UPDATE:
  ```sql
  UPDATE orders 
  SET status = 'paid', paid_at = NOW() 
  WHERE order_code = ? AND status = 'pending' AND amount <= ?;
  ```

## Liên kết
- [[../skills/payos]] - PayOS Skill
- [[../skills/sec_vietnam-payment-review]] - Vietnam Payment Review Skill
- [[../commands/payment]] - Payment Command Tổng Hợp
