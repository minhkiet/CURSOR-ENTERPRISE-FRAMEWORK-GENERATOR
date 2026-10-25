# Bazi Plugin — Upstream Sync

This folder is a **vendor drop** of
[guojiahh/bazi-analysis-skill](https://github.com/guojiahh/bazi-analysis-skill).
The framework skill at `.cursor/skills/bazi/SKILL.md` is a thin router that
wraps it. Edit nothing in here by hand — sync from upstream instead.

## Why a vendor drop

- The deterministic calculator (`scripts/calculate_bazi.py`) depends on a
  pinned `lunar_python 1.4.8` shipped under `scripts/vendor/`. Vendoring
  guarantees the skill runs offline, the test suite stays reproducible,
  and no future pip upgrade silently changes a chart.
- The references encode the project's evidence-first reasoning protocol.
  Hand-edits drift from the upstream protocol and break the
  "thin router, vendor drop" contract that `sec_hackingtool` already
  uses for `tools/hackingtool-plugin/`.

## When to sync

| Trigger | Action |
|---|---|
| Upstream releases a new tag | `git pull` the vendor drop (see below) |
| Framework `.cursor/INDEX.md` lists a new bazi feature | cross-check upstream; sync if needed |
| A regression test fails locally | re-sync first — it usually means a vendored library drift |
| User reports a chart discrepancy vs. another tool | confirm with `bazi_status.py`; if vendor is stale, re-sync |

## How to sync (manual)

```powershell
# 1. Snapshot the current vendor drop
$backup = "tools/bazi-plugin/.sync-backup-$(Get-Date -Format yyyyMMdd-HHmmss)"
Copy-Item -Recurse tools/bazi-plugin $backup

# 2. Pull the upstream skill-main folder
$tmp = New-Item -ItemType Directory "$env:TEMP\bazi-sync-$(Get-Random)"
Invoke-WebRequest -Uri "https://codeload.github.com/guojiahh/bazi-analysis-skill/zip/refs/heads/main" -OutFile "$tmp\upstream.zip"
Expand-Archive -Path "$tmp\upstream.zip" -DestinationPath "$tmp" -Force
$src = "$tmp\bazi-analysis-skill-main\bazi-skill-main"

# 3. Replace scripts/ and references/ verbatim (do not touch the framework-added bazi_status.py)
Remove-Item -Recurse tools/bazi-plugin\scripts\calculate_bazi.py
Remove-Item -Recurse tools/bazi-plugin\scripts\test_calculate_bazi.py
Remove-Item -Recurse tools/bazi-plugin\scripts\vendor
Remove-Item -Recurse tools\bazi-plugin\references -ErrorAction SilentlyContinue
Copy-Item -Recurse "$src\scripts" tools\bazi-plugin
Copy-Item -Recurse "$src\references" tools\bazi-plugin
Copy-Item -Force "$src\LICENSE" tools\bazi-plugin
Copy-Item -Force "$src\THIRD_PARTY_NOTICES.md" tools\bazi-plugin

# 4. Re-run the regression suite + status
python tools\bazi-plugin\scripts\bazi_status.py
python -m unittest -v tools\bazi-plugin\scripts\test_calculate_bazi.py

# 5. Drop the backup if both pass
Remove-Item -Recurse $backup
```

## How to sync (scripted)

A `sync_bazi.ps1` helper can be added in a follow-up once this sync protocol
proves stable. Until then, the manual steps above are the source of truth.

## What the framework adds on top

| File | Source | Why it is OK to edit |
|---|---|---|
| `tools/bazi-plugin/scripts/bazi_status.py` | framework | thin preflight wrapper; not in upstream |
| `tools/bazi-plugin/SYNC.md` | framework | this file; not in upstream |
| `tools/bazi-plugin/scripts/calculate_bazi.py` | upstream | **do not edit** |
| `tools/bazi-plugin/scripts/test_calculate_bazi.py` | upstream | **do not edit** |
| `tools/bazi-plugin/scripts/vendor/lunar_python/` | upstream | **do not edit** |
| `tools/bazi-plugin/references/*.md` | upstream | **do not edit** |
| `tools/bazi-plugin/agents/openai.yaml` | upstream | **do not edit** |
| `tools/bazi-plugin/LICENSE`, `THIRD_PARTY_NOTICES.md` | upstream | **do not edit** |

## License

Upstream is MIT (`tools/bazi-plugin/LICENSE`). Third-party notice for the
bundled `lunar_python` is at `tools/bazi-plugin/THIRD_PARTY_NOTICES.md`.
