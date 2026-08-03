<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface Metric {
  value: string
  label: string
}

interface Capability {
  icon: string
  title: string
  desc: string
}

const heroRef = ref<HTMLElement | null>(null)
const windowRef = ref<HTMLElement | null>(null)
const isVisible = ref(false)
const mouseX = ref(50)
const mouseY = ref(50)
const prefersReducedMotion = ref(false)

const metrics: Metric[] = [
  { value: '41', label: 'MDC rules' },
  { value: '18', label: 'Skills' },
  { value: '272', label: 'Knowledge files' },
  { value: '8', label: 'Specialist agents' }
]

const capabilities: Capability[] = [
  {
    icon: 'route',
    title: 'Context Router',
    desc: 'Routes only the domain knowledge needed for the task. Skip the rest.'
  },
  {
    icon: 'memory',
    title: 'Memory First',
    desc: 'Reuses past decisions, ADRs, and bug fixes from local SQLite.'
  },
  {
    icon: 'token',
    title: 'Token Optimized',
    desc: 'Compression and lazy loading cuts context use by up to 40%.'
  }
]

function smoothScroll(href: string) {
  const target = document.querySelector(href)
  if (target) {
    const navbarHeight = 56
    const targetPosition = target.getBoundingClientRect().top + window.scrollY - navbarHeight
    window.scrollTo({ top: targetPosition, behavior: 'smooth' })
  }
}

function onIntersection(entries: IntersectionObserverEntry[]) {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      isVisible.value = true
    }
  })
}

function onMouseMove(e: MouseEvent) {
  if (prefersReducedMotion.value || !windowRef.value) return
  const rect = windowRef.value.getBoundingClientRect()
  const x = ((e.clientX - rect.left) / rect.width) * 100
  const y = ((e.clientY - rect.top) / rect.height) * 100
  mouseX.value = Math.max(0, Math.min(100, x))
  mouseY.value = Math.max(0, Math.min(100, y))
}

let observer: IntersectionObserver | null = null

onMounted(() => {
  prefersReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  if (heroRef.value && !prefersReducedMotion.value) {
    observer = new IntersectionObserver(onIntersection, { threshold: 0.05 })
    observer.observe(heroRef.value)
  } else {
    isVisible.value = true
  }

  if (windowRef.value) {
    windowRef.value.addEventListener('mousemove', onMouseMove, { passive: true })
  }
})

onUnmounted(() => {
  if (observer) observer.disconnect()
  if (windowRef.value) {
    windowRef.value.removeEventListener('mousemove', onMouseMove)
  }
})

const titleWords1 = ['An', 'opinionated', 'framework']
const titleWords2 = ['for', 'AI', 'coding', 'agents.']
</script>

