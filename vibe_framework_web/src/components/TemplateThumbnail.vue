<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ slug: string; alt?: string }>()

const src = computed(() => `/templates/_previews/${props.slug}.png`)
</script>

<template>
  <div class="template-thumbnail" :data-slug="slug">
    <div class="thumbnail-inner">
      <img
        class="thumbnail-svg"
        :src="src"
        :alt="alt ?? `${slug} template preview`"
        loading="lazy"
        decoding="async"
      />
    </div>
  </div>
</template>

<style scoped>
.template-thumbnail {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: #09090b;
  pointer-events: none;
  user-select: none;
}

.thumbnail-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: transform;
}

.thumbnail-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  object-position: top center;
}
</style>
