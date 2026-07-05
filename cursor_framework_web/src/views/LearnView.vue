<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'
import {
  CATALOG,
  RULES,
  SKILLS,
  AGENTS,
  categoriesForType,
  type FrameworkItem,
  type FrameworkItemType
} from '../data/framework'

const sectionRef = ref<HTMLElement | null>(null)
const detailRef = ref<HTMLElement | null>(null)
const isVisible = ref(false)

type TabKey = 'rule' | 'skill' | 'agent'
const tabOrder: TabKey[] = ['rule', 'skill', 'agent']

const activeTab = ref<TabKey>('rule')
const selectedCategory = ref<string>('all')
const searchQuery = ref<string>('')
const openId = ref<string | null>(null)

function setTab(t: TabKey) {
  activeTab.value = t
  selectedCategory.value = 'all'
  searchQuery.value = ''
  openId.value = null
}

function pickItem(item: FrameworkItem) {
  // Toggle: click same card closes, click another opens.
  openId.value = openId.value === item.id ? null : item.id
}

function closeItem() {
  openId.value = null
}

// ESC closes the modal; body scroll is locked while the modal is open.
function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape' && openId.value) closeItem()
}

watch(openId, async (val) => {
  if (val) {
    document.body.style.overflow = 'hidden'
    await nextTick()
    detailRef.value?.focus()
  } else {
    document.body.style.overflow = ''
  }
})

onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = ''
})

function categoryBadgeColor(type: FrameworkItemType): string {
  if (type === 'rule') return '#60a5fa'
  if (type === 'skill') return '#a78bfa'
  return '#fbbf24'
}

const counts = computed(() => ({
  rule: RULES.length,
  skill: SKILLS.length,
  agent: AGENTS.length
}))

const visibleCategories = computed(() => categoriesForType(activeTab.value))

