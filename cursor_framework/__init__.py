"""
Cursor Enterprise Framework - Python Core Library

A comprehensive Python library supporting the Cursor Enterprise Framework rules and skills.
Provides utilities for context routing, memory management, token optimization, and skill discovery.

See STRUCTURE.md for full directory layout and data flow diagrams.

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

__version__ = "1.2.1"
__author__ = "Cursor Enterprise Framework"

# Lazy attribute access (PEP 562): importing `cursor_framework` does not
# load Dashboard/Workflow/Watcher/Indexer. Submodules are imported on
# first attribute access so cold-start CLI subcommands that only need
# argparse + __version__ stay fast.
_LAZY_EXPORTS = {
    "ContextRouter": "cursor_framework.context_router",
    "IntentClassifier": "cursor_framework.context_router",
    "IntentType": "cursor_framework.context_router",
    "Domain": "cursor_framework.context_router",
    "Skill": "cursor_framework.context_router",
    "SkillRoute": "cursor_framework.context_router",
    "MemoryManager": "cursor_framework.memory_manager",
    "MemoryEntry": "cursor_framework.memory_manager",
    "MemoryTier": "cursor_framework.memory_manager",
    "MemoryStore": "cursor_framework.memory_store",
    "TokenOptimizer": "cursor_framework.token_optimizer",
    "TokenBudget": "cursor_framework.token_optimizer",
    "CompressionStrategy": "cursor_framework.token_optimizer",
    "CompressionResult": "cursor_framework.token_optimizer",
    "SkillDiscovery": "cursor_framework.skill_discovery",
    "SkillRegistry": "cursor_framework.skill_discovery",
    "Indexer": "cursor_framework.indexer",
    "IndexResult": "cursor_framework.indexer",
    "AssetEntry": "cursor_framework.indexer",
    "ContextBuilder": "cursor_framework.context_builder",
    "ContextResult": "cursor_framework.context_builder",
    "Workflow": "cursor_framework.workflow",
    "WorkflowResult": "cursor_framework.workflow",
    "Watcher": "cursor_framework.watcher",
    "Dashboard": "cursor_framework.dashboard",
}


def __getattr__(name: str):
    module_name = _LAZY_EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module 'cursor_framework' has no attribute {name!r}")
    import importlib
    module = importlib.import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value  # cache for subsequent access
    return value


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