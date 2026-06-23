---
title: "Claude API Best Practices"
description: "Best practices cho Claude API - effective prompts, message structuring, tool use, response parsing, cost optimization, streaming, error handling"
tags: ["claude", "best-practices", "api", "anthropic", "llm", "prompts", "optimization", "production"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Claude API Best Practices

## Tổng quan (Overview)

Best practices là những thực hành đã được kiểm chứng trong production environments, giúp developers đạt được kết quả tối ưu với Claude API. Khác với anti-patterns (những cách tiếp cận gây hại), best practices là những guidelines giúp maximize output quality, minimize costs, và ensure reliable performance trong mọi conditions.

Tài liệu này tổng hợp các best practices được đúc kết từ nhiều production deployments, từ simple chatbot applications đến complex enterprise systems với millions of daily requests. Các best practices được tổ chức theo functional areas: prompt design, message structuring, tool use, response parsing, cost optimization, streaming, error handling, và testing.

Việc tuân thủ best practices không chỉ improve immediate results mà còn tạo ra nền tảng vững chắc cho việc scale và maintain hệ thống trong dài hạn. Một system được xây dựng theo best practices sẽ dễ dàng debug, optimize, và extend hơn.

## Mục đích (Purpose)

Mục tiêu chính của tài liệu này bao gồm:

1. **Cung cấp actionable guidelines** - Mỗi best practice đi kèm với practical implementation
2. **Giải thích rationale** - Tại sao một practice được khuyến nghị, backed by evidence và experience
3. **Show code examples** - Production-ready code snippets cho từng practice
4. **Performance optimization** - Cách maximize quality và minimize costs đồng thời

## Prompt Design Best Practices

### 1. Clear và Specific Instructions

#### Nguyên tắc cơ bản

Các instructions trong prompts càng rõ ràng và cụ thể, Claude càng có khả năng follow đúng và cho ra kết quả mong muốn. "Clear" có nghĩa là không ambiguous, không có contradictions. "Specific" có nghĩa là define exactly what, how, và when.

```
┌─────────────────────────────────────────────────────────────────┐
│           PROMPT CLARITY SPECTRUM                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  UNCLEAR ──────────────────────────────────────────── CLEAR     │
│                                                                 │
│  "Analyze this data"    →    "Categorize the sentiment of       │
│                              customer feedback as positive,        │
│                              neutral, or negative. Return a      │
│                              JSON object with 'sentiment' and    │
│                              'confidence' fields."              │
│                                                                 │
│  "Write something"     →    "Write a 3-paragraph summary of     │
│                              the main argument, conclusion,      │
│                              and key evidence from the text."    │
│                                                                 │
│  "Help me"            →     "Extract the names, email           │
│                              addresses, and phone numbers        │
│                              from the text below."              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Ví dụ Implementation

```python
class PromptTemplate:
    """Templates cho clear, specific prompts."""
    
    @staticmethod
    def sentiment_analysis(text: str, context: str = "") -> str:
        """Tạo prompt rõ ràng cho sentiment analysis."""
        
        return f"""Analyze the sentiment of the customer feedback below.

## TASK
Classify the sentiment as exactly one of:
- positive: praise, satisfaction, recommendation
- negative: complaint, dissatisfaction, disappointment  
- neutral: factual statement, question, unclear sentiment

## OUTPUT FORMAT
Return ONLY valid JSON:
{{
  "sentiment": "positive|negative|neutral",
  "confidence": 0.0-1.0,
  "key_phrase": "1-3 words that best captures sentiment"
}}

## CUSTOMER FEEDBACK
{text}

## CONTEXT
{context if context else "No additional context provided."}
""".strip()
    
    @staticmethod
    def code_review(code: str, language: str, focus_areas: list[str]) -> str:
        """Tạo prompt rõ ràng cho code review."""
        
        focus_instruction = "\n".join(
            f"- {area}: review for {area}" 
            for area in focus_areas
        )
        
        return f"""Review this {language} code and provide structured feedback.

## CODE TO REVIEW
```{language}
{code}
```

## REVIEW FOCUS AREAS
{focus_instruction}

## OUTPUT FORMAT
Return ONLY valid JSON:
{{
  "overall_quality": "excellent|good|acceptable|poor",
  "issues": [
    {{
      "severity": "critical|major|minor",
      "location": "file:line or function name",
      "description": "clear description of issue",
      "suggestion": "specific fix recommendation"
    }}
  ],
  "strengths": ["list of positive aspects"],
  "security_concerns": ["any security issues found"],
  "performance_observations": ["performance-related notes"]
}}

## RULES
- Only report actual issues, don't invent problems
- Be specific in all descriptions
- Suggest actionable fixes
- Check for common {language} pitfalls
""".strip()


class PromptValidator:
    """Validate prompts trước khi sử dụng."""
    
    def validate(self, prompt: str) -> dict:
        """Check prompt quality."""
        
        issues = []
        
        # Check for ambiguity
        vague_phrases = ["something", "etc", "and so on", "whatever"]
        for phrase in vague_phrases:
            if phrase in prompt.lower():
                issues.append(f"Found vague phrase: '{phrase}'")
        
        # Check for contradictions
        contradictions = [
            ("always", "never"),
            ("must", "optional"),
            ("required", "optional")
        ]
        
        # Check length
        if len(prompt) < 50:
            issues.append("Prompt may be too short for clarity")
        
        if len(prompt) > 10000:
            issues.append("Prompt very long - consider splitting")
        
        # Check for output format specification
        if "json" not in prompt.lower() and "format" not in prompt.lower():
            issues.append("No output format specified")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "recommendations": self._suggest_improvements(prompt)
        }
    
    def _suggest_improvements(self, prompt: str) -> list[str]:
        """Gợi ý cải thiện prompt."""
        suggestions = []
        
        if not prompt.strip():
            suggestions.append("Add clear task description")
        
        if prompt.isupper():
            suggestions.append("Consider using mixed case for readability")
        
        if prompt.count("!") > 3:
            suggestions.append("Reduce number of exclamation marks")
        
        return suggestions
