# PDF Knowledge Base - Architecture

## Tổng quan Kiến trúc PDF trong Enterprise Framework

Document này mô tả chi tiết kiến trúc hệ thống xử lý PDF được thiết kế cho Cursor Enterprise Framework. Kiến trúc được xây dựng trên nguyên tắc modularity, scalability, và maintainability.

## 1. High-Level Architecture Overview

### 1.1 System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     PDF Processing Gateway                        │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤
│  Ingestion  │ Transformation│  Validation │  Rendering  │ Export  │
│   Layer     │    Layer      │    Layer    │    Layer    │  Layer  │
├─────────────┴─────────────┴─────────────┴─────────────┴─────────┤
│                    Core PDF Engine                                │
├─────────────────────────────────────────────────────────────────┤
│  Object Model  │  Stream Handler  │  Security  │  Metadata        │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Responsibilities

#### Ingestion Layer
- Tiếp nhận PDF files từ nhiều nguồn: upload, email, API, scheduled jobs
- Thực hiện preliminary validation (file signature, basic structure)
- Routing đến appropriate processing pipeline
- Quản lý temporary storage và cleanup

#### Transformation Layer
- Xử lý content extraction và manipulation
- Thực hiện merge, split, rotate, watermark operations
- Handle form processing (fill, flatten, export data)
- Implement compression optimization

#### Validation Layer
- Kiểm tra PDF/A compliance
- Verify structural integrity
- Check accessibility requirements
- Validate digital signatures

#### Rendering Layer
- Convert PDF pages sang images (PNG, JPEG, TIFF)
- Generate thumbnails cho preview
- Create print-ready output
- Support vector output (SVG)

#### Export Layer
- Export sang various formats (HTML, DOCX, plain text)
- Generate archive-ready PDF/A files
- Create optimized web versions
- Produce print-optimized PDFs

## 2. Core PDF Engine Architecture

### 2.1 Object Model Design

```typescript
// PDF Document Object Model
interface PDFDocument {
  header: PDFHeader;
  body: Map<PDFObjectNumber, PDFObject>;
  xrefTable: CrossReferenceTable;
  trailer: PDFTrailer;
  
  // Methods
  getPage(pageNumber: number): PDFPage;
  getObject(objectNumber: number): PDFObject;
  updateObject(objNum: number, obj: PDFObject): void;
  write(output: WritableStream): Promise<void>;
}

interface PDFPage {
  objectNumber: PDFObjectNumber;
  dictionary: PDFDictionary;
  contentStreams: ContentStream[];
  annotations: Annotation[];
  
  // Methods
  render(ctx: RenderContext): Promise<RenderedPage>;
  extractText(): string;
  getImages(): EmbeddedImage[];
}
```

### 2.2 Stream Processing Pipeline

```
┌──────────┐    ┌───────────┐    ┌───────────┐    ┌──────────┐
│ Raw Data │───▶│  Decode   │───▶│  Parse    │───▶│  Object  │
│  Stream  │    │  Filter   │    │  Content  │    │   Model  │
└──────────┘    └───────────┘    └───────────┘    └──────────┘
                    │                                   │
                    ▼                                   ▼
              ┌───────────┐                      ┌───────────┐
              │  Encode   │◀─── Transform ────▶│   Render  │
              │  Filter   │                     │   Output  │
              └───────────┘                      └───────────┘
```

### 2.3 Memory Management Strategy

PDF files có thể rất lớn, do đó cần chiến lược memory management hiệu quả:

```typescript
interface MemoryManager {
  // Chunked reading cho large files
  readChunked(file: PDFSource, 
              options: { chunkSize: number; onProgress: (p: number) => void }): 
    AsyncIterable<PDFFragment>;
  
  // Object pooling cho frequently accessed objects
  getObjectPool(objectType: PDFObjectType): ObjectPool;
  
  // Lazy loading cho page content
  getPageLazy(pageNum: number): Lazy<PDFPage>;
}
```

## 3. Security Architecture

