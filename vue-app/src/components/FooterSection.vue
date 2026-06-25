<script setup lang="ts">
const footerLinks = {
  framework: [
    { label: 'Rules & Skills', href: '#explorer' },
    { label: 'Nguyên tắc', href: '#principles' },
    { label: 'Kiến trúc', href: '#architecture' },
    { label: 'Components', href: '#components' },
    { label: 'Domains', href: '#domains' }
  ],
  resources: [
    { label: 'Documentation', href: '#' },
    { label: 'Knowledge Base', href: '#' },
    { label: 'Rules Reference', href: '#' },
    { label: 'Scripts', href: '#' }
  ],
  community: [
    { label: 'GitHub', href: 'https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR', external: true },
    { label: 'Discord', href: '#' },
    { label: 'Twitter / X', href: '#' },
    { label: 'Changelog', href: '#' }
  ]
}

function smoothScroll(e: Event, href: string) {
  if (href.startsWith('#')) {
    e.preventDefault()
    const target = document.querySelector(href)
    if (target) {
      const navbarHeight = 60
      const targetPosition = target.getBoundingClientRect().top + window.scrollY - navbarHeight
      window.scrollTo({ top: targetPosition, behavior: 'smooth' })
    }
  }
}
</script>

<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <div class="footer-logo">
            <div class="footer-logo-icon">
              <svg viewBox="0 0 16 16" fill="none">
                <path d="M8 1L1 4.5L8 8L15 4.5L8 1Z" fill="white" fill-opacity="0.9"/>
                <path d="M1 11.5L8 15L15 11.5" stroke="white" stroke-opacity="0.6" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M1 7.75L8 11.25L15 7.75" stroke="white" stroke-opacity="0.75" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </div>
            <span>Cursor Enterprise Framework</span>
          </div>
          <p>Enterprise-grade framework cho AI coding agents. Tối ưu token, memory, và knowledge reuse.</p>
          <div class="footer-version">
            <span class="cef-badge cef-badge-purple">v4.0.0</span>
            <span class="cef-badge cef-badge-outline">MIT</span>
          </div>
        </div>

        <div class="footer-col">
          <h4>Framework</h4>
          <ul>
            <li v-for="link in footerLinks.framework" :key="link.label">
              <a :href="link.href" @click="smoothScroll($event, link.href)">{{ link.label }}</a>
            </li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Resources</h4>
          <ul>
            <li v-for="link in footerLinks.resources" :key="link.label">
              <a :href="link.href">{{ link.label }}</a>
            </li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Community</h4>
          <ul>
            <li v-for="link in footerLinks.community" :key="link.label">
              <a :href="link.href" :target="link.external ? '_blank' : undefined" :rel="link.external ? 'noopener noreferrer' : undefined">
                {{ link.label }}
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <span>MIT License &copy; 2026 Cursor Enterprise Framework</span>
        <span class="footer-stats">
          463 files &nbsp;&middot;&nbsp; 79 rules &nbsp;&middot;&nbsp; 47 skills &nbsp;&middot;&nbsp; 272 knowledge &nbsp;&middot;&nbsp; 35+ domains
        </span>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  border-top: 1px solid var(--border-subtle);
  padding: 64px 0 40px;
  background: rgba(255, 255, 255, 0.01);
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 40px;
  margin-bottom: 48px;
}

.footer-brand {
  max-width: 340px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.footer-logo-icon {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  background: var(--gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 12px rgba(120, 119, 232, 0.25);
}

.footer-logo-icon svg {
  width: 14px;
  height: 14px;
}

.footer-logo span {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
}

.footer-brand p {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.65;
  margin-bottom: 16px;
}

.footer-version {
  display: flex;
  gap: 6px;
}

.footer-col h4 {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 16px;
}

.footer-col ul {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.footer-col li a {
  font-size: 12.5px;
  color: var(--text-secondary);
  transition: color var(--t-fast);
}

.footer-col li a:hover {
  color: var(--text-primary);
}

.footer-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 28px;
  border-top: 1px solid var(--border-subtle);
  font-size: 11px;
  color: var(--text-muted);
}

.footer-stats {
  font-family: var(--font-mono);
  font-size: 10.5px;
}

@media (max-width: 1024px) {
  .footer-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 28px;
  }

  .footer-bottom {
    flex-direction: column;
    gap: 10px;
    text-align: center;
  }
}
</style>
