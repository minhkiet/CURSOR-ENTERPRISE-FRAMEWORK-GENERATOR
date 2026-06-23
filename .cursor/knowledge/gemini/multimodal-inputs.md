---
title: "Multimodal Inputs - Xử Lý Hình Ảnh, Video, Audio và PDF"
description: "Hướng dẫn toàn diện về xử lý multimodal inputs với Gemini API, bao gồm image inputs, video processing, audio processing, PDF analysis và cách tính token cho các loại dữ liệu đa phương thức"
tags:
  - "gemini"
  - "multimodal"
  - "image-processing"
  - "video-processing"
  - "audio-processing"
  - "pdf-analysis"
  - "token-calculation"
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Multimodal Inputs - Xử Lý Hình Ảnh, Video, Audio và PDF

## Tổng Quan (Overview)

Khả năng xử lý đa phương thức (multimodal) là một trong những tính năng mạnh mẽ nhất của Gemini API. Khác với các mô hình ngôn ngữ truyền thống chỉ xử lý text, Gemini có thể hiểu và phân tích nhiều loại dữ liệu khác nhau như hình ảnh, video, audio, và PDF trong cùng một yêu cầu.

Việc tích hợp multimodal inputs vào ứng dụng enterprise mở ra rất nhiều khả năng: từ việc phân tích tài liệu tự động, nhận diện nội dung video, đến việc xây dựng các hệ thống AI có khả năng "nhìn" và hiểu nội dung đa phương tiện. Tuy nhiên, để sử dụng hiệu quả, developers cần hiểu rõ về cách Gemini xử lý từng loại dữ liệu, cách tính token, và các best practices để tối ưu chi phí và hiệu suất.

Trong tài liệu này, chúng ta sẽ đi sâu vào chi tiết kỹ thuật của từng loại multimodal input, từ những concepts cơ bản đến các patterns nâng cao cho production deployment.

## Mục Đích (Purpose)

**1. Hiểu Rõ Các Loại Multimodal Inputs**

Cung cấp kiến thức chuyên sâu về cách Gemini xử lý từng loại dữ liệu: hình ảnh (images), video, audio, và PDF. Mỗi loại dữ liệu có những đặc điểm riêng về format, kích thước, và cách xử lý mà developers cần nắm vững.

**2. Nắm Vững Kỹ Thuật Token Calculation**

Token calculation là yếu tố quan trọng để ước tính chi phí và quản lý context window. Gemini sử dụng các công thức khác nhau để tính token cho text, images, video, và audio - hiểu rõ các công thức này giúp tối ưu hóa chi phí và tránh các lỗi liên quan đến context window.

**3. Xây Dựng Các Ứng Dụng Production-Grade**

Cung cấp các code patterns và best practices thực tế để xây dựng các ứng dụng xử lý multimodal ổn định, có khả năng mở rộng, và dễ bảo trì trong môi trường enterprise.

## Các Khái Niệm Cốt Lõi (Key Concepts)

### 1. Cấu Trúc Dữ Liệu Part Trong Gemini

Trong Gemini API, tất cả dữ liệu input đều được biểu diễn dưới dạng "Parts" - đây là đơn vị cơ bản của dữ liệu có thể là text, image, video, audio, hoặc file. Hiểu cách tạo và quản lý Parts là nền tảng cho việc làm việc với multimodal inputs.

```python
from google.generativeai import types

# Text Part - đơn giản nhất
text_part = types.Part(text="Hello, how can I help you?")

# Image Part - từ base64 encoded image
image_part = types.Part(
    inline_data=types.Blob(
        mime_type="image/png",  # Hoặc "image/jpeg", "image/webp", "image/gif"
        data=image_bytes  # bytes object
    )
)

# Image Part - từ URL (Image URLs không được hỗ trợ trực tiếp,
# cần download về trước)
with open("image.png", "rb") as f:
    image_data = f.read()

image_part = types.Part(
    inline_data=types.Blob(
        mime_type="image/png",
        data=image_data
    )
)

# Video Part - từ file bytes
video_part = types.Part(
    inline_data=types.Blob(
        mime_type="video/mp4",  # Hỗ trợ: video/mp4, video/mpeg, video/webm
        data=video_bytes
    )
)

# Audio Part - từ file bytes
audio_part = types.Part(
    inline_data=types.Blob(
        mime_type="audio/wav",  # Hỗ trợ: audio/wav, audio/mp3, audio/mpeg, audio/webm
        data=audio_bytes
    )
)

# PDF Part - Gemini xử lý PDF như images
pdf_part = types.Part(
    inline_data=types.Blob(
        mime_type="application/pdf",
        data=pdf_bytes
    )
)
```

```typescript
// TypeScript/Node.js
import { HarmCategory, HarmBlockThreshold, Part } from '@google/generative-ai';

// Text Part
const textPart: Part = {
  text: 'Hello, how can I help you?',
};

// Image Part
const imagePart: Part = {
  inlineData: {
    mimeType: 'image/png',
    data: imageBase64, // base64 encoded string
  },
};

// Video Part
const videoPart: Part = {
  inlineData: {
    mimeType: 'video/mp4',
    data: videoBase64,
  },
};

// Audio Part
const audioPart: Part = {
  inlineData: {
    mimeType: 'audio/wav',
    data: audioBase64,
  },
};
```

### 2. Image Inputs - Xử Lý Hình Ảnh

Gemini hỗ trợ nhiều định dạng hình ảnh phổ biến: PNG, JPEG, WEBP, GIF, và HEIC. Khi làm việc với images, có một số điểm quan trọng cần lưu ý:

**Đặc điểm của Image Input:**

- **Kích thước tối đa**: 20MB cho mỗi ảnh
- **Định dạng được hỗ trợ**: PNG, JPEG, WEBP, GIF, HEIC
- **Độ phân giải**: Gemini tự động downscale ảnh lớn để tối ưu token
- **Animation**: GIF được xử lý như một chuỗi frames, không phải single frame

**Chiến lược xử lý ảnh cho production:**

