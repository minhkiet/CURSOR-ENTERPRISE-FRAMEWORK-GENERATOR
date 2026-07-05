<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'
import { PROMPTS, type PromptItem, type PromptExecutionStep } from '../data/prompts'
import { CATALOG, type FrameworkItem } from '../data/framework'

const sectionRef = ref<HTMLElement | null>(null)
const isVisible = ref(false)
const promptBody = ref<string>('')
const selectedPromptId = ref<string>(PROMPTS[0].id)
const isRunning = ref(false)
const hasRun = ref(false)
const runnerStepIndex = ref<number>(-1)
const runnerTrace = ref<PromptExecutionStep[]>([])
const runnerStartMs = ref<number>(0)
const runnerEndMs = ref<number>(0)
const progressPct = ref<number>(0)
const logRef = ref<HTMLElement | null>(null)

const selectedCategory = ref<string>('all')
const searchQuery = ref<string>('')
const runnerExpanded = ref<Record<number, boolean>>({})

const categories = ['Spec', 'Review', 'Build', 'Debug', 'Ship']

const filteredPrompts = computed<PromptItem[]>(() => {
  return PROMPTS.filter((p) => {
    if (selectedCategory.value !== 'all' && p.category !== selectedCategory.value) return false
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase().trim()
      return (
        p.title.toLowerCase().includes(q) ||
        p.oneLiner.toLowerCase().includes(q) ||
        p.prompt.toLowerCase().includes(q)
      )
    }
    return true
  })
})

const selectedPrompt = computed<PromptItem | undefined>(() =>
  PROMPTS.find((p) => p.id === selectedPromptId.value)
)

function resolveItem(type: FrameworkItem['type'], id: string): FrameworkItem | undefined {
  return CATALOG.find((i) => i.type === type && i.id === id)
}

function typeColor(type: 'rule' | 'skill' | 'agent'): string {
  if (type === 'rule') return '#60a5fa'
  if (type === 'skill') return '#a78bfa'
  return '#fbbf24'
}

function selectPrompt(p: PromptItem) {
  if (isRunning.value) return
  selectedPromptId.value = p.id
  promptBody.value = p.prompt
  hasRun.value = false
  runnerTrace.value = []
  runnerStepIndex.value = -1
  progressPct.value = 0
}

function useAsBase() {
  if (selectedPrompt.value) {
    promptBody.value = selectedPrompt.value.prompt
  }
}

async function runPrompt() {
  if (isRunning.value) return
  if (!promptBody.value.trim()) return
  if (!selectedPrompt.value) return

  isRunning.value = true
  hasRun.value = true
  runnerTrace.value = []
  runnerStepIndex.value = -1
  progressPct.value = 0
  runnerStartMs.value = performance.now()

  const steps = selectedPrompt.value.trace
  // Simulate a realistic execution: plan → pre-review → run → post-review → deliver
  for (let i = 0; i < steps.length; i++) {
    runnerStepIndex.value = i
    runnerTrace.value = [...runnerTrace.value, steps[i]]
    progressPct.value = Math.round(((i + 1) / steps.length) * 100)
    await nextTick()
    scrollToBottom()
    await wait(560 + i * 80)
  }

  runnerEndMs.value = performance.now()
  isRunning.value = false
}

function wait(ms: number): Promise<void> {
  return new Promise((r) => setTimeout(r, ms))
}

function scrollToBottom() {
  if (logRef.value) {
    logRef.value.scrollTop = logRef.value.scrollHeight
  }
}

function resetRunner() {
  isRunning.value = false
  hasRun.value = false
  runnerTrace.value = []
  runnerStepIndex.value = -1
  progressPct.value = 0
}

function toggleStep(i: number) {
  runnerExpanded.value[i] = !runnerExpanded.value[i]
  if (runnerExpanded.value[i] === undefined) {
    runnerExpanded.value[i] = true
  }
}

function phaseIcon(phase: PromptExecutionStep['phase']): string {
  switch (phase) {
    case 'plan':
      return '◐'
    case 'pre-review':
      return '✓'
    case 'run':
      return '▶'
    case 'post-review':
      return '◆'
    case 'deliver':
      return '★'
  }
}

