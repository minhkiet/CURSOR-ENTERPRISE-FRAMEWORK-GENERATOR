# Cursor Enterprise Framework V4 - Index

## Tổng quan
Cursor Enterprise Framework là bộ framework hoàn chỉnh dành cho AI coding agents, được thiết kế theo nguyên tắc Memory First, Retrieval First, Token Optimization First, và Knowledge Reuse First.

## Compatibility
Framework tương thích với:
- Cursor
- Claude Code
- Vibe Code
- Windsurf
- Cline
- Roo Code

## Cấu trúc thư mục

```
.cursor/
├── rules/         # MDC rules - Nguyên tắc và tiêu chuẩn
├── skills/        # MDC skills - Kỹ năng chuyên môn
├── memory/        # Memory system - Hệ thống bộ nhớ
│   ├── schema/    # SQLite schemas
│   ├── session-summary/
│   ├── architecture-history/
│   ├── decision-history/
│   └── bug-history/
├── knowledge/     # Knowledge files - Kiến thức chuyên domain (34 domains)
├── prompts/       # Prompt templates - Template prompts
├── workflows/    # Standard workflows - Quy trình chuẩn
├── templates/     # Template files
├── scripts/       # Automation scripts
├── cache/         # Compiled cache
└── vector-db/     # Vector database config
```

## Rules Index
| Category | Files |
|----------|-------|
| Core | core-architecture, memory-first, context-router, token-optimization |
| Frontend | nextjs, vue, nuxt, frontend-architecture |
| Backend | laravel, aspnet-core, nestjs, backend-architecture |
| Database | database, mysql, postgres, sql-server, redis |
| AI/RAG | openai, gemini, claude, rag, vector-search, pgvector |
| Business | crm-saas, multi-tenant, billing |
| PDF | pdf-engine |
| Architecture | enterprise-architecture, ddd, cqrs, clean-architecture, microservice, monolith |
| Infrastructure | docker, kubernetes, cloudflare, azure, aws, gcp |
| Operations | security, monitoring, testing, deployment, observability, incident-response, secrets-management, queue, api, version-control |
| Workflow Tools | n8n, temporal, trigger-dev |
| Optimization | performance, cost-optimization |

## Skills Index
| Category | Skills |
|----------|--------|
| Development | debug, root-cause-analysis, feature-builder, refactor-planner, code-review |
| Quality | performance-audit, security-audit, testing-strategy |
| Database | database-optimization, redis-audit, queue-audit, postgres-optimization |
| Frameworks | laravel-review, aspnet-review, entity-framework-audit, nextjs-review, vue-review, nuxt-review |
| AI/RAG | rag-builder, vector-search-review, embedding-builder, ai-integration-review |
| PDF | pdf-generator, pdf-optimization |
| Supabase | supabase-review, rls-audit |
| SaaS | crm-saas-review, tenant-isolation-review, billing-review, multi-tenant-design |
| Architecture | ddd-design, cqrs-implementation, clean-architecture, microservice-design |
| Operations | monitoring-review, deployment-review, cost-optimization-review, docker-review, kubernetes-review |
| Workflow | n8n-workflow, temporal-workflow |
| Memory | memory-manager, knowledge-compiler, prompt-cache-builder, adr-generator |

## Knowledge Base (34 domains)
Mỗi domain có: glossary, architecture, best-practice, anti-pattern, checklist, faq, decision-tree.

| Domain | Mục đích |
|--------|----------|
| Bazi | Tính Bát Tự, Cung mệnh, Vận trình |
| Tuvi | Lá số Tử Vi, Sao chiếu |
| Numerology | Thần Số Học, Số chủ đạo |
| CRM | CRM SaaS Multi-Tenant |
| Marketing | Marketing automation |
| NextJS | Next.js 15 framework |
| Vue | Vue 3 framework |
| Nuxt | Nuxt 4 framework |
| Laravel | Laravel 12 framework |
| ASP.NET Core | ASP.NET Core 9 |
| NestJS | NestJS framework |
| MySQL | MySQL database |
| PostgreSQL | PostgreSQL database |
| SQL Server | SQL Server database |
| Redis | Cache và queue |
| Supabase | BaaS với RLS, PGVector |
| RLS | Row Level Security |
| PGVector | Vector storage |
| OpenAI | OpenAI API integration |
| Gemini | Gemini API integration |
| Claude | Claude API integration |
| RAG | Retrieval Augmented Generation |
| Vector Search | Vector search algorithms |
| PDF | PDF generation engine |
| Docker | Containerization |
| Kubernetes | Container orchestration |
| Cloudflare | Cloudflare platform |
| Azure | Microsoft Azure |
| AWS | Amazon Web Services |