const filteredItems = computed<FrameworkItem[]>(() => {
  const base = CATALOG.filter((i) => i.type === activeTab.value)
  const q = searchQuery.value.toLowerCase().trim()
  return base.filter((i) => {
    const matchCat = selectedCategory.value === 'all' || i.category === selectedCategory.value
    if (!matchCat) return false
    if (!q) return true
    return (
      i.title.toLowerCase().includes(q) ||
      i.subtitle.toLowerCase().includes(q) ||
      i.description.toLowerCase().includes(q) ||
      i.tags.some((t) => t.toLowerCase().includes(q)) ||
      i.category.toLowerCase().includes(q)
    )
  })
})

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
  <div class="learn-view" ref="sectionRef">
    <!-- HERO -->
    <section class="learn-hero">
      <div class="container">
        <div class="section-label">Framework Library</div>
        <h1 class="learn-title">
          {{ counts.rule }} rules. {{ counts.skill }} skills. {{ counts.agent }} agents.<br />
          <span class="learn-title-accent">One framework, fully understood.</span>
        </h1>
        <p class="learn-subtitle">
          Every rule, skill, and agent that powers the Cursor Enterprise Framework.
          Click any card to read the full profile — description, key ideas, trigger, metrics — and see how
          it connects to the rest of the system.
        </p>

        <div class="learn-meta">
          <div class="meta-block">
            <div class="meta-value">{{ counts.rule + counts.skill + counts.agent }}</div>
            <div class="meta-label">Total items</div>
          </div>
          <div class="meta-block">
            <div class="meta-value">11</div>
            <div class="meta-label">Categories</div>
          </div>
          <div class="meta-block">
            <div class="meta-value">42+</div>
            <div class="meta-label">Gates (pre + post)</div>
          </div>
          <div class="meta-block">
            <div class="meta-value">100%</div>
            <div class="meta-label">Curated</div>
          </div>
        </div>
      </div>
    </section>

    <!-- TABS + FILTER -->
    <section class="learn-controls">
      <div class="container">
        <div class="learn-tab-bar" role="tablist" aria-label="Framework sections">
          <button
            v-for="t in tabOrder"
            :key="t"
            class="learn-tab"
            :class="{ active: activeTab === t }"
            role="tab"
            :aria-selected="activeTab === t"
            @click="setTab(t)"
          >
            <span class="learn-tab-dot" :style="{ background: categoryBadgeColor(t) }"></span>
            <span class="learn-tab-label">
              {{ t === 'rule' ? 'Rules' : t === 'skill' ? 'Skills' : 'Agents' }}
            </span>
            <span class="learn-tab-count">
              {{ t === 'rule' ? counts.rule : t === 'skill' ? counts.skill : counts.agent }}
            </span>
          </button>
        </div>

        <div class="learn-filter-row">
          <div class="learn-search">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="11" cy="11" r="8" />
              <path d="M21 21l-4.35-4.35" />
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              :placeholder="`Search ${activeTab === 'rule' ? 'rules' : activeTab === 'skill' ? 'skills' : 'agents'}…`"
              aria-label="Search framework items"
            />
          </div>
          <div class="learn-categories">
            <button
              class="learn-cat-btn"
              :class="{ active: selectedCategory === 'all' }"
              @click="selectedCategory = 'all'"
            >
              All
            </button>
            <button
              v-for="cat in visibleCategories"
              :key="cat"
              class="learn-cat-btn"
              :class="{ active: selectedCategory === cat }"
              @click="selectedCategory = cat"
            >
              {{ cat }}
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- GRID -->
    <section class="learn-grid-section">
      <div class="container">
        <div class="learn-grid" :class="{ visible: isVisible }">
          <!-- CARDS -->
          <article
            v-for="item in filteredItems"
            :key="item.id"
            class="learn-card"
            :class="{ open: openId === item.id }"
            @click="pickItem(item)"
          >
            <header class="learn-card-head">
              <div class="learn-card-meta">
                <span
                  class="learn-card-type"
                  :style="{ color: categoryBadgeColor(item.type) }"
                >
                  {{ item.type === 'rule' ? 'RULE' : item.type === 'skill' ? 'SKILL' : 'AGENT' }}
                </span>
                <span class="learn-card-cat">{{ item.category }}</span>
              </div>
              <span v-if="item.role" class="learn-card-role">{{ item.role }}</span>
            </header>

            <h3 class="learn-card-title">{{ item.title }}</h3>
            <p class="learn-card-subtitle">{{ item.subtitle }}</p>

            <p class="learn-card-desc">{{ item.description }}</p>

            <footer class="learn-card-foot">
              <div class="learn-card-tags">
                <span v-for="t in item.tags.slice(0, 4)" :key="t" class="learn-tag">{{ t }}</span>
                <span v-if="item.tags.length > 4" class="learn-tag learn-tag-more">+{{ item.tags.length - 4 }}</span>
              </div>
              <button class="learn-card-cta">
                <span v-if="openId === item.id">Close</span>
                <span v-else>Read profile</span>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M5 12h14M13 6l6 6-6 6" />
                </svg>
              </button>
            </footer>
          </article>
        </div>

        <div v-if="filteredItems.length === 0" class="learn-empty">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="11" cy="11" r="8" />
            <path d="M21 21l-4.35-4.35" />
          </svg>
          <h3>No items match this filter</h3>
          <p>Try a different search term or category.</p>
        </div>
      </div>
    </section>

    <!-- CALLOUT -->
    <section class="learn-callout">
      <div class="container">
        <div class="callout-box">
          <div>
            <div class="section-label">Next step</div>
            <h2 class="callout-title">See them in action.</h2>
            <p class="callout-desc">
              The Prompts page runs each rule, skill, and agent against a real workflow —
              plan, pre-review, run, post-review, deliver.
            </p>
          </div>
          <router-link to="/prompts" class="btn btn-primary">
            Open the prompt runner
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M5 12h14M13 6l6 6-6 6" />
            </svg>
          </router-link>
        </div>
      </div>
    </section>

    <!-- MODAL -->
    <Transition name="learn-modal">
      <div
        v-if="openId"
        ref="detailRef"
        class="learn-modal-backdrop"
        @click.self="closeItem"
        @keydown.esc="closeItem"
        tabindex="-1"
      >
        <div
          v-for="item in filteredItems"
          v-show="item.id === openId"
          :key="item.id"
          class="learn-modal-card learn-detail-card"
          role="dialog"
          aria-modal="true"
          :aria-label="item.title"
        >
          <header class="learn-detail-head">
            <div class="learn-detail-title-wrap">
              <span
                class="learn-detail-badge"
                :style="{ color: categoryBadgeColor(item.type), borderColor: categoryBadgeColor(item.type) }"
              >
                {{ item.type === 'rule' ? 'RULE' : item.type === 'skill' ? 'SKILL' : 'AGENT' }}
              </span>
              <h2 class="learn-detail-title">{{ item.title }}</h2>
              <p class="learn-detail-subtitle">{{ item.subtitle }}</p>
            </div>
            <button class="learn-detail-close" @click="closeItem" aria-label="Close detail panel">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M18 6L6 18M6 6l12 12" />
              </svg>
            </button>
          </header>

          <div class="learn-detail-grid">
            <div class="learn-detail-col">
              <h3>What it does</h3>
              <p>{{ item.description }}</p>

              <div v-if="item.bullets" class="learn-detail-bullets">
                <h3>Key ideas</h3>
                <ul>
                  <li v-for="b in item.bullets" :key="b">{{ b }}</li>
                </ul>
              </div>
            </div>

            <div class="learn-detail-side">
              <div class="learn-detail-row">
                <span class="row-label">File path</span>
                <code class="row-code">{{ item.path }}</code>
              </div>
              <div v-if="item.role" class="learn-detail-row">
                <span class="row-label">Role</span>
                <span class="row-chip row-chip-accent">{{ item.role }}</span>
              </div>
              <div v-if="item.trigger" class="learn-detail-row">
                <span class="row-label">Trigger</span>
                <code class="row-code row-code-light">{{ item.trigger }}</code>
              </div>
              <div v-if="item.gates && item.gates.length" class="learn-detail-row">
                <span class="row-label">Gates</span>
                <span class="row-chips">
                  <span v-for="g in item.gates" :key="g" class="row-chip">{{ g }}</span>
                </span>
              </div>
              <div v-if="item.alignsWith && item.alignsWith.length" class="learn-detail-row">
                <span class="row-label">Aligns with</span>
                <span class="row-chips">
                  <span v-for="a in item.alignsWith" :key="a" class="row-chip row-chip-soft">{{ a }}</span>
                </span>
              </div>
              <div class="learn-detail-row">
                <span class="row-label">Category</span>
                <span class="row-chip">{{ item.category }}</span>
              </div>
              <div class="learn-detail-row">
                <span class="row-label">Tags</span>
                <span class="row-chips">
                  <span v-for="t in item.tags" :key="t" class="row-chip row-chip-soft">{{ t }}</span>
                </span>
              </div>
              <div v-if="item.metrics" class="learn-detail-metrics">
                <div v-for="m in item.metrics" :key="m.label" class="metric-tile">
                  <div class="metric-tile-value">{{ m.value }}</div>
                  <div class="metric-tile-label">{{ m.label }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.learn-view {
  width: 100%;
}

/* HERO ───────────────────────────────────────────────────────────────────── */

.learn-hero {
  position: relative;
  padding: 140px 0 64px;
  border-bottom: 1px solid var(--border-subtle);
}

.learn-title {
  font-size: clamp(34px, 5vw, 56px);
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  margin: 16px 0 20px;
  max-width: 880px;
}

.learn-title-accent {
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 0.78em;
  font-weight: 500;
}

.learn-subtitle {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.65;
  max-width: 700px;
  margin: 0 0 36px;
}

.learn-meta {
  display: inline-flex;
  align-items: stretch;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--bg-surface);
}

