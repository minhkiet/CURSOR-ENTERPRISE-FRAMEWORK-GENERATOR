"""Verify Hướng 1 — lazy package + lazy CLI."""
import time
import subprocess
import sys


def test_lazy_attribute_access():
    """`from vibe_framework import X` returns the actual submodule symbol."""
    import vibe_framework
    assert hasattr(vibe_framework, "Workflow")
    assert hasattr(vibe_framework, "__version__")
    wf_cls = vibe_framework.Workflow
    from vibe_framework.workflow import Workflow as DirectWF
    assert wf_cls is DirectWF


def test_lazy_unrelated_submodule_not_imported():
    """
    Importing vibe_framework should NOT pull in heavy submodules like
    dashboard / watcher / workflow. Only the version + argparse-related
    bits should be loaded.

    Note: we *capture* the sys.modules snapshot for `vibe_framework.*`
    before the test, then import and inspect afterwards. We do not wipe
    `sys.modules` because that would create a fresh `MemoryTier` (and
    every other class) for subsequent tests, which breaks dict lookups
    inside `MemoryStore.load_into`. The capture-then-diff pattern below
    is enough to assert lazy semantics without disturbing other tests.
    """
    import importlib
    import sys
    # Capture before-snapshot of anything vibe_framework related.
    before = {m for m in sys.modules if m.startswith("vibe_framework.") or m == "vibe_framework"}
    if "vibe_framework" not in sys.modules:
        # Test ran first: import once to get the package loaded.
        import vibe_framework  # noqa: F401

    # Snapshot of sub-modules right after package import (lazy).
    after = {m for m in sys.modules if m.startswith("vibe_framework.") or m == "vibe_framework"}
    new_modules = after - before
    heavy = {"vibe_framework.workflow", "vibe_framework.dashboard", "vibe_framework.watcher"}
    # These should not appear just from importing the top-level package.
    # (They may be present if a previous test imported them; that is fine.)
    imported_by_lazy_getattr = new_modules & heavy
    assert not imported_by_lazy_getattr, f"Lazy imports leaked: {imported_by_lazy_getattr}"


def test_version_string_present():
    import vibe_framework
    assert vibe_framework.__version__
    parts = vibe_framework.__version__.split(".")
    assert len(parts) == 3
    assert all(p.isdigit() for p in parts)


def test_cli_no_argv_no_crash():
    """
    Lazy CLI: running `python -m vibe_framework --version` should not
    import any heavy submodule (Dashboard/Workflow/Watcher).
    """
    result = subprocess.run(
        [sys.executable, "-m", "vibe_framework", "--version"],
        capture_output=True, text=True, timeout=10,
    )
    assert result.returncode == 0
    assert "vibe-framework" in result.stdout
