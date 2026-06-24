# Cursor Enterprise Framework V4 - Project Overview

## Version
4.0.0 - 2026-06-23

## Giới thiệu
Cursor Enterprise Framework là framework hoàn chỉnh dành cho AI coding agents, được thiết kế để tối ưu hóa hiệu suất làm việc của AI agents trên nhiều IDE.

## Compatibility Matrix

| IDE | Support Level | Notes |
|-----|--------------|-------|
| Cursor | Primary | Fully optimized |
| Claude Code | Supported | Native compatible |
| Vibe Code | Supported | Native compatible |
| Windsurf | Supported | Native compatible |
| Cline | Supported | Native compatible |
| Roo Code | Supported | Native compatible |

## Technology Stack Overview

### Frontend Ecosystem
- **Next.js 15**: App Router, Server Components, TypeScript
- **React 19**: Hooks, Server Components
- **Vue 3**: Composition API, Script Setup
- **Nuxt 4**: Universal rendering
- **UI Libraries**: TailwindCSS, Shadcn/UI, Vuetify, Ant Design

### Backend Ecosystem
- **Laravel 12**: PHP modern development
- **ASP.NET Core 9**: .NET 9, minimal APIs
- **NestJS**: TypeScript, decorators
- **NodeJS**: Runtime environment

### Data Layer
- **Relational**: MySQL 8.0, PostgreSQL 16, SQL Server 2022
- **Local**: SQLite 3
- **Cache**: Redis 7
- **BaaS**: Supabase (Auth, Database, Storage, Edge Functions, PGVector)

### AI/RAG Stack
- **Providers**: OpenAI (GPT-4o), Gemini (2.0 Flash), Claude (Opus 4)
- **Local**: Ollama
- **Aggregators**: OpenRouter
- **Vector Stores**: PGVector, ChromaDB, Qdrant, Weaviate

### Infrastructure
- **Cloud**: Cloudflare Workers/Pages, AWS, Azure, GCP
- **Containers**: Docker, Kubernetes
- **Deploy**: Vercel, Railway, Coolify

## Nguyên tắc cốt lõi

### 1. Memory First
Luôn tra cứu memory system trước khi thực hiện bất kỳ task nào.
- Check decisions.sqlite cho existing ADRs
- Check bugs.sqlite cho known bugs
- Check session-summary cho context

### 2. Retrieval First
Luôn retrieval knowledge trước khi hỏi hoặc implement.
- Sử dụng Context Router để load đúng domain
- Sử dụng semantic search thay vì full scan
- Không đọc lại tài liệu đã được cache

### 3. Token Optimization First
Tối ưu token tiêu thụ ở mọi bước.
- Chỉ load domain cần thiết
- Sử dụng prompt cache
- Compress session summary
- Lazy load knowledge

### 4. Knowledge Reuse First
Tái sử dụng existing decisions và solutions.
- Không tạo lại ADR đã tồn tại
- Không fix lại bug đã biết
- Không implement lại pattern đã có

## Framework Architecture

```
.cursor/
├── rules/          # Behavioral rules (MDC)
├── skills/         # Technical skills (MDC)
├── commands/       # Slash commands for Cursor IDE (22 commands)
├── hooks/          # Hooks for Git, CI/CD, and development (12 hooks)
├── memory/         # Persistent memory
│   ├── *.json      # Index files
│   └── schema/     # SQLite databases
├── knowledge/       # Domain knowledge (MD)
├── prompts/        # Prompt templates (MD)
├── workflows/       # Workflow definitions (MD)
├── templates/       # Code templates
├── scripts/        # Automation scripts (PS1)
├── cache/          # Compiled artifacts
└── vector-db/      # Vector DB configs
```

## Quick Start Guide

### Step 1: Understand the Task
```markdown
1. Identify primary domain
2. Identify secondary domains
3. Load Context Router configuration
```

### Step 2: Load Relevant Knowledge
```markdown
1. Check technology-stack.json
2. Load relevant knowledge files
3. Check relevant rules
4. Load relevant skills
```

### Step 3: Check Memory
```markdown
1. Check decisions.sqlite (existing ADRs)
2. Check bugs.sqlite (known issues)
3. Check session-summary (previous context)
```

