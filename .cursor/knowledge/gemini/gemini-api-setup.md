---
title: "Gemini API Setup - AI Studio và Vertex AI Configuration"
description: "Hướng dẫn toàn diện về thiết lập Google Gemini API, so sánh AI Studio vs Vertex AI, quản lý API key, và cấu hình SDK cho Python/Node.js trong môi trường enterprise"
tags:
  - "gemini"
  - "api-setup"
  - "ai-studio"
  - "vertex-ai"
  - "api-key"
  - "sdk-configuration"
  - "enterprise"
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Gemini API Setup - AI Studio và Vertex AI Configuration

## Tổng Quan (Overview)

Google Gemini API là giao diện lập trình cho phép các nhà phát triển tích hợp khả năng của các mô hình AI Gemini vào ứng dụng của họ. Việc thiết lập API một cách đúng đắn là bước nền tảng quan trọng cho bất kỳ dự án enterprise nào sử dụng Gemini.

Trong phạm vi tài liệu này, chúng ta sẽ đi sâu vào các khía cạnh kỹ thuật của việc thiết lập Gemini API, bao gồm sự khác biệt giữa Google AI Studio và Vertex AI, cách quản lý API key an toàn, cấu hình SDK cho Python và Node.js, và các chiến lược tối ưu hóa quota và limits cho môi trường production.

Việc hiểu rõ sự khác biệt giữa các nền tảng và cách cấu hình đúng sẽ giúp đội ngũ phát triển tránh được nhiều vấn đề phổ biến và xây dựng hệ thống ổn định ngay từ đầu.

## Mục Đích (Purpose)

Tài liệu này phục vụ các mục đích chính sau:

**1. Hướng Dẫn Thiết Lập Chuẩn Enterprise**

Cung cấp các best practices cho việc thiết lập Gemini API trong môi trường enterprise, bao gồm security configuration, quota management, và monitoring setup. Mục tiêu là giúp các đội ngũ DevOps và Backend có thể triển khai hệ thống một cách nhất quán và an toàn.

**2. So Sánh Nền Tảng AI Studio và Vertex AI**

Giải thích chi tiết sự khác biệt giữa Google AI Studio (dành cho phát triển và thử nghiệm) và Vertex AI (dành cho production enterprise), giúp người đọc đưa ra quyết định đúng đắn về nền tảng phù hợp với nhu cầu của họ.

**3. Cung Cấp Code Examples Thực Tế**

Bao gồm các ví dụ code hoàn chỉnh cho cả Python và Node.js, từ cơ bản đến nâng cao, giúp developers có thể copy-paste và customize theo nhu cầu cụ thể của dự án.

## Các Khái Niệm Cốt Lõi (Key Concepts)

### 1. Google AI Studio

Google AI Studio là môi trường phát triển tích hợp (IDE) trực tuyến của Google dành cho việc làm việc với Gemini API. Đây là điểm khởi đầu lý tưởng cho các nhà phát triển muốn thử nghiệm nhanh với các mô hình Gemini.

**Đặc điểm chính của AI Studio:**

- Giao diện web-based cho phép tương tác trực tiếp với các mô hình Gemini
- Hỗ trợ testing nhanh các prompt và parameters
- Quản lý API keys dễ dàng thông qua giao diện
- Cung cấp các templates và examples có sẵn
- Miễn phí với tier cơ bản, phù hợp cho development và prototyping

**Giới hạn của AI Studio:**

- Không phù hợp cho production với traffic lớn
- Giới hạn về quota và rate limiting
- Không có các tính năng enterprise như VPC, IAM chi tiết
- Không hỗ trợ các tính năng compliance nâng cao

### 2. Vertex AI

Vertex AI là nền tảng Machine Learning enterprise của Google Cloud, cung cấp môi trường production-grade cho việc triển khai Gemini models. Vertex AI được thiết kế cho các doanh nghiệp cần scale, security, và các tính năng enterprise.

**Lợi ích của Vertex AI cho Enterprise:**

- **Scale không giới hạn**: Có thể xử lý hàng triệu requests mà không gặp vấn đề về capacity
- **Security nâng cao**: Tích hợp với VPC, Private Service Connect, và IAM chi tiết
- **Compliance**: Hỗ trợ HIPAA, SOC 2, ISO 27001, và các compliance frameworks khác
- **Monitoring và Logging**: Tích hợp sẵn với Cloud Monitoring, Cloud Logging, và Audit Logs
- **Cost Management**: Các công cụ chi tiết cho việc theo dõi và tối ưu chi phí

### 3. Sự Khác Biệt Chi Tiết: AI Studio vs Vertex AI