```

### 2. System Prompt Structure

#### Anatomy của một Effective System Prompt

Một system prompt hiệu quả nên có cấu trúc rõ ràng với các sections sau:

1. **Role/Persona Definition** - Claude là ai, làm gì
2. **Task Description** - Nhiệm vụ cụ thể
3. **Output Format** - Format của response
4. **Constraints/Rules** - Những gì được làm, không được làm
5. **Examples (optional)** - Few-shot examples khi cần

#### Ví dụ System Prompts

```python
# GOOD: Well-structured system prompt
EFFECTIVE_SYSTEM_PROMPT = """You are {company_name}'s customer support AI assistant.

## YOUR ROLE
- Help customers with order inquiries, product questions, and returns
- Provide accurate information about products and services
- Escalate complex issues to human agents when needed

## COMMUNICATION STYLE
- Language: Vietnamese (default) or English based on customer preference
- Tone: Professional, friendly, and empathetic
- Response length: Concise unless customer asks for details

## TASK: Order Status Inquiry
When customer asks about order status:
1. Ask for order number if not provided
2. Look up order in system
3. Provide: status, estimated delivery, tracking link
4. If delayed, apologize and provide new ETA

## OUTPUT FORMAT
For order inquiries, use this format:
```
Order #{order_number}
Status: {status}
{tracking_info if available}
Estimated Delivery: {date}
```

## CONSTRAINTS
- Do NOT process refunds or cancellations (escalate to human)
- Do NOT share internal pricing or competitor information
- Do NOT make promises about delivery times
- Always verify customer identity before sharing order details
- If unsure, say "Tôi sẽ kiểm tra và phản hồi sớm nhất"

## RESPONSE TEMPLATE
Always end with:
- Summary of action taken
- Next steps if any
- Invitation for further questions
"""


# Template builder cho reusable system prompts
class SystemPromptBuilder:
    """Build consistent, well-structured system prompts."""
    
    def __init__(self, role: str, company: str = "our company"):
        self.role = role
        self.company = company
        self.sections = []
    
    def add_role(self, role_description: str) -> "SystemPromptBuilder":
        self.sections.append(f"## ROLE\n{role_description}")
        return self
    
    def add_constraints(self, constraints: list[str]) -> "SystemPromptBuilder":
        constraints_text = "\n".join(f"- {c}" for c in constraints)
        self.sections.append(f"## CONSTRAINTS\n{constraints_text}")
        return self
    
    def add_output_format(
        self, 
        format_type: str, 
        template: str
    ) -> "SystemPromptBuilder":
        self.sections.append(f"## OUTPUT FORMAT ({format_type})\n{template}")
        return self
    
    def add_examples(self, examples: list[dict]) -> "SystemPromptBuilder":
        example_text = "\n\n".join(
            f"Example {i+1}:\nInput: {e['input']}\nOutput: {e['output']}"
            for i, e in enumerate(examples)
        )
        self.sections.append(f"## EXAMPLES\n{example_text}")
        return self
    
    def build(self) -> str:
        """Build final system prompt."""
        header = f"You are {self.role} for {self.company}."
        return header + "\n\n" + "\n\n".join(self.sections)


