# PDF Knowledge Base - FAQ

## Tổng quan

Document này cung cấp 10 câu hỏi thường gặp và câu trả lời chi tiết về xử lý PDF trong Cursor Enterprise Framework.

## Câu hỏi 1: Làm thế nào để tạo PDF/A compliant document?

### Câu trả lời

Để tạo PDF/A compliant document, bạn cần tuân thủ các yêu cầu nghiêm ngặt của tiêu chuẩn ISO 19005. Dưới đây là các bước chi tiết:

```typescript
import { PDFAValidator } from '@enterprise/pdf-validator';

class PDFACreator {
  async createPDFA(
    content: PDFContent,
    options: PDFAOptions
  ): Promise<Buffer> {
    // 1. Sử dụng document factory với PDF/A settings
    const doc = await this.createDocument({
      version: '1.7',
      standard: 'pdf/a-3b', // Hoặc pdf/a-1a, pdf/a-2a, etc.
      conformance: 'B' // Hoặc 'A' cho accessible
    });
    
    // 2. Embed tất cả fonts - ĐÂY LÀ BẮT BUỘC
    const fonts = await this.collectAndEmbedFonts(content);
    
    // 3. Sử dụng chỉ colorspaces được phép
    await this.setAllowedColorspaces(doc, content);
    // - RGB (được phép trong PDF/A-1, 2, 3)
    // - Grayscale (được phép)
    // - CMYK (chỉ được phép trong PDF/A-3)
    
    // 4. Thêm required metadata
    doc.setMetadata({
      title: options.title,
      author: options.author,
      subject: options.subject,
      keywords: options.keywords,
      creator: 'Enterprise PDF Generator',
      producer: 'Enterprise PDF Generator v1.0',
      creationDate: new Date(),
      modificationDate: new Date()
    });
    
    // 5. Thêm XMP metadata
    doc.setXMPMetadata({
      'pdfa:part': '3',
      'pdfa:conformance': 'B',
      'dc:title': options.title,
      'dc:creator': options.author
    });
    
    // 6. Add content
    await this.addContent(doc, content);
    
    // 7. Validate trước khi save
    const validator = new PDFAValidator();
    const validationResult = await validator.validate(doc);
    
    if (!validationResult.isCompliant) {
      throw new PDFANonComplianceError(validationResult.issues);
    }
    
    return doc.save();
  }
  
  private async collectAndEmbedFonts(
    content: PDFContent
  ): Promise<EmbeddedFont[]> {
    const fontPaths = new Set<string>();
    
    // Collect all unique fonts
    for (const block of content.blocks) {
      if (block.fontFamily) {
        fontPaths.add(block.fontFamily);
      }
    }
    
    const embeddedFonts = [];
    
    for (const fontPath of fontPaths) {
      const fontData = await fs.readFile(fontPath);
      const embedded = await this.embedFont(fontData, {
        subset: true, // Tối ưu: chỉ embed glyphs thực sự sử dụng
        embed: true
      });
      embeddedFonts.push(embedded);
    }
    
    return embeddedFonts;
  }
  
  private async setAllowedColorspaces(
    doc: PDFDocument,
    content: PDFContent
  ): Promise<void> {
    // Convert DeviceCMYK to DeviceRGB nếu cần
    // PDF/A-1 và PDF/A-2 không cho phép DeviceCMYK
    for (const image of content.images) {
      if (image.colorspace === 'CMYK') {
        image.colorspace = 'RGB';
        image.data = this.convertCMYKtoRGB(image.data);
      }
    }
  }
}
```

### Các loại PDF/A phổ biến

| Loại | Mô tả | Use Cases |
|------|-------|-----------|
| PDF/A-1a | Level A accessible | Legal, government documents cần accessibility |
| PDF/A-1b | Level B basic | Long-term archive, basic appearance |
| PDF/A-2a | Level A + vector graphics | Engineering drawings |
| PDF/A-2b | Level B + improved compression | General archival |
| PDF/A-3a | Level A + allow attachments | Invoices, forms với attachments |
| PDF/A-3b | Level B + allow attachments | General use với file attachments |

## Câu hỏi 2: Làm thế nào để xử lý large PDF files hiệu quả?

