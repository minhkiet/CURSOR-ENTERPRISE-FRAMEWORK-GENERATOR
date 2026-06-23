# Kiến Trúc Hệ Thống Bazi

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
│  │  BaziService │  │ CungMenhSvc  │  │   NapAmService       │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  PhuongMenSvc │  │ ThaiDuyenSvc │  │   LyHoaService       │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                       Data Access Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Repository  │  │   Cache      │  │   External APIs       │  │
│  │  Pattern     │  │  (Redis)     │  │   (LichViet, etc.)    │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                        Storage Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  PostgreSQL   │  │    Redis     │  │   Object Storage     │  │
│  │  (Primary)    │  │  (Cache)     │  │   (Charts, Reports)  │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Architecture

```
bazi-system/
├── src/
│   ├── api/
│   │   ├── controllers/
│   │   │   ├── BaziController.ts
│   │   │   ├── CungMenhController.ts
│   │   │   └── NapAmController.ts
│   │   ├── routes/
│   │   │   ├── baziRoutes.ts
│   │   │   └── apiRoutes.ts
│   │   └── middleware/
│   │       ├── auth.ts
│   │       ├── validation.ts
│   │       └── rateLimit.ts
│   ├── services/
│   │   ├── bazi/
│   │   │   ├── BaziCalculator.ts
│   │   │   ├── BaziInterpreter.ts
│   │   │   ├── BaziReportGenerator.ts
│   │   │   └── BaziCacheService.ts
│   │   ├── cung-menh/
│   │   │   ├── CungMenhCalculator.ts
│   │   │   ├── NgayHoangDao.ts
│   │   │   └── GioHoangDao.ts
│   │   └── nap-am/
│   │       ├── NapAmCalculator.ts
│   │       ├── AmDongNguyen.ts
│   │       └── AmDongTay.ts
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── BaziChart.ts
│   │   │   ├── BaziElement.ts
│   │   │   ├── BaziRelation.ts
│   │   │   └── CungMenh.ts
│   │   ├── value-objects/
│   │   │   ├── CanChi.ts
│   │   │   ├── NgũHành.ts
│   │   │   └── NapAm.ts
│   │   └── events/
│   │       ├── BaziCalculated.ts
│   │       └── ReportGenerated.ts
│   ├── infrastructure/
│   │   ├── repositories/
│   │   │   ├── BaziRepository.ts
│   │   │   └── UserRepository.ts
│   │   ├── cache/
│   │   │   └── BaziCache.ts
│   │   └── external/
│   │       └── LichVietClient.ts
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
// BaziChart Entity
interface BaziChart {
  id: string;
  userId: string;
  
  // Thông tin thời gian
  birthDate: Date;
  birthTime: string; // "HH:MM" format
  timeZone: string;
  lunarDate: LunarDate;
  
  // Bốn trụ (Tứ Trụ)
  yearPillar: Pillar;
  monthPillar: Pillar;
  dayPillar: Pillar;
  hourPillar: Pillar;
  
  // Ngũ Hành
  elementBalance: ElementBalance;
  dominantElement: Element;
  weakElement: Element;
  
  // Cung Mệnh
  menhInfo: MenhInfo;
  
  // Nắp Ấm
  napAm: NapAmInfo;
  
  // Metadata
  createdAt: Date;
  updatedAt: Date;
  version: number;
}

interface Pillar {
  can: Can;      // Thiên Can
  chi: Chi;      // Địa Chi
  nhAm: number;  // Nạp Âm (âm/dương)
  napAm: string; // Tên Nạp Âm
  hiddenStem: Can[]; // Can ẩn trong Chi
}

interface LunarDate {
  day: number;
  month: number;
  year: number;
  isLeapMonth: boolean;
}

interface ElementBalance {
  wood: number;   // Mộc
  fire: number;   // Hỏa
  earth: number;  // Thổ
  metal: number;  // Kim
  water: number;  // Thủy
}

interface MenhInfo {
  menh: string;           // Tên Cung Mệnh
  element: Element;       // Hành của Mệnh
  napAm: string;          // Nạp Âm của Mệnh
  can: Can;               // Can của Mệnh
  description: string;
  strengths: string[];
  weaknesses: string[];
  compatibleElements: Element[];
  inCompatibleElements: Element[];
}

interface NapAmInfo {
  yearOfBirth: string;
  napAmName: string;
  description: string;
  characteristics: string[];
  suitableDirections: Direction[];
  suitableColors: string[];
  luckyNumbers: number[];
}
```

