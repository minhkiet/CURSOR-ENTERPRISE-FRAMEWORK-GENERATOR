---
title: "Nuxt FAQ - Câu Hỏi Thường Gặp"
description: "Tổng hợp các câu hỏi thường gặp về Nuxt.js với câu trả lời chi tiết từ chuyên gia"
tags: ["nuxt", "vue", "faq", "questions", "answers", "troubleshooting"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Nuxt FAQ - Câu Hỏi Thường Gặp

## Overview

Tài liệu này tổng hợp các câu hỏi thường gặp nhất về Nuxt.js development, được phân loại theo topics và trả lời chi tiết với code examples. Các câu hỏi được thu thập từ documentation, community forums, và real-world project issues.

Nuxt.js là một framework với nhiều concepts có thể confusing cho beginners và даже experienced developers. FAQ này nhằm mục đích cung cấp quick answers cho common questions, giúp developers tiết kiệm thời gian debugging và research.

## Purpose

Bộ FAQ này phục vụ các mục đích chính sau:

1. **Quick Answers** - Giải đáp nhanh các thắc mắc thường gặp
2. **Problem Solving** - Hướng dẫn fix common issues
3. **Best Practices** - Recommend correct approaches
4. **Migration Help** - Assist với Nuxt 2 → Nuxt 3 migration

## General Questions

### Q1: Nuxt 3 vs Nuxt 2 - Nên chọn cái nào?

**Short Answer**: Luôn chọn Nuxt 3 cho projects mới.

**Detailed Answer**: Nuxt 3 được viết lại hoàn toàn với Vue 3, mang lại nhiều cải tiến đáng kể so với Nuxt 2:

| Aspect | Nuxt 2 | Nuxt 3 |
|--------|--------|--------|
| Vue Version | Vue 2 | Vue 3 |
| Build Tool | Webpack | Vite |
| Server Engine | Express | Nitro |
| State Management | Vuex | Pinia (recommended) |
| TypeScript | Partial | Full support |
| Bundle Size | Larger | Up to 60% smaller |
| Active Development | Ended (LTS only) | Active |

**Migration Path**: Nếu đang có Nuxt 2 project, có thể migrate dần dần sử dụng Nuxt Bridge để chạy Nuxt 3 compatibility layer.

**Recommendation**: 
- **New Projects**: Bắt đầu với Nuxt 3 ngay
- **Nuxt 2 Projects**: Consider migration, especially for new features
- **Enterprise**: Evaluate migration cost vs benefits

---

### Q2: Sự khác nhau giữa SSR, SSG, và SPA là gì?

**Short Answer**: Các rendering modes khác nhau ở nơi và khi nào HTML được generate.

**Detailed Answer**:

#### Server-Side Rendering (SSR)
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    '/dashboard/**': { ssr: true } // Default
  }
})
```
- **Khi nào**: Server render HTML cho mỗi request
- **Ưu điểm**: SEO tốt, First Contentful Paint nhanh, personalized content
- **Nhược điểm**: Cần server, potential latency, more complex deployment
- **Use cases**: E-commerce, user dashboards, social media apps

#### Static Site Generation (SSG)
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    '/': { prerender: true },
    '/blog/**': { prerender: true }
  }
})
```
- **Khi nào**: HTML pre-generated tại build time
- **Ưu điểm**: Fastest performance, simple deployment, can host anywhere
- **Nhược điểm**: Phải rebuild để update content, không personalized
- **Use cases**: Documentation, blogs, marketing sites

