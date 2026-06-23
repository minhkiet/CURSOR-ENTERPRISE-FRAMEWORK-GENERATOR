---
title: "Vue FAQ - Câu Hỏi Thường Gặp Vue.js"
description: "Tổng hợp các câu hỏi thường gặp về Vue.js với câu trả lời chuyên sâu từ các chuyên gia"
tags: ["vue", "javascript", "faq", "questions", "answers", "troubleshooting"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Vue FAQ - Câu Hỏi Thường Gặp Vue.js

## Tổng Quan

Tài liệu này tổng hợp các câu hỏi thường gặp (Frequently Asked Questions) về Vue.js, được trả lời chi tiết bởi các chuyên gia trong lĩnh vực. Mỗi câu hỏi được phân loại theo category và bao gồm giải thích sâu, examples, và references đến documentation liên quan.

FAQ được thiết kế để address common pain points và misconceptions developers thường gặp khi làm việc với Vue. Các câu trả lời không chỉ provide immediate solutions mà còn explain underlying concepts để help readers understand why.

## Câu Hỏi Cơ Bản

### Q1: Vue 2 vs Vue 3 - Tôi nên chọn version nào?

**Câu hỏi**: Tôi đang bắt đầu một project mới. Nên chọn Vue 2 hay Vue 3? Tôi nghe nói Vue 2 vẫn còn được sử dụng rộng rãi.

**Câu trả lời chi tiết**:

**Vue 3 là lựa chọn duy nhất cho new projects vào năm 2026**. Dưới đây là reasons:

1. **Vue 2 đã End-of-Life**: Vue 2 đã officially entered End-of-Life state và không còn receive updates hoặc security patches. Using it cho new projects là security risk.

2. **Composition API**: Vue 3 cung cấp Composition API - một way to organize component logic that is more flexible, testable, và TypeScript-friendly. Đây là future của Vue development.

3. **Performance Improvements**: Vue 3's runtime có significant performance improvements so với Vue 2, bao gồm faster rendering, smaller bundle size, và better memory management.

4. **TypeScript Native Support**: Vue 3 được viết in TypeScript từ ground up, providing first-class TypeScript support. Vue 2 requires additional configuration cho TypeScript.

5. **Modern Build Tooling**: Vue 3 works optimally với Vite - một next-generation build tool với instant server start và fast HMR.

**Migration Path nếu đang dùng Vue 2**:

```typescript
// Vue 2 Options API
export default {
  data() {
    return { count: 0 }
  },
  methods: {
    increment() { this.count++ }
  }
}

// Vue 3 Composition API
<script setup lang="ts">
import { ref } from 'vue'

const count = ref(0)
const increment = () => count.value++
</script>
```

**When Vue 2 might still be relevant**:

- Maintaining existing Vue 2 codebase (plan migration)
- Legacy dependencies chưa support Vue 3
- Team chưa ready cho Vue 3 migration

### Q2: Composition API vs Options API - Nên dùng cái nào?

**Câu hỏi**: Vue 3 hỗ trợ cả Composition API và Options API. Khi nào nên dùng cái nào?

**Câu trả lời chi tiết**:

**Recommendation: Use Composition API as your default approach**. Đây là reasons:

**Benefits của Composition API**:

```typescript
// Better code organization
// Instead of scattering related logic across multiple options...

// Options API - Logic scattered
export default {
  data() { return { count: 0, doubled: 0 } },
  computed: {
    doubled() { return this.count * 2 }
  },
  watch: {
    count(newVal) {
      this.doubled = newVal * 2
      this.saveToServer(newVal)
    }
  },
  methods: {
    increment() { this.count++ },
    decrement() { this.count-- }
  }
}

// Composition API - Related logic grouped
<script setup lang="ts">
import { ref, computed, watch } from 'vue'

// All counter logic together
const count = ref(0)
const doubled = computed(() => count.value * 2)

watch(count, async (newVal) => {
  await saveToServer(newVal)
})

const increment = () => count.value++
const decrement = () => count.value--
</script>
```

**When to use each**:

| Scenario | Recommendation |
|----------|----------------|
| New Vue 3 project | Composition API |
| Complex components | Composition API |
| TypeScript project | Composition API |
| Reusable logic | Composition API (composables) |
| Simple component | Either (team preference) |
| Quick prototype | Either |
| Vue 2 migration | Gradual (both work) |

### Q3: Pinia vs Vuex - State management nào tốt hơn?

**Câu hỏi**: Vue 3 nên sử dụng Pinia hay Vuex? Vuex có còn được recommend không?

**Câu trả lời chi tiết**:

**Pinia là lựa chọn duy nhất cho Vue 3 projects**. Vuex đã officially deprecated cho new Vue 3 projects.

**Why Pinia is better**:

```typescript
// Pinia - Simpler, TypeScript-friendly
// stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const profile = ref<User | null>(null)

  const isAuthenticated = computed(() => profile.value !== null)

  const login = async (credentials: Credentials) => {
    const response = await api.login(credentials)
    profile.value = response.user
  }

  return { profile, isAuthenticated, login }
})

// Usage - no complex setup
const userStore = useUserStore()
userStore.login(credentials)
```

**Pinia vs Vuex comparison**:

| Feature | Pinia | Vuex |
|---------|-------|------|
| TypeScript | Native | Requires workarounds |
| Boilerplate | Minimal | High |
| DevTools | Full support | Limited |
| Module system | Flat | Namespaced modules |
| Mutations | Not required | Required |
| Learning curve | Low | High |
| Future support | Active | Maintenance only |

### Q4: Nuxt hay Vue SPA - Khi nào nên dùng Nuxt?

**Câu hỏi**: Tôi đang quyết định giữa Vue SPA thuần và Nuxt. Khi nào nên chọn Nuxt?

**Câu trả lời chi tiết**:

**Chọn Nuxt khi**:

1. **SEO là requirement quan trọng**: Nuxt cung cấp SSR/SSG built-in, giúp search engines index content properly.

2. **Full-stack application**: Nuxt 3 có server routes, API handlers, và database integration.

3. **Convention over configuration**: Team prefer structured approach với file-based routing.

4. **Built-in features cần thiết**: Auto-imports, image optimization, PWA support.

**Chọn Vue SPA khi**:

```typescript
// Vue SPA - Maximum control
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: () => import('./pages/Home.vue') },
    // Manual route definition
  ]
})
```

**Decision criteria**:

| Requirement | Vue SPA | Nuxt |
|-------------|---------|------|
| SEO | Need SSR setup | Built-in SSR |
| Full-stack | Separate backend | Server routes |
| Team preference | Maximum control | Convention |
| Timeline | More setup | Faster start |
| Performance | Customizable | Optimized defaults |

## Câu Hỏi về Reactivity

### Q5: Tại sao state của tôi không reactive?

**Câu hỏi**: Tôi đang cố gắng update một giá trị trong component nhưng UI không re-render. Tại sao?

**Câu trả lời chi tiết**:

Đây là một trong những vấn đề phổ biến nhất trong Vue. Có several causes:

**1. Missing Reactivity System**:

```typescript
// Không reactive - plain object
const user = { name: 'John' }
user.name = 'Jane' // UI won't update!

// Reactive
import { reactive } from 'vue'
const user = reactive({ name: 'John' })
user.name = 'Jane' // UI updates
```

**2. Destructuring Breaking Reactivity**:

```typescript
import { reactive } from 'vue'

const state = reactive({ count: 0, name: 'John' })

// ❌ Destructuring breaks reactivity
const { count, name } = state
count++ // Won't update UI!

// ✅ Correct approaches
// Option 1: Use as-is
state.count++

// Option 2: Use toRefs
import { toRefs } from 'vue'
const { count, name } = toRefs(state)
count.value++ // Works!

// Option 3: Computed
import { computed } from 'vue'
const count = computed(() => state.count)
```

**3. Array Index Assignment**:

```typescript
import { reactive } from 'vue'

const items = reactive([1, 2, 3])

// ❌ This won't trigger reactivity
items[0] = 10

// ✅ Correct approaches
// Option 1: Use splice
items.splice(0, 1, 10)

// Option 2: Replace entire array
Object.assign(items, [10, 2, 3])

// Option 3: Use ref for arrays
import { ref } from 'vue'
const items = ref([1, 2, 3])
items.value[0] = 10 // Works!
```

**4. Object Property Addition**:

```typescript
import { reactive } from 'vue'

const state = reactive({ name: 'John' })

// ❌ New properties aren't reactive
state.age = 30 // Won't update!

// ✅ Correct approaches
// Option 1: Use Object.assign
Object.assign(state, { age: 30 })

// Option 2: Define all upfront
const state = reactive({ name: 'John', age: 0 })

// Option 3: Use ref
import { ref } from 'vue'
const state = ref({ name: 'John' })
state.value.age = 30 // Works!
```

### Q6: Computed vs Watch - Khi nào dùng cái nào?

**Câu hỏi**: Tôi không chắc chắn khi nào nên dùng computed property và khi nào nên dùng watcher. Có thể giải thích?

**Câu trả lời chi tiết**:

**Basic Rule**:

- **Computed**: Để tạo derived values (read-only, automatic caching)
- **Watch**: Để respond to changes (side effects, read/write, async operations)

**Computed cho Derived State**:

```typescript
import { ref, computed } from 'vue'

const firstName = ref('John')
const lastName = ref('Doe')

// ✅ Computed - pure derivation
const fullName = computed(() => `${firstName.value} ${lastName.value}`)

// Computed là cached - chỉ re-compute khi dependencies thay đổi
// Nếu firstName hoặc lastName không thay đổi,
// fullName sẽ return cached value
```

**Watch cho Side Effects**:

```typescript
import { ref, watch } from 'vue'

const searchQuery = ref('')
const searchResults = ref([])

// ✅ Watch - side effect (async operation)
watch(searchQuery, async (query) => {
  if (query.length > 2) {
    const results = await fetch(`/api/search?q=${query}`)
    searchResults.value = results
  }
}, { immediate: true })
```

**Watch cho Old/New Values**:

```typescript
import { ref, watch } from 'vue'

const count = ref(0)

// ✅ Watch - khi cần old value
watch(count, (newVal, oldVal) => {
  console.log(`Changed from ${oldVal} to ${newVal}`)
  if (oldVal < 5 && newVal >= 5) {
    showCelebration()
  }
})
```

**Common Mistakes**:

```typescript
// ❌ WRONG: Side effect trong computed
const doubled = computed(() => {
  fetch(`/api/count/${count.value}`) // Side effect!
  return count.value * 2
})

// ✅ CORRECT: Computed for derivation
const doubled = computed(() => count.value * 2)

// ✅ CORRECT: Watch for side effect
watch(count, async (newVal) => {
  await saveToServer(newVal)
})
```

## Câu Hỏi về Component

### Q7: Props không thay đổi được - Tôi nên làm gì?

**Câu hỏi**: Tôi nhận được một prop trong component con và muốn modify nó. Vue báo lỗi "Avoid mutating a prop directly". Tôi nên làm sao?

**Câu trả lời chi tiết**:

**Vue's One-Way Data Flow**: Props là read-only by design. Child components không nên modify props vì nó vi phạm one-way data flow và tạo ra unpredictable state.

**Solutions**:

**1. Emit event để parent xử lý**:

```vue
<!-- ChildComponent.vue -->
<script setup lang="ts">
const props = defineProps<{
  count: number
}>()

const emit = defineEmits<{
  'update:count': [value: number]
}>()

const increment = () => {
  emit('update:count', props.count + 1)
}
</script>
```

```vue
<!-- ParentComponent.vue -->
<script setup lang="ts">
import { ref } from 'vue'
import ChildComponent from './ChildComponent.vue'

const count = ref(0)
</script>

<template>
  <ChildComponent v-model:count="count" />
  <!-- Hoặc -->
  <ChildComponent :count="count" @update:count="count = $event" />
</template>
```

**2. Local state với initial value**:

```vue
<script setup lang="ts">
const props = defineProps<{
  initialCount: number
}>()

// Local copy - safe to modify
const count = ref(props.initialCount)
</script>
```

**3. v-model modifier (.sync deprecated in Vue 3)**:

```vue
<script setup lang="ts">
// Vue 3 v-model
const model = defineModel<number>({ default: 0 })

model.value++ // Modifies parent's state
</script>
```

### Q8: Khi nào nên tách component?

**Câu hỏi**: Component của tôi đang trở nên lớn. Khi nào nên tách nó thành nhiều components nhỏ hơn?

**Câu trả lời chi tiết**:

**Signs bạn cần tách component**:

```vue
<!-- ❌ Red flags - Component quá lớn -->
<template>
  <!-- 500+ lines of template -->
  <!-- Multiple distinct sections -->
  <!-- Multiple responsibilities -->
</template>

<script setup lang="ts">
// 1000+ lines of script
// Too many refs, computed, methods
// Multiple unrelated features
</script>

<!-- ✅ Refactor when you see: -->
<!-- 1. Logical sections (header, body, footer) -->
<!-- 2. Reusable patterns -->
<!-- 3. Complex nested structures -->
<!-- 4. Multiple team members need to edit -->
```

**Refactoring Example**:

```vue
<!-- ❌ Before: One huge component -->
<UserSettingsPage>
  <!-- Header with user info -->
  <!-- Profile form -->
  <!-- Password change -->
  <!-- Notification preferences -->
  <!-- Billing information -->
  <!-- Connected accounts -->
</UserSettingsPage>

<!-- ✅ After: Separated by concern -->
<UserSettingsPage>
  <template #header>
    <UserSettingsHeader :user="user" />
  </template>

  <ProfileSettings :profile="user.profile" />
  <PasswordChange @update="handlePasswordUpdate" />
  <NotificationPreferences v-model="preferences" />
  <BillingSection :billing="user.billing" />
  <ConnectedAccounts :accounts="user.accounts" />
</UserSettingsPage>
```

**Guidelines**:

| Factor | Keep in One | Split Out |
|--------|-------------|-----------|
| Reusability | Only here | Multiple places |
| Complexity | Low | High |
| Team | Single owner | Multiple owners |
| Testing | Easy | Hard |
| Lines of code | < 200 | > 400 |

### Q9: Slots vs Props - Khi nào dùng cái nào?

**Câu hỏi**: Tôi đang build một reusable component. Nên dùng slots hay props để truyền content?

**Câu trả lời chi tiết**:

**Slots** cho flexible content placement, **Props** cho data configuration.

**Props - Khi content là data-driven**:

```vue
<!-- DataTable - Props cho data -->
<template>
  <table>
    <thead>
      <tr>
        <th v-for="col in columns" :key="col.key">
          {{ col.label }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in data" :key="row.id">
        <td v-for="col in columns" :key="col.key">
          {{ row[col.key] }}
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
defineProps<{
  columns: Column[]
  data: Row[]
}>()
</script>

<!-- Usage -->
<DataTable :columns="userColumns" :data="users" />
```

**Slots - Khi content là custom**:

```vue
<!-- Card - Slots cho flexible content -->
<template>
  <div class="card">
    <header class="card-header">
      <slot name="header">
        Default Header
      </slot>
    </header>
    <div class="card-body">
      <slot>Default Body</slot>
    </div>
    <footer class="card-footer">
      <slot name="footer" :user="currentUser" />
    </footer>
  </div>
</template>

<!-- Usage -->
<Card>
  <template #header>
    <h2>User Profile</h2>
  </template>

  <p>Custom content here</p>

  <template #footer="{ user }">
    <span>{{ user.name }}</span>
  </template>
</Card>
```

**Hybrid Approach - Scoped Slots**:

```vue
<!-- TableGrid - Complex scenarios -->
<DataGrid :items="products">
  <template #cell="{ item, column }">
    <td v-if="column.key === 'price'">
      {{ formatCurrency(item.price) }}
    </td>
    <td v-else-if="column.key === 'actions'">
      <button @click="edit(item)">Edit</button>
    </td>
    <td v-else>
      {{ item[column.key] }}
    </td>
  </template>
</DataGrid>
```

## Câu Hỏi về Performance

### Q10: Làm sao để improve Vue app performance?

**Câu hỏi**: Ứng dụng Vue của tôi đang chậm. Có những cách nào để improve performance?

**Câu trả lời chi tiết**:

**1. Lazy Loading Routes**:

```typescript
// router/index.ts
const routes = [
  // ✅ Lazy load non-critical routes
  {
    path: '/dashboard',
    component: () => import('./pages/Dashboard.vue')
  },
  {
    path: '/settings',
    component: () => import('./pages/Settings.vue')
  },
  // ⚠️ Only eager load critical routes
  {
    path: '/',
    component: HomePage // Inline import
  }
]
```

**2. Virtual Scrolling cho Lists**:

```vue
<script setup lang="ts">
import { useVirtualList } from '@vueuse/core'

const items = ref([...Array(10000).keys()].map(i => ({ id: i })))

const { list, containerProps, wrapperProps } = useVirtualList(items, {
  itemHeight: 50,
  overscan: 10
})
</script>

<template>
  <div v-bind="containerProps" class="h-400px">
    <div v-bind="wrapperProps">
      <div v-for="{ data } in list" :key="data.id">
        {{ data.id }}
      </div>
    </div>
  </div>
</template>
```

**3. Computed thay vì Method trong Template**:

```vue
<!-- ❌ Method called every render -->
<template>
  <div>{{ formatDate(date) }}</div>
  <div>{{ formatCurrency(amount) }}</div>
</template>

<!-- ✅ Computed cached -->
<script setup lang="ts">
const formattedDate = computed(() => formatDate(date))
const formattedAmount = computed(() => formatCurrency(amount))
</script>

<template>
  <div>{{ formattedDate }}</div>
  <div>{{ formattedAmount }}</div>
</template>
```

**4. v-memo cho Stable Lists**:

```vue
<template>
  <!-- Only re-render when item.id or item.status changes -->
  <div v-for="item in items" v-memo="[item.id, item.status]">
    <ComplexComponent :item="item" />
  </div>
</template>
```

**5. shallowRef cho Large Data**:

```typescript
import { shallowRef } from 'vue'

// ❌ Deep reactivity - tracks all nested properties
const data = ref(veryLargeObject)

// ✅ Shallow - only tracks .value replacement
const data = shallowRef(veryLargeObject)
```

**6. Keep-alive cho Cached Components**:

```vue
<template>
  <router-view v-slot="{ Component }">
    <keep-alive :include="['UserList', 'ProductGrid']">
      <component :is="Component" />
    </keep-alive>
  </router-view>
</template>
```

### Q11: Bundle size lớn - Làm sao giảm?

**Câu hỏi**: Bundle size của ứng dụng Vue rất lớn. Có cách nào để giảm?

**Câu trả lời chi tiết**:

**1. Analyze Bundle**:

```bash
# Run bundle analyzer
npm run build -- --mode production
npx vite-bundle-visualizer
```

**2. Lazy Load Components**:

```typescript
// Instead of
import HeavyChart from './HeavyChart.vue'

// Use
const HeavyChart = defineAsyncComponent(() =>
  import('./HeavyChart.vue')
)
```

**3. Tree Shaking**:

```typescript
// ❌ Import entire library
import _ from 'lodash'
_.debounce()

// ✅ Import specific function
import debounce from 'lodash/debounce'

// ✅ Or use lighter alternative
import { debounce } from 'vueuse/core'
```

**4. External Dependencies**:

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      external: ['vue', 'vue-router', 'pinia']
    }
  }
})
```

**5. Replace Heavy Libraries**:

| Heavy | Lightweight Alternative |
|-------|------------------------|
| moment.js | date-fns, dayjs |
| lodash | lodash-es (tree-shakeable) |
| axios | ky, ofetch |
| chart.js | chart.js (tree-shake) |

**6. Optimize Images**:

```vue
<!-- Use modern formats -->
<img src="image.webp" />
<img src="image.avif" />

