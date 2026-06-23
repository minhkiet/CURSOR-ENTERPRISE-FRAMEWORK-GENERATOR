# Nuxt FAQ - Câu Hỏi Thường Gặp Nuxt.js

## Giới thiệu

Tài liệu này tổng hợp các câu hỏi thường gặp về Nuxt.js.

## Câu Hỏi Cơ Bản

### 1. Nuxt.js là gì?

Nuxt.js là full-stack framework built on top of Vue.js. Cung cấp SSR, SSG, hybrid rendering, file-based routing, auto-imports, server routes.

### 2. Nuxt 2 vs Nuxt 3?

Nuxt 3 là version mới với Vue 3, Vite, improved performance, Nitro server engine. Nuxt 2 reached end-of-life.

### 3. Khi nào nên dùng SSG vs SSR?

SSG cho content tĩnh (docs, blogs). SSR cho dynamic content (dashboards, personalized pages).

### 4. Server routes là gì?

API endpoints trong server/api/ directory. Tự động tạo routes. TypeScript support.

## Câu Hỏi Kỹ Thuật

### 5. Data fetching như thế nào?

useFetch và useAsyncData cho SSR-aware data fetching. Auto-caching và deduplication.

### 6. Modules là gì?

Extensions cho Nuxt functionality. Install qua npm. Configure trong nuxt.config.ts.

### 7. Auto-imports hoạt động ra sao?

Components và composables tự động imported. Không cần manual imports.