| Tiêu chí | AI Studio | Vertex AI |
|----------|-----------|-----------|
| Mục đích sử dụng | Development, Testing, Prototyping | Production Enterprise |
| Authentication | API Key đơn giản | Service Account, OAuth 2.0 |
| Network Security | Không có VPC | VPC, PSC, Private DNS |
| Quota Management | Giới hạn cố định | Có thể request tăng quota |
| SLA | Không có | 99.9% uptime |
| Cost | Free tier có giới hạn | Pay-per-use, commit discounts |
| Compliance | Cơ bản | Đầy đủ enterprise compliance |
| Integrations | Giới hạn | Toàn bộ Google Cloud ecosystem |

### 4. API Key Management

Quản lý API key là một trong những khía cạnh quan trọng nhất của security. Dưới đây là các best practices được khuyến nghị.

**Nguyên tắc quan trọng:**

- Không bao giờ commit API keys vào source code
- Sử dụng environment variables hoặc secret management services
- Rotate API keys định kỳ
- Theo dõi và audit việc sử dụng API keys
- Sử dụng separate keys cho development và production

**Các phương pháp lưu trữ API Key:**

**Environment Variables (Development):**

```python
# Development environment - sử dụng .env file
import os
from dotenv import load_dotenv

load_dotenv()

# Lấy API key từ environment variable
api_key = os.getenv("GEMINI_API_KEY")
```

```typescript
// Node.js - Development environment
import 'dotenv/config';

const apiKey = process.env.GEMINI_API_KEY;
```

**Google Secret Manager (Production):**

```python
# Production environment - sử dụng Secret Manager
from google.cloud import secretmanager
import os

def get_api_key_from_secret_manager(project_id: str, secret_id: str) -> str:
    """
    Lấy API key từ Google Secret Manager.
    
    Args:
        project_id: Google Cloud Project ID
        secret_id: Tên của secret chứa API key
        
    Returns:
        API key string
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Sử dụng
api_key = get_api_key_from_secret_manager(
    project_id="my-project-123",
    secret_id="gemini-api-key"
)
```

```typescript
// Node.js - Production với Secret Manager
import { SecretManagerServiceClient } from '@google-cloud/secret-manager';

async function getApiKeyFromSecretManager(
    projectId: string,
    secretId: string
): Promise<string> {
    const client = new SecretManagerServiceClient();
    const [version] = await client.accessSecretVersion({
        name: `projects/${projectId}/secrets/${secretId}/versions/latest`,
    });
    return version.payload?.data?.toString() ?? '';
}
```

## Best Practices

### 1. SDK Setup cho Python

```python
# requirements.txt
google-generativeai>=0.8.0
google-cloud-aiplatform>=1.60.0
python-dotenv>=1.0.0

# Cài đặt
# pip install -r requirements.txt
```

