# Cursor Enterprise Framework - Naming Convention v2

> **Version:** 2.0.0  
> **Created:** 2026-08-03  
> **Purpose:** Unified naming convention với prefix system cho skills, rules, agents

## Tổng quan

Document này định nghĩa hệ thống đặt tên thống nhất với prefix để:
- Dễ dàng nhận diện loại artifact
- Nhanh chóng gọi, kết nối và tương tác
- Tự động routing khi request được truyền vào

---

## Prefix System

### Skills (`.cursor/skills/`)

| Prefix | Domain | Examples |
|--------|--------|----------|
| `code_` | Code & Development | code_karpathy, code_ponytail, code_full-output |
| `ui_` | UI & Visual Design | ui_landing-page-pro, ui_dashboard-ui, ui_frontend-taste |
| `doc_` | Document & Knowledge | doc_book-to-skill, doc_simple-english |
| `db_` | Database | db_mysql-patterns, db_sql-server |
| `infra_` | Infrastructure | infra_deploy-vercel, infra_docker, infra_k8s |
| `sec_` | Security | sec_security-review, sec_vietnam-payment |
| `perf_` | Performance | perf_webperf, perf_react-best-practices |
| `ai_` | AI & Agent | ai_weknora-kb, ai_pixelrag, ai_video-generation |
| `special_` | Special/Specific | special_bazi, special_vietnam-address |
| `util_` | Utilities | util_skill-installer, util_create-pull-request |

### Rules (`.cursor/rules/`)

| Prefix | Type | Examples |
|--------|------|----------|
| `rule_` | Core Rules | rule_skill-registry, rule_skill-integration, rule_task-analyzer |
| `proto_` | Protocol | proto_multi-language-vibe-code, proto_context-router |
| `ref_` | Reference | ref_architecture-patterns, ref_frontend-frameworks |
| `meta_` | Meta/Config | meta_coding-standards, meta_deployment |

### Agents (`.cursor/agents/`)

| Prefix | Type | Examples |
|--------|------|----------|
| `agent_` | Agent Personas | agent_code-reviewer, agent_security-auditor |
| `cmd_` | Slash Commands | cmd_spec, cmd_plan, cmd_build |

---

## Skill Mapping (Old → New)

### Code & Development
| Old Name | New Name | Path |
|----------|----------|------|
| `karpathy-coding` | `code_karpathy` | `.cursor/skills/code_karpathy/` |
| `karpathy-guidelines` | `code_karpathy` | `.cursor/rules/rule_karpathy-guidelines.mdc` |
| `ponytail` | `code_ponytail` | `.cursor/skills/code_ponytail/` |
| `full-output` | `code_full-output` | `.cursor/skills/code_full-output/` |
| `vibe-coding` | `code_vibe-coding` | `.cursor/skills/code_vibe-coding/` |

### UI & Visual Design
| Old Name | New Name | Path |
|----------|----------|------|
| `landing-page-pro` | `ui_landing-page-pro` | `.cursor/skills/ui_landing-page-pro/` |
| `dashboard-ui` | `ui_dashboard-ui` | `.cursor/skills/ui_dashboard-ui/` |
| `frontend-taste` | `ui_frontend-taste` | `.cursor/skills/ui_frontend-taste/` |
| `hallmark` | `ui_hallmark` | `.cursor/skills/ui_hallmark/` |
| `frontend-redesign` | `ui_frontend-redesign` | `.cursor/skills/ui_frontend-redesign/` |
| `frontend-review` | `ui_frontend-review` | `.cursor/skills/ui_frontend-review/` |
| `visual-explainer` | `ui_visual-explainer` | `.cursor/skills/ui_visual-explainer/` |
| `canvas-design` | `ui_canvas-design` | `.cursor/skills/ui_canvas-design/` |
| `theme-factory` | `ui_theme-factory` | `.cursor/skills/ui_theme-factory/` |
| `open-design` | `ui_open-design` | `.cursor/skills/ui_open-design/` |

### Document & Writing
| Old Name | New Name | Path |
|----------|----------|------|
| `ai-copywriter` | `doc_ai-copywriter` | `.cursor/skills/doc_ai-copywriter/` |
| `book-to-skill` | `doc_book-to-skill` | `.cursor/skills/doc_book-to-skill/` |
| `simple-english` | `doc_simple-english` | `.cursor/skills/doc_simple-english/` |
| `visual-explainer` | `ui_visual-explainer` | `.cursor/skills/ui_visual-explainer/` |
| `microsoft-docs` | `doc_microsoft-docs` | `.cursor/skills/doc_microsoft-docs/` |