<!-- Lazy load -->
<img src="image.jpg" loading="lazy" />
```

## Câu Hỏi về TypeScript

### Q12: Làm sao để add TypeScript vào Vue project?

**Câu hỏi**: Tôi có Vue project không có TypeScript. Làm sao để add TypeScript vào?

**Câu trả lời chi tiết**:

**For New Projects (Recommended)**:

```bash
npm create vue@latest my-project -- --typescript
# Select TypeScript option during setup
```

**For Existing Projects**:

```bash
# Install TypeScript
npm install -D typescript vue-tsc

# Create tsconfig
npx tsc --init
```

**tsconfig.json Configuration**:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,

    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",

    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,

    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.tsx", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

**Type Your Components**:

```typescript
// UserCard.vue
<script setup lang="ts">
interface Props {
  user: {
    id: number
    name: string
    email: string
    role: 'admin' | 'user' | 'guest'
  }
  compact?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  compact: false
})

const emit = defineEmits<{
  select: [userId: number]
  delete: [userId: number]
}>()
</script>
```

### Q13: TypeScript errors với reactive objects

**Câu hỏi**: TypeScript complain khi tôi destructure từ reactive object. Làm sao fix?

**Câu trả lời chi tiết**:

**Problem**:

```typescript
import { reactive } from 'vue'

