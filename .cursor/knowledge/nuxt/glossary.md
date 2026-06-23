---
title: "Nuxt Glossary - Từ Điển Thuật Ngữ Nuxt.js"
description: "Danh sách đầy đủ các thuật ngữ chuyên ngành Nuxt.js với giải thích chi tiết bằng Tiếng Việt"
tags: ["nuxt", "vue", "glossary", "terminology", "dictionary"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Nuxt Glossary - Từ Điển Thuật Ngữ Nuxt.js

## Overview

Tài liệu này cung cấp danh sách toàn diện các thuật ngữ chuyên ngành được sử dụng trong Nuxt.js development. Mỗi thuật ngữ được định nghĩa rõ ràng với ngữ cảnh sử dụng và các ví dụ minh họa khi phù hợp.

Nuxt.js là một framework phức tạp với nhiều khái niệm đặc thù, từ các composables cơ bản đến các tính năng nâng cao của server engine. Việc nắm vững các thuật ngữ này là essential cho việc đọc documentation, tham gia discussions, và debugging issues.

## Purpose

Bộ từ điển này phục vụ các mục đích chính sau:

1. **Learning Reference** - Giúp người mới làm quen với các thuật ngữ
2. **Quick Lookup** - Tra cứu nhanh khi gặp thuật ngữ lạ
3. **Consistent Terminology** - Đảm bảo team sử dụng cùng một cách gọi
4. **Interview Preparation** - Chuẩn bị cho các câu hỏi kỹ thuật

## Glossary

### A

#### App Directory

**Definition**: Directory chính chứa application source code trong Nuxt 3.2+. Chứa `components/`, `composables/`, `layouts/`, `pages/`, `plugins/`, và `middleware/`.

**Usage**: Từ Nuxt 3.2, có thể chọn sử dụng `app/` directory thay vì đặt files trực tiếp ở root.

```
app/
├── components/
├── composables/
├── layouts/
└── pages/
```

#### AsyncData

**Definition**: Xem `useAsyncData`

#### Auto-Import

**Definition**: Tính năng tự động import các composables, components, và utilities. Files trong các directories đặc biệt (`components/`, `composables/`, `utils/`) được tự động imported mà không cần explicit import statements.

**Usage**: Giúp giảm boilerplate code và đảm bảo consistency trong cách import components.

```typescript
// Không cần import vì useState là auto-imported
const count = useState('count', () => 0)

// Component cũng auto-imported
// <MyComponent /> tự động available
```

### B

#### Bundle Analyzer

**Definition**: Công cụ visualize kích thước của các JavaScript bundles. Giúp identify large dependencies và opportunities cho optimization.

**Usage**: Chạy với `npx nuxi analyze` hoặc thêm vào dev dependencies.

#### Built-in Modules

**Definition**: Các modules được phát triển và bảo trì bởi Nuxt team, được include sẵn với Nuxt installation. Bao gồm `@nuxt/image`, `@nuxtjs/google-fonts`, `@nuxt/content`, etc.

### C

#### ClientOnly

**Definition**: Vue component chỉ render trên client-side, không được server-rendered. Hữu ích cho các components sử dụng browser-only APIs.

**Usage**:
```vue
<ClientOnly>
  <BrowserOnlyComponent />
  <template #fallback>
    <LoadingSkeleton />
  </template>
</ClientOnly>
```

#### CSR (Client-Side Rendering)

**Definition**: Rendering xảy ra hoàn toàn ở browser. Server gửi một shell HTML và JavaScript bundle, browser download JS và render content.

**Contrast**: Khác với SSR, nơi server render HTML hoàn chỉnh.

#### Composables

**Definition**: Các hàm sử dụng Vue's Composition API để encapsulate và reuse logic có state. Tương đương với "hooks" trong React.

**Usage**: Đặt trong `composables/` directory để auto-imported.

```typescript
// composables/useCounter.ts
export const useCounter = (initialValue = 0) => {
  const count = ref(initialValue)
  const increment = () => count.value++
  return { count, increment }
}
```

### D

#### definePageMeta

**Definition**: Macro định nghĩa metadata cho một page. Cho phép set layout, middleware, title, và các options khác.

**Usage**:
```vue
<script setup lang="ts">
definePageMeta({
  layout: 'custom',
  middleware: ['auth'],
  title: 'Dashboard'
})
</script>
```

#### defineNuxtPlugin

**Definition**: Macro định nghĩa một Nuxt plugin. Plugins là entry points để extend Vue app.

**Usage**:
```typescript
// plugins/my-plugin.ts
export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.provide('hello', (name: string) => `Hello, ${name}!`)
})
```

#### Dynamic Routing

**Definition**: Routes có dynamic segments, được định nghĩa bằng square brackets trong file names.

**Usage**:
```
pages/
├── users/
│   └── [id].vue      → /users/:id
├── products/
│   └── [category]/
│       └── [id].vue  → /products/:category/:id
└── [...slug].vue     → /* (catch-all)
```

### E

#### Error Page

**Definition**: Trang hiển thị khi có unhandled errors. File `error.vue` ở root của app.

**Usage**: Nhận props `error` với `statusCode` và `message`.

```vue
<!-- error.vue -->
<script setup lang="ts">
defineProps<{ error: NuxtError }>()
</script>
```

#### Event Handler

**Definition**: Hàm xử lý incoming requests trong server routes. Định nghĩa với `defineEventHandler`.

**Usage**:
```typescript
// server/api/hello.get.ts
export default defineEventHandler((event) => {
  return { message: 'Hello!' }
})
```

### F

#### Fallback Slot

**Definition**: Slot content được hiển thị trong khi chờ async component hoặc ClientOnly content hydrate.

**Usage**:
```vue
<ClientOnly>
  <HeavyChart />
  <template #fallback>
    <ChartSkeleton />
  </template>
</ClientOnly>
```

### G

#### getCookie / setCookie

**Definition**: H3 utilities để đọc và ghi cookies trong server-side code.

**Usage**:
```typescript
export default defineEventHandler((event) => {
  const token = getCookie(event, 'auth-token')
  setCookie(event, 'visited', 'true', {
    httpOnly: true,
    maxAge: 60 * 60 * 24 * 7
  })
})
```

### H

#### H3

**Definition**: Minimal HTTP framework được sử dụng bởi Nitro. Cung cấp utilities cho request handling, routing, và middleware.

**Usage**: Import từ `h3` package.

```typescript
import { createError, getQuery, readBody } from 'h3'
```

#### Head Management

**Definition**: Quản lý HTML head tags (title, meta, link, script). Sử dụng `useHead()` hoặc `useSeoMeta()`.

**Usage**:
```vue
<script setup lang="ts">
useHead({
  title: 'My Page',
  meta: [
    { name: 'description', content: 'Page description' }
  ]
})
</script>
```

#### Hydration

**Definition**: Quá trình Vue client-side attach event listeners và reactive systems vào HTML đã được server-rendered. Đảm bảo server-rendered HTML và client-side virtual DOM đồng bộ.

**Usage**: Hydration xảy ra tự động; issues xảy ra khi có mismatches giữa server và client output.

### I

#### ISR (Incremental Static Regeneration)

**Definition**: Hybrid rendering strategy: pre-render pages nhưng revalidate định kỳ. Kết hợp lợi ích của SSG (speed) và dynamic content.

**Usage**: Configure qua route rules.
```typescript
routeRules: {
  '/blog/**': { swr: 3600 } // Revalidate every hour
}
```

#### isLoading

**Definition**: Property trả về từ `useFetch`/`useAsyncData`, cho biết request đang pending hay không.

**Usage**:
```vue
<script setup lang="ts">
const { data, isLoading } = await useFetch('/api/users')
</script>

<template>
  <div v-if="isLoading">Loading...</div>
  <div v-else>{{ data }}</div>
</template>
```

### J

#### JSON Payload

**Definition**: Data được serialized từ server và gửi đến client trong script tag. Chứa `useAsyncData` results và Pinia state để hydrate client-side.

**Usage**: Truy cập qua `useNuxtApp().payload`.

### L

#### Layout

**Definition**: Wrapper components xung quanh page content. Cho phép reuse common UI structures như headers, footers, sidebars.

**Usage**:
```
layouts/
├── default.vue
├── auth.vue
└── dashboard.vue
```

```vue
<!-- layouts/dashboard.vue -->
<template>
  <div class="dashboard">
    <Sidebar />
    <main>
      <slot />
    </main>
  </div>
</template>
```

```vue
<!-- pages/dashboard/index.vue -->
<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })
</script>
```

#### Lazy Fetch

**Definition**: Phiên bản lazy của `useFetch`, không block page rendering. Sử dụng `useLazyFetch` hoặc set `lazy: true` option.

**Usage**:
```typescript
// Không block rendering
const { data } = useLazyFetch('/api/users')

// Hoặc
const { data } = useFetch('/api/users', { lazy: true })
```

### M

#### Meta Tags

**Definition**: HTML tags trong `<head>` cung cấp metadata về page. Quan trọng cho SEO và social sharing.

**Types**: title, description, og:title, og:image, canonical, robots, etc.

**Usage**:
```vue
<script setup lang="ts">
useSeoMeta({
  title: 'Page Title',
  ogTitle: 'Social Title',
  description: 'Page description'
})
</script>
```

#### Middleware

**Definition**: Functions chạy trước khi render page. Có thể redirect, modify context, hoặc throw errors.

**Types**:
- Route Middleware: Chạy trên specific routes
- Server Middleware: Chạy trên server cho all requests

**Usage**:
```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to) => {
  const { isAuthenticated } = useAuth()
  if (!isAuthenticated.value) {
    return navigateTo('/login')
  }
})
```

### N

#### Nitro

**Definition**: Universal server engine powers Nuxt's backend. Handles routing, middleware, API routes, và deployment to multiple platforms.

**Usage**: Server code được execute bởi Nitro; configure qua `nitro` config key.

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  nitro: {
    preset: 'node-server'
  }
})
```

#### Nuxt Module

**Definition**: Extensions cho Nuxt functionality. Được install như npm packages và configure trong `nuxt.config.ts`.

**Usage**:
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@nuxt/image', '@nuxtjs/tailwindcss']
})
```

