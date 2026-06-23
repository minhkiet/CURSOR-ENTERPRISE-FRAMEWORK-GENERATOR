# Kiến Trúc Hệ Thống Numerology

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
│  │ Pythagorean  │  │  Chaldean   │  │   Kabbalah Service   │  │
│  │ Service      │  │  Service    │  │                      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  SoulUrge   │  │ Expression   │  │   LifePath Service    │  │
│  │  Service     │  │  Service     │  │                      │  │
│  └──────────────┘  └────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                       Data Access Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Repository  │  │   Cache      │  │   Lookup Tables       │ │
│  │  Pattern     │  │  (Redis)     │  │   (Letters, Numbers) │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                        Storage Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  PostgreSQL   │  │    Redis     │  │   File Storage       │ │
│  │  (Primary)    │  │  (Cache)     │  │   (Reports, Charts) │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Architecture

```
numerology-system/
├── src/
│   ├── api/
│   │   ├── controllers/
│   │   │   ├── NumerologyController.ts
│   │   │   ├── NameAnalysisController.ts
│   │   │   └── BirthNumberController.ts
│   │   ├── routes/
│   │   │   ├── numerologyRoutes.ts
│   │   │   └── apiRoutes.ts
│   │   └── middleware/
│   │       ├── auth.ts
│   │       ├── validation.ts
│   │       └── rateLimit.ts
│   ├── services/
│   │   ├── numerology/
│   │   │   ├── PythagoreanService.ts
│   │   │   ├── ChaldeanService.ts
│   │   │   ├── KabbalahService.ts
│   │   │   ├── SoulUrgeService.ts
│   │   │   ├── ExpressionService.ts
│   │   │   ├── LifePathService.ts
│   │   │   ├── PersonalityService.ts
│   │   │   ├── BirthdayService.ts
│   │   │   └── NumerologyReportGenerator.ts
│   │   └── compatibility/
│   │       ├── NameCompatibilityService.ts
│   │       └── RelationshipAnalyzer.ts
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── NumerologyChart.ts
│   │   │   ├── NameAnalysis.ts
│   │   │   └── NumberProfile.ts
│   │   ├── value-objects/
│   │   │   ├── NameNumber.ts
│   │   │   ├── BirthNumber.ts
│   │   │   └── MasterNumber.ts
│   │   └── events/
│   │       ├── CalculationCompleted.ts
│   │       └── ReportGenerated.ts
│   ├── infrastructure/
│   │   ├── repositories/
│   │   │   ├── NumerologyRepository.ts
│   │   │   └── UserRepository.ts
│   │   ├── cache/
│   │   │   └── NumerologyCache.ts
│   │   └── lookup-tables/
│   │       ├── pythagoreanTable.ts
│   │       ├── chaldeanTable.ts
│   │       └── meaningTable.ts
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
// NumerologyChart Entity
interface NumerologyChart {
  id: string;
  userId: string;
  
  // Thông tin cơ bản
  fullName: string;
  birthDate: Date;
  
  // Các số chính
  lifePathNumber: LifePathNumber;
  expressionNumber: ExpressionNumber;
  soulUrgeNumber: SoulUrgeNumber;
  personalityNumber: PersonalityNumber;
  birthdayNumber: BirthdayNumber;
  
  // Các số phụ
  maturityNumber?: MaturityNumber;
  personalYear: PersonalYearNumber;
  balanceNumber?: BalanceNumber;
  rationalityNumber?: RationalityNumber;
  
  // Name Analysis
  nameAnalysis: NameAnalysis;
  
  // Inner Dreams
  innerDreams: InnerDreams;
  
  // Hidden Passions
  hiddenPassions: HiddenPassions;
  
  // Life Cycles
  lifeCycles: LifeCycles;
  
  // Metadata
  createdAt: Date;
  updatedAt: Date;
  version: number;
}

interface LifePathNumber {
  value: number;
  masterNumber?: boolean;
  meaning: string;
  strengths: string[];
  challenges: string[];
  compatibleWith: number[];
  careerSuggestions: string[];
}

interface ExpressionNumber {
  value: number;
  masterNumber?: boolean;
  meaning: string;
  talents: string[];
  purpose: string;
  expression: string;
}

interface SoulUrgeNumber {
  value: number;
  masterNumber?: boolean;
  meaning: string;
  desires: string[];
  innerMotivation: string;
  heartDesire: string;
}

interface PersonalityNumber {
  value: number;
  masterNumber?: boolean;
  meaning: string;
  externalPersona: string;
  howOthersPerceive: string;
}

interface BirthdayNumber {
  value: number;
  meaning: string;
  trait: string;
  emphasis: string;
}

interface NameAnalysis {
  // Chaldean
  chaldeanNameNumber: number;
  chaldeanMeaning: string;
  
  // Pythagorean
  pythagoreanNameNumber: number;
  pythagoreanMeaning: string;
  
  // Combined
  combinedAnalysis: string;
  
  // Letter Analysis
  vowelNumber: number;
  consonantNumber: number;
}

interface LifeCycles {
  firstCycle: CycleInfo;
  secondCycle: CycleInfo;
  thirdCycle: CycleInfo;
  pinnacleNumbers: number[];
  challengeNumbers: number[];
}

interface CycleInfo {
  duration: string;
  startAge: number;
  endAge: number;
  number: number;
  meaning: string;
}

// Master Numbers (11, 22, 33)
interface MasterNumber {
  value: 11 | 22 | 33;
  isActive: boolean;
  meaning: string;
  challenges: string[];
  isDoubleDigit: boolean;
}

interface NumerologySystem {
  type: 'pythagorean' | 'chaldean' | 'kabbalah' | 'combined';
  description: string;
  letterValues: Record<string, number>;
}
```

