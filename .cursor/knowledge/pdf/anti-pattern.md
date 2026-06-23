---
title: "PDF Anti-Patterns - Các Mẫu Cần Tránh"
description: "Comprehensive guide to common anti-patterns in PDF generation and processing that lead to performance issues, security vulnerabilities, and poor user experience"
tags: ["pdf", "anti-patterns", "performance", "security", "best-practices", "cursor-enterprise-framework"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# PDF Anti-Patterns - Các Mẫu Cần Tránh Trong Xử Lý PDF

## Overview

Trong quá trình phát triển hệ thống xử lý PDF, có nhiều anti-patterns phổ biến mà developers thường mắc phải. Những anti-patterns này không chỉ ảnh hưởng đến hiệu suất mà còn gây ra các vấn đề về bảo mật, memory leaks, và trải nghiệm người dùng kém. Tài liệu này sẽ đi sâu vào phân tích từng anti-pattern, giải thích tại sao chúng là vấn đề, và cung cấp các giải pháp thay thế tối ưu cho production systems.

Việc nhận diện và tránh các anti-patterns này ngay từ đầu sẽ giúp tiết kiệm đáng kể thời gian debug, giảm chi phí vận hành, và đảm bảo hệ thống PDF hoạt động ổn định trong môi trường production với tải cao.

## Purpose

Mục đích của tài liệu này bao gồm việc liệt kê và giải thích chi tiết các anti-patterns phổ biến nhất trong PDF processing, cung cấp các dấu hiệu nhận biết để developers có thể phát hiện sớm các vấn đề tiềm ẩn, đưa ra giải pháp thay thế tối ưu cho từng trường hợp, và thiết lập các best practices để tránh mắc phải các lỗi tương tự trong tương lai. Thông qua việc hiểu rõ các anti-patterns này, đội ngũ phát triển có thể xây dựng hệ thống PDF vừa hiệu quả vừa bảo mật.

## Key Concepts

### 1. Anti-Pattern là gì?

Anti-pattern là một giải pháp phổ biến cho một vấn đề nhưng lại gây ra nhiều hậu quả tiêu cực hơn là lợi ích. Trong context của PDF processing, anti-patterns thường xuất hiện dưới dạng những shortcuts tạm thời tiện lợi nhưng về lâu dài sẽ trở thành technical debt khó maintain. Ví dụ điển hình là việc embedding toàn bộ font file thay vì subset fonts - giải pháp này đơn giản nhưng khiến file PDF có thể tăng từ vài KB lên hàng chục MB.

### 2. Tại sao Anti-Patterns lại nguy hiểm?

Các anti-patterns trong PDF processing có thể gây ra nhiều vấn đề nghiêm trọng bao gồm memory exhaustion khi xử lý các file lớn do không có proper streaming, security vulnerabilities như path traversal attacks do unsafe file path handling, performance degradation nghiêm trọng khi hệ thống phải xử lý nhiều PDF cùng lúc, và user experience kém do thời gian tải quá lâu hoặc file PDF quá nặng. Những vấn đề này thường không được phát hiện cho đến khi hệ thống scale lên hoặc gặp production workloads thực tế.

### 3. Root Causes phổ biến

Phần lớn các anti-patterns trong PDF processing bắt nguồn từ việc không hiểu rõ PDF specification, thiếu knowledge về performance optimization, áp lực về thời gian delivery dẫn đến shortcuts không được review kỹ, và assumption rằng "nó chạy được là được" mà không quan tâm đến scalability. Đặc biệt trong các dự án enterprise, việc ignore những vấn đề nhỏ ban đầu có thể dẫn đến technical debt khổng lồ sau này.

## Common Anti-Patterns

### Anti-Pattern #1: Embedding Full Fonts

**Mô tả**: Việc embed toàn bộ font file (thường từ 500KB đến 5MB per font) vào mỗi PDF document là một trong những anti-pattern phổ biến và gây hại nhất.

**Tại sao đây là vấn đề**:

Khi embed full fonts, mỗi PDF có thể có kích thước từ 5-20MB thay vì chỉ 50-200KB nếu dùng font subsetting. Điều này dẫn đến increased storage costs, slower download times đặc biệt quan trọng trên mobile networks, increased bandwidth costs cho CDN và hosting, và longer rendering times trong browser hoặc PDF viewer.

**Code ví dụ - Anti-Pattern**:

```javascript
// Anti-pattern: Embedding full font
async function generateReportWithFullFonts(data) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.goto('about:blank');
  
  // Anti-pattern: Full font embedding
  await page.addScriptTag({
    content: `
      @font-face {
        font-family: 'CustomFont';
        src: url('/fonts/custom-font.woff2') format('woff2');
        font-weight: normal;
        font-style: normal;
      }
      * { font-family: 'CustomFont', sans-serif; }
    `
  });
  
  // This embeds the ENTIRE font file in the PDF
  // A typical font file is 500KB-5MB
  const pdfBuffer = await page.pdf({
    path: 'report.pdf',
    format: 'A4',
    printBackground: true
  });
  
  return pdfBuffer;
}
```

**Giải pháp tối ưu - Font Subsetting**:

Font subsetting chỉ embed những glyphs thực sự được sử dụng trong document. Một font có thể chỉ còn 20-50KB sau khi subset thay vì 2-5MB full font.

```javascript
// Best practice: Font subsetting với PreloadFont
async function generateReportWithFontSubsetting(data) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // Sử dụng pre-subsubset fonts
  // Font subsetting tool như fonttools, sfntly
  await page.goto('about:blank');
  
  // Chỉ load pre-subset fonts (đã được xử lý trước)
  await page.addStyleTag({
    content: `
      @font-face {
        font-family: 'SubsetFont';
        src: url('/fonts/subset/custom-font-subset.woff2') format('woff2');
        font-weight: normal;
        font-style: normal;
        /* Chỉ chứa các glyphs cần thiết */
      }
      body { font-family: 'SubsetFont', sans-serif; }
    `
  });
  
  // Font chỉ embed những characters thực sự dùng
  const pdfBuffer = await page.pdf({
    path: 'optimized-report.pdf',
    format: 'A4',
    printBackground: true
  });
  
  return pdfBuffer;
}
```

### Anti-Pattern #2: Ignoring Image Compression

**Mô tả**: Việc không nén images trước khi embed vào PDF hoặc sử dụng wrong compression format là một anti-pattern gây ra kích thước PDF tăng đáng kể.

**Tại sao đây là vấn đề**:

Một hình ảnh 5MB có thể được nén xuống còn 200-500KB với quality loss không đáng kể. Khi không nén, PDF files trở nên quá lớn cho việc lưu trữ và truyền tải. Điều này đặc biệt nghiêm trọng khi hệ thống phải xử lý hàng nghìn documents mỗi ngày.

**Code ví dụ - Anti-Pattern**:

```javascript
// Anti-pattern: Sử dụng ảnh không nén
async function generateInvoiceWithRawImages(invoiceData) {
  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        .invoice-header { 
          background: url('/images/company-logo-4k.png') no-repeat;
          /* PNG 4K logo - thường 2-5MB */
        }
        .product-image {
          background: url('/images/products/${invoiceData.productId}.png') center;
          /* Ảnh sản phẩm full resolution */
        }
      </style>
    </head>
    <body>
      <!-- Images được embed nguyên size -->
      <div class="invoice-header"></div>
      ${invoiceData.items.map(item => `
        <div class="product-image" data-product="${item.id}"></div>
      `).join('')}
    </body>
    </html>
  `;
  
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(html);
  
  const pdfBuffer = await page.pdf();
  // Kết quả: PDF có thể 10-50MB thay vì 500KB-2MB
}
```

**Giải pháp tối ưu - Image Optimization Pipeline**:

```javascript
// Best practice: Image compression pipeline
const sharp = require('sharp');
const path = require('path');

