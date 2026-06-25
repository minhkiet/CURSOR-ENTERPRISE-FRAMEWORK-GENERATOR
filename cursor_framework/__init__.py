"""
Cursor Enterprise Framework - Python Core Library

A comprehensive Python library supporting the Cursor Enterprise Framework rules and skills.
Provides utilities for context routing, memory management, token optimization, and skill discovery.

Modules:
    context_router: Intent classification and skill routing
    memory_manager: Memory-first context management
    token_optimizer: Token usage optimization
    skill_discovery: Automatic skill detection and loading
    utils: Common utilities

Author: Cursor Enterprise Framework
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Cursor Enterprise Framework"

from .context_router import ContextRouter, IntentClassifier, SkillRoute
from .memory_manager import MemoryManager, MemoryEntry, MemoryTier
from .token_optimizer import TokenOptimizer, TokenBudget
from .skill_discovery import SkillDiscovery, SkillRegistry

__all__ = [
    "ContextRouter",
    "IntentClassifier",
    "SkillRoute",
    "MemoryManager",
    "MemoryEntry",
    "MemoryTier",
    "TokenOptimizer",
    "TokenBudget",
    "SkillDiscovery",
    "SkillRegistry",
]
