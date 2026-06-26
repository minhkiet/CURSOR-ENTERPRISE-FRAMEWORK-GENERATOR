# WeKnora MCP Configuration Guide

## Overview

WeKnora provides an MCP (Model Context Protocol) server that allows AI agents like Cursor, Claude Code, and Aider to interact with WeKnora's knowledge bases through standardized tool calls.

## MCP Server Setup

### 1. Install WeKnora CLI

```bash
# macOS
brew install weknora

# Linux
curl -fsSL https://get.weknora.com/install.sh | sh

# Windows
# Download from https://github.com/Tencent/WeKnora/releases
```

### 2. Start MCP Server

```bash
# Start with stdio transport (for Cursor)
weknora mcp serve

# Start with SSE transport (for remote access)
weknora mcp serve --transport sse --port 8081

# Start with HTTP transport
weknora mcp serve --transport http --port 8082
```

### 3. Configure Environment Variables

```bash
# .env file
WEKNORA_HOST=http://localhost:8080
WEKNORA_API_KEY=your-api-key
WEKNORA_MCP_TRANSPORT=stdio
```

## Cursor MCP Configuration

### Option 1: Via Cursor Settings (GUI)

1. Open Cursor Settings → MCP Servers
2. Click "Add MCP Server"
3. Configure:
   - **Name**: `weknora`
   - **Command**: `weknora`
   - **Arguments**: `mcp serve`
   - **Environment**: Add `WEKNORA_HOST`, `WEKNORA_API_KEY`

### Option 2: Via Configuration File

```jsonc
// Windows: %USERPROFILE%\.cursor\mcp.json
// macOS: ~/.cursor/mcp.json

{
  "mcpServers": {
    "weknora": {
      "command": "weknora",
      "args": ["mcp", "serve"],
      "env": {
        "WEKNORA_HOST": "http://localhost:8080",
        "WEKNORA_API_KEY": "${WEKNORA_API_KEY}"
      }
    }
  }
}
```

### Option 3: Project-Specific Configuration

```jsonc
// In your project: .cursor/mcp.json

{
  "mcpServers": {
    "weknora": {
      "command": "weknora",
      "args": ["mcp", "serve", "--transport", "stdio"],
      "cwd": "${workspaceFolder}",
      "env": {
        "WEKNORA_HOST": "http://localhost:8080",
        "WEKNORA_API_KEY": "${env:WEKNORA_API_KEY}"
      }
    }
  }
}
```

## Available MCP Tools

### Knowledge Base Management

```json
{
  "name": "weknora_kb_list",
  "description": "List all knowledge bases",
  "inputSchema": {
    "type": "object",
    "properties": {}
  }
}
```

```json
{
  "name": "weknora_kb_create",
  "description": "Create a new knowledge base",
  "inputSchema": {
    "type": "object",
    "properties": {
      "name": { "type": "string" },
      "type": { "type": "string", "enum": ["faq", "document", "wiki"] },
      "description": { "type": "string" }
    },
    "required": ["name", "type"]
  }
}
```

### Document Operations

```json
{
  "name": "weknora_doc_upload",
  "description": "Upload a document to knowledge base",
  "inputSchema": {
    "type": "object",
    "properties": {
      "file_path": { "type": "string" },
      "kb_id": { "type": "string" },
      "parser": { "type": "string", "enum": ["builtin", "paddleocr", "opendata"] },
      "chunk_size": { "type": "number" }
    },
    "required": ["file_path", "kb_id"]
  }
}
```

```json
{
  "name": "weknora_doc_list",
  "description": "List documents in a knowledge base",
  "inputSchema": {
    "type": "object",
    "properties": {
      "kb_id": { "type": "string" },
      "limit": { "type": "number", "default": 20 }
    },
    "required": ["kb_id"]
  }
}
```

```json
{
  "name": "weknora_doc_delete",
  "description": "Delete a document",
  "inputSchema": {
    "type": "object",
    "properties": {
      "doc_id": { "type": "string" },
      "kb_id": { "type": "string" }
    },
    "required": ["doc_id", "kb_id"]
  }
}
```

### Search & Chat

