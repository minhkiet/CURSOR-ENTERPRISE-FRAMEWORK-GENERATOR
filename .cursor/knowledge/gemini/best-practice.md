---
title: "Gemini Best Practices - Thực Hành Tốt Nhất"
description: "Comprehensive guide on best practices for Google Gemini API integration, including effective prompting, multimodal inputs, function calling, and context window management"
tags: ["gemini", "google-ai", "best-practices", "llm", "vertex-ai", "prompt-engineering"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Gemini Best Practices - Thực Hành Tối Ưu

## Tổng Quan (Overview)

Google Gemini API cung cấp một loạt các khả năng mạnh mẽ cho việc xây dựng ứng dụng AI đa phương thức. Để tận dụng tối đa các capabilities của Gemini, developers cần nắm vững các best practices được kiểm chứng qua nhiều dự án production. Tài liệu này tổng hợp các best practices theo từng lĩnh vực cụ thể.

Trong Cursor Enterprise Framework, việc tích hợp Gemini đòi hỏi không chỉ việc gọi API đúng cách mà còn phải tối ưu hóa về chi phí, hiệu suất, và trải nghiệm người dùng. Các best practices được trình bày ở đây đã được rút ra từ kinh nghiệm triển khai thực tế và được validate qua nhiều enterprise projects.

Mỗi phần trong tài liệu này bao gồm lý thuyết nền tảng, code examples thực tế, và các recommendations cụ thể có thể áp dụng ngay vào dự án của bạn.

## Mục Đích (Purpose)

Tài liệu này được thiết kế để:

1. **Hướng dẫn prompt engineering hiệu quả** với các techniques đã được chứng minh
2. **Cung cấp patterns cho multimodal inputs** tối ưu hóa cho image, audio, và video
3. **Giải thích function calling patterns** để tích hợp Gemini với external systems
4. **Hướng dẫn context window management** để tối ưu hóa token usage và cost

## Khái Niệm Chính (Key Concepts)

### 1. Prompt Engineering Fundamentals

Prompt engineering là nghệ thuật và khoa học của việc thiết kế inputs để có được desired outputs từ language models. Với Gemini, prompt engineering đặc biệt quan trọng vì model's capabilities có thể được tận dụng tối đa thông qua well-crafted prompts. Các nguyên tắc cơ bản bao gồm specificity, structure, và context provision.

Specificity đề cập đến việc cung cấp rõ ràng những gì model cần làm. Thay vì ask "Explain this code", hãy ask "Explain what this function does, its parameters, return value, and potential side effects." Structure liên quan đến việc tổ chức prompt một cách logic, sử dụng delimiters, numbered lists, và clear sections. Context provision nghĩa là cung cấp background information cần thiết để model hiểu bối cảnh của request.

### 2. Multimodal Processing

Gemini's multimodal capabilities cho phép xử lý đồng thời text, images, audio, và video trong một single request. Điều này mở ra khả năng mạnh mẽ cho applications như document understanding, visual question answering, và audio transcription. Tuy nhiên, để đạt được kết quả tốt nhất, developers cần hiểu cách format và truyền các loại data khác nhau một cách hiệu quả.

Image inputs cần được optimize về size và quality để balance giữa visual information và token cost. Audio inputs require proper sampling và format conversion. Video inputs nên được xử lý frame-by-frame hoặc sử dụng sampling strategies để capture key moments.

### 3. Function Calling Architecture

Function calling cho phép Gemini trigger external functions và sử dụng kết quả trong quá trình generation. Đây là một pattern mạnh mẽ để xây dựng agents và chatbots có thể interact với external systems như databases, APIs, và services. Proper function declaration và response handling là key to successful implementation.

### 4. Context Management Strategy

Context window là một trong những strengths của Gemini, với models hỗ trợ đến 1M tokens. Tuy nhiên, efficient context management vẫn rất quan trọng để optimize costs và maintain performance. Strategies bao gồm smart truncation, summarization, và caching.

## Best Practices Chi Tiết

### Best Practice #1: Effective Prompt Design

#### System Instructions vs User Prompts

Gemini hỗ trợ system instructions cho việc set model behavior một cách persistent. System instructions được áp dụng trước user messages và giúp establish model's role, tone, và constraints. Đây là cách hiệu quả để define persistent behaviors như "You are a helpful coding assistant" hoặc "Always respond in JSON format."

```typescript
// System instruction cho coding assistant
const codingModel = vertexai.getGenerativeModel({
  model: 'gemini-1.5-pro',
  systemInstruction: {
    role: 'system',
    parts: [{
      text: `You are an expert software engineer specializing in TypeScript and Node.js.
      
      Guidelines:
      - Always write type-safe code with proper TypeScript types
      - Follow SOLID principles
      - Include error handling in all async functions
      - Use async/await instead of callbacks
      - Export interfaces separately from implementations
      - Add JSDoc comments for complex logic
      
      Response format:
      - Provide code in proper markdown code blocks
      - Include explanation before or after code
      - List any assumptions made`
    }]
  }
});

// System instruction cho data analyst
const analyticsModel = vertexai.getGenerativeModel({
  model: 'gemini-1.5-pro',
  systemInstruction: {
    role: 'system',
    parts: [{
      text: `You are a data analyst assistant that helps users understand their data.
      
      Capabilities:
      - Statistical analysis and interpretation
      - Data visualization recommendations
      - Trend identification
      - Anomaly detection insights
      
      Output format:
      - Always start with key findings
      - Use bullet points for multiple insights
      - Include confidence levels for predictions
      - Suggest next steps for deeper analysis`
    }]
  }
});
```

#### Few-Shot Examples

Few-shot learning là kỹ thuật cung cấp examples trong prompt để guide model output. Examples giúp model understand format, tone, và expectations cho specific tasks. Đây là cách hiệu quả để handle complex tasks mà khó describe in text alone.

```typescript
interface FewShotExample {
  input: string;
  output: string;
  reasoning?: string;
}

const classificationExamples: FewShotExample[] = [
  {
    input: "This product exceeded my expectations!",
    output: "positive"
  },
  {
    input: "Arrived on time and works perfectly.",
    output: "positive"
  },
  {
    input: "Poor quality and slow shipping.",
    output: "negative"
  },
  {
    input: "The item was damaged when it arrived.",
    output: "negative"
  },
  {
    input: "It's okay, nothing special.",
    output: "neutral"
  }
];

function buildFewShotPrompt(
  task: string,
  examples: FewShotExample[],
  newInput: string
): string {
  const exampleSection = examples.map((ex, i) => 
    `Example ${i + 1}:\nInput: "${ex.input}"\nOutput: ${ex.output}`
  ).join('\n\n');
  
  return `Task: ${task}

${exampleSection}

Now classify this input:
Input: "${newInput}"
Output:`;
}

async function classifyWithFewShot(
  input: string,
  category: string
): Promise<string> {
  const examples = getExamplesForCategory(category);
  const prompt = buildFewShotPrompt(
    `Classify the sentiment of the input as: positive, negative, or neutral`,
    examples,
    input
  );
  
  const result = await model.generateContent(prompt);
  return result.response.text().trim().toLowerCase();
}
```

#### Chain of Thought Prompting

Chain of thought prompting encourages model to show reasoning steps before giving final answer. Điều này đặc biệt hữu ích cho complex reasoning tasks như math problems, logical deduction, và multi-step analysis.

```typescript
const chainOfThoughtPrompt = `Solve this problem step by step. For each step:
1. Show your reasoning
2. Explain why you chose this approach
3. Calculate the result

Problem: A store has 150 items. They sell 3/5 of them on Monday and 1/3 of the remaining on Tuesday. How many items are left?

Let's think through this step by step:

Step 1: Calculate items sold on Monday
- Total items: 150
- Fraction sold: 3/5
- Items sold: 150 × (3/5) = 90 items
- Remaining: 150 - 90 = 60 items

Step 2: Calculate items sold on Tuesday
- Remaining after Monday: 60
- Fraction sold: 1/3
- Items sold: 60 × (1/3) = 20 items
- Remaining: 60 - 20 = 40 items

Final Answer: 40 items remain in the store.`;

async function solveWithChainOfThought(
  problem: string,
  showWork: boolean = true
): Promise<{
  answer: string;
  steps?: string[];
}> {
  const prompt = showWork
    ? `${problem}\n\nSolve this step by step, showing your reasoning.`
    : problem;
  
  const result = await model.generateContent({
    contents: [{ role: 'user', parts: [{ text: prompt }] }],
    generationConfig: {
      maxOutputTokens: 1024,
      temperature: 0.3, // Lower temperature for more deterministic reasoning
    }
  });
  
  const response = result.response.text();
  
  if (showWork) {
    const steps = extractSteps(response);
    const answer = extractFinalAnswer(response);
    return { answer, steps };
  }
  
  return { answer: response };
}
```

#### Structured Output

For tasks requiring structured data, specify format explicitly in prompt. Use JSON schema, XML tags, or specific delimiters to help model output parseable content.

```typescript
interface StructuredPromptConfig {
  format: 'json' | 'xml' | 'delimited';
  schema?: Record<string, unknown>;
  includeExamples?: boolean;
}

function buildStructuredPrompt(
  task: string,
  data: Record<string, unknown>,
  config: StructuredPromptConfig
): string {
  let formatInstructions = '';
  
  switch (config.format) {
    case 'json':
      formatInstructions = `Respond ONLY with valid JSON matching this schema:
${JSON.stringify(config.schema || {}, null, 2)}`;
      break;
      
    case 'xml':
      formatInstructions = `Respond ONLY with XML tags:
${buildXMLSchema(config.schema || {})}`;
      break;
      
    case 'delimited':
      formatInstructions = `Respond with pipe-delimited values in this order:
${Object.keys(config.schema || {}).join(' | ')}`;
      break;
  }
  
  return `${task}

Data to process:
${JSON.stringify(data, null, 2)}

${formatInstructions}`;
}

// Example: Extract structured information from text
const extractionPrompt = buildStructuredPrompt(
  'Extract contact information from the text below',
  { text: 'Contact John at john@example.com or call 555-1234' },
  {
    format: 'json',
    schema: {
      name: 'Person name',
      email: 'Email address',
      phone: 'Phone number'
    }
  }
);

async function extractStructuredData<T>(
  text: string,
  schema: Record<string, string>
): Promise<T> {
  const prompt = buildStructuredPrompt(
    `Extract the following fields from the text`,
    { text },
    { format: 'json', schema }
  );
  
  const result = await model.generateContent(prompt);
  const response = result.response.text();
  
  // Parse and validate
  try {
    return JSON.parse(extractJSON(response)) as T;
  } catch {
    throw new Error(`Failed to parse response as JSON: ${response}`);
  }
}
```

### Best Practice #2: Multimodal Input Optimization

#### Image Optimization

Images là một trong những input phổ biến nhất cho Gemini's multimodal capabilities. Tuy nhiên, image size và quality ảnh hưởng đáng kể đến token count và latency. Best practice là optimize images trước khi send to API.

```typescript
interface ImageOptimizationOptions {
  maxDimension: number;
  quality: number;
  format: 'jpeg' | 'png' | 'webp';
  preserveAspectRatio: boolean;
}

const PRESETS = {
  thumbnail: {
    maxDimension: 256,
    quality: 70,
    format: 'jpeg' as const,
    preserveAspectRatio: true,
  },
  preview: {
    maxDimension: 512,
    quality: 80,
    format: 'jpeg' as const,
    preserveAspectRatio: true,
  },
  analysis: {
    maxDimension: 1024,
    quality: 85,
    format: 'jpeg' as const,
    preserveAspectRatio: true,
  },
  highQuality: {
    maxDimension: 1536,
    quality: 90,
    format: 'png' as const,
    preserveAspectRatio: true,
  },
};

class ImageOptimizer {
  async optimize(
    imageBuffer: Buffer,
    preset: keyof typeof PRESETS
  ): Promise<{ buffer: Buffer; mimeType: string; dimensions: Dimensions }> {
    const config = PRESETS[preset];
    
    // Get image metadata
    const metadata = await this.getImageMetadata(imageBuffer);
    
    // Calculate resize dimensions
    const dimensions = this.calculateDimensions(
      metadata.width,
      metadata.height,
      config.maxDimension,
      config.preserveAspectRatio
    );
    
    // Resize and compress
    const optimized = await this.processImage(imageBuffer, {
      width: dimensions.width,
      height: dimensions.height,
      quality: config.quality,
      format: config.format,
    });
    
    return {
      buffer: optimized,
      mimeType: `image/${config.format}`,
      dimensions,
    };
  }
  
  private calculateDimensions(
    origWidth: number,
    origHeight: number,
    maxDimension: number,
    preserveRatio: boolean
  ): Dimensions {
    if (!preserveRatio) {
      return { width: maxDimension, height: maxDimension };
    }
    
    if (origWidth <= maxDimension && origHeight <= maxDimension) {
      return { width: origWidth, height: origHeight };
    }
    
    const ratio = Math.min(maxDimension / origWidth, maxDimension / origHeight);
    return {
      width: Math.round(origWidth * ratio),
      height: Math.round(origHeight * ratio),
    };
  }
  
  private async processImage(
    buffer: Buffer,
    options: ProcessOptions
  ): Promise<Buffer> {
    // Implementation using Sharp or similar library
    // return await sharp(buffer)
    //   .resize(options.width, options.height)
    //   .toFormat(options.format, { quality: options.quality })
    //   .toBuffer();
    return buffer; // Placeholder
  }
  
  private async getImageMetadata(buffer: Buffer): Promise<ImageMetadata> {
    // Implementation using Sharp or similar
    return { width: 1920, height: 1080 }; // Placeholder
  }
}

// Usage với proper optimization
async function analyzeImageContent(
  imageBuffer: Buffer,
  query: string
): Promise<string> {
  // Optimize image for analysis
  const optimized = await imageOptimizer.optimize(imageBuffer, 'analysis');
  
  // Create multimodal content
  const result = await visionModel.generateContent({
    contents: [{
      role: 'user',
      parts: [
        {
          inlineData: {
            mimeType: optimized.mimeType,
            data: optimized.buffer.toString('base64'),
          },
        },
        { text: query },
      ],
    }],
  });
  
  return result.response.text();
}
```

#### Audio Processing

Audio inputs require proper format conversion và sampling rate configuration. Gemini hỗ trợ various audio formats và có thể transcribe hoặc analyze audio content.

```typescript
interface AudioProcessingConfig {
  sampleRate: number;
  channels: number;
  format: 'wav' | 'mp3' | 'ogg';
  maxDurationSeconds: number;
}

const DEFAULT_AUDIO_CONFIG: AudioProcessingConfig = {
  sampleRate: 16000, // Optimal for speech recognition
  channels: 1,       // Mono
  format: 'wav',     // WAV provides best compatibility
  maxDurationSeconds: 60, // Gemini has limits on audio length
};

class AudioProcessor {
  async processAudio(
    audioBuffer: Buffer,
    config: Partial<AudioProcessingConfig> = {}
  ): Promise<{ buffer: Buffer; duration: number; config: AudioProcessingConfig }> {
    const finalConfig = { ...DEFAULT_AUDIO_CONFIG, ...config };
    
    // Check duration
    const duration = this.calculateDuration(audioBuffer, finalConfig);
    if (duration > finalConfig.maxDurationSeconds) {
      throw new Error(`Audio exceeds maximum duration of ${finalConfig.maxDurationSeconds}s`);
    }
    
    // Convert to compatible format
    const processed = await this.convertAudio(audioBuffer, finalConfig);
    
    return {
      buffer: processed,
      duration,
      config: finalConfig,
    };
  }
  
  async transcribeAudio(
    audioBuffer: Buffer,
    language?: string
  ): Promise<TranscriptionResult> {
    const processed = await this.processAudio(audioBuffer);
    
    const prompt = language
      ? `Transcribe this audio in ${language}. Include speaker identification if possible.`
      : 'Transcribe this audio. Include speaker identification if possible.';
    
    const result = await model.generateContent({
      contents: [{
        role: 'user',
        parts: [
          {
            inlineData: {
              mimeType: 'audio/wav',
              data: processed.buffer.toString('base64'),
            },
          },
          { text: prompt },
        ],
      }],
    });
    
    return {
      text: result.response.text(),
      duration: processed.duration,
      language: language || 'auto-detected',
    };
  }
  
  async summarizeAudio(
    audioBuffer: Buffer,
    summaryType: 'brief' | 'detailed' | 'action-items'
  ): Promise<string> {
    const processed = await this.processAudio(audioBuffer);
    
    const promptTemplates = {
      brief: 'Provide a brief 2-3 sentence summary of this audio.',
      detailed: 'Provide a detailed summary with key points and important details.',
      'action-items': 'Extract all action items, decisions, and follow-up tasks mentioned in this audio.',
    };
    
    const result = await model.generateContent({
      contents: [{
        role: 'user',
        parts: [
          {
            inlineData: {
              mimeType: 'audio/wav',
              data: processed.buffer.toString('base64'),
            },
          },
          { text: promptTemplates[summaryType] },
        ],
      }],
    });
    
    return result.response.text();
  }
  
  private calculateDuration(
    buffer: Buffer,
    config: AudioProcessingConfig
  ): number {
    // WAV header parsing or metadata-based calculation
    const bytesPerSample = 2; // 16-bit audio
    const bytesPerSecond = config.sampleRate * config.channels * bytesPerSample;
    return buffer.length / bytesPerSecond;
  }
  
  private async convertAudio(
    buffer: Buffer,
    config: AudioProcessingConfig
  ): Promise<Buffer> {
    // Implementation using ffmpeg or audio processing library
    return buffer; // Placeholder
  }
}
```

#### Document Processing Pipeline

```typescript
interface DocumentProcessingConfig {
  extractText: boolean;
  extractTables: boolean;
  extractImages: boolean;
  ocrLanguage?: string;
  pageRange?: { start: number; end: number };
}

class DocumentProcessor {
  async processDocument(
    documentBuffer: Buffer,
    mimeType: string,
    config: DocumentProcessingConfig
  ): Promise<DocumentResult> {
    const results: DocumentResult = {
      pages: [],
      text: '',
      tables: [],
      images: [],
    };
    
    // Process each page
    const pages = await this.splitPages(documentBuffer, mimeType);
    const pageRange = config.pageRange || { start: 0, end: pages.length };
    
    for (let i = pageRange.start; i < pageRange.end; i++) {
      const page = pages[i];
      const pageResult = await this.processPage(page, config);
      results.pages.push(pageResult);
      
      if (config.extractText) {
        results.text += `\n--- Page ${i + 1} ---\n${pageResult.text}`;
      }
      if (config.extractTables) {
        results.tables.push(...pageResult.tables);
      }
      if (config.extractImages) {
        results.images.push(...pageResult.images);
      }
    }
    
    return results;
  }
  
  private async processPage(
    page: Buffer,
    config: DocumentProcessingConfig
  ): Promise<PageResult> {
    // Convert to image for analysis
    const image = await this.convertToImage(page);
    const optimized = await imageOptimizer.optimize(image, 'analysis');
    
    const prompt = this.buildDocumentPrompt(config);
    
    const result = await visionModel.generateContent({
      contents: [{
        role: 'user',
        parts: [
          {
            inlineData: {
              mimeType: optimized.mimeType,
              data: optimized.buffer.toString('base64'),
            },
          },
          { text: prompt },
        ],
      }],
    });
    
    return this.parseDocumentResponse(result.response.text(), config);
  }
  
  private buildDocumentPrompt(config: DocumentProcessingConfig): string {
    const tasks: string[] = [];
    
    if (config.extractText) {
      tasks.push('- Extract all text content');
    }
    if (config.extractTables) {
      tasks.push('- Identify and extract tables in JSON format');
    }
    if (config.extractImages) {
      tasks.push('- Note any embedded images and their descriptions');
    }
    
    return `Analyze this document page and provide:

${tasks.join('\n')}

Format tables as:
{
  "tables": [
    {
      "headers": [...],
      "rows": [[...], ...]
    }
  ]
}

Return all extracted data in a structured format.`;
  }
}
```

### Best Practice #3: Function Calling Patterns

#### Function Declaration Best Practices

Well-designed function declarations are crucial for successful function calling. Each function should have clear name, description, và properly defined parameters với types và constraints.

```typescript
// Comprehensive function declaration examples
const functionDeclarations = [
  // Database query function
  {
    name: 'query_database',
    description: `Searches the internal database for records matching the given criteria.
    
    Use this function when:
    - User asks about specific data records
    - User wants to filter or search records
    - User needs statistics or aggregations
    
    Returns matching records with all relevant fields.`,
    parameters: {
      type: 'object',
      properties: {
        table: {
          type: 'string',
          description: 'The database table to query',
          enum: ['users', 'orders', 'products', 'inventory', 'transactions']
        },
        filters: {
          type: 'object',
          description: 'Key-value pairs for filtering results',
          additionalProperties: {
            type: 'string'
          }
        },
        limit: {
          type: 'integer',
          description: 'Maximum number of results to return',
          default: 50,
          minimum: 1,
          maximum: 1000
        },
        orderBy: {
          type: 'string',
          description: 'Field to sort results by (prefix with - for descending)'
        }
      },
      required: ['table']
    }
  },
  
  // Calculator function for math operations
  {
    name: 'calculate',
    description: `Performs mathematical calculations with high precision.
    
    Supports:
    - Basic arithmetic (+, -, *, /)
    - Advanced math (power, sqrt, log, sin, cos)
    - Unit conversions
    - Percentage calculations
    
    Always use this for numerical computations.`,
    parameters: {
      type: 'object',
      properties: {
        expression: {
          type: 'string',
          description: 'Mathematical expression to evaluate (e.g., "2 + 3 * 4" or "sqrt(16) + 5")'
        },
        precision: {
          type: 'integer',
          description: 'Number of decimal places in result',
          default: 2,
          minimum: 0,
          maximum: 10
        },
        unit: {
          type: 'string',
          description: 'Optional unit for result conversion',
          enum: ['USD', 'EUR', 'GBP', 'kg', 'lb', 'm', 'ft', 'celsius', 'fahrenheit']
        }
      },
      required: ['expression']
    }
  },
  
  // Weather lookup function
  {
    name: 'get_weather',
    description: `Retrieves current weather or forecast for a location.
    
    Provides:
    - Current temperature and conditions
    - 5-day forecast
    - Precipitation chances
    - Wind speed and direction
    
    Always specify units for temperature.`,
    parameters: {
      type: 'object',
      properties: {
        location: {
          type: 'string',
          description: 'City name, address, or coordinates (lat,lng)',
          examples: ['San Francisco, CA', '40.7128,-74.0060']
        },
        units: {
          type: 'string',
          description: 'Temperature unit preference',
          enum: ['celsius', 'fahrenheit'],
          default: 'celsius'
        },
        forecast: {
          type: 'string',
          description: 'Type of weather data needed',
          enum: ['current', 'hourly', 'daily', 'all'],
          default: 'current'
        }
      },
      required: ['location']
    }
  },
  
  // Email/send message function
  {
    name: 'send_notification',
    description: `Sends a notification or message to users.
    
    Can send:
    - Email notifications
    - In-app notifications
    - SMS messages (if configured)
    
    Requires valid user ID and message content.`,
    parameters: {
      type: 'object',
      properties: {
        userId: {
          type: 'string',
          description: 'The user ID to send notification to'
        },
        channel: {
          type: 'string',
          description: 'Notification channel',
          enum: ['email', 'sms', 'push', 'in_app']
        },
        subject: {
          type: 'string',
          description: 'Subject line for email notifications'
        },
        message: {
          type: 'string',
          description: 'The notification message content',
          maxLength: 5000
        },
        priority: {
          type: 'string',
          description: 'Message priority level',
          enum: ['low', 'normal', 'high', 'urgent'],
          default: 'normal'
        }
      },
      required: ['userId', 'channel', 'message']
    }
  }
];

// Complete function calling implementation
class FunctionCallingHandler {
  private functions: Map<string, FunctionImplementation>;
  
  constructor() {
    this.functions = new Map();
    this.registerDefaultFunctions();
  }
  
  registerFunction(
    name: string,
    implementation: FunctionImplementation
  ): void {
    this.functions.set(name, implementation);
  }
  
  async handleFunctionCalls(
    calls: FunctionCall[],
    chatHistory: ChatMessage[]
  ): Promise<FunctionResponse[]> {
    const responses: FunctionResponse[] = [];
    
    for (const call of calls) {
      const implementation = this.functions.get(call.name);
      
      if (!implementation) {
        responses.push({
          name: call.name,
          success: false,
          error: `Unknown function: ${call.name}`
        });
        continue;
      }
      
      try {
        const result = await implementation(call.args);
        responses.push({
          name: call.name,
          success: true,
          result
        });
      } catch (error) {
        responses.push({
          name: call.name,
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error'
        });
      }
    }
    
    return responses;
  }
  
  private registerDefaultFunctions(): void {
    this.registerFunction('query_database', async (args) => {
      const { table, filters, limit, orderBy } = args;
      return await db.query(table, { where: filters, limit, orderBy });
    });
    
    this.registerFunction('calculate', async (args) => {
      const { expression, precision, unit } = args;
      const result = math.evaluate(expression);
      const converted = unit ? this.convertUnit(result, unit) : result;
      return Number(converted.toFixed(precision || 2));
    });
    
    this.registerFunction('get_weather', async (args) => {
      const { location, units, forecast } = args;
      return await weatherService.getWeather(location, units, forecast);
    });
    
    this.registerFunction('send_notification', async (args) => {
      const { userId, channel, subject, message, priority } = args;
      return await notificationService.send({ userId, channel, subject, message, priority });
    });
  }
  
  private convertUnit(value: number, unit: string): number {
    // Unit conversion logic
    return value;
  }
}
```

#### Multi-Turn Function Calling

Complex tasks often require multiple function calls in sequence. Implement proper state management và result handling for these scenarios.

```typescript
class MultiTurnFunctionCaller {
  private model: GenerativeModel;
  private handler: FunctionCallingHandler;
  private maxTurns: number = 5;
  
  async execute(
    initialPrompt: string,
    context?: Record<string, unknown>
  ): Promise<ExecutionResult> {
    const history: ChatTurn[] = [];
    let currentPrompt = initialPrompt;
    let contextData = context || {};
    
    for (let turn = 0; turn < this.maxTurns; turn++) {
      // Generate response with function calling
      const generationResult = await this.model.generateContent({
        contents: [{
          role: 'user',
          parts: [{ text: currentPrompt }]
        }],
        tools: [{ functionDeclarations }]
      });
      
      const response = generationResult.response;
      history.push({ role: 'user', content: currentPrompt });
      
      // Check for function calls
      const functionCalls = response.functionCalls();
      
      if (!functionCalls || functionCalls.length === 0) {
        // No more function calls, return final response
        return {
          finalResponse: response.text(),
          functionCalls: history.filter(t => t.functionCalls).length,
          turns: turn + 1
        };
      }
      
      // Execute function calls
      history.push({ role: 'model', content: '', functionCalls });
      
      const functionResponses = await this.handler.handleFunctionCalls(
        functionCalls,
        history
      );
      
      // Update context with results
      for (const funcResponse of functionResponses) {
        if (funcResponse.success) {
          contextData[funcResponse.name] = funcResponse.result;
        }
      }
      
      // Prepare for next turn
      currentPrompt = this.formatFunctionResponses(functionResponses);
    }
    
    return {
      finalResponse: 'Maximum turns exceeded',
      functionCalls: this.maxTurns,
      turns: this.maxTurns,
      error: 'Could not complete in maximum turns'
    };
  }
  
  private formatFunctionResponses(responses: FunctionResponse[]): string {
    return responses.map(r => {
      if (r.success) {
        return `Function ${r.name} returned: ${JSON.stringify(r.result)}`;
      }
      return `Function ${r.name} failed: ${r.error}`;
    }).join('\n');
  }
}
```

### Best Practice #4: Context Window Management

#### Smart Context Truncation

When dealing with long conversations or documents, implement smart truncation strategies to stay within context limits while preserving important information.

```typescript
interface TruncationStrategy {
  preserveSystemPrompt: boolean;
  preserveRecentMessages: number;
  preserveUserPreferences: boolean;
  summarizationThreshold: number;
}

const DEFAULT_TRUNCATION: TruncationStrategy = {
  preserveSystemPrompt: true,
  preserveRecentMessages: 10,
  preserveUserPreferences: true,
  summarizationThreshold: 0.8, // Summarize when 80% of context used
};

class ContextManager {
  private model: GenerativeModel;
  private maxTokens: number;
  private truncationStrategy: TruncationStrategy;
  
  constructor(
    model: GenerativeModel,
    maxTokens: number = 128000,
    strategy: Partial<TruncationStrategy> = {}
  ) {
    this.model = model;
    this.maxTokens = maxTokens;
    this.truncationStrategy = { ...DEFAULT_TRUNCATION, ...strategy };
  }
  
  async prepareContext(
    messages: ChatMessage[],
    systemPrompt?: string
  ): Promise<ContextResult> {
    // Calculate available token budget
    const systemPromptTokens = systemPrompt 
      ? await this.countTokens(systemPrompt) 
      : 0;
    
    const reservedTokens = systemPromptTokens + 
      (this.truncationStrategy.preserveRecentMessages * 50); // Estimate per message
    
    const availableTokens = this.maxTokens - reservedTokens;
    const usedPercentage = availableTokens / this.maxTokens;
    
    // Determine strategy based on usage
    if (usedPercentage > this.truncationStrategy.summarizationThreshold) {
      return this.summarizeAndTruncate(messages, availableTokens, systemPrompt);
    }
    
    return this.truncatePreservingStructure(messages, availableTokens, systemPrompt);
  }
  
  private async summarizeAndTruncate(
    messages: ChatMessage[],
    tokenBudget: number,
    systemPrompt?: string
  ): Promise<ContextResult> {
    // Separate messages to summarize from recent ones to keep
    const recentMessages = messages.slice(-this.truncationStrategy.preserveRecentMessages);
    const olderMessages = messages.slice(0, -this.truncationStrategy.preserveRecentMessages);
    
    // Summarize older messages
    const summary = await this.summarizeMessages(olderMessages);
    
    // Build final context
    const context = {
      systemPrompt,
      summary,
      recentMessages
    };
    
    const tokens = await this.countTokens(JSON.stringify(context));
    
    return {
      context,
      tokens,
      truncated: true,
      strategy: 'summarized'
    };
  }
  
  private async truncatePreservingStructure(
    messages: ChatMessage[],
    tokenBudget: number,
    systemPrompt?: string
  ): Promise<ContextResult> {
    const result: ChatMessage[] = [];
    let currentTokens = 0;
    
    // Process messages from oldest to newest
    for (const message of messages.reverse()) {
      const messageTokens = await this.countTokens(message.content);
      
      if (currentTokens + messageTokens <= tokenBudget) {
        result.unshift(message);
        currentTokens += messageTokens;
      } else {
        // Truncate this message if it's the user's latest message
        if (message.role === 'user' && result.length === 0) {
          const truncatedContent = await this.truncateToTokenBudget(
            message.content,
            tokenBudget - currentTokens
          );
          result.unshift({ ...message, content: truncatedContent });
        }
        break;
      }
    }
    
    return {
      context: {
        systemPrompt,
        messages: result
      },
      tokens: currentTokens,
      truncated: currentTokens < await this.countTokens(JSON.stringify(messages)),
      strategy: 'truncated'
    };
  }
  
  private async summarizeMessages(messages: ChatMessage[]): Promise<string> {
    const conversation = messages.map(m => `${m.role}: ${m.content}`).join('\n');
    
    const summaryPrompt = `Summarize this conversation concisely, preserving key information:

${conversation}

Summary should include:
- Main topics discussed
- Key decisions or conclusions
- Any unresolved issues
- Important context for continuing the conversation`;

    const result = await this.model.generateContent({
      contents: [{ role: 'user', parts: [{ text: summaryPrompt }] }],
      generationConfig: { maxOutputTokens: 500 }
    });
    
    return `[Previous conversation summary]: ${result.response.text()}`;
  }
  
  private async truncateToTokenBudget(text: string, maxTokens: number): Promise<string> {
    const words = text.split(/\s+/);
    let currentWords: string[] = [];
    
    for (const word of words) {
      const test = currentWords.concat(word).join(' ');
      const tokens = await this.countTokens(test);
      
      if (tokens > maxTokens) {
        break;
      }
      
      currentWords.push(word);
    }
    
    return currentWords.join(' ') + '... [truncated]';
  }
  
  private async countTokens(text: string): Promise<number> {
    // Use Gemini's token counting API or approximation
    return Math.ceil(text.length / 4);
  }
}
```

#### Context Caching for Repeated Use

Context caching allows you to cache frequently used content and reduce costs for repeated queries.

```typescript
class ContextCachingService {
  private cache: Map<string, CachedContext> = new Map();
  private apiCache: Map<string, string> = new Map(); // API-level cache names
  
  async createCache(
    contextId: string,
    content: string,
    ttlSeconds: number = 3600
  ): Promise<CacheInfo> {
    const tokenCount = await this.countTokens(content);
    const now = Date.now();
    
    const cachedContext: CachedContext = {
      content,
      tokenCount,
      createdAt: now,
      expiresAt: now + (ttlSeconds * 1000),
      accessCount: 0
    };
    
    this.cache.set(contextId, cachedContext);
    
    // Optionally create API-level cache via Vertex AI
    if (this.useVertexAI) {
      const apiCacheName = await this.createAPICache(content, ttlSeconds);
      this.apiCache.set(contextId, apiCacheName);
    }
    
    return {
      contextId,
      tokenCount,
      cacheHit: false
    };
  }
  
  async getCachedContent(
    contextId: string,
    additionalPrompt: string
  ): Promise<CachedQueryResult> {
    const cached = this.cache.get(contextId);
    
    if (!cached) {
      return { hit: false, content: null };
    }
    
    if (Date.now() > cached.expiresAt) {
      this.cache.delete(contextId);
      this.apiCache.delete(contextId);
      return { hit: false, content: null };
    }
    
    cached.accessCount++;
    const additionalTokens = await this.countTokens(additionalPrompt);
    
    return {
      hit: true,
      content: cached.content,
      tokenCount: cached.tokenCount,
      additionalTokens,
      apiCacheName: this.apiCache.get(contextId)
    };
  }
  
  async queryWithCache(
    contextId: string,
    query: string
  ): Promise<QueryResult> {
    const cached = await this.getCachedContent(contextId, query);
    
    if (!cached.hit) {
      throw new Error(`Cache miss for context: ${contextId}`);
    }
    
    const startTime = Date.now();
    const result = await this.executeQuery(cached, query);
    const latency = Date.now() - startTime;
    
    // Calculate cost savings
    const withoutCache = cached.tokenCount + cached.additionalTokens;
    const withCache = cached.additionalTokens;
    const savingsPercent = ((withoutCache - withCache) / withoutCache) * 100;
    
    return {
      result,
      latency,
      cacheHit: true,
      tokensSaved: withoutCache - withCache,
      costSavings: savingsPercent
    };
  }
  
  private async executeQuery(
    cached: CachedQueryResult,
    query: string
  ): Promise<string> {
    if (cached.apiCacheName) {
      // Use API-level cache
      return await this.queryWithAPICache(cached.apiCacheName, query);
    }
    
    // Fall back to standard query with context
    const prompt = `${cached.content}\n\nQuery: ${query}`;
    const result = await model.generateContent(prompt);
    return result.response.text();
  }
  
  private async queryWithAPICache(
    cacheName: string,
    query: string
  ): Promise<string> {
    // Vertex AI cached content query
    const result = await model.generateContent({
      contents: [{ role: 'user', parts: [{ text: query }] }],
      cachedContent: cacheName
    });
    return result.response.text();
  }
}
```

## Common Patterns

### Pattern 1: Chat Interface

```typescript
interface ChatMessage {
  role: 'user' | 'model';
  content: string;
  timestamp: number;
}

class GeminiChat {
  private history: ChatMessage[] = [];
  private contextManager: ContextManager;
  
  async send(message: string): Promise<string> {
    this.history.push({
      role: 'user',
      content: message,
      timestamp: Date.now()
    });
    
    const context = await this.contextManager.prepareContext(
      this.history,
      this.systemPrompt
    );
    
    const result = await model.generateContent({
      ...context.context,
      generationConfig: {
        maxOutputTokens: 2048,
        temperature: 0.7,
        topP: 0.95,
      }
    });
    
    const response = result.response.text();
    
    this.history.push({
      role: 'model',
      content: response,
      timestamp: Date.now()
    });
    
    return response;
  }
  
  clearHistory(): void {
    this.history = [];
  }
  
  getHistory(): ChatMessage[] {
    return [...this.history];
  }
}
```

### Pattern 2: Batch Processing

```typescript
class BatchProcessor {
  async processBatch(
    items: BatchItem[],
    options: BatchOptions = {}
  ): Promise<BatchResult[]> {
    const {
      concurrency = 5,
      model = 'gemini-1.5-flash',
      onProgress = () => {}
    } = options;
    
    const results: BatchResult[] = [];
    const semaphore = new Semaphore(concurrency);
    
    const promises = items.map((item, index) =>
      semaphore.acquire().then(async () => {
        try {
          const result = await this.processItem(item, model);
          results[index] = { success: true, result };
        } catch (error) {
          results[index] = { 
            success: false, 
            error: error instanceof Error ? error.message : 'Unknown error' 
          };
        } finally {
          semaphore.release();
          onProgress(results.filter(r => r).length, items.length);
        }
      })
    );
    
    await Promise.all(promises);
    return results;
  }
  
  private async processItem(item: BatchItem, model: string): Promise<string> {
    const result = await model.generateContent({
      contents: [{ role: 'user', parts: [{ text: item.prompt }] }],
      generationConfig: { maxOutputTokens: 1024 }
    });
    return result.response.text();
  }
}
```

## Troubleshooting

### High Latency Issues

**Symptoms**: Responses taking longer than expected

**Solutions**:
1. Check if using appropriate model tier (Flash vs Pro)
2. Optimize input size and format
3. Enable streaming for better perceived performance
4. Check network latency to API endpoint
5. Consider using regional endpoints

### Inconsistent Outputs

**Symptoms**: Model producing varying quality or format outputs

**Solutions**:
1. Lower temperature for more deterministic outputs
2. Add more specific instructions in prompt
3. Use few-shot examples
4. Implement output validation
5. Consider using structured output mode

### High Costs

**Symptoms**: Unexpectedly high API bills

**Solutions**:
1. Implement token budgets per request
2. Use context caching for repeated queries
3. Select appropriate model tier per use case
4. Add usage monitoring and alerts
5. Optimize prompt length

## Examples

### Example 1: Complete Production Service

```typescript
interface GeminiServiceConfig {
  model: 'gemini-1.5-pro' | 'gemini-1.5-flash';
  temperature: number;
  maxOutputTokens: number;
  safetySettings: SafetySetting[];
  enableCaching: boolean;
  rateLimitRPM: number;
}

class ProductionGeminiService {
  private model: GenerativeModel;
  private cache: ContextCachingService;
  private rateLimiter: RateLimitedClient;
  
  constructor(config: GeminiServiceConfig) {
    this.model = vertexai.getGenerativeModel({
      model: config.model,
      generationConfig: {
        temperature: config.temperature,
        maxOutputTokens: config.maxOutputTokens,
      },
      safetySettings: config.safetySettings,
    });
    
    this.cache = new ContextCachingService(config.enableCaching);
    this.rateLimiter = new RateLimitedClient(
      this.model,
      undefined,
      config.rateLimitRPM
    );
  }
  
  async generate(options: GenerateOptions): Promise<GenerateResult> {
    const startTime = Date.now();
    
    try {
      // Check cache if enabled
      if (options.cacheKey) {
        const cached = await this.cache.getCachedContent(
          options.cacheKey,
          options.prompt
        );
        
        if (cached.hit) {
          return {
            text: cached.content,
            cached: true,
            latency: Date.now() - startTime
          };
        }
      }
      
      // Generate with rate limiting
      const result = await this.rateLimiter.withRetry(() =>
        this.model.generateContent({
          contents: [{ role: 'user', parts: [{ text: options.prompt }] }],
          systemInstruction: options.systemPrompt ? {
            role: 'system',
            parts: [{ text: options.systemPrompt }]
          } : undefined,
        })
      );
      
      const text = result.response.text();
      
      // Cache result if cache key provided
      if (options.cacheKey && text) {
        await this.cache.createCache(options.cacheKey, text);
      }
      
      return {
        text,
        cached: false,
        latency: Date.now() - startTime
      };
      
    } catch (error) {
      return {
        error: this.parseError(error),
        latency: Date.now() - startTime
      };
    }
  }
}
```

### Example 2: Multimodal Document Pipeline

```typescript
class MultimodalDocumentPipeline {
  async process(
    document: DocumentInput,
    options: ProcessingOptions
  ): Promise<DocumentProcessingResult> {
    const results: DocumentProcessingResult = {
      documentId: document.id,
      text: '',
      tables: [],
      images: [],
      summary: '',
      entities: []
    };
    
    // Step 1: Extract text and structure
    if (options.extractText || options.extractTables) {
      const extractionResult = await this.extractTextAndStructure(document);
      results.text = extractionResult.text;
      results.tables = extractionResult.tables;
    }
    
    // Step 2: Process images
    if (options.extractImages && document.images) {
      results.images = await this.processImages(document.images);
    }
    
    // Step 3: Generate summary
    if (options.generateSummary && results.text) {
      results.summary = await this.generateSummary(results.text);
    }
    
    // Step 4: Extract entities
    if (options.extractEntities && results.text) {
      results.entities = await this.extractEntities(results.text);
    }
    
    return results;
  }
  
  private async extractTextAndStructure(
    document: DocumentInput
  ): Promise<{ text: string; tables: Table[] }> {
    // Convert document pages to images and analyze
    const pageImages = await this.convertDocumentToImages(document);
    const optimizedImages = await Promise.all(
      pageImages.map(img => imageOptimizer.optimize(img, 'analysis'))
    );
    
    const prompt = `Extract all text and identify tables from this document.
Return in JSON format:
{
  "text": "full extracted text",
  "tables": [
    {"headers": [...], "rows": [[...], ...]}
  ]
}`;
    
    const results = await Promise.all(
      optimizedImages.map(img => visionModel.generateContent({
        contents: [{
          role: 'user',
          parts: [
            { inlineData: { mimeType: img.mimeType, data: img.buffer.toString('base64') } },
            { text: prompt }
          ]
        }]
      }))
    );
    
    // Combine results from all pages
    return this.combinePageResults(results);
  }
}
```

## References

- [Google Gemini API Documentation](https://ai.google.dev/docs/gemini_api)
- [Vertex AI Gemini Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/overview)
- [Prompt Engineering Guide](https://ai.google.dev/gemini-api/docs/prompting)
- [Function Calling Documentation](https://ai.google.dev/docs/function_calling)
- [Context Caching Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/context-cache)
- [Token Counting API](https://ai.google.dev/docs/token_counting)
- [Gemini Model Versions](https://ai.google.dev/models/gemini)
