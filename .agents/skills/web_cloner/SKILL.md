---
name: web-cloner
description: 网页复刻提示词生成器。输入一张/多张网页截图或一个网页 URL，反推出一份「确定性复刻 prompt」——用于授权页面、用户自有页面、内部研究或本地视觉回归。触发词：复刻、clone、1:1还原、仿做网页、生成复刻prompt。
---

# Web Clone Prompt · 网页复刻提示词生成器

**一句话**：用户给**截图**或 **URL** → 你**反推**出一份**确定性复刻 prompt** → 先交付 prompt → **询问用户是否继续用这份 prompt 生成网站** → 用户确认后再进入 Codex 构建与视觉回归。

**唯一目标**：在授权/内部研究范围内尽可能精确复刻。不要把任务降级成「风格类似」「视觉参考」或「受启发的重做」。

---

## Phase 0 · Discovery & Questions (BẮT BUỘC)

### 0.1 Initial Questions (Hỏi TRƯỚC KHI bắt đầu clone)

Trước khi bắt đầu clone, **PHẢI HỎI** người dùng các câu hỏi sau để xác định technology stack:

#### Câu hỏi bắt buộc:

```
1. 🌐 NGÔN NGỮ/PLATFORM:
   - Web này sử dụng ngôn ngữ gì? (Vietnamese, English, Chinese, Japanese, Arabic...)
   - Hoặc: Bạn muốn clone sang ngôn ngữ nào?

2. 🖥️ FRONTEND (chọn 1):
   - React + TypeScript (Next.js, Vite, CRA)
   - Vue + TypeScript (Nuxt, Vue CLI)
   - Angular + TypeScript
   - Svelte / SvelteKit
   - Vanilla HTML/CSS/JS
   - PHP + Blade
   - Python + Flask/Django
   - .NET Razor Pages
   - Other: _____________

3. 🗄️ DATABASE (chọn 1+):
   - PostgreSQL
   - MySQL / MariaDB
   - MongoDB
   - SQLite
   - SQL Server
   - Supabase (PostgreSQL + Realtime)
   - Firebase (Firestore + Auth)
   - Prisma ORM
   - Drizzle ORM
   - Không cần database (static site)
   - Other: _____________

4. ⚙️ BACKEND (chọn 1):
   - Node.js + Express/Fastify
   - Next.js API Routes
   - Nuxt Server Routes
   - Python + FastAPI/Django/Flask
   - Go + Gin/Echo
   - Rust + Actix
   - .NET Core / ASP.NET
   - Laravel (PHP)
   - Ruby on Rails
   - Không cần backend (static/SSG)
   - Other: _____________

5. 🔧 AUTHENTICATION:
   - Firebase Auth
   - Supabase Auth
   - Auth0 / Clerk / Lucia
   - NextAuth.js
   - Passport.js
   - JWT (custom)
   - OAuth only
   - Không cần auth

6. 📦 HOSTING (chọn 1):
   - Vercel (recommended for Next.js)
   - Netlify
   - Cloudflare Pages
   - Railway
   - Render
   - AWS (EC2, Lambda, ECS)
   - Azure
   - Self-hosted (Docker, VPS)
   - Other: _____________
```

#### Quick Detect (nếu có URL, tự động detect):

| Signal | Technology |
|--------|------------|
| `_next/static` | Next.js |
| `__nuxt` | Nuxt.js |
| `/api/` + JSON responses | REST API |
| `graphql` endpoint | GraphQL |
| `wp-content` | WordPress |
| `/cdn-cgi/` | Cloudflare |
| `firebaseapp.com` | Firebase |
| `supabase.co` | Supabase |

### 0.2 Technology Detection Checklist

Nếu có URL, phân tích và ghi nhận:

