# Task Analyzer & Synchronized Context System
## Cursor Enterprise Framework - Task Orchestration Engine

---

## 1. System Overview

```
╔════════════════════════════════════════════════════════════════════════════════════╗
║                  TASK ANALYZER & SYNCED CONTEXT SYSTEM                           ║
║                                                                                  ║
║  ┌─────────────────────────────────────────────────────────────────────────────┐  ║
║  │                    USER REQUEST (Any Language)                              │  ║
║  │              "Tạo một landing page cho startup AI"                         │  ║
║  └─────────────────────────────────────────────────────────────────────────────┘  ║
║                                      │                                            ║
║                                      ▼                                            ║
║  ┌─────────────────────────────────────────────────────────────────────────────┐  ║
║  │  PHASE 1: CONTEXT SYNC & ANALYSIS                                          │  ║
║  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │  ║
║  │  │Rule Registry│  │Skill Matrix │  │MCP Servers  │  │Dependencies │      │  ║
║  │  │   84 rules  │  │  17 skills  │  │  5 servers  │  │   sync'd    │      │  ║
║  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │  ║
║  └─────────────────────────────────────────────────────────────────────────────┘  ║
║                                      │                                            ║
║                                      ▼                                            ║
║  ┌─────────────────────────────────────────────────────────────────────────────┐  ║
║  │  PHASE 2: LANGUAGE DETECTION & TRANSLATION                                  │  ║
║  │  Vietnamese → English (semantic-preserving)                                  │  ║
║  └─────────────────────────────────────────────────────────────────────────────┘  ║
║                                      │                                            ║
║                                      ▼                                            ║
║  ┌─────────────────────────────────────────────────────────────────────────────┐  ║
║  │  PHASE 3: INTENT & SKILL DETECTION                                         │  ║
║  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │  ║
║  │  │  Intent:    │  │  Domain:   │  │  Skills:   │  │  Rules:    │      │  ║
║  │  │  BUILD      │  │  FRONTEND  │  │  4 matched │  │  6 matched │      │  ║
║  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │  ║
║  └─────────────────────────────────────────────────────────────────────────────┘  ║
║                                      │                                            ║
║                                      ▼                                            ║
║  ┌─────────────────────────────────────────────────────────────────────────────┐  ║
║  │  PHASE 4: TASK DECOMPOSITION                                               │  ║
║  │  ┌───────────────────────────────────────────────────────────────────────┐   │  ║
║  │  │  TASK-1: Pre-Review Gates (karpathy + frontend-taste + full-output)│   │  ║
║  │  │  TASK-2: Implementation (Hero Section)                              │   │  ║
║  │  │  TASK-3: Implementation (Features Section)                          │   │  ║
║  │  │  TASK-4: Implementation (CTA Section)                               │   │  ║
║  │  │  TASK-5: Post-Review Gates (all skills)                            │   │  ║
║  │  └───────────────────────────────────────────────────────────────────────┘   │  ║
║  └─────────────────────────────────────────────────────────────────────────────┘  ║
║                                      │                                            ║
║                                      ▼                                            ║
║  ┌─────────────────────────────────────────────────────────────────────────────┐  ║
║  │  PHASE 5: DEPENDENCY CHECK & AUTO-INSTALL                                   │  ║
║  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                          │  ║
║  │  │ TailwindCSS│  │Framer-Motion│ │  Lucide    │  → Auto-install if needed │  ║
║  │  └─────────────┘  └─────────────┘  └─────────────┘                          │  ║
║  └─────────────────────────────────────────────────────────────────────────────┘  ║
║                                      │                                            ║
║                                      ▼                                            ║
║  ┌─────────────────────────────────────────────────────────────────────────────┐  ║
║  │  PHASE 6: TASK EXECUTION (Sequential or Parallel)                          │  ║
║  │                                                                              │  ║
║  │  [TASK-1] ──→ [TASK-2] ──→ [TASK-3] ──→ [TASK-4] ──→ [TASK-5]          │  ║
║  │     │           │           │           │           │                        │  ║
║  │     ▼           ▼           ▼           ▼           ▼                        │  ║
║  │  karpathy    Hero       Features      CTA      Post-Review                  │  ║
║  │  + taste    Section    Section     Section     + Delivery                   │  ║
║  └─────────────────────────────────────────────────────────────────────────────┘  ║
║                                                                                  ║
╚════════════════════════════════════════════════════════════════════════════════════╝
```

---

## 2. Context Synchronization Registry

### 2.1 Rule Registry (Auto-Discovered)

```yaml
rules_registry:
  metadata:
    total_rules: 84
    categories:
      - architecture: 15 rules
      - frontend: 8 rules  
      - backend: 12 rules
      - security: 6 rules
      - devops: 10 rules
      - database: 7 rules
      - integration: 26 rules
    last_sync: "2026-06-26T13:00:00Z"
    
  rule_patterns:
    frontend:
      patterns:
        - "landing page"
        - "portfolio"
        - "landing"
        - "homepage"
        - "marketing site"
      associated_rules:
        - frontend-architecture
        - ui-visual-design
        - coding-standards
        - nextjs | nuxt | vue | react
      confidence_boost: 0.15
        
    backend:
      patterns:
        - "API"
        - "backend"
        - "server"
        - "endpoint"
        - "database"
      associated_rules:
        - backend-architecture
        - api
        - restful-api
      confidence_boost: 0.15
      
    security:
      patterns:
        - "auth"
        - "login"
        - "security"
        - "JWT"
        - "OAuth"
        - "payment"
        - "MoMo"
        - "SePay"
      associated_rules:
        - web-security
        - authentication
        - authorization
        - billing
      confidence_boost: 0.20
      
    devops:
      patterns:
        - "docker"
        - "kubernetes"
        - "deploy"
        - "CI/CD"
        - "AWS"
        - "Azure"
      associated_rules:
        - docker
        - kubernetes
        - deployment
        - ci-cd
      confidence_boost: 0.15
```

### 2.2 Skill Registry (Auto-Discovered)

