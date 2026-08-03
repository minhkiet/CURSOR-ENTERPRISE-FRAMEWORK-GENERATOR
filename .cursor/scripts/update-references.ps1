# Update-References.ps1
# Script de update tat ca references sau khi rename skills va rules
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

function Write-Updated {
    param([string]$File, [int]$Count)
    Write-Host "  [OK] $File ($Count updates)" -ForegroundColor Green
}

function Update-FileReferences {
    param(
        [string]$FilePath,
        [hashtable]$SkillMappings,
        [hashtable]$RuleMappings
    )
    
    if (-not (Test-Path $FilePath)) {
        Write-Step "File not found: $FilePath"
        return 0
    }
    
    $content = Get-Content $FilePath -Raw -Encoding UTF8
    $originalContent = $content
    $updateCount = 0
    
    # Update skill references
    foreach ($old in $SkillMappings.Keys) {
        $new = $SkillMappings[$old]
        
        # Pattern: .cursor/skills/OLD-NAME/
        $pattern = "\.cursor[/\\]skills[/\\]" + [regex]::Escape($old)
        $replacement = ".cursor/skills/$new"
        
        if ($content -match $pattern) {
            $content = $content -replace $pattern, $replacement
            $updateCount++
        }
        
        # Pattern: skills/OLD-NAME/
        $pattern = "skills[/\\]" + [regex]::Escape($old) + "[/\\]"
        $replacement = "skills/$new/"
        
        if ($content -match $pattern) {
            $content = $content -replace $pattern, $replacement
            $updateCount++
        }
        
        # Pattern: OLD-NAME/SKILL.md
        $pattern = [regex]::Escape($old) + "[/\\]SKILL\.md"
        $replacement = "$new/SKILL.md"
        
        if ($content -match $pattern) {
            $content = $content -replace $pattern, $replacement
            $updateCount++
        }
    }
    
    # Update rule references
    foreach ($old in $RuleMappings.Keys) {
        $new = $RuleMappings[$old]
        
        # Pattern: .cursor/rules/OLD-NAME.mdc
        $pattern = "\.cursor[/\\]rules[/\\]" + [regex]::Escape($old) + "\.mdc"
        $replacement = ".cursor/rules/$new.mdc"
        
        if ($content -match $pattern) {
            $content = $content -replace $pattern, $replacement
            $updateCount++
        }
        
        # Pattern: [[OLD-NAME]]
        $pattern = "\[\[" + [regex]::Escape($old) + "\]\]"
        $replacement = "[[$new]]"
        
        if ($content -match $pattern) {
            $content = $content -replace $pattern, $replacement
            $updateCount++
        }
    }
    
    if ($updateCount -gt 0 -and $content -ne $originalContent) {
        if ($DryRun) {
            Write-Step "Would update: $FilePath ($updateCount changes)"
        } else {
            Set-Content -Path $FilePath -Value $content -Encoding UTF8 -NoNewline
            Write-Updated $FilePath $updateCount
        }
    }
    
    return $updateCount
}

Write-Host ""
Write-Host "========================================"
Write-Host "  UPDATE REFERENCES SCRIPT v2.0"
Write-Host "========================================"
Write-Host ""

# ============================================================
# MAPPING TABLES
# ============================================================

$SkillMappings = @{
    # UI & Visual Design
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
    
    # Code & Development
    "karpathy-coding" = "code_karpathy"
    "ponytail" = "code_ponytail"
    "full-output" = "code_full-output"
    "vibe-coding" = "code_vibe-coding"
    
    # Document & Writing
    "ai-copywriter" = "doc_ai-copywriter"
    "book-to-skill" = "doc_book-to-skill"
    "simple-english" = "doc_simple-english"
    
    # Database
    "mysql" = "db_mysql"
    "mysql-patterns" = "db_mysql-patterns"
    "adbc" = "db_adbc"
    
    # Security
    "security-review" = "sec_security-review"
    "vietnam-payment-review" = "sec_vietnam-payment-review"
    
    # Performance
    "vercel-react-best-practices" = "perf_react-best-practices"
    "vercel-composition-patterns" = "perf_composition-patterns"
    
    # AI & Agent
    "weknora-kb" = "ai_weknora-kb"
    "weknora-agent" = "ai_weknora-agent"
    "pixelrag" = "ai_pixelrag"
    "video-generation" = "ai_video-generation"
    
    # Special
    "bazi" = "special_bazi"
    "vietnam-address" = "special_vietnam-address"
    
    # Utilities
    "skill-installer" = "util_skill-installer"
    "create-pull-request" = "util_create-pull-request"
    "csv-wrangling" = "util_csv-wrangling"
    "document-ocr" = "util_document-ocr"
}