# Usage
builder = SystemPromptBuilder(
    role="technical support specialist",
    company="TechCorp Vietnam"
)
builder.add_role("Help customers troubleshoot technical issues")
builder.add_constraints([
    "Do not ask for passwords",
    "Do not access customer accounts without verification",
    "Escalate security concerns immediately"
])
builder.add_output_format("JSON", '{"issue": "", "solution": "", "escalate": true/false}')

system_prompt = builder.build()
```

### 3. Few-Shot Examples

#### Khi nào nên sử dụng Few-Shot

Few-shot examples đặc biệt hữu ích khi:

- Task có format/structure requirements phức tạp
- Cần guide Claude vào specific patterns hoặc tones
- Edge cases mà text description không cover đủ
- Domain-specific terminology hoặc conventions

#### Ví dụ Implementation

```python
# GOOD: Few-shot examples cho format guidance
FEWSHOT_SUMMARIZATION = """Summarize the following article.

## STYLE
- 3 sentences maximum
- Start with main finding
- Include key numbers and dates
- No opinions or interpretations

## EXAMPLES

Input: "Scientists at MIT discovered a new method to convert CO2 into 
fuel using sunlight. The process is 40% more efficient than existing 
methods and could be operational within 5 years. The research was 
funded by the Department of Energy and published in Nature."

Output: "MIT scientists developed a new solar-powered method to convert 
CO2 into fuel, achieving 40% better efficiency than current approaches. 
The technology could be ready within 5 years. The research appears 
in Nature (DOE-funded)."

Input: "{article_content}"

Output:"""


