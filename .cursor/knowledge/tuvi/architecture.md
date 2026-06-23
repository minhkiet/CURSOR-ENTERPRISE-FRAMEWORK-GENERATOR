# Kiến Trúc Hệ Thống Tử Vi

## 1. Tổng Quan Kiến Trúc

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        API Gateway Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  REST API    │  │  GraphQL     │  │  WebSocket (Real-time)│ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                     Business Logic Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ TuviService  │  │ SaoService   │  │   VanHanService      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  CungService │  │PhuongMenSvc  │  │   GieoQueService     │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                       Data Access Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Repository  │  │   Cache      │  │   Lookup Tables       │ │
│  │  Pattern     │  │  (Redis)     │  │   (Sao, Cung, Vận)   │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                        Storage Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  PostgreSQL   │  │    Redis     │  │   File Storage       │ │
│  │  (Primary)    │  │  (Cache)     │  │   (Charts, Images)  │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Architecture

```
tuvi-system/
├── src/
│   ├── api/
│   │   ├── controllers/
│   │   │   ├── TuviController.ts
│   │   │   ├── SaoController.ts
│   │   │   └── VanHanController.ts
│   │   ├── routes/
│   │   │   ├── tuviRoutes.ts
│   │   │   └── apiRoutes.ts
│   │   └── middleware/
│   │       ├── auth.ts
│   │       ├── validation.ts
│   │       └── rateLimit.ts
│   ├── services/
│   │   ├── tuvi/
│   │   │   ├── TuviCalculator.ts
│   │   │   ├── SaoService.ts
│   │   │   ├── CungService.ts
│   │   │   ├── VanHanService.ts
│   │   │   ├── PhuongMenService.ts
│   │   │   └── TuviReportGenerator.ts
│   │   └── gieo-que/
│   │       ├── GieoQueService.ts
│   │       └── KinhDuongService.ts
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── TuviChart.ts
│   │   │   ├── Sao.ts
│   │   │   ├── Cung.ts
│   │   │   ├── VanHan.ts
│   │   │   └── PhuongMen.ts
│   │   ├── value-objects/
│   │   │   ├── SaoInfo.ts
│   │   │   ├── CungInfo.ts
│   │   │   └── VanInfo.ts
│   │   └── events/
│   │       ├── ChartCreated.ts
│   │       └── ReportGenerated.ts
│   ├── infrastructure/
│   │   ├── repositories/
│   │   │   ├── TuviRepository.ts
│   │   │   └── UserRepository.ts
│   │   ├── cache/
│   │   │   └── TuviCache.ts
│   │   └── lookup-tables/
│   │       ├── saoTable.ts
│   │       ├── cungTable.ts
│   │       └── vanHanTable.ts
│   └── shared/
│       ├── constants/
│       ├── utils/
│       └── exceptions/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── config/
```

## 2. Data Model

### 2.1 Core Entities

