---
title: "Embedding Models - Text Embeddings và Semantic Search"
description: "Hướng dẫn toàn diện về text embeddings trong Gemini API, bao gồm các task types (RETRIEVAL_DOCUMENT, RETRIEVAL_QUERY, SEMANTIC_SIMILARITY), batch embedding, và production patterns cho semantic search"
tags:
  - "gemini"
  - "embeddings"
  - "text-embeddings"
  - "semantic-search"
  - "vector-search"
  - "retrieval"
  - "similarity"
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Embedding Models - Text Embeddings và Semantic Search

## Tổng Quan (Overview)

Text embeddings là kỹ thuật chuyển đổi text thành các vectors (mảng số) trong một không gian liên tục, sao cho các texts có ý nghĩa tương tự sẽ có vị trí gần nhau trong không gian vector. Đây là nền tảng cho rất nhiều ứng dụng AI hiện đại: semantic search, document retrieval, clustering, recommendation systems, và RAG (Retrieval-Augmented Generation).

Gemini API cung cấp embedding models cho phép developers tạo embeddings từ text với các task types khác nhau, tối ưu hóa cho different use cases. Khác với general-purpose models, task-specific embeddings được trained để perform better trong các scenarios cụ thể.

Việc sử dụng embeddings hiệu quả đòi hỏi:

- Hiểu các task types khác nhau và khi nào sử dụng
- Biết cách preprocess và chunk text phù hợp
- Nắm vững cách store và search với vector databases
- Design patterns cho production RAG systems

Trong tài liệu này, chúng ta sẽ khám phá chi tiết về embedding models của Gemini, các task types, và cách xây dựng các production-grade semantic search systems.

## Mục Đích (Purpose)

**1. Hiểu Rõ Embedding Task Types**

Cung cấp kiến thức chi tiết về RETRIEVAL_DOCUMENT, RETRIEVAL_QUERY, và SEMANTIC_SIMILARITY - mỗi task type có đặc điểm riêng và phù hợp với different use cases. Hiểu rõ sự khác biệt giúp select đúng task type.

**2. Nắm Vững Chunking Strategies**

Hướng dẫn các chiến lược chunking text hiệu quả để tạo ra embeddings chất lượng cao, bao gồm fixed-size chunking, semantic chunking, và hierarchical approaches.

**3. Xây Dựng Production Semantic Search Systems**

Cung cấp patterns và architectures thực tế cho việc xây dựng semantic search systems với vector storage, efficient similarity search, và hybrid search combining keyword và semantic approaches.

## Các Khái Niệm Cốt Lõi (Key Concepts)

### 1. Embedding Fundamentals

**Embedding là gì?**

Embedding là một vector representation của text trong không gian nhiều chiều. Mỗi dimension của vector đại diện cho một feature semantic nào đó của text. Điều quan trọng là: texts có ý nghĩa tương tự sẽ có embeddings gần nhau trong không gian vector.

```python
# Ví dụ đơn giản về embedding concept

# Giả sử chúng ta có 3 texts:
# Text 1: "How do I reset my password?"
# Text 2: "I forgot my password, how to recover?"
# Text 3: "What's the weather today?"

# Trong không gian 2D (đơn giản hóa):
# Embedding 1: [0.2, 0.8]  (password-related)
# Embedding 2: [0.3, 0.7]  (password-related - gần Embedding 1)
# Embedding 3: [0.9, 0.1]  (weather-related - xa Embedding 1 và 2)

# Khoảng cách cosine:
# similarity(Embedding 1, Embedding 2) = HIGH (cùng chủ đề)
# similarity(Embedding 1, Embedding 3) = LOW (khác chủ đề)
```

**Tại sao Embeddings quan trọng?**

- **Semantic Understanding**: Hiểu ý nghĩa, không chỉ keywords
- **Analogies**: King - Man + Woman = Queen (vector arithmetic)
- **Clustering**: Tự động nhóm texts tương tự
- **Search**: Tìm kiếm theo ý nghĩa, không chỉ exact matches

### 2. Task Types Trong Gemini Embeddings

```python
# src/embeddings/task_types.py
"""
Embedding Task Types cho Gemini
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List


class EmbeddingTaskType(Enum):
    """
    Các loại task cho embedding.
    Mỗi task type được tối ưu hóa cho một use case cụ thể.
    """
    
    # RETRIEVAL_DOCUMENT - Dùng để embed documents
    # Được tối ưu hóa để represent documents trong retrieval systems
    # Thường được dùng khi index documents vào vector database
    RETRIEVAL_DOCUMENT = "RETRIEVAL_DOCUMENT"
    
    # RETRIEVAL_QUERY - Dùng để embed user queries
    # Được tối ưu hóa để match với documents
    # Thường được dùng khi user search/query
    RETRIEVAL_QUERY = "RETRIEVAL_QUERY"
    
    # SEMANTIC_SIMILARITY - Dùng để so sánh semantic similarity
    # Được tối ưu hóa để compute similarity scores
    # Thường dùng cho recommendation, duplicate detection
    SEMANTIC_SIMILARITY = "SEMANTIC_SIMILARITY"
    
    # CLASSIFICATION - Dùng để phân loại text
    # Được tối ưu hóa để sử dụng với classifiers
    # Output có thể được dùng trực tiếp cho classification
    CLASSIFICATION = "CLASSIFICATION"
    
    # CLUSTERING - Dùng để cluster texts
    # Được tối ưu hóa để group similar items
    # Good cho topic modeling, document organization
    CLUSTERING = "CLUSTERING"


@dataclass
class EmbeddingTaskConfig:
    """
    Cấu hình cho một embedding task.
    """
    task_type: EmbeddingTaskType
    title: Optional[str] = None  # Cho RETRIEVAL_DOCUMENT
    query: Optional[str] = None  # Cho RETRIEVAL_QUERY
    
    # Output options
    output_dimension: Optional[int] = None  # 768, 512, 256, etc.
    
    # Advanced options
    normalized: bool = True  # Normalize output vectors
    include_timestamp: bool = False  # Include timestamp embeddings


# Task Type Descriptions
TASK_TYPE_DESCRIPTIONS = {
    EmbeddingTaskType.RETRIEVAL_DOCUMENT: """
        RETRIEVAL_DOCUMENT được sử dụng để embed các documents hoặc passages.
        
        Đặc điểm:
        - Tối ưu hóa để represent nội dung document
        - Thường được dùng khi indexing documents vào vector database
        - Có thể include title để improve representation
        - Embeddings thường có dimension cao hơn
        
        Use cases:
        - Document indexing
        - Semantic search (documents)
        - Knowledge base building
        - RAG document storage
    """,
    
    EmbeddingTaskType.RETRIEVAL_QUERY: """
        RETRIEVAL_QUERY được sử dụng để embed user queries hoặc questions.
        
        Đặc điểm:
        - Tối ưu hóa để match với documents
        - Thường được dùng khi user nhập search query
        - Ngắn hơn documents, focus vào search intent
        - được trained để align với RETRIEVAL_DOCUMENT space
        
        Use cases:
        - User search queries
        - Question answering
        - Chat message embeddings
        - Query-document matching
    """,
    
    EmbeddingTaskType.SEMANTIC_SIMILARITY: """
        SEMANTIC_SIMILARITY được sử dụng để compute similarity giữa texts.
        
        Đặc điểm:
        - Tối ưu hóa để compare texts directly
        - Good cho symmetric similarity (text A vs text B)
        - Không cần query-document distinction
        - Độ chính xác cao trong similarity scoring
        
        Use cases:
        - Duplicate detection
        - Recommendation systems
        - Paraphrase identification
        - Semantic clustering
    """,
    
    EmbeddingTaskType.CLASSIFICATION: """
        CLASSIFICATION được sử dụng cho text classification tasks.
        
        Đặc điểm:
        - Tối ưu hóa để sử dụng với classifiers
        - Embeddings phù hợp cho linear classifiers
        - Thường dùng kèm với classification labels
        
        Use cases:
        - Text classification
        - Sentiment analysis
        - Topic classification
        - Content moderation
    """,
    
    EmbeddingTaskType.CLUSTERING: """
        CLUSTERING được sử dụng để cluster groups of texts.
        
        Đặc điểm:
        - Tối ưu hóa để group similar items
        - Good cho unsupervised learning
        - Maintain separation between clusters
        
        Use cases:
        - Topic modeling
        - Document organization
        - Customer feedback grouping
        - Anomaly detection
    """,
}


def get_task_config(
    task_type: EmbeddingTaskType,
    title: Optional[str] = None,
    query: Optional[str] = None
) -> EmbeddingTaskConfig:
    """
    Helper để tạo task config nhanh.
    """
    return EmbeddingTaskConfig(
        task_type=task_type,
        title=title,
        query=query,
    )
```

