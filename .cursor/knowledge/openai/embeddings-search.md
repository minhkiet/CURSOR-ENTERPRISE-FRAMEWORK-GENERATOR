---
title: Embeddings và Semantic Search
description: Hướng dẫn toàn diện về Embeddings API, cosine similarity, vector storage, approximate nearest neighbor và hybrid search
tags: [openai, embeddings, vector, search, semantic, typescript, python]
created: 2026-06-23
version: 1.0.0
framework: cursor-enterprise
---

# Embeddings và Semantic Search

## Tổng quan

Embeddings là một trong những công nghệ nền tảng của các ứng dụng AI hiện đại, cho phép chuyển đổi text, images, và other data types thành numerical vectors mà machines có thể understand và compare. Trong ngữ cảnh của OpenAI, embeddings được tạo ra bởi specialized models được trained để capture semantic meaning của data, enabling powerful search và similarity operations.

OpenAI cung cấp Embeddings API với các models như `text-embedding-3-large` (3072 dimensions), `text-embedding-3-small` (1536 dimensions), và legacy `text-embedding-ada-002`. Các models mới hơn (embedding-3) hỗ trợ dimensionality reduction, cho phép bạn trade off giữa quality và storage/cost.

Semantic search dựa trên nguyên tắc rằng similar content sẽ có similar embeddings. Thay vì keyword matching truyền thống, semantic search tìm kiếm based on meaning và context, mang lại better results cho natural language queries. Điều này đặc biệt hữu ích cho applications như document search, recommendation systems, và chatbots cần retrieve relevant context.

## Mục đích và Phạm vi

Tài liệu này cung cấp hướng dẫn toàn diện về việc sử dụng OpenAI Embeddings API cho semantic search applications. Phạm vi bao gồm từ basic embedding generation, đến vector storage và retrieval strategies, và advanced topics như approximate nearest neighbor (ANN) algorithms, hybrid search, và production deployment patterns.

Chúng tôi sẽ cover practical implementation patterns cho cả TypeScript và Python, với focus on production-ready solutions. Các examples bao gồm vector database integration (Pinecone, Weaviate, Qdrant, Milvus), indexing strategies, và optimization techniques cho high-performance search systems.

## Các Khái niệm Chính

### Vector Embeddings là gì

Embeddings là dense numerical representations của data trong a high-dimensional vector space. Mỗi dimension capture một aspect của meaning hoặc characteristics của data. Items có similar meanings hoặc characteristics sẽ có similar vectors, measured by metrics như cosine similarity hoặc Euclidean distance.

Ví dụ, trong không gian 2D đơn giản hóa:
- "dog" có thể có vector [0.8, 0.2]
- "cat" có thể có vector [0.75, 0.25]
- "car" có thể có vector [0.1, 0.9]

Dogs và cats có vectors gần nhau vì chúng đều là animals, trong khi cars có vector far from both. Trong thực tế, embeddings có hàng nghìn dimensions và capture nuanced semantic relationships.

OpenAI embeddings được trained trên massive datasets và capture rich semantic information. `text-embedding-3-large` tạo ra 3072-dimensional vectors với state-of-the-art performance trên benchmarks. Bạn có thể reduce dimensions sử dụng `dimensions` parameter mà không mất nhiều quality, thanks to advanced training techniques.

### Cosine Similarity

Cosine similarity là metric phổ biến nhất để measure similarity giữa vectors. Nó measures cosine của angle giữa hai vectors, ranges từ -1 (opposite) đến 1 (identical). Values gần 1 indicate high similarity.

```
cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)
```

Trong đó:
- A · B là dot product của hai vectors
- ||A|| và ||B|| là magnitudes của mỗi vector

Ví dụ với two vectors:
- A = [0.1, 0.2, 0.3, 0.4]
- B = [0.11, 0.19, 0.31, 0.39]

cosine_similarity = (0.1×0.11 + 0.2×0.19 + 0.3×0.31 + 0.4×0.39) / (√(0.1²+0.2²+0.3²+0.4²) × √(0.11²+0.19²+0.31²+0.39²))

Cosine similarity đặc biệt hữu ích cho text embeddings vì nó measures directional similarity rather than magnitude, which is often not meaningful for text similarity.

### Embedding Models và Dimensions

OpenAI cung cấp multiple embedding models với different capabilities và price points:

**`text-embedding-3-large`** (recommended):
- Dimensions: 3072 (adjustable down to 256)
- Best quality for most use cases
- Price: $0.00013 per 1K tokens
- Use cases: Production search, RAG, semantic analysis

**`text-embedding-3-small`**:
- Dimensions: 1536 (adjustable down to 256)
- 5x cheaper than large, slight quality trade-off
- Price: $0.00002 per 1K tokens
- Use cases: Cost-sensitive applications, large-scale indexing

**`text-embedding-ada-002`** (legacy):
- Dimensions: 1536
- Original embedding model
- Still supported but not recommended for new projects
- Price: $0.0001 per 1K tokens

### Approximate Nearest Neighbor (ANN)

Exact nearest neighbor search có complexity O(n × d) với n = number of vectors, d = dimensions. Điều này không scale cho large datasets với millions hoặc billions of vectors.

ANN algorithms trade off some accuracy for dramatic speed improvements, achieving sub-linear or logarithmic complexity. Popular algorithms bao gồm:

**HNSW (Hierarchical Navigable Small World)**:
- Graph-based algorithm với excellent query speed
- Memory-intensive but very accurate
- Default choice cho most vector databases
- Parameters: M (connections per node), efConstruction (build quality)

**IVF (Inverted File Index)**:
- Clusters vectors into inverted lists
- Faster search by limiting scan scope
- Good for very large datasets
- Parameters: nlist (number of clusters), nprobe (clusters to search)

**PQ (Product Quantization)**:
- Compresses vectors by splitting into subvectors
- Dramatically reduces memory usage
- Good for billion-scale datasets
- Trade-off: lower accuracy, slower encoding

**DiskANN và ScaNN**:
- Optimized for billion-scale on-disk indices
- Used by major cloud vector services
- Complex to implement but very scalable

## Best Practices cho Production

### Embedding Generation

