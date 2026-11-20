<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'
import { useTypewriter } from '../composables/useTypewriter'

const sectionRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()

interface Prompt {
  id: string
  title: string
  context: string
  before: string
  after: string
  delta: string
  animated?: boolean
}

const prompts: Prompt[] = [
  {
    id: 'spec',
    title: 'Spec generator',
    context: 'Idea → PRD',
    before: 'Build a CRM',
    after: 'Build a multi-tenant CRM with RLS, RabbitMQ events, Supabase auth, role-based access (sales / manager / admin), Vietnamese address parsing, Zalo OA integration. Max 65-char email. ASCII username only.',
    delta: '+847% context, 4.2× more accurate',
    animated: true
  },
  {
    id: 'plan',
    title: 'Plan generator',
    context: 'Spec → tasks',
    before: 'Build the auth system',
    after: 'Step 1: Generate Supabase project + RLS policies for users, orgs, memberships. Step 2: Implement OAuth with PKCE, store refresh tokens encrypted. Step 3: Write integration tests covering 401/403/idempotency. Each step verifiable.',
    delta: '+18 min saved / task'
  },
  {
    id: 'review',
    title: 'Code review',
    context: 'Code → feedback',
    before: 'Review this code',
    after: 'Five-axis review: (1) correctness (race conditions, off-by-one), (2) design (single responsibility, dependency inversion), (3) security (OWASP, secrets), (4) performance (N+1, cache), (5) a11y (WCAG 2.1 AA). Score 1-5 per axis. Block above 4/10.',
    delta: '7 issues caught / 200 LOC'
  }
]

const isVisible = ref(false)

const { displayed, isTyping } = useTypewriter({
  text: prompts[0].after,
  speed: 14,
  startDelay: 600
})

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      isVisible.value = true
    }, { threshold: 0.05 })
  }
})
</script>

<template>
  <section class="prompts-section" id="prompts" ref="sectionRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Prompt Library</div>
        <h2 class="section-title">Before and after. With measurement.</h2>
        <p class="section-desc">
          The framework ships 42 production-tested prompts. Each one is paired with metrics
          on real workloads, not guesses.
        </p>
      </div>

      <div class="prompts-stack">
        <article
          v-for="(prompt, i) in prompts"
          :key="prompt.id"
          class="prompt-card"
          :style="{ '--delay': `${i * 80}ms` }"
        >
          <header class="prompt-head">
            <div class="prompt-meta">
              <span class="prompt-id">.{{ prompt.id }}</span>
              <span class="prompt-context">{{ prompt.context }}</span>
            </div>
            <h3 class="prompt-title">{{ prompt.title }}</h3>
          </header>

          <div class="prompt-content">
            <div class="prompt-col prompt-col-before">
              <div class="prompt-col-label">
                <span class="prompt-col-dot prompt-col-dot-before"></span>
                Naive prompt
              </div>
              <p class="prompt-col-text">{{ prompt.before }}</p>
            </div>

            <div class="prompt-arrow">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
            </div>

            <div class="prompt-col prompt-col-after">
              <div class="prompt-col-label">
                <span class="prompt-col-dot prompt-col-dot-after"></span>
                Framework prompt
              </div>
              <p class="prompt-col-text">
                <template v-if="prompt.animated">
                  <span class="typed">{{ displayed }}</span>
                  <span class="typed-caret" :class="{ active: isTyping }" aria-hidden="true"></span>
                </template>
                <template v-else>{{ prompt.after }}</template>
              </p>
            </div>
          </div>

          <footer class="prompt-footer">
            <span class="prompt-delta">{{ prompt.delta }}</span>
          </footer>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.prompts-section {
  padding: var(--section-py) 0;
}

.prompts-stack {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.prompt-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  padding: 28px 32px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  opacity: 0;
  animation: fade-in-up 500ms var(--ease-out-quart) both;
  animation-delay: var(--delay);
  transition: border-color var(--t-base);
}

.prompt-card:hover {
  border-color: var(--border-default);
}

.prompt-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.prompt-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.prompt-id {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  padding: 3px 8px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
}

.prompt-context {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-tertiary);
}

.prompt-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.015em;
}

.prompt-content {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 24px;
  align-items: stretch;
}

.prompt-col {
  padding: 16px 18px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-hairline);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.prompt-col-before {
  border-color: var(--border-subtle);
}

.prompt-col-after {
  border-color: rgba(16, 185, 129, 0.25);
  background: linear-gradient(to bottom, rgba(16, 185, 129, 0.04), transparent);
}

.prompt-col-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  font-weight: 500;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.prompt-col-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.prompt-col-dot-before {
  background: var(--text-muted);
}

.prompt-col-dot-after {
  background: var(--accent);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}

.prompt-col-text {
  font-size: 13px;
  line-height: 1.65;
  color: var(--text-secondary);
}

.prompt-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
}

.prompt-arrow svg {
  width: 18px;
  height: 18px;
}

.prompt-footer {
  padding-top: 16px;
  border-top: 1px solid var(--border-hairline);
  display: flex;
  justify-content: flex-end;
}

.prompt-delta {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
  color: var(--accent);
  padding: 4px 10px;
  background: var(--accent-dim);
  border: 1px solid var(--accent-line);
  border-radius: var(--radius-sm);
}

/* Typewriter cursor */
.typed-caret {
  display: inline-block;
  width: 7px;
  height: 13px;
  background: var(--accent);
  margin-left: 2px;
  vertical-align: text-bottom;
  opacity: 1;
  transform: translateY(1px);
  border-radius: 1px;
}

.typed-caret.active {
  animation: caret-blink 1s steps(2, end) infinite;
}

.typed-caret:not(.active) {
  animation: caret-fade 800ms var(--ease-out-quart) forwards;
}

@keyframes caret-blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

@keyframes caret-fade {
  from { opacity: 1; }
  to { opacity: 0; transform: translateY(1px) scaleY(0); }
}

@media (max-width: 768px) {
  .prompt-content {
    grid-template-columns: 1fr;
  }
  .prompt-arrow {
    transform: rotate(90deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .typed-caret {
    animation: none !important;
    opacity: 0;
  }
}
</style>