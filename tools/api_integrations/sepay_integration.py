#!/usr/bin/env python
"""
SePay API Integration Tool

Provides SePay (Vietnam Payments) integration for:
- Bank accounts and balances inspection
- Real-time transaction lookup and reconciliation
- VietQR code / image URL generation
- Virtual Account (VA) orders management
- Webhook authorization verification

Usage:
    python sepay_integration.py accounts --token API_KEY [--sandbox]
    python sepay_integration.py transactions --token API_KEY [--limit 20] [--sandbox]
    python sepay_integration.py vietqr --account ACC_NUM --bank BANK_CODE --amount 50000 --memo "DH123"
    python sepay_integration.py verify-webhook --token API_KEY --auth-header "Apikey YOUR_KEY"
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)


@dataclass
class SePayConfig:
    """SePay API configuration."""
    api_key: str
    sandbox: bool = False

    @property
    def base_url(self) -> str:
        if self.sandbox:
            return "https://userapi-sandbox.sepay.vn/v2"
        return "https://userapi.sepay.vn/v2"


class SePayClient:
    """Client for SePay API v2."""

    def __init__(self, api_key: str, sandbox: bool = False):
        self.config = SePayConfig(api_key=api_key, sandbox=sandbox)
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def list_bank_accounts(self) -> Dict[str, Any]:
        """Fetch linked bank accounts."""
        url = f"{self.config.base_url}/bank-accounts"
        resp = self.session.get(url, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def list_transactions(self, limit: int = 20, since_id: Optional[str] = None) -> Dict[str, Any]:
        """Fetch transaction history."""
        url = f"{self.config.base_url}/transactions"
        params: Dict[str, Any] = {"limit": limit}
        if since_id:
            params["since_id"] = since_id
        resp = self.session.get(url, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def get_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """Get detail of a single transaction."""
        url = f"{self.config.base_url}/transactions/{transaction_id}"
        resp = self.session.get(url, timeout=15)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def generate_vietqr_url(account: str, bank: str, amount: int, memo: str, template: str = "compact") -> str:
        """
        Generate standard VietQR image link via SePay.
        
        Args:
            account: Bank account number
            bank: Bank BIN or short code (e.g. VCB, MB, ACB, TPB)
            amount: Transaction amount in VND
            memo: Order / transfer description
            template: QR template (compact, qr_only, etc.)
        """
        params = {
            "acc": account,
            "bank": bank,
            "amount": str(amount),
            "des": memo,
            "template": template
        }
        return f"https://qr.sepay.vn/img?{urlencode(params)}"

    @staticmethod
    def verify_webhook_auth(auth_header: Optional[str], expected_token: str) -> bool:
        """
        Verify incoming webhook authorization header.
        
        SePay webhooks typically provide 'Apikey <token>' or 'Bearer <token>'.
        """
        if not auth_header or not expected_token:
            return False
        
        header_val = auth_header.strip()
        expected = expected_token.strip()
        
        # Direct match
        if header_val == expected:
            return True
            
        # Apikey <token>
        if header_val.startswith("Apikey "):
            return header_val[len("Apikey "):].strip() == expected
            
        # Bearer <token>
        if header_val.startswith("Bearer "):
            return header_val[len("Bearer "):].strip() == expected
            
        return False


def main():
    parser = argparse.ArgumentParser(description="SePay CLI & Integration Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Accounts command
    acc_parser = subparsers.add_parser("accounts", help="List linked bank accounts")
    acc_parser.add_argument("--token", default=os.environ.get("SEPAY_API_KEY"), help="SePay API Key")
    acc_parser.add_argument("--sandbox", action="store_true", help="Use sandbox environment")

    # Transactions command
    tx_parser = subparsers.add_parser("transactions", help="List recent transactions")
    tx_parser.add_argument("--token", default=os.environ.get("SEPAY_API_KEY"), help="SePay API Key")
    tx_parser.add_argument("--limit", type=int, default=20, help="Number of items to retrieve")
    tx_parser.add_argument("--since-id", help="Filter transactions created after this ID")
    tx_parser.add_argument("--sandbox", action="store_true", help="Use sandbox environment")

    # VietQR command
    qr_parser = subparsers.add_parser("vietqr", help="Generate VietQR image URL")
    qr_parser.add_argument("--account", required=True, help="Bank account number")
    qr_parser.add_argument("--bank", required=True, help="Bank code (e.g. MB, VCB, ACB)")
    qr_parser.add_argument("--amount", type=int, required=True, help="Amount in VND")
    qr_parser.add_argument("--memo", required=True, help="Transfer memo / order code")
    qr_parser.add_argument("--template", default="compact", help="QR template style")

    # Verify webhook command
    wh_parser = subparsers.add_parser("verify-webhook", help="Verify webhook authorization header")
    wh_parser.add_argument("--token", default=os.environ.get("SEPAY_API_KEY"), help="Configured SePay API Key")
    wh_parser.add_argument("--auth-header", required=True, help="Header value from request")

    args = parser.parse_args()

    if args.command == "vietqr":
        qr_url = SePayClient.generate_vietqr_url(
            account=args.account,
            bank=args.bank,
            amount=args.amount,
            memo=args.memo,
            template=args.template
        )
        print(f"VietQR Image URL: {qr_url}")
        return

    if args.command == "verify-webhook":
        if not args.token:
            print("ERROR: API token required (--token or SEPAY_API_KEY).", file=sys.stderr)
            sys.exit(1)
        valid = SePayClient.verify_webhook_auth(args.auth_header, args.token)
        print(json.dumps({"valid": valid}))
        sys.exit(0 if valid else 1)

    # API commands
    if not args.token:
        print("ERROR: SePay API token required (--token or SEPAY_API_KEY env var).", file=sys.stderr)
        sys.exit(1)

    client = SePayClient(api_key=args.token, sandbox=args.sandbox)

    try:
        if args.command == "accounts":
            res = client.list_bank_accounts()
            print(json.dumps(res, indent=2, ensure_ascii=False))
        elif args.command == "transactions":
            res = client.list_transactions(limit=args.limit, since_id=args.since_id)
            print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as ex:
        print(f"API Error: {ex}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
