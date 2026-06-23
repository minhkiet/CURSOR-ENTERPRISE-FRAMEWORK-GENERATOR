---
title: "Function Calling Gemini - Tool Use và Function Declarations"
description: "Hướng dẫn toàn diện về Function Calling trong Gemini API, bao gồm cách định nghĩa functions, tool use, parallel/sequential function calling, và patterns cho production deployment"
tags:
  - "gemini"
  - "function-calling"
  - "tool-use"
  - "function-declarations"
  - "parallel-calling"
  - "sequential-calling"
  - "api-integration"
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Function Calling Gemini - Tool Use và Function Declarations

## Tổng Quan (Overview)

Function Calling (còn gọi là Tool Use) là một trong những tính năng mạnh mẽ nhất của Gemini API, cho phép model gọi các external functions hoặc APIs để lấy thông tin, thực hiện actions, hoặc tương tác với các hệ thống bên ngoài. Điều này biến Gemini từ một text generator thành một agent có khả năng thực hiện các tác vụ thực tế.

Khác với việc chỉ generate text, Function Calling cho phép Gemini:

- Truy cập real-time information (weather, stocks, news)
- Tương tác với databases và external APIs
- Thực hiện calculations và computations
- Quản lý files và documents
- Xây dựng multi-step workflows
- Tạo các AI agents có khả năng autonomous action

Trong tài liệu này, chúng ta sẽ khám phá chi tiết cách định nghĩa function declarations, cách handle function calls từ model, patterns cho parallel và sequential calling, và các best practices cho production systems.

## Mục Đích (Purpose)

**1. Hiểu Rõ Function Calling Mechanism**

Cung cấp kiến thức chuyên sâu về cách Gemini xử lý function calls, cách model quyết định khi nào cần gọi function, và cách response format được structured. Hiểu rõ mechanism này giúp developers debug và optimize function calling implementations.

**2. Nắm Vững Declarations và Tool Definitions**

Hướng dẫn chi tiết cách định nghĩa functions với JSON schema, including nested objects, required parameters, và descriptions. Đây là foundation quan trọng vì quality của function declarations直接影响 model understanding và accuracy.

**3. Xây Dựng Robust Tool-Using Systems**

Cung cấp các patterns và architectures thực tế cho việc xây dựng các hệ thống tool-using có thể handle complex workflows, errors, retries, và edge cases trong môi trường production.

## Các Khái Niệm Cốt Lõi (Key Concepts)

### 1. Function Declaration Structure

Function declarations trong Gemini sử dụng JSON Schema format để define function signature và parameters. Đây là cách model hiểu function của bạn và quyết định khi nào để gọi.

```python
# src/tools/function_declarations.py
"""
Function Declaration Helpers và Types
"""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import json


@dataclass
class FunctionParameter:
    """Định nghĩa một parameter cho function."""
    name: str
    type: str  # "string", "number", "boolean", "array", "object"
    description: str
    required: bool = True
    enum: Optional[List[str]] = None
    default: Optional[Any] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    items: Optional["FunctionParameter"] = None  # For array type
    properties: Optional[Dict[str, "FunctionParameter"]] = None  # For object type
    
    def to_schema(self) -> Dict[str, Any]:
        """Convert thành JSON Schema format."""
        schema: Dict[str, Any] = {
            "type": self.type,
            "description": self.description,
        }
        
        if self.enum:
            schema["enum"] = self.enum
        
        if self.default is not None:
            schema["default"] = self.default
        
        if self.minimum is not None:
            schema["minimum"] = self.minimum
        
        if self.maximum is not None:
            schema["maximum"] = self.maximum
        
        if self.type == "array" and self.items:
            schema["items"] = self.items.to_schema()
        
        if self.type == "object" and self.properties:
            schema["properties"] = {
                name: prop.to_schema()
                for name, prop in self.properties.items()
            }
        
        return schema


@dataclass
class FunctionDeclaration:
    """Định nghĩa hoàn chỉnh của một function."""
    name: str
    description: str
    parameters: Dict[str, FunctionParameter] = field(default_factory=dict)
    
    def to_schema(self) -> Dict[str, Any]:
        """Convert thành Gemini function declaration format."""
        required_params = [
            name for name, param in self.parameters.items()
            if param.required
        ]
        
        properties = {
            name: param.to_schema()
            for name, param in self.parameters.items()
        }
        
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required_params if required_params else None,
            },
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FunctionDeclaration":
        """Create từ dictionary (parsed JSON)."""
        params = {}
        for name, param_data in data.get("parameters", {}).get("properties", {}).items():
            params[name] = FunctionParameter(
                name=name,
                type=param_data.get("type", "string"),
                description=param_data.get("description", ""),
                required=name in data.get("parameters", {}).get("required", []),
                enum=param_data.get("enum"),
            )
        
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            parameters=params,
        )


# Builder class cho dễ tạo function declarations
class FunctionDeclarationBuilder:
    """Builder để tạo function declarations dễ dàng hơn."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.parameters: Dict[str, FunctionParameter] = {}
    
    def add_string_param(
        self,
        name: str,
        description: str,
        required: bool = True,
        enum: Optional[List[str]] = None
    ) -> "FunctionDeclarationBuilder":
        """Add a string parameter."""
        self.parameters[name] = FunctionParameter(
            name=name,
            type="string",
            description=description,
            required=required,
            enum=enum,
        )
        return self
    
    def add_number_param(
        self,
        name: str,
        description: str,
        required: bool = True,
        minimum: Optional[float] = None,
        maximum: Optional[float] = None
    ) -> "FunctionDeclarationBuilder":
        """Add a number parameter."""
        self.parameters[name] = FunctionParameter(
            name=name,
            type="number",
            description=description,
            required=required,
            minimum=minimum,
            maximum=maximum,
        )
        return self
    
    def add_boolean_param(
        self,
        name: str,
        description: str,
        required: bool = True,
        default: Optional[bool] = None
    ) -> "FunctionDeclarationBuilder":
        """Add a boolean parameter."""
        self.parameters[name] = FunctionParameter(
            name=name,
            type="boolean",
            description=description,
            required=required,
            default=default,
        )
        return self
    
    def add_array_param(
        self,
        name: str,
        description: str,
        item_type: str,
        required: bool = True
    ) -> "FunctionDeclarationBuilder":
        """Add an array parameter."""
        self.parameters[name] = FunctionParameter(
            name=name,
            type="array",
            description=description,
            required=required,
            items=FunctionParameter(name="item", type=item_type, description=""),
        )
        return self
    
    def add_object_param(
        self,
        name: str,
        description: str,
        properties: Dict[str, FunctionParameter],
        required: bool = True
    ) -> "FunctionDeclarationBuilder":
        """Add an object parameter."""
        self.parameters[name] = FunctionParameter(
            name=name,
            type="object",
            description=description,
            required=required,
            properties=properties,
        )
        return self
    
    def build(self) -> FunctionDeclaration:
        """Build the function declaration."""
        return FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=self.parameters,
        )


# Examples
def create_weather_function() -> FunctionDeclaration:
    """Create weather function declaration."""
    return (
        FunctionDeclarationBuilder(
            name="get_weather",
            description="Lấy thông tin thời tiết hiện tại cho một thành phố."
        )
        .add_string_param(
            name="location",
            description="Tên thành phố cần tra cứu thời tiết (VD: Hà Nội, TP.HCM)",
            required=True
        )
        .add_string_param(
            name="units",
            description="Đơn vị nhiệt độ: 'celsius' hoặc 'fahrenheit'",
            required=False,
            enum=["celsius", "fahrenheit"]
        )
        .build()
    )


def create_database_function() -> FunctionDeclaration:
    """Create database query function declaration."""
    return (
        FunctionDeclarationBuilder(
            name="query_database",
            description="Thực hiện truy vấn SQL để lấy dữ liệu từ database."
        )
        .add_string_param(
            name="query",
            description="Câu lệnh SQL SELECT (chỉ hỗ trợ SELECT, không hỗ trợ INSERT/UPDATE/DELETE)",
            required=True
        )
        .add_number_param(
            name="limit",
            description="Số lượng rows tối đa trả về",
            required=False,
            minimum=1,
            maximum=1000
        )
        .build()
    )


def create_api_function() -> FunctionDeclaration:
    """Create generic API call function declaration."""
    return (
        FunctionDeclarationBuilder(
            name="call_external_api",
            description="Gọi một external API endpoint."
        )
        .add_string_param(
            name="endpoint",
            description="API endpoint URL",
            required=True
        )
        .add_string_param(
            name="method",
            description="HTTP method",
            required=True,
            enum=["GET", "POST", "PUT", "DELETE", "PATCH"]
        )
        .add_object_param(
            name="headers",
            description="HTTP headers",
            properties={
                "Content-Type": FunctionParameter(
                    name="Content-Type",
                    type="string",
                    description="Content type"
                ),
                "Authorization": FunctionParameter(
                    name="Authorization",
                    type="string",
                    description="Authorization header"
                ),
            },
            required=False
        )
        .add_object_param(
            name="body",
            description="Request body (cho POST/PUT/PATCH)",
            properties={},
            required=False
        )
        .build()
    )
```

