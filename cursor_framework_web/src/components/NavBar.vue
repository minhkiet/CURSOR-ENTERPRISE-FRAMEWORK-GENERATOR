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
  { to: '/learn', label: 'Library', kind: 'route' },
  { href: '#explorer', label: 'Explorer', kind: 'anchor' },
  { href: '#architecture', label: 'Architecture', kind: 'anchor' },
  { to: '/prompts', label: 'Prompts', kind: 'route' },
  { to: '/templates', label: 'Templates', kind: 'route' },
  { to: '/cms', label: 'CMS Dashboard', kind: 'route' },
  { to: '/install', label: 'Install', kind: 'route' }
] as const

function handleScroll() {
  isScrolled.value = window.scrollY > 8
}

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

function closeMobileMenu() {
  isMobileMenuOpen.value = false
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
  isMobileMode.value = window.innerWidth < 880
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
        <span class="navbar-logo-text">Cursor Enterprise</span>
        <span class="navbar-logo-tag">Framework</span>
      </router-link>

      <nav v-if="!isMobileMode" class="navbar-nav">
        <template v-for="link in navLinks" :key="link.label">
          <router-link
            v-if="link.kind === 'route'"
            :to="link.to"
            class="nav-link"
            @click="closeMobileMenu"
          >
            {{ link.label }}
          </router-link>
          <a
            v-else
            :href="link.href"
            class="nav-link"
            @click="smoothScroll($event, link.href)"
          >
            {{ link.label }}
          </a>
        </template>
      </nav>

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
        <router-link to="/templates" class="btn btn-primary">
          Templates
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M7 17l9.2-9.2M17 17V7H7"/>
          </svg>
        </router-link>
      </div>

      <button
        v-if="isMobileMode"
        class="navbar-toggle"
        @click="toggleMobileMenu"
        :aria-label="isMobileMenuOpen ? 'Close menu' : 'Open menu'"
        :aria-expanded="isMobileMenuOpen"
      >
        <span :class="{ open: isMobileMenuOpen }"></span>
        <span :class="{ open: isMobileMenuOpen }"></span>
      </button>
    </div>

    <div v-if="isMobileMode" class="mobile-menu" :class="{ open: isMobileMenuOpen }">
      <nav class="mobile-nav">
        <template v-for="link in navLinks" :key="link.label">
          <router-link
            v-if="link.kind === 'route'"
            :to="link.to"
            class="mobile-nav-link"
            @click="closeMobileMenu"
          >
            {{ link.label }}
          </router-link>
          <a
            v-else
            :href="link.href"
            class="mobile-nav-link"
            @click="smoothScroll($event, link.href)"
          >
            {{ link.label }}
          </a>
        </template>
        <router-link to="/templates" class="mobile-nav-link" @click="closeMobileMenu">
          Templates
        </router-link>
        <a href="https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR" class="mobile-nav-link" target="_blank" rel="noopener">
          GitHub
        </a>

        <!-- Mobile Theme Bar -->
        <div class="mobile-theme-section">
          <div class="mobile-theme-title">Theme Giao Diện</div>
          <div class="mobile-theme-grid">
            <button
              v-for="t in themes"
              :key="t.id"
              class="mobile-theme-chip"
              :class="{ active: currentTheme === t.id }"
              @click="selectTheme(t.id)"
            >
              <span class="mobile-theme-dot" :style="{ backgroundColor: t.accentColor }"></span>
              <span>{{ t.name }}</span>
            </button>
          </div>
        </div>
      </nav>
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
  height: 56px;
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
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 var(--container-px);
  height: 100%;
  display: flex;
  align-items: center;
  gap: 32px;
}

.navbar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
  font-weight: 600;
}

.navbar-logo-mark {
  width: 26px;
  height: 26px;
  border-radius: var(--radius-sm);
  background: var(--accent);
  color: var(--bg-base);
  display: flex;
  align-items: center;
  justify-content: center;
}

.navbar-logo-mark svg {
  width: 15px;
  height: 15px;
  stroke-width: 2.5;
}

.navbar-logo-text {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.015em;
}

.navbar-logo-tag {
  font-size: 12px;
  color: var(--text-tertiary);
  font-weight: 400;
  padding-left: 10px;
  margin-left: 2px;
  border-left: 1px solid var(--border-subtle);
}

.navbar-nav {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
}

.nav-link {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  transition: color var(--t-fast), background var(--t-fast);
}

.nav-link:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.04);
}

.nav-link.router-link-active {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.06);
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}

.navbar-toggle {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 32px;
  height: 32px;
  padding: 8px;
  margin-left: auto;
  border-radius: var(--radius-sm);
}

.navbar-toggle span {
  display: block;
  width: 100%;
  height: 1.5px;
  background: var(--text-primary);
  border-radius: 2px;
  transition: transform var(--t-fast), opacity var(--t-fast);
}

.navbar-toggle span.open:nth-child(1) {
  transform: translateY(6.5px) rotate(45deg);
}

.navbar-toggle span.open:nth-child(2) {
  transform: rotate(-45deg);
}

.mobile-menu {
  max-height: 0;
  overflow: hidden;
  background: var(--bg-overlay);
  backdrop-filter: blur(20px) saturate(160%);
  border-bottom: 1px solid var(--border-hairline);
  transition: max-height var(--t-base);
}

.mobile-menu.open {
  max-height: 400px;
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  padding: 12px 24px 20px;
  gap: 2px;
}

.mobile-nav-link {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  padding: 11px 12px;
  border-radius: var(--radius-sm);
  transition: color var(--t-fast), background var(--t-fast);
}

.mobile-nav-link:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.04);
}

.mobile-nav-link.router-link-active {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.06);
}

/* ─── Theme Switcher Styles ─── */
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
  from {
    opacity: 0;
    transform: translateY(-6px) scale(0.97);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
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

/* Mobile Theme Picker */
.mobile-theme-section {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border-subtle);
}

.mobile-theme-title {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-tertiary);
  margin-bottom: 8px;
  padding: 0 4px;
}

.mobile-theme-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
}

.mobile-theme-chip {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 8px 10px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  font-size: 12px;
  color: var(--text-secondary);
  cursor: pointer;
  text-align: left;
}

.mobile-theme-chip.active {
  border-color: var(--accent);
  color: var(--text-primary);
  background: var(--accent-dim);
}

.mobile-theme-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

@media (max-width: 480px) {
  .navbar-logo-tag { display: none; }
  .navbar-logo-text { font-size: 13px; }
}
</style>