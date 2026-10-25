# Cursor Framework Standalone Tools

This directory contains standalone Python tools that can run independently from any project directory.

## Tools

### cursor_framework_cli.py
Standalone CLI tool that wraps `cursor_framework` module.
```
python cursor_framework_cli.py serve --port 8765
python cursor_framework_cli.py index --root .
python cursor_framework_cli.py scan --root .
```

### mcp_config_generator.py
Generates MCP configuration file.
```
python mcp_config_generator.py --output mcp.json
```

### skill_installer.py
Installs skills from git repositories or local paths.
```
python skill_installer.py install --repo owner/repo --skill skill-id
```

### api_integrations/
- `zalo_integration.py` - Zalo API integration
- `telegram_integration.py` - Telegram Bot API integration
- `facebook_integration.py` - Facebook Graph API integration
- `google_integration.py` - Google APIs integration
- `shopee_integration.py` - Shopee API integration

## Requirements

```bash
pip install requests httpx pydantic
```

## Usage

Each tool can be run independently:

```bash
# CLI tool
python tools/cursor_framework_cli.py --help

# Generate MCP config
python tools/mcp_config_generator.py --workspace /path/to/project

# Install skills
python tools/skill_installer.py --list-available

# API integrations
python tools/api_integrations/zalo_integration.py --help
```
