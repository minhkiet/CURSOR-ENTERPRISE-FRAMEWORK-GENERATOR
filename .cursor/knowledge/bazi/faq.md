# FAQ - Hỏi Đáp về Hệ Thống Bazi

## 1. Câu Hỏi Chung

### Q1: Bazi là gì và nó khác gì so với Tử Vi?

**A:** Bazi (八字 - Bát Tự) là hệ thống bói toán Trung Hoa dựa trên thời điểm sinh, sử dụng 4 cột (Tứ Trụ) gồm:
- Năm Trụ (年柱)
- Tháng Trụ (月柱)
- Ngày Trụ (日柱)
- Giờ Trụ (时柱)

Mỗi cột gồm 1 Thiên Can và 1 Địa Chi, tạo thành 8 ký tự → "Bát Tự" (8字).

**Sự khác nhau với Tử Vi:**

| Tiêu chí | Bazi | Tử Vi |
|----------|------|-------|
| **Đơn vị phân tích** | Tứ Trụ (4 cột) | 12 cung, 12 đặc phẩm, sao |
| **Độ chính xác thời gian** | Cao (tính đến giờ) | Trung bình (tính đến ngày) |
| **Phương pháp** | Ngũ Hành, Can Chi | Sao, Cung, Lộc |
| **Ứng dụng** | Phân tích vận mệnh, tính cách | Bói toán chi tiết, hạn |

### Q2: Làm thế nào để tính Bazi chính xác?

**A:** Để tính Bazi chính xác, cần:

1. **Ngày sinh Dương lịch** chính xác (năm, tháng, ngày)
2. **Giờ sinh** chính xác (theo giờ Trung Quốc, mỗi giờ = 2 tiếng)
3. **Múi giờ** của nơi sinh
4. **Chuyển đổi sang Âm lịch** (cần thiết vì Bazi dùng âm lịch)

**Công thức cơ bản:**
```
Năm Trụ = Can của (Năm âm lịch + 6) % 10 + Chi của (Năm âm lịch + 8) % 12
```

**Ví dụ:** Sinh năm 1990-05-15 (Âm lịch: 1990-03-20)
- Năm Can: (1990 + 6) % 10 = 6 → Canh
- Năm Chi: (1990 + 8) % 12 = 10 → Ngọ
- Kết quả: **Canh Ngọ**

### Q3: Sự khác nhau giữa Giờ sinh Việt Nam và Giờ Trung Quốc?

**A:** Giờ trong Bazi sử dụng **Giờ Trung Quốc** (Chinese Hour), mỗi giờ = 2 tiếng Dương lịch:

| Giờ Bazi | Giờ Dương lịch | Tên |
|---------|----------------|-----|
| Tý | 23:00 - 00:59 | Midnight |
| Sửu | 01:00 - 02:59 | Ox |
| Dần | 03:00 - 04:59 | Tiger |
| Mão | 05:00 - 06:59 | Rabbit |
| Thìn | 07:00 - 08:59 | Dragon |
| Tỵ | 09:00 - 10:59 | Snake |
| Ngọ | 11:00 - 12:59 | Horse |
| Mùi | 13:00 - 14:59 | Goat |
| Thân | 15:00 - 16:59 | Monkey |
| Dậu | 17:00 - 18:59 | Rooster |
| Tuất | 19:00 - 20:59 | Dog |
| Hợi | 21:00 - 22:59 | Pig |

**Lưu ý:** Giờ Tý bắt đầu từ 23:00 ngày hôm trước!

### Q4: Nạp Âm là gì và nó quan trọng như thế nào?

**A:** Nạp Âm (納音) là hệ thống gán "âm thanh" cho mỗi cặp Can-Chi, đại diện cho vật chất/hiện tượng trong tự nhiên. Có 60 Nạp Âm (10 Thiên Can × 12 Địa Chi).

**Ví dụ:**
- **Hải Trung Kim** (海 中 金): Vàng dưới biển - Người sinh năm Giáp Tý hoặc Ất Tý
- **Sơn Hạ Hỏa** (山 下 火): Lửa dưới núi - Người sinh năm Mậu Tý hoặc Kỷ Tý

