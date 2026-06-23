---
title: "Context Window Management - Quản Lý 1M Token Context"
description: "Hướng dẫn toàn diện về quản lý context window trong Gemini API, bao gồm strategies cho 1M token context, cách sử dụng context hiệu quả, sliding window approaches, và tối ưu hóa chi phí"
tags:
  - "gemini"
  - "context-window"
  - "token-management"
  - "1m-tokens"
  - "context-strategies"
  - "sliding-window"
  - "memory-management"
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Context Window Management - Quản Lý 1M Token Context

## Tổng Quan (Overview)

Context window là một trong những khía cạnh quan trọng nhất khi làm việc với Gemini API. Với khả năng xử lý lên đến 1 triệu tokens trong Gemini 2.0, đây là một lợi thế lớn so với nhiều mô hình khác. Tuy nhiên, việc quản lý context window một cách hiệu quả đòi hỏi sự hiểu biết sâu về cách Gemini sử dụng tokens, cách tối ưu hóa context, và các chiến lược để xử lý các use cases phức tạp.

Trong tài liệu này, chúng ta sẽ khám phá các khía cạnh kỹ thuật của context window management: từ cơ bản về cách tokens được tính và sử dụng, đến các chiến lược nâng cao như summarization, chunking, và hierarchical context. Chúng ta cũng sẽ xem xét các best practices cho production systems và cách xây dựng các patterns có thể tái sử dụng.

Context window không chỉ là về số lượng tokens - đó còn về cách tổ chức thông tin để model có thể hiểu và xử lý một cách hiệu quả. Một context 100K tokens được tổ chức tốt có thể hiệu quả hơn một context 500K tokens được tổ chức kém.

## Mục Đích (Purpose)

**1. Hiểu Rõ Cách Context Window Hoạt Động**

Cung cấp kiến thức chuyên sâu về cách Gemini xử lý context, cách tokens được tính cho different types of content, và cách context được sử dụng trong quá trình inference. Hiểu rõ cơ chế bên trong giúp developers đưa ra các quyết định tốt hơn về cách tổ chức context.

**2. Nắm Vững Các Chiến Lược Context Management**

Giới thiệu và giải thích chi tiết các chiến lược quản lý context: summarization, compression, chunking, hierarchical organization, và sliding window. Mỗi chiến lược có ưu điểm và nhược điểm riêng, phù hợp với các use cases khác nhau.

**3. Xây Dựng Production-Grade Context Management Systems**

Cung cấp các code patterns và architectures thực tế cho việc xây dựng các hệ thống quản lý context có thể mở rộng, dễ bảo trì, và hiệu quả về chi phí trong môi trường enterprise.

## Các Khái Niệm Cốt Lõi (Key Concepts)

### 1. Context Window Architecture

Context window là vùng nhớ nơi Gemini lưu trữ tất cả thông tin liên quan đến một cuộc hội thoại hoặc một yêu cầu. Với Gemini 2.0, context window lên đến 1 triệu tokens mang đến khả năng xử lý các documents dài, codebase lớn, và cuộc hội thoại phức tạp.

**Cấu trúc bên trong của Context Window:**

```
┌─────────────────────────────────────────────────────────────────┐
│                      CONTEXT WINDOW (1M Tokens)                  │
├─────────────────────────────────────────────────────────────────┤
│  SYSTEM          │  HISTORY           │  CONTEXT     │  RESPONSE │
│  INSTRUCTION     │  (Conversation)   │  (Document)  │  RESERVE  │
│  ~500 tokens     │  Variable          │  Variable    │  ~500-2K  │
└─────────────────────────────────────────────────────────────────┘
```

**Phân bổ tokens trong context:**

- **System Instruction**: Hướng dẫn cho model về cách xử lý (thường 100-1000 tokens)
- **Conversation History**: Lịch sử hội thoại (tùy thuộc vào độ dài cuộc trò chuyện)
- **Input Context**: Tài liệu, code, hoặc dữ liệu cần xử lý
- **Response Reserve**: Không gian dành cho output (thường 500-2000 tokens tùy use case)

```python
# src/context/context_allocator.py
"""
Context Allocator - Quản lý phân bổ context window
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class ContextSection(Enum):
    """Các phần của context window."""
    SYSTEM_INSTRUCTION = "system_instruction"
    CONVERSATION_HISTORY = "conversation_history"
    INPUT_CONTEXT = "input_context"
    OUTPUT_RESERVE = "output_reserve"


@dataclass
class ContextAllocation:
    """Kết quả phân bổ context."""
    section: ContextSection
    tokens: int
    content: str
    priority: int = 1  # 1-10, cao hơn = ưu tiên hơn


@dataclass
class ContextBudget:
    """Ngân sách tokens cho từng section."""
    total: int
    system_instruction_max: int = 1000
    conversation_history_max: int = 100000
    output_reserve_min: int = 500
    output_reserve_max: int = 4000
    
    def input_context_max(self) -> int:
        """Tính toán không gian tối đa cho input context."""
        return (
            self.total
            - self.system_instruction_max
            - self.conversation_history_max
            - self.output_reserve_min
        )


class ContextAllocator:
    """
    Allocator để phân bổ context window một cách hiệu quả.
    Đảm bảo các section quan trọng có đủ không gian.
    """
    
    def __init__(self, total_context: int = 1000000, model_name: str = "gemini-2.0-flash"):
        self.total_context = total_context
        self.model_name = model_name
        self.budget = ContextBudget(total_context)
        
        # Cache token counts
        self._token_counts: Dict[str, int] = {}
    
    def estimate_tokens(self, text: str) -> int:
        """
        Ước tính số tokens cho text.
        Sử dụng approximation: ~4 chars = 1 token.
        """
        if text in self._token_counts:
            return self._token_counts[text]
        
        # Approximate: 4 characters per token
        estimated = (len(text) + 3) // 4
        self._token_counts[text] = estimated
        return estimated
    
    def allocate(
        self,
        system_instruction: str,
        conversation_history: List[Dict[str, str]],
        input_context: str,
        expected_output_tokens: int = 1000
    ) -> Dict[ContextSection, ContextAllocation]:
        """
        Phân bổ context window cho các thành phần.
        
        Args:
            system_instruction: System prompt
            conversation_history: Lịch sử hội thoại [{role, content}]
            input_context: Document hoặc context chính
            expected_output_tokens: Ước tính output tokens
            
        Returns:
            Dict of allocations
        """
        allocations = {}
        
        # 1. System Instruction (ưu tiên cao)
        system_tokens = self.estimate_tokens(system_instruction)
        if system_tokens > self.budget.system_instruction_max:
            system_instruction = self.truncate(
                system_instruction,
                self.budget.system_instruction_max
            )
            system_tokens = self.budget.system_instruction_max
        
        allocations[ContextSection.SYSTEM_INSTRUCTION] = ContextAllocation(
            section=ContextSection.SYSTEM_INSTRUCTION,
            tokens=system_tokens,
            content=system_instruction,
            priority=10
        )
        
        # 2. Output Reserve (cố định)
        output_reserve = max(
            self.budget.output_reserve_min,
            min(expected_output_tokens, self.budget.output_reserve_max)
        )
        
        # 3. Conversation History (có thể truncate)
        history_text = self.format_history(conversation_history)
        history_tokens = self.estimate_tokens(history_text)
        
        # Nếu history quá lớn, truncate từ đầu (giữ messages gần đây nhất)
        if history_tokens > self.budget.conversation_history_max:
            history_text, history_tokens = self.truncate_history(
                conversation_history,
                self.budget.conversation_history_max
            )
        
        allocations[ContextSection.CONVERSATION_HISTORY] = ContextAllocation(
            section=ContextSection.CONVERSATION_HISTORY,
            tokens=history_tokens,
            content=history_text,
            priority=7
        )
        
        # 4. Input Context (sau khi đã reserve cho others)
        input_tokens = self.estimate_tokens(input_context)
        input_max = self.budget.input_context_max()
        
        if input_tokens > input_max:
            input_context = self.truncate(input_context, input_max)
            input_tokens = input_max
        
        allocations[ContextSection.INPUT_CONTEXT] = ContextAllocation(
            section=ContextSection.INPUT_CONTEXT,
            tokens=input_tokens,
            content=input_context,
            priority=5
        )
        
        # Tính tổng
        total_allocated = sum(a.tokens for a in allocations.values())
        
        return allocations
    
    def format_history(
        self,
        history: List[Dict[str, str]]
    ) -> str:
        """Format conversation history thành text."""
        lines = []
        for msg in history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            lines.append(f"{role.upper()}: {content}")
        return "\n".join(lines)
    
    def truncate_history(
        self,
        history: List[Dict[str, str]],
        max_tokens: int
    ) -> tuple[str, int]:
        """
        Truncate history từ đầu, giữ messages gần đây nhất.
        """
        # Estimate tokens per message (rough)
        avg_tokens_per_msg = 100
        
        # Calculate how many messages we can keep
        max_messages = max_tokens // avg_tokens_per_msg
        
        # Take the most recent messages
        recent_history = history[-max_messages:] if len(history) > max_messages else history
        
        text = self.format_history(recent_history)
        tokens = self.estimate_tokens(text)
        
        return text, tokens
    
    def truncate(self, text: str, max_tokens: int) -> str:
        """Truncate text để fit trong max_tokens."""
        max_chars = max_tokens * 4  # ~4 chars per token
        
        if len(text) <= max_chars:
            return text
        
        return text[:max_chars] + "\n\n[...truncated...]"
    
    def get_summary(self, allocations: Dict[ContextSection, ContextAllocation]) -> str:
        """Tạo summary của allocations."""
        lines = ["Context Allocation Summary:", "=" * 40]
        
        total = sum(a.tokens for a in allocations.values())
        
        for section, allocation in allocations.items():
            pct = (allocation.tokens / self.total_context) * 100
            lines.append(
                f"  {section.value}: {allocation.tokens:,} tokens ({pct:.1f}%)"
            )
        
        lines.append(f"\n  TOTAL: {total:,} tokens ({total/self.total_context*100:.1f}%)")
        lines.append(f"  REMAINING: {self.total_context - total:,} tokens")
        
        return "\n".join(lines)
```