### Câu trả lời

Xử lý large PDF files đòi hỏi chiến lược memory-efficient. Dưới đây là các kỹ thuật quan trọng:

```typescript
import { createReadStream, createWriteStream } from 'fs';
import { pipeline } from 'stream/promises';

class LargePDFProcessor {
  // Strategy 1: Stream-based processing
  async processLargePDF(
    inputPath: string,
    outputPath: string,
    operation: PDFOperation
  ): Promise<void> {
    const readStream = createReadStream(inputPath, {
      highWaterMark: 1024 * 1024 // 1MB chunks
    });
    
    const processor = this.createProcessor(operation);
    const writeStream = createWriteStream(outputPath);
    
    // pipeline() handles backpressure automatically
    await pipeline(readStream, processor, writeStream);
  }
  
  // Strategy 2: Page-by-page processing
  async processLargePDFPageByPage(
    inputPath: string,
    options: ProcessingOptions
  ): Promise<string> {
    const outputPath = this.generateOutputPath(inputPath);
    
    // Open document for sequential access
    const doc = await PDFDocument.open(inputPath, {
      sequentialAccess: true // IMPORTANT: loads only visible portions
    });
    
    const outputDoc = await PDFDocument.create();
    
    const pageCount = doc.getPageCount();
    
    for (let i = 0; i < pageCount; i++) {
      // Process one page at a time
      const page = await doc.getPage(i);
      
      // Apply operation to page
      const processedPage = await this.processPage(page, options);
      
      // Copy to output document
      await outputDoc.copyPages([processedPage], [0]);
      
      // Report progress
      this.reportProgress(i + 1, pageCount);
    }
    
    await outputDoc.save(outputPath);
    return outputPath;
  }
  
  // Strategy 3: Chunked extraction
  async extractTextChunked(
    inputPath: string,
    options: {
      chunkSize: number;
      onProgress: (progress: number) => void;
    }
  ): Promise<string> {
    const chunks: string[] = [];
    const stat = await fs.stat(inputPath);
    const totalSize = stat.size;
    
    await this.withReadStream(inputPath, async (stream) => {
      let bytesProcessed = 0;
      
      for await (const chunk of stream) {
        const text = await this.extractTextFromChunk(chunk);
        chunks.push(text);
        
        bytesProcessed += chunk.length;
        options.onProgress((bytesProcessed / totalSize) * 100);
      }
    });
    
    return chunks.join('\n');
  }
  
  // Strategy 4: Temporary file strategy
  async processWithTempFiles(inputPath: string): Promise<Buffer> {
    const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'pdf-'));
    
    try {
      // Step 1: Create temporary working files
      const tempInput = path.join(tempDir, 'input.pdf');
      const tempOutput = path.join(tempDir, 'output.pdf');
      
      // Copy input to temp if needed
      if (inputPath !== tempInput) {
        await fs.copyFile(inputPath, tempInput);
      }
      
      // Step 2: Process
      await this.processDocument(tempInput, tempOutput);
      
      // Step 3: Read result
      return await fs.readFile(tempOutput);
      
    } finally {
      // Always cleanup
      await fs.rm(tempDir, { recursive: true, force: true });
    }
  }
}
```

### Best practices cho Large PDF Handling

1. **Sử dụng sequentialAccess**: Giảm memory usage đáng kể
2. **Stream processing**: Pipe data thay vì load all
3. **Page-by-page processing**: Không load toàn bộ document
4. **Temporary files**: Dùng disk space thay vì memory
5. **Progress reporting**: Luôn báo cáo progress cho UX
6. **Timeout handling**: Đặt timeout cho operations dài

## Câu hỏi 3: Làm thế nào để implement digital signature?

### Câu trả lời

Digital signatures trong PDF yêu cầu PKI infrastructure và proper certificate management:

```typescript
import { PKIAdapter } from '@enterprise/pki';
import { TimestampAuthority } from '@enterprise/timestamps';

class PDFSigner {
  private pkiAdapter: PKIAdapter;
  private tsa: TimestampAuthority;
  
  async signDocument(
    documentPath: string,
    options: SigningOptions
  ): Promise<Buffer> {
    // 1. Load certificate và private key
    const certData = await fs.readFile(options.certificatePath);
    const keyData = await fs.readFile(options.privateKeyPath);
    
    const certificate = this.pkiAdapter.parseCertificate(certData);
    const privateKey = this.pkiAdapter.parsePrivateKey(keyData, options.password);
    
    // 2. Validate certificate
    const validation = await this.validateCertificate(certificate);
    if (!validation.valid) {
      throw new CertificateValidationError(validation.errors);
    }
    
    // 3. Open document
    const doc = await PDFDocument.load(documentPath);
    
    // 4. Create signature field
    const signatureField = await this.createSignatureField(doc, {
      pageIndex: options.pageIndex || 0,
      position: options.position || { x: 50, y: 700 },
      width: options.width || 200,
      height: options.height || 50
    });
    
    // 5. Calculate content hash
    const contentHash = await this.calculateDocumentHash(doc, signatureField);
    
    // 6. Sign hash với private key
    const signature = await this.pkiAdapter.sign(contentHash, privateKey);
    
    // 7. Request timestamp từ TSA
    let timestamp: Timestamp | undefined;
    if (options.includeTimestamp) {
      timestamp = await this.tsa.requestTimestamp(signature, options.tsaUrl);
    }
    
    // 8. Embed signature
    await this.embedSignature(doc, signatureField, {
      signature,
      certificate,
      timestamp,
      reason: options.reason,
      location: options.location,
      contactInfo: options.contactInfo
    });
    
    // 9. Verify signature
    const isValid = await this.verifySignature(doc, signatureField);
    if (!isValid) {
      throw new SignatureVerificationError('Signature verification failed');
    }
    
    return doc.save();
  }
  
  private async calculateDocumentHash(
    doc: PDFDocument,
    signatureField: SignatureField
  ): Promise<Buffer> {
    // Byte range cho signature calculation
    const ranges = await doc.getByteRanges(signatureField);
    
    // Hash các phần document trong byte range
    const hashInput = await doc.readByteRanges(ranges);
    
    return crypto.createHash('sha256').update(hashInput).digest();
  }
  
  private async embedSignature(
    doc: PDFDocument,
    field: SignatureField,
    data: SignatureData
  ): Promise<void> {
    // Create signature dictionary
    const sigDict = {
      Type: '/Sig',
      Filter: '/Adobe.PPKLite',
      SubFilter: '/adbe.pkcs7.detached',
      ByteRange: data.byteRange,
      Contents: data.contents, // PKCS#7 signature
      Reason: data.reason,
      Location: data.location,
      ContactInfo: data.contactInfo,
      M: data.timestamp || new Date()
    };
    
    // Add certificate chain
    if (data.certificate.chain) {
      sigDict.Cert = data.certificate.chain;
    }
    
    await doc.updateObject(field.objectNumber, sigDict);
  }
  
  async verifySignature(
    doc: PDFDocument,
    fieldName: string
  ): Promise<VerificationResult> {
    const field = doc.getSignatureField(fieldName);
    if (!field) {
      throw new Error('Signature field not found');
    }
    
    // Extract signature data
    const signatureData = await this.extractSignatureData(field);
    
    // Verify certificate
    const certResult = await this.pkiAdapter.verifyCertificate(
      signatureData.certificate
    );
    if (!certResult.valid) {
      return { valid: false, errors: certResult.errors };
    }
    
    // Verify signature
    const contentHash = await this.calculateDocumentHash(doc, field);
    const sigValid = await this.pkiAdapter.verify(
      contentHash,
      signatureData.signature,
      signatureData.certificate.publicKey
    );
    
    if (!sigValid) {
      return {
        valid: false,
        errors: ['Signature does not match document content']
      };
    }
    
    // Verify timestamp if present
    if (signatureData.timestamp) {
      const tsaResult = await this.tsa.verifyTimestamp(
        signatureData.timestamp
      );
      if (!tsaResult.valid) {
        return { valid: false, errors: tsaResult.errors };
      }
    }
    
    return {
      valid: true,
      signer: signatureData.certificate.subject,
      timestamp: signatureData.timestamp?.time,
      documentModified: false
    };
  }
}
```

## Câu hỏi 4: Làm thế nào để merge multiple PDF files?

