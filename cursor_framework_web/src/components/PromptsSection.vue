<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

interface PromptExample {
  id: string
  type: 'skill' | 'rule'
  category: string
  icon: string
  title: string
  prompt: string
  description: string
}

const sectionRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()
const visibleItems = ref(new Set<string>())

const activeTab = ref('all')
const searchQuery = ref('')

interface TabItem {
  id: string
  label: string
  icon: string
}

const tabs: TabItem[] = [
  { id: 'all', label: 'Tất cả', icon: 'grid' },
  { id: 'skills', label: 'Skills', icon: 'zap' },
  { id: 'rules', label: 'Rules', icon: 'layers' }
]

const promptExamples: PromptExample[] = [
  // ============== SKILLS ==============
  {
    id: '1',
    type: 'skill',
    category: 'frontend-taste',
    icon: 'monitor',
    title: 'Landing Page - AI SaaS',
    prompt: 'Tạo một landing page cho startup AI SaaS với thiết kế hiện đại, minimalist, theo phong cách Linear. Sử dụng Next.js và TailwindCSS.',
    description: 'Frontend taste với anti-slop patterns, three dials (VARIANCE/MOTION/DENSITY)'
  },
  {
    id: '2',
    type: 'skill',
    category: 'frontend-taste',
    icon: 'monitor',
    title: 'Portfolio - Developer',
    prompt: 'Xây dựng portfolio cá nhân cho một senior developer với thiên hướng clean, editorial style. Sử dụng Vue 3 và GSAP animations.',
    description: 'Design read declaration, motion intensity control, premium typography'
  },
  {
    id: '3',
    type: 'skill',
    category: 'frontend-taste',
    icon: 'monitor',
    title: 'Marketing - Agency',
    prompt: 'Tạo landing page cho digital agency với phong cách bold, creative, thể hiện portfolio work. Dark theme với accent colors.',
    description: 'VARIANCE: 9, MOTION: 7, DENSITY: 3 - Bold creative design'
  },
  {
    id: '4',
    type: 'skill',
    category: 'frontend-redesign',
    icon: 'refresh',
    title: 'Redesign - Dashboard',
    prompt: 'Cải thiện dashboard hiện tại của tôi với UI dated. Nâng cấp lên modern design system mà không phá vỡ functionality.',
    description: 'Preserve functionality, upgrade visuals, audit existing state'
  },
  {
    id: '5',
    type: 'skill',
    category: 'frontend-redesign',
    icon: 'refresh',
    title: 'Redesign - E-commerce',
    prompt: 'Refresh website e-commerce cũ với modern look, better UX cho mobile, improved checkout flow. Giữ nguyên products và categories.',
    description: 'Mobile-first redesign, preserve IA, improve conversion'
  },
  {
    id: '6',
    type: 'skill',
    category: 'frontend-redesign',
    icon: 'refresh',
    title: 'Upgrade - Mobile',
    prompt: 'Cải thiện mobile experience của website hiện tại. Implement responsive breakpoints tốt hơn, touch-friendly interactions.',
    description: 'Mobile optimization, touch interactions, responsive improvement'
  },
  {
    id: '7',
    type: 'skill',
    category: 'security-review',
    icon: 'shield',
    title: 'Security - Auth Review',
    prompt: 'Review code authentication của tôi xem có vulnerability nào không. Kiểm tra SQL injection, XSS, và CSRF.',
    description: 'OWASP Top 10, input validation, authentication/authorization'
  },
  {
    id: '8',
    type: 'skill',
    category: 'security-review',
    icon: 'shield',
    title: 'Security - API Audit',
    prompt: 'Audit API endpoint của tôi về security. Kiểm tra rate limiting, CORS, và webhook signature validation.',
    description: 'API security, webhook security, rate limiting patterns'
  },
  {
    id: '9',
    type: 'skill',
    category: 'security-review',
    icon: 'shield',
    title: 'Security - JWT & Tokens',
    prompt: 'Review JWT implementation của tôi. Kiểm tra token expiration, refresh logic, và secure storage.',
    description: 'JWT security, token management, session security'
  },
  {
    id: '10',
    type: 'skill',
    category: 'security-review',
    icon: 'shield',
    title: 'Security - LLM Integration',
    prompt: 'Audit LLM integration của tôi về security. Kiểm tra prompt injection, data privacy, và output sanitization.',
    description: 'ASI Top 10, prompt injection, LLM security'
  },
  {
    id: '11',
    type: 'skill',
    category: 'full-output',
    icon: 'code',
    title: 'Full Impl - E-commerce',
    prompt: 'Implement đầy đủ một trang e-commerce với product listing, cart, checkout. Không skeleton, không TODO, full code.',
    description: 'No truncation, no placeholders, complete deliverables'
  },
  {
    id: '12',
    type: 'skill',
    category: 'full-output',
    icon: 'code',
    title: 'Full Impl - Admin Panel',
    prompt: 'Build complete admin panel với user management, role-based access, analytics dashboard. Full CRUD operations.',
    description: 'Complete admin features, RBAC, data visualization'
  },
  {
    id: '13',
    type: 'skill',
    category: 'full-output',
    icon: 'code',
    title: 'Full Impl - Social Feed',
    prompt: 'Implement social feed component với infinite scroll, real-time updates, like/comment interactions. Full code, no skeleton.',
    description: 'Real-time features, infinite scroll, social interactions'
  },
  {
    id: '14',
    type: 'skill',
    category: 'frontend-review',
    icon: 'check',
    title: 'Code Review - Quality Check',
    prompt: 'Review chất lượng code của tôi. Kiểm tra accessibility, performance, và state management.',
    description: 'Correctness, design, accessibility, performance review'
  },
  {
    id: '15',
    type: 'skill',
    category: 'frontend-review',
    icon: 'check',
    title: 'Accessibility Audit',
    prompt: 'Audit accessibility của React component. Kiểm tra WCAG compliance, keyboard navigation, screen reader support.',
    description: 'WCAG 2.1 AA, a11y, keyboard nav, ARIA'
  },
  {
    id: '16',
    type: 'skill',
    category: 'vietnam-payment-review',
    icon: 'creditcard',
    title: 'Payment - MoMo Integration',
    prompt: 'Tích hợp thanh toán MoMo vào app React. Implement webhook handler với signature validation và idempotency.',
    description: 'Vietnam payment providers, webhook security, payment flow'
  },
  {
    id: '17',
    type: 'skill',
    category: 'vietnam-payment-review',
    icon: 'creditcard',
    title: 'Payment - PayOS & VNPay',
    prompt: 'Implement thanh toán PayOS và VNPay gateway. Handle redirect payment flow, webhook confirmation, và error recovery.',
    description: 'Multi-gateway integration, payment reconciliation'
  },
  {
    id: '18',
    type: 'skill',
    category: 'vietnam-payment-review',
    icon: 'creditcard',
    title: 'Payment - SePay Banking',
    prompt: 'Tích hợp SePay cho thanh toán banking. Monitor transaction status, auto-reconcile payments, handle webhooks.',
    description: 'Banking integration, transaction monitoring, auto-reconciliation'
  },

  // ============== RULES ==============
  {
    id: '19',
    type: 'rule',
    category: 'nextjs.mdc',
    icon: 'server',
    title: 'Next.js - App Router',
    prompt: 'Xây dựng dashboard sử dụng Next.js 15 App Router với Server Components, Suspense boundaries, và proper data fetching.',
    description: 'App Router patterns, Server Components, ISR, metadata API'
  },
  {
    id: '20',
    type: 'rule',
    category: 'nextjs.mdc',
    icon: 'server',
    title: 'Next.js - SSG Blog',
    prompt: 'Tạo blog system với Next.js static generation. Implement ISR, dynamic routing, và SEO optimization.',
    description: 'Static generation, ISR, blog patterns, SEO'
  },
  {
    id: '21',
    type: 'rule',
    category: 'react.mdc',
    icon: 'code',
    title: 'React - Component Patterns',
    prompt: 'Tạo một form component với React Hook Form, Zod validation, và proper error handling. Type-safe với TypeScript.',
    description: 'React patterns, hooks, form handling, TypeScript'
  },
  {
    id: '22',
    type: 'rule',
    category: 'react.mdc',
    icon: 'code',
    title: 'React - State Management',
    prompt: 'Implement state management cho large-scale React app sử dụng Zustand. Chia state theo domain, implement persistence.',
    description: 'Zustand patterns, state persistence, domain separation'
  },
  {
    id: '23',
    type: 'rule',
    category: 'database.mdc',
    icon: 'database',
    title: 'Database - PostgreSQL',
    prompt: 'Thiết kế schema cho multi-tenant SaaS với Row Level Security. Đảm bảo tenant isolation và performance.',
    description: 'PostgreSQL patterns, RLS, multi-tenant architecture'
  },
  {
    id: '24',
    type: 'rule',
    category: 'database.mdc',
    icon: 'database',
    title: 'Database - MySQL Optimization',
    prompt: 'Optimize MySQL queries cho high-traffic application. Implement indexing strategy, query caching, và connection pooling.',
    description: 'MySQL performance, indexing, query optimization'
  },
  {
    id: '25',
    type: 'rule',
    category: 'openai.mdc',
    icon: 'bot',
    title: 'AI - RAG Implementation',
    prompt: 'Implement RAG system sử dụng OpenAI embeddings và pgvector. Chunk documents và query với semantic search.',
    description: 'OpenAI API, pgvector, RAG patterns, embeddings'
  },
  {
    id: '26',
    type: 'rule',
    category: 'openai.mdc',
    icon: 'bot',
    title: 'AI - Chat Completion',
    prompt: 'Build AI chat completion feature với streaming responses, context management, và tool use capabilities.',
    description: 'Streaming chat, context window, function calling'
  },
  {
    id: '27',
    type: 'rule',
    category: 'docker.mdc',
    icon: 'cloud',
    title: 'Docker - Container Setup',
    prompt: 'Setup Docker configuration cho Node.js app với multi-stage build, production optimization, và health checks.',
    description: 'Docker best practices, multi-stage builds, security'
  },
  {
    id: '28',
    type: 'rule',
    category: 'docker.mdc',
    icon: 'cloud',
    title: 'Docker - Compose Stack',
    prompt: 'Setup Docker Compose cho full stack: frontend, backend, database, redis, và nginx reverse proxy.',
    description: 'Multi-container setup, networking, volume management'
  },
  {
    id: '29',
    type: 'rule',
    category: 'security.mdc',
    icon: 'shield',
    title: 'Security - JWT Auth',
    prompt: 'Implement JWT authentication với refresh tokens, proper expiration, và secure storage.',
    description: 'JWT patterns, token security, authentication'
  },
  {
    id: '30',
    type: 'rule',
    category: 'security.mdc',
    icon: 'shield',
    title: 'Security - RBAC System',
    prompt: 'Implement role-based access control system với permissions, roles, và resource ownership checks.',
    description: 'RBAC patterns, permission management, access control'
  },
  {
    id: '31',
    type: 'rule',
    category: 'api.mdc',
    icon: 'layers',
    title: 'API - REST Design',
    prompt: 'Thiết kế REST API cho blog system với proper versioning, pagination, và error responses.',
    description: 'RESTful API design, versioning, best practices'
  },
  {
    id: '32',
    type: 'rule',
    category: 'api.mdc',
    icon: 'layers',
    title: 'API - GraphQL Schema',
    prompt: 'Design GraphQL schema cho e-commerce với products, orders, users. Implement resolvers, subscriptions.',
    description: 'GraphQL patterns, schema design, real-time subscriptions'
  },
  {
    id: '33',
    type: 'rule',
    category: 'performance.mdc',
    icon: 'zap',
    title: 'Performance - Optimization',
    prompt: 'Optimize Next.js app với image optimization, code splitting, và bundle analysis.',
    description: 'Core Web Vitals, bundle optimization, caching'
  },
  {
    id: '34',
    type: 'rule',
    category: 'performance.mdc',
    icon: 'zap',
    title: 'Performance - Caching',
    prompt: 'Implement caching strategy với Redis cho API responses, database queries, và session storage.',
    description: 'Redis caching, cache invalidation, performance'
  },
  {
    id: '35',
    type: 'rule',
    category: 'nestjs.mdc',
    icon: 'server',
    title: 'NestJS - Module Structure',
    prompt: 'Build NestJS application với clean module structure, dependency injection, và proper error handling.',
    description: 'NestJS architecture, modules, services, controllers'
  },
  {
    id: '36',
    type: 'rule',
    category: 'nestjs.mdc',
    icon: 'server',
    title: 'NestJS - Microservices',
    prompt: 'Implement NestJS microservices với message queue (RabbitMQ), event-driven architecture, và CQRS.',
    description: 'Microservices, message queue, event-driven patterns'
  },
  {
    id: '37',
    type: 'rule',
    category: 'laravel.mdc',
    icon: 'server',
    title: 'Laravel - API Development',
    prompt: 'Build RESTful API với Laravel với proper validation, rate limiting, và API versioning.',
    description: 'Laravel API patterns, resource controllers, form requests'
  },
  {
    id: '38',
    type: 'rule',
    category: 'laravel.mdc',
    icon: 'server',
    title: 'Laravel - Livewire Components',
    prompt: 'Implement interactive UI components với Laravel Livewire. Build real-time updates, form handling.',
    description: 'Livewire patterns, real-time UI, Alpine.js integration'
  },
  {
    id: '39',
    type: 'rule',
    category: 'redis.mdc',
    icon: 'database',
    title: 'Redis - Caching',
    prompt: 'Setup Redis caching cho high-traffic application. Implement cache-aside pattern, distributed locking.',
    description: 'Redis patterns, caching strategies, distributed systems'
  },
  {
    id: '40',
    type: 'rule',
    category: 'redis.mdc',
    icon: 'database',
    title: 'Redis - Rate Limiting',
    prompt: 'Implement rate limiting với Redis. Support sliding window, token bucket, và per-user limits.',
    description: 'Rate limiting algorithms, Redis implementation, API protection'
  },
  {
    id: '41',
    type: 'rule',
    category: 'testing.mdc',
    icon: 'check',
    title: 'Testing - Unit Tests',
    prompt: 'Write comprehensive unit tests cho business logic functions. Cover happy path và edge cases.',
    description: 'Unit testing, TDD, Jest/Vitest patterns'
  },
  {
    id: '42',
    type: 'rule',
    category: 'testing.mdc',
    icon: 'check',
    title: 'Testing - E2E Tests',
    prompt: 'Setup Playwright cho end-to-end testing. Cover critical user flows, authentication, và form submissions.',
    description: 'Playwright, E2E testing, critical user journeys'
  },
  {
    id: '43',
    type: 'rule',
    category: 'graphql.mdc',
    icon: 'layers',
    title: 'GraphQL - Schema Design',
    prompt: 'Design GraphQL API schema với proper types, relationships, và pagination. Implement DataLoader for N+1.',
    description: 'GraphQL schema, N+1 problem, DataLoader'
  },
  {
    id: '44',
    type: 'rule',
    category: 'graphql.mdc',
    icon: 'layers',
    title: 'GraphQL - Federation',
    prompt: 'Setup Apollo Federation cho microservices. Design subgraphs, implement entity references.',
    description: 'Apollo Federation, subgraph design, entity resolution'
  },
  {
    id: '45',
    type: 'rule',
    category: 'supabase.mdc',
    icon: 'database',
    title: 'Supabase - Auth Setup',
    prompt: 'Setup Supabase authentication với social logins, magic links, và Row Level Security policies.',
    description: 'Supabase auth, RLS policies, authentication'
  },
  {
    id: '46',
    type: 'rule',
    category: 'supabase.mdc',
    icon: 'database',
    title: 'Supabase - Realtime',
    prompt: 'Implement real-time features với Supabase. Broadcast presence, listen to database changes.',
    description: 'Supabase realtime, presence, live queries'
  },
  {
    id: '47',
    type: 'rule',
    category: 'git-workflow.mdc',
    icon: 'code',
    title: 'Git - Commit Convention',
    prompt: 'Setup conventional commits cho team. Implement commit linting, changelog generation.',
    description: 'Conventional commits, semantic versioning, changelog'
  },
  {
    id: '48',
    type: 'rule',
    category: 'git-workflow.mdc',
    icon: 'code',
    title: 'Git - Branching Strategy',
    prompt: 'Implement Gitflow branching strategy cho release management. Setup PR templates, code review process.',
    description: 'Gitflow, branch protection, PR workflow'
  }
]

