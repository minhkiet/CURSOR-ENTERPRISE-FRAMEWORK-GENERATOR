/**
 * Framework catalog — single source of truth for the /learn and /prompts pages.
 * Mirrors the actual `.cursor/rules`, `.cursor/skills`, and `.cursor/agents` folders.
 * Content is curated from the framework front-matter + opening sections so it can
 * be displayed quickly without re-reading 100+ files at runtime.
 */

export type FrameworkItemType = 'rule' | 'skill' | 'agent'

export interface FrameworkItem {
  id: string
  type: FrameworkItemType
  name: string
  title: string // short human title (used as card heading)
  subtitle: string // one-line tagline
  description: string // 2–4 sentence summary
  category: string // grouping column shown in tabs/filters
  tags: string[]
  role?: 'primary' | 'secondary' | 'mandatory' | 'overlay'
  trigger?: string // slash command or invoker
  path: string // where it lives in the repo
  gates?: string[] // pre/post gate names
  bullets?: string[] // 3–5 key points / pillars
  metrics?: { label: string; value: string }[]
  alignsWith?: string[] // rule/file references
}

// ────────────────────────────────────────────────────────────────────────────
// RULES — `.cursor/rules/*.mdc`
// ────────────────────────────────────────────────────────────────────────────

export const RULES: FrameworkItem[] = [
  {
    id: 'karpathy-guidelines',
    type: 'rule',
    name: 'karpathy-guidelines',
    title: 'Karpathy Guidelines',
    subtitle: 'Behavioral overlay for every coding task',
    description:
      'Always-applied rule that injects the four Karpathy pillars (think before coding, simplicity, surgical changes, goal-driven execution) into every assistant turn. Bias toward caution over speed.',
    category: 'Foundations',
    tags: ['always-applied', 'coding-discipline', 'overlays'],
    path: '.cursor/rules/rule_karpathy-guidelines.mdc',
    bullets: [
      'Think Before Coding — surface tradeoffs, ask when unclear',
      'Simplicity First — minimum code that solves the problem',
      'Surgical Changes — touch only what the request requires',
      'Goal-Driven — define verification criteria up front'
    ]
  },
  {
    id: 'coding-standards',
    type: 'rule',
    name: 'coding-standards',
    title: 'Coding Standards',
    subtitle: 'Uniform code style across the framework',
    description:
      'Project-wide conventions on naming, comments, error handling, async patterns, and file layout. The baseline every other rule references.',
    category: 'Foundations',
    tags: ['style', 'conventions', 'cross-cutting'],
    path: '.cursor/rules/rule_coding-standards.mdc'
  },
  {
    id: 'intent-detection',
    type: 'rule',
    name: 'intent-detection',
    title: 'Intent Detection',
    subtitle: 'Skill auto-discovery + clarification flow',
    description:
      'Identifies the user intent, auto-loads relevant skills/rules, and triggers clarification when the request is ambiguous. Combines with the translation layer for multi-language input.',
    category: 'Routing',
    tags: ['router', 'multi-language', 'clarification'],
    path: '.cursor/rules/proto_intent-detection.mdc'
  },
  {
    id: 'context-router',
    type: 'rule',
    name: 'context-router',
    title: 'Context Router',
    subtitle: 'Smart routing to the right handler',
    description:
      'Forwards only the domain knowledge needed for a task — backend work loads backend rules, frontend work loads frontend rules. Cuts context by up to 40%.',
    category: 'Routing',
    tags: ['token-optimization', 'router'],
    path: '.cursor/rules/proto_context-router.mdc',
    bullets: ['Reduces token usage by ~40%', 'Pulls only relevant domain MDCs', 'Pairs with memory-first to skip already-decided topics']
  },
  {
    id: 'memory-first',
    type: 'rule',
    name: 'memory-first',
    title: 'Memory First',
    subtitle: 'Decision and incident memory before queries',
    description:
      'Checks the local SQLite memory store (ADRs, bug fixes, prior decisions) before doing any other lookup. Avoids relitigating settled questions.',
    category: 'Routing',
    tags: ['memory', 'knowledge'],
    path: '.cursor/rules/proto_memory-first.mdc'
  },
  {
    id: 'task-analyzer',
    type: 'rule',
    name: 'task-analyzer',
    title: 'Task Analyzer',
    subtitle: 'Auto-detect rules/skills + emit task manifest',
    description:
      'Splits incoming requests into a structured task manifest with subtasks, owners, and verification steps. Feeds multi-language-vibe-code and the skill registry.',
    category: 'Routing',
    tags: ['planning', 'manifest', 'auto-discovery'],
    path: '.cursor/rules/proto_task-analyzer.mdc'
  },
  {
    id: 'multi-language-processing',
    type: 'rule',
    name: 'multi-language-processing',
    title: 'Multi-language Processing',
    subtitle: 'Vietnamese, Chinese, Japanese, Korean, Arabic',
    description:
      'Translation layer that converts a request from any supported language into English before processing, so downstream prompts and rules behave consistently.',
    category: 'Routing',
    tags: ['i18n', 'vietnamese', 'chinese'],
    path: '.cursor/rules/proto_multi-language-processing.mdc'
  },
  {
    id: 'skill-integration',
    type: 'rule',
    name: 'skill-integration',
    title: 'Skill Integration',
    subtitle: 'Skill auto-discovery execution protocol',
    description:
      'Routes work to the right skill, then enforces pre-review and post-review gates before and after code generation. Every task passes both gates.',
    category: 'Routing',
    tags: ['skills', 'gates', 'lifecycle'],
    path: '.cursor/rules/proto_skill-integration.mdc'
  },
  {
    id: 'skill-registry',
    type: 'rule',
    name: 'skill-registry',
    title: 'Skill Registry',
    subtitle: 'Single source of truth for skill definitions',
    description:
      'Defines every skill, its triggers, confidence thresholds, role (primary/overlay/mandatory), and gate mappings. Everything else imports from here.',
    category: 'Routing',
    tags: ['sot', 'registry', 'metadata'],
    path: '.cursor/rules/rule_skill-registry.mdc'
  },
  {
    id: 'architecture-patterns',
    type: 'rule',
    name: 'architecture-patterns',
    title: 'Architecture Patterns',
    subtitle: 'Clean, Hexagonal, CQRS, Event Sourcing, DDD',
    description:
      'Reference architectures and decision frameworks for choosing between monolith/microservices, layering, and isolation strategies.',
    category: 'Architecture',
    tags: ['clean', 'hexagonal', 'cqrs', 'event-sourcing', 'ddd'],
    path: '.cursor/rules/ref_architecture-patterns.mdc',
    bullets: ['Decision trees for layer split', 'When to use CQRS vs simple CRUD', 'Boundary and anti-corruption layer patterns']
  },
  {
    id: 'enterprise-patterns',
    type: 'rule',
    name: 'enterprise-patterns',
    title: 'Enterprise Patterns',
    subtitle: 'Monolith / Microservices / Core architecture',
    description:
      'System-architecture guidance for large teams: service boundaries, data ownership, deployment topology, and migration playbooks.',
    category: 'Architecture',
    tags: ['monolith', 'microservices', 'core-architecture'],
    path: '.cursor/rules/ref_enterprise-patterns.mdc'
  },
  {
    id: 'frontend-frameworks',
    type: 'rule',
    name: 'frontend-frameworks',
    title: 'Frontend Frameworks',
    subtitle: 'Next.js, Nuxt, Vue 3, generic patterns',
    description:
      'Conventions and tradeoffs for the three supported meta-frameworks. Covers App Router, server components, state management, and form patterns.',
    category: 'Architecture',
    tags: ['nextjs', 'nuxt', 'vue', 'ssr', 'ssg'],
    path: '.cursor/rules/ref_frontend-frameworks.mdc'
  },
  {
    id: 'backend-frameworks',
    type: 'rule',
    name: 'backend-frameworks',
    title: 'Backend Frameworks',
    subtitle: 'NestJS, Laravel, ASP.NET Core',
    description:
      'Reference patterns for the three supported backends — controller/service/repository layout, request validation, transactional boundaries.',
    category: 'Architecture',
    tags: ['nestjs', 'laravel', 'aspnet'],
    path: '.cursor/rules/ref_backend-frameworks.mdc'
  },
  {
    id: 'api-patterns',
    type: 'rule',
    name: 'api-patterns',
    title: 'API Patterns',
    subtitle: 'REST, GraphQL, gRPC, event-driven',
    description:
      'Contract design, versioning strategies, error envelopes (RFC 7807), pagination, and webhook signing. Pairs with the api-designer agent.',
    category: 'Architecture',
    tags: ['rest', 'graphql', 'grpc', 'webhooks'],
    path: '.cursor/rules/ref_api-patterns.mdc'
  },
  {
    id: 'auth',
    type: 'rule',
    name: 'auth',
    title: 'Authentication & Authorization',
    subtitle: 'Authentication + Authorization patterns',
    description:
      'JWT, OAuth2, OIDC, session, RBAC/ABAC. Covers refresh token rotation, PKCE, secure cookie flags, and authorization checks at the boundary.',
    category: 'Architecture',
    tags: ['jwt', 'oauth', 'rbac'],
    path: '.cursor/rules/ref_auth.mdc'
  },
  {
    id: 'multi-tenant',
    type: 'rule',
    name: 'multi-tenant',
    title: 'Multi-Tenant Architecture',
    subtitle: 'Isolation strategies for SaaS',
    description:
      'Silo, bridge, pool models with Postgres RLS patterns. When to share vs isolate, tenant-aware migrations, and tenant-bound audit logs.',
    category: 'Architecture',
    tags: ['saas', 'rls', 'isolation'],
    path: '.cursor/rules/ref_multi-tenant.mdc'
  },
  {
    id: 'databases',
    type: 'rule',
    name: 'databases',
    title: 'Databases',
    subtitle: 'PostgreSQL, MySQL, SQL Server + RLS',
    description:
      'Schema design, query optimization, migrations, and row-level security. Pair with the database-reviewer agent for any DDL change.',
    category: 'Data',
    tags: ['postgres', 'mysql', 'sqlserver', 'rls'],
    path: '.cursor/rules/ref_databases.mdc'
  },
  {
    id: 'redis',
    type: 'rule',
    name: 'redis',
    title: 'Redis & Caching',
    subtitle: 'Cache strategy + invalidation patterns',
    description:
      'Read-through, write-through, cache-aside, stampede protection, keyspace partitioning, and tag-based invalidation.',
    category: 'Data',
    tags: ['cache', 'redis', 'invalidation'],
    path: '.cursor/rules/ref_redis.mdc'
  },
  {
    id: 'supabase',
    type: 'rule',
    name: 'supabase',
    title: 'Supabase',
    subtitle: 'Patterns specific to Supabase',
    description:
      'Auth + RLS policies, edge functions, realtime channels, storage buckets, and migrations tied to the Supabase CLI.',
    category: 'Data',
    tags: ['supabase', 'rls', 'realtime'],
    path: '.cursor/rules/ref_supabase.mdc'
  },
  {
    id: 'security',
    type: 'rule',
    name: 'security',
    title: 'Security',
    subtitle: 'Web security + secrets management',
    description:
      'OWASP Top 10, secrets handling, supply-chain hardening, CSP, CORS. Pair with the security-auditor agent for any auth or payment work.',
    category: 'Security',
    tags: ['owasp', 'secrets', 'csp'],
    path: '.cursor/rules/ref_security.mdc'
  },
  {
    id: 'performance',
    type: 'rule',
    name: 'performance',
    title: 'Performance & Rate Limiting',
    subtitle: 'App perf + quota enforcement',
    description:
      'Bundle budgets, N+1 detection, cache layering, and rate-limit design (token bucket, leaky bucket, fixed window).',
    category: 'Security',
    tags: ['perf', 'rate-limit', 'caching'],
    path: '.cursor/rules/ref_performance.mdc'
  },
  {
    id: 'container-orchestration',
    type: 'rule',
    name: 'container-orchestration',
    title: 'Container Orchestration',
    subtitle: 'Docker + Kubernetes',
    description:
      'Image building, multi-stage patterns, pod security, networking, and rollout strategies (blue/green, canary).',
    category: 'Infrastructure',
    tags: ['docker', 'k8s', 'rollouts'],
    path: '.cursor/rules/ref_container-orchestration.mdc'
  },
  {
    id: 'cloud-providers',
    type: 'rule',
    name: 'cloud-providers',
    title: 'Cloud Providers',
    subtitle: 'AWS, Azure, GCP',
    description:
      'Provider-specific primitives, IAM nuances, network topology, and managed-service comparison cheatsheets.',
    category: 'Infrastructure',
    tags: ['aws', 'azure', 'gcp'],
    path: '.cursor/rules/ref_cloud-providers.mdc'
  },
  {
    id: 'cloud-infra',
    type: 'rule',
    name: 'cloud-infra',
    title: 'Cloud Infrastructure',
    subtitle: 'Cloud + infra architecture',
    description:
      'Account topology, VPC design, shared services, and infra-as-code patterns (Terraform, CDK).',
    category: 'Infrastructure',
    tags: ['vpc', 'iac', 'terraform'],
    path: '.cursor/rules/ref_cloud-infra.mdc'
  },
  {
    id: 'serverless',
    type: 'rule',
    name: 'serverless',
    title: 'Serverless & IaC',
    subtitle: 'Lambda / Functions + IaC',
    description:
      'Cold-start mitigation, function boundaries, IaC module layout, and state management.',
    category: 'Infrastructure',
    tags: ['lambda', 'serverless', 'iac'],
    path: '.cursor/rules/ref_serverless.mdc'
  },
  {
    id: 'cloudflare',
    type: 'rule',
    name: 'cloudflare',
    title: 'Cloudflare & CDN',
    subtitle: 'Edge platform + content delivery',
    description:
      'Workers, Pages, R2, KV, D1, cache rules, and edge observability.',
    category: 'Infrastructure',
    tags: ['cloudflare', 'cdn', 'edge'],
    path: '.cursor/rules/ref_cloudflare.mdc'
  },
  {
    id: 'deployment',
    type: 'rule',
    name: 'deployment',
    title: 'Deployment & CI/CD',
    subtitle: 'Deployment + CI/CD',
    description:
      'Release pipelines, environment promotion, rollback, and progressive delivery. Templates for GitHub Actions and GitLab CI.',
    category: 'Infrastructure',
    tags: ['cicd', 'release', 'rollback'],
    path: '.cursor/rules/ref_deployment.mdc'
  },
  {
    id: 'version-control',
    type: 'rule',
    name: 'version-control',
    title: 'Version Control',
    subtitle: 'Git + GitHub workflow',
    description:
      'Trunk-based, branch naming, PR conventions, and merge strategies. Pair with split-to-prs skill for large refactors.',
    category: 'Infrastructure',
    tags: ['git', 'github', 'pr'],
    path: '.cursor/rules/ref_version-control.mdc'
  },
  {
    id: 'observability',
    type: 'rule',
    name: 'observability',
    title: 'Observability',
    subtitle: 'Metrics, logs, traces, dashboards',
    description:
      'Three-pillar setup: metrics (Prometheus), logs (structured), and traces (OTel). Alert routing and SLO design.',
    category: 'Infrastructure',
    tags: ['otel', 'prometheus', 'logs'],
    path: '.cursor/rules/ref_observability.mdc'
  },
  {
    id: 'operations',
    type: 'rule',
    name: 'operations',
    title: 'Operations',
    subtitle: 'Alerting + Incident Response',
    description:
      'Pager setup, runbooks, sev levels, retrospectives, and communication cadence.',
    category: 'Infrastructure',
    tags: ['incident', 'runbook', 'sev'],
    path: '.cursor/rules/ref_operations.mdc'
  },
  {
    id: 'workflow-engines',
    type: 'rule',
    name: 'workflow-engines',
    title: 'Workflow Engines',
    subtitle: 'n8n, Trigger.dev, Temporal',
    description:
      'When to use which engine. Patterns for retries, idempotency, durable execution, and webhook ingress.',
    category: 'Integration',
    tags: ['n8n', 'triggerdev', 'temporal'],
    path: '.cursor/rules/ref_workflow-engines.mdc'
  },
  {
    id: 'vibe-code-protocol',
    type: 'rule',
    name: 'vibe-code-protocol',
    title: 'Vibe Code Protocol',
    subtitle: 'Pre/Post execution + retry + auth handling',
    description:
      'Workflow-execution protocol with pre-review and post-review gates, retry with fallback strategies, and safe-handling for auth/payment.',
    category: 'Integration',
    tags: ['vibe-code', 'retry', 'auth'],
    path: '.cursor/rules/ref_vibe-code-protocol.mdc'
  },
  {
    id: 'billing',
    type: 'rule',
    name: 'billing',
    title: 'Billing Implementation',
    subtitle: 'SaaS billing patterns',
    description:
      'Plans, proration, invoices, dunning, MRR/ARR reporting, and Stripe-specific pitfalls. Pair with the vietnam-payment-review skill for local gateways.',
    category: 'Integration',
    tags: ['stripe', 'saas-billing'],
    path: '.cursor/rules/ref_billing.mdc'
  },
  {
    id: 'chatbot-development',
    type: 'rule',
    name: 'chatbot-development',
    title: 'ChatbotX Development',
    subtitle: 'Omnichannel chatbot marketing platform',
    description:
      'Patterns for feature scaffold, Drizzle ORM, BullMQ workers, and Next.js routing inside the ChatbotX platform (ManyChat alternative).',
    category: 'Integration',
    tags: ['chatbotx', 'manychat', 'drizzle'],
    path: '.cursor/rules/ref_chatbot-development.mdc'
  },
  {
    id: 'crm-saas',
    type: 'rule',
    name: 'crm-saas',
    title: 'CRM SaaS',
    subtitle: 'Multi-tenant CRM patterns',
    description:
      'Vertical-specific patterns for CRM SaaS: pipeline stages, lead scoring, segmentation, and activity logging.',
    category: 'Integration',
    tags: ['crm', 'lead', 'pipeline'],
    path: '.cursor/rules/ref_crm-saas.mdc'
  },
  {
    id: 'ui-visual-design',
    type: 'rule',
    name: 'ui-visual-design',
    title: 'UI Visual Design',
    subtitle: 'Premium UI/visual design language',
    description:
      'Reference language for the framework landing pages and tools: tokens, motion, density, and anti-slop defaults.',
    category: 'Experience',
    tags: ['design', 'ui', 'tokens'],
    path: '.cursor/rules/ref_ui-visual-design.mdc'
  },
  {
    id: 'ai-knowledge',
    type: 'rule',
    name: 'ai-knowledge',
    title: 'AI Knowledge Stack',
    subtitle: 'RAG, vector search, PDF engine',
    description:
      'RAG orchestration with WeKnora, pgvector, hybrid retrieval, and PDF ingestion pipeline for document-grounded chat.',
    category: 'AI',
    tags: ['rag', 'weknora', 'pgvector'],
    path: '.cursor/rules/ref_ai-knowledge.mdc'
  },
  {
    id: 'llm-providers',
    type: 'rule',
    name: 'llm-providers',
    title: 'LLM Providers',
    subtitle: 'OpenAI, Gemini, Claude integration',
    description:
      'Provider APIs, retry semantics, streaming, function/tool calling, and fallback chains across the three majors.',
    category: 'AI',
    tags: ['openai', 'gemini', 'claude'],
    path: '.cursor/rules/ref_llm-providers.mdc'
  },
  {
    id: 'testing',
    type: 'rule',
    name: 'testing',
    title: 'Testing Best Practices',
    subtitle: 'Unit, integration, E2E, TDD',
    description:
      'Test pyramid, naming, mocking strategies, property-based testing, and the test-as-proof mantra. Pair with the test-engineer agent.',
    category: 'Quality',
    tags: ['tdd', 'unit', 'e2e'],
    path: '.cursor/rules/ref_testing.mdc'
  },
  {
    id: 'cost-optimization',
    type: 'rule',
    name: 'cost-optimization',
    title: 'Cost & Token Optimization',
    subtitle: 'Cost + token cost control',
    description:
      'Budget ceilings, prompt compression, response caching, and token accounting per workflow.',
    category: 'Quality',
    tags: ['cost', 'tokens', 'budget'],
    path: '.cursor/rules/ref_cost-optimization.mdc'
  }
]

