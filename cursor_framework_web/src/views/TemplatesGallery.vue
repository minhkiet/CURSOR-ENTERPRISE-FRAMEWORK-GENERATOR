<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { templates, type Template } from '../data/templates'
import TemplatePreviewSvg from '../components/TemplatePreviewSvg.vue'

const router = useRouter()
const selectedCategory = ref<string>('all')
const searchQuery = ref<string>('')

// Auto-Scroll States
const isShowcaseScrollAll = ref(false)
const activeAutoScroll = ref<Record<string, boolean>>({})

// Quick Preview Modal
const quickPreviewTemplate = ref<Template | null>(null)
const isQuickPreviewOpen = ref(false)
const quickIframeRef = ref<HTMLIFrameElement | null>(null)
const isQuickAutoScrolling = ref(false)
let quickScrollInterval: ReturnType<typeof setInterval> | null = null

const categories = computed(() => {
  const set = new Set<string>(templates.map((t) => t.industry))
  return ['all', ...Array.from(set)]
})

const filteredTemplates = computed<Template[]>(() => {
  return templates.filter((t) => {
    const matchesCategory = selectedCategory.value === 'all' || t.industry === selectedCategory.value
    const q = searchQuery.value.toLowerCase().trim()
    const matchesSearch =
      !q ||
      t.name.toLowerCase().includes(q) ||
      t.tagline.toLowerCase().includes(q) ||
      t.tags.some((tag) => tag.toLowerCase().includes(q))
    return matchesCategory && matchesSearch
  })
})

function viewTemplate(t: Template) {
  router.push(`/templates/${t.id}`)
}

function toggleCardAutoScroll(id: string, e?: Event) {
  if (e) e.stopPropagation()
  activeAutoScroll.value[id] = !activeAutoScroll.value[id]
}

function toggleShowcaseScrollAll() {
  isShowcaseScrollAll.value = !isShowcaseScrollAll.value
  if (isShowcaseScrollAll.value) {
    templates.forEach((t) => {
      activeAutoScroll.value[t.id] = true
    })
  } else {
    activeAutoScroll.value = {}
  }
}

function openQuickPreview(t: Template, e?: Event) {
  if (e) e.stopPropagation()
  quickPreviewTemplate.value = t
  isQuickPreviewOpen.value = true
  isQuickAutoScrolling.value = true
  setTimeout(() => {
    startQuickAutoScroll()
  }, 350)
}

function closeQuickPreview() {
  isQuickPreviewOpen.value = false
  quickPreviewTemplate.value = null
  stopQuickAutoScroll()
}

function toggleQuickAutoScroll() {
  isQuickAutoScrolling.value = !isQuickAutoScrolling.value
  if (isQuickAutoScrolling.value) {
    startQuickAutoScroll()
  } else {
    stopQuickAutoScroll()
  }
}

function startQuickAutoScroll() {
  stopQuickAutoScroll()
  const iframe = quickIframeRef.value
  if (!iframe) return
  let dir = 1
  quickScrollInterval = setInterval(() => {
    try {
      const win = iframe.contentWindow
      const doc = iframe.contentDocument || win?.document
      if (doc && win) {
        const cur = win.scrollY || 0
        const maxS = Math.max(doc.documentElement.scrollHeight, doc.body.scrollHeight) - win.innerHeight
        if (maxS <= 0) return
        if (cur >= maxS - 10) dir = -1
        else if (cur <= 10) dir = 1
        win.scrollBy({ top: 3 * dir, behavior: 'auto' })
      }
    } catch (_e) {
      // fallback
    }
  }, 25)
}

function stopQuickAutoScroll() {
  if (quickScrollInterval) {
    clearInterval(quickScrollInterval)
    quickScrollInterval = null
  }
}

onUnmounted(() => {
  stopQuickAutoScroll()
})
</script>

