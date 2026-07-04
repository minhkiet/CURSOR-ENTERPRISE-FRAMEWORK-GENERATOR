<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getTemplateById, templates } from '../data/templates'

const route = useRoute()
const router = useRouter()

const template = computed(() => getTemplateById(route.params.id as string))

const viewMode = ref<'desktop' | 'tablet' | 'mobile'>('desktop')
const showInfo = ref(true)
const downloadStatus = ref<'idle' | 'preparing' | 'ready'>('idle')

const iframeSrc = computed(() => {
  if (!template.value) return ''
  return `/templates/${template.value.id}/index.html`
})

const otherTemplates = computed(() =>
  templates.filter((t) => t.id !== template.value?.id).slice(0, 3)
)

function backToGallery() {
  router.push('/templates')
}

function previewTemplate(id: string) {
  router.push(`/templates/${id}`)
}

function downloadTemplate() {
  if (!template.value) return
  downloadStatus.value = 'preparing'
  // Simulate prep then trigger download
  setTimeout(() => {
    downloadStatus.value = 'ready'
    const link = document.createElement('a')
    link.href = `/templates/${template.value!.id}/${template.value!.id}-landing.zip`
    link.download = `${template.value!.id}-landing.zip`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    setTimeout(() => (downloadStatus.value = 'idle'), 2000)
  }, 600)
}

function downloadAll() {
  downloadStatus.value = 'preparing'
  setTimeout(() => {
    downloadStatus.value = 'ready'
    const link = document.createElement('a')
    link.href = `/templates/all-templates.zip`
    link.download = `cef-landing-templates.zip`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    setTimeout(() => (downloadStatus.value = 'idle'), 2000)
  }, 800)
}

const iframeRef = ref<HTMLIFrameElement | null>(null)

function viewSource() {
  if (!template.value) return
  window.open(`/templates/${template.value.id}/index.html`, '_blank')
}

function onIframeLoad() {
  try {
    iframeRef.value?.contentWindow?.scrollTo(0, 0)
  } catch (_e) {
    // ignore cross-origin access errors
  }
}

function refreshFrame() {
  if (iframeRef.value) {
    const src = iframeRef.value.src
    iframeRef.value.src = 'about:blank'
    // Force a reload on the next tick so the new src fully resets scroll
    requestAnimationFrame(() => {
      if (iframeRef.value) {
        iframeRef.value.src = src
      }
    })
  }
}
</script>