```typescript
// src/tools/function-declarations.ts
/**
 * Function Declaration Types (TypeScript)
 */

import { FunctionDeclaration, Part } from '@google/generative-ai';

// Type definitions for function declarations
export interface ParameterSchema {
  type: string;
  description?: string;
  enum?: string[];
  default?: any;
  minimum?: number;
  maximum?: number;
  items?: ParameterSchema;
  properties?: Record<string, ParameterSchema>;
}

export interface FunctionDeclarations {
  name: string;
  description: string;
  parameters: {
    type: 'object';
    properties: Record<string, ParameterSchema>;
    required?: string[];
  };
}

// Builder class
export class FunctionDeclarationBuilder {
  private name: string;
  private description: string;
  private parameters: Record<string, ParameterSchema> = {};
  private required: string[] = [];

  constructor(name: string, description: string) {
    this.name = name;
    this.description = description;
  }

  addStringParam(
    name: string,
    description: string,
    required: boolean = true,
    enumValues?: string[]
  ): FunctionDeclarationBuilder {
    this.parameters[name] = {
      type: 'string',
      description,
      enum: enumValues,
    };
    if (required) this.required.push(name);
    return this;
  }

  addNumberParam(
    name: string,
    description: string,
    required: boolean = true,
    min?: number,
    max?: number
  ): FunctionDeclarationBuilder {
    this.parameters[name] = {
      type: 'number',
      description,
      minimum: min,
      maximum: max,
    };
    if (required) this.required.push(name);
    return this;
  }

  addBooleanParam(
    name: string,
    description: string,
    required: boolean = true,
    defaultValue?: boolean
  ): FunctionDeclarationBuilder {
    this.parameters[name] = {
      type: 'boolean',
      description,
      default: defaultValue,
    };
    if (required) this.required.push(name);
    return this;
  }

  addObjectParam(
    name: string,
    description: string,
    properties: Record<string, ParameterSchema>,
    required: boolean = true
  ): FunctionDeclarationBuilder {
    this.parameters[name] = {
      type: 'object',
      description,
      properties,
    };
    if (required) this.required.push(name);
    return this;
  }

  addArrayParam(
    name: string,
    description: string,
    itemType: string,
    required: boolean = true
  ): FunctionDeclarationBuilder {
    this.parameters[name] = {
      type: 'array',
      description,
      items: { type: itemType },
    };
    if (required) this.required.push(name);
    return this;
  }

  build(): FunctionDeclarations {
    return {
      name: this.name,
      description: this.description,
      parameters: {
        type: 'object',
        properties: this.parameters,
        required: this.required.length > 0 ? this.required : undefined,
      },
    };
  }
}

// Example function declarations
export function createWeatherFunction(): FunctionDeclarations {
  return new FunctionDeclarationBuilder(
    'get_weather',
    'Lấy thông tin thời tiết hiện tại cho một thành phố.'
  )
    .addStringParam('location', 'Tên thành phố cần tra cứu thời tiết', true)
    .addStringParam('units', 'Đơn vị nhiệt độ', false, ['celsius', 'fahrenheit'])
    .build();
}

export function createSearchFunction(): FunctionDeclarations {
  return new FunctionDeclarationBuilder(
    'web_search',
    'Tìm kiếm thông tin trên internet.'
  )
    .addStringParam('query', 'Từ khóa tìm kiếm', true)
    .addNumberParam('max_results', 'Số lượng kết quả tối đa', false, 1, 20)
    .build();
}
```

### 2. Tool Configuration và Model Setup

Sau khi định nghĩa functions, cần configure model để sử dụng tools.

```python
# src/tools/tool_config.py
"""
Tool Configuration cho Gemini
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from google.generativeai import GenerativeModel, types
from google.generativeai import GenerativeModel


@dataclass
class ToolConfig:
    """Cấu hình cho tools."""
    function_declarations: List[Dict[str, Any]]
    max_iterations: int = 10
    timeout_seconds: float = 60.0


class ToolEnabledModel:
    """
    Wrapper cho Gemini model với tool support.
    """
    
    def __init__(
        self,
        model: GenerativeModel,
        tools: List[Dict[str, Any]],
        config: Optional[ToolConfig] = None
    ):
        self.model = model
        self.tools = tools
        self.config = config or ToolConfig(
            function_declarations=[t for t in tools if t.get('name')]
        )
        
        # Generate tools config
        self._tools_config = [
            {
                "function_declarations": tools
            }
        ]
    
    def generate_with_tools(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> "types.GenerateContentResponse":
        """
        Generate content với tool support.
        """
        generation_config = {}
        if temperature is not None:
            generation_config["temperature"] = temperature
        if max_tokens is not None:
            generation_config["max_output_tokens"] = max_tokens
        
        return self.model.generate_content(
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
            tools=self._tools_config,
            generation_config=generation_config if generation_config else None,
        )
    
    def start_chat_with_tools(self) -> "types.ChatSession":
        """
        Bắt đầu chat session với tools.
        """
        return self.model.start_chat(
            enable_automatic_function_calling=True,
        )
```

### 3. Function Response Handling

Khi model gọi function, response cần được formatted đúng để model có thể tiếp tục xử lý.

