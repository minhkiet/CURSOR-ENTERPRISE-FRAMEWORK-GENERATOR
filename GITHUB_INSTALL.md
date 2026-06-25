# GitHub Installation Guide

## Quick Install (One Command)

### Windows (PowerShell) - INSTALL
```powershell
irm https://raw.githubusercontent.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/main/install.ps1 | iex
```

### Windows (PowerShell) - UPDATE (if already installed)
```powershell
& {irm https://raw.githubusercontent.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/main/install.ps1} -Update
```

### Windows (CMD)
```cmd
curl -LO https://raw.githubusercontent.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/main/install.ps1 && powershell -ExecutionPolicy Bypass -File install.ps1 && del install.ps1
```

## Using setup.bat with GitHub

### Clone from GitHub (Recommended)
```cmd
setup.bat --github
setup.bat --github https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR
setup.bat --github https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR --branch develop
```

### Explicit Clone Mode
```cmd
setup.bat --clone https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR
setup.bat --clone https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR main
```

### Download as ZIP
```cmd
setup.bat --zip https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR
setup.bat --zip https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR --branch main
```

## Using install-github.bat

```cmd
:: Default repo
install-github.bat

:: Custom repo
install-github.bat https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR

:: Custom repo + branch
install-github.bat https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR main
```

## Using install-github.ps1 (PowerShell)

```powershell
# Default installation
.\install-github.ps1

# Custom repo and branch
.\install-github.ps1 -RepoUrl "https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR" -Branch "main"

# Check for updates
.\install-github.ps1 -CheckUpdate

# Dry run (preview)
.\install-github.ps1 -DryRun

# Force overwrite existing
.\install-github.ps1 -Force
```

## Options

| Flag | Description |
|------|-------------|
| `--github` | Clone from GitHub (uses default or provided URL) |
| `--clone` | Explicit clone mode |
| `--zip` | Download as ZIP file |
| `--branch` | Specify branch name |
| `--force` | Overwrite existing files |
| `--no-cursor-check` | Skip Cursor running check |

## Requirements

- Windows 10/11
- Git (optional, for clone mode)
- PowerShell 5.0+ (for ZIP download)
- Internet connection

## Repository

**GitHub**: https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR
