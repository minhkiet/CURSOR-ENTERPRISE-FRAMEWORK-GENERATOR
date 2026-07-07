<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getTemplateById, templates } from '../data/templates'
import DownloadModal from '../components/DownloadModal.vue'

const route = useRoute()
const router = useRouter()

const template = computed(() => getTemplateById(route.params.id as string))

const viewMode = ref<'desktop' | 'tablet' | 'mobile'>('desktop')
const showInfo = ref(true)
const showDownloadModal = ref(false)

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

function openDownloadModal() {
  showDownloadModal.value = true
}

function closeDownloadModal() {
  showDownloadModal.value = false
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
    // ignore cross-origin access
  }
}

function refreshFrame() {
  if (iframeRef.value) {
    const src = iframeRef.value.src
    iframeRef.value.src = 'about:blank'
    requestAnimationFrame(() => {
      if (iframeRef.value) {
        iframeRef.value.src = src
      }
    })
  }
}
</script>

<template>
  <div v-if="template" class="preview-page">
    <section class="preview-topbar">
      <div class="container">
        <div class="preview-topbar-inner">
          <button class="back-btn" @click="backToGallery">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
            <span>Back to gallery</span>
          </button>

          <div class="preview-meta">
            <span class="preview-meta-cat">{{ template.industry }}</span>
            <span class="preview-meta-sep">/</span>
            <h1 class="preview-meta-title">{{ template.name }}</h1>
          </div>

          <div class="preview-actions">
            <button class="action-btn" @click="viewSource">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
              <span>Source</span>
            </button>
            <button class="action-btn" @click="showInfo = !showInfo" :aria-label="showInfo ? 'Hide info' : 'Show info'">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>
              <span>{{ showInfo ? 'Hide info' : 'Info' }}</span>
            </button>
            <button class="btn btn-primary dl-btn" @click="openDownloadModal">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
              <span>Tải về</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <div class="preview-layout" :class="{ 'info-hidden': !showInfo }">
      <aside class="preview-sidebar">
        <div class="sidebar-section">
          <span class="sidebar-label">About</span>
          <p class="sidebar-tagline">{{ template.tagline }}</p>
          <p class="sidebar-desc">{{ template.description }}</p>
        </div>

        <div class="sidebar-section">
          <span class="sidebar-label">Highlights</span>
          <div class="sidebar-stats">
            <div v-for="h in template.highlights" :key="h.label" class="sidebar-stat">
              <div class="sidebar-stat-value">{{ h.value }}</div>
              <div class="sidebar-stat-label">{{ h.label }}</div>
            </div>
          </div>
        </div>

        <div class="sidebar-section">
          <span class="sidebar-label">Features</span>
          <ul class="sidebar-features">
            <li v-for="f in template.features" :key="f">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
              {{ f }}
            </li>
          </ul>
        </div>

        <div class="sidebar-section">
          <span class="sidebar-label">Tech Stack</span>
          <div class="sidebar-tech">
            <span v-for="tech in template.techStack" :key="tech" class="tech-pill">{{ tech }}</span>
          </div>
        </div>

        <div class="sidebar-section">
          <span class="sidebar-label">File Info</span>
          <div class="sidebar-file">
            <div class="file-row">
              <span>Pages</span>
              <strong>{{ template.pages }}</strong>
            </div>
            <div class="file-row">
              <span>Size</span>
              <strong>{{ template.fileSize }}</strong>
            </div>
            <div class="file-row">
              <span>Format</span>
              <strong>HTML/CSS/JS</strong>
            </div>
          </div>
        </div>
      </aside>

      <div class="preview-stage">
        <div class="device-bar">
          <div class="device-modes">
            <button
              v-for="mode in (['desktop', 'tablet', 'mobile'] as const)"
              :key="mode"
              class="device-btn"
              :class="{ active: viewMode === mode }"
              @click="viewMode = mode"
            >
              <svg v-if="mode === 'desktop'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>
              <svg v-else-if="mode === 'tablet'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M11 18h2"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/></svg>
              <span>{{ mode === 'desktop' ? 'Desktop' : mode === 'tablet' ? 'Tablet' : 'Mobile' }}</span>
            </button>
          </div>
          <div class="device-url">
            <span class="url-dot"></span>
            <span class="url-text">cef.dev/templates/{{ template.id }}</span>
          </div>
          <div class="device-action">
            <button class="device-refresh" @click="refreshFrame" :aria-label="'Refresh preview'">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M23 4v6h-6M1 20v-6h6"/><path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/></svg>
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

    <section class="preview-related">
      <div class="container">
        <div class="section-header">
          <div class="section-label">More templates</div>
          <h2 class="section-title">Other landing pages in the library.</h2>
        </div>
        <div class="related-grid">
          <article
            v-for="t in otherTemplates"
            :key="t.id"
            class="related-card"
            @click="previewTemplate(t.id)"
          >
            <div class="related-thumb">
              <iframe
                :src="`/templates/${t.slug}/`"
                :title="t.name"
                class="related-thumb-iframe"
                loading="lazy"
              ></iframe>
            </div>
            <div class="related-body">
              <span class="related-cat">{{ t.industry }}</span>
              <h3>{{ t.name }}</h3>
              <p>{{ t.tagline }}</p>
            </div>
          </article>
        </div>
      </div>
    </section>
  </div>

  <div v-else class="not-found">
    <div class="container">
      <h2>Template not found</h2>
      <p>The template you requested does not exist or was removed.</p>
      <button class="btn btn-primary" @click="backToGallery">Back to gallery</button>
    </div>
  </div>

  <DownloadModal
    v-if="showDownloadModal && template"
    :template-id="template.id"
    :template-name="template.name"
    :template-industry="template.industry"
    :template-tagline="template.tagline"
    :template-description="template.description"
    @close="closeDownloadModal"
  />
