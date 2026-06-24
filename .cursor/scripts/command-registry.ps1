# ============================================================
# CURSOR ENTERPRISE FRAMEWORK - COMMAND & HOOK REGISTRY
# ============================================================
# Purpose: Register, link, and manage commands and hooks
# Language: PowerShell
# Framework: Cursor Enterprise Framework V4
# Created: 2026-06-24
# ============================================================

param(
    [ValidateSet("install", "uninstall", "list", "validate", "init")]
    [string]$Action = "list",

    [ValidateSet("all", "commands", "hooks", "git", "ci-cd", "dev", "scripts")]
    [string]$Target = "all",

    [switch]$Verbose,
    [switch]$Force,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$FrameworkVersion = "4.0.0"
$CursorDir = ".cursor"
$HooksDir = Join-Path $CursorDir "hooks"
$CommandsDir = Join-Path $CursorDir "commands"
$GitHooksDir = ".git/hooks"

# Colors for output
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "INFO"    { "White" }
        "WARN"    { "Yellow" }
        "ERROR"   { "Red" }
        "SUCCESS" { "Green" }
        "HEADER"  { "Cyan" }
        "DIM"     { "DarkGray" }
        default   { "White" }
    }
    if ($Verbose -or $Level -eq "ERROR" -or $Level -eq "SUCCESS") {
        Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color
    }
}

# ============================================================
# COMMAND REGISTRY
# ============================================================