```python
# src/tools/function_handler.py
"""
Function Handler - Execute functions và format responses
"""

from typing import Any, Dict, List, Optional, Callable, Awaitable
from dataclasses import dataclass
from abc import ABC, abstractmethod
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class FunctionCall:
    """Represent a function call request từ model."""
    name: str
    arguments: Dict[str, Any]
    call_id: Optional[str] = None


@dataclass
class FunctionResult:
    """Kết quả từ function execution."""
    name: str
    response: Any
    error: Optional[str] = None
    
    def to_part(self) -> Dict[str, Any]:
        """Convert thành Gemini function response part."""
        if self.error:
            return {
                "function_response": {
                    "name": self.name,
                    "response": {
                        "error": self.error
                    }
                }
            }
        
        return {
            "function_response": {
                "name": self.name,
                "response": self.response if isinstance(self.response, dict) else {"result": self.response}
            }
        }


class BaseFunctionHandler(ABC):
    """Abstract base class cho function handlers."""
    
    @abstractmethod
    async def execute(self, arguments: Dict[str, Any]) -> FunctionResult:
        """
        Execute function với given arguments.
        
        Returns:
            FunctionResult object
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return function name."""
        pass


# Example implementations
class WeatherHandler(BaseFunctionHandler):
    """Handler cho weather function."""
    
    async def execute(self, arguments: Dict[str, Any]) -> FunctionResult:
        location = arguments.get("location", "")
        units = arguments.get("units", "celsius")
        
        # Mock weather API call
        weather_data = {
            "location": location,
            "temperature": 28 if units == "celsius" else 82,
            "condition": "partly_cloudy",
            "humidity": 75,
            "wind_speed": 15,
        }
        
        return FunctionResult(
            name="get_weather",
            response=weather_data
        )
    
    def get_name(self) -> str:
        return "get_weather"


class DatabaseHandler(BaseFunctionHandler):
    """Handler cho database query function."""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    async def execute(self, arguments: Dict[str, Any]) -> FunctionResult:
        query = arguments.get("query", "")
        limit = arguments.get("limit", 100)
        
        try:
            # Validate query is SELECT only
            if not query.strip().upper().startswith("SELECT"):
                return FunctionResult(
                    name="query_database",
                    response={"error": "Only SELECT queries are allowed"},
                    error="Invalid query type"
                )
            
            # Execute query
            # rows = self.db.execute(query, limit=limit)
            
            # Mock response
            return FunctionResult(
                name="query_database",
                response={
                    "rows": [
                        {"id": 1, "name": "Sample 1"},
                        {"id": 2, "name": "Sample 2"},
                    ],
                    "count": 2
                }
            )
        except Exception as e:
            logger.error(f"Database query error: {e}")
            return FunctionResult(
                name="query_database",
                response={"error": str(e)},
                error=str(e)
            )
    
    def get_name(self) -> str:
        return "query_database"


class ToolExecutor:
    """
    Executor để handle function calls từ model.
    """
    
    def __init__(self):
        self.handlers: Dict[str, BaseFunctionHandler] = {}
    
    def register(self, handler: BaseFunctionHandler) -> None:
        """Register a function handler."""
        self.handlers[handler.get_name()] = handler
    
    def register_function(
        self,
        name: str,
        handler: Callable[[Dict[str, Any]], Awaitable[Any]]
    ) -> None:
        """Register a function với lambda handler."""
        self.handlers[name] = LambdaHandler(name, handler)
    
    async def execute(self, function_call: FunctionCall) -> FunctionResult:
        """Execute a function call."""
        name = function_call.name
        
        if name not in self.handlers:
            return FunctionResult(
                name=name,
                response={"error": f"Unknown function: {name}"},
                error=f"Handler not found for function: {name}"
            )
        
        handler = self.handlers[name]
        
        try:
            result = await handler.execute(function_call.arguments)
            return result
        except Exception as e:
            logger.error(f"Error executing function {name}: {e}")
            return FunctionResult(
                name=name,
                response={"error": str(e)},
                error=str(e)
            )
    
    async def execute_batch(
        self,
        function_calls: List[FunctionCall]
    ) -> List[FunctionResult]:
        """Execute multiple function calls."""
        results = []
        for call in function_calls:
            result = await self.execute(call)
            results.append(result)
        return results


class LambdaHandler(BaseFunctionHandler):
    """Handler wrapper cho lambda functions."""
    
    def __init__(
        self,
        name: str,
        handler: Callable[[Dict[str, Any]], Awaitable[Any]]
    ):
        self.name = name
        self.handler = handler
    
    async def execute(self, arguments: Dict[str, Any]) -> FunctionResult:
        try:
            result = await self.handler(arguments)
            return FunctionResult(name=self.name, response=result)
        except Exception as e:
            return FunctionResult(name=self.name, response={"error": str(e)}, error=str(e))
    
    def get_name(self) -> str:
        return self.name


class FunctionCallParser:
    """
    Parser để extract function calls từ model response.
    """
    
    @staticmethod
    def extract_function_calls(response) -> List[FunctionCall]:
        """Extract function calls từ model response."""
        function_calls = []
        
        # Check if response has candidates
        if not response.candidates:
            return function_calls
        
        for candidate in response.candidates:
            # Check for function calls in content
            if not candidate.content or not candidate.content.parts:
                continue
            
            for part in candidate.content.parts:
                # Check if this part is a function call
                if hasattr(part, 'function_call') and part.function_call:
                    fc = part.function_call
                    function_calls.append(FunctionCall(
                        name=fc.name,
                        arguments=dict(fc.args) if hasattr(fc, 'args') else {},
                        call_id=fc.id if hasattr(fc, 'id') else None
                    ))
        
        return function_calls
```

```typescript
// src/tools/function-handler.ts
/**
 * Function Handler (TypeScript)
 */

import { FunctionDeclaration, Part, Content } from '@google/generative-ai';

// Types
export interface FunctionCall {
  name: string;
  args: Record<string, any>;
  callId?: string;
}

export interface FunctionResult {
  name: string;
  response: any;
  error?: string;
}

export interface FunctionHandler {
  execute(args: Record<string, any>): Promise<FunctionResult>;
  getName(): string;
}

// Base handler
export abstract class BaseHandler implements FunctionHandler {
  abstract execute(args: Record<string, any>): Promise<FunctionResult>;
  abstract getName(): string;
}

// Tool Executor
export class ToolExecutor {
  private handlers: Map<string, FunctionHandler> = new Map();

  register(handler: FunctionHandler): void {
    this.handlers.set(handler.getName(), handler);
  }

  registerFunction(
    name: string,
    handler: (args: Record<string, any>) => Promise<any>
  ): void {
    this.handlers.set(name, {
      execute: async (args) => {
        try {
          const result = await handler(args);
          return { name, response: result };
        } catch (error) {
          return { name, response: { error: String(error) }, error: String(error) };
        }
      },
      getName: () => name,
    });
  }

  async execute(functionCall: FunctionCall): Promise<FunctionResult> {
    const handler = this.handlers.get(functionCall.name);

    if (!handler) {
      return {
        name: functionCall.name,
        response: { error: `Unknown function: ${functionCall.name}` },
        error: `Handler not found`,
      };
    }

    try {
      return await handler.execute(functionCall.args);
    } catch (error) {
      return {
        name: functionCall.name,
        response: { error: String(error) },
        error: String(error),
      };
    }
  }

  async executeBatch(functionCalls: FunctionCall[]): Promise<FunctionResult[]> {
    return Promise.all(functionCalls.map(call => this.execute(call)));
  }
}

// Extract function calls from response
export function extractFunctionCalls(response: any): FunctionCall[] {
  const calls: FunctionCall[] = [];

  if (!response.candidates) return calls;

  for (const candidate of response.candidates) {
    if (!candidate.content?.parts) continue;

    for (const part of candidate.content.parts) {
      if (part.functionCall) {
        const fc = part.functionCall;
        calls.push({
          name: fc.name,
          args: fc.args || {},
          callId: fc.id,
        });
      }
    }
  }

  return calls;
}

// Convert function result to Part
export function functionResultToPart(result: FunctionResult): Part {
  return {
    functionResponse: {
      name: result.name,
      response: result.error
        ? { error: result.error }
        : (typeof result.response === 'object' ? result.response : { result: result.response }),
    },
  };
}
```

