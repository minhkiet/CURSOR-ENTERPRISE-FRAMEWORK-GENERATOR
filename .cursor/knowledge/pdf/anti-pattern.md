# PDF Knowledge Base - Anti-Patterns

## Tổng quan

Document này liệt kê các anti-patterns phổ biến trong xử lý PDF và đề xuất giải pháp thay thế. Mỗi anti-pattern được mô tả chi tiết với ví dụ về cách phát hiện và khắc phục.

## Anti-Pattern 1: Loading Entire PDF Into Memory

### Mô tả

Một trong những lỗi phổ biến nhất là load toàn bộ PDF file vào memory trước khi xử lý. Điều này gây ra memory spikes và có thể crash application khi xử lý large PDF files.

### Ví dụ xấu

```typescript
// ❌ ANTI-PATTERN: Loading entire file into memory
async function processPDF(path: string): Promise<ProcessingResult> {
  // Load entire file - BAD for large files!
  const fileBuffer = await fs.readFile(path);
  
  // Parse entire document
  const document = pdfParser.parse(fileBuffer);
  
  // Process document
  const result = await processDocument(document);
  
  return result;
}

// Even worse: processing multiple large PDFs
async function batchProcess(paths: string[]): Promise<ProcessingResult[]> {
  const documents = await Promise.all(
    paths.map(async (path) => {
      const buffer = await fs.readFile(path); // All files in memory!
      return pdfParser.parse(buffer);
    })
  );
  
  return documents.map(processDocument);
}
```

### Giải pháp

```typescript
// ✅ SOLUTION: Stream-based processing
class StreamPDFProcessor {
  async processPDF(
    inputPath: string, 
    outputPath: string
  ): Promise<void> {
    const readStream = createReadStream(inputPath, {
      highWaterMark: 64 * 1024 // 64KB chunks
    });
    
    const writeStream = createWriteStream(outputPath);
    const pdfStream = new PDFTransformStream({
      mode: 'process',
      onProgress: (progress) => this.emit('progress', progress)
    });
    
    await pipeline(
      readStream,
      pdfStream,
      writeStream
    );
  }
  
  // For content extraction with progress tracking
  async extractTextWithProgress(
    path: string,
    onProgress: (percent: number) => void
  ): Promise<string> {
    const stat = await fs.stat(path);
    const totalSize = stat.size;
    let processedSize = 0;
    
    return new Promise((resolve, reject) => {
      const chunks: string[] = [];
      const stream = createReadStream(path);
      
      stream.on('data', async (chunk: Buffer) => {
        processedSize += chunk.length;
        onProgress((processedSize / totalSize) * 100);
        
        // Process chunk immediately
        const text = await this.extractTextFromChunk(chunk);
        chunks.push(text);
      });
      
      stream.on('end', () => resolve(chunks.join('')));
      stream.on('error', reject);
    });
  }
}

// For batch processing with memory management
async function batchProcessManaged(
  paths: string[],
  options: { concurrency: number; maxMemoryMB: number }
): Promise<ProcessingResult[]> {
  const semaphore = new Semaphore(options.concurrency);
  const memoryGuard = new MemoryGuard(options.maxMemoryMB);
  
  const results: ProcessingResult[] = [];
  
  for (const path of paths) {
    await semaphore.acquire();
    
    // Wait if memory is running low
    await memoryGuard.waitIfNeeded();
    
    const result = await processPDFManaged(path);
    results.push(result);
    
    // Force garbage collection if needed
    if (memoryGuard.shouldGC()) {
      global.gc();
    }
    
    semaphore.release();
  }
  
  return results;
}
```

## Anti-Pattern 2: Ignoring Font Embedding

### Mô tả

Khi tạo PDF mà không embed fonts, document có thể hiển thị sai trên systems không có fonts được sử dụng. Đây là vấn đề nghiêm trọng cho PDF/A compliance.

### Ví dụ xấu

```typescript
// ❌ ANTI-PATTERN: Not embedding fonts
function createPDFWithSystemFonts(): Buffer {
  const doc = new PDFDocument();
  
  doc.font('Helvetica'); // System font - NOT embedded!
  doc.text('Hello World');
  
  return doc.save();
}

// Another bad pattern: using custom fonts without embedding
function createPDFWithCustomFonts(): Buffer {
  const doc = new PDFDocument();
  
  doc.font('/path/to/font.ttf'); // Font not embedded
  doc.text('Custom Font Text');
  
  return doc.save(); // Font reference will break!
}
```

### Giải pháp

