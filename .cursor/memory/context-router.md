# Context Router - Bộ định tuyến ngữ cảnh

## Mô tả
Bộ định tuyến ngữ cảnh giúp AI agent chỉ load đúng knowledge domain cần thiết, không load thừa. Giảm token tiêu thụ tối đa.

## Quy tắc định tuyến

### Rule 1: Single Domain Request
Khi user hỏi về một domain cụ thể, chỉ load domain đó và các dependency trực tiếp.

| Yêu cầu | Load | Skip |
|----------|------|------|
| Tối ưu Entity Framework | aspnet-core, sql-server, postgres | bazi, pdf, crm, marketing |
| Tạo PDF Bát Tự | bazi, pdf | aspnet-core, supabase, postgres |
| Tạo RAG pipeline | rag, vector-search, pgvector, openai | bazi, crm, billing |
| Review Laravel code | laravel, mysql | nextjs, vue, aspnet-core |

### Rule 2: Multi Domain Request
Khi user hỏi về nhiều domain, load union của các domain và shared knowledge.

| Yêu cầu | Load | Skip |
|----------|------|------|
| CRM SaaS với Supabase | crm, supabase, rls, pgvector, multi-tenant | bazi, numerology |
| E-Commerce + Billing | crm, billing, multi-tenant, postgres | bazi, tuvi |
| AI SaaS + RAG | rag, vector-search, openai, gemini, claude | crm, billing, marketing |

### Rule 3: Cross-Cutting Concern
Khi user hỏi về cross-cutting concern (security, performance, monitoring), load tất cả các domain liên quan.

| Yêu cầu | Load | Skip |
|----------|------|------|
| Security audit | security, api, database, secrets-management | bazi, numerology |
| Performance audit | performance, database, redis, queue | marketing, billing |
| Monitoring setup | monitoring, observability, deployment, docker | bazi, crm |

## Context Router Matrix

### Frontend Domain
```
nextjs      → nextjs/*
vue         → vue/*
nuxt        → nuxt/*
frontend-core → frontend/glossary, frontend/architecture
```

### Backend Domain
```
laravel        → laravel/*
aspnet-core    → aspnet-core/*
nestjs         → nestjs/*
backend-core   → backend/glossary, backend/architecture
```

### Database Domain
```
mysql         → mysql/*
postgres      → postgres/*
sql-server    → sql-server/*
redis         → redis/*
database-core → database/glossary, database/architecture
```

### AI/RAG Domain
```
openai      → openai/*
gemini      → gemini/*
claude      → claude/*
rag         → rag/*
vector-search → vector-search/*
pgvector    → pgvector/*
ai-core     → ai/glossary, ai/architecture
```

### Business Domain
```
bazi         → bazi/*
tuvi         → tuvi/*
numerology   → numerology/*
crm          → crm/*
marketing    → marketing/*
billing      → billing/*
```

### Infrastructure Domain
```
docker       → docker/*
kubernetes   → kubernetes/*
cloudflare   → cloudflare/*
azure        → azure/*
aws          → aws/*
deployment   → deployment/glossary, deployment/architecture
```

## Decision Tree cho Context Router

```
START: User request received
  │
  ▼
Identify primary domain(s)
  │
  ├── Frontend? ──→ Load: nextjs/vue/nuxt knowledge
  │
  ├── Backend? ──→ Load: laravel/aspnet-core/nestjs knowledge
  │
  ├── Database? ──→ Load: mysql/postgres/sql-server/redis knowledge
  │
  ├── AI/RAG? ────→ Load: rag/vector-search/openai/gemini/claude knowledge
  │
  ├── Business? ──→ Load: bazi/tuvi/numerology/crm/marketing knowledge
  │
  └── Infra? ─────→ Load: docker/kubernetes/cloudflare/azure/aws knowledge
  │
  ▼
Identify secondary domains (dependencies)
  │
  ▼
Load shared knowledge (if needed)
  │
  ▼
Check memory/session-summary (reuse)
  │
  ▼
Execute task with minimal context
```

## Ví dụ thực tế

### Ví dụ 1: "Tạo API cho module Billing"
```
Request: Tạo API cho module Billing
Router Decision:
  Primary: api, billing
  Dependencies: multi-tenant, database
  Load:
    - knowledge/api/glossary.md
    - knowledge/api/architecture.md
    - knowledge/billing/glossary.md
    - knowledge/billing/architecture.md
    - knowledge/multi-tenant/glossary.md
    - rules/api.mdc
    - rules/billing.mdc
  Skip:
    - bazi/*
    - tuvi/*
    - numerology/*
    - marketing/*
    - nextjs/*
```

### Ví dụ 2: "Tối ưu RAG pipeline cho Bát Tự"
```
Request: Tối ưu RAG pipeline cho Bát Tự
Router Decision:
  Primary: rag, bazi
  Dependencies: vector-search, pgvector, pdf
  Load:
    - knowledge/rag/glossary.md
    - knowledge/rag/architecture.md
    - knowledge/rag/best-practice.md
    - knowledge/bazi/glossary.md
    - knowledge/bazi/architecture.md
    - knowledge/vector-search/glossary.md
    - knowledge/pgvector/glossary.md
    - knowledge/pgvector/best-practice.md
    - knowledge/pdf/glossary.md
    - rules/rag.mdc
    - rules/vector-search.mdc
  Skip:
    - crm/*
    - billing/*
    - laravel/*
    - aspnet-core/*
    - kubernetes/*
```

## Liên kết
- [[project-index]] - Project Index
- [[token-optimization]] - Token Optimization
- [[memory-first]] - Memory First
- [[../skills/knowledge-compiler]] - Knowledge Compiler
- [[../scripts/context-router]] - Context Router Script