#### NuxtLink

**Definition**: Component cho client-side navigation. Auto prefetches linked pages và applies active classes.

**Usage**:
```vue
<NuxtLink to="/about" active-class="active">
  About
</NuxtLink>
```

#### NuxtApp

**Definition**: Root Vue app instance được wrap bởi Nuxt. Truy cập qua `useNuxtApp()`.

**Usage**:
```typescript
const nuxtApp = useNuxtApp()
nuxtApp.payload.data     // Server-rendered data
nuxtApp.provide('hello') // Access provided utilities
```

### O

#### onErrorCaptured

**Definition**: Vue lifecycle hook để catch errors từ child components. Dùng để implement error boundaries.

**Usage**:
```vue
<script setup lang="ts">
onErrorCaptured((error) => {
  console.error('Error caught:', error)
  return false // Prevent propagation
})
</script>
```

### P

#### Pages

**Definition**: Directory chứa Vue components được use như pages. File structure tự động tạo routes.

**Usage**:
```
pages/
├── index.vue      → /
├── about.vue      → /about
└── blog/
    └── [slug].vue → /blog/:slug
```

#### Payload

**Definition**: Data được transfer từ server đến client. Chứa `useAsyncData` results và state để hydrate app mà không cần refetch.

**Usage**: Automatically handled by Nuxt; accessible via `useNuxtApp().payload`.

