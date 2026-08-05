<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const sectionRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()

interface Domain {
  id: string
  title: string
  description: string
  ruleCount: number
  skillCount: number
  icon: string
  highlights: string[]
}

const domains: Domain[] = [
  {
    id: 'frontend',
    title: 'Frontend',
    description: 'React, Next.js, Vue, Nuxt. Design tokens, component APIs, SSR patterns.',
    ruleCount: 4,
    skillCount: 3,
    icon: 'layout',
    highlights: ['Next.js App Router', 'Server vs Client Components', 'Tailwind v4 + design tokens']
  },
  {
    id: 'backend',
    title: 'Backend',
    description: 'NestJS, Laravel, ASP.NET Core. APIs, transactions, concurrency, IDOR.',
    ruleCount: 5,
    skillCount: 3,
    icon: 'server',
    highlights: ['Clean architecture', 'Repository pattern', 'OAuth + JWT standards']
  },
  {
    id: 'database',
    title: 'Database',
    description: 'Postgres, MySQL, SQL Server, RLS, vector search, query optimization.',
    ruleCount: 3,
    skillCount: 2,
    icon: 'database',
    highlights: ['Row level security', 'Connection pooling', 'pgvector for RAG']
  },
  {
    id: 'cloud',
    title: 'Cloud & Infra',
    description: 'AWS, Cloudflare, Vercel. Serverless, edge functions, IaC patterns.',
    ruleCount: 4,
    skillCount: 3,
    icon: 'cloud',
    highlights: ['Edge runtime', 'Workers + queues', 'IaC with Terraform']
  },
  {
    id: 'ai',
    title: 'AI & RAG',
    description: 'Vector search, WeKnora, embeddings, context routing, prompt patterns. TDAM layered memory.',
    ruleCount: 4,
    skillCount: 4,
    icon: 'brain',
    highlights: ['TDAM 4-layer memory (L0–L3)', 'Hybrid retrieval', 'Context window mgmt']
  },
  {
    id: 'security',
    title: 'Security',
    description: 'OWASP Top 10, secrets management, auth flows, payment security.',
    ruleCount: 4,
    skillCount: 2,
    icon: 'shield',
    highlights: ['STRIDE threat model', 'Zero trust', 'Vietnam payment standards']
  }
]

const isVisible = ref(false)

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      isVisible.value = true
    }, { threshold: 0.05 })
  }
})
</script>

<template>
  <section class="domains-section" id="domains" ref="sectionRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Domains</div>
        <h2 class="section-title">Six domains. One consistent standard.</h2>
        <p class="section-desc">
          Each domain bundles its own rules, skills, and patterns. Agents pull only what's relevant
          to the current task, no more context bloat.
        </p>
      </div>

      <div class="domains-grid">
        <article
          v-for="(domain, i) in domains"
          :key="domain.id"
          class="domain-card"
          :style="{ '--delay': `${i * 60}ms` }"
        >
          <div class="domain-head">
            <div class="domain-icon">
              <svg v-if="domain.icon === 'layout'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>
              <svg v-else-if="domain.icon === 'server'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><line x1="6" y1="6" x2="6.01" y2="6"/></svg>
              <svg v-else-if="domain.icon === 'database'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>
              <svg v-else-if="domain.icon === 'cloud'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M18 10h-1.26A8 8 0 109 20h9a5 5 0 000-10z"/></svg>
              <svg v-else-if="domain.icon === 'brain'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2a4 4 0 00-4 4c0 1.95 1.4 3.58 3.25 3.92L11 10H8a4 4 0 00-4 4c0 1.95 1.4 3.58 3.25 3.92L7 18a4 4 0 004 4"/><path d="M12 2a4 4 0 014 4c0 1.95-1.4 3.58-3.25 3.92L13 10h3a4 4 0 014 4c0 1.95-1.4 3.58-3.25 3.92L17 18a4 4 0 01-4 4"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <div class="domain-badges">
              <span class="domain-badge">{{ domain.ruleCount }} rules</span>
              <span class="domain-badge">{{ domain.skillCount }} skills</span>
            </div>
          </div>

          <h3 class="domain-title">{{ domain.title }}</h3>
          <p class="domain-desc">{{ domain.description }}</p>

          <ul class="domain-highlights">
            <li v-for="h in domain.highlights" :key="h">
              <span class="hl-dot"></span>
              {{ h }}
            </li>
          </ul>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.domains-section {
  padding: var(--section-py) 0;
}

.domains-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.domain-card {
  padding: 28px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  display: flex;
  flex-direction: column;
  gap: 14px;
  opacity: 0;
  animation: fade-in-up 500ms var(--ease-out-quart) both;
  animation-delay: var(--delay);
  transition: border-color var(--t-base), background var(--t-base);
}

.is-visible .domain-card {
  opacity: 1;
}

.domain-card:hover {
  border-color: var(--accent-line);
  background: var(--bg-elevated);
  transform: translateY(-2px);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(16, 185, 129, 0.1);
}

.domain-card:hover .domain-icon {
  transform: rotate(-6deg) scale(1.05);
  background: var(--accent-dim);
}

.domain-card:hover .hl-dot {
  background: var(--accent-bright);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.18);
}

.domain-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.domain-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  transition: transform var(--t-base), background var(--t-base);
}

.domain-icon svg {
  width: 20px;
  height: 20px;
}

.domain-badges {
  display: flex;
  gap: 6px;
}

.domain-badge {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 500;
  color: var(--text-tertiary);
  padding: 3px 7px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
}

.domain-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.015em;
}

.domain-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.55;
}

.domain-highlights {
  list-style: none;
  padding-top: 12px;
  border-top: 1px solid var(--border-hairline);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.domain-highlights li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-secondary);
  font-family: var(--font-mono);
}

.hl-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--accent);
  transition: all var(--t-base);
}

@media (max-width: 1024px) {
  .domains-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .domains-grid {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .domain-card,
  .domain-icon {
    transition: none !important;
  }
  .domain-card:hover {
    transform: none;
  }
  .domain-card:hover .domain-icon {
    transform: none;
  }
}
</style>