const filteredPrompts = computed(() => {
  return promptExamples.filter(prompt => {
    const matchesTab = activeTab.value === 'all' || prompt.type === activeTab.value
    const matchesSearch = searchQuery.value === '' ||
      prompt.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      prompt.prompt.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      prompt.category.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesTab && matchesSearch
  })
})

function setTab(tabId: string) {
  activeTab.value = tabId
}

async function copyToClipboard(text: string) {
  try {
    await navigator.clipboard.writeText(text)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      promptExamples.forEach((prompt) => {
        visibleItems.value.add(prompt.id)
      })
    }, { threshold: 0.1 })
  }
})
</script>

<template>
  <section class="prompts-section" id="prompts" ref="sectionRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Examples</div>
        <h2 class="section-title">Prompt Examples</h2>
        <p class="section-desc">
          Các câu prompts ví dụ để kích hoạt skills và rules. Copy và adapt cho use case của bạn.
        </p>
      </div>

      <!-- Tabs -->
      <div class="prompts-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          class="prompt-tab"
          :class="{ active: activeTab === tab.id }"
          @click="setTab(tab.id)"
        >
          <svg v-if="tab.icon === 'grid'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
          </svg>
          <svg v-else-if="tab.icon === 'zap'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
          {{ tab.label }}
        </button>
      </div>

      <!-- Search -->
      <div class="prompts-search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/>
          <path d="M21 21l-4.35-4.35"/>
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Tìm kiếm prompt..."
        />
      </div>

      <!-- Prompts Grid -->
      <div class="prompts-grid">
        <div
          v-for="prompt in filteredPrompts"
          :key="prompt.id"
          class="prompt-card"
          :class="{ visible: visibleItems.has(prompt.id) }"
        >
          <div class="prompt-card-header">
            <div class="prompt-type-badge" :class="prompt.type">
              {{ prompt.type === 'skill' ? 'Skill' : 'Rule' }}
            </div>
            <div class="prompt-category">{{ prompt.category }}</div>
          </div>
          
          <h4 class="prompt-title">{{ prompt.title }}</h4>
          
          <div class="prompt-content">
            <div class="prompt-text">{{ prompt.prompt }}</div>
          </div>
          
          <div class="prompt-footer">
            <p class="prompt-description">{{ prompt.description }}</p>
            <button class="prompt-copy" @click="copyToClipboard(prompt.prompt)">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v9a2 2 0 01-2 2h-1"/>
              </svg>
              Copy
            </button>
          </div>
        </div>
      </div>

      <div v-if="filteredPrompts.length === 0" class="prompts-empty">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="11" cy="11" r="8"/>
          <path d="M21 21l-4.35-4.35"/>
        </svg>
        <p>Không tìm thấy prompts phù hợp</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.prompts-section {
  padding: var(--section-py) 0;
  background: var(--gradient-surface);
}