**Ý nghĩa:**
1. Bổ sung ý nghĩa cho năm sinh
2. Xác định tính cách bổ sung
3. Ảnh hưởng đến vận mệnh

## 2. Câu Hỏi Kỹ Thuật

### Q5: Làm thế nào để chuyển đổi Dương lịch sang Âm lịch?

**A:** Có 2 phương pháp:

**Phương pháp 1: Sử dụng thư viện Lunar Calendar**
```typescript
import { LunarDate } from 'lunar-calendar';

const result = LunarDate.toLunar(new Date(1990, 4, 15));
// result: { year: 1990, month: 3, day: 20 }
```

**Phương pháp 2: Tự implement thuật toán**
```typescript
function solarToLunar(date: Date): LunarDate {
  // Sử dụng Julian Day Number
  const jd = dateToJD(date);
  const lunar JD = jdToLunar(jd);
  return jdToLunarDate(lunarJD);
}
```

**Lưu ý:** Cần xử lý tháng nhuận (leap month) trong âm lịch.

### Q6: Công thức tính Ngày Trụ (Day Pillar) như thế nào?

**A:** Ngày Trụ là phức tạp nhất, cần sử dụng **Julian Day Number**:

```typescript
function calculateDayPillar(lunarDate: LunarDate): Pillar {
  // 1. Chuyển ngày sang Julian Day
  const jd = lunarToJD(lunarDate);
  
  // 2. Tính Can Index: (JD + 1) % 10
  const canIndex = (Math.floor(jd) + 1) % 10;
  
  // 3. Tính Chi Index: (JD + 1) % 12
  const chiIndex = (Math.floor(jd) + 1) % 12;
  
  return {
    can: CAN[canIndex],
    chi: CHI[chiIndex]
  };
}
```

**Ví dụ:** Ngày 15/05/2024
- JD = 2460456
- Can Index = (2460456 + 1) % 10 = 7 → Tân
- Chi Index = (2460456 + 1) % 12 = 1 → Sửu
- Kết quả: **Tân Sửu**

### Q7: Tại sao cần xác định giới tính để tính Cung Mệnh?

**A:** Cung Mệnh (命) được tính theo **Thập Tự Pháp** (十直法), khác nhau cho Nam và Nữ:

**Nam mệnh:**
| Ngày Can | Cung |
|---------|------|
| Giáp, Kỷ | Cấn |
| Ất, Canh | Ly |
| Bính, Tân | Khôn |
| Đinh, Nhâm | Khang |
| Mậu, Quý | Chấn |

**Nữ mệnh:**
| Ngày Can | Cung |
|---------|------|
| Giáp, Kỷ | Chấn |
| Ất, Canh | Khôn |
| Bính, Tân | Ly |
| Đinh, Nhâm | Cấn |
| Mậu, Quý | Khang |

**Ví dụ:** Nam sinh ngày Canh (Day Pillar = Canh)
→ Cung Mệnh = **Ly** (Lửa)

### Q8: Làm thế nào để tính Ngũ Hành tương sinh/tương khắc?

**A:** Ngũ Hành có 2 quy luật chính:

**Tương Sinh (相生):** A sinh B
```
Mộc → Hỏa → Thổ → Kim → Thủy → Mộc
```

**Tương Khắc (相克):** A khắc B
```
Mộc → Thổ → Thủy → Hỏa → Kim → Mộc
```

```typescript
function calculateElementBalance(pillars: Pillar[]): ElementBalance {
  const balance = { wood: 0, fire: 0, earth: 0, metal: 0, water: 0 };
  
  for (const pillar of pillars) {
    // Can cho Ngũ Hành chính
    balance[getCanElement(pillar.can)] += 2;
    
    // Chi cho Ngũ Hành chính
    balance[getChiElement(pillar.chi)] += 1;
    
    // Hidden Stems
    for (const hiddenCan of pillar.hiddenStems || []) {
      balance[getCanElement(hiddenCan)] += 0.5;
    }
  }
  
  return balance;
}
```

## 3. Câu Hỏi Triển Khai

### Q9: Nên sử dụng database nào cho hệ thống Bazi?

