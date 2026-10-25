/**
 * Prompt library for the /prompts page.
 * Each prompt composes rules + skills + agents from the framework catalog so the
 * prompt runner can show "what's being applied" alongside the prompt body.
 *
 * In a production deployment these would call an LLM endpoint; here we render a
 * realistic execution trace (plan → diff → review → metrics) so the page itself
 * is a useful artifact even without a backend.
 */

export type FrameworkRefType = 'rule' | 'skill' | 'agent'

export interface FrameworkRef {
  type: FrameworkRefType
  id: string // matches FrameworkItem.id from data/framework.ts
  reason: string // why this is in the chain — shown to the user
}

export interface PromptExecutionStep {
  phase: 'plan' | 'pre-review' | 'run' | 'post-review' | 'deliver'
  label: string
  by: string // which rule/skill/agent ran this phase
  bullets: string[]
}

export interface PromptItem {
  id: string
  category: 'Spec' | 'Review' | 'Build' | 'Debug' | 'Ship'
  title: string
  oneLiner: string
  prompt: string // the literal prompt body
  applies: FrameworkRef[] // rules + skills + agents wired in
  expectedDelta: string // user-facing metric improvement
  trace: PromptExecutionStep[]
  slashCommand?: string // e.g. /ui-ux, /dashboard-ui
  tags?: string[]
}

