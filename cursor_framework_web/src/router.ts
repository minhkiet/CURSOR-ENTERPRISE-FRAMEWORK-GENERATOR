import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import TemplatesGallery from './views/TemplatesGallery.vue'
import TemplatePreview from './views/TemplatePreview.vue'

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
    }
  ],
  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, top: 60, behavior: 'smooth' }
    return { top: 0 }
  }
})

export default router