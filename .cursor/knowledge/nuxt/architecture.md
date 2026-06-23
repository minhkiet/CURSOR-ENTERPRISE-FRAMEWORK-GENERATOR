---
title: "Nuxt Architecture - Kiến Trúc Nuxt.js"
description: "Phân tích chi tiết kiến trúc Nuxt 3/4 bao gồm Universal Rendering, Nitro Server Engine, Module Ecosystem, và các architectural patterns"
tags: ["nuxt", "vue", "architecture", "ssr", "nitro", "server", "modules"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Nuxt Architecture - Kiến Trúc Nuxt.js

## Overview

Tài liệu này cung cấp phân tích toàn diện về kiến trúc của Nuxt 3 và Nuxt 4, bao gồm các internal systems, rendering strategies, server engine, và cách các components tương tác với nhau. Hiểu rõ kiến trúc này giúp developers đưa ra better architectural decisions và debug issues hiệu quả hơn.

Nuxt là một meta-framework được xây dựng trên Vue.js, cung cấp một opinionated structure cho việc phát triển full-stack Vue applications. Kiến trúc của Nuxt được thiết kế để đơn giản hóa complex tasks như SSR, code splitting, routing, và state management, trong khi vẫn cho phép developers tùy chỉnh khi cần.

## Purpose

Mục đích của tài liệu này bao gồm:

1. **Architectural Understanding** - Hiểu cách Nuxt hoạt động bên trong để debug và optimize
2. **Design Decisions** - Giúp teams đưa ra informed decisions về rendering strategies và deployment
3. **Extension Points** - Identify nơi và cách extend Nuxt's functionality
4. **Performance Optimization** - Hiểu data flow để optimize rendering và caching

## Key Concepts

### Universal Rendering Model

Nuxt hỗ trợ nhiều rendering modes trong cùng một application, mỗi mode phù hợp với different use cases. Việc hiểu cách Nuxt manages different rendering contexts là fundamental cho việc xây dựng optimized applications.

### Nitro Server Engine

Nitro là universal server engine được sử dụng bởi Nuxt. Nó handles tất cả server-side logic bao gồm routing, middleware, API handlers, và deployment target abstraction. Nitro cho phép Nuxt deploy đến bất kỳ environment nào từ serverless functions đến traditional servers.

### Module System

Nuxt modules là extensions cho phép developers customize và extend Nuxt's core functionality. Modules có access đến Nuxt's lifecycle hooks và có thể modify build process, add plugins, configure components, và nhiều hơn nữa.

## Nuxt Directory Structure

### Standard Directory Layout

```
├── .output/                    # Build output (generated)
├── .nuxt/                      # Nuxt engine files (generated)
├── .output/                     # Deployment-ready files
├── app/
│   ├── components/             # Vue components (auto-imported)
│   ├── composables/            # Vue composables (auto-imported)
│   ├── layouts/                # Page layouts
│   ├── middleware/             # Route middleware
│   ├── pages/                  # File-based routing
│   ├── plugins/                # Vue plugins
│   ├── app.vue                 # Root app component
│   └── router.options.ts       # Router customization
├── assets/                     # Uncompiled assets (CSS, images)
├── public/                     # Static files (served as-is)
├── server/
│   ├── api/                    # API routes
│   ├── middleware/             # Server middleware
│   ├── routes/                 # Server routes (non-API)
│   ├── utils/                  # Server utilities
│   └── plugins/                # Server plugins
├── types/                      # TypeScript type definitions
├── nuxt.config.ts              # Nuxt configuration
├── package.json
└── tsconfig.json
```

### Directory Conventions

**Auto-import Directories**: Các directories sau tự động scanned và auto-imported:

- `app/components/` → Components available globally
- `app/composables/` → Composables available globally
- `app/utils/` → Utility functions available globally
- `app/plugins/` → Plugins run on app initialization
- `app/middleware/` → Route middleware
- `server/utils/` → Server-side utilities
- `server/middleware/` → Server middleware

**Special Files**:

- `app/app.vue` → Root component của application
- `app/router.options.ts` → Customize Vue Router
- `app/page.metadata.ts` → Page metadata defaults
- `error.vue` → Global error page

### Nuxt App Directory (Nuxt 3.2+)

Từ Nuxt 3.2+, có thể sử dụng `app/` directory để organize app-specific files:

```
app/
├── components/
├── composables/
├── layouts/
├── pages/
├── plugins/
├── middleware/
├── utils/
├── App.vue
└── router.options.ts
```

Điều này cho phép clearer separation giữa app code và server code.

## Universal Rendering Architecture

### Rendering Modes Overview

Nuxt hỗ trợ 5 rendering modes chính, được configure qua `routeRules` hoặc page metadata:

1. **SSR (Server-Side Rendering)**: Server renders HTML cho mỗi request
2. **SSG (Static Site Generation)**: Pre-rendered at build time
3. **SWR (Stale-While-Revalidate)**: Cached with background revalidation
4. **ISR (Incremental Static Regeneration)**: Hybrid of SSG và dynamic
5. **SPA (Single Page Application)**: Client-side rendering only

### SSR Rendering Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         REQUEST                                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      NUXT SERVER                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Nitro Server Engine                   │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │    │
│  │  │   Router     │  │  Middleware  │  │  Page Load   │  │    │
│  │  │   (Route     │──▶│  (Auth, CORS │──▶│  (useAsync   │  │    │
│  │  │   Matching)  │  │   Rate Limit)│  │   Data)      │  │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │    │
│  │                                                          │    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │              Vue SSR Renderer                     │   │    │
│  │  │  1. Create Vue App Instance                       │   │    │
│  │  │  2. Execute setup() functions                      │   │    │
│  │  │  3. Render to HTML string                         │   │    │
│  │  │  4. Serialize state to payload                    │   │    │
│  │  └──────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        HTML RESPONSE                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  <html>                                                  │    │
│  │    <head>...</head>                                      │    │
│  │    <body>                                                │    │
│  │      <!-- App HTML -->                                   │    │
│  │      <script>window.__NUXT__={...}</script>             │    │
│  │    </body>                                               │    │
│  │  </html>                                                 │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       CLIENT BROWSER                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  1. Download HTML                                         │    │
│  │  2. Download JavaScript bundles                          │    │
│  │  3. Create Vue App (same structure as server)            │    │
│  │  4. Hydrate HTML using window.__NUXT__ payload           │    │
│  │  5. Attach event listeners                                │    │
│  │  6. Vue reactivity active                                │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Hybrid Rendering

Nuxt 3's hybrid rendering cho phép kết hợp different rendering modes trong cùng application:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    // Homepage: Pre-rendered at build time
    '/': { prerender: true },
    
    // Blog posts: Pre-rendered
    '/blog': { prerender: true },
    '/blog/**': { prerender: true },
    
    // Dashboard: Client-side only (SPA)
    '/dashboard/**': { ssr: false },
    
    // Products: ISR with 1 hour revalidation
    '/products/**': { swr: 3600 },
    
    // API: No caching
    '/api/**': { cache: false },
    
    // Admin: SSR with caching
    '/admin/**': { 
      ssr: true,
      cache: { maxAge: 60 * 10 }
    }
  }
})
```

### Nuxt Payload System

Nuxt sử dụng một payload system để transfer data từ server đến client:

```typescript
// Server-side: Data được serialized vào payload
const payload = {
  serverRendered: true,
  data: {
    'user-profile': { id: '1', name: 'John', email: 'john@example.com' }
  },
  state: {
    // Pinia state
  },
  config: {
    // Public runtime config
  }
}

