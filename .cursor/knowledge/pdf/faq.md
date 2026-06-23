---
title: "PDF FAQ - Câu Hỏi Thường Gặp Về PDF"
description: "Comprehensive FAQ covering frequently asked questions about PDF generation, optimization, security, accessibility, and library selection with expert answers"
tags: ["pdf", "faq", "troubleshooting", "questions", "cursor-enterprise-framework"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# PDF FAQ - Câu Hỏi Thường Gặp Về PDF

## Overview

Tài liệu này tổng hợp các câu hỏi thường gặp về PDF processing và generation, được phân loại theo topics và answered bằng expert guidance. Mỗi câu hỏi được trả lời với practical details, code examples khi appropriate, và references đến relevant documentation.

Những câu hỏi này được compile từ real-world usage patterns và common issues developers gặp phải khi working with PDF systems. Answers được provided by considering production requirements và best practices từ enterprise perspective.

## Purpose

FAQ này phục vụ như một quick reference cho developers gặp specific issues hoặc có questions about PDF implementation. Nó cũng hữu ích cho architects evaluating PDF solutions và managers understanding PDF-related decisions.

## General Questions

### Q1: What is the difference between PDF/A and PDF/UA?

**Answer**:

PDF/A (ISO 19005) và PDF/UA (ISO 14289) là hai standards phục vụ different purposes:

**PDF/A (Archival)**:

- Designed cho long-term document preservation
- Ensures documents remain readable over decades
- Prohibits features that might become unreadable:
  - External font references (fonts must be embedded)
  - Audio/video content
  - Executable content (JavaScript must be restricted)
  - Encryption (unless key stored with document)
  - Transparency (in PDF/A-1)
- Three conformance levels: a (accessible), u (Unicode text extraction), b (basic)
- Ideal for: Legal documents, government records, academic archives

**PDF/UA (Universal Accessibility)**:

- Designed cho users với disabilities
- Ensures documents are accessible via assistive technologies
- Requirements include:
  - Proper document structure (tags)
  - Alternative text for all images
  - Logical reading order
  - Document title
  - Language specification
- Ideal for: Government publications, educational materials, accessibility compliance

**Key Difference**: PDF/A ensures document longevity, PDF/UA ensures accessibility. A document can be both PDF/A and PDF/UA compliant.

```javascript
// Creating PDF/A-1a compliant document
const pdfDoc = await PDFDocument.create();
pdfDoc.setTitle('Important Document');
pdfDoc.setLang('en-US');

// Embed fonts (required for PDF/A)
const font = await pdfDoc.embedFont(StandardFonts.Helvetica);

// Verify PDF/A compliance (after generation)
// Use preflight tools to validate
```

### Q2: Why are my generated PDFs so large?

**Answer**:

Large PDF files usually result from one or more of these causes:

**1. Uncompressed Images (Most Common)**:

Images are typically 70-90% of PDF file size.

```javascript
// Problem: High-resolution images embedded as-is
// Solution: Compress images before embedding
const sharp = require('sharp');

// Bad: Embedding raw 4K image (5MB+)
page.drawImage(highResImage);

// Good: Compress first
const optimized = await sharp(imageBuffer)
  .resize(1200, 1200, { fit: 'inside' })
  .jpeg({ quality: 85, progressive: true })
  .toBuffer();
page.drawImage(optimized);
```

**2. Full Font Embedding**:

A single font file can be 2-5MB.

```javascript
// Problem: Embedding entire font file
// Solution: Subset fonts - only embed used characters
const usedChars = 'Hello World 1234567890'.split('');
const subsetFont = font.subset(usedChars);
// Result: 20-50KB instead of 5MB
```

**3. No Compression Applied**:

PDF streams can be compressed but might not be by default.

```javascript
// Enable compression when saving
const pdfBytes = await pdfDoc.save({
  useObjectStreams: true  // Compress objects
});
```

**4. Debug Information**:

Development settings might include unnecessary data.

```javascript
// Ensure production settings
await page.pdf({
  printBackground: true,  // Don't include debug layers
  // ...
});
```

### Q3: How do I handle Unicode/text encoding in PDFs?

**Answer**:

Unicode handling in PDFs requires careful attention to encoding:

**1. Use Unicode-Compatible Fonts**:

```javascript
// Bad: Standard fonts may not support Unicode
const font = await pdfDoc.embedFont(StandardFonts.Helvetica);
// Helvetica only supports Latin-1

// Good: Use Unicode-aware fonts
const font = await pdfDoc.embedFont(
  await fetch('https://fonts.gstatic.com/s/notosans/v36/o-0IIpQlx3QUlC5A4pnrV6B.woff2')
);
```

**2. For Vietnamese with diacritics**:

```javascript
// Vietnamese requires font with combining diacritics support
const vietnameseText = 'Nguyễn Văn Minh - Đường ABC, TP.HCM';

const font = await pdfDoc.embedFont(
  await fetch('NotoSans-VariableFont_wght.ttf')
);

page.drawText(vietnameseText, {
  x: 50,
  y: 700,
  size: 12,
  font: font
});
```

**3. For CJK Languages**:

```javascript
// Chinese, Japanese, Korean require specific fonts
// Use Adobe's CJK fonts or Noto CJK
const cjkFont = await pdfDoc.embedFont(
  await fetch('NotoSansCJKsc-Variable.ttf')
);

page.drawText('中文测试 - 日本語テスト - 한국어 테스트', {
  font: cjkFont,
  // ...
});
```

**4. Set Document Language**:

```javascript
pdfDoc.setLang('vi-VN'); // For Vietnamese documents
```

### Q4: What is the best approach for generating PDFs from HTML?

**Answer**:

The best approach depends on your requirements:

**Option 1: Puppeteer (Best for Complex CSS)**:

```javascript
const puppeteer = require('puppeteer');

async function htmlToPDF(html) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.setContent(html, { waitUntil: 'networkidle0' });
  
  const pdf = await page.pdf({
    format: 'A4',
    printBackground: true,
    margin: { top: '20px', bottom: '20px' }
  });
  
  await browser.close();
  return Buffer.from(pdf);
}
```

**Best for**: Complex layouts, CSS Grid/Flexbox, @media print styles

**Option 2: Playwright (Best for Cross-Browser)**:

```javascript
const { chromium } = require('playwright');

async function htmlToPDF(html) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.setContent(html);
  
  const pdf = await page.pdf({
    format: 'A4',
    printBackground: true
  });
  
  await browser.close();
  return Buffer.from(pdf);
}
```

**Best for**: Cross-browser consistency, modern web features

**Option 3: WeasyPrint (Best for Python/Server)**:

```python
from weasyprint import HTML, CSS

def html_to_pdf(html_content):
    html = HTML(string=html_content)
    css = CSS('@page { size: A4; margin: 20px; }')
    return html.write_pdf(stylesheets=[css])
```

**Best for**: Python environments, CSS Paged Media support

### Q5: How do I create a PDF with digital signatures?

**Answer**:

Digital signatures require PKI infrastructure and careful implementation:

**Simple Approach (Using pdf-lib)**:

```javascript
const { PDFDocument, PDFName, PDFHexString } = require('pdf-lib');

async function signPDF(pdfBuffer, options) {
  const doc = await PDFDocument.load(pdfBuffer);
  
  // Create signature field
  const page = doc.getPage(0);
  const signature = doc.addSignature(page, {
    widgetRect: [400, 700, 550, 750]  // Signature box position
  });
  
  // For actual production use, integrate with a signing service:
  // - DocuSign, Adobe Sign, or HelloSign APIs
  // - Or use OpenSSL/node-forge for custom implementation
  
  const signatureBytes = await createPKCS7Signature(
    doc.getBytesToSign(),
    options.certificate,
    options.privateKey
  );
  
  signature.setSignature(signatureBytes);
  
  return await doc.save();
}

async function createPKCS7Signature(content, cert, privateKey) {
  const forge = require('node-forge');
  
  const p7 = forge.pkcs7.createSignedData();
  p7.content = forge.util.createBuffer(content);
  
  // Add certificate
  const certificate = forge.pki.certificateFromPem(cert);
  p7.addCertificate(certificate);
  
  // Sign
  const privateKeyObj = forge.pki.privateKeyFromPem(privateKey);
  p7.sign({ detached: true });
  
  // Return DER encoded signature
  return forge.asn1.toDer(p7.toAsn1()).getBytes();
}
```

**Production Considerations**:

1. Use a certified signing service for legal documents
2. Implement timestamp authority (TSA) for long-term signatures
3. Store certificates securely (HSM/KMS)
4. Maintain audit trail

**Third-Party Services**:

```javascript
// Using DocuSign API
const docusign = require('docusign-esign');

async function signWithDocuSign(pdfBuffer) {
  const apiClient = new docusign.ApiClient();
  apiClient.setBasePath('https://demo.docusign.net/restapi');
  apiClient.addDefaultHeader(
    'Authorization', 
    `Bearer ${accessToken}`
  );
  
  // Upload document
  const documentsApi = new docusign.DocumentsApi(apiClient);
  const result = await documentsApi.listSigningGroups(accountId);
  
  // Create envelope and send for signing
  // ...
}
```

## Performance Questions

### Q6: How can I speed up PDF generation?

**Answer**:

Performance optimization involves multiple strategies:

**1. Browser Reuse (Critical for Puppeteer/Playwright)**:

```javascript
// Bad: Launch browser for each request
async function generatePDF(html) {
  const browser = await puppeteer.launch();  // Slow!
  // ...
  await browser.close();
}

// Good: Reuse browser instance
class PDFGenerator {
  constructor() {
    this.browser = null;
  }
  
  async initialize() {
    if (!this.browser) {
      this.browser = await puppeteer.launch();
    }
    return this.browser;
  }
  
  async generate(html) {
    const browser = await this.initialize();
    const page = await browser.newPage();
    try {
      // ...
    } finally {
      await page.close();  // Keep browser open
    }
  }
}
```

**2. Pre-render Templates**:

```javascript
// Pre-compile Handlebars templates
const Handlebars = require('handlebars');
const templateCache = new Map();

function getTemplate(name) {
  if (!templateCache.has(name)) {
    const source = fs.readFileSync(`./templates/${name}.hbs`, 'utf8');
    templateCache.set(name, Handlebars.compile(source));
  }
  return templateCache.get(name);
}
```

**3. Parallel Generation**:

```javascript
// Generate multiple PDFs in parallel
async function generateBatch(requests) {
  const results = await Promise.all(
    requests.map(req => generatePDF(req.html, req.options))
  );
  return results;
}
```

**4. Image Optimization Pipeline**:

```javascript
// Pre-optimize images before PDF generation
const sharp = require('sharp');

async function preProcessImages(images) {
  return Promise.all(
    images.map(img => 
      sharp(img.buffer)
        .resize(1200, 1200, { fit: 'inside' })
        .jpeg({ quality: 85 })
        .toBuffer()
    )
  );
}
```

**5. Caching**:

```javascript
// Cache generated PDFs
const cache = new Map();

async function generateCachedPDF(data, key) {
  if (cache.has(key)) {
    return cache.get(key);
  }
  
  const pdf = await generatePDF(data);
  cache.set(key, pdf);
  
  return pdf;
}
```

### Q7: How do I handle memory issues with large PDFs?

**Answer**:

Memory issues typically occur with Puppeteer-based solutions. Here's a systematic approach:

**1. Limit Concurrent Operations**:

```javascript
const PQueue = require('p-queue');

const queue = new PQueue({ concurrency: 2 });  // Limit parallel jobs

async function generatePDF(html) {
  return queue.add(async () => {
    // Process one at a time
  });
}
```

**2. Memory Limits for Puppeteer**:

```javascript
await puppeteer.launch({
  args: [
    '--max-old-space-size=512',  // Limit to 512MB
    '--disable-dev-shm-usage',
    '--disable-accelerated-2d-canvas',
    '--no-sandbox'
  ]
});
```

**3. Stream Processing for Large Files**:

```javascript
// Process PDFs in chunks instead of loading entire file
async function processLargePDF(inputPath) {
  // Read in chunks
  const readStream = fs.createReadStream(inputPath, {
    highWaterMark: 1024 * 1024  // 1MB chunks
  });
  
  // Process chunk by chunk
  let position = 0;
  for await (const chunk of readStream) {
    await processChunk(chunk, position);
    position += chunk.length;
  }
}
```

**4. Garbage Collection Hints**:

```javascript
// Periodically suggest garbage collection
async function generateManyPDFs(htmlList) {
  for (let i = 0; i < htmlList.length; i++) {
    await generatePDF(htmlList[i]);
    
    // After every 10 documents, hint GC
    if (i % 10 === 0) {
      global.gc?.();
    }
  }
}
```

**5. Use pdf-lib for Manipulation**:

```javascript
// pdf-lib is much lighter than Puppeteer for manipulation
const { PDFDocument } = require('pdf-lib');

async function manipulatePDF(buffer) {
  const doc = await PDFDocument.load(buffer);
  // Memory usage: 10-50MB vs 200-500MB for Puppeteer
  // ...
  return await doc.save();
}
```

### Q8: How do I implement PDF caching effectively?

**Answer**:

A multi-level caching strategy works best:

**Level 1: In-Memory Cache (Fastest)**:

```javascript
const LRU = require('lru-cache');

const memoryCache = new LRU({
  max: 100,  // Max 100 PDFs
  ttl: 1000 * 60 * 60  // 1 hour
});

async function getCachedPDF(dataHash) {
  return memoryCache.get(dataHash);
}

async function setCachedPDF(dataHash, pdfBuffer) {
  memoryCache.set(dataHash, pdfBuffer);
}
```

**Level 2: Redis Cache (Distributed)**:

```javascript
const Redis = require('ioredis');

async function getFromRedis(cacheKey) {
  const redis = new Redis(process.env.REDIS_URL);
  
  const metadata = await redis.hgetall(cacheKey);
  if (!metadata.storageKey) {
    return null;
  }
  
  // Get actual PDF from storage
  const pdfBuffer = await storage.get(metadata.storageKey);
  return pdfBuffer;
}

async function saveToRedis(cacheKey, pdfBuffer) {
  const storageKey = `pdfs/${cacheKey}.pdf`;
  
  // Save PDF to storage
  await storage.put(storageKey, pdfBuffer);
  
  // Save metadata to Redis
  await redis.hset(cacheKey, {
    storageKey,
    size: pdfBuffer.length,
    createdAt: Date.now()
  });
  
  await redis.expire(cacheKey, 86400);  // 24 hours
}
```

**Level 3: CDN Cache (Edge)**:

```javascript
// Set appropriate cache headers
app.get('/api/pdf/:id', async (req, res) => {
  const pdf = await getPDF(req.params.id);
  
  // Cache at CDN for 1 hour, browser for 1 day
  res.setHeader('Cache-Control', 'public, max-age=86400, s-maxage=3600');
  res.setHeader('ETag', generateETag(pdf));
  
  res.send(pdf);
});
```

**Cache Invalidation**:

```javascript
// Invalidate on data change
async function onDataUpdate(dataId) {
  const cacheKeys = await redis.keys(`pdf:*:${dataId}*`);
  
  for (const key of cacheKeys) {
    await redis.del(key);
  }
}
```

## Security Questions

### Q9: How do I prevent path traversal in PDF file operations?

**Answer**:

Path traversal allows attackers to access files outside intended directories. Here's how to prevent it:

**1. Whitelist Approach (Recommended)**:

```javascript
const path = require('path');
const fs = require('fs').promises;

const ALLOWED_DIRS = ['/var/app/pdfs', '/var/app/templates'];
const BASE_DIR = '/var/app';

function safePath(requestedPath, baseDir = BASE_DIR) {
  // Resolve to absolute path
  const absolutePath = path.resolve(baseDir, requestedPath);
  
  // Check it's within allowed directories
  const isAllowed = ALLOWED_DIRS.some(dir => 
    absolutePath.startsWith(path.resolve(dir) + path.sep)
  );
  
  if (!isAllowed) {
    throw new Error('Path outside allowed directory');
  }
  
  return absolutePath;
}

async function readTemplate(templateName) {
  const safeFilePath = safePath(templateName, '/var/app/templates');
  
  // Verify file exists
  await fs.access(safeFilePath);
  
  return await fs.readFile(safeFilePath, 'utf8');
}
```

**2. Validate Against Filename Patterns**:

```javascript
function sanitizeFilename(filename) {
  // Remove any path components
  const basename = path.basename(filename);
  
  // Remove null bytes and control characters
  const sanitized = basename.replace(/[\x00-\x1f\x7f]/g, '');
  
  // Remove potentially dangerous characters
  const safe = sanitized.replace(/[<>:"|?*\x5c]/g, '_');
  
  // Check for path traversal patterns
  if (safe.includes('..') || safe.includes('/') || safe.includes('\\')) {
    throw new Error('Invalid filename');
  }
  
  return safe;
}
```

**3. Use Content-Disposition for Downloads**:

```javascript
app.get('/api/download', async (req, res) => {
  const { filename } = req.query;
  
  try {
    const safeName = sanitizeFilename(filename);
    const filePath = safePath(safeName, '/var/app/pdfs');
    
    // Set Content-Disposition to prevent injection
    res.setHeader(
      'Content-Disposition', 
      `attachment; filename="${safeName}"`
    );
    
    res.sendFile(filePath);
  } catch (error) {
    res.status(403).json({ error: 'Access denied' });
  }
});
```

### Q10: How do I securely handle sensitive data in PDFs?

**Answer**:

Sensitive data requires multiple layers of protection:

**1. Encryption at Rest**:

```javascript
const { PDFDocument } = require('pdf-lib');

async function encryptPDF(pdfBuffer, passwords) {
  const doc = await PDFDocument.load(pdfBuffer);
  
  doc.encrypt({
    userPassword: passwords.userPassword,
    ownerPassword: passwords.ownerPassword,
    permissions: {
      printing: 'highResolution',
      modifying: false,
      copying: false,
      annotating: false,
      fillingForms: false,
      contentAccessibility: true,
      documentAssembly: false
    }
  });
  
  return await doc.save();
}
```

**2. Redact Sensitive Information Before Generation**:

```javascript
function redactSensitiveData(data) {
  const sensitiveFields = ['ssn', 'creditCard', 'password'];
  
  const redacted = { ...data };
  for (const field of sensitiveFields) {
    if (redacted[field]) {
      redacted[field] = '***REDACTED***';
    }
  }
  
  return redacted;
}

async function generateSafePDF(data) {
  const safeData = redactSensitiveData(data);
  return await generatePDF(safeData);
}
```

**3. Secure Storage and Transmission**:

```javascript
// HTTPS only
app.use((req, res, next) => {
  if (!req.secure && process.env.NODE_ENV === 'production') {
    return res.redirect(`https://${req.hostname}${req.url}`);
  }
  next();
});