<template>
  <div v-if="template" class="preview-page" :style="{ '--tpl-accent': template.accent, '--tpl-accent-2': template.accentSecondary }">
    <!-- Top Bar -->
    <section class="preview-topbar">
      <div class="container">
        <div class="preview-topbar-inner">
          <button class="back-btn" @click="backToGallery">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 12H5M12 19l-7-7 7-7" />
            </svg>
            <span>Quay lại gallery</span>
          </button>

          <div class="preview-meta">
            <span class="preview-meta-cat">{{ template.industry }}</span>
            <span class="preview-meta-sep">/</span>
            <h1 class="preview-meta-title">{{ template.name }}</h1>
          </div>

          <div class="preview-actions">
            <button class="info-toggle" :class="{ active: showInfo }" @click="showInfo = !showInfo" :aria-label="showInfo ? 'Ẩn thông tin' : 'Hiện thông tin'">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" />
                <path d="M12 16v-4M12 8h.01" />
              </svg>
            </button>
            <button class="src-btn" @click="viewSource" title="Xem source">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="16 18 22 12 16 6" />
                <polyline points="8 6 2 12 8 18" />
              </svg>
              <span>Source</span>
            </button>
            <button class="dl-btn" @click="downloadTemplate" :disabled="downloadStatus !== 'idle'">
              <svg v-if="downloadStatus === 'idle'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3" />
              </svg>
              <svg v-else-if="downloadStatus === 'preparing'" class="spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12a9 9 0 11-6.219-8.56" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12" />
              </svg>
              <span>
                {{
                  downloadStatus === 'idle' ? 'Tải về .zip' :
                  downloadStatus === 'preparing' ? 'Đang chuẩn bị...' :
                  'Đã tải!'
                }}
              </span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <div class="preview-layout">
      <!-- Side Info -->
      <aside v-if="showInfo" class="preview-sidebar">
        <div class="sidebar-section">
          <span class="sidebar-label">Tagline</span>
          <p class="sidebar-tagline">{{ template.tagline }}</p>
          <p class="sidebar-desc">{{ template.description }}</p>
        </div>

        <div class="sidebar-section">
          <span class="sidebar-label">Thông số</span>
          <div class="sidebar-stats">
            <div v-for="h in template.highlights" :key="h.label" class="sidebar-stat">
              <div class="sidebar-stat-value">{{ h.value }}</div>
              <div class="sidebar-stat-label">{{ h.label }}</div>
            </div>
          </div>
        </div>

        <div class="sidebar-section">
          <span class="sidebar-label">Tính năng chính</span>
          <ul class="sidebar-features">
            <li v-for="f in template.features" :key="f">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="20 6 9 17 4 12" />
              </svg>
              {{ f }}
            </li>
          </ul>
        </div>

        <div class="sidebar-section">
          <span class="sidebar-label">Tech stack</span>
          <div class="sidebar-tech">
            <span v-for="tech in template.techStack" :key="tech" class="tech-pill">{{ tech }}</span>
          </div>
        </div>

        <div class="sidebar-section">
          <span class="sidebar-label">File info</span>
          <div class="sidebar-file">
            <div class="file-row">
              <span>Số trang</span>
              <strong>{{ template.pages }}</strong>
            </div>
            <div class="file-row">
              <span>Dung lượng</span>
              <strong>{{ template.fileSize }}</strong>
            </div>
            <div class="file-row">
              <span>Format</span>
              <strong>HTML/CSS/JS</strong>
            </div>
          </div>
        </div>

        <button class="sidebar-dl" @click="downloadTemplate">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3" />
          </svg>
          Tải template này
        </button>
      </aside>

      <!-- Iframe Preview -->
      <div class="preview-stage">
        <div class="device-bar">
          <div class="device-modes">
            <button
              v-for="mode in ['desktop', 'tablet', 'mobile'] as const"
              :key="mode"
              class="device-btn"
              :class="{ active: viewMode === mode }"
              @click="viewMode = mode"
            >
              <svg v-if="mode === 'desktop'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="3" width="20" height="14" rx="2" />
                <path d="M8 21h8M12 17v4" />
              </svg>
              <svg v-else-if="mode === 'tablet'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="4" y="2" width="16" height="20" rx="2" />
                <path d="M11 18h2" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="5" y="2" width="14" height="20" rx="2" />
                <path d="M12 18h.01" />
              </svg>
              <span>{{ mode === 'desktop' ? 'Desktop' : mode === 'tablet' ? 'Tablet' : 'Mobile' }}</span>
            </button>
          </div>
          <div class="device-url">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" />
              <path d="M7 11V7a5 5 0 0110 0v4" />
            </svg>
            <span>cef.minhkiet.dev/templates/{{ template.id }}</span>
          </div>
          <div class="device-action">
            <button class="device-refresh" @click="refreshFrame">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M23 4v6h-6M1 20v-6h6" />
                <path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15" />
              </svg>
            </button>
          </div>
        </div>

        <div class="device-frame" :class="`device-${viewMode}`">
          <iframe
            ref="iframeRef"
            :src="iframeSrc"
            class="tpl-frame"
            :title="template.name"
            @load="onIframeLoad"
          ></iframe>
        </div>
      </div>
    </div>

    <!-- Related -->
    <section class="preview-related">
      <div class="container">
        <div class="section-header">
          <div class="section-label">Khám phá thêm</div>
          <h2 class="section-title">Templates khác bạn có thể thích</h2>
        </div>
        <div class="related-grid">
          <article
            v-for="t in otherTemplates"
            :key="t.id"
            class="related-card"
            :style="{ '--rc-accent': t.accent }"
            @click="previewTemplate(t.id)"
          >
            <div class="related-thumb" :style="{ background: t.bgGradient }">
              <div class="related-thumb-mock">
                <div class="rt-line" :style="{ background: t.accent, width: '60%' }"></div>
                <div class="rt-line" :style="{ background: t.accentSecondary, opacity: 0.5, width: '80%' }"></div>
                <div class="rt-blocks">
                  <div :style="{ background: t.accent, opacity: 0.4 }"></div>
                  <div :style="{ background: t.accentSecondary, opacity: 0.4 }"></div>
                  <div :style="{ background: t.accent, opacity: 0.3 }"></div>
                </div>
              </div>
            </div>
            <div class="related-body">
              <span class="related-cat">{{ t.industry }}</span>
              <h3>{{ t.name }}</h3>
              <p>{{ t.tagline }}</p>
            </div>
          </article>
        </div>

        <div class="download-all-bar">
          <div class="dab-content">
            <div class="dab-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z" />
                <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
                <line x1="12" y1="22.08" x2="12" y2="12" />
              </svg>
            </div>
            <div>
              <h3>Tải tất cả 6 templates</h3>
              <p>Bundle đầy đủ với documentation và assets</p>
            </div>
          </div>
          <button class="dab-btn" @click="downloadAll">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3" />
            </svg>
            Tải bộ đầy đủ
          </button>
        </div>
      </div>
    </section>
  </div>

  <div v-else class="not-found">
    <div class="container">
      <h2>Không tìm thấy template</h2>
      <p>Template không tồn tại hoặc đã bị xóa.</p>
      <button class="cta-btn" @click="backToGallery">Quay lại gallery</button>
    </div>
  </div>