```python
# src/config/gemini_config.py
"""
Module cấu hình Gemini API cho ứng dụng.
Hỗ trợ cả AI Studio (Direct API) và Vertex AI.
"""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from google import generativeai as genai
from google.cloud import aiplatform
from dotenv import load_dotenv

load_dotenv()


class Platform(Enum):
    """Enum cho các nền tảng Gemini API."""
    AI_STUDIO = "ai_studio"
    VERTEX_AI = "vertex_ai"


@dataclass
class GeminiConfig:
    """Cấu hình chi tiết cho Gemini API."""
    
    # Platform settings
    platform: Platform = Platform.AI_STUDIO
    
    # AI Studio settings
    api_key: Optional[str] = None
    
    # Vertex AI settings
    project_id: Optional[str] = None
    location: str = "us-central1"
    
    # Model settings
    model_name: str = "gemini-2.0-flash"
    generation_config: dict = None
    
    # Safety settings
    safety_settings: dict = None
    
    # System instruction
    system_instruction: Optional[str] = None
    
    def __post_init__(self):
        if self.generation_config is None:
            self.generation_config = {
                "temperature": 0.9,
                "top_p": 1.0,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
        
        if self.safety_settings is None:
            self.safety_settings = {
                "HARASSMENT": "block_medium_and_above",
                "HATE_SPEECH": "block_medium_and_above",
                "SEXUALLY_EXPLICIT": "block_medium_and_above",
                "DANGEROUS": "block_medium_and_above",
            }
    
    @classmethod
    def from_env(cls) -> "GeminiConfig":
        """
        Tạo cấu hình từ environment variables.
        
        Environment variables:
        - GEMINI_PLATFORM: 'ai_studio' hoặc 'vertex_ai'
        - GEMINI_API_KEY: API key cho AI Studio
        - GEMINI_PROJECT_ID: Project ID cho Vertex AI
        - GEMINI_LOCATION: Location cho Vertex AI (default: us-central1)
        - GEMINI_MODEL: Model name (default: gemini-2.0-flash)
        """
        platform_str = os.getenv("GEMINI_PLATFORM", "ai_studio").lower()
        platform = Platform.VERTEX_AI if platform_str == "vertex_ai" else Platform.AI_STUDIO
        
        config = cls(
            platform=platform,
            api_key=os.getenv("GEMINI_API_KEY"),
            project_id=os.getenv("GEMINI_PROJECT_ID"),
            location=os.getenv("GEMINI_LOCATION", "us-central1"),
            model_name=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        )
        
        return config


def initialize_gemini(config: GeminiConfig) -> None:
    """
    Khởi tạo Gemini API với cấu hình được chỉ định.
    
    Args:
        config: GeminiConfig object chứa các thông số cấu hình
        
    Raises:
        ValueError: Nếu cấu hình không hợp lệ
    """
    if config.platform == Platform.AI_STUDIO:
        if not config.api_key:
            raise ValueError(
                "API key is required for AI Studio platform. "
                "Set GEMINI_API_KEY environment variable."
            )
        genai.configure(api_key=config.api_key)
        
    elif config.platform == Platform.VERTEX_AI:
        if not config.project_id:
            raise ValueError(
                "Project ID is required for Vertex AI platform. "
                "Set GEMINI_PROJECT_ID environment variable."
            )
        aiplatform.init(project=config.project_id, location=config.location)


def create_model(config: GeminiConfig) -> "generativeai.GenerativeModel":
    """
    Tạo Gemini model instance với cấu hình được chỉ định.
    
    Args:
        config: GeminiConfig object
        
    Returns:
        GenerativeModel instance
    """
    model = genai.GenerativeModel(
        model_name=config.model_name,
        generation_config=config.generation_config,
        safety_settings=config.safety_settings,
        system_instruction=config.system_instruction,
    )
    return model


# Singleton pattern cho application-wide usage
class GeminiClient:
    """
    Singleton client cho Gemini API.
    Sử dụng pattern này để tránh việc khởi tạo nhiều lần.
    """
    
    _instance: Optional["GeminiClient"] = None
    _model: Optional["generativeai.GenerativeModel"] = None
    _config: Optional[GeminiConfig] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def initialize(cls, config: Optional[GeminiConfig] = None) -> None:
        """
        Khởi tạo Gemini client.
        
        Args:
            config: GeminiConfig object. Nếu None, sử dụng config từ env vars.
        """
        if cls._model is not None:
            return  # Đã được khởi tạo rồi
        
        config = config or GeminiConfig.from_env()
        initialize_gemini(config)
        cls._model = create_model(config)
        cls._config = config
    
    @classmethod
    def get_model(cls) -> "generativeai.GenerativeModel":
        """
        Lấy model instance hiện tại.
        
        Returns:
            GenerativeModel instance
            
        Raises:
            RuntimeError: Nếu client chưa được khởi tạo
        """
        if cls._model is None:
            cls.initialize()
        return cls._model
    
    @classmethod
    def reset(cls) -> None:
        """Reset singleton instance - hữu ích cho testing."""
        cls._instance = None
        cls._model = None
        cls._config = None
```

### 2. SDK Setup cho Node.js/TypeScript

