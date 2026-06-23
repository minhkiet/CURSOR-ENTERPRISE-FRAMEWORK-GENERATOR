---
title: "Vue Decision Tree - Cây Quyết Định Vue.js"
description: "Hướng dẫn quyết định cho các lựa chọn kiến trúc và pattern trong Vue.js với các câu hỏi và câu trả lời có cấu trúc"
tags: ["vue", "javascript", "decision-tree", "architecture", "patterns"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Vue Decision Tree - Cây Quyết Định Vue.js

## Tổng Quan

Tài liệu này cung cấp một decision tree có cấu trúc giúp developers đưa ra quyết định đúng đắn khi lựa chọn patterns, tools, và architectural approaches trong Vue.js development. Mỗi decision point được trình bày dưới dạng câu hỏi với các lựa chọn và giải thích chi tiết cho từng lựa chọn.

Việc đưa ra quyết định kiến trúc đúng đắn là một trong những thách thức lớn nhất trong Vue development, đặc biệt với ecosystem phong phú và nhiều lựa chọn. Decision tree này giúp simplify quá trình này bằng cách break down complex decisions thành smaller, manageable choices.

Tài liệu được thiết kế để sử dụng như practical reference trong quá trình development, không phải đọc từ đầu đến cuối. Developers có thể navigate đến relevant sections dựa trên questions họ đang facing.

## Mục Đích

1. **Accelerate Decision Making**: Cung cấp structured approach để make architectural decisions nhanh chóng. Thay vì research từ đầu mỗi lần, developers có thể follow decision tree.

2. **Reduce Decision Fatigue**: Vue ecosystem có nhiều options, và decision tree giúp narrow down choices dựa trên specific requirements.

3. **Enable Consistency**: Team members follow same decision-making process, leading to consistent architecture across projects.

4. **Document Rationale**: Mỗi recommendation đi kèm rationale, giúp teams understand và adapt recommendations when needed.

## Project Setup Decisions

### Câu Hỏi 1: Nên sử dụng Vue 2 hay Vue 3?

```
Bạn đang bắt đầu project mới?
├── CÓ → Vue 3 (Recommended)
│         - Composition API
│         - Better TypeScript support
│         - Improved performance
│         - Active development
│         - Vite as default build tool
│
└── KHÔNG → Đang maintain Vue 2 project?
          ├── CÓ → Vue 2 + Options API
          │         - Still receives security updates
          │         - Consider migration plan
          │         - Vue CLI still supported
          │
          └── KHÔNG → Vue 2 (End of Life)
                    - Migrate to Vue 3
                    - Use Vue 2 Compatibility Build
```

**Recommendation**: **Vue 3 là lựa chọn duy nhất cho new projects**. Vue 3 cung cấp Composition API, TypeScript support tốt hơn, và performance improvements đáng kể so với Vue 2.

**When to Choose Vue 2**:

- Legacy project đã stable với Vue 2
- Team chưa ready cho Vue 3 migration
- Dependencies chưa support Vue 3

### Câu Hỏi 2: Build Tool nào phù hợp?

```
Bạn cần build tool cho Vue 3 project?
├── Vite (Recommended)
│    │
│    ├── Pros:
│    │   - Instant server start
│    │   - HMR nhanh
│    │   - Native ESM
│    │   - Optimized production builds
│    │
│    └── When to use:
│        - New projects (default)
│        - Projects cần fast development cycle
│        - Teams want modern tooling
│
├── Vue CLI
│    │
│    ├── Pros:
│    │   - Mature ecosystem
│    │   - Rich plugin ecosystem
│    │   - GUI interface available
│    │
│    └── When to use:
│        - Existing Vue CLI projects
│        - Complex webpack configurations
│        - Need extensive customization
│
└── Nuxt (Full-Stack Framework)
     │
     ├── Pros:
     │   - SSR/SSG built-in
     │   - File-based routing
     │   - Auto-imports
     │   - Server routes
     │
     └── When to use:
         - Need SSR hoặc SSG
         - Full-stack application
         - Want opinionated structure
```

**Recommendation**: **Vite là default choice cho Vue 3 SPAs**. Nó cung cấp superior developer experience với fast HMR và instant server start.

**When to Choose Nuxt**:

- SEO requirements cần SSR
- Full-stack application với backend routes
- Team prefers convention-over-configuration
- Need built-in features như auto-imports, file routing

### Câu Hỏi 3: Có cần TypeScript không?

```
Project cần TypeScript?
├── CÓ (Recommended for most projects)
│    │
│    ├── Benefits:
│    │   - Better IDE support
│    │   - Catch errors at compile time
│    │   - Self-documenting code
│    │   - Refactoring confidence
│    │
│    └── Setup:
│        - tsconfig.json với strict mode
│        - Volar extension for VS Code
│        - Define interfaces for components
│
└── KHÔNG
     │
     ├── When acceptable:
     │   - Small prototypes
     │   - Team unfamiliar với TypeScript
     │   - Quick experiments
     │
     └── Consider adding later:
         - Start with JSDoc comments
         - Use .d.ts files for types
         - Plan migration path
```

**Recommendation**: **Yes, use TypeScript**. TypeScript provides significant benefits for maintainability và error prevention, đặc biệt important trong larger projects và teams.

**Minimum Setup**:

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "moduleResolution": "bundler",
    "jsx": "preserve",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.vue"]
}
```

## Component Design Decisions

### Câu Hỏi 4: Composition API vs Options API?

```
Bạn nên sử dụng API style nào?
├── Composition API (Recommended)
│    │
│    ├── Benefits:
│    │   - Better TypeScript support
│    │   - Easier code reuse (composables)
│    │   - Better organization for large components
│    │   - Flexible logic composition
│    │
│    └── Best for:
│        - Complex components
│        - TypeScript projects
│        - Reusable logic patterns
│        - Long-term maintainability
│
├── Options API
│    │
│    ├── Benefits:
│    │   - More structured
│    │   - Easier for beginners
│    │   - Clear organization by option type
│    │
│    └── Best for:
│        - Simple components
│        - Team new to Vue
│        - Quick prototyping
│
└── MIXED (Vue 3 supports both)
     │
     └── When to mix:
         - Migrating from Vue 2
         - Simple presentational components
         - Gradual adoption
