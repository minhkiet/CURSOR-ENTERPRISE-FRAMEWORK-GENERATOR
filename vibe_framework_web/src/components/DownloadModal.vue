<script setup lang="ts">
import { ref, computed } from 'vue'
import { useDownload, type DownloadFormat } from '../composables/useDownload'

interface Props {
  templateId: string
  templateName: string
  templateIndustry: string
  templateTagline: string
  templateDescription: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  close: []
}>()

const { downloadStatus, downloadProgress, errorMessage, downloadTemplate } = useDownload()

const selectedFormat = ref<DownloadFormat>('html')

const formats = [
  {
    id: 'html' as DownloadFormat,
    name: 'HTML/CSS/JS',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4l5 16 2.5-6.5L14 20 19 4H4z"/><path d="M6.5 7.5h10l-.5 3h-9l.5 1.5 1 3h-8l-.5-2h-2l.5 6"/></svg>`,
    desc: 'File HTML, CSS, JS riêng biệt',
    files: 'index.html, styles.css, script.js'
  },
  {
    id: 'nextjs' as DownloadFormat,
    name: 'React + Next.js',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>`,
    desc: 'Next.js App Router + Tailwind CSS',
    files: 'page.tsx, layout.tsx, components/, package.json'
  },
  {
    id: 'vue' as DownloadFormat,
    name: 'Vue 3 + Vite',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2L3 6v6c0 5.5 3.5 10 9 12 5.5-2 9-6.5 9-12V6l-9-4z"/></svg>`,
    desc: 'Vue 3 Composition API + Vite',
    files: 'LandingPage.vue, App.vue, main.ts, package.json'
  }
]

const isDownloading = computed(() => downloadStatus.value === 'preparing')
const isReady = computed(() => downloadStatus.value === 'ready')
const isError = computed(() => downloadStatus.value === 'error')

const statusText = computed(() => {
  if (isDownloading.value) return 'Đang chuẩn bị...'
  if (isReady.value) return 'Đã tải thành công!'
  if (isError.value) return errorMessage.value || 'Lỗi'
  return ''
})

function handleDownload() {
  downloadTemplate({
    id: props.templateId,
    slug: props.templateId,
    name: props.templateName,
    industry: props.templateIndustry,
    tagline: props.templateTagline,
    description: props.templateDescription
  }, selectedFormat.value)
}

function handleClose() {
  if (!isDownloading.value) {
    emit('close')
  }
}
</script>

