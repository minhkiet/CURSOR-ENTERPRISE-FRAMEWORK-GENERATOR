# Checklist cho Hệ Thống Tử Vi

## 1. Data Validation

### 1.1 Input Date Validation

- [ ] Kiểm tra định dạng ngày sinh (YYYY-MM-DD)
- [ ] Validate ngày sinh trong khoảng hợp lệ (1900-01-01 đến hiện tại)
- [ ] Kiểm tra ngày sinh không phải ngày tương lai
- [ ] Validate định dạng giờ sinh (HH:MM, 00:00-23:59)
- [ ] Kiểm tra múi giờ hợp lệ (IANA timezone)
- [ ] Validate giới tính (male/female enum)
- [ ] Validate giây phút hợp lệ (00-59)

### 1.2 Lunar Date Validation

- [ ] Ngày âm lịch trong khoảng 1-30
- [ ] Tháng âm lịch trong khoảng 1-13
- [ ] Xử lý tháng nhuận (leap month)
- [ ] Validate ngày Tết Nguyên Đán
- [ ] Validate ngày rằm (15 âm lịch)

### 1.3 Business Rules Validation

- [ ] Giờ sinh phải nằm trong khoảng giờ hợp lệ
- [ ] Ngày sinh phải là ngày hợp lệ trong tháng
- [ ] Năm âm lịch phải tương ứng với năm dương lịch

## 2. Lunar Calendar Conversion

### 2.1 Core Conversion Logic

- [ ] Chuyển đổi Dương lịch → Âm lịch chính xác
- [ ] Hỗ trợ múi giờ Asia/Ho_Chi_Minh
- [ ] Xử lý năm nhuận âm lịch
- [ ] Xác định tháng nhuận đúng cách
- [ ] Độ chính xác cho năm 1900-2100

### 2.2 Edge Cases

- [ ] Ngày Tết Nguyên Đán
- [ ] Ngày giao thừa (30 Tết)
- [ ] Tháng có 29 hoặc 30 ngày
- [ ] Năm có 12 hoặc 13 tháng
- [ ] Historical dates (1900-1950)

## 3. Menh Cach Calculation

### 3.1 Menh Calculation

- [ ] Lấy Ngày Can Chi chính xác
- [ ] Áp dụng bảng Nam mệnh đúng
- [ ] Áp dụng bảng Nữ mệnh đúng
- [ ] Xác định Ngũ Hành của Mệnh
- [ ] Tính Nhị Thập Bát Tú
- [ ] Tính Thập Thiên Niên

### 3.2 Menh Table Validation

- [ ] Giáp → Kim/Mộc
- [ ] Ất → Kim/Mộc
- [ ] Bính → Thủy/Hỏa
- [ ] Đinh → Thủy/Hỏa
- [ ] Mậu → Hỏa/Thổ
- [ ] Kỷ → Hỏa/Thổ
- [ ] Canh → Thổ/Kim
- [ ] Tân → Thổ/Kim
- [ ] Nhâm → Kim/Thủy
- [ ] Quý → Kim/Thủy

## 4. Cung Management

### 4.1 12 Cung Structure

- [ ] Cung Mệnh (index 0)
- [ ] Cung Phụ Mẫu (index 1)
- [ ] Cung Phúc Đức (index 2)
- [ ] Cung Điền Trạch (index 3)
- [ ] Cung Quan Lộc (index 4)
- [ ] Cung Nô Bộc (index 5)
- [ ] Cung Thiên Di (index 6)
- [ ] Cung Tật Ách (index 7)
- [ ] Cung Tài Bạch (index 8)
- [ ] Cung Tử Tức (index 9)
- [ ] Cung Phu Thê (index 10)
- [ ] Cung Huỵệt (index 11)

### 4.2 Cung Properties

- [ ] Tên cung (name)
- [ ] Index trong 12 cung
- [ ] Vị trí so với Cung Mệnh
- [ ] Danh sách sao trong cung
- [ ] Có trống không (isEmpty)
- [ ] Sao chiếm cung (occupant)
- [ ] Sao chủ cung (owner)
- [ ] Hành của cung

### 4.3 Cung Element Mapping

