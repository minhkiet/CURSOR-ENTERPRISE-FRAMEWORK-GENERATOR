<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const sectionRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()

const isVisible = ref(false)

const tabs = ['Overview', 'Components', 'Rules', 'Settings']
const activeTab = ref(0)

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      isVisible.value = true
    }, { threshold: 0.05 })
  }
})
</script>

<template>
  <section class="components-section" id="components" ref="sectionRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Component Library</div>
        <h2 class="section-title">Real primitives. Ship them as-is.</h2>
        <p class="section-desc">
          Buttons, badges, inputs, cards, alerts, progress, tabs. Each component is
          accessible, keyboard-navigable, and follows a single design token system.
        </p>
      </div>

      <!-- Buttons -->
      <div class="component-group" :class="{ visible: isVisible }">
        <div class="component-head">
          <h3 class="component-title">Buttons</h3>
          <code class="component-count">6 variants</code>
        </div>
        <div class="component-row">
          <div class="comp-item">
            <button class="btn btn-primary">Primary</button>
            <span class="comp-label">btn-primary</span>
          </div>
          <div class="comp-item">
            <button class="btn btn-secondary">Secondary</button>
            <span class="comp-label">btn-secondary</span>
          </div>
          <div class="comp-item">
            <button class="btn btn-ghost">Ghost</button>
            <span class="comp-label">btn-ghost</span>
          </div>
          <div class="comp-item">
            <button class="btn btn-secondary btn-danger">Danger</button>
            <span class="comp-label">btn-danger</span>
          </div>
        </div>
        <div class="component-row">
          <div class="comp-item">
            <button class="btn btn-secondary btn-sm">Small</button>
            <span class="comp-label">Small</span>
          </div>
          <div class="comp-item">
            <button class="btn btn-primary">Medium</button>
            <span class="comp-label">Default</span>
          </div>
          <div class="comp-item">
            <button class="btn btn-secondary btn-lg">Large</button>
            <span class="comp-label">Large</span>
          </div>
          <div class="comp-item">
            <button class="btn btn-secondary btn-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 5v14M5 12h14"/></svg>
              With icon
            </button>
            <span class="comp-label">With icon</span>
          </div>
        </div>
        <div class="component-row">
          <div class="comp-item">
            <button class="btn btn-primary" disabled>Disabled</button>
            <span class="comp-label">Disabled</span>
          </div>
          <div class="comp-item">
            <button class="btn btn-secondary" disabled>Disabled</button>
            <span class="comp-label">All states</span>
          </div>
        </div>
      </div>

      <!-- Badges -->
      <div class="component-group" :class="{ visible: isVisible }">
        <div class="component-head">
          <h3 class="component-title">Badges and tags</h3>
          <code class="component-count">5 styles</code>
        </div>
        <div class="component-row">
          <div class="comp-item">
            <span class="badge badge-success">Success</span>
            <span class="comp-label">Success</span>
          </div>
          <div class="comp-item">
            <span class="badge badge-warning">Warning</span>
            <span class="comp-label">Warning</span>
          </div>
          <div class="comp-item">
            <span class="badge badge-danger">Danger</span>
            <span class="comp-label">Danger</span>
          </div>
          <div class="comp-item">
            <span class="badge badge-info">Info</span>
            <span class="comp-label">Info</span>
          </div>
          <div class="comp-item">
            <span class="badge badge-outline">Outline</span>
            <span class="comp-label">Outline</span>
          </div>
        </div>
      </div>

      <!-- Inputs -->
      <div class="component-group" :class="{ visible: isVisible }">
        <div class="component-head">
          <h3 class="component-title">Form inputs</h3>
          <code class="component-count">6 controls</code>
        </div>
        <div class="component-row component-row-wrap">
          <div class="comp-item comp-item-stack">
            <label class="input-label" for="comp-input-1">Project name</label>
            <input id="comp-input-1" type="text" class="comp-input" placeholder="crm-platform" />
            <span class="comp-label">Text input</span>
          </div>
          <div class="comp-item comp-item-stack">
            <label class="input-label" for="comp-input-2">API key</label>
            <input id="comp-input-2" type="text" class="comp-input comp-input-error" value="sk_invalid_8x2" />
            <span class="comp-error">Invalid format: must start with sk_live_</span>
            <span class="comp-label">Error state</span>
          </div>
          <div class="comp-item comp-item-stack">
            <label class="input-label" for="comp-input-3">Endpoint</label>
            <input id="comp-input-3" type="text" class="comp-input comp-input-success" value="https://api.cef.dev/v2" />
            <span class="comp-label">Success state</span>
          </div>
          <div class="comp-item comp-item-stack">
            <label class="input-label" for="comp-select-1">Framework</label>
            <select id="comp-select-1" class="comp-input comp-select">
              <option>Next.js</option>
              <option>Nuxt 3</option>
              <option>Laravel 11</option>
              <option>NestJS</option>
            </select>
            <span class="comp-label">Select</span>
          </div>
          <div class="comp-item comp-item-stack">
            <span class="input-label">Features</span>
            <div class="comp-checks">
              <label class="comp-check">
                <input type="checkbox" checked />
                <span class="comp-check-box"></span>
                <span>RLS policies</span>
              </label>
              <label class="comp-check">
                <input type="checkbox" checked />
                <span class="comp-check-box"></span>
                <span>Multi-tenant mode</span>
              </label>
              <label class="comp-check">
                <input type="checkbox" />
                <span class="comp-check-box"></span>
                <span>Audit logs</span>
              </label>
            </div>
            <span class="comp-label">Checkbox group</span>
          </div>
          <div class="comp-item comp-item-stack">
            <span class="input-label">Dark mode</span>
            <label class="comp-toggle">
              <input type="checkbox" checked />
              <span class="comp-toggle-track"></span>
              <span class="comp-toggle-label">Enabled</span>
            </label>
            <span class="comp-label">Toggle</span>
          </div>
        </div>
      </div>

      <!-- Card -->
      <div class="component-group" :class="{ visible: isVisible }">
        <div class="component-head">
          <h3 class="component-title">Card</h3>
          <code class="component-count">1 component, many surfaces</code>
        </div>
        <div class="component-row">
          <article class="demo-card">
            <header class="demo-card-head">
              <div class="demo-card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
              </div>
              <div class="demo-card-meta">
                <h4>Multi-tenant CRM</h4>
                <span>Updated 2 hours ago</span>
              </div>
              <span class="badge badge-success">Active</span>
            </header>
            <p class="demo-card-body">
              Enterprise CRM with Supabase RLS, billing integration and workflow automation.
              Pre-built adapters for Supabase, Stripe, and Resend.
            </p>
            <footer class="demo-card-foot">
              <div class="demo-card-tags">
                <span>12 components</span>
                <span>8 rules</span>
                <span>3 domains</span>
              </div>
              <div class="demo-card-actions">
                <button class="btn btn-ghost btn-sm">View</button>
                <button class="btn btn-primary btn-sm">Edit</button>
              </div>
            </footer>
          </article>
        </div>
      </div>

      <!-- Alerts -->
      <div class="component-group" :class="{ visible: isVisible }">
        <div class="component-head">
          <h3 class="component-title">Alerts and toasts</h3>
          <code class="component-count">3 variants</code>
        </div>
        <div class="component-row component-row-stack">
          <div class="alert alert-success">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="20 6 9 17 4 12"/></svg>
            <div>
              <strong>Deployment successful</strong>
              <span>Application deployed to Cloudflare Workers in 12s.</span>
            </div>
          </div>
          <div class="alert alert-warning">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            <div>
              <strong>Approaching rate limit</strong>
              <span>API usage at 85% of monthly quota.</span>
            </div>
          </div>
          <div class="alert alert-danger">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
            <div>
              <strong>Connection failed</strong>
              <span>Unable to reach Supabase instance. Retrying in 4s.</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Progress / Skeleton -->
      <div class="component-group" :class="{ visible: isVisible }">
        <div class="component-head">
          <h3 class="component-title">Progress and skeletons</h3>
          <code class="component-count">3 patterns</code>
        </div>
        <div class="component-row">
          <div class="comp-item comp-item-stack">
            <div class="progress">
              <div class="progress-label">
                <span>Knowledge indexed</span>
                <span class="progress-value">78%</span>
              </div>
              <div class="progress-track">
                <div class="progress-fill" style="width: 78%"></div>
              </div>
            </div>
            <span class="comp-label">Progress bar</span>
          </div>
          <div class="comp-item comp-item-stack">
            <div class="skel-stack">
              <div class="skel-line skel-line-lg"></div>
              <div class="skel-line"></div>
              <div class="skel-line skel-line-sm"></div>
            </div>
            <span class="comp-label">Skeleton loader</span>
          </div>
          <div class="comp-item comp-item-stack">
            <div class="spinner-group">
              <span class="spinner"></span>
              <span class="spinner spinner-sm"></span>
              <span class="spinner-text">Loading agents…</span>
            </div>
            <span class="comp-label">Spinners</span>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="component-group" :class="{ visible: isVisible }">
        <div class="component-head">
          <h3 class="component-title">Tab navigation</h3>
          <code class="component-count">underlined</code>
        </div>
        <div class="tabs">
          <div class="tabs-nav">
            <button
              v-for="(tab, index) in tabs"
              :key="tab"
              class="tabs-btn"
              :class="{ active: activeTab === index }"
              @click="activeTab = index"
            >
              {{ tab }}
            </button>
          </div>
          <div class="tabs-panel">
            <p>
              The <strong>{{ tabs[activeTab] }}</strong> tab content. Switch between
              tabs to see how state preserves without any animation flicker or layout shift.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.components-section {
  padding: var(--section-py) 0;
  border-top: 1px solid var(--border-hairline);
}

