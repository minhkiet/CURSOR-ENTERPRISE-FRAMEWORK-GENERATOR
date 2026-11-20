<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const sectionRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()

interface Principle {
  id: number
  icon: string
  title: string
  description: string
  meta: string
}

const principles: Principle[] = [
  {
    id: 1,
    icon: 'database',
    title: 'Memory first',
    description: 'Before any task, query local memory for past decisions, ADRs, and bug fixes. Avoid re-deriving what is already known.',
    meta: 'decisions.sqlite'
  },
  {
    id: 2,
    icon: 'search',
    title: 'Retrieval first',
    description: 'Semantic search across 272 knowledge files beats guessing. Load only what the current task needs.',
    meta: 'knowledge base'
  },
  {
    id: 3,
    icon: 'zap',
    title: 'Token optimization',
    description: 'Context router, auto-compression, and lazy loading cut context use by up to 40 percent on long sessions.',
    meta: 'context router'
  },
  {
    id: 4,
    icon: 'share',
    title: 'Knowledge reuse',
    description: 'Reuse existing patterns, conventions, and solutions. Adapt and extend, never rebuild from scratch.',
    meta: 'patterns.db'
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
        <div class="section-label">Principles</div>
        <h2 class="section-title">Four rules that shape every decision.</h2>
        <p class="section-desc">
          Not aspirational guidelines. These are mechanical behaviors enforced by the framework,
          measurable in token count, latency, and retrieval accuracy.
        </p>
      </div>

      <div class="principles-grid">
        <article
          v-for="(principle, index) in principles"
          :key="principle.id"
          class="principle-card"
          :class="{ visible: visibleCards.has(index) }"
        >
          <div class="principle-number">{{ String(principle.id).padStart(2, '0') }}</div>
          <div class="principle-icon">
            <svg v-if="principle.icon === 'database'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>
            <svg v-else-if="principle.icon === 'search'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
            <svg v-else-if="principle.icon === 'zap'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
          </div>
          <h3 class="principle-title">{{ principle.title }}</h3>
          <p class="principle-desc">{{ principle.description }}</p>
          <code class="principle-meta">{{ principle.meta }}</code>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.principles-section {
  padding: var(--section-py) 0;
}

.principles-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.principle-card {
  padding: 28px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  display: flex;
  flex-direction: column;
  gap: 16px;
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 500ms var(--ease-out-quart), transform 500ms var(--ease-out-quart), border-color var(--t-base);
  position: relative;
  overflow: hidden;
}

.principle-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  transition: left 800ms var(--ease-out-quart);
  transition-delay: var(--delay, 0ms);
}

.principle-card.visible::after {
  left: 100%;
}

.principle-card.visible {
  opacity: 1;
  transform: translateY(0);
}

.principle-card:hover {
  border-color: var(--accent-line);
  background: var(--bg-elevated);
  transform: translateY(-3px);
}

.principle-card:hover .principle-icon {
  background: var(--accent-dim);
  transform: scale(1.05);
}

.principle-number {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  letter-spacing: 0.04em;
}

.principle-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  transition: all var(--t-base);
}

.principle-icon svg {
  width: 22px;
  height: 22px;
}

.principle-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.015em;
  line-height: 1.2;
}

.principle-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  flex: 1;
}

.principle-meta {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
  padding: 4px 8px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-hairline);
  border-radius: var(--radius-sm);
  align-self: flex-start;
}

@media (max-width: 1024px) {
  .principles-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .principles-grid {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .principle-card,
  .principle-icon {
    transition: none !important;
  }
  .principle-card::after {
    display: none;
  }
  .principle-card:hover {
    transform: none;
  }
  .principle-card:hover .principle-icon {
    transform: none;
  }
}
</style>