### 3.1 Encryption Subsystem

```typescript
interface EncryptionManager {
  // Encryption algorithms supported
  supportedAlgorithms: ['RC4-40', 'RC4-128', 'AES-128', 'AES-256'];
  
  // Encrypt PDF document
  encrypt(doc: PDFDocument, config: EncryptionConfig): Promise<EncryptedDocument>;
  
  // Decrypt PDF document
  decrypt(doc: EncryptedDocument, credentials: Credentials): Promise<PDFDocument>;
  
  // Verify password
  verifyPassword(doc: EncryptedDocument, password: string): boolean;
}

interface EncryptionConfig {
  algorithm: EncryptionAlgorithm;
  userPassword: string;
  ownerPassword: string;
  permissions: PermissionFlags;
}
```

### 3.2 Digital Signature Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Signature Processing Pipeline                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐       │
│  │  Hash   │───▶│  Sign   │───▶│ Embed   │───▶│ Verify  │       │
│  │ Document│   │ w/ Key  │   │  Sig    │   │  on Open│       │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘       │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              Certificate Management                      │     │
│  │  - Certificate Chain Validation                          │     │
│  │  - CRL/OCSP Checking                                     │     │
│  │  - Timestamp Authority Integration                        │     │
│  └─────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 Permission System

```typescript
interface PermissionManager {
  permissions: {
    print: boolean;           // Inferred: P+4
    modifyContent: boolean;   // Inferred: P+8
    extractContent: boolean;  // Inferred: P+16
    modifyAnnotations: boolean; // Inferred: P+32
    fillForms: boolean;       // Inferred: P+256
    extractAccessibility: boolean; // Inferred: P+512
    assemble: boolean;        // Inferred: P+1024
    printDegraded: boolean;   // Inferred: P+2048
  };
  
  checkPermission(operation: string): boolean;
  applyRestrictions(doc: PDFDocument, permissions: PermissionFlags): void;
}
```

## 4. Processing Pipelines

### 4.1 PDF/A Conversion Pipeline

```typescript
interface PDFAConversionPipeline {
  stages: [
    PreFlightCheck,        // Analyze source PDF
    FontEmbedding,         // Embed all fonts
    ColorspaceConversion,   // Convert to allowed colorspaces
    MetadataFixup,         // Add/fix XMP metadata
    StructureTagging,       // Add logical structure
    Validation,            // Final compliance check
    OutputGeneration       // Write PDF/A file
  ];
  
  execute(source: PDFSource, targetFormat: PDFAType): 
    Promise<ConversionResult>;
}

type PDFAType = 'pdf/a-1a' | 'pdf/a-1b' | 'pdf/a-2a' | 'pdf/a-2b' | 
                'pdf/a-3a' | 'pdf/a-3b';
```

### 4.2 Content Extraction Pipeline

```typescript
interface ContentExtractionPipeline {
  // Extract text với layout preservation
  extractText(options: TextExtractionOptions): Promise<ExtractedText>;
  
  // Extract images với metadata
  extractImages(options: ImageExtractionOptions): Promise<ExtractedImage[]>;
  
  // Extract metadata
  extractMetadata(): Promise<DocumentMetadata>;
  
  // Extract form data
  extractFormData(): Promise<FormData>;
}

interface TextExtractionOptions {
  preserveLayout: boolean;
  combineLines: boolean;
  includeHidden: boolean;
  pageRange?: PageRange;
}
```

### 4.3 Merge/Split Pipeline

```typescript
interface DocumentAssemblyPipeline {
  // Merge multiple PDFs
  merge(sources: PDFSource[], options: MergeOptions): Promise<PDFDocument>;
  
  // Split PDF
  split(source: PDFSource, criteria: SplitCriteria): Promise<PDFDocument[]>;
  
  // Extract pages
  extractPages(source: PDFSource, pages: number[]): Promise<PDFDocument>;
  
  // Rotate pages
  rotatePages(source: PDFSource, rotations: Map<number, Rotation>): Promise<PDFDocument>;
}
```

