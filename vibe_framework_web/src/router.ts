import { createRouter, createWebHashHistory } from 'vue-router'
import { defineAsyncComponent } from 'vue'
import HomeView from './views/HomeView.vue'

const TemplatesGallery = defineAsyncComponent(() => import('./views/TemplatesGallery.vue'))
const TemplatePreview = defineAsyncComponent(() => import('./views/TemplatePreview.vue'))
const LearnView = defineAsyncComponent(() => import('./views/LearnView.vue'))
const PromptsView = defineAsyncComponent(() => import('./views/PromptsView.vue'))
const InstallGuideView = defineAsyncComponent(() => import('./views/InstallGuideView.vue'))
const CmsDashboardView = defineAsyncComponent(() => import('./views/CmsDashboardView.vue'))

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
      path: '/cms',
      name: 'cms-dashboard',
      component: CmsDashboardView
    },
    {
      path: '/dashboard',
      redirect: '/cms'
    },
    {
      path: '/login',
      redirect: '/cms'
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
