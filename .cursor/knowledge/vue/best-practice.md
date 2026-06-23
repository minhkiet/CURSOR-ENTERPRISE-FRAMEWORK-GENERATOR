---
title: "Vue Best Practices - Thực Hành Tốt Nhất Vue.js"
description: "Hướng dẫn toàn diện về các best practices cho Vue.js development bao gồm Composition API, Pinia, component design, và performance optimization"
tags: ["vue", "javascript", "best-practices", "composition-api", "pinia", "frontend"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Vue Best Practices - Thực Hành Tốt Nhất Vue.js

## Tổng Quan

Tài liệu này cung cấp hướng dẫn chi tiết và toàn diện về các best practices trong Vue.js development. Được xây dựng dựa trên kinh nghiệm thực tế từ các dự án enterprise và feedback từ cộng đồng Vue, tài liệu này cover mọi aspect từ component design đến state management, từ TypeScript integration đến performance optimization.

Vue.js là một framework progressive được thiết kế để có thể adopt incrementally, nhưng khi ứng dụng scale up, việc tuân thủ các best practices trở nên quan trọng hơn bao giờ hết. Một ứng dụng Vue được viết tốt không chỉ hoạt động correct mà còn maintainable, testable, và scalable theo thời gian.

Tài liệu này phù hợp cho developers ở mọi level, từ beginners mới làm quen với Vue đến experienced developers muốn refine their skills và áp dụng enterprise-grade patterns vào projects của họ.

## Mục Đích

Mục đích của tài liệu best practices này là:

1. **Standardization**: Cung cấp một bộ tiêu chuẩn thống nhất cho Vue development trong team, giúp code review và collaboration hiệu quả hơn. Khi mọi developer trong team follow cùng conventions, code trở nên predictable và dễ đọc.

2. **Performance Optimization**: Hướng dẫn cách viết code Vue performant từ đầu, tránh những common pitfalls dẫn đến performance issues. Performance không phải là thứ nên được optimize sau khi code đã viết xong.

3. **Maintainability**: Các best practices được document ở đây hướng đến việc code dễ maintain, debug, và extend theo thời gian. Một codebase maintainable tốt giảm đáng kể technical debt và thời gian onboarding cho new developers.

4. **Type Safety**: Với TypeScript integration mạnh mẽ của Vue 3, tài liệu này hướng dẫn cách tận dụng tối đa type system để catch bugs sớm và improve developer experience.

## Key Concepts

### 1. Single-File Components (SFC) Best Practices

Single-File Components là format chuẩn cho Vue components, combining template, script, và styles trong một file. SFC provides excellent developer experience nhưng để tận dụng tối đa benefits, developers cần follow certain conventions.

**Script Setup Syntax**:

`<script setup>` là recommended syntax cho Vue 3 components vì nó cung cấp cleaner code, better TypeScript support, và improved performance với less boilerplate.

```vue
<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { PropType } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { formatDate } from '@/utils/formatters'

// Define types
interface User {
  id: number
  name: string
  email: string
  role: 'admin' | 'user' | 'guest'
}

// Props definition với full TypeScript support
const props = withDefaults(defineProps<{
  userId: number
  user: User
  showActions?: boolean
  variant?: 'compact' | 'expanded'
}>(), {
  showActions: true,
  variant: 'expanded'
})

// Emits definition
const emit = defineEmits<{
  select: [userId: number]
  delete: [userId: number]
  update: [user: Partial<User>]
}>()

// Store integration
const authStore = useAuthStore()

// Reactive state
const isLoading = ref(false)
const isEditing = ref(false)

// Computed properties
const isAdmin = computed(() => props.user.role === 'admin')
const canEdit = computed(() =>
  authStore.currentUser?.id === props.userId || isAdmin.value
)

// Methods
const handleSelect = () => emit('select', props.userId)
const handleDelete = () => emit('delete', props.userId)
const handleUpdate = (data: Partial<User>) => emit('update', data)
</script>
```

**Template Best Practices**:

```vue
<template>
  <!-- Use semantic HTML elements -->
  <article class="user-card" :class="{ 'user-card--compact': variant === 'compact' }">
    <header class="user-card__header">
      <img
        :src="user.avatar"
        :alt="`Avatar of ${user.name}`"
        class="user-card__avatar"
        loading="lazy"
      />
      <div class="user-card__info">
        <h3>{{ user.name }}</h3>
        <p class="user-card__email">{{ user.email }}</p>
      </div>
    </header>

    <!-- Conditional rendering -->
    <section v-if="variant === 'expanded'" class="user-card__details">
      <dl>
        <dt>Role</dt>
        <dd>{{ user.role }}</dd>
      </dl>
    </section>

    <!-- Actions slot -->
    <footer v-if="showActions && canEdit" class="user-card__actions">
      <slot name="actions" :user="user">
        <button @click="handleSelect">Select</button>
      </slot>
    </footer>
  </article>
</template>
```

**Style Best Practices**:

```vue
<style scoped lang="scss">
// Use CSS custom properties for theming
.user-card {
  --card-padding: 16px;
  --card-radius: 8px;
  --card-bg: var(--color-surface);
  --card-border: 1px solid var(--color-border);

  padding: var(--card-padding);
  border-radius: var(--card-radius);
  background: var(--card-bg);
  border: var(--card-border);

  // BEM-like naming
  &__header {
    display: flex;
    gap: 12px;
    align-items: center;
  }

  &__avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    object-fit: cover;
  }

  &__info {
    flex: 1;
  }

  &__details {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--color-border);
  }

  &__actions {
    margin-top: 12px;
    display: flex;
    gap: 8px;
    justify-content: flex-end;
  }

  // Variant modifiers
  &--compact {
    padding: 8px;

    .user-card__avatar {
      width: 32px;
      height: 32px;
    }
  }
}
</style>
```

### 2. Composition API Patterns

Composition API là heart của Vue 3, providing flexible way để organize logic trong components. Để tận dụng tối đa, developers nên follow certain patterns.

**Composable Organization**:

```typescript
// composables/useCounter.ts
import { ref, computed, type Ref } from 'vue'

export interface UseCounterOptions {
  min?: number
  max?: number
  step?: number
}

export function useCounter(initialValue = 0, options: UseCounterOptions = {}) {
  const { min = -Infinity, max = Infinity, step = 1 } = options

  const count = ref(initialValue)

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
    count.value = initialValue
  }

  const setValue = (value: number) => {
    count.value = Math.min(max, Math.max(min, value))
  }

  const isAtMin = computed(() => count.value <= min)
  const isAtMax = computed(() => count.value >= max)

  return {
    count: count as Readonly<Ref<number>>,
    increment,
    decrement,
    reset,
    setValue,
    isAtMin,
    isAtMax
  }
}
```

**Stateful Logic Reuse**:

```typescript
// composables/useAsync.ts
import { ref, shallowRef, isRef, watchEffect, type Ref } from 'vue'

export interface UseAsyncOptions<T> {
  immediate?: boolean
  onError?: (error: Error) => void
  onSuccess?: (data: T) => void
}

export function useAsync<T>(
  asyncFn: () => Promise<T>,
  options: UseAsyncOptions<T> = {}
) {
  const { immediate = true, onError, onSuccess } = options

  const data = shallowRef<T | null>(null)
  const error = shallowRef<Error | null>(null)
  const isLoading = ref(false)
  const isSuccess = ref(false)

  const execute = async (...args: unknown[]) => {
    isLoading.value = true
    error.value = null

    try {
      const result = await asyncFn(...args)
      data.value = result
      isSuccess.value = true
      onSuccess?.(result)
      return result
    } catch (e) {
      const err = e instanceof Error ? e : new Error('Unknown error')
      error.value = err
      isSuccess.value = false
      onError?.(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  if (immediate) {
    execute()
  }

  return {
    data: data as Readonly<Ref<T | null>>,
    error: error as Readonly<Ref<Error | null>>,
    isLoading: isLoading as Readonly<Ref<boolean>>,
    isSuccess: isSuccess as Readonly<Ref<boolean>>,
    execute
  }
}

// Usage
const fetchUsers = () => fetch('/api/users').then(r => r.json())
const { data: users, isLoading, error, execute: refreshUsers } = useAsync(fetchUsers)
```

### 3. Pinia State Management

Pinia là official state management library cho Vue 3, cung cấp intuitive API với full TypeScript support. Để maintain scalable state management, follow these patterns.

**Store Structure**:

```typescript
// stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, UserCredentials, UserProfile } from '@/types'

export const useUserStore = defineStore('user', () => {
  // State
  const profile = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isLoading = ref(false)
  const error = ref<Error | null>(null)

  // Getters (Computed)
  const isAuthenticated = computed(() => token.value !== null && profile.value !== null)
  const userRole = computed(() => profile.value?.role ?? 'guest')
  const userFullName = computed(() => {
    if (!profile.value) return ''
    return `${profile.value.firstName} ${profile.value.lastName}`
  })

  // Actions
  const login = async (credentials: UserCredentials): Promise<void> => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      })

      if (!response.ok) {
        throw new Error('Invalid credentials')
      }

      const data = await response.json()
      token.value = data.token
      profile.value = data.user
      localStorage.setItem('auth_token', data.token)
    } catch (e) {
      error.value = e instanceof Error ? e : new Error('Login failed')
      throw error.value
    } finally {
      isLoading.value = false
    }
  }

  const logout = (): void => {
    profile.value = null
    token.value = null
    localStorage.removeItem('auth_token')
  }

  const fetchProfile = async (): Promise<void> => {
    if (!token.value) return

    isLoading.value = true
    error.value = null

    try {
      const response = await fetch('/api/users/me', {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })

      if (!response.ok) {
        throw new Error('Failed to fetch profile')
      }

      profile.value = await response.json()
    } catch (e) {
      error.value = e instanceof Error ? e : new Error('Failed to fetch profile')
    } finally {
      isLoading.value = false
    }
  }

  const updateProfile = async (updates: Partial<UserProfile>): Promise<void> => {
    if (!token.value) throw new Error('Not authenticated')

    isLoading.value = true
    error.value = null

    try {
      const response = await fetch('/api/users/me', {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token.value}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updates)
      })

      if (!response.ok) {
        throw new Error('Failed to update profile')
      }

      profile.value = await response.json()
    } catch (e) {
      error.value = e instanceof Error ? e : new Error('Failed to update profile')
      throw error.value
    } finally {
      isLoading.value = false
    }
  }

  // Initialize from localStorage
  const initAuth = (): void => {
    const storedToken = localStorage.getItem('auth_token')
    if (storedToken) {
      token.value = storedToken
      fetchProfile()
    }
  }

  return {
    // State
    profile,
    token,
    isLoading,
    error,
    // Getters
    isAuthenticated,
    userRole,
    userFullName,
    // Actions
    login,
    logout,
    fetchProfile,
    updateProfile,
    initAuth
  }
})
```

**Store Composition Patterns**:

```typescript
// stores/cart.ts - Setup store với cart logic
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Product, CartItem } from '@/types'

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])

  // Computed getters
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
  const addItem = (product: Product, quantity = 1): void => {
    const existingItem = items.value.find(item => item.id === product.id)

    if (existingItem) {
      existingItem.quantity += quantity
    } else {
      items.value.push({
        ...product,
        quantity
      })
    }
  }

  const removeItem = (productId: number): void => {
    const index = items.value.findIndex(item => item.id === productId)
    if (index !== -1) {
      items.value.splice(index, 1)
    }
  }

  const updateQuantity = (productId: number, quantity: number): void => {
    const item = items.value.find(item => item.id === productId)
    if (item) {
      if (quantity <= 0) {
        removeItem(productId)
      } else {
        item.quantity = quantity
      }
    }
  }

  const clearCart = (): void => {
    items.value = []
  }

  return {
    items,
    itemCount,
    subtotal,
    tax,
    total,
    isEmpty,
    addItem,
    removeItem,
    updateQuantity,
    clearCart
  }
})
```

### 4. Vue Router Best Practices

Vue Router là essential cho SPAs, và proper setup là critical cho maintainability và performance.

**Route Definitions**:

```typescript
// router/index.ts
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Lazy load all routes
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/pages/HomePage.vue'),
    meta: { title: 'Home' }
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/pages/AboutPage.vue'),
    meta: { title: 'About Us' }
  },
  {
    path: '/products',
    name: 'products',
    component: () => import('@/pages/ProductsPage.vue'),
    meta: { title: 'Products' }
  },
  {
    path: '/products/:slug',
    name: 'product-detail',
    component: () => import('@/pages/ProductDetailPage.vue'),
    meta: { title: 'Product Details' }
  },
  {
    path: '/cart',
    name: 'cart',
    component: () => import('@/pages/CartPage.vue'),
    meta: { title: 'Shopping Cart' }
  },
  {
    path: '/checkout',
    name: 'checkout',
    component: () => import('@/pages/CheckoutPage.vue'),
    meta: { title: 'Checkout', requiresAuth: true }
  },
  {
    path: '/dashboard',
    component: () => import('@/layouts/DashboardLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'dashboard',
        component: () => import('@/pages/dashboard/DashboardPage.vue'),
        meta: { title: 'Dashboard' }
      },
      {
        path: 'orders',
        name: 'orders',
        component: () => import('@/pages/dashboard/OrdersPage.vue'),
        meta: { title: 'My Orders' }
      },
      {
        path: 'settings',
        name: 'settings',
        component: () => import('@/pages/dashboard/SettingsPage.vue'),
        meta: { title: 'Settings' }
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/LoginPage.vue'),
    meta: { guestOnly: true, title: 'Login' }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/pages/RegisterPage.vue'),
    meta: { guestOnly: true, title: 'Register' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/pages/NotFoundPage.vue'),
    meta: { title: 'Page Not Found' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else if (to.hash) {
      return { el: to.hash }
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Initialize auth if needed
  if (!authStore.isInitialized) {
    await authStore.initialize()
  }

  // Update document title
  document.title = to.meta.title
    ? `${to.meta.title} | My App`
    : 'My App'

  // Check authentication requirements
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  // Redirect authenticated users away from guest-only pages
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    next({ name: 'dashboard' })
    return
  }

  next()
})

export default router
```

**Route Types**:

```typescript
// types/router.ts
import type { RouteRecordRaw } from 'vue-router'

export interface RouteMeta {
  title?: string
  requiresAuth?: boolean
  guestOnly?: boolean
  layout?: 'default' | 'dashboard' | 'auth'
  breadcrumb?: BreadcrumbItem[]
  [key: string]: unknown
}

export interface BreadcrumbItem {
  label: string
  to?: string
  active?: boolean
}

// Extend RouteRecordRaw
declare module 'vue-router' {
  interface RouteMeta {
    title?: string
    requiresAuth?: boolean
    guestOnly?: boolean
  }
}
```

## Best Practices for Component Design

### 1. Props and Emits

**Type-Safe Props**:

```typescript
// Define prop types explicitly
interface Props {
  title: string
  count: number
  items: string[]
  user: User
  onClick: () => void
  callback: (value: string) => void
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
}

// Using defineProps with types
const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  items: () => [] // Default factory function for arrays
})

// With complex types
const props = defineProps({
  user: {
    type: Object as PropType<User>,
    required: true
  },
  items: {
    type: Array as PropType<string[]>,
    default: () => []
  },
  callback: {
    type: Function as PropType<(value: string) => void>,
    required: true
  }
})
```

**Type-Safe Emits**:

```typescript
// Using defineEmits with type syntax (recommended)
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'submit', data: FormData): void
  (e: 'cancel'): void
  (e: 'custom', payload: { id: number; action: string }): void
}>()

// Usage
emit('update:modelValue', 'new value')
emit('submit', { name: 'John', email: 'john@example.com' })
emit('custom', { id: 1, action: 'delete' })
```

### 2. Slots and Scoped Slots

**Named Slots Pattern**:

```vue
<!-- DataTable.vue -->
<script setup lang="ts">
defineProps<{
  data: any[]
  loading?: boolean
}>()

defineSlots<{
  default(): any
  header(): any
  'cell'({ row, column, value }: { row: any; column: string; value: any }): any
  actions({ row }: { row: any }): any
}>()
</script>

<template>
  <div class="data-table">
    <slot name="header" />

    <table>
      <thead>
        <tr>
          <slot name="thead" />
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in data" :key="row.id">
          <slot name="cell" :row="row" column="default" :value="row">
            {{ value }}
          </slot>
          <slot name="actions" :row="row" />
        </tr>
      </tbody>
    </table>
  </div>
</template>
```

**Usage**:

```vue
<DataTable :data="users" :loading="isLoading">
  <template #header>
    <h2>Users</h2>
  </template>

  <template #thead>
    <th>Name</th>
    <th>Email</th>
    <th>Actions</th>
  </template>

  <template #cell="{ row, column }">
    <td v-if="column === 'name'">{{ row.name }}</td>
    <td v-else-if="column === 'email'">{{ row.email }}</td>
  </template>

  <template #actions="{ row }">
    <td>
      <button @click="editUser(row)">Edit</button>
      <button @click="deleteUser(row)">Delete</button>
    </td>
  </template>
</DataTable>
```

### 3. Dependency Injection

**Provide/Inject Pattern**:

```typescript
// composables/useTheme.ts
import { inject, provide, readonly, type InjectionKey } from 'vue'

interface Theme {
  primaryColor: string
  secondaryColor: string
  darkMode: boolean
  toggleDarkMode: () => void
}

const themeKey: InjectionKey<Theme> = Symbol('theme')

export function provideTheme() {
  const primaryColor = ref('#007bff')
  const secondaryColor = ref('#6c757d')
  const darkMode = ref(false)

  const toggleDarkMode = () => {
    darkMode.value = !darkMode.value
  }

  const theme: Theme = {
    primaryColor: readonly(primaryColor) as string,
    secondaryColor: readonly(secondaryColor) as string,
    darkMode: readonly(darkMode) as boolean,
    toggleDarkMode
  }

  provide(themeKey, theme)

  return theme
}

export function useTheme(): Theme {
  const theme = inject(themeKey)
  if (!theme) {
    throw new Error('Theme not provided')
  }
  return theme
}
```

## Performance Optimization

### 1. Lazy Loading Components

```vue
<script setup lang="ts">
import { defineAsyncComponent } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ErrorBoundary from '@/components/ErrorBoundary.vue'

// Lazy load heavy components
const HeavyChart = defineAsyncComponent({
  loader: () => import('@/components/HeavyChart.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorBoundary,
  delay: 200,
  timeout: 3000
})

// With suspense-compatible setup
const AsyncModal = defineAsyncComponent(() =>
  import('@/components/Modal.vue')
)
</script>
```

### 2. Virtual Scrolling

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { useVirtualList } from '@vueuse/core'

const items = ref([...Array(10000).keys()].map(i => ({ id: i, text: `Item ${i}` })))

const {
  list,
  containerProps,
  wrapperProps
} = useVirtualList(items, {
  itemHeight: 50,
  overscan: 10
})
</script>

<template>
  <div v-bind="containerProps" class="virtual-list">
    <div v-bind="wrapperProps">
      <div v-for="{ data, index } in list" :key="data.id">
        {{ data.text }} - Index: {{ index }}
      </div>
    </div>
  </div>
</template>
```

### 3. Memoization and Caching

```typescript
// composables/useDebounce.ts
import { ref, watch } from 'vue'

export function useDebouncedRef<T>(initialValue: T, delay: number = 300) {
  const value = ref<T>(initialValue)
  const debouncedValue = ref<T>(initialValue)

  let timeout: ReturnType<typeof setTimeout>

  watch(value, (newValue) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      debouncedValue.value = newValue
    }, delay)
  })

  return { value, debouncedValue }
}

