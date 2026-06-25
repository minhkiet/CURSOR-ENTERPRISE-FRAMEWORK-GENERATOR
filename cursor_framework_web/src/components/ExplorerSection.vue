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
}

const explorerRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()
const visibleItems = ref(new Set<number>())

const activeCategory = ref('all')
const activeFilter = ref('all')
const searchQuery = ref('')
const showRules = computed(() => activeCategory.value !== 'skills')

const navItems = [
  { id: 'all', label: 'Tất cả', count: 126, icon: 'grid' },
  { id: 'rules', label: 'Rules', count: 79, icon: 'layers' },
  { id: 'skills', label: 'Skills', count: 47, icon: 'file' }
]

const categoryItems = [
  { id: 'frontend', label: 'Frontend', count: 8, icon: 'monitor' },
  { id: 'backend', label: 'Backend', count: 11, icon: 'server' },
  { id: 'database', label: 'Database', count: 7, icon: 'database' },
  { id: 'ai', label: 'AI & RAG', count: 10, icon: 'bot' },
  { id: 'devops', label: 'Cloud & DevOps', count: 14, icon: 'cloud' },
  { id: 'business', label: 'Business', count: 9, icon: 'users' }
]

const filterTags = [
  { id: 'all', label: 'All' },
  { id: 'core', label: 'Core' },
  { id: 'frontend', label: 'Frontend' },
  { id: 'backend', label: 'Backend' },
  { id: 'ai', label: 'AI' },
  { id: 'devops', label: 'DevOps' }
]

const rules: RuleItem[] = [
  { id: '1', name: 'core-architecture.mdc', domain: 'core', tags: ['architecture', 'foundation'], icon: 'layers' },
  { id: '2', name: 'memory-first.mdc', domain: 'core', tags: ['memory', 'context'], icon: 'grid' },
  { id: '3', name: 'context-router.mdc', domain: 'core', tags: ['routing', 'intelligence'], icon: 'search' },
  { id: '4', name: 'token-optimization.mdc', domain: 'core', tags: ['tokens', 'efficiency'], icon: 'zap' },
  { id: '5', name: 'nextjs.mdc', domain: 'frontend', tags: ['next.js', 'react'], icon: 'monitor' },
  { id: '6', name: 'aspnet-core.mdc', domain: 'backend', tags: ['.net', 'api'], icon: 'server' },
  { id: '7', name: 'supabase.mdc', domain: 'database', tags: ['postgres', 'rls'], icon: 'database' },
  { id: '8', name: 'openai.mdc', domain: 'ai', tags: ['gpt', 'api'], icon: 'bot' },
  { id: '9', name: 'pgvector.mdc', domain: 'ai', tags: ['vector', 'embedding'], icon: 'box' },
  { id: '10', name: 'cloudflare.mdc', domain: 'devops', tags: ['workers', 'cdn'], icon: 'cloud' },
  { id: '11', name: 'multi-tenant.mdc', domain: 'business', tags: ['saas', 'isolation'], icon: 'users' },
  { id: '12', name: 'billing.mdc', domain: 'business', tags: ['subscription', 'pricing'], icon: 'creditcard' }
]

const skills: SkillItem[] = [
  { id: '1', name: 'aspnet-core', platform: 'Cursor · Codex · Claude', initials: 'AS' },
  { id: '2', name: 'vercel-deploy', platform: 'Cursor · Claude Plugins', initials: 'VE' },
  { id: '3', name: 'playwright', platform: 'Cursor · Claude Code · Codex', initials: 'PW' },
  { id: '4', name: 'figma', platform: 'Cursor · Claude Plugins', initials: 'FG' },
  { id: '5', name: 'cloudflare-deploy', platform: 'Cursor · Claude Code', initials: 'CF' },
  { id: '6', name: 'docker', platform: 'Cursor · Claude Code', initials: 'DOC' },
  { id: '7', name: 'kubernetes', platform: 'Cursor · Claude Code', initials: 'K8S' },
  { id: '8', name: 'jupyter-notebook', platform: 'Claude Code · Claude Plugins', initials: 'JY' },
  { id: '9', name: 'gh-address-comments', platform: 'Claude Code · Claude Plugins', initials: 'GHP' },
  { id: '10', name: 'pdf', platform: 'Cursor · Claude Plugins', initials: 'PDF' },
  { id: '11', name: 'netlify-deploy', platform: 'Cursor · Claude Plugins', initials: 'NET' },
  { id: '12', name: 'screenshot', platform: 'Claude Plugins', initials: 'SCR' }
]

const filteredRules = computed(() => {
  return rules.filter(rule => {
    const matchesFilter = activeFilter.value === 'all' || rule.domain === activeFilter.value
    const matchesSearch = searchQuery.value === '' ||
      rule.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      rule.tags.some(tag => tag.toLowerCase().includes(searchQuery.value.toLowerCase()))
    return matchesFilter && matchesSearch
  })
})

function setCategory(category: string) {
  activeCategory.value = category
}

function setFilter(filter: string) {
  activeFilter.value = filter
}

onMounted(() => {
  if (explorerRef.value) {
    observe(explorerRef.value, () => {
      rules.forEach((_, idx) => {
        visibleItems.value.add(idx)
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
          79 MDC rules chuẩn hóa + 47 specialized skills. Mỗi rule định nghĩa tiêu chuẩn,
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
              @click="setFilter(item.id)"
            >
              <svg v-if="item.icon === 'monitor'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
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

          <!-- Rules list -->
          <div v-if="showRules" class="rules-list">
            <div
              v-for="rule in filteredRules"
              :key="rule.id"
              class="rule-item"
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
              <div class="rule-arrow">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M7 17l9.2-9.2M17 17V7H7"/>
                </svg>
              </div>
            </div>

            <div v-if="filteredRules.length === 0" class="explorer-empty">
              Không tìm thấy kết quả phù hợp
            </div>
          </div>

          <!-- Skills grid -->
          <div v-else class="skills-grid">
            <div
              v-for="skill in skills"
              :key="skill.id"
              class="skill-item"
            >
              <div class="skill-icon">{{ skill.initials }}</div>
              <div>
                <div class="skill-name">{{ skill.name }}</div>
                <div class="skill-platform">{{ skill.platform }}</div>
              </div>
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
  border: 1px solid var(--border-accent);
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
}

.explorer-search {
  flex: 1;
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
  font-size: 13px;
  font-weight: 800;
  color: var(--accent-tertiary);
  font-family: var(--font-mono);
}

.skill-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  font-family: var(--font-mono);
}

.skill-platform {
  font-size: 10px;
  color: var(--text-muted);
  margin-top: 1px;
}

.skill-item:hover .skill-name {
  color: var(--text-primary);
}

.explorer-empty {
  text-align: center;
  padding: 48px 0;
  color: var(--text-muted);
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
