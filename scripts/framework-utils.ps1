# Framework Utils - PowerShell Utilities for Cursor Framework
# Quick access to common framework operations

param(
    [Parameter(Position=0)]
    [ValidateSet("warm", "stats", "scan", "index", "clear", "dashboard", "graph", "skills", "help")]
    [string]$Command = "help",
    
    [switch]$Force,
    [switch]$Json,
    [int]$Port = 8765
)

$ErrorActionPreference = "Continue"
$FRAMEWORK_ROOT = ".cursor"
$MEMORY_PATH = ".cache/memory.json"

# Colors
function Write-Status {
    param([string]$Message, [string]$Type = "info")
    switch ($Type) {
        "success" { Write-Host "[OK] $Message" -ForegroundColor Green }
        "error" { Write-Host "[ERROR] $Message" -ForegroundColor Red }
        "warning" { Write-Host "[WARN] $Message" -ForegroundColor Yellow }
        "info" { Write-Host "[INFO] $Message" -ForegroundColor Cyan }
    }
}

# Check Python
function Test-Python {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        $python = Get-Command python3 -ErrorAction SilentlyContinue
    }
    return $python
}

# Run framework command
function Invoke-Framework {
    param([string]$Cmd, [switch]$Silent)
    $python = Test-Python
    if (-not $python) {
        Write-Status "Python not found" "error"
        return $null
    }
    
    $output = & $python -m cursor_framework $Cmd --root $FRAMEWORK_ROOT 2>&1
    if (-not $Silent) {
        if ($LASTEXITCODE -eq 0) {
            return $output
        } else {
            Write-Status "Command failed: $output" "error"
            return $null
        }
    }
    return $output
}

# Header
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host "  Cursor Framework Utilities" -ForegroundColor Magenta
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host ""

