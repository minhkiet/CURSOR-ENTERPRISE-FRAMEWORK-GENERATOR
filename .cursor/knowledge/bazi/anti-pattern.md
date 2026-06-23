# Anti-Patterns trong Hệ Thống Bazi

## 1. Calculation Anti-Patterns

### 1.1 Hardcoded Magic Numbers

```typescript
// ❌ Anti-pattern: Magic numbers không giải thích
function calculateYearCan(year: number): string {
  const canIndex = (year + 6) % 10;
  // 6 và 10 là magic numbers - không rõ ý nghĩa
  const cans = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý'];
  return cans[canIndex];
}

function calculateYearChi(year: number): string {
  const chiIndex = (year + 8) % 12;
  // 8 và 12 là magic numbers
  const chis = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi'];
  return chis[chiIndex];
}

// ✅ Solution: Sử dụng Constants có ý nghĩa
const HEAVENLY_STEM_OFFSET = 6;  // Offset để tính Thiên Can
const HEAVENLY_STEM_CYCLE = 10; // Chu kỳ 10 năm của Thiên Can

const EARTHLY_BRANCH_OFFSET = 8; // Offset để tính Địa Chi  
const EARTHLY_BRANCH_CYCLE = 12; // Chu kỳ 12 năm của Địa Chi

function calculateYearCan(year: number): string {
  const canIndex = (year + HEAVENLY_STEM_OFFSET) % HEAVENLY_STEM_CYCLE;
  const cans = Object.values(Can);
  return cans[canIndex];
}

function calculateYearChi(year: number): string {
  const chiIndex = (year + EARTHLY_BRANCH_OFFSET) % EARTHLY_BRANCH_CYCLE;
  const chis = Object.values(Chi);
  return chis[chiIndex];
}
```

### 1.2 Inline Calendar Conversion

```typescript
// ❌ Anti-pattern: Tính toán âm lịch trực tiếp trong service
class BaziService {
  async calculateBazi(birthDate: Date) {
    // Tính toán âm lịch ngay trong đây - phức tạp và dễ sai
    const year = birthDate.getFullYear();
    const month = birthDate.getMonth() + 1;
    const day = birthDate.getDate();
    
    // Lunar calculation logic dài 200 dòng...
    // Rất khó debug và test
    
    return chart;
  }
}

// ✅ Solution: Tách riêng Lunar Calendar Service
interface LunarCalendarService {
  convertToLunar(solarDate: Date, timezone: string): Promise<LunarDate>;
  convertToSolar(lunarDate: LunarDate, timezone: string): Promise<Date>;
}

// Sử dụng external service hoặc library đã test
class LunarCalendarServiceImpl implements LunarCalendarService {
  constructor(private client: LichVietApiClient) {}

  async convertToLunar(solarDate: Date, timezone: string): Promise<LunarDate> {
    const response = await this.client.getLunarDate(
      solarDate,
      timezone
    );
    return response.lunarDate;
  }
}

class BaziService {
  constructor(private lunarCalendar: LunarCalendarService) {}

  async calculateBazi(birthDate: Date) {
    // Logic tính Bazi đơn giản, dễ đọc
    const lunarDate = await this.lunarCalendar.convertToLunar(
      birthDate,
      'Asia/Ho_Chi_Minh'
    );
    // ...
  }
}
```

### 1.3 Single Method God

