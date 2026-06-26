# Open Design Design System Adapter

## Tổng quan

Adapter này kết nối Cursor Enterprise Framework với Open Design design systems, cho phép sử dụng 150+ brand-grade DESIGN.md files trong workflow.

## Cài đặt

### 1. Cài đặt Open Design CLI

```bash
# Windows
# Tải từ: https://github.com/nexu-io/open-design/releases
# Hoặc winget:
winget install nexu-io.open-design

# Hoặc npm:
npm install -g open-design-cli
```

### 2. Cài đặt MCP Server

```bash
od mcp install cursor
```

### 3. Verify Installation

```bash
od --version
od mcp status
```

## Sử dụng

### Trong Cursor Agent

```bash
# Liệt kê design systems
od design-systems list

# Cài đặt vào project
od design-systems install linear-app --target ./design-systems/

# Tạo DESIGN.md mới từ brand
od design-systems create --name "My Brand" --target ./DESIGN.md
```

### Design System Categories

```
AI & LLM:
├── claude         - Anthropic Claude
├── cohere         - Cohere
├── mistral-ai     - Mistral AI
├── ollama         - Ollama
├── replicate      - Replicate
├── runwayml       - Runway
└── elevenlabs     - ElevenLabs

Developer Tools:
├── cursor         - Cursor IDE
├── vercel         - Vercel
├── linear-app     - Linear
├── framer         - Framer
├── expo           - Expo
├── supabase       - Supabase
├── posthog        - PostHog
├── sentry         - Sentry
├── warp           - Warp Terminal
└── webflow        - Webflow

Productivity:
├── notion         - Notion
├── figma          - Figma
├── miro           - Miro
├── airtable       - Airtable
├── superhuman     - Superhuman
├── intercom       - Intercom
├── zapier         - Zapier
└── raycast        - Raycast

Fintech:
├── stripe         - Stripe
├── coinbase       - Coinbase
├── binance        - Binance
├── kraken         - Kraken
├── mastercard     - Mastercard
├── revolut        - Revolut
└── wise           - Wise

E-commerce:
├── shopify        - Shopify
├── airbnb         - Airbnb
├── uber           - Uber
├── nike           - Nike
├── starbucks      - Starbucks
└── pinterest      - Pinterest

Media:
├── spotify        - Spotify
├── playstation    - PlayStation
├── wired          - Wired
├── theverge       - The Verge
└── meta           - Meta

Automotive:
├── tesla          - Tesla
├── bmw            - BMW
├── ferrari        - Ferrari
├── lamborghini    - Lamborghini
├── bugatti        - Bugatti
└── renault        - Renault

Other:
├── apple          - Apple
├── ibm            - IBM
├── nvidia         - NVIDIA
├── vodafone       - Vodafone
├── resend         - Resend
└── spacex         - SpaceX
```

## Workflow

### Design System Selection

```
1. User yêu cầu UI design
2. Agent phân tích:
   - Target industry/brand
   - Required design tokens
   - Component patterns
3. Agent suggest design system phù hợp
4. User confirm hoặc chọn alternative
5. Agent install design system
6. Agent generate artifact với design tokens
```

### Integration với Frontend Skills

```
frontend-taste + open-design:
├── Design system: linear-app, vercel, stripe
├── Skills: web-prototype, saas-landing, dashboard
└── Output: Brand-compliant HTML prototype

frontend-redesign + open-design:
├── Design system: current brand
├── Skills: refresh pattern
└── Output: Refreshed components
```

## DESIGN.md Schema

```markdown
# [Brand] Design System

## 1. Colors
- Primary: #XXXXXX
- Secondary: #XXXXXX
- Accent: #XXXXXX
- Background: #XXXXXX
- Text: #XXXXXX
- Border: #XXXXXX
- Success: #XXXXXX
- Warning: #XXXXXX
- Error: #XXXXXX

## 2. Typography
- Display Font: [font-name], size, weight
- Body Font: [font-name], size, weight
- Code Font: [font-name], size, weight
- Line Heights
- Letter Spacing

## 3. Spacing
- Base Unit: Xpx
- Scale: 4px base (xs: 4, sm: 8, md: 16, lg: 24, xl: 32, 2xl: 48)

## 4. Layout
- Grid: X columns
- Container: max-width
- Breakpoints: sm/md/lg/xl

## 5. Components
- Button variants
- Input styles
- Card styles
- Navigation
- Modal
- Toast

## 6. Motion
- Duration: Xms
- Easing: cubic-bezier(...)
- Animations: fade, slide, scale, etc.

## 7. Voice & Tone
- Writing style
- Error messages
- Success messages
- Placeholder text

## 8. Brand
- Logo usage
- Imagery style
- Iconography

## 9. Anti-Patterns
- Patterns to avoid
- Common mistakes
- Accessibility issues
```

## Examples

### Linear-style Landing Page

```bash
od design-systems install linear-app --target ./design-systems/
od plugin run saas-landing --brief "landing page với feature grid và pricing table" --design-system linear-app
```

### Stripe-style Dashboard

```bash
od design-systems install stripe --target ./design-systems/
od plugin run dashboard --brief "payment analytics dashboard" --design-system stripe
```

### Apple-style Mobile App

```bash
od design-systems install apple --target ./design-systems/
od plugin run mobile-app --brief "music streaming app với player và playlists" --design-system apple
```

## Troubleshooting

### MCP Server không hoạt động

```bash
# Restart MCP
od mcp uninstall cursor
od mcp install cursor

# Check status
od mcp status
```

### Design system không tìm thấy

```bash
# List tất cả available
od design-systems list

# Search
od design-systems search "linear"
```

### Artifact generation failed

```bash
# Check skill parameters
od skill info web-prototype

# Verify design system
od design-systems verify linear-app
```

## Liên kết

- [Open Design GitHub](https://github.com/nexu-io/open-design)
- [Design Systems Catalog](design-systems/)
- [Skills Protocol](docs/skills-protocol.md)