### 3. Embedding API Usage

```python
# src/embeddings/embedding_client.py
"""
Embedding Client cho Gemini
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
import numpy as np

from google.generativeai import embed_content


@dataclass
class EmbeddingResult:
    """Kết quả từ embedding request."""
    embedding: List[float]
    tokens: int
    
    def to_list(self) -> List[float]:
        """Convert to list."""
        return self.embedding
    
    def to_numpy(self) -> np.ndarray:
        """Convert to numpy array."""
        return np.array(self.embedding)
    
    @property
    def dimension(self) -> int:
        """Get embedding dimension."""
        return len(self.embedding)


@dataclass
class BatchEmbeddingResult:
    """Kết quả từ batch embedding request."""
    embeddings: List[List[float]]
    tokens_per_text: List[int]
    
    def __len__(self) -> int:
        return len(self.embeddings)
    
    def __getitem__(self, index: int) -> EmbeddingResult:
        return EmbeddingResult(
            embedding=self.embeddings[index],
            tokens=self.tokens_per_text[index]
        )


class GeminiEmbeddingClient:
    """
    Client để tạo embeddings với Gemini.
    """
    
    def __init__(
        self,
        model: str = "models/embedding-001",
        api_key: Optional[str] = None
    ):
        self.model = model
        self.api_key = api_key
        self._configure()
    
    def _configure(self) -> None:
        """Configure API."""
        import os
        from google.generativeai import configure
        
        if self.api_key:
            configure(api_key=self.api_key)
        elif os.getenv("GEMINI_API_KEY"):
            configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    def embed(
        self,
        content: str,
        task_type: str = "RETRIEVAL_DOCUMENT",
        title: Optional[str] = None,
        normalized: bool = True
    ) -> EmbeddingResult:
        """
        Tạo embedding cho một text.
        
        Args:
            content: Text cần embed
            task_type: Task type (RETRIEVAL_DOCUMENT, RETRIEVAL_QUERY, etc.)
            title: Optional title (cho documents)
            normalized: Normalize output vector
            
        Returns:
            EmbeddingResult object
        """
        config = {
            "task_type": task_type,
            "normalized": normalized,
        }
        
        if title:
            config["title"] = title
        
        response = embed_content(
            model=self.model,
            content=content,
            task_type=task_type,
            title=title,
        )
        
        return EmbeddingResult(
            embedding=response["embedding"],
            tokens=response.get("token_count", 0)
        )
    
    def embed_query(self, query: str) -> EmbeddingResult:
        """
        Tạo embedding cho một query.
        Shortcut cho embed với task_type=RETRIEVAL_QUERY.
        """
        return self.embed(
            content=query,
            task_type="RETRIEVAL_QUERY"
        )
    
    def embed_document(
        self,
        content: str,
        title: Optional[str] = None
    ) -> EmbeddingResult:
        """
        Tạo embedding cho một document.
        Shortcut cho embed với task_type=RETRIEVAL_DOCUMENT.
        """
        return self.embed(
            content=content,
            task_type="RETRIEVAL_DOCUMENT",
            title=title
        )
    
    def embed_for_similarity(
        self,
        content: str
    ) -> EmbeddingResult:
        """
        Tạo embedding cho semantic similarity.
        """
        return self.embed(
            content=content,
            task_type="SEMANTIC_SIMILARITY"
        )
    
    def embed_batch(
        self,
        texts: List[str],
        task_type: str = "RETRIEVAL_DOCUMENT",
        title: Optional[str] = None,
        batch_size: int = 100,
        show_progress: bool = False
    ) -> BatchEmbeddingResult:
        """
        Tạo embeddings cho nhiều texts.
        
        Args:
            texts: List of texts
            task_type: Task type
            title: Optional title for all (or None for per-text)
            batch_size: Batch size cho API calls
            show_progress: Show progress
            
        Returns:
            BatchEmbeddingResult object
        """
        all_embeddings = []
        all_tokens = []
        
        total_batches = (len(texts) + batch_size - 1) // batch_size
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_num = i // batch_size + 1
            
            if show_progress:
                print(f"Processing batch {batch_num}/{total_batches}")
            
            # Process each text in batch
            batch_embeddings = []
            batch_tokens = []
            
            for text in batch:
                try:
                    result = self.embed(
                        content=text,
                        task_type=task_type,
                        title=title
                    )
                    batch_embeddings.append(result.embedding)
                    batch_tokens.append(result.tokens)
                except Exception as e:
                    print(f"Error embedding text: {e}")
                    # Return zero vector as fallback
                    batch_embeddings.append([0.0] * 768)  # Default dimension
                    batch_tokens.append(0)
            
            all_embeddings.extend(batch_embeddings)
            all_tokens.extend(batch_tokens)
        
        return BatchEmbeddingResult(
            embeddings=all_embeddings,
            tokens_per_text=all_tokens
        )
```

