# NextJS Glossary - Từ Điển Thuật Ngữ Next.js

## Giới thiệu

Tài liệu này cung cấp danh sách đầy đủ các thuật ngữ chuyên ngành Next.js, framework React phổ biến nhất hiện nay. Mỗi thuật ngữ được định nghĩa chi tiết với ngữ cảnh ứng dụng trong thực tế.

## Các thuật ngữ cơ bản

### 1. App Router (Bộ Định Tuyến Ứng Dụng)

App Router là hệ thống định tuyến mới trong Next.js 13+, sử dụng cấu trúc thư mục để xác định routes. App Router thay thế cho Pages Router và cung cấp nhiều tính năng mới như layouts, nested routing, loading states, error boundaries, và Server Components. Routes được tạo bằng cách tạo thư mục trong thư mục `app`, mỗi thư mục đại diện cho một route.

Trong App Router, các file đặc biệt bao gồm: `page.tsx` cho UI của route, `layout.tsx` cho shared layout, `loading.tsx` cho loading states, `error.tsx` cho error boundaries, `not-found.tsx` cho 404 pages. Server Components là default trong App Router, cho phép fetch data trực tiếp trong component mà không cần client-side fetching.

### 2. Server Components (Thành Phần Phía Server)

Server Components là các React components được render trên server và gửi HTML đến client. Server Components cho phép giảm JavaScript bundle size vì code không được gửi đến client. Chúng có thể truy cập trực tiếp vào backend resources như database mà không cần API layer. Server Components không thể sử dụng hooks hoặc browser APIs.

Để sử dụng Client Components, cần thêm directive `'use client'` ở đầu file. Client Components được hydrate trên client và có thể sử dụng hooks, event handlers, và browser APIs. Mixing Server và Client Components cho phép tối ưu hóa performance trong khi vẫn có interactive features.

### 3. Static Site Generation (SSG - Tạo Trang Tĩnh)

SSG là phương pháp tạo HTML tĩnh tại thời điểm build time. Trang được pre-rendered và có thể được serve từ CDN mà không cần server-side processing. SSG phù hợp cho content không thay đổi thường xuyên như blog posts, documentation, landing pages. Tốc độ load cực nhanh vì không cần server processing.

Trong Next.js, SSG được implement bằng cách export async function `generateStaticParams` hoặc sử dụng `getStaticProps`. Incremental Static Regeneration (ISR) cho phép update một số pages mà không cần rebuild toàn bộ site. Static pages có thể được regenerated khi có request (revalidate option).

### 4. Server-Side Rendering (SSR - Render Phía Server)

SSR là phương pháp render pages trên server mỗi khi có request. SSR đảm bảo content luôn fresh và có thể personalize content dựa trên request. SEO benefits vì content có sẵn trong initial HTML. SSR phù hợp cho content thay đổi thường xuyên hoặc cần real-time data.

Trong Next.js, SSR được implement bằng cách export async function `getServerSideProps` trong Pages Router hoặc trực tiếp trong Server Components với async functions. SSR có độ trễ cao hơn SSG vì cần server processing mỗi request, nhưng đảm bảo content luôn updated.

### 5. Client-Side Rendering (CSR - Render Phía Client)

CSR là phương pháp render pages trên client sử dụng JavaScript. Initial HTML chỉ chứa một shell, sau đó JavaScript fetch data và render content. CSR phù hợp cho dashboard, admin panels, hoặc personalized content không cần SEO. Tuy nhiên, CSR có thể gây ra loading delay và ảnh hưởng đến SEO.

Trong Next.js, CSR được implement bằng cách sử dụng hooks như `useEffect` và `useSWR` hoặc React Query để fetch data trong Client Components. Hybrid approach kết hợp SSR/SSG cho initial content và CSR cho interactive parts thường là best practice.

### 6. Incremental Static Regeneration (ISR - Tái Tạo Tĩnh Tăng Dần)

ISR cho phép tạo hoặc update static pages sau khi đã build. Thay vì rebuild toàn bộ site khi content thay đổi, ISR chỉ regenerate các pages cần thiết. ISR kết hợp benefits của cả SSG (speed) và SSR (fresh content). Revalidation có thể là time-based hoặc on-demand.

Trong Next.js, ISR được implement bằng cách export `revalidate` property từ `getStaticProps`. Revalidation interval xác định tần suất page được regenerated. On-demand revalidation sử dụng `revalidatePath` hoặc `revalidateTag` API để trigger regeneration từ CMS webhook hoặc user action.

### 7. Image Component (Thành Phần Hình Ảnh)

Next.js Image Component (`next/image`) cung cấp automatic image optimization: automatic resizing, format conversion (WebP/AVIF), lazy loading, và priority loading cho above-the-fold images. Image Component ngăn chặn Layout Shift bằng cách yêu cầu dimensions hoặc fill mode. Remote images cần được configured trong `next.config.js`.

Features bao gồm: `placeholder="blur"` cho blur-up effect, `priority` cho preload critical images, `sizes` để hint browser về responsive sizes, `fill` mode cho container-based layouts. Image Optimization API xử lý images on-the-fly và cache chúng cho performance tối ưu.

### 8. API Routes (Tuyến API)

API Routes cho phép tạo API endpoints trong Next.js app bằng cách tạo files trong thư mục `pages/api` (Pages Router) hoặc `app/api` (App Router). API Routes có thể handle GET, POST, PUT, DELETE requests. Serverless functions được tạo cho mỗi route, scale automatically theo demand.

Trong App Router, API Routes được implement như Route Handlers với file `route.ts`. Route Handlers có thể export functions cho các HTTP methods: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS. Dynamic API Routes sử dụng brackets syntax: `[id]/route.ts` cho `/api/items/[id]`.

