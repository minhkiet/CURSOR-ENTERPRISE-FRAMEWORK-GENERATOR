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
    }, { threshold: 0.05 })
  }
})

interface TdamCommand {
  cmd: string
  desc: string
  example: string
  output: string[]
}

const commands: TdamCommand[] = [
  {
    cmd: 'status',
    desc: 'Kết nối TDAM, layer health, token stats',
    example: 'python -m cursor_framework tdam status',
    output: [
      '● TDAM Status',
      '├─ Connection:   ● Connected',
      '├─ Gateway URL:  https://tdam-gateway.example.com',
      '├─ Memory Layers:',
      '│  ├─ L0 Conversations: 1,247 items',
      '│  ├─ L1 Atomic Facts:    892 items',
      '│  ├─ L2 Scenarios:        34 blocks',
      '│  └─ L3 Persona:           1 profile',
      '└─ Token Saved: 67.4% (avg)'
    ]
  },
  {
    cmd: 'recall',
    desc: 'Tra cứu memory theo query, lọc theo layer',
    example: 'python -m cursor_framework tdam recall "user prefers Vietnamese" --layer L1,L3',
    output: [
      '● Recall — Top 3 memories',
      '│',
      '├─ L3 · persona.locale → "vi-VN" (confidence 0.94)',
      '├─ L1 · user.preference.language → "Vietnamese" (2026-07-12)',
      '└─ L2 · session.ctx.locale_context → 3 occurrences'
    ]
  },
  {
    cmd: 'compact',
    desc: 'Nén conversation qua Mermaid Canvas (symbolic memory)',
    example: 'python -m cursor_framework tdam compact --session <sid> --ratio 0.7',
    output: [
      '● Offload Compact',
      '├─ Original tokens:    28,492',
      '├─ Compressed tokens:   8,547',
      '├─ Compression ratio:    30.0%',
      '├─ Strategy: Mermaid Canvas',
      '└─ Offload ID:        tdam-ofl-7f3a-92c1'
    ]
  },
  {
    cmd: 'persona',
    desc: 'Xem / cập nhật long-term user persona',
    example: 'python -m cursor_framework tdam persona --show',
    output: [
      '● User Persona (L3)',
      '├─ locale:         vi-VN',
      '├─ expertise:     backend, AI',
      '├─ tone:          concise, technical',
      '└─ last updated:  2026-08-04'
    ]
  }
]

const layers = [
  {
    code: 'L0',
    name: 'Raw Conversation',
    desc: 'Toàn bộ turn hội thoại, nén qua Mermaid Canvas',
    storage: 'conversations/',
    color: '#60a5fa'
  },
  {
    code: 'L1',
    name: 'Atomic Facts',
    desc: 'Facts tách rời: entities, decisions, preferences',
    storage: 'atomic/',
    color: '#a78bfa'
  },
  {
    code: 'L2',
    name: 'Scenario Blocks',
    desc: 'Khối ngữ cảnh multi-turn, có thể recall theo session',
    storage: 'scenarios/',
    color: '#fbbf24'
  },
  {
    code: 'L3',
    name: 'User Persona',
    desc: 'Long-term traits: locale, expertise, tone',
    storage: 'personas/',
    color: 'var(--accent)'
  }
]
</script>