```

**Recommendation**: **Use Composition API as default**. Nó cung cấp better TypeScript support và better code organization, đặc biệt cho complex components.

**When to Use Options API**:

- Very simple presentational components
- Team members new to Vue 3
- Quick prototyping without TypeScript

### Câu Hỏi 5: Component nên có state management như thế nào?

```
Component cần state management approach nào?
├── Local State (ref/reactive)
│    │
│    ├── Use when:
│    │   - State chỉ dùng trong 1 component
│    │   - Child components don't need access
│    │   - No cross-component sharing
│    │
│    └── Examples:
│        - Form input values
│        - UI toggle states
│        - Animation states
│
├── Props và Emits
│    │
│    ├── Use when:
│    │   - Parent-child communication
│    │   - Data flow từ parent xuống
│    │   - Events flow từ child lên
│    │
│    └── Examples:
│        - Reusable UI components
│        - List item components
│        - Form field components
│
├── Provide/Inject
│    │
│    ├── Use when:
│    │   - Deep component tree sharing
│    │   - Avoid prop drilling
│    │   - Theme, locale, configuration
│    │
│    └── Examples:
│        - Theme provider
│        - User context
│        - Feature flags
│
└── Global State (Pinia)
     │
     ├── Use when:
     │   - State needed across many components
     │   - State needs persistence
     │   - Cross-domain data sharing
     │
     └── Examples:
         - Authentication state
         - Shopping cart
         - User preferences
```

**Decision Matrix**:

| Scenario | Recommendation |
|----------|----------------|
| Single component only | `ref()` hoặc `reactive()` |
| Parent passes to child | Props |
| Child notifies parent | Emits |
| Deep tree, same data | Provide/Inject |
| Multiple components need | Pinia store |
| Shared across routes | Pinia store |

### Câu Hỏi 6: Khi nào nên tạo Composable?

```
Component cần reusable logic?
├── YES - Tạo Composable khi:
│    │
│    ├── Criteria:
│    │   ├── Logic được reuse across components
│    │   ├── Multiple components need same behavior
│    │   ├── Logic is stateful (has reactive state)
│    │   └── No framework-specific coupling needed
│    │
│    └── Examples of good composables:
│        ├── useFetch() - API data fetching
│        ├── useLocalStorage() - persistence
│        ├── useDebounce() - input debouncing
│        ├── useModal() - modal state management
│        └── usePagination() - pagination logic
│
└── NO - Không cần Composable khi:
     │
     ├── Logic chỉ dùng trong 1 component
     ├── Simple utility function (no state)
     ├── Framework-specific không cần abstraction
     └── Could be a simple utility function
