"""
Cursor Framework - Integrations Module

This module contains optional integrations with external tools and services.

Available integrations:
    - code_graph_rag: Integration with vitali87/code-graph-rag for knowledge graph queries

Usage:
    from cursor_framework.integrations import code_graph_rag
    
    if code_graph_rag.is_available():
        rag = code_graph_rag.CodeGraphRAG()
"""

from cursor_framework.integrations import code_graph_rag

__all__ = ["code_graph_rag"]