```typescript
// ✅ SOLUTION: Proper font embedding
class FontEmbeddingPDFCreator {
  async createPDFWithEmbeddedFonts(
    content: PDFContent
  ): Promise<PDFDocument> {
    const doc = new PDFDocument({
      autoFirstPage: true
    });
    
    // Collect all fonts used
    const fontPaths = this.collectFontPaths(content);
    
    // Embed each font
    const embeddedFonts = await Promise.all(
      fontPaths.map(async (path) => {
        const fontData = await fs.readFile(path);
        const font = await doc.embedFont(fontData, {
          subset: true, // Subset for smaller file size
          embed: true
        });
        return { name: path, font };
      })
    );
    
    // Create font map
    const fontMap = new Map(
      embeddedFonts.map(({ name, font }) => [name, font])
    );
    
    // Generate content with embedded fonts
    for (const block of content.blocks) {
      const font = fontMap.get(block.fontPath);
      if (!font) {
        throw new Error(`Font not found: ${block.fontPath}`);
      }
      
      doc.useFont(font);
      doc.text(block.text, block.position);
    }
    
    // Ensure all fonts are embedded in output
    await doc.finalizeFonts();
    
    return doc;
  }
  
  private collectFontPaths(content: PDFContent): string[] {
    const fonts = new Set<string>();
    
    for (const block of content.blocks) {
      if (block.fontPath) {
        fonts.add(block.fontPath);
      }
    }
    
    return Array.from(fonts);
  }
}

// For PDF/A compliance specifically
class PDFACompliantCreator {
  async createPDFA(
    content: PDFContent,
    options: PDFAOptions
  ): Promise<Buffer> {
    const doc = await this.createPDFWithEmbeddedFonts(content);
    
    // Add required PDF/A metadata
    doc.setMetadata({
      title: options.title,
      author: options.author,
      creator: 'Enterprise PDF Generator',
      creationDate: new Date(),
      modificationDate: new Date()
    });
    
    // Embed all fonts (required for PDF/A)
    await this.ensureAllFontsEmbedded(doc);
    
    // Add structure tags
    this.addStructureTags(doc);
    
    // Validate PDF/A compliance
    const validator = new PDFAValidator();
    const result = await validator.validate(doc);
    
    if (!result.isCompliant) {
      throw new PDFANonComplianceError(result.issues);
    }
    
    return doc.save();
  }
}
```

## Anti-Pattern 3: No Error Handling for Corrupted Files

### Mô tả

Ignoring potential errors when processing potentially corrupted or malformed PDF files can lead to crashes, security vulnerabilities, hoặc data corruption.

### Ví dụ xấu

```typescript
// ❌ ANTI-PATTERN: No error handling
async function processPDFUnsafe(path: string): Promise<Result> {
  const buffer = await fs.readFile(path);
  
  // No validation!
  const doc = pdfParser.parse(buffer);
  
  // No try-catch!
  const text = doc.extractText();
  const images = doc.extractImages();
  
  return { text, images };
}

// Another bad pattern: swallowing errors silently
async function processWithSilentFailures(path: string): Promise<Result | null> {
  try {
    const doc = await pdfParser.parse(path);
    return await processDocument(doc);
  } catch (error) {
    // Silent failure - no logging, no indication of failure
    return null;
  }
}
```

### Giải pháp