### 2.2 Database Schema (PostgreSQL)

```sql
-- Bảng chính lưu trữ Numerology
CREATE TABLE numerology_charts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    
    -- Thông tin cơ bản
    full_name VARCHAR(200) NOT NULL,
    birth_date DATE NOT NULL,
    
    -- Các số chính
    life_path_number INT NOT NULL,
    life_path_master BOOLEAN DEFAULT FALSE,
    
    expression_number INT NOT NULL,
    expression_master BOOLEAN DEFAULT FALSE,
    
    soul_urge_number INT NOT NULL,
    soul_urge_master BOOLEAN DEFAULT FALSE,
    
    personality_number INT NOT NULL,
    personality_master BOOLEAN DEFAULT FALSE,
    
    birthday_number INT NOT NULL,
    
    -- Các số phụ
    maturity_number INT,
    personal_year INT,
    balance_number INT,
    rationality_number INT,
    
    -- Name Analysis JSON
    name_analysis JSONB,
    
    -- Life Cycles JSON
    life_cycles JSONB,
    
    -- Hệ thống sử dụng
    numerology_system VARCHAR(20) DEFAULT 'pythagorean',
    
    -- Metadata
    version INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng Name Analysis chi tiết
CREATE TABLE name_analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chart_id UUID REFERENCES numerology_charts(id) ON DELETE CASCADE,
    
    full_name VARCHAR(200) NOT NULL,
    
    -- Pythagorean
    pythagorean_value INT NOT NULL,
    pythagorean_letter_values JSONB,
    
    -- Chaldean
    chaldean_value INT NOT NULL,
    chaldean_letter_values JSONB,
    
    -- Vowel/Consonant
    vowel_value INT NOT NULL,
    consonant_value INT NOT NULL,
    
    -- Analysis
    combined_analysis TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng Personal Year
CREATE TABLE personal_years (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chart_id UUID REFERENCES numerology_charts(id) ON DELETE CASCADE,
    
    year INT NOT NULL,
    personal_year_number INT NOT NULL,
    meaning TEXT,
    focus_areas JSONB,
    advice TEXT,
    
    UNIQUE(chart_id, year)
);

-- Bảng Compatibility
CREATE TABLE name_compatibility (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    name1 VARCHAR(200) NOT NULL,
    name2 VARCHAR(200) NOT NULL,
    
    name1_number INT NOT NULL,
    name2_number INT NOT NULL,
    
    compatibility_score DECIMAL(3,2),
    compatibility_type VARCHAR(50),
    analysis TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_numerology_user_id ON numerology_charts(user_id);
CREATE INDEX idx_numerology_birth_date ON numerology_charts(birth_date);
CREATE INDEX idx_numerology_life_path ON numerology_charts(life_path_number);
CREATE INDEX idx_name_analysis_chart ON name_analyses(chart_id);
CREATE INDEX idx_personal_year_chart_year ON personal_years(chart_id, year);
```

