---
title: Vision API và Multimodal
description: Hướng dẫn toàn diện về Vision API, image input formats, base64 encoding, token calculation và multimodal use cases
tags: [openai, vision, multimodal, image, gpt-4o, typescript, python]
created: 2026-06-23
version: 1.0.0
framework: cursor-enterprise
---

# Vision API và Multimodal

## Tổng quan

Vision API là một trong những capabilities mạnh mẽ nhất của các model hiện đại như GPT-4o và GPT-4o mini, cho phép models interpret và reason about images không chỉ text. Khả năng này mở ra vô số applications từ document understanding, visual content analysis, medical imaging assistance, đến multimodal conversational interfaces.

OpenAI's Vision implementation cho phép developers include images trong chat completions requests theo nhiều formats khác nhau: URLs, base64-encoded images, hoặc thông qua image URLs từ cloud storage. Models có thể analyze images, describe content, extract information, answer questions về visual content, và thậm chí interpret charts, diagrams, và screenshots.

Understanding cách Vision API hoạt động, cách optimize image inputs cho cost và performance, và cách handle various image types là essential cho building effective multimodal applications. Trong tài liệu này, chúng ta sẽ cover mọi aspect của Vision API từ basic usage đến advanced optimization techniques.

## Mục đích và Phạm vi

Tài liệu này cung cấp hướng dẫn toàn diện về việc sử dụng OpenAI's Vision API cho các ứng dụng enterprise. Phạm vi bao gồm từ basic image input configuration, đến advanced techniques như token calculation, cost optimization, và production deployment patterns.

Chúng tôi sẽ cover practical implementation patterns cho cả TypeScript và Python, với focus on real-world use cases như document processing, visual content analysis, và multimodal chatbots. Các topics bao gồm image formats và quality settings, token estimation, caching strategies, và error handling.

## Các Khái niệm Chính

### Multimodal Models

OpenAI's multimodal models như GPT-4o có khả năng process cả text và images trong single request. Điều này khác với traditional models chỉ handle text, và mở ra khả năng mới cho applications.

**GPT-4o** (flagship model):
- Native multimodal architecture
- Handles text, images, audio, và video
- 128K context window
- Fast response times
- Vision capabilities integrated seamlessly

**GPT-4o mini** (cost-effective option):
- Smaller, faster variant
- Maintains strong vision capabilities
- Lower cost than full GPT-4o
- Good for high-volume applications

**Model Selection Considerations**:
- GPT-4o: Best quality, higher cost
- GPT-4o mini: Good quality, lower cost, faster
- Consider trade-offs based on use case requirements

### Image Input Formats

Vision API hỗ trợ nhiều image input formats, each với pros và cons:

**URL-based Images**:
- Reference external URLs (public or signed)
- No size limit enforced by API
- External image must be accessible
- Best for: Cloud storage, CDNs, public URLs

**Base64-encoded Images**:
- Inline images in request
- Format: `data:image/<type>;base64,<encoded_data>`
- Subject to token limits
- Best for: Local files, private resources, embedded content

**Supported Image Types**:
- JPEG (recommended for photos)
- PNG (recommended for graphics, screenshots)
- WebP (good compression)
- GIF (animated images - first frame only)

### Detail Levels

The `detail` parameter controls how images are processed:

**"low"**:
- Lower resolution processing
- Fewer tokens used
- Faster processing
- Suitable for simple identification tasks

**"high"**:
- Full resolution processing
- More tokens used
- Better for detailed analysis
- Required for reading small text, fine details

**"auto"** (default):
- Model decides based on image size
- Optimizes for cost/quality balance

## Image Processing

### Preprocessing Utilities

```typescript
// utils/imageProcessor.ts - Image preprocessing utilities
import * as fs from 'fs';
import * as path from 'path';

interface ProcessedImage {
  base64: string;
  format: string;
  width: number;
  height: number;
  size: number;
  tokenEstimate: number;
}

interface ImageProcessingOptions {
  maxWidth?: number;
  maxHeight?: number;
  quality?: number; // 0-100 for JPEG
  format?: 'jpeg' | 'png' | 'webp';
  preserveAspectRatio?: boolean;
}

// Image processor using Sharp (Node.js)
export class ImageProcessor {
  private sharp: any; // Sharp library
  
  constructor() {
    // In production, import sharp:
    // import sharp from 'sharp';
  }
  
  async loadFromFile(filePath: string): Promise<Buffer> {
    return fs.promises.readFile(filePath);
  }
  
  async loadFromUrl(url: string): Promise<Buffer> {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch image: ${response.status}`);
    }
    return Buffer.from(await response.arrayBuffer());
  }
  
  async processImage(
    input: Buffer | string,
    options: ImageProcessingOptions = {}
  ): Promise<ProcessedImage> {
    // If string, assume it's a URL or file path
    let buffer: Buffer;
    if (typeof input === 'string') {
      if (input.startsWith('http')) {
        buffer = await this.loadFromUrl(input);
      } else {
        buffer = await this.loadFromFile(input);
      }
    } else {
      buffer = input;
    }
    
    // Get image metadata
    const metadata = await this.getImageMetadata(buffer);
    
    // Calculate resize dimensions
    const dimensions = this.calculateDimensions(
      metadata.width,
      metadata.height,
      options.maxWidth || 2048,
      options.maxHeight || 2048,
      options.preserveAspectRatio !== false
    );
    
    // Process and encode
    const processed = await this.resizeAndEncode(
      buffer,
      dimensions,
      options
    );
    
    return {
      ...processed,
      width: dimensions.width,
      height: dimensions.height,
      size: buffer.length,
      tokenEstimate: this.estimateTokens(processed.base64),
    };
  }
  
  private async getImageMetadata(buffer: Buffer): Promise<{
    width: number;
    height: number;
    format: string;
  }> {
    // Using sharp:
    // const metadata = await sharp(buffer).metadata();
    // return { width: metadata.width, height: metadata.height, format: metadata.format };
    
    // Fallback: return estimates
    return { width: 1920, height: 1080, format: 'jpeg' };
  }
  
  private calculateDimensions(
    originalWidth: number,
    originalHeight: number,
    maxWidth: number,
    maxHeight: number,
    preserveAspect: boolean
  ): { width: number; height: number } {
    if (!preserveAspect) {
      return { width: maxWidth, height: maxHeight };
    }
    
    const aspectRatio = originalWidth / originalHeight;
    
    let width = originalWidth;
    let height = originalHeight;
    
    if (width > maxWidth) {
      width = maxWidth;
      height = width / aspectRatio;
    }
    
    if (height > maxHeight) {
      height = maxHeight;
      width = height * aspectRatio;
    }
    
    // Ensure dimensions are multiples of 2 (required by many encoders)
    return {
      width: Math.floor(width / 2) * 2,
      height: Math.floor(height / 2) * 2,
    };
  }
  
  private async resizeAndEncode(
    buffer: Buffer,
    dimensions: { width: number; height: number },
    options: ImageProcessingOptions
  ): Promise<{ base64: string; format: string }> {
    // Using sharp:
    /*
    const processed = await sharp(buffer)
      .resize(dimensions.width, dimensions.height, {
        fit: 'inside',
        withoutEnlargement: true,
      })
      .toFormat(options.format || 'jpeg', {
        quality: options.quality || 85,
      })
      .toBuffer();
    
    const base64 = processed.toString('base64');
    return { base64, format: options.format || 'jpeg' };
    */
    
    // Fallback: just encode original
    return {
      base64: buffer.toString('base64'),
      format: 'jpeg',
    };
  }
  
  estimateTokens(base64String: string): number {
    // Vision token calculation:
    // Each 256x256 patch = ~170 tokens
    // Base overhead + image data tokens
    
    const imageDataLength = base64String.length;
    const bytesPerToken = 4; // Base64 is ~4 chars per 3 bytes
    
    // Rough estimate based on image size
    // Real calculation depends on actual image dimensions
    return Math.ceil(imageDataLength / bytesPerToken / 6); // Conservative estimate
  }
}

