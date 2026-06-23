# Checklist cho Hệ Thống Bazi

## 1. Data Validation

### 1.1 Input Date Validation

- [ ] Kiểm tra định dạng ngày sinh (YYYY-MM-DD)
- [ ] Validate ngày sinh trong khoảng hợp lệ (1900-01-01 đến hiện tại)
- [ ] Kiểm tra ngày sinh không phải ngày tương lai
- [ ] Validate định dạng giờ sinh (HH:MM, 00:00-23:59)
- [ ] Kiểm tra múi giờ hợp lệ (IANA timezone format)
- [ ] Validate giới tính (male/female enum)
- [ ] Kiểm tra timezone có hỗ trợ DST không
- [ ] Validate leap year và ngày nhuận âm lịch

### 1.2 Data Sanitization

- [ ] Loại bỏ whitespace thừa từ input
- [ ] Escape special characters trong user-provided name
- [ ] Validate độ dài tối đa của các trường string
- [ ] Kiểm tra Unicode/UTF-8 encoding
- [ ] Sanitize HTML trong response để tránh XSS

### 1.3 Business Rules Validation

- [ ] Ngày sinh phải là ngày hợp lệ (không phải 30/2)
- [ ] Giờ sinh phải nằm trong khoảng 23:00-01:00 cho Giờ Tý
- [ ] Kiểm tra ngày nhuận âm lịch (tháng nhuận)
- [ ] Validate sự phù hợp của Can Chi với năm sinh

## 2. Lunar Calendar Conversion

### 2.1 Core Conversion Logic

- [ ] Sử dụng thư viện/chế độ âm lịch đã được kiểm chứng
- [ ] Hỗ trợ múi giờ Việt Nam (Asia/Ho_Chi_Minh)
- [ ] Xử lý năm nhuận (tháng nhuận trong âm lịch)
- [ ] Tính toán chính xác ngày bắt đầu tháng âm lịch
- [ ] Xử lý tháng nhuận đúng cách (tháng nhuận nào trong năm)
- [ ] Đảm bảo độ chính xác cho các năm từ 1900-2100

### 2.2 Edge Cases

- [ ] Xử lý ngày Tết Nguyên Đán (mùng 1 tháng 1 âm lịch)
- [ ] Xử lý ngày rằm (15 tháng âm lịch)
- [ ] Xử lý năm có 13 tháng nhuận
- [ ] Xử lý ngày giao thừa (30 Tết âm lịch)
- [ ] Kiểm tra conversion với historical dates

### 2.3 Testing

- [ ] Unit test cho các ngày cố định (Tết 2020, 2024)
- [ ] Integration test với nguồn dữ liệu chuẩn
- [ ] Benchmark để đảm bảo performance
- [ ] Test với các edge cases (ngày nhuận, tháng nhuận)

## 3. Bazi Calculation

### 3.1 Thiên Can (Heavenly Stems)

- [ ] Tính Can cho Năm đúng công thức (năm + 6) % 10
- [ ] Tính Can cho Tháng theo Năm Can
- [ ] Tính Can cho Ngày theo Lịch Julius
- [ ] Tính Can cho Giờ theo Ngày Can
- [ ] Đảm bảo đủ 10 Thiên Can: Giáp, Ất, Bính, Đinh, Mậu, Kỷ, Canh, Tân, Nhâm, Quý

### 3.2 Địa Chi (Earthly Branches)

- [ ] Tính Chi cho Năm đúng công thức (năm + 8) % 12
- [ ] Tính Chi cho Tháng theo tháng Dương lịch + 1
- [ ] Tính Chi cho Ngày theo Lịch Julius
- [ ] Tính Chi cho Giờ theo giờ sinh (23:00-01:00 = Tý)
- [ ] Đảm bảo đủ 12 Địa Chi: Tý, Sửu, Dần, Mão, Thìn, Tỵ, Ngọ, Mùi, Thân, Dậu, Tuất, Hợi

### 3.3 Tứ Trụ (Four Pillars)

- [ ] Năm Trụ (Year Pillar) chính xác
- [ ] Tháng Trụ (Month Pillar) chính xác
- [ ] Ngày Trụ (Day Pillar) chính xác
- [ ] Giờ Trụ (Hour Pillar) chính xác
- [ ] Can ẩn trong Chi (Hidden Stems) đầy đủ