```typescript
// src/embeddings/embedding-client.ts
/**
 * Embedding Client cho Gemini (TypeScript)
 */

import { GoogleGenerativeAI, TaskType } from '@google/generative-ai';

export interface EmbeddingResult {
  embedding: number[];
  tokens: number;
  
  toArray(): number[];
  getDimension(): number;
}

export interface BatchEmbeddingResult {
  embeddings: number[][];
  tokensPerText: number[];
  
  length: number;
  get(index: number): EmbeddingResult;
}

export class GeminiEmbeddingClient {
  private model: string;
  private client: GoogleGenerativeAI;
  
  constructor(apiKey: string, model: string = 'models/embedding-001') {
    this.model = model;
    this.client = new GoogleGenerativeAI(apiKey);
  }
  
  /**
   * Tạo embedding cho một text
   */
  async embed(
    content: string,
    options: {
      taskType?: TaskType;
      title?: string;
      normalized?: boolean;
    } = {}
  ): Promise<EmbeddingResult> {
    const { taskType = TaskType.RETRIEVAL_DOCUMENT, title, normalized = true } = options;
    
    const result = await this.client.embedContent({
      model: this.model,
      content: {
        role: 'user',
        parts: [{ text: content }],
      },
      taskType,
      title,
      outputDimensionality: normalized ? 768 : undefined,
    });
    
    return {
      embedding: result.embedding?.values || [],
      tokens: 0, // Token count not always returned
      
      toArray(): number[] {
        return this.embedding;
      },
      
      getDimension(): number {
        return this.embedding.length;
      },
    };
  }
  
  /**
   * Tạo embedding cho query
   */
  async embedQuery(query: string): Promise<EmbeddingResult> {
    return this.embed(query, {
      taskType: TaskType.RETRIEVAL_QUERY,
    });
  }
  
  /**
   * Tạo embedding cho document
   */
  async embedDocument(
    content: string,
    title?: string
  ): Promise<EmbeddingResult> {
    return this.embed(content, {
      taskType: TaskType.RETRIEVAL_DOCUMENT,
      title,
    });
  }
  
  /**
   * Tạo embedding cho similarity
   */
  async embedForSimilarity(content: string): Promise<EmbeddingResult> {
    return this.embed(content, {
      taskType: TaskType.SEMANTIC_SIMILARITY,
    });
  }
  
  /**
   * Tạo embeddings cho nhiều texts
   */
  async embedBatch(
    texts: string[],
    options: {
      taskType?: TaskType;
      title?: string;
      batchSize?: number;
      onProgress?: (progress: { completed: number; total: number }) => void;
    } = {}
  ): Promise<BatchEmbeddingResult> {
    const {
      taskType = TaskType.RETRIEVAL_DOCUMENT,
      title,
      batchSize = 100,
      onProgress,
    } = options;
    
    const allEmbeddings: number[][] = [];
    const allTokens: number[] = [];
    
    const totalBatches = Math.ceil(texts.length / batchSize);
    
    for (let i = 0; i < texts.length; i += batchSize) {
      const batch = texts.slice(i, i + batchSize);
      const batchNum = Math.floor(i / batchSize) + 1;
      
      if (onProgress) {
        onProgress({ completed: i, total: texts.length });
      }
      
      // Process batch
      const batchPromises = batch.map(text => 
        this.embed(text, { taskType, title })
          .catch(err => {
            console.error(`Error embedding text: ${err}`);
            return {
              embedding: new Array(768).fill(0),
              tokens: 0,
            };
          })
      );
      
      const batchResults = await Promise.all(batchPromises);
      
      for (const result of batchResults) {
        allEmbeddings.push(result.embedding);
        allTokens.push(result.tokens);
      }
    }
    
    if (onProgress) {
      onProgress({ completed: texts.length, total: texts.length });
    }
    
    return {
      embeddings: allEmbeddings,
      tokensPerText: allTokens,
      
      length: allEmbeddings.length,
      
      get(index: number): EmbeddingResult {
        return {
          embedding: this.embeddings[index],
          tokens: this.tokensPerText[index],
          toArray(): number[] {
            return this.embedding;
          },
          getDimension(): number {
            return this.embedding.length;
          },
        };
      },
    };
  }
}
```

## Best Practices

### 1. Text Chunking Strategies