## Best Practices

### 1. Parallel vs Sequential Function Calling

```python
# src/tools/calling_patterns.py
"""
Patterns cho Parallel và Sequential Function Calling
"""

import asyncio
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class FunctionCallRequest:
    """Request cho một function call."""
    name: str
    arguments: Dict[str, Any]
    priority: int = 1  # 1 = high, 2 = medium, 3 = low


@dataclass
class FunctionCallResponse:
    """Response từ một function call."""
    name: str
    success: bool
    result: Any
    error: Optional[str] = None
    execution_time_ms: float = 0


class ParallelExecutionStrategy:
    """
    Strategy cho parallel function execution.
    Tốt khi các functions không phụ thuộc nhau.
    """
    
    def __init__(self, executor: "ToolExecutor", max_concurrent: int = 10):
        self.executor = executor
        self.max_concurrent = max_concurrent
    
    async def execute_all(
        self,
        requests: List[FunctionCallRequest]
    ) -> List[FunctionCallResponse]:
        """
        Execute all functions in parallel.
        """
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def execute_with_semaphore(req: FunctionCallRequest) -> FunctionCallResponse:
            async with semaphore:
                return await self._execute_single(req)
        
        tasks = [execute_with_semaphore(req) for req in requests]
        return await asyncio.gather(*tasks)
    
    async def _execute_single(
        self,
        request: FunctionCallRequest
    ) -> FunctionCallResponse:
        """Execute a single function call."""
        import time
        start = time.time()
        
        try:
            result = await self.executor.execute(
                FunctionCall(
                    name=request.name,
                    arguments=request.arguments
                )
            )
            
            execution_time = (time.time() - start) * 1000
            
            return FunctionCallResponse(
                name=request.name,
                success=result.error is None,
                result=result.response,
                error=result.error,
                execution_time_ms=execution_time
            )
        except Exception as e:
            return FunctionCallResponse(
                name=request.name,
                success=False,
                result=None,
                error=str(e),
                execution_time_ms=(time.time() - start) * 1000
            )


class SequentialExecutionStrategy:
    """
    Strategy cho sequential function execution.
    Tốt khi functions phụ thuộc nhau.
    """
    
    def __init__(self, executor: "ToolExecutor"):
        self.executor = executor
    
    async def execute_chain(
        self,
        requests: List[FunctionCallRequest],
        stop_on_error: bool = True
    ) -> List[FunctionCallResponse]:
        """
        Execute functions sequentially.
        Kết quả của function trước có thể được truyền cho function sau.
        """
        results: List[FunctionCallResponse] = []
        context: Dict[str, Any] = {}
        
        for request in requests:
            # Inject context from previous results
            resolved_args = self._resolve_arguments(request.arguments, context)
            
            result = await self._execute_single(
                FunctionCall(name=request.name, arguments=resolved_args)
            )
            
            results.append(result)
            context[request.name] = result.result
            
            if stop_on_error and not result.success:
                break
        
        return results
    
    def _resolve_arguments(
        self,
        arguments: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Resolve argument references từ context."""
        resolved = {}
        
        for key, value in arguments.items():
            if isinstance(value, str) and value.startswith("$"):
                # Reference to previous result
                ref = value[1:]
                resolved[key] = context.get(ref, value)
            else:
                resolved[key] = value
        
        return resolved
    
    async def _execute_single(
        self,
        function_call: FunctionCall
    ) -> FunctionCallResponse:
        """Execute a single function call."""
        import time
        start = time.time()
        
        try:
            result = await self.executor.execute(function_call)
            
            return FunctionCallResponse(
                name=function_call.name,
                success=result.error is None,
                result=result.response,
                error=result.error,
                execution_time_ms=(time.time() - start) * 1000
            )
        except Exception as e:
            return FunctionCallResponse(
                name=function_call.name,
                success=False,
                result=None,
                error=str(e),
                execution_time_ms=(time.time() - start) * 1000
            )


class HybridExecutionStrategy:
    """
    Hybrid strategy - kết hợp parallel và sequential.
    Tự động xác định dependencies và execute phù hợp.
    """
    
    def __init__(self, executor: "ToolExecutor", max_concurrent: int = 10):
        self.executor = executor
        self.parallel_strategy = ParallelExecutionStrategy(executor, max_concurrent)
        self.sequential_strategy = SequentialExecutionStrategy(executor)
    
    async def execute(
        self,
        requests: List[FunctionCallRequest]
    ) -> List[FunctionCallResponse]:
        """
        Execute với automatic dependency resolution.
        """
        # Build dependency graph
        dependencies = self._build_dependency_graph(requests)
        
        # Topological sort để determine execution order
        execution_groups = self._topological_sort(requests, dependencies)
        
        # Execute each group
        all_results: List[FunctionCallResponse] = []
        context: Dict[str, Any] = {}
        
        for group in execution_groups:
            if len(group) == 1:
                # Sequential execution cho single items
                req = group[0]
                resolved_args = self._resolve_arguments(req.arguments, context)
                
                result = await self._execute_single(
                    FunctionCall(name=req.name, arguments=resolved_args)
                )
                all_results.append(result)
                context[req.name] = result.result
            else:
                # Parallel execution cho independent items
                parallel_requests = []
                for req in group:
                    resolved_args = self._resolve_arguments(req.arguments, context)
                    parallel_requests.append(
                        FunctionCallRequest(name=req.name, arguments=resolved_args)
                    )
                
                results = await self.parallel_strategy.execute_all(parallel_requests)
                all_results.extend(results)
                
                for result in results:
                    context[result.name] = result.result
        
        return all_results
    
    def _build_dependency_graph(
        self,
        requests: List[FunctionCallRequest]
    ) -> Dict[str, List[str]]:
        """Build dependency graph từ argument references."""
        dependencies: Dict[str, List[str]] = {req.name: [] for req in requests}
        
        for req in requests:
            for _, value in req.arguments.items():
                if isinstance(value, str) and value.startswith("$"):
                    dep_name = value[1:].split(".")[0]
                    if dep_name in dependencies:
                        dependencies[req.name].append(dep_name)
        
        return dependencies
    
    def _topological_sort(
        self,
        requests: List[FunctionCallRequest],
        dependencies: Dict[str, List[str]]
    ) -> List[List[FunctionCallRequest]]:
        """Sort requests into execution groups."""
        request_map = {req.name: req for req in requests}
        in_degree = {name: len(deps) for name, deps in dependencies.items()}
        
        groups: List[List[FunctionCallRequest]] = []
        remaining = set(request_map.keys())
        
        while remaining:
            # Find all items with no dependencies
            ready = [
                name for name in remaining
                if in_degree[name] == 0
            ]
            
            if not ready:
                # Cycle detected - just take first remaining
                ready = [next(iter(remaining))]
            
            groups.append([request_map[name] for name in ready])
            
            for name in ready:
                remaining.remove(name)
                # Update in-degrees
                for other_name, deps in dependencies.items():
                    if name in deps:
                        in_degree[other_name] -= 1
        
        return groups
    
    def _resolve_arguments(
        self,
        arguments: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Resolve argument references từ context."""
        resolved = {}
        
        for key, value in arguments.items():
            if isinstance(value, str) and value.startswith("$"):
                ref = value[1:]
                resolved[key] = self._get_nested_value(context, ref)
            else:
                resolved[key] = value
        
        return resolved
    
    def _get_nested_value(self, obj: Any, path: str) -> Any:
        """Get nested value from object using dot notation."""
        parts = path.split(".")
        current = obj
        
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
        
        return current
    
    async def _execute_single(
        self,
        function_call: FunctionCall
    ) -> FunctionCallResponse:
        """Execute a single function call."""
        import time
        start = time.time()
        
        try:
            result = await self.executor.execute(function_call)
            
            return FunctionCallResponse(
                name=function_call.name,
                success=result.error is None,
                result=result.response,
                error=result.error,
                execution_time_ms=(time.time() - start) * 1000
            )
        except Exception as e:
            return FunctionCallResponse(
                name=function_call.name,
                success=False,
                result=None,
                error=str(e),
                execution_time_ms=(time.time() - start) * 1000
            )
```

