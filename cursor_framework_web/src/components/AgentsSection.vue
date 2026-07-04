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
  initials: string
  accent: 'cyan' | 'emerald' | 'violet' | 'amber' | 'rose'
  description: string
  triggers: string[]
}

const agents: Agent[] = [
  {
    id: 'code-reviewer',
    name: 'code-reviewer',
    role: 'Senior Staff Engineer',
    slash: '/review',
    initials: 'CR',
    accent: 'cyan',
    description: 'Five-axis review (correctness, design, readability, security, performance) với surgical change principle.',
    triggers: ['Sau khi implement feature/refactor', 'Trước khi merge PR', 'Khi user yêu cầu /review']
  },
  {
    id: 'security-auditor',
    name: 'security-auditor',
    role: 'Security Engineer',
    slash: '/security',
    initials: 'SA',
    accent: 'rose',
    description: 'OWASP Top 10 audit, threat modeling (STRIDE), secrets scan, payment security (MoMo/SePay/PayOS).',
    triggers: ['Auth/authz implementation', 'Payment flows', 'Pre-production deploy gate']
  },
  {
    id: 'test-engineer',
    name: 'test-engineer',
    role: 'QA Specialist',
    slash: '/test',
    initials: 'TE',
    accent: 'emerald',
    description: 'Prove-It pattern, test pyramid (80/15/5), coverage analysis, mocking strategy, regression tests.',
    triggers: ['Test strategy mới', 'Coverage gaps review', 'Debug flaky tests']
  },
  {
    id: 'web-performance-auditor',
    name: 'web-performance-auditor',
    role: 'Web Performance Engineer',
    slash: '/perf',
    initials: 'WP',
    accent: 'amber',
    description: 'Core Web Vitals (LCP/INP/CLS), bundle analysis, render profiling, Lighthouse audits.',
    triggers: ['Lighthouse regression', 'Bundle size delta', 'CWV below threshold']
  },
  {
    id: 'api-designer',
    name: 'api-designer',
    role: 'API Designer',
    slash: '/api',
    initials: 'AD',
    accent: 'violet',
    description: 'REST maturity, GraphQL schema, error models (RFC 7807), versioning strategy, OpenAPI specs.',
    triggers: ['New API endpoint', 'Versioning decision', 'OpenAPI spec review']
  },
  {
    id: 'backend-reviewer',
    name: 'backend-reviewer',
    role: 'Backend Specialist',
    slash: '/backend',
    initials: 'BR',
    accent: 'cyan',
    description: 'NestJS / Laravel / ASP.NET Core — business logic, transactions, concurrency, IDOR, error handling.',
    triggers: ['New endpoint', 'Transaction boundary', 'Concurrency hazard']
  },
  {
    id: 'database-reviewer',
    name: 'database-reviewer',
    role: 'Database Specialist',
    slash: '/db',
    initials: 'DR',
    accent: 'emerald',
    description: 'Schema design, query optimization, indexing, migrations, RLS policies, data integrity.',
    triggers: ['Schema change', 'Migration plan', 'Slow query investigation']
  },
  {
    id: 'frontend-architect',
    name: 'frontend-architect',
    role: 'Frontend Architect',
    slash: '/frontend',
    initials: 'FA',
    accent: 'amber',
    description: 'Next.js / Nuxt / Vue 3 — component design, state management, SSR/SSG, accessibility.',
    triggers: ['Component API design', 'State architecture', 'SSR/SSG decision']
  }
]

const { observe } = useIntersectionObserver()

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      isVisible.value = true
    }, { threshold: 0.1 })
  }
})
</script>