class ImageOptimizationService {
  constructor(options = {}) {
    this.maxWidth = options.maxWidth || 1200;
    this.maxHeight = options.maxHeight || 1200;
    this.quality = options.quality || 80;
    this.format = options.format || 'webp'; // Hoặc 'jpeg' cho photos
  }
  
  async optimizeImage(inputPath, outputPath) {
    const image = sharp(inputPath);
    const metadata = await image.metadata();
    
    // Resize nếu cần
    let processor = image;
    if (metadata.width > this.maxWidth || metadata.height > this.maxHeight) {
      processor = processor.resize(this.maxWidth, this.maxHeight, {
        fit: 'inside',
        withoutEnlargement: true
      });
    }
    
    // Convert và compress
    if (this.format === 'webp') {
      processor = processor.webp({ quality: this.quality });
    } else if (this.format === 'jpeg') {
      processor = processor.jpeg({ quality: this.quality, progressive: true });
    } else {
      processor = processor.png({ compressionLevel: 9 });
    }
    
    await processor.toFile(outputPath);
    
    // Trả về stats để logging
    const optimizedMetadata = await sharp(outputPath).metadata();
    return {
      originalSize: metadata.width * metadata.height,
      optimizedSize: optimizedMetadata.width * optimizedMetadata.height,
      compressionRatio: (1 - optimizedMetadata.size / metadata.size) * 100
    };
  }
  
