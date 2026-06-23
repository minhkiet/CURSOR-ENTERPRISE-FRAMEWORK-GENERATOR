---
title: "Structured Outputs"
description: "Hướng dẫn Structured Outputs cho Claude API - output schemas, JSON mode, constrained sampling, regex extraction, structured response patterns"
tags: ["claude", "structured-outputs", "json", "schema", "validation", "output-formatting"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Structured Outputs

## Tổng quan (Overview)

Structured Outputs là kỹ thuật yêu cầu Claude trả về dữ liệu theo định dạng cụ thể thay vì free-form text. Trong môi trường enterprise, nơi mà AI outputs thường được sử dụng bởi các hệ thống khác (databases, APIs, dashboards), khả năng nhận được responses có định dạng nhất quán và có thể xác thực được là yếu tố then chốt.

Việc sử dụng Structured Outputs không chỉ giúp parsing responses dễ dàng hơn mà còn cải thiện độ chính xác của model, giảm hallucinations, và enable các downstream automation workflows đáng tin cậy.

Tài liệu này cung cấp hướng dẫn toàn diện về các phương pháp tạo Structured Outputs với Claude, từ basic JSON responses đến advanced constrained sampling techniques.

## Mục đích (Purpose)

Mục tiêu chính của tài liệu này bao gồm:

1. **JSON Mode** - Yêu cầu Claude trả về JSON hợp lệ
2. **Output Schemas** - Định nghĩa và sử dụng schemas để validate outputs
3. **Constrained Sampling** - Giới hạn output space để đảm bảo format
4. **Regex Extraction** - Trích xuất structured data từ text
5. **Production Patterns** - Best practices cho reliable structured outputs

## Khái niệm cốt lõi (Key Concepts)

### 1. Tại sao cần Structured Outputs?

```
┌─────────────────────────────────────────────────────────────────┐
│                   UNSTRUCTURED OUTPUT                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  "The customer John Doe ordered 3 units of Product ABC          │
│   on January 15th, 2024 for a total of $150. The order         │
│   was shipped to 123 Main Street, Hanoi."                       │
│                                                                 │
│  Problems:                                                      │
│  - Parse manually required                                      │
│  - Error-prone extraction                                       │
│  - Inconsistent formats                                         │
│  - Hard to validate                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STRUCTURED OUTPUT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  {                                                              │
│    "customer_name": "John Doe",                                 │
│    "order_date": "2024-01-15",                                 │
│    "items": [                                                   │
│      {"product": "Product ABC", "quantity": 3}                 │
│    ],                                                           │
│    "total_amount": 150.00,                                      │
│    "shipping_address": {                                        │
│      "street": "123 Main Street",                              │
│      "city": "Hanoi"                                           │
│    }                                                            │
│  }                                                              │
│                                                                 │
│  Benefits:                                                      │
│  ✓ Direct programmatic access                                   │
│  ✓ Automatic validation possible                                │
│  ✓ Consistent format                                            │
│  ✓ Easy integration                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Methods for Structured Outputs

| Method | Pros | Cons | Use Case |
|--------|------|------|----------|
| JSON in System Prompt | Simple, flexible | May not always produce valid JSON | General purpose |
| Output Schema | Validated, reliable | More complex setup | Production systems |
| Constrained Sampling | Guarantees format | Limited flexibility | Strict requirements |
| Regex Extraction | Works with any text | Fragile, manual | Quick extraction |
| Few-Shot Examples | Natural, reliable | More tokens | Most cases |

## JSON Mode và Output Schemas

### 1. Basic JSON Output

```python
import anthropic
from typing import Literal

client = anthropic.Anthropic()

# Simple JSON output request
def generate_json_response(prompt: str, schema: dict | None = None) -> dict:
    """Generate JSON response from Claude."""
    
    # Build system prompt with JSON instructions
    system_prompt = """You must respond with ONLY valid JSON.
Do not include any text outside the JSON.
The JSON must match this schema exactly:
"""
    
    if schema:
        system_prompt += f"""
```json
{schema}
```"""
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Parse JSON from response
    import json
    text = response.content[0].text.strip()
    
    # Handle potential markdown code blocks
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    
    return json.loads(text)
```

### 2. Output Schema Definition

```python
from pydantic import BaseModel, Field
from typing import Optional

# Define schema using Pydantic (Python)
class CustomerOrder(BaseModel):
    """Schema cho customer order data."""
    
    order_id: str = Field(..., description="Unique order identifier")
    customer_name: str = Field(..., description="Full name of customer")
    customer_email: str = Field(..., description="Customer email address")
    
    items: list[OrderItem] = Field(..., description="List of ordered items")
    total_amount: float = Field(..., ge=0, description="Total order amount")
    currency: str = Field(default="USD", description="Currency code")
    
    shipping_address: Address = Field(..., description="Shipping address")
    billing_address: Optional[Address] = Field(None, description="Billing address")
    
    order_date: str = Field(..., description="Order date in YYYY-MM-DD format")
    status: Literal["pending", "processing", "shipped", "delivered", "cancelled"]
    priority: Literal["low", "normal", "high"] = "normal"


class OrderItem(BaseModel):
    """Schema cho order item."""
    
    product_id: str
    product_name: str
    quantity: int = Field(..., ge=1)
    unit_price: float = Field(..., ge=0)
    subtotal: float = Field(..., ge=0)


class Address(BaseModel):
    """Schema cho address."""
    
    street: str
    city: str
    state: Optional[str] = None
    postal_code: str
    country: str = Field(default="US")


def schema_to_json_string(schema: type[BaseModel]) -> str:
    """Convert Pydantic schema to JSON schema string."""
    import json
    return json.dumps(schema.model_json_schema(), indent=2)
```

### 3. TypeScript Schema Definition

```typescript
import { z } from 'zod';

// Define schemas using Zod (TypeScript)
export const AddressSchema = z.object({
  street: z.string(),
  city: z.string(),
  state: z.string().optional(),
  postalCode: z.string(),
  country: z.string().default('US'),
});

export const OrderItemSchema = z.object({
  productId: z.string(),
  productName: z.string(),
  quantity: z.number().int().positive(),
  unitPrice: z.number().min(0),
  subtotal: z.number().min(0),
});

export const CustomerOrderSchema = z.object({
  orderId: z.string(),
  customerName: z.string(),
  customerEmail: z.string().email(),
  items: z.array(OrderItemSchema),
  totalAmount: z.number().min(0),
  currency: z.string().default('USD'),
  shippingAddress: AddressSchema,
  billingAddress: AddressSchema.optional(),
  orderDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  status: z.enum(['pending', 'processing', 'shipped', 'delivered', 'cancelled']),
  priority: z.enum(['low', 'normal', 'high']).default('normal'),
});

export type CustomerOrder = z.infer<typeof CustomerOrderSchema>;
export type Address = z.infer<typeof AddressSchema>;
export type OrderItem = z.infer<typeof OrderItemSchema>;
```

## Prompt Engineering cho Structured Outputs

### 1. JSON Output Prompts

```python
# Best practices for JSON output prompts
JSON_PROMPT_TEMPLATE = """Bạn là một data extraction assistant. Trích xuất thông tin và trả về JSON.

## Output Format
BẮT BUỘC trả về JSON theo schema sau:
```json
{{
  "field_name": "description",
  "nested_object": {{
    "field": "value"
  }}
}}
```

## Rules
1. Chỉ trả về JSON, không thêm text khác
2. Tuân thủ chính xác schema - không thêm hoặc bớt fields
3. Sử dụng null cho missing optional fields
4. Dùng array [] cho empty lists
5. Sử dụng appropriate types (string, number, boolean)

## Input
{input_text}

## JSON Output:"""


def create_json_extraction_prompt(
    input_text: str,
    schema_description: str,
    field_requirements: dict[str, str]
) -> str:
    """Create optimized prompt for JSON extraction."""
    
    schema_section = "# Schema\n```json\n{\n"
    for field, desc in field_requirements.items():
        schema_section += f'  "{field}": "{desc}",\n'
    schema_section += "}\n```\n"
    
    return f"""Extract information from the input and return as JSON.

{schema_section}

# Rules
- Return ONLY valid JSON, no additional text
- Follow schema exactly, no extra fields
- Use null for missing optional fields
- Use arrays for multiple values

# Input
{input_text}

# JSON Output:"""
```

### 2. Few-Shot Examples for Structure

```python
FEWSHOT_EXTRACTION_PROMPT = """Extract order information from text and return as JSON.

## Schema
```json
{{
  "customer": {{
    "name": "Customer full name",
    "email": "Customer email"
  }},
  "order_date": "Date in YYYY-MM-DD format",
  "items": [
    {{
      "name": "Product name",
      "quantity": "Number of items",
      "price": "Price per unit"
    }}
  ],
  "total": "Total amount as number"
}}
```

## Examples

Example 1:
Input: "Ngày 15/03/2024, ông Nguyễn Văn A (email: nguyenvana@email.com) đặt 2 sản phẩm: Bàn phím (500.000đ) và Chuột (200.000đ). Tổng cộng: 700.000đ"
Output:
```json
{{
  "customer": {{
    "name": "Nguyễn Văn A",
    "email": "nguyenvana@email.com"
  }},
  "order_date": "2024-03-15",
  "items": [
    {{"name": "Bàn phím", "quantity": 1, "price": 500000}},
    {{"name": "Chuột", "quantity": 1, "price": 200000}}
  ],
  "total": 700000
}}
```

Example 2:
Input: "Khách hàng Trần Thị B mua 5 cái áo phông giá 150.000 VNĐ/cái vào ngày 20-04-2024."
Output:
```json
{{
  "customer": {{
    "name": "Trần Thị B",
    "email": null
  }},
  "order_date": "2024-04-20",
  "items": [
    {{"name": "Áo phông", "quantity": 5, "price": 150000}}
  ],
  "total": 750000
}}
```

## Input
{input_text}

## Output:"""
```

### 3. Constrained Output Patterns

```python
# Pattern 1: Enum-based constrained output
ENUM_CONSTRAINT_PROMPT = """Classify the sentiment into exactly ONE category.

Categories: POSITIVE, NEGATIVE, NEUTRAL

Input: {text}

Category:"""

# Pattern 2: Boolean constrained output
BOOLEAN_CONSTRAINT_PROMPT = """Answer the question with YES or NO only.

Question: {question}

Answer:"""

# Pattern 3: Numeric constrained output
NUMERIC_CONSTRAINT_PROMPT = """Extract the exact number mentioned.

Rules:
- Return ONLY a number, no text
- If multiple numbers, return the first one
- If no number found, return null

Text: {text}

Number:"""

# Pattern 4: List constrained output
LIST_CONSTRAINT_PROMPT = """Extract all mentioned dates.

Rules:
- Return as JSON array of strings
- Format: YYYY-MM-DD
- If Vietnamese format, convert appropriately
- If no dates, return empty array []

Text: {text}

Dates:"""
```

## Validation và Error Handling

### 1. Output Validation

```python
from pydantic import ValidationError
from typing import Type
import json

class StructuredOutputValidator:
    """Validate structured outputs against schemas."""
    
    def __init__(self, schema: Type[BaseModel]):
        self.schema = schema
    
    def validate(self, output: str | dict) -> tuple[bool, dict | None, str | None]:
        """Validate output against schema.
        
        Returns: (is_valid, parsed_data, error_message)
        """
        
        # Parse JSON if string
        if isinstance(output, str):
            try:
                # Clean potential markdown
                output = self._clean_json_string(output)
                data = json.loads(output)
            except json.JSONDecodeError as e:
                return False, None, f"Invalid JSON: {e}"
        else:
            data = output
        
        # Validate against schema
        try:
            validated = self.schema.model_validate(data)
            return True, validated.model_dump(), None
        except ValidationError as e:
            return False, None, f"Validation error: {e}"
    
    def _clean_json_string(self, text: str) -> str:
        """Clean JSON string from potential markdown or extra text."""
        
        text = text.strip()
        
        # Remove markdown code blocks
        if text.startswith("```"):
            lines = text.split("\n")
            # Remove first and last line (code block markers)
            text = "\n".join(lines[1:-1])
        
        # Remove any leading/trailing text
        json_start = text.find("{")
        json_end = text.rfind("}") + 1
        
        if json_start >= 0 and json_end > json_start:
            text = text[json_start:json_end]
        
        return text


class RobustJSONParser:
    """Parse JSON with multiple fallback strategies."""
    
    def parse(self, text: str) -> dict | None:
        """Parse JSON with fallback strategies."""
        
        # Strategy 1: Direct parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Strategy 2: Extract from markdown
        text = self._extract_from_markdown(text)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Strategy 3: Extract array/object pattern
        parsed = self._extract_json_pattern(text)
        if parsed:
            return parsed
        
        # Strategy 4: Try to fix common issues
        fixed = self._fix_common_issues(text)
        try:
            return json.loads(fixed)
        except json.JSONDecodeError:
            pass
        
        return None
    
    def _extract_from_markdown(self, text: str) -> str:
        """Extract JSON from markdown code blocks."""
        import re
        
        # Match ```json ... ``` or ``` ... ```
        pattern = r'```(?:json)?\s*([\s\S]*?)```'
        matches = re.findall(pattern, text)
        
        if matches:
            return matches[0].strip()
        
        return text
    
    def _extract_json_pattern(self, text: str) -> dict | None:
        """Extract JSON-like pattern from text."""
        import re
        
        # Find balanced braces
        start = text.find('{')
        if start == -1:
            start = text.find('[')
        
        if start == -1:
            return None
        
        depth = 0
        for i, char in enumerate(text[start:], start):
            if char == '{' or char == '[':
                depth += 1
            elif char == '}' or char == ']':
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i+1])
                    except json.JSONDecodeError:
                        pass
                    break
        
        return None
    
    def _fix_common_issues(self, text: str) -> str:
        """Fix common JSON parsing issues."""
        
        # Remove trailing commas
        text = re.sub(r',(\s*[}\]])', r'\1', text)
        
        # Fix single quotes to double quotes (simple cases)
        text = re.sub(r"'([^']*)'", r'"\1"', text)
        
        # Remove comments
        text = re.sub(r'//.*', '', text)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        
        return text
