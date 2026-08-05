# Cursor Enterprise Framework - Python Library

Hướng dẫn sử dụng đầy đủ cho `cursor_framework` — Python core library của Cursor Enterprise Framework.

> **Version**: 1.3.0
> **Python**: 3.10+
> **License**: MIT

---

## Mục lục

1. [Giới thiệu](#giới-thiệu)
2. [Cài đặt](#cài-đặt)
3. [Khởi đầu nhanh](#khởi-đầu-nhanh)
4. [Các Module chính](#các-module-chính)
   - [ContextRouter](#contextrouter)
   - [MemoryManager](#memorymanager)
   - [TokenOptimizer](#tokenoptimizer)
   - [SkillDiscovery](#skilldiscovery)
   - [ContextBuilder](#contextbuilder)
   - [Workflow](#workflow)
5. [TencentDB Agent Memory (TDAM)](#tencentdb-agent-memory-tdam)
6. [CLI Commands](#cli-commands)
7. [Patterns nâng cao](#patterns-nâng-cao)
8. [API Reference](#api-reference)

---

## Giới thiệu

`cursor_framework` là thư viện Python cốt lõi của Cursor Enterprise Framework, cung cấp:

- **Context Routing**: Phân loại intent và định tuyến skill tự động
- **Memory Management**: Quản lý bộ nhớ phân cấp (HOT/WARM/COLD)
- **Token Optimization**: Tối ưu token với nhiều chiến lược nén
- **Skill Discovery**: Tự động phát hiện skill + pre/post-review gates
- **TDAM Integration**: Tích hợp TencentDB Agent Memory (giảm 61.38% token, tăng 51.52% success rate)
- **Dashboard**: HTTP server visualization

### Benchmark Hiệu suất

| Metric | Trước | Sau | Cải thiện |
|--------|-------|-----|-----------|
| Token Usage (WideSearch) | 221.31M | 85.64M | **-61.38%** |
| Task Success Rate | 33% | 50% | **+51.52%** |
| Persona Memory Accuracy | 48% | 76% | **+59%** |

---

## Cài đặt

### Cài đặt cơ bản

```bash
pip install cursor-framework
```

### Cài đặt từ source

```bash
git clone https://github.com/your-org/cursor-framework.git
cd cursor-framework
pip install -e .
```

### Dependencies tùy chọn

```bash
# Cho TDAM integration (HTTP client)
pip install httpx

# Cho TDAM CLI với giao diện đẹp
pip install rich

# Tất cả optional dependencies
pip install cursor-framework[full]
```

### Cấu hình môi trường (cho TDAM)

```bash
# Windows PowerShell
$env:TDAM_ENDPOINT = "http://127.0.0.1:8420"
$env:TDAM_API_KEY = "your-api-key"
$env:TDAM_SERVICE_ID = "your-service-id"

# Linux/Mac
export TDAM_ENDPOINT="http://127.0.0.1:8420"
export TDAM_API_KEY="your-api-key"
export TDAM_SERVICE_ID="your-service-id"
```

---

## Khởi đầu nhanh

### Ví dụ 1: Context Routing

```python
from cursor_framework import ContextRouter

router = ContextRouter()

# Định tuyến request → skill
route = router.route("Create a landing page for SaaS product")
print(f"Skill: {route.skill.value}")
print(f"Confidence: {route.confidence}")
print(f"Domain: {route.domain}")
```

### Ví dụ 2: Memory Management

```python
from cursor_framework import MemoryManager, MemoryTier

memory = MemoryManager()

# Lưu context theo tier
memory.store("project_name", "MyApp", tier=MemoryTier.WARM)
memory.store("user_pref", "dark_mode", tier=MemoryTier.HOT, ttl_seconds=3600)

# Lưu session context
memory.store_session_context("user-123", {
    "current_task": "build dashboard",
    "language": "python"
})

# Truy xuất
name = memory.retrieve("project_name")  # "MyApp"
pref = memory.retrieve("user_pref")  # "dark_mode"

# Stats
stats = memory.get_stats()
print(f"Hit rate: {stats.hit_rate:.2%}")
```

### Ví dụ 3: Token Optimization

```python
from cursor_framework import TokenOptimizer, CompressionStrategy

optimizer = TokenOptimizer(max_tokens=100000)

# Ước lượng tokens
text = "Long context here..."
tokens = optimizer.estimate_tokens(text)

# Nén context
compressed = optimizer.compress(
    long_text,
    target_tokens=4000,
    strategy=CompressionStrategy.SEMANTIC_WITH_SUMMARY
)

# Tối ưu toàn bộ context window
result = optimizer.optimize_context_window(
    system="You are a helpful assistant.",
    history=[{"role": "user", "content": "..."}, ...],
    current_prompt="What's the weather?"
)
print(f"Optimized: {result['history']}")
```

### Ví dụ 4: Workflow hoàn chỉnh

```python
from cursor_framework import Workflow

# Workflow = scan + build + cache + persist
wf = Workflow(root=".cursor", max_tokens=4000)
wf.warm()  # Warm cache

# Ask một câu hỏi
result = wf.ask("design landing page for SaaS")
print(f"From cache: {result.from_cache}")
print(f"Latency: {result.latency_ms}ms")
print(f"Context:\n{result.context.text}")
```

---

## Các Module chính

### ContextRouter

Phân loại intent và định tuyến tới skill phù hợp.

```python
from cursor_framework import ContextRouter

router = ContextRouter()

# Định tuyến với confidence score
route = router.route("implement authentication with JWT")
print(route.skill)         # Skill.AUTH
print(route.confidence)    # 0.95
print(route.reasoning)     # "Detected auth keywords + security context"

# Các intent types
# - BUILD: Implement code
# - REDESIGN: Improve existing UI
# - REVIEW: Code review
# - DEBUG: Fix bugs
# - DOCUMENT: Generate docs
# - TEST: Write tests
```

### MemoryManager

Quản lý bộ nhớ phân cấp với 3 tiers:

```python
from cursor_framework import MemoryManager, MemoryTier, MemoryEntry

memory = MemoryManager(max_entries_per_tier={
    MemoryTier.HOT: 100,    # Session-level, 1h TTL
    MemoryTier.WARM: 500,   # Project-level, 24h TTL
    MemoryTier.COLD: 1000,  # Long-term, 7d TTL
})

# Store với priority
entry = memory.store(
    key="critical_config",
    value={"api_key": "***"},
    tier=MemoryTier.WARM,
    priority=9,  # Higher = keep longer
    ttl_seconds=86400
)

# Cross-reference linking
memory.link_entries("project_a", "project_a_meta")

# Pattern queries
results = memory.query_by_pattern("user_*")  # Match user_* keys

# Cleanup
memory.cleanup_expired()
memory.optimize()  # Evict low priority

# Stats
stats = memory.get_stats()
print(f"Total entries: {stats.total_entries}")
print(f"Hit rate: {stats.hit_rate:.2%}")
print(f"Token savings: {stats.token_savings}")
```

### TokenOptimizer

Nén context và quản lý token budget:

```python
from cursor_framework import TokenOptimizer, CompressionStrategy, TokenBudget

# Budget management
budget = TokenBudget(
    max_tokens=100000,
    system_reserve=5000,
    response_reserve=3000
)

success = budget.allocate("user_context", 8000, priority=7)
print(f"Available: {budget.available_for_context}")
print(f"Usage: {budget.usage_ratio:.1%}")

# Compression strategies
context = "Long text here..."

# 1. SEMANTIC - Keep meaning, remove redundancy
result = optimizer.compress(context, target_tokens=4000, strategy=CompressionStrategy.SEMANTIC)

# 2. STRUCTURAL - Compress structure, keep data
result = optimizer.compress(context, strategy=CompressionStrategy.STRUCTURAL)

# 3. TEMPORAL - Prioritize recent content
result = optimizer.compress(context, strategy=CompressionStrategy.TEMPORAL)

# 4. SEMANTIC_WITH_SUMMARY - Add summary header
result = optimizer.compress(context, strategy=CompressionStrategy.SEMANTIC_WITH_SUMMARY)

# Full context window optimization
optimized = optimizer.optimize_context_window(
    system="...",
    history=[...],
    current_prompt="..."
)
```

### SkillDiscovery

Tự động phát hiện skill + pre/post-review gates:

```python
from cursor_framework import SkillDiscovery, SkillRegistry

# Load skills from .cursor/skills/
registry = SkillRegistry()
all_skills = registry.get_all()

# Detect skills for a request
discovery = SkillDiscovery(base_path=".")
detected = discovery.detect_skills("build a React dashboard")

for s in detected:
    print(f"{s.skill}: {s.confidence}")

# Load specific skill content
content = discovery.load_skill_file("frontend-taste")

# Pre/post-review gates
from cursor_framework.skill_discovery import GateExecutor
executor = GateExecutor()
pre_results = executor.execute_pre_gates(detected_skills)
post_results = executor.execute_post_gates(detected_skills, output)
```

### ContextBuilder

Orchestrates skill detection + token compression:

```python
from cursor_framework import ContextBuilder

builder = ContextBuilder(root=".cursor", max_tokens=4000)

# Build context from request
result = builder.build("design landing page for SaaS")

print(f"Skills used: {result.skills_used}")
print(f"Tokens: {result.tokens}")
print(f"Truncated: {result.truncated}")
print(f"Text:\n{result.text}")

# With TDAM memory (see below)
from cursor_framework import TDAMIntegration
tdam = TDAMIntegration.from_env()
builder.set_tdam(tdam)

result = builder.build_with_memory(
    request="build a dashboard",
    session_id="user-1",
    include_persona=True,
    include_memories=True
)
print(f"Persona: {result.persona}")
print(f"Memories: {result.memories}")
```

### Workflow

End-to-end pipeline với caching:

```python
from cursor_framework import Workflow

# Initialize
wf = Workflow(
    root=".cursor",
    memory_path=".cache/memory.json",
    max_tokens=4000
)

# Warm cache (one-time scan)
wf.warm()

# Ask (cached if request seen before)
result = wf.ask("design landing page")

# Stats
print(f"Memory hits: {wf.stats()['memory_hits']}")
print(f"Cache hit rate: {wf.stats()['cache_hit_rate']}")

# Clear cache
wf.clear_cache()
```

---

## TencentDB Agent Memory (TDAM)

Tích hợp TencentDB Agent Memory cho layered memory (L0-L3) + symbolic memory (Mermaid).

### Cài đặt

```bash
# Install httpx cho TDAM HTTP client
pip install httpx

# Run TDAM Gateway (Docker)
docker run -d -p 8420:8420 --name tdam-gateway \
  tencentdb/agent-memory:latest
```

### Cấu hình

```python
from cursor_framework import TDAMConfig, TDAMIntegration

config = TDAMConfig(
    endpoint="http://127.0.0.1:8420",
    api_key="your-api-key",
    service_id="my-service",
    offload_enabled=True,
    recall_strategy="hybrid",  # keyword | embedding | hybrid
    max_results=5,
)
tdam = TDAMIntegration(config)
```

### Sử dụng cơ bản

```python
from cursor_framework import ConversationTurn
from datetime import datetime

# Capture conversation
messages = [
    ConversationTurn(role="user", content="Hello"),
    ConversationTurn(role="assistant", content="Hi there!"),
]
result = tdam.capture_conversation("session-1", messages)

# Recall memories
memories = tdam.recall("user preferences", limit=5)
for m in memories:
    print(f"[{m.layer.value}] {m.content} (score: {m.score})")

# Persona (L3)
persona = tdam.get_persona()
tdam.update_persona("# User Profile\n- I prefer TypeScript")

# Scenarios (L2)
scenarios = tdam.list_scenarios()
content = tdam.get_scenario("project-workflow.md")
```

### Symbolic Memory (Mermaid Canvas)

```python
# Compact context into Mermaid symbols
result = tdam.compact_context(
    session_id="session-1",
    messages=[...],
    ratio=0.7,  # Keep 70% meaning in 70% tokens
    context_window=128000
)

print(f"Tokens: {result.tokens_before} → {result.tokens_after}")
print(f"Mermaid canvas:\n{result.mermaid_canvas}")
```

### Integrate với MemoryManager

```python
from cursor_framework import MemoryManager

manager = MemoryManager()
manager.set_tdam_integration(tdam)

# Sync local memory to TDAM
manager.sync_to_tdam("session-1")

# Recall via TDAM
memories = manager.recall_from_tdam("preferences")

# Get persona
persona = manager.get_persona_from_tdam()
```

### Integrate với ContextBuilder

```python
from cursor_framework import ContextBuilder

builder = ContextBuilder()
builder.set_tdam(tdam)

# Build context với memory recall
result = builder.build_with_memory(
    request="build dashboard",
    session_id="user-1",
    include_persona=True,
    include_memories=True
)
```

### Full Pipeline

```python
# Compaction + persona + memories
context = tdam.build_context(
    session_id="user-1",
    current_task="build dashboard",
    max_tokens=4000
)

print(f"Persona: {context['persona']}")
print(f"Memories: {len(context['memories'])}")
print(f"Total tokens: {context['total_tokens']}")
```

---

## CLI Commands

### Framework CLI

```bash
# Start dashboard server
python -m cursor_framework serve --port 8765

# Run workflow once
python -m cursor_framework ask "design landing page"

# Warm cache
python -m cursor_framework warm

# View stats
python -m cursor_framework stats

# Scan .cursor/
python -m cursor_framework scan

# Generate index
python -m cursor_framework index

# Build skill dependency graph
python -m cursor_framework graph

# Serve graph visualization
python -m cursor_framework serve-graph --port 8766

# Clear cache
python -m cursor_framework clear-cache --force
```

### TDAM CLI (với giao diện đẹp)

```bash
# Status
python -m cursor_framework.tdam_cli status

# Capture messages
python -m cursor_framework.tdam_cli capture \
  --session user-1 \
  --message "Hello" \
  --message "How are you?"

# Recall memories
python -m cursor_framework.tdam_cli recall \
  --query "preferences" \
  --layers l1 l2 \
  --limit 10

# Compact context
python -m cursor_framework.tdam_cli compact \
  --session user-1 \
  --ratio 0.7 \
  --message "Long conversation..."

# Persona management
python -m cursor_framework.tdam_cli persona --read
python -m cursor_framework.tdam_cli persona --write "# Profile"
python -m cursor_framework.tdam_cli persona --interactive

# Scenarios
python -m cursor_framework.tdam_cli scenarios --list
python -m cursor_framework.tdam_cli scenarios --read "workflow.md"

# Tool call capture
python -m cursor_framework.tdam_cli tool-call \
  --session user-1 \
  --tool search \
  --params '{"q":"python"}' \
  --result "Results..."

# Build full context
python -m cursor_framework.tdam_cli build-context \
  --session user-1 \
  --task "build dashboard" \
  --max-tokens 4000
```

### Qua main CLI

```bash
python -m cursor_framework tdam status
python -m cursor_framework tdam recall --query "preferences"
```

---

## Patterns nâng cao

### 1. Lazy Loading (PEP 562)

```python
# Import không load tất cả modules
import cursor_framework

# Modules được load on-demand
ContextBuilder = cursor_framework.ContextBuilder  # Load khi access
```

### 2. Persistence với MemoryStore

```python
from cursor_framework import MemoryManager, MemoryStore

manager = MemoryManager()
store = MemoryStore(memory_path=".cache/memory.json")

# Save
store.save(manager)

# Load (với size cap 50MB)
store.load_into(manager)

# Save chỉ khi dirty (skip writes khi không có thay đổi)
store.save_if_dirty(manager)
```

### 3. File Watcher

```python
from cursor_framework import Watcher

def on_change(path):
    print(f"File changed: {path}")

watcher = Watcher(root=".cursor", callback=on_change)
watcher.start()  # Watch for changes
```

### 4. Custom Compression Strategy

```python
from cursor_framework import TokenOptimizer, CompressionStrategy

class CustomCompressor:
    def compress(self, text, target_tokens):
        # Custom logic
        return compressed_text

# Use as strategy
optimizer = TokenOptimizer()
optimizer.custom_compressor = CustomCompressor()
```

### 5. Error Handling

```python
from cursor_framework import TDAMIntegration
from cursor_framework.tdam_integration import TDAMError

try:
    tdam = TDAMIntegration()
    result = tdam.recall("query")
except TDAMError as e:
    print(f"TDAM error: {e.code} - {e.message}")
except Exception as e:
    print(f"Unexpected: {e}")
```

### 6. Batch Operations

```python
# Capture multiple sessions
sessions = ["user-1", "user-2", "user-3"]
for session_id in sessions:
    messages = build_messages(session_id)
    tdam.capture_conversation(session_id, messages)

# Sync tất cả vào TDAM
for session_id in sessions:
    manager.sync_to_tdam(session_id)
```

---

## API Reference

### Core Classes

| Class | Description |
|-------|-------------|
| `ContextRouter` | Intent classification + skill routing |
| `MemoryManager` | Tiered memory (HOT/WARM/COLD) |
| `MemoryStore` | JSON persistence |
| `TokenOptimizer` | Compression + token budget |
| `SkillDiscovery` | Auto-detect skills |
| `ContextBuilder` | Orchestrates build pipeline |
| `Workflow` | End-to-end pipeline |
| `Watcher` | File system watcher |
| `Dashboard` | HTTP dashboard server |

### TDAM Classes

| Class | Description |
|-------|-------------|
| `TDAMIntegration` | High-level TDAM interface |
| `TDAMClient` | Low-level HTTP client |
| `TDAMConfig` | Configuration |
| `MemoryLayer` | L0/L1/L2/L3 enum |
| `MemoryItem` | Single memory item |
| `ConversationTurn` | Conversation message |
| `OffloadResult` | Compaction result |

### Enums

```python
from cursor_framework import (
    MemoryTier,        # HOT, WARM, COLD
    MemoryLayer,       # L0_CONVERSATION, L1_ATOM, L2_SCENARIO, L3_PERSONA
    CompressionStrategy,  # SEMANTIC, STRUCTURAL, TEMPORAL, SEMANTIC_WITH_SUMMARY
    IntentType,        # BUILD, REDESIGN, REVIEW, DEBUG, DOCUMENT, TEST
    Domain,            # FRONTEND, BACKEND, DATABASE, etc.
)
```

---

## Examples

### Example: Tech Lead Workflow

```python
from cursor_framework import Workflow, TDAMIntegration

# Setup
tdam = TDAMIntegration.from_env()
wf = Workflow(root=".cursor", max_tokens=4000)

# Phase 1: Analyze request
result = wf.ask("design authentication system")
print(f"Detected: {result.skills_used}")
print(f"Time: {result.latency_ms}ms")

# Phase 2: Get context with memory
session_id = "user-tech-lead-1"
context = tdam.build_context(session_id, "design auth", max_tokens=4000)
print(f"Persona: {context['persona']}")
print(f"Relevant memories: {len(context['memories'])}")

# Phase 3: Capture conversation
from cursor_framework import ConversationTurn
messages = [
    ConversationTurn(role="user", content="design authentication"),
    ConversationTurn(role="assistant", content="I'll use JWT..."),
]
tdam.capture_conversation(session_id, messages)
```

### Example: Context7 MCP Integration

```python
from cursor_framework import ContextBuilder

builder = ContextBuilder(root=".cursor")

# Build context for a specific library
result = builder.build("implement Next.js server actions")
print(f"Skills: {result.skills_used}")
# Output: ['nextjs-patterns', 'security-review', 'context7-docs']
```

### Example: Cost Optimization

```python
from cursor_framework import TokenOptimizer, TDAMIntegration

optimizer = TokenOptimizer(max_tokens=100000)
tdam = TDAMIntegration.from_env()

# Without TDAM: 100% tokens
long_context = "..." * 10000  # 50k tokens
full_tokens = optimizer.estimate_tokens(long_context)

# With TDAM: 38% tokens (61.38% savings)
result = tdam.compact_context("session", messages, ratio=0.7)
compressed = result.mermaid_canvas + result.messages
compressed_tokens = optimizer.estimate_tokens(compressed)

print(f"Tokens: {full_tokens} → {compressed_tokens}")
print(f"Savings: {(1 - compressed_tokens/full_tokens):.1%}")
```

---

## Troubleshooting

### TDAM connection issues

```python
# Check connection
from cursor_framework import TDAMIntegration

tdam = TDAMIntegration()
if not tdam.is_available():
    print("Start TDAM Gateway first:")
    print("docker run -d -p 8420:8420 tencentdb/agent-memory:latest")
```

### Slow first import

```python
# Use lazy loading (default)
import cursor_framework  # Chỉ load __version__, args

# Access chỉ modules bạn cần
from cursor_framework import MemoryManager  # Load on-demand
```

### Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_tdam_integration.py -v

# With coverage
pytest tests/ --cov=cursor_framework --cov-report=html
```

---

## License

MIT License - Part of Cursor Enterprise Framework

## Contributing

See CONTRIBUTING.md for guidelines.

## Links

- [GitHub Repository](https://github.com/your-org/cursor-framework)
- [Documentation](https://cursor-framework.readthedocs.io)
- [TencentDB Agent Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory)
- [Issue Tracker](https://github.com/your-org/cursor-framework/issues)