# GOOD: Few-shot cho specialized domain
FEWSHOT_MEDICAL = """Extract medical conditions and medications from clinical notes.

## OUTPUT FORMAT
JSON with arrays:
{{
  "conditions": [
    {{"name": "", "status": "active|resolved|family_history", "severity": ""}}
  ],
  "medications": [
    {{"name": "", "dosage": "", "frequency": ""}}
  ]
}}

## EXAMPLES

Input: "Patient presents with Type 2 Diabetes (HbA1c 8.2%), controlled 
with Metformin 500mg twice daily. Family history of hypertension. 
Currently taking Lisinopril 10mg for BP control."

Output:
{{
  "conditions": [
    {{"name": "Type 2 Diabetes", "status": "active", "severity": "moderate"}},
    {{"name": "Hypertension", "status": "family_history", "severity": "unknown"}}
  ],
  "medications": [
    {{"name": "Metformin", "dosage": "500mg", "frequency": "twice daily"}},
    {{"name": "Lisinopril", "dosage": "10mg", "frequency": "once daily"}}
  ]
}}

Input: "{clinical_notes}"

Output:"""
```

## Message Structuring Best Practices

### 1. Conversation Context Management

```python
class ConversationContextManager:
    """
    Manage conversation context efficiently với smart truncation.
    """
    
    def __init__(
        self,
        max_tokens: int = 100000,
        preserve_recent: int = 10,
        summary_threshold: int = 50000
    ):
        self.max_tokens = max_tokens
        self.preserve_recent = preserve_recent  # Messages to always keep
        self.summary_threshold = summary_threshold
        self.messages: list[dict] = []
        self.summary: str = ""
    
    def add_message(self, role: str, content: str) -> None:
        """Add message to conversation."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_context_for_api(self) -> tuple[list[dict], str]:
        """
        Get messages formatted for API call.
        Returns (messages, summary) tuple.
        """
        
        # Calculate current token count
        total_tokens = self._estimate_tokens()
        
        if total_tokens <= self.max_tokens:
            return self._get_all_messages(), self.summary
        
        # Need to truncate
        return self._truncate_and_summarize()
    
    def _get_all_messages(self) -> list[dict]:
        """Get all messages without summary."""
        return [
            {"role": m["role"], "content": m["content"]}
            for m in self.messages
        ]
    
    def _estimate_tokens(self) -> int:
        """Rough token estimation."""
        total = 0
        for msg in self.messages:
            # ~4 chars per token for English, ~2 for Vietnamese
            total += len(msg["content"]) // 3
        return total
    
    def _truncate_and_summarize(self) -> tuple[list[dict], str]:
        """Truncate older messages và add summary."""
        
        if len(self.messages) <= self.preserve_recent:
            return self._get_all_messages(), self.summary
        
        # Keep recent messages
        recent = self.messages[-self.preserve_recent:]
        
        # Summarize older messages
        older = self.messages[:-self.preserve_recent]
        
        if older and not self.summary:
            # Create summary of older conversation
            self.summary = self._create_summary(older)
        
        result = [{"role": "user", "content": f"[Previous conversation summary]\n{self.summary}"}]
        result.extend([{"role": m["role"], "content": m["content"]} for m in recent])
        
        return result, self.summary
    
    def _create_summary(self, messages: list[dict]) -> str:
        """Create summary of older messages."""
        # In production, could use Claude itself to summarize
        topics = set()
        for msg in messages:
            words = msg["content"].lower().split()
            topics.update(words[:20])  # First 20 words
        
        return f"Earlier conversation covered: {', '.join(list(topics)[:15])}"
```

### 2. Multi-Turn Conversation Patterns

```python
class MultiTurnConversation:
    """
    Pattern cho multi-turn conversations với Claude.
    """
    
    def __init__(self, client: Anthropic, system_prompt: str):
        self.client = client
        self.system_prompt = system_prompt
        self.history: list[dict] = []
        self.max_turns = 10
    
    async def send(
        self,
        message: str,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """Send message và return response."""
        
        self.history.append({"role": "user", "content": message})
        
        response = await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            temperature=temperature,
            system=self.system_prompt,
            messages=self.history
        )
        
        assistant_message = response.content[0].text
        self.history.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message
    
    async def send_with_tools(
        self,
        message: str,
        tools: list[dict]
    ) -> str:
        """Send message với tool use."""
        
        self.history.append({"role": "user", "content": message})
        
        response = await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            system=self.system_prompt,
            messages=self.history,
            tools=tools
        )
        
        # Handle tool calls if present
        while response.stop_reason == "tool_use":
            # Process tool calls
            tool_results = await self._execute_tools(response.content)
            
            self.history.append({"role": "assistant", "content": response.content})
            self.history.append({"role": "user", "content": tool_results})
            
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                system=self.system_prompt,
                messages=self.history,
                tools=tools
            )
        
        assistant_message = response.content[0].text
        self.history.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message
    
    def get_history(self) -> list[dict]:
        """Get conversation history."""
        return self.history.copy()
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.history = []
```

## Tool Use Best Practices

### 1. Tool Definition Guidelines

```python
# GOOD: Well-designed tool definitions
TOOL_DEFINITIONS = [
    {
        "name": "search_products",
        "description": """Search product catalog by name, category, or description.
        
Use when:
- Customer asks about product availability
- Customer wants to find specific items
- Customer compares products

Returns: List of matching products with prices and availability.""",
        
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (product name, category, or description)"
                },
                "category": {
                    "type": "string",
                    "enum": ["electronics", "fashion", "home", "beauty"],
                    "description": "Filter by category (optional)"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum results to return",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 50
                },
                "price_range": {
                    "type": "object",
                    "description": "Filter by price range (VND)",
                    "properties": {
                        "min": {"type": "number"},
                        "max": {"type": "number"}
                    }
                }
            },
            "required": ["query"]
        }
    },
    
    {
        "name": "check_order_status",
        "description": """Look up order status by order number.

Use when:
- Customer asks about delivery status
- Customer wants tracking information
- Customer asks about order details

