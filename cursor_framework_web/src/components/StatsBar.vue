<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface Stat {
  target: number
  label: string
  decimals?: number
  suffix?: string
}

const stats: Stat[] = [
  { target: 720, label: 'Total files' },
  { target: 39, label: 'Rules' },
  { target: 22, label: 'Skills' },
  { target: 329, label: 'Knowledge files' },
  { target: 18, label: 'Agents' },
  { target: 4, label: 'TDAM layers', suffix: '' }
]

const displayValues = ref<number[]>(stats.map(() => 0))
const isVisible = ref(false)
const sectionRef = ref<HTMLElement | null>(null)
const reduceMotion = ref(false)

let observer: IntersectionObserver | null = null
let rafIds: number[] = []
let hasRun = false

function easeOutQuart(t: number): number {
  return 1 - Math.pow(1 - t, 4)
}

function animateCounter(index: number, target: number, startDelay: number, duration = 1600) {
  const startTime = performance.now() + startDelay
  const update = (currentTime: number) => {
    if (currentTime < startTime) {
      rafIds.push(requestAnimationFrame(update))
      return
    }
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)
    const eased = easeOutQuart(progress)
    displayValues.value[index] = Math.round(eased * target)
    if (progress < 1) {
      rafIds.push(requestAnimationFrame(update))
    }
  }
  rafIds.push(requestAnimationFrame(update))
}

function setFinalValues() {
  displayValues.value = stats.map((s) => s.target)
}

onMounted(() => {
  reduceMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  if (reduceMotion.value) {
    setFinalValues()
    isVisible.value = true
    return
  }

  if (!sectionRef.value) return

  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !hasRun) {
          hasRun = true
          isVisible.value = true
          stats.forEach((stat, index) => {
            animateCounter(index, stat.target, index * 120)
          })
          observer?.disconnect()
        }
      })
    },
    { threshold: 0.4 }
  )

  observer.observe(sectionRef.value)
})

onUnmounted(() => {
  rafIds.forEach((id) => cancelAnimationFrame(id))
  observer?.disconnect()
})
</script>

<template>
  <section class="stats-bar" ref="sectionRef">
    <div class="container">
      <div class="stats-grid" :class="{ visible: isVisible }">
        <div
          v-for="(stat, index) in stats"
          :key="stat.label"
          class="stat-item"
          :class="{ visible: isVisible }"
          :style="{ '--delay': `${index * 80}ms` }"
        >
          <span class="stat-number">
            {{ displayValues[index].toLocaleString('en-US') }}
          </span>
          <span class="stat-label">{{ stat.label }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.stats-bar {
  border-top: 1px solid var(--border-hairline);
  border-bottom: 1px solid var(--border-hairline);
  padding: 36px 0;
  background: rgba(255, 255, 255, 0.01);
  position: relative;
}

.stats-bar::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 40% 100% at 0% 50%, rgba(16, 185, 129, 0.04), transparent 60%),
    radial-gradient(ellipse 40% 100% at 100% 50%, rgba(16, 185, 129, 0.04), transparent 60%);
  pointer-events: none;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  align-items: center;
  position: relative;
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 4px 16px;
  position: relative;
  text-align: center;
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 500ms var(--ease-out-quart), transform 500ms var(--ease-out-quart);
  transition-delay: var(--delay);
}

.stat-item.visible {
  opacity: 1;
  transform: translateY(0);
}

.stat-item::after {
  content: '';
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 1px;
  height: 28px;
  background: var(--border-hairline);
}

.stat-item:last-child::after { display: none; }

.stat-number {
  font-size: 30px;
  font-weight: 600;
  letter-spacing: -0.025em;
  color: var(--text-primary);
  line-height: 1;
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  background: linear-gradient(180deg, var(--text-primary) 0%, var(--text-secondary) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-label {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px 0;
  }

  .stat-item::after { display: none; }
}

@media (max-width: 480px) {
  .stat-number { font-size: 24px; }
}

@media (prefers-reduced-motion: reduce) {
  .stat-item {
    transition: none !important;
    transform: none !important;
    opacity: 1 !important;
  }
}
</style>