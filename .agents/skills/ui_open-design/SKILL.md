# Open Design Integration

## Mục tiêu

Tích hợp Open Design (nexu-io/open-design) vào Codex Enterprise Framework để:
- Sử dụng 100+ skills và 150 design systems có sẵn
- Tự động hóa thiết kế UI chuyên nghiệp không thuần AI
- Kết nối với các coding agent qua MCP server
- Hỗ trợ prototype generation, deck, hyperframes, image generation

## Open Design là gì

Open Design là open-source Claude Design alternative với:
- **100+ Skills** - SKILL.md files cho nhiều loại artifact
- **150 Design Systems** - Brand-grade DESIGN.md files (Linear, Stripe, Vercel, etc.)
- **261 Plugins** - Reusable workflows
- **Artifact Types**: Web prototype, mobile app, dashboard, deck, hyperframes, images

## Tích hợp qua MCP Server

### Cài đặt MCP Server

```bash
# Cài đặt Open Design CLI
# Tải từ: https://github.com/nexu-io/open-design/releases

# Cài đặt MCP cho Codex
od mcp install cursor
```

### MCP Tools Available

```
od search-files "<query>"      # Tìm kiếm files
od get-file <path>             # Lấy nội dung file
od get-artifact <slug>         # Lấy artifact đã render
od plugin run <plugin>         # Chạy plugin
od skill list --scenario <s>    # Liệt kê skills
```

## Skill Auto-Discovery Integration

| Keyword / Pattern | Skill | Confidence |
|---|---|---|
| `open-design` | open-design | 0.95 |
| `prototype` | open-design (web-prototype) | 0.90 |
| `landing page` | open-design (saas-landing) | 0.90 |
| `mobile app` | open-design (mobile-app) | 0.90 |
| `dashboard` | open-design (dashboard) | 0.90 |
| `design system` | open-design (design-system) | 0.95 |
| `deck` / `presentation` | open-design (guizang-ppt) | 0.90 |
| `hyperframes` | open-design (hyperframes) | 0.95 |
| `image generation` | open-design (image) | 0.90 |

## Design System Workflow

### Bước 1: Chọn Design System

```bash
# Liệt kê design systems có sẵn
od design-systems list

# Các design systems phổ biến:
# - linear-app    (Developer Tools)
# - stripe        (Fintech)
# - vercel        (Developer Tools)
# - cursor        (Developer Tools)
# - supabase      (Developer Tools)
# - figma         (Productivity)
# - airbnb        (E-commerce)
# - apple         (Other)
# - tesla         (Automotive)
```

### Bước 2: Chọn Skill/Template

```
Prototype Skills:
├── web-prototype      - Landing page / hero
├── saas-landing       - SaaS marketing page
├── dashboard          - Admin / analytics
├── mobile-app         - iPhone / Pixel framed app
├── mobile-onboarding  - Onboarding flow
├── pm-spec           - PM spec document
└── finance-report    - Finance summary

Deck Skills:
├── guizang-ppt       - Magazine-style deck
├── html-ppt-*        - 15 templates x 36 themes

HyperFrames:
└── motion-frames     - HTML → MP4 animation
```

### Bước 3: Generate Artifact

```bash
# Qua CLI
od plugin run web-prototype --brief "landing page for AI startup" --design-system linear-app

# Qua MCP tools (trong Codex agent)
```

## Pre-Review Gate

### O.1 Design Intent Lock
- [ ] Design system selected (Linear, Stripe, Vercel, etc.)
- [ ] Skill/template selected (web-prototype, dashboard, etc.)
- [ ] Artifact type confirmed (prototype, deck, hyperframes)
- [ ] Design direction from DESIGN.md loaded

### O.2 Anti-AI-Slop Check
- [ ] Using brand design tokens (not AI-generated defaults)
- [ ] Following DESIGN.md schema (9 sections)
- [ ] No generic placeholder content
- [ ] Real components from skill templates

### O.3 Design Read Declaration
```
"Reading this as: [artifact type] for [target audience],
 with [design system] design language,
 following [skill] template."
```

## Post-Review Gate

### 6.A Design System Compliance
- [ ] Colors from DESIGN.md palette used
- [ ] Typography from DESIGN.md type scale used
- [ ] Spacing from DESIGN.md spacing system used
- [ ] Components match DESIGN.md patterns

### 6.B Skill Template Compliance
- [ ] Structure follows skill template
- [ ] All required sections present
- [ ] Anti-patterns from skill avoided

### 6.C Technical Quality
- [ ] Valid HTML/CSS output
- [ ] Responsive breakpoints defined
- [ ] No broken links or missing assets
- [ ] Performance optimized (lazy loading, etc.)

## Implementation

### Method 1: MCP Server (Recommended)

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

### Method 2: CLI Commands

```bash
# Chạy trong terminal
od plugin run <skill> --brief "<description>" --design-system <system>
```

### Method 3: Design System Import

```bash
# Import design system vào project
od design-systems install linear-app --target ./design-systems/

# Tạo DESIGN.md mới
od design-systems create --name "My Brand" --target ./DESIGN.md
```

## Design Systems có sẵn

| Category | Systems |
|---|---|
| AI & LLM | claude, cohere, mistral-ai, ollama, replicate, runwayml, elevenlabs |
| Developer Tools | cursor, vercel, linear-app, framer, expo, clickhouse, mongodb, supabase, posthog, sentry, warp, webflow, sanity |
| Productivity | notion, figma, miro, airtable, superhuman, intercom, zapier, cal, clay, raycast |
| Fintech | stripe, coinbase, binance, kraken, mastercard, revolut, wise |
| E-commerce | shopify, airbnb, uber, nike, starbucks, pinterest |
| Media | spotify, playstation, wired, theverge, meta |
| Automotive | tesla, bmw, ferrari, lamborghini, bugatti, renault |
| Other | apple, ibm, nvidia, vodafone, resend, spacex |

## Skill Templates có sẵn

| Skill | Output | Scenario |
|---|---|---|
| web-prototype | HTML prototype | design |
| saas-landing | Marketing page | marketing |
| dashboard | Admin/analytics | operation |
| mobile-app | Mobile prototype | design |
| mobile-onboarding | Onboarding flow | design |
| social-carousel | Social posts | marketing |
| email-marketing | Email template | marketing |
| magazine-poster | Magazine layout | marketing |
| motion-frames | CSS animation | marketing |
| sprite-animation | Pixel animation | marketing |
| pm-spec | PM spec doc | product |
| team-okrs | OKR scorecard | product |
| eng-runbook | Runbook | engineering |
| finance-report | Finance report | finance |
| hr-onboarding | Onboarding plan | hr |
| guizang-ppt | Magazine deck | marketing |
| hyperframes | MP4 video | marketing |

## Notes

- Open Design chạy local-first, không cần cloud
- MCP server cho phép agent đọc design files trực tiếp
- Tất cả output tuân thủ DESIGN.md schema
- Hỗ trợ export sang HTML, PDF, PPTX, MP4

## Liên kết

- [Open Design GitHub](https://github.com/nexu-io/open-design)
- [Skills Protocol](docs/skills-protocol.md)
- [Design Systems](design-systems/)
- [Plugins](plugins/)
