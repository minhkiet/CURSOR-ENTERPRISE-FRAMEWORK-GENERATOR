# PayOS Checkout Flow & Integration Patterns

PayOS hỗ trợ hai mô hình thanh toán chính:
1. **Hosted Checkout (Trang thanh toán của PayOS):** Chuyển hướng người mua sang URL do PayOS cung cấp (`checkoutUrl`).
2. **Embedded Checkout (Nhúng trực tiếp vào website):** Tích hợp iframe hoặc thư viện `@payos/payos-checkout` ngay trên trang web của người bán.

---

## 1. Mô Hình Hosted Checkout (Khuyên Dùng Cho Khởi Đầu)

```
[Khách Hàng]                 [Merchant Backend]                [PayOS Gateway]
     │                               │                                │
     │── 1. Bấm Thanh toán ─────────▶│                                │
     │                               │── 2. POST /payment-requests ──▶│
     │                               │◀─ 3. Trả checkoutUrl + QR ─────│
     │◀─ 4. Chuyển hướng checkoutUrl─│                                │
     │                                                                │
     │── 5. Mở App Ngân hàng quét VietQR Napas ───────────────────────▶│ (Tiền vào tài khoản thật)
     │                                                                │
     │                               │◀── 6. Bắn Webhook tức thì ─────│
     │                               │─── 7. Trả HTTP 200 OK ────────▶│
     │                                                                │
     │◀─ 8. Chuyển hướng về returnUrl ────────────────────────────────│
```

### Các bước triển khai:
1. **Khách tạo đơn:** Frontend gửi thông tin giỏ hàng lên Backend của bạn.
2. **Tạo yêu cầu thanh toán:** Backend gọi API PayOS `POST /v2/payment-requests` kèm chữ ký `signature`.
3. **Nhận link:** PayOS trả về `checkoutUrl`.
4. **Chuyển hướng:** Backend trả link cho frontend redirect khách hàng sang `checkoutUrl`.
5. **Thanh toán:** Khách quét mã VietQR trên trang PayOS bằng ứng dụng ngân hàng bất kỳ.
6. **Xác nhận thanh toán:**
   - Webhook được PayOS bắn về Backend của bạn.
   - Khi thanh toán xong trên web, PayOS tự động chuyển hướng khách về `returnUrl`.
   - Nếu khách bấm "Hủy", PayOS chuyển hướng về `cancelUrl`.

---

## 2. Mô Hình Embedded Checkout (Nhúng SDK)

Người mua thanh toán mà không rời khỏi website của bạn.

### Cài đặt thư viện Client-side:
```html
<script src="https://pay.payos.vn/web/embed/payos-checkout.js"></script>
```

Hoặc npm:
```bash
npm install @payos/payos-checkout
```

### Kích hoạt Popup/Iframe:
```javascript
const payOSConfig = {
  RETURN_URL: "https://shop.example/success",
  ELEMENT_ID: "payos-checkout-iframe",
  CHECKOUT_URL: checkoutUrlFromBackend,
  onSuccess: (event) => {
    console.log("Thanh toán thành công:", event);
    window.location.href = "/success";
  },
  onCancel: (event) => {
    console.log("Khách hủy thanh toán:", event);
  },
  onExit: (event) => {
    console.log("Đóng cửa sổ thanh toán:", event);
  }
};

const { open, exit } = PayOSCheckout.usePayOS(payOSConfig);
open();
```

---

## 3. Quản Lý Trạng Thái Đơn Hàng (Order States)

```
             ┌───────────┐
             │  PENDING  │ ◄─── Khi tạo payment-request
             └─────┬─────┘
                   │
      ┌────────────┴────────────┐
      ▼                         ▼
┌───────────┐             ┌───────────┐
│   PAID    │             │ CANCELLED │
└───────────┘             └───────────┘
(Nhận Webhook)             (Hết hạn hoặc khách bấm Hủy)
```

- **PENDING:** Đơn hàng vừa tạo, đang chờ thanh toán.
- **PAID:** Đã nhận tiền thành công, Webhook đã xác thực.
- **CANCELLED:** Quá thời gian `expiredAt` hoặc bị hủy chủ động.
