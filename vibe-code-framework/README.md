# Vibe Code Framework

> **Cross-Platform AI Coding Framework** — Một nguồn quy tắc, nhiều bộ adapter

**Version:** 1.0.0  
**Updated:** 2026-10-09

---

## Tổng quan

Vibe Code Framework chuẩn hóa cách tổ chức Rules, Skills, Agents và Workflows cho các Vibe Coding tool. Thay vì nhồi nhét tất cả vào thư mục riêng của từng IDE, framework này xây dựng **một bộ nguồn dùng chung** và **adapter cho từng tool**.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         VIBE CODE FRAMEWORK                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│   │ 01-core-    │    │ 02-stacks/  │    │ 03-skills/  │    │ 04-agents/ │ │
│   │   rules/    │    │             │    │             │    │             │ │
│   │             │    │ vue3-ts/    │    │ create-api/ │    │ architect/ │ │
│   │ principles  │    │ aspnetcore/ │    │ create-ui/  │    │ frontend/  │ │
│   │ security    │    │ database/   │    │ db-migrate/ │    │ backend/   │ │
│   │ code-quality│    │ deployment/ │    │ code-review/│    │ reviewer/  │ │
│   └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘ │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                        07-adapters/                                  │   │
│   │  ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌─────────┐ ┌─────────────┐ │   │
│   │  │ Cursor/ │ │ Claude/ │ │ Codex/   │ │ Copilot/│ │ Windsurf/   │ │   │
│   │  │ .mdc    │ │ .md      │ │ AGENTS   │ │ .md     │ │ rules/      │ │   │
│   │  └─────────┘ └─────────┘ └──────────┘ └─────────┘ └─────────────┘ │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Ba lớp phân chia

| Lớp | Mô tả | Ví dụ |
|-----|-------|-------|
| **Rules** | Quy tắc luôn phải tuân thủ | Kiến trúc, coding style, bảo mật, cấu trúc dự án |
| **Skills** | Quy trình chuyên biệt cho từng task | Tạo API, thiết kế UI, review code, tạo database migration |
| **Agents/Workflows** | Vai trò và quy trình phối hợp nhiều bước | Solution Architect, Fullstack Engineer, multi-step workflows |

---

## Cấu trúc thư mục

```
vibe-code-framework/
├── README.md                    # Framework overview
├── AGENTS.md                    # Agent personas (OpenAI Codex format)
├── CLAUDE.md                    # Claude Code instructions
├── GEMINI.md                    # Google Antigravity instructions
│
├── 01-core-rules/              # Nguyên tắc chung, không phụ thuộc IDE
│   ├── 01-principles.md        # Nguyên tắc nền tảng
│   ├── 02-security.md          # Bảo mật (OWASP, secrets)
│   ├── 03-code-quality.md      # Chất lượng code
│   ├── 04-architecture.md      # Kiến trúc (Clean, Hexagonal)
│   ├── 05-git-workflow.md      # Git workflow
│   └── README.md               # Core rules index
│
├── 02-stacks/                  # Quy tắc theo tech stack
│   ├── vue3-typescript/        # Vue 3 + TypeScript
│   ├── nuxt/                   # Nuxt.js
│   ├── aspnetcore/             # ASP.NET Core
│   ├── nodejs/                 # Node.js
│   ├── database/               # PostgreSQL, MySQL
│   ├── deployment/             # Docker, Vercel, K8s
│   └── README.md               # Stacks index
│
├── 03-skills/                  # Skills dùng chung
│   ├── create-feature/         # Tạo feature mới
│   │   └── SKILL.md
│   ├── create-api/             # Tạo REST/GraphQL API
│   │   └── SKILL.md
│   ├── create-ui/              # Thiết kế UI
│   │   └── SKILL.md
│   ├── database-migration/      # Tạo database migration
│   │   └── SKILL.md
│   ├── code-review/            # Review code
│   │   └── SKILL.md
│   ├── debug-error/            # Debug lỗi
│   │   └── SKILL.md
│   ├── fullstack-web/          # Fullstack web app
│   │   └── SKILL.md
│   ├── security-scan/          # Security scan
│   │   └── SKILL.md
│   └── README.md               # Skills index
│
├── 04-agents/                  # Agent personas
│   ├── architect.md            # Solution Architect
│   ├── frontend.md            # Frontend Engineer
│   ├── backend.md             # Backend Engineer
│   ├── database.md            # Database Engineer
│   ├── reviewer.md            # Code Reviewer
│   └── README.md               # Agents index
│
├── 05-workflows/               # Multi-step workflows
│   ├── new-project.md          # Tạo project mới
│   ├── new-feature.md          # Tạo feature mới
│   ├── bug-fix.md             # Fix bug
│   ├── release.md             # Release workflow
│   └── README.md               # Workflows index
│
├── 06-templates/               # Code templates
│   ├── vue-component/          # Vue component template
│   ├── api-endpoint/           # API endpoint template
│   ├── database-schema/        # Database schema template
│   └── README.md               # Templates index
│
├── 07-adapters/                # Tool-specific adapters
│   ├── cursor/                 # Cursor IDE
│   │   └── rules/              # → .cursor/rules/*.mdc
│   ├── codex/                  # OpenAI Codex
│   │   └── skills/             # → .agents/skills/
│   ├── claude-code/            # Claude Code
│   │   ├── rules/              # → .claude/rules/
│   │   └── skills/             # → .claude/skills/
│   ├── copilot/                # GitHub Copilot
│   │   └── instructions/       # → .github/copilot-instructions.md
│   ├── windsurf/               # Windsurf
│   │   └── rules/              # → .windsurf/rules/
│   ├── antigravity/            # Google Antigravity
│   │   └── rules/              # → Tool-specific rules
│   └── README.md               # Adapters index
│
└── 08-scripts/                 # Utilities
    ├── install.ps1             # Windows installer
    ├── install.sh              # Unix installer
    ├── sync-adapters.ps1      # Sync adapters
    └── validate.ps1            # Validate framework
```