### 2. Context Management Strategies

#### Strategy 1: Summarization (Tóm tắt)

Summarization là chiến lược phổ biến nhất để giảm context size. Thay vì giữ toàn bộ nội dung, ta tóm tắt và chỉ giữ thông tin quan trọng.

```python
# src/context/strategies/summarization.py
"""
Summarization Strategy - Tóm tắt context
"""

from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod


class Summarizer(ABC):
    """Abstract base class cho summarizers."""
    
    @abstractmethod
    def summarize(self, text: str, max_tokens: int) -> str:
        """Tóm tắt text thành max_tokens."""
        pass
    
    @abstractmethod
    def extract_key_points(self, text: str, max_points: int) -> List[str]:
        """Trích xuất các điểm chính từ text."""
        pass


class GeminiSummarizer(Summarizer):
    """
    Summarizer sử dụng Gemini để tóm tắt.
    """
    
    def __init__(self, model):
        self.model = model
    
    def summarize(self, text: str, max_tokens: int) -> str:
        """
        Tóm tắt text sử dụng Gemini.
        """
        prompt = f"""
Hãy tóm tắt nội dung sau thành khoảng {max_tokens} tokens.

Yêu cầu:
- Giữ các thông tin quan trọng nhất
- Sử dụng ngôn ngữ ngắn gọn
- Trình bày dưới dạng văn bản liền mạch
- Không dùng danh sách bullet points

NỘI DUNG:
{text}

TÓM TẮT:
"""
        response = self.model.generate_content(prompt)
        return response.text.strip()
    
    def extract_key_points(self, text: str, max_points: int = 5) -> List[str]:
        """
        Trích xuất các điểm chính từ text.
        """
        prompt = f"""
Phân tích nội dung sau và trích xuất {max_points} điểm chính quan trọng nhất.

Yêu cầu:
- Mỗi điểm không quá 2 câu
- Ưu tiên thông tin có giá trị thực tiễn
- Sắp xếp theo mức độ quan trọng giảm dần

NỘI DUNG:
{text}

CÁC ĐIỂM CHÍNH:
"""
        response = self.model.generate_content(prompt)
        
        # Parse response - extract lines starting with numbers
        lines = response.text.strip().split('\n')
        points = []
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove number/bullet prefix
                cleaned = line.lstrip('0123456789.- )').strip()
                points.append(cleaned)
        
        return points[:max_points]


class RecursiveSummarizer(Summarizer):
    """
    Recursive summarization - chia nhỏ, tóm tắt từng phần,
    rồi tóm tắt lại kết quả.
    """
    
    def __init__(
        self,
        base_summarizer: Summarizer,
        chunk_size: int = 10000,
        overlap: int = 500
    ):
        self.base_summarizer = base_summarizer
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def summarize(self, text: str, max_tokens: int) -> str:
        """
        Recursively summarize text.
        """
        # Base case: text is small enough
        estimated_tokens = (len(text) + 3) // 4
        if estimated_tokens <= max_tokens * 1.5:
            return self.base_summarizer.summarize(text, max_tokens)
        
        # Split into chunks
        chunks = self.split_into_chunks(text)
        
        # Summarize each chunk
        intermediate_summaries = []
        intermediate_max = max_tokens // len(chunks)
        
        for i, chunk in enumerate(chunks):
            summary = self.base_summarizer.summarize(chunk, intermediate_max)
            intermediate_summaries.append(summary)
        
        # Combine and summarize again
        combined = "\n\n".join(intermediate_summaries)
        return self.base_summarizer.summarize(combined, max_tokens)
    
    def extract_key_points(self, text: str, max_points: int = 5) -> List[str]:
        """
        Extract key points sử dụng recursive approach.
        """
        # Similar approach - split, extract, combine, extract again
        chunks = self.split_into_chunks(text)
        
        all_points = []
        points_per_chunk = max(2, max_points // len(chunks))
        
        for chunk in chunks:
            points = self.base_summarizer.extract_key_points(chunk, points_per_chunk)
            all_points.extend(points)
        
        # Combine all points and extract top ones
        combined_points = "\n".join(f"- {p}" for p in all_points)
        return self.base_summarizer.extract_key_points(combined_points, max_points)
    
    def split_into_chunks(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        chars_per_chunk = self.chunk_size * 4
        overlap_chars = self.overlap * 4
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chars_per_chunk
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence ending
                for sep in ['.\n', '.\n\n', '!\n', '?\n', ';\n']:
                    last_sep = text.rfind(sep, start + chars_per_chunk // 2, end)
                    if last_sep > start:
                        end = last_sep + len(sep)
                        break
            
            chunk = text[start:end]
            chunks.append(chunk)
            
            start = end - overlap_chars
        
        return chunks


class ContextSummarizer:
    """
    Context-aware summarizer cho conversation history.
    """
    
    def __init__(self, model, summarizer: Optional[Summarizer] = None):
        self.model = model
        self.summarizer = summarizer or GeminiSummarizer(model)
    
    def summarize_conversation(
        self,
        messages: List[Dict[str, str]],
        max_history_tokens: int
    ) -> Dict[str, any]:
        """
        Summarize conversation history.
        
        Returns:
            {
                'summary': str,
                'remaining_messages': List[Dict],
                'dropped_tokens': int
            }
        """
        if not messages:
            return {
                'summary': '',
                'remaining_messages': [],
                'dropped_tokens': 0
            }
        
        # Calculate current tokens
        total_chars = sum(len(m.get('content', '')) for m in messages)
        current_tokens = (total_chars + 3) // 4
        
        if current_tokens <= max_history_tokens:
            return {
                'summary': '',
                'remaining_messages': messages,
                'dropped_tokens': 0
            }
        
        # Need to summarize
        # Take messages from the middle (keep recent and oldest)
        messages_to_summarize = messages[1:-1]  # Skip first (system) and last (recent)
        
        if not messages_to_summarize:
            # Can't summarize - just truncate recent
            return {
                'summary': '',
                'remaining_messages': messages[-10:],  # Keep last 10
                'dropped_tokens': current_tokens - (max_history_tokens)
            }
        
        # Format messages for summarization
        history_text = self.format_messages(messages_to_summarize)
        
        # Estimate tokens needed for summary
        available_for_summary = max_history_tokens - (
            self.estimate_messages_tokens(messages[0]) +  # system
            self.estimate_messages_tokens(messages[-1])    # last message
        )
        
        # Summarize
        summary = self.summarizer.summarize(history_text, available_for_summary)
        summary_tokens = (len(summary) + 3) // 4
        
        # Return result
        return {
            'summary': f"[Earlier in conversation: {summary}]",
            'remaining_messages': [messages[0], {
                'role': 'user',
                'content': f"[Summarized: {summary}]"
            }, messages[-1]],
            'dropped_tokens': summary_tokens
        }
    
    def format_messages(self, messages: List[Dict[str, str]]) -> str:
        """Format messages thành text."""
        lines = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            lines.append(f"{role.upper()}: {content}")
        return "\n\n".join(lines)
    
    def estimate_messages_tokens(self, messages) -> int:
        """Estimate tokens cho messages."""
        if isinstance(messages, list):
            return sum(self.estimate_messages_tokens(m) for m in messages)
        return (len(str(messages)) + 3) // 4
```

