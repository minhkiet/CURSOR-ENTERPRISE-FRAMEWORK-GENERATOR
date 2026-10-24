# Vue 3 + TypeScript Stack

> **Version:** 1.0.0 | **Framework:** Vue 3 | **Language:** TypeScript

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Vue 3.4+ (Composition API) |
| Language | TypeScript 5.0+ (strict mode) |
| Build | Vite 5+ |
| Styling | Tailwind CSS 3+ |
| State | Pinia |
| Router | Vue Router 4 |
| HTTP | Axios |
| Testing | Vitest + Vue Test Utils |

---

## Project Structure

```
src/
├── assets/                 # Static assets
├── components/             # Vue components
│   ├── ui/               # Base UI components
│   │   ├── BaseButton.vue
│   │   ├── BaseInput.vue
│   │   └── BaseCard.vue
│   └── features/         # Feature components
│       ├── UserList.vue
│       └── ProductCard.vue
├── composables/           # Vue composables
│   ├── useAuth.ts
│   ├── useFetch.ts
│   └── useForm.ts
├── stores/               # Pinia stores
│   ├── auth.ts
│   ├── user.ts
│   └── cart.ts
├── views/                 # Route views
│   ├── HomeView.vue
│   ├── LoginView.vue
│   └── DashboardView.vue
├── router/               # Vue Router
│   └── index.ts
├── services/             # API services
│   ├── api.ts
│   ├── authService.ts
│   └── userService.ts
├── types/                 # TypeScript types
│   ├── api.ts
│   ├── user.ts
│   └── index.ts
├── utils/                 # Utilities
│   ├── formatters.ts
│   └── validators.ts
├── App.vue
└── main.ts
```

---

## Component Pattern

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

// Types
interface Props {
  title: string;
  count?: number;
}

interface Emits {
  (e: 'update', value: string): void;
  (e: 'delete', id: number): void;
}

// Props & Emits
const props = withDefaults(defineProps<Props>(), {
  count: 0
});

const emit = defineEmits<Emits>();

// State
const isLoading = ref(false);
const localValue = ref('');

// Computed
const doubledCount = computed(() => props.count * 2);

// Methods
function handleSubmit() {
  emit('update', localValue.value);
  localValue.value = '';
}

// Lifecycle
onMounted(() => {
  console.log('Component mounted');
});
</script>

<template>
  <div class="component">
    <h2>{{ title }}</h2>
    <p>Count: {{ doubledCount }}</p>
    
    <input v-model="localValue" type="text" />
    <button @click="handleSubmit">Submit</button>
  </div>
</template>

<style scoped>
.component {
  padding: 1rem;
}
</style>
```

---

## Pinia Store Pattern

```typescript
// stores/user.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { User } from '@/types';

export const useUserStore = defineStore('user', () => {
  // State
  const users = ref<User[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  
  // Getters
  const activeUsers = computed(() => 
    users.value.filter(u => u.status === 'active')
  );
  
  const userCount = computed(() => users.value.length);
  
  // Actions
  async function fetchUsers() {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await fetch('/api/users');
      users.value = await response.json();
    } catch (e) {
      error.value = 'Failed to fetch users';
    } finally {
      isLoading.value = false;
    }
  }
  
  async function createUser(data: CreateUserDto): Promise<User> {
    const response = await fetch('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) throw new Error('Failed to create user');
    
    const user = await response.json();
    users.value.push(user);
    return user;
  }
  
  return {
    // State
    users,
    isLoading,
    error,
    // Getters
    activeUsers,
    userCount,
    // Actions
    fetchUsers,
    createUser
  };
});
```

---

## API Service Pattern

```typescript
// services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
});

// Request interceptor
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      // Refresh token or logout
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// services/userService.ts
import api from './api';
import type { User, CreateUserDto } from '@/types';

export const userService = {
  getAll(params?: ListParams) {
    return api.get<{ data: User[]; meta: Meta }>('/users', { params });
  },
  
  getById(id: string) {
    return api.get<User>(`/users/${id}`);
  },
  
  create(data: CreateUserDto) {
    return api.post<User>('/users', data);
  },
  
  update(id: string, data: UpdateUserDto) {
    return api.put<User>(`/users/${id}`, data);
  },
  
  delete(id: string) {
    return api.delete(`/users/${id}`);
  }
};
```

---

## Testing Pattern

```typescript
// components/UserList.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import UserList from './UserList.vue';

// Mock composable
vi.mock('@/stores/user', () => ({
  useUserStore: () => ({
    users: [
      { id: '1', name: 'John', email: 'john@test.com' }
    ],
    isLoading: false,
    fetchUsers: vi.fn()
  })
}));

describe('UserList', () => {
  it('renders user list', () => {
    const wrapper = mount(UserList);
    expect(wrapper.findAll('.user-item')).toHaveLength(1);
  });
  
  it('displays loading state', () => {
    vi.mock('@/stores/user', () => ({
      useUserStore: () => ({
        users: [],
        isLoading: true,
        fetchUsers: vi.fn()
      })
    }));
    
    const wrapper = mount(UserList);
    expect(wrapper.find('.loading').exists()).toBe(true);
  });
});
```

---

## Checklist

```
┌─────────────────────────────────────────────────────────────┐
│ Vue 3 + TypeScript Checklist                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ □ Vue 3 Composition API (setup script)                     │
│ □ TypeScript strict mode                                  │
│ □ Proper type definitions                                  │
│ □ Pinia stores for state                                  │
│ □ Composables for reusable logic                          │
│ □ Vue Router for navigation                               │
│ □ Axios with interceptors                                 │
│ □ Vitest for testing                                     │
│ □ Tailwind for styling                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