#### Single Page Application (SPA)
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    '/admin/**': { ssr: false }
  }
})
```
- **Khi nào**: Browser download JS và render hoàn toàn client-side
- **Ưu điểm**: Fast navigation sau initial load, no server needed
- **Nhược điểm**: Poor SEO (without workarounds), slower initial load, requires JS
- **Use cases**: Admin panels, complex web apps, authenticated dashboards

#### Hybrid Rendering
```typescript
// Kết hợp nhiều modes trong một app
export default defineNuxtConfig({
  routeRules: {
    '/': { prerender: true },           // SSG
    '/blog/**': { prerender: true },    // SSG
    '/products/**': { swr: 3600 },       // SWR
    '/dashboard/**': { ssr: true },     // SSR
    '/admin/**': { ssr: false }         // SPA
  }
})
```

---

### Q3: Nuxt 3 có hỗ trợ TypeScript không?

**Short Answer**: Có, với full support bao gồm auto-generated types.

**Detailed Answer**: Nuxt 3 có first-class TypeScript support:

```typescript
// Type-safe composables
export const useUser = (id: string) => {
  const { data: user } = useFetch<User>(`/api/users/${id}`)
  return { user }
}

// Type-safe API routes
import { z } from 'zod'

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email()
})

export default defineEventHandler(async (event) => {
  // ...
})
```

**Features**:
- Auto-generates types cho pages, composables, và plugins
- Type-safe `runtimeConfig`
- Built-in TypeScript compiler (không cần tạo `tsconfig.json` thủ công)
- IDE integration với Volar

---

### Q4: Làm sao để debug ứng dụng Nuxt?

**Short Answer**: Sử dụng Nuxt DevTools và browser DevTools.

**Detailed Answer**:

#### Nuxt DevTools
```bash
# Enable trong nuxt.config.ts
export default defineNuxtConfig({
  devtools: { enabled: true }
})
```
- Component inspector
- Page routing visualization
- Module management
- Payload inspection

#### Browser DevTools
```typescript
// Add breakpoints trong source files
export default defineEventHandler(async (event) => {
  debugger; // Browser sẽ pause ở đây
  const data = await fetchData()
  return data
})
```

#### Server Debugging
```bash
# Run với debug flags
NODE_OPTIONS="--inspect" npx nuxt dev

# Hoặc sử dụng VS Code launch config
{
  "type": "node",
  "request": "launch",
  "name": "Debug Nuxt",
  "runtimeExecutable": "npx",
  "runtimeArgs": ["nuxt", "dev"],
  "env": { "NODE_OPTIONS": "--inspect" }
}
```

---

## Data Fetching Questions

### Q5: useFetch vs useAsyncData - Nên dùng cái nào?

**Short Answer**: `useFetch` cho hầu hết cases, `useAsyncData` khi cần custom configuration.

**Detailed Answer**:

#### useFetch (Recommended for most cases)
```typescript
// Simple GET request - auto-generates cache key
const { data, pending, error } = await useFetch('/api/users')

// Với options
const { data } = await useFetch('/api/users', {
  method: 'POST',
  body: { name: 'John' },
  headers: { Authorization: `Bearer ${token}` }
})
```

**When to use**:
- Simple CRUD operations
- Auto-generated cache keys are sufficient
- Minimal configuration needed

#### useAsyncData (For advanced cases)
```typescript
// Custom cache key
const { data } = await useAsyncData('custom-key', () => $fetch('/api/data'))

// Multiple parallel requests
const [{ data: users }, { data: posts }] = await Promise.all([
  useAsyncData('users', () => $fetch('/api/users')),
  useAsyncData('posts', () => $fetch('/api/posts'))
])

// Custom transform
const { data } = await useAsyncData('users', () => $fetch('/api/users'), {
  transform: (users) => users.map(u => ({ ...u, fullName: u.name }))
})
```

**When to use**:
- Need custom cache key
- Multiple parallel fetches
- Complex data transformations
- Need more control over the fetching process

---

### Q6: Data fetch nhưng page vẫn loading - Làm sao?

**Short Answer**: Kiểm tra xem có await promise và sử dụng `pending` state đúng cách.

**Common Issues và Solutions**:

#### Issue 1: Missing await
```vue
<!-- ❌ Không await - data sẽ không có khi render -->
<script setup lang="ts">
useFetch('/api/data') // Missing await
</script>