Returns: Order status, tracking number, estimated delivery date.""",
        
        "input_schema": {
            "type": "object",
            "properties": {
                "order_number": {
                    "type": "string",
                    "description": "Order number (format: ORD-XXXXX)"
                },
                "include_history": {
                    "type": "boolean",
                    "description": "Include order status history",
                    "default": False
                }
            },
            "required": ["order_number"]
        }
    }
]


class ToolDefinitionValidator:
    """Validate tool definitions before deployment."""
    
    def validate(self, tool: dict) -> tuple[bool, list[str]]:
        """Validate a tool definition."""
        errors = []
        
        # Check required fields
        if "name" not in tool:
            errors.append("Missing 'name' field")
        elif not tool["name"].replace("_", "").isalnum():
            errors.append("Tool name should be alphanumeric with underscores")
        
        if "description" not in tool:
            errors.append("Missing 'description' field")
        elif len(tool["description"]) < 50:
            errors.append("Description too short - should explain when to use")
        
        if "input_schema" not in tool:
            errors.append("Missing 'input_schema' field")
        else:
            schema = tool["input_schema"]
            if schema.get("type") != "object":
                errors.append("Schema type must be 'object'")
            
            if "properties" not in schema:
                errors.append("Missing 'properties' in schema")
            else:
                for prop_name, prop_def in schema["properties"].items():
                    if "description" not in prop_def:
                        errors.append(f"Property '{prop_name}' missing description")
        
        return len(errors) == 0, errors
```

### 2. Tool Execution Best Practices

```python
class ToolExecutor:
    """
    Robust tool executor với error handling và logging.
    """
    
    def __init__(self, client: Anthropic):
        self.client = client
        self.tools = []
        self.handlers: dict[str, callable] = {}
        self.execution_log: list[dict] = []
    
    def register_tool(
        self, 
        definition: dict, 
        handler: callable
    ) -> None:
        """Register a tool với its handler."""
        self.tools.append(definition)
        self.handlers[definition["name"]] = handler
    
    async def execute_tool(
        self,
        tool_name: str,
        tool_input: dict,
        timeout: float = 30.0
    ) -> dict:
        """Execute a tool với timeout và error handling."""
        
        start_time = time.time()
        
        self.execution_log.append({
            "tool": tool_name,
            "input": tool_input,
            "start_time": start_time
        })
        
        try:
            if tool_name not in self.handlers:
                result = {
                    "success": False,
                    "error": f"Tool '{tool_name}' not found",
                    "error_code": "TOOL_NOT_FOUND"
                }
            else:
                # Execute with timeout
                result = await asyncio.wait_for(
                    self.handlers[tool_name](tool_input),
                    timeout=timeout
                )
                result = {"success": True, "data": result}
                
        except asyncio.TimeoutError:
            result = {
                "success": False,
                "error": f"Tool '{tool_name}' timed out after {timeout}s",
                "error_code": "TIMEOUT"
            }
            
        except ValidationError as e:
            result = {
                "success": False,
                "error": f"Invalid input: {str(e)}",
                "error_code": "VALIDATION_ERROR"
            }
            
        except PermissionError as e:
            result = {
                "success": False,
                "error": "Permission denied",
                "error_code": "PERMISSION_ERROR"
            }
            
        except Exception as e:
            result = {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "error_code": "INTERNAL_ERROR"
            }
        
        # Log execution
        elapsed = time.time() - start_time
        self.execution_log[-1].update({
            "result": result,
            "elapsed_ms": elapsed * 1000
        })
        
        return result
    
    async def execute_tools_parallel(
        self,
        tool_calls: list[dict]
    ) -> list[dict]:
        """Execute multiple independent tools in parallel."""
        
        tasks = [
            self.execute_tool(call["name"], call["input"])
            for call in tool_calls
        ]
        
        return await asyncio.gather(*tasks)
```

## Response Parsing Best Practices

### 1. Structured Output Parsing

```python
import json
import re
from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class ParseResult:
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    raw_output: Optional[str] = None

class ResponseParser:
    """
    Parse Claude responses với robust error handling.
    """
    
    def parse_json(self, response: str) -> ParseResult:
        """Parse JSON từ response."""
        
        # Try direct JSON parse first
        try:
            data = json.loads(response)
            return ParseResult(success=True, data=data, raw_output=response)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from markdown code block
        json_match = re.search(
            r'```(?:json)?\s*\n?(.*?)\n?```',
            response,
            re.DOTALL
        )
        
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                return ParseResult(success=True, data=data, raw_output=response)
            except json.JSONDecodeError:
                pass
        
        # Try to find JSON-like structure
        json_like_match = re.search(
            r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',
            response,
            re.DOTALL
        )
        
        if json_like_match:
            try:
                data = json.loads(json_like_match.group())
                return ParseResult(success=True, data=data, raw_output=response)
            except json.JSONDecodeError:
                pass
        
        return ParseResult(
            success=False,
            error="Could not parse JSON from response",
            raw_output=response
        )
    
    def parse_structured_text(
        self,
        response: str,
        field_patterns: dict[str, str]
    ) -> ParseResult:
        """
        Parse structured text với regex patterns.
        
        Args:
            response: Claude's text response
            field_patterns: Dict of field_name -> regex pattern
        """
        
        result = {}
        
        for field_name, pattern in field_patterns.items():
            match = re.search(pattern, response, re.IGNORECASE | re.MULTILINE)
            if match:
                result[field_name] = match.group(1).strip()
        
        if not result:
            return ParseResult(
                success=False,
                error="Could not extract fields from response",
                raw_output=response
            )
        
        return ParseResult(success=True, data=result, raw_output=response)
    
    def parse_key_value(self, response: str) -> ParseResult:
        """Parse key-value format responses."""
        
        lines = response.strip().split('\n')
        result = {}
        
        for line in lines:
            # Match "Key: Value" or "Key = Value" patterns
            match = re.match(r'^[\-\*]?\s*([^:=]+)[:=\-]\s*(.+)$', line.strip())
            if match:
                key = match.group(1).strip().lower().replace(' ', '_')
                value = match.group(2).strip()
                result[key] = value
        
        if not result:
            return ParseResult(
                success=False,
                error="Could not parse key-value format",
                raw_output=response
            )
        
        return ParseResult(success=True, data=result, raw_output=response)


class RobustJSONGenerator:
    """
    Ensure Claude generates valid JSON bằng cách prompt engineering.
    """
    
    @staticmethod
    def build_json_prompt(
        schema: dict,
        task_description: str,
        examples: list[dict] | None = None
    ) -> str:
        """Build prompt that encourages valid JSON output."""
        
        schema_str = json.dumps(schema, indent=2)
        
        example_section = ""
        if examples:
            example_section = "\n\n## EXAMPLES\n" + "\n".join(
                f"Input: {e['input']}\nOutput: {json.dumps(e['output'])}"
                for e in examples
            )
        
        return f"""{task_description}