```
┌─────────────────────────────────────────────────────────────┐
│ TECHNOLOGY STACK DETECTED                                 │
├─────────────────────────────────────────────────────────────┤
│ Frontend: _______________                                │
│ CSS Framework: _________ (Tailwind, Bootstrap, custom)   │
│ UI Library: _____________ (shadcn, MUI, Vuetify)         │
│ State Management: ________ (Zustand, Pinia, Redux)        │
│ Backend: _______________                                 │
│ Database: ______________                                 │
│ Auth: _________________                                  │
│ APIs: __________________                                │
│ Hosting: _______________                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1 · Full Site Analysis

### 1.1 HTML Structure Analysis

```markdown
### HTML Analysis

**Document Structure:**
- Semantic tags: <header>, <nav>, <main>, <article>, <section>, <aside>, <footer>
- Meta tags: viewport, description, OG tags, Twitter cards
- Schema.org markup: JSON-LD for SEO
- Accessibility: ARIA labels, alt texts, semantic headings

**Forms (nếu có):**
- Form fields: input types, validation
- Submit handlers
- CSRF tokens

**Key Elements:**
| Element | Selector | Purpose |
|---------|----------|---------|
| Header | `header` | Navigation, logo |
| Hero | `.hero`, `#hero` | Main banner |
| CTA | `.cta-button` | Call to action |
| Footer | `footer` | Links, copyright |
```

### 1.2 CSS Analysis

```markdown
### CSS Analysis

**CSS Methodology:**
- [ ] Tailwind CSS (utility-first)
- [ ] BEM (Block Element Modifier)
- [ ] CSS Modules
- [ ] Styled Components
- [ ] CSS-in-JS
- [ ] Custom CSS

**Color Palette (EXACT hex):**
| Token | Hex | Usage |
|-------|-----|-------|
| primary | #XXXXXX | Main brand color |
| secondary | #XXXXXX | Accents |
| background | #XXXXXX | Page bg |
| text | #XXXXXX | Body text |
| border | #XXXXXX | Borders |

**Spacing System:**
- Base unit: __px
- Scale: 4, 8, 12, 16, 24, 32, 48, 64, 96

**Breakpoints:**
| Breakpoint | Width | Usage |
|------------|-------|-------|
| mobile | < 640px | Phones |
| tablet | 640-1024px | Tablets |
| desktop | > 1024px | Desktop |
| wide | > 1440px | Large screens |

**Animations:**
- Transition timing: ease-in-out, ease
- Duration: 150ms, 300ms, 500ms
- Keyframes: fadeIn, slideUp, scale
```

### 1.3 JavaScript Analysis

```markdown
### JavaScript Analysis

**Core Libraries Detected:**
| Library | Version | Purpose |
|---------|---------|---------|
| React | 18.x | UI framework |
| Vue | 3.x | UI framework |
| Next.js | 14.x | SSR/SSG |
| jQuery | 3.x | DOM manipulation |
| lodash | 4.x | Utilities |
| moment/dayjs | - | Date handling |
| axios/fetch | - | HTTP client |
| chart.js/echarts | - | Charts |
| three.js | - | 3D graphics |

**State Management:**
- [ ] React Context
- [ ] Redux Toolkit
- [ ] Zustand
- [ ] Pinia
- [ ] Vuex
- [ ] Apollo Client (GraphQL)

**Custom Scripts:**
```javascript
// Key functions to replicate
function handleSubmit() { ... }
function validateForm() { ... }
function fetchData() { ... }
```

**Event Handlers:**
| Event | Element | Action |
|-------|---------|--------|
| click | .btn-submit | Form submit |
| change | input | Validation |
| scroll | window | Lazy load |
| resize | window | Responsive |
```

### 1.4 Third-Party Libraries

```markdown
### External Libraries & CDNs

**CSS Libraries:**
| Library | CDN URL | Purpose |
|---------|---------|---------|
| Tailwind | unpkg, cdnjs | Utility CSS |
| Bootstrap | cdnjs | Grid system |
| Font Awesome | cdnjs | Icons |
| Google Fonts | fonts.googleapis | Typography |

