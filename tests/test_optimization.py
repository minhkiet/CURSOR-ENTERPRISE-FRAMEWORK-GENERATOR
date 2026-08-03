"""Verify Hướng 2 + 3 — memory_store.save_if_dirty + token_optimizer
single-pass estimate_tokens + SkillDiscovery shared registry."""
from collections import deque
from pathlib import Path
import tempfile

from cursor_framework.memory_manager import MemoryManager, MemoryTier
from cursor_framework.memory_store import MemoryStore
from cursor_framework.skill_discovery import (
    SkillDiscovery,
    SkillRegistry,
    get_shared_registry,
)
from cursor_framework.token_optimizer import TokenOptimizer


def test_save_if_dirty_skips_write(tmp_path: Path):
    mem = tmp_path / "memory.json"
    manager = MemoryManager()
    store = MemoryStore(mem)
    manager.store("k", "v", tier=MemoryTier.WARM)
    written = store.save_if_dirty(manager)
    assert written == 1
    assert mem.exists()

    # No mutation → must not write again.
    before = mem.read_bytes()
    written = store.save_if_dirty(manager)
    assert written == 0
    after = mem.read_bytes()
    assert before == after

    # Now mutate → should write.
    manager.store("k2", "v2", tier=MemoryTier.WARM)
    written = store.save_if_dirty(manager)
    assert written == 2


def test_token_estimate_single_pass_text():
    opt = TokenOptimizer()
    assert opt.estimate_tokens("") == 0
    assert opt.estimate_tokens("hello world") >= 2
    assert opt.estimate_tokens("hello world this is a longer sentence") >= 6
    # Estimates should grow with word count, not artificially cap.
    assert opt.estimate_tokens("a " * 100) >= 100


def test_token_estimate_code():
    opt = TokenOptimizer()
    code = "```python\ndef foo(x, y):\n    return x + y\n```"
    tokens = opt.estimate_tokens(code)
    assert tokens > 5


def test_compression_history_bounded():
    opt = TokenOptimizer()
    assert isinstance(opt._compression_history, deque)
    assert opt._compression_history.maxlen == 1000


def test_priority_indicators_are_frozensets():
    """Hot path uses substring check; frozenset allows faster membership."""
    for v in TokenOptimizer.PRIORITY_INDICATORS.values():
        assert isinstance(v, frozenset)


def test_shared_registry_singleton():
    a = get_shared_registry()
    b = get_shared_registry()
    assert a is b


def test_skill_discovery_uses_shared_registry():
    sd1 = SkillDiscovery()
    sd2 = SkillDiscovery()
    assert sd1.registry is sd2.registry
    assert isinstance(sd1.registry, SkillRegistry)


def test_skill_discovery_history_bounded():
    sd = SkillDiscovery()
    assert isinstance(sd._discovery_history, deque)
    assert sd._discovery_history.maxlen == 1000


def test_skill_registry_independent_construction_still_works():
    """Backwards-compat: explicit SkillRegistry() returns a fresh object."""
    r = SkillRegistry()
    s = get_shared_registry()
    assert r is not s
    # Both should be SkillRegistry instances
    assert isinstance(r, SkillRegistry)
    assert isinstance(s, SkillRegistry)