function phaseLabel(phase: PromptExecutionStep['phase']): string {
  switch (phase) {
    case 'plan':
      return 'PLAN'
    case 'pre-review':
      return 'PRE-REVIEW'
    case 'run':
      return 'RUN'
    case 'post-review':
      return 'POST-REVIEW'
    case 'deliver':
      return 'DELIVER'
  }
}

const executionSeconds = computed(() => {
  if (!runnerStartMs.value || !runnerEndMs.value) return 0
  return ((runnerEndMs.value - runnerStartMs.value) / 1000).toFixed(1)
})

// Total applies wired into the selected prompt
const appliesStats = computed(() => {
  const sel = selectedPrompt.value
  if (!sel) return { rules: 0, skills: 0, agents: 0 }
  return sel.applies.reduce(
    (acc, r) => {
      if (r.type === 'rule') acc.rules++
      else if (r.type === 'skill') acc.skills++
      else acc.agents++
      return acc
    },
    { rules: 0, skills: 0, agents: 0 }
  )
})

const { observe } = useIntersectionObserver()

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      isVisible.value = true
    }, { threshold: 0.05 })
  }
  if (selectedPrompt.value) {
    promptBody.value = selectedPrompt.value.prompt
  }
})
</script>

<template>
  <div class="prompts-view" ref="sectionRef">
    <!-- HERO -->
    <section class="pr-hero">
      <div class="container">
        <div class="section-label">Prompt Runner</div>
        <h1 class="pr-title">
          Type a prompt. Wire the framework.<br />
          <span class="pr-title-accent">Watch the pipeline execute.</span>
        </h1>
        <p class="pr-subtitle">
          Pick a template, attach the rules, skills, and agents that should run, and execute the prompt
          end-to-end. Each phase — plan, pre-review, run, post-review, deliver — is shown with the
          actual framework item that drove it.
        </p>

        <div class="pr-stats">
          <div class="pr-stat">
            <div class="pr-stat-value">{{ PROMPTS.length }}</div>
            <div class="pr-stat-label">Templates</div>
          </div>
          <div class="pr-stat">
            <div class="pr-stat-value">5</div>
            <div class="pr-stat-label">Phases per run</div>
          </div>
          <div class="pr-stat">
            <div class="pr-stat-value">10</div>
            <div class="pr-stat-label">Max applies / prompt</div>
          </div>
          <div class="pr-stat">
            <div class="pr-stat-value">100%</div>
            <div class="pr-stat-label">Traced</div>
          </div>
        </div>
      </div>
    </section>

    <!-- BUILDER + RUNNER -->
    <section class="pr-main">
      <div class="container">
        <div class="pr-grid">
          <!-- LEFT: TEMPLATES + PROMPT BODY -->
          <div class="pr-col pr-col-left">
            <div class="pr-panel">
              <header class="pr-panel-head">
                <div>
                  <h2 class="pr-panel-title">1 · Pick a template</h2>
                  <p class="pr-panel-desc">A library of pre-wired prompts. Edit before run.</p>
                </div>
                <span class="pr-panel-badge">{{ filteredPrompts.length }} templates</span>
              </header>

              <div class="pr-filter-row">
                <div class="pr-search">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <circle cx="11" cy="11" r="8" />
                    <path d="M21 21l-4.35-4.35" />
                  </svg>
                  <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="Search prompts…"
                    aria-label="Search prompts"
                  />
                </div>
                <div class="pr-categories">
                  <button
                    class="pr-cat-btn"
                    :class="{ active: selectedCategory === 'all' }"
                    @click="selectedCategory = 'all'"
                  >
                    All
                  </button>
                  <button
                    v-for="cat in categories"
                    :key="cat"
                    class="pr-cat-btn"
                    :class="{ active: selectedCategory === cat }"
                    @click="selectedCategory = cat"
                  >
                    {{ cat }}
                  </button>
                </div>
              </div>

              <div class="pr-template-list" :class="{ visible: isVisible }">
                <button
                  v-for="p in filteredPrompts"
                  :key="p.id"
                  class="pr-template"
                  :class="{ active: selectedPromptId === p.id }"
                  @click="selectPrompt(p)"
                  :disabled="isRunning"
                >
                  <span class="pr-template-cat">{{ p.category }}</span>
                  <span class="pr-template-title">{{ p.title }}</span>
                  <span class="pr-template-oneliner">{{ p.oneLiner }}</span>
                  <span class="pr-template-meta">
                    {{ p.applies.length }} applies · {{ p.trace.length }} phases
                  </span>
                </button>
              </div>
            </div>

            <div class="pr-panel" v-if="selectedPrompt">
              <header class="pr-panel-head">
                <div>
                  <h2 class="pr-panel-title">2 · Prompt body</h2>
                  <p class="pr-panel-desc">Edit freely. The applies below will run alongside it.</p>
                </div>
                <button class="pr-mini-btn" @click="useAsBase" :disabled="isRunning">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M3 12a9 9 0 1 0 3-6.7L3 8" />
                    <path d="M3 3v5h5" />
                  </svg>
                  Reset to template
                </button>
              </header>

              <div class="pr-editor-wrap">
                <div class="pr-editor-bar">
                  <span class="pr-dot pr-dot-red"></span>
                  <span class="pr-dot pr-dot-yellow"></span>
                  <span class="pr-dot pr-dot-green"></span>
                  <span class="pr-editor-name">prompt.md</span>
                  <span class="pr-editor-meta">UTF-8 · {{ promptBody.length }} chars</span>
                </div>
                <textarea
                  v-model="promptBody"
                  class="pr-editor"
                  spellcheck="false"
                  rows="9"
                  placeholder="Describe what you want the framework to do…"
                  aria-label="Prompt body"
                  :disabled="isRunning"
                ></textarea>
              </div>

              <div class="pr-actions">
                <button class="btn btn-primary pr-run-btn" @click="runPrompt" :disabled="isRunning || !promptBody.trim()">
                  <svg v-if="!isRunning" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8 5v14l11-7L8 5z" />
                  </svg>
                  <span v-if="!isRunning">Run prompt</span>
                  <span v-else>Running…</span>
                </button>
                <button
                  class="btn btn-secondary"
                  @click="resetRunner"
                  :disabled="isRunning"
                >
                  Reset run
                </button>
                <div class="pr-actions-hint">
                  Wires <strong>{{ appliesStats.rules }} rules</strong>,
                  <strong>{{ appliesStats.skills }} skills</strong>,
                  <strong>{{ appliesStats.agents }} agents</strong>
                </div>
              </div>
            </div>
          </div>

          <!-- RIGHT: APPLIES + RUNNER -->
          <div class="pr-col pr-col-right">
            <!-- APPLIES -->
            <div class="pr-panel" v-if="selectedPrompt">
              <header class="pr-panel-head">
                <div>
                  <h2 class="pr-panel-title">3 · Framework applies</h2>
                  <p class="pr-panel-desc">
                    These rule(s), skill(s), and agent(s) are in the chain. Click to inspect.
                  </p>
                </div>
                <span class="pr-panel-badge pr-panel-badge-accent">
                  {{ selectedPrompt.applies.length }} applies
                </span>
              </header>

              <div class="pr-applies">
                <div
                  v-for="(ref, i) in selectedPrompt.applies"
                  :key="ref.id + i"
                  class="pr-apply"
                >
                  <span
                    class="pr-apply-type"
                    :style="{ color: typeColor(ref.type), borderColor: typeColor(ref.type) }"
                  >
                    {{ ref.type === 'rule' ? 'RULE' : ref.type === 'skill' ? 'SKILL' : 'AGENT' }}
                  </span>
                  <div class="pr-apply-body">
                    <div class="pr-apply-name">
                      <span class="mono">{{ resolveItem(ref.type, ref.id)?.name ?? ref.id }}</span>
                    </div>
                    <div class="pr-apply-reason">{{ ref.reason }}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- RUNNER / TRACE -->
            <div class="pr-panel pr-runner">
              <header class="pr-panel-head">
                <div>
                  <h2 class="pr-panel-title">4 · Run trace</h2>
                  <p class="pr-panel-desc">Live execution: plan → pre-review → run → post-review → deliver.</p>
                </div>
                <span v-if="isRunning" class="pr-panel-badge pr-panel-badge-run">
                  <span class="pr-runner-spinner"></span>
                  Executing
                </span>
                <span v-else-if="hasRun" class="pr-panel-badge pr-panel-badge-ok">
                  <span class="pr-checkmark">✓</span>
                  Completed in {{ executionSeconds }}s
                </span>
                <span v-else class="pr-panel-badge">Idle</span>
              </header>

              <!-- Progress bar -->
              <div v-if="hasRun" class="pr-progress">
                <div class="pr-progress-track">
                  <div class="pr-progress-fill" :style="{ width: `${progressPct}%` }"></div>
                </div>
                <div class="pr-progress-meta">
                  <span>Phase {{ Math.min(runnerStepIndex + 1, runnerTrace.length) }} / {{ runnerTrace.length }}</span>
                  <span>{{ progressPct }}%</span>
                </div>
              </div>

              <!-- Empty state -->
              <div v-if="!hasRun && !isRunning" class="pr-empty">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="12" cy="12" r="9" />
                  <path d="M9 9l6 3-6 3z" fill="currentColor" stroke="none" />
                </svg>
                <h3>Ready when you are</h3>
                <p>Hit "Run prompt" to execute the chain. Each phase shows who ran it and why.</p>
              </div>

              <!-- Trace log -->
              <div v-else ref="logRef" class="pr-trace-log">
                <div
                  v-for="(step, i) in runnerTrace"
                  :key="i"
                  class="pr-trace-step"
                  :class="['phase-' + step.phase, { active: runnerStepIndex === i }]"
                >
                  <header class="pr-trace-step-head" @click="toggleStep(i)">
                    <span class="pr-trace-icon">{{ phaseIcon(step.phase) }}</span>
                    <span class="pr-trace-phase">{{ phaseLabel(step.phase) }}</span>
                    <span class="pr-trace-label">{{ step.label }}</span>
                    <span class="pr-trace-by">by {{ step.by }}</span>
                    <button class="pr-trace-toggle" :aria-expanded="runnerExpanded[i] ?? true">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M6 9l6 6 6-6" />
                      </svg>
                    </button>
                  </header>
                  <div v-if="runnerExpanded[i] !== false" class="pr-trace-bullets">
                    <span v-for="(b, bi) in step.bullets" :key="bi" class="pr-trace-bullet">
                      <span class="pr-bullet-marker">→</span>
                      <span>{{ b }}</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FOOTNOTE / NUDGE BACK TO LEARN -->
    <section class="pr-footnote">
      <div class="container">
        <div class="footnote-box">
          <div>
            <div class="section-label">Reference</div>
            <h2 class="footnote-title">Want the full profiles?</h2>
            <p class="footnote-desc">
              Every rule, skill, and agent in the chain is also described in the
              framework library — with file paths, gates, and metrics.
            </p>
          </div>
          <router-link to="/learn" class="btn btn-primary">
            Open framework library
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M5 12h14M13 6l6 6-6 6" />
            </svg>
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.prompts-view {
  width: 100%;
}