### 2. Error Handling và Retry Patterns

```python
# src/tools/error_handling.py
"""
Error Handling cho Function Calling
"""

import asyncio
from typing import Optional, Callable, Type, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class RetryStrategy(Enum):
    """Các chiến lược retry."""
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    LINEAR_BACKOFF = "linear_backoff"
    FIXED_DELAY = "fixed_delay"


@dataclass
class RetryConfig:
    """Cấu hình cho retry logic."""
    max_retries: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    retryable_exceptions: Tuple[Type[Exception], ...] = (
        TimeoutError,
        ConnectionError,
        RuntimeError,
    )


@dataclass
class FunctionError:
    """Structured error information."""
    function_name: str
    error_type: str
    message: str
    retry_count: int
    original_error: Optional[Exception] = None


class RetryableFunctionError(Exception):
    """Exception cho errors có thể retry."""
    
    def __init__(self, error: FunctionError):
        self.error = error
        super().__init__(error.message)


class FunctionCallWithRetry:
    """
    Wrapper cho function calls với retry logic.
    """
    
    def __init__(
        self,
        executor: "ToolExecutor",
        config: Optional[RetryConfig] = None
    ):
        self.executor = executor
        self.config = config or RetryConfig()
    
    async def execute_with_retry(
        self,
        function_call: FunctionCall,
        on_retry: Optional[Callable[[FunctionError], None]] = None
    ) -> FunctionResult:
        """
        Execute function với automatic retry.
        """
        last_error = None
        retry_count = 0
        
        while retry_count <= self.config.max_retries:
            try:
                # Execute function
                result = await self.executor.execute(function_call)
                
                # Check if result indicates an error
                if isinstance(result.response, dict) and "error" in result.response:
                    error = FunctionError(
                        function_name=function_call.name,
                        error_type="ExecutionError",
                        message=result.response["error"],
                        retry_count=retry_count,
                    )
                    
                    if self._should_retry(error):
                        retry_count += 1
                        last_error = error
                        
                        if on_retry:
                            on_retry(error)
                        
                        await self._wait_before_retry(retry_count)
                        continue
                
                return result
                
            except self.config.retryable_exceptions as e:
                error = FunctionError(
                    function_name=function_call.name,
                    error_type=type(e).__name__,
                    message=str(e),
                    retry_count=retry_count,
                    original_error=e,
                )
                
                if retry_count < self.config.max_retries:
                    retry_count += 1
                    last_error = error
                    
                    if on_retry:
                        on_retry(error)
                    
                    await self._wait_before_retry(retry_count)
                else:
                    last_error = error
            except Exception as e:
                # Non-retryable error
                return FunctionResult(
                    name=function_call.name,
                    response={"error": str(e)},
                    error=str(e)
                )
        
        # All retries exhausted
        return FunctionResult(
            name=function_call.name,
            response={
                "error": f"Max retries ({self.config.max_retries}) exhausted",
                "last_error": last_error.message if last_error else None
            },
            error=last_error.message if last_error else "Unknown error"
        )
    
    def _should_retry(self, error: FunctionError) -> bool:
        """Determine if an error should trigger retry."""
        # Don't retry on certain errors
        non_retryable = ["invalid", "unauthorized", "forbidden", "not_found"]
        
        for pattern in non_retryable:
            if pattern in error.message.lower():
                return False
        
        return True
    
    async def _wait_before_retry(self, retry_count: int) -> None:
        """Calculate và wait for appropriate delay."""
        if self.config.strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            delay = min(
                self.config.initial_delay * (self.config.exponential_base ** retry_count),
                self.config.max_delay
            )
        elif self.config.strategy == RetryStrategy.LINEAR_BACKOFF:
            delay = min(
                self.config.initial_delay * retry_count,
                self.config.max_delay
            )
        else:  # FIXED_DELAY
            delay = self.config.initial_delay
        
        await asyncio.sleep(delay)
```

### 3. Validation và Security

```python
# src/tools/validation.py
"""
Validation cho Function Arguments
"""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
import re


@dataclass
class ValidationError:
    """Error từ validation."""
    field: str
    message: str
    value: Any


@dataclass
class ValidationResult:
    """Result của validation."""
    valid: bool
    errors: List[ValidationError] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
    
    @property
    def error_messages(self) -> List[str]:
        return [f"{e.field}: {e.message}" for e in self.errors]


class Validator(ABC):
    """Abstract base class cho validators."""
    
    @abstractmethod
    def validate(self, value: Any) -> Optional[str]:
        """Validate value, return error message if invalid."""
        pass


class StringValidator(Validator):
    """Validator cho string values."""
    
    def __init__(
        self,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        pattern: Optional[str] = None,
        enum: Optional[List[str]] = None
    ):
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = pattern
        self.enum = enum
    
    def validate(self, value: Any) -> Optional[str]:
        if not isinstance(value, str):
            return f"Expected string, got {type(value).__name__}"
        
        if self.min_length and len(value) < self.min_length:
            return f"String too short (min: {self.min_length})"
        
        if self.max_length and len(value) > self.max_length:
            return f"String too long (max: {self.max_length})"
        
        if self.pattern and not re.match(self.pattern, value):
            return f"String doesn't match pattern: {self.pattern}"
        
        if self.enum and value not in self.enum:
            return f"Value must be one of: {', '.join(self.enum)}"
        
        return None


class NumberValidator(Validator):
    """Validator cho numeric values."""
    
    def __init__(
        self,
        minimum: Optional[float] = None,
        maximum: Optional[float] = None,
        integer_only: bool = False
    ):
        self.minimum = minimum
        self.maximum = maximum
        self.integer_only = integer_only
    
    def validate(self, value: Any) -> Optional[str]:
        if self.integer_only and not isinstance(value, int):
            return f"Expected integer, got {type(value).__name__}"
        
        if not isinstance(value, (int, float)):
            return f"Expected number, got {type(value).__name__}"
        
        if self.minimum is not None and value < self.minimum:
            return f"Value too small (min: {self.minimum})"
        
        if self.maximum is not None and value > self.maximum:
            return f"Value too large (max: {self.maximum})"
        
        return None


class FunctionArgumentValidator:
    """
    Validator cho function arguments.
    """
    
    def __init__(self):
        self.field_validators: Dict[str, List[Validator]] = {}
    
    def add_validator(self, field: str, validator: Validator) -> "FunctionArgumentValidator":
        """Add a validator for a field."""
        if field not in self.field_validators:
            self.field_validators[field] = []
        self.field_validators[field].append(validator)
        return self
    
    def validate(self, arguments: Dict[str, Any]) -> ValidationResult:
        """Validate arguments against all validators."""
        errors: List[ValidationError] = []
        
        for field, validators in self.field_validators.items():
            value = arguments.get(field)
            
            for validator in validators:
                error = validator.validate(value)
                if error:
                    errors.append(ValidationError(
                        field=field,
                        message=error,
                        value=value
                    ))
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors
        )


class SecurityValidator:
    """
    Security validators cho function arguments.
    """
    
    # Patterns for potentially dangerous inputs
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|TRUNCATE)\b)",
        r"(--|;|/\*|\*/|@@|@)",
    ]
    
    COMMAND_INJECTION_PATTERNS = [
        r"[;&|`$]",
        r"\b(cat|ls|rm|wget|curl|bash|sh|python)\b",
    ]
    
    @classmethod
    def validate_sql_safety(cls, query: str) -> ValidationResult:
        """Validate SQL query for injection patterns."""
        errors = []
        
        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                errors.append(ValidationError(
                    field="query",
                    message=f"Potentially dangerous pattern detected: {pattern}",
                    value=query
                ))
        
        return ValidationResult(valid=len(errors) == 0, errors=errors)
    
    @classmethod
    def validate_command_safety(cls, command: str) -> ValidationResult:
        """Validate command for injection patterns."""
        errors = []
        
        for pattern in cls.COMMAND_INJECTION_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                errors.append(ValidationError(
                    field="command",
                    message=f"Potentially dangerous pattern detected: {pattern}",
                    value=command
                ))
        
        return ValidationResult(valid=len(errors) == 0, errors=errors)
    
    @classmethod
    def validate_url_safety(cls, url: str) -> ValidationResult:
        """Validate URL for security concerns."""
        errors = []
        
        # Check for allowed protocols
        allowed_protocols = ["http", "https"]
        
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            
            if parsed.scheme.lower() not in allowed_protocols:
                errors.append(ValidationError(
                    field="url",
                    message=f"Only {', '.join(allowed_protocols)} protocols allowed",
                    value=url
                ))
            
            # Check for localhost/private IPs in production
            if any(host in parsed.netloc for host in ["localhost", "127.0.0.1", "0.0.0.0"]):
                errors.append(ValidationError(
                    field="url",
                    message="Access to localhost/private IPs not allowed",
                    value=url
                ))
                
        except Exception as e:
            errors.append(ValidationError(
                field="url",
                message=f"Invalid URL: {str(e)}",
                value=url
            ))
        
        return ValidationResult(valid=len(errors) == 0, errors=errors)