#### Strategy 2: Hierarchical Context

Tổ chức context theo hierarchical structure, từ high-level overview đến detailed information.

```python
# src/context/strategies/hierarchical_context.py
"""
Hierarchical Context - Tổ chức context theo hierarchical structure
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class ContextNode:
    """Một node trong hierarchical context tree."""
    id: str
    level: int  # 0 = root, higher = more detailed
    title: str
    content: str
    tokens: int
    children: List["ContextNode"] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_all_tokens(self) -> int:
        """Tính tổng tokens bao gồm children."""
        total = self.tokens
        for child in self.children:
            total += child.get_all_tokens()
        return total


class HierarchicalContextBuilder:
    """
    Builder để tạo hierarchical context structure.
    """
    
    def __init__(self, model, max_tokens_per_level: Optional[Dict[int, int]] = None):
        self.model = model
        
        # Default max tokens per level
        self.max_tokens_per_level = max_tokens_per_level or {
            0: 500,    # Root overview
            1: 2000,   # Main sections
            2: 8000,   # Subsections
            3: 32000,  # Details
        }
    
    def build_from_document(
        self,
        document: str,
        structure: str = "auto"
    ) -> ContextNode:
        """
        Build hierarchical context từ document.
        
        Args:
            document: Document text
            structure: 'auto' để Gemini quyết định, hoặc specify structure
            
        Returns:
            Root ContextNode
        """
        if structure == "auto":
            return self._build_auto(document)
        else:
            return self._build_with_structure(document, structure)
    
    def _build_auto(self, document: str) -> ContextNode:
        """Automatically determine structure và build hierarchy."""
        
        # Step 1: Identify main sections
        sections_prompt = f"""
Phân tích document sau và trả về cấu trúc chính dưới dạng JSON.

Trả về format:
{{
  "title": "Tên document",
  "sections": [
    {{
      "title": "Tên section 1",
      "summary": "Tóm tắt 1-2 câu về section này",
      "key_points": ["Điểm quan trọng 1", "Điểm quan trọng 2"]
    }}
  ]
}}

Chỉ trả về JSON, không giải thích gì thêm.

DOCUMENT:
{document[:10000]}...
"""
        
        response = self.model.generate_content(sections_prompt)
        
        import json
        try:
            structure = json.loads(response.text)
        except:
            # Fallback nếu JSON parse fails
            structure = {
                "title": "Document",
                "sections": [{"title": "Main", "summary": document[:500]}]
            }
        
        # Build root node
        root = ContextNode(
            id="root",
            level=0,
            title=structure.get("title", "Document"),
            content=structure.get("title", "Document"),
            tokens=100
        )
        
        # Build section nodes
        for i, section in enumerate(structure.get("sections", [])):
            section_node = ContextNode(
                id=f"section_{i}",
                level=1,
                title=section.get("title", f"Section {i+1}"),
                content=f"{section.get('summary', '')}\n\nKey Points:\n" +
                        "\n".join(f"- {p}" for p in section.get('key_points', [])),
                tokens=len(section.get('summary', '')) // 4 + 200
            )
            root.children.append(section_node)
        
        return root
    
    def _build_with_structure(self, document: str, structure: str) -> ContextNode:
        """Build với structure được chỉ định."""
        # Parse structure specification
        # Format: "Title > Section1 > Subsection > ..."
        parts = [p.strip() for p in structure.split('>')]
        
        root = ContextNode(
            id="root",
            level=0,
            title=parts[0],
            content=parts[0],
            tokens=100
        )
        
        # Add subsequent levels as children
        current = root
        for i, part in enumerate(parts[1:], 1):
            child = ContextNode(
                id=f"level_{i}",
                level=i,
                title=part,
                content="",
                tokens=0
            )
            current.children.append(child)
            current = child
        
        return root
    
    def flatten_for_context(
        self,
        node: ContextNode,
        max_tokens: int
    ) -> str:
        """
        Flatten hierarchical structure thành text cho context.
        Giới hạn bởi max_tokens.
        """
        lines = []
        current_tokens = 0
        
        def add_node(n: ContextNode, prefix: str = ""):
            nonlocal current_tokens
            
            # Calculate tokens cho this node và its content
            node_text = f"{prefix}{n.title}\n{n.content}\n\n"
            node_tokens = (len(node_text) + 3) // 4
            
            if current_tokens + node_tokens > max_tokens:
                # Can't fit this node fully
                remaining = max_tokens - current_tokens
                if remaining > 100:  # Can fit at least a summary
                    lines.append(f"{prefix}{n.title}\n[...truncated...]\n")
                return False
            
            lines.append(node_text)
            current_tokens += node_tokens
            
            # Add children
            for child in n.children:
                new_prefix = prefix + "## "
                if not add_node(child, new_prefix):
                    break
            
            return True
        
        # Start with root
        lines.append(f"# {node.title}\n\n")
        current_tokens = (len(lines[0]) + 3) // 4
        
        for child in node.children:
            add_node(child, "## ")
        
        return "".join(lines)
    
    def expand_node(
        self,
        node: ContextNode,
        full_content: Dict[str, str]
    ) -> ContextNode:
        """
        Expand a node với full content từ source.
        """
        if node.id in full_content:
            node.content = full_content[node.id]
            node.tokens = (len(node.content) + 3) // 4
        
        for child in node.children:
            self.expand_node(child, full_content)
        
        return node


class SemanticChunker:
    """
    Chunk documents dựa trên semantic boundaries.
    """
    
    def __init__(self, model):
        self.model = model
    
    def chunk_by_semantics(
        self,
        document: str,
        chunk_size: int = 8000,
        overlap: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Chunk document dựa trên semantic boundaries.
        """
        # Step 1: Identify semantic chunks using Gemini
        identify_prompt = f"""
Phân tích document sau và chia thành các phần semantic.

Mỗi phần nên:
- Có một chủ đề hoặc ý chính rõ ràng
- Có thể đứng độc lập (ít phụ thuộc vào phần khác)
- Độ dài từ 1000-8000 tokens

Trả về format JSON:
{{
  "chunks": [
    {{
      "title": "Tên phần",
      "start": "Vị trí bắt đầu (0-based)",
      "end": "Vị trí kết thúc",
      "summary": "Tóm tắt 1-2 câu"
    }}
  ]
}}

DOCUMENT:
{document[:30000]}...
"""
        
        response = self.model.generate_content(identify_prompt)
        
        import json
        try:
            chunk_info = json.loads(response.text)
            chunks_data = chunk_info.get("chunks", [])
        except:
            # Fallback to simple chunking
            chunks_data = self._simple_chunk(document, chunk_size, overlap)
        
        # Step 2: Extract actual content for each chunk
        chunks = []
        for chunk_data in chunks_data:
            start = chunk_data.get("start", 0)
            end = chunk_data.get("end", min(start + chunk_size, len(document)))
            
            content = document[start:end]
            
            chunks.append({
                "title": chunk_data.get("title", f"Chunk {len(chunks)+1}"),
                "content": content.strip(),
                "start": start,
                "end": end,
                "summary": chunk_data.get("summary", ""),
                "tokens": (len(content) + 3) // 4
            })
        
        return chunks
    
    def _simple_chunk(
        self,
        document: str,
        chunk_size: int,
        overlap: int
    ) -> List[Dict]:
        """Simple character-based chunking as fallback."""
        chunks = []
        chars_per_chunk = chunk_size * 4
        chars_overlap = overlap * 4
        
        start = 0
        i = 1
        while start < len(document):
            end = min(start + chars_per_chunk, len(document))
            
            chunks.append({
                "title": f"Part {i}",
                "start": start,
                "end": end,
                "summary": document[start:min(start+200, end)]
            })
            
            start = end - chars_overlap
            i += 1
        
        return chunks
```