// composables/useMemo.ts
export function useMemo<T>(factory: () => T, deps: unknown[]): Readonly<Ref<T>> {
  const value = ref<T>() as Ref<T>
  let oldDeps: unknown[] | undefined

  const update = () => {
    if (!oldDeps || !depsEqual(deps, oldDeps)) {
      value.value = factory()
      oldDeps = deps
    }
  }

  update()

  return value as Readonly<Ref<T>>
}
```

## Security Best Practices

### 1. XSS Prevention

```typescript
// Never use v-html with user-provided content
// BAD
const userContent = '<script>alert("xss")</script>'
// <div v-html="userContent"></div>

// GOOD: Sanitize first
import DOMPurify from 'dompurify'

const sanitizedContent = computed(() =>
  DOMPurify.sanitize(userContent.value)
)

// Then use
// <div v-html="sanitizedContent"></div>

// For rich text, use a safe library like TipTap or Quill
```

### 2. Input Validation

```typescript
// composables/useFormValidation.ts
import { ref, computed, type Ref } from 'vue'

interface ValidationRule {
  validate: (value: unknown) => boolean
  message: string
}

export function useFormValidation<T extends Record<string, unknown>>(
  initialValues: T,
  rules: Record<keyof T, ValidationRule[]>
) {
  const values = ref(initialValues) as Ref<T>
  const errors = ref<Partial<Record<keyof T, string>>>({})

  const validate = (field?: keyof T): boolean => {
    if (field) {
      return validateField(field)
    }

    let isValid = true
    for (const key in rules) {
      if (!validateField(key)) {
        isValid = false
      }
    }
    return isValid
  }

  const validateField = (field: keyof T): boolean => {
    const fieldRules = rules[field]
    if (!fieldRules) return true

    for (const rule of fieldRules) {
      if (!rule.validate(values.value[field])) {
        errors.value[field] = rule.message
        return false
      }
    }

    errors.value[field] = undefined
    return true
  }

  const reset = () => {
    values.value = { ...initialValues }
    errors.value = {}
  }

  return {
    values,
    errors,
    validate,
    validateField,
    reset
  }
}

