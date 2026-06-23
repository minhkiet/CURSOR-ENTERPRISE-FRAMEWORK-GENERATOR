---
title: Fine-tuning OpenAI Models
description: Hướng dẫn toàn diện về fine-tuning process, training data format, evaluation metrics và cost optimization
tags: [openai, fine-tuning, training, machine-learning, typescript, python]
created: 2026-06-23
version: 1.0.0
framework: cursor-enterprise
---

# Fine-tuning OpenAI Models

## Tổng quan

Fine-tuning là quá trình tinh chỉnh các pre-trained models của OpenAI trên dữ liệu custom để cải thiện performance cho specific tasks hoặc domains. Thay vì sử dụng generic model capabilities, fine-tuning cho phép bạn customize model behavior, improve consistency, reduce latency, và optimize cost cho your particular use case.

OpenAI hỗ trợ fine-tuning cho nhiều models bao gồm GPT-4o mini, GPT-3.5 Turbo, và các models khác. Mỗi model có different capabilities và pricing structures. Fine-tuning sử dụng supervised learning để adjust model weights dựa trên your training examples, resulting in a new model variant specialized for your data.

Quá trình fine-tuning bao gồm nhiều steps từ data preparation, training configuration, model training, đến evaluation và deployment. Understanding mỗi step là critical để achieve desired results. Trong tài liệu này, chúng ta sẽ cover end-to-end fine-tuning workflow với practical examples cho cả TypeScript và Python.

Fine-tuning mang lại nhiều benefits so với few-shot prompting: lower latency (smaller models với faster inference), consistent output format, reduced token usage (no need for examples in each request), và better control over model behavior. Tuy nhiên, fine-tuning cũng đòi hỏi significant investment trong data preparation và ongoing maintenance.

## Mục đích và Phạm vi

Tài liệu này cung cấp hướng dẫn toàn diện về fine-tuning OpenAI models từ A đến Z. Phạm vi bao gồm data preparation và formatting, training configuration và hyperparameters, training process monitoring, model evaluation và selection, inference optimization, và cost management strategies.

Chúng tôi sẽ cover practical implementation patterns cho production use cases, bao gồm how to prepare high-quality training data, how to evaluate fine-tuned models, và how to optimize costs. Các examples được provided cho cả TypeScript và Python sử dụng OpenAI SDK.

## Các Khái niệm Chính

### Khi nào nên Fine-tune

Fine-tuning phù hợp cho nhiều use cases nhưng không phải lúc nào cũng là best approach. Understanding khi nào nên fine-tune versus sử dụng prompting là critical decision.

**Nên Fine-tune khi:**

1. **Consistent Output Format**: Bạn cần model luôn output trong specific format (JSON, specific structure) và prompting không đủ reliable. Ví dụ: structured data extraction, form generation.

2. **Domain-Specific Vocabulary**: Model cần understand và use domain-specific terminology, abbreviations, hoặc conventions. Ví dụ: medical records, legal documents, technical support.

3. **Complex Task Patterns**: Task có complex patterns hoặc subtle nuances mà few-shot examples không capture được consistently. Ví dụ: sentiment analysis với nuanced categories.

4. **Lower Latency Required**: Bạn cần faster inference time và có thể use a smaller, fine-tuned model thay vì large frontier model với examples.

5. **Cost Optimization**: Bạn có high volume requests và fine-tuning với smaller model tổng chi phí thấp hơn significantly so với larger models với extensive prompting.

6. **Brand Voice/P-tone**: Model cần adopt specific writing style, tone, hoặc communication patterns cho your brand hoặc organization.

**Không nên Fine-tune khi:**

1. **Rapidly Changing Data**: Data hoặc requirements thay đổi frequently. Fine-tuned models require retraining để update.

2. **Small Dataset**: Bạn có ít hơn vài hundred high-quality examples. Better to prompt.

3. **Simple Tasks**: Task straightforward và prompting works well. Fine-tuning adds complexity không cần thiết.

4. **Experimentation Phase**: Bạn đang still experimenting với task definition. Prompt first, then fine-tune once stable.

### Supported Models

OpenAI hỗ trợ fine-tuning cho các models sau:

**GPT-4o mini** (recommended for most cases):
- Best balance of capability và cost
- Faster inference than larger models
- Training: $0.003 per 1K tokens
- Input: $0.00015 per 1K tokens
- Output: $0.0006 per 1K tokens

**GPT-3.5 Turbo** (legacy but still supported):
- Good for simple tasks
- Faster than GPT-4 models
- Training: $0.008 per 1K tokens
- Input: $0.003 per 1K tokens
- Output: $0.006 per 1K tokens

**babbage-002 và davinci-002** (legacy base models):
- Can be fine-tuned but not recommended
- Less capable than instruction-tuned models
- Requires more training data
- No chat-completion optimization

**Fine-tune vs Base Models**:

Fine-tuned versions của instruction-tuned models (như GPT-3.5 Turbo) đã được trained với instruction-following data, nên chúng perform better trong conversational contexts. Base models chỉ predict next token và require more examples để learn task patterns.

## Training Data Preparation

### Data Format Requirements

OpenAI fine-tuning yêu cầu data trong JSONL format với chat-style messages. Mỗi line chứa một training example với messages array.

