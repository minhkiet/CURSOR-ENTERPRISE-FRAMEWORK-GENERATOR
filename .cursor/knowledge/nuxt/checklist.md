---
title: "Nuxt Checklist - Danh Sách Kiểm Tra"
description: "Comprehensive checklist cho pre-deployment review, code review, và production readiness của ứng dụng Nuxt"
tags: ["nuxt", "vue", "deployment", "code-review", "checklist", "production"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Nuxt Checklist - Danh Sách Kiểm Tra

## Overview

Tài liệu này cung cấp checklist toàn diện cho việc review và deploy ứng dụng Nuxt. Được thiết kế để sử dụng trong nhiều contexts khác nhau: self-review trước khi commit, peer code review, pre-deployment verification, và periodic production audits.

Mỗi section chứa các items được đánh dấu theo mức độ quan trọng: **Critical** (phải hoàn thành trước khi deploy), **Important** (nên hoàn thành), và **Nice-to-have** (recommended nhưng không bắt buộc). Việc không hoàn thành các items Critical sẽ ngăn cản việc deploy production.

## Purpose

Danh sách kiểm tra này phục vụ các mục đích chính sau:

1. **Quality Assurance** - Đảm bảo tất cả aspects của ứng dụng đã được properly implemented
2. **Knowledge Transfer** - Checklist giúp reviewers nhanh chóng identify areas cần attention
3. **Consistency** - Áp dụng same standards across all team members và projects
4. **Confidence** - Deployment team có thể confident rằng đã review kỹ lưỡng trước khi release

## Key Concepts

### Checklist Categories

Danh sách được chia thành 8 categories chính, mỗi category bao gồm một aspect cụ thể của ứng dụng Nuxt. Việc phân chia này giúp dễ dàng assign reviewers cho specific areas và track progress của từng phần.

### Priority Levels

- **Critical** (🔴): Must complete trước production deployment. Không có exception.
- **Important** (🟡): Should complete trước production deployment. Technical debt nên được tracked.
- **Nice-to-have** (🟢): Recommended cho optimal user experience và maintainability.

### Reviewer Types

- **Developer**: Người viết code tự review trước khi gửi PR
- **Peer**: Team member review code của developer khác
- **Tech Lead**: Senior review cho architectural decisions
- **QA**: Functional testing và acceptance criteria verification

## Pre-Deployment Checklist

### 1. Configuration Verification 🔴

#### Environment Variables

- [ ] All required environment variables are documented
- [ ] `.env.example` file exists với placeholder values
- [ ] No hardcoded secrets in source code
- [ ] Environment variables are properly typed in `RuntimeConfig`
- [ ] Sensitive variables are marked as `private` (server-only)

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  runtimeConfig: {
    // Public - exposed to client
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE
    },
    // Private - server only
    databaseUrl: process.env.DATABASE_URL,
    jwtSecret: process.env.JWT_SECRET
  }
})
```

#### Build Configuration

- [ ] `nuxt.config.ts` không chứa development-only settings
- [ ] Route rules được configured cho proper caching
- [ ] Module versions tương thích với Nuxt version
- [ ] TypeScript strict mode enabled (nếu project yêu cầu)
- [ ] Build output directory chính xác

```typescript
// Check route rules configuration
export default defineNuxtConfig({
  routeRules: {
    '/': { prerender: true },
    '/api/**': { cache: false },
    '/admin/**': { ssr: false }
  }
})
```

#### Security Configuration

- [ ] CORS properly configured cho API routes
- [ ] Security headers configured (CSP, X-Frame-Options, etc.)
- [ ] Rate limiting enabled cho public endpoints
- [ ] No debug mode enabled in production

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  app: {
    head: {
      meta: [
        { name: 'X-Content-Type-Options', content: 'nosniff' },
        { name: 'X-Frame-Options', content: 'DENY' }
      ],
      link: [
        { rel: 'strict-transport-security', content: 'max-age=31536000' }
      ]
    }
  },
  routeRules: {
    '/api/**': {
      cors: true,
      headers: {
        'X-RateLimit-Limit': '100',
        'X-RateLimit-Window': '60'
      }
    }
  }
})
```

### 2. SEO Verification 🔴

#### Meta Tags

- [ ] Every page có unique `title` tag
- [ ] Every page có `description` meta tag
- [ ] `og:title`, `og:description`, `og:image` cho social sharing
- [ ] `canonical` URL được set cho all pages
- [ ] `robots` meta tag appropriately configured