// Don't log sensitive data
const safeLogger = {
  info: (message, data) => {
    const sanitized = sanitizeForLogging(data);
    console.log(message, sanitized);
  }
};

function sanitizeForLogging(data) {
  const sensitive = ['password', 'token', 'secret', 'ssn'];
  return Object.fromEntries(
    Object.entries(data).map(([k, v]) => [
      k,
      sensitive.some(s => k.toLowerCase().includes(s)) ? '[REDACTED]' : v
    ])
  );
}
```

**4. Watermark with User Info**:

```javascript
async function addSecurityWatermark(pdfBuffer, userInfo) {
  const doc = await PDFDocument.load(pdfBuffer);
  const font = await doc.embedFont(StandardFonts.Helvetica);
  
  for (const page of doc.getPages()) {
    const { width, height } = page.getSize();
    
    page.drawText(`Downloaded by: ${userInfo.email}`, {
      x: 50,
      y: height - 50,
      size: 8,
      font: font,
      color: rgb(0.7, 0.7, 0.7),
      opacity: 0.3
    });
    
    page.drawText(new Date().toISOString(), {
      x: width - 150,
      y: height - 50,
      size: 8,
      font: font,
      color: rgb(0.7, 0.7, 0.7),
      opacity: 0.3
    });
  }
  
  return await doc.save();
}
```

## Accessibility Questions

### Q11: How do I make PDFs accessible (PDF/UA compliant)?

**Answer**:

Accessibility requires proper structure and metadata:

**1. Set Document Language**:

```javascript
const pdfDoc = await PDFDocument.create();
pdfDoc.setLang('en-US');  // Or 'vi-VN' for Vietnamese
```

**2. Create Tagged PDF Structure**:

```javascript
async function createAccessiblePDF(content) {
  const pdfDoc = await PDFDocument.create();
  
  // Enable tagging
  pdfDoc.catalog.set(
    PDFName.of('MarkInfo'),
    pdfDoc.context.obj({ Marked: true })
  );
  
  // Create structure tree root
  const structTreeRoot = pdfDoc.context.obj({
    Type: 'StructTreeRoot'
  });
  pdfDoc.catalog.set(PDFName.of('StructTreeRoot'), structTreeRoot);
  
  // Add pages and mark content
  const page = pdfDoc.addPage([595, 842]);
  
  // Mark heading
  const headingStruct = pdfDoc.context.obj({
    Type: 'StructElem',
    S: 'H1',
    Pg: page.node,
    K: []  // Kids reference content
  });
  
  // Continue for all content types...
  
  return await pdfDoc.save();
}
```

**3. Add Alternative Text for Images**:

```javascript
// For images, add alt text in structure
const imageXObject = await pdfDoc.embedPNG(imageBuffer);

