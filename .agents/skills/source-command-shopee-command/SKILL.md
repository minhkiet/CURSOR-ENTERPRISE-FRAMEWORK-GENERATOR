# Shopee API Integration Skill

> **Version:** 1.0.0  
> **Platform:** Shopee Open Platform API  
> **Use case:** E-commerce automation, order management, product listing

## Overview

Shopee là sàn thương mại điện tử lớn nhất Đông Nam Á. Skill này cung cấp integration với Shopee Open Platform API để quản lý sản phẩm, đơn hàng, và analytics.

## API Capabilities

### 1. Product Management

| Feature | Endpoint | Description |
|---------|----------|-------------|
| Add Item | `/api/v2/product/add_item` | Tạo sản phẩm mới |
| Update Item | `/api/v2/product/update_item` | Cập nhật sản phẩm |
| Delete Item | `/api/v2/product/delete_item` | Xóa sản phẩm |
| Get Item Detail | `/api/v2/product/get_item_detail` | Lấy chi tiết sản phẩm |
| List Items | `/api/v2/product/get_items_list` | Danh sách sản phẩm |
| Update Stock | `/api/v2/product/update_stock` | Cập nhật tồn kho |
| Update Price | `/api/v2/product/update_price` | Cập nhật giá |

### 2. Order Management

| Feature | Endpoint | Description |
|---------|----------|-------------|
| Get Orders | `/api/v2/order/get_orders` | Lấy danh sách đơn hàng |
| Get Order Detail | `/api/v2/order/get_order_detail` | Chi tiết đơn hàng |
| Cancel Order | `/api/v2/order/cancel_order` | Hủy đơn hàng |
| Handle RTS | `/api/v2/logistics/rts` | Ready to ship |
| Get Tracking | `/api/v2/logistics/get_tracking` | Theo dõi vận chuyển |

### 3. Finance

| Feature | Endpoint | Description |
|---------|----------|-------------|
| Get Balance | `/api/v2/finance/get_balance` | Số dư tài khoản |
| Get Orders Period | `/api/v2/finance/get_orders_period` | Doanh thu theo kỳ |
| Withdraw | `/api/v2/finance/withdraw` | Rút tiền |

### 4. Shop Information

| Feature | Endpoint | Description |
|---------|----------|-------------|
| Get Profile | `/api/v2/shop/get_profile` | Thông tin shop |
| Get Performance | `/api/v2/shop/get_performance` | Metrics shop |

## Quick Start

### 1. Setup Shopee Partner