```typescript
// TuviChart Entity
interface TuviChart {
  id: string;
  userId: string;
  
  // Thông tin thời gian
  birthDate: Date;
  birthTime: string;
  timeZone: string;
  gender: Gender;
  lunarDate: LunarDate;
  
  // Mệnh cách (命)
  menhCach: MenhCach;
  
  // 12 Cung
  cungTrung: Cung[];
  
  // Các sao
  saoChinh: Sao[];
  saoPhu: Sao[];
  saoTutan: Sao[];
  
  // Vận hạn
  vanHan: VanHan[];
  
  // Phương Mệnh
  phuongMen: PhuongMen;
  
  // Metadata
  createdAt: Date;
  updatedAt: Date;
  version: number;
}

interface LunarDate {
  day: number;
  month: number;
  year: number;
  isLeapMonth: boolean;
}

interface MenhCach {
  name: string;           // Tên Mệnh (VD: Kim, Mộc, Thủy, Hỏa, Thổ)
  element: Element;       // Ngũ Hành
  can: string;           // Thiên Can
  chi: string;           // Địa Chi
  nichttu: string;       // Nhị Thập Bát Tú
  that: string;          // Thập Thiên Niên
}

interface Cung {
  name: CungName;        // Tên Cung
  stars: Sao[];          // Các sao trong cung
  palace: string;        // Cung điện
  isEmpty: boolean;      // Cung không có sao chính
  occupant: string;      // Sao chiếm cung
  owner: string;        // Sao chủ cung
  element: Element;      // Hành của cung
}

type CungName = 
  | 'Mệnh' | 'Phụ Mẫu' | 'Phúc Đức' | 'Điền Trạch'
  | 'Quan Lộc' | 'Nô Bộc' | 'Thiên Di' | 'Tật Ách'
  | 'Tài Bạch' | 'Tử Tức' | 'Phu Thê' | 'Huỵêt';

interface Sao {
  name: string;          // Tên sao
  type: SaoType;          // Loại sao
  position: CungName;     // Cung vị trí
  brightness: SaoBrightness; // Độ sáng
  isVanChanh: boolean;   // Thuộc Vận hạn
  meanings: string[];     // Ý nghĩa
}

type SaoType = 
  | 'chinh'      // Sao chính
  | 'phu'        // Sao phụ
  | 'tutan'      // Sao tùng tán
  | 'batquat';   // Bát Quái

type SaoBrightness = 
  | 'duong'      // Dương (sáng)
  | 'am'         // Âm (tối)
  | 'trung';     // Trung bình

interface VanHan {
  year: number;          // Năm vận
  age: number;           // Tuổi
  van: VanType;         // Vận (Thiên, Nhân, Địa)
  han: string[];         // Các Hạn
  taiBach: string[];     // Tai Bach
  satSat: string[];      // Sát Sát
  than: string[];        // Thần
  hacDuong: string[];    // Hạc Dương
  lichSu: string;       // Lịch Sử vận
  forecast: string;      // Dự đoán
}

type VanType = 'thien' | 'nhan' | 'dia';

interface PhuongMen {
  tuongTac: TuongTac;     // Tương tác Ngũ Hành
  thienYen: string;      // Thiên Yên
  nghichHai: string;     // Nghịch Hại
  sinhKhach: string;     // Sinh Khắc
  phuongHuong: PhuongHuong; // Phương hướng tốt/xấu
}

interface TuongTac {
  menhElement: Element;
 有利元素: Element[];
 不利元素: Element[];
  recommendation: string;
}
```

### 2.2 Database Schema (PostgreSQL)

```sql
-- Bảng chính lưu trữ Tử Vi
CREATE TABLE tuvi_charts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    
    -- Thông tin sinh
    birth_date DATE NOT NULL,
    birth_time TIME NOT NULL,
    timezone VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    
    -- Dương lịch
    solar_day INT NOT NULL,
    solar_month INT NOT NULL,
    solar_year INT NOT NULL,
    
    -- Âm lịch
    lunar_day INT NOT NULL,
    lunar_month INT NOT NULL,
    lunar_year INT NOT NULL,
    is_leap_month BOOLEAN DEFAULT FALSE,
    
    -- Mệnh cách
    menh_name VARCHAR(50),
    menh_element VARCHAR(10),
    menh_can VARCHAR(2),
    menh_chi VARCHAR(2),
    
    -- Cung Mệnh (vị trí)
    cung_menh_index INT,
    
    -- 12 Cung (JSON)
    cung_data JSONB,
    
    -- Sao chính (JSON)
    sao_chinh JSONB,
    
    -- Sao phụ (JSON)
    sao_phu JSONB,
    
    -- Vận hạn (JSON)
    van_han JSONB,
    
    -- Phương Mệnh (JSON)
    phuong_men JSONB,
    
    -- Metadata
    version INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng Sao
CREATE TABLE sao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL,
    element VARCHAR(10),
    brightness VARCHAR(10),
    meanings TEXT[],
    is_van_chanh BOOLEAN DEFAULT FALSE,
    
    UNIQUE(name)
);

-- Bảng Vận Hạn
CREATE TABLE van_han (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chart_id UUID REFERENCES tuvi_charts(id) ON DELETE CASCADE,
    
    van_type VARCHAR(20) NOT NULL,
    start_year INT NOT NULL,
    end_year INT NOT NULL,
    
    -- Các hạn
    han_data JSONB,
    
    -- Sao Vận
    sao_van JSONB,
    
    -- Lịch Sử
    lich_su TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng Phân Tích
CREATE TABLE tuvi_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chart_id UUID REFERENCES tuvi_charts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    
    -- Tổng quan
    overview TEXT,
    
    -- Chi tiết từng cung
    cung_analyses JSONB,
    
    -- Chi tiết sao
    sao_analyses JSONB,
    
    -- Phương Mệnh
    phuong_men_analysis TEXT,
    
    -- Vận hạn chi tiết
    van_han_analysis TEXT,
    
    -- Recommendations
    recommendations JSONB,
    
    -- Version
    version INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_tuvi_user_id ON tuvi_charts(user_id);
CREATE INDEX idx_tuvi_birth_date ON tuvi_charts(birth_date);
CREATE INDEX idx_tuvi_menh ON tuvi_charts(menh_element);
CREATE INDEX idx_tuvi_lunar ON tuvi_charts(lunar_year, lunar_month, lunar_day);
CREATE INDEX idx_van_han_chart ON van_han(chart_id);
```