```typescript
// services/embeddingService.ts - Embedding generation utilities
import OpenAI from 'openai';

interface EmbeddingOptions {
  model?: string;
  dimensions?: number; // For embedding-3 models only
  batchSize?: number;
}

interface EmbeddingResult {
  embedding: number[];
  tokens: number;
  model: string;
}

interface BatchEmbeddingResult {
  embeddings: number[][];
  tokens: number;
  model: string;
  processingTimeMs: number;
}

export class EmbeddingService {
  private client: OpenAI;
  private defaultModel: string;
  
  constructor(client: OpenAI, defaultModel: string = 'text-embedding-3-large') {
    this.client = client;
    this.defaultModel = defaultModel;
  }
  
  async createEmbedding(
    text: string,
    options: EmbeddingOptions = {}
  ): Promise<EmbeddingResult> {
    const model = options.model || this.defaultModel;
    
    // Pre-process text
    const processedText = this.preprocessText(text);
    
    const response = await this.client.embeddings.create({
      model,
      input: processedText,
      dimensions: options.dimensions, // Only for embedding-3 models
    });
    
    return {
      embedding: response.data[0].embedding,
      tokens: response.usage.prompt_tokens,
      model: response.model,
    };
  }
  
  async createBatchEmbeddings(
    texts: string[],
    options: EmbeddingOptions = {}
  ): Promise<BatchEmbeddingResult> {
    const startTime = Date.now();
    const model = options.model || this.defaultModel;
    const batchSize = options.batchSize || 100;
    
    const allEmbeddings: number[][] = [];
    let totalTokens = 0;
    
    // Process in batches to respect rate limits
    for (let i = 0; i < texts.length; i += batchSize) {
      const batch = texts.slice(i, i + batchSize);
      const processedBatch = batch.map(text => this.preprocessText(text));
      
      const response = await this.client.embeddings.create({
        model,
        input: processedBatch,
        dimensions: options.dimensions,
      });
      
      // Sort by index to maintain order
      const indexedEmbeddings = response.data
        .sort((a, b) => a.index - b.index)
        .map(item => item.embedding);
      
      allEmbeddings.push(...indexedEmbeddings);
      totalTokens += response.usage.prompt_tokens;
      
      // Respect rate limits between batches
      if (i + batchSize < texts.length) {
        await this.delay(100); // 100ms delay between batches
      }
    }
    
    return {
      embeddings: allEmbeddings,
      tokens: totalTokens,
      model,
      processingTimeMs: Date.now() - startTime,
    };
  }
  
  private preprocessText(text: string): string {
    // Remove excessive whitespace
    let processed = text.replace(/\s+/g, ' ').trim();
    
    // Truncate if too long (max ~8000 tokens for safety)
    const maxChars = 32000;
    if (processed.length > maxChars) {
      processed = processed.substring(0, maxChars);
    }
    
    return processed;
  }
  
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Text chunking utilities for long documents
export class TextChunker {
  private chunkSize: number;
  private overlap: number;
  
  constructor(chunkSize: number = 1000, overlap: number = 200) {
    this.chunkSize = chunkSize;
    this.overlap = overlap;
  }
  
  chunkText(text: string, metadata?: Record<string, any>): Array<{
    text: string;
    metadata: Record<string, any>;
    chunkIndex: number;
    totalChunks: number;
  }> {
    const words = text.split(/\s+/);
    const chunks: Array<{
      text: string;
      metadata: Record<string, any>;
      chunkIndex: number;
      totalChunks: number;
    }> = [];
    
    let start = 0;
    let chunkIndex = 0;
    
    while (start < words.length) {
      let end = start + this.chunkSize;
      
      // Try to break at sentence boundary
      if (end < words.length) {
        const slice = words.slice(start, end).join(' ');
        const lastPeriod = slice.lastIndexOf('.');
        const lastNewline = slice.lastIndexOf('\n');
        const breakPoint = Math.max(lastPeriod, lastNewline);
        
        if (breakPoint > this.chunkSize * 0.5) {
          end = start + breakPoint + 1;
        }
      }
      
      const chunkText = words.slice(start, end).join(' ');
      const baseMetadata = metadata || {};
      
      chunks.push({
        text: chunkText,
        metadata: {
          ...baseMetadata,
          chunkStart: start,
          chunkEnd: end,
        },
        chunkIndex,
        totalChunks: 0, // Will be updated after all chunks are created
      });
      
      chunkIndex++;
      start = Math.max(start + this.chunkSize - this.overlap, end);
    }
    
    // Update total chunks
    const totalChunks = chunks.length;
    chunks.forEach(chunk => {
      chunk.totalChunks = totalChunks;
    });
    
    return chunks;
  }
  
  chunkDocument(document: {
    content: string;
    title?: string;
    url?: string;
    id?: string;
  }): Array<{
    text: string;
    metadata: Record<string, any>;
    chunkIndex: number;
    totalChunks: number;
  }> {
    return this.chunkText(document.content, {
      title: document.title,
      url: document.url,
      documentId: document.id,
    });
  }
}
```

```python
# services/embedding_service.py - Embedding generation utilities
from openai import OpenAI
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import time
import re

@dataclass
class EmbeddingResult:
    embedding: List[float]
    tokens: int
    model: str

@dataclass
class BatchEmbeddingResult:
    embeddings: List[List[float]]
    tokens: int
    model: str
    processing_time_ms: float

class EmbeddingService:
    def __init__(self, api_key: str, default_model: str = 'text-embedding-3-large'):
        self.client = OpenAI(api_key=api_key)
        self.default_model = default_model
    
    def create_embedding(
        self,
        text: str,
        model: Optional[str] = None,
        dimensions: Optional[int] = None
    ) -> EmbeddingResult:
        model = model or self.default_model
        processed_text = self._preprocess_text(text)
        
        params = {
            'model': model,
            'input': processed_text,
        }
        
        # Only add dimensions for embedding-3 models
        if 'embedding-3' in model and dimensions:
            params['dimensions'] = dimensions
        
        response = self.client.embeddings.create(**params)
        
        return EmbeddingResult(
            embedding=response.data[0].embedding,
            tokens=response.usage.prompt_tokens,
            model=response.model,
        )
    
    def create_batch_embeddings(
        self,
        texts: List[str],
        model: Optional[str] = None,
        dimensions: Optional[int] = None,
        batch_size: int = 100,
        delay_between_batches: float = 0.1
    ) -> BatchEmbeddingResult:
        start_time = time.time()
        model = model or self.default_model
        
        all_embeddings: List[List[float]] = []
        total_tokens = 0
        
        # Process in batches
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            processed_batch = [self._preprocess_text(t) for t in batch]
            
            params = {
                'model': model,
                'input': processed_batch,
            }
            
            if 'embedding-3' in model and dimensions:
                params['dimensions'] = dimensions
            
            response = self.client.embeddings.create(**params)
            
            # Sort by index to maintain order
            embeddings_by_index = sorted(
                response.data,
                key=lambda x: x.index
            )
            
            all_embeddings.extend([e.embedding for e in embeddings_by_index])
            total_tokens += response.usage.prompt_tokens
            
            # Respect rate limits between batches
            if i + batch_size < len(texts):
                time.sleep(delay_between_batches)
        
        return BatchEmbeddingResult(
            embeddings=all_embeddings,
            tokens=total_tokens,
            model=model,
            processing_time_ms=(time.time() - start_time) * 1000,
        )
    
    def _preprocess_text(self, text: str) -> str:
        # Remove excessive whitespace
        processed = re.sub(r'\s+', ' ', text).strip()
        
        # Truncate if too long
        max_chars = 32000
        if len(processed) > max_chars:
            processed = processed[:max_chars]
        
        return processed

class TextChunker:
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        words = text.split()
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(words):
            end = start + self.chunk_size
            
            # Try to break at sentence boundary
            if end < len(words):
                chunk_slice = ' '.join(words[start:end])
                last_period = chunk_slice.rfind('.')
                last_newline = chunk_slice.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > self.chunk_size * 0.5:
                    end = start + break_point + 1
            
            chunk_text = ' '.join(words[start:end])
            base_metadata = metadata or {}
            
            chunks.append({
                'text': chunk_text,
                'metadata': {
                    **base_metadata,
                    'chunk_start': start,
                    'chunk_end': end,
                },
                'chunk_index': chunk_index,
                'total_chunks': 0,  # Will be updated
            })
            
            chunk_index += 1
            start = max(start + self.chunk_size - self.overlap, end)
        
        # Update total chunks
        total_chunks = len(chunks)
        for chunk in chunks:
            chunk['total_chunks'] = total_chunks
        
        return chunks
    
    def chunk_document(
        self,
        content: str,
        title: Optional[str] = None,
        url: Optional[str] = None,
        doc_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        metadata = {
            'title': title,
            'url': url,
            'document_id': doc_id,
        }
        metadata = {k: v for k, v in metadata.items() if v is not None}
        return self.chunk_text(content, metadata)
```