```vue
<script setup lang="ts">
// Kiểm tra mỗi page có useHead hoặc useSeoMeta
useHead({
  title: 'Page Title | Brand',
  meta: [
    { name: 'description', content: 'Page description' },
    { property: 'og:title', content: 'Page Title' },
    { property: 'og:description', content: 'Page description' },
    { property: 'og:image', content: '/images/og-image.jpg' },
    { name: 'robots', content: 'index, follow' }
  ],
  link: [
    { rel: 'canonical', href: 'https://example.com/page' }
  ]
})
</script>
```

#### Technical SEO

- [ ] Sitemap được generate và auto-update
- [ ] Robots.txt configured properly
- [ ] Structured data (JSON-LD) cho important pages
- [ ] Breadcrumbs implemented for navigation
- [ ] Pagination properly implemented với rel="prev/next"

```typescript
// nuxt.config.ts - sitemap generation
export default defineNuxtConfig({
  modules: ['@nuxtjs/sitemap'],
  site: {
    url: 'https://example.com'
  },
  sitemap: {
    strictNuxtContentPaths: true
  }
})
```

### 3. Performance Verification 🟡

#### Bundle Analysis

- [ ] Bundle size đã được analyzed với `npx nuxi analyze`
- [ ] No unintended large dependencies
- [ ] Tree-shaking hoạt động đúng
- [ ] Dynamic imports used cho heavy components

```bash
# Run bundle analysis
npx nuxi analyze

# Check for large bundles
npm run build -- --analyze
```

#### Image Optimization

- [ ] `@nuxt/image` module installed và configured
- [ ] All images use `<NuxtImg>` component
- [ ] Images properly sized (no oversized images)
- [ ] Lazy loading enabled for below-fold images
- [ ] WebP/AVIF format configured

```vue
<!-- Correct image usage -->
<NuxtImg
  src="/images/product.jpg"
  alt="Product image"
  width="400"
  height="300"
  format="webp"
  loading="lazy"
/>
```

#### Loading Performance

- [ ] Critical CSS inlined
- [ ] Font loading optimized (font-display: swap)
- [ ] Third-party scripts lazy-loaded
- [ ] Route-based code splitting hoạt động
- [ ] Preload hints for critical resources

### 4. Error Handling Verification 🔴

#### Error Pages

- [ ] Custom error page (`error.vue`) implemented
- [ ] Error states properly displayed cho users
- [ ] Error messages are user-friendly (not technical)
- [ ] Recovery actions available (retry, go home)

```vue
<!-- error.vue -->
<template>
  <div class="error-page">
    <h1>{{ error.statusCode }}</h1>
    <p>{{ errorMessage }}</p>
    <NuxtLink to="/">Go Home</NuxtLink>
    <button @click="handleError">Try Again</button>
  </div>
</template>
```

#### API Error Handling

- [ ] All API routes có error handling
- [ ] Proper HTTP status codes returned
- [ ] Error responses follow consistent format
- [ ] Client properly handles API errors

```typescript
// Server-side error handling
export default defineEventHandler(async (event) => {
  try {
    return await handleRequest(event)
  } catch (error) {
    console.error('API Error:', error)
    
    throw createError({
      statusCode: error instanceof AppError ? error.statusCode : 500,
      message: error.message || 'Internal server error'
    })
  }
})
```

#### Client-Side Error Boundaries

- [ ] ErrorBoundary component used for fragile sections
- [ ] Async operations wrapped in try-catch
- [ ] Global error handler configured
- [ ] Errors logged to monitoring service

### 5. Security Verification 🔴

#### Authentication & Authorization

- [ ] All protected routes have auth middleware
- [ ] Role-based access control properly implemented
- [ ] Session/token expiration properly handled
- [ ] Password hashing uses strong algorithms (bcrypt, argon2)
- [ ] CSRF protection enabled

```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware(async (to) => {
  const { isAuthenticated, user } = useAuth()
  
  const publicRoutes = ['/login', '/register']
  
  if (!publicRoutes.includes(to.path) && !isAuthenticated.value) {
    return navigateTo(`/login?redirect=${to.fullPath}`)
  }
  
  if (to.path.startsWith('/admin') && user.value?.role !== 'admin') {
    throw createError({ statusCode: 403, message: 'Admin access required' })
  }
})
```

#### Data Validation

- [ ] All user inputs validated (both client và server)
- [ ] Zod hoặc similar schema validation used
- [ ] SQL injection prevention (use Prisma ORM)
- [ ] XSS prevention (Vue auto-escapes by default)
- [ ] File upload validation (type, size)

