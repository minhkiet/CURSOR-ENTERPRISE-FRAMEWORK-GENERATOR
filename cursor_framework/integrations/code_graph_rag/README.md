# Code Graph RAG Integration

> **Version:** 1.0.0 | **Requires:** code-graph-rag | **Created:** 2026-08-16

## Overview

This module provides optional integration with [vitali87/code-graph-rag](https://github.com/vitali87/code-graph-rag) - a powerful RAG system for codebases using knowledge graphs (Memgraph) and vector search (Qdrant).

## Features

- **Knowledge Graph Queries**: Query code structure using Cypher language
- **Semantic Search**: Find similar code using embeddings
- **Code Intelligence**: Understand relationships between files, functions, classes
- **AST-based Analysis**: Deep code structure analysis with tree-sitter

## Requirements

```bash
# Install code-graph-rag with dependencies
uv tool install "code-graph-rag[treesitter-full,semantic]"

# Or with pipx
pipx install "code-graph-rag[treesitter-full,semantic]"

# Start Memgraph + Qdrant
cgr daemon up
```

## Usage

### CLI

```bash
# Parse repository into graph
cgr start --repo-path /path/to/repo --update-graph

# Query the codebase
cgr start --repo-path /path/to/repo
```

### MCP Server

The MCP server is available at `https://github.com/vitali87/code-graph-rag` and can be configured in your MCP settings:

```json
{
  "mcpServers": {
    "code-graph-rag": {
      "command": "cgr",
      "args": ["mcp", "serve"]
    }
  }
}
```

## Architecture

```
Source Code → Tree-sitter Parser → AST → Memgraph Knowledge Graph
                                            ↓
User Query → AI (Cypher Gen) → Cypher Query → Graph Results → Response
```

## Tools Available

| Tool | Description |
|------|-------------|
| `query_code_graph` | Natural language query → Cypher |
| `search_code` | Semantic code search |
| `find_dependencies` | Find file dependencies |
| `analyze_calls` | Analyze function/class calls |
| `find_usages` | Find where symbols are used |
| `list_functions` | List all functions |
| `list_classes` | List all classes |

## Configuration

Environment variables (see `.env.example` in code-graph-rag):

| Variable | Default | Description |
|----------|---------|-------------|
| `MEMGRAPH_HOST` | localhost | Memgraph host |
| `MEMGRAPH_PORT` | 7687 | Memgraph port |
| `QDRANT_HOST` | localhost | Qdrant host |
| `QDRANT_PORT` | 6333 | Qdrant port |

## Integration with Cursor Framework

The `cursor_framework.code_graph` module provides a lightweight alternative for simple dependency graphs without requiring Memgraph/Qdrant. Use code-graph-rag for:

- Large monorepos requiring deep analysis
- Semantic code search with embeddings
- Complex dependency visualization
- AI-powered code understanding

## See Also

- [code-graph-rag GitHub](https://github.com/vitali87/code-graph-rag)
- [Memgraph](https://memgraph.com/)
- [Qdrant](https://qdrant.tech/)
