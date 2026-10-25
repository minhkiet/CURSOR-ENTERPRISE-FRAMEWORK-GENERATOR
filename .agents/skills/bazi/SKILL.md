---
name: bazi
description: >
 确定性四柱八字排盘 + 证据优先的传统命理分析。Bằng cách chạy `python
 tools/bazi-plugin/scripts/calculate_bazi.py` (vendored lunar_python 1.4.8)
 để có calendar-derived facts (四柱、十神、藏干、大运、流年、干支关系) rồi
 load theo nhu cầu từ `tools/bazi-plugin/references/` để suy luận có nguồn gốc.
 Use this skill whenever user asks for 八字、四柱、命盘、算命、排盘、批命、
 流年、大运、事业财运、婚姻子女、健康倾向、Bazi、Four Pillars、fortune
 telling, hoặc cung cấp ngày giờ sinh yêu cầu phân tích. Triggers (zh):
 算八字、看八字、批八字、排八字、四柱、命盘、算命、命理、运势、大运、流年.
 Triggers (vi/en): bazi, bazi analysis, four pillars, birth chart, fortune.
 Even when user only mentions "算命"/"八字" without explicit skill ask, use this.
---

# Bazi (八字) — Framework Bridge

This skill **wraps** [guojiahh/bazi-analysis-skill](https://github.com/guojiahh/bazi-analysis-skill)
and reuses the existing prompt-time references in `.cursor/skills/special_bazi/`.
The upstream deterministic calculator (`scripts/calculate_bazi.py`) and
references (`references/`) live in this repo at `tools/bazi-plugin/` and are
**kept verbatim** — see `tools/bazi-plugin/SYNC.md` for the sync protocol.

> **The skill is a thin router.** Calculation = upstream Python.
> Reasoning = upstream references + `.cursor/skills/special_bazi/references/`.
> LLM role = synthesize, falsify, and bound uncertainty. **Never** re-derive
> the day pillar, major luck cycles, or jieqi boundaries from memory.

## Three-layer model (mirror upstream)

```
┌─────────────────────────────────────────────────────────────────────┐
│ Layer 1 — Deterministic calculator                                  │
│   tools/bazi-plugin/scripts/calculate_bazi.py  (vendored lunar_python)│
│   Output: four_pillars, day_master, hidden_stems, ten_gods,        │
│           element_profile (heuristic), natal_relations,            │
│           luck_cycles, target_year, derived_palaces                 │
├─────────────────────────────────────────────────────────────────────┤
│ Layer 2 — Knowledge (load on demand)                                │
│   tools/bazi-plugin/references/                                    │
│     calculation-conventions · reasoning-protocol · domain-rules     │
│     temporal-reasoning · classical-texts · consultation-output      │
│     worked-examples · benchmark-protocol · wuxing-tables            │
│     shichen-table · dayun-rules                                     │
│   .cursor/skills/special_bazi/references/   (prompt-time fallback)  │
│     wuxing-tables · shichen-table · dayun-rules · classical-texts  │
├─────────────────────────────────────────────────────────────────────┤
│ Layer 3 — LLM synthesis                                             │
│   Synthesize (1) and (2); explicitly distinguish:                  │
│     (a) chart facts (cannot disagree with calculator),              │
│     (b) structural reading (classical interpretation, bounded),     │
│     (c) conditional inference (requires facts beyond chart),        │
│     (d) practical advice (real-world, not deterministic).           │
│   Always cite the strongest counter-evidence; downgrade confidence. │
└─────────────────────────────────────────────────────────────────────┘
```

## Pre-Review Gate (run once per session)

### K.1 Preflight before any analysis

```bash
python tools/bazi-plugin/scripts/bazi_status.py
```

If `ok: false`, **stop** and surface the `actions[]` block. Do not
substitute LLM-only inference for the deterministic chart — that is the
exact failure mode upstream explicitly warns against (see upstream
`SKILL.md` §"严禁凭记忆心算日柱、大运或节气交界").

### K.2 Map the ask to a task mode, not a free-form essay

| Mode | Trigger | Read |
|---|---|---|
| **A. Full consultation** | user wants the whole chart + multi-domain read | `calculation-conventions.md`, `reasoning-protocol.md`, `domain-rules.md`, `temporal-reasoning.md`, `consultation-output.md` |
| **B. Focused consultation** | one domain (career / wealth / relationship / health / study / year) | the matching section of `domain-rules.md` only |
| **C. Year / event window** | specific year or "should I switch jobs in 2026–2027" | `temporal-reasoning.md` + `calculation-conventions.md` |
| **D. Benchmark / MCQ** | given chart + multiple-choice, often historical | `benchmark-protocol.md` (do **not** leak answers; isolate context) |

### K.3 Minimal information principle (mirror upstream)

Collect only what is required for the current question. Do not re-ask what
the user already provided. Default day boundary = 晚子换日; only ask for
true-solar longitude when birth time is near a jieqi or shichen boundary.

### K.4 karpathy-coding overlay

- **State assumptions**: gender, calendar, day-boundary — all assumptions
  belong in the answer header, not silently in the chart.
- **Simplicity first**: if the user only asked "is 2026 good for changing
  jobs", do not produce a 2,000-word full chart essay.
- **Surgical changes**: only edit `tools/bazi-plugin/scripts/` or
  `tools/bazi-plugin/references/` when upstream releases a new version
  (see `SYNC.md`). Never hand-edit `data/tools.json`-style manifests.
- **Goal-driven**: "done" = calculator JSON returned + answer cites both
  supporting and counter evidence with a confidence band.

## Execution (framework gate)

The framework does **not** reimplement the calculator. It dispatches:

```bash
# Default solar chart
python tools/bazi-plugin/scripts/calculate_bazi.py \
  --date 1990-05-15 --time 14:30 --gender female \
  --target-year 2026 --compact

# Lunar input with leap month
python tools/bazi-plugin/scripts/calculate_bazi.py \
  --date 1990-04-21 --time 14:30 --calendar lunar --leap \
  --gender female --compact

# Civil-midnight day boundary
python tools/bazi-plugin/scripts/calculate_bazi.py \
  --date 1990-05-15 --time 23:30 --gender male \
  --day-boundary civil-midnight --compact

# True-solar correction (longitude + UTC offset)
python tools/bazi-plugin/scripts/calculate_bazi.py \
  --date 1990-05-15 --time 14:30 --gender female \
  --longitude 104.07 --utc-offset 8 --compact
```

Pass `--help` once: `python tools/bazi-plugin/scripts/calculate_bazi.py --help`.

### Pass-through helpers (optional, for in-Python composition)

```python
from pathlib import Path
import json, subprocess

ROOT = Path("tools/bazi-plugin/scripts")

def bazi_calc(**flags) -> dict:
    argv = [str(ROOT / "calculate_bazi.py")]
    for key, value in flags.items():
        argv += [f"--{key.replace('_', '-')}", str(value)]
    argv += ["--compact"]
    return json.loads(subprocess.check_output(argv))

def bazi_status() -> dict:
    return json.loads(
        subprocess.check_output([str(ROOT / "bazi_status.py")])
    )
```

Use them only when composing inside Python; for one-off charts the Bash
calls above are fine.

## Post-Review Gate (after every chart call)

### K.5 Read the JSON honestly

- `conventions` block must be echoed in the answer header (year_boundary,
  month_boundary, day_boundary, primary_luck_start_method).
- `element_profile` is a **heuristic triage**, not a final 旺衰/喜忌 ruling.
  Always surface its `warning` string verbatim.
- `luck_cycles.primary` is the main answer; `alternative` is shown for
  school-of-thought divergence.
- `target_year` may be `null` — do not invent one.

### K.6 Surface the strongest counter-evidence

For every structural claim, list at least one counter-evidence
(空亡、冲合刑害、被反吟、节气差). If the counter-evidence is fatal,
downgrade confidence or change the conclusion. Do not search for
supporting evidence only.

### K.7 Reference, don't duplicate

- Calculator & test: `tools/bazi-plugin/scripts/calculate_bazi.py` +
  `tools/bazi-plugin/scripts/test_calculate_bazi.py`
- Reasoning & domain knowledge: `tools/bazi-plugin/references/*.md`
- Prompt-time tables (lightweight fallback when no chart available):
  `.cursor/skills/special_bazi/references/*.md`
- Sync protocol: `tools/bazi-plugin/SYNC.md`
- Upstream home: <https://github.com/guojiahh/bazi-analysis-skill>

### K.8 Don't drift from upstream

If you find yourself wanting to edit `calculate_bazi.py`, the vendored
`lunar_python/`, or `references/*.md` in `tools/bazi-plugin/`: **stop**.
This folder is a vendor drop — see `SYNC.md`.

## High-risk topics (mirror upstream)

- **Health**: traditional image only, never diagnose or predict death.
  Refer to professional medical advice.
- **Finance / career**: no leverage / all-in recommendations.
- **Marriage / fertility**: never assert infertility, affairs, divorce,
  or sexual orientation from a chart. Describe patterns and pressure
  windows only.
- **Disaster / legal risk**: avoid fear language; use risk management
  framing and practical advice.

## When this skill does NOT apply

- Pure psychological / life coaching with no birth data → use a generic
  chat mode; this skill is for factual + traditional chart work.
- Bazi MCQ benchmark with answer leakage risk → still use this skill,
  but load `references/benchmark-protocol.md` first and isolate context.
- Other cultural systems (紫微, 西洋占星, 塔罗) → different skills.

## References

- Calculator: `tools/bazi-plugin/scripts/calculate_bazi.py`
- Tests: `tools/bazi-plugin/scripts/test_calculate_bazi.py`
- Preflight: `tools/bazi-plugin/scripts/bazi_status.py`
- Upstream references: `tools/bazi-plugin/references/*.md`
- Sync protocol: `tools/bazi-plugin/SYNC.md`
- Prompt-time fallback: `.cursor/skills/special_bazi/SKILL.md` +
  `.cursor/skills/special_bazi/references/*.md`
- Upstream home: <https://github.com/guojiahh/bazi-analysis-skill>

> 本技能用于传统文化研究与娱乐参考。Benchmark 模式仍可选择最符合传统
> 命理规则的选项，但不得把该选择包装成科学事实。