// Client-side: Payload được used để hydrate app
const nuxtApp = useNuxtApp()
nuxtApp.payload.data['user-profile'] // Already available, no refetch
```

## Nitro Server Engine Architecture

### Nitro Overview

Nitro là universal server engine được phát triển bởi UnJS team, powers Nuxt's server-side functionality. Nó provides:

- HTTP server implementation
- Routing system
- Middleware pipeline
- API route handlers
- Cloud provider adapters
- Auto-imports for server utilities

### Nitro Directory Structure

```
server/
├── api/                    # REST API routes
│   ├── users.get.ts       # GET /api/users
│   ├── users.post.ts      # POST /api/users
│   └── users/
│       └── [id].get.ts    # GET /api/users/:id
├── routes/                # Non-API routes
│   └── health.get.ts      # GET /health
├── middleware/           # Server middleware
│   ├── auth.ts           # Authentication
│   └── logger.ts         # Request logging
├── plugins/              # Server plugins
│   └── database.ts      # Database initialization
└── utils/                # Server utilities
    ├── database.ts       # Database client
    └── validators.ts    # Input validation
```

### API Route Handler Pattern

```typescript
// server/api/users/index.get.ts
export default defineEventHandler(async (event) => {
  // Get query parameters
  const query = getQuery(event)
  const { page = 1, limit = 10 } = query
  
  // Get request body (for POST/PUT)
  // const body = await readBody(event)
  
  // Get params
  // const params = getRouterParams(event)
  
  // Get headers
  // const headers = getHeaders(event)
  
  // Response
  const users = await prisma.user.findMany({
    skip: (Number(page) - 1) * Number(limit),
    take: Number(limit)
  })
  
  return {
    users,
    total: users.length,
    page: Number(page)
  }
})
```

### Server Middleware

```typescript
// server/middleware/auth.ts
export default defineEventHandler(async (event) => {
  // Skip auth for public routes
  const publicPaths = ['/api/health', '/api/auth/login']
  if (publicPaths.includes(event.path)) return
  
  // Extract token
  const authHeader = getHeader(event, 'authorization')
  if (!authHeader?.startsWith('Bearer ')) {
    throw createError({
      statusCode: 401,
      message: 'Missing or invalid authorization header'
    })
  }
  
  const token = authHeader.slice(7)
  
  // Verify token
  try {
    const payload = await verifyToken(token)
    event.context.user = payload
  } catch {
    throw createError({
      statusCode: 401,
      message: 'Invalid token'
    })
  }
})
```

### H3 Utilities

Nitro uses H3 (minimal HTTP framework) cung cấp nhiều utilities:

```typescript
import {
  // Request parsing
  getQuery,        // Get query params
  getHeaders,      // Get request headers
  getRouterParams, // Get route params
  getBody,          // Get request body
  getCookie,        // Get cookie value
  getRequestURL,    // Get full request URL
  
  // Response creation
  createError,      // Create error response
  setResponseStatus,
  sendRedirect,
  
  // Utilities
  readBody,         // Read parsed body
  defineEventHandler,
  defineHandler,
  
  // CORS
  setCorsHeaders
} from 'h3'
```

### Server Plugins

```typescript
// server/plugins/database.ts
export default defineNitroPlugin(async (nitroApp) => {
  // Initialize database connection
  const prisma = new PrismaClient()
  
  // Make available globally
  globalThis.prisma = prisma
  
  // Graceful shutdown
  nitroApp.hooks.hook('close', async () => {
    await prisma.$disconnect()
  })
})
```

## Module Ecosystem

### Module Architecture

Nuxt modules là npm packages extend Nuxt's core functionality. Modules have access to:

- Nuxt lifecycle hooks
- Build process customization
- Component registration
- Composable registration
- Plugin registration
- Configuration modification

### Popular Official Modules

| Module | Purpose |
|--------|---------|
| `@nuxt/image` | Image optimization và lazy loading |
| `@nuxtjs/google-fonts` | Google Fonts integration |
| `@nuxt/content` | File-based CMS |
| `@pinia/nuxt` | Pinia state management |
| `@nuxtjs/tailwindcss` | Tailwind CSS integration |
| `@nuxtjs/color-mode` | Dark mode support |
| `@nuxtjs/i18n` | Internationalization |
| `@nuxtjs/auth` | Authentication |
| `@vueuse/nuxt` | VueUse composables |
| `@nuxtjs/sitemap` | Sitemap generation |

### Creating a Module

```typescript
// modules/my-module.ts
import { defineNuxtModule, installModule } from '@nuxtkit/core'

