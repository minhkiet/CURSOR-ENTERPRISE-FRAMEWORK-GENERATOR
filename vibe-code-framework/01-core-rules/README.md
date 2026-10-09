# Core Rules Index

> **Version:** 1.0.0 | **Updated:** 2026-10-09

---

## Tổng quan

`01-core-rules/` chứa các nguyên tắc chung, không phụ thuộc vào IDE hay tech stack cụ thể. Đây là nền tảng cho mọi development work.

## Các rules trong bộ này

| # | Rule | Mô tả |
|---|------|--------|
| 01 | [01-principles.md](./01-principles.md) | Nguyên tắc nền tảng (YAGNI, DRY, KISS) |
| 02 | [02-security.md](./02-security.md) | Bảo mật cơ bản (OWASP Top 10, secrets) |
| 03 | [03-code-quality.md](./03-code-quality.md) | Chất lượng code (clean code, testing) |
| 04 | [04-architecture.md](./04-architecture.md) | Kiến trúc (Clean Architecture, patterns) |
| 05 | [05-git-workflow.md](./05-git-workflow.md) | Git workflow (commit, branch, PR) |

## Sử dụng

Các rules này được tự động nạp khi làm việc với bất kỳ project nào. Chúng cung cấp:

- **Nền tắc tư duy** — YAGNI, DRY, KISS, SOLID
- **An toàn bảo mật** — OWASP, secrets management
- **Chất lượng code** — Clean code, testing strategy
- **Kiến trúc hệ thống** — Layer separation, dependency rules
- **Version control** — Git conventions

## Ánh xạ sang Cursor

```
01-core-rules/01-principles.md  → .cursor/rules/core.mdc
01-core-rules/02-security.md    → .cursor/rules/security.mdc
01-core-rules/03-code-quality.md → .cursor/rules/code-quality.mdc
01-core-rules/04-architecture.md → .cursor/rules/architecture.mdc
01-core-rules/05-git-workflow.md → .cursor/rules/git-workflow.mdc
```

## Ánh xạ sang Claude Code

```
01-core-rules/01-principles.md  → .claude/rules/01-principles.md
01-core-rules/02-security.md    → .claude/rules/02-security.md
01-core-rules/03-code-quality.md → .claude/rules/03-code-quality.md
01-core-rules/04-architecture.md → .claude/rules/04-architecture.md
01-core-rules/05-git-workflow.md → .claude/rules/05-git-workflow.md
```
