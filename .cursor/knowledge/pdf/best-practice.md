---
title: "PDF Best Practices - Thực Hành Tốt Nhất Khi Xử Lý PDF"
description: "Comprehensive guide to best practices for PDF generation, optimization, and processing including font subsetting, image compression, template caching, async generation, digital signatures, and accessibility"
tags: ["pdf", "best-practices", "performance", "optimization", "accessibility", "cursor-enterprise-framework"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# PDF Best Practices - Thực Hành Tốt Nhất Khi Xử Lý PDF

## Overview

Việc tạo và xử lý PDF trong môi trường enterprise đòi hỏi không chỉ hiểu biết về kỹ thuật mà còn phải nắm vững các best practices đã được kiểm chứng qua thực tế. Tài liệu này tổng hợp những best practices thiết yếu cho việc xử lý PDF, từ font management, image optimization, đến accessibility và security. Mỗi best practice đều đi kèm với rationale (lý do), implementation details, và code examples để developers có thể áp dụng ngay vào production systems.

Trong bối cảnh các ứng dụng web hiện đại, PDF vẫn là định dạng document tiêu chuẩn cho việc chia sẻ và lưu trữ tài liệu quan trọng như hóa đơn, báo cáo, hợp đồng. Việc generate PDF một cách hiệu quả không chỉ improves user experience mà còn reduces infrastructure costs đáng kể thông qua việc giảm bandwidth, storage, và processing time.

## Purpose

Tài liệu này phục vụ nhiều mục đích quan trọng cho đội ngũ phát triển và vận hành. Trước tiên, nó cung cấp một comprehensive reference cho việc implement PDF features trong enterprise applications. Thứ hai, nó thiết lập các tiêu chuẩn về performance, security, và maintainability mà tất cả PDF-related code nên tuân thủ. Thứ ba, nó giúp reduce decision fatigue bằng cách đưa ra những recommendations đã được proven qua production experience. Cuối cùng, nó serve as a training resource cho new team members để họ quickly understand best practices mà không cần học từ mistakes.

## Key Concepts

### 1. Performance Budgeting for PDFs

Trước khi implement bất kỳ PDF feature nào, điều quan trọng là phải establish performance budgets. Một typical PDF performance budget có thể bao gồm các metrics như maximum file size (ví dụ: 500KB cho một invoice page), target generation time (dưới 3 giây cho documents thông thường), maximum memory usage (không quá 512MB per request), và cache hit rate target (trên 80% cho repeated content). Việc define và monitor these budgets đảm bảo rằng hệ thống luôn meet performance expectations.

### 2. The PDF Generation Pipeline

Một PDF generation pipeline hiệu quả thường bao gồm nhiều stages: data preparation (fetching và transforming input data), template rendering (converting template + data sang HTML), asset optimization (optimizing images, subsetting fonts), PDF rendering (HTML to PDF conversion), post-processing (compression, signature, metadata), và caching/storage. Mỗi stage nên be designed independently và có clear interfaces với các stages khác để dễ dàng optimize và debug.

### 3. Observability Requirements

Production PDF systems cần có comprehensive observability. Điều này bao gồm metrics (generation time, file size, cache hit rate, error rates), logging (structured logs với request IDs để trace issues), và tracing (distributed tracing để identify bottlenecks trong complex pipelines). Không có observability, việc optimize và debug production issues trở nên extremely difficult.

## Best Practices

### Best Practice #1: Font Subsetting

#### Tại sao quan trọng

Font subsetting là quá trình chỉ embed những glyphs thực sự được sử dụng trong document thay vì entire font file. Một typical full font file có thể từ 500KB đến 5MB, trong khi một subset chỉ chứa các characters cần thiết có thể chỉ từ 20KB đến 100KB. Điều này có thể reduce PDF file size từ 50% đến 90%, tùy thuộc vào font và content.

#### Implementation Strategy

```javascript
// Font subsetting service sử dụng fonttools
const { SubsetFont } = require('fonttools/subset');
const fs = require('fs').promises;
const path = require('path');

class FontSubsettingService {
  constructor(options = {}) {
    this.cacheDir = options.cacheDir || './font-cache';
    this.fontDir = options.fontDir || './fonts';
  }
  
  async subsetFont(fontPath, text) {
    const fontName = path.basename(fontPath, path.extname(fontPath));
    const cacheKey = this.generateCacheKey(fontPath, text);
    const cachedPath = path.join(this.cacheDir, `${cacheKey}.woff2`);
    
    // Check cache first
    try {
      const cached = await fs.readFile(cachedPath);
      return cached;
    } catch (e) {
      // Cache miss, need to subset
    }
    
    // Load font và subset
    const font = await fonttools.load(fontPath);
    const subset = new SubsetFont();
    
    // Add characters từ text
    const uniqueChars = [...new Set(text)];
    subset.populate(text);
    
    // Subset và save
    const subsetBuffer = await subset.subset(font);
    const woff2Buffer = await this.convertToWoff2(subsetBuffer);
    
    // Cache result
    await fs.mkdir(this.cacheDir, { recursive: true });
    await fs.writeFile(cachedPath, woff2Buffer);
    
    return woff2Buffer;
  }
  
  generateCacheKey(fontPath, text) {
    const hash = crypto.createHash('sha256')
      .update(fontPath + ':' + [...new Set(text)].sort().join(''))
      .digest('hex')
      .substring(0, 16);
    return `${path.basename(fontPath, '.ttf')}_${hash}`;
  }
  
  async convertToWoff2(buffer) {
    // Sử dụng woff2 encoder
    const woff2 = require('woff2');
    return await woff2.encode(buffer);
  }
  
  async prepareFontsForDocument(documentText, fontConfig) {
    const fontPreparations = {};
    
    for (const [fontFamily, fontData] of Object.entries(fontConfig)) {
      const fontPath = path.join(this.fontDir, fontData.file);
      const subsetBuffer = await this.subsetFont(fontPath, documentText);
      
      fontPreparations[fontFamily] = {
        buffer: subsetBuffer,
        family: fontFamily,
        weight: fontData.weight || 'normal',
        style: fontData.style || 'normal'
      };
    }
    
    return fontPreparations;
  }
}

// Integration với Puppeteer
class PDFGeneratorWithFontSubset {
  constructor() {
    this.fontService = new FontSubsettingService();
  }
  
  async generateWithOptimizedFonts(template, data) {
    // Bước 1: Render HTML để extract text
    const html = template.render(data);
    const textContent = this.extractText(html);
    
    // Bước 2: Prepare subset fonts
    const fontConfig = {
      'Roboto': { file: 'Roboto-Regular.ttf', weight: 400 },
      'Roboto-Bold': { file: 'Roboto-Bold.ttf', weight: 700 },
      'NotoSans': { file: 'NotoSans-Regular.ttf', weight: 400 }
    };
    
    const preparedFonts = await this.fontService.prepareFontsForDocument(
      textContent,
      fontConfig
    );
    
    // Bước 3: Convert fonts sang base64 data URIs
    const css = this.generateFontCSS(preparedFonts);
    
    // Bước 4: Generate PDF
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    // Inject optimized CSS với embedded fonts
    await page.setContent(html + `<style>${css}</style>`);
    
    const pdfBuffer = await page.pdf({ format: 'A4' });
    await browser.close();
    
    return pdfBuffer;
  }
  
  extractText(html) {
    // Strip HTML tags để get text content
    return html.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ');
  }
  
  generateFontCSS(fonts) {
    let css = '';
    for (const [name, font] of Object.entries(fonts)) {
      const base64 = font.buffer.toString('base64');
      css += `
        @font-face {
          font-family: '${font.family}';
          src: url('data:font/woff2;base64,${base64}') format('woff2');
          font-weight: ${font.weight};
          font-style: ${font.style};
        }
      `;
    }
    return css;
  }
}
```

### Best Practice #2: Image Compression

#### Tại sao quan trọng

Images thường chiếm 70-90% total PDF file size. Một single high-resolution image có thể lớn hơn cả toàn bộ text content của document. Việc optimize images trước khi embed vào PDF là một trong những impact cao nhất optimization có thể thực hiện.

#### Image Optimization Pipeline

```javascript
const sharp = require('sharp');
const path = require('path');
const crypto = require('crypto');

class ImageOptimizationPipeline {
  constructor(options = {}) {
    this.maxWidth = options.maxWidth || 1200;
    this.maxHeight = options.maxHeight || 1200;
    this.quality = options.quality || 85;
    this.formats = options.formats || {
      photo: { extension: 'jpeg', quality: 85 },
      graphic: { extension: 'png', compressionLevel: 9 },
      screenshot: { extension: 'webp', quality: 80 }
    };
    this.cacheDir = options.cacheDir;
  }
  
  async optimizeImage(inputPath, imageType = 'photo') {
    const config = this.formats[imageType] || this.formats.photo;
    const cacheKey = await this.getCacheKey(inputPath, config);
    
    // Try cache first
    if (this.cacheDir) {
      const cachedPath = path.join(this.cacheDir, `${cacheKey}.${config.extension}`);
      try {
        return await fs.readFile(cachedPath);
      } catch (e) {}
    }
    
    const image = sharp(inputPath);
    const metadata = await image.metadata();
    
    // Resize nếu cần thiết
    let processor = image;
    if (metadata.width > this.maxWidth || metadata.height > this.maxHeight) {
      processor = image.resize(this.maxWidth, this.maxHeight, {
        fit: 'inside',
        withoutEnlargement: true
      });
    }
    
    // Apply format-specific processing
    switch (config.extension) {
      case 'jpeg':
        processor = processor.jpeg({ 
          quality: config.quality,
          progressive: true,
          mozjpeg: true
        });
        break;
      case 'png':
        processor = processor.png({ 
          compressionLevel: config.compressionLevel,
          progressive: true
        });
        break;
      case 'webp':
        processor = processor.webp({ 
          quality: config.quality,
          effort: 6
        });
        break;
    }
    
    const optimizedBuffer = await processor.toBuffer();
    
    // Cache result
    if (this.cacheDir) {
      await fs.mkdir(this.cacheDir, { recursive: true });
      const cachedPath = path.join(this.cacheDir, `${cacheKey}.${config.extension}`);
      await fs.writeFile(cachedPath, optimizedBuffer);
    }
    
    return optimizedBuffer;
  }
  
  async getCacheKey(inputPath, config) {
    const stats = await fs.stat(inputPath);
    const content = `${inputPath}:${stats.mtime.getTime()}:${JSON.stringify(config)}`;
    return crypto.createHash('sha256').update(content).digest('hex').substring(0, 16);
  }
  
  // Batch optimization cho multiple images
  async optimizeImagesForDocument(images) {
    const results = await Promise.all(
      images.map(async (img) => {
        const optimized = await this.optimizeImage(img.path, img.type);
        return {
          originalName: img.path,
          buffer: optimized,
          type: img.type
        };
      })
    );
    
    return results;
  }
}

// Advanced: DPI optimization cho print vs screen
class PrintImageOptimizer {
  constructor() {
    this.screenDPI = 96;
    this.printDPI = 300;
  }
  
  calculateOptimalDimensions(originalWidth, originalHeight, targetDPI, maxDimension = 2400) {
    // Calculate aspect ratio
    const aspectRatio = originalWidth / originalHeight;
    
    // Calculate dimensions at target DPI
    let optimalWidth = originalWidth * (targetDPI / this.screenDPI);
    let optimalHeight = originalHeight * (targetDPI / this.screenDPI);
    
    // Scale down nếu exceeds max
    if (optimalWidth > maxDimension) {
      optimalWidth = maxDimension;
      optimalHeight = maxDimension / aspectRatio;
    }
    if (optimalHeight > maxDimension) {
      optimalHeight = maxDimension;
      optimalWidth = maxDimension * aspectRatio;
    }
    
    return {
      width: Math.round(optimalWidth),
      height: Math.round(optimalHeight)
    };
  }
  
  async optimizeForPrint(imagePath, options = {}) {
    const metadata = await sharp(imagePath).metadata();
    const { width, height } = this.calculateOptimalDimensions(
      metadata.width,
      metadata.height,
      options.dpi || this.printDPI,
      options.maxDimension || 2400
    );
    
    return await sharp(imagePath)
      .resize(width, height, { fit: 'fill' })
      .jpeg({ quality: options.quality || 95, progressive: true })
      .toBuffer();
  }
}
```

### Best Practice #3: Template Caching

#### Tại sao quan trọng

Template compilation và parsing có thể tốn đáng kể CPU time, đặc biệt với complex templates. Caching compiled templates giúp reduce latency và CPU usage đáng kể. Một template thường được reused thousands of times, so amortizing the compilation cost across all uses là rất hiệu quả.

#### Implementation

```javascript
const LRU = require('lru-cache');

class TemplateCache {
  constructor(options = {}) {
    this.maxSize = options.maxSize || 100;
    this.maxAge = options.maxAge || 1000 * 60 * 60; // 1 hour
    this.templateDir = options.templateDir;
    this.engine = options.engine || 'handlebars';
    
    // LRU cache for compiled templates
    this.cache = new LRU({
      max: this.maxSize,
      ttl: this.maxAge,
      updateAgeOnGet: true
    });
    
    // Watch for template changes in development
    if (options.watch !== false) {
      this.setupWatcher();
    }
  }
  
  setupWatcher() {
    const chokidar = require('chokidar');
    const watcher = chokidar.watch(
      path.join(this.templateDir, '**/*.hbs'),
      { persistent: true }
    );
    
    watcher.on('change', (filePath) => {
      const key = this.getTemplateKey(filePath);
      this.cache.delete(key);
      console.log(`Template cache invalidated: ${filePath}`);
    });
  }
  
  getTemplateKey(templatePath) {
    const relativePath = path.relative(this.templateDir, templatePath);
    return `${this.engine}:${relativePath}`;
  }
  
  async getTemplate(templateName) {
    const cacheKey = this.getTemplateKey(
      path.join(this.templateDir, templateName)
    );
    
    // Check cache
    let template = this.cache.get(cacheKey);
    if (template) {
      return template;
    }
    
    // Load and compile
    const templatePath = path.join(this.templateDir, templateName);
    const source = await fs.readFile(templatePath, 'utf8');
    
    template = this.compileTemplate(source, templateName);
    this.cache.set(cacheKey, template);
    
    return template;
  }
  
  compileTemplate(source, name) {
    switch (this.engine) {
      case 'handlebars':
        return Handlebars.compile(source, {
          preventIndent: true,
          strict: true
        });
      
      case 'ejs':
        return EJS.compile(source, {
          cache: false,
          filename: name
        });
      
      case 'pug':
        return pug.compile(source, {
          cache: true,
          name: name
        });
      
      default:
        throw new Error(`Unsupported template engine: ${this.engine}`);
    }
  }
  
  // Warm up cache với commonly used templates
  async warmup(templateNames) {
    await Promise.all(
      templateNames.map(name => this.getTemplate(name))
    );
    console.log(`Template cache warmed with ${templateNames.length} templates`);
  }
  
  // Invalidate specific template
  invalidate(templateName) {
    const key = this.getTemplateKey(
      path.join(this.templateDir, templateName)
    );
    this.cache.delete(key);
  }
  
  // Get cache statistics
  getStats() {
    return {
      size: this.cache.size,
      calculated: this.cache.calculate()
    };
  }
}

// Template service integration
class PDFTemplateService {
  constructor(options = {}) {
    this.templateCache = new TemplateCache({
      templateDir: options.templateDir,
      engine: options.engine || 'handlebars',
      watch: process.env.NODE_ENV === 'development'
    });
  }
  
  async renderTemplate(templateName, data) {
    const template = await this.templateCache.getTemplate(templateName);
    return template(data);
  }
  
  async renderTemplateWithLayout(templateName, data, layoutName) {
    const [template, layout] = await Promise.all([
      this.templateCache.getTemplate(templateName),
      this.templateCache.getTemplate(layoutName)
    ]);
    
    const content = template(data);
    return layout({ ...data, body: content });
  }
}
```

### Best Practice #4: Async Generation

#### Tại sao quan trọng

Synchronous PDF generation blocks event loop và causes poor user experience. Users phải wait for generation to complete before receiving response. Async generation với background processing allows immediate response (với job ID) và improved scalability.

#### Implementation

```javascript
const Bull = require('bull');
const { Worker } = require('worker_threads');

class AsyncPDFService {
  constructor(options = {}) {
    this.redisUrl = options.redisUrl;
    this.queue = new Bull('pdf-generation', {
      redis: this.redisUrl,
      defaultJobOptions: {
        attempts: 3,
        backoff: {
          type: 'exponential',
          delay: 2000
        }
      }
    });
    
    // Setup job processing
    this.queue.process(this.handlePDFJob.bind(this));
    
    // Event handlers
    this.setupEventHandlers();
  }
  
  setupEventHandlers() {
    this.queue.on('completed', (job, result) => {
      console.log(`PDF job ${job.id} completed`);
      // Notify via WebSocket, update database, etc.
    });
    
    this.queue.on('failed', (job, err) => {
      console.error(`PDF job ${job.id} failed:`, err.message);
    });
    
    this.queue.on('progress', (job, progress) => {
      // Update job progress in real-time
    });
  }
  
  async handlePDFJob(job) {
    const { jobId, template, data, options } = job.data;
    
    await job.progress(10);
    
    // Step 1: Render template
    const html = await this.renderTemplate(template, data);
    await job.progress(30);
    
    // Step 2: Generate PDF (in worker thread)
    const pdfBuffer = await this.generatePDFInWorker(html, options);
    await job.progress(80);
    
    // Step 3: Upload to storage
    const storageKey = await this.uploadToStorage(pdfBuffer, jobId);
    await job.progress(100);
    
    return {
      jobId,
      storageKey,
      size: pdfBuffer.length,
      generatedAt: new Date().toISOString()
    };
  }
  
  async generateInBackground(template, data, options = {}) {
    const jobId = crypto.randomUUID();
    
    const job = await this.queue.add({
      jobId,
      template,
      data,
      options
    }, {
      jobId: jobId // Use custom job ID for easier tracking
    });
    
    return {
      jobId,
      status: 'queued',
      statusUrl: `/api/pdf/status/${jobId}`,
      estimatedTime: options.priority === 'high' ? 2000 : 5000
    };
  }
  
  async generatePDFInWorker(html, options) {
    return new Promise((resolve, reject) => {
      const worker = new Worker(`
        const puppeteer = require('puppeteer');
        
        async function generate() {
          const browser = await puppeteer.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
          });
          
          try {
            const page = await browser.newPage();
            await page.setContent(html, { waitUntil: 'networkidle0' });
            const pdf = await page.pdf({
              format: 'A4',
              printBackground: true,
              margin: { top: '20px', bottom: '20px' }
            });
            await browser.close();
            return pdf;
          } finally {
            await browser.close();
          }
        }
        
        generate().then(pdf => process.parentPort.postMessage({ success: true, pdf }))
                  .catch(err => process.parentPort.postMessage({ success: false, error: err.message }));
      `, { eval: true });
      
      worker.on('message', (result) => {
        if (result.success) {
          resolve(Buffer.from(result.pdf));
        } else {
          reject(new Error(result.error));
        }
      });
      
      worker.on('error', reject);
    });
  }
  
  async getJobStatus(jobId) {
    const job = await this.queue.getJob(jobId);
    
    if (!job) {
      return { status: 'not_found' };
    }
    
    const state = await job.getState();
    const progress = job.progress();
    const result = job.returnvalue;
    const failedReason = job.failedReason;
    
    return {
      status: state,
      progress,
      result: state === 'completed' ? result : undefined,
      error: state === 'failed' ? failedReason : undefined,
      createdAt: job.timestamp,
      processedAt: job.processedOn,
      finishedAt: job.finishedOn
    };
  }
}
```