```

**Composable Template**:

```typescript
// composables/useFeature.ts
import { ref, computed, type Ref } from 'vue'

interface UseFeatureOptions {
  // Configuration options
}

interface UseFeatureReturn {
  // Reactive state
  // Computed values
  // Methods
}

export function useFeature(options: UseFeatureOptions = {}): UseFeatureReturn {
  // Implementation
  const state = ref(initialState)

  const computedValue = computed(() => /* ... */)

  const method = () => {
    // Logic
  }

  return {
    state,
    computedValue,
    method
  }
}
```

## State Management Decisions

### Câu Hỏi 7: Khi nào cần Pinia Store?

```
Application cần Pinia store?
├── CÓ - Cần Pinia khi:
│    │
│    ├── Criteria:
│    │   ├── State shared across multiple components
│    │   ├── State persists across route changes
│    │   ├── Need centralized state management
│    │   ├── Complex state logic with multiple mutations
│    │   └── Need devtools debugging
│    │
│    └── Examples:
│        ├── User authentication
│        ├── Shopping cart
│        ├── Global UI state (modals, toasts)
│        └── Application-wide settings
│
└── KHÔNG - Không cần Pinia khi:
     │
     ├── State chỉ cần trong 1 component
     ├── Simple parent-child data flow
     ├── Props/emits đủ cho communication
     ├── Very small application
     └── State có thể derived from other stores
```

**Store Organization Decision**:

```
Nên tổ chức store như thế nào?
├── Domain-based (Recommended)
│    │
│    ├── Structure:
│    │   ├── stores/auth.ts
│    │   ├── stores/cart.ts
│    │   ├── stores/products.ts
│    │   └── stores/orders.ts
│    │
│    └── Benefits:
│        - Clear ownership
│        - Easy to find related state
│        - Scales well
│
├── Feature-based
│    │
│    ├── Structure:
│    │   ├── stores/featureA/
│    │   ├── stores/featureB/
│    │   └── stores/shared/
│    │
│    └── Benefits:
│        - Better for large features
│        - Self-contained features
│        - Easy feature removal
│
└── Flat
     │
     ├── Structure:
     │   ├── store.ts (all state)
     │   └── store-helpers.ts
     │
     └── Best for:
         - Very small apps
         - Quick prototypes
```

### Câu Hỏi 8: State nên được persist không?

```
State có cần persistence không?
├── CÓ - Cần persist khi:
│    │
│    ├── User data nên survive refresh:
│    │   ├── Authentication tokens
│    │   ├── User preferences
│    │   ├── Shopping cart
│    │   └── Form draft data
│    │
│    └── Implementation options:
│        ├── pinia-plugin-persistedstate
│        ├── localStorage
│        └── IndexedDB for large data
│
└── KHÔNG - Không cần persist khi:
     │
     ├── State fetched from server on load
     ├── Temporary UI state
     ├── Computed from persistent state
     └── Privacy-sensitive data
```

**Persistence Strategy**:

```typescript
// stores/user.ts with persistence
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  // These persist
  const token = ref<string | null>(null)
  const preferences = ref<UserPreferences>(defaultPreferences)

  // These don't persist (fetched on load)
  const profile = ref<User | null>(null)

  // Actions
  const login = async (credentials) => {
    const response = await api.login(credentials)
    token.value = response.token
  }

  return { token, preferences, profile, login }
}, {
  // Only persist token and preferences
  persist: {
    paths: ['token', 'preferences']
  }
})
```

## Routing Decisions

### Câu Hỏi 9: Route nên được load như thế nào?

```
Routes nên được load eagerly hay lazily?
├── Lazy Load (Recommended for most)
│    │
│    ├── Benefits:
│    │   - Smaller initial bundle
│    │   - Faster Time to Interactive
│    │   - Better for apps with many routes
│    │
│    ├── When to use:
│    │   ├── All routes except initial
│    │   ├── Routes behind authentication
│    │   └── Heavy page components
│    │
│    └── Implementation:
│        └── { path: '/', component: () => import('./Page.vue') }
│
├── Eager Load
│    │
│    ├── Benefits:
│    │   - Faster subsequent navigation
│    │   - No loading flash
│    │
│    ├── When to use:
│    │   ├── Very small applications
│    │   ├── Initial landing page
│    │   └── Critical routes (login, 404)
│    │
│    └── Implementation:
│        └── { path: '/', component: HomePage }
│
└── Prefetch
     │
     ├── Benefits:
     │   - Lazy load with prefetch
     │   - Smooth navigation experience
     │
     └── When to use:
         - Balance between bundle size và UX