```

### 2. TypeScript Validation

```typescript
import { z } from 'zod';

export class StructuredOutputValidator<T extends z.ZodSchema> {
  constructor(private schema: T) {}
  
  validate(output: string): {
    success: boolean;
    data?: z.infer<T>;
    error?: string;
  } {
    // Try to parse JSON
    let parsed: unknown;
    try {
      parsed = JSON.parse(output);
    } catch (e) {
      // Try to extract JSON
      const extracted = this.extractJSON(output);
      if (!extracted) {
        return { success: false, error: 'Failed to parse JSON' };
      }
      parsed = extracted;
    }
    
    // Validate against schema
    const result = this.schema.safeParse(parsed);
    
    if (result.success) {
      return { success: true, data: result.data };
    } else {
      return {
        success: false,
        error: `Validation failed: ${result.error.message}`
      };
    }
  }
  
  private extractJSON(text: string): unknown | null {
    // Try markdown code block
    const codeBlockMatch = text.match(/```(?:json)?\s*([\s\S]*?)```/);
    if (codeBlockMatch) {
      try {
        return JSON.parse(codeBlockMatch[1].trim());
      } catch {}
    }
    
    // Try to find JSON object or array
    const jsonMatch = text.match(/(\{[\s\S]*\}|\[[\s\S]*\])/);
    if (jsonMatch) {
      try {
        return JSON.parse(jsonMatch[1]);
      } catch {}
    }
    
    return null;
  }
}

