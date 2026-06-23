---
title: Chat Completion API
description: Hướng dẫn toàn diện về Chat Completions API, message roles, parameters, function calling và structured outputs
tags: [openai, chat, completion, api, typescript, python]
created: 2026-06-23
version: 1.0.0
framework: cursor-enterprise
---

# Chat Completion API

## Tổng quan

Chat Completions API là một trong những API được sử dụng rộng rãi nhất của OpenAI, cho phép developers tạo ra các ứng dụng conversational AI với khả năng xử lý ngôn ngữ tự nhiên. API này hỗ trợ multi-turn conversations với các message roles khác nhau, cho phép building chatbots, virtual assistants, và các ứng dụng AI-driven interactions khác.

So với legacy Completions API, Chat Completions API cung cấp cấu trúc linh hoạt hơn thông qua việc sử dụng messages thay vì single prompt. Điều này giúp developers dễ dàng quản lý conversation history, implement multi-turn interactions, và control model behavior thông qua system prompts.

OpenAI liên tục cải thiện Chat Completions API với các features mới như function calling, structured outputs, và vision capabilities. Việc nắm vững các features này là essential cho việc building production-ready AI applications. Trong tài liệu này, chúng ta sẽ cover tất cả các khía cạnh từ basic usage đến advanced patterns.

## Mục đích và Phạm vi

Tài liệu này được thiết kế để cung cấp kiến thức toàn diện về Chat Completions API cho các developers. Phạm vi bao gồm từ basic API structure và message format, cho đến các advanced features như function calling, structured outputs, và streaming responses. Chúng tôi sẽ cung cấp practical examples cho cả TypeScript và Python.

Đối tượng mục tiêu bao gồm developers muốn integrate AI capabilities vào applications, AI engineers building conversational interfaces, và technical architects designing AI-powered systems. Kiến thức cơ bản về REST APIs và asynchronous programming sẽ hữu ích nhưng không bắt buộc.

## Các Khái niệm Chính

### Message Roles và Conversation Structure

Chat Completions API sử dụng message-based structure với ba role chính: system, user, và assistant. Mỗi role có chức năng riêng biệt và ảnh hưởng đến cách model interpret và respond to messages.

**System role** định nghĩa behavior và personality của assistant. System messages set up the context và instructions cho how the model should behave throughout the conversation. Effective system prompts có thể dramatically improve model performance và ensure consistent responses. System messages được process đầu tiên và có ảnh hưởng lớn nhất đến model behavior.

**User role** represent messages từ end-user. Đây là input chính mà model cần respond to. User messages có thể contain questions, requests, statements, hoặc any form of natural language input. Model được trained để understand và respond appropriately to diverse user inputs.

**Assistant role** là output từ model. Trong API calls, assistant messages có thể được include để provide examples of desired behavior hoặc maintain conversation continuity. Khi continuing a conversation, assistant messages from previous turns được passed back để maintain context.

### Model Parameters

Chat Completions API cung cấp nhiều parameters để control model behavior và output characteristics. Understanding các parameters này là critical cho achieving desired results.

**model** parameter xác định which model sẽ be used cho completion. OpenAI cung cấp nhiều models với different capabilities và pricing: gpt-4o (latest flagship), gpt-4o-mini (cost-effective), gpt-4-turbo (fast, capable), gpt-3.5-turbo (budget option). Model selection nên be based on use case requirements và budget constraints.

**temperature** controls randomness của output. Giá trị từ 0 đến 2, với 0 là deterministic (almost always pick highest probability token) và 2 là very random. Lower temperature (0-0.3) phù hợp cho tasks cần consistency và factual accuracy như summarization, translation. Higher temperature (0.7-1.0) phù hợp cho creative tasks như brainstorming, storytelling. Default là 1.0.

**top_p** là alternative sampling method đến temperature. Nó xác định cumulative probability threshold cho token selection. top_p=0.1 có nghĩa là model chỉ consider top 10% probability mass. Khi sử dụng top_p, thường nên set temperature = 1.0 hoặc experiment với cả hai. Using both temperature và top_p không recommended.

**max_tokens** giới hạn maximum length của output. Đây là hard limit cho số lượng tokens trong response. Setting quá thấp có thể result in truncated responses, trong khi setting quá cao có thể waste tokens và tăng latency. Best practice là estimate dựa trên expected response length và add some buffer.

**stop** sequences là strings mà khi xuất hiện sẽ stop generation. Useful cho structured outputs hoặc when you want to limit response to specific patterns. Có thể specify up to 4 stop sequences.

### Response Format

Response từ Chat Completions API chứa nhiều thông tin hữu ích ngoài content. Understanding response structure giúp bạn extract và use information hiệu quả.

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-4o-2024-08-06",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Response content here"
    },
    "finish_reason": "stop",
    "logprobs": null
  }],
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 100,
    "total_tokens": 150
  },
  "system_fingerprint": "fp_12345"
}
```

**id** là unique identifier cho request, useful cho debugging và tracking. **created** timestamp allows ordering và chronological analysis. **choices** array chứa actual responses, thường chỉ có một choice trừ khi bạn request multiple outputs với n>1.

**finish_reason** indicates why generation stopped: "stop" means normal completion, "length" means max_tokens hit, "content_filter" means content was filtered, "function_call" means model triggered function calling. **usage** object cung cấp token consumption details cho cost tracking và optimization.

## Best Practices cho Production

### System Prompt Design

```typescript
// prompts/systemPrompts.ts - System prompt templates và patterns

interface SystemPromptConfig {
  personality: {
    tone: 'professional' | 'friendly' | 'technical' | 'casual';
    verbosity: 'concise' | 'moderate' | 'detailed';
    creativity: 'reserved' | 'balanced' | 'creative';
  };
  expertise: {
    domain: string;
    level: 'beginner' | 'intermediate' | 'expert';
    includeExamples: boolean;
  };
  constraints: {
    responseFormat: 'plain' | 'structured' | 'markdown';
    maxLength: 'short' | 'medium' | 'long';
    disallowedTopics?: string[];
  };
}

// Professional assistant with technical expertise
const professionalTechnicalPrompt = `Bạn là một Technical Solutions Architect với hơn 15 năm kinh nghiệm trong ngành công nghiệp phần mềm.

## Chuyên môn của bạn:
- System architecture và design patterns
- Cloud computing (AWS, Azure, GCP)
- DevOps và CI/CD pipelines
- Database design và optimization
- API design và microservices

## Nguyên tắc làm việc:
1. Phân tích vấn đề một cách có hệ thống trước khi đề xuất giải pháp
2. Luôn consider trade-offs giữa complexity, performance, và maintainability
3. Ưu tiên practical, implementable solutions over theoretical最优解
4. Provide concrete code examples khi cần thiết

## Giới hạn:
- Không đề xuất giải pháp không an toàn hoặc có security vulnerabilities
- Không đưa ra lời khuyên vi phạm ethical guidelines
- Nếu không chắc chắn, hãy nói rõ và suggest cách verify

## Response Format:
- Use markdown để format code blocks và technical terms
- Include pros/cons khi compare solutions
- Suggest next steps hoặc verification methods khi appropriate`;

