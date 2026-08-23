"""Smoke test for all cursor_framework subcommands.

Run from project root: python _smoke_test.py
"""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(r"D:\PROJECTS\CURSORS\CURSOR ENTERPRISE FRAMEWORK GENERATOR")

# Each entry is (label, command_args, timeout_sec)
# serve commands are excluded - they are blocking
TESTS = [
    ("version", ["--version"], 10),
    ("scan", ["scan", "--root", ".cursor"], 30),
    ("stats", ["stats", "--root", ".cursor"], 15),
    ("warm", ["warm", "--root", ".cursor"], 15),
    ("index", ["index", "--root", ".cursor"], 15),
    ("graph", ["graph", "--root", ".cursor"], 15),
    ("dump-graph", ["dump-graph", "--root", ".cursor"], 15),
    ("context", ["context", "--root", ".cursor"], 15),
    ("session-stats", ["session-stats", "--root", ".cursor"], 15),
    ("session-clear --force", ["session-clear", "--root", ".cursor", "--force"], 15),
    ("clear-cache --force", ["clear-cache", "--root", ".cursor", "--force"], 15),
    ("ask", ["ask", "redesign landing page", "--root", ".cursor"], 30),
]

failures = []
for label, args, timeout in TESTS:
    print(f"\n=== {label} ===")
    t0 = time.perf_counter()
    try:
        r = subprocess.run(
            [sys.executable, "-m", "cursor_framework", *args],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        elapsed = time.perf_counter() - t0
        if r.returncode == 0:
            print(f"  OK ({elapsed:.1f}s) - {len(r.stdout or '')} bytes stdout")
            if r.stderr.strip():
                print(f"  stderr: {r.stderr.strip()[:300]}")
        else:
            print(f"  FAILED exit={r.returncode} ({elapsed:.1f}s)")
            print(f"  stdout: {r.stdout[:500]}")
            print(f"  stderr: {r.stderr[:500]}")
            failures.append(label)
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT after {timeout}s")
        failures.append(label)
    except Exception as e:
        print(f"  ERROR: {e}")
        failures.append(label)

print("\n" + "=" * 60)
if failures:
    print(f"FAILURES ({len(failures)}):")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
else:
    print(f"ALL {len(TESTS)} COMMANDS PASSED")
    sys.exit(0)