  async generatePDFWithOptimizedImages(invoiceData) {
    const optimizationService = new ImageOptimizationService({
      maxWidth: 800,  // Giảm cho print quality
      maxHeight: 800,
      quality: 85,
      format: 'jpeg'  // JPEG cho ảnh chụp, PNG cho graphics
    });
    
    // Pre-process tất cả images
    const optimizedImagePaths = await Promise.all(
      invoiceData.images.map(async (img) => {
        const optimizedPath = `/tmp/optimized/${path.basename(img)}`;
        await optimizationService.optimizeImage(img, optimizedPath);
        return optimizedPath;
      })
    );
    
    // Generate PDF với pre-optimized images
    const html = await this.buildHTML(invoiceData, optimizedImagePaths);
    return await this.renderToPDF(html);
  }
}
```

### Anti-Pattern #3: Generating on the Fly Without Caching

**Mô tăng**: Việc generate PDF mỗi khi được request mà không có caching layer là một anti-pattern gây ra unnecessary computation và latency cao.

**Tại sao đây là vấn đề**:

Nếu cùng một document (ví dụ: monthly report) được request 1000 lần, hệ thống sẽ generate 1000 lần thay vì 1 lần và cache lại. Điều này gây ra increased CPU usage, increased latency cho users, increased cost nếu dùng cloud services có tính phí theo computation.

**Code ví dụ - Anti-Pattern**:

```javascript
// Anti-pattern: Generate on the fly, no caching
app.get('/api/invoices/:id/pdf', async (req, res) => {
  const { id } = req.params;
  
  // Mỗi request đều generate mới - rất tốn kém
  const invoiceData = await getInvoiceData(id);
  const html = await renderInvoiceTemplate(invoiceData);
  
  // Browser rendering mất 2-5 giây MỖI LẦN
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'networkidle0' });
  const pdf = await page.pdf({ format: 'A4' });
  await browser.close();
  
  res.setHeader('Content-Type', 'application/pdf');
  res.send(pdf);
});
```

**Giải pháp tối ưu - Multi-Level Caching**:

```javascript
// Best practice: Multi-level caching
const Redis = require('ioredis');
const redis = new Redis(process.env.REDIS_URL);
const crypto = require('crypto');

class PDFCacheService {
  constructor(options = {}) {
    this.redis = redis;
    this.ttl = options.ttl || 3600 * 24; // 24 hours default
    this.s3Bucket = options.s3Bucket;
  }
  
  generateCacheKey(data, template) {
    // Tạo deterministic cache key từ data và template version
    const hash = crypto.createHash('sha256')
      .update(JSON.stringify({ data, templateVersion: template.version }))
      .digest('hex')
      .substring(0, 16);
    return `pdf:${template.name}:${hash}`;
  }
  
  async getCachedPDF(cacheKey) {
    // Level 1: Check Redis for metadata
    const metadata = await this.redis.hgetall(cacheKey);
    
    if (metadata.exists === 'true') {
      // Level 2: Get from S3/Blob storage
      const pdfBuffer = await this.getFromStorage(metadata.storageKey);
      return {
        buffer: pdfBuffer,
        cached: true,
        generatedAt: metadata.generatedAt
      };
    }
    
    return null;
  }
  
  async cachePDF(cacheKey, pdfBuffer, metadata = {}) {
    const storageKey = `pdfs/${cacheKey.replace(':', '/')}.pdf`;
    
    // Store actual PDF in blob storage
    await this.putToStorage(storageKey, pdfBuffer);
    
    // Store metadata in Redis
    await this.redis.hset(cacheKey, {
      exists: 'true',
      storageKey,
      size: pdfBuffer.length,
      generatedAt: new Date().toISOString(),
      ...metadata
    });
    
    await this.redis.expire(cacheKey, this.ttl);
  }
  
  async generateOrGetCachedPDF(data, template) {
    const cacheKey = this.generateCacheKey(data, template);
    
    // Try cache first
    const cached = await this.getCachedPDF(cacheKey);
    if (cached) {
      return cached;
    }
    
    // Generate fresh PDF
    const html = await template.render(data);
    const pdfBuffer = await renderToPDF(html);
    
    // Cache for future requests
    await this.cachePDF(cacheKey, pdfBuffer, {
      dataHash: cacheKey.split(':')[2]
    });
    
    return {
      buffer: pdfBuffer,
      cached: false,
      generatedAt: new Date().toISOString()
    };
  }
}