<template>
  <div class="gallery-page">
    <section class="gallery-hero">
      <div class="container">
        <div class="gallery-hero-content">
          <div class="section-label">Kho Templates Thực Chiến 2026</div>
          <h1 class="gallery-title">
            {{ templates.length }} Production-Ready Templates.<br />
            <span class="gallery-title-accent">Chuẩn Craft, Không Thuần AI.</span>
          </h1>
          <p class="gallery-subtitle">
            Bao gồm 5 bộ chuyên sâu: <strong>UI/UX Enterprise</strong>, <strong>Dashboard UI Pro</strong>, <strong>Frontend Taste (57 Gates)</strong>, <strong>CMS SaaS v4</strong> và <strong>Image Workflow Studio</strong>. Mỗi template đều có thể tự động cuộn lướt xem giao diện thực tế.
          </p>

          <div class="gallery-hero-actions">
            <router-link to="/cms" class="btn btn-primary" style="display: inline-flex; align-items: center; gap: 8px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="16" height="16">
                <rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/>
                <rect x="14" y="14" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/>
              </svg>
              <span>Quản Lý CMS Templates</span>
            </router-link>

            <button
              class="btn btn-secondary showcase-hero-btn"
              :class="{ active: isShowcaseScrollAll }"
              @click="toggleShowcaseScrollAll"
            >
              <svg viewBox="0 0 24 24" fill="currentColor" width="15" height="15">
                <polygon v-if="!isShowcaseScrollAll" points="5 3 19 12 5 21 5 3"/>
                <rect v-else x="6" y="4" width="4" height="16"/>
              </svg>
              <span>{{ isShowcaseScrollAll ? 'Dừng Tự Động Lướt' : 'Bật Tự Động Lướt Xem Web (Showcase)' }}</span>
            </button>
          </div>

          <div class="gallery-stats">
            <div class="gallery-stat">
              <div class="gallery-stat-value">{{ templates.length }}</div>
              <div class="gallery-stat-label">Templates</div>
            </div>
            <div class="gallery-stat">
              <div class="gallery-stat-value">5/5</div>
              <div class="gallery-stat-label">Chuyên Sâu Mới</div>
            </div>
            <div class="gallery-stat">
              <div class="gallery-stat-value">100%</div>
              <div class="gallery-stat-label">Responsive Mobile</div>
            </div>
            <div class="gallery-stat">
              <div class="gallery-stat-value">Auto-Scroll</div>
              <div class="gallery-stat-label">Lướt Web 1-Click</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── FILTER & CONTROLS ─── -->
    <section class="gallery-filter">
      <div class="container">
        <div class="gallery-filter-inner">
          <div class="gallery-search">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Tìm kiếm template (/ui-ux, dashboard, taste, cms...)"
              aria-label="Search templates"
            />
          </div>

          <div class="gallery-categories">
            <button
              v-for="cat in categories"
              :key="cat"
              class="gallery-cat-btn"
              :class="{ active: selectedCategory === cat }"
              @click="selectedCategory = cat"
            >
              {{ cat === 'all' ? 'Tất cả (' + templates.length + ')' : cat }}
            </button>
          </div>

          <button
            class="gallery-showcase-toggle"
            :class="{ active: isShowcaseScrollAll }"
            @click="toggleShowcaseScrollAll"
            title="Tự động cuộn lướt web trên toàn bộ thẻ"
          >
            <span class="showcase-dot"></span>
            <span>{{ isShowcaseScrollAll ? 'Dừng Tự Cuộn' : '⚡ Tự Động Cuộn Lướt Web' }}</span>
          </button>
        </div>
      </div>
    </section>

    <!-- ─── TEMPLATES GRID ─── -->
    <section class="gallery-grid-section" id="templates-grid">
      <div class="container">
        <div class="gallery-grid">
          <article
            v-for="t in filteredTemplates"
            :key="t.id"
            class="template-card"
          >
            <div
              class="template-card-preview"
              :class="{ 'auto-scrolling': isShowcaseScrollAll || activeAutoScroll[t.id] }"
            >
              <TemplatePreviewSvg :slug="t.slug" />

              <!-- Quick scroll pill on card top-right -->
              <button
                class="card-scroll-pill"
                :class="{ active: isShowcaseScrollAll || activeAutoScroll[t.id] }"
                @click="toggleCardAutoScroll(t.id, $event)"
                :title="activeAutoScroll[t.id] ? 'Dừng lướt' : 'Bật tự cuộn lướt web'"
              >
                <span class="scroll-status-dot"></span>
                <span>{{ (isShowcaseScrollAll || activeAutoScroll[t.id]) ? 'Đang cuộn' : 'Tự cuộn' }}</span>
              </button>

              <div class="template-card-overlay">
                <button class="overlay-btn" @click="viewTemplate(t)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  <span>Xem Chi Tiết</span>
                </button>
                <button class="overlay-btn secondary" @click="openQuickPreview(t, $event)" title="Xem nhanh trang web trực tiếp kèm tự cuộn">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                    <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>
                  </svg>
                  <span>Lướt Nhanh</span>
                </button>
              </div>
            </div>

            <div class="template-card-body">
              <div class="template-card-meta">
                <span class="template-card-category">{{ t.industry }}</span>
                <span class="template-card-pages">{{ t.pages }} trang · {{ t.fileSize }}</span>
              </div>
              <h3 class="template-card-title">{{ t.name }}</h3>
              <p class="template-card-tagline">{{ t.tagline }}</p>

              <div class="template-card-tags">
                <span v-for="tag in t.tags.slice(0, 3)" :key="tag" class="template-tag">
                  {{ tag }}
                </span>
              </div>

              <div class="template-card-actions">
                <button class="btn btn-primary template-btn" @click="viewTemplate(t)">
                  <span>Live Demo</span>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12">
                    <path d="M7 17l9.2-9.2M17 17V7H7"/>
                  </svg>
                </button>
                <button class="btn btn-ghost template-btn" @click="openQuickPreview(t, $event)">
                  <span>Tự Cuộn</span>
                </button>
              </div>
            </div>
          </article>
        </div>

        <div v-if="filteredTemplates.length === 0" class="gallery-empty">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
          <h3>Không tìm thấy template phù hợp</h3>
          <p>Thử tìm với từ khóa khác như "ui-ux", "dashboard", "taste", "cms" hoặc "image".</p>
        </div>
      </div>
    </section>

    <!-- ─── QUICK PREVIEW MODAL ─── -->
    <div
      v-if="isQuickPreviewOpen && quickPreviewTemplate"
      class="quick-modal-backdrop"
      @click="closeQuickPreview"
      role="dialog"
      aria-modal="true"
    >
      <div class="quick-modal-card" @click.stop>
        <div class="quick-modal-bar">
          <div class="quick-modal-info">
            <span class="quick-ind">{{ quickPreviewTemplate.industry }}</span>
            <span class="quick-sep">/</span>
            <strong>{{ quickPreviewTemplate.name }}</strong>
            <span class="quick-tagline">— {{ quickPreviewTemplate.tagline }}</span>
          </div>

          <div class="quick-modal-actions">
            <button
              class="quick-scroll-toggle"
              :class="{ active: isQuickAutoScrolling }"
              @click="toggleQuickAutoScroll"
              :title="isQuickAutoScrolling ? 'Tạm dừng cuộn' : 'Bật tự động lướt xem web'"
            >
              <span>{{ isQuickAutoScrolling ? '⏸ Dừng Tự Cuộn' : '▶ Bật Tự Động Lướt' }}</span>
            </button>
            <button class="btn btn-primary btn-sm" @click="viewTemplate(quickPreviewTemplate)">
              Trang Chi Tiết
            </button>
            <button class="quick-close" @click="closeQuickPreview" aria-label="Đóng cửa sổ">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                <path d="M18 6L6 18M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="quick-modal-iframe-wrap">
          <iframe
            ref="quickIframeRef"
            :src="`/templates/${quickPreviewTemplate.id}/index.html`"
            class="quick-modal-iframe"
            :title="quickPreviewTemplate.name"
          ></iframe>
        </div>
      </div>
    </div>

    <!-- ─── CTA BOTTOM ─── -->
    <section class="gallery-cta">
      <div class="container">
        <div class="cta-box">
          <div class="cta-content">
            <div class="section-label">Tự Động Hóa Với Cursor</div>
            <h2 class="cta-title">Cần xây dựng website chuyên nghiệp riêng?</h2>
            <p class="cta-desc">
              Sử dụng các lệnh <code>/ui-ux</code>, <code>/dashboard-ui</code>, <code>/frontend-taste</code>, <code>/cms-landing-enterprise</code> hoặc <code>/image-workflow</code> trong Cursor IDE để tạo ngay giao diện chuẩn Enterprise trong 3 phút.
            </p>
          </div>
          <router-link to="/prompts" class="btn btn-primary">
            <span>Khám Phá Kho Prompts</span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.gallery-page {
  padding-top: 60px;
}

