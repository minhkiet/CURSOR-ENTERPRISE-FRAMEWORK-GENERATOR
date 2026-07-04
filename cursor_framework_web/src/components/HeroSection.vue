<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const heroRef = ref<HTMLElement | null>(null)
const isVisible = ref(false)

const { observe } = useIntersectionObserver()

function smoothScroll(href: string) {
  const target = document.querySelector(href)
  if (target) {
    const navbarHeight = 60
    const targetPosition = target.getBoundingClientRect().top + window.scrollY - navbarHeight
    window.scrollTo({ top: targetPosition, behavior: 'smooth' })
  }
}

const stats = [
  { icon: 'layers', title: 'Rules', count: '41', items: ['skill-registry, skill-integration', 'architecture-patterns, coding-standards', 'security, performance, multi-tenant'], color: 'violet' },
  { icon: 'file', title: 'Skills', count: '18', items: ['frontend-taste, frontend-review', 'karpathy-coding, ponytail', 'security-review, full-output'], color: 'cyan' },
  { icon: 'search', title: 'Knowledge', count: '37', items: ['architecture, best-practice, anti-pattern', 'faq, checklist, glossary', 'decision-tree per domain'], color: 'emerald' },
  { icon: 'code', title: 'Domains', count: '37+', items: ['Nuxt, Vue, Next, React', 'Laravel, NestJS, ASP.NET Core', 'Supabase, PostgreSQL, Redis'], color: 'violet' }
]

const terminalLines = [
  { type: 'cmd', text: 'Initialize CEF for my CRM project' },
  { type: 'muted', text: 'Loading rules...', success: '41 rules loaded' },
  { type: 'muted', text: 'Loading skills...', success: '18 skills loaded' },
  { type: 'muted', text: 'Loading knowledge...', success: '37 knowledge directories indexed' },
  { type: 'muted', text: 'Building memory...', success: 'Context optimized' },
  { type: 'cmd', text: 'Build Multi-Tenant SaaS with Supabase' },
  { type: 'success', text: '✓ Context routed: supabase, rls, multi-tenant' },
  { type: 'cyan', text: '✓ Token saved: 12,400 (~40% reduction)' }
]

onMounted(() => {
  if (heroRef.value) {
    observe(heroRef.value, () => {
      isVisible.value = true
    }, { threshold: 0.1 })
  }
})
</script>

