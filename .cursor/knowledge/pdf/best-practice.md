# PDF Knowledge Base - Best Practices

## Tổng quan

Document này cung cấp 10+ best practices cho việc xử lý PDF trong Cursor Enterprise Framework, kèm theo code examples cụ thể cho từng practice.

## Practice 1: Always Validate PDF Structure Before Processing

### Mô tả

Trước khi thực hiện bất kỳ operation nào trên PDF, luôn luôn validate cấu trúc cơ bản của document. Điều này giúp tránh crashes và unexpected behavior khi xử lý các files không hợp lệ hoặc corrupted.

```typescript
import { PDFParser } from '@enterprise/pdf-parser';
import { PDFValidator } from '@enterprise/pdf-validator';

class SafePDFProcessor {
  private parser: PDFParser;
  private validator: PDFValidator;
  
  async processPDF(filePath: string): Promise<ProcessedResult> {
    // Bước 1: Validate file signature (magic bytes)
    const isValidSignature = await this.validator.validateSignature(filePath);
    if (!isValidSignature) {
      throw new PDFValidationError('Invalid PDF file signature');
    }
    
    // Bước 2: Validate basic structure
    const structureReport = await this.validator.validateStructure(filePath);
    if (!structureReport.isValid) {
      throw new PDFValidationError(
        `Invalid PDF structure: ${structureReport.errors.join(', ')}`
      );
    }
    
    // Bước 3: Parse document
    const document = await this.parser.parse(filePath);
    
    // Bước 4: Validate content integrity
    await this.validateContentIntegrity(document);
    
    return this.processDocument(document);
  }
  
  private async validateContentIntegrity(doc: PDFDocument): Promise<void> {
    // Check xref table integrity
    const xrefValid = await this.checkXRefTable(doc);
    if (!xrefValid) {
      throw new PDFValidationError('Cross-reference table is corrupted');
    }
    
    // Check all referenced objects exist
    const missingObjects = await this.findMissingObjects(doc);
    if (missingObjects.length > 0) {
      throw new PDFValidationError(
        `Missing objects: ${missingObjects.join(', ')}`
      );
    }
  }
}
```

### Tại sao quan trọng

- Tránh crashes khi xử lý corrupted files
- Cung cấp meaningful error messages
- Bảo vệ downstream processing từ bad input
- Improve overall system reliability

## Practice 2: Use Stream-Based Processing for Large Files

### Mô tả

Đối với PDF files lớn (trên 50MB), sử dụng streaming approach thay vì load toàn bộ file vào memory. Điều này giúp tiết kiệm memory và cải thiện performance.

```typescript
import { createReadStream, createWriteStream } from 'fs';
import { PDFStreamProcessor } from '@enterprise/pdf-stream';

class LargePDFProcessor {
  private readonly CHUNK_SIZE = 64 * 1024; // 64KB chunks
  
  async processLargePDF(
    inputPath: string, 
    outputPath: string,
    options: ProcessingOptions
  ): Promise<void> {
    // Create readable stream for input
    const readStream = createReadStream(inputPath, {
      highWaterMark: this.CHUNK_SIZE
    });
    
    // Create PDF stream processor
    const processor = new PDFStreamProcessor(options);
    
    // Create writable stream for output
    const writeStream = createWriteStream(outputPath);
    
    // Pipe through processor
    await new Promise<void>((resolve, reject) => {
      readStream
        .pipe(processor.createTransformStream())
        .pipe(writeStream)
        .on('finish', resolve)
        .on('error', reject);
    });
  }
  
  async extractTextFromLargePDF(
    filePath: string,
    onProgress: (progress: number) => void
  ): Promise<string> {
    const fileSize = await this.getFileSize(filePath);
    let bytesProcessed = 0;
    const textChunks: string[] = [];
    
    const readStream = createReadStream(filePath);
    const processor = new PDFStreamProcessor({
      mode: 'text-extraction'
    });
    
    for await (const chunk of readStream.pipe(processor)) {
      bytesProcessed += chunk.length;
      onProgress((bytesProcessed / fileSize) * 100);
      
      if (chunk.text) {
        textChunks.push(chunk.text);
      }
    }
    
    return textChunks.join('\n');
  }
}
```

## Practice 3: Embed Fonts Properly for PDF/A Generation