</template>

<style scoped>
.preview-page {
  padding-top: 60px;
}

.preview-topbar {
  position: sticky;
  top: 60px;
  z-index: 40;
  background: var(--bg-canvas);
  border-bottom: 1px solid var(--border-subtle);
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
  padding: 7px 12px;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: 12.5px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--t-fast);
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
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.08em;
  color: var(--accent);
  text-transform: uppercase;
}

.preview-meta-sep {
  color: var(--text-faint);
}

.preview-meta-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.01em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.preview-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 10px;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: 12.5px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--t-fast);
  font-family: inherit;
}

.action-btn:hover {
  color: var(--text-primary);
  border-color: var(--border-strong);
}

.action-btn svg {
  width: 14px;
  height: 14px;
}

.dl-btn {
  font-size: 12.5px;
  padding: 7px 14px;
}

.dl-btn:disabled {
  opacity: 0.85;
  cursor: not-allowed;
}

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
  transition: grid-template-columns 250ms var(--ease-out-quart);
}

.preview-layout.info-hidden {
  grid-template-columns: 0 1fr;
}

.preview-stage {
  min-width: 0;
}

.preview-sidebar {
  border-right: 1px solid var(--border-subtle);
  background: var(--bg-surface);
  padding: 24px;
  overflow-y: auto;
  max-height: calc(100vh - 60px);
  position: sticky;
  top: 60px;
  transition: opacity 200ms var(--ease-out-quart);
}

.preview-layout.info-hidden .preview-sidebar {
  opacity: 0;
  pointer-events: none;
}

.sidebar-section {
  padding-bottom: 20px;
  margin-bottom: 20px;
  border-bottom: 1px solid var(--border-subtle);
}

.sidebar-section:last-child {
  border-bottom: 0;
  padding-bottom: 0;
}

.sidebar-label {
  display: block;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-bottom: 10px;
}

.sidebar-tagline {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  margin: 0 0 8px;
  letter-spacing: -0.01em;
}

.sidebar-desc {
  font-size: 12.5px;
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
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  text-align: center;
}

.sidebar-stat-value {
  font-family: var(--font-mono);
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
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
  font-size: 12.5px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.sidebar-features svg {
  width: 14px;
  height: 14px;
  color: var(--accent);
  flex-shrink: 0;
  margin-top: 2px;
}

.sidebar-tech {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tech-pill {
  padding: 3px 8px;
  font-size: 11px;
  font-weight: 500;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
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
  font-size: 12.5px;
  color: var(--text-secondary);
  padding: 6px 0;
}

.file-row strong {
  color: var(--text-primary);
  font-family: var(--font-mono);
  font-weight: 500;
}

.preview-stage {
  background: var(--bg-canvas);
  display: flex;
  flex-direction: column;
}

.device-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 20px;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
}

.device-modes {
  display: flex;
  gap: 2px;
  padding: 2px;
  background: var(--bg-canvas);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
}

.device-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 9px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 11.5px;
  font-weight: 500;
  border-radius: 4px;
  cursor: pointer;
  transition: all var(--t-fast);
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
  width: 13px;
  height: 13px;
}

.device-url {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: var(--bg-canvas);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: 11.5px;
  color: var(--text-secondary);
  max-width: 360px;
}

.url-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
  flex-shrink: 0;
}

.url-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.device-action {
  display: flex;
  gap: 6px;
}

.device-refresh {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background: var(--bg-canvas);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--t-fast);
}

.device-refresh:hover {
  color: var(--text-primary);
  border-color: var(--border-strong);
}

.device-refresh svg {
  width: 13px;
  height: 13px;
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
  height: calc(100vh - 200px);
  min-height: 600px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: #fff;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  transition: max-width 300ms var(--ease-out-quart);
}

.device-frame {
  width: 100%;
}

.device-tablet .tpl-frame {
  max-width: 768px;
  height: 1024px;
  max-height: calc(100vh - 200px);
}

.device-mobile .tpl-frame {
  max-width: 375px;
  height: 812px;
  max-height: calc(100vh - 200px);
}

.preview-related {
  padding: 60px 0 80px;
  background: var(--bg-canvas);
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 14px;
}

.related-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: all var(--t-base);
}

.related-card:hover {
  border-color: var(--border-default);
  transform: translateY(-2px);
}

.related-thumb {
  aspect-ratio: 16 / 10;
  background: var(--bg-canvas);
  overflow: hidden;
  position: relative;
}

.related-thumb-iframe {
  width: 200%;
  height: 200%;
  transform: scale(0.5);
  transform-origin: top left;
  border: 0;
  pointer-events: none;
  background: #fff;
}

.related-body {
  padding: 16px 18px;
}

.related-cat {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.08em;
  color: var(--accent);
  text-transform: uppercase;
}

.related-body h3 {
  font-size: 15px;
  font-weight: 600;
  margin: 6px 0 4px;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.related-body p {
  font-size: 12px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.55;
}

.not-found {
  padding: 200px 0;
  text-align: center;
}

.not-found h2 {
  font-size: 24px;
  margin-bottom: 8px;
  font-weight: 600;
}

.not-found p {
  color: var(--text-secondary);
  margin-bottom: 24px;
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
    border-bottom: 1px solid var(--border-subtle);
  }

  .device-url {
    display: none;
  }

  .tpl-frame {
    height: 700px;
  }
}

@media (max-width: 640px) {
  .preview-meta-title {
    font-size: 13px;
  }

  .action-btn span {
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