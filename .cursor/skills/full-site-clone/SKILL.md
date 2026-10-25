---
name: full-site-clone
description: Clone toàn bộ website bao gồm tất cả pages, routes, URLs. Kết hợp site-crawler, route-discovery, và web-cloner. Keywords: clone full site, clone all pages, complete site clone, full website clone.
---

# Full Site Clone Workflow

Clone toàn bộ website với tất cả pages, routes, và URLs - đảm bảo clone xong chạy được mượt mà.

## Tổng quan Workflow

```
URL → Technology Questions → Site Crawler → Route Discovery → Tech Stack Analysis → Clone → Test → Ship
```

---

## Phase 0: Technology Discovery (BẮT BUỘC)

### 0.1 Questions cho User

**HỎI NGƯỜI DÙNG TRƯỚC KHI CLONE:**

```
🌐 CLONE QUESTIONS

1. Ngôn ngữ web gốc: _______________
   Hoặc bạn muốn clone sang ngôn ngữ: _______________

2. Frontend stack (chọn 1):
   □ React + TypeScript (Next.js/Vite)
   □ Vue + TypeScript (Nuxt)
   □ Angular + TypeScript
   □ Svelte / SvelteKit
   □ Vanilla HTML/CSS/JS
   □ PHP + Blade (Laravel)
   □ Python + Flask/Django
   □ .NET Razor Pages
   □ Other: _______________

3. Database (chọn 1+):
   □ PostgreSQL
   □ MySQL / MariaDB
   □ MongoDB
   □ SQLite
   □ Supabase (PostgreSQL + Realtime)
   □ Firebase (Firestore)
   □ Prisma ORM
   □ Không cần database
   □ Other: _______________

4. Backend:
   □ Node.js + Express/Fastify
   □ Next.js API Routes
   □ Nuxt Server Routes
   □ Python + FastAPI/Django
   □ Go + Gin
   □ .NET Core
   □ Laravel (PHP)
   □ Không cần backend
   □ Other: _______________

5. Authentication:
   □ Firebase Auth
   □ Supabase Auth
   □ NextAuth.js / Auth.js
   □ Auth0 / Clerk
   □ JWT (custom)
   □ OAuth only
   □ Không cần auth

6. Hosting:
   □ Vercel
   □ Netlify
   □ Cloudflare Pages
   □ Railway
   □ AWS
   □ Self-hosted
```

### 0.2 Auto-Detect (từ URL)

```bash
# Technology detection
curl -I https://example.com  # Check headers
curl -s https://example.com | grep -E "next|nuxt|react" # Check JS framework
curl -s https://example.com/sitemap.xml | head -50 # Check sitemap
```

### 0.3 Technology Stack Report

```markdown
┌─────────────────────────────────────────────────────────┐
│ TECHNOLOGY STACK DETECTED                               │
├─────────────────────────────────────────────────────────┤
│ Frontend: _______________  (React/Vue/Angular/etc)    │
│ CSS: _______________  (Tailwind/Bootstrap/custom)    │
│ UI Library: _______________  (shadcn/MUI/Vuetify)    │
│ State: _______________  (Zustand/Pinia/Redux)       │
│ Backend: _______________                             │
│ Database: _______________                             │
│ Auth: _______________                                 │
│ Hosting: _______________                              │
│ APIs: _______________  (REST/GraphQL/WebSocket)       │
│ Total Pages: _______________                          │
│ Total Routes: _______________                         │
└─────────────────────────────────────────────────────────┘
```

---

## Phase 1: Discovery

### 1.1 Check Sitemap

```bash
# Get sitemap
curl -s https://example.com/sitemap.xml > sitemap.xml

# Parse URLs
grep -oP '(?<=<loc>)[^<]+' sitemap.xml > urls.txt

# Count
wc -l urls.txt
```

### 1.2 Crawl Full Site

```bash
# Using crawl4ai
pip install crawl4ai

crawl4ai https://example.com \
  --extract-links \
  --max-depth 10 \
  --max-pages 500 \
  --output-json site_crawl.json

# Extract all discovered URLs
cat site_crawl.json | jq -r '.[].url' > all_urls.txt
sort -u all_urls.txt > unique_urls.txt
```

### 1.3 Discover Routes (for SPA)

