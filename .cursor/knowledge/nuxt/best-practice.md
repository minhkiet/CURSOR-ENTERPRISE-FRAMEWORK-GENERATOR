---
title: "Nuxt Best Practices - Thực Hành Tốt Nhất"
description: "Hướng dẫn toàn diện về các best practices trong Nuxt.js development cho production-ready applications"
tags: ["nuxt", "vue", "ssr", "performance", "seo", "pinia", "typescript"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Nuxt Best Practices - Thực Hành Tốt Nhất

## Overview

Tài liệu này tổng hợp các best practices thiết yếu cho việc phát triển ứng dụng Nuxt.js production-ready. Được xây dựng dựa trên kinh nghiệm thực tế và official documentation, các practices được tổ chức theo từng domain cụ thể giúp developers dễ dàng reference và implement trong dự án của mình.

Nuxt.js là một framework mạnh mẽ cung cấp nhiều features out-of-the-box như file-based routing, auto-imports, server-side rendering, và built-in optimization tools. Tuy nhiên, để tận dụng tối đa những lợi ích này và tránh các common pitfalls, cần nắm vững các best practices được document trong tài liệu này.

## Purpose

Mục đích chính của tài liệu này là:

1. **Standardize team practices** - Thiết lập conventions thống nhất cho toàn team
2. **Prevent common mistakes** - Giảm thiểu bugs và issues phổ biến từ đầu
3. **Optimize performance** - Đạt được tốc độ load và runtime performance tốt nhất
4. **Improve SEO** - Đảm bảo các pages được search engines index đúng cách
5. **Enhance maintainability** - Giúp codebase dễ đọc, debug và extend trong tương lai

## Key Concepts

### Rendering Strategies

Nuxt 3 hỗ trợ nhiều rendering modes khác nhau, mỗi mode phù hợp với từng use case cụ thể. Việc chọn đúng rendering strategy là quyết định kiến trúc quan trọng đầu tiên cần thực hiện.

**SSR (Server-Side Rendering)**: Server render HTML cho mỗi request. Phù hợp với content động, personalized pages, và SEO-critical pages. Time to First Byte (TTFB) nhanh, nhưng cần server resources.

**SSG (Static Site Generation)**: Pre-render tất cả pages tại build time. Phù hợp với content không thay đổi thường xuyên như documentation, blogs, marketing sites. Performance tốt nhất vì không cần server processing.

**SWR (Stale-While-Revalidate)**: Serve cached content ngay lập tức trong khi revalidate ở background. Phù hợp với content thay đổi periodcally như dashboards, news feeds.

**SPA (Single Page Application)**: Client-side rendering hoàn toàn. Phù hợp với authenticated dashboards, admin panels, hoặc apps cần heavy client-side interactions.

**Hybrid Rendering**: Kết hợp nhiều rendering modes trong cùng một app thông qua route rules. Mỗi route có thể có rendering strategy riêng.

### File-Based Routing

Nuxt tự động tạo routes dựa trên file structure trong `pages/` directory. Điều này giúp đơn giản hóa routing configuration nhưng đòi hỏi tuân thủ certain conventions để tránh conflicts và unexpected behaviors.

### Auto-Imports System

Một trong những features mạnh mẽ nhất của Nuxt là auto-imports. Composables, components, utils từ các directories đặc biệt sẽ tự động available mà không cần explicit imports. Tuy nhiên, điều này đòi hỏi understanding về cách system hoạt động để tránh naming collisions và performance issues.

## Best Practices

### 1. File-Based Routing Best Practices

#### Sử dụng TypeScript Interface cho Route Params

```typescript
// types/route.ts
export interface ProductRouteParams {
  category: string
  id: string
}

export interface UserRouteParams {
  username: string
}
```

```vue
<!-- pages/products/[category]/[id].vue -->
<script setup lang="ts">
import type { ProductRouteParams } from '~/types/route'

const route = useRoute()
const params = route.params as ProductRouteParams

// Type-safe access to route params
const { category, id } = route.params as ProductRouteParams
</script>
```

#### Tổ Chức Pages Directory

```
pages/
├── index.vue                    # Homepage (/)
├── about.vue                    # About page (/about)
├── blog/
│   ├── index.vue               # Blog listing (/blog)
│   ├── [slug].vue              # Blog post (/blog/my-post)
│   └── category/
│       └── [category].vue      # Category filter (/blog/category/tech)
├── products/
│   ├── index.vue               # Products listing (/products)
│   ├── [id].vue                # Product detail (/products/123)
│   └── [id]/
│       └── review.vue          # Nested route (/products/123/review)
├── auth/
│   ├── login.vue               # Login page
│   ├── register.vue            # Register page
│   └── forgot-password.vue     # Password recovery
└── (app)/
    ├── dashboard.vue           # Layout group
    ├── settings.vue            # /settings
    └── profile.vue             # /profile
```

#### Sử dụng Route Groups cho Layouts

```vue
<!-- pages/(marketing)/index.vue -->
<!-- Sử dụng layouts/marketing.vue -->
<template>
  <div>
    <MarketingHeader />
    <slot />
    <MarketingFooter />
  </div>
</template>
```

```vue
<!-- pages/(app)/dashboard.vue -->
<!-- Sử dụng layouts/default.vue hoặc layouts/app.vue -->
<template>
  <div>
    <AppSidebar />
    <main>
      <slot />
    </main>
    <AppHeader />
  </div>
</template>
```

### 2. Data Fetching Best Practices

#### Luôn Sử Dụng useFetch/useAsyncData

```typescript
// Bad: fetch trong onMounted
<script setup lang="ts">
const data = ref(null)

onMounted(async () => {
  const response = await fetch('/api/users')
  data.value = await response.json()
})
</script>

// Good: Sử dụng useFetch
<script setup lang="ts">
const { data: users, pending, error } = await useFetch('/api/users', {
  // Auto-generated cache key
  // SSR-aware
  // Deduplication built-in
})
</script>
```

#### Caching Strategy

```typescript
// Static content - prerender và cache vĩnh viễn
const { data: docs } = await useFetch('/api/docs', {
  key: 'documentation',
  getCachedData(key, nuxtApp) {
    return nuxtApp.payload.data[key] || nuxtApp.static.data[key]
  }
})

// Dynamic content - SWR với revalidation
const { data: products } = await useFetch('/api/products', {
  key: 'products',
  watch: [categoryFilter],
  // Cache for 1 hour, revalidate in background
  lazy: true
})

// User-specific content - No caching
const { data: userProfile } = await useFetch('/api/user/profile', {
  key: 'user-profile',
  credentials: 'include',
  headers: useRequestHeaders(['cookie'])
})
```

#### Parallel Data Fetching

```typescript
// Bad: Sequential fetches
<script setup lang="ts">
const { data: user } = await useFetch('/api/user')
const { data: posts } = await useFetch('/api/posts')
const { data: notifications } = await useFetch('/api/notifications')
</script>

// Good: Parallel fetches với Promise.all
<script setup lang="ts">
const [{ data: user }, { data: posts }, { data: notifications }] = await Promise.all([
  useFetch('/api/user', { key: 'user' }),
  useFetch('/api/posts', { key: 'posts' }),
  useFetch('/api/notifications', { key: 'notifications' })
])
</script>

// Better: Sử dụng useLazy for non-critical data
<script setup lang="ts">
// These don't block page render
const { data: recommendations } = useLazyFetch('/api/recommendations')
const { data: trending } = useLazyFetch('/api/trending')
</script>
```

### 3. Auto-Imports Best Practices

#### Tổ Chức Composables có Hệ Thống

```
composables/
├── useAuth.ts                  # Authentication logic
├── useUser.ts                  # User-related state
├── useCart.ts                  # Shopping cart
├── useWishlist.ts              # Wishlist functionality
├── useNotifications.ts         # Notification system
└── utils/
    ├── useFormatters.ts        # Date, currency formatters
    └── useValidators.ts        # Form validation helpers
```

#### Type-Safe Composable Pattern

```typescript
// composables/useCounter.ts
interface CounterOptions {
  min?: number
  max?: number
  step?: number
}

interface CounterReturn {
  count: Ref<number>
  increment: () => void
  decrement: () => void
  reset: () => void
}

export const useCounter = (options: CounterOptions = {}): CounterReturn => {
  const { min = -Infinity, max = Infinity, step = 1 } = options
  
  const count = ref(0)
  
  const increment = () => {
    if (count.value + step <= max) {
      count.value += step
    }
  }
  
  const decrement = () => {
    if (count.value - step >= min) {
      count.value -= step
    }
  }
  
  const reset = () => {
    count.value = 0
  }
  
  return {
    count: readonly(count),
    increment,
    decrement,
    reset
  }
}
```

#### Avoid Naming Collisions

```typescript
// Bad: Generic names có thể conflict
// composables/useData.ts
export const useData = () => { ... } // Too generic!

// Good: Specific, descriptive names
// composables/useProductList.ts
export const useProductList = () => { ... }

// Good: Prefix với feature name
// composables/useAuthToken.ts
export const useAuthToken = () => { ... }
```

### 4. Server Routes Best Practices

#### RESTful API Structure

```
server/
├── api/
│   ├── users/
│   │   ├── index.get.ts        # GET /api/users - List users
│   │   ├── index.post.ts       # POST /api/users - Create user
│   │   └── [id].get.ts         # GET /api/users/:id
│   ├── products/
│   │   ├── index.get.ts        # GET /api/products
│   │   ├── index.post.ts       # POST /api/products
│   │   ├── [id].get.ts         # GET /api/products/:id
│   │   ├── [id].put.ts         # PUT /api/products/:id
│   │   └── [id].delete.ts      # DELETE /api/products/:id
│   └── orders/
│       └── [orderId]/
│           ├── index.get.ts     # GET /api/orders/:orderId
│           └── cancel.post.ts  # POST /api/orders/:orderId/cancel
├── middleware/
│   ├── auth.ts                 # Authentication middleware
│   └── rateLimit.ts            # Rate limiting
└── utils/
    ├── database.ts             # Database client
    └── validators.ts           # Input validation
```

#### Type-Safe Request/Response

```typescript
// server/api/users/index.post.ts
import { z } from 'zod'

const UserCreateSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  password: z.string().min(8),
  role: z.enum(['user', 'admin']).default('user')
})

type UserCreateInput = z.infer<typeof UserCreateSchema>
type UserCreateOutput = Promise<{ user: User; token: string }>

export default defineEventHandler(async (event): UserCreateOutput => {
  // Validate body
  const body = await readBody(event)
  const result = UserCreateSchema.safeParse(body)
  
  if (!result.success) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Validation Error',
      data: result.error.flatten()
    })
  }
  
  const { email, name, password, role } = result.data
  
  // Check for existing user
  const existingUser = await prisma.user.findUnique({
    where: { email }
  })
  
  if (existingUser) {
    throw createError({
      statusCode: 409,
      statusMessage: 'Conflict',
      message: 'User with this email already exists'
    })
  }
  
  // Hash password
  const hashedPassword = await hashPassword(password)
  
  // Create user
  const user = await prisma.user.create({
    data: {
      email,
      name,
      password: hashedPassword,
      role
    }
  })
  
  // Generate token
  const token = generateToken(user)
  
  return {
    user: sanitizeUser(user),
    token
  }
})

// Utility to sanitize user object (remove password)
const sanitizeUser = (user: User) => {
  const { password, ...safeUser } = user
  return safeUser
}
```

#### Error Handling

```typescript
// server/utils/errors.ts
export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public code?: string,
    public data?: unknown
  ) {
    super(message)
    this.name = 'AppError'
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, identifier?: string | number) {
    super(
      `${resource} not found${identifier ? `: ${identifier}` : ''}`,
      404,
      'NOT_FOUND'
    )
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Authentication required') {
    super(message, 401, 'UNAUTHORIZED')
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Access denied') {
    super(message, 403, 'FORBIDDEN')
  }
}
```

```typescript
// server/middleware/errorHandler.ts
export default defineEventHandler(async (event) => {
  try {
    return await handle(event)
  } catch (error) {
    if (error instanceof AppError) {
      throw createError({
        statusCode: error.statusCode,
        statusMessage: error.statusMessage || error.message,
        message: error.message,
        data: error.data
      })
    }
    
    // Log unexpected errors
    console.error('Unhandled error:', error)
    
    throw createError({
      statusCode: 500,
      statusMessage: 'Internal Server Error',
      message: process.env.NODE_ENV === 'development' 
        ? (error as Error).message 
        : 'An unexpected error occurred'
    })
  }
})
```

### 5. State Management với Pinia

#### Store Organization

```
stores/
├── auth.ts                     # Authentication state
├── cart.ts                     # Shopping cart
├── user/
│   ├── index.ts                # User store
│   ├── preferences.ts          # User preferences
│   └── settings.ts             # User settings
└── app/
    ├── theme.ts                # Theme state
    ├── notifications.ts         # Notification queue
    └── ui.ts                   # UI state (sidebar, modals)
```

#### Type-Safe Pinia Store

```typescript
// stores/auth.ts
import { defineStore } from 'pinia'
import type { User, LoginCredentials, AuthTokens } from '~/types'

interface AuthState {
  user: User | null
  tokens: AuthTokens | null
  isLoading: boolean
  error: string | null
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const tokens = ref<AuthTokens | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  
  // Getters
  const isAuthenticated = computed(() => !!user.value && !!tokens.value)
  const userRole = computed(() => user.value?.role ?? 'guest')
  const isAdmin = computed(() => userRole.value === 'admin')
  
  // Actions
  const login = async (credentials: LoginCredentials) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await $fetch<{ user: User; tokens: AuthTokens }>(
        '/api/auth/login',
        {
          method: 'POST',
          body: credentials
        }
      )
      
      user.value = response.user
      tokens.value = response.tokens
      
      // Store tokens
      if (import.meta.client) {
        localStorage.setItem('refreshToken', response.tokens.refreshToken)
      }
      
      return response
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Login failed'
      throw e
    } finally {
      isLoading.value = false
    }
  }
  
  const logout = async () => {
    try {
      if (tokens.value?.refreshToken) {
        await $fetch('/api/auth/logout', {
          method: 'POST',
          body: { refreshToken: tokens.value.refreshToken }
        })
      }
    } finally {
      user.value = null
      tokens.value = null
      
      if (import.meta.client) {
        localStorage.removeItem('refreshToken')
      }
      
      await navigateTo('/login')
    }
  }
  
  const refreshTokens = async () => {
    if (import.meta.client) {
      const refreshToken = localStorage.getItem('refreshToken')
      
      if (refreshToken) {
        const response = await $fetch<{ tokens: AuthTokens }>(
          '/api/auth/refresh',
          {
            method: 'POST',
            body: { refreshToken }
          }
        )
        
        tokens.value = response.tokens
        return response.tokens
      }
    }
    
    throw new Error('No refresh token available')
  }
  
  return {
    // State
    user,
    tokens,
    isLoading,
    error,
    // Getters
    isAuthenticated,
    userRole,
    isAdmin,
    // Actions
    login,
    logout,
    refreshTokens
  }
})
```

### 6. SEO Best Practices

#### useHead với Dynamic Data

```vue
<script setup lang="ts">
const route = useRoute()
const { data: product } = await useFetch(`/api/products/${route.params.id}`)

useHead({
  title: () => product.value?.name ?? 'Loading...',
  meta: [
    {
      name: 'description',
      content: () => product.value?.description ?? ''
    },
    {
      property: 'og:title',
      content: () => `${product.value?.name ?? 'Product'} | Shop`
    },
    {
      property: 'og:description',
      content: () => product.value?.description ?? ''
    },
    {
      property: 'og:image',
      content: () => product.value?.image ?? '/default-og.png'
    },
    {
      property: 'og:type',
      content: 'product'
    },
    {
      name: 'twitter:card',
      content: 'summary_large_image'
    }
  ],
  link: [
    {
      rel: 'canonical',
      href: () => `https://example.com/products/${route.params.id}`
    }
  ],
  script: [
    {
      type: 'application/ld+json',
      innerHTML: () => JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'Product',
        name: product.value?.name,
        description: product.value?.description,
        image: product.value?.image,
        offers: {
          '@type': 'Offer',
          price: product.value?.price,
          priceCurrency: 'USD'
        }
      })
    }
  ]
})
</script>
```

#### useSeoMeta cho Common Patterns

```vue
<script setup lang="ts">
const { data: article } = await useFetch(`/api/articles/${route.params.slug}`)

