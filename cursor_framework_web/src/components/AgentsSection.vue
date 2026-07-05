<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const sectionRef = ref<HTMLElement | null>(null)
const isVisible = ref(false)

interface Agent {
  id: string
  name: string
  role: string
  slash: string
  description: string
  icon: string
  scope: string
}

const agents: Agent[] = [
  {
    id: 'code-reviewer',
    name: 'code-reviewer',
    role: 'Senior staff engineer',
    slash: '/review',
    description: 'Reviews code on five axes: correctness, design, readability, security, and performance.',
    icon: 'check',
    scope: 'All changes'
  },
  {
    id: 'security-auditor',
    name: 'security-auditor',
    role: 'Security engineer',
    slash: '/security',
    description: 'OWASP Top 10 audit, STRIDE threat modeling, secrets scan, payment flow review.',
    icon: 'shield',
    scope: 'Auth, payments'
  },
  {
    id: 'test-engineer',
    name: 'test-engineer',
    role: 'QA specialist',
    slash: '/test',
    description: 'Test pyramid, coverage analysis, mocking strategy, regression tests for new features.',
    icon: 'beaker',
    scope: 'Test gaps'
  },
  {
    id: 'web-performance',
    name: 'web-performance',
    role: 'Web perf engineer',
    slash: '/perf',
    description: 'Core Web Vitals, bundle analysis, render profiling, Lighthouse audits, INP tuning.',
    icon: 'gauge',
    scope: 'Frontend'
  },
  {
    id: 'api-designer',
    name: 'api-designer',
    role: 'API designer',
    slash: '/api',
    description: 'REST maturity, GraphQL schema, RFC 7807 errors, versioning, OpenAPI specs.',
    icon: 'route',
    scope: 'New endpoints'
  },
  {
    id: 'backend-reviewer',
    name: 'backend-reviewer',
    role: 'Backend specialist',
    slash: '/backend',
    description: 'NestJS, Laravel, ASP.NET Core. Transactions, concurrency, IDOR, error handling.',
    icon: 'server',
    scope: 'API, workers'
  },
  {
    id: 'database-reviewer',
    name: 'database-reviewer',
    role: 'DB specialist',
    slash: '/db',
    description: 'Schema design, query optimization, indexing, migrations, RLS, integrity checks.',
    icon: 'database',
    scope: 'Migrations'
  },
  {
    id: 'frontend-architect',
    name: 'frontend-architect',
    role: 'Frontend architect',
    slash: '/frontend',
    description: 'Next.js, Nuxt, Vue 3. Component design, state management, SSR/SSG, a11y.',
    icon: 'layout',
    scope: 'Components'
  }
]

const { observe } = useIntersectionObserver()

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      isVisible.value = true
    }, { threshold: 0.05 })
  }
})
</script>

<template>
  <section class="agents-section" id="agents" ref="sectionRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Subagents</div>
        <h2 class="section-title">8 personas. One slash command away.</h2>
        <p class="section-desc">
          Each persona is a specialist. Triggered by slash command, dispatched by intent,
          read-only by default. They augment your main agent, not replace it.
        </p>
      </div>

      <div class="agents-grid" :class="{ visible: isVisible }">
        <article
          v-for="(agent, index) in agents"
          :key="agent.id"
          class="agent-card"
          :style="{ '--delay': `${index * 40}ms` }"
        >
          <div class="agent-card-head">
            <div class="agent-icon">
              <svg v-if="agent.icon === 'check'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><polyline points="20 6 9 17 4 12"/></svg>
              <svg v-else-if="agent.icon === 'shield'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              <svg v-else-if="agent.icon === 'beaker'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><path d="M9 2h6M10 2v6.5L4 18a2 2 0 002 3h12a2 2 0 002-3l-6-9.5V2"/></svg>
              <svg v-else-if="agent.icon === 'gauge'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><path d="M12 14v-4M3.34 19a10 10 0 1117.32 0"/></svg>
              <svg v-else-if="agent.icon === 'route'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 000-7h-11a3.5 3.5 0 010-7H15"/><circle cx="18" cy="5" r="3"/></svg>
              <svg v-else-if="agent.icon === 'server'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><circle cx="6" cy="6" r=".5" fill="currentColor"/><circle cx="6" cy="18" r=".5" fill="currentColor"/></svg>
              <svg v-else-if="agent.icon === 'database'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>
            </div>
            <code class="agent-slash">{{ agent.slash }}</code>
          </div>

          <h4 class="agent-name">{{ agent.name }}</h4>
          <div class="agent-role">{{ agent.role }}</div>

          <p class="agent-desc">{{ agent.description }}</p>

          <div class="agent-scope">
            <span class="agent-scope-label">Scope</span>
            <span class="agent-scope-value">{{ agent.scope }}</span>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.agents-section {
  padding: var(--section-py) 0;
}

.agents-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 500ms var(--ease-out-quart), transform 500ms var(--ease-out-quart);
}

.agents-grid.visible {
  opacity: 1;
  transform: translateY(0);
}

.agent-card {
  position: relative;
  padding: 22px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: border-color var(--t-base), transform var(--t-base), background var(--t-base);
  opacity: 0;
  animation: fade-in-up 500ms var(--ease-out-quart) both;
  animation-delay: var(--delay);
}

.agents-grid.visible .agent-card {
  opacity: 1;
}

.agent-card:hover {
  border-color: var(--border-strong);
  background: var(--bg-elevated);
  transform: translateY(-2px);
}

.agent-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.agent-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  transition: all var(--t-base);
}

.agent-card:hover .agent-icon {
  background: var(--accent-dim);
  border-color: var(--accent-line);
  color: var(--accent);
  transform: rotate(-8deg) scale(1.08);
}

.agent-icon svg {
  width: 18px;
  height: 18px;
  transition: transform var(--t-base);
}

.agent-card:hover .agent-icon svg {
  transform: rotate(8deg);
}

.agent-icon svg {
  width: 18px;
  height: 18px;
}

.agent-slash {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
  padding: 3px 8px;
  border-radius: var(--radius-sm);
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
}

.agent-card:hover .agent-slash {
  background: var(--bg-surface);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.agent-name {
  font-family: var(--font-mono);
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  letter-spacing: -0.01em;
  margin-top: 4px;
}

.agent-role {
  font-size: 11px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-top: -8px;
  font-weight: 500;
}

.agent-desc {
  font-size: 12.5px;
  color: var(--text-secondary);
  line-height: 1.55;
  flex: 1;
}

.agent-scope {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid var(--border-hairline);
  font-size: 11px;
}

.agent-scope-label {
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 500;
}

.agent-scope-value {
  color: var(--text-secondary);
}

@media (max-width: 1024px) {
  .agents-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .agents-grid {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .agent-card,
  .agent-icon,
  .agent-icon svg {
    transition: none !important;
  }
  .agent-card:hover .agent-icon {
    transform: none;
  }
  .agent-card:hover .agent-icon svg {
    transform: none;
  }
}
</style>