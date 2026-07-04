<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const sectionRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()

const isVisible = ref(false)

interface TechCategory {
  label: string
  items: string[]
}

const techStack: TechCategory[] = [
  {
    label: 'Frontend',
    items: ['Next.js 15', 'React 19', 'Vue 3', 'Nuxt 4', 'TypeScript 5', 'TailwindCSS', 'Shadcn/UI']
  },
  {
    label: 'Backend',
    items: ['Laravel 12', 'ASP.NET Core 9', 'NestJS', 'NodeJS']
  },
  {
    label: 'Database',
    items: ['MySQL', 'PostgreSQL', 'SQL Server', 'SQLite', 'Redis', 'Supabase']
  },
  {
    label: 'AI & RAG',
    items: ['OpenAI', 'Gemini', 'Claude', 'Ollama', 'PGVector', 'ChromaDB', 'Qdrant']
  },
  {
    label: 'Cloud & DevOps',
    items: ['Cloudflare', 'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Vercel']
  },
  {
    label: 'Workflow',
    items: ['n8n', 'Temporal', 'Trigger.dev']
  }
]

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      isVisible.value = true
    }, { threshold: 0.1 })
  }
})
</script>

<template>
  <section class="architecture-section" id="architecture" ref="sectionRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Structure</div>
        <h2 class="section-title">Kiến trúc hệ thống</h2>
        <p class="section-desc">
          `.cursor/` directory chứa toàn bộ framework — được tổ chức theo nguyên tắc
          separation of concerns, mỗi thành phần có trách nhiệm rõ ràng.
        </p>
      </div>

      <div class="arch-hero" :class="{ visible: isVisible }">
        <!-- File tree -->
        <div class="file-tree">
          <div class="ft-header">
            <div class="ft-dots"><span></span><span></span><span></span></div>
            <span class="ft-title">.cursor/</span>
          </div>
          <div class="ft-body">
            <div class="ft-branch">
              <div class="ft-item ft-folder">
                <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>
                </svg>
                rules
                <span class="ft-count">41 files</span>
              </div>
              <div class="ft-sub">
                <div class="ft-item ft-file">
                  <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                  </svg>
                  core-architecture.mdc
                </div>
                <div class="ft-item ft-file">
                  <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                  </svg>
                  memory-first.mdc
                </div>
                <div class="ft-item ft-file">
                  <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                  </svg>
                  context-router.mdc
                </div>
                <div class="ft-item ft-file" style="color: var(--text-faint); font-style: italic;">+38 more rules...</div>
              </div>
            </div>

            <div class="ft-branch">
              <div class="ft-item ft-folder" style="color: #06b6d4;">
                <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="stroke: #06b6d4;">
                  <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>
                </svg>
                skills
                <span class="ft-count">18 files</span>
              </div>
              <div class="ft-sub">
                <div class="ft-item ft-file">
                  <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                  </svg>
                  aspnet-core/
                </div>
                <div class="ft-item ft-file">
                  <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                  </svg>
                  playwright/
                </div>
                <div class="ft-item ft-file">
                  <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                  </svg>
                  figma/
                </div>
                <div class="ft-item ft-file" style="color: var(--text-faint); font-style: italic;">+15 more skills...</div>
              </div>
            </div>

            <div class="ft-branch">
              <div class="ft-item ft-folder" style="color: #34d399;">
                <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="stroke: #34d399;">
                  <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>
                </svg>
                knowledge
                <span class="ft-count">37 directories</span>
              </div>
              <div class="ft-sub">
                <div class="ft-item ft-folder" style="color: var(--text-secondary);">
                  <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>
                  </svg>
                  frontend/
                </div>
                <div class="ft-item ft-folder" style="color: var(--text-secondary);">
                  <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>
                  </svg>
                  backend/
                </div>
                <div class="ft-item ft-folder" style="color: var(--text-secondary);">
                  <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>
                  </svg>
                  ai-rag/
                </div>
                <div class="ft-item ft-file" style="color: var(--text-faint); font-style: italic;">+6 more domains...</div>
              </div>
            </div>

            <div class="ft-branch">
              <div class="ft-item ft-folder" style="color: #fbbf24;">
                <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="stroke: #fbbf24;">
                  <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>
                </svg>
                agents
                <span class="ft-count">8 personas</span>
              </div>
              <div class="ft-sub">
                <div class="ft-item ft-file">
                  <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                  </svg>
                  code-reviewer.md
                </div>
                <div class="ft-item ft-file">
                  <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                  </svg>
                  security-auditor.md
                </div>
                <div class="ft-item ft-file">
                  <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                  </svg>
                  test-engineer.md
                </div>
                <div class="ft-item ft-file" style="color: var(--text-faint); font-style: italic;">+5 more agents...</div>
              </div>
            </div>

            <div class="ft-branch">
              <div class="ft-item ft-folder">
                <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>
                </svg>
                memory/
                <span class="ft-count">schemas</span>
              </div>
            </div>

            <div class="ft-branch">
              <div class="ft-item ft-folder">
                <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>
                </svg>
                scripts/
                <span class="ft-count">automation</span>
              </div>
            </div>

            <div class="ft-branch">
              <div class="ft-item ft-folder">
                <svg class="ft-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>
                </svg>
                prompts/
                <span class="ft-count">templates</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Architecture description -->
        <div class="arch-desc">
          <div class="arch-desc-item">
            <div class="arch-desc-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
              </svg>
            </div>
            <div class="arch-desc-text">
              <h4>41 MDC Rules</h4>
              <p>YAML frontmatter với metadata, tags, version. Mỗi rule định nghĩa tiêu chuẩn cho architecture, coding, security, performance.</p>
            </div>
          </div>

          <div class="arch-desc-item">
            <div class="arch-desc-icon" style="background: rgba(6, 182, 212, 0.08); border-color: rgba(6, 182, 212, 0.2);">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="stroke: #06b6d4;">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
              </svg>
            </div>
            <div class="arch-desc-text">
              <h4>18 Specialized Skills</h4>
              <p>SKILL.md files cho Cursor, Claude Code, Codex, Claude Plugins. Mỗi skill cung cấp step-by-step expertise.</p>
            </div>
          </div>

          <div class="arch-desc-item">
            <div class="arch-desc-icon" style="background: rgba(52, 211, 153, 0.08); border-color: rgba(52, 211, 153, 0.2);">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="stroke: #34d399;">
                <circle cx="11" cy="11" r="8"/>
                <path d="M21 21l-4.35-4.35"/>
              </svg>
            </div>
            <div class="arch-desc-text">
              <h4>37 Knowledge Domains</h4>
              <p>Mỗi domain đi kèm bộ knowledge chuẩn hóa: architecture, best-practice, anti-pattern, faq, checklist, glossary.</p>
            </div>
          </div>

          <div class="arch-desc-item">
            <div class="arch-desc-icon" style="background: rgba(251, 191, 36, 0.08); border-color: rgba(251, 191, 36, 0.2);">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="stroke: #fbbf24;">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
              </svg>
            </div>
            <div class="arch-desc-text">
              <h4>8 Agent Personas</h4>
              <p>Specialist reviewers cho code, security, test, perf, API, backend, database, frontend. Dispatch qua slash commands: /review, /security, /test, /perf.</p>
            </div>
          </div>

          <div class="arch-desc-item">
            <div class="arch-desc-icon" style="background: rgba(251, 191, 36, 0.08); border-color: rgba(251, 191, 36, 0.2);">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="stroke: #fbbf24;">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
              </svg>
            </div>
            <div class="arch-desc-text">
              <h4>Context Router & Memory System</h4>
              <p>Tự động route đúng domain, load đúng rules, ghi nhớ decisions. Giảm 40% token consumption.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Tech Stack -->
      <div class="tech-stack-section">
        <h3 style="font-size: 16px; font-weight: 700; color: var(--text-primary); margin-bottom: 8px;">Tech Stack Supported</h3>
        <div class="tech-grid">
          <div v-for="category in techStack" :key="category.label" class="tech-category">
            <span class="tech-cat-label">{{ category.label }}</span>
            <div class="tech-items">
              <span v-for="item in category.items" :key="item" class="tech-chip">{{ item }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.architecture-section {
  padding: var(--section-py) 0;
}

.arch-hero {
  margin-top: 48px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  align-items: start;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s var(--ease-out), transform 0.6s var(--ease-out);
}

.arch-hero.visible {
  opacity: 1;
  transform: translateY(0);
}

.file-tree {
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.ft-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(255, 255, 255, 0.02);
}

.ft-dots {
  display: flex;
  gap: 5px;
}

.ft-dots span {
  width: 9px;
  height: 9px;
  border-radius: 50%;
}

.ft-dots span:nth-child(1) { background: #f87171; }
.ft-dots span:nth-child(2) { background: #fbbf24; }
.ft-dots span:nth-child(3) { background: #34d399; }

.ft-title {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--text-muted);
  flex: 1;
  text-align: center;
  letter-spacing: 0.05em;
}

.ft-body {
  padding: 12px 0;
}

.ft-branch {
  padding-left: 16px;
}

.ft-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 16px;
  font-size: 12px;
  font-family: var(--font-mono);
  color: var(--text-secondary);
  border-radius: var(--radius-xs);
  cursor: pointer;
  transition: background var(--t-fast);
  user-select: none;
}

.ft-item:hover {
  background: rgba(255, 255, 255, 0.04);
}

.ft-folder {
  color: var(--accent-primary);
}

.ft-file {
  color: var(--text-muted);
}

.ft-icon {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

.ft-sub {
  padding-left: 28px;
}

.ft-count {
  margin-left: auto;
  font-size: 10px;
  color: var(--text-faint);
}

.arch-desc {
  background: var(--bg-surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-xl);
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.arch-desc-item {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.arch-desc-icon {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-sm);
  background: var(--accent-glow);
  border: 1px solid var(--border-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.arch-desc-icon svg {
  width: 15px;
  height: 15px;
  stroke: var(--accent-primary);
}

.arch-desc-text h4 {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.arch-desc-text p {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.tech-stack-section {
  margin-top: 48px;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
  margin-top: 28px;
}

.tech-category {
  padding: 20px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-soft);
  background: var(--bg-surface);
}

.tech-cat-label {
  display: block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 12px;
}

.tech-items {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tech-chip {
  font-size: 11px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border-subtle);
  background: rgba(255, 255, 255, 0.02);
  color: var(--text-secondary);
  transition: all var(--t-fast);
}

.tech-chip:hover {
  border-color: var(--border-accent);
  color: var(--text-primary);
  background: var(--accent-glow);
}

@media (max-width: 1024px) {
  .arch-hero {
    grid-template-columns: 1fr;
  }
}
</style>
