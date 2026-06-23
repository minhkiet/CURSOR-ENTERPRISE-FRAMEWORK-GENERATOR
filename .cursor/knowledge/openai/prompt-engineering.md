---
title: Prompt Engineering
description: Hướng dẫn toàn diện về system prompts, few-shot prompting, chain-of-thought, prompt templates và dynamic prompting
tags: [openai, prompt, engineering, engineering, typescript, python]
created: 2026-06-23
version: 1.0.0
framework: cursor-enterprise
---

# Prompt Engineering

## Tổng quan

Prompt engineering là nghệ thuật và khoa học của việc craft prompts hiệu quả để elicit desired responses từ language models. Trong bối cảnh của OpenAI API và các ứng dụng enterprise, prompt engineering đóng vai trò then chốt trong việc tạo ra các AI-powered features đáng tin cậy, accurate, và useful.

Prompt engineering không chỉ đơn thuần là việc viết prompts. Nó bao gồm việc hiểu cách models interpret và process information, cách context và examples ảnh hưởng đến outputs, và cách optimize prompts cho specific use cases. Một well-crafted prompt có thể là sự khác biệt giữa một AI feature hoạt động mediocre và một feature thực sự valuable.

Trong tài liệu này, chúng ta sẽ explore nhiều prompting techniques từ basic đến advanced, bao gồm system prompt design, few-shot learning, chain-of-thought reasoning, prompt chaining, và dynamic prompting systems. Mỗi technique có свои strengths và appropriate use cases, và việc master chúng sẽ giúp bạn build more capable AI applications.

## Mục đích và Phạm vi

Tài liệu này cung cấp comprehensive guide về prompt engineering cho các developers làm việc với OpenAI API. Phạm vi bao gồm từ fundamental concepts như prompt structure và role definition, đến advanced techniques như multi-step reasoning và dynamic prompt generation.

Chúng tôi sẽ cover practical examples cho cả TypeScript và Python, với focus on production-ready implementations. Các topics bao gồm system prompt design patterns, few-shot prompting strategies, chain-of-thought implementation, prompt templating systems, và techniques cho maintaining prompt quality over time.

## Các Khái niệm Chính

### Prompt Anatomy

Một prompt hiệu quả thường bao gồm nhiều components hoạt động cùng nhau để guide model behavior:

**Instruction** là phần quan trọng nhất của prompt, chỉ định rõ ràng model nên làm gì. Instructions nên be clear, specific, và unambiguous. Thay vì "Analyze this", hãy write "Identify the main argument, supporting evidence, and potential weaknesses in this text."

**Context** cung cấp background information giúp model understand the task better. Context có thể bao gồm domain knowledge, relevant facts, hoặc constraints mà model cần consider. Good context reduces ambiguity và improves response quality.

**Examples** (few-shot) cho model thấy desired input-output pairs. Examples are particularly powerful cho tasks where the desired format or approach isn't easily described in words. They help model understand patterns và conventions.

**Input Data** là content mà model sẽ process. Đây có thể là text cần được analyzed, summarized, transformed, hoặc responded to. Input data nên be clearly delineated từ rest of prompt.

**Output Format** chỉ định expected format của response. Format specifications giúp ensure consistency và make outputs easier to parse programmatically. Examples bao gồm JSON, markdown, bulleted lists, hoặc specific structures.

### Role và Persona

Assigning a role to the model là một trong những techniques đơn giản nhưng hiệu quả nhất trong prompt engineering. Role định nghĩa perspective và expertise mà model nên adopt:

**Expert Roles**: Yêu cầu model adopt specific professional perspective. "Bạn là một Senior Software Architect với 15 năm kinh nghiệm" thiết lập expectations về depth và type of analysis.

**Persona Roles**: Định nghĩa personality và communication style. "Bạn là Maya, một customer support agent thân thiện và empathetic" sets tone cho interactions.

**Constraint Roles**: Chỉ định what model không nên do. "Bạn là một fact-checker nghiêm ngặt, không bao giờ speculate" establishes boundaries.

Role definitions work by activating relevant knowledge và patterns trong model's training data. Khi model được told nó là một expert in a field, nó tends to access và apply that expertise more consistently.

### Token Economy

Tokens are the fundamental unit of computation trong LLM processing. Understanding token economics là essential cho prompt optimization:

**Input tokens** được tính phí cho mỗi request, bao gồm system prompt, conversation history, và user input. Longer prompts = higher costs.

**Output tokens** được tính phí riêng, thường cao hơn input tokens. Limiting output với max_tokens là cách control costs.

**Context window** limits total tokens (input + output) mà model có thể process trong một request. Exceeding context = truncated responses.

**Optimization strategies** bao gồm concise writing, removing redundant information, truncating conversation history when needed, và choosing smaller models khi possible.

## System Prompt Design

### Design Patterns

```typescript
// prompts/systemPromptPatterns.ts - System prompt design patterns

// Pattern 1: Comprehensive Role Definition
const comprehensiveRolePrompt = `Bạn là {role_name}, một chuyên gia với {years_experience} năm kinh nghiệm trong lĩnh vực {domain}.

## Chuyên môn
{expertise_list}

## Phong cách làm việc
- {style_attribute_1}
- {style_attribute_2}
- {style_attribute_3}

## Nguyên tắc cốt lõi
1. {principle_1}
2. {principle_2}
3. {principle_3}

## Giới hạn và Boundaries
- Không bao giờ {prohibited_action_1}
- Luôn {required_action_1}
- Trong trường hợp không chắc chắn, {fallback_action}

## Output Format
{output_format_specification}`;

// Pattern 2: Task-Specific Constraints
const taskSpecificPrompt = `Nhiệm vụ: {task_description}

## Mục tiêu
{objective_1}
{objective_2}

## Ràng buộc
- Độ dài response: {length_constraint}
- Định dạng: {format_constraint}
- Ngôn ngữ: {language_constraint}

## Các bước thực hiện
1. {step_1}
2. {step_2}
3. {step_3}

## Ví dụ Input/Output
Input: {example_input}
Output: {example_output}`;

// Pattern 3: Conversation Flow Control
const conversationFlowPrompt = `Bạn đang trò chuyện với người dùng về {topic}.

## Quy tắc hội thoại
- Bắt đầu bằng lời chào thân thiện
- Hỏi clarifying questions nếu cần
- Cung cấp answer hoặc acknowledge uncertainty
- Kết thúc bằng việc offer additional help

## Xử lý Edge Cases
- Nếu câu hỏi không rõ: {unclear_handling}
- Nếu không biết: {unknown_handling}
- Nếu out of scope: {scope_handling}

## Tone và Style
{ tone_description }`;

// Pattern 4: Domain Expert with Tools
const toolEnabledPrompt = `Bạn là một Data Analyst chuyên nghiệp, có quyền truy cập vào các công cụ phân tích dữ liệu.

## Công cụ Available
- **calculate**: Thực hiện các phép tính toán học
- **analyze**: Phân tích dữ liệu và đưa ra insights
- **visualize**: Tạo biểu đồ hoặc đồ thị
- **summarize**: Tóm tắt thông tin từ dữ liệu

## Quy trình làm việc
1. Xác định loại phân tích cần thiết
2. Sử dụng tool appropriate
3. Giải thích kết quả một cách rõ ràng
4. Đề xuất next steps nếu phù hợp

## Output Standards
- Luôn include số liệu cụ thể
- Giải thích ý nghĩa của data
- Đưa ra recommendations dựa trên evidence`;

// Pattern 5: Graduated Complexity
const graduatedComplexityPrompt = `Hãy phân tích văn bản sau theo các mức độ chi tiết:

## Level 1: Tóm tắt (2-3 câu)
Tổng hợp main points một cách ngắn gọn.

## Level 2: Phân tích chi tiết
- Main arguments
- Supporting evidence
- Counterarguments (nếu có)

## Level 3: Đánh giá chuyên sâu
- Strengths của argument
- Weaknesses hoặc gaps
- Overall assessment

