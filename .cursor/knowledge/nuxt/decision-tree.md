---
title: "Nuxt Decision Tree - Cây Quyết Định"
description: "Flowchart và decision tree giúp lựa chọn đúng patterns, architectures, và configurations trong Nuxt development"
tags: ["nuxt", "vue", "decision-tree", "architecture", "patterns"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Nuxt Decision Tree - Cây Quyết Định

## Overview

Tài liệu này cung cấp các decision trees giúp developers đưa ra quyết định đúng đắn khi thiết kế và implement ứng dụng Nuxt. Mỗi decision tree bao gồm các câu hỏi dẫn dắt đến recommendations cụ thể, với giải thích ngắn gọn cho mỗi lựa chọn.

Việc có một structured approach để đưa ra quyết định kiến trúc giúp đảm bảo consistency trong team và reduce decision fatigue. Các decision trees dưới đây được xây dựng dựa trên best practices và real-world experience với Nuxt projects.

## Purpose

Bộ decision trees này phục vụ các mục đích chính sau:

1. **Accelerate Decision Making** - Giảm thời gian để đưa ra quyết định cân nhắc
2. **Reduce Errors** - Tránh common mistakes bằng cách follow proven paths
3. **Standardize Approaches** - Đảm bảo team aligned on architectural choices
4. **Onboard Faster** - Giúp new team members understand decisions

## Decision Trees

### 1. Rendering Strategy Decision Tree

```
BẮT ĐẦU
    │
    ▼
"Content có thay đổi theo thời gian không?"
    │
    ├─[Không]───────────────────→ "Content có cần SEO không?"
    │                                     │
    │                          ├─[Có]────→ SSG (Prerender)
    │                          │           └── blog/, docs/, marketing pages
    │                          │
    │                          └─[Không]──→ SPA (Client-only)
    │                                          └── dashboards, admin panels
    │
    └─[Có]───────────────────→ "Content cá nhân hóa theo user không?"
                                     │
                         ├─[Có]──────→ SSR (Server-render mỗi request)
                         │             └── user-specific feeds, auth pages
                         │
                         └─[Không]──→ "Content thay đổi bao lâu một lần?"
                                         │
                             ├─<1 giờ──→ SWR (Stale-While-Revalidate)
                             │           └── news, product listings
                             │
                             ├─<1 ngày──→ ISR (hourly revalidation)
                             │           └── weather, stock prices
                             │
                             └─>1 ngày──→ SSG với on-demand revalidation
                                             └── changelogs, press releases
```

#### Detailed Recommendations by Rendering Mode

| Mode | Use Case | Configuration |
|------|----------|---------------|
| **SSG** | Blogs, docs, marketing sites | `{ '/': { prerender: true } }` |
| **SSR** | User dashboards, auth flows | `{ ssr: true }` |
| **SWR** | E-commerce listings, news | `{ swr: 3600 }` |
| **SPA** | Admin panels, SPAs | `{ ssr: false }` |

#### Hybrid Rendering Example

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    // Marketing - pre-rendered
    '/': { prerender: true },
    '/about': { prerender: true },
    '/pricing': { prerender: true },
    
    // Blog - pre-rendered with revalidation
    '/blog': { prerender: true },
    '/blog/**': { prerender: true },
    
    // Products - ISR
    '/products': { swr: 3600 },
    '/products/**': { swr: 3600 },
    
    // Dashboard - SSR
    '/dashboard/**': { ssr: true },
    
    // Admin - SPA
    '/admin/**': { ssr: false },
    
    // API - no caching
    '/api/**': { cache: false }
  }
})
```

---

### 2. Data Fetching Decision Tree

```
BẮT ĐẦU
    │
    ▼
"Cần fetch data ở đâu?"
    │
    ├─[Server-side only]──────→ "Cần custom transform không?"
    │                                   │
    │                       ├─[Có]────→ useAsyncData + $fetch
    │                       │           └── useAsyncData('key', () => $fetch('/api/data'))
    │                       │
    │                       └─[Không]──→ useFetch (auto-transforms)
    │                                       └── useFetch('/api/data')
    │
    ├─[Client-side only]────→ "Block page render không?"
    │                                   │
    │                       ├─[Có]────→ useFetch (default: lazy: false)
    │                       │           └── useFetch('/api/data')
    │                       │
    │                       └─[Không]──→ useLazyFetch
    │                                       └── useLazyFetch('/api/recommendations')
    │
    └─[Both (SSR + Hydration)]→ useAsyncData hoặc useFetch
        └── Mặc định của Nuxt, cả server và client đều fetch