### Mô tả

Khi tạo PDF/A files, tất cả fonts phải được embedded đầy đủ để đảm bảo document hiển thị chính xác trên mọi hệ thống mà không cần cài đặt fonts.

```typescript
import { PDFFontManager } from '@enterprise/pdf-fonts';

class PDFAGenerator {
  private fontManager: PDFFontManager;
  
  async generatePDFA(
    sourceDoc: PDFDocument,
    options: PDFAOptions
  ): Promise<Buffer> {
    // Load required fonts
    const fonts = await this.loadFontsForEmbedding(sourceDoc);
    
    // Embed all fonts
    const embeddedFonts = await this.embedAllFonts(fonts);
    
    // Convert colorspaces if necessary
    const colorspaceFixed = await this.fixColorspaces(sourceDoc);
    
    // Add XMP metadata
    const withMetadata = await this.addPDFAMetadata(colorspaceFixed);
    
    // Add structure tags
    const taggedDoc = await this.addStructureTags(withMetadata);
    
    // Validate final document
    const validator = new PDFAValidator();
    const result = await validator.validate(taggedDoc);
    
    if (!result.isCompliant) {
      throw new PDFAValidationError(
        `PDF/A compliance issues: ${result.issues.join(', ')}`
      );
    }
    
    return this.serializeDocument(taggedDoc);
  }
  
  private async embedAllFonts(
    fonts: FontSource[]
  ): Promise<EmbeddedFont[]> {
    const embeddedFonts: EmbeddedFont[] = [];
    
    for (const font of fonts) {
      if (font.isAlreadyEmbedded) {
        embeddedFonts.push(font);
        continue;
      }
      
      // Get font data
      const fontData = await this.fontManager.getFontData(font);
      
      // Embed font subset if full embedding not needed
      if (this.shouldSubset(font, fontData)) {
        const subset = await this.createFontSubset(font, fontData);
        embeddedFonts.push(subset);
      } else {
        embeddedFonts.push(await this.embedFullFont(font, fontData));
      }
    }
    
    return embeddedFonts;
  }
  
  private async createFontSubset(
    font: FontSource,
    fontData: Buffer
  ): Promise<EmbeddedFont> {
    // Analyze which glyphs are used
    const usedGlyphs = this.analyzeUsedGlyphs(font);
    
    // Create subset using fonttools or similar
    const subsetData = await fonttools.subset(fontData, {
      glyphs: usedGlyphs,
      format: 'opentype'
    });
    
    return {
      name: font.name,
      embedded: true,
      subset: true,
      subsetPrefix: this.generateSubsetPrefix(),
      data: subsetData
    };
  }
}
```

## Practice 4: Implement Proper Error Handling

### Mô tả

Xử lý lỗi một cách có hệ thống với proper error hierarchy và meaningful error messages giúp debugging và troubleshooting dễ dàng hơn.

```typescript
// Define comprehensive error hierarchy
abstract class PDFError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly recoverable: boolean
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

class PDFParseError extends PDFError {
  constructor(
    message: string,
    public readonly location: { offset: number; line: number; column: number }
  ) {
    super(message, 'PDF_PARSE_ERROR', false);
  }
}

class PDFValidationError extends PDFError {
  constructor(
    message: string,
    public readonly validationErrors: ValidationError[]
  ) {
    super(message, 'PDF_VALIDATION_ERROR', true);
  }
}

class PDFEncryptionError extends PDFError {
  constructor(
    message: string,
    public readonly reason: 'wrong-password' | 'corrupted-key' | 'unsupported-algorithm'
  ) {
    super(message, 'PDF_ENCRYPTION_ERROR', false);
  }
}

class PDFProcessingPipeline {
  async processWithErrorHandling(
    document: PDFSource,
    options: ProcessingOptions
  ): Promise<ProcessingResult> {
    try {
      // Processing logic
      const result = await this.processDocument(document, options);
      return { success: true, result };
      
    } catch (error) {
      if (error instanceof PDFError) {
        return this.handlePDFError(error, document);
      }
      
      // Wrap unexpected errors
      return this.handlePDFError(
        new PDFError(
          `Unexpected error: ${error.message}`,
          'PDF_UNKNOWN_ERROR',
          false
        ),
        document
      );
    }
  }
  
  private handlePDFError(
    error: PDFError,
    document: PDFSource
  ): ProcessingResult {
    logger.error({
      error: {
        type: error.code,
        message: error.message,
        stack: error.stack,
        recoverable: error.recoverable
      },
      document: {
        path: document.path,
        size: document.size,
        checksum: document.checksum
      }
    });
    
    if (error.recoverable) {
      return {
        success: false,
        error: error.message,
        canRetry: true,
        partialResult: error instanceof PDFValidationError 
          ? error.validationErrors 
          : undefined
      };
    }
    
    return {
      success: false,
      error: error.message,
      canRetry: false
    };
  }
}
```

