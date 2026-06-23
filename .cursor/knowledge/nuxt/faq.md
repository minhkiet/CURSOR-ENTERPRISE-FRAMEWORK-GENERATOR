# Nuxt.js FAQ - Câu Hỏi Thường Gặp

## Mục lục
1. [General](#1-general)
2. [Data Fetching](#2-data-fetching)
3. [State Management](#3-state-management)
4. [Routing](#4-routing)
5. [Server Routes](#5-server-routes)
6. [Performance](#6-performance)

---

## 1. General

### Q1: Nuxt 3 vs Nuxt 2 - Nên chọn cái nào?

**A:** **Nuxt 3 là lựa chọn khuyến nghị:**

| Aspect | Nuxt 2 | Nuxt 3 |
|--------|--------|--------|
| Vue Version | Vue 2 | Vue 3 |
| TypeScript | Partial | Full support |
| Performance | Good | Significantly better |
| Server Engine | Express | Nitro |
| Module System | Legacy | Modern |
| State | Vuex | Pinia/Composition API |
| Bundle Size | Larger | 60% smaller |
| Maintenance | Security fixes only | Active development |

**Khuyến nghị**: Sử dụng Nuxt 3 cho tất cả projects mới.

---

### Q2: Sự khác nhau giữa nuxt generate và nuxt build?

**A:**

| Command | Purpose | Output |
|---------|---------|--------|
| `nuxt generate` | Static site generation | Pre-rendered HTML |
| `nuxt build` | SSR/SPA build | Node.js server |

```bash
# Static generation (SSG)
nuxt generate

# SSR/SPA deployment
nuxt build
node .output/server/index.mjs
```

---

### Q3: Làm thế nào để debug Nuxt applications?

**A:** Multiple methods available:

**1. Vue DevTools**
```bash
# Install Nuxt DevTools
npx nuxi@latest devtools enable
```

**2. Nuxt DevTools Dashboard**
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  devtools: { enabled: true }
});
```

**3. Console Logging**
```vue
<script setup>
const nuxtApp = useNuxtApp();
console.log(nuxtApp.payload);
console.log(nuxtApp.isHydrating);
</script>
```

**4. Server-side debugging**
```typescript
// server/api/debug.ts
export default defineEventHandler(async (event) => {
  console.log('Request headers:', getHeaders(event));
  console.log('Query:', getQuery(event));
  return { success: true };
});
```

---

## 2. Data Fetching

### Q4: useFetch và useAsyncData khác nhau thế nào?

**A:**

| Aspect | useFetch | useAsyncData |
|--------|----------|--------------|
| Syntax | Simpler | More verbose |
| Auto key | Yes (from URL) | No (manual) |
| HTTP methods | Easy to change | Manual |
| Type inference | Automatic | Manual with generic |
| Best for | Simple requests | Complex logic |

```vue
<script setup>
// useFetch - simpler
const { data } = await useFetch('/api/users');

// useAsyncData - more control
const { data } = await useAsyncData('users', () => 
  $fetch('/api/users')
);
</script>
```

---

### Q5: Làm thế nào để revalidate data?

**A:** Multiple ways:

**1. Refresh function**
```vue
<script setup>
const { data, refresh } = await useFetch('/api/users');

function reload() {
  refresh();
}
</script>
```

**2. Manual revalidation**
```vue
<script setup>
const { data, refresh } = await useAsyncData('users', () => 
  $fetch('/api/users')
);

// After mutation
async function deleteUser(id: string) {
  await $fetch(`/api/users/${id}`, { method: 'DELETE' });
  refresh(); // Revalidate
}
</script>
```

**3. Auto-refresh với refreshInterval**
```vue
<script setup>
const { data } = await useFetch('/api/stats', {
  refreshInterval: 30000, // 30 seconds
});
</script>
```

---

### Q6: Tại sao data không có sẵn trong component?

**A:** Common causes:

**1. Not awaited**
```vue
<script setup>
// ❌ Wrong
const { data } = useFetch('/api/users');

console.log(data.value); // undefined!

// ✅ Correct
const { data } = await useFetch('/api/users');

console.log(data.value); // available!
</script>
```

**2. Fetching in components instead of pages**
```vue
<!-- ❌ Bad: Fetching in child component -->
<template>
  <div>{{ data }}</div>
</template>

<script setup>
const { data } = await useFetch('/api/data');
// This runs on server, but parent may not wait
</script>

<!-- ✅ Better: Fetch in page, pass as prop -->
<template>
  <ChildComponent :data="data" />
</template>

<script setup>
const { data } = await useFetch('/api/data');
</script>
```

---

## 3. State Management

### Q7: Khi nào nên dùng useState vs Pinia?

**A:**

| Scenario | Solution |
|----------|----------|
| Simple primitive value | useState |
| Cross-component primitive | useState |
| Complex object state | Pinia |
| State with actions | Pinia |
| DevTools needed | Pinia |
| SSR-safe simple state | useState |

```vue
<script setup>
// Simple: useState
const count = useState('count', () => 0);
const isOpen = useState('isOpen', () => false);

// Complex: Pinia
const cartStore = useCartStore();
</script>
```

---

### Q8: Làm thế nào để persist state qua page reloads?

**A:** Multiple approaches:

**1. useCookie (for simple values)**
```vue
<script setup>
const theme = useCookie('theme', {
  default: () => 'light',
});

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
}
</script>
```

**2. Pinia with persistence plugin**
```typescript
// stores/cart.ts
import { defineStore } from 'pinia';

export const useCartStore = defineStore('cart', {
  state: () => ({ items: [] }),
  persist: true, // Requires pinia-plugin-persistedstate
});
```

**3. LocalStorage (client-only)**
```vue
<script setup>
const stored = localStorage.getItem('preferences');
const preferences = ref(stored ? JSON.parse(stored) : {});

watch(preferences, (val) => {
  localStorage.setItem('preferences', JSON.stringify(val));
}, { deep: true });
</script>
```

---

### Q9: useState vs ref - khi nào dùng cái nào?

**A:**

| Feature | useState | ref |
|---------|----------|-----|
| SSR-safe | Yes | No |
| Shared across components | Yes | No |
| Serialized to payload | Yes | No |
| Simple syntax | Yes | Yes |
| Type support | Full | Full |

```vue
<script setup>
// Local-only, simple - use ref
const count = ref(0);
const message = ref('');

// Shared, SSR - use useState
const user = useState('user', () => null);
const cart = useState('cart', () => []);
</script>
```

---

## 4. Routing

### Q10: Làm thế nào để protected routes?

**A:** Use route middleware:

**1. Create middleware**
```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const user = useUser();
  
  if (!user.isAuthenticated) {
    return navigateTo({
      path: '/login',
      query: { redirect: to.fullPath },
    });
  }
});
```

**2. Apply to pages**
```vue
<script setup>
definePageMeta({
  middleware: 'auth',
});
</script>
```

**3. Apply globally (optional)**
```typescript
// middleware/auth.global.ts
export default defineNuxtRouteMiddleware((to) => {
  // Runs on every route
});
```

---

### Q11: Dynamic routes hoạt động như thế nào?

**A:** File-based routing với square brackets:

```
pages/
├── users/[id].vue         → /users/:id
├── users/[id]/posts.vue    → /users/:id/posts
├── [...slug].vue           → /* (catch-all)
└── [[slug]].vue            → / or /* (optional catch-all)
```

```vue
<!-- pages/users/[id].vue -->
<script setup>
const route = useRoute();
const userId = route.params.id; // Access param

const { data: user } = await useFetch(`/api/users/${userId}`);
</script>
```

---

### Q12: Nested routes với layouts?

**A:** Structure pages nested in directories:

```
pages/
├── users.vue              # Parent - defines layout
│   └── <NuxtPage />       # Renders child pages
├── users/
│   ├── index.vue          # /users - default child
│   └── [id].vue           # /users/:id - specific child
└── dashboard.vue          # Separate layout
```

```vue
<!-- pages/users.vue -->
<template>
  <div class="user-layout">
    <UserSidebar />
    <NuxtPage />  <!-- Child pages render here -->
  </div>
</template>
```

---

## 5. Server Routes

### Q13: Làm thế nào để validate request body?

**A:** Using Zod:

```typescript
// server/api/users/index.post.ts
import { z } from 'zod';

const createUserSchema = z.object({
  name: z.string().min(2, 'Tên phải có ít nhất 2 ký tự'),
  email: z.string().email('Email không hợp lệ'),
  age: z.number().min(18).optional(),
});

export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  
  const result = createUserSchema.safeParse(body);
  
  if (!result.success) {
    throw createError({
      statusCode: 400,
      message: result.error.issues[0].message,
    });
  }
  
  return db.user.create({ data: result.data });
});
```

---

### Q14: Làm thế nào để handle errors trong server routes?

**A:** Use createError and handle properly:

```typescript
export default defineEventHandler(async (event) => {
  try {
    const user = await db.user.findUnique({
      where: { id: getRouterParam(event, 'id') },
    });
    
    if (!user) {
      throw createError({
        statusCode: 404,
        message: 'User not found',
      });
    }
    
    return { user };
    
  } catch (error) {
    // Re-throw Nuxt errors
    if (error.statusCode) throw error;
    
    // Log and wrap other errors
    console.error('Server error:', error);
    throw createError({
      statusCode: 500,
      message: 'Internal server error',
    });
  }
});
```

---

### Q15: Làm thế nào để access database trong server routes?

**A:** Multiple patterns:

**1. Prisma (recommended)**
```typescript
// server/utils/db.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export { prisma };

// server/api/users/index.get.ts
import { prisma } from '~/server/utils/db';

export default defineEventHandler(async () => {
  return prisma.user.findMany();
});
```

**2. Drizzle**
```typescript
import { db } from '~/server/utils/db';
import { users } from '~/server/utils/schema';

export default defineEventHandler(async () => {
  return db.select().from(users);
});
```

---

## 6. Performance

### Q16: Làm thế nào để improve SSR performance?

**A:** Several strategies:

**1. Use routeRules for hybrid rendering**
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    '/': { prerender: true },
    '/blog/**': { swr: 3600 },
    '/dashboard/**': { ssr: false },
  },
});
```

**2. Optimize data fetching**
```vue
<script setup>
// Select only needed fields
const { data } = await useFetch('/api/user', {
  pick: ['id', 'name', 'email'],
});
</script>
```

**3. Lazy load components**
```vue
<script setup>
const HeavyChart = defineAsyncComponent(() => 
  import('~/components/HeavyChart.vue')
);
</script>
```

---

### Q17: Tại sao bundle size lớn và làm thế nào để reduce?

**A:** Common causes:

**1. Too many modules**
```typescript
// nuxt.config.ts - install only what you need
modules: [
  '@pinia/nuxt',
  '@vueuse/nuxt',
  // Don't add unused modules
],
```

**2. Large dependencies**
```typescript
// ❌ Import entire library
import _ from 'lodash';

// ✅ Import specific functions
import debounce from 'lodash/debounce';
```

**3. Not lazy loading routes**
```typescript
// Nuxt lazy loads routes by default
// But large pages should split manually
```

**4. Analyze bundle**
```bash
npx nuxi analyze
```

---

### Q18: ISR vs SSR - khi nào dùng cái nào?

**A:**

| Mode | When Data Updated | Best For |
|------|-------------------|----------|
| SSR | Every request | User-specific, real-time |
| ISR (SWR) | Periodically cached | Frequently updated, shared content |
| Prerender | Build time | Static content, SEO |
| SPA | Client-only | Dashboards, apps |

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    // SSR - always fresh
    '/profile/**': { ssr: true },
    
    // ISR - cached, revalidates every hour
    '/blog/**': { swr: 3600 },
    
    // Prerendered
    '/about': { prerender: true },
    
    // SPA - client-side only
    '/dashboard/**': { ssr: false },
  },
});
```

---

## Liên kết liên quan
- [Nuxt Glossary](./glossary.md)
- [Nuxt Architecture](./architecture.md)
- [Nuxt Best Practices](./best-practice.md)
- [Nuxt Anti-Patterns](./anti-pattern.md)
- [Nuxt Checklist](./checklist.md)
- [Nuxt Decision Tree](./decision-tree.md)
