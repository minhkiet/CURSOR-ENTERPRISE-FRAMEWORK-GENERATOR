<script setup lang="ts">
import { currentYear } from '../composables/useCurrentYear'

interface FooterLink {
  label: string
  href: string
  external?: boolean
}

interface FooterGroup {
  label: string
  links: FooterLink[]
}

const linkGroups: FooterGroup[] = [
  {
    label: 'Framework',
    links: [
      { label: 'Library', href: '/learn' },
      { label: 'Architecture', href: '#architecture' },
      { label: 'Subagents', href: '#agents' },
      { label: 'Principles', href: '#principles' }
    ]
  },
  {
    label: 'Resources',
    links: [
      { label: 'Templates', href: '/templates' },
      { label: 'Prompts', href: '/prompts' },
      { label: 'Components', href: '#components' },
      { label: 'Optimization', href: '#optimization' }
    ]
  },
  {
    label: 'Stack',
    links: [
      { label: 'File explorer', href: '#explorer' },
      { label: 'Getting started', href: '#getting-started' },
      { label: 'Karpathy guidelines', href: 'https://github.com/multica-ai/andrej-karpathy-skills', external: true },
      { label: 'GitHub repo', href: 'https://github.com', external: true }
    ]
  }
]

function smoothScroll(e: MouseEvent, href: string): void {
  if (!href.startsWith('#')) return
  e.preventDefault()
  const target = document.querySelector(href) as HTMLElement | null
  if (!target) return
  const navbarHeight = 56
  const targetPosition = target.getBoundingClientRect().top + window.scrollY - navbarHeight
  window.scrollTo({ top: targetPosition, behavior: 'smooth' })
  history.pushState(null, '', href)
}
</script>

<template>
  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <div class="footer-logo">
            <svg class="hero-logo-mark" viewBox="0 0 36 36" fill="none">
              <rect x="6" y="6" width="20" height="20" rx="3" stroke="currentColor" stroke-width="1.5"/>
              <path d="M12 24L18 14L24 24" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"/>
              <path d="M14.5 20L21.5 20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <circle cx="30" cy="14" r="3" fill="currentColor"/>
            </svg>
            <div class="footer-logo-text">
              <span class="footer-logo-main">Cursor Enterprise Framework</span>
              <span class="footer-logo-sub">Opinionated structure for AI coding agents</span>
            </div>
          </div>

          <div class="footer-status">
            <span class="footer-status-dot"></span>
            <span class="footer-status-text">All systems operational</span>
          </div>
        </div>

        <nav class="footer-links" aria-label="Footer navigation">
          <div v-for="group in linkGroups" :key="group.label" class="footer-group">
            <div class="footer-label">{{ group.label }}</div>
            <ul class="footer-list">
              <li v-for="link in group.links" :key="link.label">
                <a
                  v-if="link.external"
                  :href="link.href"
                  class="footer-link"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {{ link.label }}
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="footer-link-icon" aria-hidden="true">
                    <path d="M7 17L17 7M17 7H8M17 7V16"/>
                  </svg>
                </a>
                <router-link
                  v-else-if="link.href.startsWith('/')"
                  :to="link.href"
                  class="footer-link"
                >
                  {{ link.label }}
                </router-link>
                <a
                  v-else
                  :href="link.href"
                  class="footer-link"
                  @click="smoothScroll($event, link.href)"
                >
                  {{ link.label }}
                </a>
              </li>
            </ul>
          </div>
        </nav>
      </div>

      <div class="footer-bottom">
        <div class="footer-meta">
          <span>{{ currentYear }} Cursor Enterprise Framework</span>
          <span class="footer-sep" aria-hidden="true">·</span>
          <span class="footer-mono">build {{ new Date().toISOString().slice(0, 10) }}</span>
        </div>
        <div class="footer-legal">
          <a href="https://github.com" class="footer-link" target="_blank" rel="noopener noreferrer">
            Documentation
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="footer-link-icon" aria-hidden="true">
              <path d="M7 17L17 7M17 7H8M17 7V16"/>
            </svg>
          </a>
          <span class="footer-sep" aria-hidden="true">·</span>
          <a href="https://github.com" class="footer-link" target="_blank" rel="noopener noreferrer">
            MIT License
          </a>
          <span class="footer-sep" aria-hidden="true">·</span>
          <router-link to="/" class="footer-link">
            Changelog
          </router-link>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  border-top: 1px solid var(--border-subtle);
  background: var(--bg-canvas);
  margin-top: var(--section-py);
  padding: 64px 0 32px;
}

.footer-top {
  display: grid;
  grid-template-columns: 1.4fr 2fr;
  gap: 48px;
  padding-bottom: 48px;
  border-bottom: 1px solid var(--border-subtle);
}

.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.footer-logo {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.hero-logo-mark {
  width: 36px;
  height: 36px;
  color: var(--accent);
  flex-shrink: 0;
  margin-top: 2px;
}

.footer-logo-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.footer-logo-main {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.footer-logo-sub {
  font-size: 12.5px;
  color: var(--text-tertiary);
  line-height: 1.5;
  max-width: 280px;
}

.footer-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  width: fit-content;
}

.footer-status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.18);
  animation: pulse 2.4s var(--ease-out-quart) infinite;
}

.footer-status-text {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-secondary);
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.18); }
  50% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0.06); }
}

@media (prefers-reduced-motion: reduce) {
  .footer-status-dot {
    animation: none;
  }
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.footer-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 14px;
}

.footer-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  color: var(--text-secondary);
  transition: color var(--t-fast);
  cursor: pointer;
}

.footer-link:hover {
  color: var(--text-primary);
}

.footer-link-icon {
  width: 11px;
  height: 11px;
  color: var(--text-tertiary);
  transition: color var(--t-fast);
  flex-shrink: 0;
}

.footer-link:hover .footer-link-icon {
  color: var(--accent);
}

.footer-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 24px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.footer-meta, .footer-legal {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.footer-sep {
  color: var(--text-faint);
}

.footer-mono {
  font-family: var(--font-mono);
}

@media (max-width: 768px) {
  .footer-top {
    grid-template-columns: 1fr;
    gap: 32px;
  }
  .footer-links {
    grid-template-columns: repeat(2, 1fr);
    gap: 28px;
  }
  .footer-bottom {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .footer-links {
    grid-template-columns: 1fr;
  }
}
</style>