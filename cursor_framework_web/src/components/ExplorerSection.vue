<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

interface RuleItem {
  id: string
  name: string
  domain: string
  tags: string[]
  icon: string
}

interface SkillItem {
  id: string
  name: string
  platform: string
  initials: string
  category: string
}

const explorerRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()
const visibleItems = ref(new Set<string>())

const activeCategory = ref('all')
const activeFilter = ref('all')
const searchQuery = ref('')

const rules: RuleItem[] = [
  { id: 'r1', name: 'core-architecture.mdc', domain: 'core', tags: ['architecture', 'foundation'], icon: 'layers' },
  { id: 'r2', name: 'memory-first.mdc', domain: 'core', tags: ['memory', 'context'], icon: 'grid' },
  { id: 'r3', name: 'context-router.mdc', domain: 'core', tags: ['routing', 'intelligence'], icon: 'search' },
  { id: 'r4', name: 'token-optimization.mdc', domain: 'core', tags: ['tokens', 'efficiency'], icon: 'zap' },
  { id: 'r5', name: 'coding-standards.mdc', domain: 'core', tags: ['code', 'conventions'], icon: 'code' },
  { id: 'r6', name: 'nextjs.mdc', domain: 'frontend', tags: ['next.js', 'react'], icon: 'monitor' },
  { id: 'r7', name: 'vue.mdc', domain: 'frontend', tags: ['vue', 'nuxt'], icon: 'monitor' },
  { id: 'r8', name: 'react.mdc', domain: 'frontend', tags: ['react', 'hooks'], icon: 'monitor' },
  { id: 'r9', name: 'aspnet-core.mdc', domain: 'backend', tags: ['.net', 'api'], icon: 'server' },
  { id: 'r10', name: 'nestjs.mdc', domain: 'backend', tags: ['nestjs', 'microservices'], icon: 'server' },
  { id: 'r11', name: 'laravel.mdc', domain: 'backend', tags: ['laravel', 'php'], icon: 'server' },
  { id: 'r12', name: 'database.mdc', domain: 'database', tags: ['postgres', 'mysql'], icon: 'database' },
  { id: 'r13', name: 'postgres.mdc', domain: 'database', tags: ['postgres', 'rls'], icon: 'database' },
  { id: 'r14', name: 'mysql.mdc', domain: 'database', tags: ['mysql', 'optimization'], icon: 'database' },
  { id: 'r15', name: 'redis.mdc', domain: 'database', tags: ['redis', 'cache'], icon: 'database' },
  { id: 'r16', name: 'openai.mdc', domain: 'ai', tags: ['gpt', 'api'], icon: 'bot' },
  { id: 'r17', name: 'pgvector.mdc', domain: 'ai', tags: ['vector', 'embedding'], icon: 'box' },
  { id: 'r18', name: 'rag.mdc', domain: 'ai', tags: ['rag', 'retrieval'], icon: 'bot' },
  { id: 'r19', name: 'docker.mdc', domain: 'devops', tags: ['docker', 'containers'], icon: 'cloud' },
  { id: 'r20', name: 'kubernetes.mdc', domain: 'devops', tags: ['k8s', 'orchestration'], icon: 'cloud' },
  { id: 'r21', name: 'aws.mdc', domain: 'devops', tags: ['aws', 'cloud'], icon: 'cloud' },
  { id: 'r22', name: 'security.mdc', domain: 'business', tags: ['security', 'auth'], icon: 'shield' },
  { id: 'r23', name: 'multi-tenant.mdc', domain: 'business', tags: ['saas', 'isolation'], icon: 'users' },
  { id: 'r24', name: 'billing.mdc', domain: 'business', tags: ['billing', 'subscription'], icon: 'creditcard' },
]

