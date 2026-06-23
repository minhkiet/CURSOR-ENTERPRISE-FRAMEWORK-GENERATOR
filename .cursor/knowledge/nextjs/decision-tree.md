# NextJS Decision Tree - Cây Quyết Định Next.js

## Giới thiệu

Cây quyết định này hướng dẫn developers trong việc đưa ra các quyết định kiến trúc Next.js.

## Quyết định về Router

### Câu hỏi: Sử dụng App Router hay Pages Router?

- **App Router**
  - Pros: Server Components, layouts, streaming
  - Cons: New, learning curve
  - Khi nào: New projects

- **Pages Router**
  - Pros: Mature, simple
  - Cons: Less features
  - Khi nào: Migration từ legacy

## Quyết định về Rendering

### Câu hỏi: Chọn rendering strategy nào?

- **SSG**
  - Khi: Content tĩnh, blog, docs
  - Pros: Fast, SEO-friendly
  - Cons: Build time increases

- **SSR**
  - Khi: Dynamic content, personalization
  - Pros: Fresh content, SEO
  - Cons: Server processing

- **ISR**
  - Khi: Hybrid, e-commerce
  - Pros: Static speed + fresh
  - Cons: Complexity

## Quyết định về Styling

### Câu hỏi: Chọn styling solution nào?

- **Tailwind CSS**
  - Pros: Fast, utility-first
  - Cons: HTML pollution
  - Khi nào: Most projects

- **CSS Modules**
  - Pros: Scoped, simple
  - Cons: No utilities
  - Khi nào: Simple projects

## Quyết định về State Management

### Câu hỏi: State management solution nào?

- **Server State**
  - Approach: Server Components + fetch
  - Khi nào: Most cases

- **Zustand/Jotai**
  - Approach: Lightweight stores
  - Khi nào: Simple client state

- **Redux**
  - Approach: Full-featured
  - Khi nào: Complex state

## Quyết định về Database

### Câu hỏi: Database ORM nào?

- **Prisma**
  - Pros: Type-safe, easy migrations
  - Khi nào: Most cases

- **Drizzle**
  - Pros: Lightweight, SQL-like
  - Khi nào: Performance-critical

## Summary

Use this decision tree as a starting point và adapt based on specific requirements.
