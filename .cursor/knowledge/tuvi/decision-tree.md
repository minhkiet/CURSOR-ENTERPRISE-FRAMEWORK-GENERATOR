# Decision Tree cho Hệ Thống Tử Vi

## 1. Decision Tree Tổng Quan

```
┌─────────────────────────────────────────────────────────────────┐
│                    BẮT ĐẦU: Tính Tử Vi                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. NHẬP DỮ LIỆU ĐẦU VÀO                                        │
│                                                                 │
│ Câu hỏi: Dữ liệu có đầy đủ và hợp lệ?                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    ┌─────────────────┐                                          │
│    │ CÓ              │                                          │
│    └────────┬────────┘                                          │
│             │                                                   │
│             ▼                                                   │
│    ┌─────────────────────────────────────────┐                  │
│    │ Validate Input                           │                  │
│    │ - birthDate (YYYY-MM-DD)                 │                  │
│    │ - birthTime (HH:MM)                      │                  │
│    │ - timeZone (IANA)                        │                  │
│    │ - gender (male/female)                   │                  │
│    └──────────────────────┬──────────────────┘                  │
│                           │                                     │
│         ┌─────────────────┴─────────────────┐                  │
│         │ HỢP LỆ                            │ KHÔNG HỢP LỆ    │
│         ▼                                     ▼                   │
│  ┌────────────────┐                    ┌────────────────┐        │
│  │ Tiếp tục       │                    │ Return Error   │        │
│  └───────┬────────┘                    │ VALIDATION_    │        │
│          │                             │ ERROR          │        │
└──────────┼────────────────────────────┴────────────────┘        │
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. CHUYỂN ĐỔI NGÀY SINH → ÂM LỊCH                               │
│                                                                 │
│ Câu hỏi: Chuyển đổi âm lịch thành công?                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    ┌─────────────────────────────────────────┐                  │
│    │ Gọi Lunar Calendar Service               │                  │
│    │ Input: birthDate, timezone               │                  │
│    │ Output: lunarYear, lunarMonth,           │                  │
│    │         lunarDay, isLeapMonth            │                  │
│    └──────────────────────┬──────────────────┘                  │
│                           │                                     │
│         ┌─────────────────┴─────────────────┐                  │
│         │ THÀNH CÔNG                       │ LỖI             │
│         ▼                                     ▼                   │
│  ┌────────────────┐                    ┌────────────────┐        │
│  │ Lưu Lunar Date │                    │ Return Error   │        │
│  └───────┬────────┘                    │ LUNAR_ERROR    │        │
│          │                             └────────────────┘        │
└──────────┼──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. XÁC ĐỊNH NGÀY CAN CHI                                        │
│                                                                 │
│ Câu hỏi: Tính Ngày Can Chi như thế nào?                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Sử dụng Julian Day Number:                                      │
│                                                                 │
│   JD = dateToJD(lunarDate)                                      │
│   dayCanIndex = (JD + 1) % 10                                   │
│   dayChiIndex = (JD + 1) % 12                                   │
│                                                                 │
│ Ví dụ: 15/05/2024 (Âm: 08/04/2024)                             │
│   JD = 2460456                                                  │
│   dayCanIndex = (2460456 + 1) % 10 = 7 → Tân                   │
│   dayChiIndex = (2460456 + 1) % 12 = 1 → Sửu                    │
│                                                                 │
│                           ▼                                     │
│    ┌─────────────────────────────────────────┐                  │
│    │ Ngày: Tân Sửu                           │                  │
│    └─────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. TÍNH MỆNH CÁCH                                               │
│                                                                 │
│ Câu hỏi: Xác định Mệnh Cách dựa vào giới tính?                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ NAM MỆNH                                                     │ │
│ │                                                             │ │
│ │ Ngày Can = Giáp, Kỷ → Mệnh (Kim)                           │ │
│ │ Ngày Can = Ất, Canh → Phụ Mẫu (Thổ)                        │ │
│ │ Ngày Can = Bính, Tân → Phúc Đức (Thổ)                     │ │
│ │ Ngày Can = Đinh, Nhâm → Điền Trạch (Thổ)                  │ │
│ │ Ngày Can = Mậu, Quý → Quan Lộc (Kim)                       │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ NỮ MỆNH                                                     │ │
│ │                                                             │ │
│ │ Ngày Can = Giáp, Kỷ → Quan Lộc (Kim)                       │ │
│ │ Ngày Can = Ất, Canh → Điền Trạch (Thổ)                   │ │
│ │ Ngày Can = Bính, Tân → Phúc Đức (Thổ)                     │ │
│ │ Ngày Can = Đinh, Nhâm → Phụ Mẫu (Thổ)                    │ │
│ │ Ngày Can = Mậu, Quý → Mệnh (Kim)                          │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│                           ▼                                     │
│    ┌─────────────────────────────────────────┐                  │
│    │ Ví dụ: Nam + Ngày Tân → Mệnh (Kim)    │                  │
│    │ Ví dụ: Nữ + Ngày Mậu → Mệnh (Kim)     │                  │
│    └─────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. XÁC ĐỊNH VỊ TRÍ CUNG MỆNH                                    │
│                                                                 │
│ Câu hỏi: Cung Mệnh nằm ở vị trí nào trong 12 Cung?             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 12 Cung (theo thứ tự ngược chiều kim đồng hồ từ Cung Mệnh):    │
│                                                                 │
│   Index 0: Mệnh        ──┐                                     │
│   Index 1: Phụ Mẫu       │                                     │
│   Index 2: Phúc Đức      │ Thuận chiều Kim đồng hồ              │
│   Index 3: Điền Trạch    │                                     │
│   Index 4: Quan Lộc      │                                     │
│   Index 5: Nô Bộc        ├─── 6 Cung đầu                       │
│   Index 6: Thiên Di      │                                     │
│   Index 7: Tật Ách       │                                     │
│   Index 8: Tài Bạch      │                                     │
│   Index 9: Tử Tức        │                                     │
│   Index 10: Phu Thê      │                                     │
│   Index 11: Huỵệt     ───┘                                     │
│                                                                 │
│ Cung Mệnh xác định vị trí bắt đầu của 12 Cung                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. XÁC ĐỊNH VỊ TRÍ CÁC SAO                                     │
│                                                                 │
│ Câu hỏi: Sao nhập cung dựa vào yếu tố nào?                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Sao được xác định bởi 4 yếu tố:                                  │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ THEO NGÀY                                                     │ │
│ │ Công thức: position = (dayCanIndex * 6 + dayChiIndex) % 12   │ │
│ │ Ví dụ: Tân (7) Sửu (1) → (7*6 + 1) % 12 = 43 % 12 = 7     │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ THEO THÁNG                                                   │ │
│ │ Công thức: position = (thang + 1) % 12                       │ │
│ │ Ví dụ: Tháng 4 → (4+1) % 12 = 5                            │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ THEO NĂM                                                     │ │
│ │ Công thức: position = (nam + thang) % 12                     │ │
│ │ Ví dụ: 2024 + 4 = 2028 % 12 = 4                            │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ THEO GIỜ                                                     │ │
│ │ Công thức: position = Math.floor(gio / 2) % 12              │ │
│ │ Ví dụ: 14:30 → Math.floor(14/2) % 12 = 7 % 12 = 7          │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. SẮP XẾP SAO VÀO 12 CUNG                                      │
│                                                                 │
│ Câu hỏi: Xác định Sao chiếm cung như thế nào?                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Quy tắc:                                                        │
│                                                                 │
│ 1. Bắt đầu từ Cung Mệnh, xoay NGƯỢC chiều kim đồng hồ          │
│ 2. Sao đầu tiên (loại chính) trong cung = "Sao chiếm cung"     │
│ 3. Cung không có sao chính = "Cung trống"                       │
│                                                                 │
│ Ví dụ: Cung Mệnh tại index 0                                    │
│                                                                 │
│   Cung Mệnh (0): Tử Vi, Văn Xương                               │
│   Phụ Mẫu (11): Thái Dương, Tả Phụ                              │
│   Phúc Đức (10): Liêm Trinh, Hữu Bật                            │
│   ... (tiếp tục ngược chiều kim)                               │
│                                                                 │
│                           ▼                                     │
│    ┌─────────────────────────────────────────┐                  │
│    │ Cung trống → isEmpty = true             │                  │
│    │ Cung có sao → isEmpty = false           │                  │
│    │ Sao chính đầu tiên → occupant          │                  │
│    └─────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. TÍNH VẬN HẠN                                                │
│                                                                 │
│ Câu hỏi: Xác định Vận hạn như thế nào?                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ XÁC ĐỊNH NĂM BẮT ĐẦU VẬN                                   │ │
│ │                                                             │ │
│ │ Nam: Vận bắt đầu từ năm sinh                               │ │
│ │ Nữ: Vận bắt đầu từ năm sinh + 1                            │ │
│ │                                                             │ │
│ │ Ví dụ: Sinh 1990                                            │ │
│ │   Nam: Vận 1 bắt đầu 1990                                   │ │
│ │   Nữ: Vận 1 bắt đầu 1991                                    │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ PHÂN LOẠI VẬN                                               │ │
│ │                                                             │ │
│ │ Vận 1-4 (0-39 tuổi): Thiên Vận                             │ │
│ │ Vận 5-8 (40-79 tuổi): Nhân Vận                             │ │
│ │ Vận 9-12 (80-120 tuổi): Địa Vận                            │ │
│ │                                                             │ │
│ │ Mỗi Vận kéo dài 10 năm                                     │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ CÁC HẠN TRONG MỖI VẬN                                      │ │
│ │                                                             │ │
│ │ Thiên Vận: Tràng Sinh, Mộc Dục, Quan Đới...                 │ │
│ │ Nhân Vận: Tuệ Giải, Tài Trì, Lâm Quan...                   │ │
│ │ Địa Vận: Kim Tài, Ngọc Bảo, Bảo Khương...                 │ │
│ │                                                             │ │
│ │ Hạn xác định bởi: (tuổi trong vận) % 12                    │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 9. TÍNH PHƯƠNG MỆNH                                             │
│                                                                 │
│ Câu hỏi: Xác định Phương Mệnh như thế nào?                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ TƯƠNG TÁC NGŨ HÀNH                                         │ │
│ │                                                             │ │
│ │ Xác định:                                                   │ │
│ │ - Hành của Mệnh                                             │ │
│ │ - Hành tương sinh (có lợi)                                  │ │
│ │ - Hành tương khắc (bất lợi)                                │ │
│ │ - Hành cùng sinh (hỗ trợ)                                  │ │
│ │                                                             │ │
│ │ Ví dụ: Mệnh Kim                                             │ │
│ │   Tương sinh: Thủy (Kim sinh Thủy)                         │ │
│ │   Tương khắc: Hỏa (Hỏa khắc Kim)                          │ │
│ │   Hỗ trợ: Thổ (Thổ sinh Kim)                               │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ HƯỚNG TỐT/XẤU                                              │ │
│ │                                                             │ │
│ │ Kim: Tây, Tây Bắc, Tây Nam, Bắc                            │ │
│ │ Mộc: Đông, Đông Nam, Nam, Bắc                              │ │
│ │ Thủy: Bắc, Đông Bắc, Tây, Đông                             │ │
│ │ Hỏa: Nam, Đông Nam, Bắc, Đông                              │ │
│ │ Thổ: Tây Nam, Đông Bắc, Nam, Bắc                          │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 10. TẠO TỬ VI CHART                                            │
│                                                                 │
│ Kết hợp tất cả thông tin:                                       │
│                                                                 │
│   {                                                            │
│     id: "uuid",                                                │
│     birthDate: "1990-05-15",                                   │
│     lunarDate: { year: 1990, month: 3, day: 20 },              │
│     menhCach: {                                                │
│       name: "Mệnh",                                           │
│       element: "Kim",                                          │
│       can: "Tân",                                             │
│       chi: "Sửu"                                              │
│     },                                                         │
│     cungMenhIndex: 0,                                          │
│     cungs: [                                                   │
│       { name: "Mệnh", stars: [...], isEmpty: false },         │
│       { name: "Phụ Mẫu", stars: [...], isEmpty: true },       │
│       // ... 12 cungs                                         │
│     ],                                                         │
│     vanHan: [                                                  │
│       { year: 1990, van: "thien", han: "Tràng Sinh" },       │
│       // ... các vận                                           │
│     ],                                                         │
│     phuongMen: {                                                │
│       favorableElements: ["Thủy", "Thổ"],                     │
│       unfavorableElements: ["Hỏa"],                           │
│       favorableDirections: ["Tây", "Tây Bắc"]                 │
│     }                                                          │
│   }                                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                         KẾT THÚC                                │
│                                                                 │
│ Output: TuviChart với đầy đủ thông tin:                         │
│         - Mệnh Cách                                             │
│         - 12 Cung với Sao                                       │
│         - Vận Hạn                                               │
│         - Phương Mệnh                                          │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Decision Tree Chi Tiết Từng Bước

### 2.1 Validate Input

```
START: Validate Input
│
├── birthDate format hợp lệ? (YYYY-MM-DD)
│   ├── KHÔNG → ERROR: INVALID_DATE_FORMAT
│   └── CÓ
│       │
│       ├── birthDate > today?
│       │   ├── CÓ → ERROR: FUTURE_DATE
│       │   └── KHÔNG
│       │
│       └── birthDate >= 1900-01-01?
│           ├── KHÔNG → ERROR: DATE_TOO_OLD
│           └── CÓ → Tiếp tục
│
├── birthTime format hợp lệ? (HH:MM)
│   ├── KHÔNG → ERROR: INVALID_TIME_FORMAT
│   └── CÓ
│       │
│       ├── hour trong 0-23?
│       │   ├── KHÔNG → ERROR: INVALID_HOUR
│       │   └── CÓ
│       │
│       └── minute trong 0-59?
│           ├── KHÔNG → ERROR: INVALID_MINUTE
│           └── CÓ → Tiếp tục
│
├── timezone hợp lệ? (IANA format)
│   ├── KHÔNG → ERROR: INVALID_TIMEZONE
│   └── CÓ → Tiếp tục
│
└── gender in ['male', 'female']?
    ├── KHÔNG → ERROR: INVALID_GENDER
    └── CÓ → VALIDATION_PASSED