.prompts-tabs {
  display: flex;
  gap: 8px;
  margin-top: 40px;
  margin-bottom: 20px;
}

.prompt-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-soft);
  background: var(--bg-surface);
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: all var(--t-fast);
  cursor: pointer;
}

.prompt-tab svg {
  width: 15px;
  height: 15px;
}

.prompt-tab:hover {
  border-color: var(--border-default);
  color: var(--text-primary);
}

.prompt-tab.active {
  background: var(--accent-glow);
  border-color: var(--border-accent);
  color: var(--accent-primary);
}

.prompts-search {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-md);
  padding: 10px 16px;
  margin-bottom: 28px;
  max-width: 400px;
}

.prompts-search svg {
  width: 16px;
  height: 16px;
  stroke: var(--text-muted);
  flex-shrink: 0;
}

.prompts-search input {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  font-size: 13px;
  font-family: var(--font-sans);
  color: var(--text-primary);
  caret-color: var(--accent-primary);
}

.prompts-search input::placeholder {
  color: var(--text-muted);
}

.prompts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 16px;
}

.prompt-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-xl);
  padding: 20px;
  transition: all var(--t-base);
  opacity: 0;
  transform: translateY(16px);
}

.prompt-card.visible {
  opacity: 1;
  transform: translateY(0);
}