// Simplified API cho common SEO meta
useSeoMeta({
  title: () => article.value?.title,
  description: () => article.value?.excerpt,
  ogTitle: () => article.value?.title,
  ogDescription: () => article.value?.excerpt,
  ogImage: () => article.value?.coverImage,
  ogType: 'article',
  twitterCard: 'summary_large_image',
  articleAuthor: () => article.value?.author?.name,
  articlePublishedTime: () => article.value?.publishedAt
})
</script>
```

### 7. Performance Best Practices

#### Image Optimization

```vue
<!-- Using @nuxt/image -->
<template>
  <!-- Responsive images -->
  <NuxtImg
    src="/images/product.jpg"
    alt="Product image"
    width="400"
    height="300"
    format="webp"
    loading="lazy"
    sizes="sm:100vw md:50vw lg:400px"
  />
  
  <!-- Priority loading for LCP images -->
  <NuxtImg
    src="/images/hero.jpg"
    alt="Hero image"
    width="1200"
    height="600"
    priority
  />
</template>
```

```typescript
// nuxt.config.ts - Image module configuration
export default defineNuxtConfig({
  image: {
    quality: 80,
    format: ['webp', 'avif'],
    screens: {
      xs: 320,
      sm: 640,
      md: 768,
      lg: 1024,
      xl: 1280,
      xxl: 1536
    },
    domains: ['cdn.example.com'],
    alias: {
      assets: '~/assets'
    }
  }
})
```

#### Route Rules cho Optimal Caching

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    // Homepage - prerender at build time
    '/': { prerender: true },
    
    // Blog - prerender all posts
    '/blog': { prerender: true },
    '/blog/**': { prerender: true },
    
    // Documentation - prerender
    '/docs/**': { prerender: true },
    
    // Product listing - ISR (revalidate every hour)
    '/products': { swr: 3600 },
    
    // Product detail - ISR
    '/products/**': { swr: 3600 },
    
    // User dashboard - no caching (always fresh)
    '/dashboard/**': { cache: false },
    
    // API routes - no caching
    '/api/**': { cache: false },
    
    // Admin - SPA mode
    '/admin/**': { ssr: false },
    
    // Auth pages - SSR for SEO
    '/auth/**': { ssr: true }
  }
})
```