**JS Libraries:**
| Library | CDN URL | Version |
|---------|---------|---------|
| React | unpkg, cdnjs | 18.x |
| Vue | cdnjs | 3.x |
| lodash | cdnjs | 4.x |
| axios | cdnjs | 1.x |
| Chart.js | cdnjs | 4.x |

**Icon Libraries:**
- Heroicons
- Lucide React/Vue
- Font Awesome
- Phosphor Icons
- Tabler Icons

**Fonts:**
| Font | Family | Weights |
|------|--------|---------|
| Inter | sans-serif | 400, 500, 600, 700 |
| Roboto | sans-serif | 400, 500, 700 |
```

### 1.5 API Discovery

```markdown
### API Endpoints

**REST Endpoints:**
| Method | Endpoint | Request | Response |
|--------|----------|---------|----------|
| GET | /api/users | - | User[] |
| POST | /api/users | User | User |
| GET | /api/users/:id | - | User |
| PUT | /api/users/:id | User | User |
| DELETE | /api/users/:id | - | - |
| GET | /api/products | ?page, limit | Product[] |
| GET | /api/products/:slug | - | Product |

**GraphQL (nếu có):**
```graphql
type Query {
  users: [User]
  user(id: ID!): User
  products: [Product]
}
```

**WebSocket/SSE:**
| Event | Channel | Payload |
|-------|---------|---------|
| message | /ws | Chat |
| update | /sse | Real-time |

**Authentication:**
| Type | Header | Token |
|------|--------|-------|
| Bearer | Authorization | JWT |
| Cookie | Cookie | Session |
| API Key | X-API-Key | Key |
```

### 1.6 Router Discovery

```markdown
### Route Structure

**Public Routes:**
| Path | Component | Params |
|------|-----------|--------|
| / | Home | - |
| /about | About | - |
| /blog | BlogList | page, limit |
| /blog/:slug | BlogPost | slug |
| /products | ProductList | category, sort |
| /products/:id | ProductDetail | id |
| /contact | Contact | - |
| /search | Search | q |

**Protected Routes:**
| Path | Guard | Redirect |
|------|-------|----------|
| /dashboard | auth | /login |
| /profile | auth | /login |
| /admin | admin | / |

**Dynamic Segments:**
```typescript
/:username       // User profile
/blog/:year/:slug // Blog post
/products/:category/:id // Product
```

**Nested Routes:**
```
/users
  /users           // List
  /users/:id       // Detail
  /users/:id/edit  // Edit
```

---

## Phase 2 · Clone Requirements

### 2.1 Must-Replicate Checklist

```
┌─────────────────────────────────────────────────────────────┐
│ CLONE QUALITY CHECKLIST                                   │
├─────────────────────────────────────────────────────────────┤
│ □ All pages render correctly (200 status)                 │
│ □ Navigation works (all links)                            │
│ □ Forms submit and validate                               │
│ □ API calls return correct data                           │
│ □ Authentication flows work                               │
│ □ Responsive on mobile/tablet/desktop                      │
│ □ Animations smooth (60fps)                               │
│ □ No console errors                                       │
│ □ Images load correctly                                   │
│ □ Fonts render correctly                                  │
│ □ SEO meta tags present                                   │
│ □ Accessibility (keyboard nav, screen reader)              │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Required Files to Generate

```markdown
### Project Structure

```
my-cloned-site/
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── Button/
│   │   ├── Card/
│   │   ├── Navbar/
│   │   └── Footer/
│   ├── pages/            # Route pages (Next.js)
│   │   ├── index.tsx     # Homepage
│   │   ├── about.tsx     # About page
│   │   └── blog/
│   │       ├── index.tsx
│   │       └── [slug].tsx
│   ├── lib/              # Utilities
│   │   ├── api.ts        # API client
│   │   ├── auth.ts       # Auth helpers
│   │   └── utils.ts      # Common functions
│   ├── styles/           # Global styles
│   │   └── globals.css   # Tailwind + custom
│   ├── types/            # TypeScript types
│   │   └── index.ts
│   └── hooks/            # Custom React hooks
│       ├── useAuth.ts
│       └── useFetch.ts
├── public/               # Static assets
│   ├── images/
│   └── fonts/
├── prisma/               # Database (if using)
│   └── schema.prisma
├── tests/                # Test files
│   ├── components/
│   └── e2e/
├── .env.example         # Environment template
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── README.md
```