```python
# src/multimodal/image_processor.py
"""
Image processor cho Gemini API
Xử lý ảnh trước khi gửi lên Gemini để tối ưu quality và cost
"""

import io
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple, Union, List
from PIL import Image
import base64
import logging

logger = logging.getLogger(__name__)


class ImageFormat(Enum):
    """Các định dạng ảnh được hỗ trợ."""
    PNG = "image/png"
    JPEG = "image/jpeg"
    WEBP = "image/webp"
    GIF = "image/gif"
    HEIC = "image/heic"


@dataclass
class ImageProcessingOptions:
    """Tùy chọn xử lý ảnh."""
    max_width: int = 2048
    max_height: int = 2048
    quality: int = 95  # Chất lượng nén (1-100)
    format: ImageFormat = ImageFormat.WEBP  # Format đầu ra
    preserve_aspect_ratio: bool = True
    strip_metadata: bool = True  # Loại bỏ metadata để giảm kích thước


class ImageProcessor:
    """
    Processor để chuẩn bị ảnh cho Gemini API.
    Thực hiện các bước: resize, compress, convert format.
    """
    
    SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".heic"}
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
    
    def __init__(self, options: Optional[ImageProcessingOptions] = None):
        self.options = options or ImageProcessingOptions()
    
    def load_image(self, source: Union[str, bytes, io.BytesIO]) -> Image.Image:
        """
        Load ảnh từ nhiều nguồn khác nhau.
        
        Args:
            source: Đường dẫn file, bytes, hoặc BytesIO object
            
        Returns:
            PIL Image object
        """
        if isinstance(source, str):
            with open(source, "rb") as f:
                return Image.open(f)
        elif isinstance(source, bytes):
            return Image.open(io.BytesIO(source))
        elif isinstance(source, io.BytesIO):
            return Image.open(source)
        else:
            raise ValueError(f"Unsupported image source type: {type(source)}")
    
    def resize_if_needed(
        self,
        image: Image.Image,
        max_width: int,
        max_height: int,
        preserve_aspect: bool
    ) -> Image.Image:
        """
        Resize ảnh nếu vượt quá kích thước tối đa.
        
        Args:
            image: PIL Image object
            max_width: Chiều rộng tối đa
            max_height: Chiều cao tối đa
            preserve_aspect: Có giữ tỷ lệ khung hình không
            
        Returns:
            Resized Image object
        """
        width, height = image.size
        
        if width <= max_width and height <= max_height:
            return image
        
        if preserve_aspect:
            # Tính toán tỷ lệ scale
            width_ratio = max_width / width
            height_ratio = max_height / height
            scale_ratio = min(width_ratio, height_ratio)
            
            new_width = int(width * scale_ratio)
            new_height = int(height * scale_ratio)
        else:
            new_width = max_width
            new_height = max_height
        
        logger.info(f"Resizing image from {width}x{height} to {new_width}x{new_height}")
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def convert_format(self, image: Image.Image, target_format: ImageFormat) -> bytes:
        """
        Convert ảnh sang format khác và trả về bytes.
        
        Args:
            image: PIL Image object
            target_format: Format đích
            
        Returns:
            Image bytes
        """
        output = io.BytesIO()
        
        # Xử lý GIF - giữ nguyên nếu đầu ra cũng là GIF
        if image.mode == 'P' and target_format == ImageFormat.GIF:
            image.save(output, format='GIF')
        else:
            # Convert sang RGB nếu cần (PIL không hỗ trợ RGBA cho một số format)
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')
            
            save_format = target_format.name.lower()
            image.save(
                output,
                format=save_format.upper(),
                quality=self.options.quality,
                optimize=True
            )
        
        return output.getvalue()
    
    def process_image(
        self,
        source: Union[str, bytes, io.BytesIO],
        options: Optional[ImageProcessingOptions] = None
    ) -> Tuple[bytes, str]:
        """
        Process ảnh hoàn chỉnh: resize, convert, compress.
        
        Args:
            source: Ảnh nguồn
            options: Tùy chọn xử lý (override constructor options)
            
        Returns:
            Tuple của (processed_image_bytes, mime_type)
        """
        options = options or self.options
        
        # Load ảnh
        image = self.load_image(source)
        logger.debug(f"Loaded image: {image.size}, mode={image.mode}, format={image.format}")
        
        # Resize nếu cần
        image = self.resize_if_needed(
            image,
            options.max_width,
            options.max_height,
            options.preserve_aspect_ratio
        )
        
        # Convert format
        processed_bytes = self.convert_format(image, options.format)
        
        # Check kích thước
        if len(processed_bytes) > self.MAX_FILE_SIZE:
            logger.warning(
                f"Processed image ({len(processed_bytes)} bytes) exceeds 20MB limit. "
                "Consider reducing quality or size."
            )
        
        return processed_bytes, options.format.value
    
    def create_gemini_part(
        self,
        source: Union[str, bytes, io.BytesIO],
        options: Optional[ImageProcessingOptions] = None
    ) -> "types.Part":
        """
        Tạo Gemini Part từ ảnh đã process.
        
        Args:
            source: Ảnh nguồn
            options: Tùy chọn xử lý
            
        Returns:
            Gemini Part object
        """
        from google.generativeai import types
        
        processed_bytes, mime_type = self.process_image(source, options)
        
        return types.Part(
            inline_data=types.Blob(
                mime_type=mime_type,
                data=processed_bytes
            )
        )


# Utility functions
def image_to_base64(image: Union[Image.Image, bytes]) -> str:
    """Convert image sang base64 string."""
    if isinstance(image, Image.Image):
        output = io.BytesIO()
        image.save(output, format='PNG')
        image = output.getvalue()
    
    return base64.b64encode(image).decode('utf-8')


def base64_to_image(base64_string: str) -> Image.Image:
    """Convert base64 string sang PIL Image."""
    image_bytes = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(image_bytes))
```

```typescript
// src/multimodal/image-processor.ts
/**
 * Image processor cho Gemini API (TypeScript)
 */

import { Part } from '@google/generative-ai';
import sharp from 'sharp'; // Thư viện xử lý ảnh

export interface ImageProcessingOptions {
  maxWidth: number;
  maxHeight: number;
  quality: number;
  format: 'png' | 'jpeg' | 'webp';
  preserveAspectRatio: boolean;
}

export class ImageProcessor {
  private options: ImageProcessingOptions;
  
  constructor(options: Partial<ImageProcessingOptions> = {}) {
    this.options = {
      maxWidth: options.maxWidth ?? 2048,
      maxHeight: options.maxHeight ?? 2048,
      quality: options.quality ?? 95,
      format: options.format ?? 'webp',
      preserveAspectRatio: options.preserveAspectRatio ?? true,
    };
  }
  
  /**
   * Process image và tạo Gemini Part
   */
  async processImage(
    input: Buffer | string
  ): Promise<{ part: Part; metadata: ImageMetadata }> {
    // Load image
    let image = sharp(input);
    const metadata = await image.metadata();
    
    // Resize nếu cần
    image = await this.resizeIfNeeded(image, metadata.width!, metadata.height!);
    
    // Convert sang target format
    const processedBuffer = await image
      .toFormat(this.options.format, { quality: this.options.quality })
      .toBuffer();
    
    // Detect mime type
    const mimeType = this.getMimeType(this.options.format);
    
    return {
      part: {
        inlineData: {
          mimeType,
          data: processedBuffer.toString('base64'),
        },
      },
      metadata: {
        originalSize: metadata.width! * metadata.height!,
        processedSize: processedBuffer.length,
        format: this.options.format,
        width: metadata.width,
        height: metadata.height,
      },
    };
  }
  
  private async resizeIfNeeded(
    image: sharp.Sharp,
    width: number,
    height: number
  ): Promise<sharp.Sharp> {
    if (width <= this.options.maxWidth && height <= this.options.maxHeight) {
      return image;
    }
    
    if (this.options.preserveAspectRatio) {
      return image.resize(this.options.maxWidth, this.options.maxHeight, {
        fit: 'inside',
        withoutEnlargement: true,
      });
    }
    
    return image.resize(this.options.maxWidth, this.options.maxHeight);
  }
  
  private getMimeType(format: string): string {
    const mimeTypes: Record<string, string> = {
      png: 'image/png',
      jpeg: 'image/jpeg',
      jpg: 'image/jpeg',
      webp: 'image/webp',
    };
    return mimeTypes[format] || 'image/png';
  }
}

interface ImageMetadata {
  originalSize: number;
  processedSize: number;
  format: string;
  width?: number;
  height?: number;
}
```