<!-- ✅ Correct -->
<script setup lang="ts">
const { data } = await useFetch('/api/data')
</script>
```

#### Issue 2: Using v-if with isLoading
```vue
<!-- ❌ isLoading không phải là reactive trong script setup context -->
<script setup lang="ts">
const { data, isLoading } = await useFetch('/api/data')
</script>

<!-- ✅ Correct - sử dụng pending -->
<script setup lang="ts">
const { data, pending } = await useFetch('/api/data')
</script>

<template>
  <div v-if="pending">
    <LoadingSpinner />
  </div>
  <div v-else>
    {{ data }}
  </div>
</template>
```

#### Issue 3: Client-only data fetching
```vue
<!-- ❌ Fetch trong onMounted - không SSR -->
<script setup lang="ts">
onMounted(async () => {
  const response = await fetch('/api/data')
  data.value = await response.json()
})
</script>

<!-- ✅ Correct - useFetch tự động SSR -->
<script setup lang="ts">
const { data } = await useFetch('/api/data')
</script>
```

---

### Q7: Làm sao để cache API responses?

**Short Answer**: Configure qua `routeRules` hoặc sử dụng `getCachedData` option.

**Detailed Answer**:

#### Route Rules Caching
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    // Cache for 1 hour, revalidate in background
    '/blog': { swr: 3600 },
    
    // Cache với maxAge
    '/products': { 
      cache: { 
        maxAge: 3600,
        staleMaxAge: 86400
      } 
    },
    
    // No caching
    '/api/user/**': { cache: false }
  }
})
```

#### Manual Cache Control
```typescript
const { data } = await useAsyncData('key', () => $fetch('/api/data'), {
  // Custom cache key
  key: 'custom-key',
  
  // Custom cache getter
  getCachedData(key, nuxtApp) {
    return nuxtApp.payload.data[key] || nuxtApp.static.data[key]
  }
})
```

---

## State Management Questions

### Q8: useState vs Pinia - Nên dùng cái nào?

**Short Answer**: `useState` cho simple state, Pinia cho complex state management.

**Decision Guide**:

```
State cần shared giữa các components?
│
├─ Không → ref() hoặc reactive() đủ
│
└─ Có → State có business logic phức tạp không?
        │
        ├─ Không → useState()
        │
        └─ Có → Pinia Store
```

**useState Examples**:
```typescript
// Simple counter
const count = useState('count', () => 0)

// User state
const user = useState<User | null>('user', () => null)

// Form state
const form = useState('contact-form', () => ({
  name: '',
  email: '',
  message: ''
}))
```

**Pinia Examples**:
```typescript
// stores/cart.ts
import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])
  const itemCount = computed(() => items.value.length)
  
  const addItem = (product: Product) => {
    items.value.push(product)
  }
  
  return { items, itemCount, addItem }
})

// Usage
const cart = useCartStore()
cart.addItem(product)
```

---

### Q9: State không persist khi navigate - Làm sao?

**Short Answer**: Sử dụng `useState` thay vì `ref()` để enable SSR hydration.

**Problem**:
```typescript
// ❌ ref() tạo local state - lost on navigation
const count = ref(0)

// ✅ useState() shared state - persisted
const count = useState('count', () => 0)
```

**SSR Hydration Flow**:
```typescript
// 1. Server creates state
const count = useState('count', () => 0)
count.value = 42

// 2. State serialized to payload
// window.__NUXT__ = { data: { count: 42 } }

// 3. Client hydrates from payload
// count.value is already 42, no refetch needed
```

**For Pinia - Add Persistence**:
```typescript
// stores/auth.ts
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const token = useState<string | null>('auth-token', () => null)
  
  // Persist to localStorage
  if (import.meta.client) {
    const saved = localStorage.getItem('auth-token')
    if (saved) token.value = saved
    
    watch(token, (newToken) => {
      if (newToken) {
        localStorage.setItem('auth-token', newToken)
      } else {
        localStorage.removeItem('auth-token')
      }
    })
  }
  
  return { token }
})
```