// Usage
app.get('/api/invoices/:id/pdf', async (req, res) => {
  const { id } = req.params;
  const invoiceData = await getInvoiceData(id);
  
  const cacheService = new PDFCacheService({
    s3Bucket: process.env.PDF_STORAGE_BUCKET
  });
  
  const result = await cacheService.generateOrGetCachedPDF(
    invoiceData,
    invoiceTemplate
  );
  
  res.setHeader('Content-Type', 'application/pdf');
  res.setHeader('X-Cache', result.cached ? 'HIT' : 'MISS');
  res.setHeader('X-Generated-At', result.generatedAt);
  res.send(result.buffer);
});
```

### Anti-Pattern #4: Unsafe File Path Handling

**Mô tả**: Việc sử dụng user input trực tiếp để construct file paths mà không validate có thể dẫn đến path traversal attacks và security vulnerabilities.

**Tại sao đây là vấn đề**:

Path traversal attack cho phép attacker truy cập arbitrary files trên server bằng cách sử dụng sequences như `../../../etc/passwd`. Điều này có thể dẫn đến information disclosure, data exfiltration, hoặc remote code execution trong một số trường hợp.

**Code ví dụ - Anti-Pattern**:

```javascript
// Anti-pattern: Unsafe file path handling
app.get('/api/download', async (req, res) => {
  const { filename } = req.query;
  
  // VULNERABLE: No path validation
  // Attacker có thể request: /api/download?filename=../../../etc/passwd
  const filePath = `/var/app/uploads/${filename}`;
  
  res.download(filePath);
});

// Anti-pattern trong PDF generation
app.post('/api/generate-pdf', async (req, res) => {
  const { template, outputName } = req.body;
  
  // VULNERABLE: Template path từ user input
  const templatePath = path.join(__dirname, 'templates', template);
  const outputPath = path.join(__dirname, 'output', outputName);
  
  // Attacker có thể overwrite arbitrary files
  const html = fs.readFileSync(templatePath, 'utf8');
  const pdf = await generatePDF(html);
  fs.writeFileSync(outputPath, pdf);
});
```

**Giải pháp tối ưu - Safe Path Handling**:

```javascript
// Best practice: Safe path handling
const path = require('path');
const fs = require('fs').promises;

class SafeFileService {
  constructor(options = {}) {
    this.allowedDirs = options.allowedDirs || [];
    this.baseDir = options.baseDir;
  }
  
  validatePath(requestedPath) {
    // Resolve và normalize path
    const resolved = path.resolve(this.baseDir, requestedPath);
    
    // Check if resolved path is within allowed directories
    const isAllowed = this.allowedDirs.some(dir => {
      const allowedPath = path.resolve(this.baseDir, dir);
      return resolved.startsWith(allowedPath + path.sep) || 
             resolved === allowedPath;
    });
    
    if (!isAllowed) {
      throw new Error('Path outside allowed directory');
    }
    
    // Additional check for path traversal patterns
    const normalized = path.normalize(requestedPath);
    if (normalized.includes('..')) {
      throw new Error('Path traversal detected');
    }
    
    return resolved;
  }
  
