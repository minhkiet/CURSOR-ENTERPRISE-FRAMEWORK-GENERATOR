# Pay2S Integration Architecture & Best Practices

Thiết kế kiến trúc tích hợp hệ thống thanh toán tự động và tra cứu người nhận với Pay2S.

---

## 1. Mô Hình Xử Lý Webhook Ngân Hàng (Tự Động Xác Nhận Đơn)

```
[Khách Hàng]                 [Ngân Hàng / Napas]             [Pay2S]               [Hệ Thống Của Bạn]
     │                                │                         │                           │
     │── 1. Quét VietQR / Chuyển khoản▶│                         │                           │
     │                                │── 2. Biến động số dư ──▶│                           │
     │                                                          │── 3. POST Webhook ───────▶│
     │                                                          │   (Authorization Bearer)  │
     │                                                          │                           │── 4. Kiểm tra Token
     │                                                          │                           │── 5. Kiểm tra Idempotency
     │                                                          │                           │── 6. Atomic UPDATE
     │                                                          │◀─ 7. Trả HTTP 200 OK ─────│
     │                                                              (body: {"success": true})
     │◀── 8. Web/App tự động thông báo đơn đã thanh toán ───────────────────────────────────│
```

---

## 2. Bảng Cơ Sở Dữ Liệu & Chống Race Condition

### Bảng nhật ký Webhook (Idempotency Key):
```sql
CREATE TABLE pay2s_webhook_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    transaction_id BIGINT NOT NULL UNIQUE,       -- ID duy nhất của Pay2S
    transaction_number VARCHAR(64) NULL,         -- Mã giao dịch ngân hàng
    gateway VARCHAR(32) NOT NULL,                -- Ngân hàng nhận (ACB, MBB...)
    account_number VARCHAR(32) NOT NULL,
    amount BIGINT NOT NULL,
    transfer_type VARCHAR(8) NOT NULL,           -- IN / OUT
    content TEXT NOT NULL,
    processed_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Cập Nhật Atomic Cho Đơn Hàng:
```sql
UPDATE orders 
SET status = 'paid', paid_at = NOW() 
WHERE code = ? AND status = 'pending' AND amount <= ?;
```
Nếu `affected_rows == 0`, giao dịch đã được xử lý hoặc số tiền không khớp.

---

## 3. Ứng Dụng Tính Năng Tra Cứu Tên Tài Khoản (`get-recipient-name`)

1. **Rút tiền / Trả thưởng / Hoàn tiền:** Xác minh số tài khoản và tên người nhận khớp với hồ sơ người dùng trước khi duyệt lệnh chuyển khoản ra.
2. **Kiểm tra thông tin chuyển khoản nội bộ:** Xác thực tài khoản đích trong các chức năng nạp/rút ví hoặc thanh toán nội bộ.
3. **Cơ chế Cache:** Do giới hạn 10 request/phút, lưu cache tên tài khoản (Redis/Memcached/DB) trong vòng 24h đối với cùng một cặp `(accountNumber, bankCode)` để tránh chạm rate limit.