.component-group {
  margin-bottom: 12px;
  padding: 32px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  background: var(--bg-surface);
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 500ms var(--ease-out-quart), transform 500ms var(--ease-out-quart), border-color var(--t-base);
}

.component-group.visible {
  opacity: 1;
  transform: translateY(0);
}

.component-group:hover {
  border-color: var(--border-default);
}

.component-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 20px;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--border-hairline);
}

.component-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.component-count {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
  padding: 3px 8px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
}

.component-row {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 16px;
}

.component-row:last-child {
  margin-bottom: 0;
}

.component-row-wrap {
  flex-wrap: wrap;
  align-items: flex-start;
  gap: 32px 28px;
}

.component-row-stack {
  flex-direction: column;
  align-items: stretch;
}

.comp-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
  min-width: 120px;
}

.comp-item-stack {
  flex: 1 1 200px;
  max-width: 240px;
}

.comp-label {
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: var(--text-tertiary);
}

.btn-danger {
  color: var(--color-danger);
  border-color: rgba(248, 113, 113, 0.3);
}

.btn-danger:hover {
  background: rgba(248, 113, 113, 0.08);
  border-color: rgba(248, 113, 113, 0.5);
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.btn-lg {
  padding: 12px 20px;
  font-size: 14px;
}

.btn-icon {
  gap: 6px;
}

/* Badges */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 8px;
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
  border-radius: var(--radius-sm);
  border: 1px solid;
}

