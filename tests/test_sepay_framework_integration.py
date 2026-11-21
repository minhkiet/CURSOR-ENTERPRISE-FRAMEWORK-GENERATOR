"""
Tests for SePay integration into Vibe Enterprise Framework Generator.
"""

import unittest
from vibe_framework.skill_discovery import (
    SkillDiscovery,
    SkillRegistry,
    CrossAgentSkillDiscovery
)
from tools.api_integrations.sepay_integration import SePayClient


class TestSePayFrameworkIntegration(unittest.TestCase):
    """Test suite for SePay framework integration."""

    def setUp(self):
        self.discovery = SkillDiscovery()
        self.registry = SkillRegistry()
        self.cross_discovery = CrossAgentSkillDiscovery()

    def test_sepay_in_registry(self):
        """Verify sepay metadata is registered in SkillRegistry."""
        sepay_meta = self.registry.get("sepay")
        self.assertIsNotNone(sepay_meta)
        self.assertEqual(sepay_meta.version, "1.0.3")
        self.assertIn("vietnam", sepay_meta.tags)
        self.assertIn("sepay", sepay_meta.tags)
        self.assertEqual(sepay_meta.path, ".cursor/skills/sepay/SKILL.md")

    def test_sepay_detection(self):
        """Verify sepay skill is detected on relevant prompts."""
        detected = self.discovery.detect_skills("Tích hợp webhook sepay vào hệ thống")
        skill_names = [d.skill for d in detected]
        self.assertIn("sepay", skill_names)

        slash_detected = self.discovery.detect_skills("/sepay kiểm tra giao dịch")
        slash_names = [d.skill for d in slash_detected]
        self.assertIn("sepay", slash_names)

    def test_cross_agent_mapping(self):
        """Verify sepay is present in agent mappings."""
        cursor_skills = self.cross_discovery.AGENT_SKILL_MAPPINGS.get("cursor", [])
        self.assertIn("sepay", cursor_skills)

        codex_skills = self.cross_discovery.AGENT_SKILL_MAPPINGS.get("codex", [])
        self.assertIn("sepay", codex_skills)

    def test_sepay_client_vietqr(self):
        """Verify VietQR generation utility."""
        url = SePayClient.generate_vietqr_url(
            account="12345678",
            bank="MB",
            amount=200000,
            memo="ORDER456"
        )
        self.assertTrue(url.startswith("https://qr.sepay.vn/img?"))
        self.assertIn("acc=12345678", url)
        self.assertIn("bank=MB", url)
        self.assertIn("amount=200000", url)
        self.assertIn("des=ORDER456", url)

    def test_sepay_webhook_verification(self):
        """Verify SePay webhook authorization header checks."""
        token = "secret_api_key_123"
        # Apikey format
        self.assertTrue(SePayClient.verify_webhook_auth(f"Apikey {token}", token))
        # Bearer format
        self.assertTrue(SePayClient.verify_webhook_auth(f"Bearer {token}", token))
        # Raw format
        self.assertTrue(SePayClient.verify_webhook_auth(token, token))
        # Invalid cases
        self.assertFalse(SePayClient.verify_webhook_auth("Apikey wrong_key", token))
        self.assertFalse(SePayClient.verify_webhook_auth(None, token))
        self.assertFalse(SePayClient.verify_webhook_auth("", token))

    def test_payment_skill_and_command_integration(self):
        """Verify payment skill and command include SePay 7-step lifecycle."""
        import pathlib
        skill_text = pathlib.Path(".cursor/skills/sec_vietnam-payment-review/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Quy Trình Tích Hợp AI Agent Chuẩn SePay", skill_text)
        self.assertIn("Bước 1 (Skills)", skill_text)
        self.assertIn("Bước 7 (Theo dõi hằng ngày qua SePay MCP)", skill_text)

        cmd_text = pathlib.Path(".cursor/commands/payment/command.md").read_text(encoding="utf-8")
        self.assertIn("SePay Banking - AI Agent 7-Step Lifecycle", cmd_text)
        self.assertIn("1. Skills", cmd_text)
        self.assertIn("7. MCP Daily Monitor", cmd_text)


if __name__ == "__main__":
    unittest.main()