### Vector Storage và Retrieval

```typescript
// services/vectorStore.ts - Vector storage abstraction
import OpenAI from 'openai';
import { EmbeddingService } from './embeddingService';

// Vector database interface - implement for your chosen DB
export interface VectorDatabase {
  upsert(vectors: VectorRecord[]): Promise<void>;
  search(queryEmbedding: number[], options: SearchOptions): Promise<SearchResult[]>;
  delete(ids: string[]): Promise<void>;
  getStats(): Promise<DatabaseStats>;
}

export interface VectorRecord {
  id: string;
  embedding: number[];
  metadata: Record<string, any>;
  text?: string; // Original text (optional, for display)
}

export interface SearchOptions {
  topK: number;
  filter?: Record<string, any>;
  includeVectors?: boolean;
  minScore?: number;
}

export interface SearchResult {
  id: string;
  score: number;
  metadata: Record<string, any>;
  text?: string;
}

export interface DatabaseStats {
  totalVectors: number;
  dimension: number;
  indexSizeBytes: number;
}

// In-memory vector store (for testing/small datasets)
export class InMemoryVectorStore implements VectorDatabase {
  private vectors: Map<string, VectorRecord> = new Map();
  private dimension: number = 0;
  
  async upsert(records: VectorRecord[]): Promise<void> {
    for (const record of records) {
      if (this.dimension === 0) {
        this.dimension = record.embedding.length;
      }
      this.vectors.set(record.id, record);
    }
  }
  
  async search(
    queryEmbedding: number[],
    options: SearchOptions
  ): Promise<SearchResult[]> {
    const results: SearchResult[] = [];
    
    for (const [id, record] of this.vectors) {
      // Apply filters
      if (options.filter) {
        const matchesFilter = Object.entries(options.filter).every(
          ([key, value]) => record.metadata[key] === value
        );
        if (!matchesFilter) continue;
      }
      
      const score = this.cosineSimilarity(queryEmbedding, record.embedding);
      
      if (options.minScore && score < options.minScore) continue;
      
      results.push({
        id,
        score,
        metadata: record.metadata,
        text: record.text,
      });
    }
    
    // Sort by score and return top K
    return results
      .sort((a, b) => b.score - a.score)
      .slice(0, options.topK);
  }
  
  async delete(ids: string[]): Promise<void> {
    for (const id of ids) {
      this.vectors.delete(id);
    }
  }
  
  async getStats(): Promise<DatabaseStats> {
    return {
      totalVectors: this.vectors.size,
      dimension: this.dimension,
      indexSizeBytes: this.vectors.size * this.dimension * 8, // Rough estimate
    };
  }
  
  private cosineSimilarity(a: number[], b: number[]): number {
    if (a.length !== b.length) throw new Error('Vector dimensions mismatch');
    
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
}

// Document store with embeddings
export class DocumentStore {
  private embeddingService: EmbeddingService;
  private vectorDB: VectorDatabase;
  private chunker: any;
  
  constructor(
    embeddingService: EmbeddingService,
    vectorDB: VectorDatabase,
    chunker: any
  ) {
    this.embeddingService = embeddingService;
    this.vectorDB = vectorDB;
    this.chunker = chunker;
  }
  
  async indexDocument(document: {
    id: string;
    content: string;
    title?: string;
    url?: string;
    metadata?: Record<string, any>;
  }): Promise<{ chunksIndexed: number; tokensUsed: number }> {
    // Chunk document
    const chunks = this.chunker.chunkDocument({
      content: document.content,
      title: document.title,
      url: document.url,
      id: document.id,
    });
    
    // Extract texts for embedding
    const texts = chunks.map(chunk => chunk.text);
    
    // Create embeddings in batch
    const { embeddings, tokens } = await this.embeddingService.createBatchEmbeddings(texts);
    
    // Prepare records for vector DB
    const records: VectorRecord[] = chunks.map((chunk, index) => ({
      id: `${document.id}_chunk_${index}`,
      embedding: embeddings[index],
      metadata: {
        ...chunk.metadata,
        ...document.metadata,
      },
      text: chunk.text,
    }));
    
    // Upsert to vector DB
    await this.vectorDB.upsert(records);
    
    return { chunksIndexed: chunks.length, tokensUsed: tokens };
  }
  
  async indexDocuments(documents: Array<{
    id: string;
    content: string;
    title?: string;
    url?: string;
    metadata?: Record<string, any>;
  }>): Promise<{ totalChunks: number; totalTokens: number }> {
    let totalChunks = 0;
    let totalTokens = 0;
    
    for (const doc of documents) {
      const result = await this.indexDocument(doc);
      totalChunks += result.chunksIndexed;
      totalTokens += result.tokensUsed;
    }
    
    return { totalChunks, totalTokens };
  }
  
  async search(
    query: string,
    options: {
      topK?: number;
      filter?: Record<string, any>;
      minScore?: number;
    } = {}
  ): Promise<Array<{
    text: string;
    score: number;
    metadata: Record<string, any>;
  }>> {
    // Create query embedding
    const { embedding } = await this.embeddingService.createEmbedding(query);
    
    // Search vector DB
    const results = await this.vectorDB.search(embedding, {
      topK: options.topK || 5,
      filter: options.filter,
      minScore: options.minScore,
      includeVectors: false,
    });
    
    return results.map(result => ({
      text: result.text || '',
      score: result.score,
      metadata: result.metadata,
    }));
  }
  
  async deleteDocument(documentId: string): Promise<void> {
    // This requires knowledge of chunk IDs - simplified here
    const stats = await this.vectorDB.getStats();
    // In real implementation, you'd query and delete specific chunks
    console.log(`Deleting document ${documentId}`);
  }
}
```

