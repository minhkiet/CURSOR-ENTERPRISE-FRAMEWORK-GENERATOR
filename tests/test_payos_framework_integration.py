"""
Tests for PayOS integration into Vibe Enterprise Framework Generator.
"""

import hashlib
import hmac
import pathlib
import unittest
from vibe_framework.skill_discovery import (
    SkillDiscovery,
    SkillRegistry,
    CrossAgentSkillDiscovery
)
from tools.api_integrations.payos_integration import PayOSClient


class TestPayOSFrameworkIntegration(unittest.TestCase):
    """Test suite for PayOS framework integration."""

    def setUp(self):
        self.discovery = SkillDiscovery()
        self.registry = SkillRegistry()
        self.cross_discovery = CrossAgentSkillDiscovery()

    def test_payos_in_registry(self):
        """Verify payos metadata is registered in SkillRegistry."""
        payos_meta = self.registry.get("payos")
        self.assertIsNotNone(payos_meta)
        self.assertEqual(payos_meta.version, "1.0.0")
        self.assertIn("vietnam", payos_meta.tags)
        self.assertIn("payos", payos_meta.tags)
        self.assertEqual(payos_meta.path, ".cursor/skills/payos/SKILL.md")

    def test_payos_detection(self):
        """Verify payos skill is detected on relevant requests."""
        detected = self.discovery.detect_skills("Tích hợp cổng thanh toán payos vào hệ thống")
        skill_names = [d.skill for d in detected]
        self.assertIn("payos", skill_names)

        slash_detected = self.discovery.detect_skills("/payos tạo link thanh toán")
        slash_names = [d.skill for d in slash_detected]
        self.assertIn("payos", slash_names)

    def test_cross_agent_mapping(self):
        """Verify payos is present in agent mappings."""
        cursor_skills = self.cross_discovery.AGENT_SKILL_MAPPINGS.get("cursor", [])
        self.assertIn("payos", cursor_skills)

        codex_skills = self.cross_discovery.AGENT_SKILL_MAPPINGS.get("codex", [])
        self.assertIn("payos", codex_skills)

    def test_request_signature_generation(self):
        """Verify HMAC-SHA256 request signature logic."""
        ck = "test_checksum_key_xyz"
        sig = PayOSClient.generate_request_signature(
            amount=20000,
            cancel_url="https://shop.example/cancel",
            description="Thanh toan 20000",
            order_code=1001,
            return_url="https://shop.example/success",
            checksum_key=ck
        )
        expected_str = "amount=20000&cancelUrl=https://shop.example/cancel&description=Thanh toan 20000&orderCode=1001&returnUrl=https://shop.example/success"
        expected_sig = hmac.new(ck.encode("utf-8"), expected_str.encode("utf-8"), hashlib.sha256).hexdigest()
        self.assertEqual(sig, expected_sig)

    def test_webhook_checksum_verification(self):
        """Verify webhook signature validation."""
        ck = "test_webhook_secret_key"
        data = {
            "orderCode": 1001,
            "amount": 20000,
            "description": "Thanh toan 20000",
            "accountNumber": "987654321",
            "reference": "FT999888"
        }
        sorted_keys = sorted(data.keys())
        data_str = "&".join(f"{k}={data[k]}" for k in sorted_keys)
        valid_sig = hmac.new(ck.encode("utf-8"), data_str.encode("utf-8"), hashlib.sha256).hexdigest()

        # Valid
        self.assertTrue(PayOSClient.verify_webhook_data(data, valid_sig, ck))

        # Tampered data
        tampered_data = dict(data)
        tampered_data["amount"] = 50000
        self.assertFalse(PayOSClient.verify_webhook_data(tampered_data, valid_sig, ck))

        # Invalid key or sig
        self.assertFalse(PayOSClient.verify_webhook_data(data, "invalid_sig", ck))
        self.assertFalse(PayOSClient.verify_webhook_data({}, valid_sig, ck))

    def test_payment_skill_and_command_payos_content(self):
        """Verify payment skill and command include PayOS v2 guidelines."""
        skill_text = pathlib.Path(".cursor/skills/sec_vietnam-payment-review/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("PayOS (PayOS Open Banking Gateway API v2)", skill_text)
        self.assertIn("api-merchant.payos.vn", skill_text)
        self.assertIn("PAYOS_CHECKSUM_KEY", skill_text)

        cmd_text = pathlib.Path(".cursor/commands/payment/command.md").read_text(encoding="utf-8")
        self.assertIn("PayOS (PayOS Open Banking Gateway API v2)", cmd_text)
        self.assertIn("PAYOS_CHECKSUM_KEY", cmd_text)


if __name__ == "__main__":
    unittest.main()
