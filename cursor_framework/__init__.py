"""
Cursor Enterprise Framework - Python Core Library

A comprehensive Python library supporting the Cursor Enterprise Framework rules and skills.
Provides utilities for context routing, memory management, token optimization, and skill discovery.

Modules:
    context_router: Intent classification and skill routing
    memory_manager: Memory-first context management
    memory_store: JSON-backed persistence for MemoryManager
    token_optimizer: Token usage optimization
    skill_discovery: Automatic skill detection and loading
    indexer: Scans .cursor/ into machine + human index
    context_builder: Orchestrates Indexer + SkillDiscovery + TokenOptimizer
    workflow: Single entry point — scan + cache + build + persist
    watcher: Polls .cursor/ for changes, triggers callbacks
    dashboard: Stdlib HTTP server serving INDEX.json + stats + HTML
    utils: Common utilities

Author: Cursor Enterprise Framework
Version: 1.2.0
"""

__version__ = "1.2.0"
__author__ = "Cursor Enterprise Framework"

from .context_router import (
    ContextRouter,
    IntentClassifier,
    IntentType,
    Domain,
    Skill,
    SkillRoute,
)
from .memory_manager import MemoryManager, MemoryEntry, MemoryTier
from .memory_store import MemoryStore
from .token_optimizer import TokenOptimizer, TokenBudget, CompressionStrategy, CompressionResult
from .skill_discovery import SkillDiscovery, SkillRegistry
from .indexer import Indexer, IndexResult, AssetEntry
from .context_builder import ContextBuilder, ContextResult
from .workflow import Workflow, WorkflowResult
from .watcher import Watcher
from .dashboard import Dashboard

__all__ = [
    "ContextRouter",
    "IntentClassifier",
    "IntentType",
    "Domain",
    "Skill",
    "SkillRoute",
    "MemoryManager",
    "MemoryEntry",
    "MemoryTier",
    "MemoryStore",
    "TokenOptimizer",
    "TokenBudget",
    "CompressionStrategy",
    "CompressionResult",
    "SkillDiscovery",
    "SkillRegistry",
    "Indexer",
    "IndexResult",
    "AssetEntry",
    "ContextBuilder",
    "ContextResult",
    "Workflow",
    "WorkflowResult",
    "Watcher",
    "Dashboard",
]