```python
# services/vector_store.py - Vector storage abstraction
from typing import List, Dict, Any, Optional, Protocol, runtime_checkable
from dataclasses import dataclass
import math

@runtime_checkable
class VectorDatabase(Protocol):
    async def upsert(self, records: List[Dict[str, Any]]) -> None: ...
    async def search(
        self,
        query_embedding: List[float],
        options: Dict[str, Any]
    ) -> List[Dict[str, Any]]: ...
    async def delete(self, ids: List[str]) -> None: ...
    async def get_stats(self) -> Dict[str, Any]: ...

@dataclass
class VectorRecord:
    id: str
    embedding: List[float]
    metadata: Dict[str, Any]
    text: Optional[str] = None

@dataclass
class SearchResult:
    id: str
    score: float
    metadata: Dict[str, Any]
    text: Optional[str] = None

@dataclass
class DatabaseStats:
    total_vectors: int
    dimension: int
    index_size_bytes: int

class InMemoryVectorStore:
    def __init__(self):
        self._vectors: Dict[str, VectorRecord] = {}
        self._dimension: int = 0
    
    async def upsert(self, records: List[VectorRecord]) -> None:
        for record in records:
            if self._dimension == 0:
                self._dimension = len(record.embedding)
            self._vectors[record.id] = record
    
    async def search(
        self,
        query_embedding: List[float],
        options: Dict[str, Any]
    ) -> List[SearchResult]:
        results: List[SearchResult] = []
        top_k = options.get('top_k', 10)
        filter_criteria = options.get('filter')
        min_score = options.get('min_score')
        
        for id_, record in self._vectors.items():
            # Apply filters
            if filter_criteria:
                matches = all(
                    record.metadata.get(k) == v
                    for k, v in filter_criteria.items()
                )
                if not matches:
                    continue
            
            score = self._cosine_similarity(query_embedding, record.embedding)
            
            if min_score and score < min_score:
                continue
            
            results.append(SearchResult(
                id=id_,
                score=score,
                metadata=record.metadata,
                text=record.text,
            ))
        
        # Sort and return top K
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
    
    async def delete(self, ids: List[str]) -> None:
        for id_ in ids:
            self._vectors.pop(id_, None)
    
    async def get_stats(self) -> DatabaseStats:
        return DatabaseStats(
            total_vectors=len(self._vectors),
            dimension=self._dimension,
            index_size_bytes=len(self._vectors) * self._dimension * 8,
        )
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        if len(a) != len(b):
            raise ValueError('Vector dimensions mismatch')
        
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        
        return dot_product / (norm_a * norm_b) if norm_a and norm_b else 0.0

class DocumentStore:
    def __init__(
        self,
        embedding_service,
        vector_db: VectorDatabase,
        chunker
    ):
        self.embedding_service = embedding_service
        self.vector_db = vector_db
        self.chunker = chunker
    
    async def index_document(
        self,
        content: str,
        doc_id: str,
        title: Optional[str] = None,
        url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        # Chunk document
        chunks = self.chunker.chunk_document(
            content=content,
            title=title,
            url=url,
            doc_id=doc_id,
        )
        
        # Extract texts
        texts = [chunk['text'] for chunk in chunks]
        
        # Create embeddings
        result = self.embedding_service.create_batch_embeddings(texts)
        
        # Prepare records
        records = [
            VectorRecord(
                id=f"{doc_id}_chunk_{i}",
                embedding=result.embeddings[i],
                metadata={
                    **chunk['metadata'],
                    **(metadata or {}),
                },
                text=chunk['text'],
            )
            for i, chunk in enumerate(chunks)
        ]
        
        # Upsert to vector DB
        await self.vector_db.upsert(records)
        
        return {
            'chunks_indexed': len(chunks),
            'tokens_used': result.tokens,
        }
    
    async def search(
        self,
        query: str,
        top_k: int = 5,
        filter_criteria: Optional[Dict[str, Any]] = None,
        min_score: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        # Create query embedding
        result = self.embedding_service.create_embedding(query)
        
        # Search
        search_results = await self.vector_db.search(
            result.embedding,
            {
                'top_k': top_k,
                'filter': filter_criteria,
                'min_score': min_score,
            }
        )
        
        return [
            {
                'text': r.text or '',
                'score': r.score,
                'metadata': r.metadata,
            }
            for r in search_results
        ]
```

### Semantic Search Implementation

```typescript
// services/semanticSearch.ts - Semantic search service
import { DocumentStore } from './vectorStore';
import OpenAI from 'openai';

interface SearchResult {
  results: Array<{
    text: string;
    score: number;
    metadata: {
      title?: string;
      url?: string;
      chunkIndex?: number;
      totalChunks?: number;
      [key: string]: any;
    };
  }>;
  query: string;
  totalResults: number;
  searchTimeMs: number;
  embeddingTokens: number;
}

interface SemanticSearchOptions {
  topK?: number;
  minScore?: number;
  filter?: Record<string, any>;
  rerank?: boolean;
  hybridSearch?: boolean;
  keywordBoost?: number;
}

export class SemanticSearchService {
  private documentStore: DocumentStore;
  private openai: OpenAI;
  
  constructor(documentStore: DocumentStore, openai: OpenAI) {
    this.documentStore = documentStore;
    this.openai = openai;
  }
  
  async search(
    query: string,
    options: SemanticSearchOptions = {}
  ): Promise<SearchResult> {
    const startTime = Date.now();
    
    const topK = options.topK || 5;
    const minScore = options.minScore || 0.7;
    
    let results: Array<{
      text: string;
      score: number;
      metadata: Record<string, any>;
    }>;
    let embeddingTokens = 0;
    
    if (options.hybridSearch) {
      // Hybrid search combines semantic and keyword matching
      const semanticResults = await this.documentStore.search(query, {
        topK: topK * 2,
        filter: options.filter,
      });
      
      const keywordResults = await this.keywordSearch(query, {
        topK: topK * 2,
        filter: options.filter,
      });
      
      results = this.fuseResults(
        semanticResults,
        keywordResults,
        {
          semanticWeight: 0.7,
          keywordWeight: options.keywordBoost || 0.3,
        }
      );
      
      embeddingTokens = topK * 2 * 100; // Rough estimate
    } else {
      const searchResults = await this.documentStore.search(query, {
        topK,
        filter: options.filter,
        minScore,
      });
      
      results = searchResults;
      embeddingTokens = topK * 100;
    }
    
    // Optional reranking with cross-encoder
    if (options.rerank && results.length > 0) {
      results = await this.rerankResults(query, results);
    }
    
    return {
      results: results.slice(0, topK).map(r => ({
        text: r.text,
        score: r.score,
        metadata: r.metadata,
      })),
      query,
      totalResults: results.length,
      searchTimeMs: Date.now() - startTime,
      embeddingTokens,
    };
  }
  
  private async keywordSearch(
    query: string,
    options: { topK: number; filter?: Record<string, any> }
  ): Promise<Array<{ text: string; score: number; metadata: Record<string, any> }>> {
    // Simple keyword search - in production, use Elasticsearch/BM25
    // This is a placeholder implementation
    return [];
  }
  
  private fuseResults(
    semanticResults: Array<{ text: string; score: number; metadata: any }>,
    keywordResults: Array<{ text: string; score: number; metadata: any }>,
    weights: { semanticWeight: number; keywordWeight: number }
  ): Array<{ text: string; score: number; metadata: any }> {
    const scoreMap = new Map<string, {
      text: string;
      combinedScore: number;
      metadata: any;
    }>();
    
    // Normalize and combine semantic scores
    const maxSemantic = Math.max(...semanticResults.map(r => r.score), 0.001);
    for (const result of semanticResults) {
      const normalizedScore = result.score / maxSemantic;
      const combinedScore = normalizedScore * weights.semanticWeight;
      scoreMap.set(result.text, {
        text: result.text,
        combinedScore,
        metadata: result.metadata,
      });
    }
    
    // Add keyword scores
    const maxKeyword = Math.max(...keywordResults.map(r => r.score), 0.001);
    for (const result of keywordResults) {
      const normalizedScore = result.score / maxKeyword;
      const existing = scoreMap.get(result.text);
      if (existing) {
        existing.combinedScore += normalizedScore * weights.keywordWeight;
      } else {
        scoreMap.set(result.text, {
          text: result.text,
          combinedScore: normalizedScore * weights.keywordWeight,
          metadata: result.metadata,
        });
      }
    }
    
    return Array.from(scoreMap.values())
      .sort((a, b) => b.combinedScore - a.combinedScore);
  }
  
  private async rerankResults(
    query: string,
    results: Array<{ text: string; score: number; metadata: any }>
  ): Promise<Array<{ text: string; score: number; metadata: any }>> {
    // Use a cross-encoder for reranking
    // For production, consider using models like Cohere Rerank or BGE reranker
    const response = await this.openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        {
          role: 'system',
          content: `You are a relevance assessor. Rate how relevant each document is to the query on a scale of 0-10.