<template>
  <section class="hero" ref="heroRef">
    <div class="hero-bg" aria-hidden="true">
      <div class="hero-bg-grid"></div>
      <div class="hero-bg-glow"></div>
    </div>

    <div class="container hero-container">
      <div class="hero-grid" :class="{ visible: isVisible }">
        <!-- LEFT: Headline + CTA -->
        <div class="hero-left">
          <div class="hero-eyebrow" :class="{ visible: isVisible }">
            <span class="hero-pulse"></span>
            <span>Open source · MIT License</span>
          </div>

          <h1 class="hero-title">
            <span class="hero-line">
              <span
                v-for="(word, i) in titleWords1"
                :key="`a-${word}`"
                class="hero-word"
                :class="{ visible: isVisible }"
                :style="{ '--i': i }"
              >{{ word }}</span>
            </span>
            <span class="hero-line hero-line-italic">
              <span
                v-for="(word, i) in titleWords2"
                :key="`b-${word}`"
                class="hero-word"
                :class="{ visible: isVisible }"
                :style="{ '--i': titleWords1.length + i }"
              >{{ word }}</span>
            </span>
          </h1>

          <p class="hero-sub" :class="{ visible: isVisible }">
            41 rules, 18 skills, 272 knowledge files, 8 specialist personas.
            One drop-in <code class="hero-code">.cursor/</code> directory that pushes
            your coding agent from prototype to production.
          </p>

          <div class="hero-cta" :class="{ visible: isVisible }">
            <button class="btn btn-primary hero-cta-primary" @click="smoothScroll('#getting-started')">
              Install framework
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M13 6l6 6-6 6"/>
              </svg>
            </button>
            <router-link to="/templates" class="btn btn-secondary">
              Browse templates
            </router-link>
          </div>

          <div class="hero-metrics" :class="{ visible: isVisible }">
            <div v-for="m in metrics" :key="m.label" class="hero-metric">
              <span class="hero-metric-value">{{ m.value }}</span>
              <span class="hero-metric-label">{{ m.label }}</span>
            </div>
          </div>
        </div>

        <!-- RIGHT: Capability stack (real visual, not fake terminal) -->
        <div class="hero-right">
          <div
            class="hero-window"
            ref="windowRef"
            :style="{
              '--mx': `${mouseX}%`,
              '--my': `${mouseY}%`
            }"
          >
            <div class="hero-window-glow" aria-hidden="true"></div>

            <div class="hero-window-bar">
              <div class="hero-window-dots">
                <span></span><span></span><span></span>
              </div>
              <div class="hero-window-title">.cursor/skills/ui_frontend-taste</div>
              <div class="hero-window-action">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="16 18 22 12 16 6"/>
                  <polyline points="8 6 2 12 8 18"/>
                </svg>
              </div>
            </div>
            <div class="hero-window-body">
              <article
                v-for="(cap, i) in capabilities"
                :key="cap.title"
                class="hero-cap"
                :class="{ visible: isVisible }"
                :style="{ '--delay': `${i * 100 + 200}ms` }"
              >
                <div class="hero-cap-icon">
                  <svg v-if="cap.icon === 'route'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75">
                    <circle cx="6" cy="19" r="3"/>
                    <path d="M9 19h8.5a3.5 3.5 0 000-7h-11a3.5 3.5 0 010-7H15"/>
                    <circle cx="18" cy="5" r="3"/>
                  </svg>
                  <svg v-else-if="cap.icon === 'memory'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75">
                    <ellipse cx="12" cy="5" rx="9" ry="3"/>
                    <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75">
                    <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                  </svg>
                </div>
                <div class="hero-cap-text">
                  <div class="hero-cap-title">{{ cap.title }}</div>
                  <div class="hero-cap-desc">{{ cap.desc }}</div>
                </div>
                <div class="hero-cap-status">
                  <span class="hero-cap-status-dot"></span>
                  Active
                </div>
              </article>

              <div class="hero-window-footer">
                <div class="hero-foot-stat">
                  <span class="hero-foot-num">40%</span>
                  <span class="hero-foot-label">tokens saved</span>
                </div>
                <div class="hero-foot-bar">
                  <div class="hero-foot-bar-fill" :class="{ visible: isVisible }"></div>
                </div>
                <div class="hero-foot-stat hero-foot-stat-end">
                  <span class="hero-foot-num">2.1s</span>
                  <span class="hero-foot-label">avg latency</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Floating tag -->
          <div class="hero-float-tag" :class="{ visible: isVisible }">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            <span>Works with Cursor, Claude Code, Codex</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  position: relative;
  padding: 112px 0 80px;
  overflow: hidden;
  min-height: calc(100vh - 56px);
  display: flex;
  align-items: center;
}

.hero-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.hero-bg-grid {
  position: absolute;
  inset: -20% -10% -20% -10%;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.022) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.022) 1px, transparent 1px);
  background-size: 56px 56px;
  mask-image: radial-gradient(ellipse 60% 80% at 50% 0%, black 30%, transparent 75%);
  -webkit-mask-image: radial-gradient(ellipse 60% 80% at 50% 0%, black 30%, transparent 75%);
  animation: grid-drift 60s linear infinite;
}

.hero-bg-glow {
  position: absolute;
  inset: 0;
  background: var(--gradient-hero);
}

@keyframes grid-drift {
  from { transform: translate3d(0, 0, 0); }
  to { transform: translate3d(56px, 56px, 0); }
}

.hero-container {
  position: relative;
  z-index: 1;
}

.hero-grid {
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: 80px;
  align-items: center;
}

/* ─── LEFT COLUMN ─────────────────────────────────────────────────── */
.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px 5px 8px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-pill);
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 28px;
  font-family: var(--font-mono);
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 500ms var(--ease-out-quart), transform 500ms var(--ease-out-quart);
}

.hero-eyebrow.visible {
  opacity: 1;
  transform: translateY(0);
  transition-delay: 0ms;
}