#### Component Lazy Loading

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  components: {
    dirs: [
      {
        // Auto-lazy-load heavy components
        path: '~/components/heavy',
        pattern: '**/*',
        lazy: true
      },
      {
        // Auto-lazy-load all modal components
        path: '~/components/modals',
        pattern: '**/*',
        lazy: true
      },
      {
        // Regular components - not lazy
        path: '~/components/ui',
        prefix: 'Ui'
      }
    ]
  }
})
```

```vue
<!-- Manual lazy loading khi cần -->
<script setup lang="ts">
const HeavyChart = defineAsyncComponent({
  loader: () => import('~/components/HeavyChart.vue'),
  loadingComponent: ChartSkeleton,
  errorComponent: ChartError,
  delay: 200,
  timeout: 3000
})
</script>
```

### 8. Error Handling Best Practices

#### Global Error Page

```vue
<!-- error.vue -->
<template>
  <NuxtLayout>
    <div class="error-page">
      <div class="error-content">
        <h1 class="error-code">{{ error.statusCode }}</h1>
        <h2 class="error-title">{{ errorTitle }}</h2>
        <p class="error-message">{{ error.message }}</p>
        
        <div class="error-actions">
          <NuxtLink to="/" class="btn-primary">
            Go Home
          </NuxtLink>
          <button @click="handleError" class="btn-secondary">
            Try Again
          </button>
        </div>
        
        <details v-if="isDev" class="error-stack">
          <summary>Error Details</summary>
          <pre>{{ error.stack }}</pre>
        </details>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import type { NuxtError } from '#app'