// Usage
const validator = new StructuredOutputValidator(CustomerOrderSchema);
const result = validator.validate(modelResponse);

if (result.success) {
  console.log('Valid order:', result.data);
} else {
  console.error('Validation failed:', result.error);
}
```

## Regex Extraction

### 1. Pattern-Based Extraction

```python
import re
from typing import Any
from dataclasses import dataclass

@dataclass
class ExtractionPattern:
    """Pattern cho regex-based extraction."""
    name: str
    pattern: str
    group: int
    transform: Any = None


class RegexExtractor:
    """Extract structured data using regex patterns."""
    
    PATTERNS = {
        "email": ExtractionPattern(
            name="email",
            pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            group=0
        ),
        "phone_vietnam": ExtractionPattern(
            name="phone",
            pattern=r'(?:0[0-9]{9}|0[0-9]{2}[0-9]{7})',
            group=0,
            transform=lambda x: x.replace('.', '').replace('-', '').replace(' ', '')
        ),
        "date_vietnamese": ExtractionPattern(
            name="date",
            pattern=r'(\d{1,2})[-/](\d{1,2})[-/](\d{4})',
            group=0,
            transform=lambda x: _parse_vietnamese_date(x)
        ),
        "date_iso": ExtractionPattern(
            name="date",
            pattern=r'(\d{4})-(\d{2})-(\d{2})',
            group=0
        ),
        "money_vnd": ExtractionPattern(
            name="money",
            pattern=r'(\d{1,3}(?:[.,]\d{3})*)\s*(?:VNĐ|VND|đ)',
            group=1,
            transform=lambda x: float(x.replace('.', '').replace(',', '.'))
        ),
        "money_usd": ExtractionPattern(
            name="money",
            pattern=r'\$\s*([\d,]+\.?\d*)',
            group=1,
            transform=lambda x: float(x.replace(',', ''))
        ),
        "url": ExtractionPattern(
            name="url",
            pattern=r'https?://[^\s<>"{}|\\^`\[\]]+',
            group=0
        ),
    }
    
    def extract(self, text: str, pattern_name: str) -> list[Any]:
        """Extract data using named pattern."""
        
        if pattern_name not in self.PATTERNS:
            raise ValueError(f"Unknown pattern: {pattern_name}")
        
        pattern = self.PATTERNS[pattern_name]
        matches = re.findall(pattern.pattern, text)
        
        results = []
        for match in matches:
            value = match if isinstance(match, str) else match[pattern.group]
            
            if pattern.transform:
                try:
                    value = pattern.transform(value)
                except Exception:
                    pass
            
            results.append(value)
        
        return results
    
    def extract_multiple(self, text: str, pattern_names: list[str]) -> dict:
        """Extract multiple patterns at once."""
        
        return {
            name: self.extract(text, name)
            for name in pattern_names
        }


