# Shopee API Integration Skill

**Version:** 1.0.0  
**Author:** Cursor Enterprise Framework  
**Triggers:** shopee, shopee api, shopee seller, shopee integration, e-commerce

## Overview

This skill provides Shopee API integration for Cursor Enterprise Framework. It enables product management, order processing, logistics handling, and analytics for Shopee sellers.

## Capabilities

- **Product Management**: List products, get details, manage inventory
- **Order Management**: List orders, get order details, process orders
- **Logistics**: Get shipping info, manage shipments
- **Shop Info**: Get shop information and settings
- **Analytics**: Get sales data and reports

## Installation

```bash
pip install requests
```

Or use the bundled tool:
```bash
python tools/api_integrations/shopee_integration.py --help
```

## Configuration

### Shopee Partner Setup

1. Register at [Shopee Partners](https://partner.shopeemobile.com/)
2. Create a partner application
3. Get Partner ID and Partner Key
4. Authorization: Get Shop ID through authorization flow

### Environment Variables

```bash
export SHOPEE_PARTNER_ID="your_partner_id"
export SHOPEE_PARTNER_KEY="your_partner_key"
export SHOPEE_SHOP_ID="your_shop_id"
```

## Authentication

### Partner Authorization

1. Generate authorization URL
2. Merchant approves authorization
3. Get Shop ID and Access Token

```python
# Authorization URL format
auth_url = f"https://partner.shopeemobile.com/api/v1/shop/auth/?partner_id={PARTNER_ID}"
```

## Usage

### CLI Tool

```bash
# Get shop info
python tools/api_integrations/shopee_integration.py --partner-id ID --partner-key KEY --shop-id SHOP_ID shop-info

# List products
python tools/api_integrations/shopee_integration.py --partner-id ID --partner-key KEY --shop-id SHOP_ID product-list

# Get product detail
python tools/api_integrations/shopee_integration.py --partner-id ID --partner-key KEY --shop-id SHOP_ID product-detail --product-id 12345

# List orders
python tools/api_integrations/shopee_integration.py --partner-id ID --partner-key KEY --shop-id SHOP_ID order-list --from TIMESTAMP --to TIMESTAMP

# Get order detail
python tools/api_integrations/shopee_integration.py --partner-id ID --partner-key KEY --shop-id SHOP_ID order-detail --order-id 123456

# Get logistics options
python tools/api_integrations/shopee_integration.py --partner-id ID --partner-key KEY --shop-id SHOP_ID logistics

# List orders by status
python tools/api_integrations/shopee_integration.py --partner-id ID --partner-key KEY --shop-id SHOP_ID order-status --status ready_to_ship
```

### Python API

```python
from tools.api_integrations.shopee_integration import ShopeeClient

# Initialize client
client = ShopeeClient(
    partner_id="PARTNER_ID",
    partner_key="PARTNER_KEY",
    shop_id=SHOP_ID
)

# Get shop info
shop = client.get_shop_info()
print(shop)

# List products
products = client.get_product_list(offset=0, page_size=50)
for product in products:
    print(f"{product['product_id']}: {product['product_name']}")

# Get order list
orders = client.get_order_list()
for order in orders:
    print(f"Order {order['order_sn']}: {order['order_status']}")
```

## Product Management

### List Products
```python
# Get first page
products = client.get_product_list(offset=0, page_size=50)

# Paginate
all_products = []
offset = 0
while True:
    products = client.get_product_list(offset=offset, page_size=50)
    if not products:
        break
    all_products.extend(products)
    offset += 50
```

### Get Product Detail
```python
product = client.get_product_detail(product_id=12345)
print(f"Name: {product['product_name']}")
print(f"Price: {product['price']}")
print(f"Stock: {product['stock']}")
```

### Product Status Mapping

| Status Code | Status Name |
|-------------|-------------|
| 1 | Normal |
| 2 | Deleted |
| 3 | Unlisted |

## Order Management

### List Orders
```python
from datetime import datetime, timedelta

# Last 7 days
to_time = int(datetime.now().timestamp())
from_time = int((datetime.now() - timedelta(days=7)).timestamp())

orders = client.get_order_list(
    create_time_from=from_time,
    create_time_to=to_time
)
```

### Order Status Mapping

| Status Code | Status Name | Description |
|-------------|-------------|-------------|
| UNPAID | Unpaid | Awaiting payment |
| READY_TO_SHIP | Ready to Ship | Paid, ready for shipping |
| PROCESSED | Processed | Being prepared |
| SHIPPED | Shipped | In transit |
| COMPLETED | Completed | Delivered |
| CANCELLED | Cancelled | Order cancelled |
| IN_CANCEL | In Cancellation | Cancellation pending |

### Get Order Detail
```python
order = client.get_order_detail(order_id=123456)
print(f"Order SN: {order['order_sn']}")
print(f"Buyer: {order['buyer_username']}")
print(f"Total: {order['total_amount']}")
for item in order.get('items', []):
    print(f"  - {item['product_name']} x {item['quantity']}")
```

## Logistics

### Get Available Logistics
```python
logistics = client.get_logistics()
for log in logistics:
    print(f"{log['logistics_id']}: {log['logistics_name']}")
```

### Get Shipping Parameter
```python
# Get available shipping options for an order
shipping_info = client.get_logistics_info(order_id=123456)
print(shipping_info)
```

### Logistics Status Mapping

| Status Code | Description |
|-------------|-------------|
| 101 | Pending Pickup |
| 102 | Picked Up |
| 103 | In Transit |
| 104 | Delivering |
| 105 | Delivered |
| 106 | Delivery Failed |
| 107 | Returned |
| 108 | Returning |

## Examples

### Order Processing Pipeline
```python
def process_orders(client):
    # Get ready-to-ship orders
    orders = client.get_orders_by_status(order_status="READY_TO_SHIP")
    
    results = []
    for order in orders:
        try:
            # Get order details
            detail = client.get_order_detail(order['order_id'])
            
            # Validate items
            if validate_order(detail):
                # Process shipping
                results.append({
                    'order_id': order['order_id'],
                    'status': 'processed'
                })
            else:
                results.append({
                    'order_id': order['order_id'],
                    'status': 'failed',
                    'reason': 'validation_failed'
                })
        except Exception as e:
            results.append({
                'order_id': order['order_id'],
                'status': 'error',
                'error': str(e)
            })
    
    return results
```

### Product Inventory Sync
```python
def sync_inventory(client, external_inventory):
    """
    Sync inventory from external system to Shopee.
    
    external_inventory: dict of {product_id: quantity}
    """
    products = client.get_product_list(offset=0, page_size=100)
    
    for product in products:
        ext_id = product['product_id']
        if ext_id in external_inventory:
            new_stock = external_inventory[ext_id]
            # Update stock (requires separate API call)
            print(f"Updating {product['product_name']}: {new_stock} units")
```

### Sales Report Generator
```python
def generate_sales_report(client, start_time, end_time):
    orders = client.get_order_list(
        create_time_from=start_time,
        create_time_to=end_time
    )
    
    report = {
        'total_orders': 0,
        'total_revenue': 0,
        'completed_orders': 0,
        'cancelled_orders': 0
    }
    
    for order in orders:
        report['total_orders'] += 1
        report['total_revenue'] += float(order.get('total_amount', 0))
        
        if order['order_status'] == 'COMPLETED':
            report['completed_orders'] += 1
        elif order['order_status'] == 'CANCELLED':
            report['cancelled_orders'] += 1
    
    return report
```

### Auto-Reply for Orders
```python
def notify_buyer(client, order_id, message):
    # Get order detail
    order = client.get_order_detail(order_id)
    
    # Send message via Shopee Chat API (requires separate integration)
    print(f"Notifying buyer {order['buyer_username']}: {message}")
```

## Best Practices

1. **Signature Generation**: Always generate fresh signatures for each request
2. **Timestamp**: Use current timestamp for each request
3. **Pagination**: Handle paginated results properly
4. **Error Handling**: Handle API errors gracefully
5. **Rate Limiting**: Respect Shopee's rate limits

## Troubleshooting

### Signature Error
- Verify Partner Key is correct
- Ensure timestamp is current
- Check signature encoding (UTF-8)

### Authentication Error
- Verify Partner ID and Shop ID
- Check if authorization is still valid
- Ensure timestamp is within acceptable range

### Order Not Found
- Check order ID/Order SN
- Verify order belongs to your shop

## References

- [Shopee Partner API](https://partner.shopeemobile.com/)
- [Shopee API Documentation](https://shopee.github.io/docs/)
- [API Status Codes](https://shopee.github.io/docs/error-codes)

## License

MIT License - See bundled LICENSE file
