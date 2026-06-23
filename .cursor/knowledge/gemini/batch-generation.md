---
title: "Batch Generation - Batch Prediction API và Async Processing"
description: "Hướng dẫn toàn diện về Batch Prediction API trong Gemini API, bao gồm cách xử lý batch large datasets, async batch jobs, cost optimization, và production patterns"
tags:
  - "gemini"
  - "batch-processing"
  - "batch-prediction"
  - "async-jobs"
  - "cost-optimization"
  - "large-scale"
  - "batch-api"
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Batch Generation - Batch Prediction API và Async Processing

## Tổng Quan (Overview)

Batch processing là một tính năng quan trọng cho các ứng dụng enterprise cần xử lý số lượng lớn requests một cách hiệu quả về chi phí. Gemini Batch Prediction API cho phép developers gửi hàng nghìn hoặc hàng triệu requests trong một batch job, với chi phí được tối ưu hóa đáng kể so với việc gọi API đơn lẻ.

Việc sử dụng Batch API mang lại nhiều lợi ích:

- **Tiết kiệm chi phí**: Batch processing có discount đáng kể (lên đến 50%) so với synchronous API calls
- **Tăng throughput**: Xử lý hàng nghìn requests mà không cần quản lý rate limiting
- **Tự động hóa**: Setup once, run many times - lý tưởng cho recurring tasks
- **Resource efficiency**: Giảm overhead từ multiple HTTP connections

Tuy nhiên, batch processing cũng đi kèm với những thách thức riêng: latency cao hơn, cần xử lý errors khác nhau, và cần design patterns phù hợp để tích hợp vào existing systems.

Trong tài liệu này, chúng ta sẽ khám phá chi tiết về Batch API, cách setup và manage batch jobs, strategies cho cost optimization, và các production patterns để xử lý large-scale batch processing.

## Mục Đích (Purpose)

**1. Hiểu Rõ Batch API Architecture**

Cung cấp kiến thức chi tiết về cách Batch Prediction API hoạt động, including input/output formats, job lifecycle, và cách results được structured. Hiểu rõ architecture giúp developers design solutions hiệu quả.

**2. Nắm Vững Batch Job Management**

Hướng dẫn chi tiết cách create, monitor, cancel, và manage batch jobs trong production. Bao gồm cách xử lý partial failures và retries.

**3. Xây Dựng Scalable Batch Processing Systems**

Cung cấp patterns và architectures cho việc xây dựng các hệ thống batch processing có thể scale từ hàng trăm đến hàng triệu records, với error handling và monitoring đầy đủ.

## Các Khái Niệm Cốt Lõi (Key Concepts)

### 1. Batch API Overview

Gemini Batch Prediction API cho phép bạn submit một batch của prompts và nhận kết quả về sau. Điều nghĩa là:

- **Asynchronous**: Bạn submit job và nhận job ID, sau đó poll hoặc receive callback khi hoàn thành
- **Bulk processing**: Tối ưu cho việc xử lý many prompts cùng một lúc
- **Cost effective**: Significant discount so với real-time API
- **Large scale**: Có thể xử lý hàng triệu records trong một job

```python
# Batch API Concepts (Python)

# Batch Job Lifecycle:
# 1. CREATE: Submit batch job với input data
# 2. PENDING: Job đang được queued
# 3. RUNNING: Job đang được process
# 4. SUCCEEDED: Job hoàn thành, results có sẵn
# 5. FAILED: Job thất bại (có thể retry)
# 6. CANCELLED: Job bị cancelled

# Input Format:
# JSONL format (JSON Lines)
# Mỗi dòng là một JSON object với prompt hoặc cấu hình

# Output Format:
# JSONL format
# Mỗi dòng chứa kết quả tương ứng với input
```

```typescript
// Batch API Concepts (TypeScript)

// Batch Job States
type BatchJobState = 
  | 'JOB_STATE_PENDING'
  | 'JOB_STATE_RUNNING'
  | 'JOB_STATE_SUCCEEDED'
  | 'JOB_STATE_FAILED'
  | 'JOB_STATE_CANCELLED'
  | 'JOB_STATE_CANCELLING';

// Input record format
interface BatchInputRecord {
  prompt: string;
  // Optional: custom ID để match input với output
  clientInfo?: {
    [key: string]: string;
  };
}

// Output record format  
interface BatchOutputRecord {
  // Matched với input
  clientInfo?: { [key: string]: string };
  
  // Response
  content: string;
  
  // Safety info
  safetyRatings?: SafetyRating[];
  
  // Error info (nếu failed)
  error?: {
    code: string;
    message: string;
  };
}
```

### 2. Input/Output Format Specification

```python
# src/batch/formats.py
"""
Batch Input/Output Format Handlers
"""

from typing import List, Dict, Any, Optional, Iterator
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import json
import gzip


@dataclass
class BatchInputRecord:
    """Một record trong batch input."""
    prompt: str
    client_info: Optional[Dict[str, Any]] = None
    generation_config: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert thành dictionary cho JSONL."""
        result = {
            "prompt": self.prompt,
        }
        
        if self.client_info:
            result["client_info"] = self.client_info
        
        if self.generation_config:
            result["generation_config"] = self.generation_config
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchInputRecord":
        """Create từ dictionary."""
        return cls(
            prompt=data["prompt"],
            client_info=data.get("client_info"),
            generation_config=data.get("generation_config"),
        )


@dataclass
class BatchOutputRecord:
    """Một record trong batch output."""
    content: str
    client_info: Optional[Dict[str, Any]] = None
    safety_ratings: Optional[List[Dict[str, Any]]] = None
    error: Optional[Dict[str, str]] = None
    finish_reason: Optional[str] = None
    
    @property
    def is_error(self) -> bool:
        """Check nếu record có error."""
        return self.error is not None
    
    @property
    def is_blocked(self) -> bool:
        """Check nếu content bị blocked."""
        if not self.safety_ratings:
            return False
        
        for rating in self.safety_ratings:
            prob = rating.get("probability", "")
            if prob in ["HIGH", "CRITICAL"]:
                return True
        
        return False
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchOutputRecord":
        """Create từ dictionary."""
        return cls(
            content=data.get("content", ""),
            client_info=data.get("client_info"),
            safety_ratings=data.get("safety_ratings"),
            error=data.get("error"),
            finish_reason=data.get("finish_reason"),
        )


class BatchFileHandler:
    """
    Handler để create và parse batch files.
    """
    
    @staticmethod
    def write_input_file(
        records: List[BatchInputRecord],
        output_path: str,
        compress: bool = False
    ) -> None:
        """
        Write batch input file.
        
        Args:
            records: List of input records
            output_path: Path to output file
            compress: Compress với gzip không
        """
        mode = 'wt'
        if compress:
            output_path += '.gz'
            mode = 'wb'
        
        if compress:
            with gzip.open(output_path, mode) as f:
                for record in records:
                    line = json.dumps(record.to_dict()) + '\n'
                    f.write(line.encode('utf-8'))
        else:
            with open(output_path, mode, encoding='utf-8') as f:
                for record in records:
                    f.write(json.dumps(record.to_dict(), ensure_ascii=False) + '\n')
    
    @staticmethod
    def read_output_file(
        input_path: str,
        decompress: bool = False
    ) -> Iterator[BatchOutputRecord]:
        """
        Read batch output file.
        
        Yields:
            BatchOutputRecord objects
        """
        if decompress or input_path.endswith('.gz'):
            with gzip.open(input_path, 'rt', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        yield BatchOutputRecord.from_dict(data)
        else:
            with open(input_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        yield BatchOutputRecord.from_dict(data)
    
    @staticmethod
    def read_input_file(
        input_path: str,
        decompress: bool = False
    ) -> Iterator[BatchInputRecord]:
        """
        Read batch input file (để verify hoặc reprocess).
        
        Yields:
            BatchInputRecord objects
        """
        if decompress or input_path.endswith('.gz'):
            with gzip.open(input_path, 'rt', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        yield BatchInputRecord.from_dict(data)
        else:
            with open(input_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        yield BatchInputRecord.from_dict(data)
```

