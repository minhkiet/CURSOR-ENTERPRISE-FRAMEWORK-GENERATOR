#!/usr/bin/env python
"""
Pay2S API Integration Tool

Provides Pay2S (Vietnam Bank Webhook & Recipient Name Lookup) integration for:
- Looking up bank account recipient names (get-recipient-name)
- Webhook authorization verification (Bearer token)
- Inbound transactions filtering and validation

Usage:
    python pay2s_integration.py recipient-name --account 0123456789 --bank VCB --secret-key YOUR_KEY
    python pay2s_integration.py verify-webhook --auth-header "Bearer TOKEN" --token TOKEN
    python pay2s_integration.py parse-webhook --payload-json '{"transactions": [...]}'
"""

import argparse
import base64
import hmac
import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)


@dataclass
class Pay2SConfig:
    """Pay2S API configuration."""
    secret_key: Optional[str] = None
    webhook_token: Optional[str] = None
    base_url: str = "https://api.pay2s.vn"


class Pay2SClient:
    """Client for Pay2S API and Webhooks."""

    def __init__(self, secret_key: Optional[str] = None, webhook_token: Optional[str] = None):
        sk = secret_key or os.environ.get("PAY2S_SECRET_KEY")
        wt = webhook_token or os.environ.get("PAY2S_WEBHOOK_TOKEN")
        self.config = Pay2SConfig(secret_key=sk, webhook_token=wt)
        self.session = requests.Session()

    @staticmethod
    def encode_token(secret_key: str) -> str:
        """Encode SecretKey to Base64 for pay2s-token header."""
        return base64.b64encode(secret_key.strip().encode("utf-8")).decode("utf-8")

    @staticmethod
    def verify_webhook_auth(auth_header: Optional[str], expected_token: str) -> bool:
        """
        Verify incoming webhook Authorization header.
        Supports 'Bearer <token>' or raw token match.
        """
        if not auth_header or not expected_token:
            return False

        header_val = auth_header.strip()
        expected = expected_token.strip()

        if header_val == expected:
            return True

        if header_val.startswith("Bearer "):
            token_part = header_val[len("Bearer "):].strip()
            return hmac.compare_digest(token_part, expected)

        return False

    @staticmethod
    def parse_webhook_transactions(payload: Union[Dict[str, Any], List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Extract transaction list from Pay2S webhook payload."""
        if isinstance(payload, dict):
            raw = payload.get("transactions", [])
            return raw if isinstance(raw, list) else []
        if isinstance(payload, list):
            return payload
        return []

    @staticmethod
    def filter_inbound_transactions(transactions: Union[Dict[str, Any], List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Filter transactions where transferType is 'IN'. Accepts dict with 'transactions' or raw list."""
        tx_list = Pay2SClient.parse_webhook_transactions(transactions)
        return [
            tx for tx in tx_list
            if isinstance(tx, dict) and str(tx.get("transferType", "")).upper() == "IN"
        ]

    def get_recipient_name(self, account_number: str, bank_code: str) -> Dict[str, Any]:
        """
        Query account holder name via get-recipient-name API.
        Rate limit: max 10 requests / minute.
        """
        if not self.config.secret_key:
            raise ValueError("Pay2S Secret Key required for get-recipient-name API.")

        token = self.encode_token(self.config.secret_key)
        headers = {
            "Content-Type": "application/json",
            "pay2s-token": token
        }
        body = {
            "accountNumber": str(account_number).strip(),
            "bankCode": str(bank_code).strip().upper()
        }

        url = f"{self.config.base_url}/userapi/get-recipient-name"
        resp = self.session.post(url, json=body, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()


def main():
    parser = argparse.ArgumentParser(description="Pay2S Integration CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Recipient name lookup
    rec_parser = subparsers.add_parser("recipient-name", help="Lookup bank account holder name")
    rec_parser.add_argument("--account", required=True, help="Bank account number")
    rec_parser.add_argument("--bank", required=True, help="Bank code (e.g. VCB, MBB, ACB)")
    rec_parser.add_argument("--secret-key", default=os.environ.get("PAY2S_SECRET_KEY"), help="Pay2S Secret Key")

    # Verify webhook
    wh_parser = subparsers.add_parser("verify-webhook", help="Verify webhook authorization header")
    wh_parser.add_argument("--auth-header", required=True, help="Authorization header value")
    wh_parser.add_argument("--token", default=os.environ.get("PAY2S_WEBHOOK_TOKEN"), help="Configured webhook token")

    # Parse webhook
    parse_parser = subparsers.add_parser("parse-webhook", help="Parse and filter webhook payload")
    parse_parser.add_argument("--payload-json", required=True, help="Webhook payload JSON string")

    args = parser.parse_args()

    if args.command == "verify-webhook":
        if not args.token:
            print("ERROR: Webhook token required (--token or PAY2S_WEBHOOK_TOKEN).", file=sys.stderr)
            sys.exit(1)
        valid = Pay2SClient.verify_webhook_auth(args.auth_header, args.token)
        print(json.dumps({"valid": valid}))
        sys.exit(0 if valid else 1)

    elif args.command == "parse-webhook":
        try:
            payload = json.loads(args.payload_json)
        except Exception as e:
            print(f"ERROR: Invalid payload JSON: {e}", file=sys.stderr)
            sys.exit(1)

        raw_txs = payload.get("transactions", [])
        inbound = Pay2SClient.filter_inbound_transactions(raw_txs)
        print(json.dumps({
            "total_transactions": len(raw_txs),
            "inbound_transactions": inbound
        }, indent=2, ensure_ascii=False))

    elif args.command == "recipient-name":
        if not args.secret_key:
            print("ERROR: Pay2S Secret Key required (--secret-key or PAY2S_SECRET_KEY).", file=sys.stderr)
            sys.exit(1)

        client = Pay2SClient(secret_key=args.secret_key)
        try:
            res = client.get_recipient_name(account_number=args.account, bank_code=args.bank)
            print(json.dumps(res, indent=2, ensure_ascii=False))
        except Exception as ex:
            print(f"API Error: {ex}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
