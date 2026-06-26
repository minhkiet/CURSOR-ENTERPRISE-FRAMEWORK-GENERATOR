<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const sectionRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()

const isVisible = ref(false)

interface InstallOption {
  title: string
  description: string
  command: string
  badge: string
}

const installOptions: InstallOption[] = [
  {
    title: 'Cài đặt lần đầu',
    description: 'Chạy script cài đặt hoàn chỉnh framework vào project của bạn.',
    command: 'irm https://raw.githubusercontent.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/main/install.ps1 -OutFile $env:TEMP\\install-cef.ps1; & $env:TEMP\\install-cef.ps1',
    badge: 'Fresh Install'
  },
  {
    title: 'Cập nhật về sau',
    description: 'Cập nhật framework lên phiên bản mới nhất từ GitHub.',
    command: 'irm https://raw.githubusercontent.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/main/install.ps1 -OutFile $env:TEMP\\install-cef.ps1; & $env:TEMP\\install-cef.ps1 -Update',
    badge: 'Update'
  }
]

interface InitCommand {
  title: string
  description: string
  command: string
  icon: string
}

const initCommands: InitCommand[] = [
  {
    title: 'Build Memory Database',
    description: 'Khởi tạo SQLite databases cho context và code embeddings.',
    command: '. .cursor/scripts/memory-builder/build-memory.ps1',
    icon: 'database'
  },
  {
    title: 'Compile Knowledge',
    description: 'Compile và merge knowledge files thành context tối ưu.',
    command: '. .cursor/scripts/knowledge-compiler/compile-knowledge.ps1',
    icon: 'book'
  },
  {
    title: 'Build Project Index',
    description: 'Index toàn bộ code để search nhanh và context-aware.',
    command: '. .cursor/scripts/project-index-builder/build-index.ps1',
    icon: 'search'
  },
  {
    title: 'Build Embeddings',
    description: 'Tạo vector embeddings cho RAG và semantic search.',
    command: '. .cursor/scripts/embedding-builder/build-embeddings.ps1',
    icon: 'cube'
  }
]

const copiedIndex = ref<number | null>(null)
const copiedInitIndex = ref<number | null>(null)