### 2.2 Database Schema (PostgreSQL)

```sql
-- Bảng chính lưu trữ Tứ Trụ
CREATE TABLE bazi_charts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    
    -- Thông tin sinh
    birth_date DATE NOT NULL,
    birth_time TIME NOT NULL,
    timezone VARCHAR(50) NOT NULL,
    
    -- Dương lịch
    solar_day INT NOT NULL,
    solar_month INT NOT NULL,
    solar_year INT NOT NULL,
    
    -- Âm lịch
    lunar_day INT NOT NULL,
    lunar_month INT NOT NULL,
    lunar_year INT NOT NULL,
    is_leap_month BOOLEAN DEFAULT FALSE,
    
    -- Năm Trụ
    year_can VARCHAR(2) NOT NULL,
    year_chi VARCHAR(2) NOT NULL,
    year_nap_am VARCHAR(10),
    
    -- Tháng Trụ
    month_can VARCHAR(2) NOT NULL,
    month_chi VARCHAR(2) NOT NULL,
    month_nap_am VARCHAR(10),
    
    -- Ngày Trụ
    day_can VARCHAR(2) NOT NULL,
    day_chi VARCHAR(2) NOT NULL,
    day_nap_am VARCHAR(10),
    
    -- Giờ Trụ
    hour_can VARCHAR(2) NOT NULL,
    hour_chi VARCHAR(2) NOT NULL,
    hour_nap_am VARCHAR(10),
    
    -- Ngũ Hành tương sinh/tương khắc
    element_wood INT DEFAULT 0,
    element_fire INT DEFAULT 0,
    element_earth INT DEFAULT 0,
    element_metal INT DEFAULT 0,
    element_water INT DEFAULT 0,
    
    -- Cung Mệnh
    menh_name VARCHAR(50),
    menh_element VARCHAR(10),
    
    -- Nắp Ấm
    nap_am_name VARCHAR(50),
    
    -- Metadata
    version INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng quan hệ Bazi
CREATE TABLE bazi_relations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chart_id UUID REFERENCES bazi_charts(id) ON DELETE CASCADE,
    
    -- Mối quan hệ giữa các Can
    can_relation JSONB,
    
    -- Mối quan hệ giữa các Chi  
    chi_relation JSONB,
    
    -- Mối quan hệ với Cung Mệnh
    menh_relation JSONB,
    
    -- Tương Sinh
    generative_interactions JSONB,
    
    -- Tương Khắc
    controlling_interactions JSONB,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng lưu Interpretation và Reports
CREATE TABLE bazi_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chart_id UUID REFERENCES bazi_charts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    
    -- Phân tích tổng quát
    general_analysis TEXT,
    
    -- Phân tích chi tiết từng Trụ
    year_pillar_analysis TEXT,
    month_pillar_analysis TEXT,
    day_pillar_analysis TEXT,
    hour_pillar_analysis TEXT,
    
    -- Cung Mệnh
    menh_analysis TEXT,
    
    -- Nắp Ấm
    nap_am_analysis TEXT,
    
    -- Ngũ Hành
    element_analysis TEXT,
    
    -- Vận hạn
    fortune_analysis TEXT,
    
    -- Recommendations
    recommendations JSONB,
    
    -- Version để cache
    version INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_bazi_charts_user_id ON bazi_charts(user_id);
CREATE INDEX idx_bazi_charts_birth_date ON bazi_charts(birth_date);
CREATE INDEX idx_bazi_charts_lunar ON bazi_charts(lunar_year, lunar_month, lunar_day);
CREATE INDEX idx_bazi_reports_chart_id ON bazi_reports(chart_id);
```