.hero-pulse {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
  animation: pulse-soft 2.4s ease-in-out infinite;
  box-shadow: 0 0 8px var(--accent-glow);
}

@keyframes pulse-soft {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(0.85); }
}

.hero-title {
  font-size: clamp(36px, 5.6vw, 64px);
  font-weight: 600;
  line-height: 1.04;
  letter-spacing: -0.04em;
  color: var(--text-primary);
  margin-bottom: 24px;
}

.hero-line {
  display: block;
  overflow: hidden;
}

.hero-word {
  display: inline-block;
  opacity: 0;
  transform: translateY(110%);
  transition: opacity 600ms var(--ease-out-quart), transform 600ms var(--ease-out-quart);
  transition-delay: calc(var(--i) * 60ms + 100ms);
}

.hero-word.visible {
  opacity: 1;
  transform: translateY(0);
}

.hero-line-italic {
  color: var(--text-tertiary);
  font-style: italic;
  font-weight: 500;
}

.hero-sub {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.65;
  max-width: 52ch;
  margin-bottom: 36px;
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 600ms var(--ease-out-quart), transform 600ms var(--ease-out-quart);
  transition-delay: 700ms;
}

.hero-sub.visible {
  opacity: 1;
  transform: translateY(0);
}

.hero-code {
  font-family: var(--font-mono);
  font-size: 13px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  color: var(--accent);
  margin: 0 2px;
}

.hero-cta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 56px;
  flex-wrap: wrap;
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 600ms var(--ease-out-quart), transform 600ms var(--ease-out-quart);
  transition-delay: 800ms;
}

.hero-cta.visible {
  opacity: 1;
  transform: translateY(0);
}

.hero-cta-primary {
  padding: 11px 20px;
  font-size: 14px;
  font-weight: 500;
  position: relative;
  overflow: hidden;
}

.hero-cta-primary::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(120deg, transparent 30%, rgba(255, 255, 255, 0.15) 50%, transparent 70%);
  transform: translateX(-100%);
  transition: transform 700ms var(--ease-out-quart);
  pointer-events: none;
}

.hero-cta-primary:hover::after {
  transform: translateX(100%);
}

.hero-metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  padding-top: 28px;
  border-top: 1px solid var(--border-hairline);
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 600ms var(--ease-out-quart), transform 600ms var(--ease-out-quart);
  transition-delay: 900ms;
}

.hero-metrics.visible {
  opacity: 1;
  transform: translateY(0);
}

.hero-metric {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.hero-metric-value {
  font-size: 24px;
  font-weight: 600;
  font-family: var(--font-mono);
  letter-spacing: -0.02em;
  color: var(--text-primary);
  line-height: 1;
}

.hero-metric-label {
  font-size: 11px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 500;
}

/* ─── RIGHT COLUMN (real window visual) ───────────────────────────── */
.hero-right {
  position: relative;
}

.hero-window {
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  position: relative;
}

.hero-window-glow {
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-radius: var(--radius-xl);
  opacity: 0;
  background: radial-gradient(
    circle 320px at var(--mx, 50%) var(--my, 50%),
    rgba(16, 185, 129, 0.12) 0%,
    transparent 70%
  );
  transition: opacity 400ms var(--ease-out-quart);
  z-index: 1;
}

.hero-window:hover .hero-window-glow {
  opacity: 1;
}

.hero-window-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-bottom: 1px solid var(--border-hairline);
  background: var(--bg-surface);
  position: relative;
  z-index: 2;
}

.hero-window-dots {
  display: flex;
  gap: 6px;
}

.hero-window-dots span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--border-default);
}

.hero-window-dots span:nth-child(1) { background: rgba(248, 113, 113, 0.5); }
.hero-window-dots span:nth-child(2) { background: rgba(251, 191, 36, 0.5); }
.hero-window-dots span:nth-child(3) { background: rgba(52, 211, 153, 0.5); }

.hero-window-title {
  flex: 1;
  text-align: center;
  font-family: var(--font-mono);
  font-size: 11.5px;
  color: var(--text-tertiary);
  letter-spacing: 0.02em;
}

.hero-window-action {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-tertiary);
}

.hero-window-action svg {
  width: 12px;
  height: 12px;
}

.hero-window-body {
  padding: 8px;
  position: relative;
  z-index: 2;
}

