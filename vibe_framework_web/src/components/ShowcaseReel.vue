<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { templates } from '../data/templates'
import TemplateThumbnail from './TemplateThumbnail.vue'

const REEL_IDS = [
  'ui-ux',
  'cms-landing-enterprise',
  'dashboard-ui',
  'frontend-taste',
  'image-workflow',
  'viet-restaurant',
  'auto-showroom'
]

const DURATION = 5200

const items = REEL_IDS
  .map((id) => templates.find((item) => item.id === id))
  .filter((item): item is (typeof templates)[number] => Boolean(item))

const activeIndex = ref(0)
const active = computed(() => items[activeIndex.value] ?? items[0])
const progress = ref(0)
const isPlaying = ref(true)

let frameId: number | null = null
let startedAt = 0
let elapsed = 0

function clearFrame() {
  if (frameId !== null) {
    cancelAnimationFrame(frameId)
    frameId = null
  }
}

function tick(now: number) {
  if (!isPlaying.value || items.length === 0) return
  const ratio = Math.min((now - startedAt + elapsed) / DURATION, 1)
  progress.value = ratio
  if (ratio >= 1) {
    go(1)
    return
  }
  frameId = requestAnimationFrame(tick)
}

function play() {
  if (isPlaying.value || items.length === 0) return
  isPlaying.value = true
  if (elapsed >= DURATION) elapsed = 0
  startedAt = performance.now()
  clearFrame()
  frameId = requestAnimationFrame(tick)
}

function pause() {
  if (!isPlaying.value) return
  elapsed = Math.min(elapsed + (performance.now() - startedAt), DURATION)
  isPlaying.value = false
  clearFrame()
}

function togglePlay() {
  if (isPlaying.value) pause()
  else play()
}

function go(step: number) {
  if (items.length === 0) return
  activeIndex.value = (activeIndex.value + step + items.length) % items.length
  progress.value = 0
  elapsed = 0
  startedAt = performance.now()
  clearFrame()
  if (isPlaying.value) frameId = requestAnimationFrame(tick)
}

function select(index: number) {
  if (index === activeIndex.value) return
  const step = index - activeIndex.value
  go(step)
}

onMounted(() => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    isPlaying.value = false
    return
  }
  startedAt = performance.now()
  frameId = requestAnimationFrame(tick)
})

onUnmounted(clearFrame)
</script>

<template>
  <section id="showcase-reel" class="reel-section">
    <div class="container">
      <div class="reel-head">
        <div>
          <span class="reel-label">SHOWCASE / TEMPLATE REEL</span>
          <h2>Xem luồng template, không xem clip dựng sẵn</h2>
        </div>
        <p>
          Mỗi khung là preview được dựng từ template có trong repository. Chuyển cảnh để so sánh bố cục,
          màu và mức độ hoàn thiện trước khi mở bản live.
        </p>
      </div>

      <div v-if="active" class="reel-panel">
        <div class="reel-stage">
          <transition name="reel-fade">
            <div :key="active.id" class="reel-frame">
              <TemplateThumbnail :slug="active.slug" />
            </div>
          </transition>
          <span class="reel-counter">{{ String(activeIndex + 1).padStart(2, '0') }} / {{ String(items.length).padStart(2, '0') }}</span>
        </div>

        <div class="reel-toolbar">
          <div class="reel-caption">
            <span>{{ active.industry }}</span>
            <strong>{{ active.name }}</strong>
            <small>{{ active.tagline }}</small>
          </div>

          <div class="reel-controls" aria-label="Điều khiển showcase">
            <button class="reel-btn" aria-label="Template trước" @click="go(-1)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <path d="M15 18l-6-6 6-6" />
              </svg>
            </button>
            <button class="reel-btn reel-play" :aria-label="isPlaying ? 'Tạm dừng' : 'Tiếp tục'" @click="togglePlay">
              <svg v-if="isPlaying" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <rect x="7" y="5" width="3.5" height="14" rx="1" />
                <rect x="13.5" y="5" width="3.5" height="14" rx="1" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M8 5v14l11-7z" />
              </svg>
            </button>
            <button class="reel-btn" aria-label="Template tiếp theo" @click="go(1)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
                <path d="M9 18l6-6-6-6" />
              </svg>
            </button>
          </div>

          <router-link :to="`/templates/${active.id}`" class="reel-open">
            Mở live demo
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
              <path d="M7 17l9.2-9.2M17 17V7H7" />
            </svg>
          </router-link>
        </div>

        <div class="reel-progress-track" aria-hidden="true">
          <div class="reel-progress-fill" :style="{ width: `${progress * 100}%` }"></div>
        </div>

        <div class="reel-dots" role="tablist" aria-label="Chọn template">
          <button
            v-for="(item, index) in items"
            :key="item.id"
            class="reel-dot"
            :class="{ active: index === activeIndex }"
            role="tab"
            :aria-selected="index === activeIndex"
            :aria-label="item.name"
            @click="select(index)"
          ></button>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.reel-section {
  padding: var(--section-py) 0;
  border-top: 1px solid var(--border-hairline);
  background:
    radial-gradient(ellipse 70% 40% at 50% 0%, rgba(16, 185, 129, 0.045), transparent 70%),
    var(--bg-base);
}