/* HERO ───────────────────────────────────────────────────────────────────── */

.pr-hero {
  position: relative;
  padding: 140px 0 64px;
  border-bottom: 1px solid var(--border-subtle);
}

.pr-title {
  font-size: clamp(34px, 5vw, 56px);
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  margin: 16px 0 20px;
  max-width: 900px;
}

.pr-title-accent {
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 0.78em;
  font-weight: 500;
}

.pr-subtitle {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.65;
  max-width: 740px;
  margin: 0 0 36px;
}

.pr-stats {
  display: inline-flex;
  align-items: stretch;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--bg-surface);
}

.pr-stat {
  padding: 16px 28px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  border-right: 1px solid var(--border-hairline);
  min-width: 130px;
}

.pr-stat:last-child {
  border-right: 0;
}

.pr-stat-value {
  font-family: var(--font-mono);
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.pr-stat-label {
  font-size: 10.5px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-family: var(--font-mono);
}

/* MAIN ───────────────────────────────────────────────────────────────────── */

.pr-main {
  padding: 64px 0 100px;
}

.pr-grid {
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: 28px;
  align-items: start;
}

.pr-col {
  display: flex;
  flex-direction: column;
  gap: 24px;
  min-width: 0;
}

.pr-panel {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 24px;
}

.pr-panel-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding-bottom: 18px;
  margin-bottom: 18px;
  border-bottom: 1px solid var(--border-hairline);
}