## 3. API Design

### 3.1 REST API Endpoints

```
Base URL: /api/v1/bazi

# Chart Management
POST   /charts                    # Tạo Bazi Chart mới
GET    /charts/:id                # Lấy Bazi Chart theo ID
GET    /charts/user/:userId       # Lấy tất cả charts của user
PUT    /charts/:id                # Cập nhật chart
DELETE /charts/:id                # Xóa chart

# Analysis Endpoints
GET    /charts/:id/analysis       # Phân tích tổng quát
GET    /charts/:id/cung-menh      # Phân tích Cung Mệnh
GET    /charts/:id/nap-am         # Phân tích Nắp Ấm
GET    /charts/:id/ngu-hanh       # Phân tích Ngũ Hành
GET    /charts/:id/van-han        # Phân tích Vận Hạn
GET    /charts/:id/relations      # Phân tích quan hệ

# Report Endpoints
GET    /charts/:id/report         # Lấy full report
POST   /charts/:id/report/regenerate # Tạo lại report

# Utility Endpoints
GET    /lich-viet/lunar-date       # Chuyển đổi Dương → Âm lịch
GET    /lich-viet/solar-date      # Chuyển đổi Âm → Dương lịch
GET    /thien-can                  # Danh sách Thiên Can
GET    /dia-chi                    # Danh sách Địa Chi
GET    /nap-am                     # Danh sách Nạp Âm
```

### 3.2 Request/Response Examples

```typescript
// POST /api/v1/bazi/charts - Tạo Bazi Chart mới
interface CreateBaziRequest {
  birthDate: string;      // "1990-05-15"
  birthTime: string;      // "14:30"
  timeZone: string;       // "Asia/Ho_Chi_Minh"
  gender: 'male' | 'female';
  name?: string;
}

interface CreateBaziResponse {
  success: boolean;
  data: {
    chart: BaziChart;
    analysis: {
      elementBalance: ElementBalance;
      menh: string;
      napAm: string;
    };
  };
  meta: {
    calculationTime: number; // ms
    cacheHit: boolean;
  };
}

// GET /api/v1/bazi/charts/:id/analysis
interface BaziAnalysisResponse {
  success: boolean;
  data: {
    chartId: string;
    
    // Tứ Trụ
    fourPillars: {
      year: PillarAnalysis;
      month: PillarAnalysis;
      day: PillarAnalysis;
      hour: PillarAnalysis;
    };
    
    // Cung Mệnh
    menh: MenhAnalysis;
    
    // Nắp Ấm
    napAm: NapAmAnalysis;
    
    // Ngũ Hành
    elements: ElementAnalysis;
    
    // Quan hệ
    relations: RelationAnalysis;
    
    // Vận hạn
    fortune: FortuneAnalysis;
  };
}
```

### 3.3 GraphQL Schema