```

## Common Patterns

### 1. Agentic Workflow System

```python
# src/tools/agentic_workflow.py
"""
Agentic Workflow System - Xây dựng AI Agent với Function Calling
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import logging

logger = logging.getLogger(__name__)


class AgentState(Enum):
    """Trạng thái của agent."""
    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING_TOOL = "executing_tool"
    WAITING_RESPONSE = "waiting_response"
    DONE = "done"
    ERROR = "error"


@dataclass
class ToolDefinition:
    """Định nghĩa của một tool cho agent."""
    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Callable


@dataclass
class AgentMessage:
    """Một message trong agent conversation."""
    role: str  # "user", "assistant", "system"
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_results: Optional[List[Dict[str, Any]]] = None


@dataclass
class AgentConfig:
    """Cấu hình cho agent."""
    max_iterations: int = 10
    timeout_seconds: float = 60.0
    verbose: bool = True
    system_prompt: str = "Bạn là một AI assistant thông minh có thể sử dụng tools để hoàn thành tác vụ."


class AgenticWorkflow:
    """
    Agentic workflow system với function calling.
    """
    
    def __init__(
        self,
        model,
        tools: List[ToolDefinition],
        config: Optional[AgentConfig] = None
    ):
        self.model = model
        self.tools = tools
        self.config = config or AgentConfig()
        
        # Setup tool executor
        self.executor = ToolExecutor()
        for tool in tools:
            self.executor.register_function(tool.name, tool.handler)
        
        # Execution strategies
        self.execution_strategy = HybridExecutionStrategy(self.executor)
        
        # State
        self.messages: List[AgentMessage] = []
        self.state = AgentState.IDLE
        self.iteration = 0
    
    async def run(self, user_input: str) -> str:
        """
        Run agent với user input.
        """
        # Add user message
        self.messages.append(AgentMessage(
            role="user",
            content=user_input
        ))
        
        self.state = AgentState.THINKING
        self.iteration = 0
        
        while self.iteration < self.config.max_iterations:
            self.iteration += 1
            
            if self.config.verbose:
                print(f"\n--- Iteration {self.iteration} ---")
                print(f"State: {self.state.value}")
            
            # Generate response
            response = await self._generate_response()
            
            # Check for function calls
            function_calls = FunctionCallParser.extract_function_calls(response)
            
            if not function_calls:
                # No function calls - we're done
                if response.candidates and response.candidates[0].content:
                    final_text = response.candidates[0].content.parts[0].text
                    self.messages.append(AgentMessage(
                        role="assistant",
                        content=final_text
                    ))
                    self.state = AgentState.DONE
                    return final_text
                else:
                    self.state = AgentState.DONE
                    return "Không có response từ model."
            
            # Execute function calls
            if self.config.verbose:
                print(f"Function calls: {[fc.name for fc in function_calls]}")
            
            self.state = AgentState.EXECUTING_TOOL
            
            # Build requests
            requests = [
                FunctionCallRequest(
                    name=fc.name,
                    arguments=fc.arguments
                )
                for fc in function_calls
            ]
            
            # Execute
            results = await self.execution_strategy.execute(requests)
            
            # Format results for model
            function_response_parts = [
                result.to_part() for result in results
            ]
            
            if self.config.verbose:
                print(f"Function results: {[r.name for r in results]}")
                for result in results:
                    print(f"  - {result.name}: {'Success' if result.success else 'Error'}")
            
            # Add tool results to messages
            self.messages.append(AgentMessage(
                role="user",  # Model sees this as continuation
                content="",
                tool_results=[r.to_part() for r in results]
            ))
            
            self.state = AgentState.THINKING
        
        # Max iterations reached
        self.state = AgentState.ERROR
        return "Đã đạt số iteration tối đa. Không thể hoàn thành tác vụ."
    
    async def _generate_response(self):
        """Generate response từ model với current messages."""
        # Build contents for API
        contents = []
        
        for msg in self.messages:
            if msg.role == "system":
                continue
            
            content_parts = []
            
            if msg.content:
                content_parts.append({"text": msg.content})
            
            if msg.tool_results:
                content_parts.extend(msg.tool_results)
            
            if content_parts:
                contents.append({
                    "role": msg.role,
                    "parts": content_parts
                })
        
        # Add system prompt
        system_instruction = self.config.system_prompt
        
        return self.model.generate_content(
            contents=contents,
            tools=[{"function_declarations": self._get_tool_declarations()}],
            system_instruction=system_instruction
        )
    
    def _get_tool_declarations(self) -> List[Dict[str, Any]]:
        """Get tool declarations for model."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
            for tool in self.tools
        ]
    
    def reset(self) -> None:
        """Reset agent state."""
        self.messages = []
        self.state = AgentState.IDLE
        self.iteration = 0
```

### 2. Tool-Enabled Chat Interface

```typescript
// src/tools/tool-chat.ts
/**
 * Tool-Enabled Chat Interface (TypeScript)
 */

