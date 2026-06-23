---
title: "PDF Glossary - Từ Điển Thuật Ngữ PDF"
description: "Comprehensive glossary of PDF terminology covering PDF/A, PDF/UA, CIDFont, CMYK, linearized PDF, object streams, and other essential PDF concepts"
tags: ["pdf", "glossary", "terminology", "pdf-a", "pdf-ua", "cursor-enterprise-framework"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# PDF Glossary - Từ Điển Thuật Ngữ PDF

## Overview

Tài liệu này cung cấp một comprehensive glossary của các thuật ngữ liên quan đến PDF processing và generation. Việc hiểu rõ các thuật ngữ này là essential cho bất kỳ ai làm việc với PDF systems, từ developers đến architects và QA engineers. Mỗi entry bao gồm định nghĩa, context về cách nó được sử dụng, và thường có examples để clarify.

PDF (Portable Document Format) là một file format phức tạp với hàng chục năm lịch sử phát triển. Understanding its terminology giúp developers make better decisions về cách generate, manipulate, và optimize PDF files. Đặc biệt trong enterprise context, nơi compliance và accessibility là important, knowing correct terminology giúp communicate effectively với stakeholders và vendors.

## Purpose

Glossary này phục vụ như một quick reference cho developers và architects khi họ encounter unfamiliar PDF terminology. Nó cũng hữu ích cho việc đào tạo new team members và làm reference document trong technical discussions. Mỗi term được định nghĩa rõ ràng với practical context, giúp readers apply knowledge ngay vào work của họ.

## Key Terms

### A

#### Accessibility (PDF Accessibility)

**Định nghĩa**: Khả năng của PDF document được accessible bởi người dùng với disabilities, bao gồm người mù, khiếm thị, hoặc có difficulties với motor control.

**Context**: PDF accessibility bao gồm support cho screen readers, keyboard navigation, và proper document structure. Điều này được regulated bởi various laws như Section 508 trong US và EN 301 549 ở EU.

** Ví dụ**:

```javascript
// Creating accessible PDF structure
const pdfDoc = await PDFDocument.create();
pdfDoc.setTitle('Accessible Document');
pdfDoc.setLang('en-US');

// Enable tagged PDF
pdfDoc.catalog.set(
  PDFName.of('MarkInfo'),
  pdfDoc.context.obj({ Marked: true })
);
```

#### AcroForm

**Định nghĩa**: Adobe's form technology cho PDF, cho phép interactive forms với fields như text inputs, checkboxes, radio buttons, và dropdowns.

**Context**: AcroForms là legacy form system của Adobe. Mặc dù vẫn widely supported, Adobe đã giới thiệu XFA forms như successor. Many modern PDF libraries hỗ trợ cả hai.

** Ví dụ**: Khi bạn tạo một PDF form trong Adobe Acrobat, các fields được tạo là AcroForm fields. Các libraries như pdf-lib và iText có thể programmatically fill và create these fields.

#### Appearance Stream

**Định nghĩa**: Một XObject chứa drawing instructions để render một annotation hoặc form field's visual representation.

**Context**: Mỗi form field có một appearance stream xác định nó trông như thế nào trên page. Điều này tách biệt visual representation khỏi field's data, cho phép field look different depending on state (normal, rollover, pressed).

### B

#### Byte Range

**Định nghĩa**: Một cặp numbers xác định vị trí và độ dài của một phần data trong PDF file, được sử dụng chủ yếu cho digital signatures.

**Context**: Trong digital signatures, byte ranges chỉ định phần nào của PDF được signed. Phần contents của signature được represented bằng một placeholder string để signature có thể được added sau mà không làm invalid signature.

** Ví dụ**:

```
/ByteRange [0 12345 16385 67890]
```

Điều này có nghĩa là byte 0-12344 và byte 16385-67889 được hash để tạo signature, với placeholder ở byte 12345-16384.

#### Bleed

**Định nghĩa**: Vùng extends beyond trim size của document, thường là 3-5mm, được thiết kế để accommodate cutting variations trong print production.

**Context**: Trong professional printing, bleed đảm bảo rằng khi document được cắt, không có white edges xuất hiện do minor cutting inaccuracies. Các design tools như Adobe InDesign hỗ trợ bleed settings.

### C

#### CMYK

**Định nghĩa**: Color model sử dụng Cyan, Magenta, Yellow, và Key (Black) inks để reproduce colors, phổ biến trong in ấn.

**Context**: Trong khi screens sử dụng RGB (Red, Green, Blue), printers sử dụng CMYK. PDF files cho print production nên được specified trong CMYK. RGB colors được automatically converted khi printed, nhưng results có thể không như expected.

** Ví dụ**:

```javascript
// CMYK color in PDF
const cyan = 0;
const magenta = 1;
const yellow = 1;
const key = 0;

page.drawText('Cyan Text', {
  color: rgb(cyan, magenta, yellow, key) // Custom CMYK color
});
```

#### CIDFont (Character Identifier Font)

**Định nghĩa**: Font type được thiết kế để support large character sets như those found in Asian languages, sử dụng character identifiers thay vì direct character codes.

**Context**: CIDFonts được sử dụng cho CJK (Chinese, Japanese, Korean) languages và other writing systems với large character inventories. Chúng bao gồm CJK fonts như "STSong-Light" cho Chinese text.

** Ví dụ**: Khi embedding Vietnamese text với many diacritics, CIDFont systems như Adobe CIDKey fonts có thể được sử dụng, hoặc modern Unicode fonts với glyph substitution.

#### Content Stream

**Định nghĩa**: Phần của PDF page object chứa drawing operators và operands xác định những gì được rendered trên page đó.

**Context**: Content streams sử dụng một mini-language của operators (như "cm" cho concatenation matrix, "Tm" cho text matrix) để describe graphics và text. Understanding content streams là essential cho low-level PDF manipulation.

** Ví dụ**:

```
q
0 0 1 rg
0 0 100 100 re
f
Q
```

Đoạn này save graphics state (q), set fill color thành blue (0 0 1 rg), draw rectangle (0 0 100 100 re), fill it (f), và restore graphics state (Q).

#### Cross-Reference Table (Xref)

**Định nghĩa**: Bảng trong PDF file chứa vị trí của tất cả indirect objects, cho phép random access vào PDF structure.

**Context**: Xref table là một trong những đổi mới quan trọng của PDF, cho phép applications access any part của file mà không cần đọc entire file. Các versions mới hơn của PDF sử dụng Xref streams để compress this information.

### D

#### Digital Signature

**Định nghĩa**: Cryptographic mechanism cho authentication, integrity verification, và non-repudiation của PDF documents.

**Context**: Digital signatures trong PDF sử dụng PKI (Public Key Infrastructure) với certificates. Chúng provides stronger assurance của document authenticity hơn handwritten signatures trong many legal contexts.

** Ví dụ**:

```javascript
// Conceptual signature structure
const signature = {
  Type: 'Sig',
  Filter: 'Adobe.PPKLite',
  SubFilter: 'adbe.pkcs7.detached',
  ByteRange: [0, placeholder_position, placeholder_end, file_length],
  Contents: base64_encoded_signature,
  Reason: 'Document Signed',
  Location: 'Server',
  M: '2026-06-23T12:00:00Z'
};
```

#### DPI (Dots Per Inch)

**Định nghĩa**: Measure của image resolution và print quality, indicating how many dots of ink per inch a printer can produce.

**Context**: Screen displays thường ở 96 DPI, trong khi professional printing yêu cầu 300 DPI hoặc cao hơn. Low DPI images sẽ appear pixelated khi printed.

### E

#### Encrypted PDF

**Định nghĩa**: PDF file được protected bằng encryption, yêu cầu password hoặc certificate để open hoặc modify.

**Context**: PDF encryption có thể be user-level (password-protected) hoặc permission-level (限制了 certain operations như printing hoặc copying). Encryption sử dụng algorithms như RC4 hoặc AES.

** Ví dụ**:

```javascript
const pdfDoc = await PDFDocument.load(encryptedBuffer, {
  password: 'user-password'
});

// Set permissions
pdfDoc.setEncryption({
  userPassword: 'user-password',
  ownerPassword: 'owner-password',
  permissions: {
    printing: 'highResolution',
    modifying: false,
    copying: false,
    annotating: false
  }
});
```

#### Extractable Text

**Định nghĩa**: Text trong PDF mà có thể được selected và copied bởi users và indexed bởi search engines.

**Context**: Nếu text được rendered as outlines (shapes) thay vì actual text objects, nó sẽ không be extractable. Điều này thường xảy ra khi converting from scanned images (OCR required) hoặc when fonts được embedded incorrectly.

### F

#### File ID

**Định nghĩa**: Two-part identifier trong PDF trailer: một deterministic identifier based on file content và một random identifier tạo mỗi khi file được opened/saved.

**Context**: File IDs được sử dụng trong digital signatures và encryption schemes. The deterministic ID helps detect file changes, trong khi the random ID provides uniqueness.

#### Font Descriptor

**Định nghĩa**: Object chứa metrical information về một font, bao gồm bounding boxes, stem widths, và other characteristics.

**Context**: Font descriptors are essential cho font substitution khi một font không available. Chúng describe font's appearance characteristics mà allows rendering engine approximate appearance.

#### Font Subsetting

**Định nghĩa**: Kỹ thuật chỉ embed những glyphs thực sự được sử dụng trong document thay vì entire font file.

**Context**: Một full Unicode font có thể là 5-10MB. Subsetting chỉ embed characters used (ví dụ: chỉ "Hello" từ một font) giảm size dramatically. Subset fonts still render correctly nhưng không thể be used để render other characters.

** Ví dụ**:

```javascript
// Font subsetting concept
const usedChars = new Set('Hello World 123'.split(''));
const subset = font.subset(usedChars);
// subset chỉ chứa glyphs cho H, e, l, o, space, W, r, d, 1, 2, 3
```

### G

#### Gamut

**Định nghĩa**: Range of colors có thể be reproduced bởi một color device hoặc viewing condition.

**Context**: RGB và CMYK có different gamuts. Colors nằm ngoài device's gamut phải be approximated, có thể dẫn đến color shifts. Soft-proofing helps preview these conversions.

### H

#### Halftone

**Định nghĩa**: Kỹ thuật sử dụng patterns của dots để simulate continuous tones trong print.

**Context**: Printers chỉ có thể print solid dots, không phải continuous gradients. Halftones use varying dot sizes và spacing để create illusion của continuous tone. PDF hỗ trợ various halftone spot functions.

### I

#### ISO 19005 (PDF/A)

**Định nghĩa**: International standard cho long-term preservation của electronic documents, ensuring documents remain readable over decades.

**Context**: PDF/A prohibits features có thể become unreadable over time như external font references, multimedia, và executable content. Nó yêu cầu fonts be embedded và metadata be standardized.

**PDF/A Levels**:

- **PDF/A-1a**: Level A conformance, full accessibility support
- **PDF/A-1b**: Level B conformance, basic reliability
- **PDF/A-2a, PDF/A-2u, PDF/A-2b**: Based on PDF 1.7
- **PDF/A-3a, PDF/A-3u, PDF/A-3b**: Allows embedded files

#### ISO 14289 (PDF/UA)

**Định nghĩa**: International standard cho universal accessibility in PDF documents.

**Context**: PDF/UA requires proper document structure (tags), alternative text cho images, và logical reading order. Nó là necessary cho compliance với accessibility laws ở many jurisdictions.

### J

#### JavaScript Actions

**Định nghĩa**: JavaScript code embedded trong PDF để add interactivity, như form validation hoặc document actions.

**Context**: PDF JavaScript là subset của ECMAScript, cho phép features như calculating form field totals, validating input, và responding to document events. Tuy nhiên, many production environments disable JavaScript for security.

### L

#### Linearized PDF

**Định nghĩa**: PDF file được optimized cho fast web viewing, với file structure rearranged để allow first page display before entire download completes.

**Context**: Linearized PDFs (còn gọi là "web-optimized") được designed cho HTTP byte-serving, cho phép progressive rendering as bytes arrive. They are essential for good performance khi viewing PDFs over the web.

** Ví dụ**: Khi bạn open một PDF từ một URL, linearized PDF hiển thị first page almost immediately, trong khi non-linearized PDF phải download hoàn toàn trước khi hiển thị anything.

#### LZW (Lempel-Ziv-Welch)

**Định nghĩa**: Compression algorithm được sử dụng trong PDF cho inline images và compressed object streams.

**Context**: LZW là một trong những earliest compression algorithms trong PDF. Nó đã được deprecated trong some contexts due to patent issues, với DEFLATE (zip) compression now preferred.

### M

#### MDPE (Modular Document Production Engine)

**Định nghĩa**: Adobe's architecture cho modular PDF processing, cho phép components như content assembly, digital signatures, và accessibility được combined.

**Context**: MDPE represents Adobe's approach to extensible PDF processing, where different modules can be plugged in depending on requirements.

#### Media Box

**Định nghĩa**: Bounding box xác định vùng của physical page trong PDF, including any production marks như bleed hoặc crop marks.

**Context**: Media box là default page boundary. Các boxes khác như Crop Box và Trim Box define different visible areas của page. Media box is always the largest.

#### Metadata

**Định nghĩa**: Descriptive information về PDF document, bao gồm title, author, subject, keywords, creation date, và modification date.

**Context**: Document metadata là essential cho document management systems, search indexing, và accessibility. PDF/A standards require specific metadata schemas.

** Ví dụ**:

```javascript
const pdfDoc = await PDFDocument.create();
pdfDoc.setTitle('Invoice #12345');
pdfDoc.setAuthor('Acme Corporation');
pdfDoc.setSubject('Monthly Invoice');
pdfDoc.setKeywords(['invoice', 'billing', '2026']);
pdfDoc.setProducer('PDF Generator v1.0');
pdfDoc.setCreator('Acme Billing System');
pdfDoc.setCreationDate(new Date());
pdfDoc.setModificationDate(new Date());
```

### N

#### Named Destinations

**Định nghĩa**: Predefined locations in a PDF document được referenced by name rather than by page number, making links stable even when pages are rearranged.

**Context**: Named destinations allow external links to remain valid even when document pages are reordered. They are essential for document management systems where pages might be inserted or removed.

### O

#### Object Streams

**Định nghĩa**: Compression technique xếp nhiều PDF objects vào một stream, reducing file size và improving parsing efficiency.

**Context**: Object streams are part of linearized PDF optimization và are required in PDF/A-2 and later. They store multiple indirect objects as a single compressed stream.

#### Optional Content Groups (OCG)

**Định nghĩa**: Feature cho conditional visibility của content, thường được sử dụng để create layers trong CAD drawings hoặc to hide sensitive information.

**Context**: OCGs allow documents to contain multiple layers of content that can be shown or hidden based on user preference or printing requirements. This is similar to layers in design software.

### P

#### PDF/A (Archival)

**Định nghĩa**: ISO 19005 standard for long-term document preservation, ensuring documents remain readable and reproducible over extended periods.

**Context**: PDF/A prohibits features có thể become obsolete, như:
- External font references (fonts must be embedded)
- Audio and video content
- Executable content (JavaScript must be restricted)
- Encryption (unless key stored with document)
- Transparency (in PDF/A-1)

#### PDF/UA (Universal Accessibility)

**Định nghĩa**: ISO 14289 standard ensuring PDF documents are accessible to users with disabilities, particularly those using assistive technologies.

**Context**: PDF/UA requirements include:
- Document must be tagged with proper structure
- All images must have alternate text
- Reading order must be logical
- Document must have a document title
- Language must be specified

#### PDF/X (Exchange)

**Định nghĩa**: Family of ISO standards cho print production, ensuring reliable color reproduction và eliminating variables that affect print quality.

**Context**: PDF/X standards specify:
- PDF/X-1a: No transparency, CMYK or spot colors only
- PDF/X-3: Allows ICC color management
- PDF/X-4: Allows live transparency và PDF 1.6 features
- PDF/X-5: Allows external content references

#### Page Tree

**Định nghĩa**: Hierarchical structure trong PDF xác định thứ tự và hierarchy của pages trong document.

**Context**: Page tree là a tree structure với intermediate nodes (page tree nodes) và leaf nodes (page objects). Nó allows efficient navigation và manipulation của large documents.

#### Preflight

**Định nghĩa**: Process của analyzing PDF file để verify nó meets specific requirements, như PDF/A compliance hoặc print production standards.

**Context**: Preflight checks verify fonts are embedded, colors are in correct space, required metadata is present, và no prohibited features are used. Adobe Acrobat includes preflight tool.

#### Print Production Marks

**Định nghĩa**: Technical marks added to pages for print production, including crop marks, bleed marks, registration marks, và color bars.

**Context**: Print production marks help printer align paper, verify color, và ensure correct trimming. They are outside the trim area và are removed during final binding.

### R

#### Reflow

**Định nghĩa**: Process của reformatting PDF content để fit different screen sizes hoặc reading preferences.

**Context**: Tagged PDFs có thể be reflowed bởi screen readers và mobile apps để provide better reading experience. Non-tagged PDFs cannot be reflowed reliably.

#### Resources Dictionary

**Định nghĩa**: Object in a PDF page hoặc form xác định fonts, images, patterns, và other resources cần thiết để render the content.

**Context**: Each page references a resources dictionary to find the actual font và image objects used in its content stream. This separation allows resources to be shared across multiple pages.

### S

#### Stream

**Định nghĩa**: Object type trong PDF chứa sequence of bytes, possibly compressed, representing content hoặc data.

**Context**: Streams are fundamental to PDF, used for page content, images, embedded fonts, và metadata. They can be filtered (compressed) using various algorithms.

** Ví dụ**:

```javascript
// Stream object structure
const streamObj = {
  Length: 1234,
  Filter: 'FlateDecode',
  // Stream data follows
};
```

#### Structure Tree

**Định nghĩa**: Hierarchical tree of tagged PDF defining document's logical structure, essential for accessibility và content extraction.

**Context**: Structure tree maps visual content to semantic meaning. For example, a heading's visual appearance maps to a "H1" structure element. Screen readers use this tree to navigate and read content.

### T

#### Tagged PDF

**Định nghĩa**: PDF with additional markup indicating document's logical structure, required for accessibility compliance và reliable text extraction.

**Context**: Tagged PDF includes:
- Document structure tree
- Standardized structure types (paragraphs, headings, tables)
- Artifacts for decorative content
- Reading order information

#### Trailer

**Định nghĩa**: Final section của PDF file chứa location của cross-reference table và other essential information.

**Context**: Trailer specifies where to find the xref table, document's catalog, and optional encrypt/signature information. It allows applications to quickly locate key parts of the document.

### U

#### Unicode

**Định nghĩa**: Universal character encoding standard supporting characters from all writing systems, essential for multilingual documents.

**Context**: Modern PDFs use Unicode (UTF-16 or UTF-8) for text encoding, replacing older single-byte encodings. This allows proper rendering of any language, from English to emoji to CJK characters.

#### Unembedable Fonts

**Định nghĩa**: Fonts with license restrictions prohibiting embedding in PDF documents.

**Context**: Some fonts are licensed for use on specific devices or cannot be distributed in documents. PDF readers must substitute these with similar available fonts, potentially affecting document appearance.

### V

#### Vector Graphics

**Định nghĩa**: Graphics defined using mathematical equations for lines and curves, as opposed to raster graphics which use pixel grids.

**Context**: PDF excels at vector graphics, maintaining crisp rendering at any zoom level. Logos, charts, và diagrams are typically vector. Only photographs và complex gradients use raster images.

### W

#### Watermark

**Định nghĩa**: Semi-transparent text hoặc image overlaid on page content, often used for branding hoặc security (like "CONFIDENTIAL").

**Context**: Watermarks can be:
- Text-based ("DRAFT", "CONFIDENTIAL")
- Image-based (company logo)
- Applied to all pages or specific pages
- In foreground or background

** Ví dụ**:

```javascript
const pdfDoc = await PDFDocument.load(buffer);
const helvetica = await pdfDoc.embedFont(StandardFonts.Helvetica);

const pages = pdfDoc.getPages();
for (const page of pages) {
  const { width, height } = page.getSize();
  
  page.drawText('CONFIDENTIAL', {
    x: width / 4,
    y: height / 2,
    size: 60,
    font: helvetica,
    color: rgb(0.8, 0.8, 0.8),
    opacity: 0.3,
    rotate: degrees(45)
  });
}
```

### X

#### XObject

**Định nghĩa**: PDF object type representing reusable content, including images, forms, và PostScript calculations.

**Context**: XObjects are referenced from content streams and allow content to be defined once but used multiple times. Types include:
- Image XObject: raster images
- Form XObject: reusable graphic content
- PostScript XObject: deprecated, for PS calculations

#### Xref (Cross-Reference)

**Định nghĩa**: Table trong PDF file listing location và details của each object, enabling random access.

**Context**: Xref table entries specify:
- Object number
- Byte offset in file
- Generation number
- Whether object is in use or free

Modern PDF versions use Xref streams for better compression.

### Y

#### Y Coordinate System

**Định nghĩa**: PDF's coordinate system với origin at bottom-left corner, positive Y going upward.

**Context**: Unlike many graphics systems where Y increases downward (like HTML), PDF places origin at bottom-left. This affects calculations when converting from other formats.

```
┌─────────────────┐ 0, 841 (top)
│                 │
│    PDF Page     │
│                 │
└─────────────────┘ 0, 0 (origin)
```

## Common Acronyms

| Acronym | Full Form | Description |
|---------|-----------|-------------|
| PDF | Portable Document Format | Adobe's document format |
| PDF/A | PDF Archival | ISO 19005 for long-term preservation |
| PDF/UA | PDF Universal Accessibility | ISO 14289 for accessibility |
| PDF/X | PDF Exchange | ISO 15930 for print production |
| CMYK | Cyan, Magenta, Yellow, Key | Print color model |
| RGB | Red, Green, Blue | Screen color model |
| DPI | Dots Per Inch | Print resolution measure |
| PPI | Pixels Per Inch | Screen resolution measure |
| OCR | Optical Character Recognition | Text extraction from images |
| XObject | External Object | Reusable PDF content blocks |
| OCG | Optional Content Group | Layer/visibility control |
| CID | Character Identifier | Font character encoding |
| LZW | Lempel-Ziv-Welch | Compression algorithm |
| DES | Data Encryption Standard | Encryption algorithm (deprecated) |
| AES | Advanced Encryption Standard | Modern encryption |
| PKI | Public Key Infrastructure | Digital certificate system |
| XMP | Extensible Metadata Platform | Standardized metadata |
| ICC | International Color Consortium | Color management standard |

## Industry Standards

### ISO Standards Related to PDF

| Standard | Title | Purpose |
|----------|-------|---------|
| ISO 32000-1 | PDF 1.7 | Core PDF specification |
| ISO 32000-2 | PDF 2.0 | Updated PDF specification |
| ISO 19005-1 | PDF/A-1 | Archival, Level A and B |
| ISO 19005-2 | PDF/A-2 | PDF/A-1 + transparency, JPEG2000 |
| ISO 19005-3 | PDF/A-3 | PDF/A-3 + embedded files |
| ISO 14289-1 | PDF/UA-1 | Universal accessibility |
| ISO 15930-1 | PDF/X-1a | Print exchange, CMYK only |
| ISO 15930-3 | PDF/X-3 | Print exchange, ICC support |
| ISO 16612-2 | PDF/VT | Variable and transactional printing |

## References

- Adobe PDF Reference (ISO 32000): https://www.adobe.com/devnet/pdf.html
- PDF/A Standard: https://www.iso.org/standard/38920.html
- PDF/UA Standard: https://www.pdfa.org/ua-standard/
- PDF/X Standard: https://www.pdfx.org/
- PDF Library Comparison: https://pdf-lib.org/
- Mozilla PDF.js: https://github.com/mozilla/pdf.js
