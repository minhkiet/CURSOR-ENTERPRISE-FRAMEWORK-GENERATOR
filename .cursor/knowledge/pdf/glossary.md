# PDF Knowledge Base - Glossary

## Tổng quan

Document này cung cấp danh sách các thuật ngữ chuyên ngành liên quan đến xử lý PDF trong Cursor Enterprise Framework. Các thuật ngữ được phân loại theo từng nhóm để dễ tra cứu.

## Nhóm 1: Core PDF Concepts

### 1. PDF (Portable Document Format)

Định dạng tài liệu di động do Adobe phát triển, cho phép hiển thị tài liệu độc lập với phần mềm, phần cứng và hệ điều hành. PDF sử dụng PostScript language để mô tả bố cục và đồ họa, đảm bảo tính nhất quán khi hiển thị trên mọi nền tảng.

```pdf
%PDF-1.7
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
```

PDF hỗ trợ nhiều tính năng như mã hóa, chữ ký số, form fields, annotations, và embedded fonts. Trong enterprise environment, PDF là format chuẩn cho việc lưu trữ và chia sẻ tài liệu quan trọng.

### 2. PDF/A (PDF for Archiving)

Phiên bản PDF được chuẩn hóa ISO 19005 cho mục đích lưu trữ dài hạn. PDF/A yêu cầu tất cả fonts phải được embedded, không được sử dụng external references, và metadata phải tuân thủ schema cụ thể.

```xml
<!-- PDF/A-3a compliance example -->
<xmpMM:ManifestDictionary>
  <pdfaPart>3</pdfaPart>
  <pdfaConformance>A</pdfaConformance>
</xmpMM:ManifestDictionary>
```

### 3. PDF/UA (PDF for Universal Accessibility)

Tiêu chuẩn PDF cho khả năng tiếp cận toàn cầu (ISO 14289), đảm bảo người khuyết tật có thể đọc tài liệu PDF bằng screen readers. Yêu cầu tagging structure, alt text cho images, và proper reading order.

### 4. Linearized PDF

PDF đã được tối ưu hóa để hiển thị nhanh trên web (web-optimized). File được sắp xếp sao cho trình duyệt có thể bắt đầu hiển thị trước khi download hoàn tất.

## Nhóm 2: PDF Structure

### 5. Object Reference

Tham chiếu đến các đối tượng PDF như pages, fonts, images. Sử dụng indirect objects với object number và generation number để xác định vị trí.

```pdf
3 0 obj  % Indirect object
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>
endobj
```

### 6. Cross-Reference Table (Xref)

Bảng chỉ mục chứa vị trí của tất cả indirect objects trong PDF, cho phép random access mà không cần đọc toàn bộ file.

```pdf
xref
0 5
0000000000 65535 f 
0000000015 00000 n 
0000000068 00000 n 
0000000125 00000 n 
0000000300 00000 n 
```

### 7. Trailer

Phần cuối file PDF chứa thông tin về vị trí của Xref table và Catalog object. Trailer cho phép PDF reader nhanh chóng xác định cấu trúc document.

```pdf
trailer
<< /Size 5 /Root 1 0 R /Info 4 0 R >>
startxref
385
%%EOF
```

### 8. Catalog Object

Root object của PDF structure, chứa references đến all major structures như Pages tree, Outlines, Named destinations.

```pdf
1 0 obj
<< /Type /Catalog /Pages 2 0 R /PageMode /UseOutlines >>
endobj
```

## Nhóm 3: Content Representation

### 9. Content Stream

Chuỗi các operators và operands mô tả nội dung của một page, bao gồm vẽ shapes, hiển thị text, và xử lý images.

```pdf
stream
BT
/F1 12 Tf
100 700 Td
(Hello World) Tj
ET
endstream
```

### 10. Text Object

Phần tử content stream chịu trách nhiệm hiển thị text, bao gồm font selection, positioning, và actual text content.

### 11. Graphics State

