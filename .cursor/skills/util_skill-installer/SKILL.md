# Skill Dependency Auto-Installer

## Mục tiêu

Tự động kiểm tra và cài đặt dependencies khi skills được kích hoạt. Đảm bảo môi trường sẵn sàng trước khi chạy skill tasks.

## Cách hoạt động

### Auto-Install Flow

```
User Request → Skill Detection → Dependency Check → Auto-Install (if needed) → Run Skill
                                       ↓
                              [Prompt user if needed]
                                       ↓
                              [Install dependencies]
                                       ↓
                                   Continue
```

### Dependency Manifest

Mỗi skill có định nghĩa dependencies trong `skill-dependencies.json`:

```json
{
  "skills": {
    "document-ocr": {
      "name": "Document OCR",
      "dependencies": {
        "python": {
          "required": true,
          "packages": [
            {"name": "pytesseract", "version": "latest"},
            {"name": "Pillow", "version": "latest"}
          ]
        },
        "system": {
          "required": true,
          "windows": {
            "name": "Tesseract OCR",
            "installCommand": "Download from GitHub releases"
          }
        }
      }
    }
  }
}
```

## Sử dụng

### Check Dependencies

```bash
# Check a specific skill
python .cursor/scripts/skill-installer.py check document-ocr

# PowerShell
. .cursor/scripts/skill-installer.ps1 -Command check -SkillName document-ocr
```

### Install Dependencies

```bash
# Install for specific skill
python .cursor/scripts/skill-installer.py install document-ocr

# PowerShell
. .cursor/scripts/skill-installer.ps1 -Command install -SkillName document-ocr

# Install all
python .cursor/scripts/skill-installer.py install-all

# PowerShell
. .cursor/scripts/skill-installer.ps1 -Command install-all
```

### List Skills

```bash
python .cursor/scripts/skill-installer.py list

# PowerShell
. .cursor/scripts/skill-installer.ps1 -Command list
```

## Auto-Install Configuration

```json
{
  "autoInstallConfig": {
    "enabled": true,
    "promptBeforeInstall": true,
    "installOptional": true,
    "checkBeforeRun": true,
    "verbose": true,
    "continueOnError": true
  }
}
```

| Config | Description |
|--------|-------------|
| `enabled` | Bật/tắt auto-install |
| `promptBeforeInstall` | Hỏi trước khi cài đặt |
| `installOptional` | Cài đặt optional dependencies |
| `checkBeforeRun` | Check trước khi chạy skill |
| `verbose` | Hiển thị chi tiết |
| `continueOnError` | Tiếp tục nếu có lỗi |

## Supported Skills

| Skill | Python | Node | System |
|-------|--------|------|--------|
| document-ocr | pytesseract, Pillow, opencv-python | - | Tesseract OCR |
| playwright-web-scraper | playwright | @playwright/test | - |
| rag-builder | chromadb, langchain, pypdf | - | - |
| frontend-taste | - | tailwindcss, framer-motion | - |
| frontend-redesign | - | tailwindcss, prettier | - |
| security-review | bandit, safety | npm-audit | - |
| database-optimization | sqlparse, psycopg2-binary | - | - |
| performance-audit | - | lighthouse | - |

## Integration với Skill Detection

### Auto-Trigger Keywords

| Keyword | Action |
|---------|--------|
| `install deps` | Run dependency check |
| `check deps` | Check dependencies only |
| `setup` | Install all dependencies |

### Integration Flow

1. **Skill Detection** nhận diện skill cần chạy
2. **Dependency Check** kiểm tra packages còn thiếu
3. **Auto-Install** cài đặt nếu cần (hoặc prompt user)
4. **Run Skill** thực thi skill task

### Example Flow

```
User: "OCR text từ file này"

→ Skill Detection: document-ocr (confidence: 0.95)
→ Dependency Check: pytesseract [MISSING], opencv-python [OK]
→ Auto-Install: pip install pytesseract
→ Run Skill: OCR extraction
```

## PowerShell Examples

```powershell
# Check document-ocr dependencies
. .\.cursor\scripts\skill-installer.ps1 -Command check -SkillName document-ocr

# Install document-ocr dependencies
. .\.cursor\scripts\skill-installer.ps1 -Command install -SkillName document-ocr

# Install all
. .\.cursor\scripts\skill-installer.ps1 -Command install-all

# List all skills
. .\.cursor\scripts\skill-installer.ps1 -Command list
```

## Python Examples

```python
from skill_installer import SkillDependencyInstaller

installer = SkillDependencyInstaller()

# Check dependencies
check = installer.check_skill("document-ocr")
print(check.all_satisfied)

# Install dependencies
installer.install_skill("document-ocr")

# Install all
results = installer.install_all()
```

## Troubleshooting

### Tesseract not found

```bash
# Windows: Download từ GitHub
https://github.com/UB-Mannheim/tesseract/releases

# Sau khi cài đặt, thêm vào PATH:
# C:\Program Files\Tesseract-OCR\

# Verify
tesseract --version
```

### pip not found

```powershell
# Ensure Python is in PATH
# Hoặc sử dụng python -m pip
python -m pip install pytesseract
```

### Permission denied

```powershell
# Run as Administrator
# Hoặc sử dụng --user flag
pip install --user pytesseract
```

## Files

- `skill-dependencies.json` - Dependency manifest
- `skill-installer.py` - Python installer
- `skill-installer.ps1` - PowerShell installer

## Notes

- Auto-install chỉ chạy khi `autoInstallConfig.enabled = true`
- Prompt user trước khi cài đặt (nếu `promptBeforeInstall = true`)
- Tiếp tục với skill ngay cả khi cài đặt thất bại (nếu `continueOnError = true`)
- Kiểm tra dependencies trước khi chạy skill (nếu `checkBeforeRun = true`)