```typescript
// types/trainingData.ts - Training data types
interface TrainingMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

interface TrainingExample {
  messages: TrainingMessage[];
}

interface ValidationExample extends TrainingExample {
  // Same structure, used for validation during training
}

// Example training data
const trainingData: TrainingExample[] = [
  {
    messages: [
      {
        role: 'system',
        content: 'Bạn là một trợ lý kỹ thuật chuyên nghiệp cho phần mềm TechCRM.',
      },
      {
        role: 'user',
        content: 'Làm thế nào để tạo một pipeline mới trong hệ thống?',
      },
      {
        role: 'assistant',
        content: 'Để tạo pipeline mới trong TechCRM, bạn cần thực hiện các bước sau:\n\n1. Truy cập mục "Cài đặt" từ menu chính\n2. Chọn "Quản lý Pipeline"\n3. Click nút "Tạo Pipeline Mới"\n4. Điền thông tin: tên pipeline, mô tả, các giai đoạn\n5. Click "Lưu" để hoàn tất',
      },
    ],
  },
  {
    messages: [
      {
        role: 'system',
        content: 'Bạn là một trợ lý kỹ thuật chuyên nghiệp cho phần mềm TechCRM.',
      },
      {
        role: 'user',
        content: 'Tôi gặp lỗi khi export báo cáo. Log có ghi "Permission denied".',
      },
      {
        role: 'assistant',
        content: 'Lỗi "Permission denied" khi export báo cáo thường do thiếu quyền truy cập. Hãy kiểm tra:\n\n1. Bạn có quyền "Xuất báo cáo" trong role không?\n2. Thư mục lưu báo cáo có quyền ghi không?\n3. Liên hệ admin nếu cần cấp quyền.',
      },
    ],
  },
];

// JSONL format for API upload
function convertToJSONL(data: TrainingExample[]): string {
  return data.map(example => JSON.stringify(example)).join('\n');
}

// Validate training data
function validateTrainingData(data: TrainingExample[]): {
  valid: boolean;
  errors: string[];
  warnings: string[];
} {
  const errors: string[] = [];
  const warnings: string[] = [];
  
  if (data.length < 10) {
    warnings.push(`Dataset có ${data.length} examples. Khuyến nghị ít nhất 10-20 examples để bắt đầu fine-tuning.`);
  }
  
  for (let i = 0; i < data.length; i++) {
    const example = data[i];
    
    // Check message structure
    if (!example.messages || example.messages.length === 0) {
      errors.push(`Example ${i}: Thiếu messages array`);
      continue;
    }
    
    // Check for system message
    const hasSystem = example.messages.some(m => m.role === 'system');
    if (!hasSystem) {
      warnings.push(`Example ${i}: Không có system message. System message giúp định hướng model behavior.`);
    }
    
    // Check for assistant message
    const hasAssistant = example.messages.some(m => m.role === 'assistant');
    if (!hasAssistant) {
      errors.push(`Example ${i}: Thiếu assistant message - cần có response mẫu`);
    }
    
    // Check message content
    for (let j = 0; j < example.messages.length; j++) {
      const message = example.messages[j];
      
      if (!message.content || message.content.trim() === '') {
        errors.push(`Example ${i}, Message ${j}: Content rỗng`);
      }
      
      if (!['system', 'user', 'assistant'].includes(message.role)) {
        errors.push(`Example ${i}, Message ${j}: Invalid role "${message.role}"`);
      }
    }
    
    // Check conversation flow
    const validFlow = example.messages.every((msg, idx) => {
      if (idx === 0) return true;
      const prevMsg = example.messages[idx - 1];
      // User can follow system, assistant, hoặc user
      // Assistant chỉ follow user hoặc system
      if (msg.role === 'assistant') {
        return prevMsg.role === 'user' || prevMsg.role === 'system';
      }
      return true;
    });
    
    if (!validFlow) {
      warnings.push(`Example ${i}: Cấu trúc hội thoại có thể không optimal`);
    }
  }
  
  return {
    valid: errors.length === 0,
    errors,
    warnings,
  };
}

// Estimate token count for training
function estimateTrainingTokens(data: TrainingExample[]): number {
  // Rough estimate: 1 token ≈ 4 characters + overhead
  const CHARS_PER_TOKEN = 4;
  const OVERHEAD_PER_MESSAGE = 4; // Role tokens overhead
  
  let totalChars = 0;
  
  for (const example of data) {
    for (const message of example.messages) {
      totalChars += message.content.length;
      totalChars += OVERHEAD_PER_MESSAGE;
    }
    totalChars += 3; // Message format overhead
  }
  
  return Math.ceil(totalChars / CHARS_PER_TOKEN);
}
```

```python
# types/training_data.py - Training data types
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import json

@dataclass
class TrainingMessage:
    role: str  # 'system', 'user', 'assistant'
    content: str

@dataclass
class TrainingExample:
    messages: List[TrainingMessage]
    
    def to_dict(self) -> Dict:
        return {
            'messages': [
                {'role': m.role, 'content': m.content}
                for m in self.messages
            ]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TrainingExample':
        return cls(
            messages=[
                TrainingMessage(role=m['role'], content=m['content'])
                for m in data['messages']
            ]
        )

def convert_to_jsonl(examples: List[TrainingExample]) -> str:
    """Convert training examples to JSONL format."""
    return '\n'.join(json.dumps(ex.to_dict()) for ex in examples)

def validate_training_data(
    data: List[TrainingExample]
) -> Tuple[bool, List[str], List[str]]:
    """Validate training data and return errors and warnings."""
    errors = []
    warnings = []
    
    if len(data) < 10:
        warnings.append(
            f"Dataset có {len(data)} examples. "
            "Khuyến nghị ít nhất 10-20 examples để bắt đầu fine-tuning."
        )
    
    for i, example in enumerate(data):
        # Check message structure
        if not example.messages:
            errors.append(f"Example {i}: Thiếu messages array")
            continue
        
        # Check for system message
        has_system = any(m.role == 'system' for m in example.messages)
        if not has_system:
            warnings.append(
                f"Example {i}: Không có system message"
            )
        
        # Check for assistant message
        has_assistant = any(m.role == 'assistant' for m in example.messages)
        if not has_assistant:
            errors.append(
                f"Example {i}: Thiếu assistant message"
            )
        
        # Check message content
        for j, message in enumerate(example.messages):
            if not message.content or not message.content.strip():
                errors.append(f"Example {i}, Message {j}: Content rỗng")
            
            if message.role not in ['system', 'user', 'assistant']:
                errors.append(
                    f"Example {i}, Message {j}: Invalid role '{message.role}'"
                )
    
    return len(errors) == 0, errors, warnings

def estimate_training_tokens(data: List[TrainingExample]) -> int:
    """Estimate total tokens for training."""
    CHARS_PER_TOKEN = 4
    OVERHEAD_PER_MESSAGE = 4
    
    total_chars = 0
    
    for example in data:
        for message in example.messages:
            total_chars += len(message.content)
            total_chars += OVERHEAD_PER_MESSAGE
        total_chars += 3  # Format overhead
    
    return (total_chars // CHARS_PER_TOKEN) + 1
```

### Data Quality Guidelines

High-quality training data là yếu tố quyết định success của fine-tuning. Dưới đây là guidelines cho việc prepare training data:

**Quality Standards:**

1. **Consistency**: Tất cả examples nên follow same format và conventions. Nếu một số responses dùng markdown và một số không, model sẽ confused.

2. **Completeness**: Mỗi response nên be complete và address đầy đủ user request. Không nên có incomplete responses.

3. **Accuracy**: Content trong responses phải correct và reliable. Model sẽ learn từ cả correct và incorrect examples.

4. **Diversity**: Dataset nên cover đa dạng scenarios và edge cases. Không nên chỉ có happy path.

5. **Format Consistency**: Nếu format output là JSON, tất cả examples nên output valid JSON với consistent structure.

```typescript
// utils/dataAugmentation.ts - Data augmentation for training
interface AugmentedExample extends TrainingExample {
  augmentationType: string;
}

export function augmentTrainingData(
  examples: TrainingExample[],
  options: {
    paraphrase?: boolean;
    addVariations?: boolean;
    expandContexts?: boolean;
  } = {}
): TrainingExample[] {
  const augmented: TrainingExample[] = [...examples];
  
  if (options.paraphrase) {
    // Add paraphrase variations
    // In production, use LLM to generate paraphrases
  }
  
  if (options.addVariations) {
    // Add variations with different phrasings
  }
  
  if (options.expandContexts) {
    // Add more detailed context to responses
  }
  
  return augmented;
}

// Balance dataset
export function balanceDataset(
  examples: TrainingExample[],
  labelKey: (ex: TrainingExample) => string
): TrainingExample[] {
  const labelCounts = new Map<string, number>();
  
  // Count labels
  for (const ex of examples) {
    const label = labelKey(ex);
    labelCounts.set(label, (labelCounts.get(label) || 0) + 1);
  }
  
  // Find minimum count
  const minCount = Math.min(...labelCounts.values());
  
  // Sample equally
  const balanced: TrainingExample[] = [];
  const labelExamples = new Map<string, TrainingExample[]>();
  
  for (const ex of examples) {
    const label = labelKey(ex);
    if (!labelExamples.has(label)) {
      labelExamples.set(label, []);
    }
    labelExamples.get(label)!.push(ex);
  }
  
  for (const [label, exs] of labelExamples) {
    const sampled = shuffleArray(exs).slice(0, minCount);
    balanced.push(...sampled);
  }
  
  return shuffleArray(balanced);
}

function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}
```