// Usage
const { values, errors, validate } = useFormValidation(
  { email: '', password: '' },
  {
    email: [
      { validate: v => !!v, message: 'Email is required' },
      { validate: v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v), message: 'Invalid email' }
    ],
    password: [
      { validate: v => v.length >= 8, message: 'Password must be at least 8 characters' }
    ]
  }
)
```

## Testing Best Practices

### 1. Component Testing

```typescript
// components/UserCard.spec.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import UserCard from './UserCard.vue'

describe('UserCard', () => {
  const mockUser = {
    id: 1,
    name: 'John Doe',
    email: 'john@example.com',
    role: 'admin'
  }

  it('renders user information correctly', () => {
    const wrapper = mount(UserCard, {
      props: {
        user: mockUser,
        showActions: true
      }
    })

    expect(wrapper.find('.user-card__name').text()).toBe('John Doe')
    expect(wrapper.find('.user-card__email').text()).toBe('john@example.com')
  })

  it('emits select event when clicked', async () => {
    const wrapper = mount(UserCard, {
      props: { user: mockUser }
    })

    await wrapper.find('button').trigger('click')

    expect(wrapper.emitted('select')?.[0]).toEqual([mockUser.id])
  })

  it('respects showActions prop', () => {
    const withActions = mount(UserCard, {
      props: { user: mockUser, showActions: true }
    })

    const withoutActions = mount(UserCard, {
      props: { user: mockUser, showActions: false }
    })

    expect(withActions.find('.user-card__actions').exists()).toBe(true)
    expect(withoutActions.find('.user-card__actions').exists()).toBe(false)
  })
})
```

### 2. Composables Testing

```typescript
// composables/useCounter.spec.ts
import { describe, it, expect } from 'vitest'
import { useCounter } from './useCounter'

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { count } = useCounter()
    expect(count.value).toBe(0)
  })

  it('accepts custom initial value', () => {
    const { count } = useCounter(10)
    expect(count.value).toBe(10)
  })

  it('respects min and max bounds', () => {
    const { count, increment, decrement, isAtMin, isAtMax } = useCounter(5, {
      min: 0,
      max: 10
    })

    // Test max boundary
    for (let i = 0; i < 10; i++) increment()
    expect(count.value).toBe(10)
    expect(isAtMax.value).toBe(true)

    // Test min boundary
    for (let i = 0; i < 20; i++) decrement()
    expect(count.value).toBe(0)
    expect(isAtMin.value).toBe(true)
  })

  it('resets to initial value', () => {
    const { count, increment, reset } = useCounter(0)
    increment()
    increment()
    expect(count.value).toBe(2)
    reset()
    expect(count.value).toBe(0)
  })
})
```

## Examples

### Complete Component Example

```vue
<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useNotifications } from '@/composables/useNotifications'

