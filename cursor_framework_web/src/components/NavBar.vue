<script setup lang="ts">
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useTheme, type ThemeName } from '../composables/useTheme'

const route = useRoute()
const router = useRouter()

const { currentTheme, themes, applyTheme, initTheme } = useTheme()
const isThemeDropdownOpen = ref(false)

const isScrolled = ref(false)
const isMobileMenuOpen = ref(false)
const isMobileMode = ref(false)

const isSubpage = computed(() => route.path !== '/')

const navLinks = [
  { to: '/learn', label: 'Thư Viện', kind: 'route' },
  { href: '#explorer', label: 'Explorer', kind: 'anchor' },
  { href: '#architecture', label: 'Kiến Trúc', kind: 'anchor' },
  { to: '/prompts', label: 'Prompts', kind: 'route', badge: 'Hot' },
  { to: '/templates', label: 'Templates', kind: 'route', badge: '27+' },
  { to: '/cms', label: 'CMS Quản Trị', kind: 'route' }
] as const

const quickCommands = [
  { cmd: '/ui-ux', title: 'UI/UX System', desc: 'Design Tokens & Wireframe' },
  { cmd: '/dashboard-ui', title: 'Dashboard Pro', desc: 'Cockpit Analytics & Table' },
  { cmd: '/frontend-taste', title: 'Frontend Taste', desc: 'Anti-Slop 57 Gates' },
  { cmd: '/cms-landing-enterprise', title: 'CMS Enterprise', desc: 'Full SaaS v4 & Ví' },
  { cmd: '/image-workflow', title: 'Image Workflow', desc: 'AI Asset Studio & Cloner' }
] as const

const copiedCommand = ref<string | null>(null)

function copyCommand(cmd: string) {
  navigator.clipboard.writeText(cmd)
  copiedCommand.value = cmd
  setTimeout(() => {
    copiedCommand.value = null
  }, 2200)
}

function handleScroll() {
  isScrolled.value = window.scrollY > 8
}

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
  document.body.style.overflow = isMobileMenuOpen.value ? 'hidden' : ''
}

function closeMobileMenu() {
  isMobileMenuOpen.value = false
  document.body.style.overflow = ''
}

function toggleThemeDropdown() {
  isThemeDropdownOpen.value = !isThemeDropdownOpen.value
}

function selectTheme(t: ThemeName) {
  applyTheme(t)
  isThemeDropdownOpen.value = false
}

function handleClickOutside(e: MouseEvent) {
  const target = e.target as HTMLElement
  if (!target.closest('.theme-switcher-wrapper')) {
    isThemeDropdownOpen.value = false
  }
}

async function smoothScroll(e: Event, href: string): Promise<void> {
  e.preventDefault()
  closeMobileMenu()
  if (route.path !== '/') {
    await router.push({ path: '/', hash: href })
    return
  }
  await nextTick()
  const target = document.querySelector(href)
  if (target) {
    const navbarHeight = 56
    const targetPosition = target.getBoundingClientRect().top + window.scrollY - navbarHeight
    window.scrollTo({ top: targetPosition, behavior: 'smooth' })
  }
}

function checkMobileMode() {
  isMobileMode.value = window.innerWidth < 960
  if (!isMobileMode.value && isMobileMenuOpen.value) {
    closeMobileMenu()
  }
}

onMounted(() => {
  initTheme()
  checkMobileMode()
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('resize', checkMobileMode)
  window.addEventListener('click', handleClickOutside)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', checkMobileMode)
  window.removeEventListener('click', handleClickOutside)
  document.body.style.overflow = ''
})
</script>

<template>
  <header class="navbar" :class="{ scrolled: isScrolled, 'is-subpage': isSubpage }">
    <div class="navbar-inner">
      <router-link to="/" class="navbar-logo" @click="closeMobileMenu">
        <div class="navbar-logo-mark">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 17l6-6 4 4 8-9" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M14 6h8v8" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="navbar-logo-text-group">
          <span class="navbar-logo-text">Cursor Enterprise</span>
          <span class="navbar-logo-sub">Framework 2026</span>
        </div>
        <span class="navbar-logo-tag">Anti-Slop</span>
      </router-link>

      <!-- Desktop Nav -->
      <nav v-if="!isMobileMode" class="navbar-nav">
        <template v-for="link in navLinks" :key="link.label">
          <router-link
            v-if="link.kind === 'route'"
            :to="link.to"
            class="nav-link"
            @click="closeMobileMenu"
          >
            <span>{{ link.label }}</span>
            <span v-if="'badge' in link && link.badge" class="nav-badge">{{ link.badge }}</span>
          </router-link>
          <a
            v-else
            :href="link.href"
            class="nav-link"
            @click="smoothScroll($event, link.href)"
          >
            <span>{{ link.label }}</span>
          </a>
        </template>
      </nav>

      <!-- Desktop Actions -->
      <div v-if="!isMobileMode" class="navbar-actions">
        <!-- Theme Switcher Dropdown -->
        <div class="theme-switcher-wrapper">
          <button
            class="theme-switcher-btn"
            @click.stop="toggleThemeDropdown"
            :title="'Đổi theme giao diện (Hiện tại: ' + currentTheme + ')'"
            :aria-expanded="isThemeDropdownOpen"
          >
            <span class="theme-dot" :style="{ backgroundColor: themes.find(t => t.id === currentTheme)?.accentColor }"></span>
            <span class="theme-btn-label">{{ themes.find(t => t.id === currentTheme)?.name }}</span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </button>

          <div v-if="isThemeDropdownOpen" class="theme-dropdown-menu">
            <div class="theme-dropdown-header">
              <span>Theme Giao Diện</span>
              <span class="theme-count">{{ themes.length }} themes</span>
            </div>
            <button
              v-for="t in themes"
              :key="t.id"
              class="theme-option-item"
              :class="{ active: currentTheme === t.id }"
              @click="selectTheme(t.id)"
            >
              <div class="theme-option-preview" :style="{ backgroundColor: t.bgPreview, borderColor: t.accentColor }">
                <span class="theme-option-accent" :style="{ backgroundColor: t.accentColor }"></span>
              </div>
              <div class="theme-option-info">
                <div class="theme-option-name">
                  <span>{{ t.icon }} {{ t.name }}</span>
                  <span v-if="currentTheme === t.id" class="theme-active-tag">Active</span>
                </div>
                <div class="theme-option-desc">{{ t.labelVi }} · {{ t.vibe }}</div>
              </div>
            </button>
          </div>
        </div>

        <a href="https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR" class="btn btn-ghost" target="_blank" rel="noopener">
          <svg viewBox="0 0 24 24" fill="currentColor" width="14" height="14">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
          </svg>
          <span>GitHub</span>
        </a>

        <router-link to="/install" class="btn btn-primary" title="Xem hướng dẫn cài đặt và khởi tạo Framework">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
            <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
          </svg>
          <span>Cài Đặt Ngay</span>
        </router-link>
      </div>

      <!-- Mobile Right Controls (Quick Theme Dot + Hamburger) -->
      <div v-if="isMobileMode" class="mobile-header-controls">
        <button
          class="mobile-quick-theme-btn"
          @click="toggleThemeDropdown"
          :title="'Đổi theme (' + currentTheme + ')'"
          aria-label="Đổi theme"
        >
          <span class="theme-dot" :style="{ backgroundColor: themes.find(t => t.id === currentTheme)?.accentColor }"></span>
        </button>

        <button
          class="navbar-toggle"
          @click="toggleMobileMenu"
          :aria-label="isMobileMenuOpen ? 'Đóng menu' : 'Mở menu'"
          :aria-expanded="isMobileMenuOpen"
        >
          <span :class="{ open: isMobileMenuOpen }"></span>
          <span :class="{ open: isMobileMenuOpen }"></span>
          <span :class="{ open: isMobileMenuOpen }"></span>
        </button>
      </div>
    </div>

    <!-- ─── MOBILE DRAWER & OVERLAY ─── -->
    <div
      v-if="isMobileMode && isMobileMenuOpen"
      class="mobile-backdrop"
      @click="closeMobileMenu"
      aria-hidden="true"
    ></div>

    <div
      v-if="isMobileMode"
      class="mobile-drawer"
      :class="{ open: isMobileMenuOpen }"
      role="dialog"
      aria-modal="true"
      aria-label="Menu điều hướng di động"
    >
      <div class="mobile-drawer-header">
        <div class="mobile-drawer-brand">
          <div class="navbar-logo-mark">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 17l6-6 4 4 8-9" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M14 6h8v8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div>
            <div class="drawer-brand-title">Cursor Enterprise</div>
            <div class="drawer-brand-sub">Framework v5.1 · Anti-Slop</div>
          </div>
        </div>
        <button class="drawer-close-btn" @click="closeMobileMenu" aria-label="Đóng menu">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Copied Feedback Banner -->
      <transition name="fade">
        <div v-if="copiedCommand" class="copy-alert">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <span>Đã sao chép <strong>{{ copiedCommand }}</strong> vào clipboard! Dán vào Cursor ngay.</span>
        </div>
      </transition>

      <div class="mobile-drawer-scroll">
        <!-- Section: Menu Chính -->
        <div class="drawer-section">
          <div class="drawer-section-title">ĐIỀU HƯỚNG CHÍNH</div>
          <div class="drawer-nav-list">
            <router-link to="/" class="drawer-nav-item" @click="closeMobileMenu">
              <span class="drawer-nav-icon">🏠</span>
              <span>Trang Chủ</span>
            </router-link>

            <router-link to="/templates" class="drawer-nav-item" @click="closeMobileMenu">
              <span class="drawer-nav-icon">📦</span>
              <span>Kho Templates</span>
              <span class="drawer-pill-badge accent">27+ Mẫu Mới</span>
            </router-link>

            <router-link to="/cms" class="drawer-nav-item" @click="closeMobileMenu">
              <span class="drawer-nav-icon">🗂️</span>
              <span>CMS Dashboard v4</span>
              <span class="drawer-pill-badge">SaaS CRM</span>
            </router-link>

            <router-link to="/prompts" class="drawer-nav-item" @click="closeMobileMenu">
              <span class="drawer-nav-icon">⚡</span>
              <span>Kho Prompts Thực Chiến</span>
              <span class="drawer-pill-badge hot">Hot</span>
            </router-link>

            <router-link to="/learn" class="drawer-nav-item" @click="closeMobileMenu">
              <span class="drawer-nav-icon">📚</span>
              <span>Thư Viện Framework & Rules</span>
            </router-link>

            <a href="#explorer" class="drawer-nav-item" @click="smoothScroll($event, '#explorer')">
              <span class="drawer-nav-icon">🧭</span>
              <span>Cây Thư Mục Explorer</span>
            </a>

            <a href="#architecture" class="drawer-nav-item" @click="smoothScroll($event, '#architecture')">
              <span class="drawer-nav-icon">🏛️</span>
              <span>Kiến Trúc Enterprise</span>
            </a>
          </div>
        </div>

        <!-- Section: Lệnh Nhanh Cursor (Interactive One-Tap Copy) -->
        <div class="drawer-section">
          <div class="drawer-section-title">
            <span>⚡ LỆNH NHANH CURSOR (CHẠM ĐỂ CHÉP)</span>
          </div>
          <div class="quick-commands-grid">
            <button
              v-for="q in quickCommands"
              :key="q.cmd"
              class="quick-cmd-btn"
              @click="copyCommand(q.cmd)"
            >
              <div class="q-cmd-code">{{ q.cmd }}</div>
              <div class="q-cmd-desc">{{ q.desc }}</div>
            </button>
          </div>
        </div>

        <!-- Section: Theme Giao Diện -->
        <div class="drawer-section">
          <div class="drawer-section-title">
            <span>🎨 CHỌN THEME GIAO DIỆN ({{ themes.length }})</span>
          </div>
          <div class="mobile-theme-grid">
            <button
              v-for="t in themes"
              :key="t.id"
              class="mobile-theme-chip"
              :class="{ active: currentTheme === t.id }"
              @click="selectTheme(t.id)"
            >
              <span class="mobile-theme-dot" :style="{ backgroundColor: t.accentColor }"></span>
              <span class="chip-label">{{ t.name }}</span>
            </button>
          </div>
        </div>

        <!-- Section: CTAs -->
        <div class="drawer-footer-actions">
          <router-link to="/install" class="btn btn-primary btn-block" @click="closeMobileMenu">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15">
              <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
            </svg>
            <span>Cài Đặt Framework Ngay</span>
          </router-link>
          <a
            href="https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR"
            target="_blank"
            rel="noopener"
            class="btn btn-ghost btn-block"
          >
            <span>GitHub Repository</span>
          </a>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: 60px;
  background: transparent;
  border-bottom: 1px solid transparent;
  transition: background var(--t-base), border-color var(--t-base), backdrop-filter var(--t-base);
}

.navbar.scrolled,
.navbar.is-subpage {
  background: var(--bg-overlay);
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  border-bottom-color: var(--border-hairline);
}

.navbar-inner {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 0 clamp(16px, 2.5vw, 44px);
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.navbar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
  font-weight: 600;
  text-decoration: none;
}

.navbar-logo-mark {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  background: var(--accent);
  color: var(--bg-base);
  display: flex;
  align-items: center;
  justify-content: center;
}

.navbar-logo-mark svg {
  width: 16px;
  height: 16px;
  stroke-width: 2.4;
}

.navbar-logo-text-group {
  display: flex;
  flex-direction: column;
}

.navbar-logo-text {
  font-size: 13.5px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.015em;
  line-height: 1.2;
}

.navbar-logo-sub {
  font-size: 10px;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
}

.navbar-logo-tag {
  font-size: 10.5px;
  color: var(--accent);
  background: var(--accent-dim);
  border: 1px solid var(--accent-line);
  font-weight: 700;
  padding: 2px 7px;
  border-radius: var(--radius-pill);
}

.navbar-nav {
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
}

.nav-link {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  transition: color var(--t-fast), background var(--t-fast);
}

.nav-link:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.05);
}

.nav-link.router-link-active {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.08);
  font-weight: 600;
}

