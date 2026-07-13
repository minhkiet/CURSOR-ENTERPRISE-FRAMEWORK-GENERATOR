import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import TemplatesGallery from './views/TemplatesGallery.vue'
import TemplatePreview from './views/TemplatePreview.vue'
import LearnView from './views/LearnView.vue'
import PromptsView from './views/PromptsView.vue'
import InstallGuideView from './views/InstallGuideView.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/templates',
      name: 'templates',
      component: TemplatesGallery
    },
    {
      path: '/templates/:id',
      name: 'template-preview',
      component: TemplatePreview
    },
    {
      path: '/learn',
      name: 'learn',
      component: LearnView
    },
    {
      path: '/prompts',
      name: 'prompts',
      component: PromptsView
    },
    {
      path: '/install',
      name: 'install',
      component: InstallGuideView
    }
  ],
  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, top: 60, behavior: 'smooth' }
    return { top: 0 }
  }
})

export default router