```yaml
skill_registry:
  metadata:
    total_skills: 17
    skill_categories:
      - frontend: 2 skills
      - review: 3 skills
      - efficiency: 2 skills
      - domain: 4 skills
      - knowledge: 3 skills
      - special: 3 skills
    last_sync: "2026-06-26T13:00:00Z"
    
  skills:
    frontend-taste:
      id: "frontend-taste"
      path: ".cursor/skills/frontend-taste/SKILL.md"
      description: "Premium frontend design skill for landing pages and portfolios"
      keywords:
        en: ["landing page", "portfolio", "homepage", "marketing site", "SaaS landing"]
        vi: ["trang đích", "danh mục", "trang chủ", "web marketing"]
        zh: ["落地页", "作品集", "主页", "营销网站"]
      triggers:
        - "landing page"
        - "portfolio"
        - "greenfield"
        - "new build"
      confidence: 0.95
      dependencies:
        npm: ["tailwindcss", "framer-motion", "lucide-react"]
      gates:
        pre: ["taste-pre"]
        post: ["taste-post"]
      priority: HIGH
      
    frontend-redesign:
      id: "frontend-redesign"
      path: ".cursor/skills/frontend-redesign/SKILL.md"
      description: "Redesign existing frontend codebase"
      keywords:
        en: ["redesign", "upgrade", "improve existing", "modernize", "enhance"]
        vi: ["cải thiện", "nâng cấp", "thiết kế lại", "hiện đại hóa"]
      triggers:
        - "existing site"
        - "redesign"
        - "upgrade"
        - "improve"
      confidence: 0.90
      dependencies:
        npm: ["tailwindcss", "prettier", "eslint"]
      gates:
        pre: ["redesign-pre"]
        post: ["redesign-post"]
      priority: HIGH
      
    full-output:
      id: "full-output"
      path: ".cursor/skills/full-output/SKILL.md"
      description: "Ensure complete implementation without truncation"
      keywords:
        en: ["full implementation", "complete", "not skeleton", "no TODO", "entire"]
        vi: ["triển khai đầy đủ", "hoàn chỉnh", "toàn bộ"]
      triggers:
        - "full implementation"
        - "complete"
        - "not skeleton"
        - "no TODO"
      confidence: 0.95
      dependencies: []
      gates:
        pre: ["fulloutput-pre"]
        post: ["fulloutput-post"]
      priority: MANDATORY
      
    frontend-review:
      id: "frontend-review"
      path: ".cursor/skills/frontend-review/SKILL.md"
      description: "Quality review for frontend tasks"
      keywords:
        en: ["review", "quality check", "audit", "taste check"]
        vi: ["kiểm tra", "đánh giá", "chất lượng", "review"]
      triggers:
        - "review"
        - "quality check"
        - "audit"
      confidence: 0.95
      dependencies: []
      gates:
        pre: ["review-pre"]
        post: ["review-post"]
      priority: MANDATORY
      auto_apply: true  # Always runs with frontend tasks
      
    security-review:
      id: "security-review"
      path: ".cursor/skills/security-review/SKILL.md"
      description: "Security vulnerability assessment"
      keywords:
        en: ["security", "vulnerability", "XSS", "SQL injection", "auth", "JWT"]
        vi: ["bảo mật", "lỗ hổng", "auth", "mã hóa"]
      triggers:
        - "security"
        - "vulnerability"
        - "pentest"
        - "CVE"
        - "OWASP"
        - "JWT"
        - "OAuth"
      confidence: 0.95
      dependencies:
        python: ["bandit", "safety"]
      gates:
        pre: ["security-pre"]
        post: ["security-post"]
      priority: HIGH
      
    vietnam-payment-review:
      id: "vietnam-payment-review"
      path: ".cursor/skills/vietnam-payment-review/SKILL.md"
      description: "Vietnam payment integration review"
      keywords:
        en: ["MoMo", "SePay", "PayOS", "VNPay", "ZaloPay", "VietQR"]
        vi: ["MoMo", "SePay", "PayOS", "VNPay", "ZaloPay", "VietQR", "thanh toán"]
      triggers:
        - "MoMo"
        - "SePay"
        - "PayOS"
        - "VNPay"
        - "ZaloPay"
        - "VietQR"
      confidence: 0.95
      dependencies: []
      gates:
        pre: ["payment-pre"]
        post: ["payment-post"]
      priority: HIGH
      
    ponytail:
      id: "ponytail"
      path: ".cursor/skills/ponytail/SKILL.md"
      description: "Lazy Senior Dev - minimal code, efficient"
      keywords:
        en: ["less code", "yagni", "over-engineering", "simple", "minimal"]
        vi: ["đơn giản", "tối thiểu", "ít code"]
      triggers:
        - "less code"
        - "yagni"
        - "over-engineering"
        - "simple"
      confidence: 0.85
      dependencies: []
      gates:
        pre: []
        post: []
      priority: MEDIUM
      
    karpathy-coding:
      id: "karpathy-coding"
      path: ".cursor/skills/karpathy-coding/SKILL.md"
      description: "Vibe coding discipline - always overlay"
      keywords:
        en: ["vibe code", "just do it", "don't overthink", "simple"]
        vi: ["vibe code", "cứ làm đi", "đơn giản thôi"]
      triggers:
        - "ALL CODING TASKS"
      confidence: 1.0
      dependencies: []
      gates:
        pre: ["karpathy-pre"]
        post: ["karpathy-post"]
      priority: MANDATORY
      auto_apply: true  # Always runs with EVERY task
      
    visual-explainer:
      id: "visual-explainer"
      path: ".cursor/skills/visual-explainer/SKILL.md"
      description: "Generate HTML diagrams and visual explanations"
      keywords:
        en: ["diagram", "architecture overview", "flowchart", "diff review"]
        vi: ["sơ đồ", "kiến trúc", "lưu đồ"]
      triggers:
        - "diagram"
        - "architecture"
        - "flowchart"
        - "visual"
      confidence: 0.90
      dependencies: []
      gates:
        pre: []
        post: []
      priority: MEDIUM
      
    open-design:
      id: "open-design"
      path: ".cursor/skills/open-design/SKILL.md"
      description: "Open Design system integration"
      keywords:
        en: ["open-design", "design system", "prototype", "brand-grade"]
        vi: ["open-design", "design system", "prototype"]
      triggers:
        - "open-design"
        - "design system"
        - "prototype"
      confidence: 0.95
      dependencies:
        npm: []
        system: ["open-design-mcp"]
      gates:
        pre: ["od-pre"]
        post: ["od-post"]
      priority: MEDIUM
      
    document-ocr:
      id: "document-ocr"
      path: ".cursor/skills/document-ocr/SKILL.md"
      description: "Text extraction from images using Tesseract OCR"
      keywords:
        en: ["ocr", "text extraction", "image to text"]
        vi: ["ocr", "đọc text", "trích xuất text"]
      triggers:
        - "ocr"
        - "text extraction"
        - "image to text"
      confidence: 0.95
      dependencies:
        python: ["pytesseract", "Pillow", "opencv-python"]
        system: ["tesseract"]
      gates:
        pre: ["ocr-pre"]
        post: ["ocr-post"]
      priority: MEDIUM
      
    bazi:
      id: "bazi"
      path: ".cursor/skills/bazi/SKILL.md"
      description: "Chinese Bazi fortune analysis"
      keywords:
        en: ["bazi", "fortune", "birth chart"]
        zh: ["八字", "算命", "四柱", "命盘", "运势"]
      triggers:
        - "bazi"
        - "算八字"
        - "四柱"
        - "命盘"
      confidence: 0.95
      dependencies: []
      gates:
        pre: []
        post: []
      priority: LOW
      
    vietnam-address:
      id: "vietnam-address"
      path: ".cursor/skills/vietnam-address/SKILL.md"
      description: "Vietnamese administrative units"
      keywords:
        en: ["vietnam address", "province", "district", "ward"]
        vi: ["địa chỉ Việt Nam", "tỉnh", "thành phố", "quận", "huyện"]
      triggers:
        - "vietnam address"
        - "địa chỉ Việt Nam"
        - "province"
        - "district"
      confidence: 0.95
      dependencies:
        data: ["vietnamese-provinces-database"]
      gates:
        pre: []
        post: []
      priority: MEDIUM
      
    weknora-kb:
      id: "weknora-kb"
      path: ".cursor/skills/weknora-kb/SKILL.md"
      description: "WeKnora RAG knowledge platform"
      keywords:
        en: ["knowledge base", "rag", "document q&a", "wiki", "weknora"]
        vi: ["cơ sở tri thức", "rag", "hỏi đáp tài liệu"]
      triggers:
        - "knowledge base"
        - "rag"
        - "document q&a"
        - "wiki"
        - "weknora"
      confidence: 0.95
      dependencies:
        system: ["weknora-cli", "docker"]
        mcp: ["weknora"]
      gates:
        pre: ["weknora-pre"]
        post: ["weknora-post"]
      priority: MEDIUM
      
    weknora-agent:
      id: "weknora-agent"
      path: ".cursor/skills/weknora-agent/SKILL.md"
      description: "WeKnora ReAct agent"
      keywords:
        en: ["agent mode", "react agent", "autonomous reasoning", "agentic workflow"]
        vi: ["agent mode", "tự động", "suy luận"]
      triggers:
        - "agent mode"
        - "react agent"
        - "autonomous"
      confidence: 0.95
      dependencies:
        system: ["weknora-cli"]
        mcp: ["weknora"]
      gates:
        pre: ["agent-pre"]
        post: ["agent-post"]
      priority: MEDIUM
      
    pixelrag:
      id: "pixelrag"
      path: ".cursor/skills/pixelrag/SKILL.md"
      description: "Visual RAG - screenshot-based document understanding"
      keywords:
        en: ["pixelrag", "visual rag", "screenshot rag", "table extraction"]
        vi: ["pixelrag", "rag hình ảnh", "đọc bảng", "đọc biểu đồ"]
      triggers:
        - "pixelrag"
        - "visual rag"
        - "screenshot rag"
        - "table extraction"
        - "chart extraction"
      confidence: 0.95
      dependencies:
        python: ["pixelrag", "playwright"]
        system: ["chromium"]
      gates:
        pre: ["pixelrag-pre"]
        post: ["pixelrag-post"]
      priority: MEDIUM
```

