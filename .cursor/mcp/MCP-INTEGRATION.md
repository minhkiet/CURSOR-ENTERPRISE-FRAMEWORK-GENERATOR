# Cursor Enterprise Framework - MCP Integration Guide

> **Version:** 1.0.0 | **Framework:** 3.1.0 | **Created:** 2026-08-09

## Tổng quan

Đã tạo **3 MCP servers** để tự động hóa việc gọi rules, skills, agents với tính năng tối ưu token và bộ nhớ:

```
tools/
├── cursor-framework-mcp/     # Core Framework Registry (9 tools)
├── cursor-autopilot-mcp/     # Auto-Execution Engine (8 tools)  
├── cursor-memory-mcp/        # Memory & Context Management (9 tools)
├── mcp-config-template.json   # MCP settings template
└── setup-mcp.ps1            # Setup script
```

---

## MCP Servers

### 1. cursor-framework (Core Registry)

**Path:** `tools/cursor-framework-mcp/`

Cung cấp registry và caching cho tất cả rules, skills, agents trong framework.

| Tool | Mô tả |
|------|--------|
| `get_rule` | Load rule theo ID/path với caching |
| `get_skill` | Load skill với dependencies |
| `get_agent` | Load agent persona |
| `analyze_task` | Phân tích request → gợi ý rules/skills/agents |
| `load_skill_bundle` | Preload skill bundle (A-E) |
| `get_essential_skills` | Load karpathy, ponytail, full-output |
| `clear_cache` | Xóa cache để giải phóng bộ nhớ |
| `get_framework_status` | Xem memory/token usage |
| `optimize_framework` | Tối ưu cache tự động |

**Cache Config:**
- Max 20 rules, 30 skills, 10 agents
- LRU eviction khi đạt limit
- TTL 30 phút

---

### 2. cursor-autopilot (Auto-Execution)

**Path:** `tools/cursor-autopilot-mcp/`

Tự động thực thi workflows dựa trên task analysis.

| Tool | Mô tả |
|------|--------|
| `auto_execute` | Analyze + auto-load + execute |
| `execute_workflow` | Chạy predefined workflow |
| `run_gate_validation` | Run pre/post gates |
| `get_workflow_status` | Xem workflow status |
| `abort_workflow` | Dừng workflow |
| `list_workflows` | List available workflows |
| `estimate_cost` | Ước tính token/time |
| `suggest_optimization` | Gợi ý tối ưu |

**Predefined Workflows:**

| Workflow | Steps |
|----------|-------|
| `build` | karpathy-coding → ponytail → full-output → code-reviewer |
| `fix` | debugger → karpathy-coding → code-reviewer |
| `review` | analyze → load_reviewer → run_review |
| `test` | test-engineer → analyze_coverage → run_tests |
| `security` | security-review → security-auditor → vietnam-payment-review (if payment) |
| `perf` | web-performance-auditor → perf_optimization |

---

### 3. cursor-memory (Context & Memory)

**Path:** `tools/cursor-memory-mcp/`

Quản lý conversation context và memory với token optimization.

| Tool | Mô tả |
|------|--------|
| `store_memory` | Lưu fact/conclusion vào memory |
| `recall_memory` | Recall memories liên quan |
| `compact_context` | Nén context để tiết kiệm token |
| `summarize_history` | Tóm tắt conversation history |
| `get_context_stats` | Token usage breakdown |
| `prune_context` | Xóa context không liên quan |
| `export_memory` | Export memories ra JSON |
| `import_memory` | Import memories từ JSON |
| `sync_to_disk` | Persist memory to disk |

**Memory Tiers:**
- **Short-term:** Current session
- **Medium-term:** Per-project
- **Long-term:** Persistent (compacted)

---

## Cài đặt

### Bước 1: Cài đặt Dependencies

```powershell
cd tools/cursor-framework-mcp
pip install -r requirements.txt

cd ../cursor-autopilot-mcp
pip install -r requirements.txt

cd ../cursor-memory-mcp
pip install -r requirements.txt
```

### Bước 2: Copy MCP Config

**Windows:**
```powershell
copy tools\mcp-config-template.json $env:USERPROFILE\.cursor\mcp.json
```

