---
description: WeKnora Agent Skill - ReAct autonomous reasoning agent với multi-step planning, tool calling, web search, và MCP tools integration
created: 2026-06-26
version: 1.0.0
tags: [weknora, react-agent, autonomous, reasoning, agent, tool-calling, web-search, mcp, multi-step, workflow]
---

# WeKnora Agent Skill

## Mục tiêu

Tận dụng WeKnora ReAct Agent để:
- Autonomous reasoning với multi-step planning
- Orchestrate giữa knowledge retrieval, external tools, và LLM
- Tích hợp Web Search cho current information
- Sử dụng MCP Tools để mở rộng năng lực
- Xử lý complex multi-step tasks tự động

## Pre-Review Gate

### A.1 Task Analysis

**1. Identify Task Type:**
- [ ] Simple Q&A (use QA mode instead)
- [ ] Multi-step reasoning (use Agent mode)
- [ ] Research task (Agent + Web search)
- [ ] Complex workflow (Agent + MCP tools)

**2. Tool Requirements:**
- [ ] Knowledge retrieval needed?
- [ ] Web search required?
- [ ] External MCP tools needed?
- [ ] Custom tool development required?

**3. Safety Considerations:**
- [ ] Human-in-the-loop required?
- [ ] Action approval thresholds defined?
- [ ] Rate limits understood?
- [ ] Error handling planned?

### A.2 Agent Configuration

**1. LLM Settings:**
- [ ] Model selected (GPT-4/Claude/DeepSeek)
- [ ] Temperature configured (0.3 for factual, 0.7 for creative)
- [ ] Max tokens set appropriately
- [ ] Thinking mode enabled (if supported)

**2. Loop Configuration:**
- [ ] Max steps defined (prevent infinite loops)
- [ ] Timeout configured
- [ ] Error handling strategy defined
- [ ] Fallback response prepared

**3. Tool Configuration:**
- [ ] Knowledge search tool configured
- [ ] Web search provider set (DuckDuckGo/Bing/Google)
- [ ] MCP tools registered
- [ ] Tool permissions defined

---

## Implementation

### Phase 1: Agent Setup

```bash
# Configure agent mode in WeKnora
weknora agent config \
  --model gpt-4-turbo \
  --temperature 0.3 \
  --max-steps 10 \
  --thinking-mode

# Enable web search
weknora agent config --web-search-provider duckduckgo

# Register MCP tools
weknora mcp add my-tools --command "node ./my-mcp-server.js"
```

### Phase 2: Task Execution

```bash
# Start agent session
weknora chat "Analyze the codebase and suggest improvements" \
  --kb "my-kb" \
  --mode agent \
  --stream

# With specific tools
weknora chat "Research latest AI trends and summarize" \
  --kb "tech-kb" \
  --mode agent \
  --tools web-search,knowledge \
  --max-steps 15
```

### Phase 3: Integration

```typescript
// Agent integration
async function runAgentTask(query: string, options?: AgentOptions) {
  const session = await client.chat({
    kbId: options?.kbId || 'default',
    message: query,
    mode: 'agent',
    stream: options?.stream || false,
    tools: options?.tools || ['knowledge', 'web-search'],
    maxSteps: options?.maxSteps || 10
  });

  return session;
}

// Streaming response
const stream = await client.chat({
  kbId: 'research-kb',
  message: 'Research the impact of AI on software development',
  mode: 'agent',
  stream: true
});

for await (const chunk of stream) {
  process.stdout.write(chunk);
}
```

---

## ReAct Loop Visualization

