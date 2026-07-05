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
  { label: 'Frontend', items: ['Next.js 15', 'React 19', 'Vue 3', 'Nuxt 4', 'TypeScript'] },
  { label: 'Backend', items: ['Laravel 12', 'NestJS', 'ASP.NET Core 9', 'Node.js'] },
  { label: 'Database', items: ['PostgreSQL', 'MySQL', 'Redis', 'Supabase', 'SQL Server'] },
  { label: 'AI & RAG', items: ['OpenAI', 'Claude', 'Gemini', 'pgvector', 'Ollama'] },
  { label: 'Cloud', items: ['Cloudflare', 'AWS', 'Vercel', 'Docker', 'Kubernetes'] },
  { label: 'Workflow', items: ['n8n', 'Temporal', 'Trigger.dev', 'BullMQ'] }
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
        <div class="section-label">Architecture</div>
        <h2 class="section-title">One folder. Every tool your agent needs.</h2>
        <p class="section-desc">
          Drop the <code class="mono" style="background: var(--bg-elevated); padding: 1px 6px; border-radius: 4px; font-size: 13px; color: var(--accent);">.cursor/</code> directory into any project. The agent picks up rules, skills, knowledge,
          and personas automatically, no config files, no setup scripts.
        </p>
      </div>

      <div class="arch-bento" :class="{ visible: isVisible }">
        <!-- File tree panel -->
        <div class="arch-tree">
          <div class="arch-tree-header">
            <span class="arch-tree-title">.cursor/</span>
            <span class="arch-tree-meta">5 top-level folders</span>
          </div>
          <div class="arch-tree-body">
            <div class="tree-node tree-node--root">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 7l9-4 9 4-9 4-9-4z"/><path d="M3 12l9 4 9-4M3 17l9 4 9-4"/></svg>
              <span class="tree-name">rules</span>
              <span class="tree-count">41 .mdc</span>
            </div>
            <div class="tree-files">
              <div class="tree-file">coding-standards.mdc</div>
              <div class="tree-file">security.mdc</div>
              <div class="tree-file tree-file--more">+ 38 more</div>
            </div>

            <div class="tree-node">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="13 2 13 9 20 9"/><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/></svg>
              <span class="tree-name">skills</span>
              <span class="tree-count">18 /</span>
            </div>
            <div class="tree-files">
              <div class="tree-file">frontend-taste/</div>
              <div class="tree-file">security-review/</div>
              <div class="tree-file tree-file--more">+ 16 more</div>
            </div>

            <div class="tree-node">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
              <span class="tree-name">knowledge</span>
              <span class="tree-count">37 domains</span>
            </div>

            <div class="tree-node">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M16 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="8.5" cy="7" r="4"/><path d="M20 8v6M23 11h-6"/></svg>
              <span class="tree-name">agents</span>
              <span class="tree-count">8 personas</span>
            </div>

            <div class="tree-node">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>
              <span class="tree-name">memory</span>
              <span class="tree-count">sqlite</span>
            </div>

            <div class="tree-node">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
              <span class="tree-name">scripts</span>
              <span class="tree-count">12 .ps1</span>
            </div>
          </div>
        </div>

        <!-- Description panels (bento grid) -->
        <div class="arch-panel arch-panel--rules">
          <div class="arch-panel-head">
            <span class="arch-panel-tag">Core</span>
            <h3 class="arch-panel-title">41 MDC rules</h3>
          </div>
          <p class="arch-panel-text">
            Every rule is a typed Markdown file with frontmatter, version, and scope tags.
            The agent reads the right one at the right time.
          </p>
          <div class="arch-panel-stat">
            <span class="arch-panel-stat-num">9</span>
            <span class="arch-panel-stat-label">domains covered</span>
          </div>
        </div>

        <div class="arch-panel arch-panel--skills">
          <div class="arch-panel-head">
            <span class="arch-panel-tag">Skills</span>
            <h3 class="arch-panel-title">18 skills, each a workflow</h3>
          </div>
          <p class="arch-panel-text">
            Skill files contain step-by-step instructions, anti-patterns, and outputs.
            No more guessing what to do next.
          </p>
        </div>

        <div class="arch-panel arch-panel--agents">
          <div class="arch-panel-head">
            <span class="arch-panel-tag">Subagents</span>
            <h3 class="arch-panel-title">8 specialist reviewers</h3>
          </div>
          <p class="arch-panel-text">
            Code, security, test, performance, API, backend, database, frontend.
            Each persona reads only what it needs.
          </p>
          <div class="arch-panel-list">
            <code>/review</code>
            <code>/security</code>
            <code>/test</code>
            <code>/perf</code>
          </div>
        </div>

        <div class="arch-panel arch-panel--memory">
          <div class="arch-panel-head">
            <span class="arch-panel-tag">Memory</span>
            <h3 class="arch-panel-title">Local SQLite memory</h3>
          </div>
          <p class="arch-panel-text">
            ADRs, bug history, and past decisions stay local. The agent reuses them
            instead of re-deriving from scratch.
          </p>
        </div>
      </div>

      <!-- Tech stack -->
      <div class="arch-tech">
        <div class="arch-tech-head">
          <span class="section-label" style="margin-bottom: 0;">Coverage</span>
          <h3 class="arch-tech-title">Works with the stacks you already use</h3>
        </div>
        <div class="tech-grid">
          <div v-for="category in techStack" :key="category.label" class="tech-cat">
            <div class="tech-cat-label">{{ category.label }}</div>
            <div class="tech-cat-items">
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