## Fine-tuning Process

### Starting Fine-tuning Job

```typescript
// services/fineTuningService.ts - Fine-tuning management
import OpenAI from 'openai';
import * as fs from 'fs';
import * as path from 'path';

interface FineTuningConfig {
  model: string;
  trainingFile: string;
  validationFile?: string;
  nEpochs?: number;
  batchSize?: number;
  learningRateMultiplier?: number;
  promptLossWeight?: number;
  classificationSettings?: {
    numClasses: number;
    positiveClassWeight?: number;
  };
  hyperparameters?: {
    batch_size?: 'auto' | number;
    learning_rate_multiplier?: 'auto' | number;
    num_epochs?: 'auto' | number;
  };
}

interface FineTuningJob {
  id: string;
  model: string;
  trainingFile: string;
  validationFile?: string;
  status: 'queued' | 'running' | 'succeeded' | 'failed' | 'cancelled';
  fineTunedModel?: string;
  createdAt: Date;
  finishedAt?: Date;
  error?: string;
  metrics?: {
    step: number;
    trainingLoss: number;
    trainingAccuracy?: number;
    validLoss?: number;
    validMeanTokenAccuracy?: number;
  }[];
}

export class FineTuningService {
  private client: OpenAI;
  
  constructor(client: OpenAI) {
    this.client = client;
  }
  
  async uploadTrainingFile(
    filePath: string,
    purpose: string = 'fine-tune'
  ): Promise<{ fileId: string; bytes: number }> {
    const fileStream = fs.createReadStream(filePath);
    
    const uploadResponse = await this.client.files.create({
      file: fileStream,
      purpose,
    });
    
    console.log(`Uploaded file: ${uploadResponse.id}`);
    console.log(`Size: ${uploadResponse.bytes} bytes`);
    
    return {
      fileId: uploadResponse.id,
      bytes: uploadResponse.bytes,
    };
  }
  
  async createFineTuningJob(
    config: FineTuningConfig
  ): Promise<string> {
    const createParams: any = {
      training_file: config.trainingFile,
      model: config.model,
    };
    
    if (config.validationFile) {
      createParams.validation_file = config.validationFile;
    }
    
    if (config.nEpochs) {
      createParams.hyperparameters = {
        ...createParams.hyperparameters,
        num_epochs: config.nEpochs,
      };
    }
    
    if (config.batchSize) {
      createParams.hyperparameters = {
        ...createParams.hyperparameters,
        batch_size: config.batchSize,
      };
    }
    
    if (config.learningRateMultiplier) {
      createParams.hyperparameters = {
        ...createParams.hyperparameters,
        learning_rate_multiplier: config.learningRateMultiplier,
      };
    }
    
    if (config.classificationSettings) {
      createParams.classification_settings = config.classificationSettings;
    }
    
    const job = await this.client.fineTuning.jobs.create(createParams);
    
    console.log(`Created fine-tuning job: ${job.id}`);
    console.log(`Status: ${job.status}`);
    
    return job.id;
  }
  
  async getJobStatus(jobId: string): Promise<FineTuningJob> {
    const job = await this.client.fineTuning.jobs.retrieve(jobId);
    
    return {
      id: job.id,
      model: job.model,
      trainingFile: job.training_file,
      validationFile: job.validation_file,
      status: job.status,
      fineTunedModel: job.fine_tuned_model,
      createdAt: new Date(job.created_at * 1000),
      finishedAt: job.finished_at ? new Date(job.finished_at * 1000) : undefined,
      error: job.error?.message,
    };
  }
  
  async listJobs(limit: number = 20): Promise<FineTuningJob[]> {
    const jobs = await this.client.fineTuning.jobs.list({ limit });
    
    return jobs.data.map(job => ({
      id: job.id,
      model: job.model,
      trainingFile: job.training_file,
      validationFile: job.validation_file,
      status: job.status,
      fineTunedModel: job.fine_tuned_model,
      createdAt: new Date(job.created_at * 1000),
      finishedAt: job.finished_at ? new Date(job.finished_at * 1000) : undefined,
      error: job.error?.message,
    }));
  }
  
  async getJobEvents(jobId: string): Promise<Array<{
    type: string;
    message: string;
    createdAt: Date;
  }>> {
    const events = await this.client.fineTuning.jobs.listEvents(jobId, { limit: 100 });
    
    return events.data.map(event => ({
      type: event.type,
      message: event.message,
      createdAt: new Date(event.created_at * 1000),
    }));
  }
  
  async cancelJob(jobId: string): Promise<void> {
    await this.client.fineTuning.jobs.cancel(jobId);
    console.log(`Cancelled fine-tuning job: ${jobId}`);
  }
  
  async deleteModel(modelId: string): Promise<void> {
    await this.client.models.del(modelId);
    console.log(`Deleted model: ${modelId}`);
  }
  
  async waitForCompletion(
    jobId: string,
    onProgress?: (status: FineTuningJob) => void,
    pollIntervalMs: number = 30000
  ): Promise<FineTuningJob> {
    return new Promise((resolve, reject) => {
      const poll = async () => {
        try {
          const status = await this.getJobStatus(jobId);
          
          if (onProgress) {
            onProgress(status);
          }
          
          if (status.status === 'succeeded') {
            resolve(status);
            return;
          }
          
          if (status.status === 'failed') {
            reject(new Error(`Fine-tuning failed: ${status.error}`));
            return;
          }
          
          if (status.status === 'cancelled') {
            reject(new Error('Fine-tuning was cancelled'));
            return;
          }
          
          // Continue polling
          setTimeout(poll, pollIntervalMs);
        } catch (error) {
          reject(error);
        }
      };
      
      poll();
    });
  }
}
```