.badge-success {
  color: var(--color-success);
  background: rgba(52, 211, 153, 0.08);
  border-color: rgba(52, 211, 153, 0.3);
}

.badge-warning {
  color: var(--color-warning);
  background: rgba(251, 191, 36, 0.08);
  border-color: rgba(251, 191, 36, 0.3);
}

.badge-danger {
  color: var(--color-danger);
  background: rgba(248, 113, 113, 0.08);
  border-color: rgba(248, 113, 113, 0.3);
}

.badge-info {
  color: var(--color-info);
  background: rgba(96, 165, 250, 0.08);
  border-color: rgba(96, 165, 250, 0.3);
}

.badge-outline {
  color: var(--text-secondary);
  background: transparent;
  border-color: var(--border-default);
}

/* Inputs */
.input-label {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
  color: var(--text-tertiary);
}

.comp-input {
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--text-primary);
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: 9px 12px;
  outline: none;
  transition: border-color var(--t-fast), box-shadow var(--t-fast);
  width: 100%;
}

.comp-input::placeholder {
  color: var(--text-muted);
}

.comp-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.12);
}

.comp-input-error {
  border-color: rgba(248, 113, 113, 0.5);
}

.comp-input-error:focus {
  border-color: var(--color-danger);
  box-shadow: 0 0 0 3px rgba(248, 113, 113, 0.12);
}

.comp-input-success {
  border-color: rgba(52, 211, 153, 0.5);
}

.comp-error {
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: var(--color-danger);
}

.comp-select {
  appearance: none;
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23a1a1aa' stroke-width='1.5'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 32px;
}

/* Checkbox */
.comp-checks {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.comp-check {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-size: 13px;
  color: var(--text-secondary);
}

.comp-check input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.comp-check-box {
  width: 16px;
  height: 16px;
  border: 1px solid var(--border-default);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--t-fast);
  flex-shrink: 0;
  background: var(--bg-elevated);
}

.comp-check input:checked + .comp-check-box {
  background: var(--accent);
  border-color: var(--accent);
}

.comp-check input:checked + .comp-check-box::after {
  content: '';
  width: 8px;
  height: 4px;
  border: 1.5px solid var(--bg-canvas);
  border-top: 0;
  border-right: 0;
  transform: rotate(-45deg) translateY(-1px);
}

.comp-check input:focus-visible + .comp-check-box {
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
}

/* Toggle */
.comp-toggle {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
}

