# NextJS Checklist - Danh Sách Kiểm Tra Next.js

## Giới thiệu

Danh sách kiểm tra này được thiết kế để đảm bảo chất lượng toàn diện cho ứng dụng Next.js.

## Checklist Rendering Strategy

### Thiết kế

- [ ] Xác định rendering strategy cho mỗi route
- [ ] Sử dụng SSG cho static pages
- [ ] Sử dụng SSR cho dynamic pages
- [ ] Cân nhắc ISR cho hybrid cases

### Implementation

- [ ] Implement Server Components đúng cách
- [ ] Add 'use client' directive khi cần thiết
- [ ] Sử dụng loading.tsx cho routes
- [ ] Implement error.tsx cho error boundaries

## Checklist Data Fetching

### Implementation

- [ ] Fetch data trong Server Components
- [ ] Sử dụng parallel fetching khi có thể
- [ ] Implement proper caching
- [ ] Handle errors gracefully

### Testing

- [ ] Test với slow connections
- [ ] Test với failed requests
- [ ] Verify data consistency

## Checklist Components

### Implementation

- [ ] Sử dụng next/image
- [ ] Sử dụng next/font
- [ ] Sử dụng next/script với strategies
- [ ] Implement responsive design
- [ ] Test keyboard navigation

## Checklist Performance

### Implementation

- [ ] Monitor bundle size
- [ ] Implement dynamic imports
- [ ] Optimize images
- [ ] Enable compression

### Testing

- [ ] Test Core Web Vitals
- [ ] Lighthouse audit
- [ ] Performance profiling

## Checklist Security

### Implementation

- [ ] Protect sensitive routes
- [ ] Validate user inputs
- [ ] Use environment variables
- [ ] Implement CSRF protection

## Checklist Deployment

### Preparation

- [ ] Test locally
- [ ] Review environment variables
- [ ] Test in preview environment

### Deployment

- [ ] Deploy to production
- [ ] Monitor error rates
- [ ] Verify functionality

## Kết luận

Sử dụng checklist này như companion trong quá trình phát triển Next.js.
