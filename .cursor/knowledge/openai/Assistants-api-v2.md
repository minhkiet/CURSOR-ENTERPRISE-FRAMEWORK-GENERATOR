---
title: Assistants API v2
description: Hướng dẫn toàn diện về Assistants API v2, threads, messages, runs, tools và streaming responses
tags: [openai, assistants, api, threads, tools, typescript, python]
created: 2026-06-23
version: 1.0.0
framework: cursor-enterprise
---

# Assistants API v2

## Tổng quan

Assistants API là một trong những capabilities mạnh mẽ nhất của OpenAI, cho phép developers xây dựng AI assistants với khả năng thực hiện multi-step tasks thông qua việc sử dụng tools như code interpreter, file search, và function calling. Khác với Chat Completions API đòi hỏi developers tự quản lý conversation state và tool orchestration, Assistants API cung cấp một managed framework cho việc xây dựng persistent assistants.

API này hỗ trợ ba loại tools chính: Code Interpreter cho phép assistants execute code để thực hiện calculations, analyze data, và generate outputs; File Search cho phép tìm kiếm trong knowledge bases để retrieve relevant information; Function Tools cho phép assistants call external APIs và perform actions trong thế giới thực.

Với Assistants API, developers có thể tạo ra các ứng dụng phức tạp như customer support bots, data analysis assistants, coding helpers, và nhiều hơn nữa. Trong tài liệu này, chúng ta sẽ cover mọi aspect của Assistants API từ basic setup đến advanced production patterns.

## Mục đích và Phạm vi

Tài liệu này cung cấp hướng dẫn toàn diện về Assistants API v2 cho các developers muốn xây dựng AI-powered applications. Phạm vi bao gồm từ basic assistant creation và configuration, đến advanced topics như tool management, streaming responses, và multi-turn conversation handling.

Chúng tôi sẽ cover practical implementation patterns cho cả TypeScript và Python, với focus on production-ready solutions. Các topics bao gồm thread management, run lifecycle, tool definitions, file handling, và error handling strategies.

## Các Khái niệm Chính

### Architecture Overview

Assistants API được thiết kế với một số core concepts hoạt động cùng nhau để tạo ra một complete agentic system:

**Assistant** là persistent entity được tạo bởi developer, với instructions định nghĩa behavior, tools mà nó có thể sử dụng, và model preferences. Assistants có thể be reused across multiple conversations và maintain state through their tools.

**Thread** represents a conversation session giữa user và assistant. Threads chứa Messages và automatically manage truncation để fit content vào model context window. Mỗi conversation với user tạo ra một Thread mới, và assistants có thể maintain multiple active threads.

**Message** là individual piece of content trong một Thread. Messages có thể be from user hoặc from assistant, và có thể chứa text, images, hoặc files. Messages được automatically processed và added to thread.

**Run** là một invocation của Assistant on a Thread để generate a response. Runs handle message processing, tool execution, và response generation. Multiple runs có thể happen sequentially trong một thread để complete complex tasks.

### Tool Types

Assistants API supports three types of tools:

**Code Interpreter** cho phép assistants write và execute Python code trong một sandboxed environment. Đây là tool mạnh mẽ cho data analysis, calculations, file processing, và text generation. Assistant có thể write code, execute nó, nhận output, và use results để tiếp tục conversation.

**File Search** (Vector Store) cho phép assistants search through uploaded files để find relevant information. Files được organized into vector stores với automatic chunking và embedding. Assistant có thể retrieve relevant chunks và use chúng as context for responses.

**Function Tools** là custom tools được defined by developer. Giống như function calling trong Chat Completions API, function tools cho phép assistants call external APIs, access databases, hoặc perform any external actions.

## Assistant Creation và Configuration

### Basic Setup

```typescript
// services/assistantService.ts - Assistant management
import OpenAI from 'openai';

interface AssistantConfig {
  name: string;
  instructions: string;
  model?: string;
  description?: string;
  tools?: Tool[];
  fileIds?: string[];
  temperature?: number;
  topP?: number;
}

interface Tool {
  type: 'code_interpreter' | 'file_search' | 'function';
  function?: {
    name: string;
    description: string;
    parameters: any;
  };
}

export class AssistantService {
  private client: OpenAI;
  
  constructor(client: OpenAI) {
    this.client = client;
  }
  
  async createAssistant(config: AssistantConfig): Promise<string> {
    const assistant = await this.client.beta.assistants.create({
      name: config.name,
      instructions: config.instructions,
      model: config.model || 'gpt-4o',
      description: config.description,
      tools: config.tools || [],
      tool_resources: config.fileIds ? {
        file_search: {
          vector_store_ids: config.fileIds,
        },
      } : undefined,
      temperature: config.temperature,
      top_p: config.topP,
    });
    
    return assistant.id;
  }
  
  async getAssistant(assistantId: string) {
    return await this.client.beta.assistants.retrieve(assistantId);
  }
  
  async updateAssistant(
    assistantId: string,
    updates: Partial<AssistantConfig>
  ) {
    return await this.client.beta.assistants.update(assistantId, {
      name: updates.name,
      instructions: updates.instructions,
      description: updates.description,
      tools: updates.tools,
      temperature: updates.temperature,
      top_p: updates.topP,
    });
  }
  
  async deleteAssistant(assistantId: string): Promise<void> {
    await this.client.beta.assistants.delete(assistantId);
  }
  
  async listAssistants(limit: number = 20) {
    const assistants = await this.client.beta.assistants.list({ limit });
    return assistants.data;
  }
}
```

```python
# services/assistant_service.py - Assistant management
from openai import OpenAI
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Tool:
    type: str  # 'code_interpreter', 'file_search', 'function'
    function: Optional[Dict[str, Any]] = None

class AssistantService:
    """Service for managing OpenAI Assistants."""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    def create_assistant(
        self,
        name: str,
        instructions: str,
        model: str = 'gpt-4o',
        description: Optional[str] = None,
        tools: Optional[List[Tool]] = None,
        file_ids: Optional[List[str]] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
    ) -> str:
        """Create a new assistant."""
        params = {
            'name': name,
            'instructions': instructions,
            'model': model,
        }
        
        if description:
            params['description'] = description
        
        if tools:
            params['tools'] = [
                {
                    'type': t.type,
                    'function': t.function,
                }
                for t in tools if t.type == 'function'
            ] + [
                {'type': t.type}
                for t in tools if t.type != 'function'
            ]
        
        if file_ids:
            params['tool_resources'] = {
                'file_search': {
                    'vector_store_ids': file_ids,
                }
            }
        
        if temperature is not None:
            params['temperature'] = temperature
        
        if top_p is not None:
            params['top_p'] = top_p
        
        assistant = self.client.beta.assistants.create(**params)
        return assistant.id
    
    def get_assistant(self, assistant_id: str) -> Dict[str, Any]:
        """Get assistant details."""
        return self.client.beta.assistants.retrieve(assistant_id)
    
    def update_assistant(
        self,
        assistant_id: str,
        **updates
    ) -> Dict[str, Any]:
        """Update assistant configuration."""
        return self.client.beta.assistants.update(assistant_id, **updates)
    
    def delete_assistant(self, assistant_id: str) -> None:
        """Delete an assistant."""
        self.client.beta.assistants.delete(assistant_id)
    
    def list_assistants(self, limit: int = 20) -> List[Dict[str, Any]]:
        """List all assistants."""
        assistants = self.client.beta.assistants.list(limit=limit)
        return assistants.data
```

### Assistant Templates