<template>
  <div class="modal-overlay" @click.self="handleClose">
    <div class="modal-panel">
      <div class="modal-header">
        <div class="modal-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
          </svg>
          <span>Tải template</span>
        </div>
        <button class="modal-close" @click="handleClose" :disabled="isDownloading">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <div class="modal-body">
        <div class="template-info">
          <div class="template-badge">{{ templateIndustry }}</div>
          <h3 class="template-name">{{ templateName }}</h3>
          <p class="template-desc">{{ templateTagline }}</p>
        </div>

        <div class="format-section">
          <label class="section-label">Chọn định dạng</label>
          <div class="format-grid">
            <label 
              v-for="fmt in formats" 
              :key="fmt.id"
              class="format-card"
              :class="{ 
                selected: selectedFormat === fmt.id,
                disabled: isDownloading 
              }"
            >
              <input 
                type="radio" 
                :value="fmt.id" 
                v-model="selectedFormat"
                :disabled="isDownloading"
                class="sr-only"
              />
              <div class="format-icon" v-html="fmt.icon"></div>
              <div class="format-content">
                <div class="format-name">{{ fmt.name }}</div>
                <div class="format-desc">{{ fmt.desc }}</div>
                <div class="format-files">{{ fmt.files }}</div>
              </div>
              <div class="format-check">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
              </div>
            </label>
          </div>
        </div>

        <div v-if="isDownloading" class="progress-section">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: `${downloadProgress}%` }"></div>
          </div>
          <div class="progress-text">
            <span>Đang nén files...</span>
            <span>{{ downloadProgress }}%</span>
          </div>
        </div>

        <div v-if="isReady" class="success-section">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="16 10 10 16 8 14"/>
          </svg>
          <span>File đã được tải về!</span>
        </div>

        <div v-if="isError" class="error-section">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <span>{{ errorMessage }}</span>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-ghost" @click="handleClose" :disabled="isDownloading">
          Hủy
        </button>
        <button 
          class="btn btn-primary download-btn"
          @click="handleDownload"
          :disabled="isDownloading || isReady"
        >
          <svg v-if="!isDownloading && !isReady" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
          </svg>
          <svg v-else-if="isDownloading" class="spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M21 12a9 9 0 11-6.219-8.56"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <span v-if="isDownloading">{{ statusText }}</span>
          <span v-else-if="isReady">Đã tải xong</span>
          <span v-else>Tải về (.zip)</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  animation: fadeIn 150ms ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-panel {
  background: var(--bg-surface, #1a1a2e);
  border: 1px solid var(--border-default, #2d2d44);
  border-radius: 16px;
  width: 100%;
  max-width: 560px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: slideUp 200ms ease-out;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-subtle, #2d2d44);
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary, #f0f0f0);
}

.modal-title svg {
  width: 20px;
  height: 20px;
  color: var(--accent, #10b981);
}

.modal-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: transparent;
  border: 1px solid var(--border-default, #2d2d44);
  border-radius: 8px;
  color: var(--text-secondary, #888);
  cursor: pointer;
  transition: all 150ms ease;
}

.modal-close:hover:not(:disabled) {
  background: var(--bg-elevated, #252540);
  color: var(--text-primary, #f0f0f0);
}

.modal-close:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.modal-close svg {
  width: 16px;
  height: 16px;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
}

.template-info {
  text-align: center;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border-subtle, #2d2d44);
}

.template-badge {
  display: inline-block;
  padding: 4px 12px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--accent, #10b981);
  background: rgba(16, 185, 129, 0.1);
  border-radius: 20px;
  margin-bottom: 8px;
}

.template-name {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary, #f0f0f0);
  margin: 0 0 4px;
}

.template-desc {
  font-size: 13px;
  color: var(--text-secondary, #888);
  margin: 0;
}

.format-section {
  margin-bottom: 20px;
}

.section-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted, #666);
  margin-bottom: 12px;
}

.format-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.format-card {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 16px;
  background: var(--bg-elevated, #252540);
  border: 2px solid var(--border-default, #2d2d44);
  border-radius: 12px;
  cursor: pointer;
  transition: all 150ms ease;
}

.format-card:hover:not(.disabled) {
  border-color: var(--border-strong, #404060);
  background: rgba(37, 37, 64, 0.8);
}

.format-card.selected {
  border-color: var(--accent, #10b981);
  background: rgba(16, 185, 129, 0.08);
}

.format-card.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.format-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-surface, #1a1a2e);
  border-radius: 10px;
  color: var(--accent, #10b981);
}

.format-icon :deep(svg) {
  width: 22px;
  height: 22px;
}

.format-content {
  flex: 1;
  min-width: 0;
}

.format-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary, #f0f0f0);
  margin-bottom: 2px;
}

.format-desc {
  font-size: 12px;
  color: var(--text-secondary, #888);
  margin-bottom: 4px;
}

.format-files {
  font-size: 11px;
  font-family: var(--font-mono, monospace);
  color: var(--text-muted, #666);
}

.format-check {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--bg-surface, #1a1a2e);
  border: 2px solid var(--border-default, #2d2d44);
  color: transparent;
  transition: all 150ms ease;
}

.format-card.selected .format-check {
  background: var(--accent, #10b981);
  border-color: var(--accent, #10b981);
  color: white;
}

.format-check svg {
  width: 14px;
  height: 14px;
}

.progress-section {
  margin-top: 16px;
}

.progress-bar {
  height: 6px;
  background: var(--bg-elevated, #252540);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent, #10b981), var(--accent-secondary, #059669));
  border-radius: 3px;
  transition: width 200ms ease;
}

.progress-text {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 12px;
  color: var(--text-secondary, #888);
}

.success-section,
.error-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px;
  margin-top: 16px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
}

.success-section {
  background: rgba(16, 185, 129, 0.1);
  color: var(--accent, #10b981);
}

.error-section {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.success-section svg,
.error-section svg {
  width: 20px;
  height: 20px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 20px 24px;
  border-top: 1px solid var(--border-subtle, #2d2d44);
  background: var(--bg-elevated, #252540);
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 18px;
  font-size: 13px;
  font-weight: 600;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: all 150ms ease;
  font-family: inherit;
}

.btn svg {
  width: 16px;
  height: 16px;
}

.btn-ghost {
  background: transparent;
  color: var(--text-secondary, #888);
  border: 1px solid var(--border-default, #2d2d44);
}

.btn-ghost:hover:not(:disabled) {
  background: var(--bg-surface, #1a1a2e);
  color: var(--text-primary, #f0f0f0);
}

.btn-primary {
  background: var(--accent, #10b981);
  color: white;
  min-width: 140px;
}

.btn-primary:hover:not(:disabled) {
  background: var(--accent-secondary, #059669);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
</style>
