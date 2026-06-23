# Vue FAQ - Câu Hỏi Thường Gặp Vue.js

## Giới thiệu

Tài liệu này tổng hợp các câu hỏi thường gặp về Vue.js.

## Câu Hỏi Cơ Bản

### 1. Vue.js là gì?

Vue.js là progressive JavaScript framework cho xây dựng giao diện người dùng. Vue được thiết kế để adoptable incrementally, có thể sử dụng cho everything từ adding interactivity đến building complex SPAs.

### 2. Vue 2 vs Vue 3?

Vue 3 là version mới nhất với Composition API, better TypeScript support, improved performance. Vue 2 đã reached end-of-life. Vue 3 recommended cho all new projects.

### 3. Composition API vs Options API?

Composition API cung cấp better code organization, TypeScript support, và code reuse via composables. Options API vẫn supported và có thể mix trong Vue 3.

### 4. Pinia vs Vuex?

Pinia là official state management cho Vue 3, simpler API, better TypeScript support. Vuex là legacy và không recommended cho new projects.

## Câu Hỏi Kỹ Thuật

### 5. Làm thế nào để quản lý state?

Sử dụng Pinia cho global state. Props và emits cho parent-child communication. Composables cho reusable stateful logic.

### 6. Vue Router hoạt động như thế nào?

Vue Router map URLs to components. Dynamic segments cho parameterized routes. Navigation guards cho authentication. Lazy loading cho code splitting.

### 7. Composables là gì?

Composables là functions sử dụng Vue Composition API để reuse stateful logic. Pattern: useXxx naming convention. Có thể combine composables.

### 8. Làm thế nào để test Vue components?

Sử dụng Vue Test Utils. Mount components, simulate events, assert results. Vitest là recommended test runner.

## Câu Hỏi Performance

### 9. Làm thế nào để optimize Vue apps?

Lazy load routes. Use v-memo cho lists. Avoid unnecessary re-renders. Optimize bundle size. Use production build.

### 10. Virtual scrolling là gì?

Virtual scrolling chỉ render visible items trong long lists. vue-virtual-scroller hoặc vue-virtual-scroll-grid là popular libraries.
