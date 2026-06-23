---
title: "Claude 3 Models Comparison"
description: "Hướng dẫn so sánh các Claude 3 models - Haiku, Sonnet, Opus, Sonnet 4 - use case recommendations, cost-performance tradeoffs, selection criteria"
tags: ["claude", "models", "claude-3", "haiku", "sonnet", "opus", "comparison"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Claude 3 Models Comparison

## Tổng quan (Overview)

Anthropic đã phát triển dòng Claude 3 với nhiều models phục vụ các use cases khác nhau, từ những tác vụ đơn giản, nhanh chóng đến những công việc phức tạp đòi hỏi khả năng reasoning cao cấp. Việc hiểu rõ sự khác biệt giữa các models và biết cách chọn đúng model cho từng tác vụ là yếu tố then chốt để xây dựng ứng dụng AI hiệu quả và tiết kiệm chi phí.

Trong môi trường enterprise, nơi mà chi phí có thể tích lũy nhanh chóng và chất lượng output ảnh hưởng trực tiếp đến trải nghiệm người dùng, việc nắm vững cách sử dụng từng model một cách tối ưu là kỹ năng không thể thiếu.

Tài liệu này cung cấp so sánh chi tiết giữa các Claude 3 models, hướng dẫn chọn model phù hợp, và các best practices để tối ưu hóa chi phí và hiệu suất.

## Mục đích (Purpose)

Mục tiêu chính của tài liệu này bao gồm:

1. **Hiểu đặc điểm từng model** - Haiku, Sonnet, Opus, và Sonnet 4
2. **Biết cách chọn model phù hợp** - Selection criteria cho từng use case
3. **Tối ưu chi phí** - Cost-performance tradeoff analysis
4. **Implement model selection** - Auto-selection và routing patterns
5. **Best practices** - Khi nào nên upgrade hoặc downgrade models

## Khái niệm cốt lõi (Key Concepts)

### 1. Model Tiers

```
┌─────────────────────────────────────────────────────────────────┐
│                    MODEL CAPABILITY TIERS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    OPUS TIER                             │   │
│  │  • Complex reasoning, analysis                          │   │
│  │  • Long-context tasks                                   │   │
│  │  • Nuanced, detailed outputs                            │   │
│  │  • Code generation (complex)                             │   │
│  │  • Strategic planning                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ▲                                     │
│                            │ Higher Cost                        │
│                            │ Better Quality                     │
│                            │                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  SONNET TIER (3.5)                      │   │
│  │  • Balanced performance/cost                           │   │
│  │  • Most common use cases                                │   │
│  │  • Good coding capabilities                             │   │
│  │  • Versatile                                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ▲                                     │
│                            │ Lower Cost                          │
│                            │ Fast Response                       │
│                            │                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   HAIKU TIER                             │   │
│  │  • Simple, fast tasks                                   │   │
│  │  • Classification, extraction                           │   │
│  │  • High-volume, low-latency needs                       │   │
│  │  • Cost-sensitive applications                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Benchmark Categories

| Category | Description |
|----------|-------------|
| Reasoning | Logical deduction, problem-solving |
| Coding | Code generation, debugging, explanation |
| Knowledge | Factual recall, comprehension |
| Writing | Content creation, editing, summarization |
| Math | Mathematical calculations, proofs |
| Safety | Harmful content detection, ethical responses |

## Model Specifications

### 1. Claude 3.5 Sonnet (20241022)

```python
CLAUDE_3_5_SONNET_CONFIG = {
    "name": "claude-3-5-sonnet-20241022",
    "display_name": "Claude 3.5 Sonnet",
    
    # Capabilities
    "context_window": 200000,  # 200K tokens
    "max_output_tokens": 4096,
    
    # Performance characteristics
    "speed": "fast",  # 5x faster than Opus for many tasks
    "intelligence": "high",
    "cost_efficiency": "excellent",
    
    # Strengths
    "strengths": [
        "Balanced performance across all tasks",
        "Excellent coding capabilities",
        "Fast response time",
        "Cost-effective for most use cases",
        "Strong reasoning abilities",
        "Good at following complex instructions",
    ],
    
    # Best for
    "best_for": [
        "General-purpose applications",
        "Customer service chatbots",
        "Code generation and review",
        "Content creation",
        "Data analysis and insights",
        "Multi-step task completion",
    ],
    
    # Pricing (example, check current rates)
    "pricing": {
        "input_tokens_per_million": 3.0,  # USD
        "output_tokens_per_million": 15.0,  # USD
    }
}
```

### 2. Claude 3 Opus (20240229)

```python
CLAUDE_3_OPUS_CONFIG = {
    "name": "claude-3-opus-20240229",
    "display_name": "Claude 3 Opus",
    
    # Capabilities
    "context_window": 200000,  # 200K tokens
    "max_output_tokens": 4096,
    
    # Performance characteristics
    "speed": "slow",  # Most capable but slower
    "intelligence": "highest",
    "cost_efficiency": "lower",  # Best quality at higher cost
    
    # Strengths
    "strengths": [
        "Highest intelligence and reasoning",
        "Best for complex, nuanced tasks",
        "Superior coding capabilities",
        "Handles ambiguity well",
        "Excellent for research and analysis",
        "Most reliable instruction following",
    ],
    
    # Best for
    "best_for": [
        "Complex research tasks",
        "High-stakes decision making",
        "Advanced code generation",
        "Long-form content creation",
        "Strategic planning",
        "Legal and financial analysis",
    ],
    
    # Pricing (example)
    "pricing": {
        "input_tokens_per_million": 15.0,  # USD
        "output_tokens_per_million": 75.0,  # USD
    }
}
```

### 3. Claude 3.5 Haiku (20241022)

```python
CLAUDE_3_5_HAIKU_CONFIG = {
    "name": "claude-3-5-haiku-20241022",
    "display_name": "Claude 3.5 Haiku",
    
    # Capabilities
    "context_window": 200000,  # 200K tokens
    "max_output_tokens": 4096,
    
    # Performance characteristics
    "speed": "fastest",  # Near-instant responses
    "intelligence": "good",  # Sufficient for many tasks
    "cost_efficiency": "excellent",  # Most cost-effective
    
    # Strengths
    "strengths": [
        "Lowest latency, fastest responses",
        "Most cost-effective option",
        "Excellent for classification",
        "Good for simple extractions",
        "High-volume applications",
        "Real-time interactions",
    ],
    
    # Weaknesses
    "weaknesses": [
        "Less capable for complex reasoning",
        "May struggle with nuanced tasks",
        "Not ideal for long-form content",
        "Limited for advanced coding",
    ],
    
    # Best for
    "best_for": [
        "High-volume, simple queries",
        "Text classification",
        "Sentiment analysis",
        "Entity extraction",
        "Simple Q&A",
        "Real-time chatbots",
        "Auto-completion",
    ],
    
    # Pricing (example)
    "pricing": {
        "input_tokens_per_million": 0.25,  # USD
        "output_tokens_per_million": 1.25,  # USD
    }
}
```

## Use Case Recommendations

### 1. Decision Matrix

| Use Case | Recommended Model | Alternative | Notes |
|----------|------------------|-------------|-------|
| Customer Support Bot | Haiku hoặc Sonnet 3.5 | - | Haiku cho simple queries, Sonnet cho complex |
| Code Generation | Sonnet 3.5 | Opus | Sonnet đủ cho hầu hết, Opus cho extremely complex |
| Code Review | Sonnet 3.5 hoặc Opus | - | Opus cho security-critical reviews |
| Document Summarization | Sonnet 3.5 | Haiku (short docs) | Sonnet cho nuanced summaries |
| Long Document Analysis | Opus hoặc Sonnet 3.5 | - | Opus tốt hơn cho very long docs |
| Classification | Haiku | Sonnet 3.5 | Haiku đủ cho simple classification |
| Data Extraction | Haiku hoặc Sonnet 3.5 | - | Sonnet cho complex/nested extraction |
| Content Generation | Sonnet 3.5 | Opus (creative) | Sonnet balanced, Opus cho high-quality |
| Research Analysis | Opus | Sonnet 3.5 | Opus cho comprehensive analysis |
| Real-time Chat | Haiku | Sonnet 3.5 | Haiku cho instant responses |

### 2. Implementation Examples

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class ModelRecommendation:
    model: str
    confidence: float
    reasoning: str
    cost_efficiency: str


class ModelSelector:
    """Intelligent model selector cho different tasks."""
    
    # Cost multiplier (relative to Haiku)
    COST_MULTIPLIERS = {
        "claude-3-5-haiku-20241022": 1.0,
        "claude-3-5-sonnet-20241022": 12.0,
        "claude-3-opus-20240229": 60.0,
    }
    
    def recommend(
        self,
        task_type: str,
        complexity: Literal["low", "medium", "high"],
        urgency: Literal["low", "medium", "high"],
        budget_sensitivity: Literal["low", "medium", "high"],
    ) -> ModelRecommendation:
        """Recommend model based on task characteristics."""
        
        # Classification - always use Haiku unless complex
        if task_type == "classification":
            if complexity == "low":
                return ModelRecommendation(
                    model="claude-3-5-haiku-20241022",
                    confidence=0.95,
                    reasoning="Simple classification tasks are well-handled by Haiku",
                    cost_efficiency="excellent"
                )
        
        # Code generation - need Sonnet or Opus
        if task_type == "code_generation":
            if complexity in ["low", "medium"]:
                return ModelRecommendation(
                    model="claude-3-5-sonnet-20241022",
                    confidence=0.9,
                    reasoning="Sonnet handles most code generation efficiently",
                    cost_efficiency="good"
                )
            else:
                return ModelRecommendation(
                    model="claude-3-opus-20240229",
                    confidence=0.85,
                    reasoning="Complex code generation benefits from Opus intelligence",
                    cost_efficiency="moderate"
                )
        
        # Research/analysis - need Opus
        if task_type in ["research", "analysis", "strategic_planning"]:
            return ModelRecommendation(
                model="claude-3-opus-20240229",
                confidence=0.9,
                reasoning=f"{task_type} tasks require highest intelligence",
                cost_efficiency="low"
            )
        
        # Default: Sonnet for balanced needs
        return ModelRecommendation(
            model="claude-3-5-sonnet-20241022",
            confidence=0.85,
            reasoning="Sonnet provides balanced performance for general tasks",
            cost_efficiency="good"
        )
```

### 3. TypeScript Model Selector

```typescript
export type TaskType = 
  | 'classification'
  | 'extraction'
  | 'code_generation'
  | 'code_review'
  | 'summarization'
  | 'content_generation'
  | 'research'
  | 'analysis'
  | 'chat'
  | 'general';

export type Complexity = 'low' | 'medium' | 'high';
export type BudgetSensitivity = 'low' | 'medium' | 'high';

interface ModelRecommendation {
  model: string;
  confidence: number;
  reasoning: string;
  estimatedCost: 'very_low' | 'low' | 'medium' | 'high' | 'very_high';
}

const MODEL_COSTS = {
  'claude-3-5-haiku-20241022': 0.25,
  'claude-3-5-sonnet-20241022': 3.0,
  'claude-3-opus-20240229': 15.0,
};

export class ModelSelector {
  recommend(
    taskType: TaskType,
    complexity: Complexity,
    budgetSensitivity: BudgetSensitivity
  ): ModelRecommendation {
    // Fast path for simple tasks
    if (taskType === 'classification' && complexity === 'low') {
      return {
        model: 'claude-3-5-haiku-20241022',
        confidence: 0.95,
        reasoning: 'Haiku excels at simple classification at lowest cost',
        estimatedCost: 'very_low'
      };
    }

    // High-value tasks justify Opus
    if (taskType === 'research' || taskType === 'analysis') {
      if (budgetSensitivity === 'low') {
        return {
          model: 'claude-3-opus-20240229',
          confidence: 0.9,
          reasoning: 'Research tasks require Opus intelligence',
          estimatedCost: 'high'
        };
      } else {
        return {
          model: 'claude-3-5-sonnet-20241022',
          confidence: 0.8,
          reasoning: 'Sonnet provides good analysis at lower cost',
          estimatedCost: 'medium'
        };
      }
    }

    // Code generation
    if (taskType === 'code_generation') {
      if (complexity === 'high') {
        return {
          model: 'claude-3-opus-20240229',
          confidence: 0.85,
          reasoning: 'Complex code benefits from Opus capabilities',
          estimatedCost: 'high'
        };
      }
      return {
        model: 'claude-3-5-sonnet-20241022',
        confidence: 0.9,
        reasoning: 'Sonnet handles most coding tasks efficiently',
        estimatedCost: 'medium'
      };
    }

    // Default fallback
    return {
      model: 'claude-3-5-sonnet-20241022',
      confidence: 0.85,
      reasoning: 'Sonnet balances intelligence and cost',
      estimatedCost: 'medium'
    };
  }
}
```

## Cost-Performance Tradeoffs

### 1. Cost Analysis

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class CostAnalysis:
    """Cost analysis for different models."""
    
    model: str
    input_cost_per_1m: float
    output_cost_per_1m: float
    
    # Typical usage patterns
    average_input_tokens: int = 500
    average_output_tokens: int = 200
    
    @property
    def cost_per_request(self) -> float:
        """Calculate cost per request."""
        input_cost = (self.average_input_tokens / 1_000_000) * self.input_cost_per_1m
        output_cost = (self.average_output_tokens / 1_000_000) * self.output_cost_per_1m
        return input_cost + output_cost
    
    @property
    def requests_per_dollar(self) -> float:
        """Calculate how many requests per $1."""
        return 1 / self.cost_per_request if self.cost_per_request > 0 else 0


def generate_cost_comparison() -> dict:
    """Generate cost comparison between models."""
    
    models = {
        "Haiku": CostAnalysis(
            model="claude-3-5-haiku-20241022",
            input_cost_per_1m=0.25,
            output_cost_per_1m=1.25
        ),
        "Sonnet 3.5": CostAnalysis(
            model="claude-3-5-sonnet-20241022",
            input_cost_per_1m=3.0,
            output_cost_per_1m=15.0
        ),
        "Opus": CostAnalysis(
            model="claude-3-opus-20240229",
            input_cost_per_1m=15.0,
            output_cost_per_1m=75.0
        ),
    }
    
    comparison = {}
    for name, analysis in models.items():
        comparison[name] = {
            "model": analysis.model,
            "cost_per_request": f"${analysis.cost_per_request:.4f}",
            "requests_per_dollar": f"{analysis.requests_per_dollar:.0f}",
            "cost_ratio": f"{analysis.cost_per_request / models['Haiku'].cost_per_request:.1f}x",
        }
    
    return comparison
```

### 2. Performance vs Cost Matrix

```python
# Performance ratings (1-5 scale)
PERFORMANCE_RATINGS = {
    "claude-3-5-haiku-20241022": {
        "classification": 5,      # Excellent
        "extraction": 4,          # Very good
        "simple_qa": 5,          # Excellent
        "summarization": 3,      # Good for short
        "code_generation": 3,    # Adequate
        "complex_reasoning": 2,  # Limited
        "creative_writing": 3,   # Adequate
        "analysis": 2,           # Limited
    },
    "claude-3-5-sonnet-20241022": {
        "classification": 5,      # Excellent
        "extraction": 5,         # Excellent
        "simple_qa": 5,          # Excellent
        "summarization": 5,      # Excellent
        "code_generation": 5,    # Excellent
        "complex_reasoning": 4,  # Very good
        "creative_writing": 5,  # Excellent
        "analysis": 4,           # Very good
    },
    "claude-3-opus-20240229": {
        "classification": 5,      # Excellent
        "extraction": 5,          # Excellent
        "simple_qa": 5,          # Excellent
        "summarization": 5,      # Excellent
        "code_generation": 5,    # Excellent
        "complex_reasoning": 5,  # Excellent
        "creative_writing": 5,   # Excellent
        "analysis": 5,           # Excellent
    },
}


def calculate_value_score(
    task_type: str,
    model: str,
    budget_weight: float = 0.5  # 0 = quality, 1 = cost
) -> float:
    """Calculate value score balancing quality and cost."""
    
    performance = PERFORMANCE_RATINGS.get(model, {}).get(task_type, 1)
    
    # Normalize to 0-1
    performance_score = performance / 5.0
    
    # Cost score (inverse, normalized)
    costs = {
        "claude-3-5-haiku-20241022": 0.1,
        "claude-3-5-sonnet-20241022": 0.5,
        "claude-3-opus-20240229": 1.0,
    }
    cost_score = 1 - costs.get(model, 0.5)
    
    # Weighted value
    return (1 - budget_weight) * performance_score + budget_weight * cost_score
```

## Model Selection Patterns

### 1. Cascading Model Selection

```python
class CascadingModelSelector:
    """Try cheaper model first, escalate if needed."""
    
    def __init__(self, client: Anthropic):
        self.client = client
        self.primary_model = "claude-3-5-haiku-20241022"
        self.fallback_model = "claude-3-5-sonnet-20241022"
        self.escalation_model = "claude-3-opus-20240229"
        
        # Thresholds
        self.confidence_threshold = 0.7
    
    async def generate_with_cascade(
        self,
        prompt: str,
        task_type: str,
        max_cost_level: Literal["low", "medium", "high"] = "high"
    ) -> dict:
        """Generate response with cascading model selection."""
        
        models_to_try = []
        
        if max_cost_level in ["low", "medium", "high"]:
            models_to_try.append(self.primary_model)
        if max_cost_level in ["medium", "high"]:
            models_to_try.append(self.fallback_model)
        if max_cost_level == "high":
            models_to_try.append(self.escalation_model)
        
        last_error = None
        
        for model in models_to_try:
            try:
                response = await self._attempt_generate(model, prompt)
                
                # Check if response quality is acceptable
                quality_score = self._assess_quality(response, task_type)
                
                if quality_score >= self.confidence_threshold:
                    return {
                        "response": response,
                        "model_used": model,
                        "quality_score": quality_score,
                        "cascade_level": models_to_try.index(model) + 1
                    }
                
                # Continue to better model if quality insufficient
                continue
                
            except Exception as e:
                last_error = e
                continue
        
        # All models failed
        raise ModelSelectionError(
            f"Failed with all models. Last error: {last_error}"
        )
    
    async def _attempt_generate(self, model: str, prompt: str) -> str:
        """Attempt generation with specific model."""
        response = await self.client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    def _assess_quality(self, response: str, task_type: str) -> float:
        """Assess response quality (simplified)."""
        
        # Basic heuristics
        score = 0.5
        
        if len(response) < 10:
            score -= 0.2
        elif len(response) > 100:
            score += 0.2
        
        if "?" not in response and task_type == "qa":
            score -= 0.1
        
        # Add more sophisticated checks as needed
        return min(1.0, max(0.0, score))
```

### 2. Task Router

```python
from dataclasses import dataclass

@dataclass
class TaskConfig:
    model: str
    max_tokens: int
    temperature: float

class TaskRouter:
    """Route tasks to appropriate models based on analysis."""
    
    TASK_CONFIGS = {
        "quick_classify": TaskConfig(
            model="claude-3-5-haiku-20241022",
            max_tokens=50,
            temperature=0.0
        ),
        "moderate_extraction": TaskConfig(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            temperature=0.1
        ),
        "code_review": TaskConfig(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            temperature=0.3
        ),
        "complex_analysis": TaskConfig(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            temperature=0.7
        ),
        "creative_generation": TaskConfig(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            temperature=0.9
        ),
    }
    
    def __init__(self, client: Anthropic):
        self.client = client
    
    async def route_and_execute(
        self,
        task_type: str,
        prompt: str,
        context: dict | None = None
    ) -> dict:
        """Analyze task and route to appropriate model."""
        
        # Analyze task if not explicitly specified
        if task_type == "auto":
            task_type = await self._analyze_task(prompt, context)
        
        config = self.TASK_CONFIGS.get(task_type)
        
        if not config:
            # Default fallback
            config = TaskConfig(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                temperature=0.7
            )
        
        # Build messages
        messages = []
        if context and context.get("system"):
            messages.append({"role": "system", "content": context["system"]})
        messages.append({"role": "user", "content": prompt})
        
        # Execute
        start_time = time.time()
        response = await self.client.messages.create(
            model=config.model,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            messages=messages
        )
        
        return {
            "response": response.content[0].text,
            "model": config.model,
            "task_type": task_type,
            "latency_ms": int((time.time() - start_time) * 1000),
            "usage": response.usage
        }
    
    async def _analyze_task(self, prompt: str, context: dict | None) -> str:
        """Use Claude to analyze and categorize the task."""
        
        response = await self.client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=50,
            messages=[{
                "role": "user",
                "content": f"""Analyze this task and categorize it.
                Categories: quick_classify, moderate_extraction, code_review, 
                complex_analysis, creative_generation
                
                Task: {prompt}
                
                Category:"""
            }]
        )
        
        return response.content[0].text.strip().lower()
