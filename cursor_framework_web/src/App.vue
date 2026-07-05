<script setup lang="ts">
import NavBar from './components/NavBar.vue'
import FooterSection from './components/FooterSection.vue'
</script>

<template>
  <div class="app">
    <a href="#main" class="skip-link">Skip to content</a>
    <NavBar />
    <main id="main">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
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

.page-enter-active,
.page-leave-active {
  transition: opacity 280ms cubic-bezier(0.22, 1, 0.36, 1), transform 280ms cubic-bezier(0.22, 1, 0.36, 1);
}

.page-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

@media (prefers-reduced-motion: reduce) {
  .page-enter-active,
  .page-leave-active {
    transition: none;
  }
  .page-enter-from,
  .page-leave-to {
    transform: none;
  }
}
</style>