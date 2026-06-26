# WeKnora MCP Configuration Generator

# Generates Cursor MCP configuration for WeKnora integration

param(
    [string]$WeKnoraHost = "http://localhost:8080",
    [string]$WeKnoraApiKey = "",
    [string]$Transport = "stdio",  # stdio, sse, http
    [switch]$AddToCursor,
    [switch]$ShowConfig
)

$ErrorActionPreference = "Stop"

# Colors for output
function Write-Step { param($Message) Write-Host "[STEP] $Message" -ForegroundColor Cyan }
function Write-Success { param($Message) Write-Host "[OK] $Message" -ForegroundColor Green }
function Write-Info { param($Message) Write-Host "[INFO] $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "[ERROR] $Message" -ForegroundColor Red }

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║       WeKnora MCP Configuration Generator for Cursor           ║" -ForegroundColor Magenta
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

# Step 1: Check prerequisites
Write-Step "Checking prerequisites..."

# Check if weknora CLI is installed
$weknoraCmd = Get-Command weknora -ErrorAction SilentlyContinue
if ($weknoraCmd) {
    $version = & weknora --version 2>$null
    Write-Success "WeKnora CLI installed: $version"
} else {
    Write-Info "WeKnora CLI not found. Will generate config for manual setup."
}

# Check Cursor directory
$cursorDir = "$env:USERPROFILE\.cursor"
if (Test-Path $cursorDir) {
    Write-Success "Cursor config directory found: $cursorDir"
} else {
    Write-Info "Creating Cursor config directory..."
    New-Item -ItemType Directory -Path $cursorDir -Force | Out-Null
}

# Step 2: Get WeKnora connection details
Write-Host ""
Write-Step "WeKnora Connection Configuration"

if ([string]::IsNullOrEmpty($WeKnoraApiKey)) {
    Write-Host "Please enter your WeKnora API Key: " -NoNewline
    $WeKnoraApiKey = Read-Host
}

# Step 3: Generate MCP configuration
Write-Host ""
Write-Step "Generating MCP Configuration..."

$config = @{
    mcpServers = @{
        weknora = @{
            command = "weknora"
            args = @("mcp", "serve")
            env = @{
                WEKNORA_HOST = $WeKnoraHost
                WEKNORA_API_KEY = $WeKnoraApiKey
            }
        }
    }
} | ConvertTo-Json -Depth 5

# Format JSON nicely
$formattedConfig = $config | ConvertFrom-Json | ConvertTo-Json -Depth 5

Write-Host ""
Write-Host "Generated Configuration:" -ForegroundColor White
Write-Host "────────────────────────────────────────" -ForegroundColor Gray
Write-Host $formattedConfig
Write-Host "────────────────────────────────────────" -ForegroundColor Gray

# Step 4: Save configuration
Write-Step "Saving Configuration..."

$mcpConfigPath = Join-Path $cursorDir "mcp.json"

# Check if mcp.json exists and merge
if (Test-Path $mcpConfigPath) {
    Write-Info "Existing mcp.json found. Merging..."
    
    $existingConfig = Get-Content $mcpConfigPath -Raw | ConvertFrom-Json
    
    # Add weknora to existing servers
    $existingServers = $existingConfig.mcpServers
    if (-not $existingServers) {
        $existingConfig | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value (@{}.PSObject.BaseObject) -Force
    }
    
    $existingConfig.mcpServers | Add-Member -MemberType NoteProperty -Name "weknora" -Value $config.mcpServers.weknora -Force
    
    $existingConfig | ConvertTo-Json -Depth 10 | Set-Content $mcpConfigPath -Encoding UTF8
} else {
    # Create new config
    $config | ConvertTo-Json -Depth 10 | Set-Content $mcpConfigPath -Encoding UTF8
}

Write-Success "Configuration saved to: $mcpConfigPath"

# Step 5: Show next steps
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║                    Next Steps                               ║" -ForegroundColor Magenta
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""
Write-Host "1. Restart Cursor to load the MCP configuration"
Write-Host ""
Write-Host "2. If WeKnora is not running, start it:"
Write-Host "   git clone https://github.com/Tencent/WeKnora.git"
Write-Host "   cd WeKnora"
Write-Host "   cp .env.example .env"
Write-Host "   # Edit .env with your settings"
Write-Host "   docker compose up -d"
Write-Host ""
Write-Host "3. Verify MCP connection in Cursor:"
Write-Host "   - Open Cursor Settings"
Write-Host "   - Go to MCP Servers"
Write-Host "   - Check that 'weknora' shows as connected"
Write-Host ""

# Show config if requested
if ($ShowConfig) {
    Write-Host ""
    Write-Host "Full Configuration:" -ForegroundColor White
    Get-Content $mcpConfigPath | Write-Host
}

Write-Host ""
Write-Success "Configuration complete!"
