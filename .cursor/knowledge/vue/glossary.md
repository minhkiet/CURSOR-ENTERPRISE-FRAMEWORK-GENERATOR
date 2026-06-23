---
title: "Vue Glossary - Từ Điển Thuật Ngữ Vue.js"
description: "Từ điển toàn diện các thuật ngữ chuyên ngành Vue.js với giải thích chi tiết bằng tiếng Việt và tiếng Anh"
tags: ["vue", "javascript", "glossary", "terminology", "reference"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Vue Glossary - Từ Điển Thuật Ngữ Vue.js

## Tổng Quan

Tài liệu này cung cấp một từ điển toàn diện các thuật ngữ chuyên ngành được sử dụng trong Vue.js ecosystem. Mỗi thuật ngữ được định nghĩa chi tiết với ngữ cảnh sử dụng, ví dụ code, và cross-references đến các thuật ngữ liên quan.

Vue.js là một framework progressive với một hệ sinh thái phong phú, và việc hiểu đúng các thuật ngữ là nền tảng cho việc sử dụng hiệu quả. Từ điển này được thiết kế để serve như một reference guide cho cả beginners lẫn experienced developers.

Các thuật ngữ được tổ chức theo categories để dễ navigation. Cross-references được provided để help connect related concepts. Examples được provided trong TypeScript/Vue 3 syntax.

## Mục Đích

1. **Standardize Terminology**: Cung cấp consistent definitions cho Vue terminology trong team. Khi everyone shares common understanding, communication becomes clearer.

2. **Onboarding Support**: Giúp new team members quickly understand Vue terminology. Từ điển này có thể được sử dụng như reference during onboarding.

3. **Knowledge Reference**: Serve như quick reference khi encountering unfamiliar terms. Useful khi reading Vue documentation hoặc tutorials.

4. **Bilingual Support**: Cung cấp explanations trong cả tiếng Việt (cho khái niệm) và tiếng Anh (cho technical terms và code).

## A

### Abstract Syntax Tree (AST)

**Định nghĩa**: Một biểu diễn cấu trúc dữ liệu của code ở dạng tree structure, where mỗi node đại diện cho một construct trong source code như expressions, statements, hoặc declarations.

**Trong Vue Context**: Vue compiler chuyển đổi template strings thành AST trước khi tạo ra render functions hoặc JavaScript code. AST allows Vue's compiler thực hiện optimizations và transformations.

**Ví dụ**:

```typescript
// Template được parse thành AST
const template = '<div class="container">{{ message }}</div>'

// Vue compiler tạo ra AST structure
const ast = {
  type: 'Element',
  tag: 'div',
  props: [
    { type: 'Attribute', name: 'class', value: 'container' }
  ],
  children: [
    {
      type: 'Interpolation',
      content: { type: 'Expression', value: 'message' }
    }
  ]
}
```

**Xem thêm**: Template Compilation, Virtual DOM

### Async Component

**Định nghĩa**: Một component được loaded asynchronously khi cần thiết, thay vì bundle cùng với main application bundle. Async components giúp reduce initial bundle size và improve load time.

**Trong Vue Context**: Sử dụng `defineAsyncComponent` để define async components. Useful cho code splitting và lazy loading.

**Ví dụ**:

```typescript
import { defineAsyncComponent } from 'vue'

// Basic async component
const AsyncModal = defineAsyncComponent(() =>
  import('./components/Modal.vue')
)

// Với loading và error states
const AsyncDashboard = defineAsyncComponent({
  loader: () => import('./pages/Dashboard.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorFallback,
  delay: 200,
  timeout: 3000
})
```

**Xem thêm**: Code Splitting, Lazy Loading

## B

### Bootstrap

**Định nghĩa**: Quá trình khởi tạo và prepare một Vue application để chạy, bao gồm việc setup plugins, stores, và router.

**Trong Vue Context**: Thường xảy ra trong `main.ts` hoặc `main.js` file, nơi Vue app được created và mounted.

**Ví dụ**:

```typescript
// main.ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

const app = createApp(App)

// Bootstrap process
app.use(createPinia())
app.use(router)
app.mount('#app')
```

**Xem thêm**: Application Instance, Plugin

### Build Tool

**Định nghĩa**: Tool được sử dụng để bundle, compile, và transform Vue application code thành production-ready artifacts. Common build tools cho Vue bao gồm Vite, Webpack (thông qua Vue CLI), và Rollup.

**Trong Vue Context**: Build tools handle template compilation, TypeScript transpilation, CSS preprocessing, và asset optimization.

**Ví dụ**:

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  build: {
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia']
        }
      }
    }
  }
})
```

**Xem thêm**: Vite, Webpack, Vue CLI

## C

### Component (Thành Phần)

**Định nghĩa**: Khối xây dựng cơ bản trong Vue.js, là một self-contained unit của UI có thể tái sử dụng. Mỗi component encapsulates its own template, logic, và styles.

**Trong Vue Context**: Components có thể be nested để tạo thành component tree. Chúng communicate qua props, emits, slots, và dependency injection.

**Ví dụ**:

```vue
<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  title: string
  count?: number
}

const props = withDefaults(defineProps<Props>(), {
  count: 0
})

const emit = defineEmits<{
  update: [value: number]
}>()

const localCount = ref(props.count)

const increment = () => {
  localCount.value++
  emit('update', localCount.value)
}
</script>

<template>
  <div class="counter">
    <h2>{{ title }}</h2>
    <p>Count: {{ localCount }}</p>
    <button @click="increment">Increment</button>
  </div>
</template>

<style scoped>
.counter {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}
</style>
```

**Xem thêm**: Single-File Component, Component Instance

### Component Instance

**Định nghĩa**: Một runtime instance của một Vue component, được tạo ra khi component được rendered. Mỗi instance có its own reactive state, computed properties, watchers, và lifecycle hooks.

**Trong Vue Context**: Trong Vue 3 với Composition API, component instance được tự động tạo khi sử dụng `<script setup>`. Trong Options API, instance được tạo và các options được merged.

**Ví dụ**:

```typescript
// Accessing component instance
const MyComponent = {
  setup() {
    // In Composition API, this is automatic
    const message = ref('Hello')

    return { message }
  }
}

// Accessing via ref
const componentRef = ref<InstanceType<typeof MyComponent> | null>(null)