```

## Best Practices

### 1. When to Use Each Model

```python
# HAIKU - Use when:
HAIKU_USE_CASES = """
Use Claude 3.5 Haiku when:
✓ High volume, simple queries
✓ Classification tasks (sentiment, intent, topic)
✓ Simple entity extraction
✓ Real-time chat with strict latency requirements
✓ First-pass filtering
✓ Auto-completion
✓ Token-sensitive applications

Avoid Haiku when:
✗ Complex reasoning required
✗ Nuanced content generation
✗ Multi-step problem solving
✗ Ambiguous inputs
✗ Critical decisions
"""

# SONNET - Use when:
SONNET_USE_CASES = """
Use Claude 3.5 Sonnet when:
✓ Most production applications
✓ Code generation and review
✓ Content creation
✓ Multi-step task completion
✓ Balanced intelligence and cost
✓ Most common use cases
✓ Versatile requirements

Sonnet is your default choice for:
• Customer support
• Document processing
• General Q&A
• Tool use applications
• APIs and integrations
"""

# OPUS - Use when:
OPUS_USE_CASES = """
Use Claude 3 Opus when:
✓ Research and analysis
✓ Strategic planning
✓ Complex legal/financial documents
✓ Long-context tasks
✓ High-stakes decisions
✓ Nuanced creative writing
✓ When quality > cost

Consider Opus for:
• R&D applications
• Executive summaries
• Complex code architecture
• Academic research
• Critical business decisions
• Comprehensive analysis
"""
```

### 2. Cost Optimization Strategies

```python
class CostOptimizer:
    """Strategies to optimize Claude API costs."""
    
    @staticmethod
    def use_haiku_for_routing(prompt: str) -> str:
        """Use Haiku to classify if request needs Sonnet/Opus."""
        
        client = Anthropic()
        
        classification = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=20,
            messages=[{
                "role": "user",
                "content": f"""Classify this query:
                - simple: basic Q&A, classification, short responses
                - moderate: code generation, content creation, analysis
                - complex: research, strategic planning, nuanced tasks
                
                Query: {prompt}
                
                Classification:"""
            }]
        )
        
        return classification.content[0].text.strip().lower()
    
    @staticmethod
    def batch_similar_requests(requests: list[dict]) -> list[dict]:
        """Batch similar requests to save on overhead."""
        
        # Group by approximate token count
        batches = {
            "small": [],   # < 500 tokens
            "medium": [],  # 500-2000 tokens
            "large": [],   # > 2000 tokens
        }
        
        for req in requests:
            estimated_tokens = len(req.get("content", "")) // 4
            if estimated_tokens < 500:
                batches["small"].append(req)
            elif estimated_tokens < 2000:
                batches["medium"].append(req)
            else:
                batches["large"].append(req)
        
        return batches
    
    @staticmethod
    def cache_common_responses(prompt: str, response: str):
        """Cache common prompts and responses."""
        
        # Use LRU cache with prompt hash
        cache = {}
        
        prompt_hash = hash(prompt)
        if prompt_hash in cache:
            return cache[prompt_hash]
        
        cache[prompt_hash] = response
        return None
