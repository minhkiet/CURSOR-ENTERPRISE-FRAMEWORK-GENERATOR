# Cursor Framework Workflow

Single entry point for the 4-stage pipeline:

```
ask(request)
   ↓
[1] Indexer.scan()           — 1st call only, lazy, cached
   ↓
[2] SkillDiscovery.detect()  — find relevant skills by keywords
   ↓
[3] load_skill_file()        — mtime cache (Phase 2)
   ↓
[4] TokenOptimizer.compress() — fit within max_tokens budget
   ↓
[5] MemoryManager.store()    — HOT tier (1h TTL)
   ↓
[6] MemoryStore.save()       — atomic JSON write to disk
   ↓
WorkflowResult { context, from_cache, hits, misses, asset_count }
```

## Quick start

```python
from cursor_framework import Workflow

wf = Workflow(
    root=".cursor",
    memory_path=".cache/memory.json",
    max_tokens=4000,
    max_skills=5,
)

result = wf.ask("redesign landing page for our SaaS")
print(result.context.text)        # the prompt-ready context
print(result.context.tokens)      # estimated tokens
print(result.from_cache)          # True if cached, False if rebuilt

# Stats for dashboard
wf.stats()
# {'restored_entries': 2, 'memory_entries': 2, 'memory_hits': 5,
#  'memory_misses': 3, 'tokens_saved': 0, 'assets_indexed': 572,
#  'cache_files': 3}

# Warm up at startup to surface asset count
wf.warm()
```

## What survives process restart

Persisted to `memory_path`:
- All `MemoryEntry` objects (keys, values, metadata, stats)
- Schema-versioned JSON, atomic write

NOT persisted (rebuilt on demand):
- The lazy asset `Indexer` (rebuilt on first ask)
- The skill file mtime cache (rebuilt on first load)

## Token economics

- **Without Workflow:** every agent call re-reads skill files, parses them, no compression.
- **With Workflow:**
  - First call: scan (2s) + detect + load + compress → budgeted context.
  - Repeat call (same session): cache hit → instant.
  - Repeat call (post-restart): key lookup hits, value rebuilds (cheap).

## Module map

| Module | Phase | Role |
|---|---|---|
| `indexer` | 1 | Scan `.cursor/` → INDEX.json + INDEX.md |
| `skill_discovery` | 2 | Detect relevant skills + mtime cache |
| `token_optimizer` | 3 | Compress context to fit budget |
| `memory_manager` + `memory_store` | 4 | Persist memory across sessions |
| `workflow` | 5 | Orchestrate all four |

All in `cursor_framework/`. Single import: `from cursor_framework import Workflow`.