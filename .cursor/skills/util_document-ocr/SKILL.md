# Document OCR Skill - Text Extraction from Images

## Mục tiêu

Tích hợp OCR (Optical Character Recognition) vào Cursor Enterprise Framework để:
- Tự động đọc text từ ảnh, file scanned, PDF
- Tăng khả năng đọc hiểu khi vibe coding
- Hỗ trợ nhiều ngôn ngữ (Vietnamese, English, Chinese, etc.)
- Extract text từ screenshot, diagram, flowchart

## OCR Engine

### Tesseract.js (Recommended - Node.js/Browser)

```bash
# Cài đặt Tesseract.js
npm install tesseract.js

# Hoặc Python binding
pip install pytesseract
```

### Sử dụng Python (pytesseract)

```python
import pytesseract
from PIL import Image

# Đọc text từ ảnh
img = Image.open('document.png')
text = pytesseract.image_to_string(img, lang='vie+eng')
print(text)

# Với preprocessing
from PIL import ImageFilter, ImageEnhance

img = Image.open('document.png')
# Convert to grayscale
img = img.convert('L')
# Enhance contrast
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2)
# Apply sharpening
img = img.filter(ImageFilter.SHARPEN)

text = pytesseract.image_to_string(img, lang='vie+eng')
```

### Sử dụng Node.js (Tesseract.js)

```javascript
import Tesseract from 'tesseract.js';

// Basic usage
const { data: { text } } = await Tesseract.recognize(
  'document.png',
  'vie+eng',
  { logger: m => console.log(m) }
);
console.log(text);

// Advanced with worker
const worker = await Tesseract.createWorker('vie+eng');
const { data } = await worker.recognize('document.png');
console.log(data.text);
await worker.terminate();
```

## Supported File Types

| Type | Extension | Support |
|------|----------|---------|
| Images | png, jpg, jpeg, tiff, bmp, webp | Full |
| PDF (scanned) | pdf | Via image conversion |
| Screenshots | png, jpg | Full |
| Diagrams | png, svg | With preprocessing |

## Language Support

### Vietnamese OCR

```python
# Vietnamese OCR với preprocessing
import pytesseract
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

def preprocess_for_vietnamese(image_path):
    img = Image.open(image_path)
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    
    # Increase brightness
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.2)
    
    # Apply sharpening
    img = img.filter(ImageFilter.SHARPEN)
    
    # Auto-invert nếu background tối
    if sum(img.getpixel((0, 0))) < 128:
        img = ImageOps.invert(img)
    
    return img

# OCR Vietnamese
img = preprocess_for_vietnamese('hoadon.png')
text = pytesseract.image_to_string(img, lang='vie')
```

### Multi-language OCR

```python
# Multiple languages
text = pytesseract.image_to_string(img, lang='vie+eng')
text = pytesseract.image_to_string(img, lang='vie+eng+chi_sim')
text = pytesseract.image_to_string(img, lang='eng')
```

## Preprocessing Pipeline

### Image Enhancement

```python
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import numpy as np

def enhance_document(image_path, output_path=None):
    """Enhanced document preprocessing pipeline"""
    img = Image.open(image_path)
    
    # 1. Convert to grayscale
    img = img.convert('L')
    
    # 2. Denoise
    img = img.filter(ImageFilter.MedianFilter(size=3))
    
    # 3. Increase contrast (1.5x)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    
    # 4. Increase sharpness
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.5)
    
    # 5. Auto levels
    img = ImageOps.autocontrast(img)
    
    # 6. Resize for better OCR (300 DPI)
    # base_size = 3000
    # w, h = img.size
    # if max(w, h) > base_size:
    #     ratio = base_size / max(w, h)
    #     img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
    
    if output_path:
        img.save(output_path)
    
    return img

def extract_text_from_document(image_path, lang='vie+eng'):
    """Full extraction pipeline"""
    # Preprocess
    img = enhance_document(image_path)
    
    # OCR
    text = pytesseract.image_to_string(img, lang=lang)
    
    # Post-process
    text = text.strip()
    
    return text
```

