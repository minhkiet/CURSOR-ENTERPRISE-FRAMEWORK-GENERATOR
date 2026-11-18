# Pay2S Recipient Name Lookup API Reference

Tài liệu chi tiết về API kiểm tra và tra cứu tên chủ tài khoản ngân hàng thụ hưởng qua mạng lưới Napas.

- Tham chiếu chính thức: https://docs.pay2s.vn/get-recipient-name/tai-lieu-ky-thuat.html

---

## 1. Thông Tin Endpoint

- **URL:** `https://api.pay2s.vn/userapi/get-recipient-name`
- **Method:** `POST`
- **Rate Limit:** Tối đa **10 requests / phút** cho mỗi tài khoản.

---

## 2. Cấu Trúc Header

```http
Content-Type: application/json
pay2s-token: <BASE64_SECRET_KEY>
```

> **Lưu ý về `pay2s-token`:**  
> Lấy `SecretKey` từ mục quản lý Web/App trên trang quản trị Pay2S, sau đó mã hóa sang dạng **Base64**.  
> Ví dụ trong Python: `base64.b64encode(secret_key.encode()).decode()`

---

## 3. Cấu Trúc Request Body

```json
{
  "accountNumber": "1234567890",
  "bankCode": "VCB"
}
```

### Tham số:
| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|:---:|---|
| `accountNumber` | String | Có | Số tài khoản ngân hàng cần tra cứu |
| `bankCode` | String | Có | Mã ngân hàng viết tắt (VCB, TCB, MBB, ACB, VPB,...) hoặc mã BIN (9704...) |

---

## 4. Cấu Trúc Response

### Thành công (HTTP 200):
```json
{
  "status": true,
  "messages": "Thành công",
  "data": {
    "accountName": "NGUYEN VAN A"
  }
}
```

### Thất bại (Không tìm thấy / Sai thông tin):
```json
{
  "status": false,
  "messages": "Không tìm thấy thông tin tài khoản hoặc ngân hàng không hỗ trợ"
}
```

---

## 5. Code Mẫu Tra Cứu

### Python
```python
import base64
import requests

def get_recipient_name(account_number: str, bank_code: str, secret_key: str) -> dict:
    url = "https://api.pay2s.vn/userapi/get-recipient-name"
    token = base64.b64encode(secret_key.encode("utf-8")).decode("utf-8")
    
    headers = {
        "Content-Type": "application/json",
        "pay2s-token": token
    }
    body = {
        "accountNumber": account_number,
        "bankCode": bank_code
    }
    
    resp = requests.post(url, json=body, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()
```