// Customer support chatbot prompt
const customerSupportPrompt = `Bạn là Maya, một customer support agent thân thiện cho TechCorp, một công ty SaaS về project management software.

## Thông tin về TechCorp:
- Founded: 2018
- Products: TaskFlow Pro, TeamSync, AnalyticsHub
- Support hours: 24/7
- Average response time: < 2 minutes

## Phong cách giao tiếp:
- Thân thiện, empathetic, và professional
- Sử dụng ngôn ngữ simple, tránh jargon không cần thiết
- Xưng hô "bạn" với khách hàng
- Show empathy: "Tôi hiểu điều đó có thể gây frustrate"
- Offer solutions proactively

## Quy trình xử lý:
1. Greet customer warmly và introduce yourself
2. Ask clarifying questions nếu cần
3. Provide clear solution steps
4. Confirm if issue is resolved
5. Offer additional help

## Boundaries:
- Không shared confidential company information
- Không make promises về features hoặc timelines
- Escalate billing issues to billing@techcorp.com
- Escalate technical bugs to support tier 2

## Response Style:
- Keep responses under 150 words cho simple queries
- Use numbered lists cho multi-step instructions
- Always end with: "Còn gì khác tôi có thể giúp bạn không?"`;

// Code assistant prompt
const codeAssistantPrompt = `Bạn là một Senior Software Engineer với deep expertise trong multiple programming languages và frameworks.

## Expertise Areas:
- Languages: TypeScript, Python, Java, Go, Rust, C++
- Frontend: React, Vue, Angular, Next.js, Nuxt.js
- Backend: Node.js, Django, Spring Boot, FastAPI
- Databases: PostgreSQL, MongoDB, Redis, Elasticsearch
- Cloud: Docker, Kubernetes, Terraform, AWS/GCP/Azure

## Code Standards:
- Write clean, maintainable code với meaningful variable names
- Include comments cho complex logic
- Follow best practices và design patterns
- Consider error handling và edge cases
- Optimize for readability over cleverness

## Output Format:
\`\`\`language
// Code here
\`\`\`

## Response Structure:
1. Brief explanation của approach
2. Code solution
3. Complexity analysis (time/space)
4. Potential improvements hoặc alternatives
5. Testing suggestions`;

// Multi-language translator prompt
const translatorPrompt = `Bạn là một professional translator chuyên nghiệp với native-level fluency in multiple languages.

## Supported Languages:
- Vietnamese (primary)
- English
- Mandarin Chinese
- Japanese
- Korean
- French
- German

## Translation Principles:
1. Preserve meaning, tone, và intent của original text
2. Adapt cultural references appropriately
3. Maintain formatting và structure
4. Preserve technical terms và proper nouns
5. Use appropriate register cho target audience

## Quality Checklist:
- Check for grammatical accuracy
- Verify terminology consistency
- Ensure natural flow trong target language
- Verify number/date formatting
- Review for ambiguous translations

## Response Format:
[Source Language → Target Language]

**Original:** (quote original text)
**Translation:** (provide translation)

**Notes:** (any translation notes, alternative interpretations, hoặc cultural context)`;

export function buildSystemPrompt(config: SystemPromptConfig): string {
  const toneMap = {
    professional: 'formal, respectful, and precise',
    friendly: 'warm, approachable, and conversational',
    technical: 'precise, detailed, and analytical',
    casual: 'relaxed, informal, and easy-going',
  };

  const verbosityMap = {
    concise: '2-3 sentences maximum',
    moderate: '1-2 paragraphs',
    detailed: 'thorough explanations with examples',
  };

  let prompt = `# Role: ${config.expertise.domain} Expert\n\n`;
  prompt += `## Communication Style\n`;
  prompt += `Tone: ${toneMap[config.personality.tone]}\n`;
  prompt += `Verbosity: ${verbosityMap[config.personality.verbosity]}\n`;
  prompt += `Creativity: ${config.personality.creativity === 'creative' ? 'Feel free to suggest innovative approaches' : 'Focus on established best practices'}\n\n`;
  prompt += `## Expertise Level\n`;
  prompt += `Assume ${config.expertise.level} audience\n`;
  prompt += `Use ${config.expertise.includeExamples ? 'concrete examples' : 'conceptual explanations'}\n\n`;
  prompt += `## Response Format\n`;
  prompt += `Format: ${config.constraints.responseFormat}\n`;
  prompt += `Length: ${config.constraints.maxLength}\n`;
  
  if (config.constraints.disallowedTopics?.length) {
    prompt += `\n## Off-Limits\n`;
    prompt += `Do not discuss: ${config.constraints.disallowedTopics.join(', ')}\n`;
  }

  return prompt;
}

export { professionalTechnicalPrompt, customerSupportPrompt, codeAssistantPrompt, translatorPrompt };
```

```python
# prompts/system_prompts.py - System prompt templates và patterns
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class Tone(Enum):
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    TECHNICAL = "technical"
    CASUAL = "casual"

class Verbosity(Enum):
    CONCISE = "concise"
    MODERATE = "moderate"
    DETAILED = "detailed"

class ExpertiseLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"

class ResponseFormat(Enum):
    PLAIN = "plain"
    STRUCTURED = "structured"
    MARKDOWN = "markdown"

@dataclass
class SystemPromptConfig:
    tone: Tone = Tone.PROFESSIONAL
    verbosity: Verbosity = Verbosity.MODERATE
    creativity: str = "balanced"
    expertise_domain: str = "general"
    expertise_level: ExpertiseLevel = ExpertiseLevel.INTERMEDIATE
    include_examples: bool = True
    response_format: ResponseFormat = ResponseFormat.MARKDOWN
    max_length: str = "medium"
    disallowed_topics: Optional[List[str]] = None

PROFESSIONAL_TECHNICAL_PROMPT = """Bạn là một Technical Solutions Architect với hơn 15 năm kinh nghiệm trong ngành công nghiệp phần mềm.

## Chuyên môn của bạn:
- System architecture và design patterns
- Cloud computing (AWS, Azure, GCP)
- DevOps và CI/CD pipelines
- Database design và optimization
- API design và microservices

## Nguyên tắc làm việc:
1. Phân tích vấn đề một cách có hệ thống trước khi đề xuất giải pháp
2. Luôn consider trade-offs giữa complexity, performance, và maintainability
3. Ưu tiên practical, implementable solutions over theoretical最优解
4. Provide concrete code examples khi cần thiết

## Giới hạn:
- Không đề xuất giải pháp không an toàn hoặc có security vulnerabilities
- Không đưa ra lời khuyên vi phạm ethical guidelines
- Nếu không chắc chắn, hãy nói rõ và suggest cách verify

## Response Format:
- Use markdown để format code blocks và technical terms
- Include pros/cons khi compare solutions
- Suggest next steps hoặc verification methods khi appropriate"""

CUSTOMER_SUPPORT_PROMPT = """Bạn là Maya, một customer support agent thân thiện cho TechCorp, một công ty SaaS về project management software.

## Thông tin về TechCorp:
- Founded: 2018
- Products: TaskFlow Pro, TeamSync, AnalyticsHub
- Support hours: 24/7
- Average response time: < 2 minutes

## Phong cách giao tiếp:
- Thân thiện, empathetic, và professional
- Sử dụng ngôn ngữ simple, tránh jargon không cần thiết
- Xưng hô "bạn" với khách hàng
- Show empathy: "Tôi hiểu điều đó có thể gây frustrate"
- Offer solutions proactively

## Quy trình xử lý:
1. Greet customer warmly và introduce yourself
2. Ask clarifying questions nếu cần
3. Provide clear solution steps
4. Confirm if issue is resolved
5. Offer additional help

## Boundaries:
- Không shared confidential company information
- Không make promises về features hoặc timelines
- Escalate billing issues to billing@techcorp.com
- Escalate technical bugs to support tier 2

## Response Style:
- Keep responses under 150 words cho simple queries
- Use numbered lists cho multi-step instructions
- Always end with: "Còn gì khác tôi có thể giúp bạn không?\""""

