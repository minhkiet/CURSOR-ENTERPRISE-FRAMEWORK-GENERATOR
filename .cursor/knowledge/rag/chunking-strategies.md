---
title: "Chunking Strategies"
description: "Hướng dẫn về các chiến lược chunking cho RAG: fixed-size, semantic, recursive text splitting và code-aware chunking"
tags: ["chunking", "rag", "text-splitting", "retrieval", "embedding"]
created: "2026-06-23"
version: "1.0.0"
framework: "Cursor Enterprise Framework"
---

# Chunking Strategies

## Tổng Quan

Chunking là bước quan trọng đầu tiên trong việc xây dựng RAG system. Cách chúng ta chia nhỏ documents thành các chunks sẽ ảnh hưởng trực tiếp đến quality của retrieval và final answers. Chunk quá lớn có thể chứa quá nhiều thông tin nhiễu, trong khi chunk quá nhỏ có thể thiếu context cần thiết.

Có nhiều chiến lược chunking khác nhau, từ đơn giản như fixed-size splitting đến phức tạp như semantic chunking sử dụng NLP. Việc lựa chọn chiến lược phù hợp phụ thuộc vào loại content, embedding model, và use case cụ thể.

Tài liệu này sẽ đi sâu vào các chiến lược chunking phổ biến, giúp developers hiểu rõ khi nào nên sử dụng phương pháp nào và cách implement chúng hiệu quả.

## Mục Đích

Tài liệu này nhằm cung cấp kiến thức toàn diện về chunking strategies cho RAG systems:

Đầu tiên, chúng ta sẽ tìm hiểu fixed-size chunking - phương pháp đơn giản nhất nhưng hiệu quả cho nhiều trường hợp.

Thứ hai, tài liệu hướng dẫn semantic chunking - phương pháp sử dụng NLP để chia theo ngữ nghĩa.

Thứ ba, chúng ta sẽ đề cập đến recursive text splitting - kỹ thuật chia nhỏ đệ quy theo hierarchical structure.

Cuối cùng, tài liệu cung cấp specialized chunking strategies cho code và structured content.

## Key Concepts

### 1. Chunking Parameters

Trước khi đi vào chi tiết từng chiến lược, chúng ta cần hiểu các parameters cơ bản:

```python
# Common chunking parameters
CHUNK_SIZE = 500       # Số characters hoặc tokens trong mỗi chunk
CHUNK_OVERLAP = 50    # Số characters/tokens overlap giữa các chunks
MIN_CHUNK_SIZE = 100  # Kích thước tối thiểu của chunk
MAX_CHUNK_SIZE = 1000 # Kích thước tối đa của chunk

# Additional parameters
SEPARATORS = ["\n\n", "\n", ". ", " "]  # Characters dùng để tách text
```

Việc lựa chọn chunk size phụ thuộc vào:
- Embedding model context window
- LLM context window
- Nature của content
- Query patterns

```python
# Chunk size guidelines by use case
CHUNK_SIZE_GUIDELINES = {
    "conversational_qa": 300,      # Short, focused chunks
    "summarization": 1000,         # Longer chunks for context
    "code_analysis": 200,           # Small for precision
    "document_search": 500,         # Balanced
    "semantic_search": 700,         # Larger for meaning
}
```

### 2. Token Estimation

Vì nhiều embedding models sử dụng tokens thay vì characters, việc estimate token count là quan trọng:

```python
def estimate_tokens(text: str, model: str = "cl100k_base") -> int:
    """
    Estimate token count cho text.
    Uses approximate ratios for different encodings.
    """
    # Approximate: 1 token ≈ 4 characters for English
    # Hoặc sử dụng tiktoken library để count chính xác
    
    if model == "cl100k_base":  # GPT-4, text-embedding-3
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    elif model == "p50k_base":  # GPT-3.5, Codex
        enc = tiktoken.get_encoding("p50k_base")
        return len(enc.encode(text))
    else:
        # Fallback approximation
        return len(text) // 4

def characters_to_tokens(char_count: int) -> int:
    """Approximate conversion - 4 chars = 1 token"""
    return char_count // 4
```

## Fixed-Size Chunking

### 1. Basic Implementation

```python
from typing import List, Tuple
import re

class FixedSizeChunker:
    """
    Simple fixed-size chunking by characters or tokens.
    """
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        length_function = len
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.length_function = length_function
    
    def chunk(self, text: str) -> List[Tuple[str, int, int]]:
        """
        Split text into fixed-size chunks.
        
        Returns:
            List of (chunk_text, start_char, end_char)
        """
        if not text:
            return []
        
        chunks = []
        start = 0
        text_length = self.length_function(text)
        
        while start < text_length:
            end = start + self.chunk_size
            
            # Don't cut in middle of word if possible
            if end < text_length:
                # Find last space before end
                last_space = text.rfind(' ', start, end)
                if last_space != -1 and last_space > start:
                    end = last_space
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append((chunk, start, end))
            
            # Move start with overlap
            start = end - self.chunk_overlap
            
            # Ensure we're making progress
            if start <= chunks[-1][2] if chunks else start >= start:
                start = end
        
        return chunks


# Usage
chunker = FixedSizeChunker(chunk_size=500, chunk_overlap=50)
text = "Your long document content here..."
chunks = chunker.chunk(text)
```

