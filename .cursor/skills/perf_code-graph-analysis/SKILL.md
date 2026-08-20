# Code Graph Analysis Skill

**Version:** 1.0.0  
**Created:** 2026-08-16  
**Category:** Code Intelligence  
**Confidence:** 0.85  
**Triggers:** ["code graph", "dependency analysis", "knowledge graph", "cypher", "codebase query", "code search"]

## Overview

This skill provides code graph analysis capabilities using [code-graph-rag](https://github.com/vitali87/code-graph-rag) - a powerful RAG system that builds knowledge graphs from codebases.

## When to Use

Use this skill when you need to:

- **Understand code structure** - Find relationships between files, classes, functions
- **Trace dependencies** - Map how modules depend on each other
- **Semantic search** - Find similar code using embeddings
- **Query codebase** - Ask natural language questions about code
- **Refactor safely** - Understand impact before making changes

## Pre-Gates

1. Verify code-graph-rag is installed: `cgr --version`
2. Check Memgraph + Qdrant services: `cgr daemon status`
3. Confirm project is indexed: Check graph stats

## Tools Available

| Tool | Purpose |
|------|---------|
| `query_code_graph` | Natural language → Cypher query |
| `search_code` | Semantic code search |
| `find_dependencies` | Find what a file depends on |
| `find_dependents` | Find what depends on a file |
| `analyze_calls` | Trace function/class call chains |
| `find_usages` | Find where a symbol is used |
| `list_functions` | List all functions |
| `list_classes` | List all classes |
| `list_modules` | List all modules |

## Example Queries

### Find dependencies
```
"How is the database connection handled?"
"What files import the auth module?"
"Show me the call chain for user authentication"
```

### Understand structure
```
"What are the main components?"
"List all API endpoints"
"What classes handle payment processing?"
```

### Refactoring support
```
"What would break if I change this function?"
"Find all places that use this utility"
"Where is error handling implemented?"
```

## Usage

### MCP Server
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

### Python API
```python
from cursor_framework.integrations.code_graph_rag import CodeGraphRAG

rag = CodeGraphRAG(project_root=".")
await rag.index()
results = await rag.query("How is auth implemented?")
```

## Dependencies

- Memgraph (graph database)
- Qdrant (vector search)
- Tree-sitter parsers

## Alternative

For simple dependency graphs without external services, use `cursor_framework.code_graph.CodeGraph` which provides basic file dependency tracking.

## Post-Gates

1. Verify query results match expectations
2. Check all referenced files exist
3. Validate dependency chains are complete
