# Cursor Enterprise Framework - Changelog

> **Version:** 4.5.0 | **Date:** 2026-10-13

---

## 🎉 New Features v4.5.0

### REA (Reverse Engineer Anything) Integration

Tích hợp **REA v6.4.0** ([morluto/rea](https://github.com/morluto/rea)) — công cụ phân tích kỹ thuật đảo ngược hợp nhất thông qua CLI & MCP Server:

| Thành phần | Chi tiết | Vị trí |
|------------|----------|--------|
| **Core Tool** | REA v6.4.0 vendor drop (compiled dist + bridges + scripts) | `tools/rea/` |
| **MCP Server** | Stdio MCP Server cho Cursor, Claude, Codex, Windsurf | `.cursor/mcp.json`, `mcp/mcp_config.json` |
| **Skills** | `reverse-engineer-anything` (với 6 reference guides) | `.cursor/skills/sec_reverse-engineer-anything/`, `.agents/skills/` |
| **Commands** | `/rea`, `/reverse` | `.cursor/commands/rea.md`, `.cursor/commands/reverse.md` |
| **Engines** | Native (Ghidra, Hopper, IDA), Electron/JS ASAR, .NET, APK, WASM, EVM, Go, CDP | `tools/rea/` |

---

## 🎉 New Features v4.4.0

### ECC (Enhanced Code Copilot) Integration

Tích hợp **ECC v2.2.2** - Enhanced Code Copilot với 68 agents, 292 skills, 94 commands:

| Component | Count | Description |
|-----------|-------|-------------|
| **Agents** | 68 | Planning, review, security, architecture specialists |
| **Skills** | 292 | TDD, research, security, docs, frontend, data, ML, ops |
| **Commands** | 94 | Slash command shims for all workflows |
| **Hooks** | Runtime | Session summaries, continuous learning, context controls |
| **AgentShield** | Built-in | Security scanning for prompts, hooks, MCP config |

#### Supported Harnesses

| Harness | Profile | Hooks | Plugin |
|---------|---------|-------|--------|
| Claude Code | minimal/core/full | ✅ | ✅ ecc@ecc |
| Codex | minimal/core | ✅ | ✅ Native |
| Cursor | minimal | ❌ | ❌ |
| Gemini CLI | minimal | ❌ | ❌ |
| Zed | minimal | ❌ | ❌ |
| Kimi Code | minimal | ❌ | ❌ |
| GitHub Copilot | minimal | ❌ | ❌ |
| + 7 others | minimal | ❌ | ❌ |

#### Installation

```bash
# Claude Code / Codex (recommended)
npx ecc-universal@2.2.2 install --profile core --target claude

# Guided multi-harness setup
npx ecc-universal@2.2.2 install --guided

# Cursor (project-local)
./install.sh --profile minimal --target cursor
```

#### New Module

```python
from cursor_framework import (
    ECCIntegration,
    HarnessType,
    InstallProfile
)

ecc = ECCIntegration()
status = ecc.get_status()
print(f"ECC v{status.version} installed: {status.installed}")
```

---

## 📦 Previous Release v4.3.0

> **Date:** 2026-07-22

### MCP server sync, glassmorphic UI, toast notifications

### 1. API Integration Skills

Tích hợp đầy đủ các API phổ biến tại Việt Nam và quốc tế:

| Platform | Skill | Description |
|----------|-------|-------------|
| **Zalo** | `source-command-zalo-command` | Zalo OA API - messaging, profile, menu, Mini App với ZaUI |
| **Telegram** | `source-command-telegram-command` | Telegram Bot API - messages, media, groups, inline queries |
| **Facebook** | `source-command-facebook-command` | Facebook Graph API - Page posts, Messenger, insights |
| **Google** | `source-command-google-command` | Google APIs - Sheets, Gmail, Calendar, Drive, Maps |
| **Shopee** | `source-command-shopee-command` | Shopee Open Platform - products, orders, logistics |

### 2. MCP Servers Mới

Thêm 2 MCP server mới:

| Server | Type | Tools | Description |
|--------|------|-------|-------------|
| **vercel** | URL-based | 5 | Vercel deployment integration & monitoring |
| **browser** | npx | 15 | Browser automation via CDP - navigate, snapshot, click, type, screenshot |

### 3. Standalone CLI Tool

`cursor_framework_cli.py` - CLI tool độc lập có thể chạy bất cứ đâu:

```bash
python tools/cursor_framework_cli.py status
python tools/cursor_framework_cli.py skills list
python tools/cursor_framework_cli.py mcp status
python tools/cursor_framework_cli.py api list
```

### 4. Enhanced Stats

Cập nhật số liệu framework:

| Metric | Before | After |
|--------|--------|-------|
| Skills | 22 | **27** |
| MCP Servers | 4 (TDAM layers) | **5** |
| Total Commands | 37 | **42** |

---

## 📦 Installation

### Quick Install

```powershell
# PowerShell (Windows)
irm https://raw.githubusercontent.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/main/install.ps1 | iex
```

### Manual Install

1. Clone repository
2. Copy `.cursor/` to `~/.cursor/`
3. Configure MCP servers

### MCP Configuration

```json
{
  "mcpServers": {
    "cursor-framework": {
      "command": "python",
      "args": ["-m", "cursor_framework_mcp.server"],
      "cwd": "${CURSOR_PROJECT}/tools/cursor-framework-mcp"
    },
    "cursor-autopilot": {
      "command": "python",
      "args": ["-m", "cursor_autopilot_mcp.server"],
      "cwd": "${CURSOR_PROJECT}/tools/cursor-autopilot-mcp"
    },
    "cursor-memory": {
      "command": "python",
      "args": ["-m", "cursor_memory_mcp.server"],
      "cwd": "${CURSOR_PROJECT}/tools/cursor-memory-mcp"
    },
    "vercel": {
      "url": "https://mcp.vercel.com"
    },
    "browser": {
      "command": "npx",
      "args": ["-y", "@browsermcp/mcp"]
    }
  }
}
```

---

## 🚀 Quick Start

### Zalo Integration

```python
from tools.api_integrations.zalo_integration import ZaloClient

client = ZaloClient(access_token="YOUR_TOKEN")
client.send_message("user_id", "Xin chào! 👋")
```

### Telegram Bot

```python
from tools.api_integrations.telegram_integration import TelegramBot

bot = TelegramBot(bot_token="BOT_TOKEN")
bot.send_message(chat_id=123456789, text="Hello from bot!")
```

### Google Sheets

```python
from tools.api_integrations.google_integration import GoogleSheetsClient

sheets = GoogleSheetsClient(credentials_path="credentials.json")
sheets.update_values(
    spreadsheet_id="YOUR_ID",
    range="Sheet1!A1",
    values=[["Name", "Value"], ["Item 1", 100]]
)
```

### Shopee Orders

```python
from tools.api_integrations.shopee_integration import ShopeeClient

client = ShopeeClient(
    partner_id=123456,
    partner_key="PARTNER_KEY",
    shop_id=789012
)
orders = client.get_orders(create_time_from=1704067200, create_time_to=1706745600)
```

---

## 📚 Documentation

### Skills

- [Zalo Integration](./.agents/skills/source-command-zalo-command/SKILL.md)
- [Telegram Integration](./.agents/skills/source-command-telegram-command/SKILL.md)
- [Facebook Integration](./.agents/skills/source-command-facebook-command/SKILL.md)
- [Google Integration](./.agents/skills/source-command-google-command/SKILL.md)
- [Shopee Integration](./.agents/skills/source-command-shopee-command/SKILL.md)

### MCP Servers

- [Browser MCP](./.cursor/knowledge/browser-mcp.md)

### Skill Index

- [Full Skill Index](./.cursor/SKILL-INDEX.md)

---

## 🔧 Development

### Running CLI

```bash
# Status
python tools/cursor_framework_cli.py status

# Skills
python tools/cursor_framework_cli.py skills list

# MCP
python tools/cursor_framework_cli.py mcp status

# API Integrations
python tools/cursor_framework_cli.py api list
```

### Browser MCP Setup

```bash
# Install Chrome extension
# 1. Open chrome://extensions
# 2. Enable Developer Mode
# 3. Load unpacked from tools/browser-mcp/extension

# Or use npx
npx -y @browsermcp/mcp
```

---

## 📊 Framework Statistics

| Component | Count |
|-----------|-------|
| Total Files | 720 |
| Rules | 39 |
| Skills | 27 |
| Knowledge Files | 329 |
| Agents | 18 |
| MCP Servers | 5 |
| Slash Commands | 42 |

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Add skills/API integrations
4. Update documentation
5. Submit PR

---

## 📄 License

MIT License - xem LICENSE file

---

## 🔗 Links

- [GitHub Repository](https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR)
- [Documentation](./.cursor/SKILL-INDEX.md)
- [Skills](./.agents/skills/)
- [Rules](./.cursor/rules/)
- [Agents](./.codex/agents/)