### 2.3 MCP Server Registry

```yaml
mcp_registry:
  metadata:
    total_servers: 5
    active_servers: 0
    last_sync: "2026-06-26T13:00:00Z"
    
  servers:
    cursor-ide-browser:
      id: "cursor-ide-browser"
      name: "Browser Automation"
      description: "Cursor-owned browser tab + Chrome DevTools Protocol"
      capabilities:
        - browser_tabs
        - browser_navigate
        - browser_snapshot
        - browser_screenshot
        - browser_click
        - browser_type
        - browser_cdp
      mcp_command: "cursor-ide-browser"
      requires_auth: false
      status: "available"
      
    user-codegraph:
      id: "user-codegraph"
      name: "Code Intelligence"
      description: "SQLite knowledge graph of code symbols, edges, files"
      capabilities:
        - codegraph_explore
        - codegraph_search
        - codegraph_callers
        - codegraph_callees
        - codegraph_node
        - codegraph_files
        - codegraph_status
      mcp_command: "user-codegraph"
      requires_auth: false
      status: "available"
      
    user-vercel:
      id: "user-vercel"
      name: "Vercel Deployment"
      description: "Deploy, monitor, and manage Vercel projects"
      capabilities:
        - vercel_deploy
        - vercel_status
        - vercel_logs
        - vercel_domains
      mcp_command: "user-vercel"
      requires_auth: true
      env_vars: ["VERCEL_TOKEN"]
      status: "available"
      
    user-typeui:
      id: "user-typeui"
      name: "TypeUI Design"
      description: "UI component generation with design systems"
      capabilities:
        - typeui_setup
        - typeui_generate
        - typeui_install
      mcp_command: "user-typeui"
      requires_auth: false
      status: "available"
      
    user-shadcn:
      id: "user-shadcn"
      name: "shadcn/ui Components"
      description: "Add and manage shadcn/ui components"
      capabilities:
        - shadcn_add
        - shadcn_list
        - shadcn_search
        - shadcn_audit
      mcp_command: "user-shadcn"
      requires_auth: false
      status: "available"
      
    user-browsermcp:
      id: "user-browsermcp"
      name: "Browser MCP"
      description: "External browser automation"
      capabilities:
        - browser_automation
        - screenshot
        - scrape
      mcp_command: "user-browsermcp"
      requires_auth: false
      status: "available"
```

---

## 3. Task Analysis Engine

### 3.1 Input Processing Pipeline

```yaml
task_analysis_pipeline:
  name: "Multi-Language Task Analyzer"
  version: "1.0.0"
  
  stages:
    stage_1_language_detection:
      name: "Language Detection"
      description: "Detect source language and translation needs"
      supported_languages:
        - code: "vi"
          name: "Vietnamese"
          native: "Tiếng Việt"
          confidence_keywords: ["tạo", "xây dựng", "cải thiện", "sửa lỗi", "thiết kế"]
        - code: "zh"
          name: "Chinese"
          native: "中文"
          confidence_keywords: ["创建", "构建", "改进", "修复", "设计"]
        - code: "ja"
          name: "Japanese"
          native: "日本語"
          confidence_keywords: ["作成", "構築", "開発", "設計"]
        - code: "ko"
          name: "Korean"
          native: "한국어"
          confidence_keywords: ["생성", "구축", "개발", "설계"]
        - code: "en"
          name: "English"
          native: "English"
          confidence_keywords: ["create", "build", "improve", "fix", "design"]
      output:
        - detected_language
        - confidence_score
        - is_translated
        - original_text
        - translated_text
        
    stage_2_intent_classification:
      name: "Intent Classification"
      description: "Determine primary and secondary intents"
      intents:
        build:
          keywords: ["create", "build", "make", "add", "implement", "develop", "tạo", "xây dựng", "创建", "構築"]
          weight: 0.25
        redesign:
          keywords: ["improve", "upgrade", "redesign", "modernize", "enhance", "cải thiện", "改进"]
          weight: 0.20
        fix:
          keywords: ["fix", "bug", "error", "issue", "repair", "debug", "sửa lỗi", "修复"]
          weight: 0.20
        review:
          keywords: ["review", "check", "audit", "analyze", "assess", "kiểm tra", "审查"]
          weight: 0.15
        explain:
          keywords: ["explain", "how", "what", "why", "understand", "giải thích", "解释"]
          weight: 0.10
        security:
          keywords: ["security", "vulnerability", "auth", "JWT", "bảo mật", "安全"]
          weight: 0.10
      output:
        - primary_intent
        - secondary_intents
        - intent_scores
        - intent_confidence
        
    stage_3_domain_detection:
      name: "Domain Detection"
      description: "Identify technical domains"
      domains:
        frontend:
          keywords: ["frontend", "UI", "UX", "landing", "page", "component", "button", "form", "responsive", "react", "vue", "angular", "next", "nuxt"]
          file_patterns: ["*.tsx", "*.jsx", "*.vue", "*.svelte", "*.css", "*.scss"]
          associated_skills: ["frontend-taste", "frontend-redesign", "frontend-review"]
        backend:
          keywords: ["backend", "API", "server", "endpoint", "authentication", "CRUD", "REST", "GraphQL"]
          file_patterns: ["*.py", "*.java", "*.go", "*.ts", "*.js"]
          associated_skills: []
        security:
          keywords: ["security", "auth", "login", "password", "JWT", "OAuth", "XSS", "SQL injection", "vulnerability"]
          file_patterns: []
          associated_skills: ["security-review", "vietnam-payment-review"]
        payment:
          keywords: ["payment", "checkout", "stripe", "paypal", "MoMo", "SePay", "PayOS", "VNPay", "ZaloPay", "VietQR"]
          file_patterns: []
          associated_skills: ["vietnam-payment-review", "security-review"]
        mobile:
          keywords: ["mobile", "app", "iOS", "Android", "react native", "flutter", "expo"]
          file_patterns: ["*.tsx", "*.swift", "*.kt"]
          associated_skills: []
        database:
          keywords: ["database", "SQL", "PostgreSQL", "MySQL", "MongoDB", "migration", "schema"]
          file_patterns: ["*.sql", "*.prisma", "*.sqlite"]
          associated_skills: []
        devops:
          keywords: ["docker", "kubernetes", "CI/CD", "deployment", "AWS", "Azure", "GCP", "serverless"]
          file_patterns: ["Dockerfile", "docker-compose.yml", "*.yaml", "*.yml"]
          associated_skills: []
        knowledge:
          keywords: ["knowledge base", "RAG", "document", "wiki", "FAQ", "weknora"]
          file_patterns: []
          associated_skills: ["weknora-kb", "weknora-agent", "pixelrag"]
        ocr:
          keywords: ["ocr", "text extraction", "image to text", "scanned"]
          file_patterns: []
          associated_skills: ["document-ocr", "pixelrag"]
      output:
        - detected_domains
        - primary_domain
        - domain_confidence
        - domain_skills
        
    stage_4_skill_matching:
      name: "Skill Auto-Discovery"
      description: "Match skills based on detected patterns"
      matching_algorithm:
        type: "weighted_keyword_matching"
        thresholds:
          auto_select: 0.75
          suggest: 0.50
          ambiguous: 0.40
        weights:
          exact_keyword: 1.0
          partial_keyword: 0.5
          domain_match: 0.3
          file_pattern: 0.2
      mandatory_skills:
        - karpathy-coding  # Always runs with EVERY coding task
        - frontend-review  # Always runs with frontend tasks
      output:
        - matched_skills
        - skill_confidences
        - primary_skill
        - secondary_skills
        - required_gates
```

