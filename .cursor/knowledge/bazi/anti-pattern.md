# Bazi Anti-Patterns - Các Mẫu Thiết Kế Cần Tránh

## Giới thiệu

Tài liệu này liệt kê các anti-patterns phổ biến trong việc phát triển hệ thống Bazi. Mỗi anti-pattern được mô tả chi tiết với ví dụ, hậu quả, và giải pháp thay thế. Việc nhận diện và tránh các anti-patterns này giúp development teams tiết kiệm thời gian, giảm bugs, và xây dựng hệ thống chất lượng cao hơn.

## Anti-Patterns về Tính Toán

### 1. Hard-code Lunar Calendar Rules

**Mô tả**: Việc hard-code các quy tắc chuyển đổi Âm Lịch thay vì sử dụng thư viện hoặc thuật toán động.

**Ví dụ xấu**: Code sử dụng switch statement để map các ngày cố định sang Âm Lịch hoặc sử dụng bảng lookup với data cứng.

```typescript
// ❌ ANTI-PATTERN: Hard-coded lunar dates
const LUNAR_DATES = {
  '2024-01-01': { lunarYear: 2023, lunarMonth: 12, lunarDay: 20 },
  '2024-01-15': { lunarYear: 2023, lunarMonth: 12, lunarDay: 4 },
  // ... hàng trăm dòng hard-coded data
};
```

**Hậu quả**: Data không đầy đủ, không chính xác cho các năm ngoài range đã defined. Không xử lý được năm nhuận, tháng nhuận. Rất khó maintain và update.

**Giải pháp**: Sử dụng thư viện chuyên dụng như `lunar-calendar-js` hoặc implement thuật toán dựa trên astronomical calculations. Nếu cần custom implementation, xây dựng data structure cho phép dynamic updates và validation.

### 2. Ignoring Timezone Handling

**Mô tả**: Bỏ qua múi giờ khi xử lý giờ sinh, dẫn đến tính toán sai thiên can của giờ.

**Ví dụ xấu**: Code lưu và xử lý giờ sinh mà không consider timezone, giả định tất cả users ở cùng một timezone.

```typescript
// ❌ ANTI-PATTERN: Ignoring timezone
function calculateHourStem(hour: number): string {
  // Giả định giờ được nhập theo local time của server
  return HOUR_STEMS[(hour - 1) % 10];
}
```

**Hậu quả**: Thiên can của giờ bị sai cho users ở các timezone khác nhau. Giờ sinh 23:00 có thể bị tính sai nếu user ở timezone UTC+7. User ở Việt Nam sinh lúc 23:30 có thể bị tính thuộc can khác với thực tế.

**Giải pháp**: Luôn yêu cầu timezone khi nhập giờ sinh. Store tất cả thời gian theo UTC và convert khi hiển thị. Sử dụng thư viện như `luxon` hoặc `date-fns-tz` để handle timezone conversions một cách chính xác.

### 3. Oversimplified Element Calculations

**Mô tả**: Tính ngũ hành quá đơn giản, chỉ dựa vào can hoặc chi mà bỏ qua các yếu tố khác.

**Ví dụ xấu**: Code chỉ count số lượng mỗi ngũ hành mà không consider trọng số, vị trí, và các tương tác phức tạp.

```typescript
// ❌ ANTI-PATTERN: Too simple element calculation
function calculateElements(baZi: BaZiReading): Elements {
  return {
    metal: countCan(baZi, ['canh', 'tân']) + countChi(baZi, ['thân', 'dậu']),
    wood: countCan(baZi, ['giáp', 'ất']) + countChi(baZi, ['mão', 'dần']),
    // ... chỉ count đơn giản
  };
}
```

**Hậu quả**: Kết quả thiếu chính xác vì không reflect được các yếu tố như ngũ hành của thập thần, cục diện, hay các tương tác tương sinh tương khắc. Đánh giá ngũ hành vượng/thiếu không chính xác.

**Giải pháp**: Implement full calculation bao gồm: ngũ hành của tất cả 8 chữ, trọng số theo vị trí (năm, tháng, ngày, giờ có trọng số khác nhau), các yếu tố Hóa, và cục diện. Tham khảo các tài liệu chuyên sâu về phép tính ngũ hành.

## Anti-Patterns về Data Management

### 4. Storing BaZi Data as Plain Text