---

## Component Questions

### Q10: Component không render trên server - Làm sao?

**Short Answer**: Kiểm tra xem có sử dụng browser-only APIs không được wrapped đúng cách.

**Common Causes và Solutions**:

#### Cause 1: Using window/document
```typescript
// ❌ Error: window is not defined on server
const width = window.innerWidth

// ✅ Correct - use onMounted
const width = ref(0)
onMounted(() => {
  width.value = window.innerWidth
})

// ✅ Or use import.meta check
if (import.meta.client) {
  width.value = window.innerWidth
}
```

#### Cause 2: Module-level browser access
```typescript
// ❌ This runs on both server and client
import { createClient } from 'some-lib'

// ✅ Lazy import
const client = ref(null)
onMounted(async () => {
  client.value = await import('some-lib').then(m => m.createClient())
})
```

#### Cause 3: Need ClientOnly wrapper
```vue
<!-- When component truly can't be SSR'd -->
<template>
  <ClientOnly>
    <BrowserOnlyChart />
    <template #fallback>
      <ChartSkeleton />
    </template>
  </ClientOnly>
</template>
```

---

### Q11: Props không reactive - Làm sao?

**Short Answer**: Props được reactive by default trong Vue 3, kiểm tra cách truy cập.

**Common Issues**:

#### Issue 1: Destructuring loses reactivity
```vue
<script setup lang="ts">
// ❌ Destructuring props breaks reactivity
const { title, count } = defineProps<{
  title: string
  count: number
}>()

// ✅ Access via props or keep reactive
const props = defineProps<{
  title: string
  count: number
}>()

// Using in template - auto-unwraps
console.log(props.count)

// ✅ Or use withDefaults
const props = withDefaults(defineProps<{
  title: string
  count?: number
}>(), {
  count: 0
})
</script>
```

#### Issue 2: Watch không trigger
```vue
<script setup lang="ts">
const props = defineProps<{
  userId: string
}>()

// ✅ Watch props directly
watch(() => props.userId, (newId) => {
  fetchUser(newId)
})
</script>
```

---

## Performance Questions

### Q12: Bundle size quá lớn - Làm sao tối ưu?

**Short Answer**: Sử dụng bundle analyzer và lazy load heavy components.

**Optimization Steps**:

#### 1. Analyze Bundle
```bash
npx nuxi analyze
```

#### 2. Lazy Load Components
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  components: {
    dirs: [
      {
        path: '~/components/heavy',
        pattern: '**/*',
        lazy: true // Auto-lazy-load
      }
    ]
  }
})
```

```vue
<!-- Manual lazy loading -->
<script setup lang="ts">
const HeavyChart = defineAsyncComponent(() => 
  import('~/components/HeavyChart.vue')
)
</script>
```

#### 3. Optimize Dependencies
```typescript
// ❌ Import entire library
import _ from 'lodash'

// ✅ Import specific functions
import debounce from 'lodash-es/debounce'
import cloneDeep from 'lodash-es/cloneDeep'
```

#### 4. Enable Route Rules
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    // Pre-render static pages
    '/': { prerender: true },
    
    // ISR for dynamic content
    '/blog/**': { swr: 3600 }
  }
})
```

---

### Q13: Images load chậm - Làm sao cải thiện?

**Short Answer**: Sử dụng `@nuxt/image` module với `<NuxtImg>` component.

**Setup**:
```bash
npm install @nuxt/image
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@nuxt/image'],
  image: {
    quality: 80,
    format: ['webp', 'avif']
  }
})
```