#### Pinia

**Definition**: Official state management library cho Vue 3. Được recommend thay cho Vuex.

**Usage**:
```typescript
// stores/counter.ts
export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const increment = () => count.value++
  return { count, increment }
})
```

#### Prerender

**Definition**: Quá trình generate static HTML files tại build time. Pages được pre-rendered có thể được serve từ CDN mà không cần server.

**Usage**:
```typescript
routeRules: {
  '/': { prerender: true },
  '/blog/**': { prerender: true }
}
```

### Q

#### Query Parameters

**Definition**: Parameters trong URL sau dấu `?`. Truy cập qua `useRoute().query`.

**Usage**:
```typescript
const route = useRoute()
const page = route.query.page // '2'
```

### R

#### Ref

**Definition**: Vue 3 reactive reference. Wrap primitive values để make them reactive.

**Usage**:
```typescript
const count = ref(0)
count.value++ // Access .value in script
// {{ count }} in template auto-unwraps
```

#### Route Rules

**Definition**: Configuration object định nghĩa rendering strategy và caching cho different routes.

**Usage**:
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    '/': { prerender: true },
    '/api/**': { cache: false },
    '/dashboard/**': { ssr: false }
  }
})
```

#### useRoute

**Definition**: Composable để access current route object. Cung cấp access đến params, query, path, và route metadata.

**Usage**:
```typescript
const route = useRoute()
console.log(route.params.id)  // Dynamic segment
console.log(route.query.page) // Query parameter
```

#### useRouter

**Definition**: Composable để access Vue Router instance. Cung cấp navigation methods.

**Usage**:
```typescript
const router = useRouter()
router.push('/about')           // Navigate
router.back()                   // Go back
router.replace('/new-path')     // Replace current
```

### S

#### Script Setup

**Definition**: Vue 3 syntax sugar cho Composition API. `<script setup>` blocks được compile thành setup function của component.

**Usage**:
```vue
<script setup lang="ts">
const count = ref(0)
const increment = () => count.value++
</script>
```

#### SEO

**Definition**: Search Engine Optimization. Practices để improve page visibility trong search results.

**Key Elements**: Meta tags, structured data, sitemaps, semantic HTML, page speed.

#### Server Routes

**Definition**: API endpoints được định nghĩa trong `server/api/` directory. Auto-routed dựa trên file paths.

**Usage**:
```
server/api/
├── users.get.ts      → GET /api/users
├── users.post.ts     → POST /api/users
└── users/
    └── [id].get.ts   → GET /api/users/:id