### 3.2 Skill Combination Matrix

```yaml
skill_combinations:
  # Frontend Landing/Portfolio
  landing_page:
    description: "New landing page or portfolio"
    primary_skill: "frontend-taste"
    required_skills:
      - frontend-taste
      - full-output
      - frontend-review
      - karpathy-coding
    gates:
      pre:
        - karpathy-pre
        - taste-pre
        - fulloutput-pre
        - review-pre
      post:
        - taste-post
        - fulloutput-post
        - review-post
        - karpathy-post
    dependencies:
      npm: ["tailwindcss", "framer-motion", "lucide-react"]
    estimated_complexity: "medium"
    estimated_tasks: 5
    
  # Frontend Redesign
  redesign:
    description: "Redesign existing site/app"
    primary_skill: "frontend-redesign"
    required_skills:
      - frontend-redesign
      - full-output
      - frontend-review
      - karpathy-coding
    gates:
      pre:
        - karpathy-pre
        - redesign-pre
        - fulloutput-pre
        - review-pre
      post:
        - redesign-post
        - fulloutput-post
        - review-post
        - karpathy-post
    dependencies:
      npm: ["tailwindcss", "prettier", "eslint"]
    estimated_complexity: "high"
    estimated_tasks: 6
    
  # Security Review
  security_review:
    description: "Security vulnerability assessment"
    primary_skill: "security-review"
    required_skills:
      - security-review
      - karpathy-coding
    gates:
      pre:
        - karpathy-pre
        - security-pre
      post:
        - security-post
        - karpathy-post
    dependencies:
      python: ["bandit", "safety"]
    estimated_complexity: "high"
    estimated_tasks: 4
    
  # Vietnam Payment
  vietnam_payment:
    description: "Vietnam payment integration"
    primary_skill: "vietnam-payment-review"
    required_skills:
      - vietnam-payment-review
      - security-review
      - full-output
      - karpathy-coding
    gates:
      pre:
        - karpathy-pre
        - payment-pre
        - security-pre
        - fulloutput-pre
      post:
        - payment-post
        - security-post
        - fulloutput-post
        - karpathy-post
    dependencies: []
    estimated_complexity: "high"
    estimated_tasks: 5
    
  # Knowledge Base Setup
  knowledge_base:
    description: "Knowledge base with RAG"
    primary_skill: "weknora-kb"
    required_skills:
      - weknora-kb
      - karpathy-coding
    gates:
      pre:
        - karpathy-pre
        - weknora-pre
      post:
        - weknora-post
        - karpathy-post
    dependencies:
      system: ["weknora-cli", "docker"]
      mcp: ["weknora"]
    estimated_complexity: "high"
    estimated_tasks: 6
    
  # Document OCR
  document_ocr:
    description: "Text extraction from documents"
    primary_skill: "document-ocr"
    required_skills:
      - document-ocr
      - karpathy-coding
    gates:
      pre:
        - karpathy-pre
        - ocr-pre
      post:
        - ocr-post
        - karpathy-post
    dependencies:
      python: ["pytesseract", "Pillow", "opencv-python"]
      system: ["tesseract"]
    estimated_complexity: "low"
    estimated_tasks: 3
    
  # Visual RAG
  visual_rag:
    description: "Visual document understanding"
    primary_skill: "pixelrag"
    required_skills:
      - pixelrag
      - karpathy-coding
    gates:
      pre:
        - karpathy-pre
        - pixelrag-pre
      post:
        - pixelrag-post
        - karpathy-post
    dependencies:
      python: ["pixelrag", "playwright"]
      system: ["chromium"]
    estimated_complexity: "medium"
    estimated_tasks: 4
    
  # Generic Build
  generic_build:
    description: "Generic build/implement task"
    primary_skill: null
    required_skills:
      - karpathy-coding
    gates:
      pre:
        - karpathy-pre
      post:
        - karpathy-post
    dependencies: []
    estimated_complexity: "low"
    estimated_tasks: 2
    
  # Generic Review
  generic_review:
    description: "Generic review/audit task"
    primary_skill: "frontend-review"
    required_skills:
      - frontend-review
      - karpathy-coding
    gates:
      pre:
        - karpathy-pre
        - review-pre
      post:
        - review-post
        - karpathy-post
    dependencies: []
    estimated_complexity: "medium"
    estimated_tasks: 3
```

---

## 4. Task Decomposition Engine

### 4.1 Task Template Library