```json
{
  "name": "weknora_search",
  "description": "Search knowledge base",
  "inputSchema": {
    "type": "object",
    "properties": {
      "kb_id": { "type": "string" },
      "query": { "type": "string" },
      "mode": { "type": "string", "enum": ["qa", "agent"], "default": "qa" },
      "top_k": { "type": "number", "default": 10 }
    },
    "required": ["kb_id", "query"]
  }
}
```

```json
{
  "name": "weknora_chat",
  "description": "Chat with knowledge base using agent",
  "inputSchema": {
    "type": "object",
    "properties": {
      "kb_id": { "type": "string" },
      "message": { "type": "string" },
      "session_id": { "type": "string" },
      "stream": { "type": "boolean", "default": false }
    },
    "required": ["kb_id", "message"]
  }
}
```

### Session Management

```json
{
  "name": "weknora_session_list",
  "description": "List chat sessions",
  "inputSchema": {
    "type": "object",
    "properties": {
      "kb_id": { "type": "string" },
      "limit": { "type": "number", "default": 20 }
    }
  }
}
```

```json
{
  "name": "weknora_session_history",
  "description": "Get session conversation history",
  "inputSchema": {
    "type": "object",
    "properties": {
      "session_id": { "type": "string" }
    },
    "required": ["session_id"]
  }
}
```

```json
{
  "name": "weknora_session_stop",
  "description": "Stop a running agent session",
  "inputSchema": {
    "type": "object",
    "properties": {
      "session_id": { "type": "string" }
    },
    "required": ["session_id"]
  }
}
```

## Example Usage in Cursor

### Agent Mode with WeKnora

```
You: @weknora Search my knowledge base for information about RAG implementation

Agent calls weknora_search:
{
  "kb_id": "my-kb-123",
  "query": "RAG implementation best practices",
  "mode": "agent",
  "top_k": 10
}

Result: Returns relevant documents and agent reasoning...
```

### Document Upload Flow

```
You: @weknora Upload the API docs PDF to my knowledge base

Agent calls weknora_doc_upload:
{
  "file_path": "./docs/api.pdf",
  "kb_id": "my-kb-123",
  "parser": "paddleocr"
}

Result: Document indexed successfully...
```

## Advanced Configuration

### MCP with SSE Transport

```bash
# Server side (on WeKnora host)
weknora mcp serve --transport sse --port 8081

# Client side (Cursor)
weknora mcp connect --url http://your-server:8081/mcp
```

### MCP with HTTP Transport

```json
// .cursor/mcp.json
{
  "mcpServers": {
    "weknora": {
      "command": "weknora",
      "args": ["mcp", "connect", "--url", "http://your-server:8082/mcp"],
      "env": {
        "WEKNORA_API_KEY": "${WEKNORA_API_KEY}"
      }
    }
  }
}
```

### MCP with Authentication

```bash
# Login first
weknora auth login --host https://kb.example.com

# Server will use stored credentials
weknora mcp serve
```

## Troubleshooting

### MCP Server Not Starting

```bash
# Check if weknora is installed
weknora --version

# Verify configuration
weknora mcp status

# Check logs
weknora mcp debug
```

### Authentication Errors

```bash
# Re-authenticate
weknora auth logout
weknora auth login --host http://localhost:8080

# Check API key
echo $WEKNORA_API_KEY
```

### Connection Refused

```bash
# Check if WeKnora server is running
docker compose ps

# Verify port accessibility
curl http://localhost:8080/health
```

## Multi-Transport Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    WeKnora MCP Architecture                       │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐                                              │
│   │   Cursor    │                                              │
│   │  (client)   │                                              │
│   └──────┬──────┘                                              │
│          │                                                     │
│          │ stdio / HTTP / SSE                                 │
│          │                                                     │
│   ┌──────▼──────┐     ┌─────────────────────┐                 │
│   │ weknora mcp │────▶│   WeKnora Server    │                 │
│   │   serve     │     │   (localhost)       │                 │
│   └─────────────┘     └─────────────────────┘                 │
│                                              │                  │
│   Transport Types:                           │                  │
│   • stdio: Direct pipe                     │                  │
│   • SSE: Server-Sent Events                │                  │
│   • HTTP: REST-like polling                 │                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Security Considerations

- API keys are encrypted at rest
- TLS recommended for remote MCP connections
- Rate limiting applies to all MCP calls
- Audit logging captures all operations
- SSRF protection enabled by default