const skills: SkillItem[] = [
  { id: 's1', name: 'aspnet-core', platform: 'Cursor · Codex · Claude', initials: 'AS', category: 'backend' },
  { id: 's2', name: 'vercel-deploy', platform: 'Cursor · Claude Plugins', initials: 'VE', category: 'devops' },
  { id: 's3', name: 'playwright', platform: 'Cursor · Claude Code · Codex', initials: 'PW', category: 'testing' },
  { id: 's4', name: 'figma', platform: 'Cursor · Claude Plugins', initials: 'FG', category: 'design' },
  { id: 's5', name: 'cloudflare-deploy', platform: 'Cursor · Claude Code', initials: 'CF', category: 'devops' },
  { id: 's6', name: 'docker', platform: 'Cursor · Claude Code', initials: 'DOC', category: 'devops' },
  { id: 's7', name: 'kubernetes', platform: 'Cursor · Claude Code', initials: 'K8S', category: 'devops' },
  { id: 's8', name: 'jupyter-notebook', platform: 'Claude Code · Claude Plugins', initials: 'JY', category: 'ai' },
  { id: 's9', name: 'gh-address-comments', platform: 'Claude Code · Claude Plugins', initials: 'GHP', category: 'devops' },
  { id: 's10', name: 'pdf', platform: 'Cursor · Claude Plugins', initials: 'PDF', category: 'utility' },
  { id: 's11', name: 'netlify-deploy', platform: 'Cursor · Claude Plugins', initials: 'NET', category: 'devops' },
  { id: 's12', name: 'screenshot', platform: 'Claude Plugins', initials: 'SCR', category: 'utility' },
  { id: 's13', name: 'frontend-taste', platform: 'Cursor · Claude', initials: 'FT', category: 'frontend' },
  { id: 's14', name: 'frontend-redesign', platform: 'Cursor · Claude', initials: 'FR', category: 'frontend' },
  { id: 's15', name: 'frontend-review', platform: 'Cursor · Claude', initials: 'FVR', category: 'frontend' },
  { id: 's16', name: 'security-review', platform: 'Cursor · Claude', initials: 'SEC', category: 'security' },
  { id: 's17', name: 'full-output', platform: 'Cursor · Claude', initials: 'FO', category: 'utility' },
  { id: 's18', name: 'vietnam-payment', platform: 'Cursor · Claude', initials: 'VP', category: 'business' },
]

// Dynamic counts based on actual data
const rulesCount = computed(() => rules.length)
const skillsCount = computed(() => skills.length)
const totalCount = computed(() => rulesCount.value + skillsCount.value)

// Count by domain for rules
const rulesByDomain = computed(() => {
  const counts: Record<string, number> = {}
  rules.forEach(r => {
    counts[r.domain] = (counts[r.domain] || 0) + 1
  })
  return counts
})

// Count by category for skills
const skillsByCategory = computed(() => {
  const counts: Record<string, number> = {}
  skills.forEach(s => {
    counts[s.category] = (counts[s.category] || 0) + 1
  })
  return counts
})

const navItems = computed(() => [
  { id: 'all', label: 'Tất cả', count: totalCount.value, icon: 'grid' },
  { id: 'rules', label: 'Rules', count: rulesCount.value, icon: 'layers' },
  { id: 'skills', label: 'Skills', count: skillsCount.value, icon: 'file' }
])

const categoryItems = computed(() => {
  const cats = [
    { id: 'core', label: 'Core', icon: 'layers' },
    { id: 'frontend', label: 'Frontend', icon: 'monitor' },
    { id: 'backend', label: 'Backend', icon: 'server' },
    { id: 'database', label: 'Database', icon: 'database' },
    { id: 'ai', label: 'AI & RAG', icon: 'bot' },
    { id: 'devops', label: 'Cloud & DevOps', icon: 'cloud' },
    { id: 'business', label: 'Business', icon: 'users' },
  ]
  return cats.map(c => ({
    ...c,
    count: (rulesByDomain.value[c.id] || 0) + (skillsByCategory.value[c.id] || 0)
  }))
})