export default defineNuxtModule({
  name: 'my-module',
  configKey: 'myModule',
  
  // Module dependencies
  dependencies: {},
  devDependencies: {},
  
  // Default configuration
  defaults: {
    enabled: true,
    apiKey: ''
  },
  
  // Setup function
  async setup(options, nuxt) {
    // Add module components
    nuxt.hook('components:dirs', (dirs) => {
      dirs.push({
        path: './module-components',
        prefix: 'My'
      })
    })
    
    // Add composables
    nuxt.hook('prepare:types', ({ references }) => {
      references.push({ types: './module-types' })
    })
    
    // Add plugins
    nuxt.hook('app:resolve', (app) => {
      app.plugins.push('./module-plugins/setup.ts')
    })
    
    // Register hooks
    nuxt.hook('page:start', () => {
      console.log('Page rendering started')
    })
  }
})
```

### Module Composition

Modules có thể depend on other modules:

```typescript
export default defineNuxtModule({
  name: 'my-module',
  async setup(options, nuxt) {
    // Install dependencies first
    await installModule('@nuxtjs/google-fonts', {
      families: {
        Inter: [400, 500, 600, 700]
      }
    })
    
    // Then add own functionality
    // ...
  }
})
```

## Component Auto-Import System

### How Auto-Imports Work

Nuxt tự động import tất cả components từ `components/` directory. Component name được derived từ file path:

```
components/
├── Header.vue                    → <Header>
├── Base/Button.vue              → <BaseButton>
├── Base/Input.vue               → <BaseInput>
└── icons/
    └── ArrowRight.vue           → <IconsArrowRight>