### 2. Token-based Chunking

```python
import tiktoken

class TokenChunker:
    """
    Chunking based on token count for better embedding quality.
    """
    
    def __init__(
        self,
        model: str = "cl100k_base",
        chunk_size: int = 256,  # tokens
        chunk_overlap: int = 32,  # tokens
    ):
        self.encoding = tiktoken.get_encoding(model)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk(self, text: str) -> List[dict]:
        """
        Split text into token-based chunks.
        
        Returns:
            List of {"text": str, "tokens": int, "start": int, "end": int}
        """
        tokens = self.encoding.encode(text)
        total_tokens = len(tokens)
        
        chunks = []
        start = 0
        
        while start < total_tokens:
            end = min(start + self.chunk_size, total_tokens)
            
            # Get chunk tokens and decode
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)
            
            if chunk_text.strip():
                chunks.append({
                    "text": chunk_text,
                    "tokens": len(chunk_tokens),
                    "start": start,
                    "end": end
                })
            
            # Move start with overlap
            start = end - self.chunk_overlap
            
            if start >= end:
                break
        
        return chunks


# Usage
chunker = TokenChunker(model="cl100k_base", chunk_size=256, chunk_overlap=32)
chunks = chunker.chunk(document_text)
```

### 3. Hybrid Chunking with Metadata

```python
class DocumentChunker:
    """
    Advanced chunking với metadata tracking.
    """
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        min_chunk_size: int = 100,
        max_chunks: int = None
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
        self.max_chunks = max_chunks
    
    def chunk(
        self,
        text: str,
        document_id: str,
        document_metadata: dict = None
    ) -> List[dict]:
        """
        Chunk document với full metadata.
        """
        chunks = []
        base_metadata = {
            "document_id": document_id,
            **(document_metadata or {})
        }
        
        # Basic chunking
        chunker = FixedSizeChunker(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        
        raw_chunks = chunker.chunk(text)
        
        # Process and validate chunks
        for i, (chunk_text, start, end) in enumerate(raw_chunks):
            # Skip tiny chunks at document end
            if len(chunk_text) < self.min_chunk_size and i == len(raw_chunks) - 1:
                # Merge with previous chunk
                if chunks:
                    chunks[-1]["text"] += "\n" + chunk_text
                    chunks[-1]["end_char"] = end
                continue
            
            chunk = {
                "text": chunk_text,
                "chunk_index": i,
                "start_char": start,
                "end_char": end,
                "char_count": len(chunk_text),
                "word_count": len(chunk_text.split()),
                **base_metadata
            }
            chunks.append(chunk)
            
            # Respect max chunks limit
            if self.max_chunks and len(chunks) >= self.max_chunks:
                break
        
        return chunks
```

## Semantic Chunking

### 1. Sentence-based Chunking

```python
import re
from typing import List
import nltk

# Download required NLTK data
# nltk.download('punkt')
# nltk.download('punkt_tab')

class SentenceChunker:
    """
    Semantic chunking by sentences.
    """
    
    def __init__(
        self,
        max_sentences: int = 5,
        min_sentences: int = 1,
        combine_texts: bool = True
    ):
        self.max_sentences = max_sentences
        self.min_sentences = min_sentences
        self.combine_texts = combine_texts
    
    def split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Use NLTK for better sentence splitting
        from nltk.tokenize import sent_tokenize
        return sent_tokenize(text)
    
    def chunk(self, text: str) -> List[Tuple[str, int, int]]:
        """
        Split into semantic chunks based on sentences.
        """
        sentences = self.split_into_sentences(text)
        chunks = []
        current_chunk = []
        current_sentence_count = 0
        current_start = 0
        
        for i, sentence in enumerate(sentences):
            current_chunk.append(sentence)
            current_sentence_count += 1
            current_text = " ".join(current_chunk)
            
            if current_sentence_count >= self.max_sentences:
                # Create chunk
                chunk_text = current_text.strip()
                if chunk_text:
                    start_char = text.find(chunk_text)
                    chunks.append((chunk_text, start_char, start_char + len(chunk_text)))
                
                # Start new chunk with overlap
                current_chunk = []
                current_sentence_count = 0
        
        # Handle remaining sentences
        if current_chunk and current_sentence_count >= self.min_sentences:
            chunk_text = " ".join(current_chunk).strip()
            if chunk_text:
                start_char = text.find(chunk_text)
                chunks.append((chunk_text, start_char, start_char + len(chunk_text)))
        
        return chunks


# Usage
chunker = SentenceChunker(max_sentences=5, min_sentences=2)
chunks = chunker.chunk(long_document)
```

