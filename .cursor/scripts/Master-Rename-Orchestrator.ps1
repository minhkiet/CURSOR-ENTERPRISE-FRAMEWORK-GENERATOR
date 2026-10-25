# Master-Rename-Orchestrator.ps1
# Orchestrator script để chạy toàn bộ quá trình rename với prefix system
# Version: 2.0.0 - 2026-08-03

param(
    [switch]$DryRun,
    [switch]$Verbose,
    [switch]$SkipRename,
    [switch]$SkipRefs,
    [switch]$SkipCompat
)

$ErrorActionPreference = "Stop"

function Write-Banner {
    param([string]$Text)
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║  $Text" -ForegroundColor Magenta
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
    Write-Host ""
}

Write-Banner "CURSOR ENTERPRISE FRAMEWORK - RENAME ORCHESTRATOR v2.0"

$ScriptRoot = $PSScriptRoot
$CursorRoot = Split-Path $ScriptRoot -Parent

Write-Host "Cursor Root: $CursorRoot" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# PRE-FLIGHT CHECK
# ============================================================

Write-Host "Phase 0: Pre-flight Check" -ForegroundColor White
Write-Host "=" * 60 -ForegroundColor Gray
Write-Host ""

# Check if we're in a git repo
$isGitRepo = Test-Path (Join-Path $CursorRoot ".git")
if ($isGitRepo) {
    Write-Host "  ✓ Git repository detected" -ForegroundColor Green
    
    # Check for uncommitted changes
    $status = git status --porcelain 2>$null
    if ($status) {
        Write-Host ""
        Write-Host "  ⚠ WARNING: Uncommitted changes detected!" -ForegroundColor Yellow
        Write-Host "  Consider committing before proceeding" -ForegroundColor Yellow
        Write-Host ""
        $response = Read-Host "Continue anyway? (y/N)"
        if ($response -ne 'y' -and $response -ne 'Y') {
            Write-Host "Aborted." -ForegroundColor Red
            exit 0
        }
    }
} else {
    Write-Host "  ⚠ Not a git repository - backup recommended" -ForegroundColor Yellow
}

# Backup reminder
Write-Host ""
Write-Host "  📦 RECOMMENDED: Create backup before proceeding" -ForegroundColor Cyan
Write-Host "  Run: git backup or copy .cursor folder manually" -ForegroundColor Gray
Write-Host ""

if (-not $DryRun) {
    $response = Read-Host "Continue with rename? (y/N)"
    if ($response -ne 'y' -and $response -ne 'Y') {
        Write-Host "Aborted." -ForegroundColor Red
        exit 0
    }
}

# ============================================================
# PHASE 1: RENAME FOLDERS
# ============================================================

if (-not $SkipRename) {
    Write-Banner "PHASE 1: RENAME FOLDERS"
    
    & (Join-Path $ScriptRoot "rename-skills-rules.ps1") -DryRun:$DryRun -Verbose:$Verbose
} else {
    Write-Host "Phase 1: SKIPPED (--SkipRename)" -ForegroundColor Yellow
}

# ============================================================
# PHASE 2: UPDATE REFERENCES
# ============================================================

if (-not $SkipRefs) {
    Write-Banner "PHASE 2: UPDATE REFERENCES"
    
    # Run Python script for skill-registry
    $pythonScript = Join-Path $ScriptRoot "update-skill-registry.py"
    if (Test-Path $pythonScript) {
        Write-Host "Running: update-skill-registry.py" -ForegroundColor Cyan
        if (-not $DryRun) {
            python $pythonScript
        } else {
            Write-Host "  (DRY RUN - skipped)" -ForegroundColor Yellow
        }
    }
    
    # Run PowerShell script for other files
    & (Join-Path $ScriptRoot "update-references.ps1") -DryRun:$DryRun -Verbose:$Verbose
} else {
    Write-Host "Phase 2: SKIPPED (--SkipRefs)" -ForegroundColor Yellow
}

# ============================================================
# PHASE 3: CREATE COMPATIBILITY LAYER
# ============================================================

if (-not $SkipCompat) {
    Write-Banner "PHASE 3: CREATE COMPATIBILITY LAYER"
    
    & (Join-Path $ScriptRoot "create-compatibility-layer.ps1") -DryRun:$DryRun -Verbose:$Verbose
} else {
    Write-Host "Phase 3: SKIPPED (--SkipCompat)" -ForegroundColor Yellow
}

# ============================================================
# SUMMARY
# ============================================================

Write-Banner "RENAME COMPLETE"

if ($DryRun) {
    Write-Host "DRY RUN MODE - No actual changes were made" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To apply changes, run without -DryRun flag:" -ForegroundColor White
    Write-Host "  .\.cursor\scripts\Master-Rename-Orchestrator.ps1" -ForegroundColor Gray
} else {
    Write-Host "✓ All phases completed successfully" -ForegroundColor Green
    Write-Host ""
    Write-Host "Files have been renamed:" -ForegroundColor White
    Write-Host "  - Skills folders with prefix (ui_, code_, sec_, ai_, etc.)" -ForegroundColor Gray
    Write-Host "  - Rules files with prefix (rule_, proto_, ref_)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Documents created:" -ForegroundColor White
    Write-Host "  - NAMING-CONVENTION.md - Full naming guide" -ForegroundColor Gray
    Write-Host "  - COMPATIBILITY.md - Backward compatibility guide" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Scripts created:" -ForegroundColor White
    Write-Host "  - rename-skills-rules.ps1 - Rename folders" -ForegroundColor Gray
    Write-Host "  - update-references.ps1 - Update references" -ForegroundColor Gray
    Write-Host "  - create-compatibility-layer.ps1 - Create aliases" -ForegroundColor Gray
    Write-Host "  - update-skill-registry.py - Update skill-registry" -ForegroundColor Gray
}

Write-Host ""
Write-Host "REVIEW REQUIRED:" -ForegroundColor Yellow
Write-Host "  1. Review all renamed folders in .cursor/skills/" -ForegroundColor Gray
Write-Host "  2. Review all renamed files in .cursor/rules/" -ForegroundColor Gray
Write-Host "  3. Check .cursorrules references" -ForegroundColor Gray
Write-Host "  4. Check AGENTS.md references" -ForegroundColor Gray
Write-Host "  5. Test skill loading" -ForegroundColor Gray
Write-Host ""

# ============================================================
# GIT COMMIT SUGGESTION
# ============================================================

if ($isGitRepo -and -not $DryRun) {
    Write-Host "To commit changes:" -ForegroundColor White
    Write-Host '  git add -A' -ForegroundColor Gray
    Write-Host '  git commit -m "refactor: rename skills and rules with prefix system v2.0"' -ForegroundColor Gray
    Write-Host '  git tag -a v2.0.0 -m "Prefix system v2.0"' -ForegroundColor Gray
    Write-Host '  git push origin main --tags' -ForegroundColor Gray
}