$RuleMappings = @{
    # Core Rules
    "skill-registry" = "rule_skill-registry"
    "skill-integration" = "rule_skill-integration"
    "task-analyzer" = "rule_task-analyzer"
    "intent-detection" = "rule_intent-detection"
    
    # Protocols
    "multi-language-processing" = "proto_multi-language-processing"
    "multi-language-vibe-code" = "proto_multi-language-vibe-code"
    "context-router" = "proto_context-router"
    "memory-first" = "proto_memory-first"
    
    # References
    "architecture-patterns" = "ref_architecture-patterns"
    "frontend-frameworks" = "ref_frontend-frameworks"
    "backend-frameworks" = "ref_backend-frameworks"
}

# ============================================================
# FILES TO UPDATE
# ============================================================

Write-Host "Phase 1: Updating SKILL.md files" -ForegroundColor White
Write-Host "----------------------------------------"
Write-Host ""

$SkillsRoot = Join-Path $CursorRoot ".cursor\skills"
$TotalUpdates = 0

# Get all SKILL.md files
$skillFiles = Get-ChildItem -Path $SkillsRoot -Recurse -Filter "SKILL.md" -File

foreach ($file in $skillFiles) {
    $count = Update-FileReferences -FilePath $file.FullName -SkillMappings $SkillMappings -RuleMappings $RuleMappings
    $TotalUpdates += $count
}

Write-Host ""
Write-Host "SKILL.md files: $TotalUpdates total updates" -ForegroundColor Green

Write-Host ""
Write-Host "Phase 2: Updating Rules files" -ForegroundColor White
Write-Host "----------------------------------------"
Write-Host ""

$RulesRoot = Join-Path $CursorRoot ".cursor\rules"
$rulesFiles = Get-ChildItem -Path $RulesRoot -Filter "*.mdc" -File

foreach ($file in $rulesFiles) {
    $count = Update-FileReferences -FilePath $file.FullName -SkillMappings $SkillMappings -RuleMappings $RuleMappings
    $TotalUpdates += $count
}

Write-Host ""
Write-Host "Rules files: $TotalUpdates total updates" -ForegroundColor Green

Write-Host ""
Write-Host "Phase 3: Updating Root files" -ForegroundColor White
Write-Host "----------------------------------------"
Write-Host ""

$RootFiles = @(
    (Join-Path $CursorRoot ".cursorrules"),
    (Join-Path $CursorRoot ".cursor\AGENTS.md"),
    (Join-Path $CursorRoot ".cursor\INDEX.md"),
    (Join-Path $CursorRoot ".cursor\PROJECT.md"),
    (Join-Path $CursorRoot ".cursor\NAMING-CONVENTION.md")
)

foreach ($file in $RootFiles) {
    if (Test-Path $file) {
        $count = Update-FileReferences -FilePath $file -SkillMappings $SkillMappings -RuleMappings $RuleMappings
        $TotalUpdates += $count
    }
}

Write-Host ""
Write-Host "Root files: $TotalUpdates total updates" -ForegroundColor Green

Write-Host ""
Write-Host "========================================"
Write-Host "  REFERENCES UPDATE COMPLETED"
Write-Host "========================================"
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN MODE - No actual changes were made" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Total updates made: $TotalUpdates" -ForegroundColor White
