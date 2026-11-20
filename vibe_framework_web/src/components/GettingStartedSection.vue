<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const sectionRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()

const isVisible = ref(false)

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      isVisible.value = true
    }, { threshold: 0.05 })
  }
})

interface Step {
  number: string
  title: string
  description: string
  command: string
  detail: string
}

const steps: Step[] = [
  {
    number: '01',
    title: 'Clone the framework',
    description: 'Get the monorepo with all rules, skills, and agents preconfigured.',
    command: 'git clone https://github.com/your-org/cursor-enterprise-framework.git',
    detail: 'Takes 12 seconds. Includes 39 rules, 17 skills, 8 agents.'
  },
  {
    number: '02',
    title: 'Open in Cursor',
    description: 'Cursor auto-loads the .cursor/ directory and indexes the rules.',
    command: 'cursor ./cursor-enterprise-framework',
    detail: 'No CLI to learn. Indexes 272 files on first open.'
  },
  {
    number: '03',
    title: 'Run the spec agent',
    description: 'Slash command dispatches the spec agent to scope your next project.',
    command: '/spec "Build a multi-tenant CRM with RLS and RabbitMQ"',
    detail: 'Returns a structured PRD in under 90 seconds.'
  },
  {
    number: '04',
    title: 'Build with confidence',
    description: 'The plan agent decomposes into verifiable tasks. Each task has a check.',
    command: '/plan .artifacts/spec.md',
    detail: '37 tasks in the example. Average task: 4-12 minutes.'
  }
]
</script>

<template>
  <section class="getting-section" id="getting-started" ref="sectionRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Getting Started</div>
        <h2 class="section-title">From clone to first task in 4 steps.</h2>
        <p class="section-desc">
          No proprietary CLI. No vendor lock-in. The framework lives in your repo as plain files.
          Cursor reads them natively.
        </p>
      </div>

      <div class="getting-grid">
        <article
          v-for="(step, i) in steps"
          :key="step.number"
          class="getting-step"
          :style="{ '--delay': `${i * 80}ms` }"
        >
          <div class="step-number">{{ step.number }}</div>
          <div class="step-content">
            <h3 class="step-title">{{ step.title }}</h3>
            <p class="step-desc">{{ step.description }}</p>

            <code class="step-command">{{ step.command }}</code>

            <p class="step-detail">{{ step.detail }}</p>
          </div>
        </article>
      </div>

      <div class="getting-dev-cta">
        <div class="getting-dev-cta-text">
          <div class="getting-dev-cta-label">Python devs</div>
          <h3 class="getting-dev-cta-title">Cài <code>cursor_framework</code> để dùng CLI & dashboard</h3>
          <p class="getting-dev-cta-desc">
            Ngoài <code>.cursor/</code> rules, framework còn có Python package với 11 subcommands
            (serve, ask, stats, graph, tdam). Cài qua pip, chạy Dashboard local ở port 8765.
          </p>
        </div>
        <router-link to="/install" class="btn btn-primary getting-dev-cta-btn">
          Install Python package
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M13 6l6 6-6 6"/>
          </svg>
        </router-link>
      </div>
    </div>
  </section>
</template>

<style scoped>
.getting-section {
  padding: var(--section-py) 0;
}

.getting-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.getting-step {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 24px;
  padding: 28px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  opacity: 0;
  animation: fade-in-up 500ms var(--ease-out-quart) both;
  animation-delay: var(--delay);
  transition: border-color var(--t-base);
}

.getting-step:hover {
  border-color: var(--border-default);
}

.step-number {
  font-family: var(--font-mono);
  font-size: 32px;
  font-weight: 600;
  color: var(--text-faint);
  letter-spacing: -0.02em;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.step-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.step-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.015em;
}

.step-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.step-command {
  display: block;
  font-family: var(--font-mono);
  font-size: 12.5px;
  color: var(--accent);
  padding: 10px 14px;
  background: var(--bg-canvas);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  overflow-x: auto;
  white-space: nowrap;
}

.step-detail {
  font-size: 11.5px;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
}

/* ─── DEV CTA (Python package) ──────────────────────────────────────── */
.getting-dev-cta {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 32px;
  align-items: center;
  margin-top: 20px;
  padding: 28px 32px;
  background: linear-gradient(
    135deg,
    rgba(96, 165, 250, 0.06) 0%,
    rgba(52, 211, 153, 0.04) 100%
  );
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
}

.getting-dev-cta::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse 280px 180px at 0% 100%,
    rgba(96, 165, 250, 0.08) 0%,
    transparent 60%
  );
  pointer-events: none;
}

.getting-dev-cta-text {
  position: relative;
  min-width: 0;
}

.getting-dev-cta-label {
  display: inline-flex;
  align-items: center;
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-info);
  padding: 3px 8px;
  background: rgba(96, 165, 250, 0.08);
  border: 1px solid rgba(96, 165, 250, 0.3);
  border-radius: var(--radius-sm);
  margin-bottom: 12px;
}

.getting-dev-cta-title {
  font-size: 19px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.015em;
  margin-bottom: 8px;
  line-height: 1.3;
}

.getting-dev-cta-title code {
  font-family: var(--font-mono);
  font-size: 0.85em;
  padding: 2px 8px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  color: var(--accent);
}

.getting-dev-cta-desc {
  font-size: 13.5px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
  max-width: 540px;
}

.getting-dev-cta-desc code {
  font-family: var(--font-mono);
  font-size: 0.9em;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  padding: 1px 6px;
  border-radius: var(--radius-sm);
  color: var(--accent);
}

.getting-dev-cta-btn {
  position: relative;
  padding: 12px 22px;
  font-size: 13.5px;
  white-space: nowrap;
  flex-shrink: 0;
}

.getting-dev-cta-btn svg {
  width: 14px;
  height: 14px;
  transition: transform var(--t-fast);
}

.getting-dev-cta-btn:hover svg {
  transform: translateX(3px);
}

@media (max-width: 768px) {
  .getting-grid {
    grid-template-columns: 1fr;
  }

  .getting-dev-cta {
    grid-template-columns: 1fr;
    gap: 18px;
    padding: 22px;
  }

  .getting-dev-cta-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>