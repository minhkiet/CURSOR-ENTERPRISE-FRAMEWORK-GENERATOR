---
title: "Claude API Glossary"
description: "Từ điển thuật ngữ toàn diện cho Claude API - Anthropic API, Messages API, tool use, token counting, Claude 3 models comparison, production terminology"
tags: ["claude", "glossary", "api", "anthropic", "terminology", "llm", "models", "tokens"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Claude API Glossary

## Tổng quan (Overview)

Tài liệu này cung cấp một glossary toàn diện các thuật ngữ liên quan đến Claude API và Anthropic. Glossary được thiết kế để serve như một reference resource cho developers, architects, và technical stakeholders làm việc với Claude API.

Các thuật ngữ được tổ chức theo các categories logic, từ basic concepts đến advanced topics. Mỗi entry bao gồm: definition, usage context, và related terms. Glossary bao gồm cả technical terminology (API-specific) và conceptual terms (LLM-related).

Glossary là một living document - được update regular basis để reflect new features, terminology changes, và lessons learned từ production deployments. Contributions và corrections được welcome qua standard documentation process.

## Mục đích (Purpose)

Mục tiêu chính của glossary này bao gồm:

1. **Standardize terminology** - Cung cấp consistent definitions across teams
2. **Enable communication** - Giúp technical và non-technical stakeholders communicate effectively
3. **Support onboarding** - Cung cấp reference cho new team members
4. **Reduce ambiguity** - Clear definitions cho complex concepts

## Category A: Core API Concepts

### Anthropic API

**Definition**: The Anthropic API là REST API được cung cấp bởi Anthropic cho phép developers tích hợp Claude vào applications của họ. API hỗ trợ các operations như text generation, multi-turn conversations, tool use, và vision capabilities.

**Usage Context**: "We integrated Claude via the Anthropic API to power our customer support chatbot."

**Related Terms**: Claude API, REST API, Anthropic SDK
**Category**: Core API

---

### Messages API

**Definition**: Messages API là primary API endpoint của Anthropic cho việc tạo conversations. Thay vì legacy text completions API, Messages API cung cấp structured approach cho việc handling multi-turn conversations với support cho system prompts, multiple messages, và various content types.

**Usage Context**: "The Messages API accepts a messages array where each message has a role and content."

**Related Terms**: Anthropic API, Messages endpoint, Completion API
**Category**: Core API

---

### Claude Model

**Definition**: Claude model là một instance của Claude language model được deploy trên Anthropic's infrastructure. Models được identified bằng versioned names (ví dụ: `claude-3-5-sonnet-20241022`) và có different capabilities, pricing, và performance characteristics.

**Usage Context**: "We use Claude 3.5 Sonnet for most tasks due to its balance of capability and cost."

**Related Terms**: Claude 3 Opus, Claude 3.5 Sonnet, Claude 3.5 Haiku, Model version
**Category**: Core API

---

### API Key

**Definition**: API key là unique identifier được sử dụng để authenticate requests đến Anthropic API. Keys được generated từ Anthropic console và nên được stored securely, không bao giờ hardcoded trong source code.

**Usage Context**: "Configure your API key as an environment variable: ANTHROPIC_API_KEY"

**Related Terms**: Authentication, Secret key, Environment variable
**Category**: Core API

---

### Request

**Definition**: Một API request là một HTTP call gửi đến Anthropic API endpoint, bao gồm model specification, messages, parameters, và authentication. Mỗi request được tính phí dựa trên token usage.

**Usage Context**: "Each request must include the model, max_tokens, and messages array."

**Related Terms**: API call, HTTP request, Token usage
**Category**: Core API

---

### Response

**Definition**: API response là data được trả về từ Anthropic API sau khi xử lý request. Response bao gồm generated text content, usage statistics (input/output tokens), và metadata như stop reason.

**Usage Context**: "The response includes content blocks with the generated text and usage information."

**Related Terms**: API response, Content block, Usage
**Category**: Core API

---

## Category B: Message & Conversation

### Message

**Definition**: Message là một unit of communication trong Claude API, bao gồm role (user hoặc assistant) và content. Messages được truyền as an array trong request và đại diện cho conversation history.

**Usage Context**: "The messages array contains the full conversation history from oldest to newest."

**Related Terms**: User message, Assistant message, System prompt, Messages array
**Category**: Message & Conversation

**Structure**:
```json
{
  "role": "user|assistant",
  "content": "Message text or content blocks"
}
```

---

### System Prompt

**Definition**: System prompt là instructions được gửi cùng với mỗi request để define Claude's behavior, persona, và constraints. System prompts set context và guidelines cho generation mà không làm part của conversation history.

**Usage Context**: "Include a system prompt to establish the assistant's role and capabilities."

**Related Terms**: System message, Instructions, Context, Persona
**Category**: Message & Conversation

---

### User Message

**Definition**: User message là message với role "user", đại diện cho input từ end user hoặc system initiating conversation turn.

**Usage Context**: "Format user messages clearly with specific requests or questions."

**Related Terms**: Message, User input, Conversation turn
**Category**: Message & Conversation

---

### Assistant Message

**Definition**: Assistant message là message với role "assistant", đại diện cho Claude's response. Assistant messages được include trong conversation history để maintain context across turns.

**Usage Context**: "Append the assistant's response to the messages array for the next turn."

**Related Terms**: Message, Claude response, Assistant reply
**Category**: Message & Conversation

---

### Messages Array

**Definition**: Messages array là ordered list of messages được gửi trong mỗi API request, chứa toàn bộ conversation history từ oldest đến newest message. Array này xác định context cho generation.

**Usage Context**: "The Messages API requires a messages array with role and content for each message."

**Related Terms**: Conversation history, Message history, Context window
**Category**: Message & Conversation

---

### Multi-turn Conversation

**Definition**: Multi-turn conversation là interaction pattern trong đó multiple message exchanges occur between user và Claude, với conversation history maintained across turns.

**Usage Context**: "Multi-turn conversations require including all prior messages in each request."

**Related Terms**: Conversation, Message history, Turn
**Category**: Message & Conversation

---

### Content Block

**Definition**: Content block là structured element trong Claude's response hoặc message content, có thể chứa text, tool use requests, hoặc other content types. Multiple blocks có thể appear trong một response.

**Usage Context**: "The response content contains blocks of type 'text' or 'tool_use'."

**Related Terms**: Text block, Tool use block, Multi-modal content
**Category**: Message & Conversation

---

### Stop Reason

**Definition**: Stop reason là indicator cho biết tại sao Claude stopped generating, có thể là: `end_turn` (completed normally), `max_tokens` (hit token limit), `stop_sequence` (encountered stop sequence), hoặc `tool_use` (requested tool execution).

**Usage Context**: "Check stop_reason to determine if the response is complete or truncated."

**Related Terms**: End of response, Token limit, Tool use
**Category**: Message & Conversation

---

## Category C: Token & Context

### Token

**Definition**: Token là basic unit of text được processed bởi Claude. Tokens approximate words nhưng không exactly match word boundaries. Average ratio là approximately 4 characters per token for English text.

**Usage Context**: "Tokenize the input to estimate API costs before making a request."

**Related Terms**: Tokenization, Token count, Token limit
**Category**: Token & Context

**Token Examples**:
| Text | Approximate Tokens |
|------|-------------------|
| "hello" | 1-2 |
| "The quick brown fox" | 4 |
| "Vietnam" | 2-3 |

---

### Token Count

**Definition**: Token count là số lượng tokens trong một piece of text, được sử dụng để estimate costs và check against context limits. Anthropic cung cấp `count_tokens` endpoint cho accurate counting.

**Usage Context**: "Use the token counting API to verify request size before sending."

**Related Terms**: Token, Token estimation, Token counting
**Category**: Token & Context

---

### Token Limit

**Definition**: Token limit là maximum number of tokens có thể fit trong một single request, bao gồm input (messages + system) và output (max_tokens parameter). Claude models có different limits.

**Usage Context**: "The 200K token context window includes both input and output tokens."

**Related Terms**: Context window, max_tokens, Context limit
**Category**: Token & Context

---

### Context Window

**Definition**: Context window là total capacity của model cho input tokens + output tokens trong một single request. Claude 3 models có 200K token context window.

**Usage Context**: "The 200K context window allows processing very long documents."

**Related Terms**: Token limit, Context management, Long context
**Category**: Token & Context

---

### Input Tokens

**Definition**: Input tokens là tokens trong phần input của request, bao gồm system prompt và messages array. Input tokens được tính phí theo per-token rate.

**Usage Context**: "Optimize prompts to reduce input token costs."

**Related Terms**: Output tokens, Token pricing, Token usage
**Category**: Token & Context

---

### Output Tokens

**Definition**: Output tokens là tokens được generated trong response. Output tokens được tính phí ở rate cao hơn input tokens và bị giới hạn bởi max_tokens parameter.

**Usage Context**: "Set max_tokens appropriately to balance response length with cost."

**Related Terms**: Input tokens, max_tokens, Token pricing
**Category**: Token & Context

---

### max_tokens

**Definition**: max_tokens là parameter xác định maximum tokens Claude có thể generate trong response. Set quá thấp có thể truncate responses; set quá cao có thể waste tokens.

**Usage Context**: "Set max_tokens to 1024 for concise responses, 4096 for detailed outputs."

**Related Terms**: Output tokens, Token limit, Response length
**Category**: Token & Context

---

### Token Pricing

**Definition**: Token pricing là cost structure cho Claude API, được tính per million tokens với different rates cho input và output tokens, và different rates cho different models.

**Usage Context**: "Claude 3.5 Sonnet costs $3/input million and $15/output million tokens."

**Related Terms**: API cost, Token rate, Model pricing
**Category**: Token & Context

**Pricing Reference** (approximate):
| Model | Input ($/M tokens) | Output ($/M tokens) |
|-------|-------------------|---------------------|
| Claude 3.5 Haiku | $0.25 | $1.25 |
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude 3 Opus | $15.00 | $75.00 |

---

### Token Estimation

**Definition**: Token estimation là technique để approximate token count without calling the API, sử dụng heuristics như character count divided by 4 (for English).

**Usage Context**: "For quick estimates, use 4 characters per token for English text."

**Related Terms**: Token count, Token counting API, Estimation
**Category**: Token & Context

---

### Context Management

**Definition**: Context management là practices và techniques để handle conversation history within token limits, bao gồm truncation, summarization, và strategic message retention.

**Usage Context**: "Implement context management to handle long conversations efficiently."

**Related Terms**: Context window, Truncation, Summarization
**Category**: Token & Context

---

### Truncation

**Definition**: Truncation là process of removing older messages from conversation history khi approaching context limits, để ensure new requests fit within token limits.

**Usage Context**: "Use truncation to keep recent context while staying within limits."

**Related Terms**: Context management, Token limit, History pruning
**Category**: Token & Context

---

### Summarization

**Definition**: Summarization là technique trong đó older conversation history được condensed thành brief summary để save tokens while preserving key information.

**Usage Context**: "Summarize conversation history to maintain context efficiently."

**Related Terms**: Context management, History compression
**Category**: Token & Context

---

## Category D: Model Parameters

### Temperature

**Definition**: Temperature là parameter controlling randomness trong generation. Lower values (靠近 0) produce more deterministic, focused outputs; higher values (靠近 1) produce more creative, varied outputs.

**Usage Context**: "Use temperature=0.7 for balanced creative responses."

**Related Terms**: Sampling, Randomness, Creativity
**Category**: Model Parameters

**Temperature Guide**:
| Value | Characteristics | Use Cases |
|-------|----------------|-----------|
| 0.0-0.3 | Deterministic, focused | Factual, extraction |
| 0.4-0.7 | Balanced | General purpose |
| 0.8-1.0 | Creative, varied | Creative writing |

---

### top_p (Nucleus Sampling)

**Definition**: top_p là nucleus sampling parameter xác định maximum probability mass to consider for token selection. Lower values restrict to more likely tokens; higher values allow more diversity.

**Usage Context**: "Use top_p=0.9 with temperature for balanced creativity."

**Related Terms**: Temperature, Nucleus sampling, Sampling
**Category**: Model Parameters

---

### top_k

**Definition**: top_k là parameter giới hạn token selection chỉ consider top k most likely tokens. This provides another mechanism for controlling output diversity.

**Usage Context**: "Set top_k=40 to limit token selection to top 40 candidates."

**Related Terms**: Temperature, top_p, Token selection
**Category**: Model Parameters

---

### Stop Sequence

**Definition**: Stop sequence là string that, when encountered in output, causes Claude to stop generating. Useful for controlling response boundaries and format.

**Usage Context**: "Use stop_sequence=['```'] to end code blocks properly."

**Related Terms**: Stop reason, Response formatting
**Category**: Model Parameters

---

### Response Format

**Definition**: Response format là specification for how Claude should format outputs, có thể be controlled through prompts và parameters. Common formats include plain text, JSON, và structured formats.

**Usage Context**: "Specify JSON format in system prompt for structured outputs."

**Related Terms**: Output format, Structured output, JSON mode
**Category**: Model Parameters

---

## Category E: Tool Use

### Tool Use

**Definition**: Tool Use (formerly Function Calling) là capability cho phép Claude call external tools và functions được defined trong request. Claude có thể request execution của multiple tools trong một response.

**Usage Context**: "Implement tool use to let Claude query databases and APIs."

**Related Terms**: Function calling, Tool definition, Tool execution
**Category**: Tool Use

---

### Tool Definition

**Definition**: Tool definition là structured specification của một tool, bao gồm name, description, và input_schema xác định parameters tool accepts.

**Usage Context**: "Define tools with clear descriptions to help Claude understand when to use them."

**Related Terms**: Tool schema, Tool specification, Function definition
**Category**: Tool Use

**Example Structure**:
```json
{
  "name": "get_weather",
  "description": "Get weather for a location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {"type": "string"}
    },
    "required": ["location"]
  }
}
```

---

### Tool Use Block

**Definition**: Tool use block là content block trong Claude's response indicating a request to execute a tool, chứa tool name và parameters.

**Usage Context**: "Parse tool_use blocks to extract tool name and input parameters."

**Related Terms**: Content block, Tool call, Tool request
**Category**: Tool Use

---

### Tool Result

**Definition**: Tool result là output từ tool execution được fed back vào Claude as part of conversation, cho phép Claude incorporate real-world data vào responses.

**Usage Context**: "Return tool results as messages with type='tool_result'."

**Related Terms**: Tool execution, Tool output, Tool response
**Category**: Tool Use

---

### Tool Executor

**Definition**: Tool executor là component trong application responsible for executing tools requested by Claude và returning results.

**Usage Context**: "Build a tool executor to handle tool calls securely and efficiently."

**Related Terms**: Tool handler, Tool implementation
**Category**: Tool Use

---

### Multi-tool Scenario

**Definition**: Multi-tool scenario là situation trong đó Claude requests execution của multiple tools, có thể in parallel hoặc sequential.

**Usage Context**: "Handle multi-tool scenarios by executing tools and aggregating results."

**Related Terms**: Tool use, Parallel tool execution
**Category**: Tool Use

---

## Category F: Claude 3 Models

### Claude 3 Opus

**Definition**: Claude 3 Opus là most capable model trong Claude 3 lineup, designed for complex reasoning, analysis, và high-quality generation. Offers highest intelligence at highest cost.

**Usage Context**: "Use Opus for strategic analysis and complex research tasks."

**Related Terms**: Claude 3 Sonnet, Claude 3 Haiku, Model comparison
**Category**: Claude 3 Models

**Characteristics**:
- Intelligence: Highest
- Speed: Slowest
- Cost: Highest
- Best for: Complex reasoning, research, strategic analysis

---

### Claude 3.5 Sonnet

**Definition**: Claude 3.5 Sonnet là balanced model cung cấp excellent performance across most tasks với good cost efficiency. Recommended as default choice cho many use cases.

**Usage Context**: "Claude 3.5 Sonnet is our go-to model for production applications."

**Related Terms**: Claude 3 Opus, Claude 3.5 Haiku, Model selection
**Category**: Claude 3 Models

**Characteristics**:
- Intelligence: High
- Speed: Fast
- Cost: Moderate
- Best for: General purpose, coding, content generation

---

### Claude 3.5 Haiku

**Definition**: Claude 3.5 Haiku là fastest và most cost-efficient model, designed cho high-volume, simple tasks như classification, extraction, và real-time interactions.

**Usage Context**: "Use Haiku for classification and simple extraction tasks."

**Related Terms**: Claude 3.5 Sonnet, Claude 3 Opus, Model selection
**Category**: Claude 3 Models

**Characteristics**:
- Intelligence: Good (for simple tasks)
- Speed: Fastest
- Cost: Lowest
- Best for: Classification, extraction, high-volume simple tasks

---

### Claude 3 Sonnet

**Definition**: Claude 3 Sonnet là earlier version của Sonnet model, replaced by Claude 3.5 Sonnet. Retained for backwards compatibility.

**Usage Context**: "Prefer Claude 3.5 Sonnet over Claude 3 Sonnet for better performance."

**Related Terms**: Claude 3.5 Sonnet, Claude 3 models
**Category**: Claude 3 Models

---

### Model Version

**Definition**: Model version là dated identifier for a specific model release, ví dụ: `claude-3-5-sonnet-20241022`. Versions may have different capabilities và behaviors.

**Usage Context**: "Pin model versions in production for consistent behavior."

**Related Terms**: Model name, Model identifier
**Category**: Claude 3 Models

---

### Model Selection

**Definition**: Model selection là process of choosing appropriate Claude model cho specific task, based on complexity, quality requirements, latency needs, và cost constraints.

**Usage Context**: "Implement model routing to select optimal model per request."

**Related Terms**: Model routing, Cost optimization
**Category**: Claude 3 Models

---

### Model Routing

**Definition**: Model routing là automated system to direct requests to appropriate models based on task characteristics, complexity, và resource requirements.

**Usage Context**: "Build a model router to optimize cost-quality balance."

**Related Terms**: Model selection, Adaptive model selection
**Category**: Claude 3 Models

---

## Category G: Error Handling

### Rate Limit

**Definition**: Rate limit là maximum number of requests hoặc tokens allowed per time period. Exceeding rate limits results in 429 errors và requires retry logic.

**Usage Context**: "Implement exponential backoff when hitting rate limits."

**Related Terms**: Rate limit error, Request limits, Quota
**Category**: Error Handling

---

### Rate Limit Error

**Definition**: Rate limit error (HTTP 429) xảy ra khi API request rate hoặc token usage exceeds limits. Response includes `Retry-After` header indicating when to retry.

**Usage Context**: "Handle rate limit errors with retry logic and backoff."

**Related Terms**: Rate limit, 429 error, Backoff
**Category**: Error Handling

---

### Context Length Exceeded

**Definition**: Context length exceeded error xảy ra khi request size exceeds model's context window limit. Requires truncating messages or reducing prompt size.

**Usage Context**: "Truncate conversation history when hitting context length limits."

**Related Terms**: Token limit, Context window, Truncation
**Category**: Error Handling

---

### Authentication Error

**Definition**: Authentication error (HTTP 401) xảy ra khi API key is invalid, expired, hoặc missing. Requires checking key configuration.

**Usage Context**: "Verify API key is correctly set in environment variables."

**Related Terms**: 401 error, API key, Authentication
**Category**: Error Handling

---

### Server Error

**Definition**: Server error (HTTP 5xx) xảy ra when Anthropic's servers have issues. These are typically temporary và should be handled with retry logic.

**Usage Context**: "Retry server errors with exponential backoff."

**Related Terms**: 500 error, 502 error, 503 error, Retry
**Category**: Error Handling

---

### Timeout

**Definition**: Timeout xảy ra khi request takes too long to complete. Claude API has configurable timeout, và long-running requests should be handled appropriately.

**Usage Context**: "Set appropriate timeout values and handle timeout errors gracefully."

**Related Terms**: Request timeout, Connection timeout
**Category**: Error Handling

---

### Retry Logic

**Definition**: Retry logic là implementation cho handling temporary errors bằng cách re-attempting requests after delays, typically with exponential backoff.

**Usage Context**: "Implement retry logic for rate limits and server errors."

**Related Terms**: Backoff, Error handling, Resilience
**Category**: Error Handling

---

### Exponential Backoff

**Definition**: Exponential backoff là retry strategy trong đó delay between retries increases exponentially (1s, 2s, 4s, 8s...) để avoid overwhelming servers.

**Usage Context**: "Use exponential backoff with jitter for production resilience."

**Related Terms**: Retry logic, Jitter, Rate limit
**Category**: Error Handling

---

### Circuit Breaker

**Definition**: Circuit breaker là pattern để prevent cascade failures bằng cách temporarily stopping requests when error rate exceeds threshold.

**Usage Context**: "Implement circuit breaker to protect against sustained API issues."

**Related Terms**: Error handling, Resilience, Fallback
**Category**: Error Handling

---

## Category H: Streaming & Real-time

### Streaming

**Definition**: Streaming là capability cho phép Claude return response incrementally as tokens are generated, reducing perceived latency for long responses.

**Usage Context**: "Implement streaming for better UX in interactive applications."

**Related Terms**: Stream response, Server-sent events
**Category**: Streaming & Real-time

---

### Stream Response

**Definition**: Stream response là response format trong which content is sent incrementally via Server-Sent Events (SSE), allowing progressive rendering.

**Usage Context**: "Parse stream events to display text as it's generated."

**Related Terms**: Streaming, SSE, Incremental output
**Category**: Streaming & Real-time

---

### Time to First Token (TTFT)

**Definition**: TTFT là metric measuring latency từ request submission đến generation of first token. Important metric cho streaming applications.

**Usage Context**: "Optimize for TTFT in real-time chat applications."

**Related Terms**: Streaming, Latency, Time to last token
**Category**: Streaming & Real-time

---

## Category I: Vision & Multi-modal

### Vision

**Definition**: Vision capability cho phép Claude process images as input, enabling image analysis, document understanding, và visual question answering.

**Usage Context**: "Use vision to analyze screenshots and extract document information."

**Related Terms**: Image input, Multi-modal, Image understanding
**Category**: Vision & Multi-modal

---

### Image Block

**Definition**: Image block là content block chứa image data, either as base64 encoded image hoặc URL reference, sent as part of user message.

**Usage Context**: "Include image blocks in messages to enable vision analysis."

**Related Terms**: Vision, Image input, Content block
**Category**: Vision & Multi-modal

---

### Multi-modal

**Definition**: Multi-modal là capability to process multiple content types (text, images, etc.) in a single request.

**Usage Context**: "Multi-modal models support both text and image inputs."

**Related Terms**: Vision, Multi-content, Image processing
**Category**: Vision & Multi-modal

---

## Category J: SDK & Development

### Anthropic SDK

**Definition**: Anthropic SDK là official library provided by Anthropic for interacting with Claude API, available in Python, TypeScript/JavaScript, và other languages.

**Usage Context**: "Use the Anthropic SDK for type-safe API interactions."

**Related Terms**: API client, SDK, Python SDK, TypeScript SDK
**Category**: SDK & Development

---

### Python SDK

**Definition**: Official Python library for Claude API, installable via pip, providing async support và type hints.

**Usage Context**: "Install Python SDK: pip install anthropic"

**Related Terms**: Anthropic SDK, Python, pip
**Category**: SDK & Development

---

### TypeScript SDK

**Definition**: Official TypeScript library for Claude API, available via npm, with full TypeScript type definitions.

**Usage Context**: "Install TypeScript SDK: npm install @anthropic-ai/sdk"

**Related Terms**: Anthropic SDK, TypeScript, npm
**Category**: SDK & Development

---

### API Client

**Definition**: API client là wrapper class/object abstracting API interactions, providing convenience methods và handling common patterns.

**Usage Context**: "Create an API client class to centralize API logic."

**Related Terms**: SDK, Client wrapper, API abstraction
**Category**: SDK & Development

---

## Category K: Best Practices

### Prompt Engineering

**Definition**: Prompt engineering là practice of crafting effective prompts to achieve desired outputs, including instruction clarity, format specification, và example provision.

**Usage Context**: "Invest in prompt engineering for better response quality."

**Related Terms**: Prompt design, Few-shot learning, In-context learning
**Category**: Best Practices

---

### Few-shot Learning

**Definition**: Few-shot learning là technique trong đó examples are included in prompt to guide Claude toward desired format hoặc behavior.

**Usage Context**: "Use few-shot examples to demonstrate expected output format."

**Related Terms**: Prompt engineering, In-context learning, Examples
**Category**: Best Practices

---

### System Prompt Design

**Definition**: System prompt design là practice of crafting effective system-level instructions defining Claude's role, constraints, và response format.

**Usage Context**: "Structure system prompts with clear sections for role, rules, và format."

**Related Terms**: System prompt, Prompt engineering, Instructions
**Category**: Best Practices

---

### Cost Optimization

**Definition**: Cost optimization là practice of minimizing API costs through model selection, token reduction, caching, và efficient prompt design.

**Usage Context**: "Implement cost optimization to reduce operational expenses."

**Related Terms**: Token optimization, Model selection, Caching
**Category**: Best Practices

---

### Graceful Degradation

**Definition**: Graceful degradation là design pattern trong đó system provides reduced functionality when primary capabilities are unavailable, ensuring continued operation.

**Usage Context**: "Implement graceful degradation when API is unavailable."

**Related Terms**: Fallback, Error handling, Resilience
**Category**: Best Practices

---

## Appendix: Quick Reference Tables

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 400 | Bad request | Check request format |
| 401 | Authentication error | Verify API key |
| 413 | Payload too large | Reduce input size |
| 429 | Rate limit | Retry with backoff |
| 500 | Server error | Retry with backoff |
| 529 | Service overloaded | Retry later |

### Model Comparison Quick Reference

| Model | Use When | Avoid When |
|-------|----------|------------|
| Opus | Complex reasoning, research | Simple tasks, cost-sensitive |
| Sonnet 3.5 | General purpose, balanced | - |
| Haiku | Classification, extraction, high volume | Complex reasoning |

### Token Estimation Quick Reference

| Content Type | Approximate Rate |
|--------------|-----------------|
| English text | 4 chars = 1 token |
| Vietnamese text | 2-3 chars = 1 token |
| Code | 3-4 chars = 1 token |
| Numbers | 1-2 chars = 1 token |

## References

- [Anthropic API Documentation](https://docs.anthropic.com/claude/docs)
- [API Reference](https://docs.anthropic.com/claude/reference)
- [Model Pricing](https://www.anthropic.com/pricing)
- [SDK Documentation](https://docs.anthropic.com/claude/sdk)