**A:** Khuyến nghị:

| Database | Ưu điểm | Phù hợp khi |
|---------|---------|------------|
| **PostgreSQL** | JSON support, Full-text search | Production, complex queries |
| **MongoDB** | Flexible schema, Easy scaling | Prototype, document storage |
| **Redis** | Fast caching, Session storage | Caching layer |

**Schema thiết kế:**
```sql
CREATE TABLE bazi_charts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  
  -- Birth info
  birth_date DATE NOT NULL,
  birth_time TIME NOT NULL,
  timezone VARCHAR(50) NOT NULL,
  
  -- Lunar date
  lunar_year INT NOT NULL,
  lunar_month INT NOT NULL,
  lunar_day INT NOT NULL,
  
  -- Tứ Trụ
  year_can VARCHAR(2), year_chi VARCHAR(2),
  month_can VARCHAR(2), month_chi VARCHAR(2),
  day_can VARCHAR(2), day_chi VARCHAR(2),
  hour_can VARCHAR(2), hour_chi VARCHAR(2),
  
  -- Metadata
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Q10: Làm thế nào để optimize performance cho Bazi calculation?

**A:** Các strategies:

**1. Caching:**
```typescript
// Cache kết quả lunar conversion
const lunarCache = new LRUCache<string, LunarDate>({
  max: 10000,
  ttl: 30 * 24 * 60 * 60 * 1000 // 30 days
});

// Cache kết quả Bazi calculation
const baziCache = new RedisCache({
  prefix: 'bazi:',
  ttl: 24 * 60 * 60 // 24 hours
});
```

**2. Batch Processing:**
```typescript
async function calculateBatch(inputs: BaziInput[]): Promise<BaziChart[]> {
  // Xử lý song song, giới hạn concurrency
  return Promise.all(
    inputs.map(input => calculateWithLock(input))
  );
}
```

**3. Database Optimization:**
```sql
-- Index cho các queries thường dùng
CREATE INDEX idx_bazi_user_date ON bazi_charts(user_id, created_at DESC);
CREATE INDEX idx_bazi_birth ON bazi_charts(birth_year, birth_month, birth_day);
```

**4. Pre-computation:**
```typescript
// Pre-compute Can-Chi table cho performance
const CAN_CHI_TABLE = generateCanChiTable(1900, 2100);
```

## 4. Câu Hỏi Về Độ Chính Xác

### Q11: Bazi có chính xác 100% không?

**A:** Không có hệ thống bói toán nào chính xác 100%. Bazi có độ chính xác bị ảnh hưởng bởi:

**Yếu tố ảnh hưởng:**

| Yếu tố | Mức độ ảnh hưởng | Giải pháp |
|--------|------------------|------------|
| Giờ sinh chính xác | **Rất cao** | Cần xác định chính xác giờ sinh |
| Múi giờ | **Cao** | Sử dụng IANA timezone |
| Năm nhuận | **Trung bình** | Correct lunar calendar library |
| Leap second | **Thấp** | Thường bỏ qua |
| Quốc gia/region | **Thấp** | Bazi dùng âm lịch phổ quát |

**Độ chính xác ước tính:**
- Giờ sinh chính xác (±15 phút): ~95%
- Giờ sinh approximate (±1 giờ): ~80%
- Giờ sinh ước lượng (sáng/chiều/tối): ~60%

### Q12: Tại sao cùng ngày sinh nhưng Bazi có thể khác nhau?

**A:** Có thể khác nhau vì:

1. **Khác múi giờ:**
   - Sinh ở Việt Nam (UTC+7) vs Nhật Bản (UTC+9)
   - Cùng giờ nhưng khác "giờ Bazi"

2. **Khác ngày âm lịch:**
   - Gần ngày Tết Nguyên Đán
   - Tháng nhuận có thể gây confusion

3. **Sai giờ sinh:**
   - Giờ bệnh viện ghi vs giờ thực
   - DST adjustment không được tính

4. **Phương pháp tính:**
   - Lunar calendar library khác nhau
   - Thuật toán Julian Day khác nhau

### Q13: Có nên dùng Bazi để quyết định quan trọng không?

**A:** Bazi nên được xem là **tham khảo**, không phải quyết định:

**Nên dùng để:**
- Hiểu bản thân (điểm mạnh/yếu)
- Xác định hướng phát triển
- Chọn thời điểm tốt cho việc quan trọng
- Hiểu mối quan hệ với người khác

**Không nên dùng để:**
- Quyết định hôn nhân (nên dựa vào tình cảm thực)
- Chọn nghề nghiệp duy nhất
- Đặt cược/đầu tư dựa hoàn toàn vào bazi
- Thay thế tư vấn chuyên môn (y tế, pháp lý)

## 5. Câu Hỏi Về API

### Q14: Làm sao để integrate Bazi API vào ứng dụng?

**A:** Integration steps:

**1. Gọi API:**
```typescript
const response = await fetch('/api/v1/bazi/charts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
  },
  body: JSON.stringify({
    birthDate: '1990-05-15',
    birthTime: '14:30',
    timeZone: 'Asia/Ho_Chi_Minh',
    gender: 'male'
  })
});

