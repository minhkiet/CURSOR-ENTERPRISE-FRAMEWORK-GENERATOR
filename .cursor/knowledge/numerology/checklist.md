# Checklist cho Hệ Thống Numerology

## 1. Data Validation

### 1.1 Name Validation

- [ ] Kiểm tra tên không rỗng
- [ ] Kiểm tra độ dài tối thiểu (>= 2 ký tự)
- [ ] Kiểm tra độ dài tối đa (<= 200 ký tự)
- [ ] Xử lý Vietnamese diacritics (Ạ, ạ, Ỏ, ...)
- [ ] Normalize tên về chữ hoa không dấu
- [ ] Loại bỏ ký tự đặc biệt (chỉ giữ A-Z)
- [ ] Kiểm tra tên có chứa số không

### 1.2 Birth Date Validation

- [ ] Kiểm tra ngày sinh không rỗng
- [ ] Kiểm tra định dạng ngày sinh (YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY)
- [ ] Kiểm tra ngày sinh không phải tương lai
- [ ] Kiểm tra ngày sinh không quá cũ (>= 1900)
- [ ] Kiểm tra ngày hợp lệ (không phải 31/02)
- [ ] Parse Date object từ string

### 1.3 Number Validation

- [ ] Kiểm tra số trong khoảng 1-33
- [ ] Kiểm tra Master Numbers (11, 22, 33)
- [ ] Kiểm tra số nguyên
- [ ] Kiểm tra số dương

## 2. Letter Values

### 2.1 Pythagorean System

- [ ] A=1, B=2, C=3, D=4, E=5
- [ ] F=6, G=7, H=8, I=9
- [ ] J=1, K=2, L=3, M=4, N=5
- [ ] O=6, P=7, Q=8, R=9
- [ ] S=1, T=2, U=3, V=4, W=5
- [ ] X=6, Y=7, Z=8
- [ ] Không có số 9 cho J-S (quay vòng 1-8)

### 2.2 Chaldean System

- [ ] A=1, B=2, C=3, D=4, E=5
- [ ] U=6, O=7, F=8
- [ ] I=9, Y=1, J=1, K=2
- [ ] L=3, M=4, N=5, X=6
- [ ] G=7, H=8, Z=8, P=8
- [ ] Q=1, R=2, S=3, T=4
- [ ] V=6, W=6, D=4
- [ ] Chỉ có 1-8 (không có 9 như Pythagorean)

### 2.3 Vietnamese Diacritics

- [ ] Á, A, À, Ả, Ã, Ạ → A
- [ ] É, È, Ẻ, Ẽ, Ẹ → E
- [ ] Í, Ì, Ỉ, Ĩ, Ị → I
- [ ] Ó, Ò, Ỏ, Õ, Ọ → O
- [ ] Ú, Ù, Ủ, Ũ, Ụ → U
- [ ] Ý, Ỳ, Ỷ, Ỹ, Ỵ → Y
- [ ] Ậ, Ắ, Ằ, Ẳ, Ẵ, Ặ → A
- [ ] Ế, Ề, Ể, Ễ, Ệ → E
- [ ] Ố, Ồ, Ổ, Ỗ, Ộ → O
- [ ] Ứ, Ừ, Ử, Ữ, Ự → U
- [ ] Ớ, Ờ, Ở, Ỡ, Ợ → O

## 3. Number Reduction

### 3.1 Basic Reduction

- [ ] Giảm số về 1 chữ số (1-9)
- [ ] Xử lý double digits (10, 12, 15...)
- [ ] Xử lý triple digits trở lên
- [ ] Không giảm Master Numbers (11, 22, 33)

### 3.2 Master Numbers

- [ ] 11 là Master Number (tránh giảm thành 2)
- [ ] 22 là Master Number (tránh giảm thành 4)
- [ ] 33 là Master Number (tránh giảm thành 6)
- [ ] Lưu secondary meaning cho Master Numbers

### 3.3 Reduction Logic

- [ ] Cộng các chữ số cho đến khi < 10
- [ ] Trừ khi gặp Master Number
- [ ] Maximum iterations để tránh infinite loop
- [ ] Return cả giá trị và trạng thái isMaster

## 4. Number Calculations

### 4.1 Life Path Number

