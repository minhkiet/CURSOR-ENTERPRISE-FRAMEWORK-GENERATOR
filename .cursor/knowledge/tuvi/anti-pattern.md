# Anti-Patterns trong Hệ Thống Tử Vi

## 1. Sao Calculation Anti-Patterns

### 1.1 Hardcoded Sao Positions

```typescript
// ❌ Anti-pattern: Sao positions hardcoded trong code
function getSaoPosition(saoName: string, birthDate: Date): string {
  if (saoName === 'Tử Vi' && birthDate.getMonth() === 0) return 'Mệnh';
  if (saoName === 'Tử Vi' && birthDate.getMonth() === 1) return 'Phụ Mẫu';
  if (saoName === 'Thiên Cơ' && birthDate.getMonth() === 0) return 'Phúc Đức';
  // ... hàng trăm dòng if-else
  return 'Unknown';
}

// ✅ Solution: Lookup table tách biệt
const SAO_POSITION_TABLE = {
  'Tử Vi': {
    ngayChinh: [0, 6],  // Index của cung
    thangChinh: [2, 8],
    // ...
  },
  'Thiên Cơ': {
    ngayChinh: [1, 7],
    // ...
  }
};

function getSaoPosition(saoName: string, index: number): number {
  const saoConfig = SAO_POSITION_TABLE[saoName];
  if (!saoConfig) return -1;
  
  const positions = saoConfig.ngayChinh || saoConfig.thangChinh || [];
  return positions[index % positions.length];
}
```

### 1.2 Missing Sao Type Validation

```typescript
// ❌ Anti-pattern: Không phân biệt loại sao
function addSaoToCung(cung: Cung, saoName: string) {
  cung.stars.push({ name: saoName }); // Không có type!
  cung.isEmpty = false; // Sai!
}

// ✅ Solution: Type-aware Sao addition
interface SaoInput {
  name: string;
  type: SaoType;
  brightness?: SaoBrightness;
}

function addSaoToCung(cung: Cung, saoInput: SaoInput): Cung {
  const hasChinhSao = cung.stars.some(s => s.type === SaoType.Chinh);
  const addingChinhSao = saoInput.type === SaoType.Chinh;
  
  // Chỉ đánh dấu empty = false nếu có sao chính
  const newIsEmpty = hasChinhSao || addingChinhSao 
    ? false 
    : cung.isEmpty;
  
  return {
    ...cung,
    stars: [...cung.stars, { ...saoInput }],
    isEmpty: newIsEmpty,
    occupant: addingChinhSao ? saoInput.name : cung.occupant
  };
}
```

## 2. Cung Anti-Patterns

### 2.1 Mutable Cung Array

```typescript
// ❌ Anti-pattern: Mutable cungs
function addSaoToMenhCung(chart: TuviChart, sao: Sao) {
  // Direct mutation!
  const menhCung = chart.cungs.find(c => c.name === 'Mệnh');
  menhCung.stars.push(sao);
  menhCung.isEmpty = false;
}

// Khiến chart không nhất quán
function checkChartIntegrity(chart: TuviChart) {
  // Không đáng tin vì có thể đã bị mutate
}

// ✅ Solution: Immutable operations
class CungManager {
  addSaoToCung(cungs: Cung[], cungName: CungName, sao: Sao): Cung[] {
    return cungs.map(cung => {
      if (cung.name !== cungName) return cung;
      
      return {
        ...cung,
        stars: [...cung.stars, sao],
        isEmpty: cung.stars.some(s => s.type === 'chinh') || sao.type === 'chinh'
          ? false 
          : cung.isEmpty,
        occupant: sao.type === 'chinh' ? sao.name : cung.occupant
      };
    });
  }

  removeSao(cungs: Cung[], cungName: CungName, saoName: string): Cung[] {
    return cungs.map(cung => {
      if (cung.name !== cungName) return cung;
      
      const newStars = cung.stars.filter(s => s.name !== saoName);
      const hasChinhSao = newStars.some(s => s.type === 'chinh');
      
      return {
        ...cung,
        stars: newStars,
        isEmpty: !hasChinhSao,
        occupant: hasChinhSao 
          ? newStars.find(s => s.type === 'chinh')?.name 
          : undefined
      };
    });
  }
}
```

### 2.2 Cung Index Confusion