// ────────────────────────────────────────────────────────────────────────────
// SKILLS — `.cursor/skills/*/SKILL.md`
// ────────────────────────────────────────────────────────────────────────────

export const SKILLS: FrameworkItem[] = [
  {
    id: 'karpathy-coding',
    type: 'skill',
    name: 'karpathy-coding',
    title: 'Karpathy Coding',
    subtitle: 'Mandatory overlay: think first, code second',
    description:
      'Codifies the four pillars (think before coding, simplicity, surgical changes, goal-driven). Runs pre/post gates on every coding task. -54% lines, -22% tokens.',
    category: 'Coding Discipline',
    tags: ['overlay', 'mandatory', 'karpathy'],
    role: 'overlay',
    path: '.cursor/skills/code_karpathy-coding/SKILL.md',
    gates: ['karpathy-pre', 'karpathy-post'],
    metrics: [
      { label: 'Lines of code', value: '-54%' },
      { label: 'Tokens', value: '-22%' },
      { label: 'Cost', value: '-20%' },
      { label: 'Time', value: '-27%' }
    ],
    bullets: [
      'karpathy-pre gates — assumptions, scope, success criteria',
      'Implementation: minimum code that solves the problem',
      'karpathy-post gates — surgical? minimal? goal-driven?'
    ]
  },
  {
    id: 'ponytail',
    type: 'skill',
    name: 'ponytail',
    title: 'Ponytail (Lazy Senior)',
    subtitle: 'YAGNI optimization, minimum code',
    description:
      '"He says nothing. He writes one line. It works." The YAGNI ladder paired with Karpathy — think first, then minimize. Cuts code while keeping safety at 100%.',
    category: 'Coding Discipline',
    tags: ['yagni', 'minimal', 'senior'],
    role: 'secondary',
    path: '.cursor/skills/special_ponytail/SKILL.md',
    gates: ['ponytail-pre', 'ponytail-post'],
    bullets: [
      'YAGNI Ladder (skip → reuse → stdlib → native → dependency → one line)',
      'Runs after karpathy gates — don\'t skip thinking',
      'Modes: lite / full / ultra / off'
    ]
  },
  {
    id: 'full-output',
    type: 'skill',
    name: 'full-output',
    title: 'Full Output',
    subtitle: 'No skeletons, no placeholders',
    description:
      'Enforces complete, unabridged code. Locks scope pre-generation, verifies completeness post-generation. No TODOs, no "continue later".',
    category: 'Coding Discipline',
    tags: ['completeness', 'no-skeleton'],
    role: 'primary',
    path: '.cursor/skills/special_full-output/SKILL.md',
    gates: ['fulloutput-pre', 'fulloutput-post']
  },
  {
    id: 'frontend-taste',
    type: 'skill',
    name: 'frontend-taste',
    title: 'Frontend Taste (Anti-Slop)',
    subtitle: 'For landing pages, portfolios, redesigns',
    description:
      'Reads the brief, infers design direction, sets three dials (VARIANCE / MOTION / DENSITY), and ships interfaces that don\'t look templated.',
    category: 'Frontend',
    tags: ['anti-slop', 'taste', 'landing-page'],
    role: 'primary',
    path: '.cursor/skills/ui_frontend-taste/SKILL.md',
    gates: ['taste-pre', 'taste-post'],
    bullets: [
      'Brief inference before code',
      'Three dials: VARIANCE · MOTION · DENSITY',
      'Anti-default discipline (no AI purple, no three feature cards)'
    ]
  },
  {
    id: 'frontend-review',
    type: 'skill',
    name: 'frontend-review',
    title: 'Frontend Review',
    subtitle: 'Dual-gate code quality check',
    description:
      'Mandatory pre-review scope analysis + post-review quality gates. Reviews correctness, design quality, accessibility, performance, and taste.',
    category: 'Frontend',
    tags: ['review', 'dual-gate', 'a11y'],
    role: 'primary',
    path: '.cursor/skills/ui_frontend-review/SKILL.md',
    gates: ['review-pre', 'review-post']
  },
  {
    id: 'frontend-redesign',
    type: 'skill',
    name: 'frontend-redesign',
    title: 'Frontend Redesign',
    subtitle: 'Improve existing UI without breaking it',
    description:
      'Pre-audit + post-audit gates for redesigns. Preserves what works, replaces what doesn\'t, and keeps the diff focused.',
    category: 'Frontend',
    tags: ['redesign', 'audit'],
    role: 'secondary',
    path: '.cursor/skills/ui_frontend-redesign/SKILL.md',
    gates: ['redesign-pre', 'redesign-post']
  },
  {
    id: 'security-review',
    type: 'skill',
    name: 'security-review',
    title: 'Security Review',
    subtitle: 'OWASP & pre-deploy check',
    description:
      'Pre-deploy audit against OWASP Top 10. Walks secrets, auth, input validation, supply-chain, and payment-specific surface.',
    category: 'Security',
    tags: ['owasp', 'pre-deploy'],
    role: 'primary',
    path: '.cursor/skills/sec_security-review/SKILL.md',
    gates: ['security-pre', 'security-post']
  },
  {
    id: 'vietnam-payment-review',
    type: 'skill',
    name: 'vietnam-payment-review',
    title: 'Vietnam Payment Review',
    subtitle: 'MoMo, SePay, PayOS, VNPay',
    description:
      'Payment-specific review for the Vietnamese market. Checks webhook signatures, idempotency, refund/partial-refund flow, and reconciliation.',
    category: 'Security',
    tags: ['payment', 'vietnam', 'webhook'],
    role: 'primary',
    path: '.cursor/skills/sec_vietnam-payment-review/SKILL.md',
    gates: ['payment-pre', 'payment-post']
  },
  {
    id: 'vietnam-address',
    type: 'skill',
    name: 'vietnam-address',
    title: 'Vietnam Address',
    subtitle: 'Provinces / wards / districts parser',
    description:
      'Parse, normalize, and validate Vietnamese administrative addresses. Handles the post-2025 province/ward restructuring.',
    category: 'Domain',
    tags: ['vietnam', 'address'],
    role: 'secondary',
    path: '.cursor/skills/ai_vietnam-address/SKILL.md'
  },
  {
    id: 'bazi',
    type: 'skill',
    name: 'bazi',
    title: 'Bazi (Tử Vi)',
    subtitle: 'Four Pillars / astrology engine',
    description:
      'Bazi (Tứ Trụ) engine for the Bazi landing template. Stem-branch calculations, ten-gods, and ten-year luck pillars.',
    category: 'Domain',
    tags: ['bazi', 'astrology', 'tu-vi'],
    role: 'primary',
    path: '.cursor/skills/ai_bazi/SKILL.md'
  },
  {
    id: 'document-ocr',
    type: 'skill',
    name: 'document-ocr',
    title: 'Document OCR',
    subtitle: 'Scan + extract structured data',
    description:
      'OCR for invoices, IDs, and contracts. Outputs normalized JSON + per-field confidence scores.',
    category: 'Domain',
    tags: ['ocr', 'invoice'],
    role: 'primary',
    path: '.cursor/skills/doc_document-ocr/SKILL.md'
  },
  {
    id: 'weknora-kb',
    type: 'skill',
    name: 'weknora-kb',
    title: 'WeKnora KB',
    subtitle: 'Knowledge base scaffold',
    description:
      'Scaffold a WeKnora-backed knowledge base for a project: sources, ingestion jobs, embedding strategy, and retrieval config.',
    category: 'AI',
    tags: ['rag', 'kb', 'weknora'],
    role: 'primary',
    path: '.cursor/skills/ai_weknora-kb/SKILL.md'
  },
  {
    id: 'weknora-agent',
    type: 'skill',
    name: 'weknora-agent',
    title: 'WeKnora Agent',
    subtitle: 'Grounded agent on a WeKnora KB',
    description:
      'Build a chat agent grounded on a WeKnora KB. Tool calling, citation rendering, and refusal when sources are missing.',
    category: 'AI',
    tags: ['agent', 'rag'],
    role: 'primary',
    path: '.cursor/skills/ai_weknora-agent/SKILL.md'
  },
  {
    id: 'video-generation',
    type: 'skill',
    name: 'video-generation',
    title: 'Video Generation',
    subtitle: 'AI short video (9:16)',
    description:
      'Generate vertical short-form video with AI. Script, scene, voiceover, and render pipeline.',
    category: 'AI',
    tags: ['video', 'short-form'],
    role: 'primary',
    path: '.cursor/skills/special_video-generation/SKILL.md'
  },
  {
    id: 'pixelrag',
    type: 'skill',
    name: 'pixelrag',
    title: 'Pixel RAG',
    subtitle: 'RAG over images',
    description:
      'Visual RAG: chunk images into regions, embed, and retrieve. Useful for design and screenshot QA.',
    category: 'AI',
    tags: ['image', 'rag'],
    role: 'secondary',
    path: '.cursor/skills/ai_pixelrag/SKILL.md'
  },
  {
    id: 'visual-explainer',
    type: 'skill',
    name: 'visual-explainer',
    title: 'Visual Explainer',
    subtitle: 'Diagrams from text',
    description:
      'Turn prose into annotated diagrams (sequence, architecture, ER). Style aligned with the UI visual design language.',
    category: 'Experience',
    tags: ['diagram', 'docs'],
    role: 'secondary',
    path: '.cursor/skills/special_visual-explainer/SKILL.md'
  },
  {
    id: 'open-design',
    type: 'skill',
    name: 'open-design',
    title: 'Open Design',
    subtitle: 'Design tokens for new projects',
    description:
      'Pick a token set, spacing scale, and motion curve before scaffolding a frontend. Anti-slop by default.',
    category: 'Experience',
    tags: ['design-tokens', 'primitives'],
    role: 'secondary',
    path: '.cursor/skills/special_open-design/SKILL.md'
  },
  {
    id: 'skill-installer',
    type: 'skill',
    name: 'skill-installer',
    title: 'Skill Installer',
    subtitle: 'Bootstrap a skill into a repo',
    description:
      'Install a new skill into the `.cursor/skills/` folder of a project and register it in the skill-registry rule.',
    category: 'Meta',
    tags: ['meta', 'install'],
    role: 'secondary',
    path: '.cursor/skills/util_skill-installer/SKILL.md'
  },
  {
    id: 'test-analysis',
    type: 'skill',
    name: 'test-analysis',
    title: 'Test Analysis',
    subtitle: 'Comprehensive testing: functional, UI, integration, e2e',
    description:
      'Comprehensive test analysis covering functional, UI, integration, and e2e testing. Ensures code correctness through systematic test design and verification.',
    category: 'Quality',
    tags: ['testing', 'quality', 'functional', 'UI-test', 'integration', 'e2e'],
    role: 'mandatory',
    path: '.cursor/skills/test_test-analysis/SKILL.md',
    gates: ['T.1', 'T.2'],
    bullets: [
      'Unit tests for individual functions/modules',
      'UI component and interaction testing',
      'API and integration testing',
      'E2E full user journey testing'
    ]
  },
  {
    id: 'perf-optimization',
    type: 'skill',
    name: 'perf-optimization',
    title: 'Performance Optimization',
    subtitle: 'Memory, speed, token efficiency, caching',
    description:
      'Performance optimization covering memory, speed, token efficiency, and caching strategies. Ensures applications run efficiently and cost-effectively.',
    category: 'Performance',
    tags: ['performance', 'optimization', 'memory', 'speed', 'token', 'caching'],
    role: 'mandatory',
    path: '.cursor/skills/perf_perf-optimization/SKILL.md',
    gates: ['P.1', 'P.2'],
    bullets: [
      'Memory optimization and leak prevention',
      'Speed optimization and parallel execution',
      'Token reduction and context management',
      'Caching strategies (memory, CDN, service worker)'
    ]
  },
  {
    id: 'stability',
    type: 'skill',
    name: 'stability',
    title: 'Stability & Reliability',
    subtitle: 'Error handling, resilience, monitoring',
    description:
      'Stability and reliability through error handling, resilience patterns, monitoring, and graceful degradation. Ensures applications remain operational under adverse conditions.',
    category: 'Operations',
    tags: ['stability', 'reliability', 'error-handling', 'resilience', 'monitoring'],
    role: 'mandatory',
    path: '.cursor/skills/util_stability/SKILL.md',
    gates: ['S.1', 'S.2'],
    bullets: [
      'Error classification and recovery patterns',
      'Circuit breaker and bulkhead patterns',
      'Health checks and monitoring',
      'Graceful degradation strategies'
    ]
  },
  {
    id: 'data-quality',
    type: 'skill',
    name: 'data-quality',
    title: 'Data Quality',
    subtitle: 'Database schema, validation, migrations, query optimization',
    description:
      'Data quality and database skill covering validation, schema design, migrations, and query optimization. Ensures data correctness and reliability.',
    category: 'Data',
    tags: ['data', 'database', 'validation', 'schema', 'migration', 'sql'],
    role: 'mandatory',
    path: '.cursor/skills/db_data-quality/SKILL.md',
    gates: ['D.1', 'D.2'],
    bullets: [
      'Input validation layers (client, API, service, database)',
      'Schema design and naming conventions',
      'Safe migrations with rollback strategy',
      'Query optimization and indexing'
    ]
  },
  {
    id: 'tdam-integration',
    type: 'skill',
    name: 'tdam-integration',
    title: 'TencentDB Agent Memory (TDAM)',
    subtitle: 'Layered memory hub for AI agents',
    description:
      'Integrates TencentCloud/TencentDB-Agent-Memory for advanced agent memory: 4 layers (L0 conversation → L3 persona), symbolic Mermaid Canvas compression, atomic fact extraction. Reduces token spend up to 92% on long sessions.',
    category: 'AI',
    tags: ['memory', 'tencentdb', 'tdam', 'token-savings', 'mermaid', 'layered-memory'],
    role: 'primary',
    path: '.cursor/skills/ai_tdam-integration/SKILL.md',
    gates: ['tdam-pre', 'tdam-post'],
    metrics: [
      { label: 'Token savings', value: '92%' },
      { label: 'Task success', value: '+47%' },
      { label: 'Latency', value: '<50ms' },
      { label: 'Memory layers', value: '4' }
    ],
    bullets: [
      '🆕 L0 — Raw conversation turns (compressed)',
      '🆕 L1 — Atomic facts extraction (entities, decisions)',
      '🆕 L2 — Scenario blocks (multi-turn context)',
      '🆕 L3 — User persona (long-term traits)',
      '🆕 Symbolic Mermaid Canvas — short-term context compression'
    ]
  },
  {
    id: 'tdam-cli',
    type: 'skill',
    name: 'tdam-cli',
    title: 'TDAM CLI',
    subtitle: 'Beautiful terminal UI for memory management',
    description:
      'Rich-powered CLI for interacting with TDAM directly from the terminal. Commands: status, capture, recall, compact, persona, scenarios, tool-call, build-context. Windows encoding-safe.',
    category: 'AI',
    tags: ['cli', 'rich', 'tdam', 'terminal-ui', 'productivity'],
    role: 'secondary',
    path: '.cursor_framework/tdam_cli.py',
    bullets: [
      'Rich-powered tables, trees, markdown rendering',
      'Cross-platform: Windows UTF-8 + Linux/macOS',
      'Operations: capture · recall · compact · persona · scenarios',
      'Workflow integration via build-context command'
    ]
  },
  {
    id: 'code-graph-analysis',
    type: 'skill',
    name: 'code-graph-analysis',
    title: 'Code Graph Analysis',
    subtitle: 'Knowledge graph queries using Memgraph + Qdrant',
    description:
      'Code graph analysis using vitali87/code-graph-rag. Provides natural language → Cypher queries, semantic code search, dependency tracing, and AST-based code understanding. Alternative to simple dependency graphs.',
    category: 'Performance',
    tags: ['knowledge-graph', 'cypher', 'memgraph', 'qdrant', 'code-analysis'],
    role: 'secondary',
    path: '.cursor/skills/code-graph-analysis/SKILL.md',
    gates: ['graph-pre', 'graph-post'],
    bullets: [
      'Natural language query → Cypher query',
      'Semantic code search with embeddings',
      'Dependency tracing and call chains',
      'AST-based code structure analysis'
    ]
  }
]