**Mô tả**: Lưu trữ thông tin Bazi trong text fields thay vì structured data types.

**Ví dụ xấu**: Lưu trữ toàn bộ lá số như một string trong database.

```sql
-- ❌ ANTI-PATTERN: Plain text storage
CREATE TABLE baZi_readings (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  reading_text TEXT, -- "Năm Giáp Tý, Tháng Bính Dần, Ngày Đinh Mão, Giờ Mậu Tỵ"
  interpretation TEXT
);
```

**Hậu quả**: Không thể query hoặc filter dựa trên các thành phần của lá số. Không thể thực hiện calculations dựa trên stored data. Rất khó update hoặc modify individual components. Performance kém khi cần truy vấn trên dữ liệu lớn.

**Giải pháp**: Sử dụng structured columns hoặc separate tables cho từng component: year_can, year_chi, month_can, month_chi, day_can, day_chi, hour_can, hour_chi. Các trường này nên là enum types hoặc foreign keys đến lookup tables.

### 5. No Data Validation on Birth Information

**Mô tả**: Không validate birth_date và birth_time trước khi lưu hoặc tính toán.

**Ví dụ xấu**: Code nhận birth_date string và immediately pass vào calculation function mà không validate.

```typescript
// ❌ ANTI-PATTERN: No validation
async function createBaZiReading(userId: string, birthDate: string, birthTime: string) {
  const lunarDate = convertToLunar(birthDate, birthTime); // No validation!
  const reading = calculateBaZi(lunarDate);
  await db.save(reading);
}
```

**Hậu quả**: Invalid data có thể được lưu vào database. Calculations có thể throw exceptions hoặc produce incorrect results với malformed inputs. Khó debug khi có issues về data quality.

**Giải pháp**: Implement comprehensive validation: date format, range check (1900-2100), time format, reasonable birth_time validation. Return clear error messages cho invalid inputs. Log validation failures để track patterns và improve UX.

### 6. No Audit Trail for BaZi Calculations

**Mô tả**: Không lưu lại lịch sử các lần tính toán và thay đổi lá số.

**Ví dụ xấu**: User update birth_date và old reading bị overwrite mà không có backup.

```typescript
// ❌ ANTI-PATTERN: Overwriting without history
async function updateBirthDate(userId: string, newDate: string) {
  const user = await db.users.find(userId);
  user.birth_date = newDate; // Mất dữ liệu cũ!
  await db.save(user);
  await recalculateBaZi(userId);
}
```

**Hậu quả**: Không thể trace lại các phân tích trước đó. Không có way để so sánh readings mới và cũ. Compliance issues nếu cần audit. Khó debug khi user reports inconsistent results.

**Giải pháp**: Implement soft delete hoặc version tracking cho readings. Audit logs cho tất cả changes đến user birth information. Separate tables cho user profile và calculated readings để allow multiple readings per user. Timestamp all records và maintain referential integrity.

## Anti-Patterns về API Design

### 7. Exposing Raw Internal Data Structures

**Mô tả**: API trả về raw internal data structures thay vì business-friendly responses.

**Ví dụ xấu**: API trả về database entities trực tiếp với internal field names và format.

```json
// ❌ ANTI-PATTERN: Raw internal data
{
  "id": "uuid-here",
  "y_can": "giáp",
  "y_chi": "tý",
  "m_can": "bính",
  "m_chi": "dần",
  "ng_can": "đinh",
  "ng_chi": "mão",
  "g_can": "mậu",
  "g_chi": "tỵ",
  "created_at": "2024-01-15T10:30:00Z",
  "calc_version": 3
}
```

**Hậu quả**: API không intuitive cho clients. Breaking changes khi internal structures change. Clients phải understand internal domain model. Poor developer experience.

**Giải pháp**: API responses nên use business-friendly names và structure. DTOs (Data Transfer Objects) được designed cho API consumption. Documentation xác định rõ contract giữa client và server. Versioning được implemented để allow gradual API evolution.

### 8. Synchronous Heavy Calculations

**Mô tả**: Thực hiện các tính toán nặng (AI analysis, complex readings) synchronously trong API request.

**Ví dụ xấu**: Endpoint gọi AI model để generate interpretation và wait synchronously.

