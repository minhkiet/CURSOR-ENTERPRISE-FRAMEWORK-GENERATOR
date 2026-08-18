# Cursor Enterprise Framework - Skill Index

> **Phiên bản:** 3.6.0 | **Cập nhật:** 2026-08-18
> **Total Skills:** 101+ | **Rules:** 43 | **Agents:** 18 | **Commands:** 37 | **Python Scripts:** 12+
>
> **Mới (2026-08-18):**
> - **ui-ux-pro-max** từ [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) (117k stars):
>   - 79 UI styles (Glassmorphism, Claymorphism, etc.)
>   - 192 color palettes theo industry
>   - 74 font pairings
>   - Design System Generator với 192 reasoning rules
>   - 22 tech stacks (React, Vue, SwiftUI, etc.)
>
> **Mới (2026-08-16):**
> - **agent-skills integration** từ [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (87k stars):
>   - 8 commands mới: `/spec`, `/plan`, `/build`, `/build auto`, `/test`, `/review`, `/code-simplify`, `/ship`, `/webperf`
>   - 5 skills mới: `spec-driven-development`, `planning-and-task-breakdown`, `incremental-implementation`, `test-driven-development`, `code-review-and-quality`, `code-simplification`, `debugging-and-error-recovery`
>   - Session hooks cho agent awareness

---

## Tổng quan cấu trúc

```
.cursor/
├── skills/           # 93+ skills (tự động gọi theo context)
├── agent-skills/    # 8 skills từ agent-skills
├── rules/            # 43 rules (luật theo domain)
├── agents/           # 18 agent personas (chuyên gia)
├── agent-commands/  # 8 commands từ agent-skills
├── commands/         # 29+ slash commands (workflows)
├── hooks/            # 15 hooks (CI/CD, git, dev)
├── agent-hooks/      # Session hooks cho agent awareness
├── knowledge/        # 329 knowledge bases (theo ngôn ngữ/framework)
├── workflows/         # 11 workflows (standard processes)
├── prompts/           # 31 prompts (task templates)
├── memory/            # 14 memory files (context)
├── references/       # 4 references (checklists)
└── templates/        # 6 templates (ADR, bug, feature)
```

---

## NHÓM 1: CODE & DEVELOPMENT

### 1.1 Core Coding Skills

| Skill | Path | Description |
|-------|------|-------------|
| `karpathy-coding` | `skills/karpathy-coding/` | Think before coding, simplicity, surgical changes, goal-driven execution |
| `karpathy-guidelines` | `rules/karpathy-guidelines.mdc` | Karpathy Behavioral Guidelines overlay |
| `ponytail` | `skills/ponytail/` | Lazy Senior Dev - YAGNI, minimal code |
| `full-output` | `skills/full-output/` | No skeletons, complete implementation |
| `vibe-coding` | `skills/vibe-coding/` | Vibe coding protocol với pre/post gates |

### 1.2 Code Review & Quality

| Skill | Path | Description |
|-------|------|-------------|
| `code-reviewer` | `agents/code-reviewer.md` | Senior Staff Engineer - five-axis review |
| `backend-reviewer` | `agents/backend-reviewer.md` | NestJS, Laravel, ASP.NET Core review |
| `frontend-review` | `skills/frontend-review/` | Quality gate cho frontend work |
| `database-reviewer` | `agents/database-reviewer.md` | Schema, query, indexing review |

### 1.3 Code Refactoring & Debugging

| Skill | Path | Description |
|-------|------|-------------|
| `refactor-specialist` | `agents/refactor-specialist.md` | Behavior-preserving refactoring |
| `debugger` | `agents/debugger.md` | 4-phase root-cause protocol |

### 1.4 Coding Standards Rules

| Rule | Path | Description |
|------|------|-------------|
| `coding-standards` | `rules/coding-standards.mdc` | Unified coding standards |
| `architecture-patterns` | `rules/architecture-patterns.mdc` | Clean Architecture, Hexagonal, CQRS |
| `api-patterns` | `rules/api-patterns.mdc` | REST, GraphQL, API Gateway |
| `testing` | `rules/testing.mdc` | Unit, integration, E2E, TDD |

### 1.5 Agent-Skills Development Lifecycle

**From [agent-skills](https://github.com/addyosmani/agent-skills) (87k stars)**

| Skill | Path | Description |
|-------|------|-------------|
| `spec-driven-development` | `agent-skills/spec-driven-development/` | Write specs before coding |
| `planning-and-task-breakdown` | `agent-skills/planning-and-task-breakdown/` | Break work into ordered tasks |
| `incremental-implementation` | `agent-skills/incremental-implementation/` | Build in thin vertical slices |
| `test-driven-development` | `agent-skills/test-driven-development/` | RED-GREEN-REFACTOR cycle |
| `code-review-and-quality` | `agent-skills/code-review-and-quality/` | Multi-axis code review |
| `code-simplification` | `agent-skills/code-simplification/` | Simplify for clarity |
| `debugging-and-error-recovery` | `agent-skills/debugging-and-error-recovery/` | Systematic root-cause debugging |
| `security-and-hardening` | `agent-skills/security-and-hardening/` | Security vulnerabilities & hardening |

---

## NHÓM 2: UI & VISUAL DESIGN

### 2.1 Core Design Skills

| Skill | Path | Description |
|-------|------|-------------|
| `frontend-taste` | `skills/frontend-taste/` | Anti-slop frontend cho landing/portfolio (6 pre + 8 post gates) |
| `hallmark` | `skills/hallmark/` | Anti-slop design taste (57 slop-test gates) |
| `frontend-redesign` | `skills/frontend-redesign/` | Redesign existing UI |
| `dashboard-ui` | `skills/dashboard-ui/` | Dashboard/Admin components (inputs, tables, forms, pickers) |
| `ui-designer` | `agents/ui-designer.md` | Design systems, layouts, typography |
| `ui-ux-pro-max` | `skills/ui-ux-pro-max/` | **117k stars** - 79 styles, 192 palettes, 74 fonts, 192 reasoning rules, 22 stacks |

### 2.2 Landing Page Components

#### Landing Page Sections
```
┌─────────────────────────────────────────────────────────────────┐
│ LANDING PAGE SECTIONS                                            │
├─────────────────────────────────────────────────────────────────┤
│ 1. Navigation (Sticky)     │ Header, Menu, CTA                │
│ 2. Hero                 │ Headline, Subhead, CTA, Visual    │
│ 3. Social Proof        │ Logos, Stats, Testimonials        │
│ 4. Problem/Solution    │ Pain points, How it works         │
│ 5. Features            │ Benefits, Capabilities            │
│ 6. Product Showcase    │ Demo, Gallery, Before/After      │
│ 7. Pricing             │ Plans, Comparison, FAQ           │
│ 8. Testimonials        │ Reviews, Case studies              │
│ 9. Blog/Resources      │ Posts, Guides, Downloads           │
│ 10. CTA Section       │ Final conversion push               │
│ 11. Contact/Forms     │ Lead capture, Support              │
│ 12. Footer           │ Links, Social, Legal               │
└─────────────────────────────────────────────────────────────────┘
```

#### E-commerce Components
```
┌─────────────────────────────────────────────────────────────────┐
│ E-COMMERCE                                                    │
├─────────────────────────────────────────────────────────────────┤
│ Product Card    │ Quick View    │ Cart Drawer    │ Wishlist    │
│ Category Grid │ Search       │ Filters       │ Checkout    │
│ Promo Banner  │ Newsletter   │ Trust Badges │ Social Feed │
└─────────────────────────────────────────────────────────────────┘
```

#### Auth Components
```
┌─────────────────────────────────────────────────────────────────┐
│ AUTH FORMS                                                     │
├─────────────────────────────────────────────────────────────────┤
│ Login Form   │ Register Form  │ Forgot Password │ OTP Verify  │
│ Social Login │ Password Reset │ Account Setup │ Magic Link  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Design Principles

| Rule | Path | Description |
|------|------|-------------|
| `ui-visual-design` | `rules/ui-visual-design.mdc` | Typography, color, icons, animation |
| `frontend-frameworks` | `rules/frontend-frameworks.mdc` | Next.js, Nuxt, Vue best practices |

### 2.3 Design Knowledge

| Knowledge | Path |
|-----------|------|
| Apple Design | `knowledge/design-systems/apple.md` |
| Cursor Design | `knowledge/design-systems/cursor.md` |
| Linear Design | `knowledge/design-systems/linear.md` |
| Stripe Design | `knowledge/design-systems/stripe.md` |
| Vercel Design | `knowledge/design-systems/vercel.md` |

---

## NHÓM 3: WRITING & COPY

### 3.1 Writing Skills

| Skill | Path | Description |
|-------|------|-------------|
| `ai-copywriter` | `skills/ai-copywriter/` | Humanize AI text, anti-slop (33 patterns) |
| `simple-english` | `skills/simple-english/` | Simplify to plain language |

### 3.2 Writing Principles

| Rule | Path | Description |
|------|------|-------------|
| `hallmark` | `skills/hallmark/` | Copy gates (10 rules) |

---

## NHÓM 4: DOCUMENT & KNOWLEDGE

### 4.1 Document Processing

| Skill | Path | Description |
|-------|------|-------------|
| `book-to-skill` | `skills/book-to-skill/` | Convert books/docs to agent skills |
| `document-ocr` | `skills/document-ocr/` | OCR document processing |
| `pixelrag` | `skills/pixelrag/` | Visual RAG - PDF, website, tables |

### 4.2 Knowledge Bases

| Knowledge Area | Count | Path Pattern |
|----------------|-------|--------------|
| AI/ML | 50+ | `knowledge/claude/`, `knowledge/gemini/`, `knowledge/openai/` |
| Databases | 60+ | `knowledge/postgres/`, `knowledge/mysql/`, `knowledge/supabase/` |
| Frontend | 40+ | `knowledge/nextjs/`, `knowledge/nuxt/`, `knowledge/vue/` |
| Cloud | 40+ | `knowledge/aws/`, `knowledge/azure/`, `knowledge/cloudflare/` |

### 4.3 AI & RAG

| Rule | Path | Description |
|------|------|-------------|
| `ai-knowledge` | `rules/ai-knowledge.mdc` | RAG, Vector Search, pgvector |
| `weknora-agent` | `skills/weknora-agent/` | ReAct autonomous reasoning |
| `weknora-kb` | `skills/weknora-kb/` | RAG implementation, hybrid search |

---

## NHÓM 5: OPTIMIZATION & PERFORMANCE

### 5.1 Performance Skills

| Skill | Path | Description |
|-------|------|-------------|
| `web-performance-auditor` | `agents/web-performance-auditor.md` | Core Web Vitals, bundle analysis |
| `frontend-architect` | `agents/frontend-architect.md` | SSR/SSG, state management |
| `vercel-react-best-practices` | `skills/vercel-react-best-practices/` | 40+ React perf rules |
| `vercel-composition-patterns` | `skills/vercel-composition-patterns/` | Component composition |
| `code-graph-analysis` | `skills/code-graph-analysis/` | Knowledge graph queries using Memgraph + Qdrant |

### 5.2 Performance Rules

| Rule | Path | Description |
|------|------|-------------|
| `performance` | `rules/performance.mdc` | Performance & rate limiting |
| `redis` | `rules/redis.mdc` | Caching strategy |
| `cost-optimization` | `rules/cost-optimization.mdc` | Cost & token optimization |

### 5.3 Performance References

| Reference | Path |
|-----------|------|
| Performance Checklist | `references/performance-checklist.md` |

---

## NHÓM 6: SECURITY

### 6.1 Security Skills

| Skill | Path | Description |
|-------|------|-------------|
| `security-review` | `skills/security-review/` | OWASP Top 10, ASI Top 10, supply chain |
| `sec_security-review` | `skills/sec_security-review/` | Active framework security review (OWASP, payment, AD) |
| `vietnam-payment-review` | `skills/vietnam-payment-review/` | MoMo, SePay, PayOS, ZaloPay |
| `hackingtool` | `skills/sec_hackingtool/` | **Pentest/OSINT bridge** — 183 tools (nmap, nuclei, sherlock, subfinder, maigret, sqlmap, impacket, …) via `tools/hackingtool-plugin/`. Use `/pentest` slash command. Active scan cần authorization. |

### 6.2 Security Rules

| Rule | Path | Description |
|------|------|-------------|
| `security` | `rules/security.mdc` | Security, web-security, secrets |
| `auth` | `rules/auth.mdc` | Authentication & authorization |

### 6.3 Security References

| Reference | Path |
|-----------|------|
| Security Checklist | `references/security-checklist.md` |

---

## NHÓM 7: PROJECT STRUCTURE (By Language)

### 7.1 Backend Frameworks

| Language | Rules | Knowledge |
|----------|-------|-----------|
| **NestJS** | `rules/backend-frameworks.mdc` | `knowledge/nestjs/` (7 files) |
| **Laravel** | - | `knowledge/laravel/` (7 files) |
| **ASP.NET Core** | - | `knowledge/aspnet-core/` (7 files) |
| **FastAPI** | - | `skills/fastapi-martinholovsky/` |

### 7.2 Frontend Frameworks

| Framework | Rules | Knowledge |
|-----------|-------|-----------|
| **Next.js** | `rules/frontend-frameworks.mdc` | `knowledge/nextjs/` (7 files) |
| **Nuxt.js** | - | `knowledge/nuxt/` (7 files) |
| **Vue.js** | - | `knowledge/vue/` (7 files) |

### 7.3 Databases

| Database | Knowledge |
|----------|-----------|
| **PostgreSQL** | `knowledge/postgres/` (12 files) + pgvector |
| **MySQL** | `knowledge/mysql/` (12 files) |
| **SQL Server** | `knowledge/sql-server/` (7 files) |
| **Supabase** | `knowledge/supabase/` (7 files) |

### 7.4 Cloud Providers

| Provider | Knowledge |
|----------|-----------|
| **AWS** | `knowledge/aws/` (15 files) |
| **Azure** | `knowledge/azure/` (7 files) |
| **Cloudflare** | `knowledge/cloudflare/` (7 files) |

### 7.5 Infrastructure

| Topic | Rules/Knowledge |
|-------|-----------------|
| **Container** | `rules/container-orchestration.mdc` + `knowledge/docker/` |
| **Kubernetes** | `knowledge/kubernetes/` (7 files) |
| **Serverless** | `rules/serverless.mdc` + `knowledge/aws/lambda-serverless.md` |
| **Redis** | `rules/redis.mdc` + `knowledge/redis/` (12 files) |

---

## NHÓM 8: WEB CLONING & SCRAPING

### 8.1 Web Cloning

| Skill | Path | Description |
|-------|------|-------------|
| `web-cloner` | `skills/web_cloner/` | **Prompt-first clone** — screenshot/URL → deterministic prompt. Full-site clone với site-crawler + route-discovery |
| `web-clone-ui` | `agents/web-cloner.md` | Agent persona for website cloning |
| `web-scraper` | `agents/web-scraper.md` | Extract structured content (docs, articles, tables) |
| `site-crawler` | `skills/site-crawler/` | Crawl toàn bộ site, phát hiện tất cả URLs, sitemap |
| `route-discovery` | `skills/route-discovery/` | Tìm routes cho SPA (React, Vue, Next.js) và SSR |
| `full-site-clone` | `skills/full-site-clone/` | Workflow đầy đủ: discovery → URLs → clone → full site |

### 8.2 Image Assets (Stock + AI)

| Skill | Path | Description |
|-------|------|-------------|
| `image-finder` | `skills/image-finder/` | Stock images: Unsplash, Pexels, Pravatar, DiceBear |
| `image-generator` | `skills/image-generator/` | AI generation: DALL-E 3, Flux, Stable Diffusion |
| `image-workflow` | `skills/image-workflow/` | Combined: finder → generator → web-cloner |

### 8.3 Web Design

| Skill | Path | Description |
|-------|------|-------------|
| `open-design` | `skills/open-design/` | Open Design integration |
| `landing-page-pro` | `skills/landing-page-pro/` | Build landing pages from requirements |

---

## NHÓM 9: WEB CREATION (From Requirements)

### 9.1 Web Building Skills

| Skill | Path | Description |
|-------|------|-------------|
| `frontend-taste` | `skills/frontend-taste/` | Build landing pages, portfolios |
| `frontend-redesign` | `skills/frontend-redesign/` | Redesign existing sites |
| `deploy-to-vercel` | `skills/deploy-to-vercel/` | Deploy to Vercel |

### 9.2 Web Testing

| Skill | Path | Description |
|-------|------|-------------|
| `webapp-testing` | `skills/webapp-testing/` | E2E testing với Playwright |

### 9.3 Deployment

| Skill | Path | Description |
|-------|------|-------------|
| `deployment-engineer` | `agents/deployment-engineer.md` | Vercel, Cloudflare, AWS, K8s |
| `devops-engineer` | `agents/devops-engineer.md` | CI/CD, IaC, pipelines |

---

## SLASH COMMANDS

### Development Lifecycle

| Command | Path | Description |
|---------|------|-------------|
| `/build` | `commands/build/` | Build feature mới |
| `/fix` | `commands/fix/` | Fix bug với root cause analysis |
| `/test` | `commands/test/` | Testing strategy |
| `/refactor` | `commands/refactor/` | Refactor code |
| `/review` | `commands/review/` | Code review |
| `/deploy` | `commands/deploy/` | Deployment workflow |

### Specialized

| Command | Path | Description |
|---------|------|-------------|
| `/clone` | `commands/clone/` | Clone website |
| `/frontend` | `commands/frontend/` | Frontend tasks |
| `/security` | `commands/security/` | Security review |
| `/perf` | `commands/perf/` | Performance audit |
| `/doc` | `commands/doc/` | Generate docs |
| `/generate` | `commands/generate/` | Generate code |
| `/audit` | `commands/audit/` | Security/Perf/Architecture audit |
| `/adr` | `commands/adr/` | Architecture Decision Record |
| `/workflow` | `commands/workflow/` | Execute workflows |

---

## AGENT PERSONAS

### Code Quality

| Agent | Description |
|-------|-------------|
| `code-reviewer` | Senior Staff Engineer - 5-axis review |
| `backend-reviewer` | NestJS, Laravel, ASP.NET Core |
| `database-reviewer` | Schema, query, indexing |
| `refactor-specialist` | Behavior-preserving refactor |

### Architecture

| Agent | Description |
|-------|-------------|
| `api-designer` | REST/GraphQL contracts, OpenAPI |
| `frontend-architect` | Next.js, Nuxt, Vue architecture |
| `migration-specialist` | Database, framework migrations |

### Quality Assurance

| Agent | Description |
|-------|-------------|
| `test-engineer` | Test strategy, Prove-It pattern |
| `web-performance-auditor` | Core Web Vitals, bundle |
| `debugger` | 4-phase root-cause protocol |

### Security & Operations

| Agent | Description |
|-------|-------------|
| `security-auditor` | OWASP, threat modeling |
| `deployment-engineer` | Vercel, Cloudflare, K8s |
| `devops-engineer` | CI/CD, IaC, pipelines |

### Content & Design

| Agent | Description |
|-------|-------------|
| `ui-designer` | Design systems, typography |
| `web-cloner` | Website cloning (prompt-first) |
| `web-scraper` | Content extraction |
| `marketing-strategist` | Positioning, SEO, lifecycle |
| `doc-writer` | API docs, READMEs, ADRs |

---

## NHÓM 10: KNOWLEDGE — TRADITIONAL SYSTEMS

### 10.1 Chinese Metaphysics (Bazi / Four Pillars)

| Skill | Path | Description |
|-------|------|-------------|
| `bazi` (bridge) | `skills/bazi/` | **Framework bridge** wrapping `guojiahh/bazi-analysis-skill`. Deterministic Python calculator (pinned `lunar_python 1.4.8`, vendored offline) for tứ trụ, 大运, 流年. 9 references for evidence-first reasoning. Use `/bazi` slash command. |
| `bazi` (prompt-time) | `skills/special_bazi/` | **Prompt-time fallback** with lightweight references (五鼠遁元、调候用神). Use when runtime cannot run Python or for quick general reading. |
| `bazi` (registry) | `rules/rule_skill-registry.mdc` §"bazi" | Single source of truth, two parallel skills, choose by ask. |

**Sources:**
- Upstream: [guojiahh/bazi-analysis-skill](https://github.com/guojiahh/bazi-analysis-skill) (MIT, vendored at `tools/bazi-plugin/`)
- Original prompt-time: [bazi-skill](https://github.com/jinchenma94/bazi-skill) (2k stars, MIT)

**How they differ:**

| | bridge (`bazi/`) | prompt-time (`special_bazi/`) |
|---|---|---|
| Chart calculation | `lunar_python 1.4.8` (offline) | Manual table lookup + LLM |
| Day pillar / 节气交月 | **Deterministic** | Error-prone |
| Tests | 5 regression tests | None |
| Output | JSON with full provenance | Free-form text |
| Reference loading | On-demand (3-5 files / analysis) | Often read at once |
| Best for | Real consultations, MCQ benchmarks | Quick read, no Python runtime |

**Run preflight before any analysis:**
```bash
python tools/bazi-plugin/scripts/bazi_status.py
```

---

## INTEGRATION STACKS

### Stack 1: Landing Page
```
frontend-taste + hallmark + ai-copywriter + simple-english
     ↓              ↓            ↓              ↓
 Design taste   Anti-slop    Human copy     Plain language
```

### Stack 2: Full-Stack App
```
karpathy-coding + ponytail + full-output
     ↓               ↓           ↓
 Think first    Minimal code  Complete impl
```

### Stack 3: Security Audit
```
security-review + security-auditor + auth
      ↓                ↓              ↓
  OWASP/ASI      Threat model    Auth check
```

### Stack 4: Performance
```
web-performance-auditor + vercel-react-best-practices
         ↓                         ↓
   Core Web Vitals          40+ perf rules
```

### Stack 5: Document to Skill
```
book-to-skill + simple-english + ai-copywriter
      ↓               ↓                ↓
Extract frameworks  Simplify       Humanize copy
```

### Stack 6: Web Clone & Deploy
```
web-cloner + site-crawler + route-discovery + full-site-clone + image-workflow
     ↓           ↓               ↓              ↓              ↓
   Clone UI   Find URLs     Discover      Clone all     Asset workflow
                           routes         pages
```

---

## SKILL TRIGGER MAP

### Auto-trigger by keywords

| Keywords | Auto-load Skill |
|----------|-----------------|
| landing, portfolio, homepage, SaaS | `frontend-taste` |
| redesign, improve UI | `frontend-redesign` |
| clone, copy website | `web-cloner` + `full-site-clone` |
| clone all pages, full site | `site-crawler` + `route-discovery` |
| crawl site, find URLs | `site-crawler` |
| discover routes, SPA routes | `route-discovery` |
| scrape, extract, crawl | `web-scraper` |
| tìm ảnh, find image, stock | `image-finder` |
| tạo ảnh, generate image | `image-generator` |
| security, vulnerability, OWASP | `security-review` |
| performance, optimize, Core Web Vitals | `web-performance-auditor` |
| book, document, PDF, convert | `book-to-skill` |
| copy, write, humanize | `ai-copywriter` |
| simplify, plain language | `simple-english` |
| deploy, Vercel | `deploy-to-vercel` |
| test, testing | `test-engineer` |

---

## ESSENTIAL SKILL BUNDLES

### Bundle A: Web & Dashboard
```markdown
1. ui-ux-pro-max (design system generator - 117k stars)
2. frontend-taste (anti-slop frontend)
3. hallmark (57 slop-test gates)
4. dashboard-ui (components)
5. ai-copywriter (human copy)
6. simple-english (clarity)
7. karpathy-coding (code quality)
8. ponytail (minimal code)
```

### Bundle B: Full-Stack
```markdown
1. karpathy-coding (think first)
2. full-output (complete)
3. ponytail (minimal)
4. code-reviewer (quality gate)
5. security-review (mandatory)
6. test-engineer (prove it works)
```

### Bundle C: AI/ML
```markdown
1. weknora-kb (RAG)
2. weknora-agent (autonomous)
3. pixelrag (visual docs)
4. ai-knowledge (RAG patterns)
```

### Bundle D: Database
```markdown
1. database-reviewer
2. migration-specialist
3. Supabase knowledge
4. PostgreSQL knowledge
```

### Bundle E: Infrastructure
```markdown
1. deployment-engineer
2. devops-engineer
3. cloud-providers rules
4. container-orchestration rules
```

---

## QUICK REFERENCE

### Tạo landing page
```
1. /frontend → frontend-taste activates
2. Design read (Section 0.B)
3. Set dials: VARIANCE/MOTION/DENSITY
4. Build với anti-slop rules
5. Humanize copy với ai-copywriter
```

### Clone website (single page)
```
1. /clone → web-cloner activates
2. image-workflow → analyze & source images
3. image-finder → find stock alternatives
4. image-generator → create custom images
5. Deploy với deploy-to-vercel
```

### Clone full site (all pages)
```
1. site-crawler → crawl sitemap, discover all URLs
2. route-discovery → find SPA/SSR routes
3. full-site-clone → categorize pages, identify templates
4. web-cloner → clone each page/template
5. image-workflow → source all images
6. Deploy với deploy-to-vercel
```

### Security review
```
1. /security → security-review auto-loads
2. Pre-review: threat modeling
3. Post-review: OWASP + ASI gates
4. Report với security-auditor agent
```

### Convert book to skill
```
1. book-to-skill → extract frameworks
2. simple-english → clarify concepts
3. ai-copywriter → humanize output
4. Save to .cursor/skills/
```

---

## PYTHON SCRIPT SKILLS

Các skills có thể gọi Python scripts để thực thi các tác vụ tự động:

### Design & UI

| Skill | Script | Mục đích |
|-------|--------|-----------|
| `ui-ux-pro-max` | `scripts/search.py` | Design System Generator, BM25 search, 192 reasoning rules |
| `ui-ux-pro-max` | `scripts/design_system.py` | Generate complete design system cho project |

### Data Engineering

| Skill | Script | Mục đích |
|-------|--------|-----------|
| `senior-data-engineer` | `scripts/pipeline_orchestrator.py` | Generate Airflow DAG config |
| `senior-data-engineer` | `scripts/data_quality_validator.py` | Validate data quality checks |
| `senior-data-engineer` | `scripts/etl_performance_optimizer.py` | Optimize Spark/ETL performance |
| `db_sql-server-table-reconciliation` | `scripts/reconcile.py` | Compare tables across SQL Server instances |

### Media

| Skill | Script | Mục đích |
|-------|--------|-----------|
| `youtube-downloader` | `scripts/download_video.py` | Download YouTube videos (yt-dlp) |

### Framework Tools

| Script | Mục đích |
|--------|-----------|
| `scripts/skill-installer.py` | Auto-install skill dependencies (pip/npm) |
| `scripts/ocr_tool.py` | OCR text extraction (Tesseract) |

### Bazi/命理

| Path | Script | Mục đích |
|------|--------|-----------|
| `tools/bazi-plugin/scripts/` | `calculate_bazi.py` | 四柱八字排盘 (lunar_python 1.4.8) |
| `tools/bazi-plugin/scripts/` | `bazi_status.py` | Preflight check trước phân tích |

---

## SYNC COMMANDS

```powershell
# Sync all skills from remote repos
.\.cursor\scripts\sync-repos.ps1

# Sync specific repo
.\.cursor\scripts\sync-repos.ps1 -Repo "AminBlg/SimpleEnglish"

# Available repos:
# - thaofvn-coca06/2026     (versioning conventions)
# - mikiarlo3/ai-copywriter (AI copywriting)
# - virgiliojr94/book-to-skill (books to skills)
# - AminBlg/SimpleEnglish   (plain language)
# - Nutlope/hallmark       (anti-slop design)
# - xiaopu-ai/web-clone-prompt (prompt-first clone)
# - nextlevelbuilder/ui-ux-pro-max-skill (117k stars - UI/UX design)
```

---

## DESIGN SYSTEM WORKFLOW

### Stack 7: Design System (UI/UX Pro Max)
```
ui-ux-pro-max + frontend-taste + hallmark
     ↓              ↓             ↓
 Design System  Anti-slop    Anti-slop
   Generator    frontend      design
```

### Generate Design System
```bash
# Basic design system
python .cursor/skills/ui-ux-pro-max/scripts/search.py "beauty spa" --design-system -p "MyApp"

# With design dials
python .cursor/skills/ui-ux-pro-max/scripts/search.py "SaaS dashboard" --design-system --variance 8 --motion 9 --density 7

# Persist to files
python .cursor/skills/ui-ux-pro-max/scripts/search.py "fintech" --design-system --persist -p "MyBank"
```
