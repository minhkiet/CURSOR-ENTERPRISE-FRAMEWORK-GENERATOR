"""
Context Router Module

Provides intelligent context routing based on intent classification and skill matching.
Implements the Context Router principle from the Cursor Enterprise Framework.

Features:
    - Intent classification using keyword matching and semantic analysis
    - Skill routing with confidence scoring
    - Multi-stage routing for complex requests
    - Fallback hierarchy for graceful degradation

Usage:
    >>> from cursor_framework import ContextRouter
    >>> router = ContextRouter()
    >>> route = router.route("Create a landing page for SaaS product")
    >>> print(route.skill)
    'frontend-taste'
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import re


class IntentType(Enum):
    """Enumeration of possible intent types."""

    CODE_GENERATION = "code_generation"
    DEBUGGING = "debugging"
    REFACTORING = "refactoring"
    DOCUMENTATION = "documentation"
    EXPLANATION = "explanation"
    REVIEW = "review"
    SECURITY_AUDIT = "security_audit"
    DESIGN = "design"
    DEPLOYMENT = "deployment"
    MARKETING_PLANNING = "marketing_planning"
    MARKETING_EXECUTION = "marketing_execution"
    GENERAL = "general"


class Domain(Enum):
    """Enumeration of technical domains."""

    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASE = "database"
    DEVOPS = "devops"
    SECURITY = "security"
    API = "api"
    MOBILE = "mobile"
    AI_ML = "ai_ml"
    INFRASTRUCTURE = "infrastructure"
    MARKETING = "marketing"
    GENERAL = "general"


class Skill(Enum):
    """Available skills in the framework."""

    FRONTEND_TASTE = "frontend-taste"
    FRONTEND_REDESIGN = "frontend-redesign"
    FRONTEND_REVIEW = "frontend-review"
    FULL_OUTPUT = "full-output"
    SECURITY_REVIEW = "security-review"
    VIETNAM_PAYMENT_REVIEW = "vietnam-payment-review"
    CODE_REVIEW = "code-review"
    TESTING_STRATEGY = "testing-strategy"
    PERFORMANCE_AUDIT = "performance-audit"
    DDD_DESIGN = "ddd-design"
    CLEAN_ARCHITECTURE = "clean-architecture"
    MICROSERVICE_DESIGN = "microservice-design"
    DATABASE_OPTIMIZATION = "database-optimization"
    RAG_BUILDER = "rag-builder"
    VECTOR_SEARCH_REVIEW = "vector-search-review"
    # Marketing concept-ref (47 marketingskills → existing knowledge files, see
    # .cursor/rules/skill-registry.mdc §9). One umbrella Skill enum value because
    # the concept-ref pattern doesn't create per-skill files — Agent routes
    # within the umbrella via knowledge/marketing/decision-tree.md §11.
    MARKETING = "marketing"
    # ── Agents (sync 2026-07-15) ── 10 specialized agents registered as
    # routable skills. Each maps to .cursor/agents/{name}.md. The router
    # dispatches user intent keywords → agent via SKILL_TRIGGERS below;
    # the actual behavior is governed by each agent's profile.
    DEBUGGER = "debugger"
    UI_DESIGNER = "ui-designer"
    WEB_CLONER = "web-cloner"
    WEB_SCRAPER = "web-scraper"
    REFACTOR_SPECIALIST = "refactor-specialist"
    DEPLOYMENT_ENGINEER = "deployment-engineer"
    MIGRATION_SPECIALIST = "migration-specialist"
    DOC_WRITER = "doc-writer"
    DEVOPS_ENGINEER = "devops-engineer"
    MARKETING_STRATEGIST = "marketing-strategist"


@dataclass
class SkillRoute:
    """Represents a routing decision with metadata."""

    skill: Skill
    confidence: float
    intent: IntentType
    domain: Domain
    reasoning: str
    alternatives: list["SkillRoute"] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class RoutingRequest:
    """Represents an incoming routing request."""

    text: str
    context: dict = field(default_factory=dict)
    session_id: Optional[str] = None
    project_path: Optional[str] = None


class IntentClassifier:
    """
    Classifies user intent from request text.

    Uses keyword matching and pattern recognition to determine
    the primary intent and domain of a request.
    """

    # Intent keywords mapping
    INTENT_KEYWORDS = {
        IntentType.CODE_GENERATION: [
            "create", "build", "implement", "generate", "write", "add",
            "make", "develop", "construct", "new", "implement"
        ],
        IntentType.DEBUGGING: [
            "fix", "bug", "error", "issue", "problem", "debug", "not working",
            "broken", "failed", "crash", "exception", "stack trace"
        ],
        IntentType.REFACTORING: [
            "refactor", "restructure", "reorganize", "improve", "optimize code",
            "clean up", "simplify", "extract", "rename"
        ],
        IntentType.DOCUMENTATION: [
            "document", "docs", "comment", "explain", "readme", "api doc",
            "specification", "describe"
        ],
        IntentType.REVIEW: [
            "review", "audit", "check", "quality", "assess", "evaluate",
            "inspect", "analyze"
        ],
        IntentType.SECURITY_AUDIT: [
            "security", "vulnerability", "penetration", "owasp", "xss", "injection",
            "csrf", "authentication", "authorization", "encrypt", "secure"
        ],
        IntentType.DESIGN: [
            "design", "layout", "ui", "ux", "interface", "component", "landing",
            "redesign", "modernize", "upgrade"
        ],
        IntentType.DEPLOYMENT: [
            "deploy", "release", "publish", "push", "ship", "production",
            "staging", "ci/cd", "pipeline"
        ],
        # Marketing intents (sync 2026-07-15 with marketingskills repo).
        # Distinguish planning vs execution so the agent can route to
        # `.cursor/knowledge/marketing/decision-tree.md §11` accordingly.
        IntentType.MARKETING_PLANNING: [
            "marketing plan", "go-to-market", "gtm", "quarterly plan",
            "marketing strategy", "launch strategy", "launch plan",
            "positioning", "icp", "ideal customer profile",
            "marketing research", "competitor research", "competitive analysis",
            "audience research", "customer research", "jtbd",
            "marketing brainstorm", "marketing council", "tactic catalog"
        ],
        IntentType.MARKETING_EXECUTION: [
            "cro", "conversion rate", "optimize conversion", "ab test", "a/b test",
            "split test", "cold email", "outreach", "cold outreach", "prospecting",
            "seo audit", "programmatic seo", "schema markup", "structured data",
            "llms.txt", "ai seo", "llmo", "aso", "app store",
            "ads", "google ads", "meta ads", "facebook ads", "linkedin ads",
            "ad creative", "creative testing",
            "email sequence", "newsletter", "drip", "sms marketing",
            "paywall", "churn prevention", "dunning",
            "referral", "co-marketing", "free tool",
            "pricing", "pricing strategy", "tier",
            "pr pitch", "media pitch", "haro",
            "directory submission", "marketing loop"
        ],
    }

    # Domain keywords mapping
    DOMAIN_KEYWORDS = {
        Domain.FRONTEND: [
            "frontend", "react", "vue", "angular", "html", "css", "javascript",
            "typescript", "ui", "ux", "landing", "page", "component", "button",
            "tailwind", "nextjs", "nuxt", "svelte", "tailwind", "css"
        ],
        Domain.BACKEND: [
            "backend", "server", "api", "endpoint", "route", "controller",
            "service", "middleware", "express", "fastapi", "django", "spring"
        ],
        Domain.DATABASE: [
            "database", "db", "sql", "query", "table", "schema", "migration",
            "postgresql", "mysql", "mongodb", "redis", "index", "join"
        ],
        Domain.DEVOPS: [
            "docker", "kubernetes", "ci/cd", "pipeline", "deploy", "container",
            "helm", "terraform", "ansible", "cloud", "aws", "azure", "gcp"
        ],
        Domain.SECURITY: [
            "security", "auth", "jwt", "oauth", "password", "encrypt", "token",
            "permission", "vulnerability", "cors", "csrf", "xss"
        ],
        Domain.API: [
            "api", "rest", "graphql", "grpc", "endpoint", "webhook", "http",
            "request", "response", "json", "xml"
        ],
        Domain.AI_ML: [
            "ai", "ml", "llm", "openai", "claude", "gemini", "gpt", "embedding",
            "rag", "vector", "prompt", "token", "model"
        ],
        Domain.MARKETING: [
            # 9 marketingskills categories → umbrella Domain.MARKETING
            "marketing", "growth", "cro", "conversion", "signup", "onboarding",
            "popup", "paywall", "copywriting", "cold email", "newsletter",
            "sms marketing", "social content", "seo", "programmatic seo",
            "ai seo", "schema", "aso", "paid ads", "google ads", "meta ads",
            "facebook ads", "linkedin ads", "ad creative", "ab test",
            "a/b test", "split test", "analytics", "tracking plan",
            "churn", "retention", "dunning", "co-marketing", "free tool",
            "referral", "launch", "pricing", "offer", "revops", "lead scoring",
            "mql", "sql", "prospecting", "outbound", "pr", "press release",
            "haro", "directory submission", "customer research", "jtbd",
            "marketing loop", "icp", "positioning"
        ],
    }

    def __init__(self):
        """Initialize the intent classifier."""
        self._compiled_patterns: dict = {}

    def classify_intent(self, text: str) -> tuple[IntentType, float]:
        """
        Classify the intent from request text.

        Args:
            text: The request text to analyze

        Returns:
            Tuple of (IntentType, confidence_score)
        """
        text_lower = text.lower()
        scores: dict[IntentType, int] = {intent: 0 for intent in IntentType}

        for intent, keywords in self.INTENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[intent] += 1

        if not any(scores.values()):
            return IntentType.GENERAL, 0.5

        best_intent = max(scores, key=scores.get)
        max_score = scores[best_intent]
        confidence = min(0.95, 0.5 + (max_score * 0.15))

        return best_intent, confidence

    def classify_domain(self, text: str) -> tuple[Domain, float]:
        """
        Classify the technical domain from request text.

        Args:
            text: The request text to analyze

        Returns:
            Tuple of (Domain, confidence_score)
        """
        text_lower = text.lower()
        scores: dict[Domain, int] = {domain: 0 for domain in Domain}

        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[domain] += 1

        if not any(scores.values()):
            return Domain.GENERAL, 0.5

        best_domain = max(scores, key=scores.get)
        max_score = scores[best_domain]
        confidence = min(0.95, 0.5 + (max_score * 0.1))

        return best_domain, confidence


class ContextRouter:
    """
    Main context router that handles skill routing.

    Implements the Context Router principle by analyzing requests
    and routing them to appropriate skills based on intent and domain.
    """

    # Skill trigger keywords
    SKILL_TRIGGERS = {
        Skill.FRONTEND_TASTE: [
            "landing page", "portfolio", "landing", "homepage", "marketing site",
            "minimalist", "awwwards", "apple-y", "linear-style", "brutalist",
            "editorial", "greenfield frontend"
        ],
        Skill.FRONTEND_REDESIGN: [
            "redesign", "upgrade", "improve existing", "modernize", "redesign site",
            "redesign app", "improve current"
        ],
        Skill.FRONTEND_REVIEW: [
            "review", "quality check", "audit ui", "taste check", "review quality"
        ],
        Skill.FULL_OUTPUT: [
            "full implementation", "complete", "not skeleton", "no todo",
            "multiple files", "all files", "full code"
        ],
        Skill.SECURITY_REVIEW: [
            "security", "vulnerability", "penetration test", "owasp", "xss",
            "sql injection", "ssrf", "csrf", "authentication", "authorization",
            "apk decompile", "binary analysis", "prompt injection"
        ],
        Skill.VIETNAM_PAYMENT_REVIEW: [
            "momo", "sepay", "ayos", "vietqr", "zalo", "payos", "vnpay",
            "vietnam payment", "payment integration", "webhook thanh toan"
        ],
        Skill.CODE_REVIEW: [
            "code review", "pull request", "pr review", "merge check"
        ],
        Skill.TESTING_STRATEGY: [
            "test", "testing", "unit test", "e2e", "integration test"
        ],
        Skill.PERFORMANCE_AUDIT: [
            "performance", "optimize speed", "slow", "latency", "bundle size"
        ],
        # Marketing umbrella — 47 marketingskills concept-refs are routed
        # within MARKETING via `.cursor/knowledge/marketing/decision-tree.md §11`
        # (no per-skill SKILL.md files; see skill-registry.mdc §9).
        Skill.MARKETING: [
            "marketing", "growth", "cro", "conversion rate", "conversion",
            "signup", "sign-up", "register", "onboarding", "activation",
            "popup", "pop-up", "modal", "exit-intent", "paywall",
            "upgrade flow", "trial expiration",
            "copywriting", "copy editing", "cold email", "outreach",
            "email sequence", "newsletter", "drip campaign", "lifecycle email",
            "sms marketing", "tcpa", "social content", "social post",
            "instagram", "linkedin post", "tiktok script",
            "image gen", "ai image", "dall-e", "midjourney",
            "video script", "video marketing",
            "seo", "seo audit", "technical seo", "ai seo", "llmo", "geo", "aeo",
            "llms.txt", "programmatic seo", "schema markup", "json-ld",
            "rich snippets", "structured data", "aso", "app store optimization",
            "site architecture", "information architecture", "url structure",
            "competitor page", "comparison page", "vs page", "alternatives page",
            "paid ads", "google ads", "meta ads", "facebook ads", "linkedin ads",
            "ad creative", "ad copy", "creative testing",
            "analytics", "tracking plan", "event tracking", "ga4", "mixpanel",
            "ab test", "a/b test", "split test", "experiment",
            "churn", "churn prevention", "cancel flow", "retention", "dunning",
            "co-marketing", "joint webinar", "partnership marketing",
            "free tool", "calculator", "grader", "lead magnet tool",
            "referral", "referral program", "affiliate",
            "marketing ideas", "marketing tactics", "growth tactics",
            "marketing psychology", "mental models", "loss aversion", "social proof",
            "marketing plan", "quarterly plan", "go-to-market", "gtm",
            "launch", "product launch", "launch strategy",
            "pricing", "pricing strategy", "pricing page", "tier pricing",
            "offer", "offer construction", "value equation", "guarantee",
            "revops", "lead scoring", "lead lifecycle", "mql", "sql",
            "sales enablement", "sales deck", "pitch deck", "one-pager",
            "prospecting", "outbound", "cold call", "sales sequence",
            "public relations", "press release", "media pitch", "haro",
            "pr campaign", "pr strategy", "pr outreach",
            "directory submission", "directory listing", "saas directories",
            "customer research", "user interview", "jtbd", "jobs to be done",
            "competitor", "competitor profiling", "battlecard", "positioning",
            "marketing council", "marketing brainstorm", "multi-persona",
            "marketing loops", "recurring agent", "marketing workflow",
            "product marketing", "product context", "icp",
            "marketing research", "marketing strategy"
        ],
        # ── Agent skill triggers (sync 2026-07-15) ──
        # Each agent routes via compact trigger set; long-tail variants live
        # in skill_discovery.py so context_router stays lean.
        Skill.DEBUGGER: [
            "debug", "bug", "fix bug", "fix error", "repro", "reproduce",
            "root cause", "intermittent", "stack trace", "exception",
            "fix lỗi", "sửa lỗi", "lỗi", "bug report", "/debug", "/fix"
        ],
        Skill.UI_DESIGNER: [
            "design ui", "ui design", "ux", "design system",
            "design tokens", "component spec", "redesign",
            "thiết kế ui", "thiết kế giao diện", "wireframe",
            "mockup", "landing page design", "/design", "/ui"
        ],
        Skill.WEB_CLONER: [
            "clone", "copy website", "mirror", "replicate site",
            "clone web", "copy site", "sao chép web",
            "/clone", "/copy", "/mirror"
        ],
        Skill.WEB_SCRAPER: [
            "scrape", "extract", "crawl", "fetch docs",
            "scrape web", "lấy nội dung", "trích xuất",
            "/scrape", "/extract", "/docs",
            "pull documentation", "scrape article"
        ],
        Skill.REFACTOR_SPECIALIST: [
            "refactor", "cleanup", "code smell", "tech debt",
            "extract function", "rename",
            "refactor code", "dọn dẹp code", "/refactor"
        ],
        Skill.DEPLOYMENT_ENGINEER: [
            "deploy", "release", "ship", "rollout", "production deploy",
            "canary", "blue green", "deploy to prod",
            "triển khai", "release phiên bản",
            "/deploy", "/release", "/ship"
        ],
        Skill.MIGRATION_SPECIALIST: [
            "migrate", "migration", "schema change", "backfill",
            "add column", "drop column", "rename column",
            "data migration", "framework upgrade",
            "/migrate", "di trú", "migration script"
        ],
        Skill.DOC_WRITER: [
            "write docs", "readme", "documentation", "adr",
            "runbook", "tutorial", "api reference",
            "viết tài liệu",
            "/doc", "/readme", "/adr", "/runbook"
        ],
        Skill.DEVOPS_ENGINEER: [
            "ci", "cd", "pipeline", "infrastructure", "iac",
            "terraform", "kubernetes", "docker",
            "ci/cd", "build pipeline", "/build", "container"
        ],
        Skill.MARKETING_STRATEGIST: [
            "marketing", "growth", "positioning", "funnel",
            "cro strategy", "seo strategy", "paid ads",
            "retention strategy", "churn", "pricing strategy",
            "launch strategy", "growth strategy",
            "chiến lược marketing", "/marketing", "/growth"
        ],
    }

    # Skill combination rules
    SKILL_COMBINATIONS = {
        "landing_page": [Skill.FRONTEND_TASTE, Skill.FULL_OUTPUT, Skill.FRONTEND_REVIEW],
        "redesign": [Skill.FRONTEND_REDESIGN, Skill.FULL_OUTPUT, Skill.FRONTEND_REVIEW],
        "frontend_review": [Skill.FRONTEND_REVIEW],
        "multi_file": [Skill.FULL_OUTPUT, Skill.FRONTEND_REVIEW],
        "security_task": [Skill.SECURITY_REVIEW],
        "payment_task": [Skill.VIETNAM_PAYMENT_REVIEW, Skill.SECURITY_REVIEW],
        # Marketing combinations — when user request hits marketing umbrella,
        # these secondary skills may be added by the agent:
        #   - FULL_OUTPUT (if build request)
        #   - karpathy-coding overlay (mandatory for any code-generating marketing task)
        "marketing_task": [Skill.MARKETING],
        "marketing_build": [Skill.MARKETING, Skill.FULL_OUTPUT],
        # ── Agent combinations (sync 2026-07-15) ──
        # When multiple agents collaborate, list primary + supporting.
        "debug_fix": [Skill.DEBUGGER],
        "design_system": [Skill.UI_DESIGNER, Skill.FULL_OUTPUT],
        "clone_site": [Skill.WEB_CLONER],
        "extract_content": [Skill.WEB_SCRAPER],
        "refactor_code": [Skill.REFACTOR_SPECIALIST, Skill.FULL_OUTPUT],
        "deploy_release": [Skill.DEPLOYMENT_ENGINEER],
        "db_migration": [Skill.MIGRATION_SPECIALIST, Skill.DEPLOYMENT_ENGINEER],
        "write_docs": [Skill.DOC_WRITER],
        "infra_change": [Skill.DEVOPS_ENGINEER, Skill.DEPLOYMENT_ENGINEER],
        "marketing_strategy": [Skill.MARKETING_STRATEGIST, Skill.MARKETING],
        # Priority composition sets — when multiple agents could apply (e.g., UI
        # design + frontend-taste), the agent listed first takes routing
        # precedence; secondary is invoked via SKILL_COMBINATIONS only.
        "ui_design_priority": [Skill.UI_DESIGNER, Skill.FRONTEND_TASTE, Skill.FRONTEND_REVIEW],
    }

    def __init__(self):
        """Initialize the context router."""
        self.classifier = IntentClassifier()
        self._routing_history: list[SkillRoute] = []

    def route(self, request: str | RoutingRequest) -> SkillRoute:
        """
        Route a request to the appropriate skill.

        Args:
            request: The request text or RoutingRequest object

        Returns:
            SkillRoute with routing decision and metadata
        """
        if isinstance(request, str):
            request = RoutingRequest(text=request)

        intent, intent_confidence = self.classifier.classify_intent(request.text)
        domain, domain_confidence = self.classifier.classify_domain(request.text)

        skill = self._determine_skill(request.text, intent, domain)
        confidence = self._calculate_confidence(intent_confidence, domain_confidence, skill)

        route = SkillRoute(
            skill=skill,
            confidence=confidence,
            intent=intent,
            domain=domain,
            reasoning=self._generate_reasoning(intent, domain, skill, intent_confidence, domain_confidence),
            alternatives=self._get_alternatives(skill),
            metadata={
                "intent_confidence": intent_confidence,
                "domain_confidence": domain_confidence,
            },
        )

        self._routing_history.append(route)
        return route

    def route_multi_skill(self, request: str | RoutingRequest) -> list[SkillRoute]:
        """
        Route a request to multiple skills when combination is needed.

        Args:
            request: The request text or RoutingRequest object

        Returns:
            List of SkillRoute objects for combined skills
        """
        primary_route = self.route(request)
        routes = [primary_route]

        text = request.text if isinstance(request, str) else request.text.lower()

        if any(kw in text for kw in ["landing", "portfolio", "greenfield"]):
            routes.extend([self._create_route(s) for s in [Skill.FULL_OUTPUT, Skill.FRONTEND_REVIEW]])

        if any(kw in text for kw in ["redesign", "upgrade", "improve existing"]):
            routes.extend([self._create_route(s) for s in [Skill.FULL_OUTPUT, Skill.FRONTEND_REVIEW]])

        if any(kw in text for kw in ["momo", "sepay", "vietqr", "payment"]):
            routes.extend([self._create_route(s) for s in [Skill.SECURITY_REVIEW]])

        return routes

    def _determine_skill(
        self, text: str, intent: IntentType, domain: Domain
    ) -> Skill:
        """Determine the primary skill based on text and classifications."""
        text_lower = text.lower()

        for skill, triggers in self.SKILL_TRIGGERS.items():
            for trigger in triggers:
                if trigger in text_lower:
                    return skill

        if domain == Domain.FRONTEND and intent == IntentType.DESIGN:
            return Skill.FRONTEND_TASTE
        elif domain == Domain.FRONTEND and intent == IntentType.REVIEW:
            return Skill.FRONTEND_REVIEW
        elif intent == IntentType.SECURITY_AUDIT:
            return Skill.SECURITY_REVIEW
        elif intent == IntentType.CODE_GENERATION:
            return Skill.FULL_OUTPUT
        else:
            return Skill.CODE_REVIEW

    def _calculate_confidence(
        self, intent_conf: float, domain_conf: float, skill: Skill
    ) -> float:
        """Calculate overall routing confidence."""
        return min(0.99, (intent_conf + domain_conf) / 2 + 0.2)

    def _generate_reasoning(
        self, intent: IntentType, domain: Domain, skill: Skill,
        intent_conf: float = 0.0, domain_conf: float = 0.0
    ) -> str:
        """Generate reasoning text for the routing decision."""
        return (
            f"Intent: {intent.value} ({intent_conf:.2f}), "
            f"Domain: {domain.value} ({domain_conf:.2f}), "
            f"Matched to: {skill.value}"
        )

    def _get_alternatives(self, primary: Skill) -> list[SkillRoute]:
        """Get alternative routing options."""
        alternatives = []
        for skill in Skill:
            if skill != primary:
                alternatives.append(
                    SkillRoute(
                        skill=skill,
                        confidence=0.3,
                        intent=IntentType.GENERAL,
                        domain=Domain.GENERAL,
                        reasoning=f"Alternative: {skill.value}",
                    )
                )
        return alternatives[:3]

    def _create_route(self, skill: Skill) -> SkillRoute:
        """Create a route for a specific skill."""
        return SkillRoute(
            skill=skill,
            confidence=0.8,
            intent=IntentType.CODE_GENERATION,
            domain=Domain.FRONTEND,
            reasoning=f"Combined skill: {skill.value}",
        )

    def get_routing_history(self) -> list[SkillRoute]:
        """Get the routing history."""
        return self._routing_history.copy()


def create_router() -> ContextRouter:
    """Factory function to create a configured ContextRouter."""
    return ContextRouter()