Return JSON array with format: [{"index": 0, "relevance": 8.5}, ...]`,
        },
        {
          role: 'user',
          content: `Query: ${query}\n\nDocuments:\n${results.map((r, i) => `${i}. ${r.text}`).join('\n')}`,
        },
      ],
      response_format: { type: 'json_schema', json_schema: {
        type: 'object',
        properties: {
          rankings: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                index: { type: 'integer' },
                relevance: { type: 'number' },
              },
              required: ['index', 'relevance'],
            },
          },
        },
      }},
      temperature: 0.1,
    });
    
    const rankings = JSON.parse(response.choices[0].message.content || '{}').rankings || [];
    
    return rankings
      .sort((a: any, b: any) => b.relevance - a.relevance)
      .map((rank: any) => ({
        ...results[rank.index],
        score: rank.relevance / 10,
      }));
  }
}

// RAG (Retrieval Augmented Generation) service
export class RAGService {
  private searchService: SemanticSearchService;
  private openai: OpenAI;
  private contextWindow: number;
  
  constructor(
    searchService: SemanticSearchService,
    openai: OpenAI,
    contextWindow: number = 4000
  ) {
    this.searchService = searchService;
    this.openai = openai;
    this.contextWindow = contextWindow;
  }
  
  async query(
    question: string,
    options: {
      topK?: number;
      systemPrompt?: string;
      hybridSearch?: boolean;
    } = {}
  ): Promise<{
    answer: string;
    sources: Array<{
      text: string;
      score: number;
      metadata: any;
    }>;
  }> {
    // Retrieve relevant documents
    const searchResults = await this.searchService.search(question, {
      topK: options.topK || 5,
      hybridSearch: options.hybridSearch,
    });
    
    // Build context from retrieved documents
    const context = this.buildContext(searchResults.results);
    
    // Generate answer with context
    const systemPrompt = options.systemPrompt || `Bạn là một trợ lý AI hữu ích. 
Sử dụng ngữ cảnh được cung cấp bên dưới để trả lời câu hỏi của người dùng.
Nếu ngữ cảnh không chứa thông tin cần thiết, hãy nói rõ điều này thay vì tạo ra câu trả lời không chính xác.
Trích dẫn nguồn khi có thể.`;
    
    const response = await this.openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        { role: 'system', content: systemPrompt },
        {
          role: 'user',
          content: `Ngữ cảnh:
${context}

Câu hỏi: ${question}`,
        },
      ],
      temperature: 0.3,
      max_tokens: 1000,
    });
    
    return {
      answer: response.choices[0].message.content || '',
      sources: searchResults.results.map(r => ({
        text: r.text,
        score: r.score,
        metadata: r.metadata,
      })),
    };
  }
  
  private buildContext(results: Array<{ text: string; score: number; metadata: any }>): string {
    const contexts: string[] = [];
    let totalChars = 0;
    
    for (const result of results) {
      const chunk = `[Nguồn: ${result.metadata.title || 'Unknown'} (${result.score.toFixed(2)})]\n${result.text}`;
      
      if (totalChars + chunk.length > this.contextWindow) {
        break;
      }
      
      contexts.push(chunk);
      totalChars += chunk.length;
    }
    
    return contexts.join('\n\n---\n\n');
  }
}
```

```python
# services/semantic_search.py - Semantic search service
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json
import time

@dataclass
class SearchResult:
    results: List[Dict[str, Any]]
    query: str
    total_results: int
    search_time_ms: float
    embedding_tokens: int

class SemanticSearchService:
    def __init__(self, document_store, openai_client):
        self.document_store = document_store
        self.openai = openai_client
    
    async def search(
        self,
        query: str,
        top_k: int = 5,
        min_score: float = 0.7,
        filter_criteria: Optional[Dict[str, Any]] = None,
        rerank: bool = False,
        hybrid_search: bool = False,
        keyword_boost: float = 0.3,
    ) -> SearchResult:
        start_time = time.time()
        
        if hybrid_search:
            semantic_results = await self.document_store.search(
                query,
                top_k=top_k * 2,
                filter_criteria=filter_criteria,
            )
            
            keyword_results = await self._keyword_search(
                query,
                top_k=top_k * 2,
                filter_criteria=filter_criteria,
            )
            
            results = self._fuse_results(
                semantic_results,
                keyword_results,
                semantic_weight=0.7,
                keyword_weight=keyword_boost,
            )
            embedding_tokens = top_k * 2 * 100
        else:
            results = await self.document_store.search(
                query,
                top_k=top_k,
                filter_criteria=filter_criteria,
                min_score=min_score,
            )
            embedding_tokens = top_k * 100
        
        if rerank and results:
            results = await self._rerank_results(query, results)
        
        return SearchResult(
            results=results[:top_k],
            query=query,
            total_results=len(results),
            search_time_ms=(time.time() - start_time) * 1000,
            embedding_tokens=embedding_tokens,
        )
    
    async def _keyword_search(
        self,
        query: str,
        top_k: int,
        filter_criteria: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        # Placeholder - use Elasticsearch/BM25 in production
        return []
    
    def _fuse_results(
        self,
        semantic_results: List[Dict[str, Any]],
        keyword_results: List[Dict[str, Any]],
        semantic_weight: float = 0.7,
        keyword_weight: float = 0.3,
    ) -> List[Dict[str, Any]]:
        score_map: Dict[str, Dict[str, Any]] = {}
        
        # Normalize semantic scores
        max_semantic = max((r['score'] for r in semantic_results), default=0.001)
        for result in semantic_results:
            normalized = result['score'] / max_semantic
            score_map[result['text']] = {
                'text': result['text'],
                'combined_score': normalized * semantic_weight,
                'metadata': result['metadata'],
            }
        
        # Add keyword scores
        max_keyword = max((r['score'] for r in keyword_results), default=0.001)
        for result in keyword_results:
            normalized = result['score'] / max_keyword
            existing = score_map.get(result['text'])
            if existing:
                existing['combined_score'] += normalized * keyword_weight
            else:
                score_map[result['text']] = {
                    'text': result['text'],
                    'combined_score': normalized * keyword_weight,
                    'metadata': result['metadata'],
                }
        
        return sorted(
            score_map.values(),
            key=lambda x: x['combined_score'],
            reverse=True
        )
    
    async def _rerank_results(
        self,
        query: str,
        results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        # Use cross-encoder for reranking
        response = self.openai.chat.completions.create(
            model='gpt-4o',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a relevance assessor. Rate how relevant each document is to the query on a scale of 0-10. Return JSON array with format: [{"index": 0, "relevance": 8.5}, ...]',
                },
                {
                    'role': 'user',
                    'content': f'Query: {query}\n\nDocuments:\n' + '\n'.join(
                        f'{i}. {r["text"]}' for i, r in enumerate(results)
                    ),
                },
            ],
            response_format={
                'type': 'json_schema',
                'json_schema': {
                    'type': 'object',
                    'properties': {
                        'rankings': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'index': {'type': 'integer'},
                                    'relevance': {'type': 'number'},
                                },
                                'required': ['index', 'relevance'],
                            },
                        },
                    },
                },
            },
            temperature=0.1,
        )
        
        rankings = json.loads(response.choices[0].message.content or '{}').get('rankings', [])
        
        return sorted(
            rankings,
            key=lambda x: x['relevance'],
            reverse=True,
        )

class RAGService:
    def __init__(
        self,
        search_service: SemanticSearchService,
        openai_client,
        context_window: int = 4000,
    ):
        self.search_service = search_service
        self.openai = openai_client
        self.context_window = context_window
    
    async def query(
        self,
        question: str,
        top_k: int = 5,
        system_prompt: Optional[str] = None,
        hybrid_search: bool = False,
    ) -> Dict[str, Any]:
        # Retrieve relevant documents
        search_results = await self.search_service.search(
            question,
            top_k=top_k,
            hybrid_search=hybrid_search,
        )
        
        # Build context
        context = self._build_context(search_results.results)
        
        # Generate answer
        default_system = """Bạn là một trợ lý AI hữu ích. 
Sử dụng ngữ cảnh được cung cấp bên dưới để trả lời câu hỏi của người dùng.
Nếu ngữ cảnh không chứa thông tin cần thiết, hãy nói rõ điều này thay vì tạo ra câu trả lời không chính xác.
Trích dẫn nguồn khi có thể."""
        
        response = self.openai.chat.completions.create(
            model='gpt-4o',
            messages=[
                {'role': 'system', 'content': system_prompt or default_system},
                {
                    'role': 'user',
                    'content': f'Ngữ cảnh:\n{context}\n\nCâu hỏi: {question}',
                },
            ],
            temperature=0.3,
            max_tokens=1000,
        )
        
        return {
            'answer': response.choices[0].message.content or '',
            'sources': search_results.results,
        }
    
    def _build_context(self, results: List[Dict[str, Any]]) -> str:
        contexts = []
        total_chars = 0
        
        for result in results:
            chunk = f"[Nguồn: {result['metadata'].get('title', 'Unknown')} ({result['score']:.2f})]\n{result['text']}"
            
            if total_chars + len(chunk) > self.context_window:
                break
            
            contexts.append(chunk)
            total_chars += len(chunk)
        
        return '\n\n---\n\n'.join(contexts)
```