.nav-badge {
  font-size: 9.5px;
  font-weight: 700;
  font-family: var(--font-mono);
  background: var(--accent-dim);
  color: var(--accent);
  border: 1px solid var(--accent-line);
  padding: 1px 5px;
  border-radius: var(--radius-pill);
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: auto;
}

/* Mobile Header Controls */
.mobile-header-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}

.mobile-quick-theme-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.navbar-toggle {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 38px;
  height: 38px;
  padding: 8px;
  border-radius: var(--radius-sm);
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  cursor: pointer;
}

.navbar-toggle span {
  display: block;
  width: 100%;
  height: 1.8px;
  background: var(--text-primary);
  border-radius: 2px;
  transition: transform var(--t-fast), opacity var(--t-fast);
}

.navbar-toggle span.open:nth-child(1) {
  transform: translateY(6.8px) rotate(45deg);
}

.navbar-toggle span.open:nth-child(2) {
  opacity: 0;
}

.navbar-toggle span.open:nth-child(3) {
  transform: translateY(-6.8px) rotate(-45deg);
}

/* ─── Mobile Slide-over Drawer ─── */
.mobile-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(8px);
  z-index: 9990;
  animation: fadeIn 0.25s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.mobile-drawer {
  position: fixed;
  top: 0;
  bottom: 0;
  right: 0;
  width: min(380px, 92vw);
  background: var(--bg-overlay, #0f121a);
  backdrop-filter: blur(28px) saturate(190%);
  -webkit-backdrop-filter: blur(28px) saturate(190%);
  border-left: 1px solid var(--border-default);
  box-shadow: -12px 0 40px rgba(0, 0, 0, 0.7);
  z-index: 9999;
  display: flex;
  flex-direction: column;
  transform: translateX(100%);
  transition: transform 0.32s cubic-bezier(0.16, 1, 0.3, 1);
}

.mobile-drawer.open {
  transform: translateX(0);
}

.mobile-drawer-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.mobile-drawer-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.drawer-brand-title {
  font-size: 13.5px;
  font-weight: 700;
  color: var(--text-primary);
}

.drawer-brand-sub {
  font-size: 10.5px;
  color: var(--accent);
  font-family: var(--font-mono);
}

.drawer-close-btn {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.mobile-drawer-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 18px 20px max(30px, env(safe-area-inset-bottom, 30px));
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.copy-alert {
  background: rgba(16, 185, 129, 0.15);
  border-left: 3px solid #10b981;
  padding: 10px 14px;
  font-size: 12px;
  color: #34d399;
  display: flex;
  align-items: center;
  gap: 8px;
}

.drawer-section-title {
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-tertiary);
  margin-bottom: 10px;
  display: block;
}

.drawer-nav-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.drawer-nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 14px;
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-size: 13.5px;
  font-weight: 600;
  text-decoration: none;
  background: var(--bg-surface);
  border: 1px solid var(--border-hairline, rgba(255, 255, 255, 0.05));
  transition: all 0.15s ease;
}