.pr-panel-title {
  font-size: 14.5px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.012em;
  margin-bottom: 4px;
}

.pr-panel-desc {
  font-size: 12.5px;
  color: var(--text-tertiary);
  line-height: 1.55;
  margin: 0;
  max-width: 460px;
}

.pr-panel-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  background: var(--bg-elevated);
  color: var(--text-tertiary);
  border: 1px solid var(--border-subtle);
  white-space: nowrap;
  flex-shrink: 0;
}

.pr-panel-badge-accent {
  color: var(--accent);
  background: var(--accent-dim);
  border-color: var(--accent-line);
}

.pr-panel-badge-ok {
  color: var(--color-success);
  background: rgba(52, 211, 153, 0.08);
  border-color: rgba(52, 211, 153, 0.3);
}

.pr-panel-badge-run {
  color: var(--accent);
  background: var(--accent-dim);
  border-color: var(--accent-line);
}

.pr-runner-spinner {
  width: 10px;
  height: 10px;
  border: 1.5px solid var(--accent-line);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

.pr-checkmark {
  display: inline-flex;
  width: 14px;
  height: 14px;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--color-success);
  color: var(--bg-canvas);
  font-size: 9px;
  font-weight: 700;
  line-height: 1;
}

.pr-mini-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  padding: 7px 10px;
  border-radius: var(--radius-sm);
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  font-family: inherit;
  transition: all var(--t-fast);
  cursor: pointer;
  flex-shrink: 0;
}

