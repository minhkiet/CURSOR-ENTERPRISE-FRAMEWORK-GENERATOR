---
title: "Nuxt Anti-Patterns - Các Mẫu Cần Tránh"
description: "Danh sách đầy đủ các anti-patterns phổ biến trong Nuxt.js development cùng với giải pháp thực tế"
tags: ["nuxt", "vue", "ssr", "performance", "hydration", "best-practices"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Nuxt Anti-Patterns - Các Mẫu Cần Tránh

## Overview

Tài liệu này cung cấp danh sách toàn diện các anti-patterns phổ biến trong Nuxt.js development. Mỗi anti-pattern được phân tích chi tiết về nguyên nhân gây ra vấn đề, cách nhận diện, và giải pháp thay thế được khuyến nghị. Việc tránh các anti-patterns này giúp ứng dụng Nuxt đạt hiệu suất tối ưu, maintainability cao, và trải nghiệm người dùng mượt mà.

Nuxt.js là một framework mạnh mẽ với nhiều features tiện lợi, nhưng cũng dễ gây ra các vấn đề nếu không hiểu rõ cách hoạt động của nó, đặc biệt là trong bối cảnh SSR (Server-Side Rendering) và hydration. Các anti-patterns được liệt kê dưới đây được tổng hợp từ kinh nghiệm thực tế và các vấn đề thường gặp trong production deployments.

## Purpose

Mục đích của tài liệu này là giúp developers:

1. **Nhận diện sớm** các vấn đề tiềm ẩn trong codebase
2. **Hiểu nguyên nhân gốc rễ** của từng anti-pattern
3. **Áp dụng giải pháp đúng đắn** thay vì workarounds tạm thời
4. **Xây dựng thói quen code tốt** ngay từ đầu dự án
5. **Review code hiệu quả** với checklist rõ ràng cho team

Việc nắm vững các anti-patterns này đặc biệt quan trọng khi làm việc với Nuxt vì framework này có nhiều "magic" behaviors mà nếu không hiểu kỹ, có thể dẫn đến các bug khó debug như hydration mismatches, memory leaks, hoặc performance degradation.

## Key Concepts

### SSR Context và Client Context

Nuxt chạy code ở cả server và client. Điều này có nghĩa là một số APIs chỉ an toàn khi sử dụng ở client-side (như `window`, `document`, `localStorage`), trong khi một số khác chỉ available ở server-side (như reading files từ filesystem). Việc không phân biệt rõ ràng giữa hai context này là nguồn gốc của nhiều anti-patterns.

### Hydration Process

Hydration là quá trình Vue ".attach" event listeners và reactive systems vào DOM đã được server render sẵn. Nếu có bất kỳ sự khác biệt nào giữa HTML được server generate và DOM structure mà Vue expect, hydration mismatch sẽ xảy ra, gây ra flickering hoặc errors.

### Auto-imports System

Nuxt tự động import components, composables, và utilities từ các directories đặc biệt. Điều này tiện lợi nhưng cũng có thể dẫn đến confusion về nơi code được import từ đâu, và vô tình import các dependencies không cần thiết.

## Best Practices

### 1. Tránh Overusing Client-Only Components

**Anti-Pattern Description**: Việc đánh dấu components là `<ClientOnly>` khi không thực sự cần thiết là một anti-pattern phổ biến. Điều này gây ra:

- Content không được render trên server, ảnh hưởng SEO
- Tăng Time to First Contentful Paint (FCP)
- Layout shifts khi client-side hydration hoàn thành
- User có thể thấy blank spaces hoặc loading states không mong muốn

**Bad Pattern Example**:

```vue
<!-- Bad: Wrap toàn bộ page trong ClientOnly -->
<template>
  <ClientOnly>
    <Header />
    <main>
      <ProductList :products="products" />
    </main>
    <Footer />
  </ClientOnly>
</template>
```

**Root Cause**: Developers thường sử dụng `<ClientOnly>` vì họ không hiểu rõ cách làm cho components của họ SSR-compatible. Họ thường gặp lỗi khi sử dụng browser-only APIs như `window` hoặc `document` mà không có proper guards.

**Solution - Sử dụng onMounted Hook**:

```vue
<template>
  <div>
    <ClientOnly>
      <InteractiveChart :data="chartData" />
      <template #fallback>
        <StaticChartPlaceholder :data="chartData" />
      </template>
    </ClientOnly>
  </div>
</template>

<script setup lang="ts">
// Tốt hơn: Chỉ wrap phần cần client-only
// Sử dụng fallback slot để show loading state
</script>
```

**Better Solution - Sử dụng Process Check**:

```vue
<template>
  <div>
    <Chart v-if="isMounted" :data="chartData" />
    <ChartSkeleton v-else />
  </div>
</template>

<script setup lang="ts">
const isMounted = ref(false)

onMounted(() => {
  isMounted.value = true
})
</script>
```

**Best Solution - Composable Pattern**:

```typescript
// composables/useMounted.ts
export const useMounted = () => {
  const isMounted = useState('isMounted', () => false)
  
  onMounted(() => {
    isMounted.value = true
  })
  
  return { isMounted }
}
```

```vue
<template>
  <div>
    <Chart v-if="isMounted.value" :data="chartData" />
    <ChartSkeleton v-else />
  </div>
</template>

<script setup lang="ts">
const { isMounted } = useMounted()
</script>
```

### 2. Tránh Improper Data Fetching

**Anti-Pattern Description**: Fetching data trong `onMounted` hoặc sử dụng plain `fetch`/`axios` thay vì Nuxt's built-in data fetching composables là một anti-pattern nghiêm trọng.

**Bad Pattern Examples**:

```typescript
// Bad Pattern 1: Fetch trong onMounted
<script setup lang="ts">
const products = ref([])

onMounted(async () => {
  const response = await fetch('/api/products')
  products.value = await response.json()
})
</script>

// Bad Pattern 2: Double fetching (server + client)
<script setup lang="ts">
const { data } = await useFetch('/api/products') // Server fetch
const user = ref(null)

onMounted(async () => {
  const response = await fetch('/api/user') // Client fetch lại
  user.value = await response.json()
})
</script>

// Bad Pattern 3: Sử dụng axios thay vì $fetch
<script setup lang="ts">
import axios from 'axios'

const products = ref([])

// Không tận dụng được Nuxt's caching và deduplication
onMounted(async () => {
  const { data } = await axios.get('/api/products')
  products.value = data
})
</script>
```

**Root Cause**: Developers thường quen với cách làm việc trong Vue SPA thuần túy và không nhận thức được rằng Nuxt có những composables đặc biệt được thiết kế cho SSR context.

**Correct Pattern - useFetch**:

```typescript
// composables/useProducts.ts
export const useProducts = (category?: Ref<string> | string) => {
  const query = computed(() => ({
    category: unref(category)
  }))
  
  // Tự động deduplicate requests
  // Tự động cache kết quả
  // SSR-compatible
  const { data, pending, error, refresh } = useFetch('/api/products', {
    query,
    transform: (data) => data.products,
    key: () => `products-${unref(category)}`
  })
  
  return { products: data, pending, error, refresh }
}
```

```vue
<script setup lang="ts">
const category = ref('electronics')

// Sử dụng composable
const { products, pending, error } = useProducts(category)

// Watch for changes
watch(category, () => {
  // useFetch tự động refetch khi query thay đổi
})
</script>
```

**Correct Pattern - useAsyncData với Server Route**:

```typescript
// server/api/products.get.ts
export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  const category = query.category as string | undefined
  
  // Database call với proper typing
  const products = await prisma.product.findMany({
    where: category ? { category } : undefined,
    take: 20
  })
  
  return { products }
})
```

```vue
<script setup lang="ts">
// Sử dụng useAsyncData khi cần custom transform
const { data: products, pending, error } = await useAsyncData(
  'featured-products',
  () => $fetch('/api/products', {
    query: { featured: true }
  }),
  {
    transform: (data) => data.products,
    default: () => []
  }
)
</script>
```

### 3. Tránh Hydration Mismatches

**Anti-Pattern Description**: Hydration mismatch xảy ra khi HTML được server render khác với DOM structure mà Vue expect ở client-side. Điều này gây ra console errors và potential visual glitches.

**Bad Pattern Examples**:

```vue
<!-- Bad Pattern 1: Sử dụng Date.now() hoặc Math.random() trong template -->
<template>
  <div>
    <p>ID: {{ Math.random() }}</p>
    <p>Time: {{ new Date().toLocaleString() }}</p>
  </div>
</template>

<!-- Bad Pattern 2: Conditional rendering khác nhau server/client -->
<script setup lang="ts">
const isClient = ref(false)

onMounted(() => {
  isClient.value = true
})
</script>

<template>
  <div>
    <!-- Server: shows "Server"
         Client: shows "Client" sau hydration -->
    <span>{{ isClient ? 'Client' : 'Server' }}</span>
  </div>
</template>

<!-- Bad Pattern 3: Accessing window/document trực tiếp -->
<script setup lang="ts">
const width = window.innerWidth // Error ở server-side!
</script>

<!-- Bad Pattern 4: Using client-only values trong SSR -->
<script setup lang="ts">
const userAgent = navigator.userAgent // Error ở server-side!
</script>
```

**Root Cause**: Nuxt renders components trên server để generate HTML, sau đó client-side Vue hydrate HTML đó. Bất kỳ sự khác biệt nào giữa hai quá trình này đều gây ra mismatch.

**Solution - Sử dụng Process Check hoặc Built-in Composables**:

```vue
<!-- Good Pattern 1: Sử dụng useNuxtApp() -->
<script setup lang="ts">
const { process } = useNuxtApp()

// process.client chỉ true ở client-side
// process.server chỉ true ở server-side
</script>

<!-- Good Pattern 2: Sử dụng ClientOnly component -->
<template>
  <div>
    <StaticContent />
    <ClientOnly>
      <BrowserOnlyContent />
    </ClientOnly>
  </div>
</template>

<!-- Good Pattern 3: Sử dụng onMounted cho client-only logic -->
<script setup lang="ts">
const browserWidth = ref(0)

onMounted(() => {
  browserWidth.value = window.innerWidth
})
</script>

<template>
  <p>Window width: {{ browserWidth }}px</p>
</template>
```

**Solution - State Synchronization**:

```typescript
// composables/useWindowSize.ts
export const useWindowSize = () => {
  const width = ref(0)
  const height = ref(0)
  
  const updateSize = () => {
    width.value = window.innerWidth
    height.value = window.innerHeight
  }
  
  onMounted(() => {
    updateSize()
    window.addEventListener('resize', updateSize)
  })
  
  onUnmounted(() => {
    window.removeEventListener('resize', updateSize)
  })
  
  return { width, height }
}
```

```vue
<script setup lang="ts">
const { width, height } = useWindowSize()

// Luôn khởi tạo với giá trị mặc định
// để tránh mismatch
</script>
```

### 4. Tránh Memory Leaks

**Anti-Pattern Description**: Memory leaks trong Nuxt thường xảy ra khi không cleanup event listeners, subscriptions, hoặc intervals khi component unmounts.

**Bad Pattern Examples**:

```typescript
// Bad Pattern 1: Event listener không được cleanup
<script setup lang="ts">
const handleScroll = () => {
  console.log(window.scrollY)
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  // Không có onUnmounted để remove listener!
})
</script>

// Bad Pattern 2: Interval không được clear
<script setup lang="ts">
onMounted(() => {
  setInterval(() => {
    checkNotifications()
  }, 5000)
  // Interval tiếp tục chạy ngay cả khi component unmounted!
})
</script>

// Bad Pattern 3: WebSocket connection không được đóng
<script setup lang="ts">
const ws = ref<WebSocket | null>(null)

onMounted(() => {
  ws.value = new WebSocket('wss://api.example.com')
  ws.value.onmessage = (event) => {
    handleMessage(event)
  }
})
</script>
```

**Solution - Proper Cleanup**:

```typescript
// Good Pattern 1: Sử dụng useEventListener (auto-cleanup)
<script setup lang="ts">
import { useEventListener } from '@vueuse/core'

const scrollY = ref(0)

// Tự động cleanup khi component unmounted
useEventListener(window, 'scroll', () => {
  scrollY.value = window.scrollY
})
</script>

// Good Pattern 2: Manual cleanup với onUnmounted
<script setup lang="ts">
const handleScroll = () => {
  console.log(window.scrollY)
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

// Good Pattern 3: Sử dụng Composable pattern
// composables/useScrollPosition.ts
export const useScrollPosition = () => {
  const scrollY = ref(0)
  let scrollHandler: (() => void) | null = null
  
  onMounted(() => {
    scrollHandler = () => {
      scrollY.value = window.scrollY
    }
    window.addEventListener('scroll', scrollHandler)
  })
  
  onUnmounted(() => {
    if (scrollHandler) {
      window.removeEventListener('scroll', scrollHandler)
    }
  })
  
  return { scrollY }
}
```

```vue
<script setup lang="ts">
const { scrollY } = useScrollPosition()
</script>
```

**Solution - Auto-cleanup với useAsyncData**:

```typescript
// Bad: không cancel request khi component unmounted
const fetchData = async () => {
  const response = await fetch('/api/large-data')
  data.value = await response.json()
}

// Good: useFetch tự động cancel request
const { data } = useFetch('/api/large-data', {
  lazy: true // Cancel nếu user navigate away
})
```

### 5. Tránh Large Bundle Size

**Anti-Pattern Description**: Importing entire libraries thay vì specific imports, hoặc không lazy-loading heavy components dẫn đến bundle size quá lớn, ảnh hưởng đến initial load time.

**Bad Pattern Examples**:

```typescript
// Bad Pattern 1: Import entire library
import _ from 'lodash' // ~70KB gzipped

// Bad Pattern 2: Import entire Vue component library
import { Button, Input, Select, Modal, Table } from 'primevue'

// Bad Pattern 3: Synchronous import cho heavy components
import HeavyChart from '~/components/HeavyChart.vue'
```

**Solution - Tree-shaking và Lazy Loading**:

```typescript
// Good Pattern 1: Specific imports
import { debounce } from 'lodash-es' // Chỉ import debounce
import { cloneDeep } from 'lodash-es' // Hoặc import riêng từng function

// Good Pattern 2: Dynamic imports
const HeavyChart = defineAsyncComponent(() => 
  import('~/components/HeavyChart.vue')
)

// Good Pattern 3: Sử dụng Nuxt auto-imports optimization
// Trong nuxt.config.ts
export default defineNuxtConfig({
  components: [
    {
      path: '~/components',
      pathPrefix: false // Không prefix component names
    }
  ]
})
```

**Solution - Bundle Analysis**:

```bash
# Install bundle analyzer
npm install -D @nuxt/bundle-analysis

# Run analysis
npx nuxi analyze
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  experimental: {
    bundleAnalysis: true
  },
  routeRules: {
    '/admin/**': { prerender: false } // SSG pages
  }
})
```

### 6. Tránh Improper Error Boundaries

**Anti-Pattern Description**: Không có error handling thích hợp cho async operations và server routes, dẫn đến unhandled errors crashes app.

**Bad Pattern Examples**:

```typescript
// Bad Pattern 1: Không catch errors
<script setup lang="ts">
const fetchProducts = async () => {
  const { data } = await useFetch('/api/products')
  // Nếu API fail, không có error handling!
  return data
}
</script>

// Bad Pattern 2: Generic error handling
<script setup lang="ts">
try {
  await fetchData()
} catch (e) {
  console.log('Error') // Không có proper logging hoặc error reporting
}
</script>

// Bad Pattern 3: Không handle server errors
// server/api/users.get.ts
export default defineEventHandler(async () => {
  const users = await prisma.user.findMany()
  // Nếu database fail, error không được handle
  return users
})
</script>
```

**Solution - Proper Error Handling Pattern**:

```typescript
// composables/useAsyncDataWithError.ts
export const useAsyncDataWithError = <T>(
  key: string,
  handler: () => Promise<T>,
  options?: {
    defaultValue?: T
    onError?: (error: Error) => void
  }
) => {
  const data = ref<T | null>(options?.defaultValue ?? null) as Ref<T | null>
  const error = ref<Error | null>(null)
  const pending = ref(true)
  
  const fetch = async () => {
    try {
      pending.value = true
      data.value = await handler()
    } catch (e) {
      error.value = e instanceof Error ? e : new Error(String(e))
      options?.onError?.(error.value)
    } finally {
      pending.value = false
    }
  }
  
  onMounted(fetch)
  
  return { data, error, pending, refresh: fetch }
}
```

```vue
<script setup lang="ts">
const { data: products, error, pending, refresh } = await useAsyncData(
  'products',
  () => $fetch('/api/products'),
  {
    default: () => [],
    onError: (error) => {
      // Log to error tracking service
      console.error('Failed to fetch products:', error)
    }
  }
)

// Sử dụng error.value in template
</script>
```

**Solution - Server Error Handling**:

```typescript
// server/api/users.get.ts
export default defineEventHandler(async (event) => {
  try {
    const users = await prisma.user.findMany({
      take: 100
    })
    return users
  } catch (error) {
    // Log error
    console.error('Database error:', error)
    
    // Return proper error response
    throw createError({
      statusCode: 500,
      statusMessage: 'Internal Server Error',
      message: 'Failed to fetch users'
    })
  }
})
```

### 7. Tránh Improper SEO Implementation

**Anti-Pattern Description**: Không set meta tags hoặc set không đúng cách, ảnh hưởng đến SEO và social sharing.

**Bad Pattern Examples**:

```vue
<!-- Bad Pattern 1: Không có meta tags -->
<template>
  <div>
    <h1>My Page</h1>
  </div>
</template>

<!-- Bad Pattern 2: Hardcoded meta tags -->
<head>
  <title>My Website</title>
  <meta name="description" content="Static description">
</head>

<!-- Bad Pattern 3: Sử dụng document.title thay vì useHead -->
<script setup lang="ts">
onMounted(() => {
  document.title = 'My Page Title' // Không SSR-friendly
})
</script>
```

**Solution - useHead Composable**:

```vue
<script setup lang="ts">
// Sử dụng useHead cho every page
useHead({
  title: 'Product Name | My Website',
  meta: [
    { name: 'description', content: 'Product description here' },
    { property: 'og:title', content: 'Product Name' },
    { property: 'og:description', content: 'Product description' },
    { property: 'og:image', content: '/images/product.jpg' },
    { name: 'twitter:card', content: 'summary_large_image' }
  ],
  link: [
    { rel: 'canonical', href: 'https://example.com/product' }
  ]
})
</script>
```

**Solution - useSeoMeta Composable**:

```vue
<script setup lang="ts">
// Simplified API cho common SEO meta tags
useSeoMeta({
  title: 'Product Name',
  ogTitle: 'Product Name',
  description: 'Product description here',
  ogDescription: 'Product description for social sharing',
  ogImage: '/images/product.jpg',
  twitterCard: 'summary_large_image'
})
</script>
```

**Solution - useServerSeoMeta cho Server-specific SEO**:

```vue
<script setup lang="ts">
// Set SEO meta tags server-side only (không overwrite client)
useServerSeoMeta({
  robots: 'index, follow',
  'og:locale': 'vi_VN'
})
</script>
```

## Common Patterns

### Pattern 1: SSR-Safe Browser Detection

```typescript
// composables/useIsBrowser.ts
export const useIsBrowser = () => {
  const isBrowser = import.meta.client
  const isServer = import.meta.server
  
  return { isBrowser, isServer }
}

// composables/useLocalStorage.ts
export const useLocalStorage = <T>(key: string, defaultValue: T) => {
  const isBrowser = import.meta.client
  
  const storedValue = isBrowser 
    ? localStorage.getItem(key) 
    : null
  
  const data = ref<T>(
    storedValue ? JSON.parse(storedValue) : defaultValue
  )
  
  watch(data, (newValue) => {
    if (isBrowser) {
      localStorage.setItem(key, JSON.stringify(newValue))
    }
  }, { deep: true })
  
  return data
}
```

### Pattern 2: Async Middleware with Loading State

```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware(async (to, from) => {
  const { isAuthenticated, fetchUser } = useAuth()
  
  // Chỉ check ở server hoặc khi chưa có user data
  if (!isAuthenticated.value) {
    await fetchUser()
    
    if (!isAuthenticated.value) {
      return navigateTo('/login')
    }
  }
})
```

### Pattern 3: Hybrid Data Fetching

```typescript
// Sử dụng useAsyncData cho initial data (SSR)
// và watch để refetch khi cần
const { data: user } = await useAsyncData(
  'user',
  () => $fetch('/api/user'),
  {
    default: () => null,
    server: true, // Fetch ở server
    lazy: false // Đợi data trước khi render
  }
)

// Client-side: watch for manual refetch
const refreshUser = () => {
  refreshNuxtData('user')
}
```

### Pattern 4: Error Boundary Component

```vue
<!-- components/ErrorBoundary.vue -->
<template>
  <slot v-if="!hasError" />
  <div v-else class="error-boundary">
    <h2>Something went wrong</h2>
    <p>{{ errorMessage }}</p>
    <button @click="resetError">Try again</button>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  onError?: (error: Error) => void
}>()

const hasError = ref(false)
const errorMessage = ref('')

const errorHandler = (error: Error) => {
  hasError.value = true
  errorMessage.value = error.message
  props.onError?.(error)
}

onErrorCaptured((error) => {
  errorHandler(error)
  return false // Prevent error propagation
})

const resetError = () => {
  hasError.value = false
  errorMessage.value = ''
}
</script>
```

## Troubleshooting

### Common Issues và Solutions

#### Issue 1: "Hydration node mismatch"

**Symptoms**: Console error "Hydration node mismatch" xuất hiện khi page load.

**Diagnosis**: Sử dụng `vue-loader`'s hydration debugging:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  devtools: { enabled: true },
  vue: {
    config: {
      performance: true,
      compilerOptions: {
        // Enable hydration comments in dev
      }
    }
  }
})
```

**Common Causes**:
- Date/time values rendered differently
- Conditional rendering based on client-only state
- Random values in template
- Third-party scripts modifying DOM

**Solution**: Review template và loại bỏ any non-deterministic code từ server-rendered output.

#### Issue 2: "Window is not defined"

**Symptoms**: Server-side error "Window is not defined".

**Common Causes**:
- Direct access to `window` hoặc `document` ở module level
- Importing client-only libraries ở server

**Solution**:

```typescript
// Bad: Module-level window access
const width = window.innerWidth