const state = reactive({
  count: 0,
  name: 'John'
})

// ❌ TypeScript error - loses reactivity
const { count, name } = state
```

**Solutions**:

**1. Use toRefs**:

```typescript
import { reactive, toRefs } from 'vue'

const state = reactive({
  count: 0,
  name: 'John'
})

// ✅ Preserves reactivity
const { count, name } = toRefs(state)
// count.value và name.value là reactive
```

**2. Keep Original Reference**:

```typescript
import { reactive } from 'vue'

const state = reactive({
  count: 0,
  name: 'John'
})

// ✅ Access through original reference
state.count++
state.name = 'Jane'
```

**3. Use Computed**:

```typescript
import { reactive, computed } from 'vue'

const state = reactive({
  count: 0,
  name: 'John'
})

// ✅ Typed refs
const count = computed(() => state.count)
const name = computed(() => state.name)
```

## Câu Hỏi về Testing

### Q14: Làm sao test Vue components?

**Câu hỏi**: Tôi muốn viết tests cho Vue components. Nên bắt đầu như thế nào?

**Câu trả lời chi tiết**:

**Setup Vitest + Vue Test Utils**:

```bash
npm install -D vitest @vue/test-utils happy-dom
```

**vitest.config.ts**:

```typescript
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'happy-dom',
    globals: true
  }
})
```

**Basic Component Test**:

```typescript
// UserCard.spec.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import UserCard from './UserCard.vue'