.drawer-nav-item:hover, .drawer-nav-item.router-link-active {
  background: var(--accent-dim);
  border-color: var(--accent-line);
  color: var(--accent);
}

.drawer-nav-item:active {
  transform: scale(0.98);
}

.drawer-nav-icon {
  font-size: 16px;
}

.drawer-pill-badge {
  margin-left: auto;
  font-size: 10px;
  font-weight: 700;
  font-family: var(--font-mono);
  padding: 2px 7px;
  border-radius: var(--radius-pill);
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-secondary);
}

.drawer-pill-badge.accent {
  background: var(--accent-dim);
  color: var(--accent);
  border: 1px solid var(--accent-line);
}

.drawer-pill-badge.hot {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
}

/* Quick Commands Grid */
.quick-commands-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 6px;
}

.quick-cmd-btn {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 10px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  text-align: left;
  transition: all 0.15s;
}

.quick-cmd-btn:hover {
  border-color: var(--accent);
  background: var(--accent-dim);
}

.quick-cmd-btn:active {
  transform: scale(0.98);
}

.q-cmd-code {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  color: var(--accent);
}

.q-cmd-desc {
  font-size: 11px;
  color: var(--text-tertiary);
}

/* Mobile Theme Chips */
.mobile-theme-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
}

.mobile-theme-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  cursor: pointer;
  text-align: left;
}

.mobile-theme-chip.active {
  border-color: var(--accent);
  background: var(--accent-dim);
}

.mobile-theme-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.chip-label {
  font-size: 11.5px;
  font-weight: 600;
  color: var(--text-secondary);
}

.mobile-theme-chip.active .chip-label {
  color: var(--text-primary);
}

.drawer-footer-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 10px;
}

.btn-block {
  width: 100%;
  justify-content: center;
  padding: 10px;
}

/* Theme Switcher Dropdown (Desktop) */
.theme-switcher-wrapper {
  position: relative;
}

.theme-switcher-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 11px;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-pill);
  font-size: 12px;
  font-weight: 500;
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--t-fast);
}

.theme-switcher-btn:hover {
  border-color: var(--accent);
  background: var(--bg-elevated);
}

.theme-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  display: inline-block;
  box-shadow: 0 0 8px currentColor;
  flex-shrink: 0;
}

.theme-btn-label {
  font-size: 12px;
  letter-spacing: -0.01em;
}

.theme-dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 260px;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg), 0 0 20px rgba(0, 0, 0, 0.4);
  padding: 6px;
  z-index: 100;
  display: flex;
  flex-direction: column;
  gap: 3px;
  backdrop-filter: blur(20px);
  animation: themeMenuPop 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes themeMenuPop {
  from { opacity: 0; transform: translateY(-6px) scale(0.97); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.theme-dropdown-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 10px 8px;
  border-bottom: 1px solid var(--border-subtle);
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-tertiary);
}

.theme-count {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--accent);
}

.theme-option-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  cursor: pointer;
  text-align: left;
  transition: all var(--t-fast);
  background: transparent;
}

.theme-option-item:hover {
  background: var(--bg-elevated);
  border-color: var(--border-subtle);
}

.theme-option-item.active {
  background: var(--accent-dim);
  border-color: var(--accent-line);
}

.theme-option-preview {
  width: 26px;
  height: 26px;
  border-radius: var(--radius-sm);
  border: 1.5px solid;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.theme-option-accent {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: block;
}

.theme-option-info {
  flex: 1;
  min-width: 0;
}

.theme-option-name {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12.5px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.2;
}

.theme-active-tag {
  font-size: 9.5px;
  font-weight: 700;
  font-family: var(--font-mono);
  color: var(--accent);
  background: rgba(255, 255, 255, 0.08);
  padding: 1px 5px;
  border-radius: var(--radius-pill);
}

.theme-option-desc {
  font-size: 11px;
  color: var(--text-tertiary);
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

@media (max-width: 960px) {
  .navbar-nav,
  .navbar-actions {
    display: none !important;
  }
  .mobile-header-controls {
    display: flex !important;
  }
}

@media (min-width: 961px) {
  .mobile-header-controls,
  .mobile-backdrop,
  .mobile-drawer {
    display: none !important;
  }
}

@media (max-width: 480px) {
  .navbar-logo-tag { display: none; }
  .navbar-logo-text { font-size: 12.5px; }
}
</style>