### 3.4 Ngũ Hành (Five Elements)

- [ ] Xác định hành của mỗi Thiên Can
- [ ] Xác định hành của mỗi Địa Chi
- [ ] Tính tổng balance giữa 5 hành
- [ ] Xác định hành vượng (dominant)
- [ ] Xác định hành suy (weak)
- [ ] Áp dụng quy luật tương sinh (Mộc→Hỏa→Thổ→Kim→Thủy→Mộc)
- [ ] Áp dụng quy luật tương khắc (Mộc→Thổ→Thủy→Hỏa→Kim→Mộc)

## 4. Nạp Âm (Ten Heavenly Stems + Earthly Branches)

### 4.1 Nạp Âm Table

- [ ] Có đầy đủ 60 Nạp Âm combinations
- [ ] Nạp Âm cho Năm chính xác
- [ ] Nạp Âm cho Tháng chính xác
- [ ] Nạp Âm cho Ngày chính xác
- [ ] Nạp Âm cho Giờ chính xác

### 4.2 Nạp Âm Properties

- [ ] Xác định hành của mỗi Nạp Âm
- [ ] Lấy description cho mỗi Nạp Âm
- [ ] Xác định hướng tốt cho mỗi Nạp Âm
- [ ] Xác định màu sắc may mắn
- [ ] Xác định con số may mắn

### 4.3 Nạp Âm Known Values

- [ ] Hải Trung Kim (Giáp-Ất Tý)
- [ ] Diện Không Hỏa (Bính-Đinh Tý)
- [ ] Sơn Hạ Hỏa (Mậu-Kỷ Tý)
- [ ] Lộ Bàng Thổ (Canh-Tân Tý)
- [ ] Đại Khê Thủy (Nhâm-Quý Tý)
- [ ] (Tiếp tục cho 55 Nạp Âm còn lại)

## 5. Cung Mệnh (Destiny)

### 5.1 Cung Mệnh Calculation

- [ ] Xác định Cung Mệnh dựa trên Ngày Can và Giới tính
- [ ] Áp dụng Nam mệnh thập tự pháp
- [ ] Áp dụng Nữ mệnh thập tự pháp
- [ ] Tính toán chính xác cho Nam/Nữ

### 5.2 Cung Mệnh Properties

- [ ] Xác định hành của Cung Mệnh
- [ ] Lấy mô tả tính cách
- [ ] Xác định điểm mạnh
- [ ] Xác định điểm yếu
- [ ] Xác định hành tương hợp
- [ ] Xác định hành tương khắc
- [ ] Xác định hướng tốt/xấu

### 5.3 Cung Mệnh Values

- [ ] Kim (Thin Kim, Pbục Kim)
- [ ] Mộc (Bình Mộc, Tư Mệnh)
- [ ] Thủy (Phương Thủy, Quý Thủy)
- [ ] Hỏa (Tướng Hỏa, Cụ Hỏa)
- [ ] Thổ (Tọa Thổ, Thổ Tích)

## 6. API Development

### 6.1 RESTful API Design

- [ ] Sử dụng proper HTTP methods (GET, POST, PUT, DELETE)
- [ ] Sử dụng proper status codes (200, 201, 400, 404, 500)
- [ ] Consistent API versioning (/api/v1/)
- [ ] RESTful resource naming (/bazi/charts/:id)
- [ ] Proper error response format
- [ ] Pagination cho list endpoints

### 6.2 Request/Response

- [ ] JSON request/response format
- [ ] Request validation với schema
- [ ] Response envelope format
- [ ] Content-Type header application/json
- [ ] CORS headers nếu cần
- [ ] Cache-Control headers

### 6.3 Authentication & Authorization

- [ ] API key authentication
- [ ] JWT token validation
- [ ] Rate limiting
- [ ] User ownership validation
- [ ] Scope-based permissions

## 7. Database Design

### 7.1 Schema Design

- [ ] Bảng bazi_charts với đầy đủ columns
- [ ] Bảng bazi_reports cho phân tích
- [ ] Bảng bazi_relations cho quan hệ
- [ ] Bảng users để liên kết
- [ ] Proper foreign keys
- [ ] UUID primary keys