```yaml
task_templates:
  karpathy_pre_gate:
    name: "Karpathy Pre-Review Gate"
    skill: "karpathy-coding"
    gate_type: "pre"
    description: "Think before coding - define assumptions, simplicity check, scope"
    subtasks:
      - id: "kpre-1"
        name: "State Assumptions"
        description: "Explicitly state all assumptions about the request"
        checkpoints:
          - "What framework/stack is assumed?"
          - "What files need to be modified?"
          - "What is the scope of changes?"
      - id: "kpre-2"
        name: "Simplicity Check"
        description: "Check if request is over-engineered or ambiguous"
        checkpoints:
          - "Is there a simpler approach?"
          - "Are there ambiguous interpretations?"
          - "Should I ask clarifying questions?"
      - id: "kpre-3"
        name: "Surgical Scope"
        description: "Define exactly what must be changed"
        checkpoints:
          - "What MUST be changed?"
          - "What should NOT be touched?"
          - "Will every changed line trace to the request?"
      - id: "kpre-4"
        name: "Goal Definition"
        description: "Define success criteria in verifiable terms"
        checkpoints:
          - "What does 'success' look like?"
          - "What verification steps are needed?"
    output_format: |
      ============================================================
      [KARPATHY PRE-REVIEW GATE]
      ============================================================
      
      Assumptions:
        - [ ] Framework: ...
        - [ ] Files to modify: ...
        - [ ] Scope: ...
      
      Simplicity Check:
        - [ ] Simpler approach exists: YES/NO
        - [ ] Ambiguous interpretations: ...
        - [ ] Clarification needed: YES/NO
      
      Surgical Scope:
        - [ ] Must change: ...
        - [ ] Must NOT touch: ...
        - [ ] Line traceability: ...
      
      Goals:
        - [ ] Success criteria: ...
        - [ ] Verification steps: ...
      
      >>> PRE-REVIEW GATE: PASS/FAIL
      ============================================================

  karpathy_post_gate:
    name: "Karpathy Post-Review Gate"
    skill: "karpathy-coding"
    gate_type: "post"
    description: "Verify surgical changes, simplicity maintained, goals achieved"
    subtasks:
      - id: "kpost-1"
        name: "Implementation Verification"
        description: "Verify changes are surgical and traceable"
        checkpoints:
          - "Every line connects to user's ask?"
          - "No adjacent code 'improved'?"
          - "Unused code removed?"
      - id: "kpost-2"
        name: "Simplicity Re-Check"
        description: "Re-verify simplicity after implementation"
        checkpoints:
          - "Could written code be shorter?"
          - "Any speculative abstractions added?"
          - "Any unnecessary flexibility?"
      - id: "kpost-3"
        name: "Goal Achievement"
        description: "Verify all success criteria met"
        checkpoints:
          - "All verification steps pass?"
          - "No regressions introduced?"
          - "Changes are minimal and surgical?"
    output_format: |
      ============================================================
      [KARPATHY POST-REVIEW GATE]
      ============================================================
      
      Implementation:
        - [ ] Surgical changes: PASS/FAIL
        - [ ] No adjacent improvements: PASS/FAIL
        - [ ] Unused code removed: PASS/FAIL
      
      Simplicity:
        - [ ] No over-engineering: PASS/FAIL
        - [ ] No speculative abstractions: PASS/FAIL
        - [ ] Minimal code: PASS/FAIL
      
      Goals:
        - [ ] Success criteria met: PASS/FAIL
        - [ ] No regressions: PASS/FAIL
        - [ ] Minimal changes: PASS/FAIL
      
      >>> POST-REVIEW GATE: PASS/FAIL
      ============================================================

  frontend_taste_pre:
    name: "Frontend Taste Pre-Review Gate"
    skill: "frontend-taste"
    gate_type: "pre"
    description: "Design read declaration, anti-default discipline, dial values"
    subtasks:
      - id: "ftpre-1"
        name: "Brief Inference"
        description: "Understand page kind, vibe, audience, brand"
        checkpoints:
          - "Page kind: landing/portfolio/editorial?"
          - "Vibe words: modern/premium/minimalist?"
          - "Audience: B2B/consumer/investor?"
          - "Brand assets available?"
      - id: "ftpre-2"
        name: "Design Read Declaration"
        description: "Declare design read (1 line, verbatim)"
        checkpoints:
          - "Reading this as: [CONTEXT] for [AUDIENCE]"
          - "With a [AESTHETIC] language"
          - "Leaning toward [DESIGN SYSTEM]"
      - id: "ftpre-3"
        name: "Anti-Default Discipline"
        description: "Eliminate AI-slop patterns"
        checkpoints:
          - "No AI-purple gradients"
          - "No generic glassmorphism"
          - "No Inter font as default"
          - "No three-equal cards"
      - id: "ftpre-4"
        name: "Dial Values"
        description: "Set design dial values"
        checkpoints:
          - "VARIANCE (1-10): ..."
          - "MOTION (1-10): ..."
          - "DENSITY (1-10): ..."

  frontend_taste_post:
    name: "Frontend Taste Post-Review Gate"
    skill: "frontend-taste"
    gate_type: "post"
    description: "Verify layout, typography, animation, assets"
    subtasks:
      - id: "ftpost-1"
        name: "Layout & Structure"
        description: "Verify layout quality"
        checkpoints:
          - "Hero fits viewport?"
          - "Section diversity?"
          - "No split-header pattern?"
      - id: "ftpost-2"
        name: "Typography & Content"
        description: "Verify typography quality"
        checkpoints:
          - "No em-dashes?"
          - "No fake-precise numbers?"
          - "No generic names?"
      - id: "ftpost-3"
        name: "Animation & Motion"
        description: "Verify animation quality"
        checkpoints:
          - "Motion = Motion shown?"
          - "Reduced motion supported?"
      - id: "ftpost-4"
        name: "Assets & Images"
        description: "Verify asset quality"
        checkpoints:
          - "Real images used?"
          - "No div-based fake screenshots?"

  fulloutput_pre:
    name: "Full Output Pre-Review Gate"
    skill: "full-output"
    gate_type: "pre"
    description: "Lock scope and deliverables"
    subtasks:
      - id: "fopre-1"
        name: "Scope Lock"
        description: "Lock full request understanding"
        checkpoints:
          - "Full request read and understood"
          - "Deliverable count locked: N items"
          - "This count is a contract"
      - id: "fopre-2"
        name: "Dependency Check"
        description: "Identify all dependencies"
        checkpoints:
          - "Packages needed: ..."
          - "Framework/stack confirmed"
          - "File paths confirmed"

  fulloutput_post:
    name: "Full Output Post-Review Gate"
    skill: "full-output"
    gate_type: "post"
    description: "Verify completeness - no skeletons, no TODOs"
    subtasks:
      - id: "fopost-1"
        name: "Completeness Check"
        description: "Verify no truncation patterns"
        checkpoints:
          - "No // ... patterns"
          - "No // TODO comments"
          - "No // implement here"
          - "No skeleton code"
      - id: "fopost-2"
        name: "Quality Check"
        description: "Verify code quality"
        checkpoints:
          - "All imports exist"
          - "No hardcoded values"
          - "Error handling present"
      - id: "fopost-3"
        name: "File Structure Check"
        description: "Verify file structure"
        checkpoints:
          - "All paths match"
          - "Entry points correct"
          - "No circular imports"

  review_pre:
    name: "Frontend Review Pre-Review Gate"
    skill: "frontend-review"
    gate_type: "pre"
    description: "Scope analysis and quality plan"
    subtasks:
      - id: "rvpre-1"
        name: "Scope Analysis"
        description: "Analyze full scope"
        checkpoints:
          - "All requirements understood"
          - "Files to touch listed"
          - "Dependencies identified"
      - id: "rvpre-2"
        name: "Quality Plan"
        description: "Define quality checks"
        checkpoints:
          - "Correctness checks planned"
          - "Design checks planned"
          - "Accessibility checks planned"

  review_post:
    name: "Frontend Review Post-Review Gate"
    skill: "frontend-review"
    gate_type: "post"
    description: "Comprehensive quality verification"
    subtasks:
      - id: "rvpost-1"
        name: "Correctness Review"
        description: "Code correctness"
        checkpoints:
          - "Builds without errors"
          - "No TypeScript errors"
          - "All imports resolve"
      - id: "rvpost-2"
        name: "Design & Taste Review"
        description: "Design quality"
        checkpoints:
          - "Design read declared"
          - "Dial values set"
          - "No AI-slop patterns"
      - id: "rvpost-3"
        name: "Accessibility Review"
        description: "A11y quality"
        checkpoints:
          - "Alt text present"
          - "Color contrast passes"
          - "Focus indicators visible"
      - id: "rvpost-4"
        name: "Performance Review"
        description: "Performance quality"
        checkpoints:
          - "LCP < 2.5s"
          - "Images have dimensions"
          - "No layout jank"
```

### 4.2 Implementation Task Templates

