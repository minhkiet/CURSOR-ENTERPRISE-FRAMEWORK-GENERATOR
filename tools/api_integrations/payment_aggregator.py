#!/usr/bin/env python
"""
Vietnam Payment Aggregator & Multi-Provider Quota Manager

Manages payment accounts across multiple providers (SePay, PayOS, Pay2S):
- Tracks transaction counts and volume limits per account and provider.
- Automatically routes payments to available providers based on remaining quota and priority.
- Automatically fails over to secondary providers when primary accounts exceed limits.
- Automatically falls back to Manual Bank Transfer Verification when all automated quotas are exhausted.
- Supports customer receipt image upload and manual review workflow.

Usage:
    python payment_aggregator.py status
    python payment_aggregator.py route --order ORDER123 --amount 250000
    python payment_aggregator.py submit-receipt --order ORDER123 --image /path/to/bill.jpg
    python payment_aggregator.py list-manual
    python payment_aggregator.py review-manual --order ORDER123 --action approve
"""

import argparse
import datetime
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class ProviderType(str, Enum):
    SEPAY = "sepay"
    PAYOS = "payos"
    PAY2S = "pay2s"
    MANUAL = "manual"


class RoutingStatus(str, Enum):
    AUTO_ROUTED = "AUTO_ROUTED"
    ALL_QUOTA_EXCEEDED_FALLBACK_MANUAL = "ALL_QUOTA_EXCEEDED_FALLBACK_MANUAL"
    DISABLED = "DISABLED"


class ManualPaymentStatus(str, Enum):
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