### 7.2 Indexes

- [ ] Index trên user_id
- [ ] Index trên birth_date
- [ ] Index trên created_at
- [ ] Composite indexes cho common queries
- [ ] Partial indexes cho filtered queries

### 7.3 Data Integrity

- [ ] NOT NULL constraints cho required fields
- [ ] UNIQUE constraints cho chart IDs
- [ ] CHECK constraints cho enum values
- [ ] Default values cho optional fields
- [ ] ON DELETE CASCADE cho related tables

## 8. Caching Strategy

### 8.1 Cache Implementation

- [ ] Redis cache cho chart data
- [ ] Cache key naming convention
- [ ] TTL settings hợp lý
- [ ] Cache invalidation strategy
- [ ] Cache-aside pattern implementation

### 8.2 Cache Optimization

- [ ] Cache lunar date conversions
- [ ] Cache nap am lookups
- [ ] Multi-level caching (memory + Redis)
- [ ] Cache warming cho hot data
- [ ] Cache eviction policy

## 9. Error Handling

### 9.1 Error Types

- [ ] ValidationError (400)
- [ ] ChartNotFoundError (404)
- [ ] UnauthorizedError (403)
- [ ] LunarConversionError (422)
- [ ] InternalServerError (500)

### 9.2 Error Response Format

- [ ] Consistent error schema
- [ ] Error code machine-readable
- [ ] Error message user-friendly
- [ ] Error details for debugging
- [ ] Request ID for tracing

### 9.3 Error Logging

- [ ] Structured logging format
- [ ] Log levels (error, warn, info)
- [ ] Request context in logs
- [ ] Stack trace for errors
- [ ] Metrics for error rates

## 10. Performance

### 10.1 Response Time

- [ ] P95 response time < 500ms cho read operations
- [ ] P95 response time < 2s cho write operations
- [ ] Database query optimization
- [ ] Connection pooling
- [ ] Async processing cho heavy operations

### 10.2 Scalability

- [ ] Stateless application
- [ ] Horizontal scaling ready
- [ ] Load balancing compatible
- [ ] Session management external

## 11. Testing

### 11.1 Unit Tests

- [ ] Calculator unit tests (Year/Month/Day/Hour pillars)
- [ ] Element balance calculation tests
- [ ] Nap am lookup tests
- [ ] Cung menh calculation tests
- [ ] Input validation tests

### 11.2 Integration Tests

- [ ] API endpoint tests
- [ ] Database integration tests
- [ ] Cache integration tests
- [ ] Lunar calendar service tests

### 11.3 Test Coverage

- [ ] Overall coverage > 80%
- [ ] Critical paths > 90%
- [ ] Edge cases covered
- [ ] Error paths covered

## 12. Security

### 12.1 Input Security

- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] Input length limits
- [ ] Character whitelist validation

### 12.2 Data Security

- [ ] Sensitive data encryption
- [ ] Secure data transmission (HTTPS)
- [ ] Data privacy compliance
- [ ] Audit logging

### 12.3 API Security

- [ ] Rate limiting
- [ ] API key validation
- [ ] Request signing
- [ ] IP allowlisting (optional)

## 13. Documentation

### 13.1 Code Documentation

- [ ] JSDoc/TSDoc comments
- [ ] Complex logic explained
- [ ] Constant values documented
- [ ] Business rules explained

### 13.2 API Documentation

- [ ] OpenAPI/Swagger spec
- [ ] Request/Response examples
- [ ] Error codes documented
- [ ] Authentication documented

### 13.3 Architecture Documentation

- [ ] System architecture diagram
- [ ] Data flow diagrams
- [ ] Database schema documentation
- [ ] Deployment guide

## 14. Monitoring & Logging

### 14.1 Metrics

- [ ] Request count metrics
- [ ] Response time histograms
- [ ] Error rate counters
- [ ] Cache hit/miss rates
- [ ] System health metrics

### 14.2 Logging

- [ ] Structured log format
- [ ] Request ID tracing
- [ ] Performance logging
- [ ] Error logging with context
- [ ] Audit logging

### 14.3 Alerts

- [ ] Error rate alerts
- [ ] Response time alerts
- [ ] System health alerts
- [ ] Cache failure alerts