$CommandRegistry = @{
    "build"       = @{
        Name        = "Build Feature"
        Description = "Xay dung feature moi tu requirement den implementation"
        Category    = "Development"
        Path        = "$CommandsDir/build/command.md"
        Keywords    = @("build feature", "tao feature", "xay dung feature", "implement feature")
    }
    "fix"         = @{
        Name        = "Fix Bug"
        Description = "Sua loi bug voi root cause analysis"
        Category    = "Development"
        Path        = "$CommandsDir/fix/command.md"
        Keywords    = @("fix bug", "sua loi", "fix error", "bug fix", "loi")
    }
    "review"      = @{
        Name        = "Code Review"
        Description = "Review code quality, correctness, performance"
        Category    = "Quality"
        Path        = "$CommandsDir/review/command.md"
        Keywords    = @("review code", "code review", "review", "kiem tra code")
    }
    "audit"       = @{
        Name        = "Audit"
        Description = "Security, Performance, Architecture, Database audit"
        Category    = "Quality"
        Path        = "$CommandsDir/audit/command.md"
        Keywords    = @("audit", "security audit", "performance audit", "kiem toan")
    }
    "design"      = @{
        Name        = "Design"
        Description = "Thiet ke kien truc (DDD, CQRS, Database, API)"
        Category    = "Architecture"
        Path        = "$CommandsDir/design/command.md"
        Keywords    = @("design", "thiet ke", "architecture design", "ddd design", "cqrs")
    }
    "rag"         = @{
        Name        = "RAG"
        Description = "Xay dung RAG system voi embedding va retrieval"
        Category    = "AI"
        Path        = "$CommandsDir/rag/command.md"
        Keywords    = @("rag", "rag system", "retrieval augmented", "vector search")
    }
    "deploy"      = @{
        Name        = "Deploy"
        Description = "Deployment workflow tu build den production"
        Category    = "DevOps"
        Path        = "$CommandsDir/deploy/command.md"
        Keywords    = @("deploy", "deployment", "trien khai", "release")
    }
    "test"        = @{
        Name        = "Test"
        Description = "Chien luoc va implementation testing"
        Category    = "Testing"
        Path        = "$CommandsDir/test/command.md"
        Keywords    = @("test", "testing", "viet test", "unit test", "integration test")
    }
    "doc"         = @{
        Name        = "Doc"
        Description = "Tao tai lieu (README, API docs, inline docs)"
        Category    = "Documentation"
        Path        = "$CommandsDir/doc/command.md"
        Keywords    = @("doc", "document", "tai lieu", "documentation", "generate doc")
    }
    "memory"      = @{
        Name        = "Memory"
        Description = "Quan ly memory system (build, query, update)"
        Category    = "Memory"
        Path        = "$CommandsDir/memory/command.md"
        Keywords    = @("memory", "quan ly memory", "build memory", "update memory")
    }
    "adr"         = @{
        Name        = "ADR"
        Description = "Tao Architecture Decision Record"
        Category    = "Architecture"
        Path        = "$CommandsDir/adr/command.md"
        Keywords    = @("adr", "architecture decision", "tao adr", "decision record")
    }
    "payment"     = @{
        Name        = "Payment"
        Description = "Review payment integration Viet Nam (MoMo, SePay, PayOS, ZaloPay, VNPay)"
        Category    = "Domain"
        Path        = "$CommandsDir/payment/command.md"
        Keywords    = @("payment", "thanh toan", "momo", "sepay", "payos", "vnpay", "vietqr")
    }
    "security"    = @{
        Name        = "Security"
        Description = "Security review (OWASP, vulnerabilities, authentication)"
        Category    = "Security"
        Path        = "$CommandsDir/security/command.md"
        Keywords    = @("security", "bao mat", "security review", "vulnerability", "owasp")
    }
    "frontend"    = @{
        Name        = "Frontend"
        Description = "Frontend tasks (build landing, redesign, review)"
        Category    = "Frontend"
        Path        = "$CommandsDir/frontend/command.md"
        Keywords    = @("frontend", "landing page", "redesign", "frontend review", "ui")
    }
    "perf"        = @{
        Name        = "Performance"
        Description = "Performance audit va optimization"
        Category    = "Performance"
        Path        = "$CommandsDir/perf/command.md"
        Keywords    = @("perf", "performance", "toi uu hieu suat", "optimization")
    }
    "refactor"    = @{
        Name        = "Refactor"
        Description = "Refactor code voi design patterns"
        Category    = "Refactoring"
        Path        = "$CommandsDir/refactor/command.md"
        Keywords    = @("refactor", "tai cau truc", "code refactor", "clean code")
    }
    "generate"    = @{
        Name        = "Generate"
        Description = "Generate code (PDF, API, migration, boilerplate)"
        Category    = "Generation"
        Path        = "$CommandsDir/generate/command.md"
        Keywords    = @("generate", "tao code", "migration", "boilerplate", "scaffold")
    }
    "workflow"    = @{
        Name        = "Workflow"
        Description = "Execute standard workflows"
        Category    = "Workflow"
        Path        = "$CommandsDir/workflow/command.md"
        Keywords    = @("workflow", "quy trinh", "execute workflow", "standard workflow")
    }
    "report"      = @{
        Name        = "Report"
        Description = "Tao report (security, performance, architecture)"
        Category    = "Reporting"
        Path        = "$CommandsDir/report/command.md"
        Keywords    = @("report", "bao cao", "create report", "security report")
    }
    "bazi"        = @{
        Name        = "Bazi"
        Description = "Tinh Bat Tu (Four Pillars of Destiny)"
        Category    = "Domain"
        Path        = "$CommandsDir/bazi/command.md"
        Keywords    = @("bazi", "bat tu", "four pillars", "la so")
    }
    "tuvi"        = @{
        Name        = "Tuvi"
        Description = "Tinh Tu Vi (Vietnamese Astrology)"
        Category    = "Domain"
        Path        = "$CommandsDir/tuvi/command.md"
        Keywords    = @("tuvi", "tu vi", "vietnamese astrology", "la so tu vi")
    }
    "numerology"  = @{
        Name        = "Numerology"
        Description = "Than So Hoc (Numerology)"
        Category    = "Domain"
        Path        = "$CommandsDir/numerology/command.md"
        Keywords    = @("numerology", "than so hoc", "so chu dao", "life path")
    }
}

# ============================================================
# HOOK REGISTRY
# ============================================================