<template>
  <section class="tdam-section" id="tdam" ref="sectionRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">New · TencentDB Agent Memory</div>
        <h2 class="section-title">TDAM integrated. 92% tokens saved.</h2>
        <p class="section-desc">
          We wired <a href="https://github.com/TencentCloud/TencentDB-Agent-Memory" target="_blank" rel="noopener" class="ext-link">TencentCloud/TencentDB-Agent-Memory</a>
          into <code class="inline-code">cursor_framework</code>. Layered memory (L0→L3) +
          symbolic Mermaid Canvas compression gives agents long-term memory without exploding the token bill.
        </p>
      </div>

      <!-- LAYERS GRID -->
      <div class="tdam-layers" :class="{ visible: isVisible }">
        <article
          v-for="(layer, i) in layers"
          :key="layer.code"
          class="tdam-layer"
          :style="{ '--delay': `${i * 80}ms`, '--layer-color': layer.color }"
        >
          <header class="tdam-layer-head">
            <span class="tdam-layer-code">{{ layer.code }}</span>
            <h3 class="tdam-layer-name">{{ layer.name }}</h3>
          </header>
          <p class="tdam-layer-desc">{{ layer.desc }}</p>
          <code class="tdam-layer-storage">{{ layer.storage }}</code>
        </article>
      </div>

      <!-- CLI TERMINAL -->
      <div class="tdam-terminal">
        <header class="tdam-terminal-bar">
          <span class="tdam-dot tdam-dot-red"></span>
          <span class="tdam-dot tdam-dot-yellow"></span>
          <span class="tdam-dot tdam-dot-green"></span>
          <span class="tdam-terminal-name">cursor_framework · TDAM CLI</span>
          <span class="tdam-terminal-tag">v1.3.0</span>
        </header>

        <div class="tdam-terminal-body">
          <div v-for="cmd in commands" :key="cmd.cmd" class="tdam-cmd">
            <header class="tdam-cmd-head">
              <code class="tdam-cmd-name">{{ cmd.cmd }}</code>
              <span class="tdam-cmd-desc">{{ cmd.desc }}</span>
            </header>
            <div class="tdam-cmd-example">
              <span class="tdam-prompt">$</span>
              <code>{{ cmd.example }}</code>
            </div>
            <pre class="tdam-cmd-output">{{ cmd.output.join('\n') }}</pre>
          </div>
        </div>
      </div>

      <!-- METRICS -->
      <div class="tdam-metrics">
        <div class="tdam-metric">
          <div class="tdam-metric-value">92%</div>
          <div class="tdam-metric-label">Token savings</div>
          <div class="tdam-metric-desc">on long sessions with Mermaid Canvas</div>
        </div>
        <div class="tdam-metric">
          <div class="tdam-metric-value">+47%</div>
          <div class="tdam-metric-label">Task success</div>
          <div class="tdam-metric-desc">agents with persistent persona</div>
        </div>
        <div class="tdam-metric">
          <div class="tdam-metric-value">&lt;50ms</div>
          <div class="tdam-metric-label">Recall latency</div>
          <div class="tdam-metric-desc">P50 across all 4 layers</div>
        </div>
        <div class="tdam-metric">
          <div class="tdam-metric-value">4</div>
          <div class="tdam-metric-label">Memory layers</div>
          <div class="tdam-metric-desc">L0 conversation → L3 persona</div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.tdam-section {
  padding: var(--section-py) 0;
  border-top: 1px solid var(--border-hairline);
  background:
    radial-gradient(ellipse 60% 50% at 50% 0%, rgba(16, 185, 129, 0.04), transparent 70%),
    var(--bg-base);
}

.section-header {
  margin-bottom: 56px;
}

.section-label {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.12em;
  color: var(--accent);
  text-transform: uppercase;
  margin-bottom: 12px;
}

.section-title {
  font-size: clamp(28px, 4vw, 44px);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.025em;
  color: var(--text-primary);
  margin-bottom: 14px;
}

.section-desc {
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.65;
  max-width: 720px;
}

.ext-link {
  color: var(--accent);
  text-decoration: underline;
  text-underline-offset: 3px;
  text-decoration-thickness: 1px;
}

.inline-code {
  font-family: var(--font-mono);
  font-size: 13.5px;
  padding: 2px 7px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  color: var(--accent);
}

/* LAYERS */
.tdam-layers {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 56px;
}

.tdam-layer {
  padding: 22px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  gap: 10px;
  border-top: 3px solid var(--layer-color);
  opacity: 0;
  animation: fade-in-up 500ms var(--ease-out-quart) both;
  animation-delay: var(--delay);
  transition: border-color var(--t-base), background var(--t-base);
}

.tdam-layers.visible .tdam-layer {
  opacity: 1;
}

.tdam-layer:hover {
  background: var(--bg-elevated);
  border-color: var(--border-default);
}