#### Strategy 3: Sliding Window Approach

Sử dụng sliding window để xử lý các documents hoặc conversations dài.

```python
# src/context/strategies/sliding_window.py
"""
Sliding Window Strategy - Xử lý context dài với sliding window
"""

from typing import List, Iterator, Dict, Any, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class WindowSlice:
    """Một slice của sliding window."""
    index: int
    content: str
    tokens: int
    metadata: Dict[str, Any]
    
    def __repr__(self) -> str:
        return f"WindowSlice(index={self.index}, tokens={self.tokens})"


class SlidingWindow:
    """
    Sliding window implementation cho context processing.
    """
    
    def __init__(
        self,
        window_size: int = 32000,
        step_size: int = 16000,
        overlap_tokens: int = 2000
    ):
        self.window_size = window_size
        self.step_size = step_size
        self.overlap_tokens = overlap_tokens
        
        # Cache
        self._windows: Optional[List[WindowSlice]] = None
        self._source_text: Optional[str] = None
    
    def create_windows(self, text: str) -> List[WindowSlice]:
        """
        Tạo các windows từ text.
        """
        if self._source_text == text and self._windows is not None:
            return self._windows
        
        chars_per_window = self.window_size * 4
        chars_per_step = self.step_size * 4
        chars_overlap = self.overlap_tokens * 4
        
        windows = []
        start = 0
        index = 0
        
        while start < len(text):
            end = min(start + chars_per_window, len(text))
            
            # Try to break at semantic boundary
            if end < len(text):
                end = self._find_break_point(text, start, end)
            
            content = text[start:end]
            
            windows.append(WindowSlice(
                index=index,
                content=content,
                tokens=(len(content) + 3) // 4,
                metadata={
                    "start_char": start,
                    "end_char": end,
                    "start_token": start // 4,
                    "end_token": end // 4
                }
            ))
            
            start = end - chars_overlap
            index += 1
        
        self._windows = windows
        self._source_text = text
        
        return windows
    
    def _find_break_point(self, text: str, start: int, end: int) -> int:
        """Tìm điểm break tốt nhất (sentence/paragraph boundary)."""
        # Look for paragraph break first
        for sep in ['\n\n', '\n', '. ', '! ', '? ']:
            # Search backwards from end
            search_start = max(start, end - 200)
            pos = text.rfind(sep, search_start, end)
            
            if pos > start:
                return pos + len(sep)
        
        return end
    
    def iter_windows(self, text: str) -> Iterator[WindowSlice]:
        """Iterate qua các windows."""
        windows = self.create_windows(text)
        for window in windows:
            yield window
    
    def get_context_with_neighbors(
        self,
        text: str,
        target_index: int,
        num_neighbors: int = 1
    ) -> str:
        """
        Get window với context từ neighboring windows.
        """
        windows = self.create_windows(text)
        
        if target_index < 0 or target_index >= len(windows):
            raise ValueError(f"Invalid window index: {target_index}")
        
        # Collect windows
        start_idx = max(0, target_index - num_neighbors)
        end_idx = min(len(windows), target_index + num_neighbors + 1)
        
        parts = []
        for i in range(start_idx, end_idx):
            if i == target_index:
                parts.append(f"=== WINDOW {i} (CURRENT) ===\n{windows[i].content}\n")
            else:
                parts.append(f"=== WINDOW {i} ===\n{windows[i].content}\n")
        
        return "\n".join(parts)


class ProcessingPipeline:
    """
    Pipeline để process sliding windows với Gemini.
    """
    
    def __init__(
        self,
        model,
        window_size: int = 32000,
        step_size: int = 16000
    ):
        self.model = model
        self.sliding_window = SlidingWindow(
            window_size=window_size,
            step_size=step_size
        )
    
    def process_document(
        self,
        document: str,
        process_fn: Callable[[str], str],
        aggregate_fn: Optional[Callable[[List[str]], str]] = None,
        show_progress: bool = True
    ) -> str:
        """
        Process entire document bằng cách chunking và aggregate.
        
        Args:
            document: Document text
            process_fn: Function để process mỗi window
            aggregate_fn: Function để aggregate results
            show_progress: Show progress bar
            
        Returns:
            Aggregated result
        """
        windows = self.sliding_window.create_windows(document)
        
        if show_progress:
            print(f"Processing {len(windows)} windows...")
        
        results = []
        
        for i, window in enumerate(windows):
            if show_progress:
                print(f"  Window {i+1}/{len(windows)}: {window.tokens} tokens")
            
            # Process window
            result = process_fn(window.content)
            results.append({
                "index": i,
                "window": window,
                "result": result
            })
        
        # Aggregate results
        if aggregate_fn:
            final_result = aggregate_fn([r["result"] for r in results])
        else:
            final_result = "\n\n".join(r["result"] for r in results)
        
        return final_result
    
    def query_with_context(
        self,
        document: str,
        query: str,
        context_size: int = 3
    ) -> Dict[str, Any]:
        """
        Query document với sliding window context.
        """
        # Find relevant windows using token-based search
        windows = self.sliding_window.create_windows(document)
        
        # Simple relevance scoring
        query_lower = query.lower()
        
        scored_windows = []
        for window in windows:
            # Count query term matches
            score = sum(1 for term in query_lower.split() 
                       if term in window.content.lower())
            scored_windows.append((score, window))
        
        # Sort by score
        scored_windows.sort(key=lambda x: x[0], reverse=True)
        
        # Get top windows
        top_windows = scored_windows[:context_size]
        top_windows.sort(key=lambda x: x[1].index)  # Sort by position
        
        # Build context
        context_parts = []
        for score, window in top_windows:
            context_parts.append(
                f"[Position {window.index} - {score} relevant mentions]:\n{window.content}"
            )
        
        full_context = "\n\n".join(context_parts)
        
        # Query
        prompt = f"""
Based on the following context from a document, answer the query.

CONTEXT:
{full_context}

QUERY: {query}

ANSWER:
"""
        
        response = self.model.generate_content(prompt)
        
        return {
            "answer": response.text,
            "windows_used": [w.index for _, w in top_windows],
            "total_tokens": sum(w.tokens for _, w in top_windows)
        }
    
    def extract_by_sliding_window(
        self,
        document: str,
        extraction_prompt: str
    ) -> List[Dict[str, Any]]:
        """
        Extract information từ document sử dụng sliding window.
        """
        windows = self.sliding_window.create_windows(document)
        
        results = []
        
        for window in windows:
            prompt = f"""
{extrraction_prompt}

DOCUMENT WINDOW (position {window.index}):
{window.content}

Extract relevant information. Return JSON format with your findings.
"""
            
            response = self.model.generate_content(prompt)
            
            try:
                import json
                extraction = json.loads(response.text)
                results.append({
                    "window_index": window.index,
                    "data": extraction
                })
            except:
                # Non-JSON response
                results.append({
                    "window_index": window.index,
                    "data": {"raw": response.text}
                })
        
        return results
```