### Best Practice #5: Digital Signatures

#### Tại sao quan trăng

Digital signatures trong PDF cung cấp authenticity (xác thực ai tạo ra document), integrity (đảm bảo document không bị thay đổi sau khi signed), và non-repudiation (người ký không thể phủ nhận). Đối với legal documents, invoices, và contracts, digital signatures là requirement không thể thiếu.

#### Implementation

```javascript
const { PDFDocument, rgb, PDFName, PDFDict, PDFArray } = require('pdf-lib');
const forge = require('node-forge');
const crypto = require('crypto');

class PDFSignatureService {
  constructor(options = {}) {
    this.certificates = options.certificates || {};
    this.timestampAuthority = options.tsa; // Timestamp Authority URL
  }
  
  // Tạo self-signed certificate cho demo
  generateSelfSignedCert() {
    const keys = forge.pki.rsa.generateKeyPair(2048);
    const cert = forge.pki.createCertificate();
    
    cert.publicKey = keys.publicKey;
    cert.serialNumber = forge.util.bytesToHex(crypto.randomBytes(16));
    cert.validity.notBefore = new Date();
    cert.validity.notAfter = new Date();
    cert.validity.notAfter.setFullYear(cert.validity.notBefore.getFullYear() + 1);
    
    const attrs = [{
      shortName: 'CN',
      value: 'PDF Signer'
    }, {
      shortName: 'O',
      value: 'Organization'
    }];
    
    cert.setSubject(attrs);
    cert.setIssuer(attrs);
    cert.sign(keys.privateKey);
    
    return {
      cert: forge.pki.certificateToPem(cert),
      key: forge.pki.privateKeyToPem(keys.privateKey)
    };
  }
  
  async signPDF(pdfBuffer, options = {}) {
    const {
      certPath = options.certificate,
      keyPath = options.privateKey,
      reason = 'Document signed',
      location = 'Office',
      contactInfo = '',
      signatureFieldName = 'Signature1'
    } = options;
    
    // Load certificate và key
    const certPem = await fs.readFile(certPath, 'utf8');
    const keyPem = await fs.readFile(keyPath, 'utf8');
    
    // Load PDF
    const pdfDoc = await PDFDocument.load(pdfBuffer);
    
    // Create signature field
    const page = pdfDoc.getPage(0);
    const { width, height } = page.getSize();
    
    // Add signature appearance
    const signatureBox = {
      x: width - 200,
      y: 20,
      width: 150,
      height: 50
    };
    
    // Create the signature field
    const signatureField = pdfDoc.context.obj({
      Type: 'Annot',
      Subtype: 'Widget',
      Rect: [signatureBox.x, signatureBox.y, 
             signatureBox.x + signatureBox.width, 
             signatureBox.y + signatureBox.height],
      FT: 'Sig',
      T: signatureFieldName,
      V: {
        Type: 'Sig',
        Filter: 'Adobe.PPKLite',
        SubFilter: 'adbe.pkcs7.detached',
        ByteRange: [0, '********', '********', '********'],
        Contents: '',
        Reason: reason,
        Location: location,
        ContactInfo: contactInfo,
        M: new Date().toISOString()
      },
      AP: {
        N: {
          Type: 'XObject',
          Subtype: 'Form',
          BBox: [0, 0, signatureBox.width, signatureBox.height],
          Contents: `q 0.5 g f /Helvetica 12 tf 0 0 0 rg (${reason}) show`
        }
      }
    });
    
    // Sign the PDF
    const signedPdfBytes = await this.applySignature(
      pdfBuffer,
      signatureField,
      certPem,
      keyPem,
      { reason, location, contactInfo }
    );
    
    return signedPdfBytes;
  }
  
  async applySignature(pdfBytes, signatureField, certPem, keyPem, options) {
    // Calculate signature placeholder size
    const signatureSize = 8192; // bytes
    const signaturePlaceholder = Buffer.alloc(signatureSize, 0);
    
    // Convert PDF to buffer if needed
    const pdfBuffer = Buffer.isBuffer(pdfBytes) ? pdfBytes : Buffer.from(pdfBytes);
    
    // Find byte range positions
    const startMarker = Buffer.from('/ByteRange [0 ');
    const endMarker = Buffer.from(' /Length ');
    
    // Calculate content and signature positions
    const contentEnd = pdfBuffer.indexOf(startMarker) + startMarker.length;
    const signatureStart = contentEnd;
    const contentStart = signatureStart + signatureSize + 2; // +2 for ' '
    
    // Calculate hash of content
    const contentPart1 = pdfBuffer.slice(0, signatureStart);
    const contentPart2 = pdfBuffer.slice(contentStart);
    const contentHash = crypto
      .createHash('sha256')
      .update(Buffer.concat([contentPart1, contentPart2]))
      .digest();
    
    // Create PKCS#7 signature
    const p7 = forge.pkcs7.createSignedData();
    p7.detached = true;
    
    // Add certificate
    const cert = forge.pki.certificateFromPem(certPem);
    p7.addCertificate(cert);
    
    // Add signer
    const key = forge.pki.privateKeyFromPem(keyPem);
    p7.addSigner({
      key: key,
      certificate: cert,
      digestAlgorithm: forge.pki.oids.sha256,
      authenticatedAttributes: [
        {
          type: forge.pki.oids.contentType,
          value: forge.pki.oids.data
        },
        {
          type: forge.pki.oids.messageDigest,
          value: contentHash
        }
      ]
    });
    
    // Add content
    p7.content = {
      value: Buffer.concat([contentPart1, contentPart2]),
      encode: () => Buffer.concat([contentPart1, contentPart2])
    };
    
    // Sign
    p7.sign({ detached: true });
    
    // Convert to DER
    const signatureDer = forge.asn1.toDer(p7.toAsn1()).getBytes();
    const signatureBase64 = forge.util.encode64(signatureDer);
    
    // Pad signature to exact size
    const paddedSignature = signatureBase64.padEnd(signatureSize, ' ');
    
    // Construct final PDF
    const result = Buffer.concat([
      contentPart1,
      Buffer.from(paddedSignature),
      contentPart2
    ]);
    
    return result;
  }
  
  async verifySignature(pdfBuffer) {
    // Load and verify signature
    const pdfDoc = await PDFDocument.load(pdfBuffer);
    const signatureFields = pdfDoc.catalog.get(PDFName.of('AcroForm'));
    
    if (!signatureFields) {
      return { signed: false };
    }
    
    // Extract signature field
    const fieldArray = signatureFields.get(PDFName.of('Fields'));
    if (!fieldArray) {
      return { signed: false };
    }
    
    // Verify each signature
    const signatures = [];
    for (const field of fieldArray.array) {
      const sig = this.verifySignatureField(field);
      signatures.push(sig);
    }
    
    return {
      signed: signatures.length > 0,
      signatures
    };
  }
  
  verifySignatureField(field) {
    // Implementation of signature verification
    return {
      fieldName: field.get(PDFName.of('T')),
      reason: field.getIn(PDFName.of('V'), PDFName.of('Reason')),
      location: field.getIn(PDFName.of('V'), PDFName.of('Location')),
      signedAt: field.getIn(PDFName.of('V'), PDFName.of('M')),
      valid: true // Actual verification requires cryptographic checks
    };
  }
}
```