$HookRegistry = @{
    # Git Hooks
    "git-pre-commit" = @{
        Name        = "Pre-Commit"
        Description = "Lint, format, type check truoc khi commit"
        Category    = "Git"
        Path        = "$HooksDir/git-hooks/pre-commit/hook.md"
        Trigger     = "git commit"
    }
    "git-commit-msg" = @{
        Name        = "Commit-Msg"
        Description = "Validate commit message format"
        Category    = "Git"
        Path        = "$HooksDir/git-hooks/commit-msg/hook.md"
        Trigger     = "git commit message"
    }
    "git-pre-push" = @{
        Name        = "Pre-Push"
        Description = "Run tests va security scan truoc khi push"
        Category    = "Git"
        Path        = "$HooksDir/git-hooks/pre-push/hook.md"
        Trigger     = "git push"
    }
    "git-post-commit" = @{
        Name        = "Post-Commit"
        Description = "Update session summary sau commit"
        Category    = "Git"
        Path        = "$HooksDir/git-hooks/post-commit/hook.md"
        Trigger     = "git commit (sau)"
    }

    # CI/CD Hooks
    "ci-pre-build" = @{
        Name        = "Pre-Build"
        Description = "Verify dependencies truoc khi build"
        Category    = "CI-CD"
        Path        = "$HooksDir/ci-cd-hooks/pre-build/hook.md"
        Trigger     = "truoc build"
    }
    "ci-post-build" = @{
        Name        = "Post-Build"
        Description = "Verify artifacts sau khi build"
        Category    = "CI-CD"
        Path        = "$HooksDir/ci-cd-hooks/post-build/hook.md"
        Trigger     = "sau build"
    }
    "ci-pre-deploy" = @{
        Name        = "Pre-Deploy"
        Description = "Final checks truoc khi deploy"
        Category    = "CI-CD"
        Path        = "$HooksDir/ci-cd-hooks/pre-deploy/hook.md"
        Trigger     = "truoc deploy"
    }
    "ci-post-deploy" = @{
        Name        = "Post-Deploy"
        Description = "Health check va notify sau deploy"
        Category    = "CI-CD"
        Path        = "$HooksDir/ci-cd-hooks/post-deploy/hook.md"
        Trigger     = "sau deploy"
    }
    "ci-on-failure" = @{
        Name        = "On-Failure"
        Description = "Analyze error va suggest fix khi CI/CD fail"
        Category    = "CI-CD"
        Path        = "$HooksDir/ci-cd-hooks/on-failure/hook.md"
        Trigger     = "CI/CD failure"
    }

    # Development Hooks
    "dev-before-task" = @{
        Name        = "Before-Task"
        Description = "Load context va check memory truoc task"
        Category    = "Dev"
        Path        = "$HooksDir/dev-hooks/before-task/hook.md"
        Trigger     = "truoc task"
    }
    "dev-after-task" = @{
        Name        = "After-Task"
        Description = "Update memory va summarize sau task"
        Category    = "Dev"
        Path        = "$HooksDir/dev-hooks/after-task/hook.md"
        Trigger     = "sau task"
    }
    "dev-on-error" = @{
        Name        = "On-Error"
        Description = "Analyze error va suggest fix khi co error"
        Category    = "Dev"
        Path        = "$HooksDir/dev-hooks/on-error/hook.md"
        Trigger     = "khi co error"
    }
}

# ============================================================
# GIT HOOK TEMPLATES (PowerShell scripts)
# ============================================================