```graphql
type Query {
  # Lấy Bazi Chart
  baziChart(id: ID!): BaziChart
  
  # Lấy tất cả charts của user
  userBaziCharts(userId: ID!): [BaziChart!]!
  
  # Phân tích nhanh
  quickBaziAnalysis(input: BaziInput!): BaziAnalysis!
}

type Mutation {
  # Tạo Chart mới
  createBaziChart(input: CreateBaziInput!): BaziChart!
  
  # Cập nhật Chart
  updateBaziChart(id: ID!, input: UpdateBaziInput!): BaziChart!
  
  # Xóa Chart
  deleteBaziChart(id: ID!): Boolean!
}

input BaziInput {
  birthDate: String!
  birthTime: String!
  timeZone: String!
  gender: Gender!
}

input CreateBaziInput {
  birthDate: String!
  birthTime: String!
  timeZone: String!
  gender: Gender!
  name: String
}

type BaziChart {
  id: ID!
  userId: ID!
  
  # Thông tin sinh
  birthDate: Date!
  birthTime: String!
  lunarDate: LunarDate!
  
  # Tứ Trụ
  yearPillar: Pillar!
  monthPillar: Pillar!
  dayPillar: Pillar!
  hourPillar: Pillar!
  
  # Ngũ Hành
  elementBalance: ElementBalance!
  dominantElement: Element!
  
  # Cung Mệnh
  menh: Menh!
  
  # Nắp Ấm
  napAm: NapAm!
  
  # Reports
  reports: [BaziReport!]
}

type Pillar {
  can: Can!
  chi: Chi!
  napAm: String
  hiddenStems: [Can!]
  element: Element!
}

type Menh {
  name: String!
  element: Element!
  description: String!
  strengths: [String!]!
  weaknesses: [String!]!
}

type NapAm {
  name: String!
  description: String!
  characteristics: [String!]!
  suitableDirections: [Direction!]!
}
```

## 4. Business Logic

### 4.1 Core Services

