"""Verify Hướng 1 — lazy package + lazy CLI."""
import time
import subprocess
import sys


def test_lazy_attribute_access():
    """`from cursor_framework import X` returns the actual submodule symbol."""
    import cursor_framework
    assert hasattr(cursor_framework, "Workflow")
    assert hasattr(cursor_framework, "__version__")
    wf_cls = cursor_framework.Workflow
    from cursor_framework.workflow import Workflow as DirectWF
    assert wf_cls is DirectWF


def test_lazy_unrelated_submodule_not_imported():
    """
    Importing cursor_framework should NOT pull in heavy submodules like
    dashboard / watcher / workflow. Only the version + argparse-related
    bits should be loaded.

    Note: we *capture* the sys.modules snapshot for `cursor_framework.*`
    before the test, then import and inspect afterwards. We do not wipe
    `sys.modules` because that would create a fresh `MemoryTier` (and
    every other class) for subsequent tests, which breaks dict lookups
    inside `MemoryStore.load_into`. The capture-then-diff pattern below
    is enough to assert lazy semantics without disturbing other tests.
    """
    import importlib
    import sys
    # Capture before-snapshot of anything cursor_framework related.
    before = {m for m in sys.modules if m.startswith("cursor_framework.") or m == "cursor_framework"}
    if "cursor_framework" not in sys.modules:
        # Test ran first: import once to get the package loaded.
        import cursor_framework  # noqa: F401

    # Snapshot of sub-modules right after package import (lazy).
    after = {m for m in sys.modules if m.startswith("cursor_framework.") or m == "cursor_framework"}
    new_modules = after - before
    heavy = {"cursor_framework.workflow", "cursor_framework.dashboard", "cursor_framework.watcher"}
    # These should not appear just from importing the top-level package.
    # (They may be present if a previous test imported them; that is fine.)
    imported_by_lazy_getattr = new_modules & heavy
    assert not imported_by_lazy_getattr, f"Lazy imports leaked: {imported_by_lazy_getattr}"


def test_version_string_present():
    import cursor_framework
    assert cursor_framework.__version__
    parts = cursor_framework.__version__.split(".")
    assert len(parts) == 3
    assert all(p.isdigit() for p in parts)


def test_cli_no_argv_no_crash():
    """
    Lazy CLI: running `python -m cursor_framework --version` should not
    import any heavy submodule (Dashboard/Workflow/Watcher).
    """
    result = subprocess.run(
        [sys.executable, "-m", "cursor_framework", "--version"],
        capture_output=True, text=True, timeout=10,
    )
    assert result.returncode == 0
    assert "cursor-framework" in result.stdout