```

### Câu Hỏi 10: Navigation guards nên xử lý authentication thế nào?

```
Authentication guard nên implement như thế nào?
├── Route-level Guard (Simple)
│    │
│    ├── Best for:
│    │   ├── Simple auth requirements
│    │   └── All protected routes need same check
│    │
│    └── Implementation:
│        └── router.beforeEach((to, from, next) => {
│            if (to.meta.requiresAuth && !isLoggedIn) {
│                next('/login')
│            } else {
│                next()
│            }
│        })
│
├── Meta-based with Role Check (Recommended)
│    │
│    ├── Best for:
│    │   ├── Multiple auth levels
│    │   ├── Role-based access
│    │   └── Complex permission requirements
│    │
│    └── Implementation:
│        └── {
│            meta: {
│                requiresAuth: true,
│                roles: ['admin', 'editor']
│            }
│        }
│
└── Component-level Guard
     │
     ├── Best for:
     │   ├── Granular control
     │   └── Guards that need component context
     │
     └── Implementation:
         └── onMounted(() => {
             if (!canAccess()) router.push('/unauthorized')
         })
```

**Route Meta Types**:

```typescript
// types/router.ts
interface RouteMeta {
  title?: string
  requiresAuth?: boolean
  roles?: string[]
  guestOnly?: boolean
  layout?: 'default' | 'auth' | 'dashboard'
}
```

## Component Communication Decisions

### Câu Hỏi 11: Components nên communicate như thế nào?

```
Hai components cần share data?
├── Parent ↔ Child
│    │
│    ├── Props (down) + Emits (up)
│    │   └── Best for: Direct parent-child
│    │
│    ├── v-model
│    │   └── Best for: Form controls, two-way binding
│    │
│    └── defineModel (Vue 3.4+)
│        └── Best for: Two-way binding with cleaner syntax
│
├── Siblings
│    │
│    ├── Shared Parent
│    │   └── Lift state to shared parent
│    │
│    └── Pinia Store
│        └── Best for: Unrelated components
│
├── Ancestor ↔ Descendant
│    │
│    ├── Provide/Inject
│    │   └── Best for: Deep trees, avoid prop drilling
│    │
│    └── Pinia Store
│        └── Best for: Complex shared state
│
└── Cross-cutting
     │
     └── Event Bus (deprecated)
         └── Use Pinia or composables instead
```

**Decision Flow**:

```
Components need to share data
│
├─ Parent-Child?
│   └─ Yes → Props + Emits
│           ├─ Simple data → Props
│           ├─ Two-way → v-model hoặc defineModel
│           └─ Complex → Props + Events
│
├─ Siblings?
│   └─ Yes → Lift state to parent or use store
│
├─ Deep tree (prop drilling)?
│   └─ Yes → Provide/Inject or Store
│
└─ Unrelated components?
    └─ Yes → Pinia Store
```

### Câu Hỏi 12: Khi nào nên use v-model vs Props/Emits?

```
Nên dùng v-model hay Props + Emits?
├── v-model (Recommended for forms)
│    │
│    ├── Best for:
│    │   ├── Form inputs
│    │   ├── Two-way binding
│    │   ├── Native-like components
│    │   └── When value should sync both ways
│    │
│    └── Vue 3.4+ syntax:
│        const model = defineModel<string>()
│        // v-model:modelValue + @update:modelValue
│
└── Props + Emits (Explicit)
     │
     ├── Best for:
     │   ├── Complex data objects
     │   ├── Multiple props needed
     │   ├── Clearer data flow
     │   └── When you want explicit events
     │
     └── Syntax:
         const props = defineProps<Props>()
         const emit = defineEmits<{ ... }>()