const props = defineProps<{
  error: NuxtError
}>()

const isDev = import.meta.dev

const errorTitle = computed(() => {
  switch (props.error.statusCode) {
    case 404:
      return 'Page Not Found'
    case 500:
      return 'Server Error'
    case 403:
      return 'Access Denied'
    default:
      return 'Something Went Wrong'
  }
})

const handleError = () => {
  clearError({ redirect: '/' })
}
</script>
```

#### Client-Side Error Boundaries

```vue
<!-- components/ErrorBoundary.vue -->
<template>
  <slot v-if="!hasError" />
  <div v-else class="error-boundary" :class="variant">
    <div v-if="variant === 'alert'" class="error-alert">
      <span>{{ errorMessage }}</span>
      <button @click="reset">Dismiss</button>
    </div>
    <div v-else class="error-fallback">
      <p>{{ fallbackMessage }}</p>
      <button @click="reset">{{ retryText }}</button>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(defineProps<{
  fallbackMessage?: string
  retryText?: string
  variant?: 'alert' | 'fallback'
  onError?: (error: Error) => void
}>(), {
  fallbackMessage: 'Something went wrong',
  retryText: 'Retry',
  variant: 'fallback'
})

const hasError = ref(false)
const errorMessage = ref('')

onErrorCaptured((error) => {
  hasError.value = true
  errorMessage.value = error.message
  props.onError?.(error)
  
  // Prevent error from propagating
  return false
})

