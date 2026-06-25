<script setup lang="ts">
import NavBar from './components/NavBar.vue'
import HeroSection from './components/HeroSection.vue'
import StatsBar from './components/StatsBar.vue'
import ExplorerSection from './components/ExplorerSection.vue'
import PrinciplesSection from './components/PrinciplesSection.vue'
import ArchitectureSection from './components/ArchitectureSection.vue'
import ComponentsSection from './components/ComponentsSection.vue'
import DomainsSection from './components/DomainsSection.vue'
import OptimizationSection from './components/OptimizationSection.vue'
import GettingStartedSection from './components/GettingStartedSection.vue'
import FooterSection from './components/FooterSection.vue'
</script>

<template>
  <div class="app">
    <NavBar />
    <main>
      <HeroSection />
      <StatsBar />
      <ExplorerSection />
      <PrinciplesSection />
      <ArchitectureSection />
      <ComponentsSection />
      <DomainsSection />
      <OptimizationSection />
      <GettingStartedSection />
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
</style>
