# Cursor Enterprise Framework V4

## Giới thiệu
Cursor Enterprise Framework là bộ framework cấp Enterprise dành cho AI coding agents, được xây dựng trên 4 nguyên tắc: Memory First, Retrieval First, Token Optimization First, Knowledge Reuse First.

## Compatibility
- Cursor (Primary)
- Claude Code
- Vibe Code
- Windsurf
- Cline
- Roo Code

## Cấu trúc

```
.cursor/
├── rules/         # 55 MDC Rules
├── skills/        # 44 MDC Skills
├── memory/        # Memory System (JSON + SQLite)
├── knowledge/     # 200+ Knowledge Files (29 domains)
├── prompts/       # 30+ Prompt Templates
├── workflows/     # 10+ Standard Workflows
├── templates/     # Template files
├── scripts/       # Automation Scripts
├── cache/         # Compiled Cache
└── vector-db/     # Vector DB Config
```

## Tech Stack

### Frontend
Next.js 15, React 19, Vue 3, Nuxt 4, TypeScript 5, TailwindCSS, Shadcn/UI

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

### Cloud
Cloudflare, AWS, Azure, GCP

### Deployment
Docker, Kubernetes, Coolify, Vercel, Railway

## Quick Start

1. Check Context Router để load đúng domain
2. Check Memory System trước khi implement
3. Use Prompt Templates cho task mới
4. Follow Workflow step by step
5. Update Memory sau khi hoàn thành

## Scripts

```powershell
# Build Memory
. .cursor/scripts/memory-builder/build-memory.ps1

# Compile Knowledge
. .cursor/scripts/knowledge-compiler/compile-knowledge.ps1

# Package Framework
. .cursor/scripts/packager.ps1
```

## License
MIT

## Version
4.0.0 - 2026-06-23