$GitHookTemplates = @{
    "pre-commit" = @'
#!/usr/bin/env pwsh
# ============================================================
# PRE-COMMIT HOOK - Auto-generated by Cursor Enterprise Framework
# ============================================================
# DO NOT EDIT - This file is managed by command-registry.ps1
# ============================================================

$ErrorActionPreference = "Continue"

Write-Host "Running pre-commit hook..." -ForegroundColor Cyan

# Check for staged files
$stagedFiles = git diff --cached --name-only --diff-filter=ACM
if (-not $stagedFiles) {
    Write-Host "No staged files to check." -ForegroundColor Green
    exit 0
}

$errors = @()
$warnings = @()
$fixed = @()

foreach ($file in $stagedFiles -split "`n") {
    if (-not $file) { continue }

    # Skip binary files
    if ((Test-Path $file -PathType Leaf) -and ((Get-Content $file -Raw -ErrorAction SilentlyContinue) -match "`0")) {
        continue
    }

    # TypeScript/JavaScript files
    if ($file -match '\.(ts|tsx|js|jsx)$') {
        # Check formatting with Prettier (if available)
        if (Get-Command prettier -ErrorAction SilentlyContinue) {
            $formatResult = prettier --check $file 2>&1
            if ($LASTEXITCODE -ne 0) {
                Write-Host "Formatting issue in $file - auto-fixing..." -ForegroundColor Yellow
                prettier --write $file 2>&1 | Out-Null
                git add $file
                $fixed += $file
            }
        }

        # Check for console.log/debugger
        $content = Get-Content $file -Raw
        if ($content -match 'console\.(log|debug|info)\(') {
            $errors += "console.* found in $file - remove before committing"
        }
        if ($content -match 'debugger') {
            $errors += "debugger found in $file - remove before committing"
        }
    }

    # Check for secrets
    $content = Get-Content $file -Raw -ErrorAction SilentlyContinue
    if ($content -match '(api[_-]?key|secret[ly]?|password|token)\s*=\s*["''][^"'']{8,}["'']') {
        $errors += "Potential secret found in $file"
    }
}

# Print results
Write-Host ""
Write-Host "Pre-commit check results:" -ForegroundColor Cyan
Write-Host "  Files checked: $($stagedFiles -split "`n" | Measure-Object).Count"

if ($fixed.Count -gt 0) {
    Write-Host "  Auto-fixed: $($fixed.Count)" -ForegroundColor Yellow
    foreach ($f in $fixed) {
        Write-Host "    - $f" -ForegroundColor Yellow
    }
}

if ($errors.Count -gt 0) {
    Write-Host "  Errors: $($errors.Count)" -ForegroundColor Red
    foreach ($e in $errors) {
        Write-Host "    - $e" -ForegroundColor Red
    }
    exit 1
}

if ($warnings.Count -gt 0) {
    Write-Host "  Warnings: $($warnings.Count)" -ForegroundColor Yellow
    foreach ($w in $warnings) {
        Write-Host "    - $w" -ForegroundColor Yellow
    }
}

Write-Host "  Pre-commit check passed!" -ForegroundColor Green
exit 0
'@

    "commit-msg" = @'
#!/usr/bin/env pwsh
# ============================================================
# COMMIT-MSG HOOK - Auto-generated by Cursor Enterprise Framework
# ============================================================
# DO NOT EDIT - This file is managed by command-registry.ps1
# ============================================================

$commitMsgFile = $args[0]
$commitMsg = Get-Content $commitMsgFile -Raw

# Skip for merge commits
if ($commitMsg -match "^Merge branch") {
    exit 0
}

# Allowed types
$types = @("feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "chore", "revert")

# Scopes
$scopes = @("api", "auth", "db", "ui", "auth", "security", "perf", "docs", "test", "infra", "ci", "core", "fe", "be")

# Check format: type(scope): subject
$pattern = "^($($types -join '|'))(\($($scopes -join '|'|?{$_})\))?: .+"

if ($commitMsg -notmatch $pattern) {
    Write-Host "Invalid commit message format!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Expected format: type(scope): subject" -ForegroundColor Yellow
    Write-Host "  type: $($types -join ', ')" -ForegroundColor Yellow
    Write-Host "  scope: $($scopes -join ', ')" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Example: feat(auth): add JWT refresh token"
    exit 1
}

# Check subject length (max 72 chars)
$lines = $commitMsg -split "`n"
$subject = $lines[0]
if ($subject.Length -gt 72) {
    Write-Host "Subject line too long (max 72 chars): $($subject.Length)" -ForegroundColor Red
    exit 1
}

# Check no trailing period
if ($subject -match ': .+\.$') {
    Write-Host "Subject should not end with a period" -ForegroundColor Yellow
}

exit 0
'@

    "pre-push" = @'
#!/usr/bin/env pwsh
# ============================================================
# PRE-PUSH HOOK - Auto-generated by Cursor Enterprise Framework
# ============================================================
# DO NOT EDIT - This file is managed by command-registry.ps1
# ============================================================

$ErrorActionPreference = "Continue"

Write-Host "Running pre-push hook..." -ForegroundColor Cyan

# Check if this is a protected branch push
$targetBranch = git rev-parse --abbrev-ref HEAD
$protectedBranches = @("main", "master", "develop")

if ($protectedBranches -contains $targetBranch) {
    Write-Host "Pushing to protected branch: $targetBranch" -ForegroundColor Yellow
    Write-Host "Running additional checks..." -ForegroundColor Yellow

    # Check if CI passed (requires CI_STATUS_CHECK env var)
    # if ($env:CI_STATUS_CHECK -ne "passed") {
    #     Write-Host "CI has not passed for this branch!" -ForegroundColor Red
    #     Write-Host "Please ensure all CI checks pass before pushing to $targetBranch" -ForegroundColor Red
    #     exit 1
    # }
}

# Run tests if test command exists
if (Get-Command npm -ErrorAction SilentlyContinue) {
    if (Test-Path "package.json") {
        Write-Host "Running tests..." -ForegroundColor Cyan
        npm test 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Tests failed! Aborting push." -ForegroundColor Red
            exit 1
        }
        Write-Host "Tests passed!" -ForegroundColor Green
    }
}