```typescript
// ❌ Anti-pattern: Một method xử lý tất cả
class BaziCalculator {
  calculate(birthDate: Date, birthTime: string) {
    // 1. Parse date
    // 2. Convert to lunar
    // 3. Calculate year pillar
    // 4. Calculate month pillar
    // 5. Calculate day pillar
    // 6. Calculate hour pillar
    // 7. Calculate elements
    // 8. Calculate nap am
    // 9. Calculate menh
    // 10. Generate interpretation
    // 11. Save to DB
    // 12. Return result
    // Tất cả trong 500 dòng!
  }
}

// ✅ Solution: Pipeline với nhiều small methods
class BaziCalculator {
  async calculate(input: BaziInput): Promise<BaziChart> {
    const parsedDate = this.parseDate(input.birthDate);
    const lunarDate = await this.toLunar(parsedDate);
    const yearPillar = this.calcYearPillar(lunarDate.year);
    const monthPillar = this.calcMonthPillar(lunarDate, yearPillar.can);
    const dayPillar = this.calcDayPillar(lunarDate);
    const hourPillar = this.calcHourPillar(dayPillar.can, input.birthTime);
    const elements = this.calcElements([yearPillar, monthPillar, dayPillar, hourPillar]);
    const napAm = this.calcNapAm(yearPillar);
    const menh = this.determineMenh(dayPillar.can, input.gender);
    
    return new BaziChart({
      lunarDate,
      yearPillar,
      monthPillar,
      dayPillar,
      hourPillar,
      elements,
      napAm,
      menh
    });
  }

  private parseDate(dateStr: string): ParsedDate { /* ... */ }
  private async toLunar(date: ParsedDate): Promise<LunarDate> { /* ... */ }
  private calcYearPillar(year: number): Pillar { /* ... */ }
  private calcMonthPillar(lunar: LunarDate, yearCan: Can): Pillar { /* ... */ }
  private calcDayPillar(lunar: LunarDate): Pillar { /* ... */ }
  private calcHourPillar(dayCan: Can, time: string): Pillar { /* ... */ }
  private calcElements(pillars: Pillar[]): ElementBalance { /* ... */ }
  private calcNapAm(yearPillar: Pillar): string { /* ... */ }
  private determineMenh(dayCan: Can, gender: Gender): MenhInfo { /* ... */ }
}
```

## 2. Data Model Anti-Patterns

### 2.1 Flat Data Structure

```typescript
// ❌ Anti-pattern: Tất cả trong một object phẳng
interface FlatBaziChart {
  birthDate: string;
  birthTime: string;
  yearCan: string;
  yearChi: string;
  monthCan: string;
  monthChi: string;
  dayCan: string;
  dayChi: string;
  hourCan: string;
  hourChi: string;
  elementWood: number;
  elementFire: number;
  elementEarth: number;
  elementMetal: number;
  elementWater: number;
  // 30 properties nữa...
}

// Khó đọc, khó maintain, dễ sai khi truy xuất
const chart: FlatBaziChart = { /* ... */ };
const yearCanElement = chart.yearCan + ' ' + chart.yearChi; // String concatenation
const totalElements = chart.elementWood + chart.elementFire + ...; // Dễ thiếu

// ✅ Solution: Nested và typed structures
interface BaziChart {
  id: string;
  birthDate: Date;
  
  yearPillar: Pillar;
  monthPillar: Pillar;
  dayPillar: Pillar;
  hourPillar: Pillar;
  
  elementBalance: ElementBalance;
  menh: MenhInfo;
  napAm: NapAmInfo;
}

interface Pillar {
  can: Can;
  chi: Chi;
  napAm?: string;
  hiddenStems?: Can[];
}

interface ElementBalance {
  wood: number;
  fire: number;
  earth: number;
  metal: number;
  water: number;
  
  getTotal(): number;
  getDominant(): Element;
  getWeakest(): Element;
}

// Dễ đọc và type-safe
const chart: BaziChart = { /* ... */ };
const yearPillarName = `${chart.yearPillar.can} ${chart.yearPillar.chi}`;
const dominantElement = chart.elementBalance.getDominant();
```

### 2.2 Mutable State

```typescript
// ❌ Anti-pattern: Mutable chart object
class BaziService {
  async calculate(birthDate: Date) {
    const chart: any = {};
    
    // Gán từng trường một - có thể ghi đè
    chart.yearCan = this.calcYearCan(birthDate);
    chart.yearChi = this.calcYearChi(birthDate);
    
    // Có thể bị modify ở đâu đó
    chart.yearCan = 'Sai'; // Bug!
    
    // Không có validation khi update
    
    return chart;
  }
}

// ✅ Solution: Immutable với builder pattern
class BaziChartBuilder {
  private data: Partial<BaziChartData> = {};

  setBirthDate(date: Date): this {
    this.data.birthDate = date;
    return this;
  }

  setYearPillar(pillar: Pillar): this {
    this.data.yearPillar = Object.freeze(pillar);
    return this;
  }

  build(): BaziChart {
    // Validate all required fields
    this.validate();
    
    // Freeze to prevent mutation
    return Object.freeze(new BaziChart(this.data)) as BaziChart;
  }

  private validate(): void {
    if (!this.data.birthDate) throw new Error('Missing birthDate');
    if (!this.data.yearPillar) throw new Error('Missing yearPillar');
    // ...
  }
}

// Usage
const chart = new BaziChartBuilder()
  .setBirthDate(birthDate)
  .setYearPillar(yearPillar)
  .setMonthPillar(monthPillar)
  // ...
  .build();

// Không thể mutate sau khi build
// chart.birthDate = new Date(); // Error!
```

