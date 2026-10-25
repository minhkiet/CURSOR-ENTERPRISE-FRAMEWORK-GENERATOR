# Zalo API Integration Skill

> **Version:** 1.0.0  
> **Platform:** Zalo Official Account (OA) API  
> **Use case:** Vietnamese chat, OA management, Mini App development

## Overview

Zalo là nền tảng messaging phổ biến nhất tại Việt Nam với 100M+ người dùng. Skill này cung cấp integration với Zalo API để gửi message, quản lý OA, và phát triển Zalo Mini App.

## API Capabilities

### 1. Zalo OA API (Official Account)

| Feature | Endpoint | Description |
|----------|----------|-------------|
| Send Message | `/v2.0/me/sendmsg` | Gửi text, image, link, template |
| Get User Profile | `/v2.0/me` | Lấy thông tin user (name, picture) |
| Get Followers | `/v2.0/me/followers` | Danh sách người theo dõi |
| Create Menu | `/v2.0/me/createMenu` | Tạo menu cho OA |
| Upload File | `/v2.0/me/upload` | Upload media files |

### 2. Zalo Mini App (ZaUI)

Zalo Mini App là web app chạy trong Zalo super-app. Sử dụng ZaUI components và JavaScript APIs.

**Components:**
- `Button`, `Input`, `Textarea`, `Select`
- `Modal`, `Dialog`, `Drawer`
- `Tabs`, `Accordion`
- `Avatar`, `Badge`, `Tag`
- `Card`, `List`, `Swiper`

**JavaScript APIs:**
```javascript
// Authorization
zaapi.authorize({ appId: 'your_app_id' })
zaapi.getUserInfo()  // { userId, name, avatar, gender }
zaapi.getPhoneNumber()  // Requires user permission

// Storage
zaapi.setStorage({ key: 'cart', data: [...] })
zaapi.getStorage({ key: 'cart' })

// UI
zaapi.showToast({ message: 'Success!' })
zaapi.showLoading()
zaapi.hideLoading()
zaapi.scanQRCode()
```

## Quick Start

### 1. Setup Zalo OA

```bash
# 1. Đăng ký Zalo Official Account tại
# https://oa.zalo.me

# 2. Lấy credentials từ Zalo Official Account Dashboard
# - App ID
# - App Secret
# - Access Token
```

### 2. Python Integration

```python
from tools.api_integrations.zalo_integration import ZaloClient

client = ZaloClient(access_token="YOUR_ACCESS_TOKEN")

# Get user profile
profile = client.get_user_profile("user_id")
print(profile)  # { id, name, picture }

# Send message
client.send_message("user_id", "Xin chào! 👋")

# Send image
client.send_image("user_id", "https://example.com/image.jpg", "Caption here")

# Send rich link
client.send_link("user_id", "https://shopee.vn/product", "Mua sắm", "Giảm giá 50%")
```

### 3. CLI Usage

```bash
# Send message
python tools/api_integrations/zalo_integration.py send --token TOKEN --uid UID --message "Hello"

# Get profile
python tools/api_integrations/zalo_integration.py profile --token TOKEN --uid UID

# Send image
python tools/api_integrations/zalo_integration.py send-image --token TOKEN --uid UID --image URL

# Get followers
python tools/api_integrations/zalo_integration.py followers --token TOKEN
```

## Best Practices

### 1. Message Content

```python
# ✅ Good: Clear, actionable message
client.send_message(uid, "Đơn hàng #12345 của bạn đã được giao thành công! 📦")

# ✅ Good: With quick action
client.send_link(uid, "https://shop.example/orders/12345", "Xem chi tiết", "Theo dõi đơn hàng")

# ❌ Bad: Generic message
client.send_message(uid, "Cảm ơn đã mua sắm")
```

### 2. Error Handling

```python
from tools.api_integrations.zalo_integration import ZaloClient

client = ZaloClient(access_token="TOKEN")

try:
    result = client.send_message("user_id", "Hello")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 400:
        print("Invalid recipient or message format")
    elif e.response.status_code == 401:
        print("Token expired, refresh needed")
    elif e.response.status_code == 429:
        print("Rate limit exceeded, implement backoff")
    else:
        print(f"API Error: {e}")
```

### 3. Rate Limiting

Zalo có rate limit cho message sending. Implement exponential backoff:

```python
import time
import requests

def send_with_retry(client, uid, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.send_message(uid, message)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

## Integration with Cursor Framework

### Slash Command

Use `/zalo` command in Cursor to trigger Zalo integration:

```
/zalo send "user_id" "Hello from Cursor!"
```

### Workflow

```yaml
# .cursor/workflows/zalo-notification.yaml
name: Zalo Order Notification
trigger:
  type: webhook
  source: order-service

steps:
  - name: Get order details
    action: database.query
    query: "SELECT * FROM orders WHERE id = :order_id"
    
  - name: Send notification
    action: zalo.send_message
    params:
      template: "order_confirmed"
      data:
        order_id: "{{ order.id }}"
        status: "{{ order.status }}"
```

## Security

### Token Management

```python
import os

# Environment variable (recommended)
token = os.environ.get("ZALO_ACCESS_TOKEN")

# Or use cursor-memory for secure storage
from tools.cursor_memory import secure_store
secure_store("zalo_token", token)
```

### Webhook Verification

```python
import hmac
import hashlib

def verify_zalo_webhook(request, app_secret):
    """Verify webhook signature from Zalo."""
    data = request.get_data()
    signature = request.headers.get("X-Zalo-Signature")
    
    expected = hmac.new(
        app_secret.encode(),
        data,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected)
```

## References

- [Zalo Official API Docs](https://developers.zalo.me/docs/)
- [Zalo Mini App SDK](https://mini-app.zalo.me/docs/)
- [ZaUI Components](https://developers.zalo.me/docs/mini-app/ui/zaui-overview)
- [Zalo Payment (ZaloPay)](./sec_vietnam-payment-review.md)