```typescript
// BaziCalculator - Service chính tính toán Bazi
class BaziCalculator {
  constructor(
    private lunarCalendarService: LunarCalendarService,
    private napAmService: NapAmService
  ) {}

  async calculateBazi(
    birthDate: Date,
    birthTime: string,
    timeZone: string,
    gender: Gender
  ): Promise<BaziChart> {
    // 1. Chuyển đổi Dương lịch → Âm lịch
    const lunarDate = await this.lunarCalendarService.toLunar(
      birthDate,
      timeZone
    );

    // 2. Xác định Can Chi cho Ngày
    const dayCanChi = this.calculateDayCanChi(lunarDate);

    // 3. Xác định Can Chi cho Tháng
    const monthCanChi = this.calculateMonthCanChi(lunarDate.year, lunarDate.month);

    // 4. Xác định Can Chi cho Năm
    const yearCanChi = this.calculateYearCanChi(lunarDate.year);

    // 5. Xác định Can Chi cho Giờ
    const hourCanChi = this.calculateHourCanChi(dayCanChi.can, birthTime);

    // 6. Tính Nạp Âm
    const pillars = [yearCanChi, monthCanChi, dayCanChi, hourCanChi];
    const napAmInfo = this.napAmService.calculateNapAm(pillars);

    // 7. Tính Ngũ Hành
    const elementBalance = this.calculateElementBalance(pillars);

    // 8. Xác định Cung Mệnh
    const menhInfo = this.determineMenh(dayCanChi, gender);

    return {
      id: generateUUID(),
      birthDate,
      birthTime,
      timeZone,
      lunarDate,
      yearPillar: yearCanChi,
      monthPillar: monthCanChi,
      dayPillar: dayCanChi,
      hourPillar: hourCanChi,
      elementBalance,
      menhInfo,
      napAmInfo,
      createdAt: new Date(),
      updatedAt: new Date(),
      version: 1
    };
  }

  private calculateDayCanChi(lunarDate: LunarDate): Pillar {
    // Sử dụng thuật toán Lịch Việt
    const jd = this.lunarToJulianDay(lunarDate);
    const dayIndex = (jd + 1) % 10;
    const chiIndex = (jd + 1) % 12;
    return {
      can: CAN[dayIndex],
      chi: CHI[chiIndex],
      napAm: this.napAmService.getNapAm(CAN[dayIndex], CHI[chiIndex]),
      hiddenStem: this.getHiddenStems(CHI[chiIndex])
    };
  }

  private calculateYearCanChi(lunarYear: number): Pillar {
    const canIndex = (lunarYear + 6) % 10;
    const chiIndex = (lunarYear + 8) % 12;
    return {
      can: CAN[canIndex],
      chi: CHI[chiIndex],
      napAm: this.napAmService.getNapAm(CAN[canIndex], CHI[chiIndex]),
      hiddenStem: []
    };
  }

  private calculateMonthCanChi(yearCan: Can, month: number): Pillar {
    const canTable = [
      ['Giáp', 'Ất'], ['Bính', 'Đinh'], ['Mậu', 'Kỷ'],
      ['Canh', 'Tân'], ['Nhâm', 'Quý']
    ];
    const yearCanIndex = CAN.indexOf(yearCan);
    const canGroup = Math.floor(yearCanIndex / 2);
    const canIndex = (yearCanIndex % 2 === 0) ? canTable[canGroup][0] : canTable[canGroup][1];
    
    const monthChi = CHI[(month + 1) % 12];
    return {
      can: canIndex,
      chi: monthChi,
      napAm: this.napAmService.getNapAm(canIndex, monthChi),
      hiddenStem: []
    };
  }

  private calculateHourCanChi(dayCan: Can, time: string): Pillar {
    const [hours] = time.split(':').map(Number);
    const chiIndex = Math.floor((hours + 1) / 2) % 12;
    
    // Bảng tính Giờ Can
    const canTable = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý'];
    const dayCanIndex = CAN.indexOf(dayCan);
    const hourCanIndex = (dayCanIndex % 5) * 2 + Math.floor(chiIndex / 2);
    
    return {
      can: canTable[hourCanIndex % 10],
      chi: CHI[chiIndex],
      napAm: this.napAmService.getNapAm(canTable[hourCanIndex % 10], CHI[chiIndex]),
      hiddenStem: []
    };
  }
}

// NapAmService - Service tính Nạp Âm
class NapAmService {
  private readonly NAP_AM_RULES = {
    // Nạp Âm theo Can-Chi của Năm
    'Giáp Tý': 'Hải Trung Kim',
    'Ất Tý': 'Hải Trung Kim',
    'Bính Tý': 'Diện Không Hỏa',
    'Đinh Tý': 'Diện Không Hỏa',
    'Mậu Tý': 'Sơn Hạ Hỏa',
    'Kỷ Tý': 'Sơn Hạ Hỏa',
    // ... (đầy đủ 60 Nạp Âm)
  };

  calculateNapAm(pillars: Pillar[]): NapAmInfo {
    // Nạp Âm chính dựa vào Năm
    const yearPillar = pillars[0];
    const napAmName = this.NAP_AM_RULES[`${yearPillar.can} ${yearPillar.chi}`];
    
    return {
      name: napAmName,
      element: this.getNapAmElement(napAmName),
      description: NAP_AM_DESCRIPTIONS[napAmName],
      characteristics: NAP_AM_CHARACTERISTICS[napAmName],
      suitableDirections: NAP_AM_DIRECTIONS[napAmName],
      luckyNumbers: NAP_AM_NUMBERS[napAmName]
    };
  }

  getNapAm(can: string, chi: string): string {
    return this.NAP_AM_RULES[`${can} ${chi}`] || 'Không xác định';
  }

  private getNapAmElement(napAmName: string): Element {
    const elementMap = {
      'Kim': 'metal',
      'Mộc': 'wood',
      'Thủy': 'water',
      'Hỏa': 'fire',
      'Thổ': 'earth'
    };
    return elementMap[napAmName] || 'unknown';
  }
}

// CungMenhService - Service phân tích Cung Mệnh
class CungMenhService {
  private readonly MENH_TABLE = {
    male: {
      'Giáp': 'Mộc', 'Ất': 'Mộc',
      'Bính': 'Hỏa', 'Đinh': 'Hỏa',
      'Mậu': 'Thổ', 'Kỷ': 'Thổ',
      'Canh': 'Kim', 'Tân': 'Kim',
      'Nhâm': 'Thủy', 'Quý': 'Thủy'
    },
    female: {
      'Giáp': 'Mộc', 'Ất': 'Mộc',
      'Bính': 'Hỏa', 'Đinh': 'Hỏa',
      'Mậu': 'Thổ', 'Kỷ': 'Thổ',
      'Canh': 'Kim', 'Tân': 'Kim',
      'Nhâm': 'Thủy', 'Quý': 'Thủy'
    }
  };

  analyzeMenh(dayPillar: Pillar, gender: Gender): MenhInfo {
    const can = dayPillar.can;
    const menhElement = this.MENH_TABLE[gender][can];
    
    return {
      menh: `${can} ${menhElement}`,
      element: menhElement,
      napAm: dayPillar.napAm,
      description: this.getMenhDescription(menhElement),
      strengths: this.getStrengths(menhElement),
      weaknesses: this.getWeaknesses(menhElement),
      compatibleElements: this.getCompatibleElements(menhElement),
      inCompatibleElements: this.getInCompatibleElements(menhElement)
    };
  }
}
```