```yaml
implementation_templates:
  landing_hero_section:
    name: "Hero Section Implementation"
    description: "Create hero section with headline, subtext, CTA"
    estimated_time: "15-20 minutes"
    checkpoints:
      - "Headline max 2 lines"
      - "Subtext max 20 words"
      - "CTA button with hover state"
      - "Responsive mobile collapse"
    skills_needed: ["frontend-taste", "karpathy-coding"]
    
  landing_features_section:
    name: "Features Section Implementation"
    description: "Create features showcase section"
    estimated_time: "20-25 minutes"
    checkpoints:
      - "3-4 feature cards"
      - "Icons from allowed library"
      - "Hover states"
      - "Responsive grid"
    skills_needed: ["frontend-taste", "karpathy-coding"]
    
  landing_cta_section:
    name: "CTA Section Implementation"
    description: "Create call-to-action section"
    estimated_time: "10-15 minutes"
    checkpoints:
      - "Clear CTA text"
      - "Button with contrast"
      - "Background treatment"
    skills_needed: ["frontend-taste", "karpathy-coding"]
    
  api_endpoint:
    name: "API Endpoint Implementation"
    description: "Create REST API endpoint"
    estimated_time: "20-30 minutes"
    checkpoints:
      - "Request validation"
      - "Response format"
      - "Error handling"
      - "Authentication"
    skills_needed: ["karpathy-coding"]
    
  database_migration:
    name: "Database Migration"
    description: "Create database migration"
    estimated_time: "15-25 minutes"
    checkpoints:
      - "Schema defined"
      - "Up migration written"
      - "Down migration written"
      - "Constraints added"
    skills_needed: ["karpathy-coding"]
    
  payment_webhook:
    name: "Payment Webhook Handler"
    description: "Implement payment webhook"
    estimated_time: "25-35 minutes"
    checkpoints:
      - "Signature validation"
      - "Idempotency handling"
      - "Error logging"
      - "Status update"
    skills_needed: ["vietnam-payment-review", "security-review", "karpathy-coding"]
```

---

## 5. Dependency Auto-Installation

### 5.1 Dependency Resolver

```yaml
dependency_resolver:
  version: "1.0.0"
  
  resolution_strategy:
    priority:
      - "system"           # OS-level dependencies first
      - "python"          # Python packages
      - "npm"             # Node.js packages
      - "docker"          # Container images
      - "mcp"             # MCP servers
    
    auto_install_threshold:
      confidence: 0.75
      user_prompt: true
    
    install_options:
      skip_if_satisfied: true
      force_reinstall: false
      install_optional: true
      
  package_managers:
    python:
      command: "pip"
      install: "pip install {packages}"
      check: "pip show {package}"
      verify: "pip --version"
      
    npm:
      command: "npm"
      install: "npm install {packages}"
      check: "npm list {package}"
      verify: "npm --version"
      
    system:
      tesseract:
        windows:
          download: "https://github.com/UB-Mannheim/tesseract/releases"
          verify: "tesseract --version"
        macos:
          install: "brew install tesseract tesseract-lang"
          verify: "tesseract --version"
        linux:
          install: "sudo apt install tesseract-ocr tesseract-ocr-vie"
          verify: "tesseract --version"
          
      docker:
        install: "docker --version"
        verify: "docker ps"
        
  weknora_setup:
    cli_check: "weknora --version"
    docker_check: "docker ps"
    mcp_config_path: "~/.cursor/mcp.json"
    setup_script: ".cursor/scripts/weknora/setup-mcp.ps1"
    
  pixelrag_setup:
    python_check: "pip show pixelrag"
    playwright_check: "playwright --version"
    chromium_check: "chromium --version"
```

### 5.2 MCP Auto-Setup

```yaml
mcp_auto_setup:
  version: "1.0.0"
  
  setup_workflow:
    detect:
      - Check if MCP servers are configured
      - List available MCP servers
      - Check connection status
      
    configure:
      - Generate MCP config if not exists
      - Merge with existing config
      - Validate JSON structure
      
    enable:
      - Restart Cursor to load config
      - Verify connection status
      - Log any errors
      
  supported_servers:
    weknora:
      setup_script: ".cursor/scripts/weknora/setup-mcp.ps1"
      requires_api_key: true
      docker_compose: "docker-compose.yml"
      health_check: "weknora health"
      
    cursor-ide-browser:
      status: "built-in"
      requires_auth: false
      health_check: "browser tabs list"
      
    user-codegraph:
      status: "built-in"
      requires_auth: false
      health_check: "codegraph status"
      init_command: "codegraph init -i"
```

---

## 6. Task Distribution System

### 6.1 Task Manifest Schema

```yaml
task_manifest:
  version: "1.0.0"
  generated_at: "2026-06-26T13:00:00Z"
  request_id: "uuid-v4"
  
  input:
    original_request: "string"
    detected_language: "vi|en|zh|ja|ko"
    translated_request: "string"
    primary_intent: "build|redesign|fix|review|explain|security"
    primary_domain: "string"
    
  analysis:
    skills_selected:
      - skill_id: "string"
        skill_name: "string"
        confidence: 0.0-1.0
        role: "primary|secondary|mandatory|overlay"
        
    rules_matched:
      - rule_id: "string"
        rule_name: "string"
        
    gates_required:
      pre:
        - gate_id: "string"
          gate_name: "string"
          skill: "string"
      post:
        - gate_id: "string"
          gate_name: "string"
          skill: "string"
          
    dependencies:
      python: ["package1", "package2"]
      npm: ["package1", "package2"]
      system: ["tesseract", "docker"]
      mcp: ["weknora", "browser"]
      
  tasks:
    - task_id: "task-1"
      task_name: "string"
      task_type: "pre-gate|implementation|post-gate|delivery"
      description: "string"
      estimated_time: "string"
      skills_applied: ["string"]
      subtasks:
        - subtask_id: "string"
          name: "string"
          description: "string"
          checkpoints: ["string"]
      dependencies: ["task-id"]  # Must complete before these tasks
      status: "pending|in_progress|completed|failed"
      
  execution_order:
    sequential:
      - ["task-1", "task-2", "task-3"]
    parallel_groups:
      - ["task-4a", "task-4b"]  # These can run in parallel
      
  output:
    summary: "string"
    deliverables: ["string"]
    warnings: ["string"]
    next_steps: ["string"]
```

### 6.2 Example Task Manifest