.pr-mini-btn:hover:not(:disabled) {
  color: var(--text-primary);
  border-color: var(--border-strong);
}

.pr-mini-btn svg {
  width: 13px;
  height: 13px;
}

/* FILTERS ───────────────────────────────────────────────────────────────── */

.pr-filter-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.pr-search {
  flex: 1;
  min-width: 200px;
  position: relative;
  display: flex;
  align-items: center;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: 0 12px;
  transition: border-color var(--t-fast);
}

.pr-search:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-dim);
}

.pr-search svg {
  width: 14px;
  height: 14px;
  color: var(--text-muted);
  flex-shrink: 0;
}

.pr-search input {
  flex: 1;
  padding: 8px 10px;
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-size: 12.5px;
  font-family: inherit;
}

.pr-search input::placeholder {
  color: var(--text-muted);
}

.pr-categories {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.pr-cat-btn {
  padding: 6px 12px;
  font-size: 11.5px;
  font-weight: 500;
  color: var(--text-secondary);
  background: transparent;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--t-fast);
  font-family: inherit;
}

.pr-cat-btn:hover {
  color: var(--text-primary);
  border-color: var(--border-strong);
}

.pr-cat-btn.active {
  color: var(--bg-canvas);
  background: var(--accent);
  border-color: var(--accent);
}

/* TEMPLATE LIST ─────────────────────────────────────────────────────────── */

.pr-template-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 380px;
  overflow-y: auto;
  opacity: 0;
  transform: translateY(6px);
  transition: opacity 500ms var(--ease-out-quart), transform 500ms var(--ease-out-quart);
  padding-right: 4px;
}

.pr-template-list.visible {
  opacity: 1;
  transform: translateY(0);
}

.pr-template-list::-webkit-scrollbar {
  width: 6px;
}

.pr-template {
  display: grid;
  grid-template-columns: auto 1fr;
  grid-template-rows: auto auto auto;
  column-gap: 12px;
  row-gap: 4px;
  text-align: left;
  padding: 14px 16px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--t-fast);
  font-family: inherit;
}

.pr-template:hover:not(:disabled) {
  border-color: var(--border-strong);
  background: var(--bg-raised);
}

.pr-template.active {
  border-color: var(--accent-line);
  background: linear-gradient(
    to right,
    rgba(16, 185, 129, 0.06),
    transparent 50%
  );
}