const filterTags = [
  { id: 'all', label: 'All' },
  { id: 'core', label: 'Core' },
  { id: 'frontend', label: 'Frontend' },
  { id: 'backend', label: 'Backend' },
  { id: 'database', label: 'Database' },
  { id: 'ai', label: 'AI' },
  { id: 'devops', label: 'DevOps' },
  { id: 'business', label: 'Business' }
]

const showRules = computed(() => activeCategory.value === 'all' || activeCategory.value === 'rules')
const showSkills = computed(() => activeCategory.value === 'all' || activeCategory.value === 'skills')

const filteredRules = computed(() => {
  return rules.filter(rule => {
    const matchesFilter = activeFilter.value === 'all' || rule.domain === activeFilter.value
    const matchesSearch = searchQuery.value === '' ||
      rule.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      rule.tags.some(tag => tag.toLowerCase().includes(searchQuery.value.toLowerCase()))
    return matchesFilter && matchesSearch
  })
})

const filteredSkills = computed(() => {
  return skills.filter(skill => {
    const matchesFilter = activeFilter.value === 'all' || skill.category === activeFilter.value
    const matchesSearch = searchQuery.value === '' ||
      skill.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      skill.platform.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesFilter && matchesSearch
  })
})

function setCategory(category: string) {
  activeCategory.value = category
  // Reset filter when switching main category
  activeFilter.value = 'all'
}

function setFilter(filter: string) {
  activeFilter.value = filter
}

function clearSearch() {
  searchQuery.value = ''
}

onMounted(() => {
  if (explorerRef.value) {
    observe(explorerRef.value, () => {
      rules.forEach((rule) => {
        visibleItems.value.add(rule.id)
      })
      skills.forEach((skill) => {
        visibleItems.value.add(skill.id)
      })
    }, { threshold: 0.1 })
  }
})
</script>

