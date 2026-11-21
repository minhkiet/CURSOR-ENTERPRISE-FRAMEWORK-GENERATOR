<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { templates } from '../data/templates'
import TemplateThumbnail from '../components/TemplateThumbnail.vue'

interface FlowNode {
  id: string
  label: string
  tag: string
  title: string
  desc: string
  checks: string[]
}

const flowNodes: FlowNode[] = [
  {
    id: 'input',
    label: 'Input',
    tag: '01 / CONTEXT',
    title: 'Bắt đầu từ yêu cầu có ngữ cảnh',
    desc: 'Prompt, ảnh chụp màn hình hoặc asset có sẵn được đưa vào đúng workspace. Không cần đoán ý từ một câu lệnh ngắn.',
    checks: ['prompt / screenshot / asset', 'workspace rõ ràng', 'mục tiêu đầu ra']
  },
  {
    id: 'router',
    label: 'Router',
    tag: '02 / ROUTING',
    title: 'Chỉ nạp đúng phần cần dùng',
    desc: 'Rule, skill và domain knowledge được chọn theo tác vụ. Phần không liên quan đứng yên, giúp giảm nhiễu và giữ token cho việc quan trọng.',
    checks: ['rule theo domain', 'skill theo intent', 'memory theo dự án']
  },
  {
    id: 'build',
    label: 'Build',
    tag: '03 / EXECUTION',
    title: 'Thi hành theo contract, không đoán',
    desc: 'Agent nhận đầu việc nhỏ, enum rõ ràng và tiêu chí nghiệm thu. Gate trước/sau giữ changelog, test và scope không bị trôi.',
    checks: ['task atom', 'pre / post gate', 'diff có thể review']
  },
  {
    id: 'verify',
    label: 'Verify',
    tag: '04 / DELIVERY',
    title: 'Chỉ bàn giao khi có bằng chứng',
    desc: 'Build, test và review là một phần của luồng. Kết quả bàn giao kèm lệnh đã chạy, file đã đổi và phần còn biết trước.',
    checks: ['build / test / review', 'edge case có ghi chú', 'handoff ngắn gọn']
  }
]

const activeNodeId = ref('router')
const activeNode = computed(() => flowNodes.find((n) => n.id === activeNodeId.value) ?? flowNodes[0])

const featuredIds = ['ui-ux', 'cms-landing-enterprise', 'dashboard-ui']
const featured = computed(() =>
  featuredIds
    .map((id) => templates.find((t) => t.id === id))
    .filter((t): t is (typeof templates)[number] => Boolean(t))
)

const facts = computed(() => [
  { value: String(templates.length), label: 'Templates trong repo' },
  { value: '6', label: 'Theme modes' },
  { value: '10+', label: 'Vibe code tools' },
  { value: 'MIT', label: 'License' }
])

const heroRef = ref<HTMLElement | null>(null)
const isVisible = ref(false)
let observer: IntersectionObserver | null = null

function smoothScroll(href: string) {
  const target = document.querySelector(href)
  if (!target) return
  const top = target.getBoundingClientRect().top + window.scrollY - 64
  window.scrollTo({ top, behavior: 'smooth' })
}

onMounted(() => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !heroRef.value) {
    isVisible.value = true
    return
  }
  observer = new IntersectionObserver(
    (entries) => {
      if (entries.some((entry) => entry.isIntersecting)) {
        isVisible.value = true
        observer?.disconnect()
      }
    },
    { threshold: 0.06 }
  )
  observer.observe(heroRef.value)
})

onUnmounted(() => observer?.disconnect())
</script>

