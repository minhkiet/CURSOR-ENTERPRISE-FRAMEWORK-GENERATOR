# PayOS Webhook Guide & Checksum Verification

Webhook là cơ chế để PayOS thông báo tức thời cho hệ thống của bạn ngay khi giao dịch chuyển khoản ngân hàng thành công qua mạng lưới Napas.

---

## 1. Cấu Trúc Payload Webhook

Khi thanh toán hoàn tất, PayOS sẽ gửi một request `POST` với định dạng JSON:

```json
{
  "code": "00",
  "desc": "success",
  "data": {
    "orderCode": 123456,
    "amount": 50000,
    "description": "Thanh toan don 123456",
    "accountNumber": "0123456789",
    "reference": "FT261117...",
    "transactionDateTime": "2026-11-17 19:30:00",
    "currency": "VND",
    "paymentLinkId": "c7a8b9e0-1234-5678-9abc-def012345678",
    "code": "00",
    "desc": "success",
    "counterAccountBankId": "970415",
    "counterAccountBankName": "VietinBank",
    "counterAccountName": "TRAN VAN B",
    "counterAccountNumber": "1012345678",
    "virtualAccountName": null,
    "virtualAccountNumber": null
  },
  "signature": "d41d8cd98f00b204e9800998ecf8427e..."
}
```

---

## 2. Quy Trình Xác Thực Chữ Ký (Checksum Verification Algorithm)

Để đảm bảo webhook xuất phát từ chính PayOS mà không bị kẻ xấu giả mạo hoặc thay đổi giá trị:

1. **Lấy đối tượng `data`** từ payload webhook.
2. **Sắp xếp tất cả các trường (keys)** trong `data` theo thứ tự alphabet (A-Z).
3. **Nối chuỗi dữ liệu (query string)**:
   - Các trường có giá trị `null` hoặc chuỗi rỗng: chuyển thành chuỗi rỗng `""` hoặc bỏ qua tùy theo phiên bản SDK (khuyến nghị chuẩn SDK: giữ nguyên giá trị chuỗi rỗng).
   - Ghép thành chuỗi dạng `key1=value1&key2=value2...`.
4. **Băm HMAC-SHA256**:
   - Dùng `PAYOS_CHECKSUM_KEY` làm secret key.
   - Băm chuỗi đã nối thành chuỗi hex digest.
5. **So sánh hằng thời gian**:
   - So sánh chuỗi vừa băm với `payload["signature"]`. Nếu khớp tuyệt đối, webhook hợp lệ.

---

## 3. Code Mẫu Xác Thực Webhook Đa Ngôn Ngữ

### Python
```python
import hmac
import hashlib

def verify_payos_webhook(payload: dict, checksum_key: str) -> bool:
    data = payload.get("data", {})
    signature = payload.get("signature", "")
    if not data or not signature:
        return False

    # 1. Sắp xếp các keys theo thứ tự alphabet
    sorted_items = sorted(data.items(), key=lambda x: x[0])
    
    # 2. Tạo chuỗi key1=value1&key2=value2...
    data_parts = []
    for k, v in sorted_items:
        val_str = "" if v is None else str(v)
        data_parts.append(f"{k}={val_str}")
    data_str = "&".join(data_parts)

    # 3. Tính HMAC-SHA256
    calculated_sig = hmac.new(
        checksum_key.encode("utf-8"),
        data_str.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    # 4. So sánh an toàn
    return hmac.compare_digest(calculated_sig, signature)
```

### Node.js / TypeScript
```typescript
import crypto from 'crypto';

export function verifyPayOSWebhook(payload: any, checksumKey: string): boolean {
  const { data, signature } = payload;
  if (!data || !signature) return false;

  // Sắp xếp keys A-Z
  const sortedKeys = Object.keys(data).sort();
  const dataStr = sortedKeys
    .map(key => `${key}=${data[key] === null || data[key] === undefined ? '' : data[key]}`)
    .join('&');

  const calculatedSig = crypto
    .createHmac('sha256', checksumKey)
    .update(dataStr)
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(calculatedSig, 'hex'),
    Buffer.from(signature, 'hex')
  );
}
```

### PHP
```php
function verifyPayOSWebhook(array $payload, string $checksumKey): bool {
    $data = $payload['data'] ?? [];
    $signature = $payload['signature'] ?? '';
    if (empty($data) || empty($signature)) return false;

    ksort($data);
    $parts = [];
    foreach ($data as $key => $value) {
        $valStr = is_null($value) ? '' : (string)$value;
        $parts[] = "{$key}={$valStr}";
    }
    $dataStr = implode('&', $parts);

    $calculatedSig = hash_hmac('sha256', $dataStr, $checksumKey);
    return hash_equals($calculatedSig, $signature);
}
```

---

## 4. Xử Lý Phản Hồi Webhook

- Ngay khi nhận được webhook và xác thực signature thành công:
  - Cập nhật trạng thái đơn hàng trong DB.
  - Trả về mã HTTP `200 OK` với body `{"success": true}` ngay lập tức.
- Không để các tác vụ nặng (gửi email, gọi API bên thứ ba...) chặn luồng phản hồi webhook (sử dụng Background Queue/Job).
