# PDF Knowledge Base - Decision Tree

## Tổng quan

Document này cung cấp cây quyết định chi tiết để hướng dẫn việc lựa chọn phương pháp xử lý PDF phù hợp trong Cursor Enterprise Framework.

## 1. PDF Operation Selection Tree

```
Bạn muốn thực hiện operation gì trên PDF?
│
├── [TẠO MỚI] Tạo PDF từ đầu
│   │
│   ├── Mục đích gì?
│   │   ├── Lưu trữ dài hạn (Archive)
│   │   │   └── → Đi đến: PDF/A Decision Tree
│   │   │
│   │   ├── In ấn (Print)
│   │   │   └── → Đi đến: Print-Ready PDF Decision
│   │   │
│   │   ├── Web viewing
│   │   │   └── → Đi đến: Web Optimization Decision
│   │   │
│   │   └── General use
│   │       └── → Standard PDF với embedded fonts
│   │
│   └── Cần hỗ trợ tiếng Việt không?
│       ├── Có → Sử dụng Unicode fonts (Noto, Arial Unicode)
│       └── Không → System fonts được phép
│
├── [ĐỌC] Đọc/Trích xuất nội dung
│   │
│   ├── Extract text?
│   │   ├── Chỉ text thuần túy → Plain text extraction
│   │   ├── Giữ layout → Layout-preserving extraction
│   │   └── Structured data (table, form) → Structured extraction
│   │
│   ├── Extract images?
│   │   └── → Image extraction với metadata
│   │
│   └── Get metadata?
│       └── → Metadata extraction
│
├── [CHỈNH SỬA] Chỉnh sửa PDF hiện có
│   │
│   ├── Merge multiple PDFs?
│   │   └── → Đi đến: Merge Decision Tree
│   │
│   ├── Split PDF?
│   │   └── → Đi đến: Split Decision Tree
│   │
│   ├── Rotate pages?
│   │   └── → Simple rotation (90°, 180°, 270°)
│   │
│   ├── Add content?
│   │   ├── Watermark → Đi đến: Watermark Decision
│   │   ├── Header/Footer → Page numbering operations
│   │   └── Annotation → Annotation types
│   │
│   └── Remove content?
│       ├── Remove pages → Page deletion
│       └── Remove sensitive info → Redaction
│
├── [BẢO MẬT] Bảo mật PDF
│   │
│   ├── Encrypt/Password protect?
│   │   └── → Đi đến: Encryption Decision
│   │
│   ├── Digital signature?
│   │   └── → Đi đến: Signing Decision
│   │
│   └── Redact sensitive info?
│       └── → Secure redaction process
│
└── [CHUYỂN ĐỔI] Chuyển đổi định dạng
    │
    ├── PDF → Image?
    │   └── → Đi đến: Render Decision
    │
    ├── Image → PDF?
    │   └── → Image to PDF conversion
    │
    ├── PDF → Text/HTML?
    │   └── → Export extraction
    │
    └── PDF/A conversion?
        └── → Đi đến: PDF/A Decision Tree
```

## 2. PDF/A Decision Tree

