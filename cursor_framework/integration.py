"""
Framework Integration Module

Provides integration between Python utilities and framework rules/skills.
"""

from .context_router import ContextRouter, IntentClassifier, SkillRoute, IntentType, Domain, Skill, RoutingRequest
from .memory_manager import MemoryManager, MemoryEntry, MemoryTier, MemoryStats
from .token_optimizer import TokenOptimizer, TokenBudget, CompressionStrategy, CompressionResult
from .skill_discovery import SkillDiscovery, SkillRegistry, SkillMetadata, DetectedSkill, GateExecutor, GateType, GateResult

__all__ = [
    # Context Router
    "ContextRouter",
    "IntentClassifier",
    "SkillRoute",
    "IntentType",
    "Domain",
    "Skill",
    "RoutingRequest",
    # Memory Manager
    "MemoryManager",
    "MemoryEntry",
    "MemoryTier",
    "MemoryStats",
    # Token Optimizer
    "TokenOptimizer",
    "TokenBudget",
    "CompressionStrategy",
    "CompressionResult",
    # Skill Discovery
    "SkillDiscovery",
    "SkillRegistry",
    "SkillMetadata",
    "DetectedSkill",
    "GateExecutor",
    "GateType",
    "GateResult",
]