1. Register at [Shopee Partner Portal](https://partner.shopeemobile.com)
2. Create application to get Partner ID and Partner Key
3. Get Shop ID from your Shopee shop

### 2. Python Integration

```python
from tools.api_integrations.shopee_integration import ShopeeClient

# Initialize client
client = ShopeeClient(
    partner_id=123456,
    partner_key="PARTNER_KEY",
    shop_id=789012
)

# Get shop profile
shop = client.get_profile()
print(f"Shop: {shop['shop_name']}")
print(f"Status: {shop['status']}")

# Get products
products = client.get_items_list()
for item in products['items']:
    print(f"- {item['item_name']}: {item['price']}")

# Get orders
orders = client.get_orders(
    create_time_from=1704067200,  # 2024-01-01
    create_time_to=1706745600     # 2024-02-01
)
for order in orders['orders']:
    print(f"Order {order['order_sn']}: {order['order_status']}")
```

## Product Management

### 1. Create Product

```python
# Create new product
item = client.add_item(
    item_name="Áo Polo nam cao cấp",
    description="Chất liệu cotton 100%, thoáng mát",
    price=299000,
    stock=100,
    category_id=11000547,  # Fashion > Men > Tops > Polo
    images=["https://example.com/photo1.jpg"],
    attributes=[
        {"attributes_id": 100009, "value": "M"},  # Size
        {"attributes_id": 100010, "value": "Xanh navy"}  # Color
    ],
    weight=0.3,  # kg
    dimension={
        "package_length": 30,
        "package_width": 20,
        "package_height": 5
    }
)
print(f"Created item ID: {item['item_id']}")
```

### 2. Update Product

```python
# Update price
client.update_price(
    item_id="12345678",
    price=249000
)

# Update stock
client.update_stock(
    item_id="12345678",
    stock=50
)

# Update full item
client.update_item(
    item_id="12345678",
    item_name="Áo Polo nam cao cấp - 2024",
    description="Updated description",
    price=279000
)
```

### 3. Product Attributes

```python
# Get category attributes
attrs = client.get_category_attributes(category_id=11000547)
for attr in attrs['attributes']:
    print(f"{attr['attributes_id']}: {attr['attributes_name']}")
    for val in attr.get('options', []):
        print(f"  - {val}")
```

## Order Management

### 1. Order Lifecycle

```
1. UNPAID        → Buyer chưa thanh toán
2. READY_TO_SHIP → Buyer đã thanh toán, chờ gửi hàng
3. SHIPPING      → Đang vận chuyển
4. COMPLETED     → Giao hàng thành công
5. CANCELLED     → Đơn bị hủy
6. IN_CANCEL     → Đang xử lý hủy
7. Returns       → Yêu cầu trả hàng
```

### 2. Get Orders with Filters

```python
from datetime import datetime, timedelta

# Last 7 days
end_time = int(datetime.now().timestamp())
start_time = int((datetime.now() - timedelta(days=7)).timestamp())

# Get unpaid orders
orders = client.get_orders(
    order_status="UNPAID",
    create_time_from=start_time,
    create_time_to=end_time,
    page_size=50
)

# Get ready-to-ship orders
rts_orders = client.get_orders(
    order_status="READY_TO_SHIP",
    create_time_from=start_time,
    create_time_to=end_time
)
```

### 3. Handle Ready-to-Ship

```python
# Get order details with logistics info
order_detail = client.get_order_detail(order_sn="240115ABC123")

# Get available shipping methods
logistics = client.get_logistics(order_sn="240115ABC123")
for log in logistics['logistics']:
    print(f"- {log['logistics_name']}: {log['fee']}")

# Mark as Ready to Ship with tracking
client.rts(
    order_sn="240115ABC123",
    logistics_id=70021,  # GHN
    tracking_no="TRACK123456"
)
```

### 4. Order Details

```python
# Get detailed order info
detail = client.get_order_detail(order_sn="240115ABC123")

print(f"Order: {detail['order_sn']}")
print(f"Status: {detail['order_status']}")
print(f"Total: {detail['total_amount']} VND")
print(f"Buyer: {detail['buyer_username']}")

# Items
for item in detail['items']:
    print(f"  - {item['item_name']} x{item['quantity']} = {item['item_price']}")

# Shipping address
addr = detail['address_shipping']
print(f"Ship to: {addr['full_address']}")
```

## Integration Examples

### 1. Auto-Invoice Generation

```python
from datetime import datetime

def generate_order_invoice(order_sn):
    """Generate invoice for Shopee order."""
    detail = client.get_order_detail(order_sn)
    
    invoice = {
        "invoice_number": f"INV-{detail['order_sn']}",
        "date": datetime.fromtimestamp(detail['create_time']).strftime("%Y-%m-%d"),
        "buyer": {
            "name": detail['buyer_username'],
            "address": detail['address_shipping']['full_address'],
            "phone": detail['address_shipping']['phone']
        },
        "items": [],
        "subtotal": 0
    }
    
    for item in detail['items']:
        line_total = item['item_price'] * item['quantity']
        invoice['items'].append({
            "sku": item['item_sku'],
            "name": item['item_name'],
            "qty": item['quantity'],
            "price": item['item_price'],
            "total": line_total
        })
        invoice['subtotal'] += line_total
    
    invoice['shipping_fee'] = detail['actual_shipping_fee']
    invoice['total'] = detail['total_amount']
    
    return invoice
```

### 2. Stock Sync

```python
def sync_shopee_stock(erp_products):
    """Sync stock from ERP to Shopee."""
    results = {"updated": 0, "failed": []}
    
    for erp_item in erp_products:
        try:
            # Find Shopee item by SKU
            shopee_items = client.get_items_list(
                item_status="NORMAL",
                update_time_from=int((datetime.now() - timedelta(days=7)).timestamp())
            )
            
            matched = [i for i in shopee_items['items'] 
                      if i.get('item_sku') == erp_item['sku']]
            
            if matched:
                client.update_stock(
                    item_id=matched[0]['item_id'],
                    stock=erp_item['stock']
                )
                results['updated'] += 1
            else:
                results['failed'].append(erp_item['sku'])
                
        except Exception as e:
            results['failed'].append(f"{erp_item['sku']}: {str(e)}")
    
    return results
```

### 3. Sales Report

```python
from collections import defaultdict
from datetime import datetime, timedelta

def generate_sales_report(month: int, year: int):
    """Generate monthly sales report."""
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)
    
    orders = client.get_orders(
        create_time_from=int(start.timestamp()),
        create_time_to=int(end.timestamp()),
        order_status="COMPLETED",
        page_size=100
    )
    
    report = {
        "period": f"{month}/{year}",
        "total_orders": 0,
        "total_revenue": 0,
        "total_items": 0,
        "products": defaultdict(lambda: {"qty": 0, "revenue": 0})
    }
    
    for order in orders['orders']:
        detail = client.get_order_detail(order['order_sn'])
        report['total_orders'] += 1
        report['total_revenue'] += detail['total_amount']
        
        for item in detail['items']:
            sku = item.get('item_sku', 'N/A')
            qty = item['quantity']
            revenue = item['item_price'] * qty
            
            report['products'][sku]['qty'] += qty
            report['products'][sku]['revenue'] += revenue
            report['products'][sku]['name'] = item['item_name']
            report['total_items'] += qty
    
    return report
```

## Webhook Integration

### Flask Webhook Server

```python
from flask import Flask, request, jsonify
from tools.api_integrations.shopee_integration import ShopeeClient
import os
import hmac
import hashlib

app = Flask(__name__)
client = ShopeeClient(
    partner_id=int(os.environ["PARTNER_ID"]),
    partner_key=os.environ["PARTNER_KEY"],
    shop_id=int(os.environ["SHOP_ID"])
)

@app.route("/webhook/shopee", methods=["GET"])
def verify_webhook():
    """Webhook verification."""
    if client.verify_webhook(request):
        return request.args.get("challenge"), 200
    return "Verification failed", 403

@app.route("/webhook/shopee", methods=["POST"])
def receive_update():
    """Handle Shopee webhook."""
    data = request.get_json()
    
    order_sn = data.get("order_sn")
    order_status = data.get("order_status")
    
    if order_status == "READY_TO_SHIP":
        # Send notification
        send_rts_notification(order_sn)
    
    elif order_status == "COMPLETED":
        # Request review
        request_review(order_sn)
    
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(port=5000)
```

## Best Practices

### 1. Error Handling

```python
from tools.api_integrations.shopee_integration import ShopeeClient

client = ShopeeClient(partner_id=123, partner_key="key", shop_id=456)

try:
    result = client.get_orders()
except shopee_integration.ShopeeAPIError as e:
    if e.code == 1001:  # INVALID_PARAM
        print(f"Invalid parameters: {e.message}")
    elif e.code == 1002:  # AUTH_FAILED
        print("Authentication failed")
    elif e.code == 1003:  # SHOP_NOT_FOUND
        print("Shop not found")
    elif e.code == 500:  # SYSTEM_ERROR
        print("Shopee system error, retry later")
```

### 2. Rate Limiting

Shopee API limits:
- 5000 requests/minute per shop
- 10 requests/second per endpoint

```python
import time

def call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except shopee_integration.ShopeeAPIError as e:
            if e.code == 429:  # Rate limit
                time.sleep(1 * (attempt + 1))  # Backoff
            else:
                raise
    raise Exception("Max retries exceeded")
```

### 3. Signature Generation

```python
import hmac
import hashlib

def generate_signature(path, partner_key, timestamp):
    """Generate Shopee API signature."""
    message = f"{path}{timestamp}{partner_key}"
    return hmac.new(
        partner_key.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
```

## Integration with Cursor Framework

### Slash Commands

```
/shopee products
/shopee orders --status READY_TO_SHIP
/shopee order "240115ABC123"
/shopee stock "12345678" 100
/shopee price "12345678" 249000
```

### Workflow Example

```yaml
# .cursor/workflows/shopee-rts.yaml
name: Auto RTS Notification
trigger:
  type: webhook
  source: shopee-webhook

steps:
  - name: Get order details
    action: shopee.get_order_detail
    output: order

  - name: Format message
    action: template.render
    template: |
      📦 Đơn hàng mới cần xử lý!
      
      Mã: {{ order.order_sn }}
      Khách: {{ order.buyer_username }}
      Tổng: {{ order.total_amount | currency }}

  - name: Send to team
    action: telegram.send_message
    params:
      chat_id: "{{ secrets.telegram_shop_channel }}"
      text: "{{ message }}"
```

## References

- [Shopee Partner Portal](https://partner.shopeemobile.com)
- [Shopee Open Platform API Docs](https://open.shopee.com/documents)
- [Shopee Developer Blog](https://developer.shopee.com/)
- [Shopee Academy](https://seller.shopee.vn/edu)