### 2.3 Missing Indexes

```typescript
// ❌ Anti-pattern: Không có indexes hoặc indexes không đúng
CREATE TABLE bazi_charts (
  id UUID PRIMARY KEY,
  user_id UUID,
  birth_date DATE,
  created_at TIMESTAMP
  -- Không có index!
);

-- Query này sẽ slow khi có nhiều records
SELECT * FROM bazi_charts 
WHERE user_id = 'xxx' 
ORDER BY created_at DESC;

// ✅ Solution: Appropriate indexes
CREATE TABLE bazi_charts (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  birth_date DATE NOT NULL,
  birth_year INT NOT NULL,
  birth_month INT NOT NULL,
  lunar_day INT NOT NULL,
  lunar_month INT NOT NULL,
  lunar_year INT NOT NULL,
  menh_element VARCHAR(10),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes cho các query patterns thường dùng
CREATE INDEX idx_bazi_user_id ON bazi_charts(user_id);
CREATE INDEX idx_bazi_birth_date ON bazi_charts(birth_date);
CREATE INDEX idx_bazi_lunar_year_month ON bazi_charts(lunar_year, lunar_month);
CREATE INDEX idx_bazi_user_created ON bazi_charts(user_id, created_at DESC);
CREATE INDEX idx_bazi_menh ON bazi_charts(menh_element) WHERE menh_element IS NOT NULL;
```

## 3. API Anti-Patterns

### 3.1 Leaky Abstraction

```typescript
// ❌ Anti-pattern: API expose internal details
interface BaziApiResponse {
  internalId: string;      // Không nên expose
  dbRowVersion: number;     // Implementation detail
  cacheKey: string;         // Leak cache implementation
  _links: {                 // Quá nhiều metadata
    self: string;
    next: string;
    prev: string;
    related: string[];
    actions: string[]
  }
}

// ✅ Solution: Clean API contract
interface BaziApiResponse {
  id: string;               // Public ID
  birthInfo: {
    date: string;
    time: string;
    timezone: string;
  };
  pillars: {
    year: PillarInfo;
    month: PillarInfo;
    day: PillarInfo;
    hour: PillarInfo;
  };
  menh: MenhSummary;
  meta: {
    version: string;        // Semantic versioning
    generatedAt: string;    // Khi nào được tạo
  }
}
```

### 3.2 N+1 Query Problem

```typescript
// ❌ Anti-pattern: N+1 khi lấy user charts
class BaziController {
  async getUserCharts(userId: string) {
    // Query 1: Lấy tất cả charts
    const charts = await this.chartRepo.findByUser(userId);
    
    // Query N: Mỗi chart gọi thêm để lấy analysis
    for (const chart of charts) {
      chart.analysis = await this.analysisRepo.findByChart(chart.id);
    }
    
    return charts;
  }
}

// ✅ Solution: Batch load hoặc JOIN
class BaziController {
  async getUserCharts(userId: string) {
    // Query 1: JOIN để lấy tất cả cùng lúc
    const charts = await this.chartRepo.findByUserWithAnalysis(userId);
    return charts;
    
    // Hoặc sử dụng DataLoader pattern
    // const loader = new DataLoader(keys => batchFetch(keys));
    // return charts.map(c => ({ ...c, analysis: loader.load(c.id) }));
  }
}

// Repository
async findByUserWithAnalysis(userId: string): Promise<BaziChartWithAnalysis[]> {
  return this.db.query(`
    SELECT 
      c.*,
      json_agg(a.*) as analyses
    FROM bazi_charts c
    LEFT JOIN bazi_analyses a ON a.chart_id = c.id
    WHERE c.user_id = $1
    GROUP BY c.id
    ORDER BY c.created_at DESC
  `, [userId]);
}
```

### 3.3 Missing Rate Limiting