## Practice 5: Optimize Memory Usage with Object Pooling

### Mô tả

Sử dụng object pooling để tái sử dụng expensive objects như PDF parsers, font caches, và image buffers, giảm garbage collection overhead.

```typescript
import { ObjectPool } from '@enterprise/object-pool';

class PDFProcessorPool {
  private parserPool: ObjectPool<PDFParser>;
  private rendererPool: ObjectPool<PDFRenderer>;
  private fontCachePool: ObjectPool<FontCache>;
  
  constructor() {
    this.parserPool = new ObjectPool({
      create: () => new PDFParser(),
      reset: (parser) => parser.reset(),
      maxSize: 10,
      minSize: 2
    });
    
    this.rendererPool = new ObjectPool({
      create: () => new PDFRenderer(),
      reset: (renderer) => renderer.reset(),
      maxSize: 5,
      minSize: 1
    });
    
    this.fontCachePool = new ObjectPool({
      create: () => new FontCache({ maxSize: 100 }),
      reset: (cache) => cache.clear(),
      maxSize: 8,
      minSize: 2
    });
  }
  
  async processDocument(path: string): Promise<ProcessingResult> {
    // Acquire resources from pools
    const parser = await this.parserPool.acquire();
    const renderer = await this.rendererPool.acquire();
    const fontCache = await this.fontCachePool.acquire();
    
    try {
      // Set font cache on renderer
      renderer.setFontCache(fontCache);
      
      // Process document
      const document = await parser.parse(path);
      const result = await this.renderDocument(document, renderer);
      
      return result;
    } finally {
      // Always release back to pools
      this.parserPool.release(parser);
      this.rendererPool.release(renderer);
      this.fontCachePool.release(fontCache);
    }
  }
}

// Usage with async/await
const pool = new PDFProcessorPool();

async function batchProcess(documents: string[]): Promise<ProcessingResult[]> {
  const results: ProcessingResult[] = [];
  
  // Process documents sequentially to avoid memory spikes
  for (const doc of documents) {
    const result = await pool.processDocument(doc);
    results.push(result);
  }
  
  return results;
}
```

## Practice 6: Implement Progress Tracking for Long Operations

### Mô tả

Cung cấp progress updates cho các operations mất nhiều thời gian, giúp users biết được operation đang ở đâu và estimate completion time.