```typescript
// ❌ Anti-pattern: Sử dụng index trực tiếp
function getCungByIndex(cungs: Cung[], index: number): Cung {
  return cungs[index]; // Không rõ index nào là gì
}

// Usage dễ confuse
const cung = getCungByIndex(cungs, 5);
if (cung.name === 'Mệnh') { // Không đúng!
  // ...
}

// ✅ Solution: Named constants và accessors
const CUNG_INDICES = {
  MENH: 0,
  PHU_MAU: 1,
  PHUC_DUC: 2,
  DIEN_TRACH: 3,
  QUAN_LOC: 4,
  NO_BOC: 5,
  THIEN_DI: 6,
  TAT_ACH: 7,
  TAI_BACH: 8,
  TU_TUC: 9,
  PHU_THE: 10,
  HUYET: 11
} as const;

const CUNG_NAMES = [
  'Mệnh', 'Phụ Mẫu', 'Phúc Đức', 'Điền Trạch',
  'Quan Lộc', 'Nô Bộc', 'Thiên Di', 'Tật Ách',
  'Tài Bạch', 'Tử Tức', 'Phu Thê', 'Huỵệt'
] as const;

class CungAccessor {
  static getByIndex(cungs: Cung[], index: number): Cung {
    return cungs[index];
  }

  static getByName(cungs: Cung[], name: CungName): Cung | undefined {
    return cungs.find(c => c.name === name);
  }

  static getMenh(cungs: Cung[]): Cung {
    return cungs[CUNG_INDICES.MENH];
  }

  static getCungTheoViTri(cungs: Cung[], viTri: number): Cung {
    return cungs[viTri % 12];
  }
}
```

## 3. Vận Hạn Anti-Patterns

### 3.1 Linear Vận Calculation

```typescript
// ❌ Anti-pattern: Tính vận tuyến tính
function calculateVanHan(birthYear: number): VanHan[] {
  const vans: VanHan[] = [];
  
  for (let i = 0; i < 12; i++) {
    const year = birthYear + i * 10;
    vans.push({
      year,
      van: i % 3 === 0 ? 'thien' : i % 3 === 1 ? 'nhan' : 'dia'
    });
  }
  
  return vans;
}

// ✅ Solution: Vận với rules rõ ràng
function calculateVanHan(birthYear: number, gender: Gender): VanHan[] {
  const vans: VanHan[] = [];
  const startYear = gender === 'male' ? birthYear : birthYear + 1;
  const vanTypes: VanType[] = ['thien', 'nhan', 'dia'];
  
  for (let i = 0; i < 12; i++) {
    const vanYear = startYear + i * 10;
    const age = vanYear - birthYear;
    const vanType = vanTypes[i % 3];
    
    vans.push({
      year: vanYear,
      age,
      van: vanType,
      han: calculateHan(vanYear, vanType, gender),
      lichSu: getLichSu(age, gender),
      forecast: generateForecast(vanYear, vanType)
    });
  }
  
  return vans;
}
```

### 3.2 Hardcoded Han Table

```typescript
// ❌ Anti-pattern: Hardcoded hạn
const THIEN_HAN = [
  'Tràng Sinh', 'Mộc Dục', 'Quan Đới', 'Mộc Trì',
  'Mộc Tàng', 'Hoang Vu', 'Kiếp Tài', 'Ngũ Bất',
  'Tử Thọ', 'Phúc Dương', 'Đại Hao', 'Thiên Khốc'
];

// Usage dễ sai
const hanIndex = Math.floor(age / 10) % 12;
const han = THIEN_HAN[hanIndex]; // Không clear!

// ✅ Solution: Structured Han data
interface Han {
  name: string;
  element: Element;
  meaning: string;
  favorable: boolean;
  avoid: string[];
}

const HAN_TABLE: Record<VanType, Han[]> = {
  thien: [
    { name: 'Tràng Sinh', element: 'Mộc', meaning: 'Sống lâu, khỏe mạnh', favorable: true, avoid: [] },
    { name: 'Mộc Dục', element: 'Mộc', meaning: 'Tắm rửa, thanh tẩy', favorable: true, avoid: [] },
    { name: 'Quan Đới', element: 'Mộc', meaning: 'Quan tài, chấm dứt', favorable: false, avoid: ['cưới hỏi', 'khởi nghiệp'] },
    // ... có ý nghĩa rõ ràng
  ],
  nhan: [
    // ... structured data
  ],
  dia: [
    // ... structured data
  ]
};

function getHan(vanType: VanType, age: number): Han {
  const hanIndex = Math.floor(age / 10) % 12;
  return HAN_TABLE[vanType][hanIndex];
}
```

## 4. Analysis Anti-Patterns

### 4.1 Monolithic Analysis

