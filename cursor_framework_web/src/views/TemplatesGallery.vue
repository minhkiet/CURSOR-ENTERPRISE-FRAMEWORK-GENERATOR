<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { templates, type Template } from '../data/templates'

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

function categoryLabel(c: string) {
  if (c === 'all') return 'Tất cả'
  return c
}
</script>

<template>
  <div class="gallery-page">
    <!-- Hero -->
    <section class="gallery-hero">
      <div class="gallery-hero-bg"></div>
      <div class="container">
        <div class="gallery-hero-content">
          <div class="gallery-badge">
            <span class="gallery-badge-dot"></span>
            <span>Landing Page Templates</span>
          </div>
          <h1 class="gallery-title">
            Bộ sưu tập <span class="text-accent">Landing Page</span><br />
            mẫu đẹp · tĩnh · tải về dùng ngay
          </h1>
          <p class="gallery-subtitle">
            6 templates HTML/CSS/JS thuần, tối ưu conversion, responsive 100%.
            Xem demo trực tiếp trong trình duyệt và tải về sử dụng ngay hôm nay.
          </p>

          <div class="gallery-stats">
            <div class="gallery-stat">
              <div class="gallery-stat-value">6</div>
              <div class="gallery-stat-label">Templates</div>
            </div>
            <div class="gallery-stat-sep"></div>
            <div class="gallery-stat">
              <div class="gallery-stat-value">~250KB</div>
              <div class="gallery-stat-label">Trung bình</div>
            </div>
            <div class="gallery-stat-sep"></div>
            <div class="gallery-stat">
              <div class="gallery-stat-value">100%</div>
              <div class="gallery-stat-label">Responsive</div>
            </div>
            <div class="gallery-stat-sep"></div>
            <div class="gallery-stat">
              <div class="gallery-stat-value">0đ</div>
              <div class="gallery-stat-label">Miễn phí</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Filter -->
    <section class="gallery-filter">
      <div class="container">
        <div class="gallery-filter-inner">
          <div class="gallery-search">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8" />
              <path d="M21 21l-4.35-4.35" />
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Tìm kiếm template..."
              aria-label="Tìm kiếm template"
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
              {{ categoryLabel(cat) }}
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Templates Grid -->
    <section class="gallery-grid-section">
      <div class="container">
        <div class="gallery-grid">
          <article
            v-for="t in filteredTemplates"
            :key="t.id"
            class="template-card"
            :style="{ '--card-accent': t.accent, '--card-accent-2': t.accentSecondary }"
          >
            <div class="template-card-preview">
              <div class="template-card-bg" :style="{ background: t.bgGradient }"></div>
              <div class="template-card-mockup">
                <div class="mockup-window">
                  <div class="mockup-bar">
                    <span></span><span></span><span></span>
                  </div>
                  <div class="mockup-body">
                    <div class="mockup-line mockup-line-lg" :style="{ background: t.accent }"></div>
                    <div class="mockup-line" :style="{ background: t.accentSecondary, opacity: 0.6 }"></div>
                    <div class="mockup-line" :style="{ background: t.accentSecondary, opacity: 0.4 }"></div>
                    <div class="mockup-blocks">
                      <div class="mockup-block" :style="{ background: t.accent, opacity: 0.3 }"></div>
                      <div class="mockup-block" :style="{ background: t.accentSecondary, opacity: 0.3 }"></div>
                      <div class="mockup-block" :style="{ background: t.accent, opacity: 0.2 }"></div>
                    </div>
                    <div class="mockup-line" :style="{ background: t.accentSecondary, opacity: 0.4 }"></div>
                    <div class="mockup-btn" :style="{ background: t.accent }"></div>
                  </div>
                </div>
              </div>
              <div class="template-card-overlay">
                <button class="overlay-btn" @click="viewTemplate(t)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                    <circle cx="12" cy="12" r="3" />
                  </svg>
                  Xem demo
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
                <button class="template-btn template-btn-primary" @click="viewTemplate(t)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                    <circle cx="12" cy="12" r="3" />
                  </svg>
                  Xem demo
                </button>
                <button class="template-btn template-btn-secondary" @click="viewTemplate(t)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3" />
                  </svg>
                  Tải về
                </button>
              </div>
            </div>
          </article>
        </div>

        <div v-if="filteredTemplates.length === 0" class="gallery-empty">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="11" cy="11" r="8" />
            <path d="M21 21l-4.35-4.35" />
          </svg>
          <h3>Không tìm thấy template nào</h3>
          <p>Thử thay đổi từ khóa hoặc chọn category khác</p>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="gallery-cta">
      <div class="container">
        <div class="cta-box">
          <div class="cta-content">
            <div class="section-label">Cần template riêng?</div>
            <h2 class="cta-title">Bạn cần một landing page riêng cho dự án của mình?</h2>
            <p class="cta-desc">
              CEF cung cấp bộ rules, skills, và agents giúp Cursor AI xây dựng landing page tùy chỉnh
              theo yêu cầu của bạn chỉ trong vài phút.
            </p>
          </div>
          <a href="#/" class="cta-btn" @click.prevent="router.push('/')">
            Khám phá Framework
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M7 17l9.2-9.2M17 17V7H7" />
            </svg>
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
  overflow: hidden;
}

