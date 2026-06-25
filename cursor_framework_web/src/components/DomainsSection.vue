<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const sectionRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()

interface Domain {
  id: number
  icon: string
  title: string
  description: string
  tags: string[]
  spotlight?: boolean
}

const domains: Domain[] = [
  {
    id: 1,
    icon: 'monitor',
    title: 'Frontend',
    description: 'Next.js, Vue 3, Nuxt 4, React 19 với patterns và performance optimization',
    tags: ['Next.js', 'Vue', 'Nuxt', 'React']
  },
  {
    id: 2,
    icon: 'server',
    title: 'Backend',
    description: 'Laravel, ASP.NET Core, NestJS với clean architecture và patterns chuẩn',
    tags: ['Laravel', 'ASP.NET', 'NestJS']
  },
  {
    id: 3,
    icon: 'database',
    title: 'Database',
    description: 'MySQL, PostgreSQL, SQL Server, Redis với patterns và optimization',
    tags: ['MySQL', 'PostgreSQL', 'Redis', 'SQL Server']
  },
  {
    id: 4,
    icon: 'bot',
    title: 'AI & RAG',
    description: 'OpenAI, Gemini, Claude, pgvector, ChromaDB cho AI-powered applications',
    tags: ['OpenAI', 'Claude', 'pgvector', 'RAG']
  },
  {
    id: 5,
    icon: 'cloud',
    title: 'Cloud & DevOps',
    description: 'Cloudflare, AWS, Azure, GCP, Docker, Kubernetes, CI/CD pipelines',
    tags: ['Cloudflare', 'AWS', 'Docker', 'K8s']
  },
  {
    id: 6,
    icon: 'users',
    title: 'Business Logic',
    description: 'CRM SaaS, Multi-Tenant, Billing, Authentication, Authorization patterns',
    tags: ['CRM', 'Billing', 'Auth', 'RLS']
  },
  {
    id: 7,
    icon: 'box',
    title: 'Workflow & Events',
    description: 'Temporal, Trigger.dev, n8n, Event Sourcing, CQRS patterns',
    tags: ['Temporal', 'n8n', 'CQRS', 'Event']
  },
  {
    id: 8,
    icon: 'file',
    title: 'Bát Tự & Phong Thủy',
    description: 'Tính Bát Tự, Lá số Tử Vi, Thần Số Học — Domain đặc biệt cho ứng dụng tâm linh',
    tags: ['Bazi', 'Tử Vi', 'Numerology', 'PDF'],
    spotlight: true
  }
]

const visibleCards = ref<Set<number>>(new Set())

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      domains.forEach((_, index) => {
        setTimeout(() => {
          visibleCards.value.add(index)
        }, index * 60)
      })
    }, { threshold: 0.1 })
  }
})
</script>

<template>
  <section class="domains-section" id="domains" ref="sectionRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Supported</div>
        <h2 class="section-title">35+ Domains được hỗ trợ</h2>
        <p class="section-desc">
          Mỗi domain đi kèm bộ knowledge chuẩn hóa: Architecture, Best Practices,
          Anti-Patterns, FAQ, Checklist, Glossary. Framework bao phủ toàn bộ stack.
        </p>
      </div>

      <div class="domains-grid">
        <div
          v-for="domain in domains"
          :key="domain.id"
          class="domain-card"
          :class="{ 'domain-card-spotlight': domain.spotlight, visible: visibleCards.has(domain.id - 1) }"
        >
          <div v-if="domain.spotlight" class="domain-spotlight-badge">Spotlight</div>
          <div class="domain-icon" :class="{ spotlight: domain.spotlight }">
            <svg v-if="domain.icon === 'monitor'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
              <line x1="8" y1="21" x2="16" y2="21"/>
              <line x1="12" y1="17" x2="12" y2="21"/>
            </svg>
            <svg v-else-if="domain.icon === 'server'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="2" y="2" width="20" height="8" rx="2" ry="2"/>
              <rect x="2" y="14" width="20" height="8" rx="2" ry="2"/>
              <line x1="6" y1="6" x2="6.01" y2="6"/>
              <line x1="6" y1="18" x2="6.01" y2="18"/>
            </svg>
            <svg v-else-if="domain.icon === 'database'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <ellipse cx="12" cy="5" rx="9" ry="3"/>
              <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
              <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
            </svg>
            <svg v-else-if="domain.icon === 'bot'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 2a4 4 0 014 4c0 1.1-.9 2-2 2h-4a4 4 0 01-4-4 4 4 0 014-4m0 10c4.42 0 8 1.79 8 4v2H4v-2c0-2.21 3.58-4 8-4z"/>
            </svg>
            <svg v-else-if="domain.icon === 'cloud'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M18 10h-1.26A8 8 0 109 20h9a5 5 0 000-10z"/>
            </svg>
            <svg v-else-if="domain.icon === 'users'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>
            </svg>
            <svg v-else-if="domain.icon === 'box'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
            </svg>
          </div>
          <h4>{{ domain.title }}</h4>
          <p>{{ domain.description }}</p>
          <div class="domain-tags">
            <span v-for="tag in domain.tags" :key="tag">{{ tag }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.domains-section {
  padding: var(--section-py) 0;
}

.domains-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 14px;
  margin-top: 48px;
}

.domain-card {
  position: relative;
  padding: 24px;
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-soft);
  background: var(--bg-surface);
  transition: all var(--t-base);
  cursor: default;
  opacity: 0;
  transform: translateY(16px);
}

.domain-card.visible {
  opacity: 1;
  transform: translateY(0);
}

.domain-card:hover {
  border-color: var(--border-accent);
  transform: translateY(-3px);
  box-shadow: var(--shadow-glow);
}

.domain-card-spotlight {
  border-color: rgba(167, 139, 250, 0.2);
  background: linear-gradient(135deg, rgba(167, 139, 250, 0.04) 0%, rgba(120, 119, 232, 0.02) 100%);
}

.domain-spotlight-badge {
  position: absolute;
  top: 14px;
  right: 14px;
  font-size: 9.5px;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--accent-secondary);
  background: rgba(167, 139, 250, 0.1);
  border: 1px solid rgba(167, 139, 250, 0.2);
  padding: 3px 8px;
  border-radius: var(--radius-full);
}

.domain-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background: var(--accent-glow);
  border: 1px solid var(--border-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.domain-icon.spotlight {
  background: rgba(167, 139, 250, 0.08);
  border-color: rgba(167, 139, 250, 0.2);
}

.domain-icon svg { width: 20px; height: 20px; stroke: var(--accent-primary); }

.domain-card h4 {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
  letter-spacing: -0.01em;
}

.domain-card p {
  font-size: 12.5px;
  color: var(--text-secondary);
  line-height: 1.65;
  margin-bottom: 14px;
}

.domain-tags { display: flex; flex-wrap: wrap; gap: 5px; }

.domain-tags span {
  font-size: 10.5px;
  font-weight: 500;
  color: var(--text-muted);
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  padding: 2px 8px;
  border-radius: var(--radius-full);
  transition: all var(--t-fast);
}

.domain-card:hover .domain-tags span {
  border-color: var(--border-soft);
  color: var(--text-secondary);
}
</style>
