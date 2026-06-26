# Cursor Enterprise Framework - Local Setup

Script để cài đặt `.cursor` từ project này sang các project khác trong máy.

## Cấu Trúc

```
.cursor/
├── scripts/
│   ├── setup-local.ps1           # Script chính để cài đặt
│   ├── setup-local-config.json   # Configuration file
│   └── setup-local.md           # Hướng dẫn sử dụng
```

## Cách Sử Dụng

### 1. Liệt Kê Projects

```powershell
.\setup-local.ps1 -List
```

Output:
```
╔══════════════════════════════════════════════════════════════════════╗
║        CURSOR ENTERPRISE FRAMEWORK - LOCAL SETUP WIZARD              ║
╚══════════════════════════════════════════════════════════════════════╝

Source: D:\PROJECTS\CURSORS\CURSOR ENTERPRISE FRAMEWORK GENERATOR
Available Components:
  [rules] - 30 files
  [skills] - 17 files
  [scripts] - 5 files
  [knowledge] - 3 files

=== PROJECTS WITH .CURSOR ===
  [+] MyProject - D:\Projects\MyProject

=== PROJECTS WITHOUT .CURSOR ===
  [-] NewApp - D:\Projects\NewApp
  [-] ApiService - D:\Projects\ApiService
```

### 2. Cài Đặt Đầy Đủ

```powershell
.\setup-local.ps1 "D:\Projects\MyApp"
```

### 3. Cài Đặt Chọn Lọc

```powershell
# Chỉ rules và skills
.\setup-local.ps1 "D:\Projects\MyApp" -Components rules,skills

# Chỉ scripts
.\setup-local.ps1 "D:\Projects\MyApp" -Components scripts
```

### 4. Dry Run (Xem Trước)

```powershell
.\setup-local.ps1 "D:\Projects\MyApp" -DryRun
```

Output:
```
[DRY RUN] Would install:
  - rules (30 files)
  - skills (17 files)
  - scripts (5 files)
  - knowledge (3 files)
```

### 5. Cài Đặt Với Backup

```powershell
.\setup-local.ps1 "D:\Projects\MyApp" -Backup
```

### 6. Ghi Đè Không Cần Hỏi

```powershell
.\setup-local.ps1 "D:\Projects\MyApp" -Force
```

### 7. Tạo Symlink (Đồng Bộ Tự Động)

```powershell
.\setup-local.ps1 "D:\Projects\MyApp" -CreateSymlink
```

> **Lưu ý:** Symlink cần quyền Admin trên Windows. Nếu không có quyền, script sẽ tự động fallback sang copy.

## Các Thành Phần

| Component | Mô tả | Files |
|-----------|-------|-------|
| `rules` | Architecture & coding rules (.mdc) | ~30 |
| `skills` | Skill definitions | ~17 |
| `scripts` | Automation scripts | ~5 |
| `knowledge` | Knowledge base | ~3 |

## Options Chi Tiết

| Option | Mô tả |
|--------|-------|
| `-List` | Liệt kê tất cả projects trong máy |
| `-Components <items>` | Chọn components: `all`, `rules`, `skills`, `scripts`, `knowledge` |
| `-DryRun` | Xem trước không cài đặt |
| `-Backup` | Backup trước khi ghi đè |
| `-Force` | Ghi đè không cần hỏi |
| `-CreateSymlink` | Tạo symbolic link thay vì copy |

## Tự Động Tìm Projects

Script sẽ tự động tìm projects trong các thư mục:

- `D:\PROJECTS`
- `C:\Projects`
- `C:\Dev`
- `D:\Dev`
- `D:\Work`
- `C:\Work`
- `~\Documents`
- `~\Desktop`

## Ví Dụ Sử Dụng Thực Tế

### Thiết Lập Project Mới

```powershell
# 1. Tạo project mới
mkdir "D:\Projects\MyNewApp"
cd "D:\Projects\MyNewApp"

# 2. Clone repo hoặc tạo code

# 3. Copy .cursor vào
& "D:\PROJECTS\CURSORS\CURSOR ENTERPRISE FRAMEWORK GENERATOR\.cursor\scripts\setup-local.ps1" "D:\Projects\MyNewApp"
```

### Đồng Bộ Rules Sang Tất Cả Projects

```powershell
$projects = @(
    "D:\Projects\Project1",
    "D:\Projects\Project2",
    "D:\Projects\Project3"
)

foreach ($proj in $projects) {
    .\setup-local.ps1 $proj -Components rules -Force
}
```

### Cập Nhật Skills Cho Tất Cả Projects

```powershell
$projects = Get-ChildItem "D:\Projects" -Directory

foreach ($proj in $projects) {
    .\setup-local.ps1 $proj.FullName -Components skills -Backup
}
```

## Troubleshooting

### "Project not found"

Kiểm tra lại đường dẫn hoặc dùng `-List` để xem projects có sẵn.

### "Symlink failed (may need admin)"

Symlink cần quyền Administrator. Script sẽ tự động fallback sang copy.

### "Target already has .cursor"

Dùng `-Force` để ghi đè hoặc `-Backup` để backup trước.

## Configuration

Chỉnh sửa `setup-local-config.json` để tùy chỉnh:

```json
{
  "installOptions": {
    "defaultBehavior": "prompt",
    "autoBackup": true,
    "createSymlink": false
  }
}
```