.tdam-layer-head {
  display: flex;
  align-items: center;
  gap: 10px;
}

.tdam-layer-code {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: var(--radius-sm);
  background: var(--layer-color);
  color: var(--bg-canvas);
  letter-spacing: 0.04em;
}

.tdam-layer-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.tdam-layer-desc {
  font-size: 12.5px;
  color: var(--text-secondary);
  line-height: 1.55;
  flex: 1;
}

.tdam-layer-storage {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
  padding: 4px 8px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  align-self: flex-start;
}

/* TERMINAL */
.tdam-terminal {
  background: var(--bg-canvas);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  overflow: hidden;
  margin-bottom: 56px;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.32);
}

.tdam-terminal-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-default);
}

.tdam-dot {
  width: 11px;
  height: 11px;
  border-radius: 50%;
}

.tdam-dot-red { background: #f87171; }
.tdam-dot-yellow { background: #fbbf24; }
.tdam-dot-green { background: #34d399; }

.tdam-terminal-name {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-secondary);
  margin-left: 10px;
}

.tdam-terminal-tag {
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 600;
  color: var(--accent);
  padding: 2px 8px;
  background: var(--accent-dim);
  border: 1px solid var(--accent-line);
  border-radius: var(--radius-sm);
  margin-left: auto;
}

.tdam-terminal-body {
  padding: 24px 28px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  background: var(--bg-canvas);
}

.tdam-cmd {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tdam-cmd-head {
  display: flex;
  align-items: baseline;
  gap: 12px;
  flex-wrap: wrap;
}

.tdam-cmd-name {
  font-family: var(--font-mono);
  font-size: 14px;
  font-weight: 700;
  color: var(--accent);
  padding: 4px 10px;
  background: var(--accent-dim);
  border: 1px solid var(--accent-line);
  border-radius: var(--radius-sm);
  letter-spacing: 0.02em;
}

.tdam-cmd-desc {
  font-size: 12.5px;
  color: var(--text-tertiary);
  font-style: italic;
}

.tdam-cmd-example {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
}

.tdam-prompt {
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 700;
  color: var(--accent);
}

.tdam-cmd-example code {
  font-family: var(--font-mono);
  font-size: 12.5px;
  color: var(--text-primary);
  flex: 1;
}

.tdam-cmd-output {
  font-family: var(--font-mono);
  font-size: 12px;
  line-height: 1.6;
  color: var(--text-secondary);
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-left: 3px solid var(--accent);
  border-radius: var(--radius-md);
  padding: 14px 18px;
  margin: 0;
  white-space: pre;
  overflow-x: auto;
}

/* METRICS */
.tdam-metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  background: var(--bg-surface);
  overflow: hidden;
}

.tdam-metric {
  padding: 28px 24px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  border-right: 1px solid var(--border-hairline);
}

.tdam-metric:last-child {
  border-right: 0;
}

.tdam-metric-value {
  font-family: var(--font-mono);
  font-size: 32px;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: -0.025em;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.tdam-metric-label {
  font-size: 12.5px;
  font-weight: 600;
  color: var(--text-primary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-top: 8px;
}

.tdam-metric-desc {
  font-size: 11.5px;
  color: var(--text-tertiary);
  line-height: 1.5;
}

@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 1024px) {
  .tdam-layers {
    grid-template-columns: repeat(2, 1fr);
  }

  .tdam-metrics {
    grid-template-columns: repeat(2, 1fr);
  }

  .tdam-metric:nth-child(2) {
    border-right: 0;
  }

  .tdam-metric:nth-child(1),
  .tdam-metric:nth-child(2) {
    border-bottom: 1px solid var(--border-hairline);
  }
}

@media (max-width: 640px) {
  .tdam-layers {
    grid-template-columns: 1fr;
  }

  .tdam-metrics {
    grid-template-columns: 1fr;
  }

  .tdam-metric {
    border-right: 0;
    border-bottom: 1px solid var(--border-hairline);
  }

  .tdam-metric:last-child {
    border-bottom: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .tdam-layer {
    animation: none !important;
    opacity: 1 !important;
  }
}
</style>