```python
# src/embeddings/chunking.py
"""
Text Chunking Strategies cho Embeddings
"""

from typing import List, Dict, Any, Optional, Callable, Iterator
from dataclasses import dataclass
import re


@dataclass
class Chunk:
    """Một chunk của text."""
    id: str
    content: str
    start_char: int
    end_char: int
    tokens: int
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def length(self) -> int:
        """Character length."""
        return self.end_char - self.start_char


class ChunkingStrategy(ABC):
    """Abstract base class cho chunking strategies."""
    
    @abstractmethod
    def chunk(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Chunk]:
        """Chunk text thành list of Chunks."""
        pass
    
    @abstractmethod
    def estimate_tokens(self, text: str) -> int:
        """Estimate tokens cho text."""
        pass


class FixedSizeChunker(ChunkingStrategy):
    """
    Chunk text theo fixed size (characters hoặc tokens).
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        count_by: str = "characters"  # "characters" or "tokens"
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.count_by = count_by
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate tokens (~4 chars per token)."""
        return (len(text) + 3) // 4
    
    def chunk(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Chunk]:
        """Chunk text với fixed size."""
        chunks = []
        
        if self.count_by == "characters":
            chunks = self._chunk_by_characters(text)
        else:
            chunks = self._chunk_by_tokens(text)
        
        # Add metadata
        if metadata:
            for chunk in chunks:
                chunk.metadata = {**metadata, **chunk.metadata}
        
        return chunks
    
    def _chunk_by_characters(self, text: str) -> List[Chunk]:
        """Chunk by character count."""
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence ending
                for sep in ['. ', '! ', '? ', '.\n', '!\n', '?\n']:
                    last_sep = text.rfind(sep, start + self.chunk_size // 2, end)
                    if last_sep > start:
                        end = last_sep + len(sep)
                        break
            
            chunk = Chunk(
                id=f"chunk_{chunk_id}",
                content=text[start:end].strip(),
                start_char=start,
                end_char=end,
                tokens=self.estimate_tokens(text[start:end])
            )
            
            if chunk.content:  # Skip empty chunks
                chunks.append(chunk)
            
            chunk_id += 1
            start = end - self.chunk_overlap
        
        return chunks
    
    def _chunk_by_tokens(self, text: str) -> List[Chunk]:
        """Chunk by token count (approximate)."""
        # For simplicity, convert to chars and chunk
        # In production, use actual token counting
        char_size = self.chunk_size * 4  # ~4 chars per token
        char_overlap = self.chunk_overlap * 4
        
        return self._chunk_by_characters(text)


class SemanticChunker(ChunkStrategy):
    """
    Chunk text dựa trên semantic boundaries.
    """
    
    def __init__(
        self,
        max_tokens: int = 500,
        min_tokens: int = 100,
        overlap_tokens: int = 50
    ):
        self.max_tokens = max_tokens
        self.min_tokens = min_tokens
        self.overlap_tokens = overlap_tokens
    
    def estimate_tokens(self, text: str) -> int:
        return (len(text) + 3) // 4
    
    def chunk(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Chunk]:
        """Chunk text dựa trên semantic units."""
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for para in paragraphs:
            para_tokens = self.estimate_tokens(para)
            
            # If single paragraph is too large
            if para_tokens > self.max_tokens:
                # Flush current
                if current_chunk:
                    chunks.extend(self._create_chunks(current_chunk, metadata))
                    current_chunk = []
                    current_tokens = 0
                
                # Split large paragraph
                chunks.extend(self._split_large_paragraph(para, metadata))
            
            # Check if adding this paragraph exceeds limit
            elif current_tokens + para_tokens > self.max_tokens:
                # Create chunk from current
                if current_tokens >= self.min_tokens:
                    chunks.extend(self._create_chunks(current_chunk, metadata))
                
                # Start new chunk with overlap
                overlap_text = ' '.join(current_chunk[-2:]) if len(current_chunk) > 1 else ''
                current_chunk = [overlap_text, para] if overlap_text else [para]
                current_tokens = self.estimate_tokens(' '.join(current_chunk))
            else:
                current_chunk.append(para)
                current_tokens += para_tokens
        
        # Flush remaining
        if current_chunk and current_tokens >= self.min_tokens:
            chunks.extend(self._create_chunks(current_chunk, metadata))
        
        return chunks
    
    def _create_chunks(
        self,
        paragraphs: List[str],
        metadata: Optional[Dict[str, Any]]
    ) -> List[Chunk]:
        """Create chunks từ paragraphs."""
        content = '\n\n'.join(paragraphs)
        
        return [
            Chunk(
                id=f"chunk_{hash(content) % 1000000}",
                content=content.strip(),
                start_char=0,
                end_char=len(content),
                tokens=self.estimate_tokens(content),
                metadata=metadata or {}
            )
        ]
    
    def _split_large_paragraph(
        self,
        paragraph: str,
        metadata: Optional[Dict[str, Any]]
    ) -> List[Chunk]:
        """Split large paragraph by sentences."""
        # Split by sentences
        sentences = re.split(r'(?<=[.!?])\s+', paragraph)
        
        chunks = []
        current_sentences = []
        current_tokens = 0
        
        for sentence in sentences:
            sentence_tokens = self.estimate_tokens(sentence)
            
            if current_tokens + sentence_tokens > self.max_tokens:
                if current_sentences:
                    chunks.extend(self._create_chunks(current_sentences, metadata))
                
                current_sentences = [sentence]
                current_tokens = sentence_tokens
            else:
                current_sentences.append(sentence)
                current_tokens += sentence_tokens
        
        if current_sentences:
            chunks.extend(self._create_chunks(current_sentences, metadata))
        
        return chunks


class RecursiveCharacterChunker(ChunkingStrategy):
    """
    Recursive character chunking với multiple separators.
    """
    
    def __init__(
        self,
        separators: List[str] = None,
        chunk_size: int = 1000,
        overlap: int = 200
    ):
        self.separators = separators or ['\n\n', '\n', '. ', ' ']
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def estimate_tokens(self, text: str) -> int:
        return (len(text) + 3) // 4
    
    def chunk(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Chunk]:
        """Chunk text recursively."""
        chunks = []
        self._chunk_recursive(
            text,
            0,
            chunks,
            metadata or {}
        )
        return chunks
    
    def _chunk_recursive(
        self,
        text: str,
        chunk_num: int,
        chunks: List[Chunk],
        metadata: Dict[str, Any]
    ) -> None:
        """Recursive chunking."""
        if len(text) <= self.chunk_size:
            if text.strip():
                chunks.append(Chunk(
                    id=f"chunk_{chunk_num}",
                    content=text.strip(),
                    start_char=0,
                    end_char=len(text),
                    tokens=self.estimate_tokens(text),
                    metadata=metadata
                ))
            return
        
        # Try separators in order
        for separator in self.separators:
            if separator in text:
                parts = text.split(separator)
                current = ""
                
                for i, part in enumerate(parts):
                    test = current + separator + part if current else part
                    
                    if self.estimate_tokens(test) > self.chunk_size:
                        if current.strip():
                            chunks.append(Chunk(
                                id=f"chunk_{chunk_num}",
                                content=current.strip(),
                                start_char=0,
                                end_char=len(current),
                                tokens=self.estimate_tokens(current),
                                metadata=metadata
                            ))
                            chunk_num += 1
                        
                        current = part
                    else:
                        current = test
                
                # Process remaining
                if current.strip():
                    chunks.append(Chunk(
                        id=f"chunk_{chunk_num}",
                        content=current.strip(),
                        start_char=0,
                        end_char=len(current),
                        tokens=self.estimate_tokens(current),
                        metadata=metadata
                    ))
                
                return
        
        # No separator worked, force chunk
        for i in range(0, len(text), self.chunk_size - self.overlap):
            chunk_text = text[i:i + self.chunk_size]
            chunks.append(Chunk(
                id=f"chunk_{chunk_num}",
                content=chunk_text.strip(),
                start_char=i,
                end_char=i + len(chunk_text),
                tokens=self.estimate_tokens(chunk_text),
                metadata=metadata
            ))
            chunk_num += 1
```

### 2. Vector Similarity Functions

