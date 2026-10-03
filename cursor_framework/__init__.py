"""
Cursor Enterprise Framework - Python Core Library

A comprehensive Python library supporting the Cursor Enterprise Framework rules and skills.
Provides utilities for context routing, memory management, token optimization, and skill discovery.

Supports multiple vibe coding agents:
- Cursor IDE
- Codex (cursor.com)
- Claude Code (@cursor/codex)
- Grok (x.com/grok)

See STRUCTURE.md for full directory layout and data flow diagrams.

Modules:
    context_router: Intent classification and skill routing
    memory_manager: Memory-first context management
    memory_store: JSON-backed persistence for MemoryManager
    token_optimizer: Token usage optimization
    skill_discovery: Automatic skill detection and loading
    cross_agent: Unified cross-agent skill compatibility layer
    indexer: Scans .cursor/ into machine + human index
    context_builder: Orchestrates Indexer + SkillDiscovery + TokenOptimizer
    workflow: Single entry point — scan + cache + build + persist
    watcher: Polls .cursor/ for changes, triggers callbacks
    dashboard: Stdlib HTTP server serving INDEX.json + stats + HTML
    code_graph: Project code graph indexer with dependency detection
    session_memory: Session memory tracker for file reads
    cursor_integration: Cursor IDE integration layer
    agent_integration: Cross-agent integration (Codex, Claude Code, Grok)
    utils: Common utilities

Author: Cursor Enterprise Framework
Version: 1.6.0
"""

from __future__ import annotations

import importlib

__version__ = "1.6.0"
__author__ = "Cursor Enterprise Framework"

