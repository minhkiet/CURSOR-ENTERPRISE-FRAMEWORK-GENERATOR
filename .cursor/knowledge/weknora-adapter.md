# WeKnora Knowledge Adapter

This adapter allows Cursor Enterprise Framework to connect with WeKnora for knowledge-based operations.

## Overview

The WeKnora Knowledge Adapter provides:
- Seamless integration with WeKnora knowledge bases
- Document ingestion and search capabilities
- Agent mode for complex reasoning tasks
- FAQ and document knowledge base support

## Configuration

### Environment Variables

```bash
# .env
WEKNORA_HOST=http://localhost:8080
WEKNORA_API_KEY=your-api-key
WEKNORA_KB_DEFAULT=default
WEKNORA_LLM_PROVIDER=openai
```

### Adapter Setup

```typescript
// lib/weknora-adapter.ts
import { WeKnoraClient } from '@weknora/client';

export interface WeKnoraConfig {
  host: string;
  apiKey: string;
  defaultKb?: string;
  llmProvider?: string;
}

export class WeKnoraAdapter {
  private client: WeKnoraClient;
  private defaultKb: string;

  constructor(config: WeKnoraConfig) {
    this.client = new WeKnoraClient({
      host: config.host,
      apiKey: config.apiKey,
    });
    this.defaultKb = config.defaultKb || 'default';
  }

  // Knowledge Base Operations
  async listKBs(): Promise<KB[]> {
    return this.client.kb.list();
  }

  async createKB(name: string, type: 'faq' | 'document' | 'wiki'): Promise<KB> {
    return this.client.kb.create({ name, type });
  }

  // Document Operations
  async uploadDocument(
    filePath: string,
    kbId: string = this.defaultKb,
    options?: UploadOptions
  ): Promise<UploadResult> {
    return this.client.doc.upload(filePath, { kbId, ...options });
  }

  async listDocuments(kbId: string = this.defaultKb): Promise<Document[]> {
    return this.client.doc.list({ kbId });
  }

  // Search Operations
  async search(
    query: string,
    kbId: string = this.defaultKb,
    options?: SearchOptions
  ): Promise<SearchResult[]> {
    return this.client.search({ kbId, query, ...options });
  }

  // Agent Operations
  async chat(
    message: string,
    kbId: string = this.defaultKb,
    options?: ChatOptions
  ): Promise<ChatResponse> {
    return this.client.chat({ kbId, message, mode: 'agent', ...options });
  }
}
```

## Integration with Existing Knowledge Bases

### Connect to Cursor's RAG System

```typescript
// lib/rag-integration.ts
import { WeKnoraAdapter } from './weknora-adapter';
import { VectorStore } from './vector-store';

export class HybridRAGSystem {
  constructor(
    private weknora: WeKnoraAdapter,
    private vectorStore: VectorStore
  ) {}

  async query(
    question: string,
    options?: { kbId?: string; useAgent?: boolean }
  ): Promise<HybridResponse> {
    const kbId = options?.kbId || this.weknora.defaultKb;

    // 1. Search local vector store
    const localResults = await this.vectorStore.search(question);

    // 2. Search WeKnora knowledge base
    const weknoraResults = await this.weknora.search(question, kbId);

    // 3. If using agent mode, get reasoning
    let agentReasoning = null;
    if (options?.useAgent) {
      const agentResponse = await this.weknora.chat(question, kbId);
      agentReasoning = agentResponse.reasoning;
    }

    // 4. Combine and rerank results
    return this.combineResults(localResults, weknoraResults, agentReasoning);
  }
}
```

### Connect to Document OCR System

```typescript
// lib/ocr-integration.ts
export class DocumentProcessingPipeline {
  constructor(private weknora: WeKnoraAdapter) {}

  async processDocument(
    filePath: string,
    options?: {
      ocr?: boolean;
      kbId?: string;
      generateQa?: boolean;
    }
  ): Promise<ProcessingResult> {
    const uploadOptions = {
      parser: options?.ocr ? 'paddleocr' : 'builtin',
      qa_generation: {
        enabled: options?.generateQa ?? false,
        count: 5,
      },
    };

    return this.weknora.uploadDocument(filePath, options?.kbId, uploadOptions);
  }
}
```

## Usage Examples

### Basic Q&A

```typescript
const adapter = new WeKnoraAdapter({
  host: process.env.WEKNORA_HOST,
  apiKey: process.env.WEKNORA_API_KEY,
});

// Simple search
const results = await adapter.search("What are the best practices for RAG?");
console.log(results);

// Agent mode for complex questions
const response = await adapter.chat(
  "Analyze the architecture patterns in our codebase and suggest improvements"
);
console.log(response.answer);
console.log(response.reasoning);
```

### Document Ingestion

```typescript
// Upload documents to knowledge base
await adapter.uploadDocument('./docs/manual.pdf', 'my-kb', {
  parser: 'paddleocr',
  chunk_size: 512,
});

// Generate Q&A pairs from documents
await adapter.uploadDocument('./docs/faq.md', 'my-kb', {
  qa_generation: { enabled: true, count: 10 },
});
```

### Multi-KB Search

```typescript
// Search across multiple knowledge bases
const kbIds = ['product-docs', 'api-reference', 'support-faq'];

const results = await Promise.all(
  kbIds.map(kbId => adapter.search('authentication', kbId))
);

const combined = results.flat().sort((a, b) => b.score - a.score);
```

## Workflow Integration

### With Skill System

```typescript
// When skill requires knowledge lookup
async function executeSkillWithKnowledge(skillName: string, context: Context) {
  // Check if skill needs knowledge base
  if (skillRequiresKnowledge(skillName)) {
    const relevantKB = getRelevantKB(skillName);
    const knowledge = await weknora.search(context.query, relevantKB);
    context.knowledgeContext = knowledge;
  }

  // Execute skill with knowledge context
  return executeSkill(skillName, context);
}
```

### With Memory System

```typescript
// Store important findings in WeKnora
async function rememberInsight(insight: Insight) {
  await weknora.uploadDocument(
    Buffer.from(JSON.stringify(insight)),
    'insights',
    { parser: 'builtin' }
  );
}

// Retrieve relevant memories
async function recallMemories(query: string) {
  return weknora.search(query, 'insights');
}
```

## Error Handling

```typescript
try {
  const result = await weknora.search(query);
} catch (error) {
  if (error instanceof WeKnoraAuthError) {
    // Re-authenticate
    await weknora.reconnect();
  } else if (error instanceof WeKnoraRateLimitError) {
    // Wait and retry
    await delay(1000);
    return weknora.search(query);
  } else {
    throw error;
  }
}
```

## Health Check

```typescript
async function checkWeKnoraHealth(): Promise<HealthStatus> {
  try {
    const kbs = await weknora.listKBs();
    return {
      status: 'healthy',
      kbCount: kbs.length,
      connected: true,
    };
  } catch (error) {
    return {
      status: 'unhealthy',
      error: error.message,
      connected: false,
    };
  }
}
```