```python
# src/embeddings/similarity.py
"""
Vector Similarity Functions
"""

import numpy as np
from typing import List, Union, Tuple


def cosine_similarity(
    v1: Union[List[float], np.ndarray],
    v2: Union[List[float], np.ndarray]
) -> float:
    """
    Tính cosine similarity giữa hai vectors.
    
    Cosine similarity = (A · B) / (||A|| × ||B||)
    Range: -1 to 1 (1 = identical, 0 = orthogonal, -1 = opposite)
    
    Args:
        v1: Vector 1
        v2: Vector 2
        
    Returns:
        Cosine similarity score
    """
    v1 = np.array(v1)
    v2 = np.array(v2)
    
    # Handle zero vectors
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return np.dot(v1, v2) / (norm1 * norm2)


def euclidean_distance(
    v1: Union[List[float], np.ndarray],
    v2: Union[List[float], np.ndarray]
) -> float:
    """
    Tính Euclidean distance giữa hai vectors.
    
    Distance = √(Σ(aᵢ - bᵢ)²)
    
    Args:
        v1: Vector 1
        v2: Vector 2
        
    Returns:
        Euclidean distance
    """
    v1 = np.array(v1)
    v2 = np.array(v2)
    
    return float(np.linalg.norm(v1 - v2))


def dot_product(
    v1: Union[List[float], np.ndarray],
    v2: Union[List[float], np.ndarray]
) -> float:
    """
    Tính dot product giữa hai vectors.
    """
    v1 = np.array(v1)
    v2 = np.array(v2)
    
    return float(np.dot(v1, v2))


def manhattan_distance(
    v1: Union[List[float], np.ndarray],
    v2: Union[List[float], np.ndarray]
) -> float:
    """
    Tính Manhattan (L1) distance.
    
    Distance = Σ|aᵢ - bᵢ|
    """
    v1 = np.array(v1)
    v2 = np.array(v2)
    
    return float(np.sum(np.abs(v1 - v2)))


def cosine_to_distance(cosine_sim: float) -> float:
    """
    Convert cosine similarity sang distance.
    distance = 1 - similarity
    """
    return 1.0 - cosine_sim


class VectorStore:
    """
    Simple in-memory vector store cho similarity search.
    """
    
    def __init__(
        self,
        dimension: int = 768,
        metric: str = "cosine"  # "cosine", "euclidean", "dot"
    ):
        self.dimension = dimension
        self.metric = metric
        self.vectors: List[np.ndarray] = []
        self.metadata: List[dict] = []
        self._index = None  # For future FAISS integration
    
    def add(
        self,
        vector: Union[List[float], np.ndarray],
        metadata: Optional[dict] = None
    ) -> int:
        """
        Add vector to store.
        
        Returns:
            Index of added vector
        """
        vector = np.array(vector)
        
        if len(vector) != self.dimension:
            raise ValueError(
                f"Vector dimension {len(vector)} != expected {self.dimension}"
            )
        
        self.vectors.append(vector)
        self.metadata.append(metadata or {})
        
        return len(self.vectors) - 1
    
    def add_batch(
        self,
        vectors: List[Union[List[float], np.ndarray]],
        metadata_list: Optional[List[dict]] = None
    ) -> List[int]:
        """Add multiple vectors."""
        indices = []
        
        for i, vector in enumerate(vectors):
            meta = metadata_list[i] if metadata_list else None
            idx = self.add(vector, meta)
            indices.append(idx)
        
        return indices
    
    def search(
        self,
        query_vector: Union[List[float], np.ndarray],
        k: int = 5,
        filter_fn: Optional[callable] = None
    ) -> List[Tuple[int, float, dict]]:
        """
        Search for k nearest vectors.
        
        Returns:
            List of (index, score, metadata) tuples
        """
        query = np.array(query_vector)
        
        if len(query) != self.dimension:
            raise ValueError(
                f"Query dimension {len(query)} != expected {self.dimension}"
            )
        
        # Calculate similarities
        results = []
        
        for i, vector in enumerate(self.vectors):
            # Apply filter if provided
            if filter_fn and not filter_fn(self.metadata[i]):
                continue
            
            # Calculate score based on metric
            if self.metric == "cosine":
                score = cosine_similarity(query, vector)
            elif self.metric == "euclidean":
                score = -euclidean_distance(query, vector)  # Negative for min
            elif self.metric == "dot":
                score = dot_product(query, vector)
            else:
                raise ValueError(f"Unknown metric: {self.metric}")
            
            results.append((i, score, self.metadata[i]))
        
        # Sort by score (descending for cosine/dot, ascending for euclidean)
        if self.metric == "euclidean":
            results.sort(key=lambda x: x[1])  # Lower is better
        else:
            results.sort(key=lambda x: x[1], reverse=True)  # Higher is better
        
        return results[:k]
    
    def search_by_text(
        self,
        query_embedding: Union[List[float], np.ndarray],
        k: int = 5,
        min_score: float = 0.0
    ) -> List[dict]:
        """
        Search và return only metadata.
        """
        results = self.search(query_embedding, k * 2)  # Get more to filter
        
        filtered = [
            {
                **meta,
                "score": score,
                "index": idx
            }
            for idx, score, meta in results
            if score >= min_score
        ][:k]
        
        return filtered
    
    def count(self) -> int:
        """Get number of vectors."""
        return len(self.vectors)
    
    def clear(self) -> None:
        """Clear all vectors."""
        self.vectors = []
        self.metadata = []
```

## Common Patterns

### 1. RAG (Retrieval-Augmented Generation) System

