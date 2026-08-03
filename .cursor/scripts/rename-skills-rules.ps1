# Rename-SkillsAndRules.ps1
# Script de rename skills va rules voi prefix system moi
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

function Write-Done {
    param([string]$Message)
    Write-Host "  [OK] $Message" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================"
Write-Host "  RENAME SCRIPT v2.0"
Write-Host "========================================"
Write-Host ""

# ============================================================
# SKILLS RENAME MAPPING
# ============================================================

$SkillRenames = @{
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
    "web-design-guidelines" = "ui_web-design-guidelines"

    # Code & Development
    "karpathy-coding" = "code_karpathy"
    "ponytail" = "code_ponytail"
    "full-output" = "code_full-output"
    "vibe-coding" = "code_vibe-coding"

    # Document & Writing
    "ai-copywriter" = "doc_ai-copywriter"
    "book-to-skill" = "doc_book-to-skill"
    "simple-english" = "doc_simple-english"
    "microsoft-docs" = "doc_microsoft-docs"

    # Database
    "mysql" = "db_mysql"
    "mysql-patterns" = "db_mysql-patterns"
    "sql-server-table-reconciliation" = "db_sql-server-table-reconciliation"
    "adbc" = "db_adbc"
    "redis-observability" = "db_redis-observability"

    # Infrastructure
    "deploy-to-vercel" = "infra_deploy-vercel"
    "docker" = "infra_docker"
    "prefect" = "infra_prefect"

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
    "chatbotx-feature" = "ai_chatbotx-feature"
    "chatbotx-database" = "ai_chatbotx-database"
    "chatbotx-worker" = "ai_chatbotx-worker"

    # Special
    "bazi" = "special_bazi"
    "vietnam-address" = "special_vietnam-address"

    # Utilities
    "skill-installer" = "util_skill-installer"
    "create-pull-request" = "util_create-pull-request"
    "csv-wrangling" = "util_csv-wrangling"
    "document-ocr" = "util_document-ocr"
    "webapp-testing" = "util_webapp-testing"
}

# ============================================================
# RULES RENAME MAPPING
# ============================================================

$RuleRenames = @{
    # Core Rules
    "skill-registry" = "rule_skill-registry"
    "skill-integration" = "rule_skill-integration"
    "task-analyzer" = "rule_task-analyzer"
    "intent-detection" = "rule_intent-detection"
    "memory-first" = "proto_memory-first"
    "context-router" = "proto_context-router"

    # Protocols
    "multi-language-processing" = "proto_multi-language-processing"
    "multi-language-vibe-code" = "proto_multi-language-vibe-code"

    # References
    "architecture-patterns" = "ref_architecture-patterns"
    "frontend-frameworks" = "ref_frontend-frameworks"
    "backend-frameworks" = "ref_backend-frameworks"
    "enterprise-patterns" = "ref_enterprise-patterns"
    "api-patterns" = "ref_api-patterns"
    "database-patterns" = "ref_database-patterns"

    # Meta/Config
    "coding-standards" = "meta_coding-standards"
    "deployment" = "meta_deployment"
    "auth" = "meta_auth"
    "security" = "meta_security"
    "billing" = "meta_billing"
    "crm-saas" = "meta_crm-saas"
    "multi-tenant" = "meta_multi-tenant"
    "observability" = "meta_observability"
    "performance" = "meta_performance"
    "cloud-providers" = "meta_cloud-providers"
    "cloud-infra" = "meta_cloud-infra"
    "container-orchestration" = "meta_container-orchestration"
    "serverless" = "meta_serverless"
    "workflow-engines" = "meta_workflow-engines"
    "redis" = "meta_redis"
    "cost-optimization" = "meta_cost-optimization"
    "chatbot-development" = "meta_chatbot-development"
    "ai-knowledge" = "meta_ai-knowledge"
    "testing" = "meta_testing"
    "version-control" = "meta_version-control"
    "vibe-code-protocol" = "meta_vibe-code-protocol"
    "operations" = "meta_operations"
    "cloudflare" = "meta_cloudflare"
}

# ============================================================
# EXECUTE RENAME
# ============================================================

Write-Host "Phase 1: Renaming Skills" -ForegroundColor White
Write-Host "----------------------------------------"

$SkillsRoot = Join-Path $CursorRoot ".cursor\skills"
$SkillsRenamed = 0
$SkillsSkipped = 0

foreach ($old in $SkillRenames.Keys) {
    $oldPath = Join-Path $SkillsRoot $old
    $newName = $SkillRenames[$old]

    if (Test-Path $oldPath) {
        if ($DryRun) {
            Write-Step "Would rename: $old -> $newName"
        } else {
            Write-Step "Renaming: $old -> $newName"
            try {
                Rename-Item -Path $oldPath -NewName $newName -ErrorAction Stop
                Write-Done "Renamed: $old -> $newName"
                $SkillsRenamed++
            } catch {
                Write-Warning "Failed to rename $old"
                $SkillsSkipped++
            }
        }
    } else {
        if ($Verbose) {
            Write-Step "Not found (skipped): $old"
        }
        $SkillsSkipped++
    }
}

Write-Host ""
Write-Host "Skills: $SkillsRenamed renamed, $SkillsSkipped skipped" -ForegroundColor Green

Write-Host ""
Write-Host "Phase 2: Renaming Rules" -ForegroundColor White
Write-Host "----------------------------------------"

$RulesRoot = Join-Path $CursorRoot ".cursor\rules"
$RulesRenamed = 0
$RulesSkipped = 0

foreach ($old in $RuleRenames.Keys) {
    $oldMdc = Join-Path $RulesRoot "$old.mdc"
    $oldMd = Join-Path $RulesRoot "$old.md"
    $newName = $RuleRenames[$old]

    $renamed = $false

    if (Test-Path $oldMdc) {
        if ($DryRun) {
            Write-Step "Would rename: $old.mdc -> $newName.mdc"
        } else {
            Write-Step "Renaming: $old.mdc -> $newName.mdc"
            try {
                Rename-Item -Path $oldMdc -NewName "$newName.mdc" -ErrorAction Stop
                Write-Done "Renamed: $old.mdc -> $newName.mdc"
                $renamed = $true
                $RulesRenamed++
            } catch {
                Write-Warning "Failed to rename $old.mdc"
            }
        }
    }

    if ((Test-Path $oldMd) -and (-not $renamed)) {
        if ($DryRun) {
            Write-Step "Would rename: $old.md -> $newName.md"
        } else {
            Write-Step "Renaming: $old.md -> $newName.md"
            try {
                Rename-Item -Path $oldMd -NewName "$newName.md" -ErrorAction Stop
                Write-Done "Renamed: $old.md -> $newName.md"
                $RulesRenamed++
            } catch {
                Write-Warning "Failed to rename $old.md"
            }
        }
    }

    if ((-not $renamed) -and (-not (Test-Path $oldMdc)) -and (-not (Test-Path $oldMd))) {
        if ($Verbose) {
            Write-Step "Not found (skipped): $old"
        }
        $RulesSkipped++
    }
}

Write-Host ""
Write-Host "Rules: $RulesRenamed renamed, $RulesSkipped skipped" -ForegroundColor Green

Write-Host ""
Write-Host "========================================"
Write-Host "  RENAME COMPLETED"
Write-Host "========================================"
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN MODE - No actual changes were made" -ForegroundColor Yellow
    Write-Host "Remove -DryRun flag to execute actual rename" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Update skill-registry.mdc with new paths"
Write-Host "  2. Update .cursorrules references"
Write-Host "  3. Update AGENTS.md references"
Write-Host "  4. Update INDEX.md and INDEX.json"
Write-Host "  5. Run update-references.ps1 to update all internal references"
