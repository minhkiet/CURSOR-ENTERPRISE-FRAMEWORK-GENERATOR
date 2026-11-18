# PayOS Security & Best Practices

Bộ quy chuẩn an toàn bắt buộc khi tích hợp cổng thanh toán PayOS.

---

## 1. Bảo Vệ Thông Tin Bí Mật (Secrets Management)

- **Biến môi trường:** Lưu trữ `PAYOS_CLIENT_ID`, `PAYOS_API_KEY`, `PAYOS_CHECKSUM_KEY` trong file `.env` hoặc Secret Vault.
- **Client-Side Leakage:** Tuyệt đối không nhúng `PAYOS_API_KEY` hay `PAYOS_CHECKSUM_KEY` vào mã nguồn Frontend (React, Vue, mobile app...). Mọi request tạo payment và xác thực webhook phải chạy hoàn toàn ở Backend.

---

## 2. Phòng Chống Tấn Công Giả Mạo & Trùng Lặp (Idempotency & Replay Attack)

### Ràng buộc cơ sở dữ liệu:
- Cột `order_code` phải là `BIGINT NOT NULL UNIQUE`.
- Cột `payment_link_id` lưu UUID của PayOS trả về (`VARCHAR(64) UNIQUE`).

### Bảng nhật ký Webhook (Webhook Audit Log):
```sql
CREATE TABLE payos_webhook_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_code BIGINT NOT NULL,
    payment_link_id VARCHAR(64) NOT NULL,
    amount BIGINT NOT NULL,
    reference VARCHAR(64) NOT NULL UNIQUE, -- Mã giao dịch ngân hàng
    payload JSON NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Xử lý Atomic UPDATE (Chống Race Condition):
Không thực hiện tuần tự `SELECT` rồi `UPDATE` vì webhook gửi lại hoặc gửi đồng thời có thể gây ghi nhận kép:
```sql
-- ✅ Chuẩn: Atomic UPDATE chỉ áp dụng khi status đang là 'pending'
UPDATE orders 
SET status = 'paid', paid_at = NOW() 
WHERE order_code = ? AND status = 'pending' AND amount <= ?;
```
Nếu `affected_rows == 0`, bỏ qua vì đơn đã được xử lý trước đó.

---

## 3. Xác Thực Chuỗi Dữ Liệu Chuyển Khoản

- Trường `description` tối đa 25 ký tự, chỉ nên chứa mã đơn hàng hoặc ký tự chữ số không dấu (ví dụ: `DH123456`).
- Tuyệt đối không đưa trực tiếp chuỗi `description` hoặc dữ liệu chuyển khoản thô vào câu truy vấn SQL (SQL Injection) hay câu lệnh hệ thống (`eval`, `exec`).