.meta-block {
  padding: 16px 28px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  border-right: 1px solid var(--border-hairline);
  min-width: 130px;
}

.meta-block:last-child {
  border-right: 0;
}

.meta-value {
  font-family: var(--font-mono);
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.meta-label {
  font-size: 10.5px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-family: var(--font-mono);
}

/* TABS + FILTER ─────────────────────────────────────────────────────────── */

.learn-controls {
  padding: 28px 0 8px;
  position: sticky;
  top: 56px;
  z-index: 50;
  background: var(--bg-base);
  border-bottom: 1px solid var(--border-subtle);
  backdrop-filter: blur(20px);
}

.learn-tab-bar {
  display: flex;
  gap: 4px;
  padding: 4px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  margin-bottom: 16px;
  width: fit-content;
}

.learn-tab {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 14px;
  font-size: 13px;
  font-weight: 500;
  font-family: inherit;
  color: var(--text-secondary);
  background: transparent;
  border-radius: 6px;
  cursor: pointer;
  transition: color var(--t-fast), background var(--t-fast);
}

.learn-tab:hover {
  color: var(--text-primary);
}

.learn-tab.active {
  color: var(--text-primary);
  background: var(--bg-raised);
  box-shadow: var(--shadow-sm);
}

.learn-tab-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.learn-tab-label {
  font-weight: 600;
}

.learn-tab-count {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
  padding: 1px 7px;
  border-radius: var(--radius-sm);
  background: var(--bg-canvas);
  color: var(--text-tertiary);
}

.learn-tab.active .learn-tab-count {
  color: var(--text-primary);
  background: var(--bg-elevated);
}

.learn-filter-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 0 16px;
  flex-wrap: wrap;
}

.learn-search {
  flex: 1;
  min-width: 220px;
  position: relative;
  display: flex;
  align-items: center;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: 0 14px;
  transition: border-color var(--t-fast);
}