```

#### SSR (Server-Side Rendering)

**Definition**: Rendering Vue components thành HTML trên server trước khi gửi đến client. Cải thiện initial load performance và SEO.

**Usage**: Default mode in Nuxt; configure qua `ssr` option hoặc `routeRules`.

#### Static Generation

**Definition**: Xem `Prerender`

#### SWR (Stale-While-Revalidate)

**Definition**: Caching strategy: serve cached content immediately while revalidating in background. Kết hợp fast response với fresh data.

**Usage**:
```typescript
routeRules: {
  '/blog': { swr: 3600 } // Cache for 1 hour
}
```

### T

#### TypeScript Support

**Definition**: Nuxt có built-in TypeScript support. Auto-generate types cho composables, pages, và server routes.

**Usage**: Files `.ts`, `.tsx`, và `<script lang="ts">` được type-checked.

### U

#### useAsyncData

**Definition**: Composable fetch và cache data trên cả server và client. Prevents duplicate requests và ensures SSR compatibility.

**Usage**:
```typescript
const { data, pending, error, refresh } = await useAsyncData(
  'key',           // Unique cache key
  () => $fetch('/api/data'),
  {
    transform: (data) => data.items,
    default: () => []
  }
)
```

#### useCookie

**Definition**: Composable create reactive cookie. Value được sync giữa server và client.

**Usage**:
```typescript
const token = useCookie('token', {
  maxAge: 60 * 60 * 24 * 7,
  secure: true
})
token.value = 'new-token'
```

#### useFetch

**Definition**: Wrapper around `useAsyncData` với built-in $fetch. Auto-generates cache key từ URL.

**Usage**:
```typescript
const { data } = await useFetch('/api/users')
```

#### useHead

**Definition**: Composable quản lý HTML head tags. Reactive - updates khi values thay đổi.

**Usage**:
```vue
<script setup lang="ts">
useHead({
  title: () => product.value?.name ?? 'Loading',
  meta: [
    { name: 'description', content: '...' }
  ]
})
</script>
```

#### useLazyFetch / useLazyAsyncData

**Definition**: Lazy versions của useFetch/useAsyncData. Không block page rendering.

**Usage**:
```typescript
const { data } = useLazyFetch('/api/recommendations')
```

#### useNuxtApp

**Definition**: Access Nuxt app instance. Cung cấp access đến payload, hooks, và provided utilities.

**Usage**:
```typescript
const nuxtApp = useNuxtApp()
const { $api } = nuxtApp
```

#### useRuntimeConfig

**Definition**: Access runtime configuration. Public config có thể truy cập từ client; private config server-only.

**Usage**:
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  runtimeConfig: {
    public: { apiBase: '/api' },
    privateKey: process.env.PRIVATE_KEY
  }
})

// In app
const config = useRuntimeConfig()
console.log(config.public.apiBase) // Client-accessible
console.log(config.privateKey)    // Server-only
```