```typescript
// src/config/gemini.config.ts
/**
 * Gemini API Configuration Module
 * Hỗ trợ cả AI Studio (Direct API) và Vertex AI
 */

import { GoogleGenerativeAI, HarmBlockThreshold, HarmCategory } from '@google/generative-ai';
import { VertexAI } from '@google-cloud/vertexai';
import process from 'process';

// Enum cho platform
export enum Platform {
  AI_STUDIO = 'ai_studio',
  VERTEX_AI = 'vertex_ai',
}

// Interface cho cấu hình
export interface GeminiConfig {
  platform: Platform;
  apiKey?: string;
  projectId?: string;
  location: string;
  modelName: string;
  generationConfig?: {
    temperature?: number;
    topP?: number;
    topK?: number;
    maxOutputTokens?: number;
    responseMimeType?: string;
  };
  safetySettings?: Array<{
    category: HarmCategory;
    threshold: HarmBlockThreshold;
  }>;
  systemInstruction?: string;
}

// Default configuration
export const defaultConfig: GeminiConfig = {
  platform: Platform.AI_STUDIO,
  location: 'us-central1',
  modelName: 'gemini-2.0-flash',
  generationConfig: {
    temperature: 0.9,
    topP: 1.0,
    topK: 40,
    maxOutputTokens: 2048,
  },
  safetySettings: [
    { category: HarmCategory.HARM_CATEGORY_HARASSMENT, threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE },
    { category: HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE },
    { category: HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE },
    { category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE },
  ],
};

// Load config từ environment variables
export function loadConfigFromEnv(): GeminiConfig {
  const platformStr = process.env.GEMINI_PLATFORM?.toLowerCase() || 'ai_studio';
  const platform = platformStr === 'vertex_ai' ? Platform.VERTEX_AI : Platform.AI_STUDIO;
  
  return {
    ...defaultConfig,
    platform,
    apiKey: process.env.GEMINI_API_KEY,
    projectId: process.env.GEMINI_PROJECT_ID,
    location: process.env.GEMINI_LOCATION || 'us-central1',
    modelName: process.env.GEMINI_MODEL || 'gemini-2.0-flash',
  };
}

// Factory class cho việc tạo clients
export class GeminiClientFactory {
  private static instance: GoogleGenerativeAI | VertexAI | null = null;
  private static config: GeminiConfig | null = null;
  
  /**
   * Khởi tạo Gemini client với cấu hình được chỉ định
   */
  static initialize(config: GeminiConfig = loadConfigFromEnv()): void {
    if (this.instance) {
      console.warn('Gemini client already initialized. Call reset() first to reinitialize.');
      return;
    }
    
    this.config = config;
    
    if (config.platform === Platform.AI_STUDIO) {
      if (!config.apiKey) {
        throw new Error('API key is required for AI Studio platform');
      }
      this.instance = new GoogleGenerativeAI(config.apiKey);
    } else {
      if (!config.projectId) {
        throw new Error('Project ID is required for Vertex AI platform');
      }
      this.instance = new VertexAI({
        project: config.projectId,
        location: config.location,
      });
    }
  }
  
  /**
   * Lấy model instance cho AI Studio
   */
  static getModel(): GoogleGenerativeAI {
    if (!(this.instance instanceof GoogleGenerativeAI)) {
      throw new Error('Model is only available for AI Studio platform');
    }
    return this.instance;
  }
  
  /**
   * Lấy Vertex AI instance
   */
  static getVertexAI(): VertexAI {
    if (!(this.instance instanceof VertexAI)) {
      throw new Error('Vertex AI instance is only available for Vertex AI platform');
    }
    return this.instance;
  }
  
  /**
   * Tạo generative model cho AI Studio
   */
  static createGenerativeModel(): InstanceType<typeof GoogleGenerativeAI>['getGenerativeModel'] {
    const client = this.getModel();
    return client.getGenerativeModel({
      model: this.config?.modelName || 'gemini-2.0-flash',
      generationConfig: this.config?.generationConfig,
      safetySettings: this.config?.safetySettings,
      systemInstruction: this.config?.systemInstruction,
    });
  }
  
  /**
   * Tạo preview generative model cho Vertex AI
   */
  static createVertexGenerativeModel(): InstanceType<typeof VertexAI>['getGenerativeModel'] {
    const client = this.getVertexAI();
    return client.getGenerativeModel({
      model: this.config?.modelName || 'gemini-2.0-flash',
      generationConfig: this.config?.generationConfig,
      safetySettings: this.config?.safetySettings,
      systemInstruction: this.config?.systemInstruction,
    });
  }
  
  /**
   * Reset client - hữu ích cho testing
   */
  static reset(): void {
    this.instance = null;
    this.config = null;
  }
}
```

```typescript
// src/services/gemini.service.ts
/**
 * Gemini Service - Abstraction layer cho Gemini API
 */

import {
  GoogleGenerativeAI,
  GenerateContentRequest,
  GenerateContentResult,
  Part,
} from '@google/generative-ai';
import { GeminiClientFactory, loadConfigFromEnv, GeminiConfig } from '../config/gemini.config';

export interface ChatSession {
  sendMessage: (message: string | Part[]) => Promise<GenerateContentResult>;
  sendMessageStream: (message: string | Part[]) => Promise<AsyncGenerator<GenerateContentResult>>;
  history: () => Array<{ role: string; parts: Part[] }>;
  model: string;
}

export class GeminiService {
  private model: ReturnType<GoogleGenerativeAI['getGenerativeModel']>;
  
  constructor(config?: GeminiConfig) {
    if (!config) {
      config = loadConfigFromEnv();
    }
    
    if (!config.apiKey) {
      throw new Error('API key is required');
    }
    
    const client = new GoogleGenerativeAI(config.apiKey);
    this.model = client.getGenerativeModel({
      model: config.modelName,
      generationConfig: config.generationConfig,
      safetySettings: config.safetySettings,
      systemInstruction: config.systemInstruction,
    });
  }
  
  /**
   * Generate content từ prompt
   */
  async generateContent(prompt: string | Part[]): Promise<GenerateContentResult> {
    try {
      const result = await this.model.generateContent(prompt);
      return result;
    } catch (error) {
      console.error('Error generating content:', error);
      throw error;
    }
  }
  
  /**
   * Generate content với streaming response
   */
  async *generateContentStream(prompt: string | Part[]): AsyncGenerator<GenerateContentResult> {
    const stream = await this.model.generateContentStream(prompt);
    
    for await (const chunk of stream) {
      yield chunk;
    }
  }
  
  /**
   * Tạo chat session
   */
  startChat(initialHistory?: Array<{ role: string; parts: Part[] }>): ChatSession {
    const session = this.model.startChat({
      history: initialHistory,
    });
    
    return {
      sendMessage: async (message: string | Part[]) => {
        const result = await session.sendMessage(message);
        return result;
      },
      sendMessageStream: async function* (message: string | Part[]) {
        const stream = await session.sendMessageStream(message);
        for await (const chunk of stream) {
          yield chunk;
        }
      },
      history: () => session.getHistory(),
      model: this.model.model,
    };
  }
  
  /**
   * Count tokens trong prompt
   */
  async countTokens(text: string | Part[]): Promise<number> {
    const result = await this.model.countTokens(text);
    return result.totalTokens;
  }
}
```