// Accessing via $refs (Options API)
const myComponent = this.$refs.myComponent as InstanceType<typeof MyComponent>
```

**Xem thêm**: Component, Reactive System

### Composition API

**Định nghĩa**: Một set của APIs cho phép developers organize component logic sử dụng imported functions thay vì options objects. Introduced trong Vue 3 như một alternative cho Options API.

**Trong Vue Context**: Composition API cung cấp better TypeScript support, better code reuse (through composables), và better organization cho complex components.

**Core Functions**:

```typescript
import {
  ref,           // Tạo reactive reference
  reactive,      // Tạo reactive object
  computed,      // Tạo computed property
  watch,         // Watch for changes
  watchEffect,   // Watch with immediate effect
  onMounted,     // Lifecycle hook
  onUnmounted,   // Lifecycle hook
  provide,       // Provide for descendants
  inject,        // Inject from ancestors
  defineProps,   // Define props
  defineEmits,   // Define emits
  defineExpose    // Expose public interface
} from 'vue'
```

**Ví dụ**:

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// Reactive state
const count = ref(0)
const user = reactive({ name: 'John', age: 30 })

// Computed
const doubled = computed(() => count.value * 2)

// Method
const increment = () => {
  count.value++
}

// Lifecycle
onMounted(() => {
  console.log('Component mounted')
})
</script>
```

**Xem thêm**: Options API, Composable, Reactivity System

### Computed Property

**Định nghĩa**: Một reactive property được derived tự động từ other reactive data. Computed properties are cached và chỉ re-evaluate khi dependencies thay đổi.

**Trong Vue Context**: Computed properties perfect cho derived state - data được calculate từ other state mà không cần manual synchronization.

**Ví dụ**:

```typescript
import { ref, computed } from 'vue'

const firstName = ref('John')
const lastName = ref('Doe')

// Computed property
const fullName = computed(() => {
  return `${firstName.value} ${lastName.value}`
})

// Computed với setter
const fullNameWithSetter = computed({
  get: () => `${firstName.value} ${lastName.value}`,
  set: (value: string) => {
    const [first, last] = value.split(' ')
    firstName.value = first
    lastName.value = last
  }
})
```

**Xem thêm**: Reactivity, Watcher, Getter

### Custom Directive

**Định nghĩa**: Một directive mà developers có thể register để perform custom DOM manipulation. Directives cung cấp a way để attach reusable behavior đến elements.

**Trong Vue Context**: Vue có một số built-in directives như `v-bind`, `v-model`, `v-if`. Custom directives cho phép extend Vue's template capabilities.

**Lifecycle Hooks**:

```typescript
const myDirective = {
  // Called before parent component mounted
  created(el, binding, vnode, prevVnode) {},

  // Called before element inserted into DOM
  beforeMount(el, binding, vnode, prevVnode) {},

  // Called when element is mounted
  mounted(el, binding, vnode, prevVnode) {},

  // Called before parent component updates
  beforeUpdate(el, binding, vnode, prevVnode) {},

  // Called when component updates
  updated(el, binding, vnode, prevVnode) {},

  // Called before parent component unmounts
  beforeUnmount(el, binding, vnode, prevVnode) {},

  // Called when element is unmounted
  unmounted(el, binding, vnode, prevVnode) {}
}
```

**Registration**:

```typescript
// Global
app.directive('focus', myDirective)

// Local
const vFocus = {
  mounted: (el) => el.focus()
}
```

**Xem thêm**: Directive, Built-in Directive

## D

### Dependency Injection

**Định nghĩa**: Một pattern trong đó một component provides data hoặc services mà descendants có thể consume without explicit passing qua props chain. Vue implement this qua provide/inject.

**Trong Vue Context**: Useful cho passing data through deep component trees mà không cần prop drilling. Common use cases bao gồm theme configuration, authentication state, và feature flags.

**Ví dụ**:

```typescript
// Provider (ancestor component)
import { provide, ref } from 'vue'

const theme = ref('light')

provide('theme', {
  current: theme,
  toggleTheme: () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
  }
})

// Consumer (descendant component)
import { inject } from 'vue'

const theme = inject('theme')

// With default value và type safety
interface ThemeContext {
  current: Ref<string>
  toggleTheme: () => void
}

const theme = inject<ThemeContext>('theme', {
  current: ref('light'),
  toggleTheme: () => {}
})
```

**Xem thêm**: Provide/Inject, Prop Drilling

### Directive (Chỉ Thị)

**Định nghĩa**: Special attributes prefixed với `v-` cung cấp declarative binding giữa data và DOM. Directives có thể perform DOM manipulation, handle events, hoặc apply conditional rendering.

**Trong Vue Context**: Built-in directives bao gồm `v-if`, `v-for`, `v-bind`, `v-on`, `v-model`, `v-show`, `v-slot`, `v-cloak`, `v-once`, và `v-memo`.

**Ví dụ**:

```vue
<template>
  <!-- v-bind - one-way binding -->
  <img v-bind:src="imageUrl" :alt="description" />

  <!-- v-on - event binding -->
  <button v-on:click="handleClick" @keyup.enter="handleEnter">
    Click me
  </button>

  <!-- v-model - two-way binding -->
  <input v-model="searchQuery" />

  <!-- v-if/v-else - conditional -->
  <div v-if="isLoggedIn">Welcome</div>
  <div v-else>Please login</div>

  <!-- v-for - list rendering -->
  <li v-for="item in items" :key="item.id">{{ item.name }}</li>

  <!-- v-show - visibility toggle -->
  <div v-show="isVisible">Content</div>
</template>
```

**Xem thêm**: Built-in Directive, Custom Directive

### Dynamic Component

**Định nghĩa**: Một component được resolved dynamically dựa trên runtime data, sử dụng `<component :is="...">` syntax. Cho phép switch between different components without changing the route.

**Trong Vue Context**: Useful cho tabbed interfaces, component switching based on user input, và dynamic layouts.

**Ví dụ**:

```vue
<script setup lang="ts">
import { ref, shallowRef } from 'vue'
import HomeTab from './tabs/HomeTab.vue'
import ProfileTab from './tabs/ProfileTab.vue'
import SettingsTab from './tabs/SettingsTab.vue'

const activeTab = ref('home')
const tabs = {
  home: HomeTab,
  profile: ProfileTab,
  settings: SettingsTab
}
</script>

<template>
  <div class="tab-container">
    <button
      v-for="(_, key) in tabs"
      :key="key"
      :class="{ active: activeTab === key }"
      @click="activeTab = key as string"
    >
      {{ key }}
    </button>

    <component :is="tabs[activeTab]" />
  </div>
</template>
```

**Xem thêm**: Component, Async Component

## E

### Effect

**Định nghĩa**: Một function chạy side effects dựa trên reactive state changes. Effects are automatically tracked và re-run khi dependencies thay đổi.

**Trong Vue Context**: Vue's reactivity system automatically tracks effects như watchers, computed properties, và template rendering. `watchEffect` là một explicit effect that immediately runs và tracks dependencies.

**Ví dụ**:

