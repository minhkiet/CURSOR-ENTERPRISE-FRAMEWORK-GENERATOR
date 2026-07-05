<script setup lang="ts">
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const isScrolled = ref(false)
const isMobileMenuOpen = ref(false)
const isMobileMode = ref(false)

const navLinks = [
  { to: '/learn', label: 'Library', kind: 'route' },
  { href: '#explorer', label: 'Explorer', kind: 'anchor' },
  { href: '#architecture', label: 'Architecture', kind: 'anchor' },
  { to: '/prompts', label: 'Prompts', kind: 'route' },
  { href: '#getting-started', label: 'Install', kind: 'anchor' }
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
  checkMobileMode()
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('resize', checkMobileMode)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', checkMobileMode)
})
</script>

<template>
  <header class="navbar" :class="{ scrolled: isScrolled }">
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

.navbar.scrolled {
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

@media (max-width: 480px) {
  .navbar-logo-tag { display: none; }
  .navbar-logo-text { font-size: 13px; }
}
</style>