```python
# src/rag/rag_system.py
"""
RAG System - Retrieval-Augmented Generation với Gemini
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import hashlib

from src.embeddings.embedding_client import GeminiEmbeddingClient
from src.embeddings.chunking import Chunk, ChunkingStrategy, RecursiveCharacterChunker
from src.embeddings.similarity import VectorStore, cosine_similarity


@dataclass
class Document:
    """Một document trong RAG system."""
    id: str
    content: str
    title: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.id:
            self.id = hashlib.md5(self.content.encode()).hexdigest()[:12]


@dataclass
class RetrievedChunk:
    """Một chunk đã được retrieve."""
    content: str
    document_id: str
    document_title: Optional[str]
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RAGConfig:
    """Cấu hình cho RAG system."""
    embedding_model: str = "models/embedding-001"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 5
    min_similarity_score: float = 0.5
    enable_reranking: bool = False


class RAGVectorStore:
    """
    Vector store cho RAG system.
    """
    
    def __init__(self, dimension: int = 768):
        self.dimension = dimension
        self.store = VectorStore(dimension=dimension, metric="cosine")
        self.chunks: Dict[int, Chunk] = {}
        self.documents: Dict[str, Document] = {}
    
    def add_document(
        self,
        document: Document,
        chunker: ChunkingStrategy,
        embed_client: GeminiEmbeddingClient
    ) -> int:
        """
        Add document to store.
        
        Returns:
            Number of chunks added
        """
        # Store document
        self.documents[document.id] = document
        
        # Chunk document
        chunks = chunker.chunk(
            document.content,
            metadata={
                "document_id": document.id,
                "title": document.title,
                **document.metadata
            }
        )
        
        # Embed chunks
        chunk_texts = [c.content for c in chunks]
        
        batch_result = embed_client.embed_batch(
            chunk_texts,
            task_type="RETRIEVAL_DOCUMENT",
            title=document.title
        )
        
        # Add to store
        for i, chunk in enumerate(chunks):
            idx = self.store.add(
                batch_result.embeddings[i],
                metadata={
                    "chunk_id": chunk.id,
                    "document_id": document.id,
                    "content": chunk.content,
                    "title": document.title,
                    **chunk.metadata
                }
            )
            self.chunks[idx] = chunk
        
        return len(chunks)
    
    def retrieve(
        self,
        query: str,
        embed_client: GeminiEmbeddingClient,
        top_k: int = 5,
        min_score: float = 0.0,
        filter_fn: Optional[Callable[[dict], bool]] = None
    ) -> List[RetrievedChunk]:
        """
        Retrieve relevant chunks cho query.
        """
        # Embed query
        query_result = embed_client.embed_query(query)
        
        # Search
        results = self.store.search(
            query_result.embedding,
            k=top_k * 2,  # Get more for filtering
            filter_fn=filter_fn
        )
        
        # Convert to RetrievedChunks
        retrieved = []
        for idx, score, meta in results:
            if score < min_score:
                continue
            
            retrieved.append(RetrievedChunk(
                content=meta.get("content", ""),
                document_id=meta.get("document_id", ""),
                document_title=meta.get("title"),
                score=score,
                metadata=meta
            ))
            
            if len(retrieved) >= top_k:
                break
        
        return retrieved
    
    def count(self) -> tuple[int, int]:
        """Get document and chunk counts."""
        return len(self.documents), len(self.chunks)


class RAGSystem:
    """
    Complete RAG system với Gemini.
    """
    
    def __init__(
        self,
        config: RAGConfig,
        embed_client: Optional[GeminiEmbeddingClient] = None
    ):
        self.config = config
        self.embed_client = embed_client or GeminiEmbeddingClient()
        self.vector_store = RAGVectorStore()
        self.chunker = RecursiveCharacterChunker(
            chunk_size=config.chunk_size,
            overlap=config.chunk_overlap
        )
        self._model = None  # Gemini model for generation
    
    def set_generation_model(self, model) -> None:
        """Set Gemini model cho generation."""
        self._model = model
    
    def add_documents(
        self,
        documents: List[Document],
        show_progress: bool = True
    ) -> int:
        """
        Add multiple documents.
        
        Returns:
            Total chunks added
        """
        total_chunks = 0
        
        for i, doc in enumerate(documents):
            if show_progress:
                print(f"Processing document {i+1}/{len(documents)}: {doc.title or doc.id}")
            
            chunks = self.vector_store.add_document(
                doc,
                self.chunker,
                self.embed_client
            )
            total_chunks += chunks
        
        return total_chunks
    
    def add_documents_from_texts(
        self,
        texts: List[str],
        titles: Optional[List[str]] = None,
        metadatas: Optional[List[dict]] = None
    ) -> int:
        """Add documents from texts."""
        documents = []
        
        for i, text in enumerate(texts):
            doc = Document(
                id=f"doc_{i}",
                content=text,
                title=titles[i] if titles else None,
                metadata=metadatas[i] if metadatas else {}
            )
            documents.append(doc)
        
        return self.add_documents(documents)
    
    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[RetrievedChunk]:
        """
        Retrieve relevant documents cho query.
        """
        k = top_k or self.config.top_k
        
        return self.vector_store.retrieve(
            query,
            self.embed_client,
            top_k=k,
            min_score=self.config.min_similarity_score
        )
    
    def generate(
        self,
        query: str,
        context_override: Optional[List[str]] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate answer sử dụng retrieved context.
        """
        if not self._model:
            raise ValueError("Generation model not set. Call set_generation_model() first.")
        
        # Retrieve context
        if context_override is None:
            retrieved = self.retrieve(query)
            context_parts = [
                f"[Document: {r.document_title or r.document_id}] "
                f"(Score: {r.score:.2f})\n{r.content}"
                for r in retrieved
            ]
            context = "\n\n---\n\n".join(context_parts)
        else:
            context = "\n\n---\n\n".join(context_override)
        
        # Build prompt
        default_system = """Bạn là một AI assistant được thiết kế để trả lời câu hỏi dựa trên ngữ cảnh được cung cấp.

Hướng dẫn:
1. Trả lời dựa trên ngữ cảnh được cung cấp
2. Nếu câu trả lời không có trong ngữ cảnh, hãy nói rõ điều đó
3. Trích dẫn nguồn khi có thể
4. Trả lời bằng tiếng Việt"""

        system = system_prompt or default_system
        
        prompt = f"""Ngữ cảnh:
{context}

Câu hỏi: {query}

Trả lời:"""
        
        # Generate
        response = self._model.generate_content(prompt)
        
        return response.text
    
    async def generate_async(
        self,
        query: str,
        context_override: Optional[List[str]] = None
    ) -> str:
        """Async version of generate."""
        return self.generate(query, context_override)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get RAG system statistics."""
        doc_count, chunk_count = self.vector_store.count()
        
        return {
            "documents": doc_count,
            "chunks": chunk_count,
            "chunk_size": self.config.chunk_size,
            "top_k": self.config.top_k,
        }
```

### 2. Hybrid Search System

