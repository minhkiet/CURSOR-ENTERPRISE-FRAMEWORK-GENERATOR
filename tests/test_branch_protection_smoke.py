"""DELIBERATE FAILURE — branch protection smoke test.

This file exists only to verify that a failing CI check blocks PR merge.
Delete this file after the test completes.
"""

import unittest


class TestDeliberateFailure(unittest.TestCase):
    def test_must_fail_to_block_merge(self):
        """This test intentionally fails to verify CI blocks merge."""
        self.assertEqual(1 + 1, 3, "intentional failure for branch protection smoke test")