### 3. Video Processing - Xử Lý Video

Xử lý video với Gemini có một số đặc điểm riêng biệt so với images:

**Đặc điểm của Video Input:**

- **Format được hỗ trợ**: MP4, MPEG, WEBM
- **Kích thước tối đa**: 20MB cho mỗi video
- **Thời lượng**: Không có giới hạn cứng, nhưng bị giới hạn bởi token limit và file size
- **Frame sampling**: Gemini tự động sample frames từ video để phân tích
- **Audio track**: Nếu video có audio, Gemini sẽ xử lý cả âm thanh

**Chiến lược xử lý video:**

```python
# src/multimodal/video_processor.py
"""
Video processor cho Gemini API
Xử lý video trước khi gửi lên Gemini
"""

import io
import logging
from dataclasses import dataclass
from typing import Optional, List, Tuple, Union
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class VideoProcessingOptions:
    """Tùy chọn xử lý video."""
    max_duration_seconds: int = 120  # Giới hạn độ dài video
    target_fps: int = 1  # Số frames sample mỗi giây
    max_resolution: Tuple[int, int] = (1280, 720)
    quality: int = 80  # Chất lượng nén (1-100)
    extract_audio: bool = False  # Trích xuất audio riêng
    codec: str = "libx264"  # Video codec


class VideoProcessor:
    """
    Processor để chuẩn bị video cho Gemini API.
    Hỗ trợ cắt, resize, compress video.
    """
    
    SUPPORTED_FORMATS = {".mp4", ".mpeg", ".webm", ".mov"}
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
    
    def __init__(self, options: Optional[VideoProcessingOptions] = None):
        self.options = options or VideoProcessingOptions()
    
    def get_video_info(self, video_path: Union[str, Path]) -> dict:
        """
        Lấy thông tin video (thời lượng, kích thước, fps).
        Sử dụng ffprobe.
        """
        import subprocess
        import json
        
        video_path = str(video_path)
        
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        info = json.loads(result.stdout)
        
        # Extract relevant info
        video_stream = next(
            (s for s in info.get("streams", []) if s.get("codec_type") == "video"),
            None
        )
        
        audio_stream = next(
            (s for s in info.get("streams", []) if s.get("codec_type") == "audio"),
            None
        )
        
        format_info = info.get("format", {})
        
        return {
            "duration": float(format_info.get("duration", 0)),
            "size": int(format_info.get("size", 0)),
            "format": format_info.get("format_name", ""),
            "video_stream": {
                "codec": video_stream.get("codec_name") if video_stream else None,
                "width": video_stream.get("width") if video_stream else None,
                "height": video_stream.get("height") if video_stream else None,
                "fps": eval(video_stream.get("r_frame_rate", "0/1")) if video_stream else 0,
            } if video_stream else None,
            "has_audio": audio_stream is not None,
        }
    
    def create_video_part(
        self,
        video_path: Union[str, Path, bytes]
    ) -> "types.Part":
        """
        Tạo Gemini Part từ video file.
        
        Args:
            video_path: Đường dẫn video hoặc bytes
            
        Returns:
            Gemini Part object
        """
        from google.generativeai import types
        
        if isinstance(video_path, (str, Path)):
            with open(video_path, "rb") as f:
                video_bytes = f.read()
        elif isinstance(video_path, bytes):
            video_bytes = video_path
        else:
            raise ValueError(f"Unsupported video source type: {type(video_path)}")
        
        # Detect mime type từ magic bytes
        mime_type = self._detect_video_mime_type(video_bytes)
        
        logger.info(f"Creating video part: {len(video_bytes)} bytes, mime={mime_type}")
        
        return types.Part(
            inline_data=types.Blob(
                mime_type=mime_type,
                data=video_bytes
            )
        )
    
    def _detect_video_mime_type(self, data: bytes) -> str:
        """Detect video mime type từ file magic bytes."""
        if data.startswith(b'\x00\x00\x00'):
            # Check for MP4/MOV signature
            if b'ftyp' in data[:20]:
                return "video/mp4"
            if b'moov' in data[:20]:
                return "video/mp4"
        
        if data.startswith(b'\x1aE\xdf\xa3'):
            # WEBM signature
            return "video/webm"
        
        if data.startswith(b'\x00\x00\x01'):
            # MPEG signature
            return "video/mpeg"
        
        # Default to MP4
        return "video/mp4"
    
    def process_video_for_gemini(
        self,
        video_path: Union[str, Path]
    ) -> List["types.Part"]:
        """
        Process video và tạo các Parts cho Gemini.
        Nếu video quá dài, tự động chia thành các segments.
        
        Args:
            video_path: Đường dẫn video
            
        Returns:
            List of Gemini Parts
        """
        from google.generativeai import types
        
        info = self.get_video_info(video_path)
        duration = info["duration"]
        file_size = info["size"]
        
        logger.info(
            f"Processing video: duration={duration}s, size={file_size} bytes"
        )
        
        # Check nếu video quá dài
        if duration > self.options.max_duration_seconds:
            logger.warning(
                f"Video duration ({duration}s) exceeds limit ({self.options.max_duration_seconds}s). "
                "Will be processed but may result in high token usage."
            )
        
        # Check file size
        if file_size > self.MAX_FILE_SIZE:
            raise ValueError(
                f"Video file size ({file_size} bytes) exceeds 20MB limit. "
                "Please compress or truncate the video."
            )
        
        # Tạo single part cho video
        return [self.create_video_part(video_path)]


# Batch video processing
class VideoBatchProcessor:
    """
    Processor để xử lý batch nhiều videos.
    Hữu ích cho các tác vụ như video summarization, content analysis.
    """
    
    def __init__(
        self,
        video_processor: VideoProcessor,
        max_concurrent: int = 3
    ):
        self.video_processor = video_processor
        self.max_concurrent = max_concurrent
    
    async def process_video_batch(
        self,
        video_paths: List[Union[str, Path]],
        process_func: callable,
        progress_callback: Optional[callable] = None
    ) -> List[Any]:
        """
        Process batch videos với concurrent execution.
        
        Args:
            video_paths: Danh sách đường dẫn videos
            process_func: Function để xử lý mỗi video
            progress_callback: Callback để report progress
            
        Returns:
            List of results
        """
        import asyncio
        
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def process_with_semaphore(video_path, index):
            async with semaphore:
                result = await process_func(video_path)
                if progress_callback:
                    progress_callback(index + 1, len(video_paths))
                return result
        
        tasks = [
            process_with_semaphore(path, i)
            for i, path in enumerate(video_paths)
        ]
        
        return await asyncio.gather(*tasks)
```