.prompt-card:hover {
  border-color: var(--border-accent);
  box-shadow: var(--shadow-glow);
}

.prompt-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.prompt-type-badge {
  font-size: 9.5px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: var(--radius-full);
}

.prompt-type-badge.skill {
  background: rgba(6, 182, 212, 0.1);
  color: #06b6d4;
  border: 1px solid rgba(6, 182, 212, 0.2);
}

.prompt-type-badge.rule {
  background: rgba(120, 119, 232, 0.1);
  color: var(--accent-primary);
  border: 1px solid rgba(120, 119, 232, 0.2);
}

.prompt-category {
  font-size: 10px;
  font-family: var(--font-mono);
  color: var(--text-faint);
  background: rgba(255, 255, 255, 0.03);
  padding: 2px 8px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border-subtle);
}

.prompt-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;
  letter-spacing: -0.01em;
}

.prompt-content {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 12px;
  margin-bottom: 14px;
}

.prompt-text {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.6;
  font-style: italic;
}

.prompt-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.prompt-description {
  font-size: 11px;
  color: var(--text-muted);
  flex: 1;
  line-height: 1.5;
}

.prompt-copy {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-soft);
  background: rgba(255, 255, 255, 0.03);
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  transition: all var(--t-fast);
  cursor: pointer;
  white-space: nowrap;
}

.prompt-copy svg {
  width: 13px;
  height: 13px;
}

.prompt-copy:hover {
  border-color: var(--border-accent);
  color: var(--accent-primary);
  background: var(--accent-glow);
}

.prompts-empty {
  text-align: center;
  padding: 60px 0;
  color: var(--text-muted);
}

.prompts-empty svg {
  width: 40px;
  height: 40px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.prompts-empty p {
  font-size: 14px;
}

@media (max-width: 768px) {
  .prompts-grid {
    grid-template-columns: 1fr;
  }
  
  .prompts-tabs {
    flex-wrap: wrap;
  }
}
</style>