```typescript
// ❌ Anti-pattern: Tất cả phân tích trong một method
function analyzeChart(chart: TuviChart): string {
  let result = '';
  
  // Menh cach
  result += 'Mệnh: ' + chart.menhCach.name + '\n';
  
  // Cungs - tất cả trong một vòng
  for (const cung of chart.cungs) {
    result += cung.name + ': ';
    for (const sao of cung.stars) {
      result += sao.name + ', ';
    }
    result += '\n';
  }
  
  // Van han
  result += 'Vận hạn: ' + chart.vanHan[0].van;
  
  return result; // String khó parse, không structured
}

// ✅ Solution: Structured analysis
interface AnalysisResult {
  menhCach: MenhCachAnalysis;
  cungs: Record<CungName, CungAnalysis>;
  vanHan: VanHanAnalysis;
  recommendations: Recommendation[];
}

function analyzeChart(chart: TuviChart): AnalysisResult {
  return {
    menhCach: analyzeMenhCach(chart.menhCach),
    cungs: analyzeAllCungs(chart.cungs),
    vanHan: analyzeVanHan(chart.vanHan),
    recommendations: generateRecommendations(chart)
  };
}
```

### 4.2 String Concatenation for Reports

```typescript
// ❌ Anti-pattern: Concatenate report string
function generateReport(chart: TuviChart): string {
  let report = '=== BÁO CÁO TỬ VI ===\n\n';
  report += '1. Mệnh Cách\n';
  report += 'Mệnh: ' + chart.menhCach.name + '\n';
  report += 'Hành: ' + chart.menhCach.element + '\n\n';
  
  // ... nhiều concatenation
  // Khó maintain, khó translate, khó format
  
  return report;
}

// ✅ Solution: Template-based generation
class ReportGenerator {
  private templates: ReportTemplates;

  generateReport(chart: TuviChart): Report {
    return {
      title: this.templates.title,
      sections: [
        this.generateMenhSection(chart.menhCach),
        this.generateCungSection(chart.cungs),
        this.generateSaoSection(chart.cungs),
        this.generateVanHanSection(chart.vanHan),
        this.generatePhuongMenSection(chart.phuongMen)
      ],
      footer: this.templates.footer
    };
  }

  private generateMenhSection(menh: MenhCach): ReportSection {
    return {
      title: 'I. Mệnh Cách',
      content: this.templates.menhTemplate(menh),
      order: 1
    };
  }
}
```

## 5. API Anti-Patterns

### 5.1 Exposing Internal IDs

```typescript
// ❌ Anti-pattern: Expose database IDs
interface TuviResponse {
  id: string;           // Database UUID
  _internalId: number;  // Auto-increment
  menhCach: {
    internalMenhId: number; // Internal ID
    // ...
  }
}

// ✅ Solution: Clean public API
interface TuviPublicResponse {
  id: string;           // Public ID (UUID)
  menhCach: {
    name: string;       // Public name
    element: string;    // Public element
    // ...
  };
}
```

### 5.2 Missing Input Validation

```typescript
// ❌ Anti-pattern: No validation
class TuviController {
  async createChart(req: Request, res: Response) {
    const chart = await this.service.calculate(
      req.body.birthDate,
      req.body.birthTime,
      req.body.gender
    );
    // birthDate có thể là string, number, Date object
    // birthTime có thể là '25:99'
    // gender có thể là 'other'
  }
}

// ✅ Solution: Comprehensive validation
class TuviInputValidator {
  validate(input: CreateTuviInput): ValidationResult {
    const errors: ValidationError[] = [];

    // Date validation
    if (!this.isValidDate(input.birthDate)) {
      errors.push({ field: 'birthDate', message: 'Invalid date format' });
    }

    // Time validation
    if (!this.isValidTime(input.birthTime)) {
      errors.push({ field: 'birthTime', message: 'Invalid time format' });
    }

    // Gender validation
    if (!['male', 'female'].includes(input.gender)) {
      errors.push({ field: 'gender', message: 'Gender must be male or female' });
    }

    // Range validation
    const date = new Date(input.birthDate);
    if (date > new Date()) {
      errors.push({ field: 'birthDate', message: 'Cannot be future date' });
    }
    if (date < new Date('1900-01-01')) {
      errors.push({ field: 'birthDate', message: 'Date too old' });
    }

    return { isValid: errors.length === 0, errors };
  }
}
```

## 6. Performance Anti-Patterns

### 6.1 N+1 Sao Queries