```

### 2.2 Lunar Conversion

```
START: Convert to Lunar
│
├── Check cache: lunarCache.get(birthDate + timezone)
│   ├── HIT → Return cached LunarDate
│   └── MISS
│       │
│       └── Gọi Lunar Calendar Service
│           │
│           ├── API thành công?
│           │   ├── KHÔNG → ERROR: LUNAR_SERVICE_UNAVAILABLE
│           │   └── CÓ
│           │
│           └── Parse response
│               │
│               ├── lunarYear trong 1900-2100?
│               │   ├── KHÔNG → ERROR: YEAR_OUT_OF_RANGE
│               │   └── CÓ
│               │
│               ├── lunarMonth trong 1-13?
│               │   ├── KHÔNG → ERROR: INVALID_MONTH
│               │   └── CÓ
│               │
│               ├── lunarDay trong 1-30?
│               │   ├── KHÔNG → ERROR: INVALID_DAY
│               │   └── CÓ
│               │
│               └── Store to cache
│                   │
│                   └── Return LunarDate
```

### 2.3 Menh Calculation

```
START: Calculate Menh
│
├── Input: dayCan ("Tân"), gender ("male")
│
├── Gender = "male"?
│   ├── CÓ
│   │   │
│   │   └── Xem bảng Nam Mệnh:
│   │       Giáp → Mệnh (Kim)
│   │       Ất → Phụ Mẫu (Thổ)
│   │       Bính → Phúc Đức (Thổ)
│   │       Đinh → Điền Trạch (Thổ)
│   │       Mậu → Quan Lộc (Kim)
│   │       Kỷ → Mệnh (Kim)
│   │       Canh → Phụ Mẫu (Thổ)
│   │       Tân → Phúc Đức (Thổ)
│   │       Nhâm → Điền Trạch (Thổ)
│   │       Quý → Quan Lộc (Kim)
│   │
│   │       dayCan = "Tân" → Phúc Đức (Thổ)
│   │
│   └── KHÔNG (female)
│       │
│       └── Xem bảng Nữ Mệnh:
│           Giáp → Quan Lộc (Kim)
│           Ất → Điền Trạch (Thổ)
│           Bính → Phúc Đức (Thổ)
│           Đinh → Phụ Mẫu (Thổ)
│           Mậu → Mệnh (Kim)
│           Kỷ → Mệnh (Kim)
│           Canh → Điền Trạch (Thổ)
│           Tân → Phúc Đức (Thổ)
│           Nhâm → Phụ Mẫu (Thổ)
│           Quý → Quan Lộc (Kim)
│
│           dayCan = "Tân" → Phúc Đức (Thổ)
│
└── Return MenhInfo: { name: "Phúc Đức", element: "Thổ" }
```

### 2.4 CungMenh Position

```
START: Determine CungMenh Position
│
├── Input: menhName ("Phúc Đức"), gender ("male")
│
├── Xác định Cung index:
│   │
│   ├── Nam: index = bảng Nam Mệnh.indexOf(menhName)
│   └── Nữ: index = bảng Nữ Mệnh.indexOf(menhName)
│
├── Bảng Cung:
│   Index 0: Mệnh
│   Index 1: Phụ Mẫu
│   Index 2: Phúc Đức
│   Index 3: Điền Trạch
│   Index 4: Quan Lộc
│   Index 5: Nô Bộc
│   Index 6: Thiên Di
│   Index 7: Tật Ách
│   Index 8: Tài Bạch
│   Index 9: Tử Tức
│   Index 10: Phu Thê
│   Index 11: Huỵệt
│
├── menhName = "Phúc Đức" → index = 2
│
└── Return cungMenhIndex = 2
```

### 2.5 Sao Position Calculation

```
START: Calculate Sao Position
│
├── Input: lunarDate, birthTime, cungMenhIndex
│
├── Bước 1: Tính vị trí theo Ngày
│   │
│   └── dayCanIndex = 7 ("Tân")
│       dayChiIndex = 1 ("Sửu")
│       dayPosition = (7 * 6 + 1) % 12 = 43 % 12 = 7
│       → "Thiên Di"
│
├── Bước 2: Tính vị trí theo Tháng
│   │
│   └── lunarMonth = 4
│       monthPosition = (4 + 1) % 12 = 5
│       → "Quan Lộc"
│
├── Bước 3: Tính vị trí theo Năm
│   │
│   └── lunarYear = 1990
│       yearPosition = (1990 + 4) % 12 = 1994 % 12 = 6
│       → "Thiên Di"
│
├── Bước 4: Tính vị trí theo Giờ
│   │
│   └── birthTime = "14:30"
│       hour = 14
│       hourPosition = Math.floor(14/2) % 12 = 7 % 12 = 7
│       → "Thiên Di"
│
└── Return saoPositions: {
    ngay: "Thiên Di",
    thang: "Quan Lộc",
    nam: "Thiên Di",
    gio: "Thiên Di"
  }