### Best Practice #6: Accessibility (PDF/UA)

#### Tại sao quan trọng

PDF/UA (Universal Accessibility) là ISO standard cho accessible PDF documents. Nó đảm bảo rằng documents có thể được access bởi people with disabilities, bao gồm người dùng screen readers. Ngoài legal requirements trong nhiều jurisdictions, accessibility improves usability cho tất cả users.

#### Implementation

```javascript
const { PDFDocument, StandardFonts, rgb } = require('pdf-lib');

class AccessiblePDFService {
  constructor() {
    this.metadata = {
      title: '',
      author: '',
      subject: '',
      keywords: [],
      creator: 'Accessible PDF Generator',
      producer: 'Enterprise PDF System',
      creationDate: new Date()
    };
  }
  
  async createAccessiblePDF(content, options = {}) {
    const pdfDoc = await PDFDocument.create();
    
    // Set metadata
    pdfDoc.setTitle(options.title || 'Document');
    pdfDoc.setAuthor(options.author || 'Unknown');
    pdfDoc.setSubject(options.subject || '');
    pdfDoc.setKeywords(options.keywords || []);
    pdfDoc.setCreator(this.metadata.creator);
    pdfDoc.setProducer(this.metadata.producer);
    pdfDoc.setCreationDate(this.metadata.creationDate);
    pdfDoc.setModificationDate(new Date());
    
    // Set PDF/A-1a compatible settings
    pdfDoc.catalog.getOrCreateViewerPreferences();
    
    // Create pages with proper structure
    for (const pageContent of content.pages) {
      const page = pdfDoc.addPage([pageContent.width || 595, pageContent.height || 842]);
      
      // Add page tree node
      page.node.set(PDFName.of('Tabs'), PDFName.of('S'));
      
      // Add content
      if (pageContent.text) {
        await this.addAccessibleText(page, pageContent.text, pdfDoc);
      }
      
      // Add images with alt text
      if (pageContent.images) {
        for (const img of pageContent.images) {
          await this.addAccessibleImage(page, img, pdfDoc);
        }
      }
    }
    
    // Add document outline (bookmarks)
    if (content.headings) {
      this.addDocumentOutline(pdfDoc, content.headings);
    }
    
    return await pdfDoc.save();
  }
  
  async addAccessibleText(page, textContent, pdfDoc) {
    const helvetica = await pdfDoc.embedFont(StandardFonts.Helvetica);
    
    const text = `${textContent.value}`;
    const fontSize = textContent.fontSize || 12;
    const color = rgb(0, 0, 0);
    
    page.drawText(text, {
      x: textContent.x || 50,
      y: textContent.y || 700,
      size: fontSize,
      font: helvetica,
      color: color,
      maxWidth: textContent.maxWidth || 500
    });
    
    // Mark heading in structure tree
    if (textContent.headingLevel) {
      page.node.set(
        PDFName.of('H'),
        PDFName.of(`H${textContent.headingLevel}`)
      );
    }
  }
  
  async addAccessibleImage(page, imageData, pdfDoc) {
    // Embed image
    let image;
    if (imageData.format === 'png') {
      image = await pdfDoc.embedPng(imageData.buffer);
    } else if (imageData.format === 'jpeg') {
      image = await pdfDoc.embedJpg(imageData.buffer);
    }
    
    page.drawImage(image, {
      x: imageData.x,
      y: imageData.y,
      width: imageData.width,
      height: imageData.height
    });
    
    // Add artifact for decorative images
    if (!imageData.altText) {
      page.node.set(
        PDFName.of('Contents'),
        PDFName.of('Artifact')
      );
    }
  }
  
  addDocumentOutline(pdfDoc, headings) {
    const root = pdfDoc.context.obj({
      Type: 'Outlines',
      Count: headings.length
    });
    
    let prev = null;
    let first = null;
    
    for (let i = 0; i < headings.length; i++) {
      const heading = headings[i];
      const outlineItem = pdfDoc.context.obj({
        Title: new String(heading.text),
        Parent: root,
        Dest: `[page ${heading.pageIndex} /XYZ 0 0 0]`
      });
      
      if (prev) {
        outlineItem.set(PDFName.of('Prev'), prev);
        prev.set(PDFName.of('Next'), outlineItem);
      }
      
      if (!first) {
        first = outlineItem;
      }
      
      prev = outlineItem;
    }
    
    if (first) {
      root.set(PDFName.of('First'), first);
      root.set(PDFName.of('Last'), prev);
    }
    
    pdfDoc.catalog.set(PDFName.of('Outlines'), root);
  }
  
  // Add lang attribute for language
  setDocumentLanguage(pdfDoc, lang) {
    pdfDoc.catalog.set(
      PDFName.of('Lang'),
      new String(lang)
    );
  }
  
  // Mark document as tagged PDF
  enableTaggedPDF(pdfDoc) {
    pdfDoc.catalog.set(
      PDFName.of('MarkInfo'),
      pdfDoc.context.obj({
        Marked: true
      })
    );
  }
}
```