## Best Practices

### 1. Efficient Context Usage

```python
# Best practices cho context management

class EfficientContextManager:
    """Best practices implementation."""
    
    @staticmethod
    def optimize_system_prompt(prompt: str) -> str:
        """
        Tối ưu system prompt:
        - Remove redundant instructions
        - Use concise language
        - Organize with clear sections
        """
        # Remove common filler phrases
        filler_phrases = [
            "Please ",
            "I want you to ",
            "You are a ",
            "As an AI, ",
        ]
        
        result = prompt
        for phrase in filler_phrases:
            result = result.replace(phrase, "")
        
        return result.strip()
    
    @staticmethod
    def structure_conversation_history(
        messages: List[Dict],
        max_tokens: int
    ) -> List[Dict]:
        """
        Structure conversation history hiệu quả:
        - Keep recent messages fully
        - Summarize older messages
        - Remove redundant acknowledgments
        """
        if not messages:
            return []
        
        # Calculate available tokens
        total_chars = sum(len(m.get('content', '')) for m in messages)
        current_tokens = (total_chars + 3) // 4
        
        if current_tokens <= max_tokens:
            return messages
        
        # Priority: keep last 2-3 exchanges fully
        # Summarize middle messages
        recent_messages = messages[-6:]  # Keep last 6 messages
        older_messages = messages[1:-6]  # Skip system, summarize rest
        
        if older_messages:
            # Create summary of older messages
            summary_text = "\n".join(
                f"{m.get('role', 'user')}: {m.get('content', '')[:200]}"
                for m in older_messages
            )
            
            return [
                messages[0],  # System
                {"role": "user", "content": f"[Earlier conversation summary]"},
                *recent_messages
            ]
        
        return [messages[0]] + recent_messages
    
    @staticmethod
    def cache_frequently_used_context(
        context: str,
        cache: Dict[str, Any],
        ttl_seconds: int = 3600
    ) -> str:
        """
        Cache frequently used context (e.g., documentation, system rules).
        """
        import hashlib
        import time
        
        cache_key = hashlib.md5(context.encode()).hexdigest()
        
        if cache_key in cache:
            cached = cache[cache_key]
            if time.time() - cached['timestamp'] < ttl_seconds:
                return cached['content']
        
        cache[cache_key] = {
            'content': context,
            'timestamp': time.time()
        }
        
        return context
```

### 2. Context Organization Patterns

```python
# Patterns cho context organization

class ContextPatterns:
    """Các patterns để tổ chức context hiệu quả."""
    
    # Pattern 1: Structured Document Format
    DOCUMENT_TEMPLATE = """
# Document: {title}

## Summary
{summary}

## Main Sections
{section_titles}

## Content
{content}
"""
    
    # Pattern 2: Conversation Summary Format
    CONVERSATION_TEMPLATE = """
## Conversation Summary
Topics discussed: {topics}
Key decisions: {decisions}
Outstanding items: {outstanding}

## Recent Exchange
{recent_messages}

## User Intent
{current_intent}
"""
    
    # Pattern 3: Code Context Format
    CODE_CONTEXT_TEMPLATE = """
## Code Context
File: {file_path}
Language: {language}
Framework: {framework}

## Imports/Dependencies
{imports}

## Related Files
{related_files}

## Current Code
```{language}
{code}
```
"""
```

### 3. Token Budgeting Strategies

```python
# Token budgeting strategies

class TokenBudget:
    """Quản lý token budget cho context."""
    
    def __init__(self, total_limit: int = 1000000):
        self.total_limit = total_limit
        self.reserved = {}
    
    def reserve(
        self,
        purpose: str,
        tokens: int,
        priority: int = 1
    ) -> bool:
        """
        Reserve tokens cho một purpose cụ thể.
        
        Returns:
            True nếu reservation thành công
        """
        total_reserved = sum(self.reserved.values())
        
        if total_reserved + tokens > self.total_limit:
            return False
        
        self.reserved[purpose] = tokens
        return True
    
    def get_available(self, purpose: Optional[str] = None) -> int:
        """
        Get available tokens.
        """
        total_reserved = sum(self.reserved.values())
        
        if purpose and purpose in self.reserved:
            total_reserved -= self.reserved[purpose]
        
        return self.total_limit - total_reserved
    
    def allocate(
        self,
        needs: Dict[str, int],
        priorities: Optional[Dict[str, int]] = None
    ) -> Dict[str, int]:
        """
        Allocate tokens cho multiple needs dựa trên priorities.
        """
        if priorities is None:
            priorities = {k: 1 for k in needs.keys()}
        
        # Sort by priority
        sorted_needs = sorted(
            needs.items(),
            key=lambda x: priorities.get(x[0], 1),
            reverse=True
        )
        
        allocations = {}
        available = self.get_available()
        
        for purpose, requested in sorted_needs:
            allocated = min(requested, available // (len(sorted_needs) - len(allocations)))
            allocations[purpose] = allocated
            available -= allocated
        
        return allocations
```