```
Bạn cần tạo PDF/A cho mục đích gì?
│
├── Lưu trữ dài hạn (không cần accessibility)?
│   │
│   ├── File có chứa color-critical content?
│   │   ├── Có → PDF/A-3b (hỗ trợ CMYK, attachments)
│   │   └── Không → PDF/A-1b (đơn giản nhất, tương thích rộng)
│   │
│   └── Kích thước file quan trọng?
│       ├── Quan trọng → PDF/A-2b (nén tốt hơn)
│       └── Không quan trọng → PDF/A-1b
│
├── Cần accessibility (screen reader)?
│   │
│   └── PDF/A-1a hoặc PDF/A-2a (Level A)
│       │
│       ├── Chỉ cần basic accessibility?
│       │   └── PDF/A-1a (legacy support tốt)
│       │
│       └── Cần vector graphics support?
│           └── PDF/A-2a (hỗ trợ transparency)
│
└── Cần attach files?
    │
    ├── Có → PDF/A-3b (cho phép attachments)
    │   │
    │   └── Attachment là gì?
    │       ├── XML/CSV data → Có thể embed và link
    │       ├── Source code → PDF/A-3b hỗ trợ
    │       └── Other PDFs → Có thể embed (PDF/A-3)
    │
    └── Không → PDF/A-1b hoặc PDF/A-2b

QUYẾT ĐỊNH CUỐI CÙNG:
┌─────────────────────────────────────────────────────────────┐
│ Accessibility? │ CMYK?     │ Attach? │ → Chọn PDF/A         │
├───────────────┼───────────┼─────────┼───────────────────────┤
│ Không         │ Không     │ Không   │ → PDF/A-1b            │
│ Không         │ Không     │ Có      │ → PDF/A-3b            │
│ Không         │ Có        │ Không   │ → PDF/A-3b            │
│ Có            │ Không     │ Không   │ → PDF/A-1a            │
│ Có            │ Không     │ Có      │ → PDF/A-3a            │
│ Có            │ Có        │ Không   │ → PDF/A-2a            │
│ Có            │ Có        │ Có      │ → PDF/A-3a            │
└───────────────┴───────────┴─────────┴───────────────────────┘
```

## 3. Encryption Decision Tree

```
Bạn cần mức bảo mật nào?
│
├── Basic password protection?
│   │
│   ├── Chỉ ngăn unauthorized viewing?
│   │   └── User password only (owner password = none)
│   │
│   └── Ngăn cả editing/modification?
│       └── Both user và owner password
│
├── Standard encryption (legacy compatibility)?
│   │
│   ├── RC4-40 (legacy, không khuyến khích)
│   │   └── Chỉ khi cần tương thích với old readers
│   │
│   └── RC4-128 (standard, deprecated)
│       └──过渡方案 cho legacy systems
│
└── Modern encryption (khuyến khích)?
    │
    ├── AES-128
    │   └── Balance giữa security và performance
    │
    └── AES-256
        └── Maximum security, recommended

PERMISSIONS DECISION:
┌─────────────────────────────────────────────────────────────┐
│ Use Case                    │ Permissions                   │
├─────────────────────────────┼───────────────────────────────┤
│ Internal document           │ Print, Modify, Copy: Yes       │
│ External sharing            │ Print: Yes, Modify: No        │
│ Sensitive data              │ Print: No, Copy: No            │
│ Print-only review           │ Print: Yes, Modify: No, Copy: No│
│ Fully locked                │ All: No                        │
└─────────────────────────────┴───────────────────────────────┘
```

## 4. Merge Decision Tree

```
Bạn cần merge như thế nào?
│
├── Số lượng files?
│   ├── 2 files → Direct merge
│   └── Multiple files → Batch merge
│
├── Cần giữ nguyên file gốc?
│   ├── Có → Copy pages sang new document
│   └── Không → Có thể modify trực tiếp
│
├── Cần tạo bookmarks/outline?
│   │
│   ├── Có → Create outline từ filenames
│   │   │
│   │   ├── Custom bookmark names?
│   │   │   ├── Có → Read from metadata/config
│   │   │   └── Không → Use filenames
│   │   │
│   │   └── Nested bookmarks?
│   │       ├── Có → Hierarchical structure
│   │       └── Không → Flat structure
│   │
│   └── Không → Simple merge without outline
│
├── Cần merge specific pages?
│   │
│   ├── Specify page ranges → Custom page selection
│   │   │
│   │   └── Format nào?
│   │       ├── "1-5, 10, 15-20" → Range syntax
│   │       └── Odd/Even pages → Special keywords
│   │
│   └── Merge all pages → Full merge
│
└── Files có encryption khác nhau?
    │
    ├── Cùng password → Merge được
    └── Khác password → Không merge được (phải unlock trước)
```

## 5. Text Extraction Decision Tree