// Screenshot capture utility
export class ScreenshotCapture {
  async captureViewport(url: string): Promise<Buffer> {
    // Using Puppeteer or Playwright:
    /*
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url);
    const screenshot = await page.screenshot();
    await browser.close();
    return screenshot;
    */
    
    throw new Error('Screenshot capture not implemented - integrate Puppeteer/Playwright');
  }
  
  async captureElement(url: string, selector: string): Promise<Buffer> {
    /*
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url);
    const element = await page.$(selector);
    const screenshot = await element.screenshot();
    await browser.close();
    return screenshot;
    */
    
    throw new Error('Element capture not implemented');
  }
}
```

```python
# utils/image_processor.py - Image preprocessing utilities
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass
import base64
import io
from PIL import Image
import requests

@dataclass
class ProcessedImage:
    base64: str
    format: str
    width: int
    height: int
    size: int
    token_estimate: int

class ImageProcessor:
    """Process images for Vision API."""
    
    def __init__(
        self,
        max_width: int = 2048,
        max_height: int = 2048,
        default_quality: int = 85
    ):
        self.max_width = max_width
        self.max_height = max_height
        self.default_quality = default_quality
    
    def load_from_file(self, file_path: str) -> bytes:
        """Load image from file."""
        with open(file_path, 'rb') as f:
            return f.read()
    
    def load_from_url(self, url: str) -> bytes:
        """Load image from URL."""
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    
    def load_from_base64(self, data: str) -> bytes:
        """Load image from base64 string."""
        # Handle data URI format
        if ',' in data:
            data = data.split(',', 1)[1]
        return base64.b64decode(data)
    
    def process_image(
        self,
        input_data: Any,
        format: str = 'jpeg',
        quality: Optional[int] = None,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
    ) -> ProcessedImage:
        """Process image for Vision API."""
        # Load image data
        if isinstance(input_data, str):
            if input_data.startswith('http'):
                image_data = self.load_from_url(input_data)
            elif input_data.startswith('data:'):
                image_data = self.load_from_base64(input_data)
            else:
                image_data = self.load_from_file(input_data)
        elif isinstance(input_data, bytes):
            image_data = input_data
        else:
            raise ValueError('Invalid input type')
        
        # Open with PIL
        image = Image.open(io.BytesIO(image_data))
        
        # Calculate target dimensions
        target_width, target_height = self._calculate_dimensions(
            image.size[0],
            image.size[1],
            max_width or self.max_width,
            max_height or self.max_height
        )
        
        # Resize if needed
        if (target_width, target_height) != image.size:
            image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Convert RGBA to RGB if needed (for JPEG)
        if image.mode == 'RGBA' and format == 'jpeg':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background
        
        # Encode to target format
        output = io.BytesIO()
        image.save(output, format=format.upper(), quality=quality or self.default_quality)
        encoded_data = output.getvalue()
        
        # Encode to base64
        base64_str = base64.b64encode(encoded_data).decode('utf-8')
        
        return ProcessedImage(
            base64=base64_str,
            format=format,
            width=target_width,
            height=target_height,
            size=len(encoded_data),
            token_estimate=self._estimate_tokens(encoded_data, target_width, target_height),
        )
    
    def _calculate_dimensions(
        self,
        width: int,
        height: int,
        max_width: int,
        max_height: int
    ) -> Tuple[int, int]:
        """Calculate resized dimensions maintaining aspect ratio."""
        if width <= max_width and height <= max_height:
            # Ensure dimensions are even (required by encoders)
            return (width // 2) * 2, (height // 2) * 2
        
        aspect_ratio = width / height
        
        if width > height:
            new_width = min(width, max_width)
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(height, max_height)
            new_width = int(new_height * aspect_ratio)
        
        # Ensure dimensions are even
        return (new_width // 2) * 2, (new_height // 2) * 2
    
    def _estimate_tokens(
        self,
        image_data: bytes,
        width: int,
        height: int
    ) -> int:
        """
        Estimate tokens for image.
        GPT-4o with 'high' detail:
        - Each 512x512 patch = ~170 tokens
        - Minimum ~85 tokens for small images
        """
        # Calculate number of 512x512 patches needed
        patches_w = (width + 511) // 512
        patches_h = (height + 511) // 512
        num_patches = patches_w * patches_h
        
        # Base tokens + patch tokens
        base_tokens = 85
        tokens_per_patch = 170
        
        return base_tokens + (num_patches * tokens_per_patch)
    
    def create_vision_content(
        self,
        input_data: Any,
        detail: str = 'high'
    ) -> Dict[str, Any]:
        """Create content object for Vision API."""
        processed = self.process_image(input_data)
        
        return {
            'type': 'image_url',
            'image_url': {
                'url': f'data:image/{processed.format};base64,{processed.base64}',
                'detail': detail,
            }
        }
```

## Token Calculation

### Detailed Token Estimation

```typescript
// utils/visionTokenCalculator.ts - Token calculation for Vision API
interface TokenEstimate {
  totalTokens: number;
  baseTokens: number;
  imageTokens: number;
  textTokens: number;
  breakdown: {
    width: number;
    height: number;
    patches: number;
    patchTokens: number;
  };
}

export function calculateVisionTokens(
  imageWidth: number,
  imageHeight: number,
  detailLevel: 'low' | 'high' | 'auto' = 'high'
): TokenEstimate {
  const baseTokens = 85;
  
  // For 'low' detail, images are downsampled to 512x512
  let width = imageWidth;
  let height = imageHeight;
  let tokensPerPatch = 170;
  
  if (detailLevel === 'low') {
    // Low detail: single 512x512 patch approximation
    return {
      totalTokens: 85 + 85, // base + low detail token
      baseTokens,
      imageTokens: 85,
      textTokens: 0,
      breakdown: {
        width: 512,
        height: 512,
        patches: 1,
        patchTokens: 85,
      },
    };
  }
  
  // For 'high' detail, calculate patches
  // Each patch is 512x512, but they overlap
  const patchSize = 512;
  
  // Calculate number of patches (each patch includes context from neighbors)
  const patchesX = Math.ceil(width / patchSize);
  const patchesY = Math.ceil(height / patchSize);
  
  // GPT-4o uses overlapping patches with context
  // Rough approximation: ~170 tokens per effective patch
  const effectivePatches = patchesX * patchesY;
  const patchTokens = effectivePatches * tokensPerPatch;
  
  return {
    totalTokens: baseTokens + patchTokens,
    baseTokens,
    imageTokens: patchTokens,
    textTokens: 0,
    breakdown: {
      width,
      height,
      patches: effectivePatches,
      patchTokens,
    },
  };
}

// Estimate from base64 string
export function estimateTokensFromBase64(
  base64String: string,
  detailLevel: 'low' | 'high' = 'high'
): TokenEstimate {
  // Estimate dimensions from file size (rough)
  // Average compression ratio for photos: ~0.1 bytes per pixel
  const estimatedPixels = base64String.length / 4 * 3;
  const aspectRatios = [
    [4, 3],
    [16, 9],
    [1, 1],
  ];
  
  // Assume 16:9 for estimation
  const pixels = estimatedPixels * 0.1;
  const width = Math.sqrt(pixels * 16 / 9);
  const height = width * 9 / 16;
  
  return calculateVisionTokens(
    Math.round(width),
    Math.round(height),
    detailLevel
  );
}

// Cost calculator
interface CostEstimate {
  imageCost: number;
  textCost: number;
  totalCost: number;
  detailLevel: string;
}

export function calculateVisionCost(
  imageWidth: number,
  imageHeight: number,
  textTokens: number = 0,
  detailLevel: 'low' | 'high' = 'high',
  model: string = 'gpt-4o'
): CostEstimate {
  const pricing: Record<string, { input: number; output: number }> = {
    'gpt-4o': { input: 2.5, output: 10.0 },
    'gpt-4o-mini': { input: 0.15, output: 0.6 },
  };
  
  const modelPricing = pricing[model] || pricing['gpt-4o'];
  
  const tokenEstimate = calculateVisionTokens(
    imageWidth,
    imageHeight,
    detailLevel
  );
  
  const totalTokens = tokenEstimate.totalTokens + textTokens;
  
  const imageCost = (tokenEstimate.totalTokens / 1_000_000) * modelPricing.input;
  const textCost = (textTokens / 1_000_000) * modelPricing.input;
  
  return {
    imageCost,
    textCost,
    totalCost: imageCost + textCost,
    detailLevel,
  };
}

// Multiple images batch calculation
export function calculateBatchVisionCost(
  images: Array<{
    width: number;
    height: number;
    detailLevel?: 'low' | 'high' | 'auto';
  }>,
  textTokens: number = 0,
  model: string = 'gpt-4o'
): {
  totalTokens: number;
  imageTokens: number;
  textTokens: number;
  totalCost: number;
  perImage: TokenEstimate[];
} {
  const pricing: Record<string, { input: number }> = {
    'gpt-4o': { input: 2.5 },
    'gpt-4o-mini': { input: 0.15 },
  };
  
  const modelPricing = pricing[model] || pricing['gpt-4o'];
  
  let totalImageTokens = 0;
  const perImage: TokenEstimate[] = [];
  
  for (const img of images) {
    const estimate = calculateVisionTokens(
      img.width,
      img.height,
      img.detailLevel || 'high'
    );
    perImage.push(estimate);
    totalImageTokens += estimate.totalTokens;
  }
  
  const totalTokens = totalImageTokens + textTokens;
  const totalCost = (totalTokens / 1_000_000) * modelPricing.input;
  
  return {
    totalTokens,
    imageTokens: totalImageTokens,
    textTokens,
    totalCost,
    perImage,
  };
}
```

```python
# utils/vision_token_calculator.py - Token calculation for Vision API
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class TokenEstimate:
    total_tokens: int
    base_tokens: int
    image_tokens: int
    text_tokens: int
    breakdown: Dict[str, Any]

def calculate_vision_tokens(
    image_width: int,
    image_height: int,
    detail_level: str = 'high'
) -> TokenEstimate:
    """
    Calculate tokens for an image based on dimensions and detail level.
    
    GPT-4o Vision token calculation:
    - Base tokens: 85
    - Each 512x512 patch: ~170 tokens (for 'high' detail)
    - For 'low' detail: ~85 tokens flat
    """
    base_tokens = 85
    
    if detail_level == 'low':
        # Low detail: single patch approximation
        return TokenEstimate(
            total_tokens=85 + 85,
            base_tokens=base_tokens,
            image_tokens=85,
            text_tokens=0,
            breakdown={
                'width': 512,
                'height': 512,
                'patches': 1,
                'patch_tokens': 85,
            }
        )
    
    # For 'high' detail, calculate patches
    patch_size = 512
    
    # Number of 512x512 patches
    patches_x = (image_width + 511) // 512
    patches_y = (image_height + 511) // 512
    num_patches = patches_x * patches_y
    
    # Each patch = ~170 tokens
    tokens_per_patch = 170
    patch_tokens = num_patches * tokens_per_patch
    
    return TokenEstimate(
        total_tokens=base_tokens + patch_tokens,
        base_tokens=base_tokens,
        image_tokens=patch_tokens,
        text_tokens=0,
        breakdown={
            'width': image_width,
            'height': image_height,
            'patches': num_patches,
            'patch_tokens': patch_tokens,
        }
    )

def estimate_tokens_from_base64(base64_string: str) -> TokenEstimate:
    """Estimate tokens from base64 encoded image."""
    import base64
    
    # Estimate image size from base64
    estimated_bytes = len(base64_string) * 3 // 4
    estimated_pixels = estimated_bytes * 0.1  # Compression ratio
    
    # Assume 16:9 aspect ratio
    import math
    pixels = estimated_pixels
    width = int(math.sqrt(pixels * 16 / 9))
    height = int(width * 9 / 16)
    
    return calculate_vision_tokens(width, height)

def calculate_vision_cost(
    image_width: int,
    image_height: int,
    text_tokens: int = 0,
    detail_level: str = 'high',
    model: str = 'gpt-4o'
) -> Dict[str, float]:
    """Calculate cost for a Vision request."""
    pricing = {
        'gpt-4o': {'input': 2.5, 'output': 10.0},
        'gpt-4o-mini': {'input': 0.15, 'output': 0.6},
    }
    
    model_pricing = pricing.get(model, pricing['gpt-4o'])
    
    token_estimate = calculate_vision_tokens(image_width, image_height, detail_level)
    total_tokens = token_estimate.total_tokens + text_tokens
    
    input_cost = (total_tokens / 1_000_000) * model_pricing['input']
    
    return {
        'image_cost': (token_estimate.total_tokens / 1_000_000) * model_pricing['input'],
        'text_cost': (text_tokens / 1_000_000) * model_pricing['input'],
        'total_cost': input_cost,
        'total_tokens': total_tokens,
        'detail_level': detail_level,
    }

def calculate_batch_vision_cost(
    images: List[Dict[str, Any]],
    text_tokens: int = 0,
    model: str = 'gpt-4o'
) -> Dict[str, Any]:
    """Calculate cost for multiple images."""
    pricing = {
        'gpt-4o': {'input': 2.5},
        'gpt-4o-mini': {'input': 0.15},
    }
    
    model_pricing = pricing.get(model, pricing['gpt-4o'])
    
    total_image_tokens = 0
    per_image = []
    
    for img in images:
        estimate = calculate_vision_tokens(
            img['width'],
            img['height'],
            img.get('detail_level', 'high')
        )
        per_image.append(estimate)
        total_image_tokens += estimate.total_tokens
    
    total_tokens = total_image_tokens + text_tokens
    total_cost = (total_tokens / 1_000_000) * model_pricing['input']
    
    return {
        'total_tokens': total_tokens,
        'image_tokens': total_image_tokens,
        'text_tokens': text_tokens,
        'total_cost': total_cost,
        'per_image': per_image,
    }
```

## Vision API Implementation

### Basic Usage

```typescript
// services/visionService.ts - Vision API service
import OpenAI from 'openai';
import { ImageProcessor } from '../utils/imageProcessor';
import { calculateVisionTokens, calculateVisionCost } from '../utils/visionTokenCalculator';

interface VisionRequest {
  images: Array<{
    source: string | Buffer; // URL, file path, or buffer
    detail?: 'low' | 'high' | 'auto';
  }>;
  text?: string;
  systemPrompt?: string;
}

interface VisionResponse {
  content: string;
  usage: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  cost: number;
  images: Array<{
    width: number;
    height: number;
    detail: string;
    tokens: number;
  }>;
}

export class VisionService {
  private client: OpenAI;
  private imageProcessor: ImageProcessor;
  
  constructor(client: OpenAI) {
    this.client = client;
    this.imageProcessor = new ImageProcessor();
  }
  
  async analyze(request: VisionRequest): Promise<VisionResponse> {
    const contents: any[] = [];
    const imageInfo: VisionResponse['images'] = [];
    
    // Process images
    for (const img of request.images) {
      const processed = await this.imageProcessor.processImage(
        typeof img.source === 'string' ? img.source : Buffer.from(img.source),
        { maxWidth: 2048, maxHeight: 2048 }
      );
      
      const detail = img.detail || 'high';
      
      contents.push({
        type: 'image_url',
        image_url: {
          url: `data:image/${processed.format};base64,${processed.base64}`,
          detail,
        },
      });
      
      imageInfo.push({
        width: processed.width,
        height: processed.height,
        detail,
        tokens: processed.tokenEstimate,
      });
    }
    
    // Add text content
    if (request.text) {
      contents.push({
        type: 'text',
        text: request.text,
      });
    }
    
    // Build messages
    const messages: any[] = [];
    
    if (request.systemPrompt) {
      messages.push({
        role: 'system',
        content: request.systemPrompt,
      });
    }
    
    messages.push({
      role: 'user',
      content: contents,
    });
    
    // Make request
    const response = await this.client.chat.completions.create({
      model: 'gpt-4o',
      messages,
      max_tokens: 4096,
    });
    
    // Calculate cost
    const totalImageTokens = imageInfo.reduce((sum, img) => sum + img.tokens, 0);
    const textTokens = response.usage?.prompt_tokens || 0;
    const cost = calculateVisionCost(
      imageInfo[0]?.width || 1024,
      imageInfo[0]?.height || 768,
      textTokens
    ).totalCost;
    
    return {
      content: response.choices[0].message.content || '',
      usage: {
        promptTokens: response.usage?.prompt_tokens || 0,
        completionTokens: response.usage?.completion_tokens || 0,
        totalTokens: response.usage?.total_tokens || 0,
      },
      cost,
      images: imageInfo,
    };
  }
  
  async describeImage(imageSource: string | Buffer): Promise<string> {
    const result = await this.analyze({
      images: [{ source: imageSource, detail: 'high' }],
      text: 'Mô tả chi tiết nội dung của hình ảnh này.',
    });
    
    return result.content;
  }
  
  async extractText(
    imageSource: string | Buffer,
    language: string = 'auto'
  ): Promise<string> {
    const result = await this.analyze({
      images: [{ source: imageSource, detail: 'high' }],
      text: `Trích xuất tất cả văn bản có trong hình ảnh. Giữ nguyên format và cấu trúc. Ngôn ngữ: ${language}.`,
    });
    
    return result.content;
  }
  
  async analyzeDocument(
    imageSource: string | Buffer,
    documentType: 'invoice' | 'receipt' | 'contract' | 'form' | 'id' | 'other' = 'other'
  ): Promise<{
    type: string;
    data: Record<string, any>;
    confidence: number;
    rawText: string;
  }> {
    const typePrompts = {
      invoice: 'Đây là hóa đơn. Trích xuất: tên công ty, địa chỉ, số hóa đơn, ngày, danh sách sản phẩm, tổng tiền.',
      receipt: 'Đây là biên nhận. Trích xuất: tên cửa hàng, ngày, danh sách mặt hàng, tổng số tiền.',
      contract: 'Đây là hợp đồng. Trích xuất: các bên tham gia, ngày ký, điều khoản chính.',
      form: 'Đây là form/mẫu đơn. Trích xuất: tiêu đề form, các trường và giá trị.',
      id: 'Đây là giấy tờ tùy thân. Trích xuất: họ tên, ngày sinh, số CMND/CCCD.',
      other: 'Phân tích và trích xuất thông tin từ tài liệu này.',
    };
    
    const result = await this.analyze({
      images: [{ source: imageSource, detail: 'high' }],
      text: typePrompts[documentType],
      systemPrompt: 'Bạn là chuyên gia OCR và trích xuất thông tin từ tài liệu. Trả lời bằng JSON format với các trường phù hợp.',
    });
    
    // Parse JSON from response
    const jsonMatch = result.content.match(/```json\n?([\s\S]*?)\n?```/) ||
                      result.content.match(/```\n?([\s\S]*?)\n?```/) ||
                      result.content.match(/{[\s\S]*}/);
    
    let data = {};
    if (jsonMatch) {
      try {
        data = JSON.parse(jsonMatch[1] || jsonMatch[0]);
      } catch {
        // Use raw text if JSON parsing fails
      }
    }
    
    return {
      type: documentType,
      data,
      confidence: 0.85, // Simplified
      rawText: result.content,
    };
  }
}
```

```python
# services/vision_service.py - Vision API service
from openai import OpenAI
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from utils.image_processor import ImageProcessor
from utils.vision_token_calculator import calculate_vision_cost

@dataclass
class VisionResponse:
    content: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float
    images: List[Dict[str, Any]]

class VisionService:
    """Service for Vision API operations."""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.image_processor = ImageProcessor()
    
    async def analyze(
        self,
        images: List[Dict[str, Any]],
        text: Optional[str] = None,
        system_prompt: Optional[str] = None,
        model: str = 'gpt-4o'
    ) -> VisionResponse:
        """Analyze images with optional text prompt."""
        contents = []
        image_info = []
        
        # Process images
        for img in images:
            source = img['source']
            detail = img.get('detail', 'high')
            
            processed = self.image_processor.process_image(
                source,
                detail=detail
            )
            
            contents.append({
                'type': 'image_url',
                'image_url': {
                    'url': f'data:image/{processed.format};base64,{processed.base64}',
                    'detail': detail,
                }
            })
            
            image_info.append({
                'width': processed.width,
                'height': processed.height,
                'detail': detail,
                'tokens': processed.token_estimate,
            })
        
        # Add text content
        if text:
            contents.append({
                'type': 'text',
                'text': text
            })
        
        # Build messages
        messages = []
        
        if system_prompt:
            messages.append({
                'role': 'system',
                'content': system_prompt
            })
        
        messages.append({
            'role': 'user',
            'content': contents
        })
        
        # Make request
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=4096
        )
        
        # Calculate cost
        total_image_tokens = sum(img['tokens'] for img in image_info)
        text_tokens = response.usage.prompt_tokens if response.usage else 0
        
        cost_info = calculate_vision_cost(
            image_info[0]['width'] if image_info else 1024,
            image_info[0]['height'] if image_info else 768,
            text_tokens
        )
        
        return VisionResponse(
            content=response.choices[0].message.content or '',
            prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
            completion_tokens=response.usage.completion_tokens if response.usage else 0,
            total_tokens=response.usage.total_tokens if response.usage else 0,
            cost=cost_info['total_cost'],
            images=image_info
        )
    
    async def describe_image(
        self,
        image_source: Any,
        language: str = 'vi'
    ) -> str:
        """Get detailed description of an image."""
        prompt = 'Mô tả chi tiết nội dung của hình ảnh này.'
        
        result = await self.analyze(
            images=[{'source': image_source, 'detail': 'high'}],
            text=prompt
        )
        
        return result.content
    
    async def extract_text(
        self,
        image_source: Any,
        language: str = 'auto'
    ) -> str:
        """Extract text from an image (OCR)."""
        prompt = f"""Trích xuất tất cả văn bản có trong hình ảnh. 
Giữ nguyên format và cấu trúc.
Ngôn ngữ: {language}."""
        
        result = await self.analyze(
            images=[{'source': image_source, 'detail': 'high'}],
            text=prompt
        )
        
        return result.content
    
    async def analyze_document(
        self,
        image_source: Any,
        document_type: str = 'other'
    ) -> Dict[str, Any]:
        """Analyze and extract data from documents."""
        type_prompts = {
            'invoice': 'Đây là hóa đơn. Trích xuất: tên công ty, địa chỉ, số hóa đơn, ngày, danh sách sản phẩm, tổng tiền.',
            'receipt': 'Đây là biên nhận. Trích xuất: tên cửa hàng, ngày, danh sách mặt hàng, tổng số tiền.',
            'contract': 'Đây là hợp đồng. Trích xuất: các bên tham gia, ngày ký, điều khoản chính.',
            'form': 'Đây là form/mẫu đơn. Trích xuất: tiêu đề form, các trường và giá trị.',
            'id': 'Đây là giấy tờ tùy thân. Trích xuất: họ tên, ngày sinh, số CMND/CCCD.',
            'other': 'Phân tích và trích xuất thông tin từ tài liệu này.',
        }
        
        system_prompt = 'Bạn là chuyên gia OCR và trích xuất thông tin từ tài liệu. Trả lời bằng JSON format.'
        
        result = await self.analyze(
            images=[{'source': image_source, 'detail': 'high'}],
            text=type_prompts.get(document_type, type_prompts['other']),
            system_prompt=system_prompt
        )
        
        # Parse JSON from response
        import json
        import re
        
        json_match = re.search(r'```json\n?(.*?)\n?```', result.content, re.DOTALL) or \
                     re.search(r'```\n?(.*?)\n?```', result.content, re.DOTALL) or \
                     re.search(r'({.*})', result.content, re.DOTALL)
        
        data = {}
        if json_match:
            try:
                data = json.loads(json_match.group(1) or json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        return {
            'type': document_type,
            'data': data,
            'confidence': 0.85,  # Simplified
            'raw_text': result.content,
        }
```

## Common Use Cases

### Document Processing

```typescript
// useCases/documentProcessor.ts - Document processing use cases
import { VisionService } from '../services/visionService';

interface InvoiceData {
  vendorName?: string;
  vendorAddress?: string;
  invoiceNumber?: string;
  invoiceDate?: string;
  lineItems?: Array<{
    description: string;
    quantity: number;
    unitPrice: number;
    total: number;
  }>;
  subtotal?: number;
  tax?: number;
  total?: number;
  currency?: string;
}

interface ReceiptData {
  merchantName?: string;
  merchantAddress?: string;
  date?: string;
  time?: string;
  items?: Array<{
    name: string;
    price: number;
  }>;
  subtotal?: number;
  tax?: number;
  tip?: number;
  total?: number;
}

export class DocumentProcessor {
  private visionService: VisionService;
  
  constructor(visionService: VisionService) {
    this.visionService = visionService;
  }
  
  async processInvoice(imageSource: string | Buffer): Promise<InvoiceData> {
    const result = await this.visionService.analyzeDocument(
      imageSource,
      'invoice'
    );
    
    return result.data as InvoiceData;
  }
  
  async processReceipt(imageSource: string | Buffer): Promise<ReceiptData> {
    const result = await this.visionService.analyzeDocument(
      imageSource,
      'receipt'
    );
    
    return result.data as ReceiptData;
  }
  
  async extractBusinessCard(imageSource: string | Buffer): Promise<{
    name?: string;
    title?: string;
    company?: string;
    phone?: string;
    email?: string;
    address?: string;
    website?: string;
  }> {
    const result = await this.visionService.analyze({
      images: [{ source: imageSource, detail: 'high' }],
      text: `Trích xuất thông tin từ danh thiếp:
- Họ tên
- Chức danh
- Công ty
- Số điện thoại
- Email
- Địa chỉ
- Website

Trả lời bằng JSON.`,
    });
    
    // Parse JSON response
    try {
      const jsonMatch = result.content.match(/{[\s\S]*}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
    } catch {
      // Fall through to return empty
    }
    
    return {};
  }
  
  async compareDocuments(
    image1: string | Buffer,
    image2: string | Buffer
  ): Promise<{
    differences: string[];
    similarity: number;
  }> {
    const result = await this.visionService.analyze({
      images: [
        { source: image1, detail: 'high' },
        { source: image2, detail: 'high' },
      ],
      text: `So sánh hai tài liệu này và liệt kê:
1. Các điểm giống nhau
2. Các điểm khác nhau
3. Đánh giá mức độ tương đồng (0-100%)

Trả lời bằng JSON format.`,
    });
    
    try {
      const jsonMatch = result.content.match(/{[\s\S]*}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
    } catch {
      // Fall through
    }
    
    return { differences: [], similarity: 0 };
  }
}
```

```python
# use_cases/document_processor.py - Document processing use cases
from typing import Dict, Any, List, Optional
from services.vision_service import VisionService
from dataclasses import dataclass

@dataclass
class InvoiceData:
    vendor_name: Optional[str] = None
    vendor_address: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    line_items: Optional[List[Dict[str, Any]]] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    currency: Optional[str] = None

@dataclass
class ReceiptData:
    merchant_name: Optional[str] = None
    merchant_address: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    items: Optional[List[Dict[str, Any]]] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    tip: Optional[float] = None
    total: Optional[float] = None

class DocumentProcessor:
    """Process various document types using Vision API."""
    
    def __init__(self, vision_service: VisionService):
        self.vision_service = vision_service
    
    async def process_invoice(self, image_source) -> InvoiceData:
        """Process an invoice image."""
        result = await self.vision_service.analyze_document(
            image_source,
            'invoice'
        )
        return InvoiceData(**result['data'])
    
    async def process_receipt(self, image_source) -> ReceiptData:
        """Process a receipt image."""
        result = await self.vision_service.analyze_document(
            image_source,
            'receipt'
        )
        return ReceiptData(**result['data'])
    
    async def extract_business_card(self, image_source) -> Dict[str, Any]:
        """Extract information from a business card."""
        result = await self.vision_service.analyze(
            images=[{'source': image_source, 'detail': 'high'}],
            text="""Trích xuất thông tin từ danh thiếp:
- Họ tên
- Chức danh
- Công ty
- Số điện thoại
- Email
- Địa chỉ
- Website

Trả lời bằng JSON format."""
        )
        
        import json
        import re
        
        json_match = re.search(r'({.*})', result.content, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        return {}
    
    async def compare_documents(
        self,
        image1,
        image2
    ) -> Dict[str, Any]:
        """Compare two documents."""
        result = await self.vision_service.analyze(
            images=[
                {'source': image1, 'detail': 'high'},
                {'source': image2, 'detail': 'high'}
            ],
            text="""So sánh hai tài liệu này và liệt kê:
1. Các điểm giống nhau
2. Các điểm khác nhau
3. Đánh giá mức độ tương đồng (0-100%)

Trả lời bằng JSON format."""
        )
        
        import json
        import re
        
        json_match = re.search(r'({.*})', result.content, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        return {'differences': [], 'similarity': 0}
```

### Visual Content Analysis

```typescript
// useCases/visualAnalysis.ts - Visual content analysis use cases
import { VisionService } from '../services/visionService';

interface SceneAnalysis {
  description: string;
  objects: string[];
  people?: number;
  setting?: string;
  activities?: string[];
  sentiment?: string;
  quality?: 'excellent' | 'good' | 'fair' | 'poor';
}

interface ChartAnalysis {
  type: 'bar' | 'line' | 'pie' | 'scatter' | 'other';
  title?: string;
  dataPoints: Array<{
    label: string;
    value: number;
  }>;
  insights: string[];
  summary: string;
}

interface UIAnalysis {
  components: Array<{
    type: string;
    text?: string;
    position: { x: number; y: number; width: number; height: number };
  }>;
  accessibility: {
    contrastIssues: string[];
    missingAlt: string[];
  };
  recommendations: string[];
}

export class VisualAnalyzer {
  private visionService: VisionService;
  
  constructor(visionService: VisionService) {
    this.visionService = visionService;
  }
  
  async analyzeScene(imageSource: string | Buffer): Promise<SceneAnalysis> {
    const result = await this.visionService.analyze({
      images: [{ source: imageSource, detail: 'high' }],
      text: `Phân tích hình ảnh và trả lời:
1. Mô tả tổng quan cảnh
2. Liệt kê các đối tượng chính
3. Ước tính số người (nếu có)
4. Mô tả setting/bối cảnh
5. Xác định hoạt động đang diễn ra
6. Đánh giá sentiment/tâm trạng
7. Đánh giá chất lượng ảnh

Trả lời bằng JSON.`,
    });
    
    return this.parseJSONResponse(result.content);
  }
  
  async analyzeChart(imageSource: string | Buffer): Promise<ChartAnalysis> {
    const result = await this.visionService.analyze({
      images: [{ source: imageSource, detail: 'high' }],
      text: `Phân tích biểu đồ và trả lời:
1. Loại biểu đồ (bar, line, pie, scatter, other)
2. Tiêu đề biểu đồ (nếu có)
3. Trích xuất tất cả data points (label và value)
4. Đưa ra insights từ dữ liệu
5. Tóm tắt ý nghĩa của biểu đồ

Trả lời bằng JSON format với các trường: type, title, dataPoints (array), insights (array), summary.`,
    });
    
    return this.parseJSONResponse(result.content);
  }
  
  async analyzeUI(imageSource: string | Buffer): Promise<UIAnalysis> {
    const result = await this.visionService.analyze({
      images: [{ source: imageSource, detail: 'high' }],
      text: `Phân tích giao diện người dùng và trả lời:
1. Liệt kê các thành phần UI chính (buttons, inputs, text, etc.)
2. Xác định vấn đề accessibility (contrast, missing alt text)
3. Đề xuất cải thiện

Trả lời bằng JSON format.`,
    });
    
    return this.parseJSONResponse(result.content);
  }
  
  async findSimilarImages(
    queryImage: string | Buffer,
    referenceImages: string[] | Buffer[]
  ): Promise<Array<{ index: number; similarity: number }>> {
    // Get description of query image
    const queryDescription = await this.describeImage(queryImage);
    
    const similarities: Array<{ index: number; similarity: number }> = [];
    
    for (let i = 0; i < referenceImages.length; i++) {
      const refDescription = await this.describeImage(referenceImages[i]);
      
      // Compare descriptions (simplified - use embeddings in production)
      const similarity = this.calculateTextSimilarity(
        queryDescription,
        refDescription
      );
      
      similarities.push({ index: i, similarity });
    }
    
    return similarities.sort((a, b) => b.similarity - a.similarity);
  }
  
  private async describeImage(imageSource: string | Buffer): Promise<string> {
    const result = await this.visionService.describeImage(imageSource);
    return result;
  }
  
  private parseJSONResponse<T>(content: string): T {
    try {
      const jsonMatch = content.match(/{[\s\S]*}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
    } catch {
      // Fall through
    }
    return {} as T;
  }
  
  private calculateTextSimilarity(text1: string, text2: string): number {
    // Simplified similarity - use embeddings in production
    const words1 = new Set(text1.toLowerCase().split(/\s+/));
    const words2 = new Set(text2.toLowerCase().split(/\s+/));
    
    const intersection = new Set([...words1].filter(x => words2.has(x)));
    const union = new Set([...words1, ...words2]);
    
    return intersection.size / union.size;
  }
}
```

```python
# use_cases/visual_analysis.py - Visual content analysis use cases
from typing import Dict, Any, List, Optional
from services.vision_service import VisionService
from dataclasses import dataclass

@dataclass
class SceneAnalysis:
    description: str
    objects: List[str]
    people: Optional[int] = None
    setting: Optional[str] = None
    activities: Optional[List[str]] = None
    sentiment: Optional[str] = None
    quality: Optional[str] = None

@dataclass
class ChartAnalysis:
    chart_type: str
    title: Optional[str]
    data_points: List[Dict[str, Any]]
    insights: List[str]
    summary: str

class VisualAnalyzer:
    """Analyze visual content using Vision API."""
    
    def __init__(self, vision_service: VisionService):
        self.vision_service = vision_service
    
    async def analyze_scene(self, image_source) -> SceneAnalysis:
        """Analyze a scene/photo."""
        result = await self.vision_service.analyze(
            images=[{'source': image_source, 'detail': 'high'}],
            text="""Phân tích hình ảnh và trả lời:
1. Mô tả tổng quan cảnh
2. Liệt kê các đối tượng chính
3. Ước tính số người (nếu có)
4. Mô tả setting/bối cảnh
5. Xác định hoạt động đang diễn ra
6. Đánh giá sentiment/tâm trạng
7. Đánh giá chất lượng ảnh

Trả lời bằng JSON."""
        )
        
        import json
        import re
        
        json_match = re.search(r'({.*})', result.content, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                return SceneAnalysis(**data)
            except (json.JSONDecodeError, TypeError):
                pass
        
        return SceneAnalysis(description=result.content, objects=[])
    
    async def analyze_chart(self, image_source) -> ChartAnalysis:
        """Analyze a chart/graph."""
        result = await self.vision_service.analyze(
            images=[{'source': image_source, 'detail': 'high'}],
            text="""Phân tích biểu đồ và trả lời:
1. Loại biểu đồ (bar, line, pie, scatter, other)
2. Tiêu đề biểu đồ (nếu có)
3. Trích xuất tất cả data points (label và value)
4. Đưa ra insights từ dữ liệu
5. Tóm tắt ý nghĩa của biểu đồ

Trả lời bằng JSON format với các trường: type, title, dataPoints (array), insights (array), summary."""
        )
        
        import json
        import re
        
        json_match = re.search(r'({.*})', result.content, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                return ChartAnalysis(
                    chart_type=data.get('type', 'other'),
                    title=data.get('title'),
                    data_points=data.get('dataPoints', []),
                    insights=data.get('insights', []),
                    summary=data.get('summary', '')
                )
            except (json.JSONDecodeError, TypeError):
                pass
        
        return ChartAnalysis(
            chart_type='unknown',
            title=None,
            data_points=[],
            insights=[],
            summary=result.content
        )
    
    async def find_similar_images(
        self,
        query_image,
        reference_images: List
    ) -> List[Dict[str, Any]]:
        """Find similar images based on descriptions."""
        query_description = await self.vision_service.describe_image(query_image)
        
        similarities = []
        
        for i, ref_image in enumerate(reference_images):
            ref_description = await self.vision_service.describe_image(ref_image)
            similarity = self._calculate_text_similarity(
                query_description,
                ref_description
            )
            similarities.append({'index': i, 'similarity': similarity})
        
        return sorted(similarities, key=lambda x: x['similarity'], reverse=True)
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity using Jaccard."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0.0
```

## Best Practices

### Optimization Guidelines

```typescript
// bestPractices/visionOptimization.ts - Vision API optimization

interface OptimizationResult {
  recommendedSize: { width: number; height: number };
  estimatedTokens: number;
  estimatedCost: number;
  quality: 'high' | 'medium' | 'low';
}

// Image size optimization
export function optimizeImageSize(
  originalWidth: number,
  originalHeight: number,
  targetTokens: number = 1000
): OptimizationResult {
  // GPT-4o: ~170 tokens per 512x512 patch
  // Target ~1000 tokens = ~6 patches
  
  const patchesX = Math.ceil(originalWidth / 512);
  const patchesY = Math.ceil(originalHeight / 512);
  const totalPatches = patchesX * patchesY;
  
  const currentTokens = 85 + (totalPatches * 170);
  
  // If over target, scale down
  if (currentTokens > targetTokens) {
    const scaleFactor = Math.sqrt(targetTokens / currentTokens);
    return {
      recommendedSize: {
        width: Math.floor(originalWidth * scaleFactor / 2) * 2,
        height: Math.floor(originalHeight * scaleFactor / 2) * 2,
      },
      estimatedTokens: targetTokens,
      estimatedCost: (targetTokens / 1_000_000) * 2.5,
      quality: targetTokens < 500 ? 'low' : 'medium',
    };
  }
  
  return {
    recommendedSize: { width: originalWidth, height: originalHeight },
    estimatedTokens: currentTokens,
    estimatedCost: (currentTokens / 1_000_000) * 2.5,
    quality: 'high',
  };
}

// Batch processing for multiple images
export async function* batchProcessImages(
  imageSources: Array<string | Buffer>,
  batchSize: number = 5,
  visionService: VisionService
): AsyncGenerator<Array<VisionResponse>, void, unknown> {
  for (let i = 0; i < imageSources.length; i += batchSize) {
    const batch = imageSources.slice(i, i + batchSize);
    
    const results = await Promise.all(
      batch.map(img => visionService.describeImage(img))
    );
    
    yield results;
  }
}

// Caching strategy
export class VisionCache {
  private cache: Map<string, string>; // hash -> description
  private redis?: any;
  
  constructor(redis?: any) {
    this.cache = new Map();
    this.redis = redis;
  }
  
  private async getHash(source: string | Buffer): Promise<string> {
    // Simple hash - use proper hash in production
    const data = typeof source === 'string' ? source : source.toString('base64');
    return data.substring(0, 64); // Simplified
  }
  
  async get(source: string | Buffer): Promise<string | null> {
    const hash = await this.getHash(source);
    
    // Check memory cache
    if (this.cache.has(hash)) {
      return this.cache.get(hash)!;
    }
    
    // Check Redis if available
    if (this.redis) {
      const cached = await this.redis.get(`vision:${hash}`);
      if (cached) {
        this.cache.set(hash, cached);
        return cached;
      }
    }
    
    return null;
  }
  
  async set(source: string | Buffer, description: string): Promise<void> {
    const hash = await this.getHash(source);
    
    this.cache.set(hash, description);
    
    if (this.redis) {
      await this.redis.setex(`vision:${hash}`, 86400, description); // 24h TTL
    }
  }
}
```

```python
# best_practices/vision_optimization.py - Vision API optimization
from typing import Dict, Any, List, Optional, AsyncGenerator
import hashlib
import asyncio

def optimize_image_size(
    original_width: int,
    original_height: int,
    target_tokens: int = 1000
) -> Dict[str, Any]:
    """
    Optimize image dimensions for target token count.
    GPT-4o: ~170 tokens per 512x512 patch
    """
    # Calculate current patches
    patches_x = (original_width + 511) // 512
    patches_y = (original_height + 511) // 512
    total_patches = patches_x * patches_y
    
    current_tokens = 85 + (total_patches * 170)
    
    # Scale down if over target
    if current_tokens > target_tokens:
        import math
        scale_factor = math.sqrt(target_tokens / current_tokens)
        
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        
        # Ensure even dimensions
        new_width = (new_width // 2) * 2
        new_height = (new_height // 2) * 2
        
        quality = 'low' if target_tokens < 500 else 'medium'
        
        return {
            'recommended_size': {'width': new_width, 'height': new_height},
            'estimated_tokens': target_tokens,
            'estimated_cost': (target_tokens / 1_000_000) * 2.5,
            'quality': quality,
        }
    
    return {
        'recommended_size': {'width': original_width, 'height': original_height},
        'estimated_tokens': current_tokens,
        'estimated_cost': (current_tokens / 1_000_000) * 2.5,
        'quality': 'high',
    }

async def batch_process_images(
    image_sources: List,
    batch_size: int = 5,
    vision_service=None
) -> AsyncGenerator[List, None, None]:
    """Process images in batches."""
    for i in range(0, len(image_sources), batch_size):
        batch = image_sources[i:i + batch_size]
        
        tasks = [
            vision_service.describe_image(img)
            for img in batch
        ]
        
        results = await asyncio.gather(*tasks)
        yield results

class VisionCache:
    """Cache for Vision API results."""
    
    def __init__(self, redis_client=None):
        self.cache: Dict[str, str] = {}
        self.redis = redis_client
    
    def _get_hash(self, source) -> str:
        """Generate hash for image."""
        if isinstance(source, str):
            data = source.encode()
        else:
            import base64
            data = base64.b64encode(source)
        
        return hashlib.sha256(data).hexdigest()[:64]
    
    async def get(self, source) -> Optional[str]:
        """Get cached description."""
        hash_key = self._get_hash(source)
        
        # Check memory cache
        if hash_key in self.cache:
            return self.cache[hash_key]
        
        # Check Redis if available
        if self.redis:
            cached = await self.redis.get(f'vision:{hash_key}')
            if cached:
                self.cache[hash_key] = cached
                return cached
        
        return None
    
    async def set(self, source, description: str) -> None:
        """Cache description."""
        hash_key = self._get_hash(source)
        
        self.cache[hash_key] = description
        
        if self.redis:
            await self.redis.setex(f'vision:{hash_key}', 86400, description)
```

## Troubleshooting

### Common Vision Issues

```typescript
// troubleshooting/visionIssues.ts - Vision API troubleshooting
const visionIssueGuides = [
  {
    issue: 'Image Not Loading',
    symptoms: [
      'Request fails with image loading error',
      'Invalid image format error',
      'Empty or blank response',
    ],
    causes: [
      'Corrupted image file',
      'Unsupported format',
      'URL not accessible',
      'Base64 encoding error',
    ],
    solutions: [
      'Verify image file integrity',
      'Convert to supported format (JPEG, PNG, WebP)',
      'Check URL accessibility',
      'Validate base64 encoding',
      'Use image processing library to validate',
    ],
  },
  {
    issue: 'Poor Text Recognition',
    symptoms: [
      'Missing or incorrect text extraction',
      'Blurry text in results',
      'Wrong character recognition',
    ],
    causes: [
      'Image resolution too low',
      'Text too small in original image',
      'Using "low" detail setting',
      'Poor image quality',
    ],
    solutions: [
      'Use "high" detail setting',
      'Pre-process image to enhance quality',
      'Zoom in on text regions if possible',
      'Increase image dimensions',
      'Use image sharpening filters',
    ],
  },
  {
    issue: 'High Costs',
    symptoms: [
      'Token usage much higher than expected',
      'Large images causing high bills',
      'Multiple images per request adding up',
    ],
    causes: [
      'Sending high-resolution images unnecessarily',
      'Too many images in single request',
      'Using high detail when not needed',
    ],
    solutions: [
      'Resize images to optimal dimensions',
      'Use "low" detail for simple tasks',
      'Batch similar requests together',
      'Implement caching for repeated images',
      'Monitor token usage per request',
    ],
  },
  {
    issue: 'Slow Processing',
    symptoms: [
      'Long response times',
      'Timeout errors',
      'Intermittent slow responses',
    ],
    causes: [
      'Very large images',
      'High detail processing',
      'Network latency',
      'Rate limiting',
    ],
    solutions: [
      'Resize images before sending',
      'Use "low" detail for faster processing',
      'Pre-upload images to CDN',
      'Implement async processing',
      'Add retry logic with backoff',
    ],
  },
  {
    issue: 'Inconsistent Results',
    symptoms: [
      'Different descriptions for same image',
      'Variable quality of analysis',
      'Sometimes misses obvious elements',
    ],
    causes: [
      'Temperature too high',
      'Prompt not specific enough',
      'Image quality variations',
    ],
    solutions: [
      'Use lower temperature (0.1-0.3)',
      'Add specific analysis instructions',
      'Pre-process images for consistency',
      'Include examples in prompt',
    ],
  },
];
```

## References

### Official Documentation

- [Vision Guide](https://platform.openai.com/docs/guides/vision)
- [Vision API](https://platform.openai.com/docs/api-reference/chat/chat-completions)
- [Image Inputs](https://platform.openai.com/docs/guides/vision/uploading-images)

### Image Processing Libraries

- [Sharp](https://sharp.pixel.s.org/) - Node.js image processing
- [Pillow](https://pillow.readthedocs.io/) - Python image processing
- [Libvips](https://www.libvips.org/) - Fast image processing

### Additional Resources

- [Vision Tutorials](https://platform.openai.com/docs/guides/vision)
- [GPT-4o Capabilities](https://openai.com/index/gpt-4o)
- [Image Optimization Guide](https://platform.openai.com/docs/guides/vision/low-or-high-detail-image)

---

**Tài liệu này là một phần của Cursor Enterprise Framework Generator.**
