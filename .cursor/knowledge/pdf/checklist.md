---
title: "PDF Pre-Deployment Checklist - Danh Sách Kiểm Tra Trước Triển Khai"
description: "Comprehensive pre-deployment checklist for PDF generation and processing systems covering security, performance, accessibility, monitoring, and compliance requirements"
tags: ["pdf", "checklist", "deployment", "production", "quality-assurance", "cursor-enterprise-framework"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# PDF Pre-Deployment Checklist - Danh Sách Kiểm Tra Trước Triển Khai

## Overview

Trước khi deploy bất kỳ hệ thống PDF nào lên production, điều quan trọng là phải thực hiện một loạt các checks và verifications để đảm bảo rằng hệ thống hoạt động đúng, secure, và scalable. Checklist này được thiết kế để cover tất cả các khía cạnh quan trọng của PDF processing, từ security và performance đến accessibility và compliance. Mỗi item trong checklist đều có rationale giải thích tại sao nó quan trọng và expected outcome khi pass.

Việc sử dụng checklist này không chỉ giúp prevent production incidents mà còn tiết kiệm significant time và resources bằng cách catch issues early. Một issue được phát hiện trong development có chi phí fix thấp hơn nhiều so với khi nó đã ở production. Đặc biệt với PDF processing, nơi mà output correctness và file size có thể có legal implications (như signed documents hoặc financial reports), việc có một systematic verification process là absolutely essential.

## Purpose

Danh sách kiểm tra này phục vụ nhiều mục đích quan trọng trong quy trình phát triển và deployment. Đầu tiên, nó cung cấp một systematic approach để verify tất cả critical aspects của PDF system trước khi release. Thứ hai, nó giúp standardize quality process giữa các teams và projects. Thứ ba, checklist này serve as documentation của những gì đã được verified, hữu ích cho audit và compliance purposes. Cuối cùng, nó giúp reduce cognitive load cho developers bằng cách break down complex verification into manageable items.

## Key Concepts

### 1. Pre-Deployment Testing Philosophy

Pre-deployment testing không chỉ là "kiểm tra xem code có chạy không". Nó phải bao gồm comprehensive verification of correctness, performance, security, và maintainability. Một PDF system có thể "chạy được" nhưng vẫn có bugs nghiêm trọng như memory leaks, security vulnerabilities, hoặc incorrect rendering. Testing philosophy của chúng ta phải cover tất cả these dimensions.

### 2. Risk-Based Verification

Không phải tất cả items trong checklist đều có equal importance. Một số items, như security checks, là critical và phải pass trước khi deploy. Others, như documentation checks, có thể be deferred. Điều quan trọng là phải distinguish giữa blockers và nice-to-haves và allocate testing resources accordingly.

### 3. Automated vs Manual Verification

Nhiều items trong checklist có thể be automated, và nên được. Automated tests chạy consistently mỗi lần và không bị human error. Tuy nhiên, some aspects (như visual quality review hoặc accessibility audit) vẫn cần human judgment. A good pre-deployment process combines both approaches.

## Pre-Deployment Checklist

### Section 1: Security Verification

#### [ ] 1.1 Input Validation Complete

**Mô tả**: Verify rằng tất cả user inputs được validated trước khi sử dụng trong PDF generation.

**Verification Steps**:

```bash
# Test with malicious inputs
curl -X POST /api/generate-pdf \
  -d '{"filename": "../../../etc/passwd"}'

curl -X POST /api/generate-pdf \
  -d '{"template": "<script>alert(1)</script>"}'

curl -X POST /api/generate-pdf \
  -d '{"data": {"__proto__:": "injected"}}'
```

**Expected Outcome**: Tất cả malicious inputs được rejected với appropriate error messages, không có path traversal hoặc injection possible.

**Rationale**: User inputs trong PDF generation có thể là entry point cho path traversal, XSS (nếu HTML rendered), và prototype pollution attacks.

#### [ ] 1.2 File Path Security

**Mô tả**: Verify rằng all file operations sử dụng safe path handling.

**Verification Steps**:

```bash
# Test path traversal attempts
curl "/api/download?file=../../../app/secrets.txt"
curl "/api/download?file=..%2F..%2F..%2Fetc%2Fpasswd"
curl "/api/download?file=..%5C..%5C..%5CWindows%5CSystem32"
```

**Expected Outcome**: Tất cả path traversal attempts được blocked, server returns 403 Forbidden.

**Code Review Checklist**:

```javascript
// Verify these patterns are in place:
1. path.resolve() được sử dụng
2. Path whitelist được implemented
3. path.normalize() được applied
4. Null byte injection được prevented
5. Absolute path inputs được rejected
```

#### [ ] 1.3 Rate Limiting và Rate Limiting Bypass

**Mô tả**: Verify rằng rate limiting được implemented đúng cách.

**Verification Steps**:

```bash
# Test rate limiting
for i in {1..110}; do
  curl -o /dev/null -s -w "%{http_code}\n" \
    http://localhost:3000/api/generate-pdf
done
```

**Expected Outcome**: Sau 100 requests trong 1 phút, subsequent requests được throttled với 429 Too Many Requests response.

**Rationale**: PDF generation là CPU-intensive. Không có rate limiting, attackers có thể abuse system cho DoS hoặc resource exhaustion.

#### [ ] 1.4 Authentication và Authorization

**Mô tả**: Verify rằng all PDF endpoints require proper authentication.

**Verification Steps**:

```bash
# Test unauthenticated access
curl http://localhost:3000/api/generate-pdf

# Test unauthorized access to other user's documents
curl -H "Authorization: Bearer $USER1_TOKEN" \
  http://localhost:3000/api/documents/USER2_DOC_ID/pdf
```

**Expected Outcome**: Unauthenticated requests nhận 401 Unauthorized. Unauthorized access requests nhận 403 Forbidden.

#### [ ] 1.5 Sensitive Data Handling

**Mô tả**: Verify rằng sensitive data (PII, credentials) không được logged hoặc exposed.

**Verification Steps**:

```bash
# Search logs for sensitive patterns
grep -r "password\|secret\|token\|ssn\|credit_card" ./logs/

# Check API responses
curl http://localhost:3000/api/generate-pdf/123 | jq .
```

**Expected Outcome**: Không có sensitive data trong logs. API responses không chứa unintended sensitive information.

#### [ ] 1.6 HTTPS Enforcement

**Mô tả**: Verify rằng PDF endpoints chỉ accessible qua HTTPS.

**Verification Steps**:

```bash
# Test HTTP access
curl http://localhost:3000/api/generate-pdf

# Verify HSTS headers
curl -I https://localhost:3000/api/generate-pdf | grep -i strict-transport
```

**Expected Outcome**: HTTP requests được redirected sang HTTPS. HSTS header được present trong HTTPS responses.

#### [ ] 1.7 CSP Headers

**Mô tả**: Verify rằng Content Security Policy được properly configured.

**Verification Steps**:

```bash
curl -I https://localhost:3000/api/generate-pdf | grep -i content-security-policy
```

**Expected Outcome**: CSP header được present và appropriately restrictive.

### Section 2: Performance Verification

#### [ ] 2.1 Load Testing Complete

**Mô tả**: Verify system handles expected production load.

**Verification Steps**:

```bash
# Using Apache Bench
ab -n 1000 -c 50 -T "application/json" \
  -p request.json \
  http://localhost:3000/api/generate-pdf

# Using k6
k6 run --vus 50 --duration 60s load-test.js
```

**Expected Outcome**:

- p95 latency < 3 seconds
- Error rate < 1%
- No memory leaks over sustained load
- CPU usage < 80% under sustained load

**Load Test Configuration Example** (k6):

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<3000'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.post(
    'http://localhost:3000/api/generate-pdf',
    JSON.stringify({ template: 'invoice', data: generateTestData() }),
    { headers: { 'Content-Type': 'application/json' } }
  );
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'content type is pdf': (r) => r.headers['Content-Type'] === 'application/pdf',
    'response time < 3s': (r) => r.timings.duration < 3000,
  });
  
  sleep(1);
}
```

#### [ ] 2.2 Memory Profiling

**Mô tả**: Verify no memory leaks under sustained operation.

**Verification Steps**:

```bash
# Run with memory monitoring
node --expose-gc --inspect server.js &
# Attach Chrome DevTools or use clinic.js