CODE_ASSISTANT_PROMPT = """Bạn là một Senior Software Engineer với deep expertise trong multiple programming languages và frameworks.

## Expertise Areas:
- Languages: TypeScript, Python, Java, Go, Rust, C++
- Frontend: React, Vue, Angular, Next.js, Nuxt.js
- Backend: Node.js, Django, Spring Boot, FastAPI
- Databases: PostgreSQL, MongoDB, Redis, Elasticsearch
- Cloud: Docker, Kubernetes, Terraform, AWS/GCP/Azure

## Code Standards:
- Write clean, maintainable code với meaningful variable names
- Include comments cho complex logic
- Follow best practices và design patterns
- Consider error handling và edge cases
- Optimize for readability over cleverness

## Output Format:
```language
# Code here
```

## Response Structure:
1. Brief explanation của approach
2. Code solution
3. Complexity analysis (time/space)
4. Potential improvements hoặc alternatives
5. Testing suggestions"""

def build_system_prompt(config: SystemPromptConfig) -> str:
    """Build system prompt from configuration."""
    tone_map = {
        Tone.PROFESSIONAL: "formal, respectful, and precise",
        Tone.FRIENDLY: "warm, approachable, and conversational",
        Tone.TECHNICAL: "precise, detailed, and analytical",
        Tone.CASUAL: "relaxed, informal, and easy-going",
    }
    
    verbosity_map = {
        Verbosity.CONCISE: "2-3 sentences maximum",
        Verbosity.MODERATE: "1-2 paragraphs",
        Verbosity.DETAILED: "thorough explanations with examples",
    }
    
    prompt = f"# Role: {config.expertise_domain} Expert\n\n"
    prompt += f"## Communication Style\n"
    prompt += f"Tone: {tone_map[config.tone]}\n"
    prompt += f"Verbosity: {verbosity_map[config.verbosity]}\n"
    prompt += f"Creativity: {'Feel free to suggest innovative approaches' if config.creativity == 'creative' else 'Focus on established best practices'}\n\n"
    prompt += f"## Expertise Level\n"
    prompt += f"Assume {config.expertise_level.value} audience\n"
    prompt += f"Use {'concrete examples' if config.include_examples else 'conceptual explanations'}\n\n"
    prompt += f"## Response Format\n"
    prompt += f"Format: {config.response_format.value}\n"
    prompt += f"Length: {config.max_length}\n"
    
    if config.disallowed_topics:
        prompt += f"\n## Off-Limits\n"
        prompt += f"Do not discuss: {', '.join(config.disallowed_topics)}\n"
    
    return prompt
```

## Function Calling

### Defining Functions

```typescript
// functions/definitions.ts - Function calling patterns

interface FunctionDefinition {
  name: string;
  description: string;
  parameters: {
    type: 'object';
    properties: Record<string, any>;
    required: string[];
  };
}

// Weather function
const weatherFunction: FunctionDefinition = {
  name: 'get_weather',
  description: 'Get current weather information for a specific location',
  parameters: {
    type: 'object',
    properties: {
      location: {
        type: 'string',
        description: 'City name or location (e.g., "Hanoi", "Ho Chi Minh City")',
      },
      units: {
        type: 'string',
        enum: ['celsius', 'fahrenheit'],
        description: 'Temperature unit preference',
        default: 'celsius',
      },
    },
    required: ['location'],
  },
};

// Calendar function
const calendarFunction: FunctionDefinition = {
  name: 'create_calendar_event',
  description: 'Create a new event in the user calendar',
  parameters: {
    type: 'object',
    properties: {
      title: {
        type: 'string',
        description: 'Event title or subject',
      },
      start_time: {
        type: 'string',
        format: 'date-time',
        description: 'Event start time in ISO 8601 format',
      },
      end_time: {
        type: 'string',
        format: 'date-time',
        description: 'Event end time in ISO 8601 format',
      },
      description: {
        type: 'string',
        description: 'Event description or notes',
      },
      location: {
        type: 'string',
        description: 'Physical location or meeting link',
      },
      attendees: {
        type: 'array',
        items: { type: 'string' },
        description: 'Email addresses of attendees',
      },
      reminders: {
        type: 'object',
        properties: {
          use_default: { type: 'boolean' },
          overrides: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                method: { type: 'string', enum: ['email', 'popup'] },
                minutes: { type: 'integer' },
              },
            },
          },
        },
      },
    },
    required: ['title', 'start_time', 'end_time'],
  },
};

// Database query function
const databaseQueryFunction: FunctionDefinition = {
  name: 'query_database',
  description: 'Execute a SQL query against the analytics database',
  parameters: {
    type: 'object',
    properties: {
      query: {
        type: 'string',
        description: 'SQL query to execute (SELECT statements only)',
      },
      limit: {
        type: 'integer',
        description: 'Maximum number of rows to return',
        default: 100,
      },
      timeout_seconds: {
        type: 'integer',
        description: 'Query timeout in seconds',
        default: 30,
      },
    },
    required: ['query'],
  },
};

// Email function
const emailFunction: FunctionDefinition = {
  name: 'send_email',
  description: 'Send an email to specified recipients',
  parameters: {
    type: 'object',
    properties: {
      to: {
        type: 'array',
        items: { type: 'string' },
        description: 'Recipient email addresses',
      },
      cc: {
        type: 'array',
        items: { type: 'string' },
        description: 'CC recipient email addresses',
      },
      subject: {
        type: 'string',
        description: 'Email subject line',
      },
      body: {
        type: 'string',
        description: 'Email body content (plain text)',
      },
      is_html: {
        type: 'boolean',
        description: 'Whether body contains HTML content',
        default: false,
      },
      attachments: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            filename: { type: 'string' },
            content_type: { type: 'string' },
            data: { type: 'string' },
          },
        },
        description: 'File attachments',
      },
    },
    required: ['to', 'subject', 'body'],
  },
};

// Search function
const searchFunction: FunctionDefinition = {
  name: 'search_knowledge_base',
  description: 'Search the internal knowledge base for relevant documents',
  parameters: {
    type: 'object',
    properties: {
      query: {
        type: 'string',
        description: 'Search query string',
      },
      filters: {
        type: 'object',
        properties: {
          category: {
            type: 'array',
            items: { type: 'string' },
            description: 'Filter by document categories',
          },
          date_from: { type: 'string', format: 'date' },
          date_to: { type: 'string', format: 'date' },
          author: { type: 'string' },
          tags: { type: 'array', items: { type: 'string' } },
        },
      },
      limit: {
        type: 'integer',
        description: 'Maximum number of results',
        default: 10,
      },
      include_summary: {
        type: 'boolean',
        description: 'Include document summaries in results',
        default: true,
      },
    },
    required: ['query'],
  },
};

// All available functions
export const availableFunctions = {
  get_weather: weatherFunction,
  create_calendar_event: calendarFunction,
  query_database: databaseQueryFunction,
  send_email: emailFunction,
  search_knowledge_base: searchFunction,
};

export type AvailableFunctionName = keyof typeof availableFunctions;
```

```python
# functions/definitions.py - Function calling patterns
from typing import List, Optional, TypedDict
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class FunctionProperty:
    type: str
    description: str
    enum: Optional[List[str]] = None
    default: Optional[Any] = None
    format: Optional[str] = None
    items: Optional[Any] = None

@dataclass
class FunctionDefinition:
    name: str
    description: str
    parameters: dict

# Weather function
WEATHER_FUNCTION = FunctionDefinition(
    name="get_weather",
    description="Get current weather information for a specific location",
    parameters={
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City name or location (e.g., 'Hanoi', 'Ho Chi Minh City')",
            },
            "units": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit preference",
            },
        },
        "required": ["location"],
    },
)