## Vector Database Integration

### Pinecone Integration

```typescript
// integrations/pinecone.ts - Pinecone vector database integration
import { Pinecone } from '@pinecone-database/pinecone';

interface PineconeConfig {
  apiKey: string;
  indexName: string;
  environment?: string;
  dimension?: number;
  metric?: 'cosine' | 'euclidean' | 'dotproduct';
}

export class PineconeVectorStore {
  private client: Pinecone;
  private indexName: string;
  private index: any;
  
  constructor(config: PineconeConfig) {
    this.client = new Pinecone({
      apiKey: config.apiKey,
    });
    this.indexName = config.indexName;
  }
  
  async initialize(config?: {
    dimension?: number;
    metric?: 'cosine' | 'euclidean' | 'dotproduct';
  }): Promise<void> {
    // Check if index exists, create if not
    const indexes = await this.client.listIndexes();
    const indexExists = indexes.indexes?.some(i => i.name === this.indexName);
    
    if (!indexExists) {
      await this.client.createIndex({
        name: this.indexName,
        dimension: config?.dimension || 3072,
        metric: config?.metric || 'cosine',
        spec: {
          serverless: {
            cloud: 'aws',
            region: 'us-east-1',
          },
        },
      });
      
      // Wait for index to be ready
      await this.waitForIndex();
    }
    
    this.index = this.client.index(this.indexName);
  }
  
  private async waitForIndex(maxWaitMs: number = 60000): Promise<void> {
    const startTime = Date.now();
    while (Date.now() - startTime < maxWaitMs) {
      const description = await this.client.describeIndex(this.indexName);
      if (description.status?.ready) {
        return;
      }
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
    throw new Error('Index creation timed out');
  }
  
  async upsert(records: Array<{
    id: string;
    embedding: number[];
    metadata?: Record<string, any>;
  }>): Promise<void> {
    const vectors = records.map(record => ({
      id: record.id,
      values: record.embedding,
      metadata: record.metadata || {},
    }));
    
    // Pinecone recommends batches of 100 for upsert
    const batchSize = 100;
    for (let i = 0; i < vectors.length; i += batchSize) {
      const batch = vectors.slice(i, i + batchSize);
      await this.index.upsert(batch);
    }
  }
  
  async search(
    queryEmbedding: number[],
    options: {
      topK: number;
      filter?: Record<string, any>;
      includeVectors?: boolean;
      includeMetadata?: boolean;
    }
  ): Promise<Array<{
    id: string;
    score: number;
    metadata?: Record<string, any>;
    values?: number[];
  }>> {
    const queryResponse = await this.index.query({
      vector: queryEmbedding,
      topK: options.topK,
      filter: options.filter,
      includeValues: options.includeVectors ?? false,
      includeMetadata: options.includeMetadata ?? true,
    });
    
    return (queryResponse.matches || []).map(match => ({
      id: match.id,
      score: match.score || 0,
      metadata: match.metadata as Record<string, any> | undefined,
      values: match.values as number[] | undefined,
    }));
  }
  
  async delete(ids: string[]): Promise<void> {
    await this.index.deleteMany(ids);
  }
  
  async deleteAll(): Promise<void> {
    await this.index.deleteAll();
  }
  
  async getStats(): Promise<{
    totalVectors: number;
    dimension: number;
  }> {
    const stats = await this.index.describeIndexStats();
    return {
      totalVectors: stats.totalRecordCount || 0,
      dimension: stats.dimension || 0,
    };
  }
  
  // Pagination for large result sets
  async *scanAll(
    options: {
      limit?: number;
      filter?: Record<string, any>;
    } = {}
  ): AsyncGenerator<Array<{
    id: string;
    metadata?: Record<string, any>;
    values?: number[];
  }>, void, unknown> {
    let paginationToken: string | undefined;
    
    do {
      const response = await this.index.list({
        prefix: '',
        limit: options.limit || 1000,
        paginationToken,
        filter: options.filter,
        includeValues: true,
        includeMetadata: true,
      });
      
      if (response.vectors && response.vectors.length > 0) {
        yield response.vectors.map(v => ({
          id: v.id,
          metadata: v.metadata,
          values: v.values,
        }));
      }
      
      paginationToken = response.pagination?.next;
    } while (paginationToken);
  }
}
```