```typescript
// Input validation example
import { z } from 'zod'

const UserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.number().min(13).max(120).optional()
})

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const result = UserSchema.safeParse(body)
  
  if (!result.success) {
    throw createError({
      statusCode: 400,
      message: 'Validation failed',
      data: result.error.flatten()
    })
  }
  
  // Proceed với validated data
})
```

#### Secrets Management

- [ ] No secrets in source code (use env vars)
- [ ] Secrets rotated regularly
- [ ] API keys have minimal required permissions
- [ ] Database credentials are strong

### 6. Testing Verification 🟡

#### Unit Tests

- [ ] Composables have unit tests
- [ ] Utility functions tested
- [ ] Store (Pinia) actions tested
- [ ] At least 70% code coverage for business logic

```typescript
// composables/__tests__/useCounter.spec.ts
import { describe, it, expect } from 'vitest'
import { useCounter } from '../useCounter'

describe('useCounter', () => {
  it('increments count', () => {
    const { count, increment } = useCounter()
    expect(count.value).toBe(0)
    increment()
    expect(count.value).toBe(1)
  })
})
```

#### Integration Tests

- [ ] API routes have integration tests
- [ ] Page components tested
- [ ] Navigation flows tested
- [ ] Auth flows tested

```typescript
// server/api/__tests__/users.spec.ts
import { describe, it, expect } from 'vitest'
import { setup, $fetch } from '@nuxt/test-utils'

describe('Users API', () => {
  await setup({ fixture: 'fixture' })
  
  it('returns users list', async () => {
    const users = await $fetch('/api/users')
    expect(Array.isArray(users)).toBe(true)
  })
})
```

#### E2E Tests

- [ ] Critical user flows have E2E tests
- [ ] Authentication flow tested
- [ ] Checkout flow tested (nếu applicable)
- [ ] Form submissions tested

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test('user can login', async ({ page }) => {
  await page.goto('/login')
  await page.fill('[name="email"]', 'user@example.com')
  await page.fill('[name="password"]', 'password123')
  await page.click('button[type="submit"]')
  
  await expect(page).toHaveURL('/dashboard')
})
```

### 7. Accessibility Verification 🟡

#### Semantic HTML

- [ ] Proper heading hierarchy (h1 → h6)
- [ ] Semantic elements used (main, nav, article, aside)
- [ ] Buttons used for actions, links for navigation
- [ ] Form elements properly labeled

#### Keyboard Navigation

- [ ] All interactive elements focusable
- [ ] Focus order is logical
- [ ] Focus visible styles applied
- [ ] Skip links provided

#### ARIA

- [ ] ARIA labels for icon-only buttons
- [ ] ARIA live regions for dynamic content
- [ ] Form error messages linked with aria-describedby

### 8. Code Quality Verification 🟡

#### Code Style

- [ ] ESLint passes without errors
- [ ] Prettier formatting applied
- [ ] No console.log statements (use proper logging)
- [ ] Code follows team conventions

```bash
# Run linter
npm run lint

# Fix auto-fixable issues
npm run lint:fix

# Format code
npm run format
```

#### TypeScript

- [ ] Strict TypeScript enabled
- [ ] No `any` types (use `unknown` when necessary)
- [ ] Props have proper types
- [ ] API responses typed
- [ ] Composables have return type annotations

```typescript
// Good: Proper typing
interface User {
  id: string
  email: string
  name: string
}

