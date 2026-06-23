---
title: "Context Window Management"
description: "Hướng dẫn Context Window Management cho Claude API - token budgeting, efficient context usage, truncation strategies, optimization"
tags: ["claude", "context-window", "tokens", "optimization", "memory", "truncation"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Context Window Management

## Tổng quan (Overview)

Context window là một trong những tài nguyên quan trọng nhất khi làm việc với Claude API. Nó xác định tổng số tokens mà model có thể xử lý trong một single request, bao gồm cả input (system prompt, messages) và output. Việc quản lý context window hiệu quả là yếu tố then chốt để xây dựng các ứng dụng AI production-ready, cost-efficient và có khả năng mở rộng.

Trong môi trường enterprise, nơi mà chi phí có thể tăng nhanh chóng với token usage và chất lượng responses phụ thuộc vào việc cung cấp đủ context, việc nắm vững các kỹ thuật context window management trở nên đặc biệt quan trọng.

Tài liệu này cung cấp hướng dẫn toàn diện về token counting, context budgeting, truncation strategies, và các best practices để tối ưu hóa việc sử dụng context window.

## Mục đích (Purpose)

Mục tiêu chính của tài liệu này bao gồm:

1. **Hiểu cơ chế context window** - Cách Claude tính và giới hạn tokens
2. **Token counting chính xác** - Phương pháp đếm tokens cho text khác nhau
3. **Context budgeting** - Chiến lược phân bổ tokens cho system, history, và input
4. **Truncation strategies** - Các kỹ thuật cắt giảm context an toàn
5. **Optimization patterns** - Best practices để maximize context efficiency

## Khái niệm cốt lõi (Key Concepts)

### 1. Token là gì?

Token là đơn vị nhỏ nhất mà LLM xử lý. Với Claude:

- **1 token ≈ 4 ký tự tiếng Anh** (trung bình)
- **1 token ≈ 1-2 ký tự tiếng Việt** (tùy độ phức tạp)
- **1 word tiếng Anh ≈ 1.3 tokens**
- **Code thường có token density cao hơn text thông thường**

### 2. Claude Models và Context Windows

| Model | Context Window | Input + Output |
|-------|----------------|----------------|
| Claude 3.5 Sonnet | 200K tokens | Max 4096 output |
| Claude 3 Opus | 200K tokens | Max 4096 output |
| Claude 3 Sonnet | 200K tokens | Max 4096 output |
| Claude 3 Haiku | 200K tokens | Max 4096 output |

### 3. Context Composition

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONTEXT WINDOW                               │
│                    (200K tokens max)                             │
├───────────────────────┬─────────────────────────────────────────┤
│                       │                                         │
│   SYSTEM PROMPT      │          MESSAGES ARRAY                 │
│   (instructions,     │   ┌─────────────────────────────────┐   │
│    constraints,      │   │  Message 1 (user)               │   │
│    persona)          │   ├─────────────────────────────────┤   │
│                       │   │  Message 2 (assistant)           │   │
│   ~500-2000 tokens   │   ├─────────────────────────────────┤   │
│                       │   │  Message 3 (user)               │   │
│                       │   ├─────────────────────────────────┤   │
│                       │   │  ...                            │   │
│                       │   ├─────────────────────────────────┤   │
│                       │   │  Message N (user) - LATEST      │   │
│                       │   └─────────────────────────────────┘   │
│                       │                                         │
├───────────────────────┴─────────────────────────────────────────┤
│                                                                 │
│                     OUTPUT SPACE                                │
│               (max_tokens parameter)                            │
│                     ~1024-4096 tokens                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Token Counting

### 1. Python Token Counter

```python
import anthropic
from typing import Literal

class TokenCounter:
    """Accurate token counter cho Claude API."""
    
    def __init__(self, api_key: str | None = None):
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def count_messages(self, messages: list[dict]) -> dict:
        """Đếm tokens trong messages array."""
        
        total = 0
        breakdown = []
        
        for i, msg in enumerate(messages):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            
            if isinstance(content, list):
                # Multi-modal content
                content_text = ""
                for block in content:
                    if block.get("type") == "text":
                        content_text += block["text"]
            else:
                content_text = str(content)
            
            tokens = self.count_text(content_text)
            total += tokens
            
            breakdown.append({
                "index": i,
                "role": role,
                "token_count": tokens,
                "char_count": len(content_text)
            })
        
        return {
            "total_tokens": total,
            "message_count": len(messages),
            "breakdown": breakdown
        }
    
    def count_text(self, text: str) -> int:
        """Đếm tokens trong text (sử dụng API)."""
        
        response = self.client.count_tokens(text)
        return response.count
    
    def estimate_tokens(self, text: str) -> int:
        """Ước tính tokens (không gọi API).
        
        Phương pháp: ~4 characters = 1 token (tiếng Anh)
        Tiếng Việt: ~2-3 characters = 1 token
        """
        
        # Rough estimation
        char_count = len(text)
        
        # Check if likely Vietnamese (high frequency of Vietnamese diacritics)
        vietnamese_chars = sum(1 for c in text if '\u00C0' <= c <= '\u024F')
        is_vietnamese = vietnamese_chars / char_count > 0.1 if char_count > 0 else False
        
        if is_vietnamese:
            return char_count // 2
        else:
            return char_count // 4
    
    def count_request(
        self,
        system: str | None = None,
        messages: list[dict] | None = None,
        max_tokens: int = 1024,
    ) -> dict:
        """Đếm tokens cho một complete request."""
        
        total = max_tokens  # Reserve for output
        
        if system:
            total += self.count_text(system)
        
        if messages:
            msg_tokens = self.count_messages(messages)
            total += msg_tokens["total_tokens"]
        
        return {
            "estimated_total": total,
            "system_tokens": self.count_text(system) if system else 0,
            "messages_tokens": self.count_messages(messages)["total_tokens"] if messages else 0,
            "output_tokens": max_tokens,
            "within_limit": total <= 200000
        }
```

### 2. TypeScript Token Counter

```typescript
import Anthropic from '@anthropic-ai/sdk';

export interface TokenCountResult {
  totalTokens: number;
  breakdown: Array<{
    index: number;
    role: string;
    tokenCount: number;
    charCount: number;
  }>;
}

export class TokenCounter {
  private client: Anthropic;
  
  constructor(apiKey?: string) {
    this.client = new Anthropic({ apiKey });
  }
  
  async countText(text: string): Promise<number> {
    const response = await this.client.countTokens({ text });
    return response.count;
  }
  
  async countMessages(
    messages: Array<{ role: string; content: string | any[] }>
  ): Promise<TokenCountResult> {
    let total = 0;
    const breakdown: TokenCountResult['breakdown'] = [];
    
    for (let i = 0; i < messages.length; i++) {
      const msg = messages[i];
      let contentText = '';
      
      if (Array.isArray(msg.content)) {
        contentText = msg.content
          .filter(b => b.type === 'text')
          .map(b => (b as any).text)
          .join('');
      } else {
        contentText = String(msg.content);
      }
      
      const tokenCount = await this.countText(contentText);
      total += tokenCount;
      
      breakdown.push({
        index: i,
        role: msg.role,
        tokenCount,
        charCount: contentText.length
      });
    }
    
    return { totalTokens: total, breakdown };
  }
  
  estimateTokens(text: string): number {
    const charCount = text.length;
    
    // Check for Vietnamese characters
    const vietnamesePattern = /[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]/gi;
    const vietnameseMatches = text.match(vietnamesePattern);
    const isVietnamese = vietnameseMatches && 
                        vietnameseMatches.length / charCount > 0.1;
    
    return isVietnamese ? Math.ceil(charCount / 2) : Math.ceil(charCount / 4);
  }
}
```

## Context Budgeting

### 1. Budget Manager Implementation

```python
from dataclasses import dataclass, field
from typing import Literal

@dataclass
class ContextBudget:
    """Budget manager cho Claude context window."""
    
    max_tokens: int = 200000
    max_output_tokens: int = 4096
    system_budget: int = 3000
    history_budget: int = 150000
    safety_margin: int = 500
    
    _reserved: dict[str, int] = field(default_factory=dict)
    
    def reserve(self, name: str, tokens: int):
        """Reserve tokens cho một purpose."""
        self._reserved[name] = tokens
    
    def release(self, name: str):
        """Release reserved tokens."""
        self._reserved.pop(name, None)
    
    @property
    def total_reserved(self) -> int:
        return sum(self._reserved.values())
    
    @property
    def available(self) -> int:
        return self.max_tokens - self.total_reserved - self.safety_margin
    
    @property
    def input_budget(self) -> int:
        """Tokens available cho input (system + messages)."""
        return self.available - self.max_output_tokens
    
    def can_fit(self, system_tokens: int, message_tokens: int) -> bool:
        """Check if request fits within budget."""
        total = system_tokens + message_tokens + self.max_output_tokens
        return total <= self.max_tokens - self.safety_margin
    
    def get_truncation_needed(
        self,
        system_tokens: int,
        message_tokens: int
    ) -> int:
        """Calculate tokens cần truncate."""
        total = system_tokens + message_tokens + self.max_output_tokens
        if total <= self.available:
            return 0
        return total - self.available


class AdaptiveBudget:
    """Adaptive budget manager điều chỉnh theo usage patterns."""
    
    def __init__(
        self,
        max_tokens: int = 200000,
        model: str = "claude-3-5-sonnet-20241022"
    ):
        self.max_tokens = max_tokens
        self.model = model
        
        # Dynamic allocations
        self.system_allocation = 2000
        self.output_allocation = 2048
        
        # Track usage for optimization
        self.usage_history: list[dict] = []
        self.avg_tokens_per_request = 0
    
    def allocate(
        self,
        system_prompt: str,
        estimated_input_tokens: int,
        desired_output_tokens: int,
        token_counter: 'TokenCounter'
    ) -> dict:
        """Calculate optimal allocation cho request."""
        
        # Get actual token counts
        system_tokens = token_counter.count_text(system_prompt)
        message_tokens = estimated_input_tokens
        
        # Calculate available
        available = self.max_tokens - system_tokens - desired_output_tokens
        
        # Determine if truncation needed
        if message_tokens <= available:
            # No truncation needed
            return {
                "needs_truncation": False,
                "truncate_messages": 0,
                "output_tokens": desired_output_tokens,
                "system_tokens": system_tokens,
                "message_tokens": message_tokens
            }
        else:
            # Truncation needed
            truncate_amount = message_tokens - available
            
            return {
                "needs_truncation": True,
                "truncate_messages": truncate_amount,
                "output_tokens": desired_output_tokens,
                "system_tokens": system_tokens,
                "message_tokens": message_tokens,
                "available": available
            }
    
    def record_usage(self, tokens_used: dict):
        """Record usage cho future optimization."""
        self.usage_history.append(tokens_used)
        
        # Keep last 100 records
        if len(self.usage_history) > 100:
            self.usage_history = self.usage_history[-100:]
        
        # Update averages
        if self.usage_history:
            recent = self.usage_history[-10:]
            self.avg_tokens_per_request = sum(
                u.get("total", 0) for u in recent
            ) / len(recent)
```

## Truncation Strategies

### 1. Smart Truncation

```python
from typing import Callable

class SmartTruncator:
    """Truncation strategies cho different content types."""
    
    def truncate_messages(
        self,
        messages: list[dict],
        max_tokens: int,
        token_counter: 'TokenCounter',
        strategy: Literal["smart", "last", "first", "summary"] = "smart"
    ) -> list[dict]:
        """Truncate messages theo strategy."""
        
        current_tokens = token_counter.count_messages(messages)["total_tokens"]
        
        if current_tokens <= max_tokens:
            return messages
        
        strategies = {
            "smart": self._smart_truncate,
            "last": self._last_n_truncate,
            "first": self._first_n_truncate,
            "summary": self._summary_truncate,
        }
        
        return strategies[strategy](messages, max_tokens, token_counter)
    
    def _smart_truncate(
        self,
        messages: list[dict],
        max_tokens: int,
        token_counter: 'TokenCounter'
    ) -> list[dict]:
        """Smart truncation: keep recent + summary of older."""
        
        if len(messages) <= 2:
            return self._last_n_truncate(messages, max_tokens, token_counter)
        
        # Keep last message(s) intact
        kept_messages = []
        kept_tokens = 0
        truncate_from = 0
        
        # Keep messages from the end until we hit limit
        for i in range(len(messages) - 1, -1, -1):
            msg_tokens = token_counter.count_text(
                str(messages[i].get("content", ""))
            )
            
            if kept_tokens + msg_tokens > max_tokens * 0.7:
                break
            
            kept_messages.insert(0, messages[i])
            kept_tokens += msg_tokens
            truncate_from = i
        
        # Add summary of truncated messages
        if truncate_from > 0:
            truncated = messages[:truncate_from]
            summary = self._generate_summary(truncated)
            summary_tokens = token_counter.count_text(summary)
            
            if kept_tokens + summary_tokens <= max_tokens:
                kept_messages.insert(0, {
                    "role": "system",
                    "content": f"[Previous conversation summary]\n{summary}"
                })
            else:
                # Just keep last N messages
                return self._last_n_truncate(messages, max_tokens, token_counter)
        
        return kept_messages
    
    def _last_n_truncate(
        self,
        messages: list[dict],
        max_tokens: int,
        token_counter: 'TokenCounter'
    ) -> list[dict]:
        """Truncate: keep only last N messages."""
        
        result = []
        total_tokens = 0
        
        # Iterate from end to start
        for msg in reversed(messages):
            msg_tokens = token_counter.count_text(
                str(msg.get("content", ""))
            )
            
            if total_tokens + msg_tokens > max_tokens:
                break
            
            result.insert(0, msg)
            total_tokens += msg_tokens
        
        return result
    
    def _first_n_truncate(
        self,
        messages: list[dict],
        max_tokens: int,
        token_counter: 'TokenCounter'
    ) -> list[dict]:
        """Truncate: keep only first N messages (not recommended)."""
        
        result = []
        total_tokens = 0
        
        for msg in messages:
            msg_tokens = token_counter.count_text(
                str(msg.get("content", ""))
            )
            
            if total_tokens + msg_tokens > max_tokens:
                break
            
            result.append(msg)
            total_tokens += msg_tokens
        
        return result
    
    def _summary_truncate(
        self,
        messages: list[dict],
        max_tokens: int,
        token_counter: 'TokenCounter'
    ) -> list[dict]:
        """Keep first + last, summarize middle (requires LLM)."""
        
        if len(messages) <= 4:
            return self._last_n_truncate(messages, max_tokens, token_counter)
        
        # Keep first and last messages
        first = messages[0]
        last = messages[-1]
        middle = messages[1:-1]
        
        middle_tokens = token_counter.count_messages(middle)["total_tokens"]
        
        # If middle is small enough, include all
        first_tokens = token_counter.count_text(str(first.get("content", "")))
        last_tokens = token_counter.count_text(str(last.get("content", "")))
        
        if first_tokens + last_tokens + middle_tokens <= max_tokens:
            return [first, *middle, last]
        
        # Need to summarize middle
        # (In production, this would call Claude to summarize)
        summary = self._generate_summary(middle)
        
        return [first, {"role": "system", "content": f"[Summary: {summary}]"}, last]
    
    def _generate_summary(self, messages: list[dict]) -> str:
        """Generate summary of messages (placeholder - use LLM in production)."""
        
        summary_parts = []
        for msg in messages:
            role = msg.get("role", "unknown")
            content = str(msg.get("content", ""))[:100]
            summary_parts.append(f"{role}: {content}...")
        
        return f"Conversation had {len(messages)} messages. Topics discussed: [summary needed]"
```

### 2. Document Truncation

```python
class DocumentTruncator:
    """Truncate long documents while preserving key information."""
    
    def truncate_document(
        self,
        document: str,
        max_tokens: int,
        token_counter: 'TokenCounter',
        preserve_sections: list[str] | None = None
    ) -> str:
        """Truncate document với awareness về structure."""
        
        current_tokens = token_counter.count_text(document)
        
        if current_tokens <= max_tokens:
            return document
        
        # Try to preserve important sections
        if preserve_sections:
            return self._preserve_important_sections(
                document, max_tokens, token_counter, preserve_sections
            )
        
        # Smart chunk truncation
        return self._smart_chunk_truncate(
            document, max_tokens, token_counter
        )
    
    def _preserve_important_sections(
        self,
        document: str,
        max_tokens: int,
        token_counter: 'TokenCounter',
        important_keywords: list[str]
    ) -> str:
        """Keep sections containing important keywords."""
        
        # Split into sections (by double newlines)
        sections = document.split("\n\n")
        
        # Score sections by importance
        scored_sections = []
        for section in sections:
            tokens = token_counter.count_text(section)
            score = sum(
                1 for kw in important_keywords
                if kw.lower() in section.lower()
            )
            scored_sections.append({
                "content": section,
                "tokens": tokens,
                "score": score
            })
        
        # Sort by importance
        scored_sections.sort(key=lambda x: (-x["score"], x["tokens"]))
        
        # Select sections until max_tokens
        result = []
        total_tokens = 0
        
        for section in scored_sections:
            if total_tokens + section["tokens"] <= max_tokens:
                result.append(section)
                total_tokens += section["tokens"]
        
        # Re-sort by original order
        result.sort(key=lambda x: document.index(x["content"]))
        
        return "\n\n".join(s["content"] for s in result)
    
    def _smart_chunk_truncate(
        self,
        document: str,
        max_tokens: int,
        token_counter: 'TokenCounter'
    ) -> str:
        """Truncate by sentences, preserving complete sentences."""
        
        # Split into sentences (works for multiple languages)
        import re
        sentences = re.split(r'(?<=[.!?])\s+', document)
        
        result = []
        total_tokens = 0
        
        for sentence in sentences:
            sentence_tokens = token_counter.count_text(sentence)
            
            if total_tokens + sentence_tokens > max_tokens:
                # Check if we can add a partial sentence
                # (In production, might add "[truncated]" marker)
                break
            
            result.append(sentence)
            total_tokens += sentence_tokens
        
        return " ".join(result)
```

## Efficient Context Usage

### 1. Message Compression

```python
class MessageCompressor:
    """Compress messages để save tokens."""
    
    COMPRESSION_PATTERNS = {
        # Remove extra whitespace
        r'\s+': ' ',
        # Remove repeated punctuation
        r'([.!?])\1+': r'\1',
        # Shorten common phrases
        'tôi muốn': 'muốn',
        'bạn có thể': 'bạn',
        'xin vui lòng': '',
        # Remove hedging language
        'có lẽ có thể': 'có',
    }
    
    def compress(self, text: str) -> str:
        """Apply compression patterns."""
        
        result = text
        
        for pattern, replacement in self.COMPRESSION_PATTERNS.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        # Clean up extra spaces
        result = re.sub(r'\s+', ' ', result).strip()
        
        return result
    
    def compress_messages(self, messages: list[dict]) -> list[dict]:
        """Compress all messages."""
        
        compressed = []
        
        for msg in messages:
            content = msg.get("content", "")
            
            if isinstance(content, str):
                compressed_content = self.compress(content)
            elif isinstance(content, list):
                compressed_content = [
                    block if block.get("type") != "text"
                    else {**block, "text": self.compress(block["text"])}
                    for block in content
                ]
            else:
                compressed_content = content
            
            compressed.append({
                **msg,
                "content": compressed_content
            })
        
        return compressed
```

### 2. Semantic Chunking

```python
class SemanticChunker:
    """Chunk documents by semantic content."""
    
    def __init__(self, client: Anthropic):
        self.client = client
    
    def chunk_by_topic(
        self,
        document: str,
        max_chunk_tokens: int = 8000,
        overlap_tokens: int = 500,
        token_counter: 'TokenCounter' = None
    ) -> list[dict]:
        """Split document into semantically coherent chunks."""
        
        # Use Claude to identify topic boundaries
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": f"""Analyze this document and identify semantic sections.
                Return a JSON array of sections with:
                - "title": section title
                - "start": character position where section starts
                - "end": character position where section ends
                - "summary": brief summary of section content
                
                Document:
                {document[:5000]}..."""  # First 5000 chars for analysis
            }]
        )
        
        # Parse response and create chunks
        # (Implementation would parse JSON response)
        sections = self._parse_sections(response.content[0].text)
        
        chunks = []
        for section in sections:
            section_text = document[section["start"]:section["end"]]
            section_tokens = token_counter.count_text(section_text)
            
            if section_tokens <= max_chunk_tokens:
                chunks.append({
                    "title": section["title"],
                    "content": section_text,
                    "tokens": section_tokens,
                    "summary": section["summary"]
                })
            else:
                # Split large section
                sub_chunks = self._split_large_section(
                    section_text,
                    max_chunk_tokens,
                    overlap_tokens,
                    token_counter
                )
                chunks.extend(sub_chunks)
        
        return chunks
    
    def _split_large_section(
        self,
        text: str,
        max_tokens: int,
        overlap_tokens: int,
        token_counter: 'TokenCounter'
    ) -> list[dict]:
        """Split large section into smaller chunks."""
        
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for para in paragraphs:
            para_tokens = token_counter.count_text(para)
            
            if current_tokens + para_tokens > max_tokens and current_chunk:
                # Save current chunk
                chunks.append("\n\n".join(current_chunk))
                
                # Start new chunk with overlap
                overlap_text = "\n\n".join(current_chunk[-2:])
                overlap_tokens_count = token_counter.count_text(overlap_text)
                
                if overlap_tokens_count <= overlap_tokens:
                    current_chunk = [overlap_text, para]
                    current_tokens = overlap_tokens_count + para_tokens
                else:
                    current_chunk = [para]
                    current_tokens = para_tokens
            else:
                current_chunk.append(para)
                current_tokens += para_tokens
        
        # Add final chunk
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))
        
        return [{"content": c, "tokens": token_counter.count_text(c)} for c in chunks]
```

## Best Practices

### 1. System Prompt Optimization

```python
# EFFICIENT: Concise, well-structured system prompt
EFFICIENT_SYSTEM = """Bạn là {company} customer support AI.

## QUICK RULES
- Language: Vietnamese (default)
- Tone: Professional, empathetic
- Response: Concise bullet points

## CAPABILITIES
- Answer FAQs about products/services
- Help with order tracking
- Process simple requests

## LIMITATIONS
- No external web access
- Escalate: refunds >$100, technical issues
"""

# INEFFICIENT: Verbose, redundant system prompt
INEFFICIENT_SYSTEM = """Bạn là một trợ lý AI rất thông minh và hữu ích. 
Bạn được thiết kế để hỗ trợ khách hàng của công ty {company}.
Công ty {company} là một công ty hàng đầu trong lĩnh vực bán lẻ.
Chúng tôi cung cấp các sản phẩm và dịch vụ chất lượng cao cho khách hàng.
Trong vai trò trợ lý AI, bạn cần phải rất lịch sự và thân thiện...
[continues with more redundancy]
"""
```

### 2. History Management

```python
class ConversationHistoryManager:
    """Manage conversation history efficiently."""
    
    def __init__(
        self,
        max_history_tokens: int = 100000,
        token_counter: TokenCounter = None
    ):
        self.max_history_tokens = max_history_tokens
        self.token_counter = token_counter or TokenCounter()
        self.messages: list[dict] = []
    
    def add_message(self, role: str, content: str):
        """Add a message to history."""
        self.messages.append({
            "role": role,
            "content": content
        })
        self._ensure_within_limit()
    
    def add_message_with_context(
        self,
        role: str,
        content: str,
        context: dict | None = None
    ):
        """Add message with additional context (stored separately)."""
        msg = {
            "role": role,
            "content": content
        }
        
        if context:
            msg["metadata"] = context
        
        self.messages.append(msg)
        self._ensure_within_limit()
    
    def _ensure_within_limit(self):
        """Remove old messages if over limit."""
        
        while True:
            total = self.token_counter.count_messages(self.messages)
            if total["total_tokens"] <= self.max_history_tokens:
                break
            
            if len(self.messages) <= 2:
                # Can't remove more, keep last 2
                break
            
            # Remove oldest non-system message
            for i, msg in enumerate(self.messages):
                if msg["role"] != "system":
                    self.messages.pop(i)
                    break
    
    def get_messages_for_api(self) -> list[dict]:
        """Get messages formatted for API call."""
        return self.messages.copy()
    
    def create_summary(self, client: Anthropic) -> str:
        """Create summary of conversation history."""
        
        if len(self.messages) <= 4:
            return ""
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"""Summarize this conversation briefly.
                Include key topics, user requests, and any important decisions.
                Keep under 200 words.
                
                Conversation:
                {self._format_for_summary()}"
            }]
        )
        
        return response.content[0].text
    
    def _format_for_summary(self) -> str:
        """Format messages for summarization."""
        lines = []
        for msg in self.messages:
            role = msg["role"].upper()
            content = msg["content"]
            if isinstance(content, list):
                content = " ".join(
                    b.get("text", "") for b in content if b.get("type") == "text"
                )
            lines.append(f"{role}: {content[:500]}")
        return "\n".join(lines)
```

### 3. Batch Processing with Context Management

```python
class BatchProcessor:
    """Process multiple items with shared context."""
    
    def __init__(
        self,
        client: Anthropic,
        token_counter: TokenCounter,
        max_context_tokens: int = 180000
    ):
        self.client = client
        self.token_counter = token_counter
        self.max_context_tokens = max_context_tokens
    
    async def process_with_shared_context(
        self,
        system_prompt: str,
        items: list[str],
        process_instruction: str,
        items_per_batch: int = 5
    ) -> list[dict]:
        """Process items in batches with shared context."""
        
        results = []
        
        for i in range(0, len(items), items_per_batch):
            batch = items[i:i + items_per_batch]
            
            # Build batch prompt
            batch_content = f"{process_instruction}\n\n"
            for idx, item in enumerate(batch, i + 1):
                batch_content += f"\n--- Item {idx} ---\n{item}"
            
            # Calculate tokens
            total_tokens = (
                self.token_counter.count_text(system_prompt) +
                self.token_counter.count_text(batch_content)
            )
            
            # If too large, process individually
            if total_tokens > self.max_context_tokens:
                for idx, item in enumerate(batch, i + 1):
                    single_result = await self._process_single(
                        system_prompt,
                        f"{process_instruction}\n\nItem: {item}",
                        idx
                    )
                    results.append(single_result)
            else:
                # Process batch
                batch_result = await self._process_batch(
                    system_prompt,
                    batch_content,
                    start_idx=i + 1
                )
                results.extend(batch_result)
        
        return results
    
    async def _process_single(
        self,
        system: str,
        content: str,
        idx: int
    ) -> dict:
        """Process a single item."""
        # Implementation
        pass
    
    async def _process_batch(
        self,
        system: str,
        content: str,
        start_idx: int
    ) -> list[dict]:
        """Process a batch of items."""
        # Implementation
        pass
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `context_length_exceeded` | Too many tokens | Implement truncation |
| Inconsistent responses | System prompt getting cut off | Put critical instructions at start |
| Poor quality outputs | Not enough context | Increase budget for important context |
| High costs | Inefficient token usage | Compress messages, optimize prompts |
| Missing conversation history | History being truncated | Implement smart history management |

### Monitoring Token Usage

```python
class TokenMonitor:
    """Monitor và alert on token usage."""
    
    def __init__(
        self,
        warning_threshold: float = 0.8,
        critical_threshold: float = 0.95
    ):
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.usage_records: list[dict] = []
    
    def record_request(
        self,
        request_id: str,
        tokens: dict,
        response_time: float
    ):
        """Record token usage for a request."""
        
        record = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "input_tokens": tokens.get("input", 0),
            "output_tokens": tokens.get("output", 0),
            "total_tokens": tokens.get("total", 0),
            "response_time": response_time
        }
        
        self.usage_records.append(record)
        
        # Check thresholds
        utilization = tokens.get("total", 0) / 200000
        
        if utilization >= self.critical_threshold:
            self._send_alert("CRITICAL", f"Token usage at {utilization:.1%}")
        elif utilization >= self.warning_threshold:
            self._send_alert("WARNING", f"Token usage at {utilization:.1%}")
    
    def get_usage_stats(self, days: int = 7) -> dict:
        """Get usage statistics."""
        
        cutoff = datetime.now() - timedelta(days=days)
        recent = [
            r for r in self.usage_records
            if datetime.fromisoformat(r["timestamp"]) > cutoff
        ]
        
        if not recent:
            return {"error": "No usage data"}
        
        return {
            "period_days": days,
            "total_requests": len(recent),
            "total_input_tokens": sum(r["input_tokens"] for r in recent),
            "total_output_tokens": sum(r["output_tokens"] for r in recent),
            "avg_tokens_per_request": sum(r["total_tokens"] for r in recent) / len(recent),
            "avg_response_time": sum(r["response_time"] for r in recent) / len(recent)
        }
    
    def _send_alert(self, level: str, message: str):
        """Send alert (implement based on your notification system)."""
        print(f"[{level}] {message}")
```

## References

- [Anthropic Token Counting](https://docs.anthropic.com/claude/reference/token-counting)
- [Context Window Best Practices](https://docs.anthropic.com/claude/docs/context-windows)
- [Optimizing Token Usage](https://docs.anthropic.com/claude/docs/optimizing-token-usage)