.gallery-hero-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 60% 50% at 50% 0%, rgba(120, 119, 232, 0.18) 0%, transparent 60%),
    radial-gradient(ellipse 40% 30% at 80% 30%, rgba(6, 182, 212, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.gallery-hero-content {
  position: relative;
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.gallery-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  background: var(--bg-glass);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.gallery-badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-success);
  box-shadow: 0 0 8px var(--color-success);
}

.gallery-title {
  font-size: clamp(32px, 5vw, 56px);
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.03em;
  margin-bottom: 20px;
}

.gallery-subtitle {
  font-size: 17px;
  color: var(--text-secondary);
  line-height: 1.7;
  max-width: 620px;
  margin: 0 auto 40px;
}

.gallery-stats {
  display: inline-flex;
  align-items: center;
  gap: 24px;
  padding: 16px 28px;
  background: var(--bg-glass);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-xl);
  backdrop-filter: blur(12px);
}

.gallery-stat {
  text-align: center;
}

.gallery-stat-value {
  font-size: 22px;
  font-weight: 800;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}

.gallery-stat-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-top: 4px;
}

.gallery-stat-sep {
  width: 1px;
  height: 28px;
  background: var(--border-soft);
}

.gallery-filter {
  padding: 40px 0;
  position: sticky;
  top: 60px;
  z-index: 50;
  background: rgba(7, 7, 26, 0.85);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
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
  min-width: 280px;
  position: relative;
  display: flex;
  align-items: center;
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-md);
  padding: 0 14px;
  transition: border-color var(--t-base);
}

.gallery-search:focus-within {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px rgba(120, 119, 232, 0.1);
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
  font-size: 14px;
  font-family: inherit;
}

.gallery-search input::placeholder {
  color: var(--text-muted);
}

.gallery-categories {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.gallery-cat-btn {
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-full);
  transition: all var(--t-base);
  cursor: pointer;
}

.gallery-cat-btn:hover {
  color: var(--text-primary);
  border-color: var(--border-strong);
}

.gallery-cat-btn.active {
  color: #fff;
  background: var(--gradient-primary);
  border-color: transparent;
  box-shadow: 0 0 16px rgba(120, 119, 232, 0.3);
}

.gallery-grid-section {
  padding: 60px 0 100px;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 28px;
}

.template-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-xl);
  overflow: hidden;
  transition: all var(--t-base);
  display: flex;
  flex-direction: column;
}

.template-card:hover {
  border-color: var(--card-accent);
  transform: translateY(-4px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), 0 0 0 1px var(--card-accent);
}

