# Command: /scrape-image - Screenshot/Image OCR Extraction

## Mô tả
Trích xuất text từ screenshots, diagrams, và images sử dụng Tesseract OCR để tăng khả năng đọc hiểu khi vibe coding.

## Trigger Keywords
- `/scrape-image` - Bắt đầu OCR
- `/ocr-image` - OCR từ image
- `/screenshot-text` - Extract text from screenshot
- `/extract-text` - Trích xuất text từ image
- `/image-to-text` - Image to text conversion

## Supported Formats

| Format | Extension | Support |
|--------|----------|---------|
| PNG | `.png` | Full |
| JPEG | `.jpg`, `.jpeg` | Full |
| TIFF | `.tiff` | Full |
| BMP | `.bmp` | Full |
| WebP | `.webp` | Full |
| PDF (scanned) | `.pdf` | Via image conversion |

## Usage Examples

### Basic OCR

```
/scrape-image screenshot.png
/scrape-image ui-design.png
```

### Vietnamese Document

```
/scrape-image hoadon.png -l vie
/scrape-image document.jpg -l vie+eng -o text.txt
```

### JSON Output

```
/scrape-image screenshot.png --json
```

### Different Preprocessing

```
/scrape-image receipt.png --preprocessor opencv
/scrape-image low-quality.png --preprocessor pillow
```

## Language Options

| Code | Language | Use Case |
|------|----------|----------|
| `vie` | Vietnamese | Vietnamese documents |
| `eng` | English | English documents |
| `vie+eng` | Vietnamese + English | Mixed documents |
| `chi_sim` | Simplified Chinese | Chinese text |
| `jpn` | Japanese | Japanese text |
| `kor` | Korean | Korean text |

## Command Prompt

```
# Task: Image Text Extraction (OCR)

## Image to Process:
{image_path}

## Language:
{language}

## Preprocessing:
{preprocessor}

## Workflow:

### 1. Check Dependencies
- Tesseract OCR installed
- pytesseract Python package installed
- PIL/Pillow available

### 2. Image Preprocessing
If image is low quality:
- Convert to grayscale
- Increase contrast (1.5x)
- Sharpen image
- Remove noise
- Auto-levels

### 3. OCR Extraction
- Use Tesseract with specified language
- Apply PSM mode (auto/block/sparse)
- Extract text with confidence

### 4. Post-Processing
- Clean whitespace
- Validate extracted text
- Return structured result

## Output Format:
{
  "success": true/false,
  "text": "extracted text",
  "confidence": 85.5,
  "language": "vie+eng",
  "word_count": 150
}

## Deliverables:
- Extracted text content
- Confidence score
- Word count
- Processing metadata
```

## Integration Points

### With Web Scrape
```
/scrape <url> sdk,api
/scrape-image screenshot.png -l eng
```

### With Design Review
```
/scrape-image mockup.png
# Analyze extracted text for UI elements
```

### With Document Processing
```
/scrape-image invoice.pdf
# Extract text for data entry
```

## Related
- [[../skills/document-ocr]] - Document OCR Skill
- [[../scripts/ocr_tool]] - OCR Python Tool
- [[../skills/visual-explainer]] - Visual Analysis Skill