```typescript
// ❌ ANTI-PATTERN: Synchronous heavy computation
app.post('/api/baZi/:id/interpret', async (req, res) => {
  const reading = await getReading(req.params.id);
  const interpretation = await generateAIInterpretation(reading); // Có thể mất 5-10 giây!
  res.json({ interpretation });
});
```

**Hậu quả**: API timeouts khi calculations exceed timeout limits. Poor user experience với waiting times. Server resources bị blocked trong thời gian dài. Cannot scale horizontally due to blocking operations.

**Giải pháp**: Sử dụng async processing với message queues. Webhook hoặc WebSocket để notify clients khi done. Progress indicators cho long-running tasks. Background job processing với proper error handling và retries.

### 9. Missing Rate Limiting cho Expensive Operations

**Mô tả**: Không có rate limiting cho các endpoints tính toán nặng.

**Ví dụ xấu**: Endpoint phân tích chi tiết không có giới hạn số lần gọi.

```typescript
// ❌ ANTI-PATTERN: No rate limiting
app.post('/api/baZi/detailed-analysis', async (req, res) => {
  // Không check số lần user đã gọi
  const analysis = await performExpensiveAnalysis(req.body);
  res.json(analysis);
});
```

**Hậu quả**: Resource exhaustion từ abuse hoặc accidental loops. Cost unpredictability từ excessive usage. Poor experience cho legitimate users khi system overloaded. Security vulnerabilities.

**Giải pháp**: Implement rate limiting với appropriate limits per tier. Different limits cho different operations. Return 429 Too Many Requests với Retry-After header. Usage tracking cho analytics và billing.

## Anti-Patterns về Business Logic

### 10. Deterministic Predictions

**Mô tả**: Trình bày kết quả Bazi như deterministic predictions thay vì probabilistic guidance.

**Ví dụ xấu**: Language trong readings sử dụng "bạn SẼ gặp may mắn" thay vì "có khả năng cao bạn sẽ gặp may mắn".

```typescript
// ❌ ANTI-PATTERN: Deterministic language
const interpretation = "Năm nay bạn SẼ gặp một cơ hội lớn trong công việc. Bạn NHẤT ĐỊNH sẽ thành công nếu theo đuổi con đường này.";
```

**Hậu quả**: Misleading users về độ chính xác của readings. Ethical concerns về giving false confidence. Users có thể make poor decisions dựa trên overconfident predictions. Reputation damage khi predictions không come true.

**Giải pháp**: Sử dụng probabilistic language: "có khả năng", "xu hướng", "tiềm năng". Provide confidence levels hoặc uncertainty indicators. Include disclaimers về limitations của predictions. Expert review cho sensitive predictions.

### 11. Ignoring User Context trong Recommendations

**Mô tả**: Đưa ra recommendations mà không consider user context và preferences.

**Ví dụ xấu**: Recommend hướng nhà theo Bazi mà không hỏi về budget, location preferences, hoặc current housing situation.

```typescript
// ❌ ANTI-PATTERN: Context-free recommendations
function recommendDirection(baZi: BaZiReading) {
  // Chỉ dựa vào Bazi, không consider user constraints
  return { direction: 'Đông', reason: 'Phù hợp với mệnh của bạn' };
}
```

**Hậu quả**: Recommendations không actionable cho users. Frustration khi recommendations không feasible. Trust erosion khi recommendations consistently impractical.

**Giải phải**: Gather user context trước recommendations. Provide multiple options với trade-offs. Filter recommendations by feasibility. Allow users to set constraints và preferences.

### 12. One-Size-Fits-All Interpretation

**Mô tả**: Sử dụng cùng một interpretation template cho tất cả users.

**Ví dụ xấu**: Tất cả users với cùng cục diện nhận được identical text.

```typescript
// ❌ ANTI-PATTERN: Generic interpretations
const templates = {
  'công-thương-nghiệp': 'Bạn phù hợp với việc kinh doanh...'
};

function interpret(baZi: BaZiReading) {
  return templates[baZi.pattern]; // Cùng text cho mọi người
}
```

**Hậu quả**: Poor user experience với generic content. Users feel like they're getting "canned" responses. Missed opportunity để personalize và add value. Differentiation lost vs competitors.

**Giải pháp**: Dynamic interpretation generation với user-specific details. Combination của templates và dynamic content. ML-powered personalization based on user profile và interactions. User feedback được used để improve personalization.

## Anti-Patterns về Security