<template>
  <section class="explorer-section" id="explorer" ref="explorerRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Documentation</div>
        <h2 class="section-title">Rules & Skills Explorer</h2>
        <p class="section-desc">
          {{ rulesCount }} MDC rules chuẩn hóa + {{ skillsCount }} specialized skills. Mỗi rule định nghĩa tiêu chuẩn,
          mỗi skill cung cấp expertise chuyên sâu cho AI agent.
        </p>
      </div>

      <div class="explorer-layout">
        <!-- Sidebar nav -->
        <aside class="explorer-sidebar">
          <div class="explorer-nav-section">
            <div class="explorer-nav-label">Framework</div>
            <button
              v-for="item in navItems"
              :key="item.id"
              class="explorer-nav-btn"
              :class="{ active: activeCategory === item.id }"
              @click="setCategory(item.id)"
            >
              <svg v-if="item.icon === 'grid'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
                <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
              </svg>
              <svg v-else-if="item.icon === 'layers'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
              </svg>
              {{ item.label }}
              <span class="explorer-nav-count">{{ item.count }}</span>
            </button>
          </div>

          <div class="explorer-nav-section">
            <div class="explorer-nav-label">Category</div>
            <button
              v-for="item in categoryItems"
              :key="item.id"
              class="explorer-nav-btn"
              :class="{ active: activeFilter === item.id }"
              @click="setFilter(item.id)"
            >
              <svg v-if="item.icon === 'layers'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
              </svg>
              <svg v-else-if="item.icon === 'monitor'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
                <line x1="8" y1="21" x2="16" y2="21"/>
                <line x1="12" y1="17" x2="12" y2="21"/>
              </svg>
              <svg v-else-if="item.icon === 'server'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="2" y="2" width="20" height="8" rx="2" ry="2"/>
                <rect x="2" y="14" width="20" height="8" rx="2" ry="2"/>
                <line x1="6" y1="6" x2="6.01" y2="6"/>
                <line x1="6" y1="18" x2="6.01" y2="18"/>
              </svg>
              <svg v-else-if="item.icon === 'database'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <ellipse cx="12" cy="5" rx="9" ry="3"/>
                <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
              </svg>
              <svg v-else-if="item.icon === 'bot'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M12 2a4 4 0 014 4c0 1.1-.9 2-2 2h-4a4 4 0 01-4-4 4 4 0 014-4m0 10c4.42 0 8 1.79 8 4v2H4v-2c0-2.21 3.58-4 8-4z"/>
              </svg>
              <svg v-else-if="item.icon === 'cloud'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M18 10h-1.26A8 8 0 109 20h9a5 5 0 000-10z"/>
              </svg>
              <svg v-else-if="item.icon === 'shield'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>
              </svg>
              {{ item.label }}
              <span class="explorer-nav-count">{{ item.count }}</span>
            </button>
          </div>
        </aside>

        <!-- Main content -->
        <div class="explorer-main">
          <div class="explorer-toolbar">
            <div class="explorer-search">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/>
                <path d="M21 21l-4.35-4.35"/>
              </svg>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Tìm kiếm rule hoặc skill..."
              />
              <button v-if="searchQuery" class="search-clear" @click="clearSearch">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
              <span class="explorer-search-shortcut">Ctrl+K</span>
            </div>
            <div class="explorer-filter-tags">
              <button
                v-for="tag in filterTags"
                :key="tag.id"
                class="filter-tag"
                :class="{ active: activeFilter === tag.id }"
                @click="setFilter(tag.id)"
              >
                {{ tag.label }}
              </button>
            </div>
          </div>

          <!-- Results count -->
          <div class="results-count">
            <span v-if="showRules && filteredRules.length > 0">
              {{ filteredRules.length }} rules
            </span>
            <span v-if="showRules && filteredSkills.length > 0"> · </span>
            <span v-if="showSkills && filteredSkills.length > 0">
              {{ filteredSkills.length }} skills
            </span>
            <span v-if="filteredRules.length === 0 && filteredSkills.length === 0">
              Không tìm thấy kết quả
            </span>
          </div>

          <!-- Rules list -->
          <div v-if="showRules" class="rules-list">
            <div
              v-for="rule in filteredRules"
              :key="rule.id"
              class="rule-item"
              :class="{ visible: visibleItems.has(rule.id) }"
            >
              <div class="rule-icon">
                <svg v-if="rule.icon === 'layers'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
                <svg v-else-if="rule.icon === 'grid'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
                  <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
                </svg>
                <svg v-else-if="rule.icon === 'search'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
                </svg>
                <svg v-else-if="rule.icon === 'code'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>
                </svg>
                <svg v-else-if="rule.icon === 'monitor'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>
                </svg>
                <svg v-else-if="rule.icon === 'server'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/>
                </svg>
                <svg v-else-if="rule.icon === 'database'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
                </svg>
                <svg v-else-if="rule.icon === 'bot'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M12 2a4 4 0 014 4c0 1.1-.9 2-2 2h-4a4 4 0 01-4-4 4 4 0 014-4m0 10c4.42 0 8 1.79 8 4v2H4v-2c0-2.21 3.58-4 8-4z"/>
                </svg>
                <svg v-else-if="rule.icon === 'cloud'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M18 10h-1.26A8 8 0 109 20h9a5 5 0 000-10z"/>
                </svg>
                <svg v-else-if="rule.icon === 'shield'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
                <svg v-else-if="rule.icon === 'users'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/>
                </svg>
                <svg v-else-if="rule.icon === 'creditcard'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                </svg>
              </div>
              <div class="rule-info">
                <div class="rule-item-name">{{ rule.name }}</div>
                <div class="rule-item-meta">
                  <span class="rule-domain">{{ rule.domain }}</span>
                  <div class="rule-tags">
                    <span v-for="tag in rule.tags" :key="tag" class="rule-tag">{{ tag }}</span>
                  </div>
                </div>
              </div>
              <div class="rule-badge">Rule</div>
              <div class="rule-arrow">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M7 17l9.2-9.2M17 17V7H7"/>
                </svg>
              </div>
            </div>

            <div v-if="filteredRules.length === 0 && activeCategory !== 'skills'" class="explorer-empty">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="11" cy="11" r="8"/>
                <path d="M21 21l-4.35-4.35"/>
              </svg>
              <p>Không tìm thấy rules phù hợp</p>
            </div>
          </div>

          <!-- Skills grid -->
          <div v-if="showSkills" class="skills-grid">
            <div
              v-for="skill in filteredSkills"
              :key="skill.id"
              class="skill-item"
              :class="{ visible: visibleItems.has(skill.id) }"
            >
              <div class="skill-icon">{{ skill.initials }}</div>
              <div class="skill-info">
                <div class="skill-name">{{ skill.name }}</div>
                <div class="skill-platform">{{ skill.platform }}</div>
              </div>
              <div class="skill-badge">Skill</div>
            </div>

            <div v-if="filteredSkills.length === 0 && activeCategory !== 'rules'" class="explorer-empty">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="11" cy="11" r="8"/>
                <path d="M21 21l-4.35-4.35"/>
              </svg>
              <p>Không tìm thấy skills phù hợp</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.explorer-section {
  padding: var(--section-py) 0;
}