# Using clinic.js
clinic doctor -- node server.js

# Check for memory growth
watch -n 5 'curl -s localhost:3000/metrics | grep nodejs_heap'
```

**Expected Outcome**:

- Memory usage stable over 1 hour of operation
- No gradual memory growth
- GC runs don't cause significant pauses

#### [ ] 2.3 PDF File Size Optimization

**Mô tả**: Verify generated PDFs meet size requirements.

**Verification Steps**:

```bash
# Generate test PDFs và check sizes
for i in {1..20}; do
  curl -s -o "test-pdf-$i.pdf" \
    -d "template=invoice&data=$TEST_DATA" \
    http://localhost:3000/api/generate-pdf
  ls -lh "test-pdf-$i.pdf"
done

# Calculate statistics
awk '{sum+=$5; count++} END {print "Average:", sum/count, "KB"}' < <(ls -l *.pdf)
```

**Expected Outcome**:

- Average PDF size < 500KB for typical documents
- No PDFs > 2MB (except explicitly large documents)
- Font subsetting working (verify with pdffonts tool)

```bash
# Verify font subsetting
pdffonts test-pdf.pdf
# Output should show subset fonts, not full fonts
```

#### [ ] 2.4 Caching Verification

**Mô tả**: Verify caching layer is working correctly.

**Verification Steps**:

```bash
# First request (cache miss)
time curl -s -o /dev/null http://localhost:3000/api/generate-pdf/invoice-123

