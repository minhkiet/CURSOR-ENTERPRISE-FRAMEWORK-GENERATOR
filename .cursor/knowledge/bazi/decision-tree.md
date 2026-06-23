# Decision Tree cho Hệ Thống Bazi

## 1. Decision Tree Tổng Quan

```
┌─────────────────────────────────────────────────────────────────┐
│                    BẮT ĐẦU: Tính Bazi                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. NHẬP DỮ LIỆU ĐẦU VÀO                                        │
│                                                                 │
│ Câu hỏi: Người dùng cung cấp đủ thông tin?                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    ┌─────────────────┐                                          │
│    │ CÓ              │                                          │
│    └────────┬────────┘                                          │
│             │                                                   │
│             ▼                                                   │
│    ┌─────────────────────────────────────────┐                  │
│    │ 2. VALIDATE INPUT                       │                  │
│    │                                         │                  │
│    │ Câu hỏi: Dữ liệu có hợp lệ?             │                  │
│    └──────────────────────┬──────────────────┘                  │
│                           │                                     │
│         ┌─────────────────┴─────────────────┐                 │
│         │ CÓ                                 │ KHÔNG           │
│         ▼                                     ▼                 │
│  ┌────────────────┐                    ┌────────────────┐        │
│  │ Tiếp tục      │                    │ Return Error   │        │
│  └───────┬────────┘                    │ VALIDATION_    │        │
│          │                             │ ERROR          │        │
│          │                             └────────────────┘        │
└──────────┼──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. CHUYỂN ĐỔI NGÀY SINH                                         │
│                                                                 │
│ Câu hỏi: Cần chuyển sang Âm lịch?                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    ┌─────────────────┐                                          │
│    │ CÓ              │                                          │
│    └────────┬────────┘                                          │
│             │                                                   │
│             ▼                                                   │
│    ┌─────────────────────────────────────────┐                  │
│    │ 3.1. Gọi Lunar Calendar Service         │                  │
│    │     Input: birthDate, timezone           │                  │
│    │     Output: lunarYear, lunarMonth,       │                  │
│    │            lunarDay, isLeapMonth         │                  │
│    └──────────────────────┬──────────────────┘                  │
│                           │                                     │
│         ┌─────────────────┴─────────────────┐                  │
│         │ THÀNH CÔNG                       │ LỖI             │
│         ▼                                   ▼                   │
│  ┌────────────────┐                    ┌────────────────┐        │
│  │ Lưu Lunar Date │                    │ Return Error   │        │
│  └───────┬────────┘                    │ LUNAR_CONV_    │        │
│          │                             │ ERROR          │        │
└──────────┼────────────────────────────┴────────────────┘        │
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. TÍNH NĂM TRỤ (YEAR PILLAR)                                   │
│                                                                 │
│ Câu hỏi: Tính Năm Trụ như thế nào?                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Formula:                                                        │
│   yearCanIndex = (lunarYear + 6) % 10                            │
│   yearChiIndex = (lunarYear + 8) % 12                            │
│                                                                 │
│ Ví dụ: lunarYear = 1990                                          │
│   yearCanIndex = (1990 + 6) % 10 = 1996 % 10 = 6 → Canh         │
│   yearChiIndex = (1990 + 8) % 12 = 1998 % 12 = 10 → Ngọ         │
│                                                                 │
│                           ▼                                     │
│    ┌─────────────────────────────────────────┐                  │
│    │ Năm Trụ: Can Canh + Chi Ngọ            │                  │
│    │ Vietnamese: "Canh Ngọ"                  │                  │
│    └─────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. TÍNH THÁNG TRỤ (MONTH PILLAR)                                │
│                                                                 │
│ Câu hỏi: Xác định Can Tháng dựa vào Năm Can?                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Bảng Can Tháng:                                                  │
│ ┌──────────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│ │ Năm Can  │ Tý │ Sửu │ Dần │ Mão │ Thìn│ Tỵ  │ Ngọ │ Mùi │ Thân│ Dậu │ Tuất│ Hợi │
│ ├──────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
│ │ Giáp/Ất │ Bính│ Bính│ Bính│ Bính│ Bính│ Bính│ Bính│ Bính│ Bính│ Bính│ Bính│ Bính│
│ │ Bính/   │ Mậu │ Mậu │ Mậu │ Mậu │ Mậu │ Mậu │ Mậu │ Mậu │ Mậu │ Mậu │ Mậu │ Mậu │
│ │ Đinh    │     │     │     │     │     │     │     │     │     │     │     │     │
│ │ Mậu/Kỷ  │ Canh│ Canh│ Canh│ Canh│ Canh│ Canh│ Canh│ Canh│ Canh│ Canh│ Canh│ Canh│
│ │ Canh/   │ Nhâm│ Nhâm│ Nhâm│ Nhâm│ Nhâm│ Nhâm│ Nhâm│ Nhâm│ Nhâm│ Nhâm│ Nhâm│ Nhâm│
│ │ Tân    │     │     │     │     │     │     │     │     │     │     │     │     │
│ │ Nhâm/   │ Giáp│ Giáp│ Giáp│ Giáp│ Giáp│ Giáp│ Giáp│ Giáp│ Giáp│ Giáp│ Giáp│ Giáp│
│ │ Quý    │     │     │     │     │     │     │     │     │     │     │     │     │
│ └──────────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
│                                                                 │
│ Chi Tháng = (lunarMonth + 1) % 12                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. TÍNH NGÀY TRỤ (DAY PILLAR)                                    │
│                                                                 │
│ Câu hỏi: Tính Ngày Trụ bằng phương pháp nào?                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ PHƯƠNG PHÁP: SỬ DỤNG JULIAN DAY NUMBER                      │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ Steps:                                                          │
│ 1. Chuyển ngày sang Julian Day Number                          │
│ 2. dayCanIndex = (JD + 1) % 10                                  │
│ 3. dayChiIndex = (JD + 1) % 12                                  │
│                                                                 │
│ Ví dụ: 15/05/2024                                               │
│   JD = 2460456                                                  │
│   dayCanIndex = (2460456 + 1) % 10 = 7 → Tân                   │
│   dayChiIndex = (2460456 + 1) % 12 = 1 → Sửu                    │
│                                                                 │
│                           ▼                                     │
│    ┌─────────────────────────────────────────┐                  │
│    │ Ngày Trụ: Can Tân + Chi Sửu            │                  │
│    │ Vietnamese: "Tân Sửu"                   │                  │
│    └─────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. TÍNH GIỜ TRỤ (HOUR PILLAR)                                   │
│                                                                 │
│ Câu hỏi: Giờ sinh thuộc Giờ nào trong Bazi?                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Bảng Giờ Chi:                                                   │
│ ┌─────────────┬──────────────┐                                  │
│ │ Giờ Dương  │ Giờ Bazi     │                                  │
│ ├─────────────┼──────────────┤                                  │
│ │ 23:00-00:59│ Tý           │                                  │
│ │ 01:00-02:59│ Sửu           │                                  │
│ │ 03:00-04:59│ Dần           │                                  │
│ │ 05:00-06:59│ Mão           │                                  │
│ │ 07:00-08:59│ Thìn           │                                  │
│ │ 09:00-10:59│ Tỵ            │                                  │
│ │ 11:00-12:59│ Ngọ           │                                  │
│ │ 13:00-14:59│ Mùi           │                                  │
│ │ 15:00-16:59│ Thân           │                                  │
│ │ 17:00-18:59│ Dậu           │                                  │
│ │ 19:00-20:59│ Tuất           │                                  │
│ │ 21:00-22:59│ Hợi           │                                  │
│ └─────────────┴──────────────┘                                  │
│                                                                 │
│ Giờ Can Index = (dayCanIndex * 2 + chiIndex/2) % 10             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. XÁC ĐỊNH CUNG MỆNH                                           │
│                                                                 │
│ Câu hỏi: Tính Cung Mệnh như thế nào?                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Dựa vào Ngày Can và Giới tính:                                  │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ NAM MỆNH (Thập Tự Pháp)                                    │ │
│ │                                                             │ │
│ │   Ngày Can = Giáp/Kỷ → Cung Cấn (Thổ)                      │ │
│ │   Ngày Can = Ất/Canh → Cung Ly (Hỏa)                      │ │
│ │   Ngày Can = Bính/Tân → Cung Khôn (Thổ)                   │ │
│ │   Ngày Can = Đinh/Nhâm → Cung Khang (Mộc)                 │ │
│ │   Ngày Can = Mậu/Quý → Cung Chấn (Mộc)                     │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ NỮ MỆNH (Thập Tự Pháp)                                     │ │
│ │                                                             │ │
│ │   Ngày Can = Giáp/Kỷ → Cung Chấn (Mộc)                     │ │
│ │   Ngày Can = Ất/Canh → Cung Khôn (Thổ)                    │ │
│ │   Ngày Can = Bính/Tân → Cung Ly (Hỏa)                      │ │
│ │   Ngày Can = Đinh/Nhâm → Cung Cấn (Thổ)                   │ │
│ │   Ngày Can = Mậu/Quý → Cung Khang (Mộc)                   │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 9. TÍNH NẠP ÂM                                                  │
│                                                                 │
│ Câu hỏi: Tra cứu Nạp Âm như thế nào?                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Sử dụng bảng 60 Nạp Âm:                                         │
│                                                                 │
│ Format: lookup_table[`${can} ${chi}`]                            │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ NĂM NẠP ÂM (60 combinations)                              │ │
│ │                                                             │ │
│ │ Giáp Tý / Ất Tý → Hải Trung Kim                           │ │
│ │ Bính Tý / Đinh Tý → Diện Không Hỏa                        │ │
│ │ Mậu Tý / Kỷ Tý → Sơn Hạ Hỏa                                │ │
│ │ Canh Tý / Tân Tý → Lộ Bàng Thổ                            │ │
│ │ Nhâm Tý / Quý Tý → Đại Khê Thủy                           │ │
│ │                                                             │ │
│ │ Giáp Sửu / Ất Sửu → Tích Lịch Hỏa                          │ │
│ │ Bính Sửu / Đinh Sửu → Giản Hạ Thổ                          │ │
│ │ ... (tiếp tục cho 60 combinations)                        │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 10. TÍNH NGŨ HÀNH                                               │
│                                                                 │
│ Câu hỏi: Xác định Ngũ Hành tương sinh/tương khắc?             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ BƯỚC 1: Gán Hành cho mỗi Can                               │ │
│ │                                                             │ │
│ │ Giáp, Ất → Mộc                                              │ │
│ │ Bính, Đinh → Hỏa                                            │ │
│ │ Mậu, Kỷ → Thổ                                               │ │
│ │ Canh, Tân → Kim                                              │ │
│ │ Nhâm, Quý → Thủy                                            │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ BƯỚC 2: Gán Hành cho mỗi Chi                               │ │
│ │                                                             │ │
│ │ Tý, Ngọ → Thủy                                              │ │
│ │ Sửu, Mùi → Thổ                                               │ │
│ │ Dần, Thân → Kim                                              │ │
│ │ Mão, Dậu → Mộc                                              │ │
│ │ Thìn, Tuất → Thổ                                             │ │
│ │ Tỵ, Hợi → Hỏa                                                │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ BƯỚC 3: Tính Tổng Balance                                  │ │
│ │                                                             │ │
│ │ elementScore = Σ(canHanh × 2) + Σ(chiHanh × 1)              │ │
│ │                                                             │ │
│ │ Ví dụ: chart với (Mộc×2, Hỏa×1, Thổ×2, Kim×1, Thủy×2)     │ │
│ │ → Mộc và Thủy cao nhất → Hành vượng                        │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 11. TẠO BÁZI CHART                                              │
│                                                                 │
│ Kết hợp tất cả thông tin:                                       │
│                                                                 │
│   {                                                            │
│     id: "uuid",                                                │
│     birthDate: "1990-05-15",                                   │
│     lunarDate: { year: 1990, month: 3, day: 20 },               │
│     pillars: {                                                 │
│       year: { can: "Canh", chi: "Ngọ" },                       │
│       month: { can: "Bính", chi: "Mão" },                      │
│       day: { can: "Tân", chi: "Sửu" },                          │
│       hour: { can: "Đinh", chi: "Mùi" }                         │
│     },                                                         │
│     menh: { name: "Ly", element: "Hỏa" },                       │
│     napAm: { year: "Lộ Bàng Thổ" },                             │
│     elements: {                                                │
│       wood: 2, fire: 3, earth: 2, metal: 1, water: 2           │
│     }                                                           │
│   }                                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                         KẾT THÚC                                │
│                                                                 │
│ Output: BaziChart với đầy đủ thông tin Tứ Trụ,                 │
│         Cung Mệnh, Nạp Âm, Ngũ Hành                            │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Decision Tree - Chi Tiết Từng Bước

### 2.1 Validate Input

```
START: Validate Input
│
├── birthDate format hợp lệ? (YYYY-MM-DD)
│   ├── KHÔNG → Return ERROR: INVALID_DATE_FORMAT
│   └── CÓ
│       │
│       ├── birthDate > today?
│       │   ├── CÓ → Return ERROR: FUTURE_DATE
│       │   └── KHÔNG
│       │
│       └── birthDate >= 1900-01-01?
│           ├── KHÔNG → Return ERROR: DATE_TOO_OLD
│           └── CÓ
│               │
│               └── Tiếp tục validate...
│
├── birthTime format hợp lệ? (HH:MM)
│   ├── KHÔNG → Return ERROR: INVALID_TIME_FORMAT
│   └── CÓ
│       │
│       ├── hour >= 0 AND hour <= 23?
│       │   ├── KHÔNG → Return ERROR: INVALID_HOUR
│       │   └── CÓ
│       │
│       └── minute >= 0 AND minute <= 59?
│           ├── KHÔNG → Return ERROR: INVALID_MINUTE
│           └── CÓ → OK
│
├── timezone hợp lệ?
│   ├── KHÔNG → Return ERROR: INVALID_TIMEZONE
│   └── CÓ → OK
│
└── gender in ['male', 'female']?
    ├── KHÔNG → Return ERROR: INVALID_GENDER
    └── CÓ → VALIDATION_PASSED