page.drawImage(imageXObject, {
  x: 50,
  y: 600,
  width: 200,
  height: 100
});

// Mark in structure tree
const figureStruct = pdfDoc.context.obj({
  Type: 'StructElem',
  S: 'Figure',
  Alt: PDFString.of('Company logo in blue'),  // Alt text
  Pg: page.node
});
```

**4. Ensure Proper Reading Order**:

```javascript
// Reading order follows structure tree
// Parent-child relationships determine reading sequence

const page = pdfDoc.addPage([595, 842]);

// Content order in structure tree = reading order
const structureOrder = [
  { type: 'H1', content: 'Report Title' },
  { type: 'P', content: 'Introduction paragraph' },
  { type: 'H2', content: 'Section 1' },
  { type: 'P', content: 'Section 1 content' }
];
```

### Q12: How do I verify PDF accessibility?

**Answer**:

Use automated tools and manual testing:

**Automated Tools**:

```bash
# PAC (PDF Accessibility Checker)
# https://www.access-for-all.ch/en/pdf-lab/pac-download.html

# Preflight in Adobe Acrobat
# Run accessibility check

# PDF Accessibility Checker (Java)
pdfa-online-validator --accessible document.pdf
```

**Manual Testing**:

```javascript
// Extract text and verify reading order
const { PDFDocument } = require('pdf-lib');

