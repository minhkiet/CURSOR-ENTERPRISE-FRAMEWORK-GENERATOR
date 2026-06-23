---
title: "Claude API Decision Tree"
description: "Cây quyết định cho Claude API - model selection, tool use strategy, context management, parameter tuning, feature adoption, và production deployment decisions"
tags: ["claude", "decision-tree", "api", "anthropic", "model-selection", "tool-use", "context-management"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Claude API Decision Tree

## Tổng quan (Overview)

Decision trees là visual và logical frameworks giúp developers make informed decisions trong quá trình tích hợp Claude API. Mỗi decision tree address một specific area: model selection, tool use strategy, context management, parameter tuning, feature adoption, và production deployment.

Thay vì prescribing single "right answers", decision trees cung cấp structured approach để evaluate options dựa trên specific criteria và constraints. Users follow branching logic từ starting point through relevant considerations đến recommendations.

Tài liệu này được thiết kế như một practical reference - sử dụng khi facing specific decisions, không cần đọc tuần tự. Các trees được independent và có thể reference standalone.

## Mục đích (Purpose)

Mục tiêu chính của decision trees này bao gồm:

1. **Guide decisions** - Provide structured logic cho complex choices
2. **Reduce trial-and-error** - Leverage established patterns
3. **Support reasoning** - Make decision process explicit
4. **Enable consistency** - Standardize decision-making across team

## Decision Tree 1: Model Selection

### When to Use This Tree

Sử dụng decision tree này khi:

- Starting new Claude integration project
- Selecting model cho new feature
- Re-evaluating current model choices
- Optimizing cost-quality balance
- Choosing between models for different use cases

### Model Selection Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│                 MODEL SELECTION DECISION TREE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  START: What type of task?                                       │
│                                                                 │
│  ├─── CLASSIFICATION / EXTRACTION ──────────────────────────────┐│
│  │                                                            ││
│  │    Is task simple binary classification?                    ││
│  │    ├── YES ──→ Use Claude 3.5 Haiku                        ││
│  │    │        (lowest cost, sufficient accuracy)             ││
│  │    │                                                        ││
│  │    NO                                                       ││
│  │    │                                                        ││
│  │    Does task require nuanced understanding?                 ││
│  │    ├── YES ──→ Use Claude 3.5 Sonnet                       ││
│  │    │        (better classification accuracy)               ││
│  │    │                                                        ││
│  │    NO ──→ Use Claude 3.5 Haiku                              ││
│  │         (simple multi-class is fine with Haiku)            ││
│  │                                                            ││
│  └─── GENERAL PURPOSE / Q&A ───────────────────────────────────┘│
│                                                                 │
│  │                                                            │
│  │    Is response quality critical?                            │
│  │    ├── YES ──→ Is latency important?                       ││
│  │    │        ├── YES ──→ Use Claude 3.5 Sonnet              ││
│  │    │        │        (balance quality and speed)           ││
│  │    │        │                                                ││
│  │    │        NO ──→ Use Claude 3 Opus                        ││
│  │    │               (highest quality for critical tasks)    ││
│  │    │                                                        ││
│  │    NO ──→ Use Claude 3.5 Sonnet                             ││
│  │         (default choice for most applications)            ││
│  │                                                            ││
│  └─── CODE GENERATION ──────────────────────────────────────────┘│
│                                                                 │
│  │                                                            │
│  │    Is codebase complex/large?                               │
│  │    ├── YES ──→ Use Claude 3.5 Sonnet or Opus               ││
│  │    │        (Sonnet for most, Opus for extremely complex) ││
│  │    │                                                        ││
│  │    NO ──→ Use Claude 3.5 Sonnet                             ││
│  │         (good enough for simple code tasks)               ││
│  │                                                            ││
│  └─── CREATIVE WRITING ────────────────────────────────────────┘│
│                                                                 │
│  │                                                            │
│  │    Is creative uniqueness important?                        │
│  │    ├── YES ──→ Increase temperature (0.8-1.0)              ││
│  │    │        Use Claude 3.5 Sonnet                           ││
│  │    │                                                        ││
│  │    NO ──→ Lower temperature (0.3-0.5)                      ││
│  │         Use Claude 3.5 Sonnet                               ││
│  │                                                            ││
│  └─── RESEARCH / ANALYSIS ─────────────────────────────────────┘│
│                                                                 │
│  │                                                            │
│  │    Is this high-stakes decision?                            │
│  │    ├── YES ──→ Use Claude 3 Opus                           ││
│  │    │        (best reasoning, thorough analysis)            ││
│  │    │                                                        ││
│  │    NO ──→ Use Claude 3.5 Sonnet                             ││
│  │         (sufficient for most analysis tasks)               ││
│  │                                                            ││
└─────────────────────────────────────────────────────────────────┘
```

### Model Selection Matrix

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MODEL SELECTION MATRIX                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TASK COMPLEXITY    │    LOW COST    │   BALANCED   │  HIGH QUALITY   │
│  ────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  Simple (classify, │                │              │                  │
│  extract, tag)     │   Haiku ★★★    │  Sonnet ★★   │  Opus ★        │
│                    │   (optimal)    │              │                  │
│                    │                │              │                  │
│  Medium (summarize,│                │              │                  │
│  translate, write) │   Haiku ★     │  Sonnet ★★★  │  Opus ★★       │
│                    │                │   (optimal)  │                  │
│                    │                │              │                  │
│  Complex (analyze, │                │              │                  │
│  reason, plan)     │   Haiku ★     │  Sonnet ★★   │  Opus ★★★      │
│                    │                │              │   (optimal)     │
│                    │                │              │                  │
│  Creative (stories,│                │              │                  │
│  marketing copy)   │   Haiku ★     │  Sonnet ★★★  │  Opus ★★       │
│                    │                │   (optimal)  │                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

LEGEND:
★ = Usable but not optimal
★★ = Good choice
★★★ = Recommended for this complexity level
```

### Model Selection Code

```python
from dataclasses import dataclass
from enum import Enum
from typing import Literal

class TaskComplexity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class CostSensitivity(Enum):
    LOW = "low"      # Quality > Cost
    MEDIUM = "medium"
    HIGH = "high"    # Cost > Quality

@dataclass
class ModelRecommendation:
    model: str
    reasoning: str
    estimated_cost_level: Literal["low", "medium", "high"]
    quality_level: Literal["low", "medium", "high"]

class ModelSelector:
    """Decision tree implementation for model selection."""
    
    def select_model(
        self,
        task_type: str,
        complexity: TaskComplexity,
        cost_sensitivity: CostSensitivity,
        latency_requirement: float = 5.0  # seconds
    ) -> ModelRecommendation:
        """
        Select appropriate model based on decision tree logic.
        
        Args:
            task_type: Type of task (classification, code, creative, etc.)
            complexity: Task complexity level
            cost_sensitivity: How cost-sensitive is the use case
            latency_requirement: Maximum acceptable latency in seconds
        """
        
        # Classification/Extraction path
        if task_type in ["classification", "extraction", "tagging"]:
            return self._handle_classification(complexity, cost_sensitivity)
        
        # Code generation path
        if task_type in ["code_generation", "code_review", "debugging"]:
            return self._handle_coding(complexity, cost_sensitivity)
        
        # Creative writing path
        if task_type in ["creative_writing", "marketing", "content"]:
            return self._handle_creative(complexity, cost_sensitivity)
        
        # Research/Analysis path
        if task_type in ["research", "analysis", "planning"]:
            return self._handle_research(complexity, cost_sensitivity)
        
        # General purpose - default to Sonnet
        return ModelRecommendation(
            model="claude-3-5-sonnet-20241022",
            reasoning="Default choice for general purpose tasks",
            estimated_cost_level="medium",
            quality_level="high"
        )
    
    def _handle_classification(
        self,
        complexity: TaskComplexity,
        cost_sensitivity: CostSensitivity
    ) -> ModelRecommendation:
        
        if complexity == TaskComplexity.LOW:
            return ModelRecommendation(
                model="claude-3-5-haiku-20241022",
                reasoning="Simple classification - Haiku sufficient at lowest cost",
                estimated_cost_level="low",
                quality_level="medium"
            )
        
        if cost_sensitivity == CostSensitivity.HIGH:
            return ModelRecommendation(
                model="claude-3-5-haiku-20241022",
                reasoning="Nuanced but cost-sensitive - Haiku with careful prompt",
                estimated_cost_level="low",
                quality_level="medium"
            )
        
        return ModelRecommendation(
            model="claude-3-5-sonnet-20241022",
            reasoning="Complex or quality-critical classification - Sonnet recommended",
            estimated_cost_level="medium",
            quality_level="high"
        )
    
    def _handle_coding(
        self,
        complexity: TaskComplexity,
        cost_sensitivity: CostSensitivity
    ) -> ModelRecommendation:
        
        if complexity == TaskComplexity.LOW:
            return ModelRecommendation(
                model="claude-3-5-sonnet-20241022",
                reasoning="Simple code tasks - Sonnet is good and cost-effective",
                estimated_cost_level="medium",
                quality_level="high"
            )
        
        if complexity == TaskComplexity.HIGH and cost_sensitivity == CostSensitivity.LOW:
            return ModelRecommendation(
                model="claude-3-opus-20240229",
                reasoning="Complex code with quality priority - Opus for best results",
                estimated_cost_level="high",
                quality_level="high"
            )
        
        return ModelRecommendation(
            model="claude-3-5-sonnet-20241022",
            reasoning="Standard choice for most coding tasks",
            estimated_cost_level="medium",
            quality_level="high"
        )
    
    def _handle_creative(
        self,
        complexity: TaskComplexity,
        cost_sensitivity: CostSensitivity
    ) -> ModelRecommendation:
        
        return ModelRecommendation(
            model="claude-3-5-sonnet-20241022",
            reasoning="Sonnet balances creativity and coherence for creative tasks",
            estimated_cost_level="medium",
            quality_level="high"
        )
    
    def _handle_research(
        self,
        complexity: TaskComplexity,
        cost_sensitivity: CostSensitivity
    ) -> ModelRecommendation:
        
        if complexity == TaskComplexity.HIGH:
            return ModelRecommendation(
                model="claude-3-opus-20240229",
                reasoning="Complex research requires Opus's best reasoning",
                estimated_cost_level="high",
                quality_level="high"
            )
        
        if cost_sensitivity == CostSensitivity.HIGH:
            return ModelRecommendation(
                model="claude-3-5-sonnet-20241022",
                reasoning="Research but budget-conscious - Sonnet with thorough prompts",
                estimated_cost_level="medium",
                quality_level="high"
            )
        
        return ModelRecommendation(
            model="claude-3-opus-20240229",
            reasoning="Research benefits from Opus's thorough analysis",
            estimated_cost_level="high",
            quality_level="high"
        )
```

## Decision Tree 2: Tool Use Strategy

### When to Use This Tree

Sử dụng decision tree này khi:

- Deciding whether to implement tool use
- Designing tool definitions
- Choosing between tool use và long prompts
- Planning multi-tool workflows

### Tool Use Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│                 TOOL USE STRATEGY DECISION TREE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  START: Does task require external data/actions?                  │
│                                                                 │
│  NO ──→ Can the information be in prompt context?               │
│         ├── YES ──→ Don't use tools                              │
│         │         Use direct prompting                           │
│         │                                                        │
│         NO ──→ Consider:                                         │
│                • Is data frequently needed?                      │
│                • Can you cache/generate it?                      │
│                → May need tool use after all                     │
│                                                                 │
│  YES ──→ What type of external interaction?                     │
│                                                                 │
│         ├─── REAL-TIME DATA ──────────────────────────────────┐ │
│         │                                                        │ │
│         │    Examples: weather, stock prices, news             │ │
│         │                                                         │ │
│         │    → USE TOOL                                          │ │
│         │    Tool type: API call (read-only)                    │ │
│         │    Caching: Cache where possible                      │ │
│         │                                                        │ │
│         └─── DATABASE QUERY ───────────────────────────────────┘ │
│         │                                                        │ │
│         │    Examples: user data, orders, products              │ │
│         │                                                         │ │
│         │    Is query pattern well-defined?                      │ │
│         │    ├── YES ──→ USE TOOL                                │ │
│         │    │        Tool type: Parameterized query              │ │
│         │    │        Security: Parameterize, whitelist tables   │ │
│         │    │                                                        │ │
│         │    NO ──→ Consider simpler interface first             │ │
│         │         (search-based, predefined queries)            │ │
│         │                                                        │ │
│         └─── CALCULATION / PROCESSING ──────────────────────────┐ │
│         │                                                        │ │
│         │    Examples: math, data transformation, formatting    │ │
│         │                                                        │ │
│         │    Can Claude do this accurately?                      │ │
│         │    ├── YES ──→ Don't use tools                        │ │
│         │    │        (let Claude handle internally)            │ │
│         │    │                                                        │ │
│         │    NO ──→ USE TOOL                                    │ │
│         │         Tool type: Computation/Processing             │ │
│         │         Examples: precise math, date calculations     │ │
│         │                                                        │ │
│         └─── ACTION EXECUTION ─────────────────────────────────┐ │
│         │                                                        │ │
│         │    Examples: send email, create record, update data   │ │
│         │                                                        │ │
│         │    Is action reversible/low-risk?                       │ │
│         │    ├── YES ──→ USE TOOL with confirmation             │ │
│         │    │        Tool type: Action with confirmation       │ │
│         │    │        Pattern: Confirm → Execute → Report       │ │
│         │    │                                                        │ │
│         │    NO ──→ Consider carefully                           │ │
│         │         • Add human-in-the-loop                        │ │
│         │         • Implement safety checks                      │ │
│         │         • Use read-only tools where possible           │ │
│         │                                                        │ │
│         └─── MULTIPLE TOOLS NEEDED? ───────────────────────────┐ │
│         │                                                        │ │
│         │    Are tools independent?                              │ │
│         │    ├── YES ──→ Execute in parallel                    │ │
│         │    │        (faster, better UX)                      │ │
│         │    │                                                        │ │
│         │    NO ──→ Execute sequentially                        │ │
│         │         (dependent results)                           │ │
│         │         Implement proper error handling                 │ │
│         │                                                        │ │
└─────────────────────────────────────────────────────────────────┘
```

### Tool Definition Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              TOOL DEFINITION DECISION TREE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  START: Design tool definition                                    │
│                                                                 │
│  ├─── NAME ───────────────────────────────────────────────────┐│
│  │                                                            ││
│  │    Use descriptive, action-oriented names                   ││
│  │    Format: verb_noun (e.g., search_products, get_weather)   ││
│  │    Avoid: vague names (query, get_data, process)            ││
│  │                                                            ││
│  └─── DESCRIPTION ────────────────────────────────────────────┘│
│                                                                 │
│  │                                                            │
│  │    Include:                                                │
│  │    • What the tool does                                    │
│  │    • When to use it                                        │
│  │    • What input is expected                                │
│  │    • What output is returned                               ││
│  │    • When NOT to use it                                    │
│  │                                                            │
│  │    Length: 100-500 characters                              │
│  │    Be specific but not overly detailed                     │
│  │                                                            │
│  └─── INPUT SCHEMA ────────────────────────────────────────────┘
│                                                                 │
│  │                                                            │
│  │    Properties:                                             │
│  │    • Each parameter needs type and description              │
│  │    • Include examples in descriptions if helpful           ││
│  │    • Use enums for limited options                         ││
│  │    • Set sensible defaults                                 ││
│  │                                                            │
│  │    Required array:                                         │
│  │    • Only truly required parameters                        ││
│  │    • Avoid requiring what can be optional                  ││
│  │    • Consider lazy evaluation                              ││
│  │                                                            │
└─────────────────────────────────────────────────────────────────┘
```

## Decision Tree 3: Context Management

### When to Use This Tree

Sử dụng decision tree này khi:

- Managing long conversations
- Handling context window limits
- Designing conversation history strategies
- Implementing truncation or summarization

### Context Management Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              CONTEXT MANAGEMENT DECISION TREE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  START: Analyze conversation characteristics                      │
│                                                                 │
│  ├─── CONVERSATION LENGTH ─────────────────────────────────────┐│
│  │                                                            ││
│  │    How many turns expected?                                 ││
│  │    ├── < 10 turns ──→ Full history (no truncation needed)  ││
│  │    │                                                         ││
│  │    ├── 10-50 turns ──→ Truncation strategy required         ││
│  │    │                                                         ││
│  │    └── > 50 turns ──→ Summarization recommended            ││
│  │                                                            ││
│  └─── MESSAGE SIZE ────────────────────────────────────────────┘│
│                                                                 │
│  │                                                            │
│  │    Average message length?                                   │
│  │    ├── Short (< 500 chars) ──→ Can keep more turns         ││
│  │    │                                (more history)          ││
│  │    │                                                         ││
│  │    ├── Medium (500-2000 chars) ──→ Balance turns & size    ││
│  │    │                                                         ││
│  │    └── Long (> 2000 chars) ──→ Fewer turns kept           ││
│  │                                   (context pressure)         ││
│  │                                                            ││
│  └─── TOKEN BUDGET ────────────────────────────────────────────┘
│                                                                 │
│  │                                                            │
│  │    Available for conversation history:                       │
│  │    ├── > 150K tokens ──→ Full history viable               ││
│  │    │                         (200K - system - output)      ││
│  │    │                                                         ││
│  │    ├── 50K-150K tokens ──→ Smart truncation               ││
│  │    │                         Keep recent + summary          ││
│  │    │                                                         ││
│  │    └── < 50K tokens ──→ Aggressive truncation             ││
│  │                          Keep only recent turns              ││
│  │                          Consider summarization               ││
│  │                                                            ││
│  └─── TRUNCATION STRATEGY ──────────────────────────────────────┘
│                                                                 │
│  │                                                            │
│  │    Choose based on conversation type:                       ││
│  │                                                            │
│  │    ├── Task-oriented (Q&A, support)                         ││
│  │    │    → Keep last N messages                              ││
│  │    │    → Discard oldest when full                          ││
│  │    │                                                         ││
│  │    ├── Creative (brainstorm, writing)                       ││
│  │    │    → Keep first + last + summary                       ││
│  │    │    → Important context from beginning                   ││
│  │    │                                                         ││
│  │    ├── Complex (multi-step tasks)                            ││
│  │    │    → Keep everything until limit                       ││
│  │    │    → Summarize when forced to truncate                 ││
│  │    │                                                         ││
│  │    └── Hybrid                                               ││
│  │         → Adaptive based on content type                     ││
│  │                                                            ││
└─────────────────────────────────────────────────────────────────┘
```

### Context Management Implementation Guide

```python
from enum import Enum
from typing import Literal

class ConversationType(Enum):
    TASK_ORIENTED = "task"      # Q&A, support, simple queries
    CREATIVE = "creative"       # Writing, brainstorming
    COMPLEX = "complex"          # Multi-step, sequential tasks
    HYBRID = "hybrid"           # Mixed

class TruncationStrategy(Enum):
    KEEP_RECENT = "keep_recent"         # Just last N
    FIRST_LAST_SUMMARY = "first_last"    # First + recent + summary
    ADAPTIVE = "adaptive"               # Based on content

def select_context_strategy(
    conversation_type: ConversationType,
    avg_message_tokens: int,
    max_history_tokens: int
) -> TruncationStrategy:
    """
    Select appropriate context management strategy.
    """
    
    if conversation_type == ConversationType.TASK_ORIENTED:
        # Simple Q&A: keep recent only
        return TruncationStrategy.KEEP_RECENT
    
    if conversation_type == ConversationType.CREATIVE:
        # Writing: first context matters
        return TruncationStrategy.FIRST_LAST_SUMMARY
    
    if conversation_type == ConversationType.COMPLEX:
        # Multi-step: keep as much as possible
        # Use summarization when forced
        return TruncationStrategy.ADAPTIVE
    
    # Hybrid: use adaptive
    return TruncationStrategy.ADAPTIVE

def calculate_optimal_history(
    system_tokens: int,
    output_tokens: int,
    max_context: int = 200000
) -> int:
    """
    Calculate optimal history token budget.
    """
    available = max_context - system_tokens - output_tokens
    # Reserve some buffer
    return int(available * 0.9)  # 90% for history, 10% safety margin
```

## Decision Tree 4: Parameter Tuning

### When to Use This Tree

Sử dụng decision tree này khi:

- Configuring generation parameters
- Choosing temperature settings
- Setting max_tokens
- Optimizing for quality vs. cost

### Parameter Tuning Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              PARAMETER TUNING DECISION TREE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  START: What aspect to tune?                                     │
│                                                                 │
│  ├─── TEMPERATURE ─────────────────────────────────────────────┐│
│  │                                                            ││
│  │    What output behavior do you need?                        ││
│  │                                                            ││
│  │    ├── Factual/Extraction                                   ││
│  │    │    └── temperature = 0.0-0.2                          ││
│  │    │        (deterministic, consistent)                     ││
│  │    │                                                         ││
│  │    ├── Balanced (general use)                               ││
│  │    │    └── temperature = 0.5-0.7                          ││
│  │    │        (balanced creativity)                           ││
│  │    │                                                         ││
│  │    ├── Creative/Varied                                      ││
│  │    │    └── temperature = 0.8-1.0                          ││
│  │    │        (creative, diverse)                             ││
│  │    │                                                         ││
│  │    └── PRO TIP: Start at 0.7, adjust based on results       ││
│  │                                                            ││
│  └─── MAX_TOKENS ──────────────────────────────────────────────┘│
│                                                                 │
│  │                                                            │
│  │    Expected response length?                                 ││
│  │                                                            ││
│  │    ├── Short answer (yes/no, simple)                        ││
│  │    │    └── max_tokens = 100-300                           ││
│  │    │                                                         ││
│  │    ├── Medium (explanation, summary)                         ││
│  │    │    └── max_tokens = 500-1500                          ││
│  │    │                                                         ││
│  │    ├── Long (detailed response, analysis)                    ││
│  │    │    └── max_tokens = 2000-4096                         ││
│  │    │                                                         ││
│  │    └── PRO TIP: Set slightly higher than expected            ││
│  │         (cheaper than regenerating if truncated)            ││
│  │                                                            ││
│  └─── TOP_P ────────────────────────────────────────────────────┘
│                                                                 │
│  │                                                            │
│  │    Usually use with temperature                              ││
│  │                                                            ││
│  │    ├── Low creativity needed (factual)                       ││
│  │    │    └── top_p = 0.5-0.7                               ││
│  │    │                                                         ││
│  │    ├── Balanced                                             ││
│  │    │    └── top_p = 0.9 (default, works with temp)         ││
│  │    │                                                         ││
│  │    └── PRO TIP: If adjusting temperature, consider top_p     ││
│  │         Setting both = fine-tuning sampling behavior        ││
│  │                                                            ││
└─────────────────────────────────────────────────────────────────┘
```

### Parameter Quick Reference

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PARAMETER SETTINGS QUICK REFERENCE                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  USE CASE                  │  TEMP  │  TOP_P  │  MAX_TOKENS            │
│  ────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  Classification            │  0.0   │  0.9    │  50-200               │
│  Sentiment Analysis       │  0.0   │  0.9    │  100-300              │
│  Data Extraction          │  0.1   │  0.9    │  200-500              │
│  Code Generation          │  0.3   │  0.95   │  500-2000             │
│  Code Review              │  0.2   │  0.9    │  1000-3000            │
│  Summarization            │  0.3   │  0.9    │  300-1000             │
│  Question Answering       │  0.3   │  0.9    │  500-1500             │
│  Content Writing          │  0.7   │  0.95   │  1000-3000            │
│  Creative Writing         │  0.8-1.0│  0.95   │  2000-4096           │
│  Brainstorming            │  0.8   │  0.95   │  1000-2000            │
│  Technical Documentation  │  0.3   │  0.9    │  1000-3000            │
│  Customer Support         │  0.5   │  0.9    │  500-1500             │
│                                                                         │
│  NOTES:                                                                 │
│  • Start with recommended values, adjust based on output quality        │
│  • Lower temperature = more predictable, higher = more creative          │
│  • max_tokens too low = truncated, too high = wasted tokens             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Decision Tree 5: Feature Adoption

### When to Use This Tree

Sử dụng decision tree này khi:

- Evaluating new Claude features
- Deciding on feature implementation priority
- Planning feature rollout

### Feature Adoption Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              FEATURE ADOPTION DECISION TREE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  START: Evaluate new feature                                      │
│                                                                 │
│  ├─── STREAMING ───────────────────────────────────────────────┐│
│  │                                                            ││
│  │    Will users wait for long responses?                      ││
│  │    ├── YES ──→ IMPLEMENT                                   ││
│  │    │        (improves perceived latency significantly)      ││
│  │    │                                                        ││
│  │    NO ──→ Consider:                                         ││
│  │         • Response latency requirements                     ││
│  │         • Implementation complexity                          ││
│  │         • → May not be worth it for short responses        ││
│  │                                                            ││
│  └─── TOOL USE ────────────────────────────────────────────────┘│
│                                                                 │
│  │                                                            ││
│  │    Does use case require external data/actions?             ││
│  │    ├── YES ──→ IMPLEMENT                                   ││
│  │    │        (core feature for complex applications)        ││
│  │    │                                                        ││
│  │    NO ──→ Consider:                                         ││
│  │         • Are there edge cases needing tools?                ││
│  │         • Would tools simplify prompts?                     ││
│  │         • → May not need for simple use cases              ││
│  │                                                            ││
│  └─── VISION ───────────────────────────────────────────────────┘
│                                                                 │
│  │                                                            ││
│  │    Does use case involve images?                            ││
│  │    ├── YES ──→ IMPLEMENT                                   ││
│  │    │        (only available on Sonnet/Opus models)         ││
│  │    │                                                        ││
│  │    NO ──→ Not applicable                                   ││
│  │         (don't add complexity if not needed)               ││
│  │                                                            ││
│  └─── MEMORY / PERSISTENCE ─────────────────────────────────────┘
│                                                                 │
│  │                                                            ││
│  │    Need cross-session state?                                ││
│  │    ├── YES ──→ IMPLEMENT CUSTOM                            ││
│  │    │        (database-backed conversation state)           ││
│  │    │                                                        ││
│  │    NO ──→ Per-session memory is sufficient                ││
│  │                                                            ││
└─────────────────────────────────────────────────────────────────┘
```

## Decision Tree 6: Error Handling Strategy

### When to Use This Tree

Sử dụng decision tree này khi:

- Designing error handling systems
- Choosing retry strategies
- Planning fallback behavior

### Error Handling Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              ERROR HANDLING DECISION TREE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  START: An error occurred - classify type                        │
│                                                                 │
│  ├─── RATE LIMIT (429) ────────────────────────────────────────┐│
│  │                                                            ││
│  │    Retry with exponential backoff                           ││
│  │    Initial delay: 1-2 seconds                               ││
│  │    Max retries: 3-5                                        ││
│  │    Include jitter to prevent thundering herd               ││
│  │                                                            ││
│  ├─── AUTHENTICATION (401) ────────────────────────────────────┤│
│  │                                                            ││
│  │    Do NOT retry                                             ││
│  │    Log error, alert immediately                             ││
│  │    Check API key configuration                              ││
│  │                                                            ││
│  ├─── CONTEXT TOO LONG (400) ──────────────────────────────────┤││
│  │                                                            ││
│  │    Do NOT retry same request                                ││
│  │    Truncate/summarize conversation history                  ││
│  │    Re-attempt with reduced context                          ││
│  │                                                            ││
│  ├─── SERVER ERROR (5xx) ──────────────────────────────────────┤││
│  │                                                            ││
│  │    Retry with exponential backoff                            ││
│  │    Max retries: 3                                           ││
│  │    Monitor for sustained errors                              ││
│  │                                                            ││
│  ├─── TIMEOUT ─────────────────────────────────────────────────┤││
│  │                                                            ││
│  │    Retry once with same parameters                          ││
│  │    If persists, may be network/server issue                  ││
│  │                                                            ││
│  └─── UNKNOWN ERROR ───────────────────────────────────────────┤││
│      │                                                            ││
│      │    Log full error details                                 ││
│      │    Retry once if potentially transient                    ││
│      │    Return user-friendly fallback if persists             ││
│      │                                                            ││
└─────────────────────────────────────────────────────────────────┘
```

## Decision Tree 7: Production Deployment

### When to Use This Tree

Sử dụng decision tree này khi:

- Planning production deployment
- Evaluating readiness
- Making deployment decisions

### Production Deployment Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              PRODUCTION DEPLOYMENT DECISION TREE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  START: Is the feature ready for production?                      │
│                                                                 │
│  ├─── TESTING COMPLETE? ────────────────────────────────────────┐│
│  │    ├── Unit tests passing                                    ││
│  │    ├── Integration tests passing                              ││
│  │    ├── Performance tests completed                            ││
│  │    └── YES ──→ Continue to next check                        ││
│  │         NO ──→ Complete testing first                         ││
│  │                                                            ││
│  ├─── ERROR HANDLING IMPLEMENTED? ──────────────────────────────┤│
│  │    ├── Retry logic with backoff                               ││
│  │    ├── Circuit breaker                                       ││
│  │    ├── Graceful degradation                                  ││
│  │    └── YES ──→ Continue                                      ││
│  │         NO ──→ Implement before production                    ││
│  │                                                            ││
│  ├─── MONITORING CONFIGURED? ──────────────────────────────────┤│
│  │    ├── Metrics dashboards                                    ││
│  │    ├── Error alerting                                        ││
│  │    ├── Cost monitoring                                       ││
│  │    └── YES ──→ Continue                                      ││
│  │         NO ──→ Set up before production                      ││
│  │                                                            ││
│  ├─── SECURITY REVIEWED? ──────────────────────────────────────┤│
│  │    ├── API keys secured                                      ││
│  │    ├── Input/output sanitized                                ││
│  │    ├── Rate limiting in place                                ││
│  │    └── YES ──→ Continue                                      ││
│  │         NO ──→ Complete security review                      ││
│  │                                                            ││
│  └─── DOCUMENTATION UPDATED? ──────────────────────────────────┤│
│       │    ├── API documentation                                 ││
│       │    ├── Runbooks                                          ││
│       │    ├── Deployment procedures                             ││
│       │    └── YES ──→ Ready for deployment                      ││
│            NO ──→ Update documentation first                     ││
│                                                                 │
│  DEPLOYMENT STRATEGY:                                            │
│  ├─── Canary Release (recommended for new features)              ││
│  │    • Deploy to 1-5% of traffic first                        ││
│  │    • Monitor for issues                                     ││
│  │    • Gradually increase traffic                              ││
│  │    • Full rollout over 1-2 weeks                            ││
│  │                                                            ││
│  ├─── Feature Flag                                              ││
│  │    • Enable/disable without redeployment                    ││
│  │    • Quick rollback capability                               ││
│  │                                                            ││
│  └─── Blue-Green (for critical deployments)                     ││
│       • Maintain parallel environments                         ││
│       • Switch traffic atomically                              ││
│       • Quick rollback option                                   ││
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Decision Summary Cards

### Model Selection Quick Card

```
╔═══════════════════════════════════════════════════════════════╗
║              MODEL SELECTION QUICK CARD                         ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  TASK TYPE              →  MODEL                             ║
║  ─────────────────────────────────────────────────────────   ║
║  Classification/Simple   →  Claude 3.5 Haiku                  ║
║  General Purpose        →  Claude 3.5 Sonnet                  ║
║  Complex Reasoning      →  Claude 3 Opus                       ║
║  Code (simple)          →  Claude 3.5 Sonnet                  ║
║  Code (complex)         →  Claude 3 Opus                       ║
║  Creative Writing       →  Claude 3.5 Sonnet + high temp       ║
║  Research/Analysis      →  Claude 3 Opus                       ║
║                                                               ║
║  COST QUALITY TRADE-OFF:                                       ║
║  Haiku:  1x cost   - Good for simple tasks                     ║
║  Sonnet: 12x cost  - Best balance (default choice)              ║
║  Opus:   60x cost  - Best quality                              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

### Parameter Quick Card

```
╔═══════════════════════════════════════════════════════════════╗
║              PARAMETER SETTINGS QUICK CARD                     ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  BEHAVIOR           →  TEMPERATURE  →  USE CASE              ║
║  ──────────────────────────────────────────────────────────   ║
║  Deterministic      →  0.0 - 0.2   →  Classification         ║
║  Focused            →  0.3 - 0.5   →  Code, Q&A              ║
║  Balanced           →  0.5 - 0.7   →  General use            ║
║  Creative           →  0.7 - 0.9   →  Content               ║
║  Very Creative      →  0.9 - 1.0   →  Brainstorming          ║
║                                                               ║
║  RESPONSE LENGTH   →  MAX_TOKENS                             ║
║  ──────────────────────────────────────────────────────────   ║
║  Very short         →  50 - 200    (yes/no, single word)      ║
║  Short              →  200 - 500   (simple answers)           ║
║  Medium             →  500 - 1500  (explanations)             ║
║  Long               →  1500 - 3000 (detailed)               ║
║  Very Long          →  3000 - 4096 (comprehensive)           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## References

- [Anthropic API Documentation](https://docs.anthropic.com/claude/docs)
- [Model Selection Guide](https://docs.anthropic.com/claude/docs/model-selection)
- [Tool Use Documentation](https://docs.anthropic.com/claude/docs/tool-use)
- [Best Practices](https://docs.anthropic.com/claude/docs/best-practices)