## Common Patterns

### 1. Long Document Q&A System

```python
# src/pipelines/long_document_qa.py
"""
Long Document Q&A System với context management
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import hashlib


@dataclass
class DocumentIndex:
    """Index cho document chunks."""
    chunk_id: str
    content: str
    tokens: int
    summary: str
    position: int


class LongDocumentQASystem:
    """
    System để answer questions về long documents.
    Sử dụng hierarchical context và smart retrieval.
    """
    
    def __init__(self, model):
        self.model = model
        self.sliding_window = SlidingWindow(window_size=32000, step_size=24000)
        self.summarizer = RecursiveSummarizer(
            GeminiSummarizer(model),
            chunk_size=32000
        )
        
        # Index for retrieval
        self.chunks: List[DocumentIndex] = []
        self.document_hash: Optional[str] = None
    
    def index_document(self, document: str) -> None:
        """
        Index document để prepare cho querying.
        """
        import hashlib
        
        # Check if already indexed
        current_hash = hashlib.md5(document.encode()).hexdigest()
        if current_hash == self.document_hash:
            return
        
        self.document_hash = current_hash
        
        # Create chunks
        windows = self.sliding_window.create_windows(document)
        
        self.chunks = []
        for i, window in enumerate(windows):
            # Generate summary for each chunk
            summary = self.summarizer.summarize(
                window.content,
                max_tokens=200
            )
            
            self.chunks.append(DocumentIndex(
                chunk_id=f"chunk_{i}",
                content=window.content,
                tokens=window.tokens,
                summary=summary,
                position=i
            ))
    
    def answer_question(
        self,
        document: str,
        question: str,
        max_context_tokens: int = 50000
    ) -> Dict[str, any]:
        """
        Answer question about document.
        """
        # Index if needed
        self.index_document(document)
        
        # Find relevant chunks
        relevant_chunks = self._find_relevant_chunks(question)
        
        # Build context from relevant chunks
        context, tokens_used = self._build_context(
            relevant_chunks,
            max_context_tokens
        )
        
        # Generate answer
        prompt = f"""
Dựa trên nội dung tài liệu sau, hãy trả lời câu hỏi một cách chi tiết và chính xác.

Nếu câu trả lời không có trong tài liệu, hãy nói rõ điều đó.

NỘI DUNG TÀI LIỆU:
{context}

CÂU HỎI: {question}

TRẢ LỜI:
"""
        
        response = self.model.generate_content(prompt)
        
        return {
            "answer": response.text,
            "chunks_used": len(relevant_chunks),
            "tokens_used": tokens_used,
            "chunk_positions": [c.position for c in relevant_chunks]
        }
    
    def _find_relevant_chunks(self, query: str, top_k: int = 5) -> List[DocumentIndex]:
        """Find chunks relevant to query."""
        # Simple keyword matching (in production, use embeddings)
        query_terms = set(query.lower().split())
        
        scored_chunks = []
        for chunk in self.chunks:
            # Count matching terms in content
            content_lower = chunk.content.lower()
            score = sum(1 for term in query_terms if term in content_lower)
            
            # Also check summary
            summary_lower = chunk.summary.lower()
            score += sum(2 for term in query_terms if term in summary_lower)
            
            scored_chunks.append((score, chunk))
        
        # Sort and return top k
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [chunk for _, chunk in scored_chunks[:top_k]]
    
    def _build_context(
        self,
        chunks: List[DocumentIndex],
        max_tokens: int
    ) -> tuple[str, int]:
        """Build context string từ chunks."""
        parts = []
        total_tokens = 0
        
        for chunk in chunks:
            chunk_text = f"[Phần {chunk.position + 1}]\n{chunk.content}\n"
            chunk_tokens = chunk.tokens
            
            if total_tokens + chunk_tokens > max_tokens:
                break
            
            parts.append(chunk_text)
            total_tokens += chunk_tokens
        
        return "\n".join(parts), total_tokens
```

### 2. Multi-Turn Conversation Manager

```typescript
// src/context/conversation-manager.ts
/**
 * Conversation Manager với context optimization (TypeScript)
 */

import { Content, Part } from '@google/generative-ai';

interface Message {
  role: 'user' | 'model';
  parts: Part[];
  tokens?: number;
}

interface ConversationState {
  messages: Message[];
  summary: string;
  totalTokens: number;
}

interface TokenBudget {
  systemPrompt: number;
  summary: number;
  history: number;
  currentInput: number;
  responseReserve: number;
}

export class ConversationManager {
  private model: ReturnType<GoogleGenerativeAI['getGenerativeModel']>;
  private maxContextTokens: number;
  private tokenBudget: TokenBudget;
  
  constructor(
    model: ReturnType<GoogleGenerativeAI['getGenerativeModel']>,
    maxContextTokens: number = 1000000
  ) {
    this.model = model;
    this.maxContextTokens = maxContextTokens;
    
    // Default budget allocation
    this.tokenBudget = {
      systemPrompt: 500,
      summary: 2000,
      history: 50000,
      currentInput: 10000,
      responseReserve: 2000,
    };
  }
  
  /**
   * Build context cho request
   */
  async buildContext(
    systemPrompt: string,
    messages: Message[],
    currentInput: Part[]
  ): Promise<Content> {
    // Calculate available tokens for history
    const currentInputTokens = await this.countTokens(currentInput);
    const systemPromptTokens = await this.countTokens([{ text: systemPrompt }]);
    
    const reservedTokens = 
      systemPromptTokens + 
      this.tokenBudget.summary + 
      currentInputTokens + 
      this.tokenBudget.responseReserve;
    
    const availableForHistory = this.maxContextTokens - reservedTokens;
    
    // Optimize history
    const optimizedHistory = this.optimizeHistory(
      messages,
      availableForHistory
    );
    
    // Build content parts
    const content: Content = {
      role: 'user',
      parts: [
        { text: systemPrompt },
        ...optimizedHistory.map(m => m.parts).flat(),
        ...currentInput,
      ],
    };
    
    return content;
  }
  
  /**
   * Optimize conversation history within token budget
   */
  private optimizeHistory(
    messages: Message[],
    maxTokens: number
  ): Message[] {
    if (!messages.length) return [];
    
    // Calculate total tokens
    const totalTokens = messages.reduce(
      (sum, m) => sum + (m.tokens || 0),
      0
    );
    
    if (totalTokens <= maxTokens) {
      return messages;
    }
    
    // Strategy: Keep recent messages fully, summarize older ones
    const recentMessages = this.getRecentMessages(messages, maxTokens / 2);
    const olderMessages = messages.slice(0, -recentMessages.length);
    
    if (olderMessages.length > 0) {
      // Summarize older messages
      const summary = this.summarizeMessages(olderMessages);
      return [
        {
          role: 'user',
          parts: [{ text: `[Earlier conversation summary]: ${summary}` }],
          tokens: Math.ceil(summary.length / 4),
        },
        ...recentMessages,
      ];
    }
    
    return recentMessages;
  }
  
  /**
   * Get recent messages that fit within token budget
   */
  private getRecentMessages(
    messages: Message[],
    maxTokens: number
  ): Message[] {
    const result: Message[] = [];
    let totalTokens = 0;
    
    // Go backwards through messages
    for (let i = messages.length - 1; i >= 0; i--) {
      const msgTokens = messages[i].tokens || Math.ceil(
        messages[i].parts.map(p => 'text' in p ? p.text : '').join('').length / 4
      );
      
      if (totalTokens + msgTokens > maxTokens) {
        break;
      }
      
      result.unshift(messages[i]);
      totalTokens += msgTokens;
    }
    
    return result;
  }
  
  /**
   * Summarize old messages
   */
  private summarizeMessages(messages: Message[]): string {
    // In production, call Gemini to summarize
    // For now, return simple concatenation
    return messages
      .map(m => `${m.role}: ${m.parts.map(p => 'text' in p ? p.text : '').join('')}`)
      .join('\n')
      .substring(0, 1000);
  }
  
  /**
   * Count tokens
   */
  private async countTokens(parts: Part[]): Promise<number> {
    const result = await this.model.countTokens({ contents: [{ role: 'user', parts }] });
    return result.totalTokens;
  }
  
  /**
   * Update token budget
   */
  setBudget(budget: Partial<TokenBudget>): void {
    this.tokenBudget = { ...this.tokenBudget, ...budget };
  }
}
```

