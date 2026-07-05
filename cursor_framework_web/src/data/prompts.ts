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
  }
]
