---
name: hackingtool
description: Pentesting and OSINT bridge to AKCodez/hackingtool-plugin (183 tools from Z4nzu/hackingtool). Use when the user asks to recon a target, scan a network, enumerate subdomains, investigate a username or email, test a web app, check for leaked secrets, do authorized pentest, red-team, OSINT, or any task matching `pentest`, `osint`, `recon`, `nmap`, `nuclei`, `sherlock`, `amass`, `subfinder`, `httpx`, `maigret`, `holehe`, `trufflehog`, `sqlmap`, `impacket`, `netexec`, `hashcat`, `aircrack`. Wraps the upstream wrappers with framework gates (karpathy-pre, sec-pre, sec-post). Always requires explicit authorization before running any active scan or attack tool.
---

# Pentest / OSINT — Framework Bridge

This skill **wraps** [AKCodez/hackingtool-plugin](https://github.com/AKCodez/hackingtool-plugin) (183+ tools from Z4nzu/hackingtool) and adds the Cursor Enterprise Framework gates. The upstream Python wrappers (`ht_env.py`, `ht_preflight.py`, `ht_search.py`, `ht_run.py`, `ht_index.py`) live in this repo at `tools/hackingtool-plugin/scripts/` and are **kept verbatim** — see `tools/hackingtool-plugin/SYNC.md`.

> **The skill is a thin router. The actual execution logic is in the upstream scripts. Read them once, trust them, call them.**

---

## ⚠️ Authorization gate (MUST run before any active scan)

Before **any** tool that sends packets to a target (`nmap`, `nuclei`, `ffuf`, `sqlmap`, `wafw00f`, `subfinder`, `amass`, `httpx`, `katana`, `masscan`, `rustscan`, `gobuster`, `dirb`, `dirsearch`, `feroxbuster`, `nikto`, `skipfish`, `sublist3r`, `testssl`, `dnstwist`, `evilginx`, all wireless/DoS/phishing tools, etc.), confirm authorization. Do NOT skip this gate, even if the user just said "scan X".

```
──── Authorization check ──────────────────────
Before running <tool> against <target>, I need confirmation of one of:

  A) You own/operate <target> and authorize the scan.
  B) You have written permission (bug bounty, pentest contract, CTF).
  C) It's a lab / your own machine / a CTF range (HackTheBox, TryHackMe, DVWA).
  D) The tool is fully passive / OSINT-only (no packets to target).

If none of the above, I will not run the tool.
─────────────────────────────────────────────────
```

If authorization is unclear, **stop and ask**. Do not "just try with low intensity".

Passive-only tools (no packets to target) skip the gate: `Sherlock`, `Maigret`, `Holehe`, `theHarvester`, `Infoga`, `Knockmail`, `SocialScan`, `Hash Buster`, `Amass intel` (passive mode), `dnstwist` (without resolving), `TruffleHog`/`Gitleaks` on local repos.

---

## Pre-Review Gate (before calling any wrapper)

### K.1 Pick the right tool, don't guess

If you cannot name the tool id, run search first. Never hardcode a binary name — ids are namespaced (`web_attack.Nuclei`, not `Nuclei`).

### K.2 Map ask → workflow, not tool-by-tool

Use the named playbooks in `tools/hackingtool-plugin/skills/pentest/reference/workflows.md`. The 11 workflows cover ~95% of pentest/OSINT asks. Don't reinvent.

### K.3 Preflight once per session, not per tool

```bash
python tools/hackingtool-plugin/scripts/ht_preflight.py
```

If verdict is `blocked`, surface the recommendations and stop — **don't** substitute manual `curl`/`Invoke-WebRequest` probes for a missing tool (this misleads the user about coverage and is explicitly called out as an anti-pattern in the upstream skill).

### K.4 karpathy-coding overlay

- **State assumptions**: if the user's target is ambiguous, ask. Never pick a target silently.
- **Simplicity first**: don't compose 5 tools when 2 cover the ask.
- **Surgical changes**: only modify `data/tools.json` if upstream adds tools (use `ht_index.py`); never edit it by hand.
- **Goal-driven**: define "done" per ask — "found 3+ live subdomains with HTTP 200" is better than "ran subfinder".

---

## Execution (framework gate)

The framework does NOT reimplement the runner. It dispatches to the upstream wrapper:

```bash
# Find tool id
python tools/hackingtool-plugin/scripts/ht_search.py --q "<keyword>" --limit 5

# Execute
python tools/hackingtool-plugin/scripts/ht_run.py <tool_id> --args "<args>"
# or, when run_commands is empty:
python tools/hackingtool-plugin/scripts/ht_run.py <tool_id> --command "<full command>"
```

Backend flags (`--network-host`, `--privileged`, `--force`, `--timeout`, `--backend`, `--docker-image`) pass through unchanged. Read the help once: `python tools/hackingtool-plugin/scripts/ht_run.py --help`.

### Pass-through helpers

For convenience, the framework exposes the same wrappers via short Python:

```python
from pathlib import Path
import subprocess, json

ROOT = Path("tools/hackingtool-plugin/scripts")

def ht_search(q: str, **filters) -> list[dict]:
    argv = [str(ROOT / "ht_search.py"), "--q", q]
    for k, v in filters.items():
        argv += [f"--{k.replace('_', '-')}", str(v)]
    return json.loads(subprocess.check_output(argv))["tools"]

def ht_run(tool_id: str, command: str = None, args: str = None, **flags) -> dict:
    argv = [str(ROOT / "ht_run.py"), tool_id]
    if command: argv += ["--command", command]
    if args:    argv += ["--args", args]
    for k, v in flags.items():
        flag = f"--{k.replace('_', '-')}"
        argv += [flag] if isinstance(v, bool) and v else [flag, str(v)]
    return json.loads(subprocess.check_output(argv))
```

Use them only when you need to compose inside Python — for one-off scans, Bash is fine.

---

## Post-Review Gate (after every wrapper call)

### K.5 Parse the JSON status honestly

| `status`         | Action                                                         |
|------------------|----------------------------------------------------------------|
| `ok`             | Summarize stdout highlights. Quote 3-5 lines, not 300.         |
| `error`          | Read stderr, decide retry vs report. Don't paraphrase command. |
| `fallback`       | Apply the template from `runtime-fallbacks.md` for `reason`.   |
| `timeout`        | Raise `--timeout` or chunk the scan. Partial output is gold.   |
| `no_backend`     | Surface `ht_preflight.py` recommendations verbatim.            |

### K.6 Surface fallback blocks, don't hide them

If `ht_run.py` returns `status: fallback`, the runtime-fallbacks template exists for that exact reason. **Show the block to the user.** Don't paraphrase, don't abbreviate, don't say "you can try installing it".

### K.7 Reference, don't duplicate

The full workflows and fallback templates are already documented upstream. Link them, don't restate:

- Workflows: `tools/hackingtool-plugin/skills/pentest/reference/workflows.md`
- Fallbacks:  `tools/hackingtool-plugin/skills/pentest/reference/runtime-fallbacks.md`
- Sync / refresh: `tools/hackingtool-plugin/SYNC.md`

### K.8 Don't drift from upstream

If you find yourself wanting to edit `ht_run.py`, `ht_search.py`, or `ht_preflight.py`: **stop**. Open a PR against `AKCodez/hackingtool-plugin` instead. This folder is a vendor drop — see `SYNC.md`.

---

## When this skill does NOT apply

- Pure web-app code review with no live scan → use `sec_security-review` instead.
- Threat modeling / architecture security review → `sec_security-review`.
- Asking how to harden a config → `sec_security-review`.
- Cloud security policy as code (Terraform/AWS) → `sec_security-review` + cloud rules.
- Reverse engineering without execution intent → use the `reverse-engineering` skill family in `.cursor/skills/reverse-skill/`.

This skill is **for running real tools against real (or simulated) targets**. If you're not running a tool, you don't need this skill.

---

## References

- `tools/hackingtool-plugin/scripts/ht_preflight.py` — capability check (run first)
- `tools/hackingtool-plugin/scripts/ht_search.py` — discover tool ids
- `tools/hackingtool-plugin/scripts/ht_run.py` — execute
- `tools/hackingtool-plugin/skills/pentest/reference/workflows.md` — 11 named playbooks
- `tools/hackingtool-plugin/skills/pentest/reference/runtime-fallbacks.md` — fallback templates
- `tools/hackingtool-plugin/SYNC.md` — how to refresh from upstream
- Upstream: <https://github.com/AKCodez/hackingtool-plugin>
- Tool index source: <https://github.com/Z4nzu/hackingtool>

> **For authorized security testing, bug bounty, CTFs, and research only.**