## 3. API Design

### 3.1 REST API Endpoints

```
Base URL: /api/v1/tuvi

# Chart Management
POST   /charts                    # Tạo Tử Vi Chart mới
GET    /charts/:id                # Lấy Chart theo ID
GET    /charts/user/:userId       # Lấy tất cả charts của user
PUT    /charts/:id                # Cập nhật chart
DELETE /charts/:id                # Xóa chart

# Analysis Endpoints
GET    /charts/:id/analysis       # Phân tích tổng quát
GET    /charts/:id/cung           # Chi tiết 12 Cung
GET    /charts/:id/sao            # Chi tiết các Sao
GET    /charts/:id/van-han        # Chi tiết Vận Hạn
GET    /charts/:id/phuong-men     # Chi tiết Phương Mệnh
GET    /charts/:id/nam-sinh       # Chi tiết Năm Sinh

# Report Endpoints
GET    /charts/:id/report         # Lấy full report
POST   /charts/:id/report/regenerate # Tạo lại report

# Gieo Quẻ
POST   /que/tu-vi                 # Gieo Quẻ Tử Vi
GET    /que/:queId                # Lấy kết quả quẻ

# Lookup Endpoints
GET    /sao                       # Danh sách tất cả sao
GET    /sao/:saoName              # Chi tiết một sao
GET    /cung                      # Thông tin 12 Cung
GET    /van-han/nam/:year        # Vận hạn theo năm
GET    /menh                      # Thông tin Mệnh cách
```

### 3.2 Request/Response Examples

```typescript
// POST /api/v1/tuvi/charts - Tạo Tử Vi Chart
interface CreateTuviRequest {
  birthDate: string;      // "1990-05-15"
  birthTime: string;      // "14:30"
  timeZone: string;       // "Asia/Ho_Chi_Minh"
  gender: 'male' | 'female';
  name?: string;
}

interface CreateTuviResponse {
  success: boolean;
  data: {
    chart: TuviChart;
    summary: {
      menhCach: string;
      cungMenh: CungName;
      mainStars: string[];
      vanChanh: string;
    };
  };
  meta: {
    calculationTime: number;
    cacheHit: boolean;
  };
}

// GET /api/v1/tuvi/charts/:id/analysis
interface TuviAnalysisResponse {
  success: boolean;
  data: {
    chartId: string;
    
    // Mệnh Cách
    menhCach: MenhCachAnalysis;
    
    // 12 Cung
    cungs: {
      [key in CungName]?: CungAnalysis;
    };
    
    // Sao
    stars: StarAnalysis;
    
    // Vận Hạn
    fortune: FortuneAnalysis;
    
    // Phương Mệnh
    phuongMen: PhuongMenAnalysis;
    
    // Recommendations
    recommendations: Recommendation[];
  };
}
```

## 4. Business Logic

### 4.1 Core Services

