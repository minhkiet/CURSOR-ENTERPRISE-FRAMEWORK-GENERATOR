<script setup lang="ts">
import NavBar from './components/NavBar.vue'
import FooterSection from './components/FooterSection.vue'
</script>

<template>
  <div class="app">
    <a href="#main" class="skip-link">Skip to content</a>
    <NavBar />
    <main id="main">
      <router-view v-slot="{ Component, route }">
        <component :is="Component" :key="route.fullPath" />
      </router-view>
    </main>
    <FooterSection />
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

.skip-link {
  position: absolute;
  top: -40px;
  left: 12px;
  padding: 8px 14px;
  background: var(--text-primary);
  color: var(--bg-canvas);
  border-radius: var(--radius-md);
  font-size: 12px;
  font-weight: 500;
  text-decoration: none;
  z-index: 100;
  transition: top var(--t-fast);
}

.skip-link:focus {
  top: 12px;
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
</style>