</template>

<style scoped>
.preview-page {
  --tpl-accent: #6366f1;
  --tpl-accent-2: #a78bfa;
  padding-top: 60px;
}

.preview-topbar {
  position: sticky;
  top: 60px;
  z-index: 40;
  background: rgba(7, 7, 26, 0.92);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border-soft);
  padding: 14px 0;
}

.preview-topbar-inner {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--t-base);
  font-family: inherit;
}

.back-btn:hover {
  color: var(--text-primary);
  border-color: var(--border-strong);
}

.back-btn svg {
  width: 14px;
  height: 14px;
}

.preview-meta {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.preview-meta-cat {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--tpl-accent);
  text-transform: uppercase;
}

.preview-meta-sep {
  color: var(--text-faint);
}

.preview-meta-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.preview-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-toggle,
.src-btn,
.dl-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--t-base);
  font-family: inherit;
}

.info-toggle:hover,
.src-btn:hover {
  color: var(--text-primary);
  border-color: var(--border-strong);
}

.info-toggle.active {
  color: var(--tpl-accent);
  border-color: var(--tpl-accent);
  background: rgba(99, 102, 241, 0.08);
}

.dl-btn {
  background: var(--tpl-accent);
  color: #fff;
  border-color: transparent;
}

.dl-btn:hover:not(:disabled) {
  background: var(--tpl-accent-2);
  transform: translateY(-1px);
}

.dl-btn:disabled {
  opacity: 0.85;
  cursor: not-allowed;
}

.info-toggle svg,
.src-btn svg,
.dl-btn svg {
  width: 14px;
  height: 14px;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.preview-layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  min-height: calc(100vh - 60px);
}

.preview-sidebar {
  border-right: 1px solid var(--border-soft);
  background: var(--bg-surface);
  padding: 24px;
  overflow-y: auto;
  max-height: calc(100vh - 60px);
  position: sticky;
  top: 60px;
}

.sidebar-section {
  padding-bottom: 20px;
  margin-bottom: 20px;
  border-bottom: 1px solid var(--border-subtle);
}

.sidebar-section:last-of-type {
  border-bottom: none;
}

.sidebar-label {
  display: block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-bottom: 10px;
}

.sidebar-tagline {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.4;
  margin: 0 0 8px;
}

.sidebar-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.65;
  margin: 0;
}

.sidebar-stats {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
}

.sidebar-stat {
  padding: 12px 8px;
  background: var(--bg-raised);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  text-align: center;
}

.sidebar-stat-value {
  font-size: 16px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--tpl-accent), var(--tpl-accent-2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.sidebar-stat-label {
  font-size: 10px;
  color: var(--text-muted);
  margin-top: 4px;
}

.sidebar-features {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sidebar-features li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.sidebar-features svg {
  width: 14px;
  height: 14px;
  color: var(--tpl-accent);
  flex-shrink: 0;
  margin-top: 2px;
}

.sidebar-tech {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tech-pill {
  padding: 4px 10px;
  font-size: 11px;
  font-weight: 600;
  background: var(--bg-raised);
  border: 1px solid var(--border-soft);
  color: var(--text-secondary);
  border-radius: var(--radius-full);
  font-family: var(--font-mono);
}

.sidebar-file {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.file-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: var(--text-secondary);
  padding: 6px 0;
}

.file-row strong {
  color: var(--text-primary);
  font-weight: 700;
}

.sidebar-dl {
  width: 100%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  background: var(--tpl-accent);
  color: #fff;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all var(--t-base);
  font-family: inherit;
  margin-top: 4px;
}

.sidebar-dl:hover {
  background: var(--tpl-accent-2);
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.sidebar-dl svg {
  width: 16px;
  height: 16px;
}

.preview-stage {
  background:
    repeating-linear-gradient(45deg, rgba(255, 255, 255, 0.01) 0 2px, transparent 2px 16px),
    var(--bg-void);
  display: flex;
  flex-direction: column;
}

.device-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  background: var(--bg-base);
  border-bottom: 1px solid var(--border-soft);
}

.device-modes {
  display: flex;
  gap: 4px;
  padding: 3px;
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-md);
}

.device-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 10px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 600;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--t-base);
  font-family: inherit;
}