# Calendar function
CALENDAR_FUNCTION = FunctionDefinition(
    name="create_calendar_event",
    description="Create a new event in the user calendar",
    parameters={
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Event title or subject"},
            "start_time": {"type": "string", "format": "date-time", "description": "Event start time in ISO 8601 format"},
            "end_time": {"type": "string", "format": "date-time", "description": "Event end time in ISO 8601 format"},
            "description": {"type": "string", "description": "Event description or notes"},
            "location": {"type": "string", "description": "Physical location or meeting link"},
            "attendees": {"type": "array", "items": {"type": "string"}, "description": "Email addresses of attendees"},
            "reminders": {
                "type": "object",
                "properties": {
                    "use_default": {"type": "boolean"},
                    "overrides": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "method": {"type": "string", "enum": ["email", "popup"]},
                                "minutes": {"type": "integer"},
                            },
                        },
                    },
                },
            },
        },
        "required": ["title", "start_time", "end_time"],
    },
)

# Database query function
DATABASE_QUERY_FUNCTION = FunctionDefinition(
    name="query_database",
    description="Execute a SQL query against the analytics database",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "SQL query to execute (SELECT statements only)"},
            "limit": {"type": "integer", "description": "Maximum number of rows to return", "default": 100},
            "timeout_seconds": {"type": "integer", "description": "Query timeout in seconds", "default": 30},
        },
        "required": ["query"],
    },
)

# Email function
EMAIL_FUNCTION = FunctionDefinition(
    name="send_email",
    description="Send an email to specified recipients",
    parameters={
        "type": "object",
        "properties": {
            "to": {"type": "array", "items": {"type": "string"}, "description": "Recipient email addresses"},
            "cc": {"type": "array", "items": {"type": "string"}, "description": "CC recipient email addresses"},
            "subject": {"type": "string", "description": "Email subject line"},
            "body": {"type": "string", "description": "Email body content (plain text)"},
            "is_html": {"type": "boolean", "description": "Whether body contains HTML content"},
            "attachments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string"},
                        "content_type": {"type": "string"},
                        "data": {"type": "string"},
                    },
                },
                "description": "File attachments",
            },
        },
        "required": ["to", "subject", "body"],
    },
)

AVAILABLE_FUNCTIONS = {
    "get_weather": WEATHER_FUNCTION,
    "create_calendar_event": CALENDAR_FUNCTION,
    "query_database": DATABASE_QUERY_FUNCTION,
    "send_email": EMAIL_FUNCTION,
}
```

### Implementing Function Handlers

```typescript
// functions/handlers.ts - Function implementation handlers
import { AvailableFunctionName } from './definitions';

interface FunctionCall {
  name: AvailableFunctionName;
  arguments: Record<string, any>;
}

interface FunctionResult {
  success: boolean;
  result?: any;
  error?: string;
}

// Weather service implementation
async function getWeather(location: string, units?: string): Promise<FunctionResult> {
  try {
    // Simulated weather API call
    const weatherData = {
      location,
      temperature: units === 'fahrenheit' ? 72 : 22,
      condition: 'partly_cloudy',
      humidity: 65,
      wind_speed: units === 'fahrenheit' ? '12 mph' : '19 km/h',
      forecast: [
        { day: 'Today', high: 25, low: 18, condition: 'Sunny' },
        { day: 'Tomorrow', high: 23, low: 17, condition: 'Cloudy' },
        { day: 'Day After', high: 26, low: 19, condition: 'Partly Cloudy' },
      ],
    };
    
    return { success: true, result: weatherData };
  } catch (error) {
    return { success: false, error: `Failed to get weather: ${error.message}` };
  }
}

// Calendar service implementation
async function createCalendarEvent(params: {
  title: string;
  start_time: string;
  end_time: string;
  description?: string;
  location?: string;
  attendees?: string[];
}): Promise<FunctionResult> {
  try {
    // Validate inputs
    if (!params.title || !params.start_time || !params.end_time) {
      return { success: false, error: 'Missing required fields' };
    }
    
    const eventId = `evt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    return {
      success: true,
      result: {
        event_id: eventId,
        title: params.title,
        start_time: params.start_time,
        end_time: params.end_time,
        location: params.location,
        attendees: params.attendees || [],
        status: 'confirmed',
        meeting_link: `https://meet.techcorp.com/${eventId}`,
      },
    };
  } catch (error) {
    return { success: false, error: `Failed to create event: ${error.message}` };
  }
}

// Database query implementation
async function queryDatabase(query: string, limit?: number): Promise<FunctionResult> {
  try {
    // Validate query is SELECT only
    const normalizedQuery = query.trim().toUpperCase();
    if (!normalizedQuery.startsWith('SELECT')) {
      return { success: false, error: 'Only SELECT queries are allowed' };
    }
    
    // Add LIMIT if not specified
    let finalQuery = query;
    if (!query.toLowerCase().includes('limit')) {
      finalQuery = `${query} LIMIT ${limit || 100}`;
    }
    
    // Simulated database query
    return {
      success: true,
      result: {
        rows: [
          { id: 1, name: 'Sample Data', value: 100 },
          { id: 2, name: 'Another Entry', value: 200 },
        ],
        row_count: 2,
        query_time_ms: 45,
        execution_time: '45ms',
      },
    };
  } catch (error) {
    return { success: false, error: `Query failed: ${error.message}` };
  }
}

// Email service implementation
async function sendEmail(params: {
  to: string[];
  cc?: string[];
  subject: string;
  body: string;
  is_html?: boolean;
}): Promise<FunctionResult> {
  try {
    // Validate inputs
    if (!params.to.length) {
      return { success: false, error: 'At least one recipient is required' };
    }
    
    if (!params.subject || !params.body) {
      return { success: false, error: 'Subject and body are required' };
    }
    
    // Simulated email send
    return {
      success: true,
      result: {
        message_id: `msg_${Date.now()}@techcorp.com`,
        to: params.to,
        cc: params.cc || [],
        subject: params.subject,
        sent_at: new Date().toISOString(),
        status: 'delivered',
      },
    };
  } catch (error) {
    return { success: false, error: `Failed to send email: ${error.message}` };
  }
}

// Main handler dispatcher
const handlers: Record<AvailableFunctionName, Function> = {
  get_weather: getWeather,
  create_calendar_event: createCalendarEvent,
  query_database: queryDatabase,
  send_email: sendEmail,
};

export async function handleFunctionCall(functionCall: FunctionCall): Promise<FunctionResult> {
  const { name, arguments: args } = functionCall;
  
  const handler = handlers[name];
  if (!handler) {
    return { success: false, error: `Unknown function: ${name}` };
  }
  
  try {
    return await handler(...Object.values(args));
  } catch (error) {
    return { success: false, error: `Handler error: ${error.message}` };
  }
}

export { getWeather, createCalendarEvent, queryDatabase, sendEmail };
```

### Function Calling Flow

```typescript
// services/functionCallingService.ts - Complete function calling workflow
import OpenAI from 'openai';
import { availableFunctions, AvailableFunctionName } from '../functions/definitions';
import { handleFunctionCall, FunctionResult } from '../functions/handlers';

interface FunctionCallMessage {
  role: 'assistant';
  content: string;
  function_call: {
    name: AvailableFunctionName;
    arguments: string;
  };
}

interface ConversationTurn {
  messages: Array<{ role: string; content: string }>;
  functionCalls: Array<{
    name: string;
    args: any;
    result: FunctionResult;
  }>;
}

export class FunctionCallingService {
  private client: OpenAI;
  private maxIterations: number;
  