.learn-search:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-dim);
}

.learn-search svg {
  width: 16px;
  height: 16px;
  color: var(--text-muted);
  flex-shrink: 0;
}

.learn-search input {
  flex: 1;
  padding: 10px 12px;
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-size: 13px;
  font-family: inherit;
}

.learn-search input::placeholder {
  color: var(--text-muted);
}

.learn-categories {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.learn-cat-btn {
  padding: 7px 14px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--t-fast);
  font-family: inherit;
}

.learn-cat-btn:hover {
  color: var(--text-primary);
  border-color: var(--border-strong);
}

.learn-cat-btn.active {
  color: var(--bg-canvas);
  background: var(--accent);
  border-color: var(--accent);
}

/* MODAL ─────────────────────────────────────────────────────────────────── */

.learn-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 64px 24px 24px;
  background: rgba(8, 10, 14, 0.72);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  overflow-y: auto;
}

.learn-modal-card {
  position: relative;
  width: 100%;
  max-width: 960px;
  max-height: calc(100vh - 88px);
  overflow-y: auto;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.4),
    0 0 0 1px var(--border-default);
}

/* Modal transitions */
.learn-modal-enter-active,
.learn-modal-leave-active {
  transition: opacity 220ms var(--ease-out-quart);
}
.learn-modal-enter-active .learn-modal-card,
.learn-modal-leave-active .learn-modal-card {
  transition: transform 220ms var(--ease-out-quart),
    opacity 220ms var(--ease-out-quart);
}
.learn-modal-enter-from,
.learn-modal-leave-to {
  opacity: 0;
}
.learn-modal-enter-from .learn-modal-card,
.learn-modal-leave-to .learn-modal-card {
  opacity: 0;
  transform: translateY(-12px) scale(0.98);
}

@media (prefers-reduced-motion: reduce) {
  .learn-modal-enter-active,
  .learn-modal-leave-active,
  .learn-modal-enter-active .learn-modal-card,
  .learn-modal-leave-active .learn-modal-card {
    transition-duration: 0ms;
  }
}

/* DETAIL CARD (used inside modal) ────────────────────────────────────── */

.learn-detail-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 32px;
  position: relative;
  overflow: hidden;
}

.learn-detail-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--gradient-hero);
  pointer-events: none;
  opacity: 0.7;
}

.learn-detail-badge {
  display: inline-flex;
  align-items: center;
  align-self: flex-start;
  padding: 4px 10px;
  border: 1px solid currentColor;
  border-radius: var(--radius-sm);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  background: rgba(255, 255, 255, 0.02);
}

@keyframes detail-rise {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.learn-detail-head {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 28px;
  position: relative;
}

.learn-detail-title-wrap {
  flex: 1;
  min-width: 0;
}

.learn-detail-badge {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.12em;
  padding: 3px 8px;
  background: transparent;
  border: 1px solid;
  border-radius: var(--radius-sm);
  margin-bottom: 12px;
}

.learn-detail-title {
  font-size: clamp(22px, 3vw, 30px);
  font-weight: 600;
  line-height: 1.2;
  letter-spacing: -0.025em;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.learn-detail-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  line-height: 1.5;
  font-family: var(--font-mono);
}

.learn-detail-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  color: var(--text-tertiary);
  flex-shrink: 0;
  transition: all var(--t-fast);
  cursor: pointer;
}

.learn-detail-close:hover {
  color: var(--text-primary);
  border-color: var(--border-strong);
}

.learn-detail-close svg {
  width: 14px;
  height: 14px;
}

.learn-detail-grid {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 36px;
  align-items: start;
  position: relative;
}

.learn-detail-col h3 {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 10px;
  font-family: var(--font-mono);
}

.learn-detail-col p {
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-secondary);
  margin: 0;
}

.learn-detail-bullets {
  margin-top: 24px;
}

.learn-detail-bullets ul {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.learn-detail-bullets li {
  position: relative;
  padding-left: 18px;
  font-size: 13.5px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.learn-detail-bullets li::before {
  content: '→';
  position: absolute;
  left: 0;
  color: var(--accent);
  font-family: var(--font-mono);
}

.learn-detail-side {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 22px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
}

.learn-detail-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border-hairline);
}

.learn-detail-row:last-of-type {
  padding-bottom: 0;
  border-bottom: 0;
}

.row-label {
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
}

.row-code {
  font-family: var(--font-mono);
  font-size: 12.5px;
  color: var(--text-primary);
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  padding: 5px 8px;
  border-radius: var(--radius-sm);
  word-break: break-all;
}