.template-card-preview {
  position: relative;
  aspect-ratio: 16 / 10;
  overflow: hidden;
}

.template-card-bg {
  position: absolute;
  inset: 0;
  opacity: 0.9;
}

.template-card-mockup {
  position: absolute;
  inset: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mockup-window {
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  border-radius: 8px;
  overflow: hidden;
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
}

.mockup-bar {
  display: flex;
  gap: 6px;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.3);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.mockup-bar span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
}

.mockup-body {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.mockup-line {
  height: 6px;
  border-radius: 3px;
  width: 80%;
}

.mockup-line-lg {
  height: 12px;
  width: 60%;
}

.mockup-blocks {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
  margin: 6px 0;
}

.mockup-block {
  height: 28px;
  border-radius: 4px;
}

.mockup-btn {
  width: 60px;
  height: 22px;
  border-radius: 6px;
  margin-top: auto;
}

.template-card-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity var(--t-base);
}

.template-card:hover .template-card-overlay {
  opacity: 1;
}

.overlay-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.95);
  color: #07071a;
  border: none;
  border-radius: var(--radius-full);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: transform var(--t-base);
  font-family: inherit;
}

.overlay-btn:hover {
  transform: scale(1.05);
}

.overlay-btn svg {
  width: 16px;
  height: 16px;
}

.template-card-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
}

.template-card-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.template-card-category {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--card-accent);
  text-transform: uppercase;
}

.template-card-pages {
  font-size: 11px;
  color: var(--text-muted);
}

.template-card-title {
  font-size: 20px;
  font-weight: 800;
  letter-spacing: -0.01em;
  color: var(--text-primary);
  line-height: 1.2;
}

.template-card-tagline {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

.template-card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 4px;
}

.template-tag {
  padding: 4px 10px;
  font-size: 11px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-soft);
  color: var(--text-secondary);
  border-radius: var(--radius-full);
}

.template-card-actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.template-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 12px;
  font-size: 13px;
  font-weight: 700;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--t-base);
  border: 1px solid transparent;
  font-family: inherit;
}

.template-btn svg {
  width: 14px;
  height: 14px;
}

.template-btn-primary {
  background: var(--card-accent);
  color: #fff;
}

.template-btn-primary:hover {
  background: var(--card-accent-2);
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.template-btn-secondary {
  background: transparent;
  color: var(--text-primary);
  border-color: var(--border-default);
}

.template-btn-secondary:hover {
  border-color: var(--card-accent);
  color: var(--card-accent);
}

.gallery-empty {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-muted);
}

.gallery-empty svg {
  width: 48px;
  height: 48px;
  margin-bottom: 16px;
  opacity: 0.4;
}

.gallery-empty h3 {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.gallery-cta {
  padding: 80px 0;
}

.cta-box {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 40px;
  align-items: center;
  padding: 48px;
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-2xl);
  position: relative;
  overflow: hidden;
}

.cta-box::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--gradient-surface);
  pointer-events: none;
}

.cta-content {
  position: relative;
}

.cta-title {
  font-size: 28px;
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -0.02em;
  margin: 12px 0 12px;
}

.cta-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
  margin: 0;
}

.cta-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 24px;
  background: var(--gradient-primary);
  color: #fff;
  font-weight: 700;
  border-radius: var(--radius-md);
  box-shadow: 0 8px 32px rgba(120, 119, 232, 0.3);
  transition: transform var(--t-base), box-shadow var(--t-base);
}

.cta-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(120, 119, 232, 0.4);
}

.cta-btn svg {
  width: 16px;
  height: 16px;
}

@media (max-width: 768px) {
  .cta-box {
    grid-template-columns: 1fr;
    padding: 32px;
  }

  .gallery-stats {
    flex-wrap: wrap;
    gap: 16px;
  }

  .gallery-stat-sep {
    display: none;
  }
}
</style>