```typescript
// ❌ Anti-pattern: Không có rate limit
class BaziController {
  async createChart(req: Request, res: Response) {
    // Không giới hạn - có thể bị abuse
    const chart = await this.baziService.calculate(req.body);
    res.json(chart);
  }
}

// ✅ Solution: Rate limiting cụ thể cho từng endpoint
const rateLimiter = {
  // Giới hạn chặt cho expensive operations
  createChart: { limit: 10, window: '1m', key: 'ip' },
  
  // Giới hạn vừa cho read operations
  getChart: { limit: 100, window: '1m', key: 'ip' },
  
  // Giới hạn cho export/report
  exportReport: { limit: 5, window: '5m', key: 'user' }
};

class BaziController {
  @RateLimit(rateLimiter.createChart)
  async createChart(req: Request, res: Response) {
    // Implementation
  }
}

// Hoặc sử dụng middleware
app.use('/api/v1/bazi/charts', 
  rateLimit({
    windowMs: 60 * 1000, // 1 minute
    max: 10,
    message: 'Quá nhiều yêu cầu, vui lòng thử lại sau'
  })
);
```

## 4. Caching Anti-Patterns

### 4.1 Cache Stampede

```typescript
// ❌ Anti-pattern: Nhiều requests cùng tính toán một chart
async function getChart(id: string) {
  // Request 1: Cache miss -> tính toán
  // Request 2: Cache miss -> tính toán lại
  // Request 3: Cache miss -> tính toán lại
  // ...
  // 100 requests = 100 calculations!
  
  const cached = await redis.get(`bazi:chart:${id}`);
  if (cached) return JSON.parse(cached);
  
  const chart = await calculateExpensive(id);
  await redis.setex(`bazi:chart:${id}`, 3600, JSON.stringify(chart));
  return chart;
}

// ✅ Solution: Distributed Lock hoặc Cache-aside with lock
async function getChart(id: string) {
  const cached = await redis.get(`bazi:chart:${id}`);
  if (cached) return JSON.parse(cached);

  // Try to acquire lock
  const lockKey = `lock:bazi:chart:${id}`;
  const lockAcquired = await redis.set(lockKey, '1', 'NX', 'EX', 30);

  if (!lockAcquired) {
    // Wait for other process to populate cache
    return await waitForCache(id, 5000);
  }

  try {
    const chart = await calculateExpensive(id);
    await redis.setex(`bazi:chart:${id}`, 3600, JSON.stringify(chart));
    return chart;
  } finally {
    await redis.del(lockKey);
  }
}

async function waitForCache(id: string, timeout: number): Promise<Chart> {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const cached = await redis.get(`bazi:chart:${id}`);
    if (cached) return JSON.parse(cached);
    await sleep(100);
  }
  throw new Error('Timeout waiting for cache');
}
```

### 4.2 Cache Invalidation Sprawl

```typescript
// ❌ Anti-pattern: Cache invalidation khắp nơi
class BaziService {
  async updateChart(id: string, data: UpdateData) {
    await this.chartRepo.update(id, data);
    await this.cache.del(`chart:${id}`);
    await this.cache.del(`analysis:${id}`);
    await this.cache.del(`user:${userId}:charts`);
    await this.cache.del(`report:${id}`);
    // Vô số nơi để invalidate - dễ miss
  }
}

// ✅ Solution: Centralized cache management
class CacheManager {
  private readonly cache: Redis;
  private readonly invalidationRules: Map<string, string[]>;

  constructor() {
    // Define invalidation dependencies một lần
    this.invalidationRules = new Map([
      ['bazi:chart:*', ['bazi:chart:*', 'bazi:analysis:*', 'bazi:report:*']],
      ['bazi:user:*', ['bazi:user:*', 'bazi:dashboard:*']]
    ]);
  }

  async invalidate(pattern: string): Promise<void> {
    const keys = await this.cache.keys(pattern);
    
    // Xóa tất cả matching keys
    if (keys.length > 0) {
      await this.cache.del(...keys);
    }

    // Xóa dependent caches
    const dependentPatterns = this.invalidationRules.get(pattern) || [];
    for (const depPattern of dependentPatterns) {
      await this.invalidate(depPattern);
    }
  }
}

class BaziService {
  constructor(private cacheManager: CacheManager) {}

  async updateChart(id: string, data: UpdateData) {
    await this.chartRepo.update(id, data);
    // Chỉ cần gọi một lần
    await this.cacheManager.invalidate(`bazi:chart:${id}`);
  }
}
```

## 5. Error Handling Anti-Patterns

### 5.1 Swallowing Exceptions