---
Văn bản cần phân tích:
{input_text}`;

export class SystemPromptBuilder {
  private role: string = '';
  private expertise: string[] = [];
  private constraints: string[] = [];
  private outputFormat: string = '';
  private tone: string = '';
  private examples: Array<{ input: string; output: string }> = [];
  
  setRole(role: string): this {
    this.role = role;
    return this;
  }
  
  addExpertise(expertise: string): this {
    this.expertise.push(expertise);
    return this;
  }
  
  addConstraint(constraint: string): this {
    this.constraints.push(constraint);
    return this;
  }
  
  setOutputFormat(format: string): this {
    this.outputFormat = format;
    return this;
  }
  
  setTone(tone: string): this {
    this.tone = tone;
    return this;
  }
  
  addExample(input: string, output: string): this {
    this.examples.push({ input, output });
    return this;
  }
  
  build(): string {
    let prompt = '';
    
    if (this.role) {
      prompt += `# Role: ${this.role}\n\n`;
    }
    
    if (this.expertise.length > 0) {
      prompt += `## Expertise\n`;
      prompt += this.expertise.map(e => `- ${e}`).join('\n');
      prompt += '\n\n';
    }
    
    if (this.tone) {
      prompt += `## Tone & Style\n${this.tone}\n\n`;
    }
    
    if (this.constraints.length > 0) {
      prompt += `## Constraints\n`;
      prompt += this.constraints.map(c => `- ${c}`).join('\n');
      prompt += '\n\n';
    }
    
    if (this.outputFormat) {
      prompt += `## Output Format\n${this.outputFormat}\n\n`;
    }
    
    if (this.examples.length > 0) {
      prompt += `## Examples\n`;
      this.examples.forEach((ex, i) => {
        prompt += `Example ${i + 1}:\n`;
        prompt += `Input: ${ex.input}\n`;
        prompt += `Output: ${ex.output}\n\n`;
      });
    }
    
    return prompt.trim();
  }
}
```

```python
# prompts/system_prompt_patterns.py - System prompt design patterns
from typing import List, Optional
from dataclasses import dataclass, field

# Pattern 1: Comprehensive Role Definition
COMPREHENSIVE_ROLE_PROMPT = """Bạn là {role_name}, một chuyên gia với {years_experience} năm kinh nghiệm trong lĩnh vực {domain}.

## Chuyên môn
{expertise_list}

## Phong cách làm việc
- {style_attribute_1}
- {style_attribute_2}
- {style_attribute_3}

## Nguyên tắc cốt lõi
1. {principle_1}
2. {principle_2}
3. {principle_3}

## Giới hạn và Boundaries
- Không bao giờ {prohibited_action_1}
- Luôn {required_action_1}
- Trong trường hợp không chắc chắn, {fallback_action}

## Output Format
{output_format_specification}"""

# Pattern 2: Task-Specific Constraints
TASK_SPECIFIC_PROMPT = """Nhiệm vụ: {task_description}

## Mục tiêu
{objective_1}
{objective_2}

## Ràng buộc
- Độ dài response: {length_constraint}
- Định dạng: {format_constraint}
- Ngôn ngữ: {language_constraint}

## Các bước thực hiện
1. {step_1}
2. {step_2}
3. {step_3}

## Ví dụ Input/Output
Input: {example_input}
Output: {example_output}"""

# Pattern 3: Conversation Flow Control
CONVERSATION_FLOW_PROMPT = """Bạn đang trò chuyện với người dùng về {topic}.

## Quy tắc hội thoại
- Bắt đầu bằng lời chào thân thiện
- Hỏi clarifying questions nếu cần
- Cung cấp answer hoặc acknowledge uncertainty
- Kết thúc bằng việc offer additional help

## Xử lý Edge Cases
- Nếu câu hỏi không rõ: {unclear_handling}
- Nếu không biết: {unknown_handling}
- Nếu out of scope: {scope_handling}

## Tone và Style
{tone_description}"""

@dataclass
class SystemPromptBuilder:
    """Builder for constructing system prompts."""
    role: str = ""
    expertise: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    output_format: str = ""
    tone: str = ""
    examples: List[dict] = field(default_factory=list)
    
    def set_role(self, role: str) -> 'SystemPromptBuilder':
        self.role = role
        return self
    
    def add_expertise(self, expertise: str) -> 'SystemPromptBuilder':
        self.expertise.append(expertise)
        return self
    
    def add_constraint(self, constraint: str) -> 'SystemPromptBuilder':
        self.constraints.append(constraint)
        return self
    
    def set_output_format(self, format_str: str) -> 'SystemPromptBuilder':
        self.output_format = format_str
        return self
    
    def set_tone(self, tone: str) -> 'SystemPromptBuilder':
        self.tone = tone
        return self
    
    def add_example(self, input_text: str, output_text: str) -> 'SystemPromptBuilder':
        self.examples.append({'input': input_text, 'output': output_text})
        return self
    
    def build(self) -> str:
        parts = []
        
        if self.role:
            parts.append(f"# Role: {self.role}\n")
        
        if self.expertise:
            parts.append("## Expertise\n")
            parts.extend(f"- {e}" for e in self.expertise)
            parts.append("\n")
        
        if self.tone:
            parts.append(f"## Tone & Style\n{self.tone}\n\n")
        
        if self.constraints:
            parts.append("## Constraints\n")
            parts.extend(f"- {c}" for c in self.constraints)
            parts.append("\n")
        
        if self.output_format:
            parts.append(f"## Output Format\n{self.output_format}\n\n")
        
        if self.examples:
            parts.append("## Examples\n")
            for i, ex in enumerate(self.examples, 1):
                parts.append(f"Example {i}:\n")
                parts.append(f"Input: {ex['input']}\n")
                parts.append(f"Output: {ex['output']}\n\n")
        
        return ''.join(parts).strip()
```

## Few-Shot Prompting

### Implementation Strategies

```typescript
// prompts/fewShotPatterns.ts - Few-shot prompting implementations

interface FewShotExample {
  input: string;
  output: string;
  explanation?: string;
}

interface FewShotConfig {
  examples: FewShotExample[];
  labels?: string[];
  randomize?: boolean;
  includeExplanation?: boolean;
}

// Standard few-shot: Direct examples
export function createFewShotPrompt(
  taskDescription: string,
  examples: FewShotExample[],
  newInput: string
): string {
  let prompt = `${taskDescription}\n\n`;
  prompt += '## Ví dụ:\n\n';
  
  for (const example of examples) {
    prompt += `Input: ${example.input}\n`;
    prompt += `Output: ${example.output}\n\n`;
  }
  
  prompt += `## Nhiệm vụ mới:\n`;
  prompt += `Input: ${newInput}\n`;
  prompt += 'Output:';
  
  return prompt;
}

// Chain-of-thought few-shot: Examples with reasoning
export function createCoTFewShotPrompt(
  taskDescription: string,
  examples: Array<{
    input: string;
    reasoning: string;
    output: string;
  }>,
  newInput: string
): string {
  let prompt = `${taskDescription}\n\n`;
  prompt += '## Ví dụ với quá trình suy luận:\n\n';
  
  for (const example of examples) {
    prompt += `Input: ${example.input}\n`;
    prompt += `Quá trình suy luận: ${example.reasoning}\n`;
    prompt += `Output: ${example.output}\n\n`;
  }
  
  prompt += `## Nhiệm vụ mới:\n`;
  prompt += `Input: ${newInput}\n`;
  prompt += 'Quá trình suy luận: ';
  
  return prompt;
}

// Classification few-shot
export function createClassificationFewShot(
  categories: string[],
  examples: Array<{ text: string; category: string }>,
  newText: string
): string {
  let prompt = `Phân loại văn bản vào một trong các categories: ${categories.join(', ')}.\n\n`;
  prompt += '## Ví dụ:\n\n';
  
  for (const example of examples) {
    prompt += `Văn bản: ${example.text}\n`;
    prompt += `Category: ${example.category}\n\n`;
  }
  
  prompt += `## Phân loại văn bản mới:\n`;
  prompt += `Văn bản: ${newText}\n`;
  prompt += 'Category:';
  
  return prompt;
}

