<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const sectionRef = ref<HTMLElement | null>(null)
const { observe } = useIntersectionObserver()

interface FileNode {
  name: string
  path: string
  type: 'folder' | 'file'
  kind: 'rule' | 'skill' | 'agent' | 'kb' | 'config' | 'package' | 'doc' | 'memory'
  size?: string
  children?: FileNode[]
}

const fileTree: FileNode[] = [
  {
    name: 'cursor-framework',
    path: '/',
    type: 'folder',
    kind: 'package',
    children: [
      {
        name: 'rules',
        path: '.cursor/rules',
        type: 'folder',
        kind: 'rule',
        children: [
          { name: 'rule_karpathy-guidelines.mdc', path: '.cursor/rules/rule_karpathy-guidelines.mdc', type: 'file', kind: 'rule', size: '3.2 KB' },
          { name: 'ref_architecture-patterns.mdc', path: '.cursor/rules/ref_architecture-patterns.mdc', type: 'file', kind: 'rule', size: '8.4 KB' },
          { name: 'ref_security.mdc', path: '.cursor/rules/ref_security.mdc', type: 'file', kind: 'rule', size: '6.7 KB' },
          { name: '+ 36 more', path: '.cursor/rules', type: 'file', kind: 'rule', size: '39 files' }
        ]
      },
      {
        name: 'skills',
        path: '.cursor/skills',
        type: 'folder',
        kind: 'skill',
        children: [
          { name: 'code_karpathy-coding', path: '.cursor/skills/code_karpathy-coding', type: 'file', kind: 'skill', size: 'SKILL.md' },
          { name: 'special_ponytail', path: '.cursor/skills/special_ponytail', type: 'file', kind: 'skill', size: 'SKILL.md' },
          { name: 'ui_frontend-review', path: '.cursor/skills/ui_frontend-review', type: 'file', kind: 'skill', size: 'SKILL.md' },
          { name: '+ 14 more', path: '.cursor/skills', type: 'file', kind: 'skill', size: '17 skills' }
        ]
      },
      {
        name: 'agents',
        path: '.cursor/agents',
        type: 'folder',
        kind: 'agent',
        children: [
          { name: 'code-reviewer.md', path: '.cursor/agents/code-reviewer.md', type: 'file', kind: 'agent', size: '4.1 KB' },
          { name: 'security-auditor.md', path: '.cursor/agents/security-auditor.md', type: 'file', kind: 'agent', size: '5.8 KB' },
          { name: '+ 6 more', path: '.cursor/agents', type: 'file', kind: 'agent', size: '8 agents' }
        ]
      }
    ]
  }
]

const isVisible = ref(false)

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      isVisible.value = true
    }, { threshold: 0.1 })
  }
})

const getFileIcon = (kind: string) => {
  switch (kind) {
    case 'rule': return '📘'
    case 'skill': return '⚡'
    case 'agent': return '◆'
    case 'kb': return '◆'
    case 'package': return '◆'
    default: return '◆'
  }
}
</script>

<template>
  <section class="explorer-section" id="explorer" ref="sectionRef">
    <div class="container">
      <div class="section-header">
        <div class="section-label">File Explorer</div>
        <h2 class="section-title">A real repository. Not a screenshot.</h2>
        <p class="section-desc">
          The framework ships as a structured monorepo. 39 rules, 17 skills, 8 agents, 36 knowledge
          files. Browse the actual structure.
        </p>
      </div>

      <div class="explorer-window" :class="{ visible: isVisible }">
        <div class="explorer-bar">
          <div class="explorer-dots">
            <span class="dot dot-red"></span>
            <span class="dot dot-yellow"></span>
            <span class="dot dot-green"></span>
          </div>
          <div class="explorer-path">
            <span class="path-icon">◇</span>
            <span class="path-text">cursor-framework</span>
          </div>
          <div class="explorer-meta">main</div>
        </div>

        <div class="explorer-body">
          <aside class="explorer-sidebar">
            <div class="sidebar-section">
              <div class="sidebar-label">Workspace</div>
              <div class="sidebar-item active">
                <span class="sidebar-icon">◇</span>
                <span class="sidebar-name">cursor-framework</span>
              </div>
            </div>
            <div class="sidebar-section">
              <div class="sidebar-label">Structure</div>
              <div class="sidebar-item">
                <span class="sidebar-icon sidebar-icon-rule">◆</span>
                <span class="sidebar-name">rules</span>
                <span class="sidebar-count">39</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-icon sidebar-icon-skill">◆</span>
                <span class="sidebar-name">skills</span>
                <span class="sidebar-count">17</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-icon sidebar-icon-agent">◆</span>
                <span class="sidebar-name">agents</span>
                <span class="sidebar-count">8</span>
              </div>
              <div class="sidebar-item">
                <span class="sidebar-icon sidebar-icon-kb">◆</span>
                <span class="sidebar-name">knowledge</span>
                <span class="sidebar-count">36</span>
              </div>
            </div>
          </aside>

          <div class="explorer-main">
            <div class="explorer-breadcrumb">
              <span>cursor-framework</span>
              <span class="bc-sep">/</span>
              <span class="bc-current">.cursor</span>
            </div>

            <div class="explorer-tree">
              <div
                v-for="(node, i) in fileTree[0].children"
                :key="node.name"
                class="tree-folder"
                :style="{ '--delay': `${i * 80}ms` }"
              >
                <div class="tree-folder-header">
                  <span class="tree-icon">{{ getFileIcon(node.kind) }}</span>
                  <span class="tree-name">{{ node.name }}</span>
                  <span class="tree-count">{{ node.children?.length || 0 }} items</span>
                </div>
                <ul class="tree-files">
                  <li
                    v-for="child in node.children"
                    :key="child.name"
                    class="tree-file"
                  >
                    <span class="tree-file-icon" :class="`tree-file-icon-${child.kind}`">◇</span>
                    <span class="tree-file-name">{{ child.name }}</span>
                    <span class="tree-file-size">{{ child.size }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div class="explorer-status">
          <div class="status-item">
            <span class="status-dot status-dot-success"></span>
            <span>39 rules, 17 skills, 8 agents</span>
            <span class="status-caret" aria-hidden="true"></span>
          </div>
          <div class="status-item">
            <span class="status-text">1.2 MB</span>
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

.explorer-window {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: 0 32px 64px -24px rgba(0, 0, 0, 0.5);
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 600ms var(--ease-out-quart), transform 600ms var(--ease-out-quart);
}

.explorer-window.visible {
  opacity: 1;
  transform: translateY(0);
}

.explorer-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 10px 16px;
  background: var(--bg-elevated);
  border-bottom: 1px solid var(--border-subtle);
}