```typescript
// TuviCalculator - Service chính tính toán Tử Vi
class TuviCalculator {
  constructor(
    private lunarCalendarService: LunarCalendarService,
    private saoService: SaoService,
    private cungService: CungService,
    private vanHanService: VanHanService
  ) {}

  async calculateTuvi(
    birthDate: Date,
    birthTime: string,
    timeZone: string,
    gender: Gender
  ): Promise<TuviChart> {
    // 1. Chuyển đổi Dương lịch → Âm lịch
    const lunarDate = await this.lunarCalendarService.toLunar(
      birthDate,
      timeZone
    );

    // 2. Xác định Mệnh Cách
    const menhCach = this.calculateMenhCach(lunarDate, gender);

    // 3. Xác định Cung Mệnh
    const cungMenhIndex = this.calculateCungMenh(menhCach.can, gender);

    // 4. Xác định vị trí các Sao
    const saos = this.saoService.calculateSaoPosition(
      lunarDate,
      birthTime,
      cungMenhIndex
    );

    // 5. Xác định 12 Cung
    const cungs = this.cungService.calculateCung(
      cungMenhIndex,
      saos
    );

    // 6. Tính Vận Hạn
    const vanHan = this.vanHanService.calculateVanHan(
      lunarDate.year,
      cungMenhIndex,
      gender
    );

    // 7. Phương Mệnh
    const phuongMen = this.calculatePhuongMen(menhCach, cungs);

    return {
      id: generateUUID(),
      userId: '', // Will be set by controller
      birthDate,
      birthTime,
      timeZone,
      gender,
      lunarDate,
      menhCach,
      cungMenhIndex,
      cungs,
      saos,
      vanHan,
      phuongMen,
      createdAt: new Date(),
      updatedAt: new Date(),
      version: 1
    };
  }

  private calculateMenhCach(lunarDate: LunarDate, gender: Gender): MenhCach {
    // Lấy Ngày Can Chi
    const dayCanChi = this.getDayCanChi(lunarDate);
    
    // Xác định Mệnh dựa vào giới tính và Ngày Can
    const menhTable = this.getMenhTable(gender);
    const menhName = menhTable[dayCanChi.canIndex];
    
    return {
      name: menhName,
      element: this.getElementFromMenh(menhName),
      can: dayCanChi.can,
      chi: dayCanChi.chi,
      nichttu: this.getNhiThapBatTu(lunarDate),
      that: this.getThat(lunarDate.year)
    };
  }

  private calculateCungMenh(dayCan: string, gender: Gender): number {
    // Bảng xác định Cung Mệnh (Nam/Nữ khác nhau)
    const cungMenhTable = {
      male: {
        'Giáp': 0, 'Kỷ': 0,     // Mệnh
        'Ất': 1, 'Canh': 1,     // Phụ Mẫu
        'Bính': 2, 'Tân': 2,    // Phúc Đức
        'Đinh': 3, 'Nhâm': 3,   // Điền Trạch
        'Mậu': 4, 'Quý': 4      // Quan Lộc
      },
      female: {
        'Giáp': 4, 'Kỷ': 4,     // Quan Lộc
        'Ất': 3, 'Canh': 3,     // Điền Trạch
        'Bính': 2, 'Tân': 2,    // Phúc Đức
        'Đinh': 1, 'Nhâm': 1,   // Phụ Mẫu
        'Mậu': 0, 'Quý': 0      // Mệnh
      }
    };
    
    return cungMenhTable[gender][dayCan] ?? 0;
  }
}

// SaoService - Service xác định vị trí các Sao
class SaoService {
  private readonly SAO_TABLE = {
    // Các sao theo thứ tự trong cung
    // Format: [canIndex][chiIndex] = [danhSachSao]
  };

  calculateSaoPosition(
    lunarDate: LunarDate,
    birthTime: string,
    cungMenhIndex: number
  ): SaoPositionResult {
    // 1. Xác định vị trí Sao theo Ngày
    const dayPosition = this.getDayPosition(lunarDate);
    
    // 2. Xác định vị trí Sao theo Tháng
    const monthPosition = this.getMonthPosition(lunarDate.month);
    
    // 3. Xác định vị trí Sao theo Năm
    const yearPosition = this.getYearPosition(lunarDate.year);
    
    // 4. Xác định vị trí Sao theo Giờ
    const hourPosition = this.getHourPosition(birthTime);
    
    // 5. Kết hợp và sắp xếp vào 12 Cung
    return this.arrangeStars(
      dayPosition,
      monthPosition,
      yearPosition,
      hourPosition,
      cungMenhIndex
    );
  }

  private arrangeStars(
    dayStars: Sao[],
    monthStars: Sao[],
    yearStars: Sao[],
    hourStars: Sao[],
    cungMenhIndex: number
  ): SaoPositionResult {
    // 12 Cung xoay ngược chiều kim đồng hồ từ Cung Mệnh
    const cungs: CungName[] = [
      'Mệnh', 'Phụ Mẫu', 'Phúc Đức', 'Điền Trạch',
      'Quan Lộc', 'Nô Bộc', 'Thiên Di', 'Tật Ách',
      'Tài Bạch', 'Tử Tức', 'Phu Thê', 'Huỵệt'
    ];
    
    // Bắt đầu từ Cung Mệnh, xoay ngược
    const startIndex = cungMenhIndex;
    
    // Sắp xếp Sao vào các Cung
    const cungStars: Record<CungName, Sao[]> = {} as any;
    
    for (let i = 0; i < 12; i++) {
      const cungIndex = (startIndex + i) % 12;
      const cungName = cungs[cungIndex];
      
      cungStars[cungName] = [
        ...this.getStarsForCung(dayStars, i, 'ngay'),
        ...this.getStarsForCung(monthStars, i, 'thang'),
        ...this.getStarsForCung(yearStars, i, 'nam'),
        ...this.getStarsForCung(hourStars, i, 'gio')
      ];
    }
    
    return {
      cungStars,
      allStars: [...dayStars, ...monthStars, ...yearStars, ...hourStars]
    };
  }
}

// CungService - Service xử lý 12 Cung
class CungService {
  calculateCung(
    cungMenhIndex: number,
    saoPositions: SaoPositionResult
  ): Cung[] {
    const cungNames: CungName[] = [
      'Mệnh', 'Phụ Mẫu', 'Phúc Đức', 'Điền Trạch',
      'Quan Lộc', 'Nô Bộc', 'Thiên Di', 'Tật Ách',
      'Tài Bạch', 'Tử Tức', 'Phu Thê', 'Huỵệt'
    ];
    
    return cungNames.map((name, index) => {
      const stars = saoPositions.cungStars[name] || [];
      const isEmpty = this.isCungEmpty(stars);
      
      return {
        name,
        index,
        stars,
        isEmpty,
        occupant: this.getOccupantStar(stars),
        owner: this.getOwnerStar(name),
        element: this.getCungElement(name),
        position: (index - cungMenhIndex + 12) % 12
      };
    });
  }

  private isCungEmpty(stars: Sao[]): boolean {
    // Cung trống = không có Sao chính
    return !stars.some(s => s.type === 'chinh');
  }
}

// VanHanService - Service tính Vận Hạn
class VanHanService {
  calculateVanHan(
    birthYear: number,
    cungMenhIndex: number,
    gender: Gender
  ): VanHan[] {
    const vanHans: VanHan[] = [];
    const currentYear = new Date().getFullYear();
    
    // Tính Vận từ năm sinh
    for (let age = 0; age <= 120; age += 10) {
      const year = birthYear + age;
      if (year > currentYear + 10) break;
      
      const vanType = this.getVanType(age);
      const han = this.calculateHan(year, cungMenhIndex, gender);
      const lichSu = this.getLichSuVan(age, gender);
      
      vanHans.push({
        year,
        age,
        van: vanType,
        han: han.hans,
        taiBach: han.taiBach,
        satSat: han.satSat,
        than: han.than,
        hacDuong: han.hacDuong,
        lichSu,
        forecast: this.generateForecast(han)
      });
    }
    
    return vanHans;
  }

  private getVanType(age: number): VanType {
    if (age < 40) return 'thien';
    if (age < 80) return 'nhan';
    return 'dia';
  }
}
```

