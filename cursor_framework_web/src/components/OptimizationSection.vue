<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const sectionRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()

const isVisible = ref(false)
const barWidth = ref(0)

const optimizations = [
  {
    num: '01',
    title: 'Context Router',
    description: 'Chỉ load domain cần thiết, skip 80% knowledge không liên quan'
  },
  {
    num: '02',
    title: 'Auto-Compression',
    description: 'Nén context dài tự động qua session summary'
  },
  {
    num: '03',
    title: 'Decision Memory',
    description: 'Tái sử dụng 3-10 ADRs thay vì tái tạo decision logic'
  },
  {
    num: '04',
    title: 'Bug Memory',
    description: 'Tránh lặp bug patterns đã biết, tiết kiệm 15-30% effort debugging'
  }
]

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      isVisible.value = true
      setTimeout(() => {
        barWidth.value = 60
      }, 200)
    }, { threshold: 0.3 })
  }
})
</script>

<template>
  <section class="optimization-section" ref="sectionRef">
    <div class="container">
      <div class="optimization-inner" :class="{ visible: isVisible }">
        <div class="optimization-text">
          <div class="section-label">Efficiency</div>
          <h2 class="section-title">Tiết kiệm đến <span class="text-accent">40%</span> token</h2>
          <p>
            10 chiến lược tối ưu token được implement trong framework giúp AI agent
            hoạt động hiệu quả hơn, giảm chi phí API và tăng tốc độ phản hồi.
          </p>
          <ul class="optimization-list">
            <li v-for="opt in optimizations" :key="opt.num">
              <span class="opt-num">{{ opt.num }}</span>
              <div>
                <strong>{{ opt.title }}</strong> — {{ opt.description }}
              </div>
            </li>
          </ul>
        </div>
        <div class="optimization-visual">
          <div class="token-chart">
            <div class="tc-bar-group">
              <div class="tc-bar" style="--h: 100%">
                <span class="tc-bar-label">Without CEF</span>
                <div class="tc-bar-fill"></div>
                <span class="tc-bar-val">100%</span>
              </div>
            </div>
            <div class="tc-bar-group">
              <div class="tc-bar" style="--h: 60%">
                <span class="tc-bar-label">With CEF</span>
                <div class="tc-bar-fill" :style="{ width: barWidth + '%' }"></div>
                <span class="tc-bar-val">~60%</span>
              </div>
            </div>
            <div class="tc-savings">
              <span class="tc-savings-num">~40%</span>
              <span class="tc-savings-label">Token Saved</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.optimization-section {
  padding: var(--section-py) 0;
}

.optimization-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
  padding: 48px;
  border-radius: var(--radius-2xl);
  border: 1px solid var(--border-soft);
  background: var(--bg-surface);
  position: relative;
  overflow: hidden;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s var(--ease-out), transform 0.6s var(--ease-out);
}

.optimization-inner.visible {
  opacity: 1;
  transform: translateY(0);
}

.optimization-inner::before {
  content: '';
  position: absolute;
  top: -120px;
  right: -120px;
  width: 380px;
  height: 380px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(120, 119, 232, 0.07) 0%, transparent 70%);
  pointer-events: none;
}

.optimization-text .section-title { margin-bottom: 18px; }
.optimization-text > p { font-size: 14px; color: var(--text-secondary); line-height: 1.75; margin-bottom: 28px; }

.optimization-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.optimization-list li {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.opt-num {
  font-size: 10px;
  font-weight: 800;
  color: var(--accent-primary);
  font-family: var(--font-mono);
  min-width: 22px;
  padding-top: 3px;
}

.optimization-list strong { color: var(--text-primary); font-weight: 600; }
.optimization-list div { font-size: 13px; color: var(--text-secondary); line-height: 1.55; }

/* Token chart */
.token-chart {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 12px;
}

.tc-bar-group { display: flex; flex-direction: column; gap: 4px; }

.tc-bar {
  position: relative;
  height: 34px;
  background: rgba(255, 255, 255, 0.025);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.tc-bar-label {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 11px;
  font-weight: 500;
  color: var(--text-secondary);
  z-index: 1;
}

.tc-bar-fill {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  border-radius: var(--radius-sm);
  transition: width 1.5s var(--ease-out);
}

.tc-bar-group:first-child .tc-bar-fill {
  background: linear-gradient(90deg, rgba(80, 80, 110, 0.3) 0%, rgba(80, 80, 110, 0.15) 100%);
}

.tc-bar-group:last-child .tc-bar-fill {
  background: var(--gradient-primary);
  box-shadow: 0 0 16px rgba(120, 119, 232, 0.3);
}

.tc-bar-val {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 11px;
  font-weight: 700;
  color: var(--text-primary);
  z-index: 1;
}

.tc-savings {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 20px;
  border-radius: var(--radius-lg);
  background: var(--accent-glow);
  border: 1px solid var(--border-accent);
  text-align: center;
}

.tc-savings-num {
  font-size: 38px;
  font-weight: 900;
  letter-spacing: -0.04em;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  font-family: var(--font-mono);
}

.tc-savings-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

@media (max-width: 1024px) {
  .optimization-inner {
    grid-template-columns: 1fr;
  }
}
</style>