def _parse_vietnamese_date(date_str: str) -> str:
    """Convert Vietnamese date format to ISO."""
    parts = re.split(r'[-/]', date_str)
    if len(parts) == 3:
        day, month, year = parts
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    return date_str
```

### 2. Structured Extraction with Claude + Regex

```python
class HybridExtractor:
    """Combine Claude extraction với regex validation."""
    
    def __init__(self, client: anthropic.Anthropic):
        self.client = client
        self.regex_extractor = RegexExtractor()
    
    def extract_with_validation(
        self,
        text: str,
        schema: type[BaseModel],
        required_fields: list[str] | None = None
    ) -> dict:
        """Extract using Claude, validate with regex."""
        
        # Get initial extraction from Claude
        json_response = self._claude_extract(text, schema)
        
        # Validate and enrich with regex
        validated = self._validate_and_enrich(json_response, text)
        
        return validated
    
    def _claude_extract(self, text: str, schema: type[BaseModel]) -> dict:
        """Extract using Claude."""
        
        schema_str = schema_to_json_string(schema)
        
        prompt = f"""Extract data from text and return as JSON.

Schema:
{schema_str}

Text:
{text}

Return only JSON:"""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response
        parser = RobustJSONParser()
        parsed = parser.parse(response.content[0].text)
        
        if not parsed:
            raise ValueError("Failed to parse Claude response")
        
        return parsed
    
    def _validate_and_enrich(
        self,
        data: dict,
        original_text: str
    ) -> dict:
        """Validate extracted data and enrich with regex."""
        
        enriched = data.copy()
        
        # Validate email if present
        if 'email' in enriched and enriched['email']:
            emails = self.regex_extractor.extract(original_text, 'email')
            if enriched['email'] not in emails:
                # Use regex-extracted if Claude version doesn't match
                pass  # Could add logging here
        
        # Extract additional data via regex
        extracted = self.regex_extractor.extract_multiple(
            original_text,
            ['phone_vietnam', 'url']
        )
        
        # Enrich with regex data
        for key, value in extracted.items():
            if key not in enriched or not enriched[key]:
                if value:
                    enriched[key] = value[0] if len(value) == 1 else value
        
        return enriched
