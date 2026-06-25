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
    }, { threshold: 0.1 })
  }
})
</script>

<template>
  <section class="components-section" id="components" ref="sectionRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">UI Components</div>
        <h2 class="section-title">Component Showcase</h2>
        <p class="section-desc">
          Preview các UI components được sử dụng trong framework. Mỗi component được
          thiết kế theo nguyên tắc atomic design, có đầy đủ states và accessibility.
        </p>
      </div>

      <!-- Buttons -->
      <div class="component-group" :class="{ visible: isVisible }">
        <h3 class="component-group-title">Buttons</h3>
        <div class="component-row">
          <div class="comp-item">
            <button class="cef-btn cef-btn-primary">Primary Button</button>
            <span class="comp-label">Primary</span>
          </div>
          <div class="comp-item">
            <button class="cef-btn cef-btn-secondary">Secondary Button</button>
            <span class="comp-label">Secondary</span>
          </div>
          <div class="comp-item">
            <button class="cef-btn cef-btn-ghost">Ghost Button</button>
            <span class="comp-label">Ghost</span>
          </div>
          <div class="comp-item">
            <button class="cef-btn cef-btn-danger">Danger Button</button>
            <span class="comp-label">Danger</span>
          </div>
        </div>
        <div class="component-row">
          <div class="comp-item">
            <button class="cef-btn cef-btn-primary cef-btn-sm">Small</button>
            <span class="comp-label">Size: Small</span>
          </div>
          <div class="comp-item">
            <button class="cef-btn cef-btn-primary">Medium</button>
            <span class="comp-label">Size: Medium</span>
          </div>
          <div class="comp-item">
            <button class="cef-btn cef-btn-primary cef-btn-lg">Large Button</button>
            <span class="comp-label">Size: Large</span>
          </div>
          <div class="comp-item">
            <button class="cef-btn cef-btn-primary cef-btn-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>
              Icon
            </button>
            <span class="comp-label">With Icon</span>
          </div>
        </div>
        <div class="component-row">
          <div class="comp-item">
            <button class="cef-btn cef-btn-primary cef-btn-loading">
              <span class="cef-spinner"></span>
              Loading...
            </button>
            <span class="comp-label">Loading State</span>
          </div>
          <div class="comp-item">
            <button class="cef-btn cef-btn-primary" disabled>Disabled</button>
            <span class="comp-label">Disabled</span>
          </div>
        </div>
      </div>

      <!-- Badges -->
      <div class="component-group" :class="{ visible: isVisible }">
        <h3 class="component-group-title">Badges & Tags</h3>
        <div class="component-row">
          <div class="comp-item">
            <div class="cef-badge cef-badge-success">Success</div>
            <span class="comp-label">Success</span>
          </div>
          <div class="comp-item">
            <div class="cef-badge cef-badge-warning">Warning</div>
            <span class="comp-label">Warning</span>
          </div>
          <div class="comp-item">
            <div class="cef-badge cef-badge-danger">Danger</div>
            <span class="comp-label">Danger</span>
          </div>
          <div class="comp-item">
            <div class="cef-badge cef-badge-info">Info</div>
            <span class="comp-label">Info</span>
          </div>
          <div class="comp-item">
            <div class="cef-badge cef-badge-purple">Purple</div>
            <span class="comp-label">Purple</span>
          </div>
          <div class="comp-item">
            <div class="cef-badge cef-badge-outline">Outline</div>
            <span class="comp-label">Outline</span>
          </div>
        </div>
      </div>

      <!-- Inputs -->
      <div class="component-group" :class="{ visible: isVisible }">
        <h3 class="component-group-title">Form Inputs</h3>
        <div class="component-row">
          <div class="comp-item">
            <div class="cef-input-group">
              <input type="text" class="cef-input" placeholder="Enter project name..." />
            </div>
            <span class="comp-label">Text Input</span>
          </div>
          <div class="comp-item">
            <div class="cef-input-group">
              <input type="text" class="cef-input cef-input-error" value="Invalid value" />
              <span class="cef-error-text">This field is required</span>
            </div>
            <span class="comp-label">Error State</span>
          </div>
          <div class="comp-item">
            <div class="cef-input-group">
              <input type="text" class="cef-input cef-input-success" value="Validated input" />
            </div>
            <span class="comp-label">Success State</span>
          </div>
          <div class="comp-item">
            <div class="cef-input-group" style="position: relative;">
              <input type="text" class="cef-input" placeholder="Search..." />
              <button class="cef-input-action">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
              </button>
            </div>
            <span class="comp-label">With Action</span>
          </div>
        </div>
        <div class="component-row">
          <div class="comp-item">
            <div class="cef-input-group">
              <label class="cef-label">Select Framework</label>
              <select class="cef-select">
                <option>Next.js</option>
                <option>Vue / Nuxt</option>
                <option>Laravel</option>
                <option>ASP.NET Core</option>
              </select>
            </div>
            <span class="comp-label">Select</span>
          </div>
          <div class="comp-item">
            <div class="cef-checkbox-group">
              <label class="cef-checkbox">
                <input type="checkbox" checked />
                <span class="cef-checkbox-box"></span>
                <span>Enable RLS</span>
              </label>
              <label class="cef-checkbox">
                <input type="checkbox" />
                <span class="cef-checkbox-box"></span>
                <span>Multi-tenant mode</span>
              </label>
            </div>
            <span class="comp-label">Checkbox</span>
          </div>
          <div class="comp-item">
            <div class="cef-toggle-group">
              <span class="cef-label">Dark Mode</span>
              <label class="cef-toggle">
                <input type="checkbox" checked />
                <span class="cef-toggle-track"></span>
              </label>
            </div>
            <span class="comp-label">Toggle</span>
          </div>
        </div>
      </div>

      <!-- Cards -->
      <div class="component-group" :class="{ visible: isVisible }">
        <h3 class="component-group-title">Cards</h3>
        <div class="component-row">
          <div class="comp-item" style="width: 100%;">
            <div class="cef-card">
              <div class="cef-card-header">
                <div class="cef-card-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                  </svg>
                </div>
                <div>
                  <h4>Multi-Tenant CRM</h4>
                  <span>Last updated 2 hours ago</span>
                </div>
                <div class="cef-badge cef-badge-success cef-card-badge">Active</div>
              </div>
              <p class="cef-card-desc">Enterprise-grade multi-tenant CRM với Supabase RLS, billing integration và workflow automation.</p>
              <div class="cef-card-footer">
                <div class="cef-card-meta">
                  <span>12 components</span>
                  <span>8 rules</span>
                  <span>3 domains</span>
                </div>
                <div class="cef-card-actions">
                  <button class="cef-btn cef-btn-ghost cef-btn-sm">View</button>
                  <button class="cef-btn cef-btn-primary cef-btn-sm">Edit</button>
                </div>
              </div>
            </div>
            <span class="comp-label">Project Card</span>
          </div>
        </div>
      </div>

      <!-- Alerts & Toasts -->
      <div class="component-group" :class="{ visible: isVisible }">
        <h3 class="component-group-title">Alerts & Toasts</h3>
        <div class="component-row">
          <div class="comp-item">
            <div class="cef-alert cef-alert-success">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
              <div>
                <strong>Deployment successful</strong>
                <span>Application deployed to Cloudflare Workers in 12s</span>
              </div>
            </div>
            <span class="comp-label">Success Alert</span>
          </div>
          <div class="comp-item">
            <div class="cef-alert cef-alert-warning">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
              <div>
                <strong>Approaching rate limit</strong>
                <span>API usage at 85% of monthly quota</span>
              </div>
            </div>
            <span class="comp-label">Warning Alert</span>
          </div>
          <div class="comp-item">
            <div class="cef-alert cef-alert-error">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
              <div>
                <strong>Connection failed</strong>
                <span>Unable to reach Supabase instance. Retrying...</span>
              </div>
            </div>
            <span class="comp-label">Error Alert</span>
          </div>
        </div>
      </div>

      <!-- Progress & Loading -->
      <div class="component-group" :class="{ visible: isVisible }">
        <h3 class="component-group-title">Progress & Loading</h3>
        <div class="component-row">
          <div class="comp-item">
            <div class="cef-progress">
              <div class="cef-progress-label">
                <span>Knowledge indexed</span>
                <span>78%</span>
              </div>
              <div class="cef-progress-track">
                <div class="cef-progress-fill" style="width: 78%"></div>
              </div>
            </div>
            <span class="comp-label">Progress Bar</span>
          </div>
          <div class="comp-item">
            <div class="cef-skeleton" style="width: 200px; height: 14px;"></div>
            <div class="cef-skeleton" style="width: 150px; height: 10px; margin-top: 8px;"></div>
            <div class="cef-skeleton" style="width: 230px; height: 10px; margin-top: 6px;"></div>
            <span class="comp-label">Skeleton Loader</span>
          </div>
          <div class="comp-item">
            <div class="cef-spinners">
              <div class="cef-spinner"></div>
              <div class="cef-spinner cef-spinner-lg"></div>
            </div>
            <span class="comp-label">Spinners</span>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="component-group" :class="{ visible: isVisible }">
        <h3 class="component-group-title">Tabs</h3>
        <div class="component-row">
          <div class="comp-item" style="width: 100%;">
            <div class="cef-tabs-nav">
              <button
                v-for="(tab, index) in tabs"
                :key="tab"
                class="cef-tab-btn"
                :class="{ active: activeTab === index }"
                @click="activeTab = index"
              >
                {{ tab }}
              </button>
            </div>
            <div class="cef-tabs-panel">
              <p>This is the overview tab content. It displays the main information about the selected section with a clean, readable layout.</p>
            </div>
            <span class="comp-label">Tab Navigation</span>
          </div>
        </div>
      </div>

      <!-- Extras -->
      <div class="component-group" :class="{ visible: isVisible }">
        <h3 class="component-group-title">Extras</h3>
        <div class="component-row">
          <div class="comp-item">
            <div class="cef-avatars">
              <div class="cef-avatar" style="background: linear-gradient(135deg, #7878e8, #a78bfa);">A</div>
              <div class="cef-avatar" style="background: linear-gradient(135deg, #06b6d4, #818cf8);">T</div>
              <div class="cef-avatar cef-avatar-sm">+3</div>
            </div>
            <span class="comp-label">Avatar Stack</span>
          </div>
          <div class="comp-item">
            <div class="cef-breadcrumb">
              <a href="#">Projects</a>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
              <a href="#">CRM</a>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
              <span>Components</span>
            </div>
            <span class="comp-label">Breadcrumb</span>
          </div>
          <div class="comp-item">
            <div class="cef-pagination">
              <button class="cef-page-btn" disabled>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
              </button>
              <button class="cef-page-btn active">1</button>
              <button class="cef-page-btn">2</button>
              <button class="cef-page-btn">3</button>
              <span class="cef-page-ellipsis">...</span>
              <button class="cef-page-btn">12</button>
              <button class="cef-page-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
              </button>
            </div>
            <span class="comp-label">Pagination</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.components-section {
  padding: var(--section-py) 0;
  background: linear-gradient(180deg, transparent 0%, rgba(120, 119, 232, 0.015) 50%, transparent 100%);
}

