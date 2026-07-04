<script setup lang="ts">
const footerLinks = {
  framework: [
    { label: 'Templates Gallery', to: '/templates', isRoute: true },
    { label: 'Rules & Skills', href: '#explorer' },
    { label: 'Nguyên tắc', href: '#principles' },
    { label: 'Kiến trúc', href: '#architecture' },
    { label: 'Components', href: '#components' },
    { label: 'Domains', href: '#domains' },
    { label: 'Agent Personas', href: '#agents' }
  ],
  resources: [
    { label: 'Documentation', href: 'https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR#readme', external: true },
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

const socialLinks = [
  {
    name: 'GitHub',
    href: 'https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR',
    icon: 'github'
  },
  {
    name: 'Discord',
    href: '#',
    icon: 'discord'
  },
  {
    name: 'Twitter',
    href: '#',
    icon: 'twitter'
  }
]

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
            <span class="cef-badge cef-badge-purple">v5.0.0</span>
            <span class="cef-badge cef-badge-outline">MIT</span>
          </div>
          <div class="footer-social">
            <a 
              v-for="social in socialLinks" 
              :key="social.name"
              :href="social.href"
              :aria-label="social.name"
              target="_blank"
              rel="noopener noreferrer"
              class="social-link"
            >
              <svg v-if="social.icon === 'github'" viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              <svg v-else-if="social.icon === 'discord'" viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
                <path d="M20.317 4.37a19.791 19.791 0 00-4.885-1.515.074.074 0 00-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 00-5.487 0 12.64 12.64 0 00-.617-1.25.077.077 0 00-.079-.037A19.736 19.736 0 003.677 4.37a.07.07 0 00-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 00.031.057 19.9 19.9 0 005.993 3.03.078.078 0 00.084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 00-.041-.106 13.107 13.107 0 01-1.872-.892.077.077 0 01-.008-.128 10.2 10.2 0 00.372-.292.074.074 0 01.077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 01.078.01c.12.098.246.198.373.292a.077.077 0 01-.006.127 12.299 12.299 0 01-1.873.892.077.077 0 00-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 00.084.028 19.839 19.839 0 006.002-3.03.077.077 0 00.032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 00-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
              </svg>
            </a>
          </div>
        </div>

        <div class="footer-col">
          <h4>Framework</h4>
          <ul>
            <li v-for="link in footerLinks.framework" :key="link.label">
              <router-link v-if="link.isRoute" :to="link.to!">{{ link.label }}</router-link>
              <a v-else :href="link.href" @click="smoothScroll($event, link.href!)">{{ link.label }}</a>
            </li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Resources</h4>
          <ul>
            <li v-for="link in footerLinks.resources" :key="link.label">
              <a :href="link.href" :target="link.external ? '_blank' : undefined" :rel="link.external ? 'noopener noreferrer' : undefined">{{ link.label }}</a>
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

.footer-social {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}

.social-link {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  transition: all var(--t-fast);
}

.social-link:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: var(--border-accent);
  color: var(--text-primary);
  transform: translateY(-2px);
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