### Required Dependencies

```json
{
  "dependencies": {
    "react": "^18.x",
    "react-dom": "^18.x",
    "next": "^14.x",
    "typescript": "^5.x",
    "tailwindcss": "^3.x",
    "@tanstack/react-query": "^5.x",
    "axios": "^1.x",
    "zod": "^3.x",
    "lucide-react": "^0.x"
  },
  "devDependencies": {
    "vitest": "^1.x",
    "@testing-library/react": "^14.x",
    "playwright": "^1.x"
  }
}
```
```

---

## Phase 3 · Implementation Prompt Template

### 3.1 Clone Prompt (Output Format)

```markdown
# Clone Prompt: [SITE NAME]

## Technology Stack
- **Frontend:** [React/Vue/Angular/etc] + [TypeScript/JavaScript]
- **Styling:** [Tailwind/Bootstrap/custom CSS]
- **Backend:** [Node.js/Python/.NET/etc] + [Framework]
- **Database:** [PostgreSQL/MongoDB/etc]
- **Auth:** [Firebase/Auth0/custom]

## Pages to Clone

### 1. Homepage (`/`)
**URL:** [original-url]

**Components:**
- [ ] Hero section with [elements]
- [ ] Navigation bar with [items]
- [ ] Feature cards: [count] items
- [ ] CTA section
- [ ] Footer

**Interactions:**
- [ ] Scroll animations
- [ ] Form submission
- [ ] Hover effects

### 2. [Page Name] (`/[path]`)
...

## APIs to Mock

### GET /api/[endpoint]
**Response:**
```json
{
  "data": [],
  "meta": { "total": 0 }
}
```

## Assets to Source

| Asset | Type | Source |
|-------|------|--------|
| Logo | SVG | [source] |
| Hero image | JPG | Unsplash: [search terms] |
| Icons | SVG | Heroicons |

## Verification Checklist

- [ ] All pages render
- [ ] Navigation works
- [ ] Forms validate
- [ ] APIs return data
- [ ] Mobile responsive
- [ ] No console errors
```

---

## Phase 4 · Testing & Verification

### 4.1 Test Cases

```typescript
// tests/pages/homepage.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Homepage', () => {
  test('should load without errors', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveTitle(/Original Title/)
  })

  test('navigation works', async ({ page }) => {
    await page.goto('/')
    await page.click('text=About')
    await expect(page).toHaveURL(/\/about/)
  })

  test('form validates', async ({ page }) => {
    await page.goto('/contact')
    await page.click('button[type=submit]')
    await expect(page.locator('.error')).toBeVisible()
  })
})
```

### 4.2 Performance Checklist

```
□ First Contentful Paint < 1.5s
□ Largest Contentful Paint < 2.5s
□ Time to Interactive < 3.5s
□ Cumulative Layout Shift < 0.1
□ Bundle size < 500KB gzipped
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/inference-guide.md` | Visual analysis method |
| `references/prompt-template.md` | Prompt structure |
| `references/conventions.md` | Coding conventions |
| `references/font-matching.md` | Font identification |
| `references/asset-sourcing.md` | Image sourcing |
| `site-crawler` | Full site discovery |
| `route-discovery` | Route analysis |

---

## Defaults

- **Target Stack:** React 18 + TypeScript + Vite + Tailwind CSS + lucide-react
- **Output:** Complete, runnable project
- **Testing:** Playwright for E2E