### 13. Storing Sensitive Birth Data in Plain Text

**Mô tả**: Lưu trữ thông tin nhạy cảm (birth data, personal readings) mà không mã hóa.

**Ví dụ xấu**: Birth date và time được lưu trong plain columns không encrypted.

```sql
-- ❌ ANTI-PATTERN: Unencrypted sensitive data
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR,
  birth_date DATE, -- Plain text!
  birth_time TIME, -- Plain text!
  baZi_data JSONB -- Có thể chứa sensitive info
);
```

**Hậu quả**: Data breach exposure nếu database compromised. Privacy violations nếu data accessed unauthorized. Compliance failures với GDPR và data protection regulations.

**Giải pháp**: Encrypt sensitive fields at rest. Encryption at application level cho PII. Key management với proper rotation. Access controls giới hạn ai có thể access encrypted data. Audit logging cho all access.

### 14. No Input Sanitization cho User-Provided Content

**Mô tả**: Không sanitize user inputs trước khi store hoặc display.

**Ví dụ xấu**: User có thể input XSS payloads trong name hoặc notes fields.

```typescript
// ❌ ANTI-PATTERN: No sanitization
app.post('/api/profile', (req, res) => {
  const { name, notes } = req.body;
  db.save({ name, notes }); // Có thể chứa malicious content!
  res.send('Saved');
});
```

**Hậu quả**: XSS vulnerabilities nếu content được displayed. SQL injection nếu inputs được used trong queries. Data corruption từ malformed inputs.

**Giải pháp**: Input validation ở both client và server. Output encoding khi displaying user content. Parameterized queries cho database operations. Content Security Policy headers. Regular security audits.

## Anti-Patterns về Performance

### 15. N+1 Queries khi Loading Readings

**Mô tả**: Load readings gây ra N+1 query problem.

**Ví dụ xấu**: Fetch user list rồi query database cho mỗi user để get reading.

```typescript
// ❌ ANTI-PATTERN: N+1 queries
async function getUsersWithReadings() {
  const users = await db.query('SELECT * FROM users');
  return Promise.all(users.map(async (user) => {
    const reading = await db.query('SELECT * FROM readings WHERE user_id = ?', user.id);
    return { ...user, reading };
  }));
}
```

**Hậu quả**: Performance degradation exponential với number of users. Database connection exhaustion. Timeout errors under load.

**Giải pháp**: JOIN queries hoặc batch queries. Eager loading với ORM. Database indexing trên foreign keys. Pagination cho large result sets.

### 16. No Pagination cho Large Result Sets

**Mô tả**: API trả về toàn bộ results mà không pagination.

**Ví dụ xấu**: Endpoint lấy tất cả readings của user mà không limit.

```typescript
// ❌ ANTI-PATTERN: No pagination
app.get('/api/users/:id/readings', async (req, res) => {
  const readings = await db.query('SELECT * FROM readings WHERE user_id = ?', req.params.id);
  res.json(readings); // Có thể trả về hàng ngàn records!
});
```

**Hậu quả**: Memory exhaustion với large datasets. Timeout errors. Poor performance trên mobile devices. API abuse potential.

**Giải pháp**: Implement cursor-based hoặc offset-based pagination. Default page size và maximum limits. Return pagination metadata (total count, has more). Cache paginated results.

### 17. Synchronous External API Calls

**Mô tả**: Gọi external APIs (AI services, payment gateways) synchronously.

**Ví dụ xấu**: API call đến OpenAI synchronous trong request handler.

```typescript
// ❌ ANTI-PATTERN: Synchronous external calls
app.post('/api/analyze', async (req, res) => {
  const result = await openai.complete(req.body.prompt); // Synchronous!
  res.json({ result });
});
```

**Hậu quả**: Request timeouts nếu external service slow. Thread/connection pool exhaustion. Cascading failures khi external service down.

**Giải pháp**: Async calls với webhooks hoặc polling. Circuit breaker pattern. Retry mechanisms với exponential backoff. Fallback mechanisms khi external services unavailable.

## Kết luận

Việc nhận diện và tránh các anti-patterns này là bước quan trọng để xây dựng hệ thống Bazi chất lượng cao. Teams nên thực hiện code reviews đặc biệt chú ý đến các areas này và implement automated checks để prevent regressions. Regular architecture reviews giúp identify potential issues trước khi chúng trở thành production problems.