### Câu trả lời

```typescript
class PDFMerger {
  async merge(
    sources: string[],
    options: MergeOptions = {}
  ): Promise<Buffer> {
    // Create output document
    const outputDoc = await PDFDocument.create({
      autoFirstPage: false
    });
    
    // Track page mappings for outline
    const outlineItems: OutlineItem[] = [];
    let pageOffset = 0;
    
    for (const sourcePath of sources) {
      // Load source document
      const sourceDoc = await PDFDocument.load(sourcePath, {
        ignoreEncryption: options.ignoreEncryption
      });
      
      // Copy all pages
      const pageIndices = options.pageRange 
        ? this.parsePageRange(options.pageRange)
        : Array.from({ length: sourceDoc.getPageCount() }, (_, i) => i);
      
      const copiedPages = await outputDoc.copyPages(
        sourceDoc,
        pageIndices
      );
      
      // Add copied pages to output
      for (const page of copiedPages) {
        outputDoc.addPage(page);
      }
      
      // Create outline entry for this source
      if (options.createOutline) {
        outlineItems.push({
          title: options.getTitle?.(sourcePath) || path.basename(sourcePath),
          pageIndex: pageOffset,
          children: []
        });
        pageOffset += copiedPages.length;
      }
    }
    
    // Add outline if requested
    if (options.createOutline && outlineItems.length > 0) {
      await this.addOutline(outputDoc, outlineItems);
    }
    
    // Apply global operations
    if (options.optimize) {
      await this.optimize(outputDoc);
    }
    
    return outputDoc.save();
  }
  
  async mergeWithBookmarks(
    sources: MergeSource[],
    options: MergeOptions
  ): Promise<Buffer> {
    const outputDoc = await PDFDocument.create({
      autoFirstPage: false
    });
    
    const bookmarks: BookmarkNode[] = [];
    
    for (const source of sources) {
      const sourceDoc = await PDFDocument.load(source.path);
      const bookmark = await this.processSourceWithBookmark(
        outputDoc,
        sourceDoc,
        source
      );
      bookmarks.push(bookmark);
    }
    
    // Build bookmark tree
    await this.buildBookmarkTree(outputDoc, bookmarks);
    
    return outputDoc.save();
  }
  
  private async processSourceWithBookmark(
    outputDoc: PDFDocument,
    sourceDoc: PDFDocument,
    source: MergeSource
  ): Promise<BookmarkNode> {
    const startPage = outputDoc.getPageCount();
    
    // Copy pages
    const pages = await outputDoc.copyPages(sourceDoc, source.pages);
    for (const page of pages) {
      outputDoc.addPage(page);
    }
    
    const endPage = outputDoc.getPageCount() - 1;
    
    return {
      title: source.title || path.basename(source.path),
      startPage,
      endPage,
      children: source.children?.map(
        child => this.processSourceWithBookmark(outputDoc, sourceDoc, child)
      ) || []
    };
  }
}
```

## Câu hỏi 5: Làm thế nào để extract text từ PDF với layout preservation?

### Câu trả lời