```python
# services/fine_tuning_service.py - Fine-tuning management
from openai import OpenAI
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import time
import os

@dataclass
class FineTuningConfig:
    model: str
    training_file: str
    validation_file: Optional[str] = None
    n_epochs: Optional[int] = None
    batch_size: Optional[int] = None
    learning_rate_multiplier: Optional[float] = None
    classification_settings: Optional[Dict[str, Any]] = None

@dataclass
class FineTuningJob:
    id: str
    model: str
    training_file: str
    validation_file: Optional[str]
    status: str
    fine_tuned_model: Optional[str]
    created_at: datetime
    finished_at: Optional[datetime]
    error: Optional[str]
    metrics: List[Dict[str, Any]]

class FineTuningService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    def upload_training_file(
        self,
        file_path: str,
        purpose: str = 'fine-tune'
    ) -> Dict[str, Any]:
        """Upload training file to OpenAI."""
        with open(file_path, 'rb') as f:
            upload_response = self.client.files.create(
                file=f,
                purpose=purpose
            )
        
        print(f"Uploaded file: {upload_response.id}")
        print(f"Size: {upload_response.bytes} bytes")
        
        return {
            'file_id': upload_response.id,
            'bytes': upload_response.bytes,
        }
    
    def create_fine_tuning_job(
        self,
        config: FineTuningConfig
    ) -> str:
        """Create a new fine-tuning job."""
        create_params = {
            'training_file': config.training_file,
            'model': config.model,
        }
        
        if config.validation_file:
            create_params['validation_file'] = config.validation_file
        
        hyperparameters = {}
        if config.n_epochs:
            hyperparameters['num_epochs'] = config.n_epochs
        if config.batch_size:
            hyperparameters['batch_size'] = config.batch_size
        if config.learning_rate_multiplier:
            hyperparameters['learning_rate_multiplier'] = config.learning_rate_multiplier
        
        if hyperparameters:
            create_params['hyperparameters'] = hyperparameters
        
        if config.classification_settings:
            create_params['classification_settings'] = config.classification_settings
        
        job = self.client.fine_tuning.jobs.create(**create_params)
        
        print(f"Created fine-tuning job: {job.id}")
        print(f"Status: {job.status}")
        
        return job.id
    
    def get_job_status(self, job_id: str) -> FineTuningJob:
        """Get fine-tuning job status."""
        job = self.client.fine_tuning.jobs.retrieve(job_id)
        
        return FineTuningJob(
            id=job.id,
            model=job.model,
            training_file=job.training_file,
            validation_file=job.validation_file,
            status=job.status,
            fine_tuned_model=job.fine_tuned_model,
            created_at=datetime.fromtimestamp(job.created_at),
            finished_at=datetime.fromtimestamp(job.finished_at) if job.finished_at else None,
            error=job.error.message if job.error else None,
            metrics=[],
        )
    
    def list_jobs(self, limit: int = 20) -> List[FineTuningJob]:
        """List recent fine-tuning jobs."""
        jobs = self.client.fine_tuning.jobs.list(limit=limit)
        
        return [
            FineTuningJob(
                id=job.id,
                model=job.model,
                training_file=job.training_file,
                validation_file=job.validation_file,
                status=job.status,
                fine_tuned_model=job.fine_tuned_model,
                created_at=datetime.fromtimestamp(job.created_at),
                finished_at=datetime.fromtimestamp(job.finished_at) if job.finished_at else None,
                error=job.error.message if job.error else None,
                metrics=[],
            )
            for job in jobs.data
        ]
    
    def get_job_events(self, job_id: str) -> List[Dict[str, Any]]:
        """Get events for a fine-tuning job."""
        events = self.client.fine_tuning.jobs.list_events(
            job_id,
            limit=100
        )
        
        return [
            {
                'type': event.type,
                'message': event.message,
                'created_at': datetime.fromtimestamp(event.created_at),
            }
            for event in events.data
        ]
    
    def cancel_job(self, job_id: str) -> None:
        """Cancel a fine-tuning job."""
        self.client.fine_tuning.jobs.cancel(job_id)
        print(f"Cancelled fine-tuning job: {job_id}")
    
    def delete_model(self, model_id: str) -> None:
        """Delete a fine-tuned model."""
        self.client.models.delete(model_id)
        print(f"Deleted model: {model_id}")
    
    def wait_for_completion(
        self,
        job_id: str,
        on_progress: Optional[callable] = None,
        poll_interval_seconds: float = 30
    ) -> FineTuningJob:
        """Wait for fine-tuning job to complete."""
        while True:
            status = self.get_job_status(job_id)
            
            if on_progress:
                on_progress(status)
            
            if status.status == 'succeeded':
                return status
            
            if status.status == 'failed':
                raise RuntimeError(f"Fine-tuning failed: {status.error}")
            
            if status.status == 'cancelled':
                raise RuntimeError("Fine-tuning was cancelled")
            
            time.sleep(poll_interval_seconds)
```

### Monitoring Training Progress

```typescript
// services/trainingMonitor.ts - Training progress monitoring
export class TrainingMonitor {
  private jobId: string;
  private service: FineTuningService;
  private eventHistory: Map<string, any> = new Map();
  
  constructor(jobId: string, service: FineTuningService) {
    this.jobId = jobId;
    this.service = service;
  }
  
  async startMonitoring(
    onUpdate: (metrics: TrainingMetrics) => void,
    pollIntervalMs: number = 30000
  ): Promise<void> {
    let lastStep = 0;
    
    const poll = async () => {
      try {
        const status = await this.service.getJobStatus(this.jobId);
        
        if (status.status === 'succeeded' || status.status === 'failed') {
          return;
        }
        
        // Get events for progress
        const events = await this.service.getJobEvents(this.jobId);
        
        // Extract training metrics
        const metrics = this.extractMetrics(events);
        
        if (metrics.step > lastStep) {
          lastStep = metrics.step;
          onUpdate(metrics);
        }
        
        setTimeout(poll, pollIntervalMs);
      } catch (error) {
        console.error('Monitoring error:', error);
        setTimeout(poll, pollIntervalMs);
      }
    };
    
    poll();
  }
  
  private extractMetrics(events: any[]): TrainingMetrics {
    const trainingLosses: number[] = [];
    const validLosses: number[] = [];
    let currentStep = 0;
    
    for (const event of events) {
      if (event.message.includes('training_loss:')) {
        const match = event.message.match(/training_loss:\s*([\d.]+)/);
        if (match) {
          trainingLosses.push(parseFloat(match[1]));
        }
      }
      
      if (event.message.includes('step')) {
        const match = event.message.match(/step (\d+)/);
        if (match) {
          currentStep = parseInt(match[1]);
        }
      }
    }
    
    return {
      step: currentStep,
      trainingLoss: trainingLosses[trainingLosses.length - 1] || 0,
      lossHistory: trainingLosses,
    };
  }
}

interface TrainingMetrics {
  step: number;
  trainingLoss: number;
  validLoss?: number;
  trainingAccuracy?: number;
  validAccuracy?: number;
  lossHistory: number[];
}
```

## Model Evaluation

### Evaluation Strategies