```typescript
// src/batch/formats.ts
/**
 * Batch Input/Output Format Handlers (TypeScript)
 */

import { writeFileSync, readFileSync, createReadStream, createWriteStream } from 'fs';
import { createGzip, createGunzip } from 'zlib';
import { pipeline } from 'stream';
import { promisify } from 'util';

const pipelineAsync = promisify(pipeline);

// Types
export interface BatchInputRecord {
  prompt: string;
  clientInfo?: Record<string, string>;
  generationConfig?: Record<string, any>;
}

export interface BatchOutputRecord {
  content?: string;
  clientInfo?: Record<string, string>;
  safetyRatings?: SafetyRating[];
  error?: {
    code: string;
    message: string;
  };
  finishReason?: string;
}

export interface SafetyRating {
  category: string;
  probability: string;
}

export class BatchFileHandler {
  /**
   * Write batch input file
   */
  static async writeInputFile(
    records: BatchInputRecord[],
    outputPath: string,
    compress: boolean = false
  ): Promise<void> {
    const lines = records.map(r => JSON.stringify(r)).join('\n') + '\n';
    
    if (compress) {
      const gzip = createGzip();
      const output = createWriteStream(outputPath + '.gz');
      await pipelineAsync(
        Buffer.from(lines, 'utf-8'),
        gzip,
        output
      );
    } else {
      writeFileSync(outputPath, lines, 'utf-8');
    }
  }
  
  /**
   * Read batch output file
   */
  static async *readOutputFile(
    inputPath: string,
    decompress: boolean = false
  ): AsyncGenerator<BatchOutputRecord> {
    const isCompressed = decompress || inputPath.endsWith('.gz');
    
    if (isCompressed) {
      const gunzip = createGunzip();
      const input = createReadStream(inputPath.endsWith('.gz') ? inputPath : inputPath + '.gz');
      
      let buffer = '';
      for await (const chunk of input.pipe(gunzip)) {
        buffer += chunk.toString();
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';
        
        for (const line of lines) {
          if (line.trim()) {
            yield JSON.parse(line) as BatchOutputRecord;
          }
        }
      }
      
      if (buffer.trim()) {
        yield JSON.parse(buffer) as BatchOutputRecord;
      }
    } else {
      const content = readFileSync(inputPath, 'utf-8');
      const lines = content.split('\n');
      
      for (const line of lines) {
        if (line.trim()) {
          yield JSON.parse(line) as BatchOutputRecord;
        }
      }
    }
  }
  
  /**
   * Read batch input file
   */
  static async *readInputFile(
    inputPath: string,
    decompress: boolean = false
  ): AsyncGenerator<BatchInputRecord> {
    const isCompressed = decompress || inputPath.endsWith('.gz');
    
    if (isCompressed) {
      const gunzip = createGunzip();
      const input = createReadStream(inputPath.endsWith('.gz') ? inputPath : inputPath + '.gz');
      
      let buffer = '';
      for await (const chunk of input.pipe(gunzip)) {
        buffer += chunk.toString();
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';
        
        for (const line of lines) {
          if (line.trim()) {
            yield JSON.parse(line) as BatchInputRecord;
          }
        }
      }
    } else {
      const content = readFileSync(inputPath, 'utf-8');
      const lines = content.split('\n');
      
      for (const line of lines) {
        if (line.trim()) {
          yield JSON.parse(line) as BatchInputRecord;
        }
      }
    }
  }
}
```

### 3. Batch Job Management

```python
# src/batch/job_manager.py
"""
Batch Job Manager - Create, monitor, và manage batch jobs
"""

from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import time
import logging

logger = logging.getLogger(__name__)


class BatchJobState(Enum):
    """Batch job states."""
    PENDING = "JOB_STATE_PENDING"
    RUNNING = "JOB_STATE_RUNNING"
    SUCCEEDED = "JOB_STATE_SUCCEEDED"
    FAILED = "JOB_STATE_FAILED"
    CANCELLED = "JOB_STATE_CANCELLED"
    CANCELLING = "JOB_STATE_CANCELLING"


@dataclass
class BatchJobInfo:
    """Thông tin về một batch job."""
    name: str
    display_name: str
    state: BatchJobState
    create_time: str
    update_time: str
    model: str
    input_config: Dict[str, Any]
    output_config: Dict[str, Any]
    
    # Progress info (khi running)
    completed_attempt_count: int = 0
    attempt_count: int = 1
    
    # Error info (khi failed)
    error_message: Optional[str] = None
    
    @property
    def is_terminal(self) -> bool:
        """Check nếu job ở terminal state."""
        return self.state in [
            BatchJobState.SUCCEEDED,
            BatchJobState.FAILED,
            BatchJobState.CANCELLED,
        ]
    
    @property
    def is_successful(self) -> bool:
        """Check nếu job thành công."""
        return self.state == BatchJobState.SUCCEEDED
    
    @property
    def progress_percent(self) -> float:
        """Estimate progress percentage."""
        if self.attempt_count == 0:
            return 0.0
        
        return (self.completed_attempt_count / self.attempt_count) * 100


@dataclass
class BatchJobConfig:
    """Cấu hình cho batch job."""
    model: str = "gemini-2.0-flash"
    display_name: Optional[str] = None
    batch_size: int = 1000  # Records per batch
    output_prefix: Optional[str] = None
    
    # Generation config
    temperature: Optional[float] = None
    max_output_tokens: Optional[int] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    
    # Retry config
    max_retries: int = 3
    retry_delay_seconds: int = 60
    
    # Priority
    priority: int = 0  # Higher = more important


class BatchJobManager:
    """
    Manager để create và manage batch jobs.
    """
    
    def __init__(self, vertex_client=None):
        """
        Initialize manager.
        
        Args:
            vertex_client: Vertex AI client (None for AI Studio)
        """
        self.client = vertex_client
    
    def create_job(
        self,
        input_path: str,
        output_path: str,
        config: BatchJobConfig,
        project_id: Optional[str] = None,
        location: str = "us-central1"
    ) -> str:
        """
        Create a batch prediction job.
        
        Args:
            input_path: GCS path to input JSONL file
            output_path: GCS path for output
            config: Job configuration
            project_id: GCP project ID
            location: GCP location
            
        Returns:
            Job resource name
        """
        # Build job config
        job_request = {
            "display_name": config.display_name or f"batch-job-{int(time.time())}",
            "model": f"projects/{project_id}/locations/{location}/models/{config.model}",
            "input_config": {
                "instances_format": "jsonl",
                "gcs_source": {"uris": [input_path]},
            },
            "output_config": {
                "predictions_format": "jsonl",
                "gcs_destination": {"uri": output_path},
            },
            "dedicated_resources": {
                "machine_type": "n1-standard-4",
                "starting_replica_count": 4,
                "max_replica_count": 10,
            },
        }
        
        # Add generation config if specified
        generation_config = {}
        if config.temperature is not None:
            generation_config["temperature"] = config.temperature
        if config.max_output_tokens is not None:
            generation_config["max_tokens"] = config.max_output_tokens
        if config.top_p is not None:
            generation_config["topP"] = config.top_p
        if config.top_k is not None:
            generation_config["topK"] = config.top_k
        
        if generation_config:
            job_request["generation_config"] = generation_config
        
        # Create job
        if self.client:
            # Vertex AI
            job = self.client.batch_prediction_job.create(job_request)
            return job.resource_name
        else:
            # AI Studio (simplified)
            raise NotImplementedError("AI Studio batch API not implemented in this example")
    
    def get_job(self, job_name: str) -> BatchJobInfo:
        """
        Get job info.
        
        Args:
            job_name: Full job resource name
            
        Returns:
            BatchJobInfo object
        """
        if self.client:
            job = self.client.batch_prediction_job.get(job_name)
            
            return BatchJobInfo(
                name=job.name,
                display_name=job.display_name,
                state=BatchJobState(job.state),
                create_time=job.create_time,
                update_time=job.update_time,
                model=job.model,
                input_config=job.input_config,
                output_config=job.output_config,
                completed_attempt_count=job.completed_attempt_count,
                attempt_count=job.attempt_count,
                error_message=job.error.message if job.error else None,
            )
        else:
            raise NotImplementedError("AI Studio batch API not implemented")
    
    def cancel_job(self, job_name: str) -> None:
        """Cancel a running job."""
        if self.client:
            self.client.batch_prediction_job.cancel(job_name)
        else:
            raise NotImplementedError("AI Studio batch API not implemented")
    
    def delete_job(self, job_name: str) -> None:
        """Delete a job."""
        if self.client:
            self.client.batch_prediction_job.delete(job_name)
        else:
            raise NotImplementedError("AI Studio batch API not implemented")
    
    def wait_for_job(
        self,
        job_name: str,
        poll_interval_seconds: int = 30,
        timeout_seconds: Optional[int] = None,
        progress_callback: Optional[Callable[[BatchJobInfo], None]] = None
    ) -> BatchJobInfo:
        """
        Wait for job to complete.
        
        Args:
            job_name: Job resource name
            poll_interval_seconds: Seconds between status checks
            timeout_seconds: Max seconds to wait (None = no timeout)
            progress_callback: Called with job info on each poll
            
        Returns:
            Final BatchJobInfo
        """
        start_time = time.time()
        
        while True:
            job_info = self.get_job(job_name)
            
            # Call progress callback
            if progress_callback:
                progress_callback(job_info)
            
            # Check if terminal state
            if job_info.is_terminal:
                return job_info
            
            # Check timeout
            if timeout_seconds and (time.time() - start_time) > timeout_seconds:
                raise TimeoutError(f"Job did not complete within {timeout_seconds} seconds")
            
            # Wait before next poll
            time.sleep(poll_interval_seconds)
    
    def list_jobs(
        self,
        project_id: str,
        location: str = "us-central1",
        filter_str: Optional[str] = None,
        page_size: int = 100
    ) -> List[BatchJobInfo]:
        """List batch jobs."""
        if self.client:
            jobs = self.client.batch_prediction_job.list(
                f"projects/{project_id}/locations/{location}",
                filter=filter_str,
                page_size=page_size,
            )
            
            return [
                BatchJobInfo(
                    name=job.name,
                    display_name=job.display_name,
                    state=BatchJobState(job.state),
                    create_time=job.create_time,
                    update_time=job.update_time,
                    model=job.model,
                    input_config=job.input_config,
                    output_config=job.output_config,
                    error_message=job.error.message if job.error else None,
                )
                for job in jobs
            ]
        else:
            raise NotImplementedError("AI Studio batch API not implemented")
```

