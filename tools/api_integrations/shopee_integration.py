#!/usr/bin/env python
"""
Shopee API Integration Tool

Provides Shopee API integration for:
- Product management
- Order management
- Shop information
- Logistics
- Analytics

Usage:
    python shopee_integration.py --partner-id ID --partner-key KEY --shop-id SHOP_ID product list
    python shopee_integration.py --partner-id ID --partner-key KEY --shop-id SHOP_ID order list
"""

import argparse
import hashlib
import hmac
import json
import time
import sys
from dataclasses import dataclass
from typing import Optional, List
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)


@dataclass
class ShopeeConfig:
    """Shopee API configuration."""
    api_base_url: str = "https://partner.shopeemobile.com"
    api_version: str = "v1"


class ShopeeClient:
    """Shopee API client."""
    
    def __init__(self, partner_id: str, partner_key: str, shop_id: int, 
                 config: Optional[ShopeeConfig] = None):
        self.partner_id = partner_id
        self.partner_key = partner_key.encode()
        self.shop_id = shop_id
        self.config = config or ShopeeConfig()
        self.session = requests.Session()
    
    def _generate_signature(self, path: str, post_data: str) -> str:
        """Generate Shopee API signature."""
        message = f"{path}{post_data}"
        return hmac.new(self.partner_key, message.encode(), hashlib.sha256).hexdigest()
    
    def _request(self, endpoint: str, method: str = "POST", params: dict = None, 
                 data: dict = None) -> dict:
        """Make API request."""
        timestamp = int(time.time())
        
        url = f"{self.config.api_base_url}{endpoint}"
        
        request_data = {
            "partner_id": int(self.partner_id),
            "shopid": self.shop_id,
            "timestamp": timestamp,
        }
        if data:
            request_data.update(data)
        
        post_data = json.dumps(request_data)
        path = endpoint
        signature = self._generate_signature(path, post_data)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": signature,
        }
        
        if method == "POST":
            response = self.session.post(url, headers=headers, data=post_data)
        else:
            response = self.session.get(url, headers=headers, params=params)
        
        response.raise_for_status()
        result = response.json()
        
        if result.get("error"):
            raise Exception(f"Shopee API Error: {result.get('error_msg', 'Unknown')}")
        
        return result
    
    def get_shop_info(self) -> dict:
        """Get shop information."""
        return self._request("/api/v1/shop/get")
    
    def get_product_list(self, offset: int = 0, page_size: int = 50) -> List[dict]:
        """Get product list."""
        data = {
            "pagination_offset": offset,
            "pagination_entries_per_page": page_size,
        }
        result = self._request("/api/v1/product/get_list", data=data)
        return result.get("response", {}).get("product", [])
    
    def get_product_detail(self, product_id: int) -> dict:
        """Get product detail."""
        data = {"product_id": product_id}
        return self._request("/api/v1/product/get", data=data)
    
    def get_order_list(self, create_time_from: int = None, create_time_to: int = None,
                       page_size: int = 50) -> List[dict]:
        """Get order list."""
        data = {
            "page_size": page_size,
        }
        if create_time_from:
            data["create_time_from"] = create_time_from
        if create_time_to:
            data["create_time_to"] = create_time_to
        
        result = self._request("/api/v1/orders/get", data=data)
        return result.get("response", {}).get("orders", [])
    
    def get_order_detail(self, order_id: int) -> dict:
        """Get order detail."""
        data = {"order_id": order_id}
        result = self._request("/api/v1/orders/get", data=data)
        return result.get("response", {})
    
    def get_logistics(self) -> List[dict]:
        """Get available logistics."""
        return self._request("/api/v1/logistics/get")
    
    def get_logistics_info(self, order_id: int) -> dict:
        """Get logistics info for order."""
        data = {"order_id": order_id}
        return self._request("/api/v1/logistics/get_shipping_parameter", data=data)
    
    def get_orders_by_status(self, order_status: str = "unpaid", page_size: int = 50) -> List[dict]:
        """Get orders by status."""
        data = {
            "order_status": order_status,
            "page_size": page_size,
        }
        result = self._request("/api/v1/orders/get", data=data)
        return result.get("response", {}).get("orders", [])


def main():
    parser = argparse.ArgumentParser(
        description="Shopee API Integration Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--partner-id", "-p", required=True, help="Shopee Partner ID")
    parser.add_argument("--partner-key", "-k", required=True, help="Shopee Partner Key")
    parser.add_argument("--shop-id", "-s", type=int, required=True, help="Shop ID")
    
    sub = parser.add_subparsers(dest="cmd", help="Commands")
    
    # shop-info
    sub.add_parser("shop-info", help="Get shop information")
    
    # product list
    product_list = sub.add_parser("product-list", help="Get product list")
    product_list.add_argument("--offset", type=int, default=0, help="Offset")
    product_list.add_argument("--page-size", type=int, default=50, help="Page size")
    
    # product-detail
    product_detail = sub.add_parser("product-detail", help="Get product detail")
    product_detail.add_argument("--product-id", type=int, required=True, help="Product ID")
    
    # order list
    order_list = sub.add_parser("order-list", help="Get order list")
    order_list.add_argument("--from", dest="from_time", type=int, help="From timestamp")
    order_list.add_argument("--to", dest="to_time", type=int, help="To timestamp")
    order_list.add_argument("--page-size", type=int, default=50, help="Page size")
    
    # order-detail
    order_detail = sub.add_parser("order-detail", help="Get order detail")
    order_detail.add_argument("--order-id", type=int, required=True, help="Order ID")
    
    # logistics
    sub.add_parser("logistics", help="Get available logistics")
    
    # order-status
    order_status = sub.add_parser("order-status", help="Get orders by status")
    order_status.add_argument("--status", default="unpaid", 
                             choices=["unpaid", "ready_to_ship", "shipped", "completed", "cancelled"],
                             help="Order status")
    order_status.add_argument("--page-size", type=int, default=50, help="Page size")
    
    args = parser.parse_args()
    client = ShopeeClient(args.partner_id, args.partner_key, args.shop_id)
    
    try:
        if args.cmd == "shop-info":
            result = client.get_shop_info()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "product-list":
            result = client.get_product_list(args.offset, args.page_size)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "product-detail":
            result = client.get_product_detail(args.product_id)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "order-list":
            result = client.get_order_list(args.from_time, args.to_time, args.page_size)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "order-detail":
            result = client.get_order_detail(args.order_id)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "logistics":
            result = client.get_logistics()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "order-status":
            result = client.get_orders_by_status(args.status, args.page_size)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        return 0
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
