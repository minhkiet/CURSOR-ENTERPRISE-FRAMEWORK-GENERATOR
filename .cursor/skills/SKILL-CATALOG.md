# Cursor Enterprise Framework Generator
## Hướng Dẫn Sử Dụng - Skill System

**Phiên bản:** 1.2.0  
**Cập nhật:** 2026-06-26  
**Tổng số Skills:** 17

---

## Tổng Quan Kiến Trúc

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CURSOR ENTERPRISE FRAMEWORK                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────┐    ┌──────────────────┐    ┌─────────────────────────┐ │
│   │  USER       │───►│  SKILL DETECTION  │───►│  SKILL EXECUTION       │ │
│   │  REQUEST    │    │  ENGINE          │    │  (Pre → Code → Post)   │ │
│   │  (any lang) │    │  Auto-Discovery  │    │                         │ │
│   └─────────────┘    └──────────────────┘    └─────────────────────────┘ │
│                              │                              │              │
│                              ▼                              ▼              │
│                    ┌──────────────────┐          ┌─────────────────────┐  │
│                    │  SKILL MATRIX   │          │  KARPATHY-CODING    │  │
│                    │  Keywords       │          │  OVERLAY (always)   │  │
│                    │  Confidence     │          │  Simplicity First   │  │
│                    └──────────────────┘          └─────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phần 1: Skill Detection Engine

### 1.1 Cách Hoạt Động

Khi bạn gửi yêu cầu, hệ thống tự động:

1. **Parse Request** → Trích xuất keywords và intent signals
2. **Match Matrix** → Đối chiếu với Skill Keyword Matrix
3. **Calculate Confidence** → Tính điểm confidence (0-1)
4. **Determine Combination** → Xác định skill combination phù hợp
5. **Output Decision** → Hiển thị skills được chọn + review gates

### 1.2 Confidence Thresholds

| Threshold | Hành động |
|-----------|-----------|
| **≥ 0.75** | AUTO-SELECT - Không cần xác nhận |
| **0.50-0.74** | SUGGEST - Đề nghị áp dụng |
| **< 0.50** | AMBIGUOUS - Cần hỏi làm rõ |

### 1.3 Decision Tree

```
YÊU CẦU NHẬN ĐƯỢC
       │
       ▼
┌─────────────────────────────┐
│ PAYMENT? (MoMo, SePay...)  │──YES──► security + vietnam-payment
└─────────────┬───────────────┘
              │ NO
              ▼
┌─────────────────────────────┐
│ SECURITY? (vuln, OWASP...) │──YES──► security-review
└─────────────┬───────────────┘
              │ NO
              ▼
┌─────────────────────────────┐
│ FRONTEND? (UI, landing...) │
└─────────────┬───────────────┘
              │
       ┌──────┴──────┐
       │             │
      REDESIGN      BUILD
       │             │
       ▼             ▼
  redesign +      taste +
  full-output     full-output
```

---

## Phần 2: Danh Sách Skills (17 Skills)

### 2.1 Skills Chính (Core)

| # | Skill | Mô tả | Priority | Auto-Apply |
|---|-------|-------|----------|------------|
| 1 | **frontend-taste** | Premium frontend design. Anti-slop. Cho landing pages, portfolios. | HIGH | ❌ |
| 2 | **frontend-redesign** | Upgrade UI hiện có. Không phá vỡ functionality. | HIGH | ❌ |
| 3 | **full-output** | Không truncation, không skeleton, đầy đủ code. | MANDATORY | ❌ |
| 4 | **frontend-review** | Quality review. Correctness, design, a11y, performance. | MANDATORY | ✅ |
| 5 | **security-review** | OWASP Top 10, LLM/AI Security, CVE, pentest. | HIGH | ❌ |
| 6 | **vietnam-payment-review** | MoMo, SePay, PayOS, ZaloPay, VNPay, VietQR. | HIGH | ❌ |

### 2.2 Skills Overlay (Luôn chạy)

| # | Skill | Mô tả | Priority | Auto-Apply |
|---|-------|-------|----------|------------|
| 7 | **karpathy-coding** | Simplicity first. Surgical changes. Think before coding. | MANDATORY | ✅ (always) |