```typescript
import { ref, watchEffect } from 'vue'

const count = ref(0)

// This effect runs immediately và re-runs when count changes
watchEffect(() => {
  console.log(`Count changed to: ${count.value}`)

  // Effect automatically tracks count.value
  document.title = `Count: ${count.value}`
})

// Effect with cleanup
watchEffect((onCleanup) => {
  const timer = setInterval(() => {
    count.value++
  }, 1000)

  onCleanup(() => {
    clearInterval(timer)
  })
})
```

**Xem thêm**: Reactivity System, Watcher, Computed

### Error Boundary

**Định nghĩa**: Một component được wrap around other components để catch và handle JavaScript errors trong child components. Khi một error được caught, error boundary displays a fallback UI thay vì crashing the entire app.

**Trong Vue Context**: Vue 3 cung cấp `onErrorCaptured` hook để capture errors từ child components. Error boundaries giúp prevent partial failures từ crashing the whole application.

**Ví dụ**:

```vue
<script setup lang="ts">
import { ref, onErrorCaptured } from 'vue'

const hasError = ref(false)
const errorMessage = ref('')

onErrorCaptured((error, instance, info) => {
  hasError.value = true
  errorMessage.value = error.message

  // Log error for debugging
  console.error('Captured error:', error, info)

  // Return false to prevent error from propagating
  return false
})

const resetError = () => {
  hasError.value = false
  errorMessage.value = ''
}
</script>

<template>
  <div v-if="hasError" class="error-boundary">
    <h2>Something went wrong</h2>
    <p>{{ errorMessage }}</p>
    <button @click="resetError">Try Again</button>
  </div>
  <slot v-else />
</template>
```

**Xem thêm**: Error Handling, onErrorCaptured

### Event Handling

**Định nghĩa**: Xử lý user interactions và system events trong Vue components. Events được handle thông qua `v-on` directive hoặc `@` shorthand.

**Trong Vue Context**: Vue cung cấp unified interface cho handling all types of events, bao gồm native DOM events, custom component events, và system events.

**Ví dụ**:

```vue
<script setup lang="ts">
import { ref } from 'vue'

const handleClick = (event: MouseEvent) => {
  console.log('Clicked at:', event.clientX, event.clientY)
}

const handleSubmit = (event: Event) => {
  event.preventDefault()
  // Handle form submission
}

const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    submitForm()
  }
}

// Event modifiers
const handleClickOnce = () => {
  console.log('Will only log once per click')
}

// Keyboard modifiers
const handleCtrlClick = (event: KeyboardEvent) => {
  if (event.ctrlKey && event.key === 's') {
    event.preventDefault()
    save()
  }
}
</script>

<template>
  <button @click="handleClick">Click</button>
  <form @submit.prevent="handleSubmit">...</form>
  <input @keydown.enter="handleKeydown" />
  <button @click.once="handleClickOnce">Once</button>
  <div @click.ctrl="handleCtrlClick">Ctrl + Click</div>
</template>
```

**Xem thêm**: v-on, Event Modifiers

## F

### Fragment

**Định nghĩa**: Một virtual node không có root element, cho phép component return multiple elements without wrapping them in a container. Fragments giúp avoid unnecessary DOM nodes.

**Trong Vue Context**: Vue 3 components có thể return multiple root elements (fragment). `<template>` tags without a root element are also fragments.

**Ví dụ**:

```vue
<script setup lang="ts">
// Component with fragment - multiple root elements
</script>

<template>
  <!-- Fragment - no wrapper element -->
  <header>Header</header>
  <main>Content</main>
  <footer>Footer</footer>
</template>

<!-- Or using template with multiple roots -->
<template>
  <td>Cell 1</td>
  <td>Cell 2</td>
  <td>Cell 3</td>
</template>
```

**Xem thêm**: Virtual DOM, Template

### Functional Component

**Định nghĩa**: Một component được defined như một function thay vì an options object. Functional components are stateless (no reactive data) và instances (no instance created).

**Trong Vue Context**: Functional components were common trong Vue 2 cho performance optimization. Trong Vue 3, `shallowRef` và `v-memo` provide better alternatives.

**Ví dụ**:

```typescript
// Vue 3 functional component
import { h, defineComponent } from 'vue'

const FunctionalTitle = (props, { slots, attrs, emit }) => {
  return h(
    'h1',
    {
      class: ['title', attrs.class],
      style: { color: props.color }
    },
    slots.default?.()
  )
}

// With defineComponent
const MyFunctional = defineComponent({
  functional: true,
  props: {
    level: { type: Number, default: 1 }
  },
  render(props, { slots }) {
    return h(`h${props.level}`, slots.default?.())
  }
})
```

**Xem thêm**: Component, Stateful Component

## G

### Getter

**Định nghĩa**: Một function that retrieves computed data từ store state. Getters are like computed properties cho state management stores.

**Trong Vue Context**: Trong Pinia, getters được defined as computed properties inside store definition. Chúng cache results và re-compute when dependencies change.

**Ví dụ**:

```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useProductStore = defineStore('products', () => {
  const products = ref<Product[]>([])

  // Getter - computed from state
  const totalProducts = computed(() => products.value.length)

  const expensiveProducts = computed(() =>
    products.value.filter(p => p.price > 100)
  )

  const productsByCategory = computed(() => {
    return products.value.reduce((acc, product) => {
      if (!acc[product.category]) {
        acc[product.category] = []
      }
      acc[product.category].push(product)
      return acc
    }, {} as Record<string, Product[]>)
  })

  // Getter với parameter (factory pattern)
  const getProductById = (id: number) => {
    return computed(() => products.value.find(p => p.id === id))
  }

  return {
    products,
    totalProducts,
    expensiveProducts,
    productsByCategory,
    getProductById
  }
})
```

**Xem thêm**: Computed Property, Store, Pinia

### Global State

**Định nghĩa**: State được accessible từ bất kỳ đâu trong application, contrast với local state chỉ accessible trong một component. Global state thường được managed bằng state management library.

**Trong Vue Context**: Pinia là recommended global state management solution cho Vue 3. Global state phù hợp cho data cần được share across multiple components.

**Ví dụ**:

```typescript
// stores/theme.ts - Global state
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(false)

  const theme = computed(() => isDark.value ? 'dark' : 'light')

  const toggleTheme = () => {
    isDark.value = !isDark.value
    document.documentElement.classList.toggle('dark', isDark.value)
  }

  return { isDark, theme, toggleTheme }
})

// Any component có thể access
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()
// themeStore.isDark, themeStore.toggleTheme()
```

**Xem thêm**: Local State, Pinia, State Management

## H

### HMR (Hot Module Replacement)

**Định nghĩa**: Một development feature cho phép update modules trong browser without full page reload. HMR preserves application state trong khi applying updates.

