<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const statsBarRef = ref<HTMLElement | null>(null)
const isVisible = ref(false)

const stats = [
  { target: 668, label: 'Files', sublabel: '668 total in framework' },
  { target: 40, label: 'Rules', sublabel: 'MDC rules & principles' },
  { target: 17, label: 'Skills', sublabel: 'Specialized expertise' },
  { target: 36, label: 'Knowledge', sublabel: 'Directories across domains' },
  { target: 12, label: 'Scripts', sublabel: 'Automation & build tools' }
]

const displayValues = ref(stats.map(() => 0))

const { observe } = useIntersectionObserver()

function animateCounter(index: number, target: number, duration: number = 1800) {
  const startTime = performance.now()
  const easeOutExpo = (t: number) => t === 1 ? 1 : 1 - Math.pow(2, -10 * t)

  const update = (currentTime: number) => {
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)
    const easedProgress = easeOutExpo(progress)
    const current = Math.round(easedProgress * target)
    displayValues.value[index] = current

    if (progress < 1) {
      requestAnimationFrame(update)
    }
  }

  requestAnimationFrame(update)
}

onMounted(() => {
  if (statsBarRef.value) {
    observe(statsBarRef.value, () => {
      isVisible.value = true
      stats.forEach((stat, index) => {
        animateCounter(index, stat.target)
      })
    }, { threshold: 0.3 })
  }
})
</script>

<template>
  <section class="stats-bar" ref="statsBarRef">
    <div class="container">
      <div class="stats-grid">
        <div v-for="(stat, index) in stats" :key="stat.label" class="stat-item">
          <span class="stat-number">{{ displayValues[index] }}</span>
          <span class="stat-suffix">+</span>
          <span class="stat-label">{{ stat.label }}</span>
          <span class="stat-sublabel">{{ stat.sublabel }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.stats-grid {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 0 52px;
  text-align: center;
  position: relative;
}

.stat-item::after {
  content: '';
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 1px;
  height: 40px;
  background: var(--border-subtle);
}

.stat-item:last-child::after {
  display: none;
}

.stat-number {
  font-size: 34px;
  font-weight: 900;
  letter-spacing: -0.04em;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  font-family: var(--font-mono);
}

.stat-suffix {
  font-size: 22px;
  font-weight: 900;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-left: -6px;
  font-family: var(--font-mono);
}

.stat-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--text-primary);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-top: 6px;
}

.stat-sublabel {
  font-size: 10.5px;
  color: var(--text-muted);
}

@media (max-width: 768px) {
  .stats-grid {
    gap: 20px;
  }

  .stat-item {
    padding: 0 24px;
  }

  .stat-item::after {
    display: none;
  }
}
</style>