```

### Configuration

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  components: [
    {
      path: '~/components',
      pathPrefix: true,          // Include path in name
      prefix: '',                 // Custom prefix
      pattern: '**/*.vue',
      ignore: ['**/README.md'],
      extensions: ['vue']
    },
    {
      path: '~/components/icons',
      prefix: 'Icon'
    }
  ]
})
```

### Component Discovery

```typescript
// Nuxt scans these patterns:
// ~/components/Header.vue → <Header>
// ~/components/Base/Button.vue → <BaseButton>
// ~/components/base/button.vue → <BaseButton> (kebab-case)

// Custom naming:
// ~/components/base/button.vue with prefix 'Ui' → <UiBaseButton>
```

## Composable Auto-Import System

### Built-in Composables

Nuxt auto-imports many built-in Vue và Nuxt composables:

```typescript
// Vue Reactivity
ref, computed, reactive, watch, watchEffect, 
onMounted, onUnmounted, onUpdated, nextTick

// Vue Router
useRoute, useRouter, useRouterPush, useLink

// Nuxt
useNuxtApp, useRuntimeConfig, useState,
useFetch, useAsyncData, useLazyFetch, useLazyAsyncData,
useHead, useSeoMeta, useServerSeoMeta,
useCookie, useStorage, useRequestHeaders
```

### Custom Composables

```typescript
// composables/useCounter.ts
export const useCounter = (initialValue = 0) => {
  const count = ref(initialValue)
  
  const increment = () => count.value++
  const decrement = () => count.value--
  const reset = () => count.value = initialValue
  
  return {
    count: readonly(count),
    increment,
    decrement,
    reset
  }
}
```