## Examples

### 1. Complete Context Management System - Python

```python
# src/examples/context_management.py
"""
Complete Context Management System Example
"""

import os
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from google.generativeai import GenerativeModel
from src.config.gemini_config import GeminiConfig, initialize_gemini, create_model
from src.context.context_allocator import ContextAllocator
from src.context.strategies.summarization import (
    ContextSummarizer, 
    RecursiveSummarizer,
    GeminiSummarizer
)
from src.context.strategies.sliding_window import SlidingWindow


@dataclass
class QueryResult:
    """Kết quả từ query."""
    answer: str
    tokens_used: int
    chunks_processed: int
    processing_time_ms: float


class ContextAwareQASystem:
    """
    Complete Q&A system với context management.
    """
    
    def __init__(
        self,
        config: Optional[GeminiConfig] = None,
        context_limit: int = 1000000
    ):
        # Initialize Gemini
        if config is None:
            config = GeminiConfig.from_env()
        initialize_gemini(config)
        self.model = create_model(config)
        
        # Initialize context management components
        self.context_allocator = ContextAllocator(
            total_context=context_limit,
            model_name=config.model_name
        )
        self.summarizer = RecursiveSummarizer(
            GeminiSummarizer(self.model)
        )
        self.sliding_window = SlidingWindow(
            window_size=32000,
            step_size=24000
        )
        self.context_summarizer = ContextSummarizer(self.model)
        
        # State
        self.conversation_history: List[Dict[str, str]] = []
        self.document_cache: Dict[str, Any] = {}
    
    def query_document(
        self,
        document: str,
        question: str,
        conversation_id: Optional[str] = None
    ) -> QueryResult:
        """
        Query a document với automatic context management.
        """
        import time
        start_time = time.time()
        
        # Index document
        if conversation_id and conversation_id in self.document_cache:
            chunks = self.document_cache[conversation_id]
        else:
            windows = self.sliding_window.create_windows(document)
            chunks = [
                {
                    "content": w.content,
                    "tokens": w.tokens,
                    "position": w.index
                }
                for w in windows
            ]
            
            if conversation_id:
                self.document_cache[conversation_id] = chunks
        
        # Find relevant chunks
        relevant_chunks = self._find_relevant_chunks(chunks, question)
        
        # Build context
        context_text = "\n\n".join(
            f"[Section {c['position'] + 1}]:\n{c['content']}"
            for c in relevant_chunks
        )
        
        # Count tokens
        total_tokens = sum(c['tokens'] for c in relevant_chunks)
        
        # Add conversation history if exists
        history_summary = ""
        if self.conversation_history:
            history_result = self.context_summarizer.summarize_conversation(
                self.conversation_history,
                max_history_tokens=5000
            )
            history_summary = history_result['summary']
        
        # Build full prompt
        prompt_parts = []
        
        if history_summary:
            prompt_parts.append(f"Previous conversation:\n{history_summary}\n\n")
        
        prompt_parts.extend([
            f"Based on the following document sections, answer the question.\n\n",
            f"DOCUMENT SECTIONS:\n{context_text}\n\n",
            f"QUESTION: {question}\n\n",
            f"ANSWER:"
        ])
        
        full_prompt = "".join(prompt_parts)
        
        # Generate response
        response = self.model.generate_content(full_prompt)
        
        # Update conversation history
        self.conversation_history.extend([
            {"role": "user", "content": question},
            {"role": "model", "content": response.text}
        ])
        
        # Keep history manageable
        if len(self.conversation_history) > 50:
            result = self.context_summarizer.summarize_conversation(
                self.conversation_history,
                max_history_tokens=10000
            )
            if result['summary']:
                self.conversation_history = [
                    {"role": "user", "content": result['summary']},
                    self.conversation_history[-2],
                    self.conversation_history[-1]
                ]
        
        processing_time = (time.time() - start_time) * 1000
        
        return QueryResult(
            answer=response.text,
            tokens_used=total_tokens,
            chunks_processed=len(relevant_chunks),
            processing_time_ms=processing_time
        )
    
    def _find_relevant_chunks(
        self,
        chunks: List[Dict],
        question: str,
        max_chunks: int = 10
    ) -> List[Dict]:
        """Find chunks relevant to question."""
        question_lower = question.lower()
        question_terms = set(question_lower.split())
        
        scored_chunks = []
        for chunk in chunks:
            content_lower = chunk['content'].lower()
            
            # Score based on term frequency
            score = sum(1 for term in question_terms if term in content_lower)
            
            # Bonus for terms appearing in first 500 chars
            first_part = content_lower[:2000]
            score += sum(1 for term in question_terms if term in first_part)
            
            scored_chunks.append((score, chunk))
        
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        # Take top chunks, but preserve order
        top_chunks = scored_chunks[:max_chunks]
        top_chunks.sort(key=lambda x: x[1]['position'])
        
        return [c for _, c in top_chunks]
    
    def reset_conversation(self) -> None:
        """Reset conversation state."""
        self.conversation_history = []
    
    def clear_document_cache(self) -> None:
        """Clear document cache."""
        self.document_cache = {}


async def main():
    """Example usage."""
    
    # Initialize system
    system = ContextAwareQASystem()
    
    # Sample document (long)
    sample_document = """
[This would be a very long document - for demonstration purposes]
""" * 1000
    
    # First query
    print("Query 1: What is the main topic?")
    result1 = system.query_document(
        document=sample_document,
        question="What is the main topic of this document?",
        conversation_id="doc_001"
    )
    print(f"Answer: {result1.answer[:200]}...")
    print(f"Tokens: {result1.tokens_used}, Chunks: {result1.chunks_processed}")
    print()
    
    # Follow-up query (uses conversation history)
    print("Query 2: Can you elaborate on that?")
    result2 = system.query_document(
        document=sample_document,
        question="Can you elaborate on that point?",
        conversation_id="doc_001"
    )
    print(f"Answer: {result2.answer[:200]}...")
    print(f"Tokens: {result2.tokens_used}, Chunks: {result2.chunks_processed}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### 2. Streaming Response with Context Management

```typescript
// src/examples/context-streaming.ts
/**
 * Streaming response với context management (TypeScript)
 */