```

#### Data Fetching Options Comparison

| Method | SSR | Caching | Blocking | Use Case |
|--------|-----|--------|---------|----------|
| `useFetch` | ✅ | Auto | Yes | Most cases |
| `useLazyFetch` | ✅ | Auto | No | Non-critical data |
| `useAsyncData` | ✅ | Manual key | Yes | Custom transforms |
| `useLazyAsyncData` | ✅ | Manual key | No | Heavy computations |
| `onMounted + fetch` | ❌ | Manual | N/A | Client-only modules |

#### When to Use Each Method

```typescript
// 1. Simple fetch - use useFetch
const { data } = await useFetch('/api/users')

// 2. With transform - use useFetch with transform
const { data: names } = await useFetch('/api/users', {
  transform: (users) => users.map(u => u.name)
})

// 3. Custom key và multiple sources - useAsyncData
const [{ data: users }, { data: posts }] = await Promise.all([
  useAsyncData('users', () => $fetch('/api/users')),
  useAsyncData('posts', () => $fetch('/api/posts'))
])

// 4. Heavy component - useLazyFetch
const { data: recommendations } = await useLazyFetch('/api/recommendations')

// 5. Query-based - useFetch with query
const route = useRoute()
const { data: products } = await useFetch('/api/products', {
  query: { category: route.params.category }
})

// 6. Real-time data - onMounted (after hydration)
const realtimeData = ref(null)
onMounted(() => {
  const ws = new WebSocket('wss://api.example.com')
  ws.onmessage = (event) => {
    realtimeData.value = JSON.parse(event.data)
  }
})
```

---

### 3. State Management Decision Tree

```
BẮT ĐẦU
    │
    ▼
"State cần được share giữa các components không?"
    │
    ├─[Không]──────────────────→ Local state (ref/reactive)
    │                           └── const count = ref(0)
    │
    └─[Có]────────────────────→ "State cần SSR-safe không?"
                                     │
                         ├─[Có]──────→ useState
                         │            └── const user = useState('user', () => null)
                         │
                         └─[Không]──→ "State complex không?"
                                         │
                             ├─[Có]────→ Pinia Store
                             │          └── defineStore('counter', ...)
                             │
                             └─[Không]──→ useState với objects
                                             └── const form = useState('form', () => ({...}))
```

#### State Management Options

| Option | Complexity | SSR-Safe | DevTools | Persistence | Use Case |
|--------|------------|----------|----------|-------------|----------|
| `ref/reactive` | Low | ❌ | Basic | Manual | Local component state |
| `useState` | Low | ✅ | Basic | Manual | Simple shared state |
| `Pinia` | Medium | ✅ | Full | Plugin | Complex state/logic |
| `Vuex` | High | ✅ | Full | Plugin | Legacy projects |

#### useState Best Practices

```typescript
// ✅ Simple primitive values
const count = useState('count', () => 0)
const isOpen = useState('modal-open', () => false)

// ✅ Objects with defaults
const user = useState<User | null>('user', () => null)

// ✅ Arrays
const notifications = useState<Notification[]>('notifications', () => [])

// ❌ Don't use useState for everything
// Complex business logic belongs in Pinia stores
```

#### Pinia Best Practices

```typescript
// stores/cart.ts - Complex state
import { defineStore } from 'pinia'
import type { Product, CartItem } from '~/types'

interface CartState {
  items: CartItem[]
  couponCode: string | null
  isApplyingCoupon: boolean
}

export const useCartStore = defineStore('cart', () => {
  // State
  const items = ref<CartItem[]>([])
  const couponCode = ref<string | null>(null)
  const isApplyingCoupon = ref(false)
  
  // Getters
  const itemCount = computed(() => items.value.length)
  const subtotal = computed(() => 
    items.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
  )
  const discount = computed(() => 
    couponCode.value ? subtotal.value * 0.1 : 0
  )
  const total = computed(() => subtotal.value - discount.value)
  
  // Actions
  const addItem = async (product: Product, quantity = 1) => {
    const existing = items.value.find(i => i.productId === product.id)
    if (existing) {
      existing.quantity += quantity
    } else {
      items.value.push({ productId: product.id, quantity, price: product.price })
    }
  }
  
  const applyCoupon = async (code: string) => {
    isApplyingCoupon.value = true
    try {
      const result = await $fetch('/api/coupons/validate', { body: { code } })
      couponCode.value = code
      return result
    } finally {
      isApplyingCoupon.value = false
    }
  }
  
  return {
    items,
    couponCode,
    itemCount,
    subtotal,
    discount,
    total,
    addItem,
    applyCoupon
  }
})
```

---

### 4. Component Pattern Decision Tree

```
BẮT ĐẦU
    │
    ▼