const reset = () => {
  hasError.value = false
  errorMessage.value = ''
}
</script>
```

## Common Patterns

### Authentication Pattern

```typescript
// composables/useAuth.ts
export const useAuth = () => {
  const authStore = useAuthStore()
  const { isAuthenticated, user, isAdmin } = storeToRefs(authStore)
  const { login, logout, refreshTokens } = authStore
  
  // Redirect if not authenticated
  const requireAuth = async () => {
    if (!isAuthenticated.value) {
      await navigateTo('/login')
    }
  }
  
  // Redirect if not admin
  const requireAdmin = async () => {
    await requireAuth()
    if (!isAdmin.value) {
      throw createError({
        statusCode: 403,
        message: 'Admin access required'
      })
    }
  }
  
  return {
    isAuthenticated,
    user,
    isAdmin,
    login,
    logout,
    requireAuth,
    requireAdmin
  }
}
```

```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware(async (to) => {
  const { isAuthenticated } = useAuth()
  
  // Public routes that don't need auth
  const publicRoutes = ['/login', '/register', '/forgot-password']
  
  if (!publicRoutes.includes(to.path) && !isAuthenticated.value) {
    return navigateTo(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
  }
  
  // Redirect authenticated users away from auth pages
  if (publicRoutes.includes(to.path) && isAuthenticated.value) {
    return navigateTo('/dashboard')
  }
})
```

### Form Validation Pattern

```typescript
// composables/useForm.ts
import { z } from 'zod'

export const useForm = <T extends z.ZodType>(
  schema: T,
  initialValues?: z.infer<T>
) => {
  const values = ref(initialValues ?? {} as z.infer<T>)
  const errors = ref<Record<string, string>>({})
  const isSubmitting = ref(false)
  const isDirty = ref(false)
  
  const validate = () => {
    const result = schema.safeParse(values.value)
    
    if (!result.success) {
      errors.value = result.error.flatten().fieldErrors
        .reduce((acc, err) => {
          const [field, messages] = Object.entries(err)[0]
          acc[field] = messages.join(', ')
          return acc
        }, {} as Record<string, string>)
      return false
    }
    
    errors.value = {}
    return true
  }
  
  const submit = async (handler: (values: z.infer<T>) => Promise<void>) => {
    if (!validate()) return
    
    isSubmitting.value = true
    try {
      await handler(values.value)
      isDirty.value = false
    } finally {
      isSubmitting.value = false
    }
  }
  
  // Mark as dirty on change
  watch(values, () => {
    isDirty.value = true
  }, { deep: true })
  
  return {
    values,
    errors,
    isSubmitting,
    isDirty,
    validate,
    submit
  }
}
```

```vue
<script setup lang="ts">
import { z } from 'zod'

const schema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  remember: z.boolean().optional()
})