- [ ] Mệnh: Kim
- [ ] Phụ Mẫu: Thổ
- [ ] Phúc Đức: Thổ
- [ ] Điền Trạch: Thổ
- [ ] Quan Lộc: Kim
- [ ] Nô Bộc: Kim
- [ ] Thiên Di: Thủy
- [ ] Tật Ách: Thủy
- [ ] Tài Bạch: Kim
- [ ] Tử Tức: Mộc
- [ ] Phu Thê: Hỏa
- [ ] Huỵệt: Hỏa

## 5. Sao Management

### 5.1 Sao Chinh (Main Stars)

- [ ] Tử Vi
- [ ] Thiên Cơ
- [ ] Thái Dương
- [ ] Thái Âm
- [ ] Văn Xương
- [ ] Văn Khúc
- [ ] Liêm Trinh
- [ ] Thiên Đồng
- [ ] Thiên Giáp
- [ ] Cự Môn
- [ ] Đà La
- [ ] Hóa Lưc Cổ
- [ ] Lộc Tồn
- [ ] Kình Dương
- [ ] Đường Phù
- [ ] Tang Môn
- [ ] Hy Vọng
- [ ] Tam Thai
- [ ] Bát Tọa
- [ ] Phong Cáo

### 5.2 Sao Phu (Secondary Stars)

- [ ] Tả Phụ
- [ ] Hữu Bật
- [ ] Xương Cu
- [ ] Khúc Cu
- [ ] Thiên Hỷ
- [ ] Thiên Quý
- [ ] Ân Quang
- [ ] Thiên Thời
- [ ] Thiên Sứ
- [ ] Thiên Mã

### 5.3 Sao Properties

- [ ] Tên sao
- [ ] Loại sao (chinh/phu/tutan/batquai)
- [ ] Hành (Ngũ Hành)
- [ ] Độ sáng (duong/am/trung)
- [ ] Ý nghĩa
- [ ] Thuộc vận hạn không

### 5.4 Sao Position Rules

- [ ] Sao nhập cung theo Ngày
- [ ] Sao nhập cung theo Tháng
- [ ] Sao nhập cung theo Năm
- [ ] Sao nhập cung theo Giờ
- [ ] Sắp xếp sao vào 12 cung

## 6. Van Han Calculation

### 6.1 Van Types

- [ ] Thiên Vận (0-39 tuổi)
- [ ] Nhân Vận (40-79 tuổi)
- [ ] Địa Vận (80-120 tuổi)

### 6.2 Han Calculation

- [ ] 12 Thiên Hạn
- [ ] 12 Nhân Hạn
- [ ] 12 Địa Hạn
- [ ] Hạn theo tuổi
- [ ] Hạn theo giới tính

### 6.3 Van Han Properties

- [ ] Năm vận
- [ ] Tuổi
- [ ] Loại vận (thien/nhan/dia)
- [ ] Danh sách hạn
- [ ] Tai Bach
- [ ] Sát Sát
- [ ] Thần
- [ ] Hạc Dương
- [ ] Lịch sử vận
- [ ] Dự đoán

## 7. Phuong Men

### 7.1 Tuong Tac Nguyen Hanh

- [ ] Xác định hành của Mệnh
- [ ] Xác định hành của các Cung
- [ ] Tính tương sinh
- [ ] Tính tương khắc
- [ ] Xác định hành có lợi
- [ ] Xác định hành bất lợi

### 7.2 Phuong Huong

- [ ] Hướng tốt cho Mệnh
- [ ] Hướng xấu cho Mệnh
- [ ] Màu sắc tương hợp
- [ ] Con số may mắn
- [ ] Tháng tốt
- [ ] Ngày tốt

## 8. API Development

### 8.1 RESTful API Design

- [ ] Sử dụng HTTP methods đúng (GET, POST, PUT, DELETE)
- [ ] Status codes chính xác (200, 201, 400, 404, 500)
- [ ] API versioning (/api/v1/tuvi)
- [ ] RESTful resource naming
- [ ] Consistent error format
- [ ] Pagination cho list endpoints

### 8.2 Request/Response

- [ ] JSON format
- [ ] Request validation
- [ ] Response envelope
- [ ] Content-Type header
- [ ] CORS headers
- [ ] Cache-Control headers

### 8.3 Endpoints