```typescript
import { EventEmitter } from 'events';

interface ProgressEvent {
  operation: string;
  phase: string;
  current: number;
  total: number;
  percentage: number;
  elapsedMs: number;
  estimatedRemainingMs: number;
  message?: string;
}

class ProgressTracker extends EventEmitter {
  private startTime: number;
  private phases: Map<string, { current: number; total: number }>;
  
  constructor(private operationName: string) {
    super();
    this.startTime = Date.now();
    this.phases = new Map();
  }
  
  startPhase(name: string, totalItems: number): void {
    this.phases.set(name, { current: 0, total: totalItems });
    this.emitProgress(name, 'started');
  }
  
  updatePhase(name: string, increment: number = 1, message?: string): void {
    const phase = this.phases.get(name);
    if (!phase) return;
    
    phase.current += increment;
    this.emitProgress(name, 'progress', message);
  }
  
  completePhase(name: string): void {
    const phase = this.phases.get(name);
    if (!phase) return;
    
    phase.current = phase.total;
    this.emitProgress(name, 'completed');
  }
  
  private emitProgress(
    phaseName: string, 
    status: string, 
    message?: string
  ): void {
    const event: ProgressEvent = {
      operation: this.operationName,
      phase: phaseName,
      current: this.getTotalCurrent(),
      total: this.getTotalItems(),
      percentage: this.calculateOverallPercentage(),
      elapsedMs: Date.now() - this.startTime,
      estimatedRemainingMs: this.estimateRemainingTime(),
      message
    };
    
    this.emit('progress', event);
  }
}

class PDFProcessingService {
  async processPDFWithProgress(
    inputPath: string,
    outputPath: string,
    onProgress: (event: ProgressEvent) => void
  ): Promise<void> {
    const tracker = new ProgressTracker('PDF Processing');
    tracker.on('progress', onProgress);
    
    // Phase 1: Validation
    tracker.startPhase('validation', 3);
    await this.validateSignature(inputPath);
    tracker.updatePhase('validation', 1, 'Signature validated');
    
    await this.validateStructure(inputPath);
    tracker.updatePhase('validation', 1, 'Structure validated');
    
    await this.validateSecurity(inputPath);
    tracker.updatePhase('validation', 1, 'Security checked');
    tracker.completePhase('validation');
    
    // Phase 2: Parsing
    tracker.startPhase('parsing', 100);
    const document = await this.parseDocument(inputPath, (progress) => {
      tracker.updatePhase('parsing', progress, `Parsing page ${progress}`);
    });
    tracker.completePhase('parsing');
    
    // Phase 3: Transformation
    tracker.startPhase('transformation', 5);
    const transformed = await this.transformDocument(document);
    tracker.completePhase('transformation');
    
    // Phase 4: Export
    tracker.startPhase('export', 100);
    await this.exportDocument(transformed, outputPath, (progress) => {
      tracker.updatePhase('export', progress);
    });
    tracker.completePhase('export');
  }
}
```

## Practice 7: Use Content Hashing for Deduplication

### Mô tả

Implement content-based deduplication để tránh lưu trữ duplicate PDF files, tiết kiệm storage và improve performance.

```typescript
import { createHash } from 'crypto';
import { ContentHasher } from '@enterprise/pdf-hash';

interface DeduplicationService {
  computeContentHash(document: PDFDocument): Promise<string>;
  checkExists(hash: string): Promise<boolean>;
  storeDocument(document: PDFDocument, path: string): Promise<string>;
  retrieveDocument(hash: string): Promise<PDFDocument | null>;
}

class PDFDeduplicationService implements DeduplicationService {
  private hashCache: Map<string, string>;
  
  constructor(
    private storageService: StorageService,
    private cache: CacheService
  ) {
    this.hashCache = new Map();
  }
  
  async computeContentHash(document: PDFDocument): Promise<string> {
    const hasher = new ContentHasher();
    
    // Hash document content (excluding metadata)
    await hasher.update(document.body);
    
    // Include page count
    hasher.update(document.pageCount);
    
    // Include important dictionary values
    for (const font of document.fonts) {
      hasher.update(font.baseFont);
    }
    
    // Include images checksums
    for (const image of document.images) {
      hasher.update(image.checksum);
    }
    
    return hasher.finalize();
  }
  
  async storeDocument(
    document: PDFDocument, 
    desiredPath: string
  ): Promise<string> {
    const hash = await this.computeContentHash(document);
    
    // Check if already exists
    const existing = await this.checkExists(hash);
    if (existing) {
      // Return reference to existing document
      return this.getExistingPath(hash);
    }
    
    // Store new document
    const path = desiredPath || this.generatePath(hash);
    await this.storageService.write(path, document);
    
    // Register in deduplication index
    await this.registerDocument(hash, path, document.metadata);
    
    return path;
  }
  
  private async registerDocument(
    hash: string,
    path: string,
    metadata: DocumentMetadata
  ): Promise<void> {
    await this.cache.put(`dedup:${hash}`, {
      path,
      metadata,
      createdAt: new Date().toISOString(),
      size: metadata.size
    });
    
    // Also store reverse index by path
    await this.cache.put(`path:${metadata.originalPath}`, hash);
  }
}
```

## Practice 8: Implement Proper Cleanup for Temporary Files

### Mô tả

Đảm bảo tất cả temporary files được cleanup đúng cách, tránh disk space leaks và security concerns.