**Trong Vue Context**: Vue CLI và Vite both support HMR, cho phép developers see changes immediately while maintaining component state.

**Ví dụ**:

```typescript
// vite.config.ts - HMR configuration
import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    hmr: {
      overlay: true, // Show errors in overlay
      clientPort: 5173
    }
  }
})

// Manual HMR handling
if (import.meta.hot) {
  import.meta.hot.accept(() => {
    // Custom HMR logic
  })

  import.meta.hot.dispose(() => {
    // Cleanup before reload
  })
}
```

**Xem thêm**: Vite, Development Mode

###Hydration

**Định nghĩa**: Quá trình attach Vue's reactivity system đến server-rendered HTML, tạo ra một fully functional Vue application từ static HTML.

**Trong Vue Context**: Trong Server-Side Rendering (SSR), Vue renders components trên server thành HTML string. Hydration sau đó makes those components interactive on client side.

**Ví dụ**:

```typescript
// server.ts - Server rendering
import { renderToString } from 'vue/server-renderer'
import { createApp } from './app'

export async function render(url: string) {
  const app = createApp()
  const router = app.use(router)

  await router.push(url)
  await router.isReady()

  const html = await renderToString(app)
  return html
}

// client.ts - Hydration
import { createApp } from 'vue'
import { createSSRApp } from 'vue'

createSSRApp(App).mount('#app') // Hydrates existing HTML
```

**Xem thêm**: SSR, CSR, Virtual DOM

## I

### Injection

**Định nghĩa**: Nhận data hoặc services được provided bởi ancestor components thông qua dependency injection system.

**Trong Vue Context**: `inject()` được sử dụng trong child components để receive values được provided by ancestors through `provide()`.

**Ví dụ**:

```typescript
import { inject, ref, type InjectionKey } from 'vue'

// Define type for injection
interface UserContext {
  user: { name: string; email: string }
  isAdmin: boolean
}

// Create injection key
const UserContextKey: InjectionKey<UserContext> = Symbol('user')

// In ancestor component
const userContext = computed<UserContext>(() => ({
  user: { name: 'John', email: 'john@example.com' },
  isAdmin: true
}))

provide(UserContextKey, userContext)

// In descendant component
const context = inject(UserContextKey)

if (context) {
  console.log(context.value.user.name)
}
```

**Xem thêm**: Provide, Dependency Injection

## K

### keep-alive

**Định nghĩa**: Một built-in component caching inactive component instances thay vì destroying them. Cached components preserve their state và can be quickly switched back.

**Trong Vue Context**: Useful cho preserving state across route changes, tab interfaces, và any scenario where component switching needs to be fast và state-preserving.

**Ví dụ**:

```vue
<template>
  <!-- Basic usage -->
  <keep-alive>
    <component :is="currentComponent" />
  </keep-alive>

  <!-- With include/exclude -->
  <keep-alive include="UserList,ProductGrid" exclude="AdminPanel">
    <router-view />
  </keep-alive>

  <!-- With max cache -->
  <keep-alive :max="10">
    <component :is="activeComponent" />
  </keep-alive>
</template>

<script setup lang="ts">
// Lifecycle hooks behavior with keep-alive
import { onActivated, onDeactivated } from 'vue'

// Called when component is mounted to cache
onActivated(() => {
  console.log('Component activated')
})

// Called when component is removed from cache
onDeactivated(() => {
  console.log('Component deactivated')
})
</script>
```

**Xem thêm**: Component Caching, Virtual DOM

## L

### Lifecycle Hook

**Định nghĩa**: Functions được called at specific points in component's lifecycle. Lifecycle hooks cho phép developers execute code at appropriate times, như after mount hoặc before unmount.

**Trong Vue Context**: Vue provides multiple lifecycle hooks từ creation đến unmounting.

**Lifecycle Diagram**:

```
Creation
  ├─ beforeCreate
  └─ created

Mounting
  ├─ beforeMount
  └─ mounted

Updating
  ├─ beforeUpdate
  └─ updated

Unmounting
  ├─ beforeUnmount
  └─ unmounted

Error Handling
  └─ errorCaptured
```

**Ví dụ**:

```typescript
import {
  onBeforeCreate,
  onCreated,
  onBeforeMount,
  onMounted,
  onBeforeUpdate,
  onUpdated,
  onBeforeUnmount,
  onUnmounted,
  onErrorCaptured
} from 'vue'

// In <script setup>
onMounted(() => {
  // DOM is ready
  const el = document.querySelector('.my-element')
})

onBeforeUnmount(() => {
  // Cleanup before component is destroyed
  window.removeEventListener('resize', handleResize)
})

onErrorCaptured((error) => {
  // Handle errors from child components
  console.error('Captured error:', error)
  return false // Prevent propagation
})
```

**Xem thêm**: Component Lifecycle, Setup

### Local State

**Định nghĩa**: State chỉ tồn tại trong một component và không được share với other parts of application. Local state được created với `ref()` hoặc `reactive()` trong component's setup.

**Trong Vue Context**: Most component state nên be local. Global state chỉ nên được used khi data thực sự cần shared across components.

**Ví dụ**:

```vue
<script setup lang="ts">
import { ref, reactive } from 'vue'

// Local primitive state
const count = ref(0)
const message = ref('Hello')

// Local object state
const form = reactive({
  email: '',
  password: '',
  rememberMe: false
})

// Local array state
const items = ref<string[]>([])
</script>
```

**Xem thêm**: Global State, Reactive, Ref

## M

### Mixin

**Định nghĩa**: Một pattern cho reusing code across multiple components. Mixins chứa options that được merged vào component's options.

**Trong Vue Context**: Mixins were popular trong Vue 2 nhưng đã được superseded by Composables trong Vue 3 cho most use cases. Mixins still work và có thể useful trong một số scenarios.

**Ví dụ**:

```typescript
// mixins/formatter.ts
export const formatterMixin = {
  methods: {
    formatDate(date: Date): string {
      return new Intl.DateTimeFormat('en-US').format(date)
    },
    formatCurrency(amount: number): string {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount)
    }
  }
}

// Using in component
import { formatterMixin } from '@/mixins/formatter'

export default {
  mixins: [formatterMixin],
  mounted() {
    console.log(this.formatCurrency(100)) // $100.00
  }
}
```

**Xem thêm**: Composable, Code Reuse

### Mutation

**Định nghĩa**: Thay đổi state trong reactive system. Mutations trigger reactivity và cause dependent computations và DOM updates.

**Trong Vue Context**: Trong Vuex (Vue 2), mutations are synchronous operations that modify state. Trong Pinia (Vue 3), mutations xảy ra implicitly when modifying reactive state.