.explorer-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 24px;
  margin-top: 48px;
  min-height: 540px;
}

.explorer-sidebar {
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-xl);
  padding: 8px;
  height: fit-content;
  position: sticky;
  top: 80px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
}

.explorer-nav-section {
  margin-bottom: 4px;
}

.explorer-nav-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
  padding: 12px 12px 6px;
}

.explorer-nav-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 9px 12px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: all var(--t-fast);
  text-align: left;
  cursor: pointer;
  border: 1px solid transparent;
}

.explorer-nav-btn svg {
  width: 15px;
  height: 15px;
  flex-shrink: 0;
}

.explorer-nav-btn:hover {
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-primary);
}

.explorer-nav-btn.active {
  background: var(--accent-glow);
  color: var(--accent-primary);
  border-color: var(--border-accent);
}

.explorer-nav-count {
  margin-left: auto;
  font-size: 10px;
  font-weight: 700;
  color: var(--text-muted);
  background: rgba(255, 255, 255, 0.04);
  padding: 1px 6px;
  border-radius: var(--radius-full);
  font-family: var(--font-mono);
}

.explorer-nav-btn.active .explorer-nav-count {
  background: rgba(120, 119, 232, 0.15);
  color: var(--accent-primary);
}

.explorer-main {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.explorer-toolbar {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.explorer-search {
  flex: 1;
  min-width: 200px;
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-md);
  padding: 9px 14px;
  transition: border-color var(--t-fast), box-shadow var(--t-fast);
}

.explorer-search:focus-within {
  border-color: rgba(120, 119, 232, 0.4);
  box-shadow: 0 0 0 3px rgba(120, 119, 232, 0.08);
}

.explorer-search svg {
  width: 14px;
  height: 14px;
  stroke: var(--text-muted);
  flex-shrink: 0;
}

.explorer-search input {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  font-size: 13px;
  font-family: var(--font-sans);
  color: var(--text-primary);
  caret-color: var(--accent-primary);
}

.explorer-search input::placeholder {
  color: var(--text-muted);
}

.search-clear {
  background: none;
  border: none;
  cursor: pointer;
  padding: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  transition: color var(--t-fast);
}

.search-clear:hover {
  color: var(--text-primary);
}

.search-clear svg {
  width: 14px;
  height: 14px;
}

.explorer-search-shortcut {
  font-size: 10px;
  font-weight: 600;
  color: var(--text-muted);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-subtle);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: var(--font-mono);
}

.explorer-filter-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.filter-tag {
  font-size: 11px;
  font-weight: 600;
  padding: 5px 12px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border-soft);
  background: transparent;
  color: var(--text-secondary);
  transition: all var(--t-fast);
  cursor: pointer;
  letter-spacing: 0.02em;
}