### 4. Audio Processing - Xử Lý Âm Thanh

**Đặc điểm của Audio Input:**

- **Format được hỗ trợ**: WAV, MP3, MPEG, WEBM
- **Kích thước tối đa**: 20MB cho mỗi audio file
- **Thời lượng**: Phụ thuộc vào file size và bitrate
- **Sampling rate**: Khuyến nghị 16kHz hoặc 48kHz

```python
# src/multimodal/audio_processor.py
"""
Audio processor cho Gemini API
"""

import io
import logging
from dataclasses import dataclass
from typing import Optional, Union, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class AudioProcessingOptions:
    """Tùy chọn xử lý audio."""
    sample_rate: int = 16000  # 16kHz recommended
    channels: int = 1  # Mono
    format: str = "wav"  # Output format
    normalize: bool = True  # Normalize audio levels


class AudioProcessor:
    """Processor để chuẩn bị audio cho Gemini API."""
    
    SUPPORTED_FORMATS = {".wav", ".mp3", ".mpeg", ".webm", ".ogg", ".flac"}
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
    
    def __init__(self, options: Optional[AudioProcessingOptions] = None):
        self.options = options or AudioProcessingOptions()
    
    def create_audio_part(
        self,
        audio_path: Union[str, Path, bytes],
        mime_type: Optional[str] = None
    ) -> "types.Part":
        """
        Tạo Gemini Part từ audio file.
        
        Args:
            audio_path: Đường dẫn audio hoặc bytes
            mime_type: MIME type (tự động detect nếu không cung cấp)
            
        Returns:
            Gemini Part object
        """
        from google.generativeai import types
        
        if isinstance(audio_path, (str, Path)):
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
        elif isinstance(audio_path, bytes):
            audio_bytes = audio_path
        else:
            raise ValueError(f"Unsupported audio source type: {type(audio_path)}")
        
        # Auto-detect mime type
        if mime_type is None:
            mime_type = self._detect_audio_mime_type(audio_bytes, audio_path)
        
        logger.info(f"Creating audio part: {len(audio_bytes)} bytes, mime={mime_type}")
        
        return types.Part(
            inline_data=types.Blob(
                mime_type=mime_type,
                data=audio_bytes
            )
        )
    
    def _detect_audio_mime_type(
        self,
        data: bytes,
        source: Union[str, Path, bytes]
    ) -> str:
        """Detect audio mime type."""
        # Check file extension
        if isinstance(source, (str, Path)):
            ext = Path(source).suffix.lower()
            ext_to_mime = {
                ".wav": "audio/wav",
                ".mp3": "audio/mp3",
                ".mpeg": "audio/mpeg",
                ".webm": "audio/webm",
                ".ogg": "audio/ogg",
                ".flac": "audio/flac",
            }
            if ext in ext_to_mime:
                return ext_to_mime[ext]
        
        # Check magic bytes
        if data.startswith(b'RIFF') and b'WAVE' in data[:20]:
            return "audio/wav"
        if data.startswith(b'\xff\xfb') or data.startswith(b'\xff\xf3'):
            return "audio/mp3"
        if data.startswith(b'ID3'):
            return "audio/mpeg"
        
        # Default
        return "audio/wav"
```

### 5. PDF Analysis - Phân Tích PDF

Gemini xử lý PDF bằng cách render từng trang thành hình ảnh. Điều này có nghĩa là:

**Đặc điểm của PDF Input:**

- Mỗi trang PDF được coi như một hình ảnh riêng biệt
- Text trong PDF được OCR và xử lý như text
- Layout và formatting được preserve
- Chart, graph, và hình ảnh trong PDF cũng được phân tích

```python
# src/multimodal/pdf_processor.py
"""
PDF processor cho Gemini API
"""

import io
import logging
from dataclasses import dataclass
from typing import Optional, Union, List, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class PDFProcessingOptions:
    """Tùy chọn xử lý PDF."""
    max_pages: int = 100  # Giới hạn số trang
    dpi: int = 150  # Resolution cho rendering
    format: str = "PNG"  # Output format (PNG/JPEG)
    page_start: int = 0  # Trang bắt đầu
    page_end: Optional[int] = None  # Trang kết thúc


class PDFProcessor:
    """Processor để chuẩn bị PDF cho Gemini API."""
    
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
    
    def __init__(self, options: Optional[PDFProcessingOptions] = None):
        self.options = options or PDFProcessingOptions()
    
    def pdf_to_images(
        self,
        pdf_path: Union[str, Path, bytes]
    ) -> List[Tuple[int, bytes]]:
        """
        Convert PDF pages thành images.
        
        Returns:
            List of (page_number, image_bytes) tuples
        """
        try:
            from pypdf import PdfReader  # Hoặc PyMuPDF
        except ImportError:
            raise ImportError(
                "Please install pypdf or PyMuPDF: pip install pypdf"
            )
        
        # Load PDF
        if isinstance(pdf_path, (str, Path)):
            reader = PdfReader(pdf_path)
        elif isinstance(pdf_path, bytes):
            reader = PdfReader(io.BytesIO(pdf_path))
        else:
            raise ValueError(f"Unsupported PDF source type: {type(pdf_path)}")
        
        # Determine page range
        total_pages = len(reader.pages)
        start = self.options.page_start
        end = self.options.page_end or total_pages
        end = min(end, self.options.max_pages)
        
        logger.info(f"Converting PDF pages {start} to {end} ({total_pages} total pages)")
        
        images = []
        
        for page_num in range(start, end):
            page = reader.pages[page_num]
            
            # Render page to image
            # Sử dụng PyMuPDF cho quality tốt hơn
            try:
                import fitz  # PyMuPDF
                
                if isinstance(pdf_path, (str, Path)):
                    doc = fitz.open(pdf_path)
                else:
                    doc = fitz.open(stream=pdf_path, filetype="pdf")
                
                page = doc[page_num]
                mat = fitz.Matrix(self.options.dpi / 72, self.options.dpi / 72)
                pix = page.get_pixmap(matrix=mat)
                
                if self.options.format == "PNG":
                    img_bytes = pix.tobytes("png")
                else:
                    img_bytes = pix.tobytes("jpeg")
                
                images.append((page_num + 1, img_bytes))
                doc.close()
                
            except ImportError:
                # Fallback: sử dụng pdf2image
                from pdf2image import convert_from_path
                
                if isinstance(pdf_path, (str, Path)):
                    images_list = convert_from_path(
                        pdf_path,
                        dpi=self.options.dpi,
                        first_page=page_num + 1,
                        last_page=page_num + 1,
                        fmt=self.options.format.lower()
                    )
                else:
                    from pdf2image import convert_from_bytes
                    images_list = convert_from_bytes(
                        pdf_path,
                        dpi=self.options.dpi,
                        first_page=page_num + 1,
                        last_page=page_num + 1,
                        fmt=self.options.format.lower()
                    )
                
                for img in images_list:
                    buf = io.BytesIO()
                    img.save(buf, format=self.options.format)
                    images.append((page_num + 1, buf.getvalue()))
        
        return images
    
    def create_pdf_parts(
        self,
        pdf_path: Union[str, Path, bytes],
        combine_pages: bool = False
    ) -> Union[List["types.Part"], "types.Part"]:
        """
        Tạo Gemini Parts từ PDF.
        
        Args:
            pdf_path: Đường dẫn PDF hoặc bytes
            combine_pages: Nếu True, combine tất cả pages thành một Part
            
        Returns:
            List of Parts hoặc single Part (nếu combine_pages=True)
        """
        from google.generativeai import types
        
        images = self.pdf_to_images(pdf_path)
        
        if combine_pages:
            # Combine all pages vào một part
            combined_parts = []
            for page_num, img_bytes in images:
                combined_parts.append(
                    types.Part(
                        text=f"Page {page_num}:\n"
                    ),
                    types.Part(
                        inline_data=types.Blob(
                            mime_type=f"image/{self.options.format.lower()}",
                            data=img_bytes
                        )
                    )
                )
            # Flatten list
            return [part for part_tuple in zip(combined_parts[::2], combined_parts[1::2]) for part in part_tuple]
        else:
            # Tạo separate parts cho mỗi page
            parts = []
            for page_num, img_bytes in images:
                parts.extend([
                    types.Part(
                        text=f"Trang {page_num}:\n"
                    ),
                    types.Part(
                        inline_data=types.Blob(
                            mime_type=f"image/{self.options.format.lower()}",
                            data=img_bytes
                        )
                    )
                ])
            return parts
```

