---
name: payos
description: "PayOS (Vietnam Open Banking & VietQR Payment Gateway): API v2 integration, payment link creation, checkout flow, webhook handling, checksum-key signature verification, and reconciliation. Use when implementing or reviewing PayOS payments, VietQR banking transfers, webhooks, or refund/cancellation."
metadata:
  author: payos
  version: "1.0.0"
---

# PayOS

PayOS là giải pháp cổng thanh toán mở (Open Banking Payment Gateway) hàng đầu tại Việt Nam, kết nối trực tiếp tài khoản ngân hàng của doanh nghiệp với mạng lưới Napas 24/7 và hệ sinh thái VietQR. Tiền chuyển khoản từ khách hàng chuyển thẳng vào tài khoản ngân hàng của người bán theo thời gian thực (Zero-fee, Zero-hold).

- Cổng thông tin & Tài liệu: https://payos.vn/docs/api
- Trang quản trị: https://my.payos.vn

## Tài Liệu Tham Khảo Trong `references/`

| Nhu cầu | File tham khảo |
|---|---|
| Đặc tả API v2, Headers, Endpoints (`/v2/payment-requests`) | `references/api.md` |
| Cấu hình Webhook, cấu trúc Payload & Thuật toán Checksum HMAC-SHA256 | `references/webhook.md` |
| Quy trình Checkout (Hosted Link, Embedded Iframe, Return/Cancel URLs) | `references/checkout-flow.md` |
| Bảo mật Checksum Key, mã hóa chữ ký, chống xử lý trùng (Idempotency) | `references/security.md` |

---

## 3 Thông Tin Xác Thực Bắt Buộc (Credentials)

Mỗi kênh thanh toán trên PayOS cung cấp 3 khóa bảo mật tại **Kênh thanh toán → Cài đặt**:
1. `PAYOS_CLIENT_ID`: Định danh ứng dụng / merchant.
2. `PAYOS_API_KEY`: Khóa xác thực gửi trong Header `x-api-key`.
3. `PAYOS_CHECKSUM_KEY`: Khóa bí mật dùng để tạo và xác thực chữ ký HMAC-SHA256 (tuyệt đối không để lộ ở client-side).

---

## Nguyên Tắc Cốt Lõi Khi Tích Hợp PayOS

1. **Chuẩn hóa `orderCode`**:
   - `orderCode` bắt buộc là **số nguyên dương** (`integer`), tối đa 16 chữ số (giới hạn `Number.MAX_SAFE_INTEGER` = 9,007,199,254,740,991).
   - Tuyệt đối không dùng chuỗi ký tự chữ hoặc dấu gạch ngang (ví dụ: `DH-1234` là không hợp lệ; phải dùng dạng số như `20261117001`).

2. **Quy tắc tạo chữ ký (Signature Generation)**:
   - Khi tạo link thanh toán, sắp xếp 5 trường bắt buộc theo thứ tự bảng chữ cái:
     `amount={amount}&cancelUrl={cancelUrl}&description={description}&orderCode={orderCode}&returnUrl={returnUrl}`
   - Ký HMAC-SHA256 với `PAYOS_CHECKSUM_KEY`.

3. **Xác thực Webhook (Webhook Checksum Verification)**:
   - Khi nhận Webhook từ PayOS, bóc tách trường `data` và `signature`.
   - Sắp xếp tất cả các trường trong `data` theo thứ tự chữ cái A-Z (loại trừ `signature`), nối chuỗi dạng `key1=value1&key2=value2...`.
   - Tính mã băm HMAC-SHA256 với `PAYOS_CHECKSUM_KEY` và so sánh hằng thời gian (`hash_equals` / `compare_digest`) với `signature` nhận được.
   - Trả lời HTTP 200 `{"success": true}` ngay lập tức để tránh PayOS thử lại (retry).

4. **Tính Bất Biến & Chống Trùng (Idempotency)**:
   - Lưu trữ `orderCode` và `paymentLinkId` với ràng buộc duy nhất trong cơ sở dữ liệu.
   - Sử dụng câu lệnh Atomic UPDATE:
     ```sql
     UPDATE orders 
     SET status = 'paid', paid_at = NOW() 
     WHERE order_code = ? AND status = 'pending' AND amount <= ?;
     ```