```

### 3. Model Switching Logic

```python
class AdaptiveModelSwitcher:
    """Switch models based on runtime conditions."""
    
    def __init__(self):
        self.current_load = 0
        self.budget_remaining = 1000.0  # USD
        self.performance_mode = "balanced"
    
    def select_model(
        self,
        task_complexity: str,
        latency_requirement: float,
        budget_per_request: float
    ) -> str:
        """Select optimal model based on conditions."""
        
        # Check budget first
        if self.budget_remaining < 0.1:
            return "claude-3-5-haiku-20241022"
        
        # Check latency requirements
        if latency_requirement < 1.0:  # seconds
            return "claude-3-5-haiku-20241022"
        
        # Check complexity
        if task_complexity == "high":
            if self.performance_mode == "quality" and budget_per_request > 0.05:
                return "claude-3-opus-20240229"
            return "claude-3-5-sonnet-20241022"
        
        # Default to Sonnet for moderate tasks
        return "claude-3-5-sonnet-20241022"
    
    def update_conditions(self, usage: dict):
        """Update conditions after request."""
        
        self.budget_remaining -= usage.get("cost", 0)
        
        # Simple load calculation
        if usage.get("latency_ms", 0) > 5000:
            self.current_load = min(100, self.current_load + 10)
        else:
            self.current_load = max(0, self.current_load - 5)