## Token Calculation Cho Multimodal Inputs

Việc tính token cho multimodal inputs là phức tạp hơn so với text thuần túy. Dưới đây là cách Gemini tính token:

### Token Calculation Formulas

```python
# src/multimodal/token_calculator.py
"""
Token Calculator cho Multimodal Inputs
"""

import math
from dataclasses import dataclass
from typing import Optional, Union, List


@dataclass
class TokenEstimate:
    """Kết quả ước tính token."""
    text_tokens: int
    image_tokens: int
    video_tokens: int
    audio_tokens: int
    total_tokens: int
    
    def __str__(self) -> str:
        return (
            f"TokenEstimate(\n"
            f"  text={self.text_tokens},\n"
            f"  image={self.image_tokens},\n"
            f"  video={self.video_tokens},\n"
            f"  audio={self.audio_tokens},\n"
            f"  total={self.total_tokens}\n"
            f")"
        )


class MultimodalTokenCalculator:
    """
    Calculator để ước tính token usage cho multimodal inputs.
    
    Công thức token calculation:
    - Text: ~4 characters = 1 token (tùy language)
    - Images: Dựa trên kích thước ảnh sau khi encode
    - Video: Dựa trên số frames và kích thước
    - Audio: 1 token per ~0.6 seconds (cho 16kHz audio)
    """
    
    # Text token estimation
    CHARS_PER_TOKEN = 4
    
    # Image token calculation constants
    # Gemini tính token dựa trên kích thước ảnh gốc, không phải compressed
    # Base tokens cho mỗi image
    BASE_IMAGE_TOKENS = 258  # Minimum tokens cho một image
    
    # Scale factor: tokens tăng theo kích thước ảnh
    # 256x256 = ~258 tokens
    # Mỗi lần tăng gấp đôi kích thước, tokens tăng ~258
    # Maximum cho một image: ~4096 tokens
    
    # Video token constants
    # 1 frame được tính như 1 image
    # Plus overhead cho temporal information
    FRAME_TOKENS = 258  # Tokens per frame
    VIDEO_OVERHEAD_PER_SECOND = 85  # Additional tokens per second
    
    # Audio token constants
    AUDIO_SECONDS_PER_TOKEN = 0.6  # ~0.6 seconds per token
    
    def estimate_text_tokens(self, text: str) -> int:
        """Ước tính tokens cho text."""
        return math.ceil(len(text) / self.CHARS_PER_TOKEN)
    
    def estimate_image_tokens(
        self,
        width: int,
        height: int,
        include_video_frame: bool = False
    ) -> int:
        """
        Ước tính tokens cho một image.
        
        Args:
            width: Chiều rộng pixels
            height: Chiều cao pixels
            include_video_frame: Đang xử lý như video frame
            
        Returns:
            Số tokens ước tính
        """
        # Tính số lượng 256x256 patches cần thiết
        patches_x = math.ceil(width / 256)
        patches_y = math.ceil(height / 256)
        total_patches = patches_x * patches_y
        
        # Tokens cho patches
        patch_tokens = total_patches * 258
        
        # Tokens cho overhead
        overhead_tokens = 170 if not include_video_frame else 85
        
        return patch_tokens + overhead_tokens
    
    def estimate_video_tokens(
        self,
        duration_seconds: float,
        fps: int = 1,
        width: int = 1920,
        height: int = 1080
    ) -> int:
        """
        Ước tính tokens cho video.
        
        Args:
            duration_seconds: Thời lượng video (giây)
            fps: Frames per second được sample
            width: Chiều rộng frame
            height: Chiều cao frame
            
        Returns:
            Số tokens ước tính
        """
        # Số frames
        num_frames = min(int(duration_seconds * fps), 300)  # Max 300 frames
        
        # Tokens cho frames (như images)
        frame_tokens = num_frames * self.estimate_image_tokens(width, height, True)
        
        # Overhead cho temporal information
        temporal_tokens = int(duration_seconds * self.VIDEO_OVERHEAD_PER_SECOND)
        
        return frame_tokens + temporal_tokens
    
    def estimate_audio_tokens(
        self,
        duration_seconds: float,
        sample_rate: int = 16000
    ) -> int:
        """
        Ước tính tokens cho audio.
        
        Args:
            duration_seconds: Thời lượng audio (giây)
            sample_rate: Sample rate (Hz)
            
        Returns:
            Số tokens ước tính
        """
        return math.ceil(duration_seconds / self.AUDIO_SECONDS_PER_TOKEN)
    
    def estimate_multimodal_tokens(
        self,
        text: Optional[str] = None,
        images: Optional[List[tuple]] = None,  # [(width, height), ...]
        videos: Optional[List[dict]] = None,   # [{duration, fps, width, height}, ...]
        audios: Optional[List[tuple]] = None,   # [(duration, sample_rate), ...]
    ) -> TokenEstimate:
        """
        Ước tính tổng tokens cho multimodal input.
        
        Args:
            text: Text content
            images: List of (width, height) tuples
            videos: List of video info dicts
            audios: List of (duration, sample_rate) tuples
            
        Returns:
            TokenEstimate object
        """
        text_tokens = self.estimate_text_tokens(text) if text else 0
        
        image_tokens = 0
        if images:
            for width, height in images:
                image_tokens += self.estimate_image_tokens(width, height)
        
        video_tokens = 0
        if videos:
            for video in videos:
                video_tokens += self.estimate_video_tokens(
                    duration_seconds=video.get("duration", 0),
                    fps=video.get("fps", 1),
                    width=video.get("width", 1920),
                    height=video.get("height", 1080)
                )
        
        audio_tokens = 0
        if audios:
            for duration, sample_rate in audios:
                audio_tokens += self.estimate_audio_tokens(duration, sample_rate)
        
        return TokenEstimate(
            text_tokens=text_tokens,
            image_tokens=image_tokens,
            video_tokens=video_tokens,
            audio_tokens=audio_tokens,
            total_tokens=text_tokens + image_tokens + video_tokens + audio_tokens
        )
    
    def can_fit_in_context(
        self,
        total_tokens: int,
        context_limit: int = 1000000,
        reserve_for_response: int = 1000
    ) -> tuple[bool, int]:
        """
        Kiểm tra xem tokens có fit trong context window không.
        
        Returns:
            (can_fit, remaining_tokens)
        """
        available = context_limit - reserve_for_response
        can_fit = total_tokens <= available
        remaining = max(0, available - total_tokens)
        
        return can_fit, remaining
```