```typescript
// src/batch/job-manager.ts
/**
 * Batch Job Manager (TypeScript)
 */

import { CloudLifeCycle } from '@google-cloud/aiplatform';

// Types
export enum BatchJobState {
  JOB_STATE_PENDING = 'JOB_STATE_PENDING',
  JOB_STATE_RUNNING = 'JOB_STATE_RUNNING',
  JOB_STATE_SUCCEEDED = 'JOB_STATE_SUCCEEDED',
  JOB_STATE_FAILED = 'JOB_STATE_FAILED',
  JOB_STATE_CANCELLED = 'JOB_STATE_CANCELLED',
  JOB_STATE_CANCELLING = 'JOB_STATE_CANCELLING',
}

export interface BatchJobInfo {
  name: string;
  displayName: string;
  state: BatchJobState;
  createTime: string;
  updateTime: string;
  model: string;
  inputConfig: Record<string, any>;
  outputConfig: Record<string, any>;
  completedAttemptCount: number;
  attemptCount: number;
  errorMessage?: string;
}

export interface BatchJobConfig {
  model?: string;
  displayName?: string;
  batchSize?: number;
  temperature?: number;
  maxOutputTokens?: number;
  topP?: number;
  topK?: number;
  maxRetries?: number;
  retryDelaySeconds?: number;
  priority?: number;
}

export class BatchJobManager {
  private projectId: string;
  private location: string;
  private endpoint: string;
  
  constructor(projectId: string, location: string = 'us-central1') {
    this.projectId = projectId;
    this.location = location;
    this.endpoint = `https://${location}-aiplatform.googleapis.com/v1`;
  }
  
  /**
   * Create a batch prediction job
   */
  async createJob(
    inputPath: string,
    outputPath: string,
    config: BatchJobConfig = {}
  ): Promise<string> {
    const displayName = config.displayName || `batch-job-${Date.now()}`;
    
    const jobRequest = {
      displayName,
      model: `projects/${this.projectId}/locations/${this.location}/models/${config.model || 'gemini-2.0-flash'}`,
      inputConfig: {
        instancesFormat: 'jsonl',
        gcsSource: {
          uris: [inputPath],
        },
      },
      outputConfig: {
        predictionsFormat: 'jsonl',
        gcsDestination: {
          uri: outputPath,
        },
      },
      dedicatedResources: {
        machineType: 'n1-standard-4',
        startingReplicaCount: 4,
        maxReplicaCount: 10,
      },
    };
    
    // Add generation config if specified
    const generationConfig: Record<string, any> = {};
    if (config.temperature !== undefined) {
      generationConfig.temperature = config.temperature;
    }
    if (config.maxOutputTokens !== undefined) {
      generationConfig.maxTokens = config.maxOutputTokens;
    }
    if (config.topP !== undefined) {
      generationConfig.topP = config.topP;
    }
    if (config.topK !== undefined) {
      generationConfig.topK = config.topK;
    }
    
    if (Object.keys(generationConfig).length > 0) {
      (jobRequest as any).generationConfig = generationConfig;
    }
    
    // Make API call
    const response = await fetch(`${this.endpoint}/batchPredictionJobs`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${await this.getAccessToken()}`,
      },
      body: JSON.stringify(jobRequest),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to create batch job: ${response.statusText}`);
    }
    
    const result = await response.json();
    return result.name;
  }
  
  /**
   * Get job info
   */
  async getJob(jobName: string): Promise<BatchJobInfo> {
    const response = await fetch(`${this.endpoint}/${jobName}`, {
      headers: {
        'Authorization': `Bearer ${await this.getAccessToken()}`,
      },
    });
    
    if (!response.ok) {
      throw new Error(`Failed to get job: ${response.statusText}`);
    }
    
    const job = await response.json();
    
    return {
      name: job.name,
      displayName: job.displayName,
      state: job.state as BatchJobState,
      createTime: job.createTime,
      updateTime: job.updateTime,
      model: job.model,
      inputConfig: job.inputConfig,
      outputConfig: job.outputConfig,
      completedAttemptCount: job.completedAttemptCount || 0,
      attemptCount: job.attemptCount || 1,
      errorMessage: job.error?.message,
    };
  }
  
  /**
   * Cancel a job
   */
  async cancelJob(jobName: string): Promise<void> {
    const response = await fetch(`${this.endpoint}/${jobName}:cancel`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${await this.getAccessToken()}`,
      },
    });
    
    if (!response.ok) {
      throw new Error(`Failed to cancel job: ${response.statusText}`);
    }
  }
  
  /**
   * Delete a job
   */
  async deleteJob(jobName: string): Promise<void> {
    const response = await fetch(`${this.endpoint}/${jobName}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${await this.getAccessToken()}`,
      },
    });
    
    if (!response.ok) {
      throw new Error(`Failed to delete job: ${response.statusText}`);
    }
  }
  
  /**
   * Wait for job to complete
   */
  async waitForJob(
    jobName: string,
    options: {
      pollIntervalSeconds?: number;
      timeoutSeconds?: number;
      onProgress?: (info: BatchJobInfo) => void;
    } = {}
  ): Promise<BatchJobInfo> {
    const {
      pollIntervalSeconds = 30,
      timeoutSeconds,
      onProgress,
    } = options;
    
    const startTime = Date.now();
    
    while (true) {
      const jobInfo = await this.getJob(jobName);
      
      // Call progress callback
      if (onProgress) {
        onProgress(jobInfo);
      }
      
      // Check if terminal state
      if (this.isTerminalState(jobInfo.state)) {
        return jobInfo;
      }
      
      // Check timeout
      if (timeoutSeconds && (Date.now() - startTime) / 1000 > timeoutSeconds) {
        throw new Error(`Job did not complete within ${timeoutSeconds} seconds`);
      }
      
      // Wait before next poll
      await this.sleep(pollIntervalSeconds * 1000);
    }
  }
  
  /**
   * List batch jobs
   */
  async listJobs(filter?: string): Promise<BatchJobInfo[]> {
    const parent = `projects/${this.projectId}/locations/${this.location}`;
    const url = new URL(`${this.endpoint}/${parent}/batchPredictionJobs`);
    
    if (filter) {
      url.searchParams.set('filter', filter);
    }
    
    const response = await fetch(url.toString(), {
      headers: {
        'Authorization': `Bearer ${await this.getAccessToken()}`,
      },
    });
    
    if (!response.ok) {
      throw new Error(`Failed to list jobs: ${response.statusText}`);
    }
    
    const result = await response.json();
    const jobs = result.batchPredictionJobs || [];
    
    return jobs.map((job: any) => ({
      name: job.name,
      displayName: job.displayName,
      state: job.state as BatchJobState,
      createTime: job.createTime,
      updateTime: job.updateTime,
      model: job.model,
      inputConfig: job.inputConfig,
      outputConfig: job.outputConfig,
      errorMessage: job.error?.message,
    }));
  }
  
  private isTerminalState(state: BatchJobState): boolean {
    return [
      BatchJobState.JOB_STATE_SUCCEEDED,
      BatchJobState.JOB_STATE_FAILED,
      BatchJobState.JOB_STATE_CANCELLED,
    ].includes(state);
  }
  
  private async getAccessToken(): Promise<string> {
    // Use Application Default Credentials
    const { GoogleAuth } = require('google-auth-library');
    const auth = new GoogleAuth();
    const client = await auth.getClient();
    const tokenResponse = await client.getAccessToken();
    return tokenResponse.token || '';
  }
  
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

## Best Practices

### 1. Batch Input Preparation

```python
# src/batch/input_preparation.py
"""
Batch Input Preparation Utilities
"""

from typing import List, Iterator, Dict, Any, Optional, Callable
from dataclasses import dataclass
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class BatchPreparationConfig:
    """Cấu hình cho batch preparation."""
    max_records_per_file: int = 100000
    compress: bool = True
    add_client_info: bool = True
    chunk_size: int = 10000  # Records per chunk for processing
    
    # Validation
    validate_prompts: bool = True
    max_prompt_length: int = 32000
    
    # Transformation
    preprocess_prompt: Optional[Callable[[str], str]] = None
    add_system_prompt: Optional[str] = None


class BatchInputPreparator:
    """
    Preparator để prepare batch inputs từ various sources.
    """
    
    def __init__(self, config: BatchPreparationConfig = None):
        self.config = config or BatchPreparationConfig()
    
    def prepare_from_csv(
        self,
        input_path: str,
        prompt_column: str,
        output_dir: str,
        additional_columns: Optional[List[str]] = None,
        id_column: Optional[str] = None
    ) -> List[str]:
        """
        Prepare batch inputs từ CSV file.
        
        Args:
            input_path: Path to input CSV
            prompt_column: Column chứa prompts
            output_dir: Directory cho output files
            additional_columns: Additional columns để include trong client_info
            id_column: Column dùng làm ID
            
        Returns:
            List of output file paths
        """
        import pandas as pd
        
        # Read CSV
        df = pd.read_csv(input_path)
        
        output_paths = []
        current_records = []
        file_index = 0
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        for idx, row in df.iterrows():
            # Get prompt
            prompt = str(row[prompt_column])
            
            # Validate
            if self.config.validate_prompts:
                validation_error = self._validate_prompt(prompt)
                if validation_error:
                    logger.warning(f"Row {idx}: {validation_error}")
                    continue
            
            # Preprocess
            if self.config.preprocess_prompt:
                prompt = self.config.preprocess_prompt(prompt)
            
            # Add system prompt
            if self.config.add_system_prompt:
                prompt = f"{self.config.add_system_prompt}\n\n{prompt}"
            
            # Build record
            record = {"prompt": prompt}
            
            # Add client info
            if self.config.add_client_info:
                client_info = {}
                
                if id_column and id_column in row:
                    client_info["id"] = str(row[id_column])
                
                client_info["row_index"] = str(idx)
                
                if additional_columns:
                    for col in additional_columns:
                        if col in row:
                            client_info[col] = str(row[col])
                
                record["client_info"] = client_info
            
            current_records.append(record)
            
            # Check if we need to write current batch
            if len(current_records) >= self.config.max_records_per_file:
                output_path = self._write_batch(
                    current_records,
                    output_dir,
                    file_index
                )
                output_paths.append(output_path)
                file_index += 1
                current_records = []
        
        # Write remaining records
        if current_records:
            output_path = self._write_batch(
                current_records,
                output_dir,
                file_index
            )
            output_paths.append(output_path)
        
        return output_paths
    
    def prepare_from_jsonl(
        self,
        input_path: str,
        prompt_field: str,
        output_dir: str,
        id_field: Optional[str] = None
    ) -> List[str]:
        """
        Prepare batch inputs từ JSONL file.
        """
        output_paths = []
        current_records = []
        file_index = 0
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f):
                if not line.strip():
                    continue
                
                data = json.loads(line)
                prompt = str(data.get(prompt_field, ""))
                
                # Validate
                if self.config.validate_prompts:
                    validation_error = self._validate_prompt(prompt)
                    if validation_error:
                        logger.warning(f"Line {idx}: {validation_error}")
                        continue
                
                # Preprocess
                if self.config.preprocess_prompt:
                    prompt = self.config.preprocess_prompt(prompt)
                
                # Build record
                record = {"prompt": prompt}
                
                if self.config.add_client_info:
                    client_info = {"row_index": str(idx)}
                    
                    if id_field and id_field in data:
                        client_info["id"] = str(data[id_field])
                    
                    record["client_info"] = client_info
                
                current_records.append(record)
                
                if len(current_records) >= self.config.max_records_per_file:
                    output_path = self._write_batch(
                        current_records,
                        output_dir,
                        file_index
                    )
                    output_paths.append(output_path)
                    file_index += 1
                    current_records = []
        
        if current_records:
            output_path = self._write_batch(
                current_records,
                output_dir,
                file_index
            )
            output_paths.append(output_path)
        
        return output_paths
    
    def prepare_from_iterator(
        self,
        records: Iterator[Dict[str, Any]],
        prompt_field: str,
        output_dir: str,
        id_field: Optional[str] = None
    ) -> List[str]:
        """
        Prepare batch inputs từ iterator (e.g., database cursor).
        """
        output_paths = []
        current_records = []
        file_index = 0
        record_index = 0
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        for data in records:
            prompt = str(data.get(prompt_field, ""))
            
            if self.config.validate_prompts:
                validation_error = self._validate_prompt(prompt)
                if validation_error:
                    logger.warning(f"Record {record_index}: {validation_error}")
                    record_index += 1
                    continue
            
            if self.config.preprocess_prompt:
                prompt = self.config.preprocess_prompt(prompt)
            
            record = {"prompt": prompt}
            
            if self.config.add_client_info:
                client_info = {"row_index": str(record_index)}
                
                if id_field and id_field in data:
                    client_info["id"] = str(data[id_field])
                
                record["client_info"] = client_info
            
            current_records.append(record)
            record_index += 1
            
            if len(current_records) >= self.config.max_records_per_file:
                output_path = self._write_batch(
                    current_records,
                    output_dir,
                    file_index
                )
                output_paths.append(output_path)
                file_index += 1
                current_records = []
        
        if current_records:
            output_path = self._write_batch(
                current_records,
                output_dir,
                file_index
            )
            output_paths.append(output_path)
        
        return output_paths
    
    def _validate_prompt(self, prompt: str) -> Optional[str]:
        """Validate a prompt."""
        if not prompt or not prompt.strip():
            return "Empty prompt"
        
        if len(prompt) > self.config.max_prompt_length:
            return f"Prompt too long ({len(prompt)} > {self.config.max_prompt_length})"
        
        return None
    
    def _write_batch(
        self,
        records: List[Dict[str, Any]],
        output_dir: str,
        file_index: int
    ) -> str:
        """Write a batch to file."""
        from .formats import BatchFileHandler
        
        output_path = f"{output_dir}/batch_input_{file_index:04d}.jsonl"
        
        if self.config.compress:
            output_path += ".gz"
        
        BatchFileHandler.write_input_file(
            [BatchInputRecord(**r) for r in records],
            output_path if not self.config.compress else output_path[:-3],
            compress=self.config.compress
        )
        
        logger.info(f"Written {len(records)} records to {output_path}")
        
        return output_path
```

### 2. Batch Output Processing

```python
# src/batch/output_processor.py
"""
Batch Output Processing và Analysis
"""

from typing import List, Dict, Any, Optional, Iterator, Callable
from dataclasses import dataclass, field
from pathlib import Path
import json
import logging
from collections import Counter

logger = logging.getLogger(__name__)


@dataclass
class BatchProcessingStats:
    """Statistics từ batch processing."""
    total_records: int
    successful_records: int
    failed_records: int
    blocked_records: int
    
    # Error breakdown
    error_types: Dict[str, int]
    
    # Safety breakdown
    safety_by_category: Dict[str, Dict[str, int]]
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_records == 0:
            return 0.0
        return (self.successful_records / self.total_records) * 100
    
    @property
    def failure_rate(self) -> float:
        """Calculate failure rate."""
        if self.total_records == 0:
            return 0.0
        return (self.failed_records / self.total_records) * 100


@dataclass
class ProcessedRecord:
    """Một record đã được process."""
    original_input: Dict[str, Any]
    output: str
    success: bool
    error: Optional[str] = None
    is_blocked: bool = False
    safety_ratings: Optional[List[Dict[str, Any]]] = None
    finish_reason: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert thành dictionary."""
        return {
            "input": self.original_input,
            "output": self.output,
            "success": self.success,
            "error": self.error,
            "is_blocked": self.is_blocked,
            "finish_reason": self.finish_reason,
        }


class BatchOutputProcessor:
    """
    Processor để process batch outputs và analyze results.
    """
    
    def __init__(self):
        self.stats = None
    
    def process_output_file(
        self,
        output_path: str,
        input_path: Optional[str] = None,
        decompress: bool = False
    ) -> Iterator[ProcessedRecord]:
        """
        Process batch output file.
        
        Args:
            output_path: Path to output file
            input_path: Optional path to input file (để match records)
            decompress: Decompress gzip file
            
        Yields:
            ProcessedRecord objects
        """
        from .formats import BatchFileHandler, BatchOutputRecord
        
        # Load input records if provided
        input_records = {}
        if input_path:
            for i, record in enumerate(BatchFileHandler.read_input_file(input_path, decompress)):
                input_records[i] = record.to_dict()
        
        # Process output records
        for i, record in enumerate(BatchFileHandler.read_output_file(output_path, decompress)):
            # Get corresponding input
            original_input = input_records.get(i, {})
            
            # Check for errors
            if record.error:
                yield ProcessedRecord(
                    original_input=original_input,
                    output="",
                    success=False,
                    error=record.error.get("message", str(record.error)),
                    is_blocked=False,
                )
            elif record.is_blocked:
                yield ProcessedRecord(
                    original_input=original_input,
                    output="",
                    success=False,
                    error="Content blocked by safety filter",
                    is_blocked=True,
                    safety_ratings=record.safety_ratings,
                )
            else:
                yield ProcessedRecord(
                    original_input=original_input,
                    output=record.content or "",
                    success=True,
                    is_blocked=False,
                    safety_ratings=record.safety_ratings,
                    finish_reason=record.finish_reason,
                )
    
    def analyze_output(
        self,
        output_path: str,
        decompress: bool = False
    ) -> BatchProcessingStats:
        """
        Analyze batch output và return statistics.
        """
        total = 0
        successful = 0
        failed = 0
        blocked = 0
        
        error_types: Counter = Counter()
        safety_by_category: Dict[str, Counter] = {
            "HARASSMENT": Counter(),
            "HATE_SPEECH": Counter(),
            "SEXUALLY_EXPLICIT": Counter(),
            "DANGEROUS": Counter(),
        }
        
        for record in self.process_output_file(output_path, decompress=decompress):
            total += 1
            
            if record.success:
                successful += 1
            else:
                failed += 1
                
                if record.is_blocked:
                    blocked += 1
                
                if record.error:
                    error_types[record.error] += 1
            
            # Process safety ratings
            if record.safety_ratings:
                for rating in record.safety_ratings:
                    category = rating.get("category", "").replace("HARM_CATEGORY_", "")
                    probability = rating.get("probability", "")
                    
                    if category in safety_by_category:
                        safety_by_category[category][probability] += 1
        
        self.stats = BatchProcessingStats(
            total_records=total,
            successful_records=successful,
            failed_records=failed,
            blocked_records=blocked,
            error_types=dict(error_types),
            safety_by_category={
                k: dict(v) for k, v in safety_by_category.items()
            },
        )
        
        return self.stats
    
    def write_successful_to_jsonl(
        self,
        output_path: str,
        target_path: str,
        decompress: bool = False
    ) -> int:
        """
        Write successful records to JSONL file.
        
        Returns:
            Number of records written
        """
        count = 0
        
        with open(target_path, 'w', encoding='utf-8') as f:
            for record in self.process_output_file(output_path, decompress=decompress):
                if record.success:
                    output_record = {
                        "input": record.original_input,
                        "output": record.output,
                        "finish_reason": record.finish_reason,
                    }
                    f.write(json.dumps(output_record, ensure_ascii=False) + '\n')
                    count += 1
        
        logger.info(f"Written {count} successful records to {target_path}")
        return count
    
    def write_failed_to_jsonl(
        self,
        output_path: str,
        target_path: str,
        decompress: bool = False
    ) -> int:
        """
        Write failed records to JSONL file (để retry).
        
        Returns:
            Number of records written
        """
        count = 0
        
        with open(target_path, 'w', encoding='utf-8') as f:
            for record in self.process_output_file(output_path, decompress=decompress):
                if not record.success:
                    output_record = {
                        "input": record.original_input,
                        "error": record.error,
                        "is_blocked": record.is_blocked,
                    }
                    f.write(json.dumps(output_record, ensure_ascii=False) + '\n')
                    count += 1
        
        logger.info(f"Written {count} failed records to {target_path}")
        return count
    
    def generate_report(self, stats: BatchProcessingStats) -> str:
        """
        Generate human-readable report.
        """
        lines = [
            "=" * 60,
            "BATCH PROCESSING REPORT",
            "=" * 60,
            "",
            f"Total Records: {stats.total_records}",
            f"Successful: {stats.successful_records} ({stats.success_rate:.2f}%)",
            f"Failed: {stats.failed_records} ({stats.failure_rate:.2f}%)",
            f"Blocked: {stats.blocked_records}",
            "",
        ]
        
        if stats.error_types:
            lines.append("ERROR BREAKDOWN:")
            lines.append("-" * 40)
            for error_type, count in sorted(
                stats.error_types.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                lines.append(f"  {error_type}: {count}")
            lines.append("")
        
        if any(stats.safety_by_category.values()):
            lines.append("SAFETY RATINGS BREAKDOWN:")
            lines.append("-" * 40)
            for category, ratings in stats.safety_by_category.items():
                if ratings:
                    lines.append(f"  {category}:")
                    for prob, count in sorted(ratings.items()):
                        lines.append(f"    {prob}: {count}")
            lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
```

## Common Patterns

### 1. Complete Batch Processing Pipeline

```python
# src/batch/pipeline.py
"""
Complete Batch Processing Pipeline
"""

from typing import List, Optional, Dict, Any, Callable
from dataclasses import dataclass
from pathlib import Path
import logging
import asyncio

from .job_manager import BatchJobManager, BatchJobConfig, BatchJobInfo, BatchJobState
from .input_preparation import BatchInputPreparator, BatchPreparationConfig
from .output_processor import BatchOutputProcessor, BatchProcessingStats

logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """Cấu hình cho batch pipeline."""
    # Project & Location
    project_id: str
    location: str = "us-central1"
    
    # GCS paths
    input_gcs_path: str  # gs://bucket/inputs/
    output_gcs_path: str  # gs://bucket/outputs/
    working_dir: str = "/tmp/batch"
    
    # Job config
    model: str = "gemini-2.0-flash"
    display_name_prefix: str = "batch-job"
    
    # Retry config
    max_job_retries: int = 2
    retry_delay_seconds: int = 300
    
    # Progress
    show_progress: bool = True


class BatchProcessingPipeline:
    """
    Complete pipeline cho batch processing với Gemini.
    """
    
    def __init__(
        self,
        config: PipelineConfig,
        job_manager: Optional[BatchJobManager] = None
    ):
        self.config = config
        self.job_manager = job_manager or BatchJobManager()
        self.input_preparator = BatchInputPreparator()
        self.output_processor = BatchOutputProcessor()
    
    async def run(
        self,
        input_source: str,
        input_type: str,  # "csv", "jsonl", "iterator"
        prompt_column: str = "prompt",
        id_column: Optional[str] = None,
        additional_columns: Optional[List[str]] = None,
        preprocess_fn: Optional[Callable[[str], str]] = None,
        wait_for_completion: bool = True,
        poll_interval: int = 30
    ) -> Dict[str, Any]:
        """
        Run complete batch processing pipeline.
        
        Args:
            input_source: Path to input source
            input_type: Type of input ("csv", "jsonl")
            prompt_column: Column/field chứa prompt
            id_column: Column/field dùng làm ID
            additional_columns: Additional columns để include
            preprocess_fn: Optional preprocessing function
            wait_for_completion: Wait for job to complete
            poll_interval: Seconds between status polls
            
        Returns:
            Dictionary với job info và results
        """
        import uuid
        
        # Generate run ID
        run_id = str(uuid.uuid4())[:8]
        local_working_dir = f"{self.config.working_dir}/{run_id}"
        Path(local_working_dir).mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Starting batch pipeline run {run_id}")
        logger.info(f"Working directory: {local_working_dir}")
        
        # Step 1: Prepare input files
        logger.info("Step 1: Preparing input files...")
        
        prep_config = BatchPreparationConfig(
            max_records_per_file=50000,
            compress=True,
            preprocess_prompt=preprocess_fn,
        )
        self.input_preparator.config = prep_config
        
        if input_type == "csv":
            input_files = self.input_preparator.prepare_from_csv(
                input_source,
                prompt_column,
                local_working_dir,
                additional_columns,
                id_column
            )
        elif input_type == "jsonl":
            input_files = self.input_preparator.prepare_from_jsonl(
                input_source,
                prompt_column,
                local_working_dir,
                id_column
            )
        else:
            raise ValueError(f"Unsupported input type: {input_type}")
        
        logger.info(f"Prepared {len(input_files)} input files")
        
        # Step 2: Upload to GCS
        logger.info("Step 2: Uploading to GCS...")
        
        gcs_input_files = []
        for local_file in input_files:
            gcs_path = await self._upload_to_gcs(
                local_file,
                f"{self.config.input_gcs_path}/{run_id}/{Path(local_file).name}"
            )
            gcs_input_files.append(gcs_path)
        
        logger.info(f"Uploaded {len(gcs_input_files)} files to GCS")
        
        # Step 3: Create and run batch jobs
        logger.info("Step 3: Creating batch jobs...")
        
        jobs = []
        for i, gcs_input in enumerate(gcs_input_files):
            job_config = BatchJobConfig(
                model=self.config.model,
                display_name=f"{self.config.display_name_prefix}-{run_id}-{i}",
            )
            
            gcs_output = f"{self.config.output_gcs_path}/{run_id}/output_{i}.jsonl"
            
            job_name = self.job_manager.create_job(
                gcs_input,
                gcs_output,
                job_config,
                self.config.project_id,
                self.config.location
            )
            
            jobs.append({
                "job_name": job_name,
                "input_file": gcs_input,
                "output_file": gcs_output,
                "index": i,
            })
            
            logger.info(f"Created job {job_name}")
        
        # Step 4: Wait for completion
        if wait_for_completion:
            logger.info("Step 4: Waiting for jobs to complete...")
            
            completed_jobs = []
            
            for job_info in jobs:
                try:
                    final_info = self.job_manager.wait_for_job(
                        job_info["job_name"],
                        poll_interval_seconds=poll_interval,
                        progress_callback=self._progress_callback
                    )
                    
                    completed_jobs.append({
                        **job_info,
                        "state": final_info.state.value,
                        "error": final_info.error_message,
                    })
                    
                except Exception as e:
                    logger.error(f"Error waiting for job {job_info['job_name']}: {e}")
                    completed_jobs.append({
                        **job_info,
                        "state": "ERROR",
                        "error": str(e),
                    })
        
        # Step 5: Download and process results
        logger.info("Step 5: Processing results...")
        
        all_stats = []
        for job_info in completed_jobs:
            if job_info.get("state") == BatchJobState.SUCCEEDED.value:
                # Download output
                local_output = f"{local_working_dir}/output_{job_info['index']}.jsonl"
                await self._download_from_gcs(job_info["output_file"], local_output)
                
                # Analyze
                stats = self.output_processor.analyze_output(local_output)
                all_stats.append(stats)
        
        # Aggregate stats
        aggregated_stats = self._aggregate_stats(all_stats)
        
        logger.info("=" * 60)
        logger.info(f"Pipeline {run_id} completed")
        logger.info(f"Total records: {aggregated_stats['total_records']}")
        logger.info(f"Success rate: {aggregated_stats['success_rate']:.2f}%")
        
        return {
            "run_id": run_id,
            "jobs": completed_jobs,
            "stats": aggregated_stats,
            "working_directory": local_working_dir,
        }
    
    def _progress_callback(self, job_info: BatchJobInfo) -> None:
        """Callback for progress updates."""
        if self.config.show_progress:
            pct = job_info.progress_percent
            logger.info(
                f"Job {job_info.display_name}: {job_info.state.value} "
                f"({pct:.1f}%)"
            )
    
    async def _upload_to_gcs(self, local_path: str, gcs_path: str) -> str:
        """Upload file to GCS."""
        # Implementation depends on GCS client
        # For simplicity, using gsutil command
        import subprocess
        
        cmd = ["gsutil", "cp", local_path, gcs_path]
        subprocess.run(cmd, check=True)
        
        return gcs_path
    
    async def _download_from_gcs(self, gcs_path: str, local_path: str) -> None:
        """Download file from GCS."""
        import subprocess
        
        Path(local_path).parent.mkdir(parents=True, exist_ok=True)
        
        cmd = ["gsutil", "cp", gcs_path, local_path]
        subprocess.run(cmd, check=True)
    
    def _aggregate_stats(
        self,
        stats_list: List[BatchProcessingStats]
    ) -> Dict[str, Any]:
        """Aggregate statistics from multiple batches."""
        if not stats_list:
            return {
                "total_records": 0,
                "successful_records": 0,
                "failed_records": 0,
                "blocked_records": 0,
                "success_rate": 0.0,
            }
        
        total = sum(s.total_records for s in stats_list)
        successful = sum(s.successful_records for s in stats_list)
        failed = sum(s.failed_records for s in stats_list)
        blocked = sum(s.blocked_records for s in stats_list)
        
        return {
            "total_records": total,
            "successful_records": successful,
            "failed_records": failed,
            "blocked_records": blocked,
            "success_rate": (successful / total * 100) if total > 0 else 0.0,
            "total_batches": len(stats_list),
        }
```

### 2. Incremental Batch Processing

```typescript
// src/batch/incremental-processor.ts
/**
 * Incremental Batch Processor (TypeScript)
 * Xử lý only new/changed records since last run
 */

import { BatchJobManager, BatchJobConfig, BatchJobInfo, BatchJobState } from './job-manager';
import { BatchFileHandler, BatchInputRecord, BatchOutputRecord } from './formats';

interface IncrementalState {
  lastProcessedTimestamp: string;
  processedIds: Set<string>;
  cursor: string | null;
}

export class IncrementalBatchProcessor {
  private jobManager: BatchJobManager;
  private stateFile: string;
  
  constructor(projectId: string, stateFile: string) {
    this.jobManager = new BatchJobManager(projectId);
    this.stateFile = stateFile;
  }
  
  /**
   * Load incremental state
   */
  private loadState(): IncrementalState {
    try {
      const content = readFileSync(this.stateFile, 'utf-8');
      const state = JSON.parse(content);
      return {
        lastProcessedTimestamp: state.lastProcessedTimestamp || '',
        processedIds: new Set(state.processedIds || []),
        cursor: state.cursor || null,
      };
    } catch {
      return {
        lastProcessedTimestamp: '',
        processedIds: new Set(),
        cursor: null,
      };
    }
  }
  
  /**
   * Save incremental state
   */
  private saveState(state: IncrementalState): void {
    const content = JSON.stringify({
      lastProcessedTimestamp: state.lastProcessedTimestamp,
      processedIds: Array.from(state.processedIds),
      cursor: state.cursor,
    });
    writeFileSync(this.stateFile, content, 'utf-8');
  }
  
  /**
   * Process incremental batch
   */
  async processIncremental(
    records: AsyncGenerator<BatchInputRecord>,
    getRecordId: (record: BatchInputRecord) => string,
    processOutput: (output: BatchOutputRecord, input: BatchInputRecord) => Promise<void>,
    options: {
      batchSize?: number;
      maxConcurrency?: number;
      onProgress?: (progress: { processed: number; total: number }) => void;
    } = {}
  ): Promise<{ processed: number; failed: number }> {
    const state = this.loadState();
    const batchSize = options.batchSize || 1000;
    
    let batch: BatchInputRecord[] = [];
    let processedCount = 0;
    let failedCount = 0;
    let latestTimestamp = state.lastProcessedTimestamp;
    
    for await (const record of records) {
      const recordId = getRecordId(record);
      
      // Skip already processed
      if (state.processedIds.has(recordId)) {
        continue;
      }
      
      batch.push(record);
      
      if (batch.length >= batchSize) {
        const result = await this.processBatch(batch, processOutput);
        processedCount += result.processed;
        failedCount += result.failed;
        
        // Update state
        for (const rec of batch) {
          state.processedIds.add(getRecordId(rec));
        }
        this.saveState(state);
        
        // Update progress
        if (options.onProgress) {
          options.onProgress({
            processed: processedCount,
            total: state.processedIds.size + batch.length,
          });
        }
        
        batch = [];
      }
    }
    
    // Process remaining batch
    if (batch.length > 0) {
      const result = await this.processBatch(batch, processOutput);
      processedCount += result.processed;
      failedCount += result.failed;
      
      for (const rec of batch) {
        state.processedIds.add(getRecordId(rec));
      }
      this.saveState(state);
    }
    
    return { processed: processedCount, failed: failedCount };
  }
  
  /**
   * Process a single batch
   */
  private async processBatch(
    inputRecords: BatchInputRecord[],
    processOutput: (output: BatchOutputRecord, input: BatchInputRecord) => Promise<void>
  ): Promise<{ processed: number; failed: number }> {
    // Write batch to temp file
    const inputPath = `/tmp/batch_${Date.now()}_input.jsonl`;
    const outputPath = `/tmp/batch_${Date.now()}_output.jsonl`;
    
    await BatchFileHandler.writeInputFile(inputRecords, inputPath);
    
    try {
      // Create job
      const jobName = await this.jobManager.createJob(
        inputPath,
        outputPath,
        {}
      );
      
      // Wait for completion
      await this.jobManager.waitForJob(jobName, {
        pollIntervalSeconds: 30,
      });
      
      // Process output
      let processed = 0;
      let failed = 0;
      
      for await (const output of BatchFileHandler.readOutputFile(outputPath)) {
        const inputIndex = output.clientInfo?.['row_index'] || processed;
        const inputRecord = inputRecords[parseInt(inputIndex)] || inputRecords[processed];
        
        await processOutput(output, inputRecord);
        
        if (output.error) {
          failed++;
        } else {
          processed++;
        }
      }
      
      return { processed, failed };
      
    } finally {
      // Cleanup temp files
      // await unlink(inputPath);
      // await unlink(outputPath);
    }
  }
}
```

## Examples

### 1. Complete Batch Processing Example - Python

```python
# src/examples/batch_processing.py
"""
Complete Batch Processing Example
"""

import asyncio
import logging
from pathlib import Path
from google.cloud import storage
from src.batch.pipeline import BatchProcessingPipeline, PipelineConfig
from src.batch.output_processor import BatchOutputProcessor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main execution."""
    
    # Configuration
    config = PipelineConfig(
        project_id="my-project-123",
        location="us-central1",
        input_gcs_path="gs://my-bucket/batch-inputs",
        output_gcs_path="gs://my-bucket/batch-outputs",
        working_dir="/tmp/batch-processing",
        model="gemini-2.0-flash",
        display_name_prefix="my-batch-job",
    )
    
    # Create pipeline
    pipeline = BatchProcessingPipeline(config)
    
    # Optional preprocessing function
    def preprocess_prompt(prompt: str) -> str:
        # Clean and format prompt
        prompt = prompt.strip()
        
        # Add context if missing
        if not prompt.endswith('?'):
            prompt = prompt + "?"
        
        return prompt
    
    # Run pipeline
    result = await pipeline.run(
        input_source="data/customer_queries.csv",
        input_type="csv",
        prompt_column="query",
        id_column="query_id",
        additional_columns=["customer_tier", "category"],
        preprocess_fn=preprocess_prompt,
        wait_for_completion=True,
        poll_interval=60
    )
    
    # Print summary
    logger.info("=" * 60)
    logger.info("BATCH PROCESSING COMPLETED")
    logger.info("=" * 60)
    logger.info(f"Run ID: {result['run_id']}")
    logger.info(f"Total Records: {result['stats']['total_records']}")
    logger.info(f"Success Rate: {result['stats']['success_rate']:.2f}%")
    logger.info(f"Failed Records: {result['stats']['failed_records']}")
    
    # Generate detailed report
    processor = BatchOutputProcessor()
    for job in result['jobs']:
        if job.get('state') == 'JOB_STATE_SUCCEEDED':
            local_output = f"{result['working_directory']}/output_{job['index']}.jsonl"
            stats = processor.analyze_output(local_output)
            print(processor.generate_report(stats))
    
    # Export successful results
    output_dir = Path(result['working_directory'])
    success_output = output_dir / "successful_results.jsonl"
    
    for job in result['jobs']:
        if job.get('state') == 'JOB_STATE_SUCCEEDED':
            local_output = f"{result['working_directory']}/output_{job['index']}.jsonl"
            processor.write_successful_to_jsonl(local_output, str(success_output))
    
    logger.info(f"Results exported to: {success_output}")


if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Complete Batch Processing Example - TypeScript

```typescript
// src/examples/batch-processing.ts
/**
 * Complete Batch Processing Example (TypeScript)
 */

import { BatchJobManager, BatchJobConfig } from '../batch/job-manager';
import { BatchFileHandler, BatchInputRecord } from '../batch/formats';
import { BatchOutputProcessor } from '../batch/output-processor';

async function main() {
  const projectId = 'my-project-123';
  const location = 'us-central1';
  
  // Initialize manager
  const jobManager = new BatchJobManager(projectId, location);
  
  // Example 1: Create and run a batch job
  console.log('Creating batch job...');
  
  const inputRecords: BatchInputRecord[] = [
    { prompt: 'What is machine learning?' },
    { prompt: 'Explain neural networks in simple terms.' },
    { prompt: 'What are the benefits of AI?' },
    { prompt: 'How does deep learning work?' },
    { prompt: 'What is natural language processing?' },
  ];
  
  // Write input file
  const inputPath = '/tmp/batch_input.jsonl';
  await BatchFileHandler.writeInputFile(inputRecords, inputPath);
  
  // Create job config
  const jobConfig: BatchJobConfig = {
    displayName: `batch-job-${Date.now()}`,
    model: 'gemini-2.0-flash',
    temperature: 0.7,
    maxOutputTokens: 1024,
  };
  
  // Create job
  const inputGcsPath = 'gs://my-bucket/inputs/batch_input.jsonl';
  const outputGcsPath = 'gs://my-bucket/outputs/batch_output.jsonl';
  
  // Upload to GCS (simplified - use actual GCS client)
  console.log('Uploading input to GCS...');
  // await uploadToGCS(inputPath, inputGcsPath);
  
  // Create batch job
  const jobName = await jobManager.createJob(
    inputGcsPath,
    outputGcsPath,
    jobConfig
  );
  
  console.log(`Created job: ${jobName}`);
  
  // Wait for completion
  console.log('Waiting for job to complete...');
  
  const finalJob = await jobManager.waitForJob(jobName, {
    pollIntervalSeconds: 30,
    onProgress: (info) => {
      console.log(`Progress: ${info.state} - ${info.completedAttemptCount}/${info.attemptCount}`);
    },
  });
  
  console.log(`Job completed with state: ${finalJob.state}`);
  
  if (finalJob.state === 'JOB_STATE_SUCCEEDED') {
    // Download output
    const outputLocalPath = '/tmp/batch_output.jsonl';
    console.log('Downloading output from GCS...');
    // await downloadFromGCS(outputGcsPath, outputLocalPath);
    
    // Process output
    const processor = new BatchOutputProcessor();
    const stats = processor.analyzeOutput(outputLocalPath);
    
    console.log('='.repeat(60));
    console.log('BATCH RESULTS');
    console.log('='.repeat(60));
    console.log(`Total Records: ${stats.totalRecords}`);
    console.log(`Successful: ${stats.successfulRecords}`);
    console.log(`Failed: ${stats.failedRecords}`);
    console.log(`Blocked: ${stats.blockedRecords}`);
    console.log(`Success Rate: ${stats.successRate.toFixed(2)}%`);
    
    // Generate report
    console.log(processor.generateReport(stats));
  }
  
  // Example 2: List and manage jobs
  console.log('\nListing recent jobs...');
  
  const recentJobs = await jobManager.listJobs(
    `state="JOB_STATE_SUCCEEDED" OR state="JOB_STATE_FAILED"`
  );
  
  for (const job of recentJobs.slice(0, 5)) {
    console.log(`- ${job.displayName}: ${job.state} (${job.createTime})`);
  }
}

// Run
main().catch(console.error);
```

## Troubleshooting

### Các Vấn Đề Thường Gặp

**1. "Job stuck in PENDING state"**

```
Nguyên nhân: Quá nhiều jobs đang chạy, hoặc quota issue
Giải pháp:
- Kiểm tra quota trong Google Cloud Console
- Reduce số lượng concurrent jobs
- Check nếu input file format đúng
- Xem job error messages
```

**2. "Partial failures in output"**

```
Nguyên nhân: Một số records có vấn đề (safety block, invalid input, etc.)
Giải pháp:
- Analyze error breakdown từ output processor
- Check safety ratings cho blocked content
- Validate input prompts trước khi submit
- Implement retry cho failed records
```

**3. "Output file missing or empty"**

```
Nguyên nhân: Job failed hoặc output path sai
Giải pháp:
- Check job state và error message
- Verify GCS permissions
- Check input file format (must be valid JSONL)
- Verify output path format
```

**4. "High cost despite batch discount"**

```
Nguyên nhân: Quá nhiều tokens hoặc records
Giải pháp:
- Optimize prompts để reduce tokens
- Filter out low-priority records
- Use batching efficiently (larger batches = better economics)
- Monitor token usage per batch
```

**5. "Timeout waiting for job"**

```
Nguyên nhân: Job mất quá lâu để complete
Giải pháp:
- Split thành smaller batches
- Check nếu có bottleneck (quota, resources)
- Implement progress monitoring và alerts
- Consider increasing timeout hoặc async processing
```

## References

### Official Documentation

- [Batch Prediction Overview](https://cloud.google.com/vertex-ai/docs/generative-ai/preview/batch-prediction)
- [Batch Prediction API](https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.batchPredictionJobs)
- [Batch Prediction Formats](https://cloud.google.com/vertex-ai/docs/generative-ai/preview/batch-prediction#input-and-output)

### Related Documents

- `@gemini-api-setup.md` - Setup và configuration
- `@cost-optimization.mdc` - Cost optimization strategies
- `@performance.mdc` - Performance best practices
- `@monitoring.mdc` - Monitoring và logging