# Second request (should be cache hit)
time curl -s -o /dev/null http://localhost:3000/api/generate-pdf/invoice-123

# Check cache headers
curl -I http://localhost:3000/api/generate-pdf/invoice-123
# Should have X-Cache: HIT header on second request
```

**Expected Outcome**:

- Second request significantly faster (< 100ms vs > 1000ms)
- Cache hit rate > 80% for repeated content
- Cache invalidation working correctly

#### [ ] 2.5 Concurrent Request Handling

**Mô tả**: Verify system handles concurrent requests properly.

**Verification Steps**:

```javascript
// concurrent-test.js
const axios = require('axios');

async function testConcurrency() {
  const promises = [];
  const numConcurrent = 50;
  
  for (let i = 0; i < numConcurrent; i++) {
    promises.push(
      axios.post(
        'http://localhost:3000/api/generate-pdf',
        { template: 'invoice', data: { id: i } },
        { responseType: 'arraybuffer' }
      )
    );
  }
  
  const results = await Promise.allSettled(promises);
  
  const successes = results.filter(r => r.status === 'fulfilled');
  const failures = results.filter(r => r.status === 'rejected');
  
  console.log(`Success: ${successes.length}/${numConcurrent}`);
  console.log(`Failures: ${failures.length}/${numConcurrent}`);
  
  // Verify each PDF is correct
  for (const result of successes) {
    const isValidPDF = validatePDFBuffer(result.value.data);
    if (!isValidPDF) {
      console.error('Invalid PDF received');
    }
  }
}
```

**Expected Outcome**:

- All or almost all requests succeed
- No race conditions (each user gets their own PDF)
- No corrupted outputs

### Section 3: Functional Verification

#### [ ] 3.1 Template Rendering Tests

**Mô tả**: Verify all templates render correctly.

**Verification Steps**:

```bash
# Test each template
for template in invoice receipt report contract statement; do
  curl -X POST http://localhost:3000/api/generate-pdf \
    -d "template=$template" \
    -d "data=$(cat test-data/$template.json)" \
    -o "test-$template.pdf"
  
  # Verify PDF is valid
  file "test-$template.pdf"
  pdfinfo "test-$template.pdf"