## Best Practices

### 1. Tối Ưu Hóa Image Inputs

```python
# Best practices cho image processing

# 1. Resize ảnh trước khi gửi - không cần gửi ảnh 4K nếu Gemini sẽ downscale
# Gemini tự động downscale, nhưng bạn vẫn phải trả token cho ảnh gốc

# 2. Sử dụng định dạng hiệu quả
# WEBP thường cho compression tốt nhất với quality cao
# PNG chỉ khi cần transparency
# JPEG cho photos

# 3. Strip metadata không cần thiết
# EXIF, IPTC, XMP metadata không cần thiết cho Gemini
# Giảm kích thước file mà không ảnh hưởng quality

# 4. Chọn đúng vùng cần phân tích
# Nếu chỉ cần phân tích một phần của ảnh, crop trước
# Giảm token usage đáng kể
```

### 2. Video Processing Strategy

```python
# Chiến lược xử lý video hiệu quả

# 1. Sampling strategy
# Để phân tích nội dung, 1 FPS thường đủ
# Để phân tích chuyển động, cần 2-4 FPS
# Để phân tích chi tiết, có thể cần 10+ FPS

# 2. Pre-processing
# Trim video chỉ giữ phần cần thiết
# Lower resolution nếu không cần chi tiết
# Convert sang format efficient (MP4/H.264)

# 3. Chunking cho videos dài
# Nếu video > 2 phút, consider chunking thành segments
# Process mỗi segment riêng rồi combine kết quả
```

### 3. Error Handling Cho Multimodal

```python
# Error handling patterns

class MultimodalError(Exception):
    """Base exception cho multimodal processing."""
    pass

class FileTooLargeError(MultimodalError):
    """File vượt quá kích thước tối đa."""
    pass

class UnsupportedFormatError(MultimodalError):
    """Format không được hỗ trợ."""
    pass

class ContextWindowExceededError(MultimodalError):
    """Content vượt quá context window."""
    pass

def process_multimodal_safely(
    model,
    parts: List,
    max_context_tokens: int = 1000000
) -> str:
    """
    Process multimodal input với error handling.
    """
    try:
        # Count tokens trước
        token_count = model.count_tokens(parts)
        
        if token_count.total_tokens > max_context_tokens:
            raise ContextWindowExceededError(
                f"Content exceeds context window: {token_count.total_tokens} > {max_context_tokens}"
            )
        
        # Generate response
        response = model.generate_content(parts)
        
        # Check nếu response bị blocked
        if not response.candidates:
            if response.prompt_feedback:
                raise MultimodalError(
                    f"Content blocked: {response.prompt_feedback.block_reason}"
                )
            raise MultimodalError("No response generated")
        
        return response.text
        
    except Exception as e:
        logger.error(f"Error processing multimodal: {e}")
        raise
```

## Common Patterns

### 1. Document Analysis Pipeline

```python
# src/pipelines/document_analysis.py
"""
Document Analysis Pipeline - Phân tích tài liệu đa format
"""

from typing import List, Optional, Union
from dataclasses import dataclass
import logging

from src.multimodal.image_processor import ImageProcessor
from src.multimodal.pdf_processor import PDFProcessor
from src.multimodal.token_calculator import MultimodalTokenCalculator

logger = logging.getLogger(__name__)


@dataclass
class DocumentAnalysisResult:
    """Kết quả phân tích document."""
    text: str
    token_usage: int
    pages_processed: int
    processing_time_ms: int
    warnings: List[str]


class DocumentAnalysisPipeline:
    """
    Pipeline để phân tích các loại tài liệu khác nhau:
    - PDF documents
    - Images (scanned documents, screenshots)
    - Mixed content
    """
    
    def __init__(
        self,
        model,
        config: Optional[dict] = None
    ):
        self.model = model
        self.config = config or {}
        
        self.pdf_processor = PDFProcessor()
        self.image_processor = ImageProcessor()
        self.token_calculator = MultimodalTokenCalculator()
    
    async def analyze_document(
        self,
        file_path: Union[str, bytes],
        file_type: str,
        question: str,
        options: Optional[dict] = None
    ) -> DocumentAnalysisResult:
        """
        Phân tích document với câu hỏi cụ thể.
        
        Args:
            file_path: Đường dẫn file hoặc bytes
            file_type: Loại file ('pdf', 'image', 'png', 'jpg', etc.)
            question: Câu hỏi về document
            options: Tùy chọn xử lý
            
        Returns:
            DocumentAnalysisResult object
        """
        import time
        start_time = time.time()
        warnings = []
        
        # Tạo prompt
        prompt_parts = [f"Phân tích tài liệu sau và trả lời câu hỏi: {question}\n\n"]
        
        # Process theo loại file
        if file_type.lower() in ['pdf']:
            pages = self.pdf_processor.pdf_to_images(file_path)
            pages_processed = len(pages)
            
            for page_num, img_bytes in pages:
                prompt_parts.append(
                    f"--- Trang {page_num} ---\n"
                )
                prompt_parts.append(
                    self.image_processor.create_gemini_part(img_bytes)
                )
        
        elif file_type.lower() in ['png', 'jpg', 'jpeg', 'webp', 'gif']:
            pages_processed = 1
            prompt_parts.append(
                self.image_processor.create_gemini_part(file_path)
            )
        
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Ước tính tokens
        token_estimate = self.token_calculator.estimate_multimodal_tokens(
            text=question,
            images=[(2048, 2048)] * pages_processed
        )
        
        if token_estimate.total_tokens > 900000:
            warnings.append(
                f"Token usage high ({token_estimate.total_tokens}). "
                "Consider reducing document size."
            )
        
        # Generate response
        try:
            response = self.model.generate_content(prompt_parts)
            text = response.text
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            text = f"Lỗi khi phân tích document: {str(e)}"
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return DocumentAnalysisResult(
            text=text,
            token_usage=token_estimate.total_tokens,
            pages_processed=pages_processed,
            processing_time_ms=processing_time,
            warnings=warnings
        )
```