.hero-cap {
  display: grid;
  grid-template-columns: 36px 1fr auto;
  gap: 14px;
  align-items: center;
  padding: 14px 12px;
  border-radius: var(--radius-md);
  transition: background var(--t-fast), transform var(--t-fast);
  opacity: 0;
  transform: translateX(12px);
}

.hero-cap.visible {
  opacity: 1;
  transform: translateX(0);
  transition: opacity 600ms var(--ease-out-quart), transform 600ms var(--ease-out-quart);
  transition-delay: var(--delay);
}

.hero-cap:hover {
  background: rgba(255, 255, 255, 0.02);
  transform: translateX(4px);
}

.hero-cap-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-dim);
  color: var(--accent);
  border: 1px solid var(--accent-line);
  transition: transform var(--t-base);
}

.hero-cap:hover .hero-cap-icon {
  transform: rotate(-6deg) scale(1.05);
}

.hero-cap-icon svg {
  width: 18px;
  height: 18px;
}

.hero-cap-text {
  min-width: 0;
}

.hero-cap-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 2px;
  letter-spacing: -0.005em;
}

.hero-cap-desc {
  font-size: 11.5px;
  color: var(--text-tertiary);
  line-height: 1.45;
}

.hero-cap-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10.5px;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.hero-cap-status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 6px var(--accent-glow);
  animation: pulse-soft 2.4s ease-in-out infinite;
}

.hero-window-footer {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 16px;
  align-items: center;
  padding: 14px 16px;
  margin-top: 6px;
  border-top: 1px solid var(--border-hairline);
  background: var(--bg-surface);
}

.hero-foot-stat {
  display: flex;
  flex-direction: column;
}

.hero-foot-stat-end {
  text-align: right;
}

.hero-foot-num {
  font-size: 14px;
  font-weight: 600;
  font-family: var(--font-mono);
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.hero-foot-label {
  font-size: 10px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.hero-foot-bar {
  height: 6px;
  border-radius: var(--radius-pill);
  background: var(--bg-base);
  overflow: hidden;
}

.hero-foot-bar-fill {
  height: 100%;
  width: 0;
  background: linear-gradient(90deg, var(--accent), var(--accent-bright));
  border-radius: var(--radius-pill);
  transition: width 1.4s var(--ease-out-quart) 1s;
}

.hero-foot-bar-fill.visible {
  width: 60%;
}

/* Floating tag below the window */
.hero-float-tag {
  position: absolute;
  bottom: -22px;
  left: 24px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-pill);
  font-size: 12px;
  color: var(--text-secondary);
  box-shadow: var(--shadow-md);
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 600ms var(--ease-out-quart), transform 600ms var(--ease-out-quart);
  transition-delay: 1100ms;
}

.hero-float-tag.visible {
  opacity: 1;
  transform: translateY(0);
}

.hero-float-tag svg {
  width: 12px;
  height: 12px;
  color: var(--accent);
  stroke-width: 2.5;
}

/* ─── RESPONSIVE ──────────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .hero-grid {
    grid-template-columns: 1fr;
    gap: 56px;
  }

  .hero-right {
    max-width: 540px;
    margin: 0 auto;
    width: 100%;
  }

  .hero-metrics {
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }
}

@media (max-width: 640px) {
  .hero {
    padding: 96px 0 56px;
  }

  .hero-cta {
    flex-direction: column;
    align-items: stretch;
    width: 100%;
  }

  .hero-cta .btn {
    width: 100%;
    justify-content: center;
  }

  .hero-metrics {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px 24px;
  }

  .hero-float-tag {
    position: static;
    margin-top: 24px;
    justify-content: center;
    width: fit-content;
    margin-left: auto;
    margin-right: auto;
  }
}

@media (prefers-reduced-motion: reduce) {
  .hero-bg-grid,
  .hero-pulse,
  .hero-cap-status-dot {
    animation: none !important;
  }

  .hero-word,
  .hero-sub,
  .hero-cta,
  .hero-metrics,
  .hero-eyebrow,
  .hero-float-tag,
  .hero-cap,
  .hero-window-glow {
    transition: none !important;
    transform: none !important;
    opacity: 1 !important;
  }

  .hero-foot-bar-fill.visible {
    width: 60% !important;
    transition: none !important;
  }

  .hero-cta-primary::after {
    display: none;
  }
}
</style>