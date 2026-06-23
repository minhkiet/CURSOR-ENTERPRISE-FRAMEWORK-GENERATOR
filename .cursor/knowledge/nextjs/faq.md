# NextJS FAQ - Câu Hỏi Thường Gặp Next.js

## Giới thiệu

Tài liệu này tổng hợp các câu hỏi thường gặp về Next.js.

## Câu Hỏi Cơ Bản

### 1. Next.js là gì và tại sao nên sử dụng?

Next.js là React framework cho phép xây dựng ứng dụng web với nhiều rendering strategies: SSG, SSR, CSR. Next.js cung cấp opinionated defaults cho routing, image optimization, font optimization, và performance. Tại sao nên dùng: developer experience tốt, built-in optimizations, flexible rendering, strong ecosystem, Vercel integration.

### 2. App Router vs Pages Router?

App Router là router mới từ Next.js 13+, sử dụng React Server Components và nested layouts. Pages Router là router cũ, đơn giản hơn nhưng ít tính năng. App Router recommended cho new projects vì nhiều benefits: Server Components, layouts, streaming.

### 3. Server Components vs Client Components?

Server Components được render trên server, không gửi JS đến client. Client Components có 'use client' directive, hydrate trên client. Default trong App Router là Server Components. Use Client Components khi cần interactivity, hooks, browser APIs.

### 4. Khi nào nên sử dụng SSG, SSR, hoặc CSR?

SSG cho content tĩnh như blog posts, documentation. SSR cho content động cần SEO như e-commerce product pages. CSR cho dashboard, auth-protected pages cần real-time data.

## Câu Hỏi Kỹ Thuật

### 5. Làm thế nào để fetch data trong Next.js?

Trong Server Components: async functions và direct database/API calls. Trong Client Components: useEffect + fetch, hoặc React Query/SWR. Route Handlers cho API endpoints.

### 6. ISR là gì và khi nào nên sử dụng?

ISR (Incremental Static Regeneration) cho phép regenerate static pages sau build. Use ISR khi content thay đổi định kỳ như blog posts, product listings. Revalidation interval xác định tần suất regenerate.

### 7. Middleware hoạt động như thế nào?

Middleware chạy trước mỗi request, cho phép redirect, rewrite, add headers. Use cases: authentication, geolocation, A/B testing. Middleware chạy trên Edge Runtime.

### 8. Image Optimization được implement như thế nào?

Sử dụng next/image component thay vì img tag. Next.js tự động resize, convert sang WebP/AVIF, lazy load. Configure remote patterns trong next.config.js cho external images.

## Câu Hỏi Performance

### 9. Làm thế nào để cải thiện Core Web Vitals?

LCP: Optimize images, use priority loading, enable font optimization. CLS: Specify image dimensions, use font-display: swap. INP: Minimize client-side JS, use Server Components.

### 10. Bundle size quá lớn nên làm gì?

Analyze bundle với @next/bundle-analyzer. Dynamic imports cho large components. Tree-shake unused code. Replace heavy libraries với lighter alternatives.

## Câu Hỏi Deployment

### 11. Deploy Next.js ở đâu tốt nhất?

Vercel là best choice vì native Next.js support, automatic deployments, edge network. Self-host với Node.js, Docker, hoặc Kubernetes cũng possible.

### 12. Environment variables hoạt động như thế nào?

Client-side: prefix với NEXT_PUBLIC_. Server-side: regular .env files. Không đặt secrets trong NEXT_PUBLIC_ vars.
