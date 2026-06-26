# Cursor Enterprise Framework - Index

> Last updated: 2026-06-26

## Tổng quan

| Category | Count |
|----------|-------|
| Rules | 39 files |
| Skills | 17 folders |
| Knowledge | 36 dirs |
| Scripts | 12 |

## Files

| File | Type | Description |
|------|------|-------------|
| `.cursorrules` | root | Project root Cursor rules |
| `.cursor/cursor.json` | workspace | Workspace settings |

## Rules (39 files)

### Core Protocol (5)
- `skill-registry.mdc` - Single source of truth cho skills
- `skill-integration.mdc` - Skill auto-discovery và execution
- `task-analyzer.mdc` - Task analysis và context sync
- `context-router.mdc` - Smart context routing
- `memory-first.mdc` - Memory-first context management

### Architecture (4)
- `architecture-patterns.mdc` - Clean, Hexagonal, CQRS, DDD
- `enterprise-patterns.mdc` - Monolith, Microservices, Enterprise
- `cloud-infra.mdc` - Cloud Infrastructure
- `serverless.mdc` - Serverless & IaC

### Backend (5)
- `backend-frameworks.mdc` - NestJS, Laravel, ASP.NET Core
- `databases.mdc` - PostgreSQL, MySQL, SQL Server, RLS
- `redis.mdc` - Redis Cache & Caching
- `auth.mdc` - Authentication & Authorization
- `security.mdc` - Security Best Practices

### Frontend (2)
- `frontend-frameworks.mdc` - Next.js, Nuxt, Vue
- `ui-visual-design.mdc` - UI/Visual Design

### AI/ML (2)
- `llm-providers.mdc` - OpenAI, Gemini, Claude
- `ai-knowledge.mdc` - RAG, Vector Search, WeKnora

### DevOps (6)
- `deployment.mdc` - Deployment & CI/CD
- `container-orchestration.mdc` - Docker & Kubernetes
- `observability.mdc` - Monitoring & Logging
- `operations.mdc` - Alerting & Incident Response
- `performance.mdc` - Performance & Rate Limiting
- `version-control.mdc` - Git & GitHub

### Cloud (3)
- `cloud-providers.mdc` - AWS, Azure, GCP
- `cloudflare.mdc` - Cloudflare & CDN
- `api-patterns.mdc` - REST, GraphQL, API Gateway

### Enterprise (4)
- `billing.mdc` - Billing Implementation
- `crm-saas.mdc` - CRM SaaS
- `multi-tenant.mdc` - Multi-Tenant Architecture
- `workflow-engines.mdc` - n8n, Trigger.dev, Temporal

### Supporting (4)
- `coding-standards.mdc` - Coding Standards
- `cost-optimization.mdc` - Cost & Token Optimization
- `testing.mdc` - Unit, Integration, E2E, TDD
- `supabase.mdc` - Supabase

### Special (4)
- `multi-language-vibe-code.mdc` - Multi-language Processing (redirect)
- `intent-detection.mdc` - Intent Analysis & Skill Discovery
- `vibe-code-protocol.mdc` - Vibe Code Execution & Validation
- `multi-language-processing.mdc` - Translation Layer

## Skills (17 skills)

| Skill | Path |
|-------|------|
| `frontend-taste` | skills/frontend-taste/SKILL.md |
| `frontend-redesign` | skills/frontend-redesign/SKILL.md |
| `frontend-review` | skills/frontend-review/SKILL.md |
| `full-output` | skills/full-output/SKILL.md |
| `security-review` | skills/security-review/SKILL.md |
| `ponytail` | skills/ponytail/SKILL.md |
| `karpathy-coding` | skills/karpathy-coding/SKILL.md |
| `visual-explainer` | skills/visual-explainer/SKILL.md |
| `open-design` | skills/open-design/SKILL.md |
| `document-ocr` | skills/document-ocr/SKILL.md |
| `bazi` | skills/bazi/SKILL.md |
| `vietnam-payment-review` | skills/vietnam-payment-review/SKILL.md |
| `vietnam-address` | skills/vietnam-address/SKILL.md |
| `weknora-kb` | skills/weknora-kb/SKILL.md |
| `weknora-agent` | skills/weknora-agent/SKILL.md |
| `pixelrag` | skills/pixelrag/SKILL.md |
| `skill-installer` | skills/skill-installer/SKILL.md |