## 3. API Design

### 3.1 REST API Endpoints

```
Base URL: /api/v1/numerology

# Chart Management
POST   /charts                    # Tạo Numerology Chart
GET    /charts/:id              # Lấy Chart theo ID
GET    /charts/user/:userId      # Lấy tất cả charts của user
PUT    /charts/:id               # Cập nhật chart
DELETE /charts/:id               # Xóa chart

# Number Analysis
GET    /charts/:id/life-path    # Phân tích Life Path
GET    /charts/:id/expression    # Phân tích Expression
GET    /charts/:id/soul-urge    # Phân tích Soul Urge
GET    /charts/:id/personality   # Phân tích Personality
GET    /charts/:id/birthday     # Phân tích Birthday
GET    /charts/:id/name         # Phân tích Name
GET    /charts/:id/cycles       # Phân tích Life Cycles

# Personal Year
GET    /charts/:id/personal-year # Personal Year hiện tại
GET    /charts/:id/personal-year/:year # Personal Year theo năm

# Compatibility
POST   /compatibility/name      # Kiểm tra tương thích tên
GET    /compatibility/:id       # Lấy kết quả compatibility

# Report
GET    /charts/:id/report       # Lấy full report
GET    /numbers/:number/meaning # Ý nghĩa của số

# Utils
GET    /systems                 # Danh sách các hệ thống Numerology
POST   /calculate/name           # Tính số từ tên
```

### 3.2 Request/Response Examples

```typescript
// POST /api/v1/numerology/charts
interface CreateNumerologyRequest {
  fullName: string;       // "Nguyen Van A"
  birthDate: string;      // "1990-05-15"
  system?: 'pythagorean' | 'chaldean' | 'combined';
}

interface CreateNumerologyResponse {
  success: boolean;
  data: {
    chart: NumerologyChart;
    summary: {
      lifePath: number;
      expression: number;
      soulUrge: number;
      personality: number;
      birthday: number;
    };
  };
  meta: {
    calculationTime: number;
    system: string;
  };
}

// GET /api/v1/numerology/charts/:id/life-path
interface LifePathResponse {
  success: boolean;
  data: {
    number: number;
    isMasterNumber: boolean;
    meaning: string;
    strengths: string[];
    challenges: string[];
    compatibleWith: number[];
    careerSuggestions: string[];
    lifePurpose: string;
  };
}

// GET /api/v1/numerology/charts/:id/cycles
interface LifeCyclesResponse {
  success: boolean;
  data: {
    firstCycle: {
      duration: string;
      startAge: number;
      endAge: number;
      number: number;
      meaning: string;
    };
    secondCycle: CycleInfo;
    thirdCycle: CycleInfo;
    pinnacleNumbers: number[];
    challengeNumbers: number[];
  };
}
```

## 4. Business Logic

### 4.1 Core Services