// Structured output few-shot
export function createStructuredFewShot(
  schema: {
    fields: Array<{ name: string; description: string; type: string }>;
  },
  examples: Array<{ input: string; output: Record<string, any> }>,
  newInput: string
): string {
  const fieldDescriptions = schema.fields
    .map(f => `  - ${f.name} (${f.type}): ${f.description}`)
    .join('\n');
  
  let prompt = `Trích xuất thông tin theo schema sau:\n\n${fieldDescriptions}\n\n`;
  prompt += '## Ví dụ:\n\n';
  
  for (const example of examples) {
    prompt += `Input: ${example.input}\n`;
    prompt += `Output: ${JSON.stringify(example.output, null, 2)}\n\n`;
  }
  
  prompt += `## Trích xuất thông tin:\n`;
  prompt += `Input: ${newInput}\n`;
  prompt += 'Output:';
  
  return prompt;
}

// Mixed approach: Positive and negative examples
export function createContrastiveFewShot(
  positiveExamples: string[],
  negativeExamples: string[],
  newInput: string
): string {
  let prompt = 'Xác định xem input sau có match criteria hay không.\n\n';
  
  prompt += '## Positive Examples (Match):\n';
  for (const ex of positiveExamples) {
    prompt += `- ${ex}\n`;
  }
  
  prompt += '\n## Negative Examples (No Match):\n';
  for (const ex of negativeExamples) {
    prompt += `- ${ex}\n`;
  }
  
  prompt += '\n## Đánh giá input mới:\n';
  prompt += `Input: ${newInput}\n`;
  prompt += 'Match (Yes/No):';
  
  return prompt;
}

// Dynamic few-shot selection
export class DynamicFewShotSelector {
  private embeddingService: any;
  private exampleEmbeddings: Map<string, number[]> = new Map();
  
  constructor(embeddingService: any) {
    this.embeddingService = embeddingService;
  }
  
  async addExample(
    example: FewShotExample,
    category?: string
  ): Promise<void> {
    const key = category || example.input;
    const embedding = await this.embeddingService.createEmbedding(
      example.input
    );
    this.exampleEmbeddings.set(key, embedding.embedding);
  }
  
  async selectRelevantExamples(
    input: string,
    k: number = 5
  ): Promise<FewShotExample[]> {
    const inputEmbedding = await this.embeddingService.createEmbedding(input);
    const similarities: Array<{ key: string; similarity: number }> = [];
    
    for (const [key, embedding] of this.exampleEmbeddings) {
      const similarity = this.cosineSimilarity(
        inputEmbedding.embedding,
        embedding
      );
      similarities.push({ key, similarity });
    }
    
    return similarities
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, k)
      .map(s => ({ input: s.key, output: '' })); // Simplified
  }
  
  private cosineSimilarity(a: number[], b: number[]): number {
    let dot = 0, normA = 0, normB = 0;
    for (let i = 0; i < a.length; i++) {
      dot += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }
    return dot / (Math.sqrt(normA) * Math.sqrt(normB));
  }
}
```

```python
# prompts/few_shot_patterns.py - Few-shot prompting implementations
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class FewShotExample:
    input: str
    output: str
    explanation: Optional[str] = None

def create_few_shot_prompt(
    task_description: str,
    examples: List[FewShotExample],
    new_input: str
) -> str:
    """Create standard few-shot prompt."""
    lines = [task_description, "", "## Ví dụ:", ""]
    
    for ex in examples:
        lines.append(f"Input: {ex.input}")
        lines.append(f"Output: {ex.output}")
        lines.append("")
    
    lines.extend(["## Nhiệm vụ mới:", f"Input: {new_input}", "Output:"])
    
    return "\n".join(lines)

def create_cot_few_shot_prompt(
    task_description: str,
    examples: List[Dict[str, str]],
    new_input: str
) -> str:
    """Create chain-of-thought few-shot prompt."""
    lines = [task_description, "", "## Ví dụ với quá trình suy luận:", ""]
    
    for ex in examples:
        lines.append(f"Input: {ex['input']}")
        lines.append(f"Quá trình suy luận: {ex['reasoning']}")
        lines.append(f"Output: {ex['output']}")
        lines.append("")
    
    lines.extend([
        "## Nhiệm vụ mới:",
        f"Input: {new_input}",
        "Quá trình suy luận:"
    ])
    
    return "\n".join(lines)

def create_classification_few_shot(
    categories: List[str],
    examples: List[Dict[str, str]],
    new_text: str
) -> str:
    """Create classification few-shot prompt."""
    lines = [
        f"Phân loại văn bản vào một trong các categories: {', '.join(categories)}.",
        "", "## Ví dụ:", ""
    ]
    
    for ex in examples:
        lines.append(f"Văn bản: {ex['text']}")
        lines.append(f"Category: {ex['category']}")
        lines.append("")
    
    lines.extend([
        "## Phân loại văn bản mới:",
        f"Văn bản: {new_text}",
        "Category:"
    ])
    
    return "\n".join(lines)

def create_structured_few_shot(
    schema: Dict[str, Any],
    examples: List[Dict[str, Any]],
    new_input: str
) -> str:
    """Create structured output few-shot prompt."""
    field_lines = [
        f"  - {f['name']} ({f['type']}): {f['description']}"
        for f in schema['fields']
    ]
    
    lines = ["Trích xuất thông tin theo schema sau:", "", "\n".join(field_lines), "", "## Ví dụ:", ""]
    
    for ex in examples:
        lines.append(f"Input: {ex['input']}")
        import json
        lines.append(f"Output: {json.dumps(ex['output'], indent=2)}")
        lines.append("")
    
    lines.extend(["## Trích xuất thông tin:", f"Input: {new_input}", "Output:"])
    
    return "\n".join(lines)

class DynamicFewShotSelector:
    """Selects relevant examples dynamically based on similarity."""
    
    def __init__(self, embedding_service):
        self.embedding_service = embedding_service
        self.example_embeddings: Dict[str, List[float]] = {}
    
    async def add_example(
        self,
        example: FewShotExample,
        category: Optional[str] = None
    ) -> None:
        """Add an example with its embedding."""
        key = category or example.input
        result = await self.embedding_service.create_embedding(example.input)
        self.example_embeddings[key] = result.embedding
    
    async def select_relevant_examples(
        self,
        input_text: str,
        k: int = 5
    ) -> List[FewShotExample]:
        """Select top-k most similar examples."""
        input_embedding = await self.embedding_service.create_embedding(input_text)
        
        similarities = []
        for key, embedding in self.example_embeddings.items():
            similarity = self._cosine_similarity(input_embedding.embedding, embedding)
            similarities.append((key, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return [
            FewShotExample(input=key, output="")
            for key, _ in similarities[:k]
        ]
    
    @staticmethod
    def _cosine_similarity(a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0
```

## Chain-of-Thought Prompting

### Implementation

```typescript
// prompts/chainOfThought.ts - Chain-of-thought prompting patterns

interface CoTConfig {
  includeSteps: boolean;
  stepLabels?: string[];
  requireVerification?: boolean;
}

// Zero-shot chain-of-thought
export const zeroShotCoTPrompt = `Hãy giải quyết vấn đề sau theo từng bước:

Vấn đề: {problem}

Bước 1: [Xác định thông tin đã biết]
[Phân tích chi tiết]

Bước 2: [Xác định phương pháp giải quyết]
[Giải thích approach]

Bước 3: [Thực hiện tính toán/phân tích]
[Chi tiết các bước cụ thể]

Bước 4: [Kiểm tra kết quả]
[Xác minh logic]

Kết luận: [Final answer with explanation]`;

// Few-shot chain-of-thought
export function createCoTFewShot(
  taskType: string,
  examples: Array<{
    problem: string;
    steps: string[];
    finalAnswer: string;
  }>,
  newProblem: string
): string {
  let prompt = `Hãy giải quyết các vấn đề ${taskType} theo từng bước suy luận.\n\n`;
  
  for (let i = 0; i < examples.length; i++) {
    const ex = examples[i];
    prompt += `## Ví dụ ${i + 1}:\n\n`;
    prompt += `Vấn đề: ${ex.problem}\n\n`;
    prompt += `Suy luận:\n`;
    
    for (let j = 0; j < ex.steps.length; j++) {
      prompt += `${j + 1}. ${ex.steps[j]}\n`;
    }
    
    prompt += `\nĐáp án: ${ex.finalAnswer}\n\n`;
  }
  
  prompt += `---\n\n`;
  prompt += `## Vấn đề cần giải quyết:\n\n`;
  prompt += `Vấn đề: ${newProblem}\n\n`;
  prompt += `Suy luận:\n`;
  
  return prompt;
}

// Self-consistency with chain-of-thought
export async function selfConsistencyCoT(
  openai: any,
  problem: string,
  nResponses: number = 5,
  temperature: number = 0.7
): Promise<{
  answers: string[];
  consensusAnswer: string;
  consistencyScore: number;
}> {
  const prompts = Array(nResponses).fill(null).map(() => 
    `Hãy suy nghĩ về vấn đề này một cách cẩn thận và đưa ra câu trả lời cuối cùng.\n\nVấn đề: ${problem}\n\nSuy luận:`
  );
  
  // Generate multiple responses
  const responses = await Promise.all(
    prompts.map(p => openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: p }],
      temperature,
      max_tokens: 500,
    }))
  );
  
  const answers = responses.map(r => r.choices[0].message.content || '');
  
  // Count answer frequencies (simplified - in production use more sophisticated matching)
  const answerCounts = new Map<string, number>();
  for (const answer of answers) {
    const normalized = answer.toLowerCase().trim();
    answerCounts.set(normalized, (answerCounts.get(normalized) || 0) + 1);
  }
  
  // Find consensus
  let maxCount = 0;
  let consensusAnswer = '';
  for (const [answer, count] of answerCounts) {
    if (count > maxCount) {
      maxCount = count;
      consensusAnswer = answer;
    }
  }
  
  return {
    answers,
    consensusAnswer,
    consistencyScore: maxCount / nResponses,
  };
}

