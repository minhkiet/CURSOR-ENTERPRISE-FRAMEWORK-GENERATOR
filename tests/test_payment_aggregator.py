"""
Tests for Vietnam Payment Aggregator, Multi-Provider Quota Management,
Auto-Failover (SePay -> PayOS -> Pay2S), and Manual Fallback with Receipt Verification.
"""

import datetime
import json
import pathlib
import tempfile
import unittest

from tools.api_integrations.payment_aggregator import (
    AccountQuota,
    ManualPaymentStatus,
    PaymentAggregator,
    ProviderType,
    RoutingStatus,
)


class TestPaymentAggregator(unittest.TestCase):
    """Test suite for payment aggregator, quota routing, and manual fallback."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.state_file = pathlib.Path(self.temp_dir.name) / "payment_aggregator_state.json"
        self.aggregator = PaymentAggregator(data_file=str(self.state_file))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_default_accounts_initialization(self):
        """Verify default demo accounts for SePay, PayOS, and Pay2S."""
        summary = self.aggregator.get_summary()
        self.assertEqual(summary["total_accounts"], 3)

        accounts = {a["account_id"]: a for a in summary["accounts"]}
        self.assertIn("sepay-mb-01", accounts)
        self.assertIn("payos-vcb-01", accounts)
        self.assertIn("pay2s-tcb-01", accounts)

        # Priority 1: SePay, Priority 2: PayOS, Priority 3: Pay2S
        self.assertEqual(accounts["sepay-mb-01"]["priority"], 1)
        self.assertEqual(accounts["payos-vcb-01"]["priority"], 2)
        self.assertEqual(accounts["pay2s-tcb-01"]["priority"], 3)

    def test_primary_routing_to_sepay(self):
        """When all accounts have quota, route should select Priority 1 (SePay)."""
        res = self.aggregator.route_payment(order_id="ORD101", amount=150_000.0)
        self.assertTrue(res.success)
        self.assertEqual(res.status, RoutingStatus.AUTO_ROUTED)
        self.assertEqual(res.provider, ProviderType.SEPAY.value)
        self.assertEqual(res.account_id, "sepay-mb-01")
        self.assertFalse(res.is_manual_verification)
        self.assertIn("vietqr_url", res.payment_instruction)

    def test_failover_to_payos_when_sepay_exhausted(self):
        """When SePay reaches transaction or amount limit, auto-failover to PayOS."""
        sepay_acc = self.aggregator.get_account("sepay-mb-01")
        self.assertIsNotNone(sepay_acc)
        # Exhaust SePay daily tx limit
        sepay_acc.current_daily_tx_count = sepay_acc.daily_tx_limit

        res = self.aggregator.route_payment(order_id="ORD102", amount=200_000.0)
        self.assertTrue(res.success)
        self.assertEqual(res.status, RoutingStatus.AUTO_ROUTED)
        self.assertEqual(res.provider, ProviderType.PAYOS.value)
        self.assertEqual(res.account_id, "payos-vcb-01")

    def test_failover_to_pay2s_when_sepay_and_payos_exhausted(self):
        """When both SePay and PayOS reach limit, auto-failover to Pay2S."""
        sepay_acc = self.aggregator.get_account("sepay-mb-01")
        payos_acc = self.aggregator.get_account("payos-vcb-01")
        sepay_acc.current_daily_tx_count = sepay_acc.daily_tx_limit
        payos_acc.current_daily_amount = payos_acc.daily_amount_limit

        res = self.aggregator.route_payment(order_id="ORD103", amount=500_000.0)
        self.assertTrue(res.success)
        self.assertEqual(res.status, RoutingStatus.AUTO_ROUTED)
        self.assertEqual(res.provider, ProviderType.PAY2S.value)
        self.assertEqual(res.account_id, "pay2s-tcb-01")

    def test_fallback_to_manual_when_all_quotas_exhausted(self):
        """When ALL automated accounts are exhausted, fallback to manual bank transfer."""
        for acc in self.aggregator.accounts.values():
            acc.current_daily_tx_count = acc.daily_tx_limit

        res = self.aggregator.route_payment(order_id="ORD104", amount=1_000_000.0)
        self.assertFalse(res.success)
        self.assertEqual(res.status, RoutingStatus.ALL_QUOTA_EXCEEDED_FALLBACK_MANUAL)
        self.assertTrue(res.is_manual_verification)
        self.assertEqual(res.provider, ProviderType.MANUAL.value)

        # Check manual instructions & contact info
        instruction = res.payment_instruction
        self.assertEqual(instruction["payment_mode"], "MANUAL_VERIFICATION_FALLBACK")
        self.assertIn("Vietcombank", instruction["bank_name"])
        self.assertIn("XACNHAN DHORD104", instruction["transfer_content"])
        self.assertIn("hotline", res.manual_contact)
        self.assertIn("zalo", res.manual_contact)

    def test_preferred_provider_routing(self):
        """Specifying preferred_provider routes to that provider if it has quota."""
        res = self.aggregator.route_payment(
            order_id="ORD105",
            amount=300_000.0,
            preferred_provider="pay2s"
        )
        self.assertTrue(res.success)
        self.assertEqual(res.provider, "pay2s")
        self.assertEqual(res.account_id, "pay2s-tcb-01")

    def test_single_tx_limits(self):
        """Amounts violating single transaction bounds are rejected by account quota."""
        acc = self.aggregator.get_account("sepay-mb-01")
        # Below min amount (2,000 VND)
        ok_min, _ = acc.has_quota(500.0)
        self.assertFalse(ok_min)

        # Exceeds max per tx (20,000,000 VND)
        ok_max, _ = acc.has_quota(25_000_000.0)
        self.assertFalse(ok_max)

    def test_submit_manual_receipt_and_admin_review(self):
        """Customer uploads receipt image and admin approves payment."""
        # Create a mock receipt image file
        mock_image = pathlib.Path(self.temp_dir.name) / "bill_payment_1001.jpg"
        mock_image.write_bytes(b"mock_image_binary_content")

        sub_res = self.aggregator.submit_manual_receipt(
            order_id="ORD201",
            amount=2_500_000.0,
            sender_name="Nguyen Van A",
            receipt_image_path=str(mock_image),
            note="Da chuyen khoan luc 14:30 tu VCB",
            contact_phone="0912345678"
        )
        self.assertTrue(sub_res["success"])
        self.assertEqual(sub_res["status"], ManualPaymentStatus.PENDING_REVIEW.value)
        self.assertTrue(sub_res["receipt_attached"])

        # Check pending list
        summary = self.aggregator.get_summary()
        self.assertEqual(summary["pending_manual_reviews"], 1)

        # Admin approves
        review_res = self.aggregator.review_manual_payment(
            order_id="ORD201",
            action="approve",
            reviewed_by="admin_linh",
            review_note="Sao ke bank khop 2,500,000 VND"
        )
        self.assertTrue(review_res["success"])
        self.assertEqual(review_res["status"], ManualPaymentStatus.APPROVED.value)

        # Pending count drops
        summary_after = self.aggregator.get_summary()
        self.assertEqual(summary_after["pending_manual_reviews"], 0)

    def test_invalid_receipt_file_extension(self):
        """Uploading dangerous file extensions raises ValueError."""
        mock_exe = pathlib.Path(self.temp_dir.name) / "malicious.exe"
        mock_exe.write_bytes(b"danger")

        with self.assertRaises(ValueError):
            self.aggregator.submit_manual_receipt(
                order_id="ORD202",
                amount=100_000.0,
                sender_name="Bad Actor",
                receipt_image_path=str(mock_exe)
            )

    def test_daily_reset_logic(self):
        """When date changes, daily counters should automatically reset."""
        acc = self.aggregator.get_account("sepay-mb-01")
        acc.current_daily_tx_count = 50
        acc.current_daily_amount = 25_000_000.0
        acc.last_reset_date = "2020-01-01"

        acc.check_reset()
        self.assertEqual(acc.current_daily_tx_count, 0)
        self.assertEqual(acc.current_daily_amount, 0.0)
        self.assertEqual(acc.last_reset_date, datetime.date.today().isoformat())

    def test_persistence_save_and_load(self):
        """State is persisted to JSON file and reloaded accurately."""
        self.aggregator.record_successful_payment("sepay-mb-01", 1_000_000.0)
        self.assertTrue(self.state_file.exists())

        # Create new aggregator instance with same file
        new_agg = PaymentAggregator(data_file=str(self.state_file))
        new_sepay = new_agg.get_account("sepay-mb-01")
        self.assertEqual(new_sepay.current_daily_tx_count, 1)
        self.assertEqual(new_sepay.current_daily_amount, 1_000_000.0)


if __name__ == "__main__":
    unittest.main()