/* ─── BENTO LAYOUT ───────────────────────────────────────────────── */
.arch-bento {
  display: grid;
  grid-template-columns: 1.1fr 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 16px;
  margin-bottom: 80px;
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 600ms var(--ease-out-quart), transform 600ms var(--ease-out-quart);
}

.arch-bento.visible {
  opacity: 1;
  transform: translateY(0);
}

.arch-tree {
  grid-column: 1;
  grid-row: 1 / span 2;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.arch-tree-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  border-bottom: 1px solid var(--border-hairline);
  background: var(--bg-surface);
}

.arch-tree-title {
  font-family: var(--font-mono);
  font-size: 12.5px;
  color: var(--text-primary);
  font-weight: 500;
}

.arch-tree-meta {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
}

.arch-tree-body {
  padding: 12px 0;
  font-family: var(--font-mono);
  font-size: 12.5px;
}

.tree-node {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px 18px;
  color: var(--text-primary);
  transition: background var(--t-fast);
}

.tree-node:hover {
  background: rgba(255, 255, 255, 0.025);
}

.tree-node svg {
  width: 14px;
  height: 14px;
  color: var(--text-tertiary);
  flex-shrink: 0;
}

.tree-name {
  font-weight: 500;
}

.tree-count {
  margin-left: auto;
  font-size: 11px;
  color: var(--text-tertiary);
}

.tree-files {
  padding: 0 18px 6px 44px;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.tree-file {
  font-size: 12px;
  color: var(--text-tertiary);
  padding: 3px 8px;
  border-radius: 3px;
  transition: color var(--t-fast), background var(--t-fast);
}

.tree-file:hover {
  color: var(--text-secondary);
  background: rgba(255, 255, 255, 0.025);
}

.tree-file--more {
  color: var(--text-muted);
  font-style: italic;
}

/* ─── DESCRIPTION PANELS ───────────────────────────────────────── */
.arch-panel {
  padding: 24px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  display: flex;
  flex-direction: column;
  transition: border-color var(--t-base), background var(--t-base);
}

.arch-panel:hover {
  border-color: var(--border-default);
}

.arch-panel--rules { grid-column: 2; grid-row: 1; }
.arch-panel--skills { grid-column: 3; grid-row: 1; }
.arch-panel--agents { grid-column: 2; grid-row: 2; }
.arch-panel--memory { grid-column: 3; grid-row: 2; }

.arch-panel-head {
  margin-bottom: 12px;
}

.arch-panel-tag {
  display: inline-block;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent);
  background: var(--accent-dim);
  border: 1px solid var(--accent-line);
  padding: 3px 8px;
  border-radius: var(--radius-pill);
  font-family: var(--font-mono);
  margin-bottom: 12px;
}

.arch-panel-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.015em;
  line-height: 1.25;
}

.arch-panel-text {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  flex: 1;
}

.arch-panel-stat {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid var(--border-hairline);
}

.arch-panel-stat-num {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  font-family: var(--font-mono);
  letter-spacing: -0.02em;
}

.arch-panel-stat-label {
  font-size: 11px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.arch-panel-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 14px;
}

.arch-panel-list code {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--accent);
  background: var(--accent-dim);
  padding: 3px 8px;
  border-radius: var(--radius-sm);
}

/* ─── TECH STACK ───────────────────────────────────────────────── */
.arch-tech {
  margin-top: 64px;
}

.arch-tech-head {
  margin-bottom: 32px;
}

.arch-tech-title {
  font-size: clamp(20px, 2.6vw, 26px);
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  margin-top: 12px;
  max-width: 32ch;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
}

.tech-cat {
  padding: 20px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-hairline);
  border-radius: var(--radius-lg);
  transition: border-color var(--t-base);
}

.tech-cat:hover {
  border-color: var(--border-default);
}

.tech-cat-label {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-tertiary);
  margin-bottom: 12px;
  font-family: var(--font-mono);
}

.tech-cat-items {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tech-chip {
  font-size: 12px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  background: var(--bg-surface);
  border: 1px solid var(--border-hairline);
  color: var(--text-secondary);
  transition: all var(--t-fast);
}

.tech-chip:hover {
  color: var(--text-primary);
  border-color: var(--border-default);
}

@media (max-width: 1024px) {
  .arch-bento {
    grid-template-columns: 1fr 1fr;
  }

  .arch-tree {
    grid-column: 1 / -1;
    grid-row: auto;
  }

  .arch-panel--rules,
  .arch-panel--skills { grid-row: auto; }
  .arch-panel--agents,
  .arch-panel--memory { grid-row: auto; }
}

@media (max-width: 640px) {
  .arch-bento {
    grid-template-columns: 1fr;
  }

  .arch-panel { grid-column: 1 !important; }
}
</style>