### Database
| Old Name | New Name | Path |
|----------|----------|------|
| `mysql` | `db_mysql` | `.cursor/skills/db_mysql/` |
| `mysql-patterns` | `db_mysql-patterns` | `.cursor/skills/db_mysql-patterns/` |
| `sql-server-table-reconciliation` | `db_sql-server-table-reconciliation` | `.cursor/skills/db_sql-server-table-reconciliation/` |
| `adbc` | `db_adbc` | `.cursor/skills/db_adbc/` |
| `redis-observability` | `db_redis-observability` | `.cursor/skills/db_redis-observability/` |

### Infrastructure
| Old Name | New Name | Path |
|----------|----------|------|
| `deploy-to-vercel` | `infra_deploy-vercel` | `.cursor/skills/infra_deploy-to-vercel/` |
| `docker` | `infra_docker` | `.cursor/skills/infra_docker/` |
| `prefect` | `infra_prefect` | `.cursor/skills/infra_prefect/` |

### Security
| Old Name | New Name | Path |
|----------|----------|------|
| `security-review` | `sec_security-review` | `.cursor/skills/sec_security-review/` |
| `vietnam-payment-review` | `sec_vietnam-payment-review` | `.cursor/skills/sec_vietnam-payment-review/` |

### Performance
| Old Name | New Name | Path |
|----------|----------|------|
| `vercel-react-best-practices` | `perf_react-best-practices` | `.cursor/skills/perf_react-best-practices/` |
| `vercel-composition-patterns` | `perf_composition-patterns` | `.cursor/skills/perf_composition-patterns/` |

### AI & Agent
| Old Name | New Name | Path |
|----------|----------|------|
| `weknora-kb` | `ai_weknora-kb` | `.cursor/skills/ai_weknora-kb/` |
| `weknora-agent` | `ai_weknora-agent` | `.cursor/skills/ai_weknora-agent/` |
| `pixelrag` | `ai_pixelrag` | `.cursor/skills/ai_pixelrag/` |
| `video-generation` | `ai_video-generation` | `.cursor/skills/ai_video-generation/` |
| `chatbotx-feature` | `ai_chatbotx-feature` | `.cursor/skills/ai_chatbotx-feature/` |
| `chatbotx-database` | `ai_chatbotx-database` | `.cursor/skills/ai_chatbotx-database/` |
| `chatbotx-worker` | `ai_chatbotx-worker` | `.cursor/skills/ai_chatbotx-worker/` |

### Special
| Old Name | New Name | Path |
|----------|----------|------|
| `bazi` | `special_bazi` | `.cursor/skills/special_bazi/` |
| `vietnam-address` | `special_vietnam-address` | `.cursor/skills/special_vietnam-address/` |

### Utilities
| Old Name | New Name | Path |
|----------|----------|------|
| `skill-installer` | `util_skill-installer` | `.cursor/skills/util_skill-installer/` |
| `create-pull-request` | `util_create-pull-request` | `.cursor/skills/util_create-pull-request/` |
| `csv-wrangling` | `util_csv-wrangling` | `.cursor/skills/util_csv-wrangling/` |
| `document-ocr` | `util_document-ocr` | `.cursor/skills/util_document-ocr/` |
| `webapp-testing` | `util_webapp-testing` | `.cursor/skills/util_webapp-testing/` |

---

## Rule Mapping (Old → New)

| Old Name | New Name | Path |
|----------|----------|------|
| `skill-registry.mdc` | `rule_skill-registry.mdc` | `.cursor/rules/rule_skill-registry.mdc` |
| `skill-integration.mdc` | `rule_skill-integration.mdc` | `.cursor/rules/rule_skill-integration.mdc` |
| `task-analyzer.mdc` | `rule_task-analyzer.mdc` | `.cursor/rules/rule_task-analyzer.mdc` |
| `intent-detection.mdc` | `rule_intent-detection.mdc` | `.cursor/rules/rule_intent-detection.mdc` |
| `multi-language-processing.mdc` | `proto_multi-language-processing.mdc` | `.cursor/rules/proto_multi-language-processing.mdc` |
| `multi-language-vibe-code.mdc` | `proto_multi-language-vibe-code.mdc` | `.cursor/rules/proto_multi-language-vibe-code.mdc` |
| `context-router.mdc` | `proto_context-router.mdc` | `.cursor/rules/proto_context-router.mdc` |
| `memory-first.mdc` | `proto_memory-first.mdc` | `.cursor/rules/proto_memory-first.mdc` |
| `architecture-patterns.mdc` | `ref_architecture-patterns.mdc` | `.cursor/rules/ref_architecture-patterns.mdc` |
| `frontend-frameworks.mdc` | `ref_frontend-frameworks.mdc` | `.cursor/rules/ref_frontend-frameworks.mdc` |
| `backend-frameworks.mdc` | `ref_backend-frameworks.mdc` | `.cursor/rules/ref_backend-frameworks.mdc` |
| `coding-standards.mdc` | `meta_coding-standards.mdc` | `.cursor/rules/meta_coding-standards.mdc` |
| `deployment.mdc` | `meta_deployment.mdc` | `.cursor/rules/meta_deployment.mdc` |
| `auth.mdc` | `meta_auth.mdc` | `.cursor/rules/meta_auth.mdc` |
| `security.mdc` | `meta_security.mdc` | `.cursor/rules/meta_security.mdc` |