@dataclass
class AccountQuota:
    """Configuration and live usage metrics for a payment provider account."""
    account_id: str
    provider: str  # "sepay", "payos", "pay2s"
    bank_name: str
    account_number: str
    account_holder: str
    priority: int = 1  # 1 = highest priority, 2 = fallback 1, 3 = fallback 2
    daily_tx_limit: int = 100  # Max transactions allowed per day
    daily_amount_limit: float = 50_000_000.0  # Max total amount per day (VND)
    max_amount_per_tx: float = 20_000_000.0  # Max amount for a single transaction
    min_amount_per_tx: float = 2_000.0  # Min amount for a single transaction
    current_daily_tx_count: int = 0
    current_daily_amount: float = 0.0
    is_active: bool = True
    last_reset_date: str = field(default_factory=lambda: datetime.date.today().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def check_reset(self) -> None:
        """Reset daily counters if current date differs from last reset date."""
        today_str = datetime.date.today().isoformat()
        if self.last_reset_date != today_str:
            self.current_daily_tx_count = 0
            self.current_daily_amount = 0.0
            self.last_reset_date = today_str

    def has_quota(self, amount: float) -> Tuple[bool, str]:
        """Check if account can accommodate a new transaction with given amount."""
        self.check_reset()
        if not self.is_active:
            return False, f"Account {self.account_id} is inactive"
        if amount < self.min_amount_per_tx:
            return False, f"Amount {amount:,.0f} VND is below minimum {self.min_amount_per_tx:,.0f} VND"
        if amount > self.max_amount_per_tx:
            return False, f"Amount {amount:,.0f} VND exceeds single tx limit {self.max_amount_per_tx:,.0f} VND"
        if self.current_daily_tx_count >= self.daily_tx_limit:
            return False, f"Daily transaction limit reached ({self.current_daily_tx_count}/{self.daily_tx_limit})"
        if (self.current_daily_amount + amount) > self.daily_amount_limit:
            return False, (
                f"Daily amount limit reached (Current: {self.current_daily_amount:,.0f} + "
                f"Requested: {amount:,.0f} > Limit: {self.daily_amount_limit:,.0f} VND)"
            )
        return True, "OK"

    def record_usage(self, amount: float) -> None:
        """Record a completed transaction against quota."""
        self.check_reset()
        self.current_daily_tx_count += 1
        self.current_daily_amount += amount

    @property
    def remaining_tx_count(self) -> int:
        self.check_reset()
        return max(0, self.daily_tx_limit - self.current_daily_tx_count)

    @property
    def remaining_amount(self) -> float:
        self.check_reset()
        return max(0.0, self.daily_amount_limit - self.current_daily_amount)

    @property
    def usage_percentage(self) -> float:
        self.check_reset()
        if self.daily_tx_limit <= 0:
            return 100.0
        tx_ratio = (self.current_daily_tx_count / self.daily_tx_limit) * 100
        amount_ratio = (self.current_daily_amount / self.daily_amount_limit) * 100 if self.daily_amount_limit > 0 else 0
        return max(tx_ratio, amount_ratio)


@dataclass
class PaymentRoutingResult:
    """Outcome of a payment routing request."""
    success: bool
    status: RoutingStatus
    order_id: str
    amount: float
    provider: Optional[str] = None
    account_id: Optional[str] = None
    is_manual_verification: bool = False
    payment_instruction: Dict[str, Any] = field(default_factory=dict)
    manual_contact: Dict[str, Any] = field(default_factory=dict)
    message: str = ""


@dataclass
class ManualReceiptSubmission:
    """Manual bank transfer verification submission with optional image proof."""
    order_id: str
    amount: float
    sender_name: str
    transfer_time: str
    receipt_image_path: Optional[str] = None
    receipt_image_name: Optional[str] = None
    note: str = ""
    contact_phone: str = ""
    status: ManualPaymentStatus = ManualPaymentStatus.PENDING_REVIEW
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[str] = None
    review_note: Optional[str] = None


class PaymentAggregator:
    """
    Central Manager for Multi-Provider Vietnam Payments (SePay, PayOS, Pay2S, Manual).
    """

    DEFAULT_FALLBACK_CONTACT = {
        "hotline": "1900-8888",
        "zalo": "https://zalo.me/0988888888",
        "telegram": "@hotro_thanhtoan",
        "email": "billing@example.com",
        "instruction": (
            "Tất cả các cổng thanh toán tự động đã đạt hạn mức trong ngày. "
            "Vui lòng chuyển khoản trực tiếp và gửi kèm hình ảnh hóa đơn / sao kê để được xác thực thủ công nhanh nhất."
        ),
    }

    DEFAULT_MANUAL_BANK_ACCOUNT = {
        "bank_name": "Vietcombank (VCB)",
        "bank_code": "VCB",
        "account_number": "9998888999",
        "account_holder": "CONG TY TNHH ENTERPRISE VIBE",
        "branch": "Hoi So Chinh",
    }

    def __init__(self, data_file: Optional[str] = None):
        self.data_file = Path(data_file) if data_file else None
        self.accounts: Dict[str, AccountQuota] = {}
        self.manual_submissions: Dict[str, ManualReceiptSubmission] = {}
        self.manual_bank_account = dict(self.DEFAULT_MANUAL_BANK_ACCOUNT)
        self.fallback_contact = dict(self.DEFAULT_FALLBACK_CONTACT)

        if self.data_file and self.data_file.exists():
            self.load_state()
        else:
            self._init_default_demo_accounts()

    def _init_default_demo_accounts(self) -> None:
        """Initialize standard production accounts with tiered priority."""
        # 1. SePay (Primary - Priority 1)
        self.register_account(AccountQuota(
            account_id="sepay-mb-01",
            provider=ProviderType.SEPAY.value,
            bank_name="MBBank",
            account_number="0388888888",
            account_holder="CONG TY TNHH ENTERPRISE VIBE",
            priority=1,
            daily_tx_limit=100,
            daily_amount_limit=50_000_000.0,
            max_amount_per_tx=20_000_000.0,
        ))

        # 2. PayOS (Secondary Fallback - Priority 2)
        self.register_account(AccountQuota(
            account_id="payos-vcb-01",
            provider=ProviderType.PAYOS.value,
            bank_name="Vietcombank",
            account_number="1012345678",
            account_holder="CONG TY TNHH ENTERPRISE VIBE",
            priority=2,
            daily_tx_limit=80,
            daily_amount_limit=40_000_000.0,
            max_amount_per_tx=15_000_000.0,
        ))

        # 3. Pay2S (Tertiary Fallback - Priority 3)
        self.register_account(AccountQuota(
            account_id="pay2s-tcb-01",
            provider=ProviderType.PAY2S.value,
            bank_name="Techcombank",
            account_number="19033333333333",
            account_holder="CONG TY TNHH ENTERPRISE VIBE",
            priority=3,
            daily_tx_limit=50,
            daily_amount_limit=30_000_000.0,
            max_amount_per_tx=10_000_000.0,
        ))

    def register_account(self, quota: AccountQuota) -> None:
        """Register or update a payment account."""
        self.accounts[quota.account_id] = quota
        self.save_state()

    def remove_account(self, account_id: str) -> bool:
        """Remove an account by ID."""
        if account_id in self.accounts:
            del self.accounts[account_id]
            self.save_state()
            return True
        return False

    def get_account(self, account_id: str) -> Optional[AccountQuota]:
        """Fetch account by ID."""
        return self.accounts.get(account_id)

    def route_payment(
        self,
        order_id: str,
        amount: float,
        description: str = "",
        preferred_provider: Optional[str] = None
    ) -> PaymentRoutingResult:
        """
        Route payment to the best available provider account.
        
        Logic:
        1. If preferred_provider is specified, try active accounts matching that provider first.
        2. Otherwise, sort active accounts by priority (1 is highest), then remaining quota.
        3. If an account has sufficient quota (tx count and amount limit), allocate payment to it.
        4. If ALL automated accounts are exhausted or over limit, trigger Manual Verification Fallback.
        """
        candidates: List[AccountQuota] = [
            acc for acc in self.accounts.values() if acc.is_active
        ]

        # Prioritize preferred provider if requested
        if preferred_provider:
            pref_lower = preferred_provider.lower()
            candidates.sort(key=lambda a: (0 if a.provider.lower() == pref_lower else 1, a.priority, -a.remaining_amount))
        else:
            candidates.sort(key=lambda a: (a.priority, -a.remaining_amount))

        selected_account: Optional[AccountQuota] = None
        rejection_reasons: List[str] = []

        for acc in candidates:
            ok, reason = acc.has_quota(amount)
            if ok:
                selected_account = acc
                break
            else:
                rejection_reasons.append(f"[{acc.account_id} - {acc.provider}]: {reason}")

        if selected_account:
            # Auto-route successful
            instruction = {
                "provider": selected_account.provider,
                "account_id": selected_account.account_id,
                "bank_name": selected_account.bank_name,
                "account_number": selected_account.account_number,
                "account_holder": selected_account.account_holder,
                "order_id": order_id,
                "amount": amount,
                "transfer_content": f"DH{order_id}",
                "payment_mode": "AUTOMATED_GATEWAY",
                "vietqr_url": (
                    f"https://img.vietqr.io/image/{selected_account.bank_name}-{selected_account.account_number}-compact.png"
                    f"?amount={int(amount)}&addInfo=DH{order_id}&accountName={selected_account.account_holder}"
                )
            }
            return PaymentRoutingResult(
                success=True,
                status=RoutingStatus.AUTO_ROUTED,
                order_id=order_id,
                amount=amount,
                provider=selected_account.provider,
                account_id=selected_account.account_id,
                is_manual_verification=False,
                payment_instruction=instruction,
                message=f"Đơn hàng #{order_id} được tự động điều phối qua {selected_account.provider.upper()} ({selected_account.bank_name})."
            )

        # Fallback to Manual Bank Transfer Verification
        manual_instruction = {
            "order_id": order_id,
            "amount": amount,
            "bank_name": self.manual_bank_account["bank_name"],
            "account_number": self.manual_bank_account["account_number"],
            "account_holder": self.manual_bank_account["account_holder"],
            "branch": self.manual_bank_account.get("branch", ""),
            "transfer_content": f"XACNHAN DH{order_id}",
            "payment_mode": "MANUAL_VERIFICATION_FALLBACK",
            "vietqr_url": (
                f"https://img.vietqr.io/image/{self.manual_bank_account['bank_name']}-{self.manual_bank_account['account_number']}-compact.png"
                f"?amount={int(amount)}&addInfo=XACNHAN+DH{order_id}&accountName={self.manual_bank_account['account_holder']}"
            ),
            "rejection_summary": rejection_reasons
        }

        return PaymentRoutingResult(
            success=False,
            status=RoutingStatus.ALL_QUOTA_EXCEEDED_FALLBACK_MANUAL,
            order_id=order_id,
            amount=amount,
            provider=ProviderType.MANUAL.value,
            account_id="manual-fallback",
            is_manual_verification=True,
            payment_instruction=manual_instruction,
            manual_contact=self.fallback_contact,
            message=(
                f"Tất cả các tài khoản thanh toán tự động (SePay, PayOS, Pay2S) đã hết hạn mức trong ngày. "
                f"Hệ thống tự động chuyển đơn #{order_id} sang chế độ chuyển khoản trực tiếp và xác thực thủ công."
            )
        )

    def record_successful_payment(self, account_id: str, amount: float) -> bool:
        """Increment quota counters when a payment succeeds."""
        if account_id in self.accounts:
            self.accounts[account_id].record_usage(amount)
            self.save_state()
            return True
        return False

    def submit_manual_receipt(
        self,
        order_id: str,
        amount: float,
        sender_name: str,
        receipt_image_path: Optional[str] = None,
        note: str = "",
        contact_phone: str = "",
    ) -> Dict[str, Any]:
        """
        Record user payment proof (receipt image or transfer note) for manual review.
        """
        img_name = None
        if receipt_image_path:
            p = Path(receipt_image_path)
            valid_exts = {".jpg", ".jpeg", ".png", ".webp", ".pdf"}
            if p.suffix.lower() not in valid_exts:
                raise ValueError(f"Định dạng hình ảnh không hỗ trợ: {p.suffix}. Hỗ trợ: {', '.join(valid_exts)}")
            img_name = p.name

        submission = ManualReceiptSubmission(
            order_id=order_id,
            amount=amount,
            sender_name=sender_name,
            transfer_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            receipt_image_path=str(receipt_image_path) if receipt_image_path else None,
            receipt_image_name=img_name,
            note=note,
            contact_phone=contact_phone,
            status=ManualPaymentStatus.PENDING_REVIEW
        )

        self.manual_submissions[order_id] = submission
        self.save_state()

        return {
            "success": True,
            "order_id": order_id,
            "status": ManualPaymentStatus.PENDING_REVIEW.value,
            "receipt_attached": bool(receipt_image_path),
            "message": (
                f"Đã nhận thông tin chuyển khoản và bằng chứng thanh toán cho đơn hàng #{order_id}. "
                f"Nhân viên hỗ trợ sẽ đối soát và kích hoạt đơn hàng trong ít phút."
            ),
            "hotline": self.fallback_contact.get("hotline"),
            "zalo": self.fallback_contact.get("zalo")
        }

    def review_manual_payment(
        self,
        order_id: str,
        action: str,  # "approve" or "reject"
        reviewed_by: str = "admin",
        review_note: str = ""
    ) -> Dict[str, Any]:
        """Approve or reject a manual payment submission."""
        sub = self.manual_submissions.get(order_id)
        if not sub:
            return {"success": False, "error": f"Không tìm thấy đơn hàng #{order_id} trong danh sách chờ duyệt"}

        action_clean = action.strip().lower()
        if action_clean == "approve":
            sub.status = ManualPaymentStatus.APPROVED
        elif action_clean == "reject":
            sub.status = ManualPaymentStatus.REJECTED
        else:
            return {"success": False, "error": f"Hành động không hợp lệ: {action}. Chỉ chấp nhận 'approve' hoặc 'reject'"}

        sub.reviewed_by = reviewed_by
        sub.reviewed_at = datetime.datetime.now().isoformat()
        sub.review_note = review_note
        self.save_state()

        return {
            "success": True,
            "order_id": order_id,
            "status": sub.status.value,
            "reviewed_by": reviewed_by,
            "review_note": review_note
        }

    def get_summary(self) -> Dict[str, Any]:
        """Get high-level status of all provider accounts and quotas."""
        acc_summaries = []
        total_capacity_amount = 0.0
        total_used_amount = 0.0
        total_capacity_tx = 0
        total_used_tx = 0

        for acc in sorted(self.accounts.values(), key=lambda a: a.priority):
            acc.check_reset()
            total_capacity_amount += acc.daily_amount_limit
            total_used_amount += acc.current_daily_amount
            total_capacity_tx += acc.daily_tx_limit
            total_used_tx += acc.current_daily_tx_count

            acc_summaries.append({
                "account_id": acc.account_id,
                "provider": acc.provider,
                "bank": acc.bank_name,
                "account_number": acc.account_number,
                "priority": acc.priority,
                "active": acc.is_active,
                "tx_quota": f"{acc.current_daily_tx_count}/{acc.daily_tx_limit}",
                "tx_remaining": acc.remaining_tx_count,
                "amount_quota": f"{acc.current_daily_amount:,.0f}/{acc.daily_amount_limit:,.0f} VND",
                "amount_remaining": f"{acc.remaining_amount:,.0f} VND",
                "usage_pct": round(acc.usage_percentage, 1)
            })

        pending_manual = sum(
            1 for s in self.manual_submissions.values()
            if s.status == ManualPaymentStatus.PENDING_REVIEW
        )

        return {
            "total_accounts": len(self.accounts),
            "accounts": acc_summaries,
            "total_daily_tx_quota": f"{total_used_tx}/{total_capacity_tx}",
            "total_daily_amount_quota": f"{total_used_amount:,.0f}/{total_capacity_amount:,.0f} VND",
            "pending_manual_reviews": pending_manual,
            "manual_contact": self.fallback_contact
        }

    def save_state(self) -> None:
        """Persist state to JSON file if data_file is configured."""
        if not self.data_file:
            return
        state = {
            "accounts": {k: asdict(v) for k, v in self.accounts.items()},
            "manual_submissions": {k: asdict(v) for k, v in self.manual_submissions.items()},
            "manual_bank_account": self.manual_bank_account,
            "fallback_contact": self.fallback_contact,
        }
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def load_state(self) -> None:
        """Restore state from JSON file."""
        if not self.data_file or not self.data_file.exists():
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                state = json.load(f)
            self.accounts = {
                k: AccountQuota(**v) for k, v in state.get("accounts", {}).items()
            }
            self.manual_submissions = {
                k: ManualReceiptSubmission(**v) for k, v in state.get("manual_submissions", {}).items()
            }
            self.manual_bank_account = state.get("manual_bank_account", self.DEFAULT_MANUAL_BANK_ACCOUNT)
            self.fallback_contact = state.get("fallback_contact", self.DEFAULT_FALLBACK_CONTACT)
        except Exception as e:
            sys.stderr.write(f"Error loading state from {self.data_file}: {e}\n")


def main():
    parser = argparse.ArgumentParser(description="Vietnam Payment Aggregator & Quota Manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # status
    subparsers.add_parser("status", help="Show quota status of all accounts")

    # route
    route_parser = subparsers.add_parser("route", help="Route payment for an order")
    route_parser.add_argument("--order", required=True, help="Order ID")
    route_parser.add_argument("--amount", type=float, required=True, help="Amount in VND")
    route_parser.add_argument("--provider", help="Preferred provider (sepay, payos, pay2s)")
    route_parser.add_argument("--description", default="", help="Order description")

    # submit-receipt
    receipt_parser = subparsers.add_parser("submit-receipt", help="Submit manual transfer proof")
    receipt_parser.add_argument("--order", required=True, help="Order ID")
    receipt_parser.add_argument("--amount", type=float, required=True, help="Amount in VND")
    receipt_parser.add_argument("--sender", required=True, help="Sender name")
    receipt_parser.add_argument("--image", help="Receipt screenshot / file path")
    receipt_parser.add_argument("--phone", default="", help="Customer contact phone")
    receipt_parser.add_argument("--note", default="", help="Customer note")

    # list-manual
    subparsers.add_parser("list-manual", help="List pending manual verification requests")

    # review-manual
    review_parser = subparsers.add_parser("review-manual", help="Review manual payment")
    review_parser.add_argument("--order", required=True, help="Order ID")
    review_parser.add_argument("--action", choices=["approve", "reject"], required=True)
    review_parser.add_argument("--reviewer", default="admin", help="Reviewer username")
    review_parser.add_argument("--note", default="", help="Review note")

    args = parser.parse_args()
    aggregator = PaymentAggregator()

    if args.command == "status":
        summary = aggregator.get_summary()
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    elif args.command == "route":
        result = aggregator.route_payment(
            order_id=args.order,
            amount=args.amount,
            preferred_provider=args.provider,
            description=args.description
        )
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    elif args.command == "submit-receipt":
        res = aggregator.submit_manual_receipt(
            order_id=args.order,
            amount=args.amount,
            sender_name=args.sender,
            receipt_image_path=args.image,
            contact_phone=args.phone,
            note=args.note
        )
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.command == "list-manual":
        pending = [
            asdict(s) for s in aggregator.manual_submissions.values()
            if s.status == ManualPaymentStatus.PENDING_REVIEW
        ]
        print(json.dumps(pending, indent=2, ensure_ascii=False))
    elif args.command == "review-manual":
        res = aggregator.review_manual_payment(
            order_id=args.order,
            action=args.action,
            reviewed_by=args.reviewer,
            review_note=args.note
        )
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