## Common Patterns

### Pattern 1: Multi-Level Caching Strategy

Production PDF systems nên implement multi-level caching:

1. **Redis Cache** (fast, in-memory): Stores metadata về generated PDFs, cache keys
2. **Object Storage** (S3/GCS/Azure Blob): Stores actual PDF files
3. **CDN Cache**: Cached versions near users for fast delivery
4. **Browser Cache**: ETag/Last-Modified headers for client-side caching

```javascript
class MultiLevelCache {
  constructor(options) {
    this.redis = new Redis(options.redisUrl);
    this.storage = options.storage; // S3, GCS, etc.
    this.cdn = options.cdn; // CloudFlare, CloudFront, etc.
  }
  
  async get(cacheKey) {
    // Level 1: Check Redis
    const meta = await this.redis.hgetall(cacheKey);
    if (!meta || meta.exists !== 'true') {
      return null;
    }
    
    // Level 2: Get from storage
    const pdfBuffer = await this.storage.get(meta.storageKey);
    
    return {
      buffer: pdfBuffer,
      metadata: meta
    };
  }
  
  async set(cacheKey, pdfBuffer, metadata = {}) {
    const storageKey = `pdfs/${cacheKey}.pdf`;
    
    // Store in object storage
    await this.storage.put(storageKey, pdfBuffer);
    
    // Update Redis metadata
    await this.redis.hset(cacheKey, {
      exists: 'true',
      storageKey,
      size: pdfBuffer.length,
      createdAt: new Date().toISOString(),
      ...metadata
    });
    
    // Set TTL (e.g., 24 hours)
    await this.redis.expire(cacheKey, 86400);
    
    // Invalidate CDN cache
    await this.cdn.purge(`/${storageKey}`);
  }
}
```

