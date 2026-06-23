# PDF Architecture - Kiến Trúc PDF Processing

## Tổng quan

PDF processing bao gồm parsing, extraction, generation. Libraries: pdf.js, pdf-parse, puppeteer.

## Kiến trúc chi tiết

### 1. Parsing

```javascript
import pdf from 'pdf-parse';

const data = await pdf(buffer);
const text = data.text;
```

### 2. Extraction

- Text extraction
- Table extraction
- Image extraction
- Metadata extraction

## Kết luận

PDF processing architecture enables document automation.