```typescript
// services/evaluationService.ts - Model evaluation
import OpenAI from 'openai';

interface EvaluationResult {
  overall: {
    accuracy: number;
    precision: number;
    recall: number;
    f1Score: number;
  };
  perCategory: Map<string, {
    truePositives: number;
    falsePositives: number;
    falseNegatives: number;
    precision: number;
    recall: number;
    f1: number;
  }>;
  examples: {
    input: string;
    expected: string;
    predicted: string;
    correct: boolean;
  }[];
}

export class EvaluationService {
  private client: OpenAI;
  
  constructor(client: OpenAI) {
    this.client = client;
  }
  
  async evaluateClassification(
    modelName: string,
    testData: Array<{
      input: string;
      expectedCategory: string;
    }>,
    categories: string[]
  ): Promise<EvaluationResult> {
    const examples: EvaluationResult['examples'] = [];
    const confusionMatrix = new Map<string, Map<string, number>>();
    
    // Initialize confusion matrix
    for (const cat of categories) {
      confusionMatrix.set(cat, new Map());
      for (const cat2 of categories) {
        confusionMatrix.get(cat)!.set(cat2, 0);
      }
    }
    
    // Run evaluation
    for (const testCase of testData) {
      const response = await this.client.chat.completions.create({
        model: modelName,
        messages: [
          {
            role: 'user',
            content: `Classify: ${testCase.input}\n\nCategories: ${categories.join(', ')}`,
          },
        ],
        temperature: 0,
        max_tokens: 50,
      });
      
      const predicted = this.extractCategory(
        response.choices[0].message.content || '',
        categories
      );
      const correct = predicted === testCase.expectedCategory;
      
      examples.push({
        input: testCase.input,
        expected: testCase.expectedCategory,
        predicted,
        correct,
      });
      
      // Update confusion matrix
      confusionMatrix
        .get(testCase.expectedCategory)!
        .set(predicted, (confusionMatrix.get(testCase.expectedCategory)!.get(predicted) || 0) + 1);
    }
    
    // Calculate metrics
    const { overall, perCategory } = this.calculateMetrics(
      confusionMatrix,
      categories
    );
    
    return {
      overall,
      perCategory,
      examples,
    };
  }
  
  private extractCategory(response: string, categories: string[]): string {
    const lowerResponse = response.toLowerCase();
    
    for (const category of categories) {
      if (lowerResponse.includes(category.toLowerCase())) {
        return category;
      }
    }
    
    return categories[0]; // Default to first category
  }
  
  private calculateMetrics(
    confusionMatrix: Map<string, Map<string, number>>,
    categories: string[]
  ): {
    overall: EvaluationResult['overall'];
    perCategory: EvaluationResult['perCategory'];
  } {
    const perCategory = new Map();
    let totalTP = 0;
    let totalFP = 0;
    let totalFN = 0;
    
    for (const category of categories) {
      const row = confusionMatrix.get(category)!;
      let tp = 0;
      let fp = 0;
      let fn = 0;
      
      for (const [predicted, count] of row) {
        if (predicted === category) {
          tp = count;
        } else {
          fp += count;
        }
      }
      
      for (const [actual, count] of confusionMatrix) {
        if (actual !== category) {
          fn += row.get(actual) || 0;
        }
      }
      
      const precision = tp + fp > 0 ? tp / (tp + fp) : 0;
      const recall = tp + fn > 0 ? tp / (tp + fn) : 0;
      const f1 = precision + recall > 0 ? 2 * (precision * recall) / (precision + recall) : 0;
      
      perCategory.set(category, { tp, fp, fn, precision, recall, f1 } as any);
      
      totalTP += tp;
      totalFP += fp;
      totalFN += fn;
    }
    
    const overallPrecision = totalTP + totalFP > 0 ? totalTP / (totalTP + totalFP) : 0;
    const overallRecall = totalTP + totalFN > 0 ? totalTP / (totalTP + totalFN) : 0;
    const overallF1 = overallPrecision + overallRecall > 0
      ? 2 * (overallPrecision * overallRecall) / (overallPrecision + overallRecall)
      : 0;
    
    return {
      overall: {
        accuracy: totalTP / (totalTP + totalFP + totalFN),
        precision: overallPrecision,
        recall: overallRecall,
        f1Score: overallF1,
      },
      perCategory,
    };
  }
  
  async evaluateTextGeneration(
    modelName: string,
    testData: Array<{
      input: string;
      reference: string;
    }>,
    metrics: ('bleu' | 'rouge' | 'semantic')[] = ['rouge', 'semantic']
  ): Promise<{
    results: Array<{
      input: string;
      reference: string;
      generated: string;
      scores: Record<string, number>;
    }>;
    averageScores: Record<string, number>;
  }> {
    const results: any[] = [];
    const scoreSums: Record<string, number> = {};
    
    for (const testCase of testData) {
      const response = await this.client.chat.completions.create({
        model: modelName,
        messages: [{ role: 'user', content: testCase.input }],
        temperature: 0.3,
        max_tokens: 500,
      });
      
      const generated = response.choices[0].message.content || '';
      const scores: Record<string, number> = {};
      
      if (metrics.includes('rouge')) {
        scores.rouge = this.calculateRouge(testCase.reference, generated);
      }
      
      if (metrics.includes('semantic')) {
        // Create embeddings and compare
        scores.semanticSimilarity = await this.calculateSemanticSimilarity(
          testCase.reference,
          generated
        );
      }
      
      results.push({
        input: testCase.input,
        reference: testCase.reference,
        generated,
        scores,
      });
      
      for (const [metric, score] of Object.entries(scores)) {
        scoreSums[metric] = (scoreSums[metric] || 0) + score;
      }
    }
    
    const averageScores: Record<string, number> = {};
    for (const [metric, sum] of Object.entries(scoreSums)) {
      averageScores[metric] = sum / results.length;
    }
    
    return { results, averageScores };
  }
  
  private calculateRouge(reference: string, generated: string): number {
    // Simplified ROUGE-L implementation
    const refWords = reference.toLowerCase().split(/\s+/);
    const genWords = generated.toLowerCase().split(/\s+/);
    
    let lcsLength = 0;
    const dp: number[][] = Array(refWords.length + 1)
      .fill(null)
      .map(() => Array(genWords.length + 1).fill(0));
    
    for (let i = 1; i <= refWords.length; i++) {
      for (let j = 1; j <= genWords.length; j++) {
        if (refWords[i - 1] === genWords[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1] + 1;
          lcsLength = Math.max(lcsLength, dp[i][j]);
        }
      }
    }
    
    const precision = lcsLength / genWords.length;
    const recall = lcsLength / refWords.length;
    const f1 = precision + recall > 0 ? 2 * (precision * recall) / (precision + recall) : 0;
    
    return f1;
  }
  
  private async calculateSemanticSimilarity(text1: string, text2: string): Promise<number> {
    const embeddings = await Promise.all([
      this.client.embeddings.create({
        model: 'text-embedding-3-small',
        input: text1,
      }),
      this.client.embeddings.create({
        model: 'text-embedding-3-small',
        input: text2,
      }),
    ]);
    
    const vec1 = embeddings[0].data[0].embedding;
    const vec2 = embeddings[1].data[0].embedding;
    
    // Cosine similarity
    let dot = 0;
    let norm1 = 0;
    let norm2 = 0;
    
    for (let i = 0; i < vec1.length; i++) {
      dot += vec1[i] * vec2[i];
      norm1 += vec1[i] * vec1[i];
      norm2 += vec2[i] * vec2[i];
    }
    
    return dot / (Math.sqrt(norm1) * Math.sqrt(norm2));
  }
}
```