**Usage**:
```vue
<!-- Basic usage -->
<NuxtImg
  src="/images/hero.jpg"
  alt="Hero image"
  width="1200"
  height="600"
  loading="lazy"
/>

<!-- Responsive -->
<NuxtImg
  src="/images/product.jpg"
  alt="Product"
  sizes="sm:100vw md:50vw lg:400px"
/>

<!-- Priority for LCP -->
<NuxtImg
  src="/images/hero.jpg"
  alt="Hero"
  width="1920"
  height="1080"
  priority
/>
```

---

## Server Routes Questions

### Q14: Làm sao để validate API input?

**Short Answer**: Sử dụng Zod schema validation.

**Setup**:
```bash
npm install zod
```

**Usage**:
```typescript
// server/api/users.post.ts
import { z } from 'zod'

const CreateUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  name: z.string().min(2, 'Name must be at least 2 characters'),
  password: z.string().min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase')
    .regex(/[0-9]/, 'Password must contain number'),
  age: z.number().min(13).max(120).optional()
})

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  
  const result = CreateUserSchema.safeParse(body)
  
  if (!result.success) {
    throw createError({
      statusCode: 400,
      message: 'Validation failed',
      data: result.error.flatten()
    })
  }
  
  const { email, name, password, age } = result.data
  
  // Proceed với validated data
  const user = await prisma.user.create({
    data: { email, name, passwordHash: await hash(password), age }
  })
  
  return { user: sanitizeUser(user) }
})
```

---

### Q15: Làm sao để handle authentication trong API routes?

**Short Answer**: Sử dụng server middleware và event context.

**Middleware**:
```typescript
// server/middleware/auth.ts
export default defineEventHandler(async (event) => {
  // Skip for public routes
  const publicPaths = ['/api/auth/login', '/api/health']
  if (publicPaths.some(p => event.path.startsWith(p))) {
    return
  }
  
  const authHeader = getHeader(event, 'authorization')
  
  if (!authHeader?.startsWith('Bearer ')) {
    throw createError({
      statusCode: 401,
      message: 'Missing authorization header'
    })
  }
  
  const token = authHeader.slice(7)
  
  try {
    const payload = verifyJWT(token)
    event.context.user = payload
  } catch {
    throw createError({
      statusCode: 401,
      message: 'Invalid token'
    })
  }
})
```

**Protected Route**:
```typescript
// server/api/profile.get.ts
export default defineEventHandler(async (event) => {
  const user = event.context.user
  
  if (!user) {
    throw createError({
      statusCode: 401,
      message: 'Authentication required'
    })
  }
  
  const profile = await prisma.user.findUnique({
    where: { id: user.id }
  })
  
  return profile
})
```

---

## Deployment Questions

### Q16: Deploy lên Vercel như thế nào?

**Short Answer**: Push code lên Git repo và connect với Vercel.

**Steps**:

1. **Push code lên Git** (GitHub/GitLab/Bitbucket)
2. **Connect repo với Vercel**
3. **Vercel tự động detect Nuxt và deploy**

```typescript
// nuxt.config.ts - Verify preset
export default defineNuxtConfig({
  nitro: {
    preset: 'vercel' // Usually auto-detected
  }
})
```

**Configuration**:
```json
// vercel.json (optional)
{
  "buildCommand": "npm run build",
  "outputDirectory": ".output/public",
  "installCommand": "npm install"
}
```

**Environment Variables**:
- Set trong Vercel Dashboard
- Private variables cho server-only secrets
- Public variables cho client-accessible config

---

### Q17: Self-host với Docker như thế nào?

**Short Answer**: Build Docker image và run container.

**Dockerfile**:
```dockerfile
# Dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source
COPY . .

# Build
RUN npm run build

# Expose port
EXPOSE 3000

# Start
CMD ["node", ".output/server/index.mjs"]
```

**Build và Run**:
```bash
# Build image
docker build -t my-nuxt-app .

# Run container
docker run -p 3000:3000 \
  -e DATABASE_URL="postgresql://..." \
  -e NUXT_PUBLIC_API_BASE="https://api.example.com" \
  my-nuxt-app
```