```

### 2.2 Lunar Conversion

```
START: Convert to Lunar Date
│
├── Check cache: lunarCache.get(birthDate + timezone)
│   ├── HIT → Return cached LunarDate
│   └── MISS
│       │
│       └── Gọi Lunar Calendar Service
│           │
│           ├── API call thành công?
│           │   ├── KHÔNG → Return ERROR: LUNAR_SERVICE_UNAVAILABLE
│           │   └── CÓ
│           │
│           └── Response valid?
│               ├── KHÔNG → Return ERROR: LUNAR_CONVERSION_FAILED
│               └── CÓ
│                   │
│                   └── Parse response
│                       │
│                       ├── lunarYear trong range 1900-2100?
│                       │   ├── KHÔNG → Return ERROR: LUNAR_YEAR_OUT_OF_RANGE
│                       │   └── CÓ
│                       │
│                       ├── lunarMonth trong range 1-13?
│                       │   ├── KHÔNG → Return ERROR: INVALID_LUNAR_MONTH
│                       │   └── CÓ
│                       │
│                       └── lunarDay trong range 1-30?
│                           ├── KHÔNG → Return ERROR: INVALID_LUNAR_DAY
│                           └── CÓ
│                               │
│                               └── Store to cache
│                                   │
│                                   └── Return LunarDate
```

### 2.3 Year Pillar Calculation

```
START: Calculate Year Pillar
│
├── Input: lunarYear (VD: 1990)
│
├── Calculate yearCanIndex = (lunarYear + 6) % 10
│   │
│   ├── (1990 + 6) % 10 = 1996 % 10 = 6
│   │
│   └── Map index to Can:
│       0 = Giáp, 1 = Ất, 2 = Bính, 3 = Đinh, 4 = Mậu
│       5 = Kỷ, 6 = Canh, 7 = Tân, 8 = Nhâm, 9 = Quý
│       │
│       └── yearCanIndex = 6 → "Canh"
│
├── Calculate yearChiIndex = (lunarYear + 8) % 12
│   │
│   ├── (1990 + 8) % 12 = 1998 % 12 = 10
│   │
│   └── Map index to Chi:
│       0 = Tý, 1 = Sửu, 2 = Dần, 3 = Mão, 4 = Thìn, 5 = Tỵ
│       6 = Ngọ, 7 = Mùi, 8 = Thân, 9 = Dậu, 10 = Tuất, 11 = Hợi
│       │
│       └── yearChiIndex = 10 → "Ngọ"
│
└── Return Year Pillar: { can: "Canh", chi: "Ngọ" }
```

### 2.4 Month Pillar Calculation

```
START: Calculate Month Pillar
│
├── Input: yearCan, lunarMonth (VD: Canh, tháng 3)
│
├── Xác định Can Tháng theo Năm Can:
│   │
│   ├── Năm Can thuộc nhóm nào?
│   │   ├── Giáp/Ất (index 0,1) → Can Tháng = Bính
│   │   ├── Bính/Đinh (index 2,3) → Can Tháng = Mậu
│   │   ├── Mậu/Kỷ (index 4,5) → Can Tháng = Canh
│   │   ├── Canh/Tân (index 6,7) → Can Tháng = Nhâm
│   │   └── Nhâm/Quý (index 8,9) → Can Tháng = Giáp
│   │
│   └── Với yearCan = Canh (index 6)
│       → Năm thuộc nhóm Canh/Tân
│       → Can Tháng = Nhâm
│
├── Calculate Chi Tháng:
│   │
│   └── chiIndex = (lunarMonth + 1) % 12
│       Với lunarMonth = 3
│       → chiIndex = (3 + 1) % 12 = 4
│       → "Thìn"
│
└── Return Month Pillar: { can: "Nhâm", chi: "Thìn" }
```

### 2.5 Day Pillar Calculation

```
START: Calculate Day Pillar
│
├── Input: lunarDate (VD: 1990-03-20)
│
├── Bước 1: Chuyển sang Julian Day Number
│   │
│   └── Sử dụng công thức:
│       a = floor((14 - month) / 12)
│       y = year + 4800 - a
│       m = month + 12*a - 3
│       JD = day + floor((153*m + 2)/5) + 365*y + floor(y/4) 
│             - floor(y/100) + floor(y/400) - 32045
│
├── Bước 2: Tính Day Can Index
│   │
│   └── dayCanIndex = (JD + 1) % 10
│       VD: JD = 2447893
│       → dayCanIndex = (2447893 + 1) % 10 = 4
│       → "Mậu"
│
├── Bước 3: Tính Day Chi Index
│   │
│   └── dayChiIndex = (JD + 1) % 12
│       VD: JD = 2447893
│       → dayChiIndex = (2447893 + 1) % 12 = 5
│       → "Tỵ"
│
└── Return Day Pillar: { can: "Mậu", chi: "Tỵ" }
```

### 2.6 Hour Pillar Calculation

```
START: Calculate Hour Pillar
│
├── Input: dayCan ("Mậu"), birthTime ("14:30")
│
├── Bước 1: Xác định Giờ Chi
│   │
│   └── Từ birthTime = 14:30
│       → 14:00-14:59 = Giờ Mùi
│       → chiIndex = 7
│
├── Bước 2: Tính Giờ Can
│   │
│   └── Công thức:
│       hourCanIndex = (dayCanIndex*2 + floor(chiIndex/2)) % 10
│       
│       Với dayCan = Mậu = index 4
│       Với chiIndex = 7 (Mùi)
│       → hourCanIndex = (4*2 + floor(7/2)) % 10
│       → hourCanIndex = (8 + 3) % 10 = 11 % 10 = 1
│       → "Ất"
│
└── Return Hour Pillar: { can: "Ất", chi: "Mùi" }
```

### 2.7 Menh Calculation

```
START: Calculate Menh
│
├── Input: dayCan ("Mậu"), gender ("male")
│
├── Xác định Cung Mệnh:
│   │
│   ├── Giới tính = male?
│   │   ├── CÓ
│   │   │   │
│   │   │   └── Xem bảng Nam Mệnh:
│   │   │       Giáp/Kỷ → Cấn
│   │   │       Ất/Canh → Ly
│   │   │       Bính/Tân → Khôn
│   │   │       Đinh/Nhâm → Khang
│   │   │       Mậu/Quý → Chấn
│   │   │       
│   │   │       dayCan = Mậu → Cung = Chấn
│   │   │
│   │   └── KHÔNG (female)
│   │       │
│   │       └── Xem bảng Nữ Mệnh:
│   │           Giáp/Kỷ → Chấn
│   │           Ất/Canh → Khôn
│   │           Bính/Tân → Ly
│   │           Đinh/Nhâm → Cấn
│   │           Mậu/Quý → Khang
│   │
│   └── Xác định Hành của Cung:
│       │
│       ├── Cấn, Khôn → Thổ
│       ├── Ly → Hỏa
│       ├── Khang, Chấn → Mộc
│       ├── Chấn → Mộc
│       └── Không → Thủy
│
│       Cung = Chấn → Hành = Mộc
│
└── Return Menh: { name: "Chấn", element: "Mộc" }
```

### 2.8 Nap Am Calculation

```
START: Calculate Nap Am
│
├── Input: yearPillar (Can: "Canh", Chi: "Ngọ")
│
├── Tra cứu bảng Nạp Âm:
│   │
│   └── lookup_table["Canh Ngọ"]
│       │
│       ├── Giáp Ngọ / Ất Ngọ → Sơn Hạ Hỏa
│       ├── Bính Ngọ / Đinh Ngọ → Thiên Hà Thủy
│       ├── Mậu Ngọ / Kỷ Ngọ → Địa Bì Thổ
│       ├── Canh Ngọ / Tân Ngọ → Phượng Các Mộc
│       └── Nhâm Ngọ / Quý Ngọ → Bình Địa Kim
│           │
│           → Canh Ngọ → "Phượng Các Mộc"
│
└── Return Nap Am: { name: "Phượng Các Mộc", element: "Mộc" }
```

### 2.9 Element Balance Calculation

```
START: Calculate Element Balance
│
├── Input: 4 Pillars
│   │
│   ├── Year: Canh (Kim), Ngọ (Hỏa)
│   ├── Month: Nhâm (Thủy), Thìn (Thổ)
│   ├── Day: Mậu (Thổ), Tỵ (Hỏa)
│   └── Hour: Ất (Mộc), Mùi (Thổ)
│
├── Tính điểm cho mỗi pillar:
│   │
│   ├── Can đóng góp 2 điểm
│   └── Chi đóng góp 1 điểm
│
├── Tổng hợp:
│   │
│   ├── Mộc: Ất×2 + Mão×1 = 2 + 1 = 3
│   ├── Hỏa: Ngọ×2 + Tỵ×1 = 2 + 1 = 3
│   ├── Thổ: Thìn×1 + Mùi×1 + Mậu×2 = 4
│   ├── Kim: Canh×2 = 2
│   └── Thủy: Nhâm×2 = 2
│
├── Xác định hành vượng/suy:
│   │
│   ├── Total = 3+3+4+2+2 = 14
│   ├── Average = 14/5 = 2.8
│   │
│   ├── Hành vượng (>= average + 1): Thổ (4)
│   └── Hành suy (<= average - 1): Kim (2), Thủy (2)
│
└── Return Element Balance:
    {
      wood: 3, fire: 3, earth: 4, metal: 2, water: 2,
      dominant: "Thổ",
      weakest: ["Kim", "Thủy"]
    }
