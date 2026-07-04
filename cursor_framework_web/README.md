# CEF Landing Vue 3 App

> Enterprise-grade Vue 3 landing page cho **Cursor Enterprise Framework v5.0.0** — synced 2026-07-04.

## What's New

### Landing Page Templates Gallery (v5.0)
Bộ sưu tập **6 landing page templates** HTML/CSS/JS thuần, đẹp mắt, responsive, tối ưu conversion.

**Truy cập:** [/#/templates](http://localhost:5173/#/templates) sau khi chạy dev server.

#### 6 Templates bao gồm:

| # | Template | Industry | Phong cách |
|---|----------|----------|------------|
| 1 | **CRM Dashboard** | CRM/SaaS | Violet/cyan, dashboard mockup |
| 2 | **Sale Pro** | E-commerce | Orange/gold, flash sale, countdown |
| 3 | **Bazi Tử Vi** | Tử Vi/Phong thủy | Dark + vàng, cổ điển Á Đông |
| 4 | **Numerology Life** | Thần số học | Cosmic dark, stars canvas |
| 5 | **Blog Editorial** | Magazine/Blog | Serif typography, dark mode |
| 6 | **Portfolio Studio** | Designer/Dev | Editorial Fraunces, masonry |

#### Tính năng Gallery:
- **Preview iframe**: xem demo trực tiếp trong browser (desktop/tablet/mobile)
- **Sidebar thông tin**: tagline, highlights, features, tech stack, file info
- **Tải về riêng lẻ**: download file zip từng template
- **Tải bộ đầy đủ**: download tất cả 6 templates
- **Xem source**: mở HTML trực tiếp trong tab mới
- **Responsive preview**: switch giữa desktop/tablet/mobile
- **Search + Category filter**: lọc theo tên, tag, industry

#### Cấu trúc templates:
```
public/templates/
├── crm/          # index.html, styles.css, script.js
├── sale/         # index.html, styles.css, script.js
├── bazi/         # index.html, styles.css, script.js
├── numerology/   # index.html, styles.css, script.js
├── blog/         # index.html, styles.css, script.js
└── portfolio/    # index.html, styles.css, script.js
```

Mỗi template là standalone HTML/CSS/JS, không phụ thuộc vào framework. Có thể copy trực tiếp vào bất kỳ project nào.

---

## Tech Stack

- **Vue 3** với Composition API và `<script setup>`
- **TypeScript** cho type safety
- **Vue Router 4** cho SPA navigation (3 routes: home, templates, template/:id)
- **Vite** cho fast development và building
- **CSS Variables** cho design tokens

## Features

- Responsive design với mobile-first approach
- Dark theme với premium SaaS aesthetic
- Vue Router với hash-based routing
- Intersection Observer animations
- Interactive components showcase
- Rules & Skills explorer với search và filtering
- Token optimization visualization
- **6 Landing page templates gallery với iframe preview**
- Copy-to-clipboard functionality
- Smooth scroll navigation

## Project Structure

```
cursor_framework_web/
├── src/
│   ├── components/         # 12 section components
│   ├── composables/        # useIntersectionObserver
│   ├── views/              # 3 router views (NEW)
│   │   ├── HomeView.vue
│   │   ├── TemplatesGallery.vue
│   │   └── TemplatePreview.vue
│   ├── data/               # Template metadata (NEW)
│   │   └── templates.ts
│   ├── router.ts           # Vue Router config (NEW)
│   ├── styles/
│   │   ├── main.css
│   │   └── templates.css   # Gallery styles (NEW)
│   ├── App.vue
│   └── main.ts
├── public/
│   ├── favicon.svg
│   └── templates/          # 6 standalone templates (NEW)
│       ├── crm/
│       ├── sale/
│       ├── bazi/
│       ├── numerology/
│       ├── blog/
│       └── portfolio/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
└── tsconfig.node.json
```

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev      # → http://localhost:5173

# Build for production
npm run build

# Preview production build
npm run preview  # → http://localhost:4173
```

## Routing

| Route | Page |
|-------|------|
| `/#/` | Home (framework showcase) |
| `/#/templates` | Templates gallery (6 templates grid) |
| `/#/templates/:id` | Template preview (iframe demo + download) |

Available template IDs: `crm`, `sale`, `bazi`, `numerology`, `blog`, `portfolio`

## Deployment

The app is configured for Vercel deployment via `vercel.json`:
- Framework: Vite
- Build command: `npm run build`
- Output directory: `dist`
- Static templates in `public/templates/` are served at `/templates/:id/`

## License

MIT