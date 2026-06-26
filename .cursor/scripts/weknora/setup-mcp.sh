#!/bin/bash
# WeKnora MCP Configuration Generator for Cursor
# Generates and installs MCP configuration for WeKnora integration

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Default values
WEKNORA_HOST="http://localhost:8080"
TRANSPORT="stdio"
CURSOR_DIR="$HOME/.cursor"

print_header() {
    echo -e "${MAGENTA}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║       WeKnora MCP Configuration Generator for Cursor          ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${CYAN}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --host)
            WEKNORA_HOST="$2"
            shift 2
            ;;
        --api-key)
            WEKNORA_API_KEY="$2"
            shift 2
            ;;
        --transport)
            TRANSPORT="$2"
            shift 2
            ;;
        --cursor-dir)
            CURSOR_DIR="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --host HOST           WeKnora host URL (default: http://localhost:8080)"
            echo "  --api-key KEY         WeKnora API key"
            echo "  --transport TYPE      MCP transport type: stdio, sse, http (default: stdio)"
            echo "  --cursor-dir DIR     Cursor config directory (default: ~/.cursor)"
            echo "  --show-config        Show generated configuration"
            echo "  --help               Show this help message"
            exit 0
            ;;
        --show-config)
            SHOW_CONFIG=true
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

print_header

# Step 1: Check prerequisites
print_step "Checking prerequisites..."

# Check if weknora CLI is installed
if command -v weknora &> /dev/null; then
    VERSION=$(weknora --version 2>/dev/null || echo "unknown")
    print_success "WeKnora CLI installed: $VERSION"
else
    print_info "WeKnora CLI not found. Will generate config for manual setup."
fi

# Check Cursor directory
if [ -d "$CURSOR_DIR" ]; then
    print_success "Cursor config directory found: $CURSOR_DIR"
else
    print_info "Creating Cursor config directory..."
    mkdir -p "$CURSOR_DIR"
fi

# Step 2: Get API key if not provided
print_step "WeKnora Connection Configuration"

if [ -z "$WEKNORA_API_KEY" ]; then
    echo -n "Please enter your WeKnora API Key: "
    read -s WEKNORA_API_KEY
    echo ""
fi

if [ -z "$WEKNORA_API_KEY" ]; then
    print_error "API key is required"
    exit 1
fi

# Step 3: Generate MCP configuration
print_step "Generating MCP Configuration..."

CONFIG_JSON=$(cat <<EOF
{
  "mcpServers": {
    "weknora": {
      "command": "weknora",
      "args": ["mcp", "serve"],
      "env": {
        "WEKNORA_HOST": "$WEKNORA_HOST",
        "WEKNORA_API_KEY": "$WEKNORA_API_KEY"
      }
    }
  }
}
EOF
)

echo ""
echo "Generated Configuration:"
echo "────────────────────────────────────────"
echo "$CONFIG_JSON" | jq '.' 2>/dev/null || echo "$CONFIG_JSON"
echo "────────────────────────────────────────"

# Step 4: Save configuration
print_step "Saving Configuration..."

MCP_CONFIG_PATH="$CURSOR_DIR/mcp.json"

# Check if mcp.json exists and merge
if [ -f "$MCP_CONFIG_PATH" ]; then
    print_info "Existing mcp.json found. Merging..."
    
    # Use jq to merge configs
    TEMP_CONFIG=$(mktemp)
    echo "$CONFIG_JSON" | jq --argfile existing "$MCP_CONFIG_PATH" '. + {mcpServers: (.mcpServers + $existing.mcpServers)}' > "$TEMP_CONFIG"
    mv "$TEMP_CONFIG" "$MCP_CONFIG_PATH"
else
    # Create new config
    echo "$CONFIG_JSON" | jq '.' > "$MCP_CONFIG_PATH"
fi

print_success "Configuration saved to: $MCP_CONFIG_PATH"

# Step 5: Show next steps
echo ""
echo -e "${MAGENTA}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    Next Steps                               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo "1. Restart Cursor to load the MCP configuration"
echo ""
echo "2. If WeKnora is not running, start it:"
echo "   git clone https://github.com/Tencent/WeKnora.git"
echo "   cd WeKnora"
echo "   cp .env.example .env"
echo "   # Edit .env with your settings"
echo "   docker compose up -d"
echo ""
echo "3. Verify MCP connection in Cursor:"
echo "   - Open Cursor Settings"
echo "   - Go to MCP Servers"
echo "   - Check that 'weknora' shows as connected"
echo ""

# Show config if requested
if [ "$SHOW_CONFIG" = true ]; then
    echo ""
    echo "Full Configuration:"
    cat "$MCP_CONFIG_PATH"
fi

echo ""
print_success "Configuration complete!"