// Tree of thoughts
export class TreeOfThoughts {
  private openai: any;
  private maxDepth: number;
  private breadth: number;
  
  constructor(openai: any, maxDepth: number = 3, breadth: number = 3) {
    this.openai = openai;
    this.maxDepth = maxDepth;
    this.breadth = breadth;
  }
  
  async solve(
    problem: string,
    evaluators: Array<(thought: string) => Promise<number>>
  ): Promise<{
    bestPath: string[];
    score: number;
  }> {
    // Initialize with problem analysis
    const initialThought = await this.generateThought(
      `Phân tích vấn đề: ${problem}`
    );
    
    let nodes = [{ thought: initialThought, depth: 0, score: 0 }];
    let bestNode = nodes[0];
    
    for (let depth = 0; depth < this.maxDepth; depth++) {
      const newNodes: Array<{
        thought: string;
        depth: number;
        score: number;
        parent?: string;
      }> = [];
      
      for (const node of nodes) {
        // Generate multiple branches
        const branches = await this.generateBranches(
          node.thought,
          this.breadth
        );
        
        for (const branch of branches) {
          // Evaluate each branch
          const scores = await Promise.all(
            evaluators.map(e => e(branch))
          );
          const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
          
          newNodes.push({
            thought: branch,
            depth: depth + 1,
            score: node.score + avgScore,
            parent: node.thought,
          });
        }
      }
      
      // Prune to top branches
      nodes = newNodes
        .sort((a, b) => b.score - a.score)
        .slice(0, this.breadth);
      
      if (nodes.length > 0 && nodes[0].score > bestNode.score) {
        bestNode = nodes[0];
      }
    }
    
    // Reconstruct path
    const path = this.reconstructPath(bestNode);
    
    return {
      bestPath: path,
      score: bestNode.score,
    };
  }
  
  private async generateThought(prompt: string): Promise<string> {
    const response = await this.openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.7,
      max_tokens: 300,
    });
    return response.choices[0].message.content || '';
  }
  
  private async generateBranches(
    thought: string,
    n: number
  ): Promise<string[]> {
    const prompt = `${thought}\n\nDựa trên suy nghĩ trên, hãy đề xuất ${n} hướng đi khác nhau để tiếp tục phân tích:`;
    
    const response = await this.openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.9,
      max_tokens: 500,
    });
    
    // Parse branches (simplified)
    const content = response.choices[0].message.content || '';
    return content.split(/\n/).filter(line => line.trim()).slice(0, n);
  }
  
  private reconstructPath(node: any): string[] {
    const path = [node.thought];
    // In real implementation, follow parent pointers
    return path.reverse();
  }
}
```

```python
# prompts/chain_of_thought.py - Chain-of-thought prompting patterns
from typing import List, Dict, Any, Optional
import asyncio

ZERO_SHOT_COT_PROMPT = """Hãy giải quyết vấn đề sau theo từng bước:

Vấn đề: {problem}

Bước 1: [Xác định thông tin đã biết]
[Phân tích chi tiết]

Bước 2: [Xác định phương pháp giải quyết]
[Giải thích approach]

Bước 3: [Thực hiện tính toán/phân tích]
[Chi tiết các bước cụ thể]

Bước 4: [Kiểm tra kết quả]
[Xác minh logic]

Kết luận: [Final answer with explanation]"""

def create_cot_few_shot(
    task_type: str,
    examples: List[Dict[str, Any]],
    new_problem: str
) -> str:
    """Create few-shot chain-of-thought prompt."""
    lines = [f"Hãy giải quyết các vấn đề {task_type} theo từng bước suy luận.", ""]
    
    for i, ex in enumerate(examples, 1):
        lines.append(f"## Ví dụ {i}:")
        lines.append(f"Vấn đề: {ex['problem']}")
        lines.append("")
        lines.append("Suy luận:")
        
        for j, step in enumerate(ex['steps'], 1):
            lines.append(f"{j}. {step}")
        
        lines.append("")
        lines.append(f"Đáp án: {ex['final_answer']}")
        lines.append("")
    
    lines.extend([
        "---",
        "## Vấn đề cần giải quyết:",
        f"Vấn đề: {new_problem}",
        "",
        "Suy luận:"
    ])
    
    return "\n".join(lines)

async def self_consistency_cot(
    openai_client,
    problem: str,
    n_responses: int = 5,
    temperature: float = 0.7
) -> Dict[str, Any]:
    """Generate multiple CoT responses and find consensus."""
    prompts = [
        f"""Hãy suy nghĩ về vấn đề này một cách cẩn thận và đưa ra câu trả lời cuối cùng.

Vấn đề: {problem}

Suy luận:"""
        for _ in range(n_responses)
    ]
    
    # Generate responses
    tasks = [
        openai_client.chat.completions.create(
            model='gpt-4o',
            messages=[{'role': 'user', 'content': p}],
            temperature=temperature,
            max_tokens=500,
        )
        for p in prompts
    ]
    
    responses = await asyncio.gather(*tasks)
    answers = [r.choices[0].message.content or '' for r in responses]
    
    # Count frequencies (simplified)
    answer_counts = {}
    for answer in answers:
        normalized = answer.lower().strip()
        answer_counts[normalized] = answer_counts.get(normalized, 0) + 1
    
    # Find consensus
    consensus_answer = max(answer_counts, key=answer_counts.get)
    max_count = answer_counts[consensus_answer]
    
    return {
        'answers': answers,
        'consensus_answer': consensus_answer,
        'consistency_score': max_count / n_responses,
    }