```typescript
// templates/assistantTemplates.ts - Pre-configured assistant templates

interface AssistantTemplate {
  name: string;
  description: string;
  instructions: string;
  tools: Tool[];
  suggestedPrompts?: string[];
}

const dataAnalystTemplate: AssistantTemplate = {
  name: 'Data Analyst',
  description: 'Analyzes data, creates visualizations, and provides insights',
  instructions: `Bạn là một Data Analyst chuyên nghiệp với khả năng phân tích dữ liệu xuất sắc.

## Khả năng:
- Phân tích datasets và trích xuất insights
- Tạo visualizations và charts
- Thực hiện statistical analyses
- Làm sạch và transform dữ liệu
- Trả lời câu hỏi về dữ liệu

## Phong cách làm việc:
1. Hiểu rõ câu hỏi/requirement của user
2. Viết và execute code để phân tích
3. Giải thích kết quả một cách rõ ràng
4. Đề xuất additional analyses nếu phù hợp

## Output format:
- Luôn include code đã sử dụng
- Trình bày kết quả dưới dạng bảng hoặc chart khi phù hợp
- Giải thích ý nghĩa của các con số

## Giới hạn:
- Chỉ sử dụng pandas, numpy, matplotlib, seaborn, plotly
- Không thực hiện các tác vụ outside sandbox
- Nếu data không đủ, thông báo cho user`,
  tools: [{ type: 'code_interpreter' }],
  suggestedPrompts: [
    'Phân tích xu hướng doanh thu quý này',
    'So sánh hiệu suất của các sản phẩm',
    'Tạo biểu đồ phân bố khách hàng',
    'Tìm outliers trong dataset',
  ],
};

const customerSupportTemplate: AssistantTemplate = {
  name: 'Customer Support Agent',
  description: 'Helps customers with inquiries and support requests',
  instructions: `Bạn là một Customer Support Agent chuyên nghiệp cho TechCorp, công ty SaaS về quản lý dự án.

## Thông tin công ty:
- Founded: 2018
- Products: TaskFlow Pro, TeamSync, AnalyticsHub
- Support Email: support@techcorp.com
- Support Hours: 24/7

## Nguyên tắc phục vụ:
1. Empathy: Luôn thể hiện sự thấu hiểu với khách hàng
2. Clarity: Giải thích rõ ràng, tránh jargon
3. Efficiency: Cố gắng resolve trong một response
4. Professionalism: Thân thiện nhưng chuyên nghiệp

## Quy trình xử lý:
1. Xác nhận đã hiểu vấn đề
2. Hỏi thông tin bổ sung nếu cần
3. Cung cấp giải pháp cụ thể
4. Confirm resolution
5. Offer additional help

## Giới hạn:
- Không shared confidential information
- Không make promises về features
- Escalate billing/security issues
- Không cung cấp refund without approval`,
  tools: [{ type: 'file_search' }],
  suggestedPrompts: [
    'Tôi không đăng nhập được tài khoản',
    'Làm sao để tạo mới project?',
    'Báo cáo lỗi khi export dữ liệu',
    'Hướng dẫn thiết lập integration',
  ],
};

const codingAssistantTemplate: AssistantTemplate = {
  name: 'Coding Assistant',
  description: 'Helps with code writing, debugging, and explanations',
  instructions: `Bạn là một Senior Software Engineer với deep expertise trong multiple programming languages và frameworks.

## Expertise:
- Languages: TypeScript, Python, Java, Go, Rust, C++
- Frontend: React, Vue, Angular, Next.js, Nuxt.js
- Backend: Node.js, Django, FastAPI, Spring Boot
- Databases: PostgreSQL, MongoDB, Redis, Elasticsearch
- Cloud: AWS, GCP, Azure, Docker, Kubernetes

## Code Standards:
- Write clean, maintainable code
- Follow best practices và design patterns
- Include proper error handling
- Add comments for complex logic
- Consider performance và scalability

## Response Structure:
1. Brief explanation của approach
2. Code solution với comments
3. Time/Space complexity
4. Potential improvements
5. Testing suggestions

## Examples format:
\`\`\`language
// Code here
\`\`\``,
  tools: [
    { type: 'code_interpreter' },
    { type: 'function', function: { name: 'search_documentation', description: 'Search internal documentation', parameters: { type: 'object', properties: { query: { type: 'string' } }, required: ['query'] } } },
  ],
  suggestedPrompts: [
    'Viết function để sort array',
    'Debug lỗi authentication',
    'Giải thích đoạn code này',
    'Review pull request này',
  ],
};

const researchAssistantTemplate: AssistantTemplate = {
  name: 'Research Assistant',
  description: 'Helps with research, summarization, and information retrieval',
  instructions: `Bạn là một Research Assistant chuyên nghiệp, giúp users tìm kiếm và synthesize information.

## Capabilities:
- Search và summarize documents
- Compare và contrast information
- Extract key findings
- Generate literature reviews
- Create citations

## Research Process:
1. Xác định research scope và questions
2. Search relevant information
3. Evaluate source quality
4. Synthesize findings
5. Present với proper citations

## Output Formats:
- Executive summaries
- Detailed reports
- Comparison tables
- Annotated bibliographies
- Key findings highlights`,
  tools: [
    { type: 'file_search' },
    { type: 'function', function: { name: 'search_web', description: 'Search the web for information', parameters: { type: 'object', properties: { query: { type: 'string' }, limit: { type: 'integer' } }, required: ['query'] } } },
  ],
  suggestedPrompts: [
    'Tìm research về AI trends 2024',
    'So sánh different ML approaches',
    'Summarize article này',
    'Tạo literature review về topic',
  ],
};

export const assistantTemplates = {
  dataAnalyst: dataAnalystTemplate,
  customerSupport: customerSupportTemplate,
  codingAssistant: codingAssistantTemplate,
  researchAssistant: researchAssistantTemplate,
};

export class AssistantTemplateService {
  private assistantService: AssistantService;
  
  constructor(assistantService: AssistantService) {
    this.assistantService = assistantService;
  }
  
  async createFromTemplate(templateName: keyof typeof assistantTemplates): Promise<string> {
    const template = assistantTemplates[templateName];
    if (!template) {
      throw new Error(`Template "${templateName}" not found`);
    }
    
    return await this.assistantService.createAssistant({
      name: template.name,
      instructions: template.instructions,
      description: template.description,
      tools: template.tools,
    });
  }
}
```

```python
# templates/assistant_templates.py - Pre-configured assistant templates
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class AssistantTemplate:
    name: str
    description: str
    instructions: str
    tools: List[Dict[str, Any]]
    suggested_prompts: Optional[List[str]] = None

DATA_ANALYST_TEMPLATE = AssistantTemplate(
    name='Data Analyst',
    description='Analyzes data, creates visualizations, and provides insights',
    instructions="""Bạn là một Data Analyst chuyên nghiệp với khả năng phân tích dữ liệu xuất sắc.

## Khả năng:
- Phân tích datasets và trích xuất insights
- Tạo visualizations và charts
- Thực hiện statistical analyses
- Làm sạch và transform dữ liệu
- Trả lời câu hỏi về dữ liệu

## Phong cách làm việc:
1. Hiểu rõ câu hỏi/requirement của user
2. Viết và execute code để phân tích
3. Giải thích kết quả một cách rõ ràng
4. Đề xuất additional analyses nếu phù hợp

## Output format:
- Luôn include code đã sử dụng
- Trình bày kết quả dưới dạng bảng hoặc chart khi phù hợp
- Giải thích ý nghĩa của các con số""",
    tools=[{'type': 'code_interpreter'}],
    suggested_prompts=[
        'Phân tích xu hướng doanh thu quý này',
        'So sánh hiệu suất của các sản phẩm',
    ]
)

