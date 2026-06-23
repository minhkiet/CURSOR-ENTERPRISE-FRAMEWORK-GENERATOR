# Vue Best Practices - Thực Hành Tốt Nhất Vue

## Giới thiệu

Tài liệu này tổng hợp các best practices cho Vue.js development.

## Component Best Practices

### 1. Single-File Components

- Sử dụng `<script setup>` cho cleaner syntax
- Đặt tên component theo PascalCase
- Props có type definitions
- Emit events với type safety

### 2. Reactivity

- Sử dụng `ref()` cho primitives
- Sử dụng `reactive()` cho objects
- Tránh destructure reactive objects
- Sử dụng `computed()` cho derived state

### 3. Composition API

- Extract logic vào composables
- Keep components small và focused
- Use composables for code reuse
- Organize imports logically

## State Management

### 4. Pinia Store

- One store per domain
- Keep store state minimal
- Use getters for computed state
- Actions cho async operations

### 5. Props và Events

- Define prop types
- Validate props
- Use v-model properly
- Emit typed events

## Performance

### 6. Lazy Loading

- Lazy load routes
- Lazy load heavy components
- Use Suspense for async
- Code splitting

### 7. Optimization

- Use v-memo cho large lists
- Avoid unnecessary re-renders
- Use shallowRef cho large data
- Memoize expensive computed

## Security

### 8. XSS Prevention

- Sanitize user input
- Use v-text thay vì v-html when possible
- Validate all props
- Avoid dynamic template evaluation

## Testing

### 9. Component Testing

- Test behavior, not implementation
- Use Vue Test Utils
- Mock dependencies properly
- Test edge cases

## Kết luận

Following these practices ensures maintainable Vue applications.