```

### 2.6 Arrange Stars to Cungs

```
START: Arrange Stars to Cungs
│
├── Input: cungMenhIndex = 2, saoPositions
│
├── 12 Cung theo thứ tự (index):
│   0: Mệnh, 1: Phụ Mẫu, 2: Phúc Đức, 3: Điền Trạch,
│   4: Quan Lộc, 5: Nô Bộc, 6: Thiên Di, 7: Tật Ách,
│   8: Tài Bạch, 9: Tử Tức, 10: Phu Thê, 11: Huỵệt
│
├── Sắp xếp: Bắt đầu từ Cung Mệnh (index 2), xoay NGƯỢC
│
│   Cung Mệnh (2): [Tử Vi, Văn Xương]
│   Phụ Mẫu (1): [Thái Dương, Tả Phụ]
│   Phúc Đức (0): [Liêm Trinh, Hữu Bật]
│   Điền Trạch (11): []
│   Quan Lộc (10): [Lộc Tồn]
│   Nô Bộc (9): []
│   Thiên Di (8): [Thái Âm]
│   Tật Ách (7): [Kình Dương]
│   Tài Bạch (6): []
│   Tử Tức (5): []
│   Phu Thê (4): []
│   Huỵệt (3): [Cự Môn]
│
├── Xác định Cung trống:
│   │
│   ├── Điền Trạch: isEmpty = true (không sao chính)
│   ├── Nô Bộc: isEmpty = true
│   ├── Tài Bạch: isEmpty = true
│   ├── Tử Tức: isEmpty = true
│   ├── Phu Thê: isEmpty = true
│   │
│   └── Các cung còn lại: isEmpty = false
│
└── Return arrangedCungs
```

### 2.7 VanHan Calculation

```
START: Calculate VanHan
│
├── Input: birthYear = 1990, gender = "male"
│
├── Xác định năm bắt đầu Vận:
│   │
│   ├── Gender = "male"?
│   │   ├── CÓ → vanStartYear = 1990
│   │   └── KHÔNG → vanStartYear = 1991
│   │
│   └── vanStartYear = 1990
│
├── Tính các Vận:
│   │
│   ├── Vận 1: 1990-1999 (tuổi 0-9) → Thiên Vận
│   ├── Vận 2: 2000-2009 (tuổi 10-19) → Thiên Vận
│   ├── Vận 3: 2010-2019 (tuổi 20-29) → Thiên Vận
│   ├── Vận 4: 2020-2029 (tuổi 30-39) → Thiên Vận
│   ├── Vận 5: 2030-2039 (tuổi 40-49) → Nhân Vận
│   ├── Vận 6: 2040-2049 (tuổi 50-59) → Nhân Vận
│   ├── Vận 7: 2050-2059 (tuổi 60-69) → Nhân Vận
│   ├── Vận 8: 2060-2069 (tuổi 70-79) → Nhân Vận
│   ├── Vận 9: 2070-2079 (tuổi 80-89) → Địa Vận
│   └── ...
│
├── Tính Hạn trong mỗi Vận:
│   │
│   └── Ví dụ: Vận 1 (1990-1999)
│       │
│       ├── 1990 (tuổi 0): Tràng Sinh
│       ├── 1991 (tuổi 1): Mộc Dục
│       ├── 1992 (tuổi 2): Quan Đới
│       ├── 1993 (tuổi 3): Mộc Trì
│       ├── 1994 (tuổi 4): Mộc Tàng
│       ├── 1995 (tuổi 5): Hoang Vu
│       ├── 1996 (tuổi 6): Kiếp Tài
│       ├── 1997 (tuổi 7): Ngũ Bất
│       ├── 1998 (tuổi 8): Tử Thọ
│       └── 1999 (tuổi 9): Phúc Dương
│
└── Return vanHan[]
```

### 2.8 PhuongMen Calculation

```
START: Calculate PhuongMen
│
├── Input: menhElement = "Thổ"
│
├── Xác định tương tác Ngũ Hành:
│   │
│   ├── Hành của Mệnh: Thổ
│   │
│   ├── Hành Tương Sinh: Kim (Thổ sinh Kim)
│   │
│   ├── Hành Tương Khắc: Mộc (Mộc khắc Thổ)
│   │
│   ├── Hành Bất Lợi: Mộc, Hỏa (Hỏa khắc Kim, Mộc khắc Thổ)
│   │
│   └── Hành Có Lợi: Kim, Thủy (Kim hỗ trợ Thổ, Thủy nuôi Thổ)
│
├── Xác định Hướng:
│   │
│   └── Thổ: Tây Nam, Đông Bắc, Nam, Bắc
│       │
│       ├── Hướng Tốt: Tây Nam, Đông Bắc
│       └── Hướng Xấu: Đông, Tây
│
├── Xác định Màu Sắc:
│   │
│   └── Thổ: Vàng, Nâu, Cam
│       │
│       ├── Màu Tốt: Vàng, Nâu
│       └── Màu Xấu: Xanh lá, Đỏ
│
├── Xác định Con Số:
│   │
│   └── Thổ: 2, 5, 8
│       │
│       ├── Số May Mắn: 5, 8
│       └── Số Kém: 3, 4
│
└── Return phuongMen: {
    menhElement: "Thổ",
    favorableElements: ["Kim", "Thủy"],
    unfavorableElements: ["Mộc", "Hỏa"],
    favorableDirections: ["Tây Nam", "Đông Bắc", "Nam", "Bắc"],
    unfavorableDirections: ["Đông", "Tây"],
    favorableColors: ["Vàng", "Nâu"],
    unfavorableColors: ["Xanh lá", "Đỏ"],
    luckyNumbers: [5, 8]
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
│   │   └── Specific error?
│   │       ├── INVALID_DATE → 400: "Ngày sinh không hợp lệ"
│   │       ├── INVALID_TIME → 400: "Giờ sinh không hợp lệ"
│   │       ├── INVALID_TIMEZONE → 400: "Múi giờ không hợp lệ"
│   │       ├── INVALID_GENDER → 400: "Giới tính không hợp lệ"
│   │       ├── FUTURE_DATE → 400: "Ngày sinh không thể là tương lai"
│   │       └── OLD_DATE → 400: "Ngày sinh quá cũ"
│   │
│   └── Return 400 Bad Request
│
├── Error Type = LUNAR_CONVERSION_ERROR?
│   │
│   ├── CÓ
│   │   │
│   │   └── Retry?
│   │       ├── CÓ → Retry với exponential backoff
│   │       └── KHÔNG → Return 422
│   │
│   └── Return 422 Unprocessable Entity
│
├── Error Type = NOT_FOUND?
│   │
│   └── Return 404 Not Found
│
├── Error Type = UNAUTHORIZED?
│   │
│   └── Return 401/403 Unauthorized/Forbidden
│
├── Error Type = RATE_LIMIT?
│   │
│   └── Return 429 Too Many Requests
│
└── Error Type = INTERNAL_ERROR?
    │
    └── Return 500 Internal Server Error
```