- [ ] Sử dụng đầy đủ ngày sinh (DD/MM/YYYY)
- [ ] Cộng Year + Month + Day
- [ ] Giảm về single digit hoặc Master Number
- [ ] Xử lý Master Numbers cho Life Path

### 4.2 Expression Number

- [ ] Tính tất cả các chữ cái trong tên đầy đủ
- [ ] Sử dụng hệ thống đã chọn (Pythagorean/Chaldean)
- [ ] Giảm về single digit hoặc Master Number
- [ ] Lưu letter values để debug

### 4.3 Soul Urge Number

- [ ] Chỉ tính nguyên âm (A, E, I, O, U, Y)
- [ ] Sử dụng Pythagorean values
- [ ] Giảm về single digit hoặc Master Number
- [ ] Y được tính là nguyên âm trong một số trường hợp

### 4.4 Personality Number

- [ ] Chỉ tính phụ âm trong tên
- [ ] Sử dụng Pythagorean values
- [ ] Giảm về single digit hoặc Master Number
- [ ] Không tính nguyên âm

### 4.5 Birthday Number

- [ ] Sử dụng ngày sinh (DD)
- [ ] Giữ nguyên nếu là Master Number (11, 22)
- [ ] Giảm nếu > 9 và không phải Master

## 5. Life Cycles

### 5.1 Pinnacle Numbers

- [ ] First Pinnacle = Day + Month (reduced)
- [ ] Second Pinnacle = Day + Year (reduced)
- [ ] Third Pinnacle = First + Second (reduced)
- [ ] Fourth Pinnacle = Month + Year (reduced)
- [ ] Tính độ dài mỗi pinnacle

### 5.2 Challenge Numbers

- [ ] First Challenge = |Month - Day|
- [ ] Second Challenge = |Year - Day|
- [ ] Third Challenge = |Year - Month|
- [ ] Fourth Challenge = |Second - First|
- [ ] Reduce all challenges

### 5.3 Life Cycles

- [ ] First Cycle = Từ sinh đến tuổi ~36-40
- [ ] Second Cycle = Từ tuổi ~36-40 đến ~66-72
- [ ] Third Cycle = Từ tuổi ~66-72 trở đi
- [ ] Cycle number = Tổng các số trong giai đoạn

## 6. Name Analysis

### 6.1 Name Parsing

- [ ] Tách first name, middle names, last name
- [ ] Normalize tên (loại bỏ dấu, viết hoa)
- [ ] Loại bỏ spaces và special characters
- [ ] Xử lý tên có hyphen/dash

### 6.2 Vowel Analysis

- [ ] Xác định nguyên âm (A, E, I, O, U, Y)
- [ ] Tính tổng giá trị nguyên âm
- [ ] Giảm về single digit
- [ ] Lưu vowel letters

### 6.3 Consonant Analysis

- [ ] Xác định phụ âm
- [ ] Tính tổng giá trị phụ âm
- [ ] Giảm về single digit
- [ ] Lưu consonant letters

## 7. Number Meanings

### 7.1 Core Numbers (1-9)

- [ ] 1: Leadership, independence, innovation
- [ ] 2: Cooperation, diplomacy, partnership
- [ ] 3: Expression, creativity, communication
- [ ] 4: Stability, practicality, foundation
- [ ] 5: Freedom, change, adventure
- [ ] 6: Responsibility, harmony, nurturing
- [ ] 7: Analysis, spirituality, introspection
- [ ] 8: Authority, material success, power
- [ ] 9: Humanitarianism, completion, wisdom

### 7.2 Master Numbers (11, 22, 33)

- [ ] 11: Intuition, spiritual insight, illumination
- [ ] 22: Master builder, big dreams, practicality
- [ ] 33: Master teacher, compassion, selfless service

### 7.3 Compatibility

- [ ] Numbers tương thích với nhau
- [ ] Số nào hợp với số nào
- [ ] Số nào xung đột với nhau
- [ ] Recommendations cho mỗi số

## 8. API Development

### 8.1 RESTful Endpoints