```typescript
import { promises as fs } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';

class TemporaryFileManager {
  private tempFiles: Set<string>;
  private tempDir: string;
  
  constructor() {
    this.tempFiles = new Set();
    this.tempDir = join(tmpdir(), 'pdf-processing');
  }
  
  async initialize(): Promise<void> {
    await fs.mkdir(this.tempDir, { recursive: true });
  }
  
  async createTempFile(suffix: string = '.tmp'): Promise<string> {
    const filename = `pdf-${Date.now()}-${Math.random().toString(36).substr(2, 9)}${suffix}`;
    const filepath = join(this.tempDir, filename);
    
    this.tempFiles.add(filepath);
    return filepath;
  }
  
  async createTempDirectory(): Promise<string> {
    const dirname = `pdf-dir-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const dirpath = join(this.tempDir, dirname);
    
    await fs.mkdir(dirpath, { recursive: true });
    this.tempFiles.add(dirpath);
    
    return dirpath;
  }
  
  async cleanup(): Promise<CleanupResult> {
    const errors: Error[] = [];
    let deletedCount = 0;
    
    for (const filepath of this.tempFiles) {
      try {
        const stat = await fs.stat(filepath);
        
        if (stat.isDirectory()) {
          await fs.rm(filepath, { recursive: true });
        } else {
          await fs.unlink(filepath);
        }
        
        deletedCount++;
      } catch (error) {
        errors.push(error as Error);
      }
    }
    
    this.tempFiles.clear();
    
    return {
      deletedCount,
      errorCount: errors.length,
      errors
    };
  }
  
  async cleanupOnExit(): Promise<void> {
    process.on('exit', () => this.cleanupSync());
    process.on('SIGINT', () => process.exit(1));
    process.on('SIGTERM', () => process.exit(1));
  }
  
  private cleanupSync(): void {
    for (const filepath of this.tempFiles) {
      try {
        require('fs').rmSync(filepath, { recursive: true, force: true });
      } catch {
        // Ignore cleanup errors on exit
      }
    }
  }
}

// Usage in PDF processor
class PDFProcessor {
  private tempManager: TemporaryFileManager;
  
  constructor() {
    this.tempManager = new TemporaryFileManager();
    this.tempManager.cleanupOnExit();
  }
  
  async processWithTempFiles(input: Buffer): Promise<Buffer> {
    // Create temp files for intermediate processing
    const inputTemp = await this.tempManager.createTempFile('.pdf');
    const outputTemp = await this.tempManager.createTempFile('.pdf');
    
    try {
      // Write input to temp
      await fs.writeFile(inputTemp, input);
      
      // Process document
      const result = await this.processDocument(inputTemp, outputTemp);
      
      // Read result
      return await fs.readFile(outputTemp);
      
    } finally {
      // Cleanup happens automatically on exit
      // But we can also force cleanup
      await this.tempManager.cleanup();
    }
  }
}
```

## Practice 9: Implement Rate Limiting for API Endpoints

### Mô tả

Sử dụng rate limiting để bảo vệ PDF processing service khỏi abuse và ensure fair resource allocation.

```typescript
import { RateLimiter } from '@enterprise/rate-limiter';

interface RateLimitConfig {
  windowMs: number;        // Time window in milliseconds
  maxRequests: number;     // Max requests per window
  keyGenerator: (ctx: Context) => string;
  handler: (ctx: Context, retryAfter: number) => void;
}

class PDFProcessingRateLimiter {
  private limiter: RateLimiter;
  
  constructor(private redis: RedisClient) {
    this.limiter = new RateLimiter({
      store: new RedisRateLimitStore(this.redis),
      windowMs: 60 * 1000, // 1 minute window
      maxRequests: {
        create: 100,    // 100 creates per minute
        read: 500,      // 500 reads per minute
        merge: 20,      // 20 merges per minute
        export: 50      // 50 exports per minute
      },
      keyGenerator: (ctx) => `ratelimit:${ctx.userId}:${ctx.operation}`
    });
  }
  
  async checkLimit(
    userId: string, 
    operation: string
  ): Promise<RateLimitResult> {
    const key = `ratelimit:${userId}:${operation}`;
    
    const result = await this.limiter.check(key, {
      limit: this.getOperationLimit(operation),
      windowMs: 60 * 1000
    });
    
    return {
      allowed: result.allowed,
      remaining: result.remaining,
      resetAt: result.resetAt,
      retryAfter: result.retryAfter
    };
  }
  
