# Hooks Installer for Cursor Framework
# Installs git hooks for automatic framework operations

param(
    [switch]$Uninstall,
    [switch]$All,
    [ValidateSet("pre-commit", "post-commit", "pre-push")]
    [string[]]$Hooks = @("pre-commit", "post-commit", "pre-push")
)

$ErrorActionPreference = "Stop"

$HOOKS_DIR = ".git\hooks"
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Cursor Framework Hooks Installer" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Detect shell type
$isBash = $PSVersionTable.Platform -eq "Unix" -or $env:SHELL -match "bash"
$isWindows = $PSVersionTable.Platform -eq "Win32NT" -or -not $isBash

if ($Uninstall) {
    Write-Host "Uninstalling hooks..." -ForegroundColor Yellow
    
    foreach ($hook in $Hooks) {
        $hookPath = Join-Path $HOOKS_DIR "$hook"
        
        if ($isBash) {
            $backupPath = "$hookPath.backup"
            if (Test-Path $backupPath) {
                Move-Item $backupPath $hookPath -Force
                Write-Host "Restored: $hook" -ForegroundColor Green
            }
        } else {
            # PowerShell - check for marker
            if (Test-Path $hookPath) {
                $content = Get-Content $hookPath -Raw -ErrorAction SilentlyContinue
                if ($content -match "Cursor Framework") {
                    Remove-Item $hookPath -Force
                    Write-Host "Removed: $hook" -ForegroundColor Green
                }
            }
        }
    }
    
    Write-Host ""
    Write-Host "Uninstallation complete!" -ForegroundColor Green
    exit 0
}

# Install hooks
Write-Host "Installing hooks to: $HOOKS_DIR" -ForegroundColor Cyan
Write-Host ""

# Ensure hooks directory exists
if (-not (Test-Path $HOOKS_DIR)) {
    New-Item -ItemType Directory -Path $HOOKS_DIR -Force | Out-Null
}

foreach ($hook in $Hooks) {
    $hookSource = Join-Path $SCRIPT_DIR "$hook.ps1"
    $hookDest = Join-Path $HOOKS_DIR $hook
    
    if ($isBash) {
        # Bash/Linux/macOS - use shell scripts
        $shellSource = Join-Path $SCRIPT_DIR $hook
        
        if (Test-Path $shellSource) {
            # Backup existing hook
            if (Test-Path $hookDest) {
                Move-Item $hookDest "$hookDest.backup" -Force
            }
            
            # Copy and make executable
            Copy-Item $shellSource $hookDest
            chmod +x $hookDest
            
            Write-Host "Installed: $hook (shell)" -ForegroundColor Green
        }
    } else {
        # Windows PowerShell - create wrapper
        $wrapperContent = @"
# Cursor Framework Hook: $hook
# Generated at $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

# Run PowerShell hook
powershell.exe -ExecutionPolicy Bypass -File "$SCRIPT_DIR\$hook.ps1"

# Exit with hook's exit code
exit `$LASTEXITCODE
"@
        
        # For pre-commit, also check shell script for Git Bash
        if ($hook -eq "pre-commit" -and (Test-Path "$SCRIPT_DIR\pre-commit")) {
            $wrapperContent = @"
#!/bin/bash
# Cursor Framework Hook: $hook
# Generated at $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

# Run shell script if bash is available
if command -v bash &> /dev/null; then
    bash "$SCRIPT_DIR\$hook"
else
    # Fallback to PowerShell
    powershell.exe -ExecutionPolicy Bypass -File "$SCRIPT_DIR\$hook.ps1"
fi

exit `$?
"@
        }
        
        Set-Content -Path $hookDest -Value $wrapperContent -Force
        Write-Host "Installed: $hook (PowerShell)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Installation complete!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Available commands:" -ForegroundColor Cyan
Write-Host "  .\hooks\install-hooks.ps1          # Install all hooks"
Write-Host "  .\hooks\install-hooks.ps1 -Uninstall  # Remove hooks"
Write-Host "  .\hooks\install-hooks.ps1 -Hooks pre-commit  # Install specific hook"
Write-Host ""

# Show hook details
Write-Host "Installed hooks:" -ForegroundColor Cyan
foreach ($hook in $Hooks) {
    $hookDest = Join-Path $HOOKS_DIR $hook
    if (Test-Path $hookDest) {
        Write-Host "  ✓ $hook" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $hook (failed)" -ForegroundColor Red
    }
}