```bash
# Check for route definitions in source
# React Router, Vue Router, Next.js

# Next.js App Router
find app -name "page.tsx" -o -name "page.jsx" 2>/dev/null

# Next.js Pages Router
find pages -name "*.tsx" 2>/dev/null

# React Router
grep -r "path=" src/ --include="*.tsx" 2>/dev/null
```

---

## Phase 2: URL Analysis

### 2.1 Categorize URLs

```bash
# Static pages
grep -E "^https://example.com/($|/about|/contact|/pricing)" urls.txt

# Blog/News
grep -E "/(blog|news|posts|articles)/" urls.txt

# Products
grep -E "/(product|item|catalog)/" urls.txt

# Dynamic routes
grep -vE "^https://example.com/($|about|contact|pricing|blog|products)" urls.txt
```

### 2.2 Generate URL Report

```markdown
# URL Analysis: example.com

## Summary
- Total URLs: 156
- Static pages: 12
- Dynamic pages: 144

## By Type
| Type | Count | Example |
|------|-------|---------|
| Homepage | 1 | `/` |
| Blog Posts | 89 | `/blog/post-slug` |
| Products | 42 | `/products/item-123` |
| Categories | 8 | `/category/electronics` |
| Static | 12 | `/about`, `/pricing` |

## Priority
1. Homepage `/`
2. Core pages: `/about`, `/pricing`, `/contact`
3. Listing pages: `/blog`, `/products`
4. Dynamic: All others
```

---

## Phase 3: Page Templates

### 3.1 Identify Page Templates

```
Dynamic URLs thường share templates:

/blog/post-1      } → Template A: Blog Post
/blog/post-2      }
/products/item-1  } → Template B: Product Detail
/products/item-2  }
```

### 3.2 Template Groups

