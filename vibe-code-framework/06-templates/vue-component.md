# Vue 3 Component Template

> **Version:** 1.0.0 | **Framework:** Vue 3 | **Language:** TypeScript

---

## Single File Component Template

```vue
<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';

// Props
interface Props {
  title: string;
  count?: number;
  items?: string[];
}

const props = withDefaults(defineProps<Props>(), {
  count: 0,
  items: () => []
});

// Emits
const emit = defineEmits<{
  (e: 'update', value: string): void;
  (e: 'delete', id: number): void;
}>();

// State
const isLoading = ref(false);
const inputValue = ref('');

// Computed
const displayCount = computed(() => props.count * 2);
const hasItems = computed(() => props.items.length > 0);

// Watch
watch(() => props.title, (newTitle) => {
  console.log('Title changed:', newTitle);
});

// Lifecycle
onMounted(() => {
  console.log('Component mounted');
});

// Methods
function handleInput(event: Event) {
  const target = event.target as HTMLInputElement;
  inputValue.value = target.value;
}

function submitValue() {
  emit('update', inputValue.value);
  inputValue.value = '';
}

function deleteItem(id: number) {
  emit('delete', id);
}
</script>

<template>
  <div class="component">
    <h2>{{ title }}</h2>
    
    <p>Count: {{ displayCount }}</p>
    
    <div v-if="hasItems" class="items">
      <div 
        v-for="(item, index) in items" 
        :key="index"
        class="item"
      >
        {{ item }}
        <button @click="deleteItem(index)">Delete</button>
      </div>
    </div>
    
    <div v-else class="empty">
      No items
    </div>
    
    <input 
      v-model="inputValue"
      type="text"
      placeholder="Enter value"
      @input="handleInput"
    />
    
    <button 
      :disabled="!inputValue"
      @click="submitValue"
    >
      Submit
    </button>
    
    <div v-if="isLoading" class="loading">
      Loading...
    </div>
  </div>
</template>

<style scoped>
.component {
  padding: 1rem;
}

.items {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.empty {
  padding: 1rem;
  color: #666;
  text-align: center;
}

input {
  width: 100%;
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.5rem 1rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loading {
  margin-top: 1rem;
  color: #666;
}
</style>
```

## Composition API Options Pattern

```vue
<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';

export default defineComponent({
  name: 'MyComponent',
  
  props: {
    title: {
      type: String,
      required: true
    },
    initialCount: {
      type: Number,
      default: 0
    }
  },
  
  emits: ['update', 'delete'],
  
  setup(props, { emit }) {
    const count = ref(props.initialCount);
    const inputValue = ref('');
    
    const doubleCount = computed(() => count.value * 2);
    
    function increment() {
      count.value++;
    }
    
    function submit() {
      emit('update', inputValue.value);
      inputValue.value = '';
    }
    
    onMounted(() => {
      console.log('Mounted with title:', props.title);
    });
    
    return {
      count,
      inputValue,
      doubleCount,
      increment,
      submit
    };
  }
});
</script>
```

## TypeScript Interface

```typescript
// types/MyComponent.ts
export interface MyComponentProps {
  title: string;
  count?: number;
  items?: string[];
}

export interface MyComponentEmits {
  (e: 'update', value: string): void;
  (e: 'delete', id: number): void;
}

export interface MyComponentSlots {
  default(): any;
  footer(): any;
}
```

## Test Template

```typescript
// components/MyComponent.test.ts
import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import MyComponent from './MyComponent.vue';

describe('MyComponent', () => {
  const defaultProps = {
    title: 'Test Title',
    count: 5,
    items: ['Item 1', 'Item 2']
  };

  it('renders title', () => {
    const wrapper = mount(MyComponent, {
      props: defaultProps
    });
    
    expect(wrapper.find('h2').text()).toBe('Test Title');
  });

  it('displays doubled count', () => {
    const wrapper = mount(MyComponent, {
      props: defaultProps
    });
    
    expect(wrapper.text()).toContain('Count: 10');
  });

  it('emits update event', async () => {
    const wrapper = mount(MyComponent, {
      props: defaultProps
    });
    
    await wrapper.find('input').setValue('test');
    await wrapper.find('button').trigger('click');
    
    expect(wrapper.emitted('update')).toBeTruthy();
    expect(wrapper.emitted('update')![0]).toEqual(['test']);
  });
});
```