**Ví dụ**:

```typescript
// Vuex mutation (Vue 2)
const store = createStore({
  state: {
    count: 0
  },
  mutations: {
    increment(state) {
      state.count++ // Mutation
    },
    setCount(state, payload) {
      state.count = payload // Mutation
    }
  }
})

// Pinia mutation (Vue 3) - just modifying state
const useCounterStore = defineStore('counter', {
  state: () => ({ count: 0 }),
  actions: {
    increment() {
      this.count++ // Direct mutation
    }
  }
})
```

**Xem thêm**: Reactivity System, State Management

## N

### nextTick

**Định nghĩa**: Một utility cho scheduling a callback để be executed after the next DOM update cycle. Useful khi bạn cần access updated DOM after changing reactive data.

**Trong Vue Context**: Khi reactive data changes, Vue batches updates và schedules DOM updates asynchronously. `nextTick` ensures your callback runs after these updates are complete.

**Ví dụ**:

```typescript
import { ref, nextTick } from 'vue'

const message = ref('Hello')
const messageRef = ref<HTMLElement | null>(null)

const updateMessage = async () => {
  message.value = 'Updated message'

  // DOM not updated yet here
  console.log(messageRef.value?.textContent) // 'Hello'

  await nextTick()

  // DOM updated now
  console.log(messageRef.value?.textContent) // 'Updated message'
}

// Alternative callback syntax
nextTick(() => {
  console.log('DOM is now updated')
})
```

**Xem thêm**: Reactivity, Async Updates

### Nuxt

**Định nghĩa**: Một meta-framework built on top of Vue.js cung cấp server-side rendering, static site generation, và nhiều features cho building production-ready Vue applications.

**Trong Vue Context**: Nuxt simplifies Vue development bằng automatic routing, file-based structure, server-side rendering, và built-in best practices.

**Ví dụ**:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@pinia/nuxt', '@nuxtjs/tailwindcss'],

  app: {
    head: {
      title: 'My Nuxt App',
      meta: [
        { name: 'description', content: 'My Nuxt App' }
      ]
    }
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE
    }
  }
})

// pages/index.vue
<script setup lang="ts">
const { data: users } = await useFetch('/api/users')

useHead({
  title: 'Home Page',
  style: []
})
</script>

<template>
  <div>
    <h1>Users</h1>
    <ul>
      <li v-for="user in users" :key="user.id">
        {{ user.name }}
      </li>
    </ul>
  </div>
</template>
```

**Xem thêm**: SSR, SSG, Vue.js

## O

### Options API

**Định nghĩa**: Traditional way để define Vue components sử dụng an options object với properties như data, methods, computed, và lifecycle hooks.

**Trong Vue Context**: Options API vẫn supported trong Vue 3 và backwards compatible. Nó cung cấp a more structured approach nhưng có limitations với TypeScript support và code reuse.

**Ví dụ**:

```typescript
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'UserCard',

  // Props
  props: {
    user: {
      type: Object as () => User,
      required: true
    },
    showActions: {
      type: Boolean,
      default: true
    }
  },

  // Reactive state
  data() {
    return {
      isEditing: false,
      editForm: {
        name: '',
        email: ''
      }
    }
  },

  // Computed
  computed: {
    fullName(): string {
      return `${this.user.firstName} ${this.user.lastName}`
    },
    isAdmin(): boolean {
      return this.user.role === 'admin'
    }
  },

  // Methods
  methods: {
    startEditing() {
      this.editForm.name = this.user.name
      this.editForm.email = this.user.email
      this.isEditing = true
    },
    saveChanges() {
      this.$emit('update', this.editForm)
      this.isEditing = false
    }
  },

  // Lifecycle hooks
  mounted() {
    console.log('Component mounted')
  },

  // Watchers
  watch: {
    'user.email'(newEmail) {
      console.log('Email changed to:', newEmail)
    }
  }
})
```

**Xem thể**: Composition API, Component

## P

### Plugin

**Định nghĩa**: A self-contained code that adds global-level functionality to Vue application. Plugins có thể add components, directives, hoặc modify Vue's prototype.

**Trong Vue Context**: Plugins commonly used cho adding UI libraries, installing router/store, hoặc adding global features.

**Ví dụ**:

```typescript
// plugins/logger.ts
import type { App } from 'vue'

export const loggerPlugin = {
  install(app: App) {
    // Add to app instance
    app.config.globalProperties.$logger = {
      log: (message: string) => console.log(`[LOG] ${message}`),
      error: (message: string) => console.error(`[ERROR] ${message}`),
      warn: (message: string) => console.warn(`[WARN] ${message}`)
    }

    // Directive
    app.directive('logger', {
      mounted(el, binding) {
        console.log(`[v-logger] Element mounted with value: ${binding.value}`)
      }
    })
  }
}

// main.ts
import { createApp } from 'vue'
import { loggerPlugin } from '@/plugins/logger'

const app = createApp(App)
app.use(loggerPlugin)
app.mount('#app')

// Usage
// this.$logger.log('Hello')
// <div v-logger="someValue" />
```

**Xem thêm**: Application Instance, Vue.use

### Provide/Inject

**Định nghĩa**: A pattern cho passing data through component tree without prop drilling. Ancestor components "provide" values và descendants "inject" them.

**Trong Vue Context**: Perfect cho passing data through deep component hierarchies như theme, user context, hoặc configuration.

**Ví dụ**:

```typescript
// Ancestor component
import { provide, ref, readonly } from 'vue'

const theme = ref('light')

// Provide as readonly to prevent mutation
provide('theme', readonly(theme))

// Or provide with full access
provide('themeContext', {
  current: theme,
  setTheme: (newTheme: string) => {
    theme.value = newTheme
  }
})

// Descendant component
import { inject } from 'vue'

const theme = inject('theme')

// With default value
const theme = inject('theme', ref('light'))

// With type
interface ThemeContext {
  current: Ref<string>
  setTheme: (theme: string) => void
}

const context = inject<ThemeContext>('themeContext')
```

**Xem thêm**: Dependency Injection, Prop Drilling

### Prop

**Định nghĩa**: Custom attributes được used để pass data từ parent component xuống child component. Props are reactive và trigger re-renders when changed.

**Trong Vue Context**: Props là primary mechanism cho parent-child communication. Props should be immutable in child components.

**Ví dụ**:

```typescript
// TypeScript with defineProps
interface Props {
  title: string
  count?: number
  items: string[]
  user: User
  onClick: () => void
  variant?: 'primary' | 'secondary'
}

// Basic usage
const props = defineProps<Props>()

// With defaults
const props = withDefaults(defineProps<Props>(), {
  count: 0,
  variant: 'primary'
})

