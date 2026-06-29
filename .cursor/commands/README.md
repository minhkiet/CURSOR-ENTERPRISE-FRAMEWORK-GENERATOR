# Cursor Commands Registry

> Last updated: 2026-06-29  
> Framework: Cursor Enterprise Framework V5 (agent-skills integrated)

## Giới thiệu

Commands là các slash commands cho Cursor IDE. Mỗi command được định nghĩa trong thư mục riêng với:
- `command.md` - Mô tả command và trigger keywords
- `prompt.md` - Prompt template cho command

## Development Lifecycle Commands

Dựa trên [agent-skills](https://github.com/addyosmani/agent-skills) (67k stars)

```
DEFINE          PLAN           BUILD          VERIFY         SHIP
┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
│ Idea │ ───▶ │ Spec │ ───▶ │ Code │ ───▶ │ Test │ ───▶ │  Go  │
│Refine│      │  PRD │      │ Impl │      │Debug │      │ Live │
└──────┘      └──────┘      └──────┘      └──────┘      └──────┘
  /spec          /plan          /build        /test         /ship
```

### Define Phase

| Command | Mô tả | Key Principle |
|---------|--------|---------------|
| `/spec` | Define what to build | **Spec before code** |
| `/interview` | Clarify requirements via one-question-at-a-time | Extract what user actually wants |

### Plan Phase

| Command | Mô tả | Key Principle |
|---------|--------|---------------|
| `/plan` | Plan how to build it | **Small, atomic tasks** |
| `/plan auto` | Auto-generate plan from spec | One approved plan |

### Build Phase

| Command | Mô tả | Key Principle |
|---------|--------|---------------|
| `/build` | Build incrementally | **One slice at a time** |
| `/build auto` | Auto-generate plan + implement approved pass | Approve once, run autonomously |

### Verify Phase

| Command | Mô tả | Key Principle |
|---------|--------|---------------|
| `/test` | Prove it works | **Tests are proof** |
| `/debug` | Debugging and error recovery | Five-step triage |
| `/webperf` | Audit web performance | Measure before optimize |

### Review Phase

| Command | Mô tả | Key Principle |
|---------|--------|---------------|
| `/review` | Review before merge | **Improve code health** |
| `/code-simplify` | Simplify the code | Clarity over cleverness |
| `/security` | Security hardening | OWASP Top 10 prevention |

### Ship Phase

| Command | Mô tả | Key Principle |
|---------|--------|---------------|
| `/ship` | Ship to production | **Faster is safer** |

---

## Domain Commands

| Command | Category | Mô tả |
|---------|----------|--------|
| `/payment` | Domain | Review payment integration Việt Nam |
| `/frontend` | Frontend | Frontend tasks (build, redesign, review) |
| `/bazi` | Domain | Tính Bát Tự |
| `/tuvi` | Domain | Tính Tử Vi |
| `/numerology` | Domain | Thần Số Học |

## Quality Commands

| Command | Category | Mô tả |
|---------|----------|--------|
| `/audit` | Quality | Audit code (security, performance, architecture) |
| `/perf` | Performance | Performance audit |
| `/refactor` | Quality | Refactor code |
| `/doc` | Quality | Tạo tài liệu |
| `/adr` | Architecture | Tạo ADR (Architecture Decision Record) |

## Development Commands

| Command | Category | Mô tả |
|---------|----------|--------|
| `/fix` | Development | Sửa lỗi bug |
| `/design` | Architecture | Thiết kế (DDD, CQRS, Database) |
| `/rag` | AI | Xây dựng RAG system |
| `/generate` | Generation | Generate code (PDF, API, migration) |
| `/workflow` | Workflow | Execute standard workflow |

## DevOps Commands

| Command | Category | Mô tả |
|---------|----------|--------|
| `/deploy` | DevOps | Deployment workflow |
| `/test` | Testing | Chiến lược testing |

## Data Commands

| Command | Category | Mô tả |
|---------|----------|--------|
| `/scrape` | Data | Web scraping và content extraction |
| `/clone` | Data | Clone website về giao diện và chức năng |
| `/memory` | Memory | Quản lý memory system |
| `/report` | Reporting | Tạo report |

## Cách sử dụng

1. Gõ `/` trong Cursor chat để hiển thị danh sách commands
2. Chọn command phù hợp với task
3. Mô tả chi tiết yêu cầu sau command

## Agent Personas

Commands có thể activate agent personas cho specialized reviews:

| Persona | Trigger | Expertise |
|---------|---------|-----------|
| **Code Reviewer** | `/review` | Code quality, architecture |
| **Test Engineer** | `/test` | Test strategy, coverage |
| **Security Auditor** | `/security` | OWASP, vulnerabilities |
| **Web Performance Auditor** | `/webperf` | Core Web Vitals, bundle |

---

## Thêm Command mới

1. Tạo thư mục mới trong `.cursor/commands/<command-name>/`
2. Tạo file `command.md` với mô tả
3. Tạo file `prompt.md` với prompt template
4. Cập nhật registry này

---

## Changelog

### 2026-06-29 v5.0
- Integrated agent-skills lifecycle commands (/spec, /plan, /build, /test, /review, /ship)
- Added agent personas section
- Updated command categories