  sanitizeFilename(filename) {
    // Remove any path components
    const basename = path.basename(filename);
    // Remove null bytes và control characters
    const sanitized = basename.replace(/[\x00-\x1f\x7f]/g, '');
    // Remove any remaining suspicious characters
    return sanitized.replace(/[<>:"|?*]/g, '_');
  }
}

// Usage
const fileService = new SafeFileService({
  baseDir: '/var/app',
  allowedDirs: ['uploads', 'templates', 'output']
});

app.get('/api/download', async (req, res) => {
  const { filename } = req.query;
  
  try {
    const safeName = fileService.sanitizeFilename(filename);
    const safePath = fileService.validatePath(safeName);
    
    // Verify file exists
    await fs.access(safePath);
    
    res.download(safePath);
  } catch (error) {
    if (error.message.includes('outside allowed')) {
      res.status(403).json({ error: 'Access denied' });
    } else {
      res.status(404).json({ error: 'File not found' });
    }
  }
});

// Alternative: Whitelist approach
app.post('/api/generate-pdf', async (req, res) => {
  const { templateId } = req.body;
  
  // Whitelist: Chỉ cho phép predefined templates
  const ALLOWED_TEMPLATES = {
    'invoice': 'invoice-template.html',
    'report': 'report-template.html',
    'receipt': 'receipt-template.html'
  };
  
  const templateFile = ALLOWED_TEMPLATES[templateId];
  if (!templateFile) {
    return res.status(400).json({ error: 'Invalid template' });
  }
  
  const templatePath = path.join(__dirname, 'templates', templateFile);
  const html = await fs.readFile(templatePath, 'utf8');
  
  const pdf = await generatePDF(html);
  res.setHeader('Content-Type', 'application/pdf');
  res.send(pdf);
});
```

### Anti-Pattern #5: Memory Leaks with Large PDFs

**Mô tả**: Việc không properly handle large PDF files dẫn đến memory exhaustion và potential OOM (Out of Memory) crashes.

**Tại sao đây là vấn đề**:

Một PDF 100MB có thể consume gigabytes RAM khi parse nếu không xử lý đúng cách. Memory leaks accumulate over time, đặc biệt nguy hiểm trong long-running processes như Node.js servers. eventual OOM crashes affect all users của service.

**Code ví dụ - Anti-Pattern**:

```javascript
// Anti-pattern: Load entire PDF into memory
app.post('/api/process-pdf', async (req, res) => {
  const pdfBuffer = req.body.pdf; // Could be 100MB+
  
  // Anti-pattern: Entire file loaded into memory
  const pdfDoc = await PDFLib.PDFDocument.load(pdfBuffer);
  
  // Anti-pattern: Keep reference to page content
  const pages = pdfDoc.getPages();
  const allContent = pages.map(page => page.getContent());
  
  // Memory leak: buffers never released
  const processedData = processContent(allContent);
  
  res.json(processedData);
  // pdfDoc, pages, allContent vẫn còn trong memory
});

// Anti-pattern: Stream không được properly closed
app.get('/api/compress-pdf', async (req, res) => {
  const readStream = fs.createReadStream(req.body.path);
  
  const pdfDoc = await PDFLib.PDFDocument.load(readStream);
  // ... processing ...
  
  const pdfBytes = await pdfDoc.save();
  res.send(pdfBytes);
  
  // readStream không được close!
});
```

**Giải pháp tối ưu - Streaming and Memory Management**:

```javascript
// Best practice: Streaming và memory management
const { PDFDocument } = require('pdf-lib');
const { pipeline } = require('stream/promises');
const { createWriteStream, createReadStream } = require('fs');
const os = require('os');

class LargePDFProcessor {
  constructor(options = {}) {
    this.maxMemoryMB = options.maxMemoryMB || 512;
    this.tempDir = options.tempDir || os.tmpdir();
  }
  
  async processLargePDF(inputPath, outputPath) {
    // Use streaming để tránh load entire file vào memory
    const tempFiles = [];
    
    try {
      // Step 1: Get PDF info without loading full content
      const pdfInfo = await this.getPDFInfo(inputPath);
      const totalPages = pdfInfo.pageCount;
      
      // Step 2: Process in chunks
      const chunkSize = 10; // Process 10 pages at a time
      const writeStreams = [];
      
      for (let i = 0; i < totalPages; i += chunkSize) {
        const end = Math.min(i + chunkSize, totalPages);
        const chunkPath = path.join(this.tempDir, `chunk_${i}.pdf`);
        tempFiles.push(chunkPath);
        
        await this.processChunk(inputPath, chunkPath, i, end);
        
        // Force garbage collection periodically
        if (i % 50 === 0) {
          global.gc?.();
        }
      }
      
      // Step 3: Merge chunks
      await this.mergeChunks(writeStreams, outputPath);
      
    } finally {
      // Cleanup temp files
      await Promise.all(tempFiles.map(f => fs.unlink(f).catch(() => {})));
    }
  }
  
  async getPDFInfo(pdfPath) {
    // Chỉ đọc metadata, không load content
    const doc = await PDFDocument.load(
      fs.readFileSync(pdfPath),
      { 
        ignoreEncryption: true,
        updateMetadata: false 
      }
    );
    
    return {
      pageCount: doc.getPageCount(),
      metadata: doc.getMetadata()
    };
  }
  
  async processChunk(inputPath, outputPath, startPage, endPage) {
    // Load only the chunk we need
    const inputBuffer = fs.readFileSync(inputPath);
    const sourceDoc = await PDFDocument.load(inputBuffer, {
      maxChunkSize: this.maxMemoryMB * 1024 * 1024
    });
    
    const newDoc = await PDFDocument.create();
    const pageIndices = [];
    
    for (let i = startPage; i < endPage; i++) {
      pageIndices.push(i);
    }
    
    const copiedPages = await newDoc.copyPages(sourceDoc, pageIndices);
    copiedPages.forEach(page => newDoc.addPage(page));
    
    fs.writeFileSync(outputPath, await newDoc.save());
  }
  
  // Progressive processing với streaming
  async *streamProcessPDF(inputPath) {
    const pdfInfo = await this.getPDFInfo(inputPath);
    
    yield { type: 'start', totalPages: pdfInfo.pageCount };
    
    const inputBuffer = fs.readFileSync(inputPath);
    const doc = await PDFDocument.load(inputBuffer);
    
    for (let i = 0; i < doc.getPageCount(); i++) {
      const page = doc.getPages()[i];
      const pageData = await this.extractPageData(page);
      
      yield { type: 'page', pageNumber: i + 1, data: pageData };
      
      // Cleanup after each page
      delete pageData;
    }
    
    yield { type: 'complete' };
  }
}
```

### Anti-Pattern #6: Synchronous PDF Operations in Event Loop

**Mô tả**: Blocking event loop với synchronous PDF operations gây ra performance issues nghiêm trọng trong Node.js applications.

**Tại sao đây là vấn đề**:

Node.js uses single-threaded event loop. Synchronous operations block tất cả other requests, dẫn đến complete application freeze. Users experience extremely slow response times, timeouts, và connection errors.

**Code ví dụ - Anti-Pattern**:

```javascript
// Anti-pattern: Synchronous file operations
app.post('/api/generate-pdf', async (req, res) => {
  const html = req.body.html;
  
  // Anti-pattern: Synchronous operations
  fs.writeFileSync('/tmp/pdf-input.html', html);  // BLOCKS!
  
  await generatePDFWithWeasyPrint('/tmp/pdf-input.html', '/tmp/output.pdf');
  
  const pdfBuffer = fs.readFileSync('/tmp/output.pdf');  // BLOCKS!
  
  res.send(pdfBuffer);
});

// Anti-pattern: CPU-intensive operations blocking
app.get('/api/parse-pdf', async (req, res) => {
  const pdfData = await downloadPDF(req.query.url);
  
  // Anti-pattern: Synchronous parsing - BLOCKS for seconds
  const parsed = syncParsePDF(pdfData);  // This blocks!
  
  res.json(parsed);
});
```

**Giải pháp tối ưu - Async/Worker Thread Pattern**:

```javascript
// Best practice: Async operations và worker threads
const { Worker } = require('worker_threads');
const { unlink, writeFile, readFile } = require('fs').promises;
const path = require('path');
const os = require('os');

// Worker thread cho CPU-intensive PDF operations
function runPDFWorker(workerData) {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./pdf-processor-worker.js', {
      workerData
    });
    