.explorer-dots {
  display: flex;
  gap: 7px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: block;
}

.dot-red { background: #ff5f57; }
.dot-yellow { background: #febc2e; }
.dot-green { background: #28c840; }

.explorer-path {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-secondary);
  padding: 5px 12px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  max-width: 480px;
}

.path-icon {
  color: var(--text-tertiary);
  font-size: 11px;
}

.explorer-meta {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
  padding: 3px 8px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
}

.explorer-body {
  display: grid;
  grid-template-columns: 220px 1fr;
  min-height: 380px;
}

.explorer-sidebar {
  border-right: 1px solid var(--border-subtle);
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-section {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.sidebar-label {
  font-size: 10px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 4px 8px;
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  font-size: 12.5px;
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
  transition: background var(--t-fast);
}

.sidebar-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.sidebar-item.active {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.sidebar-icon {
  font-size: 10px;
  color: var(--text-muted);
}

.sidebar-icon-rule {
  color: #60a5fa;
}

.sidebar-icon-skill {
  color: var(--accent);
}

.sidebar-icon-agent {
  color: #a78bfa;
}

.sidebar-icon-kb {
  color: #fbbf24;
}

.sidebar-name {
  flex: 1;
}

.sidebar-count {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--text-muted);
  padding: 2px 6px;
  background: var(--bg-elevated);
  border-radius: 4px;
}

.explorer-main {
  padding: 20px 24px;
  overflow: auto;
}

.explorer-breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-tertiary);
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-hairline);
  margin-bottom: 20px;
}

.bc-sep {
  color: var(--text-muted);
}

.bc-current {
  color: var(--text-secondary);
}

.explorer-tree {
  display: grid;
  gap: 24px;
}

.tree-folder {
  opacity: 0;
  animation: fade-in-up 500ms var(--ease-out-quart) both;
  animation-delay: var(--delay);
}

.explorer-window.visible .tree-folder {
  opacity: 1;
}

.tree-folder-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 0;
  margin-bottom: 4px;
}

.tree-icon {
  font-size: 12px;
  color: var(--text-tertiary);
}

.tree-name {
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
}

.tree-count {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--text-muted);
  padding: 2px 6px;
  background: var(--bg-elevated);
  border-radius: 4px;
  margin-left: auto;
}

.tree-files {
  list-style: none;
  padding-left: 20px;
  border-left: 1px dashed var(--border-subtle);
  display: flex;
  flex-direction: column;
}

.tree-file {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 12px;
  font-family: var(--font-mono);
  font-size: 12px;
  border-radius: var(--radius-sm);
  transition: background var(--t-fast);
}

.tree-file:hover {
  background: var(--bg-hover);
}

.tree-file-icon {
  font-size: 10px;
  color: var(--text-muted);
}

.tree-file-icon-rule { color: #60a5fa; }
.tree-file-icon-skill { color: var(--accent); }
.tree-file-icon-agent { color: #a78bfa; }

.tree-file-name {
  color: var(--text-secondary);
  flex: 1;
}

.tree-file-size {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
}

.explorer-status {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px;
  background: var(--bg-elevated);
  border-top: 1px solid var(--border-subtle);
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent);
}

.status-dot-success {
  background: var(--accent);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
  animation: status-pulse 2.4s ease-in-out infinite;
}

.status-caret {
  display: inline-block;
  width: 6px;
  height: 11px;
  background: var(--accent);
  margin-left: 6px;
  vertical-align: text-bottom;
  border-radius: 1px;
  animation: caret-blink 1.1s steps(2, end) infinite;
}

.status-text {
  font-weight: 500;
}

@keyframes status-pulse {
  0%, 100% { box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15); }
  50% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0.06); }
}

@keyframes caret-blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

@media (max-width: 768px) {
  .explorer-body {
    grid-template-columns: 1fr;
  }
  .explorer-sidebar {
    display: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .status-dot-success,
  .status-caret {
    animation: none !important;
  }
  .status-caret {
    opacity: 0;
  }
}
</style>