### 2.3 Skills Tiện Ích (Utility)

| # | Skill | Mô tả | Priority | Auto-Apply |
|---|-------|-------|----------|------------|
| 8 | **ponytail** | Lazy Senior Dev. Minimal code. YAGNI. | MEDIUM | ❌ |
| 9 | **visual-explainer** | HTML diagrams, architecture, flowcharts. | MEDIUM | ❌ |
| 10 | **open-design** | Design system integration. Prototype, dashboard. | MEDIUM | ❌ |
| 11 | **document-ocr** | Tesseract OCR. Vietnamese, English, Chinese. | MEDIUM | ❌ |

### 2.4 Skills Đặc Biệt (Special)

| # | Skill | Mô tả | Priority | Auto-Apply |
|---|-------|-------|----------|------------|
| 12 | **bazi** | 四柱八字命理分析. Chinese fortune telling. | LOW | ❌ |
| 13 | **vietnam-address** | 34 tỉnh/thành, ~11,000 phường/xã. Cascading dropdown. | MEDIUM | ❌ |

### 2.5 Skills Knowledge & RAG (Knowledge)

| # | Skill | Mô tả | Priority | Auto-Apply |
|---|-------|-------|----------|------------|
| 14 | **weknora-kb** | RAG knowledge platform. Hybrid search, Wiki Mode. | MEDIUM | ❌ |
| 15 | **weknora-agent** | ReAct Agent. Autonomous reasoning, multi-step. | MEDIUM | ❌ |
| 16 | **pixelrag** | Visual RAG. Screenshot-based. 18.1% accuracy improvement. | MEDIUM | ❌ |

---

## Phần 3: Skill Combinations

### 3.1 Frontend Tasks

| Task Type | Skills Applied | Review Gates |
|-----------|---------------|--------------|
| Landing page mới | taste + full-output + review | taste-pre + taste-post + fulloutput-pre + review-pre |
| Redesign existing | redesign + full-output + review | redesign-pre + redesign-post + fulloutput-pre + review-pre |
| Code review only | review (standalone) | review-pre + review-post |
| Multi-file impl | full-output + review | fulloutput-pre + fulloutput-post + review-pre |

### 3.2 Security Tasks

| Task Type | Skills Applied | Review Gates |
|-----------|---------------|--------------|
| Vulnerability | security-review | security-pre + security-post |
| Payment integration | security + payment-review | security-pre + payment-pre + security-post |
| API security | security-review | security-pre + security-post |

### 3.3 Knowledge & RAG Tasks

| Task Type | Skills Applied | Review Gates |
|-----------|---------------|--------------|
| Knowledge base setup | weknora-kb + full-output | weknora-pre + weknora-post + fulloutput-pre |
| RAG implementation | weknora-kb + rag | weknora-pre + rag-pre + weknora-post |
| FAQ system | weknora-kb | weknora-pre + weknora-post |
| Visual RAG | pixelrag + full-output | pixelrag-pre + pixelrag-post + fulloutput-pre |
| Hybrid (KB + Visual) | pixelrag + weknora-kb | pixelrag-pre + weknora-pre + pixelrag-post |

---

## Phần 4: Execution Protocol (6 Bước)

```
═══════════════════════════════════════════════════════════════════════
                    SKILL EXECUTION FLOWCHART
═══════════════════════════════════════════════════════════════════════

  REQUEST RECEIVED
        │
        ▼
  ┌─────────────────────────┐
  │ 0. SKILL DETECTION      │  Auto-Discovery
  │    ★ PRIMARY: [skill]  │  Parse → Match → Calculate → Load
  │    ○ SECONDARY: [...]   │
  └──────────┬──────────────┘
             ▼
  ┌─────────────────────────┐
  │ 1. PRE-REVIEW GATE     │  TRƯỚC KHI VIẾT CODE
  │    ALL PASS → continue │  Scope lock, Design direction
  │    FAIL → STOP         │  Dial values, Anti-default
  └──────────┬──────────────┘
             ▼
  ┌─────────────────────────┐
  │ 2. IMPLEMENTATION       │  VIẾT CODE
  │    Track deliverables  │  Full code, NO placeholders
  │    If limit → PAUSE    │  NO em-dashes, NO AI-slop
  └──────────┬──────────────┘
             ▼
  ┌─────────────────────────┐
  │ 3. POST-REVIEW GATE     │  SAU KHI VIẾT CODE
  │    ALL PASS → deliver  │  Design/Taste/A11y/Perf
  │    FAIL → FIX + re-run │  Correctness/State/Testing
  └──────────┬──────────────┘
             ▼
  ┌─────────────────────────┐
  │ 4. DELIVERY            │  Code + review notes
  └─────────────────────────┘

═══════════════════════════════════════════════════════════════════════
```