interface Props {
  taskId: number
}

const props = defineProps<Props>()

const emit = defineEmits<{
  complete: [taskId: number]
  delete: [taskId: number]
  update: [taskId: number, updates: Partial<Task>]
}>()

// Stores and composables
const authStore = useAuthStore()
const notifications = useNotifications()

// Local state
const isEditing = ref(false)
const editForm = ref({
  title: '',
  description: '',
  priority: 'medium' as 'low' | 'medium' | 'high',
  dueDate: ''
})

// Computed
const canEdit = computed(() =>
  authStore.currentUser?.id === props.task?.assigneeId ||
  authStore.hasPermission('tasks.edit')
)

// Watchers
watch(() => props.task, (newTask) => {
  if (newTask) {
    editForm.value = {
      title: newTask.title,
      description: newTask.description,
      priority: newTask.priority,
      dueDate: newTask.dueDate
    }
  }
}, { immediate: true })

// Methods
const startEditing = () => {
  editForm.value = {
    title: props.task?.title ?? '',
    description: props.task?.description ?? '',
    priority: props.task?.priority ?? 'medium',
    dueDate: props.task?.dueDate ?? ''
  }
  isEditing.value = true
}

const cancelEditing = () => {
  isEditing.value = false
}

const saveChanges = () => {
  emit('update', props.taskId, editForm.value)
  notifications.success('Task updated successfully')
  isEditing.value = false
}

