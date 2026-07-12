# Cursor Enterprise Framework Generator

> A cross-IDE framework for AI coding agents — built around **Memory First**, **Retrieval First**, **Token Optimization**, and **Knowledge Reuse**.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Latest Release](https://img.shields.io/badge/release-v1.3.0-blue)](https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/releases)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

---

## What is it?

**Cursor Enterprise Framework (CEF)** is a drop-in `.cursor/` configuration that turns any AI coding agent — Cursor, Claude Code, Windsurf, Cline, Roo Code, Vibe Code — into a context-aware, token-efficient, memory-backed senior developer.

Instead of starting every session from zero, the framework:

1. **Routes requests** to the right domain knowledge via a `ContextRouter`.
2. **Stores decisions and bug history** in a SQLite-backed memory layer.
3. **Reuses prompts and skills** from a curated skill library.
4. **Compresses and caches** token-heavy context automatically.

## What's in the box

| Component | Files | Where |
|---|--:|---|
| Rules (`.mdc`) | 42 | `.cursor/rules/` |
| Skills | 50 | `.cursor/skills/` |
| Python library (`cursor_framework`) | 14 modules + 6 utils | `cursor_framework/` |
| Vue.js dashboard | Vue 3 + Vite + Tailwind | `cursor_framework_web/` |
| Demo projects | 5 (CRM, fitness, food-delivery, realestate, travel) | `demos/` |
| Windows GUI installer (built) | `cursor-setup.exe` (~162 MB), `cursor-setup.zip` (~22 MB) | `dist/` |
| PowerShell / CMD installers | 5 scripts | root |

The framework ships **605+ files** inside `cursor-setup.zip` (the actual `.cursor/` payload). Repo source counts higher because of demos and build artifacts.

## Architecture

```
.cursor/                        # Framework config (installed to ~/.cursor/)
├── rules/                      # 42 .mdc rule files
├── skills/                     # 50 specialized skill folders
├── memory/                     # SQLite memory layer
├── knowledge/                  # Domain knowledge base
├── prompts/                    # Prompt templates
├── workflows/                  # Standard workflows
├── templates/                  # Project templates
├── commands/                   # Slash commands
├── hooks/                      # Lifecycle hooks
└── agents/                     # Agent personas

cursor_framework/               # Python library
├── context_router.py           # Intent → skill routing
├── memory_manager.py           # Memory tier manager
├── memory_store.py             # SQLite-backed store with size cap
├── token_optimizer.py          # Token compression
├── skill_discovery.py          # Auto skill detection + cache
├── rules_parser.py             # .mdc parser
├── skills_parser.py            # Skill def parser
├── workflow.py                 # Workflow engine
├── indexer.py                  # Builds .cursor/INDEX.json
├── integration.py              # Cross-module glue
├── context_builder.py          # Builds full context for LLM
├── watcher.py                  # Auto-reload on file changes
├── dashboard.py                # Streamlit dashboard
└── utils/                      # text / file / code / http / security

cursor_framework_web/           # Vue 3 dashboard
├── src/{views,components,composables}/
└── package.json (vue, vite, vue-router, motion, jszip)

cursor-setup-gui/               # C# WinForms GUI installer
├── SetupForm.cs                # 1600 LOC, per-category picker
└── Lang.cs / LangItem.cs       # i18n (en/vi)

demos/                          # Reference projects
├── crm/  fitness/  food-delivery/  realestate/  travel/
```

## Installation

Three ways to install — pick whichever fits your environment.

### Option 1: Windows GUI (recommended for first-time users)

1. Download both files from the [latest release](https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/releases):
   - `cursor-setup.exe` (self-contained, no .NET required)
   - `cursor-setup.zip` (framework payload, ~22 MB)
2. Place them in the same folder.
3. Double-click `cursor-setup.exe`.
4. Pick the destination folder in the GUI dialog (defaults to `%USERPROFILE%\.cursor`).
5. Click **Install**. Restart Cursor IDE.

The GUI shows progress, an extraction log, and a file-count sanity check.

### Option 2: One-liner from PowerShell

```powershell
irm https://raw.githubusercontent.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/main/install.ps1 | iex
```

Download the ZIP from GitHub, extract, and run `setup.bat` automatically. Updates:

```powershell
& {irm https://raw.githubusercontent.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/main/install.ps1} -Update
```

### Option 3: Clone + setup

```powershell
git clone https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR.git
cd "CURSOR ENTERPRISE FRAMEWORK GENERATOR"
.\setup.bat                    # install to %USERPROFILE%\.cursor
.\setup.bat --force            # overwrite existing install
.\setup.bat --gui-picker       # show folder-picker dialog
.\setup.bat --install-dir "D:\custom\.cursor"
```

Equivalent CLI installers at the repo root: `install-github.bat`, `install-github.ps1`, `quick-install.ps1`.

## Usage

### In Cursor / Claude Code / Windsurf

Once installed, just open any project. The framework auto-loads:

- **Skills** via `cursor_framework.skill_discovery` — detected from your request, loaded on demand.
- **Memory** at `~/.cursor/memory/decisions.sqlite` — previous ADRs and bug fixes are checked first.
- **Rules** in `.cursor/rules/*.mdc` — applied automatically to every request.

Example: ask *"Optimize this Entity Framework query"* and the framework will load `aspnet-core` + `sql-server` skills, skip `bazi`/`pdf`, and surface any related decisions from memory.

### As a Python library

```bash
git clone https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR.git
cd cursor-framework
pip install -e ".[all]"        # editable install from this repo
# PyPI publishing not yet available — install from source for now
```

```python
from cursor_framework import (
    ContextRouter,
    MemoryManager,
    MemoryTier,
    SkillDiscovery,
)

# Route a request to the right skill
router = ContextRouter()
route = router.route("Create a SaaS landing page with Tailwind")
print(route.skill, route.confidence)

# Store and retrieve decisions
memory = MemoryManager()
memory.store("auth_choice", {"method": "JWT", "reason": "stateless API"})
print(memory.retrieve("auth_choice"))

# Discover applicable skills for a prompt
skills = SkillDiscovery().detect_skills("Add unit tests for payment module")
for s in skills:
    print(s.skill, s.confidence)
```

Modules: `context_router`, `memory_manager`, `memory_store`, `token_optimizer`, `skill_discovery`, `rules_parser`, `skills_parser`, `context_builder`, `workflow`, `indexer`, `integration`, `watcher`, `dashboard`, `review.frontend_reviewer`. Utilities in `cursor_framework/utils/`: `text_utils`, `file_utils`, `code_utils`, `http_utils`, `security_utils`.

### Vue dashboard (development)

```bash
cd cursor_framework_web
npm install
npm run dev                     # http://localhost:5173
npm run build                   # production bundle to dist/
```

Views: Home, Learn, Prompts, Template Preview, Templates Gallery.

## Tech stack supported

- **Frontend**: Next.js 15 · React 19 · Vue 3 · Nuxt 4 · TypeScript · TailwindCSS · Shadcn/UI · Vuetify · Ant Design
- **Backend**: Laravel 12 · ASP.NET Core 9 · NestJS · NodeJS
- **Database**: PostgreSQL · MySQL · SQL Server · SQLite · Redis
- **BaaS**: Supabase (Auth, DB, Storage, Edge Functions, PGVector)
- **AI**: OpenAI · Gemini · Claude · Ollama · OpenRouter
- **RAG**: PGVector · ChromaDB · Qdrant · Weaviate
- **Workflow**: n8n · Temporal · Trigger.dev · Prefect
- **Cloud / Deploy**: Cloudflare · AWS · Azure · GCP · Docker · Kubernetes · Coolify · Vercel · Railway

## Demos

| Demo | Stack | Use as reference for |
|---|---|---|
| `demos/crm/` | Next.js + Prisma | Multi-tenant SaaS, RLS, billing |
| `demos/fitness/` | Next.js | Consumer app with dashboards |
| `demos/food-delivery/` | docs-only | Marketplace patterns (reference docs) |
| `demos/realestate/` | docs-only | Listing + search (reference docs) |
| `demos/travel/` | docs-only | Booking flows (reference docs) |

## Development

```bash
# Clone
git clone https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR.git

# Install Python deps
pip install -e ".[all]"

# Run tests (136+ tests across 2 suites)
pytest                                  # all tests with coverage

# Build the GUI installer
cd cursor-setup-gui
dotnet publish -c Release -r win-x64 --self-contained \
  -p:PublishSingleFile=true -o ../dist
```

Branch protection on `main` is active (PR + 1 approval required, status checks enforced). Releases are tagged (`v1.3.0` current); see `dist/RELEASE-NOTES-*.md` for each version.

## License

MIT — see [LICENSE on GitHub](https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/blob/main/LICENSE). *(No LICENSE file is committed in this repo at the moment — declared in `pyproject.toml` and the `setup.bat` installer banner.)*

## Versioning

- **Repo tags** (`v1.x.y`): mark repo-level milestones.
- **Framework version** (`4.x.y`, in `setup.bat`): tracks the installed `.cursor/` payload content.
- **Library version** (`pyproject.toml`): the `cursor_framework` Python package.

Current: repo `v1.3.0` · framework `4.2.0` · library `1.0.0`.
