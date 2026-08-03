# Cursor Enterprise Framework - Skill Index

> **Phiên bản:** 3.0.0 | **Cập nhật:** 2026-08-03
> **Total Skills:** 50+ | **Rules:** 43 | **Agents:** 18 | **Commands:** 28

---

## Tổng quan cấu trúc

```
.cursor/
├── skills/           # 50+ skills (tự động gọi theo context)
├── rules/            # 43 rules (luật theo domain)
├── agents/           # 18 agent personas (chuyên gia)
├── commands/          # 28 slash commands (workflows)
├── hooks/            # 15 hooks (CI/CD, git, dev)
├── knowledge/         # 329 knowledge bases (theo ngôn ngữ/framework)
├── workflows/         # 11 workflows (standard processes)
├── prompts/          # 31 prompts (task templates)
├── memory/           # 14 memory files (context)
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
| `security-auditor` | `agents/security-auditor.md` | Threat modeling, auth, secrets |
| `vietnam-payment-review` | `skills/vietnam-payment-review/` | MoMo, SePay, PayOS, ZaloPay |

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
| `web-cloner` | `agents/web-cloner.md` | Clone UI/visual, assets, behavior với Playwright |
| `web-scraper` | `agents/web-scraper.md` | Extract structured content (docs, articles, tables) |

### 8.2 Web Design

| Skill | Path | Description |
|-------|------|-------------|
| `open-design` | `skills/open-design/` | Open Design integration |

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
| `web-cloner` | Website cloning |
| `web-scraper` | Content extraction |
| `marketing-strategist` | Positioning, SEO, lifecycle |
| `doc-writer` | API docs, READMEs, ADRs |

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
web-cloner + web-scraper + frontend-taste + deploy-to-vercel
     ↓           ↓              ↓                ↓
   Clone UI    Extract     Rebuild taste      Ship it
```

---

## SKILL TRIGGER MAP

### Auto-trigger by keywords

| Keywords | Auto-load Skill |
|----------|-----------------|
| landing, portfolio, homepage, SaaS | `frontend-taste` |
| redesign, improve UI | `frontend-redesign` |
| clone, copy website | `web-cloner` |
| scrape, extract, crawl | `web-scraper` |
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
1. frontend-taste (landing pages)
2. hallmark (anti-slop design)
3. dashboard-ui (dashboard/admin components)
4. ai-copywriter (human copy)
5. simple-english (clarity)
6. karpathy-coding (code quality)
7. ponytail (minimal code)
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

### Clone website
```
1. /clone → web-cloner activates
2. Playwright capture
3. Extract structured content (web-scraper)
4. Rebuild với frontend-taste
5. Deploy với deploy-to-vercel
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
```