```typescript
// PythagoreanService - Hệ thống Pythagorean
class PythagoreanService {
  private readonly LETTER_VALUES: Record<string, number> = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
    'I': 9, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7,
    'Q': 8, 'R': 9, 'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6,
    'Y': 7, 'Z': 8
  };

  // Master numbers (11, 22, 33) - không giảm
  private readonly MASTER_NUMBERS = [11, 22, 33];

  calculateNameNumber(name: string): NumberResult {
    const letters = this.removeSpaces(name).toUpperCase().split('');
    let sum = 0;
    const letterValues: Record<string, number> = {};

    for (const letter of letters) {
      const value = this.LETTER_VALUES[letter] || 0;
      letterValues[letter] = value;
      sum += value;
    }

    const reducedNumber = this.reduceNumber(sum);
    
    return {
      originalSum: sum,
      reducedNumber: reducedNumber.value,
      isMasterNumber: reducedNumber.isMaster,
      letterValues,
      meaning: this.getNumberMeaning(reducedNumber.value)
    };
  }

  private reduceNumber(num: number): { value: number; isMaster: boolean } {
    // Master numbers không giảm
    if (this.MASTER_NUMBERS.includes(num)) {
      return { value: num, isMaster: true };
    }

    if (num <= 9) {
      return { value: num, isMaster: false };
    }

    return this.reduceNumber(this.sumDigits(num));
  }

  private sumDigits(num: number): number {
    return num.toString().split('').reduce((sum, digit) => sum + parseInt(digit), 0);
  }
}

// ChaldeanService - Hệ thống Chaldean
class ChaldeanService {
  private readonly LETTER_VALUES: Record<string, number> = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'U': 6, 'O': 7, 'F': 8,
    'I': 9, 'Y': 1, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'X': 6,
    'G': 7, 'H': 8, 'Z': 8, 'P': 8, 'Q': 1, 'R': 2, 'S': 3, 'T': 4,
    'V': 6, 'W': 6, 'D': 4
  };

  // Chaldean có 8 số (1-8), không có số 9
  calculateNameNumber(name: string): NumberResult {
    const letters = this.removeSpaces(name).toUpperCase().split('');
    let sum = 0;
    const letterValues: Record<string, number> = {};

    for (const letter of letters) {
      const value = this.LETTER_VALUES[letter] || 0;
      letterValues[letter] = value;
      sum += value;
    }

    const reducedNumber = this.reduceNumber(sum);
    
    return {
      originalSum: sum,
      reducedNumber: reducedNumber.value,
      isMasterNumber: reducedNumber.value > 8, // 11, 22 thường không dùng trong Chaldean
      letterValues,
      meaning: this.getNumberMeaning(reducedNumber.value)
    };
  }
}

// LifePathService - Tính Life Path Number
class LifePathService {
  constructor(
    private pythagorean: PythagoreanService
  ) {}

  calculateLifePath(birthDate: Date): LifePathNumber {
    const dateStr = this.formatBirthDate(birthDate);
    let sum = 0;

    // Cộng tất cả các chữ số trong ngày sinh
    for (const char of dateStr) {
      if (/\d/.test(char)) {
        sum += parseInt(char);
      }
    }

    const result = this.reduceToSingleDigit(sum, true); // true = allow master numbers
    
    return {
      value: result.value,
      masterNumber: result.isMaster,
      meaning: this.getLifePathMeaning(result.value),
      strengths: this.getStrengths(result.value),
      challenges: this.getChallenges(result.value),
      compatibleWith: this.getCompatibleNumbers(result.value),
      careerSuggestions: this.getCareerSuggestions(result.value)
    };
  }

  private reduceToSingleDigit(num: number, allowMaster: boolean): { value: number; isMaster: boolean } {
    if (allowMaster && [11, 22, 33].includes(num)) {
      // Tiếp tục giảm master number để lấy secondary meaning
      return { value: num, isMaster: true };
    }

    if (num <= 9) {
      return { value: num, isMaster: false };
    }

    return this.reduceToSingleDigit(
      num.toString().split('').reduce((sum, d) => sum + parseInt(d), 0),
      allowMaster
    );
  }

  private formatBirthDate(date: Date): string {
    return `${date.getFullYear()}${String(date.getMonth() + 1).padStart(2, '0')}${String(date.getDate()).padStart(2, '0')}`;
  }
}

// SoulUrgeService - Tính Soul Urge Number (chỉ tính vowels)
class SoulUrgeService {
  private readonly VOWELS = ['A', 'E', 'I', 'O', 'U', 'Y'];

  calculateSoulUrge(fullName: string): SoulUrgeNumber {
    const letters = fullName.toUpperCase().split('');
    let sum = 0;

    for (const letter of letters) {
      if (this.VOWELS.includes(letter)) {
        sum += PythagoreanService.LETTER_VALUES[letter] || 0;
      }
    }

    const result = this.reduceToSingleDigit(sum);
    
    return {
      value: result.value,
      masterNumber: result.isMaster,
      meaning: this.getSoulUrgeMeaning(result.value),
      desires: this.getDesires(result.value),
      innerMotivation: this.getInnerMotivation(result.value),
      heartDesire: this.getHeartDesire(result.value)
    };
  }
}

// ExpressionService - Tính Expression Number (tất cả letters)
class ExpressionService {
  calculateExpression(fullName: string): ExpressionNumber {
    const pythagorean = new PythagoreanService();
    const result = pythagorean.calculateNameNumber(fullName);
    
    return {
      value: result.reducedNumber,
      masterNumber: result.isMasterNumber,
      meaning: this.getExpressionMeaning(result.reducedNumber),
      talents: this.getTalents(result.reducedNumber),
      purpose: this.getPurpose(result.reducedNumber),
      expression: this.getExpression(result.reducedNumber)
    };
  }
}

// PersonalityService - Tính Personality Number (chỉ consonants)
class PersonalityService {
  private readonly VOWELS = ['A', 'E', 'I', 'O', 'U', 'Y'];

  calculatePersonality(fullName: string): PersonalityNumber {
    const letters = fullName.toUpperCase().split('');
    let sum = 0;

    for (const letter of letters) {
      if (!this.VOWELS.includes(letter) && /[A-Z]/.test(letter)) {
        sum += PythagoreanService.LETTER_VALUES[letter] || 0;
      }
    }

    const result = this.reduceToSingleDigit(sum);
    
    return {
      value: result.value,
      masterNumber: result.isMaster,
      meaning: this.getPersonalityMeaning(result.value),
      externalPersona: this.getExternalPersona(result.value),
      howOthersPerceive: this.getHowOthersPerceive(result.value)
    };
  }
}

// BirthdayService - Tính Birthday Number
class BirthdayService {
  calculateBirthday(birthDate: Date): BirthdayNumber {
    const day = birthDate.getDate();
    const result = this.reduceToSingleDigit(day);
    
    return {
      value: result.value,
      meaning: this.getBirthdayMeaning(result.value),
      trait: this.getTrait(result.value),
      emphasis: this.getEmphasis(result.value)
    };
  }

  private reduceToSingleDigit(num: number): { value: number; isMaster: boolean } {
    if ([11, 22, 33].includes(num)) {
      return { value: num, isMaster: true };
    }
    if (num <= 9) {
      return { value: num, isMaster: false };
    }
    return this.reduceToSingleDigit(
      num.toString().split('').reduce((sum, d) => sum + parseInt(d), 0),
    );
  }
}
```

