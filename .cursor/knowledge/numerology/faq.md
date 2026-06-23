# FAQ - Hỏi Đáp về Hệ Thống Numerology

## 1. Câu Hỏi Chung

### Q1: Numerology là gì?

**A:** Numerology (Thần Số Học) là hệ thống nghiên cứu mối liên hệ giữa các con số và sự kiện trong cuộc sống con người. Numerology tin rằng các con số có năng lượng và ý nghĩa đặc biệt, ảnh hưởng đến tính cách, vận mệnh và cuộc sống của mỗi người.

**Các hệ thống Numerology phổ biến:**

| Hệ thống | Mô tả | Số lượng chữ cái |
|----------|--------|------------------|
| **Pythagorean** | Phổ biến nhất, từ Hy Lạp | 1-9 (J=1, S=1) |
| **Chaldean** | Cổ xưa từ Babylon | 1-8 (không có 9) |
| **Kabbalah** | Hebrew mysticism | 1-11 (chỉ tên) |

**Các con số chính trong Numerology:**
- **Life Path Number** (Đường đời): Số quan trọng nhất
- **Expression Number** (Biểu đạt): Tài năng và khả năng
- **Soul Urge Number** (Số tâm hồn): Mong muốn bên trong
- **Personality Number** (Số nhân cách): Cách người khác nhìn bạn
- **Birthday Number** (Số ngày sinh): Điểm nhấn đặc biệt

### Q2: Sự khác nhau giữa Pythagorean và Chaldean?

**A:** Hai hệ thống có cách gán giá trị chữ cái khác nhau:

**Pythagorean System:**
```
A=1, B=2, C=3, D=4, E=5, F=6, G=7, H=8, I=9
J=1, K=2, L=3, M=4, N=5, O=6, P=7, Q=8, R=9
S=1, T=2, U=3, V=4, W=5, X=6, Y=7, Z=8
```
- Bảng chữ cái theo thứ tự alphabet
- J, S, Y quay về 1
- 1-9, quay vòng

**Chaldean System:**
```
A=1, B=2, C=3, D=4, E=5, U=6, O=7, F=8
I=9, Y=1, J=1, K=2, L=3, M=4, N=5, X=6
G=7, H=8, Z=8, P=8, Q=1, R=2, S=3, T=4
V=6, W=6, D=4
```
- Bảng chữ cái theo "âm thanh"
- Không có số 9 trong bảng (I=9 đứng riêng)
- P, Z cùng = 8

**Ví dụ:** Tên "KATE"
- Pythagorean: K=2, A=1, T=2, E=5 = 10 → 1
- Chaldean: K=2, A=1, T=4, E=5 = 12 → 3

### Q3: Master Numbers là gì?

**A:** Master Numbers là các số 11, 22, và 33 - được coi là có năng lượng đặc biệt mạnh mẽ.

**Các Master Numbers:**

| Số | Tên | Ý nghĩa |
|----|------|----------|
| **11** | The Illuminator | Trực giác, tầm nhìn, ánh sáng tâm linh |
| **22** | The Master Builder | Xây dựng vĩ đại, thực tiễn, ambição |
| **33** | The Master Teacher | Phụng sự, yêu thương, giáo dục |

**Quy tắc quan trọng:**
- Master Numbers không được giảm xuống single digit
- 11 → 2 (secondary meaning)
- 22 → 4 (secondary meaning)
- 33 → 6 (secondary meaning)

**Ví dụ:** Nếu tên của bạn cộng lại = 22, bạn giữ nguyên là 22 (Master Builder), không giảm thành 4.

### Q4: Life Path Number là gì?

**A:** Life Path Number là số quan trọng nhất trong Numerology, được tính từ ngày sinh đầy đủ.

**Cách tính:**
```
Ví dụ: Ngày sinh 15/05/1990

1. Viết ngày sinh dạng số: 1 + 5 + 0 + 5 + 1 + 9 + 9 + 0
2. Cộng: 1 + 5 + 0 + 5 + 1 + 9 + 9 + 0 = 30
3. Giảm: 3 + 0 = 3
4. Life Path = 3

Nếu kết quả là 11, 22, hoặc 33 → Giữ nguyên (Master Number)
```