.device-btn:hover {
  color: var(--text-primary);
}

.device-btn.active {
  background: var(--bg-elevated);
  color: var(--text-primary);
}

.device-btn svg {
  width: 14px;
  height: 14px;
}

.device-url {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-md);
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-secondary);
}

.device-url svg {
  width: 12px;
  height: 12px;
  color: var(--color-success);
}

.device-refresh {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--t-base);
}

.device-refresh:hover {
  color: var(--text-primary);
  border-color: var(--border-strong);
}

.device-refresh svg {
  width: 14px;
  height: 14px;
}

.device-frame {
  flex: 1;
  padding: 24px;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  overflow: auto;
}

.tpl-frame {
  width: 100%;
  height: calc(100vh - 220px);
  min-height: 600px;
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-md);
  background: #fff;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  transition: max-width var(--t-base);
}

.device-tablet .tpl-frame {
  max-width: 768px;
  height: 1024px;
  max-height: calc(100vh - 220px);
}

.device-mobile .tpl-frame {
  max-width: 375px;
  height: 812px;
  max-height: calc(100vh - 220px);
}

.preview-related {
  padding: 80px 0;
  background: var(--bg-base);
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

.related-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: all var(--t-base);
}

.related-card:hover {
  border-color: var(--rc-accent);
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

.related-thumb {
  aspect-ratio: 16 / 10;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.related-thumb-mock {
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 6px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.rt-line {
  height: 6px;
  border-radius: 3px;
}

.rt-blocks {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
  margin-top: 6px;
}

.rt-blocks > div {
  height: 24px;
  border-radius: 4px;
}

.related-body {
  padding: 20px;
}

.related-cat {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--rc-accent);
  text-transform: uppercase;
}

.related-body h3 {
  font-size: 16px;
  font-weight: 700;
  margin: 6px 0 4px;
  color: var(--text-primary);
}

.related-body p {
  font-size: 12px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

.download-all-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 24px 32px;
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
}

.download-all-bar::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--gradient-surface);
  pointer-events: none;
}

.dab-content {
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
}

.dab-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-primary);
  border-radius: var(--radius-md);
  color: #fff;
  flex-shrink: 0;
}

.dab-icon svg {
  width: 24px;
  height: 24px;
}

.dab-content h3 {
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 2px;
  color: var(--text-primary);
}

.dab-content p {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0;
}

.dab-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--gradient-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all var(--t-base);
  font-family: inherit;
  box-shadow: 0 8px 24px rgba(120, 119, 232, 0.3);
}

.dab-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(120, 119, 232, 0.4);
}

.dab-btn svg {
  width: 16px;
  height: 16px;
}

.not-found {
  padding: 200px 0;
  text-align: center;
}

.not-found h2 {
  font-size: 28px;
  margin-bottom: 8px;
}

.not-found p {
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: var(--gradient-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
}

@media (max-width: 1024px) {
  .preview-layout {
    grid-template-columns: 1fr;
  }

  .preview-sidebar {
    position: relative;
    top: 0;
    max-height: none;
    border-right: none;
    border-bottom: 1px solid var(--border-soft);
  }

  .device-url {
    display: none;
  }

  .tpl-frame {
    height: 700px;
  }

  .download-all-bar {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
  }
}

@media (max-width: 640px) {
  .preview-meta-title {
    font-size: 13px;
  }

  .src-btn span {
    display: none;
  }

  .device-bar {
    padding: 8px 12px;
  }

  .device-btn span {
    display: none;
  }
}
</style>