```
Bạn cần extract text với mức độ chi tiết nào?
│
├── Plain text only?
│   │
│   ├── Không cần preserve formatting → Simple extraction
│   │   └── Fast, low memory
│   │
│   └── Cần basic structure (paragraphs)?
│       └── Paragraph-aware extraction
│
├── Preserve layout?
│   │
│   ├── Web/HTML output?
│   │   └── → HTML extraction với CSS positioning
│   │
│   ├── Document rebuild?
│   │   └── → DOCX/Word với styles
│   │
│   └── Screen reader compatibility?
│       └── → Tagged extraction với reading order
│
└── Structured extraction?
    │
    ├── Tables?
    │   ├── Detect tables → Table extraction
    │   │   │
    │   │   ├── Preserve formatting? → Vector table export
    │   │   └── Data analysis? → CSV/Excel export
    │   │
    │   └── Keep as image? → Image-based table
    │
    ├── Forms?
    │   └── → Form field extraction
    │
    └── Key-value pairs?
        └── → Intelligent document extraction

EXTRACTION MODE SELECTION:
┌─────────────────────────────────────────────────────────────┐
│ Speed Priority  │ Layout Priority │ → Use                    │
├────────────────┼─────────────────┼──────────────────────────┤
│ High           │ Low             │ → Plain text mode         │
│ Medium         │ Medium          │ → Layout-preserving       │
│ Low            │ High            │ → Structured extraction   │
│ Any            │ Any            │ → Background processing   │
└────────────────┴─────────────────┴──────────────────────────┘
```

## 6. Image Render Decision Tree

```
Bạn cần render PDF sang image như thế nào?
│
├── Output format nào?
│   │
│   ├── PNG → Lossless, transparency support
│   │   └── Use cho: icons, graphics, screenshots
│   │
│   ├── JPEG → Smaller size, lossy
│   │   └── Use cho: photos, previews, web
│   │
│   ├── TIFF → High quality, multi-page
│   │   └── Use cho: print, archival
│   │
│   └── WebP → Modern, good compression
│       └── Use cho: web performance
│
├── Resolution/DPI?
│   │
│   ├── Screen (72 DPI)
│   │   └── Fast preview, small files
│   │
│   ├── Print (300 DPI)
│   │   └── High quality printing
│   │
│   └── Custom DPI
│       └── → Calculate based on output needs
│
├── Color mode?
│   │
│   ├── RGB → Screen display
│   ├── Grayscale → Black & white documents
│   └── CMYK → Professional printing (limited support)
│
└── Quality settings?
    │
    ├── JPEG quality (0-100)
    │   ├── Web optimization → 70-80
    │   ├── Balanced → 80-90
    │   └── High quality → 90-100
    │
    └── PNG compression
        └── Lossless, compression level 1-9
```

## 7. Signing Decision Tree

```
Bạn cần signing như thế nào?
│
├── Signature type?
│   │
│   ├── Digital signature (PKI-based)?
│   │   │
│   │   ├── Có certificate?
│   │   │   ├── Có (valid) → Use existing certificate
│   │   │   └── Có (expired) → Renew hoặc create new
│   │   │
│   │   └── Không có → Certificate generation
│   │       │
│   │       ├── Self-signed → Internal use
│   │       └── CA-issued → External/legal use
│   │
│   └── Timestamp?
│       ├── Cần long-term validity → TSA timestamp required
│       └── Short-term → Optional
│
├── Signature placement?
│   │
│   ├── Specific page/position → Manual placement
│   ├── Existing signature field → Fill existing
│   └── Multiple signatures? → Incremental save
│
└── Certificate management?
    │
    ├── Enterprise PKI → Integration với existing CA
    ├── Cloud signing → Cloud HSM/key management
    └── Local keys → File-based key storage
```

## 8. Large File Handling Decision Tree