.component-group {
  margin-top: 48px;
  padding: 36px;
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-subtle);
  background: rgba(255, 255, 255, 0.01);
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s var(--ease-out), transform 0.5s var(--ease-out);
}

.component-group.visible {
  opacity: 1;
  transform: translateY(0);
}

.component-group:nth-child(2) { transition-delay: 0.05s; }
.component-group:nth-child(3) { transition-delay: 0.1s; }
.component-group:nth-child(4) { transition-delay: 0.15s; }
.component-group:nth-child(5) { transition-delay: 0.2s; }
.component-group:nth-child(6) { transition-delay: 0.25s; }
.component-group:nth-child(7) { transition-delay: 0.3s; }
.component-group:nth-child(8) { transition-delay: 0.35s; }
.component-group:nth-child(9) { transition-delay: 0.4s; }

.component-group-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-subtle);
  letter-spacing: 0.02em;
}

.component-row {
  display: flex;
  align-items: flex-end;
  gap: 16px;
  flex-wrap: wrap;
}

.comp-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.comp-label {
  font-size: 10px;
  color: var(--text-muted);
  text-align: center;
}

/* Buttons */
.cef-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-family: var(--font-sans);
  font-weight: 600;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--t-base);
  border: 1px solid transparent;
  white-space: nowrap;
  letter-spacing: 0.01em;
}