```typescript
// src/search/hybrid-search.ts
/**
 * Hybrid Search System - Kết hợp keyword và semantic search
 */

import { GeminiEmbeddingClient, EmbeddingResult } from '../embeddings/embedding-client';

interface SearchResult {
  id: string;
  content: string;
  score: number;
  source: 'keyword' | 'semantic' | 'hybrid';
  metadata: Record<string, any>;
}

interface HybridSearchConfig {
  semanticWeight: number;
  keywordWeight: number;
  topK: number;
  minScore: number;
}

export class HybridSearchEngine {
  private embeddingClient: GeminiEmbeddingClient;
  private documents: Map<string, { content: string; metadata: Record<string, any>; embedding?: number[] }> = new Map();
  private keywordIndex: Map<string, Set<string>> = new Map();
  
  constructor(apiKey: string, config: Partial<HybridSearchConfig> = {}) {
    this.embeddingClient = new GeminiEmbeddingClient(apiKey);
    this.config = {
      semanticWeight: config.semanticWeight ?? 0.7,
      keywordWeight: config.keywordWeight ?? 0.3,
      topK: config.topK ?? 10,
      minScore: config.minScore ?? 0.3,
    };
  }
  
  private config: HybridSearchConfig;
  
  /**
   * Index a document
   */
  async indexDocument(
    id: string,
    content: string,
    metadata: Record<string, any> = {}
  ): Promise<void> {
    // Get embedding
    const embedding = await this.embeddingClient.embedDocument(content);
    
    // Store document
    this.documents.set(id, {
      content,
      metadata,
      embedding: embedding.embedding,
    });
    
    // Build keyword index
    const keywords = this.extractKeywords(content);
    for (const keyword of keywords) {
      if (!this.keywordIndex.has(keyword)) {
        this.keywordIndex.set(keyword, new Set());
      }
      this.keywordIndex.get(keyword)!.add(id);
    }
  }
  
  /**
   * Index multiple documents
   */
  async indexDocuments(
    documents: Array<{ id: string; content: string; metadata?: Record<string, any> }>,
    onProgress?: (progress: { completed: number; total: number }) => void
  ): Promise<void> {
    const total = documents.length;
    
    for (let i = 0; i < documents.length; i++) {
      const doc = documents[i];
      await this.indexDocument(doc.id, doc.content, doc.metadata || {});
      
      if (onProgress) {
        onProgress({ completed: i + 1, total });
      }
    }
  }
  
  /**
   * Search documents
   */
  async search(query: string): Promise<SearchResult[]> {
    // Semantic search
    const queryEmbedding = await this.embeddingClient.embedQuery(query);
    
    const semanticResults = this.semanticSearch(queryEmbedding.embedding);
    
    // Keyword search
    const keywordResults = this.keywordSearch(query);
    
    // Combine results
    const combinedResults = this.combineResults(semanticResults, keywordResults);
    
    // Sort and filter
    return combinedResults
      .filter(r => r.score >= this.config.minScore)
      .sort((a, b) => b.score - a.score)
      .slice(0, this.config.topK);
  }
  
  /**
   * Semantic search using embeddings
   */
  private semanticSearch(queryEmbedding: number[]): Map<string, number> {
    const results = new Map<string, number>();
    
    for (const [id, doc] of this.documents) {
      if (!doc.embedding) continue;
      
      const similarity = this.cosineSimilarity(queryEmbedding, doc.embedding);
      results.set(id, similarity);
    }
    
    return results;
  }
  
  /**
   * Keyword search using inverted index
   */
  private keywordSearch(query: string): Map<string, number> {
    const results = new Map<string, number>();
    const queryKeywords = this.extractKeywords(query);
    
    for (const keyword of queryKeywords) {
      const docIds = this.keywordIndex.get(keyword.toLowerCase());
      
      if (docIds) {
        for (const id of docIds) {
          const currentScore = results.get(id) || 0;
          results.set(id, currentScore + 1);
        }
      }
    }
    
    // Normalize scores
    if (queryKeywords.length > 0) {
      for (const [id, score] of results) {
        results.set(id, score / queryKeywords.length);
      }
    }
    
    return results;
  }
  
  /**
   * Combine semantic and keyword results
   */
  private combineResults(
    semantic: Map<string, number>,
    keyword: Map<string, number>
  ): SearchResult[] {
    const allIds = new Set([...semantic.keys(), ...keyword.keys()]);
    const results: SearchResult[] = [];
    
    for (const id of allIds) {
      const semScore = semantic.get(id) || 0;
      const keyScore = keyword.get(id) || 0;
      
      // Weighted combination
      const combinedScore = 
        semScore * this.config.semanticWeight +
        keyScore * this.config.keywordWeight;
      
      const doc = this.documents.get(id);
      
      if (doc) {
        results.push({
          id,
          content: doc.content,
          score: combinedScore,
          source: this.getScoreSource(semScore, keyScore),
          metadata: doc.metadata,
        });
      }
    }
    
    return results;
  }
  
  /**
   * Determine primary source of score
   */
  private getScoreSource(
    semanticScore: number,
    keywordScore: number
  ): 'keyword' | 'semantic' | 'hybrid' {
    if (semanticScore > 0.7 && keywordScore < 0.3) {
      return 'semantic';
    }
    if (keywordScore > 0.7 && semanticScore < 0.3) {
      return 'keyword';
    }
    return 'hybrid';
  }
  
  /**
   * Calculate cosine similarity
   */
  private cosineSimilarity(a: number[], b: number[]): number {
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;
    
    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }
    
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
  }
  
  /**
   * Extract keywords from text
   */
  private extractKeywords(text: string): string[] {
    // Simple tokenization and lowercasing
    const words = text
      .toLowerCase()
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 2);
    
    // Remove common stopwords
    const stopwords = new Set([
      'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
      'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were',
      'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
      'did', 'will', 'would', 'should', 'could', 'may', 'might',
    ]);
    
    return words.filter(word => !stopwords.has(word));
  }
}
```

## Examples

### 1. Complete RAG System Example - Python

```python
# src/examples/rag_system.py
"""
Complete RAG System Example
"""

import asyncio
from typing import List
from google.generativeai import GenerativeModel

from src.rag.rag_system import RAGSystem, RAGConfig, Document
from src.embeddings.embedding_client import GeminiEmbeddingClient


async def main():
    """Example usage of RAG system."""
    
    # Initialize RAG system
    config = RAGConfig(
        embedding_model="models/embedding-001",
        chunk_size=500,
        chunk_overlap=100,
        top_k=3,
        min_similarity_score=0.6
    )
    
    rag_system = RAGSystem(config)
    
    # Sample documents
    documents = [
        Document(
            id="doc_1",
            content="""
            Gemini is a family of multimodal AI models developed by Google DeepMind.
            Gemini 2.0 Flash is the latest model offering improved performance
            and faster inference times. It supports text, images, audio, and video inputs.
            """,
            title="Introduction to Gemini",
            metadata={"category": "AI", "source": "documentation"}
        ),
        Document(
            id="doc_2",
            content="""
            RAG (Retrieval-Augmented Generation) is a technique that combines
            information retrieval with text generation. It allows AI models to
            access and cite external knowledge bases. This improves the accuracy
            and relevance of generated content.
            """,
            title="RAG Explained",
            metadata={"category": "AI", "source": "documentation"}
        ),
        Document(
            id="doc_3",
            content="""
            Vector embeddings are numerical representations of text that capture
            semantic meaning in a high-dimensional space. Similar texts will have
            similar embeddings. This enables semantic search and similarity matching.
            """,
            title="Vector Embeddings",
            metadata={"category": "ML", "source": "documentation"}
        ),
    ]
    
    # Add documents
    print("Indexing documents...")
    chunks_added = rag_system.add_documents(documents)
    print(f"Added {len(documents)} documents ({chunks_added} chunks)")
    
    # Set generation model
    model = GenerativeModel("gemini-2.0-flash")
    rag_system.set_generation_model(model)
    
    # Queries
    queries = [
        "What is Gemini?",
        "How does RAG work?",
        "What are vector embeddings?"
    ]
    
    print("\n" + "=" * 60)
    print("RAG SYSTEM DEMO")
    print("=" * 60)
    
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 40)
        
        # Show retrieved context
        retrieved = rag_system.retrieve(query)
        print(f"Retrieved {len(retrieved)} relevant chunks:")
        for r in retrieved:
            print(f"  - [{r.score:.2f}] {r.content[:100]}...")
        
        # Generate answer
        print("\nGenerated Answer:")
        answer = rag_system.generate(query)
        print(answer)
        print()


if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Complete Semantic Search Example - TypeScript

```typescript
// src/examples/semantic-search.ts
/**
 * Complete Semantic Search Example (TypeScript)
 */

