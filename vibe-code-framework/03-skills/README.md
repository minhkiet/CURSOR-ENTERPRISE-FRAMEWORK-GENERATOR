# Skills Index

> **Version:** 1.0.0 | **Updated:** 2026-10-09

---

## Tổng quan

`03-skills/` chứa các skills dùng chung cho mọi Vibe Coding tool. Mỗi skill được đóng gói trong thư mục riêng với file `SKILL.md` theo chuẩn.

## Cấu trúc Skill

```
skill-name/
├── SKILL.md              # Bắt buộc - Mô tả skill
├── README.md             # Tùy chọn - Hướng dẫn chi tiết
├── references/           # Tài liệu tham khảo
│   ├── architecture.md
│   ├── examples.md
│   └── checklist.md
└── templates/           # Mẫu code
    ├── template-1.ts
    └── template-2.ts
```

## Các skills trong bộ này

| Skill | Mô tả |
|-------|--------|
| [create-feature](./create-feature/) | Tạo feature mới từ spec đến implementation |
| [create-api](./create-api/) | Thiết kế và implement REST/GraphQL API |
| [create-ui](./create-ui/) | Thiết kế và implement UI components |
| [database-migration](./database-migration/) | Tạo và quản lý database migrations |
| [code-review](./code-review/) | Review code theo quality gates |
| [debug-error](./debug-error/) | Debug và fix lỗi systematic |
| [fullstack-web](./fullstack-web/) | Fullstack web app (ASP.NET + React) |
| [security-scan](./security-scan/) | Security vulnerability scan |
| [frontend-design](./frontend-design/) | External frontend design skill; pending owner review |

## Ánh xạ sang Cursor

```
03-skills/create-api/SKILL.md → .cursor/skills/create-api/SKILL.md
03-skills/create-ui/SKILL.md  → .cursor/skills/create-ui/SKILL.md
...
```

## Ánh xạ sang Codex

```
03-skills/create-api/SKILL.md → .agents/skills/create-api/SKILL.md
03-skills/create-ui/SKILL.md  → .agents/skills/create-ui/SKILL.md
...
```

## Bổ sung skill từ GitHub

Dùng importer append-only tại `tools/skill_installer.py` để lấy một thư mục
skill thật có `SKILL.md` từ GitHub vào Resource Hub:

```powershell
python tools/skill_installer.py add-github `
  --repo owner/repository `
  --skill-path skills/example `
  --ref main
```

Thêm `--dry-run` để tải và kiểm tra trước mà không ghi file.

Importer không ghi đè thư mục đã tồn tại, không xóa hoặc migration `.cursor`,
và ghi provenance external vào
`00-governance/records/external-skills.json`. Skill mới ở trạng thái
`SOT-EXTERNAL`/`PENDING_REVIEW`; không có approval nào được suy diễn.
