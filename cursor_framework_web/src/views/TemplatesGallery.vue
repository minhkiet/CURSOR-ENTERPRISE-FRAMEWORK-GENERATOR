<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { templates, type Template } from '../data/templates'
import TemplatePreviewSvg from '../components/TemplatePreviewSvg.vue'

const router = useRouter()
const selectedCategory = ref<string>('all')
const searchQuery = ref<string>('')

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
</script>

<template>
  <div class="gallery-page">
    <section class="gallery-hero">
      <div class="container">
        <div class="gallery-hero-content">
          <div class="section-label">Template Library</div>
          <h1 class="gallery-title">
            {{ templates.length }} Production-Ready Templates.<br />
            <span class="gallery-title-accent">Clone, customize & ship.</span>
          </h1>
          <p class="gallery-subtitle">
            Mỗi template là một gói HTML/CSS/JS độc lập, tối ưu tỷ lệ chuyển đổi, tải siêu tốc
            và tương thích hoàn hảo với Next.js, Vue 3 hoặc thuần static web.
          </p>

          <div class="gallery-hero-actions" style="display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap;">
            <router-link to="/cms" class="btn btn-primary" style="display: inline-flex; align-items: center; gap: 8px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="16" height="16">
                <rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/>
                <rect x="14" y="14" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/>
              </svg>
              <span>Quản Lý CMS Templates</span>
            </router-link>
            <a href="#templates-grid" class="btn btn-ghost" style="display: inline-flex; align-items: center; gap: 8px;">
              <span>Khám phá bộ sưu tập</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="16" height="16"><path d="M19 9l-7 7-7-7"/></svg>
            </a>
          </div>

          <div class="gallery-stats">
            <div class="gallery-stat">
              <div class="gallery-stat-value">{{ templates.length }}</div>
              <div class="gallery-stat-label">Templates</div>
            </div>
            <div class="gallery-stat">
              <div class="gallery-stat-value">~250</div>
              <div class="gallery-stat-label">KB avg</div>
            </div>
            <div class="gallery-stat">
              <div class="gallery-stat-value">100%</div>
              <div class="gallery-stat-label">Responsive</div>
            </div>
            <div class="gallery-stat">
              <div class="gallery-stat-value">0</div>
              <div class="gallery-stat-label">Dependencies</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="gallery-filter">
      <div class="container">
        <div class="gallery-filter-inner">
          <div class="gallery-search">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search templates..."
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
              {{ cat === 'all' ? 'All' : cat }}
            </button>
          </div>
        </div>
      </div>
    </section>

    <section class="gallery-grid-section" id="templates-grid">
      <div class="container">
        <div class="gallery-grid">
          <article
            v-for="t in filteredTemplates"
            :key="t.id"
            class="template-card"
          >
            <div class="template-card-preview">
              <TemplatePreviewSvg :slug="t.slug" />
              <div class="template-card-overlay">
                <button class="overlay-btn" @click="viewTemplate(t)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  View demo
                </button>
              </div>
            </div>

            <div class="template-card-body">
              <div class="template-card-meta">
                <span class="template-card-category">{{ t.industry }}</span>
                <span class="template-card-pages">{{ t.pages }} pages · {{ t.fileSize }}</span>
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
                  Preview
                </button>
                <button class="btn btn-ghost template-btn" @click="viewTemplate(t)">
                  Source
                </button>
              </div>
            </div>
          </article>
        </div>

        <div v-if="filteredTemplates.length === 0" class="gallery-empty">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
          <h3>No templates match</h3>
          <p>Try a different search term or category.</p>
        </div>
      </div>
    </section>

    <section class="gallery-cta">
      <div class="container">
        <div class="cta-box">
          <div class="cta-content">
            <div class="section-label">Build your own</div>
            <h2 class="cta-title">Need a custom landing page?</h2>
            <p class="cta-desc">
              The framework ships 39 rules, 17 skills, and 8 agents that turn a one-line
              spec into a production-ready template in minutes.
            </p>
          </div>
          <a href="#/" class="btn btn-primary" @click.prevent="router.push('/')">
            Explore Framework
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
          </a>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.gallery-hero {
  position: relative;
  padding: 140px 0 60px;
  border-bottom: 1px solid var(--border-subtle);
}

.gallery-hero-content {
  max-width: 760px;
}

.gallery-title {
  font-size: clamp(32px, 5vw, 52px);
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.03em;
  margin: 16px 0 20px;
  color: var(--text-primary);
}

.gallery-title-accent {
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 0.85em;
  font-weight: 500;
}