<template>
  <section ref="heroRef" class="hero" :class="{ visible: isVisible }">
    <div class="hero-bg" aria-hidden="true">
      <div class="hero-gridlines"></div>
    </div>

    <div class="container hero-layout">
      <div class="hero-copy">
        <div class="hero-eyebrow">
          <span class="hero-signal"></span>
          <span>OPEN SOURCE · MIT · FRAMEWORK 2026</span>
        </div>

        <h1 class="hero-title">
          Vibe code có cấu trúc.<br />
          <span>Bàn giao được production.</span>
        </h1>

        <p class="hero-sub">
          Rule, skill, agent và template được xếp thành một luồng rõ ràng. Router chỉ nạp ngữ cảnh
          cần thiết; gate kiểm tra trước khi bàn giao. Dùng được trên Cursor, Codex, Claude Code,
          Windsurf và các tool vibe code khác.
        </p>

        <div class="hero-actions">
          <button class="btn btn-primary" @click="smoothScroll('#getting-started')">
            Xem hướng dẫn setup
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
              <path d="M5 12h14M13 6l6 6-6 6" />
            </svg>
          </button>
          <router-link to="/templates" class="btn btn-secondary">Kho templates</router-link>
          <button class="hero-reel-link" @click="smoothScroll('#showcase-reel')">Xem demo reel</button>
        </div>

        <dl class="hero-facts">
          <div v-for="fact in facts" :key="fact.label" class="hero-fact">
            <dt>{{ fact.value }}</dt>
            <dd>{{ fact.label }}</dd>
          </div>
        </dl>
      </div>

      <div class="hero-board">
        <div class="board-head">
          <div class="board-head-left">
            <span class="board-mark">VF</span>
            <span class="board-title">framework / flow</span>
          </div>
          <span class="board-badge">local-first · repo-driven</span>
        </div>

        <div class="flow-rail" role="tablist" aria-label="Luồng thực thi framework">
          <button
            v-for="(node, index) in flowNodes"
            :key="node.id"
            class="flow-node"
            :class="{ active: activeNodeId === node.id }"
            role="tab"
            :aria-selected="activeNodeId === node.id"
            @click="activeNodeId = node.id"
          >
            <span class="flow-index">0{{ index + 1 }}</span>
            <span class="flow-label">{{ node.label }}</span>
          </button>
        </div>

        <div class="flow-detail" aria-live="polite">
          <div class="flow-detail-copy">
            <span class="flow-tag">{{ activeNode.tag }}</span>
            <h2>{{ activeNode.title }}</h2>
            <p>{{ activeNode.desc }}</p>
          </div>
          <ul class="flow-checks">
            <li v-for="check in activeNode.checks" :key="check">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true">
                <polyline points="20 6 9 17 4 12" />
              </svg>
              {{ check }}
            </li>
          </ul>
        </div>

        <div class="board-previews">
          <router-link
            v-for="item in featured"
            :key="item.id"
            :to="`/templates/${item.id}`"
            class="board-preview"
            :title="`Mở ${item.name}`"
          >
            <TemplateThumbnail :slug="item.slug" />
            <span>{{ item.name }}</span>
          </router-link>
        </div>

        <div class="board-foot">
          <span>Preview dựng từ template có trong repo — không phải ảnh AI.</span>
          <span>build · test · review</span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  position: relative;
  min-height: calc(100vh - 60px);
  display: flex;
  align-items: center;
  padding: 104px 0 72px;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: var(--gradient-hero);
}

.hero-gridlines {
  position: absolute;
  inset: -15% -10%;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.024) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.024) 1px, transparent 1px);
  background-size: 64px 64px;
  mask-image: radial-gradient(ellipse 62% 74% at 70% 22%, #000 15%, transparent 76%);
  -webkit-mask-image: radial-gradient(ellipse 62% 74% at 70% 22%, #000 15%, transparent 76%);
}

.hero-layout {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 0.92fr) minmax(480px, 1.08fr);
  gap: clamp(36px, 5vw, 76px);
  align-items: center;
}

.hero-copy > * {
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 600ms var(--ease-out-quart), transform 600ms var(--ease-out-quart);
}

.hero.visible .hero-copy > * {
  opacity: 1;
  transform: translateY(0);
}

.hero.visible .hero-copy > :nth-child(2) { transition-delay: 60ms; }
.hero.visible .hero-copy > :nth-child(3) { transition-delay: 120ms; }
.hero.visible .hero-copy > :nth-child(4) { transition-delay: 180ms; }
.hero.visible .hero-copy > :nth-child(5) { transition-delay: 240ms; }

.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: fit-content;
  padding: 5px 11px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-pill);
  background: var(--bg-surface);
  color: var(--text-secondary);
  font: 500 11px/1 var(--font-mono);
  letter-spacing: 0.04em;
}

.hero-signal {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 8px var(--accent-glow);
}

.hero-title {
  margin: 22px 0 20px;
  font-size: clamp(38px, 4.6vw, 64px);
  line-height: 1.06;
  letter-spacing: -0.045em;
  font-weight: 650;
  color: var(--text-primary);
}

.hero-title span {
  color: var(--accent);
}

.hero-sub {
  max-width: 55ch;
  margin: 0 0 30px;
  color: var(--text-secondary);
  font-size: 15.5px;
  line-height: 1.7;
}

.hero-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 38px;
}

.hero-actions .btn svg {
  width: 15px;
  height: 15px;
}

.hero-reel-link {
  padding: 8px 4px;
  background: none;
  border: 0;
  color: var(--text-secondary);
  font: 500 13px/1.4 inherit;
  text-decoration: underline;
  text-underline-offset: 4px;
  text-decoration-color: var(--border-default);
  cursor: pointer;
}

.hero-reel-link:hover {
  color: var(--accent);
  text-decoration-color: var(--accent-line);
}

.hero-facts {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin: 0;
  padding-top: 24px;
  border-top: 1px solid var(--border-hairline);
}

.hero-fact dt {
  font: 600 21px/1 var(--font-mono);
  color: var(--text-primary);
}