```typescript
class PDFTextExtractor {
  async extractText(
    documentPath: string,
    options: TextExtractionOptions = {}
  ): Promise<ExtractedText> {
    const doc = await PDFDocument.load(documentPath);
    
    if (options.mode === 'plain') {
      return this.extractPlainText(doc, options);
    }
    
    if (options.mode === 'layout') {
      return this.extractWithLayout(doc, options);
    }
    
    if (options.mode === 'structured') {
      return this.extractStructured(doc, options);
    }
    
    throw new Error(`Unknown extraction mode: ${options.mode}`);
  }
  
  private async extractWithLayout(
    doc: PDFDocument,
    options: TextExtractionOptions
  ): Promise<ExtractedText> {
    const pages: ExtractedPage[] = [];
    
    const pageRange = options.pageRange || {
      start: 0,
      end: doc.getPageCount() - 1
    };
    
    for (let i = pageRange.start; i <= pageRange.end; i++) {
      const page = await doc.getPage(i);
      const pageContent = await this.extractPageWithLayout(page);
      pages.push(pageContent);
    }
    
    return {
      pages,
      metadata: {
        totalPages: doc.getPageCount(),
        extractedPages: pages.length,
        language: await this.detectLanguage(pages)
      }
    };
  }
  
  private async extractPageWithLayout(
    page: PDFPage
  ): Promise<ExtractedPage> {
    const blocks: TextBlock[] = [];
    const pageHeight = page.getMediaBox().height;
    
    // Extract text items with position
    const textItems = await page.getTextItems({
      includePositions: true,
      includeFontInfo: true
    });
    
    // Group items into lines
    const lines = this.groupIntoLines(textItems, pageHeight);
    
    // Group lines into paragraphs
    const paragraphs = this.groupIntoParagraphs(lines);
    
    // Detect blocks (headings, paragraphs, etc.)
    for (const paragraph of paragraphs) {
      blocks.push({
        type: this.classifyBlock(paragraph),
        content: paragraph.lines.map(l => l.text).join('\n'),
        bounds: this.calculateBounds(paragraph.lines),
        style: paragraph.style
      });
    }
    
    return {
      pageNumber: page.pageNumber,
      width: page.getMediaBox().width,
      height: pageHeight,
      blocks,
      lines: lines.map(l => ({
        text: l.text,
        y: l.y,
        x: l.x,
        width: l.width
      }))
    };
  }
  
  private groupIntoLines(
    items: TextItem[],
    pageHeight: number
  ): TextLine[] {
    const lines: TextLine[] = [];
    const tolerance = 5; // Y-position tolerance
    
    // Sort by Y position (top to bottom), then X position (left to right)
    const sorted = [...items].sort((a, b) => {
      const yDiff = (pageHeight - a.y) - (pageHeight - b.y);
      if (Math.abs(yDiff) > tolerance) return yDiff;
      return a.x - b.x;
    });
    
    let currentLine: TextItem[] = [];
    let currentY: number | null = null;
    
    for (const item of sorted) {
      const itemY = pageHeight - item.y;
      
      if (currentY === null) {
        currentY = itemY;
        currentLine.push(item);
      } else if (Math.abs(itemY - currentY) <= tolerance) {
        currentLine.push(item);
      } else {
        // New line
        lines.push(this.createLine(currentLine));
        currentLine = [item];
        currentY = itemY;
      }
    }
    
    if (currentLine.length > 0) {
      lines.push(this.createLine(currentLine));
    }
    
    return lines;
  }
  
  private createLine(items: TextItem[]): TextLine {
    // Sort items by X position
    const sorted = [...items].sort((a, b) => a.x - b.x);
    
    return {
      text: sorted.map(i => i.text).join(''),
      x: sorted[0].x,
      y: sorted[0].y,
      width: sorted[sorted.length - 1].x + sorted[sorted.length - 1].width - sorted[0].x,
      items: sorted,
      fontSize: sorted[0].fontSize,
      fontFamily: sorted[0].fontFamily
    };
  }
}
```

## Câu hỏi 6: Làm thế nào để protect PDF với password?

### Câu trả lời

```typescript
class PDFProtectionService {
  async encryptPDF(
    inputPath: string,
    options: EncryptionOptions
  ): Promise<Buffer> {
    const doc = await PDFDocument.load(inputPath);
    
    // Encryption configuration
    const encryptionConfig = {
      algorithm: options.algorithm || 'AES-256',
      userPassword: await this.getSecurePassword(options.userPassword),
      ownerPassword: await this.getSecurePassword(options.ownerPassword),
      permissions: this.mapPermissions(options.permissions)
    };
    
    doc.encrypt(encryptionConfig);
    
    return doc.save();
  }
  
  private mapPermissions(
    perms: PermissionOptions
  ): PermissionFlags {
    let flags = 0;
    
    if (perms.print) flags |= 0x04;        // bit 3
    if (perms.modifyContent) flags |= 0x08; // bit 4
    if (perms.extractContent) flags |= 0x10; // bit 5
    if (perms.modifyAnnotations) flags |= 0x20; // bit 6
    if (perms.fillForms) flags |= 0x100;    // bit 9
    if (perms.extractAccessibility) flags |= 0x200; // bit 10
    if (perms.assemble) flags |= 0x400;     // bit 11
    if (perms.printDegraded) flags |= 0x800; // bit 12
    
    return flags;
  }
  
  async removePassword(
    inputPath: string,
    ownerPassword: string
  ): Promise<Buffer> {
    const doc = await PDFDocument.load(inputPath, {
      password: ownerPassword
    });
    
    // Remove encryption by saving without encryption
    // This only works if we have the owner password
    return doc.save();
  }
}
```

