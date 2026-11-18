# PayOS API v2 Reference

Tài liệu chi tiết các Endpoints chính của PayOS API v2.

- **Base URL:** `https://api-merchant.payos.vn`
- **Headers bắt buộc cho mọi request:**
  ```http
  x-client-id: <PAYOS_CLIENT_ID>
  x-api-key: <PAYOS_API_KEY>
  Content-Type: application/json
  ```

---

## 1. Tạo Link Thanh Toán (`POST /v2/payment-requests`)

Tạo yêu cầu thanh toán mới và nhận URL trang thanh toán chứa mã VietQR động.

### Request Body:
```json
{
  "orderCode": 123456,
  "amount": 50000,
  "description": "Thanh toan don 123456",
  "cancelUrl": "https://shop.example/cancel",
  "returnUrl": "https://shop.example/success",
  "signature": "<HMAC_SHA256_HEX>",
  "items": [
    {
      "name": "Sản phẩm A",
      "quantity": 1,
      "price": 50000
    }
  ],
  "buyerName": "Nguyen Van A",
  "buyerEmail": "buyer@example.com",
  "buyerPhone": "0901234567",
  "buyerAddress": "Hà Nội",
  "expiredAt": 1700000000
}
```

### Các trường quan trọng:
| Trường | Kiểu dữ liệu | Bắt buộc | Ghi chú |
|---|---|:---:|---|
| `orderCode` | Integer | Có | Mã đơn dạng số nguyên dương (≤ 9,007,199,254,740,991) |
| `amount` | Integer | Có | Số tiền bằng VND (không chứa số thập phân) |
| `description` | String | Có | Mô tả chuyển khoản (tối đa 25 ký tự, không dấu / ASCII) |
| `cancelUrl` | String | Có | URL chuyển hướng khi khách bấm Hủy thanh toán |
| `returnUrl` | String | Có | URL chuyển hướng khi khách thanh toán thành công |
| `signature` | String | Có | Chữ ký HMAC-SHA256 của chuỗi 5 tham số sắp xếp A-Z |
| `expiredAt` | Integer | Không | Thời gian hết hạn (Unix timestamp tính bằng giây) |

### Response Thành Công (HTTP 200):
```json
{
  "code": "00",
  "desc": "Success",
  "data": {
    "bin": "970422",
    "accountNumber": "0123456789",
    "accountName": "NGUYEN VAN A",
    "amount": 50000,
    "description": "Thanh toan don 123456",
    "orderCode": 123456,
    "currency": "VND",
    "paymentLinkId": "c7a8b9e0-1234-5678-9abc-def012345678",
    "status": "PENDING",
    "checkoutUrl": "https://pay.payos.vn/web/c7a8b9e0...",
    "qrCode": "00020101021238540010A0000007270124000697042201100123456789..."
  },
  "signature": "<RESPONSE_SIGNATURE>"
}
```

---

## 2. Lấy Thông Tin Link Thanh Toán (`GET /v2/payment-requests/{orderCode}`)

Tra cứu trạng thái của đơn hàng đã tạo theo mã `orderCode`.

### URL:
`GET https://api-merchant.payos.vn/v2/payment-requests/123456`

### Response (HTTP 200):
```json
{
  "code": "00",
  "desc": "Success",
  "data": {
    "id": "c7a8b9e0-1234-5678-9abc-def012345678",
    "orderCode": 123456,
    "amount": 50000,
    "amountPaid": 50000,
    "amountRemaining": 0,
    "status": "PAID",
    "createdAt": "2026-11-17T12:00:00Z",
    "transactions": [
      {
        "reference": "FT261117...",
        "amount": 50000,
        "accountNumber": "0123456789",
        "description": "Thanh toan don 123456",
        "transactionDateTime": "2026-11-17 12:05:00"
      }
    ]
  }
}
```

Trạng thái `status`:
- `PENDING`: Đang chờ thanh toán
- `PROCESSING`: Đang xử lý
- `PAID`: Đã thanh toán thành công
- `CANCELLED`: Đã bị hủy

---

## 3. Hủy Link Thanh Toán (`POST /v2/payment-requests/{orderCode}/cancel`)

### Request Body:
```json
{
  "cancellationReason": "Khách hàng đổi ý / Hết hạn"
}
```

---

## 4. Đăng Ký / Xác Nhận Webhook URL (`POST /v2/payment-requests/invoices/webhook`)

### Request Body:
```json
{
  "webhookUrl": "https://shop.example/api/payos/webhook"
}
```
PayOS sẽ gửi một request kiểm tra đến URL của bạn trước khi lưu cấu hình.