### 3. Quota và Limits Management

```python
# src/monitoring/quota_manager.py
"""
Quota Manager - Theo dõi và quản lý API usage
"""

import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
import threading


class QuotaType(Enum):
    """Các loại quota."""
    REQUESTS_PER_MINUTE = "requests_per_minute"
    REQUESTS_PER_DAY = "requests_per_day"
    TOKENS_PER_MINUTE = "tokens_per_minute"
    TOKENS_PER_DAY = "tokens_per_day"


@dataclass
class QuotaLimit:
    """Định nghĩa một quota limit."""
    quota_type: QuotaType
    limit: int
    window_seconds: int = 60  # Default 1 phút
    
    def is_per_day(self) -> bool:
        return self.quota_type in [
            QuotaType.REQUESTS_PER_DAY,
            QuotaType.TOKENS_PER_DAY
        ]


@dataclass
class QuotaUsage:
    """Theo dõi việc sử dụng quota."""
    timestamps: List[float] = field(default_factory=list)
    token_counts: List[int] = field(default_factory=list)
    
    def add_request(self, timestamp: float, token_count: int = 0) -> None:
        """Thêm một request mới."""
        self.timestamps.append(timestamp)
        if token_count > 0:
            self.token_counts.append(token_count)
    
    def get_count_in_window(self, window_seconds: int) -> int:
        """Đếm số requests trong khoảng thời gian."""
        cutoff = time.time() - window_seconds
        return sum(1 for ts in self.timestamps if ts >= cutoff)
    
    def get_tokens_in_window(self, window_seconds: int) -> int:
        """Đếm tổng tokens trong khoảng thời gian."""
        cutoff = time.time() - window_seconds
        total = 0
        for ts, tokens in zip(self.timestamps, self.token_counts):
            if ts >= cutoff:
                total += tokens
        return total
    
    def cleanup_old_entries(self, max_age_seconds: int) -> None:
        """Xóa các entries cũ để tiết kiệm memory."""
        cutoff = time.time() - max_age_seconds
        new_timestamps = []
        new_token_counts = []
        
        for ts, tokens in zip(self.timestamps, self.token_counts):
            if ts >= cutoff:
                new_timestamps.append(ts)
                new_token_counts.append(tokens)
        
        self.timestamps = new_timestamps
        self.token_counts = new_token_counts


class QuotaManager:
    """
    Manager để theo dõi và enforce quota limits.
    Thread-safe cho multi-threaded applications.
    """
    
    def __init__(self, limits: List[QuotaLimit]):
        """
        Khởi tạo QuotaManager.
        
        Args:
            limits: Danh sách các quota limits
        """
        self.limits = {limit.quota_type: limit for limit in limits}
        self.usage: Dict[QuotaType, QuotaUsage] = {
            qt: QuotaUsage() for qt in self.limits.keys()
        }
        self._lock = threading.Lock()
        
        # Background cleanup thread
        self._running = True
        self._cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._cleanup_thread.start()
    
    def _cleanup_loop(self) -> None:
        """Background loop để cleanup old entries."""
        while self._running:
            time.sleep(300)  # Cleanup mỗi 5 phút
            self.cleanup()
    
    def check_and_update(
        self,
        quota_type: QuotaType,
        token_count: int = 0,
        raise_on_exceeded: bool = True
    ) -> bool:
        """
        Kiểm tra và cập nhật quota usage.
        
        Args:
            quota_type: Loại quota cần kiểm tra
            token_count: Số tokens của request (cho token quotas)
            raise_on_exceeded: Có raise exception không nếu quota exceeded
            
        Returns:
            True nếu request được phép
            
        Raises:
            QuotaExceededError: Nếu quota đã exceeded và raise_on_exceeded=True
        """
        if quota_type not in self.limits:
            return True  # Không có limit cho loại quota này
        
        limit = self.limits[quota_type]
        current_time = time.time()
        
        with self._lock:
            usage = self.usage[quota_type]
            
            # Xác định window
            window = limit.window_seconds if not limit.is_per_day() else 86400
            
            # Kiểm tra current usage
            if quota_type in [QuotaType.REQUESTS_PER_MINUTE, QuotaType.REQUESTS_PER_DAY]:
                current_usage = usage.get_count_in_window(window)
            else:
                current_usage = usage.get_tokens_in_window(window)
            
            # Kiểm tra limit
            if current_usage >= limit.limit:
                if raise_on_exceeded:
                    raise QuotaExceededError(
                        f"Quota exceeded for {quota_type.value}: "
                        f"{current_usage}/{limit.limit} in {window}s window"
                    )
                return False
            
            # Cập nhật usage
            usage.add_request(current_time, token_count)
            return True
    
    def get_usage(self, quota_type: QuotaType) -> Dict[str, int]:
        """Lấy thông tin usage hiện tại."""
        if quota_type not in self.limits:
            return {}
        
        limit = self.limits[quota_type]
        usage = self.usage[quota_type]
        window = limit.window_seconds if not limit.is_per_day() else 86400
        
        if quota_type in [QuotaType.REQUESTS_PER_MINUTE, QuotaType.REQUESTS_PER_DAY]:
            count = usage.get_count_in_window(window)
        else:
            count = usage.get_tokens_in_window(window)
        
        return {
            "current": count,
            "limit": limit.limit,
            "window_seconds": window,
            "remaining": max(0, limit.limit - count),
        }
    
    def cleanup(self) -> None:
        """Cleanup old entries."""
        max_age = 86400 * 2  # 2 days
        
        with self._lock:
            for usage in self.usage.values():
                usage.cleanup_old_entries(max_age)
    
    def stop(self) -> None:
        """Dừng background cleanup thread."""
        self._running = False


class QuotaExceededError(Exception):
    """Exception raised khi quota bị exceeded."""
    pass
```