class TreeOfThoughts:
    """Tree of thoughts reasoning implementation."""
    
    def __init__(self, openai_client, max_depth: int = 3, breadth: int = 3):
        self.client = openai_client
        self.max_depth = max_depth
        self.breadth = breadth
    
    async def solve(
        self,
        problem: str,
        evaluators: List[callable]
    ) -> Dict[str, Any]:
        """Solve problem using tree of thoughts."""
        # Initialize
        initial_thought = await self._generate_thought(
            f"Phân tích vấn đề: {problem}"
        )
        
        nodes = [{'thought': initial_thought, 'depth': 0, 'score': 0.0}]
        best_node = nodes[0]
        
        for depth in range(self.max_depth):
            new_nodes = []
            
            for node in nodes:
                # Generate branches
                branches = await self._generate_branches(
                    node['thought'],
                    self.breadth
                )
                
                for branch in branches:
                    # Evaluate
                    scores = await asyncio.gather(
                        *[e(branch) for e in evaluators]
                    )
                    avg_score = sum(scores) / len(scores)
                    
                    new_nodes.append({
                        'thought': branch,
                        'depth': depth + 1,
                        'score': node['score'] + avg_score,
                        'parent': node['thought'],
                    })
            
            # Prune
            new_nodes.sort(key=lambda x: x['score'], reverse=True)
            nodes = new_nodes[:self.breadth]
            
            if nodes and nodes[0]['score'] > best_node['score']:
                best_node = nodes[0]
        
        path = self._reconstruct_path(best_node)
        
        return {
            'best_path': path,
            'score': best_node['score'],
        }
    
    async def _generate_thought(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model='gpt-4o',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.7,
            max_tokens=300,
        )
        return response.choices[0].message.content or ''
    
    async def _generate_branches(
        self,
        thought: str,
        n: int
    ) -> List[str]:
        prompt = f"""{thought}

Dựa trên suy nghĩ trên, hãy đề xuất {n} hướng đi khác nhau để tiếp tục phân tích:"""
        
        response = await self.client.chat.completions.create(
            model='gpt-4o',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.9,
            max_tokens=500,
        )
        
        content = response.choices[0].message.content or ''
        branches = [line.strip() for line in content.split('\n') if line.strip()]
        return branches[:n]
    
    def _reconstruct_path(self, node: Dict) -> List[str]:
        """Reconstruct path from node to root."""
        path = [node['thought']]
        # In real implementation, follow parent pointers
        return list(reversed(path))
```

## Prompt Templates

### Template Systems

```typescript
// prompts/templateEngine.ts - Prompt template system
import * as Handlebars from 'handlebars';

interface TemplateContext {
  [key: string]: any;
}

interface PromptTemplate {
  name: string;
  template: string;
  description?: string;
  variables: string[];
}

// Predefined templates
const templates: Record<string, PromptTemplate> = {
  analyze: {
    name: 'analyze',
    template: `## Nhiệm vụ: Phân tích {{subject}}

{{#if focus}}
Trọng tâm: {{focus}}
{{/if}}

{{#each analysisDimensions}}
- {{this}}
{{/each}}

{{#if examples}}
## Ví dụ tham khảo:
{{#each examples}}
{{this}}
{{/each}}
{{/if}}

## Nội dung cần phân tích:
{{content}}

{{#if constraints}}
## Ràng buộc:
{{#each constraints}}
- {{this}}
{{/each}}
{{/if}}`,
    variables: ['subject', 'focus', 'analysisDimensions', 'content', 'examples', 'constraints'],
  },
  
  summarize: {
    name: 'summarize',
    template: `Tóm tắt nội dung sau một cách {{length}}:

Độ dài mong muốn: {{lengthDescription}}
Trọng tâm: {{focus}}

Nội dung:
{{content}}

{{#if includeKeyPoints}}
Bao gồm các điểm chính:
{{#each keyPoints}}
- {{this}}
{{/each}}
{{/if}}

{{#if includeActionItems}}
Liệt kê các hành động cần thực hiện.
{{/if}}`,
    variables: ['length', 'lengthDescription', 'focus', 'content', 'keyPoints', 'includeActionItems'],
  },
  
  extract: {
    name: 'extract',
    template: `Trích xuất thông tin từ văn bản theo schema:

Schema:
{{schema}}

Văn bản nguồn:
{{content}}

{{#if instructions}}
Hướng dẫn bổ sung:
{{instructions}}
{{/if}}`,
    variables: ['schema', 'content', 'instructions'],
  },
  
  translate: {
    name: 'translate',
    template: `Dịch {{sourceLanguage}} sang {{targetLanguage}}:

{{#if tone}}
Phong cách: {{tone}}
{{/if}}

{{#if context}}
Bối cảnh: {{context}}
{{/if}}

Nội dung:
{{content}}

{{#if preserveFormat}}
Giữ nguyên định dạng.
{{/if}}

{{#if glossaries}}
Thuật ngữ:
{{#each glossaries}}
- {{this.source}} = {{this.target}}
{{/each}}
{{/if}}`,
    variables: ['sourceLanguage', 'targetLanguage', 'tone', 'context', 'content', 'preserveFormat', 'glossaries'],
  },
};

export class PromptTemplateEngine {
  private templates: Map<string, HandlebarsTemplateDelegate>;
  
  constructor() {
    this.templates = new Map();
    this.registerBuiltInTemplates();
  }
  
  private registerBuiltInTemplates(): void {
    for (const [name, template] of Object.entries(templates)) {
      this.register(name, template.template);
    }
  }
  
  register(name: string, template: string): void {
    this.templates.set(name, Handlebars.compile(template));
  }
  
  render(name: string, context: TemplateContext): string {
    const template = this.templates.get(name);
    if (!template) {
      throw new Error(`Template "${name}" not found`);
    }
    return template(context);
  }
  
  renderRaw(template: string, context: TemplateContext): string {
    const compiled = Handlebars.compile(template);
    return compiled(context);
  }
  
  listTemplates(): string[] {
    return Array.from(this.templates.keys());
  }
}

// Advanced template features
export class DynamicPromptBuilder {
  private openai: any;
  private context: Map<string, any> = new Map();
  
  constructor(openai: any) {
    this.openai = openai;
  }
  
  setContext(key: string, value: any): this {
    this.context.set(key, value);
    return this;
  }
  
  async generateDynamicInstruction(
    taskType: string,
    inputData: any
  ): Promise<string> {
    const contextSummary = this.summarizeContext();
    
    const response = await this.openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        {
          role: 'system',
          content: `Bạn là một prompt engineer chuyên nghiệp. Tạo instructions chi tiết cho task được yêu cầu.`,
        },
        {
          role: 'user',
          content: `Tạo prompt cho task: ${taskType}

Context hiện tại:
${contextSummary}

Input data:
${JSON.stringify(inputData, null, 2)}

Hãy tạo một prompt chi tiết, bao gồm:
1. Mục tiêu rõ ràng
2. Các bước thực hiện
3. Ràng buộc và expectations
4. Output format`,
        },
      ],
      temperature: 0.3,
      max_tokens: 500,
    });
    
    return response.choices[0].message.content || '';
  }
  
  private summarizeContext(): string {
    const lines: string[] = [];
    for (const [key, value] of this.context) {
      lines.push(`- ${key}: ${JSON.stringify(value)}`);
    }
    return lines.join('\n');
  }
}
```

```python
# prompts/template_engine.py - Prompt template system
from typing import Dict, Any, List, Optional, Callable
import re
from string import Template

class PromptTemplate:
    """Simple prompt template with variable substitution."""
    
    def __init__(self, template: str):
        self.template = Template(template)
    
    def render(self, **kwargs) -> str:
        return self.template.substitute(**kwargs)

# Predefined templates
TEMPLATES = {
    'analyze': PromptTemplate("""## Nhiệm vụ: Phân tích $subject

$focus

$analysis_dimensions

$content

$constraints"""),
    
    'summarize': PromptTemplate("""Tóm tắt nội dung sau một cách $length:

Độ dài mong muốn: $length_description
Trọng tâm: $focus

Nội dung:
$content"""),
    
    'extract': PromptTemplate("""Trích xuất thông tin từ văn bản theo schema:

Schema:
$schema

Văn bản nguồn:
$content"""),
}

class PromptTemplateEngine:
    """Engine for managing and rendering prompt templates."""
    
    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
        self._register_builtins()
    
    def _register_builtins(self) -> None:
        for name, template in TEMPLATES.items():
            self.register(name, template.template.template)
    
    def register(self, name: str, template_str: str) -> None:
        self.templates[name] = PromptTemplate(template_str)
    
    def render(self, name: str, **context) -> str:
        if name not in self.templates:
            raise ValueError(f'Template "{name}" not found')
        return self.templates[name].render(**context)
    
    def render_raw(self, template_str: str, **context) -> str:
        return Template(template_str).substitute(**context)
    
    def list_templates(self) -> List[str]:
        return list(self.templates.keys())

