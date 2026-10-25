---
name: "source-command-design-open-design"
description: "Migrated source command `design-open-design`"
---

# source-command-design-open-design

Use this skill when the user asks to run the migrated source command `design-open-design`.

## Command Template

# Open Design Command

## Mục đích

Tự động hóa thiết kế UI bằng Open Design (nexu-io/open-design) - open-source design agent với 100+ skills và 150 design systems.

## Cú pháp

```
/od <subcommand> [options]
/od help
```

## Subcommands

### Design Systems

```bash
# Liệt kê design systems có sẵn
/od list-design-systems

# Cài đặt design system vào project
/od install-design-system <name> [--target <path>]

# Ví dụ:
/od install-design-system linear-app
/od install-design-system stripe --target ./design-systems/
```

### Skills/Templates

```bash
# Liệt kê skills theo scenario
/od list-skills [--scenario <marketing|design|engineering|product>]

# Chạy một skill
/od run <skill> --brief "<mô tả>"

# Ví dụ:
/od run web-prototype --brief "landing page cho AI startup"
/od run dashboard --brief "admin panel cho CRM"
```

### Generate

```bash
# Generate artifact với design system
/od generate <type> --brief "<brief>" --design-system <system>

# Types: prototype, deck, hyperframes, image
# Design systems: linear-app, stripe, vercel, cursor, supabase, figma, airbnb, apple, tesla, ...

# Ví dụ:
/od generate prototype --brief "SaaS landing page" --design-system linear-app
/od generate deck --brief "pitch deck cho seed round" --design-system apple
/od generate mobile-app --brief "onboarding flow cho app fitness" --design-system figma
```

### Artifact

```bash
# Lấy artifact đã generate
/od artifact <slug>

# Lưu artifact vào file
/od artifact <slug> --save <path>

# Preview artifact
/od preview <slug>
```

### MCP

```bash
# Cài đặt MCP server cho Codex
/od setup-mcp

# Kiểm tra trạng thái MCP
/od mcp-status

# Gỡ cài đặt MCP
/od remove-mcp
```

## Workflow Tự động

### 1. Chọn Design System

```
Design Systems có sẵn:

AI & LLM: claude, cohere, mistral-ai, ollama, replicate, runwayml, elevenlabs

Developer Tools: cursor, vercel, linear-app, framer, expo, clickhouse, 
                 mongodb, supabase, posthog, sentry, warp, webflow, sanity

Productivity: notion, figma, miro, airtable, superhuman, intercom, zapier, cal

Fintech: stripe, coinbase, binance, kraken, mastercard, revolut, wise

E-commerce: shopify, airbnb, uber, nike, starbucks, pinterest

Media: spotify, playstation, wired, theverge, meta

Automotive: tesla, bmw, ferrari, lamborghini, bugatti, renault

Other: apple, ibm, nvidia, vodafone, resend, spacex
```

### 2. Chọn Skill/Template

```
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

### 3. Tạo Artifact

Agent sẽ:
1. Đọc SKILL.md của skill được chọn
2. Đọc DESIGN.md của design system
3. Generate artifact (HTML prototype)
4. Stream vào sandboxed iframe preview
5. Export thành HTML/PDF/PPTX/MP4

## Ví dụ Usage

### Tạo Landing Page

```
User: Tạo landing page cho startup AI của tôi

Agent:
1. /od list-design-systems (gợi ý: claude, linear-app, cursor)
2. /od install-design-system linear-app
3. /od run saas-landing --brief "AI startup landing page với feature highlights và pricing"
4. Artifact được generate và preview
```

### Tạo Mobile App Prototype

```
User: Thiết kế mobile app cho ứng dụng fitness

Agent:
1. /od install-design-system figma
2. /od run mobile-app --brief "fitness tracking app với workout plans và progress tracking"
3. Artifact được generate với iPhone 15 Pro frame
```

### Tạo Dashboard

```
User: Tạo admin dashboard cho CRM

Agent:
1. /od install-design-system linear-app
2. /od run dashboard --brief "CRM admin dashboard với KPIs, user management và analytics"
3. Artifact được generate với sidebar navigation
```

## Design System Schema (9 sections)

Mỗi DESIGN.md tuân theo schema:

```markdown
# [Brand Name] Design System

## 1. Colors
- Primary: #hex
- Secondary: #hex
- Accent: #hex
- Background: #hex
- Text: #hex

## 2. Typography
- Display: font-family, size, weight
- Body: font-family, size, weight
- Code: font-family, size

## 3. Spacing
- Base unit: Xpx
- Scale: xs, sm, md, lg, xl, 2xl

## 4. Layout
- Grid columns: N
- Container max-width: Xpx
- Breakpoints: sm/md/lg/xl

## 5. Components
- Buttons, Forms, Cards, Navigation, etc.

## 6. Motion
- Duration: Xms
- Easing: cubic-bezier(...)
- Animations: fade, slide, scale, etc.

## 7. Voice & Tone
- Writing style
- Terminology
- Error messages

## 8. Brand
- Logo usage
- Imagery style
- Iconography

## 9. Anti-Patterns
- Patterns to avoid
- Common mistakes
```

## Notes

- Open Design chạy local-first, không cần cloud
- Tất cả output tuân thủ brand design tokens
- Hỗ trợ preview trong sandboxed iframe
- Export được sang HTML, PDF, PPTX, MP4