function copyCommand(index: number, command: string) {
  navigator.clipboard.writeText(command).then(() => {
    copiedIndex.value = index
    setTimeout(() => {
      copiedIndex.value = null
    }, 2000)
  }).catch(() => {
    const textarea = document.createElement('textarea')
    textarea.value = command
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

function copyInitCommand(index: number, command: string) {
  navigator.clipboard.writeText(command).then(() => {
    copiedInitIndex.value = index
    setTimeout(() => {
      copiedInitIndex.value = null
    }, 2000)
  }).catch(() => {
    const textarea = document.createElement('textarea')
    textarea.value = command
    textarea.style.cssText = 'position:fixed;opacity:0;'
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    document.body.removeChild(textarea)
    copiedInitIndex.value = index
    setTimeout(() => {
      copiedInitIndex.value = null
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
        <h2 class="section-title">Cài đặt Framework</h2>
        <p class="section-desc">
          Copy framework vào project của bạn với một lệnh PowerShell duy nhất.
          Chạy với quyền Administrator nếu được yêu cầu.
        </p>
      </div>

      <div class="install-grid" :class="{ visible: isVisible }">
        <div v-for="(option, index) in installOptions" :key="index" class="install-card">
          <div class="install-card-header">
            <span class="install-badge" :class="option.badge === 'Fresh Install' ? 'badge-primary' : 'badge-update'">
              {{ option.badge }}
            </span>
            <button
              class="copy-btn"
              @click="copyCommand(index, option.command)"
              :title="copiedIndex === index ? 'Đã copy!' : 'Copy command'"
            >
              <svg v-if="copiedIndex !== index" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
            </button>
          </div>
          <h3>{{ option.title }}</h3>
          <p>{{ option.description }}</p>
          <div class="install-code">
            <code>{{ option.command }}</code>
          </div>
        </div>
      </div>

      <div class="install-note">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="16" x2="12" y2="12"/>
          <line x1="12" y1="8" x2="12.01" y2="8"/>
        </svg>
        <span>Script download từ GitHub official repository. Đảm bảo chạy PowerShell với quyền phù hợp.</span>
      </div>

      <!-- Initialization Commands -->
      <div class="init-section">
        <h3 class="init-title">Khởi tạo sau cài đặt</h3>
        <p class="init-desc">Chạy các lệnh sau để khởi tạo context và database cho framework hoạt động tối ưu.</p>
        <div class="init-grid">
          <div v-for="(cmd, index) in initCommands" :key="index" class="init-card">
            <div class="init-icon">
              <svg v-if="cmd.icon === 'database'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <ellipse cx="12" cy="5" rx="9" ry="3"/>
                <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
              </svg>
              <svg v-else-if="cmd.icon === 'book'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
              <svg v-else-if="cmd.icon === 'cube'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/>
                <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
                <line x1="12" y1="22.08" x2="12" y2="12"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
              </svg>
            </div>
            <div class="init-content">
              <h4>{{ cmd.title }}</h4>
              <p>{{ cmd.description }}</p>
            </div>
            <button
              class="copy-btn-sm"
              @click="copyInitCommand(index, cmd.command)"
              :title="copiedInitIndex === index ? 'Đã copy!' : 'Copy command'"
            >
              <svg v-if="copiedInitIndex !== index" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
            </button>
            <code class="init-code">{{ cmd.command }}</code>
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

.install-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 20px;
  margin-top: 48px;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s var(--ease-out), transform 0.6s var(--ease-out);
}

.install-grid.visible {
  opacity: 1;
  transform: translateY(0);
}

.install-card {
  padding: 28px;
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-soft);
  background: var(--bg-surface);
  transition: all var(--t-base);
  position: relative;
  overflow: hidden;
}

.install-card::before {
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

.install-card:hover {
  border-color: var(--border-accent);
  box-shadow: var(--shadow-glow);
}

.install-card:hover::before {
  opacity: 1;
}

.install-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.install-badge {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: var(--radius-full);
}

.badge-primary {
  color: var(--color-success);
  background: rgba(52, 211, 153, 0.1);
  border: 1px solid rgba(52, 211, 153, 0.2);
}

.badge-update {
  color: #60a5fa;
  background: rgba(96, 165, 250, 0.1);
  border: 1px solid rgba(96, 165, 250, 0.2);
}

.copy-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  background: transparent;
  border: 1px solid var(--border-subtle);
  color: var(--text-muted);
  cursor: pointer;
  transition: all var(--t-fast);
}

.copy-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--border-soft);
  color: var(--text-primary);
}

.copy-btn svg {
  width: 15px;
  height: 15px;
}

.install-card h3 {
  font-size: 17px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.install-card > p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.65;
  margin-bottom: 18px;
}

.install-code {
  background: rgba(4, 4, 14, 0.6);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 12px 14px;
  overflow: hidden;
}

.install-code code {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-secondary);
  line-height: 1.6;
  word-break: break-all;
  display: block;
}

.install-note {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-top: 28px;
  padding: 14px 18px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
}

.install-note svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  color: var(--text-muted);
  margin-top: 1px;
}

.install-note span {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.5;
}

@media (max-width: 768px) {
  .install-grid {
    grid-template-columns: 1fr;
  }

  .install-code code {
    font-size: 10px;
  }
}

/* Initialization Section */
.init-section {
  margin-top: 64px;
}

.init-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.init-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.init-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.init-card {
  display: grid;
  grid-template-columns: 40px 1fr auto;
  grid-template-rows: auto auto;
  gap: 6px 14px;
  padding: 18px 20px;
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-lg);
  transition: all var(--t-fast);
}

.init-card:hover {
  border-color: var(--border-accent);
  background: rgba(255, 255, 255, 0.02);
}

.init-icon {
  grid-row: span 2;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--radius-md);
}

.init-icon svg {
  width: 18px;
  height: 18px;
  color: var(--color-primary);
}

.init-content h4 {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.init-content p {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.copy-btn-sm {
  grid-row: span 2;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  color: var(--text-muted);
  cursor: pointer;
  transition: all var(--t-fast);
  align-self: center;
}

.copy-btn-sm:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--border-soft);
  color: var(--text-primary);
}

.copy-btn-sm svg {
  width: 14px;
  height: 14px;
}

.init-code {
  grid-column: 2 / 4;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
  background: rgba(4, 4, 14, 0.4);
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  word-break: break-all;
}

@media (max-width: 640px) {
  .init-card {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
  }

  .init-icon {
    display: none;
  }

  .copy-btn-sm {
    grid-row: auto;
    grid-column: auto;
  }

  .init-code {
    grid-column: 1;
  }
}
</style>