  private getOperationLimit(operation: string): number {
    const limits: Record<string, number> = {
      create: 100,
      read: 500,
      merge: 20,
      export: 50,
      convert: 30,
      sign: 10
    };
    
    return limits[operation] || 50;
  }
}

// Express middleware
async function rateLimitMiddleware(
  req: Request, 
  res: Response, 
  next: NextFunction
): Promise<void> {
  const userId = req.user?.id || req.ip;
  const operation = req.route?.path || 'unknown';
  
  const result = await rateLimiter.checkLimit(userId, operation);
  
  res.setHeader('X-RateLimit-Limit', result.remaining);
  res.setHeader('X-RateLimit-Remaining', result.remaining);
  res.setHeader('X-RateLimit-Reset', result.resetAt.toISOString());
  
  if (!result.allowed) {
    res.status(429).json({
      error: 'Rate limit exceeded',
      retryAfter: result.retryAfter
    });
    return;
  }
  
  next();
}
```

## Practice 10: Use Digital Signatures for Document Integrity

### Mô tả

Implement digital signatures để verify document integrity và authenticity, đặc biệt quan trọng cho legal và financial documents.

```typescript
import { PKIAdapter } from '@enterprise/pki';
import { TimestampAuthority } from '@enterprise/timestamps';

interface SigningOptions {
  certificatePath: string;
  privateKeyPath: string;
  certificatePassword: string;
  signatureField: string;
  reason: string;
  location: string;
  includeTimestamp: boolean;
  timestampAuthority?: string;
}

class PDFSigningService {
  private pkiAdapter: PKIAdapter;
  private tsa: TimestampAuthority;
  
  constructor(
    pkiService: PKIService,
    tsaService: TimestampAuthorityService
  ) {
    this.pkiAdapter = new PKIAdapter(pkiService);
    this.tsa = new TimestampAuthority(tsaService);
  }
  
  async signDocument(
    document: PDFDocument,
    options: SigningOptions
  ): Promise<PDFDocument> {
    // Load certificate and private key
    const certificate = await this.pkiAdapter.loadCertificate(options.certificatePath);
    const privateKey = await this.pkiAdapter.loadPrivateKey(
      options.privateKeyPath,
      options.certificatePassword
    );
    
    // Create signature field if not exists
    const signatureField = await this.createSignatureField(
      document,
      options.signatureField
    );
    
    // Calculate document hash
    const hash = await this.calculateDocumentHash(document);
    
    // Sign hash with private key
    const signature = await this.pkiAdapter.sign(hash, privateKey);
    
    // Get timestamp if enabled
    let timestamp: Timestamp | undefined;
    if (options.includeTimestamp && options.timestampAuthority) {
      timestamp = await this.tsa.requestTimestamp(signature, options.timestampAuthority);
    }
    
    // Embed signature in document
    const signedDoc = await this.embedSignature(
      document,
      signatureField,
      signature,
      certificate,
      timestamp
    );
    
    // Verify signature immediately
    await this.verifySignature(signedDoc, signatureField);
    
    return signedDoc;
  }
  
  async verifySignature(
    document: PDFDocument,
    signatureField: string
  ): Promise<VerificationResult> {
    // Extract signature data
    const signatureData = await this.extractSignatureData(document, signatureField);
    
    // Extract certificate
    const certificate = signatureData.certificate;
    
    // Verify certificate chain
    const chainResult = await this.pkiAdapter.verifyCertificateChain(certificate);
    if (!chainResult.valid) {
      return {
        valid: false,
        errors: chainResult.errors
      };
    }
    
    // Check certificate validity dates
    const now = new Date();
    if (now < certificate.notBefore || now > certificate.notAfter) {
      return {
        valid: false,
        errors: ['Certificate has expired or is not yet valid']
      };
    }
    
    // Verify signature
    const hash = await this.calculateDocumentHash(document);
    const signatureValid = await this.pkiAdapter.verify(
      hash,
      signatureData.signature,
      certificate.publicKey
    );
    
    if (!signatureValid) {
      return {
        valid: false,
        errors: ['Signature verification failed - document may have been modified']
      };
    }
    
    // Verify timestamp if present
    if (signatureData.timestamp) {
      const tsaResult = await this.tsa.verifyTimestamp(signatureData.timestamp);
      if (!tsaResult.valid) {
        return {
          valid: false,
          errors: ['Timestamp verification failed', ...tsaResult.errors]
        };
      }
    }
    
    return {
      valid: true,
      certificateInfo: {
        subject: certificate.subject,
        issuer: certificate.issuer,
        serialNumber: certificate.serialNumber
      },
      signatureInfo: {
        signedAt: signatureData.signedAt,
        timestamp: signatureData.timestamp
      }
    };
  }
}
```

## Practice 11: Monitor PDF Processing Metrics

### Mô tả

Implement comprehensive metrics collection để monitor health, performance, và capacity planning của PDF processing system.

```typescript
import { MetricsCollector } from '@enterprise/metrics';