describe('UserCard', () => {
  const mockUser = {
    id: 1,
    name: 'John Doe',
    email: 'john@example.com',
    role: 'admin' as const
  }

  it('renders user information', () => {
    const wrapper = mount(UserCard, {
      props: { user: mockUser }
    })

    expect(wrapper.find('.name').text()).toBe('John Doe')
    expect(wrapper.find('.email').text()).toBe('john@example.com')
  })

  it('emits select event when clicked', async () => {
    const wrapper = mount(UserCard, {
      props: { user: mockUser }
    })

    await wrapper.find('.card').trigger('click')

    expect(wrapper.emitted('select')?.[0]).toEqual([mockUser.id])
  })

  it('shows actions when showActions is true', () => {
    const wrapper = mount(UserCard, {
      props: { user: mockUser, showActions: true }
    })

    expect(wrapper.find('.actions').exists()).toBe(true)
  })
})
```

### Q15: Mocking composables trong tests

**Câu hỏi**: Làm sao để mock một composable khi test component?

**Câu trả lời chi tiết**:

**Using vi.mock()**:

```typescript
// UserProfile.spec.ts
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

// Mock the composable
vi.mock('@/composables/useAuth', () => ({
  useAuth: () => ({
    user: { id: 1, name: 'Mock User' },
    isAuthenticated: true,
    logout: vi.fn()
  })
}))

