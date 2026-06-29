# Test Case: Năng Lượng Số Học Chatbot - Rules/Skills Reasoning Trace

## Requirement
> "Tham khảo tài liệu năng lượng số với file pdf này: batcuclinhso.pdf, thực hiện viết ứng dụng chat bot tư vấn năng lượng với bậc thầy chuyên gia."

**Document:** `batcuclinhso.pdf` (Năng Lượng Số Học - Energy Numerology)
**Status:** ✅ PDF FOUND and ANALYZED (111 pages, ~14,271 lines)

---

## Phase 1: Intent Detection & Task Analysis

### Step 1.1: Intent Detection (intent-detection.mdc)
```
Input: "Tham khảo tài liệu năng lượng số với file pdf này: batcuclinhso.pdf, thực hiện viết ứng dụng chat bot tư vấn năng lượng với bậc thầy chuyên gia"

Intent Classification:
├── Primary Intent: IMPLEMENT_APPLICATION
├── Secondary Intent: DOCUMENT_REFERENCE
├── Domain: NĂNG_LƯỢNG_SỐ_HỌC (Energy Numerology)
├── Sub-Domain: Vietnamese Fortune-telling / Esoteric System
├── Complexity: MEDIUM-HIGH (AI + Domain Knowledge + Calculation)
├── Urgency: STANDARD
└── Language: Vietnamese (→ translate to English for processing)

Detected Keywords:
- "batcuclinhso.pdf" → Năng Lượng Số Học document
- "năng lượng số" → Energy Numerology system
- "chat bot" → conversation AI
- "tư vấn" → consultation service
- "bậc thầy chuyên gia" → expert persona

Document Analysis (from PDF content):
✅ Chapter 1: 8 Sao (8 Stars) - 4 Cát tinh, 4 Hung tinh
✅ Chapter 2-3: Số 0 và 5 trong Năng Lượng Số Học
✅ Chapter 4-12: Sự Kết Hợp của Các Sao (Tuyến, Diện)
✅ Chapter 13-20: Ứng Dụng Thực Tế
```