```markdown
## Page Templates Identified

### Template A: Homepage
- URL: `/`
- Priority: Critical

### Template B: Static Pages
- URLs: `/about`, `/pricing`, `/contact`, `/faq`
- Template: 1 static page clone

### Template C: Blog Listing
- URL: `/blog`
- Priority: High

### Template D: Blog Post
- URLs: `/blog/*` (89 pages)
- Template: 1 dynamic template
- Dynamic part: slug

### Template E: Product Listing
- URL: `/products`
- Priority: High

### Template F: Product Detail
- URLs: `/products/*` (42 pages)
- Template: 1 dynamic template
- Dynamic part: product ID

### Template G: Category
- URLs: `/category/*` (8 pages)
- Template: 1 category template
```

---

## Phase 4: Clone Execution

### 4.1 Clone by Priority

```bash
# Priority 1: Homepage
# → web-cloner skill → generate prompt → clone

# Priority 2: Static Pages (4 pages)
# → Clone each page individually

# Priority 3: Dynamic Templates (3 templates)
# → Clone 1 representative page per template
# → Create reusable component
```

### 4.2 Clone Process

```bash
# For each page/template:
# 1. Get page content (Playwright/crawl4ai)
# 2. Generate clone prompt (web-cloner)
# 3. Execute clone
# 4. Verify output
# 5. Repeat for next
```

### 4.3 Progress Tracking

```markdown
# Full Site Clone Progress

## Completed: 3/156 (2%)
| Page | Status | Notes |
|------|--------|-------|
| `/` | ✅ Done | Homepage cloned |
| `/about` | ✅ Done | Static page |
| `/pricing` | ✅ Done | Static page |

## In Progress: 1
| Page | Status | Notes |
|------|--------|-------|
| `/contact` | 🔄 Cloning | Static page |

## Pending: 152
| Template | Count | Status |
|----------|-------|--------|
| Blog Post | 89 | ⏳ Pending |
| Product Detail | 42 | ⏳ Pending |
| Category | 8 | ⏳ Pending |
```

---

## Phase 5: Verify & Fix

### 5.1 Visual Regression

```bash
# Compare original vs clone
# Use url-regression-protocol from web-cloner

# For each page:
# 1. Take screenshot of original
# 2. Take screenshot of clone
# 3. Compare visually
# 4. Document differences
```

### 5.2 Links Check

```bash
# Verify all internal links work
# Check for broken links in clone

# Check images load
# Check fonts load
# Check scripts work
```

---

## Complete Workflow Example

```bash
#!/bin/bash
# full-clone.sh - Complete site clone workflow

SITE="https://example.com"
OUTPUT="./clone-output"

# 1. Discovery
echo "=== Phase 1: Discovery ==="
curl -s "$SITE/sitemap.xml" > sitemap.xml
grep -oP '(?<=<loc>)[^<]+' sitemap.xml > urls.txt
echo "Found $(wc -l < urls.txt) URLs"

# 2. Categorize
echo "=== Phase 2: Categorize ==="
mkdir -p "$OUTPUT"/{pages,templates,assets}
grep -E "^$SITE/($|#)" urls.txt > "$OUTPUT/static.txt"
grep "/blog/" urls.txt > "$OUTPUT/blog.txt"
grep "/products/" urls.txt > "$OUTPUT/products.txt"
echo "Static: $(wc -l < "$OUTPUT/static.txt")"
echo "Blog: $(wc -l < "$OUTPUT/blog.txt")"
echo "Products: $(wc -l < "$OUTPUT/products.txt")"

# 3. Clone each category
echo "=== Phase 3: Clone ==="
# ... clone commands ...

echo "=== Clone Complete ==="
```

---

## Output Structure

```
clone-output/
├── sitemap.xml
├── urls.txt
├── static.txt
├── blog.txt
├── products.txt
├── pages/
│   ├── homepage/
│   │   ├── index.html
│   │   └── assets/
│   ├── about/
│   │   └── index.html
│   └── pricing/
│       └── index.html
├── templates/
│   ├── blog-post/
│   │   ├── [slug].html
│   │   └── assets/
│   └── product-detail/
│       ├── [id].html
│       └── assets/
└── report.md
```

---

## Quality Checklist

### Pre-Clone Verification
- [ ] Technology stack confirmed with user
- [ ] All URLs discovered from sitemap
- [ ] Route structure documented
- [ ] API endpoints identified
- [ ] Authentication flows mapped

### Post-Clone Verification

#### Core Functionality
- [ ] All pages render without errors
- [ ] Navigation works (all links functional)
- [ ] Forms submit and validate correctly
- [ ] API calls return expected data
- [ ] Authentication flows work (login/logout)
- [ ] User sessions persist correctly

#### Frontend Quality
- [ ] Responsive on mobile (< 640px)
- [ ] Responsive on tablet (640-1024px)
- [ ] Responsive on desktop (> 1024px)
- [ ] Animations smooth (60fps)
- [ ] No layout shifts
- [ ] Fonts render correctly
- [ ] Images load and display properly

#### Technical Quality
- [ ] No console errors (Error level)
- [ ] No 404 resources
- [ ] SEO meta tags present
- [ ] Accessibility: keyboard navigation works
- [ ] Accessibility: screen reader compatible
- [ ] Performance: FCP < 1.5s
- [ ] Performance: LCP < 2.5s
- [ ] Bundle size optimized

#### Security
- [ ] Input validation on all forms
- [ ] XSS protection in place
- [ ] CSRF tokens present (if applicable)
- [ ] Auth tokens stored securely

---

## Phase 6: Testing & Deployment

### 6.1 Playwright E2E Tests

```typescript
// tests/e2e/site.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Site Clone Tests', () => {
  test('homepage loads', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveTitle(/.*/)
    await expect(page.locator('nav')).toBeVisible()
  })

  test('navigation works', async ({ page }) => {
    await page.goto('/')
    await page.click('a[href="/about"]')
    await expect(page).toHaveURL(/\/about/)
  })

  test('forms validate', async ({ page }) => {
    await page.goto('/contact')
    await page.click('button[type="submit"]')
    await expect(page.locator('.error')).toBeVisible()
  })

  test('mobile responsive', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    await expect(page.locator('nav')).toBeHidden() // Mobile menu
  })
})
```

### 6.2 Deploy Checklist

```
□ All tests passing
□ Build succeeds: npm run build
□ No console errors
□ Performance acceptable
□ Mobile responsive
□ Deploy to staging
□ Verify staging works
□ Deploy to production
□ Final verification
```

### 6.3 Bundle Optimization

```json
{
  "build": {
    "analyze": "webpack-bundle-analyzer",
    "targets": {
      "main": "<200KB",
      "vendor": "<300KB",
      "total": "<500KB gzipped"
    }
  }
}
```