import UserProfile from './UserProfile.vue'

describe('UserProfile', () => {
  it('displays user name', () => {
    const wrapper = mount(UserProfile)
    expect(wrapper.find('.user-name').text()).toBe('Mock User')
  })
})
```

**Using stubs**:

```typescript
import { mount } from '@vue/test-utils'
import UserCard from './UserCard.vue'

// Stub child component
const wrapper = mount(UserCard, {
  props: { user: mockUser },
  global: {
    stubs: {
      UserAvatar: {
        template: '<img class="avatar-stub" />'
      }
    }
  }
})
```

## Câu Hỏi về Routing

### Q16: Vue Router navigation không hoạt động

**Câu hỏi**: Router.push() không navigate đến trang mới. Console không có lỗi.

**Câu trả lời chi tiết**:

**Common Causes và Solutions**:

**1. Router chưa được install**:

```typescript
// main.ts
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router) // ⚠️ Missing!
app.mount('#app')
```

**2. async navigation không được awaited**:

```typescript
// ❌ async route guard not awaited
router.beforeEach(async (to, from) => {
  await checkAuth() // Missing return!
})

// ✅ Await the navigation
router.beforeEach(async (to, from) => {
  const isAuthenticated = await checkAuth()
  if (!isAuthenticated) return '/login'
})
```

**3. useRouter() chưa import**:

```typescript
import { useRouter } from 'vue-router'