### Pattern 2: Graceful Degradation

```javascript
async function generatePDFWithFallback(data, options = {}) {
  const strategies = [
    // Strategy 1: Full-featured Puppeteer
    () => this.generateWithPuppeteer(data, options),
    
    // Strategy 2: Lighter pdf-lib approach
    () => this.generateWithPDFLib(data, options),
    
    // Strategy 3: External service fallback
    () => this.generateWithExternalService(data, options)
  ];
  
  for (const strategy of strategies) {
    try {
      return await strategy();
    } catch (error) {
      console.warn(`PDF generation strategy failed:`, error.message);
      continue;
    }
  }
  
  throw new Error('All PDF generation strategies failed');
}
```

## Troubleshooting

### Common Issues và Solutions

**Issue: PDF files too large**

- Check image optimization pipeline
- Verify font subsetting is working
- Enable PDF compression
- Consider using vector graphics instead of raster images

**Issue: Slow generation time**

- Implement caching
- Use worker threads for CPU-intensive operations
- Pre-render templates
- Optimize image processing

**Issue: Memory exhaustion**

- Process PDFs in chunks
- Use streaming where possible
- Set appropriate memory limits
- Implement proper cleanup

**Issue: Fonts not rendering correctly**

- Verify font embedding
- Check CORS if loading external fonts
- Ensure font licenses allow embedding
- Use web-safe font fallbacks

