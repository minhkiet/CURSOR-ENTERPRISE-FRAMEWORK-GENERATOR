# ============================================================
# PROJECT INDEX BUILDER SCRIPT
# ============================================================
# Purpose: Build and update project index
# Language: PowerShell
# Created: 2026-06-23
# ============================================================

param(
    [string]$ProjectRoot = ".",
    [string]$OutputPath = ".cursor/memory/project-index.md",
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "INFO" { "White" }
        "WARN" { "Yellow" }
        "ERROR" { "Red" }
        "SUCCESS" { "Green" }
        default { "White" }
    }
    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color
}

function Get-CodePatterns {
    param([string]$Root)

    $patterns = @()

    # Frontend patterns
    $frontendFiles = @("package.json", "next.config.*", "nuxt.config.*", "vite.config.*", "tailwind.config.*")
    if ($frontendFiles | ForEach-Object { Test-Path (Join-Path $Root $_) } | Where-Object { $_ }) {
        $patterns += @{
            category = "frontend"
            type = "config"
            files = @($frontendFiles | Where-Object { Test-Path (Join-Path $Root $_) })
        }
    }

    # Backend patterns
    $backendPatterns = @(
        @{ path = "composer.json"; type = "laravel" },
        @{ path = "*.csproj"; type = "aspnet-core" },
        @{ path = "package.json"; type = "nestjs" },
        @{ path = "requirements.txt"; type = "python" }
    )
    foreach ($bp in $backendPatterns) {
        $found = Get-ChildItem -Path $Root -Filter $bp.path -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) {
            $patterns += @{
                category = "backend"
                type = $bp.type
                root = $found.DirectoryName
            }
        }
    }

    # Database patterns
    $dbPatterns = @("migrations/**", "*.sql", "schema/**")
    $patterns += @{ category = "database"; patterns = $dbPatterns }

    # Docker patterns
    if (Test-Path (Join-Path $Root "Dockerfile")) {
        $patterns += @{ category = "docker"; files = @("Dockerfile", "docker-compose*.yml") }
    }

    return $patterns
}

function Build-ProjectIndex {
    param([string]$Root)

    $index = @{
        metadata = @{
            generated_at = (Get-Date).ToString("o")
            version = "1.0.0"
            project_root = $Root
        }
        framework = @{
            cursor_version = "latest"
            compatibility = @("cursor", "claude-code", "vibe-code", "windsurf", "cline", "roo-code")
        }
        patterns = Get-CodePatterns -Root $Root
        rules = @{
            count = (Get-ChildItem -Path ".cursor/rules" -Filter "*.mdc" -ErrorAction SilentlyContinue | Measure-Object).Count
            path = ".cursor/rules"
        }
        skills = @{
            count = (Get-ChildItem -Path ".cursor/skills" -Filter "*.mdc" -ErrorAction SilentlyContinue | Measure-Object).Count
            path = ".cursor/skills"
        }
        knowledge = @{
            domains = @()
            total_files = 0
            path = ".cursor/knowledge"
        }
        prompts = @{
            count = (Get-ChildItem -Path ".cursor/prompts" -Filter "*.md" -ErrorAction SilentlyContinue | Measure-Object).Count
            path = ".cursor/prompts"
        }
        workflows = @{
            count = (Get-ChildItem -Path ".cursor/workflows" -Filter "*.md" -ErrorAction SilentlyContinue | Measure-Object).Count
            path = ".cursor/workflows"
        }
        memory = @{
            databases = @("decisions", "bugs", "prompt-cache", "knowledge", "embeddings", "sessions")
            path = ".cursor/memory"
        }
    }

    # Count knowledge domains
    $knowledgeDomains = Get-ChildItem -Path ".cursor/knowledge" -Directory -ErrorAction SilentlyContinue
    $index.knowledge.domains = @($knowledgeDomains | ForEach-Object { $_.Name })
    foreach ($domain in $knowledgeDomains) {
        $files = Get-ChildItem -Path $domain.FullName -Filter "*.md" -Recurse -ErrorAction SilentlyContinue
        $index.knowledge.total_files += $files.Count
    }

    return $index
}

Write-Log "Building project index..."
$index = Build-ProjectIndex -Root $ProjectRoot

$outputDir = Split-Path $OutputPath -Parent
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

$json = $index | ConvertTo-Json -Depth 10
$json | Out-File -FilePath $OutputPath -Encoding UTF8

Write-Log "Project index built successfully!" "SUCCESS"
Write-Log "Rules: $($index.rules.count)"
Write-Log "Skills: $($index.skills.count)"
Write-Log "Knowledge domains: $($index.knowledge.domains.Count)"
Write-Log "Knowledge files: $($index.knowledge.total_files)"
Write-Log "Prompts: $($index.prompts.count)"
Write-Log "Workflows: $($index.workflows.count)"