```

## Performance Decisions

### Câu Hỏi 13: Khi nào cần Lazy Loading?

```
Component/page nào nên lazy load?
├── Routes
│    │
│    ├── All routes (Recommended)
│    │   └── component: () => import('./Page.vue')
│    │
│    ├── Exceptions:
│    │   ├── Initial landing page
│    │   ├── Error pages
│    │   └── Auth pages (for quick redirects)
│
├── Components
│    │
│    ├── Heavy components
│    │   ├── Charts/graphs
│    │   ├── Rich text editors
│    │   ├── Video players
│    │   └── Maps
│    │
│    └── Conditional display
│        └── defineAsyncComponent
│
└── Libraries
     │
     ├── Heavy dependencies
     │   ├── moment.js
     │   ├── chart.js
     │   └── date-fns
     │
     └── Dynamic import
         └── const heavyLib = () => import('heavy-lib')
```

### Câu Hỏi 14: Reactivity nào phù hợp?

```
Nên dùng ref, reactive, hay shallowRef?
├── ref<T>()
│    │
│    ├── Best for:
│    │   ├── Primitive values (string, number, boolean)
│    │   ├── Values you'll replace entirely
│    │   ├── Clear .value access pattern
│    │   └── Most cases
│    │
│    └── Example:
│        const count = ref(0)
│        const user = ref<User | null>(null)
│
├── reactive()
│    │
│    ├── Best for:
│    │   ├── Related state grouped together
│    │   ├── Objects you mutate in place
│    │   └── Form state
│    │
│    └── Example:
│        const form = reactive({
│            email: '',
│            password: ''
│        })
│
├── shallowRef()
│    │
│    ├── Best for:
│    │   ├── Large data structures
│    │   ├── When you replace, not mutate
│    │   └── Performance-critical updates
│    │
│    └── Example:
│        const tableData = shallowRef<TableData[]>([])
│        // Trigger update by reassignment
│
└── shallowReactive()
     │
     ├── Best for:
     │   └── Objects where you replace nested, not mutate
```

**Reactivity Decision Matrix**:

| Type | Use For | Don't Use For |
|------|---------|---------------|
| `ref()` | Primitives, replacing values | Objects you mutate |
| `reactive()` | Related object state | Independent primitives |
| `shallowRef()` | Large data, bulk updates | Deep reactivity needed |
| `shallowReactive()` | Top-level mutations only | Nested reactivity |

### Câu Hỏi 15: Computed vs Watch?

```
Nên dùng computed hay watch?
├── Computed (Preferred)
│    │
│    ├── Best for:
│    │   ├── Derived state
│    │   ├── Read-only values
│    │   ├── Cached results
│    │   └── Synchronous calculations
│    │
│    └── Syntax:
│        const doubled = computed(() => count.value * 2)
│
└── Watch
     │
     ├── Best for:
     │   ├── Side effects
     │   ├── Async operations
     │   ├── Complex change detection
     │   └── When you need old/new values
     │
     └── Syntax:
         watch(count, (newVal, oldVal) => {
             // Side effect
         })
```

**Decision Rules**:

```
Need reactive value?
│
├─ Derive from other values?
│   └─ Yes → Use **computed**
│
├─ Side effect on change?
│   └─ Yes → Use **watch**
│
├─ Async operation on change?
│   └─ Yes → Use **watch** with async
│
└─ Need old and new value?
    └─ Yes → Use **watch**
```

## API & Data Fetching Decisions

### Câu Hỏi 16: Data fetching nên xử lý thế nào?

```
Application nên fetch data như thế nào?
├── Composables (Recommended)
│    │
│    ├── Best for:
│    │   ├── Custom fetching logic
│    │   ├── Reusable data fetching
│    │   ├── TypeScript projects
│    │   └── Need caching control
│    │
│    └── Pattern:
│        const { data, loading, error } = useFetch('/api/users')
│
├── Vue Query / TanStack Query
│    │
│    ├── Best for:
│    │   ├── Complex caching needs
│    │   ├── Optimistic updates
│    │   ├── Background refetching
│    │   └── Enterprise applications
│    │
│    └── Benefits:
│        ├── Automatic caching
│        ├── Stale-while-revalidate
│        └── Built-in loading/error states
│
├── Nuxt useFetch (if using Nuxt)
│    │
│    ├── Best for:
│    │   ├── SSR/SSG projects
│    │   ├── Auto key generation
│    │   └── Built-in hydration
│    │
│    └── Syntax:
│        const { data } = await useFetch('/api/users')
│
└── Direct fetch (Simple cases)
     │
     ├── Best for:
     │   ├── One-off requests
     │   ├── Simple components
     │   └── Quick prototypes
     │
     └── Pattern:
         const data = ref(null)
         onMounted(async () => {
             data.value = await fetch(url)
         })
