# Nuxt Architecture - Kiến Trúc Nuxt.js

## Tổng quan

Nuxt.js là full-stack framework built on top of Vue.js. Cung cấp SSR, SSG, hybrid rendering. File-based routing, auto-imports, server routes.

## Kiến trúc chi tiết

### 1. Directory Structure

```
├── app/
│   ├── components/     # Auto-imported components
│   ├── composables/   # Auto-imported composables
│   ├── layouts/       # Page layouts
│   ├── pages/          # File-based routing
│   ├── plugins/       # Vue plugins
│   └── App.vue        # Root component
├── assets/            # Static assets
├── components/        # (legacy location)
├── composables/       # (legacy location)
├── layouts/          # (legacy location)
├── pages/           # (legacy location)
├── plugins/         # (legacy location)
├── public/          # Static files
├── server/          # Server-side code
│   ├── api/         # REST endpoints
│   ├── middleware/   # Server middleware
│   └── utils/       # Server utilities
├── nuxt.config.ts    # Configuration
└── package.json
```

### 2. Rendering Modes

**SSR**: Server-side rendering với hydration.
**SSG**: Pre-rendered at build time.
**Hybrid**: Mix of SSR/SSG/SPA per page.

### 3. Data Fetching

```typescript
// Server-side
const { data } = await useAsyncData('key', () => $fetch('/api/data'))

// Client-side
const { data } = await useFetch('/api/data')
```

### 4. Server Routes

```typescript
// server/api/users.get.ts
export default defineEventHandler(() => {
  return [{ id: 1, name: 'John' }]
})
```

### 5. State Management

```typescript
// Global state
const count = useState('count', () => 0)

// Pinia integration available
```

### 6. Deployment

- Vercel, Netlify (serverless)
- Node.js server (self-hosted)
- Docker containers

## Kết luận

Nuxt cung cấp complete full-stack Vue solution với powerful features.