export default {
  setup() {
    const router = useRouter() // ⚠️ Common mistake

    const navigate = () => {
      router.push('/dashboard')
    }

    return { navigate }
  }
}
```

**4. Router view không tồn tại**:

```vue
<!-- App.vue -->
<template>
  <nav>...</nav>

  <router-view /> <!-- ⚠️ Missing router-view! -->

  <footer>...</footer>
</template>
```

### Q17: Route params không reactive

**Câu hỏi**: Khi route params thay đổi, component không re-render với data mới.

**Câu trả lời chi tiết**:

**Problem**:

```typescript
// URL changes from /users/1 to /users/2
// But component doesn't re-fetch data
```

**Solution 1: Watch route params**:

```typescript
import { watch } from 'vue'
import { useRoute } from 'vue-router'

export default {
  setup() {
    const route = useRoute()
    const user = ref(null)

    // Watch route params
    watch(
      () => route.params.id,
      async (newId) => {
        user.value = await fetchUser(newId)
      },
      { immediate: true }
    )

    return { user }
  }
}
```

**Solution 2: Use props (Recommended)**:

```typescript
// router/index.ts
const routes = [
  {
    path: '/users/:id',
    component: () => import('./UserProfile.vue'),
    props: true // Pass route params as props
  }
]
```

```vue
<script setup lang="ts">
// UserProfile.vue
const props = defineProps<{
  id: string
}>()