```vue
<script setup lang="ts">
// Auto-imported, no need to import
const { count, increment } = useCounter()
</script>
```

## State Management Architecture

### useState - Built-in SSR-Safe State

```typescript
// useState creates reactive state shared across components
// State is serialized and transferred from server to client

// Basic usage
const count = useState('count', () => 0)

// With initializer function (runs on both server and client)
const user = useState('user', () => {
  // On server: returns null
  // On client: returns serialized value from server
  return null
})

// Type-safe
interface User {
  id: string
  name: string
}
const user = useState<User | null>('user', () => null)
```

### Pinia Integration

```typescript
// stores/auth.ts
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isAuthenticated = computed(() => !!user.value)
  
  const login = async (credentials: Credentials) => {
    const response = await $fetch('/api/auth/login', {
      method: 'POST',
      body: credentials
    })
    user.value = response.user
  }
  
  return { user, isAuthenticated, login }
})
```

### State Hydration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ SERVER SIDE                                                      │
│                                                                  │
│ useState('user') → creates ref(null)                            │
│ login() → sets user.value = response.user                       │
│                                                                  │
│ BEFORE RESPONSE:                                                 │
│ state = { user: { id: '1', name: 'John' } }                     │
│                                                                  │
│ Serialize to payload.__NUXT__                                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ CLIENT SIDE                                                      │
│                                                                  │
│ Payload.__NUXT__ contains serialized state                     │
│                                                                  │
│ useState('user') → reads from payload, NOT creating new ref    │
│                                                                  │
│ user.value is already { id: '1', name: 'John' }                 │
│ Hydration complete, no re-fetch needed                          │
└─────────────────────────────────────────────────────────────────┘
```

## Router Architecture

### File-Based Routing

Nuxt tự động tạo routes từ files trong `pages/` directory:

```
pages/
├── index.vue              → /
├── about.vue              → /about
├── blog/
│   ├── index.vue          → /blog
│   └── [slug].vue         → /blog/:slug
└── users/
    └── [id].vue           → /users/:id
```

### Route Metadata

```typescript
// pages/dashboard.vue
definePageMeta({
  // Layout to use
  layout: 'dashboard',
  
  // Middleware to apply
  middleware: ['auth', 'admin'],
  
  // SEO
  title: 'Dashboard',
  
  // Rendering mode override
  ssr: false,
  
  // Query params to watch for re-fetching
  watchQuery: ['page', 'filter']
})
```

### Programmatic Navigation

```typescript
// Navigate to a route
await navigateTo('/about')

// Navigate with options
await navigateTo({
  path: '/users',
  query: { page: 2 }
})

// Navigate back
await navigateTo(request.headers.referer, { redirectCode: 301 })

// Route parameters
const route = useRoute()
const userId = route.params.id // '123'
```

## Plugin System

### Plugin Execution Order

Plugins run in order of filename (alphabetically):

```
plugins/
├── 01.my-plugin.ts        → runs first
├── 02.another-plugin.ts   → runs second
└── auth.ts                → runs third
```

### Client vs Server Plugins

```typescript
// plugins/client-only.ts
// Only runs in browser
export default defineNuxtPlugin(() => {
  console.log('Client only plugin')
})

// plugins/server-only.ts
// Only runs on server
export default defineNuxtPlugin(() => {
  console.log('Server only plugin')
})