```typescript
// ✅ SOLUTION: Comprehensive error handling
class SafePDFProcessor {
  private logger: Logger;
  
  async processPDFWithErrorHandling(
    path: string,
    options: ProcessingOptions = {}
  ): Promise<ProcessingResult> {
    // Step 1: Pre-validation
    const validationResult = await this.validatePDF(path);
    
    if (!validationResult.isValid) {
      return {
        success: false,
        error: {
          type: 'VALIDATION_ERROR',
          code: validationResult.errorCode,
          message: validationResult.errorMessage,
          details: validationResult.details
        },
        recoverable: true
      };
    }
    
    // Step 2: Safe parsing with timeout
    try {
      const doc = await this.parseWithTimeout(path, options.timeout || 30000);
      return await this.processDocument(doc, options);
      
    } catch (error) {
      if (error instanceof PDFParseError) {
        return this.handleParseError(error, path);
      }
      
      if (error instanceof TimeoutError) {
        return this.handleTimeoutError(path);
      }
      
      return this.handleUnexpectedError(error, path);
    }
  }
  
  private async validatePDF(path: string): Promise<ValidationResult> {
    // Check file signature
    const buffer = Buffer.alloc(8);
    const { bytesRead } = await fs.open(path, 'r')
      .then(async (fd) => {
        const result = await fd.read(buffer, 0, 8, 0);
        await fd.close();
        return result;
      });
    
    // Verify PDF magic bytes
    const signature = buffer.toString('ascii', 0, 5);
    if (signature !== '%PDF-') {
      return {
        isValid: false,
        errorCode: 'INVALID_SIGNATURE',
        errorMessage: `Invalid PDF signature: ${signature}`
      };
    }
    
    // Check file integrity
    const integrityResult = await this.checkIntegrity(path);
    if (!integrityResult.valid) {
      return {
        isValid: false,
        errorCode: 'CORRUPTED_FILE',
        errorMessage: 'PDF file appears to be corrupted',
        details: integrityResult.issues
      };
    }
    
    return { isValid: true };
  }
  
  private handleParseError(error: PDFParseError, path: string): ProcessingResult {
    this.logger.error({
      event: 'PDF_PARSE_ERROR',
      path,
      error: {
        message: error.message,
        offset: error.location?.offset,
        line: error.location?.line,
        column: error.location?.column
      }
    });
    
    return {
      success: false,
      error: {
        type: 'PARSE_ERROR',
        message: `Failed to parse PDF: ${error.message}`,
        recoverable: error.recoverable
      }
    };
  }
}

// Custom error classes for better error handling
class PDFProcessingError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly recoverable: boolean,
    public readonly details?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'PDFProcessingError';
  }
}

class PDFValidationError extends PDFProcessingError {
  constructor(message: string, details?: Record<string, unknown>) {
    super(message, 'VALIDATION_ERROR', true, details);
    this.name = 'PDFValidationError';
  }
}

class PDFParseError extends PDFProcessingError {
  constructor(
    message: string,
    public readonly location?: { offset: number; line: number; column: number }
  ) {
    super(message, 'PARSE_ERROR', false);
    this.name = 'PDFParseError';
  }
}
```

## Anti-Pattern 4: Storing Passwords in Plain Text

### Mô tả

Lưu trữ passwords hoặc encryption keys trong code hoặc configuration files không được mã hóa là một security anti-pattern nghiêm trọng.

### Ví dụ xấu

```typescript
// ❌ ANTI-PATTERN: Hardcoded passwords
const PDF_ENCRYPTION_PASSWORD = 'MySecretPassword123';

// Using hardcoded password
async function encryptPDF(path: string): Promise<Buffer> {
  const doc = await PDFDocument.load(path);
  
  doc.encrypt({
    userPassword: 'MySecretPassword123', // Hardcoded!
    ownerPassword: 'AnotherPassword',     // Hardcoded!
    permissions: {
      printing: true,
      modifying: false
    }
  });
  
  return doc.save();
}

// Another bad pattern: password in config file
// config.json
// {
//   "pdfPassword": "secret123"
// }
```

### Giải pháp

```typescript
// ✅ SOLUTION: Secure credential management
class SecurePDFProcessor {
  private keyVault: KeyVaultClient;
  
  constructor(keyVault: KeyVaultClient) {
    this.keyVault = keyVault;
  }
  
  async encryptPDF(
    path: string,
    options: EncryptionOptions
  ): Promise<Buffer> {
    // Retrieve password from secure vault
    const password = await this.keyVault.getSecret('pdf-encryption-key');
    
    // Additional security: rotate password periodically
    const sessionKey = await this.keyVault.getSessionKey(password, {
      purpose: 'pdf-encryption',
      validity: '24h'
    });
    
    const doc = await PDFDocument.load(path);
    
    doc.encrypt({
      userPassword: sessionKey.userPassword,
      ownerPassword: sessionKey.ownerPassword,
      permissions: options.permissions
    });
    
    // Clear sensitive data from memory
    sessionKey.clear();
    
    return doc.save();
  }
}

// Environment-based configuration with secrets manager
class ConfigurationLoader {
  private secretsManager: AWSSecretsManager; // or HashiCorp Vault, etc.
  
  async loadConfiguration(): Promise<Configuration> {
    // Load non-sensitive config from file
    const baseConfig = await this.loadFromFile('config.json');
    
    // Load sensitive config from secrets manager
    const secrets = await this.secretsManager.getSecret('production/pdf-settings');
    
    return {
      ...baseConfig,
      pdfEncryptionKey: secrets.pdfEncryptionKey,
      signingCertificate: secrets.signingCertificate,
      signingPrivateKey: secrets.signingPrivateKey
    };
  }
}

// Using environment variables with validation
class EnvironmentValidator {
  validate(): void {
    const required = ['PDF_ENCRYPTION_KEY_REF', 'PDF_SIGNING_CERT_PATH'];
    
    for (const key of required) {
      if (!process.env[key]) {
        throw new ConfigurationError(`Missing required environment variable: ${key}`);
      }
    }
  }
  
  getEncryptionKey(): Buffer {
    const keyRef = process.env.PDF_ENCRYPTION_KEY_REF;
    
    // Key reference should point to a secret manager
    if (keyRef.startsWith('arn:')) {
      return this.secretsManager.getSecret(keyRef);
    }
    
    throw new Error('Encryption key must be stored in secrets manager');
  }
}
```

