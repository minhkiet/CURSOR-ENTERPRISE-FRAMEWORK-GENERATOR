# Vue Architecture - Kiến Trúc Vue.js

## Tổng quan

Vue.js là framework progressive cho xây dựng giao diện người dùng. Kiến trúc Vue tập trung vào component-based development, reactivity, và developer experience.

## Kiến trúc chi tiết

### 1. Project Structure

```
├── src/
│   ├── assets/          # Static assets
│   ├── components/       # Reusable components
│   ├── composables/     # Composition functions
│   ├── layouts/        # Page layouts
│   ├── pages/           # Page components
│   ├── plugins/         # Vue plugins
│   ├── router/          # Vue Router config
│   ├── stores/          # Pinia stores
│   ├── types/           # TypeScript types
│   ├── App.vue          # Root component
│   └── main.ts          # Entry point
├── public/              # Static files
└── package.json
```

### 2. Component Architecture

**Single-File Components**: Template + Script + Style trong `.vue` file. Script setup syntax cho cleaner code. TypeScript support tích hợp.

**Component Patterns**: Container/Presentational separation. Provider/Consumer pattern. Slots cho composition.

### 3. State Management (Pinia)

**Store Structure**:
```typescript
export const useUserStore = defineStore('user', {
  state: () => ({ name: '', email: '' }),
  getters: { fullName: (state) => `${state.name}` },
  actions: { async fetchUser() { /* */ } }
})
```

**Usage**: `const store = useUserStore()`

### 4. Vue Router

**Route Definition**:
```typescript
const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About },
  { path: '/users/:id', component: UserDetail }
]
```

### 5. Composables

**Pattern**:
```typescript
export function useCounter() {
  const count = ref(0)
  const increment = () => count.value++
  return { count, increment }
}
```

## Deployment

### Build & Deploy

```bash
npm run build
npm run preview
```

Deploy lên Vercel, Netlify, hoặc any static host.

## Kết luận

Vue cung cấp flexible architecture phù hợp cho mọi project size.