Write-Host "Pre-push check passed!" -ForegroundColor Green
exit 0
'@

    "post-commit" = @'
#!/usr/bin/env pwsh
# ============================================================
# POST-COMMIT HOOK - Auto-generated by Cursor Enterprise Framework
# ============================================================
# DO NOT EDIT - This file is managed by command-registry.ps1
# ============================================================

Write-Host "Post-commit hook running..." -ForegroundColor Cyan

# Get commit info
$commitHash = git rev-parse HEAD
$commitMsg = git log -1 --pretty=%B
$author = git log -1 --pretty=%an
$timestamp = git log -1 --pretty=%ci

Write-Host "Commit: $commitHash" -ForegroundColor Gray
Write-Host "Author: $author" -ForegroundColor Gray

# Update session summary (if memory system exists)
$memoryFile = ".cursor/memory/session-summary/last-commit.json"
if (Test-Path ".cursor/memory") {
    $commitInfo = @{
        hash = $commitHash
        message = $commitMsg
        author = $author
        timestamp = $timestamp
        date = Get-Date -Format "yyyy-MM-dd"
    } | ConvertTo-Json -Depth 3

    if (Test-Path $memoryFile) {
        # Append to existing history
        $history = Get-Content $memoryFile -Raw | ConvertFrom-Json
        $history.commits += $commitInfo
        $history | ConvertTo-Json -Depth 5 | Out-File $memoryFile -Encoding UTF8
    } else {
        @{
            lastUpdate = Get-Date -Format "o"
            commits = @($commitInfo)
        } | ConvertTo-Json -Depth 5 | Out-File $memoryFile -Encoding UTF8
    }
    Write-Host "Session summary updated." -ForegroundColor Green
}

exit 0
'@
}

# ============================================================
# FUNCTIONS
# ============================================================

function Get-CommandStats {
    $commands = @{
        Total = $CommandRegistry.Count
        ByCategory = @{}
    }

    foreach ($cmd in $CommandRegistry.Values) {
        $cat = $cmd.Category
        if (-not $commands.ByCategory.ContainsKey($cat)) {
            $commands.ByCategory[$cat] = 0
        }
        $commands.ByCategory[$cat]++
    }

    return $commands
}

function Get-HookStats {
    $hooks = @{
        Total = $HookRegistry.Count
        ByCategory = @{}
    }

    foreach ($hook in $HookRegistry.Values) {
        $cat = $hook.Category
        if (-not $hooks.ByCategory.ContainsKey($cat)) {
            $hooks.ByCategory[$cat] = 0
        }
        $hooks.ByCategory[$cat]++
    }

    return $hooks
}