### Step 1.2: Document Knowledge Structure (from batcuclinhso.pdf)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BATCUCLINHSO.PDF - KNOWLEDGE STRUCTURE               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  CHAPTER 1: 8 SAO NĂNG LƯỢNG (8 Stars System)                          │
│  ════════════════════════════════════════════════════════════════════════│
│                                                                          │
│  4 CÁT TINH (Auspicious Stars):                                        │
│  ┌──────────────┬────────────────────────────────────────────────────┐│
│  │ Thiên Y       │ Tài Lộc & Chính Duyên                              ││
│  │ (天医星)      │ 13/31(c1), 68/86(c2), 49/94(c3), 27/72(c4)       ││
│  ├──────────────┼────────────────────────────────────────────────────┤│
│  │ Diên Niên     │ Sự Nghiệp & Kho Chứa                               ││
│  │ (延年星)      │ 19/91(c1), 78/87(c2), 34/43(c3), 26/62(c4)       ││
│  ├──────────────┼────────────────────────────────────────────────────┤│
│  │ Sinh Khí      │ Quý Nhân & Niềm Vui                                ││
│  │ (生气星)      │ 14/41(c1), 67/76(c2), 39/93(c3), 28/82(c4)       ││
│  ├──────────────┼────────────────────────────────────────────────────┤│
│  │ Phục Vị       │ Sự Kiên Trì & Chờ Đợi                             ││
│  │ (伏位星)      │ 11/22(c1), 88/99(c2), 66/77(c3), 33/44(c4)       ││
│  └──────────────┴────────────────────────────────────────────────────┘│
│                                                                          │
│  4 HUNG TINH (Inauspicious Stars):                                     │
│  ┌──────────────┬────────────────────────────────────────────────────┐│
│  │ Ngũ Quỷ      │ Trí Tuệ & Dị Biệt (Thiên Tài)                      ││
│  │ (五鬼星)     │ 18/81(c1), 79/97(c2), 36/63(c3), 24/42(c4)       ││
│  ├──────────────┼────────────────────────────────────────────────────┤│
│  │ Tuyệt Mệnh   │ Lòng Dũng Cảm & Quyết Đoán                        ││
│  │ (绝命星)     │ 12/21(c1), 69/96(c2), 48/84(c3), 37/73(c4)       ││
│  ├──────────────┼────────────────────────────────────────────────────┤│
│  │ Họa Hại      │ Khẩu Tài & Thị Phi                                  ││
│  │ (祸害星)     │ 17/71(c1), 89/98(c2), 46/64(c3), 23/32(c4)       ││
│  ├──────────────┼────────────────────────────────────────────────────┤│
│  │ Lục Sát      │ Tình Cảm & Đào Hoa                                  ││
│  │ (六煞星)     │ 16/61(c1), 47/74(c2), 38/83(c3), 29/92(c4)       ││
│  └──────────────┴────────────────────────────────────────────────────┘│
│                                                                          │
│  Cấp độ năng lượng: Cấp 1 (mạnh nhất) > Cấp 2 > Cấp 3 > Cấp 4        │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  CHAPTER 2: SỐ 0 VÀ 5 TRONG NĂNG LƯỢNG SỐ HỌC                          │
│  ════════════════════════════════════════════════════════════════════════│
│                                                                          │
│  SỐ 0: Ẩn Giấu, Tàng Hình, Linh Tính                                  │
│  ├── Làm suy yếu năng lượng các sao đứng trước và sau                 │
│  ├── Ở cuối số → công cốc (tình cảm, sự nghiệp, tài lộc)            │
│  ├── Nhiều 0 ở giữa → nỗ lực nhiều nhưng thu hoạch ít               │
│  └── Tăng linh tính (hữu ích cho người tu hành)                       │
│                                                                          │
│  SỐ 5: Hiển Thị, Tăng Cường, Cương Cường                              │
│  ├── Tăng năng lượng các sao đi cùng                                  │
│  ├── Phải đặt đúng chỗ, quá nhiều → ngược                            │
│  ├── Ở vị trí thứ 5 từ cuối → nguy cơ kiện tụng, nhập viện          │
│  └── Chú ý: cột sống, thắt lưng, tim mạch                            │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  CHAPTER 3-12: SỰ KẾT HỢP CÁC SAO                                      │
│  ════════════════════════════════════════════════════════════════════════│
│                                                                          │
│  Tuyến (2 sao liền nhau):                                              │
│  ├── Cát + Cát: Rất tốt (VD: 1319 = Thiên Y + Diên Niên)              │
│  ├── Cát + Hung: Cần cân nhắc, hóa giải bằng Cát tinh khác           │
│  └── Hung + Hung: Nguy hiểm (VD: 1812 = Ngũ Quỷ + Tuyệt Mệnh)        │
│                                                                          │
│  Diện (3-4 sao):                                                       │
│  └── Xem xét tổng thể, có quy tắc hóa giải                          │
│                                                                          │
│  QUY TẮC HÓA GIẢI:                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │ Thiên Y  → Hóa giải Tuyệt Mệnh                                    ││
│  │ Sinh Khí → Hóa giải Họa Hại                                       ││
│  │ Diên Niên→ Hóa giải Lục Sát                                       ││
│  │ Sinh Khí + Thiên Y + Diên Niên → Hóa giải Ngũ Quỷ                 ││
│  │ Diên Niên + Phục Vị → Hóa giải Ngũ Quỷ                           ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                          │
│  VÍ DỤ PHÂN TÍCH:                                                      │
│  ├── 1319 (Thiên Y + Diên Niên): Có tiền + Giữ được tiền            │
│  ├── 318 (Thiên Y + Ngũ Quỷ): Có tiền nhưng dễ mất do thay đổi     │
│  ├── 1812 (Ngũ Quỷ + Tuyệt Mệnh): "Không chết cũng tàn tật"        │
│  └── 18141319: Ngũ Quỷ được hóa giải hoàn toàn bởi chuỗi Cát tinh  │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  CHAPTER 13-20: ỨNG DỤNG THỰC TẾ                                       │
│  ════════════════════════════════════════════════════════════════════════│
│                                                                          │
│  1. SỐ ĐIỆN THOẠI:                                                     │
│     ├── 4-6 số cuối nên là Cát tinh                                    │
│     ├── Không nên có 2 Diên Niên hoặc 2 Thiên Y song song             │
│     └── Không nên đặt Hung tinh ở cuối                                 │
│                                                                          │
│  2. SỐ CMND/CCCD:                                                      │
│     └── Phân tích vận hạn theo từng giai đoạn 5 năm                   │
│                                                                          │
│  3. BIỂN SỐ XE:                                                        │
│     └── Chủ yếu xem 4 số cuối                                         │
│                                                                          │
│  4. SỐ NHÀ:                                                            │
│     └── Phân tích năng lượng của ngôi nhà                             │
│                                                                          │
│  5. TÀI KHOẢN MXH (WeChat, Zalo, Facebook):                           │
│     └── Tên, ID, ảnh đại diện                                         │
│                                                                          │
│  6. THẺ NGÂN HÀNG:                                                     │
│     └── Khả năng giữ tiền của "kho chứa"                             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Step 1.3: Task Analyzer (task-analyzer.mdc)
```
Task Manifest Generation:
Task: Năng Lượng Số Học Consultation Chatbot

Knowledge Base Structure (from batcuclinhso.pdf):
├── Collection: "batcuclinhso_energy"
│   ├── 8_stars_chunks (8 sao + chi tiết)
│   ├── number_0_5_chunks (số 0 và 5)
│   ├── combinations_chunks (sự kết hợp)
│   ├── mitigation_rules_chunks (quy tắc hóa giải)
│   └── applications_chunks (ứng dụng thực tế)

Subtasks:
[1] Document Processing Pipeline (batcuclinhso.pdf)
    - PDF parsing and OCR
    - Vietnamese text extraction
    - Content chunking by chapter
    - Knowledge base population (weknora-kb)

[2] Năng Lượng Số Học Calculation Engine
    - 8 Sao Analyzer (nhận diện sao từ số)
    - Energy Level Calculator (cấp 1-4)
    - Combination Analyzer (Tuyến, Diện)
    - Mitigation Checker (hóa giải Hung tinh)
    - Application Selector (điện thoại, biển số, CMND...)

[3] AI Expert Master Persona
    - Character: Thầy Năng Lượng Số
    - Tone: Traditional Vietnamese wisdom, respectful
    - Knowledge: From batcuclinhso.pdf + built-in
    - Response Style: Explain energy patterns + give guidance

[4] Chat Interface
    - Chat UI with history
    - Number input form (phone, license plate, ID)
    - Energy chart visualization
    - Star (Sao) display with meanings

[5] AI Integration
    - LLM provider (OpenAI/Gemini/Claude)
    - RAG pipeline with batcuclinhso KB
    - Context management
    - Master persona response

[6] Consultation Flow
    - User input: "Phân tích số điện thoại 09x.xxx.xxxx"
    - Calculate 8 sao for each pair
    - Retrieve knowledge from KB
    - Generate expert explanation
    - Provide mitigation suggestions

[7] Backend API
    - Chat endpoints
    - Number analysis endpoint
    - Document upload API
    - Session management

Estimated Complexity: 10-15 hours
Framework: Nuxt 3 (frontend) + FastAPI (backend)
```

