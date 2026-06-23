---
title: "Vue Anti-Patterns - Các Mẫu Cần Tránh"
description: "Hướng dẫn toàn diện về các anti-patterns phổ biến trong Vue.js development, cách nhận diện và khắc phục chúng"
tags: ["vue", "javascript", "anti-patterns", "best-practices", "frontend"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Vue Anti-Patterns - Các Mẫu Cần Tránh

## Tổng Quan

Tài liệu này cung cấp hướng dẫn chi tiết về các anti-patterns phổ biến trong Vue.js development. Việc nhận diện và tránh các mẫu code không tốt này là yếu tố quan trọng để xây dựng ứng dụng Vue có hiệu suất cao, dễ bảo trì và ít lỗi. Anti-patterns không chỉ ảnh hưởng đến chất lượng code mà còn tác động đến trải nghiệm người dùng và hiệu suất ứng dụng tổng thể.

Trong quá trình phát triển Vue, developers thường mắc phải những sai lầm phổ biến do thiếu hiểu biết sâu về reactivity system, component lifecycle, hoặc do áp dụng các pattern không phù hợp với quy mô dự án. Tài liệu này sẽ giúp bạn nhận diện những vấn đề này và cung cấp giải pháp thay thế tối ưu.

Các anti-patterns được trình bày trong tài liệu này được phân loại theo mức độ nghiêm trọng và tần suất xuất hiện trong các dự án thực tế. Mỗi phần đều bao gồm ví dụ code cụ thể, giải thích tại sao đó là anti-pattern, và hướng dẫn cách khắc phục với best practice đi kèm.

## Mục Đích

Mục đích chính của tài liệu này là giúp các developers:

1. **Nhận diện sớm** các vấn đề tiềm ẩn trong codebase Vue trước khi chúng trở thành technical debt lớn. Việc phát hiện sớm giúp giảm đáng kể thời gian debug và refactoring sau này.

2. **Hiểu nguyên nhân gốc rễ** của mỗi anti-pattern, không chỉ là cách khắc phục bề mặt. Khi hiểu rõ tại sao một pattern là "anti", developers sẽ có khả năng tự nhận diện các vấn đề tương tự trong tương lai.

3. **Áp dụng giải pháp tối ưu** phù hợp với context và yêu cầu cụ thể của dự án. Không phải giải pháp nào cũng phù hợp cho mọi tình huống, và tài liệu này cung cấp guidance để lựa chọn đúng.

4. **Xây dựng văn hóa code review** hiệu quả hơn thông qua việc có một bộ tiêu chuẩn rõ ràng về những gì nên và không nên làm trong Vue development.

## Key Concepts

### 1. Reactivity System Fundamentals

Vue's reactivity system là trái tim của framework, nhưng nó cũng là nguồn của nhiều anti-patterns nếu không hiểu rõ cách nó hoạt động. Vue 3 sử dụng ES Proxy để track dependencies và trigger updates tự động. Điều quan trọng cần nhớ là reactivity chỉ hoạt động khi giá trị được truy cập thông qua reactive proxy.

Khi destructuring một reactive object, các refs được tạo ra sẽ mất connection với original reactive object, dẫn đến mất reactivity. Đây là một trong những lỗi phổ biến nhất mà developers mới làm quen với Vue 3 mắc phải.

```typescript
// Anti-pattern: Destructuring làm mất reactivity
const user = reactive({ name: 'John', age: 30 })
const { name, age } = user // name và age không còn reactive

// Best Practice: Sử dụng toRefs để preserve reactivity
const user = reactive({ name: 'John', age: 30 })
const { name, age } = toRefs(user)
// Hoặc truy cập trực tiếp
const name = computed(() => user.name)
```

### 2. Component Communication Patterns

Vue cung cấp nhiều cách để components communicate với nhau, và việc chọn sai pattern có thể dẫn đến code khó bảo trì và bug. Parent-child communication nên sử dụng props và emits, trong khi sibling communication nên thông qua shared state (Pinia store) hoặc provide/inject cho hierarchical data.

Props trong Vue là one-way data flow by design. Child components không nên modify props received từ parent. Việc mutate props trực tiếp vi phạm nguyên tắc này và tạo ra các bug khó debug liên quan đến data flow.

```vue
<!-- Anti-pattern: Mutating props -->
<script setup>
const props = defineProps<{ count: number }>()
// Vi phạm: modify prop trực tiếp
props.count = props.count + 1
</script>

<!-- Best Practice: Emit event để parent xử lý -->
<script setup>
const props = defineProps<{ count: number }>()
const emit = defineEmits<{
  'update:count': [value: number]
}>()

const increment = () => {
  emit('update:count', props.count + 1)
}
</script>
```

### 3. Performance Considerations

Vue's virtual DOM là một optimization layer giúp minimize actual DOM manipulations, nhưng developers có thể vô hiệu hóa benefits này thông qua các anti-patterns. Unnecessary re-renders là vấn đề phổ biến nhất ảnh hưởng đến performance của Vue applications.

Mỗi component trong Vue đều có own reactive state và computed properties. Khi state thay đổi, Vue sẽ re-render component đó và tất cả children của nó (trừ khi được memoized hoặc optimized). Việc không tận dụng các optimization techniques có thể dẫn đến performance issues nghiêm trọng trong các ứng dụng lớn.

## Common Anti-Patterns

### 1. Mutating Props Directly

**Mô Tả**: Đây là một trong những anti-patterns phổ biến và nguy hiểm nhất trong Vue development. Khi một child component modify props nhận được từ parent, nó tạo ra một data flow phức tạp và khó theo dõi.

**Tại Sao Đây Là Vấn Đề**:

- Vi phạm nguyên tắc one-way data flow của Vue
- Tạo ra race conditions và unpredictable behavior
- Làm cho debugging trở nên rất khó khăn vì không rõ data thay đổi ở đâu
- Có thể gây ra infinite loops trong một số trường hợp
- Không hoạt động đúng trong Strict Mode

**Ví Dụ Anti-Pattern**:

```vue
<script setup lang="ts">
// Anti-pattern Component
const props = defineProps<{
  initialCount: number
}>()

// Lỗi: Đang modify prop trực tiếp
props.initialCount = props.initialCount + 1

// Hoặc worse - sử dụng watch để mutate
watch(() => props.initialCount, (newVal) => {
  props.initialCount = newVal + 1 // Sai hoàn toàn!
})
</script>
```

**Best Practice Solutions**:

```vue
<script setup lang="ts">
import { ref, watch } from 'vue'

// Solution 1: Sử dụng local state với initial value từ prop
const props = defineProps<{
  initialCount: number
}>()

const count = ref(props.initialCount)

// Solution 2: Sử dụng v-model với .sync modifier hoặc modelValue
const count = defineModel<number>({ default: 0 })

// Solution 3: Emit event để parent xử lý
const emit = defineEmits<{
  'update:count': [value: number]
}>()

const increment = () => {
  emit('update:count', count.value + 1)
}
</script>
```

**Real-World Scenario**:

Trong một ứng dụng thực tế, giả sử bạn có một component `UserProfile` nhận prop `user` từ parent. Nếu bạn modify `user.name` trong child component, parent sẽ không biết về thay đổi này và có thể gửi stale data lên server khi save.

```typescript
// Anti-pattern trong thực tế
const UserProfile = defineComponent({
  props: {
    user: Object
  },
  setup(props) {
    // BAD: Đang modify object được pass by reference
    const updateName = (newName: string) => {
      props.user.name = newName // Vi phạm!
    }
  }
})

// Best practice
const UserProfile = defineComponent({
  props: {
    modelValue: Object // Sử dụng v-model pattern
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const updateName = (newName: string) => {
      emit('update:modelValue', {
        ...props.modelValue,
        name: newName
      })
    }
  }
})
```

### 2. Missing Key in v-for

**Mô Tả**: Sử dụng `v-for` mà không có `:key` attribute hoặc sử dụng key không unique là một anti-pattern phổ biến dẫn đến performance issues và incorrect DOM updates.

**Tại Sao Đây Là Vấn Đề**:

- Vue không thể track individual items, dẫn đến incorrect reuses của DOM nodes
- Animation transitions không hoạt động đúng
- State của các items có thể bị mixed up
- Performance degradation với large lists
- Potential bugs khi items được added, removed, hoặc reordered

**Ví Dụ Anti-Pattern**:

```vue
<template>
  <!-- Anti-pattern 1: Không có key -->
  <div v-for="item in items">
    {{ item.name }}
  </div>

  <!-- Anti-pattern 2: Sử dụng index làm key (BAD trong hầu hết cases) -->
  <div v-for="(item, index) in items" :key="index">
    {{ item.name }}
  </div>

  <!-- Anti-pattern 3: Key không unique -->
  <div v-for="item in items" :key="item.category">
    <!-- BAD nếu multiple items cùng category -->
    {{ item.name }}
  </div>
</template>
```

**Best Practice Solutions**:

```vue
<template>
  <!-- Best Practice: Luôn sử dụng unique, stable key -->
  <div v-for="item in items" :key="item.id">
    {{ item.name }}
  </div>

  <!-- Khi cần index như một phần của key -->
  <div v-for="(item, index) in items" :key="`${item.id}-${index}`">
    <!-- Chỉ khi thực sự cần, ví dụ: có duplicate IDs -->
  </div>
</template>
```

**When Index Key Is Acceptable**:

Trong một số trường hợp hiếm hoi, index làm key có thể chấp nhận được:

```vue
<template>
  <!-- Khi danh sách là static, không thay đổi -->
  <option v-for="(city, index) in staticCities" :key="index">
    {{ city }}
  </option>

  <!-- Khi items không có unique identifier và không có side effects -->
  <li v-for="(item, index) in pureDisplayItems" :key="index">
    {{ item }}
  </li>
</template>
```

### 3. Abusing $refs

**Mô Tả**: `$refs` trong Vue cung cấp direct access đến DOM elements hoặc child component instances. Tuy nhiên, overusing hoặc misusing `$refs` là một anti-pattern phổ biến.

**Tại Sao Đây Là Vấn Đề**:

- Tạo ra tight coupling giữa components
- Vi phạm encapsulation principle
- Code trở nên khó test
- Fragile - breaks khi component structure thay đổi
- Không reactive - không trigger re-renders

**Ví Dụ Anti-Pattern**:

```vue
<script setup>
import { ref } from 'vue'

// Anti-pattern: Sử dụng $refs để control child state
const childRef = ref(null)

const resetChild = () => {
  childRef.value.reset() // Child component phải expose method này
  childRef.value.data = [] // Bad: direct state access
}

const focusInput = () => {
  childRef.value.$el.querySelector('input').focus() // Too fragile
}
</script>

<template>
  <ChildComponent ref="childRef" />
</template>
```

**Best Practice Solutions**:

```vue
<script setup>
import { ref, onMounted } from 'vue'

// Solution 1: Sử dụng template refs cho DOM elements (acceptable)
const inputRef = ref<HTMLInputElement | null>(null)

const focusInput = () => {
  inputRef.value?.focus()
}

// Solution 2: Sử dụng expose để control child component
const childRef = ref(null)

const resetChild = async () => {
  await childRef.value?.reset()
}
</script>

<template>
  <!-- DOM ref - acceptable use case -->
  <input ref="inputRef" type="text" />

  <!-- Component ref - only when necessary, through exposed methods -->
  <FormComponent ref="childRef" />
</template>
```

**Child Component Expose Pattern**:

```vue
<!-- ChildComponent.vue -->
<script setup>
import { ref } from 'vue'

const data = ref([])
const internalReset = () => {
  data.value = []
}

// Expose only what parent needs
defineExpose({
  reset: internalReset,
  // Tránh expose internal state
})
</script>
```

### 4. Memory Leaks in Vue Applications

**Mô Tả**: Memory leaks trong Vue applications thường xảy ra khi event listeners, timers, hoặc subscriptions không được cleanup đúng cách khi components unmount.

**Tại Sao Đây Là Vấn Đề**:

- Performance degradation theo thời gian
- Application crash sau khi sử dụng lâu
- Increased memory usage có thể crash browser tabs
- Hard để debug - symptoms xuất hiện lâu sau khi leak tạo ra

**Common Sources Of Memory Leaks**:

```typescript
// Anti-pattern 1: Không cleanup event listeners
import { onMounted } from 'vue'

onMounted(() => {
  window.addEventListener('resize', handleResize)
  // Lỗi: Không remove listener khi unmount
})

// Anti-pattern 2: Không clear intervals
onMounted(() => {
  setInterval(() => {
    fetchData()
  }, 5000)
  // Lỗi: Interval tiếp tục chạy sau khi component unmount
})

// Anti-pattern 3: Không unsubscribe from observables
onMounted(() => {
  subscription = someObservable.subscribe(data => {
    this.data = data
  })
  // Lỗi: Subscription vẫn active sau unmount
})
```

**Best Practice Solutions**:

```typescript
import { onMounted, onUnmounted, ref } from 'vue'

// Solution 1: Sử dụng onUnmounted cho cleanup
const handleResize = () => { /* ... */ }

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

// Solution 2: Sử dụng onBeforeUnmount
onMounted(() => {
  const intervalId = setInterval(() => {
    fetchData()
  }, 5000)

  onBeforeUnmount(() => {
    clearInterval(intervalId)
  })
})

// Solution 3: Sử dụng composables với automatic cleanup
import { onMounted, onUnmounted } from 'vue'
import { useInterval } from '@/composables/useInterval'

export function useInterval(callback: () => void, interval: number) {
  const intervalId = ref<number | null>(null)

  onMounted(() => {
    intervalId.value = window.setInterval(callback, interval)
  })

  onUnmounted(() => {
    if (intervalId.value !== null) {
      clearInterval(intervalId.value)
    }
  })
}
```

**Advanced Cleanup Patterns**:

```typescript
// Composable với full cleanup support
export function useEventListener<K extends keyof WindowEventMap>(
  event: K,
  handler: (event: WindowEventMap[K]) => void
) {
  onMounted(() => {
    window.addEventListener(event, handler)
  })

  onUnmounted(() => {
    window.removeEventListener(event, handler)
  })
}

// Composable với abort controller pattern
export function useFetch<T>(url: string) {
  const data = ref<T | null>(null)
  const error = ref<Error | null>(null)
  const abortController = new AbortController()

  onMounted(async () => {
    try {
      const response = await fetch(url, {
        signal: abortController.signal
      })
      data.value = await response.json()
    } catch (e) {
      if (e instanceof Error && e.name !== 'AbortError') {
        error.value = e
      }
    }
  })

  onUnmounted(() => {
    abortController.abort()
  })

  return { data, error }
}
```

### 5. Improper Reactivity

**Mô Tả**: Vue's reactivity system là powerful nhưng có những gotchas mà developers cần hiểu để tránh unexpected behavior.

**Common Reactivity Pitfalls**:

```typescript
// Pitfall 1: Replacing entire reactive object
const state = reactive({ count: 0, name: 'John' })

// BAD: Replace reference, loses reactivity
state = reactive({ count: 1, name: 'Jane' })

// GOOD: Mutate properties
state.count = 1
state.name = 'Jane'

// Hoặc assign nested object
Object.assign(state, { count: 1, name: 'Jane' })

// Pitfall 2: Array index assignment
const list = reactive([1, 2, 3])

// BAD: Index assignment không reactive
list[0] = 10

// GOOD: Use array methods
list.splice(0, 1, 10)
// Hoặc replace entire array
list = reactive([10, 2, 3])

// Pitfall 3: Adding new properties to reactive object
const state = reactive({ name: 'John' })

// BAD: New property không reactive
state.age = 30

// GOOD: Use spread or Object.assign
const newState = reactive({ ...state, age: 30 })
// Hoặc
Object.assign(state, { age: 30 })
```

**Best Practices for Reactivity**:

```typescript
import { reactive, ref, computed, watch } from 'vue'

// Use ref for primitives and objects you want to replace
const count = ref(0)
count.value++

// Use reactive for objects you mutate
const user = reactive({
  name: 'John',
  profile: {
    age: 30,
    city: 'NYC'
  }
})

// Nested reactive objects are automatically tracked
user.profile.age = 31 // Reactive

// For arrays, use ref or ensure reassignment
const items = ref([1, 2, 3])
items.value = [...items.value.slice(0, 1), 10, ...items.value.slice(2)]

// For complex state, consider using reactive with careful mutation
const form = reactive({
  fields: {} as Record<string, string>
})

// Adding dynamic properties - use set or replace
watch(() => form.fields, (newFields) => {
  // React properly
}, { deep: true })
```

### 6. Side Effects in Computed Properties

**Mô Tả**: Computed properties trong Vue được thiết kế để be pure derived state calculations. Thực hiện side effects (API calls, DOM manipulation, state mutations) trong computed properties là anti-pattern.

**Tại Sao Đây Là Vấn Đề**:

- Computed properties có thể execute multiple times và bất cứ khi nào dependencies thay đổi
- Side effects có thể trigger infinite loops
- Computed properties có thể be called during SSR where certain APIs aren't available
- Behavior becomes unpredictable và hard to debug
- Violates principle of pure functions

**Ví Dụ Anti-Pattern**:

```typescript
import { ref, computed } from 'vue'

const userId = ref(1)

// Anti-pattern: Side effect trong computed
const user = computed(async () => {
  const response = await fetch(`/api/users/${userId.value}`)
  return response.json()
  // Lỗi: async operation trong computed không reactive đúng cách
})

// Anti-pattern: DOM manipulation
const elementRef = ref<HTMLElement | null>(null)
const data = ref('some data')

const processedData = computed(() => {
  if (elementRef.value) {
    elementRef.value.textContent = data.value.toUpperCase()
    // Lỗi: Side effect trong computed
  }
  return data.value.toUpperCase()
})

// Anti-pattern: Mutating external state
const counter = ref(0)
const multiplier = ref(2)

const result = computed(() => {
  const r = counter.value * multiplier.value
  counter.value = r // Lỗi: Side effect!
  return r
})
```

**Best Practice Solutions**:

```typescript
import { ref, computed, watch } from 'vue'

// Solution 1: Sử dụng watchEffect hoặc watch cho side effects
const userId = ref(1)
const user = ref(null)

watchEffect(async () => {
  try {
    const response = await fetch(`/api/users/${userId.value}`)
    user.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch user:', error)
  }
})

// Solution 2: Sử dụng async composable pattern
const useUser = (id: Ref<number>) => {
  const user = ref(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const fetchUser = async () => {
    loading.value = true
    try {
      const response = await fetch(`/api/users/${id.value}`)
      user.value = await response.json()
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  }

  watch(id, fetchUser, { immediate: true })

  return { user, loading, error, refetch: fetchUser }
}

// Solution 3: Computed chỉ cho pure calculations
const items = ref([1, 2, 3, 4, 5])
const filter = ref('')

const filteredItems = computed(() => {
  // Pure computation - no side effects
  if (!filter.value) return items.value
  return items.value.filter(item =>
    item.toString().includes(filter.value)
  )
})
```

### 7. Overusing Watchers

**Mô Tả**: Watchers trong Vue là powerful nhưng developers thường overuses chúng khi computed properties sẽ là lựa chọn tốt hơn.

**Tại Sao Nên Prefer Computed**:

- Computed properties are automatically cached và chỉ re-evaluate khi dependencies thay đổi
- Computed properties are more declarative và easier to reason about
- Watchers execute on every change, computed only when needed
- Computed properties integrate better với Vue's reactivity system

**Ví Dụ Anti-Pattern**:

```typescript
import { ref, watch } from 'vue'

const firstName = ref('')
const lastName = ref('')
const fullName = ref('')

// Anti-pattern: Watch thay vì computed
watch([firstName, lastName], ([newFirst, newLast]) => {
  fullName.value = `${newFirst} ${newLast}`
})

// Worse: Watch với immediate và deep options
const user = ref({ profile: { name: '' } })
watch(user, (newUser) => {
  user.value.profile.name = newUser.profile.name.toUpperCase()
}, { deep: true, immediate: true })
```

**Best Practice Solutions**:

```typescript
import { ref, computed } from 'vue'

const firstName = ref('')
const lastName = ref('')

// Best Practice: Computed cho derived state
const fullName = computed(() => `${firstName.value} ${lastName.value}`)

// Watch chỉ khi thực sự cần side effects
watch(fullName, (newFullName) => {
  // Side effect như save to localStorage
  localStorage.setItem('fullName', newFullName)
})

// Watch khi cần perform async operations
const searchQuery = ref('')
const searchResults = ref([])

watch(searchQuery, async (query) => {
  if (query.length > 2) {
    const results = await searchAPI(query)
    searchResults.value = results
  }
}, { debounce: 300 } as any) // Consider using debounce composable
```

### 8. Overusing Global State (Pinia/Vuex)

**Mô Tả**: Đưa mọi thứ vào global store là anti-pattern phổ biến. Global state nên được reserved cho state thực sự shared across multiple components.

**Tại Sao Đây Là Vấn Đề**:

- Makes state flow khó theo dõi
- Hard để debug vì state có thể change từ bất cứ đâu
- Performance issues từ unnecessary reactivity
- Store becomes a dumping ground cho mọi thứ
- Hard để test individual components

**Ví Dụ Anti-Pattern**:

```typescript
// BAD: Store chứa quá nhiều responsibilities
export const useStore = defineStore('main', () => {
  const userName = ref('')
  const modalOpen = ref(false)
  const currentTab = ref('home')
  const loadingStates = reactive({})
  const formData = ref({})

  // Tất cả đều không cần thiết phải global
})
```

**Best Practice Solutions**:

```typescript
// GOOD: Separation of concerns
// stores/user.ts - Chỉ user-related global state
export const useUserStore = defineStore('user', () => {
  const profile = ref<User | null>(null)
  const isAuthenticated = computed(() => profile.value !== null)

  const login = async (credentials: Credentials) => {
    // ...
  }

  return { profile, isAuthenticated, login }
})

// composables/useModal.ts - Local state cho UI concerns
export function useModal() {
  const isOpen = ref(false)
  const open = () => isOpen.value = true
  const close = () => isOpen.value = false

  return { isOpen, open, close }
}

// Component sử dụng appropriately
<script setup>
import { useUserStore } from '@/stores/user'
import { useModal } from '@/composables/useModal'

const userStore = useUserStore()
const modal = useModal()
</script>
```

### 9. Not Using Lazy Loading for Routes

**Mô Tả**: Importing all routes eagerly là anti-pattern dẫn đến large initial bundle size và slower Time to Interactive.

**Ví Dụ Anti-Pattern**:

```typescript
import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import About from './views/About.vue'
import Dashboard from './views/Dashboard.vue'
import Settings from './views/Settings.vue'
import Profile from './views/Profile.vue'
import Users from './views/Users.vue'
import UserDetail from './views/UserDetail.vue'
import Products from './views/Products.vue'
import ProductDetail from './views/ProductDetail.vue'
import Checkout from './views/Checkout.vue'
import Orders from './views/Orders.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About },
  { path: '/dashboard', component: Dashboard },
  { path: '/settings', component: Settings },
  { path: '/profile', component: Profile },
  { path: '/users', component: Users },
  { path: '/users/:id', component: UserDetail },
  { path: '/products', component: Products },
  { path: '/products/:id', component: ProductDetail },
  { path: '/checkout', component: Checkout },
  { path: '/orders', component: Orders },
]

// BAD: All routes loaded upfront
```

**Best Practice Solutions**:

```typescript
import { createRouter, createWebHistory } from 'vue-router'

// Lazy load all routes
const routes = [
  {
    path: '/',
    component: () => import('./views/Home.vue')
  },
  {
    path: '/about',
    component: () => import('./views/About.vue')
  },
  {
    path: '/dashboard',
    component: () => import('./views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/users',
    component: () => import('./views/Users.vue'),
    children: [
      {
        path: ':id',
        component: () => import('./views/UserDetail.vue')
      }
    ]
  }
]

// Group related routes for better code splitting
const routes = [
  {
    path: '/shop',
    component: () => import('./layouts/ShopLayout.vue'),
    children: [
      {
        path: 'products',
        component: () => import('./views/Products.vue')
      },
      {
        path: 'products/:id',
        component: () => import('./views/ProductDetail.vue')
      },
      {
        path: 'checkout',
        component: () => import('./views/Checkout.vue')
      }
    ]
  }
]
```

### 10. Inconsistent Component Naming

**Mô Tả**: Không tuân theo naming conventions dẫn đến code khó đọc và maintain, đặc biệt trong team environments.

**Best Practices for Naming**:

```typescript
// Component file naming
// PascalCase cho component files
// UserProfile.vue
// ShoppingCart.vue
// OrderDetails.vue

// Composables naming - use* prefix
// useCounter.ts
// useAuth.ts
// useFetch.ts

// Store naming
// stores/user.ts
// stores/cart.ts
// stores/products.ts

// Constants naming
// ALL_CAPS for constants
// MAX_RETRY_COUNT
// API_BASE_URL

// Variable naming
// camelCase for variables
const userName = 'John'
const isLoading = false

// Boolean variables - use is/has/can prefix
const isActive = true
const hasPermission = true
const canEdit = false
```

## Common Patterns và Solutions

### Template refs vs Reactive State

**When To Use Template Refs**:

```vue
<script setup>
import { ref, onMounted } from 'vue'

// DOM element access
const canvasRef = ref<HTMLCanvasElement | null>(null)
const inputRef = ref<HTMLInputElement | null>(null)

// Component methods access
const formRef = ref<InstanceType<typeof FormComponent> | null>(null)

onMounted(() => {
  // Canvas setup
  if (canvasRef.value) {
    const ctx = canvasRef.value.getContext('2d')
  }

  // Focus management
  inputRef.value?.focus()
})

const submitForm = async () => {
  await formRef.value?.submit()
}
</script>

<template>
  <canvas ref="canvasRef"></canvas>
  <input ref="inputRef" type="text" />
  <FormComponent ref="formRef" />
</template>
```

**When To Use Reactive State**:

```typescript
// For shared state across components
const cartStore = useCartStore()
const cartItems = computed(() => cartStore.items)

// For local component state
const isExpanded = ref(false)
const searchQuery = ref('')

// For form state
const form = reactive({
  email: '',
  password: '',
  rememberMe: false
})
```

### Proper Error Handling

```typescript
// Anti-pattern: Unhandled errors
const loadData = async () => {
  const response = await fetch('/api/data')
  const data = await response.json()
  return data
}

// Best Practice: Comprehensive error handling
import { ref, computed } from 'vue'

interface AsyncState<T> {
  data: T | null
  error: Error | null
  loading: boolean
}

export function useAsync<T>(asyncFn: () => Promise<T>) {
  const state = reactive<AsyncState<T>>({
    data: null,
    error: null,
    loading: false
  })

  const execute = async () => {
    state.loading = true
    state.error = null

    try {
      state.data = await asyncFn()
    } catch (e) {
      state.error = e instanceof Error ? e : new Error('Unknown error')
    } finally {
      state.loading = false
    }
  }

  const isError = computed(() => state.error !== null)

  return { ...toRefs(state), isError, execute }
}

// Usage
const { data: user, loading, error, execute } = useAsync(() =>
  fetch('/api/user').then(r => r.json())
)

onMounted(() => execute())
```

## Troubleshooting

### Debugging Reactivity Issues

```typescript
import { reactive, isProxy, toRaw } from 'vue'

// Check if object is reactive
const state = reactive({ count: 0 })
console.log(isProxy(state)) // true

// Get raw object from reactive
const raw = toRaw(state)
console.log(raw === state) // false

// Watch for deep changes
watch(state, (newState, oldState) => {
  console.log('State changed:', newState)
}, { deep: true })
```

### Performance Profiling

```typescript
// Enable performance marks in development
import { mark, measure } from 'vue'

mark('component-render')
// ... component code
measure('Component Render', 'component-render')

// Use Vue Devtools for timeline analysis
// Use Chrome DevTools Performance tab
// Use vue-ruler for component-level metrics
```

### Common Error Messages và Solutions

**"Avoid mutating a prop directly"**:

```typescript
// Error: Props are readonly
// Solution: Use local copy or emit events
const props = defineProps<{ modelValue: number }>()
const emit = defineEmits<{ 'update:modelValue': [number] }>()

const localValue = ref(props.modelValue)

watch(() => props.modelValue, (v) => {
  localValue.value = v
})

const update = (newVal: number) => {
  localValue.value = newVal
  emit('update:modelValue', newVal)
}
```

**"Computed property was assigned to but it has no setter"**:

```typescript
// Error: Trying to assign to read-only computed
// Solution: Define both getter and setter if needed
const fullName = computed({
  get: () => `${firstName.value} ${lastName.value}`,
  set: (value: string) => {
    const [first, last] = value.split(' ')
    firstName.value = first
    lastName.value = last
  }
})
```

## Examples

### Complete Example: Well-Structured Vue Component

```vue
<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useNotifications } from '@/composables/useNotifications'

interface Props {
  userId: number
  editable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  editable: false
})

const emit = defineEmits<{
  update: [user: Partial<User>]
  delete: [userId: number]
}>()

// Store integration
const userStore = useUserStore()
const notifications = useNotifications()

// Local state
const isLoading = ref(true)
const isEditing = ref(false)
const formData = reactive({
  name: '',
  email: '',
  bio: ''
})

// Computed properties
const user = computed(() =>
  userStore.getUserById(props.userId)
)

const hasUnsavedChanges = computed(() =>
  formData.name !== user.value?.name ||
  formData.email !== user.value?.email ||
  formData.bio !== user.value?.bio
)

// Methods
const startEditing = () => {
  if (!props.editable) return

  formData.name = user.value?.name || ''
  formData.email = user.value?.email || ''
  formData.bio = user.value?.bio || ''
  isEditing.value = true
}

const cancelEditing = () => {
  isEditing.value = false
}

const saveChanges = async () => {
  try {
    await userStore.updateUser(props.userId, formData)
    emit('update', formData)
    notifications.success('User updated successfully')
    isEditing.value = false
  } catch (error) {
    notifications.error('Failed to update user')
  }
}

const confirmDelete = () => {
  if (confirm('Are you sure you want to delete this user?')) {
    emit('delete', props.userId)
  }
}

// Watchers for side effects
watch(() => props.userId, async (newId) => {
  isLoading.value = true
  await userStore.fetchUser(newId)
  isLoading.value = false
}, { immediate: true })

// Lifecycle
onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && isEditing.value) {
    cancelEditing()
  }
}
</script>

<template>
  <div class="user-profile">
    <div v-if="isLoading" class="loading">
      Loading...
    </div>

    <template v-else-if="user">
      <div class="profile-header">
        <img :src="user.avatar" :alt="user.name" class="avatar" />
        <div class="info">
          <h2>{{ user.name }}</h2>
          <p>{{ user.email }}</p>
        </div>
        <button
          v-if="editable && !isEditing"
          @click="startEditing"
        >
          Edit
        </button>
      </div>

      <div v-if="isEditing" class="edit-form">
        <label>
          Name
          <input v-model="formData.name" type="text" />
        </label>
        <label>
          Email
          <input v-model="formData.email" type="email" />
        </label>
        <label>
          Bio
          <textarea v-model="formData.bio"></textarea>
        </label>
        <div class="actions">
          <button @click="cancelEditing">Cancel</button>
          <button
            @click="saveChanges"
            :disabled="!hasUnsavedChanges"
          >
            Save
          </button>
        </div>
      </div>

      <div v-else class="bio">
        {{ user.bio || 'No bio provided' }}
      </div>
    </template>

    <div v-else class="not-found">
      User not found
    </div>
  </div>
</template>

<style scoped>
.user-profile {
  max-width: 600px;
  margin: 0 auto;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
}

.edit-form label {
  display: block;
  margin-bottom: 12px;
}

.edit-form input,
.edit-form textarea {
  width: 100%;
  padding: 8px;
  margin-top: 4px;
}

.actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}
</style>
```

## References

### Official Documentation

- Vue 3 Documentation: https://vuejs.org/
- Vue Router Documentation: https://router.vuejs.org/
- Pinia Documentation: https://pinia.vuejs.org/
- Vue Test Utils Documentation: https://test-utils.vuejs.org/

### Recommended Tools

- Vue DevTools: Browser extension for debugging
- Vite: Fast build tool
- Vitest: Unit testing framework
- Volar: VS Code extension for Vue

### Further Reading

- Vue Design Patterns (O'Reilly)
- Building Vue 3 Applications (Packt)
- Vue.js 3 Design Patterns (Leanpub)

## Kết Luận

Việc tránh các anti-patterns được liệt kê trong tài liệu này là bước quan trọng để xây dựng ứng dụng Vue chất lượng cao. Tuy nhiên, điều quan trọng cần nhớ là không có quy tắc cứng nhắc nào áp dụng cho mọi tình huống. Luôn evaluate context cụ thể của dự án trước khi apply bất kỳ pattern nào.

Key takeaways từ tài liệu này bao gồm:

1. **Mutating props là never acceptable** - luôn sử dụng events hoặc v-model pattern
2. **Key in v-for is mandatory** - sử dụng unique, stable identifiers
3. **$refs should be minimized** - prefer declarative patterns khi possible
4. **Cleanup is critical** - always properly dispose of subscriptions, timers, và event listeners
5. **Computed properties should be pure** - avoid side effects
6. **Prefer computed over watch** - cho derived state
7. **Global state should be minimal** - chỉ use cho cross-component state thực sự
8. **Lazy load routes** - improve initial load performance

Bằng cách áp dụng các nguyên tắc và best practices trong tài liệu này, bạn sẽ có thể viết Vue code clean, maintainable, và high-performance.