import {
  GoogleGenerativeAI,
  FunctionDeclaration,
  Part,
  Content,
  GenerateContentResponse,
} from '@google/generative-ai';
import { ToolExecutor, extractFunctionCalls, functionResultToPart, FunctionCall, FunctionResult } from './function-handler';
import { HybridExecutionStrategy } from './calling-patterns';

interface ChatMessage {
  role: 'user' | 'model';
  content: string;
  functionCalls?: FunctionCall[];
  functionResults?: FunctionResult[];
}

export class ToolEnabledChat {
  private client: GoogleGenerativeAI;
  private model: ReturnType<GoogleGenerativeAI['getGenerativeModel']>;
  private executor: ToolExecutor;
  private strategy: HybridExecutionStrategy;
  private messages: ChatMessage[] = [];
  private maxIterations: number = 10;
  
  constructor(
    apiKey: string,
    modelName: string = 'gemini-2.0-flash',
    tools: FunctionDeclaration[]
  ) {
    this.client = new GoogleGenerativeAI(apiKey);
    this.model = this.client.getGenerativeModel({
      model: modelName,
      tools: [{ functionDeclarations: tools }],
    });
    
    this.executor = new ToolExecutor();
    this.strategy = new HybridExecutionStrategy(this.executor, 10);
  }
  
  registerTool(
    name: string,
    handler: (args: Record<string, any>) => Promise<any>
  ): void {
    this.executor.registerFunction(name, handler);
  }
  
  async sendMessage(
    userMessage: string,
    systemPrompt?: string
  ): Promise<string> {
    // Add user message
    this.messages.push({
      role: 'user',
      content: userMessage,
    });
    
    let iteration = 0;
    
    while (iteration < this.maxIterations) {
      iteration++;
      
      // Build contents
      const contents: Content[] = this.messages.map(msg => ({
        role: msg.role,
        parts: this.buildParts(msg),
      }));
      
      // Generate
      const response = await this.model.generateContent({
        contents,
        systemInstruction: systemPrompt,
      });
      
      // Check for function calls
      const functionCalls = extractFunctionCalls(response);
      
      if (functionCalls.length === 0) {
        // No function calls - we're done
        const text = this.extractText(response);
        
        this.messages.push({
          role: 'model',
          content: text,
        });
        
        return text;
      }
      
      // Execute function calls
      const results = await this.strategy.execute(functionCalls);
      
      // Add function results
      this.messages.push({
        role: 'model',
        content: '',
        functionCalls,
        functionResults: results,
      });
    }
    
    return 'Max iterations reached';
  }
  
  private buildParts(message: ChatMessage): Part[] {
    const parts: Part[] = [];
    
    if (message.content) {
      parts.push({ text: message.content });
    }
    
    if (message.functionResults) {
      for (const result of message.functionResults) {
        parts.push(functionResultToPart(result));
      }
    }
    
    return parts;
  }
  
  private extractText(response: GenerateContentResponse): string {
    if (!response.candidates?.[0]?.content?.parts) {
      return '';
    }
    
    return response.candidates[0].content.parts
      .filter(p => 'text' in p)
      .map(p => (p as any).text)
      .join('');
  }
  
  reset(): void {
    this.messages = [];
  }
  
  getHistory(): ChatMessage[] {
    return [...this.messages];
  }
}
```

## Examples

### 1. Complete Tool-Using System - Python

```python
# src/examples/tool_using_system.py
"""
Complete Tool-Using System Example
"""

import asyncio
from typing import Dict, Any
from google.generativeai import GenerativeModel
from src.config.gemini_config import GeminiConfig, initialize_gemini, create_model
from src.tools.function_declarations import (
    FunctionDeclarationBuilder,
    create_weather_function,
    create_database_function,
)
from src.tools.function_handler import ToolExecutor, LambdaHandler
from src.tools.calling_patterns import HybridExecutionStrategy
from src.tools.validation import FunctionArgumentValidator, StringValidator, NumberValidator
from src.tools.agentic_workflow import AgenticWorkflow, ToolDefinition, AgentConfig