"Component có cần state không?"
    │
    ├─[Không]──────────────────→ "Là presentational component không?"
    │                                   │
    │                       ├─[Có]────→ Dumb/Presentational Component
    │                       │           └── Props → Render UI
    │                       │           └── IconButton, Card, Badge
    │                       │
    │                       └─[Không]──→ Static Utility Component
    │                                       └── Logo, Divider, Spacer
    │
    └─[Có]────────────────────→ "Component có logic phức tạp không?"
                                     │
                         ├─[Có]──────→ Smart/Container Component
                         │            └── Logic + State + Child components
                         │            └── useAuth(), useCart(), useForm()
                         │
                         └─[Không]──→ "Cần access external services không?"
                                         │
                             ├─[Có]────→ Service-Aware Component
                             │          └── API calls, event handlers
                             │          └── DataTable, SearchBox
                             │
                             └─[Không]──→ Local State Component
                                             └── ref/reactive, computed
                                             └── Toggle, Accordion
```

#### Component Organization Pattern

```
components/
├── ui/                        # Base UI components (dumb)
│   ├── Button.vue
│   ├── Input.vue
│   ├── Card.vue
│   └── Badge.vue
│
├── features/                  # Feature-specific components (smart)
│   ├── auth/
│   │   ├── LoginForm.vue
│   │   └── AuthProvider.vue
│   ├── cart/
│   │   ├── CartButton.vue
│   │   └── CartDrawer.vue
│   └── products/
│       ├── ProductCard.vue
│       └── ProductGrid.vue
│
├── layout/                    # Layout components
│   ├── Header.vue
│   ├── Footer.vue
│   ├── Sidebar.vue
│   └── PageContainer.vue
│
└── icons/                     # Icon components
    ├── ArrowRight.vue
    ├── Check.vue
    └── Loading.vue
```

#### Component Naming Conventions

| Type | Naming | Example | Description |
|------|--------|---------|-------------|
| Base UI | Noun | `Button.vue`, `Card.vue` | Reusable, no business logic |
| Layout | Noun | `Header.vue`, `Sidebar.vue` | Page structure |
| Feature | FeatureNoun | `UserCard.vue`, `ProductGrid.vue` | Feature-specific |
| Page | `index.vue` | `pages/dashboard/index.vue` | Route pages |
| Shared | `Common` prefix | `CommonCard.vue` | Shared across features |

---

### 5. API Design Decision Tree

```
BẰT ĐẦU
    │
    ▼
"API endpoint này dùng để làm gì?"
    │
    ├─[CRUD Resource]──────────→ RESTful API Structure
    │                           └── GET, POST, PUT/PATCH, DELETE
    │
    ├─[Complex Operation]───────→ Action-based Endpoint
    │                           └── POST /api/orders/:id/cancel
    │
    ├─[File Upload]────────────→ Multipart Endpoint
    │                           └── POST /api/uploads với FormData
    │
    ├─[Real-time]───────────────→ WebSocket/SSE
    │                           └── ws:// hoặc /api/events stream
    │
    └─[Aggregation]────────────→ GraphQL hoặc BFF Pattern
                                └── Aggregated data from multiple sources
```

#### RESTful API Structure

```
server/api/
├── users/
│   ├── index.get.ts        # GET    /api/users          - List users
│   ├── index.post.ts       # POST   /api/users          - Create user
│   └── [id].get.ts         # GET    /api/users/:id      - Get user
│   └── [id].put.ts         # PUT    /api/users/:id      - Update user
│   └── [id].delete.ts      # DELETE /api/users/:id      - Delete user
│
├── orders/
│   └── [id]/
│       ├── index.get.ts         # GET    /api/orders/:id
│       ├── cancel.post.ts       # POST   /api/orders/:id/cancel
│       └── refund.post.ts       # POST   /api/orders/:id/refund
│
└── uploads/
    └── index.post.ts       # POST   /api/uploads        - File upload
```

#### API Response Pattern

```typescript
// Success response
export default defineEventHandler(async (event) => {
  const users = await prisma.user.findMany()
  
  return {
    success: true,
    data: users,
    meta: {
      total: users.length,
      page: 1,
      limit: 10
    }
  }
})

// Error response
export default defineEventHandler(async (event) => {
  try {
    return await performAction()
  } catch (error) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Bad Request',
      message: error.message,
      data: { field: 'email', reason: 'already exists' }
    })
  }
})
```

---

### 6. Authentication Decision Tree

```
BẮT ĐẦU
    │
    ▼
