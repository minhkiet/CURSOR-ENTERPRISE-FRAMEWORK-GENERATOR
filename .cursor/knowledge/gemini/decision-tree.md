---
title: "Gemini Decision Tree - Cây Quyết Định"
description: "Comprehensive decision tree for Google Gemini model selection, API usage strategy, configuration, and implementation decisions"
tags: ["gemini", "google-ai", "decision-tree", "model-selection", "architecture", "vertex-ai"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Gemini Decision Tree - Cây Quyết Định

## Tổng Quan (Overview)

Tài liệu này cung cấp các decision trees toàn diện giúp developers và architects đưa ra quyết định khi làm việc với Google Gemini API. Mỗi decision tree bao gồm các nhánh quyết định, tiêu chí đánh giá, và recommendations cụ thể.

Việc sử dụng decision trees giúp standardize decision-making process, reduce cognitive load, và đảm bảo consistent choices được made across team members. Các trees được thiết kế để sử dụng trong thực tế với clear-cut decision points.

## Mục Đích (Purpose)

Tài liệu này phục vụ các mục đích chính sau:

1. **Standardized decision-making** cho common scenarios
2. **Quick reference** khi đối mặt với technical choices
3. **Training material** cho team members mới
4. **Architecture guidance** cho system design

## Decision Tree Index

1. Model Selection Tree
2. API Platform Selection Tree
3. Input Type Selection Tree
4. Output Format Selection Tree
5. Safety Configuration Tree
6. Caching Strategy Tree
7. Rate Limiting Strategy Tree
8. Error Handling Strategy Tree
9. Multimodal Processing Tree
10. Function Calling Strategy Tree

---

## Decision Tree 1: Model Selection

### Tree 1.1 - Primary Model Selection

```
START: What is your primary use case?
│
├─► Complex reasoning, research, or high-stakes decisions?
│   └─► YES → Use Gemini Ultra (gemini-1.5-pro for cost optimization)
│   │
│   └─► NO → Continue to next question
│
├─► General purpose text generation, Q&A, summarization?
│   └─► YES → Continue to Tier question
│   │
│   └─► NO → Continue to next question
│
├─► High volume, low latency requirements?
│   └─► YES → Use Gemini Flash
│   │
│   └─► NO → Continue to next question
│
└─► On-device or edge deployment?
    └─► YES → Use Gemini Nano (via AI Edge)
    │
    └─► NO → Use Gemini Pro
```

### Tree 1.2 - Model Tier Selection (Gemini Pro vs Flash vs Ultra)

```
START: What are your priorities?
│
├─► Maximum quality and capability > everything else?
│   └─► YES → Use Gemini Ultra
│       - Complex reasoning tasks
│       - Research and analysis
│       - Multi-step problem solving
│       - Code generation (complex)
│       - Premium applications
│   │
│   └─► NO → Continue
│
├─► Balancing quality, cost, and speed?
│   └─► YES → Use Gemini Pro
│       - Most production applications
│       - General content generation
│       - Document processing
│       - Chat applications
│       - Moderate complexity tasks
│   │
│   └─► NO → Continue
│
└─► Speed and cost efficiency > quality?
    └─► YES → Use Gemini Flash
        - Real-time applications
        - High-volume processing
        - Simple, repetitive tasks
        - User-facing interfaces
        - Batch processing
```

### Tree 1.3 - Model Version Selection

```
START: Do you need experimental features or maximum context?
│
├─► YES (need 1M token context or latest features)?
│   └─► Use latest model version (gemini-1.5-pro-002)
│   └─► Consider: May have stability trade-offs
│   └─► Consider: Higher cost for newer versions
│   │
│   └─► NO → Continue
│
├─► Do you need stable, well-tested features?
│   └─► YES → Use stable version (gemini-1.5-pro)
│   └─► Note: Feature parity with stable release
│   │
│   └─► NO → Continue
│
└─► Do you prioritize cost optimization?
    └─► YES → Use Flash for non-critical paths
    └─► Use Pro for critical paths
    └─► Consider tiered architecture
```

### Model Selection Matrix

| Use Case | Primary Choice | Alternative | Avoid |
|----------|---------------|-------------|-------|
| Chatbot | Gemini Pro | Gemini Flash (high volume) | Gemini Ultra |
| Code Generation | Gemini Pro | Gemini Ultra (complex) | Gemini Flash |
| Document Analysis | Gemini Pro | Gemini Ultra (complex docs) | Gemini Flash |
| Real-time Q&A | Gemini Flash | Gemini Pro | Gemini Ultra |
| Research | Gemini Ultra | Gemini Pro | Gemini Flash |
| Batch Processing | Gemini Flash | Gemini Pro | Gemini Ultra |
| Image Understanding | Gemini Pro | Gemini Flash (simple) | Gemini Ultra |
| Complex Reasoning | Gemini Ultra | Gemini Pro | Gemini Flash |

---

## Decision Tree 2: API Platform Selection

### Tree 2.1 - AI Studio vs Vertex AI

```
START: What is your deployment environment?
│
├─► Development or prototyping only?
│   └─► YES → Use AI Studio
│       - Free tier available
│       - Quick setup
│       - Ideal for experimentation
│       - Limited to non-production
│   │
│   └─► NO → Continue
│
├─► Production environment?
│   └─► YES → Use Vertex AI
│       - Enterprise security
│       - IAM integration
│       - VPC support
│       - SLA guarantees
│       - Advanced features
│   │
│   └─► NO → Continue
│
└─► Need enterprise features?
    └─► YES → Use Vertex AI
        - Compliance requirements
        - Advanced monitoring
        - Custom quotas
        - Dedicated support
        - Data residency
    │
    └─► NO → Consider both based on other factors
```

### Tree 2.2 - Authentication Method Selection

```
START: What is your deployment type?
│
├─► Vertex AI (production)?
│   └─► Use Service Account + IAM
│       - Create dedicated service account
│       - Assign minimum required roles
│       - Use workload identity if on GCP
│       - Store credentials securely
│   │
│   └─► NO → Continue
│
├─► AI Studio (development)?
│   └─► Use API Key
│       - Generate in AI Studio
│       - Apply domain restrictions
│       - Set up key rotation
│       - Monitor usage
│   │
│   └─► NO → Continue
│
└─► Local development?
    └─► Use Application Default Credentials
        - gcloud auth application-default login
        - For local testing
        - Not for production
```

---

## Decision Tree 3: Input Type Selection

### Tree 3.1 - Choosing Input Modality

```
START: What type of input do you have?
│
├─► Text only?
│   └─► YES → Use text input
│       - Direct prompt
│       - Most cost-effective
│       - Fastest processing
│   │
│   └─► NO → Continue
│
├─► Image(s)?
│   └─► YES → Continue to image type
│   │
│   ├─► Document/PDF?
│   │   └─► Use vision with document extraction
│   │   └─► Consider: PDF conversion first
│   │
│   ├─► Chart/Graph/Diagram?
│   │   └─► Use vision with analysis prompt
│   │   └─► Consider: Gemini Pro for complex analysis
│   │
│   ├─► Photo/Real-world image?
│   │   └─► Use vision with appropriate prompt
│   │   └─► Consider: Image optimization for size
│   │
│   └─► NO → Continue
│
├─► Audio?
│   └─► YES → Use audio input
│       - Convert to WAV format
│       - Sample rate: 16kHz optimal
│       - Max duration limits apply
│   │
│   └─► NO → Continue
│
└─► Video?
    └─► YES → Use frame sampling strategy
        - Sample key frames
        - Consider audio extraction
        - Balance frame count vs. context
```

### Tree 3.2 - Image Optimization Decision

```
START: What is your image quality requirement?
│
├─► High precision needed (medical, technical)?
│   └─► Use high quality preset
│       - Max dimension: 1536
│       - Quality: 90%
│       - Format: PNG
│   │
│   └─► NO → Continue
│
├─► Standard analysis (documents, photos)?
│   └─► Use analysis preset
│       - Max dimension: 1024
│       - Quality: 85%
│       - Format: JPEG
│   │
│   └─► NO → Continue
│
├─► Preview or thumbnails?
│   └─► Use preview preset
│       - Max dimension: 512
│       - Quality: 80%
│       - Format: JPEG
│   │
│   └─► NO → Continue
│
└─► Maximum speed/cost efficiency?
    └─► Use thumbnail preset
        - Max dimension: 256
        - Quality: 70%
        - Format: JPEG
```

---

## Decision Tree 4: Output Format Selection

### Tree 4.1 - Output Format Decision

```
START: How will the output be used?
│
├─► Programmatic processing (API, automation)?
│   └─► YES → Use JSON Mode
│       - Set responseMimeType: "application/json"
│       - Define output schema if needed
│       - Validate JSON in application
│   │
│   └─► NO → Continue
│
├─► Human consumption (UI, documents)?
│   └─► YES → Use plain text
│       - Natural language response
│       - Markdown formatting supported
│       - Handle variable length
│   │
│   └─► NO → Continue
│
└─► External system integration?
    └─► YES → Consider structured options
        - JSON for REST APIs
        - XML for legacy systems
        - Delimited for data pipelines
```

### Tree 4.2 - Structured Output Schema Decision

```
START: Do you need strict schema enforcement?
│
├─► YES (strict validation required)?
│   └─► Define JSON Schema
│       - Specify all fields
│       - Define types and constraints
│       - Handle partial matches
│       - Implement retry logic
│   │
│   └─► NO → Continue
│
├─► Partial structure acceptable?
│   └─► YES → Use soft schema
│       - Define key fields only
│       - Allow additional fields
│       - Parse what's available
│   │
│   └─► NO → Continue
│
└─► Natural language with guidance?
    └─► Use instruction-based format
        - Specify format in prompt
        - Use examples
        - Parse and validate output
```

---

## Decision Tree 5: Safety Configuration

### Tree 5.1 - Safety Threshold Selection

```
START: What is your content domain?
│
├─► Children's content or education?
│   └─► Use BLOCK_LOW_AND_ABOVE for all categories
│       - Maximum protection
│       - May increase false positives
│   │
│   └─► NO → Continue
│
├─► General consumer application?
│   └─► Use BLOCK_MEDIUM_AND_ABOVE
│       - Balanced approach
│       - Standard protection
│       - Good user experience
│   │
│   └─► NO → Continue
│
├─► Enterprise/internal tool?
│   └─► Use BLOCK_MEDIUM_AND_ABOVE or BLOCK_ONLY_HIGH
│       - Trust internal users somewhat
│       - Still protect against extremes
│   │
│   └─► NO → Continue
│
└─► Professional users (researchers, developers)?
    └─► Use BLOCK_ONLY_HIGH
        - Minimal blocking
        - Professional context assumed
        - Monitor for issues
```

### Tree 5.2 - Category-Specific Configuration

```
START: Do you have specific safety concerns?
│
├─► Hate speech concerns (public-facing)?
│   └─► STRENGTHEN: BLOCK_MEDIUM_AND_ABOVE
│   └─► Consider: Content moderation upstream
│   │
│   └─► NO → Continue
│
├─► Dangerous content concerns?
│   └─► STRENGTHEN: BLOCK_ONLY_HIGH minimum
│   └─► Consider: Input validation
│   │
│   └─► NO → Continue
│
├─► Harassment concerns (community platform)?
│   └─► STRENGTHEN: BLOCK_MEDIUM_AND_ABOVE
│   └─► Consider: User reporting system
│   │
│   └─► NO → Continue
│
└─► No specific concerns?
    └─► Use standard BLOCK_MEDIUM_AND_ABOVE
        - Balanced protection
        - Good for most applications
```

---

## Decision Tree 6: Caching Strategy

### Tree 6.1 - To Cache or Not To Cache

```
START: Do you have repeated context in requests?
│
├─► YES (same context across multiple requests)?
│   └─► Continue to context size question
│   │
│   ├─► Large context (>10K tokens)?
│   │   └─► YES → Use Context Cache
│   │       - Significant cost savings (up to 90%)
│   │       - Better latency for cached content
│   │       - Consider cache TTL
│   │   │
│   │   └─► NO → Consider application-level cache
│   │       - May not justify API caching overhead
│   │       - Redis/Memcached may be sufficient
│   │
│   └─► NO → Continue
│
├─► Do you have similar queries?
│   └─► YES → Use application-level response cache
│       - Cache frequent query patterns
│       - TTL based on data freshness needs
│   │
│   └─► NO → No caching needed
│       - Each request is unique
│       - Cache would have low hit rate
│
└─► Is response latency critical?
    └─► YES → Consider aggressive caching
        - Cache both context and responses
        - Shorter TTFT with cached context
    │
    └─► NO → Evaluate cost/benefit per use case
```

### Tree 6.2 - Cache TTL Selection

```
START: How often does your context change?
│
├─► Static context (system instructions, rules)?
│   └─► Use long TTL (hours to days)
│       - 3600s (1 hour) to 86400s (24 hours)
│       - Rarely needs invalidation
│   │
│   └─► NO → Continue
│
├─► Semi-static (policy documents, reference)?
│   └─► Use medium TTL (minutes to hours)
│       - 300s (5 minutes) to 3600s (1 hour)
│       - Refresh periodically
│   │
│   └─► NO → Continue
│
├─► Dynamic context (recent conversations)?
│   └─► Use short TTL (minutes)
│       - 60s to 300s
│       - Balance freshness vs cost
│   │
│   └─► NO → Continue
│
└─► Real-time context?
    └─► Consider not caching
        - Freshness more important
        - May not benefit from caching
```

---

## Decision Tree 7: Rate Limiting Strategy

### Tree 7.1 - Rate Limit Architecture

```
START: What is your expected request volume?
│
├─► Very high (>1000 requests/minute)?
│   └─► Enterprise tier + custom quotas
│       - Request quota increase
│       - Implement distributed rate limiting
│       - Consider batch processing
│   │
│   └─► NO → Continue
│
├─► High (100-1000 requests/minute)?
│   └─► Pay-as-you-go tier + app-level limiting
│       - Configure appropriate RPM limits
│       - Implement token bucket algorithm
│       - Queue excess requests
│   │
│   └─► NO → Continue
│
├─► Medium (10-100 requests/minute)?
│   └─► Standard rate limiting
│       - Respect API limits
│       - Implement basic retry logic
│   │
│   └─► NO → Continue
│
└─► Low (<10 requests/minute)?
    └─► Minimal rate limiting needed
        - API limits should suffice
        - Simple error handling
```

### Tree 7.2 - Retry Strategy Selection

```
START: What type of error did you receive?
│
├─► 429 Too Many Requests?
│   └─► YES → Retry with backoff
│       - Check Retry-After header
│       - Implement exponential backoff
│       - Add jitter to prevent thundering herd
│   │
│   └─► NO → Continue
│
├─► 500/503 Internal Error?
│   └─► YES → Retry with backoff
│       - May be transient
│       - Typically 3-5 retries
│       - Log for monitoring
│   │
│   └─► NO → Continue
│
├─► 400 Bad Request?
│   └─► NO RETRY - Fix the request
│       - Check input format
│       - Validate parameters
│       - Don't retry invalid requests
│   │
│   └─► NO → Continue
│
└─► Timeout?
    └─► MAY RETRY
        - Could be network issue
        - Implement timeout handling
        - Set reasonable timeout limits
```

### Tree 7.3 - Backoff Configuration

```
START: What is your retry tolerance?
│
├─► User-facing (immediate feedback needed)?
│   └─► Aggressive backoff
│       - Base delay: 500ms
│       - Max delay: 5s
│       - Max retries: 2-3
│       - Prioritize user experience
│   │
│   └─► NO → Continue
│
├─► Background processing (can wait)?
│   └─► Conservative backoff
│       - Base delay: 1s
│       - Max delay: 60s
│       - Max retries: 5-10
│       - Prioritize success rate
│   │
│   └─► NO → Continue
│
└─► Batch processing?
    └─► Very conservative backoff
        - Base delay: 2s
        - Max delay: 120s
        - High retry count
        - Accept long completion times
```

---

## Decision Tree 8: Error Handling Strategy

### Tree 8.1 - Error Classification

```
START: What error did you receive?
│
├─► Error contains "SAFETY" or "BLOCKED"?
│   └─► YES → Safety Error
│       - Don't retry (won't help)
│       - Log the blocked content
│       - Provide user feedback
│       - Consider adjusting safety settings
│   │
│   └─► NO → Continue
│
├─► Error contains "quota" or "limit"?
│   └─► YES → Quota Error
│       - Check quota dashboard
│       - Implement throttling
│       - Consider quota increase
│       - May retry after reset
│   │
│   └─► NO → Continue
│
├─► Error contains "auth" or "key"?
│   └─► YES → Authentication Error
│       - Don't retry
│       - Fix credentials
│       - Check service account
│   │
│   └─► NO → Continue
│
├─► Error is 5xx?
│   └─► YES → Server Error
│       - Retry with backoff
│       - Log for monitoring
│       - Alert if persistent
│   │
│   └─► NO → Continue
│
└─► Error is timeout?
    └─► MAYBE → Network/Timeout Error
        - Retry once
        - Increase timeout
        - Check network
```

### Tree 8.2 - Error Recovery Strategy

```
START: Can the error be recovered from?
│
├─► YES - Retryable error?
│   └─► Implement retry with backoff
│   └─► Check retry count
│   └─► Return error after max retries
│   │
│   └─► NO → Continue
│
├─► YES - User input issue?
│   └─► Return user-friendly message
│   └─► Suggest corrections
│   └─► Don't blame the model
│   │
│   └─► NO → Continue
│
└─► NO - Configuration/code issue?
    └─► Log detailed error
    └─► Alert operations
    └─► Return generic error to user
    └─► Fix the underlying issue
```

---

## Decision Tree 9: Multimodal Processing

### Tree 9.1 - Processing Strategy Selection

```
START: What is your primary task?
│
├─► Text extraction (OCR)?
│   └─► Use high quality image
│   └─► Explicit extraction prompt
│   └─► Consider PDF for better quality
│   │
│   └─► NO → Continue
│
├─► Image understanding/description?
│   └─► Use appropriate quality preset
│   └─► Provide clear question/prompt
│   └─► Consider multiple images
│   │
│   └─► NO → Continue
│
├─► Document analysis?
│   └─► Process page by page
│   └─► Use table/form extraction prompts
│   └─► Combine results
│   │
│   └─► NO → Continue
│
├─► Chart/graph analysis?
│   └─► Use high quality
│   └─► Specific analysis prompts
│   └─► Consider asking for data extraction
│   │
│   └─► NO → Continue
│
└─► Cross-image comparison?
    └─► Include multiple images
    └─► Explicit comparison prompt
    └─► Consider Gemini Pro for complex comparisons
```

### Tree 9.2 - Image Count Strategy

```
START: How many images do you need to process?
│
├─► Single image?
│   └─► Direct processing
│   └─► Optimize for analysis
│   │
│   └─► NO → Continue
│
├─► 2-5 images (comparison, collection)?
│   └─► Include all in single request
│   └─► Use consistent formatting
│   └─► Explicit instructions for each
│   │
│   └─► NO → Continue
│
├─► 5-20 images (document, album)?
│   └─► Consider batching
│   └─► Process in groups
│   └─► Balance context vs. quality
│   │
│   └─► NO → Continue
│
└─► Large collection (>20)?
    └─► Consider alternative approach
        - Pre-filter/select images
        - Use summary approach
        - Process in batches
        - May exceed context limits
```

---

## Decision Tree 10: Function Calling Strategy

### Tree 10.1 - Function Calling Decision

```
START: Do you need external system integration?
│
├─► YES (need database, API, file access)?
│   └─► Continue to function type
│   │
│   ├─► Simple function (lookup, calculation)?
│   │   └─► Use single function
│   │   └─► Straightforward declaration
│   │
│   ├─► Multiple related functions?
│   │   └─► Use multiple declarations
│   │   └─► Clear, non-overlapping purposes
│   │
│   └─► Complex multi-step workflow?
│       └─► Use multi-turn function calling
│       └─► Implement state management
│       └─► Consider agent framework
│
└─► NO (standalone generation)?
    └─► Don't use function calling
        - Unnecessary complexity
        - Standard generation simpler
```

### Tree 10.2 - Function Declaration Design

```
START: How complex is your function?
│
├─► Simple with few parameters?
│   └─► Flat schema
│   └─► Clear descriptions
│   └─► Appropriate defaults
│   │
│   └─► NO → Continue
│
├─► Complex with nested objects?
│   └─► Use nested JSON Schema
│   └─► Detailed field descriptions
│   └─► Consider splitting functions
│   │
│   └─► NO → Continue
│
├─► Variable parameters needed?
│   └─► Use additionalProperties
│   └─► Document expected patterns
│   │
│   └─► NO → Continue
│
└─► Fixed parameter set?
    └─► Use enum when appropriate
    └─► Set required vs optional
    └─► Provide examples
```

### Tree 10.3 - Response Handling Strategy

```
START: How will function results be used?
│
├─► Continue generation with results?
│   └─► YES → Multi-turn pattern
│       - Send results back to model
│       - Include all results simultaneously
│       - Let model synthesize response
│   │
│   └─► NO → Continue
│
├─► Extract specific data?
│   └─► YES → Parse and use directly
│       - Extract needed fields
│       - Validate data types
│       - Handle missing data
│   │
│   └─► NO → Continue
│
└─► Transform and display?
    └─► YES → Format results
        - Transform to display format
        - Add UI-friendly formatting
        - Consider error states
```

---

## Quick Reference: Common Decision Scenarios

### Scenario 1: Building a Customer Support Chatbot

```
Model: Gemini Pro (balanced quality/cost)
Platform: Vertex AI (production security)
Input: Text only (may add image later)
Output: Plain text (conversational)
Safety: BLOCK_MEDIUM_AND_ABOVE (general consumer)
Caching: Session-level context cache
Rate Limiting: Standard + app-level
Error Handling: Retry + graceful degradation
```

### Scenario 2: Document Processing Pipeline

```
Model: Gemini Pro (complex docs) or Flash (simple)
Platform: Vertex AI (batch processing)
Input: Images (scanned docs)
Output: JSON (structured extraction)
Safety: BLOCK_MEDIUM_AND_ABOVE
Caching: Document content cache
Rate Limiting: Conservative for batch
Error Handling: Retry with logging
```

### Scenario 3: Real-time Content Moderation

```
Model: Gemini Flash (speed priority)
Platform: Vertex AI (production)
Input: Text + Images
Output: JSON (classification)
Safety: BLOCK_LOW_AND_ABOVE (strict)
Caching: Minimal (fresh content)
Rate Limiting: Aggressive (high volume)
Error Handling: Fast fail + queue
```

### Scenario 4: Research Assistant

```
Model: Gemini Ultra (complex reasoning)
Platform: Vertex AI (enterprise)
Input: Multimodal (docs, images, papers)
Output: Structured + text (reports)
Safety: BLOCK_MEDIUM_AND_ABOVE
Caching: Reference material cache
Rate Limiting: Conservative (quality > speed)
Error Handling: Detailed logging
```

### Scenario 5: Code Generation Tool

```
Model: Gemini Pro (complex code) or Flash (simple)
Platform: AI Studio (prototype) → Vertex AI (prod)
Input: Text (requirements, context)
Output: Text (code) + Markdown (explanation)
Safety: BLOCK_MEDIUM_AND_ABOVE
Caching: Common patterns cache
Rate Limiting: Standard
Error Handling: Retry + fallbacks
```

---

## Decision Matrix Summary

### Quality vs. Cost vs. Speed Trade-off

| Priority | Model | Caching | Batch |
|----------|-------|---------|-------|
| Quality > All | Ultra | Yes | No |
| Balanced | Pro | Yes | Maybe |
| Speed > All | Flash | Yes | Yes |
| Cost > All | Flash | Yes | Yes |

### Security vs. Flexibility Trade-off

| Priority | Platform | Auth | Safety |
|----------|----------|------|--------|
| Maximum Security | Vertex AI | Service Account | Strict |
| Balanced | Vertex AI | Service Account | Medium |
| Development | AI Studio | API Key | Medium |
| Experimentation | AI Studio | API Key | Minimal |

### Simplicity vs. Control Trade-off

| Priority | Approach | Pros | Cons |
|----------|----------|------|------|
| Simplicity | AI Studio | Quick start | Limited control |
| Control | Vertex AI | Full features | More setup |
| Automation | API Direct | Custom pipeline | Most complex |

---

## Implementation Checklist by Decision

### After Model Selection

- [ ] Verify model availability in your region
- [ ] Check pricing for selected model
- [ ] Configure appropriate generation settings
- [ ] Test with representative inputs

### After Platform Selection

- [ ] Set up authentication
- [ ] Configure project and quotas
- [ ] Set up monitoring
- [ ] Document deployment configuration

### After Safety Configuration

- [ ] Test with edge cases
- [ ] Establish monitoring for blocks
- [ ] Create user feedback templates
- [ ] Plan for safety threshold adjustments

### After Caching Strategy

- [ ] Implement cache layer
- [ ] Test cache hit rates
- [ ] Monitor cache costs
- [ ] Set cache invalidation logic

### After Rate Limiting Strategy

- [ ] Configure rate limits
- [ ] Implement retry logic
- [ ] Test under load
- [ ] Set up alerting

---

## References

- [Google Gemini Models](https://ai.google.dev/models/gemini)
- [Vertex AI Pricing](https://cloud.google.com/vertex-ai/pricing)
- [AI Studio Pricing](https://ai.google.dev/pricing)
- [Safety Settings](https://ai.google.dev/docs/safety_guidance)
- [Context Caching](https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache)
- [Rate Limits](https://cloud.google.com/vertex-ai/quotas)
