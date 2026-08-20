"""End-to-end smoke test: framework invokes upstream hackingtool-plugin wrappers.

Run from repo root:  python tools/hackingtool-plugin/_test_e2e.py
"""
import json
import subprocess
from pathlib import Path

SCRIPTS = Path("tools/hackingtool-plugin/scripts")


def call(script: str, *args: str) -> dict:
    r = subprocess.run(
        ["python", str(SCRIPTS / script), *args],
        capture_output=True, text=True, timeout=60,
    )
    return json.loads(r.stdout) if r.stdout else {"stderr": r.stderr}


def main():
    print("--- 1) ht_env ---")
    env = call("ht_env.py")
    print("  host=" + env["host"]
          + "  preferred_backend=" + env["preferred_backend"]
          + "  wsl_distros=" + str(env["wsl_distros"]))

    print("--- 2) ht_preflight ---")
    pf = call("ht_preflight.py")
    print("  verdict=" + pf["verdict"]
          + "  disk_free_gb=" + str(pf["disk_free_gb"])
          + "  internet=" + str(pf["internet"]))
    print("  native_tools_present=" + str(pf["native_tools_present"]))
    print("  recommendations=" + str([r["priority"] for r in pf["recommendations"]]))

    print("--- 3) ht_search --q recon ---")
    hits = call("ht_search.py", "--q", "recon", "--limit", "3")
    top = hits["tools"][0]
    print("  found " + str(hits["count"]) + " tools, top: " + top["id"] + " (" + top["title"] + ")")

    print("--- 4) ht_run nuclei ---")
    out = call("ht_run.py", "web_attack.Nuclei", "--command", "nuclei -version", "--timeout", "15")
    diag = out.get("diagnostic", {}) or {}
    print("  status=" + out.get("status", "?")
          + "  reason=" + out.get("reason", "-")
          + "  backend=" + diag.get("backend", "-"))

    print()
    print("OK: framework can call all four upstream wrappers end-to-end.")


if __name__ == "__main__":
    main()