---

## Thư mục chuẩn của từng tool

| Tool | Rules / Instructions | Skills |
|------|---------------------|--------|
| **Cursor** | `.cursor/rules/*.mdc`, `AGENTS.md` | `SKILL.md` theo cơ chế hỗ trợ |
| **Claude Code** | `CLAUDE.md`, `.claude/rules/` | `.claude/skills/<name>/SKILL.md` |
| **OpenAI Codex** | `AGENTS.md` | `.agents/skills/<name>/SKILL.md` |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Tùy phiên bản |
| **VS Code Agent** | `AGENTS.md`, `.github/copilot-instructions.md` | Theo Agent Skills |
| **Windsurf** | `.windsurf/rules/` | Theo cấu hình |
| **Google Antigravity** | Quy tắc workspace/global | Theo phiên bản |

---

## Nguyên tắc cốt lõi

### 1. Single Source of Truth

Chỉ viết **một bản nội dung** trong thư mục nguồn. Script sync sẽ tạo bản tương thích cho từng tool.

```
03-skills/create-api/SKILL.md (source)
         ↓
    sync-adapters.ps1
         ↓
.cursor/rules/rule_create-api.mdc  (Cursor)
.agents/skills/create-api/SKILL.md (Codex)
.claude/skills/create-api/SKILL.md (Claude Code)
```

### 2. Không nhân bản nội dung

- Rules: Viết trong `01-core-rules/` hoặc `02-stacks/`
- Skills: Viết trong `03-skills/`
- Agents: Viết trong `04-agents/`
- Workflows: Viết trong `05-workflows/`

### 3. Adapter chỉ chuyển đổi định dạng

Adapter trong `07-adapters/` **KHÔNG** chứa nội dung gốc. Chúng chỉ:
- Chuyển đổi định dạng file (`.md` → `.mdc`)
- Thay đổi vị trí đường dẫn
- Áp dụng tool-specific conventions

### 4. File adapter đặc biệt

Riêng các file sau cần tạo theo đúng cơ chế của từng tool:
- `AGENTS.md` (Codex), `CLAUDE.md` (Claude Code), `GEMINI.md` (Antigravity)
- `.cursor/rules/*.mdc` (Cursor)
- `.github/copilot-instructions.md` (Copilot)

---

## Bắt đầu

### Cài đặt cho Cursor

```powershell
# Clone repository
git clone <repo-url> vibe-code-framework

# Chạy installer
cd vibe-code-framework
.\08-scripts\install.ps1 -Tool Cursor

# Hoặc chạy manual
Copy-Item -Recurse 07-adapters\cursor\* <your-project>\.cursor\
```

### Cài đặt cho Claude Code

```bash
git clone <repo-url> vibe-code-framework
cd vibe-code-framework
chmod +x 08-scripts/install.sh
./08-scripts/install.sh --tool claude-code
```

---

## Thứ tự xây dựng

1. ✅ Hoàn thiện `01-core-rules` (principles, security, code-quality, architecture, git)
2. ✅ Chuẩn hóa quy ước `SKILL.md`
3. ✅ Xây bộ skills dùng chung (create-feature, create-api, create-ui, database-migration, code-review, debug-error, security-scan, fullstack-web)
4. ✅ Viết adapter cho Cursor và Codex trước
5. ✅ Bổ sung Claude Code, Antigravity, Windsurf và Copilot
6. ✅ Tạo script cài đặt, đồng bộ và test adapter

## Files trong Framework

```
vibe-code-framework/
├── README.md, AGENTS.md, CLAUDE.md, GEMINI.md     ✅
├── 01-core-rules/ (5 files)                        ✅
├── 03-skills/ (7 skills)                          ✅
├── 04-agents/ (5 agents)                          ✅
├── 05-workflows/ (4 workflows)                     ✅
├── 06-templates/ (3 templates)                     ✅
├── 07-adapters/ (6 tool adapters)                ✅
└── 08-scripts/ (2 sync scripts)                   ✅

Total: ~60 files
```

---

## Liên kết

- [Cursor Rules Documentation](https://cursor.com/docs/rules)
- [OpenAI Codex AGENTS.md](https://github.com/openai/codex/blob/main/docs/agents_md.md)
- [GitHub Copilot Instructions](https://docs.github.com/en/copilot/concepts/prompting/response-customization)
- [agent-skills](https://github.com/addyosmani/agent-skills) (87k stars)
- [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) (186k stars)