const { values, errors, isSubmitting, submit } = useForm(schema, {
  email: '',
  password: '',
  remember: false
})

const handleSubmit = () => {
  submit(async (data) => {
    await $fetch('/api/auth/login', {
      method: 'POST',
      body: data
    })
    await navigateTo('/dashboard')
  })
}
</script>
```

## Troubleshooting

### Performance Issues

**Issue**: Slow initial page load

**Diagnosis Steps**:
1. Run `npx nuxi analyze` để xem bundle contents
2. Check Network tab cho large payloads
3. Verify images are optimized và lazy-loaded

**Solutions**:
- Enable route rules cho proper caching
- Lazy-load heavy components
- Optimize images với @nuxt/image
- Enable compression (gzip/brotli)
- Consider using CDN

### SSR Issues

**Issue**: Hydration mismatch

**Diagnosis Steps**:
1. Enable Vue devtools hydration overlay
2. Check for random values in templates
3. Verify browser-only APIs are properly guarded

**Solutions**:
- Move browser-only logic vào onMounted
- Use ClientOnly component khi cần
- Avoid Date.now() hoặc Math.random() in templates

### State Management Issues

**Issue**: State not persisting across navigation

**Diagnosis Steps**:
1. Verify state is stored in correct location (payload, sessionStorage, Pinia)
2. Check if page refreshes clear state

**Solutions**:
- Use useState for SSR-safe shared state
- Persist critical state to sessionStorage/localStorage
- Use Pinia with persistence plugin for complex state

## Examples

### Complete Page Example

```vue
<!-- pages/products/[category]/[id].vue -->
<template>
  <div class="product-page">
    <div v-if="pending" class="loading">
      <ProductSkeleton />
    </div>
    
    <div v-else-if="error" class="error">
      <ErrorMessage :error="error" @retry="refresh" />
    </div>
    
    <template v-else-if="product">
      <div class="product-layout">
        <div class="product-gallery">
          <NuxtImg
            :src="product.mainImage"
            :alt="product.name"
            width="600"
            height="600"
            priority
          />
          <div class="thumbnail-grid">
            <NuxtImg
              v-for="img in product.images"
              :key="img"
              :src="img"
              :alt="`${product.name} thumbnail`"
              width="100"
              height="100"
            />
          </div>
        </div>
        
        <div class="product-info">
          <h1>{{ product.name }}</h1>
          <p class="price">${{ product.price }}</p>
          <p class="description">{{ product.description }}</p>
          
          <div class="actions">
            <AddToCartButton
              :product="product"
              @added="showCartNotification"
            />
            <AddToWishlistButton :product="product" />
          </div>
          
          <ProductMeta :product="product" />
        </div>
      </div>
      
      <ProductReviews :product-id="product.id" />
      <RelatedProducts :category="product.category" />
    </template>
  </div>