.gallery-hero {
  padding: 80px 0 60px;
  background: radial-gradient(
    ellipse 80% 50% at 50% -20%,
    rgba(120, 119, 198, 0.12),
    transparent
  );
  border-bottom: 1px solid var(--border-subtle);
}

.gallery-hero-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.gallery-title {
  font-size: 42px;
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  margin: 16px 0 20px;
}

.gallery-title-accent {
  background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.gallery-subtitle {
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-secondary);
  max-width: 620px;
  margin: 0 auto 32px;
}

.gallery-hero-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.showcase-hero-btn {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  color: var(--text-primary);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.showcase-hero-btn.active {
  background: var(--accent-dim);
  border-color: var(--accent);
  color: var(--accent);
}

.gallery-stats {
  display: flex;
  justify-content: center;
  gap: 32px;
  padding-top: 32px;
  border-top: 1px solid var(--border-subtle);
}

.gallery-stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.gallery-stat-value {
  font-family: var(--font-mono);
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
}

.gallery-stat-label {
  font-size: 10.5px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* Filter bar */
.gallery-filter {
  padding: 16px 0;
  position: sticky;
  top: 60px;
  z-index: 50;
  background: var(--bg-canvas);
  border-bottom: 1px solid var(--border-subtle);
}

.gallery-filter-inner {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}

.gallery-search {
  flex: 1;
  min-width: 240px;
  position: relative;
  display: flex;
  align-items: center;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: 0 12px;
  transition: border-color var(--t-base);
}

.gallery-search:focus-within {
  border-color: var(--accent);
}

.gallery-search svg {
  width: 15px;
  height: 15px;
  color: var(--text-muted);
  flex-shrink: 0;
}

.gallery-search input {
  flex: 1;
  padding: 8px 10px;
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-size: 13px;
  font-family: inherit;
}

.gallery-categories {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.gallery-cat-btn {
  padding: 6px 12px;
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

.gallery-cat-btn:hover {
  color: var(--text-primary);
  border-color: var(--border-strong);
}

.gallery-cat-btn.active {
  color: var(--bg-canvas);
  background: var(--accent);
  border-color: var(--accent);
  font-weight: 600;
}

.gallery-showcase-toggle {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 7px 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--t-fast);
}

.gallery-showcase-toggle:hover {
  border-color: var(--accent);
  color: var(--text-primary);
}

.gallery-showcase-toggle.active {
  background: var(--accent-dim);
  border-color: var(--accent);
  color: var(--accent);
}

.showcase-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 8px var(--accent);
}

/* Grid & Card */
.gallery-grid-section {
  padding: 50px 0 90px;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
}

.template-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  overflow: hidden;
  transition: border-color var(--t-base), transform var(--t-base), box-shadow var(--t-base);
  display: flex;
  flex-direction: column;
}

.template-card:hover {
  border-color: var(--border-default);
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
}

.template-card-preview {
  position: relative;
  aspect-ratio: 16 / 10;
  background: #08080c;
  overflow: hidden;
  border-bottom: 1px solid var(--border-subtle);
}

/* Smooth Auto-Scroll Mockup Effect */
.template-card:hover :deep(.thumbnail-inner),
.template-card-preview.auto-scrolling :deep(.thumbnail-inner) {
  animation: smoothScrollMockup 7s cubic-bezier(0.4, 0, 0.2, 1) infinite alternate;
}

@keyframes smoothScrollMockup {
  0% { transform: translateY(0); }
  25% { transform: translateY(-10%); }
  60% { transform: translateY(-24%); }
  100% { transform: translateY(-38%); }
}

/* Card Scroll Pill */
.card-scroll-pill {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 10;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 9px;
  background: rgba(9, 9, 12, 0.82);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: var(--radius-pill);
  font-size: 10.5px;
  font-weight: 700;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--t-fast);
}

