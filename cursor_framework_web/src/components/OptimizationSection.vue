<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const sectionRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()

const isVisible = ref(false)

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      isVisible.value = true
    }, { threshold: 0.1 })
  }
})

const bars = [
  { label: 'Baseline agent', before: 100, after: 100, color: 'var(--text-faint)' },
  { label: 'With memory retrieval', before: 100, after: 78, color: '#60a5fa' },
  { label: 'With context router', before: 100, after: 64, color: '#a78bfa' },
  { label: 'With token optimization', before: 100, after: 47, color: 'var(--accent)' }
]

const metrics = [
  { value: '47.2%', label: 'Tokens saved', desc: 'Per complex multi-step task' },
  { value: '2.8×', label: 'Retrieval accuracy', desc: 'vs naive full-context' },
  { value: '$0.31', label: 'Avg cost / task', desc: 'GPT-4o class models' },
  { value: '34ms', label: 'P50 retrieval', desc: 'In-memory SQLite + vector' }
]
</script>

<template>
  <section class="optimization-section" id="optimization" ref="sectionRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Optimization</div>
        <h2 class="section-title">Less context. Better results.</h2>
        <p class="section-desc">
          The framework actively reduces token waste. Memory beats re-reading. Cached skills
          beat repeated lookups. Real numbers from production workloads, not marketing.
        </p>
      </div>

      <div class="opt-grid">
        <div class="opt-bars" :class="{ visible: isVisible }">
          <div class="opt-bars-head">
            <span class="opt-bars-title">Token usage per session</span>
            <span class="opt-bars-legend">vs baseline</span>
          </div>
          <div
            v-for="(bar, i) in bars"
            :key="bar.label"
            class="opt-bar-row"
            :class="{ visible: isVisible }"
            :style="{ '--delay': `${i * 120}ms`, '--width': `${bar.after}%`, '--color': bar.color }"
          >
            <div class="opt-bar-label">
              <span>{{ bar.label }}</span>
              <span class="opt-bar-amount">{{ bar.after }}%</span>
            </div>
            <div class="opt-bar-track">
              <div class="opt-bar-fill"></div>
            </div>
          </div>
        </div>

        <div class="opt-metrics">
          <div
            v-for="(metric, i) in metrics"
            :key="metric.label"
            class="opt-metric"
            :style="{ '--delay': `${i * 80}ms` }"
          >
            <div class="opt-metric-value">{{ metric.value }}</div>
            <div class="opt-metric-label">{{ metric.label }}</div>
            <div class="opt-metric-desc">{{ metric.desc }}</div>
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

.opt-grid {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 12px;
}

.opt-bars, .opt-metrics {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  padding: 28px;
}

.opt-bars {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.opt-bars-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border-hairline);
}

.opt-bars-title {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
}

.opt-bars-legend {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
}

.opt-bar-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
  opacity: 0;
  animation: fade-in-up 500ms var(--ease-out-quart) both;
  animation-delay: var(--delay);
}

.opt-bars.visible .opt-bar-row {
  opacity: 1;
}

.opt-bar-label {
  font-size: 12.5px;
  color: var(--text-secondary);
  font-weight: 500;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.opt-bar-amount {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
  font-variant-numeric: tabular-nums;
}

.opt-bar-track {
  height: 28px;
  background: var(--bg-elevated);
  border-radius: var(--radius-sm);
  overflow: hidden;
  border: 1px solid var(--border-hairline);
  position: relative;
}

.opt-bar-fill {
  height: 100%;
  width: 0;
  background: var(--color);
  border-radius: var(--radius-sm);
  transition: width 1.2s var(--ease-out-quart);
  transition-delay: var(--delay);
  position: relative;
  overflow: hidden;
}

.opt-bar-row.visible .opt-bar-fill {
  width: var(--width);
}

.opt-bar-fill::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.18) 50%,
    transparent 100%
  );
  transform: translateX(-100%);
  animation: shimmer-bar 2.4s ease-in-out infinite;
  animation-delay: calc(var(--delay) + 1.2s);
}

.opt-bar-row:last-child .opt-bar-fill {
  background: linear-gradient(90deg, var(--accent), var(--accent-bright));
  position: relative;
}

.opt-bar-row:last-child .opt-bar-fill::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.25) 50%,
    transparent 100%
  );
  animation: shimmer-pulse 2.4s ease-in-out infinite;
}

@keyframes shimmer-bar {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

@keyframes shimmer-pulse {
  0%, 100% { opacity: 0; }
  50% { opacity: 1; }
}

.opt-metrics {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
}

.opt-metric {
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  border-right: 1px solid var(--border-hairline);
  border-bottom: 1px solid var(--border-hairline);
  opacity: 0;
  animation: fade-in-up 500ms var(--ease-out-quart) both;
  animation-delay: var(--delay);
}

.opt-metric:nth-child(2n) {
  border-right: 0;
}

.opt-metric:nth-last-child(-n+2) {
  border-bottom: 0;
}

.opt-metric-value {
  font-family: var(--font-mono);
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  font-variant-numeric: tabular-nums;
}

.opt-metric-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-primary);
  margin-top: 2px;
}

.opt-metric-desc {
  font-size: 11px;
  color: var(--text-tertiary);
  margin-top: 2px;
}

@media (max-width: 1024px) {
  .opt-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .opt-metrics {
    grid-template-columns: 1fr;
  }
  .opt-metric {
    border-right: 0;
  }
  .opt-metric:not(:last-child) {
    border-bottom: 1px solid var(--border-hairline);
  }
}

@media (prefers-reduced-motion: reduce) {
  .opt-bar-fill {
    transition: none !important;
    width: var(--width) !important;
  }
  .opt-bar-fill::after,
  .opt-bar-row:last-child .opt-bar-fill::before {
    animation: none !important;
  }
}
</style>