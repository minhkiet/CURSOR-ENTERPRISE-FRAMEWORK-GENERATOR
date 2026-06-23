# Nuxt Glossary - Từ Điển Thuật Ngữ Nuxt.js

## Giới thiệu

Tài liệu này cung cấp danh sách đầy đủ các thuật ngữ chuyên ngành Nuxt.js, framework Vue.js full-stack.

## Các thuật ngữ cơ bản

### 1. Nuxt Module

Nuxt Module là extension point cho Nuxt, cho phép extend core functionality. Modules được install như npm packages và configure trong nuxt.config.ts. Popular modules: @nuxtjs/tailwindcss, @nuxt/image, @nuxt/content, @nuxt/auth. Modules có access đến Nuxt hooks và có thể modify build process.

Module installation: npm install @nuxt/module. Configuration trong nuxt.config.ts modules array. Modules có thể provide components, composables, và plugins automatically.

### 2. Nuxt Server Routes

Server Routes cho phép tạo API endpoints trong Nuxt app. Files trong server/api/ tự động become API routes. Hỗ trợ REST methods: GET, POST, PUT, DELETE. Auto-imported utilities for database access. H3 library cung cấp HTTP utilities.

Server routes có access đến Nuxt context và có thể use Nitro features. Typed API routes với useTypedRouter. Middleware for auth, validation.

### 3. useAsyncData

useAsyncData là composable fetch và cache data trong SSR context. Auto-prevents duplicate requests. Returns: data, pending, error, refresh. Key parameter xác định cache uniqueness. watch option for reactive refetching.

```typescript
const { data, pending, error, refresh } = await useAsyncData('key', () => $fetch('/api/data'))
```

### 4. useFetch

useFetch là wrapper around useAsyncData với $fetch. Auto-generates key based on URL. Provides post-processing transform. Supports typescript inference.

```typescript
const { data } = await useFetch('/api/users')
```

### 5. NuxtLink

NuxtLink là component for client-side navigation. Auto prefetches linked pages. Active class cho current page. Customizable behavior với props.

### 6. layouts/

layouts/ directory chứa page layouts. default.vue là layout mặc định. Named layouts sử dụng layout prop. Layouts wrap page content.

### 7. pages/

pages/ directory tự động tạo routes. File-based routing. Dynamic segments với _.vue. Nested routes với parent/child files.

### 8. middleware/

middleware/ directory chứa navigation guards. Global middleware chạy trên every navigation. Named middleware applied to specific pages. Redirect và navigation control.

### 9. composables/

composables/ directory auto-imports composables. Vue Composition API functions. Shared logic across components. TypeScript support.

### 10. plugins/

plugins/ directory chứa Vue plugins. Run trên app initialization. Browser-only, server-only, hoặc universal. Add global functionality.

### 11. server/

server/ directory chứa server-side code. api/ cho REST endpoints. utils/ cho server utilities. middleware/ cho server middleware.

### 12. useState

useState tạo reactive state được shared across components. SSR-safe vì serialized between server và client. Global state management pattern.

```typescript
const count = useState('count', () => 0)
```

### 13. auto-imports

Auto-imports là feature tự động import Vue APIs và Nuxt composables. Components trong components/ auto-imported. Composables trong composables/ auto-imported. Utils trong utils/ auto-imported.

### 14. useRuntimeConfig

useRuntimeConfig truy cập runtime configuration. Public config có thể accessed by client. Private config server-only. Environment variables integration.

### 15. NuxtApp Instance

NuxtApp là root Vue application instance. Access qua useNuxtApp(). Hooks system cho lifecycle events. Provides context cho composables.

### 16. Nuxt Hooks

Nuxt Hooks là lifecycle events có thể hook vào. Hook into build, render, router events. Used by modules và custom code.

### 17. Data Fetching

Nuxt cung cấp multiple data fetching patterns: useFetch, useAsyncData, useLazyFetch, useLazyAsyncData. SSR-aware với hydration.

### 18. State Management

State management options in Nuxt: useState (built-in), Pinia (recommended), Vuex (legacy). useState SSR-safe.

## Kết luận

Từ điển này cung cấp nền tảng về Nuxt.js concepts.