### Bước 0: Skill Detection (Auto-Discovery)
- Parse request → extract keywords
- Match against Skill Keyword Matrix
- Calculate confidence scores
- Output: Skills Selected + Review Gates

### Bước 1: Pre-Review Gate (TRƯỚC KHI VIẾT CODE)
- Lock scope
- Declare design direction
- Set dial values (VARIANCE/MOTION/DENSITY)
- Anti-default discipline check
- **PASS → continue to code**
- **FAIL → STOP, fix first**

### Bước 2: Implementation (VIẾT CODE)
- Full code, NO placeholders
- NO `// ...`, `// TODO`, skeleton
- NO em-dashes (`—`)
- Follow anti-default discipline
- Track deliverables

### Bước 3: Post-Review Gate (SAU KHI VIẾT CODE)
- Design & Taste check
- Accessibility check
- Performance check
- Correctness check
- **ALL PASS → deliver**
- **ANY FAIL → fix + re-run**

### Bước 4: Delivery
- Send code to user
- List delivered files
- Note any items fixed during review
- Document intentional exceptions

### Bước 5: Pause/Resume (Long Output)
- Write to clean breakpoint
- Insert PAUSE marker
- Resume on "continue"

---

## Phần 5: Anti-Patterns & Rules

### 5.1 Tuyệt Đối Cấm

| Bypass | Lý do cấm |
|--------|-----------|
| Skip pre-review | Không có design direction, scope không locked |
| Skip post-review | Không verify quality |
| Partial review | Mỗi item bảo vệ một quality dimension |
| Review-after-delivery | Bug discover sau khi user nhận code = bad UX |
| Deliver partial | Violates full-output enforcement |
| Skip anti-default | AI-slop patterns vẫn còn trong output |
| Bỏ qua em-dash ban | Zero tolerance |

### 5.2 Legitimate Exceptions

| Exception | Khi nào allowed | Yêu cầu |
|-----------|-----------------|---------|
| Intentional design | Brief đặc biệt yêu cầu | Ghi rõ trong design read |
| Performance trade-off | Có measurable justification | Ghi rõ trade-off |
| Legacy constraint | Legacy code không cho phép | Document + workaround plan |

---

## Phần 6: Keyword Quick Reference

### Frontend
- `landing page` → frontend-taste (0.95)
- `redesign` → frontend-redesign (0.95)
- `full implementation` → full-output (0.95)
- `review` → frontend-review (0.95)

### Security
- `security` / `vulnerability` → security-review (0.95)
- `MoMo` / `SePay` / `PayOS` → vietnam-payment-review (0.95)

### Knowledge
- `rag` / `knowledge base` → weknora-kb (0.95)
- `agent mode` / `react` → weknora-agent (0.95)
- `pixelrag` / `visual rag` → pixelrag (0.95)
- `địa chỉ` / `tỉnh` / `quận` → vietnam-address (0.95)

### Vietnam Payment Keywords
- `MoMo` → vietnam-payment-review (0.95)
- `SePay` → vietnam-payment-review (0.95)
- `PayOS` → vietnam-payment-review (0.95)
- `ZaloPay` → vietnam-payment-review (0.95)
- `VNPay` → vietnam-payment-review (0.95)
- `VietQR` → vietnam-payment-review (0.95)