```typescript
// ❌ Anti-pattern: Try-catch nhưng không xử lý
async function calculateBazi(birthDate: string) {
  try {
    const lunarDate = await convertToLunar(birthDate);
    const chart = calculate(lunarDate);
    return chart;
  } catch (error) {
    // Nothing - lỗi biến mất
  }
  return null; // Hoặc return undefined - caller không biết có lỗi
}

// ✅ Solution: Specific error handling với meaningful errors
class BaziCalculationError extends Error {
  constructor(
    message: string,
    public code: string,
    public context: Record<string, unknown>
  ) {
    super(message);
    this.name = 'BaziCalculationError';
  }
}

async function calculateBazi(birthDate: string): Promise<Result<BaziChart>> {
  try {
    const lunarDate = await convertToLunar(birthDate);
    const chart = calculate(lunarDate);
    return { success: true, data: chart };
  } catch (error) {
    if (error instanceof LunarConversionError) {
      return { 
        success: false, 
        error: {
          code: 'LUNAR_CONVERSION_FAILED',
          message: `Không thể chuyển đổi ngày ${birthDate}`,
          context: { birthDate, originalError: error.message }
        }
      };
    }
    
    if (error instanceof ValidationError) {
      return {
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Dữ liệu đầu vào không hợp lệ',
          context: error.details
        }
      };
    }

    // Log unexpected errors
    logger.error('Unexpected error in calculateBazi', { error, birthDate });
    throw error;
  }
}
```

### 5.2 Generic Error Responses

```typescript
// ❌ Anti-pattern: Generic error messages
class ErrorHandler {
  handle(error: Error) {
    return {
      status: 500,
      message: 'Internal server error' // Không helpful
    };
  }
}

// ✅ Solution: Specific error types với context
class ErrorHandler {
  handle(error: Error): ErrorResponse {
    if (error instanceof ChartNotFoundError) {
      return {
        status: 404,
        code: 'CHART_NOT_FOUND',
        message: `Không tìm thấy Bazi chart với ID: ${error.chartId}`,
        details: { chartId: error.chartId }
      };
    }

    if (error instanceof InvalidBirthDateError) {
      return {
        status: 400,
        code: 'INVALID_BIRTH_DATE',
        message: error.message,
        details: {
          providedDate: error.providedDate,
          reason: error.reason,
          validRange: { min: '1900-01-01', max: new Date().toISOString() }
        }
      };
    }

    if (error instanceof UnauthorizedAccessError) {
      return {
        status: 403,
        code: 'UNAUTHORIZED',
        message: 'Bạn không có quyền truy cập tài nguyên này'
      };
    }

    // Log unexpected errors
    logger.error('Unhandled error', { error });
    
    return {
      status: 500,
      code: 'INTERNAL_ERROR',
      message: 'Đã xảy ra lỗi nội bộ, vui lòng thử lại sau'
    };
  }
}
```

## 6. Testing Anti-Patterns

### 6.1 Testing Implementation Details

```typescript
// ❌ Anti-pattern: Test internal methods
describe('BaziCalculator', () => {
  it('should calculate year can index correctly', () => {
    // Test internal implementation detail
    const index = (calculator as any).getYearCanIndex(2024);
    expect(index).toBe(0); // Giáp
  });

  it('should use correct offset for year calculation', () => {
    // Test private constant
    expect((calculator as any).YEAR_CAN_OFFSET).toBe(6);
  });
});

// ✅ Solution: Test behavior, not implementation
describe('BaziCalculator', () => {
  it('should return Giáp Tý for year 1984', () => {
    const pillar = calculator.calculateYearPillar(1984);
    expect(pillar.can).toBe(Can.Giáp);
    expect(pillar.chi).toBe(Chi.Tý);
  });

  it('should return correct pillars for a known date', () => {
    const chart = calculator.calculate({
      birthDate: new Date('1990-05-15'),
      birthTime: '14:30',
      gender: 'male'
    });

    expect(chart.yearPillar).toEqual({ can: 'Giáp', chi: 'Ngọ' });
    expect(chart.dayPillar).toEqual({ can: 'Nhâm', chi: 'Tý' });
  });
});
```

### 6.2 No Edge Case Testing