---

## Phase 2: Rules Auto-Discovery

### Step 2.1: Primary Rules Selection

| Rule | Trigger Reason | Load Order |
|------|---------------|------------|
| `task-analyzer.mdc` | Universal task analysis | 1st |
| `ai-knowledge.mdc` | AI chatbot + RAG required | 2nd |
| `llm-providers.mdc` | LLM integration | 3rd |
| `frontend-frameworks.mdc` | Nuxt 3 implementation | 4th |
| `architecture-patterns.mdc` | Clean Architecture | 5th |
| `api-patterns.mdc` | Backend API design | 6th |
| `ui-visual-design.mdc` | Traditional + modern UI | 7th |
| `coding-standards.mdc` | Code consistency | 8th |
| `databases.mdc` | Knowledge base storage | 9th |

### Step 2.2: Domain-Specific Rules

| Rule | Trigger Reason |
|------|---------------|
| `weknora-kb.mdc` | Knowledge base for Năng Lượng Số |
| `weknora-agent.mdc` | AI expert agent |
| `document-ocr.mdc` | PDF processing |
| `backend-frameworks.mdc` | FastAPI backend |
| `security.mdc` | User data privacy |
| `auth.mdc` | User authentication |

### Step 2.3: Project Skills (local)

| Skill | Path | Trigger |
|-------|------|---------|
| `document-ocr` | `.cursor/skills/document-ocr/SKILL.md` | PDF processing |
| `weknora-kb` | `.cursor/skills/weknora-kb/SKILL.md` | Knowledge base |
| `weknora-agent` | `.cursor/skills/weknora-agent/SKILL.md` | AI agent |