```

### Câu Hỏi 17: Error handling nên implement thế nào?

```
API errors nên được handle như thế nào?
├── Component-level
│    │
│    ├── Best for:
│    │   ├── Simple error display
│    │   ├── UI-specific error states
│    │   └── Per-feature error handling
│    │
│    └── Pattern:
│        const { data, error } = await useFetch(url)
│        // Display error.value.message
│
├── Global Error Handler
│    │
│    ├── Best for:
│    │   ├── Centralized logging
│    │   ├── Error tracking integration
│    │   └── Unhandled errors
│    │
│    └── Pattern:
│        app.config.errorHandler = (err, vm, info) => {
│            errorTracking.capture(err)
│        }
│
└── Error Boundary Component
     │
     ├── Best for:
     │   ├── Graceful degradation
     │   ├── Recovery UI
     │   └── Preventing full crashes
     │
     └── Pattern:
         <ErrorBoundary>
             <SuspiciousComponent />
         </ErrorBoundary>
```

## Testing Decisions

### Câu Hỏi 18: Nên test ở level nào?

```
Testing pyramid cho Vue:
│
├─ Unit Tests (Foundation)
│    │
│    ├── Test:
│    │   ├── Composables
│    │   ├── Utilities
│    │   └── Store actions/getters
│    │
│    ├── Tools:
│    │   ├── Vitest
│    │   └── @vue/test-utils
│    │
│    └── When to write:
│        ├── Complex business logic
│        └── Reusable utilities
│
├─ Component Tests
│    │
│    ├── Test:
│    │   ├── Component rendering
│    │   ├── User interactions
│    │   └── Props/events
│    │
│    ├── Tools:
│    │   └── @vue/test-utils
│    │
│    └── When to write:
│        ├── Reusable components
│        └── Complex interactions
│
└─ E2E Tests (Top)
     │
     ├── Test:
     │   ├── Critical user flows
     │   ├── Authentication
     │   └── Checkout process
     │
     ├── Tools:
     │   ├── Playwright
     │   └── Cypress
     │
     └── When to write:
         ├── Happy path flows
         └── Critical user journeys
```

## Styling Decisions

### Câu Hỏi 19: Styling approach nào phù hợp?

```
Nên style Vue components như thế nào?
├── Scoped CSS (Recommended)
│    │
│    ├── Best for:
│    │   ├── Component-specific styles
│    │   ├── Avoiding conflicts
│    │   ├── Vue SFC
│    │
│    └── Syntax:
│        <style scoped>
│        .button { color: blue; }
│        </style>
│
├── CSS Variables
│    │
│    ├── Best for:
│    │   ├── Theming
│    │   ├── Design systems
│    │   ├── Cross-component consistency
│    │
│    └── Syntax:
│        :root { --primary: blue; }
│        .button { color: var(--primary); }
│
├── Utility Classes (Tailwind)
│    │
│    ├── Best for:
│    │   ├── Rapid development
│    │   ├── Consistent spacing/sizing
│    │   ├── Utility-first workflow
│    │
│    └── Syntax:
│        <div class="flex items-center p-4">
│
├── CSS Modules
│    │
│    ├── Best for:
│    │   ├── Scoped without Vue-specific syntax
│    │   ├── Non-SFC components
│    │   └── Explicit class mappings
│    │
│    └── Syntax:
│        <script setup>
│        import styles from './Button.module.css'
│        </script>
│        <div :class="styles.button">
│
└── Preprocessors (SCSS/Less)
     │
     ├── Best for:
     │   ├── Complex styles
     │   ├── Reusable patterns
     │   └── Existing SCSS codebase
     │
     └── Syntax:
         <style lang="scss">
         $primary: blue;
         .button { color: $primary; }
         </style>