```python
# services/evaluation_service.py - Model evaluation
from openai import OpenAI
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import math

@dataclass
class EvaluationResult:
    overall: Dict[str, float]
    per_category: Dict[str, Dict[str, float]]
    examples: List[Dict[str, Any]]

class EvaluationService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    async def evaluate_classification(
        self,
        model_name: str,
        test_data: List[Dict[str, str]],
        categories: List[str],
    ) -> EvaluationResult:
        """Evaluate classification model."""
        examples = []
        confusion_matrix: Dict[str, Dict[str, int]] = {
            cat: {cat2: 0 for cat2 in categories}
            for cat in categories
        }
        
        for test_case in test_data:
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[{
                    'role': 'user',
                    'content': f"Classify: {test_case['input']}\n\nCategories: {', '.join(categories)}",
                }],
                temperature=0,
                max_tokens=50,
            )
            
            predicted = self._extract_category(
                response.choices[0].message.content or '',
                categories
            )
            expected = test_case['expected_category']
            correct = predicted == expected
            
            examples.append({
                'input': test_case['input'],
                'expected': expected,
                'predicted': predicted,
                'correct': correct,
            })
            
            confusion_matrix[expected][predicted] += 1
        
        overall, per_category = self._calculate_metrics(confusion_matrix, categories)
        
        return EvaluationResult(
            overall=overall,
            per_category=per_category,
            examples=examples,
        )
    
    def _extract_category(self, response: str, categories: List[str]) -> str:
        """Extract category from response."""
        response_lower = response.lower()
        for category in categories:
            if category.lower() in response_lower:
                return category
        return categories[0]
    
    def _calculate_metrics(
        self,
        confusion_matrix: Dict[str, Dict[str, int]],
        categories: List[str],
    ) -> Tuple[Dict[str, float], Dict[str, Dict[str, float]]]:
        """Calculate precision, recall, F1."""
        per_category = {}
        total_tp = total_fp = total_fn = 0
        
        for category in categories:
            row = confusion_matrix[category]
            tp = row.get(category, 0)
            fp = sum(count for cat, count in row.items() if cat != category)
            fn = sum(
                confusion_matrix.get(cat, {}).get(category, 0)
                for cat in categories
                if cat != category
            )
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            
            per_category[category] = {
                'precision': precision,
                'recall': recall,
                'f1': f1,
            }
            
            total_tp += tp
            total_fp += fp
            total_fn += fn
        
        overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
        overall_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
        overall_f1 = 2 * overall_precision * overall_recall / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0
        
        return {
            'accuracy': total_tp / (total_tp + total_fp + total_fn),
            'precision': overall_precision,
            'recall': overall_recall,
            'f1_score': overall_f1,
        }, per_category
```

## Cost Optimization

### Cost Management Strategies

```typescript
// services/costOptimizer.ts - Fine-tuning cost optimization

interface CostEstimate {
  trainingTokens: number;
  trainingCost: number;
  inferenceTokensPerQuery: number;
  monthlyInferenceCost: number;
  totalMonthlyCost: number;
  savingsVsBaseModel: number;
}

export class CostOptimizer {
  // Pricing (per 1M tokens)
  private static readonly TRAINING_PRICES: Record<string, number> = {
    'gpt-4o-mini': 0.003,
    'gpt-3.5-turbo': 0.008,
  };
  
  private static readonly INPUT_PRICES: Record<string, number> = {
    'gpt-4o': 2.5,
    'gpt-4o-mini': 0.15,
    'gpt-3.5-turbo': 0.5,
  };
  
  private static readonly OUTPUT_PRICES: Record<string, number> = {
    'gpt-4o': 10.0,
    'gpt-4o-mini': 0.6,
    'gpt-3.5-turbo': 1.5,
  };
  
  estimateFineTuningCost(
    trainingExamples: number,
    avgTokensPerExample: number,
    nEpochs: number = 4
  ): CostEstimate {
    // Training cost
    const trainingTokens = trainingExamples * avgTokensPerExample * nEpochs;
    const baseModel = 'gpt-4o-mini';
    const trainingCost = (trainingTokens / 1_000_000) * this.TRAINING_PRICES[baseModel];
    
    // Inference cost
    const inferenceTokensPerQuery = avgTokensPerExample; // Rough estimate
    const monthlyQueries = 100_000; // Example volume
    const monthlyInferenceTokens = monthlyQueries * inferenceTokensPerQuery;
    
    const fineTunedInputCost = (monthlyInferenceTokens / 1_000_000) * this.INPUT_PRICES[baseModel];
    const baseModelInputCost = (monthlyInferenceTokens / 1_000_000) * this.INPUT_PRICES['gpt-4o'];
    
    return {
      trainingTokens,
      trainingCost,
      inferenceTokensPerQuery,
      monthlyInferenceCost: fineTunedInputCost,
      totalMonthlyCost: trainingCost + fineTunedInputCost,
      savingsVsBaseModel: baseModelInputCost - fineTunedInputCost,
    };
  }
  
  shouldFineTune(params: {
    monthlyQueryVolume: number;
    avgPromptTokens: number;
    avgCompletionTokens: number;
    nEpochs?: number;
  }): {
    recommended: boolean;
    reason: string;
    estimatedCost: CostEstimate;
    paybackPeriodMonths?: number;
  } {
    const { monthlyQueryVolume, avgPromptTokens, avgCompletionTokens } = params;
    const nEpochs = params.nEpochs || 4;
    
    const baseModel = 'gpt-4o';
    const fineTunedModel = 'gpt-4o-mini';
    
    // Estimate training data needed (rule of thumb: 100-500 examples minimum)
    const estimatedTrainingExamples = 100;
    const avgTokensPerExample = avgPromptTokens + avgCompletionTokens;
    const costEstimate = this.estimateFineTuningCost(
      estimatedTrainingExamples,
      avgTokensPerExample,
      nEpochs
    );
    
    // Compare monthly inference costs
    const baseMonthlyInput = (monthlyQueryVolume * avgPromptTokens / 1_000_000) * this.INPUT_PRICES[baseModel];
    const baseMonthlyOutput = (monthlyQueryVolume * avgCompletionTokens / 1_000_000) * this.OUTPUT_PRICES[baseModel];
    const baseTotal = baseMonthlyInput + baseMonthlyOutput;
    
    const fineTunedMonthlyInput = (monthlyQueryVolume * avgPromptTokens / 1_000_000) * this.INPUT_PRICES[fineTunedModel];
    const fineTunedMonthlyOutput = (monthlyQueryVolume * avgCompletionTokens / 1_000_000) * this.OUTPUT_PRICES[fineTunedModel];
    const fineTunedTotal = fineTunedMonthlyInput + fineTunedMonthlyOutput;
    
    const monthlySavings = baseTotal - fineTunedTotal;
    
    if (monthlySavings > costEstimate.trainingCost) {
      const paybackMonths = Math.ceil(costEstimate.trainingCost / monthlySavings);
      
      return {
        recommended: true,
        reason: `Fine-tuning sẽ tiết kiệm $${monthlySavings.toFixed(2)}/tháng. Hoàn vốn sau ${paybackMonths} tháng.`,
        estimatedCost: costEstimate,
        paybackPeriodMonths: paybackMonths,
      };
    }
    
    return {
      recommended: false,
      reason: `Chi phí fine-tuning ($${costEstimate.trainingCost.toFixed(2)}) cao hơn savings hàng tháng ($${monthlySavings.toFixed(2)}).`,
      estimatedCost: costEstimate,
    };
  }
  
  selectOptimalModel(params: {
    requiredCapabilities: string[];
    latencyRequirement?: number; // ms
    budgetConstraint?: number;
  }): {
    model: string;
    reasons: string[];
    estimatedCostPer1KTokens: number;
  }[] {
    const candidates = [
      {
        model: 'gpt-4o',
        capabilities: ['highest quality', 'largest context', 'vision'],
        latency: 2000,
        cost: 12.5, // Input + Output per 1K tokens
      },
      {
        model: 'gpt-4o-mini',
        capabilities: ['good quality', 'fast', 'cost-effective'],
        latency: 500,
        cost: 0.75,
      },
      {
        model: 'gpt-3.5-turbo',
        capabilities: ['baseline quality', 'very fast', 'cheapest'],
        latency: 300,
        cost: 2.0,
      },
    ];
    
    return candidates
      .filter(c => {
        if (params.latencyRequirement && c.latency > params.latencyRequirement) {
          return false;
        }
        if (params.budgetConstraint && c.cost > params.budgetConstraint) {
          return false;
        }
        return true;
      })
      .map(c => ({
        model: c.model,
        reasons: c.capabilities,
        estimatedCostPer1KTokens: c.cost,
      }));
  }
}
```