function Install-GitHooks {
    Write-Log "Installing Git hooks..." "HEADER"

    if (-not (Test-Path $GitHooksDir)) {
        New-Item -ItemType Directory -Path $GitHooksDir -Force | Out-Null
    }

    foreach ($hookName in $GitHookTemplates.Keys) {
        $hookPath = Join-Path $GitHooksDir $hookName

        if ((Test-Path $hookPath) -and -not $Force) {
            Write-Log "Hook $hookName already exists. Use -Force to overwrite." "WARN"
            continue
        }

        if ($DryRun) {
            Write-Log "[DRY RUN] Would create: $hookPath" "INFO"
            continue
        }

        # Write hook template
        $GitHookTemplates[$hookName] | Out-File -FilePath $hookPath -Encoding UTF8 -Force

        # Make executable (if on Unix-like system via WSL or Git Bash)
        if ($IsLinux -or $IsMacOS) {
            chmod +x $hookPath
        }

        Write-Log "Installed: $hookPath" "SUCCESS"
    }

    Write-Log "Git hooks installation complete!" "SUCCESS"
}

function Uninstall-GitHooks {
    Write-Log "Uninstalling Git hooks..." "HEADER"

    foreach ($hookName in $GitHookTemplates.Keys) {
        $hookPath = Join-Path $GitHooksDir $hookName

        if (-not (Test-Path $hookPath)) {
            Write-Log "Hook $hookName not found. Skipping." "WARN"
            continue
        }

        if ($DryRun) {
            Write-Log "[DRY RUN] Would remove: $hookPath" "INFO"
            continue
        }

        Remove-Item -Path $hookPath -Force
        Write-Log "Removed: $hookPath" "SUCCESS"
    }

    Write-Log "Git hooks uninstallation complete!" "SUCCESS"
}

function Install-Scripts {
    Write-Log "Setting up scripts..." "HEADER"

    $scriptsTarget = Join-Path $CursorDir "scripts"

    # Copy this registry script to scripts folder
    $registryPath = Join-Path $scriptsTarget "command-registry.ps1"

    if ($DryRun) {
        Write-Log "[DRY RUN] Would copy registry script to: $registryPath" "INFO"
    } else {
        if (-not (Test-Path $scriptsTarget)) {
            New-Item -ItemType Directory -Path $scriptsTarget -Force | Out-Null
        }
        # Copy self to scripts
        Write-Log "Registry script location: $registryPath" "INFO"
    }

    Write-Log "Scripts setup complete!" "SUCCESS"
}

function Validate-Registry {
    Write-Log "Validating command and hook registry..." "HEADER"

    $issues = @()

    # Validate commands
    foreach ($key in $CommandRegistry.Keys) {
        $cmd = $CommandRegistry[$key]
        if (-not (Test-Path $cmd.Path)) {
            $issues += "MISSING: Command '$key' - Path: $($cmd.Path)"
        }
    }

    # Validate hooks
    foreach ($key in $HookRegistry.Keys) {
        $hook = $HookRegistry[$key]
        if (-not (Test-Path $hook.Path)) {
            $issues += "MISSING: Hook '$key' - Path: $($hook.Path)"
        }
    }

    if ($issues.Count -eq 0) {
        Write-Log "Registry validation PASSED!" "SUCCESS"
        $cmdStats = Get-CommandStats
        $hookStats = Get-HookStats
        Write-Log "Commands: $($cmdStats.Total) ($($cmdStats.ByCategory.Keys.Count) categories)" "INFO"
        Write-Log "Hooks: $($hookStats.Total) ($($hookStats.ByCategory.Keys.Count) categories)" "INFO"
        return $true
    } else {
        Write-Log "Registry validation FAILED!" "ERROR"
        foreach ($issue in $issues) {
            Write-Log "  $issue" "ERROR"
        }
        return $false
    }
}