**Ý nghĩa các Life Path:**
- **1:** Người khởi đầu, lãnh đạo
- **2:** Người hòa giải, hợp tác
- **3:** Người sáng tạo, giao tiếp
- **4:** Người xây dựng, ổn định
- **5:** Người tự do, thay đổi
- **6:** Người nuôi dưỡng, trách nhiệm
- **7:** Người phân tích, tâm linh
- **8:** Người quyền lực, thành công
- **9:** Người nhân đạo, hoàn thành
- **11:** Người có tầm nhìn (Master)
- **22:** Người xây dựng vĩ đại (Master)
- **33:** Người thầy vĩ đại (Master)

## 2. Câu Hỏi Kỹ Thuật

### Q5: Làm thế nào để xử lý Vietnamese diacritics?

**A:** Vietnamese có nhiều dấu thanh cần được normalize trước khi tính Numerology:

**Quy tắc chuyển đổi:**

| Vietnamese | ASCII | Giá trị |
|------------|-------|---------|
| A, Á, À, Ả, Ã, Ạ | A | 1 |
| Ă, Ắ, Ằ, Ẳ, Ẵ, Ặ | A | 1 |
| Â, Ấ, Ầ, Ẩ, Ẫ, Ậ | A | 1 |
| E, É, È, Ẻ, Ẽ, Ẹ, Ề, Ể, Ễ, Ệ | E | 5 |
| I, Í, Ì, Ỉ, Ĩ, Ị | I | 9 |
| O, Ó, Ò, Ỏ, Õ, Ọ, Ố, Ồ, Ổ, Ỗ, Ộ, Ớ, Ờ, Ở, Ỡ, Ợ | O | 6 |
| U, Ú, Ù, Ủ, Ũ, Ụ, Ứ, Ừ, Ử, Ữ, Ự | U | 3 |
| Y, Ý, Ỳ, Ỷ, Ỹ, Ỵ | Y | 7 |

**Code xử lý:**
```typescript
const DIACRITIC_MAP: Record<string, string> = {
  'Ạ': 'A', 'ạ': 'a', 'Ả': 'A', 'ả': 'a', 'Ấ': 'A', 'ấ': 'a',
  'Ầ': 'A', 'ầ': 'a', 'Ẩ': 'A', 'ẩ': 'a', 'Ẫ': 'A', 'ẫ': 'a',
  'Ậ': 'A', 'ậ': 'a', 'Ắ': 'A', 'ắ': 'a', 'Ằ': 'A', 'ằ': 'a',
  // ... đầy đủ map
};

function normalizeName(name: string): string {
  return name.split('')
    .map(char => DIACRITIC_MAP[char] || char)
    .join('')
    .toUpperCase()
    .replace(/[^A-Z]/g, '');
}
```

### Q6: Cách tính Soul Urge Number?