  constructor(client: OpenAI, maxIterations: number = 10) {
    this.client = client;
    this.maxIterations = maxIterations;
  }
  
  async chatWithFunctions(
    messages: Array<{ role: string; content: string }>,
    tools?: AvailableFunctionName[]
  ): Promise<ConversationTurn> {
    const conversation: ConversationTurn = {
      messages: [...messages],
      functionCalls: [],
    };
    
    const activeTools = tools || (Object.keys(availableFunctions) as AvailableFunctionName[]);
    
    for (let iteration = 0; iteration < this.maxIterations; iteration++) {
      // Make API call with tools
      const response = await this.client.chat.completions.create({
        model: 'gpt-4o',
        messages: conversation.messages,
        tools: activeTools.map(name => ({
          type: 'function' as const,
          function: availableFunctions[name],
        })),
        tool_choice: 'auto',
      });
      
      const assistantMessage = response.choices[0].message;
      
      // Add assistant message to conversation
      conversation.messages.push({
        role: 'assistant',
        content: assistantMessage.content || '',
      });
      
      // Check for tool calls
      if (!assistantMessage.tool_calls || assistantMessage.tool_calls.length === 0) {
        // No more function calls, we're done
        break;
      }
      
      // Process each tool call
      for (const toolCall of assistantMessage.tool_calls) {
        const functionName = toolCall.function.name as AvailableFunctionName;
        const functionArgs = JSON.parse(toolCall.function.arguments);
        
        // Add tool call message
        conversation.messages.push({
          role: 'tool',
          tool_call_id: toolCall.id,
          content: '', // Will be filled after execution
        });
        
        // Execute function
        const result = await handleFunctionCall({
          name: functionName,
          arguments: functionArgs,
        });
        
        // Record function call
        conversation.functionCalls.push({
          name: functionName,
          args: functionArgs,
          result,
        });
        
        // Add tool result to messages
        conversation.messages.push({
          role: 'tool',
          content: JSON.stringify(result),
        });
      }
    }
    
    return conversation;
  }
  
  async chatWithSingleFunction<T>(
    messages: Array<{ role: string; content: string }>,
    functionName: AvailableFunctionName,
    parameters?: Record<string, any>
  ): Promise<T> {
    const response = await this.client.chat.completions.create({
      model: 'gpt-4o',
      messages: messages,
      tools: [{
        type: 'function',
        function: {
          ...availableFunctions[functionName],
          parameters: parameters || availableFunctions[functionName].parameters,
        },
      }],
      tool_choice: {
        type: 'function',
        function: { name: functionName },
      },
    });
    
    const assistantMessage = response.choices[0].message;
    
    if (!assistantMessage.tool_calls || assistantMessage.tool_calls.length === 0) {
      throw new Error('No function call returned');
    }
    
    const toolCall = assistantMessage.tool_calls[0];
    const args = JSON.parse(toolCall.function.arguments);
    
    const result = await handleFunctionCall({
      name: functionName,
      arguments: args,
    });
    
    if (!result.success) {
      throw new Error(result.error);
    }
    
    return result.result as T;
  }
}
```

## Structured Outputs

### JSON Schema Definitions

```typescript
// schemas/outputs.ts - Structured output schemas

interface StructuredOutputSchema {
  type: 'object';
  properties: Record<string, any>;
  required?: string[];
  additionalProperties?: boolean;
}

// Sentiment analysis output
const sentimentAnalysisSchema: StructuredOutputSchema = {
  type: 'object',
  properties: {
    sentiment: {
      type: 'string',
      enum: ['positive', 'negative', 'neutral', 'mixed'],
      description: 'Overall sentiment of the text',
    },
    confidence: {
      type: 'number',
      minimum: 0,
      maximum: 1,
      description: 'Confidence score for the classification',
    },
    aspects: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          aspect: { type: 'string', description: 'Aspect or feature mentioned' },
          sentiment: { type: 'string', enum: ['positive', 'negative', 'neutral'] },
          evidence: { type: 'string', description: 'Text supporting this aspect sentiment' },
        },
        required: ['aspect', 'sentiment', 'evidence'],
      },
      description: 'Sentiment for specific aspects of the text',
    },
    summary: {
      type: 'string',
      description: 'Brief summary of the overall sentiment',
    },
  },
  required: ['sentiment', 'confidence', 'summary'],
  additionalProperties: false,
};

// Product review extraction
const productReviewSchema: StructuredOutputSchema = {
  type: 'object',
  properties: {
    product_name: { type: 'string', description: 'Name of the product' },
    overall_rating: {
      type: 'number',
      minimum: 1,
      maximum: 5,
      description: 'Overall rating out of 5',
    },
    pros: {
      type: 'array',
      items: { type: 'string' },
      description: 'List of positive aspects mentioned',
    },
    cons: {
      type: 'array',
      items: { type: 'string' },
      description: 'List of negative aspects mentioned',
    },
    recommended: {
      type: 'boolean',
      description: 'Whether the reviewer recommends the product',
    },
    verified_purchase: { type: 'boolean', description: 'Whether this is a verified purchase' },
    helpful_count: { type: 'integer', description: 'Number of people who found this helpful' },
    categories: {
      type: 'array',
      items: { type: 'string' },
      description: 'Product categories or tags',
    },
  },
  required: ['product_name', 'overall_rating', 'recommended'],
  additionalProperties: false,
};

// Meeting notes extraction
const meetingNotesSchema: StructuredOutputSchema = {
  type: 'object',
  properties: {
    meeting_title: { type: 'string', description: 'Title or subject of the meeting' },
    date: { type: 'string', format: 'date', description: 'Date of the meeting' },
    duration_minutes: { type: 'integer', description: 'Meeting duration in minutes' },
    attendees: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          name: { type: 'string' },
          role: { type: 'string' },
          organization: { type: 'string' },
        },
        required: ['name'],
      },
    },
    agenda: {
      type: 'array',
      items: { type: 'string' },
      description: 'Main topics discussed',
    },
    decisions: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          decision: { type: 'string', description: 'The decision made' },
          rationale: { type: 'string', description: 'Reason for the decision' },
          owner: { type: 'string', description: 'Person responsible for implementation' },
          deadline: { type: 'string', format: 'date', description: 'Deadline for action' },
        },
        required: ['decision'],
      },
    },
    action_items: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          task: { type: 'string', description: 'Task description' },
          assignee: { type: 'string', description: 'Person responsible' },
          due_date: { type: 'string', format: 'date' },
          priority: { type: 'string', enum: ['low', 'medium', 'high', 'urgent'] },
          status: { type: 'string', enum: ['pending', 'in_progress', 'completed'] },
        },
        required: ['task', 'assignee'],
      },
    },
    next_meeting: {
      type: 'object',
      properties: {
        date: { type: 'string', format: 'date' },
        time: { type: 'string' },
        agenda_preview: { type: 'string' },
      },
    },
  },
  required: ['meeting_title', 'date', 'attendees'],
  additionalProperties: false,
};

// Code documentation generation
const codeDocumentationSchema: StructuredOutputSchema = {
  type: 'object',
  properties: {
    summary: {
      type: 'string',
      description: 'Brief description of what the code does',
    },
    parameters: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          name: { type: 'string' },
          type: { type: 'string' },
          description: { type: 'string' },
          required: { type: 'boolean' },
          default: { type: 'string' },
        },
        required: ['name', 'type', 'description'],
      },
      description: 'Function/method parameters',
    },
    returns: {
      type: 'object',
      properties: {
        type: { type: 'string' },
        description: { type: 'string' },
      },
    },
    throws: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          type: { type: 'string' },
          description: { type: 'string' },
        },
      },
      description: 'Exceptions that may be thrown',
    },
    examples: {
      type: 'array',
      items: { type: 'string' },
      description: 'Usage examples',
    },
    complexity: {
      type: 'object',
      properties: {
        time: { type: 'string', description: 'Time complexity' },
        space: { type: 'string', description: 'Space complexity' },
      },
    },
    see_also: {
      type: 'array',
      items: { type: 'string' },
      description: 'Related functions or references',
    },
  },
  required: ['summary', 'parameters'],
  additionalProperties: false,
};