// Runtime props with validation
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  count: {
    type: Number,
    default: 0
  },
  items: {
    type: Array,
    required: true
  },
  callback: {
    type: Function as PropType<() => void>,
    required: true
  }
})
```

**Xem thêm**: Emits, Props Drilling, v-bind

### Prop Drilling

**Định nghĩa**: Anti-pattern trong đó props phải pass qua nhiều levels của nested components chỉ để reach a deeply nested component that actually needs them.

**Trong Vue Context**: Prop drilling có thể make code hard to maintain. Better alternatives bao gồm provide/inject, Pinia stores, hoặc slot composition.

**Ví dụ**:

```typescript
// Prop drilling - avoid this pattern
// App.vue
<ParentComponent :user="user" />

// ParentComponent.vue
<ChildComponent :user="user" />

// ChildComponent.vue
<GrandChildComponent :user="user" />

// GrandChildComponent.vue
// Actually uses the prop
props: { user: Object }

// Better approach - use provide/inject
// App.vue
provide('user', user)

// GrandChildComponent.vue
const user = inject('user')
```

**Xem thêm**: Provide/Inject, Pinia, Context API

## R

### Reactive System

**Định nghĩa**: Vue's internal system cho tracking dependencies và automatically updating DOM when state changes. Reactive system là core của Vue's rendering engine.

**Trong Vue Context**: Vue 3 uses ES Proxy-based reactivity. State wrapped in `ref()` hoặc `reactive()` becomes reactive - changes trigger updates.

**Ví dụ**:

```typescript
import { ref, reactive, computed, watch, isRef, toRefs } from 'vue'

// ref - for primitives and any value
const count = ref(0)
console.log(isRef(count)) // true
count.value++ // Must access .value

// reactive - for objects (deeply reactive)
const state = reactive({
  count: 0,
  user: { name: 'John' }
})
state.count++ // No .value needed

// computed - derived reactive values
const doubled = computed(() => count.value * 2)

// watch - respond to changes
watch(count, (newVal, oldVal) => {
  console.log(`Changed from ${oldVal} to ${newVal}`)
})

// toRefs - convert reactive object to refs
const { count, user } = toRefs(state)
// count.value and user.value are now reactive

// shallowRef - only tracks .value changes
import { shallowRef } from 'vue'
const items = shallowRef([1, 2, 3])
items.value = [4, 5, 6] // This triggers update
// But items.value.push(7) would NOT trigger update
```

**Xem thêm**: ref, reactive, computed, watch

### Ref

**Định nghĩa**: Một function tạo ra một reactive reference đến a value. `ref()` wraps primitive values in an object với a `.value` property để enable reactivity.

**Trong Vue Context**: `ref()` là primary way để create reactive state cho primitives. For objects, consider using `reactive()` instead.

**Ví dụ**:

```typescript
import { ref, isRef, unref, type Ref } from 'vue'

// Create ref
const count = ref(0)
const message = ref('Hello')
const user = ref({ name: 'John', age: 30 })
const items = ref<string[]>([])

// Access value
console.log(count.value) // 0
count.value++

// Check if ref
console.log(isRef(count)) // true

// Unwrap in template (automatic)
const template = computed(() => `Count: ${count.value}`)

// Type annotation
const count: Ref<number> = ref(0)
const countOrString: Ref<number | string> = ref(0)

// unref - get raw value
const raw = unref(count) // number
```

**Xem thể**: reactive, toRef, shallowRef

### Render Function

**Định nghĩa**: Một function trả về virtual DOM nodes. Vue uses render functions internally to create và update DOM.

**Trong Vue Context**: Templates được compiled thành render functions. Understanding render functions helps when you need to programmatically create components.

**Ví dụ**:

```typescript
import { h, defineComponent } from 'vue'

// Render function example
const MyComponent = defineComponent({
  render() {
    return h('div', { class: 'container' }, [
      h('h1', this.title),
      h('p', this.content)
    ])
  }
})

// With components
import { h, defineComponent } from 'vue'
import BaseButton from './BaseButton.vue'

const MyWrapper = defineComponent({
  render() {
    return h('div', [
      h(BaseButton, {
        onClick: this.handleClick
      }, () => 'Click me')
    ])
  }
})

// JSX alternative
const MyComponent = defineComponent({
  render() {
    return (
      <div class="container">
        <h1>{this.title}</h1>
        <p>{this.content}</p>
      </div>
    )
  }
})
```

**Xem thể**: Virtual DOM, JSX, Template

### Router

**Định nghĩa**: Vue Router là official routing library cho Vue.js, cung cấp navigation between views trong single-page application.

**Trong Vue Context**: Vue Router maps URLs to components, supports nested routes, navigation guards, và lazy loading.

**Ví dụ**:

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/pages/HomePage.vue')
  },
  {
    path: '/users/:id',
    name: 'user-detail',
    component: () => import('@/pages/UserDetailPage.vue'),
    props: true // Pass route params as props
  },
  {
    path: '/dashboard',
    component: () => import('@/layouts/DashboardLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/dashboard/home' },
      { path: 'home', component: () => import('@/pages/dashboard/Home.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

**Xem thể**: Vue Router, Navigation Guards, Lazy Loading

## S

### Scoped CSS

**Định nghĩa**: CSS được scoped đến specific component bằng cách thêm unique attribute selectors. Styles don't leak outside component boundary.

**Trong Vue Context**: `<style scoped>` automatically scopes CSS to component's elements.

**Ví dụ**:

```vue
<style scoped>
/* These styles only apply to this component */
.container {
  padding: 1rem;
}

/* With deep selector */
:deep(.external-component) {
  color: red;
}

/* With slot content */
:slotted(.slot-content) {
  font-weight: bold;
}

/* With global fallback */
:global(.external-style) {
  color: blue;
}
</style>
```

**Xem thể**: CSS Modules, Single-File Component

### Setup

**Định nghĩa**: Entry point cho Composition API trong Vue component. Code trong `setup()` runs trước khi component được created, trước cả props resolution.

**Trong Vue Context**: Trong `<script setup>`, setup runs automatically. In non-setup components, setup is an option function.

**Ví dụ**:

```typescript
// Non-setup syntax
export default {
  setup(props, { attrs, slots, emit, expose, root }) {
    const count = ref(0)

    // Return everything that should be available in template
    return {
      count,
      increment: () => count.value++
    }
  }
}

// <script setup> syntax (Vue 3)
const count = ref(0)
const increment = () => count.value++
// Automatically available in template
```

**Xem thể**: Composition API, script setup

### Single-File Component (SFC)

**Định nghĩa**: Vue component được defined trong một file với `.vue` extension, chứa template, script, và styles trong một file.

**Trong Vue Context**: SFC is Vue's recommended format, providing collocation of related code và excellent developer experience.

**Ví dụ**:

```vue
<script setup lang="ts">
import { ref } from 'vue'
import BaseButton from './BaseButton.vue'