## Anti-Pattern 5: Synchronous File I/O in Request Handlers

### Mô tả

Sử dụng synchronous file operations trong request handlers blocks event loop và prevents application từ handling other requests.

### Ví dụ xấu

```typescript
// ❌ ANTI-PATTERN: Synchronous file I/O
import { readFileSync, writeFileSync } from 'fs';

app.post('/api/pdf/process', async (req, res) => {
  const { filePath, operation } = req.body;
  
  // Synchronous operations - blocks event loop!
  const buffer = readFileSync(filePath);     // BAD!
  const doc = pdfParser.parse(buffer);
  
  const result = await processDocument(doc);
  
  // More synchronous operations!
  writeFileSync(outputPath, result.buffer);   // BAD!
  
  res.json({ success: true, path: outputPath });
});

// Another bad pattern: using synchronous operations in loops
async function batchProcessSync(paths: string[]): Promise<void> {
  for (const path of paths) {
    // Synchronous in a loop - very bad!
    const data = readFileSync(path);
    await processData(data);
  }
}
```

### Giải pháp

```typescript
// ✅ SOLUTION: Async file I/O with streaming
import { createReadStream, createWriteStream, pipeline } from 'fs';
import { promisify } from 'util';

const pipelineAsync = promisify(pipeline);

app.post('/api/pdf/process', async (req, res) => {
  const { filePath, operation } = req.body;
  
  // Use streaming for better performance
  const resultPath = await this.processPDFStream(filePath, operation);
  
  res.json({ success: true, path: resultPath });
});

class StreamPDFProcessor {
  async processPDFStream(
    inputPath: string,
    operation: string
  ): Promise<string> {
    const outputPath = this.generateOutputPath(inputPath, operation);
    
    const readStream = createReadStream(inputPath);
    const processor = this.createProcessor(operation);
    const writeStream = createWriteStream(outputPath);
    
    await pipelineAsync(readStream, processor, writeStream);
    
    return outputPath;
  }
  
  async processLargePDF(
    inputPath: string,
    options: ProcessingOptions
  ): Promise<string> {
    const outputPath = this.generateOutputPath(inputPath, options.operation);
    
    // Use streams throughout
    const inputStream = createReadStream(inputPath, {
      highWaterMark: 1024 * 1024 // 1MB chunks
    });
    
    const processor = this.createStreamingProcessor(options);
    const outputStream = createWriteStream(outputPath, {
      highWaterMark: 1024 * 1024
    });
    
    // Pipeline handles backpressure automatically
    await pipelineAsync(inputStream, processor, outputStream);
    
    return outputPath;
  }
}

// For batch processing with proper async patterns
class BatchPDFProcessor {
  async batchProcessAsync(
    paths: string[],
    options: BatchOptions
  ): Promise<BatchResult[]> {
    // Use Promise.all for parallel processing
    // but with concurrency limit
    const semaphore = new Semaphore(options.concurrency || 5);
    
    const tasks = paths.map((path) => 
      semaphore.acquire().then(async () => {
        try {
          const result = await this.processPDFAsync(path, options);
          return { path, success: true, result };
        } finally {
          semaphore.release();
        }
      })
    );
    
    const results = await Promise.allSettled(tasks);
    
    return results.map((result, index) => {
      if (result.status === 'fulfilled') {
        return result.value;
      }
      return {
        path: paths[index],
        success: false,
        error: result.reason.message
      };
    });
  }
}
```

## Anti-Pattern 6: Not Validating User Input Before PDF Operations

### Mô tả

Không validate user input trước khi sử dụng trong PDF operations có thể dẫn đến injection attacks, buffer overflows, hoặc unexpected behavior.

### Ví dụ xấu