Tập hợp các tham số đồ họa hiện tại như fill color, stroke color, transformation matrix, clipping path. Graphics state được save/restore để quản lý nested transformations.

### 12. Clipping Path

Đường dẫn xác định vùng hiển thị của content. Bất kỳ content nào vẽ bên ngoài clipping path sẽ bị ẩn.

## Nhóm 4: Security & Protection

### 13. Encryption Filter

Cơ chế mã hóa PDF sử dụng various algorithms như RC4, AES-128, AES-256. Encryption filter áp dụng cho toàn bộ file hoặc chỉ một phần.

```pdf
/Encrypt /Standard
/U (encrypted_user_password)
/O (encrypted_owner_hash)
/P 3900  % Permissions flags
```

### 14. Digital Signature

Chữ ký số trong PDF sử dụng PKI (Public Key Infrastructure) để xác thực identity và đảm bảo document integrity. Hỗ trợ timestamp và CRL/OCSP validation.

### 15. Permission Flags

Bit flags xác định operations nào được phép thực hiện trên PDF: print, modify, copy, annotate, fill forms, extract text/graphics.

## Nhóm 5: Forms & Interactive Elements

### 16. AcroForm

Traditional PDF form technology sử dụng field dictionaries để define interactive form fields như text boxes, checkboxes, radio buttons, dropdown lists.

```pdf
/AcroForm << /Fields [
  << /T (username) /FT /Tx /Ff 0 >>
  << /T (password) /FT /Tx /Ff 1 >>
] >>
```

### 17. XFA (XML Forms Architecture)

Advanced form technology sử dụng XML để define form layout và logic. XFA forms có thể dynamically calculate values và connect đến data sources.

### 18. Form Field

Element của AcroForm cho phép user input. Mỗi field có type (Tx, Btn, Ch, etc.), value, và associated widget annotation.

## Nhóm 6: Compression & Optimization

### 19. FlateDecode

Compression filter sử dụng DEFLATE algorithm (zlib), được sử dụng mặc định cho compressed streams trong PDF. Cung cấp tỷ lệ nén tốt cho text và images.

### 20. DCTDecode (JPEG Compression)

Filter cho phép embed JPEG-compressed images trực tiếp vào PDF stream mà không cần decompression.

### 21. JBIG2Decode

Compression algorithm đặc biệt hiệu quả cho black-and-white (1-bit) images, có thể đạt compression ratios cao hơn nhiều so với CCITT fax standards.

## Nhóm 7: Metadata & Standards

### 22. XMP Metadata

Extensible Metadata Platform - XML-based metadata standard được embed vào PDF để lưu trữ custom metadata như author, creation date, custom properties.

```xml
<x:xmpmeta xmlns:x="adobe:ns:meta/">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about="">
      <dc:creator>Enterprise Framework</dc:creator>
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
```

### 23. PDF/VT

Variant của PDF được thiết kế cho transactional printing applications, hỗ trợ variable data printing (VDP) với improved performance và resource management.

### 24. Tagged PDF

PDF với logical structure tree cho phép screen readers và other accessibility tools hiểu document structure. Required cho PDF/UA compliance.

## Nhóm 8: Tools & Libraries

### 25. PDF Library

Thư viện phần mềm cung cấp API để đọc, tạo, chỉnh sửa PDF files. Các thư viện phổ biến bao gồm iText, PDFBox, MuPDF, QPDF.

### 26. PDF/A Validator

Công cụ kiểm tra PDF/A compliance bằng cách verify all requirements theo ISO 19005 standard. Popular validators: veraPDF, Adobe Acrobat PreFlight.

### 27. PDF Optimizer

Công cụ giảm kích thước file PDF bằng cách remove unnecessary objects, recompress streams, và optimize images.

## Related Documents

- [PDF Architecture](../architecture.md)
- [PDF Best Practices](../best-practice.md)
- [PDF Anti-Patterns](../anti-pattern.md)
- [PDF Checklist](../checklist.md)
- [PDF FAQ](../faq.md)
- [PDF Decision Tree](../decision-tree.md)