## Common Patterns (Các Mẫu Thường Dùng)

### 1. Retry Pattern với Exponential Backoff

```python
# src/resilience/retry_handler.py
"""
Retry handler với exponential backoff cho Gemini API calls
"""

import time
import asyncio
from typing import TypeVar, Callable, Optional, List, Type
from functools import wraps
import logging

from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable, DeadlineExceeded

logger = logging.getLogger(__name__)

T = TypeVar('T')


class RetryConfig:
    """Cấu hình cho retry logic."""
    
    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        retryable_exceptions: Optional[List[Type[Exception]]] = None,
    ):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.retryable_exceptions = retryable_exceptions or [
            ResourceExhausted,
            ServiceUnavailable,
            DeadlineExceeded,
        ]


def with_retry(config: Optional[RetryConfig] = None):
    """
    Decorator để thêm retry logic cho một function.
    
    Usage:
        @with_retry(RetryConfig(max_retries=5))
        async def call_gemini_api():
            ...
    """
    if config is None:
        config = RetryConfig()
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(config.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except tuple(config.retryable_exceptions) as e:
                    last_exception = e
                    
                    if attempt == config.max_retries:
                        logger.error(
                            f"Max retries ({config.max_retries}) reached for {func.__name__}"
                        )
                        raise
                    
                    delay = min(
                        config.initial_delay * (config.exponential_base ** attempt),
                        config.max_delay
                    )
                    
                    logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    await asyncio.sleep(delay)
            
            raise last_exception
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(config.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except tuple(config.retryable_exceptions) as e:
                    last_exception = e
                    
                    if attempt == config.max_retries:
                        logger.error(
                            f"Max retries ({config.max_retries}) reached for {func.__name__}"
                        )
                        raise
                    
                    delay = min(
                        config.initial_delay * (config.exponential_base ** attempt),
                        config.max_delay
                    )
                    
                    logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    time.sleep(delay)
            
            raise last_exception
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator


# Usage example
@with_retry(RetryConfig(max_retries=5, initial_delay=2.0))
async def generate_with_retry(model, prompt: str):
    """Example function với retry logic."""
    result = await model.generate_content_async(prompt)
    return result
```

### 2. Circuit Breaker Pattern