const markComplete = () => {
  emit('complete', props.taskId)
  notifications.success('Task marked as complete')
}

const deleteTask = () => {
  if (confirm('Are you sure you want to delete this task?')) {
    emit('delete', props.taskId)
    notifications.success('Task deleted')
  }
}

// Lifecycle
onMounted(() => {
  // Load task data if needed
})
</script>

<template>
  <article class="task-card" :class="`task-card--${task?.priority}`">
    <header class="task-card__header">
      <h3 class="task-card__title">{{ task?.title }}</h3>
      <span class="task-card__priority">{{ task?.priority }}</span>
    </header>

    <p v-if="task?.description" class="task-card__description">
      {{ task?.description }}
    </p>

    <footer class="task-card__footer">
      <span v-if="task?.dueDate" class="task-card__due-date">
        Due: {{ formatDate(task.dueDate) }}
      </span>

      <div v-if="canEdit && !isEditing" class="task-card__actions">
        <button @click="startEditing">Edit</button>
        <button @click="markComplete">Complete</button>
        <button @click="deleteTask" class="danger">Delete</button>
      </div>
    </footer>

    <!-- Edit Form -->
    <form v-if="isEditing" class="task-card__edit-form" @submit.prevent="saveChanges">
      <label>
        Title
        <input v-model="editForm.title" type="text" required />
      </label>

      <label>
        Description
        <textarea v-model="editForm.description"></textarea>
      </label>

      <label>
        Priority
        <select v-model="editForm.priority">
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </label>

      <div class="form-actions">
        <button type="button" @click="cancelEditing">Cancel</button>
        <button type="submit">Save</button>
      </div>
    </form>
  </article>