```yaml
example_manifest:
  input:
    original_request: "Tạo một landing page đẹp cho startup AI của tôi"
    detected_language: "vi"
    translated_request: "Create a beautiful landing page for my AI startup"
    primary_intent: "build"
    primary_domain: "frontend"
    
  analysis:
    skills_selected:
      - skill_id: "frontend-taste"
        skill_name: "Frontend Taste"
        confidence: 0.92
        role: "primary"
      - skill_id: "full-output"
        skill_name: "Full Output"
        confidence: 0.85
        role: "secondary"
      - skill_id: "frontend-review"
        skill_name: "Frontend Review"
        confidence: 1.0
        role: "mandatory"
      - skill_id: "karpathy-coding"
        skill_name: "Karpathy Coding"
        confidence: 1.0
        role: "overlay"
        
    rules_matched:
      - frontend-architecture
      - ui-visual-design
      - coding-standards
      
    gates_required:
      pre:
        - karpathy-pre
        - taste-pre
        - fulloutput-pre
        - review-pre
      post:
        - taste-post
        - fulloutput-post
        - review-post
        - karpathy-post
        
    dependencies:
      npm: ["tailwindcss", "framer-motion", "lucide-react"]
      system: []
      mcp: []
      
  tasks:
    - task_id: "task-0"
      task_name: "Pre-Review Gates"
      task_type: "pre-gate"
      description: "Run all pre-review gates before implementation"
      estimated_time: "10 minutes"
      skills_applied: ["karpathy-coding", "frontend-taste", "full-output"]
      subtasks:
        - subtask_id: "task-0-kpre"
          name: "Karpathy Pre-Gate"
          checkpoints: ["Assumptions stated", "Simplicity checked", "Scope defined"]
        - subtask_id: "task-0-tastepre"
          name: "Frontend Taste Pre-Gate"
          checkpoints: ["Design read declared", "Anti-default checked", "Dials set"]
        - subtask_id: "task-0-fopre"
          name: "Full Output Pre-Gate"
          checkpoints: ["Scope locked", "Deliverables counted"]
      status: "pending"
      
    - task_id: "task-1"
      task_name: "Hero Section"
      task_type: "implementation"
      description: "Create hero section with headline, subtext, CTA"
      estimated_time: "20 minutes"
      skills_applied: ["frontend-taste", "karpathy-coding"]
      subtasks:
        - subtask_id: "task-1-nav"
          name: "Navigation Bar"
          checkpoints: ["Logo", "Nav links", "Mobile menu"]
        - subtask_id: "task-1-hero"
          name: "Hero Content"
          checkpoints: ["Headline", "Subtext", "CTA button"]
      dependencies: ["task-0"]
      status: "pending"
      
    - task_id: "task-2"
      task_name: "Features Section"
      task_type: "implementation"
      description: "Create features showcase section"
      estimated_time: "25 minutes"
      skills_applied: ["frontend-taste", "karpathy-coding"]
      dependencies: ["task-1"]
      status: "pending"
      
    - task_id: "task-3"
      task_name: "Social Proof Section"
      task_type: "implementation"
      description: "Create logo wall and testimonials"
      estimated_time: "20 minutes"
      skills_applied: ["frontend-taste", "karpathy-coding"]
      dependencies: ["task-2"]
      status: "pending"
      
    - task_id: "task-4"
      task_name: "CTA Section"
      task_type: "implementation"
      description: "Create final CTA section"
      estimated_time: "15 minutes"
      skills_applied: ["frontend-taste", "karpathy-coding"]
      dependencies: ["task-3"]
      status: "pending"
      
    - task_id: "task-5"
      task_name: "Post-Review Gates"
      task_type: "post-gate"
      description: "Run all post-review gates after implementation"
      estimated_time: "15 minutes"
      skills_applied: ["karpathy-coding", "frontend-taste", "full-output", "frontend-review"]
      subtasks:
        - subtask_id: "task-5-tastepost"
          name: "Frontend Taste Post-Gate"
          checkpoints: ["Layout", "Typography", "Animation", "Assets"]
        - subtask_id: "task-5-fopost"
          name: "Full Output Post-Gate"
          checkpoints: ["No skeletons", "No TODOs", "Complete"]
        - subtask_id: "task-5-reviewpost"
          name: "Frontend Review Post-Gate"
          checkpoints: ["Correctness", "Design", "A11y", "Performance"]
        - subtask_id: "task-5-kpost"
          name: "Karpathy Post-Gate"
          checkpoints: ["Surgical", "Simple", "Goals met"]
      dependencies: ["task-4"]
      status: "pending"
      
    - task_id: "task-6"
      task_name: "Delivery"
      task_type: "delivery"
      description: "Deliver final code to user"
      estimated_time: "5 minutes"
      dependencies: ["task-5"]
      status: "pending"
      
  execution_order:
    sequential: ["task-0", "task-1", "task-2", "task-3", "task-4", "task-5", "task-6"]
    
  output:
    summary: "Landing page for AI startup with hero, features, social proof, CTA"
    deliverables:
      - "Hero section with navigation"
      - "Features section with 4 feature cards"
      - "Logo wall section"
      - "Final CTA section"
    warnings: []
    next_steps:
      - "Run npm install for dependencies"
      - "Start dev server"
      - "Test on mobile"
```

---

## 7. CLI & Integration

### 7.1 Task Analyzer CLI

```powershell
# Task Analyzer CLI
# Usage: .\.cursor\scripts\task-analyzer.ps1 -Request "your request"

param(
    [Parameter(Position=0, ValueFromRemainingArguments=$true)]
    [string]$Request = "",
    
    [switch]$Analyze,
    [switch]$GenerateTasks,
    [switch]$InstallDeps,
    [switch]$Execute,
    [switch]$Verbose,
    [switch]$DryRun
)

# Colors
function Write-Step { param($M) Write-Host "[STEP] $M" -ForegroundColor Cyan }
function Write-Success { param($M) Write-Host "[OK] $M" -ForegroundColor Green }
function Write-Warn { param($M) Write-Host "[WARN] $M" -ForegroundColor Yellow }
function Write-Error { param($M) Write-Host "[ERROR] $M" -ForegroundColor Red }

# Main execution
if ($Request -eq "" -and -not $Analyze) {
    Write-Host @"
╔══════════════════════════════════════════════════════════════════════════════╗
║                TASK ANALYZER - Cursor Enterprise Framework                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Usage:                                                                      ║
║    .\.cursor\scripts\task-analyzer.ps1 -Request "your request here"         ║
║                                                                              ║
║  Options:                                                                    ║
║    -Request       Your request (any language)                                ║
║    -Analyze      Analyze request and show skill detection                   ║
║    -GenerateTasks Generate task manifest with subtasks                       ║
║    -InstallDeps  Auto-install missing dependencies                           ║
║    -Execute      Execute tasks (requires -GenerateTasks first)               ║
║    -DryRun       Show what would happen without executing                    ║
║    -Verbose      Show detailed output                                       ║
║                                                                              ║
║  Examples:                                                                   ║
║    .\.cursor\scripts\task-analyzer.ps1 -Request "Tạo landing page"           ║
║    .\.cursor\scripts\task-analyzer.ps1 -Analyze -Request "Fix login bug"   ║
║    .\.cursor\scripts\task-analyzer.ps1 -GenerateTasks -Request "Build API"  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"@
    exit 0
}

# Step 1: Context Sync
Write-Step "Synchronizing context registry..."
$contextSync = Sync-ContextRegistry
Write-Success "Context synced: $($contextSync.rules) rules, $($contextSync.skills) skills"

# Step 2: Language Detection
Write-Step "Detecting language..."
$langResult = Detect-Language -Text $Request
Write-Host "  Detected: $($langResult.language) (confidence: $($langResult.confidence))"

# Step 3: Translation
if ($langResult.language -ne "en") {
    Write-Step "Translating to English..."
    $Request = Translate-ToEnglish -Text $Request -SourceLang $langResult.language
    Write-Success "Translated: $Request"
}

# Step 4: Intent Analysis
Write-Step "Analyzing intent..."
$intentResult = Analyze-Intent -Text $Request
Write-Host "  Primary Intent: $($intentResult.primary_intent)"
Write-Host "  Domains: $($intentResult.domains -join ', ')"

# Step 5: Skill Detection
Write-Step "Detecting skills..."
$skillResult = Detect-Skills -Text $Request -Intent $intentResult
Write-Success "Skills detected:"
$skillResult.matched_skills | ForEach-Object {
    Write-Host "  - $_ (confidence: $($skillResult.confidences[$_]))"
}

# Step 6: Generate Tasks
if ($GenerateTasks -or $Execute) {
    Write-Step "Generating task manifest..."
    $manifest = New-TaskManifest -Request $Request -Analysis $skillResult
    
    if ($Verbose) {
        Write-Host ($manifest | ConvertTo-Json -Depth 10)
    } else {
        Write-Host $manifest.summary
    }
}

# Step 7: Dependency Check
Write-Step "Checking dependencies..."
$deps = Get-RequiredDependencies -Skills $skillResult.matched_skills
if ($deps.missing.Count -gt 0) {
    Write-Warn "Missing dependencies: $($deps.missing -join ', ')"
    
    if ($InstallDeps) {
        Write-Step "Auto-installing dependencies..."
        Install-Dependencies -Packages $deps.missing
    } else {
        Write-Host "  Run with -InstallDeps to auto-install"
    }
} else {
    Write-Success "All dependencies satisfied"
}

# Step 8: Execute (if requested)
if ($Execute -and -not $DryRun) {
    Write-Step "Executing tasks..."
    $result = Invoke-TaskExecution -Manifest $manifest
    Write-Success "Execution complete: $($result.completed)/$($result.total) tasks"
} elseif ($DryRun) {
    Write-Step "[DRY RUN] Would execute $($manifest.tasks.Count) tasks"
}

Write-Host ""
Write-Success "Task Analysis Complete!"
```

