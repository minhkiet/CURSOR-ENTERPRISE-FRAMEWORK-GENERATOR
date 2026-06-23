# NextJS Architecture - Kiến Trúc Hệ Thống Next.js

## Tổng quan kiến trúc

Next.js là React framework cho phép xây dựng ứng dụng web với Server Components, Static Generation, và Server-Side Rendering. Kiến trúc Next.js tập trung vào developer experience và performance. Framework cung cấp opinionated defaults trong khi vẫn cho phép tùy biến khi cần.

## Kiến trúc chi tiết

### 1. Project Structure

```
├── app/                    # App Router (Next.js 13+)
│   ├── (routes)/         # Route Groups
│   ├── api/              # API Routes
│   ├── layout.tsx        # Root Layout
│   ├── page.tsx          # Home Page
│   └── globals.css       # Global Styles
├── components/            # Reusable Components
├── lib/                  # Utility Functions
├── public/               # Static Assets
├── styles/               # Additional Styles
├── prisma/               # Database Schema
└── next.config.js        # Configuration
```

### 2. App Router Architecture

**Pages và Layouts**: App Router sử dụng file-system based routing. Mỗi thư mục là một route. `page.tsx` là UI của route. `layout.tsx` là shared layout. `loading.tsx` cho loading states. `error.tsx` cho error boundaries.

**Server Components**: Default trong App Router. Render trên server, reduce bundle size. Truy cập backend resources trực tiếp. Không thể sử dụng hooks hoặc browser APIs.

**Client Components**: Thêm `'use client'` directive. Hydrate trên client. Sử dụng hooks, event handlers, browser APIs.

### 3. Data Fetching Patterns

**Server Components**: Async functions cho data fetching. `fetch()` với extended options. Database queries trực tiếp. Caching với `fetch()` options.

**Route Handlers**: API endpoints trong `app/api/`. Xử lý POST, GET, PUT, DELETE. Validate request bodies. Return JSON responses.

### 4. Rendering Strategies

**SSG (Static Site Generation)**: Pre-render tại build time. `generateStaticParams` cho dynamic routes. Tốt cho content không thay đổi.

**SSR (Server-Side Rendering)**: Render mỗi request. Async Server Components. Tốt cho dynamic content.

**ISR (Incremental Static Regeneration)**: `revalidate` option. Hybrid static + dynamic. On-demand revalidation với `revalidatePath`.

### 5. Database Integration

**Prisma ORM**: Schema definition. Type-safe queries. Migration management. Connection pooling.

**Pattern**: Database queries trong Server Components. Actions cho mutations. Server Actions cho form submissions.

### 6. Authentication

**NextAuth.js**: Authentication solution cho Next.js. Multiple providers. Session management. Protected routes.

**Pattern**: Middleware cho route protection. Server Components cho auth checks. Client Components cho login forms.

### 7. State Management

**Server State**: Server Components + fetch. No client state needed. Revalidation cho updates.

**Client State**: React hooks (`useState`, `useReducer`). Context API cho cross-component state. Zustand/Jotai cho complex state.

### 8. Styling

**Tailwind CSS**: Utility-first CSS. Responsive design. Dark mode support. JIT compiler.

**CSS Modules**: Component-scoped styles. No runtime overhead. Best cho complex components.

### 9. API Design

**RESTful Routes**: CRUD operations. Proper status codes. Request validation. Error handling.

**API Pattern**:
```typescript
// app/api/users/route.ts
export async function GET() { /* list */ }
export async function POST() { /* create */ }

// app/api/users/[id]/route.ts
export async function GET() { /* get one */ }
export async function PUT() { /* update */ }
export async function DELETE() { /* delete */ }
```

### 10. Performance Optimization

**Images**: `next/image` component. Automatic optimization. WebP/AVIF formats. Lazy loading.

**Fonts**: `next/font` module. Self-hosted fonts. Zero layout shift.

**Scripts**: `next/script` component. Loading strategies. Third-party scripts.

### 11. Deployment

**Vercel**: Native Next.js support. Edge network. Automatic scaling.

**Self-hosted**: Node.js server. Docker containers. Kubernetes.

## Database Schema Design

### Core Tables

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  image     String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  posts     Post[]
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

## Security Architecture

### Authentication

- Server Actions cho mutations
- CSRF protection built-in
- Input validation
- Rate limiting

### Data Protection

- Environment variables cho secrets
- Encrypted database connections
- Proper access controls

## Scalability

### Caching

- fetch() caching
- Route segment caching
- Full route cache
- Data cache

### Edge Functions

- Middleware
- Edge Runtime
- CDN caching

## Kết luận

Next.js cung cấp opinionated architecture giúp build production-ready apps nhanh chóng. Focus vào Server Components và hybrid rendering strategies giúp optimize performance.