.cef-btn svg { width: 14px; height: 14px; flex-shrink: 0; }

.cef-btn-primary {
  color: #fff;
  background: var(--gradient-primary);
  border-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 20px rgba(120, 119, 232, 0.18);
  padding: 10px 18px;
  font-size: 13px;
}

.cef-btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 28px rgba(120, 119, 232, 0.3);
  opacity: 0.92;
}

.cef-btn-primary:active { transform: translateY(0); }

.cef-btn-secondary {
  color: var(--text-primary);
  background: var(--bg-elevated);
  border-color: var(--border-default);
  padding: 10px 18px;
  font-size: 13px;
}

.cef-btn-secondary:hover {
  border-color: var(--border-strong);
  background: rgba(255, 255, 255, 0.06);
}

.cef-btn-ghost {
  color: var(--text-secondary);
  background: transparent;
  border-color: var(--border-default);
  padding: 10px 18px;
  font-size: 13px;
}

.cef-btn-ghost:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.04);
  border-color: var(--border-strong);
}

.cef-btn-danger {
  color: #fff;
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
  border-color: rgba(248, 113, 113, 0.2);
  padding: 10px 18px;
  font-size: 13px;
  box-shadow: 0 0 20px rgba(248, 113, 113, 0.18);
}

.cef-btn-danger:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 28px rgba(248, 113, 113, 0.3);
}

