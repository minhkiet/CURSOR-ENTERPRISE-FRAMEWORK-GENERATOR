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

@media (max-width: 768px) {
  .getting-grid {
    grid-template-columns: 1fr;
  }
}
</style>