```

## 3. Error Handling Decision Tree

```
START: Error Occurred
│
├── Error Type = VALIDATION_ERROR?
│   │
│   ├── CÓ
│   │   │
│   │   └── Specific validation error?
│   │       ├── INVALID_DATE → "Ngày sinh không hợp lệ"
│   │       ├── INVALID_TIME → "Giờ sinh không hợp lệ"
│   │       ├── INVALID_TIMEZONE → "Múi giờ không hợp lệ"
│   │       ├── FUTURE_DATE → "Ngày sinh không thể là tương lai"
│   │       └── OLD_DATE → "Ngày sinh quá cũ (trước 1900)"
│   │
│   └── Return 400 Bad Request
│
├── Error Type = LUNAR_CONVERSION_ERROR?
│   │
│   ├── CÓ
│   │   │
│   │   └── Retry possible?
│   │       ├── CÓ (temporary failure)
│   │       │   │
│   │       │   └── Retry với exponential backoff
│   │       │       │
│   │       │       ├── Retry 1: wait 1s
│   │       │       ├── Retry 2: wait 2s
│   │       │       └── Retry 3: wait 4s
│   │       │
│   │       └── KHÔNG (permanent failure)
│   │           │
│   │           └── Return 422 Unprocessable Entity
│   │
│   └── Return 422 với LUNAR_CONVERSION_ERROR
│
├── Error Type = NOT_FOUND?
│   │
│   └── Return 404 Not Found
│
├── Error Type = UNAUTHORIZED?
│   │
│   └── Return 401/403 Unauthorized/Forbidden
│
└── Error Type = INTERNAL_ERROR?
    │
    └── Return 500 Internal Server Error
```