```

## Production Patterns

### 1. Structured Response Handler

```python
import asyncio
from dataclasses import dataclass
from typing import Type, Optional
from enum import Enum

class ExtractionStatus(Enum):
    SUCCESS = "success"
    PARSE_ERROR = "parse_error"
    VALIDATION_ERROR = "validation_error"
    PARTIAL = "partial"


@dataclass
class ExtractionResult:
    status: ExtractionStatus
    data: Optional[dict] = None
    error: Optional[str] = None
    warnings: list[str] = None
    metadata: dict = None


class StructuredResponseHandler:
    """Production-grade handler cho structured outputs."""
    
    def __init__(
        self,
        client: anthropic.Anthropic,
        default_model: str = "claude-3-5-sonnet-20241022"
    ):
        self.client = client
        self.default_model = default_model
        self.validator = StructuredOutputValidator
        self.parser = RobustJSONParser()
    
    async def extract(
        self,
        text: str,
        schema: Type[BaseModel],
        prompt_template: str | None = None,
        model: str | None = None,
        max_retries: int = 2
    ) -> ExtractionResult:
        """Extract structured data with retries."""
        
        result = ExtractionResult(
            status=ExtractionStatus.PARSE_ERROR,
            warnings=[],
            metadata={}
        )
        
        for attempt in range(max_retries + 1):
            try:
                # Generate prompt
                if prompt_template:
                    prompt = prompt_template.format(input_text=text)
                else:
                    prompt = self._default_prompt(text, schema)
                
                # Call API
                response = await self._call_api(
                    prompt,
                    model or self.default_model
                )
                
                # Parse response
                parsed = self.parser.parse(response)
                
                if not parsed:
                    result.warnings.append(
                        f"Attempt {attempt + 1}: Failed to parse JSON"
                    )
                    continue
                
                # Validate against schema
                validator = self.validator(schema)
                is_valid, validated, error = validator.validate(parsed)
                
                if is_valid:
                    result.status = ExtractionStatus.SUCCESS
                    result.data = validated
                    return result
                else:
                    result.warnings.append(
                        f"Attempt {attempt + 1}: Validation failed - {error}"
                    )
                    
                    # Try to fix and retry
                    if attempt < max_retries:
                        continue
                    
                    result.status = ExtractionStatus.VALIDATION_ERROR
                    result.error = error
                    result.data = parsed  # Return raw data
                    return result
                    
            except Exception as e:
                result.warnings.append(
                    f"Attempt {attempt + 1}: Exception - {str(e)}"
                )
                if attempt == max_retries:
                    result.error = str(e)
        
        result.status = ExtractionStatus.PARSE_ERROR
        return result
    
    def _default_prompt(self, text: str, schema: Type[BaseModel]) -> str:
        """Generate default extraction prompt."""
        
        schema_str = schema_to_json_string(schema)
        
        return f"""Extract information from the text and return as JSON.

Schema:
{schema_str}

Rules:
- Return ONLY valid JSON, no additional text
- Follow schema exactly
- Use null for missing optional fields

Text:
{text}

JSON:"""
    
    async def _call_api(self, prompt: str, model: str) -> str:
        """Call Claude API."""
        
        response = await self.client.messages.create(
            model=model,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
```

### 2. Batch Structured Extraction

```python
class BatchStructuredExtractor:
    """Extract structured data from multiple texts."""
    
    def __init__(
        self,
        client: anthropic.Anthropic,
        schema: Type[BaseModel],
        batch_size: int = 5
    ):
        self.client = client
        self.schema = schema
        self.batch_size = batch_size
        self.handler = StructuredResponseHandler(client)
    
    async def extract_batch(
        self,
        texts: list[str],
        prompts: list[str] | None = None,
        show_progress: bool = True
    ) -> list[ExtractionResult]:
        """Extract from multiple texts with batching."""
        
        results = []
        
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            batch_prompts = prompts[i:i + self.batch_size] if prompts else None
            
            # Process batch
            batch_results = await asyncio.gather(*[
                self.handler.extract(
                    text,
                    self.schema,
                    prompt_template=bp if batch_prompts else None
                )
                for text, bp in zip(batch, batch_prompts or [None] * len(batch))
            ])
            
            results.extend(batch_results)
            
            if show_progress:
                print(f"Processed {min(i + self.batch_size, len(texts))}/{len(texts)}")
        
        return results
    
    def get_success_rate(self, results: list[ExtractionResult]) -> float:
        """Calculate success rate of extractions."""
        
        if not results:
            return 0.0
        
        successful = sum(
            1 for r in results
            if r.status == ExtractionStatus.SUCCESS
        )
        
        return successful / len(results)
    
    def get_partial_results(
        self,
        results: list[ExtractionResult]
    ) -> list[ExtractionResult]:
        """Get results that had partial data despite errors."""
        
        return [
            r for r in results
            if r.status in [ExtractionStatus.PARTIAL, ExtractionStatus.VALIDATION_ERROR]
            and r.data is not None
        ]
```

## Best Practices

### 1. Prompt Design for Reliability

```python
# RELIABLE prompt structure
RELIABLE_JSON_PROMPT = """Task: Extract information as JSON.

# STRICT RULES (MUST follow):
1. Output ONLY valid JSON, nothing else
2. No markdown, no explanation, no text
3. Match the exact schema provided
4. Use correct data types

# Schema
```json
{schema}
```

# Common Mistakes to AVOID:
- Don't add fields not in schema
- Don't use different field names
- Don't wrap in code blocks
- Don't include units in number fields

# Input Text
{input}

# JSON Output (MUST be valid JSON):"""
```

### 2. Error Recovery Patterns

```python
class ErrorRecovery:
    """Patterns for handling extraction errors."""
    
    @staticmethod
    def try_fallback_schemas(
        text: str,
        schemas: list[Type[BaseModel]],
        handler: StructuredResponseHandler
    ) -> ExtractionResult:
        """Try multiple schemas until one works."""
        
        for schema in schemas:
            result = asyncio.run(
                handler.extract(text, schema)
            )
            
            if result.status == ExtractionStatus.SUCCESS:
                return result
        
        # Return last attempt's result
        return result
    
    @staticmethod
    def extract_partial(
        text: str,
        critical_fields: list[str],
        optional_fields: list[str],
        handler: StructuredResponseHandler
    ) -> dict:
        """Extract only critical fields, make optional nullable."""
        
        # Try full extraction
        full_schema = create_schema(critical_fields + optional_fields)
        result = asyncio.run(handler.extract(text, full_schema))
        
        if result.status == ExtractionStatus.SUCCESS:
            return result.data
        
        # Try with nullable optional fields
        partial_schema = create_schema(critical_fields, optional_fields)
        result = asyncio.run(handler.extract(text, partial_schema))
        
        return result.data or {field: None for field in critical_fields}
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Invalid JSON | Model not following format | Strengthen prompt, use few-shot |
| Wrong schema fields | Ambiguous field names | Add detailed descriptions |
| Type mismatches | Wrong data types | Specify types in schema |
| Truncated JSON | max_tokens too low | Increase max_tokens |
| Extra text | Model adding explanation | Emphasize "JSON only" |

### Debugging Structured Outputs

```python
class StructuredOutputDebugger:
    """Debug structured output issues."""
    
    @staticmethod
    def analyze_parsing_failures(
        responses: list[str],
        errors: list[Exception]
    ) -> dict:
        """Analyze patterns in parsing failures."""
        
        analysis = {
            "total_responses": len(responses),
            "total_errors": len(errors),
            "error_types": {},
            "common_issues": [],
            "suggestions": []
        }
        
        for response, error in zip(responses, errors):
            error_type = type(error).__name__
            analysis["error_types"][error_type] = \
                analysis["error_types"].get(error_type, 0) + 1
            
            # Analyze response patterns
            if response.startswith("```"):
                analysis["suggestions"].append(
                    "Response has markdown - consider stripping"
                )
            
            if len(response) < 10:
                analysis["suggestions"].append(
                    "Very short response - possible truncation"
                )
        
        return analysis
```

## References

- [Anthropic Structured Outputs](https://docs.anthropic.com/claude/docs/structured-outputs)
- [JSON Mode Documentation](https://docs.anthropic.com/claude/reference/json-mode)
- [Output Schema Guide](https://docs.anthropic.com/claude/docs/output-schemas)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Zod Documentation](https://zod.dev/)