.cef-btn-sm { padding: 6px 12px; font-size: 11px; }
.cef-btn-lg { padding: 13px 24px; font-size: 15px; }
.cef-btn-icon { gap: 7px; }
.cef-btn-loading { pointer-events: none; opacity: 0.8; }

.cef-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

.cef-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  flex-shrink: 0;
}

.cef-spinner-lg { width: 20px; height: 20px; border-width: 2.5px; }

@keyframes spin { to { transform: rotate(360deg); } }

/* Badges */
.cef-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 10.5px;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: var(--radius-full);
  white-space: nowrap;
  letter-spacing: 0.02em;
}

.cef-badge-success { color: var(--color-success); background: rgba(52, 211, 153, 0.1); border: 1px solid rgba(52, 211, 153, 0.2); }
.cef-badge-warning { color: var(--color-warning); background: rgba(251, 191, 36, 0.1); border: 1px solid rgba(251, 191, 36, 0.2); }
.cef-badge-danger { color: var(--color-danger); background: rgba(248, 113, 113, 0.1); border: 1px solid rgba(248, 113, 113, 0.2); }
.cef-badge-info { color: var(--color-info); background: rgba(96, 165, 250, 0.1); border: 1px solid rgba(96, 165, 250, 0.2); }
.cef-badge-purple { color: var(--accent-secondary); background: rgba(167, 139, 250, 0.1); border: 1px solid rgba(167, 139, 250, 0.2); }
.cef-badge-outline { color: var(--text-secondary); background: transparent; border: 1px solid var(--border-default); }

/* Inputs */
.cef-input-group { display: flex; flex-direction: column; gap: 6px; }

.cef-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  letter-spacing: 0.03em;
}

.cef-input {
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--text-primary);
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: 9px 13px;
  outline: none;
  transition: border-color var(--t-fast), box-shadow var(--t-fast);
  width: 200px;
}