**Docker Compose**:
```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/mydb
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

---

## Troubleshooting Questions

### Q18: "Hydration node mismatch" error - Làm sao fix?

**Short Answer**: Kiểm tra template cho non-deterministic values và browser-only code.

**Common Causes và Fixes**:

#### Cause 1: Random values in template
```vue
<!-- ❌ Math.random() creates mismatch -->
<template>
  <div :key="Math.random()">{{ item }}</div>
</template>

<!-- ✅ Use stable keys -->
<template>
  <div :key="item.id">{{ item }}</div>
</template>
```

#### Cause 2: Date/time in template
```vue
<!-- ❌ Date.now() creates different values -->
<template>
  <span>{{ Date.now() }}</span>
</template>

<!-- ✅ Move to computed or use formatted date -->
<script setup lang="ts">
const now = ref(new Date())
onMounted(() => {
  // Client-side only
})
</script>
```

#### Cause 3: Browser-only APIs in template
```vue
<!-- ❌ window not available on server -->
<script setup lang="ts">
const width = window.innerWidth
</script>

<!-- ✅ Use refs and onMounted -->
<script setup lang="ts">
const width = ref(0)
onMounted(() => {
  width.value = window.innerWidth
})
</script>
```

---

### Q19: Page không update khi query params thay đổi

**Short Answer**: Sử dụng `watchQuery` hoặc `watch` trên route.

**Solution 1: watchQuery**
```vue
<script setup lang="ts">
definePageMeta({
  watchQuery: ['page', 'filter'] // Re-fetch when these change
})

const route = useRoute()
const { data } = await useFetch('/api/items', {
  query: {
    page: () => route.query.page,
    filter: () => route.query.filter
  }
})
</script>
```

**Solution 2: Manual watch**
```vue
<script setup lang="ts">
const route = useRoute()

// Watch for query changes
watch(
  () => route.query,
  async (newQuery) => {
    await refreshNuxtData('items')
  }
)

const { data, refresh } = await useAsyncData('items', () => 
  $fetch('/api/items', { query: route.query })
)
</script>
```

---

### Q20: Module không hoạt động sau khi install

**Short Answer**: Kiểm tra installation và configuration.

**Diagnosis Steps**:

```bash
# 1. Verify installation
npm ls @nuxt/image

# 2. Check nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@nuxt/image'] // Should be in modules, not dependencies
})

# 3. Check TypeScript types
npx nuxi prepare

# 4. Restart dev server
npm run dev
```

**Common Issues**:

1. **Module not in `modules`**: Must be in `modules` array, not `dependencies`
2. **TypeScript cache**: Run `npx nuxi prepare` after install
3. **Version mismatch**: Check Nuxt version compatibility
4. **Config order**: Some modules must be loaded before others

---

## Migration Questions

### Q21: Migrate từ Nuxt 2 sang Nuxt 3 như thế nào?

**Short Answer**: Sử dụng Nuxt Bridge để migrate dần dần, hoặc full migration.

**Migration Steps**:

1. **Update Vue 2 → Vue 3 syntax**
   ```vue
   <!-- Nuxt 2 -->
   <script>
   export default {
     data() {
       return { count: 0 }
     }
   }
   </script>
   
   <!-- Nuxt 3 -->
   <script setup lang="ts">
   const count = ref(0)
   </script>
   ```

2. **Update Vuex → Pinia**
   ```typescript
   // Nuxt 2 - Vuex
   export default {
     state: () => ({ count: 0 }),
     mutations: { increment(state) { state.count++ } },
     actions: { increment({ commit }) { commit('increment') } }
   }
   
   // Nuxt 3 - Pinia
   export const useCounterStore = defineStore('counter', () => {
     const count = ref(0)
     const increment = () => count.value++
     return { count, increment }
   })
   ```

3. **Update plugins**
   ```typescript
   // Nuxt 2
   export default ({ app }, inject) => {
     app.$myPlugin = () => 'Hello'
   }
   
   // Nuxt 3
   export default defineNuxtPlugin((nuxtApp) => {
     nuxtApp.provide('myPlugin', () => 'Hello')
   })
   ```

4. **Update middleware**
   ```typescript
   // Nuxt 2
   export default function ({ store, redirect }) {
     if (!store.isAuthenticated) {
       return redirect('/login')
     }
   }
   
   // Nuxt 3
   export default defineNuxtRouteMiddleware((to) => {
     const { isAuthenticated } = useAuth()
     if (!isAuthenticated.value) {
       return navigateTo('/login')
     }
   })
   ```

**Using Nuxt Bridge** (Incremental migration):
```bash
npm install @nuxt/bridge
```

```typescript
// nuxt.config.ts
import { defineNuxtConfig } from '@nuxt/bridge-config'