.reel-head {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
  gap: 32px;
  align-items: end;
  margin-bottom: 28px;
}

.reel-label {
  font: 600 11px/1 var(--font-mono);
  letter-spacing: 0.1em;
  color: var(--accent);
}

.reel-head h2 {
  margin: 10px 0 0;
  max-width: 18ch;
  font-size: clamp(26px, 3.4vw, 40px);
  line-height: 1.14;
  letter-spacing: -0.03em;
  color: var(--text-primary);
}

.reel-head p {
  margin: 0;
  max-width: 58ch;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.7;
}

.reel-panel {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  overflow: hidden;
  background: var(--bg-elevated);
  box-shadow: var(--shadow-lg);
}

.reel-stage {
  position: relative;
  aspect-ratio: 16 / 7.6;
  background: #08090d;
}

.reel-frame {
  position: absolute;
  inset: 0;
}

.reel-counter {
  position: absolute;
  right: 14px;
  top: 14px;
  padding: 5px 9px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--radius-sm);
  background: rgba(5, 7, 12, 0.72);
  color: #cbd5e1;
  font: 600 10px/1 var(--font-mono);
  letter-spacing: 0.05em;
}

.reel-fade-enter-active,
.reel-fade-leave-active {
  transition: opacity 360ms var(--ease-out-quart), transform 360ms var(--ease-out-quart);
}

.reel-fade-enter-from {
  opacity: 0;
  transform: scale(1.012);
}

.reel-fade-leave-to {
  opacity: 0;
  transform: scale(0.994);
}

.reel-toolbar {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 16px 20px;
  border-top: 1px solid var(--border-hairline);
  background: var(--bg-surface);
}

.reel-caption {
  display: flex;
  align-items: baseline;
  gap: 10px;
  min-width: 0;
  flex: 1;
}

.reel-caption span {
  color: var(--accent);
  font: 600 10px/1 var(--font-mono);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.reel-caption strong {
  color: var(--text-primary);
  font-size: 13.5px;
  white-space: nowrap;
}

.reel-caption small {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--text-tertiary);
  font-size: 11.5px;
}

.reel-controls {
  display: flex;
  align-items: center;
  gap: 6px;
}

.reel-btn {
  width: 30px;
  height: 30px;
  display: grid;
  place-items: center;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  background: var(--bg-elevated);
  color: var(--text-secondary);
  cursor: pointer;
  transition: border-color 180ms, color 180ms, transform 180ms;
}

.reel-btn svg {
  width: 14px;
  height: 14px;
}

.reel-btn:hover {
  color: var(--accent);
  border-color: var(--accent-line);
}

.reel-btn:active {
  transform: translateY(1px);
}

.reel-play {
  color: var(--bg-base);
  background: var(--accent);
  border-color: var(--accent);
}

.reel-play:hover {
  color: var(--bg-base);
  filter: brightness(1.08);
}

.reel-open {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--text-secondary);
  font-size: 12px;
  text-decoration: none;
  transition: color 180ms;
}

.reel-open svg {
  width: 13px;
  height: 13px;
}

.reel-open:hover {
  color: var(--accent);
}

.reel-progress-track {
  height: 2px;
  background: var(--border-subtle);
}

.reel-progress-fill {
  height: 100%;
  background: var(--accent);
  transition: width 80ms linear;
}

.reel-dots {
  display: flex;
  justify-content: center;
  gap: 6px;
  padding: 10px;
  background: var(--bg-surface);
}

.reel-dot {
  width: 18px;
  height: 3px;
  padding: 0;
  border: 0;
  border-radius: 2px;
  background: var(--border-default);
  cursor: pointer;
  transition: background 180ms, width 180ms;
}

.reel-dot.active {
  width: 34px;
  background: var(--accent);
}

@media (max-width: 760px) {
  .reel-head {
    grid-template-columns: 1fr;
    gap: 14px;
  }

  .reel-head h2 {
    max-width: none;
  }

  .reel-stage {
    aspect-ratio: 16 / 11;
  }

  .reel-toolbar {
    flex-wrap: wrap;
    gap: 12px;
  }

  .reel-caption {
    flex-basis: 100%;
  }

  .reel-caption small {
    display: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .reel-fade-enter-active,
  .reel-fade-leave-active,
  .reel-progress-fill,
  .reel-dot,
  .reel-btn {
    transition: none !important;
  }
}
</style>