## REQUIRED JSON SCHEMA
```json
{schema_str}
```

## OUTPUT RULES
1. Return ONLY valid JSON - no markdown, no explanations, no text outside the JSON
2. All required fields must be present
3. String values must be quoted
4. Numbers must not be quoted
5. Arrays must use square brackets
6. Objects must use curly braces

## VALIDATION CHECKLIST
Before returning, verify:
- [ ] JSON is valid (can be parsed)
- [ ] All required fields present
- [ ] No trailing commas
- [ ] No comments in JSON
- [ ] Proper quoting

{example_section}

## YOUR OUTPUT
""".strip()
```

## Cost Optimization Best Practices

### 1. Token Budgeting

```python
class TokenBudgetManager:
    """
    Track và manage token usage budgets.
    """
    
    def __init__(
        self,
        daily_budget_usd: float = 100.0,
        monthly_budget_usd: float = 2000.0
    ):
        self.daily_budget = daily_budget_usd
        self.monthly_budget = monthly_budget_usd
        self.daily_spent = 0.0
        self.monthly_spent = 0.0
        self.request_count = 0
        self.last_reset = datetime.now()
        
        # Pricing (per million tokens)
        self.pricing = {
            "claude-3-5-haiku-20241022": {"input": 0.25, "output": 1.25},
            "claude-3-5-sonnet-20241022": {"input": 3.0, "output": 15.0},
            "claude-3-opus-20240229": {"input": 15.0, "output": 75.0}
        }
    
    def calculate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calculate cost for a request."""
        
        prices = self.pricing.get(model, self.pricing["claude-3-5-sonnet-20241022"])
        
        input_cost = (input_tokens / 1_000_000) * prices["input"]
        output_cost = (output_tokens / 1_000_000) * prices["output"]
        
        return input_cost + output_cost
    
    def record_request(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> tuple[bool, float]:
        """
        Record a request và check budget.
        Returns (can_proceed, cost).
        """
        
        self._check_and_reset()
        
        cost = self.calculate_cost(model, input_tokens, output_tokens)
        
        # Check budgets
        if self.daily_spent + cost > self.daily_budget:
            return False, cost
        
        if self.monthly_spent + cost > self.monthly_budget:
            return False, cost
        
        # Record
        self.daily_spent += cost
        self.monthly_spent += cost
        self.request_count += 1
        
        return True, cost
    
    def _check_and_reset(self) -> None:
        """Reset daily counters if needed."""
        now = datetime.now()
        
        if now.date() > self.last_reset.date():
            self.daily_spent = 0.0
            self.last_reset = now
        
        if now.month != self.last_reset.month:
            self.monthly_spent = 0.0
            self.last_reset = now
    
    def get_remaining_budget(self) -> dict:
        """Get remaining budget information."""
        self._check_and_reset()
        
        return {
            "daily": {
                "spent": self.daily_spent,
                "remaining": self.daily_budget - self.daily_spent,
                "budget": self.daily_budget
            },
            "monthly": {
                "spent": self.monthly_spent,
                "remaining": self.monthly_budget - self.monthly_spent,
                "budget": self.monthly_budget
            },
            "request_count": self.request_count
        }
```

### 2. Model Selection Strategy

```python
class ModelRouter:
    """
    Route requests to appropriate models based on task complexity.
    """
    
    def __init__(self, client: Anthropic):
        self.client = client
    
    def select_model(
        self,
        task_type: str,
        input_tokens_estimate: int,
        requires_high_quality: bool = False
    ) -> str:
        """
        Select optimal model based on task characteristics.
        """
        
        # High-quality requirement overrides cost considerations
        if requires_high_quality:
            return "claude-3-opus-20240229"
        
        # Estimate cost with different models
        haiku_cost = self._estimate_cost("claude-3-5-haiku-20241022", input_tokens_estimate)
        sonnet_cost = self._estimate_cost("claude-3-5-sonnet-20241022", input_tokens_estimate)
        opus_cost = self._estimate_cost("claude-3-opus-20240229", input_tokens_estimate)
        
        # Route based on task type
        if task_type in ["classification", "sentiment", "simple_extraction"]:
            return "claude-3-5-haiku-20241022"
        
        if task_type in ["code_generation", "summarization", "translation", "general_qa"]:
            return "claude-3-5-sonnet-20241022"
        
        if task_type in ["complex_reasoning", "research", "strategic_analysis"]:
            return "claude-3-opus-20240229"
        
        # Default to Sonnet
        return "claude-3-5-sonnet-20241022"
    
    def _estimate_cost(self, model: str, input_tokens: int, output_tokens: int = 500) -> float:
        """Estimate cost for model."""
        
        pricing = {
            "claude-3-5-haiku-20241022": (0.25, 1.25),
            "claude-3-5-sonnet-20241022": (3.0, 15.0),
            "claude-3-opus-20240229": (15.0, 75.0)
        }
        
        input_price, output_price = pricing.get(model, (3.0, 15.0))
        
        return (input_tokens / 1_000_000) * input_price + (output_tokens / 1_000_000) * output_price
```

## Streaming Best Practices

```python
class StreamingClaudeClient:
    """
    Claude client với streaming support.
    """
    
    def __init__(self, client: Anthropic):
        self.client = client
    
    async def stream_generate(
        self,
        messages: list[dict],
        system: str | None = None,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 2048,
        on_chunk: Callable[[str], None] | None = None,
        on_complete: Callable[[dict], None] | None = None
    ) -> str:
        """
        Generate response với streaming.
        
        Args:
            on_chunk: Callback for each text chunk
            on_complete: Callback when generation complete
        """
        
        request_params = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages
        }
        
        if system:
            request_params["system"] = system
        
        full_response = ""
        
        async with self.client.messages.stream(**request_params) as stream:
            async for event in stream:
                if event.type == "content_block_delta":
                    if event.delta.type == "text_delta":
                        full_response += event.delta.text
                        
                        if on_chunk:
                            on_chunk(event.delta.text)
                
                elif event.type == "message_delta":
                    if on_complete:
                        on_complete({
                            "usage": event.usage,
                            "stop_reason": event.stop_reason
                        })
        
        return full_response