```
┌─────────────────────────────────────────────────────────────┐
│                    ReAct Agent Loop                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────┐                                              │
│   │  START  │ ──▶ User Query                               │
│   └────┬────┘                                              │
│        │                                                   │
│        ▼                                                   │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐              │
│   │  THINK  │───▶│   ACT   │───▶│ OBSERVE │              │
│   │         │    │         │    │         │              │
│   └────┬────┘    └────┬────┘    └────┬────┘              │
│        │              │              │                      │
│        │              │              ▼                      │
│        │              │         ┌─────────┐                 │
│        │              │         │DECISION │                 │
│        │              │         └────┬────┘                 │
│        │              │              │                      │
│        │              ▼              ▼                      │
│        │         ┌────────────────────────┐             │
│        │         │  Continue or Finalize?   │             │
│        │         └───────────┬──────────────┘             │
│        │                     │                             │
│        │         ┌─────────┴─────────┐                    │
│        │         │                 │                      │
│        ▼         ▼                 │                      │
│   ┌─────────┐                      │                      │
│   │ Continue│                      │                      │
│   └────┬────┘                      │                      │
│        │                           ▼                      │
│        │                    ┌─────────────┐                │
│        │                    │ FINAL      │                │
│        │                    │ ANSWER     │                │
│        │                    └─────────────┘                │
│        │                                                   │
│        └─────────────────────────────────────────────────┘
│                                                             │
│   Tools Available:                                          │
│   - knowledge_search: Vector + BM25 + GraphRAG            │
│   - web_search: DuckDuckGo, Bing, Google, Tavily         │
│   - mcp_call: External MCP tools                         │
│   - final_answer: Complete task                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Post-Review Gate

### A.3 Result Verification

**1. Reasoning Quality:**
- [ ] Reasoning steps logical
- [ ] Tool usage appropriate
- [ ] Conclusions supported by evidence
- [ ] No hallucinations detected

**2. Tool Execution:**
- [ ] Knowledge retrieval relevant
- [ ] Web search results current
- [ ] MCP tools responses correct
- [ ] No tool failures

**3. Output Quality:**
- [ ] Response comprehensive
- [ ] Citations provided
- [ ] Confidence appropriate
- [ ] Format acceptable

### A.4 Performance Check

**1. Latency:**
- [ ] Total execution time acceptable
- [ ] Per-step latency reasonable
- [ ] Tool call latency optimized
- [ ] Streaming feedback adequate

**2. Resource Usage:**
- [ ] Token count within budget
- [ ] No infinite loops (max steps respected)
- [ ] Memory usage reasonable
- [ ] Error handling graceful

### A.5 Safety Verification

**1. Guardrails:**
- [ ] No harmful content generated
- [ ] Rate limits respected
- [ ] Human-in-the-loop triggers working
- [ ] Error messages safe

**2. Security:**
- [ ] API keys not exposed
- [ ] Tool permissions enforced
- [ ] Audit logging enabled
- [ ] SSRF protection active

---

## Tool Reference

### Built-in Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `knowledge_search` | Search KB with hybrid retrieval | `query`, `topK`, `mode` |
| `web_search` | Search the internet | `query`, `provider`, `topK` |
| `final_answer` | Provide final response | `answer`, `reasoning` |

### MCP Tool Integration

```typescript
// Custom MCP tool registration
await client.mcp.register({
  name: 'code-search',
  description: 'Search code in repository',
  schema: {
    query: { type: 'string', required: true },
    lang: { type: 'string', required: false }
  },
  handler: async (params) => {
    return searchCode(params.query, params.lang);
  }
});
```

---

## Configuration Examples

### Research Agent

```yaml
agent:
  model: "gpt-4-turbo"
  temperature: 0.3
  max_steps: 15
  
  tools:
    - knowledge_search
    - web_search
    - mcp:github-tools
  
  web_search:
    provider: "duckduckgo"
    top_k: 5
  
  safety:
    human_in_the_loop: true
    approval_threshold: "sensitive_actions"
```

### Code Analysis Agent

```yaml
agent:
  model: "claude-3-opus"
  temperature: 0.2
  max_steps: 20
  
  tools:
    - knowledge_search
    - mcp:code-analysis
    - mcp:git-tools
  
  safety:
    code_execution_approval: true
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Infinite loop | Set max_steps, add timeout |
| Poor results | Tune retrieval weights, enable reranking |
| Tool failures | Check MCP server, verify permissions |
| Hallucinations | Lower temperature, add context, enable citations |

---

## Liên kết

- [[weknora]] - WeKnora Rule
- [[weknora-kb]] - Knowledge Base Skill
- [[weknora-knowledge/architecture]] - Architecture Details
- [[weknora-knowledge/mcp-integration]] - MCP Setup