**A:** Soul Urge (Heart's Desire) được tính từ các nguyên âm trong tên:

**Nguyên âm:** A, E, I, O, U, Y (trong một số trường hợp)

**Ví dụ:** Tên "KATE"
```
K = 2 (phụ âm, không tính)
A = 1 (nguyên âm)
T = 2 (phụ âm, không tính)
E = 5 (nguyên âm)

Soul Urge = 1 + 5 = 6
```

**Quy tắc về Y:**
- Y là nguyên âm khi: không có nguyên âm nào khác, hoặc Y ở cuối với âm tiết trọng âm
- Ví dụ: "LYNN" - Y là nguyên âm vì không có A, E, I, O, U

### Q7: Làm thế nào để tính Life Cycles?

**A:** Life Cycles (Chu kỳ sống) gồm 3 giai đoạn:

**1. First Cycle (Cycle đầu tiên):**
- Số = Tổng của Tháng + Ngày sinh
- Độ dài = Đến tuổi 27-36

**2. Second Cycle (Cycle thứ hai):**
- Số = Tổng của Năm sinh + Ngày sinh
- Độ dài = 27-36 năm tiếp theo

**3. Third Cycle (Cycle thứ ba):**
- Số = Tổng của Tháng + Năm sinh
- Độ dài = Phần còn lại của cuộc đời

**Ví dụ:** Sinh ngày 15/05/1990
```
First: Tháng (5) + Ngày (15) = 5 + 15 = 20 → 2 + 0 = 2
Second: Năm (1990) + Ngày (15) = 1+9+9+0 + 15 = 34 → 3 + 4 = 7
Third: Tháng (5) + Năm (1990) = 5 + 1+9+9+0 = 24 → 2 + 4 = 6
```

### Q8: Pinnacle Numbers là gì?

**A:** Pinnacle Numbers (Đỉnh cao) cho biết các giai đoạn thành công trong cuộc đời:

**4 Pinnacle Numbers:**
- **First Pinnacle** = Day + Month (Số đỉnh đầu tiên)
- **Second Pinnacle** = Day + Year (Số đỉnh thứ hai)
- **Third Pinnacle** = First + Second (Số đỉnh thứ ba)
- **Fourth Pinnacle** = Month + Year (Số đỉnh thứ tư)

**Độ dài mỗi đỉnh:**
- First Pinnacle: Từ sinh đến tuổi 27-36
- Second Pinnacle: Từ tuổi 27-36 đến 36-45
- Third Pinnacle: Từ tuổi 36-45 đến tuổi 60-67
- Fourth Pinnacle: Từ tuổi 60-67 trở đi

## 3. Câu Hỏi Triển Khai

### Q9: Nên sử dụng database nào?

**A:** PostgreSQL là lựa chọn tốt:

**Schema thiết kế:**
```sql
CREATE TABLE numerology_charts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  full_name VARCHAR(200) NOT NULL,
  birth_date DATE NOT NULL,
  
  life_path_number INT NOT NULL,
  expression_number INT NOT NULL,
  soul_urge_number INT NOT NULL,
  personality_number INT NOT NULL,
  birthday_number INT NOT NULL,
  
  name_analysis JSONB,
  life_cycles JSONB,
  
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_numerology_user ON numerology_charts(user_id);
CREATE INDEX idx_numerology_lifepath ON numerology_charts(life_path_number);
```

### Q10: Performance optimization?

**A:** Các strategies:

**1. Caching:**
```typescript
// Cache name calculations
const nameCache = new LRUCache({
  max: 10000,
  ttl: 7 * 24 * 60 * 60 * 1000 // 7 days
});

// Cache Life Path
const lifePathCache = new RedisCache({
  prefix: 'numerology:lifepath:',
  ttl: 30 * 24 * 60 * 60 // 30 days
});
```

**2. Pre-computation:**
```typescript
// Pre-compute lookup tables
const LETTER_VALUES = Object.freeze({ ... });

// Pre-compute meanings
const NUMBER_MEANINGS = Object.freeze({ ... });
```

**3. Batch Processing:**
```typescript
async function calculateBatch(inputs: Input[]): Promise<Result[]> {
  // Process in parallel with limit
  return Promise.all(inputs.map(i => calculate(i)));
}
```

## 4. Câu Hỏi Về Độ Chính Xác

### Q11: Độ chính xác của Numerology?

**A:** Độ chính xác phụ thuộc vào:

| Yếu tố | Mức độ ảnh hưởng |
|--------|-------------------|
| Tên đầy đủ (birth name) | **Rất cao** |
| Ngày sinh chính xác | **Cao** |
| Hệ thống Numerology | **Trung bình** |
| Interpretation | **Thấp** |

**Độ chính xác ước tính:**
- Số tính toán: ~95% (phụ thuộc thuật toán)
- Interpretation: ~60-80% (subjective)

### Q12: Tại sao cùng ngày sinh nhưng số khác nhau?

**A:** Có thể do:

1. **Khác hệ thống:** Pythagorean vs Chaldean cho ra số khác nhau
2. **Khác tên:** Tên đầy đủ trên giấy khai sinh vs tên thường dùng
3. **Khác cách tính:** Một số calculator giảm Master Numbers
4. **Tên Vietnamese:** Cách xử lý dấu khác nhau

### Q13: Nên tin Numerology ở mức nào?

**A:** Numerology nên được xem là **tham khảo**:

**Nên dùng để:**
- Hiểu bản thân (điểm mạnh/yếu)
- Xác định hướng phát triển
- Tham khảo thời điểm tốt cho việc quan trọng
- Hiểu mối quan hệ với người khác

**Không nên dùng để:**
- Quyết định hôn nhân hoàn toàn
- Chọn nghề nghiệp duy nhất
- Đầu tư tài chính lớn dựa hoàn toàn
- Thay thế tư vấn chuyên môn

## 5. Câu Hỏi API

### Q14: Rate limit?

**A:** Rate limits theo plan:

| Plan | Requests/phút | Requests/ngày |
|------|--------------|--------------|
| Free | 10 | 100 |
| Basic | 60 | 1,000 |
| Pro | 300 | 10,000 |
| Enterprise | Unlimited | Unlimited |

### Q15: Integration?

**A:** REST API integration:

```typescript
// Create chart
const response = await fetch('/api/v1/numerology/charts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
  },
  body: JSON.stringify({
    fullName: 'Nguyen Van A',
    birthDate: '1990-05-15',
    system: 'pythagorean'
  })
});

const { data: chart } = await response.json();
```

### Q16: Error codes?

**A:** Error codes:

| Code | HTTP Status | Mô tả |
|------|------------|-------|
| VALIDATION_ERROR | 400 | Dữ liệu đầu vào không hợp lệ |
| INVALID_NAME | 400 | Tên không hợp lệ |
| INVALID_BIRTH_DATE | 400 | Ngày sinh không hợp lệ |
| CHART_NOT_FOUND | 404 | Không tìm thấy chart |
| RATE_LIMIT_EXCEEDED | 429 | Quá rate limit |
| INTERNAL_ERROR | 500 | Lỗi nội bộ |

## 6. Câu Hỏi Về Compatibility

### Q17: Làm thế nào để kiểm tra tương thích?

**A:** Kiểm tra compatibility dựa trên các con số:

**Compatibility matrix:**
```
1 ↔ 1, 3, 5, 7, 9    (tương thích cao)
2 ↔ 2, 4, 6, 8        (tương thích cao)
3 ↔ 1, 3, 5, 9        (tương thích cao)
4 ↔ 2, 4, 6, 8        (tương thích cao)
5 ↔ 1, 3, 5, 7, 9    (tương thích cao)
6 ↔ 2, 4, 6, 8, 9    (tương thích cao)
7 ↔ 1, 5, 7, 9        (tương thích cao)
8 ↔ 2, 4, 6, 8        (tương thích cao)
9 ↔ 1, 3, 5, 6, 7, 9 (tương thích cao)
```

**Master Numbers compatibility:**
- 11 tương thích với tất cả
- 22 tương thích với 2, 4, 6, 8, 22
- 33 tương thích với 3, 6, 9, 33

### Q18: Nên dùng số nào để kiểm tra compatibility?

**A:** Nên kiểm tra nhiều số:

1. **Life Path vs Life Path:** So sánh đường đời
2. **Expression vs Expression:** So sánh tài năng
3. **Soul Urge vs Soul Urge:** So sánh tâm hồn
4. **Birthday vs Birthday:** So sánh ngày sinh

**Độ quan trọng:**
1. Life Path (quan trọng nhất)
2. Expression
3. Soul Urge
4. Birthday (ít quan trọng nhất)

**Ví dụ:** Life Path 5 và 3 → Tương thích tốt (cả hai đều thích tự do, sáng tạo)