interface PDFMetrics {
  // Counters
  documentsProcessed: Counter;
  documentsFailed: Counter;
  operationsByType: Counter;
  
  // Histograms
  processingDuration: Histogram;
  fileSizeBytes: Histogram;
  pageCount: Histogram;
  
  // Gauges
  activeOperations: Gauge;
  queueDepth: Gauge;
}

class PDFMetricsCollector {
  private metrics: PDFMetrics;
  
  constructor(private prometheus: PrometheusClient) {
    this.initializeMetrics();
  }
  
  private initializeMetrics(): void {
    this.metrics = {
      documentsProcessed: new Counter({
        name: 'pdf_documents_processed_total',
        help: 'Total number of PDF documents processed',
        labelNames: ['operation', 'status']
      }),
      
      documentsFailed: new Counter({
        name: 'pdf_documents_failed_total',
        help: 'Total number of PDF processing failures',
        labelNames: ['operation', 'error_type']
      }),
      
      operationsByType: new Counter({
        name: 'pdf_operations_total',
        help: 'PDF operations by type',
        labelNames: ['operation_type']
      }),
      
      processingDuration: new Histogram({
        name: 'pdf_processing_duration_seconds',
        help: 'PDF processing duration',
        buckets: [0.1, 0.5, 1, 2, 5, 10, 30, 60, 120, 300]
      }),
      
      fileSizeBytes: new Histogram({
        name: 'pdf_file_size_bytes',
        help: 'PDF file sizes',
        buckets: [1024, 10240, 102400, 1048576, 10485760, 104857600]
      }),
      
      pageCount: new Histogram({
        name: 'pdf_page_count',
        help: 'PDF page counts',
        buckets: [1, 5, 10, 25, 50, 100, 250, 500, 1000]
      }),
      
      activeOperations: new Gauge({
        name: 'pdf_active_operations',
        help: 'Number of currently active PDF operations'
      }),
      
      queueDepth: new Gauge({
        name: 'pdf_queue_depth',
        help: 'Number of PDF jobs in queue'
      })
    };
  }
  
  async processWithMetrics(
    operation: string,
    document: PDFDocument,
    processor: () => Promise<void>
  ): Promise<void> {
    const timer = this.metrics.processingDuration.startTimer({
      operation
    });
    
    this.metrics.activeOperations.inc({ operation });
    this.metrics.fileSizeBytes.observe(document.size);
    this.metrics.pageCount.observe(document.pageCount);
    this.metrics.operationsByType.inc({ operation_type: operation });
    
    try {
      await processor();
      
      this.metrics.documentsProcessed.inc({
        operation,
        status: 'success'
      });
      
    } catch (error) {
      this.metrics.documentsFailed.inc({
        operation,
        error_type: this.categorizeError(error)
      });
      throw error;
      
    } finally {
      this.metrics.activeOperations.dec({ operation });
      timer();
    }
  }
  
  private categorizeError(error: Error): string {
    if (error instanceof PDFValidationError) return 'validation';
    if (error instanceof PDFEncryptionError) return 'encryption';
    if (error instanceof PDFParseError) return 'parse';
    return 'unknown';
  }
}
```

## Related Documents

- [PDF Glossary](../glossary.md)
- [PDF Architecture](../architecture.md)
- [PDF Anti-Patterns](../anti-pattern.md)
- [PDF Checklist](../checklist.md)
- [PDF FAQ](../faq.md)
- [PDF Decision Tree](../decision-tree.md)
