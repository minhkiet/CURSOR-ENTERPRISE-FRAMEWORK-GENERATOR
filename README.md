# Cursor Enterprise Framework Generator V4

> Framework hoàn chỉnh cho AI Coding Agents - Tối ưu Token, Memory, và Knowledge Reuse.

## Tổng quan

Cursor Enterprise Framework là bộ framework cấp Enterprise được thiết kế để tối ưu hóa hiệu suất của AI coding agents trên nhiều IDE: Cursor, Claude Code, Vibe Code, Windsurf, Cline, và Roo Code.

Framework được xây dựng trên 4 nguyên tắc cốt lõi:

- **Memory First**: Luôn tra cứu memory trước khi thực hiện task
- **Retrieval First**: Luôn retrieval knowledge trước khi hỏi
- **Token Optimization First**: Tối ưu token tiêu thụ ở mọi bước
- **Knowledge Reuse First**: Tái sử dụng existing decisions và solutions

## Thành tựu

| Component | Target | Actual | Status |
|-----------|--------|--------|--------|
| Rules | 55 | 26+ | In Progress |
| Skills | 44 | 30+ | In Progress |
| Knowledge Files | 200+ | 45+ | In Progress |
| Knowledge Domains | 29 | 29 | Complete |
| Prompts | 30+ | 30 | Complete |
| Workflows | 10+ | 10 | Complete |
| Scripts | 5+ | 5 | Complete |
| Templates | 6+ | 6 | Complete |
| Memory JSON | 7 | 7 | Complete |
| Memory SQLite | 6 | 4 | In Progress |
| **Total Files** | **400+** | **168+** | **Ongoing** |

**ZIP Package**: `cursor-enterprise-framework-v4.zip` - 0.63 MB

## Cấu trúc

```
.cursor/
├── rules/         # MDC Rules - Tiêu chuẩn và nguyên tắc (26 files)
├── skills/        # MDC Skills - Kỹ năng chuyên môn (30 files)
├── memory/        # Memory System
│   ├── schema/    # SQLite schemas (4 files)
│   ├── session-summary/
│   ├── architecture-history/
│   ├── decision-history/
│   ├── bug-history/
│   ├── *.json     # Index files (7 files)
│   └── *.md       # Memory docs
├── knowledge/     # Knowledge Base (45+ files, 29 domains)
├── prompts/       # Prompt Templates (30 files)
├── workflows/     # Standard Workflows (10 files)
├── templates/     # Templates (6 files)
├── scripts/       # Automation scripts (5 files)
├── cache/         # Compiled cache
└── vector-db/     # Vector DB configuration
```

## Tech Stack được hỗ trợ

### Frontend
Next.js 15, React 19, Vue 3, Nuxt 4, TypeScript 5, TailwindCSS, Shadcn/UI, Vuetify, Ant Design

### Backend
Laravel 12, ASP.NET Core 9, NestJS, NodeJS

### Database
MySQL, PostgreSQL, SQL Server, SQLite, Redis

### BaaS
Supabase (Auth, Database, Storage, Edge Functions, PGVector)

### AI
OpenAI, Gemini, Claude, Ollama, OpenRouter

### RAG
PGVector, ChromaDB, Qdrant, Weaviate

### Workflow
n8n, Temporal, Trigger.dev

### Cloud
Cloudflare, AWS, Azure, GCP

### Deployment
Docker, Kubernetes, Coolify, Vercel, Railway

## Cách sử dụng

### 1. Khi bắt đầu một task mới

```markdown
1. Identify domain của task
2. Sử dụng Context Router để load đúng knowledge
3. Check Memory System (decisions.sqlite, bug-history)
4. Chọn Prompt Template phù hợp
5. Follow Workflow step by step
6. Update Memory sau khi hoàn thành
```

### 2. Sử dụng Context Router

```markdown
Request: "Tối ưu Entity Framework"
Load: aspnet-core, sql-server, postgres
Skip: bazi, pdf, crm

Request: "Tạo PDF Bát Tự"
Load: bazi, pdf
Skip: aspnet-core, supabase
```

### 3. Sử dụng Memory System

```markdown
Trước khi implement:
- Check decisions.sqlite cho existing ADRs
- Check bugs.sqlite cho known bugs
- Check bug-patterns cho common patterns

Sau khi hoàn thành:
- Update decisions.sqlite nếu tạo ADR mới
- Update bugs.sqlite nếu sửa bug
- Update session-summary cho task summary
```

## Scripts

### Build Memory System
```powershell
. .cursor/scripts/memory-builder/build-memory.ps1
```

### Compile Knowledge
```powershell
. .cursor/scripts/knowledge-compiler/compile-knowledge.ps1
```

### Build Project Index
```powershell
. .cursor/scripts/project-index-builder/build-index.ps1
```

### Build Embeddings
```powershell
. .cursor/scripts/embedding-builder/build-embeddings.ps1
```

### Package Framework
```powershell
. .cursor/scripts/packager.ps1
```

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

## Domains được hỗ trợ

| Domain | Mục đích |
|--------|----------|
| Bazi | Tính Bát Tự, Cung mệnh, Vận trình |
| Tuvi | Lá số Tử Vi, Sao chiếu |
| Numerology | Thần Số Học, Số chủ đạo |
| CRM | CRM SaaS Multi-Tenant |
| Marketing | Marketing automation |
| NextJS/Vue/Nuxt | Frontend frameworks |
| Laravel/ASP.NET/NestJS | Backend frameworks |
| MySQL/PostgreSQL/SQL Server | Relational databases |
| Redis | Cache và queue |
| Supabase | BaaS với RLS, PGVector |
| OpenAI/Gemini/Claude | AI providers |
| RAG/Vector Search | AI retrieval |
| PDF | PDF generation |
| Docker/Kubernetes | Container orchestration |
| Cloudflare/AWS/Azure/GCP | Cloud platforms |

## License

MIT License

## Version

4.0.0 - 2026-06-23