### 2. Multi-Image Comparison

```typescript
// src/pipelines/image-comparison.ts
/**
 * So sánh nhiều images với Gemini
 */

import { Part } from '@google/generative-ai';
import { ImageProcessor } from '../multimodal/image-processor';

interface ImageComparisonResult {
  comparison: string;
  similarities: string[];
  differences: string[];
  recommendations: string[];
}

export class ImageComparisonPipeline {
  private model: ReturnType<GoogleGenerativeAI['getGenerativeModel']>;
  private imageProcessor: ImageProcessor;
  
  constructor(model: ReturnType<GoogleGenerativeAI['getGenerativeModel']>) {
    this.model = model;
    this.imageProcessor = new ImageProcessor();
  }
  
  /**
   * So sánh nhiều images với nhau
   */
  async compareImages(
    imagePaths: string[],
    comparisonType: 'differences' | 'similarities' | 'both' = 'both',
    customPrompt?: string
  ): Promise<ImageComparisonResult> {
    // Process all images
    const processedImages: Part[] = [];
    
    for (let i = 0; i < imagePaths.length; i++) {
      const { part } = await this.imageProcessor.processImage(imagePaths[i]);
      processedImages.push(part);
    }
    
    // Build prompt
    let prompt = '';
    
    if (customPrompt) {
      prompt = customPrompt;
    } else {
      const comparisonInstructions = {
        differences: 'Liệt kê chi tiết các điểm khác biệt giữa các ảnh.',
        similarities: 'Liệt kê chi tiết các điểm giống nhau giữa các ảnh.',
        both: 'Phân tích chi tiết cả điểm giống và khác nhau giữa các ảnh.',
      };
      
      prompt = `
Phân tích và so sánh ${imagePaths.length} hình ảnh sau đây.

${comparisonInstructions[comparisonType]}

Trả lời theo format:
1. Tổng quan: [Mô tả ngắn gọn]
2. Điểm giống nhau: [Danh sách]
3. Điểm khác nhau: [Danh sách chi tiết]
4. Nhận xét: [Đánh giá tổng quan]
`;
    }
    
    // Generate response
    const result = await this.model.generateContent([prompt, ...processedImages]);
    const responseText = result.response.text();
    
    // Parse response (simplified - in production, use structured output)
    return {
      comparison: responseText,
      similarities: this.extractListItems(responseText, 'giống'),
      differences: this.extractListItems(responseText, 'khác'),
      recommendations: [],
    };
  }
  
  private extractListItems(text: string, keyword: string): string[] {
    // Simple extraction - in production use more robust parsing
    const lines = text.split('\n');
    const items: string[] = [];
    let captureMode = false;
    
    for (const line of lines) {
      if (line.includes(keyword)) {
        captureMode = true;
        continue;
      }
      
      if (captureMode && line.trim().match(/^[-•\d]/)) {
        items.push(line.replace(/^[-•\d]\s*/, '').trim());
      }
    }
    
    return items;
  }
}
```

## Examples

### 1. Complete Multimodal Analysis Example - Python

```python
# src/examples/multimodal_analysis.py
"""
Complete example: Multimodal analysis với Gemini
"""

import asyncio
from pathlib import Path
from typing import List, Optional

from google.generativeai import GenerativeModel
from src.config.gemini_config import GeminiConfig, initialize_gemini, create_model
from src.multimodal.image_processor import ImageProcessor
from src.multimodal.pdf_processor import PDFProcessor
from src.multimodal.token_calculator import MultimodalTokenCalculator


class MultimodalAnalyzer:
    """Complete multimodal analysis service."""
    
    def __init__(self, config: Optional[GeminiConfig] = None):
        if config is None:
            config = GeminiConfig.from_env()
        
        initialize_gemini(config)
        self.model = create_model(config)
        
        self.image_processor = ImageProcessor()
        self.pdf_processor = PDFProcessor()
        self.token_calculator = MultimodalTokenCalculator()
    
    async def analyze_image(
        self,
        image_path: str,
        prompt: str = "Mô tả chi tiết nội dung của hình ảnh này."
    ) -> dict:
        """Phân tích một hình ảnh."""
        
        # Process image
        image_part = self.image_processor.create_gemini_part(image_path)
        
        # Create prompt
        full_prompt = [
            prompt,
            image_part
        ]
        
        # Count tokens
        tokens = self.model.count_tokens(full_prompt)
        print(f"Token usage: {tokens.total_tokens}")
        
        # Generate response
        response = self.model.generate_content(full_prompt)
        
        return {
            "text": response.text,
            "tokens_used": tokens.total_tokens,
            "prompt_feedback": response.prompt_feedback,
        }
    
    async def analyze_pdf(
        self,
        pdf_path: str,
        question: str
    ) -> dict:
        """Phân tích một PDF document."""
        
        # Convert PDF to images
        pages = self.pdf_processor.pdf_to_images(pdf_path)
        
        print(f"Processing {len(pages)} pages...")
        
        # Create prompt parts
        prompt_parts = [
            f"Phân tích document PDF này và trả lời câu hỏi: {question}\n\n"
        ]
        
        for page_num, img_bytes in pages:
            prompt_parts.append(f"--- Trang {page_num} ---\n")
            prompt_parts.append(
                self.image_processor.create_gemini_part(img_bytes)
            )
        
        # Count tokens
        tokens = self.model.count_tokens(prompt_parts)
        print(f"Token usage: {tokens.total_tokens}")
        
        # Generate response
        response = self.model.generate_content(prompt_parts)
        
        return {
            "text": response.text,
            "tokens_used": tokens.total_tokens,
            "pages_processed": len(pages),
        }
    
    async def analyze_images_batch(
        self,
        image_paths: List[str],
        prompt: str = "Phân tích và so sánh các hình ảnh này."
    ) -> dict:
        """Phân tích batch nhiều hình ảnh."""
        
        # Process all images
        prompt_parts = [f"{prompt}\n\n"]
        
        for i, path in enumerate(image_paths):
            print(f"Processing image {i + 1}/{len(image_paths)}: {path}")
            image_part = self.image_processor.create_gemini_part(path)
            prompt_parts.append(f"--- Hình {i + 1} ---\n")
            prompt_parts.append(image_part)
        
        # Count tokens
        tokens = self.model.count_tokens(prompt_parts)
        print(f"Total token usage: {tokens.total_tokens}")
        
        # Generate response
        response = self.model.generate_content(prompt_parts)
        
        return {
            "text": response.text,
            "tokens_used": tokens.total_tokens,
            "images_processed": len(image_paths),
        }


async def main():
    """Main execution."""
    
    analyzer = MultimodalAnalyzer()
    
    # Example 1: Image analysis
    print("=" * 50)
    print("Example 1: Image Analysis")
    print("=" * 50)
    
    result = await analyzer.analyze_image(
        image_path="sample_image.png",
        prompt="Mô tả chi tiết nội dung và bố cục của hình ảnh này."
    )
    print(f"Result: {result['text']}")
    print(f"Tokens: {result['tokens_used']}")
    
    # Example 2: PDF analysis
    print("\n" + "=" * 50)
    print("Example 2: PDF Analysis")
    print("=" * 50)
    
    result = await analyzer.analyze_pdf(
        pdf_path="document.pdf",
        question="Tóm tắt nội dung chính của tài liệu này."
    )
    print(f"Result: {result['text']}")
    print(f"Pages: {result['pages_processed']}, Tokens: {result['tokens_used']}")


if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Complete Multimodal Example - TypeScript

```typescript
// src/examples/multimodal-analysis.ts
/**
 * Complete example: Multimodal analysis với Gemini (TypeScript)
 */