.pr-template:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pr-template-cat {
  grid-column: 1;
  grid-row: 1;
  align-self: start;
  font-family: var(--font-mono);
  font-size: 9.5px;
  font-weight: 600;
  letter-spacing: 0.12em;
  color: var(--accent);
  padding: 2px 7px;
  background: var(--accent-dim);
  border: 1px solid var(--accent-line);
  border-radius: var(--radius-sm);
  white-space: nowrap;
  height: fit-content;
  margin-top: 2px;
}

.pr-template-title {
  grid-column: 2;
  grid-row: 1;
  font-size: 13.5px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.01em;
  line-height: 1.3;
}

.pr-template-oneliner {
  grid-column: 1 / -1;
  grid-row: 2;
  font-size: 12.5px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.pr-template-meta {
  grid-column: 1 / -1;
  grid-row: 3;
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: var(--text-muted);
}

/* EDITOR ────────────────────────────────────────────────────────────────── */

.pr-editor-wrap {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--bg-elevated);
}

.pr-editor-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 9px 14px;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
}

.pr-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--text-faint);
}

.pr-dot-red { background: #f87171; }
.pr-dot-yellow { background: #fbbf24; }
.pr-dot-green { background: #34d399; }

.pr-editor-name {
  font-family: var(--font-mono);
  font-size: 11.5px;
  color: var(--text-tertiary);
  margin-left: 8px;
}

.pr-editor-meta {
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: var(--text-muted);
  margin-left: auto;
}

.pr-editor {
  display: block;
  width: 100%;
  padding: 16px 18px;
  background: transparent;
  border: none;
  outline: none;
  resize: vertical;
  font-family: var(--font-mono);
  font-size: 12.5px;
  line-height: 1.65;
  color: var(--text-primary);
  min-height: 160px;
  max-height: 360px;
}

.pr-editor::placeholder {
  color: var(--text-muted);
}

.pr-editor:focus {
  background: var(--bg-raised);
}

.pr-editor:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ACTIONS ───────────────────────────────────────────────────────────────── */

.pr-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 16px;
  flex-wrap: wrap;
}

.pr-run-btn {
  min-width: 130px;
}

.pr-run-btn svg {
  width: 14px;
  height: 14px;
}

.pr-actions-hint {
  font-size: 12px;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  margin-left: auto;
}

.pr-actions-hint strong {
  color: var(--text-primary);
  font-weight: 600;
}

/* APPLIES ───────────────────────────────────────────────────────────────── */

.pr-applies {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.pr-apply {
  display: grid;
  grid-template-columns: 56px 1fr;
  gap: 14px;
  align-items: flex-start;
  padding: 12px 14px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  transition: border-color var(--t-fast);
}

.pr-apply:hover {
  border-color: var(--border-default);
}

.pr-apply-type {
  display: inline-block;
  text-align: center;
  font-family: var(--font-mono);
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.12em;
  padding: 4px 6px;
  background: transparent;
  border: 1px solid;
  border-radius: var(--radius-sm);
  align-self: start;
  margin-top: 2px;
}

.pr-apply-body {
  min-width: 0;
}

.pr-apply-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
  word-break: break-word;
}

.pr-apply-reason {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* RUNNER ────────────────────────────────────────────────────────────────── */

.pr-runner {
  position: sticky;
  top: 220px;
}

.pr-progress {
  margin-bottom: 16px;
}

.pr-progress-track {
  height: 3px;
  width: 100%;
  background: var(--bg-elevated);
  border-radius: var(--radius-pill);
  overflow: hidden;
  border: 1px solid var(--border-subtle);
}

.pr-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent-bright));
  border-radius: var(--radius-pill);
  transition: width 320ms var(--ease-out-quart);
}

.pr-progress-meta {
  display: flex;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 11px;
  margin-top: 6px;
  color: var(--text-tertiary);
}

.pr-empty {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
}