```python
# integrations/pinecone.py - Pinecone vector database integration
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any, Optional, AsyncGenerator
import time

class PineconeVectorStore:
    def __init__(
        self,
        api_key: str,
        index_name: str,
        environment: Optional[str] = None,
    ):
        self.client = Pinecone(api_key=api_key)
        self.index_name = index_name
        self.index = None
    
    async def initialize(
        self,
        dimension: int = 3072,
        metric: str = 'cosine',
        cloud: str = 'aws',
        region: str = 'us-east-1',
    ) -> None:
        # Check if index exists
        existing_indexes = [idx.name for idx in self.client.list_indexes()]
        
        if self.index_name not in existing_indexes:
            self.client.create_index(
                name=self.index_name,
                dimension=dimension,
                metric=metric,
                spec=ServerlessSpec(cloud=cloud, region=region),
            )
            
            # Wait for index to be ready
            self._wait_for_index()
        
        self.index = self.client.Index(self.index_name)
    
    def _wait_for_index(self, max_wait_ms: int = 60000) -> None:
        start_time = time.time() * 1000
        while (time.time() * 1000 - start_time) < max_wait_ms:
            description = self.client.describe_index(self.index_name)
            if description.status.get('ready'):
                return
            time.sleep(1)
        raise TimeoutError('Index creation timed out')
    
    async def upsert(
        self,
        records: List[Dict[str, Any]],
    ) -> None:
        vectors = [
            {
                'id': record['id'],
                'values': record['embedding'],
                'metadata': record.get('metadata', {}),
            }
            for record in records
        ]
        
        # Batch upsert (Pinecone recommends batches of 100)
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            self.index.upsert(vectors=batch)
    
    async def search(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        filter_criteria: Optional[Dict[str, Any]] = None,
        include_vectors: bool = False,
        include_metadata: bool = True,
    ) -> List[Dict[str, Any]]:
        query_response = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            filter=filter_criteria,
            include_values=include_vectors,
            include_metadata=include_metadata,
        )
        
        return [
            {
                'id': match['id'],
                'score': match.get('score', 0),
                'metadata': match.get('metadata'),
                'values': match.get('values'),
            }
            for match in query_response['matches'] or []
        ]
    
    async def delete(self, ids: List[str]) -> None:
        self.index.delete(ids=ids)
    
    async def delete_all(self) -> None:
        self.index.delete_all()
    
    async def get_stats(self) -> Dict[str, Any]:
        stats = self.index.describe_index_stats()
        return {
            'total_vectors': stats.get('total_record_count', 0),
            'dimension': stats.get('dimension', 0),
        }
```

### Weaviate Integration

```typescript
// integrations/weaviate.ts - Weaviate vector database integration
import Weaviate from 'weaviate-ts-client';

interface WeaviateConfig {
  httpUrl: string;
  grpcUrl?: string;
  apiKey?: string;
  headers?: Record<string, string>;
}

export class WeaviateVectorStore {
  private client: any;
  private className: string;
  
  constructor(config: WeaviateConfig, className: string = 'Document') {
    this.client = Weaviate.client({
      httpHost: config.httpUrl,
      grpcHost: config.grpcUrl,
      auth: config.apiKey ? new weaviate.Auth.ApiKey(config.apiKey) : undefined,
      headers: config.headers,
    });
    this.className = className;
  }
  
  async initialize(properties: string[] = ['text', 'title', 'url']): Promise<void> {
    // Check if schema exists
    try {
      await this.client.schema.classGetter().className(this.className).get();
    } catch {
      // Create schema
      await this.client.schema.classCreator().withClass({
        class: this.className,
        vectorizer: 'none', // We'll provide our own vectors
        properties: properties.map(p => ({
          name: p,
          dataType: ['text'],
        })),
      }).do();
    }
  }
  
  async upsert(records: Array<{
    id: string;
    embedding: number[];
    metadata: Record<string, any>;
  }>): Promise<void> {
    const batcher = this.client.batch.objectsBatcher();
    
    for (const record of records) {
      const obj = {
        class: this.className,
        id: record.id,
        vector: record.embedding,
        properties: record.metadata,
      };
      batcher.withObject(obj);
    }
    
    await batcher.do();
  }
  
  async search(
    queryEmbedding: number[],
    options: {
      topK: number;
      filter?: string;
      properties?: string[];
    }
  ): Promise<Array<{
    id: string;
    score: number;
    metadata: Record<string, any>;
  }>> {
    const response = await this.client.graphql
      .get()
      .withClassName(this.className)
      .withNearVector({ vector: queryEmbedding })
      .withLimit(options.topK)
      .withFields('id _additional { score } ' + (options.properties?.join(' ') || '*'))
      .do();
    
    if (options.filter) {
      // Apply where filter
      return this.applyFilter(response, options);
    }
    
    return (response.data[this.className] || []).map(item => ({
      id: item.id,
      score: item._additional?.score || 0,
      metadata: { ...item },
    }));
  }
  
  async hybridSearch(
    query: string,
    options: {
      topK: number;
      alpha?: number; // 0 = keyword, 1 = vector
      filter?: string;
    }
  ): Promise<Array<{
    id: string;
    score: number;
    metadata: Record<string, any>;
  }>> {
    const response = await this.client.graphql
      .get()
      .withClassName(this.className)
      .withHybrid({
        query,
        alpha: options.alpha || 0.5,
      })
      .withLimit(options.topK)
      .withFields('id _additional { score } *')
      .do();
    
    return (response.data[this.className] || []).map(item => ({
      id: item.id,
      score: item._additional?.score || 0,
      metadata: { ...item },
    }));
  }
  
  async delete(ids: string[]): Promise<void> {
    const deleter = this.client.batch.objectsBatchDeleter();
    
    for (const id of ids) {
      await deleter.withClassName(this.className).withId(id).do();
    }
  }
}

// Custom Weaviate Auth
namespace weaviate {
  export class Auth {
    static ApiKey(apiKey: string) {
      return { apiKey };
    }
  }
}
```

## Common Patterns

### Vector Cache Pattern

