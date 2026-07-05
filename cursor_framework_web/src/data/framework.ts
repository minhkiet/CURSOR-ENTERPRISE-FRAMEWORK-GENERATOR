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
    path: '.cursor/rules/karpathy-guidelines.mdc',
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
    path: '.cursor/rules/coding-standards.mdc'
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
    path: '.cursor/rules/intent-detection.mdc'
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
    path: '.cursor/rules/context-router.mdc',
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
    path: '.cursor/rules/memory-first.mdc'
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
    path: '.cursor/rules/task-analyzer.mdc'
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
    path: '.cursor/rules/multi-language-processing.mdc'
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
    path: '.cursor/rules/skill-integration.mdc'
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
    path: '.cursor/rules/skill-registry.mdc'
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
    path: '.cursor/rules/architecture-patterns.mdc',
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
    path: '.cursor/rules/enterprise-patterns.mdc'
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
    path: '.cursor/rules/frontend-frameworks.mdc'
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
    path: '.cursor/rules/backend-frameworks.mdc'
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
    path: '.cursor/rules/api-patterns.mdc'
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
    path: '.cursor/rules/auth.mdc'
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
    path: '.cursor/rules/multi-tenant.mdc'
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
    path: '.cursor/rules/databases.mdc'
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
    path: '.cursor/rules/redis.mdc'
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
    path: '.cursor/rules/supabase.mdc'
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
    path: '.cursor/rules/security.mdc'
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
    path: '.cursor/rules/performance.mdc'
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
    path: '.cursor/rules/container-orchestration.mdc'
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
    path: '.cursor/rules/cloud-providers.mdc'
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
    path: '.cursor/rules/cloud-infra.mdc'
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
    path: '.cursor/rules/serverless.mdc'
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
    path: '.cursor/rules/cloudflare.mdc'
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
    path: '.cursor/rules/deployment.mdc'
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
    path: '.cursor/rules/version-control.mdc'
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
    path: '.cursor/rules/observability.mdc'
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
    path: '.cursor/rules/operations.mdc'
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
    path: '.cursor/rules/workflow-engines.mdc'
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
    path: '.cursor/rules/vibe-code-protocol.mdc'
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
    path: '.cursor/rules/billing.mdc'
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
    path: '.cursor/rules/chatbot-development.mdc'
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
    path: '.cursor/rules/crm-saas.mdc'
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
    path: '.cursor/rules/ui-visual-design.mdc'
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
    path: '.cursor/rules/ai-knowledge.mdc'
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
    path: '.cursor/rules/llm-providers.mdc'
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
    path: '.cursor/rules/testing.mdc'
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
    path: '.cursor/rules/cost-optimization.mdc'
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
    path: '.cursor/skills/karpathy-coding/SKILL.md',
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
    path: '.cursor/skills/ponytail/SKILL.md',
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
    path: '.cursor/skills/full-output/SKILL.md',
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
    path: '.cursor/skills/frontend-taste/SKILL.md',
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
    path: '.cursor/skills/frontend-review/SKILL.md',
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
    path: '.cursor/skills/frontend-redesign/SKILL.md',
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
    path: '.cursor/skills/security-review/SKILL.md',
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
    path: '.cursor/skills/vietnam-payment-review/SKILL.md',
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
    path: '.cursor/skills/vietnam-address/SKILL.md'
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
    path: '.cursor/skills/bazi/SKILL.md'
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
    path: '.cursor/skills/document-ocr/SKILL.md'
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
    path: '.cursor/skills/weknora-kb/SKILL.md'
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
    path: '.cursor/skills/weknora-agent/SKILL.md'
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
    path: '.cursor/skills/video-generation/SKILL.md'
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
    path: '.cursor/skills/pixelrag/SKILL.md'
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
    path: '.cursor/skills/visual-explainer/SKILL.md'
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
    path: '.cursor/skills/open-design/SKILL.md'
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
    path: '.cursor/skills/skill-installer/SKILL.md'
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
    alignsWith: ['.cursor/rules/coding-standards.mdc', '.cursor/rules/karpathy-guidelines.mdc']
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
    alignsWith: ['.cursor/rules/api-patterns.mdc', '.cursor/rules/auth.mdc']
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
    alignsWith: ['.cursor/rules/backend-frameworks.mdc', '.cursor/rules/api-patterns.mdc']
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
    alignsWith: ['.cursor/rules/frontend-frameworks.mdc', '.cursor/rules/ui-visual-design.mdc']
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
    alignsWith: ['.cursor/rules/databases.mdc', '.cursor/rules/redis.mdc']
  },
  {
    id: 'security-auditor',
    type: 'agent',
    name: 'security-auditor',
    title: 'Security Auditor',
    subtitle: 'OWASP Top 10 · STRIDE · supply-chain',
    description:
      'Security engineer: assumes breach, verifies defense. Audits auth, secrets, input validation, API security, dependency tree. Cites OWASP Top 10 for every finding.',
    category: 'Security',
    tags: ['owasp', 'secrets', 'auth', 'payment'],
    role: 'secondary',
    trigger: '/security',
    path: '.cursor/agents/security-auditor.md',
    bullets: [
      'Five layers: auth, input validation, data, API, supply chain',
      'OWASP Top 10 (2021) — A01 Broken Access Control → A10 SSRF',
      'Pre-deploy gate · runs after any CVE announcement'
    ],
    alignsWith: ['.cursor/rules/security.mdc', '.cursor/rules/auth.mdc']
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
    alignsWith: ['.cursor/rules/testing.mdc']
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
    alignsWith: ['.cursor/rules/performance.mdc']
  }
]

// ────────────────────────────────────────────────────────────────────────────
// Aggregations
// ────────────────────────────────────────────────────────────────────────────

export const CATALOG: FrameworkItem[] = [...RULES, ...SKILLS, ...AGENTS]

export function countByType(): { rules: number; skills: number; agents: number } {
  return {
    rules: RULES.length,
    skills: SKILLS.length,
    agents: AGENTS.length
  }
}

export function categoriesForType(type: FrameworkItemType): string[] {
  const set = new Set<string>()
  CATALOG.filter((i) => i.type === type).forEach((i) => set.add(i.category))
  return Array.from(set)
}
