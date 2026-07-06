<script setup lang="ts">
import { computed } from 'vue'
import { templates } from '../data/templates'

const props = defineProps<{ slug: string }>()

const template = computed(() => templates.find((t) => t.slug === props.slug))
</script>

<template>
  <div class="miniature">
    <img
      :src="`/templates/_previews/${slug}.png`"
      :alt="`${slug} template preview`"
      class="miniature-img"
      loading="lazy"
      decoding="async"
      draggable="false"
      @error="($event.target as HTMLImageElement).style.display = 'none'"
    />
    <svg
      v-if="template"
      class="miniature-fallback"
      viewBox="0 0 320 200"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      <defs>
        <linearGradient :id="`g-${slug}`" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" :stop-color="template.accent" stop-opacity="0.95" />
          <stop offset="100%" stop-color="#0a0a0f" stop-opacity="1" />
        </linearGradient>
      </defs>
      <rect width="320" height="200" :fill="`url(#g-${slug})`" />
      <!-- mock browser chrome -->
      <rect x="0" y="0" width="320" height="22" fill="rgba(0,0,0,0.4)" />
      <circle cx="10" cy="11" r="2.5" fill="#ef4444" opacity="0.7" />
      <circle cx="20" cy="11" r="2.5" fill="#eab308" opacity="0.7" />
      <circle cx="30" cy="11" r="2.5" fill="#22c55e" opacity="0.7" />
      <!-- mock hero -->
      <rect x="20" y="50" width="120" height="6" rx="2" fill="rgba(255,255,255,0.85)" />
      <rect x="20" y="62" width="160" height="14" rx="3" fill="rgba(255,255,255,0.95)" />
      <rect x="20" y="82" width="140" height="14" rx="3" fill="rgba(255,255,255,0.95)" />
      <rect x="20" y="106" width="200" height="4" rx="2" fill="rgba(255,255,255,0.5)" />
      <rect x="20" y="116" width="180" height="4" rx="2" fill="rgba(255,255,255,0.4)" />
      <rect x="20" y="138" width="60" height="18" rx="4" :fill="template.accentSecondary" />
      <!-- mock card right -->
      <rect x="200" y="50" width="100" height="130" rx="6" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.2)" />
      <rect x="208" y="58" width="84" height="40" rx="3" fill="rgba(255,255,255,0.15)" />
      <rect x="208" y="104" width="60" height="4" rx="2" fill="rgba(255,255,255,0.6)" />
      <rect x="208" y="114" width="84" height="4" rx="2" fill="rgba(255,255,255,0.4)" />
      <rect x="208" y="124" width="84" height="4" rx="2" fill="rgba(255,255,255,0.4)" />
      <!-- label -->
      <text x="20" y="190" fill="rgba(255,255,255,0.7)" font-family="monospace" font-size="9" font-weight="600" letter-spacing="0.05em">
        {{ template.industry }}
      </text>
    </svg>
  </div>
</template>

<style scoped>
.miniature {
  position: absolute;
  inset: 0;
  overflow: hidden;
  background: #09090b;
  pointer-events: none;
}
.miniature-img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: top center;
  user-select: none;
  -webkit-user-drag: none;
}
.miniature-fallback {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}
</style>