// Automatically re-runs when id changes
const { data: user } = await useFetch(`/api/users/${props.id}`)
</script>
```

## Câu Hỏi về Styling

### Q18: CSS scoped không hoạt động

**Câu hỏi**: Styles trong `<style scoped>` không apply vào elements.

**Câu trả lời chi tiết**:

**Common Issues**:

**1. Dynamic classes không match**:

```vue
<style scoped>
/* ⚠️ Won't work for dynamic classes */
.my-class { color: red; }
</style>

<template>
  <!-- Use :class binding -->
  <div :class="dynamicClass">Content</div>
</style>
```

**2. Child component root elements**:

```vue
<!-- ParentComponent.vue -->
<style scoped>
/* ⚠️ Scoped styles don't penetrate child components */
.child-component { color: red; }
</style>

<template>
  <ChildComponent class="child-component" />
  <!-- Add class to child component -->
</template>
```

**3. Need deep selector**:

```vue
<style scoped>
/* ✅ Use :deep() for child components */
:deep(.child-class) { color: red; }

/* ✅ Use :global() for global styles */
:global(body) { margin: 0; }

/* ✅ Use :slotted() for slot content */
:slotted(.slot-class) { color: blue; }
</style>
```

## Câu Hỏi về Nuxt

### Q19: Nuxt vs Vue SPA - Performance comparison?

**Câu hỏi**: Nuxt app có chậm hơn Vue SPA không? Performance khác nhau như thế nào?

**Câu trả lời chi tiết**:

**Performance Characteristics**:

| Metric | Nuxt 3 | Vue SPA |
|--------|--------|---------|
| Initial Load | Faster (SSR) | Slower (no HTML) |
| Time to Interactive | Similar | Similar |
| SEO | Better | Requires SSR |
| Bundle Size | Larger (more features) | Smaller |
| Development Speed | Faster | Slower setup |
| Hosting Complexity | Higher | Lower |

**When Nuxt is Faster**:

```typescript
// Nuxt - Pre-rendered HTML
// User sees content immediately
// Hydration happens in background

