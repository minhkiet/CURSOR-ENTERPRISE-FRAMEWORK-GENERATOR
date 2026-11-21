"""
Vibe Enterprise Framework - Python Core Library

A comprehensive Python library supporting the Vibe Enterprise Framework rules and skills.
Provides utilities for context routing, memory management, token optimization, and skill discovery.

Supports multiple vibe coding agents:
- Cursor IDE
- OpenAI Codex
- Claude Code
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

Author: Vibe Enterprise Framework
Version: 1.6.0
"""

from __future__ import annotations

import importlib

__version__ = "1.6.0"
__author__ = "Vibe Enterprise Framework"

# Lazy attribute access (PEP 562): importing `vibe_framework` does not
# load Dashboard/Workflow/Watcher/Indexer. Submodules are imported on
# first attribute access so cold-start CLI subcommands that only need
# argparse + __version__ stay fast.
_LAZY_EXPORTS = {
    # Cross-Agent Compatibility Layer
    "cross_agent": "vibe_framework.cross_agent",
    "detect_agent": "vibe_framework.cross_agent",
    "get_current_agent": "vibe_framework.cross_agent",
    "get_compatible_skills": "vibe_framework.cross_agent",
    "detect_skills_from_request": "vibe_framework.cross_agent",
    "get_skill_definition": "vibe_framework.cross_agent",
    "get_gates_for_skill": "vibe_framework.cross_agent",
    "export_skill_manifest": "vibe_framework.cross_agent",
    "export_all_skills_json": "vibe_framework.cross_agent",
    "AgentType": "vibe_framework.cross_agent",
    "GateType": "vibe_framework.cross_agent",
    "SkillDefinition": "vibe_framework.cross_agent",
    "GateResult": "vibe_framework.cross_agent",
    "GateExecutionResult": "vibe_framework.cross_agent",
    
    # Context Router
    "ContextRouter": "vibe_framework.context_router",
    "IntentClassifier": "vibe_framework.context_router",
    "IntentType": "vibe_framework.context_router",
    "Domain": "vibe_framework.context_router",
    "Skill": "vibe_framework.context_router",
    "SkillRoute": "vibe_framework.context_router",
    
    # Memory Manager
    "MemoryManager": "vibe_framework.memory_manager",
    "MemoryEntry": "vibe_framework.memory_manager",
    "MemoryTier": "vibe_framework.memory_manager",
    "MemoryStore": "vibe_framework.memory_store",
    
    # Token Optimizer
    "TokenOptimizer": "vibe_framework.token_optimizer",
    "TokenBudget": "vibe_framework.token_optimizer",
    "CompressionStrategy": "vibe_framework.token_optimizer",
    "CompressionResult": "vibe_framework.token_optimizer",
    
    # Skill Discovery
    "SkillDiscovery": "vibe_framework.skill_discovery",
    "SkillRegistry": "vibe_framework.skill_discovery",
    "CrossAgentSkillDiscovery": "vibe_framework.skill_discovery",
    "GateExecutor": "vibe_framework.skill_discovery",
    "GateType": "vibe_framework.skill_discovery",
    "GateResult": "vibe_framework.skill_discovery",
    
    # Agent Integration
    "AgentDetector": "vibe_framework.agent_integration",
    "AgentType": "vibe_framework.agent_integration",
    "CrossAgentIntegration": "vibe_framework.agent_integration",
    
    # Indexer & Context Builder
    "Indexer": "vibe_framework.indexer",
    "IndexResult": "vibe_framework.indexer",
    "AssetEntry": "vibe_framework.indexer",
    "ContextBuilder": "vibe_framework.context_builder",
    "ContextResult": "vibe_framework.context_builder",
    
    # Workflow & Dashboard
    "Workflow": "vibe_framework.workflow",
    "WorkflowResult": "vibe_framework.workflow",
    "Watcher": "vibe_framework.watcher",
    "Dashboard": "vibe_framework.dashboard",
    
    # TDAM Integration
    "TDAMIntegration": "vibe_framework.tdam_integration",
    "TDAMClient": "vibe_framework.tdam_integration",
    "TDAMConfig": "vibe_framework.tdam_integration",
    "MemoryLayer": "vibe_framework.tdam_integration",
    "MemoryItem": "vibe_framework.tdam_integration",
    "ConversationTurn": "vibe_framework.tdam_integration",
    "OffloadResult": "vibe_framework.tdam_integration",
    "create_tdam_integration": "vibe_framework.tdam_integration",
    "create_tdam_integration_from_env": "vibe_framework.tdam_integration",

    # Vibe Coding Multi-Tool Engine
    "VibeTool": "vibe_framework.vibe_sync",
    "VibeDetector": "vibe_framework.vibe_sync",
    "VibeSyncEngine": "vibe_framework.vibe_sync",
    "VibeSyncReport": "vibe_framework.vibe_sync",
    "get_vibe_summary": "vibe_framework.vibe_sync",

    # Redis Observability & Storage
    "RedisObservability": "vibe_framework.redis_store",
    "RedisMemoryStore": "vibe_framework.redis_store",
    "RedisMetricSnapshot": "vibe_framework.redis_store",
    "SlowlogEntry": "vibe_framework.redis_store",

    # Prefect Orchestration
    "prefect_flows": "vibe_framework.prefect_flows",
    "index_and_warm_flow": "vibe_framework.prefect_flows",
    "vibe_sync_flow": "vibe_framework.prefect_flows",
    "health_flow": "vibe_framework.prefect_flows",
    "full_maintenance_pipeline": "vibe_framework.prefect_flows",
    
    # Code Graph & Memory System
    "CodeGraph": "vibe_framework.code_graph",
    "CodeGraphResult": "vibe_framework.code_graph",
    "Module": "vibe_framework.code_graph",
    "Dependency": "vibe_framework.code_graph",
    "SessionMemory": "vibe_framework.session_memory",
    "FileRead": "vibe_framework.session_memory",
    "CursorIntegration": "vibe_framework.cursor_integration",
    
    # Code Graph RAG Integration (optional)
    "CodeGraphRAG": "vibe_framework.integrations.code_graph_rag",
    "is_code_graph_rag_available": "vibe_framework.integrations.code_graph_rag",

    # ECC Integration
    "ECCIntegration": "vibe_framework.ecc_integration",
    "create_ecc_integration": "vibe_framework.ecc_integration",
    "run_ecc_setup": "vibe_framework.ecc_integration",
    "HarnessType": "vibe_framework.ecc_integration",
    "InstallProfile": "vibe_framework.ecc_integration",
    "InstallStatus": "vibe_framework.ecc_integration",
    "ECCStatus": "vibe_framework.ecc_integration",
    "HarnessInfo": "vibe_framework.ecc_integration",
    "ECCComponent": "vibe_framework.ecc_integration",
    "HarnessInstallStatus": "vibe_framework.ecc_integration",
}


def __getattr__(name: str):
    module_name = _LAZY_EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module 'vibe_framework' has no attribute {name!r}")
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