```typescript
// ❌ ANTI-PATTERN: No input validation
app.post('/api/pdf/merge', async (req, res) => {
  const { files, outputName } = req.body;
  
  // No validation at all!
  const merger = new PDFMerger();
  
  for (const file of files) {
    merger.add(file.path); // User-controlled path!
  }
  
  await merger.merge(outputName); // User-controlled filename!
  
  res.json({ success: true });
});

// Another bad pattern: trusting file extensions
app.post('/api/pdf/upload', async (req, res) => {
  const file = req.files[0];
  
  // Just checking extension is not enough!
  if (file.originalname.endsWith('.pdf')) {
    await processPDF(file.path);
  }
});
```

### Giải pháp

```typescript
// ✅ SOLUTION: Comprehensive input validation
class PDFInputValidator {
  private readonly MAX_FILE_SIZE = 100 * 1024 * 1024; // 100MB
  private readonly ALLOWED_MIME_TYPES = ['application/pdf'];
  private readonly ALLOWED_EXTENSIONS = ['.pdf'];
  
  validateMergeRequest(input: MergeRequest): ValidationResult {
    const errors: string[] = [];
    
    // Validate files array
    if (!Array.isArray(input.files) || input.files.length < 2) {
      errors.push('At least 2 files required for merge');
    }
    
    if (input.files.length > 50) {
      errors.push('Maximum 50 files can be merged at once');
    }
    
    // Validate each file
    for (let i = 0; i < input.files.length; i++) {
      const file = input.files[i];
      const fileErrors = this.validateFile(file, `files[${i}]`);
      errors.push(...fileErrors);
    }
    
    // Validate output name
    const outputErrors = this.validateOutputName(input.outputName);
    errors.push(...outputErrors);
    
    return {
      valid: errors.length === 0,
      errors
    };
  }
  
  private validateFile(file: any, context: string): string[] {
    const errors: string[] = [];
    
    // Check file exists and is readable
    if (!file.path) {
      errors.push(`${context}: File path is required`);
      return errors;
    }
    
    // Path traversal protection
    if (this.containsPathTraversal(file.path)) {
      errors.push(`${context}: Invalid file path - path traversal detected`);
      return errors;
    }
    
    // Check file extension
    if (!this.hasValidExtension(file.path)) {
      errors.push(`${context}: Only PDF files are allowed`);
      return errors;
    }
    
    // Check file size
    if (file.size && file.size > this.MAX_FILE_SIZE) {
      errors.push(`${context}: File exceeds maximum size of ${this.MAX_FILE_SIZE} bytes`);
    }
    
    // Verify it's actually a PDF
    if (file.buffer) {
      const isPDF = this.isValidPDFSignature(file.buffer);
      if (!isPDF) {
        errors.push(`${context}: File is not a valid PDF`);
      }
    }
    
    return errors;
  }
  
  private validateOutputName(name: string): string[] {
    const errors: string[] = [];
    
    if (!name || typeof name !== 'string') {
      errors.push('Output name is required');
      return errors;
    }
    
    if (name.length > 255) {
      errors.push('Output name too long');
    }
    
    // Sanitize filename
    const sanitized = this.sanitizeFilename(name);
    if (sanitized !== name) {
      errors.push('Output name contains invalid characters');
    }
    
    // Prevent path traversal in output name
    if (name.includes('..') || name.includes('/') || name.includes('\\')) {
      errors.push('Output name cannot contain path separators');
    }
    
    return errors;
  }
  
  private containsPathTraversal(path: string): boolean {
    const normalized = path.replace(/\\/g, '/').replace(/\/+/g, '/');
    return normalized.includes('../') || normalized.startsWith('/');
  }
  
  private isValidPDFSignature(buffer: Buffer): boolean {
    if (buffer.length < 5) return false;
    return buffer.toString('ascii', 0, 5) === '%PDF-';
  }
  
  private sanitizeFilename(name: string): string {
    return name.replace(/[<>:"|?*]/g, '_').substring(0, 255);
  }
}

// Using validator in request handler
app.post('/api/pdf/merge', async (req, res) => {
  const validator = new PDFInputValidator();
  const validation = validator.validateMergeRequest(req.body);
  
  if (!validation.valid) {
    return res.status(400).json({
      error: 'Validation failed',
      details: validation.errors
    });
  }
  
  // Safe to proceed with validated input
  const result = await pdfService.merge(req.body.files, req.body.outputName);
  
  res.json({ success: true, result });
});
```

## Related Documents

- [PDF Glossary](../glossary.md)
- [PDF Architecture](../architecture.md)
- [PDF Best Practices](../best-practice.md)
- [PDF Checklist](../checklist.md)
- [PDF FAQ](../faq.md)
- [PDF Decision Tree](../decision-tree.md)