## Production Deployment

### Model Deployment Pattern

```typescript
// services/fineTunedModelService.ts - Fine-tuned model deployment
import OpenAI from 'openai';

interface ModelConfig {
  fineTunedModelId: string;
  fallbackModel?: string;
  temperature?: number;
  maxTokens?: number;
  retryAttempts?: number;
}

export class FineTunedModelService {
  private client: OpenAI;
  private config: ModelConfig;
  private fallbackClient: OpenAI | null = null;
  
  constructor(client: OpenAI, config: ModelConfig) {
    this.client = client;
    this.config = config;
    
    if (config.fallbackModel) {
      this.fallbackClient = client; // Same client for fallback
    }
  }
  
  async complete(
    messages: Array<{ role: string; content: string }>,
    options: {
      temperature?: number;
      maxTokens?: number;
      stream?: boolean;
    } = {}
  ): Promise<{
    content: string;
    model: string;
    usage: {
      promptTokens: number;
      completionTokens: number;
      totalTokens: number;
    };
  }> {
    const params = {
      model: this.config.fineTunedModelId,
      messages,
      temperature: options.temperature ?? this.config.temperature ?? 0.7,
      max_tokens: options.maxTokens ?? this.config.maxTokens ?? 1000,
      stream: options.stream ?? false,
    };
    
    let lastError: Error | null = null;
    
    // Try fine-tuned model
    for (let attempt = 0; attempt < (this.config.retryAttempts || 3); attempt++) {
      try {
        const response = await this.client.chat.completions.create(params);
        
        return {
          content: response.choices[0].message.content || '',
          model: response.model,
          usage: {
            promptTokens: response.usage?.prompt_tokens || 0,
            completionTokens: response.usage?.completion_tokens || 0,
            totalTokens: response.usage?.total_tokens || 0,
          },
        };
      } catch (error: any) {
        lastError = error;
        
        // Check if we should fallback
        if (
          this.config.fallbackModel &&
          (error.status === 404 || error.code === 'model_not_found')
        ) {
          break; // Try fallback
        }
        
        // Retry on rate limits or server errors
        if (error.status === 429 || error.status >= 500) {
          const delay = Math.pow(2, attempt) * 1000;
          await new Promise(resolve => setTimeout(resolve, delay));
          continue;
        }
        
        throw error;
      }
    }
    
    // Fallback to base model
    if (this.fallbackClient && this.config.fallbackModel) {
      console.log(`Falling back to model: ${this.config.fallbackModel}`);
      
      const response = await this.fallbackClient.chat.completions.create({
        model: this.config.fallbackModel,
        messages,
        temperature: params.temperature,
        max_tokens: params.max_tokens,
        stream: false,
      });
      
      return {
        content: response.choices[0].message.content || '',
        model: this.config.fallbackModel,
        usage: {
          promptTokens: response.usage?.prompt_tokens || 0,
          completionTokens: response.usage?.completion_tokens || 0,
          totalTokens: response.usage?.total_tokens || 0,
        },
      };
    }
    
    throw lastError || new Error('Failed to complete request');
  }
  
  async *streamComplete(
    messages: Array<{ role: string; content: string }>,
    options: {
      temperature?: number;
      maxTokens?: number;
    } = {}
  ): AsyncGenerator<string, void, unknown> {
    const stream = await this.client.chat.completions.create({
      model: this.config.fineTunedModelId,
      messages,
      temperature: options.temperature ?? this.config.temperature ?? 0.7,
      max_tokens: options.maxTokens ?? this.config.maxTokens ?? 1000,
      stream: true,
    });
    
    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content;
      if (content) {
        yield content;
      }
    }
  }
}

// Model registry for managing multiple fine-tuned models
export class ModelRegistry {
  private models: Map<string, FineTunedModelService> = new Map();
  private client: OpenAI;
  
  constructor(client: OpenAI) {
    this.client = client;
  }
  
  register(
    modelId: string,
    config: {
      temperature?: number;
      maxTokens?: number;
      fallbackModel?: string;
    } = {}
  ): FineTunedModelService {
    const service = new FineTunedModelService(this.client, {
      fineTunedModelId: modelId,
      ...config,
    });
    
    this.models.set(modelId, service);
    return service;
  }
  
  get(modelId: string): FineTunedModelService | undefined {
    return this.models.get(modelId);
  }
  
  list(): string[] {
    return Array.from(this.models.keys());
  }
  
  unregister(modelId: string): void {
    this.models.delete(modelId);
  }
}
```