### Vietnam Address Keywords
- `địa chỉ Việt Nam` → vietnam-address (0.95)
- `tỉnh` / `thành phố` → vietnam-address (0.90)
- `quận` / `huyện` → vietnam-address (0.90)
- `phường` / `xã` → vietnam-address (0.90)
- `shipping address` → vietnam-address (0.90)

---

## Phần 7: Dependencies & Auto-Install

### System Dependencies

| Skill | Dependency | Required |
|-------|-----------|----------|
| document-ocr | Tesseract OCR | Yes |
| weknora-kb | WeKnora CLI + Docker | Yes |
| weknora-agent | WeKnora CLI | Yes |
| pixelrag | pixelrag + playwright + chromium | Yes |

### Auto-Install Config

```json
{
  "enabled": true,
  "promptBeforeInstall": true,
  "installOptional": true,
  "checkBeforeRun": true,
  "verbose": true,
  "continueOnError": true,
  "autoSync": true,
  "syncInterval": 3600
}
```

---

## Phần 8: Skill Registry Chi Tiết

### frontend-taste
**Path:** `.cursor/skills/frontend-taste/SKILL.md`  
**Kích hoạt:** landing page, portfolio, marketing site, greenfield frontend  
**Pre-Gate:** Design read declaration, Anti-default check, Design system selection  
**Post-Gate:** Layout, Typography, Assets, Motion, States, Performance

### frontend-redesign
**Path:** `.cursor/skills/frontend-redesign/SKILL.md`  
**Kích hoạt:** cải thiện/redesign site/app hiện có  
**Pre-Gate:** Scan codebase, Audit current state, Classify redesign mode  
**Post-Gate:** Functionality preserved, Design quality, Accessibility, SEO

### full-output
**Path:** `.cursor/skills/full-output/SKILL.md`  
**Kích hoạt:** full implementation, complete, no TODO, not skeleton  
**Pre-Gate:** Scope lock, Deliverable count  
**Post-Gate:** Completeness check, Quality check, File structure

### frontend-review
**Path:** `.cursor/skills/frontend-review/SKILL.md`  
**Kích hoạt:** review, quality check, audit  
**Pre-Gate:** Scope analysis, Quality plan  
**Post-Gate:** Correctness, Design, Accessibility, Performance, State, Testing

### security-review
**Path:** `.cursor/skills/security-review/SKILL.md`  
**Kích hoạt:** security, vulnerability, pentest, OWASP, CVE  
**Pre-Gate:** Threat modeling, Security requirements, Design review  
**Post-Gate:** Auth, Input validation, Data protection, API security, LLM security

### vietnam-payment-review
**Path:** `.cursor/skills/vietnam-payment-review/SKILL.md`  
**Kích hoạt:** MoMo, SePay, PayOS, ZaloPay, VNPay, VietQR  
**Pre-Gate:** Payment flow analysis, Security requirements  
**Post-Gate:** Integration correctness, Webhook security, Error handling

### karpathy-coding
**Path:** `.cursor/skills/karpathy-coding/SKILL.md`  
**Kích hoạt:** (ALWAYS - overlay với mọi task)  
**Pre-Gate:** Think before coding, Simplicity check, Surgical scope, Goal definition  
**Post-Gate:** Implementation verification, Simplicity re-check, Goal achievement

### vietnam-address
**Path:** `.cursor/skills/vietnam-address/SKILL.md`  
**Kích hoạt:** địa chỉ Việt Nam, tỉnh/thành/phố, quận/huyện/phường/xã  
**Features:** Cascading dropdown, Autocomplete, Validation  
**Data:** 34 tỉnh/thành, ~11,000 phường/xã

### weknora-kb
**Path:** `.cursor/skills/weknora-kb/SKILL.md`  
**Kích hoạt:** knowledge base, RAG, document Q&A, FAQ, wiki  
**Features:** Hybrid Retrieval, Wiki Mode, Knowledge Graph  
**Auto-Dependencies:** WeKnora CLI, Docker, MCP server

### weknora-agent
**Path:** `.cursor/skills/weknora-agent/SKILL.md`  
**Kích hoạt:** agent mode, ReAct reasoning, autonomous workflow  
**Features:** Multi-step planning, Tool orchestration, Web search  
**Auto-Dependencies:** WeKnora CLI với agent mode