async function verifyReadingOrder(pdfBuffer) {
  const doc = await PDFDocument.load(pdfBuffer);
  
  // Get page content
  const page = doc.getPage(0);
  const content = await page.getTextContent();
  
  // Verify logical sequence
  const readingOrder = content.items.map(item => ({
    text: item.str,
    position: item.transform
  }));
  
  // Check positions are logical (top to bottom, left to right)
  const sortedByPosition = readingOrder.sort((a, b) => {
    // Sort by y position (descending for top-to-bottom)
    const yDiff = b.position[5] - a.position[5];
    if (Math.abs(yDiff) > 5) return yDiff;
    // Then by x position (ascending for left-to-right)
    return a.position[4] - b.position[4];
  });
  
  console.log('Reading order:', sortedByPosition.map(i => i.text).join(' '));
}
```

**Screen Reader Testing**:

```bash
# Test with NVDA (Windows)
# 1. Open PDF in Adobe Reader
# 2. Enable NVDA
# 3. Navigate through document
# 4. Verify all content is read in correct order
```

## Library-Specific Questions

### Q13: When should I use pdf-lib vs Puppeteer?

**Answer**:

Choose based on your primary use case:

**Use pdf-lib when**:

```javascript
// 1. PDF manipulation (watermarks, merging, splitting)
const { PDFDocument } = require('pdf-lib');