```
Kích thước file PDF của bạn là bao nhiêu?
│
├── < 10MB → Standard processing
│   └── Load entire file, no special optimization
│
├── 10MB - 50MB → Moderate optimization
│   │
│   ├── Sequential page access
│   ├── Lazy loading for images
│   └── Memory monitoring
│
├── 50MB - 200MB → Heavy optimization
│   │
│   ├── Stream-based processing
│   ├── Page-by-page operations
│   ├── Temp file usage
│   └── Progress tracking
│
└── > 200MB → Enterprise processing
    │
    ├── Streaming pipeline only
    ├── Distributed processing
    │   │
    │   ├── Chunked extraction
    │   ├── Parallel page rendering
    │   └── Distributed merge
    │
    ├── External processing (worker queue)
    │
    └── Consider alternative formats?
        └── Nếu possible, consider TIFF/document management
```

## 9. Form Handling Decision Tree

```
Bạn cần làm gì với PDF form?
│
├── Extract form data?
│   │
│   ├── Read all fields → Form data extraction
│   ├── Export to CSV/Excel → Data export
│   └── Import to database → Database integration
│
├── Fill form?
│   │
│   ├── programmatic → Form fill API
│   │   │
│   │   ├── Data từ đâu?
│   │   │   ├── Database → Auto-fill from DB
│   │   │   ├── API → Fetch and fill
│   │   │   └── User input → Web form submission
│   │   │
│   │   └── Field mapping cần thiết?
│   │       ├── Có → Create field mapping
│   │       └── Không → Direct field names
│   │
│   └── User fillable → Keep form interactive
│
├── Flatten form?
│   │
│   ├── Convert to non-editable → Flatten all fields
│   └── Keep editable → Don't flatten
│
└── Create form?
    │
    ├── Design tools → Visual form builder
    ├── Programmatic → Form API
    │   │
    │   ├── Text fields
    │   ├── Checkboxes
    │   ├── Radio buttons
    │   ├── Dropdowns
    │   └── Signature fields
    │
    └── From existing PDF → Form field addition
```

## 10. Quick Reference Decision Matrix

```
┌────────────────────────────────────────────────────────────────────────┐
│                        QUICK DECISION GUIDE                            │
├──────────────────────┬─────────────────────────────────────────────────┤
│ NEED                 │ SOLUTION                                        │
├──────────────────────┼─────────────────────────────────────────────────┤
│ Archive long-term    │ PDF/A-1b hoặc PDF/A-2b                          │
│ Accessible PDF       │ PDF/A-1a hoặc PDF/A-2a                          │
│ Attach files         │ PDF/A-3b                                        │
├──────────────────────┼─────────────────────────────────────────────────┤
│ Password protect     │ PDF encryption (AES-256 recommended)            │
│ Digital signature    │ PKCS#7 signature + TSA timestamp                 │
│ Redact info          │ Secure redaction (remove, not blackout)         │
├──────────────────────┼─────────────────────────────────────────────────┤
│ Merge PDFs           │ Page copy với optional outline                   │
│ Split PDF            │ Page extraction by range/index                  │
│ Extract pages        │ Page copy với new document creation             │
├──────────────────────┼─────────────────────────────────────────────────┤
│ Text extraction      │ Layout-preserving extraction                     │
│ Table extraction     │ Structured extraction với table detection        │
│ Image extraction     │ Image export với metadata preservation            │
├──────────────────────┼─────────────────────────────────────────────────┤
│ Web viewing          │ Linearized PDF + JPEG compression               │
│ Print quality        │ 300 DPI + lossless compression                  │
│ Thumbnail preview    │ Low-res JPEG (100-200px)                        │
├──────────────────────┼─────────────────────────────────────────────────┤
│ Large files          │ Stream processing + page-by-page operations     │
│ Batch processing     │ Queue-based workers + parallel processing        │
│ Optimize size        │ Image compression + font subsetting + streams   │
└──────────────────────┴─────────────────────────────────────────────────┘
```

## Related Documents

- [PDF Glossary](../glossary.md)
- [PDF Architecture](../architecture.md)
- [PDF Best Practices](../best-practice.md)
- [PDF Anti-Patterns](../anti-pattern.md)
- [PDF Checklist](../checklist.md)
- [PDF FAQ](../faq.md)