### 7.2 Integration with Skill Detection

```yaml
skill_detection_integration:
  description: "How task analyzer integrates with skill-integration.mdc"
  
  auto_discovery_flow:
    1_request_received:
      source: "user input"
      action: "pass to task analyzer"
      
    2_language_detection:
      source: "multi-language-vibe-code.mdc"
      action: "detect and translate"
      
    3_intent_analysis:
      source: "skill-integration.mdc Section A"
      action: "classify intent"
      
    4_skill_matching:
      source: "skill-integration.mdc Section A.2"
      action: "match against keyword matrix"
      
    5_confidence_scoring:
      source: "skill-integration.mdc Section A.3"
      action: "calculate confidence scores"
      
    6_skill_combination:
      source: "skill-integration.mdc Section A.4"
      action: "determine skill combination"
      
    7_task_generation:
      source: "this document Section 4"
      action: "generate task manifest with subtasks"
      
    8_dependency_resolution:
      source: "this document Section 5"
      action: "check and install deps"
      
    9_execution:
      source: "skill-integration.mdc Section B-E"
      action: "run pre-review → implement → post-review → deliver"
      
  gate_mapping:
    karpathy-pre: "Section K.1-K.4"
    karpathy-post: "Section K.5-K.7"
    taste-pre: "Section 0.A-0.F"
    taste-post: "Section 6.A-6.H"
    redesign-pre: "Section 0.A-0.E"
    redesign-post: "Section 4.A-4.E"
    fulloutput-pre: "Section 0.A-0.B"
    fulloutput-post: "Section 5.A-5.C"
    review-pre: "Section A.1-A.3"
    review-post: "Section B.1-B.7"
    security-pre: "Section S.1-S.3"
    security-post: "Section Security-1-9"
    payment-pre: "Payment Section Pre"
    payment-post: "Payment Section Post"
```

---

## 8. Quick Reference

### 8.1 Task Analysis Flow

```
REQUEST (Any Language)
         │
         ▼
┌─────────────────────────────────────┐
│ 1. CONTEXT SYNC                     │
│    • Load Rule Registry (84 rules)  │
│    • Load Skill Registry (17 skills)│
│    • Load MCP Registry (5 servers)  │
│    • Load Dependency Manifest       │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 2. LANGUAGE DETECTION               │
│    • Vietnamese, Chinese, Japanese  │
│    • Korean, English, etc.          │
│    • Confidence scoring             │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 3. TRANSLATION                      │
│    • Translate to English           │
│    • Preserve tech terms           │
│    • Semantic preservation         │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 4. INTENT ANALYSIS                  │
│    • Primary intent (build/fix/etc.)│
│    • Secondary intents             │
│    • Confidence scores             │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 5. DOMAIN DETECTION                 │
│    • Frontend, Backend, Security   │
│    • Payment, Database, DevOps     │
│    • Knowledge, OCR, etc.          │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 6. SKILL AUTO-DISCOVERY             │
│    • Match against Skill Matrix    │
│    • Calculate confidence          │
│    • Determine mandatory skills    │
│    • Identify skill combinations  │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 7. TASK DECOMPOSITION               │
│    • Pre-gate tasks                │
│    • Implementation tasks          │
│    • Post-gate tasks              │
│    • Delivery task                │
│    • Subtasks with checkpoints     │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 8. DEPENDENCY RESOLUTION            │
│    • Check Python packages          │
│    • Check npm packages            │
│    • Check system dependencies     │
│    • Check MCP servers             │
│    • Auto-install if needed        │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 9. EXECUTION                        │
│    • Sequential task execution      │
│    • Parallel groups (if any)      │
│    • Progress tracking             │
│    • Gate verification             │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ 10. DELIVERY                        │
│     • Final code delivery          │
│     • Summary                      │
│     • Next steps                   │
└─────────────────────────────────────┘
```

### 8.2 Skill Decision Tree

```
IS REQUEST ABOUT...
│
├─► PAYMENT? (MoMo, SePay, PayOS, VNPay, ZaloPay, VietQR)
│   ├─► + SECURITY? → vietnam-payment-review + security-review
│   └─► PAYMENT ONLY → vietnam-payment-review + security-review (if auth)
│
├─► SECURITY? (vulnerability, pentest, CVE, OWASP)
│   └─► → security-review (± reverse-skill)
│
├─► FRONTEND? (UI, landing, redesign, component)
│   ├─► REDESIGN? → frontend-redesign + full-output + frontend-review
│   ├─► BUILD? → frontend-taste + full-output + frontend-review
│   ├─► REVIEW? → frontend-review (standalone)
│   └─► OPEN-DESIGN? → open-design + frontend-taste
│
├─► KNOWLEDGE? (RAG, wiki, FAQ, weknora)
│   ├─► KB SETUP? → weknora-kb + karpathy-coding
│   ├─► AGENT? → weknora-agent + weknora-kb
│   └─► VISUAL? → pixelrag + karpathy-coding
│
├─► OCR? (text extraction, image to text)
│   └─► → document-ocr + karpathy-coding
│
├─► VIETNAM ADDRESS? (province, district, ward)
│   └─► → vietnam-address + karpathy-coding
│
├─► BAZI? (八字, fortune, birth chart)
│   └─► → bazi (standalone)
│
└─► DEFAULT?
    └─► karpathy-coding (overlay) + any detected skill
```

### 8.3 CLI Quick Reference

```powershell
# Quick analysis
.\.cursor\scripts\task-analyzer.ps1 -Request "Tạo landing page đẹp"

# Analyze only
.\.cursor\scripts\task-analyzer.ps1 -Analyze -Request "Fix login bug"

# Generate and show tasks
.\.cursor\scripts\task-analyzer.ps1 -GenerateTasks -Request "Build API endpoint"

# Full execution with deps install
.\.cursor\scripts\task-analyzer.ps1 -Execute -InstallDeps -Request "Add MoMo payment"

# Dry run
.\.cursor\scripts\task-analyzer.ps1 -GenerateTasks -DryRun -Request "Redesign homepage"
```

---

## 9. Files Reference

| File | Path | Purpose |
|------|------|---------|
| task-analyzer.ps1 | .cursor/scripts/task-analyzer.ps1 | Main CLI tool |
| task-analyzer.md | .cursor/scripts/task-analyzer.md | This documentation |
| skill-dependencies.json | .cursor/scripts/skill-dependencies.json | Dependency manifest |
| skill-installer.ps1 | .cursor/scripts/skill-installer.ps1 | Dependency installer |
| setup-mcp.ps1 | .cursor/scripts/weknora/setup-mcp.ps1 | MCP setup |
| build-embeddings.ps1 | .cursor/scripts/embedding-builder/build-embeddings.ps1 | Vector DB builder |

---

## 10. Related Documents

- [[multi-language-vibe-code]] - Multi-language request processing
- [[skill-integration]] - Skill auto-discovery protocol
- [[context-router]] - Context routing rules
- [[memory-first]] - Memory context management
- [[karpathy-coding]] - Vibe coding discipline
- [[frontend-taste]] - Frontend design skill
- [[frontend-redesign]] - Redesign skill
- [[frontend-review]] - Quality review skill
- [[security-review]] - Security review skill
- [[vietnam-payment-review]] - Vietnam payment skill