// ────────────────────────────────────────────────────────────────────────────
// AGENTS — `.cursor/agents/*.md`
// ────────────────────────────────────────────────────────────────────────────

export const AGENTS: FrameworkItem[] = [
  {
    id: 'code-reviewer',
    type: 'agent',
    name: 'code-reviewer',
    title: 'Code Reviewer',
    subtitle: 'Senior Staff Engineer — five-axis review',
    description:
      'Reviews code on correctness, design, readability, security, and performance. Surgical: change only what is needed, never refactor adjacent code. Approves cleanly when diffs are small and intent is clear.',
    category: 'Engineering',
    tags: ['review', 'readability', 'security', 'performance'],
    role: 'secondary',
    trigger: '/review · /code-simplify',
    path: '.cursor/agents/code-reviewer.md',
    bullets: [
      'Five axes: correctness, design, readability, security, performance',
      'Severity tiers: CRITICAL → HIGH → MEDIUM → LOW / NIT',
      'Targets ≤3 actionable items — manufactures issues if any are missing',
      'Blocks merge when diff exceeds 500 lines without split'
    ],
    alignsWith: ['.cursor/rules/rule_coding-standards.mdc', '.cursor/rules/rule_karpathy-guidelines.mdc']
  },
  {
    id: 'api-designer',
    type: 'agent',
    name: 'api-designer',
    title: 'API Designer',
    subtitle: 'REST / GraphQL contracts, RFC 7807',
    description:
      'Designs and reviews API contracts: REST maturity, GraphQL schema, gRPC + protobuf, webhooks (signed + idempotent), pagination, versioning, and OpenAPI specs.',
    category: 'Engineering',
    tags: ['rest', 'graphql', 'grpc', 'openapi'],
    role: 'secondary',
    trigger: '/api',
    path: '.cursor/agents/api-designer.md',
    bullets: [
      'Resource modeling: collection · singleton · sub-resource · action',
      'Idempotency, status codes, RFC 7807 Problem Details',
      'Versioning strategies (URI for public, header for internal)',
      'Webhook signature verification + delivery retries + replay endpoint'
    ],
    alignsWith: ['.cursor/rules/ref_api-patterns.mdc', '.cursor/rules/ref_auth.mdc']
  },
  {
    id: 'backend-reviewer',
    type: 'agent',
    name: 'backend-reviewer',
    title: 'Backend Reviewer',
    subtitle: 'NestJS · Laravel · ASP.NET Core',
    description:
      'Reviews backend code: API design, business logic correctness, error handling, transactional boundaries, concurrency safety, and multi-layer architecture.',
    category: 'Engineering',
    tags: ['nestjs', 'laravel', 'aspnet', 'concurrency'],
    role: 'secondary',
    trigger: '/backend',
    path: '.cursor/agents/backend-reviewer.md',
    alignsWith: ['.cursor/rules/ref_backend-frameworks.mdc', '.cursor/rules/ref_api-patterns.mdc']
  },
  {
    id: 'frontend-architect',
    type: 'agent',
    name: 'frontend-architect',
    title: 'Frontend Architect',
    subtitle: 'Next.js · Nuxt · Vue 3',
    description:
      'Component design, state management strategy, SSR/SSG/ISR choice, performance budgets, and accessibility (WCAG 2.1 AA). Reviews form architecture and routing decisions.',
    category: 'Engineering',
    tags: ['nextjs', 'nuxt', 'vue', 'a11y'],
    role: 'secondary',
    trigger: '/frontend',
    path: '.cursor/agents/frontend-architect.md',
    alignsWith: ['.cursor/rules/ref_frontend-frameworks.mdc', '.cursor/rules/ref_ui-visual-design.mdc']
  },
  {
    id: 'database-reviewer',
    type: 'agent',
    name: 'database-reviewer',
    title: 'Database Reviewer',
    subtitle: 'PostgreSQL · MySQL · SQL Server',
    description:
      'Schema design, query optimization, indexing, migrations, RLS for multi-tenant isolation, data integrity constraints, and Redis cache strategy.',
    category: 'Engineering',
    tags: ['postgres', 'rls', 'migrations', 'redis'],
    role: 'secondary',
    trigger: '/db',
    path: '.cursor/agents/database-reviewer.md',
    alignsWith: ['.cursor/rules/ref_databases.mdc', '.cursor/rules/ref_redis.mdc']
  },
  {
    id: 'security-auditor',
    type: 'agent',
    name: 'security-auditor',
    title: 'Security Auditor',
    subtitle: 'OWASP · STRIDE · marketing-privacy (MSA-01..30)',
    description:
      'Security engineer: assumes breach, verifies defense. Audits auth, secrets, input validation, API security, dependency tree. Cites OWASP Top 10 + 30 Marketing Security Additions (MSA-01 to MSA-30) covering cookie banner parity, GDPR/CCPA, email auth, ad platform privacy, dark patterns, AI marketing risks.',
    category: 'Security',
    tags: ['owasp', 'secrets', 'auth', 'payment', 'gdpr', 'consent', 'privacy', 'marketing-security'],
    role: 'secondary',
    trigger: '/security · /privacy · /gdpr · /consent',
    path: '.cursor/agents/security-auditor.md',
    bullets: [
      'Five layers: auth, input validation, data, API, supply chain',
      'OWASP Top 10 (2021) — A01 Broken Access Control → A10 SSRF',
      '🆕 30 MSA additions: cookie banner parity, GDPR/CCPA/LGPD/PIPL/PDPD, email auth, CAPI hashing, dark patterns, AI marketing',
      '🆕 BLOCKS deploy on dark patterns · pre-checked consent · PII to public LLM · missing SPF/DKIM/DMARC',
      'Pre-deploy gate · runs after any CVE announcement'
    ],
    alignsWith: [
      '.cursor/rules/security.mdc',
      '.cursor/rules/auth.mdc',
      '.cursor/knowledge/marketing/best-practice.md §10',
      '.cursor/knowledge/marketing/anti-pattern.md §10',
      '.cursor/agents/marketing-strategist.md'
    ]
  },
  {
    id: 'test-engineer',
    type: 'agent',
    name: 'test-engineer',
    title: 'Test Engineer',
    subtitle: 'QA Specialist · Prove-It pattern',
    description:
      'Test strategy, coverage analysis (line/branch/mutation), mocking strategy, test pyramid (80/15/5), and the Prove-It pattern: red → green → refactor → verify.',
    category: 'Quality',
    tags: ['tdd', 'coverage', 'mocking', 'regression'],
    role: 'secondary',
    trigger: '/test',
    path: '.cursor/agents/test-engineer.md',
    bullets: [
      'Test pyramid 80 / 15 / 5 — invert only with explicit justification',
      'Coverage: 100% happy path, 80%+ error paths',
      'Reject tests without assertions, brittle mocks, mock-everything anti-patterns'
    ],
    alignsWith: ['.cursor/rules/ref_testing.mdc']
  },
  {
    id: 'web-performance-auditor',
    type: 'agent',
    name: 'web-performance-auditor',
    title: 'Web Performance Auditor',
    subtitle: 'Core Web Vitals · Lighthouse · bundles',
    description:
      'LCP / INP / CLS targets, bundle analysis, render profiling, Lighthouse audits. Cites metric, source, and expected delta on every recommendation.',
    category: 'Quality',
    tags: ['cwv', 'lighthouse', 'bundle', 'jank'],
    role: 'secondary',
    trigger: '/perf',
    path: '.cursor/agents/web-performance-auditor.md',
    bullets: [
      'LCP < 2.5s · INP < 200ms · CLS < 0.1',
      'Audit modes: quick (Lighthouse + bundle) and deep (full perf trace)',
      'Flags: bundles > 500KB gz, render-blocking 3rd party, layout thrash'
    ],
    alignsWith: ['.cursor/rules/ref_performance.mdc']
  },
  {
    id: 'debugger',
    type: 'agent',
    name: 'debugger',
    title: 'Debugger',
    subtitle: '4-phase root-cause investigator',
    description:
      'Systematic bug investigation: reproduce → isolate → fix → verify. Forms ≤ 3 hypotheses per round, tests the cheapest first, escalates when unproven. Never shotgun-debug; never ship a fix without a regression test.',
    category: 'Engineering',
    tags: ['debug', 'root-cause', 'repro', 'verification'],
    role: 'secondary',
    trigger: '/debug · /fix · /bug',
    path: '.cursor/agents/debugger.md',
    bullets: [
      '4-phase protocol: reproduce · isolate · fix · verify',
      'Reads code, not stack traces — top-to-bottom, not just failing line',
      'Hypotheses ranked by likelihood; cheapest probe first',
      'Refuses to ship a fix without regression test + 5-step verification'
    ],
    alignsWith: ['.cursor/rules/rule_coding-standards.mdc', '.cursor/rules/rule_karpathy-guidelines.mdc']
  },
  {
    id: 'ui-designer',
    type: 'agent',
    name: 'ui-designer',
    title: 'UI Designer',
    subtitle: 'Design tokens · components · states',
    description:
      'Translates product goals into production-ready visual specs. Designs systems, not one-off screens. Outputs tokens (color/typography/spacing), component anatomy + states + a11y, ready-to-paste Tailwind / CSS. Never ships a spec without empty/loading/error states.',
    category: 'Design',
    tags: ['design-tokens', 'components', 'a11y', 'motion'],
    role: 'secondary',
    trigger: '/design · /ui · /redesign',
    path: '.cursor/agents/ui-designer.md',
    bullets: [
      'Tokens first (color / typography / spacing / radius / shadow / motion)',
      'Composition > configuration; one primary action per viewport',
      'States per component: empty · loading · error · success · hover · focus · disabled',
      'WCAG 2.1 AA baseline; never ship without a11y check'
    ],
    alignsWith: ['.cursor/rules/ref_ui-visual-design.mdc', '.cursor/skills/special_web-design-guidelines/SKILL.md']
  },
  {
    id: 'web-cloner',
    type: 'agent',
    name: 'web-cloner',
    title: 'Web Cloner',
    subtitle: 'Playwright-driven visual + behavioral clone',
    description:
      'Clones UI / visual appearance, assets, and interactive behavior into a self-contained project. Fidelity levels L1 (static) → L4 (framework-faithful). Respects robots.txt, copyright, and rate limits. Outputs to .cursor/clones/{domain}/.',
    category: 'Engineering',
    tags: ['playwright', 'clone', 'mirror', 'pixel-perfect'],
    role: 'secondary',
    trigger: '/clone · /copy · /mirror',
    path: '.cursor/agents/web-cloner.md',
    bullets: [
      '5-phase: discovery · extract · rebuild · verify · document',
      'Fidelity levels L1–L4 — default L2 (visual + essential JS)',
      'Visual diff ≤ 2% via toHaveScreenshot(maxDiffPixelRatio: 0.02)',
      'Self-contained: assets local, no external CDN, no tracking scripts'
    ],
    alignsWith: ['.cursor/commands/clone/command.md', '.cursor/skills/special_playwright/SKILL.md']
  },
  {
    id: 'web-scraper',
    type: 'agent',
    name: 'web-scraper',
    title: 'Web Scraper',
    subtitle: 'Structured content extraction (SDK/API/UI/test/qc)',
    description:
      'Extracts structured content from websites via Playwright. Targets SDK requirements, API specs, UI specs, test docs, QC criteria, articles, tables, lists. Always respects robots.txt, throttles to ≤ 1 req/sec, and cites source URLs in every output file.',
    category: 'Engineering',
    tags: ['playwright', 'scrape', 'extract', 'docs'],
    role: 'secondary',
    trigger: '/scrape · /extract · /docs',
    path: '.cursor/agents/web-scraper.md',
    bullets: [
      'Content categories: sdk · api · ui · test · qc · article · table · list · code',
      'Static HTML → fetch/curl; SPA → Playwright with networkidle wait',
      'Cleanup preserves structure; never strips code, attribution, alt-text',
      'Output schema predictable: same category → same folder under .cursor/knowledge/{domain}/'
    ],
    alignsWith: ['.cursor/commands/scrape/command.md', '.cursor/skills/special_playwright/SKILL.md']
  },
  {
    id: 'refactor-specialist',
    type: 'agent',
    name: 'refactor-specialist',
    title: 'Refactor Specialist',
    subtitle: 'Behavior-preserving transformation',
    description:
      'Refactors without breaking anything. Behavior preservation is non-negotiable: same tests pass before and after every change. Catalogs 15 code smells with refactor recipes. One smell per commit; never mixed with feature work.',
    category: 'Engineering',
    tags: ['refactor', 'smells', 'tests-first', 'boy-scout'],
    role: 'secondary',
    trigger: '/refactor · /cleanup',
    path: '.cursor/agents/refactor-specialist.md',
    bullets: [
      '15 smells → 15 refactor recipes (extract-fn, parameter-object, polymorphism…)',
      'Risk tiers R0–R3; public APIs + schema = R3 (avoid)',
      'One commit per smell · never mixed with feature work',
      'Refuses to refactor without an existing test safety net'
    ],
    alignsWith: ['.cursor/skills/special_ponytail/SKILL.md', '.cursor/agents/code-reviewer.md']
  },
  {
    id: 'deployment-engineer',
    type: 'agent',
    name: 'deployment-engineer',
    title: 'Deployment Engineer',
    subtitle: 'Safe rollout · rollback · observability',
    description:
      'Ships safely: small changes, fast rollback, observable at every step, blast radius capped. Pre-flight checklist, canary → ramp → verify phases. Coordinates with migration-specialist for schema changes. Never deploys Friday after 3pm.',
    category: 'Operations',
    tags: ['deploy', 'rollback', 'canary', 'observability'],
    role: 'secondary',
    trigger: '/deploy · /release · /ship',
    path: '.cursor/agents/deployment-engineer.md',
    bullets: [
      'Pre-flight checklist: 10 gates, all must pass before deploy',
      'Strategies: all-at-once / rolling / blue-green / canary / feature-flag',
      'Rollback rehearsed ≤ 1 min for every change',
      'Coordinates with migration-specialist for schema changes'
    ],
    alignsWith: ['.cursor/rules/ref_deployment.mdc', '.cursor/rules/ref_observability.mdc']
  },
  {
    id: 'migration-specialist',
    type: 'agent',
    name: 'migration-specialist',
    title: 'Migration Specialist',
    subtitle: 'Expand · migrate · contract',
    description:
      'Schema changes, data migrations, framework upgrades. Always reversible, always idempotent, always throttled. Uses the expand → migrate → contract pattern (3 deploys, not 1). Coordinates with deployment-engineer for release windows.',
    category: 'Engineering',
    tags: ['migration', 'schema', 'backfill', 'expand-contract'],
    role: 'secondary',
    trigger: '/migrate · /schema · /backfill',
    path: '.cursor/agents/migration-specialist.md',
    bullets: [
      'Iron rule: expand → migrate → contract (3 deploys, not 1)',
      'Backfill: batched · idempotent · observable · throttled',
      'CREATE INDEX CONCURRENTLY, never lock writes on prod tables',
      'Reversibility plan required for every migration'
    ],
    alignsWith: ['.cursor/rules/ref_databases.mdc', '.cursor/agents/deployment-engineer.md']
  },
  {
    id: 'doc-writer',
    type: 'agent',
    name: 'doc-writer',
    title: 'Doc Writer',
    subtitle: 'API docs · READMEs · ADRs · runbooks',
    description:
      'Technical writer for documentation that survives. Applies Diátaxis (tutorial / how-to / reference / explanation), templates per doc type, and verifies every command and example. Treats docs as code: versioned, reviewed, runnable.',
    category: 'Quality',
    tags: ['docs', 'adr', 'runbook', 'readme'],
    role: 'secondary',
    trigger: '/doc · /readme · /adr · /runbook',
    path: '.cursor/agents/doc-writer.md',
    bullets: [
      'Diátaxis: tutorial · how-to · reference · explanation (one per page)',
      'Templates: README · ADR · Runbook · API Reference (ready to fill)',
      'Every command runnable; every example verified; no "coming soon"',
      'Update docs in same PR as code change when relevant'
    ],
    alignsWith: ['.cursor/commands/doc/command.md', '.cursor/commands/adr/command.md']
  },
  {
    id: 'devops-engineer',
    type: 'agent',
    name: 'devops-engineer',
    title: 'DevOps Engineer',
    subtitle: 'CI/CD · IaC · containers · observability',
    description:
      'Builds the systems that build, ship, and run software. Pipelines-as-code, declarative infra, reproducible environments, four golden signals. Optimizes for MTTR, change-failure rate, and dev experience — not just speed. Tags everything for cost tracking.',
    category: 'Operations',
    tags: ['ci-cd', 'iac', 'kubernetes', 'observability'],
    role: 'secondary',
    trigger: '/build · /infra · /pipeline',
    path: '.cursor/agents/devops-engineer.md',
    bullets: [
      'Four golden signals: latency · traffic · errors · saturation',
      'IaC: modules versioned · state in remote backend with locking · drift detection',
      'Container security: non-root · distroless · resource limits · probes',
      'Reproducible from scratch ≤ 1 hour; tagged resources; SLOs mandatory'
    ],
    alignsWith: ['.cursor/rules/ref_container-orchestration.mdc', '.cursor/rules/ref_cloud-infra.mdc']
  },
  {
    id: 'marketing-strategist',
    type: 'agent',
    name: 'marketing-strategist',
    title: 'Marketing Strategist',
    subtitle: 'Positioning · funnels · security-gated growth',
    description:
      'Product marketing & growth strategist with security overlay. Designs positioning, funnels, content, SEO, paid distribution, lifecycle, retention across 9 categories (47 concept-refs from coreyhaines31/marketingskills). Every marketing task passes 5-question security gate (PII/audience/tracking/regions/AI). Numbers before opinions; cheapest test first; security is launch blocker.',
    category: 'Growth',
    tags: ['positioning', 'funnel', 'seo', 'lifecycle', 'measurement', 'privacy', 'consent'],
    role: 'secondary',
    trigger: '/marketing · /growth · /positioning · /funnel',
    path: '.cursor/agents/marketing-strategist.md',
    bullets: [
      '9 categories routed via .cursor/knowledge/marketing/decision-tree.md §11',
      '🆕 5-question security gate before any marketing skill — PII/audience/tracking/regions/AI',
      '🆕 Severity-classified routing (CRITICAL/HIGH/MEDIUM/LOW) into security-auditor',
      'Funnel audits: 5-step template with hypothesis × impact ranking',
      'CAC ceiling set before paid launch · LTV × payback target',
      'One metric · one experiment · one decision. Test before ship.'
    ],
    alignsWith: [
      '.cursor/knowledge/marketing/',
      '.cursor/rules/rule_skill-registry.mdc §9',
      '.cursor/knowledge/marketing/best-practice.md §10',
      '.cursor/agents/security-auditor.md'
    ]
  },
  {
    id: 'api-security',
    type: 'agent',
    name: 'api-security',
    title: 'API Security Auditor',
    subtitle: 'REST/GraphQL/WebSocket API security review',
    description:
      'Comprehensive security review for REST, GraphQL, and WebSocket APIs. Covers authentication, authorization, rate limiting, input validation, and secure communication. OWASP API Security Top 10 compliant.',
    category: 'Security',
    tags: ['security', 'api', 'REST', 'GraphQL', 'authentication', 'authorization'],
    role: 'primary',
    trigger: '/api-security',
    path: '.cursor/agents/agent_api-security.md',
    bullets: [
      'Authentication layer: JWT, OAuth2, API Keys',
      'Authorization: RBAC, ABAC, IDOR prevention',
      'Rate limiting: Token bucket, sliding window',
      'Input validation: Schema, sanitization, injection prevention'
    ],
    alignsWith: ['.cursor/rules/ref_security.mdc', '.cursor/rules/ref_auth.mdc']
  },
  {
    id: 'ui-design',
    type: 'agent',
    name: 'ui-design',
    title: 'UI/Design Specialist',
    subtitle: 'Visual design, animation, anti-slop principles',
    description:
      'Creates visually stunning, professional interfaces with anti-slop design principles. Focuses on aesthetics, animations, typography, and user experience. 57 slop-detection gates.',
    category: 'Design',
    tags: ['design', 'UI', 'UX', 'aesthetic', 'animation', 'typography'],
    role: 'primary',
    trigger: '/design',
    path: '.cursor/agents/agent_ui-design.md',
    bullets: [
      'Visual hierarchy and component design',
      'Animation and motion patterns',
      'Typography excellence and spacing',
      '57 anti-slop detection gates'
    ],
    alignsWith: ['.cursor/rules/ref_ui-visual-design.mdc', '.cursor/skills/ui_hallmark/SKILL.md']
  },
  {
    id: 'data-quality-agent',
    type: 'agent',
    name: 'data-quality-agent',
    title: 'Data Quality Agent',
    subtitle: 'Database schema, validation, migrations',
    description:
      'Ensures data correctness and integrity through database schema design, validation patterns, migration safety, and query optimization. PostgreSQL, MySQL, MongoDB expertise.',
    category: 'Data',
    tags: ['database', 'schema', 'validation', 'migration', 'sql'],
    role: 'primary',
    trigger: '/data-quality',
    path: '.cursor/skills/db_data-quality/SKILL.md',
    bullets: [
      'Schema design and naming conventions',
      'Input validation at every layer',
      'Safe migrations with rollback',
      'Query optimization and indexing'
    ],
    alignsWith: ['.cursor/rules/ref_databases.mdc', '.cursor/rules/ref_redis.mdc']
  },
  {
    id: 'stability-agent',
    type: 'agent',
    name: 'stability-agent',
    title: 'Stability Agent',
    subtitle: 'Error handling, resilience, monitoring',
    description:
      'Ensures application stability through error handling, resilience patterns, monitoring, and graceful degradation. Golden signals: latency, errors, traffic, saturation.',
    category: 'Operations',
    tags: ['stability', 'reliability', 'error-handling', 'monitoring'],
    role: 'primary',
    trigger: '/stability',
    path: '.cursor/skills/util_stability/SKILL.md',
    bullets: [
      'Error classification and recovery',
      'Circuit breaker and retry patterns',
      'Health checks and monitoring',
      'Golden signals monitoring'
    ],
    alignsWith: ['.cursor/rules/ref_observability.mdc', '.cursor/rules/ref_operations.mdc']
  }
];