```typescript
// ❌ Anti-pattern: N+1 khi xây dựng chart
async function buildChart(birthDate: Date) {
  const chart = await createEmptyChart(birthDate);
  
  // Query riêng cho mỗi sao
  const tuVi = await db.query('SELECT * FROM sao WHERE name = ?', ['Tử Vi']);
  const thienCo = await db.query('SELECT * FROM sao WHERE name = ?', ['Thiên Cơ']);
  const thaiDuong = await db.query('SELECT * FROM sao WHERE name = ?', ['Thái Dương']);
  // ... 100+ queries!
  
  return chart;
}

// ✅ Solution: Batch load hoặc preload
async function buildChart(birthDate: Date) {
  // Load tất cả sao một lần
  const allSaos = await saoRepository.findAll();
  const saoMap = new Map(allSaos.map(s => [s.name, s]));
  
  // Sử dụng map thay vì query
  const chart = createChart(birthDate, saoMap);
  return chart;
}
```

### 6.2 Recalculating Everything

```typescript
// ❌ Anti-pattern: Recalculate on every request
async function getChartAnalysis(chartId: string) {
  // Load chart
  const chart = await chartRepo.findById(chartId);
  
  // Recalculate tất cả từ đầu
  const lunarDate = await lunarService.convert(chart.birthDate);
  const menhCach = calculateMenhCach(lunarDate, chart.gender);
  const saos = calculateSaoPosition(lunarDate, chart.cungMenhIndex);
  const vanHan = calculateVanHan(chart.birthYear, chart.gender);
  // ... recompute everything
  
  return analysis;
}

// ✅ Solution: Cache analysis results
async function getChartAnalysis(chartId: string) {
  // Check cache first
  const cached = await cache.get(`analysis:${chartId}`);
  if (cached) return cached;
  
  // Only compute if not cached
  const analysis = await computeAnalysis(chartId);
  
  // Cache the result
  await cache.setex(`analysis:${chartId}`, 43200, analysis);
  
  return analysis;
}
```

## 7. Data Model Anti-Patterns

### 7.1 Flat JSON Storage

```typescript
// ❌ Anti-pattern: Store everything as flat JSON
CREATE TABLE tuvi_charts (
  data JSONB -- Tất cả trong một JSON!
);

-- Query khó
SELECT data->>'menhCach' FROM tuvi_charts WHERE id = ?;
SELECT data->'cungs'->0->>'stars' FROM tuvi_charts WHERE id = ?;

// ✅ Solution: Normalized schema
CREATE TABLE tuvi_charts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  birth_date DATE NOT NULL,
  birth_time TIME NOT NULL,
  gender VARCHAR(10) NOT NULL,
  menh_name VARCHAR(50),
  menh_element VARCHAR(10),
  cung_menh_index INT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE chart_cungs (
  chart_id UUID REFERENCES tuvi_charts(id) ON DELETE CASCADE,
  cung_name VARCHAR(20) NOT NULL,
  stars JSONB,
  is_empty BOOLEAN,
  occupant VARCHAR(50)
);

CREATE TABLE chart_saos (
  chart_id UUID REFERENCES tuvi_charts(id) ON DELETE CASCADE,
  sao_name VARCHAR(50) NOT NULL,
  cung_name VARCHAR(20) NOT NULL,
  sao_type VARCHAR(20)
);
```

### 7.2 Missing Indexes

```typescript
// ❌ Anti-pattern: No indexes
CREATE TABLE tuvi_charts (
  id UUID PRIMARY KEY,
  birth_date DATE,
  user_id UUID,
  menh_element VARCHAR(10)
  -- No indexes!
);

-- Slow queries
SELECT * FROM tuvi_charts WHERE user_id = ? ORDER BY created_at DESC;
SELECT * FROM tuvi_charts WHERE menh_element = 'Kim';

// ✅ Solution: Proper indexes
CREATE TABLE tuvi_charts (
  id UUID PRIMARY KEY,
  birth_date DATE NOT NULL,
  birth_time TIME NOT NULL,
  user_id UUID NOT NULL,
  gender VARCHAR(10) NOT NULL,
  menh_name VARCHAR(50),
  menh_element VARCHAR(10),
  cung_menh_index INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tuvi_user_created ON tuvi_charts(user_id, created_at DESC);
CREATE INDEX idx_tuvi_menh ON tuvi_charts(menh_element);
CREATE INDEX idx_tuvi_birth_date ON tuvi_charts(birth_date);
CREATE INDEX idx_tuvi_lunar ON tuvi_charts(lunar_year, lunar_month, lunar_day);
```

## 8. Error Handling Anti-Patterns

### 8.1 Generic Error Messages