```typescript
// patterns/vectorCache.ts - Caching embeddings for repeated queries
import { EmbeddingService } from '../services/embeddingService';
import Redis from 'ioredis';

interface CachedEmbedding {
  embedding: number[];
  createdAt: Date;
  model: string;
}

export class EmbeddingCache {
  private redis: Redis;
  private embeddingService: EmbeddingService;
  private ttl: number; // seconds
  
  constructor(
    redis: Redis,
    embeddingService: EmbeddingService,
    ttl: number = 86400 * 7 // 7 days default
  ) {
    this.redis = redis;
    this.embeddingService = embeddingService;
    this.ttl = ttl;
  }
  
  private getCacheKey(text: string, model: string): string {
    // Simple hash for cache key
    const hash = this.hashText(text);
    return `embedding:${model}:${hash}`;
  }
  
  private hashText(text: string): string {
    // Simple hash function
    let hash = 0;
    for (let i = 0; i < text.length; i++) {
      const char = text.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash).toString(36);
  }
  
  async getEmbedding(text: string, model?: string): Promise<number[] | null> {
    const cacheKey = this.getCacheKey(text, model || 'default');
    
    const cached = await this.redis.get(cacheKey);
    if (cached) {
      const data: CachedEmbedding = JSON.parse(cached);
      return data.embedding;
    }
    
    return null;
  }
  
  async setEmbedding(text: string, embedding: number[], model?: string): Promise<void> {
    const cacheKey = this.getCacheKey(text, model || 'default');
    const data: CachedEmbedding = {
      embedding,
      createdAt: new Date(),
      model: model || 'default',
    };
    
    await this.redis.setex(cacheKey, this.ttl, JSON.stringify(data));
  }
  
  async getOrCreateEmbedding(
    text: string,
    model?: string
  ): Promise<{ embedding: number[]; cached: boolean }> {
    // Try cache first
    const cached = await this.getEmbedding(text, model);
    if (cached) {
      return { embedding: cached, cached: true };
    }
    
    // Create new embedding
    const result = await this.embeddingService.createEmbedding(text, { model });
    
    // Cache it
    await this.setEmbedding(text, result.embedding, model || result.model);
    
    return { embedding: result.embedding, cached: false };
  }
  
  async clearCache(pattern?: string): Promise<number> {
    const keys = await this.redis.keys(`embedding:${pattern || '*'}`);
    if (keys.length > 0) {
      return await this.redis.del(...keys);
    }
    return 0;
  }
  
  async getCacheStats(): Promise<{
    totalKeys: number;
    memoryUsage: string;
  }> {
    const keys = await this.redis.keys('embedding:*');
    const info = await this.redis.info('memory');
    
    return {
      totalKeys: keys.length,
      memoryUsage: info,
    };
  }
}
```

### Multi-tenancy with Namespaces

```typescript
// patterns/multiTenant.ts - Multi-tenant vector storage
import { PineconeVectorStore } from '../integrations/pinecone';

export class MultiTenantVectorStore {
  private stores: Map<string, PineconeVectorStore> = new Map();
  private config: any;
  
  constructor(config: any) {
    this.config = config;
  }
  
  private getNamespace(tenantId: string): string {
    return `tenant_${tenantId}`;
  }
  
  async getStore(tenantId: string): Promise<PineconeVectorStore> {
    if (this.stores.has(tenantId)) {
      return this.stores.get(tenantId)!;
    }
    
    const store = new PineconeVectorStore({
      apiKey: this.config.apiKey,
      indexName: this.config.indexName,
    });
    
    await store.initialize({
      dimension: this.config.dimension,
    });
    
    this.stores.set(tenantId, store);
    return store;
  }
  
  async indexForTenant(
    tenantId: string,
    records: Array<{
      id: string;
      embedding: number[];
      metadata: Record<string, any>;
    }>
  ): Promise<void> {
    const store = await this.getStore(tenantId);
    
    // Add tenant ID to metadata
    const tenantRecords = records.map(r => ({
      ...r,
      metadata: {
        ...r.metadata,
        tenantId,
      },
    }));
    
    await store.upsert(tenantRecords);
  }
  
  async searchForTenant(
    tenantId: string,
    queryEmbedding: number[],
    options: {
      topK: number;
      filter?: Record<string, any>;
    }
  ): Promise<Array<{
    id: string;
    score: number;
    metadata: Record<string, any>;
  }>> {
    const store = await this.getStore(tenantId);
    
    // Always filter by tenant
    const filter = {
      ...options.filter,
      tenantId,
    };
    
    return await store.search(queryEmbedding, {
      ...options,
      filter,
    });
  }
  
  async deleteTenantData(tenantId: string): Promise<void> {
    const store = await this.getStore(tenantId);
    
    // Delete all vectors with this tenant ID
    // In Pinecone, you'd need to query and then delete
    // This is simplified
    await store.deleteAll();
    
    // Remove from cache
    this.stores.delete(tenantId);
  }
}
```

## Troubleshooting

### Common Issues

```typescript
// troubleshooting/embeddingIssues.ts - Embedding issues guide
const embeddingIssueGuides = [
  {
    issue: 'Poor Search Results',
    symptoms: [
      'Relevant documents not returned',
      'High scores for irrelevant content',
      'Inconsistent ranking across queries',
    ],
    causes: [
      'Suboptimal chunking strategy',
      'Embedding model not suited for use case',
      'Missing or poor metadata for filtering',
      'Context window too small for retrieval',
    ],
    solutions: [
      'Experiment with chunk sizes (256-1024 tokens)',
      'Try different embedding models (3-large vs 3-small)',
      'Add semantic metadata for better filtering',
      'Increase context window or use parent-doc retrieval',
      'Implement reranking for top results',
    ],
  },
  {
    issue: 'High Latency',
    symptoms: [
      'Slow embedding generation',
      'Search queries taking too long',
      'Timeouts under load',
    ],
    causes: [
      'Large embedding dimension',
      'No caching for repeated queries',
      'Vector DB not optimized',
      'Network latency to vector DB',
    ],
    solutions: [
      'Reduce embedding dimensions (embedding-3 supports this)',
      'Implement Redis caching for embeddings',
      'Optimize HNSW parameters (M, efConstruction)',
      'Use regional vector DB deployment',
      'Batch requests where possible',
    ],
  },
  {
    issue: 'Dimension Mismatch Errors',
    symptoms: [
      'Vector dimension errors',
      'Search fails with dimension warnings',
      'Index creation failures',
    ],
    causes: [
      'Using different models for indexing vs search',
      'Dimension reduction applied inconsistently',
      'Wrong dimension setting in vector DB',
    ],
    solutions: [
      'Use same embedding model consistently',
      'If using dimensions parameter, always use same value',
      'Verify dimension setting in vector DB index',
      'Check that all vectors have correct length',
    ],
  },
  {
    issue: 'Out of Memory with Large Datasets',
    symptoms: [
      'System runs out of memory',
      'Slow index building',
      'Search degradation over time',
    ],
    causes: [
      'Loading all vectors in memory',
      'No quantization for large indices',
      'Memory leak in application',
    ],
    solutions: [
      'Use quantized embeddings (PQ/SQ)',
      'Implement memory-mapped index (DiskANN)',
      'Use cloud vector DB with automatic scaling',
      'Monitor and optimize memory usage',
      'Consider sharding large indices',
    ],
  },
];
```

## References

### Official Documentation

- [Embeddings API](https://platform.openai.com/docs/api-reference/embeddings)
- [Embedding Models](https://platform.openai.com/docs/guides/embeddings)
- [Embedding V3](https://help.openai.com/en/articles/8558687-openai-embedding-models)
- [Pinecone Documentation](https://docs.pinecone.io)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [Qdrant Documentation](https://qdrant.tech/documentation/)

### Research Papers

- [ANN Algorithms Comparison](https://arxiv.org/abs/1905.09788)
- [HNSW Paper](https://arxiv.org/abs/1604.02982)
- [Vector Quantization](https://engineering.fb.com/2017/03/29/data-infrastructure/faiss-a-library-for-efficient-similarity-search/)

### Tools và Libraries

- [FAISS (Facebook)](https://github.com/facebookresearch/faiss)
- [Qdrant](https://github.com/qdrant/qdrant)
- [Milvus](https://github.com/milvus-io/milvus)
- [Chroma](https://github.com/chroma-core/chroma)
- [NumPy/SciPy for similarity](https://numpy.org/doc/stable/reference/routines.math.html)

---

**Tài liệu này là một phần của Cursor Enterprise Framework Generator.**
