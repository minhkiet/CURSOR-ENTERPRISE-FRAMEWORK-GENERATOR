<script setup lang="ts">
defineProps<{ slug: string }>()
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
    />
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
</style>