```

**Styling Combination Matrix**:

| Use Case | Primary | Secondary |
|----------|---------|-----------|
| Small project | Scoped CSS | CSS Variables |
| Design system | CSS Variables | Scoped CSS |
| Rapid prototyping | Tailwind | Components |
| Complex styles | SCSS | Scoped CSS |
| SSR styling | CSS Variables | Scoped CSS |

## Framework Decisions

### Câu Hỏi 20: Vue SPA hay Nuxt?

```
Nên chọn Vue SPA hay Nuxt?
├── Vue SPA (Vue + Vue Router)
│    │
│    ├── Best for:
│    │   ├── Pure frontend applications
│    │   ├── Existing backend API
│    │   ├── Maximum control
│    │   ├── Smaller bundle sizes
│    │   └── Simple deployment
│    │
│    ├── Trade-offs:
│    │   ├── Need manual setup for routing
│    │   ├── Manual SSR if needed
│    │   └── More configuration
│
└── Nuxt (Vue Meta-framework)
     │
     ├── Best for:
     │   ├── Full-stack applications
     │   ├── SEO requirements
     │   ├── SSR/SSG/ISR
     │   ├── File-based routing
     │   ├── Auto-imports
     │   └── Quick development
     │
     ├── Trade-offs:
     │   ├── Opinionated structure
     │   ├── Learning curve
     │   ├── More abstraction
     │   └── Larger initial bundle
```

**Decision Criteria**:

| Criteria | Vue SPA | Nuxt |
|----------|---------|------|
| SEO important | Need SSR setup | Built-in SSR |
| Backend needed | Separate API | Server routes available |
| Team size | Any | Better for larger teams |
| Timeline | More setup time | Faster initial development |
| Control needed | Full control | Convention-based |
| Deployment | Simple | More complex |

## Summary Decision Tables

### Quick Reference Matrix

| Decision | Recommendation | Alternative |
|----------|----------------|-------------|
| Vue Version | Vue 3 | Vue 2 (legacy only) |
| Build Tool | Vite | Vue CLI (legacy) |
| API Style | Composition | Options (simple only) |
| State Local | `ref()` / `reactive()` | `reactive()` for forms |
| State Global | Pinia | Provide/Inject (tree only) |
| Routes | Lazy Load | Eager (landing only) |
| Components | Lazy async | Eager (critical only) |
| Styling | Scoped + Variables | Tailwind / SCSS |
| Fetching | Composables | Vue Query (complex) |
| Testing | Vitest + Test Utils | Cypress (E2E) |

### Anti-Patterns to Avoid

| Anti-Pattern | Avoid When | Use Instead |
|--------------|------------|-------------|
| Prop mutation | Always | Emit updates |
| Prop drilling | Deep trees | Provide/Inject or Store |
| Any type | TypeScript projects | Proper types |
| Magic strings | Routing | Route names |
| Global event bus | Communication | Pinia or emits |
| Inline functions | Templates | Methods |
| Missing keys | v-for loops | Unique keys |
| Uncleaned effects | Effects | onUnmounted cleanup |

## References

### Vue Official Resources

- Vue 3 Documentation: https://vuejs.org/
- Vue Router Guide: https://router.vuejs.org/
- Pinia Documentation: https://pinia.vuejs.org/
- Vue Testing Guide: https://test-utils.vuejs.org/

### Additional Resources

- Vue Design Patterns: https://vueschool.io/
- Vue Mastery: https://www.vuemastery.com/
- Component Libraries: Quasar, Vuetify, Naive UI

### Tools Reference

| Purpose | Tool | Decision Tree Reference |
|---------|------|------------------------|
| Build | Vite | Project Setup |
| State | Pinia | State Management |
| Routing | Vue Router | Routing |
| Testing | Vitest | Testing |
| Types | TypeScript | Project Setup |
| Styling | Scoped CSS | Styling |

## Kết Luận

Decision tree này cung cấp structured approach cho making Vue architectural decisions. Key takeaways:

1. **Default to Recommendations**: Recommendations được marked với "Recommended" là starting point tốt nhất cho hầu hết cases.

2. **Context Matters**: Mọi recommendation có thể có exceptions dựa trên specific requirements. Evaluate each decision in context.

3. **Document Deviations**: Khi deviate từ recommendations, document rationale. Giúp future team members understand decisions.

4. **Review Periodically**: Ecosystem evolving. Review decisions periodically để ensure they still make sense.

5. **Team Consistency**: Sử dụng decision tree as common reference giúp maintain consistency across team.

For complex decisions, consider creating mini decision trees for your specific context và add to this document for future reference.
