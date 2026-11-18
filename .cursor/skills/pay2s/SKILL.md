---
name: pay2s
description: "Pay2S (Vietnam Bank Webhook & Recipient Name Lookup): Tích hợp Webhook biến động số dư tài khoản ngân hàng, xác thực Bearer token, xử lý danh sách giao dịch, cơ chế retry, và API tra cứu tên chủ tài khoản ngân hàng thụ hưởng (get-recipient-name)."
metadata:
  author: pay2s
  version: "1.0.0"
---

# Pay2S

Pay2S (pay2s.vn) là nền tảng cung cấp dịch vụ thông báo biến động số dư ngân hàng theo thời gian thực (Webhook) và API tra cứu định danh tài khoản ngân hàng thụ hưởng qua mạng lưới Napas.

- Tài liệu Webhook: https://docs.pay2s.vn/partner/webhook.html
- Tài liệu Tra cứu tài khoản: https://docs.pay2s.vn/get-recipient-name/tai-lieu-ky-thuat.html
- Cổng quản trị: https://pay2s.vn

---

## 1. Tài Liệu Tham Khảo Trong `references/`

| Nội dung | File tham khảo |
|---|---|
| Cấu hình Webhook, Header Bearer Token, cấu trúc `transactions[]`, cơ chế retry | `references/webhook.md` |
| API tra cứu tên chủ tài khoản (`get-recipient-name`), Base64 SecretKey token, Rate limit | `references/recipient-name.md` |
| Thiết kế hệ thống: Chống trùng đơn, Atomic UPDATE, xác minh người nhận trước khi chuyển | `references/integration-design.md` |

---

## 2. Các Tính Năng Cốt Lõi

### A. Webhook Biến Động Số Dư (Realtime Transaction Push)
- **Phương thức:** HTTP `POST` gửi đến URL HTTPS của đối tác.
- **Xác thực:** Header `Authorization: Bearer <YOUR_TOKEN_WEBHOOK>`.
- **Payload:** Danh sách giao dịch `transactions: [{ id, gateway, transactionDate, transactionNumber, accountNumber, content, transferType, transferAmount, checksum }]`.
- **Phản hồi bắt buộc:** HTTP 200 với body JSON:
  ```json
  {
    "success": true
  }
  ```
- **Cơ chế Retry:** Thử lại 5 lần cách nhau 60 giây (tổng cộng 6 lần) nếu không nhận được HTTP 200 hoặc `"success": true`.

### B. Tra Cứu Tên Chủ Tài Khoản Ngân Hàng (`get-recipient-name`)
- **Endpoint:** `POST https://api.pay2s.vn/userapi/get-recipient-name`
- **Header:** `pay2s-token: <BASE64_ENCODED_SECRET_KEY>`
- **Request Body:**
  ```json
  {
    "accountNumber": "1234567890",
    "bankCode": "VCB"
  }
  ```
- **Giới hạn tốc độ (Rate Limit):** Tối đa 10 requests / phút.
- **Phản hồi:**
  ```json
  {
    "status": true,
    "messages": "Thành công",
    "data": {
      "accountName": "NGUYEN VAN A"
    }
  }
  ```

---

## 3. Nguyên Tắc An Toàn Khi Tích Hợp

1. **Kiểm tra Token Webhook:** Luôn so sánh giá trị trong header `Authorization` với Token đã cấu hình trước khi xử lý mảng `transactions`.
2. **Xử lý Idempotency:** Ràng buộc duy nhất `transactionNumber` hoặc `id` ở cấp database; không cộng tiền trùng khi Pay2S gửi retry.
3. **Kiểm tra `transferType`:** Chỉ xử lý đơn hàng khi `transferType === 'IN'`.
4. **Phản hồi tức thì:** Lưu giao dịch vào hàng đợi (Queue / Job) và trả về `{"success": true}` ngay lập tức.