class ToolUsingSystem:
    """
    Complete system với tool calling capabilities.
    """
    
    def __init__(self, config: GeminiConfig):
        # Initialize model
        initialize_gemini(config)
        self.model = create_model(config)
        
        # Initialize executor
        self.executor = ToolExecutor()
        self._register_builtin_tools()
        
        # Initialize agent
        self.agent = self._create_agent()
    
    def _register_builtin_tools(self):
        """Register built-in tools."""
        
        # Weather tool
        async def get_weather(args: Dict[str, Any]) -> Dict[str, Any]:
            location = args.get("location", "")
            units = args.get("units", "celsius")
            
            # Mock weather API
            return {
                "location": location,
                "temperature": 28 if units == "celsius" else 82,
                "condition": "partly_cloudy",
                "humidity": 75,
                "wind_speed": 15,
                "forecast": [
                    {"day": "Tomorrow", "temp": 30, "condition": "sunny"},
                    {"day": "Day after", "temp": 29, "condition": "cloudy"},
                ]
            }
        
        self.executor.register_function("get_weather", get_weather)
        
        # Calculator tool
        async def calculate(args: Dict[str, Any]) -> Dict[str, Any]:
            expression = args.get("expression", "")
            
            try:
                # Safe evaluation (in production, use ast.literal_eval or safer parser)
                result = eval(expression, {"__builtins__": {}}, {})
                return {"result": float(result), "expression": expression}
            except Exception as e:
                return {"error": str(e), "expression": expression}
        
        self.executor.register_function("calculate", calculate)
        
        # Search tool
        async def search(args: Dict[str, Any]) -> Dict[str, Any]:
            query = args.get("query", "")
            max_results = args.get("max_results", 5)
            
            # Mock search results
            return {
                "query": query,
                "results": [
                    {"title": f"Result {i+1} for {query}", "url": f"https://example.com/{i}"}
                    for i in range(min(max_results, 5))
                ]
            }
        
        self.executor.register_function("web_search", search)
        
        # Date/time tool
        async def get_current_time(args: Dict[str, Any]) -> Dict[str, Any]:
            from datetime import datetime
            
            timezone = args.get("timezone", "UTC")
            format_type = args.get("format", "iso")
            
            now = datetime.now()
            
            if format_type == "iso":
                time_str = now.isoformat()
            elif format_type == "readable":
                time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            else:
                time_str = str(now.timestamp())
            
            return {
                "timezone": timezone,
                "datetime": time_str,
                "unix_timestamp": int(now.timestamp())
            }
        
        self.executor.register_function("get_current_time", get_current_time)
    
    def _create_agent(self) -> AgenticWorkflow:
        """Create agentic workflow."""
        
        # Define tools for agent
        tools = [
            ToolDefinition(
                name="get_weather",
                description="Lấy thông tin thời tiết cho một thành phố.",
                parameters={
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Tên thành phố"
                        },
                        "units": {
                            "type": "string",
                            "description": "Đơn vị: celsius hoặc fahrenheit",
                            "enum": ["celsius", "fahrenheit"]
                        }
                    },
                    "required": ["location"]
                },
                handler=lambda args: asyncio.coroutine(
                    lambda: {"location": args.get("location"), "temp": 28}
                )()
            ),
            ToolDefinition(
                name="calculate",
                description="Thực hiện phép tính toán.",
                parameters={
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Biểu thức toán học"
                        }
                    },
                    "required": ["expression"]
                },
                handler=lambda args: {"result": eval(args.get("expression", "0"))}
            ),
            ToolDefinition(
                name="web_search",
                description="Tìm kiếm thông tin trên internet.",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Từ khóa tìm kiếm"
                        },
                        "max_results": {
                            "type": "number",
                            "description": "Số kết quả tối đa"
                        }
                    },
                    "required": ["query"]
                },
                handler=lambda args: {"results": []}
            ),
        ]
        
        config = AgentConfig(
            max_iterations=10,
            verbose=True,
            system_prompt="""Bạn là một AI assistant thông minh có thể sử dụng các tools để trả lời câu hỏi.
            
            Các tools có sẵn:
            - get_weather: Lấy thời tiết
            - calculate: Thực hiện phép tính
            - web_search: Tìm kiếm trên web
            
            Hãy sử dụng tools khi cần thiết để cung cấp câu trả lời chính xác."""
        )
        
        return AgenticWorkflow(self.model, tools, config)
    
    async def chat(self, message: str) -> str:
        """Chat với agent."""
        return await self.agent.run(message)
    
    async def direct_tool_call(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gọi trực tiếp một tool."""
        function_call = FunctionCall(name=tool_name, arguments=arguments)
        result = await self.executor.execute(function_call)
        return result.response


async def main():
    """Example usage."""
    
    # Initialize system
    config = GeminiConfig.from_env()
    system = ToolUsingSystem(config)
    
    # Example 1: Direct tool call
    print("=" * 50)
    print("Example 1: Direct Tool Call")
    print("=" * 50)
    
    result = await system.direct_tool_call(
        "get_weather",
        {"location": "Hà Nội", "units": "celsius"}
    )
    print(f"Weather result: {result}")
    
    # Example 2: Agent chat
    print("\n" + "=" * 50)
    print("Example 2: Agent Chat")
    print("=" * 50)
    
    response = await system.chat(
        "Thời tiết ở Hà Nội như thế nào?"
    )
    print(f"\nFinal response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Complete Tool-Using System - TypeScript

```typescript
// src/examples/tool-using-system.ts
/**
 * Complete Tool-Using System (TypeScript)
 */

import { GoogleGenerativeAI, FunctionDeclaration } from '@google/generative-ai';
import { ToolEnabledChat } from '../tools/tool-chat';

// Tool declarations
const toolDeclarations: FunctionDeclaration[] = [
  {
    name: 'get_weather',
    description: 'Lấy thông tin thời tiết cho một thành phố.',
    parameters: {
      type: 'object',
      properties: {
        location: {
          type: 'string',
          description: 'Tên thành phố',
        },
        units: {
          type: 'string',
          description: 'Đơn vị nhiệt độ',
          enum: ['celsius', 'fahrenheit'],
        },
      },
      required: ['location'],
    },
  },
  {
    name: 'calculate',
    description: 'Thực hiện phép tính toán.',
    parameters: {
      type: 'object',
      properties: {
        expression: {
          type: 'string',
          description: 'Biểu thức toán học',
        },
      },
      required: ['expression'],
    },
  },
  {
    name: 'get_current_time',
    description: 'Lấy thời gian hiện tại.',
    parameters: {
      type: 'object',
      properties: {
        timezone: {
          type: 'string',
          description: 'Múi giờ (VD: Asia/Ho_Chi_Minh)',
        },
        format: {
          type: 'string',
          description: 'Định dạng: iso, readable, unix',
          enum: ['iso', 'readable', 'unix'],
        },
      },
    },
  },
];

// Create chat instance
const chat = new ToolEnabledChat(
  process.env.GEMINI_API_KEY!,
  'gemini-2.0-flash',
  toolDeclarations
);

// Register tool handlers
chat.registerTool('get_weather', async (args) => {
  const { location, units = 'celsius' } = args;
  
  // Mock weather API
  return {
    location,
    temperature: units === 'celsius' ? 28 : 82,
    condition: 'partly cloudy',
    humidity: 75,
  };
});

chat.registerTool('calculate', async (args) => {
  const { expression } = args;
  
  try {
    const result = Function(`"use strict"; return (${expression})`)();
    return { result, expression };
  } catch (error) {
    return { error: String(error) };
  }
});

chat.registerTool('get_current_time', async (args) => {
  const { timezone = 'UTC', format = 'iso' } = args;
  
  const now = new Date();
  
  if (format === 'iso') {
    return { datetime: now.toISOString(), timezone };
  } else if (format === 'readable') {
    return { datetime: now.toLocaleString(), timezone };
  } else {
    return { timestamp: Math.floor(now.getTime() / 1000), timezone };
  }
});

// Main function
async function main() {
  console.log('=== Tool-Using Chat Example ===\n');
  
  // Example 1: Weather query
  console.log('User: What is the weather in Hanoi?');
  const response1 = await chat.sendMessage(
    'What is the weather in Hanoi?',
    'You are a helpful assistant that can use tools to answer questions.'
  );
  console.log(`Assistant: ${response1}\n`);
  
  // Example 2: Calculation
  console.log('User: What is 15 * 23 + 45?');
  const response2 = await chat.sendMessage('What is 15 * 23 + 45?');
  console.log(`Assistant: ${response2}\n`);
  
  // Example 3: Combined query
  console.log('User: What time is it and what is the weather in Saigon?');
  const response3 = await chat.sendMessage(
    'What time is it and what is the weather in Saigon?'
  );
  console.log(`Assistant: ${response3}`);
  
  // Reset for new conversation
  chat.reset();
}

// Run
main().catch(console.error);
```

## Troubleshooting

### Các Vấn Đề Thường Gặp

**1. "Function not called when expected"**

```
Nguyên nhân: Model không nhận diện được khi nào cần gọi function
Giải pháp:
- Cải thiện function description để rõ ràng hơn
- Thêm examples trong system prompt
- Kiểm tra prompt có gợi ý việc sử dụng tools không
- Đảm bảo function parameters có required fields
```

**2. "Invalid arguments for function"**

```
Nguyên nhân: Arguments không match với function signature
Giải pháp:
- Validate arguments trước khi execute
- Kiểm tra parameter types trong declaration
- Thêm default values cho optional parameters
- Implement robust error handling
```

**3. "Function execution timeout"**

```
Nguyên nhân: Function mất quá lâu để execute
Giải pháp:
- Implement timeout cho async functions
- Sử dụng retry với shorter timeout
- Break long operations thành smaller chunks
- Return partial results với error message
```

**4. "Model ignores function results"**

```
Nguyên nhân: Results không được formatted đúng
Giải pháp:
- Verify function response format matches spec
- Kiểm tra function name trong response khớp với call
- Include context in results (not just raw data)
- Consider adding summary of results
```

**5. "Infinite loop of function calls"**

```
Nguyên nhân: Model liên tục gọi function mà không kết thúc
Giải pháp:
- Set max_iterations limit
- Implement stop condition logic
- Design functions để complete tasks, not repeat
- Add explicit "done" indicators in responses
```

## References

### Official Documentation

- [Gemini Function Calling Documentation](https://ai.google.dev/docs/function_calling)
- [Tool Use Guide](https://ai.google.dev/docs/tool_use)
- [Function Declaration Format](https://ai.google.dev/docs/function_declarations)

### Related Documents

- `@gemini-api-setup.md` - Setup và configuration
- `@context-window.md` - Context management khi sử dụng tools
- `@performance.mdc` - Tối ưu hiệu suất cho tool calling
- `@api.mdc` - API design patterns