### Advanced Preprocessing (OpenCV)

```python
# Sử dụng OpenCV cho advanced preprocessing
import cv2
import numpy as np
from PIL import Image
import pytesseract

def opencv_preprocess(image_path):
    """OpenCV-based document enhancement"""
    # Read image
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    
    # Threshold (Otsu's method)
    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Morphological operations
    kernel = np.ones((1, 1), np.uint8)
    processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    # Convert back to PIL Image
    processed_pil = Image.fromarray(processed)
    
    return processed_pil
```

## Skill Auto-Discovery Integration

| Keyword / Pattern | Skill | Confidence |
|---|---|---|
| `ocr` | document-ocr | 0.95 |
| `text extraction` | document-ocr | 0.95 |
| `read text from image` | document-ocr | 0.95 |
| `image to text` | document-ocr | 0.90 |
| `scanned pdf` | document-ocr | 0.85 |
| `screenshot text` | document-ocr | 0.90 |
| `vietnamese ocr` | document-ocr | 0.95 |
| `extract text` | document-ocr | 0.85 |
| `document scanner` | document-ocr | 0.80 |

## Pre-Processing Workflow

### Bước 1: Image Quality Check

```
[ ] Image resolution >= 300 DPI
[ ] Text clearly visible
[ ] No excessive blur
[ ] Good contrast
```

### Bước 2: Preprocessing

```
1. Convert to grayscale
2. Remove noise (denoise filter)
3. Increase contrast
4. Sharpen image
5. Auto-levels/contrast
```

### Bước 3: OCR Configuration

```
Language: vie+eng (Vietnamese + English)
PSM (Page Segmentation Mode):
  - 3 = Fully automatic page segmentation
  - 6 = Assume uniform block of text
  - 11 = Sparse text
OEM (OCR Engine Mode):
  - 3 = Default, based on what is available
```

### Bước 4: Post-processing

```
1. Strip whitespace
2. Fix common OCR errors
3. Validate extracted text
4. Output structured data
```

## Vibe Coding Use Cases

### 1. Screenshot to Code

```
Screenshot UI → OCR → Analyze structure → Generate code
```

```python
# Screenshot → Text → Analysis pipeline
def screenshot_to_analysis(image_path):
    # Extract text from screenshot
    text = extract_text_from_document(image_path)
    
    # Analyze for UI elements
    ui_elements = extract_ui_hints(text)
    
    # Generate component suggestions
    return generate_component_suggestions(ui_elements)
```

### 2. Document to Spec

```
PDF/Image → OCR → Extract requirements → Generate SPEC.md
```

### 3. Diagram to Code

```
Architecture diagram → OCR → Extract components → Generate code
```

## CLI Tools

### Python CLI Script

```python
#!/usr/bin/env python3
"""OCR CLI Tool for Document Scanner Integration"""

import argparse
import sys
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance

try:
    import pytesseract
except ImportError:
    print("Error: pytesseract not installed. Run: pip install pytesseract")
    sys.exit(1)

def preprocess_image(img, enhance=True):
    """Preprocess image for better OCR results"""
    # Convert to grayscale
    img = img.convert('L')
    
    if enhance:
        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        
        # Sharpen
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.5)
        
        # Denoise
        img = img.filter(ImageFilter.MedianFilter(size=3))
    
    return img

def extract_text(image_path, lang='vie+eng', preprocess=True, output=None):
    """Extract text from image"""
    img = Image.open(image_path)
    
    if preprocess:
        img = preprocess_image(img)
    
    text = pytesseract.image_to_string(img, lang=lang)
    
    if output:
        Path(output).write_text(text, encoding='utf-8')
        print(f"Text saved to: {output}")
    
    return text

def main():
    parser = argparse.ArgumentParser(description='OCR Text Extraction Tool')
    parser.add_argument('image', help='Input image file')
    parser.add_argument('-o', '--output', help='Output text file')
    parser.add_argument('-l', '--lang', default='vie+eng', help='Language (default: vie+eng)')
    parser.add_argument('--no-preprocess', action='store_true', help='Skip preprocessing')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    try:
        text = extract_text(
            args.image,
            lang=args.lang,
            preprocess=not args.no_preprocess
        )
        
        if args.json:
            import json
            print(json.dumps({'text': text, 'image': args.image, 'lang': args.lang}, ensure_ascii=False, indent=2))
        else:
            print(text)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### Usage

```bash
# Basic OCR
python ocr_tool.py document.png

