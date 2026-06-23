---
title: "Gemini API Glossary - Từ Điển Thuật Ngữ"
description: "Comprehensive glossary of Google Gemini API terminology, covering models, safety settings, function declarations, content generation, and technical concepts"
tags: ["gemini", "google-ai", "glossary", "terminology", "llm", "vertex-ai"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Gemini API Glossary - Từ Điển Thuật Ngữ

## Tổng Quan (Overview)

Tài liệu này cung cấp từ điển toàn diện các thuật ngữ liên quan đến Google Gemini API. Được thiết kế như reference guide cho developers, data scientists, và technical professionals làm việc với Gemini. Mỗi thuật ngữ được định nghĩa rõ ràng với ngữ cảnh sử dụng và examples.

Việc nắm vững các thuật ngữ này là essential cho việc hiểu tài liệu Google, tham gia discussions về AI, và implement Gemini solutions hiệu quả. Glossary được tổ chức theo categories để dễ reference.

## Mục Đích (Purpose)

Tài liệu này phục vụ các mục đích chính sau:

1. **Reference tool** cho developers khi đọc documentation
2. **Learning resource** cho những ai mới với Gemini và LLM concepts
3. **Terminology alignment** cho team members trong dự án
4. **Interview preparation** cho technical interviews

## A

### Adaptive Temperature

A parameter adjustment technique where temperature varies during generation based on content type or position in the response. Adaptive temperature can improve output quality by using lower temperatures for factual/coding tasks and higher temperatures for creative writing.

**Related**: Temperature, Top-K, Top-P

### AI Studio

Google's free developer tool for experimenting with Gemini models. Provides an interactive playground for testing prompts, API key management, and model configuration. AI Studio is designed for prototyping and development, while Vertex AI is recommended for production workloads.

**Comparison**: AI Studio is to Vertex AI as a development server is to production infrastructure.

**Related**: Vertex AI, Google Cloud Console

### API Key (Gemini)

A unique identifier used to authenticate requests to the Gemini API when using AI Studio. API keys should be kept secure and never committed to source control. For production applications, service accounts and IAM are recommended over API keys.

**Related**: Service Account, Authentication

### API Versioning

Gemini API uses date-based versioning (e.g., v1beta, v1) to indicate stability and feature availability. New features are typically introduced in beta versions before being promoted to stable. Production applications should use stable versions.

**Example**: `generativelanguage.googleapis.com/v1beta1/models/gemini-1.5-pro`

**Related**: REST API, Endpoint

## B

### Batch Processing

A mode of processing multiple requests together rather than one at a time. Batch processing in Gemini is useful for high-volume workloads like document classification, content moderation, or bulk text transformation. Can improve throughput and cost efficiency.

**Use Cases**: Document processing, content classification, bulk translation, data enrichment

**Related**: Concurrent Requests, Rate Limiting, TPM

### Blocked Content

Content that triggers Gemini's safety filters and is prevented from being generated or processed. Blocked content depends on the configured safety settings and the harm category thresholds. When content is blocked, the API returns specific block reasons.

**Related**: Safety Filtering, Safety Settings, Harm Categories

### Byte Snippet

Raw binary data encoded as a base64 string for transmission via the API. Used for image, audio, and video data in multimodal requests. The API has size limits for inline data, which vary by content type.

**Example**: `{ inlineData: { mimeType: "image/jpeg", data: "base64encodedstring..." } }`

**Related**: Base64 Encoding, Multimodal Input, Inline Data

## C

### Candidate Count

The number of alternative responses the model can generate. By default, Gemini generates one response, but this can be increased to receive multiple candidates for comparison or selection. Higher candidate counts increase API usage and costs.

**Configuration**: `generationConfig.candidateCount`

**Trade-off**: Quality vs. Cost

**Related**: N-Best, Response Selection

### Cached Content

Contextual information that is pre-processed and stored for efficient reuse across multiple requests. Caching significantly reduces costs when the same context (like system instructions or reference documents) is used repeatedly. Available through Vertex AI Context Cache feature.

**Benefits**: Up to 90% cost reduction for repeated context, improved latency for cached content

**Related**: Context Cache, Token Reduction, Vertex AI

### Category (Safety)

See Harm Category

### Chat History

The accumulated sequence of messages in a conversation, including both user inputs and model responses. Chat history is essential for maintaining context in multi-turn conversations. The API supports various history formats and sizes depending on the model's context window.

**Implementation**: Pass previous messages in the `contents` array with appropriate roles

**Related**: Context Window, Multi-Turn, Session

### Code Generation

Gemini's capability to generate, explain, and debug code in multiple programming languages. The model understands context from comments, function signatures, and project structure. Effective code generation requires clear specifications and may benefit from lower temperature settings.

**Best Practices**: Provide clear requirements, specify language, include examples, use lower temperature (0.2-0.4)

**Related**: Temperature, Prompt Engineering, Few-Shot

### Completion

The text generated by the model in response to a prompt. Completion can be a single word, a sentence, a paragraph, or an entire document depending on the task and configuration. The term derives from "language model completion."

**Related**: Generation, Response, Output

### Concurrency

The number of simultaneous API requests an application can handle. Concurrency limits are determined by your quota tier and can be configured at the application level. Higher concurrency requires proper rate limiting and error handling.

**Limits**: Vary by quota tier; Free tier has lower concurrency than paid tiers

**Related**: Rate Limiting, RPM, Quota

### Context

The total information available to the model when generating a response, including system instructions, chat history, user input, and any provided documents or data. Context is bounded by the model's context window.

**Components**: System instruction, prior messages, current input, multimodal data

**Related**: Context Window, System Instruction, Prompt

### Context Cache

See Cached Content

### Context Window

The maximum amount of text (measured in tokens) that can be provided to the model in a single request. The context window includes both input and output tokens. Gemini Ultra supports up to 1M tokens in its extended context window.

| Model | Context Window |
|-------|---------------|
| Gemini 1.5 Flash | 1M tokens |
| Gemini 1.5 Pro | 1M tokens |
| Gemini 1.0 Pro | 128K tokens |

**Related**: Token, Input Tokens, Output Tokens

### Content Generation

The process of producing text, images, audio, or video using the Gemini model. Content generation is the primary use case for the API and supports various modalities including text, images, audio, video, and documents.

**Types**: Text generation, multimodal generation, code generation, structured output generation

**Related**: Generation, Completion, Multimodal

### Content Safety

See Safety Filtering

### Conversation

See Chat History

### Corpus

A collection of text or documents used for reference, training, or context in AI applications. In the Gemini context, corpus often refers to a set of documents made searchable through grounding or RAG (Retrieval Augmented Generation).

**Related**: Grounding, RAG, Document Search

## D

### Dangerous Content

A harm category in Gemini's safety filtering system that blocks content describing how to create or use weapons, harmful substances, or other dangerous activities. This category is distinct from hate speech or harassment.

**Threshold Levels**: BLOCK_NONE, BLOCK_ONLY_HIGH, BLOCK_MEDIUM_AND_ABOVE, BLOCK_LOW_AND_ABOVE

**Related**: Safety Settings, Harm Categories, Content Filtering

### Data Loss Prevention (DLP)

Security measures to prevent sensitive data from being exposed through API requests or responses. DLP should be implemented at the application layer before sending data to the API and after receiving responses.

**Implementation**: Input validation, PII detection, output filtering, audit logging

**Related**: Security, PII, Data Protection

### Demonstration

See Few-Shot Example

### Deployment Environment

The specific infrastructure context where the Gemini API is accessed from. The two primary options are AI Studio (for development and prototyping) and Vertex AI (for production with enterprise features).

| Environment | Use Case | Features |
|-------------|----------|----------|
| AI Studio | Development, prototyping | Free tier, quick setup |
| Vertex AI | Production | Enterprise security, IAM, VPC |

**Related**: AI Studio, Vertex AI, Production

### Distinctive Capability

A unique feature or strength of Gemini compared to other AI models. Gemini's distinctive capabilities include native multimodal processing, extremely large context windows, and deep integration with Google Cloud services.

**Key Capabilities**: Multimodal (text, image, audio, video), 1M token context, function calling, grounding

**Related**: Multimodal, Context Window, Function Calling

### Dynamic Retrieval

See Grounding with Dynamic Retrieval

## E

### Embedding

A numerical representation of text as a vector of numbers that captures semantic meaning. Embeddings enable similarity search, clustering, and other machine learning tasks. Gemini can generate embeddings through a separate embedding model.

**Use Cases**: Semantic search, document similarity, recommendation systems, clustering

**Related**: Vector, Semantic Search, Embedding Model

### Embedding Model

A specialized model that converts text into vector embeddings. Google's embedding models (like text-embedding-004) produce fixed-size vectors that can be compared using distance metrics like cosine similarity.

**Related**: Embedding, Vector Database, Similarity Search

### Endpoint

A URL where API requests are sent. Gemini has different endpoints for different operations and API versions. Endpoints follow REST conventions and support both synchronous and streaming requests.

**Example**: `https://generativelanguage.googleapis.com/v1beta1/models/gemini-1.5-pro:generateContent`

**Related**: REST API, URL, Base URL

### Enumerated Safety Setting

See Threshold Level

### Evaluation

The process of measuring Gemini's output quality for a specific task or use case. Evaluation involves defining metrics, creating test datasets, and comparing outputs against baselines or ground truth.

**Metrics**: Accuracy, BLEU, ROUGE, custom task-specific metrics

**Related**: Benchmarking, Testing, Quality

### Exact Match (EM)

An evaluation metric that checks if the model's output exactly matches the expected output. EM is commonly used for classification, extraction, and structured prediction tasks.

**Related**: Evaluation, F1 Score, Accuracy

### Execution Time

See Latency

### Experimental Model

A model variant that is not yet generally available and may have limited stability or support. Experimental models are used to test new features before they become stable. Production applications should use stable model versions.

**Example**: Gemini Ultra with 1M context (experimental)

**Related**: Stable Version, Model Version, Preview

## F

### Fine-tuning

The process of customizing a base model on specific data to improve performance for a particular task. Gemini API supports fine-tuning through Vertex AI, allowing customization while using managed infrastructure.

**Use Cases**: Domain-specific applications, style customization, improved accuracy for specific tasks

**Related**: Training, Transfer Learning, Vertex AI

### Flash Model

A Gemini model variant optimized for speed and efficiency. Gemini Flash models are ideal for high-volume applications where latency is critical and can process requests faster than Pro models at lower cost.

**Characteristics**: Fast inference, lower cost, slightly reduced quality vs Pro

**Use Cases**: Real-time applications, high-volume processing, cost-sensitive applications

**Related**: Pro Model, Ultra Model, Model Selection

### Forward Filling

A technique where empty or null values in the model's output are filled with the most recent non-empty value. Useful for tasks like form completion or structured data extraction.

**Related**: Completion, Structured Output, JSON Mode

### Frequency Penalty

A generation parameter that reduces the likelihood of repeatedly generating the same tokens. Higher frequency penalties encourage more diverse outputs. Gemini implements this through its generation configuration.

**Range**: 0.0 to 2.0 (typical)

**Related**: Presence Penalty, Repetition, Diversity

### Full Self-Consistency

See Self-Consistency

### Function Call

A mechanism that allows the model to request execution of external functions or APIs during text generation. The model generates a structured response indicating which function to call and with what arguments.

**Process**: Model requests function → Application executes → Results returned → Model continues

**Related**: Function Declaration, Tool Use, Function Calling

### Function Declaration

A structured definition of a function that can be called by the model. Includes the function name, description, and parameter schema. Function declarations must be provided to the model to enable function calling.

**Components**: name, description, parameters (JSON Schema format)

**Related**: Function Call, Tool, Function Calling

### Function Calling

A Gemini feature that enables the model to invoke external functions and use the results in its response. Function calling is essential for building agents, chatbots, and applications that need to interact with external systems.

**Example Use Cases**: Database queries, API calls, file operations, calculations

**Related**: Function Declaration, Tool Use, Function Call

## G

### Gemini

Google's family of multimodal AI models. Gemini models are designed to understand and process text, images, audio, video, and code. Available in various sizes (Ultra, Pro, Nano) optimized for different use cases.

**Models**: Gemini Ultra (most capable), Gemini Pro (balanced), Gemini Nano (on-device)

**Related**: Vertex AI, AI Studio, Multimodal

### Gemini API

The REST API and client libraries for interacting with Gemini models. Provides endpoints for text generation, multimodal processing, function calling, and other AI capabilities.

**Related**: REST API, Client Library, Google Cloud

### Generation

The process of creating content using the model. Generation encompasses text completion, image creation, code generation, and multimodal content creation.

**Related**: Completion, Content Generation, Output

### Generation Config

Configuration parameters that control how the model generates content. Includes settings for temperature, max tokens, top-K, top-P, stop sequences, and response format.

**Parameters**: maxOutputTokens, temperature, topP, topK, stopSequences, responseMimeType

**Related**: Temperature, Top-K, Top-P, Stop Sequences

### Grounding

Connecting model outputs to verified external data sources to improve accuracy and reduce hallucinations. Grounding uses Google Search or Vertex AI Search to provide real-time information to the model.

**Benefits**: More accurate responses, reduced hallucinations, real-time information

**Related**: RAG, Vertex AI Search, Dynamic Retrieval

## H

### Hallucination

When an AI model generates content that appears plausible but is actually incorrect, fabricated, or not supported by its training data. Hallucination is a known limitation of all language models and should be addressed through grounding, verification, and appropriate safety measures.

**Mitigation**: Grounding, fact-checking, citations, structured output validation

**Related**: Grounding, Safety, Accuracy

### Harm Category

A classification of potentially harmful content types that Gemini's safety system can detect and filter. Each category has configurable threshold levels for blocking.

**Categories**: Hate Speech, Dangerous Content, Sexual Explicit Content, Harassment

**Related**: Safety Settings, Threshold Level, Content Filtering

### Harassment

A harm category targeting content that attacks or demeans individuals or groups based on protected characteristics. Includes slurs, discriminatory language, and intimidation.

**Related**: Hate Speech, Dangerous Content, Safety Filtering

### Hate Speech

Content that attacks or uses pejorative or discriminatory language with reference to a protected characteristic. Gemini's safety system can detect and block hate speech across multiple languages.

**Related**: Harassment, Dangerous Content, Safety Settings

### High/Medium/Low Threshold

See Threshold Level

## I

### Image Understanding

Gemini's capability to analyze, describe, extract information from, and reason about images. Image understanding is a core multimodal capability that supports document processing, visual question answering, and image analysis.

**Use Cases**: Document extraction, visual Q&A, image classification, chart analysis

**Related**: Multimodal, Vision, Image Processing

### Inference

The process of using a trained model to generate predictions or content. In Gemini context, inference refers to making API calls to generate responses.

**Metrics**: Latency, throughput, cost per request

**Related**: Generation, API Call, Request

### Input Token

A unit of text (typically 4 characters or partial words) that counts toward the model's input context. Token counting determines API costs and whether content fits within context limits.

**Calculation**: Approximately 4 characters per English token; varies by language

**Related**: Output Token, Token Count, Context Window

### Integration Layer

The middleware or service that connects your application to the Gemini API. The integration layer handles authentication, request formatting, response parsing, error handling, and other cross-cutting concerns.

**Components**: API client, authentication, retry logic, rate limiting, logging

**Related**: API Client, Middleware, Service Layer

## J

### JSON Mode

A generation configuration that instructs the model to output valid JSON. JSON Mode is useful for structured data extraction, API responses, and programmatic processing of model outputs.

**Configuration**: `responseMimeType: "application/json"`

**Related**: Structured Output, Response Format, Schema

## L

### Large Language Model (LLM)

A neural network trained on vast amounts of text data to understand and generate human language. Gemini is an LLM with multimodal capabilities. LLMs can perform various language tasks through prompting rather than task-specific training.

**Related**: Foundation Model, Generative AI, Neural Network

### Latency

The time delay between sending a request and receiving a response. Latency is measured from the API perspective and includes network transit, model processing, and response transmission. Streaming can reduce perceived latency.

**Metrics**: Time to First Token (TTFT), Time Per Output Token (TPOT), End-to-End Latency

**Related**: Streaming, Response Time, Performance

### Leading Token

The first token generated by the model in a response. In streaming mode, the time to generate the leading token is an important latency metric.

**Related**: Latency, Streaming, Time to First Token

### Log Probability

The natural logarithm of the probability assigned to a token by the model's probability distribution. Log probabilities are useful for evaluating model confidence and implementing downstream filtering.

**Range**: Negative values (more negative = less likely)

**Related**: Probability, Confidence, Token Probability

## M

### Maximum Output Tokens

A generation parameter that sets the maximum length of the generated response. This parameter helps control costs and ensures responses don't exceed expected lengths. If the model needs more tokens to complete, it may stop before reaching this limit.

**Setting**: `generationConfig.maxOutputTokens`

**Considerations**: Response type (short answer vs. essay), cost implications

**Related**: Token, Context Window, Generation Config

### Message

A single unit of conversational exchange in the chat API. Messages have roles (user, model, system) and content (text, images, or other data). The conversation history consists of messages.

**Structure**: `{ role: "user" | "model" | "system", parts: [...] }`

**Related**: Chat History, Role, Parts

### Model

A trained AI system capable of generating content. In Gemini context, model refers to specific versions like "gemini-1.5-pro" or "gemini-1.5-flash" with different capabilities and performance characteristics.

**Variants**: Ultra (most capable), Pro (balanced), Flash (fast), Nano (efficient)

**Related**: Model Version, Model Selection, API Model

### Model Selection

The process of choosing the appropriate Gemini model for a specific use case. Selection involves balancing capability, cost, latency, and availability requirements.

**Factors**: Task complexity, volume, latency requirements, budget, availability

**Related**: Pro Model, Flash Model, Model Comparison

### Model Version

A specific release of a Gemini model. Model versions may have different capabilities, performance characteristics, or availability. Versions follow naming conventions like "gemini-1.5-pro-002".

**Considerations**: Stability, features, deprecation policies

**Related**: Model, API Version, Experimental Model

### Multimodal

The ability to process and generate multiple types of data (text, images, audio, video) in a single model. Gemini's multimodal capability is a key differentiator enabling diverse applications.

**Input Types**: Text, images, audio, video, PDFs, documents

**Related**: Multimodal Input, Multimodal Generation, Vision

### Multimodal Generation

Generating content in multiple modalities, such as creating images from text descriptions or generating text descriptions of images. Gemini supports both multimodal input processing and cross-modal generation.

**Examples**: Text-to-image, image captioning, visual question answering

**Related**: Multimodal, Content Generation, Vision

### Multimodal Input

Input data in formats other than plain text, such as images, audio files, or videos. Gemini's multimodal capability allows these inputs to be processed alongside or combined with text.

**Supported**: Images (JPEG, PNG, WebP, GIF), audio (WAV, MP3, OGG), video (MP4, MOV)

**Related**: Multimodal, Inline Data, Image Input

## N

### N-Best

A technique to generate multiple candidate responses and select the best one based on additional criteria. N-Best is useful when deterministic selection isn't optimal and you want to compare alternatives.

**Configuration**: `generationConfig.n`

**Related**: Candidate Count, Self-Consistency, Ensemble

### Native Multimodal

See Multimodal

### Natural Language Generation (NLG)

The AI task of producing human-readable text. In Gemini context, NLG refers to the core capability of generating coherent, contextually appropriate text responses.

**Related**: Generation, Text Generation, Content Generation

### Nucleus Sampling

See Top-P Sampling

## O

### Observation

The result or response from executing a function or tool. In function calling workflows, observations are returned to the model to continue generation with the function results.

**Related**: Function Call, Tool Use, Function Response

### Output

The content generated by the model in response to a request. Output can be text, structured data, function calls, or multimodal content depending on the task and configuration.

**Related**: Generation, Completion, Response

### Output Token

A unit of text generated by the model that counts toward the output token limit and cost. Output tokens are priced differently (usually higher) than input tokens.

**Pricing**: Typically 2-5x higher than input token pricing

**Related**: Input Token, Token Count, Cost

## P

### Part

A discrete unit of content within a message or request. Parts can contain text, images, audio, video, or function call data. A message can contain multiple parts of different types.

**Types**: Text part, inline data part (images, audio), function call part, function response part

**Related**: Message, Content, Multimodal

### Permission

Access rights defined through IAM that control who or what can access Gemini resources. Permissions are bundled into roles and assigned to principals.

**Related**: IAM, Role, Service Account

### Presence Penalty

A generation parameter that encourages the model to discuss new topics by penalizing tokens that have already appeared. Higher presence penalties result in more diverse, less repetitive outputs.

**Range**: 0.0 to 2.0 (typical)

**Related**: Frequency Penalty, Diversity, Repetition

### Prompt

The input provided to the model to generate a response. A prompt can include instructions, context, examples, and the actual query. Well-designed prompts are crucial for achieving desired outputs.

**Components**: Task description, context, examples, query

**Related**: System Instruction, Few-Shot, Prompt Engineering

### Prompt Engineering

The discipline of designing and optimizing prompts to achieve specific outputs from AI models. Prompt engineering includes techniques like few-shot learning, chain-of-thought, and structured output.

**Techniques**: Few-shot, chain-of-thought, system instructions, output formatting

**Related**: Prompt, Few-Shot, System Instruction

### Prompt Injection

A security vulnerability where malicious input attempts to override or manipulate the model's behavior through the prompt. Prompt injection can be used to bypass safety measures or extract sensitive information.

**Prevention**: Input validation, output filtering, proper architecture

**Related**: Security, Prompt, Safety

### Pro Model

A Gemini model variant that balances capability and efficiency. Pro models are suitable for most production applications requiring good quality without the highest cost of Ultra models.

**Characteristics**: Balanced quality/speed/cost, good for general purpose

**Related**: Flash Model, Ultra Model, Model Selection

### Production

The live environment where an application serves real users. Production deployments require careful consideration of reliability, scalability, security, and monitoring.

**Requirements**: High availability, monitoring, error handling, cost management

**Related**: Deployment, Vertex AI, AI Studio

### Project ID

A unique identifier for a Google Cloud project. The project ID is required for API authentication and resource management. Each project can have its own quotas, billing, and access controls.

**Format**: Lowercase letters, numbers, hyphens (e.g., my-gemini-project)

**Related**: GCP, Authentication, Project Number

## Q

### Quality

A measure of how well the model's output meets the requirements of the task. Quality is subjective and task-dependent, often evaluated through human assessment or automated metrics.

**Dimensions**: Accuracy, coherence, relevance, helpfulness, safety

**Related**: Evaluation, Benchmark, Metrics

### Quantization

A model optimization technique that reduces precision of weights (e.g., from 32-bit to 8-bit) to decrease size and improve inference speed. Quantization may slightly reduce accuracy but enables deployment on more constrained hardware.

**Related**: Optimization, Model Size, Performance

### Query

The user's input or question in a request. The query is typically the core question or instruction that the model should respond to, distinct from context or system instructions.

**Related**: Prompt, User Input, Question

### Quota

The allowed amount of API usage, typically measured in requests per minute (RPM), tokens per minute (TPM), or requests per day. Quotas prevent abuse and ensure fair resource allocation.

**Types**: RPM (requests per minute), TPM (tokens per minute), RPD (requests per day)

**Related**: Rate Limiting, Rate Limit, Limits

### Quota Exceeded

An error condition when API usage exceeds the allocated quota. When quota is exceeded, requests are rejected with a 429 error until the quota resets or is increased.

**Handling**: Retry with backoff, request quota increase, implement caching

**Related**: Rate Limiting, Quota, Error Handling

## R

### RAG

See Retrieval Augmented Generation

### Rate Limit

The maximum number of requests or tokens allowed within a time window. Rate limits are enforced to prevent abuse and ensure service stability. Exceeding rate limits results in 429 errors.

**Types**: Hard limits (cannot exceed) vs. soft limits (warnings)

**Related**: Quota, RPM, TPM

### Rate Limiting

A technique to control API usage by limiting the number or frequency of requests. Application-level rate limiting protects against quota exhaustion and ensures fair resource sharing.

**Implementation**: Token bucket, sliding window, fixed window algorithms

**Related**: Rate Limit, Quota, Throttling

### Reasoning

The model's ability to process information, draw conclusions, and solve problems. Gemini's reasoning capabilities support chain-of-thought prompting, mathematical problem-solving, and complex decision-making.

**Techniques**: Chain-of-thought, few-shot reasoning, self-consistency

**Related**: Chain-of-Thought, Prompting, Problem Solving

### Repetition Penalty

See Frequency Penalty

### Request

A single API call to the Gemini API. Each request includes the model name, input content, and configuration parameters. Requests consume quota and incur costs based on token usage.

**Components**: Model, contents, generationConfig, safetySettings, systemInstruction

**Related**: API Call, Response, Quota

### Request ID

A unique identifier assigned to each API request for tracking and debugging. Request IDs are returned in response headers and are useful for troubleshooting and support.

**Format**: UUID or similar unique string

**Related**: Logging, Debugging, Support

### Response

The output returned by the API after processing a request. A response includes the generated content, usage statistics, safety ratings, and metadata.

**Components**: candidates, usageMetadata, safetyRatings, promptFeedback

**Related**: Request, Output, Generation

### Response Format

The structure and type of the model's output. Gemini supports various response formats including plain text, JSON, and function calls.

**Options**: text/plain, application/json, function call format

**Related**: JSON Mode, Structured Output, Schema

### Retrieval Augmented Generation (RAG)

A technique that combines information retrieval with text generation. RAG retrieves relevant documents from a corpus and includes them in the prompt to improve response accuracy and reduce hallucinations.

**Benefits**: Grounded responses, reduced hallucinations, up-to-date information

**Related**: Grounding, Corpus, Context

### Role

The participant in a conversation indicating the source of content. Roles include "user" (human input), "model" (AI response), and "system" (instructions).

**Values**: user, model, system

**Related**: Message, Chat History, System Instruction

### Root Cause Analysis

The process of investigating errors or issues to identify their underlying cause. Root cause analysis for API issues may involve checking logs, quotas, configuration, or network connectivity.

**Related**: Troubleshooting, Debugging, Error Handling

### RPM

See Requests Per Minute

## S

### Safety Block

When content is prevented from being generated or processed due to safety filter triggers. Safety blocks can occur on input or output and result in specific block reasons being returned.

**Handling**: Check block reasons, adjust thresholds, modify input, provide user feedback

**Related**: Safety Filtering, Blocked Content, Safety Settings

### Safety Category

See Harm Category

### Safety Filter

See Safety Filtering

### Safety Filtering

The process of detecting and blocking content that violates safety guidelines. Safety filtering operates on both input (to the model) and output (from the model) based on configurable thresholds.

**Categories**: Hate Speech, Dangerous Content, Sexual Explicit Content, Harassment

**Related**: Safety Settings, Harm Category, Threshold Level

### Safety Rating

An assessment of potentially harmful content in a response. Safety ratings are returned with each response and indicate the likelihood and severity of content in each harm category.

**Fields**: category, probability, probabilityScore, severity, severityScore

**Related**: Safety Settings, Harm Category, Blocked Content

### Safety Setting

Configuration parameters that control what content is filtered or blocked. Safety settings define threshold levels for each harm category, determining when content should be blocked.

**Configuration**: Category + Threshold level

**Related**: Threshold Level, Safety Filtering, Harm Category

### Schema

A structured definition of expected data format. In function declarations, schemas define the parameters the model can request. In JSON mode, schemas can define expected output structure.

**Format**: JSON Schema format for parameters and output

**Related**: Function Declaration, JSON Mode, Structured Output

### SDK

Software Development Kit - libraries and tools that simplify API integration. Google provides SDKs for multiple languages including Python, Node.js, and Go.

**Related**: Client Library, API Client, Documentation

### Search Grounding

See Grounding with Google Search

### Self-Consistency

A technique that generates multiple reasoning paths and selects the most consistent answer. Self-consistency can improve accuracy for complex reasoning tasks by identifying the most reliable conclusion.

**Implementation**: Generate N responses, aggregate answers, select most common

**Related**: N-Best, Reasoning, Chain-of-Thought

### Semantics

The meaning conveyed by text, as opposed to its literal characters. Semantic understanding enables models to grasp context, nuance, and intent beyond simple pattern matching.

**Related**: Semantic Search, Embedding, Meaning

### Service Account

A Google Cloud identity used by applications to authenticate to Google APIs. Service accounts are preferred over API keys for production applications due to better security and audit capabilities.

**Related**: API Key, Authentication, IAM

### Session

A persistent conversation context that maintains chat history across multiple requests. Sessions enable multi-turn conversations where the model remembers previous interactions.

**Management**: Store and pass conversation history, manage context within limits

**Related**: Chat History, Context, Multi-Turn

### Stop Sequence

A string that causes generation to stop when encountered. Stop sequences are useful for controlling output length or preventing the model from generating unwanted content.

**Configuration**: `generationConfig.stopSequences`

**Related**: Generation Config, Max Output Tokens

### Streaming

A mode where the response is delivered incrementally as tokens are generated, rather than waiting for the complete response. Streaming reduces perceived latency and enables progressive display.

**Benefits**: Faster perceived response, real-time feedback, better UX

**Related**: Latency, Time to First Token, Progressive Display

### Streaming Chunk

A partial response received during streaming mode. Each chunk contains incremental text that can be displayed to the user before the complete response is available.

**Related**: Streaming, Token, Partial Response

### Structured Data

Information organized in a defined format, typically JSON, XML, or tabular format. Gemini can both consume and generate structured data, enabling integration with APIs and data pipelines.

**Use Cases**: API responses, data extraction, form completion

**Related**: JSON Mode, Schema, Structured Output

### Structured Output

Generation configured to produce responses in a specific format, typically JSON. Structured output enables programmatic processing and integration with downstream systems.

**Configuration**: `responseMimeType: "application/json"`, optional schema

**Related**: JSON Mode, Schema, Response Format

### System Instruction

Persistent instructions that define the model's behavior, role, or context. System instructions are applied to every request in a conversation and guide the model's overall approach.

**Use**: Define persona, set rules, provide context

**Related**: Prompt, Role, Instructions

## T

### Temperature

A generation parameter controlling randomness in token selection. Lower temperatures produce more focused, deterministic outputs; higher temperatures produce more creative, diverse outputs.

**Range**: 0.0 (deterministic) to 2.0 (very creative)

**Recommendations**: 0.1-0.3 for coding/facts, 0.7-1.0 for creative tasks

**Related**: Top-K, Top-P, Generation Config

### Threshold Level

The sensitivity setting for each safety category, determining what probability levels trigger content blocking.

**Levels**: BLOCK_NONE, BLOCK_ONLY_HIGH, BLOCK_MEDIUM_AND_ABOVE, BLOCK_LOW_AND_ABOVE

**Related**: Safety Settings, Harm Category, Content Filtering

### Time Per Output Token (TPOT)

The average time to generate each output token. TPOT is a latency metric that indicates generation speed and is useful for estimating total response time.

**Related**: Latency, TTFT, Throughput

### Time to First Token (TTFT)

The time elapsed before the first token of the response is received. TTFT is an important metric for streaming responses and user experience.

**Related**: Latency, Streaming, TTFT

### Token

The basic unit of text processed by the model. Tokens are approximately 4 characters for English text but vary by language and content type. Both input and output are measured in tokens.

**Examples**: "hello" = 1 token, "tokenization" might be 2-3 tokens

**Related**: Token Count, Input Token, Output Token

### Token Budget

The maximum tokens allowed for a request, including both input and output. Token budgets help control costs and ensure responses stay within expected lengths.

**Related**: Token Count, Context Window, Max Output Tokens

### Token Count

The number of tokens in a piece of text. Token counting is essential for estimating costs, checking context limits, and optimizing API usage.

**Estimation**: ~4 characters per English token, varies by language

**Related**: Token, Input Token, Output Token

### Token Limitation

The maximum tokens allowed for input, output, or total context. Token limitations are determined by model capabilities and quota tiers.

**Related**: Token Budget, Context Window, Limits

### Token Probability

The likelihood assigned to each possible next token by the model. Token probabilities are used in nucleus sampling (top-P) to select tokens from the most probable portion of the distribution.

**Related**: Top-P, Sampling, Probability Distribution

### TPM

See Tokens Per Minute

### Tokens Per Minute (TPM)

A rate limit measuring the total tokens (input + output) processed per minute. TPM limits are independent of request count, making them important for applications with variable request sizes.

**Related**: RPM, Quota, Rate Limit

### Tool

An external capability that can be invoked during generation. In Gemini context, tools are defined through function declarations and enable the model to interact with external systems.

**Related**: Function Calling, Function Declaration, Tool Use

### Tool Use

The process of invoking a tool during generation. When the model determines that a tool would help fulfill the request, it generates a function call that the application executes.

**Related**: Function Calling, Tool, Function Call

### Top-K Sampling

A generation technique that limits token selection to the K most probable options. Lower K values produce more focused outputs; higher K values increase diversity.

**Range**: 1 (greedy) to 40-100 (more diverse)

**Related**: Top-P, Temperature, Sampling

### Top-P Sampling

A generation technique that selects tokens from the smallest set of highest-probability tokens that sum to P. Top-P provides a dynamic alternative to top-K that adapts to the probability distribution.

**Range**: 0.0 to 1.0 (typically 0.9-0.95)

**Related**: Top-K, Temperature, Sampling

### Training

The process of developing a model's capabilities, typically on large datasets. Training produces the weights and parameters that define model behavior. Gemini models are pre-trained by Google.

**Related**: Fine-tuning, Model, Pre-training

### Turn

A single exchange in a conversation, consisting of a user message and model response. Multi-turn conversations track context across multiple turns.

**Related**: Multi-Turn, Chat History, Session

## U

### Ultra Model

The most capable Gemini model variant, designed for complex reasoning, research, and demanding applications. Ultra models offer the highest quality at the highest cost.

**Characteristics**: Best quality, highest cost, longest latency

**Use Cases**: Complex reasoning, research, high-stakes applications

**Related**: Pro Model, Flash Model, Model Selection

### Ungrounded

Content generated without reference to external verification or context. Ungrounded content relies solely on the model's training data and may contain hallucinations or outdated information.

**Risks**: Hallucinations, outdated information, lack of citations

**Related**: Grounding, Hallucination, RAG

## V

### Validation

The process of verifying that outputs meet requirements. Validation can be automated (schema validation, rule checking) or human (review, assessment).

**Methods**: Schema validation, output format checks, quality metrics, human review

**Related**: Structured Output, Quality, Evaluation

### Vertex AI

Google Cloud's managed ML platform that provides access to Gemini models with enterprise features. Vertex AI offers enhanced security, IAM integration, VPC support, and additional capabilities beyond AI Studio.

**Features**: IAM, VPC, managed infrastructure, additional APIs

**Related**: AI Studio, Google Cloud, Production

### Vision

See Image Understanding

## W

### Warm-up Request

An initial API call made to initialize model resources before production traffic. Warm-up requests can reduce cold-start latency for latency-sensitive applications.

**Related**: Latency, Cold Start, Initialization

### Whisper Tuning

The process of providing detailed instructions or examples to refine model behavior for a specific use case. Similar to fine-tuning but done through prompting rather than training.

**Related**: Fine-tuning, Few-Shot, System Instruction

## References

- [Google Gemini API Documentation](https://ai.google.dev/docs/gemini_api)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Safety Settings Guide](https://ai.google.dev/docs/safety_guidance)
- [Function Calling Documentation](https://ai.google.dev/docs/function_calling)
- [Model Information](https://ai.google.dev/models/gemini)