### pixelrag
**Path:** `.cursor/skills/pixelrag/SKILL.md`  
**Kích hoạt:** pixelrag, visual rag, screenshot rag, table/chart extraction  
**Features:** Screenshot-based RAG, Vision embedding, Qwen3-VL  
**Improvement:** 18.1% accuracy vs Text RAG  
**Auto-Dependencies:** pixelrag[full], playwright, chromium

---

## Phần 9: Changes Log (v1.2.0)

### Added in this update:

#### 1. New Skills (4 skills)

**vietnam-address** (Skill #14)
- Vietnamese administrative units
- 34 provinces/cities, ~11,000 wards
- Cascading dropdown, autocomplete, validation

**weknora-kb** (Skill #15)
- RAG knowledge platform (17.3k stars)
- Hybrid Retrieval (Vector + BM25 + GraphRAG)
- Wiki Mode, Knowledge Graph
- MCP server integration

**weknora-agent** (Skill #16)
- ReAct Agent for autonomous reasoning
- Multi-step planning and execution
- Web search and MCP tools integration

**pixelrag** (Skill #17)
- Visual RAG (5.3k stars)
- Screenshot-based document understanding
- 18.1% accuracy improvement vs Text RAG
- Qwen3-VL-Embedding model

#### 2. Updated Rules

**rag.mdc**
- Added PixelRAG section (when to use, architecture, best practices)
- Added WeKnora and PixelRAG references
- Added evaluation comparison (Text RAG vs PixelRAG)
- Added quick decision guide

**skill-integration.mdc** (v1.2.0)
- Updated Skill Keyword Matrix với new skills
- Added skill combination rules for new skills
- Added Vietnamese address keywords
- Added Knowledge Base keywords
- Added Visual RAG keywords
- Added Agent Mode keywords

**vector-search.mdc**
- Added WeKnora reference (Hybrid Retrieval + GraphRAG)

---

## Phần 10: Quick Start Guide

### 1. Basic Usage

```markdown
User: "Tạo landing page cho startup AI"

→ Skill Detection:
   ★ PRIMARY: frontend-taste (0.95)
   ○ SECONDARY: full-output (0.85)
   ○ TERTIARY: frontend-review (0.90)

→ Execute:
   1. Pre-Review Gate (taste-pre)
   2. Implementation
   3. Post-Review Gate (taste-post + review-post)
   4. Delivery
```

### 2. Security Task

```markdown
User: "Review code này xem có SQL injection không"

→ Skill Detection:
   ★ PRIMARY: security-review (0.95)

→ Execute:
   1. Pre-Review Gate (security-pre)
   2. Implementation (security analysis)
   3. Post-Review Gate (security-post)
   4. Delivery
```

### 3. Knowledge Base Task

```markdown
User: "Tạo knowledge base cho công ty"

→ Skill Detection:
   ★ PRIMARY: weknora-kb (0.95)
   ○ SECONDARY: full-output (0.85)

→ Execute:
   1. Pre-Review Gate (weknora-pre + fulloutput-pre)
   2. Implementation
   3. Post-Review Gate (weknora-post + fulloutput-post)
   4. Delivery
```

### 4. Visual RAG Task

```markdown
User: "Phân tích báo cáo tài chính PDF"

→ Skill Detection:
   ★ PRIMARY: pixelrag (0.95)
   ○ SECONDARY: full-output (0.85)

→ Execute:
   1. Pre-Review Gate (pixelrag-pre + fulloutput-pre)
   2. Implementation
   3. Post-Review Gate (pixelrag-post + fulloutput-post)
   4. Delivery
```

---

## Liên kết

- [[skill-integration]] - Skill Integration Protocol
- [[context-router]] - Context Routing Rules
- [[memory-first]] - Memory Context Management
- [[multi-language-vibe-code]] - Multi-Language Request Processing
- [[rag]] - RAG Implementation Rules
- [[vector-search]] - Vector Search Rules
- [[weknora]] - WeKnora Integration (Enterprise RAG)
- [[pixelrag]] - PixelRAG Integration (Visual RAG)
