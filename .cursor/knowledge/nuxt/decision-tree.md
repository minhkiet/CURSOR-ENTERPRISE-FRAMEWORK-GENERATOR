# Nuxt.js Decision Tree - Cây Quyết Định

## Mục lục
1. [Data Fetching Decision](#1-data-fetching-decision)
2. [State Management Decision](#2-state-management-decision)
3. [Rendering Mode Decision](#3-rendering-mode-decision)
4. [Component Decision](#4-component-decision)
5. [API Route Decision](#5-api-route-decision)

---

## 1. Data Fetching Decision

```
Bạn cần fetch data?
│
├── Data cần SSR support?
│   ├── YES
│   │   └── Fetch logic phức tạp?
│   │       ├── YES ────────────────────────────────→ → → useAsyncData
│   │       │                                              └── Custom transform, multiple sources
│   │       │
│   │       └── NO (simple request) ─────────────────→ → → useFetch
│   │                                                              └── Auto key, simpler syntax
│   │
│   └── NO (client-only)
│       │
│       └── Cần reactive updates?
│           ├── YES ────────────────────────────────→ → → useFetch với watch
│           │                                              └── watch: [query]
│           │
│           └── NO ──────────────────────────────────→ → → $fetch trong onMounted
│                                                              └── Simple, one-time fetch
│
└── (End)
```

---

## 2. State Management Decision

```
Bạn cần quản lý state?
│
├── State là simple primitive value?
│   ├── YES
│   │   └── Cần share giữa multiple components?
│   │       ├── YES ────────────────────────────────→ → → useState
│   │       │                                              └── const count = useState('count', () => 0)
│   │       │
│   │       └── NO (local to one component) ────────→ → → ref
│   │                                                              └── const count = ref(0)
│   │
│   └── NO (complex state)
│       │
│       └── State cần actions/logic?
│           ├── YES ────────────────────────────────→ → → Pinia Store
│           │                                              └── defineStore with actions
│           │
│           └── NO (just complex data) ──────────────→ → → useState
│                                                              └── useState('data', () => ({...}))
│
└── (End)
```

---

## 3. Rendering Mode Decision

```
Bạn cần chọn rendering mode?
│
├── Trang là static (không thay đổi)?
│   ├── YES ────────────────────────────────────────→ → → Prerender
│   │                                                      └── routeRules: { '/': { prerender: true } }
│   │
│   └── NO
│       │
│       └── Trang là semi-static (thay đổi sometimes)?
│           ├── YES ────────────────────────────────→ → → ISR/SWR
│           │                                              └── routeRules: { '/blog/**': { swr: 3600 } }
│           │
│           └── NO (always changing)
│               │
│               └── Trang là user-specific?
│                   ├── YES ────────────────────────────────→ → → SSR
│                   │                                              └── routeRules: { '/profile/**': { ssr: true } }
│                   │
│                   └── NO (highly interactive app)
│                       └── → → → SPA/CSR
│                               └── routeRules: { '/dashboard/**': { ssr: false } }
│
└── (End)
```

---

## 4. Component Decision

```
Bạn cần tạo component?
│
├── Component là heavy (chart, editor)?
│   ├── YES ────────────────────────────────────────→ → → defineAsyncComponent
│   │                                                      └── Lazy load
│   │
│   └── NO
│       │
│       └── Component cần run trên client only?
│           ├── YES ────────────────────────────────→ → → ClientOnly wrapper
│           │                                              └── <ClientOnly><MyComponent /></ClientOnly>
│           │
│           └── NO
│               │
│               └── Component là optional/conditional?
│                   ├── YES ────────────────────────────────→ → → Lazy với v-if
│                   │                                              └── <LazyOptionalComponent v-if="show" />
│                   │
│                   └── NO ──────────────────────────────────→ → → Regular component
│                                                              └── Auto-imported từ components/
│
└── (End)
```

---

## 5. API Route Decision

```
Bạn cần tạo API route?
│
├── HTTP method?
│   ├── GET ───────────────────────────────────────→ → → [name].get.ts
│   │
│   ├── POST ───────────────────────────────────────→ → → [name].post.ts
│   │
│   ├── PUT ───────────────────────────────────────→ → → [name].put.ts
│   │
│   ├── DELETE ─────────────────────────────────────→ → → [name].delete.ts
│   │
│   └── PATCH ──────────────────────────────────────→ → → [name].patch.ts
│
├── Route có dynamic params?
│   ├── YES
│   │   └── → → → server/api/[resource]/[id].get.ts
│   │        └── └── Access với getRouterParam(event, 'id')
│   │
│   └── NO ─────────────────────────────────────────→ → → server/api/[resource]/index.get.ts
│
└── Input validation?
    ├── YES
    │   └── → → → Use Zod schema
    │        └── validate với schema.safeParse(body)
    │
    └── NO ─────────────────────────────────────────→ → → Direct usage
```

---

## Quick Reference

### Data Fetching
```
Simple request + SSR → useFetch
Complex logic + SSR → useAsyncData
Client-only reactive → useFetch + watch
One-time client fetch → $fetch in onMounted
```

### State
```
Local primitive → ref
Shared primitive → useState
Complex state + logic → Pinia
Persistent → useCookie or Pinia persist
```

### Rendering
```
Static (docs, blog) → prerender
Semi-static (products) → swr
User-specific (profile) → ssr
Interactive (dashboard) → ssr: false
```

### Components
```
Heavy (charts, maps) → defineAsyncComponent
Client-only (intercom) → ClientOnly
Optional → v-if + lazy
Regular → auto-import
```

### API Routes
```
GET → .get.ts
POST → .post.ts
PUT → .put.ts
DELETE → .delete.ts
Dynamic → [param].ts
```

---

## Liên kết liên quan
- [Nuxt Glossary](./glossary.md)
- [Nuxt Architecture](./architecture.md)
- [Nuxt Best Practices](./best-practice.md)
- [Nuxt Anti-Patterns](./anti-pattern.md)
- [Nuxt Checklist](./checklist.md)
- [Nuxt FAQ](./faq.md)