---

## Phase 3: Skills Auto-Discovery

### Step 3.1: Pre-Implementation Skills (skill-registry.mdc)

| Skill | Confidence | Trigger |
|-------|------------|---------|
| `karpathy-coding` | 85% | General implementation |
| `ponytail` | 50% | Minimal approach |
| `full-output` | 95% | Full implementation |

### Step 3.2: Domain-Specific Skills

| Skill | Confidence | Trigger |
|-------|------------|---------|
| `weknora-kb` | 95% | Năng Lượng Số knowledge base |
| `weknora-agent` | 95% | AI expert persona |
| `document-ocr` | 90% | batcuclinhso.pdf processing |

### Step 3.3: Quality Gate Skills

| Skill | Gate Type | Purpose |
|-------|-----------|---------|
| `frontend-taste` | PRE-GATE | Traditional + modern design |
| `frontend-review` | POST-GATE | UI quality check |
| `security-review` | POST-GATE | User data protection |

---

## Phase 4: AI Architecture

### Step 4.1: RAG Pipeline Design

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BATCUCLINHSO.PDF - NĂNG LƯỢNG SỐ HỌC                │
│                    (111 pages, Vietnamese content)                       │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Document Processing                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐          │
│  │  Upload  │──▶│ Vietnamese│──▶│  Parse   │──▶│ Chunking │          │
│  │  .pdf    │   │   OCR    │   │ Chapters │   │ 500chars │          │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘          │
│                                                      │                  │
│  Chapters: Chương 1-20 (8 Sao, Số 0/5, Kết hợp, Ứng dụng)           │
└──────────────────────────────────────────────────────┼──────────────────┘
                                                      │
                                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Knowledge Base (weknora-kb)                           │