<template>
  <section class="agents-section" id="agents" ref="sectionRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Subagents</div>
        <h2 class="section-title">8 Agent Personas chuyên biệt</h2>
        <p class="section-desc">
          Mỗi persona là một specialist reviewer với expertise riêng — dispatch qua slash commands
          hoặc tự động khi phát hiện intent phù hợp. Read-only audit mode, không modify code.
        </p>
      </div>

      <div class="agents-grid" :class="{ visible: isVisible }">
        <article
          v-for="(agent, index) in agents"
          :key="agent.id"
          class="agent-card"
          :class="[`agent-${agent.accent}`, { visible: isVisible }]"
          :style="{ transitionDelay: `${index * 50}ms` }"
        >
          <div class="agent-header">
            <div class="agent-avatar" :class="`agent-avatar-${agent.accent}`">
              {{ agent.initials }}
            </div>
            <div class="agent-title">
              <h4>{{ agent.name }}</h4>
              <span class="agent-role">{{ agent.role }}</span>
            </div>
            <code class="agent-slash">{{ agent.slash }}</code>
          </div>

          <p class="agent-desc">{{ agent.description }}</p>

          <div class="agent-triggers">
            <span class="agent-triggers-label">When to invoke</span>
            <ul>
              <li v-for="trigger in agent.triggers" :key="trigger">{{ trigger }}</li>
            </ul>
          </div>
        </article>
      </div>

      <div class="agents-footer">
        <div class="agents-footer-stat">
          <span class="agents-footer-num">8</span>
          <span class="agents-footer-label">Specialist personas</span>
        </div>
        <div class="agents-footer-stat">
          <span class="agents-footer-num">5</span>
          <span class="agents-footer-label">Review axes per agent</span>
        </div>
        <div class="agents-footer-stat">
          <span class="agents-footer-num">~250</span>
          <span class="agents-footer-label">Lines per agent spec</span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.agents-section {
  padding: var(--section-py) 0;
  background: linear-gradient(180deg, transparent 0%, rgba(120, 119, 232, 0.015) 50%, transparent 100%);
}

.agents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 14px;
  margin-top: 48px;
}

.agent-card {
  position: relative;
  padding: 22px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-soft);
  background: var(--bg-surface);
  transition: border-color var(--t-base), box-shadow var(--t-base), transform var(--t-base);
  opacity: 0;
  transform: translateY(12px);
}

.agent-card.visible {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.5s var(--ease-out), transform 0.5s var(--ease-out), border-color var(--t-base), box-shadow var(--t-base);
}

.agent-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
}

.agent-card.agent-cyan:hover { border-color: rgba(6, 182, 212, 0.35); }
.agent-card.agent-emerald:hover { border-color: rgba(52, 211, 153, 0.35); }
.agent-card.agent-violet:hover { border-color: rgba(167, 139, 250, 0.4); }
.agent-card.agent-amber:hover { border-color: rgba(251, 191, 36, 0.4); }
.agent-card.agent-rose:hover { border-color: rgba(248, 113, 113, 0.4); }

.agent-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.agent-avatar {
  width: 38px;
  height: 38px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 800;
  font-family: var(--font-mono);
  flex-shrink: 0;
}

.agent-avatar-cyan { background: rgba(6, 182, 212, 0.1); color: #06b6d4; border: 1px solid rgba(6, 182, 212, 0.2); }
.agent-avatar-emerald { background: rgba(52, 211, 153, 0.1); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.2); }
.agent-avatar-violet { background: rgba(167, 139, 250, 0.12); color: #a78bfa; border: 1px solid rgba(167, 139, 250, 0.25); }
.agent-avatar-amber { background: rgba(251, 191, 36, 0.1); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.2); }
.agent-avatar-rose { background: rgba(248, 113, 113, 0.1); color: #f87171; border: 1px solid rgba(248, 113, 113, 0.2); }

.agent-title {
  flex: 1;
  min-width: 0;
}

.agent-title h4 {
  font-size: 13.5px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 2px;
  font-family: var(--font-mono);
  letter-spacing: -0.01em;
}

.agent-role {
  font-size: 10.5px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
}

.agent-slash {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  background: var(--accent-glow);
  border: 1px solid var(--border-accent);
  color: var(--accent-primary);
  flex-shrink: 0;
}

.agent-desc {
  font-size: 12.5px;
  color: var(--text-secondary);
  line-height: 1.65;
  margin-bottom: 14px;
}

.agent-triggers {
  border-top: 1px solid var(--border-subtle);
  padding-top: 12px;
}

.agent-triggers-label {
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-faint);
  display: block;
  margin-bottom: 8px;
}

.agent-triggers ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.agent-triggers li {
  font-size: 11.5px;
  color: var(--text-secondary);
  padding-left: 14px;
  position: relative;
  line-height: 1.55;
}

.agent-triggers li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--accent-primary);
  opacity: 0.6;
}

.agents-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 48px;
  margin-top: 56px;
  padding: 24px 32px;
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-soft);
  background: var(--bg-surface);
  flex-wrap: wrap;
}

.agents-footer-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  text-align: center;
}

.agents-footer-num {
  font-size: 26px;
  font-weight: 900;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-family: var(--font-mono);
  letter-spacing: -0.03em;
}

.agents-footer-label {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
}

@media (max-width: 768px) {
  .agents-grid {
    grid-template-columns: 1fr;
  }
  .agents-footer {
    gap: 24px;
  }
}
</style>