export const PROMPTS: PromptItem[] = [
  {
    id: 'spec-crm',
    category: 'Spec',
    title: 'Spec — Multi-tenant CRM',
    oneLiner: 'Turn a one-line idea into a complete PRD with verifiable steps.',
    prompt: `Build a multi-tenant CRM with RLS, RabbitMQ events, Supabase auth, role-based access (sales / manager / admin), Vietnamese address parsing, Zalo OA integration. Max 65-char email. ASCII username only.`,
    applies: [
      { type: 'rule', id: 'task-analyzer', reason: 'Splits the spec into subtasks before any work begins.' },
      { type: 'rule', id: 'karpathy-guidelines', reason: 'Surface tradeoffs, ask before assuming.' },
      { type: 'skill', id: 'ponytail', reason: 'Enforces YAGNI ladder — refuse speculative scope.' },
      { type: 'skill', id: 'full-output', reason: 'No placeholders, complete spec.' }
    ],
    expectedDelta: '+847% context · 4.2× more accurate',
    trace: [
      {
        phase: 'plan',
        label: 'Task manifest',
        by: 'task-analyzer',
        bullets: [
          'Step 1: Supabase project + RLS policies for users, orgs, memberships',
          'Step 2: OAuth + PKCE flow, encrypted refresh-token storage',
          'Step 3: RBAC middleware (sales / manager / admin)',
          'Step 4: Vietnamese address parser integration',
          'Step 5: Zalo OA webhook with HMAC-SHA256 verification',
          'Step 6: Integration tests covering 401 / 403 / idempotency'
        ]
      },
      {
        phase: 'pre-review',
        label: 'Pre-flight gates',
        by: 'karpathy-coding · full-output',
        bullets: [
          'Assumptions stated: tenancy=pool, gateway=Zalo OA only, no SSO',
          'Deliverable count locked: 6 services, 14 endpoints, 8 policies',
          'Constraints: 65-char email cap, ASCII usernames enforced in DB constraint'
        ]
      },
      {
        phase: 'run',
        label: 'Implementation',
        by: 'framework playbook',
        bullets: [
          'DI graph built via NestJS modules; no circular dependencies',
          'RLS policies checked against the integration test fixtures',
          'Webhook signature verified before any handler runs'
        ]
      },
      {
        phase: 'post-review',
        label: 'Quality gates',
        by: 'code-reviewer · security-auditor · test-engineer',
        bullets: [
          'Five-axis review: 0 CRITICAL · 2 HIGH (closed) · 1 MEDIUM (filed)',
          'OWASP: secrets in vault, no string-built SQL, CSP headers applied',
          'Tests: 142 added · coverage 91% on services · 0 flaky in last 5 runs'
        ]
      },
      {
        phase: 'deliver',
        label: 'Ship-ready',
        by: 'workflow-engines',
        bullets: [
          'CI green on Node 20/22 · Docker image 188MB',
          'Feature flag SALE_RBAC_V2 behind a 10% rollout',
          'Rollback plan: previously deployed image pinned + migration down-script'
        ]
      }
    ]
  },
  {
    id: 'review-five-axis',
    category: 'Review',
    title: 'Five-Axis Code Review',
    oneLiner: 'A reviewer that never rubber-stamps and never invents issues.',
    prompt: `Review the diff under /api/billing/webhook. Use five axes: (1) correctness (race conditions, off-by-one), (2) design (single responsibility, dependency inversion), (3) security (OWASP, secrets), (4) performance (N+1, cache), (5) a11y (WCAG 2.1 AA). Score 1-5 per axis. Block above 4/10.`,
    applies: [
      { type: 'agent', id: 'code-reviewer', reason: 'Owns the five-axis protocol.' },
      { type: 'rule', id: 'coding-standards', reason: 'Baseline style + naming checks.' },
      { type: 'rule', id: 'security', reason: 'OWASP cross-reference on every finding.' }
    ],
    expectedDelta: '7 issues caught / 200 LOC',
    trace: [
      {
        phase: 'plan',
        label: 'Scope the review',
        by: 'code-reviewer',
        bullets: [
          'Files: billing/webhook.ts + 3 tests · ~220 LOC',
          'Axes to apply: 5 — all loaded into context'
        ]
      },
      {
        phase: 'run',
        label: 'Walk axes',
        by: 'code-reviewer',
        bullets: [
          'Correctness: 2/5 — provider sends duplicate events; idempotency key missing',
          'Design: 4/5 — handler does parsing and persistence (split recommended)',
          'Security: 3/5 — webhook signature verified BUT timestamp window 10 min (loose)',
          'Performance: 4/5 — no N+1, one cache miss on tenant lookup',
          'A11y: N/A (no UI surface)'
        ]
      },
      {
        phase: 'post-review',
        label: 'Output',
        by: 'code-reviewer',
        bullets: [
          'Verdict: REQUEST CHANGES',
          'Critical 0 · High 1 · Medium 2 · Low 1',
          'Includes file:line citations and remediation snippets'
        ]
      }
    ]
  },
  {
    id: 'build-landing',
    category: 'Build',
    title: 'Build — Bazi landing page',
    oneLiner: 'Anti-slop landing page shipped in one shot.',
    prompt: `Build the Bazi (Tứ Trụ) landing from the framework. Use the frontend-taste dials (VARIANCE 7, MOTION 7, DENSITY 4). No AI-purple gradients, no three equal feature cards. Animations honor prefers-reduced-motion.`,
    applies: [
      { type: 'skill', id: 'frontend-taste', reason: 'Anti-slop landing page discipline.' },
      { type: 'skill', id: 'full-output', reason: 'No placeholder sections.' },
      { type: 'skill', id: 'frontend-review', reason: 'Dual-gate quality check (pre + post).' },
      { type: 'rule', id: 'ui-visual-design', reason: 'Token system + motion curves.' }
    ],
    expectedDelta: 'Lighthouse 100 · CLS 0.00 · Total bundle 234KB',
    trace: [
      {
        phase: 'plan',
        label: 'Design read',
        by: 'frontend-taste',
        bullets: [
          'Page kind: cultural landing · audience: Vietnamese consumers · vibe: "Á Đông hiện đại"',
          'Three dials declared: VARIANCE 7 · MOTION 7 · DENSITY 4',
          'Anti-defaults rejected: AI-purple gradients, three feature cards, mesh blobs'
        ]
      },
      {
        phase: 'pre-review',
        label: 'Scope lock',
        by: 'full-output',
        bullets: [
          'Deliverables: 7 pages · 12 sections · 1 form · 1 payment link',
          'All assets and copy locked in /templates/bazi'
        ]
      },
      {
        phase: 'run',
        label: 'Build',
        by: 'framework',
        bullets: [
          'Hero: countdown + bảng can chi scroll reveal',
          'Pricing: 3 tiers but asymmetric weights (not "equal cards")',
          'Forms: VeeValidate + timezone-aware date picker'
        ]
      },
      {
        phase: 'post-review',
        label: 'Quality gates',
        by: 'frontend-review · web-performance-auditor',
        bullets: [
          'Pre-flight: 0 anti-patterns detected',
          'Lighthouse: 100/100 · CLS 0.00 · LCP 1.1s · INP 90ms',
          'Accessibility: WCAG 2.1 AA pass · keyboard nav verified'
        ]
      }
    ]
  },
  {
    id: 'debug-rate-spike',
    category: 'Debug',
    title: 'Debug — Checkout 5xx spike',
    oneLiner: 'Five-step triage on a live incident, with rollback built in.',
    prompt: `Checkout is returning 5xx at p99 starting 14:02 UTC. Walk me through five-step triage: hypothesis, evidence, isolation, fix, verify. Do not change code yet. Provide a rollback plan.`,
    applies: [
      { type: 'rule', id: 'operations', reason: 'Runbook + sev ladder.' },
      { type: 'rule', id: 'observability', reason: 'Three-pillar evidence (metrics, logs, traces).' },
      { type: 'agent', id: 'database-reviewer', reason: 'Suspect slow query / lock contention.' }
    ],
    expectedDelta: 'MTTR −63% vs last incident',
    trace: [
      {
        phase: 'plan',
        label: 'Form hypothesis',
        by: 'operations',
        bullets: [
          'H1: lock contention on payments table after migration ran at 13:58',
          'H2: 3rd-party gateway (SePay) timeout → retry storm',
          'H3: cache stampede on product detail'
        ]
      },
      {
        phase: 'pre-review',
        label: 'Gather evidence',
        by: 'observability',
        bullets: [
          'Metrics: p99 latency 4.2s, error rate 6.1% — correlates with migration timestamp',
          'Logs: 47 statements waiting on Payment.idx_org_created',
          'Traces: all slow spans share the same SQL id'
        ]
      },
      {
        phase: 'run',
        label: 'Isolation',
        by: 'database-reviewer',
        bullets: [
          'New index `idx_org_status_created` added (non-blocking)',
          'CONCURRENTLY used to avoid table lock',
          'Rollback: DROP INDEX CONCURRENTLY (no downtime)'
        ]
      },
      {
        phase: 'post-review',
        label: 'Verify',
        by: 'test-engineer',
        bullets: [
          'p99 latency back to baseline 380ms in 4 minutes',
          'Canary confirmed via 10% traffic ramp',
          'Post-mortem filed in /docs/incidents/2026-07-04-checkout.md'
        ]
      }
    ]
  },
  {
    id: 'ship-rollout',
    category: 'Ship',
    title: 'Ship — Progressive rollout',
    oneLiner: 'Feature-flagged deploy with a one-tap rollback.',
    prompt: `Ship the new billing-engine. Use canary at 5% → 25% → 100% with auto-rollback on p95 > 2s or error rate > 1%. Provide a 1-page incident cheat sheet.`,
    applies: [
      { type: 'rule', id: 'deployment', reason: 'Canary and rollback strategies.' },
      { type: 'rule', id: 'observability', reason: 'SLO triggers for auto-rollback.' },
      { type: 'rule', id: 'vibe-code-protocol', reason: 'Pre/Post gates + retry + fallback.' }
    ],
    expectedDelta: 'Rollouts < 6 min · rollback < 30s',
    trace: [
      {
        phase: 'plan',
        label: 'Rollout plan',
        by: 'deployment',
        bullets: [
          'Stages: 5% (15 min) → 25% (30 min) → 100%',
          'Auto-rollback triggers: p95 > 2s · error > 1%',
          'Manual gate at 25% for product owner approval'
        ]
      },
      {
        phase: 'pre-review',
        label: 'Gate checklist',
        by: 'vibe-code-protocol',
        bullets: [
          'Feature flag `billing-engine-v2` set to 5%',
          'Migration applied in shadow mode for 24h',
          'On-call rotated for the rollout window'
        ]
      },
      {
        phase: 'run',
        label: 'Progressive delivery',
        by: 'workflow-engines · Temporal',
        bullets: [
          '5% stage: p95 612ms · error 0.04% — passed',
          '25% stage: p95 644ms · error 0.07% — passed',
          '100% stage: p95 651ms · error 0.06% — passed'
        ]
      },
      {
        phase: 'deliver',
        label: 'Post-ship',
        by: 'operations',
        bullets: [
          'Cheat sheet printed and pinned to #billing-deploys',
          'Flag kept on for 48h, then considered for removal',
          'Post-launch review scheduled (T+7)'
        ]
      }
    ]
  },
  {
    id: 'build-auto-showroom',
    category: 'Build',
    title: 'Build — Auto Showroom Đa Hãng (Vibe Coding)',
    oneLiner: 'Sàn giao dịch ô tô cao cấp với công cụ tính giá lăn bánh & dự toán trả góp ngân hàng.',
    prompt: `Build an enterprise multi-brand auto showroom website (Porsche, Mercedes, BMW, Audi, Lexus, VinFast). Include:
1. Live inventory filter by vehicle segment, budget, and powertrain (EV/Gas).
2. Interactive on-road cost & monthly loan installment calculator with provincial registration taxes (Hanoi 12%, HCMC 10%).
3. 176-point certified inspection guarantee & Home Test Drive booking form.
4. Dark Slate Luxury Automotive aesthetic (VARIANCE 8, MOTION 6, DENSITY 5). Zero skeleton placeholders, fully functional Vanilla JS.`,
    applies: [
      { type: 'skill', id: 'frontend-taste', reason: 'Thiết kế thẩm mỹ Dark Slate Automotive chống AI slop.' },
      { type: 'skill', id: 'full-output', reason: 'Tạo mã nguồn đầy đủ cả CSS, JS, tính toán số liệu thực tế.' },
      { type: 'rule', id: 'coding-standards', reason: 'Cấu trúc semantic HTML5, không phụ thuộc thư viện ngoài.' }
    ],
    expectedDelta: 'Tính giá lăn bánh chính xác 100% · Lighthouse 99.2/100',
    trace: [
      {
        phase: 'plan',
        label: 'Phân tích & Khởi tạo Cấu Trúc',
        by: 'task-analyzer',
        bullets: [
          'Phân tích 8 mẫu xe đa phân khúc (Sedan, SUV, Thể Thao, Xe Điện)',
          'Thiết lập biểu thuế trước bạ địa phương (Hà Nội 12%, TP.HCM 10%, Tỉnh khác 10%)',
          'Module tính lãi suất vay ngân hàng giảm dần theo thời gian (20%-80%)'
        ]
      },
      {
        phase: 'run',
        label: 'Hiện Thực Mã Nguồn',
        by: 'full-output · frontend-taste',
        bullets: [
          'Tạo giao diện Dark Slate nhám (#090d16) viền vàng kim (#f59e0b)',
          'Tích hợp bộ lọc phân khúc xe tức thời không cần tải lại trang',
          'Xây dựng form đặt lịch lái thử tận nhà có kiểm tra số điện thoại'
        ]
      },
      {
        phase: 'deliver',
        label: 'Kiểm Định & Bàn Giao',
        by: 'frontend-review',
        bullets: [
          'Kiểm tra responsive trên Mobile / Tablet / Desktop',
          'Hoàn thiện template độc lập tại /templates/auto-showroom'
        ]
      }
    ]
  },
  {
    id: 'build-viet-restaurant',
    category: 'Build',
    title: 'Build — Nhà Hàng Ẩm Thực Việt 3 Miền (Vibe Coding)',
    oneLiner: 'Trải nghiệm ẩm thực di sản cơm niêu đất, đặt bàn trực tuyến và hệ thống e-voucher giảm giá.',
    prompt: `Build a Heritage Vietnamese Cuisine restaurant landing page (Vị Xưa Quán). Include:
1. Story of 38-year heirloom clay pot rice and 3-region culinary philosophy.
2. Interactive menu with North, Central, and South cuisine tabs + real dish descriptions.
3. VIP private rooms, ethnic musical performances, and 1-click clipboard voucher system (GIAM15, SUMVAY25).
4. 4 branch directions (Hanoi, Da Nang, Saigon, Phu Quoc) and instant table reservation with allergy/VIP notes.
5. Warm Mahogany & Terracotta aesthetic, Playfair Display typography, anti-slop human-crafted feeling.`,
    applies: [
      { type: 'skill', id: 'frontend-taste', reason: 'Tông màu gỗ mun & đất nung ấm áp Á Đông truyền thống.' },
      { type: 'skill', id: 'full-output', reason: 'Triển khai chi tiết từng món ăn và chức năng đặt bàn.' },
      { type: 'rule', id: 'ui-visual-design', reason: 'Typography Playfair Display cổ điển kết hợp sans-serif thanh lịch.' }
    ],
    expectedDelta: 'Tỉ lệ chuyển đổi đặt bàn +34% · Copy mã voucher 1 chạm',
    trace: [
      {
        phase: 'plan',
        label: 'Khung Thiết Kế Di Sản',
        by: 'frontend-taste',
        bullets: [
          'Vibe: Gỗ mun gụ ấm áp (#180e0a), đỏ đất nung và vàng hoàng cung',
          'Thực đơn 8 món biểu tượng 3 miền (Cá kho tộ, Cơm niêu, Bún chả, Bánh xèo)',
          'Cơ chế mã giảm giá E-Voucher lưu trực tiếp vào clipboard'
        ]
      },
      {
        phase: 'run',
        label: 'Xây Dựng Thành Phần',
        by: 'full-output',
        bullets: [
          'Tab phân loại ẩm thực Bắc - Trung - Nam linh hoạt',
          'Form đặt bàn hỗ trợ chọn chi nhánh, phòng VIP và ngày giờ',
          'Chỉ dẫn 4 chi nhánh chi tiết kèm hotline và hotline đặt tiệc'
        ]
      },
      {
        phase: 'deliver',
        label: 'Hoàn Tất & Tối Ưu',
        by: 'frontend-reviewer',
        bullets: [
          'Không lỗi chính tả dấu tiếng Việt, định dạng tiền tệ đ chuẩn',
          'Template hoàn chỉnh tại /templates/viet-restaurant'
        ]
      }
    ]
  },
  {
    id: 'spec-insurance',
    category: 'Spec',
    title: 'Spec — Bảo Hiểm Toàn Diện 4.0 (FinTech & Health)',
    oneLiner: 'Hệ thống bảo hiểm số với tính phí 30s và bảo lãnh viện phí 680+ bệnh viện.',
    prompt: `Architect a comprehensive 4.0 Insurance platform (Aegis Bảo An). Include:
1. Interactive 30-second premium estimator for Health, Life, Asset, and Corporate coverage.
2. 24h e-Claim compensation workflow with direct guarantee across 680+ hospitals nationwide.
3. Customer testimonials, transparent policy terms, and Step-by-Step Purchase Guide.
4. High-trust Royal Blue & Gold theme, WCAG 2.1 AA accessible, responsive across mobile, tablet, and desktop.`,
    applies: [
      { type: 'rule', id: 'task-analyzer', reason: 'Phân tích phân hệ bảo lãnh và bồi thường trực tuyến.' },
      { type: 'skill', id: 'full-output', reason: 'Tạo trọn vẹn quy trình mua bảo hiểm 4 bước.' },
      { type: 'agent', id: 'security-auditor', reason: 'Bảo mật thông tin hợp đồng bảo hiểm và thanh toán.' }
    ],
    expectedDelta: 'Tính phí bảo hiểm chỉ mất 30s · Tối ưu chuyển đổi e-Claim',
    trace: [
      {
        phase: 'plan',
        label: 'Kiến Trúc Nghiệp Vụ Bảo Hiểm',
        by: 'task-analyzer',
        bullets: [
          'Mô hình 4 gói bảo vệ: Sức Khỏe Vàng, Nhân Thọ Toàn Diện, Doanh Nghiệp & Tài Sản',
          'Hệ thống liên kết 680+ bệnh viện và cơ sở y tế toàn quốc',
          'Quy trình e-Claim giải ngân bồi thường trong 24 giờ'
        ]
      },
      {
        phase: 'run',
        label: 'Hiện Thực Giao Diện & Form',
        by: 'full-output',
        bullets: [
          'Bảng tính phí tương tác tức thì theo độ tuổi và gói quyền lợi',
          'Form nộp hồ sơ bồi thường online bảo mật',
          'Bố cục Navy Blue sang trọng với chứng nhận bảo chứng quốc tế'
        ]
      },
      {
        phase: 'deliver',
        label: 'Kiểm Định & Đóng Gói',
        by: 'security-auditor · frontend-review',
        bullets: [
          'Kiểm tra khả năng tiếp cận WCAG 2.1 AA',
          'Template sẵn sàng chạy tĩnh tại /templates/insurance'
        ]
      }
    ]
  },
  {
    id: 'review-vbs-security',
    category: 'Review',
    title: 'Security — 21-Rule VBS Security Scanner & Auto-Fix',
    oneLiner: 'Quét lỗ hổng bảo mật 21 rule cross-language với phân tích luồng dữ liệu L1-L4 và SCA CVE.',
    prompt: `Run vbsec 21-rule security scan on the repository. Trace data flows from untrusted inputs to sensitive sinks (SQL, eval, child_process, LDAP, SSRF). Scan third-party dependencies for known CVEs via OSV.dev and generate a verifiable SARIF report with atomic remediation diffs.`,
    applies: [
      { type: 'skill', id: 'vbs-scan-security', reason: 'Bộ scanner 21 quy tắc bảo mật chuyên sâu.' },
      { type: 'agent', id: 'security-auditor', reason: 'Thẩm định mức độ nghiêm trọng và giải pháp vá lỗi.' },
      { type: 'rule', id: 'security', reason: 'Chuẩn OWASP Top 10 và CWE baseline.' }
    ],
    expectedDelta: '0 False Negatives trên các lỗi Critical · Vá tự động không làm gãy build',
    trace: [
      {
        phase: 'plan',
        label: 'Định Tuyến & Phân Tích AST',
        by: 'vbs-scan-security',
        bullets: [
          'Quét toàn bộ tệp tin nguồn qua Tree-sitter AST',
          'Xác định các điểm đầu vào không tin cậy (Request Body, Query, Headers)',
          'Kiểm tra các sinks nhạy cảm (Dapper raw queries, exec commands)'
        ]
      },
      {
        phase: 'run',
        label: 'Phân Tích Dòng Dữ Liệu (Taint Analysis)',
        by: 'security-auditor',
        bullets: [
          'Kiểm tra cơ chế sanitization / parameterized queries',
          'Quét lỗ hổng phụ thuộc bên thứ 3 qua OSV.dev API',
          'Tạo bản vá đề xuất (diff) cho từng phát hiện'
        ]
      },
      {
        phase: 'deliver',
        label: 'Xuất Báo Cáo & SARIF',
        by: 'vbs-scan-security',
        bullets: [
          'Xuất file audit-report.sarif tích hợp GitHub CodeQL',
          'Xác nhận 0 lỗ hổng nghiêm trọng tồn đọng'
        ]
      }
    ]
  },
  {
    id: 'debug-rea-binary',
    category: 'Debug',
    title: 'REA — Reverse Engineer Anything & Cleanroom Rebuild',
    oneLiner: 'Dịch ngược và phân tích mã nguồn nhị phân PE/ELF/.NET/APK/WASM với bằng chứng xác thực.',
    prompt: `Inspect the target binary with REA (Reverse Engineer Anything). Extract symbols, ASTs, and network protocol signatures. Generate cleanroom interface definitions, sequence diagrams, and safe drop-in replacement modules without violating evidence bounds.`,
    applies: [
      { type: 'skill', id: 'reverse-engineer-anything', reason: 'Universal reverse engineering CLI & MCP server.' },
      { type: 'agent', id: 'fullstack-engineer', reason: 'Tái tạo mã nguồn sạch (Cleanroom Reconstruction).' },
      { type: 'rule', id: 'karpathy-guidelines', reason: 'Tôn trọng bằng chứng thực tế, không võ đoán.' }
    ],
    expectedDelta: 'Tái cấu trúc 100% API contract · Không vi phạm bản quyền logic',
    trace: [
      {
        phase: 'plan',
        label: 'Thu Thập Bằng Chứng Nhị Phân',
        by: 'reverse-engineer-anything',
        bullets: [
          'Trích xuất PE/ELF headers, import/export tables và chuỗi nhị phân',
          'Xác định cấu trúc dữ liệu IPC và endpoints mạng',
          'Đánh dấu ranh giới bằng chứng (Evidence Bounds)'
        ]
      },
      {
        phase: 'run',
        label: 'Phân Tích AST & Control Flow',
        by: 'reverse-engineer-anything',
        bullets: [
          'Khôi phục sơ đồ trạng thái (State Diagram) và API signature',
          'Viết tài liệu đặc tả chức năng độc lập (Cleanroom Spec)'
        ]
      },
      {
        phase: 'deliver',
        label: 'Hiện Thực Lại Mã Nguồn Sạch',
        by: 'fullstack-engineer',
        bullets: [
          'Tạo mã nguồn TypeScript / C# sạch thay thế hoàn toàn',
          'Bộ kiểm thử tự động xác minh tính tương thích 1:1'
        ]
      }
    ]
  },
  {
    id: 'prompt-ui-ux',
    category: 'Build',
    title: 'UI/UX — Evondev Design System & Ma Trận 5 Trạng Thái',
    oneLiner: 'Tạo hệ thống Design Tokens HSL, lưới 8px, ma trận nút bấm 5 trạng thái và kiểm định tương phản WCAG AA 4.5:1.',
    slashCommand: '/ui-ux',
    tags: ['Design System', 'Tokens', 'WCAG AA', 'Figma to Code', 'Evondev'],
    prompt: `/ui-ux Tạo Design System chuẩn doanh nghiệp cho giao diện SaaS:
1. Thiết lập bảng màu Tokens HSL có tính toán: Primary: hsl(210, 85%, 55%), Surface: #0f172a, Text: #f8fafc, Border: #334155.
2. Lưới khoảng cách 8px grid (8px, 16px, 24px, 32px, 48px), bán kính bo góc 10px.
3. Dựng ma trận component Nút bấm & Input đầy đủ 5 trạng thái: Default, Hover, Active, Disabled, Loading/Spinner.
4. Kiểm tra tương phản màu WCAG 2.1 AA tối thiểu 4.5:1 cho văn bản thường và 3:1 cho thành phần UI.`,
    applies: [
      { type: 'skill', id: 'frontend-taste', reason: 'Quy chuẩn thẩm mỹ chuyên nghiệp, chống AI slop.' },
      { type: 'skill', id: 'frontend-review', reason: 'Dual-gate kiểm định tương phản WCAG AA.' },
      { type: 'rule', id: 'karpathy-guidelines', reason: 'Tối giản mã nguồn, cấu trúc token trực quan.' },
      { type: 'rule', id: 'coding-standards', reason: 'Semantic CSS variables, không phụ thuộc thư viện nặng.' }
    ],
    expectedDelta: '100% WCAG AA · 0 Trạng thái thiếu · Tokens tái sử dụng 100%',
    trace: [
      {
        phase: 'plan',
        label: 'Khởi Tạo Bản Đồ Token & Lưới Khoảng Cách',
        by: 'ui-visual-design',
        bullets: [
          'Khai báo CSS custom properties cho thang HSL, typography clamp(), và spacing',
          'Thiết lập layout grid 8-point và quy tắc phân cấp thị giác (Visual Hierarchy)',
          'Khảo sát bảng màu tương phản dark mode & light mode'
        ]
      },
      {
        phase: 'pre-review',
        label: 'Cổng Thẩm Định Khả Năng Tiếp Cận (WCAG)',
        by: 'frontend-review',
        bullets: [
          'Kiểm tra tỉ lệ tương phản màu text/background đạt 4.8:1 (vượt chuẩn AA 4.5:1)',
          'Đảm bảo mọi phần tử tương tác có chỉ báo focus-visible rõ ràng',
          'Quy định touch target tối thiểu 44x44px trên thiết bị di động'
        ]
      },
      {
        phase: 'run',
        label: 'Hiện Thực Ma Trận 5-State Component',
        by: 'full-output',
        bullets: [
          'Xây dựng Button component với đủ 5 states: default, hover, active, disabled, loading (SVG spinner)',
          'Xây dựng Input text field có floating label, error state và helper text',
          'Tích hợp hiệu ứng micro-interaction (scale 0.98 khi active, transition cubic-bezier)'
        ]
      },
      {
        phase: 'post-review',
        label: 'Kiểm Thử Đa Trình Duyệt & Responsive',
        by: 'frontend-review',
        bullets: [
          'Thử nghiệm trên 3 kích thước: Mobile (375px), Tablet (768px), Desktop (1440px)',
          'Xác nhận không phát sinh layout shift hoặc vỡ typography',
          'Kiểm tra tính năng chuyển đổi giao diện sáng/tối không làm đứt kết nối biến màu'
        ]
      },
      {
        phase: 'deliver',
        label: 'Bàn Giao & Hướng Dẫn Sử Dụng',
        by: 'workflow-engines',
        bullets: [
          'Xuất file token tokens.css và demo live tại /templates/ui-ux',
          'Tài liệu hóa quy tắc mở rộng component cho toàn bộ nhóm phát triển'
        ]
      }
    ]
  },
  {
    id: 'prompt-dashboard-ui',
    category: 'Build',
    title: 'Dashboard UI — Executive Cockpit, Real-time KPIs & Mini Kanban',
    oneLiner: 'Xây dựng bảng điều khiển quản trị doanh nghiệp: 4 thẻ KPI động kèm biểu đồ SVG sparkline, bảng dữ liệu lọc đa tiêu chí và Kanban mini.',
    slashCommand: '/dashboard-ui',
    tags: ['Dashboard', 'KPI', 'Analytics', 'Kanban', 'Data Table'],
    prompt: `/dashboard-ui Xây dựng giao diện Executive Analytics Cockpit gồm:
1. 4 thẻ KPI động (Doanh thu tháng, Khách hàng hoạt động, Tỉ lệ chuyển đổi, ARR) tích hợp biểu đồ đường SVG mini sắc nét.
2. Bảng dữ liệu khách hàng với thanh tìm kiếm thời gian thực, bộ lọc trạng thái đa tiêu chí, phân trang và huy hiệu màu ngữ nghĩa.
3. Bảng Sprint Kanban 3 cột (Cần làm, Đang xử lý, Đã hoàn thành) có chỉ báo tiến độ phần trăm trực quan.
4. Tối ưu thời gian tải < 0.8s, không phụ thuộc thư viện chart nặng nề (thuần SVG nhẹ < 5KB).`,
    applies: [
      { type: 'skill', id: 'frontend-taste', reason: 'Bố cục Cockpit tinh tế phong cách Vercel / Linear.' },
      { type: 'skill', id: 'full-output', reason: 'Tạo mã nguồn đầy đủ HTML, CSS, JS tính toán số liệu thực.' },
      { type: 'rule', id: 'architecture-patterns', reason: 'Tổ chức component dạng Widget độc lập, dễ mở rộng.' },
      { type: 'skill', id: 'frontend-review', reason: 'Đảm bảo CLS = 0 khi render bảng dữ liệu.' }
    ],
    expectedDelta: 'Tải tức thì < 0.8s · 0 Layout Shift · Thuần SVG nhẹ < 5KB',
    trace: [
      {
        phase: 'plan',
        label: 'Thiết Kế Cấu Trúc Bố Cục Cockpit',
        by: 'dashboard-ui',
        bullets: [
          'Phân vùng layout: Header điều hành, 4 thẻ KPI tóm tắt, Grid chính chứa Biểu đồ + Bảng dữ liệu + Kanban',
          'Lựa chọn bảng màu hiển thị dữ liệu tài chính (Xanh lá dương, Đỏ cảnh báo, Xanh cyan xu hướng)'
        ]
      },
      {
        phase: 'pre-review',
        label: 'Định Dạng Dữ Liệu & Thước Đo Hiệu Năng',
        by: 'karpathy-guidelines',
        bullets: [
          'Định dạng tiền tệ chuẩn VND / USD và hiển thị tỉ lệ phần trăm tăng trưởng (+18.4%)',
          'Cam kết không dùng thư viện Chart.js cồng kềnh, dùng SVG native render mượt mà'
        ]
      },
      {
        phase: 'run',
        label: 'Lập Trình Widget Dữ Liệu Thực Tế',
        by: 'full-output',
        bullets: [
          'Vẽ biểu đồ sparkline SVG dynamic với gradient fill và điểm cực trị',
          'Dựng Data Table hỗ trợ sắp xếp theo cột và lọc khách hàng realtime',
          'Triển khai Mini Kanban dạng thẻ kéo thả với thanh tiến độ hoàn thành'
        ]
      },
      {
        phase: 'post-review',
        label: 'Kiểm Thử Mật Độ Thông Tin (Information Density)',
        by: 'frontend-review',
        bullets: [
          'Đảm bảo người quản trị đọc hiểu toàn bộ tình hình kinh doanh chỉ trong 5 giây đầu',
          'Xác nhận bảng cuộn mượt mà không giật lag trên màn hình di động 360px'
        ]
      },
      {
        phase: 'deliver',
        label: 'Đóng Gói & Xuất Bản Mẫu Trực Quan',
        by: 'workflow-engines',
        bullets: [
          'Template hoàn chỉnh sẵn sàng trải nghiệm tại /templates/dashboard-ui',
          'Mã nguồn sạch, có comment giải thích rõ ràng từng dòng tính toán'
        ]
      }
    ]
  },
  {
    id: 'prompt-frontend-taste',
    category: 'Review',
    title: 'Frontend Taste — 57 Hallmark Anti-Slop Gates & Craft Dials',
    oneLiner: 'Quét và loại bỏ triệt để 57 bẫy AI-slop (glow tím lòe loẹt, 3 cột sao chép). Tinh chỉnh 3 dial: Variance, Motion, Density.',
    slashCommand: '/frontend-taste',
    tags: ['Anti-Slop', 'Taste', 'Hallmark', 'Bento Grid', 'Micro-Interactions'],
    prompt: `/frontend-taste Quét và tái cấu trúc giao diện theo chuẩn 57 Hallmark Anti-Slop Gates:
1. Triệt tiêu hoàn toàn hiệu ứng purple gradient blur vô nghĩa và typography font sao chép thô sơ.
2. Phá vỡ bố cục 3 cột đối xứng nhàm chán bằng cấu trúc Bento Grid bất đối xứng giàu tính nhịp điệu.
3. Thiết lập 3 thanh trượt điều hướng Craft Dials: Variance 75% (độ đa dạng layout), Motion Gentle 300ms (chuyển động tinh tế), Density Compact (mật độ thông tin cao phong cách Linear / Stripe).
4. Bổ sung các chi tiết thủ công: subtle border 1px mờ, font mono cho số liệu và badge trạng thái tinh gọn.`,
    applies: [
      { type: 'skill', id: 'frontend-taste', reason: 'Bộ quy chuẩn thẩm mỹ hàng đầu chống giao diện generic AI.' },
      { type: 'skill', id: 'frontend-redesign', reason: 'Tái thiết kế layout theo tư duy thiết kế đương đại.' },
      { type: 'skill', id: 'frontend-review', reason: 'Thực thi kiểm tra 57 gates nghiêm ngặt.' },
      { type: 'rule', id: 'karpathy-guidelines', reason: 'Tối giản hiệu ứng thừa, tôn vinh nội dung thực tế.' }
    ],
    expectedDelta: '57/57 Cổng Hallmark Đạt Chuẩn · Cảm giác thủ công đẳng cấp',
    trace: [
      {
        phase: 'plan',
        label: 'Quét 57 Bẫy Thẩm Mỹ AI (Slop Audit)',
        by: 'frontend-taste',
        bullets: [
          'Phát hiện và đánh dấu các thẻ purple glow không phục vụ mục đích ngữ nghĩa',
          'Nhận diện các khối văn bản Lorem Ipsum sáo rỗng cần thay thế bằng nội dung thực',
          'Phân tích sự đơn điệu trong cấu trúc lưới giao diện'
        ]
      },
      {
        phase: 'pre-review',
        label: 'Căn Chỉnh 3 Craft Dials Cơ Bản',
        by: 'frontend-taste',
        bullets: [
          'Cài đặt Variance = 75%: Thay 3 thẻ kích thước bằng nhau bằng 1 hero Bento card + 2 thẻ bổ trợ',
          'Cài đặt Motion = 300ms cubic-bezier: Chuyển động nhẹ nhàng, không gây mỏi mắt người dùng',
          'Cài đặt Density = Compact: Giảm khoảng trắng vô lý, tăng lượng thông tin hữu ích trên màn hình đầu tiên'
        ]
      },
      {
        phase: 'run',
        label: 'Tái Cấu Trúc Toàn Diện Layout & Typography',
        by: 'frontend-redesign',
        bullets: [
          'Tạo Asymmetric Bento Grid với hiệu ứng viền 1px mờ cao cấp',
          'Thay thế phông chữ mặc định bằng tổ hợp Typography có cá tính',
          'Thêm hiệu ứng hover card mượt mà với ánh sáng spotlight định hướng chuột'
        ]
      },
      {
        phase: 'post-review',
        label: 'Xác Thực 57 Cổng Kiểm Tra Sau Tinh Chỉnh',
        by: 'frontend-review',
        bullets: [
          '0/57 lỗi AI-slop tồn dư (Đạt chứng nhận Craft Standard)',
          'Độ phản hồi của giao diện trên mobile đạt 60fps mượt mà'
        ]
      },
      {
        phase: 'deliver',
        label: 'Xuất Bản Mẫu Trực Quan Đẳng Cấp',
        by: 'workflow-engines',
        bullets: [
          'Template trực quan sống động tại /templates/frontend-taste',
          'Kèm bảng điều khiển tương tác 3 dial cho phép người dùng tự kéo thử nghiệm'
        ]
      }
    ]
  },
  {
    id: 'prompt-cms-landing-enterprise',
    category: 'Build',
    title: 'CMS Enterprise v4 — CRM Pipeline, Ví Điểm & Affiliate F0-F3',
    oneLiner: 'Khởi tạo hệ thống quản trị SaaS toàn diện: CRM pipeline 4 cột, ví điểm nạp/rút giả lập, mạng lưới hoa hồng 4 cấp F0-F3 và Webhook SePay/VietQR.',
    slashCommand: '/cms-landing-enterprise',
    tags: ['CMS', 'CRM', 'SaaS', 'Affiliate', 'Wallet', 'VietQR'],
    prompt: `/cms-landing-enterprise Dựng kiến trúc và giao diện hệ thống SaaS Portal Enterprise v4:
1. Phân hệ CRM quản lý Khách hàng tiềm năng dạng Kanban 4 cột (Mới, Đã liên hệ, Đàm phán, Chốt hợp đồng) với tổng giá trị deal.
2. Ví điểm thưởng (Points Wallet) tích hợp mã QR nạp tiền và bộ mô phỏng lệnh rút tiền tức thì (Instant Withdrawal).
3. Mạng lưới tiếp thị liên kết (Affiliate Tree) 4 tầng (F0: 20%, F1: 8%, F2: 4%, F3: 2%) tính toán hoa hồng thời gian thực.
4. Module tiếp nhận Webhook thanh toán SePay / VietQR đảm bảo Idempotency (khóa trùng lặp) và ghi sổ kế toán kép an toàn.`,
    applies: [
      { type: 'rule', id: 'rule_fullstack-development', reason: 'Kiến trúc Fullstack ASP.NET Core Web API + React TSX.' },
      { type: 'rule', id: 'security', reason: 'Bảo mật Webhook HMAC-SHA256 và khóa Idempotency.' },
      { type: 'rule', id: 'enterprise-patterns', reason: 'Mô hình Clean Architecture và Domain-Driven Design.' },
      { type: 'skill', id: 'full-output', reason: 'Tạo mã nguồn trọn vẹn không để sót skeleton hay TODO.' }
    ],
    expectedDelta: 'Full Stack SaaS Sẵn Sàng · Tính toán hoa hồng và đối soát chuẩn xác 100%',
    trace: [
      {
        phase: 'plan',
        label: 'Thiết Kế Thực Thể Cơ Sở Dữ Liệu & Hợp Đồng API',
        by: 'enterprise-patterns',
        bullets: [
          'Mô hình hóa bảng Leads, Transactions, Wallets, AffiliateNodes, WebhookLogs',
          'Xây dựng luồng giao dịch tài chính đảm bảo ACID và không mất tiền',
          'Định nghĩa cấu trúc Webhook payload của SePay và PayOS'
        ]
      },
      {
        phase: 'pre-review',
        label: 'Thẩm Tra Bảo Mật Giao Dịch & Tránh Race Condition',
        by: 'security',
        bullets: [
          'Cơ chế phân tán Redis Lock cho thao tác rút điểm khỏi ví',
          'Xác minh chữ ký điện tử HMAC trước khi kích hoạt cộng điểm vào tài khoản',
          'Chặn đứng lỗi gian lận phân cấp hoa hồng lặp vòng'
        ]
      },
      {
        phase: 'run',
        label: 'Triển Khai Giao Diện & Logic Nghiệp Vụ',
        by: 'rule_fullstack-development',
        bullets: [
          'Dựng Kanban Board quản lý Leads CRM với thao tác chuyển cột mượt mà',
          'Xây dựng Widget Ví Điểm: nạp tiền qua QR, lịch sử biến động số dư và lệnh rút tiền',
          'Vẽ sơ đồ cây Affiliate 4 tầng hiển thị trực quan tỷ lệ % hoa hồng và số lượng thành viên'
        ]
      },
      {
        phase: 'post-review',
        label: 'Kiểm Thử Đối Soát Tài Chính & Webhook Giả Lập',
        by: 'frontend-review',
        bullets: [
          'Giả lập gửi 100 request Webhook đồng thời: 100% xử lý thành công đúng 1 lần (Idempotent)',
          'Kiểm tra tính toán hoa hồng phân bổ cho F0, F1, F2, F3 khớp số lẻ đến từng đồng'
        ]
      },
      {
        phase: 'deliver',
        label: 'Bàn Giao Trọn Bộ Mẫu Chạy Trực Tiếp',
        by: 'workflow-engines',
        bullets: [
          'Mẫu chạy thực tế tại /templates/cms-landing-enterprise',
          'Trang CMS Dashboard hoàn chỉnh tại /cms với đầy đủ số liệu'
        ]
      }
    ]
  },
  {
    id: 'prompt-image-workflow',
    category: 'Build',
    title: 'Image Workflow — Studio AI Visuals, Đa Tỉ Lệ & Asset Manifest',
    oneLiner: 'Quy trình 4 pha sáng tạo hình ảnh thương phẩm: Prompt Blueprint, Negative Prompt, tỉ lệ 16:9 / 1:1 / 9:16 và Asset Manifest JSON.',
    slashCommand: '/image-workflow',
    tags: ['Image Studio', 'Midjourney', 'Stable Diffusion', 'Asset Manifest', 'Design Pipeline'],
    prompt: `/image-workflow Thiết lập quy trình tạo hình ảnh nhận diện thương hiệu chuẩn studio:
1. Cấu trúc Prompt Blueprint với thông số quang học máy ảnh (Hasselblad 80mm f/2.8, ánh sáng khuếch tán softbox 4200K, độ sâu trường ảnh mỏng).
2. Bộ Negative Prompt chuyên sâu loại bỏ dị tật ngón tay, mắt lệch, chữ rác và hiện tượng viền nhựa AI.
3. Bố cục đa khung hình cho cùng một concept hình ảnh (16:9 Banner máy tính, 1:1 Thẻ tính năng, 9:16 Story di động).
4. Xuất tệp Asset Manifest JSON theo dõi kích thước, định dạng WebP, alt text SEO và hash chống trùng lặp.`,
    applies: [
      { type: 'skill', id: 'frontend-taste', reason: 'Tư duy hình ảnh điện ảnh thực tế, chống dị tật AI.' },
      { type: 'skill', id: 'full-output', reason: 'Tạo đủ prompt, negative prompt, CSS responsive và manifest.' },
      { type: 'rule', id: 'coding-standards', reason: 'Cấu trúc thư mục tài nguyên và chuẩn định dạng WebP/AVIF tối ưu.' },
      { type: 'skill', id: 'frontend-review', reason: 'Kiểm tra độ nét và kích thước file tải nhanh.' }
    ],
    expectedDelta: 'Hình ảnh chân thực sắc nét · Tương thích hoàn hảo mọi thiết bị · Không biến dạng',
    trace: [
      {
        phase: 'plan',
        label: 'Thiết Lập Phong Cách Thị Giác & Quang Học',
        by: 'frontend-taste',
        bullets: [
          'Xác định Moodboard: Tối giản hiện đại, ánh sáng tự nhiên mềm mại, tông màu trung tính',
          'Quy định thông số máy ảnh quang học thay vì từ khóa sáo rỗng "photorealistic 8k"',
          'Phân bổ 3 tỉ lệ khung hình cho các vị trí hiển thị trên website'
        ]
      },
      {
        phase: 'pre-review',
        label: 'Xây Dựng Bộ Negative Prompt Chống Dị Tật',
        by: 'karpathy-guidelines',
        bullets: [
          'Chặn các lỗi: biến dạng bàn tay (extra fingers), mắt không đối xứng, viền ánh sáng nhựa',
          'Loại bỏ các văn bản rác vô nghĩa tự sinh trên ảnh (gibberish text, watermarks)'
        ]
      },
      {
        phase: 'run',
        label: 'Sinh Bộ Prompt Blueprint & Asset Manifest',
        by: 'full-output',
        bullets: [
          'Viết Prompt Blueprint chi tiết cho từng tỉ lệ 16:9 (Hero), 1:1 (Feature Cards), 9:16 (Mobile Banner)',
          'Tạo tệp asset-manifest.json lưu trữ metadata, kích thước tối ưu và thuộc tính SEO alt text'
        ]
      },
      {
        phase: 'post-review',
        label: 'Kiểm Thử Responsive & Tải Nhanh',
        by: 'frontend-review',
        bullets: [
          'Áp dụng thẻ <picture> với srcset đa độ phân giải (1x, 2x Retina)',
          'Đảm bảo định dạng WebP / AVIF giúp giảm 70% dung lượng mà không vỡ hình'
        ]
      },
      {
        phase: 'deliver',
        label: 'Bàn Giao Studio Trực Quan',
        by: 'workflow-engines',
        bullets: [
          'Template tương tác Studio Visuals tại /templates/image-workflow',
          'Tích hợp nút sao chép prompt và chuyển đổi nhanh tỉ lệ khung hình'
        ]
      }
    ]
  },
  {
    id: 'prompt-vietqr-payment',
    category: 'Build',
    title: 'VietQR & SePay — Cổng Thanh Toán Tự Động & Idempotent Webhook',
    oneLiner: 'Tự động tạo mã QR VietQR động theo đơn hàng, bắt Webhook SePay/PayOS với xác thực HMAC và khóa idempotency Redis.',
    slashCommand: '/payment',
    tags: ['Payment', 'VietQR', 'SePay', 'PayOS', 'Webhook', 'Fintech'],
    prompt: `/payment Xây dựng cổng thanh toán VietQR và SePay tự động:
1. Sinh mã QR theo chuẩn Napas247 chứa số tài khoản, mã ngân hàng, số tiền và mã nội dung chuyển khoản duy nhất.
2. Endpoint nhận Webhook bảo mật với xác thực Secret Token và kiểm tra khóa idempotency trong Redis tránh xử lý tiền trùng lặp.
3. Giao diện đồng hồ đếm ngược 15 phút, hướng dẫn chuyển khoản và tự động kiểm tra trạng thái thanh toán theo thời gian thực (Polling / WebSocket).
4. Tự động cập nhật số dư ví hoặc kích hoạt đơn hàng ngay khi tiền vào tài khoản.`,
    applies: [
      { type: 'rule', id: 'security', reason: 'Bảo mật giao dịch thanh toán và xác thực chữ ký Webhook.' },
      { type: 'rule', id: 'rule_fullstack-development', reason: 'Tích hợp end-to-end Backend API và Frontend UI.' },
      { type: 'rule', id: 'api-patterns', reason: 'Thiết kế RESTful webhook receiver chuẩn idempotency.' },
      { type: 'skill', id: 'full-output', reason: 'Triển khai toàn bộ luồng thanh toán, không thiếu sót xử lý lỗi.' }
    ],
    expectedDelta: 'Xác nhận thanh toán < 3s · 0 rủi ro trùng lặp · Trải nghiệm khách hàng 10/10',
    trace: [
      {
        phase: 'plan',
        label: 'Xây Dựng Kiến Trúc Giao Dịch & Mã Hóa Napas',
        by: 'api-patterns',
        bullets: [
          'Tạo định dạng nội dung chuyển khoản: PREFIX + ORDER_ID (Ví dụ: SAAS1082)',
          'Thiết lập schema lưu trữ lịch sử giao dịch và trạng thái đơn hàng (PENDING, PAID, EXPIRED)'
        ]
      },
      {
        phase: 'pre-review',
        label: 'Thẩm Định Cơ Chế Phòng Chống Gian Lận (Anti-Fraud)',
        by: 'security',
        bullets: [
          'Kiểm tra giá trị tiền thực nhận trùng khớp chính xác với số tiền đơn hàng',
          'Thiết lập Rate Limiting và Whitelist IP cho máy chủ Webhook'
        ]
      },
      {
        phase: 'run',
        label: 'Hiện Thực Giao Diện Thanh Toán & Webhook Handler',
        by: 'rule_fullstack-development',
        bullets: [
          'Tạo giao diện hiển thị mã QR VietQR chất lượng cao kèm nút sao chép nhanh số tài khoản',
          'Triển khai Webhook Controller xác thực token, kiểm tra Redis Idempotency Key trong 24h',
          'Cập nhật giao diện tự động chúc mừng khi nhận được tín hiệu tiền vào tài khoản'
        ]
      },
      {
        phase: 'post-review',
        label: 'Kiểm Thử Chịu Tải & Tình Huống Ngoại Lệ',
        by: 'frontend-review',
        bullets: [
          'Xử lý tình huống chuyển thiếu tiền, chuyển thừa tiền hoặc đơn hàng hết hạn 15 phút',
          'Đảm bảo giao diện thông báo rõ ràng cho người dùng cách xử lý sự cố'
        ]
      },
      {
        phase: 'deliver',
        label: 'Đóng Gói & Tích Hợp Vào Hệ Thống CMS',
        by: 'workflow-engines',
        bullets: [
          'Tích hợp liền mạch vào module Ví Điểm của CMS Landing Enterprise v4',
          'Hướng dẫn kết nối tài khoản ngân hàng thực tế qua SePay.vn hoặc PayOS'
        ]
      }
    ]
  },
  {
    id: 'prompt-seo-cwv',
    category: 'Ship',
    title: 'SEO & Core Web Vitals — Điểm 100/100, Schema.org & Meta Tags',
    oneLiner: 'Tối ưu hiệu năng đỉnh cao: LCP < 1.2s, INP < 50ms, CLS 0, sinh thẻ OpenGraph mạng xã hội và cấu trúc JSON-LD chuẩn Google.',
    slashCommand: '/seo-perf',
    tags: ['SEO', 'Performance', 'Core Web Vitals', 'OpenGraph', 'Schema.org'],
    prompt: `/seo-perf Kiểm định và tối ưu toàn diện hiệu năng và SEO trang web:
1. Tối ưu Core Web Vitals: LCP < 1.2s (preload critical hero fonts/images), INP < 50ms (loại bỏ long tasks trên main thread), CLS = 0 (khai báo kích thước width/height cố định cho mọi hình ảnh).
2. Thiết lập bộ thẻ Meta đầy đủ: OpenGraph, Twitter Cards, Canonical URL, Favicon đa thiết bị và Theme-Color.
3. Nhúng cấu trúc dữ liệu Schema.org JSON-LD cho Organization, SoftwareApplication và FAQPage để tối ưu hiển thị Rich Snippets trên Google.
4. Tự động sinh sitemap.xml và robots.txt chuẩn quy chuẩn tìm kiếm.`,
    applies: [
      { type: 'rule', id: 'performance', reason: 'Kỹ thuật tối ưu render path, giảm bundle size và asset preload.' },
      { type: 'rule', id: 'deployment', reason: 'Cấu hình HTTP cache headers (Cache-Control max-age=31536000, immutable).' },
      { type: 'skill', id: 'frontend-review', reason: 'Đo lường kiểm định chỉ số Lighthouse trực quan.' },
      { type: 'rule', id: 'observability', reason: 'Tích hợp Web Vitals tracking gửi về analytics.' }
    ],
    expectedDelta: 'Lighthouse 98-100 · Tối ưu hiển thị mạng xã hội · Tăng tốc lập chỉ mục Google',
    trace: [
      {
        phase: 'plan',
        label: 'Phân Tích Đường Dẫn Hiển Thị Trọng Yếu (Critical Rendering Path)',
        by: 'performance',
        bullets: [
          'Đo lường các điểm nghẽn tài nguyên chặn render (Render-blocking resources)',
          'Lập danh sách các thẻ meta và structured data cần thiết cho từng trang'
        ]
      },
      {
        phase: 'pre-review',
        label: 'Kiểm Định Chỉ Số Hiệu Năng Mục Tiêu',
        by: 'karpathy-guidelines',
        bullets: [
          'Mục tiêu: LCP <= 1.2s, FID/INP <= 50ms, CLS == 0.000',
          'Đảm bảo không đưa thêm script theo dõi bên thứ ba làm nghẽn luồng xử lý chính'
        ]
      },
      {
        phase: 'run',
        label: 'Tối Ưu Mã Nguồn & Nhúng Cấu Trúc SEO',
        by: 'full-output',
        bullets: [
          'Thêm link rel="preload" cho font woff2 và ảnh Hero chính',
          'Tích hợp đoạn mã JSON-LD Schema.org chi tiết về doanh nghiệp và phần mềm',
          'Thiết lập thẻ meta OpenGraph xem trước bắt mắt khi chia sẻ qua Zalo, Facebook, Telegram'
        ]
      },
      {
        phase: 'post-review',
        label: 'Chạy Thử Nghiệm Google Rich Results & Lighthouse',
        by: 'frontend-review',
        bullets: [
          'Kiểm tra Rich Results Test: 0 lỗi cảnh báo cú pháp JSON-LD',
          'Lighthouse kiểm định đạt 99 Performance, 100 Accessibility, 100 Best Practices, 100 SEO'
        ]
      },
      {
        phase: 'deliver',
        label: 'Xuất Bản Cấu Hình & Bàn Giao',
        by: 'workflow-engines',
        bullets: [
          'Tệp sitemap.xml và robots.txt sẵn sàng deploy',
          'Checklist duy trì thứ hạng SEO cho các lần cập nhật nội dung tiếp theo'
        ]
      }
    ]
  }
]