│  Collection: "batcuclinhso_energy"                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │ 8_stars     │  │ number_0_5   │  │ combinations │                 │
│  │ (8 sao)    │  │ (0 và 5)    │  │ (kết hợp)   │                 │
│  └──────────────┘  └──────────────┘  └──────────────┘                 │
│  ┌──────────────┐  ┌──────────────┐                                    │
│  │ mitigation   │  │ applications │                                    │
│  │ (hóa giải)  │  │ (ứng dụng)  │                                    │
│  └──────────────┘  └──────────────┘                                    │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Chat Consultation Flow                                 │
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐            │
│  │ User Input   │───▶│ Session      │───▶│ Number       │            │
│  │ "0932..."   │    │ Manager      │    │ Parser       │            │
│  └──────────────┘    └──────────────┘    └──────────────┘            │
│                                              │                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐            │
│  │ Response     │◀───│ LLM +        │◀───│ 8 Sao        │            │
│  │ Display      │    │ Master       │    │ Calculator    │            │
│  └──────────────┘    │ Persona      │    └──────────────┘            │
│                      └──────────────┘           │                      │
│                                                  ▼                      │
│                      ┌──────────────┐    ┌──────────────┐            │
│                      │ KB Retrieval │◀───│ Mitigation   │            │
│                      │ (RAG)       │    │ Checker      │            │
│                      └──────────────┘    └──────────────┘            │
└─────────────────────────────────────────────────────────────────────────┘
```

### Step 4.2: Expert Persona Definition

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    THẦY NĂNG LƯỢNG SỐ                                  │
│                    Năng Lượng Số Học Master                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  IDENTITY:                                                              │
│  ├── Name: Thầy Năng Lượng Số (configurable)                           │
│  ├── Title: Chuyên Gia Năng Lượng Số Học                              │
│  ├── Knowledge: From batcuclinhso.pdf                                  │
│  └── Style: Vietnamese traditional wisdom                               │
│                                                                          │
│  PERSONALITY:                                                          │
│  ├── Warm, knowledgeable, patient                                       │
│  ├── Speaks with wisdom and traditional references                     │
│  ├── Uses Vietnamese proverbs                                           │
│  ├── Calm and insightful                                               │
│  └── Provides practical guidance                                        │
│                                                                          │
│  EXPERTISE (from PDF):                                                  │
│  ├── 8 Sao Analysis (Thiên Y, Diên Niên, Sinh Khí...)                 │
│  ├── Number 0 & 5 Effects                                              │
│  ├── Combination Analysis (Tuyến, Diện)                                │
│  ├── Mitigation Rules (hóa giải)                                        │
│  └── Applications: Phone, License plate, ID, House number               │
│                                                                          │
│  RESPONSE STYLE:                                                       │
│  ├── Greet: "Chào con. Ta sẽ giúp con phân tích năng lượng số..."    │
│  ├── Ask: "Con muốn phân tích số gì? Điện thoại, biển số, CMND..."   │
│  ├── Explain: "Số 09x... chứa Thiên Y cấp X - đại diện cho..."        │
│  ├── Warning: "Cần lưu ý: Ngũ Quỷ ở cuối có thể gây..."               │
│  ├── Suggest: "Để hóa giải, con nên thêm Sinh Khí vào..."             │
│  └── Close: "Hãy ghi nhớ những điều Ta đã chia sẻ..."                 │
│                                                                          │
│  SYSTEM PROMPT:                                                         │
│  "You are Thầy Năng Lượng Số, a Vietnamese expert in Energy            │
│   Numerology based on the batcuclinhso.pdf document. You specialize     │
│   in analyzing numbers through the 8 Stars system (8 Sao),             │
│   understanding number 0 and 5 effects, combination analysis,          │
│   and mitigation rules. Be knowledgeable, warm, and provide            │
│   practical guidance based on Vietnamese wisdom."                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Step 4.3: Calculation Engine Design

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    NĂNG LƯỢNG SỐ CALCULATION ENGINE                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  INPUT TYPES:                                                           │
│  ├── Phone Number (số điện thoại)                                      │
│  ├── License Plate (biển số xe) - 4 số cuối                           │
│  ├── ID Number (CMND/CCCD) - 9/12 số                                  │
│  ├── House Number (số nhà)                                              │
│  └── Custom Number (số tự chọn)                                        │
│                                                                          │
│  OUTPUT:                                                                │
│  ├── Sao Analysis (list of 8 sao in the number)                        │
│  ├── Energy Levels (cấp 1-4 for each sao)                             │
│  ├── Combination Types (Tuyến, Diện)                                    │
│  ├── Warnings (Hung tinh positions)                                   │
│  ├── Mitigation Suggestions (hóa giải)                                │
│  └── Overall Assessment (tổng thể đánh giá)                            │
│                                                                          │
│  CORE FUNCTIONS:                                                        │
│                                                                          │
│  function parseNumber(input: string): string[]                        │
│  // Extract consecutive pairs from number                              │
│                                                                          │
│  function identifyStar(pair: string): {star: string, level: number}   │
│  // Match pair to 8 Sao system                                         │
│  // Return star name and energy level (1-4)                           │
│                                                                          │
│  function analyzeCombinations(stars: Star[]): CombinationResult        │
│  // Analyze 2-star (Tuyến), 3-4 star (Diện)                          │
│  // Check for dangerous combinations (1812, etc.)                     │
│                                                                          │
│  function checkMitigation(stars: Star[]): MitigationResult            │
│  // Apply mitigation rules from PDF                                   │
│  // Suggest fixes if Hung stars need balancing                        │
│                                                                          │
│  function generateReport(input: string): AnalysisReport                │
│  // Complete analysis with all findings                                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Step 4.4: 8 Sao Mapping Table

| Pair | Sao | Cấp | Thuộc tính |
|------|-----|-----|------------|
| 13, 31 | Thiên Y | 1-4 | Tài Lộc, Chính Duyên |
| 68, 86 | Thiên Y | 2 | Tài Lộc, Chính Duyên |
| 49, 94 | Thiên Y | 3 | Tài Lộc, Chính Duyên |
| 27, 72 | Thiên Y | 4 | Tài Lộc, Chính Duyên |
| 19, 91 | Diên Niên | 1 | Sự Nghiệp, Kho Chứa |
| 78, 87 | Diên Niên | 2 | Sự Nghiệp, Kho Chứa |
| 34, 43 | Diên Niên | 3 | Sự Nghiệp, Kho Chứa |
| 26, 62 | Diên Niên | 4 | Sự Nghiệp, Kho Chứa |
| 14, 41 | Sinh Khí | 1 | Quý Nhân, Niềm Vui |
| 67, 76 | Sinh Khí | 2 | Quý Nhân, Niềm Vui |
| 39, 93 | Sinh Khí | 3 | Quý Nhân, Niềm Vui |
| 28, 82 | Sinh Khí | 4 | Quý Nhân, Niềm Vui |
| 11, 22 | Phục Vị | 1 | Kiên Trì, Chờ Đợi |
| 88, 99 | Phục Vị | 2 | Kiên Trì, Chờ Đợi |
| 66, 77 | Phục Vị | 3 | Kiên Trì, Chờ Đợi |
| 33, 44 | Phục Vị | 4 | Kiên Trì, Chờ Đợi |
| 18, 81 | Ngũ Quỷ | 1 | Trí Tuệ, Dị Biệt |
| 79, 97 | Ngũ Quỷ | 2 | Trí Tuệ, Dị Biệt |
| 36, 63 | Ngũ Quỷ | 3 | Trí Tuệ, Dị Biệt |
| 24, 42 | Ngũ Quỷ | 4 | Trí Tuệ, Dị Biệt |
| 12, 21 | Tuyệt Mệnh | 1 | Dũng Cảm, Quyết Đoán |
| 69, 96 | Tuyệt Mệnh | 2 | Dũng Cảm, Quyết Đoán |
| 48, 84 | Tuyệt Mệnh | 3 | Dũng Cảm, Quyết Đoán |
| 37, 73 | Tuyệt Mệnh | 4 | Dũng Cảm, Quyết Đoán |
| 17, 71 | Họa Hại | 1 | Khẩu Tài, Thị Phi |
| 89, 98 | Họa Hại | 2 | Khẩu Tài, Thị Phi |
| 46, 64 | Họa Hại | 3 | Khẩu Tài, Thị Phi |
| 23, 32 | Họa Hại | 4 | Khẩu Tài, Thị Phi |
| 16, 61 | Lục Sát | 1 | Tình Cảm, Đào Hoa |
| 47, 74 | Lục Sát | 2 | Tình Cảm, Đào Hoa |
| 38, 83 | Lục Sát | 3 | Tình Cảm, Đào Hoa |
| 29, 92 | Lục Sát | 4 | Tình Cảm, Đào Hoa |

---

## Phase 5: Execution Flow

### Step 5.1: Pre-Implementation Gates

```
[GATE 1] Document Verification ✅
├── Check: batcuclinhso.pdf readable
├── Status: ✅ FOUND (111 pages)
├── Content: Năng Lượng Số Học (8 Sao, Số 0/5, Kết hợp)
└── Decision: APPROVE ✅