class DynamicPromptBuilder:
    """Builder that generates prompts dynamically based on context."""
    
    def __init__(self, openai_client):
        self.client = openai_client
        self.context: Dict[str, Any] = {}
    
    def set_context(self, key: str, value: Any) -> 'DynamicPromptBuilder':
        self.context[key] = value
        return self
    
    async def generate_dynamic_instruction(
        self,
        task_type: str,
        input_data: Dict[str, Any]
    ) -> str:
        """Generate dynamic instruction using LLM."""
        context_summary = self._summarize_context()
        
        response = await self.client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {
                    'role': 'system',
                    'content': 'Bạn là một prompt engineer chuyên nghiệp. Tạo instructions chi tiết cho task được yêu cầu.'
                },
                {
                    'role': 'user',
                    'content': f"""Tạo prompt cho task: {task_type}

Context hiện tại:
{context_summary}

Input data:
{input_data}

Hãy tạo một prompt chi tiết, bao gồm:
1. Mục tiêu rõ ràng
2. Các bước thực hiện
3. Ràng buộc và expectations
4. Output format"""
                }
            ],
            temperature=0.3,
            max_tokens=500,
        )
        
        return response.choices[0].message.content or ''
    
    def _summarize_context(self) -> str:
        lines = []
        for key, value in self.context.items():
            lines.append(f"- {key}: {value}")
        return '\n'.join(lines)
```

## Prompt Chaining

### Multi-Step Workflows

```typescript
// prompts/promptChain.ts - Prompt chaining patterns

interface ChainStep {
  name: string;
  prompt: string | ((input: any) => string);
  outputKey: string;
  validation?: (output: any) => boolean;
}

interface ChainResult {
  outputs: Map<string, any>;
  finalOutput: any;
  stepsExecuted: string[];
  errors: Array<{ step: string; error: string }>;
}

export class PromptChain {
  private steps: ChainStep[] = [];
  private openai: any;
  
  constructor(openai: any) {
    this.openai = openai;
  }
  
  addStep(step: ChainStep): this {
    this.steps.push(step);
    return this;
  }
  
  async execute(initialInput: any): Promise<ChainResult> {
    const outputs = new Map<string, any>();
    const stepsExecuted: string[] = [];
    const errors: Array<{ step: string; error: string }> = [];
    
    let currentInput = initialInput;
    
    for (const step of this.steps) {
      try {
        const prompt = typeof step.prompt === 'function'
          ? step.prompt(currentInput)
          : this.interpolatePrompt(step.prompt, currentInput, outputs);
        
        const response = await this.openai.chat.completions.create({
          model: 'gpt-4o',
          messages: [{ role: 'user', content: prompt }],
          temperature: 0.3,
        });
        
        const output = response.choices[0].message.content || '';
        
        // Validate if validator exists
        if (step.validation && !step.validation(output)) {
          errors.push({
            step: step.name,
            error: 'Output validation failed',
          });
          // Continue or break based on strategy
        }
        
        outputs.set(step.outputKey, output);
        stepsExecuted.push(step.name);
        currentInput = output;
        
      } catch (error: any) {
        errors.push({
          step: step.name,
          error: error.message,
        });
        // Decide whether to continue or fail
      }
    }
    
    return {
      outputs,
      finalOutput: currentInput,
      stepsExecuted,
      errors,
    };
  }
  
  private interpolatePrompt(
    prompt: string,
    currentInput: any,
    outputs: Map<string, any>
  ): string {
    let interpolated = prompt;
    
    // Replace ${input} with current input
    interpolated = interpolated.replace(
      /\${input}/g,
      typeof currentInput === 'string' ? currentInput : JSON.stringify(currentInput)
    );
    
    // Replace ${outputs.key} with previous outputs
    for (const [key, value] of outputs) {
      const valueStr = typeof value === 'string' ? value : JSON.stringify(value);
      interpolated = interpolated.replace(
        new RegExp(`\\$\\{outputs\\.${key}\\}`, 'g'),
        valueStr
      );
    }
    
    return interpolated;
  }
}

// Pre-built chains
export function createAnalysisChain(openai: any): PromptChain {
  return new PromptChain(openai)
    .addStep({
      name: 'extract',
      prompt: `Trích xuất các thông tin chính từ văn bản sau:\n\n${input}`,
      outputKey: 'extractedInfo',
    })
    .addStep({
      name: 'categorize',
      prompt: `Phân loại thông tin sau vào các categories phù hợp:\n\n${outputs.extractedInfo}`,
      outputKey: 'categories',
    })
    .addStep({
      name: 'summarize',
      prompt: `Tạo bản tóm tắt ngắn gọn từ thông tin đã phân loại:\n\n${outputs.categories}`,
      outputKey: 'summary',
    })
    .addStep({
      name: 'recommend',
      prompt: `Đưa ra recommendations dựa trên phân tích sau:\n\n${outputs.summary}`,
      outputKey: 'recommendations',
    });
}

export function createTranslationChain(openai: any): PromptChain {
  return new PromptChain(openai)
    .addStep({
      name: 'analyze',
      prompt: `Phân tích văn bản để xác định:\n1. Tone và style\n2. Domain/chuyên ngành\n3. Các thuật ngữ quan trọng\n\nVăn bản: ${input}`,
      outputKey: 'analysis',
    })
    .addStep({
      name: 'translate',
      prompt: `Dịch văn bản sang ${targetLanguage}, giữ nguyên tone, style và thuật ngữ đã xác định.\n\nPhân tích: ${outputs.analysis}\n\nVăn bản gốc: ${input}`,
      outputKey: 'translation',
    })
    .addStep({
      name: 'review',
      prompt: `Kiểm tra bản dịch và đề xuất cải thiện nếu cần:\n\nBản dịch: ${outputs.translation}\n\nPhân tích gốc: ${outputs.analysis}`,
      outputKey: 'review',
    });
}

// Conditional chains
export class ConditionalChain {
  private branches: Map<string, PromptChain> = new Map();
  private defaultChain?: PromptChain;
  
  addBranch(condition: string, chain: PromptChain): this {
    this.branches.set(condition, chain);
    return this;
  }
  
  setDefault(chain: PromptChain): this {
    this.defaultChain = chain;
    return this;
  }
  
  async execute(input: any, classifier: (input: any) => Promise<string>): Promise<ChainResult> {
    const classification = await classifier(input);
    
    const chain = this.branches.get(classification) || this.defaultChain;
    
    if (!chain) {
      throw new Error(`No chain found for classification: ${classification}`);
    }
    
    return chain.execute(input);
  }
}
```

```python
# prompts/prompt_chain.py - Prompt chaining patterns
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass
import json

@dataclass
class ChainStep:
    name: str
    prompt: Union[str, Callable[[Any], str]]
    output_key: str
    validator: Optional[Callable[[Any], bool]] = None

@dataclass
class ChainResult:
    outputs: Dict[str, Any]
    final_output: Any
    steps_executed: List[str]
    errors: List[Dict[str, str]]

class PromptChain:
    """Chain multiple prompts together."""
    
    def __init__(self, openai_client):
        self.client = openai_client
        self.steps: List[ChainStep] = []
    
    def add_step(
        self,
        name: str,
        prompt: Union[str, Callable[[Any], str]],
        output_key: str,
        validator: Optional[Callable[[Any], bool]] = None
    ) -> 'PromptChain':
        self.steps.append(ChainStep(name, prompt, output_key, validator))
        return self
    
    async def execute(self, initial_input: Any) -> ChainResult:
        outputs = {}
        steps_executed = []
        errors = []
        
        current_input = initial_input
        
        for step in self.steps:
            try:
                # Generate prompt
                if callable(step.prompt):
                    prompt = step.prompt(current_input)
                else:
                    prompt = self._interpolate_prompt(
                        step.prompt,
                        current_input,
                        outputs
                    )
                
                # Execute
                response = await self.client.chat.completions.create(
                    model='gpt-4o',
                    messages=[{'role': 'user', 'content': prompt}],
                    temperature=0.3,
                )
                
                output = response.choices[0].message.content or ''
                
                # Validate
                if step.validator and not step.validator(output):
                    errors.append({
                        'step': step.name,
                        'error': 'Output validation failed'
                    })
                
                outputs[step.output_key] = output
                steps_executed.append(step.name)
                current_input = output
                
            except Exception as e:
                errors.append({
                    'step': step.name,
                    'error': str(e)
                })
        
        return ChainResult(
            outputs=outputs,
            final_output=current_input,
            steps_executed=steps_executed,
            errors=errors
        )
    
    def _interpolate_prompt(
        self,
        prompt: str,
        current_input: Any,
        outputs: Dict[str, Any]
    ) -> str:
        """Replace variables in prompt template."""
        interpolated = prompt
        
        # Replace ${input}
        input_str = current_input if isinstance(current_input, str) else json.dumps(current_input)
        interpolated = interpolated.replace('${input}', input_str)
        
        # Replace ${outputs.key}
        for key, value in outputs.items():
            value_str = value if isinstance(value, str) else json.dumps(value)
            interpolated = interpolated.replace(f'${{outputs.{key}}}', value_str)
        
        return interpolated