### Step 4: Select Prompt Template
```markdown
1. Match task type to prompt template
2. Follow workflow steps
3. Execute task
```

### Step 5: Update Memory
```markdown
1. Update session-summary
2. Update decisions.sqlite (if new ADR)
3. Update bugs.sqlite (if bug fix)
4. Update prompt-cache.sqlite (if new prompt)
```

## Memory System Details

### SQLite Databases
- **decisions.sqlite**: Architecture Decision Records
- **bugs.sqlite**: Bug tracking và patterns
- **prompt-cache.sqlite**: Prompt templates và usage
- **knowledge.sqlite**: Knowledge base metadata
- **embeddings.sqlite**: Vector embeddings
- **sessions.sqlite**: Session history

### JSON Index Files
- **project-index.md**: Tổng quan dự án
- **code-index.md**: Code location index
- **context-router.md**: Context routing rules
- **technology-stack.json**: Tech stack definition
- **business-rules.md**: Business logic rules
- **customer-rules.md**: Customer-specific rules
- **prompt-index.md**: Prompt template index

## Token Optimization Details

### Context Router
Bộ định tuyến ngữ cảnh giúp AI agent chỉ load đúng domain cần thiết.

### Knowledge Compiler
Script tự động gộp và summarize knowledge documents.

### Prompt Cache
Lưu trữ prompt templates và usage statistics để reuse.

### Session Summary
Compress session context sau mỗi task để giảm token.

### Decision Memory
Lưu trữ ADRs và reuse trong các task tương tự.

### Bug Memory
Lưu trữ bug patterns và solutions để tránh repeat.

## Domain Coverage

### Business Domains
- Bát Tự (Four Pillars)
- Tử Vi (Chinese Fortune)
- Thần Số Học (Numerology)
- CRM SaaS
- Marketing

### Technical Domains
- Frontend: NextJS, Vue, Nuxt
- Backend: Laravel, ASP.NET Core, NestJS
- Database: MySQL, PostgreSQL, SQL Server, Redis
- AI/RAG: OpenAI, Gemini, Claude, RAG
- Infrastructure: Docker, Kubernetes, Cloudflare, AWS, Azure

## Multi-Tenant SaaS Architecture

### Tenant Isolation
- PostgreSQL Row Level Security (RLS)
- Tenant discriminator column
- Application-level filtering

### Billing
- Subscription management
- Usage-based billing
- Invoice generation

### CRM Features
- Contact management
- Lead tracking
- Deal pipeline
- Email integration

## AI/RAG Architecture

### RAG Pipeline
```
Document → Chunking → Embedding → Vector Store
                                    ↓
User Query → Embedding → Vector Search → Reranking → Generation
```

### Supported Embedding Models
- text-embedding-3-small (1536 dims)
- text-embedding-3-large (3072 dims)
- text-embedding-ada-002 (1536 dims)

## Scripts Reference

### Build Scripts
```powershell
# Manage commands and hooks
. .cursor/scripts/command-registry.ps1 -Action list
. .cursor/scripts/command-registry.ps1 -Action install

# Build memory system
. .cursor/scripts/memory-builder/build-memory.ps1

# Compile knowledge
. .cursor/scripts/knowledge-compiler/compile-knowledge.ps1

# Build project index
. .cursor/scripts/project-index-builder/build-index.ps1

# Build embeddings
. .cursor/scripts/embedding-builder/build-embeddings.ps1

# Package framework
. .cursor/scripts/packager.ps1
```

## Best Practices

### AI Agent Workflow
1. Luôn check memory trước
2. Luôn use Context Router
3. Luôn reuse existing decisions
4. Luôn update memory sau task
5. Luôn follow workflow steps

### Code Quality
1. Follow coding standards
2. Write tests first
3. Review before commit
4. Document decisions

### Performance
1. Optimize database queries
2. Use caching appropriately
3. Monitor token usage
4. Minimize context size

## License
MIT License

## Version History
- v4.1.0 (2026-06-24): Framework sync - fixed missing hooks, knowledge domains, memory files, prompts/templates frontmatter, SKILL.md Liens
- v4.0.0 (2026-06-23): Initial release with 34 domains, 55 rules, 44 skills