.cef-input::placeholder { color: var(--text-muted); }
.cef-input:focus { border-color: rgba(120, 119, 232, 0.5); box-shadow: 0 0 0 3px rgba(120, 119, 232, 0.08); }
.cef-input-error { border-color: rgba(248, 113, 113, 0.5); box-shadow: 0 0 0 3px rgba(248, 113, 113, 0.06); }
.cef-input-success { border-color: rgba(52, 211, 153, 0.5); box-shadow: 0 0 0 3px rgba(52, 211, 153, 0.06); }
.cef-error-text { font-size: 10px; color: var(--color-danger); }

.cef-input-action {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-xs);
  color: var(--text-muted);
  transition: color var(--t-fast);
}

.cef-input-action:hover { color: var(--text-primary); }
.cef-input-action svg { width: 13px; height: 13px; }

.cef-select {
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--text-primary);
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: 9px 32px 9px 13px;
  outline: none;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2350506e' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  transition: border-color var(--t-fast);
  width: 200px;
}

.cef-select:focus { border-color: rgba(120, 119, 232, 0.5); }

/* Checkbox */
.cef-checkbox-group { display: flex; flex-direction: column; gap: 8px; }

.cef-checkbox {
  display: flex;
  align-items: center;
  gap: 9px;
  cursor: pointer;
  font-size: 13px;
  color: var(--text-secondary);
}

.cef-checkbox input { display: none; }

.cef-checkbox-box {
  width: 16px;
  height: 16px;
  border: 1.5px solid var(--border-strong);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--t-fast);
  flex-shrink: 0;
}

.cef-checkbox input:checked + .cef-checkbox-box {
  background: var(--gradient-primary);
  border-color: transparent;
}

.cef-checkbox input:checked + .cef-checkbox-box::after {
  content: '';
  width: 9px;
  height: 5px;
  border: 2px solid #fff;
  border-top: none;
  border-right: none;
  transform: rotate(-45deg) translateY(-1px);
}

/* Toggle */
.cef-toggle-group { display: flex; align-items: center; gap: 10px; }

.cef-toggle { position: relative; }
.cef-toggle input { display: none; }

.cef-toggle-track {
  display: block;
  width: 38px;
  height: 20px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-full);
  position: relative;
  cursor: pointer;
  transition: background var(--t-fast), border-color var(--t-fast);
}

.cef-toggle-track::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--text-muted);
  transition: all var(--ease-spring);
}

.cef-toggle input:checked + .cef-toggle-track {
  background: rgba(120, 119, 232, 0.2);
  border-color: rgba(120, 119, 232, 0.3);
}

.cef-toggle input:checked + .cef-toggle-track::after {
  left: 20px;
  background: var(--accent-primary);
  box-shadow: 0 0 8px rgba(120, 119, 232, 0.5);
}

/* Card */
.cef-card {
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-soft);
  background: var(--bg-surface);
  overflow: hidden;
  transition: border-color var(--t-base), box-shadow var(--t-base);
  max-width: 480px;
}

.cef-card:hover {
  border-color: var(--border-accent);
  box-shadow: var(--shadow-glow);
}

.cef-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 18px;
  border-bottom: 1px solid var(--border-subtle);
}

.cef-card-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: var(--accent-glow);
  border: 1px solid var(--border-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.cef-card-icon svg { width: 17px; height: 17px; stroke: var(--accent-primary); }

.cef-card-header > div:nth-child(2) { flex: 1; min-width: 0; }
.cef-card-header h4 { font-size: 13px; font-weight: 600; color: var(--text-primary); margin-bottom: 2px; }
.cef-card-header span { font-size: 11px; color: var(--text-muted); }
.cef-card-badge { flex-shrink: 0; }

.cef-card-desc {
  padding: 14px 18px;
  font-size: 12.5px;
  color: var(--text-secondary);
  line-height: 1.65;
}

.cef-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px;
  border-top: 1px solid var(--border-subtle);
  background: rgba(255, 255, 255, 0.01);
}

.cef-card-meta { display: flex; gap: 10px; font-size: 11px; color: var(--text-muted); }
.cef-card-actions { display: flex; gap: 6px; }

