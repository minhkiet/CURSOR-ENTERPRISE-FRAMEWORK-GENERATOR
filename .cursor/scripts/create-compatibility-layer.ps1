# Create-CompatibilityLayer.ps1
# Script de tao backward compatibility layer voi aliases
# Version: 2.0.0 - 2026-08-03

param(
    [switch]$DryRun,
    [switch]$Verbose
)

$ErrorActionPreference = "Continue"
$CursorRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent

function Write-Step {
    param([string]$Message)
    if ($Verbose -or $DryRun) {
        Write-Host "  -> $Message" -ForegroundColor Cyan
    }
}

function Write-Created {
    param([string]$Message)
    Write-Host "  [OK] $Message" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================"
Write-Host "  BACKWARD COMPATIBILITY LAYER v2.0"
Write-Host "========================================"
Write-Host ""

# ============================================================
# SKILL ALIASES (Old -> New)
# ============================================================

$SkillAliases = @{
    # UI
    "landing-page-pro" = "ui_landing-page-pro"
    "dashboard-ui" = "ui_dashboard-ui"
    "frontend-taste" = "ui_frontend-taste"
    "hallmark" = "ui_hallmark"
    "frontend-redesign" = "ui_frontend-redesign"
    "frontend-review" = "ui_frontend-review"
    "visual-explainer" = "ui_visual-explainer"
    "canvas-design" = "ui_canvas-design"
    "theme-factory" = "ui_theme-factory"
    "open-design" = "ui_open-design"
    
    # Code
    "karpathy-coding" = "code_karpathy"
    "ponytail" = "code_ponytail"
    "full-output" = "code_full-output"
    "vibe-coding" = "code_vibe-coding"
    
    # Security
    "security-review" = "sec_security-review"
    "vietnam-payment-review" = "sec_vietnam-payment-review"
    
    # AI
    "weknora-kb" = "ai_weknora-kb"
    "weknora-agent" = "ai_weknora-agent"
    "pixelrag" = "ai_pixelrag"
    "video-generation" = "ai_video-generation"
    
    # DB
    "mysql" = "db_mysql"
    "mysql-patterns" = "db_mysql-patterns"
    "adbc" = "db_adbc"
    "redis-observability" = "db_redis-observability"
    
    # Utilities
    "skill-installer" = "util_skill-installer"
    "create-pull-request" = "util_create-pull-request"
    "csv-wrangling" = "util_csv-wrangling"
    "document-ocr" = "util_document-ocr"
    "webapp-testing" = "util_webapp-testing"
}

# ============================================================
# CREATE ALIAS SKILL FILES
# ============================================================

Write-Host "Creating Skill Aliases..." -ForegroundColor White
Write-Host "----------------------------------------"
Write-Host ""

$SkillsRoot = Join-Path $CursorRoot ".cursor\skills"
$AliasesCreated = 0

foreach ($old in $SkillAliases.Keys) {
    $newName = $SkillAliases[$old]
    $oldPath = Join-Path $SkillsRoot $old
    $newPath = Join-Path $SkillsRoot $newName
    
    # Check if new path exists
    if (Test-Path $newPath) {
        # Create redirect file for backward compatibility
        if (-not (Test-Path $oldPath)) {
            if ($DryRun) {
                Write-Step "Would create alias: $old -> $newName"
            } else {
                Write-Step "Creating alias: $old -> $newName"
                try {
                    # Create directory
                    New-Item -Path $oldPath -ItemType Directory -Force | Out-Null
                    
                    # Create redirect SKILL.md
                    $aliasContent = @"
# Alias: $old

**DEPRECATED**: This skill has been renamed to `$newName`.

For backward compatibility, this alias redirects to the new skill.

## Migration

Update your code to use:
```
.cursor/skills/$newName/SKILL.md
```

## Auto-Redirect

This alias is maintained for backward compatibility.
The skill-registry will automatically redirect to the new name.

---
Auto-generated alias file
Last updated: $(Get-Date -Format "yyyy-MM-dd")
"@
                    $aliasFile = Join-Path $oldPath "SKILL.md"
                    Set-Content -Path $aliasFile -Value $aliasContent -Encoding UTF8
                    Write-Created "Alias created: $old -> $newName"
                    $AliasesCreated++
                } catch {
                    Write-Warning "Failed to create alias $old"
                }
            }
        }
    }
}

Write-Host ""
Write-Host "Skill aliases: $AliasesCreated created" -ForegroundColor Green

# ============================================================
# CREATE COMPATIBILITY DOCUMENT
# ============================================================

Write-Host ""
Write-Host "Creating Compatibility Guide..." -ForegroundColor White
Write-Host "----------------------------------------"
Write-Host ""

$compatContent = @"
# Backward Compatibility Guide

> **Version:** 2.0.0  
> **Created:** $(Get-Date -Format "yyyy-MM-dd")  
> **Purpose:** Maintain backward compatibility after renaming

## Overview

In v2.0, all skills and rules have been renamed with prefix system:
- Skills: `ui_`, `code_`, `sec_`, `ai_`, `doc_`, `db_`, etc.
- Rules: `rule_`, `proto_`, `ref_`, `meta_`

For backward compatibility, aliases are maintained.

## Skill Aliases

| Old Name | New Name | Status |
|----------|----------|--------|
| `landing-page-pro` | `ui_landing-page-pro` | Alias maintained |
| `dashboard-ui` | `ui_dashboard-ui` | Alias maintained |
| `frontend-taste` | `ui_frontend-taste` | Alias maintained |
| `hallmark` | `ui_hallmark` | Alias maintained |
| `frontend-redesign` | `ui_frontend-redesign` | Alias maintained |
| `frontend-review` | `ui_frontend-review` | Alias maintained |
| `karpathy-coding` | `code_karpathy` | Alias maintained |
| `ponytail` | `code_ponytail` | Alias maintained |
| `full-output` | `code_full-output` | Alias maintained |
| `security-review` | `sec_security-review` | Alias maintained |
| `vietnam-payment-review` | `sec_vietnam-payment-review` | Alias maintained |
| `weknora-kb` | `ai_weknora-kb` | Alias maintained |
| `video-generation` | `ai_video-generation` | Alias maintained |

## Rule Aliases

| Old Name | New Name | Status |
|----------|----------|--------|
| `skill-registry` | `rule_skill-registry` | Alias maintained |
| `skill-integration` | `rule_skill-integration` | Alias maintained |
| `task-analyzer` | `rule_task-analyzer` | Alias maintained |
| `intent-detection` | `rule_intent-detection` | Alias maintained |

## Migration Path

### Old Way (v1)
```
.cursor/skills/landing-page-pro/SKILL.md
.cursor/skills/security-review/SKILL.md
.cursor/rules/skill-registry.mdc
```

### New Way (v2)
```
.cursor/skills/ui_landing-page-pro/SKILL.md
.cursor/skills/sec_security-review/SKILL.md
.cursor/rules/rule_skill-registry.mdc
```

## Auto-Detection

The skill-registry automatically handles both old and new names:
- Old names are aliased to new names
- References are auto-updated in skill-registry
- No code changes required for backward compatibility

## Deprecation Timeline

| Date | Change |
|------|--------|
| 2026-08-03 | v2.0 released with prefixes |
| 2026-10-01 | Alias warnings enabled |
| 2027-01-01 | Old names deprecated |
| 2027-06-01 | Old names removed |

## Benefits of New Naming

1. **Prefix-based discovery**: Easy to find skills by domain
2. **Auto-routing**: Keywords map directly to prefixes
3. **Namespace isolation**: No naming conflicts
4. **Scalability**: Add new domains without confusion

## Files Changed

- All skills renamed with prefix
- All rules renamed with prefix
- `NAMING-CONVENTION.md` created
- `COMPATIBILITY.md` (this file) created
- Alias links created for backward compatibility

## Support

For questions or issues with migration, see:
- `NAMING-CONVENTION.md` - Full naming guide
- `.cursor/rules/rule_skill-registry.mdc` - Skill definitions
- `.cursor/INDEX.md` - Skill index with new names
"@

$compatFile = Join-Path $CursorRoot ".cursor\COMPATIBILITY.md"

if ($DryRun) {
    Write-Step "Would create: COMPATIBILITY.md"
} else {
    Set-Content -Path $compatFile -Value $compatContent -Encoding UTF8
    Write-Created "Created: COMPATIBILITY.md"
}

Write-Host ""
Write-Host "========================================"
Write-Host "  COMPATIBILITY LAYER COMPLETED"
Write-Host "========================================"
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN MODE - No actual changes were made" -ForegroundColor Yellow
} else {
    Write-Host "Compatibility layer created successfully" -ForegroundColor Green
}