async function addWatermark(buffer) {
  const doc = await PDFDocument.load(buffer);
  // Add watermark...
  return await doc.save();
}

// 2. Programmatic PDF creation (no HTML/CSS needed)
async function createInvoice(invoiceData) {
  const doc = await PDFDocument.create();
  const page = doc.addPage();
  
  // Draw elements at exact positions
  page.drawText(invoiceData.title, { x: 50, y: 700 });
  page.drawTable(invoiceData.items, { x: 50, y: 600 });
  // ...
  
  return await doc.save();
}

// 3. Form filling
async function fillForm(templateBuffer, formData) {
  const doc = await PDFDocument.load(templateBuffer);
  const form = doc.getForm();
  
  form.getTextField('name').setText(formData.name);
  form.getCheckBox('agree').check();
  
  return await doc.save();
}
```

**Advantages of pdf-lib**:

- No browser overhead (10-50MB memory vs 200-500MB for Puppeteer)
- Much faster (50-200ms vs 1-5 seconds)
- Pure JavaScript, no native dependencies
- Better for manipulation tasks

**Use Puppeteer when**:

```javascript
// 1. Converting HTML/CSS to PDF
async function htmlToPDF(html) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.setContent(html);
  const pdf = await page.pdf();
  
  await browser.close();
  return Buffer.from(pdf);
}

