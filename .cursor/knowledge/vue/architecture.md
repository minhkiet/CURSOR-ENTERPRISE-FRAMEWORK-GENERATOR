---
title: "Vue Architecture - Kiến Trúc Vue.js"
description: "Hướng dẫn toàn diện về kiến trúc ứng dụng Vue.js bao gồm component design, state management, routing, và performance patterns"
tags: ["vue", "javascript", "architecture", "component-design", "state-management", "performance"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Vue Architecture - Kiến Trúc Vue.js

## Tổng Quan

Tài liệu này trình bày các architectural patterns và best practices cho việc xây dựng scalable Vue.js applications. Được thiết kế cho enterprise-level applications, tài liệu cover mọi aspect từ high-level architecture decisions đến low-level implementation details.

Vue.js là một framework progressive được thiết kế để be incrementally adoptable, nhưng khi applications scale, việc có một solid architecture trở nên critical. Một tốt architecture không chỉ giúp code organization mà còn impact performance, maintainability, và team productivity.

Tài liệu này được viết cho developers đã có basic Vue knowledge và muốn understand cách structure Vue applications cho long-term success. Nó bao gồm practical guidance mà bạn có thể apply trực tiếp vào projects của mình.

## Mục Đích

Mục đích của tài liệu kiến trúc này là:

1. **Provide Architectural Guidance**: Cung cấp proven patterns cho structuring Vue applications. Architecture tốt giúp teams work efficiently và maintain code over time.

2. **Scale Properly**: Hướng dẫn cách architecture applications để scale từ small startups đến large enterprises. Điều quan trọng là design for growth từ đầu.

3. **Enable Team Collaboration**: Một good architecture enables multiple developers work on same codebase without stepping on each other's toes. Clear boundaries và conventions help.

4. **Support Long-Term Maintenance**: Applications need to be maintained và extended over years. Architecture decisions made early impact maintainability significantly.

## Key Concepts

### 1. Component-Based Architecture

Vue's component-based architecture là nền tảng cho mọi Vue application. Hiểu cách design components properly là essential cho building maintainable applications.

**Component Hierarchy**:

```
Application
├── Layouts/
│   ├── DefaultLayout
│   └── DashboardLayout
├── Pages/
│   ├── HomePage
│   └── UsersPage
│       └── UserCard
├── Shared/
│   ├── Button
│   ├── Modal
│   └── DataTable
└── Feature-specific/
    └── Cart/
        ├── CartSummary
        ├── CartItem
        └── CheckoutForm
```

**Component Classification**:

```typescript
// Classification by responsibility
type ComponentType =
  | 'layout'      // Page structure và shell
  | 'page'        // Route-level components
  | 'feature'     // Feature-specific components
  | 'shared'      // Reusable across features
  | 'primitive'   // Basic UI building blocks

// Example component classification
// src/components/layout/DashboardLayout.vue
// src/components/features/cart/CartItem.vue
// src/components/shared/BaseButton.vue
// src/components/shared/icons/IconHome.vue
```

### 2. State Management Patterns

State management trong Vue ranges từ simple local state đến complex global stores. Understanding khi nào sử dụng approach nào là key cho good architecture.

**State Scope Spectrum**:

```
Local State (Component) ← → Shared State (Composables) ← → Global State (Pinia)
     ↓                              ↓                              ↓
  useState()                   useCounter()                   useUserStore()
  - Props/Emits                 - useAuth()                   - Centralized
  - Template refs               - Shared within domain         - Cross-cutting
  - Single component            - Feature-specific            - Cross-domain
```

### 3. Layered Architecture

Vue applications nên follow layered architecture để separate concerns và improve maintainability.

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│    (Components, Pages, Layouts)         │
├─────────────────────────────────────────┤
│         Application Layer               │
│    (Composables, State Management)       │
├─────────────────────────────────────────┤
│         Service Layer                  │
│    (API clients, Business Logic)        │
├─────────────────────────────────────────┤
│          Data Layer                    │
│    (Types, Interfaces, Mappers)         │
└─────────────────────────────────────────┘
```

## Project Structure

### Recommended Directory Structure

```
src/
├── assets/                    # Static assets
│   ├── images/
│   ├── fonts/
│   └── styles/
│       ├── variables.scss
│       ├── mixins.scss
│       └── global.scss
├── components/                # Vue components
│   ├── common/               # Generic, reusable components
│   │   ├── BaseButton.vue
│   │   ├── BaseInput.vue
│   │   ├── BaseModal.vue
│   │   └── BaseCard.vue
│   ├── layout/               # Layout components
│   │   ├── AppHeader.vue
│   │   ├── AppSidebar.vue
│   │   └── AppFooter.vue
│   └── features/             # Feature-specific components
│       ├── auth/
│       │   ├── LoginForm.vue
│       │   └── RegisterForm.vue
│       └── dashboard/
│           ├── StatsCard.vue
│           └── ActivityFeed.vue
├── composables/               # Composition functions
│   ├── useAuth.ts
│   ├── useFetch.ts
│   ├── useForm.ts
│   └── useModal.ts
├── layouts/                   # Page layouts
│   ├── DefaultLayout.vue
│   ├── AuthLayout.vue
│   └── DashboardLayout.vue
├── pages/                     # Route pages
│   ├── index.vue
│   ├── about.vue
│   ├── login.vue
│   └── dashboard/
│       ├── index.vue
│       └── settings.vue
├── router/                    # Vue Router setup
│   ├── index.ts
│   ├── routes.ts
│   └── guards.ts
├── stores/                    # Pinia stores
│   ├── auth.ts
│   ├── cart.ts
│   └── products.ts
├── services/                   # API services
│   ├── api.ts                # Axios/Fetch setup
│   ├── auth.service.ts
│   ├── product.service.ts
│   └── user.service.ts
├── types/                     # TypeScript types
│   ├── api.ts
│   ├── user.ts
│   └── product.ts
├── utils/                     # Utility functions
│   ├── formatters.ts
│   ├── validators.ts
│   └── constants.ts
├── App.vue
├── main.ts
└── env.d.ts
```

### Alternative Structures

**Feature-Based Structure**:

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── composables/
│   │   ├── pages/
│   │   ├── stores/
│   │   └── types/
│   ├── products/
│   │   ├── components/
│   │   ├── composables/
│   │   ├── pages/
│   │   ├── stores/
│   │   └── types/
│   └── cart/
│       └── ...
├── shared/
│   ├── components/
│   ├── composables/
│   └── types/
└── app/
    ├── router/
    ├── layouts/
    └── main.ts
```

**Monorepo Structure** (cho very large applications):

```
packages/
├── shared/
│   ├── ui/                   # Shared UI components
│   ├── utils/                # Shared utilities
│   └── types/                # Shared TypeScript types
├── features/
│   ├── auth/
│   ├── products/
│   └── cart/
└── apps/
    ├── web/
    ├── admin/
    └── mobile/
```

## Component Design Patterns

### 1. Presentational vs Container Components

Separating presentational và container components là a well-established pattern giúp improve reusability và testability.

**Presentational Components** (Pure/View):
- Focus on how things look
- Receive data via props
- Emit events for actions
- No knowledge of Vuex/Pinia stores
- Mostly functional components

**Container Components** (Smart/Controller):
- Focus on how things work
- Connect to stores/data sources
- Pass data down to presentational
- Handle business logic
- Coordinate side effects

```vue
<!-- components/UserList.vue (Container) -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import UserCard from './UserCard.vue'
import UserListSkeleton from './UserListSkeleton.vue'

const userStore = useUserStore()
const isLoading = ref(true)

onMounted(async () => {
  await userStore.fetchUsers()
  isLoading.value = false
})

const handleUserSelect = (userId: number) => {
  // Business logic
}
</script>

<template>
  <div class="user-list">
    <UserListSkeleton v-if="isLoading" :count="6" />
    <template v-else>
      <UserCard
        v-for="user in userStore.users"
        :key="user.id"
        :user="user"
        @select="handleUserSelect"
      />
    </template>
  </div>
</template>
```

```vue
<!-- components/UserCard.vue (Presentational) -->
<script setup lang="ts">
interface Props {
  user: {
    id: number
    name: string
    email: string
    avatar?: string
  }
}

defineProps<Props>()

const emit = defineEmits<{
  select: [userId: number]
}>()
</script>

<template>
  <article class="user-card" @click="emit('select', user.id)">
    <img :src="user.avatar" :alt="user.name" />
    <h3>{{ user.name }}</h3>
    <p>{{ user.email }}</p>
  </article>
</template>
```

### 2. Compound Components Pattern

Compound components cung cấp a clean API cho complex UI elements với multiple related pieces.

```vue
<!-- components/Select.vue (Parent) -->
<script setup lang="ts">
import { ref, provide } from 'vue'

const isOpen = ref(false)
const selectedValue = ref<string | null>(null)

const toggle = () => {
  isOpen.value = !isOpen.value
}

const select = (value: string) => {
  selectedValue.value = value
  isOpen.value = false
}

provide('select', { isOpen, selectedValue, toggle, select })
</script>

<template>
  <div class="select">
    <slot :is-open="isOpen" :selected="selectedValue" />
  </div>
</template>
```

```vue
<!-- components/Select.vue - Usage -->
<Select>
  <template #default="{ isOpen, selected, toggle }">
    <button @click="toggle">
      {{ selected || 'Select an option' }}
    </button>

    <div v-if="isOpen" class="dropdown">
      <SelectOption value="a">Option A</SelectOption>
      <SelectOption value="b">Option B</SelectOption>
      <SelectOption value="c">Option C</SelectOption>
    </div>
  </template>
</Select>
```

### 3. Headless Components

Headless components cung cấp behavior không có styling, cho phép flexibility trong presentation.

```typescript
// composables/useDropdown.ts
import { ref, onMounted, onUnmounted } from 'vue'

export function useDropdown() {
  const isOpen = ref(false)
  const triggerRef = ref<HTMLElement | null>(null)
  const dropdownRef = ref<HTMLElement | null>(null)

  const toggle = () => {
    isOpen.value = !isOpen.value
  }

  const close = () => {
    isOpen.value = false
  }

  const handleClickOutside = (event: MouseEvent) => {
    if (
      !triggerRef.value?.contains(event.target as Node) &&
      !dropdownRef.value?.contains(event.target as Node)
    ) {
      close()
    }
  }

  onMounted(() => {
    document.addEventListener('click', handleClickOutside)
  })

  onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
  })

  return {
    isOpen,
    triggerRef,
    dropdownRef,
    toggle,
    close
  }
}
```

### 4. Renderless Components

Renderless components handle logic và data but don't render anything themselves, providing data to slots.

```vue
<!-- components/AccordionItem.vue -->
<script setup lang="ts">
import { ref, provide } from 'vue'

const props = defineProps<{
  title: string
  initiallyOpen?: boolean
}>()

const isOpen = ref(props.initiallyOpen ?? false)

const toggle = () => {
  isOpen.value = !isOpen.value
}

// Share state with parent Accordion
const accordionState = inject<{
  activeItems: Set<string>
  registerItem: (id: string, toggle: () => void) => void
}>('accordion')

provide('accordion', {
  isOpen,
  toggle
})

onMounted(() => {
  accordionState?.registerItem(props.title, toggle)
})
</script>

<template>
  <div class="accordion-item" :class="{ 'is-open': isOpen }">
    <button class="accordion-header" @click="toggle">
      {{ title }}
      <span class="icon">{{ isOpen ? '−' : '+' }}</span>
    </button>
    <div v-show="isOpen" class="accordion-content">
      <slot />
    </div>
  </div>
</template>
```

## State Management Architecture

### 1. Pinia Store Design

Pinia stores nên được organized theo domain chứ không phải theo store type.

```typescript
// stores/auth.ts - Authentication domain
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, AuthTokens } from '@/types'
import { authApi } from '@/services/auth.service'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const tokens = ref<AuthTokens | null>(null)
  const isLoading = ref(false)
  const error = ref<Error | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!tokens.value?.accessToken && !!user.value)
  const userRole = computed(() => user.value?.role ?? 'guest')
  const isAdmin = computed(() => user.value?.role === 'admin')

  // Actions
  const login = async (credentials: { email: string; password: string }) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await authApi.login(credentials)
      tokens.value = response.tokens
      user.value = response.user
      persistTokens()
    } catch (e) {
      error.value = e instanceof Error ? e : new Error('Login failed')
      throw error.value
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    user.value = null
    tokens.value = null
    clearPersistedTokens()
  }

  const refreshTokens = async () => {
    if (!tokens.value?.refreshToken) return

    try {
      const response = await authApi.refresh(tokens.value.refreshToken)
      tokens.value = response.tokens
      persistTokens()
    } catch (e) {
      logout()
      throw e
    }
  }

  // Persistence
  const persistTokens = () => {
    if (tokens.value) {
      localStorage.setItem('auth_tokens', JSON.stringify(tokens.value))
    }
  }

  const clearPersistedTokens = () => {
    localStorage.removeItem('auth_tokens')
  }

  const hydrateFromStorage = () => {
    const stored = localStorage.getItem('auth_tokens')
    if (stored) {
      tokens.value = JSON.parse(stored)
    }
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
    refreshTokens,
    hydrateFromStorage
  }
})
```

### 2. Store Communication

Stores nên communicate through actions chứ không truy cập trực tiếp vào state của nhau.

```typescript
// stores/cart.ts
export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])
  const authStore = useAuthStore() // Access other stores

  const addItem = async (product: Product) => {
    // If user is authenticated, sync with server
    if (authStore.isAuthenticated) {
      await cartApi.addItem(product.id)
    }

    // Update local state
    const existingItem = items.value.find(i => i.id === product.id)
    if (existingItem) {
      existingItem.quantity++
    } else {
      items.value.push({ ...product, quantity: 1 })
    }
  }

  return {
    items,
    addItem
  }
})
```

### 3. Composables for Shared Logic

Composables perfect cho reusable logic không cần global state.

```typescript
// composables/usePagination.ts
import { ref, computed, type Ref } from 'vue'

export interface UsePaginationOptions {
  page?: number
  pageSize?: number
  total?: Ref<number>
}

export function usePagination(initialOptions: UsePaginationOptions = {}) {
  const {
    page: initialPage = 1,
    pageSize: initialPageSize = 10,
    total
  } = initialOptions

  const currentPage = ref(initialPage)
  const pageSize = ref(initialPageSize)

  const totalItems = computed(() => total?.value ?? 0)
  const totalPages = computed(() =>
    Math.ceil(totalItems.value / pageSize.value)
  )

  const hasNextPage = computed(() =>
    currentPage.value < totalPages.value
  )

  const hasPreviousPage = computed(() =>
    currentPage.value > 1
  )

  const offset = computed(() =>
    (currentPage.value - 1) * pageSize.value
  )

  const goToPage = (page: number) => {
    const clampedPage = Math.max(1, Math.min(page, totalPages.value))
    currentPage.value = clampedPage
  }

  const nextPage = () => goToPage(currentPage.value + 1)
  const previousPage = () => goToPage(currentPage.value - 1)
  const firstPage = () => goToPage(1)
  const lastPage = () => goToPage(totalPages.value)

  return {
    currentPage,
    pageSize,
    totalItems,
    totalPages,
    hasNextPage,
    hasPreviousPage,
    offset,
    goToPage,
    nextPage,
    previousPage,
    firstPage,
    lastPage
  }
}
```

## Vue Router Architecture

### Route Organization

```typescript
// router/routes.ts
import type { RouteRecordRaw } from 'vue-router'

export interface RouteNames {
  home: 'home'
  about: 'about'
  login: 'login'
  register: 'register'
  dashboard: 'dashboard'
  dashboardOrders: 'dashboard-orders'
  dashboardSettings: 'dashboard-settings'
  productDetail: 'product-detail'
  cart: 'cart'
  checkout: 'checkout'
  notFound: 'not-found'
}

export const routeNames: RouteNames = {
  home: 'home',
  about: 'about',
  login: 'login',
  register: 'register',
  dashboard: 'dashboard',
  dashboardOrders: 'dashboard-orders',
  dashboardSettings: 'dashboard-settings',
  productDetail: 'product-detail',
  cart: 'cart',
  checkout: 'checkout',
  notFound: 'not-found'
}

export const routes: RouteRecordRaw[] = [
  // Public routes
  {
    path: '/',
    name: routeNames.home,
    component: () => import('@/pages/home/HomePage.vue'),
    meta: { title: 'Home', layout: 'default' }
  },
  {
    path: '/about',
    name: routeNames.about,
    component: () => import('@/pages/AboutPage.vue'),
    meta: { title: 'About Us', layout: 'default' }
  },
  {
    path: '/products/:slug',
    name: routeNames.productDetail,
    component: () => import('@/pages/ProductDetailPage.vue'),
    meta: { title: 'Product', layout: 'default' }
  },
  {
    path: '/cart',
    name: routeNames.cart,
    component: () => import('@/pages/CartPage.vue'),
    meta: { title: 'Shopping Cart', layout: 'default' }
  },

  // Auth routes
  {
    path: '/auth',
    component: () => import('@/layouts/AuthLayout.vue'),
    children: [
      {
        path: 'login',
        name: routeNames.login,
        component: () => import('@/pages/auth/LoginPage.vue'),
        meta: { title: 'Login' }
      },
      {
        path: 'register',
        name: routeNames.register,
        component: () => import('@/pages/auth/RegisterPage.vue'),
        meta: { title: 'Register' }
      }
    ]
  },

  // Protected routes
  {
    path: '/checkout',
    name: routeNames.checkout,
    component: () => import('@/pages/CheckoutPage.vue'),
    meta: {
      title: 'Checkout',
      layout: 'default',
      requiresAuth: true
    }
  },
  {
    path: '/dashboard',
    component: () => import('@/layouts/DashboardLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: routeNames.dashboard,
        component: () => import('@/pages/dashboard/DashboardPage.vue'),
        meta: { title: 'Dashboard' }
      },
      {
        path: 'orders',
        name: routeNames.dashboardOrders,
        component: () => import('@/pages/dashboard/OrdersPage.vue'),
        meta: { title: 'My Orders' }
      },
      {
        path: 'settings',
        name: routeNames.dashboardSettings,
        component: () => import('@/pages/dashboard/SettingsPage.vue'),
        meta: { title: 'Settings' }
      }
    ]
  },

  // Catch-all
  {
    path: '/:pathMatch(.*)*',
    name: routeNames.notFound,
    component: () => import('@/pages/NotFoundPage.vue'),
    meta: { title: 'Page Not Found', layout: 'default' }
  }
]
```

### Route Guards

```typescript
// router/guards.ts
import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notification'

export const authenticate = async (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
) => {
  const authStore = useAuthStore()
  const notificationStore = useNotificationStore()

  // Ensure auth state is initialized
  if (!authStore.isInitialized) {
    await authStore.initialize()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Store intended destination for redirect after login
    sessionStorage.setItem('redirectAfterLogin', to.fullPath)

    notificationStore.warning('Please log in to access this page')
    next({ name: 'login' })
    return
  }

  // Redirect authenticated users away from auth pages
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    next({ name: 'dashboard' })
    return
  }

  next()
}

export const updateDocumentTitle = (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
) => {
  const title = to.meta.title as string | undefined
  document.title = title ? `${title} | My App` : 'My App'
  next()
}

export const scrollToTop = (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
) => {
  window.scrollTo(0, 0)
  next()
}
```

### Route Views Pattern

```vue
<!-- layouts/DashboardLayout.vue -->
<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import AppHeader from '@/components/layout/AppHeader.vue'

const route = useRoute()

const showSidebar = computed(() =>
  route.meta.layout !== 'none'
)
</script>

<template>
  <div class="dashboard-layout">
    <AppSidebar v-if="showSidebar" />

    <div class="dashboard-content">
      <AppHeader />
      <main class="dashboard-main">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>
```

## Performance Patterns

### 1. Lazy Loading Strategy

```typescript
// Lazy load based on route
const routes = [
  {
    path: '/dashboard',
    component: () => import('./pages/Dashboard.vue') // Lazy loaded
  }
]

// Lazy load components
const HeavyChart = defineAsyncComponent({
  loader: () => import('./HeavyChart.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorFallback,
  delay: 200,
  timeout: 3000
})

// Lazy load based on visibility
import { vLazy } from '@/directives/lazy'

// vLazy directive
export const vLazy = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const loadImage = () => {
      el.setAttribute('src', binding.value)
    }

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          loadImage()
          observer.disconnect()
        }
      },
      { rootMargin: '50px' }
    )

    observer.observe(el)
  }
}
```

### 2. State Optimization

```typescript
// Use shallowRef for large objects
const largeData = shallowRef<BigDataSet>(initialData)

// Only update when necessary
const userList = ref<User[]>([])
const filteredUsers = computed(() =>
  searchQuery.value
    ? userList.value.filter(u => u.name.includes(searchQuery.value))
    : userList.value
)

// Debounce expensive operations
import { useDebounceFn } from '@vueuse/core'

const debouncedSearch = useDebounceFn(async (query: string) => {
  results.value = await searchAPI(query)
}, 300)
```

### 3. Render Optimization

```vue
<!-- Use v-memo for stable lists -->
<template>
  <div v-for="item in items" v-memo="[item.id, item.status]">
    <ExpensiveComponent :item="item" />
  </div>
</template>

<!-- Use keep-alive for cached components -->
<template>
  <router-view v-slot="{ Component }">
    <keep-alive :include="['UserList', 'ProductGrid']" :max="10">
      <component :is="Component" />
    </keep-alive>
  </router-view>
</template>

<!-- Use shallowMount in tests -->
import { shallowMount } from '@vue/test-utils'

shallowMount(Component) // Only mounts the component, not children
```

## Error Handling Architecture

### Global Error Handler

```typescript
// errors/handler.ts
import type { App } from 'vue'
import { useErrorStore } from '@/stores/error'

export interface ErrorContext {
  component: string
  props: Record<string, unknown>
  error: Error
  info: string
}

export function setupErrorHandler(app: App) {
  const errorStore = useErrorStore()

  app.config.errorHandler = (error: Error, instance, info) => {
    const context: ErrorContext = {
      component: instance?.$options?.name ?? 'Unknown',
      props: instance?.$props ?? {},
      error,
      info
    }

    // Log to error tracking service
    errorStore.captureException(error, context)

    // Log locally in development
    if (import.meta.env.DEV) {
      console.error('Vue Error:', error, info)
    }
  }

  app.config.warnHandler = (msg, instance, trace) => {
    if (import.meta.env.DEV) {
      console.warn('Vue Warning:', msg, trace)
    }
  }
}
```

### Error Boundary Component

```vue
<!-- components/ErrorBoundary.vue -->
<script setup lang="ts">
import { ref, onErrorCaptured } from 'vue'

const hasError = ref(false)
const errorMessage = ref('')

onErrorCaptured((error) => {
  hasError.value = true
  errorMessage.value = error.message
  return false // Prevent error from propagating
})
</script>

<template>
  <div v-if="hasError" class="error-boundary">
    <h2>Something went wrong</h2>
    <p>{{ errorMessage }}</p>
    <button @click="() => location.reload()">
      Reload Page
    </button>
  </div>
  <slot v-else />
</template>
```

## Testing Architecture

### Test Organization

```
tests/
├── unit/
│   ├── composables/
│   │   └── useCounter.spec.ts
│   ├── stores/
│   │   └── auth.spec.ts
│   └── utils/
│       └── formatters.spec.ts
├── component/
│   ├── common/
│   │   └── BaseButton.spec.ts
│   └── features/
│       └── CartItem.spec.ts
├── integration/
│   ├── auth/
│   │   └── login.spec.ts
│   └── checkout/
│       └── checkout.spec.ts
├── e2e/
│   ├── login.cy.ts
│   └── checkout.cy.ts
└── helpers/
    ├── setup.ts
    └── mocks.ts
```

### Component Testing Pattern

```typescript
// tests/component/common/BaseButton.spec.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseButton from '@/components/common/BaseButton.vue'

describe('BaseButton', () => {
  // Props testing
  describe('Props', () => {
    it('renders with default props', () => {
      const wrapper = mount(BaseButton)
      expect(wrapper.classes()).toContain('btn')
      expect(wrapper.attributes('type')).toBe('button')
    })

    it('applies variant classes', () => {
      const wrapper = mount(BaseButton, {
        props: { variant: 'primary' }
      })
      expect(wrapper.classes()).toContain('btn--primary')
    })

    it('applies size classes', () => {
      const wrapper = mount(BaseButton, {
        props: { size: 'large' }
      })
      expect(wrapper.classes()).toContain('btn--large')
    })

    it('disables button when loading', () => {
      const wrapper = mount(BaseButton, {
        props: { loading: true }
      })
      expect(wrapper.attributes('disabled')).toBe('')
    })
  })

  // Event testing
  describe('Events', () => {
    it('emits click event', async () => {
      const wrapper = mount(BaseButton)
      await wrapper.trigger('click')
      expect(wrapper.emitted('click')).toBeTruthy()
    })

    it('does not emit click when disabled', async () => {
      const wrapper = mount(BaseButton, {
        props: { disabled: true }
      })
      await wrapper.trigger('click')
      expect(wrapper.emitted('click')).toBeFalsy()
    })
  })

  // Slot testing
  describe('Slots', () => {
    it('renders default slot content', () => {
      const wrapper = mount(BaseButton, {
        slots: { default: 'Click me' }
      })
      expect(wrapper.text()).toBe('Click me')
    })
  })
})
```

## Examples

### Complete Feature Architecture

```typescript
// features/cart/types/index.ts
export interface CartItem {
  id: number
  productId: number
  name: string
  price: number
  quantity: number
  image: string
}

export interface Cart {
  items: CartItem[]
  subtotal: number
  tax: number
  total: number
}

export interface AddToCartRequest {
  productId: number
  quantity: number
}
```

```typescript
// features/cart/services/cart.service.ts
import { apiClient } from '@/services/api'
import type { AddToCartRequest, CartItem } from '../types'

export const cartApi = {
  async getCart(): Promise<CartItem[]> {
    const { data } = await apiClient.get('/cart')
    return data
  },

  async addItem(request: AddToCartRequest): Promise<CartItem> {
    const { data } = await apiClient.post('/cart/items', request)
    return data
  },

  async updateQuantity(itemId: number, quantity: number): Promise<void> {
    await apiClient.patch(`/cart/items/${itemId}`, { quantity })
  },

  async removeItem(itemId: number): Promise<void> {
    await apiClient.delete(`/cart/items/${itemId}`)
  }
}
```

```typescript
// features/cart/stores/cart.store.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { CartItem } from '../types'
import { cartApi } from '../services/cart.service'
import { useAuthStore } from '@/stores/auth'

export const useCartStore = defineStore('cart', () => {
  // State
  const items = ref<CartItem[]>([])
  const isLoading = ref(false)

  // Getters
  const itemCount = computed(() =>
    items.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  const subtotal = computed(() =>
    items.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
  )

  const tax = computed(() => subtotal.value * 0.1)
  const total = computed(() => subtotal.value + tax.value)
  const isEmpty = computed(() => items.value.length === 0)

  // Actions
  const fetchCart = async () => {
    isLoading.value = true
    try {
      items.value = await cartApi.getCart()
    } finally {
      isLoading.value = false
    }
  }

  const addItem = async (productId: number, quantity = 1) => {
    const existingItem = items.value.find(item => item.productId === productId)

    if (existingItem) {
      await updateQuantity(existingItem.id, existingItem.quantity + quantity)
    } else {
      const newItem = await cartApi.addItem({ productId, quantity })
      items.value.push(newItem)
    }
  }

  const updateQuantity = async (itemId: number, quantity: number) => {
    await cartApi.updateQuantity(itemId, quantity)
    const item = items.value.find(i => i.id === itemId)
    if (item) {
      item.quantity = quantity
    }
  }

  const removeItem = async (itemId: number) => {
    await cartApi.removeItem(itemId)
    const index = items.value.findIndex(i => i.id === itemId)
    if (index !== -1) {
      items.value.splice(index, 1)
    }
  }

  const clearCart = () => {
    items.value = []
  }

  return {
    // State
    items,
    isLoading,
    // Getters
    itemCount,
    subtotal,
    tax,
    total,
    isEmpty,
    // Actions
    fetchCart,
    addItem,
    updateQuantity,
    removeItem,
    clearCart
  }
})
```

```typescript
// features/cart/composables/useCart.ts
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useCartStore } from '@/stores/cart'

export function useCart() {
  const store = useCartStore()

  // Reactive refs
  const { items, isLoading, itemCount, subtotal, tax, total, isEmpty } =
    storeToRefs(store)

  // Actions
  const addItem = store.addItem
  const removeItem = store.removeItem
  const updateQuantity = store.updateQuantity
  const clearCart = store.clearCart

  return {
    // State
    items,
    isLoading,
    itemCount,
    subtotal,
    tax,
    total,
    isEmpty,
    // Actions
    addItem,
    removeItem,
    updateQuantity,
    clearCart
  }
}
```

## References

### Vue Official Documentation

- Vue 3 Core: https://vuejs.org/
- Vue Router: https://router.vuejs.org/
- Pinia: https://pinia.vuejs.org/
- Vue Test Utils: https://test-utils.vuejs.org/

### Performance Resources

- Vue Performance Guide: https://vuejs.org/guide/best-practices性能
- Web Vitals: https://web.dev/vitals/
- Lighthouse: https://developer.chrome.com/docs/lighthouse/

### Architecture Patterns

- Feature-Sliced Design: https://feature-sliced.design/
- Component Design Patterns: https://component-design-patterns.com/

### Testing

- Vitest: https://vitest.dev/
- Vue Testing Handbook: https://lmiller1990.github.io/vue-testing-handbook/
- Testing Library: https://testing-library.com/docs/vue-testing-library/intro/

## Kết Luận

Architecture cho Vue applications cần được think about carefully từ đầu project. Key takeaways từ tài liệu này:

1. **Start with Structure**: Chọn một project structure phù hợp với team size và project complexity. Structure tốt giúp maintainability.

2. **Separate Concerns**: Use layered architecture để separate presentation, application logic, và data access. Clean separation giúp testing và maintenance.

3. **Choose State Management Wisely**: Sử dụng local state cho component-specific data, composables cho reusable logic, và Pinia cho global state. Don't over-engineer.

4. **Design Components Thoughtfully**: Apply component patterns như presentational/container separation, compound components, và headless components where appropriate.

5. **Plan for Performance**: Think about performance từ đầu. Lazy loading, memoization, và proper reactivity handling prevent issues later.

6. **Test Architecture**: Xây dựng testability vào architecture từ đầu. Testable code thường là well-designed code.

7. **Document Decisions**: Document architectural decisions và rationale. Giúp future developers (bao gồm yourself) understand why things are the way they are.

Với solid architecture, Vue applications có thể scale effectively và remain maintainable over time.
