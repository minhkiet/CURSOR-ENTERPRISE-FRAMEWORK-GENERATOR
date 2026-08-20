# tools/

Vendor drops & third-party integrations. Each subfolder is self-contained and documents its own sync protocol.

## hackingtool-plugin/

**Vendor drop of [AKCodez/hackingtool-plugin](https://github.com/AKCodez/hackingtool-plugin) — 183+ pentest / OSINT tools (nmap, nuclei, sherlock, amass, subfinder, httpx, maigret, holehe, trufflehog, sqlmap, impacket, netexec, …).**

The upstream Python wrappers (`ht_env.py`, `ht_preflight.py`, `ht_search.py`, `ht_run.py`, `ht_index.py`, `build_readme_table.py`) and the upstream Claude-Code skill (`skills/pentest/`) are kept **verbatim**. Upstream refresh procedure: see [`hackingtool-plugin/SYNC.md`](./hackingtool-plugin/SYNC.md).

The **Cursor Enterprise Framework bridge** lives at `.cursor/skills/sec_hackingtool/SKILL.md` and wraps the upstream wrappers with framework gates (karpathy-pre, sec-pre, sec-post). Use the `/pentest` slash command (in `.cursor/commands/pentest.md`) for the full workflow.

**Authorization is mandatory** for any active scan — see the bridge skill's gate. Passive/OSINT tools skip the gate.

> For authorized security testing, bug bounty, CTFs, and research only.