// First Contentful Paint - Fast
// Search engines see full content - Great for SEO
```

**When Vue SPA is Better**:

```typescript
// For highly interactive apps
// Where SEO doesn't matter
// Where bundle size is critical
// For existing API-driven apps
```

### Q20: Migrate từ Vue SPA sang Nuxt?

**Câu hỏi**: Tôi có Vue SPA muốn migrate sang Nuxt. Cần làm những bước nào?

**Câu trả lời chi tiết**:

**Migration Steps**:

**1. Install Nuxt**:

```bash
npx nuxi init nuxt-app
cd nuxt-app
npm install
```

**2. Convert Components**:

```vue
<!-- Vue SPA -->
<script setup lang="ts">
import { ref } from 'vue'
// Component logic
</script>

<!-- Nuxt - mostly same -->
<script setup lang="ts">
// Same logic, but with auto-imports!
</script>
```

**3. Convert Router to File-based**:

```typescript
// Vue SPA - manually define routes
// router/index.ts
const routes = [
  { path: '/', component: () => import('./pages/Home.vue') }
]

// Nuxt - automatic file-based routing
// pages/index.vue → /
// pages/about.vue → /about
// pages/users/[id].vue → /users/:id
```

**4. Move API Calls**:

```typescript
// Vue SPA
// stores/user.ts
const fetchUser = async () => {
  return await fetch('/api/user')
}

// Nuxt - use server routes
// server/api/user.get.ts
export default defineEventHandler(() => {
  return { user: { name: 'John' } }
})
```

**5. Update State Management**:

```typescript
// Pinia works in Nuxt, just install plugin
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@pinia/nuxt']
})
```

## Troubleshooting Common Issues

### Issue 1: "Component is missing template or render function"

**Cause**: Vue compiler không recognize file là Vue component.

**Solution**:

```typescript
// ❌ Wrong file extension
import UserCard from './UserCard'

// ✅ Correct extension
import UserCard from './UserCard.vue'
```

### Issue 2: "Cannot read property of undefined"

**Cause**: Accessing reactive data before it's initialized.

**Solution**:

```typescript
// ❌ Access before initialization
const name = computed(() => user.value.name)
const user = ref(null)

// ✅ Define ref first
const user = ref(null)
const name = computed(() => user.value?.name)
```

### Issue 3: Memory leak warnings

**Cause**: Event listeners, intervals, hoặc subscriptions not cleaned up.

**Solution**:

```typescript
import { onMounted, onUnmounted } from 'vue'

onMounted(() => {
  window.addEventListener('resize', handleResize)
  const interval = setInterval(doSomething, 1000)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  clearInterval(interval)
})
```

## References

### Official Documentation

- Vue 3 Docs: https://vuejs.org/
- Vue Router: https://router.vuejs.org/
- Pinia: https://pinia.vuejs.org/
- Nuxt: https://nuxt.com/
- Vue Test Utils: https://test-utils.vuejs.org/

### Learning Resources

- Vue School: https://vueschool.io/
- Vue Mastery: https://www.vuemastery.com/
- Vue.js Developers Blog

### Tools

- Vue DevTools: Browser extension
- Vite: https://vitejs.dev/
- Volar: VS Code extension
- Vitest: https://vitest.dev/

## Kết Luận

FAQ này cover những câu hỏi phổ biến nhất về Vue.js development. Key takeaways:

1. **Vue 3 is the standard**: Không có lý do gì để bắt đầu project mới với Vue 2.

2. **Composition API is the future**: Learn và embrace Composition API as your primary approach.

3. **Pinia replaces Vuex**: Pinia là state management solution duy nhất cho Vue 3.

4. **Reactivity requires understanding**: Vue's reactivity system là core strength, nhưng cần hiểu cách nó work để tránh common pitfalls.

5. **Performance is tunable**: Most performance issues có specific solutions - analyze trước khi optimize.

6. **Testing is essential**: Invest time in testing infrastructure early - nó pays off over time.

7. **TypeScript is recommended**: TypeScript provides significant benefits for maintainability và developer experience.

8. **Nuxt for full-stack**: Consider Nuxt khi SEO important hoặc need full-stack capabilities.

For questions không covered here, tham khảo official documentation hoặc Vue community resources.