interface Props {
  title: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  submit: [data: FormData]
}>()
</script>

<template>
  <div class="my-component">
    <h1>{{ title }}</h1>
    <BaseButton @click="handleClick">Click</BaseButton>
  </div>
</template>

<style scoped>
.my-component {
  padding: 1rem;
}
</style>
```

**Xem thể**: Component, Vue Component

### Slot

**Định nghĩa**: Một mechanism cho content distribution, cho phép parent components pass content vào child components. Slots enable flexible component composition.

**Trong Vue Context**: Vue supports named slots, scoped slots, và dynamic slot names.

**Ví dụ**:

```vue
<!-- Card.vue - slot provider -->
<template>
  <div class="card">
    <header class="card-header">
      <slot name="header">
        Default Header
      </slot>
    </header>
    <main class="card-body">
      <slot />
    </main>
    <footer class="card-footer">
      <slot name="footer" :user="currentUser" />
    </footer>
  </div>
</template>

<!-- Usage -->
<Card>
  <template #header>
    <h2>Custom Header</h2>
  </template>

  <p>Main content goes here</p>

  <template #footer="{ user }">
    <span>Logged in as {{ user.name }}</span>
  </template>
</Card>
```

**Xem thể**: Scoped Slot, Slot Props

### SSR (Server-Side Rendering)

**Định nghĩa**: Rendering Vue application trên server thành HTML string, sau đó client hydrates to become a fully interactive SPA.

**Trong Vue Context**: SSR improves initial page load performance và SEO. Nuxt provides built-in SSR capabilities.

**Ví dụ**:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  ssr: true // Default
})

// pages/index.vue
<script setup lang="ts">
// This runs on server and client
const { data } = await useFetch('/api/posts')
</script>

// For conditional code
if (import.meta.server) {
  // Server-only code
}
```

**Xem thể**: Hydration, CSR, Nuxt

### State Management

**Định nghĩa**: Pattern và tools cho managing application state across components. State management systems provide predictable ways to update và access global state.

**Trong Vue Context**: Pinia là official state management solution cho Vue 3. Nó cung cấp centralized stores với TypeScript support.

**Ví dụ**:

```typescript
// stores/cart.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  // State
  const items = ref<CartItem[]>([])
  const isLoading = ref(false)

  // Getters
  const itemCount = computed(() =>
    items.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  const total = computed(() =>
    items.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
  )

  // Actions
  const addItem = async (product: Product) => {
    isLoading.value = true
    try {
      const newItem = await api.addToCart(product.id)
      items.value.push(newItem)
    } finally {
      isLoading.value = false
    }
  }

  return {
    items,
    isLoading,
    itemCount,
    total,
    addItem
  }
})
```

**Xem thể**: Pinia, Global State, Store

## T

### Template

**Định nghĩa**: Phần HTML của Vue component được compiled thành render function. Templates cung cấp declarative way để describe desired UI structure.

**Trong Vue Context**: Vue templates use special syntax như `{{ }}` cho interpolation, `v-` directives cho binding, và `:` cho attribute binding.

**Ví dụ**:

```vue
<template>
  <div class="container">
    <!-- Interpolation -->
    <h1>{{ title }}</h1>

    <!-- Attribute binding -->
    <img :src="imageUrl" :alt="description" />

    <!-- Conditional -->
    <div v-if="isVisible">Visible</div>
    <div v-else>Hidden</div>

    <!-- List rendering -->
    <ul>
      <li v-for="item in items" :key="item.id">
        {{ item.name }}
      </li>
    </ul>

    <!-- Event handling -->
    <button @click="handleClick">Click</button>

    <!-- Two-way binding -->
    <input v-model="inputValue" />
  </div>
</template>
```

**Xem thêm**: Template Compilation, Render Function

### Teleport

**Định nghĩa**: Một built-in component cho rendering content vào một vị trí DOM khác. Useful cho modals, tooltips, và overlays.

**Trong Vue Context**: Teleport allows you to write component structure logically trong template while having content render in a different DOM location.

**Ví dụ**:

```vue
<template>
  <div class="parent">
    <h1>Parent Component</h1>

    <!-- Content renders in body -->
    <Teleport to="body">
      <div class="modal-overlay">
        <div class="modal-content">
          <h2>Modal Title</h2>
          <p>Modal content</p>
          <button @click="$emit('close')">Close</button>
        </div>
      </div>
    </Teleport>

    <!-- Conditional teleport -->
    <Teleport to="body" :disabled="!isMounted">
      <div v-if="showOverlay">
        Overlay content
      </div>
    </Teleport>
  </div>
</template>
```

**Xem thể**: Portal, Dynamic Component

### Transition

**Định nghĩa**: Built-in component for animating elements entering và leaving the DOM. Transitions provide smooth animations khi elements are added, removed, hoặc updated.

**Trong Vue Context**: Vue's transition system works with `v-if`, `v-show`, và dynamic components.

**Ví dụ**:

```vue
<template>
  <!-- Basic transition -->
  <Transition name="fade">
    <div v-if="show">Content</div>
  </Transition>

  <!-- Transition with modes -->
  <Transition name="slide" mode="out-in">
    <component :is="currentView" />
  </Transition>

  <!-- List transition -->
  <TransitionGroup name="list">
    <div v-for="item in items" :key="item.id">
      {{ item.name }}
    </div>
  </TransitionGroup>
</template>

<style>
/* CSS transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* List transitions */
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.list-move {
  transition: transform 0.3s ease;
}
</style>
```

**Xem thể**: Animation, CSS Transitions

## U

### v-bind

**Định nghĩa**: Directive cho one-way data binding từ data source đến element attribute. `:attr` là shorthand cho `v-bind:attr`.

**Trong Vue Context**: `v-bind` enables dynamic attribute binding, class binding, style binding, và prop binding.

**Ví dụ**:

```vue
<template>
  <!-- Basic attribute binding -->
  <img v-bind:src="imageUrl" :alt="description" />

  <!-- Class binding -->
  <div :class="{ active: isActive, 'text-danger': hasError }">
    Content
  </div>

  <!-- Style binding -->
  <div :style="{ color: textColor, fontSize: fontSize + 'px' }">
    Styled content
  </div>

  <!-- Object binding -->
  <div v-bind="{ id: dynamicId, class: dynamicClass }">
    Content
  </div>

  <!-- Prop binding -->
  <MyComponent :prop-name="value" />
</template>
```

**Xem thêm**: v-model, v-on, Binding

### v-for

