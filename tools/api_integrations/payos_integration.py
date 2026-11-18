#!/usr/bin/env python
"""
PayOS API Integration Tool

Provides PayOS (Vietnam Open Banking & VietQR Gateway) integration for:
- Creating payment requests with HMAC-SHA256 signature
- Getting payment request details
- Cancelling payment links
- Webhook signature / checksum verification
- Registering / confirming webhook URLs

Usage:
    python payos_integration.py create --order-code 123456 --amount 50000 --desc "Order 123" --return-url "https://shop.example/success" --cancel-url "https://shop.example/cancel"
    python payos_integration.py info --order-code 123456
    python payos_integration.py cancel --order-code 123456 --reason "Customer cancelled"
    python payos_integration.py verify-webhook --data-json '{"orderCode": 123456, ...}' --signature "hex..."
"""

import argparse
import hashlib
import hmac
import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)


@dataclass
class PayOSConfig:
    """PayOS API configuration."""
    client_id: str
    api_key: str
    checksum_key: str
    base_url: str = "https://api-merchant.payos.vn"


class PayOSClient:
    """Client for PayOS API v2."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        api_key: Optional[str] = None,
        checksum_key: Optional[str] = None
    ):
        cid = client_id or os.environ.get("PAYOS_CLIENT_ID", "")
        ak = api_key or os.environ.get("PAYOS_API_KEY", "")
        ck = checksum_key or os.environ.get("PAYOS_CHECKSUM_KEY", "")

        self.config = PayOSConfig(client_id=cid, api_key=ak, checksum_key=ck)
        self.session = requests.Session()
        self.session.headers.update({
            "x-client-id": self.config.client_id,
            "x-api-key": self.config.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    @staticmethod
    def generate_request_signature(
        amount: int,
        cancel_url: str,
        description: str,
        order_code: int,
        return_url: str,
        checksum_key: str
    ) -> str:
        """
        Generate HMAC-SHA256 signature for payment request creation.
        Sorted keys: amount, cancelUrl, description, orderCode, returnUrl.
        """
        data_str = (
            f"amount={amount}&"
            f"cancelUrl={cancel_url}&"
            f"description={description}&"
            f"orderCode={order_code}&"
            f"returnUrl={return_url}"
        )
        return hmac.new(
            checksum_key.encode("utf-8"),
            data_str.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    @staticmethod
    def verify_webhook_data(data: Dict[str, Any], signature: str, checksum_key: str) -> bool:
        """
        Verify incoming webhook signature against data object.
        """
        if not data or not signature or not checksum_key:
            return False

        # Sort all keys alphabetically
        sorted_keys = sorted(data.keys())
        parts = []
        for k in sorted_keys:
            val = data[k]
            val_str = "" if val is None else str(val)
            parts.append(f"{k}={val_str}")
        data_str = "&".join(parts)

        expected_sig = hmac.new(
            checksum_key.encode("utf-8"),
            data_str.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_sig, signature)

    def create_payment_link(
        self,
        order_code: int,
        amount: int,
        description: str,
        cancel_url: str,
        return_url: str,
        items: Optional[List[Dict[str, Any]]] = None,
        buyer_name: Optional[str] = None,
        buyer_email: Optional[str] = None,
        buyer_phone: Optional[str] = None,
        expired_at: Optional[int] = None
    ) -> Dict[str, Any]:
        """Create payment request on PayOS."""
        sig = self.generate_request_signature(
            amount=amount,
            cancel_url=cancel_url,
            description=description,
            order_code=order_code,
            return_url=return_url,
            checksum_key=self.config.checksum_key
        )

        body: Dict[str, Any] = {
            "orderCode": order_code,
            "amount": amount,
            "description": description,
            "cancelUrl": cancel_url,
            "returnUrl": return_url,
            "signature": sig
        }

        if items:
            body["items"] = items
        if buyer_name:
            body["buyerName"] = buyer_name
        if buyer_email:
            body["buyerEmail"] = buyer_email
        if buyer_phone:
            body["buyerPhone"] = buyer_phone
        if expired_at:
            body["expiredAt"] = expired_at

        url = f"{self.config.base_url}/v2/payment-requests"
        resp = self.session.post(url, json=body, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def get_payment_info(self, order_code: int) -> Dict[str, Any]:
        """Get detail of an existing payment link."""
        url = f"{self.config.base_url}/v2/payment-requests/{order_code}"
        resp = self.session.get(url, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def cancel_payment_link(self, order_code: int, cancellation_reason: str = "") -> Dict[str, Any]:
        """Cancel a pending payment request."""
        url = f"{self.config.base_url}/v2/payment-requests/{order_code}/cancel"
        body = {"cancellationReason": cancellation_reason}
        resp = self.session.post(url, json=body, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def confirm_webhook(self, webhook_url: str) -> Dict[str, Any]:
        """Register / confirm webhook URL with PayOS."""
        url = f"{self.config.base_url}/v2/payment-requests/invoices/webhook"
        body = {"webhookUrl": webhook_url}
        resp = self.session.post(url, json=body, timeout=15)
        resp.raise_for_status()
        return resp.json()


def main():
    parser = argparse.ArgumentParser(description="PayOS Integration CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create payment link
    create_parser = subparsers.add_parser("create", help="Create a payment request")
    create_parser.add_argument("--order-code", type=int, required=True, help="Numeric Order Code")
    create_parser.add_argument("--amount", type=int, required=True, help="Amount in VND")
    create_parser.add_argument("--desc", required=True, help="Transfer description (max 25 chars)")
    create_parser.add_argument("--return-url", required=True, help="Return URL")
    create_parser.add_argument("--cancel-url", required=True, help="Cancel URL")
    create_parser.add_argument("--client-id", default=os.environ.get("PAYOS_CLIENT_ID"))
    create_parser.add_argument("--api-key", default=os.environ.get("PAYOS_API_KEY"))
    create_parser.add_argument("--checksum-key", default=os.environ.get("PAYOS_CHECKSUM_KEY"))

    # Payment info
    info_parser = subparsers.add_parser("info", help="Get payment request detail")
    info_parser.add_argument("--order-code", type=int, required=True, help="Order Code")
    info_parser.add_argument("--client-id", default=os.environ.get("PAYOS_CLIENT_ID"))
    info_parser.add_argument("--api-key", default=os.environ.get("PAYOS_API_KEY"))
    info_parser.add_argument("--checksum-key", default=os.environ.get("PAYOS_CHECKSUM_KEY"))

    # Cancel payment
    cancel_parser = subparsers.add_parser("cancel", help="Cancel payment request")
    cancel_parser.add_argument("--order-code", type=int, required=True, help="Order Code")
    cancel_parser.add_argument("--reason", default="", help="Cancellation reason")
    cancel_parser.add_argument("--client-id", default=os.environ.get("PAYOS_CLIENT_ID"))
    cancel_parser.add_argument("--api-key", default=os.environ.get("PAYOS_API_KEY"))
    cancel_parser.add_argument("--checksum-key", default=os.environ.get("PAYOS_CHECKSUM_KEY"))

    # Verify webhook
    verify_parser = subparsers.add_parser("verify-webhook", help="Verify webhook signature")
    verify_parser.add_argument("--data-json", required=True, help="Webhook data JSON string")
    verify_parser.add_argument("--signature", required=True, help="Signature from payload")
    verify_parser.add_argument("--checksum-key", default=os.environ.get("PAYOS_CHECKSUM_KEY"))

    # Confirm webhook
    wh_parser = subparsers.add_parser("confirm-webhook", help="Register webhook URL")
    wh_parser.add_argument("--url", required=True, help="Webhook URL to register")
    wh_parser.add_argument("--client-id", default=os.environ.get("PAYOS_CLIENT_ID"))
    wh_parser.add_argument("--api-key", default=os.environ.get("PAYOS_API_KEY"))
    wh_parser.add_argument("--checksum-key", default=os.environ.get("PAYOS_CHECKSUM_KEY"))

    args = parser.parse_args()

    if args.command == "verify-webhook":
        ck = args.checksum_key
        if not ck:
            print("ERROR: Checksum key required (--checksum-key or PAYOS_CHECKSUM_KEY).", file=sys.stderr)
            sys.exit(1)
        try:
            data = json.loads(args.data_json)
        except Exception as e:
            print(f"ERROR: Invalid data JSON: {e}", file=sys.stderr)
            sys.exit(1)
        valid = PayOSClient.verify_webhook_data(data=data, signature=args.signature, checksum_key=ck)
        print(json.dumps({"valid": valid}))
        sys.exit(0 if valid else 1)

    # API calls require credentials
    client = PayOSClient(
        client_id=args.client_id,
        api_key=args.api_key,
        checksum_key=args.checksum_key
    )

    if not client.config.client_id or not client.config.api_key:
        print("ERROR: PayOS Client ID and API Key required.", file=sys.stderr)
        sys.exit(1)

    try:
        if args.command == "create":
            res = client.create_payment_link(
                order_code=args.order_code,
                amount=args.amount,
                description=args.desc,
                cancel_url=args.cancel_url,
                return_url=args.return_url
            )
            print(json.dumps(res, indent=2, ensure_ascii=False))
        elif args.command == "info":
            res = client.get_payment_info(order_code=args.order_code)
            print(json.dumps(res, indent=2, ensure_ascii=False))
        elif args.command == "cancel":
            res = client.cancel_payment_link(order_code=args.order_code, cancellation_reason=args.reason)
            print(json.dumps(res, indent=2, ensure_ascii=False))
        elif args.command == "confirm-webhook":
            res = client.confirm_webhook(webhook_url=args.url)
            print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as ex:
        print(f"PayOS API Error: {ex}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
