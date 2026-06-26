# Cursor Enterprise Framework - Setup Installer

## Tổng Quan

File `cursor-setup.exe` cho phép cài đặt `.cursor` configuration từ Cursor Enterprise Framework Generator sang bất kỳ project nào trong máy.

## File Locations

```
.cursor-setup.exe                    # Main executable (root folder)
.cursor/
└── scripts/
    ├── cursor-setup.exe             # Original build
    ├── dist/                        # Build output
    │   └── cursor-setup.exe        # ~7.7 MB
    ├── setup_local_installer.py    # Source Python script
    └── setup_exe_builder.py        # Builder script (nếu cần rebuild)
```

## Cách Sử Dụng

### 1. Cài Đặt Vào Project

```cmd
cursor-setup.exe "D:\Projects\MyApp"
```

### 2. Ghi Đè Project Đã Có .cursor

```cmd
cursor-setup.exe "D:\Projects\MyApp" -Force
```

### 3. Cài Đặt Không Backup

```cmd
cursor-setup.exe "D:\Projects\MyApp" -Force -NoBackup
```

### 4. Liệt Kê Tất Cả Projects

```cmd
cursor-setup.exe -List
```

Output:
```
WITH .cursor:
  + Project1
  + Project2

WITHOUT .cursor:
  - NewProject
  - ApiService
```

### 5. Xem Trợ Giúp

```cmd
cursor-setup.exe -Help
```

## Options

| Option | Mô tả |
|--------|--------|
| `<ProjectPath>` | Đường dẫn project cần cài đặt |
| `-Force` | Ghi đè `.cursor` đã tồn tại |
| `-NoBackup` | Không backup trước khi ghi đè |
| `-List` | Liệt kê tất cả projects |
| `-Help` | Hiển thị trợ giúp |

## Components Được Cài Đặt

| Component | Files | Mô tả |
|-----------|-------|-------|
| rules | 86 | Architecture & coding rules |
| skills | 557 | Skill definitions |
| scripts | 38 | Automation scripts |
| knowledge | 333 | Knowledge base |
| commands | 28 | Command registry |
| hooks | 15 | Git hooks |
| prompts | 31 | Prompt templates |
| memory | 14 | Memory system |
| workflows | 11 | Workflow definitions |
| templates | 6 | Code templates |
| cache | 36 | Cache configurations |

**Total: ~1159 files**

## Search Paths

Script tự động tìm projects trong:

- `D:\PROJECTS`
- `C:\Projects`
- `C:\Dev`
- `D:\Dev`

## Rebuild .exe

Nếu cần cập nhật source path hoặc rebuild:

```cmd
cd .cursor\scripts
pyinstaller --name="cursor-setup" --onefile --console --noconfirm --clean setup_local_installer.py
```

Hoặc sử dụng builder:

```cmd
python setup_exe_builder.py
```

## Troubleshooting

### "Source .cursor not found"

Kiểm tra `SOURCE_ROOT` trong `setup_local_installer.py`:

```python
SOURCE_ROOT = Path(r"D:\PROJECTS\CURSORS\CURSOR ENTERPRISE FRAMEWORK GENERATOR")
```

### Muốn Đổi Source Path

1. Mở `setup_local_installer.py`
2. Sửa dòng `SOURCE_ROOT`
3. Rebuild: `pyinstaller ... setup_local_installer.py`

### Chạy Trên Máy Không Có Python

File `cursor-setup.exe` là standalone - không cần Python installed.

## Ví Dụ Thực Tế

### Thiết Lập Project Mới

```cmd
# 1. Tạo project mới
mkdir "D:\Projects\MyNewApp"
cd "D:\Projects\MyNewApp"

# 2. Clone repo
git clone https://github.com/user/repo.git

# 3. Cài .cursor
cursor-setup.exe "D:\Projects\MyNewApp"
```

### Batch Install (PowerShell)

```powershell
$projects = @(
    "D:\Projects\Project1",
    "D:\Projects\Project2",
    "D:\Projects\Project3"
)

foreach ($proj in $projects) {
    & "path\to\cursor-setup.exe" $proj -Force
}
```

### Cập Nhật Skills Cho Tất Cả Projects

```powershell
Get-ChildItem "D:\Projects" -Directory | ForEach-Object {
    & "cursor-setup.exe" $_.FullName -Force
}
```