.filter-tag:hover {
  border-color: var(--border-default);
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.03);
}

.filter-tag.active {
  background: var(--accent-glow);
  border-color: var(--border-accent);
  color: var(--accent-primary);
}

.results-count {
  font-size: 12px;
  color: var(--text-muted);
  padding: 4px 0;
}

.rules-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.rule-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--t-base);
  opacity: 0;
  transform: translateY(10px);
}

.rule-item.visible {
  opacity: 1;
  transform: translateY(0);
}

.rule-item:hover {
  border-color: var(--border-accent);
  background: var(--bg-raised);
  box-shadow: 0 0 24px rgba(120, 119, 232, 0.06);
}

.rule-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: var(--accent-glow);
  border: 1px solid var(--border-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.rule-icon svg {
  width: 16px;
  height: 16px;
  stroke: var(--accent-primary);
}

.rule-info {
  flex: 1;
  min-width: 0;
}

.rule-item-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: color var(--t-fast);
}

.rule-item:hover .rule-item-name {
  color: var(--text-primary);
}

.rule-item-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rule-domain {
  font-size: 10.5px;
  font-weight: 600;
  color: var(--text-muted);
  background: rgba(255, 255, 255, 0.04);
  padding: 2px 7px;
  border-radius: var(--radius-full);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.rule-tags {
  display: flex;
  gap: 4px;
}

.rule-tag {
  font-size: 10px;
  font-weight: 500;
  color: var(--text-muted);
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  padding: 1px 6px;
  border-radius: var(--radius-full);
  font-family: var(--font-mono);
}

.rule-badge {
  font-size: 9px;
  font-weight: 700;
  color: var(--accent-primary);
  background: var(--accent-glow);
  padding: 2px 8px;
  border-radius: var(--radius-full);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  flex-shrink: 0;
}

.rule-arrow {
  color: var(--text-faint);
  transition: color var(--t-fast), transform var(--t-fast);
}

.rule-item:hover .rule-arrow {
  color: var(--accent-primary);
  transform: translateX(3px);
}

.rule-arrow svg {
  width: 14px;
  height: 14px;
}

.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 8px;
}

.skill-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--t-base);
  opacity: 0;
  transform: translateY(10px);
}

.skill-item.visible {
  opacity: 1;
  transform: translateY(0);
}

.skill-item:hover {
  border-color: rgba(6, 182, 212, 0.3);
  background: var(--bg-raised);
  box-shadow: 0 0 20px rgba(6, 182, 212, 0.06);
}

.skill-icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  background: rgba(6, 182, 212, 0.08);
  border: 1px solid rgba(6, 182, 212, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 11px;
  font-weight: 800;
  color: var(--accent-tertiary);
  font-family: var(--font-mono);
}

.skill-info {
  flex: 1;
  min-width: 0;
}

.skill-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  font-family: var(--font-mono);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.skill-item:hover .skill-name {
  color: var(--text-primary);
}

.skill-platform {
  font-size: 10px;
  color: var(--text-muted);
  margin-top: 1px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.skill-badge {
  font-size: 9px;
  font-weight: 700;
  color: var(--accent-tertiary);
  background: rgba(6, 182, 212, 0.08);
  padding: 2px 8px;
  border-radius: var(--radius-full);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  flex-shrink: 0;
}

.explorer-empty {
  text-align: center;
  padding: 48px 0;
  color: var(--text-muted);
  grid-column: 1 / -1;
}

.explorer-empty svg {
  width: 40px;
  height: 40px;
  margin: 0 auto 12px;
  opacity: 0.5;
}

.explorer-empty p {
  font-size: 14px;
}

@media (max-width: 1024px) {
  .explorer-layout {
    grid-template-columns: 1fr;
  }

  .explorer-sidebar {
    position: static;
    max-height: 400px;
    overflow-y: auto;
  }
}
</style>