/* Alerts */
.cef-alert {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px;
  border-radius: var(--radius-md);
  max-width: 300px;
}

.cef-alert svg { width: 16px; height: 16px; flex-shrink: 0; margin-top: 1px; }
.cef-alert div { display: flex; flex-direction: column; gap: 2px; }
.cef-alert strong { font-size: 12px; font-weight: 600; color: var(--text-primary); }
.cef-alert span { font-size: 11px; color: var(--text-secondary); }

.cef-alert-success { background: rgba(52, 211, 153, 0.08); border: 1px solid rgba(52, 211, 153, 0.2); }
.cef-alert-success svg { stroke: var(--color-success); }

.cef-alert-warning { background: rgba(251, 191, 36, 0.08); border: 1px solid rgba(251, 191, 36, 0.2); }
.cef-alert-warning svg { stroke: var(--color-warning); }

.cef-alert-error { background: rgba(248, 113, 113, 0.08); border: 1px solid rgba(248, 113, 113, 0.2); }
.cef-alert-error svg { stroke: var(--color-danger); }

/* Progress */
.cef-progress { width: 100%; max-width: 240px; }

.cef-progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  margin-bottom: 7px;
}

.cef-progress-label span:first-child { color: var(--text-secondary); font-weight: 500; }
.cef-progress-label span:last-child { color: var(--accent-primary); font-weight: 700; }

.cef-progress-track {
  width: 100%;
  height: 5px;
  background: var(--bg-elevated);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.cef-progress-fill {
  height: 100%;
  background: var(--gradient-primary);
  border-radius: var(--radius-full);
  box-shadow: 0 0 8px rgba(120, 119, 232, 0.4);
}

/* Skeleton */
.cef-skeleton {
  background: linear-gradient(90deg, var(--bg-elevated) 25%, rgba(255, 255, 255, 0.04) 50%, var(--bg-elevated) 75%);
  background-size: 200% 100%;
  border-radius: var(--radius-sm);
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.cef-spinners { display: flex; align-items: center; gap: 10px; }

/* Tabs */
.cef-tabs-nav {
  display: flex;
  border-bottom: 1px solid var(--border-default);
  gap: 0;
  margin-bottom: 20px;
}

.cef-tab-btn {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  padding: 9px 14px;
  border-bottom: 2px solid transparent;
  transition: all var(--t-fast);
  margin-bottom: -1px;
}

.cef-tab-btn:hover { color: var(--text-primary); }
.cef-tab-btn.active { color: var(--accent-primary); border-bottom-color: var(--accent-primary); }

.cef-tabs-panel p { font-size: 13px; color: var(--text-secondary); line-height: 1.7; }

/* Extras */
.cef-avatars { display: flex; align-items: center; }

.cef-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 800;
  color: #fff;
  border: 2px solid var(--bg-base);
  margin-left: -8px;
  flex-shrink: 0;
}

.cef-avatar:first-child { margin-left: 0; }
.cef-avatar-sm { font-size: 10px; background: var(--bg-elevated); color: var(--text-secondary); }

.cef-breadcrumb {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
}

.cef-breadcrumb a { color: var(--text-secondary); transition: color var(--t-fast); }
.cef-breadcrumb a:hover { color: var(--text-primary); }
.cef-breadcrumb svg { width: 11px; height: 11px; stroke: var(--text-muted); }
.cef-breadcrumb span { color: var(--text-primary); font-weight: 500; }

.cef-pagination { display: flex; align-items: center; gap: 3px; }

.cef-page-btn {
  min-width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  border: 1px solid transparent;
  transition: all var(--t-fast);
  padding: 0 6px;
}

.cef-page-btn:hover { color: var(--text-primary); border-color: var(--border-default); }
.cef-page-btn.active { color: #fff; background: var(--gradient-primary); border-color: transparent; }
.cef-page-btn:disabled { opacity: 0.3; cursor: not-allowed; }
.cef-page-btn svg { width: 13px; height: 13px; }
.cef-page-ellipsis { color: var(--text-muted); padding: 0 4px; }
</style>