## Prompts Index (31 files)
| ID | Name | Purpose |
|----|------|---------|
| DEV-001 | bug-fix | Sửa lỗi bug |
| DEV-002 | feature-build | Xây dựng feature |
| DEV-003 | refactor | Refactor code |
| DEV-004 | code-review | Review code |
| DEV-005 | testing-strategy | Chiến lược testing |
| ARCH-001 | architecture-review | Review kiến trúc |
| ARCH-002 | ddd-design | Thiết kế DDD |
| ARCH-003 | cqrs-implementation | Implement CQRS |
| ARCH-004 | database-design | Thiết kế database |
| ARCH-005 | api-review | Review API |
| SEC-001 | security-audit | Audit bảo mật |
| PERF-001 | performance-audit | Audit hiệu năng |
| PERF-002 | frontend-optimization | Tối ưu frontend |
| AI-001 | rag-design | Thiết kế RAG |
| AI-002 | ai-integration | Tích hợp AI |
| DOM-001 | bazi-calculation | Tính Bát Tự |
| DOM-002 | tuvi-calculation | Tính Tử Vi |
| DOM-003 | numerology-calculation | Tính Thần Số |
| DOM-004 | pdf-optimization | Tối ưu PDF |
| DOM-005 | crm-saas-review | Review CRM SaaS |
| DOM-006 | multi-tenant-setup | Setup Multi-Tenant |
| DOM-007 | ecommerce-review | Review E-Commerce |
| DOM-008 | erp-review | Review ERP |
| SUP-001 | supabase-review | Review Supabase |
| INF-001 | deployment | Deployment |
| INF-002 | docker-review | Review Docker |
| INF-003 | monitoring-setup | Setup Monitoring |
| INF-004 | nestjs-review | Review NestJS |
| MEM-001 | adr-generator | Tạo ADR |
| MEM-002 | cost-reduction | Giảm chi phí |
| OPS-001 | queue-audit | Audit Queue |

## Commands Index (22 commands)
Slash commands for Cursor IDE, each with workflow, checklist, and links to relevant rules/skills.

| Command | Category | Description |
|---------|----------|-------------|
| /build | Development | Build new feature |
| /fix | Development | Fix bug with root cause analysis |
| /review | Quality | Code review |
| /audit | Quality | Audit (security, performance, architecture) |
| /design | Architecture | Design (DDD, CQRS, Database, API) |
| /rag | AI | Build RAG system |
| /deploy | DevOps | Deployment workflow |
| /test | Testing | Testing strategy |
| /doc | Documentation | Generate documentation |
| /memory | Memory | Manage memory system |
| /adr | Architecture | Create Architecture Decision Record |
| /payment | Domain | Review Vietnam payments (MoMo, SePay, PayOS, ZaloPay, VNPay, VietQR) |
| /security | Security | Security review |
| /frontend | Frontend | Frontend tasks (landing, redesign, review) |
| /perf | Performance | Performance audit |
| /refactor | Refactoring | Code refactoring |
| /generate | Generation | Generate code (PDF, API, migration) |
| /workflow | Workflow | Execute standard workflows |
| /report | Reporting | Create report |
| /bazi | Domain | Four Pillars of Destiny calculation |
| /tuvi | Domain | Tu Vi astrology calculation |
| /numerology | Domain | Numerology calculation |

## Hooks Index (14 hooks)
Auto-trigger hooks for Git, CI/CD, and development workflow automation.

### Git Hooks
| Hook | Trigger | Description |
|------|---------|-------------|
| pre-commit | Before commit | Lint, format, type check |
| commit-msg | After message | Validate commit message format |
| pre-push | Before push | Tests, security scan |
| post-commit | After commit | Update session summary |

### CI/CD Hooks
| Hook | Trigger | Description |
|------|---------|-------------|
| pre-build | Before build | Verify dependencies |
| post-build | After build | Verify artifacts |
| pre-deploy | Before deploy | Final checks |
| post-deploy | After deploy | Health check, notify |
| on-failure | On failure | Analyze error, suggest fix |

### Development Hooks
| Hook | Trigger | Description |
|------|---------|-------------|
| before-task | Before task | Load context, check memory |
| after-task | After task | Update memory, summarize |
| on-error | On error | Analyze error, suggest fix |

## Workflows Index (10 files)

## Memory System

### JSON Index Files
- project-index.md
- code-index.md
- context-router.md
- technology-stack.json
- business-rules.md
- customer-rules.md
- prompt-index.md

### SQLite Databases (Schema files)
- decisions.schema.sql - ADR decisions
- bugs.schema.sql - Bug tracking
- prompt-cache.schema.sql - Prompt caching
- knowledge.schema.sql - Knowledge base + embeddings + sessions

## Scripts
| Script | Purpose |
|--------|---------|
| knowledge-compiler/compile-knowledge.ps1 | Compile knowledge documents |
| project-index-builder/build-index.ps1 | Build project index |
| embedding-builder/build-embeddings.ps1 | Build embeddings |
| memory-builder/build-memory.ps1 | Build memory system |
| packager.ps1 | Package framework into ZIP |
| command-registry.ps1 | Manage commands and hooks (install/list/validate) |

## Token Optimization Strategies
Framework được thiết kế với 10 chiến lược tối ưu token:

1. **Context Router** - Chỉ load domain cần thiết
2. **Knowledge Compiler** - Gộp và summarize documents
3. **Prompt Cache** - Cache frequently used prompts
4. **Session Summary** - Compress session context
5. **Decision Memory** - Reuse existing decisions
6. **Bug Memory** - Avoid repeat bugs
7. **Incremental Scan** - Chỉ scan changed files
8. **Lazy Loading** - Load knowledge on-demand
9. **Semantic Retrieval** - Semantic search thay vì full scan
10. **Auto Compression** - Compress long contexts

## Liên kết nội bộ
- [[rules/core-architecture]] - Core Architecture
- [[skills/memory-manager]] - Memory Manager
- [[memory/context-router]] - Context Router
- [[memory/technology-stack]] - Technology Stack
- [[scripts/packager]] - Packager Script