> **Note:** `reverse-skill/` folder chứa 57 CTF competition skills (không đếm vào 17 skills chính)

## Knowledge (36 directories)

| Category | Topics |
|----------|--------|
| **AI/ML** | ai-knowledge, claude, gemini, openai, pgvector, rag, vector-search, weknora |
| **Backend** | aspnet-core, laravel, nestjs, redis, supabase |
| **Cloud** | aws, azure, cloudflare, kubernetes |
| **Databases** | mysql, postgres, rls, sql-server |
| **Design** | design-systems, open-design, pixelrag |
| **Enterprise** | billing, crm, marketing, multi-tenant, monitoring |
| **Frontend** | nextjs, nuxt, vue |
| **Special** | bazi, docker, numerology, pdf, performance, security, tuvi |

## Scripts (12 scripts)

| Script | Purpose |
|--------|---------|
| `task-analyzer.ps1` | Task analysis & MCP |
| `setup-local.ps1` | Local setup |
| `setup-local-simple.ps1` | Simple setup |
| `skill-installer.ps1` | Install skills |
| `build-embeddings.ps1` | Vector embeddings |
| `build-memory.ps1` | Build memory |
| `compile-knowledge.ps1` | Knowledge base compiler |
| `command-registry.ps1` | Command registry |
| `packager.ps1` | Package builder |
| `build-index.ps1` | Index builder (project-index-builder) |
| `setup-mcp.ps1` | MCP setup (weknora) |

## Changelog

### 2026-06-26 v2.0
- Split `multi-language-vibe-code.mdc` (2860 lines) → 3 files:
  - `intent-detection.mdc` (741 lines)
  - `vibe-code-protocol.mdc` (1328 lines)
  - `multi-language-processing.mdc` (372 lines)
- Resolved karpathy-coding vs ponytail conflict (complementary phases)
- Cleaned 433 orphaned files from skills/
- Added `.cursorrules` at project root
- Added `.cursor/cursor.json` workspace settings
- Updated skill-dependencies.json to v1.1.0
- **Final counts:** Rules 39, Skills 17, Knowledge 36, Scripts 12

### 2026-06-26 (evening)
- **Split `multi-language-vibe-code.mdc`** into 3 modular files:
  - `intent-detection.mdc` (~550 lines) - Intent Analysis & Skill Discovery
  - `vibe-code-protocol.mdc` (~700 lines) - Vibe Code Execution & Validation
  - `multi-language-processing.mdc` (~300 lines) - Translation Layer
- Updated `multi-language-vibe-code.mdc` to redirect to new files
- Updated Rules count: 36 → 39 files

### 2026-06-26
- Updated stats: Rules 36, Skills 17, Knowledge 35, Scripts 11
- Removed `RULES-OPTIMIZATION-REPORT.md` from rules count
- Added `api-patterns.mdc` to Cloud section
- Removed obsolete skills from list
- Added `reverse-skill` note (57 CTF skills)
- Added changelog section

### 2026-06-25
- Initial INDEX.md creation
- 37 rules, 17 skills, 36 knowledge dirs, 12 scripts

## Quick Navigation

### Bắt đầu nhanh
1. Đọc `skill-registry.mdc` để hiểu skills
2. Chạy `task-analyzer.ps1` cho task mới
3. Tham khảo `coding-standards.mdc` cho code style

### Architecture
1. `architecture-patterns.mdc` - Design patterns
2. `enterprise-patterns.mdc` - System architecture
3. `cloud-infra.mdc` - Infrastructure

### Development
1. `backend-frameworks.mdc` - Backend
2. `frontend-frameworks.mdc` - Frontend
3. `databases.mdc` - Data layer
4. `testing.mdc` - Quality

### Deployment
1. `deployment.mdc` - CI/CD
2. `container-orchestration.mdc` - Containers
3. `observability.mdc` - Monitoring