export {
  sentimentAnalysisSchema,
  productReviewSchema,
  meetingNotesSchema,
  codeDocumentationSchema,
  type StructuredOutputSchema,
};
```

### Using Structured Outputs

```typescript
// services/structuredOutputService.ts - Structured outputs implementation
import OpenAI from 'openai';
import { StructuredOutputSchema } from '../schemas/outputs';

export class StructuredOutputService {
  private client: OpenAI;
  
  constructor(client: OpenAI) {
    this.client = client;
  }
  
  async extractStructuredData<T>(
    text: string,
    schema: StructuredOutputSchema,
    systemPrompt?: string
  ): Promise<T> {
    const defaultPrompt = `You are a data extraction specialist. Extract information from the provided text according to the specified schema. Always output valid JSON matching the exact schema structure. Do not add extra fields or modify the structure.`;
    
    const response = await this.client.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        { role: 'system', content: systemPrompt || defaultPrompt },
        { role: 'user', content: `Extract data from this text:\n\n${text}\n\nSchema:\n${JSON.stringify(schema, null, 2)}` },
      ],
      response_format: {
        type: 'json_schema',
        json_schema: schema,
      },
      temperature: 0.1, // Low temperature for consistent extraction
    });
    
    const content = response.choices[0].message.content;
    if (!content) {
      throw new Error('No content in response');
    }
    
    return JSON.parse(content) as T;
  }
  
  async analyzeSentiment(text: string): Promise<{
    sentiment: 'positive' | 'negative' | 'neutral' | 'mixed';
    confidence: number;
    aspects: Array<{ aspect: string; sentiment: string; evidence: string }>;
    summary: string;
  }> {
    const schema: StructuredOutputSchema = {
      type: 'object',
      properties: {
        sentiment: {
          type: 'string',
          enum: ['positive', 'negative', 'neutral', 'mixed'],
        },
        confidence: { type: 'number', minimum: 0, maximum: 1 },
        aspects: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              aspect: { type: 'string' },
              sentiment: { type: 'string', enum: ['positive', 'negative', 'neutral'] },
              evidence: { type: 'string' },
            },
            required: ['aspect', 'sentiment', 'evidence'],
          },
        },
        summary: { type: 'string' },
      },
      required: ['sentiment', 'confidence', 'summary'],
    };
    
    return this.extractStructuredData(text, schema);
  }
  
  async extractProductReview(text: string): Promise<{
    product_name: string;
    overall_rating: number;
    pros: string[];
    cons: string[];
    recommended: boolean;
    verified_purchase?: boolean;
    categories?: string[];
  }> {
    const schema: StructuredOutputSchema = {
      type: 'object',
      properties: {
        product_name: { type: 'string' },
        overall_rating: { type: 'number', minimum: 1, maximum: 5 },
        pros: { type: 'array', items: { type: 'string' } },
        cons: { type: 'array', items: { type: 'string' } },
        recommended: { type: 'boolean' },
        verified_purchase: { type: 'boolean' },
        categories: { type: 'array', items: { type: 'string' } },
      },
      required: ['product_name', 'overall_rating', 'recommended'],
    };
    
    return this.extractStructuredData(text, schema);
  }
  
  async extractMeetingNotes(text: string): Promise<{
    meeting_title: string;
    date: string;
    duration_minutes?: number;
    attendees: Array<{ name: string; role?: string }>;
    agenda: string[];
    decisions: Array<{ decision: string; owner?: string; deadline?: string }>;
    action_items: Array<{ task: string; assignee: string; due_date?: string }>;
  }> {
    const schema: StructuredOutputSchema = {
      type: 'object',
      properties: {
        meeting_title: { type: 'string' },
        date: { type: 'string' },
        duration_minutes: { type: 'integer' },
        attendees: {
          type: 'array',
          items: {
            type: 'object',
            properties: { name: { type: 'string' }, role: { type: 'string' } },
            required: ['name'],
          },
        },
        agenda: { type: 'array', items: { type: 'string' } },
        decisions: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              decision: { type: 'string' },
              owner: { type: 'string' },
              deadline: { type: 'string' },
            },
            required: ['decision'],
          },
        },
        action_items: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              task: { type: 'string' },
              assignee: { type: 'string' },
              due_date: { type: 'string' },
            },
            required: ['task', 'assignee'],
          },
        },
      },
      required: ['meeting_title', 'date', 'attendees'],
    };
    
    return this.extractStructuredData(text, schema);
  }
}
```

## Streaming Responses

### Streaming Implementation

```typescript
// services/streamingService.ts - Streaming responses implementation
import OpenAI from 'openai';

interface StreamChunk {
  content: string;
  isComplete: boolean;
  usage?: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
}

export class StreamingService {
  private client: OpenAI;
  
  constructor(client: OpenAI) {
    this.client = client;
  }
  
  async *streamChatCompletion(
    messages: Array<{ role: string; content: string }>,
    options: {
      model?: string;
      temperature?: number;
      maxTokens?: number;
    } = {}
  ): AsyncGenerator<StreamChunk, void, unknown> {
    const stream = await this.client.chat.completions.create({
      model: options.model || 'gpt-4o',
      messages,
      temperature: options.temperature,
      max_tokens: options.maxTokens,
      stream: true,
    });
    
    let fullContent = '';
    
    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content;
      if (content) {
        fullContent += content;
        yield {
          content,
          isComplete: false,
        };
      }
      
      // Check if stream is complete
      if (chunk.choices[0]?.finish_reason) {
        yield {
          content: '',
          isComplete: true,
          usage: chunk.usage ? {
            promptTokens: chunk.usage.prompt_tokens,
            completionTokens: chunk.usage.completion_tokens,
            totalTokens: chunk.usage.total_tokens,
          } : undefined,
        };
      }
    }
  }
  
  async streamWithProgress(
    messages: Array<{ role: string; content: string }>,
    onProgress: (content: string) => void,
    onComplete: (result: { content: string; usage?: any }) => void
  ): Promise<void> {
    let fullContent = '';
    
    for await (const chunk of this.streamChatCompletion(messages)) {
      if (chunk.content) {
        fullContent += chunk.content;
        onProgress(fullContent);
      }
      
      if (chunk.isComplete) {
        onComplete({ content: fullContent, usage: chunk.usage });
      }
    }
  }
}

// SSE streaming for web applications
export function createSSEStream(
  openaiService: StreamingService,
  messages: Array<{ role: string; content: string }>,
  options?: any
): ReadableStream {
  const encoder = new TextEncoder();
  
  return new ReadableStream({
    async start(controller) {
      try {
        for await (const chunk of openaiService.streamChatCompletion(messages, options)) {
          if (chunk.content) {
            const data = `data: ${JSON.stringify({ content: chunk.content })}\n\n`;
            controller.enqueue(encoder.encode(data));
          }
          
          if (chunk.isComplete) {
            const finalData = `data: ${JSON.stringify({ 
              done: true, 
              usage: chunk.usage 
            })}\n\n`;
            controller.enqueue(encoder.encode(finalData));
            controller.close();
          }
        }
      } catch (error) {
        const errorData = `data: ${JSON.stringify({ error: error.message })}\n\n`;
        controller.enqueue(encoder.encode(errorData));
        controller.close();
      }
    },
  });
}
```

## Common Patterns

### Conversation Management

```typescript
// services/conversationManager.ts - Conversation state management
import { EventEmitter } from 'events';