---

## Request Routing Pattern

### Input → Auto-Detect Flow

```
User Request
    │
    ▼
┌─────────────────────────────────────────┐
│  Intent Detection (rule_intent-...)     │
│  - Language (Vietnamese, Chinese...)    │
│  - Keywords (landing, security...)      │
│  - Context (frontend, backend...)       │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  Skill Auto-Discovery                    │
│  - Match prefix: ui_, code_, sec_...    │
│  - Calculate confidence                 │
│  - Return skill path                    │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  Execute Skill                          │
│  - Load SKILL.md from path              │
│  - Run pre-gates                        │
│  - Execute task                         │
│  - Run post-gates                       │
└─────────────────────────────────────────┘
```

### Keyword → Prefix Mapping

| Keyword Pattern | Auto-Select Prefix |
|-----------------|-------------------|
| `landing`, `portfolio`, `homepage` | `ui_` |
| `dashboard`, `admin`, `table` | `ui_` |
| `redesign`, `upgrade`, `improve` | `ui_` |
| `security`, `vulnerability`, `OWASP` | `sec_` |
| `payment`, `MoMo`, `SePay`, `PayOS` | `sec_` |
| `database`, `mysql`, `postgres` | `db_` |
| `deploy`, `docker`, `k8s` | `infra_` |
| `performance`, `optimize`, `bundle` | `perf_` |
| `ai`, `rag`, `agent`, `llm` | `ai_` |
| `code`, `refactor`, `simplify` | `code_` |
| `document`, `ocr`, `pdf` | `doc_` |
| `bazi`, `vietnam-address` | `special_` |
| `install`, `setup`, `utility` | `util_` |

---

## Usage Examples

### Old Way (v1)
```
User: "build a landing page"
→ Manual skill selection needed
→ Path: .cursor/skills/ui_landing-page-pro/
```

### New Way (v2)
```
User: "build a landing page"
→ Auto-detect: ui_ prefix
→ Path: .cursor/skills/ui_landing-page-pro/
→ Confidence: 0.95
```

### Voice Command Pattern
```
"run ui_landing-page-pro for landing page"
"activate sec_security-review for API security"
"execute code_karpathy for clean code"
```

---

## Migration Plan

### Phase 1: Rename Folders
```bash
# Skills
mv skills/landing-page-pro skills/ui_landing-page-pro
mv skills/dashboard-ui skills/ui_dashboard-ui
mv skills/security-review skills/sec_security-review
# ... etc

# Rules
mv rules/skill-registry.mdc rules/rule_skill-registry.mdc
mv rules/skill-integration.mdc rules/rule_skill-integration.mdc
# ... etc
```

### Phase 2: Update References
- Update all SKILL.md paths
- Update .cursorrules references
- Update AGENTS.md references
- Update INDEX.md and INDEX.json

### Phase 3: Backward Compatibility
- Create alias system in skill-registry
- Maintain old names as symlinks
- Log deprecation warnings

---

## Files Changed

| File | Change |
|------|--------|
| `.cursor/rules/rule_skill-registry.mdc` | Updated paths |
| `.cursor/rules/rule_skill-integration.mdc` | Updated paths |
| `.cursor/rules/rule_task-analyzer.mdc` | Updated paths |
| `.cursorrules` | Updated all references |
| `.cursor/AGENTS.md` | Updated skill references |
| `.cursor/INDEX.md` | Updated skill list |
| `.cursor/INDEX.json` | Updated JSON paths |
| `NAMING-CONVENTION.md` | This file |

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-08-03 | 2.0.0 | Initial version with prefix system |