```typescript
// ❌ Anti-pattern: Generic errors
catch (error) {
  logger.error(error);
  return res.status(500).json({ message: 'Lỗi xảy ra' });
}

// ✅ Solution: Specific error handling
catch (error) {
  if (error instanceof ValidationError) {
    return res.status(400).json({
      code: 'VALIDATION_ERROR',
      message: error.message,
      details: error.errors
    });
  }
  
  if (error instanceof ChartNotFoundError) {
    return res.status(404).json({
      code: 'CHART_NOT_FOUND',
      message: `Không tìm thấy chart: ${error.chartId}`
    });
  }
  
  if (error instanceof LunarConversionError) {
    return res.status(422).json({
      code: 'LUNAR_CONVERSION_ERROR',
      message: 'Không thể chuyển đổi ngày âm lịch',
      details: { originalDate: error.originalDate }
    });
  }
  
  logger.error('Unexpected error', { error });
  return res.status(500).json({
    code: 'INTERNAL_ERROR',
    message: 'Đã xảy ra lỗi nội bộ'
  });
}
```

### 8.2 Swallowing Errors

```typescript
// ❌ Anti-pattern: Swallowing errors
async function calculateVanHan(chart: TuviChart) {
  try {
    return await doCalculate(chart);
  } catch (e) {
    // Error disappears!
  }
  return null; // Caller không biết có lỗi
}

// ✅ Solution: Proper error propagation
async function calculateVanHan(chart: TuviChart): Promise<VanHan[]> {
  try {
    return await doCalculate(chart);
  } catch (error) {
    throw new VanHanCalculationError(
      'Không thể tính vận hạn',
      chart.id,
      { originalError: error.message }
    );
  }
}

// Or return Result type
async function calculateVanHan(chart: TuviChart): Promise<Result<VanHan[]>> {
  try {
    const result = await doCalculate(chart);
    return { success: true, data: result };
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'VAN_HAN_ERROR',
        message: error.message
      }
    };
  }
}
```

## 9. Testing Anti-Patterns

### 9.1 Testing Without Real Data

```typescript
// ❌ Anti-pattern: Test với mock data không realistic
it('should create chart', () => {
  const chart = calculator.calculate({
    birthDate: new Date('2024-01-01'),
    birthTime: '12:00',
    gender: 'male'
  });
  
  expect(chart.menhCach.name).toBeDefined();
  // Mock data không test được logic thực
});

// ✅ Solution: Test với real cases
describe('MenhCach Calculation', () => {
  const testCases = [
    { birthDate: '1990-05-15', gender: 'male', expectedMenh: 'Kim' },
    { birthDate: '1985-03-20', gender: 'female', expectedMenh: 'Mộc' },
    { birthDate: '2000-01-01', gender: 'male', expectedMenh: 'Thủy' },
    { birthDate: '1995-08-10', gender: 'female', expectedMenh: 'Hỏa' },
  ];

  testCases.forEach(({ birthDate, gender, expectedMenh }) => {
    it(`should calculate ${expectedMenh} for ${birthDate} (${gender})`, () => {
      const chart = calculator.calculate({
        birthDate: new Date(birthDate),
        birthTime: '14:30',
        gender
      });
      
      expect(chart.menhCach.name).toBe(expectedMenh);
    });
  });
});
```

### 9.2 No Edge Case Testing

```typescript
// ❌ Anti-pattern: Chỉ happy path
describe('TuviCalculator', () => {
  it('should calculate for normal date', () => {
    // Only one test case
  });
});

// ✅ Solution: Comprehensive edge cases
describe('TuviCalculator Edge Cases', () => {
  // Boundary dates
  it('should handle earliest valid date (1900-01-01)', () => {
    // ...
  });

  it('should handle latest valid date (today)', () => {
    // ...
  });

  // Leap months
  it('should handle leap month correctly', () => {
    // 2023 has a leap month
    const chart = calculator.calculate({
      birthDate: new Date('2023-06-18'), // Leap month
      birthTime: '12:00',
      gender: 'male'
    });
    expect(chart.lunarDate.isLeapMonth).toBe(true);
  });

  // Tết dates
  it('should handle Tết date correctly', () => {
    // Tết 2024: 10/02/2024
    const chart = calculator.calculate({
      birthDate: new Date('2024-02-10'),
      birthTime: '00:00',
      gender: 'female'
    });
    expect(chart.lunarDate.day).toBe(1);
    expect(chart.lunarDate.month).toBe(1);
  });

  // Invalid inputs
  it('should throw for future date', () => {
    expect(() => {
      const future = new Date();
      future.setFullYear(future.getFullYear() + 1);
      calculator.calculate({ birthDate: future, birthTime: '12:00', gender: 'male' });
    }).toThrow(ValidationError);
  });

  it('should throw for very old date', () => {
    expect(() => {
      calculator.calculate({
        birthDate: new Date('1800-01-01'),
        birthTime: '12:00',
        gender: 'female'
      });
    }).toThrow(ValidationError);
  });
});
```
