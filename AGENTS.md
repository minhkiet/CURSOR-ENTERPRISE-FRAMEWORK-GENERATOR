# Codex Enterprise Framework - Root Rules

> Based on [agent-skills](https://github.com/addyosmani/agent-skills) (67k stars)
> **Skill Index:** Xem `.cursor/SKILL-INDEX.md` để biết tổng hợp tất cả skills, agents, commands

## Framework Overview
This project uses Codex Enterprise Framework - a comprehensive development framework with:
- 39 specialized rules
- 50+ skills với dual-gate system
- 329 knowledge bases
- 18 agent personas
- 28 slash commands
- 4 reference checklists
- Automated task analysis

## Quick Reference

### Development Lifecycle (agent-skills)

```
DEFINE          PLAN           BUILD          VERIFY         SHIP
┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
│ Idea │ ───▶ │ Spec │ ───▶ │ Code │ ───▶ │ Test │ ───▶ │  Go  │
│Refine│      │  PRD │      │ Impl │      │Debug │      │ Live │
└──────┘      └──────┘      └──────┘      └──────┘      └──────┘
  /spec          /plan          /build        /test         /ship
```

## Essential Skills (Auto-loaded)

### Core Coding
- **karpathy-coding**: [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) (186k stars) - Think before coding, simplicity, surgical changes
- **ponytail**: Lazy Senior - minimal code, YAGNI
- **full-output**: No skeletons, complete implementation

### UI & Design
- **landing-page-pro**: Landing pages, SaaS, E-commerce (Hero, Pricing, Auth, Cart)
- **dashboard-ui**: Dashboard/Admin components (inputs, tables, forms, pickers)
- **frontend-taste**: Anti-slop frontend cho landing/portfolio (6 pre + 8 post gates)
- **hallmark**: [Nutlope/hallmark](https://github.com/Nutlope/hallmark) (9.3k stars) - 57 slop-test gates
- **frontend-redesign**: Redesign existing UI

### Writing & Copy
- **ai-copywriter**: [mikiarlo3/ai-copywriter](https://github.com/mikiarlo3/ai-copywriter) - Humanize AI text, 33 patterns
- **simple-english**: [AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish) - Plain language

### Document & Knowledge
- **book-to-skill**: [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) - Convert books to skills

### Quality & Review
- **frontend-review**: Quality gate cho all frontend work

## Skill Index
Xem `.cursor/SKILL-INDEX.md` cho tổng hợp đầy đủ theo nhóm:
- Nhóm 1: Code & Development
- Nhóm 2: UI & Visual Design
- Nhóm 3: Writing & Copy
- Nhóm 4: Document & Knowledge
- Nhóm 5: Optimization & Performance
- Nhóm 6: Security
- Nhóm 7: Project Structure (by language)
- Nhóm 8: Web Cloning & Scraping
- Nhóm 9: Web Creation (from requirements)

### Core Protocols
- Read `.cursor/rules/rule_skill-registry.mdc` - skill definitions
- Read `.cursor/rules/rule_skill-integration.mdc` - how skills work
- Read `.cursor/rules/rule_task-analyzer.mdc` - task analysis
- Read `.cursor/AGENTS.md` - agent personas

### Architecture
- `.cursor/rules/ref_architecture-patterns.mdc` - Design patterns
- `.cursor/rules/enterprise-patterns.mdc` - System architecture
- `.cursor/rules/ref_frontend-frameworks.mdc` - Frontend guides

### Quality Gates
All tasks should pass:
1. Pre-review gates (before implementation)
2. Post-review gates (after implementation)

## Agent Personas

Specialized reviewers for targeted tasks:

| Persona | Trigger | Expertise |
|---------|---------|-----------|
| Code Reviewer | /review | Five-axis code review |
| Test Engineer | /test | Test strategy, coverage |
| Security Auditor | /security | OWASP, vulnerabilities |
| Web Performance Auditor | /webperf | Core Web Vitals |

## Skills Navigation
See `.cursor/INDEX.md` for complete skill list and descriptions.

## Development Guidelines
- Follow coding standards in `.cursor/rules/coding-standards.mdc`
- Use appropriate skills for the task
- Run frontend-review for UI changes
- Use karpathy-coding + ponytail for efficient coding
- Reference `.cursor/references/` for checklists

---

## Versioning & Sync Conventions

> Synced from [thaofvn-coca06/2026](https://github.com/thaofvn-coca06/2026)

### Versioning Rules

- **Single source of truth:** `AGENTS.md`, `.cursor/AGENTS.md`, plugin manifests
- **Default: bump PATCH segment (3rd level, `X.Y.Z`)** — automatic for every shippable commit
- Only bump MINOR or MAJOR when **user explicitly asks** ("this is minor", "make it 2.0")
- After bumping, two steps required:
  1. Tag: `git tag -a v<X.Y.Z> -m "..."` + `git push origin v<X.Y.Z>`
  2. **Publish GitHub Release** for the tag (shields.io reads from Releases API, not raw tags)

### Commit Rules

- Primary author must be set with `--author="Your Name <email>"`
- Verify with `git log -1 --format='%an <%ae>'` before pushing
- Co-author trailers (`Co-Authored-By:`) are fine

### Sync Protocol

Pull latest conventions from remote:

```bash
# Sync AGENTS.md and conventions from thaofvn-coca06/2026
git fetch origin
git pull origin main
```

For automated sync, see `.cursor/scripts/sync-repos.ps1`