.pr-empty svg {
  width: 36px;
  height: 36px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.pr-empty h3 {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.pr-empty p {
  font-size: 12.5px;
  max-width: 320px;
  margin: 0 auto;
  line-height: 1.55;
}

.pr-trace-log {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 540px;
  overflow-y: auto;
  padding-right: 6px;
}

.pr-trace-log::-webkit-scrollbar {
  width: 6px;
}

.pr-trace-step {
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
  animation: trace-enter 320ms var(--ease-out-quart) both;
}

@keyframes trace-enter {
  from {
    opacity: 0;
    transform: translateX(-6px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.pr-trace-step.active {
  border-color: var(--accent-line);
  box-shadow: 0 0 0 1px var(--accent-line), 0 4px 18px rgba(16, 185, 129, 0.08);
}

.pr-trace-step.phase-plan {
  border-left: 3px solid #60a5fa;
}
.pr-trace-step.phase-pre-review {
  border-left: 3px solid #a78bfa;
}
.pr-trace-step.phase-run {
  border-left: 3px solid var(--accent);
}
.pr-trace-step.phase-post-review {
  border-left: 3px solid #fbbf24;
}
.pr-trace-step.phase-deliver {
  border-left: 3px solid var(--color-success);
}

.pr-trace-step-head {
  display: grid;
  grid-template-columns: auto auto 1fr auto auto;
  align-items: center;
  gap: 10px;
  padding: 11px 14px;
  cursor: pointer;
  transition: background var(--t-fast);
}

.pr-trace-step-head:hover {
  background: var(--bg-raised);
}

.pr-trace-icon {
  font-family: var(--font-mono);
  font-size: 14px;
  color: var(--text-secondary);
  width: 16px;
  text-align: center;
}

.pr-trace-phase {
  font-family: var(--font-mono);
  font-size: 9.5px;
  font-weight: 600;
  letter-spacing: 0.12em;
  color: var(--accent);
  padding: 2px 7px;
  background: var(--accent-dim);
  border: 1px solid var(--accent-line);
  border-radius: var(--radius-sm);
  white-space: nowrap;
}

.pr-trace-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
  letter-spacing: -0.005em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pr-trace-by {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
  white-space: nowrap;
}

.pr-trace-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: var(--radius-sm);
  color: var(--text-tertiary);
  transition: transform var(--t-fast), color var(--t-fast);
}

.pr-trace-toggle[aria-expanded='false'] svg {
  transform: rotate(-90deg);
}

.pr-trace-toggle svg {
  width: 14px;
  height: 14px;
  transition: transform var(--t-fast);
}

.pr-trace-bullets {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 4px 16px 14px 40px;
  border-top: 1px solid var(--border-hairline);
  padding-top: 12px;
  margin-top: 0;
}

.pr-trace-bullet {
  display: grid;
  grid-template-columns: 14px 1fr;
  gap: 4px;
  align-items: flex-start;
  font-size: 12.5px;
  line-height: 1.55;
  color: var(--text-secondary);
}

.pr-bullet-marker {
  font-family: var(--font-mono);
  color: var(--accent);
  font-weight: 500;
}

/* FOOTNOTE ──────────────────────────────────────────────────────────────── */

.pr-footnote {
  padding: 0 0 80px;
}

.footnote-box {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 32px;
  align-items: center;
  padding: 36px 40px;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
}

.footnote-title {
  font-size: 22px;
  font-weight: 600;
  line-height: 1.25;
  letter-spacing: -0.02em;
  margin: 12px 0 8px;
}

.footnote-desc {
  font-size: 13.5px;
  color: var(--text-secondary);
  line-height: 1.65;
  max-width: 560px;
  margin: 0;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 1100px) {
  .pr-grid {
    grid-template-columns: 1fr;
  }
  .pr-runner {
    position: static;
  }
}

@media (max-width: 768px) {
  .pr-stats {
    flex-wrap: wrap;
  }
  .pr-stat {
    flex: 1;
    min-width: 50%;
    border-right: 0;
    border-bottom: 1px solid var(--border-hairline);
    text-align: center;
  }
  .pr-stat:last-child {
    border-bottom: 0;
  }

  .footnote-box {
    grid-template-columns: 1fr;
    padding: 28px;
  }

  .pr-trace-step-head {
    grid-template-columns: auto auto 1fr auto;
    gap: 8px;
  }
  .pr-trace-by {
    display: none;
  }
}
</style>