#### useSeoMeta

**Definition**: Simplified API cho common SEO meta tags. Cú pháp declarative dễ đọc hơn `useHead`.

**Usage**:
```vue
<script setup lang="ts">
useSeoMeta({
  title: 'Page Title',
  ogTitle: 'Social Title',
  description: 'Page description'
})
</script>
```

#### useState

**Definition**: Composable tạo reactive state được shared across components và hydrated between server và client.

**Usage**:
```typescript
const count = useState('count', () => 0)
// State is serialized in payload
```

### V

#### Vue 3 Composition API

**Definition**: API style cho building Vue components sử dụng imported functions thay vì options object. Base cho Nuxt's reactivity system.

**Key APIs**: `ref`, `reactive`, `computed`, `watch`, `watchEffect`, `onMounted`, lifecycle hooks.

### W

#### watchQuery

**Definition**: Page metadata option để watch query parameters và refetch data khi chúng thay đổi.

**Usage**:
```vue
<script setup lang="ts">
definePageMeta({
  watchQuery: ['page', 'sort']
})
</script>
```

### X

#### $fetch

**Definition**: Nuxt's enhanced fetch API. Auto-handles JSON parsing, errors, và base URL.

**Usage**:
```typescript
const data = await $fetch('/api/users')
const result = await $fetch('/api/users', {
  method: 'POST',
  body: { name: 'John' }
})
```

#### $nuxt

**Definition**: Global reference đến Nuxt app instance. Legacy; sử dụng `useNuxtApp()` thay thế.

### Y

#### YAML Frontmatter

**Definition**: Metadata format ở đầu Markdown files. Nuxt Content sử dụng frontmatter cho document metadata.

**Usage**:
```yaml
---
title: "My Article"
date: 2024-01-01
tags: ["vue", "nuxt"]
---
```

### Z

#### Zod

**Definition**: TypeScript-first schema validation. Thường được sử dụng với Nuxt cho input validation.

**Usage**:
```typescript
import { z } from 'zod'

const UserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1)
})

const result = UserSchema.safeParse(data)
```

## Common Acronyms

| Acronym | Full Form | Definition |
|---------|-----------|------------|
| CSR | Client-Side Rendering | Rendering in browser |
| SSR | Server-Side Rendering | Rendering on server |
| SSG | Static Site Generation | Pre-rendered at build |
| SWR | Stale-While-Revalidate | Cache strategy |
| ISR | Incremental Static Regeneration | Hybrid static/dynamic |
| SEO | Search Engine Optimization | Search visibility |
| API | Application Programming Interface | Data endpoints |
| URL | Uniform Resource Locator | Web address |

## Common File Extensions

| Extension | Usage | Description |
|-----------|-------|-------------|
| `.vue` | Components, pages, layouts | Vue SFC files |
| `.ts` | Scripts, utilities | TypeScript files |
| `.md` | Documentation | Markdown files |
| `.mdc` | Content files | Markdown with components |
| `.config.ts` | Configuration | Nuxt config files |

## References

### Official Documentation

- [Nuxt 3 Glossary](https://nuxt.com/docs/guide/concepts/nuxtjs#explanation)
- [Vue 3 Glossary](https://vuejs.org/glossary/)
- [Nitro Glossary](https://nitro.unjs.io/)

### Related Documents

- Xem `architecture.md` để hiểu cách các components tương tác
- Xem `best-practice.md` để biết cách sử dụng đúng các features
- Xem `anti-pattern.md` để tránh common mistakes