<template>
  <section class="hero" ref="heroRef">
    <div class="hero-content">
      <div class="hero-badge">
        <span class="badge-dot"></span>
        <span>v5.0.0</span>
        <span class="badge-sep">·</span>
        <span>604 files</span>
        <span class="badge-sep">·</span>
        <span>8 agents</span>
      </div>

      <h1 class="hero-title">
        <span class="hero-title-line">Framework cấp Enterprise</span>
        <span class="hero-title-accent">cho AI Coding Agents</span>
      </h1>

      <p class="hero-subtitle">
        Tối ưu hiệu suất AI coding agents trên mọi IDE — Cursor, Claude Code,
        Vibe Code, Windsurf, Cline. Memory-First, Retrieval-First, Token-Optimized.
      </p>

      <div class="hero-actions">
        <a href="#getting-started" class="hero-btn hero-btn-primary" @click.prevent="smoothScroll('#getting-started')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
          Bắt đầu nhanh
        </a>
        <a href="#architecture" class="hero-btn hero-btn-outline" @click.prevent="smoothScroll('#architecture')">
          Xem kiến trúc
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M7 17l9.2-9.2M17 17V7H7"/>
          </svg>
        </a>
      </div>

      <div class="hero-cards">
        <div class="hc-left" :class="{ visible: isVisible }">
          <div
            v-for="(stat, index) in stats"
            :key="stat.title"
            class="hc-card"
            :style="{ transitionDelay: `${index * 80}ms` }"
          >
            <div class="hc-card-header">
              <div class="hc-card-icon" :class="{ cyan: stat.color === 'cyan', emerald: stat.color === 'emerald', violet: stat.color === 'violet' }">
                <svg v-if="stat.icon === 'layers'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
                <svg v-else-if="stat.icon === 'file'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="8" y1="13" x2="16" y2="13"/>
                  <line x1="8" y1="17" x2="16" y2="17"/>
                </svg>
                <svg v-else-if="stat.icon === 'search'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="11" cy="11" r="8"/>
                  <path d="M21 21l-4.35-4.35"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <polyline points="16 18 22 12 16 6"/>
                  <polyline points="8 6 2 12 8 18"/>
                </svg>
              </div>
              <span class="hc-card-title">{{ stat.title }}</span>
              <span class="hc-card-count" :class="{ cyan: stat.color === 'cyan', emerald: stat.color === 'emerald', violet: stat.color === 'violet' }">
                {{ stat.count }}
              </span>
            </div>
            <div class="hc-card-items">
              <div v-for="item in stat.items" :key="item" class="hc-item">
                <span class="hc-dot" :class="{ 'hc-dot-cyan': stat.color === 'cyan', 'hc-dot-emerald': stat.color === 'emerald', 'hc-dot-violet': stat.color === 'violet' }"></span>
                {{ item }}
              </div>
            </div>
          </div>
        </div>

        <div class="hc-right" :class="{ visible: isVisible }">
          <div class="hc-right-header">
            <div class="hc-terminal-dots">
              <span></span><span></span><span></span>
            </div>
            <span class="hc-terminal-label">cursor-agent — zsh</span>
          </div>
          <div class="hc-terminal-body">
            <div
              v-for="(line, index) in terminalLines"
              :key="index"
              class="hc-terminal-line"
              :style="{ animationDelay: `${0.3 + index * 0.3}s` }"
            >
              <span v-if="line.type === 'cmd'" class="ht-prompt">$</span>
              <span v-if="line.type === 'cmd'" class="ht-cmd">{{ line.text }}</span>
              <span v-if="line.type === 'muted'" class="ht-muted">{{ line.text }}</span>
              <span v-if="line.success" class="ht-success"> {{ line.success }}</span>
              <span v-if="line.type === 'success'" class="ht-success">{{ line.text }}</span>
              <span v-if="line.type === 'cyan'" class="ht-cyan">{{ line.text }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hc-card-icon.cyan {
  background: rgba(6, 182, 212, 0.08);
  border-color: rgba(6, 182, 212, 0.2);
}

.hc-card-icon.cyan svg {
  stroke: #06b6d4;
}

.hc-card-icon.emerald {
  background: rgba(52, 211, 153, 0.08);
  border-color: rgba(52, 211, 153, 0.2);
}

.hc-card-icon.emerald svg {
  stroke: #34d399;
}

.hc-card-icon.violet {
  background: rgba(120, 119, 232, 0.12);
  border-color: rgba(120, 119, 232, 0.3);
}

.hc-card-icon.violet svg {
  stroke: #a78bfa;
}

.hc-card-count.cyan {
  color: #06b6d4;
  background: rgba(6, 182, 212, 0.08);
}

.hc-card-count.emerald {
  color: #34d399;
  background: rgba(52, 211, 153, 0.08);
}

.hc-card-count.violet {
  color: #a78bfa;
  background: rgba(120, 119, 232, 0.12);
}

.hc-dot-violet {
  background: #a78bfa;
}

.hc-left {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.5s var(--ease-out), transform 0.5s var(--ease-out);
}

.hc-left.visible {
  opacity: 1;
  transform: translateY(0);
}

.hc-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-lg);
  padding: 18px 20px;
  text-align: left;
  transition: border-color var(--t-base), box-shadow var(--t-base), transform var(--t-base);
  position: relative;
  overflow: hidden;
}

.hc-card:hover {
  border-color: var(--border-accent);
  box-shadow: 0 0 32px rgba(120, 119, 232, 0.08);
  transform: translateY(-1px);
}

.hc-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--gradient-primary);
  opacity: 0;
  transition: opacity var(--t-base);
}

.hc-card:hover::before {
  opacity: 1;
}

.hc-right {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.5s var(--ease-out) 0.24s, transform 0.5s var(--ease-out) 0.24s;
}

.hc-right.visible {
  opacity: 1;
  transform: translateY(0);
}
</style>
