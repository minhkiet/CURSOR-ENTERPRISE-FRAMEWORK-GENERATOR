"""
Tests for Pay2S integration into Vibe Enterprise Framework Generator.
"""

import base64
import pathlib
import unittest
from vibe_framework.skill_discovery import (
    SkillDiscovery,
    SkillRegistry,
    CrossAgentSkillDiscovery
)
from tools.api_integrations.pay2s_integration import Pay2SClient, Pay2SConfig


class TestPay2SFrameworkIntegration(unittest.TestCase):
    """Test suite for Pay2S framework integration."""

    def setUp(self):
        self.discovery = SkillDiscovery()
        self.registry = SkillRegistry()
        self.cross_discovery = CrossAgentSkillDiscovery()

    def test_pay2s_in_registry(self):
        """Verify pay2s metadata is registered in SkillRegistry."""
        pay2s_meta = self.registry.get("pay2s")
        self.assertIsNotNone(pay2s_meta)
        self.assertEqual(pay2s_meta.version, "1.0.0")
        self.assertIn("vietnam", pay2s_meta.tags)
        self.assertIn("pay2s", pay2s_meta.tags)
        self.assertEqual(pay2s_meta.path, ".cursor/skills/pay2s/SKILL.md")

    def test_pay2s_detection(self):
        """Verify pay2s skill is detected on relevant requests."""
        detected = self.discovery.detect_skills("Tích hợp webhook biến động số dư pay2s vào hệ thống")
        skill_names = [d.skill for d in detected]
        self.assertIn("pay2s", skill_names)

        slash_detected = self.discovery.detect_skills("/pay2s tra cứu tên tài khoản")
        slash_names = [d.skill for d in slash_detected]
        self.assertIn("pay2s", slash_names)

    def test_cross_agent_mapping(self):
        """Verify pay2s is present in agent mappings."""
        cursor_skills = self.cross_discovery.AGENT_SKILL_MAPPINGS.get("cursor", [])
        self.assertIn("pay2s", cursor_skills)

        codex_skills = self.cross_discovery.AGENT_SKILL_MAPPINGS.get("codex", [])
        self.assertIn("pay2s", codex_skills)

    def test_token_base64_encoding(self):
        """Verify Pay2S token encoding for recipient name lookup."""
        raw_secret = "my_secret_key_12345"
        encoded = Pay2SClient.encode_token(raw_secret)
        expected = base64.b64encode(raw_secret.encode("utf-8")).decode("utf-8")
        self.assertEqual(encoded, expected)

    def test_webhook_bearer_auth_verification(self):
        """Verify Bearer token auth validation for Pay2S Webhooks."""
        token = "secure_pay2s_webhook_token_999"

        # Valid with Bearer prefix
        self.assertTrue(Pay2SClient.verify_webhook_auth(f"Bearer {token}", token))

        # Valid without Bearer prefix
        self.assertTrue(Pay2SClient.verify_webhook_auth(token, token))

        # Invalid token
        self.assertFalse(Pay2SClient.verify_webhook_auth("Bearer wrong_token", token))
        self.assertFalse(Pay2SClient.verify_webhook_auth(None, token))
        self.assertFalse(Pay2SClient.verify_webhook_auth("", token))

    def test_filter_inbound_transactions(self):
        """Verify extracting IN transactions from Pay2S payload."""
        payload = {
            "transactions": [
                {
                    "id": 1,
                    "gateway": "MBBank",
                    "transactionDate": "2026-05-10 14:20:00",
                    "transactionNumber": "FT260510001",
                    "accountNumber": "0388888888",
                    "content": "DH1002 chuyen khoan",
                    "transferType": "IN",
                    "transferAmount": 250000
                },
                {
                    "id": 2,
                    "gateway": "MBBank",
                    "transactionDate": "2026-05-10 14:25:00",
                    "transactionNumber": "FT260510002",
                    "accountNumber": "0388888888",
                    "content": "phi duy tri tai khoan",
                    "transferType": "OUT",
                    "transferAmount": 11000
                }
            ]
        }
        inbound = Pay2SClient.filter_inbound_transactions(payload)
        self.assertEqual(len(inbound), 1)
        self.assertEqual(inbound[0]["transactionNumber"], "FT260510001")
        self.assertEqual(inbound[0]["transferAmount"], 250000)

    def test_payment_skill_and_command_pay2s_content(self):
        """Verify payment review skill and commands contain Pay2S specifications."""
        review_text = pathlib.Path(".cursor/skills/sec_vietnam-payment-review/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Pay2S (Pay2S Banking Webhook & Recipient Name API)", review_text)
        self.assertIn("docs.pay2s.vn", review_text)
        self.assertIn("PAY2S_WEBHOOK_TOKEN", review_text)
        self.assertIn("api.pay2s.vn/userapi/get-recipient-name", review_text)

        cmd_text = pathlib.Path(".cursor/commands/payment/command.md").read_text(encoding="utf-8")
        self.assertIn("Pay2S (Pay2S Banking Webhook & Recipient Name API)", cmd_text)
        self.assertIn("PAY2S_WEBHOOK_TOKEN", cmd_text)

        # Dedicated command files exist
        self.assertTrue(pathlib.Path(".cursor/commands/pay2s/command.md").exists())
        self.assertTrue(pathlib.Path(".cursor/commands/pay2s.md").exists())
        self.assertTrue(pathlib.Path(".agents/skills/source-command-pay2s-command/SKILL.md").exists())

        # Dedicated skill files exist
        self.assertTrue(pathlib.Path(".cursor/skills/pay2s/SKILL.md").exists())
        self.assertTrue(pathlib.Path(".cursor/skills/pay2s/references/webhook.md").exists())
        self.assertTrue(pathlib.Path(".cursor/skills/pay2s/references/recipient-name.md").exists())
        self.assertTrue(pathlib.Path(".cursor/skills/pay2s/references/integration-design.md").exists())


if __name__ == "__main__":
    unittest.main()