const { data: chart } = await response.json();
```

**2. Response structure:**
```typescript
interface BaziResponse {
  success: true;
  data: {
    id: string;
    pillars: {
      year: { can: string; chi: string };
      month: { can: string; chi: string };
      day: { can: string; chi: string };
      hour: { can: string; chi: string };
    };
    elements: {
      balance: { wood: number; fire: number; earth: number; metal: number; water: number };
    };
    menh: { name: string; element: string };
    napAm: { name: string };
  };
}
```

### Q15: Rate limit cho Bazi API là bao nhiêu?

**A:** Rate limits phụ thuộc vào plan:

| Plan | Requests/minute | Requests/day |
|------|-----------------|--------------|
| Free | 10 | 100 |
| Basic | 60 | 1,000 |
| Pro | 300 | 10,000 |
| Enterprise | Unlimited | Unlimited |

**Headers returned:**
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640000000
```

### Q16: Làm thế nào để xử lý error từ Bazi API?

**A:** Error handling pattern:

```typescript
async function fetchBazi(input: BaziInput) {
  try {
    const response = await baziApi.calculate(input);
    
    if (!response.success) {
      switch (response.error.code) {
        case 'INVALID_BIRTH_DATE':
          return { valid: false, message: 'Ngày sinh không hợp lệ' };
        case 'LUNAR_CONVERSION_ERROR':
          return { valid: false, message: 'Không chuyển được ngày âm lịch' };
        case 'RATE_LIMIT_EXCEEDED':
          return { valid: false, message: 'Quá rate limit, thử lại sau' };
        default:
          return { valid: false, message: 'Lỗi không xác định' };
      }
    }
    
    return { valid: true, data: response.data };
    
  } catch (error) {
    // Network error hoặc unexpected error
    console.error('Bazi API error:', error);
    return { valid: false, message: 'Lỗi kết nối' };
  }
}
```

## 6. Câu Hỏi Về Bảo Mật

### Q17: Dữ liệu ngày sinh có được bảo mật không?

**A:** Yes, các measures:

1. **Encryption at rest:**
   ```typescript
   // Mã hóa birth_date trong database
   const encrypted = encrypt(birthDate, ENCRYPTION_KEY);
   ```

2. **HTTPS only:**
   - Tất cả API calls phải qua HTTPS

3. **Access control:**
   - Users chỉ truy cập được charts của mình
   - Admin có thể audit nhưng không đọc raw data

4. **Data retention:**
   - User có thể xóa data
   - Auto-delete sau thời gian không hoạt động

### Q18: API key có thể bị revoke không?

**A:** Có, các options:

1. **Manual revoke:**
   ```
   DELETE /api/v1/keys/{keyId}
   ```

2. **Auto-expire:**
   ```typescript
   // Key expires sau 1 năm
   const key = await createApiKey({
     expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000)
   });
   ```

3. **Scope-based:**
   ```typescript
   // Key chỉ có quyền đọc
   const readOnlyKey = await createApiKey({
     scopes: ['bazi:read']
   });
   ```
