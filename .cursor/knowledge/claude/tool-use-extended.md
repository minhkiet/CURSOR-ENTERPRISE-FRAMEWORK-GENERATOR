---
title: "Tool Use Extended với Claude"
description: "Hướng dẫn Tool Use (formerly Function Calling) cho Claude API - tool definitions, tool results, multi-turn tool use, streaming với tools"
tags: ["claude", "tool-use", "function-calling", "tools", "api", "extended"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Tool Use Extended với Claude

## Tổng quan (Overview)

Tool Use (trước đây gọi là Function Calling) là một trong những tính năng mạnh mẽ nhất của Claude API, cho phép Claude tương tác với external tools và services. Thay vì chỉ generate text, Claude có thể "gọi" các functions được định nghĩa trước để thực hiện actions như truy vấn database, call APIs, search web, execute code, và nhiều hơn nữa.

Trong môi trường enterprise, Tool Use là nền tảng cho việc xây dựng các AI agents phức tạp, automation workflows, và conversational interfaces có khả năng thực hiện real-world actions.

Tài liệu này cung cấp hướng dẫn toàn diện về việc implement Tool Use từ basic definitions đến advanced patterns như multi-turn conversations với tools và streaming responses.

## Mục đích (Purpose)

Mục tiêu của tài liệu này bao gồm:

1. **Hiểu cơ chế Tool Use** - Cách Claude xác định khi nào cần gọi tool
2. **Định nghĩa Tools** - Cấu trúc và best practices cho tool definitions
3. **Xử lý Tool Results** - Cách handle và format results từ tools
4. **Multi-turn Tool Use** - Xây dựng conversations có nhiều tool calls
5. **Streaming với Tools** - Kết hợp streaming và tool use
6. **Error Handling** - Chiến lược xử lý lỗi trong tool execution

## Khái niệm cốt lõi (Key Concepts)

### 1. Tool Use Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INPUT                               │
│                   "Tìm kiếm sản phẩm iPhone"                    │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLAUDE PROCESSES INPUT                        │
│              (determines need for tools)                        │
└─────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
         ┌─────────────────┐       ┌─────────────────┐
         │   NO TOOL CALL  │       │  TOOL CALL(s)  │
         │  (direct reply) │       │  (tool_use)     │
         └─────────────────┘       └─────────────────┘
                                          │
                                          ▼
                           ┌─────────────────────────────────┐
                           │    RETURN TOOL CALL RESULT       │
                           │  {"name": "search_products",    │
                           │   "input": {"query": "iPhone"}} │
                           └─────────────────────────────────┘
                                          │
                                          ▼
                           ┌─────────────────────────────────┐
                           │      EXTERNAL TOOL EXECUTES      │
                           │      (your code)                 │
                           └─────────────────────────────────┘
                                          │
                                          ▼
                           ┌─────────────────────────────────┐
                           │      TOOL RESULT SENT BACK       │
                           │  (as assistant message)          │
                           └─────────────────────────────────┘
                                          │
                                          ▼
                           ┌─────────────────────────────────┐
                           │  CLAUDE GENERATES FINAL RESPONSE │
                           │  (incorporating tool results)     │
                           └─────────────────────────────────┘
```

### 2. Tool Call Structure

Một tool call từ Claude bao gồm:

```json
{
  "type": "tool_use",
  "id": "toolu_01ABC123",
  "name": "search_products",
  "input": {
    "query": "iPhone 15",
    "category": "electronics",
    "max_results": 5
  }
}
```

### 3. Tool Result Structure

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_01ABC123",
  "content": "Kết quả từ tool dưới dạng text..."
}
```

## Tool Definitions

### 1. Basic Tool Definition Structure

```typescript
interface ToolDefinition {
  name: string;
  description: string;
  input_schema: {
    type: "object";
    properties: Record<string, ToolProperty>;
    required?: string[];
  };
}

interface ToolProperty {
  type: "string" | "number" | "boolean" | "object" | "array";
  description: string;
  enum?: string[];
  default?: unknown;
  minimum?: number;
  maximum?: number;
}
```

### 2. Real-World Tool Examples

#### Example 1: Product Search Tool

```typescript
const searchProductsTool: ToolDefinition = {
  name: "search_products",
  description: `Tìm kiếm sản phẩm trong catalog.
  
  Sử dụng tool này khi:
  - User muốn tìm sản phẩm cụ thể
  - User muốn so sánh giá sản phẩm
  - User hỏi về availability của sản phẩm
  
  Không sử dụng cho:
  - General questions không liên quan đến sản phẩm
  - Questions về orders hoặc shipping`,
  
  input_schema: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "Search query - có thể là tên sản phẩm, brand, hoặc mô tả"
      },
      category: {
        type: "string",
        description: "Product category để filter (electronics, fashion, home, etc.)",
        enum: ["electronics", "fashion", "home", "beauty", "sports", "books", "all"]
      },
      min_price: {
        type: "number",
        description: "Minimum price filter (VND)"
      },
      max_price: {
        type: "number",
        description: "Maximum price filter (VND)"
      },
      max_results: {
        type: "integer",
        description: "Maximum number of results to return",
        default: 10,
        minimum: 1,
        maximum: 50
      },
      sort_by: {
        type: "string",
        description: "Sort results by",
        enum: ["relevance", "price_asc", "price_desc", "newest"],
        default: "relevance"
      }
    },
    required: ["query"]
  }
};
```

#### Example 2: Database Query Tool

```python
import json
from typing import Any

def create_database_tool() -> dict[str, Any]:
    """Create a safe database query tool definition."""
    
    return {
        "name": "query_database",
        "description": """Execute a SELECT query on the database to retrieve data.
        
        Sử dụng khi:
        - User cần lấy data từ database
        - User muốn kiểm tra records
        - Reporting và analytics queries
        
        CHỈ hỗ trợ SELECT queries - không có INSERT, UPDATE, DELETE.
        
        Kết quả trả về dưới dạng JSON array.""",
        
        "input_schema": {
            "type": "object",
            "properties": {
                "table": {
                    "type": "string",
                    "description": "Tên bảng cần query",
                    "enum": ["customers", "orders", "products", "inventory", "transactions"]
                },
                "columns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Danh sách columns cần select. Dùng ['*'] cho tất cả."
                },
                "where": {
                    "type": "object",
                    "description": "Filter conditions dưới dạng key-value pairs",
                    "additionalProperties": {
                        "type": "string"
                    }
                },
                "order_by": {
                    "type": "object",
                    "description": "Order clause, ví dụ: {\"column\": \"created_at\", \"direction\": \"DESC\"}"
                },
                "limit": {
                    "type": "integer",
                    "description": "Giới hạn số rows trả về",
                    "minimum": 1,
                    "maximum": 1000,
                    "default": 100
                }
            },
            "required": ["table"]
        }
    }
```

#### Example 3: Calendar/Scheduling Tool

```typescript
const scheduleTool: ToolDefinition = {
  name: "manage_calendar",
  description: `Quản lý lịch và cuộc hẹn.
  
  Tool này có thể:
  - Tạo cuộc hẹn mới
  - Kiểm tra availability
  - Cập nhật hoặc hủy cuộc hẹn
  - Liệt kê cuộc hẹn trong khoảng thời gian
  
  Luôn kiểm tra availability trước khi tạo cuộc hẹn mới.`,
  
  input_schema: {
    type: "object",
    properties: {
      action: {
        type: "string",
        description: "Action to perform",
        enum: ["check_availability", "create_event", "update_event", "delete_event", "list_events"]
      },
      event_id: {
        type: "string",
        description: "Event ID (required for update/delete)"
      },
      title: {
        type: "string",
        description: "Tiêu đề cuộc hẹn"
      },
      description: {
        type: "string",
        description: "Mô tả chi tiết cuộc hẹn"
      },
      start_time: {
        type: "string",
        description: "Start time (ISO 8601 format, e.g., 2024-03-15T09:00:00+07:00)"
      },
      end_time: {
        type: "string",
        description: "End time (ISO 8601 format)"
      },
      attendee_emails: {
        type: "array",
        items: {"type": "string", "format": "email"},
        description: "Danh sách email người tham gia"
      },
      timezone: {
        type: "string",
        description: "Timezone cho cuộc hẹn",
        default: "Asia/Ho_Chi_Minh"
      },
      location: {
        type: "string",
        description: "Địa điểm hoặc meeting link"
      },
      date_range": {
        type: "object",
        description: "Date range cho list_events",
        properties: {
          start: {"type": "string", "description": "Start date (YYYY-MM-DD)"},
          end": {"type": "string", "description": "End date (YYYY-MM-DD)"}
        }
      }
    },
    required: ["action"]
  }
};
```

## Tool Execution Handlers

### 1. Python Tool Executor

```python
import json
import asyncio
from typing import Any, Callable, Awaitable
from anthropic import Anthropic
from anthropic.types import ToolUseBlock, ToolResultBlock

# Type definitions
ToolInput = dict[str, Any]
ToolResult = dict[str, Any]
ToolHandler = Callable[[ToolInput], Awaitable[ToolResult]]


class ToolExecutor:
    """Manages tool definitions and executes tool calls."""
    
    def __init__(self, client: Anthropic):
        self.client = client
        self.handlers: dict[str, ToolHandler] = {}
        self.tools: list[dict] = []
    
    def register_tool(
        self,
        name: str,
        definition: dict,
        handler: ToolHandler
    ):
        """Register a tool with its handler."""
        self.handlers[name] = handler
        self.tools.append(definition)
    
    async def execute_tool(self, tool_call: ToolUseBlock) -> ToolResultBlock:
        """Execute a single tool call."""
        tool_name = tool_call.name
        tool_input = tool_call.input
        tool_use_id = tool_call.id
        
        try:
            if tool_name not in self.handlers:
                result = {
                    "success": False,
                    "error": f"Tool '{tool_name}' not found"
                }
            else:
                result = await self.handlers[tool_name](tool_input)
                result["success"] = True
                
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
        
        # Format as tool_result content block
        return ToolResultBlock(
            type="tool_result",
            tool_use_id=tool_use_id,
            content=json.dumps(result, ensure_ascii=False, indent=2)
        )
    
    async def execute_tools(
        self,
        tool_calls: list[ToolUseBlock]
    ) -> list[ToolResultBlock]:
        """Execute multiple tool calls (can be parallel)."""
        
        # Execute in parallel for efficiency
        tasks = [self.execute_tool(tc) for tc in tool_calls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        formatted_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                formatted_results.append(ToolResultBlock(
                    type="tool_result",
                    tool_use_id=tool_calls[i].id,
                    content=json.dumps({
                        "success": False,
                        "error": str(result)
                    })
                ))
            else:
                formatted_results.append(result)
        
        return formatted_results
```

### 2. TypeScript Tool Executor

```typescript
import Anthropic, { ToolUseBlock, ToolResultBlock } from '@anthropic-ai/sdk';

type ToolHandler = (input: Record<string, unknown>) => Promise<Record<string, unknown>>;

interface ToolExecutorConfig {
  client: Anthropic;
  tools: ToolDefinition[];
  handlers: Record<string, ToolHandler>;
}

class ToolExecutor {
  private client: Anthropic;
  private handlers: Map<string, ToolHandler>;
  private tools: ToolDefinition[];

  constructor(config: ToolExecutorConfig) {
    this.client = config.client;
    this.handlers = new Map(Object.entries(config.handlers));
    this.tools = config.tools;
  }

  async executeToolCall(toolCall: ToolUseBlock): Promise<ToolResultBlock> {
    const { name, input, id } = toolCall;
    
    try {
      const handler = this.handlers.get(name);
      
      if (!handler) {
        return this.createToolResult(id, {
          success: false,
          error: `Tool '${name}' not registered`
        });
      }
      
      const result = await handler(input);
      return this.createToolResult(id, {
        success: true,
        ...result
      });
      
    } catch (error) {
      return this.createToolResult(id, {
        success: false,
        error: error instanceof Error ? error.message : String(error),
        errorType: error instanceof Error ? error.constructor.name : 'UnknownError'
      });
    }
  }

  async executeToolCalls(
    toolCalls: ToolUseBlock[]
  ): Promise<ToolResultBlock[]> {
    // Execute in parallel for better performance
    const promises = toolCalls.map(tc => this.executeToolCall(tc));
    return Promise.all(promises);
  }

  private createToolResult(
    toolUseId: string,
    content: Record<string, unknown>
  ): ToolResultBlock {
    return {
      type: 'tool_result',
      tool_use_id: toolUseId,
      content: JSON.stringify(content, null, 2)
    } as ToolResultBlock;
  }
}
```

### 3. Real-World Tool Handlers

```python
# Product Search Handler
async def search_products_handler(input_data: dict) -> dict:
    """Handler cho product search tool."""
    
    query = input_data.get("query", "")
    category = input_data.get("category", "all")
    min_price = input_data.get("min_price")
    max_price = input_data.get("max_price")
    max_results = input_data.get("max_results", 10)
    sort_by = input_data.get("sort_by", "relevance")
    
    # Build search query (simulated)
    products = await product_database.search(
        query=query,
        category=category,
        price_range=(min_price, max_price),
        limit=max_results,
        sort=sort_by
    )
    
    return {
        "query": query,
        "total_found": len(products),
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "currency": "VND",
                "category": p.category,
                "in_stock": p.stock > 0,
                "rating": p.rating,
                "url": f"https://shop.example.com/product/{p.id}"
            }
            for p in products
        ]
    }


# Database Query Handler
async def query_database_handler(input_data: dict) -> dict:
    """Handler cho database query tool."""
    
    table = input_data.get("table")
    columns = input_data.get("columns", ["*"])
    where = input_data.get("where", {})
    order_by = input_data.get("order_by")
    limit = input_data.get("limit", 100)
    
    # Validate table name to prevent SQL injection
    allowed_tables = ["customers", "orders", "products", "inventory", "transactions"]
    if table not in allowed_tables:
        return {
            "success": False,
            "error": f"Table '{table}' not allowed. Allowed: {allowed_tables}"
        }
    
    # Build safe query (in real implementation, use parameterized queries)
    query = f"SELECT {', '.join(columns)} FROM {table}"
    
    if where:
        conditions = [f"{k} = '{v}'" for k, v in where.items()]
        query += " WHERE " + " AND ".join(conditions)
    
    if order_by:
        col = order_by.get("column", "id")
        direction = order_by.get("direction", "ASC").upper()
        query += f" ORDER BY {col} {direction}"
    
    query += f" LIMIT {limit}"
    
    # Execute query (simulated)
    results = await database.execute(query)
    
    return {
        "query_executed": query,
        "rows_returned": len(results),
        "data": results
    }


# Calendar Handler
async def manage_calendar_handler(input_data: dict) -> dict:
    """Handler cho calendar management tool."""
    
    action = input_data.get("action")
    
    handlers = {
        "check_availability": _check_availability,
        "create_event": _create_event,
        "update_event": _update_event,
        "delete_event": _delete_event,
        "list_events": _list_events,
    }
    
    handler = handlers.get(action)
    if not handler:
        return {"success": False, "error": f"Unknown action: {action}"}
    
    return await handler(input_data)


async def _check_availability(input_data: dict) -> dict:
    """Check time slot availability."""
    start_time = input_data.get("start_time")
    end_time = input_data.get("end_time")
    
    # Check calendar service
    slots = await calendar_service.get_availability(
        start=start_time,
        end=end_time
    )
    
    return {
        "available": slots["available"],
        "slots": slots["available_slots"]
    }


async def _create_event(input_data: dict) -> dict:
    """Create new calendar event."""
    event = await calendar_service.create_event({
        "title": input_data.get("title"),
        "description": input_data.get("description"),
        "start": input_data.get("start_time"),
        "end": input_data.get("end_time"),
        "attendees": input_data.get("attendee_emails", []),
        "timezone": input_data.get("timezone", "Asia/Ho_Chi_Minh"),
        "location": input_data.get("location"),
    })
    
    return {
        "success": True,
        "event_id": event.id,
        "event_link": event.html_link,
        "message": f"Event created: {event.title}"
    }


async def _list_events(input_data: dict) -> dict:
    """List events in date range."""
    date_range = input_data.get("date_range", {})
    events = await calendar_service.list_events(
        start=date_range.get("start"),
        end=date_range.get("end")
    )
    
    return {
        "count": len(events),
        "events": [
            {
                "id": e.id,
                "title": e.title,
                "start": e.start.isoformat(),
                "end": e.end.isoformat(),
                "attendees": len(e.attendees)
            }
            for e in events
        ]
    }
```

## Multi-Turn Tool Use

### 1. Conversation Loop Pattern

```python
import asyncio
from anthropic import Anthropic
from anthropic.types import Message, ContentBlock, ToolUseBlock

class ClaudeWithTools:
    """Claude client với multi-turn tool use support."""
    
    def __init__(self, api_key: str, tools: list[dict], handlers: dict):
        self.client = Anthropic(api_key=api_key)
        self.tools = tools
        self.handlers = handlers
        self.executor = ToolExecutor(self.client)
        
        # Register tools
        for name, (definition, handler) in tools.items():
            self.executor.register_tool(name, definition, handler)
    
    async def chat(
        self,
        messages: list[dict],
        model: str = "claude-3-5-sonnet-20241022",
        max_turns: int = 10,
    ) -> str:
        """Handle a conversation với tool use."""
        
        all_messages = messages.copy()
        
        for turn in range(max_turns):
            # Create message
            response = await self.client.messages.create(
                model=model,
                max_tokens=2048,
                tools=self.tools,
                messages=all_messages,
            )
            
            # Add assistant response to messages
            all_messages.append({
                "role": "assistant",
                "content": response.content
            })
            
            # Check if we have tool calls
            tool_calls = [
                block for block in response.content
                if block.type == "tool_use"
            ]
            
            if not tool_calls:
                # No more tool calls, return the last text response
                return self._extract_text(response.content)
            
            # Execute tools
            tool_results = await self.executor.execute_tools(tool_calls)
            
            # Add tool results to messages
            all_messages.append({
                "role": "user",
                "content": tool_results
            })
        
        # Max turns reached
        return "Đã đạt giới hạn số lượng tool calls. Vui lòng thử lại."
    
    def _extract_text(self, content: list[ContentBlock]) -> str:
        """Extract text from response content."""
        texts = []
        for block in content:
            if block.type == "text":
                texts.append(block.text)
        return "\n\n".join(texts)
```

### 2. TypeScript Multi-Turn Implementation

```typescript
import Anthropic, { MessageParam, ToolDefinition } from '@anthropic-ai/sdk';

interface ClaudeWithToolsConfig {
  apiKey: string;
  tools: ToolDefinition[];
  handlers: Record<string, ToolHandler>;
}

export class ClaudeWithTools {
  private client: Anthropic;
  private executor: ToolExecutor;
  private tools: ToolDefinition[];
  
  constructor(config: ClaudeWithToolsConfig) {
    this.client = new Anthropic({ apiKey: config.apiKey });
    this.executor = new ToolExecutor({
      client: this.client,
      tools: config.tools,
      handlers: config.handlers
    });
    this.tools = config.tools;
  }
  
  async chat(
    messages: MessageParam[],
    options: {
      model?: string;
      maxTurns?: number;
      systemPrompt?: string;
    } = {}
  ): Promise<string> {
    const {
      model = 'claude-3-5-sonnet-20241022',
      maxTurns = 10,
      systemPrompt
    } = options;
    
    const allMessages: MessageParam[] = [...messages];
    
    // Add system prompt if provided
    if (systemPrompt) {
      allMessages.unshift({
        role: 'user',
        content: `System: ${systemPrompt}`
      });
    }
    
    for (let turn = 0; turn < maxTurns; turn++) {
      const response = await this.client.messages.create({
        model,
        max_tokens: 2048,
        tools: this.tools,
        messages: allMessages,
      });
      
      // Add assistant message to history
      allMessages.push({
        role: 'assistant',
        content: response.content as any
      });
      
      // Extract tool calls
      const toolCalls = (response.content as any[])
        .filter(block => block.type === 'tool_use') as ToolUseBlock[];
      
      if (toolCalls.length === 0) {
        // No more tool calls, return text response
        return this.extractText(response.content);
      }
      
      // Execute tools and add results
      const toolResults = await this.executor.executeToolCalls(toolCalls);
      allMessages.push({
        role: 'user',
        content: toolResults as any
      });
    }
    
    return 'Đã đạt giới hạn số lượng tool calls. Vui lòng thử lại.';
  }
  
  private extractText(content: any[]): string {
    return content
      .filter(block => block.type === 'text')
      .map(block => block.text)
      .join('\n\n');
  }
}
```

## Streaming với Tools

### 1. Streaming Implementation

```python
import asyncio
from anthropic import Anthropic
from anthropic.lib streaming messages = Anthropic().messages.stream

class StreamingToolClient:
    """Claude client với streaming và tool use support."""
    
    def __init__(self, api_key: str, tools: list[dict], handlers: dict):
        self.client = Anthropic(api_key=api_key)
        self.handlers = handlers
        self.executor = ToolExecutor(self.client)
        
        for name, (definition, handler) in tools.items():
            self.executor.register_tool(name, definition, handler)
    
    async def stream_chat(
        self,
        messages: list[dict],
        model: str = "claude-3-5-sonnet-20241022",
        on_token: callable | None = None,
    ) -> str:
        """Stream response với tool use support."""
        
        full_text = ""
        tool_calls_in_progress: dict[str, dict] = {}
        pending_tools: list[ToolUseBlock] = []
        
        async with self.client.messages.stream(
            model=model,
            max_tokens=2048,
            tools=self.tools,
            messages=messages,
        ) as stream:
            async for event in stream:
                if event.type == "content_block_delta":
                    if event.delta.type == "text_delta":
                        full_text += event.delta.text
                        if on_token:
                            on_token(event.delta.text)
                    elif event.delta.type == "input_json_delta":
                        # Tool input being streamed
                        tool_id = event.delta.id
                        if tool_id not in tool_calls_in_progress:
                            tool_calls_in_progress[tool_id] = {"name": "", "input": ""}
                        tool_calls_in_progress[tool_id]["input"] += event.delta.partial_json
                        
                elif event.type == "content_block_start":
                    if event.content_block.type == "tool_use":
                        tool_calls_in_progress[event.index] = {
                            "name": event.content_block.name,
                            "input": "",
                            "id": event.content_block.id
                        }
                        
                elif event.type == "message_delta":
                    if event.usage:
                        print(f"Tokens used: {event.usage}")
        
        # Check for tool calls in final message
        message = await stream.get_final_message()
        tool_calls = [
            block for block in message.content
            if block.type == "tool_use"
        ]
        
        if tool_calls:
            # Execute tools
            tool_results = await self.executor.execute_tools(tool_calls)
            
            # Add results and continue conversation
            messages.append({
                "role": "assistant",
                "content": message.content
            })
            messages.append({
                "role": "user",
                "content": tool_results
            })
            
            # Recursively continue
            continuation = await self.stream_chat(
                messages,
                model=model,
                on_token=on_token
            )
            return continuation
        
        return full_text
```

### 2. Event-Based Streaming Handler

```typescript
interface StreamEvent {
  type: 'text' | 'tool_start' | 'tool_complete' | 'tool_error' | 'done';
  content?: string;
  toolName?: string;
  toolId?: string;
  result?: unknown;
  error?: string;
}

class StreamingToolHandler {
  constructor(
    private client: Anthropic,
    private executor: ToolExecutor
  ) {}
  
  async *streamWithTools(
    messages: MessageParam[],
    tools: ToolDefinition[]
  ): AsyncGenerator<StreamEvent> {
    const allMessages = [...messages];
    let currentText = '';
    
    const response = this.client.messages.stream({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 2048,
      tools,
      messages: allMessages
    });
    
    for await (const event of response) {
      if (event.type === 'content_block_delta') {
        if (event.delta.type === 'text_delta') {
          currentText += event.delta.text;
          yield { type: 'text', content: event.delta.text };
        }
      }
      
      if (event.type === 'content_block_start') {
        if (event.content_block.type === 'tool_use') {
          yield {
            type: 'tool_start',
            toolName: event.content_block.name,
            toolId: event.content_block.id
          };
        }
      }
    }
    
    // Get final message and execute tools
    const message = await response.finalMessage();
    const toolCalls = (message.content as any[])
      .filter(b => b.type === 'tool_use');
    
    if (toolCalls.length > 0) {
      const results = await this.executor.executeToolCalls(toolCalls);
      
      for (const result of results) {
        yield {
          type: 'tool_complete',
          toolId: result.tool_use_id,
          result: JSON.parse(result.content)
        };
      }
      
      // Continue conversation
      allMessages.push({ role: 'assistant', content: message.content as any });
      allMessages.push({ role: 'user', content: results as any });
      
      // Continue streaming
      yield* this.streamWithTools(allMessages, tools);
    } else {
      yield { type: 'done', content: currentText };
    }
  }
}
```

## Best Practices

### 1. Tool Design Best Practices

```python
# GOOD: Clear, specific descriptions
GOOD_TOOL = {
    "name": "calculate_shipping",
    "description": """Tính phí ship dựa trên địa chỉ giao hàng.
    
    Input:
    - weight: trọng lượng gram
    - destination: mã tỉnh/thành phố (2 ký tự)
    - service: dịch vụ vận chuyển (standard/express/overnight)
    
    Output: phí ship (VND) và estimated delivery time
    
    Chỉ sử dụng khi user hỏi về shipping costs hoặc delivery time.""",
    
    "input_schema": {
        "type": "object",
        "properties": {
            "weight": {"type": "number", "description": "Trọng lượng (gram)"},
            "destination": {"type": "string", "description": "Mã tỉnh TP (VD: HCM, HN)"},
            "service": {
                "type": "string",
                "enum": ["standard", "express", "overnight"],
                "default": "standard"
            }
        },
        "required": ["weight", "destination"]
    }
}

# BAD: Vague descriptions lead to misuse
BAD_TOOL = {
    "name": "calc",
    "description": "Calculate something",
    "input_schema": {
        "type": "object",
        "properties": {
            "data": {"type": "string"}
        }
    }
}
```

### 2. Error Handling Best Practices

```python
async def safe_tool_handler(tool_input: dict) -> dict:
    """Wrapper để handle errors gracefully."""
    
    try:
        # Validate input
        if not validate_input(tool_input):
            return {
                "success": False,
                "error": "Invalid input format",
                "details": get_validation_errors()
            }
        
        # Execute main logic
        result = await execute_tool(tool_input)
        
        return {
            "success": True,
            "data": result
        }
        
    except ValidationError as e:
        return {
            "success": False,
            "error": "Validation failed",
            "details": str(e)
        }
        
    except ExternalServiceError as e:
        # Retry logic could go here
        return {
            "success": False,
            "error": "External service unavailable",
            "retry_suggested": True,
            "original_error": str(e)
        }
        
    except PermissionError as e:
        return {
            "success": False,
            "error": "Permission denied",
            "details": "Insufficient permissions to perform this action"
        }
        
    except Exception as e:
        # Log for debugging
        log.error(f"Unexpected error in tool handler: {e}")
        
        return {
            "success": False,
            "error": "Internal error occurred",
            "error_id": generate_error_id()  # For tracking
        }
```

### 3. Performance Best Practices

```python
# Parallel tool execution
async def execute_parallel_tools(
    tool_calls: list[ToolUseBlock],
    executor: ToolExecutor
) -> list[ToolResultBlock]:
    """Execute multiple independent tools in parallel."""
    
    # Group tools by whether they're independent
    independent_tools = []
    dependent_tools = []
    
    for tc in tool_calls:
        if is_independent(tc.name):
            independent_tools.append(tc)
        else:
            dependent_tools.append(tc)
    
    # Execute independent tools in parallel
    if independent_tools:
        parallel_results = await asyncio.gather(
            *[execute_with_timeout(executor, tc) for tc in independent_tools],
            return_exceptions=True
        )
    
    # Execute dependent tools sequentially
    sequential_results = []
    for tc in dependent_tools:
        result = await executor.execute_tool(tc)
        sequential_results.append(result)
    
    return [...format_results(parallel_results), ...sequential_results]


async def execute_with_timeout(
    executor: ToolExecutor,
    tool_call: ToolUseBlock,
    timeout: float = 30.0
) -> ToolResultBlock | Exception:
    """Execute tool với timeout."""
    try:
        return await asyncio.wait_for(
            executor.execute_tool(tool_call),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        return TimeoutError(f"Tool {tool_call.name} timed out after {timeout}s")
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Tool not called | Claude không nhận ra cần tool | Improve description, add examples |
| Wrong tool parameters | Input schema unclear | Add detailed descriptions to each param |
| Tool called repeatedly | Claude doesn't know when to stop | Add "stop after success" instruction |
| Tool result not used | Result not informative | Return structured, clear results |
| Timeout errors | Long-running operations | Add timeout handling, async execution |

### Debugging Tool Calls

```python
import logging

class DebuggingToolExecutor(ToolExecutor):
    """Tool executor với debugging support."""
    
    def __init__(self, client: Anthropic):
        super().__init__(client)
        self.logger = logging.getLogger(__name__)
    
    async def execute_tool(self, tool_call: ToolUseBlock) -> ToolResultBlock:
        self.logger.info(f"Executing tool: {tool_call.name}")
        self.logger.debug(f"Tool input: {tool_call.input}")
        
        start_time = time.time()
        
        try:
            result = await super().execute_tool(tool_call)
            
            elapsed = time.time() - start_time
            self.logger.info(
                f"Tool {tool_call.name} completed in {elapsed:.2f}s"
            )
            
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            self.logger.error(
                f"Tool {tool_call.name} failed after {elapsed:.2f}s: {e}"
            )
            raise
```

## References

- [Anthropic Tool Use Documentation](https://docs.anthropic.com/claude/docs/tool-use)
- [Tool Use Examples](https://github.com/anthropics/anthropic-sdk-python/tree/main/examples/tools)
- [Best Practices for Tool Use](https://docs.anthropic.com/claude/docs/tool-use-best-practices)