done
```

**Expected Outcome**:

- All templates produce valid PDF files
- Content matches expected template structure
- No missing or overlapping elements

#### [ ] 3.2 Data Binding Tests

**Mô tả**: Verify dynamic data renders correctly in PDFs.

**Verification Steps**:

```javascript
// Test with various data types
const testCases = [
  { name: 'unicode', data: { name: 'Nguyễn Văn A', address: '123 Đường ABC, Hà Nội' }},
  { name: 'empty', data: { name: '', address: '' }},
  { name: 'long_text', data: { name: 'A'.repeat(1000) }},
  { name: 'special_chars', data: { name: '<script>"\'&' }},
  { name: 'numbers', data: { amount: 1234567890.99, tax: 0.001 }},
  { name: 'dates', data: { created: '2026-01-01T00:00:00Z', due: '2026-12-31' }},
  { name: 'arrays', data: { items: [{name: 'Item 1'}, {name: 'Item 2'}] }}
];

for (const test of testCases) {
  const result = await generatePDF('invoice', test.data);
  verifyPDFContent(result, test);
}
```

**Expected Outcome**:

- All data types render correctly
- No encoding issues with unicode
- Empty values handled gracefully
- Special characters escaped properly
- No content overflow or clipping

#### [ ] 3.3 Image Handling Tests

**Mô tả**: Verify images of various types and sizes render correctly.

**Verification Steps**:

```bash
# Test various image formats
- PNG 4K (5000x3000px, ~5MB)
- JPEG high quality (4000x3000px, ~3MB)
- JPEG low quality (2000x1500px, ~200KB)
- SVG vector graphic
- GIF animated (should render as static)
- WebP format

# Test various sizes
- Very small (10x10px)
- Very large (10000x10000px)
- Non-standard aspect ratios
```

**Expected Outcome**:

- All image formats render
- Large images scaled appropriately
- Aspect ratios preserved
- No image quality degradation beyond expected compression
- No memory errors with extreme sizes

#### [ ] 3.4 Font Rendering Tests

**Mô tả**: Verify fonts render correctly across all supported languages.

**Verification Steps**:

```bash
# Test various scripts
- Latin (English, French, German)
- CJK (Chinese, Japanese, Korean)
- Vietnamese (with diacritics)
- Arabic (RTL)
- Thai
- Devanagari (Hindi)
- Cyrillic (Russian)

# Verify fonts are embedded
pdffonts test-pdf.pdf
pdfinfo test-pdf.pdf | grep -i font
```

**Expected Outcome**:

- All scripts render correctly
- No missing glyphs (boxes or question marks)
- Correct font embedding confirmed
- Font subsetting working (reduced file size)

#### [ ] 3.5 Page Layout Tests

**Mô tả**: Verify layouts work correctly at different page sizes.

**Verification Steps**:

```bash
# Test different page formats
curl -X POST http://localhost:3000/api/generate-pdf \
  -d "template=invoice&format=A4"

curl -X POST http://localhost:3000/api/generate-pdf \
  -d "template=invoice&format=Letter"

curl -X POST http://localhost:3000/api/generate-pdf \
  -d "template=invoice&format=A3"

# Test landscape vs portrait
curl -X POST http://localhost:3000/api/generate-pdf \
  -d "template=invoice&orientation=landscape"