## Examples

### Complete Production-Ready PDF Service

```javascript
class ProductionPDFService {
  constructor(options) {
    this.imagePipeline = new ImageOptimizationPipeline(options.images);
    this.fontService = new FontSubsettingService(options.fonts);
    this.templateCache = new TemplateCache(options.templates);
    this.cache = new MultiLevelCache(options.cache);
    this.signatureService = new PDFSignatureService(options.signing);
    this.asyncService = new AsyncPDFService(options.redis);
  }
  
  async generatePDF(request) {
    const { template, data, options } = request;
    
    // Check cache
    const cacheKey = this.generateCacheKey(template, data);
    const cached = await this.cache.get(cacheKey);
    if (cached && !options.regenerate) {
      return { ...cached, cached: true };
    }
    
    // Generate fresh
    const startTime = Date.now();
    
    // 1. Render template
    const html = await this.templateCache.renderTemplate(template, data);
    
    // 2. Optimize images
    const optimizedData = await this.imagePipeline.optimizeImagesForDocument(
      data.images || []
    );
    
    // 3. Optimize fonts
    const textContent = this.extractText(html);
    const optimizedFonts = await this.fontService.prepareFontsForDocument(
      textContent,
      data.fonts || {}
    );
    
    // 4. Generate PDF
    const pdfBuffer = await this.generatePDF(html, {
      fonts: optimizedFonts,
      images: optimizedData
    });
    
    // 5. Sign if requested
    if (options.sign) {
      pdfBuffer = await this.signatureService.signPDF(pdfBuffer, options.sign);
    }
    
    // 6. Cache result
    await this.cache.set(cacheKey, pdfBuffer, {
      template,
      generatedAt: new Date().toISOString()
    });
    
    return {
      buffer: pdfBuffer,
      size: pdfBuffer.length,
      generationTime: Date.now() - startTime,
      cached: false
    };
  }
  
  generateCacheKey(template, data) {
    return crypto.createHash('sha256')
      .update(JSON.stringify({ template, data }))
      .digest('hex')
      .substring(0, 16);
  }
  
  extractText(html) {
    return html.replace(/<[^>]*>/g, ' ');
  }
}
```

## References

- Adobe PDF Reference: https://www.adobe.com/devnet/pdf.html
- PDF/A Standard (ISO 19005): https://www.iso.org/standard/38920.html
- PDF/UA Standard (ISO 14289): https://www.pdfa.org/ua-standard/
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- Puppeteer PDF Options: https://pptr.dev/api/puppeteer.pdfoptions
- pdf-lib Documentation: https://pdf-lib.org/
- Fonttools Documentation: https://github.com/fonttools/fonttools
- Sharp Image Processing: https://sharp.pixelplumbing.com/
