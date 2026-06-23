# NextJS Anti-Patterns - Các Mẫu Thiết Kế Cần Tránh

## Giới thiệu

Tài liệu này liệt kê các anti-patterns phổ biến trong Next.js development.

## Anti-Patterns về Rendering

### 1. Overusing Client Components

**Mô tả**: Đánh dấu quá nhiều components là client components khi không cần thiết.

**Hậu quả**: Bundle size lớn, hydration overhead.

**Giải pháp**: Server Components làm default, chỉ dùng 'use client' khi cần hooks/interactivity.

### 2. Fetching Data in Client Components

**Mô tả**: Fetch data trong useEffect thay vì Server Components.

**Hậu quả**: Loading states, potential waterfall requests.

**Giải pháp**: Fetch data trong Server Components, pass as props.

### 3. Ignoring SSG Opportunities

**Mô tả**: Sử dụng SSR cho static content.

**Hậu quả**: Unnecessary server processing, slower TTFB.

**Giải pháp**: Use SSG/ISR cho content không thay đổi thường xuyên.

## Anti-Patterns về Data Fetching

### 4. Waterfall Requests

**Mô tả**: Fetch data sequentially thay vì parallel.

**Hậu quả**: Slow page loads.

**Giải pháp**: Use Promise.all() cho parallel fetches.

### 5. No Caching

**Mô tả**: Không specify caching options.

**Hậu quả**: Unnecessary re-fetching, poor performance.

**Giải pháp**: Use fetch() options cho appropriate caching.

### 6. Ignoring Errors

**Mô tả**: Không handle fetch errors.

**Hậu quả**: Silent failures, poor UX.

**Giải pháp**: Implement proper error handling và boundaries.

## Anti-Patterns về Components

### 7. Prop Drilling

**Mô tả**: Truyền props qua nhiều levels không cần thiết.

**Hậu quả**: Hard to maintain, unnecessary re-renders.

**Giải pháp**: Use Context, Zustand, hoặc composition.

### 8. Not Using Image Component

**Mô tả**: Sử dụng img tag thay vì next/image.

**Hậu quả**: Unoptimized images, poor performance.

**Giải pháp**: Always use next/image component.

### 9. Large Bundle Components

**Mô tả**: Import entire libraries cho small functionality.

**Hậu quả**: Large bundle size.

**Giải pháp**: Tree-shake, use specific imports, dynamic imports.

## Anti-Patterns về State Management

### 10. Client State Overuse

**Mô tả**: Lưu trữ quá nhiều state trên client.

**Hậu quả**: Complex state management, hydration issues.

**Giải pháp**: Use Server Components, keep state on server.

### 11. Not Using URL State

**Mô tả**: Sử dụng local state cho filters/search.

**Hậu quả**: State not shareable, hard to bookmark.

**Giải pháp**: Use URL search params cho filters.

## Anti-Patterns về Security

### 12. Client-Side Auth Checks

**Mô tả**: Chỉ check authentication trên client.

**Hậu quả**: Security vulnerabilities.

**Giải pháp**: Always validate auth server-side.

### 13. Exposing Secrets in Client

**Mô tả**: Sử dụng secrets trong Client Components.

**Hậu quả**: Secret exposure.

**Giải pháp**: Keep secrets server-side, use env vars correctly.

## Anti-Patterns về Performance

### 14. Not Implementing Error Boundaries

**Mô tả**: Không wrap components với error boundaries.

**Hậu quả**: Entire app crash on errors.

**Giải phól**: Use error.tsx và ErrorBoundary components.

### 15. Ignoring Loading States

**Mô tả**: Không implement loading states.

**Hậu quả**: Poor UX during navigation.

**Giải pháp**: Use loading.tsx cho routes.

## Kết luận

Tránh các anti-patterns này giúp xây dựng Next.js apps hiệu quả hơn.