interface Message {
  id: string;
  role: 'system' | 'user' | 'assistant';
  content: string;
  timestamp: Date;
  metadata?: {
    tokens?: number;
    cost?: number;
    model?: string;
    finishReason?: string;
  };
}

interface Conversation {
  id: string;
  messages: Message[];
  metadata: {
    created: Date;
    updated: Date;
    messageCount: number;
    totalTokens: number;
    totalCost: number;
  };
}

const MAX_CONTEXT_TOKENS = 128000; // gpt-4o context limit
const RESERVE_TOKENS = 2000; // Reserve for response

export class ConversationManager extends EventEmitter {
  private conversations: Map<string, Conversation> = new Map();
  private tokenLimits: Map<string, number> = new Map();
  
  constructor(defaultTokenLimit: number = MAX_CONTEXT_TOKENS - RESERVE_TOKENS) {
    super();
    this.tokenLimits.set('default', defaultTokenLimit);
  }
  
  createConversation(id?: string, systemMessage?: string): string {
    const conversationId = id || `conv_${Date.now()}`;
    const messages: Message[] = [];
    
    if (systemMessage) {
      messages.push({
        id: `msg_${Date.now()}_0`,
        role: 'system',
        content: systemMessage,
        timestamp: new Date(),
      });
    }
    
    this.conversations.set(conversationId, {
      id: conversationId,
      messages,
      metadata: {
        created: new Date(),
        updated: new Date(),
        messageCount: messages.length,
        totalTokens: 0,
        totalCost: 0,
      },
    });
    
    this.emit('conversation:created', conversationId);
    return conversationId;
  }
  
  addMessage(
    conversationId: string,
    role: 'user' | 'assistant',
    content: string,
    metadata?: Message['metadata']
  ): Message {
    const conversation = this.conversations.get(conversationId);
    if (!conversation) {
      throw new Error(`Conversation ${conversationId} not found`);
    }
    
    const message: Message = {
      id: `msg_${Date.now()}_${conversation.messages.length}`,
      role,
      content,
      timestamp: new Date(),
      metadata,
    };
    
    conversation.messages.push(message);
    conversation.metadata.updated = new Date();
    conversation.metadata.messageCount = conversation.messages.length;
    conversation.metadata.totalTokens += metadata?.tokens || 0;
    conversation.metadata.totalCost += metadata?.cost || 0;
    
    this.emit('message:added', { conversationId, message });
    return message;
  }
  
  getMessages(conversationId: string, limitTokens?: number): Message[] {
    const conversation = this.conversations.get(conversationId);
    if (!conversation) {
      throw new Error(`Conversation ${conversationId} not found`);
    }
    
    let messages = conversation.messages;
    
    if (limitTokens) {
      messages = this.pruneToTokenLimit(conversation.messages, limitTokens);
    }
    
    return messages;
  }
  
  private pruneToTokenLimit(messages: Message[], maxTokens: number): Message[] {
    // Estimate tokens (rough: 4 chars per token)
    const estimateTokens = (msg: Message) => Math.ceil(msg.content.length / 4) + 10; // 10 tokens overhead
    
    let totalTokens = 0;
    const prunedMessages: Message[] = [];
    
    // Iterate from newest to oldest
    for (let i = messages.length - 1; i >= 0; i--) {
      const msg = messages[i];
      const msgTokens = estimateTokens(msg);
      
      if (totalTokens + msgTokens <= maxTokens) {
        prunedMessages.unshift(msg);
        totalTokens += msgTokens;
      } else {
        // If we hit the limit, check if we should keep system message
        if (msg.role === 'system' && prunedMessages.length === 0) {
          prunedMessages.unshift(msg);
        }
        break;
      }
    }
    
    // Always keep at least system message and last user message
    if (prunedMessages.length === 0) {
      const systemMsg = messages.find(m => m.role === 'system');
      const lastUserMsg = messages.filter(m => m.role === 'user').pop();
      const lastAssistantMsg = messages.filter(m => m.role === 'assistant').pop();
      
      if (systemMsg) prunedMessages.push(systemMsg);
      if (lastAssistantMsg) prunedMessages.push(lastAssistantMsg);
      if (lastUserMsg) prunedMessages.push(lastUserMsg);
    }
    
    return prunedMessages;
  }
  
  summarizeConversation(conversationId: string, summarizer: (messages: Message[]) => Promise<string>): Promise<string> {
    const conversation = this.conversations.get(conversationId);
    if (!conversation) {
      throw new Error(`Conversation ${conversationId} not found`);
    }
    
    // Keep system message and last exchange
    const systemMsg = conversation.messages.find(m => m.role === 'system');
    const recentMessages = conversation.messages.slice(-4); // Last 2 exchanges
    
    const summaryPrompt = `Summarize the following conversation concisely, maintaining key information and context:\n\n`;
    const content = recentMessages
      .filter(m => m.role !== 'system')
      .map(m => `${m.role}: ${m.content}`)
      .join('\n');
    
    return summarizer([
      { id: 'temp', role: 'user', content: summaryPrompt + content, timestamp: new Date() },
    ]);
  }
  
  deleteConversation(conversationId: string): boolean {
    const deleted = this.conversations.delete(conversationId);
    if (deleted) {
      this.emit('conversation:deleted', conversationId);
    }
    return deleted;
  }
  
  getConversation(conversationId: string): Conversation | undefined {
    return this.conversations.get(conversationId);
  }
  
  getAllConversations(): Conversation[] {
    return Array.from(this.conversations.values());
  }
}
```

## Troubleshooting

### Common Issues và Solutions

```typescript
// troubleshooting/chatIssues.ts - Common Chat API issues

interface IssueGuide {
  issue: string;
  symptoms: string[];
  causes: string[];
  solutions: string[];
}

export const chatIssueGuides: IssueGuide[] = [
  {
    issue: 'Inconsistent Responses',
    symptoms: [
      'Same input produces different outputs',
      'Model ignores system instructions',
      'Inconsistent formatting in responses',
    ],
    causes: [
      'Temperature too high',
      'System prompt not specific enough',
      'Context overflow causing instability',
    ],
    solutions: [
      'Lower temperature to 0.1-0.3 for consistent outputs',
      'Add more specific instructions in system prompt',
      'Implement few-shot examples for desired format',
      'Clear old messages when context gets full',
    ],
  },
  {
    issue: 'Truncated Responses',
    symptoms: [
      'Responses cut off mid-sentence',
      'Incomplete JSON outputs',
      'Unfinished code blocks',
    ],
    causes: [
      'max_tokens too low',
      'Response approaching context limit',
      'Network timeout',
    ],
    solutions: [
      'Increase max_tokens limit',
      'Set max_tokens based on expected response length + buffer',
      'Implement streaming to handle long responses',
      'Add stop sequences for structured outputs',
    ],
  },
  {
    issue: 'Off-Topic Responses',
    symptoms: [
      'Model ignores user request',
      'Assistant talks about unrelated topics',
      'System instructions not followed',
    ],
    causes: [
      'System prompt too weak or vague',
      'Conflicting user instructions',
      'Model confused by conversation history',
    ],
    solutions: [
      'Strengthen system prompt with explicit instructions',
      'Use clearer, more directive language',
      'Add examples of desired behavior',
      'Consider starting fresh conversation',
    ],
  },
  {
    issue: 'Slow Response Times',
    symptoms: [
      'High latency on API calls',
      'Streaming chunks arrive slowly',
      'Timeouts on long responses',
    ],
    causes: [
      'Large context (many tokens)',
      'Complex request requiring more reasoning',
      'Rate limit throttling',
    ],
    solutions: [
      'Optimize context by pruning old messages',
      'Use gpt-4o-mini for faster responses when appropriate',
      'Implement caching for repeated queries',
      'Consider async processing for non-critical requests',
    ],
  },
  {
    issue: 'Function Calling Failures',
    symptoms: [
      'Function not called when expected',
      'Wrong function called',
      'Malformed function arguments',
    ],
    causes: [
      'Function descriptions unclear',
      'Parameters schema not strict enough',
      'Model misunderstanding intent',
    ],
    solutions: [
      'Write clearer, more specific function descriptions',
      'Use required parameters properly',
      'Add enum constraints where applicable',
      'Test with various user queries to refine',
    ],
  },
];
```

## Code Examples hoàn chỉnh

### Complete Chat Application

```typescript
// example/chatApplication.ts - Full production chat implementation
import OpenAI from 'openai';
import { ConversationManager } from '../services/conversationManager';
import { StreamingService } from '../services/streamingService';
import { FunctionCallingService } from '../services/functionCallingService';