"Authentication method nào phù hợp?"
    │
    ├─[Simple, Quick Setup]────→ Cookie-based Session
    │                           └── express-session pattern
    │                           └── Use for: MVPs, simple apps
    │
    ├─[Modern, Stateless]────→ JWT (Access + Refresh)
    │                           └── Access: short-lived, in memory
    │                           └── Refresh: long-lived, in httpOnly cookie
    │                           └── Use for: APIs, mobile apps
    │
    ├─[Enterprise]─────────────→ OAuth 2.0 + OIDC
    │                           └── Social logins
    │                           └── Use for: B2B, multi-tenant apps
    │
    └─[Third-party Provider]───→ Auth Providers
                                └── Auth0, Firebase, Supabase Auth
                                └── Use for: Fast development
```

#### Authentication Implementation Pattern

```typescript
// server/api/auth/login.post.ts
export default defineEventHandler(async (event) => {
  const { email, password } = await readBody(event)
  
  // Validate credentials
  const user = await prisma.user.findUnique({ where: { email } })
  if (!user || !await verifyPassword(password, user.passwordHash)) {
    throw createError({
      statusCode: 401,
      message: 'Invalid credentials'
    })
  }
  
  // Generate tokens
  const accessToken = generateAccessToken(user)
  const refreshToken = generateRefreshToken(user)
  
  // Set refresh token in httpOnly cookie
  setCookie(event, 'refresh_token', refreshToken, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7 // 7 days
  })
  
  return {
    user: sanitizeUser(user),
    accessToken
  }
})

// server/api/auth/refresh.post.ts
export default defineEventHandler(async (event) => {
  const refreshToken = getCookie(event, 'refresh_token')
  
  if (!refreshToken) {
    throw createError({ statusCode: 401, message: 'No refresh token' })
  }
  
  try {
    const payload = verifyRefreshToken(refreshToken)
    const user = await prisma.user.findUnique({ where: { id: payload.userId } })
    
    const newAccessToken = generateAccessToken(user)
    const newRefreshToken = generateRefreshToken(user)
    
    setCookie(event, 'refresh_token', newRefreshToken, {
      httpOnly: true,
      secure: true,
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 7
    })
    
    return { accessToken: newAccessToken }
  } catch {
    throw createError({ statusCode: 401, message: 'Invalid refresh token' })
  }
})
```

---

### 7. Styling Decision Tree

```
BẮT ĐẦU
    │
    ▼
"Team có preference về styling approach không?"
    │
    ├─[Utility-First CSS]──────→ Tailwind CSS
    │                           └── Rapid development
    │                           └── Consistent design system
    │                           └── Small bundle size
    │
    ├─[Component-Based CSS]───→ CSS Modules
    │                           └── Scoped by default
    │                           └── Import specific styles
    │                           └── Good for: existing projects
    │
    ├─[Modern CSS]────────────→ Vanilla CSS + Variables
    │                           └── Native CSS features
    │                           └── CSS custom properties
    │                           └── No build dependencies
    │
    └─[Preprocessor]──────────→ SCSS/SASS
                                └── Variables, mixins, nesting
                                └── Good for: large codebases
```

#### Styling Configuration Examples

```typescript
// nuxt.config.ts - Tailwind
export default defineNuxtConfig({
  modules: ['@nuxtjs/tailwindcss'],
  tailwindcss: {
    configPath: 'tailwind.config.js',
    exposeConfig: true
  }
})

// nuxt.config.ts - SCSS
export default defineNuxtConfig({
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "~/assets/scss/variables.scss" as *;'
        }
      }
    }
  }
})
```

---

### 8. Module Selection Decision Tree

```
BẰT ĐẦU
    │
    ▼
"Cần functionality gì?"
    │
    ├─[Images]──────────────────→ @nuxt/image
    │                           └── Optimization, lazy loading, formats
    │
    ├─[Styling]────────────────→ @nuxtjs/tailwindcss
    │                           └── Utility-first CSS
    │
    ├─[State Management]────────→ @pinia/nuxt
    │                           └── Official Vue 3 state library
    │
    ├─[Content/ CMS]───────────→ @nuxt/content
    │                           └── Markdown-based CMS
    │
    ├─[SEO]────────────────────→ @nuxtjs/sitemap
    │                           └── Automatic sitemap generation
    │
    ├─[Fonts]──────────────────→ @nuxtjs/google-fonts
    │                           └── Optimized font loading
    │
    ├─[i18n]───────────────────→ @nuxtjs/i18n
    │                           └── Internationalization
    │
    ├─[Auth]───────────────────→ @sidebase/nuxt-auth
    │                           └── Authentication
    │
    ├─[Utilities]───────────────→ @vueuse/nuxt
    │                           └── Vue composables collection
    │
    └─[All of above]───────────→ Selectively install needed modules
                                └── Don't over-engineer