### 9. Middleware (Phần Mềm Trung Gian)

Middleware cho phép execute code trước khi request được completed. Middleware có thể modify request/response, redirect users, rewrite paths, add headers. Middleware được chạy trên Edge Runtime, gần user nhất có thể để giảm latency. Middleware useful cho authentication, geolocation, A/B testing.

Trong Next.js, Middleware được tạo bằng file `middleware.ts` ở root của project. Middleware nhận `NextRequest` và có thể return `NextResponse`. Matcher config xác định routes nào middleware được applied. Middleware chạy trước tất cả routes trong App Router.

### 10. Dynamic Routes (Tuyến Động)

Dynamic Routes cho phép tạo routes với parameters, như `/products/[id]` hoặc `/blog/[slug]`. Dynamic segments được wrap trong brackets: `[param]`. Optional catch-all routes sử dụng `[...param]` để match multiple segments. Dynamic Routes cho phép tạo reusable pages cho các entities khác nhau.

Trong Next.js, dynamic segments có thể được access qua `params` prop trong page functions. `generateStaticParams` function xác định các giá trị của segment tại build time cho SSG. Nested dynamic routes như `[category]/[product]` cũng được supported.

### 11. Hydration (Hydration)

Hydration là quá trình React attach event handlers vào server-rendered HTML để make it interactive. Hydration xảy ra sau khi JavaScript bundle được tải xuống client. Mismatch giữa server và client rendering có thể gây ra hydration errors. Proper data handling và avoiding browser-only APIs trong server components giúp prevent hydration issues.

React 18 và Next.js 13+ cung cấp improved hydration với Automatic Client-Side Hydration và selective hydration. Suspense boundaries cho phép hydrate components independently, improving perceived performance.

### 12. Edge Runtime (Môi Trường Edge)

Edge Runtime là JavaScript runtime được execute trên Edge servers gần user nhất. Edge Runtime hỗ trợ subset của Node.js APIs và cho phép middleware và some Server Components chạy ở Edge. Edge Runtime có cold start nhanh hơn Serverless functions truyền thống. Memory limits và API restrictions apply.

Edge Runtime useful cho: geolocation-based routing, authentication, personalization, A/B testing. Not suitable cho heavy computations, large bundle sizes, hoặc Node.js-specific APIs.

### 13. Parallel Routes (Tuyến Song Song)

Parallel Routes cho phép render multiple routes trong cùng một layout sử dụng slots. Slots được define với `@folder` convention: `@analytics`, `@feed`. Parallel routes enable complex UI patterns như sidebars, modals, và dashboards. Active state của parallel routes được tracked independently.

Parallel routes hỗ trợ conditional rendering và intercepted routes. Intercepted routes cho phép show modal вместо full page navigation while preserving URL. This enables Instagram-like behavior where clicking opens modal but URL remains.

### 14. Route Groups (Nhóm Tuyến)

Route Groups cho phép organize routes mà không affect URL structure. Routes được wrap trong `(folder)` parentheses để create groups. Useful cho: organizing routes by feature, grouping layouts, separating public/authenticated routes. Routes trong cùng group share layouts.

Route groups không affect URL: `/app/(marketing)/about` becomes `/about`. Groups có thể có separate layouts hoặc share parent layout. Common pattern là use route groups để separate app sections: `(dashboard)`, `(marketing)`, `(auth)`.

### 15. Link Component (Thành Phần Liên Kết)

Link Component (`next/link`) cung cấp prefetching và client-side navigation mà không cần full page reload. Prefetching tải trước linked pages khi in viewport để improve navigation speed. Active state được tracked automatically. Link hỗ trợ all HTML anchor attributes.

Best practices: Always use Link thay vì `<a>` tags. Use `replace` prop để replace history entry thay vì push new one. Use `scroll={false}` để prevent scroll to top on navigation. Prefetch có thể được disabled với `prefetch={false}`.

### 16. Font Optimization (Tối Ưu Font)

Next.js tự động optimize fonts bằng cách self-host Google Fonts. Font files được downloaded at build time và served từ same origin. CLS (Cumulative Layout Shift) được prevented vì font metrics được preloaded. `next/font` module cung cấp zero-layout-shift fonts.

`next/font/google` và `next/font/local` cung cấp built-in font optimization. Fonts được loaded asynchronously để không block rendering. CSS variables cho phép customize font weights và styles.

### 17. Script Component (Thành Phần Script)

Script Component (`next/script`) cung cấp control over third-party script loading. Loading strategies: `beforeInteractive`, `afterInteractive`, `lazyOnload`. `beforeInteractive` scripts được load trước page becomes interactive, useful cho critical scripts. `afterInteractive` và `lazyOnload` được defer để improve performance.

Script Component support `onLoad` callback để run code sau khi script loaded. `strategy` prop xác định loading priority. `next/script` automatically handles script deduplication nếu same script được used multiple times.

### 18. Layouts (Bố Cục)

Layouts xác định shared UI được reuse across multiple pages. Root layout (`app/layout.tsx`) được apply cho tất cả pages. Nested layouts cho phép section-specific layouts. Layouts preserve state across navigations và không re-render khi route thay đổi.

Layouts nhận `children` prop chứa page hoặc nested layouts. Layouts có thể be Server hoặc Client Components. Template component (`app/template.tsx`) khác với layout ở chỗ re-renders on each navigation, useful cho animations.

## Kết luận

Từ điển thuật ngữ này cung cấp nền tảng kiến thức vững chắc về Next.js. Việc hiểu rõ từng thuật ngữ giúp xây dựng ứng dụng Next.js hiệu quả và tối ưu.