    worker.on('message', resolve);
    worker.on('error', reject);
    worker.on('exit', (code) => {
      if (code !== 0) {
        reject(new Error(`Worker stopped with exit code ${code}`));
      }
    });
  });
}

// Async file operations
class AsyncPDFService {
  async generatePDF(htmlContent, options = {}) {
    const tempInput = path.join(os.tmpdir(), `input_${Date.now()}.html`);
    const tempOutput = path.join(os.tmpdir(), `output_${Date.now()}.pdf`);
    
    try {
      // Async file writes - non-blocking
      await writeFile(tempInput, htmlContent, 'utf8');
      
      // Run CPU-intensive work in worker thread
      const result = await runPDFWorker({
        inputPath: tempInput,
        outputPath: tempOutput,
        options
      });
      
      // Async file read - non-blocking
      const pdfBuffer = await readFile(tempOutput);
      
      return pdfBuffer;
      
    } finally {
      // Cleanup
      await Promise.all([
        unlink(tempInput).catch(() => {}),
        unlink(tempOutput).catch(() => {})
      ]);
    }
  }
  
  async processPDFInWorker(pdfBuffer) {
    // Offload to worker thread
    return await runPDFWorker({
      type: 'parse',
      pdfBuffer: pdfBuffer.toString('base64')
    });
  }
}

// Worker file (pdf-processor-worker.js)
const { parentPort, workerData } = require('worker_threads');
const fs = require('fs');
const path = require('path');

async function processPDF() {
  const { type, inputPath, outputPath, options } = workerData;
  
  if (type === 'generate') {
    // Run synchronous PDF generation in worker
    const result = await generateWithPuppeteer(inputPath, outputPath, options);
    parentPort.postMessage({ success: true, outputPath });
  } else if (type === 'parse') {
    // Parse in worker thread
    const result = await parsePDF(workerData.pdfBuffer);
    parentPort.postMessage({ success: true, data: result });
  }
}

processPDF().catch(error => {
  parentPort.postMessage({ success: false, error: error.message });
});
```

### Anti-Pattern #7: Not Handling Concurrent Access Properly

**Mô tả**: Việc không properly handle concurrent PDF generation requests dẫn đến race conditions và corrupted outputs.

**Tại sao đây là vấn đề**:

Khi multiple users request PDF generation cùng lúc với shared resources (temp files, fonts, templates), race conditions có thể xảy ra. Output files có thể be overwritten by other requests, resulting in users receiving wrong documents. Điều này đặc biệt nghiêm trọng trong invoice/document generation where correctness is critical.

**Code ví dụ - Anti-Pattern**:

```javascript
// Anti-pattern: Shared mutable state
let currentTemplate = null;
let currentOutputPath = '/tmp/output.pdf';