// 2. Web-style documents with complex CSS
const html = `
  <style>
    .invoice { display: grid; grid-template-columns: 1fr 2fr; }
    .table { border-collapse: collapse; width: 100%; }
    /* Complex CSS Grid, Flexbox, etc. */
  </style>
  <div class="invoice">
    <!-- Complex layout -->
  </div>
`;

await page.setContent(html);
await page.pdf({ format: 'A4', printBackground: true });
```

**Advantages of Puppeteer**:

- Full CSS support (Grid, Flexbox, @media print)
- JavaScript execution (dynamic content)
- Screenshots and PDF in one tool
- Headless Chrome rendering

### Q14: How do I migrate from jsPDF to pdf-lib?

**Answer**:

jsPDF and pdf-lib have different APIs. Here's a migration guide:

**Basic Text**:

```javascript
// jsPDF
const doc = new jsPDF();
doc.setFontSize(16);
doc.text('Hello World', 10, 10);

// pdf-lib equivalent
const { PDFDocument, StandardFonts } = require('pdf-lib');
const doc = await PDFDocument.create();
const page = doc.addPage([210, 297]);  // A4 in mm
const font = await doc.embedFont(StandardFonts.Helvetica);

page.drawText('Hello World', {
  x: 10,
  y: 287,  // pdf-lib uses bottom-left origin
  size: 16,
  font: font
});
```

**Images**:

```javascript
// jsPDF
doc.addImage(imageData, 'JPEG', 10, 10, 50, 50);

// pdf-lib
const image = await doc.embedJpg(imageData);
const { width, height } = image.scale(0.5);  // Scale to 50%

page.drawImage(image, {
  x: 10,
  y: 287 - 50,  // Adjust for bottom-left origin
  width: width,
  height: height
});
```

**Tables (jsPDF has plugin, pdf-lib is manual)**:

```javascript
// jsPDF (with jsPDF-AutoTable plugin)
doc.autoTable({
  head: [['Name', 'Age']],
  body: [['John', '30'], ['Jane', '25']]
});

// pdf-lib (manual implementation)
const tableData = [
  ['Name', 'Age'],
  ['John', '30'],
  ['Jane', '25']
];

const startY = 700;
const rowHeight = 20;
const colWidths = [100, 50];

tableData.forEach((row, rowIndex) => {
  let x = 50;
  row.forEach((cell, colIndex) => {
    page.drawText(cell, {
      x: x,
      y: startY - (rowIndex * rowHeight),
      font: font,
      size: 10
    });
    x += colWidths[colIndex];
  });
});
```

### Q15: How do I handle PDF generation errors gracefully?

**Answer**:

Implement comprehensive error handling:

```javascript
class PDFGenerationError extends Error {
  constructor(message, code, details = {}) {
    super(message);
    this.name = 'PDFGenerationError';
    this.code = code;
    this.details = details;
  }
}