.card-scroll-pill:hover, .card-scroll-pill.active {
  background: var(--accent-dim);
  border-color: var(--accent);
  color: var(--accent);
}

.scroll-status-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--accent);
}

/* Card Overlay */
.template-card-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(9, 9, 11, 0.92) 0%,
    rgba(9, 9, 11, 0.45) 50%,
    rgba(9, 9, 11, 0.15) 100%
  );
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  opacity: 0;
  transition: opacity 0.25s ease-out;
  backdrop-filter: blur(3px);
  pointer-events: none;
}

.template-card:hover .template-card-overlay {
  opacity: 1;
  pointer-events: auto;
}

.overlay-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 9px 18px;
  background: #ffffff;
  color: #09090b;
  border: none;
  border-radius: var(--radius-pill);
  font-size: 12.5px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
  transition: all 0.2s;
}

.overlay-btn:hover {
  background: var(--accent);
  color: #000000;
  transform: scale(1.04);
}

.overlay-btn.secondary {
  background: rgba(255, 255, 255, 0.18);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(8px);
}

.overlay-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.32);
  color: #ffffff;
}

/* Card Body */
.template-card-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

.template-card-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.template-card-category {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--accent);
  text-transform: uppercase;
}

.template-card-pages {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
}

.template-card-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.25;
}