```python
# services/fine_tuned_model_service.py - Fine-tuned model deployment
from openai import OpenAI
from typing import List, Dict, Any, Optional, AsyncGenerator
import time

class FineTunedModelService:
    def __init__(
        self,
        client: OpenAI,
        fine_tuned_model_id: str,
        fallback_model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        retry_attempts: int = 3,
    ):
        self.client = client
        self.fine_tuned_model_id = fine_tuned_model_id
        self.fallback_model = fallback_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.retry_attempts = retry_attempts
    
    def complete(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Complete a chat completion request."""
        params = {
            'model': self.fine_tuned_model_id,
            'messages': messages,
            'temperature': temperature or self.temperature,
            'max_tokens': max_tokens or self.max_tokens,
            'stream': False,
        }
        
        last_error = None
        
        for attempt in range(self.retry_attempts):
            try:
                response = self.client.chat.completions.create(**params)
                
                return {
                    'content': response.choices[0].message.content or '',
                    'model': response.model,
                    'usage': {
                        'prompt_tokens': response.usage.prompt_tokens if response.usage else 0,
                        'completion_tokens': response.usage.completion_tokens if response.usage else 0,
                        'total_tokens': response.usage.total_tokens if response.usage else 0,
                    },
                }
            except Exception as error:
                last_error = error
                
                # Fallback on model not found
                if hasattr(error, 'status') and error.status == 404:
                    break
                
                # Retry on rate limits or server errors
                if hasattr(error, 'status') and error.status in [429, 500, 502, 503, 504]:
                    delay = 2 ** attempt
                    time.sleep(delay)
                    continue
                
                raise error
        
        # Try fallback model
        if self.fallback_model:
            print(f"Falling back to model: {self.fallback_model}")
            
            response = self.client.chat.completions.create(
                model=self.fallback_model,
                messages=messages,
                temperature=params['temperature'],
                max_tokens=params['max_tokens'],
            )
            
            return {
                'content': response.choices[0].message.content or '',
                'model': self.fallback_model,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens if response.usage else 0,
                    'completion_tokens': response.usage.completion_tokens if response.usage else 0,
                    'total_tokens': response.usage.total_tokens if response.usage else 0,
                },
            }
        
        raise last_error or RuntimeError('Failed to complete request')

class ModelRegistry:
    """Registry for managing multiple fine-tuned models."""
    
    def __init__(self, client: OpenAI):
        self.client = client
        self.models: Dict[str, FineTunedModelService] = {}
    
    def register(
        self,
        model_id: str,
        **config
    ) -> FineTunedModelService:
        """Register a new fine-tuned model."""
        service = FineTunedModelService(
            self.client,
            fine_tuned_model_id=model_id,
            **config
        )
        self.models[model_id] = service
        return service
    
    def get(self, model_id: str) -> Optional[FineTunedModelService]:
        """Get a registered model service."""
        return self.models.get(model_id)
    
    def list_models(self) -> List[str]:
        """List all registered models."""
        return list(self.models.keys())
    
    def unregister(self, model_id: str) -> None:
        """Unregister a model."""
        self.models.pop(model_id, None)
```

## Complete Workflow Example

```typescript
// example/fineTuningWorkflow.ts - Complete fine-tuning workflow
import * as fs from 'fs';
import * as path from 'path';
import OpenAI from 'openai';
import {
  FineTuningService,
} from '../services/fineTuningService';
import { EvaluationService } from '../services/evaluationService';
import { CostOptimizer } from '../services/costOptimizer';
import {
  validateTrainingData,
  convertToJSONL,
  estimateTrainingTokens,
} from '../types/trainingData';

async function main() {
  const client = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY!,
  });
  
  const fineTuningService = new FineTuningService(client);
  const evaluationService = new EvaluationService(client);
  const costOptimizer = new CostOptimizer();
  
  // Step 1: Prepare training data
  console.log('Step 1: Preparing training data...');
  
  const trainingData = [
    {
      messages: [
        { role: 'system', content: 'Bạn là một trợ lý phân tích tài chính chuyên nghiệp.' },
        { role: 'user', content: 'Phân tích rủi ro của dự án A' },
        { role: 'assistant', content: 'Dự án A có các rủi ro chính:\n\n1. Rủi ro thị trường: Thị trường mục tiêu đang bão hòa.\n2. Rủi ro tài chính: Vốn đầu tư ban đầu cao hơn dự kiến 20%.\n3. Rủi ro nhân sự: Thiếu nhân sự có kỹ năng chuyên môn.\n4. Rủi ro vận hành: Quy trình sản xuất chưa được tối ưu.' },
      ],
    },
    // ... more examples
  ];
  
  // Validate data
  const validation = validateTrainingData(trainingData);
  if (!validation.valid) {
    console.error('Validation errors:', validation.errors);
    return;
  }
  
  if (validation.warnings.length > 0) {
    console.warn('Warnings:', validation.warnings);
  }
  
  // Step 2: Cost analysis
  console.log('\nStep 2: Analyzing costs...');
  
  const costAnalysis = costOptimizer.shouldFineTune({
    monthlyQueryVolume: 50000,
    avgPromptTokens: 100,
    avgCompletionTokens: 200,
  });
  
  console.log(`Recommendation: ${costAnalysis.reason}`);
  
  if (!costAnalysis.recommended) {
    console.log('Fine-tuning may not be cost-effective. Proceed anyway? (y/n)');
    // In production, handle this properly
  }
  
  // Step 3: Upload training file
  console.log('\nStep 3: Uploading training file...');
  
  const jsonlContent = convertToJSONL(trainingData);
  const tempFile = path.join(__dirname, 'training_data.jsonl');
  fs.writeFileSync(tempFile, jsonlContent);
  
  const { fileId, bytes } = await fineTuningService.uploadTrainingFile(tempFile);
  console.log(`Uploaded: ${fileId} (${bytes} bytes)`);
  
  // Step 4: Create fine-tuning job
  console.log('\nStep 4: Creating fine-tuning job...');
  
  const jobId = await fineTuningService.createFineTuningJob({
    model: 'gpt-4o-mini',
    trainingFile: fileId,
    nEpochs: 4,
    batchSize: 'auto',
    learningRateMultiplier: 'auto',
  });
  
  console.log(`Job created: ${jobId}`);
  
  // Step 5: Monitor training
  console.log('\nStep 5: Monitoring training...');
  
  try {
    const finalStatus = await fineTuningService.waitForCompletion(jobId, (status) => {
      console.log(`Status: ${status.status}`);
    });
    
    console.log(`Training complete!`);
    console.log(`Fine-tuned model: ${finalStatus.fineTunedModel}`);
    
    // Step 6: Evaluate model
    console.log('\nStep 6: Evaluating model...');
    
    const testData = [
      { input: 'Đánh giá rủi ro dự án B', expectedCategory: 'risk_analysis' },
      { input: 'Tính ROI cho dự án C', expectedCategory: 'roi_calculation' },
    ];
    
    const evalResult = await evaluationService.evaluateClassification(
      finalStatus.fineTunedModel!,
      testData,
      ['risk_analysis', 'roi_calculation', 'general']
    );
    
    console.log('Evaluation results:');
    console.log(`Accuracy: ${evalResult.overall.accuracy}`);
    console.log(`F1 Score: ${evalResult.overall.f1Score}`);
    
  } catch (error) {
    console.error('Training failed:', error);
  } finally {
    // Cleanup
    fs.unlinkSync(tempFile);
  }
}

// Run the workflow
main().catch(console.error);
```

## References

### Official Documentation

- [Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [Fine-tuning API](https://platform.openai.com/docs/api-reference/fine-tuning)
- [Fine-tuning Examples](https://platform.openai.com/docs/guides/fine-tuning-examples)
- [Fine-tuning Best Practices](https://help.openai.com/en/articles/1794429-fine-tuning-best-practices)

### Pricing Information

- [Fine-tuning Pricing](https://openai.com/pricing)
- [Cost Calculator](https://platform.openai.com/finetuning)

### Additional Resources

- [OpenAI Fine-tuning Cookbook](https://github.com/openai/openai-cookbook/tree/main/examples/chat_finetuning)
- [Evaluation Metrics Guide](https://docs.cohere.com/docs/experiments)
- [MLflow for Model Tracking](https://mlflow.org/)

---

**Tài liệu này là một phần của Cursor Enterprise Framework Generator.**
