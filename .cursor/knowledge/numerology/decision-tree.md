# Decision Tree cho Hệ Thống Numerology

## 1. Decision Tree Tổng Quan

```
┌─────────────────────────────────────────────────────────────────┐
│                  BẮT ĐẦU: Tính Numerology                        │
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
│    │ - fullName (>= 2 ký tự, <= 200)         │                  │
│    │ - birthDate (YYYY-MM-DD)                │                  │
│    │ - system (pythagorean/chaldean)         │                  │
│    └──────────────────────┬──────────────────┘                  │
│                           │                                     │
│         ┌─────────────────┴─────────────────┐                │
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
│ 2. NORMALIZE TÊN                                                │
│                                                                 │
│ Câu hỏi: Xử lý tên như thế nào?                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Bước 1: Xóa Vietnamese diacritics                               │
│   Ễ → E, Ộ → O, Ủ → U, ...                                     │
│                                                                 │
│ Bước 2: Viết hoa                                               │
│   nguyen van a → NGUYEN VAN A                                   │
│                                                                 │
│ Bước 3: Loại bỏ ký tự không phải chữ cái                       │
│   NGUYEN VAN A → NGUYENVANA                                     │
│                                                                 │
│ Bước 4: Tách thành các phần                                      │
│   First name, Middle names, Last name                          │
│                                                                 │
│                           ▼                                     │
│    ┌─────────────────────────────────────────┐                  │
│    │ normalizedName: "NGUYENVANA"            │                  │
│    │ parts: { first, middle[], last }        │                  │
│    └─────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. CHỌN HỆ THỐNG TÍNH                                           │
│                                                                 │
│ Câu hỏi: Sử dụng hệ thống nào?                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ PYTHAGOREAN                                                 │ │
│ │                                                             │ │
│ │ A=1, B=2, C=3, D=4, E=5, F=6, G=7, H=8, I=9                │ │
│ │ J=1, K=2, L=3, M=4, N=5, O=6, P=7, Q=8, R=9                │ │
│ │ S=1, T=2, U=3, V=4, W=5, X=6, Y=7, Z=8                     │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ CHALDEAN                                                    │ │
│ │                                                             │ │
│ │ A=1, B=2, C=3, D=4, E=5, U=6, O=7, F=8                     │ │
│ │ I=9, Y=1, J=1, K=2, L=3, M=4, N=5, X=6                     │ │
│ │ G=7, H=8, Z=8, P=8, Q=1, R=2, S=3, T=4                     │ │
│ │ V=6, W=6, D=4                                               │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. TÍNH LIFE PATH NUMBER                                        │
│                                                                 │
│ Câu hỏi: Tính Life Path từ ngày sinh?                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Ví dụ: birthDate = "1990-05-15"                               │
│                                                                 │
│ Bước 1: Tách ngày sinh                                         │
│   day = 15, month = 5, year = 1990                              │
│                                                                 │
│ Bước 2: Cộng tất cả các chữ số                                 │
│   1 + 9 + 9 + 0 + 0 + 5 + 1 + 5 = 30                          │
│                                                                 │
│ Bước 3: Giảm số                                                │
│   30 → 3 + 0 = 3                                               │
│                                                                 │
│ Bước 4: Kiểm tra Master Number                                 │
│   3 (không phải 11, 22, 33) → Giữ nguyên                       │
│                                                                 │
│                           ▼                                     │
│    ┌─────────────────────────────────────────┐                  │
│    │ Life Path Number = 3                    │                  │
│    │ isMasterNumber = false                  │                  │
│    └─────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. TÍNH EXPRESSION NUMBER                                        │
│                                                                 │
│ Câu hỏi: Tính Expression từ tên?                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Ví dụ: name = "KATE" (Pythagorean)                            │
│                                                                 │
│ Bước 1: Gán giá trị cho mỗi chữ cái                            │
│   K=2, A=1, T=2, E=5                                           │
│                                                                 │
│ Bước 2: Cộng tổng                                             │
│   2 + 1 + 2 + 5 = 10                                           │
│                                                                 │
│ Bước 3: Giảm số                                                │
│   10 → 1 + 0 = 1                                               │
│                                                                 │
│ Bước 4: Kiểm tra Master Number                                 │
│   1 (không phải 11, 22, 33) → Giữ nguyên                       │
│                                                                 │
│                           ▼                                     │
│    ┌─────────────────────────────────────────┐                  │
│    │ Expression Number = 1                   │                  │
│    │ isMasterNumber = false                  │                  │
│    └─────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. TÍNH SOUL URGE NUMBER                                         │
│                                                                 │
│ Câu hỏi: Tính Soul Urge từ nguyên âm?                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Nguyên âm: A, E, I, O, U, Y                                    │
│                                                                 │
│ Ví dụ: name = "KATE"                                           │
│                                                                 │
│ Bước 1: Lọc chỉ lấy nguyên âm                                   │
│   K (phụ âm) → Bỏ                                             │
│   A (nguyên âm) → Lấy, A=1                                    │
│   T (phụ âm) → Bỏ                                             │
│   E (nguyên âm) → Lấy, E=5                                     │
│                                                                 │
│ Bước 2: Cộng tổng                                             │
│   1 + 5 = 6                                                     │
│                                                                 │
│ Bước 3: Giảm số (nếu cần)                                      │
│   6 ≤ 9 → Giữ nguyên                                           │
│                                                                 │
│                           ▼                                     │
│    ┌─────────────────────────────────────────┐                  │
│    │ Soul Urge Number = 6                    │                  │
│    │ isMasterNumber = false                  │                  │
│    └─────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. TÍNH PERSONALITY NUMBER                                      │
│                                                                 │
│ Câu hỏi: Tính Personality từ phụ âm?                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Phụ âm: Tất cả chữ cái không phải nguyên âm                    │
│                                                                 │
│ Ví dụ: name = "KATE"                                           │
│                                                                 │
│ Bước 1: Lọc chỉ lấy phụ âm                                     │
│   K (phụ âm) → Lấy, K=2                                        │
│   A (nguyên âm) → Bỏ                                           │
│   T (phụ âm) → Lấy, T=2                                        │
│   E (nguyên âm) → Bỏ                                           │
│                                                                 │
│ Bước 2: Cộng tổng                                             │
│   2 + 2 = 4                                                     │
│                                                                 │
│ Bước 3: Giảm số (nếu cần)                                      │
│   4 ≤ 9 → Giữ nguyên                                           │
│                                                                 │
│                           ▼                                     │
│    ┌─────────────────────────────────────────┐                  │
│    │ Personality Number = 4                  │                  │
│    │ isMasterNumber = false                  │                  │
│    └─────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. TÍNH BIRTHDAY NUMBER                                          │
│                                                                 │
│ Câu hỏi: Tính Birthday từ ngày sinh?                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Ví dụ: birthDate = "1990-05-15"                               │
│                                                                 │
│ Bước 1: Lấy ngày sinh                                          │
│   day = 15                                                       │
│                                                                 │
│ Bước 2: Giảm số (nếu > 9 và không phải Master)                │
│   15 → 1 + 5 = 6                                               │
│   6 ≤ 9 → Giữ nguyên                                           │
│                                                                 │
│                           ▼                                     │
│    ┌─────────────────────────────────────────┐                  │
│    │ Birthday Number = 6                     │                  │
│    │ (điểm nhấn đặc biệt)                   │                  │
│    └─────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 9. TÍNH LIFE CYCLES                                             │
│                                                                 │
│ Câu hỏi: Tính các chu kỳ sống?                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Ví dụ: birthDate = "15/05/1990"                               │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ FIRST CYCLE                                                  │ │
│ │                                                             │ │
│ │ Số = Month + Day                                            │ │
│ │ = 5 + 15 = 20 → 2 + 0 = 2                                  │ │
│ │                                                             │ │
│ │ Độ dài = ~27-36 năm (từ sinh)                             │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ SECOND CYCLE                                                 │ │
│ │                                                             │ │
│ │ Số = Day + Year digits                                      │ │
│ │ = 15 + (1+9+9+0) = 15 + 19 = 34 → 3 + 4 = 7               │ │
│ │                                                             │ │
│ │ Độ dài = ~9 năm                                            │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ THIRD CYCLE                                                  │ │
│ │                                                             │ │
│ │ Số = Month + Year digits                                    │ │
│ │ = 5 + 19 = 24 → 2 + 4 = 6                                  │ │
│ │                                                             │ │
│ │ Độ dài = Phần còn lại của cuộc đời                        │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 10. TÍNH PINNACLE NUMBERS                                        │
│                                                                 │
│ Câu hỏi: Tính các đỉnh cao?                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Ví dụ: birthDate = "15/05/1990"                               │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ FIRST PINNACLE                                              │ │
│ │ = Day + Month = 15 + 5 = 20 → 2                            │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ SECOND PINNACLE                                             │ │
│ │ = Day + Year = 15 + 1+9+9+0 = 34 → 7                       │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ THIRD PINNACLE                                              │ │
│ │ = First + Second = 2 + 7 = 9                               │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ FOURTH PINNACLE                                             │ │
│ │ = Month + Year = 5 + 1+9+9+0 = 24 → 6                     │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 11. TRA CỨU Ý NGHĨA CÁC SỐ                                       │
│                                                                 │
│ Câu hỏi: Lấy ý nghĩa của các số?                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ SINGLE DIGITS (1-9)                                         │ │
│ │                                                             │ │
│ │ 1: Leadership, Independence                                 │ │
│ │ 2: Cooperation, Diplomacy                                  │ │
│ │ 3: Expression, Creativity                                  │ │
│ │ 4: Stability, Hard work                                    │ │
│ │ 5: Freedom, Change                                         │ │
│ │ 6: Responsibility, Harmony                                 │ │
│ │ 7: Analysis, Spirituality                                  │ │
│ │ 8: Authority, Success                                      │ │
│ │ 9: Humanitarianism, Completion                            │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ MASTER NUMBERS (11, 22, 33)                                │ │
│ │                                                             │ │
│ │ 11: Intuition, Vision (Master of Intuition)               │ │
│ │ 22: Master Builder (Large scale achievement)              │ │
│ │ 33: Master Teacher (Spiritual teaching)                  │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│ 12. TẠO NUMEROLOGY CHART                                        │
│                                                                 │
│ Kết hợp tất cả thông tin:                                       │
│                                                                 │
│   {                                                            │
│     id: "uuid",                                                │
│     fullName: "Nguyen Van A",                                  │
│     birthDate: "1990-05-15",                                   │
│     numbers: {                                                 │
│       lifePath: 3,                                             │
│       expression: 1,                                          │
│       soulUrge: 6,                                             │
│       personality: 4,                                         │
│       birthday: 6                                             │
│     },                                                         │
│     lifeCycles: {                                              │
│       first: { number: 2, ageEnd: 35 },                       │
│       second: { number: 7, ageEnd: 44 },                     │
│       third: { number: 6, ageEnd: null }                      │
│     },                                                         │
│     pinnacleNumbers: [2, 7, 9, 6],                            │
│     createdAt: "2024-01-01"                                   │
│   }                                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                         KẾT THÚC                                │
│                                                                 │
│ Output: NumerologyChart với đầy đủ:                            │
│         - Life Path Number                                      │
│         - Expression Number                                     │
│         - Soul Urge Number                                      │
│         - Personality Number                                    │
│         - Birthday Number                                       │
│         - Life Cycles                                           │
│         - Pinnacle Numbers                                      │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Decision Tree Chi Tiết

### 2.1 Validate Input

```
START: Validate Input
│
├── fullName validation
│   ├── Kiểm tra không rỗng
│   ├── Kiểm tra độ dài >= 2
│   ├── Kiểm tra độ dài <= 200
│   └── Kiểm tra không chứa số
│       ├── CÓ số → ERROR: NAME_CONTAINS_DIGITS
│       └── KHÔNG → Tiếp tục
│
├── birthDate validation
│   ├── Kiểm tra không rỗng
│   ├── Kiểm tra format hợp lệ (YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY)
│   │   ├── Format không hợp lệ → ERROR: INVALID_DATE_FORMAT
│   │   └── Format hợp lệ
│   │
│   ├── Kiểm tra ngày hợp lệ
│   │   ├── Ngày không tồn tại (VD: 31/02) → ERROR: INVALID_DATE
│   │   └── Ngày hợp lệ
│   │
│   ├── Kiểm tra không trong tương lai
│   │   ├── Ngày > hôm nay → ERROR: FUTURE_DATE
│   │   └── Ngày <= hôm nay
│   │
│   └── Kiểm tra không quá cũ
│       ├── Ngày < 1900-01-01 → ERROR: DATE_TOO_OLD
│       └── Ngày >= 1900-01-01 → Tiếp tục
│
├── system validation
│   ├── system in ['pythagorean', 'chaldean']?
│   │   ├── KHÔNG → ERROR: INVALID_SYSTEM
│   │   └── CÓ → Tiếp tục
│   │
│   └── Default: 'pythagorean'
│
└── VALIDATION_PASSED
```

### 2.2 Calculate Life Path

```
START: Calculate Life Path
│
├── Input: birthDate = "1990-05-15"
│
├── Parse ngày sinh
│   ├── day = 15
│   ├── month = 5
│   └── year = 1990
│
├── Format thành chuỗi số
│   └── dateStr = "19900515"
│
├── Tách thành các chữ số
│   └── digits = ["1", "9", "9", "0", "0", "5", "1", "5"]
│
├── Cộng tổng
│   └── sum = 1+9+9+0+0+5+1+5 = 30
│
├── Reduce
│   │
│   ├── sum = 30 > 9?
│   │   ├── CÓ
│   │   │   │
│   │   │   └── sum = 3 + 0 = 3
│   │   │
│   │   └── sum = 3 <= 9?
│   │       ├── CÓ
│   │       │   │
│   │       │   └── result = 3
│   │       │
│   │       └── KHÔNG (tiếp tục reduce)
│   │
│   └── Check Master Number
│       ├── result in [11, 22, 33]?
│       │   ├── CÓ → isMaster = true
│       │   └── KHÔNG → isMaster = false
│       │
│       └── result = 3 (không phải Master)
│
└── Return: { value: 3, isMaster: false }
```

### 2.3 Calculate Expression Number

```
START: Calculate Expression Number
│
├── Input: name = "KATE", system = "pythagorean"
│
├── Normalize tên
│   └── "KATE"
│
├── Lấy giá trị từ bảng Pythagorean
│   │
│   ├── K = 2
│   ├── A = 1
│   ├── T = 2
│   └── E = 5
│
├── Cộng tổng
│   └── sum = 2 + 1 + 2 + 5 = 10
│
├── Reduce
│   │
│   ├── sum = 10 > 9?
│   │   ├── CÓ
│   │   │   │
│   │   │   └── sum = 1 + 0 = 1
│   │   │
│   │   └── sum = 1 <= 9?
│   │       ├── CÓ
│   │       │   │
│   │       │   └── result = 1
│   │       │
│   │       └── KHÔNG (tiếp tục)
│   │
│   └── Check Master Number
│       └── result = 1 (không phải Master)
│
└── Return: { value: 1, isMaster: false }
```

### 2.4 Calculate Soul Urge Number

```
START: Calculate Soul Urge Number
│
├── Input: name = "KATE"
│
├── Define Vowels
│   └── vowels = ["A", "E", "I", "O", "U", "Y"]
│
├── Lọc chỉ nguyên âm
│   │
│   ├── K = phụ âm → Bỏ
│   ├── A = nguyên âm → Lấy, value = 1
│   ├── T = phụ âm → Bỏ
│   └── E = nguyên âm → Lấy, value = 5
│
├── Cộng tổng
│   └── sum = 1 + 5 = 6
│
├── Reduce
│   │
│   ├── sum = 6 <= 9?
│   │   ├── CÓ
│   │   │   │
│   │   │   └── result = 6
│   │   │
│   │   └── KHÔNG (tiếp tục)
│   │
│   └── Check Master Number
│       └── result = 6 (không phải Master)
│
└── Return: { value: 6, isMaster: false }
```

### 2.5 Calculate Life Cycles

```
START: Calculate Life Cycles
│
├── Input: birthDate = "15/05/1990"
│   ├── day = 15
│   ├── month = 5
│   └── year = 1990
│
├── First Cycle
│   │
│   ├── Formula: month + day
│   ├── = 5 + 15 = 20
│   ├── Reduce: 20 → 2 + 0 = 2
│   ├── Duration: ~27-36 năm
│   │
│   └── First Cycle = { number: 2, duration: 36, ageEnd: 36 }
│
├── Second Cycle
│   │
│   ├── Formula: sum of year digits + day
│   ├── yearDigits = 1 + 9 + 9 + 0 = 19
│   ├── = 19 + 15 = 34
│   ├── Reduce: 34 → 3 + 4 = 7
│   ├── Duration: 9 năm
│   │
│   └── Second Cycle = { number: 7, duration: 9, ageEnd: 45 }
│
├── Third Cycle
│   │
│   ├── Formula: month + yearDigits
│   ├── = 5 + 19 = 24
│   ├── Reduce: 24 → 2 + 4 = 6
│   ├── Duration: Phần còn lại
│   │
│   └── Third Cycle = { number: 6, ageEnd: null }
│
└── Return: { first: {...}, second: {...}, third: {...} }
```

### 2.6 Calculate Pinnacles

```
START: Calculate Pinnacles
│
├── Input: birthDate = "15/05/1990"
│   ├── day = 15
│   ├── month = 5
│   └── yearDigits = 1 + 9 + 9 + 0 = 19
│
├── First Pinnacle
│   │
│   ├── Formula: day + month
│   ├── = 15 + 5 = 20
│   ├── Reduce: 20 → 2 + 0 = 2
│   │
│   └── First Pinnacle = 2
│
├── Second Pinnacle
│   │
│   ├── Formula: day + yearDigits
│   ├── = 15 + 19 = 34
│   ├── Reduce: 34 → 3 + 4 = 7
│   │
│   └── Second Pinnacle = 7
│
├── Third Pinnacle
│   │
│   ├── Formula: First + Second
│   ├── = 2 + 7 = 9
│   │
│   └── Third Pinnacle = 9
│
├── Fourth Pinnacle
│   │
│   ├── Formula: month + yearDigits
│   ├── = 5 + 19 = 24
│   ├── Reduce: 24 → 2 + 4 = 6
│   │
│   └── Fourth Pinnacle = 6
│
└── Return: [2, 7, 9, 6]
```

### 2.7 Get Number Meaning

```
START: Get Number Meaning
│
├── Input: number = 3
│
├── Check if Master Number
│   ├── number in [11, 22, 33]?
│   │   ├── CÓ → Return Master Number meaning
│   │   │   ├── 11 → "Người có tầm nhìn, trực giác mạnh"
│   │   │   ├── 22 → "Người xây dựng vĩ đại, thực tiễn"
│   │   │   └── 33 → "Người thầy vĩ đại, phụng sự"
│   │   │
│   │   └── KHÔNG → Continue
│   │
│   └── Return single digit meaning
│       │
│       ├── 1 → "Người khởi đầu, lãnh đạo, độc lập"
│       ├── 2 → "Người hòa giải, ngoại giao, hợp tác"
│       ├── 3 → "Người sáng tạo, giao tiếp, biểu đạt"
│       ├── 4 → "Người xây dựng, ổn định, chăm chỉ"
│       ├── 5 → "Người tự do, thay đổi, phiêu lưu"
│       ├── 6 → "Người nuôi dưỡng, trách nhiệm, hài hòa"
│       ├── 7 → "Người phân tích, tâm linh, nội tâm"
│       ├── 8 → "Người quyền lực, thành công, thẩm quyền"
│       └── 9 → "Người nhân đạo, hoàn thành, trí tuệ"
│
└── Return: { meaning, strengths, challenges, compatibleWith, career }
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
│   │       ├── NAME_TOO_SHORT → "Tên phải có ít nhất 2 ký tự"
│   │       ├── NAME_TOO_LONG → "Tên không được quá 200 ký tự"
│   │       ├── NAME_CONTAINS_DIGITS → "Tên không được chứa số"
│   │       ├── INVALID_DATE_FORMAT → "Định dạng ngày sinh không hợp lệ"
│   │       ├── INVALID_DATE → "Ngày sinh không tồn tại"
│   │       ├── FUTURE_DATE → "Ngày sinh không thể là tương lai"
│   │       ├── DATE_TOO_OLD → "Ngày sinh quá cũ"
│   │       └── INVALID_SYSTEM → "Hệ thống Numerology không hợp lệ"
│   │
│   └── Return 400 Bad Request
│
├── Error Type = NOT_FOUND?
│   │
│   ├── CÓ
│   │   └── Specific error?
│   │       └── CHART_NOT_FOUND → "Không tìm thấy chart"
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
