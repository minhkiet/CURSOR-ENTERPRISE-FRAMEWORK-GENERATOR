# Cursor Framework Structure

## Directory Layout

```
cursor_framework/
├── __init__.py              # Package exports
├── __main__.py              # CLI entry: cursor-framework [serve|status]
├── dashboard.py             # Dashboard visualization
│
├── core/
│   ├── context_builder.py   # Build context from sources
│   ├── context_router.py    # Route to appropriate handlers
│   ├── workflow.py          # Workflow orchestration + caching
│   └── indexer.py           # File/code indexing
│
├── memory/
│   ├── memory_manager.py    # Memory lifecycle
│   └── memory_store.py      # Memory storage
│
├── skills/
│   ├── skill_discovery.py   # Auto-detect skills (gate system)
│   ├── skills_parser.py     # Parse .skill.md files
│   └── rules_parser.py      # Parse .cursor/rules/*.mdc
│
├── optimization/
│   ├── token_optimizer.py   # Estimate & optimize tokens
│   └── watcher.py          # File watcher for cache invalidation
│
├── utils/
│   ├── __init__.py
│   ├── code_utils.py        # Code analysis utilities
│   ├── file_utils.py        # File operations
│   ├── http_utils.py        # HTTP client
│   ├── security_utils.py    # Security helpers
│   └── text_utils.py        # Text processing
│
└── integration.py           # External integrations
```

## Module Responsibilities

| Module | Purpose |
|--------|---------|
| **skill_discovery** | Auto-detect skills từ request, execute pre/post-review gates |
| **workflow** | Orchestrate request flow, caching với ETag-based invalidation |
| **token_optimizer** | Estimate tokens (word-based), suggest optimizations |
| **watcher** | Monitor file changes → trigger cache invalidation |
| **context_builder** | Build system/user/context from multiple sources |
| **indexer** | Index code files for semantic search |
| **memory_manager** | Manage conversation memory lifecycle |
| **rules_parser** | Parse .cursor/rules/*.mdc files |

## Data Flow

```
Request → skill_discovery (detect skills)
                ↓
        context_builder (build context)
                ↓
        token_optimizer (estimate/optimize)
                ↓
        workflow (orchestrate + cache)
                ↓
        Response + Memory update
```

## Cache Strategy

- **ETag-based invalidation**: Cache key includes file mtimes
- **Watcher**: Monitors skill/rule files for changes
- **Workflow cache**: Per-request deduplication

## CLI Usage

```bash
# Start dashboard server
cursor-framework serve --port 8765

# Check status
cursor-framework status
```