[GATE 2] Domain Understanding ✅
├── Check: 8 Sao system understood
├── Check: Number 0/5 effects known
├── Check: Mitigation rules extracted
├── Check: Applications identified
└── Decision: APPROVE ✅

[GATE 3] Architecture Gate
├── Check: RAG pipeline design
├── Check: Calculation engine design
├── Check: LLM provider selection
└── Decision: PROCEED
```

### Step 5.2: Implementation Phase

```
[PHASE A] Document Processing (batcuclinhso.pdf) ✅
├── PDFUpload.vue - Upload component
├── PDFParser.ts - Parse batcuclinhso.pdf
├── VietnameseTextExtractor.ts - Extract Vietnamese content
├── ChapterChunker.ts - Split by chapters
├── EmbeddingService.ts - Generate embeddings
└── weknora-kb population (5 collections)

[PHASE B] Năng Lượng Số Calculation Engine
├── NangLuongSoCalculator.ts - Main class
├── SaoIdentifier.ts - Match number pairs to 8 Sao
├── EnergyLevelCalculator.ts - Determine cấp 1-4
├── CombinationAnalyzer.ts - Tuyến & Diện analysis
├── MitigationChecker.ts - Apply hóa giải rules
├── Number0_5_Effect.ts - Số 0 & 5 effects
└── ReportGenerator.ts - Generate analysis report

[PHASE C] Knowledge Base (weknora-kb)
├── Collection: "batcuclinhso_energy"
├── Sub-collections:
│   ├── 8_stars_data (4 Cát tinh + 4 Hung tinh + chi tiết)
│   ├── number_0_5_data (effects of 0 and 5)
│   ├── combinations_data (Tuyến, Diện)
│   ├── mitigation_rules_data (hóa giải)
│   └── applications_data (điện thoại, biển số, CMND...)
└── Vector search configuration

