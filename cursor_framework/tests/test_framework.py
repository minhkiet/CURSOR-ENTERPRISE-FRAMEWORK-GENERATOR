"""
Test Module

Test cases for the Cursor Enterprise Framework Python library.
"""

import unittest


class TestContextRouter(unittest.TestCase):
    """Tests for ContextRouter."""

    def test_route_landing_page(self):
        """Test routing for landing page request."""
        from cursor_framework import ContextRouter

        router = ContextRouter()
        route = router.route("Create a landing page for SaaS product")

        self.assertIsNotNone(route)
        self.assertIsNotNone(route.skill)

    def test_route_security(self):
        """Test routing for security request."""
        from cursor_framework import ContextRouter

        router = ContextRouter()
        route = router.route("Review security vulnerabilities in authentication")

        self.assertIsNotNone(route)

    def test_intent_classification(self):
        """Test intent classification."""
        from cursor_framework import IntentClassifier, IntentType

        classifier = IntentClassifier()
        intent, confidence = classifier.classify_intent("Create a new component")

        self.assertEqual(intent, IntentType.CODE_GENERATION)
        self.assertGreater(confidence, 0)


class TestMemoryManager(unittest.TestCase):
    """Tests for MemoryManager."""

    def test_store_and_retrieve(self):
        """Test basic store and retrieve."""
        from cursor_framework import MemoryManager, MemoryTier

        manager = MemoryManager()
        manager.store("test_key", {"value": 123}, tier=MemoryTier.HOT)

        result = manager.retrieve("test_key")
        self.assertEqual(result, {"value": 123})

    def test_tier_isolation(self):
        """Test that tiers are isolated."""
        from cursor_framework import MemoryManager, MemoryTier

        manager = MemoryManager()
        manager.store("key1", "value1", tier=MemoryTier.HOT)
        manager.store("key2", "value2", tier=MemoryTier.WARM)

        result1 = manager.retrieve("key1", tier=MemoryTier.HOT)
        result2 = manager.retrieve("key1", tier=MemoryTier.WARM)

        self.assertEqual(result1, "value1")
        self.assertIsNone(result2)

    def test_session_context(self):
        """Test session context storage."""
        from cursor_framework import MemoryManager

        manager = MemoryManager()
        manager.store_session_context("session123", {
            "user": "testuser",
            "project": "testproject"
        })

        user = manager.retrieve_session_context("session123", "user")
        project = manager.retrieve_session_context("session123", "project")

        self.assertEqual(user, "testuser")
        self.assertEqual(project, "testproject")


class TestTokenOptimizer(unittest.TestCase):
    """Tests for TokenOptimizer."""

    def test_estimate_tokens(self):
        """Test token estimation."""
        from cursor_framework import TokenOptimizer

        optimizer = TokenOptimizer()
        tokens = optimizer.estimate_tokens("Hello, world!")

        self.assertGreater(tokens, 0)

    def test_compress(self):
        """Test context compression."""
        from cursor_framework import TokenOptimizer, CompressionStrategy

        optimizer = TokenOptimizer(max_tokens=1000)
        long_text = "This is a test. " * 100

        compressed = optimizer.compress(
            long_text,
            target_tokens=50,
            strategy=CompressionStrategy.SEMANTIC
        )

        self.assertIsNotNone(compressed)
        self.assertLess(len(compressed), len(long_text))


class TestSkillDiscovery(unittest.TestCase):
    """Tests for SkillDiscovery."""

    def test_detect_frontend_taste(self):
        """Test detection of frontend-taste skill."""
        from cursor_framework import SkillDiscovery

        discovery = SkillDiscovery()
        skills = discovery.detect_skills("Create a landing page for portfolio")

        self.assertGreater(len(skills), 0)

    def test_detect_security(self):
        """Test detection of security-review skill."""
        from cursor_framework import SkillDiscovery

        discovery = SkillDiscovery()
        skills = discovery.detect_skills("Review for SQL injection vulnerabilities")

        self.assertGreater(len(skills), 0)

    def test_combined_skills(self):
        """Test skill combination for landing page."""
        from cursor_framework import SkillDiscovery

        discovery = SkillDiscovery()
        skills = discovery.get_combined_skills("Build a landing page with full implementation")

        self.assertGreater(len(skills), 1)


class TestCodeUtils(unittest.TestCase):
    """Tests for code utilities."""

    def test_detect_language(self):
        """Test language detection."""
        from cursor_framework.utils import code_utils

        python_code = "def hello():\n    print('world')"
        lang = code_utils.detect_language(python_code)

        self.assertEqual(lang, "python")

    def test_check_em_dashes(self):
        """Test em-dash detection."""
        from cursor_framework.utils import code_utils

        code = "This is a test\u2014with em dash"
        issues = code_utils.check_em_dashes(code)

        self.assertEqual(len(issues), 1)

    def test_count_code_lines(self):
        """Test line counting."""
        from cursor_framework.utils import code_utils

        code = """def test():
    # comment
    pass

"""
        counts = code_utils.count_code_lines(code)

        self.assertEqual(counts["total"], 4)
        self.assertEqual(counts["code"], 2)


class TestSecurityUtils(unittest.TestCase):
    """Tests for security utilities."""

    def test_sanitize_html(self):
        """Test HTML sanitization."""
        from cursor_framework.utils import security_utils

        dirty = "<script>alert('xss')</script>Hello"
        clean = security_utils.sanitize_html(dirty)

        self.assertNotIn("<script>", clean)
        self.assertIn("Hello", clean)

    def test_generate_token(self):
        """Test token generation."""
        from cursor_framework.utils import security_utils

        token1 = security_utils.generate_token(16)
        token2 = security_utils.generate_token(16)

        self.assertEqual(len(token1), 32)  # hex encoded = 16 * 2
        self.assertNotEqual(token1, token2)


class TestTextUtils(unittest.TestCase):
    """Tests for text utilities."""

    def test_slugify(self):
        """Test text slugification."""
        from cursor_framework.utils import text_utils

        slug = text_utils.slugify("Hello World! This is a Test")
        self.assertEqual(slug, "hello-world-this-is-a-test")

    def test_remove_em_dashes(self):
        """Test em-dash removal."""
        from cursor_framework.utils import text_utils

        text = "This\u2014is\u2014a\u2014test"
        clean = text_utils.remove_em_dashes(text)

        self.assertNotIn("\u2014", clean)
        self.assertEqual(clean.count("-"), 3)


if __name__ == "__main__":
    unittest.main()