```

**Expected Outcome**:

- All page formats supported
- Content adjusts appropriately
- No overflow or cut-off content
- Margins preserved

### Section 4: Accessibility Verification

#### [ ] 4.1 PDF/UA Compliance

**Mô tả**: Verify generated PDFs meet accessibility standards.

**Verification Steps**:

```bash
# Check for PDF/UA compliance using pdfua-checker or similar
npm install -g pdfua-checker
pdfua-checker test-pdf.pdf

# Manual checks
pdfinfo -meta test-pdf.pdf | grep -i title
pdfinfo -meta test-pdf.pdf | grep -i author

# Check for tags
pdfinfo test-pdf.pdf | grep -i tag
```

**Expected Outcome**:

- Document has title metadata
- Document has author metadata
- Tagged PDF structure present
- Proper language declaration

#### [ ] 4.2 Screen Reader Compatibility

**Mô tả**: Verify PDFs are readable by screen readers.

**Verification Steps**:

```bash
# Extract text and verify reading order
pdftotext -layout test-pdf.pdf - | head -100

# Check for proper structure
# (using PAC - PDF Accessibility Checker if available)
```

**Expected Outcome**:

- Text extraction yields correct content
- Reading order logical
- Headings properly marked
- Links have text descriptions

#### [ ] 4.3 Color Contrast

**Mô tả**: Verify text has sufficient contrast ratios.

**Verification Steps**:

```bash
# Analyze color contrast in generated PDF
# Use tools like Check My Colours or contrast checkers
```

**Expected Outcome**:

- Text contrast ratio > 4.5:1 (normal text)
- Large text contrast ratio > 3:1
- No information conveyed by color alone

### Section 5: Monitoring và Observability

#### [ ] 5.1 Logging Verification

**Mô tả**: Verify appropriate logging is in place.

**Verification Steps**:

```bash
# Generate a PDF và check logs
curl -X POST http://localhost:3000/api/generate-pdf \
  -d "template=invoice&data=$TEST_DATA"

tail -20 logs/application.log

# Verify structured logging format
cat logs/application.log | jq .
```

**Expected Outcome**:

- Request logged with correlation ID
- Generation time logged
- Error details logged (without sensitive data)
- Log format is structured (JSON)

#### [ ] 5.2 Metrics Export

**Mô tả**: Verify metrics are exported correctly.

**Verification Steps**:

```bash
# Check Prometheus metrics endpoint
curl http://localhost:3000/metrics | grep pdf

# Expected metrics:
# pdf_generation_total
# pdf_generation_duration_seconds
# pdf_cache_hits_total
# pdf_cache_misses_total
# pdf_file_size_bytes
```

**Expected Outcome**:

- All expected metrics present
- Metrics properly labeled
- Values are reasonable

#### [ ] 5.3 Health Check Endpoints

**Mô tả**: Verify health check endpoints are working.

**Verification Steps**:

```bash
# Liveness probe
curl http://localhost:3000/health/live

# Readiness probe
curl http://localhost:3000/health/ready

# Detailed health
curl http://localhost:3000/health
```

**Expected Outcome**:

- Liveness returns 200 when app is running
- Readiness returns 200 when ready to serve traffic
- Dependencies (Redis, S3, etc.) checked

### Section 6: Compliance và Legal

#### [ ] 6.1 Data Retention

**Mô tả**: Verify data retention policies are implemented.

**Verification Steps**:

```bash
# Check PDF storage bucket lifecycle
aws s3api get-bucket-lifecycle-configuration \
  --bucket pdf-storage-bucket

# Verify old PDFs are cleaned up
```

**Expected Outcome**:

- Lifecycle policies configured
- PDFs deleted after retention period
- Audit trail of deletions

#### [ ] 6.2 Audit Logging

**Mô tả**: Verify audit trail for sensitive operations.

**Verification Steps**:

```bash
# Check audit logs
grep "sign\|download\|delete" audit.log | tail -20
```

**Expected Outcome**:

- All sensitive operations logged
- Logs include who, what, when
- Logs are immutable (write-once)

#### [ ] 6.3 Digital Signature Compliance

**Mô tả**: Verify digital signatures meet legal requirements.

**Verification Steps**:

```bash
# Sign a test PDF
curl -X POST http://localhost:3000/api/generate-pdf \
  -d "template=contract&sign=true" \
  -o signed-contract.pdf