/* eslint-disable @typescript-eslint/no-unused-vars */
// ────────────────────────────────────────────────────────────────────────────
// MARKETING CONCEPT-REFS — `.cursor/knowledge/marketing/*.md` (sync 2026-07-15)
//
// Source: https://github.com/coreyhaines31/marketingskills (39k stars, MIT)
//
    // Follows the Superpowers concept-ref pattern (see .cursor/rules/rule_skill-registry.mdc §8).
// Each item below is a marketing skill/category merged into an existing knowledge file.
// NO new SKILL.md files were created — entries here exist purely so the web catalog
// can display them under the "Marketing" category.
//
// 🆕 SECURITY OVERLAY (sync 2026-07-15 v2):
// All 7 marketing knowledge files also have §10/§11/§14 security sections, derived
// from coreyhaines31/marketingskills patterns touching consent, GDPR/CCPA, tracking,
// email authentication, ad platform privacy, dark patterns, AI marketing risks.
    // See .cursor/rules/rule_skill-registry.mdc §10 for full MSA-01..30 concept-ref map.
// ────────────────────────────────────────────────────────────────────────────

export type MarketingCategory =
  | 'conversion'
  | 'content'
  | 'seo'
  | 'paid'
  | 'measurement'
  | 'retention'
  | 'growth'
  | 'strategy'
  | 'sales'