app.post('/api/generate-pdf', async (req, res) => {
  // Anti-pattern: Race condition
  currentTemplate = req.body.template;
  currentOutputPath = `/tmp/output-${req.body.id}.pdf`;
  
  // Another request could change these before we use them!
  const html = renderTemplate(currentTemplate, req.body.data);
  
  await generatePDF(html, currentOutputPath);
  
  // Send wrong file if another request changed outputPath!
  res.sendFile(currentOutputPath);
});

// Anti-pattern: Sequential processing bottleneck
class PDFGenerator {
  async generate(data) {
    // This creates a Puppeteer instance per call
    const browser = await puppeteer.launch();  // SLOW!
    const page = await browser.newPage();
    // ...
    await browser.close();
    return pdfBuffer;
  }
}

// Multiple concurrent requests = many browser instances = OOM
```

**Giải pháp tối ưu - Concurrent-Safe Design**:

```javascript
// Best practice: Concurrent-safe PDF generation
const PQueue = require('p-queue');

class ConcurrentSafePDFGenerator {
  constructor(options = {}) {
    this.maxConcurrent = options.maxConcurrent || 2;
    this.queue = new PQueue({ 
      concurrency: this.maxConcurrent 
    });
    this.browser = null;
    this.browserLaunched = false;
  }
  
  async initialize() {
    if (!this.browserLaunched) {
      this.browser = await puppeteer.launch({
        args: ['--max-old-space-size=512']
      });
      this.browserLaunched = true;
    }
    return this.browser;
  }
  
  async generatePDF(jobId, html, options = {}) {
    // Tạo unique paths cho mỗi job
    const tempDir = os.tmpdir();
    const inputPath = path.join(tempDir, `pdf-input-${jobId}.html`);
    const outputPath = path.join(tempDir, `pdf-output-${jobId}.pdf`);
    
    try {
      // Serialize access thông qua queue
      return await this.queue.add(async () => {
        // Write input với unique name
        await fs.writeFile(inputPath, html, 'utf8');
        
        const browser = await this.initialize();
        const page = await browser.newPage();
        
        try {
          await page.setContent(html, { waitUntil: 'networkidle0' });
          
          const pdfBuffer = await page.pdf({
            path: outputPath,
            format: options.format || 'A4',
            printBackground: options.printBackground !== false,
            margin: options.margin || { top: '20px', bottom: '20px' }
          });
          
          return pdfBuffer;
          
        } finally {
          await page.close();
        }
      });
      
    } finally {
      // Cleanup unique temp files
      await Promise.all([
        fs.unlink(inputPath).catch(() => {}),
        fs.unlink(outputPath).catch(() => {})
      ]);
    }
  }
  
  async close() {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
      this.browserLaunched = false;
    }
  }
}

// Usage với request-level isolation
app.post('/api/generate-pdf', async (req, res) => {
  const jobId = crypto.randomUUID(); // Unique per request
  const generator = req.app.locals.pdfGenerator;
  
  try {
    const html = renderTemplate(req.body.template, req.body.data);
    const pdfBuffer = await generator.generatePDF(jobId, html, {
      format: 'A4',
      printBackground: true
    });
    
    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', 
      `attachment; filename="document-${jobId}.pdf"`);
    res.send(pdfBuffer);
    
  } catch (error) {
    console.error('PDF generation failed:', error);
    res.status(500).json({ error: 'PDF generation failed' });
  }
});
```

## Common Patterns

### Pattern 1: The "Just Works" Trap

Nhiều developers adopt anti-patterns vì chúng "just work" trong development environment. Đặc biệt với PDF processing, một solution có thể work perfectly với sample data nhưng fail catastrophically với production workloads. Prevention: Luôn test với realistic data sizes và concurrent load từ early stages.

### Pattern 2: Premature Optimization Avoidance

Ngược lại với premature optimization, nhiều developers ignore optimization entirely vì "it works fine on my machine". PDF files có thể grow exponentially, và issues chỉ manifest khi user count increases. Prevention: Establish performance budgets từ đầu và monitor against them.

### Pattern 3: Copy-Paste from Stack Overflow

Many anti-patterns are perpetuated through code copied from online examples that prioritize simplicity over correctness. Prevention: Always evaluate code snippets in context of your specific requirements and scale.

## Troubleshooting

### Identifying Anti-Patterns in Your Codebase

**Signs you have embedding issues**:

```bash
# Check average PDF size
find ./storage/pdfs -name "*.pdf" -exec ls -lh {} \; | \
  awk '{print $5}' | \
  awk '{sum+=$1; count++} END {print "Average:", sum/count "KB"}'