- [ ] POST /charts - Tạo chart
- [ ] GET /charts/:id - Lấy chart
- [ ] GET /charts/user/:userId - Danh sách charts
- [ ] PUT /charts/:id - Cập nhật chart
- [ ] DELETE /charts/:id - Xóa chart
- [ ] GET /charts/:id/analysis - Phân tích
- [ ] GET /charts/:id/cung - Chi tiết cung
- [ ] GET /charts/:id/sao - Chi tiết sao
- [ ] GET /charts/:id/van-han - Chi tiết vận hạn
- [ ] GET /charts/:id/report - Full report

## 9. Database Design

### 9.1 Schema Design

- [ ] Bảng tuvi_charts
- [ ] Bảng chart_cungs
- [ ] Bảng chart_saos
- [ ] Bảng van_han
- [ ] Bảng analysis
- [ ] Foreign keys đúng
- [ ] UUID primary keys

### 9.2 Indexes

- [ ] Index trên user_id
- [ ] Index trên birth_date
- [ ] Index trên created_at
- [ ] Composite indexes
- [ ] Partial indexes

### 9.3 Data Integrity

- [ ] NOT NULL constraints
- [ ] UNIQUE constraints
- [ ] CHECK constraints
- [ ] Default values
- [ ] ON DELETE CASCADE

## 10. Caching

### 10.1 Cache Strategy

- [ ] Cache chart data
- [ ] Cache analysis results
- [ ] Cache lookup tables
- [ ] Cache conversion results
- [ ] TTL settings hợp lý

### 10.2 Cache Invalidation

- [ ] Xóa cache khi update chart
- [ ] Xóa cache khi xóa chart
- [ ] Batch cache invalidation
- [ ] Cache warming

## 11. Error Handling

### 11.1 Error Types

- [ ] ValidationError (400)
- [ ] ChartNotFoundError (404)
- [ ] UnauthorizedError (403)
- [ ] LunarConversionError (422)
- [ ] InternalServerError (500)

### 11.2 Error Response

- [ ] Consistent error schema
- [ ] Machine-readable error codes
- [ ] User-friendly messages
- [ ] Error details
- [ ] Request ID

### 11.3 Error Logging

- [ ] Structured logging
- [ ] Log levels
- [ ] Request context
- [ ] Stack traces
- [ ] Error metrics

## 12. Performance

### 12.1 Response Time

- [ ] P95 < 500ms cho read operations
- [ ] P95 < 2s cho write operations
- [ ] Database optimization
- [ ] Connection pooling
- [ ] Async processing

### 12.2 Scalability

- [ ] Stateless application
- [ ] Horizontal scaling
- [ ] Load balancing
- [ ] Session management external

## 13. Testing

### 13.1 Unit Tests

- [ ] MenhCach calculation tests
- [ ] Cung calculation tests
- [ ] Sao position tests
- [ ] VanHan calculation tests
- [ ] Input validation tests

### 13.2 Integration Tests

- [ ] API endpoint tests
- [ ] Database tests
- [ ] Cache tests
- [ ] Lunar conversion tests

### 13.3 Test Coverage

- [ ] Overall coverage > 80%
- [ ] Critical paths > 90%
- [ ] Edge cases covered
- [ ] Error paths covered

## 14. Security

### 14.1 Input Security

- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] Input length limits
- [ ] Character validation

### 14.2 Data Security

- [ ] Encryption cho sensitive data
- [ ] HTTPS only
- [ ] Data privacy
- [ ] Audit logging

### 14.3 API Security

- [ ] Rate limiting
- [ ] API key validation
- [ ] Request signing
- [ ] IP allowlisting

## 15. Documentation

### 15.1 Code Documentation

- [ ] JSDoc/TSDoc comments
- [ ] Complex logic explained
- [ ] Constant values documented
- [ ] Business rules explained

### 15.2 API Documentation

- [ ] OpenAPI/Swagger spec
- [ ] Request/Response examples
- [ ] Error codes documented
- [ ] Authentication documented

### 15.3 Architecture Documentation

- [ ] System architecture diagram
- [ ] Data flow diagrams
- [ ] Database schema
- [ ] Deployment guide

## 16. Monitoring

### 16.1 Metrics

- [ ] Request count
- [ ] Response time histograms
- [ ] Error rate counters
- [ ] Cache hit/miss rates
- [ ] System health

### 16.2 Logging

- [ ] Structured log format
- [ ] Request ID tracing
- [ ] Performance logging
- [ ] Error logging

### 16.3 Alerts

- [ ] Error rate alerts
- [ ] Response time alerts
- [ ] System health alerts
- [ ] Cache failure alerts