// Good: Inside lifecycle hook
onMounted(() => {
  const width = window.innerWidth
})

// Good: Using import.meta for checking
if (import.meta.client) {
  const width = window.innerWidth
}

// Good: Lazy import client-only modules
const heavyLib = ref(null)
onMounted(async () => {
  const module = await import('heavy-lib')
  heavyLib.value = module.default
})
```

#### Issue 3: Stale Data After Navigation

**Symptoms**: Data không update khi navigate giữa các pages với cùng asyncData key.

**Solution**:

```typescript
// Use unique keys for different pages
const { data } = await useAsyncData(
  `product-${route.params.id}`, // Unique per product
  () => $fetch(`/api/products/${route.params.id}`)
)

// Or use watchQuery to refetch
definePageMeta({
  watchQuery: ['category']
})
```

#### Issue 4: Memory Leak from Event Listeners

**Symptoms**: Memory usage tăng liên tục khi sử dụng app.

**Solution**: Always cleanup trong `onUnmounted`:

```typescript
onUnmounted(() => {
  window.removeEventListener('resize', handler)
  clearInterval(intervalId)
  websocket?.close()
})
```

## Examples

### Complete Example: SSR-Safe Data Fetching

```typescript
// composables/useProduct.ts
export interface Product {
  id: string
  name: string
  price: number
  category: string
  image: string
  description: string
}