**Định nghĩa**: Directive cho rendering a list of elements based on an array hoặc object. Requires `:key` for proper diffing.

**Trong Vue Context**: `v-for` supports iterating over arrays, objects, và numbers.

**Ví dụ**:

```vue
<template>
  <!-- Array iteration -->
  <li v-for="(item, index) in items" :key="item.id">
    {{ index }}: {{ item.name }}
  </li>

  <!-- Object iteration -->
  <div v-for="(value, key, index) in object" :key="key">
    {{ index }}. {{ key }}: {{ value }}
  </div>

  <!-- Number iteration -->
  <span v-for="n in 5" :key="n">{{ n }}</span>

  <!-- With template -->
  <template v-for="item in items" :key="item.id">
    <li>{{ item.name }}</li>
    <li class="divider">{{ item.description }}</li>
  </template>
</template>
```

**Xem thể**: :key, List Rendering

### v-if / v-show

**Định nghĩa**: Directives cho conditional rendering. `v-if` removes elements from DOM, `v-show` toggles visibility via CSS.

**Trong Vue Context**: Choose `v-if` for rarely changing conditions, `v-show` for frequent toggling.

**Ví dụ**:

```vue
<template>
  <!-- v-if - removes from DOM -->
  <div v-if="isLoggedIn">
    Welcome, user!
  </div>
  <div v-else>
    Please log in
  </div>

  <!-- v-show - CSS visibility -->
  <div v-show="isVisible">
    Always in DOM, just hidden
  </div>

  <!-- v-else-if chain -->
  <div v-if="type === 'A'">Type A</div>
  <div v-else-if="type === 'B'">Type B</div>
  <div v-else>Other type</div>

  <!-- With template (v-if) -->
  <template v-if="showContent">
    <h1>Title</h1>
    <p>Content</p>
  </template>
</template>
```

**Xem thể**: Conditional Rendering, v-else

### v-model

**Định nghĩa**: Directive cho two-way binding trên form inputs. V-model là syntactic sugar cho binding value và handling input events.

**Trong Vue Context**: `v-model` supports various input types và có thể be used với custom components thông qua modelValue prop.

**Ví dụ**:

```vue
<template>
  <!-- Text input -->
  <input v-model="textValue" type="text" />

  <!-- Checkbox -->
  <input v-model="checked" type="checkbox" />

  <!-- Multiple checkboxes -->
  <input v-model="selectedFruits" type="checkbox" value="apple" />
  <input v-model="selectedFruits" type="checkbox" value="banana" />

  <!-- Radio -->
  <input v-model="choice" type="radio" value="a" />
  <input v-model="choice" type="radio" value="b" />

  <!-- Select -->
  <select v-model="selected">
    <option value="">Select...</option>
    <option value="a">A</option>
    <option value="b">B</option>
  </select>

  <!-- Custom component v-model -->
  <CustomInput v-model="textValue" />
  <!-- Equivalent to -->
  <CustomInput
    :modelValue="textValue"
    @update:modelValue="textValue = $event"
  />
</template>
```

**Xem thể**: Two-Way Binding, Form Handling

### Vuex

**Định nghĩa**: Legacy state management library cho Vue 2. Đã được replaced bởi Pinia cho Vue 3 projects.

**Trong Vue Context**: Vuex still used trong Vue 2 projects. Nó introduced patterns như mutations, actions, và modules.

**Ví dụ**:

```typescript
// Vuex store
import { createStore } from 'vuex'

export default createStore({
  namespaced: true,

  state: {
    user: null,
    isLoading: false
  },

  getters: {
    isAuthenticated: (state) => !!state.user,
    userName: (state) => state.user?.name ?? 'Guest'
  },

  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_LOADING(state, loading) {
      state.isLoading = loading
    }
  },

  actions: {
    async fetchUser({ commit }, userId) {
      commit('SET_LOADING', true)
      try {
        const user = await api.getUser(userId)
        commit('SET_USER', user)
      } finally {
        commit('SET_LOADING', false)
      }
    }
  },

  modules: {}
})
```

**Xem thể**: Pinia, State Management

## W

### Watcher

**Định nghĩa**: Một reactive side-effect được triggered khi reactive state changes. Watchers allow you to respond to state changes.

**Trong Vue Context**: `watch` và `watchEffect` provide different approaches to watching reactive state.

**Ví dụ**:

```typescript
import { ref, watch, watchEffect } from 'vue'

const count = ref(0)
const user = ref({ name: 'John' })

// Watch single source
watch(count, (newVal, oldVal) => {
  console.log(`Count changed from ${oldVal} to ${newVal}`)
})

// Watch multiple sources
watch([count, user], ([newCount, newUser], [oldCount, oldUser]) => {
  console.log('Changed')
})

// Watch nested property
watch(() => user.value.name, (newName) => {
  console.log(`Name changed to ${newName}`)
})

// Deep watch
watch(user, (newUser) => {
  console.log('User changed:', newUser)
}, { deep: true })

// Immediate watch (runs on mount)
watch(searchQuery, async (query) => {
  const results = await searchAPI(query)
  this.results = results
}, { immediate: true })

// watchEffect - automatic tracking
watchEffect(() => {
  // Automatically tracks count.value
  console.log(`Count is: ${count.value}`)
})
```

**Xem thể**: watchEffect, Computed, Effect

## References

### Official Documentation

- Vue 3 Documentation: https://vuejs.org/
- Vue Router: https://router.vuejs.org/
- Pinia: https://pinia.vuejs.org/
- Vue Test Utils: https://test-utils.vuejs.org/

### External Resources

- Vue.js Design Patterns (O'Reilly)
- Vue School: https://vueschool.io/
- Vue Mastery: https://www.vuemastery.com/

### Tools

- Vue DevTools: https://devtools.vuejs.org/
- Vite: https://vitejs.dev/
- Volar: VS Code Extension

## Kết Luận

Từ điển thuật ngữ này cung cấp comprehensive reference cho Vue.js terminology. Nó được thiết kế để:

1. **Serve as Learning Resource**: Giúp beginners understand Vue concepts through clear explanations và examples.

2. **Act as Quick Reference**: Cung cấp fast lookup for experienced developers when encountering unfamiliar terms.

3. **Enable Consistent Communication**: Standardize terminology usage across teams và projects.

4. **Bridge Language Gap**: Provide bilingual explanations (Vietnamese concepts, English technical terms) for Vietnamese-speaking developers.

Các thuật ngữ được tổ chức alphabetically và cross-referenced để maximize usability. Khi encountering unfamiliar terms, sử dụng cross-references để expand understanding.

For continuous learning, thực hành sử dụng các thuật ngữ này trong daily development và code discussions. Vocabulary mastery comes through consistent application.