def create_analysis_chain(openai_client) -> PromptChain:
    """Create a standard analysis chain."""
    chain = PromptChain(openai_client)
    
    chain.add_step(
        'extract',
        'Trích xuất các thông tin chính từ văn bản sau:\n\n${input}',
        'extracted_info'
    )
    
    chain.add_step(
        'categorize',
        'Phân loại thông tin sau vào các categories phù hợp:\n\n${outputs.extracted_info}',
        'categories'
    )
    
    chain.add_step(
        'summarize',
        'Tạo bản tóm tắt ngắn gọn từ thông tin đã phân loại:\n\n${outputs.categories}',
        'summary'
    )
    
    chain.add_step(
        'recommend',
        'Đưa ra recommendations dựa trên phân tích sau:\n\n${outputs.summary}',
        'recommendations'
    )
    
    return chain

class ConditionalChain:
    """Chain that branches based on input classification."""
    
    def __init__(self, openai_client):
        self.client = openai_client
        self.branches: Dict[str, PromptChain] = {}
        self.default_chain: Optional[PromptChain] = None
    
    def add_branch(self, condition: str, chain: PromptChain) -> 'ConditionalChain':
        self.branches[condition] = chain
        return self
    
    def set_default(self, chain: PromptChain) -> 'ConditionalChain':
        self.default_chain = chain
        return self
    
    async def execute(
        self,
        input_data: Any,
        classifier: Callable[[Any], str]
    ) -> ChainResult:
        classification = await classifier(input_data)
        
        chain = self.branches.get(classification) or self.default_chain
        
        if not chain:
            raise ValueError(f'No chain found for classification: {classification}')
        
        return await chain.execute(input_data)
```

## Best Practices

### Optimization Techniques

```typescript
// prompts/optimization.ts - Prompt optimization utilities

interface PromptMetrics {
  tokenCount: number;
  estimatedCost: number;
  clarityScore: number;
  specificityScore: number;
  completenessScore: number;
}

export class PromptOptimizer {
  private openai: any;
  
  constructor(openai: any) {
    this.openai = openai;
  }
  
  async analyze(prompt: string): Promise<PromptMetrics> {
    const tokenCount = await this.estimateTokens(prompt);
    
    return {
      tokenCount,
      estimatedCost: this.estimateCost(tokenCount),
      clarityScore: await this.scoreClarity(prompt),
      specificityScore: await this.scoreSpecificity(prompt),
      completenessScore: await this.scoreCompleteness(prompt),
    };
  }
  
  async optimize(
    prompt: string,
    goal: 'shorter' | 'clearer' | 'more_accurate' | 'balanced'
  ): Promise<string> {
    const optimizationStrategies = {
      shorter: 'rút gọn',
      clearer: 'làm rõ ràng hơn',
      more_accurate: 'chính xác hơn',
      balanced: 'cân bằng giữa độ dài và độ chính xác',
    };
    
    const response = await this.openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        {
          role: 'system',
          content: 'Bạn là một prompt optimization expert.',
        },
        {
          role: 'user',
          content: `Tối ưu hóa prompt sau để ${optimizationStrategies[goal]}:

Prompt hiện tại:
${prompt}

Yêu cầu:
- Giữ nguyên ý định và mục tiêu
- Cải thiện clarity và specificity
- Loại bỏ redundant information
- Đảm bảo instructions rõ ràng

Prompt đã tối ưu:`,
        },
      ],
      temperature: 0.3,
    });
    
    return response.choices[0].message.content || prompt;
  }
  
  async compare(
    promptA: string,
    promptB: string,
    testCases: string[]
  ): Promise<{
    winner: 'A' | 'B' | 'tie';
    metrics: {
      consistencyA: number;
      consistencyB: number;
      qualityA: number;
      qualityB: number;
    };
  }> {
    // Run both prompts on test cases
    const resultsA = await this.runEvaluation(promptA, testCases);
    const resultsB = await this.runEvaluation(promptB, testCases);
    
    const consistencyA = this.calculateConsistency(resultsA);
    const consistencyB = this.calculateConsistency(resultsB);
    const qualityA = this.calculateQuality(resultsA);
    const qualityB = this.calculateQuality(resultsB);
    
    let winner: 'A' | 'B' | 'tie';
    if (qualityA > qualityB && consistencyA >= consistencyB) {
      winner = 'A';
    } else if (qualityB > qualityA && consistencyB >= consistencyA) {
      winner = 'B';
    } else {
      winner = 'tie';
    }
    
    return {
      winner,
      metrics: {
        consistencyA,
        consistencyB,
        qualityA,
        qualityB,
      },
    };
  }
  
  private async estimateTokens(text: string): Promise<number> {
    // Rough estimate: ~4 chars per token
    return Math.ceil(text.length / 4);
  }
  
  private estimateCost(tokens: number): number {
    // gpt-4o pricing: $2.5 per 1M input tokens
    return (tokens / 1_000_000) * 2.5;
  }
  
  private async scoreClarity(prompt: string): Promise<number> {
    // Simplified scoring
    const clarityIndicators = [
      /^\s*#+\s/m, // Has headers
      /\n\d+\./m, // Numbered lists
      /:\s*$/m, // Ending with colon (indicates structure)
    ];
    
    const score = clarityIndicators.reduce((acc, pattern) => {
      return acc + (pattern.test(prompt) ? 0.2 : 0);
    }, 0);
    
    return Math.min(1, score);
  }
  
  private async scoreSpecificity(prompt: string): Promise<number> {
    // Check for specific instructions
    const specificityIndicators = [
      /\b(exactly|precisely|specifically)\b/i,
      /\b(must|shall|required)\b/i,
      /\b(never|always|only)\b/i,
    ];
    
    const score = specificityIndicators.reduce((acc, pattern) => {
      return acc + (pattern.test(prompt) ? 0.25 : 0);
    }, 0);
    
    return Math.min(1, score);
  }
  
  private async scoreCompleteness(prompt: string): Promise<number> {
    // Check for essential components
    const hasTask = /\b(task|objective|goal|purpose)\b/i.test(prompt);
    const hasFormat = /\b(format|output|return|respond)\b/i.test(prompt);
    const hasConstraints = /\b(constraint|limit|maximum|minimum)\b/i.test(prompt);
    
    return (hasTask ? 0.3 : 0) + (hasFormat ? 0.3 : 0) + (hasConstraints ? 0.3 : 0);
  }
  
  private async runEvaluation(
    prompt: string,
    testCases: string[]
  ): Promise<any[]> {
    return Promise.all(
      testCases.map(test =>
        this.openai.chat.completions.create({
          model: 'gpt-4o',
          messages: [
            { role: 'system', content: prompt },
            { role: 'user', content: test },
          ],
        })
      )
    );
  }
  
  private calculateConsistency(results: any[]): number {
    // Simplified: check if responses have similar lengths
    if (results.length < 2) return 1;
    
    const lengths = results.map(r =>
      r.choices[0].message.content?.length || 0
    );
    
    const avg = lengths.reduce((a, b) => a + b, 0) / lengths.length;
    const variance = lengths.reduce((sum, len) =>
      sum + Math.pow(len - avg, 2), 0
    ) / lengths.length;
    
    const cv = Math.sqrt(variance) / avg; // Coefficient of variation
    return Math.max(0, 1 - cv);
  }
  
  private calculateQuality(results: any[]): number {
    // Simplified: check for non-empty responses
    const nonEmpty = results.filter(r =>
      r.choices[0].message.content?.trim().length > 0
    ).length;
    
    return nonEmpty / results.length;
  }
}
```

```python
# prompts/optimization.py - Prompt optimization utilities
from typing import Dict, Any, List, Tuple
import re
import asyncio