## 5. Lookup Tables

### 5.1 Number Meanings

```typescript
const NUMBER_MEANINGS = {
  1: {
    meaning: 'Người khởi đầu, độc lập, lãnh đạo',
    strengths: ['Sáng tạo', 'Dũng cảm', 'Quyết đoán', 'Độc lập'],
    challenges: ['Bướng bỉnh', 'Ích kỷ', 'Thiếu kiên nhẫn'],
    compatibleWith: [1, 3, 5, 7],
    career: ['Lãnh đạo', 'Kinh doanh', 'Khởi nghiệp']
  },
  2: {
    meaning: 'Người hòa giải, ngoại giao, hợp tác',
    strengths: ['Nhạy cảm', 'Ngoại giao', 'Hợp tác', 'Trực giác'],
    challenges: ['Do dự', 'Nhút nhát', 'Phụ thuộc'],
    compatibleWith: [2, 4, 6, 8],
    career: ['Ngoại giao', 'Hòa giải', 'Tư vấn']
  },
  // ... đầy đủ cho các số 1-9 và master numbers
  11: {
    meaning: 'Người có tầm nhìn, tiên tri, mang ánh sáng',
    strengths: ['Trực giác mạnh', 'Tầm nhìn', 'Lý tưởng', 'Spiritual'],
    challenges: ['Sợ hãi', 'Lo lắng', 'Dễ tổn thương'],
    compatibleWith: [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33],
    career: ['Spiritual leader', 'Nghệ sĩ', 'Nhà tiên tri']
  },
  22: {
    meaning: 'Người xây dựng vĩ đại, master builder',
    strengths: ['Thực tiễn', 'Ambition', 'Tổ chức', 'Kỹ năng'],
    challenges: ['Căng thẳng', 'Kiểm soát', 'Impatience'],
    compatibleWith: [2, 4, 6, 8, 22],
    career: ['Xây dựng', 'Kiến trúc sư', 'Doanh nhân']
  },
  33: {
    meaning: 'Người phụng sự, teacher of teachers',
    strengths: ['Vị tha', 'Yêu thương', 'Nâng cao', 'Inspiration'],
    challenges: ['Hy sinh quá mức', 'Mệt mỏi'],
    compatibleWith: [3, 6, 9, 33],
    career: ['Giáo dục', 'Y tế', 'Tâm linh']
  }
};
```