.template-card-tagline {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.45;
}

.template-card-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-top: 4px;
}

.template-tag {
  font-size: 11px;
  padding: 2px 7px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
}

.template-card-actions {
  display: flex;
  gap: 8px;
  margin-top: auto;
  padding-top: 14px;
  border-top: 1px solid var(--border-subtle);
}

.template-btn {
  flex: 1;
  justify-content: center;
  padding: 8px 12px;
  font-size: 12.5px;
}

/* Quick Modal */
.quick-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(12px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  animation: fadeIn 0.2s ease-out;
}

.quick-modal-card {
  width: 100%;
  max-width: 1180px;
  height: 88vh;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7);
}

.quick-modal-bar {
  padding: 12px 20px;
  background: #09090e;
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.quick-modal-info {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
}

.quick-ind {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  color: var(--accent);
}

.quick-sep {
  color: var(--text-muted);
}

.quick-tagline {
  color: var(--text-secondary);
  font-size: 12px;
}

.quick-modal-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.quick-scroll-toggle {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.quick-scroll-toggle.active {
  background: var(--accent-dim);
  border-color: var(--accent);
  color: var(--accent);
}

.quick-close {
  width: 30px;
  height: 30px;
  border-radius: var(--radius-sm);
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.quick-close:hover {
  color: var(--text-primary);
}

.quick-modal-iframe-wrap {
  flex: 1;
  position: relative;
  background: #000000;
}

.quick-modal-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

/* CTA */
.gallery-cta {
  padding: 60px 0 100px;
}

.cta-box {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 32px;
  align-items: center;
  padding: 36px 40px;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
}

.cta-title {
  font-size: 22px;
  font-weight: 700;
  margin: 8px 0;
}

.cta-desc {
  font-size: 13.5px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.cta-desc code {
  font-family: var(--font-mono);
  color: var(--accent);
  background: var(--accent-dim);
  padding: 1px 6px;
  border-radius: 4px;
}

@media (max-width: 900px) {
  .gallery-grid { grid-template-columns: 1fr; }
  .cta-box { grid-template-columns: 1fr; padding: 28px; }
  .quick-tagline { display: none; }
}
</style>