## Câu hỏi 7: Làm thế nào để convert PDF sang images?

### Câu trả lời

```typescript
class PDFImageConverter {
  async convertToImages(
    inputPath: string,
    options: ImageConversionOptions = {}
  ): Promise<ImageResult[]> {
    const doc = await PDFDocument.load(inputPath);
    const results: ImageResult[] = [];
    
    const pageRange = options.pageRange || {
      start: 0,
      end: doc.getPageCount() - 1
    };
    
    for (let i = pageRange.start; i <= pageRange.end; i++) {
      const image = await this.renderPage(doc, i, options);
      results.push(image);
      
      if (options.onProgress) {
        options.onProgress(i - pageRange.start + 1, pageRange.end - pageRange.start + 1);
      }
    }
    
    return results;
  }
  
  private async renderPage(
    doc: PDFDocument,
    pageIndex: number,
    options: ImageConversionOptions
  ): Promise<ImageResult> {
    const page = await doc.getPage(pageIndex);
    
    // Calculate dimensions
    const scale = options.scale || 1;
    const { width, height } = page.getViewport({ scale });
    
    // Create canvas-like structure for rendering
    const renderer = new PDFRenderer({
      width: Math.floor(width),
      height: Math.floor(height),
      format: options.format || 'png',
      quality: options.quality || 0.92
    });
    
    await renderer.render(page);
    
    const buffer = await renderer.toBuffer();
    
    return {
      pageNumber: pageIndex + 1,
      width: Math.floor(width),
      height: Math.floor(height),
      format: options.format || 'png',
      buffer
    };
  }
  
  async convertToThumbnail(
    inputPath: string,
    options: ThumbnailOptions = {}
  ): Promise<Buffer> {
    const results = await this.convertToImages(inputPath, {
      scale: options.maxWidth ? options.maxWidth / 612 : 0.1, // 612 is standard page width
      format: 'jpeg',
      quality: 0.7,
      pageRange: { start: 0, end: 0 } // First page only
    });
    
    return results[0].buffer;
  }
}
```

## Câu hỏi 8: Làm thế nào để add watermark vào PDF?

### Câu trời

```typescript
class PDFWatermarkService {
  async addWatermark(
    inputPath: string,
    options: WatermarkOptions
  ): Promise<Buffer> {
    const doc = await PDFDocument.load(inputPath);
    
    for (let i = 0; i < doc.getPageCount(); i++) {
      const page = await doc.getPage(i);
      await this.addWatermarkToPage(page, options);
    }
    
    return doc.save();
  }
  
  private async addWatermarkToPage(
    page: PDFPage,
    options: WatermarkOptions
  ): Promise<void> {
    // Get page dimensions
    const { width, height } = page.getMediaBox();
    
    // Calculate watermark position
    const position = this.calculatePosition(options, width, height);
    
    if (options.type === 'text') {
      await this.addTextWatermark(page, position, options);
    } else if (options.type === 'image') {
      await this.addImageWatermark(page, position, options);
    }
  }
  
  private calculatePosition(
    options: WatermarkOptions,
    pageWidth: number,
    pageHeight: number
  ): WatermarkPosition {
    const { horizontalAlign, verticalAlign, rotation = 0 } = options;
    
    let x = 0;
    let y = 0;
    
    switch (horizontalAlign) {
      case 'left':
        x = options.margin || 0;
        break;
      case 'center':
        x = pageWidth / 2;
        break;
      case 'right':
        x = pageWidth - (options.margin || 0);
        break;
    }
    
    switch (verticalAlign) {
      case 'top':
        y = pageHeight - (options.margin || 0);
        break;
      case 'middle':
        y = pageHeight / 2;
        break;
      case 'bottom':
        y = options.margin || 0;
        break;
    }
    
    return { x, y, rotation };
  }
  
  private async addTextWatermark(
    page: PDFPage,
    position: WatermarkPosition,
    options: WatermarkOptions
  ): Promise<void> {
    page.drawText(options.text, {
      x: position.x,
      y: position.y,
      size: options.fontSize || 48,
      font: await this.getWatermarkFont(options),
      color: this.parseColor(options.color || '#CCCCCC'),
      opacity: options.opacity || 0.3,
      rotate: this.degreesToRadians(position.rotation),
      align: options.horizontalAlign as any,
      valign: options.verticalAlign as any
    });
  }
}
```