# Usage example
async def stream_chat_example():
    client = Anthropic()
    streaming_client = StreamingClaudeClient(client)
    
    chunks_received = []
    
    def on_chunk(chunk: str):
        chunks_received.append(chunk)
        print(chunk, end="", flush=True)
    
    response = await streaming_client.stream_generate(
        messages=[{"role": "user", "content": "Write a short story"}],
        on_chunk=on_chunk
    )
    
    print(f"\n\nTotal chunks: {len(chunks_received)}")
    print(f"Total length: {len(response)}")
```

## Error Handling Best Practices

```python
class ErrorHandlingPractices:
    """
    Best practices for Claude API error handling.
    """
    
    @staticmethod
    def classify_error(error: Exception) -> dict:
        """Classify error và determine handling strategy."""
        
        error_str = str(error).lower()
        status = getattr(error, "status", None)
        
        if status == 429:
            return {
                "type": "rate_limit",
                "retryable": True,
                "retry_after": getattr(error, "retry_after", 60),
                "message": "Rate limit exceeded"
            }
        
        if status == 401:
            return {
                "type": "auth",
                "retryable": False,
                "message": "Authentication failed - check API key"
            }
        
        if status == 400 and "context" in error_str:
            return {
                "type": "context_length",
                "retryable": False,
                "message": "Request exceeds context window"
            }
        
        if status and 500 <= status < 600:
            return {
                "type": "server_error",
                "retryable": True,
                "retry_after": 5,
                "message": "Anthropic server error"
            }
        
        if "timeout" in error_str:
            return {
                "type": "timeout",
                "retryable": True,
                "retry_after": 10,
                "message": "Request timed out"
            }
        
        return {
            "type": "unknown",
            "retryable": False,
            "message": str(error)
        }
    
    @staticmethod
    async def execute_with_fallback(
        primary_func: callable,
        fallback_func: callable | None = None,
        max_retries: int = 3
    ) -> tuple[str, str]:
        """
        Execute với fallback strategy.
        
        Returns (result, method) where method is 'primary', 'fallback', or 'error'
        """
        
        for attempt in range(max_retries):
            try:
                result = await primary_func()
                return result, "primary"
                
            except Exception as e:
                error_info = ErrorHandlingPractices.classify_error(e)
                
                if not error_info["retryable"]:
                    break
                
                if attempt < max_retries - 1:
                    await asyncio.sleep(error_info["retry_after"])
        
        # Try fallback
        if fallback_func:
            try:
                result = await fallback_func()
                return result, "fallback"
            except:
                pass
        
        return "", "error"