import { GeminiEmbeddingClient } from '../embeddings/embedding-client';
import { VectorStore } from '../embeddings/vector-store';

interface Article {
  id: string;
  title: string;
  content: string;
  category: string;
  date: string;
}

async function main() {
  const apiKey = process.env.GEMINI_API_KEY!;
  const embeddingClient = new GeminiEmbeddingClient(apiKey);
  const vectorStore = new VectorStore(768, 'cosine');
  
  // Sample articles
  const articles: Article[] = [
    {
      id: '1',
      title: 'Introduction to Machine Learning',
      content: 'Machine learning is a subset of artificial intelligence that enables systems to learn from data.',
      category: 'AI',
      date: '2024-01-15',
    },
    {
      id: '2',
      title: 'Deep Learning Fundamentals',
      content: 'Deep learning uses neural networks with multiple layers to solve complex problems.',
      category: 'AI',
      date: '2024-02-01',
    },
    {
      id: '3',
      title: 'Natural Language Processing Overview',
      content: 'NLP enables computers to understand, interpret, and generate human language.',
      category: 'AI',
      date: '2024-02-15',
    },
    {
      id: '4',
      title: 'Web Development Best Practices',
      content: 'Modern web development involves React, TypeScript, and responsive design patterns.',
      category: 'Web',
      date: '2024-03-01',
    },
  ];
  
  console.log('Indexing articles...');
  
  // Index articles
  for (const article of articles) {
    const text = `${article.title}. ${article.content}`;
    const embedding = await embeddingClient.embedDocument(text, article.title);
    
    vectorStore.add(embedding.embedding, {
      id: article.id,
      title: article.title,
      content: article.content,
      category: article.category,
    });
    
    console.log(`Indexed: ${article.title}`);
  }
  
  console.log(`\nTotal articles indexed: ${vectorStore.count()}`);
  
  // Search queries
  const queries = [
    'How do computers understand language?',
    'What is artificial intelligence?',
    'Web development frameworks',
  ];
  
  console.log('\n' + '='.repeat(60));
  console.log('SEMANTIC SEARCH RESULTS');
  console.log('='.repeat(60));
  
  for (const query of queries) {
    console.log(`\nQuery: "${query}"`);
    console.log('-'.repeat(40));
    
    const results = vectorStore.searchByText(
      await embeddingClient.embedQuery(query).then(r => r.embedding),
      k = 3,
      minScore = 0.3
    );
    
    if (results.length === 0) {
      console.log('No results found');
      continue;
    }
    
    for (const result of results) {
      console.log(
        `\n[${result.score.toFixed(3)}] ${result.title || result.id}`
      );
      console.log(`   ${result.content?.substring(0, 100)}...`);
    }
  }
}

main().catch(console.error);
```

## Troubleshooting

### Các Vấn Đề Thường Gặp

**1. "Embeddings have different dimensions"**

```
Nguyên nhân: Documents được embed với các models khác nhau
Giải pháp:
- Đảm bảo sử dụng cùng embedding model cho tất cả documents
- Kiểm tra dimension parameter trong embedding config
- Re-index tất cả documents nếu cần
```

**2. "Search returns irrelevant results"**

```
Nguyên nhân: Chunking strategy không phù hợp hoặc embeddings không đủ quality
Giải pháp:
- Thử semantic chunking thay vì fixed-size
- Tăng chunk overlap
- Verify task type đúng (RETRIEVAL_QUERY cho queries)
- Check similarity threshold
```

**3. "Slow embedding generation"**

```
Nguyên nhân: Too many API calls hoặc batch size không tối ưu
Giải pháp:
- Use batch embedding API thay vì individual calls
- Increase batch size (test với 50-100)
- Add caching cho frequently accessed embeddings
- Consider using async/parallel processing
```

**4. "Out of memory with large document collections"**

```
Nguyên nhân: Too many vectors stored in memory
Giải pháp:
- Use external vector database (Pinecone, Weaviate, Milvus)
- Implement pagination cho search results
- Use approximate nearest neighbor (ANN) algorithms
- Consider dimensionality reduction
```

**5. "RAG answers don't match retrieved context"**

```
Nguyên nhân: Context không được formatted tốt hoặc similarity threshold quá low
Giải pháp:
- Improve context formatting trong generate function
- Tăng min_similarity_score
- Thử reranking results
- Include more context chunks
```

## References

### Official Documentation

- [Gemini Embeddings Documentation](https://ai.google.dev/docs/embeddings)
- [Embedding API Reference](https://ai.google.dev/api/rest/v1beta/models/embedContent)
- [Text Embeddings Guide](https://ai.google.dev/docs/text_embeddings)

### Vector Database Options

- [Pinecone](https://www.pinecone.io/) - Managed vector database
- [Weaviate](https://weaviate.io/) - Open source vector search
- [Milvus](https://milvus.io/) - Open source vector database
- [Chroma](https://trychroma.com/) - Simple vector database for prototyping
- [FAISS](https://github.com/facebookresearch/faiss) - Facebook's similarity search

### Related Documents

- `@gemini-api-setup.md` - Setup và configuration
- `@rag.mdc` - RAG implementation best practices
- `@vector-search.mdc` - Vector search strategies
- `@performance.mdc` - Performance optimization
- `@pgvector.mdc` - PostgreSQL vector storage