```

## Troubleshooting

### Common Model Selection Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Poor quality outputs | Using Haiku for complex tasks | Upgrade to Sonnet or Opus |
| High costs | Overusing Opus | Use Sonnet for most tasks |
| Slow responses | Using Opus for simple tasks | Use Haiku for quick tasks |
| Inconsistent results | Wrong temperature settings | Adjust temperature per task |
| Truncated outputs | max_tokens too low | Increase based on expected output |

### Model Performance Debugging

```python
class ModelPerformanceMonitor:
    """Monitor và debug model performance."""
    
    def __init__(self):
        self.metrics: dict[str, list] = {
            "haiku": [],
            "sonnet": [],
            "opus": []
        }
    
    def record_request(
        self,
        model: str,
        task_type: str,
        quality_score: float,
        latency_ms: float,
        tokens_used: int
    ):
        """Record metrics for a request."""
        
        model_key = model.split("-")[2]  # haiku, sonnet, opus
        if model_key not in self.metrics:
            model_key = "sonnet"  # default
        
        self.metrics[model_key].append({
            "task_type": task_type,
            "quality": quality_score,
            "latency": latency_ms,
            "tokens": tokens_used,
            "timestamp": datetime.now()
        })
    
    def get_recommendations(self) -> dict:
        """Get model recommendations based on metrics."""
        
        recommendations = {}
        
        for model, records in self.metrics.items():
            if not records:
                continue
            
            avg_quality = sum(r["quality"] for r in records) / len(records)
            avg_latency = sum(r["latency"] for r in records) / len(records)
            
            recommendations[model] = {
                "avg_quality": avg_quality,
                "avg_latency": avg_latency,
                "suggested_use": self._suggest_use(avg_quality, avg_latency)
            }
        
        return recommendations
    
    def _suggest_use(self, quality: float, latency: float) -> str:
        """Suggest use case based on performance."""
        
        if quality > 0.9 and latency > 3000:
            return "Complex tasks, research, high-quality generation"
        elif quality > 0.8 and latency < 1500:
            return "Balanced tasks, general production use"
        elif latency < 500:
            return "Simple tasks, classification, high-volume"
        else:
            return "Moderate complexity tasks"
```

## References

- [Claude Model Comparison](https://docs.anthropic.com/claude/docs/models-overview)
- [Model Pricing](https://www.anthropic.com/pricing)
- [Choosing the Right Model](https://docs.anthropic.com/claude/docs/model-selection)
- [Performance Benchmarks](https://www.anthropic.com/benchmarks)