- [ ] POST /charts - Tạo chart mới
- [ ] GET /charts/:id - Lấy chart
- [ ] GET /charts/user/:userId - Danh sách charts
- [ ] PUT /charts/:id - Cập nhật chart
- [ ] DELETE /charts/:id - Xóa chart
- [ ] GET /charts/:id/life-path - Life Path analysis
- [ ] GET /charts/:id/expression - Expression analysis
- [ ] GET /charts/:id/soul-urge - Soul Urge analysis
- [ ] GET /charts/:id/personality - Personality analysis
- [ ] GET /charts/:id/cycles - Life cycles
- [ ] GET /numbers/:number/meaning - Number meaning
- [ ] POST /compatibility - Check compatibility

### 8.2 Request/Response

- [ ] JSON format
- [ ] Request validation
- [ ] Consistent error format
- [ ] Response envelope
- [ ] Pagination cho list endpoints
- [ ] Cache-Control headers

### 8.3 Authentication

- [ ] API key authentication
- [ ] JWT token validation
- [ ] Rate limiting
- [ ] User ownership validation

## 9. Database Design

### 9.1 Schema

- [ ] Bảng numerology_charts
- [ ] Bảng name_analyses
- [ ] Bảng personal_years
- [ ] Bảng compatibility
- [ ] UUID primary keys
- [ ] Foreign keys

### 9.2 Indexes

- [ ] Index trên user_id
- [ ] Index trên birth_date
- [ ] Index trên life_path_number
- [ ] Index trên expression_number
- [ ] Composite indexes

### 9.3 Data Integrity

- [ ] NOT NULL constraints
- [ ] UNIQUE constraints
- [ ] CHECK constraints
- [ ] Default values

## 10. Caching

### 10.1 Cache Keys

- [ ] Chart data cache
- [ ] Name calculation cache
- [ ] Life Path cache
- [ ] Meaning cache

### 10.2 TTL Settings

- [ ] Chart data: 24 hours
- [ ] Name calculations: 7 days
- [ ] Life Path: 30 days
- [ ] Meanings: 30 days (static)

### 10.3 Cache Invalidation

- [ ] Invalidate on chart update
- [ ] Invalidate on chart delete
- [ ] Batch invalidation

## 11. Error Handling

### 11.1 Error Types

- [ ] ValidationError (400)
- [ ] InvalidNameError (400)
- [ ] InvalidBirthDateError (400)
- [ ] ChartNotFoundError (404)
- [ ] UnauthorizedError (403)
- [ ] InternalServerError (500)

### 11.2 Error Response

- [ ] Consistent error schema
- [ ] Error codes
- [ ] Error messages
- [ ] Error details
- [ ] Request ID

## 12. Testing

### 12.1 Unit Tests

- [ ] Pythagorean calculation tests
- [ ] Chaldean calculation tests
- [ ] Master number preservation tests
- [ ] Number reduction tests
- [ ] Life Path calculation tests
- [ ] Soul Urge calculation tests
- [ ] Name parsing tests
- [ ] Diacritics handling tests

### 12.2 Integration Tests

- [ ] API endpoint tests
- [ ] Database integration tests
- [ ] Cache integration tests

### 12.3 Test Coverage

- [ ] Overall coverage > 80%
- [ ] Critical paths > 90%
- [ ] Edge cases covered

## 13. Security

### 13.1 Input Security

- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] Input length limits
- [ ] Character validation

### 13.2 Data Security

- [ ] HTTPS only
- [ ] Data privacy
- [ ] Audit logging

### 13.3 API Security

- [ ] Rate limiting
- [ ] API key validation
- [ ] Request signing

## 14. Performance

### 14.1 Response Time

- [ ] P95 < 200ms cho read operations
- [ ] P95 < 1s cho write operations
- [ ] Database optimization
- [ ] Connection pooling

### 14.2 Caching

- [ ] Memory cache (LRU)
- [ ] Redis cache
- [ ] Cache warming
- [ ] Cache hit rate monitoring

## 15. Documentation

### 15.1 Code Documentation

- [ ] JSDoc/TSDoc comments
- [ ] Complex logic explained
- [ ] Constant values documented

### 15.2 API Documentation

- [ ] OpenAPI/Swagger spec
- [ ] Request/Response examples
- [ ] Error codes documented

### 15.3 Number Meanings

- [ ] Complete meanings for 1-9
- [ ] Complete meanings for 11, 22, 33
- [ ] Compatibility guide
- [ ] Career suggestions