## 5. Lookup Tables

### 5.1 Sao Table (Các Sao trong Tử Vi)

```typescript
// Sao Chính
const SAO_CHINH = {
  // Nhập cung theo Ngày
  ngay: [
    { name: 'Tử Vi', element: 'Thổ', brightness: 'duong' },
    { name: 'Thiên Cơ', element: 'Mộc', brightness: 'am' },
    // ... thêm các sao
  ],
  
  // Nhập cung theo Tháng
  thang: [
    { name: 'Lưu Niên', element: 'Thổ', brightness: 'trung' },
    // ... thêm các sao
  ],
  
  // Nhập cung theo Năm
  nam: [
    { name: 'Thái Dương', element: 'Hỏa', brightness: 'duong' },
    // ... thêm các sao
  ],
  
  // Nhập cung theo Giờ
  gio: [
    { name: 'Thái Âm', element: 'Thủy', brightness: 'am' },
    // ... thêm các sao
  ]
};

// Sao Phụ
const SAO_PHU = [
  { name: 'Văn Xương', element: 'Kim', brightness: 'duong' },
  { name: 'Văn Khúc', element: 'Mộc', brightness: 'am' },
  { name: 'Tả Phụ', element: 'Mộc', brightness: 'duong' },
  { name: 'Hữu Bật', element: 'Mộc', brightness: 'duong' },
  { name: 'Tam Thai', element: 'Thổ', brightness: 'trung' },
  { name: 'Bát Tọa', element: 'Thổ', brightness: 'trung' },
  // ... thêm các sao phụ
];

// Bát Quái
const BAT_QUAI = [
  { name: 'Tứ Quái', element: 'Mộc', brightness: 'trung' },
  { name: 'Ngũ Quái', element: 'Thổ', brightness: 'trung' },
  // ... thêm các sao bát quái
];
```

