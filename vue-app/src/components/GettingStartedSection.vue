<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const sectionRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()

const isVisible = ref(false)

interface Step {
  num: number
  title: string
  description: string
  code: string
  copyText: string
}

const steps: Step[] = [
  {
    num: 1,
    title: 'One-Click Install',
    description: 'Copy framework vào project của bạn với một lệnh PowerShell duy nhất.',
    code: 'irm https://bit.ly/cef-install | iex',
    copyText: 'Copy command'
  },
  {
    num: 2,
    title: 'Build Memory',
    description: 'Khởi tạo SQLite databases, code index và knowledge embeddings cho context tối ưu.',
    code: '. .cursor/scripts/memory-builder/build-memory.ps1',
    copyText: 'Copy command'
  },
  {
    num: 3,
    title: 'Start Coding',
    description: 'Mở project trong Cursor, bắt đầu task. Framework tự động load context, rules và knowledge.',
    code: '1. Open project in Cursor\n2. Start new chat\n3. CEF auto-loads context',
    copyText: 'Copy steps'
  }
]

interface Script {
  name: string
  description: string
  command: string
}

const scripts: Script[] = [
  { name: 'Quick Install', description: 'PowerShell one-liner install', command: 'irm https://bit.ly/cef-install | iex' },
  { name: 'GitHub Clone', description: 'Clone from GitHub', command: 'setup.bat --github' },
  { name: 'Memory Builder', description: 'Build SQLite memory databases', command: '. .cursor/scripts/memory-builder/build-memory.ps1' },
  { name: 'Knowledge Compiler', description: 'Compile and merge knowledge files', command: '. .cursor/scripts/knowledge-compiler/compile-knowledge.ps1' },
  { name: 'Project Index', description: 'Build semantic code index', command: '. .cursor/scripts/project-index-builder/build-index.ps1' }
]

const copiedIndex = ref<number | null>(null)

function copyCode(index: number, code: string) {
  navigator.clipboard.writeText(code).then(() => {
    copiedIndex.value = index
    setTimeout(() => {
      copiedIndex.value = null
    }, 2000)
  }).catch(() => {
    const textarea = document.createElement('textarea')
    textarea.value = code
    textarea.style.cssText = 'position:fixed;opacity:0;'
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    document.body.removeChild(textarea)
    copiedIndex.value = index
    setTimeout(() => {
      copiedIndex.value = null
    }, 2000)
  })
}

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      isVisible.value = true
    }, { threshold: 0.1 })
  }
})
</script>

<template>
  <section class="getting-started-section" id="getting-started" ref="sectionRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Quick Start</div>
        <h2 class="section-title">Bắt đầu trong 3 bước</h2>
        <p class="section-desc">
          Copy framework vào project của bạn, khởi tạo memory system,
          và bắt đầu sử dụng. Toàn bộ setup tự động qua scripts.
        </p>
      </div>

      <div class="steps-grid" :class="{ visible: isVisible }">
        <div v-for="(step, index) in steps" :key="step.num" class="step-card">
          <div class="step-number">{{ step.num }}</div>
          <h3>{{ step.title }}</h3>
          <p>{{ step.description }}</p>
          <div class="step-code">
            <button
              class="cef-btn cef-btn-ghost cef-btn-sm step-copy-btn"
              @click="copyCode(index, step.code)"
            >
              <svg v-if="copiedIndex !== index" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              {{ copiedIndex === index ? 'Copied!' : step.copyText }}
            </button>
            <code>{{ step.code }}</code>
          </div>
        </div>
      </div>

      <!-- Scripts reference table -->
      <div class="scripts-ref">
        <h3>Automation Scripts</h3>
        <div class="scripts-table">
          <div class="scripts-table-header">
            <span>Script</span>
            <span>Description</span>
            <span>Command</span>
          </div>
          <div v-for="script in scripts" :key="script.name" class="scripts-table-row">
            <span><span class="tag-script">{{ script.name }}</span></span>
            <span>{{ script.description }}</span>
            <code>{{ script.command }}</code>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.getting-started-section {
  padding: var(--section-py) 0;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
  margin-top: 48px;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s var(--ease-out), transform 0.6s var(--ease-out);
}

.steps-grid.visible {
  opacity: 1;
  transform: translateY(0);
}

.step-card {
  padding: 28px;
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-soft);
  background: var(--bg-surface);
  transition: all var(--t-base);
  position: relative;
  overflow: hidden;
}

.step-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-primary);
  opacity: 0;
  transition: opacity var(--t-base);
}

.step-card:hover {
  border-color: var(--border-accent);
  box-shadow: var(--shadow-glow);
}

.step-card:hover::before {
  opacity: 1;
}

.step-number {
  font-size: 44px;
  font-weight: 900;
  letter-spacing: -0.04em;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 14px;
  font-family: var(--font-mono);
}

.step-card h3 {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.step-card > p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.65;
  margin-bottom: 18px;
}

.step-code {
  background: rgba(4, 4, 14, 0.6);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 10px 12px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.step-code code {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-secondary);
  line-height: 1.6;
  white-space: pre;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  min-width: 0;
}

.step-copy-btn {
  flex-shrink: 0;
}

/* Scripts table */
.scripts-ref {
  margin-top: 64px;
}

.scripts-ref > h3 {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 20px;
}

.scripts-table {
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-soft);
  overflow: hidden;
}

.scripts-table-header {
  display: grid;
  grid-template-columns: 160px 1fr 1.5fr;
  gap: 14px;
  padding: 12px 18px;
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid var(--border-subtle);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.scripts-table-row {
  display: grid;
  grid-template-columns: 160px 1fr 1.5fr;
  gap: 14px;
  padding: 12px 18px;
  border-bottom: 1px solid var(--border-subtle);
  align-items: center;
  transition: background var(--t-fast);
}

.scripts-table-row:last-child {
  border-bottom: none;
}

.scripts-table-row:hover {
  background: rgba(255, 255, 255, 0.015);
}

.scripts-table-row span:not(.tag) {
  font-size: 12px;
  color: var(--text-secondary);
}

.scripts-table-row code {
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: var(--text-muted);
  word-break: break-all;
}

.tag-script {
  font-size: 10px;
  font-weight: 600;
  color: var(--color-success);
  background: rgba(52, 211, 153, 0.08);
  border: 1px solid rgba(52, 211, 153, 0.15);
  padding: 2px 7px;
  border-radius: var(--radius-full);
}

@media (max-width: 768px) {
  .steps-grid {
    grid-template-columns: 1fr;
  }

  .scripts-table-header,
  .scripts-table-row {
    grid-template-columns: 1fr;
    gap: 6px;
  }

  .scripts-table-header span:not(:first-child),
  .scripts-table-row span:not(:first-child) {
    display: none;
  }

  .scripts-table-row code {
    display: none;
  }
}
</style>