### 2. Paragraph-based Chunking

```python
class ParagraphChunker:
    """
    Chunking by paragraphs - great for structured documents.
    """
    
    def __init__(
        self,
        max_paragraphs: int = 3,
        min_paragraphs: int = 1,
        overlap: bool = False
    ):
        self.max_paragraphs = max_paragraphs
        self.min_paragraphs = min_paragraphs
        self.overlap = overlap
    
    def split_into_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs."""
        # Split by double newlines or single newlines
        paragraphs = re.split(r'\n\s*\n|\n', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def chunk(self, text: str) -> List[dict]:
        """Split into paragraph-based chunks."""
        paragraphs = self.split_into_paragraphs(text)
        chunks = []
        current_paragraphs = []
        current_char_start = 0
        
        for i, para in enumerate(paragraphs):
            current_paragraphs.append(para)
            
            if len(current_paragraphs) >= self.max_paragraphs:
                chunk_text = "\n\n".join(current_paragraphs)
                chunk_start = text.find(chunk_text)
                
                chunks.append({
                    "text": chunk_text,
                    "paragraph_count": len(current_paragraphs),
                    "paragraph_indices": list(range(i - len(current_paragraphs) + 1, i + 1))
                })
                
                # With or without overlap
                if self.overlap:
                    current_paragraphs = current_paragraphs[-1:]
                else:
                    current_paragraphs = []
        
        # Handle remaining paragraphs
        if current_paragraphs and len(current_paragraphs) >= self.min_paragraphs:
            chunk_text = "\n\n".join(current_paragraphs)
            chunks.append({
                "text": chunk_text,
                "paragraph_count": len(current_paragraphs)
            })
        
        return chunks


# Usage
chunker = ParagraphChunker(max_paragraphs=3, overlap=True)
chunks = chunker.chunk(document_text)
```

### 3. Semantic Similarity Chunking

```python
from typing import List, Tuple
import numpy as np

class SemanticChunker:
    """
    Advanced semantic chunking using embedding similarity.
    Groups sentences that are semantically similar together.
    """
    
    def __init__(
        self,
        embedder,
        threshold: float = 0.5,
        min_chunk_size: int = 3,
        max_chunk_size: int = 10
    ):
        self.embedder = embedder  # Must have .embed(text) method
        self.threshold = threshold
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
    
    def chunk(self, text: str) -> List[dict]:
        """
        Semantic chunking using embedding similarity.
        
        Algorithm:
        1. Split into sentences
        2. Embed each sentence
        3. Group sentences by cosine similarity
        """
        from nltk.tokenize import sent_tokenize
        
        sentences = sent_tokenize(text)
        if len(sentences) < self.min_chunk_size:
            return [{"text": text, "sentences": sentences}]
        
        # Embed all sentences
        embeddings = self.embedder.embed(sentences)
        
        # Calculate similarity matrix
        n = len(sentences)
        similarity_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i + 1, n):
                sim = self.cosine_similarity(embeddings[i], embeddings[j])
                similarity_matrix[i][j] = sim
                similarity_matrix[j][i] = sim
        
        # Find semantic boundaries using similarity drops
        boundaries = self.find_boundaries(similarity_matrix, sentences)
        
        # Create chunks
        chunks = []
        start_idx = 0
        
        for end_idx in boundaries:
            chunk_sentences = sentences[start_idx:end_idx + 1]
            chunk_text = " ".join(chunk_sentences)
            
            if len(chunk_sentences) >= self.min_chunk_size:
                chunks.append({
                    "text": chunk_text,
                    "sentences": chunk_sentences,
                    "sentence_count": len(chunk_sentences)
                })
            
            start_idx = end_idx + 1
        
        # Handle final chunk
        if start_idx < len(sentences):
            chunk_sentences = sentences[start_idx:]
            chunk_text = " ".join(chunk_sentences)
            chunks.append({
                "text": chunk_text,
                "sentences": chunk_sentences,
                "sentence_count": len(chunk_sentences)
            })
        
        return chunks
    
    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def find_boundaries(self, sim_matrix: np.ndarray, sentences: List[str]) -> List[int]:
        """
        Find semantic boundaries where similarity drops significantly.
        """
        boundaries = []
        
        for i in range(1, len(sentences) - 1):
            # Average similarity with previous and next sentences
            prev_sim = np.mean(sim_matrix[i-1, :i])
            next_sim = np.mean(sim_matrix[i, i+1:])
            
            avg_sim = (prev_sim + next_sim) / 2
            
            # If similarity drops below threshold, it's a boundary
            if avg_sim < self.threshold:
                boundaries.append(i)
        
        return boundaries
```

## Recursive Text Splitting

### 1. Hierarchical Separator-based Splitting