.gallery-subtitle {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.65;
  max-width: 620px;
  margin: 0 0 40px;
}

.gallery-stats {
  display: inline-flex;
  align-items: stretch;
  gap: 0;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.gallery-stat {
  padding: 16px 28px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  border-right: 1px solid var(--border-hairline);
}

.gallery-stat:last-child {
  border-right: 0;
}

.gallery-stat-value {
  font-family: var(--font-mono);
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.gallery-stat-label {
  font-size: 10px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.gallery-filter {
  padding: 24px 0;
  position: sticky;
  top: 60px;
  z-index: 50;
  background: var(--bg-canvas);
  border-bottom: 1px solid var(--border-subtle);
}

.gallery-filter-inner {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.gallery-search {
  flex: 1;
  min-width: 260px;
  position: relative;
  display: flex;
  align-items: center;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: 0 14px;
  transition: border-color var(--t-base);
}

.gallery-search:focus-within {
  border-color: var(--accent);
}

.gallery-search svg {
  width: 16px;
  height: 16px;
  color: var(--text-muted);
  flex-shrink: 0;
}

.gallery-search input {
  flex: 1;
  padding: 10px 12px;
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-size: 13px;
  font-family: inherit;
}

.gallery-search input::placeholder {
  color: var(--text-muted);
}

.gallery-categories {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.gallery-cat-btn {
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

.gallery-cat-btn:hover {
  color: var(--text-primary);
  border-color: var(--border-strong);
}

.gallery-cat-btn.active {
  color: var(--bg-canvas);
  background: var(--accent);
  border-color: var(--accent);
}

.gallery-grid-section {
  padding: 60px 0 100px;
}

/* .gallery-grid and .template-card display/grid rules live in
   src/styles/main.css (global) to avoid scoped-style hash drift. */

.template-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  overflow: hidden;
  transition: border-color var(--t-base), transform var(--t-base);
  min-width: 0;
}

.template-card:hover {
  border-color: var(--border-default);
  transform: translateY(-2px);
}

.template-card-preview {
  position: relative;
  aspect-ratio: 16 / 10;
  background: #09090b;
  overflow: hidden;
  border-bottom: 1px solid var(--border-subtle);
}

.template-card:hover .thumbnail-inner {
  transform: scale(1.03) translateY(-2px);
}

.template-card-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(9, 9, 11, 0.88) 0%,
    rgba(9, 9, 11, 0.35) 50%,
    rgba(9, 9, 11, 0.15) 100%
  );
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  backdrop-filter: blur(2px);
  pointer-events: none;
}

.template-card:hover .template-card-overlay {
  opacity: 1;
  pointer-events: auto;
}

.overlay-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 11px 22px;
  background: #ffffff;
  color: #09090b;
  border: none;
  border-radius: var(--radius-pill);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.2);
  transform: translateY(6px);
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), background 0.15s, box-shadow 0.2s;
}

.template-card:hover .overlay-btn {
  transform: translateY(0);
}

.overlay-btn:hover {
  background: var(--accent-bright, #38bdf8);
  color: #000000;
  box-shadow: 0 12px 28px -4px rgba(56, 189, 248, 0.5);
}

.overlay-btn svg {
  width: 16px;
  height: 16px;
}

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
  font-weight: 500;
  letter-spacing: 0.1em;
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
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.2;
  letter-spacing: -0.015em;
}

.template-card-tagline {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.55;
  margin: 0;
}

.template-card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.template-tag {
  padding: 3px 8px;
  font-size: 11px;
  font-weight: 500;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
}

.template-card-actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.template-btn {
  padding: 9px 14px;
  font-size: 12.5px;
  flex: 1;
}

.gallery-empty {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-muted);
}

.gallery-empty svg {
  width: 40px;
  height: 40px;
  margin-bottom: 12px;
  opacity: 0.4;
}

.gallery-empty h3 {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.gallery-cta {
  padding: 40px 0 80px;
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
  font-weight: 600;
  line-height: 1.25;
  letter-spacing: -0.02em;
  margin: 12px 0 8px;
}

.cta-desc {
  font-size: 13.5px;
  color: var(--text-secondary);
  line-height: 1.65;
  max-width: 560px;
  margin: 0;
}

@media (max-width: 768px) {
  .cta-box {
    grid-template-columns: 1fr;
    padding: 28px;
  }

  .gallery-stats {
    flex-wrap: wrap;
  }

  .gallery-stat {
    flex: 1;
    min-width: 50%;
    text-align: center;
  }
}
</style>