export const useProduct = (productId: MaybeRefOrGetter<string>) => {
  const id = toRef(productId)
  
  const { data: product, pending, error, refresh } = useAsyncData(
    () => `product-${unref(id)}`,
    () => $fetch(`/api/products/${unref(id)}`),
    {
      transform: (data: Product) => data,
      default: () => null as Product | null,
      server: true,
      lazy: false
    }
  )
  
  // SEO meta
  useHead({
    title: computed(() => product.value 
      ? `${product.value.name} | Shop` 
      : 'Loading...'
    ),
    meta: computed(() => ({
      description: product.value?.description ?? ''
    }))
  })
  
  return { product, pending, error, refresh }
}
```

```vue
<!-- pages/products/[id].vue -->
<template>
  <div>
    <div v-if="pending" class="loading">
      <LoadingSpinner />
    </div>
    
    <div v-else-if="error" class="error">
      <ErrorMessage :error="error" @retry="refresh" />
    </div>
    
    <div v-else-if="product" class="product">
      <ProductImage :src="product.image" :alt="product.name" />
      <h1>{{ product.name }}</h1>
      <p class="price">${{ product.price }}</p>
      <p class="description">{{ product.description }}</p>
      <AddToCartButton :product="product" />
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const { product, pending, error, refresh } = useProduct(
  () => route.params.id as string
)
</script>
```

### Complete Example: Error Handling Pattern

```typescript
// utils/api.ts
export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public code?: string
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export const handleApiError = (error: unknown): ApiError => {
  if (error instanceof ApiError) {
    return error
  }
  
  if (error instanceof Error) {
    return new ApiError(error.message, 500, 'UNKNOWN_ERROR')
  }
  
  return new ApiError('An unexpected error occurred', 500, 'UNKNOWN_ERROR')
}
```

```typescript
// server/api/protected-resource.get.ts
export default defineEventHandler(async (event) => {
  // Validate authentication
  const user = await getAuthenticatedUser(event)
  
  if (!user) {
    throw createError({
      statusCode: 401,
      statusMessage: 'Unauthorized',
      message: 'Authentication required'
    })
  }
  
  // Fetch resource
  const resource = await prisma.resource.findFirst({
    where: { userId: user.id }
  })
  
  if (!resource) {
    throw createError({
      statusCode: 404,
      statusMessage: 'Not Found',
      message: 'Resource not found'
    })
  }
  
  return resource
})
```

### Complete Example: Performance Optimization

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  // Optimize bundle
  modules: [
    '@nuxt/image',
    '@nuxtjs/google-fonts',
    '@pinia/nuxt'
  ],
  
  // Component lazy loading
  components: {
    dirs: [
      {
        path: '~/components',
        pattern: '**/Heavy*.vue',
        lazy: true // Auto-lazy-load heavy components
      },
      {
        path: '~/components'
      }
    ]
  },
  
  // Image optimization
  image: {
    quality: 80,
    format: ['webp', 'avif'],
    screens: {
      xs: 320,
      sm: 640,
      md: 768,
      lg: 1024,
      xl: 1280
    }
  },
  
  // Route rules for hybrid rendering
  routeRules: {
    '/': { prerender: true },
    '/blog/**': { prerender: true },
    '/api/**': { cors: true },
    '/admin/**': { ssr: false },
    '/dashboard/**': { swr: 3600 }
  },
  
  // Experimental features
  experimental: {
    payloadExtraction: true,
    renderJsonPayloads: true
  }
})
```

## References

### Official Documentation

- [Nuxt 3 Documentation](https://nuxt.com/docs)
- [Vue 3 Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [Nitro Server Engine](https://nitro.unjs.io/)

### Key Composables Reference

- `useFetch` - Wrapper around useAsyncData với built-in fetch
- `useAsyncData` - Fetch và cache data với SSR support
- `useState` - SSR-safe reactive state management
- `useHead` - Manage head tags (title, meta, links, scripts)
- `useSeoMeta` - Simplified SEO meta tags
- `useNuxtApp` - Access Nuxt app instance
- `useRoute` - Access current route
- `useRouter` - Access router instance

### Related Rules

- Xem `coding-standards.mdc` cho code style guidelines
- Xem `performance.mdc` cho performance optimization
- Xem `api.mdc` cho API design patterns
