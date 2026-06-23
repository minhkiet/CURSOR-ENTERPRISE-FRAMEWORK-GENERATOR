---
title: "PDF Decision Tree - Cây Quyết Định PDF"
description: "Comprehensive decision tree for PDF implementation choices including server-side vs client-side, library selection, template approach, and compression strategy"
tags: ["pdf", "decision-tree", "architecture", "technology-selection", "cursor-enterprise-framework"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# PDF Decision Tree - Cây Quyết Định PDF

## Overview

Việc implement PDF functionality trong một hệ thống enterprise đòi hỏi nhiều quyết định quan trọng, từ nơi generate PDFs (server-side vs client-side) đến việc chọn library phù hợp và xác định template strategy. Tài liệu này cung cấp một comprehensive decision tree để hướng dẫn architects và developers through these decisions, với các considerations và trade-offs được explained ở mỗi bước.

Mỗi decision point được trình bày với câu hỏi cần trả lời, các options có sẵn, và guidance về cách make the choice dựa trên specific requirements. Flowcharts được provided ở dạng text-based để visualize decision paths, và examples được include để illustrate real-world applications của mỗi approach.

## Purpose

Decision tree này giúp đội ngũ phát triển make informed decisions khi architecting PDF systems. Thay vì phải research từ đầu cho mỗi project, developers có thể follow decision tree này để reach appropriate conclusions dựa trên their specific constraints và requirements.

## Decision Framework

### Overall Decision Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      START: PDF Requirements                     │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ Q1: Where should PDF generation happen?                          │
│     (Server-side, Client-side, Hybrid)                          │
└─────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              Server-side      Client-side      Hybrid
                    │               │               │
                    ▼               ▼               ▼
┌───────────────────────┐ ┌───────────────┐ ┌─────────────────────┐
│ Q2: Choose library?   │ │ Q2: Browser  │ │ Q2: When to use    │
│ (Puppeteer, iText,   │ │ capabilities │ │ each approach?      │
│  pdf-lib, etc.)      │ │ available?   │ │                     │
└───────────────────────┘ └───────────────┘ └─────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ Q3: Template approach?                                          │
│     (HTML-to-PDF, Programmatic, Form-filling)                  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              HTML-to-PDF      Programmatic      Form-filling
                    │               │               │
                    ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────────┐
│ Q4: Performance optimization strategy?                          │
│     (Caching, Async, Pre-rendering, Compression)                │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ Q5: Additional features needed?                                  │
│     (Signatures, Encryption, Accessibility)                     │
└─────────────────────────────────────────────────────────────────┘
```

## Decision 1: Server-Side vs Client-Side

### The Question

**Where should PDF generation happen in your architecture?**

### Considerations

| Factor | Server-Side | Client-Side |
|--------|-------------|-------------|
| Performance | Dedicated CPU, consistent | Depends on client machine |
| Reliability | High, controlled environment | Variable based on browser |
| Security | Better control over sensitive data | Data leaves client browser |
| Cost | Server compute costs | Client device resources |
| Complexity | More infrastructure | Simpler deployment |
| Offline capability | Requires network | Can work offline |

### Decision Flowchart

```
START: Where to generate PDFs?
│
├─► Is the PDF content sensitive/confidential?
│   │
│   ├─► YES ─► Server-Side
│   │         Rationale: Better security, data doesn't leave server
│   │
│   └─► NO ─► Does PDF need access to backend data/APIs?
│               │
│               ├─► YES ─► Server-Side
│               │         Rationale: Direct data access, single source of truth
│               │
│               └─► NO ─► Is it simple/static documents?
│                           │
│                           ├─► YES ─► Client-Side
│                           │         Rationale: Reduces server load, simple implementation
│                           │
│                           └─► NO ─► Does volume need scaling?
│                                       │
│                                       ├─► YES ─► Server-Side
│                                       │         Rationale: Centralized scaling
│                                       │
│                                       └─► NO ─► Hybrid
│                                                 Rationale: Best of both worlds
```

### Recommendations by Use Case

#### Use Case: Invoice Generation

**Recommendation**: Server-Side

**Rationale**:

- Invoices contain sensitive pricing and customer data
- Backend has direct access to database
- Consistent rendering across all customers
- Caching improves performance for repeated invoices

```javascript
// Server-side invoice generation
app.post('/api/invoices/:id/pdf', async (req, res) => {
  const invoice = await getInvoiceFromDB(req.params.id);
  
  // Generate on server - data never leaves secure environment
  const pdfBuffer = await pdfService.generateInvoice(invoice);
  
  res.setHeader('Content-Type', 'application/pdf');
  res.send(pdfBuffer);
});
```

#### Use Case: Report Export (User-Generated)

**Recommendation**: Client-Side (for simple reports), Server-Side (for complex)

**Rationale**:

- User controls when to export
- Server load reduced
- But for complex reports requiring database joins, server-side is better

```javascript
// Client-side report export
async function exportReport() {
  // Gather data client-side
  const reportData = await fetchReportData();
  
  // Generate in browser
  const pdf = await jsPDFService.generate(reportData);
  
  // Download
  downloadPDF(pdf, 'report.pdf');
}
```

#### Use Case: Document Signing

**Recommendation**: Server-Side

**Rationale**:

- Private keys must be kept secure on server
- Certificate management is complex for clients
- Compliance requirements usually mandate server-side signing

```javascript
// Server-side signing
async function signDocument(pdfBuffer) {
  // Sign with server-held certificate
  const signedPdf = await signatureService.sign(pdfBuffer, {
    certificate: process.env.SIGNING_CERT,
    privateKey: process.env.SIGNING_KEY
  });
  
  return signedPdf;
}
```

## Decision 2: Library Selection

### The Question

**Which PDF library should you use?**

### Decision Flowchart by Approach

```
START: Choose PDF Library
│
├─► Is your primary need HTML-to-PDF conversion?
│   │
│   ├─► YES ─► Is browser compatibility important?
│   │         │
│   │         ├─► YES ─► Playwright
│   │         │         Rationale: Best cross-browser support, modern features
│   │         │
│   │         └─► NO ─► Puppeteer
│   │                   Rationale: Chrome-only, good for Node.js, widely used
│   │
│   └─► NO ─► Do you need to manipulate existing PDFs?
│               │
│               ├─► YES ─► Is it Node.js environment?
│               │         │
│               │         ├─► YES ─► pdf-lib
│               │         │         Rationale: Pure JavaScript, no native deps
│               │         │
│               │         └─► NO ─► iText
│               │                   Rationale: Mature library, Java/.NET support
│               │
│               └─► NO ─► Do you need to create from scratch?
│                           │
│                           ├─► YES ─► Is complexity high?
│                           │         │
│                           │         ├─► YES ─► QuestPDF (C#) or IronPDF
│                           │         │         Rationale: Rich API, templates
│                           │         │
│                           │         └─► NO ─► jsPDF
│                           │                   Rationale: Simple, lightweight
│                           │
│                           └─► NO ─► Form filling?
│                                       │
│                                       └─► pdftk (CLI) or iText
│                                                 Rationale: Form field manipulation
```

### Library Comparison Matrix

| Library | Language | Approach | File Size | Memory | Best For |
|---------|----------|----------|-----------|--------|----------|
| Puppeteer | JavaScript | HTML-to-PDF | Medium | High | Web-style docs |
| Playwright | JavaScript | HTML-to-PDF | Medium | High | Cross-browser |
| pdf-lib | JavaScript | Programmatic | Small | Low | Manipulation |
| jsPDF | JavaScript | Programmatic | Small | Low | Simple docs |
| iText | Java/JavaScript | Hybrid | Variable | Medium | Enterprise |
| QuestPDF | C# | Programmatic | Small | Low | Complex layouts |
| IronPDF | C#/.NET | HTML-to-PDF | Medium | Medium | .NET apps |

### Decision by Requirements

#### Requirement: Complex CSS Styling

**Recommendation**: Puppeteer or Playwright

**Rationale**: Full CSS support with modern layout engine

```javascript
// Puppeteer for complex CSS
async function generateStyledPDF(html) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // Full CSS Grid, Flexbox, custom fonts support
  await page.setContent(html, { waitUntil: 'networkidle0' });
  
  return await page.pdf({
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true
  });
}
```

#### Requirement: High Volume, Low Latency

**Recommendation**: pdf-lib for manipulation, pre-rendering for static content

**Rationale**: No browser overhead, fast execution

```javascript
// pdf-lib for high-volume manipulation
async function stampManyPDFs(buffers, watermark) {
  const promises = buffers.map(buffer => 
    pdfLibService.addWatermark(buffer, watermark)
  );
  
  return Promise.all(promises); // Parallel processing
}
```

#### Requirement: Enterprise Features (Signatures, Forms)

**Recommendation**: iText (with license) or pdf-lib + custom implementation

**Rationale**: Mature enterprise features, though iText has licensing costs

```javascript
// iText for enterprise features
const pdfDoc = await iTextService.createPDF();
await pdfDoc.sign(document, options);
await pdfDoc.fillForm(data);
await pdfDoc.encrypt(passwords);
```

#### Requirement: .NET Environment

**Recommendation**: QuestPDF or IronPDF

**Rationale**: Native .NET libraries with excellent APIs

```csharp
// QuestPDF for .NET
public byte[] GenerateInvoice(InvoiceData data) {
    return Document.Create(container => {
        container.Page(page => {
            page.Content().Column(column => {
                column.Item().Text(data.Title);
                column.Item().Table(table => { /* ... */ });
            });
        });
    }).GeneratePdf();
}
```

## Decision 3: Template Approach

### The Question

**How should you structure PDF content generation?**

### Decision Flowchart

```
START: Choose Template Approach
│
├─► Is the document primarily web-based content (HTML/CSS)?
│   │
│   ├─► YES ─► Is complex formatting required?
│   │         │
│   │         ├─► YES ─► HTML-to-PDF (Puppeteer/Playwright)
│   │         │         Rationale: Leverage existing web skills
│   │         │
│   │         └─► NO ─► Is it simple text/tables?
│   │                     │
│   │                     ├─► YES ─► Template Engine + pdf-lib
│   │                     │         Rationale: Simpler, faster
│   │                     │
│   │                     └─► NO ─► HTML-to-PDF
│   │                               Rationale: Flexibility
│   │
│   └─► NO ─► Is the document highly structured (invoice, report)?
│               │
│               ├─► YES ─► Is the layout consistent across documents?
│               │         │
│               │         ├─► YES ─► Programmatic (QuestPDF/pdf-lib)
│               │         │         Rationale: Code-defined structure
│               │         │
│               │         └─► NO ─► Template Engine approach
│               │                   Rationale: Balance of flexibility and structure
│               │
│               └─► NO ─► Is it dynamic with variable content length?
│                           │
│                           └─► YES ─► Programmatic with pagination
│                                     Rationale: Handle variable length
```

### Approach Comparison

| Approach | Flexibility | Speed | Maintainability | Complexity |
|----------|-------------|-------|----------------|----------|
| HTML-to-PDF | High | Medium | High | Low |
| Template Engine | Medium | Fast | High | Low |
| Programmatic | Low | Fast | Medium | Medium |
| Form Filling | N/A | Fastest | High | Low |

### Template Strategy by Document Type

#### Document: Invoice

**Recommendation**: HTML Template + Puppeteer

**Rationale**: Invoices need consistent styling, good for HTML/CSS

```html
<!-- invoice-template.html -->
<!DOCTYPE html>
<html>
<head>
  <style>
    .invoice-header { font-weight: bold; font-size: 24px; }
    .invoice-table { width: 100%; border-collapse: collapse; }
    .invoice-table th { background: #eee; }
    .total { font-weight: bold; font-size: 18px; }
  </style>
</head>
<body>
  <h1 class="invoice-header">INVOICE #{{invoiceNumber}}</h1>
  <p>Date: {{date}}</p>
  
  <table class="invoice-table">
    <thead>
      <tr>
        <th>Item</th>
        <th>Qty</th>
        <th>Price</th>
        <th>Total</th>
      </tr>
    </thead>
    <tbody>
      {{#each items}}
      <tr>
        <td>{{name}}</td>
        <td>{{quantity}}</td>
        <td>{{price}}</td>
        <td>{{total}}</td>
      </tr>
      {{/each}}
    </tbody>
  </table>
  
  <p class="total">Total: {{grandTotal}}</p>
</body>
</html>
```

#### Document: Technical Report

**Recommendation**: Programmatic (QuestPDF/pdf-lib)

**Rationale**: Complex layouts, charts, consistent structure

```javascript
// Programmatic report generation
function generateReport(data) {
  const doc = Document.create();
  
  doc.addPage(page => {
    // Header
    page.header().text('Technical Report');
    page.header().line();
    
    // Title
    page.content().text(data.title, { size: 24, bold: true });
    
    // Table of contents
    page.content().text('Table of Contents');
    data.sections.forEach((section, i) => {
      page.content().text(`${i + 1}. ${section.title}`);
    });
    
    // Sections
    data.sections.forEach(section => {
      page.addPage(); // New page per section
      page.content().text(section.title, { size: 18, bold: true });
      page.content().text(section.content);
      
      // Charts
      if (section.chart) {
        page.content().image(section.chart);
      }
    });
    
    // Footer
    page.footer().text(`Page {pageNumber} of {totalPages}`);
  });
  
  return doc.generatePdf();
}
```

#### Document: Form

**Recommendation**: Pre-designed PDF Form + Form Filling

**Rationale**: Fixed layout, fill existing design

```javascript
// Form filling approach
async function fillForm(templatePath, formData) {
  const pdfDoc = await PDFDocument.load(templatePath);
  const form = pdfDoc.getForm();
  
  // Fill text fields
  form.getTextField('name').setText(formData.name);
  form.getTextField('address').setText(formData.address);
  
  // Check boxes
  form.getCheckBox('agree').check();
  
  // Dropdowns
  form.getDropdown('country').select(formData.country);
  
  return await pdfDoc.save();
}
```

## Decision 4: Compression Strategy

### The Question

**How should you optimize PDF file size?**

### Decision Flowchart

```
START: Optimize PDF Size
│
├─► Are images the main size contributor?
│   │
│   ├─► YES ─► Are images high-resolution photos?
│   │         │
│   │         ├─► YES ─► Compress to 150-200 DPI, JPEG at 80-85%
│   │         │         Rationale: Good quality/size balance
│   │         │
│   │         └─► NO ─► Are they graphics/diagrams?
│   │                     │
│   │                     ├─► YES ─► PNG with optimization or SVG
│   │                     │         Rationale: Preserve vector quality
│   │                     │
│   │                     └─► NO ─► Convert to JPEG or WebP
│   │                               Rationale: Smaller size
│   │
│   └─► NO ─► Are fonts the main size contributor?
│               │
│               ├─► YES ─► Is it a one-time generation?
│               │         │
│               │         ├─► YES ─► Full font embedding OK
│               │         │
│               │         └─► NO ─► Font subsetting required
│               │                   Rationale: Dramatically reduce size
│               │
│               └─► NO ─► Is the PDF for web delivery?
│                           │
│                           ├─► YES ─► Enable linearization
│                           │         Rationale: Fast web viewing
│                           │
│                           └─► NO ─► Apply general compression
│                                     Rationale: Smaller file size
```

### Compression Strategy Matrix

| Strategy | Impact | Effort | When to Use |
|----------|--------|--------|-------------|
| Image Compression | High | Low | Always for image-heavy PDFs |
| Font Subsetting | High | Medium | Always for text-heavy PDFs |
| Remove Metadata | Low | Low | For sensitive documents |
| Linearization | Medium | Low | For web-delivered PDFs |
| Object Streams | Medium | Low | For modern PDF viewers |
| JPEG2000 | High | Medium | For photo-heavy PDFs (PDF/A-2) |

### Implementation Guide

#### Strategy: Image Optimization

```javascript
// Image optimization pipeline
class ImageOptimizer {
  async optimizeImages(images) {
    return Promise.all(
      images.map(async (img) => {
        const sharp = require('sharp');
        
        let optimizer = sharp(img.buffer);
        const metadata = await optimizer.metadata();
        
        // Resize if too large
        if (metadata.width > 1200 || metadata.height > 1200) {
          optimizer = optimizer.resize(1200, 1200, {
            fit: 'inside',
            withoutEnlargement: true
          });
        }
        
        // Compress based on type
        if (metadata.format === 'png') {
          optimizer = optimizer.png({ compressionLevel: 9 });
        } else {
          optimizer = optimizer.jpeg({ quality: 85, progressive: true });
        }
        
        return await optimizer.toBuffer();
      })
    );
  }
}
```

#### Strategy: Font Subsetting

```javascript
// Font subsetting
class FontSubsetter {
  async subsetFont(fontPath, text) {
    const fonttools = require('fonttools');
    
    // Load font
    let font = fonttools.loadTTF(fontPath);
    
    // Get only used glyphs
    const usedGlyphs = this.getUsedGlyphs(font, text);
    
    // Create subset
    const subset = new fonttools.Subset();
    subset.update(usedGlyphs);
    
    return subset.subset(font);
  }
  
  getUsedGlyphs(font, text) {
    const glyphIds = new Set();
    
    for (const char of text) {
      const glyphId = font.charToGlyphIndex(char);
      glyphIds.add(glyphId);
      
      // Add fallback glyphs
      glyphIds.add(font.getFallbackGlyphId());
    }
    
    return Array.from(glyphIds);
  }
}
```

## Decision 5: Additional Features

### The Question

**What additional PDF features are needed?**

### Feature Decision Tree

```
START: Additional Features
│
├─► Digital Signatures Required?
│   │
│   ├─► YES ─► Is it for legal documents?
│   │         │
│   │         ├─► YES ─► Use qualified signatures (eIDAS, eSign)
│   │         │         Consider: DocuSign, Adobe Sign APIs
│   │         │
│   │         └─► NO ─► Basic signatures OK
│   │                   Use: pdf-lib with custom signing
│   │
│   └─► NO ─► Encryption Required?
│               │
│               ├─► YES ─► Password encryption or Certificate encryption?
│               │         │
│               │         ├─► Password ─► User password + Owner password
│               │         │
│               │         └─► Certificate ─► Public key encryption
│               │
│               └─► NO ─► Accessibility Required?
│                           │
│                           ├─► YES ─► Implement PDF/UA features
│                           │         - Proper tagging
│                           │         - Alt text for images
│                           │         - Reading order
│                           │
│                           └─► NO ─► Standard PDF generation OK
```

### Feature Implementation Guide

#### Feature: Digital Signatures

**When**: Legal documents, contracts, certificates

**Implementation**: Use dedicated signing service for production

```javascript
// Digital signature implementation
class PDFSigningService {
  async signPDF(pdfBuffer, signingConfig) {
    const { certificate, privateKey, reason, location } = signingConfig;
    
    // Load PDF
    const pdfDoc = await PDFDocument.load(pdfBuffer);
    
    // Create signature field
    const page = pdfDoc.getPage(0);
    const signatureField = pdfDoc.addSignature(page, {
      widgetRect: [100, 100, 250, 150]
    });
    
    // Sign
    const signature = await this.createSignature(pdfDoc, {
      certificate,
      privateKey,
      reason,
      location
    });
    
    // Embed signature
    signatureField.setSignature(signature);
    
    return await pdfDoc.save();
  }
  
  async createSignature(pdfDoc, config) {
    // Use PKCS#7 for signature
    const p7 = forge.pkcs7.createSignedData();
    p7.detached = true;
    
    // Add certificate and sign
    // ... (signature creation logic)
    
    return signatureBytes;
  }
}
```

#### Feature: PDF Encryption

**When**: Confidential documents, access control

```javascript
// PDF encryption
async function encryptPDF(pdfBuffer, passwords) {
  const pdfDoc = await PDFDocument.load(pdfBuffer);
  
  pdfDoc.encrypt({
    userPassword: passwords.userPassword,
    ownerPassword: passwords.ownerPassword,
    permissions: {
      printing: 'highResolution',
      modifying: false,
      copying: false,
      annotating: false,
      fillingForms: true,
      contentAccessibility: true,
      documentAssembly: false
    }
  });
  
  return await pdfDoc.save();
}
```

#### Feature: PDF/UA Accessibility

**When**: Government documents, educational materials, accessibility compliance

```javascript
// Accessible PDF generation
async function createAccessiblePDF(content) {
  const pdfDoc = await PDFDocument.create();
  
  // Set document language
  pdfDoc.setLang('en-US');
  
  // Enable tagged PDF
  pdfDoc.catalog.getOrCreateMarkInfo().set(PDFName.of('Marked'), true);
  
  // Create structure tree root
  const structTreeRoot = pdfDoc.getStructTreeRoot();
  
  // Add heading structure
  pdfDoc.addPage();
  const page = pdfDoc.getPage(0);
  
  // Mark heading in structure
  const heading = pdfDoc.context.obj({
    Type: 'StructElem',
    S: 'H1',
    T: 'Document Title',
    Pg: page.node
  });
  
  return await pdfDoc.save();
}
```

## Quick Reference: Common Scenarios

### Scenario 1: Simple Report Export

**Flow**: Client-side → jsPDF → Download

```
Requirements:
- Simple layout
- User-initiated export
- Low volume

Decision Path:
1. Location: Client-side
2. Library: jsPDF
3. Template: Programmatic
4. Optimization: Basic compression
```

### Scenario 2: Invoice Generation (High Volume)

**Flow**: Server-side → Puppeteer → Cache → CDN

```
Requirements:
- Consistent branding
- Database integration
- High volume
- Fast delivery

Decision Path:
1. Location: Server-side
2. Library: Puppeteer
3. Template: HTML with Handlebars
4. Optimization: Full (images, fonts, caching)
5. Additional: None unless required
```

### Scenario 3: Contract Signing

**Flow**: Server-side → iText/PDF-lib → Sign → Store

```
Requirements:
- Digital signatures
- Legal compliance
- Audit trail

Decision Path:
1. Location: Server-side
2. Library: pdf-lib with custom signing
3. Template: HTML-to-PDF
4. Optimization: Standard
5. Additional: Digital signatures, encryption
```

### Scenario 4: Multi-language Document

**Flow**: Server-side → Template per locale → Optimize

```
Requirements:
- Multiple languages
- Consistent formatting
- Unicode support

Decision Path:
1. Location: Server-side
2. Library: Puppeteer or pdf-lib
3. Template: Separate templates per language
4. Optimization: Font subsetting per language
5. Additional: Language metadata
```

## Decision Summary Matrix

| Requirement | Primary Choice | Alternative |
|-------------|----------------|-------------|
| Web-style layout | Puppeteer | Playwright |
| Cross-browser | Playwright | Puppeteer |
| PDF manipulation | pdf-lib | iText |
| Enterprise features | iText | pdf-lib + custom |
| Simple creation | jsPDF | pdf-lib |
| .NET environment | QuestPDF | IronPDF |
| High performance | pdf-lib | Puppeteer (with optimization) |
| Digital signatures | Server-side signing | External service |
| Accessibility | Tagged PDF | Manual tagging |
| Web delivery | Linearized PDF | Standard PDF |

## References

- Puppeteer: https://github.com/puppeteer/puppeteer
- Playwright: https://playwright.dev/
- pdf-lib: https://pdf-lib.org/
- jsPDF: https://artskydj.github.io/jsPDF/
- iText: https://itextpdf.com/
- QuestPDF: https://www.questpdf.com/
- IronPDF: https://ironpdf.com/
- Fonttools: https://github.com/fonttools/fonttools
- Sharp: https://sharp.pixelplumbing.com/