CUSTOMER_SUPPORT_TEMPLATE = AssistantTemplate(
    name='Customer Support Agent',
    description='Helps customers with inquiries and support requests',
    instructions="""Bạn là một Customer Support Agent chuyên nghiệp cho TechCorp, công ty SaaS về quản lý dự án.

## Nguyên tắc phục vụ:
1. Empathy: Luôn thể hiện sự thấu hiểu với khách hàng
2. Clarity: Giải thích rõ ràng, tránh jargon
3. Efficiency: Cố gắng resolve trong một response
4. Professionalism: Thân thiện nhưng chuyên nghiệp

## Quy trình xử lý:
1. Xác nhận đã hiểu vấn đề
2. Hỏi thông tin bổ sung nếu cần
3. Cung cấp giải pháp cụ thể
4. Confirm resolution
5. Offer additional help""",
    tools=[{'type': 'file_search'}],
    suggested_prompts=[
        'Tôi không đăng nhập được tài khoản',
        'Làm sao để tạo mới project?',
    ]
)

CODING_ASSISTANT_TEMPLATE = AssistantTemplate(
    name='Coding Assistant',
    description='Helps with code writing, debugging, and explanations',
    instructions="""Bạn là một Senior Software Engineer với deep expertise trong multiple programming languages và frameworks.

## Expertise:
- Languages: TypeScript, Python, Java, Go, Rust, C++
- Frontend: React, Vue, Angular, Next.js, Nuxt.js
- Backend: Node.js, Django, FastAPI, Spring Boot

## Code Standards:
- Write clean, maintainable code
- Follow best practices và design patterns
- Include proper error handling
- Add comments for complex logic

## Response Structure:
1. Brief explanation của approach
2. Code solution với comments
3. Time/Space complexity
4. Potential improvements
5. Testing suggestions""",
    tools=[
        {'type': 'code_interpreter'},
        {'type': 'function', 'function': {
            'name': 'search_documentation',
            'description': 'Search internal documentation',
            'parameters': {'type': 'object', 'properties': {'query': {'type': 'string'}}, 'required': ['query']}
        }}
    ],
    suggested_prompts=[
        'Viết function để sort array',
        'Debug lỗi authentication',
    ]
)

TEMPLATES = {
    'data_analyst': DATA_ANALYST_TEMPLATE,
    'customer_support': CUSTOMER_SUPPORT_TEMPLATE,
    'coding_assistant': CODING_ASSISTANT_TEMPLATE,
}

class AssistantTemplateService:
    """Service for creating assistants from templates."""
    
    def __init__(self, assistant_service):
        self.assistant_service = assistant_service
    
    def create_from_template(self, template_name: str) -> str:
        """Create an assistant from a predefined template."""
        if template_name not in TEMPLATES:
            raise ValueError(f'Template "{template_name}" not found')
        
        template = TEMPLATES[template_name]
        
        return self.assistant_service.create_assistant(
            name=template.name,
            instructions=template.instructions,
            description=template.description,
            tools=template.tools,
        )
```

## Thread Management

### Creating và Managing Threads

```typescript
// services/threadService.ts - Thread management
import OpenAI from 'openai';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  attachments?: Array<{
    fileId: string;
    tools: string[];
  }>;
}

interface ThreadWithMessages {
  threadId: string;
  messages: Message[];
  metadata?: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}

export class ThreadService {
  private client: OpenAI;
  
  constructor(client: OpenAI) {
    this.client = client;
  }
  
  async createThread(
    messages?: Message[],
    metadata?: Record<string, any>
  ): Promise<string> {
    const threadParams: any = {};
    
    if (messages && messages.length > 0) {
      threadParams.messages = messages.map(msg => ({
        role: msg.role,
        content: msg.content,
        attachments: msg.attachments,
      }));
    }
    
    if (metadata) {
      threadParams.metadata = metadata;
    }
    
    const thread = await this.client.beta.threads.create(threadParams);
    return thread.id;
  }
  
  async getThread(threadId: string) {
    return await this.client.beta.threads.retrieve(threadId);
  }
  
  async updateThread(
    threadId: string,
    metadata?: Record<string, any>
  ) {
    return await this.client.beta.threads.update(threadId, {
      metadata,
    });
  }
  
  async deleteThread(threadId: string): Promise<void> {
    await this.client.beta.threads.delete(threadId);
  }
  
  async addMessage(
    threadId: string,
    content: string,
    attachments?: Array<{ fileId: string; tools: string[] }>
  ) {
    const messageParams: any = {
      role: 'user',
      content,
    };
    
    if (attachments && attachments.length > 0) {
      messageParams.attachments = attachments;
    }
    
    return await this.client.beta.threads.messages.create(threadId, messageParams);
  }
  
  async getMessages(
    threadId: string,
    options: {
      limit?: number;
      after?: string;
      before?: string;
      order?: 'asc' | 'desc';
    } = {}
  ) {
    return await this.client.beta.threads.messages.list(threadId, {
      limit: options.limit,
      after: options.after,
      before: options.before,
      order: options.order || 'asc',
    });
  }
  
  async getMessage(threadId: string, messageId: string) {
    return await this.client.beta.threads.messages.retrieve(threadId, messageId);
  }
  
  async modifyMessage(
    threadId: string,
    messageId: string,
    metadata?: Record<string, any>
  ) {
    return await this.client.beta.threads.messages.update(threadId, messageId, {
      metadata,
    });
  }
  
  async getThreadMessagesFormatted(threadId: string): Promise<ThreadWithMessages> {
    const thread = await this.getThread(threadId);
    const messagesResponse = await this.getMessages(threadId, { order: 'asc' });
    
    const messages: Message[] = messagesResponse.data.map(msg => ({
      role: msg.role as 'user' | 'assistant',
      content: this.extractTextContent(msg.content),
      attachments: msg.attachments,
    }));
    
    return {
      threadId,
      messages,
      metadata: thread.metadata as Record<string, any>,
      createdAt: new Date(thread.created_at * 1000),
      updatedAt: new Date(thread.updated_at * 1000),
    };
  }
  
  private extractTextContent(content: any[]): string {
    if (Array.isArray(content)) {
      return content
        .filter(part => part.type === 'text')
        .map(part => part.text?.value || '')
        .join('\n');
    }
    return String(content);
  }
}
```

```python
# services/thread_service.py - Thread management
from openai import OpenAI
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    role: str  # 'user' or 'assistant'
    content: str
    attachments: Optional[List[Dict[str, Any]]] = None

@dataclass
class ThreadWithMessages:
    thread_id: str
    messages: List[Message]
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