```

## Testing Best Practices

```python
class ClaudeAPITester:
    """
    Testing framework for Claude API integrations.
    """
    
    def __init__(self, client: Anthropic):
        self.client = client
        self.test_results: list[dict] = []
    
    async def test_prompt(
        self,
        test_name: str,
        system_prompt: str,
        test_cases: list[dict]
    ) -> dict:
        """
        Test a prompt across multiple test cases.
        
        Each test_case should have:
        - input: user message
        - expected_format: regex or type to validate
        - expected_keywords: list of keywords that should appear
        - forbidden_keywords: list of keywords that should NOT appear
        """
        
        results = []
        
        for case in test_cases:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": case["input"]}]
            )
            
            text = response.content[0].text
            passed = True
            failures = []
            
            # Check format
            if "expected_format" in case:
                if not re.search(case["expected_format"], text):
                    passed = False
                    failures.append(f"Format mismatch: expected {case['expected_format']}")
            
            # Check expected keywords
            if "expected_keywords" in case:
                for keyword in case["expected_keywords"]:
                    if keyword.lower() not in text.lower():
                        passed = False
                        failures.append(f"Missing keyword: {keyword}")
            
            # Check forbidden keywords
            if "forbidden_keywords" in case:
                for keyword in case["forbidden_keywords"]:
                    if keyword.lower() in text.lower():
                        passed = False
                        failures.append(f"Forbidden keyword found: {keyword}")
            
            results.append({
                "input": case["input"],
                "output": text,
                "passed": passed,
                "failures": failures
            })
        
        test_result = {
            "test_name": test_name,
            "total": len(results),
            "passed": sum(1 for r in results if r["passed"]),
            "results": results
        }
        
        self.test_results.append(test_result)
        return test_result
    
    def generate_report(self) -> str:
        """Generate test report."""
        
        total_tests = sum(r["total"] for r in self.test_results)
        total_passed = sum(r["passed"] for r in self.test_results)
        
        report = f"""# Claude API Test Report

## Summary
- Total test suites: {len(self.test_results)}
- Total test cases: {total_tests}
- Passed: {total_passed} ({total_passed/total_tests*100:.1f}%)
- Failed: {total_tests - total_passed} ({(total_tests-total_passed)/total_tests*100:.1f}%)

"""
        
        for result in self.test_results:
            report += f"## {result['test_name']}\n"
            report += f"- Passed: {result['passed']}/{result['total']}\n"
            
            failed = [r for r in result["results"] if not r["passed"]]
            if failed:
                report += "\n### Failures:\n"
                for f in failed:
                    report += f"- Input: {f['input'][:50]}...\n"
                    for failure in f["failures"]:
                        report += f"  - {failure}\n"
            
            report += "\n"
        
        return report
```

## References

- [Anthropic Best Practices](https://docs.anthropic.com/claude/docs/best-practices)
- [Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Tool Use Best Practices](https://docs.anthropic.com/claude/docs/tool-use-best-practices)
- [API Reference](https://docs.anthropic.com/claude/reference)