switch ($Command) {
    "warm" {
        Write-Host "Warming framework cache..." -ForegroundColor Yellow
        $result = Invoke-Framework "warm"
        if ($result) {
            Write-Status "Cache warmed successfully" "success"
            if ($Json -or $result -match "^\{") {
                $result | ConvertFrom-Json | ConvertTo-Json -Depth 5
            } else {
                Write-Host $result
            }
        }
    }
    
    "stats" {
        Write-Host "Fetching framework statistics..." -ForegroundColor Yellow
        $result = Invoke-Framework "stats"
        if ($result) {
            Write-Status "Statistics retrieved" "success"
            if ($result -match "^\{") {
                $stats = $result | ConvertFrom-Json
                Write-Host ""
                Write-Host "  Assets Indexed:  $($stats.assets_indexed)" -ForegroundColor White
                Write-Host "  Memory Hits:    $($stats.memory_hits)" -ForegroundColor White
                Write-Host "  Memory Misses: $($stats.memory_misses)" -ForegroundColor White
                Write-Host "  Tokens Saved:   $($stats.tokens_saved)" -ForegroundColor White
                Write-Host "  Cache Files:   $($stats.cache_files)" -ForegroundColor White
                Write-Host ""
            } else {
                Write-Host $result
            }
        }
    }
    
    "scan" {
        Write-Host "Scanning .cursor/ directory..." -ForegroundColor Yellow
        $result = Invoke-Framework "scan"
        if ($result) {
            Write-Status "Scan complete" "success"
            if ($result -match "^\{") {
                $scan = $result | ConvertFrom-Json
                Write-Host ""
                Write-Host "  Grand Total: $($scan.totals.grand_total) assets" -ForegroundColor White
                foreach ($key in $scan.totals.PSObject.Properties | Where-Object { $_.Name -ne "grand_total" }) {
                    Write-Host "  $($key.Name): $($key.Value)" -ForegroundColor White
                }
                Write-Host ""
            } else {
                Write-Host $result
            }
        }
    }
    
    "index" {
        Write-Host "Rebuilding framework index..." -ForegroundColor Yellow
        $result = Invoke-Framework "index"
        if ($result) {
            Write-Status "Index rebuilt" "success"
            Write-Host ""
            if ($result -match "^\{") {
                $index = $result | ConvertFrom-Json
                Write-Host "  Root: $($index.root)" -ForegroundColor White
                Write-Host "  Total Assets: $($index.assets)" -ForegroundColor White
            } else {
                Write-Host $result
            }
        }
    }
    
    "clear" {
        Write-Host "Clearing framework cache..." -ForegroundColor Yellow
        if ($Force) {
            $result = Invoke-Framework "clear-cache --force"
            if ($result -match '"deleted"') {
                $data = $result | ConvertFrom-Json
                Write-Status "Cache cleared" "success"
                foreach ($file in $data.deleted) {
                    Write-Host "  Deleted: $file" -ForegroundColor DarkGray
                }
            }
        } else {
            Write-Host "Dry-run mode (use -Force to actually delete):" -ForegroundColor Yellow
            $result = Invoke-Framework "clear-cache"
            if ($result -match '"would_delete"') {
                $data = $result | ConvertFrom-Json
                foreach ($file in $data.would_delete) {
                    Write-Host "  Would delete: $file" -ForegroundColor DarkGray
                }
            }
        }
    }
    
    "dashboard" {
        Write-Host "Starting dashboard server..." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Dashboard will open at: http://localhost:$Port" -ForegroundColor Green
        Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
        Write-Host ""
        
        # Start dashboard in background
        $python = Test-Python
        $job = Start-Job -ScriptBlock {
            param($py, $p, $root)
            & $py -m cursor_framework serve --port $p --root $root
        } -ArgumentList $python.Source, $Port, $FRAMEWORK_ROOT
        
        # Wait a moment for server to start
        Start-Sleep -Seconds 2
        
        # Open browser
        Start-Process "http://localhost:$Port"
        
        # Wait for job or interrupt
        Wait-Job $job -Timeout 300 | Out-Null
    }
    
    "graph" {
        $graphPort = $Port + 1
        Write-Host "Starting graph visualization server..." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Graph will open at: http://localhost:$graphPort" -ForegroundColor Green
        Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
        Write-Host ""
        
        $python = Test-Python
        $job = Start-Job -ScriptBlock {
            param($py, $p, $root)
            & $py -m cursor_framework serve-graph --port $p --root $root
        } -ArgumentList $python.Source, $graphPort, $FRAMEWORK_ROOT
        
        Start-Sleep -Seconds 2
        Start-Process "http://localhost:$graphPort"
        
        Wait-Job $job -Timeout 300 | Out-Null
    }
    
    "skills" {
        Write-Host "Discovering skills..." -ForegroundColor Yellow
        $result = Invoke-Framework "scan"
        if ($result) {
            Write-Status "Skills scanned" "success"
            Write-Host ""
            
            # Parse and display skills
            $scan = $result | ConvertFrom-Json
            Write-Host "Available Skills:" -ForegroundColor Green
            Write-Host "  Total: $($scan.totals.skills)" -ForegroundColor White
            Write-Host "  Rules: $($scan.totals.rules)" -ForegroundColor White
            Write-Host "  Agents: $($scan.totals.agents)" -ForegroundColor White
            Write-Host ""
        }
    }
    
    "help" {
        Write-Host "Available Commands:" -ForegroundColor Green
        Write-Host ""
        Write-Host "  warm     - Warm framework cache (scan + persist)" -ForegroundColor White
        Write-Host "  stats    - Show framework statistics" -ForegroundColor White
        Write-Host "  scan     - Quick scan of .cursor/" -ForegroundColor White
        Write-Host "  index    - Full scan and persist INDEX" -ForegroundColor White
        Write-Host "  clear    - Clear cache (use -Force to delete)" -ForegroundColor White
        Write-Host "  dashboard - Open framework dashboard" -ForegroundColor White
        Write-Host "  graph    - Open skill dependency graph" -ForegroundColor White
        Write-Host "  skills   - Discover available skills" -ForegroundColor White
        Write-Host ""
        Write-Host "Examples:" -ForegroundColor Green
        Write-Host "  .\framework-utils.ps1 warm" -ForegroundColor DarkGray
        Write-Host "  .\framework-utils.ps1 stats -Json" -ForegroundColor DarkGray
        Write-Host "  .\framework-utils.ps1 clear -Force" -ForegroundColor DarkGray
        Write-Host ""
    }
}

Write-Host ""
