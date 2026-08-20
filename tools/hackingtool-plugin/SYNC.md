# hackingtool-plugin — Upstream Sync

This folder is a **vendor drop** of [AKCodez/hackingtool-plugin](https://github.com/AKCodez/hackingtool-plugin) (commit-pinned to `main`). The upstream scripts are stored **verbatim** under `scripts/` and the upstream skill is stored **verbatim** under `skills/pentest/`.

The Cursor Enterprise Framework bridge lives in `.cursor/skills/sec_hackingtool/` and adds framework gates — it does NOT modify anything here.

---

## Folder layout

```
tools/hackingtool-plugin/
├── .claude-plugin/plugin.json      # upstream manifest (verbatim)
├── data/tools.json                 # 183-tool index (regenerated, see below)
├── scripts/                        # upstream Python wrappers (verbatim)
│   ├── ht_env.py
│   ├── ht_preflight.py
│   ├── ht_search.py
│   ├── ht_run.py
│   ├── ht_index.py
│   └── build_readme_table.py
├── skills/pentest/                 # upstream Claude-Code skill (verbatim)
│   ├── SKILL.md
│   └── reference/
│       ├── workflows.md
│       └── runtime-fallbacks.md
└── SYNC.md                         # this file
```

The repo-level Claude marketplace manifest lives at `.claude-plugin/marketplace.json` and points at `./plugins/hackingtool` — adjust the path there if you move this folder.

---

## Refreshing from upstream

The upstream ships these scripts as **plain text**, no build step. To refresh:

```bash
# From the repo root, on Windows PowerShell
$src = "https://raw.githubusercontent.com/AKCodez/hackingtool-plugin/main/plugins/hackingtool"
$dst = "tools/hackingtool-plugin"

# 1. Refresh Python scripts
Invoke-WebRequest "$src/scripts/ht_env.py"          -OutFile "$dst/scripts/ht_env.py"
Invoke-WebRequest "$src/scripts/ht_preflight.py"    -OutFile "$dst/scripts/ht_preflight.py"
Invoke-WebRequest "$src/scripts/ht_search.py"       -OutFile "$dst/scripts/ht_search.py"
Invoke-WebRequest "$src/scripts/ht_run.py"          -OutFile "$dst/scripts/ht_run.py"
Invoke-WebRequest "$src/scripts/ht_index.py"        -OutFile "$dst/scripts/ht_index.py"
Invoke-WebRequest "$src/scripts/build_readme_table.py" -OutFile "$dst/scripts/build_readme_table.py"

# 2. Refresh skill docs
Invoke-WebRequest "$src/skills/pentest/SKILL.md" -OutFile "$dst/skills/pentest/SKILL.md"
Invoke-WebRequest "$src/skills/pentest/reference/workflows.md"          -OutFile "$dst/skills/pentest/reference/workflows.md"
Invoke-WebRequest "$src/skills/pentest/reference/runtime-fallbacks.md"  -OutFile "$dst/skills/pentest/reference/runtime-fallbacks.md"

# 3. Refresh plugin manifest
Invoke-WebRequest "$src/.claude-plugin/plugin.json" -OutFile "$dst/.claude-plugin/plugin.json"
```

On Linux/macOS, swap to `curl -fsSL -o <out> <url>` for the same effect.

### Regenerating the tool index

`data/tools.json` is **generated** from the upstream `Z4nzu/hackingtool` Python source. Two options:

1. **Use the bundled JSON** (fastest — what this folder ships): already at `data/tools.json` (~150 KB, 183 tools).
2. **Regenerate from source** (most accurate, slowest):
   ```bash
   git clone https://github.com/Z4nzu/hackingtool ../hackingtool
   python tools/hackingtool-plugin/scripts/ht_index.py \
     --hackingtool-path ../hackingtool
   ```

### One-shot refresh (Windows)

Run from repo root:

```powershell
.\tools\hackingtool-plugin\refresh.ps1
```

(`refresh.ps1` is **not** shipped — drop in the snippet above as a 5-line script if you want a one-liner. Kept out of the tree on purpose to keep files minimal.)

---

## Modifying the upstream code

**Don't.** That breaks sync. If you need a behaviour change, open a PR against `AKCodez/hackingtool-plugin` first, then refresh this folder.

If you must patch locally for an unmerged upstream fix, keep the patch in a sibling file (e.g. `scripts/ht_run.local.py`) and call it instead of `ht_run.py` from your bridge skill — do not edit `ht_run.py` in place.

---

## Quick sanity check

```bash
# Verify scripts still work standalone
python tools/hackingtool-plugin/scripts/ht_env.py
python tools/hackingtool-plugin/scripts/ht_preflight.py
python tools/hackingtool-plugin/scripts/ht_search.py --q "nuclei" --limit 3
python tools/hackingtool-plugin/scripts/ht_run.py web_attack.Nuclei --command "nuclei -version" --timeout 30
```

Each command emits JSON. `ht_run.py` will return `status: "fallback"` on hosts without Docker/WSL/native pentest tools — that's the correct, expected outcome (the upstream runtime-fallback templates tell the user what to do).