### 5.2 Pythagorean Letter Table

```typescript
const PYTHAGOREAN_TABLE: Record<string, number> = {
  // A=1, B=2, C=3, ...
  'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
  'I': 9, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7,
  'Q': 8, 'R': 9, 'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6,
  'Y': 7, 'Z': 8
};
```

### 5.3 Chaldean Letter Table

```typescript
const CHALDEAN_TABLE: Record<string, number> = {
  // Khác với Pythagorean
  'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'U': 6, 'O': 7, 'F': 8,
  'I': 9, 'Y': 1, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'X': 6,
  'G': 7, 'H': 8, 'Z': 8, 'P': 8, 'Q': 1, 'R': 2, 'S': 3, 'T': 4,
  'V': 6, 'W': 6, 'D': 4
};
```

## 6. Caching Strategy

```typescript
interface NumerologyCacheStrategy {
  keys: {
    chart: 'numerology:chart:{id}',
    userCharts: 'numerology:user:{userId}:charts',
    nameNumber: 'numerology:name:{name}:{system}',
    lifePath: 'numerology:birthdate:{date}',
    meaning: 'numerology:meaning:{number}'
  };

  ttl: {
    chartData: 86400,      // 24 hours
    nameCalculation: 604800, // 7 days
    meaning: 2592000      // 30 days
  };
}
```

## 7. Error Handling

```typescript
class NumerologyException extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'NumerologyException';
  }
}

class InvalidNameException extends NumerologyException {
  constructor(name: string) {
    super(
      `Tên không hợp lệ: ${name}`,
      'INVALID_NAME',
      400
    );
  }
}

class InvalidBirthDateException extends NumerologyException {
  constructor(date: string) {
    super(
      `Ngày sinh không hợp lệ: ${date}`,
      'INVALID_BIRTH_DATE',
      400
    );
  }
}

class ChartNotFoundException extends NumerologyException {
  constructor(chartId: string) {
    super(
      `Không tìm thấy Numerology chart: ${chartId}`,
      'CHART_NOT_FOUND',
      404
    );
  }
}
```
