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
  }
]