## 5. Caching Strategy

### 5.1 Redis Cache Structure

```typescript
interface CacheStrategy {
  // Cache key patterns
  keys: {
    baziChart: 'bazi:chart:{id}',
    userCharts: 'bazi:user:{userId}:charts',
    analysis: 'bazi:analysis:{chartId}',
    lunarDate: 'lichviet:lunar:{date}',
    napAm: 'napam:{can}:{chi}'
  };

  // TTL settings
  ttl: {
    chartData: 86400,      // 24 hours
    analysis: 43200,       // 12 hours
    lunarConversion: 604800, // 7 days (không đổi)
    napAmInfo: 2592000     // 30 days
  };

  // Cache invalidation patterns
  invalidation: {
    onChartUpdate: ['bazi:chart:*', 'bazi:analysis:*'],
    onUserUpdate: ['bazi:user:{userId}:*']
  };
}

// Cache Service Implementation
class BaziCacheService {
  async getChart(id: string): Promise<BaziChart | null> {
    const cached = await redis.get(`bazi:chart:${id}`);
    return cached ? JSON.parse(cached) : null;
  }

  async setChart(chart: BaziChart): Promise<void> {
    await redis.setex(
      `bazi:chart:${chart.id}`,
      86400,
      JSON.stringify(chart)
    );
  }

  async invalidateChart(id: string): Promise<void> {
    await redis.del(`bazi:chart:${id}`);
    await redis.del(`bazi:analysis:${id}`);
  }
}
```

## 6. Error Handling

### 6.1 Custom Exceptions

```typescript
class BaziException extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'BaziException';
  }
}

class InvalidBirthDateException extends BaziException {
  constructor(date: string) {
    super(
      `Ngày sinh không hợp lệ: ${date}`,
      'INVALID_BIRTH_DATE',
      400
    );
  }
}

class LunarConversionException extends BaziException {
  constructor(date: string, reason: string) {
    super(
      `Không thể chuyển đổi ngày ${date}: ${reason}`,
      'LUNAR_CONVERSION_ERROR',
      422
    );
  }
}

class ChartNotFoundException extends BaziException {
  constructor(chartId: string) {
    super(
      `Không tìm thấy Bazi chart với ID: ${chartId}`,
      'CHART_NOT_FOUND',
      404
    );
  }
}

class UnauthorizedAccessException extends BaziException {
  constructor() {
    super(
      'Bạn không có quyền truy cập tài nguyên này',
      'UNAUTHORIZED_ACCESS',
      403
    );
  }
}
```

## 7. Security Considerations

### 7.1 Data Protection

```typescript
// Mã hóa dữ liệu nhạy cảm
interface DataProtection {
  // Mã hóa ngày sinh khi lưu vào database
  encryptBirthDate(date: Date, userId: string): EncryptedData;
  
  // Giải mã khi cần thiết
  decryptBirthDate(encrypted: EncryptedData): Date;
  
  // Anonymize cho analytics
  anonymizeChartData(chart: BaziChart): AnonymizedChart;
}

// Rate Limiting
const rateLimiter = {
  createChart: { limit: 10, window: '1m' },
  getAnalysis: { limit: 100, window: '1m' },
  exportReport: { limit: 5, window: '1m' }
};
```