import { GoogleGenerativeAI, Part, GenerateContentStreamResult } from '@google/generative-ai';

interface StreamingOptions {
  maxContextTokens: number;
  includeHistory: boolean;
  historyTokens: number;
}

export class StreamingContextSystem {
  private client: GoogleGenerativeAI;
  private model: ReturnType<GoogleGenerativeAI['getGenerativeModel']>;
  private conversationHistory: Array<{ role: string; content: string }> = [];
  
  constructor(apiKey: string, modelName: string = 'gemini-2.0-flash') {
    this.client = new GoogleGenerativeAI(apiKey);
    this.model = this.client.getGenerativeModel({ model: modelName });
  }
  
  /**
   * Stream response với context management
   */
  async *streamWithContext(
    prompt: string,
    options: Partial<StreamingOptions> = {}
  ): AsyncGenerator<string> {
    const opts: StreamingOptions = {
      maxContextTokens: options.maxContextTokens ?? 1000000,
      includeHistory: options.includeHistory ?? true,
      historyTokens: options.historyTokens ?? 10000,
    };
    
    // Build context
    const contextParts = await this.buildContext(prompt, opts);
    
    // Stream response
    const result: GenerateContentStreamResult = 
      await this.model.generateContentStream(contextParts);
    
    for await (const chunk of result.stream) {
      const text = chunk.text();
      yield text;
      
      // Accumulate response
      this.conversationHistory.push({
        role: 'user',
        content: prompt,
      });
      this.conversationHistory.push({
        role: 'model',
        content: chunk.text(),
      });
    }
    
    // Prune history if needed
    this.pruneHistory(opts.historyTokens);
  }
  
  /**
   * Build context with history management
   */
  private async buildContext(
    prompt: string,
    options: StreamingOptions
  ): Promise<Part[]> {
    const parts: Part[] = [];
    
    if (options.includeHistory && this.conversationHistory.length > 0) {
      // Add history summary
      const historyText = this.conversationHistory
        .map(m => `${m.role}: ${m.content}`)
        .join('\n');
      
      // Check if history fits
      const historyTokens = Math.ceil(historyText.length / 4);
      
      if (historyTokens > options.historyTokens) {
        // Summarize older history
        const summary = await this.summarizeHistory(options.historyTokens);
        parts.push({
          text: `Previous conversation summary:\n${summary}\n\n`,
        });
      } else {
        parts.push({
          text: `Conversation history:\n${historyText}\n\n`,
        });
      }
    }
    
    // Add current prompt
    parts.push({ text: prompt });
    
    return parts;
  }
  
  /**
   * Summarize conversation history
   */
  private async summarizeHistory(maxTokens: number): Promise<string> {
    if (this.conversationHistory.length <= 4) {
      return this.conversationHistory
        .map(m => `${m.role}: ${m.content}`)
        .join('\n');
    }
    
    // Summarize older messages
    const olderMessages = this.conversationHistory.slice(0, -4);
    const recentMessages = this.conversationHistory.slice(-4);
    
    const olderText = olderMessages
      .map(m => `${m.role}: ${m.content}`)
      .join('\n');
    
    const summaryPrompt = `Summarize this conversation concisely in ${maxTokens} tokens:\n\n${olderText}`;
    
    const result = await this.model.generateContent(summaryPrompt);
    const summary = result.response.text();
    
    return `${summary}\n\n--- Recent ---\n${recentMessages.map(m => `${m.role}: ${m.content}`).join('\n')}`;
  }
  
  /**
   * Prune history to stay within token budget
   */
  private pruneHistory(maxTokens: number): void {
    let totalTokens = 0;
    const toKeep: typeof this.conversationHistory = [];
    
    // Go backwards
    for (let i = this.conversationHistory.length - 1; i >= 0; i--) {
      const msg = this.conversationHistory[i];
      const msgTokens = Math.ceil(msg.content.length / 4);
      
      if (totalTokens + msgTokens <= maxTokens) {
        toKeep.unshift(msg);
        totalTokens += msgTokens;
      } else {
        break;
      }
    }
    
    this.conversationHistory = toKeep;
  }
  
  /**
   * Reset conversation
   */
  reset(): void {
    this.conversationHistory = [];
  }
}

// Usage example
async function example() {
  const system = new StreamingContextSystem(process.env.GEMINI_API_KEY!);
  
  // First message
  console.log('User: What is machine learning?');
  
  let response = '';
  for await (const chunk of await system.streamWithContext(
    'What is machine learning? Give a brief explanation.'
  )) {
    process.stdout.write(chunk);
    response += chunk;
  }
  console.log('\n');
  
  // Follow-up (uses context)
  console.log('User: Can you give an example?');
  
  response = '';
  for await (const chunk of await system.streamWithContext(
    'Can you give an example?'
  )) {
    process.stdout.write(chunk);
    response += chunk;
  }
}
```

## Troubleshooting

### Các Vấn Đề Thường Gặp

**1. "Context window exceeded" Error**

```
Nguyên nhân: Tổng tokens vượt quá context limit
Giải pháp:
- Kiểm tra token usage bằng countTokens() trước khi gửi
- Implement summarization cho long documents
- Sử dụng chunking để process documents theo parts
- Giảm conversation history size
- Xem xét sử dụng embeddings thay vì full text
```

**2. "Model ignores part of context"**

```
Nguyên nhân: Context quá dài hoặc không được tổ chức tốt
Giải pháp:
- Đặt important information ở đầu context
- Sử dụng clear delimiters (=== SECTION ===)
- Tóm tắt các phần không quan trọng
- Giảm overall context size
- Sử dụng hierarchical structure
```

**3. "Slow response với large context"**

```
Nguyên nhân: Model cần xử lý nhiều tokens
Giải pháp:
- Cache frequent contexts
- Sử dụng smaller context windows với sliding approach
- Pre-process và index documents
- Implement smart retrieval để chỉ load relevant chunks
```

**4. "Inconsistent behavior với long conversations"**

```
Nguyên nhân: Conversation history quá dài hoặc có gaps
Giải pháp:
- Implement periodic summarization của history
- Sử dụng structured format cho history
- Clear reset sau khi topic changes
- Keep only relevant context
```

**5. "Token count mismatch"**

```
Nguyên nhân: Ước tính tokens không chính xác
Giải pháp:
- Luôn sử dụng countTokens() API để verify
- Cập nhật estimation formulas khi model được update
- Thêm buffer (10-20%) cho safety
```

## References

### Official Documentation

- [Gemini Context Window Documentation](https://ai.google.dev/docs/context_window)
- [Token Counting API](https://ai.google.dev/docs/tokens)
- [Long Context Best Practices](https://ai.google.dev/docs/long_context)

### Related Documents

- `@gemini-api-setup.md` - Setup và configuration
- `@multimodal-inputs.md` - Token calculation cho multimodal inputs
- `@performance.mdc` - Tối ưu hiệu suất
- `@caching-strategy.mdc` - Caching strategies