```python
class RecursiveChunker:
    """
    Recursive text splitting using hierarchical separators.
    Tries to split on different separators in order of preference.
    """
    
    def __init__(
        self,
        separators: List[Tuple[str, bool]] = None,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):
        # Default separators: (separator, is_regex)
        self.default_separators = [
            ("\n\n", False),      # Double newline - paragraph
            ("\n", False),         # Single newline - line
            (". ", False),         # Sentence end
            (", ", False),         # Clause
            (" ", False),          # Word
        ]
        
        self.separators = separators or self.default_separators
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str) -> List[str]:
        """
        Recursively split text using separators.
        """
        # Base case: text is small enough
        if len(text) <= self.chunk_size:
            return [text]
        
        # Try each separator in order
        for separator, is_regex in self.separators:
            splits = self._split_by_separator(text, separator, is_regex)
            
            if len(splits) > 1:
                # Recursively split large chunks
                result = []
                for split in splits:
                    result.extend(self.split_text(split))
                
                return result
        
        # If no separator worked, force split at chunk_size
        return self._force_split(text)
    
    def _split_by_separator(self, text: str, separator: str, is_regex: bool) -> List[str]:
        """Split text by separator."""
        if is_regex:
            import re
            splits = re.split(separator, text)
        else:
            splits = text.split(separator)
        
        # Re-add separator to splits (except last)
        result = []
        for i, split in enumerate(splits):
            if i < len(splits) - 1:
                result.append(split + separator)
            else:
                result.append(split)
        
        return [s for s in result if s]
    
    def _force_split(self, text: str) -> List[str]:
        """Force split when no separator found."""
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk = text[i:i + self.chunk_size]
            if chunk:
                chunks.append(chunk)
        return chunks
    
    def chunk(self, text: str) -> List[dict]:
        """Create chunks with metadata."""
        raw_chunks = self.split_text(text)
        
        chunks = []
        for i, chunk_text in enumerate(raw_chunks):
            chunks.append({
                "text": chunk_text,
                "chunk_index": i,
                "char_count": len(chunk_text)
            })
        
        return chunks


# Usage với custom separators
chunker = RecursiveChunker(
    separators=[
        ("\n## ", False),      # Markdown h2
        ("\n### ", False),     # Markdown h3
        (". ", False),          # Sentence
        (" ", False),           # Word
    ],
    chunk_size=500
)
```

### 2. Markdown-aware Chunking