# Verify signature
openssl pkcs7 -in signed-contract.pdf -inform DER -print

# Check signature validity
```

**Expected Outcome**:

- Signature embedded correctly
- Certificate chain valid
- Timestamp present (if required)

### Section 7: Documentation

#### [ ] 7.1 API Documentation

**Mô tả**: Verify API is properly documented.

**Verification Steps**:

```bash
# Check OpenAPI/Swagger docs
curl http://localhost:3000/api-docs/

# Verify all endpoints documented
```

**Expected Outcome**:

- OpenAPI spec available
- All endpoints have descriptions
- Examples provided

#### [ ] 7.2 Runbook Documentation

**Mô tả**: Verify runbooks exist for common issues.

**Verification Steps**:

```bash
# Check for runbook files
ls -la docs/runbooks/
```

**Expected Outcome**:

- Runbook for PDF generation failures
- Runbook for cache issues
- Runbook for signature verification failures

#### [ ] 7.3 On-Call Documentation

**Mô tả**: Verify on-call documentation is up-to-date.

**Verification Steps**:

```bash
# Check on-call guide
cat docs/oncall-guide.md
```

**Expected Outcome**:

- Contact information current
- Escalation procedures documented
- Common issues and solutions listed

## Post-Deployment Verification

Sau khi deploy lên production, thực hiện các verification sau:

### Immediate Post-Deploy (0-1 hour)

1. **Smoke Tests**: Generate a few test PDFs
2. **Error Rate Monitoring**: Watch error rates in dashboards
3. **Latency Monitoring**: Verify p95 latency is within SLO
4. **Log Review**: Check for any new error patterns

### 24-Hour Review

1. **Performance Review**: Compare against baseline metrics
2. **Cache Hit Rate**: Verify cache is performing as expected
3. **Storage Costs**: Check PDF storage costs
4. **User Feedback**: Monitor for user complaints

### 1-Week Review

1. **Load Pattern Analysis**: Review traffic patterns
2. **Cost Analysis**: Detailed cost breakdown
3. **Security Review**: Check for any suspicious activity
4. **Feature Requests**: Collect and prioritize feedback

## Sign-Off Requirements

Trước khi production deployment, ensure:

- [ ] Security Lead: Approved
- [ ] QA Lead: Approved
- [ ] DevOps Lead: Approved
- [ ] Product Owner: Approved
- [ ] Date: ____________
- [ ] Version: ____________

## Appendix: Test Data

### Sample Test Data Structure

```json
{
  "invoice": {
    "id": "INV-2026-001234",
    "customer": {
      "name": "Nguyễn Văn Minh",
      "address": "123 Đường Lê Lợi, Quận 1, TP.HCM",
      "taxId": "0123456789"
    },
    "items": [
      { "name": "Professional Services", "quantity": 40, "unitPrice": 150000 },
      { "name": "Software License", "quantity": 5, "unitPrice": 2500000 }
    ],
    "subtotal": 18500000,
    "tax": 1850000,
    "total": 20350000
  },
  "report": {
    "title": "Q2 2026 Financial Report",
    "date": "2026-06-30",
    "sections": ["Executive Summary", "Revenue", "Expenses", "Forecast"]
  }
}
```

## References

- OWASP Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- PDF/A Standard: https://www.iso.org/standard/38920.html
- PDF/UA Standard: https://www.pdfa.org/ua-standard/
- Google Web Vitals: https://web.dev/vitals/
- Prometheus Metrics: https://prometheus.io/docs/concepts/metric_types/