.row-code-light {
  background: var(--bg-canvas);
  color: var(--accent);
}

.row-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.row-chip {
  font-family: var(--font-mono);
  font-size: 11px;
  padding: 3px 8px;
  border-radius: var(--radius-sm);
  background: var(--bg-surface);
  color: var(--text-secondary);
  border: 1px solid var(--border-subtle);
}

.row-chip-accent {
  color: var(--accent);
  background: var(--accent-dim);
  border-color: var(--accent-line);
}

.row-chip-soft {
  background: var(--bg-elevated);
}

.learn-detail-metrics {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-top: 4px;
  padding-top: 16px;
  border-top: 1px solid var(--border-hairline);
}

.metric-tile {
  padding: 12px 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.metric-tile-value {
  font-family: var(--font-mono);
  font-size: 16px;
  font-weight: 600;
  color: var(--accent);
  line-height: 1;
}

.metric-tile-label {
  font-size: 10.5px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-family: var(--font-mono);
}

/* GRID ──────────────────────────────────────────────────────────────────── */

.learn-grid-section {
  padding: 40px 0 100px;
}

.learn-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 18px;
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 500ms var(--ease-out-quart), transform 500ms var(--ease-out-quart);
}

.learn-grid.visible {
  opacity: 1;
  transform: translateY(0);
}

.learn-card {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 24px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  cursor: pointer;
  transition: border-color var(--t-base), transform var(--t-base), background var(--t-base);
  min-width: 0;
}

.learn-card:hover {
  border-color: var(--border-default);
  transform: translateY(-2px);
  background: var(--bg-raised);
}

.learn-card.open {
  border-color: var(--accent-line);
  background: var(--bg-raised);
}

.learn-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.learn-card-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.learn-card-type {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
}

.learn-card-cat {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
  padding: 2px 8px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  background: var(--bg-elevated);
}

.learn-card-role {
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: var(--text-tertiary);
  text-transform: lowercase;
  letter-spacing: 0.04em;
}

.learn-card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.018em;
  line-height: 1.25;
}

.learn-card-subtitle {
  font-size: 12.5px;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  line-height: 1.5;
}

.learn-card-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.learn-card-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 4px;
  padding-top: 16px;
  border-top: 1px solid var(--border-hairline);
}

.learn-card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  flex: 1;
  min-width: 0;
}

.learn-tag {
  font-family: var(--font-mono);
  font-size: 10.5px;
  padding: 3px 7px;
  border-radius: var(--radius-sm);
  background: var(--bg-elevated);
  color: var(--text-secondary);
  border: 1px solid var(--border-subtle);
}

.learn-tag-more {
  color: var(--text-muted);
}

.learn-card-cta {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  background: transparent;
  padding: 6px 8px;
  border-radius: var(--radius-sm);
  transition: color var(--t-fast);
  flex-shrink: 0;
  font-family: inherit;
}

.learn-card-cta:hover {
  color: var(--accent);
}

.learn-card-cta svg {
  width: 13px;
  height: 13px;
}

.learn-card.open .learn-card-cta {
  color: var(--accent);
}

.learn-empty {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-muted);
}

.learn-empty svg {
  width: 40px;
  height: 40px;
  margin-bottom: 12px;
  opacity: 0.4;
}

.learn-empty h3 {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

/* CALLOUT ──────────────────────────────────────────────────────────────── */

.learn-callout {
  padding: 20px 0 100px;
}

.callout-box {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 32px;
  align-items: center;
  padding: 36px 40px;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
}

.callout-title {
  font-size: 22px;
  font-weight: 600;
  line-height: 1.25;
  letter-spacing: -0.02em;
  margin: 12px 0 8px;
}

.callout-desc {
  font-size: 13.5px;
  color: var(--text-secondary);
  line-height: 1.65;
  max-width: 560px;
  margin: 0;
}

@media (max-width: 880px) {
  .learn-detail-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .callout-box {
    grid-template-columns: 1fr;
    padding: 28px;
  }

  .learn-meta {
    flex-wrap: wrap;
  }

  .meta-block {
    flex: 1;
    min-width: 50%;
    text-align: center;
    border-right: 0;
    border-bottom: 1px solid var(--border-hairline);
  }

  .meta-block:last-child {
    border-bottom: 0;
  }

  .learn-controls {
    position: static;
  }
}

@media (max-width: 480px) {
  .learn-tab-label {
    display: none;
  }

  .learn-detail-card {
    padding: 22px;
  }
}
</style>