## 5. Storage Architecture

### 5.1 Document Repository Design

```typescript
interface PDFRepository {
  // Store PDF với metadata
  store(doc: PDFDocument, metadata: DocumentMetadata): Promise<DocumentRef>;
  
  // Retrieve PDF
  retrieve(ref: DocumentRef): Promise<PDFDocument>;
  
  // Update PDF
  update(ref: DocumentRef, doc: PDFDocument): Promise<void>;
  
  // Delete PDF
  delete(ref: DocumentRef): Promise<void>;
  
  // Search PDFs
  search(query: SearchQuery): Promise<DocumentRef[]>;
}

interface DocumentRef {
  id: string;
  version: number;
  storagePath: string;
  checksum: string;
  metadata: DocumentMetadata;
}
```

### 5.2 Caching Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Level Cache                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  L1: In-Memory Cache (LRU)                                       │
│      - Recently accessed documents                                │
│      - Page content caches                                       │
│      - Metadata caches                                          │
│                                                                   │
│  L2: Local Disk Cache                                            │
│      - Processed pages (images)                                  │
│      - Extraction results                                        │
│      - Temporary processing artifacts                            │
│                                                                   │
│  L3: Distributed Cache (Redis)                                  │
│      - Shared extraction results                                │
│      - Session data                                             │
│      - Rate limiting counters                                   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 6. API Architecture

### 6.1 REST API Endpoints

```yaml
/pdf:
  post:
    summary: Create PDF from various sources
    requestBody:
      content:
        multipart/form-data:
          schema:
            type: object
            properties:
              file:
                type: string
                format: binary
              options:
                $ref: '#/components/schemas/PDFOptions'
  
  /{documentId}:
    get:
      summary: Get PDF metadata
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PDFMetadata'
    
    /content:
      get:
        summary: Extract content from PDF
        parameters:
          - name: format
            in: query
            schema:
              type: string
              enum: [text, html, structured]
      
    /pages:
      get:
        summary: Get specific pages
      
      post:
        summary: Manipulate pages (rotate, delete, insert)
      
    /export:
      post:
        summary: Export to different format
```

### 6.2 Message Queue Integration

```typescript
interface PDFProcessingQueue {
  // Queue processing jobs
  enqueue(job: ProcessingJob): Promise<string>;
  
  // Get job status
  getStatus(jobId: string): Promise<JobStatus>;
  
  // Cancel job
  cancel(jobId: string): Promise<void>;
}

interface ProcessingJob {
  type: 'convert' | 'extract' | 'merge' | 'sign' | 'watermark';
  source: JobSource;
  options: ProcessingOptions;
  priority: 'low' | 'normal' | 'high';
  callback?: string; // Webhook URL
}
```

## 7. Scalability Design

### 7.1 Horizontal Scaling Architecture

```
┌─────────────┐
│   Load      │
│   Balancer  │
└──────┬──────┘
       │
   ┌───┴───┬───────────┬───────────┐
   │       │           │           │
   ▼       ▼           ▼           ▼
┌─────┐ ┌─────┐     ┌─────┐     ┌─────┐
│Node1│ │Node2│ ... │Node3│     │NodeN│
└──┬──┘ └──┬──┘     └──┬──┘     └──┬──┘
   │       │           │           │
   └───────┴─────┬─────┴───────────┘
                 │
          ┌──────▼──────┐
          │  Distributed│
          │  File Store │
          └─────────────┘
```

### 7.2 Auto-Scaling Configuration

```yaml
# Kubernetes HPA configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: pdf-processor
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: External
      external:
        metric:
          name: pdf_queue_depth
        target:
          type: AverageValue
          averageValue: "10"
```

## Related Documents

- [PDF Glossary](../glossary.md)
- [PDF Best Practices](../best-practice.md)
- [PDF Anti-Patterns](../anti-pattern.md)
- [PDF Checklist](../checklist.md)
- [PDF FAQ](../faq.md)
- [PDF Decision Tree](../decision-tree.md)