import { GoogleGenerativeAI, Part } from '@google/generative-ai';
import { ImageProcessor } from '../multimodal/image-processor';
import fs from 'fs/promises';
import path from 'path';

interface AnalysisResult {
  text: string;
  tokensUsed: number;
  metadata?: Record<string, any>;
}

export class MultimodalAnalyzerTS {
  private client: GoogleGenerativeAI;
  private model: ReturnType<GoogleGenerativeAI['getGenerativeModel']>;
  private imageProcessor: ImageProcessor;
  
  constructor(apiKey: string) {
    this.client = new GoogleGenerativeAI(apiKey);
    this.model = this.client.getGenerativeModel({
      model: 'gemini-2.0-flash',
    });
    this.imageProcessor = new ImageProcessor();
  }
  
  /**
   * Analyze a single image
   */
  async analyzeImage(
    imagePath: string,
    prompt: string = 'Mô tả chi tiết nội dung của hình ảnh này.'
  ): Promise<AnalysisResult> {
    // Load and process image
    const imageBuffer = await fs.readFile(imagePath);
    const { part, metadata } = await this.imageProcessor.processImage(imageBuffer);
    
    // Generate content
    const result = await this.model.generateContent([prompt, part]);
    const responseText = result.response.text();
    
    // Count tokens
    const countResult = await this.model.countTokens([prompt, part]);
    
    return {
      text: responseText,
      tokensUsed: countResult.totalTokens,
      metadata,
    };
  }
  
  /**
   * Analyze multiple images
   */
  async analyzeMultipleImages(
    imagePaths: string[],
    prompt: string = 'Phân tích và so sánh các hình ảnh này.'
  ): Promise<AnalysisResult> {
    const parts: Part[] = [];
    
    for (const imagePath of imagePaths) {
      const imageBuffer = await fs.readFile(imagePath);
      const { part } = await this.imageProcessor.processImage(imageBuffer);
      parts.push(part);
    }
    
    const content = [prompt, ...parts];
    const result = await this.model.generateContent(content);
    const countResult = await this.model.countTokens(content);
    
    return {
      text: result.response.text(),
      tokensUsed: countResult.totalTokens,
      metadata: { imageCount: imagePaths.length },
    };
  }
  
  /**
   * Analyze PDF (as images)
   */
  async analyzePDF(
    pdfPath: string,
    question: string
  ): Promise<AnalysisResult> {
    // Note: In production, use pdf-parse or similar library
    // to extract text directly from PDF
    
    const pdfBuffer = await fs.readFile(pdfPath);
    
    // Convert PDF to images using pdf2image or similar
    // For this example, we'll assume the PDF is already converted
    const imagePaths = [/* extracted page images */];
    
    const parts: Part[] = [`Phân tích PDF và trả lời: ${question}\n\n`];
    
    for (const imagePath of imagePaths) {
      const { part } = await this.imageProcessor.processImage(imagePath);
      parts.push(part);
    }
    
    const result = await this.model.generateContent(parts);
    const countResult = await this.model.countTokens(parts);
    
    return {
      text: result.response.text(),
      tokensUsed: countResult.totalTokens,
      metadata: { pageCount: imagePaths.length },
    };
  }
}

// Usage
async function main() {
  const apiKey = process.env.GEMINI_API_KEY!;
  const analyzer = new MultimodalAnalyzerTS(apiKey);
  
  // Single image analysis
  const imageResult = await analyzer.analyzeImage(
    'sample.png',
    'Mô tả chi tiết hình ảnh này.'
  );
  console.log('Image Analysis:', imageResult);
  
  // Multiple images
  const multiResult = await analyzer.analyzeMultipleImages(
    ['image1.png', 'image2.png', 'image3.png'],
    'So sánh các hình ảnh này và chỉ ra điểm giống và khác nhau.'
  );
  console.log('Multi-Image Analysis:', multiResult);
}

main().catch(console.error);
```

## Troubleshooting

### Các Vấn Đề Thường Gặp

**1. "Image too large" Error**

```
Nguyên nhân: File image vượt quá giới hạn 20MB hoặc resolution quá lớn
Giải pháp:
- Resize image xuống max 4096x4096 pixels
- Compress với quality thấp hơn (80-90)
- Convert sang WEBP format để giảm kích thước
- Sử dụng function ở trên để pre-process images
```

**2. "Video format not supported" Error**

```
Nguyên nhân: Video codec hoặc container không được hỗ trợ
Giải pháp:
- Convert sang MP4 với H.264 codec
- Sử dụng ffmpeg: ffmpeg -i input.avi -c:v libx264 output.mp4
- Kiểm tra file signature (magic bytes)
```

**3. "PDF page rendering failed" Error**

```
Nguyên nhân: PDF có protection, encryption, hoặc format phức tạp
Giải pháp:
- Unprotect PDF trước khi xử lý
- Sử dụng PyMuPDF thay vì pdf2image
- Convert PDF pages sang images với higher DPI
- Kiểm tra PDF không bị corrupt
```

**4. "Context window exceeded" Error**

```
Nguyên nhân: Tổng tokens vượt quá context limit
Giải pháp:
- Giảm số lượng images/videos trong request
- Lower resolution của images
- Sử dụng context management strategies (xem file context-window.md)
- Chunk large content thành multiple requests
```

**5. "Audio processing error"**

```
Nguyên nhân: Audio format không được hỗ trợ hoặc corrupted
Giải pháp:
- Convert sang WAV 16kHz
- Kiểm tra audio không bị corrupt
- Verify audio has playable content
```

## References

### Official Documentation

- [Gemini Vision Documentation](https://ai.google.dev/docs/gemini-vision)
- [Multimodal Inputs Guide](https://ai.google.dev/docs/multimodal)
- [File Uploads Documentation](https://ai.google.dev/docs/file-uploads)
- [Token Counting API](https://ai.google.dev/docs/tokens)

### Libraries

- [Sharp](https://sharp.pixelplumbing.com/) - Image processing cho Node.js
- [Pillow](https://pillow.readthedocs.io/) - Image processing cho Python
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) - PDF processing
- [pdf2image](https://pypi.org/project/pdf2image/) - PDF to images

### Related Documents

- `@gemini-api-setup.md` - Setup và configuration
- `@context-window.md` - Context management strategies
- `@performance.mdc` - Tối ưu hiệu suất