```

---

### 9. Deployment Target Decision Tree

```
BẰT ĐẦU
    │
    ▼
"Ứng dụng có cần server-side rendering không?"
    │
    ├─[Không]──────────────────→ Static Hosting
    │                           └── Vercel, Netlify, GitHub Pages
    │                           └── npx nuxi generate
    │
    └─[Có]────────────────────→ "Traffic pattern như thế nào?"
                                     │
                         ├─[Variable/HIGH]──→ Serverless
                         │               └── Vercel, AWS Lambda, Netlify
                         │               └── Auto-scaling, pay-per-use
                         │
                         └─[Predictable]──→ Traditional Server
                                             └── VPS, Docker, Kubernetes
                                             └── Full control, fixed cost
```

#### Deployment Configuration

```typescript
// Vercel (Serverless)
export default defineNuxtConfig({
  nitro: {
    preset: 'vercel'
  }
})

// Netlify (Serverless)
export default defineNuxtConfig({
  nitro: {
    preset: 'netlify'
  }
})

// AWS Lambda
export default defineNuxtConfig({
  nitro: {
    preset: 'aws-lambda'
  }
})

// Docker (Self-hosted)
export default defineNuxtConfig({
  nitro: {
    preset: 'node-server'
  }
})

// Static
export default defineNuxtConfig({
  nitro: {
    preset: 'static'
  }
})
```

---

### 10. Error Handling Decision Tree

```
BẰT ĐẦU
    │
    ▼
"Lỗi xảy ra ở đâu?"
    │
    ├─[API/Server]──────────────→ Server Error Handling
    │                           └── try-catch blocks
    │                           └── createError() for responses
    │
    ├─[Data Fetching]───────────→ Client Error Handling
    │                           └── useFetch error property
    │                           └── Display user-friendly messages
    │
    ├─[Component]───────────────→ Error Boundaries
    │                           └── onErrorCaptured hook
    │                           └── <ErrorBoundary> component
    │
    └─[Unexpected]──────────────→ Global Error Handler
                                 └── app:error hook
                                 └── error.vue page
```

#### Error Handling Patterns

```typescript
// Server - Proper error throwing
export default defineEventHandler(async (event) => {
  try {
    const data = await riskyOperation()
    return data
  } catch (error) {
    if (error instanceof ValidationError) {
      throw createError({
        statusCode: 400,
        message: error.message,
        data: error.details
      })
    }
    
    // Log unexpected errors
    console.error('Unexpected error:', error)
    
    throw createError({
      statusCode: 500,
      message: 'Internal server error'
    })
  }
})

// Client - Data fetching error handling
const { data, error } = await useFetch('/api/data')

watch(error, (err) => {
  if (err) {
    // Show toast notification
    useToast().error(err.message)
  }
})

// Component - Error boundary
onErrorCaptured((err, instance, info) => {
  console.error('Component error:', err, info)
  // Return false to prevent propagation
  return false
})
```

## Quick Reference Tables

### When to Use Each Feature

| Feature | Use When | Don't Use When |
|---------|----------|---------------|
| `useFetch` | Simple data fetching | Need complex transforms |
| `useAsyncData` | Multiple sources, custom keys | Simple fetches |
| `useState` | Simple shared state | Complex state logic |
| `Pinia` | Complex state, business logic | Simple primitive values |
| `SSR` | SEO needed, personalization | Static content only |
| `SSG` | Static content, docs | User-specific content |
| `SPA` | Dashboards, admin | Public pages needing SEO |
| `SWR` | Frequently updating content | Real-time or static data |

### Performance Decisions

| Issue | Solution | When to Apply |
|-------|----------|---------------|
| Slow initial load | Enable SSG/prerender | Public pages |
| Large bundle | Lazy load components | > 500KB JS |
| Images too large | Use NuxtImg | All images |
| API calls slow | Add caching | Read-heavy endpoints |
| Too many requests | Combine with Promise.all | Multiple independent fetches |

## References

### Official Documentation

- [Nuxt Routing](https://nuxt.com/docs/guide/directory-structure/pages)
- [Data Fetching](https://nuxt.com/docs/guide/data-fetching)
- [State Management](https://nuxt.com/docs/guide/state-management)
- [Deployment](https://nuxt.com/docs/guide/deploy)

### Related Documents

- Xem `architecture.md` để hiểu internal workings
- Xem `best-practice.md` để biết implementation details
- Xem `anti-pattern.md` để tránh common mistakes