export const useUser = (id: string) => {
  const { data, pending } = useFetch<User>(`/api/users/${id}`)
  return { user: data, pending }
}
```

## Code Review Checklist

### 1. Architecture Review

#### Component Structure

- [ ] Components are single responsibility
- [ ] Components not too large (refactor if > 300 lines)
- [ ] Logic extracted to composables when appropriate
- [ ] Slots used for flexible component composition

#### State Management

- [ ] State hoisting done correctly
- [ ] Pinia stores properly organized
- [ ] No prop drilling (use provide/inject or Pinia)
- [ ] State updates are immutable

#### File Organization

- [ ] Files follow naming conventions
- [ ] Imports ordered correctly (Vue → Nuxt → Third-party → Local)
- [ ] No circular dependencies
- [ ] Constants extracted to separate files

### 2. Performance Review

#### Data Fetching

- [ ] useFetch/useAsyncData used (not onMounted + fetch)
- [ ] Proper cache keys defined
- [ ] Parallel fetches combined with Promise.all
- [ ] Lazy loading for non-critical data

#### Reactivity

- [ ] Computed properties used for derived state
- [ ] Watchers properly cleaned up
- [ ] No unnecessary reactive wrapping
- [ ] useMemo/vcomputed used for expensive calculations

#### Rendering

- [ ] v-if vs v-show used appropriately
- [ ] Key attributes on v-for loops
- [ ] Components lazy loaded when needed
- [ ] No unnecessary re-renders

### 3. Security Review

#### Input Handling

- [ ] User input sanitized
- [ ] File uploads validated
- [ ] URL parameters validated
- [ ] SQL injection prevented (use ORM)

#### Output Handling

- [ ] XSS prevented (Vue escapes by default)
- [ ] Sensitive data not logged
- [ ] Error messages don't expose internals

### 4. Maintainability Review

#### Documentation

- [ ] Complex logic has comments
- [ ] Public APIs documented
- [ ] README updated if needed

#### Testing

- [ ] New features have tests
- [ ] Bug fixes have regression tests
- [ ] Edge cases handled

## Production Readiness Checklist

### Pre-Launch Verification 🔴

- [ ] All Critical items from above completed
- [ ] Staging environment mirrors production
- [ ] Database migrations tested
- [ ] Backup procedures documented và tested
- [ ] Monitoring và alerting configured

### Infrastructure 🟡

- [ ] CDN configured for static assets
- [ ] Load balancer configured (nếu needed)
- [ ] Auto-scaling policies defined
- [ ] Health check endpoints implemented

### Monitoring 🔴

- [ ] Error tracking (Sentry, Bugsnag) configured
- [ ] Analytics (Google Analytics, Plausible) implemented
- [ ] Performance monitoring (Web Vitals) in place
- [ ] Log aggregation configured
- [ ] Uptime monitoring set up

### Operations 🟡

- [ ] Deployment process documented
- [ ] Rollback procedure tested
- [ ] Runbook created for common issues
- [ ] On-call rotation established

## Troubleshooting

### Common Issues và Quick Fixes

#### Issue: Bundle Size Too Large

**Quick Fix**:
```bash
# Analyze bundle
npx nuxi analyze

# Check for large dependencies
npm ls | grep -E "^\s+├──|└──" | sort -k3 -h | tail -20
```

#### Issue: Hydration Mismatch

**Quick Fix**:
1. Search for `Math.random()`, `Date.now()` in templates
2. Check for direct `window`/`document` access outside `onMounted`
3. Verify conditional rendering is SSR-safe

#### Issue: SEO Score Low

**Quick Fix**:
1. Run Lighthouse audit: `npx lighthouse https://site.com`
2. Check for missing meta tags with browser devtools
3. Validate structured data: https://validator.schema.org/

## Examples

### Pre-Deployment Review Template

```markdown
## Pre-Deployment Review

### Project: [Project Name]
### Version: [Version/Tag]
### Review Date: [Date]
### Reviewer: [Name]

### Critical Items
- [ ] Configuration verified
- [ ] SEO implemented
- [ ] Error handling complete
- [ ] Security reviewed

### Important Items
- [ ] Performance optimized
- [ ] Tests written
- [ ] Accessibility checked

### Sign-Off
- [ ] Developer: [Name] - [Date]
- [ ] Reviewer: [Name] - [Date]
- [ ] Tech Lead: [Name] - [Date]
```

### Code Review Checklist Template

```markdown
## Code Review Checklist

### PR: [#123] Feature Description
### Author: [Name]
### Reviewer: [Name]

### Architecture
- [ ] Component structure appropriate
- [ ] State management correct
- [ ] No code duplication

### Security
- [ ] Input validation present
- [ ] No security vulnerabilities
- [ ] Secrets not exposed

### Performance
- [ ] No N+1 queries
- [ ] Proper data fetching
- [ ] Bundle size acceptable

### Quality
- [ ] Tests pass
- [ ] Code style consistent
- [ ] Documentation updated

### Feedback
[Detailed review comments]
```

## References

### Tools for Verification

- [Nuxt DevTools](https://devtools.nuxt.com/) - Official debugging tools
- [Vue DevTools](https://devtools.vuejs.org/) - Vue component inspection
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) - Performance auditing
- [GTmetrix](https://gtmetrix.com/) - Page speed testing
- [Schema Validator](https://validator.schema.org/) - Structured data validation

### Related Rules

- Xem `best-practice.md` cho detailed implementation guidance
- Xem `anti-pattern.md` để tránh common mistakes
- Xem `performance.mdc` cho performance optimization
- Xem `security.mdc` cho security best practices
- Xem `testing.mdc` cho testing guidelines