# Lazy attribute access (PEP 562): importing `cursor_framework` does not
# load Dashboard/Workflow/Watcher/Indexer. Submodules are imported on
# first attribute access so cold-start CLI subcommands that only need
# argparse + __version__ stay fast.
_LAZY_EXPORTS = {
    # Cross-Agent Compatibility Layer
    "cross_agent": "cursor_framework.cross_agent",
    "detect_agent": "cursor_framework.cross_agent",
    "get_current_agent": "cursor_framework.cross_agent",
    "get_compatible_skills": "cursor_framework.cross_agent",
    "detect_skills_from_request": "cursor_framework.cross_agent",
    "get_skill_definition": "cursor_framework.cross_agent",
    "get_gates_for_skill": "cursor_framework.cross_agent",
    "export_skill_manifest": "cursor_framework.cross_agent",
    "export_all_skills_json": "cursor_framework.cross_agent",
    "AgentType": "cursor_framework.cross_agent",
    "GateType": "cursor_framework.cross_agent",
    "SkillDefinition": "cursor_framework.cross_agent",
    "GateResult": "cursor_framework.cross_agent",
    "GateExecutionResult": "cursor_framework.cross_agent",
    
    # Context Router
    "ContextRouter": "cursor_framework.context_router",
    "IntentClassifier": "cursor_framework.context_router",
    "IntentType": "cursor_framework.context_router",
    "Domain": "cursor_framework.context_router",
    "Skill": "cursor_framework.context_router",
    "SkillRoute": "cursor_framework.context_router",
    
    # Memory Manager
    "MemoryManager": "cursor_framework.memory_manager",
    "MemoryEntry": "cursor_framework.memory_manager",
    "MemoryTier": "cursor_framework.memory_manager",
    "MemoryStore": "cursor_framework.memory_store",
    
    # Token Optimizer
    "TokenOptimizer": "cursor_framework.token_optimizer",
    "TokenBudget": "cursor_framework.token_optimizer",
    "CompressionStrategy": "cursor_framework.token_optimizer",
    "CompressionResult": "cursor_framework.token_optimizer",
    
    # Skill Discovery
    "SkillDiscovery": "cursor_framework.skill_discovery",
    "SkillRegistry": "cursor_framework.skill_discovery",
    "CrossAgentSkillDiscovery": "cursor_framework.skill_discovery",
    "GateExecutor": "cursor_framework.skill_discovery",
    "GateType": "cursor_framework.skill_discovery",
    "GateResult": "cursor_framework.skill_discovery",
    
    # Agent Integration
    "AgentDetector": "cursor_framework.agent_integration",
    "AgentType": "cursor_framework.agent_integration",
    "CrossAgentIntegration": "cursor_framework.agent_integration",
    
    # Indexer & Context Builder
    "Indexer": "cursor_framework.indexer",
    "IndexResult": "cursor_framework.indexer",
    "AssetEntry": "cursor_framework.indexer",
    "ContextBuilder": "cursor_framework.context_builder",
    "ContextResult": "cursor_framework.context_builder",
    
    # Workflow & Dashboard
    "Workflow": "cursor_framework.workflow",
    "WorkflowResult": "cursor_framework.workflow",
    "Watcher": "cursor_framework.watcher",
    "Dashboard": "cursor_framework.dashboard",
    
    # TDAM Integration
    "TDAMIntegration": "cursor_framework.tdam_integration",
    "TDAMClient": "cursor_framework.tdam_integration",
    "TDAMConfig": "cursor_framework.tdam_integration",
    "MemoryLayer": "cursor_framework.tdam_integration",
    "MemoryItem": "cursor_framework.tdam_integration",
    "ConversationTurn": "cursor_framework.tdam_integration",
    "OffloadResult": "cursor_framework.tdam_integration",
    "create_tdam_integration": "cursor_framework.tdam_integration",
    "create_tdam_integration_from_env": "cursor_framework.tdam_integration",
    
    # Code Graph & Memory System
    "CodeGraph": "cursor_framework.code_graph",
    "CodeGraphResult": "cursor_framework.code_graph",
    "Module": "cursor_framework.code_graph",
    "Dependency": "cursor_framework.code_graph",
    "SessionMemory": "cursor_framework.session_memory",
    "FileRead": "cursor_framework.session_memory",
    "CursorIntegration": "cursor_framework.cursor_integration",
    
    # Code Graph RAG Integration (optional)
    "CodeGraphRAG": "cursor_framework.integrations.code_graph_rag",
    "is_code_graph_rag_available": "cursor_framework.integrations.code_graph_rag",

    # ECC Integration
    "ECCIntegration": "cursor_framework.ecc_integration",
    "create_ecc_integration": "cursor_framework.ecc_integration",
    "run_ecc_setup": "cursor_framework.ecc_integration",
    "HarnessType": "cursor_framework.ecc_integration",
    "InstallProfile": "cursor_framework.ecc_integration",
    "InstallStatus": "cursor_framework.ecc_integration",
    "ECCStatus": "cursor_framework.ecc_integration",
    "HarnessInfo": "cursor_framework.ecc_integration",
    "ECCComponent": "cursor_framework.ecc_integration",
    "HarnessInstallStatus": "cursor_framework.ecc_integration",
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
    # Cross-Agent Compatibility Layer
    "cross_agent",
    "detect_agent",
    "get_current_agent",
    "get_compatible_skills",
    "detect_skills_from_request",
    "get_skill_definition",
    "get_gates_for_skill",
    "export_skill_manifest",
    "export_all_skills_json",
    "AgentType",
    "GateType",
    "SkillDefinition",
    "GateResult",
    "GateExecutionResult",
    
    # Context Router
    "ContextRouter",
    "IntentClassifier",
    "IntentType",
    "Domain",
    "Skill",
    "SkillRoute",
    
    # Memory Manager
    "MemoryManager",
    "MemoryEntry",
    "MemoryTier",
    "MemoryStore",
    
    # Token Optimizer
    "TokenOptimizer",
    "TokenBudget",
    "CompressionStrategy",
    "CompressionResult",
    
    # Skill Discovery
    "SkillDiscovery",
    "SkillRegistry",
    "CrossAgentSkillDiscovery",
    "GateExecutor",
    
    # Agent Integration
    "AgentDetector",
    "CrossAgentIntegration",
    
    # Indexer & Context Builder
    "Indexer",
    "IndexResult",
    "AssetEntry",
    "ContextBuilder",
    "ContextResult",
    
    # Workflow & Dashboard
    "Workflow",
    "WorkflowResult",
    "Watcher",
    "Dashboard",
    
    # TDAM Integration
    "TDAMIntegration",
    "TDAMClient",
    "TDAMConfig",
    "MemoryLayer",
    "MemoryItem",
    "ConversationTurn",
    "OffloadResult",
    "create_tdam_integration",
    "create_tdam_integration_from_env",
    
    # Code Graph & Memory System
    "CodeGraph",
    "CodeGraphResult",
    "Module",
    "Dependency",
    "SessionMemory",
    "FileRead",
    "CursorIntegration",
    
    # Code Graph RAG Integration (optional)
    "CodeGraphRAG",
    "is_code_graph_rag_available",

    # ECC Integration
    "ECCIntegration",
    "create_ecc_integration",
    "run_ecc_setup",
    "HarnessType",
    "InstallProfile",
    "InstallStatus",
    "ECCStatus",
    "HarnessInfo",
    "ECCComponent",
    "HarnessInstallStatus",
]