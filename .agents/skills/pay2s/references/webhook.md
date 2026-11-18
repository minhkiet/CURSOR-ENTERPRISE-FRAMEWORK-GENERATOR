# Pay2S Webhook Reference

Tài liệu chi tiết về cơ chế gửi và nhận Webhook biến động số dư từ Pay2S.

- Tham chiếu chính thức: https://docs.pay2s.vn/partner/webhook.html

---

## 1. Cấu Trúc Request Từ Pay2S

Khi phát sinh giao dịch (tiền vào/tiền ra) trên tài khoản ngân hàng liên kết, Pay2S sẽ gửi một HTTP POST request đến Endpoint bạn đã đăng ký:

- **Method:** `POST`
- **Headers:**
  ```http
  Content-Type: application/json
  Authorization: Bearer <YOUR_TOKEN_WEBHOOK>
  ```
- **Body Payload:**
  ```json
  {
    "transactions": [
      {
        "id": 32756283,
        "gateway": "ACB",
        "transactionDate": "2026-10-03 03:43:57",
        "transactionNumber": "24936",
        "accountNumber": "50853767",
        "content": "DOIXU119052 GD 6276MSCBD2PGTNVS 031026-03:43:57",
        "transferType": "IN",
        "transferAmount": 90000,
        "checksum": "37eccdf35d7eaf58fb0ff608be0ebc3e"
      }
    ]
  }
  ```

### Bảng định nghĩa các trường:
| Trường | Kiểu dữ liệu | Mô tả |
|---|---|---|
| `id` | Integer | ID giao dịch duy nhất trên hệ thống Pay2S |
| `gateway` | String | Mã định danh ngân hàng (ACB, VCB, MBB, TCB,...) |
| `transactionDate` | String | Thời gian giao dịch (`YYYY-MM-DD HH:mm:ss`) |
| `transactionNumber`| String | Số tham chiếu hoặc mã giao dịch ngân hàng |
| `accountNumber` | String | Số tài khoản ngân hàng nhận tiền |
| `content` | String | Nội dung chuyển khoản của người gửi |
| `transferType` | String | Loại giao dịch: `IN` (tiền vào) hoặc `OUT` (tiền ra) |
| `transferAmount` | Number | Số tiền giao dịch (VND) |
| `checksum` | String | Mã kiểm tra tính toàn vẹn |

---

## 2. Phản Hồi Bắt Buộc (Response)

Endpoint của bạn **phải trả về mã HTTP 200** với nội dung JSON:
```json
{
  "success": true
}
```

---

## 3. Cơ Chế Thử Lại (Retry Policy)

Nếu Pay2S không nhận được HTTP 200 hoặc body không có `"success": true`:
- Lần đầu: Gửi ngay lập tức.
- Lần 2: Sau 60 giây.
- Lần 3: Sau tiếp 60 giây.
- Lần 4: Sau tiếp 60 giây.
- Lần 5: Sau tiếp 60 giây.
- Lần 6: Sau tiếp 60 giây.
- Sau 6 lần thất bại (tổng cộng hơn 5 phút), hệ thống sẽ ngừng gửi.

> **Khuyến nghị:** Xử lý bất đồng bộ (Background Job / Message Queue) cho các tác vụ tốn thời gian (gửi mail, thông báo telegram...) để endpoint phản hồi trong vòng dưới 2 giây.

---

## 4. Code Mẫu Handler Xác Thực (Node.js & Python)

### Python (FastAPI / Flask)
```python
from fastapi import FastAPI, Request, HTTPException
import hmac

app = FastAPI()
PAY2S_WEBHOOK_TOKEN = "your_secret_token_here"

@app.post("/api/pay2s/webhook")
async def pay2s_webhook(request: Request):
    auth_header = request.headers.get("Authorization", "")
    expected = f"Bearer {PAY2S_WEBHOOK_TOKEN}"
    if not hmac.compare_digest(auth_header, expected):
        raise HTTPException(status_code=401, detail="Unauthorized")

    payload = await request.json()
    transactions = payload.get("transactions", [])

    for tx in transactions:
        if tx.get("transferType") == "IN":
            tx_id = tx.get("id")
            amount = tx.get("transferAmount")
            content = tx.get("content", "")
            # TODO: Xử lý idempotent và khớp mã đơn hàng trong content

    return {"success": True}
```

### Node.js (Express)
```javascript
const express = require('express');
const app = express();
app.use(express.json());

const PAY2S_WEBHOOK_TOKEN = process.env.PAY2S_WEBHOOK_TOKEN;

app.post('/api/pay2s/webhook', (req, res) => {
  const authHeader = req.headers['authorization'];
  if (authHeader !== `Bearer ${PAY2S_WEBHOOK_TOKEN}`) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const { transactions } = req.body;
  if (Array.isArray(transactions)) {
    for (const tx of transactions) {
      if (tx.transferType === 'IN') {
        // Xử lý đơn hàng
      }
    }
  }

  return res.status(200).json({ success: true });
});
```