```python
class MarkdownChunker:
    """
    Chunking optimized for Markdown documents.
    Respects document structure like headers, lists, code blocks.
    """
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        headers_to_split_on: List[str] = None
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.headers_to_split_on = headers_to_split_on or ["#", "##", "###"]
    
    def chunk(self, text: str) -> List[dict]:
        """Chunk Markdown respecting its structure."""
        # Parse Markdown structure
        sections = self._parse_markdown(text)
        
        chunks = []
        current_section = None
        current_text = ""
        section_stack = []
        
        for element in sections:
            if element["type"] == "header":
                # If this is a header we're splitting on
                if any(element["text"].startswith(h) for h in self.headers_to_split_on):
                    # Save current chunk
                    if current_text.strip():
                        chunks.extend(
                            self._create_chunks(current_text, current_section, len(chunks))
                        )
                    
                    # Update section context
                    header_level = len(element["text"]) - len(element["text"].lstrip("#"))
                    section_stack = section_stack[:header_level]
                    section_stack.append(element["text"])
                    current_section = " > ".join(section_stack)
                    current_text = ""
            
            elif element["type"] == "code_block":
                # Code blocks should not be split
                if current_text.strip():
                    chunks.extend(
                        self._create_chunks(current_text, current_section, len(chunks))
                    )
                    current_text = ""
                
                chunks.append({
                    "text": element["text"],
                    "type": "code",
                    "section": current_section,
                    "language": element.get("language", "")
                })
            
            else:
                current_text += element["text"] + "\n"
        
        # Handle remaining content
        if current_text.strip():
            chunks.extend(
                self._create_chunks(current_text, current_section, len(chunks))
            )
        
        return chunks
    
    def _parse_markdown(self, text: str) -> List[dict]:
        """Parse Markdown into structured elements."""
        import re
        
        elements = []
        lines = text.split("\n")
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Header
            if line.startswith("#"):
                match = re.match(r'^(#{1,6})\s+(.*)', line)
                if match:
                    elements.append({
                        "type": "header",
                        "text": line
                    })
            
            # Code block
            elif line.strip().startswith("```"):
                code_lines = [line]
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    code_lines.append(lines[i])
                    i += 1
                code_lines.append(lines[i] if i < len(lines) else "")
                
                elements.append({
                    "type": "code_block",
                    "text": "\n".join(code_lines[1:-1]),
                    "language": line.strip()[3:]
                })
            
            # Regular text
            else:
                elements.append({
                    "type": "text",
                    "text": line
                })
            
            i += 1
        
        return elements
    
    def _create_chunks(
        self,
        text: str,
        section: str,
        existing_count: int
    ) -> List[dict]:
        """Split text into chunks if too large."""
        chunks = []
        
        if len(text) <= self.chunk_size:
            chunks.append({
                "text": text.strip(),
                "section": section,
                "chunk_index": existing_count
            })
        else:
            chunker = RecursiveChunker(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
            raw_chunks = chunker.split_text(text)
            
            for j, chunk_text in enumerate(raw_chunks):
                chunks.append({
                    "text": chunk_text.strip(),
                    "section": section,
                    "chunk_index": existing_count + j
                })
        
        return chunks
```

## Code-aware Chunking

### 1. Programming Language Chunking

```python
class CodeChunker:
    """
    Specialized chunking for source code.
    Respects functions, classes, and code structure.
    """
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        language: str = "python"
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.language = language
        self.patterns = self._get_language_patterns()
    
    def _get_language_patterns(self) -> dict:
        """Get regex patterns for different languages."""
        return {
            "python": {
                "function": r'def\s+(\w+)\s*\([^)]*\)\s*(?:->\s*\w+)?\s*:',
                "class": r'class\s+(\w+)(?:\([^)]*\))?\s*:',
                "import": r'^(?:from\s+\w+\s+)?import\s+.+$',
            },
            "javascript": {
                "function": r'(?:function\s+(\w+)|const\s+(\w+)\s*=|(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>)',
                "class": r'class\s+(\w+)',
                "import": r'^(?:import|export)\s+.+$',
            },
            "java": {
                "function": r'(?:public|private|protected)\s+(?:static\s+)?(?:final\s+)?(?:\w+\s+)+(\w+)\s*\([^)]*\)',
                "class": r'class\s+(\w+)',
                "import": r'^import\s+.+$',
            },
            "general": {
                "function": r'((?:def|function|func|fn)\s+\w+\s*\([^)]*\))',
                "class": r'class\s+\w+',
            }
        }
    
    def chunk(self, code: str) -> List[dict]:
        """Chunk code respecting language structure."""
        import re
        
        chunks = []
        
        # Try to find function/class boundaries
        patterns = self.patterns.get(
            self.language, 
            self.patterns["general"]
        )
        
        # Find all functions
        functions = []
        for pattern in [patterns.get("function", ""), patterns.get("class", "")]:
            if pattern:
                matches = list(re.finditer(pattern, code, re.MULTILINE))
                functions.extend([(m.start(), m.end(), m.group()) for m in matches])
        
        if functions:
            # Sort by position
            functions.sort()
            
            # Create chunks based on functions
            chunks = self._create_structured_chunks(code, functions)
        else:
            # Fallback to simple chunking
            chunks = self._simple_chunk(code)
        
        return chunks
    
    def _create_structured_chunks(
        self, 
        code: str, 
        functions: List[Tuple[int, int, str]]
    ) -> List[dict]:
        """Create chunks based on function boundaries."""
        chunks = []
        i = 0
        
        while i < len(functions):
            start_pos, end_pos, func_def = functions[i]
            
            # Collect code until next function or chunk_size
            chunk_start = start_pos
            chunk_code = code[chunk_start:]
            
            # Find where to cut (next function or max size)
            if i + 1 < len(functions):
                next_start = functions[i + 1][0]
                gap = next_start - start_pos
                
                if gap > self.chunk_size:
                    # Split this function into smaller chunks
                    chunk_code = code[start_pos:start_pos + self.chunk_size]
                else:
                    chunk_code = code[start_pos:next_start]
            else:
                # Last function - take all
                if len(code) - start_pos > self.chunk_size:
                    chunk_code = code[start_pos:start_pos + self.chunk_size]
            
            chunks.append({
                "text": chunk_code.strip(),
                "type": "function" if "def " in func_def or "function" in func_def else "class",
                "definition": func_def.strip(),
                "start_line": code[:start_pos].count('\n') + 1
            })
            
            i += 1
        
        return chunks
    
    def _simple_chunk(self, code: str) -> List[dict]:
        """Simple character-based chunking for code."""
        lines = code.split("\n")
        chunks = []
        current_chunk = []
        current_size = 0
        
        for line in lines:
            line_size = len(line)
            
            if current_size + line_size > self.chunk_size and current_chunk:
                chunks.append({
                    "text": "\n".join(current_chunk).strip(),
                    "type": "code"
                })
                # Start new chunk with overlap
                overlap_lines = max(1, len(current_chunk) - self.chunk_overlap // 50)
                current_chunk = current_chunk[-overlap_lines:]
                current_size = sum(len(l) for l in current_chunk)
            
            current_chunk.append(line)
            current_size += line_size
        
        # Add remaining
        if current_chunk:
            chunks.append({
                "text": "\n".join(current_chunk).strip(),
                "type": "code"
            })
        
        return chunks


# Usage
chunker = CodeChunker(language="python", chunk_size=500)
python_chunks = chunker.chunk(python_code)

chunker = CodeChunker(language="javascript", chunk_size=500)
js_chunks = chunker.chunk(javascript_code)
```

## Best Practices

### 1. Choosing the Right Strategy

```python
def recommend_chunking_strategy(document_type: str, content: str) -> str:
    """
    Recommend chunking strategy based on document type.
    """
    recommendations = {
        "code": {
            "strategy": "CodeChunker",
            "reason": "Respects functions, classes, code structure"
        },
        "markdown": {
            "strategy": "MarkdownChunker",
            "reason": "Respects headers and formatting"
        },
        "article": {
            "strategy": "SemanticChunker",
            "reason": "Groups semantically related sentences"
        },
        "legal": {
            "strategy": "ParagraphChunker",
            "reason": "Preserves section structure important for legal docs"
        },
        "technical": {
            "strategy": "RecursiveChunker",
            "reason": "Preserves code/technical formatting"
        },
        "conversational": {
            "strategy": "SentenceChunker",
            "reason": "Short, focused chunks for QA"
        }
    }
    
    return recommendations.get(document_type, {
        "strategy": "FixedSizeChunker",
        "reason": "Simple and reliable fallback"
    })


# Dynamic strategy selection
def chunk_with_strategy(text: str, strategy: str, **kwargs) -> List[dict]:
    """
    Chunk text using specified strategy.
    """
    strategies = {
        "fixed": FixedSizeChunker,
        "token": TokenChunker,
        "sentence": SentenceChunker,
        "paragraph": ParagraphChunker,
        "semantic": SemanticChunker,
        "recursive": RecursiveChunker,
        "markdown": MarkdownChunker,
        "code": CodeChunker,
    }
    
    chunker_class = strategies.get(strategy, FixedSizeChunker)
    chunker = chunker_class(**kwargs)
    
    return chunker.chunk(text)
```

### 2. Chunk Size Optimization

```python
def optimize_chunk_size(
    test_queries: List[str],
    ground_truth_chunks: Dict[str, List[str]],
    chunker_class,
    chunk_sizes: List[int] = [100, 200, 300, 500, 700, 1000]
) -> dict:
    """
    Find optimal chunk size by testing retrieval quality.
    """
    results = []
    
    for chunk_size in chunk_sizes:
        chunker = chunker_class(chunk_size=chunk_size)
        chunks = chunker.chunk(document_text)
        
        # Test retrieval for each query
        recall_scores = []
        for query in test_queries:
            retrieved = retrieve_top_k(query, chunks, k=5)
            expected = ground_truth_chunks.get(query, [])
            
            # Calculate recall
            hits = len(set(retrieved) & set(expected))
            recall = hits / len(expected) if expected else 0
            recall_scores.append(recall)
        
        results.append({
            "chunk_size": chunk_size,
            "avg_recall": np.mean(recall_scores),
            "num_chunks": len(chunks)
        })
    
    # Find best chunk size
    best = max(results, key=lambda x: x["avg_recall"])
    
    return {
        "results": results,
        "recommended_chunk_size": best["chunk_size"],
        "expected_recall": best["avg_recall"]
    }
```

### 3. Overlap Strategies

```python
def chunk_with_smart_overlap(
    text: str,
    chunker,
    overlap_strategy: str = "sentence"
) -> List[dict]:
    """
    Create chunks with intelligent overlap.
    """
    chunks = []
    
    if overlap_strategy == "sentence":
        # Overlap by sentences, not characters
        sentence_chunker = SentenceChunker(max_sentences=3)
        sentences = sentence_chunker.split_into_sentences(text)
        
        # Create overlapping windows
        window_size = 5
        overlap = 2
        
        for i in range(0, len(sentences), window_size - overlap):
            window = sentences[i:i + window_size]
            if len(window) >= 2:  # Minimum window
                chunks.append({
                    "text": " ".join(window),
                    "overlap_sentences": overlap
                })
    
    elif overlap_strategy == "adaptive":
        # Overlap based on content structure
        # More overlap at section boundaries
        paragraph_chunker = ParagraphChunker(max_paragraphs=3, overlap=True)
        chunks = paragraph_chunker.chunk(text)
    
    return chunks
```

## Common Patterns

### Pattern 1: Hierarchical Chunking

```python
class HierarchicalChunker:
    """
    Multi-level chunking: chunk first by structure (headers/sections),
    then by size within each section.
    """
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk(self, text: str) -> List[dict]:
        """Create hierarchical chunks."""
        chunks = []
        
        # Level 1: Split by major sections
        sections = self._split_by_major_sections(text)
        
        for section_idx, section in enumerate(sections):
            # Level 2: Chunk within each section
            section_chunks = self._chunk_section(section)
            
            for chunk_idx, chunk_text in enumerate(section_chunks):
                chunks.append({
                    "text": chunk_text,
                    "section_index": section_idx,
                    "chunk_index": chunk_idx,
                    "section_title": section.get("title", ""),
                    "path": f"{section_idx}/{chunk_idx}"
                })
        
        return chunks
    
    def _split_by_major_sections(self, text: str) -> List[dict]:
        """Split text into major sections."""
        import re
        
        # Split by headers (h1, h2)
        pattern = r'(?=^#{1,2}\s+.+$)'
        parts = re.split(pattern, text, flags=re.MULTILINE)
        
        sections = []
        for part in parts:
            if part.strip():
                match = re.search(r'^(#{1,2})\s+(.+)', part, re.MULTILINE)
                title = match.group(2) if match else "Untitled"
                sections.append({
                    "title": title,
                    "content": part.strip()
                })
        
        return sections
    
    def _chunk_section(self, section: dict) -> List[str]:
        """Chunk a single section."""
        chunker = RecursiveChunker(chunk_size=self.chunk_size)
        return chunker.split_text(section["content"])
```

### Pattern 2: Context-aware Chunking

```python
class ContextAwareChunker:
    """
    Adds surrounding context to each chunk for better understanding.
    """
    
    def __init__(
        self,
        base_chunker,
        context_chars: int = 100,
        context_sentences: int = 1
    ):
        self.base_chunker = base_chunker
        self.context_chars = context_chars
        self.context_sentences = context_sentences
    
    def chunk(self, text: str) -> List[dict]:
        """Create chunks with context."""
        from nltk.tokenize import sent_tokenize
        
        base_chunks = self.base_chunker.chunk(text)
        sentences = sent_tokenize(text)
        
        result = []
        
        for chunk in base_chunks:
            chunk_text = chunk["text"]
            chunk_start = text.find(chunk_text)
            
            # Add preceding context
            context_start = max(0, chunk_start - self.context_chars)
            preceding_context = text[context_start:chunk_start].strip()
            
            # Find preceding sentence boundary
            if self.context_sentences > 0:
                # Add whole sentences as context
                for i, sent in enumerate(sentences):
                    if text.find(sent) >= context_start:
                        preceding_context = " ".join(
                            sentences[max(0, i - self.context_sentences):i]
                        )
                        break
            
            result.append({
                **chunk,
                "preceding_context": preceding_context,
                "full_with_context": f"{preceding_context} {chunk_text}".strip()
            })
        
        return result
```

### Pattern 3: Deduplication at Chunk Level

```python
class DeduplicatingChunker:
    """
    Chunker that removes duplicate/near-duplicate chunks.
    """
    
    def __init__(
        self,
        base_chunker,
        similarity_threshold: float = 0.9
    ):
        self.base_chunker = base_chunker
        self.similarity_threshold = similarity_threshold
    
    def chunk(self, text: str) -> List[dict]:
        """Create chunks and remove duplicates."""
        chunks = self.base_chunker.chunk(text)
        
        # Calculate hashes for deduplication
        seen_hashes = set()
        unique_chunks = []
        
        for chunk in chunks:
            chunk_hash = hash(chunk["text"])
            
            if chunk_hash not in seen_hashes:
                seen_hashes.add(chunk_hash)
                unique_chunks.append(chunk)
            else:
                # Mark as duplicate in metadata
                pass
        
        # Re-index chunks
        for i, chunk in enumerate(unique_chunks):
            chunk["chunk_index"] = i
            chunk["is_unique"] = True
        
        return unique_chunks
```

## Examples

### Example 1: Complete Document Processing Pipeline

```python
from typing import List, Dict
import hashlib

class DocumentProcessor:
    """
    Complete pipeline for processing documents into chunks.
    """
    
    def __init__(self, config: dict = None):
        self.config = config or {
            "chunk_size": 500,
            "chunk_overlap": 50,
            "strategy": "auto",  # auto-select based on content
            "add_metadata": True,
            "deduplicate": True
        }
        
        self.chunkers = {
            "fixed": FixedSizeChunker,
            "token": TokenChunker,
            "sentence": SentenceChunker,
            "paragraph": ParagraphChunker,
            "recursive": RecursiveChunker,
            "markdown": MarkdownChunker,
            "code": CodeChunker
        }
    
    def process_document(
        self,
        content: str,
        document_id: str,
        metadata: dict = None
    ) -> List[dict]:
        """Process document into searchable chunks."""
        
        # Auto-detect best strategy
        strategy = self._detect_strategy(content, metadata)
        
        # Get appropriate chunker
        chunker_class = self.chunkers.get(
            strategy, 
            FixedSizeChunker
        )
        
        chunker = self._create_chunker(chunker_class)
        
        # Create chunks
        chunks = chunker.chunk(content)
        
        # Add document metadata
        if self.config.get("add_metadata", True):
            chunks = self._add_metadata(
                chunks, 
                document_id, 
                metadata or {},
                strategy
            )
        
        # Deduplicate if enabled
        if self.config.get("deduplicate", True):
            chunks = self._deduplicate(chunks)
        
        # Generate embeddings (placeholder)
        # embeddings = self._generate_embeddings([c["text"] for c in chunks])
        
        return chunks
    
    def _detect_strategy(self, content: str, metadata: dict = None) -> str:
        """Auto-detect best chunking strategy."""
        if metadata and metadata.get("content_type"):
            return metadata["content_type"]
        
        # Detect from content
        if "```" in content or "def " in content:
            return "code"
        elif content.startswith("#"):
            return "markdown"
        elif "\n\n" in content and len(content) > 1000:
            return "paragraph"
        else:
            return "recursive"
    
    def _create_chunker(self, chunker_class) -> object:
        """Create configured chunker instance."""
        chunk_size = self.config.get("chunk_size", 500)
        chunk_overlap = self.config.get("chunk_overlap", 50)
        
        if chunker_class == FixedSizeChunker:
            return chunker_class(chunk_size, chunk_overlap)
        elif chunker_class == TokenChunker:
            return chunker_class(
                chunk_size=256,
                chunk_overlap=32
            )
        elif chunker_class == MarkdownChunker:
            return chunker_class(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
        else:
            return chunker_class()
    
    def _add_metadata(
        self,
        chunks: List[dict],
        document_id: str,
        metadata: dict,
        strategy: str
    ) -> List[dict]:
        """Add metadata to chunks."""
        for i, chunk in enumerate(chunks):
            chunk.update({
                "document_id": document_id,
                "chunk_id": f"{document_id}_{i}",
                "chunk_hash": hashlib.md5(
                    chunk["text"].encode()
                ).hexdigest(),
                "strategy": strategy,
                **metadata
            })
        
        return chunks
    
    def _deduplicate(self, chunks: List[dict]) -> List[dict]:
        """Remove duplicate chunks."""
        seen = set()
        unique = []
        
        for chunk in chunks:
            if chunk["chunk_hash"] not in seen:
                seen.add(chunk["chunk_hash"])
                chunk["is_duplicate"] = False
                unique.append(chunk)
            else:
                chunk["is_duplicate"] = True
        
        # Re-index
        for i, chunk in enumerate(unique):
            chunk["chunk_index"] = i
        
        return unique


# Usage
processor = DocumentProcessor({
    "chunk_size": 500,
    "chunk_overlap": 50,
    "strategy": "auto"
})

chunks = processor.process_document(
    content=document_text,
    document_id="doc_123",
    metadata={
        "title": "Introduction to RAG",
        "source": "company-docs"
    }
)
```

### Example 2: Streaming Chunk Processing

```python
class StreamingChunkProcessor:
    """
    Process documents in streaming fashion for large files.
    """
    
    def __init__(
        self,
        chunk_size: int = 500,
        overlap_size: int = 50
    ):
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
    
    def process_stream(self, text_stream) -> List[dict]:
        """
        Process text from a stream/generator.
        """
        buffer = ""
        chunks = []
        chunk_index = 0
        
        for chunk in text_stream:
            buffer += chunk
            
            while len(buffer) >= self.chunk_size:
                # Extract chunk
                chunk_text = buffer[:self.chunk_size]
                
                # Find good split point
                split_point = self._find_split_point(chunk_text)
                
                final_chunk = chunk_text[:split_point]
                chunks.append({
                    "text": final_chunk,
                    "chunk_index": chunk_index
                })
                
                chunk_index += 1
                
                # Keep overlap in buffer
                buffer = buffer[split_point - self.overlap_size:]
        
        # Process remaining buffer
        if buffer.strip():
            chunks.append({
                "text": buffer.strip(),
                "chunk_index": chunk_index
            })
        
        return chunks
    
    def _find_split_point(self, text: str) -> int:
        """Find a good split point (not mid-sentence)."""
        split_points = [
            text.rfind(". "),
            text.rfind("\n"),
            text.rfind(" "),
        ]
        
        for point in split_points:
            if point > self.chunk_size * 0.7:  # At least 70% of chunk size
                return point + 1
        
        return self.chunk_size


# Usage with file streaming
def read_file_in_chunks(filepath: str, chunk_size: int = 8192):
    """Generator yielding file chunks."""
    with open(filepath, 'r', encoding='utf-8') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

processor = StreamingChunkProcessor(chunk_size=500)
chunks = processor.process_stream(
    read_file_in_chunks("large_document.txt")
)
```

## References

1. **LangChain Text Splitters**: https://python.langchain.com/docs/modules/data_connection/document_transformers/
2. **Chunking Best Practices**: https://docs.llamaindex.ai/en/latest/core_modules/data_modules/indexing/metadata_extraction.html
3. **NLTK Documentation**: https://www.nltk.org/
4. **tiktoken**: https://github.com/openai/tiktoken
5. **Cursor Enterprise Framework - RAG Rules**: `.cursor/rules/rag.mdc`