</template>

<script setup lang="ts">
import type { Product } from '~/types'

const route = useRoute()
const { addToCart } = useCart()
const { addToast } = useNotifications()

// SEO
useHead({
  title: () => product.value?.name ?? 'Loading...',
  meta: () => ({
    description: product.value?.description
  })
})

// Data fetching
const { data: product, pending, error, refresh } = await useAsyncData(
  `product-${route.params.category}-${route.params.id}`,
  () => $fetch<Product>(`/api/products/${route.params.id}`),
  {
    default: () => null,
    server: true
  }
)

// Methods
const showCartNotification = () => {
  addToast({
    type: 'success',
    message: 'Added to cart'
  })
}

// Meta info
if (!product.value) {
  throw createError({
    statusCode: 404,
    message: 'Product not found'
  })
}
</script>

<style scoped>
.product-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.product-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
}

@media (max-width: 768px) {
  .product-layout {
    grid-template-columns: 1fr;
  }
}
</style>
```

## References

### Official Resources

- [Nuxt 3 Documentation](https://nuxt.com/docs)
- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Nitro Documentation](https://nitro.unjs.io/)

### Related Rules

- Xem `anti-pattern.md` trong thư mục này để tránh common mistakes
- Xem `architecture.md` để hiểu Nuxt's internals
- Xem `vue.mdc` cho Vue.js specific guidelines
- Xem `performance.mdc` cho performance optimization tips
- Xem `api.mdc` cho API design best practices
- Xem `security.mdc` cho security considerations