# Find unusually large PDFs
find ./storage/pdfs -name "*.pdf" -size +5M -ls
```

**Signs you have caching issues**:

```bash
# Monitor PDF generation time
grep "pdf_generation_time" logs/*.log | \
  awk -F',' '{print $2}' | \
  awk '{sum+=$1; count++} END {print "Average:", sum/count "ms"}'

# Check cache hit rate
redis-cli info stats | grep pdf
```

**Signs you have memory issues**:

```javascript
// Add memory monitoring
setInterval(() => {
  const used = process.memoryUsage();
  console.log({
    heapUsed: Math.round(used.heapUsed / 1024 / 1024) + 'MB',
    heapTotal: Math.round(used.heapTotal / 1024 / 1024) + 'MB',
    rss: Math.round(used.rss / 1024 / 1024) + 'MB'
  });
}, 30000);
```

### Quick Fixes vs Long-Term Solutions

**Quick Fix (Temporary)**:

```javascript
// Quick fix for large PDFs: just enable compression
const pdfBuffer = await page.pdf({
  format: 'A4',
  // Enable built-in compression
});
```

**Long-term Solution**:

Implement proper image optimization pipeline, font subsetting, và caching strategy as described in the solutions above.

## Examples

### Example 1: Complete PDF Generation Service with Anti-Patterns Fixed

```javascript
// Complete solution avoiding all anti-patterns
const { Worker } = require('worker_threads');
const sharp = require('sharp');
const PQueue = require('p-queue');
const crypto = require('crypto');

class ProductionPDFService {
  constructor(options = {}) {
    this.redis = options.redis;
    this.s3 = options.s3;
    this.maxConcurrent = options.maxConcurrent || 2;
    this.queue = new PQueue({ concurrency: this.maxConcurrent });
    this.browser = null;
    
    // Image optimization settings
    this.imageOptions = {
      maxWidth: 1200,
      maxHeight: 1200,
      quality: 85
    };
    
    // Font subsetting
    this.fontCache = new Map();
  }
  
  async initialize() {
    if (!this.browser) {
      this.browser = await puppeteer.launch({
        args: ['--max-old-space-size=512']
      });
    }
    return this.browser;
  }
  
  generateCacheKey(data, templateId) {
    return `pdf:${templateId}:${crypto
      .createHash('sha256')
      .update(JSON.stringify(data))
      .digest('hex')
      .substring(0, 16)}`;
  }
  
  async optimizeImage(imageBuffer) {
    return await sharp(imageBuffer)
      .resize(this.imageOptions.maxWidth, this.imageOptions.maxHeight, {
        fit: 'inside',
        withoutEnlargement: true
      })
      .jpeg({ quality: this.imageOptions.quality, progressive: true })
      .toBuffer();
  }
  
  async generatePDF(jobId, data, template) {
    const cacheKey = this.generateCacheKey(data, template.id);
    
    // Check cache first (Anti-Pattern #3 fix)
    const cached = await this.redis.hgetall(cacheKey);
    if (cached.exists === 'true') {
      return { buffer: await this.s3.get(cached.storageKey), cached: true };
    }
    
    // Optimize images (Anti-Pattern #2 fix)
    const optimizedImages = await Promise.all(
      (data.images || []).map(img => this.optimizeImage(img.buffer))
    );
    
    // Render with optimized assets
    const html = await template.render({
      ...data,
      images: optimizedImages
    });
    
    // Generate in worker thread (Anti-Pattern #6 fix)
    const pdfBuffer = await this.queue.add(async () => {
      const browser = await this.initialize();
      const page = await browser.newPage();
      
      try {
        await page.setContent(html, { waitUntil: 'networkidle0' });
        return await page.pdf({
          format: 'A4',
          printBackground: true,
          margin: { top: '20px', bottom: '20px', left: '20px', right: '20px' }
        });
      } finally {
        await page.close();
      }
    });
    
    // Cache result (Anti-Pattern #3 fix)
    const storageKey = `pdfs/${cacheKey}.pdf`;
    await this.s3.put(storageKey, pdfBuffer);
    await this.redis.hset(cacheKey, {
      exists: 'true',
      storageKey,
      size: pdfBuffer.length,
      generatedAt: new Date().toISOString()
    });
    await this.redis.expire(cacheKey, 86400);
    
    return { buffer: pdfBuffer, cached: false };
  }
  
  async close() {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
    }
  }
}
```

## References

- Adobe PDF Reference (ISO 32000): https://www.adobe.com/content/dam/acom/en/devnet/pdf/pdfs/PDF32000_1.pdf
- PDF.js Documentation: https://github.com/mozilla/pdf.js
- Font Subsetting Best Practices: https://developers.google.com/fonts/docs/subsetting
- Puppeteer PDF Options: https://pptr.dev/api/puppeteer.pdfoptions
- pdf-lib Documentation: https://pdf-lib.org/
- OWASP Path Traversal Prevention: https://owasp.org/www-community/OWASP_Validation_Regex_Repository
- Node.js Memory Management: https://nodejs.org/en/guides/guides/memory-management