```typescript
// src/resilience/circuit-breaker.ts
/**
 * Circuit Breaker implementation cho Gemini API calls
 */

type CircuitState = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

interface CircuitBreakerConfig {
  failureThreshold: number;
  successThreshold: number;
  timeout: number;  // ms
  name: string;
}

export class CircuitBreaker {
  private state: CircuitState = 'CLOSED';
  private failureCount: number = 0;
  private successCount: number = 0;
  private lastFailureTime: number = 0;
  private readonly config: CircuitBreakerConfig;
  
  constructor(config: CircuitBreakerConfig) {
    this.config = {
      failureThreshold: config.failureThreshold || 5,
      successThreshold: config.successThreshold || 2,
      timeout: config.timeout || 60000,  // 1 minute default
      name: config.name || 'default',
    };
  }
  
  async execute<T>(
    fn: () => Promise<T>,
    fallback?: () => Promise<T>
  ): Promise<T> {
    if (this.state === 'OPEN') {
      if (this.shouldAttemptReset()) {
        this.state = 'HALF_OPEN';
      } else {
        if (fallback) {
          return fallback();
        }
        throw new Error(`Circuit breaker OPEN for ${this.config.name}`);
      }
    }
    
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      
      if (fallback) {
        return fallback();
      }
      throw error;
    }
  }
  
  private shouldAttemptReset(): boolean {
    return Date.now() - this.lastFailureTime >= this.config.timeout;
  }
  
  private onSuccess(): void {
    this.failureCount = 0;
    
    if (this.state === 'HALF_OPEN') {
      this.successCount++;
      if (this.successCount >= this.config.successThreshold) {
        this.state = 'CLOSED';
        this.successCount = 0;
        console.log(`Circuit breaker CLOSED for ${this.config.name}`);
      }
    }
  }
  
  private onFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    
    if (this.state === 'HALF_OPEN') {
      this.state = 'OPEN';
      console.log(`Circuit breaker OPEN (half-open failure) for ${this.config.name}`);
    } else if (this.failureCount >= this.config.failureThreshold) {
      this.state = 'OPEN';
      console.log(`Circuit breaker OPEN (threshold reached) for ${this.config.name}`);
    }
  }
  
  getState(): CircuitState {
    return this.state;
  }
  
  reset(): void {
    this.state = 'CLOSED';
    this.failureCount = 0;
    this.successCount = 0;
  }
}

// Usage
const geminiCircuitBreaker = new CircuitBreaker({
  name: 'gemini-api',
  failureThreshold: 5,
  successThreshold: 2,
  timeout: 60000,
});

async function callGeminiWithCircuitBreaker(prompt: string) {
  return geminiCircuitBreaker.execute(
    () => geminiService.generateContent(prompt),
    () => Promise.resolve({ text: 'Fallback response' }) // Return cached/default response
  );
}
```

## Troubleshooting

### 1. Các Lỗi Thường Gặp và Giải Pháp

**Lỗi: "API Key not valid"**

```
Nguyên nhân: API key không hợp lệ hoặc chưa được configure
Giải pháp:
1. Kiểm tra API key có đúng format không (bắt đầu bằng AIza...)
2. Đảm bảo đã gọi genai.configure(api_key=...) 
3. Kiểm tra API key có bị disable không trong Google AI Studio
4. Verify API key còn hạn và có quota còn lại
```

**Lỗi: "Resource has been exhausted"**

```
Nguyên nhân: Đã hết quota cho API
Giải pháp:
1. Kiểm tra quota đã sử dụng trong Google Cloud Console
2. Request tăng quota nếu cần thiết
3. Implement rate limiting ở application level
4. Xem xét sử dụng caching để giảm số lượng API calls
5. Sử dụng batch API cho các tác vụ không urgent
```

**Lỗi: "Request contains invalid argument"**

```
Nguyên nhân: Request payload không đúng format
Giải pháp:
1. Kiểm tra format của prompt
2. Verify các parameters như temperature, top_p có giá trị hợp lệ
3. Đảm bảo safety settings đúng format
4. Kiểm tra model name có đúng không
```

**Lỗi: "Model not found"**

```
Nguyên nhân: Model name không đúng hoặc chưa được enable
Giải pháp:
1. Kiểm tra model name có đúng format không
2. Verify model đã được enable trong Google Cloud Console/AI Studio
3. Kiểm tra region có hỗ trợ model đó không
```

### 2. Debugging Tips

```python
# src/debug/gemini_debug.py
"""
Debug utilities cho Gemini API
"""

import logging
from typing import Any, Dict, Optional
from google.generativeai import types

logging.basicConfig(level=logging.DEBUG)

def log_request_details(
    prompt: str,
    generation_config: Optional[Dict] = None,
    safety_settings: Optional[Dict] = None,
) -> None:
    """Log chi tiết request để debug."""
    logger = logging.getLogger("gemini_debug")
    
    logger.debug("=" * 50)
    logger.debug("GEMINI REQUEST DETAILS")
    logger.debug("=" * 50)
    logger.debug(f"Prompt length: {len(prompt)} chars")
    
    if generation_config:
        logger.debug("Generation Config:")
        for key, value in generation_config.items():
            logger.debug(f"  {key}: {value}")
    
    if safety_settings:
        logger.debug("Safety Settings:")
        for category, threshold in safety_settings.items():
            logger.debug(f"  {category}: {threshold}")
    
    logger.debug("=" * 50)


def log_response_details(response: Any) -> None:
    """Log chi tiết response để debug."""
    logger = logging.getLogger("gemini_debug")
    
    logger.debug("=" * 50)
    logger.debug("GEMINI RESPONSE DETAILS")
    logger.debug("=" * 50)
    
    # Log prompt feedback nếu có
    if hasattr(response, 'prompt_feedback'):
        pf = response.prompt_feedback
        logger.debug(f"Prompt Feedback: {pf}")
        
        if hasattr(pf, 'block_reason') and pf.block_reason:
            logger.warning(f"BLOCKED: {pf.block_reason}")
            if hasattr(pf, 'block_reason_message'):
                logger.warning(f"Block reason message: {pf.block_reason_message}")
    
    # Log candidates
    if hasattr(response, 'candidates') and response.candidates:
        for i, candidate in enumerate(response.candidates):
            logger.debug(f"Candidate {i}:")
            logger.debug(f"  Finish reason: {candidate.finish_reason}")
            
            if candidate.safety_ratings:
                logger.debug("  Safety Ratings:")
                for rating in candidate.safety_ratings:
                    logger.debug(f"    {rating.category}: {rating.probability}")
            
            if candidate.content and candidate.content.parts:
                text = ''.join([p.text for p in candidate.content.parts if hasattr(p, 'text')])
                logger.debug(f"  Response length: {len(text)} chars")
    
    logger.debug("=" * 50)
```

