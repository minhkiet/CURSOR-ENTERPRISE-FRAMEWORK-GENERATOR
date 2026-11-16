---
name: claude-mem
description: Persistent memory, context compression, and cross-session knowledge recall powered by claude-mem and SQLite FTS5.
---

# claude-mem — Persistent Context & Memory Engine

Engine quản lý bộ nhớ dài hạn và nén ngữ cảnh tự động cho các AI coding agent, giải quyết dứt điểm vấn đề "mất trí nhớ" (session amnesia).

## Cấu trúc hoạt động

1. **Active Interception**:
   - `SessionStart`: Tự động nạp chỉ mục các quyết định gần nhất vào ngữ cảnh ban đầu.
   - `PostToolUse`: Bắt toàn bộ kết quả thực thi công cụ (build logs, test runs, code read).
   - `Stop` / `SessionEnd`: Kích hoạt nén và tóm tắt semantic observation.
2. **Local Storage**:
   - Database: `~/.claude-mem/claude-mem.db` (SQLite + FTS5 full-text search).
   - Nén semantic: Rút gọn các log dài thành bản tóm tắt súc tích (~500 tokens).
   - Confidence Decay: Tự động giảm trọng số các quyết định thử nghiệm sau 30 ngày.
3. **Multi-IDE Access**:
   - Claude Code: Sử dụng qua lifecycle plugin native.
   - Cursor / Antigravity / Windsurf: Kết nối qua MCP server cấu hình tại `mcp/mcp_config.json`.

## Nguyên tắc sử dụng

### 1. Privacy Guard (Bảo vệ dữ liệu nhạy cảm)
Luôn luôn bọc mật khẩu, token, API keys, credentials hoặc PII trong tag `<private>`:
```markdown
<private>
STRIPE_SECRET_KEY=sk_live_...
DATABASE_PASSWORD=SuperSecretPass!
</private>
```
Nội dung bên trong `<private>...</private>` sẽ tự động bị bỏ qua, không ghi vào database nhớ.

### 2. Tra cứu lịch sử thay vì đoán mò
Trước khi đưa ra thay đổi lớn cho hệ thống:
1. Tra cứu các quyết định kiến trúc đã lưu trong `claude-mem`.
2. Kiểm tra các lỗi từng xuất hiện để tránh lặp lại cùng một sai lầm.

### 3. Local Web Viewer
- Địa chỉ: `http://localhost:37777`
- Dùng để kiểm tra trực quan dòng sự kiện, tìm kiếm toàn văn và xóa bỏ các quan sát cũ nếu có sự thay đổi lớn về thiết kế.