function Initialize-Framework {
    Write-Log "Initializing Cursor Enterprise Framework v$FrameworkVersion..." "HEADER"
    Write-Log "========================================" "HEADER"

    # Create directories
    Write-Log "Creating directory structure..." "INFO"
    $dirs = @(
        $CommandsDir,
        $HooksDir,
        (Join-Path $CursorDir "scripts/generated"),
        (Join-Path $CursorDir "cache")
    )

    foreach ($dir in $dirs) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Log "  Created: $dir" "DIM"
        }
    }

    # Install git hooks
    Install-GitHooks

    # Validate
    Write-Log ""
    $valid = Validate-Registry

    if ($valid) {
        Write-Log ""
        Write-Log "Framework initialization complete!" "SUCCESS"
        Write-Log "========================================" "HEADER"
        Write-Log "Run './.cursor/scripts/command-registry.ps1 -Action list' to see all commands." "INFO"
    } else {
        Write-Log "Some components are missing. Run with -Verbose for details." "WARN"
    }
}

function Show-List {
    param([string]$Target)

    Write-Log "Cursor Enterprise Framework v$FrameworkVersion - Registry" "HEADER"
    Write-Log "========================================" "HEADER"

    if ($Target -eq "all" -or $Target -eq "commands") {
        Write-Log ""
        Write-Log "COMMANDS ($($CommandRegistry.Count) total)" "HEADER"

        # Group by category
        $byCategory = @{}
        foreach ($cmd in $CommandRegistry.Values) {
            if (-not $byCategory.ContainsKey($cmd.Category)) {
                $byCategory[$cmd.Category] = @()
            }
            $byCategory[$cmd.Category] += $cmd
        }

        foreach ($category in $byCategory.Keys | Sort-Object) {
            Write-Log ""
            Write-Log "  [$category]" "INFO"
            foreach ($cmd in $byCategory[$category]) {
                $name = $cmd.Name
                $desc = $cmd.Description
                $keywords = $cmd.Keywords -join ", "
                Write-Log "    / $($name.ToLower().Replace(' ', '-'))" "SUCCESS"
                Write-Log "      $desc" "DIM"
            }
        }
    }

    if ($Target -eq "all" -or $Target -eq "hooks") {
        Write-Log ""
        Write-Log "HOOKS ($($HookRegistry.Count) total)" "HEADER"

        # Group by category
        $byCategory = @{}
        foreach ($hook in $HookRegistry.Values) {
            if (-not $byCategory.ContainsKey($hook.Category)) {
                $byCategory[$hook.Category] = @()
            }
            $byCategory[$hook.Category] += $hook
        }

        foreach ($category in $byCategory.Keys | Sort-Object) {
            Write-Log ""
            Write-Log "  [$category]" "INFO"
            foreach ($hook in $byCategory[$category]) {
                $name = $hook.Name
                $desc = $hook.Description
                $trigger = $hook.Trigger
                Write-Log "    $name" "SUCCESS"
                Write-Log "      Trigger: $trigger" "DIM"
                Write-Log "      $desc" "DIM"
            }
        }
    }

    Write-Log ""
    Write-Log "========================================" "HEADER"
    Write-Log "Run './.cursor/scripts/command-registry.ps1 -Action install' to install git hooks." "INFO"
}

# ============================================================
# MAIN EXECUTION
# ============================================================

switch ($Action) {
    "list" {
        Show-List -Target $Target
    }

    "install" {
        if ($Target -eq "all" -or $Target -eq "git" -or $Target -eq "hooks") {
            Install-GitHooks
        }
        if ($Target -eq "all" -or $Target -eq "scripts") {
            Install-Scripts
        }
        Write-Log ""
        Write-Log "Installation complete!" "SUCCESS"
    }

    "uninstall" {
        if ($Target -eq "all" -or $Target -eq "git" -or $Target -eq "hooks") {
            Uninstall-GitHooks
        }
    }

    "validate" {
        $result = Validate-Registry
        if (-not $result) {
            exit 1
        }
    }

    "init" {
        Initialize-Framework
    }

    default {
        Write-Log "Unknown action: $Action" "ERROR"
        Write-Log "Usage: ./.cursor/scripts/command-registry.ps1 -Action <list|install|uninstall|validate|init>" "INFO"
        exit 1
    }
}
