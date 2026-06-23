---
title: "PDF Architecture - Kiến Trúc Xử Lý PDF"
description: "Comprehensive guide to PDF architecture including generation patterns, template engines, rendering pipelines, and library comparison (Puppeteer, Playwright, iText, pdf-lib, jsPDF, QuestPDF, IronPDF)"
tags: ["pdf", "architecture", "puppeteer", "playwright", "itext", "pdf-lib", "jsPDF", "questpdf", "ironpdf", "cursor-enterprise-framework"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# PDF Architecture - Kiến Trúc Xử Lý PDF

## Overview

Việc thiết kế một hệ thống xử lý PDF hiệu quả đòi hỏi hiểu biết sâu về các architectural patterns, strengths và weaknesses của different libraries, và cách integrate các components lại với nhau. Tài liệu này cung cấp một comprehensive overview của PDF architecture, từ high-level design patterns đến low-level implementation details của các libraries phổ biến nhất.

Trong enterprise environment, PDF processing không chỉ đơn thuần là "convert HTML to PDF". Một production-ready system cần handle authentication, caching, monitoring, error handling, và scalability. Việc choose right architecture và right tools cho use case cụ thể của bạn sẽ quyết định thành công của system.

## Purpose

Tài liệu này phục vụ như một architectural guide cho việc thiết kế và implement PDF processing systems. Nó giúp architects và developers hiểu các trade-offs giữa different approaches, select appropriate tools cho their requirements, và implement systems that are maintainable, scalable, và secure.

## Key Concepts

### 1. PDF Generation Approaches

Có ba main approaches cho PDF generation, mỗi cái có pros và cons:

**Approach 1: Template-Based HTML-to-PDF**

Đây là approach phổ biến nhất, đặc biệt trong web applications. HTML templates được rendered với data và sau đó converted sang PDF sử dụng browser rendering engine (Puppeteer, Playwright) hoặc dedicated converters (WeasyPrint, wkhtmltopdf).

**Approach 2: Programmatic PDF Generation**

Với approach này, PDF được constructed programmatically bằng cách sử dụng PDF library API (iText, pdf-lib, jsPDF). Developers specify exact positioning của elements, fonts, và graphics.

**Approach 3: Document Assembly**

Approach này sử dụng pre-designed PDF templates (forms) và populate chúng với data. Phù hợp cho documents có fixed layout như invoices, contracts.

### 2. Rendering Pipeline Architecture

Một well-designed PDF rendering pipeline bao gồm các stages sau:

1. **Input Processing**: Validate và sanitize input data
2. **Template Compilation**: Compile template với data
3. **Asset Preparation**: Optimize images, subset fonts
4. **PDF Rendering**: Convert HTML/document sang PDF
5. **Post-Processing**: Add metadata, signatures, compression
6. **Storage/Cache**: Store generated PDF

### 3. Scalability Considerations

PDF generation là CPU-intensive và memory-intensive. Architecture phải account cho:

- **Horizontal Scaling**: Multiple worker processes/instances
- **Resource Limits**: Memory limits per generation job
- **Queue Management**: Priority queues cho different PDF types
- **Timeout Handling**: Graceful degradation cho slow jobs

## Generation Patterns

### Pattern 1: Synchronous Generation

**Use Cases**: Small documents, low volume, simple templates

```javascript
// Synchronous PDF generation
app.post('/api/generate-pdf', async (req, res) => {
  const { template, data } = req.body;
  
  // 1. Render template
  const html = await renderTemplate(template, data);
  
  // 2. Generate PDF (blocks until complete)
  const pdfBuffer = await puppeteer.generatePDF(html);
  
  // 3. Return immediately
  res.setHeader('Content-Type', 'application/pdf');
  res.send(pdfBuffer);
});
```

**Pros**: Simple, easy to debug, good for single documents
**Cons**: Blocks server, poor scalability, high latency per request

### Pattern 2: Async Queue-Based Generation

**Use Cases**: High volume, large documents, complex generation

```javascript
// Async queue-based generation
const Bull = require('bull');
const pdfQueue = new Bull('pdf-generation', { redis: { port: 6379 } });

// Producer
app.post('/api/generate-pdf', async (req, res) => {
  const { template, data } = req.body;
  
  // Create job
  const job = await pdfQueue.add({ template, data }, {
    jobId: crypto.randomUUID()
  });
  
  // Return immediately with job ID
  res.json({ jobId: job.id, statusUrl: `/api/pdf/status/${job.id}` });
});

// Consumer (separate process/worker)
pdfQueue.process(async (job) => {
  const { template, data } = job.data;
  
  const html = await renderTemplate(template, data);
  const pdfBuffer = await puppeteer.generatePDF(html);
  
  // Store and notify
  await storePDF(job.id, pdfBuffer);
  await notifyUser(job.id);
  
  return { success: true, pdfUrl: `/api/pdf/download/${job.id}` };
});

// Status endpoint
app.get('/api/pdf/status/:jobId', async (req, res) => {
  const job = await pdfQueue.getJob(req.params.jobId);
  const state = await job.getState();
  
  res.json({
    jobId: job.id,
    status: state,
    progress: job.progress(),
    result: job.returnvalue
  });
});
```

**Pros**: Non-blocking, scalable, retry support, priority queuing
**Cons**: More complex, webhook/notification required

### Pattern 3: Pre-Rendering Pattern

**Use Cases**: Static or semi-static content, CDN distribution

```javascript
// Pre-render on content update
class PDFPreRenderer {
  constructor() {
    this.cache = new PDFCache();
    this.watch = new ContentWatcher();
  }
  
  async start() {
    // Watch for content changes
    this.watch.on('change', async (contentId) => {
      // Re-render affected PDFs in background
      await this.rebuildPDFsForContent(contentId);
    });
    
    // Initial render
    await this.renderAllPDFs();
  }
  
  async renderAllPDFs() {
    const contentList = await this.getAllContent();
    
    for (const content of contentList) {
      await this.renderAndCache(content);
    }
  }
  
  async renderAndCache(content) {
    const html = await this.renderTemplate(content.template, content.data);
    const pdfBuffer = await puppeteer.generatePDF(html);
    
    const cacheKey = this.getCacheKey(content);
    await this.cache.set(cacheKey, pdfBuffer);
  }
}

// Serve pre-rendered PDFs
app.get('/api/pdf/:contentId', async (req, res) => {
  const cacheKey = req.params.contentId;
  const pdfBuffer = await pdfCache.get(cacheKey);
  
  res.setHeader('Content-Type', 'application/pdf');
  res.send(pdfBuffer);
});
```

**Pros**: Instant response, CDN-cacheable, no generation latency
**Cons**: Wasted resources for unaccessed content, stale cache handling

### Pattern 4: Hybrid Pattern

**Use Cases**: Mix of static and dynamic content

```javascript
// Hybrid: Pre-render static parts, render dynamic on-demand
class HybridPDFService {
  async generateHybridPDF(contentId, dynamicData) {
    // Get pre-rendered static content
    const staticPDF = await this.staticCache.get(contentId);
    const staticDoc = await PDFDocument.load(staticPDF);
    
    // Create new document with dynamic content
    const finalDoc = await PDFDocument.create();
    
    // Copy static pages
    const staticPages = await finalDoc.copyPages(
      staticDoc, 
      staticDoc.getPageIndices()
    );
    staticPages.forEach(page => finalDoc.addPage(page));
    
    // Add dynamic pages
    const dynamicHtml = await this.renderDynamicContent(dynamicData);
    const dynamicPdf = await puppeteer.generatePDF(dynamicHtml);
    const dynamicDoc = await PDFDocument.load(dynamicPdf);
    const dynamicPages = await finalDoc.copyPages(
      dynamicDoc,
      dynamicDoc.getPageIndices()
    );
    dynamicPages.forEach(page => finalDoc.addPage(page));
    
    return await finalDoc.save();
  }
}
```

## Template Engines

### Comparison of Template Engines

| Engine | Syntax | Features | Performance | Ecosystem |
|--------|--------|----------|------------|-----------|
| Handlebars | `{{variable}}` | Partial support, helpers | Fast | Large |
| EJS | `<%= variable %>` | Simple, inline JS | Fast | Large |
| Pug | Indent-based | Clean, mixins | Medium | Medium |
| Nunjucks | `{{ variable }}` | Filters, extensions | Fast | Large |
| Mustache | `{{variable}}` | Logic-less | Very Fast | Medium |

### Template Service Architecture

```javascript
class TemplateEngineService {
  constructor(options = {}) {
    this.engine = options.engine || 'handlebars';
    this.cache = new LRUCache({ max: 100, ttl: 3600000 });
    this.partialsDir = options.partialsDir;
    this.helpers = options.helpers || {};
    
    this.initializeEngine();
  }
  
  initializeEngine() {
    switch (this.engine) {
      case 'handlebars':
        this.setupHandlebars();
        break;
      case 'ejs':
        this.setupEJS();
        break;
      case 'pug':
        this.setupPug();
        break;
    }
  }
  
  setupHandlebars() {
    const Handlebars = require('handlebars');
    
    // Register helpers
    Object.entries(this.helpers).forEach(([name, fn]) => {
      Handlebars.registerHelper(name, fn);
    });
    
    // Register partials
    if (this.partialsDir) {
      const partials = fs.readdirSync(this.partialsDir);
      partials.forEach(file => {
        if (file.endsWith('.hbs')) {
          const name = path.basename(file, '.hbs');
          const source = fs.readFileSync(
            path.join(this.partialsDir, file), 'utf8'
          );
          Handlebars.registerPartial(name, source);
        }
      });
    }
    
    this.engine = Handlebars;
  }
  
  async render(templateName, data) {
    const cacheKey = `${this.engine}:${templateName}:${JSON.stringify(data)}`;
    
    // Check cache
    const cached = this.cache.get(cacheKey);
    if (cached && !data._nocache) {
      return cached;
    }
    
    // Get template
    const template = await this.getTemplate(templateName);
    
    // Render
    const result = template(data);
    
    // Cache
    this.cache.set(cacheKey, result);
    
    return result;
  }
  
  async getTemplate(name) {
    const templatePath = path.join(this.templatesDir, `${name}.hbs`);
    const source = await fs.readFile(templatePath, 'utf8');
    
    if (this.engine.compile) {
      return this.engine.compile(source);
    }
    return this.engine(source);
  }
}
```

## Rendering Pipelines

### Standard Rendering Pipeline

```javascript
class PDFRenderingPipeline {
  constructor(options = {}) {
    this.stages = options.stages || [
      'inputValidation',
      'dataEnrichment',
      'assetOptimization',
      'templateRendering',
      'pdfGeneration',
      'postProcessing',
      'caching'
    ];
    
    this.performanceLogger = options.performanceLogger;
  }
  
  async execute(input, context = {}) {
    const startTime = Date.now();
    let data = { ...input };
    const timings = {};
    
    for (const stage of this.stages) {
      const stageStart = Date.now();
      
      try {
        data = await this.executeStage(stage, data, context);
        timings[stage] = Date.now() - stageStart;
        
        this.performanceLogger?.record(stage, timings[stage]);
      } catch (error) {
        throw new PipelineError(stage, error);
      }
    }
    
    this.performanceLogger?.record('total', Date.now() - startTime);
    
    return {
      result: data.output,
      timings,
      metadata: {
        executedStages: this.stages,
        context
      }
    };
  }
  
  async executeStage(stageName, data, context) {
    const stage = this[`stage_${stageName}`];
    if (!stage) {
      throw new Error(`Unknown stage: ${stageName}`);
    }
    return await stage.call(this, data, context);
  }
  
  // Stage: Input Validation
  async stage_inputValidation(data, context) {
    const { error, value } = pdfInputSchema.validate(data);
    if (error) {
      throw new ValidationError(error.message);
    }
    return { ...data, ...value };
  }
  
  // Stage: Data Enrichment
  async stage_dataEnrichment(data, context) {
    // Add computed fields
    data.computed = {
      total: this.calculateTotal(data.items),
      formattedDate: this.formatDate(data.date),
      barcode: this.generateBarcode(data.id)
    };
    return data;
  }
  
  // Stage: Asset Optimization
  async stage_assetOptimization(data, context) {
    if (data.images) {
      data.optimizedImages = await Promise.all(
        data.images.map(img => this.optimizeImage(img))
      );
    }
    return data;
  }
  
  // Stage: Template Rendering
  async stage_templateRendering(data, context) {
    const template = await templateService.getTemplate(data.template);
    data.html = template(data);
    return data;
  }
  
  // Stage: PDF Generation
  async stage_pdfGeneration(data, context) {
    data.pdfBuffer = await puppeteerService.generate(data.html, {
      format: data.format || 'A4',
      printBackground: true,
      margin: data.margin
    });
    return data;
  }
  
  // Stage: Post Processing
  async stage_postProcessing(data, context) {
    // Add metadata
    const pdfDoc = await PDFDocument.load(data.pdfBuffer);
    pdfDoc.setTitle(data.title);
    pdfDoc.setAuthor(data.author);
    data.output = await pdfDoc.save();
    return data;
  }
  
  // Stage: Caching
  async stage_caching(data, context) {
    const cacheKey = this.generateCacheKey(data);
    await cacheService.set(cacheKey, data.output);
    return data;
  }
}
```

### Parallel Processing Pipeline

```javascript
class ParallelPDFPipeline {
  async generateComplexDocument(sections) {
    // Process sections in parallel
    const sectionPromises = sections.map(section => 
      this.generateSection(section)
    );
    
    const generatedSections = await Promise.all(sectionPromises);
    
    // Merge sections into single PDF
    const mergedPdf = await this.mergePDFs(generatedSections);
    
    // Add table of contents
    const finalPdf = await this.addTableOfContents(mergedPdf, sections);
    
    return finalPdf;
  }
  
  async generateSection(section) {
    // Each section can be generated independently
    const html = await this.renderSection(section);
    return await puppeteerService.generate(html);
  }
  
  async mergePDFs(pdfBuffers) {
    const mergedDoc = await PDFDocument.create();
    
    for (const buffer of pdfBuffers) {
      const doc = await PDFDocument.load(buffer);
      const pages = await mergedDoc.copyPages(
        doc,
        doc.getPageIndices()
      );
      pages.forEach(page => mergedDoc.addPage(page));
    }
    
    return await mergedDoc.save();
  }
}
```

## Library Comparison

### Library Overview

| Library | Language | Approach | Performance | Pros | Cons |
|---------|----------|----------|------------|------|------|
| Puppeteer | JavaScript | HTML-to-PDF | Medium | Full CSS support, screenshots | Large memory, slow startup |
| Playwright | JavaScript | HTML-to-PDF | Medium | Cross-browser, modern | Similar to Puppeteer |
| pdf-lib | JavaScript | Programmatic | Fast | No native deps, rich API | No CSS/HTML rendering |
| jsPDF | JavaScript | Programmatic | Fast | Lightweight, client-side | Limited features |
| iText | JavaScript/Java | Hybrid | Fast | Enterprise features, signing | License cost |
| QuestPDF | C# | Programmatic | Very Fast | Fluent API, templates | .NET only |
| IronPDF | C#/.NET | HTML-to-PDF | Medium | .NET integration | License cost |

### Detailed Library Analysis

#### 1. Puppeteer

**Best For**: Complex HTML/CSS layouts, web-style documents

```javascript
// Puppeteer Setup
const puppeteer = require('puppeteer');

class PuppeteerPDFService {
  constructor(options = {}) {
    this.launchOptions = {
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--disable-gpu',
        '--max-old-space-size=512'
      ]
    };
    this.browser = null;
  }
  
  async initialize() {
    if (!this.browser) {
      this.browser = await puppeteer.launch(this.launchOptions);
    }
    return this.browser;
  }
  
  async generatePDF(html, options = {}) {
    const browser = await this.initialize();
    const page = await browser.newPage();
    
    try {
      await page.setContent(html, {
        waitUntil: 'networkidle0',
        timeout: 30000
      });
      
      // Wait for fonts to load
      await page.evaluateHandle('document.fonts.ready');
      
      const pdfBuffer = await page.pdf({
        format: options.format || 'A4',
        landscape: options.landscape || false,
        printBackground: options.printBackground !== false,
        margin: options.margin || {
          top: '20px',
          right: '20px',
          bottom: '20px',
          left: '20px'
        },
        displayHeaderFooter: options.headerFooter || false,
        headerTemplate: options.headerTemplate,
        footerTemplate: options.footerTemplate,
        scale: options.scale || 1,
        preferCSSPageSize: options.preferCSSPageSize || false
      });
      
      return Buffer.from(pdfBuffer);
      
    } finally {
      await page.close();
    }
  }
  
  async generateMultiplePDFs(requests) {
    const browser = await this.initialize();
    
    const results = await Promise.all(
      requests.map(async ({ html, options }) => {
        const page = await browser.newPage();
        try {
          await page.setContent(html, { waitUntil: 'networkidle0' });
          const pdf = await page.pdf(options);
          return { success: true, pdf: Buffer.from(pdf) };
        } catch (error) {
          return { success: false, error: error.message };
        } finally {
          await page.close();
        }
      })
    );
    
    return results;
  }
  
  async close() {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
    }
  }
}
```

**Performance Characteristics**:

- Cold start: 2-5 seconds (browser launch)
- PDF generation: 500ms-2s per page
- Memory: 150-300MB per page
- Concurrent: 2-4 per GB RAM

#### 2. Playwright

**Best For**: Cross-browser testing, modern web features

```javascript
// Playwright Setup
const { chromium } = require('playwright');

class PlaywrightPDFService {
  constructor(options = {}) {
    this.options = options;
  }
  
  async generatePDF(html, options = {}) {
    const browser = await chromium.launch({
      headless: true,
      args: ['--no-sandbox']
    });
    
    try {
      const page = await browser.newPage();
      
      await page.setContent(html, {
        waitUntil: 'networkidle',
        timeout: 30000
      });
      
      // Wait for fonts
      await page.evaluate(() => document.fonts.ready);
      
      const pdfBuffer = await page.pdf({
        format: options.format || 'A4',
        landscape: options.landscape || false,
        printBackground: options.printBackground !== false,
        margin: options.margin || {
          top: '20px',
          right: '20px',
          bottom: '20px',
          left: '20px'
        },
        displayHeaderFooter: options.displayHeaderFooter || false,
        headerTemplate: options.headerTemplate,
        footerTemplate: options.footerTemplate
      });
      
      return Buffer.from(pdfBuffer);
      
    } finally {
      await browser.close();
    }
  }
  
  // Playwright advantage: Better network interception
  async generatePDFWithNetworkMocking(html, mocks, options = {}) {
    const browser = await chromium.launch({ headless: true });
    
    try {
      const page = await browser.newPage();
      
      // Mock network requests
      await page.route('**/*', (route) => {
        const url = route.request().url();
        const mock = mocks.find(m => url.match(m.pattern));
        
        if (mock) {
          route.fulfill({
            status: mock.status || 200,
            contentType: mock.contentType || 'application/pdf',
            body: mock.body
          });
        } else {
          route.continue();
        }
      });
      
      await page.setContent(html);
      return await this.generatePDF(html, options);
      
    } finally {
      await browser.close();
    }
  }
}
```

#### 3. pdf-lib

**Best For**: PDF manipulation, programmatic creation, no browser needed

```javascript
// pdf-lib Setup
const { PDFDocument, rgb, StandardFonts, PDFPage } = require('pdf-lib');

class PDFLibService {
  async createPDF(data) {
    const pdfDoc = await PDFDocument.create();
    
    // Embed fonts
    const helvetica = await pdfDoc.embedFont(StandardFonts.Helvetica);
    const boldHelvetica = await pdfDoc.embedFont(StandardFonts.HelveticaBold);
    
    // Create pages
    let page = pdfDoc.addPage([595.28, 841.89]); // A4
    
    const fontSize = 12;
    const lineHeight = fontSize * 1.4;
    let y = 800;
    
    // Title
    page.drawText(data.title || 'Document', {
      x: 50,
      y: y,
      size: 24,
      font: boldHelvetica,
      color: rgb(0, 0, 0)
    });
    
    y -= lineHeight * 2;
    
    // Content
    const content = data.content || [];
    for (const line of content) {
      // Check if need new page
      if (y < 100) {
        page = pdfDoc.addPage([595.28, 841.89]);
        y = 800;
      }
      
      if (line.type === 'heading') {
        page.drawText(line.text, {
          x: 50,
          y: y,
          size: 18,
          font: boldHelvetica,
          color: rgb(0, 0, 0)
        });
        y -= lineHeight * 1.5;
      } else {
        page.drawText(line.text, {
          x: 50,
          y: y,
          size: fontSize,
          font: helvetica,
          color: rgb(0, 0, 0)
        });
        y -= lineHeight;
      }
    }
    
    // Set metadata
    pdfDoc.setTitle(data.title || 'Document');
    pdfDoc.setAuthor(data.author || 'System');
    pdfDoc.setCreator('PDF Generator');
    pdfDoc.setCreationDate(new Date());
    
    return await pdfDoc.save();
  }
  
  async mergePDFs(pdfBuffers) {
    const mergedDoc = await PDFDocument.create();
    
    for (const buffer of pdfBuffers) {
      const doc = await PDFDocument.load(buffer);
      const pages = await mergedDoc.copyPages(
        doc,
        doc.getPageIndices()
      );
      pages.forEach(page => mergedDoc.addPage(page));
    }
    
    return await mergedDoc.save();
  }
  
  async addWatermark(pdfBuffer, text) {
    const doc = await PDFDocument.load(pdfBuffer);
    const helvetica = await doc.embedFont(StandardFonts.Helvetica);
    
    const pages = doc.getPages();
    const watermarkText = text || 'CONFIDENTIAL';
    
    for (const page of pages) {
      const { width, height } = page.getSize();
      
      page.drawText(watermarkText, {
        x: width / 4,
        y: height / 2,
        size: 60,
        font: helvetica,
        color: rgb(0.8, 0.8, 0.8),
        rotate: degrees(45)
      });
    }
    
    return await doc.save();
  }
}
```

**Performance Characteristics**:

- Cold start: < 100ms
- PDF generation: 50-200ms per page
- Memory: 10-50MB per operation
- Concurrent: 50-100 per GB RAM

#### 4. iText (iTextSharp/iText7)

**Best For**: Enterprise PDF processing, digital signatures, forms

```javascript
// iText7 Setup
const { PdfDocument, PdfWriter, PdfReader, PdfPage, 
        Document, Paragraph, TextElement, FontProgramFactory,
        DeviceNColor } = require('@itext/itext7-core');

class ITextPDFService {
  constructor(options = {}) {
    this.licenseKey = options.licenseKey;
  }
  
  async createPDF(data) {
    // Create PDF writer
    const writer = new PdfWriter(new MemoryStream());
    const reader = new PdfReader(new MemoryStream());
    const pdfDoc = new PdfDocument(reader, writer);
    
    // Create document
    const doc = new Document(pdfDoc);
    
    // Add content
    doc.add(new Paragraph(data.title || 'Document')
      .setFontSize(24)
      .setBold());
    
    if (data.content) {
      for (const item of data.content) {
        doc.add(new Paragraph(item.text));
      }
    }
    
    // Close and get bytes
    doc.close();
    
    const memoryStream = writer.getOutputStream();
    return memoryStream.toBuffer();
  }
  
  async addDigitalSignature(pdfBuffer, signatureData) {
    const reader = new PdfReader(new MemoryStream(pdfBuffer));
    const writer = new PdfWriter(new MemoryStream());
    const pdfDoc = new PdfDocument(reader, writer);
    
    // Create signature field
    const signatureField = new PdfFormField(pdfDoc.getLastPage(), 
      PdfArray.fromArray([100, 100, 250, 150], pdfDoc));
    
    // Sign
    // ... (complex signing logic)
    
    pdfDoc.close();
    
    const memoryStream = writer.getOutputStream();
    return memoryStream.toBuffer();
  }
  
  async fillForm(pdfBuffer, formData) {
    const reader = new PdfReader(new MemoryStream(pdfBuffer));
    const writer = new PdfWriter(new MemoryStream());
    const pdfDoc = new PdfDocument(reader, writer);
    
    const form = pdfDoc.getForm();
    
    // Fill form fields
    for (const [fieldName, value] of Object.entries(formData)) {
      const field = form.getField(fieldName);
      if (field) {
        field.setValue(value);
      }
    }
    
    pdfDoc.close();
    
    const memoryStream = writer.getOutputStream();
    return memoryStream.toBuffer();
  }
}
```

#### 5. jsPDF

**Best For**: Client-side PDF generation, simple documents

```javascript
// jsPDF Setup
const { jsPDF } = require('jspdf');

class JSPDFService {
  async createPDF(data) {
    const doc = new jsPDF({
      orientation: data.orientation || 'portrait',
      unit: 'mm',
      format: data.format || 'a4'
    });
    
    let y = 20;
    
    // Title
    doc.setFontSize(24);
    doc.setFont('helvetica', 'bold');
    doc.text(data.title || 'Document', 20, y);
    y += 15;
    
    // Content
    doc.setFontSize(12);
    doc.setFont('helvetica', 'normal');
    
    const content = data.content || [];
    for (const item of content) {
      if (item.type === 'heading') {
        doc.setFontSize(16);
        doc.setFont('helvetica', 'bold');
        y += 5;
      } else {
        doc.setFontSize(12);
        doc.setFont('helvetica', 'normal');
      }
      
      const lines = doc.splitTextToSize(item.text, 170);
      doc.text(lines, 20, y);
      y += lines.length * 6 + 5;
      
      // Check for page break
      if (y > 270) {
        doc.addPage();
        y = 20;
      }
    }
    
    // Add footer
    const pageCount = doc.getNumberOfPages();
    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i);
      doc.setFontSize(10);
      doc.text(
        `Page ${i} of ${pageCount}`,
        doc.internal.pageSize.width / 2,
        doc.internal.pageSize.height - 10,
        { align: 'center' }
      );
    }
    
    return doc.output('arraybuffer');
  }
  
  async addImage(pdfBuffer, imagePath, x, y, width, height) {
    const doc = new jsPDF({ unit: 'mm' });
    
    // Load and add image
    const imageData = fs.readFileSync(imagePath);
    const imageBase64 = imageData.toString('base64');
    const ext = path.extname(imagePath).slice(1);
    
    doc.addImage(imageBase64, ext.toUpperCase(), x, y, width, height);
    
    return doc.output('arraybuffer');
  }
}
```

#### 6. QuestPDF (C#/.NET)

**Best For**: Complex layout, Fluent API, .NET applications

```csharp
// QuestPDF Setup
using QuestPDF.Fluent;
using QuestPDF.Helpers;
using QuestPDF.Infrastructure;

public class QuestPDFService
{
    public byte[] GenerateInvoice(InvoiceData data)
    {
        return Document.Create(container =>
        {
            container.Page(page =>
            {
                page.Size(PageSizes.A4);
                page.Margin(2, Unit.Centimetre);
                page.PageColor(Colors.White);
                page.DefaultTextStyle(x => x.FontSize(12));

                page.Header()
                    .Text("Invoice")
                    .SemiBold().FontSize(24).FontColor(Colors.Blue.Medium);

                page.Content()
                    .PaddingVertical(1, Unit.Centimetre)
                    .Column(column =>
                    {
                        column.Spacing(20);

                        column.Item().Text($"Invoice #: {data.InvoiceNumber}");
                        column.Item().Text($"Date: {data.Date:d}");
                        column.Item().Text($"Customer: {data.CustomerName}");

                        column.Item().Table(table =>
                        {
                            table.ColumnsDefinition(columns =>
                            {
                                columns.RelativeColumn(3);
                                columns.RelativeColumn();
                                columns.RelativeColumn();
                            });

                            table.Header(header =>
                            {
                                header.Cell().Background(Colors.Grey.Lighten2)
                                    .Padding(5).Text("Item");
                                header.Cell().Background(Colors.Grey.Lighten2)
                                    .Padding(5).AlignRight().Text("Qty");
                                header.Cell().Background(Colors.Grey.Lighten2)
                                    .Padding(5).AlignRight().Text("Amount");
                            });

                            foreach (var item in data.Items)
                            {
                                table.Cell().BorderBottom(1).BorderColor(Colors.Grey.Lighten2)
                                    .Padding(5).Text(item.Name);
                                table.Cell().BorderBottom(1).BorderColor(Colors.Grey.Lighten2)
                                    .Padding(5).AlignRight().Text(item.Quantity.ToString());
                                table.Cell().BorderBottom(1).BorderColor(Colors.Grey.Lighten2)
                                    .Padding(5).AlignRight().Text($"${item.Amount:N2}");
                            }
                        });

                        column.Item().AlignRight()
                            .Text($"Total: ${data.Total:N2}").FontSize(16).Bold();
                    });

                page.Footer()
                    .AlignCenter()
                    .Text(x =>
                    {
                        x.Span("Page ");
                        x.CurrentPageNumber();
                        x.Span(" of ");
                        x.TotalPages();
                    });
            });
        }).GeneratePdf();
    }
}
```

#### 7. IronPDF

**Best For**: .NET applications, HTML-to-PDF,Chrome-based rendering

```csharp
// IronPDF Setup
using IronPdf;

public class IronPDFService
{
    public byte[] GeneratePDF(string html)
    {
        var renderer = new ChromePdfRenderer();
        
        renderer.RenderingOptions.PaperSize = PdfPaperSize.A4;
        renderer.RenderingOptions.MarginTop = 20;
        renderer.RenderingOptions.MarginBottom = 20;
        renderer.RenderingOptions.CssMediaType = IronPdf.Imaging.CssMediaType.Print;
        
        var pdf = renderer.RenderHtmlAsPdf(html);
        return pdf.BinaryData;
    }
    
    public byte[] GenerateFromUrl(string url)
    {
        var renderer = new ChromePdfRenderer();
        var pdf = renderer.RenderUrlAsPdf(url);
        return pdf.BinaryData;
    }
    
    public async Task<byte[]> SignAndWatermark(byte[] pdfData)
    {
        var doc = PdfDocument.FromBinary(pdfData);
        
        // Add watermark
        doc.Watermark.AllPages.AddText("CONFIDENTIAL", 
            new IronPdf.Imaging.WatermarkOptions
            {
                Angle = 45,
                Opacity = 30,
                FontSize = 72
            });
        
        // Save with digital signature
        doc.ApplySignature(new IronPdf.Signature("certificate.pfx", "password"));
        
        return doc.BinaryData;
    }
}
```

## Architecture Diagrams

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Request                           │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway / Load Balancer                 │
│                    (Rate Limiting, Auth, Routing)               │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Application Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ PDF Generator│  │ PDF Merger   │  │ PDF Template Manager  │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
        ┌───────────────────┐ ┌──────────────┐ ┌──────────────┐
        │ Template Engine    │ │ Asset Opt.   │ │ Cache Layer  │
        │ (Handlebars/EJS)  │ │ (Sharp)     │ │ (Redis/S3)  │
        └───────────────────┘ └──────────────┘ └──────────────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    ▼
        ┌───────────────────────────────────────────────────────────┐
        │                   Rendering Layer                         │
        │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────┐  │
        │  │Puppeteer│  │pdf-lib  │  │ iText   │  │ External Svc│  │
        │  └─────────┘  └─────────┘  └─────────┘  └─────────────┘  │
        └───────────────────────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────────────────────┐
        │                   Storage Layer                            │
        │  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐  │
        │  │ S3 / Blob    │  │ Redis Cache  │  │ CDN            │  │
        │  └──────────────┘  └──────────────┘  └────────────────┘  │
        └───────────────────────────────────────────────────────────┘
```

### Component Architecture

```yaml
Components:
  API Gateway:
    - Authentication/Authorization
    - Rate Limiting
    - Request Validation
    - Load Balancing
  
  PDF Service:
    - Template Rendering
    - PDF Generation
    - Post Processing
    - Digital Signatures
  
  Asset Optimizer:
    - Image Compression
    - Font Subsetting
    - Asset Caching
  
  Cache Service:
    - Redis (metadata)
    - S3 (PDFs)
    - CDN (distribution)
  
  Worker Queue:
    - Bull/BullMQ
    - Priority Queues
    - Retry Logic
    - Dead Letter Queue
```

## Troubleshooting

### Common Architecture Issues

**Issue: Memory Exhaustion with Puppeteer**

Solution: Implement connection pooling và limit concurrent browsers:

```javascript
class ManagedBrowserPool {
  constructor(maxBrowsers = 2) {
    this.pool = [];
    this.maxBrowsers = maxBrowsers;
    this.queue = [];
  }
  
  async acquire() {
    if (this.pool.length > 0) {
      return this.pool.pop();
    }
    
    if (this.queue.length >= this.maxBrowsers) {
      return new Promise(resolve => {
        this.queue.push(resolve);
      });
    }
    
    const browser = await puppeteer.launch({
      args: ['--max-old-space-size=256']
    });
    return browser;
  }
  
  async release(browser) {
    if (this.queue.length > 0) {
      const waiter = this.queue.shift();
      waiter(browser);
    } else {
      this.pool.push(browser);
    }
  }
}
```

**Issue: Slow Template Compilation**

Solution: Cache compiled templates:

```javascript
const templateCache = new Map();

async function getCompiledTemplate(name) {
  if (templateCache.has(name)) {
    return templateCache.get(name);
  }
  
  const source = await fs.readFile(`./templates/${name}.hbs`);
  const compiled = Handlebars.compile(source);
  
  templateCache.set(name, compiled);
  return compiled;
}
```

## References

- Puppeteer GitHub: https://github.com/puppeteer/puppeteer
- Playwright Documentation: https://playwright.dev/
- pdf-lib Documentation: https://pdf-lib.org/
- jsPDF Documentation: https://artskydj.github.io/jsPDF/
- iText Documentation: https://itextpdf.com/
- QuestPDF Documentation: https://www.questpdf.com/
- IronPDF Documentation: https://ironpdf.com/