export default defineNuxtConfig({
  bridge: {
    meta: true,
    typescript: true
  }
})
```

---

## Best Practices Questions

### Q22: Nên đặt business logic ở đâu?

**Short Answer**: Trong composables hoặc Pinia stores, không trong components.

**Recommended Structure**:
```
composables/
├── useAuth.ts           # Authentication logic
├── useCart.ts          # Shopping cart logic
└── useForm.ts          # Form handling logic

stores/                 # Pinia stores (for complex state)
├── auth.ts
├── cart.ts
└── products.ts

server/
├── api/                # Server-side business logic
│   ├── orders/
│   │   ├── index.post.ts
│   │   └── [id].cancel.post.ts
│   └── validation.ts   # Shared validation schemas
```

**Anti-pattern**: Putting logic in components
```vue
<!-- ❌ Business logic in component -->
<script setup lang="ts">
const products = ref([])

const filteredProducts = computed(() => {
  // Complex filtering logic here
  return products.value
    .filter(p => p.active)
    .filter(p => p.category === selectedCategory.value)
    .sort((a, b) => b.createdAt - a.createdAt)
})

const addToCart = async (product) => {
  // API call in component
  await $fetch('/api/cart/add', {
    method: 'POST',
    body: { productId: product.id }
  })
  // Toast notification
  // Analytics tracking
  // ...
}
</script>
```

**Recommended**: Extract to composables
```typescript
// composables/useProducts.ts
export const useProducts = () => {
  const route = useRoute()
  const { data: products } = await useFetch('/api/products')
  
  const filteredProducts = computed(() => {
    if (!products.value) return []
    return products.value
      .filter(p => p.active)
      .filter(p => p.category === route.query.category)
      .sort((a, b) => b.createdAt - a.createdAt)
  })
  
  return { products: filteredProducts }
}

// composables/useCart.ts
export const useCart = () => {
  const toast = useToast()
  
  const addToCart = async (product: Product) => {
    await $fetch('/api/cart/add', {
      method: 'POST',
      body: { productId: product.id }
    })
    toast.success('Added to cart')
    trackEvent('add_to_cart', { productId: product.id })
  }
  
  return { addToCart }
}
```

```vue
<!-- ✅ Clean component -->
<script setup lang="ts">
const { products } = useProducts()
const { addToCart } = useCart()
</script>
```

---

## References

### Official Resources

- [Nuxt 3 Documentation](https://nuxt.com/docs)
- [Vue 3 Documentation](https://vuejs.org/guide)
- [Nitro Documentation](https://nitro.unjs.io/)
- [Nuxt GitHub Discussions](https://github.com/nuxt/nuxt/discussions)

### Community Resources

- [Nuxt Discord](https://discord.gg/nuxt)
- [Nuxt Nation](https://nuxtnation.com/)
- [Vue School](https://vueschool.io/)

### Related Documents

- Xem `architecture.md` để hiểu internal workings
- Xem `best-practice.md` để biết implementation guidance
- Xem `anti-pattern.md` để tránh common mistakes
- Xem `checklist.md` để review code trước deployment