// plugins/universal.ts
// Runs on both (default)
export default defineNuxtPlugin(() => {
  console.log('Universal plugin')
})
```

### Plugin Examples

```typescript
// plugins/axios.ts
export default defineNuxtPlugin((nuxtApp) => {
  const axios = $axios.create({
    baseURL: '/api'
  })
  
  // Add interceptors
  axios.interceptors.response.use(
    (response) => response,
    (error) => {
      // Handle errors globally
      if (error.response?.status === 401) {
        navigateTo('/login')
      }
      return Promise.reject(error)
    }
  )
  
  nuxtApp.provide('axios', axios)
})
```

```typescript
// Access in components
const { $axios } = useNuxtApp()
```

## Lifecycle Hooks

### Nuxt App Hooks

```typescript
// Hooks available for plugins và modules
export default defineNuxtPlugin(() => {
  const nuxtApp = useNuxtApp()
  
  // App lifecycle
  nuxtApp.hook('app:created', (app) => {
    // Vue app instance created
  })
  
  nuxtApp.hook('app:mounted', (app) => {
    // Vue app mounted to DOM
  })
  
  nuxtApp.hook('app:error', (error) => {
    // Global error handler
  })
  
  // Page lifecycle
  nuxtApp.hook('page:start', (pageComponent) => {
    // Page rendering started
  })
  
  nuxtApp.hook('page:finish', (pageComponent) => {
    // Page rendering finished
  })
  
  // Link prefetching
  nuxtApp.hook('link:prefetch', (route) => {
    // Link prefetch triggered
  })
})
```

### Build Hooks

```typescript
// modules/my-module.ts
export default defineNuxtModule({
  setup(options, nuxt) {
    // Prepare types
    nuxt.hook('prepare:types', ({ references }) => {
      references.push({ types: 'my-module-types' })
    })
    
    // Build started
    nuxt.hook('build:before', () => {
      // Before build starts
    })
    
    // Components registered
    nuxt.hook('components:dirs', (dirs) => {
      dirs.push({ path: '~/my-components' })
    })
  }
})
```

## Deployment Architecture

### Deployment Targets

Nuxt/Nitro supports multiple deployment targets:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  nitro: {
    preset: 'node-server'
  }
})
```

| Preset | Target |
|--------|--------|
| `node-server` | Node.js server |
| `node-cluster` | Node.js cluster mode |
| `vercel` | Vercel serverless |
| `netlify` | Netlify functions |
| `aws-lambda` | AWS Lambda |
| `cloudflare` | Cloudflare Workers |
| `static` | Static hosting |
| `bun` | Bun runtime |

