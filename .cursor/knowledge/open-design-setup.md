# Open Design Integration - Setup Guide

## Quick Setup

### 1. Install Open Design CLI

**Windows:**
```bash
# Option 1: Winget
winget install nexu-io.open-design

# Option 2: Download from GitHub
# https://github.com/nexu-io/open-design/releases
```

**macOS/Linux:**
```bash
# Option 1: Homebrew
brew install nexu-io/tap/open-design

# Option 2: Download from GitHub
# https://github.com/nexu-io/open-design/releases
```

### 2. Verify Installation

```bash
od --version
# Open Design 0.x.x
```

### 3. Setup MCP Server for Cursor

```bash
od mcp install cursor
```

### 4. Configure Cursor MCP

The installation script should automatically configure Cursor's MCP settings. If not, manually add to your Cursor settings:

```json
// .cursor/mcp.json
{
  "mcpServers": {
    "open-design": {
      "command": "od",
      "args": ["mcp", "server"]
    }
  }
}
```

---

## Files Created

```
.cursor/
├── skills/
│   └── open-design/
│       └── SKILL.md              # Main skill definition
├── knowledge/
│   ├── open-design.json         # Integration config
│   ├── open-design-adapter.md   # Adapter documentation
│   └── design-systems/
│       ├── cursor.md            # Cursor design tokens
│       ├── linear.md           # Linear design tokens
│       ├── vercel.md           # Vercel design tokens
│       ├── stripe.md           # Stripe design tokens
│       └── apple.md            # Apple design tokens
├── commands/
│   └── design/
│       ├── command.md          # /od command documentation
│       └── open-design.md      # Open Design command
└── rules/
    └── skill-integration.mdc   # Updated with open-design entry
```

---

## Usage

### In Cursor Agent

```bash
# List design systems
/od list-design-systems

# Install a design system
/od install-design-system linear-app

# Run a skill
/od run saas-landing --brief "AI startup landing page"

# Generate artifact
/od generate prototype --brief "landing page" --design-system linear-app
```

### Direct CLI

```bash
# Using od CLI directly
od plugin run saas-landing --brief "landing page" --design-system linear-app

# List all skills
od skill list

# Search for design system
od design-systems search "linear"
```

---

## Design Systems Available

| Category | Systems |
|---|---|
| **AI & LLM** | claude, cohere, mistral-ai, ollama, replicate, runwayml, elevenlabs |
| **Developer Tools** | cursor, vercel, linear-app, framer, expo, supabase, posthog, sentry, warp, webflow |
| **Productivity** | notion, figma, miro, airtable, superhuman, intercom, zapier, raycast |
| **Fintech** | stripe, coinbase, binance, kraken, mastercard, revolut, wise |
| **E-commerce** | shopify, airbnb, uber, nike, starbucks, pinterest |
| **Media** | spotify, playstation, wired, theverge, meta |
| **Automotive** | tesla, bmw, ferrari, lamborghini, bugatti, renault |
| **Other** | apple, ibm, nvidia, vodafone, resend, spacex |

---

## Skills Available

| Skill | Output | Scenario |
|---|---|---|
| `web-prototype` | HTML prototype | design |
| `saas-landing` | Marketing page | marketing |
| `dashboard` | Admin/analytics | operation |
| `mobile-app` | Mobile prototype | design |
| `mobile-onboarding` | Onboarding flow | design |
| `social-carousel` | Social posts | marketing |
| `email-marketing` | Email template | marketing |
| `magazine-poster` | Magazine layout | marketing |
| `motion-frames` | CSS animation | marketing |
| `pm-spec` | PM spec doc | product |
| `team-okrs` | OKR scorecard | product |
| `guizang-ppt` | Magazine deck | marketing |
| `hyperframes` | MP4 video | marketing |

---

## Troubleshooting

### MCP Server Not Working

```bash
# Reinstall MCP
od mcp uninstall cursor
od mcp install cursor

# Check status
od mcp status
```

### Design System Not Found

```bash
# List all available
od design-systems list

# Search
od design-systems search "keyword"
```

### Artifact Generation Failed

```bash
# Check skill parameters
od skill info web-prototype

# Verify design system
od design-systems verify linear-app
```

---

## Resources

- [Open Design GitHub](https://github.com/nexu-io/open-design)
- [Design Systems Catalog](https://github.com/nexu-io/open-design/tree/main/design-systems)
- [Skills Documentation](https://github.com/nexu-io/open-design/tree/main/skills)
- [Plugins](https://github.com/nexu-io/open-design/tree/main/plugins)
