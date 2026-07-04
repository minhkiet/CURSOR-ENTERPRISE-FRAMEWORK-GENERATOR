<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isScrolled = ref(false)
const isMobileMenuOpen = ref(false)
const isMobileMode = ref(false)

const navLinks = [
  { label: 'Templates', to: '/templates', isRoute: true },
  { href: '#explorer', label: 'Rules & Skills' },
  { href: '#principles', label: 'Nguyên tắc' },
  { href: '#architecture', label: 'Kiến trúc' },
  { href: '#components', label: 'Components' },
  { href: '#domains', label: 'Domains' },
  { href: '#agents', label: 'Agents' },
  { href: '#prompts', label: 'Prompts' },
  { href: '#getting-started', label: 'Bắt đầu' }
]

function handleScroll() {
  isScrolled.value = window.scrollY > 20
}

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

function closeMobileMenu() {
  isMobileMenuOpen.value = false
}

function checkMobileMode() {
  const inner = document.querySelector('.navbar-inner') as HTMLElement | null
  const nav = document.querySelector('.navbar-nav') as HTMLElement | null
  
  if (inner) {
    const isNarrowContainer = inner.offsetWidth < 1024
    
    let isNavWrapped = false
    if (nav) {
      const firstLink = nav.querySelector('.nav-link') as HTMLElement | null
      const lineHeight = firstLink ? parseInt(getComputedStyle(firstLink).lineHeight) || 28 : 28
      const navHeight = nav.offsetHeight
      isNavWrapped = navHeight > lineHeight * 1.2
    }
    
    isMobileMode.value = isNarrowContainer || isNavWrapped
  }
}

function smoothScroll(e: Event, link: { href?: string; to?: string; isRoute?: boolean }): void {
  e.preventDefault()
  if (link.isRoute && link.to) {
    router.push(link.to)
  } else if (link.href) {
    const target = document.querySelector(link.href)
    if (target) {
      const navbarHeight = 60
      const targetPosition = target.getBoundingClientRect().top + window.scrollY - navbarHeight
      window.scrollTo({ top: targetPosition, behavior: 'smooth' })
    }
  }
  closeMobileMenu()
}

onMounted(() => {
  queueMicrotask(() => {
    checkMobileMode()
  })
  
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('resize', checkMobileMode)
  handleScroll()
  
  const inner = document.querySelector('.navbar-inner')
  if (inner) {
    const observer = new ResizeObserver(checkMobileMode)
    observer.observe(inner)
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', checkMobileMode)
})
</script>

<template>
  <header class="navbar" :class="{ scrolled: isScrolled }">
    <div class="navbar-inner">
      <router-link to="/" class="navbar-logo">
        <div class="navbar-logo-icon">
          <svg viewBox="0 0 16 16" fill="none">
            <path d="M8 1L1 4.5L8 8L15 4.5L8 1Z" fill="white" fill-opacity="0.9"/>
            <path d="M1 11.5L8 15L15 11.5" stroke="white" stroke-opacity="0.6" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M1 7.75L8 11.25L15 7.75" stroke="white" stroke-opacity="0.75" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </div>
        <span class="navbar-logo-text">CEF</span>
        <span class="navbar-logo-sep">/</span>
        <span class="navbar-logo-full">Enterprise Framework</span>
        <span class="navbar-badge">v5.0</span>
      </router-link>

      <nav class="navbar-nav" :class="{ 'mobile-trigger': isMobileMode }">
        <template v-for="link in navLinks" :key="link.label">
          <router-link
            v-if="link.isRoute"
            :to="link.to!"
            class="nav-link"
          >
            {{ link.label }}
          </router-link>
          <a
            v-else
            :href="link.href"
            class="nav-link"
            @click="smoothScroll($event, link)"
          >
            {{ link.label }}
          </a>
        </template>
      </nav>

      <div class="navbar-actions">
        <a href="https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR" class="btn-ghost" target="_blank" rel="noopener">
          <svg viewBox="0 0 24 24" fill="currentColor" width="15" height="15">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
          </svg>
          <span>GitHub</span>
          <span class="star-badge">★</span>
        </a>
        <router-link to="/templates" class="btn-primary">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
          Templates
        </router-link>
      </div>

      <button
        v-show="isMobileMode"
        class="navbar-mobile-toggle"
        @click="toggleMobileMenu"
        aria-label="Toggle menu"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>

    <div v-show="isMobileMode" class="mobile-menu" :class="{ open: isMobileMenuOpen }">
      <nav class="mobile-nav">
        <template v-for="link in navLinks" :key="link.label">
          <router-link
            v-if="link.isRoute"
            :to="link.to!"
            class="mobile-nav-link"
            @click="closeMobileMenu"
          >
            {{ link.label }}
          </router-link>
          <a
            v-else
            :href="link.href"
            class="mobile-nav-link"
            @click="smoothScroll($event, link)"
          >
            {{ link.label }}
          </a>
        </template>
      </nav>
    </div>
  </header>
</template>
