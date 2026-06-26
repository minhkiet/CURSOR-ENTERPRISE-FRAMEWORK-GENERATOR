# Open Design Workflow Commands

## /od - Open Design Integration

### Mục đích

Tự động hóa thiết kế UI bằng Open Design (nexu-io/open-design) - open-source design agent.

### Cú pháp

```
/od <subcommand> [options]
/od help
```

---

## Subcommands

### Design Systems

#### `/od list-design-systems`
Liệt kê tất cả design systems có sẵn.

```
Output:
AI & LLM: claude, cohere, mistral-ai, ollama, replicate, runwayml, elevenlabs
Developer Tools: cursor, vercel, linear-app, framer, expo, supabase, posthog, sentry, warp, webflow
Productivity: notion, figma, miro, airtable, superhuman, intercom, zapier, raycast
Fintech: stripe, coinbase, binance, kraken, mastercard, revolut, wise
E-commerce: shopify, airbnb, uber, nike, starbucks, pinterest
Media: spotify, playstation, wired, theverge, meta
Automotive: tesla, bmw, ferrari, lamborghini, bugatti, renault
Other: apple, ibm, nvidia, vodafone, resend, spacex
```

#### `/od install-design-system <name> [--target <path>]`
Cài đặt design system vào project.

```bash
# Ví dụ:
/od install-design-system linear-app
/od install-design-system stripe --target ./design-systems/
```

---

### Skills/Templates

#### `/od list-skills [--scenario <category>]`
Liệt kê skills theo category.

```
Categories: marketing, design, engineering, product, finance, hr

Prototype Skills:
├── web-prototype      - Landing page / hero
├── saas-landing       - SaaS marketing page
├── dashboard          - Admin / analytics
├── mobile-app         - iPhone / Pixel framed app
├── mobile-onboarding  - Onboarding flow
├── social-carousel    - Social media posts
├── email-marketing    - Email template
├── magazine-poster    - Magazine layout
└── motion-frames     - CSS animation

Deck Skills:
├── guizang-ppt       - Magazine-style deck
└── html-ppt-*        - 15 templates × 36 themes

HyperFrames:
└── hyperframes        - HTML → MP4 video
```

#### `/od run <skill> --brief "<description>"`
Chạy một skill với brief.

```bash
# Ví dụ:
/od run web-prototype --brief "landing page cho AI startup với feature highlights"
/od run dashboard --brief "admin panel cho CRM với KPIs và user management"
/od run mobile-app --brief "fitness app với workout plans và progress tracking"
```

---

### Generate

#### `/od generate <type> --brief "<brief>" --design-system <system>`
Generate artifact với design system cụ thể.

```
Types: prototype, deck, hyperframes, image
```

```bash
# Web Prototype
/od generate prototype --brief "SaaS landing page" --design-system linear-app

# Mobile App
/od generate prototype --brief "music streaming app" --design-system apple

# Dashboard
/od generate prototype --brief "analytics dashboard" --design-system stripe

# Deck
/od generate deck --brief "pitch deck cho seed round" --design-system apple

# HyperFrames
/od generate hyperframes --brief "product promo video 30s" --design-system linear-app
```

---

### Artifact

#### `/od artifact <slug>`
Lấy artifact đã generate.

```bash
/od artifact my-landing-page
/od artifact dashboard-v1
```

#### `/od artifact <slug> --save <path>`
Lưu artifact vào file.

```bash
/od artifact my-landing-page --save ./output/index.html
/od artifact dashboard-v1 --save ./output/dashboard.html
```

#### `/od preview <slug>`
Preview artifact trong browser.

```bash
/od preview my-landing-page
```

---

### MCP Server

#### `/od setup-mcp`
Cài đặt MCP server cho Cursor.

```bash
/od setup-mcp
# Output: Open Design MCP installed successfully
```

#### `/od mcp-status`
Kiểm tra trạng thái MCP.

```bash
/od mcp-status
# Output: MCP server: running | stopped
```

#### `/od remove-mcp`
Gỡ cài đặt MCP.

```bash
/od remove-mcp
```

---

## Workflow Examples

### 1. Tạo Landing Page với Linear Design

```
User: Tạo landing page cho startup AI của tôi

Agent:
1. /od list-design-systems
   → Gợi ý: claude, linear-app, cursor (AI tools); stripe (payments)

2. /od install-design-system linear-app
   → Design system installed to ./design-systems/linear-app/

3. /od run saas-landing --brief "AI startup landing page với hero, features, pricing"
   → Artifact generated

4. /od artifact saas-landing --save ./output/index.html
   → Saved to file
```

### 2. Tạo Mobile App Prototype

```
User: Thiết kế mobile app cho ứng dụng fitness

Agent:
1. /od install-design-system figma
   → Design system installed

2. /od run mobile-app --brief "fitness tracking app với workout plans, progress tracking, social features"
   → Artifact generated với iPhone 15 Pro frame

3. /od preview mobile-prototype
   → Opens in browser
```

### 3. Tạo Dashboard

```
User: Tạo admin dashboard cho CRM

Agent:
1. /od install-design-system linear-app
2. /od run dashboard --brief "CRM dashboard với KPIs, user management, analytics charts"
3. /od artifact dashboard-v1 --save ./output/dashboard.html
```

### 4. Tạo Presentation Deck

```
User: Tạo pitch deck cho startup của tôi

Agent:
1. /od list-skills --scenario marketing
   → guizang-ppt, html-ppt-*

2. /od install-design-system apple
3. /od generate deck --brief "seed round pitch deck với problem, solution, market, team"
4. /od artifact pitch-deck --save ./output/deck.html
```

### 5. Tạo HyperFrames Video

```
User: Tạo product promo video ngắn

Agent:
1. /od install-design-system linear-app
2. /od generate hyperframes --brief "30s SaaS product promo với UI reveals và testimonials"
3. /od artifact promo-video --save ./output/promo.mp4
```

---

## Design System Selection Guide

| Use Case | Recommended Design System |
|---|---|
| Developer Tools / SaaS | linear-app, cursor, vercel, framer |
| Fintech / Payments | stripe, coinbase, revolut |
| Productivity / B2B | notion, figma, airtable, intercom |
| E-commerce | airbnb, uber, shopify |
| Consumer App | apple, tesla, nike |
| Media / Content | spotify, theverge, meta |
| Enterprise | ibm, sap, salesforce |

---

## Notes

- Open Design chạy local-first, không cần cloud
- Tất cả output tuân thủ brand design tokens từ DESIGN.md
- Hỗ trợ export sang HTML, PDF, PPTX, MP4
- MCP server cho phép agent đọc design files trực tiếp
- 150+ design systems từ các brand lớn

---

## Liên kết

- [Open Design GitHub](https://github.com/nexu-io/open-design)
- [Design Systems](.cursor/knowledge/design-systems/)
- [Open Design Skill](.cursor/skills/open-design/SKILL.md)
