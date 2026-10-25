---
name: route-discovery
description: Phát hiện routes cho SPA (React, Vue, Next.js) và SSR applications. Tìm dynamic routes, API endpoints, và nested routes. Keywords: discover routes, SPA routes, dynamic routes, API endpoints, next.js routes, react router.
---

# Route Discovery Skill

Phát hiện và document tất cả routes trong một web application (SPA hoặc SSR).

## Khi nào dùng

- Clone SPA (React Router, Vue Router, Next.js)
- Clone SSR app với dynamic routes
- Tìm API endpoints để mock
- Document full site structure
- Clone website có nested routes

---

## SPA Route Discovery

### 1. React Router

```bash
# Check common locations
cat src/App.tsx | grep -E "Routes|Route|Router"
cat src/App.jsx | grep -E "Routes|Route|Router"
cat src/router.tsx | grep -E "Routes|Route|Router"
```

**Common patterns:**
```typescript
// React Router v6+
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/about" element={<About />} />
  <Route path="/blog/:slug" element={<BlogPost />} />
  <Route path="/products/*" element={<Products />} />
</Routes>

// Dynamic routes
<Route path="/users/:id" element={<UserProfile />} />
<Route path="/category/:categoryId/product/:productId" />
```

### 2. Vue Router

```bash
# Check routes file
cat src/router/index.ts | grep -E "routes|path:"
cat src/router.js | grep -E "routes|path:"
```

**Common patterns:**
```typescript
const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About },
  { path: '/blog/:slug', component: BlogPost },
  { path: '/products/*', component: Products }
]
```

### 3. Next.js (App Router)

```bash
# List all page files
find app -name "page.tsx" -o -name "page.jsx"
find app -name "page.ts" -o -name "page.js"

# Show route structure
find app -type d | grep -v node_modules | sort
```

**Route Mapping:**
| File/Folder | Route |
|-------------|-------|
| `app/page.tsx` | `/` |
| `app/about/page.tsx` | `/about` |
| `app/blog/page.tsx` | `/blog` |
| `app/blog/[slug]/page.tsx` | `/blog/:slug` |
| `app/(auth)/login/page.tsx` | `/login` |
| `app/api/users/route.ts` | `/api/users` |

### 4. Next.js (Pages Router)

```bash
# List pages
find pages -name "*.tsx" -o -name "*.ts"
```

**Route Mapping:**
| File | Route |
|------|-------|
| `pages/index.tsx` | `/` |
| `pages/about.tsx` | `/about` |
| `pages/blog/[slug].tsx` | `/blog/:slug` |
| `pages/api/users.ts` | `/api/users` |

### 5. Nuxt.js

```bash
# Auto-generated routes from pages/
ls pages/
find pages -type f
```

**Route Mapping:**
| File | Route |
|------|-------|
| `pages/index.vue` | `/` |
| `pages/about.vue` | `/about` |
| `pages/blog/[slug].vue` | `/blog/:slug` |

---

## API Endpoint Discovery

### REST APIs

```bash
# Common patterns
curl -s https://api.example.com/swagger.json
curl -s https://example.com/api-docs
curl -s https://example.com/openapi.json

# Check Next.js API routes
find pages/api -name "*.ts" -o -name "*.js"
find app/api -name "route.ts" -o -name "route.js"
```

### GraphQL

```bash
# Introspection query
curl -X POST https://example.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name fields { name type { name } } } } }"}'
```

---

## Dynamic Route Patterns

### Common Patterns

| Pattern | Example URL | Matches |
|---------|------------|---------|
| `:id` | `/users/123` | `/users/:id` |
| `:slug` | `/blog/my-post` | `/blog/:slug` |
| `:category` | `/products/electronics` | `/products/:category` |
| `*` | `/docs/a/b/c` | `/docs/*` |
| `(auth)` | `/login` | Route group |

### Pagination Patterns

| Pattern | Example |
|---------|---------|
| Query param | `/blog?page=2` |
| Path param | `/blog/page/2` |
| Codex | `/blog?cursor=abc` |

---

## Route Discovery Methods

### 1. From Source Code (Best)

```bash
# React/Vue - find route definitions
grep -r "path=" src/ --include="*.tsx" --include="*.ts"

# Next.js - list pages directory
find . -path ./node_modules -prune -o \
  -name "page.tsx" -print -o -name "page.js" -print

# Nuxt - list pages
find pages -type f -name "*.vue"
```

### 2. From Network Traffic

```bash
# Open browser DevTools > Network
# Navigate site, capture all XHR/Fetch
# Extract URL patterns
```

### 3. From Sitemap

```bash
# Extract URL patterns from sitemap
curl -s https://example.com/sitemap.xml | \
  grep -oP '(?<=<loc>)[^<]+' | \
  sort -u
```

### 4. From robots.txt

```bash
# Check allowed paths
curl -s https://example.com/robots.txt
```

---

## Output: Route Registry

```markdown
# Route Registry: example.com

## Public Routes

### Pages
| Route | File | Priority |
|-------|------|----------|
| `/` | `pages/index.tsx` | High |
| `/about` | `pages/about.tsx` | Medium |
| `/blog` | `pages/blog/index.tsx` | Medium |
| `/blog/:slug` | `pages/blog/[slug].tsx` | High |
| `/products` | `pages/products/index.tsx` | Medium |
| `/products/:id` | `pages/products/[id].tsx` | High |

### API Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/users` | GET | List users |
| `/api/users/:id` | GET | Get user |
| `/api/auth/login` | POST | Login |

## Dynamic Routes Detected
- `/blog/:slug` - Blog posts
- `/products/:id` - Product detail
- `/users/:id/profile` - User profile
- `/category/:category/products` - Category products
```

---

## Full Clone Checklist

```markdown
## Route Discovery Complete

### Discovered Routes: 45
- Static pages: 12
- Dynamic pages: 28
- API endpoints: 15

### Priority Queue
1. Homepage (`/`) - Start here
2. Core pages (about, contact, pricing)
3. Dynamic routes (blog, products)
4. Sub-routes

### Clone Plan
- [ ] `/` → Clone homepage
- [ ] `/about` → Clone about page
- [ ] `/pricing` → Clone pricing page
- [ ] `/blog` → Clone blog listing
- [ ] `/blog/:slug` → Template for blog posts
- [ ] `/products` → Clone product listing
- [ ] `/products/:id` → Template for product detail
...
```

---

## Tools Summary

| Tool | Best For | Install |
|------|----------|---------|
| `find` + `grep` | Source code routes | Built-in |
| `curl` | API discovery | Built-in |
| Playwright | Runtime routes | `pip install playwright` |
| crawl4ai | Full site crawl | `pip install crawl4ai` |
| sitemap-cli | Sitemap parsing | `npx sitemap-cli` |