.hero-fact dd {
  margin: 7px 0 0;
  color: var(--text-tertiary);
  font-size: 10.5px;
  line-height: 1.35;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.hero-board {
  position: relative;
  padding: 18px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  background: var(--bg-elevated);
  box-shadow: var(--shadow-lg);
  opacity: 0;
  transform: translateY(14px);
  transition: opacity 700ms var(--ease-out-quart) 180ms, transform 700ms var(--ease-out-quart) 180ms;
}

.hero.visible .hero-board {
  opacity: 1;
  transform: translateY(0);
}

.hero-board::before {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: inherit;
  background: linear-gradient(125deg, var(--accent-line), transparent 38%);
  pointer-events: none;
}

.board-head,
.board-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.board-head {
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border-hairline);
}

.board-head-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.board-mark {
  width: 26px;
  height: 26px;
  display: grid;
  place-items: center;
  border-radius: var(--radius-sm);
  background: var(--accent);
  color: var(--bg-base);
  font: 800 11px/1 var(--font-mono);
}

.board-title,
.board-badge,
.board-foot {
  font: 500 10.5px/1.4 var(--font-mono);
  color: var(--text-tertiary);
}

.board-badge {
  padding: 4px 8px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-pill);
}

.flow-rail {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
  margin: 16px 0 12px;
}

.flow-node {
  position: relative;
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 10px 8px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
  color: var(--text-secondary);
  font: 600 12px/1 inherit;
  cursor: pointer;
  transition: transform 180ms var(--ease-out-quart), border-color 180ms, color 180ms, background 180ms;
}

.flow-node:hover {
  transform: translateY(-2px);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.flow-node.active {
  border-color: var(--accent-line);
  background: var(--accent-dim);
  color: var(--accent);
}

.flow-index {
  font: 600 9.5px/1 var(--font-mono);
  color: var(--text-faint);
}

.flow-node.active .flow-index {
  color: var(--accent);
}

.flow-detail {
  display: grid;
  grid-template-columns: 1.35fr 0.9fr;
  gap: 16px;
  padding: 18px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  background: var(--bg-surface);
}

.flow-tag {
  font: 600 10px/1 var(--font-mono);
  letter-spacing: 0.06em;
  color: var(--accent);
}

.flow-detail h2 {
  margin: 9px 0 8px;
  color: var(--text-primary);
  font-size: 16px;
  line-height: 1.35;
  letter-spacing: -0.015em;
}

.flow-detail p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 12.5px;
  line-height: 1.6;
}

.flow-checks {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 8px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.flow-checks li {
  display: flex;
  align-items: flex-start;
  gap: 7px;
  color: var(--text-secondary);
  font: 500 11px/1.45 var(--font-mono);
}

.flow-checks svg {
  width: 13px;
  height: 13px;
  flex: 0 0 auto;
  color: var(--accent);
}

.board-previews {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
  margin-top: 12px;
}

.board-preview {
  position: relative;
  display: block;
  aspect-ratio: 16 / 10;
  overflow: hidden;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: #09090b;
}

.board-preview :deep(.thumbnail-inner) {
  transition: transform 420ms var(--ease-out-quart);
}

.board-preview:hover :deep(.thumbnail-inner) {
  transform: scale(1.04);
}

.board-preview span {
  position: absolute;
  inset: auto 0 0;
  padding: 16px 8px 7px;
  background: linear-gradient(transparent, rgba(4, 6, 10, 0.92));
  color: #e8f5ef;
  font: 600 10px/1.2 var(--font-mono);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.board-foot {
  padding-top: 12px;
}

.board-foot span:last-child {
  color: var(--accent);
}

@media (max-width: 1080px) {
  .hero {
    min-height: auto;
  }

  .hero-layout {
    grid-template-columns: 1fr;
  }

  .hero-board {
    max-width: 680px;
    width: 100%;
    margin: 0 auto;
  }
}

@media (max-width: 680px) {
  .hero {
    padding: 92px 0 56px;
  }

  .hero-actions .btn {
    flex: 1 1 180px;
    justify-content: center;
  }

  .hero-facts {
    grid-template-columns: repeat(2, 1fr);
    row-gap: 20px;
  }

  .flow-rail {
    grid-template-columns: repeat(2, 1fr);
  }

  .flow-detail {
    grid-template-columns: 1fr;
  }

  .board-previews {
    grid-template-columns: 1fr;
  }

  .board-foot {
    align-items: flex-start;
    flex-direction: column;
  }
}

@media (prefers-reduced-motion: reduce) {
  .hero-copy > *,
  .hero-board,
  .flow-node,
  .board-preview :deep(.thumbnail-inner) {
    transition: none !important;
    transform: none !important;
    opacity: 1 !important;
  }
}
</style>