class ThreadService:
    """Service for managing conversation threads."""
    
    def __init__(self, client: OpenAI):
        self.client = client
    
    def create_thread(
        self,
        messages: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create a new thread."""
        thread_params = {}
        
        if messages:
            thread_params['messages'] = [
                {
                    'role': msg['role'],
                    'content': msg['content'],
                    'attachments': msg.get('attachments'),
                }
                for msg in messages
            ]
        
        if metadata:
            thread_params['metadata'] = metadata
        
        thread = self.client.beta.threads.create(**thread_params)
        return thread.id
    
    def get_thread(self, thread_id: str) -> Dict[str, Any]:
        """Get thread details."""
        return self.client.beta.threads.retrieve(thread_id)
    
    def update_thread(
        self,
        thread_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update thread metadata."""
        return self.client.beta.threads.update(thread_id, metadata=metadata)
    
    def delete_thread(self, thread_id: str) -> None:
        """Delete a thread."""
        self.client.beta.threads.delete(thread_id)
    
    def add_message(
        self,
        thread_id: str,
        content: str,
        attachments: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Add a message to thread."""
        message_params = {
            'role': 'user',
            'content': content,
        }
        
        if attachments:
            message_params['attachments'] = attachments
        
        return self.client.beta.threads.messages.create(thread_id, **message_params)
    
    def get_messages(
        self,
        thread_id: str,
        limit: int = 20,
        order: str = 'asc',
    ) -> List[Dict[str, Any]]:
        """Get messages from thread."""
        messages = self.client.beta.threads.messages.list(
            thread_id,
            limit=limit,
            order=order,
        )
        return messages.data
    
    def get_message(self, thread_id: str, message_id: str) -> Dict[str, Any]:
        """Get specific message."""
        return self.client.beta.threads.messages.retrieve(thread_id, message_id)
    
    def modify_message(
        self,
        thread_id: str,
        message_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Modify message metadata."""
        return self.client.beta.threads.messages.update(
            thread_id,
            message_id,
            metadata=metadata,
        )
    
    def get_thread_formatted(self, thread_id: str) -> ThreadWithMessages:
        """Get thread with formatted messages."""
        thread = self.get_thread(thread_id)
        messages_response = self.get_messages(thread_id, order='asc')
        
        messages = [
            Message(
                role=msg.role,
                content=self._extract_text_content(msg.content),
                attachments=msg.attachments,
            )
            for msg in messages_response
        ]
        
        return ThreadWithMessages(
            thread_id=thread_id,
            messages=messages,
            metadata=thread.metadata,
            created_at=datetime.fromtimestamp(thread.created_at),
            updated_at=datetime.fromtimestamp(thread.updated_at),
        )
    
    @staticmethod
    def _extract_text_content(content: Any) -> str:
        """Extract text from message content."""
        if isinstance(content, list):
            return '\n'.join(
                part.text.value
                for part in content
                if hasattr(part, 'type') and part.type == 'text' and hasattr(part, 'text')
            )
        return str(content)
```

## Run Lifecycle

### Creating và Managing Runs

```typescript
// services/runService.ts - Run management
import OpenAI from 'openai';

type RunStatus = 'queued' | 'in_progress' | 'requires_action' | 'cancelling' | 'cancelled' | 'failed' | 'completed' | 'expired';

interface RunResult {
  runId: string;
  status: RunStatus;
  messages: any[];
  toolsUsed?: string[];
  error?: string;
}

interface ToolCall {
  id: string;
  type: 'function';
  function: {
    name: string;
    arguments: string;
  };
}

export class RunService {
  private client: OpenAI;
  
  constructor(client: OpenAI) {
    this.client = client;
  }
  
  async createRun(
    threadId: string,
    assistantId: string,
    options: {
      model?: string;
      instructions?: string;
      tools?: any[];
      temperature?: number;
      metadata?: Record<string, any>;
    } = {}
  ): Promise<string> {
    const run = await this.client.beta.threads.runs.create(threadId, {
      assistant_id: assistantId,
      model: options.model,
      instructions: options.instructions,
      tools: options.tools,
      temperature: options.temperature,
      metadata: options.metadata,
    });
    
    return run.id;
  }
  
  async getRun(threadId: string, runId: string) {
    return await this.client.beta.threads.runs.retrieve(threadId, runId);
  }
  
  async listRuns(
    threadId: string,
    options: { limit?: number; status?: RunStatus } = {}
  ) {
    const params: any = { limit: options.limit || 20 };
    if (options.status) {
      params.status = options.status;
    }
    
    return await this.client.beta.threads.runs.list(threadId, params);
  }
  
  async submitToolOutputs(
    threadId: string,
    runId: string,
    toolCalls: ToolCall[],
    outputs: Array<{ tool_call_id: string; output: string }>
  ): Promise<void> {
    await this.client.beta.threads.runs.submit_tool_outputs(threadId, runId, {
      tool_outputs: outputs,
    });
  }
  
  async cancelRun(threadId: string, runId: string): Promise<void> {
    await this.client.beta.threads.runs.cancel(threadId, runId);
  }
  
  async waitForRun(
    threadId: string,
    runId: string,
    onProgress?: (status: RunStatus) => void,
    pollIntervalMs: number = 1000
  ): Promise<RunResult> {
    return new Promise(async (resolve, reject) => {
      while (true) {
        const run = await this.getRun(threadId, runId);
        
        if (onProgress) {
          onProgress(run.status);
        }
        
        if (run.status === 'completed') {
          // Get all messages after this run
          const messages = await this.client.beta.threads.messages.list(threadId, {
            order: 'asc',
            after: `run-${runId}`,
          });
          
          resolve({
            runId: run.id,
            status: run.status,
            messages: messages.data,
            toolsUsed: run.tools?.map((t: any) => t.id),
          });
          return;
        }
        
        if (run.status === 'requires_action') {
          // Handle tool calls
          const toolCalls = run.required_action?.submit_tool_outputs.tool_calls || [];
          resolve({
            runId: run.id,
            status: run.status,
            messages: [],
            toolsUsed: toolCalls.map((tc: any) => tc.function.name),
          });
          return;
        }
        
        if (['failed', 'cancelled', 'expired'].includes(run.status)) {
          reject(new Error(`Run ${run.status}: ${run.last_error?.message || 'Unknown error'}`));
          return;
        }
        
        if (run.status === 'cancelling') {
          await new Promise(r => setTimeout(r, pollIntervalMs));
          continue;
        }
        
        // queued or in_progress - wait
        await new Promise(r => setTimeout(r, pollIntervalMs));
      }
    });
  }
}
```

```python
# services/run_service.py - Run management
from openai import OpenAI
from typing import List, Dict, Any, Optional
from enum import Enum

class RunStatus(Enum):
    QUEUED = 'queued'
    IN_PROGRESS = 'in_progress'
    REQUIRES_ACTION = 'requires_action'
    CANCELLING = 'cancelling'
    CANCELLED = 'cancelled'
    FAILED = 'failed'
    COMPLETED = 'completed'
    EXPIRED = 'expired'

@dataclass
class RunResult:
    run_id: str
    status: str
    messages: List[Dict[str, Any]]
    tools_used: Optional[List[str]] = None
    error: Optional[str] = None

@dataclass
class ToolCall:
    id: str
    type: str
    function: Dict[str, str]

class RunService:
    """Service for managing assistant runs."""
    
    def __init__(self, client: OpenAI):
        self.client = client
    
    def create_run(
        self,
        thread_id: str,
        assistant_id: str,
        model: Optional[str] = None,
        instructions: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create a new run."""
        params = {'assistant_id': assistant_id}
        
        if model:
            params['model'] = model
        if instructions:
            params['instructions'] = instructions
        if tools:
            params['tools'] = tools
        if temperature is not None:
            params['temperature'] = temperature
        if metadata:
            params['metadata'] = metadata
        
        run = self.client.beta.threads.runs.create(thread_id, **params)
        return run.id
    
    def get_run(self, thread_id: str, run_id: str) -> Dict[str, Any]:
        """Get run details."""
        return self.client.beta.threads.runs.retrieve(thread_id, run_id)
    
    def list_runs(
        self,
        thread_id: str,
        limit: int = 20,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List runs for a thread."""
        params = {'limit': limit}
        if status:
            params['status'] = status
        
        runs = self.client.beta.threads.runs.list(thread_id, **params)
        return runs.data
    
    def submit_tool_outputs(
        self,
        thread_id: str,
        run_id: str,
        tool_outputs: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """Submit tool outputs for a run."""
        return self.client.beta.threads.runs.submit_tool_outputs(
            thread_id,
            run_id,
            tool_outputs=tool_outputs,
        )
    
    def cancel_run(self, thread_id: str, run_id: str) -> Dict[str, Any]:
        """Cancel a running operation."""
        return self.client.beta.threads.runs.cancel(thread_id, run_id)
    
    def wait_for_run(
        self,
        thread_id: str,
        run_id: str,
        on_progress: Optional[callable] = None,
        poll_interval_seconds: float = 1.0,
    ) -> RunResult:
        """Wait for run to complete."""
        import time
        
        while True:
            run = self.get_run(thread_id, run_id)
            
            if on_progress:
                on_progress(run.status)
            
            if run.status == 'completed':
                # Get messages after this run
                messages = self.client.beta.threads.messages.list(
                    thread_id,
                    order='asc',
                    after=f'run-{run_id}',
                )
                
                return RunResult(
                    run_id=run.id,
                    status=run.status,
                    messages=messages.data,
                    tools_used=[t.id for t in run.tools] if run.tools else None,
                )
            
            if run.status == 'requires_action':
                tool_calls = (
                    run.required_action.submit_tool_outputs.tool_calls
                    if run.required_action
                    else []
                )
                
                return RunResult(
                    run_id=run.id,
                    status=run.status,
                    messages=[],
                    tools_used=[tc.function.name for tc in tool_calls],
                )
            
            if run.status in ['failed', 'cancelled', 'expired']:
                raise RuntimeError(
                    f"Run {run.status}: {getattr(run.last_error, 'message', 'Unknown error')}"
                )
            
            if run.status == 'cancelling':
                time.sleep(poll_interval_seconds)
                continue
            
            # queued or in_progress - wait
            time.sleep(poll_interval_seconds)
```

## Tool Implementation

### Function Tools

```typescript
// services/toolHandler.ts - Tool implementation handlers
import OpenAI from 'openai';

interface ToolDefinition {
  type: 'function';
  function: {
    name: string;
    description: string;
    parameters: any;
  };
}

interface ToolHandler {
  name: string;
  description: string;
  parameters: any;
  execute: (args: any) => Promise<any>;
}

// Weather tool
const weatherTool: ToolHandler = {
  name: 'get_weather',
  description: 'Get current weather information for a specific location',
  parameters: {
    type: 'object',
    properties: {
      location: {
        type: 'string',
        description: 'City name or location',
      },
      units: {
        type: 'string',
        enum: ['celsius', 'fahrenheit'],
        description: 'Temperature unit',
      },
    },
    required: ['location'],
  },
  execute: async (args) => {
    // Simulated weather API
    return {
      location: args.location,
      temperature: args.units === 'fahrenheit' ? 72 : 22,
      condition: 'partly_cloudy',
      humidity: 65,
      forecast: [
        { day: 'Today', high: 25, low: 18 },
        { day: 'Tomorrow', high: 23, low: 17 },
      ],
    };
  },
};

// Calendar tool
const calendarTool: ToolHandler = {
  name: 'create_calendar_event',
  description: 'Create a new event in the user calendar',
  parameters: {
    type: 'object',
    properties: {
      title: { type: 'string', description: 'Event title' },
      start_time: { type: 'string', description: 'Start time ISO 8601' },
      end_time: { type: 'string', description: 'End time ISO 8601' },
      description: { type: 'string', description: 'Event description' },
      attendees: {
        type: 'array',
        items: { type: 'string' },
        description: 'Email addresses',
      },
    },
    required: ['title', 'start_time', 'end_time'],
  },
  execute: async (args) => {
    const eventId = `evt_${Date.now()}`;
    return {
      event_id: eventId,
      title: args.title,
      start_time: args.start_time,
      end_time: args.end_time,
      status: 'confirmed',
      meeting_link: `https://meet.techcorp.com/${eventId}`,
    };
  },
};

// Database query tool
const databaseTool: ToolHandler = {
  name: 'query_database',
  description: 'Execute a SQL query against the analytics database',
  parameters: {
    type: 'object',
    properties: {
      query: {
        type: 'string',
        description: 'SQL SELECT query (no modifications allowed)',
      },
      limit: {
        type: 'integer',
        description: 'Maximum rows to return',
        default: 100,
      },
    },
    required: ['query'],
  },
  execute: async (args) => {
    // Security: Only allow SELECT queries
    const query = args.query.trim().toUpperCase();
    if (!query.startsWith('SELECT')) {
      throw new Error('Only SELECT queries are allowed');
    }
    
    // Simulated database execution
    return {
      rows: [
        { id: 1, name: 'Sample', value: 100 },
        { id: 2, name: 'Data', value: 200 },
      ],
      row_count: 2,
      execution_time_ms: 45,
    };
  },
};

// Search documentation tool
const searchDocTool: ToolHandler = {
  name: 'search_documentation',
  description: 'Search internal documentation and knowledge base',
  parameters: {
    type: 'object',
    properties: {
      query: { type: 'string', description: 'Search query' },
      category: {
        type: 'string',
        enum: ['api', 'guides', 'faq', 'all'],
        default: 'all',
      },
      limit: {
        type: 'integer',
        default: 5,
      },
    },
    required: ['query'],
  },
  execute: async (args) => {
    // Simulated documentation search
    return {
      results: [
        {
          title: 'Getting Started Guide',
          url: '/docs/getting-started',
          snippet: 'Quick start guide for new users...',
          relevance: 0.95,
        },
        {
          title: 'API Reference',
          url: '/docs/api',
          snippet: 'Complete API documentation...',
          relevance: 0.85,
        },
      ],
      total: 2,
    };
  },
};

// All available tools
export const toolHandlers: Record<string, ToolHandler> = {
  get_weather: weatherTool,
  create_calendar_event: calendarTool,
  query_database: databaseTool,
  search_documentation: searchDocTool,
};

// Convert handlers to tool definitions
export function getToolDefinitions(): ToolDefinition[] {
  return Object.values(toolHandlers).map(handler => ({
    type: 'function' as const,
    function: {
      name: handler.name,
      description: handler.description,
      parameters: handler.parameters,
    },
  }));
}

// Execute tool by name
export async function executeTool(
  name: string,
  arguments_: Record<string, any>
): Promise<any> {
  const handler = toolHandlers[name];
  if (!handler) {
    throw new Error(`Unknown tool: ${name}`);
  }
  
  return await handler.execute(arguments_);
}

// Process tool calls from a run
export async function processToolCalls(
  toolCalls: Array<{
    id: string;
    function: { name: string; arguments: string };
  }>
): Promise<Array<{ tool_call_id: string; output: string }>> {
  const outputs: Array<{ tool_call_id: string; output: string }> = [];
  
  for (const toolCall of toolCalls) {
    try {
      const args = JSON.parse(toolCall.function.arguments);
      const result = await executeTool(toolCall.function.name, args);
      outputs.push({
        tool_call_id: toolCall.id,
        output: JSON.stringify(result),
      });
    } catch (error: any) {
      outputs.push({
        tool_call_id: toolCall.id,
        output: JSON.stringify({ error: error.message }),
      });
    }
  }
  
  return outputs;
}
```

```python
# services/tool_handler.py - Tool implementation handlers
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass

@dataclass
class ToolHandler:
    name: str
    description: str
    parameters: Dict[str, Any]
    execute: Callable[[Dict[str, Any]], Any]

# Weather tool
def get_weather_handler(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get weather information."""
    return {
        'location': args['location'],
        'temperature': 22 if args.get('units') == 'celsius' else 72,
        'condition': 'partly_cloudy',
        'humidity': 65,
        'forecast': [
            {'day': 'Today', 'high': 25, 'low': 18},
            {'day': 'Tomorrow', 'high': 23, 'low': 17},
        ],
    }

WEATHER_TOOL = ToolHandler(
    name='get_weather',
    description='Get current weather information for a location',
    parameters={
        'type': 'object',
        'properties': {
            'location': {'type': 'string', 'description': 'City name'},
            'units': {
                'type': 'string',
                'enum': ['celsius', 'fahrenheit'],
            },
        },
        'required': ['location'],
    },
    execute=get_weather_handler,
)

# Calendar tool
def create_calendar_handler(args: Dict[str, Any]) -> Dict[str, Any]:
    """Create calendar event."""
    import time
    event_id = f"evt_{int(time.time())}"
    return {
        'event_id': event_id,
        'title': args['title'],
        'start_time': args['start_time'],
        'end_time': args['end_time'],
        'status': 'confirmed',
        'meeting_link': f'https://meet.techcorp.com/{event_id}',
    }

CALENDAR_TOOL = ToolHandler(
    name='create_calendar_event',
    description='Create a new calendar event',
    parameters={
        'type': 'object',
        'properties': {
            'title': {'type': 'string'},
            'start_time': {'type': 'string'},
            'end_time': {'type': 'string'},
            'description': {'type': 'string'},
            'attendees': {'type': 'array', 'items': {'type': 'string'}},
        },
        'required': ['title', 'start_time', 'end_time'],
    },
    execute=create_calendar_handler,
)

# Database tool
def query_database_handler(args: Dict[str, Any]) -> Dict[str, Any]:
    """Execute database query."""
    query = args['query'].strip().upper()
    if not query.startswith('SELECT'):
        raise ValueError('Only SELECT queries are allowed')
    
    # Simulated execution
    return {
        'rows': [
            {'id': 1, 'name': 'Sample', 'value': 100},
            {'id': 2, 'name': 'Data', 'value': 200},
        ],
        'row_count': 2,
        'execution_time_ms': 45,
    }

DATABASE_TOOL = ToolHandler(
    name='query_database',
    description='Execute SQL query against analytics database',
    parameters={
        'type': 'object',
        'properties': {
            'query': {'type': 'string'},
            'limit': {'type': 'integer', 'default': 100},
        },
        'required': ['query'],
    },
    execute=query_database_handler,
)

# Search tool
def search_documentation_handler(args: Dict[str, Any]) -> Dict[str, Any]:
    """Search documentation."""
    return {
        'results': [
            {
                'title': 'Getting Started Guide',
                'url': '/docs/getting-started',
                'snippet': 'Quick start guide...',
                'relevance': 0.95,
            },
        ],
        'total': 1,
    }

SEARCH_TOOL = ToolHandler(
    name='search_documentation',
    description='Search internal documentation',
    parameters={
        'type': 'object',
        'properties': {
            'query': {'type': 'string'},
            'category': {'type': 'string', 'enum': ['api', 'guides', 'faq', 'all']},
            'limit': {'type': 'integer', 'default': 5},
        },
        'required': ['query'],
    },
    execute=search_documentation_handler,
)

# Tool registry
TOOL_HANDLERS: Dict[str, ToolHandler] = {
    'get_weather': WEATHER_TOOL,
    'create_calendar_event': CALENDAR_TOOL,
    'query_database': DATABASE_TOOL,
    'search_documentation': SEARCH_TOOL,
}

def get_tool_definitions() -> List[Dict[str, Any]]:
    """Get all tool definitions."""
    return [
        {
            'type': 'function',
            'function': {
                'name': handler.name,
                'description': handler.description,
                'parameters': handler.parameters,
            }
        }
        for handler in TOOL_HANDLERS.values()
    ]

def execute_tool(name: str, arguments: Dict[str, Any]) -> Any:
    """Execute a tool by name."""
    if name not in TOOL_HANDLERS:
        raise ValueError(f'Unknown tool: {name}')
    
    handler = TOOL_HANDLERS[name]
    return handler.execute(arguments)

def process_tool_calls(
    tool_calls: List[Dict[str, Any]]
) -> List[Dict[str, str]]:
    """Process multiple tool calls."""
    import json
    
    outputs = []
    for tool_call in tool_calls:
        try:
            args = json.loads(tool_call['function']['arguments'])
            result = execute_tool(tool_call['function']['name'], args)
            outputs.append({
                'tool_call_id': tool_call['id'],
                'output': json.dumps(result),
            })
        except Exception as e:
            outputs.append({
                'tool_call_id': tool_call['id'],
                'output': json.dumps({'error': str(e)}),
            })
    
    return outputs
```

## Streaming Responses

### Streaming Implementation

```typescript
// services/streamingService.ts - Streaming responses for Assistants API
import OpenAI from 'openai';

interface StreamEvent {
  type: string;
  data: any;
}

interface MessageStreamData {
  content: string;
  isComplete: boolean;
  messageId?: string;
  role?: string;
}

export class AssistantStreamingService {
  private client: OpenAI;
  
  constructor(client: OpenAI) {
    this.client = client;
  }
  
  async* streamRun(
    threadId: string,
    assistantId: string,
    options: {
      tools?: any[];
      temperature?: number;
    } = {}
  ): AsyncGenerator<StreamEvent, void, unknown> {
    const stream = this.client.beta.threads.runs.stream(threadId, {
      assistant_id: assistantId,
      tools: options.tools,
      temperature: options.temperature,
    });
    
    for await (const event of stream) {
      yield this.parseEvent(event);
    }
  }
  
  async* streamRunWithMessages(
    threadId: string,
    assistantId: string,
    options: any = {}
  ): AsyncGenerator<MessageStreamData, void, unknown> {
    let currentContent = '';
    let messageId: string | undefined;
    let role: string | undefined;
    
    for await (const event of this.streamRun(threadId, assistantId, options)) {
      if (event.type === 'thread.message.created') {
        messageId = event.data.id;
        role = event.data.role;
        yield {
          content: '',
          isComplete: false,
          messageId,
          role,
        };
      }
      
      if (event.type === 'thread.message.delta') {
        const textDelta = event.data.delta?.content?.[0]?.text?.value;
        if (textDelta) {
          currentContent += textDelta;
          yield {
            content: textDelta,
            isComplete: false,
          };
        }
      }
      
      if (event.type === 'thread.message.completed') {
        yield {
          content: currentContent,
          isComplete: true,
          messageId,
          role,
        };
        return;
      }
      
      // Handle tool events
      if (event.type === 'thread.run.requires_action') {
        yield {
          content: '[Tool call required]',
          isComplete: false,
        };
      }
    }
  }
  
  private parseEvent(event: any): StreamEvent {
    const eventType = event.event;
    return {
      type: eventType,
      data: event.data,
    };
  }
}

// SSE streaming for web clients
export function createSSEResponse(
  stream: AsyncGenerator<MessageStreamData, void, unknown>
): ReadableStream {
  const encoder = new TextEncoder();
  
  return new ReadableStream({
    async start(controller) {
      try {
        for await (const data of stream) {
          const event = {
            type: data.isComplete ? 'message_complete' : 'message_delta',
            data: {
              content: data.content,
              isComplete: data.isComplete,
              messageId: data.messageId,
              role: data.role,
            },
          };
          
          controller.enqueue(
            encoder.encode(`data: ${JSON.stringify(event)}\n\n`)
          );
        }
        
        controller.enqueue(
          encoder.encode(`data: ${JSON.stringify({ type: 'stream_end' })}\n\n`)
        );
        
        controller.close();
      } catch (error: any) {
        controller.enqueue(
          encoder.encode(`data: ${JSON.stringify({ type: 'error', error: error.message })}\n\n`)
        );
        controller.close();
      }
    },
  });
}
```

```python
# services/streaming_service.py - Streaming responses for Assistants API
from openai import OpenAI
from typing import AsyncGenerator, Dict, Any, Optional
import json
import asyncio

class AssistantStreamingService:
    """Service for streaming assistant responses."""
    
    def __init__(self, client: OpenAI):
        self.client = client
    
    async def stream_run(
        self,
        thread_id: str,
        assistant_id: str,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream run events."""
        with self.client.beta.threads.runs.stream(
            thread_id,
            assistant_id=assistant_id,
            tools=tools,
            temperature=temperature,
        ) as stream:
            for event in stream:
                yield {
                    'type': event.event,
                    'data': event.data,
                }
    
    async def stream_run_with_messages(
        self,
        thread_id: str,
        assistant_id: str,
        **options
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream messages with content updates."""
        current_content = ''
        message_id = None
        role = None
        
        async for event in self.stream_run(thread_id, assistant_id, **options):
            event_type = event['type']
            data = event['data']
            
            if event_type == 'thread.message.created':
                message_id = data.get('id')
                role = data.get('role')
                yield {
                    'content': '',
                    'is_complete': False,
                    'message_id': message_id,
                    'role': role,
                }
            
            if event_type == 'thread.message.delta':
                delta = data.get('delta', {})
                content_delta = delta.get('content', [{}])[0]
                text_value = content_delta.get('text', {}).get('value', '')
                
                if text_value:
                    current_content += text_value
                    yield {
                        'content': text_value,
                        'is_complete': False,
                    }
            
            if event_type == 'thread.message.completed':
                yield {
                    'content': current_content,
                    'is_complete': True,
                    'message_id': message_id,
                    'role': role,
                }
                return
            
            if event_type == 'thread.run.requires_action':
                yield {
                    'content': '[Tool call required]',
                    'is_complete': False,
                }

class SSEStreamingService:
    """Service for SSE streaming to web clients."""
    
    def __init__(self, streaming_service: AssistantStreamingService):
        self.streaming_service = streaming_service
    
    async def stream_to_sse(
        self,
        thread_id: str,
        assistant_id: str,
        **options
    ) -> AsyncGenerator[str, None]:
        """Generate SSE-formatted stream."""
        async for data in self.streaming_service.stream_run_with_messages(
            thread_id, assistant_id, **options
        ):
            event = {
                'type': 'message_delta' if not data['is_complete'] else 'message_complete',
                'data': data,
            }
            yield f"data: {json.dumps(event)}\n\n"
        
        yield f"data: {json.dumps({'type': 'stream_end'})}\n\n"
```

## Complete Assistant Service

### Full Implementation

```typescript
// services/assistantComplete.ts - Complete Assistant service
import OpenAI from 'openai';
import { AssistantService } from './assistantService';
import { ThreadService } from './threadService';
import { RunService } from './runService';
import { processToolCalls, getToolDefinitions, ToolHandler } from './toolHandler';
import { AssistantStreamingService } from './streamingService';

interface AssistantSession {
  assistantId: string;
  threadId: string;
  createdAt: Date;
  lastActivityAt: Date;
}

interface ConversationResult {
  message: string;
  messages: any[];
  toolsUsed: string[];
  usage: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
}

export class AssistantManager {
  private client: OpenAI;
  private assistantService: AssistantService;
  private threadService: ThreadService;
  private runService: RunService;
  private streamingService: AssistantStreamingService;
  private toolHandlers: Record<string, ToolHandler>;
  private sessions: Map<string, AssistantSession> = new Map();
  
  constructor(client: OpenAI, toolHandlers: Record<string, ToolHandler> = {}) {
    this.client = client;
    this.assistantService = new AssistantService(client);
    this.threadService = new ThreadService(client);
    this.runService = new RunService(client);
    this.streamingService = new AssistantStreamingService(client);
    this.toolHandlers = toolHandlers;
  }
  
  async createAssistant(config: {
    name: string;
    instructions: string;
    model?: string;
    description?: string;
    tools?: any[];
  }): Promise<string> {
    const tools = [
      ...(config.tools || []),
      ...getToolDefinitions(),
    ];
    
    return await this.assistantService.createAssistant({
      ...config,
      tools,
    });
  }
  
  async createSession(
    assistantId: string,
    initialMessage?: string,
    metadata?: Record<string, any>
  ): Promise<string> {
    const threadId = await this.threadService.createThread(undefined, metadata);
    
    if (initialMessage) {
      await this.threadService.addMessage(threadId, initialMessage);
    }
    
    const sessionId = `${assistantId}-${threadId}`;
    this.sessions.set(sessionId, {
      assistantId,
      threadId,
      createdAt: new Date(),
      lastActivityAt: new Date(),
    });
    
    return sessionId;
  }
  
  async chat(
    sessionId: string,
    message: string
  ): Promise<ConversationResult> {
    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new Error(`Session not found: ${sessionId}`);
    }
    
    const { assistantId, threadId } = session;
    
    // Add user message
    await this.threadService.addMessage(threadId, message);
    
    // Create and run
    const runId = await this.runService.createRun(threadId, assistantId, {
      tools: getToolDefinitions(),
    });
    
    // Process run with tool handling
    const result = await this.processRun(threadId, runId);
    
    // Update session
    session.lastActivityAt = new Date();
    
    return result;
  }
  
  async *streamChat(
    sessionId: string,
    message: string
  ): AsyncGenerator<string, void, unknown> {
    const session = this.sessions.get(sessionId);
    if (!session) {
      throw new Error(`Session not found: ${sessionId}`);
    }
    
    const { assistantId, threadId } = session;
    
    // Add user message
    await this.threadService.addMessage(threadId, message);
    
    // Stream the response
    for await (const data of this.streamingService.streamRunWithMessages(
      threadId,
      assistantId,
      { tools: getToolDefinitions() }
    )) {
      if (data.content) {
        yield data.content;
      }
    }
    
    // Update session
    session.lastActivityAt = new Date();
  }
  
  private async processRun(
    threadId: string,
    runId: string,
    maxToolIterations: number = 5
  ): Promise<ConversationResult> {
    let iterations = 0;
    let messages: any[] = [];
    const toolsUsed: string[] = [];
    
    while (iterations < maxToolIterations) {
      const run = await this.runService.waitForRun(threadId, runId);
      
      if (run.status === 'completed') {
        messages = run.messages;
        break;
      }
      
      if (run.status === 'requires_action') {
        const runData = await this.runService.getRun(threadId, runId);
        const toolCalls = runData.required_action?.submit_tool_outputs?.tool_calls || [];
        
        // Record tools used
        for (const tc of toolCalls) {
          toolsUsed.push(tc.function.name);
        }
        
        // Execute tools
        const outputs = await processToolCalls(toolCalls);
        
        // Submit outputs
        await this.runService.submitToolOutputs(threadId, runId, toolCalls, outputs);
        
        iterations++;
        continue;
      }
      
      throw new Error(`Run failed: ${run.status}`);
    }
    
    // Get final messages
    const messagesResponse = await this.threadService.getMessages(threadId, {
      limit: 10,
      order: 'desc',
    });
    
    const lastMessage = messagesResponse.data[0];
    const content = this.extractContent(lastMessage.content);
    
    return {
      message: content,
      messages: messagesResponse.data,
      toolsUsed,
      usage: {
        promptTokens: 0, // Would need to track from run
        completionTokens: 0,
        totalTokens: 0,
      },
    };
  }
  
  private extractContent(content: any[]): string {
    if (Array.isArray(content)) {
      return content
        .filter(part => part.type === 'text')
        .map(part => part.text?.value || '')
        .join('\n');
    }
    return String(content);
  }
  
  getSession(sessionId: string): AssistantSession | undefined {
    return this.sessions.get(sessionId);
  }
  
  deleteSession(sessionId: string): void {
    const session = this.sessions.get(sessionId);
    if (session) {
      this.threadService.deleteThread(session.threadId);
      this.sessions.delete(sessionId);
    }
  }
}
```

```python
# services/assistant_complete.py - Complete Assistant service
from openai import OpenAI
from typing import Dict, Any, Optional, AsyncGenerator, List
from services.assistant_service import AssistantService
from services.thread_service import ThreadService
from services.run_service import RunService
from services.streaming_service import AssistantStreamingService
from services.tool_handler import process_tool_calls, get_tool_definitions, TOOL_HANDLERS
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class AssistantSession:
    assistant_id: str
    thread_id: str
    created_at: datetime
    last_activity_at: datetime

@dataclass
class ConversationResult:
    message: str
    messages: List[Dict[str, Any]]
    tools_used: List[str]
    usage: Dict[str, int]

class AssistantManager:
    """Complete assistant management service."""
    
    def __init__(self, api_key: str, tool_handlers: Optional[Dict[str, Any]] = None):
        self.client = OpenAI(api_key=api_key)
        self.assistant_service = AssistantService(self.client)
        self.thread_service = ThreadService(self.client)
        self.run_service = RunService(self.client)
        self.streaming_service = AssistantStreamingService(self.client)
        self.tool_handlers = tool_handlers or {}
        self.sessions: Dict[str, AssistantSession] = {}
    
    def create_assistant(
        self,
        name: str,
        instructions: str,
        model: Optional[str] = None,
        description: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """Create a new assistant with tools."""
        all_tools = (tools or []) + get_tool_definitions()
        
        return self.assistant_service.create_assistant(
            name=name,
            instructions=instructions,
            model=model,
            description=description,
            tools=all_tools,
        )
    
    def create_session(
        self,
        assistant_id: str,
        initial_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create a new conversation session."""
        thread_id = self.thread_service.create_thread(
            messages=None,
            metadata=metadata,
        )
        
        if initial_message:
            self.thread_service.add_message(thread_id, initial_message)
        
        session_id = f"{assistant_id}-{thread_id}"
        self.sessions[session_id] = AssistantSession(
            assistant_id=assistant_id,
            thread_id=thread_id,
            created_at=datetime.now(),
            last_activity_at=datetime.now(),
        )
        
        return session_id
    
    def chat(self, session_id: str, message: str) -> ConversationResult:
        """Send a message and get response."""
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f'Session not found: {session_id}')
        
        assistant_id = session.assistant_id
        thread_id = session.thread_id
        
        # Add user message
        self.thread_service.add_message(thread_id, message)
        
        # Create and run
        run_id = self.run_service.create_run(
            thread_id,
            assistant_id,
            tools=get_tool_definitions(),
        )
        
        # Process run with tool handling
        result = self._process_run(thread_id, run_id)
        
        # Update session
        session.last_activity_at = datetime.now()
        
        return result
    
    async def stream_chat(
        self,
        session_id: str,
        message: str,
    ) -> AsyncGenerator[str, None]:
        """Stream assistant response."""
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f'Session not found: {session_id}')
        
        assistant_id = session.assistant_id
        thread_id = session.thread_id
        
        # Add user message
        self.thread_service.add_message(thread_id, message)
        
        # Stream the response
        async for data in self.streaming_service.stream_run_with_messages(
            thread_id,
            assistant_id,
            tools=get_tool_definitions(),
        ):
            if data['content']:
                yield data['content']
        
        # Update session
        session.last_activity_at = datetime.now()
    
    def _process_run(
        self,
        thread_id: str,
        run_id: str,
        max_tool_iterations: int = 5,
    ) -> ConversationResult:
        """Process run with tool handling."""
        iterations = 0
        tools_used: List[str] = []
        
        while iterations < max_tool_iterations:
            run_result = self.run_service.wait_for_run(thread_id, run_id)
            
            if run_result.status == 'completed':
                break
            
            if run_result.status == 'requires_action':
                run_data = self.run_service.get_run(thread_id, run_id)
                tool_calls = (
                    run_data.required_action.submit_tool_outputs.tool_calls
                    if run_data.required_action
                    else []
                )
                
                # Record tools used
                for tc in tool_calls:
                    tools_used.append(tc.function.name)
                
                # Execute tools
                outputs = process_tool_calls(tool_calls)
                
                # Submit outputs
                self.run_service.submit_tool_outputs(thread_id, run_id, outputs)
                
                iterations += 1
                continue
            
            raise RuntimeError(f'Run failed: {run_result.status}')
        
        # Get final messages
        messages_response = self.thread_service.get_messages(thread_id, limit=10, order='desc')
        last_message = messages_response[0] if messages_response else None
        content = self._extract_content(last_message.content) if last_message else ''
        
        return ConversationResult(
            message=content,
            messages=messages_response,
            tools_used=tools_used,
            usage={'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0},
        )
    
    @staticmethod
    def _extract_content(content: Any) -> str:
        """Extract text from message content."""
        if isinstance(content, list):
            return '\n'.join(
                part.text.value
                for part in content
                if hasattr(part, 'type') and part.type == 'text' and hasattr(part, 'text')
            )
        return str(content)
    
    def get_session(self, session_id: str) -> Optional[AssistantSession]:
        """Get session info."""
        return self.sessions.get(session_id)
    
    def delete_session(self, session_id: str) -> None:
        """Delete a session."""
        session = self.sessions.get(session_id)
        if session:
            self.thread_service.delete_thread(session.thread_id)
            del self.sessions[session_id]
```

## Troubleshooting

### Common Issues

```typescript
// troubleshooting/assistantIssues.ts - Assistants API troubleshooting
const assistantIssueGuides = [
  {
    issue: 'Run Hangs or Times Out',
    symptoms: [
      'Run stuck in "in_progress" status',
      'No response for extended period',
      'Tool calls not completing',
    ],
    causes: [
      'Tool execution taking too long',
      'Infinite loops in code interpreter',
      'Missing tool output submission',
      'Network issues',
    ],
    solutions: [
      'Check tool output submission',
      'Implement timeout for tool execution',
      'Cancel and retry run',
      'Add tool execution logging',
      'Check tool handler implementations',
    ],
  },
  {
    issue: 'Tools Not Called',
    symptoms: [
      'Assistant ignores available tools',
      'Tools listed but not used',
      'Wrong tool called',
    ],
    causes: [
      'Tool definitions unclear',
      'Instructions not guiding tool use',
      'Assistant choosing not to use tools',
    ],
    solutions: [
      'Improve tool descriptions',
      'Add explicit instructions about when to use tools',
      'Include examples in assistant instructions',
      'Check tool parameter definitions',
    ],
  },
  {
    issue: 'Context Truncation',
    symptoms: [
      'Old messages disappearing',
      'Assistant forgetting context',
      'Inconsistent conversation flow',
    ],
    causes: [
      'Context window exceeded',
      'Too many messages in thread',
      'Large file attachments',
    ],
    solutions: [
      'Implement message pruning strategy',
      'Use summarization for long threads',
      'Split conversations into smaller threads',
      'Remove unnecessary attachments',
    ],
  },
  {
    issue: 'Code Interpreter Errors',
    symptoms: [
      'Code execution fails',
      'Wrong results from calculations',
      'Security sandbox violations',
    ],
    causes: [
      'Invalid Python code',
      'Unsupported libraries',
      'Execution timeouts',
      'Memory limits exceeded',
    ],
    solutions: [
      'Validate code before execution',
      'Use supported libraries only',
      'Implement proper error handling',
      'Check code interpreter logs',
    ],
  },
];
```

## References

### Official Documentation

- [Assistants API Overview](https://platform.openai.com/docs/assistants/overview)
- [Assistants API Reference](https://platform.openai.com/docs/api-reference/assistants)
- [Tools](https://platform.openai.com/docs/assistants/tools)
- [Best Practices](https://platform.openai.com/docs/assistants/how-to/create-assistant)

### Additional Resources

- [Assistants Cookbook](https://github.com/openai/openai-cookbook/tree/main/examples/Assistants_api_quickstart)
- [Code Interpreter Guide](https://platform.openai.com/docs/assistants/tools/code-interpreter)
- [File Search Guide](https://platform.openai.com/docs/assistants/tools/file-search)

---

**Tài liệu này là một phần của Cursor Enterprise Framework Generator.**