## Câu hỏi 9: Làm thế nào để optimize PDF file size?

### Câu trả lời

```typescript
class PDFOptimizer {
  async optimize(
    inputPath: string,
    options: OptimizationOptions = {}
  ): Promise<Buffer> {
    const doc = await PDFDocument.load(inputPath);
    
    // 1. Remove unnecessary objects
    if (options.removeUnusedObjects) {
      await this.removeUnusedObjects(doc);
    }
    
    // 2. Optimize images
    if (options.compressImages) {
      await this.compressImages(doc, options.imageQuality || 0.8);
    }
    
    // 3. Flatten transparency
    if (options.flattenTransparency) {
      await this.flattenTransparency(doc);
    }
    
    // 4. Optimize streams
    if (options.compressStreams) {
      await this.recompressStreams(doc);
    }
    
    // 5. Remove metadata
    if (options.removeMetadata) {
      doc.removeMetadata();
    }
    
    // 6. Subset fonts
    if (options.subsetFonts) {
      await this.createFontSubsets(doc);
    }
    
    return doc.save({
      useObjectStreams: options.useObjectStreams ?? true,
      addDefaultFooter: false
    });
  }
  
  private async compressImages(
    doc: PDFDocument,
    quality: number
  ): Promise<void> {
    for (let i = 0; i < doc.getPageCount(); i++) {
      const page = await doc.getPage(i);
      const images = await page.getImages();
      
      for (const image of images) {
        // Downsample if needed
        const maxDimension = 2000;
        if (image.width > maxDimension || image.height > maxDimension) {
          await this.downsampleImage(image, maxDimension);
        }
        
        // Recompress
        await this.recompressImage(image, {
          format: 'jpeg',
          quality,
          progressive: true
        });
      }
    }
  }
}
```

## Câu hỏi 10: Làm thế nào để handle PDF forms (AcroForms)?

### Câu trả lời

```typescript
class PDFFormService {
  async extractFormData(
    inputPath: string
  ): Promise<FormData[]> {
    const doc = await PDFDocument.load(inputPath);
    const formFields = await doc.getFormFields();
    
    return formFields.map(field => ({
      name: field.getName(),
      type: field.getType(),
      value: field.getValue(),
      isReadOnly: field.isReadOnly(),
      isRequired: field.isRequired(),
      alternatives: field.getAlternatives?.() || []
    }));
  }
  
  async fillForm(
    inputPath: string,
    data: Record<string, any>
  ): Promise<Buffer> {
    const doc = await PDFDocument.load(inputPath);
    const form = await doc.getForm();
    
    for (const [fieldName, value] of Object.entries(data)) {
      try {
        const field = form.getField(fieldName);
        
        switch (field.type) {
          case 'text':
            field.setValue(value as string);
            break;
          case 'checkbox':
            field.check(value === true);
            break;
          case 'radio':
            field.select(value as string);
            break;
          case 'dropdown':
            field.select(value as string);
            break;
        }
      } catch (error) {
        console.warn(`Failed to fill field ${fieldName}:`, error);
      }
    }
    
    return doc.save();
  }
  
  async flattenForm(
    inputPath: string
  ): Promise<Buffer> {
    const doc = await PDFDocument.load(inputPath);
    const form = await doc.getForm();
    
    // Flatten makes form fields non-editable
    await form.flatten();
    
    return doc.save();
  }
}
```

## Related Documents

- [PDF Glossary](../glossary.md)
- [PDF Architecture](../architecture.md)
- [PDF Best Practices](../best-practice.md)
- [PDF Anti-Patterns](../anti-pattern.md)
- [PDF Checklist](../checklist.md)
- [PDF Decision Tree](../decision-tree.md)