interface ChatConfig {
  model: string;
  temperature: number;
  maxTokens: number;
  enableFunctions: boolean;
  enableStreaming: boolean;
}

interface ChatRequest {
  message: string;
  conversationId?: string;
  systemPrompt?: string;
  config?: Partial<ChatConfig>;
}

interface ChatResponse {
  conversationId: string;
  message: string;
  metadata: {
    tokens: number;
    cost: number;
    model: string;
    latency: number;
    finishReason: string;
  };
}

export class ChatApplication {
  private client: OpenAI;
  private conversationManager: ConversationManager;
  private streamingService: StreamingService;
  private functionCallingService: FunctionCallingService;
  private defaultConfig: ChatConfig;
  
  constructor(apiKey: string) {
    this.client = new OpenAI({ apiKey });
    this.conversationManager = new ConversationManager();
    this.streamingService = new StreamingService(this.client);
    this.functionCallingService = new FunctionCallingService(this.client);
    
    this.defaultConfig = {
      model: 'gpt-4o',
      temperature: 0.7,
      maxTokens: 4096,
      enableFunctions: true,
      enableStreaming: false,
    };
  }
  
  async chat(request: ChatRequest): Promise<ChatResponse> {
    const startTime = Date.now();
    const config = { ...this.defaultConfig, ...request.config };
    
    // Get or create conversation
    let conversationId = request.conversationId;
    if (!conversationId) {
      conversationId = this.conversationManager.createConversation(
        undefined,
        request.systemPrompt
      );
    }
    
    // Add user message
    this.conversationManager.addMessage(conversationId, 'user', request.message);
    
    // Get conversation messages
    const messages = this.conversationManager.getMessages(conversationId);
    
    // Make API call
    let responseContent: string;
    let finishReason = 'stop';
    let usage = { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 };
    
    if (config.enableFunctions) {
      const result = await this.functionCallingService.chatWithFunctions(
        messages.map(m => ({ role: m.role, content: m.content }))
      );
      
      // Get the last assistant message
      const assistantMessages = result.messages.filter(m => m.role === 'assistant');
      responseContent = assistantMessages[assistantMessages.length - 1]?.content || '';
      
      // Add assistant message to conversation
      const assistantMsg = this.conversationManager.addMessage(
        conversationId,
        'assistant',
        responseContent,
        {
          model: config.model,
          tokens: usage.total_tokens,
        }
      );
      
    } else {
      const response = await this.client.chat.completions.create({
        model: config.model,
        messages: messages.map(m => ({ role: m.role, content: m.content })),
        temperature: config.temperature,
        max_tokens: config.maxTokens,
      });
      
      responseContent = response.choices[0]?.message?.content || '';
      finishReason = response.choices[0]?.finish_reason || 'stop';
      usage = response.usage || usage;
      
      // Add assistant message
      this.conversationManager.addMessage(conversationId, 'assistant', responseContent, {
        model: config.model,
        tokens: usage.total_tokens,
        cost: this.calculateCost(usage, config.model),
      });
    }
    
    const latency = Date.now() - startTime;
    
    return {
      conversationId,
      message: responseContent,
      metadata: {
        tokens: usage.total_tokens,
        cost: this.calculateCost(usage, config.model),
        model: config.model,
        latency,
        finishReason,
      },
    };
  }
  
  async *streamChat(request: ChatRequest): AsyncGenerator<string, void, unknown> {
    const config = { ...this.defaultConfig, ...request.config };
    
    let conversationId = request.conversationId;
    if (!conversationId) {
      conversationId = this.conversationManager.createConversation(
        undefined,
        request.systemPrompt
      );
    }
    
    this.conversationManager.addMessage(conversationId, 'user', request.message);
    
    const messages = this.conversationManager.getMessages(conversationId);
    
    for await (const chunk of this.streamingService.streamChatCompletion(
      messages.map(m => ({ role: m.role, content: m.content })),
      {
        model: config.model,
        temperature: config.temperature,
        maxTokens: config.maxTokens,
      }
    )) {
      if (chunk.content) {
        yield chunk.content;
      }
      
      if (chunk.isComplete) {
        // Add complete response to conversation
        const conversation = this.conversationManager.getConversation(conversationId);
        if (conversation) {
          const assistantMessages = conversation.messages.filter(m => m.role === 'assistant');
          // Response already added incrementally during streaming
        }
      }
    }
  }
  
  private calculateCost(
    usage: { prompt_tokens: number; completion_tokens: number },
    model: string
  ): number {
    const pricing: Record<string, { input: number; output: number }> = {
      'gpt-4o': { input: 2.5, output: 10.0 },
      'gpt-4o-mini': { input: 0.15, output: 0.6 },
      'gpt-4-turbo': { input: 10.0, output: 30.0 },
      'gpt-3.5-turbo': { input: 0.5, output: 1.5 },
    };
    
    const modelPricing = pricing[model] || pricing['gpt-4o'];
    const inputCost = (usage.prompt_tokens / 1_000_000) * modelPricing.input;
    const outputCost = (usage.completion_tokens / 1_000_000) * modelPricing.output;
    
    return inputCost + outputCost;
  }
  
  getConversation(conversationId: string) {
    return this.conversationManager.getConversation(conversationId);
  }
  
  deleteConversation(conversationId: string) {
    return this.conversationManager.deleteConversation(conversationId);
  }
}
```

## References

### Official Documentation

- [Chat Completions API](https://platform.openai.com/docs/api-reference/chat)
- [Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [Streaming](https://platform.openai.com/docs/guides/streaming)
- [Token Counting](https://platform.openai.com/docs/token-counting)

### Model Information

- [GPT-4o](https://platform.openai.com/docs/models/gpt-4o)
- [GPT-4o Mini](https://platform.openai.com/docs/models/gpt-4o-mini)
- [GPT-4 Turbo](https://platform.openai.com/docs/models/gpt-4-turbo)
- [GPT-3.5 Turbo](https://platform.openai.com/docs/models/gpt-3-5-turbo)

### Additional Resources

- [ChatGPT Best Practices](https://platform.openai.com/docs/guides/gpt-best-practices)
- [API Cookbook Examples](https://github.com/openai/openai-cookbook)
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)

---

**Tài liệu này là một phần của Cursor Enterprise Framework Generator.**