.comp-toggle input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.comp-toggle-track {
  width: 36px;
  height: 20px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-pill);
  position: relative;
  cursor: pointer;
  transition: all var(--t-fast);
  flex-shrink: 0;
}

.comp-toggle-track::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--text-tertiary);
  transition: all var(--t-base);
}

.comp-toggle input:checked + .comp-toggle-track {
  background: rgba(16, 185, 129, 0.2);
  border-color: var(--accent-line);
}

.comp-toggle input:checked + .comp-toggle-track::after {
  left: 18px;
  background: var(--accent);
}

.comp-toggle-label {
  font-size: 12.5px;
  color: var(--text-secondary);
}

/* Card */
.demo-card {
  width: 100%;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
  max-width: 540px;
  transition: border-color var(--t-base);
}

.demo-card:hover {
  border-color: var(--accent-line);
}

.demo-card-head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-hairline);
}

.demo-card-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: var(--accent-dim);
  border: 1px solid var(--accent-line);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  flex-shrink: 0;
}

.demo-card-icon svg {
  width: 18px;
  height: 18px;
}

.demo-card-meta {
  flex: 1;
  min-width: 0;
}

.demo-card-meta h4 {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 2px;
  letter-spacing: -0.01em;
}

.demo-card-meta span {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
}

.demo-card-body {
  padding: 16px 20px;
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.demo-card-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.02);
  border-top: 1px solid var(--border-hairline);
}

.demo-card-tags {
  display: flex;
  gap: 12px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
}

.demo-card-actions {
  display: flex;
  gap: 6px;
}

/* Alert */
.alert {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  border-radius: var(--radius-md);
  border: 1px solid;
}

.alert svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  margin-top: 1px;
}

.alert > div {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.alert strong {
  font-size: 12.5px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.alert span {
  font-size: 12px;
  color: var(--text-secondary);
}

.alert-success {
  background: rgba(52, 211, 153, 0.05);
  border-color: rgba(52, 211, 153, 0.25);
}

.alert-success svg {
  color: var(--color-success);
}

.alert-warning {
  background: rgba(251, 191, 36, 0.05);
  border-color: rgba(251, 191, 36, 0.25);
}

.alert-warning svg {
  color: var(--color-warning);
}

.alert-danger {
  background: rgba(248, 113, 113, 0.05);
  border-color: rgba(248, 113, 113, 0.25);
}

.alert-danger svg {
  color: var(--color-danger);
}

/* Progress */
.progress {
  width: 100%;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 11px;
  margin-bottom: 8px;
  color: var(--text-secondary);
}

.progress-value {
  color: var(--accent);
  font-weight: 500;
}

.progress-track {
  width: 100%;
  height: 4px;
  background: var(--bg-elevated);
  border-radius: var(--radius-pill);
  overflow: hidden;
  border: 1px solid var(--border-subtle);
}

.progress-fill {
  height: 100%;
  background: var(--accent);
  border-radius: var(--radius-pill);
  transition: width 800ms var(--ease-out-quart);
}

/* Skeleton */
.skel-stack {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
}

.skel-line {
  height: 10px;
  background: linear-gradient(90deg, var(--bg-elevated) 25%, var(--bg-raised) 50%, var(--bg-elevated) 75%);
  background-size: 200% 100%;
  border-radius: var(--radius-sm);
  animation: shimmer 1.5s linear infinite;
}

.skel-line-lg {
  height: 14px;
  width: 80%;
}

.skel-line-sm {
  width: 50%;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Spinner */
.spinner-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid var(--border-default);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

.spinner-sm {
  width: 11px;
  height: 11px;
  border-width: 1.5px;
}

.spinner-text {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Tabs */
.tabs {
  width: 100%;
}

.tabs-nav {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid var(--border-default);
  margin-bottom: 16px;
}

.tabs-btn {
  font-family: var(--font-sans);
  font-size: 12.5px;
  font-weight: 500;
  color: var(--text-secondary);
  padding: 10px 12px;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  background: transparent;
  border-radius: 0;
  transition: all var(--t-fast);
  cursor: pointer;
}

.tabs-btn:hover {
  color: var(--text-primary);
}

.tabs-btn.active {
  color: var(--text-primary);
  border-bottom-color: var(--accent);
}

.tabs-panel p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.7;
  max-width: 56ch;
}

.tabs-panel strong {
  color: var(--text-primary);
  font-weight: 600;
}

@media (prefers-reduced-motion: reduce) {
  .skel-line,
  .spinner,
  .progress-fill {
    animation: none !important;
  }
}
</style>