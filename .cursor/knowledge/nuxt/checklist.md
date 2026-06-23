# Nuxt.js Checklist - Danh Sách Kiểm Tra

## Mục lục
1. [Project Setup](#1-project-setup)
2. [Configuration](#2-configuration)
3. [Data Fetching](#3-data-fetching)
4. [State Management](#4-state-management)
5. [Components](#5-components)
6. [Server Routes](#6-server-routes)
7. [Routing](#7-routing)
8. [Performance](#8-performance)
9. [Security](#9-security)
10. [Deployment](#10-deployment)

---

## 1. Project Setup

### 1.1 Initial Setup

- [ ] Sử dụng `npx nuxi@latest init` để tạo project
- [ ] Cài đặt TypeScript
- [ ] Cấu hình ESLint và Prettier
- [ ] Cài đặt essential modules:
  - [ ] @pinia/nuxt (state management)
  - [ ] @vueuse/nuxt (composables)
  - [ ] @nuxt/image (image optimization)

### 1.2 TypeScript Configuration

- [ ] Strict mode enabled
- [ ] Path aliases configured
- [ ] Type declarations for modules

### 1.3 Git Configuration

- [ ] .gitignore includes:
  - [ ] .nuxt/
  - [ ] .output/
  - [ ] node_modules/
  - [ ] .env

---

## 2. Configuration

### 2.1 nuxt.config.ts

- [ ] app.head configured
- [ ] css configured
- [ ] modules configured
- [ ] runtimeConfig properly set:
  - [ ] Server-only secrets
  - [ ] Public variables
- [ ] routeRules configured for production

### 2.2 Environment Variables

- [ ] .env.example created
- [ ] Sensitive variables in .env (not committed)
- [ ] Public variables with NUXT_PUBLIC_ prefix

### 2.3 DevTools

- [ ] DevTools enabled in development
- [ ] TypeScript strict mode

---

## 3. Data Fetching

### 3.1 useFetch Usage

- [ ] Always awaited in pages
- [ ] Proper error handling
- [ ] Loading states implemented
- [ ] Type-safe with generics

### 3.2 useAsyncData Usage

- [ ] Unique cache keys
- [ ] Transformations when needed
- [ ] pick option for partial data
- [ ] TTL configured for caching

### 3.3 Error Handling

- [ ] Loading states (v-if="pending")
- [ ] Error states (v-else-if="error")
- [ ] Error boundary with error.vue
- [ ] Retry mechanism

### 3.4 SSR Considerations

- [ ] Data fetched in pages (not components)
- [ ] useAsyncData for SSR-safe fetching
- [ ] Hydration handled properly

---

## 4. State Management

### 4.1 useState

- [ ] Used for SSR-safe shared state
- [ ] ref() used for local-only state
- [ ] Meaningful key names

### 4.2 Pinia Store

- [ ] Setup with @pinia/nuxt
- [ ] Store files in stores/
- [ ] Type-safe state and actions
- [ ] Hydration support

### 4.3 useCookie

- [ ] SSR-safe cookie access
- [ ] Proper security options (httpOnly, secure)
- [ ] Max age configured

### 4.4 State Patterns

- [ ] No unnecessary global state
- [ ] State lifecycle managed properly
- [ ] Cleanup on logout

---

## 5. Components

### 5.1 Auto-imports

- [ ] Components in components/ directory
- [ ] Nested directories create prefixes
- [ ] Global components properly organized

### 5.2 Component Types

- [ ] Client-only components wrapped in `<ClientOnly>`
- [ ] Dynamic components with defineAsyncComponent
- [ ] Shared components in shared/ features

### 5.3 Props and Emits

- [ ] Props defined with validation
- [ ] Emits defined explicitly
- [ ] TypeScript types used

### 5.4 Best Practices

- [ ] Single responsibility
- [ ] Proper naming conventions
- [ ] Composition API used

---

## 6. Server Routes

### 6.1 Route Structure

- [ ] RESTful naming convention
- [ ] HTTP methods in filenames
- [ ] Parameter routes properly named

### 6.2 API Development

- [ ] Input validation with Zod
- [ ] Error handling with createError
- [ ] Proper HTTP status codes
- [ ] Response structure consistent

### 6.3 Database Operations

- [ ] Prisma or ORM configured
- [ ] Connection pooling
- [ ] Error handling

### 6.4 Security

- [ ] Input sanitization
- [ ] No sensitive data in responses
- [ ] Rate limiting

---

## 7. Routing

### 7.1 Pages

- [ ] File-based routing understood
- [ ] Dynamic routes with [...slug].vue
- [ ] Nested routes properly structured

### 7.2 Middleware

- [ ] Global middleware in middleware/
- [ ] Named middleware for specific routes
- [ ] definePageMeta used

### 7.3 Navigation

- [ ] useRouter for programmatic navigation
- [ ] useRoute for route params
- [ ] Query params handled

### 7.4 Layouts

- [ ] Default layout defined
- [ ] Layout switching with definePageMeta
- [ ] Nested layouts

---

## 8. Performance

### 8.1 Route Rules

- [ ] Static pages prerendered
- [ ] Dynamic pages with appropriate rendering
- [ ] SWR for semi-static content
- [ ] SSR only when needed

### 8.2 Code Splitting

- [ ] Lazy loaded routes
- [ ] Dynamic imports for heavy components
- [ ] defineAsyncComponent used

### 8.3 Images

- [ ] @nuxt/image installed and configured
- [ ] Proper image formats
- [ ] Lazy loading
- [ ] Responsive sizes

### 8.4 Bundle

- [ ] Bundle analyzed
- [ ] Unused dependencies removed
- [ ] Tree shaking works

---

## 9. Security

### 9.1 Authentication

- [ ] Middleware for protected routes
- [ ] Token validation
- [ ] Session management

### 9.2 Input Validation

- [ ] Server-side validation
- [ ] Zod schemas defined
- [ ] Sanitized inputs

### 9.3 Secrets

- [ ] Runtime config for secrets
- [ ] Environment variables properly set
- [ ] No secrets in client bundle

### 9.4 CORS

- [ ] CORS configured for API routes
- [ ] Proper origin validation
- [ ] Security headers

---

## 10. Deployment

### 10.1 Build

- [ ] Production build successful
- [ ] Type checking passed
- [ ] ESLint passed

### 10.2 Configuration

- [ ] Environment variables set
- [ ] Runtime config configured
- [ ] Route rules for production

### 10.3 Platforms

- [ ] Vercel configured OR
- [ ] Docker configured OR
- [ ] Other platform configured

### 10.4 Monitoring

- [ ] Error tracking (Sentry)
- [ ] Analytics configured
- [ ] Health check endpoint

---

## Quick Reference

### Data Fetching
```
✅ Await useFetch/useAsyncData in pages
✅ Use unique cache keys
✅ Handle loading/error states
❌ Don't use $fetch in top-level components
```

### State
```
✅ useState for SSR-safe shared state
✅ ref() for local-only state
✅ useCookie for persistent client state
❌ Don't use window/localStorage directly
```

### Components
```
✅ Use built-in Nuxt components
✅ Leverage auto-imports
✅ Single responsibility
❌ Don't block hydration unnecessarily
```

### Server Routes
```
✅ Validate input with Zod
✅ Use createError for errors
✅ Proper HTTP methods
❌ Don't expose internal errors
```

---

## Liên kết liên quan
- [Nuxt Glossary](./glossary.md)
- [Nuxt Architecture](./architecture.md)
- [Nuxt Best Practices](./best-practice.md)
- [Nuxt Anti-Patterns](./anti-pattern.md)
- [Nuxt FAQ](./faq.md)
- [Nuxt Decision Tree](./decision-tree.md)