class PromptOptimizer:
    """Optimize prompts for better performance."""
    
    def __init__(self, openai_client):
        self.client = openai_client
    
    async def analyze(self, prompt: str) -> Dict[str, Any]:
        """Analyze prompt and return metrics."""
        token_count = self._estimate_tokens(prompt)
        
        return {
            'token_count': token_count,
            'estimated_cost': self._estimate_cost(token_count),
            'clarity_score': await self._score_clarity(prompt),
            'specificity_score': await self._score_specificity(prompt),
            'completeness_score': await self._score_completeness(prompt),
        }
    
    async def optimize(
        self,
        prompt: str,
        goal: str = 'balanced'
    ) -> str:
        """Optimize prompt based on goal."""
        goals = {
            'shorter': 'rút gọn',
            'clearer': 'làm rõ ràng hơn',
            'more_accurate': 'chính xác hơn',
            'balanced': 'cân bằng giữa độ dài và độ chính xác',
        }
        
        response = await self.client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {
                    'role': 'system',
                    'content': 'Bạn là một prompt optimization expert.'
                },
                {
                    'role': 'user',
                    'content': f"""Tối ưu hóa prompt sau để {goals.get(goal, goals['balanced'])}:

Prompt hiện tại:
{prompt}

Yêu cầu:
- Giữ nguyên ý định và mục tiêu
- Cải thiện clarity và specificity
- Loại bỏ redundant information
- Đảm bảo instructions rõ ràng

Prompt đã tối ưu:"""
                }
            ],
            temperature=0.3,
        )
        
        return response.choices[0].message.content or prompt
    
    async def compare(
        self,
        prompt_a: str,
        prompt_b: str,
        test_cases: List[str]
    ) -> Dict[str, Any]:
        """Compare two prompts on test cases."""
        results_a = await self._run_evaluation(prompt_a, test_cases)
        results_b = await self._run_evaluation(prompt_b, test_cases)
        
        consistency_a = self._calculate_consistency(results_a)
        consistency_b = self._calculate_consistency(results_b)
        quality_a = self._calculate_quality(results_a)
        quality_b = self._calculate_quality(results_b)
        
        if quality_a > quality_b and consistency_a >= consistency_b:
            winner = 'A'
        elif quality_b > quality_a and consistency_b >= consistency_a:
            winner = 'B'
        else:
            winner = 'tie'
        
        return {
            'winner': winner,
            'metrics': {
                'consistency_A': consistency_a,
                'consistency_B': consistency_b,
                'quality_A': quality_a,
                'quality_B': quality_b,
            }
        }
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count."""
        return (len(text) // 4) + 1
    
    def _estimate_cost(self, tokens: int) -> float:
        """Estimate cost in USD."""
        return (tokens / 1_000_000) * 2.5  # gpt-4o pricing
    
    async def _score_clarity(self, prompt: str) -> float:
        """Score prompt clarity."""
        indicators = [
            bool(re.search(r'^#+\s', prompt, re.MULTILINE)),  # Headers
            bool(re.search(r'\n\d+\.', prompt)),  # Numbered lists
            bool(re.search(r':\s*$', prompt, re.MULTILINE)),  # Colons
        ]
        return sum(indicators) * 0.33
    
    async def _score_specificity(self, prompt: str) -> float:
        """Score prompt specificity."""
        indicators = [
            bool(re.search(r'\b(exactly|precisely|specifically)\b', prompt, re.I)),
            bool(re.search(r'\b(must|shall|required)\b', prompt, re.I)),
            bool(re.search(r'\b(never|always|only)\b', prompt, re.I)),
        ]
        return sum(indicators) * 0.33
    
    async def _score_completeness(self, prompt: str) -> float:
        """Score prompt completeness."""
        has_task = bool(re.search(r'\b(task|objective|goal|purpose)\b', prompt, re.I))
        has_format = bool(re.search(r'\b(format|output|return|respond)\b', prompt, re.I))
        has_constraints = bool(re.search(r'\b(constraint|limit|maximum|minimum)\b', prompt, re.I))
        
        return (has_task + has_format + has_constraints) * 0.33
    
    async def _run_evaluation(
        self,
        prompt: str,
        test_cases: List[str]
    ) -> List[Any]:
        """Run prompt on test cases."""
        tasks = [
            self.client.chat.completions.create(
                model='gpt-4o',
                messages=[
                    {'role': 'system', 'content': prompt},
                    {'role': 'user', 'content': test}
                ],
            )
            for test in test_cases
        ]
        return await asyncio.gather(*tasks)
    
    def _calculate_consistency(self, results: List[Any]) -> float:
        """Calculate response consistency."""
        if len(results) < 2:
            return 1.0
        
        lengths = [len(r.choices[0].message.content or '') for r in results]
        avg = sum(lengths) / len(lengths)
        
        if avg == 0:
            return 1.0
        
        variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)
        cv = (variance ** 0.5) / avg
        
        return max(0, 1 - cv)
    
    def _calculate_quality(self, results: List[Any]) -> float:
        """Calculate response quality."""
        non_empty = sum(
            1 for r in results
            if r.choices[0].message.content and r.choices[0].message.content.strip()
        )
        return non_empty / len(results) if results else 0
```

## Troubleshooting

### Common Issues

```typescript
// troubleshooting/promptIssues.ts - Prompt troubleshooting guide
const promptIssueGuides = [
  {
    issue: 'Inconsistent Responses',
    symptoms: [
      'Same input produces different outputs',
      'Model ignores format requirements',
      'Variable response length',
    ],
    causes: [
      'System prompt too vague',
      'Temperature too high',
      'Missing format examples',
      'Insufficient constraints',
    ],
    solutions: [
      'Add explicit format examples',
      'Lower temperature to 0.1-0.3',
      'Include detailed constraints',
      'Use stronger instruction words (must, never)',
    ],
  },
  {
    issue: 'Off-Topic Responses',
    symptoms: [
      'Model goes off on tangents',
      'Addresses topics not in request',
      'Includes unnecessary information',
    ],
    causes: [
      'Task definition unclear',
      'Too much context',
      'No scope constraints',
    ],
    solutions: [
      'Add scope limitations to system prompt',
      'Be more specific about what to address',
      'Include "Only respond to..." instructions',
      'Reduce irrelevant context',
    ],
  },
  {
    issue: 'Overly Verbose Output',
    symptoms: [
      'Responses too long',
      'Unnecessary explanations',
      'Repeats information',
    ],
    causes: [
      'No length constraints',
      'Model tries to be comprehensive',
      'Missing brevity instructions',
    ],
    solutions: [
      'Add max length constraint (e.g., "under 100 words")',
      'Include "Be concise" or "Summary only"',
      'Use explicit output format limits',
      'Set max_tokens parameter',
    ],
  },
  {
    issue: 'Refuses to Answer',
    symptoms: [
      'Model says it cannot help',
      'Responses are evasive',
      'Apologizes excessively',
    ],
    causes: [
      'System prompt too restrictive',
      'Task perceived as sensitive',
      'Conflicting instructions',
    ],
    solutions: [
      'Rephrase to focus on what model CAN do',
      'Remove unnecessary restrictions',
      'Add "It is appropriate to..." instructions',
      'Simplify the request',
    ],
  },
  {
    issue: 'Follows Wrong Pattern',
    symptoms: [
      'Uses wrong format',
      'Includes wrong information',
      'Wrong reasoning approach',
    ],
    causes: [
      'Examples not representative',
      'Ambiguous format specification',
      'Conflicting format instructions',
    ],
    solutions: [
      'Use more diverse examples',
      'Be explicit about format with "Correct format:"',
      'Remove conflicting format instructions',
      'Add validation step in chain',
    ],
  },
];
```

## References

### Official Documentation

- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Best Practices](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)
- [Effective Prompting](https://help.openai.com/en/articles/6654000-effective-prompting)

### Research Papers

- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- [Tree of Thoughts](https://arxiv.org/abs/2305.10601)
- [Self-Consistency](https://arxiv.org/abs/2203.11171)
- [Least-to-Most Prompting](https://arxiv.org/abs/2205.10625)

### Additional Resources

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Learn Prompting](https://learnprompting.org/)
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/claude/docs)

---

**Tài liệu này là một phần của Cursor Enterprise Framework Generator.**