**Linux/Mac:**
```bash
cp tools/mcp-config-template.json ~/.config/cursor/mcp.json
```

### Bước 3: Khởi động lại Cursor

Sau khi cập nhật `mcp.json`, restart Cursor để load các MCP servers.

---

## Sử dụng

### Trong Cursor Chat

```
// Phân tích task và gợi ý skills
analyze_task("Build a landing page with hero, pricing, testimonials")

// Load essential skills
get_essential_skills()

// Preload Full-Stack bundle
load_skill_bundle(bundle="B")

// Xem cache status
get_framework_status()

// Tự động execute workflow
execute_workflow("build", task="Create user authentication")

// Lưu memory
store_memory(key="auth-pattern", value="Use JWT with refresh tokens")

// Nén context
compact_context()
```

### Auto-Loading Flow

```
User Request
    ↓
analyze_task() → detect domain
    ↓
auto-load essential skills (karpathy, ponytail, full-output)
    ↓
load domain-specific skills based on task
    ↓
execute with pre/post gates
    ↓
track tokens & optimize cache
```

---

## Tối ưu Token & Memory

### Memory Optimization

| Feature | Config | Default |
|---------|--------|---------|
| Rule cache | `CURSOR_FRAMEWORK_CACHE_MAX_RULES` | 20 |
| Skill cache | `CURSOR_FRAMEWORK_CACHE_MAX_SKILLS` | 30 |
| Agent cache | `CURSOR_FRAMEWORK_CACHE_MAX_AGENTS` | 10 |
| Cache TTL | `CURSOR_FRAMEWORK_CACHE_TTL_MINUTES` | 30 |
| Context budget | `CURSOR_CONTEXT_TOKEN_BUDGET` | 100000 |

### Auto-Pruning

- Items unused > 30 min tự động evicted
- LRU eviction khi cache full
- Memory auto-compact khi approaching budget

### Bundle Loading

Load bundles strategically để tránh over-fetch:

| Bundle | Contents | Use Case |
|--------|----------|----------|
| A | Web & Dashboard | Landing pages, portfolios |
| B | Full-Stack | Complete implementations |
| C | AI/ML | RAG, autonomous tasks |
| D | Database | Schema, migrations |
| E | Infrastructure | Deploy, CI/CD |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Cursor Chat                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              cursor-framework-mcp                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │  Registry   │ │   Loader    │ │   Cache     │          │
│  │ 42 rules    │ │ Lazy load   │ │ LRU + TTL   │          │
│  │ 64 skills   │ │ Token track │ │ Auto-evict  │          │
│  │ 20 agents   │ │             │ │             │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│cursor-autopilot │  │ cursor-memory   │  │   Cursor IDE    │
│                 │  │                 │  │                 │
│ • Workflow exec │  │ • Short-term    │  │ • Chat context  │
│ • Gate validate │  │ • Medium-term   │  │ • File editing  │
│ • Cost estimate │  │ • Long-term     │  │ • Terminal      │
│ • Suggestions   │  │ • Compression   │  │ • Browser       │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## Integration với Rules

Các MCP servers tự động:

1. **Read rules** từ `.cursor/rules/*.mdc`
2. **Load skills** từ `.cursor/skills/*/SKILL.md`
3. **Use agent personas** từ `.cursor/AGENTS.md`
4. **Follow skill-registry** cho trigger mappings
5. **Respect gate mappings** cho pre/post validation

---

## Troubleshooting

### MCP không hoạt động

```powershell
# Verify Python path
python -c "import mcp; print(mcp.__version__)"

# Check server imports
python -m cursor_framework_mcp.server --help

# View logs
$env:PYTHONPATH = "tools/cursor-framework-mcp"
python -m cursor_framework_mcp.server
```

### Cache issues

```python
# Clear all cache
clear_cache(kind="all")

# Check status
get_framework_status()

# Force optimize
optimize_framework(target_fill_ratio=0.7)
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-08-09 | Initial release: 3 MCP servers, 26 tools |

---

## References

- Framework: [thaofvn-coca06/2026](https://github.com/thaofvn-coca06/2026)
- Skills: `.cursor/SKILL-INDEX.md`
- Agents: `.cursor/AGENTS.md`
- Rules: `.cursor/rules/`