async function generatePDFSafely(html, options) {
  try {
    // Validate input
    if (!html || typeof html !== 'string') {
      throw new PDFGenerationError(
        'Invalid HTML input',
        'INVALID_INPUT',
        { type: typeof html }
      );
    }
    
    // Generate with timeout
    const result = await Promise.race([
      generatePDF(html, options),
      new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Generation timeout')), 30000)
      )
    ]);
    
    // Validate output
    if (!result || result.length === 0) {
      throw new PDFGenerationError(
        'Empty PDF generated',
        'EMPTY_OUTPUT'
      );
    }
    
    return result;
    
  } catch (error) {
    if (error instanceof PDFGenerationError) {
      throw error;
    }
    
    // Handle specific error types
    if (error.message.includes('network')) {
      throw new PDFGenerationError(
        'Network error during generation',
        'NETWORK_ERROR',
        { originalError: error.message }
      );
    }
    
    if (error.message.includes('memory')) {
      throw new PDFGenerationError(
        'Memory limit exceeded',
        'MEMORY_ERROR'
      );
    }
    
    // Generic error
    throw new PDFGenerationError(
      'PDF generation failed',
      'GENERATION_ERROR',
      { originalError: error.message }
    );
  }
}

// Usage with proper error handling
app.post('/api/generate-pdf', async (req, res) => {
  try {
    const pdf = await generatePDFSafely(req.body.html, req.body.options);
    res.setHeader('Content-Type', 'application/pdf');
    res.send(pdf);
  } catch (error) {
    logger.error('PDF generation failed', {
      code: error.code,
      details: error.details
    });
    
    res.status(500).json({
      error: 'PDF generation failed',
      code: error.code,
      message: error.message
    });
  }
});
```

## Integration Questions

### Q16: How do I integrate PDF generation with React/Next.js?

**Answer**:

Server-side generation is recommended for production:

**Next.js API Route**:

```javascript
// pages/api/generate-pdf.js
import formidable from 'formidable';
import { generatePDF } from '../../lib/pdf-service';

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req, res) {
  const { fields } = await new Promise((resolve, reject) => {
    const form = formidable();
    form.parse(req, (err, fields) => {
      if (err) reject(err);
      else resolve({ fields });
    });
  });
  
  const pdf = await generatePDF({
    template: fields.template,
    data: JSON.parse(fields.data)
  });
  
  res.setHeader('Content-Type', 'application/pdf');
  res.setHeader(
    'Content-Disposition',
    `attachment; filename="${fields.filename || 'document'}.pdf"`
  );
  res.send(pdf);
}
```

**Client-Side Download (for simple cases)**:

```javascript
// components/PDFDownloadButton.jsx
import { useState } from 'react';

export default function PDFDownloadButton({ data }) {
  const [loading, setLoading] = useState(false);
  
  const downloadPDF = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/generate-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data, template: 'report' })
      });
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = 'report.pdf';
      a.click();
      
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download failed:', error);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <button onClick={downloadPDF} disabled={loading}>
      {loading ? 'Generating...' : 'Download PDF'}
    </button>
  );
}
```

### Q17: How do I generate PDFs in a serverless environment (AWS Lambda)?

**Answer**:

Serverless requires special handling due to cold starts and limited resources:

**AWS Lambda Handler**:

```javascript
// handler.js
const { chromium } = require('chromium');
let browser = null;

async function getBrowser() {
  if (!browser) {
    browser = await chromium.launch({
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu'
      ]
    });
  }
  return browser;
}

exports.generatePDF = async (event) => {
  const { html, options } = JSON.parse(event.body);
  
  try {
    const browser = await getBrowser();
    const page = await browser.newPage();
    
    await page.setContent(html, { waitUntil: 'networkidle0' });
    
    const pdf = await page.pdf({
      format: options.format || 'A4',
      printBackground: true
    });
    
    await page.close();
    
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment; filename="document.pdf"'
      },
      body: pdf.toString('base64'),
      isBase64Encoded: true
    };
    
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
```

**Lambda Layer Setup**:

```javascript
// Include in layer's package.json
{
  "dependencies": {
    "@sparticuz/chromium": "^110.0.0"
  }
}
```

**Optimizations for Lambda**:

```javascript
// 1. Reuse browser across invocations (provisioned concurrency recommended)
// 2. Limit concurrent executions
// 3. Set appropriate memory limits
// 4. Use async generation with S3 for large files

exports.generatePDFAsync = async (event) => {
  // S3 trigger for async processing
  const { bucket, key } = event.Records[0].s3;
  const inputData = await s3.getObject({ Bucket: bucket, Key: key });
  
  const pdf = await generatePDF(inputData.Body.toString());
  
  await s3.putObject({
    Bucket: bucket,
    Key: key.replace('/input/', '/output/').replace('.html', '.pdf'),
    Body: pdf,
    ContentType: 'application/pdf'
  });
  
  return { status: 'completed' };
};
```

## Troubleshooting Questions

### Q18: Why are fonts not rendering correctly in PDFs?

**Answer**:

Font issues usually stem from embedding or encoding problems:

**Problem 1: Font Not Embedded**:

```javascript
// Check if font is embedded
// Use pdf-lib to verify
const pdfDoc = await PDFDocument.load(pdfBuffer);
const font = await pdfDoc.embedFont(customFontBuffer);
// Ensure this succeeds before using font
```

**Problem 2: Character Encoding Mismatch**:

```javascript
// Bad: Using StandardFonts with non-Latin characters
const font = await pdfDoc.embedFont(StandardFonts.Helvetica);
page.drawText('中文测试', { font });  // Will show boxes