[PHASE D] AI Expert Agent (weknora-agent)
├── AgentConfig: "nangluongso_master"
├── SystemPrompt: Thầy Năng Lượng Số
├── KnowledgeBase: batcuclinhso_energy KB
├── LLM: GPT-4o / Claude Sonnet
├── Temperature: 0.7 (wisdom + accuracy)
└── MaxTokens: 2000

[PHASE E] Chat Interface
├── ChatContainer.vue - Main chat layout
├── ChatHeader.vue - Master avatar + title
├── MessageBubble.vue - User/Master messages
├── ChatInput.vue - Input with send button
├── TypingIndicator.vue - Loading animation
├── NumberInputForm.vue - Input phone/license plate
├── SaoDisplay.vue - Show 8 Sao results
├── EnergyChart.vue - Visual chart of stars
├── MitigationCard.vue - Hóa giải suggestions
└── ConversationHistory.vue - Thread list

[PHASE F] Backend API (FastAPI)
├── /api/chat/send - Send message
├── /api/chat/history/{session_id} - Get history
├── /api/analyze/phone - Analyze phone number
├── /api/analyze/license - Analyze license plate
├── /api/analyze/id - Analyze ID number
├── /api/analyze/house - Analyze house number
├── /api/document/upload - Upload PDF
├── /api/session/create - Create consultation
└── /api/session/{id} - Session management

[PHASE G] Integration
├── WebSocket/SSE for real-time chat
├── Session state management (Pinia)
├── KB retrieval sync
├── Error handling with fallbacks
└── Master response formatting
```

### Step 5.3: Post-Implementation Gates

```
[GATE 4] frontend-review (post-review)
├── Check: All chat components implemented
├── Check: Number input working
├── Check: Sao display correct
├── Check: Traditional design aesthetic
├── Check: Mobile responsive
└── Decision: APPROVE or REQUEST_CHANGES

[GATE 5] calculation-accuracy (post-review)
├── Check: 8 Sao mapping correct
├── Check: 1319 = Thiên Y + Diên Niên ✅
├── Check: 1812 warning recognized ✅
├── Check: Mitigation rules applied
└── Decision: APPROVE or FIX

[GATE 6] security-review (post-review)
├── Check: User input sanitization
├── Check: API authentication
├── Check: Session data privacy
└── Decision: APPROVE
```

---

## Phase 6: Skill Execution Matrix

| Step | Skills Loaded | Rules Loaded | Output |
|------|--------------|--------------|--------|
| Analysis | `intent-detection` | `task-analyzer`, `skill-registry` | Task Manifest |
| Document | `document-ocr` | `ai-knowledge`, `weknora-kb` | Processed KB ✅ |
| Calculation | `weknora-kb` | `databases`, `backend-frameworks` | N L S Engine |
| Design | `frontend-taste` | `ui-visual-design`, `llm-providers` | UI + Arch |
| Code | `karpathy-coding`, `full-output` | `coding-standards`, `api-patterns` | Full Impl |
| Review | `frontend-review` | `testing`, `security` | Quality Gates |

---

## Expected Test Criteria

### Document Processing ✅
- [ ] batcuclinhso.pdf successfully uploaded ✅
- [ ] Vietnamese text extracted correctly ✅
- [ ] Knowledge base populated with 8 Sao data ✅
- [ ] RAG retrieval accuracy > 80%

### Calculation Engine
- [ ] 8 Sao mapping correct for all 32 pairs
- [ ] Energy levels (cấp 1-4) accurate
- [ ] Number 0 effect (suy yếu) working
- [ ] Number 5 effect (tăng cường) working
- [ ] Combination analysis (Tuyến, Diện) correct
- [ ] Mitigation rules applied correctly
- [ ] Warning for 1812 (Ngũ Quỷ + Tuyệt Mệnh) displayed

### AI Master
- [ ] Master greets appropriately
- [ ] Master explains 8 Sao clearly
- [ ] Master identifies number pairs correctly
- [ ] Master provides mitigation suggestions
- [ ] Responses use Vietnamese wisdom style

### Chat Interface
- [ ] Responsive chat UI
- [ ] Number input form working
- [ ] Sao visualization displayed
- [ ] Traditional aesthetic achieved
- [ ] Mobile responsive

### Functional Requirements
- [ ] Zero TODO comments
- [ ] Zero skeleton placeholders
- [ ] Full consultation flow working
- [ ] Multiple number types supported

### Verification Commands
```bash
# Check TODO count (should be 0)
grep -r "TODO" src/