# Vietnamese OCR
python ocr_tool.py hoadon.png -l vie

# With preprocessing (default)
python ocr_tool.py image.png -o output.txt

# Skip preprocessing
python ocr_tool.py image.png --no-preprocess

# JSON output
python ocr_tool.py image.png --json
```

## Configuration

### tesseract.conf

```conf
# Tesseract configuration
tessedit_pageseg_mode 3
tessedit_ocr_engine_mode 3
load_system_dawg 1
load_freq_dawg 1
```

### Supported PSM Modes

| Mode | Description |
|------|-------------|
| 0 | Orientation and script detection (OSD) only |
| 1 | Automatic page segmentation with OSD |
| 3 | Fully automatic page segmentation, no OSD |
| 4 | Assume uniform block of text |
| 5 | Assume uniform block of text |
| 6 | Assume uniform block of text |
| 7 | Treat the image as a single text line |
| 8 | Treat the image as a single word |
| 9 | Treat the image as a single word in a circle |
| 10 | Treat the image as a single character |
| 11 | Sparse text in no particular order |
| 12 | Sparse text with OSD |
| 13 | Raw line with OSD |

## Error Handling

```python
def safe_ocr(image_path, lang='vie+eng'):
    """OCR with error handling"""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang=lang)
        return {'success': True, 'text': text}
    except FileNotFoundError:
        return {'success': False, 'error': 'File not found'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

## Related OSS-DocumentScanner Features

Dựa trên [OSS-DocumentScanner](https://github.com/ossappscollective/OSS-DocumentScanner):

### Document Scanning Pipeline

```
1. Image Capture → 2. Edge Detection → 3. Perspective Transform → 4. Enhancement → 5. OCR
```

### Supported Features

- Auto edge detection for document boundaries
- Perspective correction
- Automatic rotation
- Image enhancement (contrast, brightness, sharpness)
- Multiple output formats (PDF, PNG, TXT)
- Multi-language OCR support

## Notes

- Tesseract v5+ khuyến nghị cho performance tốt hơn
- Vietnamese OCR cần training data `vie` được cài đặt
- Preprocessing cải thiện accuracy đáng kể (20-40%)
- Sparse mode (PSM 11) tốt cho mixed content (text + diagrams)
- Nên resize ảnh về ~3000px max dimension trước OCR

## Installation

### Auto-Install (Recommended)

```bash
# Sử dụng skill-installer
python .cursor/scripts/skill-installer.py install document-ocr

# Hoặc PowerShell
. .cursor/scripts/skill-installer.ps1 -Command install -SkillName document-ocr
```

### Manual Install

```bash
# Tesseract OCR Engine (Windows)
# Download từ: https://github.com/UB-Mannheim/tesseract/releases
# Install và thêm vào PATH

# Python packages
pip install pytesseract pillow opencv-python

# Hoặc conda
conda install -c conda-forge tesseract pillow opencv
```

### Verify Installation

```bash
# Check Tesseract
tesseract --version

# Check language data
tesseract --list-langs

# Should show: vie, eng, osd
```

## Links

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Tesseract.js](https://github.com/naptha/tesseract.js)
- [OSS-DocumentScanner](https://github.com/ossappscollective/OSS-DocumentScanner)
- [Tesseract Training Data](https://github.com/tesseract-ocr/tessdata)
- [Python pytesseract](https://pypi.org/project/pytesseract/)