### 5.2 Cung Table

```typescript
const CUNG_INFO = {
  'Mệnh': {
    description: 'Cung Mệnh là cung quan trọng nhất, thể hiện bản chất con người',
    meaning: 'Tính cách, vận mệnh, cuộc sống',
    strengths: ['Bản thân', 'Sức khỏe', 'Tính cách'],
    weaknesses: ['Tuổi thọ', 'Vận may']
  },
  'Phụ Mẫu': {
    description: 'Cung Phụ Mẫu thể hiện quan hệ với cha mẹ',
    meaning: 'Cha mẹ, tổ tiên, gia đình nội',
    // ...
  },
  'Phúc Đức': {
    description: 'Cung Phúc Đức thể hiện phúc khí và đức hạnh',
    meaning: 'Phúc lộc, đức hạnh, danh tiếng',
    // ...
  },
  'Điền Trạch': {
    description: 'Cung Điền Trạch liên quan đến nhà cửa, đất đai',
    meaning: 'Nhà ở, đất đai, tài sản cố định',
    // ...
  },
  'Quan Lộc': {
    description: 'Cung Quan Lộc thể hiện sự nghiệp và công danh',
    meaning: 'Công việc, sự nghiệp, địa vị',
    // ...
  },
  'Nô Bộc': {
    description: 'Cung Nô Bộc liên quan đến quan hệ xã hội',
    meaning: 'Bạn bè, đồng nghiệp, cấp dưới',
    // ...
  },
  'Thiên Di': {
    description: 'Cung Thiên Di thể hiện du lịch và giao tiếp',
    meaning: 'Di chuyển, giao tiếp, học hành',
    // ...
  },
  'Tật Ách': {
    description: 'Cung Tật Ách liên quan đến bệnh tật và rủi ro',
    meaning: 'Bệnh tật, tai họa, rủi ro',
    // ...
  },
  'Tài Bạch': {
    description: 'Cung Tài Bạch liên quan đến tài lộc và tiền bạc',
    meaning: 'Tài lộc, thu nhập, kinh doanh',
    // ...
  },
  'Tử Tức': {
    description: 'Cung Tử Tức liên quan đến con cái',
    meaning: 'Con cái, hậu duệ, học hành',
    // ...
  },
  'Phu Thê': {
    description: 'Cung Phu Thê liên quan đến hôn nhân và tình yêu',
    meaning: 'Vợ chồng, tình duyên, hôn nhân',
    // ...
  },
  'Huỵệt': {
    description: 'Cung Huỵệt liên quan đến sức khỏe và bệnh tật',
    meaning: 'Sức khỏe, bệnh tật, y tế',
    // ...
  }
};
```

## 6. Caching Strategy

```typescript
interface TuviCacheStrategy {
  keys: {
    chart: 'tuvi:chart:{id}',
    userCharts: 'tuvi:user:{userId}:charts',
    analysis: 'tuvi:analysis:{chartId}',
    saoPosition: 'tuvi:sao:{ngayIndex}:{thangIndex}:{gioIndex}',
    vanHan: 'tuvi:van:{birthYear}:{cungIndex}'
  };

  ttl: {
    chartData: 86400,      // 24 hours
    analysis: 43200,       // 12 hours
    saoPosition: 604800,   // 7 days
    vanHan: 2592000        // 30 days
  };
}
```

## 7. Error Handling

```typescript
class TuviException extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'TuviException';
  }
}

class InvalidBirthDateException extends TuviException {
  constructor(date: string) {
    super(`Ngày sinh không hợp lệ: ${date}`, 'INVALID_BIRTH_DATE', 400);
  }
}

class InvalidGenderException extends TuviException {
  constructor() {
    super('Giới tính phải là "male" hoặc "female"', 'INVALID_GENDER', 400);
  }
}

class ChartNotFoundException extends TuviException {
  constructor(chartId: string) {
    super(`Không tìm thấy Tử Vi chart: ${chartId}`, 'CHART_NOT_FOUND', 404);
  }
}
```
