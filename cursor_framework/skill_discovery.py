"""
Skill Discovery Module

Implements automatic skill detection and loading for the framework.
Supports pre-review and post-review gates as defined in skill-integration.mdc.

Features:
    - Automatic skill detection from request keywords
    - Skill loading and validation
    - Gate execution (pre-review and post-review)
    - Skill combination rules
    - Skill metadata management

Usage:
    >>> from cursor_framework import SkillDiscovery
    >>> discovery = SkillDiscovery()
    >>> skills = discovery.detect_skills("Create a landing page for SaaS")
    >>> print(skills)
    [Skill.FRONTEND_TASTE, Skill.FULL_OUTPUT, Skill.FRONTEND_REVIEW]
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional
import json
import os
import re


class GateType(Enum):
    """Types of review gates."""

    PRE_REVIEW = "pre-review"
    POST_REVIEW = "post-review"


@dataclass
class GateResult:
    """Result of a gate execution."""

    gate_type: GateType
    skill: str
    section: str
    passed: bool
    items_checked: int
    items_passed: int
    failed_items: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    notes: str = ""


@dataclass
class SkillMetadata:
    """Metadata for a skill."""

    name: str
    version: str
    description: str
    tags: list[str]
    path: str
    pre_review_sections: list[str]
    post_review_sections: list[str]
    trigger_keywords: list[str]
    dependencies: list[str] = field(default_factory=list)


@dataclass
class DetectedSkill:
    """A detected skill with routing information."""

    skill: str
    confidence: float
    metadata: SkillMetadata
    gates_to_execute: list[GateType] = field(default_factory=list)


class SkillRegistry:
    """
    Registry for all available skills in the framework.

    Maintains metadata and relationships between skills.
    """

    def __init__(self):
        """Initialize the skill registry."""
        self._skills: dict[str, SkillMetadata] = {}
        self._skill_paths: dict[str, str] = {}
        self._initialize_default_skills()

    def _initialize_default_skills(self):
        """Initialize default skills from framework."""
        default_skills = [
            SkillMetadata(
                name="frontend-taste",
                version="1.0.0",
                description="Anti-slop frontend for landing pages and portfolios",
                tags=["frontend", "design", "landing", "taste"],
                path=".cursor/skills/ui_frontend-taste/SKILL.md",
                pre_review_sections=["0.A", "0.B", "0.C", "0.D", "0.E", "0.F"],
                post_review_sections=["6.A", "6.B", "6.C", "6.D", "6.E", "6.F", "6.G", "6.H"],
                trigger_keywords=[
                    "landing page", "portfolio", "landing", "homepage", "marketing site",
                    "minimalist", "awwwards", "apple-y", "linear-style", "brutalist",
                    "editorial", "greenfield frontend", "new website", "create page"
                ],
            ),
            SkillMetadata(
                name="frontend-redesign",
                version="1.0.0",
                description="Upgrade UI on existing codebase",
                tags=["frontend", "redesign", "upgrade", "improve"],
                path=".cursor/skills/ui_frontend-redesign/SKILL.md",
                pre_review_sections=["0.A", "0.B", "0.C", "0.D", "0.E"],
                post_review_sections=["4.A", "4.B", "4.C", "4.D", "4.E"],
                trigger_keywords=[
                    "redesign", "upgrade", "improve existing", "modernize",
                    "redesign site", "redesign app", "enhance current"
                ],
            ),
            SkillMetadata(
                name="frontend-review",
                version="1.0.0",
                description="Quality gate for all frontend tasks",
                tags=["frontend", "review", "quality", "gate"],
                path=".cursor/skills/ui_frontend-review/SKILL.md",
                pre_review_sections=["A.1", "A.2", "A.3"],
                post_review_sections=["B.1", "B.2", "B.3", "B.4", "B.5", "B.6", "B.7"],
                trigger_keywords=[
                    "review", "quality check", "audit ui", "taste check",
                    "check quality", "code review frontend"
                ],
            ),
            SkillMetadata(
                name="full-output",
                version="1.0.0",
                description="Ensure full implementation without truncation",
                tags=["output", "completeness", "implementation"],
                path=".cursor/skills/special_full-output/SKILL.md",
                pre_review_sections=["0.A", "0.B"],
                post_review_sections=["5.A", "5.B", "5.C"],
                trigger_keywords=[
                    "full implementation", "complete", "not skeleton", "no todo",
                    "multiple files", "all files", "full code", "not partial"
                ],
            ),
            SkillMetadata(
                name="security-review",
                version="1.1.0",  # sync 2026-07-15: marketing security extensions
                description=(
                    "Comprehensive security review (OWASP Top 10 + 30 Marketing Security "
                    "Additions MSA-01..30 covering GDPR/CCPA, cookie banner parity, "
                    "email auth, ad platform privacy, dark patterns, AI marketing risks)"
                ),
                tags=["security", "vulnerability", "audit", "owasp", "gdpr", "consent", "privacy", "marketing-security"],
                path=".cursor/skills/sec_security-review/SKILL.md",
                pre_review_sections=["S.1", "S.2", "S.3"],
                post_review_sections=["Security-1", "Security-2", "Security-3", "Security-4", "Security-5", "Security-6", "Security-7", "Security-8", "Security-9"],
                trigger_keywords=[
                    "security", "vulnerability", "penetration", "owasp", "xss",
                    "sql injection", "ssrf", "csrf", "authentication", "authorization",
                    "apk decompile", "binary analysis", "prompt injection", "exploit",
                    # 🆕 Marketing security triggers (sync 2026-07-15)
                    "gdpr", "ccpa", "lgpd", "pipl", "pdpd",
                    "consent", "cookie banner", "cookie consent", "dsar",
                    "right to deletion", "data subject request", "dpo",
                    "dark pattern", "roach motel", "confirmshaming",
                    "email authentication", "spf", "dkim", "dmarc",
                    "unsubscribe", "rfc 8058", "one-click unsubscribe",
                    "webhook signature", "hmac",
                    "meta capi", "tiktok events api", "google consent mode",
                    "limited data use", "ld flag",
                    "customer match", "hashed pii",
                    "auto-renewal", "click-to-cancel", "cancellation",
                    "iptc", "att", "app tracking transparency",
                    "ai marketing", "hallucination", "fabricated stats",
                    "data breach", "security incident", "leak",
                    "coppa", "hipaa", "bipa",
                    "right to be forgotten", "data export",
                    "double opt-in", "single opt-in",
                    "consent management", "consent mode",
                    "/security", "/privacy", "/gdpr", "/consent",
                ],
            ),
            SkillMetadata(
                name="security-auditor-agent",
                version="1.0.0",
                description=(
                    "Security Auditor agent — full OWASP Top 10 + 30 MSA marketing "
                    "security additions. Cite CWE/CVE; BLOCK on dark patterns, "
                    "pre-checked consent, PII to public LLM, missing SPF/DKIM/DMARC."
                ),
                tags=["agent", "security", "auditor", "owasp", "marketing-security"],
                path=".cursor/agents/security-auditor.md",
                pre_review_sections=["scope-audit"],
                post_review_sections=["risk-prioritized", "owasp-coverage"],
                trigger_keywords=[
                    "/audit", "security audit", "pre-deploy review",
                    "owasp audit", "cookie banner audit", "consent audit",
                    "dark pattern audit", "marketing security review",
                ],
                dependencies=["security-review"],
            ),
            SkillMetadata(
                name="vietnam-payment-review",
                version="1.0.0",
                description="Vietnam payment provider review",
                tags=["payment", "vietnam", "momo", "sepay"],
                path=".cursor/skills/sec_vietnam-payment-review/SKILL.md",
                pre_review_sections=["payment-pre"],
                post_review_sections=["payment-post"],
                trigger_keywords=[
                    "momo", "sepay", "ayos", "vietqr", "zalo pay", "zalo", "payos",
                    "vnpay", "vietnam payment", "payment integration", "thanh toan"
                ],
                dependencies=["security-review"],
            ),
            # Marketing umbrella — single entry representing 47 marketingskills
            # concept-refs (sync 2026-07-15 with coreyhaines31/marketingskills,
            # 39k stars). Per skill-registry.mdc §9, NO SKILL.md file is
            # created; routing happens via `.cursor/knowledge/marketing/decision-tree.md §11`.
            SkillMetadata(
                name="marketing",
                version="1.7.0",
                description=(
                    "47 marketing concept-refs across 9 categories "
                    "(Conversion, Content, SEO, Paid, Measurement, Retention, "
                    "Growth, Strategy, Sales/RevOps) — synced from "
                    "coreyhaines31/marketingskills into existing "
                    ".cursor/knowledge/marketing/*.md sections. No new "
                    "SKILL.md files (concept-ref pattern, see skill-registry.mdc §9)."
                ),
                tags=[
                    "marketing", "growth", "cro", "conversion", "signup",
                    "onboarding", "copywriting", "cold-email", "email-sequence",
                    "seo", "programmatic-seo", "ai-seo", "schema", "aso",
                    "paid-ads", "ad-creative", "analytics", "ab-testing",
                    "churn-prevention", "co-marketing", "free-tools", "referrals",
                    "launch", "pricing", "offers", "revops", "prospecting",
                    "pr", "customer-research", "marketing-council",
                    "marketing-loops", "product-marketing"
                ],
                # Path points to the umbrella knowledge folder, not a single SKILL.md.
                # Per-skill routing is done at runtime via decision-tree.md §11.
                path=".cursor/knowledge/marketing/",
                pre_review_sections=[
                    # Generic pre-gates — concept-ref pattern means each request
                    # routes via decision-tree §11 first.
                    "marketing-pre-product-context",  # verify .agents/product-marketing.md exists
                    "marketing-pre-preflight",  # checklist.md §9.X pre-launch blockers
                ],
                post_review_sections=[
                    "marketing-post-antipattern",  # anti-pattern.md §9.X
                    "marketing-post-faq",  # faq.md §9.X
                ],
                trigger_keywords=[
                    "marketing", "growth", "cro", "conversion", "signup",
                    "onboarding", "popup", "paywall", "copywriting",
                    "cold email", "newsletter", "sms", "social content",
                    "seo", "programmatic seo", "ai seo", "schema", "aso",
                    "paid ads", "google ads", "meta ads", "ad creative",
                    "analytics", "ab test", "a/b test", "split test",
                    "churn", "retention", "dunning",
                    "co-marketing", "free tool", "referral",
                    "launch", "pricing", "offer",
                    "revops", "lead scoring", "mql", "sql",
                    "prospecting", "outbound", "pr", "press release",
                    "haro", "directory submission", "customer research",
                    "jtbd", "marketing council", "marketing loops",
                    "product marketing", "icp", "positioning"
                ],
                # Marketing requires mandatory pre-read of product context.
                dependencies=["product-marketing-context"],
            ),
            # ── Agents (sync 2026-07-15) — 10 specialized agents registered as
            # skills so context_router.py can route user requests to them via
            # the same keyword + intent pipeline. The path points to each
            # agent's .md profile at .cursor/agents/{name}.md.
            SkillMetadata(
                name="debugger",
                version="1.0.0",
                description=(
                    "4-phase root-cause investigator: reproduce → isolate → "
                    "fix → verify. Forms ≤ 3 hypotheses per round, tests "
                    "cheapest first. Never ships a fix without regression test."
                ),
                tags=["debug", "bug-fix", "root-cause", "diagnostic"],
                path=".cursor/agents/debugger.md",
                pre_review_sections=[
                    "debugger-pre-repro",  # minimal reproducible case required
                ],
                post_review_sections=[
                    "debugger-post-verify",  # 5-step verification, regression test
                ],
                trigger_keywords=[
                    "debug", "bug", "fix bug", "fix error", "repro",
                    "root cause", "intermittent", "stack trace", "exception",
                    "fix lỗi", "sửa lỗi", "lỗi", "bug report"
                ],
            ),
            SkillMetadata(
                name="ui-designer",
                version="1.0.0",
                description=(
                    "UI/UX designer for design tokens, components, layouts, "
                    "and production-ready specs. Outputs token-driven Tailwind/"
                    "CSS ready to paste. Always ships empty/loading/error states."
                ),
                tags=["design", "ui", "ux", "tokens", "components"],
                path=".cursor/agents/ui-designer.md",
                pre_review_sections=[
                    "ui-designer-pre-goal",  # user goal + aesthetic direction
                ],
                post_review_sections=[
                    "ui-designer-post-states",  # all states + a11y baseline
                ],
                trigger_keywords=[
                    "design ui", "ui design", "ux", "design system",
                    "design tokens", "component spec", "redesign",
                    "thiết kế ui", "thiết kế giao diện", "giao diện",
                    "wireframe", "mockup", "landing page design"
                ],
            ),
            SkillMetadata(
                name="web-cloner",
                version="1.0.0",
                description=(
                    "Playwright-driven website cloner. Fidelity levels L1–L4. "
                    "Respects robots.txt, copyright, and rate limits. Outputs "
                    "to .cursor/clones/{domain}/ as self-contained project."
                ),
                tags=["clone", "playwright", "mirror", "copy"],
                path=".cursor/agents/web-cloner.md",
                pre_review_sections=[
                    "web-cloner-pre-compliance",  # robots.txt + ToS check
                ],
                post_review_sections=[
                    "web-cloner-post-verification",  # visual diff ≤ 2% + a11y
                ],
                trigger_keywords=[
                    "clone", "copy website", "mirror", "replicate site",
                    "clone web", "copy site", "sao chép web",
                    "/clone", "/copy", "/mirror"
                ],
            ),
            SkillMetadata(
                name="web-scraper",
                version="1.0.0",
                description=(
                    "Structured content extraction via Playwright. Categories: "
                    "sdk, api, ui, test, qc, article, table, list, code. "
                    "≤ 1 req/sec · cites source URLs in every output file."
                ),
                tags=["scrape", "extract", "playwright", "docs"],
                path=".cursor/agents/web-scraper.md",
                pre_review_sections=[
                    "web-scraper-pre-robots",  # robots.txt + ToS check
                ],
                post_review_sections=[
                    "web-scraper-post-verify",  # 95% source match + coverage
                ],
                trigger_keywords=[
                    "scrape", "extract", "crawl", "fetch docs",
                    "scrape web", "lấy nội dung", "trích xuất",
                    "/scrape", "/extract", "/docs",
                    "pull documentation", "scrape article"
                ],
            ),
            SkillMetadata(
                name="refactor-specialist",
                version="1.0.0",
                description=(
                    "Behavior-preserving code refactoring. 15 smells → 15 "
                    "recipes. One commit per smell; never mixed with features. "
                    "Refuses to refactor without an existing test safety net."
                ),
                tags=["refactor", "smells", "cleanup", "boy-scout"],
                path=".cursor/agents/refactor-specialist.md",
                pre_review_sections=[
                    "refactor-pre-test-baseline",  # tests must pass before
                ],
                post_review_sections=[
                    "refactor-post-behavior",  # behavior unchanged + metrics
                ],
                trigger_keywords=[
                    "refactor", "cleanup", "code smell", "tech debt",
                    "boy scout", "extract function", "rename",
                    "refactor code", "dọn dẹp code", "/refactor"
                ],
            ),
            SkillMetadata(
                name="deployment-engineer",
                version="1.0.0",
                description=(
                    "Production deployment: 10-gate pre-flight, canary → "
                    "ramp → verify phases, rollback rehearsed ≤ 1 min. "
                    "Coordinates with migration-specialist for schema changes."
                ),
                tags=["deploy", "release", "rollback", "observability"],
                path=".cursor/agents/deployment-engineer.md",
                pre_review_sections=[
                    "deploy-pre-checklist",  # 10-gate pre-flight
                ],
                post_review_sections=[
                    "deploy-post-verify",  # SLO + business KPI check
                ],
                trigger_keywords=[
                    "deploy", "release", "ship", "rollout", "production",
                    "canary", "blue green", "deploy to prod",
                    "triển khai", "release phiên bản",
                    "/deploy", "/release", "/ship"
                ],
            ),
            SkillMetadata(
                name="migration-specialist",
                version="1.0.0",
                description=(
                    "Schema, data, and framework migrations. Expand → migrate → "
                    "contract (3 deploys, not 1). Always reversible, idempotent, "
                    "throttled. Coordinates with deployment-engineer."
                ),
                tags=["migration", "schema", "backfill", "alter-table"],
                path=".cursor/agents/migration-specialist.md",
                pre_review_sections=[
                    "migration-pre-audit",  # schema + callers + SLO audit
                ],
                post_review_sections=[
                    "migration-post-verify",  # row counts + checksums + lag
                ],
                trigger_keywords=[
                    "migrate", "migration", "schema change", "backfill",
                    "add column", "drop column", "rename column",
                    "data migration", "framework upgrade",
                    "/migrate", "di trú", "migration script"
                ],
            ),
            SkillMetadata(
                name="doc-writer",
                version="1.0.0",
                description=(
                    "Technical writer: README, ADR, runbook, API reference. "
                    "Diátaxis framework (tutorial · how-to · reference · "
                    "explanation). Every example runnable, every link checked."
                ),
                tags=["docs", "readme", "adr", "runbook"],
                path=".cursor/agents/doc-writer.md",
                pre_review_sections=[
                    "doc-pre-audience",  # reader profile + goal
                ],
                post_review_sections=[
                    "doc-post-verification",  # all examples verified runnable
                ],
                trigger_keywords=[
                    "write docs", "readme", "documentation", "adr",
                    "runbook", "tutorial", "api reference",
                    "viết tài liệu",
                    "/doc", "/readme", "/adr", "/runbook"
                ],
            ),
            SkillMetadata(
                name="devops-engineer",
                version="1.0.0",
                description=(
                    "CI/CD, IaC, containers, observability. Four golden signals "
                    "(latency, traffic, errors, saturation). Reproducible from "
                    "scratch ≤ 1 hour. Tagged resources for cost tracking."
                ),
                tags=["ci-cd", "iac", "kubernetes", "observability"],
                path=".cursor/agents/devops-engineer.md",
                pre_review_sections=[
                    "devops-pre-slo",  # SLO must be defined before infra work
                ],
                post_review_sections=[
                    "devops-post-verify",  # pipeline + alerts wired
                ],
                trigger_keywords=[
                    "ci", "cd", "pipeline", "infrastructure", "iac",
                    "terraform", "kubernetes", "docker",
                    "ci/cd", "build pipeline", "/build", "container"
                ],
            ),
            SkillMetadata(
                name="marketing-strategist",
                version="1.0.0",
                description=(
                    "Product marketing & growth strategist. 9 categories: "
                    "Conversion, Content, SEO, Paid, Measurement, Retention, "
                    "Growth Eng, Strategy, Sales/RevOps. Numbers before opinions."
                ),
                tags=["marketing", "growth", "positioning", "funnel"],
                path=".cursor/agents/marketing-strategist.md",
                pre_review_sections=[
                    "marketing-strategist-pre-metric",  # define measurable goal
                ],
                post_review_sections=[
                    "marketing-strategist-post-tracking",  # tracking plan wired
                ],
                trigger_keywords=[
                    "marketing", "growth", "positioning", "funnel",
                    "cro", "seo strategy", "paid ads", "retention",
                    "churn", "pricing", "launch",
                    "chiến lược marketing", "/marketing", "/growth"
                ],
            ),
        ]

        for skill in default_skills:
            self.register(skill)

    def register(self, metadata: SkillMetadata):
        """Register a skill with metadata."""
        self._skills[metadata.name] = metadata
        self._skill_paths[metadata.name] = metadata.path

    def get(self, name: str) -> Optional[SkillMetadata]:
        """Get skill metadata by name."""
        return self._skills.get(name)

    def get_all(self) -> list[SkillMetadata]:
        """Get all registered skills."""
        return list(self._skills.values())

    def find_by_keyword(self, keyword: str) -> list[SkillMetadata]:
        """Find skills matching a keyword."""
        keyword_lower = keyword.lower()
        matches = []

        for skill in self._skills.values():
            if keyword_lower in skill.name.lower():
                matches.append(skill)
            elif any(keyword_lower in kw.lower() for kw in skill.trigger_keywords):
                matches.append(skill)

        return matches

    def get_dependencies(self, name: str) -> list[str]:
        """Get dependencies for a skill."""
        skill = self._skills.get(name)
        return skill.dependencies if skill else []


class GateExecutor:
    """
    Executes pre-review and post-review gates for skills.

    Simulates gate execution and tracks results.
    """

    def __init__(self):
        """Initialize the gate executor."""
        self._results: list[GateResult] = []

    def execute_pre_review(
        self,
        skill: SkillMetadata,
        context: dict,
    ) -> GateResult:
        """
        Execute pre-review gate for a skill.

        Args:
            skill: The skill metadata
            context: Request context

        Returns:
            GateResult with execution details
        """
        checked = len(skill.pre_review_sections)
        passed_items = 0
        failed_items = []

        # Inject skill_name into context for section matching
        context = {**context, "skill_name": skill.name}

        for section in skill.pre_review_sections:
            if self._check_pre_section(section, context):
                passed_items += 1
            else:
                failed_items.append(section)

        result = GateResult(
            gate_type=GateType.PRE_REVIEW,
            skill=skill.name,
            section=",".join(skill.pre_review_sections),
            passed=len(failed_items) == 0,
            items_checked=checked,
            items_passed=passed_items,
            failed_items=failed_items,
            notes=f"Pre-review gate for {skill.name}",
        )

        self._results.append(result)
        return result

    def execute_post_review(
        self,
        skill: SkillMetadata,
        context: dict,
    ) -> GateResult:
        """
        Execute post-review gate for a skill.

        Args:
            skill: The skill metadata
            context: Implementation context

        Returns:
            GateResult with execution details
        """
        checked = len(skill.post_review_sections)
        passed_items = 0
        failed_items = []

        # Inject skill_name into context for section matching
        context = {**context, "skill_name": skill.name}

        for section in skill.post_review_sections:
            if self._check_post_section(section, context):
                passed_items += 1
            else:
                failed_items.append(section)

        result = GateResult(
            gate_type=GateType.POST_REVIEW,
            skill=skill.name,
            section=",".join(skill.post_review_sections),
            passed=len(failed_items) == 0,
            items_checked=checked,
            items_passed=passed_items,
            failed_items=failed_items,
            notes=f"Post-review gate for {skill.name}",
        )

        self._results.append(result)
        return result

    def _check_pre_section(self, section: str, context: dict) -> bool:
        """
        Check if a pre-review section passes validation.
        
        Validates that required context keys exist and have valid values
        for the given section identifier.
        
        Section identifiers can be:
        - Numeric: "0.A", "0.B", "S.1", etc. (from skill registry)
        - Named: "taste-pre", "security-pre", etc. (for custom checks)
        """
        section_lower = section.lower()
        section_clean = re.sub(r'[\d.]+', '', section_lower).strip() or section_lower
        
        # Common required context keys
        required_keys = context.get("required_keys", [])
        for key in required_keys:
            if key not in context:
                return False
        
        # Get skill name from context for better matching
        skill_name = context.get("skill_name", "").lower().replace("-", " ")
        
        # Check for specific section validations based on content keywords
        # These map section patterns to required context
        
        # Frontend taste / design sections
        if any(kw in section_clean for kw in ["taste", "design", "ui", "aesthetic", "goal"]):
            return "goal" in context or "request" in context or "design_goal" in context
        
        # Security sections
        if any(kw in section_clean for kw in ["security", "auth", "vuln", "auth"]):
            return context.get("auth_checked", False) or "auth" in context or "security" in skill_name
        
        # Review / quality sections
        if any(kw in section_clean for kw in ["review", "quality", "audit", "check"]):
            return context.get("code_baseline", False) or "code" in context or "request" in context
        
        # Output / implementation sections
        if any(kw in section_clean for kw in ["output", "implement", "complete", "scope"]):
            return "scope" in context or "request" in context
        
        # Debug / repro sections
        if any(kw in section_clean for kw in ["debug", "repro", "bug", "error"]):
            return context.get("reproducible", False) or "error" in context or "bug" in context
        
        # Marketing / strategy sections
        if any(kw in section_clean for kw in ["market", "cro", "growth", "strategy"]):
            return "goal" in context or "product" in context or "request" in context
        
        # Compliance / robots sections
        if any(kw in section_clean for kw in ["compliance", "robot", "scrap"]):
            return context.get("compliance_checked", False) or context.get("robots_checked", False) or "url" in context
        
        # Default: require basic request context
        return bool(context.get("request") or context.get("text") or context.get("goal"))

    def _check_post_section(self, section: str, context: dict) -> bool:
        """
        Check if a post-review section passes validation.
        
        Validates that implementation meets quality criteria for the section.
        """
        section_lower = section.lower()
        section_clean = re.sub(r'[\d.]+', '', section_lower).strip() or section_lower
        
        # Get skill name from context for better matching
        skill_name = context.get("skill_name", "").lower().replace("-", " ")
        
        # Check for specific post-section validations based on content keywords
        
        # Frontend taste / design sections
        if any(kw in section_clean for kw in ["taste", "design", "ui", "aesthetic"]):
            return context.get("taste_check", False) or "output" in context
        
        # Security sections - require no critical vulnerabilities
        if any(kw in section_clean for kw in ["security", "vuln", "auth", "audit"]):
            vulns = context.get("vulnerabilities", [])
            critical = [v for v in vulns if v.get("severity") == "critical"]
            return len(critical) == 0
        
        # Review / quality sections
        if any(kw in section_clean for kw in ["review", "quality", "check"]):
            return context.get("quality_pass", False) or "output" in context
        
        # Output / implementation sections - require complete implementation
        if any(kw in section_clean for kw in ["output", "implement", "complete", "scope"]):
            is_complete = context.get("is_complete", True)
            has_todos = context.get("has_todos", False)
            return is_complete and not has_todos
        
        # Marketing sections - require no anti-patterns
        if any(kw in section_clean for kw in ["market", "cro", "antipattern"]):
            return context.get("no_antipatterns", True)
        
        # Debug / verify sections - require regression test passed
        if any(kw in section_clean for kw in ["debug", "verify", "repro"]):
            return context.get("regression_pass", False) or context.get("tests_pass", False)
        
        # Compliance / scraping sections
        if any(kw in section_clean for kw in ["compliance", "robot", "scrap", "coverage"]):
            if "diff_acceptable" in context:
                return context.get("diff_acceptable", True)
            coverage = context.get("source_coverage", 0)
            return coverage >= 0.95
        
        # Test / behavior sections
        if any(kw in section_clean for kw in ["test", "behavior", "regression"]):
            return context.get("tests_pass", False) or context.get("behavior_preserved", True)
        
        # Deploy / migration sections
        if any(kw in section_clean for kw in ["deploy", "migrate", "slo", "pipeline"]):
            return context.get("slo_verified", False) or context.get("pipeline_wired", False)
        
        # Payment sections
        if any(kw in section_clean for kw in ["payment", "checkout"]):
            return context.get("payment_flow_verified", False)
        
        # Default: require output exists
        return "output" in context or "result" in context

    def get_results(self) -> list[GateResult]:
        """Get all gate execution results."""
        return self._results.copy()

    def get_summary(self) -> dict:
        """Get summary of gate executions."""
        pre_results = [r for r in self._results if r.gate_type == GateType.PRE_REVIEW]
        post_results = [r for r in self._results if r.gate_type == GateType.POST_REVIEW]

        return {
            "total_gates": len(self._results),
            "pre_review": {
                "total": len(pre_results),
                "passed": sum(1 for r in pre_results if r.passed),
                "failed": sum(1 for r in pre_results if not r.passed),
            },
            "post_review": {
                "total": len(post_results),
                "passed": sum(1 for r in post_results if r.passed),
                "failed": sum(1 for r in post_results if not r.passed),
            },
        }


class SkillDiscovery:
    """
    Automatic skill detection and loading system.

    Detects applicable skills based on request analysis
    and manages skill execution workflow.
    """

    # Skill combination rules
    COMBINATION_RULES = {
        "landing_page": {
            "primary": "frontend-taste",
            "secondary": ["full-output", "frontend-review"],
            "gates": ["taste-pre", "taste-post", "fulloutput-pre", "fulloutput-post", "review-pre", "review-post"],
        },
        "redesign": {
            "primary": "frontend-redesign",
            "secondary": ["full-output", "frontend-review"],
            "gates": ["redesign-pre", "redesign-post", "fulloutput-pre", "fulloutput-post", "review-pre", "review-post"],
        },
        "multi_file": {
            "primary": "full-output",
            "secondary": ["frontend-review"],
            "gates": ["fulloutput-pre", "fulloutput-post", "review-pre", "review-post"],
        },
        "frontend_review": {
            "primary": "frontend-review",
            "secondary": [],
            "gates": ["review-pre", "review-post"],
        },
        "payment_task": {
            "primary": "vietnam-payment-review",
            "secondary": ["security-review"],
            "gates": ["payment-pre", "payment-post", "security-pre", "security-post"],
        },
        "security_task": {
            "primary": "security-review",
            "secondary": [],
            "gates": ["security-pre", "security-post"],
        },
    }

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize skill discovery.

        Args:
            base_path: Base path for skill files
        """
        self.registry = SkillRegistry()
        self.gate_executor = GateExecutor()
        self.base_path = base_path or os.getcwd()
        self._discovery_history: list[DetectedSkill] = []
        self._skill_file_cache: dict[str, tuple[float, str]] = {}

    def detect_skills(self, request: str) -> list[DetectedSkill]:
        """
        Detect applicable skills from a request.

        Args:
            request: The user request text

        Returns:
            List of detected skills with metadata
        """
        detected: list[DetectedSkill] = []
        request_lower = request.lower()

        for skill_metadata in self.registry.get_all():
            confidence = self._calculate_confidence(request_lower, skill_metadata)

            if confidence > 0.1:
                skill = DetectedSkill(
                    skill=skill_metadata.name,
                    confidence=confidence,
                    metadata=skill_metadata,
                    gates_to_execute=self._determine_gates(skill_metadata),
                )
                detected.append(skill)
                self._discovery_history.append(skill)

        detected.sort(key=lambda s: s.confidence, reverse=True)
        return detected

    def _calculate_confidence(
        self, request: str, skill: SkillMetadata
    ) -> float:
        """Calculate confidence score for skill match."""
        matches = 0
        total_triggers = len(skill.trigger_keywords)

        for keyword in skill.trigger_keywords:
            if keyword.lower() in request:
                matches += 1

        base_confidence = matches / total_triggers if total_triggers > 0 else 0

        if skill.name.replace("-", " ") in request:
            base_confidence += 0.3

        return min(0.99, base_confidence)

    def _determine_gates(self, skill: SkillMetadata) -> list[GateType]:
        """Determine which gates to execute for a skill."""
        return [GateType.PRE_REVIEW, GateType.POST_REVIEW]

    def get_combined_skills(self, request: str) -> list[DetectedSkill]:
        """
        Get combined skills based on skill combination rules.

        Args:
            request: The user request

        Returns:
            List of skills to apply in order
        """
        detected = self.detect_skills(request)
        if not detected:
            return []

        primary = detected[0].skill

        combination_key = self._match_combination(primary, request)
        if combination_key and combination_key in self.COMBINATION_RULES:
            rule = self.COMBINATION_RULES[combination_key]
            combined = []

            primary_skill = next(
                (s for s in detected if s.skill == rule["primary"]),
                None,
            )
            if primary_skill:
                combined.append(primary_skill)

            for secondary_name in rule["secondary"]:
                secondary_skill = next(
                    (s for s in detected if s.skill == secondary_name),
                    self.registry.get(secondary_name),
                )
                if secondary_skill:
                    if isinstance(secondary_skill, SkillMetadata):
                        combined.append(DetectedSkill(
                            skill=secondary_skill.name,
                            confidence=0.8,
                            metadata=secondary_skill,
                            gates_to_execute=self._determine_gates(secondary_skill),
                        ))
                    else:
                        combined.append(secondary_skill)

            return combined

        return detected

    def _match_combination(self, primary: str, request: str) -> Optional[str]:
        """Match request to a combination rule."""
        request_lower = request.lower()

        if any(kw in request_lower for kw in ["landing", "portfolio", "homepage"]):
            return "landing_page"
        elif any(kw in request_lower for kw in ["redesign", "upgrade", "improve"]):
            return "redesign"
        elif any(kw in request_lower for kw in ["momo", "sepay", "payment", "vietqr"]):
            return "payment_task"
        elif any(kw in request_lower for kw in ["security", "vulnerability"]):
            return "security_task"
        elif any(kw in request_lower for kw in ["full", "complete", "multiple files"]):
            return "multi_file"

        return None

    def load_skill_file(self, skill_name: str) -> Optional[str]:
        """
        Load skill file content with mtime-based cache.

        Args:
            skill_name: Name of the skill

        Returns:
            Skill file content or None
        """
        skill = self.registry.get(skill_name)
        if not skill:
            return None

        skill_path = Path(self.base_path) / skill.path
        if not skill_path.exists():
            return None

        try:
            mtime = skill_path.stat().st_mtime
        except OSError:
            return None

        cached = self._skill_file_cache.get(str(skill_path))
        if cached and cached[0] == mtime:
            return cached[1]

        try:
            content = skill_path.read_text(encoding="utf-8")
        except OSError:
            return None

        self._skill_file_cache[str(skill_path)] = (mtime, content)
        return content

    def clear_skill_cache(self) -> int:
        """Drop all cached skill file contents. Returns number of entries cleared."""
        count = len(self._skill_file_cache)
        self._skill_file_cache.clear()
        return count

    def execute_gates(
        self, skills: list[DetectedSkill], context: dict, gate_type: GateType
    ) -> list[GateResult]:
        """
        Execute gates for multiple skills.

        Args:
            skills: List of detected skills
            context: Execution context
            gate_type: Type of gate to execute

        Returns:
            List of gate results
        """
        results = []

        for skill_detected in skills:
            skill_metadata = skill_detected.metadata

            if gate_type == GateType.PRE_REVIEW:
                result = self.gate_executor.execute_pre_review(skill_metadata, context)
            else:
                result = self.gate_executor.execute_post_review(skill_metadata, context)

            results.append(result)

        return results

    def get_discovery_stats(self) -> dict:
        """Get statistics about skill discovery."""
        return {
            "total_discoveries": len(self._discovery_history),
            "unique_skills": len(set(s.skill for s in self._discovery_history)),
            "avg_confidence": (
                sum(s.confidence for s in self._discovery_history) / len(self._discovery_history)
                if self._discovery_history else 0
            ),
            "gate_summary": self.gate_executor.get_summary(),
        }


def create_discovery(base_path: Optional[str] = None) -> SkillDiscovery:
    """Factory function to create a configured SkillDiscovery."""
    return SkillDiscovery(base_path=base_path)