// Good: Use Unicode font
const fontBuffer = await fetch('NotoSans-Regular.ttf');
const font = await pdfDoc.embedFont(fontBuffer);
page.drawText('中文测试', { font });  // Will render correctly
```

**Problem 3: Font Fallback Issues**:

```javascript
// Specify fallback font order
page.drawText(text, {
  font: primaryFont,
  // pdf-lib doesn't support fallback, need to handle manually
});

// Manual fallback approach
async function drawTextWithFallback(page, text, position, options) {
  const fonts = {
    latin: await doc.embedFont(latinFontBuffer),
    cjk: await doc.embedFont(cjkFontBuffer),
    arabic: await doc.embedFont(arabicFontBuffer)
  };
  
  // Draw by script segments
  const segments = segmentByScript(text);
  let x = position.x;
  
  for (const segment of segments) {
    const script = detectScript(segment);
    const font = fonts[script] || fonts.latin;
    
    page.drawText(segment, {
      x: x,
      y: position.y,
      font: font,
      size: options.size
    });
    
    x += measureTextWidth(segment, font, options.size);
  }
}
```

### Q19: Why is PDF generation slow or timing out?

**Answer**:

Common causes and solutions:

**Cause 1: Network Requests for Fonts/Images**:

```javascript
// Bad: Waiting for external resources
await page.setContent(html);
// Page waits for fonts, images from external URLs

// Good: Use local resources or embed inline
const html = `
  <html>
  <head>
    <style>
      @font-face {
        font-family: 'Custom';
        src: url('data:font/woff2;base64,${embeddedFont}') format('woff2');
      }
    </style>
  </head>
  <body>...</body>
  </html>
`;

await page.setContent(html, { waitUntil: 'domcontentloaded' });  // Not 'networkidle0'
```

**Cause 2: Browser Launch Overhead**:

```javascript
// Bad: Launch browser for each request
app.post('/pdf', async () => {
  const browser = await puppeteer.launch();  // 2-5 seconds!
  // ...
});

// Good: Singleton browser instance
let browser = null;
async function getBrowser() {
  if (!browser) {
    browser = await puppeteer.launch();
  }
  return browser;
}
```

**Cause 3: Large Image Processing**:

```javascript
// Bad: Processing images during PDF generation
await page.setContent(html);
await page.pdf();  // Images processed here - slow!

// Good: Pre-process images
const processedImages = await preProcessImages(images);
const optimizedHtml = replaceImages(html, processedImages);
await page.setContent(optimizedHtml);
await page.pdf();
```

### Q20: How do I debug PDF generation issues?

**Answer**:

Systematic debugging approach:

**1. Generate HTML First**:

```javascript
async function debugPDFGeneration(html, options) {
  // Save HTML to file for inspection
  fs.writeFileSync('/tmp/debug.html', html);
  
  // Generate PDF
  const pdf = await generatePDF(html, options);
  
  // Verify PDF structure
  const doc = await PDFDocument.load(pdf);
  console.log('Pages:', doc.getPageCount());
  console.log('Fonts:', await doc.getFontCount());
  
  return pdf;
}
```

**2. Use Puppeteer Debug Mode**:

```javascript
// Run with debug port
const browser = await puppeteer.launch({
  headless: false,  // Show browser
  devtools: true    // Enable DevTools
});

const page = await browser.newPage();
// Open http://localhost:port to debug
```

**3. Check Page Content**:

```javascript
await page.setContent(html);
const content = await page.content();
console.log('HTML content length:', content.length);

// Check for errors
const errors = await page.evaluate(() => {
  return window.__errors || [];
});
console.log('Page errors:', errors);
```

**4. Test Components Separately**:

```javascript
// Test HTML rendering
await page.setContent(html);
const screenshot = await page.screenshot();
fs.writeFileSync('/tmp/debug.png', screenshot);

// Test PDF with simplified HTML
const simpleHtml = '<html><body><p>Test</p></body></html>';
const simplePdf = await generatePDF(simpleHtml);
```

## References

- Adobe PDF Reference: https://www.adobe.com/devnet/pdf.html
- PDF.js: https://github.com/mozilla/pdf.js
- pdf-lib: https://pdf-lib.org/
- Puppeteer: https://pptr.dev/
- Playwright: https://playwright.dev/
- PDF/A Standard: https://www.iso.org/standard/38920.html
- PDF/UA Standard: https://www.pdfa.org/ua-standard/
- jsPDF Documentation: https://artskydj.github.io/jsPDF/
- Node-Forge (for signing): https://github.com/digitalbazaar/forge
