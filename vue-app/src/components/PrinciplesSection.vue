<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const sectionRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()

interface Principle {
  id: number
  icon: string
  number: string
  title: string
  description: string
  tags: string[]
}

const principles: Principle[] = [
  {
    id: 1,
    icon: 'grid',
    number: '01 / 04',
    title: 'Memory First',
    description: 'Luôn tra cứu memory trước khi bắt đầu task. Tránh lặp lại quyết định đã có, tái sử dụng ADRs và bug fixes.',
    tags: ['decisions.sqlite', 'bug-history']
  },
  {
    id: 2,
    icon: 'search',
    number: '02 / 04',
    title: 'Retrieval First',
    description: 'Luôn retrieval knowledge trước khi hỏi. Semantic search qua 272 knowledge files thay vì guess.',
    tags: ['knowledge-base', 'semantic-search']
  },
  {
    id: 3,
    icon: 'zap',
    number: '03 / 04',
    title: 'Token Optimization',
    description: 'Tối ưu token ở mọi bước. Context Router, Auto-Compression, Lazy Loading giảm tiêu thụ đến 40%.',
    tags: ['context-router', 'lazy-load']
  },
  {
    id: 4,
    icon: 'users',
    number: '04 / 04',
    title: 'Knowledge Reuse',
    description: 'Tái sử dụng existing decisions và solutions. Không tạo lại những gì đã có — chỉ adapt và extend.',
    tags: ['adr', 'pattern-reuse']
  }
]

const visibleCards = ref<Set<number>>(new Set())

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      principles.forEach((_, index) => {
        setTimeout(() => {
          visibleCards.value.add(index)
        }, index * 80)
      })
    }, { threshold: 0.1 })
  }
})
</script>

<template>
  <section class="principles-section" id="principles" ref="sectionRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Core Philosophy</div>
        <h2 class="section-title">4 Nguyên tắc cốt lõi</h2>
        <p class="section-desc">
          Mọi quyết định thiết kế đều phục vụ cho việc tối ưu hóa hiệu suất AI agent.
          Mỗi nguyên tắc được implement cụ thể trong framework.
        </p>
      </div>

      <div class="principles-grid">
        <div
          v-for="(principle, index) in principles"
          :key="principle.id"
          class="principle-card"
          :class="{ visible: visibleCards.has(index) }"
        >
          <div class="principle-icon">
            <svg v-if="principle.icon === 'grid'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
              <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
            </svg>
            <svg v-else-if="principle.icon === 'search'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
            </svg>
            <svg v-else-if="principle.icon === 'zap'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>
            </svg>
          </div>
          <div class="principle-number">{{ principle.number }}</div>
          <h3>{{ principle.title }}</h3>
          <p>{{ principle.description }}</p>
          <div class="principle-tags">
            <span v-for="tag in principle.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.principles-section {
  padding: var(--section-py) 0;
  background: var(--gradient-surface);
}

.principles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-top: 48px;
}

.principle-card {
  position: relative;
  padding: 28px;
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-soft);
  background: var(--bg-surface);
  overflow: hidden;
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.5s var(--ease-out), transform 0.5s var(--ease-out),
              border-color var(--t-base), box-shadow var(--t-base);
}

.principle-card.visible {
  opacity: 1;
  transform: translateY(0);
}

.principle-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, transparent 60%, rgba(120, 119, 232, 0.04) 100%);
  pointer-events: none;
}

.principle-card:hover {
  border-color: var(--border-accent);
  box-shadow: var(--shadow-glow);
  transform: translateY(-3px);
}

.principle-icon {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-md);
  background: var(--accent-glow);
  border: 1px solid var(--border-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
}

.principle-icon svg {
  width: 20px;
  height: 20px;
  stroke: var(--accent-primary);
}

.principle-number {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.15em;
  color: var(--text-faint);
  font-family: var(--font-mono);
  margin-bottom: 10px;
  position: relative;
  z-index: 1;
}

.principle-card h3 {
  font-size: 17px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 10px;
  position: relative;
  z-index: 1;
  letter-spacing: -0.01em;
}

.principle-card p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.65;
  margin-bottom: 18px;
  position: relative;
  z-index: 1;
}

.principle-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  position: relative;
  z-index: 1;
}

.tag {
  font-size: 10.5px;
  font-weight: 600;
  font-family: var(--font-mono);
  color: var(--accent-primary);
  background: var(--accent-glow);
  border: 1px solid var(--border-accent);
  padding: 3px 8px;
  border-radius: var(--radius-full);
}
</style>