## Examples

### 1. Complete Setup Example - Python Production

```python
# src/main.py
"""
Complete example: Production setup với Gemini API
"""

import os
import logging
from typing import Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import configurations
from src.config.gemini_config import (
    GeminiConfig,
    Platform,
    initialize_gemini,
    create_model,
)
from src.resilience.retry_handler import with_retry, RetryConfig
from src.monitoring.quota_manager import QuotaManager, QuotaLimit, QuotaType

# Initialize configuration
def initialize_app() -> None:
    """Initialize application với tất cả dependencies."""
    
    logger.info("Initializing application...")
    
    # 1. Load configuration
    config = GeminiConfig.from_env()
    logger.info(f"Using platform: {config.platform.value}")
    logger.info(f"Using model: {config.model_name}")
    
    # 2. Initialize Gemini
    initialize_gemini(config)
    model = create_model(config)
    logger.info("Gemini API initialized successfully")
    
    # 3. Setup quota manager
    quota_manager = QuotaManager([
        QuotaLimit(QuotaType.REQUESTS_PER_MINUTE, 60, 60),
        QuotaLimit(QuotaType.REQUESTS_PER_DAY, 10000, 86400),
        QuotaLimit(QuotaType.TOKENS_PER_MINUTE, 1000000, 60),
    ])
    logger.info("Quota manager initialized")
    
    return model, quota_manager


@with_retry(RetryConfig(max_retries=3, initial_delay=1.0))
async def generate_response(model, prompt: str, quota_manager):
    """Generate response với quota checking và retry."""
    
    # Check quota
    quota_manager.check_and_update(QuotaType.REQUESTS_PER_MINUTE)
    
    # Generate response
    response = model.generate_content(prompt)
    
    return response


# Run
if __name__ == "__main__":
    model, quota_manager = initialize_app()
    
    # Example usage
    response = generate_response(
        model,
        "Explain quantum computing in simple terms",
        quota_manager
    )
    
    print(response.text)
```

### 2. Complete Setup Example - TypeScript Production

```typescript
// src/main.ts
/**
 * Complete example: Production setup với Gemini API
 */

import dotenv from 'dotenv';
import { GeminiService } from './services/gemini.service';
import { loadConfigFromEnv } from './config/gemini.config';
import { CircuitBreaker } from './resilience/circuit-breaker';

// Load environment variables
dotenv.config();

// Initialize service
const config = loadConfigFromEnv();
const geminiService = new GeminiService(config);

// Initialize circuit breaker
const circuitBreaker = new CircuitBreaker({
  name: 'gemini-api',
  failureThreshold: 5,
  successThreshold: 2,
  timeout: 60000,
});

async function generateResponse(prompt: string): Promise<string> {
  const result = await circuitBreaker.execute(
    async () => {
      const response = await geminiService.generateContent(prompt);
      return response.response.text();
    },
    async () => {
      // Fallback response when circuit is open
      return 'Service temporarily unavailable. Please try again later.';
    }
  );
  
  return result;
}

// Main execution
async function main() {
  try {
    const response = await generateResponse(
      'What is the difference between AI and machine learning?'
    );
    console.log('Response:', response);
  } catch (error) {
    console.error('Error generating response:', error);
  }
}

main();
```

## References

### Official Documentation

- [Google AI Studio Documentation](https://ai.google.dev/docs)
- [Gemini API Reference](https://ai.google.dev/api/rest)
- [Vertex AI Gemini Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/overview)
- [Python SDK Documentation](https://github.com/google/generativeai-python)
- [Node.js SDK Documentation](https://github.com/google/generative-ai-js)

### Google Cloud Console

- [Google Cloud Console](https://console.cloud.google.com)
- [API Keys Management](https://console.cloud.google.com/apis/credentials)
- [Quota Management](https://console.cloud.google.com/apis/quotas)
- [IAM & Admin](https://console.cloud.google.com/iam-admin)

### Related Rules

- `@core-architecture.mdc` - Nguyên tắc kiến trúc cốt lõi
- `@security.mdc` - Nguyên tắc bảo mật
- `@performance.mdc` - Nguyên tắc tối ưu hiệu suất
- `@openai.mdc` - Best practices cho OpenAI integration (tham khảo)