```typescript
// ❌ Anti-pattern: Chỉ test happy path
describe('BaziCalculator', () => {
  it('should calculate for normal dates', () => {
    const chart = calculator.calculate({
      birthDate: new Date('1990-01-01'),
      birthTime: '12:00'
    });
    expect(chart).toBeDefined();
  });
});

// ✅ Solution: Comprehensive edge case testing
describe('BaziCalculator', () => {
  // Boundary dates
  it('should handle minimum date (1900-01-01)', () => {
    const chart = calculator.calculate({
      birthDate: new Date('1900-01-01'),
      birthTime: '00:00'
    });
    expect(chart).toBeDefined();
    expect(chart.yearPillar.chi).toBe(Chi.Tý);
  });

  it('should handle current date', () => {
    const chart = calculator.calculate({
      birthDate: new Date(),
      birthTime: '23:59'
    });
    expect(chart).toBeDefined();
  });

  // Leap year
  it('should handle leap year dates', () => {
    const chart = calculator.calculate({
      birthDate: new Date('2024-02-29'),
      birthTime: '12:00'
    });
    expect(chart).toBeDefined();
  });

  // Timezone edge cases
  it('should handle timezone boundary', () => {
    const chart = calculator.calculate({
      birthDate: new Date('2024-01-01'),
      birthTime: '23:59',
      timezone: 'Asia/Ho_Chi_Minh'
    });
    expect(chart).toBeDefined();
  });

  // Lunar calendar edge cases
  it('should handle Tết dates correctly', () => {
    // Tết 2024: 10/02/2024 âm lịch
    const chart = calculator.calculate({
      birthDate: new Date('2024-02-10'),
      birthTime: '00:00'
    });
    // Should be first day of new lunar year
    expect(chart.lunarDate.day).toBe(1);
    expect(chart.lunarDate.month).toBe(1);
  });

  // Invalid inputs
  it('should throw for invalid date', () => {
    expect(() => {
      calculator.calculate({
        birthDate: new Date('invalid'),
        birthTime: '12:00'
      });
    }).toThrow(ValidationError);
  });

  it('should throw for future date', () => {
    const futureDate = new Date();
    futureDate.setFullYear(futureDate.getFullYear() + 1);
    
    expect(() => {
      calculator.calculate({
        birthDate: futureDate,
        birthTime: '12:00'
      });
    }).toThrow(ValidationError);
  });
});
```

## 7. Security Anti-Patterns

### 7.1 Storing Raw Sensitive Data

```typescript
// ❌ Anti-pattern: Lưu ngày sinh plain text
class UserRepository {
  async create(user: User) {
    return this.db.query(`
      INSERT INTO users (name, birth_date, email)
      VALUES ($1, $2, $3)
    `, [user.name, user.birthDate, user.email]);
    // birthDate lưu plain - có thể bị leak
  }
}

// ✅ Solution: Encrypt sensitive data
class SecureUserRepository {
  private encryption: EncryptionService;

  async create(user: User) {
    const encryptedBirthDate = this.encryption.encrypt(
      user.birthDate.toISOString(),
      process.env.ENCRYPTION_KEY
    );

    return this.db.query(`
      INSERT INTO users (name, birth_date_encrypted, email)
      VALUES ($1, $2, $3)
    `, [user.name, encryptedBirthDate, user.email]);
  }

  async getBirthDate(userId: string): Promise<Date> {
    const row = await this.db.query(
      'SELECT birth_date_encrypted FROM users WHERE id = $1',
      [userId]
    );
    
    const decrypted = this.encryption.decrypt(
      row.birth_date_encrypted,
      process.env.ENCRYPTION_KEY
    );
    
    return new Date(decrypted);
  }
}
```

### 7.2 No Input Sanitization

```typescript
// ❌ Anti-pattern: Raw user input vào database
class BaziController {
  async searchByName(req: Request, res: Response) {
    const name = req.query.name;
    
    // SQL Injection possible!
    const results = await this.db.query(
      `SELECT * FROM charts WHERE name = '${name}'`
    );
    
    // Hoặc XSS khi render
    res.render('results', { name });
  }
}

// ✅ Solution: Proper sanitization
class BaziController {
  async searchByName(req: Request, res: Response) {
    const name = this.sanitize.string(req.query.name as string);
    
    // Parameterized query
    const results = await this.db.query(
      'SELECT * FROM charts WHERE name = $1',
      [name]
    );
    
    // Sanitize output
    res.render('results', { 
      name: this.sanitize.html(name) 
    });
  }
}
```