export interface MarketingSkillRef {
  id: string
  slug: string // v2.0 skill slug (renamed from v1.x)
  legacySlug?: string // v1.x slug (for migration reference)
  name: string
  title: string
  category: MarketingCategory
  description: string
  knowledgeFile: string // path under .cursor/knowledge/marketing/
  section: string // e.g. "best-practice.md §2.2"
  triggers: string[]
  antiPatternFile?: string
  faqFile?: string
}

export const MARKETING_CONCEPT_REFS: MarketingSkillRef[] = [
  // ─── Conversion Optimization ──────────────────────────────────────────────
  {
    id: 'mkt-cro',
    slug: 'cro',
    legacySlug: 'page-cro + form-cro (v2.0 merge)',
    name: 'cro',
    title: 'Conversion Rate Optimization',
    category: 'conversion',
    description:
      'Optimize landing pages, forms, and signup flows for higher conversion. Covers above-the-fold value prop, CTA placement, social proof, page speed, and form-field reduction.',
    knowledgeFile: 'best-practice.md',
    section: '§2 CRO heuristics',
    triggers: ['cro', 'conversion rate', 'landing page', 'cta'],
    antiPatternFile: 'anti-pattern.md §9.1',
    faqFile: 'faq.md §9.1'
  },
  {
    id: 'mkt-signup',
    slug: 'signup',
    legacySlug: 'signup-flow-cro',
    name: 'signup',
    title: 'Signup Flow CRO',
    category: 'conversion',
    description:
      'Reduce signup friction: minimum viable fields, social login options, progress indicators, and post-signup activation.',
    knowledgeFile: 'best-practice.md',
    section: '§2.2 Form fields',
    triggers: ['signup', 'sign-up', 'register', 'create account'],
    antiPatternFile: 'anti-pattern.md §9.1.2',
    faqFile: 'faq.md §9.1'
  },
  {
    id: 'mkt-onboarding',
    slug: 'onboarding',
    legacySlug: 'onboarding-cro',
    name: 'onboarding',
    title: 'Onboarding CRO',
    category: 'conversion',
    description:
      'Drive new users to activation event and aha moment. 3-5 step checklist, empty states that teach, milestone celebrations.',
    knowledgeFile: 'best-practice.md',
    section: '§5.1 Journey design',
    triggers: ['onboarding', 'activation', 'aha moment', 'first-run'],
    antiPatternFile: 'anti-pattern.md §9.1.5',
    faqFile: 'faq.md §9.1'
  },
  {
    id: 'mkt-popups',
    slug: 'popups',
    legacySlug: 'popup-cro',
    name: 'popups',
    title: 'Popup CRO',
    category: 'conversion',
    description:
      'Non-spammy popups: exit-intent, scroll-depth, time-delayed. Frequency capping, dismissal memory, and intent-based targeting.',
    knowledgeFile: 'best-practice.md',
    section: '§2.4 Modal templates',
    triggers: ['popup', 'pop-up', 'modal', 'exit-intent'],
    antiPatternFile: 'anti-pattern.md §9.1.4',
    faqFile: 'faq.md §9.1'
  },
  {
    id: 'mkt-paywalls',
    slug: 'paywalls',
    legacySlug: 'paywall-upgrade-cro',
    name: 'paywalls',
    title: 'Paywall & Upgrade Flow',
    category: 'conversion',
    description:
      'Trial expiration, feature limit, and usage-based upgrade prompts. Softwall vs hardwall, plan comparison, discount vs feature gating.',
    knowledgeFile: 'architecture.md',
    section: '§4.1.2 Funnel state machine',
    triggers: ['paywall', 'upgrade flow', 'trial expiration'],
    antiPatternFile: 'anti-pattern.md §9.1',
    faqFile: 'faq.md §9.1'
  },

  // ─── Content & Copy ────────────────────────────────────────────────────────
  {
    id: 'mkt-copywriting',
    slug: 'copywriting',
    name: 'copywriting',
    title: 'Copywriting',
    category: 'content',
    description:
      'Persuasive copy for landing pages, emails, ads, and sales pages. Above-the-fold formulas (problem→promise→proof→CTA), benefit-led bullets, risk reversal.',
    knowledgeFile: 'best-practice.md',
    section: '§2 Email + landing copy',
    triggers: ['copywriting', 'landing copy', 'sales copy'],
    antiPatternFile: 'anti-pattern.md §9.2',
    faqFile: 'faq.md §9.2'
  },
  {
    id: 'mkt-cold-email',
    slug: 'cold-email',
    name: 'cold-email',
    title: 'Cold Email',
    category: 'content',
    description:
      'B2B cold outreach sequences. Trigger events, multi-channel cadence (email + LinkedIn + phone), personalization tokens, reply handling.',
    knowledgeFile: 'best-practice.md',
    section: '§2.5 B2B outreach sequences',
    triggers: ['cold email', 'outreach', 'b2b email', 'sales sequence'],
    antiPatternFile: 'anti-pattern.md §9.2.4',
    faqFile: 'faq.md §9.2'
  },
  {
    id: 'mkt-emails',
    slug: 'emails',
    legacySlug: 'email-sequence',
    name: 'emails',
    title: 'Email Sequence',
    category: 'content',
    description:
      'Lifecycle email: welcome, nurture, re-engagement, transactional. Subject-line A/B, send-time optimization, deliverability (SPF/DKIM/DMARC).',
    knowledgeFile: 'best-practice.md',
    section: '§2.1 Templates',
    triggers: ['email sequence', 'newsletter', 'drip campaign', 'lifecycle email'],
    antiPatternFile: 'anti-pattern.md §9.2',
    faqFile: 'faq.md §9.2'
  },
  {
    id: 'mkt-sms',
    slug: 'sms',
    name: 'sms',
    title: 'SMS Marketing',
    category: 'content',
    description:
      'SMS marketing with TCPA / GDPR compliance. Double opt-in, time-window respect, opt-out handling, sender ID registration.',
    knowledgeFile: 'best-practice.md',
    section: '§2.9 SMS compliance + flows',
    triggers: ['sms marketing', 'sms campaign', 'tcpa'],
    antiPatternFile: 'anti-pattern.md §9.2.5',
    faqFile: 'faq.md §9.2'
  },

  // ─── SEO & Discovery ───────────────────────────────────────────────────────
  {
    id: 'mkt-seo-audit',
    slug: 'seo-audit',
    name: 'seo-audit',
    title: 'SEO Audit',
    category: 'seo',
    description:
      'Technical SEO audit: crawlability, indexability, internal linking, schema, page speed, and content quality scoring.',
    knowledgeFile: 'architecture.md',
    section: '§4.3.1 Crawler architecture',
    triggers: ['seo', 'seo audit', 'technical seo'],
    antiPatternFile: 'anti-pattern.md §9.3',
    faqFile: 'faq.md §9.3'
  },
  {
    id: 'mkt-ai-seo',
    slug: 'ai-seo',
    name: 'ai-seo',
    title: 'AI Search Optimization (AEO/GEO/LLMO)',
    category: 'seo',
    description:
      'Optimize for ChatGPT, Claude, Perplexity, Google AI Overviews. llms.txt, structured data, E-E-A-T signals, citations.',
    knowledgeFile: 'architecture.md',
    section: '§4.3.4 AI-citation schema + llms.txt',
    triggers: ['ai seo', 'llmo', 'geo', 'aeo', 'llms.txt', 'chatgpt search'],
    antiPatternFile: 'anti-pattern.md §9.3.3',
    faqFile: 'faq.md §9.3'
  },
  {
    id: 'mkt-programmatic-seo',
    slug: 'programmatic-seo',
    name: 'programmatic-seo',
    title: 'Programmatic SEO',
    category: 'seo',
    description:
      'Template-driven SEO pages at scale (100-10,000+). Data hydration, unique value per page, internal linking matrix, quality gate.',
    knowledgeFile: 'architecture.md',
    section: '§4.3.2 Template-driven pages',
    triggers: ['programmatic seo', 'seo template', 'seo at scale'],
    antiPatternFile: 'anti-pattern.md §9.3.2',
    faqFile: 'faq.md §9.3'
  },
  {
    id: 'mkt-schema',
    slug: 'schema',
    legacySlug: 'schema-markup',
    name: 'schema',
    title: 'Schema Markup',
    category: 'seo',
    description:
      'JSON-LD structured data: Organization, WebSite, Article, Product, FAQPage, BreadcrumbList, LocalBusiness. Rich Results validation.',
    knowledgeFile: 'best-practice.md',
    section: '§3.4 Product/Organization/FAQPage',
    triggers: ['schema markup', 'json-ld', 'rich snippets', 'structured data'],
    antiPatternFile: 'anti-pattern.md §9.3.4',
    faqFile: 'faq.md §9.3'
  },
  {
    id: 'mkt-aso',
    slug: 'aso',
    legacySlug: 'aso-audit',
    name: 'aso',
    title: 'App Store Optimization',
    category: 'seo',
    description:
      'App Store + Play Store listing optimization. Title, subtitle, keyword field, screenshots, preview video, ratings prompt timing.',
    knowledgeFile: 'best-practice.md',
    section: '§3.5 App Store / Play listing',
    triggers: ['aso', 'app store optimization', 'play store'],
    antiPatternFile: 'anti-pattern.md §9.3.6',
    faqFile: 'faq.md §9.3'
  },

  // ─── Paid & Distribution ───────────────────────────────────────────────────
  {
    id: 'mkt-ads',
    slug: 'ads',
    legacySlug: 'paid-ads',
    name: 'ads',
    title: 'Paid Ads',
    category: 'paid',
    description:
      'Google/Meta/LinkedIn/TikTok campaign structure. Audience targeting, exclusion lists, bid strategies, frequency capping, creative refresh cadence.',
    knowledgeFile: 'best-practice.md',
    section: '§4.1 Google/Meta/LinkedIn campaign structure',
    triggers: ['paid ads', 'google ads', 'meta ads', 'facebook ads', 'linkedin ads'],
    antiPatternFile: 'anti-pattern.md §9.4',
    faqFile: 'faq.md §9.4'
  },
  {
    id: 'mkt-ad-creative',
    slug: 'ad-creative',
    name: 'ad-creative',
    title: 'Ad Creative',
    category: 'paid',
    description:
      'Bulk creative iteration: 3×3 angle matrix → 27 ad variants → auto-test → scale winner → refresh every 7-14 days.',
    knowledgeFile: 'best-practice.md',
    section: '§4.2 Bulk headline/description iteration',
    triggers: ['ad creative', 'ad copy', 'creative testing'],
    antiPatternFile: 'anti-pattern.md §9.4.2',
    faqFile: 'faq.md §9.4'
  },

  // ─── Measurement & Testing ─────────────────────────────────────────────────
  {
    id: 'mkt-analytics',
    slug: 'analytics',
    legacySlug: 'analytics-tracking',
    name: 'analytics',
    title: 'Analytics & Tracking',
    category: 'measurement',
    description:
      'Tracking plan, event taxonomy, SDK deployment, server-side tracking, Conversion API, Enhanced Conversions. Funnel + cohort dashboards.',
    knowledgeFile: 'architecture.md',
    section: '§4.5.1 Event taxonomy',
    triggers: ['analytics', 'tracking plan', 'ga4', 'mixpanel', 'amplitude'],
    antiPatternFile: 'anti-pattern.md §9.5',
    faqFile: 'faq.md §9.5'
  },
  {
    id: 'mkt-ab-testing',
    slug: 'ab-testing',
    legacySlug: 'ab-test-setup',
    name: 'ab-testing',
    title: 'A/B Testing',
    category: 'measurement',
    description:
      'Hypothesis-driven experimentation. Power analysis, sample size, sequential testing, multi-armed bandits, attribution-aware analysis.',
    knowledgeFile: 'best-practice.md',
    section: '§8.1 Experiment design',
    triggers: ['ab test', 'a/b test', 'split test', 'experiment'],
    antiPatternFile: 'anti-pattern.md §9.5.1',
    faqFile: 'faq.md §9.5'
  },

  // ─── Retention ─────────────────────────────────────────────────────────────
  {
    id: 'mkt-churn-prevention',
    slug: 'churn-prevention',
    name: 'churn-prevention',
    title: 'Churn Prevention',
    category: 'retention',
    description:
      'Predictive churn modeling, tiered save offers, dunning sequences (Day 0/3/7/14/21), pause subscriptions, win-back flows.',
    knowledgeFile: 'best-practice.md',
    section: '§7.1 Cancel flows + dunning + save offers',
    triggers: ['churn', 'churn prevention', 'cancel flow', 'retention', 'dunning'],
    antiPatternFile: 'anti-pattern.md §9.6',
    faqFile: 'faq.md §9.6'
  },

  // ─── Growth Engineering ────────────────────────────────────────────────────
  {
    id: 'mkt-co-marketing',
    slug: 'co-marketing',
    name: 'co-marketing',
    title: 'Co-Marketing',
    category: 'growth',
    description:
      'Joint content, cross-promo, shared webinars. ICP overlap test, partner tier, UTM tracking, pipeline attribution.',
    knowledgeFile: 'best-practice.md',
    section: '§9.1 Partner ID + joint campaigns',
    triggers: ['co-marketing', 'joint webinar', 'partnership marketing'],
    antiPatternFile: 'anti-pattern.md §9.7.3',
    faqFile: 'faq.md §9.7'
  },
  {
    id: 'mkt-free-tools',
    slug: 'free-tools',
    legacySlug: 'free-tool-strategy',
    name: 'free-tools',
    title: 'Free Tools',
    category: 'growth',
    description:
      'Calculator / Grader / Generator as lead-gen. Solves real problem, shareable output, optional email gate, embed widget for viral loop.',
    knowledgeFile: 'architecture.md',
    section: '§4.7.1 Tool-as-lead-gen',
    triggers: ['free tool', 'calculator', 'grader', 'lead magnet tool'],
    antiPatternFile: 'anti-pattern.md §9.7.1',
    faqFile: 'faq.md §9.7'
  },
  {
    id: 'mkt-referrals',
    slug: 'referrals',
    legacySlug: 'referral-program',
    name: 'referrals',
    title: 'Referral Program',
    category: 'growth',
    description:
      'Double-sided incentives, fraud guardrails (device + payment + IP matching), tier system, payout (account credit preferred).',
    knowledgeFile: 'best-practice.md',
    section: '§9.3 Double-sided incentives',
    triggers: ['referral', 'referral program', 'affiliate', 'word of mouth'],
    antiPatternFile: 'anti-pattern.md §9.7.2',
    faqFile: 'faq.md §9.7'
  },

  // ─── Strategy & Monetization ───────────────────────────────────────────────
  {
    id: 'mkt-marketing-ideas',
    slug: 'marketing-ideas',
    name: 'marketing-ideas',
    title: '140 SaaS Marketing Ideas',
    category: 'strategy',
    description:
      'Curated catalog of marketing tactics: SEO, paid, content, partnerships, community, programmatic, free tools, PR.',
    knowledgeFile: 'best-practice.md',
    section: '§10.1 140 SaaS marketing ideas',
    triggers: ['marketing ideas', 'marketing tactics', 'growth tactics'],
    antiPatternFile: 'anti-pattern.md §9.8',
    faqFile: 'faq.md §9.8'
  },
  {
    id: 'mkt-launch',
    slug: 'launch',
    legacySlug: 'launch-strategy',
    name: 'launch',
    title: 'Launch Strategy',
    category: 'strategy',
    description:
      'Pre-launch (waitlist, PR list, content backlog), launch week (Product Hunt, multi-channel blast), post-launch (retention focus).',
    knowledgeFile: 'best-practice.md',
    section: '§10.3 Pre/launch/post phases',
    triggers: ['launch', 'product launch', 'launch strategy'],
    antiPatternFile: 'anti-pattern.md §9.8.2',
    faqFile: 'faq.md §9.8'
  },
  {
    id: 'mkt-pricing',
    slug: 'pricing',
    legacySlug: 'pricing-strategy',
    name: 'pricing',
    title: 'Pricing Strategy',
    category: 'strategy',
    description:
      'Value-based pricing, 3-tier structure, annual discount positioning, free trial vs freemium, international pricing (PPP).',
    knowledgeFile: 'best-practice.md',
    section: '§10.4 Value-based pricing',
    triggers: ['pricing', 'pricing strategy', 'pricing page', 'tier pricing'],
    antiPatternFile: 'anti-pattern.md §9.8.1',
    faqFile: 'faq.md §9.8'
  },

  // ─── Sales & RevOps ────────────────────────────────────────────────────────
  {
    id: 'mkt-revops',
    slug: 'revops',
    name: 'revops',
    title: 'RevOps',
    category: 'sales',
    description:
      'Lead lifecycle (Subscriber → MQL → SQL → Opp → Customer), scoring model, routing rules, SLAs, funnel reporting.',
    knowledgeFile: 'architecture.md',
    section: '§4.9.1 Lead lifecycle + scoring',
    triggers: ['revops', 'lead scoring', 'lead lifecycle', 'mql', 'sql'],
    antiPatternFile: 'anti-pattern.md §9.9.1',
    faqFile: 'faq.md §9.9'
  },
  {
    id: 'mkt-prospecting',
    slug: 'prospecting',
    name: 'prospecting',
    title: 'Prospecting',
    category: 'sales',
    description:
      'ICP definition, list-building, enrichment, multi-channel sequences. Personalization with trigger events, reply handling.',
    knowledgeFile: 'best-practice.md',
    section: '§11.2 ICP + multi-channel touch',
    triggers: ['prospecting', 'outbound', 'cold call', 'sales sequence'],
    antiPatternFile: 'anti-pattern.md §9.9.5',
    faqFile: 'faq.md §9.9'
  },
  {
    id: 'mkt-pr',
    slug: 'public-relations',
    name: 'public-relations',
    title: 'Public Relations',
    category: 'sales',
    description:
      'Earned media, journalist outreach, HARO/Connectively, tier-1 media list, press kit, coverage tracking.',
    knowledgeFile: 'best-practice.md',
    section: '§11.3 Earned media + HARO',
    triggers: ['pr', 'public relations', 'press release', 'media pitch', 'haro'],
    antiPatternFile: 'anti-pattern.md §9.9.6',
    faqFile: 'faq.md §9.9'
  },
  {
    id: 'mkt-customer-research',
    slug: 'customer-research',
    name: 'customer-research',
    title: 'Customer Research',
    category: 'sales',
    description:
      'User interview guide, sampling mix (activated + churned + never-active), JTBD synthesis, quarterly insight report.',
    knowledgeFile: 'best-practice.md',
    section: '§11.5 Interview synthesis + JTBD',
    triggers: ['customer research', 'user interview', 'jtbd', 'jobs to be done'],
    antiPatternFile: 'anti-pattern.md §9.9.7',
    faqFile: 'faq.md §9.9'
  },
  {
    id: 'mkt-marketing-loops',
    slug: 'marketing-loops',
    name: 'marketing-loops',
    title: 'Marketing Loops',
    category: 'sales',
    description:
      'Recurring agent workflows: content, SEO, outreach, retention loops. Stateful agents with persistence, halt conditions, observability.',
    knowledgeFile: 'architecture.md',
    section: '§4.9.8 Recurring agent workflows',
    triggers: ['marketing loops', 'recurring agent', 'marketing workflow'],
    antiPatternFile: 'anti-pattern.md §9.9.9',
    faqFile: 'faq.md §9.9'
  },
  {
    id: 'mkt-product-marketing',
    slug: 'product-marketing',
    legacySlug: 'product-marketing-context',
    name: 'product-marketing',
    title: 'Product Marketing Context',
    category: 'sales',
    description:
      'Single source of truth for product/audience/positioning. MANDATORY first read for all marketing skills. Stored at .agents/product-marketing.md.',
    knowledgeFile: 'glossary.md',
    section: '§13 Product-Marketing Context template',
    triggers: ['product marketing', 'product context', 'icp'],
    antiPatternFile: 'anti-pattern.md §9.9.8',
    faqFile: 'faq.md §9.9'
  }
]

// ────────────────────────────────────────────────────────────────────────────
// Aggregations
// ────────────────────────────────────────────────────────────────────────────

export const CATALOG: FrameworkItem[] = [...RULES, ...SKILLS, ...AGENTS]

export const MARKETING_CATALOG: MarketingSkillRef[] = MARKETING_CONCEPT_REFS

export function countByType(): { rules: number; skills: number; agents: number; marketing: number } {
  return {
    rules: RULES.length,
    skills: SKILLS.length,
    agents: AGENTS.length,
    marketing: MARKETING_CONCEPT_REFS.length
  }
}

export function categoriesForType(type: FrameworkItemType): string[] {
  const set = new Set<string>()
  CATALOG.filter((i) => i.type === type).forEach((i) => set.add(i.category))
  return Array.from(set)
}