# Check skeleton count (should be 0)
grep -r "skeleton" src/

# Verify calculation engine
ls src/utils/nangluongso/
# Expected: calculator.ts, sao-mapping.ts, mitigation.ts

# Verify KB collections
grep -r "8_sao\|nangluongso\|batcuclinhso" src/
```

---

## Trace Log Template

```
[13:01:00] INTENT_DETECTED: IMPLEMENT_APPLICATION, NĂNG_LƯỢNG_SỐ_HỌC
[13:01:01] DOCUMENT_FOUND: batcuclinhso.pdf (111 pages)
[13:01:02] DOCUMENT_ANALYZED: 8 Sao, Số 0/5, Kết hợp, Ứng dụng
[13:01:03] TASK_ANALYZER: Generating manifest...
[13:01:04] DOMAIN_IDENTIFIED: Vietnamese Energy Numerology (N L S)
[13:01:05] MANIFEST_COMPLETE: 7 subtasks, complexity=MEDIUM-HIGH
[13:01:06] RULES_DISCOVERY: 9 rules loaded
[13:01:07] SKILLS_DISCOVERY: 6 skills matched
[13:01:08] PRE_GATE: Document Verification [✅ APPROVED]
[13:01:09] DOMAIN_ANALYSIS: 8 Sao system extracted
[13:01:10] EXPERT_PERSONA: Thầy Năng Lượng Số defined
[13:01:11] ARCHITECTURE: RAG + Calculation Engine designed
[13:01:12] PRE_GATE: Architecture [APPROVED]
[13:01:12] SKILL_LOADED: weknora-kb
[13:01:13] SKILL_LOADED: weknora-agent
[13:01:14] SKILL_LOADED: document-ocr
[13:01:15] IMPLEMENTATION_STARTED: Document Processing
[13:01:XX] IMPLEMENTATION_STARTED: N L S Calculation Engine
[13:01:XX] IMPLEMENTATION_STARTED: Knowledge Base
[13:01:XX] IMPLEMENTATION_STARTED: AI Expert Agent
[13:01:XX] IMPLEMENTATION_STARTED: Chat Interface
[13:02:XX] IMPLEMENTATION_STARTED: Backend API
[13:02:XX] POST_GATE: frontend-review [EXECUTING]
[13:02:XX] POST_GATE: calculation-accuracy [EXECUTING]
[13:02:XX] POST_GATE: security-review [EXECUTING]
[13:02:XX] POST_GATE: All gates [APPROVED]
[13:02:XX] TASK_COMPLETE: Năng Lượng Số Học Chatbot delivered
```

---

## Critical Notes

1. **Document Clarification:**
   - File: `batcuclinhso.pdf` = **Năng Lượng Số Học** (không phải Bát Cực Linh Số)
   - Domain: Vietnamese Fortune-telling / Energy Numerology
   - Content: 8 Sao system (4 Cát tinh + 4 Hung tinh)

2. **Knowledge Accuracy:**
   - 32 number pairs mapped to 8 Sao
   - 4 energy levels per Sao
   - Mitigation rules critical for Hung tinh

3. **Calculation Priority:**
   - 4-6 số cuối quan trọng nhất cho điện thoại
   - 4 số cuối cho biển số xe
   - Tổng thể (điểm-tuyến-diện-thể) hơn riêng lẻ

4. **Expert Persona:**
   - Vietnamese traditional style
   - Wisdom + Practical guidance
   - Reference to batcuclinhso.pdf knowledge

5. **Test Cases Required:**
   - 1319 = Thiên Y + Diên Niên (Cát + Cát)
   - 318 = Thiên Y + Ngũ Quỷ (Cát + Hung)
   - 1812 = Ngũ Quỷ + Tuyệt Mệnh (Hung + Hung - nguy hiểm)
   - 18141319 = Ngũ Quỷ + Sinh Khí + Thiên Y + Diên Niên (hóa giải)