### Serverless Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CDN / EDGE                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Static Assets (HTML, JS, CSS, Images)                  │    │
│  │  - Served from edge locations                          │    │
│  │  - Aggressive caching                                   │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SERVERLESS FUNCTIONS                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  SSR Requests (page rendering)                          │    │
│  │  - Cold start: ~200-500ms                               │    │
│  │  - Instance reuse for warm requests                    │    │
│  │  - Auto-scaling based on traffic                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  API Endpoints                                           │    │
│  │  - /api/* routes                                        │    │
│  │  - Database connections pooled                         │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DATABASE                                 │
│  - PostgreSQL, MySQL, MongoDB                                  │
│  - Connection pooling                                          │
│  - Read replicas for heavy reads                               │
└─────────────────────────────────────────────────────────────────┘
```

### Self-Hosted Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       LOAD BALANCER                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  nginx / cloud load balancer                            │    │
│  │  - SSL termination                                       │    │
│  │  - Rate limiting                                         │    │
│  │  - Static file serving                                   │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                    │                       │
                    ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NODE SERVERS (CLUSTER)                        │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │  Node Process 1   │  │  Node Process 2   │  │  Node Process 3│ │
│  │  (Master)         │  │  (Worker)         │  │  (Worker)      │ │
│  │  - Load balancing │  │                   │  │                │ │
│  │  - Process mgmt   │  │                   │  │                │ │
│  └──────────────────┘  └──────────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                    │                       │
                    ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REDIS (SESSION CACHE)                         │
│  - Session storage                                              │
│  - Cache layer                                                 │
│  - Rate limiting counters                                      │
└─────────────────────────────────────────────────────────────────┘
```

## Performance Architecture

### Bundle Optimization

Nuxt tự động optimize bundles:

- Tree-shaking unused code
- Code splitting per route
- Component lazy loading
- CSS extraction và minification
- Dynamic import for large libraries

### Caching Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                        BROWSER CACHE                             │
│  - Service Worker (if enabled)                                  │
│  - HTTP cache headers                                           │
│  - Local storage / session storage                              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         CDN CACHE                                │
│  - Static assets cached at edge                                │
│  - Full-page caching (SWR/ISR)                                  │
│  - API response caching (configurable)                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       APPLICATION CACHE                          │
│  - Nuxt payload cache                                           │
│  - useFetch/useAsyncData deduplication                         │
│  - Component-level caching (if implemented)                    │
└─────────────────────────────────────────────────────────────────┘
```

## Troubleshooting

### Common Architecture Issues

#### Issue: State Not Shared Between Pages

**Cause**: Using regular `ref()` instead of `useState()`

**Solution**:
```typescript
// Bad: Creates new state on each page
const count = ref(0)

// Good: State shared across components
const count = useState('count', () => 0)
```

#### Issue: Double Data Fetching

**Cause**: Not using Nuxt's data fetching composables

**Solution**:
```typescript
// Bad: Fetches on both server AND client
onMounted(async () => {
  const data = await fetch('/api/data')
})

// Good: Fetches once, hydrated on client
const { data } = await useFetch('/api/data')
```

#### Issue: Module Not Working

**Diagnosis**: Check module installation và configuration

**Solution**:
```bash
# Verify module is installed
npm ls @nuxt/image

# Check nuxt.config.ts
modules: ['@nuxt/image']
```

## Examples

### Complete Module Example

```typescript
// modules/analytics.ts
import { defineNuxtModule } from '@nuxtkit/core'

export default defineNuxtModule({
  name: 'analytics',
  configKey: 'analytics',
  defaults: {
    trackingId: '',
    enabled: process.env.NODE_ENV === 'production'
  },
  setup(options, nuxt) {
    if (!options.enabled || !options.trackingId) return
    
    // Add plugin
    nuxt.hook('app:created', () => {
      const script = document.createElement('script')
      script.src = `https://www.googletagmanager.com/gtag/js?id=${options.trackingId}`
      script.async = true
      document.head.appendChild(script)
      
      window.dataLayer = window.dataLayer || []
      window.gtag = function gtag() {
        window.dataLayer.push(arguments)
      }
      window.gtag('js', new Date())
      window.gtag('config', options.trackingId)
    })
    
    // Add composable
    nuxt.hook('components:dirs', (dirs) => {
      dirs.push({
        path: './module/composables',
        prefix: 'Analytics'
      })
    })
  }
})
```

### Complete Server Plugin Example

```typescript
// server/plugins/prisma.ts
import { PrismaClient } from '@prisma/client'

declare module 'h3' {
  interface H3EventContext {
    prisma: PrismaClient
  }
}

export default defineNitroPlugin((nitroApp) => {
  const prisma = new PrismaClient({
    log: process.env.NODE_ENV === 'development' 
      ? ['query', 'error', 'warn']
      : ['error']
  })
  
  // Make available to all requests
  nitroApp.hooks.hook('request', (event) => {
    event.context.prisma = prisma
  })
  
  // Cleanup on close
  nitroApp.hooks.hook('close', async () => {
    await prisma.$disconnect()
  })
})
```

## References

### Official Documentation

- [Nuxt 3 Documentation](https://nuxt.com/docs)
- [Nitro Documentation](https://nitro.unjs.io/)
- [H3 Documentation](https://www.jsdocs.io/package/h3)
- [Vue 3 Documentation](https://vuejs.org/)

### Related Rules

- Xem `best-practice.md` để biết cách sử dụng các architectural features
- Xem `anti-pattern.md` để tránh common pitfalls
- Xem `glossary.md` để hiểu các thuật ngữ
- Xem `nestjs.mdc` trong rules để so sánh với NestJS architecture
- Xem `clean-architecture.mdc` để biết general architecture patterns