</template>
```

## References

### Official Resources

- Vue 3 Documentation: https://vuejs.org/
- Vue Router Documentation: https://router.vuejs.org/
- Pinia Documentation: https://pinia.vuejs.org/
- Vue Test Utils: https://test-utils.vuejs.org/

### Recommended Tools

- Vite: Fast build tool (https://vitejs.dev/)
- Vitest: Unit testing framework (https://vitest.dev/)
- Volar: VS Code extension (https://marketplace.visualstudio.com/items?itemName=Vue.volar)
- Vue DevTools: Browser extension

### Further Learning

- Vue.js Design Patterns (O'Reilly)
- Building Vue 3 Applications (Packt)
- Vue School Courses (https://vueschool.io/)

## Kết Luận

Áp dụng các best practices trong tài liệu này sẽ giúp bạn xây dựng Vue applications chất lượng cao. Tuy nhiên, quan trọng cần nhớ:

1. **Consistency quan trọng hơn perfection** - một codebase consistent với một số imperfect patterns tốt hơn một codebase inconsistent với perfect patterns.

2. **Context matters** - không phải mọi pattern đều phù hợp cho mọi situation. Evaluate case by case.

3. **Iterate and improve** - không cần phải apply tất cả cùng lúc. Bắt đầu với những thay đổi có impact cao và iterate.

4. **Document your decisions** - khi deviate từ standard practices, document lý do để team members hiểu.

5. **Stay updated** - Vue ecosystem evolving rapidly. Theo dõi changelog và official recommendations.

Với commitment to quality và continuous improvement, bạn sẽ có thể xây dựng những Vue applications xuất sắc.
